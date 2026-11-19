#!/usr/bin/env python3
"""
Repair R-002 verification harness (audit finding P7-059).

Models the row-selection semantics of
SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs::ShowResult for the
"آخر حركة" (last-movement) option.

Defect: last-movement sets a single-row cap ("top (1)") while the query keeps a
FIXED ascending order, so the OLDEST matching movement is returned instead of the
most recent. Fix: order DESCENDING when the single-row cap is active; keep
ascending (chronological) for the full list.

SQL Server is unavailable here. We use in-memory SQLite, where `LIMIT n` is the
direct semantic equivalent of T-SQL `TOP n`; only the single-row cap keyword
differs, the selection/ordering behaviour under test is identical.

Scope/limits (Rule 9): verifies the selection-semantics logic only
(verified-in-scope); WPF/.NET/SQL-Server runtime remain blocked in this env.
Tie-determinism caveat: rows sharing the exact max date are not deterministically
ordered by date alone (residual noted in TRACKER, not fixed here -- avoiding
speculative reliance on id-generation order flagged elsewhere in the audit).

Usage: python3 tests/repair/last_movement_harness.py
Exit 0 on success, 1 otherwise.
"""
import sqlite3
import sys


def build_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE Inv (id INTEGER, InvGlobalID TEXT, proc_type INT,"
                " inv_type INT, cust_id INT, branch INT, Reff_No TEXT, date TEXT,"
                " IS_Deleted INT)")
    cur.execute("CREATE TABLE Inv_Sub (InvGlobalID TEXT, ItemId INT, store INT,"
                " proc_type INT, unit INT, val REAL, val1 REAL, exchange_price REAL,"
                " UnitEquality REAL)")
    # One item (ItemId=7), several movements across dates (oldest -> newest).
    rows = [
        # (id, gid, date, label-val)
        (1, "G1", "2024-01-05", 100.0),   # oldest
        (2, "G2", "2024-03-11", 250.0),
        (3, "G3", "2025-07-19", 40.0),
        (4, "G4", "2026-11-18", 999.0),   # newest
    ]
    for i, gid, date, val in rows:
        cur.execute("INSERT INTO Inv VALUES (?,?,?,?,?,?,?,?,?)",
                    (i, gid, 1, 1, 5, 1, f"REF{i}", date, 0))
        cur.execute("INSERT INTO Inv_Sub VALUES (?,?,?,?,?,?,?,?,?)",
                    (gid, 7, 3, 1, 1, val, val, 1.0, 1.0))
    # A deleted row that must be excluded by IS_Deleted=0.
    cur.execute("INSERT INTO Inv VALUES (?,?,?,?,?,?,?,?,?)",
                (9, "GX", 1, 1, 5, 1, "REFX", "2026-12-31", 1))
    cur.execute("INSERT INTO Inv_Sub VALUES (?,?,?,?,?,?,?,?,?)",
                ("GX", 7, 3, 1, 1, 12345.0, 12345.0, 1.0, 1.0))
    # A different item that must NOT match the ItemId filter.
    cur.execute("INSERT INTO Inv VALUES (?,?,?,?,?,?,?,?,?)",
                (8, "GZ", 1, 1, 5, 1, "REFZ", "2026-11-19", 0))
    cur.execute("INSERT INTO Inv_Sub VALUES (?,?,?,?,?,?,?,?,?)",
                ("GZ", 42, 3, 1, 1, 55.0, 55.0, 1.0, 1.0))
    conn.commit()
    return conn


WHERE = ("FROM Inv, Inv_Sub "
         "WHERE Inv.InvGlobalID=Inv_Sub.InvGlobalID "
         "AND Inv_Sub.proc_type IN (1,2) AND Inv.IS_Deleted=0 "
         "AND Inv_Sub.ItemId=7")


def pick_one(conn, direction):
    """Single-row cap (TOP(1)/LIMIT 1) with the given date ordering."""
    sql = (f"SELECT Inv.id AS id, date, val {WHERE} "
           f"ORDER BY Inv.date {direction} LIMIT 1")
    return conn.execute(sql).fetchone()


def full_list(conn):
    """Full chronological list (no cap), original ascending order."""
    sql = f"SELECT Inv.id AS id, date, val {WHERE} ORDER BY Inv.date ASC"
    return conn.execute(sql).fetchall()


def main():
    conn = build_db()

    oldest = pick_one(conn, "ASC")     # pre-fix behaviour (bug)
    newest = pick_one(conn, "DESC")    # post-fix behaviour
    listing = full_list(conn)          # multi-row report ordering (unchanged)

    print("[A] last-movement single-row selection")
    print("    PRE-FIX  (TOP1 + ORDER BY date ASC ) ->", oldest)
    print("    POST-FIX (TOP1 + ORDER BY date DESC) ->", newest)

    ok = True

    # Pre-fix demonstrably wrong: returns the OLDEST (id 1, year 2024).
    if oldest[0] != 1:
        print("    ! expected pre-fix to surface oldest id=1"); ok = False
    # Post-fix correct: returns the NEWEST (id 4, 2026-11-18).
    if newest[0] != 4:
        print("    ! expected post-fix to surface newest id=4"); ok = False
    # Deleted (id 9) and other-item (id 8) rows excluded from both.
    for r in (oldest, newest):
        if r[0] in (8, 9):
            print("    ! filter leak:", r); ok = False

    print("\n[B] full chronological list (multi-row path) must stay ascending")
    ids = [r[0] for r in listing]
    dates = [r[1] for r in listing]
    print("    ids   :", ids)
    print("    dates :", dates)
    if ids != [1, 2, 3, 4]:
        print("    ! full-list ordering changed unexpectedly"); ok = False
    if dates != sorted(dates):
        print("    ! full list not chronological"); ok = False

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
