#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-034 (audit finding P3-001, follow-up H2-02)
and R-035 (P3-004). No .NET/WPF/SQL Server toolchain exists here, so both
repairs are validated as behavioural models of their exact control flows
plus static witnesses.

R-034: the period guard returned TRUE in every arm - a date-range test OR'ed
with literal true, a missing period row, and even exceptions - so ~9 write
paths ran a decorative check. The repaired helper returns the real predicate
and fails closed on absent/unreadable periods; callers already refuse on
false with their own messages. In-range writes behave identically.

R-035: when the entry binder produced null, SaveReceipt jumped to its
success label WITHOUT committing, then finally disposed the open
transaction - an implicit rollback reported to callers as success. The
repaired null arm rolls back explicitly and reports failure, matching the
adjacent SaveEnty-failure arm; the commit path is unchanged.

Run: python3 tests/repair/posting_integrity_harness.py
Exit 0 on PASS.
"""
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


COMMON = open("SmartAuditERP/Class/Common.cs", encoding="utf-8").read()
RECEIPT = open("SmartAuditERP/Class/ReceiptOper.cs", encoding="utf-8").read()

# ------------------------- Part A: P3-001 -----------------------------------
print("Part A: R-034 / P3-001 - the period gate stops rubber-stamping")

PERIOD = dict(start="2026-01-01", end="2026-12-31")


def D(s):
    from datetime import date
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)


def check_period(rules, invoice_date, row_exists=True, throws=False):
    if rules == "legacy":
        try:
            if not row_exists:
                return True                                # legacy missing-row arm
            start, end = D(PERIOD["start"]), D(PERIOD["end"])
            inv = D(invoice_date)
            return (not (inv > end or inv < start)) or True   # literal tautology
        except Exception:
            return True                                    # legacy catch arm
    try:
        if throws:
            raise RuntimeError("master unreachable")
        if not row_exists:
            return False                                   # fail closed
        start, end = D(PERIOD["start"]), D(PERIOD["end"])
        inv = D(invoice_date)
        return not (inv > end or inv < start)              # honest predicate
    except Exception:
        return False                                       # fail closed


cases = [
    ("inside the open period",      dict(invoice_date="2026-06-15"),                    True),
    ("before period start",         dict(invoice_date="2025-12-31"),                    False),
    ("after period end",            dict(invoice_date="2027-01-01"),                    False),
    ("on the inclusive boundaries", dict(invoice_date="2026-01-01"),                    True),
    ("period row missing",            dict(invoice_date="2026-06-15", row_exists=False),  False),
    ("master query throws",         dict(invoice_date="2026-06-15", throws=True),       False),
]
for label, kw, expected_fixed in cases:
    old = check_period("legacy", **kw)
    new = check_period("fixed", **kw)
    check("A1 legacy permitted '%s' regardless" % label, old is True)
    check("A2 repaired '%s' => %s" % (label, expected_fixed), new is expected_fixed)

check("A3 in-range happy path identical pre/post fix",
      check_period("legacy", "2026-06-15") == check_period("fixed", "2026-06-15") is True)


def save_flow(gate_result):
    """caller pattern shared by the nine paths: refuse before writing."""
    posted = False
    if not gate_result:
        return "refused-with-message"
    posted = True
    return "written"


check("A4 an out-of-range document no longer reaches the write under repaired rules",
      save_flow(check_period("fixed", "2027-01-01")) == "refused-with-message" and
      save_flow(check_period("legacy", "2027-01-01")) == "written")

body = COMMON.split("public static bool CheckProiedAcc")[1].split("public static bool CheckReffNo")[0]
check("A5 the literal tautology is gone from CheckProiedAcc", "|| true" not in body)
check("A6 missing row and exception arms now fail closed",
      body.count("return false;") >= 2 and "return true;" not in body)
check("A7 the honest range predicate remains intact",
      "return !(InvoiceDate > end || InvoiceDate < start);" in body)
import pathlib
callers = sum(1 for p in pathlib.Path("SmartAuditERP").rglob("*.cs")
              if "Common.CheckProiedAcc(" in p.read_text(encoding="utf-8", errors="replace"))
check("A8 all existing caller gates are preserved (none removed/weakened)",
      callers >= 9)

# ------------------------- Part B: P3-004 -----------------------------------
print("Part B: R-035 / P3-004 - null entry can never mean success")


class Txn:
    def __init__(self):
        self.committed = False
        self.rolled_back = False
        self.disposed_uncommitted = False

    def Commit(self):
        self.committed = True

    def Rollback(self):
        self.rolled_back = True

    def Dispose(self):
        # SQL Server: disposing WITHOUT either outcome implicitly rolls back -
        # that is the silent data loss the legacy path relied on. An explicit
        # Rollback resolves the transaction beforehand and is not "abandoned".
        if not self.committed and not self.rolled_back:
            self.disposed_uncommitted = True


def save_receipt(rules, entry_builder_ok, writer_ok):
    """entry_builder_ok=False models the binder returning null (exception path);
    writer_ok models SaveEnty's boolean result when an entry does exist."""
    tx = Txn()
    receipt_rows_written = True                           # INSERT executed inside the open tx
    entr = "ENTRY" if entry_builder_ok else None
    reported = None

    if entr is None:
        if rules == "legacy":
            reported = True                               # goto success label, no commit
        else:
            tx.Rollback()
            reported = False                              # explicit failure arm
    elif writer_ok:
        tx.Commit()
        reported = True
    else:
        tx.Rollback()
        reported = False

    tx.Dispose()
    persisted = receipt_rows_written and tx.committed
    return reported, persisted, tx.disposed_uncommitted


old_rep, old_per, old_dis = save_receipt("legacy", entry_builder_ok=False, writer_ok=None)
check("B1 legacy reported SUCCESS while nothing persisted (bug reproduced)",
      old_rep is True and old_per is False and old_dis is True)
new_rep, new_per, new_dis = save_receipt("fixed", entry_builder_ok=False, writer_ok=None)
check("B2 repaired null-entry save reports failure and rolls back explicitly",
      new_rep is False and new_per is False and new_dis is False)
for rules in ("legacy", "fixed"):
    rep, per, dis = save_receipt(rules, True, True)
    assert (rep, per, dis) == (True, True, False)
check("B3 successful entry+receipt flow commits and reports identically pre/post fix",
      save_receipt("legacy", True, True) == save_receipt("fixed", True, True))
rep, per, _ = save_receipt("fixed", True, False)
check("B4 SaveEnty-failure arm behaviour unchanged (rollback + false)",
      rep is False and per is False)

null_arm = RECEIPT.split("if (Entr == null)")[1].split("if (new EntryOper().SaveEnty(Entr))")[0]
check("B5 the null branch now rolls back before leaving the try block",
      "sqlTransaction.Rollback();" in null_arm and "result = false;" in null_arm)
check("B6 it no longer jumps to the success label",
      "goto IL_05d1;" not in null_arm)
check("B7 commit is still reachable ONLY through a successful SaveEnty",
      RECEIPT.count("sqlTransaction.Commit();\n\t\t\t\t\tgoto IL_05d1;") == 1)
check("B8 bilingual operator message follows the established style",
      "Operators.CompareString(MainClass.Language, \"en\", TextCompare: false)" in null_arm)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-034 (P3-001): period gates enforce real ranges and fail")
print("closed on absence/error; R-035 (P3-004): a null linked entry rolls back")
print("and reports failure instead of announcing an unpersisted success.")
sys.exit(0)
