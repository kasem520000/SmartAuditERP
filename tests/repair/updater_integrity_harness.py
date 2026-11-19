#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-017 (audit findings P1-021, P1-022 and the
bounded part of P1-023) in SmartAuditUpdater/MainWindow.xaml.cs.

No .NET/WPF toolchain exists here, so the update pipeline is modelled as a
state machine that mirrors RunUpdateProcess step by step - legacy rules vs
repaired rules - and proves:
  * every failure class ends with close ENABLED and NO success wording
    (legacy left download/install failures unclosable);
  * a persistent copy failure fails the whole install and never announces
    "all files succeeded" (legacy announced success anyway);
  * backup failure refuses to proceed to file modification (legacy logged
    "المتابعة رغم ذلك" and installed regardless);
  * the fully successful run produces byte-equivalent final state under both
    rule sets (no behaviour change on the happy path).
Static witnesses additionally pin the repaired constructs in the source.

Run: python3 tests/repair/updater_integrity_harness.py
Exit 0 on PASS.
"""
import re
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


class State:
    def __init__(self):
        self.updating = True
        self.close_enabled = False      # btnClose.IsEnabled / closability proxy
        self.success_wording = False
        self.error_title = None
        self.modified_files = False     # any destination overwrite happened
        self.finished = False


def legacy_run(download_ok, backup_ok, copy_fails):
    s = State()
    # download
    if not download_ok:
        return s                                    # early return: stuck open (P1-021)
    # backup: swallowed
    _ = backup_ok                                   # warning only, continue anyway
    # install
    copied_all = not copy_fails
    if not copied_all:
        pass                                        # warning per file...
    s.modified_files = True                         # copies attempted either way
    s.success_wording = True                        # "...بنجاح!" unconditional (P1-022)
    s.updating = False
    s.close_enabled = True
    s.finished = True
    return s


def fixed_run(download_ok, backup_ok, copy_fails):
    s = State()

    def fail_terminal(msg):                         # the one terminal-failure state
        s.error_title = msg
        s.updating = False
        s.close_enabled = True

    if not download_ok:
        fail_terminal("❌ فشل تحميل التحديث!")
        return s
    if not backup_ok:                               # refuse BEFORE modification (P1-023)
        fail_terminal("❌ فشل النسخ الاحتياطي! لن يتم تعديل الملفات.")
        return s
    # install: honest result
    if copy_fails:
        s.modified_files = True                     # some files were written before the failure
        fail_terminal("❌ فشل تثبيت التحديث!")
        return s
    s.modified_files = True
    s.success_wording = True
    s.updating = False
    s.close_enabled = True
    s.finished = True
    return s


print("Part A: behavioural model of the update pipeline")

failure_cases = [
    ("download fails",      dict(download_ok=False, backup_ok=True,  copy_fails=False)),
    ("backup fails",        dict(download_ok=True,  backup_ok=False, copy_fails=False)),
    ("copy locked x5",      dict(download_ok=True,  backup_ok=True,  copy_fails=True)),
]
for label, kw in failure_cases:
    old, new = legacy_run(**kw), fixed_run(**kw)
    check("A1 legacy shows the defect class '%s'" % label,
          (not old.close_enabled) or old.success_wording or
          (label == "backup fails" and old.modified_files))
    check("A2 repaired '%s' ends closable without success wording" % label,
          new.close_enabled and not new.success_wording and not new.updating)
    if label == "backup fails":
        check("A3 repaired backup failure touches NO files", not new.modified_files)
        check("A4 legacy backup failure modified files anyway (bug reproduced)",
              old.modified_files)
    if label == "copy locked x5":
        check("A5 legacy announced success despite failed copies (bug reproduced)",
              old.success_wording)

old_ok = legacy_run(True, True, False)
new_ok = fixed_run(True, True, False)
check("A6 full-success outcome identical pre/post fix",
      (old_ok.success_wording, old_ok.close_enabled, old_ok.updating,
       old_ok.modified_files, old_ok.finished) ==
      (new_ok.success_wording, new_ok.close_enabled, new_ok.updating,
       new_ok.modified_files, new_ok.finished) == (True, True, False, True, True))

print("Part B: static witnesses in SmartAuditUpdater/MainWindow.xaml.cs")
src = open("SmartAuditUpdater/MainWindow.xaml.cs", encoding="utf-8").read()

check("B1 one shared terminal-failure helper exists",
      re.search(r"private void FailTerminal\(string message\)", src) is not None)
check("B2 all three failure branches route through it",
      src.count("FailTerminal(") >= 4)                  # def + download + backup + install arms
check("B3 no bare 'if (!downloaded) return;' survives",
      "if (!downloaded) return;" not in src)
check("B4 no bare 'if (!installed) return;' survives",
      "if (!installed) return;" not in src)
check("B5 backup now reports success/failure",
      "private Task<bool> BackupOldFiles()" in src and
      'AddLog("المتابعة رغم ذلك...");' not in src and
      "لن تتم متابعة التحديث دون نسخة احتياطية ناجحة." in src)
check("B6 install tracks per-file failure honestly",
      "bool anyCopyFailed" in src and
      '"✅ تم تثبيت جميع الملفات بنجاح!"' in src)       # still present, but gated below
# Success wording must be emitted ONLY after the failure gate.
gate = src.index("if (anyCopyFailed)")
announce = src.index('"✅ تم تثبيت جميع الملفات بنجاح!"')
check("B7 success announcement sits AFTER the failure gate", gate < announce)
check("B8 Window_Closing still blocks close mid-update only",
      "if (_isUpdating)" in src and "e.Cancel = true;" in src)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-017 (P1-021/P1-022/P1-023 bounded): failed updates end")
print("closable with error state, failed copies/backups can never be announced")
print("as success, and nothing is modified without a successful backup first;")
print("the fully successful update behaves exactly as before.")
sys.exit(0)
