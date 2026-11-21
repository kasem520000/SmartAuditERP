#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-036 (audit findings P3-009 and P3-011) in
the customer-receipt (frmSandQ) and tax-voucher (frmSandVAT) editors. No
.NET/WPF/SQL Server toolchain exists here, so validation combines SQLite
models of the exact data scenarios with static witnesses over both forms.

P3-009: the INSERT omitted GlobalID, which the Receipts definition makes a
NOT NULL primary key without a default; and the window flipped to "existing"
before committing, so a failed insert made the next attempt take the UPDATE
branch against nothing. Repaired: fresh GUID identity per new row (the
codebase's established idiom), EntryGlobalID at the "-1" no-entry sentinel,
and mode advance only after commit.

P3-011: edit/cancel keyed on ReceiptNo+Branch although receipt numbers
repeat lawfully across voucher types within one branch - an operation could
strike another type's row. The retained statements include this form's own
ReceiptType. Subsequent containment now blocks both handlers before these
statements, because their journal lifecycle remains unresolved; these models
do not claim that saving or deletion is currently available.

Run: python3 tests/repair/voucher_contract_harness.py
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


QSRC = open("SmartAuditERP/Form_WPF/frmSandQ.xaml.cs", encoding="utf-8").read()
VSRC = open("SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs", encoding="utf-8").read()

print("Part A: cross-type collision scenarios")


def fresh():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE Receipts (GlobalID TEXT PRIMARY KEY, ReceiptNo INT,"
               " BranchID INT, ReceiptType INT, Payment REAL, ISDeleted INT)")
    # branch 1 legitimately holds receipt number 7 under three different types
    db.executemany("INSERT INTO Receipts VALUES (?,?,?,?,?,?)", [
        ("g-qd", 7, 1, 3, 500, 0),     # general receipt QD
        ("g-q",  7, 1, 5, 300, 0),     # customer receipt Q   <- this form owns type 5
        ("g-d",  7, 1, 4, 200, 0)])    # disbursement D
    return db


def cancel_voucher(db, rules, form_type, code, branch):
    where = f"ReceiptNo={code} AND BranchID={branch}"
    if rules == "fixed":
        where += f" AND ReceiptType={form_type}"
    cur = db.execute(f"UPDATE Receipts SET ISDeleted=1 WHERE {where}")
    return cur.rowcount


for rules in ("legacy", "fixed"):
    db = fresh()
    n = cancel_voucher(db, rules, form_type=5, code=7, branch=1)
    rows = sorted((r[0], r[1]) for r in db.execute(
        "SELECT ReceiptType, ISDeleted FROM Receipts"))
    if rules == "legacy":
        check("A1 legacy cancel hit EVERY type sharing the number (bug reproduced)",
              n == 3 and rows == [(3, 1), (4, 1), (5, 1)])
    else:
        check("A2 repaired cancel touches exactly its own type's row",
              n == 1 and rows == [(3, 0), (4, 0), (5, 1)])


def edit_payment(db, rules, form_type, code, branch, amount):
    where = "ReceiptNo=? AND BranchID=?" + (" AND ReceiptType=?" if rules == "fixed" else "")
    args = (code, branch, form_type) if rules == "fixed" else (code, branch)
    cur = db.execute(f"UPDATE Receipts SET Payment=? WHERE {where}", (amount,) + args)
    return cur.rowcount


db = fresh()
check("A3 legacy UPDATE rewrote all same-number vouchers' amounts (bug reproduced)",
      edit_payment(db, "legacy", 5, 7, 1, 999) == 3)
db = fresh()
check("A4 repaired UPDATE edits the single intended voucher",
      edit_payment(db, "fixed", 5, 7, 1, 999) == 1 and
      sorted(r[0] for r in db.execute("SELECT Payment FROM Receipts")) == [200.0, 500.0, 999.0])

print("Part B: identity contract and mode lifecycle model")

INSERTED_IDS = set()


def insert_receipt(rules, no, branch, form_type):
    """mirrors the upsert INSERT clause shape; returns the statement outcome."""
    cols_legacy = ["ReceiptNo", "BranchID", "ReceiptType"]          # GlobalID absent
    cols_fixed = ["GlobalID", "EntryGlobalID", "ReceiptNo", "BranchID", "ReceiptType"]
    if rules == "legacy" and "GlobalID" not in cols_legacy:
        return "CONTRACT-VIOLATION: NOT NULL PK unsupplied"         # schema verdict per DDL
    gid = "guid-%d" % len(INSERTED_IDS)
    INSERTED_IDS.add(gid)
    return "inserted:%s/entry=-1" % gid


check("B1 legacy insert cannot satisfy the NOT NULL primary-key contract (bug reproduced)",
      insert_receipt("legacy", 8, 1, 5).startswith("CONTRACT-VIOLATION"))
ok = insert_receipt("fixed", 8, 1, 5)
check("B2 repaired insert supplies a fresh identity and the no-entry sentinel",
      ok.startswith("inserted:") and "/entry=-1" in ok)
again = insert_receipt("fixed", 9, 1, 5)
check("B3 every new row gets its OWN identity (no shared/default key)",
      again != ok and again.startswith("inserted:"))


class WindowMode:
    def __init__(self, rules):
        self.rules = rules
        self.code = -1                                    # isNew while -1

    def attempt_save(self, commit_succeeds):
        no = 8
        if self.rules == "legacy":
            self.code = no                                # flips BEFORE any commit
        saved = commit_succeeds
        if self.rules == "fixed" and commit_succeeds:
            self.code = no                                # advances AFTER commit only
        return saved

    @property
    def is_new(self):
        return self.code == -1


w = WindowMode("legacy"); w.attempt_save(commit_succeeds=False)
check("B4 legacy retry after a FAILED insert takes the UPDATE path (bug reproduced)",
      w.is_new is False)
w = WindowMode("fixed"); w.attempt_save(commit_succeeds=False)
check("B5 repaired retry after failure stays a genuine CREATE",
      w.is_new is True)
w.attempt_save(commit_succeeds=True)
check("B6 successful commit promotes the window exactly once",
      w.is_new is False)

print("Part C: static witnesses over both forms")
for src, label, typeno in ((QSRC, "customer receipt Q", 5), (VSRC, "tax voucher VAT", 9)):
    ins = src.split('@"INSERT INTO Receipts')[1].split("VALUES")[0]
    upd = src.split("@ReceiptNo AND BranchID")[0][-200:] if "@ReceiptNo AND BranchID" in src else ""
    check("C1 %s INSERT now carries GlobalID and the entry sentinel" % label,
          "GlobalID" in ins and "@GlobalID" in src and 'AddWithValue("@EntryGlobalID", "-1")' in src)
    check("C2 %s generates the key via the codebase's Guid idiom" % label,
          'AddWithValue("@GlobalID", Guid.NewGuid().ToString())' in src)
    check("C3 %s UPDATE is scoped by receipt type as well" % label,
          "WHERE ReceiptNo=@ReceiptNo AND BranchID=@BranchID AND ReceiptType=@ReceiptType" in src)
    check("C4 %s cancel includes its own type constant (%d)" % (label, typeno),
          "AND ReceiptType={ReceiptType}" in src)
    check("C5 %s binds the number from the local, promoting Code only post-commit" % label,
          'AddWithValue("@ReceiptNo", receiptNo);' in src and
          "if (isNew)\n                        Code = receiptNo;" in src.replace("\r\n", "\n"))
check("C6 no pre-commit 'Code = receiptNo;' assignment survives before the transaction",
      QSRC.count("Code = receiptNo;") == 1 and VSRC.count("Code = receiptNo;") == 1 and
      "bool isNew = (Code == -1);" in QSRC and "bool isNew = (Code == -1);" in VSRC)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-036 historical SQL witnesses and independent models only.")
print("Q/VAT save and delete handlers are now blocked pending a safe ledger lifecycle;")
print("these tests do not establish that those operations currently execute.")
sys.exit(0)
