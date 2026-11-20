#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-039 (audit finding P3-017) in
AccountingPeriodManager. No .NET/WPF/SQL Server toolchain exists here, so
the repair is validated as a behavioural model of each write flow with an
injected mid-sequence failure over SQLite, plus static witnesses.

Legacy: activating a period ran guard-check, mass-deactivate and target
activation as three separate statements on one open connection - a crash
between "clear all" and "set one" stranded the table with ZERO active
accounting periods while callers believed the activation succeeded. Add and
update shared the same split-write hazard with their insert/update. Repaired:
each method runs its statements in ONE transaction, committed together and
rolled back in every catch; the single-statement Close/Reopen flows were left
as-is (reopen's identity-loss concern belongs to barrier BLK-P3-018).

Run: python3 tests/repair/period_manager_harness.py
Exit 0 on PASS.
"""
import sqlite3
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


SRC = open("SmartAuditERP/Class/AccountingPeriodManager.cs", encoding="utf-8").read()


class Crash(Exception):
    pass


def seed():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE AccountingPeriods (PeriodID INTEGER PRIMARY KEY,"
               " PeriodName TEXT, IsActive INT, IsClosed INT)")
    db.executemany("INSERT INTO AccountingPeriods VALUES (?,?,?,?)",
                   [(1, "2025", 0, 0), (2, "Q1-2026", 1, 0), (3, "Q2-2026", 0, 1)])
    return db


def activate(db, rules, period_id, fail_after_clear=False):
    """mirrors ActivatePeriod; autocommit sqlite stands in for ADO.NET's per-command commits."""
    cur = db.execute("SELECT IsClosed FROM AccountingPeriods WHERE PeriodID=?", (period_id,))
    if cur.fetchone()[0]:
        raise Exception("closed")
    use_txn = rules == "fixed"
    if use_txn:
        db.execute("BEGIN")
    try:
        db.execute("UPDATE AccountingPeriods SET IsActive=0")           # clear all
        if fail_after_clear:
            raise Crash("connection lost before setting the target")    # injected fault
        n = db.execute("UPDATE AccountingPeriods SET IsActive=1 WHERE PeriodID=?",
                       (period_id,)).rowcount
        if use_txn:
            db.execute("COMMIT")
        return n > 0
    except Exception:
        if use_txn:
            db.execute("ROLLBACK")
        raise


def actives(db):
    return [r[0] for r in db.execute("SELECT PeriodID FROM AccountingPeriods WHERE IsActive=1")]


print("Part A: mid-flight failure semantics")

db = seed()
try:
    activate(db, "legacy", 1, fail_after_clear=True)
except Crash:
    pass
check("A1 legacy crash between clear and set leaves NO active period (bug reproduced)",
      actives(db) == [])

db = seed()
try:
    activate(db, "fixed", 1, fail_after_clear=True)
except Crash:
    pass
check("A2 repaired crash rolls back; the previous period stays exactly as it was",
      actives(db) == [2])

db = seed()
ok = activate(db, "fixed", 1, fail_after_clear=False)
check("A3 happy path still activates exactly one period (single-active invariant holds)",
      ok and actives(db) == [1])

db = seed()
raised = False
try:
    activate(db, "fixed", 3)                                            # closed period
except Exception:
    raised = True
check("A4 closed-period guard unchanged and writes nothing either way",
      raised and actives(db) == [2])

print("Part B: add/update split-write scenarios")


def add_active_period(db, rules, pid, name, fail_before_insert=False):
    use_txn = rules == "fixed"
    if use_txn:
        db.execute("BEGIN")
    try:
        db.execute("UPDATE AccountingPeriods SET IsActive=0")           # deactivate siblings
        if fail_before_insert:
            raise Crash("lost before INSERT")
        db.execute("INSERT INTO AccountingPeriods VALUES (?,?,?,?)", (pid, name, 1, 0))
        if use_txn:
            db.execute("COMMIT")
        return True
    except Exception:
        if use_txn:
            db.execute("ROLLBACK")
        raise


for rules in ("legacy", "fixed"):
    db = seed()
    try:
        add_active_period(db, rules, 9, "new", fail_before_insert=True)
    except Crash:
        pass
    if rules == "legacy":
        check("B1 legacy add-failure deactivated EVERYTHING and inserted nothing (bug)",
              actives(db) == [] and not any(r == (9,) for r in
                                             db.execute("SELECT PeriodID FROM AccountingPeriods WHERE PeriodID=9")))
    else:
        check("B2 repaired add-failure restores the former active period untouched",
              actives(db) == [2])

db = seed()
add_active_period(db, "fixed", 9, "new", fail_before_insert=False)
check("B3 successful add leaves precisely one active period, the new one",
      actives(db) == [9])

print("Part C: static witnesses over the manager")


def body(method):
    return SRC.split("public bool " + method)[1].split("\n\t\tpublic ")[0]


for m in ("AddPeriod", "UpdatePeriod", "ActivatePeriod"):
    b = body(m)
    check("C1 %s opens exactly one transaction, commits once, rolls back in catch" % m,
          b.count("BeginTransaction()") == 1 and b.count("transaction.Commit();") == 1 and
          "transaction?.Rollback();" in b)
    check("C2 %s declares the handle before try so catch can reach it" % m,
          "SqlTransaction transaction = null;\n\t\t\ttry" in body(m) or
          "SqlTransaction transaction = null;\n\t\t\ttry\n" in SRC.split("public bool " + m)[0][-200:])

act = body("ActivatePeriod")
check("C3 ActivatePeriod executes ALL three statements on the shared transaction",
      '"SELECT IsClosed FROM AccountingPeriods WHERE PeriodID = @ID", sqlConnection, transaction' in act and
      '"UPDATE AccountingPeriods SET IsActive = 0", sqlConnection, transaction' in act and
      '"UPDATE AccountingPeriods SET IsActive = 1 WHERE PeriodID = @ID", sqlConnection, transaction' in act)
check("C4 the guard message survives (activating a closed period still refused)",
      'throw new Exception("لا يمكن تفعيل فترة محاسبية مغلقة");' in act)

close_b = body("ClosePeriod"); reopen_b = body("ReopenPeriod")
check("C5 single-statement close/reopen flows intentionally untouched by this repair",
      "transaction" not in close_b and "transaction" not in reopen_b)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-039 (P3-017): period add/update/activation now commit as one")
print("unit; a fault midway restores the ledger instead of orphaning it with no")
print("active accounting period.")
sys.exit(0)
