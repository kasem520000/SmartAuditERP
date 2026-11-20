#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-046 (audit finding P4-017) and R-047
(P4-025). No .NET/WPF/SQL Server toolchain exists here, so each repair is
validated as a behavioural model of its exact control flow plus static
witnesses over the repaired windows.

R-046/P4-017: the stocktake adjustment stamped Is_Approved=1 inside the
binding step - before and independently of SaveInvoice - so a failed save
left an approved draft the window's own guard (Is_Approved=0) would refuse
to approve again. The stamp now runs only after a successful save.

R-047/P4-025: the rental invoice set ISInserted=true even after its entry
rolled back, so save() announced success, printed and cleared - and flipped
marine attendance for every non-zero MarId regardless of outcome. Both the
fall-through and the unconditional MarineExit are now gated on real success.

Run: python3 tests/repair/save_outcome_harness.py
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


ADJ = open("SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs", encoding="utf-8").read()
RENT = open("SmartAuditERP/Form_WPF/frminvoice.xaml.cs", encoding="utf-8").read()

print("Part A: R-046 / P4-017 - approval follows the committed movement")


def execute_adjustment(rules, save_ok):
    state = {"approved": False, "movement_saved": False}

    def bind():
        if rules == "legacy":
            state["approved"] = True                        # stamped inside binding!
        return "invoice"

    inv = bind()
    saved = save_ok                                         # SaveInvoice outcome
    if not saved:
        return state                                        # legacy aborts AFTER the stamp
    if rules == "fixed":
        state["approved"] = True                            # stamp after real success
    state["movement_saved"] = True
    return state


legacy = execute_adjustment("legacy", save_ok=False)
check("A1 legacy failure leaves an orphaned approved draft (bug reproduced)",
      legacy == {"approved": True, "movement_saved": False})
check("A2 repaired failure leaves a clean, re-approvable draft",
      execute_adjustment("fixed", save_ok=False) ==
      {"approved": False, "movement_saved": False})
check("A3 success approves and saves identically under both algorithms",
      execute_adjustment("legacy", True) == execute_adjustment("fixed", True) ==
      {"approved": True, "movement_saved": True})

bind_body = ADJ.split("private Invoice BindToInvoice()")[1].split("\n        private ")[0]
save_print = ADJ.split("private void SaveAndPrint()")[1].split("private Invoice BindToInvoice()")[0]
check("A4 the binding step is now pure: no approval stamp remains inside it",
      "Is_Approved=1" not in bind_body)
check("A5 the stamp sits strictly after the SaveInvoice success check",
      save_print.index('SaveInvoice(invoice, null, IsNew: true)') <
      save_print.index("Is_Approved=1"))
check("A6 the guard the stamp must respect still reads unapproved drafts",
      "AND Is_Approved=0 AND IS_Deleted=0" in ADJ)

print("Part B: R-047 / P4-025 - rentals confirm only committed invoices")


class RentalWindow:
    def __init__(self, rules):
        self.rules = rules
        self.ISInserted = False
        self.printed = False
        self.cleared = False
        self.marine_flipped = False

    def save_invoice(self, entry_ok):
        committed = False
        try:
            if entry_ok:
                committed = True                            # transaction.Commit()
            else:
                committed = False                           # Rollback + error box
                if self.rules == "fixed":
                    return                                  # the early-stop repair
            self.ISInserted = True                          # reached by committed paths only
        except Exception:
            pass
        _ = committed

    def save(self, mar_id, entry_ok):
        self.ISInserted = False
        self.save_invoice(entry_ok)
        if self.rules == "legacy":
            if mar_id != 0:
                self.marine_flipped = True                  # unconditional side effect
        else:
            if mar_id != 0 and self.ISInserted:
                self.marine_flipped = True
        if self.ISInserted:
            self.printed = True
            self.cleared = True


w = RentalWindow("legacy"); w.save(mar_id=7, entry_ok=False)
check("B1 legacy announced success, printed, cleared AND flipped marine over a rollback (bug)",
      (w.ISInserted, w.printed, w.cleared, w.marine_flipped) == (True, True, True, True))
w = RentalWindow("fixed"); w.save(mar_id=7, entry_ok=False)
check("B2 repaired failure changes nothing: no flag, no print, no attendance flip",
      (w.ISInserted, w.printed, w.cleared, w.marine_flipped) == (False, False, False, False))
w_l = RentalWindow("legacy"); w_l.save(7, True)
w_f = RentalWindow("fixed"); w_f.save(7, True)
state_of = lambda w: (w.ISInserted, w.printed, w.cleared, w.marine_flipped)
check("B3 committed rentals behave identically pre/post fix",
      state_of(w_l) == state_of(w_f) == (True, True, True, True))
w = RentalWindow("fixed"); w.save(mar_id=0, entry_ok=True)
check("B4 invoices without a marine link never touch attendance",
      w.marine_flipped is False and w.ISInserted is True)

save_fn = RENT.split("public void save()\n")[1].split("public void saveInvoice()")[0]
inv_fn = RENT.split("public void saveInvoice()")[1]
check("B5 save() gates MarineExit behind the real outcome",
      "if (this.MarId != 0 && this.ISInserted) this.MarineExit(this.MarId);" in save_fn and
      "if (this.MarId != 0) this.MarineExit(this.MarId);" not in save_fn)
first_true = inv_fn.index("this.ISInserted = true;")
check("B6 a rolled-back entry returns before the success flag can be reached",
      "return;" in inv_fn[:first_true] and
      "Repair R-047 (audit finding P4-025)" in inv_fn[:first_true])
check("B7 the two committed paths (entry saved / empty accounts) are untouched",
      inv_fn.count("transaction.Commit();") >= 2)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - approvals follow committed movements and rentals confirm")
print("only invoices that truly saved, with no stray operational side effects.")
sys.exit(0)
