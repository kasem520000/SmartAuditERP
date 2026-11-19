#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for the bounded part of R-030 (audit finding
P2-001) in SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs. No .NET/WPF
toolchain exists here, so the permission-vs-command interaction is modelled:

* the platform permission pass disables named buttons when the grant is
  absent (mirrors MainClass.ApplyWpfPermissions);
* a disabled WPF button cannot raise its own Click, but an Enter keypress
  in the password field invokes btnSave_Click(null, null) directly;
* legacy handlers executed regardless -> saving without IS_Save through the
  keyboard route; repaired code re-verifies IsEnabled at the handler head.

Full-success behaviour (grant present) must be byte-equivalent pre/post fix.
The residual parts of P2-001 (a dedicated manage-permissions flag, export /
restore role checks) remain documented owner-input: no such column exists
in the examined User_Permissions schema to enforce against.

Run: python3 tests/repair/enforcement_boundary_harness.py
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


SRC = open("SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs", encoding="utf-8").read()

print("Part A: behavioural model of the bypass route")


class Screen:
    def __init__(self, rules):
        self.rules = rules
        self.btn_save_enabled = True
        self.db_writes = 0

    def apply_permissions(self, can_save):
        # mirror of ApplyWpfPermissions: !canSave -> btn.IsEnabled = false
        if not can_save:
            self.btn_save_enabled = False

    def user_clicks_save(self):
        # a disabled WPF Button raises no Click event at all
        if not self.btn_save_enabled:
            return
        self.save_handler(sender="button")

    def user_presses_enter_in_password(self):
        # txtPass_KeyDown -> btnSave_Click(null, null) : direct invocation
        self.save_handler(sender=None)

    def save_handler(self, sender):
        if self.rules == "fixed" and not self.btn_save_enabled:
            return                                   # R-030 guard refuses + warns
        # ...validation... then writes the Users row:
        self.db_writes += 1


for rules in ("legacy", "fixed"):
    s = Screen(rules)
    s.apply_permissions(can_save=False)              # IS_Save withheld
    s.user_presses_enter_in_password()
    if rules == "legacy":
        check("A1 legacy wrote the account via Enter despite withheld IS_Save (bug reproduced)",
              s.db_writes == 1)
    else:
        check("A2 repaired route refuses the write without the grant",
              s.db_writes == 0)

for rules in ("legacy", "fixed"):
    s = Screen(rules)
    s.apply_permissions(can_save=True)               # granted
    s.user_presses_enter_in_password()
    s.user_clicks_save()
    assert s.db_writes == 2
check_ok_legacy = Screen("legacy"); check_ok_fixed = Screen("fixed")
for s in (check_ok_legacy, check_ok_fixed):
    s.apply_permissions(can_save=True)
    s.user_presses_enter_in_password()
check("A3 granted users behave identically pre/post fix (Enter still saves once)",
      check_ok_legacy.db_writes == check_ok_fixed.db_writes == 1)

s = Screen("fixed")
s.apply_permissions(can_save=False)
s.user_clicks_save()
check("A4 clicking a disabled button remains a no-op under both rule sets",
      s.db_writes == 0)

print("Part B: static witnesses in frmAddUsers.xaml.cs")
head = SRC.split("private void btnSave_Click")[1].split("if (cmbEmp.SelectedValue == null)")[0]
check("B1 enforcement guard sits at the handler head, before any validation/write",
      "if (!btnSave.IsEnabled)" in head and
      '"\u0644\u0627 \u062a\u0645\u0644\u0643 \u0635\u0644\u0627\u062d\u064a\u0629 \u0627\u0644\u062d\u0641\u0638' in head)
key_region = SRC.split("#region Keyboard Events")[1].split("#endregion")[0]
check("B2 the Enter route still funnels into the single guarded handler",
      "btnSave_Click(null, null);" in key_region)
mainc = open("SmartAuditERP/Class/MainClass.cs", encoding="utf-8").read()
apply_body = mainc.split("ApplyWpfPermissions(DependencyObject parent")[1][:2000]
check("B3 permission pass mechanism unchanged: !canSave disables btnSave by name",
      'name == "btnSave"' in apply_body and "btn.IsEnabled = false;" in apply_body)
check("B4 guard references the control itself (survives null sender from Enter)",
      "!btnSave.IsEnabled" in SRC.split("private void btnSave_Click")[1][:800])

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-030 (bounded P2-001): the keyboard route can no longer")
print("save accounts when IS_Save is withheld; granted saves are unchanged.")
print("Residual P2-001 (manage-permissions flag, export/restore role checks)")
print("remains documented owner-input - no schema dimension exists for it yet.")
sys.exit(0)
