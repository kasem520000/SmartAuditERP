#!/usr/bin/env python3
"""
Repair R-005 verification harness (audit findings P7-103 and P7-104).

Models SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs using SQLite.

P7-103: the form never read the persisted print default; it always opened on the
XAML default (A4). Fix = load 'sett.val' (id=1) on open and select the matching
radio button, falling back to A4 when the setting is missing/unreadable.

P7-104: save announced success unconditionally while ignoring ExecuteNonQuery's
affected-row count; if there is no 'sett' row with id=1 nothing is persisted yet
"saved successfully" was shown. Fix = branch on the affected-row count.

Scope/limits (Rule 9): verifies the persistence round-trip and result-reporting
logic only (verified-in-scope); WPF/.NET/SQL Server cannot run here.

Usage: python3 tests/repair/print_default_harness.py
Exit 0 on success, 1 otherwise.
"""
import sqlite3
import sys

A4 = 1            # RadioButton1 -> val 1
SMALL_PAPER = 2   # RadioButton2 -> val 2


def make_db(with_row):
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE sett (id INT, val INT)")
    if with_row is not None:
        conn.execute("INSERT INTO sett VALUES (1, ?)", (with_row,))
    conn.commit()
    return conn


# ---- Load behaviour (P7-103) ------------------------------------------------

def load_fixed(conn):
    """Returns the selected print type after opening the form (fixed code)."""
    cur = conn.execute("SELECT val FROM sett WHERE id = 1")
    row = cur.fetchone()
    if row is not None and row[0] is not None:
        return SMALL_PAPER if int(row[0]) == 2 else A4
    return A4          # fallback default


def load_original(_conn):
    """Original code had no load logic -> always the XAML default (A4)."""
    return A4


# ---- Save behaviour (P7-104) ------------------------------------------------

def save(conn, value, fixed):
    """Returns (success_announced, rows_persisted_value_or_None)."""
    cur = conn.execute("UPDATE sett SET val = ? WHERE id = 1", (value,))
    conn.commit()
    affected = cur.rowcount          # == SqlCommand.ExecuteNonQuery() return
    if fixed:
        announced = affected > 0
    else:
        announced = True             # original: unconditional success
    stored = conn.execute("SELECT val FROM sett WHERE id=1").fetchone()
    return announced, (stored[0] if stored else None), affected


def main():
    ok = True

    # P7-103: a persisted SMALL_PAPER must be reflected on open (original ignored it).
    c1 = make_db(SMALL_PAPER)
    orig_sel = load_original(c1)
    fixed_sel = load_fixed(make_db(SMALL_PAPER))
    print("[L1] stored val=2 (small paper)")
    print("     original opens on:", "A4" if orig_sel == A4 else "small",
          "| fixed opens on:", "A4" if fixed_sel == A4 else "small")
    if orig_sel != A4:
        print("     ! original unexpectedly respected the setting"); ok = False
    if fixed_sel != SMALL_PAPER:
        print("     ! fixed must reflect the stored small-paper setting"); ok = False

    # Missing settings row -> fall back to A4 without error.
    fixed_missing = load_fixed(make_db(None))
    print("[L2] no sett row -> fixed falls back to:",
          "A4" if fixed_missing == A4 else "small")
    if fixed_missing != A4:
        print("     ! fallback must be A4"); ok = False

    # P7-104: saving with NO sett row must NOT announce success; row stays absent.
    c2 = make_db(None)
    ann_o, stored_o, aff_o = save(c2, SMALL_PAPER, fixed=False)
    c2b = make_db(None)
    ann_f, stored_f, aff_f = save(c2b, SMALL_PAPER, fixed=True)
    print("\n[S1] save with no sett row (nothing to update)")
    print(f"     original: announced={ann_o} affected={aff_o} stored={stored_o}")
    print(f"     fixed   : announced={ann_f} affected={aff_f} stored={stored_f}")
    if ann_o is not True:
        print("     ! original should have (wrongly) announced success"); ok = False
    if ann_f is not False or stored_f is not None:
        print("     ! fixed must NOT announce success and must persist nothing"); ok = False

    # Saving WITH an existing row must succeed and persist the new value.
    c3 = make_db(A4)
    ann3, stored3, aff3 = save(c3, SMALL_PAPER, fixed=True)
    print("\n[S2] save with existing sett row -> small paper")
    print(f"     fixed: announced={ann3} affected={aff3} stored={stored3}")
    if not (ann3 is True and stored3 == SMALL_PAPER and aff3 == 1):
        print("     ! genuine save must succeed and persist val=2"); ok = False

    # Full round trip: save small, reopen -> reflects small.
    rt = load_fixed(c3)
    print("[S3] reopen after saving small -> opens on:",
          "A4" if rt == A4 else "small")
    if rt != SMALL_PAPER:
        print("     ! round-trip failed"); ok = False

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
