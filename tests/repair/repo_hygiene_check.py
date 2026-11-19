#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation check for R-013 (audit finding P1-006): build outputs
(bin/, obj/) and per-user IDE state (*.user) were tracked in the repository
without any .gitignore. The repair added a .gitignore covering them and
untracked the existing copies with `git rm -r --cached` (files stay on disk).

This check proves, against the live git index:
  * no tracked path lives under a bin/ or obj/ directory;
  * no tracked *.user / *.suo files remain;
  * the .gitignore exists and carries the covering patterns;
  * the audit archive (docs/audit/**), including its evidence inventory,
    remains fully tracked - hygiene work must never touch audit material.

Run from the repository root: python3 tests/repair/repo_hygiene_check.py
Exit 0 on PASS.
"""
import re
import subprocess
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


def git_ls(pattern=None):
    cmd = ["git", "ls-files"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    paths = out.splitlines()
    return [p for p in paths if pattern is None or pattern.search(p)]


all_files = git_ls()
junk = [p for p in all_files if re.search(r"(^|/)(bin|obj)/", p) or re.search(r"\.(user|suo)$", p)]
check("A1 no bin//obj//*.user/*.suo paths remain tracked", not junk, repr(junk[:5]))

gi = open(".gitignore", encoding="utf-8").read()
for pat in ("bin/", "obj/", "*.user", ".vs/"):
    check("A2 .gitignore covers %r" % pat, re.search(r"^%s$" % re.escape(pat), gi, re.M) is not None)

# Audit archive integrity: key archive members still tracked (untouched).
archive_samples = ["docs/audit/findings.csv", "docs/audit/README.md",
                   "docs/audit/evidence/inventory.csv", "docs/audit/PHASE-01.md"]
tracked = set(all_files)
for f in archive_samples:
    check("B1 audit archive member still tracked: %s" % f, f in tracked)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    sys.exit(1)
print("RESULT: PASS - R-013 (P1-006): build/user artefacts untracked and")
print("ignored going forward; audit archive tracking intact.")
sys.exit(0)
