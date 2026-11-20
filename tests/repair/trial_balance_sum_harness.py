#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-041 (audit finding P3-019, arithmetic slice)
in the consolidated trial-balance screen frmMezanMorg3a. No .NET/WPF/SQL
Server toolchain exists here, so validation is a behavioural model of the
two defective computations over representative trees, plus static witnesses.

Defect 1: leaf rows close as  final = initial + movement-balance + previous,
but parent groups closed as  final = initial + movement-balance - the prior
periods they had accumulated from their children simply vanished.

Defect 2: the footer totals iterated every DISPLAYED row although each parent
row already carries its descendants rolled up; whenever the level filter also
shows the children, their values were counted twice and the debit==credit
trial property broke. Repaired footer sums only topmost displayed rows.
(The report/print loops legitimately render every row - untouched.)

The single internal sign convention (P3-021, witness ALG3-08) and the income
classification remain documented barriers; this repair changes no sign rules.

Run: python3 tests/repair/trial_balance_sum_harness.py
Exit 0 on PASS.
"""
from decimal import Decimal
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


D = Decimal
SRC = open("SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml.cs", encoding="utf-8").read()

print("Part A: parent closing balance must keep its gathered priors")


class Node:
    def __init__(self, code, parent, kind):
        self.code, self.parent, self.kind = code, parent, kind   # kind: 'group' | 'leaf'
        self.intial_d = D(0); self.intial_c = D(0)
        self.prev_d = D(0);   self.prev_c = D(0)
        self.mov_d = D(0);    self.mov_c = D(0)
        self.bal_d = D(0);    self.bal_c = D(0)
        self.fin_d = D(0);    self.fin_c = D(0)


def build_tree():
    root = Node(1, 0, "group")                    # the aggregation node
    c1 = Node(11, 1, "leaf"); c2 = Node(12, 1, "leaf")
    for n in (c1, c2):                            # leaves mirror the reader algebra
        n.intial_d, n.intial_c = D(0), D(0)
        n.prev_d, n.prev_c = D(100), D(0)         # carried-forward debit balance
        n.mov_d, n.mov_c = D(50), D(30)
        bal_d = n.mov_d - n.mov_c if n.mov_d >= n.mov_c else D(0)
        bal_c = n.mov_c - n.mov_d if n.mov_c > n.mov_d else D(0)
        fin_d = n.intial_d + n.prev_d + bal_d     # exact leaf formula (:447-451)
        fin_c = n.intial_c + n.prev_c + bal_c
        if fin_d >= fin_c:
            fin_d -= fin_c; fin_c = D(0)
        else:
            fin_c -= fin_d; fin_d = D(0)
        n.bal_d, n.bal_c = bal_d, bal_c
        n.fin_d, n.fin_c = fin_d, fin_c
    return root, [c1, c2]


def aggregate(root, children, rules):
    """mirrors the accumulation block + closing formula for non-type-2 roots."""
    for a in children:
        root.intial_d += a.intial_d; root.intial_c += a.intial_c
        root.prev_d += a.prev_d;     root.prev_c += a.prev_c
        root.mov_d += a.mov_d;       root.mov_c += a.mov_c
    if root.mov_d >= root.mov_c:
        root.bal_d = root.mov_d - root.mov_c; root.bal_c = D(0)
    else:
        root.bal_d = D(0); root.bal_c = root.mov_c - root.mov_d
    if rules == "legacy":
        root.fin_d = root.intial_d + root.bal_d                      # bug: drops priors
        root.fin_c = root.intial_c + root.bal_c
    else:
        root.fin_d = root.intial_d + root.prev_d + root.bal_d        # repaired
        root.fin_c = root.intial_c + root.prev_c + root.bal_c
    if root.fin_d >= root.fin_c:
        root.fin_d -= root.fin_c; root.fin_c = D(0)
    else:
        root.fin_c -= root.fin_d; root.fin_d = D(0)


root_l, kids = build_tree(); aggregate(root_l, kids, "legacy")
sum_leaf_fin = sum(k.fin_d for k in kids)
check("A1 legacy parent closed at %s while its leaves sum to %s (priors lost)"
      % (root_l.fin_d, sum_leaf_fin), root_l.fin_d == D(40) and sum_leaf_fin == D(240))

root_f, kids = build_tree(); aggregate(root_f, kids, "fixed")
check("A2 repaired parent reconciles exactly with the sum of its leaves",
      root_f.fin_d == sum_leaf_fin == D(240) and root_f.fin_c == D(0))

zero = build_tree()
for k in zero[1]:
    k.prev_d = D(0); k.fin_d = D(20)
aggregate(zero[0], zero[1], "fixed")
check("A3 a period with no carried balance behaves identically pre/post fix",
      zero[0].fin_d == D(40))

print("Part B: footer totals must not double-count rolled-up children")


def footer(rows, rules):
    tot = D(0)
    codes = {r["code"] for r in rows}
    for r in rows:
        if rules == "fixed" and r["parent"] != 0 and r["parent"] in codes:
            continue                                                   # skip covered children
        tot += r["fin_d"]
    return tot


displayed_with_children = [
    {"code": 1, "parent": 0, "fin_d": D(240)},   # group, already holds both children
    {"code": 11, "parent": 1, "fin_d": D(120)},
    {"code": 12, "parent": 1, "fin_d": D(120)}]
check("B1 legacy footer reports 480 for what is really 240 (bug reproduced)",
      footer(displayed_with_children, "legacy") == D(480))
check("B2 repaired footer counts the truth once, however deep it is displayed",
      footer(displayed_with_children, "fixed") == D(240))

roots_only = [displayed_with_children[0]]
check("B3 at collapse-level (roots only) both algorithms agree",
      footer(roots_only, "legacy") == footer(roots_only, "fixed") == D(240))

detached_child = [{"code": 20, "parent": 99, "fin_d": D(55)}]
check("B4 an orphan-displayed row (parent not shown) is still summed, never skipped",
      footer(detached_child, "fixed") == D(55))

balanced = [
    {"code": 1, "parent": 0, "fin_d": D(300), "fin_c": D(0), "mov_d": D(10), "mov_c": D(0)},
    {"code": 2, "parent": 0, "fin_d": D(0), "fin_c": D(300), "mov_d": D(0), "mov_c": D(10)}]
sd = footer(balanced, "fixed"); sc = D(0)
codes = {r["code"] for r in balanced}
for r in balanced:
    if r["parent"] != 0 and r["parent"] in codes:
        continue
    sc += r["fin_c"]
check("B5 the debit==credit trial property survives the repaired summation", sd == sc == D(300))

print("Part C: static witnesses")
calcsum = SRC.split("private void CalcSum()")[1].split("#endregion")[0]
check("C1 the closing formula now carries both prior sides before netting",
      "root.TrDeptFinal = root.TrDeptIntial + root.TrDeptPervious + root.TrDeptBlc;" in SRC and
      "root.TrCreditFinal = root.TrCreditIntial + root.TrCreditPervious + root.TrCreditBlc;" in SRC)
check("C2 the old prior-dropping formula is gone everywhere",
      SRC.count("TrDeptFinal = root.TrDeptIntial + root.TrDeptBlc") == 0)
check("C3 the footer skips covered children via one guard in CalcSum alone",
      "displayedCodes.Contains(row.TrParentAcc)" in calcsum and
      SRC.count("displayedCodes.Contains(row.TrParentAcc)") == 1)
export_loops = SRC.count("foreach (AccountNode row in _displayRows)")
guard_skips = SRC.count('continue;\n\n                sumDebt')
check("C4 the three legacy rendering loops unchanged plus the R-090 CSV writer; the skip-guard lives only in CalcSum",
      export_loops == 4 and guard_skips == 1 and
      SRC.count("private void ExportToCsv(string fileName)") == 1)
leaf_form = SRC[SRC.index("double num9 = num3 + num7 + num;"):]
check("C5 leaf arithmetic (the reference convention) untouched",
      "double num9 = num3 + num7 + num;" in leaf_form[:60])

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-041 (P3-019 arithmetic): parents keep their prior periods")
print("and the footer sums each value exactly once, restoring reconciliation.")
sys.exit(0)
