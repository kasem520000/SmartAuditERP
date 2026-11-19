#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-019 (audit finding P1-027) and
R-020 (P1-029). No .NET/SQL Server toolchain exists here, so:

Part A models the upgrade flow on SQLite exactly as Home.xaml.cs now behaves:
per-batch transactions that continue past failures, a boolean overall result,
and version registration ONLY on complete success. The legacy flow registered
unconditionally; the harness proves a partial upgrade no longer stamps the
target version (so the next launch retries), while fully successful upgrades
register identically under both rule sets.

Part B re-implements SmartAuditERP/Class/SqlBatchSplitter.cs line-for-line in
Python and exercises it against fixtures proving GO inside strings / comments /
bracketed names / unrelated words is content, real whole-line delimiters still
split (any case, optional count tolerated), nested block comments nest, and
benign scripts partition exactly as the old String.Split("GO") did whenever it
used to survive. Static witnesses pin the three call-site swaps.

Run: python3 tests/repair/db_upgrade_split_harness.py
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


# ------------------------- Part A: P1-027 -----------------------------------
print("Part A: R-019 / P1-027 - version registration follows real completion")

SCRIPTS_OK_FAIL_OK = ["CREATE TABLE t_ok(a INT)",          # succeeds
                      "CREATE TABLE t_ok(a INT)",          # duplicate => fails (same name)
                      "CREATE TABLE t_third(a INT)"]       # succeeds afterwards


def run_batches(db, scripts):
    """Per-batch transaction, continue-on-error - unchanged by the repair."""
    errors = 0
    for s in scripts:
        try:
            db.execute("BEGIN")
            db.execute(s)
            db.commit()
        except sqlite3.Error:
            db.rollback()
            errors += 1
    return errors == 0


def legacy_flow(db, scripts, required_version):
    run_batches(db, scripts)                 # result discarded
    db.execute("INSERT INTO DbVersions VALUES (?)", (required_version,))
    db.commit()


def fixed_flow(db, scripts, required_version):
    if run_batches(db, scripts):             # R-019: register ONLY when complete
        db.execute("INSERT INTO DbVersions VALUES (?)", (required_version,))
        db.commit()


def fresh():
    # isolation_level=None => autocommit; our explicit BEGIN/COMMIT then mirror
    # the C# per-batch SqlTransaction semantics without driver interference.
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE DbVersions(v REAL)")
    db.execute("INSERT INTO DbVersions VALUES (1.0)")   # old recorded version
    return db


for flow, label in ((legacy_flow, "legacy"), (fixed_flow, "fixed")):
    db = fresh()
    flow(db, SCRIPTS_OK_FAIL_OK, 2.0)
    rows = [r[0] for r in db.execute("SELECT v FROM DbVersions")]
    last = max(rows)
    if label == "legacy":
        check("A1 legacy stamped target version on a PARTIAL upgrade (bug reproduced)",
              last == 2.0 and len(rows) == 2)
    else:
        check("A2 fixed flow does NOT stamp the version after partial upgrade",
              last == 1.0 and len(rows) == 1)
        check("A3 partial schema still reads as 'needs upgrade' so repair retries",
              last < 2.0)

# Full success: identical behaviour.
db_l, db_f = fresh(), fresh()
good = ["CREATE TABLE x(a INT)", "CREATE TABLE y(a INT)"]
legacy_flow(db_l, good, 3.0)
fixed_flow(db_f, good, 3.0)
check("A4 fully successful upgrade registers identically pre/post fix",
      max(r[0] for r in db_l.execute("SELECT v FROM DbVersions")) ==
      max(r[0] for r in db_f.execute("SELECT v FROM DbVersions")) == 3.0)

# Idempotent retry after fixing the bad batch.
db = fresh()
fixed_flow(db, SCRIPTS_OK_FAIL_OK, 2.0)     # partial -> not registered
fixed_flow(db, good[:2], 2.0)               # repaired batch set -> registered
check("A5 retry after repair registers exactly once, at the right time",
      [r[0] for r in db.execute("SELECT v FROM DbVersions ORDER BY rowid")] == [1.0, 2.0])

# ------------------------- Part B: P1-029 -----------------------------------
print("Part B: R-020 / P1-029 - context-aware T-SQL batch splitting")


def is_go_line(line):
    t = line.strip(" \t")
    if len(t) < 2 or t[:2].upper() != "GO":
        return False
    rest = t[2:].strip(" \t")
    if rest == "":
        return True
    try:
        return int(rest) >= 0
    except ValueError:
        return False


def scan_state(line, st):
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        nx = line[i + 1] if i + 1 < n else "\0"
        if st["line_comment"]:
            break
        if st["block"] > 0:
            if c == "*" and nx == "/":
                st["block"] -= 1; i += 2; continue
            if c == "/" and nx == "*":
                st["block"] += 1; i += 2; continue
            i += 1; continue
        if st["sq"]:
            if c == "'":
                if nx == "'":
                    i += 2
                else:
                    st["sq"] = False; i += 1
                continue
            i += 1; continue
        if st["dq"]:
            if c == '"':
                st["dq"] = False
            i += 1; continue
        if st["br"]:
            if c == "]":
                st["br"] = False
            i += 1; continue
        if c == "-" and nx == "-":
            st["line_comment"] = True; break
        if c == "/" and nx == "*":
            st["block"] += 1; i += 2; continue
        if c == "'":
            st["sq"] = True; i += 1; continue
        if c == '"':
            st["dq"] = True; i += 1; continue
        if c == "[":
            st["br"] = True; i += 1; continue
        i += 1


def split_batches(script):
    batches, cur = [], []
    if not script or not script.strip():
        return batches
    st = dict(sq=False, dq=False, br=False, block=0, line_comment=False)
    for raw in script.split("\n"):
        line = raw[:-1] if raw.endswith("\r") else raw
        exposed = not (st["sq"] or st["dq"] or st["br"]) and st["block"] == 0
        if exposed and is_go_line(line):
            text = "".join(cur).strip("\n\r \t")
            if text:
                batches.append(text)
            cur = []
            st["line_comment"] = False
            continue
        cur.append(line + "\n")
        st["line_comment"] = False
        scan_state(line, st)
    text = "".join(cur).strip("\n\r \t")
    if text:
        batches.append(text)
    return batches


FIXTURES = [
    ("plain lowercase+uppercase GOs", "SELECT 1\nGO\nselect 2\ngo\n",
     ["SELECT 1", "select 2"]),
    ("GO inside string literal", "PRINT N'GO';\nGO\n",
     ["PRINT N'GO';"]),
    ("GO inside line comment", "--GO\nSELECT 1\nGO",
     ["--GO\nSELECT 1"]),
    ("GO inside multiline block comment", "/*\nGO\n*/\nSELECT 9\nGO",
     ["/*\nGO\n*/\nSELECT 9"]),
    ("nested block comments", "/* a /* GO */ b */\nSELECT 1\nGO",
     ["/* a /* GO */ b */\nSELECT 1"]),
    ("bracketed identifier containing GO", "SELECT [Category_GO_X] FROM t\nGO",
     ["SELECT [Category_GO_X] FROM t"]),
    ("multiline string spanning a GO line", "SELECT '\nGO\n'\nGO",
     ["SELECT '\nGO\n'"]),
    ("escaped quote keeps GO literal", "SELECT 'it''s GO'\nGO",
     ["SELECT 'it''s GO'"]),
    ("count suffix accepted once", "SELECT 1\nGO 3\n",
     ["SELECT 1"]),
    ("whitespace-padded delimiter", "SELECT 1\n   Go   \nSELECT 2",
     ["SELECT 1", "SELECT 2"]),
    ("unrelated word MANGO survives", "SELECT MANGO FROM fruit\nGO",
     ["SELECT MANGO FROM fruit"]),
    ("empty & whitespace inputs", "", []),
]
for label, text, expected in FIXTURES:
    got = split_batches(text)
    check("B fixture: %s" % label, got == expected, "%r vs %r" % (got, expected))

# Equivalence with the OLD splitter wherever the old one used to work: any
# script whose only GO occurrences are clean whole-line delimiters partitions
# identically under String.Split("GO").
benign = "ALTER TABLE A ADD X INT\nGO\nCREATE INDEX I ON A(X)\nGO\nUPDATE S SET V=1\nGO\n"
old_parts = [p.strip("\n\r \t") for p in benign.split("GO") if p.strip("\n\r \t")]
check("B benign scripts partition exactly as the legacy splitter did",
      split_batches(benign) == old_parts)

print("Part C: static witnesses - call sites swapped to the splitter")
home = open("SmartAuditERP/Home.xaml.cs", encoding="utf-8").read()
srv = open("SmartAuditERP/Form_WPF/frmServerSetting.xaml.cs", encoding="utf-8").read()
spl = open("SmartAuditERP/Class/SqlBatchSplitter.cs", encoding="utf-8").read()
check("C1 splitter class exists with public entry point",
      "public static List<string> SplitBatches(string script)" in spl)
check("C2 Home uses SplitBatches for AlterDb",
      "SqlBatchSplitter" in home and ".Split(\n                new[] { \"GO\" }" not in home)
check("C3 server settings use SplitBatches twice, naive splits gone",
      srv.count("SqlBatchSplitter") >= 2 and 'new[] { "GO" }' not in srv)
check("C4 splitter handles '' escapes and nesting (code-level)",
      "i += 2" in spl and "blockCommentDepth++" in spl)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-019 (P1-027): partial upgrades no longer register the")
print("target version (retry preserved; full-success registration unchanged).")
print("R-020 (P1-029): batches split only on real T-SQL GO delimiters; GO-like")
print("text anywhere else is content; benign scripts match the legacy output.")
sys.exit(0)
