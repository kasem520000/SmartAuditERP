#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-081 against audit finding P7-159 (Medium,
confirmed): accepting a document from the invoice search went straight to
Navigate in both invoice editors, while every adjacent navigation command
(first/previous/next/last/new) asks first through CheckBeforeClear. An unsaved
draft was therefore replaced with no leave-decision.

R-086/R-087 extend the same boundary to the invoice-import dialog (audit finding
P7-160, and the P7-159 evidence appended in 7B30): the acceptance test used to
guard only the Navigate call, so returning from the dialog without accepting
still converted the current invoice.

No .NET/WPF toolchain exists here, so the repairs are validated as a behavioural
model of the editor's guard, its clear/bind sequence, the search-acceptance path
and the import path (legacy vs repaired), plus static witnesses over the editors
and every caller of the import dialog.

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

class ImportEditor(Editor):
    """An editor that also carries the state the import conversion tail touches."""

    def __init__(self, kind, items=0, is_new=False, is_updated=False):
        Editor.__init__(self, kind, items, is_new, is_updated)
        self.note = "fixture-note"
        self.invoice_no = 7
        self.is_printed = True
        self.effects = []
        self.rebinds = 0
        self.numbering_calls = 0

    def load_inv_no(self, fails=False):
        """The numbering helper reads MAX+1 for the branch, type and process. It reserves nothing,
        so a failure after the note was cleared is a real boundary the repair does not claim."""
        self.numbering_calls += 1
        if fails:
            return False
        self.invoice_no = 41          # the supplied candidate number of the audit's witness
        return True

    def convert_tail(self, numbering_fails=False):
        """Everything the handlers did after the acceptance test: the opened invoice becomes a
        fresh draft. The sales tail also writes inventory effects and clears two flags; the
        purchase tail does not."""
        if self.kind == "sale":
            self.effects.append("header-impact")
            self.effects.append("item-impact-type-3-or-5")
        self.note = ""
        if not self.load_inv_no(numbering_fails):
            return "numbering-failed"
        self.is_new = True
        if self.kind == "sale":
            self.is_printed = False
            self.is_updated = False
        self.rebinds += 1
        return "converted"

    def state(self):
        return (self.reference, self.note, self.invoice_no, self.is_new, self.is_printed,
                self.is_updated, tuple(self.effects), self.rebinds, tuple(self.bound),
                tuple(self.prompts))


def import_handler(ed, rules, child, answer="No", numbering_fails=False):
    """The import handler: dialog, acceptance, (repaired) the standing guard, Navigate, tail."""
    accepted = child["is_done"] and child["gid"] != "-1"
    if rules == "legacy":
        if accepted:
            ed.navigate(child["gid"])
            return ed.convert_tail(numbering_fails)
        ed.convert_tail(numbering_fails)     # the defect: the tail ran with nothing accepted
        return "converted-without-acceptance"
    if not accepted:
        return "cancelled-untouched"
    if ed.check_before_clear(answer):
        return "stayed-with-draft"
    ed.navigate(child["gid"])
    return ed.convert_tail(numbering_fails)


CANCELLED = {"is_done": False, "gid": "-1"}        # what the child publishes unless BtnImport ran
ACCEPTED = {"is_done": True, "gid": "fixture-DOC-A"}

print()
print("Part D: R-086/R-087 - the cancelled import, the accepted import and the guard between them")

leg = ImportEditor("purchase", items=0, is_new=False, is_updated=False)
check("D1 a cancelled import used to convert the current invoice anyway: note cleared, a new"
      " number published, the header marked new and the editor rebound - with no Navigate",
      import_handler(leg, "legacy", CANCELLED) == "converted-without-acceptance" and
      leg.note == "" and leg.invoice_no == 41 and leg.is_new is True and leg.rebinds == 1 and
      leg.reference == "draft-A" and leg.bound == [],
      "state=%s" % (leg.state(),))

fix = ImportEditor("purchase", items=0, is_new=False, is_updated=False)
check("D2 the repaired handler leaves a cancelled import untouched in every field",
      import_handler(fix, "fixed", CANCELLED) == "cancelled-untouched" and
      fix.state() == ImportEditor("purchase").state(),
      "state=%s" % (fix.state(),))

dirty_cancel = ImportEditor("sale", items=4, is_new=True, is_updated=False)
check("D3 a cancelled import on a dirty draft neither converts nor asks a pointless question",
      import_handler(dirty_cancel, "fixed", CANCELLED) == "cancelled-untouched" and
      dirty_cancel.prompts == [] and dirty_cancel.note == "fixture-note" and
      dirty_cancel.invoice_no == 7 and dirty_cancel.rebinds == 0)

half = ImportEditor("purchase", items=0)
check("D4 the child's own contract is the gate: is_done with the sentinel id is still a cancel",
      import_handler(half, "fixed", {"is_done": True, "gid": "-1"}) == "cancelled-untouched" and
      half.state() == ImportEditor("purchase").state())
half2 = ImportEditor("purchase", items=0)
check("D5 and an id without is_done is a cancel too, so only BtnImport can start a conversion",
      import_handler(half2, "fixed", {"is_done": False, "gid": "fixture-DOC-A"}) ==
      "cancelled-untouched" and half2.state() == ImportEditor("purchase").state())

clean = ImportEditor("purchase", items=0)
check("D6 an accepted import on a clean editor still navigates and converts, exactly as before",
      import_handler(clean, "fixed", ACCEPTED) == "converted" and
      clean.reference == "fixture-DOC-A" and clean.bound == ["fixture-DOC-A"] and
      clean.note == "" and clean.invoice_no == 41 and clean.is_new is True and
      clean.rebinds == 1 and clean.prompts == [])

dirty_no = ImportEditor("purchase", items=3, is_updated=True)
check("D7 an accepted import now meets the standing guard: 'stay' keeps the draft unconverted",
      import_handler(dirty_no, "fixed", ACCEPTED, "No") == "stayed-with-draft" and
      dirty_no.reference == "draft-A" and dirty_no.bound == [] and
      dirty_no.note == "fixture-note" and dirty_no.invoice_no == 7 and
      dirty_no.is_new is False and dirty_no.rebinds == 0 and dirty_no.prompts == ["No"])

dirty_yes = ImportEditor("purchase", items=3, is_updated=True)
check("D8 and 'leave' navigates and converts, so the accepted path keeps its whole behaviour",
      import_handler(dirty_yes, "fixed", ACCEPTED, "Yes") == "converted" and
      dirty_yes.reference == "fixture-DOC-A" and dirty_yes.prompts == ["Yes"] and
      dirty_yes.is_new is True and dirty_yes.rebinds == 1)

legacy_dirty = ImportEditor("purchase", items=3, is_updated=True)
check("D9 the accepted import used to replace a dirty draft with no question at all",
      import_handler(legacy_dirty, "legacy", ACCEPTED) == "converted" and
      legacy_dirty.prompts == [] and legacy_dirty.reference == "fixture-DOC-A")

sale = ImportEditor("sale", items=4)
import_handler(sale, "fixed", ACCEPTED)
purch = ImportEditor("purchase", items=4)
import_handler(purch, "fixed", ACCEPTED)
check("D10 the two tails differ as the source does: sales writes inventory effects and clears the"
      " printed and updated flags, purchase writes neither",
      sale.effects == ["header-impact", "item-impact-type-3-or-5"] and
      sale.is_printed is False and sale.is_updated is False and
      purch.effects == [] and purch.is_printed is True)

failed = ImportEditor("sale", items=4)
check("D11 a numbering failure stays a partial conversion: the note and the sales effects are"
      " already written, the flags and the rebind are not reached - the repair does not claim more",
      import_handler(failed, "fixed", ACCEPTED, "Yes", numbering_fails=True) == "numbering-failed" and
      failed.note == "" and failed.effects == ["header-impact", "item-impact-type-3-or-5"] and
      failed.is_new is False and failed.is_printed is True and failed.rebinds == 0 and
      failed.numbering_calls == 1)

print()
print("Part E: static witnesses over the four import callers")


def import_slice(text):
    """Only StripImportInv_Click: the editors hold many other handlers."""
    i = text.index("private void StripImportInv_Click")
    return text[i:text.index("\n        }\n", text.index("BindingControls();", i))]


pur_import = import_slice(PUR)
sal_import = import_slice(SAL)
check("E1 the purchase import gates the whole conversion, then meets the guard, then navigates",
      pur_import.count("if (!accepted) return;") == 1 and
      pur_import.count("if (this.CheckBeforeClear()) return;") == 1 and
      pur_import.index("bool accepted = frm.isDone &&") <
      pur_import.index("if (!accepted) return;") <
      pur_import.index("if (this.CheckBeforeClear()) return;") <
      pur_import.index("this.Navigate(") < pur_import.index("this.LoadInvNo();") and
      pur_import.count("Repair R-086 (audit finding P7-160)") == 1 and
      pur_import.count("Repair R-086 (audit finding P7-159") == 1 and
      pur_import.count("StringComparison.OrdinalIgnoreCase") == 1)
check("E2 the sales import does the same and keeps its longer tail",
      sal_import.count("if (!accepted) return;") == 1 and
      sal_import.count("if (CheckBeforeClear()) return;") == 1 and
      sal_import.index("if (!accepted) return;") < sal_import.index("Navigate(") <
      sal_import.index("Invoic.InvertoryImpact = InvObj.InvertoryImpact;") <
      sal_import.index("LoadInvNo();") < sal_import.index("Invoic.IsUpdated = false;") and
      sal_import.count("Repair R-086") == 2)

POS = open("SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs", encoding="utf-8").read()
TRF = open("SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs", encoding="utf-8").read()
pos_import = import_slice(POS)
trf_import = import_slice(TRF)
check("E3 the two further callers with the same shape are gated, and gain no ungrounded guard",
      pos_import.count("if (!accepted) return;") == 1 and
      pos_import.index("if (!accepted) return;") < pos_import.index("Navigate(") <
      pos_import.index("LoadInvNo();") and
      trf_import.count("if (!accepted) return;") == 1 and
      trf_import.index("if (!accepted) return;") < trf_import.index("Navigate(") <
      trf_import.index("LoadInvoiceNumber();") and
      pos_import.count("CheckBeforeClear") == 0 and trf_import.count("CheckBeforeClear") == 0 and
      pos_import.count("Repair R-087") == 1 and trf_import.count("Repair R-087") == 1)

INOUT = open("SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs", encoding="utf-8").read()
inout_import = import_slice(INOUT)
check("E4 the fifth caller already kept its tail inside the acceptance test, so it is left alone",
      inout_import.count("if (dlg.isDone && dlg.InvGID != \"-1\")") == 1 and
      "Repair R-08" not in inout_import and
      inout_import.index("if (dlg.isDone") < inout_import.index("LoadInvNo();"))

CHILD = open("SmartAuditERP/Form_WPF/frmImportInvoice.xaml.cs", encoding="utf-8").read()
check("E5 the child's published contract is untouched and still starts as a cancellation",
      CHILD.count("public string InvGID = \"-1\";") == 1 and
      CHILD.count("public bool isDone = false;") == 1 and
      CHILD.count("isDone = true;") == 1 and
      CHILD.index("InvGID = globalId;") < CHILD.index("isDone = true;") < CHILD.index("this.Close();") and
      CHILD.count("OnClosing") == 0 and CHILD.count("DialogResult") == 0 and
      "Repair R-08" not in CHILD)

import glob
def raw(path):
    """Byte search: a few sources in this repository are not valid UTF-8."""
    return open(path, "rb").read()


callers = [f for f in glob.glob("SmartAuditERP/**/*.cs", recursive=True)
           if b"new frmImportInvoice()" in raw(f)]
check("E6 the scope bound is exact: five callers, four gated by R-086/R-087, one already correct",
      len(callers) == 5 and
      sum(1 for f in callers if b"Repair R-086" in raw(f)) == 2 and
      sum(1 for f in callers if b"Repair R-087" in raw(f)) == 2,
      "callers=%s" % sorted(callers))

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - an accepted search or import now meets the standing unsaved-draft guard,")
print("a cancelled import leaves the current invoice untouched, and clean, cancelled and refused")
print("paths behave exactly as before.")
sys.exit(0)
