#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-037 (audit finding P3-025) and R-038
(P3-022). No .NET/WPF/SQL Server toolchain exists here, so each repair is
validated as a behavioural model of its exact contract plus static
witnesses over the repaired code.

R-037 / P3-025: the credit-note and debit-note editors bound @Date on edit
but never assigned it to the header's Date column, while rebuilding the
journal entry from the newly chosen date - head and ledger could diverge
across periods. The fix persists Date on the header (as insert always did).

R-038 / P3-022: the account-statement consumer read row["subNotes"] for
every movement although only the detailed projection returns that column;
each aggregate row threw before reaching the grid. A single Columns guard
now makes aggregate rows fall back to the header note - the value the
fallback already preferred.

Run: python3 tests/repair/report_contract_harness.py
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


CREDIT = open("SmartAuditERP/Form_WPF/frmCreditNote.xaml.cs", encoding="utf-8").read()
DEBIT = open("SmartAuditERP/Form_WPF/frmDebtNote.xaml.cs", encoding="utf-8").read()
STMT = open("SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs", encoding="utf-8").read()
NOTE_WRITER = open("SmartAuditERP/Class/ReceiptOper.cs", encoding="utf-8").read()

print("Part A: R-037 / P3-025 - header date follows the edited entry date")


def edit_note(rules, doc_no, doc_type, header_date_stored, chosen_date, period_of):
    """doc row: {Doc_No, Doc_Type, Date}; journal rebuilt from chosen_date."""
    rows = {(doc_no, doc_type): dict(Date=header_date_stored)}
    set_clause = ["Inv_No=@", "Discount=@", "Net=@", "Edit_Date=@", "emp_id=@",
                  "notes=@", "cust_id=@", "Inv_Val=@"]
    if rules == "fixed":
        set_clause.insert(3, "Date=@Date")                     # the repair
    applied = [c.split("=")[0] for c in set_clause]
    values = {"Inv_No": None, "Discount": None, "Net": None, "Date": chosen_date,
              "Edit_Date": None, "emp_id": None, "notes": None, "cust_id": None, "Inv_Val": None}
    r = rows[(doc_no, doc_type)]
    for col in applied:
        if col in r:
            r[col] = values[col]
    rebuilt_entry = dict(Date=chosen_date, Type=("CreditNote" if doc_type == 1 else "DebitNote"))
    aligned = period_of(r["Date"]) == period_of(rebuilt_entry["Date"])
    return r["Date"], rebuilt_entry["Date"], aligned


for label, typ in (("credit note", 1), ("debt note", 2)):
    h, e, old_ok = edit_note("legacy", 12, typ, "2026-10-04", "2026-11-19", lambda d: d[:7])
    _, _, new_ok = edit_note("fixed", 12, typ, "2026-10-04", "2026-11-19", lambda d: d[:7])
    check("A1 %s: legacy edit left the header a month behind its entry (bug)" % label,
          h == "2026-10-04" and e == "2026-11-19" and not old_ok)
    check("A2 %s: repaired edit keeps header and entry in one period" % label, new_ok)

check("A3 shared note UPDATE assigns its date parameter",
      "UPDATE CreditDeptNotes SET Inv_No=@invoice,Discount=@discount,Net=@net,Date=@date" in NOTE_WRITER)
check("A4 both editors send their chosen date and journal to the shared writer",
      "Date = txtDate.SelectedDate.Value" in CREDIT and "Date = txtDate.DateTime" in DEBIT and
      all("SaveCreditDebtNote(draft)" in x and "Journal = entry" in x for x in (CREDIT, DEBIT)))
check("A5 update requires the selected identity, branch, number and type",
      "WHERE Id=@id AND BranchId=@branch AND Doc_No=@number AND Doc_Type=@type AND IS_Deleted=0" in NOTE_WRITER)
check("A6 insert stores the chosen date and explicit branch",
      "IS_Deleted,Edit_Date,emp_id,notes,cust_id,Inv_Val,BranchId) VALUES" in NOTE_WRITER and
      "@number,@type,@invoice,@discount,@net,@date,0,@editDate,@user,@notes,@customer,@invVal,@branch" in NOTE_WRITER)

print("Part B: R-038 / P3-022 - the two statement projections are honoured")

HEADER_ROW_DETAILED = dict(dept=10.0, credit=0.0, subNotes="فرعي: تحصيل فاتورة",
                           notes="رأس: مستند 88")
HEADER_ROW_AGGREGATE = dict(dept=40.0, credit=0.0, notes="رأس: تجميع يومي")


def read_notes(row, rules):
    """consumer reads like DataTable indexing: missing column raises."""
    if rules == "legacy":
        try:
            return row["subNotes"] if row["subNotes"] != "<<null>>" else row["notes"]
        except KeyError:
            raise                                              # what the UI hit per row
    has_sub_notes = "subNotes" in row                          # Columns.Contains equivalent
    if has_sub_notes and row.get("subNotes", "<<null>>") != "<<null>>":
        return row["subNotes"]
    return row["notes"]


detailed_ok = False
try:
    n = read_notes(dict(HEADER_ROW_DETAILED), "legacy")
    detailed_ok = (n == HEADER_ROW_DETAILED["subNotes"])
except KeyError:
    pass
agg_crashed = False
try:
    read_notes(dict(HEADER_ROW_AGGREGATE), "legacy")
except KeyError:
    agg_crashed = True
check("B1 legacy consumer passed detailed rows (sub-line note wins)", detailed_ok)
check("B2 legacy consumer crashed on EVERY aggregate row (bug reproduced)", agg_crashed)

check("B3 repaired detailed mode still prefers the sub-line note",
      read_notes(dict(HEADER_ROW_DETAILED), "fixed") == HEADER_ROW_DETAILED["subNotes"])
check("B4 repaired aggregate mode falls back to the header note without error",
      read_notes(dict(HEADER_ROW_AGGREGATE), "fixed") == HEADER_ROW_AGGREGATE["notes"])
nullsub = dict(dept=5.0, credit=5.0, subNotes="<<null>>", notes="رأس فقط")
check("B5 NULL sub-line notes in detailed mode also fall back to the header",
      read_notes(nullsub, "fixed") == "رأس فقط")

check("B6 the projection shapes themselves are unchanged (aggregate omits, detailed carries)",
      'selectFields = "SUM(Entry_sub.dept) as dept, SUM(Entry_sub.credit) as credit"' in STMT and
      "GROUP BY Entry.GlobalID, Entry.date, Entry.notes, Entry.doc_no, Entry.type, Entry_sub.branch" in STMT and
      "Entry_sub.notes as subNotes" in STMT)
import re
code_only = "\n".join(l for l in STMT.splitlines() if not l.strip().startswith("//"))
check("B7 a single guard governs the single remaining read site",
      code_only.count('row["subNotes"]') == 2 and        # guard test + ToString of one ternary
      "hasSubNotes = dtMovements.Columns.Contains" in code_only and
      "(hasSubNotes && row[\"subNotes\"] != DBNull.Value)" in code_only)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-037 (P3-025): note headers follow their edited dates;")
print("R-038 (P3-022): aggregate/detailed projections are each consumed safely.")
sys.exit(0)
