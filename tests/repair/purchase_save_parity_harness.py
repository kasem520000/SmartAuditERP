#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-049 (audit finding P4-031) in the purchase
invoice editor. No .NET/WPF/SQL Server toolchain exists here, so validation
models both save commands' predicate pipelines over representative item
lists, plus static witnesses extracted from the repaired file.

Legacy: Save-with-print refused an empty item list and non-positive
quantities, while plain Save accepted the very same invoices - two commands,
two contracts. Repaired: plain save enforces the same row contract first
(non-empty list, strictly positive quantities), mirroring the print path's
messages verbatim. Documented residual: unifying ALL checks (period,
reference, prompts) into one shared validator belongs to BLK-P3-002.

Run: python3 tests/repair/purchase_save_parity_harness.py
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


SRC = open("SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs", encoding="utf-8").read()


def gate(rules, command, items, net=100.0, supplier_ok=True):
    """returns 'saved' or the refusal reason, mirroring each handler's order."""
    if rules == "fixed" or command == "print":
        if len(items) == 0:
            return "refused:no-items"
        if any(q <= 0 for q in items):
            return "refused:nonpositive-qty"
    if command == "save":
        if net <= 0:
            return "refused:net"
        if not supplier_ok:
            return "refused:supplier"
    else:                                                   # print path net/supplier shape
        if net == 0.0:
            return "refused:net"
        if not supplier_ok:
            return "refused:supplier"
    return "saved"


print("Part A: the two buttons must share one row contract")
cases = [
    ("empty basket",          []),
    ("one zero-qty line",     [5.0, 0.0]),
    ("one negative-qty line", [3.0, -1.0]),
]
for label, items in cases:
    check("A-legacy '%s': save wrote what print refused (bug)" % label,
          gate("legacy", "save", items) == "saved" and
          gate("legacy", "print", items).startswith("refused"))
    check("A-fixed '%s': both commands refuse identically" % label,
          gate("fixed", "save", items) == gate("fixed", "print", items) != "saved")

good = [2.0, 7.5]
check("B1 valid invoices still save through BOTH commands unchanged",
      gate("legacy", "save", good) == gate("fixed", "save", good) == "saved" and
      gate("legacy", "print", good) == gate("fixed", "print", good) == "saved")
check("B2 untouched guards (net/supplier) keep working on plain save",
      gate("fixed", "save", good, net=-4) == "refused:net" and
      gate("fixed", "save", good, supplier_ok=False) == "refused:supplier")
check("B3 row contract precedes the financial checks (bad rows fail fast)",
      gate("fixed", "save", [], net=-4).endswith("no-items"))

print("Part C: static witnesses")
plain = SRC.split("private void btnSave_Click")[1].split("private void btnSavePrint_Click")[0]
prnt = SRC.split("private void btnSavePrint_Click")[1].split("private void SetPayAmounts")[0]
check("C1 plain save now carries both row predicates before the net check",
      plain.index("_invoiceItems.Count == 0") < plain.index("ItemQuantity <= 0") <
      plain.index("double.TryParse(this.txtNet.Text"))
import re
msgs_plain = re.findall(r'MessageBox\.Show\(("لا يمكن حفظ الفاتورة[^"]*")\)', plain)
msgs_print = re.findall(r'MessageBox\.Show\(("لا يمكن حفظ الفاتورة[^"]*")\)', prnt)
check("C2 the operator messages are byte-identical to the print path's",
      msgs_plain == msgs_print and len(msgs_plain) == 2)
check("C3 every refusal restores the button before returning",
      plain.count("this.btnSave.IsEnabled = true;") >= 6)
check("C4 the shared-validator residual stays documented where operators read it",
      "BLK-P3-002" in plain)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-049 (P4-031): plain purchase save refuses exactly the")
print("row-defective invoices its print twin always refused.")
sys.exit(0)
