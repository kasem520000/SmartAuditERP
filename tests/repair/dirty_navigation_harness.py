#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-081 against audit finding P7-159 (Medium,
confirmed): accepting a document from the invoice search went straight to
Navigate in both invoice editors, while every adjacent navigation command
(first/previous/next/last/new) asks first through CheckBeforeClear. An unsaved
draft was therefore replaced with no leave-decision.

No .NET/WPF toolchain exists here, so the repair is validated as a behavioural
model of the editor's guard, its clear/bind sequence and the search-acceptance
path (legacy vs repaired), plus static witnesses over both editors.

Run: python3 tests/repair/dirty_navigation_harness.py
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


PUR = open("SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs", encoding="utf-8").read()
SAL = open("SmartAuditERP/Form_WPF/frmInvSale.xaml.cs", encoding="utf-8").read()

print("Part A: the editor model - guard, clear, bind")


class Editor:
    """One invoice editor: a draft reference, the standing guard, and Navigate."""

    def __init__(self, kind, items=0, is_new=False, is_updated=False):
        self.kind = kind                      # "purchase" or "sale"
        self.reference = "draft-A"
        self.items = items
        self.is_new = is_new
        self.is_updated = is_updated
        self.prompts = []
        self.bound = []

    def dirty(self):
        if self.kind == "purchase":
            return (self.items > 0 and self.is_new) or self.is_updated
        return (self.items > 1 and self.is_new) or self.is_updated

    def check_before_clear(self, answer):
        """Returns True when the user chose to stay with the draft (the source's meaning)."""
        if not self.dirty():
            return False
        self.prompts.append(answer)
        return answer == "No"

    def navigate(self, target):
        self.reference = None                 # CLR drops the current reference first
        self.items = 0
        self.bound.append(target)             # then BindingInvoice reads the target
        self.reference = target


def search_accept(ed, rules, pick, answer="No"):
    """The search-acceptance path: refusals first, then (repaired) the guard, then Navigate."""
    if pick is None or pick["id"] == "-1":
        return "closed"
    if rules == "fixed" and not pick["snapshot_valid"]:
        return "refused-invalid-source"
    if rules == "fixed" and pick["source_type"] not in (0, pick["requested_type"]):
        return "refused-out-of-type"
    if rules == "fixed" and ed.check_before_clear(answer):
        return "stayed-with-draft"
    ed.navigate(pick["id"])
    return "navigated"


TARGET = {"id": "target-B", "snapshot_valid": True, "source_type": 1, "requested_type": 1}

leg = Editor("purchase", items=3, is_new=False, is_updated=True)
fix_no = Editor("purchase", items=3, is_new=False, is_updated=True)
fix_yes = Editor("purchase", items=3, is_new=False, is_updated=True)
check("A1 a dirty draft: the accepted search used to replace it with no question at all",
      search_accept(leg, "legacy", TARGET) == "navigated" and leg.prompts == [] and
      leg.reference == "target-B" and leg.bound == ["target-B"])
check("A2 the repaired path asks first, and 'stay' keeps the draft as the editor's reference",
      search_accept(fix_no, "fixed", TARGET, "No") == "stayed-with-draft" and
      fix_no.prompts == ["No"] and fix_no.reference == "draft-A" and fix_no.bound == [])
check("A3 and 'leave' navigates exactly as the adjacent navigation commands do",
      search_accept(fix_yes, "fixed", TARGET, "Yes") == "navigated" and
      fix_yes.prompts == ["Yes"] and fix_yes.reference == "target-B")

clean = Editor("purchase", items=0, is_new=False, is_updated=False)
check("A4 a clean editor is unchanged: no question, straight to the target",
      search_accept(clean, "fixed", TARGET) == "navigated" and clean.prompts == [] and
      clean.reference == "target-B")
new_draft = Editor("purchase", items=2, is_new=True, is_updated=False)
check("A5 an unsaved NEW invoice with rows is guarded too, on the guard's own condition",
      search_accept(new_draft, "fixed", TARGET, "No") == "stayed-with-draft" and
      new_draft.reference == "draft-A")
sale = Editor("sale", items=2, is_new=True, is_updated=False)
check("A6 the sales editor guards on its own condition (more than one grid row, and new)",
      sale.dirty() is True and search_accept(sale, "fixed", TARGET, "No") == "stayed-with-draft" and
      Editor("sale", items=1, is_new=True).dirty() is False)

print()
print("Part B: order and the paths that must not prompt")

invalid = dict(TARGET, snapshot_valid=False)
out_of_type = dict(TARGET, source_type=20)
dirty = Editor("purchase", items=3, is_updated=True)
check("B1 a pick from a failed search is refused before the guard, so no pointless question",
      search_accept(dirty, "fixed", invalid, "No") == "refused-invalid-source" and
      dirty.prompts == [] and dirty.reference == "draft-A")
dirty2 = Editor("purchase", items=3, is_updated=True)
check("B2 an out-of-type pick is refused before the guard as well",
      search_accept(dirty2, "fixed", out_of_type, "No") == "refused-out-of-type" and
      dirty2.prompts == [] and dirty2.reference == "draft-A")
cancelled = Editor("purchase", items=3, is_updated=True)
check("B3 closing the search without a pick neither navigates nor prompts",
      search_accept(cancelled, "fixed", None) == "closed" and
      search_accept(cancelled, "fixed", {"id": "-1", "snapshot_valid": True,
                                         "source_type": 1, "requested_type": 1}) == "closed" and
      cancelled.prompts == [] and cancelled.reference == "draft-A")
check("B4 the guard is the standing one: it asks only when the draft is dirty, and No blocks",
      Editor("purchase", items=0).check_before_clear("No") is False and
      Editor("purchase", items=0, is_updated=True).check_before_clear("No") is True and
      Editor("purchase", items=0, is_updated=True).check_before_clear("Yes") is False)

print()
print("Part C: static witnesses over both editors")

def method_slice(text, start_marker, end_marker):
    """Only the handler itself: other search consumers live in the same files."""
    i = text.index(start_marker)
    return text[i:text.index(end_marker, i)]


pur_handler = method_slice(PUR, "private void btnInvSrch_Click_1", "\n        #endregion")
sal_handler = method_slice(SAL, "private void btnInvSrch_Click", "private void btnRepaid_Click")
check("C1 the purchase acceptance routes through the same guard, immediately before Navigate",
      pur_handler.count("if (this.CheckBeforeClear()) return;") == 1 and
      pur_handler.index("if (this.CheckBeforeClear()) return;") < pur_handler.index("this.Navigate(") and
      "Repair R-081 (audit finding P7-159)" in pur_handler)
check("C2 the sales acceptance does the same, and keeps its single Navigate call",
      sal_handler.count("if (CheckBeforeClear()) return;") == 1 and
      sal_handler.index("if (CheckBeforeClear()) return;") < sal_handler.index("Navigate(\"select * from Inv where branch=\"") and
      sal_handler.count("Navigate(\"select * from Inv where branch=\"") == 1 and
      "Repair R-081 (audit finding P7-159)" in sal_handler)
check("C3 the guard itself and the adjacent commands are untouched in both editors",
      PUR.count("if (!this.CheckBeforeClear())") == 5 and SAL.count("if (!CheckBeforeClear())") == 5 and
      PUR.count("private bool CheckBeforeClear()") == 1 and SAL.count("private bool CheckBeforeClear()") == 1 and
      PUR.count("this.Invoic.IsUpdated") >= 1 and SAL.count("Invoic.IsUpdated") >= 1)
check("C4 the refusals repaired earlier still precede the new guard in the purchase editor",
      pur_handler.index("if (!frm.SnapshotValid)") < pur_handler.index("if (frm.SelectedInvType > 0")
      < pur_handler.index("if (this.CheckBeforeClear()) return;") < pur_handler.index("this.Navigate("))
check("C5 the acceptance conditions and the lookup query are unchanged",
      pur_handler.count("if (frm.ISDone &&") == 1 and sal_handler.count("if (frm.ISDone &&") == 1 and
      pur_handler.count("$\"and InvGlobalID=N'{frm.InvGlobalID}'\");") == 1 and
      sal_handler.count("\" and InvGlobalID=N'\" + frm.InvGlobalID + \"'\");") == 1)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - an accepted search now meets the standing unsaved-draft guard in both")
print("editors, while clean, cancelled and refused paths behave exactly as before.")
sys.exit(0)
