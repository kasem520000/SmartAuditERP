#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-016 (audit finding P1-016) in
SmartAuditERP/Home.xaml.cs.

Finding: Window_Loaded called ISSecureLogin() and DISCARDED its bool result,
so a cancelled or failed login still let the shell build connections, load
license features and start timers - an interactive business environment with
no confirmed access. The same file already contains the correct idiom on the
logout/re-login path ("if (this.ISSecureLogin()) { ...wiring... }"); the
repair applies that very contract to startup: false => application shutdown,
no wiring. (ISSecureLogin's internal cleanup of stale processes under the old
product name is tracked with P1-024 and intentionally untouched.)

No .NET/WPF toolchain exists here, so the harness models the lifecycle gate
and proves: the legacy flow wires business services even after failed login;
the repaired flow never does; success behaviour is byte-equivalent between
both; and static witnesses pin both the new guard and the untouched precedent
inside Home.xaml.cs.

Run: python3 tests/repair/startup_gate_harness.py
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


# ----------------------- Part A: lifecycle model ---------------------------
print("Part A: startup gate behaviour model")

WIRING = ["ConnObj", "SetUpLogDbConnection", "CheckLicense",
          "ApplyFeatures", "UpdateHomeStatusBar"]


class Shell:
    def __init__(self):
        self.wired = []
        self.shutdown = False

    def wire(self):
        self.wired.extend(WIRING)


def window_loaded_old(shell, is_login, secure_login_result):
    if not is_login:
        _ = secure_login_result            # result discarded (the defect)
    shell.wire()                           # proceeds unconditionally
    return shell


def window_loaded_new(shell, is_login, secure_login_result):
    if not is_login:
        if not secure_login_result:        # repair: honour the result
            shell.shutdown = True
            return shell                   # no wiring at all
    shell.wire()
    return shell


for res in (False,):                       # failed/cancelled login
    old = window_loaded_old(Shell(), False, res)
    new = window_loaded_new(Shell(), False, res)
    check("A1 legacy reproduces business wiring after FAILED login (bug)",
          old.wired == WIRING and not old.shutdown)
    check("A2 repaired flow shuts down and wires NOTHING after failed login",
          new.shutdown and new.wired == [])

for started_logged_in in (True, False):    # successful login paths
    old = window_loaded_old(Shell(), started_logged_in, True)
    new = window_loaded_new(Shell(), started_logged_in, True)
    check("A3 success wiring identical pre/post fix (started IsLogin=%s)"
          % started_logged_in,
          old.wired == new.wired == WIRING and not new.shutdown)

# ----------------------- Part B: static witnesses --------------------------
print("Part B: static witnesses in Home.xaml.cs")

src = open("SmartAuditERP/Home.xaml.cs", encoding="utf-8").read()


def method_body(name):
    i = src.index(name)
    depth = 0
    started = False
    j = i
    while j < len(src):
        c = src[j]
        if c == "{":
            depth += 1
            started = True
        elif c == "}":
            depth -= 1
            if started and depth == 0:
                return src[i:j + 1]
        j += 1
    raise AssertionError("unbalanced body for %s" % name)


loaded = method_body("private async void Window_Loaded")

check("B1 Window_Loaded now gates wiring on the login result",
      re.search(r"if\s*\(\s*!\s*this\.ISSecureLogin\(\)\s*\)\s*\{", loaded) is not None)
check("B2 failure arm shuts the application down and returns before wiring",
      re.search(r"ISSecureLogin\(\)\s*\)\s*\{\s*"
                r"System\.Windows\.Application\.Current\.Shutdown\(\);\s*"
                r"return;", loaded) is not None)
bare_call = re.search(r"^\s*this\.ISSecureLogin\(\);\s*$", loaded, re.M)
check("B3 no bare result-discarding call remains inside Window_Loaded",
      bare_call is None)
conn_pos = loaded.index("this.conn = MainClass.ConnObj();")
gate_pos = loaded.index("if (!this.ISSecureLogin())")
check("B4 the gate stands BEFORE any connection/business wiring",
      gate_pos < conn_pos)

# The pre-existing correct idiom elsewhere must be intact (repair mirrors it).
check("B5 logout/re-login precedent 'if (this.ISSecureLogin())' preserved",
      "if (this.ISSecureLogin())" in src)
# Recursive retry inside ISSecureLogin itself stays as it was (out of scope).
issl = method_body("private bool ISSecureLogin()")
check("B6 ISSecureLogin internals untouched (recursion still present)",
      "this.ISSecureLogin();" in issl)
check("B7 stale-name cleanup left for P1-024 review, not rewritten here",
      '"Auditor E-Invoicing"' in issl)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-016 (P1-016): a failed or cancelled login can no")
print("longer leave Window_Loaded wiring connections, license features and")
print("timers; the shell shuts down instead, mirroring the file's own")
print("existing gated re-login path. Success flows are unchanged.")
sys.exit(0)
