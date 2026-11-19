#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-025 (audit finding P2-015) and
R-026 (P2-002). No .NET/WPF toolchain exists here, so both repairs are
validated as behavioural mini-models of their exact lifecycle rules plus
static witnesses pinned in the sources.

Part A models support-ticket attachment lifetime across windows, the Clear
button and successful submit: the legacy 'public static' list re-sent the
previous ticket's images; per-instance storage plus a clear on every reset
route makes stale bytes unsendable without a fresh explicit selection.

Part B models the lock session contract: which dialog outcomes may release
the business shell. Legacy treated any ShowDialog return (and even an
exception while showing the lock) as unlocked; repaired code releases ONLY
on a verified unlock flag and otherwise terminates the session, with a
closing guard that blocks dismissal while unauthenticated.

Run: python3 tests/repair/session_privacy_harness.py
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


# ------------------------- Part A: P2-015 -----------------------------------
print("Part A: R-025 / P2-015 - attachments belong to one draft only")


class DraftLegacy:
    shared = None                       # public static string[] filePathDocument

    def select(self, files):
        DraftLegacy.shared = files      # assignment leaks to every window

    def clear_form(self):               # legacy ClearForm never touched the list
        pass

    def submit_payload(self):
        return list(DraftLegacy.shared or [])


class DraftFixed:
    def __init__(self):
        self.files = None               # instance field

    def select(self, files):
        self.files = files

    def clear_form(self):               # Clear + success both funnel through here
        self.files = None

    def submit_payload(self):
        out = list(self.files or [])
        return out


# Legacy defect reproduction: window B re-sends window A's images.
a = DraftLegacy(); a.select(["a1.jpg", "a2.png"])
b = DraftLegacy()                        # brand-new window, user picks nothing
check("A1 legacy new window inherits previous ticket's attachments (bug reproduced)",
      b.submit_payload() == ["a1.jpg", "a2.png"])
b.clear_form()                           # pressing Clear changes nothing about files
check("A2 legacy Clear leaves stale attachments selected",
      b.submit_payload() == ["a1.jpg", "a2.png"])

# Repaired semantics.
fa = DraftFixed(); fa.select(["a1.jpg", "a2.png"])
check("A3 fixed draft sends exactly its own selection",
      fa.submit_payload() == ["a1.jpg", "a2.png"])
fb = DraftFixed()
check("A4 fixed second window starts with NO attachments", fb.submit_payload() == [])
fa.clear_form()                          # Clear button route
check("A5 fixed Clear drops attachments", fa.submit_payload() == [])
fc = DraftFixed(); fc.select(["x.png"]); fc.clear_form()   # post-success route
fd = DraftFixed()
check("A6 fixed later ticket after success carries nothing stale",
      fd.submit_payload() == [] and fc.submit_payload() == [])

src_ticket = open("SmartAuditERP/Form_WPF/FormCreateTicket.xaml.cs", encoding="utf-8").read()
import pathlib
all_cs = [p.read_text(encoding="utf-8", errors="replace")
          for p in pathlib.Path("SmartAuditERP").rglob("*.cs")]
external_refs = sum(s.count("FormCreateTicket.filePathDocument") for s in all_cs)
check("A7 field is now instance-private (no 'static')",
      "private string[] filePathDocument;" in src_ticket and
      "public static string[] filePathDocument;" not in src_ticket)
check("A8 ClearForm nulls the attachments",
      "filePathDocument = null;" in src_ticket)
check("A9 no external code referenced the field (visibility change safe)",
      external_refs == 0)

# ------------------------- Part B: P2-002 -----------------------------------
print("Part B: R-026 / P2-002 - only verified unlocks release the business shell")

UNLOCKED = "business-shell-running"
SHUTDOWN = "session-ended"


def closing_attempt_blocks(iscorrect, is_close, rules):
    if rules == "fixed":
        return not iscorrect and not is_close     # OnClosing cancels
    return False                                  # legacy: dialog dismissible anytime


def lock_session(rules, events):
    """events: ordered outcomes observed around the modal lock dialog."""
    iscorrect = False
    is_close = False
    shown = True
    for ev in events:
        if ev == "check-ok":
            iscorrect = True                      # Check(): rows match => Iscorrect=true
        elif ev == "advanced-ok":
            if rules == "fixed":
                iscorrect = True                  # gated on SuccessLogin then Close()
            else:
                pass                              # legacy hid the dialog regardless
        elif ev == "advanced-fail-or-cancel":
            pass                                  # fixed: stays open & topmost; legacy hid it
        elif ev == "close-attempt":
            if closing_attempt_blocks(iscorrect, is_close, rules):
                continue                          # dismissal refused while unproven
            shown = False                         # dialog removed from view
        elif ev == "programmatic-close":
            is_close = True
            shown = False
        elif ev == "display-exception":
            if rules == "legacy":
                pass                              # empty catch => fall through unlocked
            else:
                return SHUTDOWN                   # failure must end the session
    if not shown or not iscorrect:
        # host side: ShowDialog returned / exception path
        if rules == "fixed":
            return UNLOCKED if iscorrect else SHUTDOWN
        return UNLOCKED                            # legacy ignored Iscorrect entirely
    return UNLOCKED


scenarios = [
    # failed password attempts leave Iscorrect false; under legacy rules a bare
    # dismissal attempt then released the shell because nothing refused it and
    # the return value was ignored.
    ("wrong password then X close",      ["close-attempt"]),
    ("advanced login cancelled",         ["advanced-fail-or-cancel", "close-attempt"]),
    ("exception while displaying lock",  ["display-exception"]),
]
for label, evs in scenarios:
    old = lock_session("legacy", list(evs))
    new = lock_session("fixed", list(evs))
    check("B1 legacy released the shell for '%s' (bug reproduced)" % label,
          old == UNLOCKED)
    check("B2 repaired ends the session for '%s'" % label, new == SHUTDOWN)

ok_evs = ["check-ok"]
check("B3 successful unlock behaves identically pre/post fix",
      lock_session("legacy", list(ok_evs)) == lock_session("fixed", list(ok_evs)) == UNLOCKED)
adv_ok = ["advanced-ok"]
check("B4 advanced SUCCESS releases under fixed rules via SuccessLogin gate",
      lock_session("fixed", list(adv_ok)) == UNLOCKED)
check("B5 closing guard refuses dismissal while unproven but honours is_close",
      closing_attempt_blocks(False, False, "fixed") and
      not closing_attempt_blocks(True, False, "fixed") and
      not closing_attempt_blocks(False, True, "fixed"))
check("B6 programmatic escape hatch (is_close) still ends the dialog",
      lock_session("fixed", ["programmatic-close"]) == SHUTDOWN)

home = open("SmartAuditERP/Home.xaml.cs", encoding="utf-8").read()
lock = open("SmartAuditERP/Form_WPF/frmlock.xaml.cs", encoding="utf-8").read()
check("B7 Home reads Iscorrect after ShowDialog",
      "unlocked = frmLock.Iscorrect;" in home)
check("B8 Home shuts down on anything but a verified unlock",
      "if (!unlocked)\n                Application.Current.Shutdown();" in home)
check("B9 the swallowing empty catch around the lock is gone",
      "frmLock.ShowDialog();\n            }\n            catch { }" not in home)
check("B10 lock window cancels closing while unauthenticated",
      "if (!Iscorrect && !is_close)\n                e.Cancel = true;" in lock)
check("B11 advanced login closes ONLY on the dialog's SuccessLogin flag",
      "if (frmUserLogin.SuccessLogin)" in lock and
      "Hide();" not in lock.split("#region Advanced Login")[1].split("#endregion")[0])
check("B12 unlock success path still sets Iscorrect before Close()",
      "Iscorrect = true;\n                    Close();" in lock)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-025 (P2-015): attachments cannot survive Clear/success/")
print("new windows; R-026 (P2-002): the business shell survives a lock dialog")
print("ONLY when authentication verifiably succeeded, every other return ends")
print("the session, and the lock cannot be dismissed while identity is unproven.")
sys.exit(0)
