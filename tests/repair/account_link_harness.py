#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-040 (audit finding P3-008). No .NET/WPF/SQL
Server toolchain exists here, so validation combines SQLite models of the
entity-binding resolution paths with static witnesses over the repaired
binders.

Legacy: Bank / Treasury / Customer constructors already carried their stored
account link inside the very query result, yet discarded it and re-resolved
the account by NAME against Accounts_Index - whose AName bears NO uniqueness
constraint (resx :38–58) - taking the first matching row. When names repeat
or drift, vouchers post against someone else's ledger account. Repaired:
trust the stored link; fall back to the historical name search ONLY for rows
where the link was never populated (preserving today's behaviour there).

Run: python3 tests/repair/account_link_harness.py
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


BANK = open("SmartAuditERP/Class/Bank.cs", encoding="utf-8").read()
TREASURY = open("SmartAuditERP/Class/Treasury.cs", encoding="utf-8").read()
CUSTOMER = open("SmartAuditERP/Class/Customer.cs", encoding="utf-8").read()


def seed():
    db = sqlite3.connect(":memory:")
    # Accounts_Index.AName carries no uniqueness constraint; two rows share one name.
    db.execute("CREATE TABLE Accounts_Index (Code INT, AName TEXT)")
    db.executemany("INSERT INTO Accounts_Index VALUES (?,?)", [
        (1211001, "خزنة الشمال"),     # inserted first -> first-row winner
        (1219999, "خزنة الشمال")])    # the treasury actually linked to THIS one
    db.execute("CREATE TABLE Stocks (id INT PRIMARY KEY, name TEXT, Acc_Code INT)")
    db.executemany("INSERT INTO Stocks VALUES (?,?,?)", [
        (1, "خزنة الشمال", 1219999),   # stored link present and correct
        (2, "بنك الأهلي", None)])      # legacy row: never linked
    return db


def name_lookup(db, name):
    """mirrors Common.GetAccountCode: first matching row, no uniqueness."""
    cur = db.execute("SELECT Code FROM Accounts_Index WHERE AName=?", (name,))
    r = cur.fetchone()
    return str(r[0]) if r else ""


def resolve(rules, db, row_id):
    """mirrors the Treasury binder after repair (Bank shares the shape)."""
    name, stored = db.execute("SELECT name, Acc_Code FROM Stocks WHERE id=?",
                              (row_id,)).fetchone()
    if rules == "legacy":
        return name_lookup(db, name)                       # discards the stored link
    if stored not in (None, "") and str(stored).strip():
        return str(stored)                                 # trust the stored link
    return name_lookup(db, name)                           # legacy fallback intact


print("Part A: duplicate-name hazard")
db = seed()
check("A1 legacy binder posts to the FIRST same-named account, not the linked one (bug)",
      resolve("legacy", db, 1) == "1211001")
check("A2 repaired binder trusts the stored link",
      resolve("fixed", db, 1) == "1219999")

print("Part B: fallback preservation for unlinked legacy rows")
for rules in ("legacy", "fixed"):
    check("B1 %s resolves an unlinked row through the historical name search" % rules,
          resolve(rules, db, 2) == "")                      # 'بنك الأهلي' absent from index
db.execute("UPDATE Stocks SET Acc_Code='' WHERE id=2")      # empty string must mean "unlinked"
db.execute("INSERT INTO Accounts_Index VALUES (1221001,'بنك الأهلي')")
check("B2 blank stored link still falls back to the name search",
      resolve("fixed", db, 2) == "1221001")

print("Part C: customer binder honours optional column presence")


def resolve_customer(rules, columns_present, value, name):
    if rules == "fixed":
        stored = value if ("AccountCode" in columns_present) else None
        if stored is not None and stored != "<<DBNull>>" and str(stored).strip():
            return str(stored)
    return "<<NAME-FALLBACK:%s>>" % name


check("C1 legacy table lacking AccountCode keeps the name fallback alive",
      resolve_customer("fixed", {"name"}, None, "عميل قديم").startswith("<<NAME-FALLBACK:"))
check("C2 populated stored link wins",
      resolve_customer("fixed", {"name", "AccountCode"}, 41007, "مؤسسة النور") == "41007")
check("C3 DBNull stored link behaves like 'never linked'",
      resolve_customer("fixed", {"name", "AccountCode"}, "<<DBNull>>", "مؤسسة النور")
      .startswith("<<NAME-FALLBACK:"))

print("Part D: static witnesses over the three binders")
for src, label in ((BANK, "Bank"), (TREASURY, "Treasury")):
    ctor = src.split(label + "(int Id)")[1]
    idx_stored = ctor.index('dataTable.Rows[0]["Acc_Code"]')
    idx_fallback = ctor.index("Common.GetAccountCode(this.Name)")
    check("D1 %s reads its stored Acc_Code before any fallback" % label,
          idx_stored < idx_fallback)
    check("D2 %s keeps the name fallback exactly once, behind the stored-link guard" % label,
          ctor.count("Common.GetAccountCode(this.Name)") == 1 and
          "? Conversions.ToString(storedAcc)" in ctor)
cust_ctor = CUSTOMER.split("Customer(int Id)")[1]
check("D3 Customer guards the column's very existence (old schemas stay safe)",
      'dataTable.Rows[0].Table.Columns.Contains("AccountCode")' in cust_ctor)
check("D4 Customer retains the single name fallback behind both guards",
      cust_ctor.count("Common.GetAccountCode(this.Name)") == 1)
check("D5 no binder dropped the original SELECT that supplies the stored link",
      "select name,Acc_Code ,DisPre from banks" in BANK and
      "select Acc_Code,name from Stocks" in TREASURY and
      "select * from customers" in CUSTOMER)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-040 (P3-008): entity binders honour their stored account")
print("link instead of a non-unique name search, with the historical fallback")
print("fully preserved for rows that were never linked.")
sys.exit(0)
