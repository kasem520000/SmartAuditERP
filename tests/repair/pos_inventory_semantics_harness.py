#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-042 (P4-001), R-043 (P4-002), R-044 (P4-005)
and R-045 (P4-024). No .NET/WPF/SQL Server toolchain exists here, so each
repair is validated as a behavioural model of its exact control flow plus
static witnesses over the repaired code.

R-042/P4-001: POS InsertFromInv hardcoded stock-OUT impact even for linked
returns; the impact now derives from ProcType per the frmInvSale convention.
R-043/P4-002: held baskets kept their sale impact; every line is zeroed on
hold, mirroring the quotation flow.
R-044/P4-005: invoice profit accumulated prefix margins per iteration; all
three calc sites derive it once from final totals - order independent.
R-045/P4-024: the delivery writer swallowed failures and windows announced
success regardless; it now reports the real commit outcome and callers gate
confirmation on it.

Run: python3 tests/repair/pos_inventory_semantics_harness.py
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


POS = open("SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs", encoding="utf-8").read()
SALE = open("SmartAuditERP/Form_WPF/frmInvSale.xaml.cs", encoding="utf-8").read()
ITEMOP = open("SmartAuditERP/Class/ItemOper.cs", encoding="utf-8").read()
CONTRACT = open("SmartAuditERP/Class/ItemOpercontract.cs", encoding="utf-8").read()
PARTIAL = open("SmartAuditERP/Form_WPF/frmInvItemsDeliveries.xaml.cs", encoding="utf-8").read()
TOTAL = open("SmartAuditERP/Form_WPF/frmInvoiceDeliveries.xaml.cs", encoding="utf-8").read()

print("Part A: R-042 / P4-001 - return lines re-enter stock")


def insert_from_inv(rules, proc_type, qty):
    """mirrors POS InsertFromInv: head impact derived, then propagated to lines."""
    if rules == "legacy":
        impact = 2                                            # hardcoded OUT
    else:
        impact = 1 if proc_type == 2 else 2                   # type-derived
    lines = [{"impact": impact} for _ in range(1)]
    return lines


def stock_delta(lines, qty):
    """CalcItemStock semantics: impact 1 = IN (+), impact 2 = OUT (-)."""
    return sum(qty if l["impact"] == 1 else -qty for l in lines)


check("A1 legacy linked return removed stock instead of restoring it (bug)",
      stock_delta(insert_from_inv("legacy", proc_type=2, qty=1), 1) == -1)
check("A2 repaired linked return restores stock (+1 per unit)",
      stock_delta(insert_from_inv("fixed", proc_type=2, qty=1), 1) == +1)
check("A3 genuine sales keep stock-OUT behaviour pre/post fix",
      stock_delta(insert_from_inv("legacy", 1, 3), 3) == -3 and
      stock_delta(insert_from_inv("fixed", 1, 3), 3) == -3)
ins = POS.split("private void InsertFromInv(int sourceType)")[1].split("#endregion")[0]
check("A4 POS derives the impact from ProcType with the documented convention",
      "Invoic.InvertoryImpact = (ProcType == 2) ? 1 : 2;" in ins and
      "it.InvertoryImpact = Invoic.InvertoryImpact;" in ins)
check("A5 the house convention cited actually exists in frmInvSale",
      "InsertLinkedReturn(2, 1)" in SALE and
      "Invoic.InvertoryImpact = invertoryImpact;" in SALE)

print("Part B: R-043 / P4-002 - holding parks without moving stock")


def hold_basket(rules, lines):
    head_proc = 3
    out = [dict(l) for l in lines]                          # loaded sale lines, impact 2
    if rules == "fixed":
        for it in out:                                        # mirror quotation zeroing
            it["impact"] = 0
    return head_proc, out


sale_lines = [{"impact": 2, "qty": 5}, {"impact": 2, "qty": 1}]
_, legacy_lines = hold_basket("legacy", sale_lines)
_, fixed_lines = hold_basket("fixed", sale_lines)
check("B1 legacy held basket persisted sale impacts (stock moved on park - bug)",
      [l["impact"] for l in legacy_lines] == [2, 2])
check("B2 repaired hold zeros every line: a parked basket moves nothing",
      [l["impact"] for l in fixed_lines] == [0, 0])
hold_block = POS.split("private void btnHoldOrd_Click")[1].split("private void Hold1Btn_Click")[0]
check("B3 the zeroing sits before SaveAndPrint inside the hold slot loop",
      "foreach (var item in Invoic.InvoiceItems)\n                            item.InvertoryImpact = 0;" in hold_block
      and hold_block.index("item.InvertoryImpact = 0;") < hold_block.index("SaveAndPrint();"))
qi = SALE.index("ProcType = 4;"); quotation = SALE[qi:qi + 500]
check("B4 the mirrored quotation idiom really zeroes all lines there too",
      "foreach (var item in Invoic.InvoiceItems)\n                item.InvertoryImpact = 0;" in quotation)

print("Part C: R-044 / P4-005 - profit no longer depends on row order")


def profit(rules, margins_in_order):
    total = 0.0; cost = 0.0; inv_profit = 0.0
    for margin in margins_in_order:
        price = 100.0 + margin                               # arbitrary base per line
        cost_v = 100.0
        total += price
        cost += cost_v
        if rules == "legacy":
            inv_profit += total - cost                        # prefix-margin accumulation
    if rules == "fixed":
        inv_profit = total - cost                             # one derivation, final totals
    return inv_profit


truth = 30.0
check("C1 legacy profit differs by row order AND disagrees with the true margin (bug)",
      profit("legacy", [10, 20]) == 40.0 and profit("legacy", [20, 10]) == 50.0)
for order in ([10, 20], [20, 10], [5, 10, 15]):
    check("C2 repaired profit is %s and order-invariant" % truth,
          profit("fixed", order) == sum(order))
check("C3 no prefix accumulation survives anywhere in the two calculators",
      ITEMOP.count("InvProfit += ") == 0 and CONTRACT.count("InvProfit += ") == 0)
check("C4 exactly one derivation in CalcRows and two in the contract calculator",
      ITEMOP.count("invo.InvProfit = invo.Total - invo.SumCost;") == 1 and
      CONTRACT.count("Invo.InvProfit = Invo.Total - Invo.SumCost;") == 2)
check("C5 the reset-at-top semantics are preserved",
      "invo.InvProfit = 0;" in ITEMOP)

print("Part D: R-045 / P4-024 - confirmations follow commits")


class Txn:
    def __init__(self):
        self.committed = False
        self.rolled_back = False


def deliver(rules, insert_fails):
    tx = Txn()
    reported = None
    try:
        if insert_fails:
            raise RuntimeError("FK violation")
        tx.committed = True
        reported = True                                       # success box shown
    except Exception:
        tx.rolled_back = True
        reported = False if rules == "fixed" else None        # legacy: silent void
    return tx, reported


def window_flow(rules, insert_fails):
    tx, reported = deliver(rules, insert_fails)
    if rules == "legacy":
        announced = True                                      # unconditional
        closed = True
    else:
        announced = reported is True
        closed = announced
    return tx.committed, announced, closed


committed, announced, closed = window_flow("legacy", insert_fails=True)
check("D1 legacy announced success and closed over a rolled-back save (bug reproduced)",
      committed is False and announced is True and closed is True)
committed, announced, closed = window_flow("fixed", insert_fails=True)
check("D2 repaired failure leaves the window open with no confirmation",
      committed is False and announced is False and closed is False)
check("D3 successful delivery still confirms and closes identically",
      window_flow("legacy", False) == window_flow("fixed", False) == (True, True, True))

for src, label in ((ITEMOP, "ItemOper"), (CONTRACT, "contract twin")):
    m = src.split("public bool SaveInvoiceItemDeliveries")[1].split("public ")[0]
    check("D4 %s writer is bool-returning with true-after-commit and false-in-catch" % label,
          "transaction.Commit();" in m and "return true;" in m and
          "return false;" in m and m.index("return true;") > m.index("Commit()"))
check("D5 no void signature survives on either writer",
      ITEMOP.count("public void SaveInvoiceItemDeliveries") == 0 and
      CONTRACT.count("public void SaveInvoiceItemDeliveries") == 0)
check("D6 partial-delivery window gates ISDone/close behind the real result",
      "if (!new ItemOper().SaveInvoiceItemDeliveries(deliveryList, isDeliveredAll))\n                    return;" in PARTIAL
      and PARTIAL.index("isDeliveredAll))") < PARTIAL.index("ISDone = true;"))
check("D7 total-delivery window gates its announcement behind the real result",
      "if (!new ItemOper().SaveInvoiceItemDeliveries(deliveryList, true))\n                        return;" in TOTAL)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - POS returns restore stock, holds park quietly, profit is")
print("order-independent, and deliveries confirm only what truly committed.")
sys.exit(0)
