#!/usr/bin/env python3
"""
Repair R-004 verification harness (audit finding P7-036).

Models the barcode-uniqueness existence check in
SmartAuditERP/Form_WPF/frmMultiBarcode.xaml.cs::IsValidBarcode using SQLite.

Defect: the original query used a comma CROSS JOIN
    FROM ItemUnits, Itembarcodes WHERE (...units...) OR (...barcodes...)
A cartesian product is empty whenever EITHER table is empty, so a barcode that
is duplicated in the non-empty table was not detected (missed duplicate).

Fix: check each table independently with UNION ALL so a match in either table is
found even if the other has no rows; existence (rowcount > 0) semantics kept.

Scope/limits (Rule 9): verifies the detection-semantics logic only
(verified-in-scope); SQL Server/WPF cannot run here. (Parameter binding hardening
applied in the same statement is not separately exercised by this model.)

Usage: python3 tests/repair/barcode_uniqueness_harness.py
Exit 0 on success, 1 otherwise.
"""
import sqlite3
import sys


def setup(item_units_rows, item_barcodes_rows):
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE ItemUnits (ItemId INT, barcode TEXT)")
    c.execute("CREATE TABLE Itembarcodes (ItemId INT, barcode TEXT)")
    c.executemany("INSERT INTO ItemUnits VALUES (?,?)", item_units_rows)
    c.executemany("INSERT INTO Itembarcodes VALUES (?,?)", item_barcodes_rows)
    return conn


def dup_original(conn, barcode, item_id):
    """Original comma cross join + OR (cartesian product)."""
    sql = ("SELECT ItemUnits.ItemId, Itembarcodes.ItemId "
           "FROM ItemUnits, Itembarcodes "
           "WHERE (ItemUnits.barcode=? AND ItemUnits.ItemId<>?) OR "
           "(Itembarcodes.barcode=? AND Itembarcodes.ItemId<>?)")
    return len(conn.execute(sql, (barcode, item_id, barcode, item_id)).fetchall()) > 0


def dup_fixed(conn, barcode, item_id):
    """Independent per-table checks combined with UNION ALL."""
    sql = ("SELECT ItemId FROM ItemUnits WHERE barcode=? AND ItemId<>? "
           "UNION ALL "
           "SELECT ItemId FROM Itembarcodes WHERE barcode=? AND ItemId<>?")
    return len(conn.execute(sql, (barcode, item_id, barcode, item_id)).fetchall()) > 0


def main():
    ok = True
    BC = "6291041500213"      # a barcode duplicated under another item (id 9)
    ME = 5                    # the item currently being edited

    # Scenario 1: ItemUnits EMPTY, but the duplicate exists in Itembarcodes.
    conn1 = setup(item_units_rows=[],                 # <-- empty table
                  item_barcodes_rows=[(9, BC)])       # duplicate here
    o1 = dup_original(conn1, BC, ME)
    f1 = dup_fixed(conn1, BC, ME)
    print("[S1] ItemUnits empty, duplicate lives in Itembarcodes")
    print("     original detects duplicate:", o1, "| fixed detects:", f1)
    if o1 is not False:
        print("     ! expected original to MISS the duplicate"); ok = False
    if f1 is not True:
        print("     ! fixed must detect the duplicate"); ok = False

    # Scenario 2: Itembarcodes EMPTY, duplicate exists in ItemUnits.
    conn2 = setup(item_units_rows=[(9, BC)],          # duplicate here
                  item_barcodes_rows=[])              # <-- empty table
    o2 = dup_original(conn2, BC, ME)
    f2 = dup_fixed(conn2, BC, ME)
    print("[S2] Itembarcodes empty, duplicate lives in ItemUnits")
    print("     original detects duplicate:", o2, "| fixed detects:", f2)
    if o2 is not False:
        print("     ! expected original to MISS the duplicate"); ok = False
    if f2 is not True:
        print("     ! fixed must detect the duplicate"); ok = False

    # Scenario 3: BOTH tables populated -> original and fixed must agree (detect).
    conn3 = setup(item_units_rows=[(9, BC)], item_barcodes_rows=[(8, BC)])
    o3 = dup_original(conn3, BC, ME)
    f3 = dup_fixed(conn3, BC, ME)
    print("[S3] both tables populated, duplicate present")
    print("     original:", o3, "| fixed:", f3)
    if not (o3 is True and f3 is True):
        print("     ! both must detect when tables are non-empty"); ok = False

    # Scenario 4: no duplicate anywhere -> both report clean (no false positive).
    conn4 = setup(item_units_rows=[(9, "OTHER")], item_barcodes_rows=[(8, "X")])
    o4 = dup_original(conn4, BC, ME)
    f4 = dup_fixed(conn4, BC, ME)
    print("[S4] no duplicate anywhere")
    print("     original:", o4, "| fixed:", f4)
    if not (o4 is False and f4 is False):
        print("     ! neither may report a duplicate that isn't there"); ok = False

    # Scenario 5: own-barcode exclusion -- the same barcode on THIS item (id ME)
    # must NOT count as a duplicate (editing an item's own barcodes).
    conn5 = setup(item_units_rows=[(ME, BC)], item_barcodes_rows=[(ME, BC)])
    f5 = dup_fixed(conn5, BC, ME)
    print("[S5] barcode belongs to the same item being edited (excluded)")
    print("     fixed reports duplicate:", f5)
    if f5 is not False:
        print("     ! own-item barcode must be excluded"); ok = False

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
