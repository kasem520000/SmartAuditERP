#!/usr/bin/env python3
"""
Repair R-006 verification harness (audit finding P7-109).

Models the period-criterion logic of
SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs::btnShow_Click using SQLite.

Defect: when the user has NOT chosen "whole period" but the month/year text fails
to parse (blank or non-numeric), the period WHERE clause was silently left empty,
so the report widened to ALL periods instead of failing or warning.

Fix: require valid year+month whenever a specific period is intended; on parse
failure stop with a clear prompt (modelled as refusing to run / returning no rows
with a signal). Valid inputs still filter correctly; "whole period" still returns
all rows. Once validated, yr/mo are integers and cannot change SQL meaning.

Scope/limits (Rule 9): verifies the criterion-construction semantics only
(verified-in-scope); WPF/.NET/SQL Server cannot run here.

Usage: python3 tests/repair/salary_period_harness.py
Exit 0 on success, 1 otherwise.
"""
import sqlite3
import sys


def build_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE SalaryPay (id INT, year TEXT, month INT, IS_Deleted INT)")
    rows = [
        (1, "2025", 1, 0),
        (2, "2025", 2, 0),
        (3, "2026", 11, 0),
        (4, "2026", 11, 0),
        (5, "2024", 7, 1),   # deleted -> always excluded
    ]
    c.executemany("INSERT INTO SalaryPay VALUES (?,?,?,?)", rows)
    return conn


def run_original(conn, whole_period, year_text, month_text):
    """Returns list of ids selected by the ORIGINAL logic."""
    cond = ""
    if not whole_period:
        try:
            yr = int(year_text); mo = int(month_text)
            cond = f" AND SalaryPay.year='{yr}' AND SalaryPay.month={mo}"
        except ValueError:
            cond = ""                 # <-- BUG: silent widening to all periods
    sql = f"SELECT id FROM SalaryPay WHERE SalaryPay.IS_Deleted=0 {cond} ORDER BY id"
    return [r[0] for r in conn.execute(sql)]


def run_fixed(conn, whole_period, year_text, month_text):
    """Returns (ok, ids). ok=False means the fixed code refuses to run (prompt shown)."""
    cond = ""
    if not whole_period:
        try:
            yr = int(year_text); mo = int(month_text)
        except ValueError:
            return (False, [])        # stop with a clear prompt; do not widen
        cond = f" AND SalaryPay.year='{yr}' AND SalaryPay.month={mo}"
    sql = f"SELECT id FROM SalaryPay WHERE SalaryPay.IS_Deleted=0 {cond} ORDER BY id"
    return (True, [r[0] for r in conn.execute(sql)])


ALL_ROWS = [1, 2, 3, 4]              # every non-deleted row, any period


def main():
    ok = True
    conn = build_db()

    # Case 1: invalid month text, specific period intended.
    orig_bad = run_original(conn, False, "2026", "abc")     # unparseable month
    fixed_bad = run_fixed(conn, False, "2026", "abc")
    print("[C1] specific period but month='abc' (invalid)")
    print("     original returns ids:", orig_bad, "| fixed:", fixed_bad)
    if orig_bad != ALL_ROWS:
        print("     ! expected original to widen to ALL rows"); ok = False
    if fixed_bad[0] is not False or fixed_bad[1] != []:
        print("     ! fixed must refuse (signal prompt) and return nothing"); ok = False

    # Case 1b: blank inputs behave like invalid.
    fixed_blank = run_fixed(conn, False, "", "")
    print("[C1b] specific period but blank inputs -> fixed:", fixed_blank)
    if fixed_blank[0] is not False:
        print("     ! blanks must also be refused"); ok = False

    # Case 2: valid specific period filters correctly under both (no regression).
    orig_ok = run_original(conn, False, "2026", "11")
    fixed_ok = run_fixed(conn, False, "2026", "11")
    print("[C2] specific period 2026/11 (valid)")
    print("     original:", orig_ok, "| fixed:", fixed_ok)
    if not (orig_ok == [3, 4] and fixed_ok == (True, [3, 4])):
        print("     ! both must select exactly the matching rows"); ok = False

    # Case 3: whole-period mode returns everything regardless of text.
    orig_all = run_original(conn, True, "", "")
    fixed_all = run_fixed(conn, True, "", "")
    print("[C3] whole-period checked")
    print("     original:", orig_all, "| fixed:", fixed_all)
    if not (orig_all == ALL_ROWS and fixed_all == (True, ALL_ROWS)):
        print("     ! whole-period must return all non-deleted rows"); ok = False

    # Deleted rows never appear in any case.
    leaked = any(5 in lst for lst in (orig_bad, orig_ok, orig_all,
                                      fixed_bad[1], fixed_ok[1], fixed_all[1]))
    if leaked:
        print("[!] deleted row leaked into results"); ok = False
    else:
        print("[C4] deleted rows excluded everywhere -> OK")

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
