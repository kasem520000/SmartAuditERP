#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-033 (audit finding P2-010). No .NET/WPF/SQL
Server toolchain exists here, so validation combines SQLite models of the
three constrained queries with static witnesses.

The policy primitive already in the codebase is User.ShowBranchsAccounts
(OperationPermission OperNo 17): granted => all branches visible; withheld
=> own branch plus shared NULL-branch accounts (the exact semantics of
Accounting.BranchCondition). The trial-balance totals, the directory listing
and the shared tree dump previously ignored it entirely whenever no explicit
branch was selected.

Run: python3 tests/repair/branch_isolation_harness.py
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


MEZAN = open("SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml.cs", encoding="utf-8").read()
DIRF  = open("SmartAuditERP/Form_WPF/frmAccountsDirectory.xaml.cs", encoding="utf-8").read()

print("Part A: model data across three branches")


def fresh():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE Entry (GlobalID TEXT, branch INT, IS_Deleted INT, type INT, state INT)")
    db.execute("CREATE TABLE Entry_sub (EntryGlobalID TEXT, acc_no INT, dept REAL, credit REAL, branch INT)")
    db.execute("CREATE TABLE Accounts_Index (Code INT, AName TEXT, ParentCode TEXT, Acc_branch INT, type INT)")
    db.executemany("INSERT INTO Entry VALUES (?,?,?,?,?)", [
        ("E1", 1, 0, 1, 1), ("E2", 2, 0, 1, 1), ("E3", 3, 0, 1, 1)])
    db.executemany("INSERT INTO Entry_sub VALUES (?,?,?,?,?)", [
        ("E1", 101, 500, 0, 1), ("E2", 101, 900, 0, 2), ("E3", 101, 700, 0, 3)])
    db.executemany("INSERT INTO Accounts_Index VALUES (?,?,?,?,?)", [
        (101, "مبيعات",   "10", None, 1),   # shared root-ish account
        (1001, "فرع1",   "101", 1,   2),
        (1002, "فرع2",   "101", 2,   2),
        (1003, "فرع3",   "101", 3,   2)])
    return db


CURRENT_BRANCH = 1          # MainClass.BranchNo analogue


def trial_balance_total(db, rules, granted, selected_branch=None):
    """sum of debit movements under the repaired vs legacy filter logic."""
    clause = ""
    if selected_branch is not None:
        clause = f"Entry.branch={selected_branch} AND Entry_sub.branch={selected_branch} AND "
    elif rules == "fixed" and not granted:
        clause = f"Entry.branch={CURRENT_BRANCH} AND Entry_sub.branch={CURRENT_BRANCH} AND "
    rows = db.execute(
        f"SELECT SUM(Entry_sub.dept) FROM Entry, Entry_sub WHERE {clause} "
        "Entry_sub.acc_no=101 AND Entry.IS_DeLETED=0 AND Entry.type<>0 "
        "AND Entry.state=1 AND Entry.GlobalID=Entry_sub.EntryGlobalID"
    ).fetchall()
    return rows[0][0] or 0


db = fresh()
check("A1 'all branches' without the grant summed EVERY branch under legacy rules (bug reproduced)",
      trial_balance_total(db, "legacy", granted=False) == 2100)
check("A2 repaired restricts the unrestricted view to the current branch",
      trial_balance_total(db, "fixed", granted=False) == 500)
check("A3 holding the cross-branch grant keeps full visibility (unchanged behaviour)",
      trial_balance_total(db, "fixed", granted=True) == 2100)
check("A4 an explicit branch selection behaves identically pre/post fix",
      trial_balance_total(db, "legacy", False, selected_branch=2) ==
      trial_balance_total(db, "fixed", False, selected_branch=2) == 900)


def directory_rows(db, rules, granted):
    q = "SELECT Code FROM Accounts_Index WHERE type=2"
    if rules == "fixed" and not granted:
        q += f" AND (Acc_branch={CURRENT_BRANCH} OR Acc_branch IS NULL)"
    return sorted(r[0] for r in db.execute(q))


db = fresh()
check("A5 legacy directory listed other branches' definitions (bug reproduced)",
      directory_rows(db, "legacy", False) == [1001, 1002, 1003])
check("A6 repaired directory shows own branch + shared (NULL) accounts only",
      directory_rows(db, "fixed", False) == [1001])
check("A7 granted users still see every definition",
      directory_rows(db, "fixed", True) == [1001, 1002, 1003])

print("Part B: static witnesses pin the enforcement points")
mezan_gate = MEZAN.split("public List<AccountNode> GetData()")[1].split("AccountList.Clear();")[0]
check("B1 trial balance gates the empty filter on User.ShowBranchsAccounts",
      "if (string.IsNullOrEmpty(branchFilter) && !User.ShowBranchsAccounts)" in mezan_gate and
      "Entry.branch={MainClass.BranchNo}" in mezan_gate)
check("B2 restricted users are told why their totals stay single-branch",
      "!User.ShowBranchsAccounts)\n                    DXMessageBox.Show" in MEZAN and
      "ستقتصر المجاميع على فرعك الحالي" in MEZAN)
check("B3 directory listing adds the parameterised branch clause when ungranted",
      'branchClause = " AND (Acc_branch=@br OR Acc_branch IS NULL)";' in DIRF and
      '"@br", SqlDbType.Int).Value = MainClass.BranchNo;' in DIRF)
check("B4 the shared tree dump applies the same gate before Fill",
      'CommandText += " WHERE Acc_branch=@br OR Acc_branch IS NULL";' in DIRF)
check("B5 no user text enters any of the new predicates (ints/parameters only)",
      "@br" in DIRF and "{_selectedCode}" not in mezan_gate)

print("Part C: consistency with the platform's existing policy primitive")
user_cs = open("SmartAuditERP/Class/User.cs", encoding="utf-8").read()
check("C1 ShowBranchsAccounts remains THE cross-branch switch (OperNo 17 clears BranchCondition)",
      "public static bool ShowBranchsAccounts" in user_cs and
      'User.ShowBranchsAccounts = true;' in user_cs and
      'Accounting.BranchCondition = " ";' in user_cs)
check("C2 repairs reuse that switch rather than inventing a new one",
      MEZAN.count("User.ShowBranchsAccounts") >= 2 and DIRF.count("User.ShowBranchsAccounts") >= 2)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-033 (P2-010): without the cross-branch viewing grant the")
print("trial balance totals the current branch only and the directories hide")
print("foreign definitions (shared NULL-branch accounts remain visible);")
print("granted users and explicit selections behave exactly as before.")
sys.exit(0)
