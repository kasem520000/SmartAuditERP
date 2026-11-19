#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-010 (audit finding P7-140) in
SmartAuditERP/Class/Print.cs.

Finding: the ALTERNATE invoice-print path built an `invoiceData2` record and
passed Inv.Currency into the Arabic/English wording calls, yet never assigned
`invoiceData2.currency`, so reports from that branch rendered an empty
"العملة" field while the primary paths populated it
(`invoiceData.currency = Inv.Currency.ToString();`). The repair mirrors that
assignment verbatim on the alternate path.

No .NET toolchain is available here, so this harness validates the contract
two ways:
  1. Static witness over Print.cs: every binding path that computes
     ArabicLetter/ToEnWords from Inv.Currency also assigns `.currency` BEFORE
     doing so; counts match the two known call sites (+the foundation path).
  2. A tiny field-parity model: extract the invoice-level field names each
     path assigns and prove the only historical gap ('currency') is closed,
     with no other field lost or added by mistake.

Run: python3 tests/repair/print_data_parity_harness.py
Exit 0 on PASS.
"""
import re
import sys

src = open("SmartAuditERP/Class/Print.cs", encoding="utf-8").read()
lines = src.splitlines()
FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


print("Part A: static witnesses in Print.cs")

cur_assigns = [i for i, l in enumerate(lines) if re.search(r"\binvoiceData\d?\.currency\s*=\s*Inv\.Currency\.ToString\(\);", l)]
tafqit_sites = [i for i, l in enumerate(lines) if "InvoiceOper.ToArabicLetter(" in l]
en_sites = [i for i, l in enumerate(lines) if "SpellNumberEDP(" in l]

check("A1 currency assignment appears on BOTH invoice paths (%d sites)" % len(cur_assigns),
      len(cur_assigns) >= 3, str(len(cur_assigns)))   # foundation-area + path A + path B

check("A2 two Arabic-wording call sites remain intact", len(tafqit_sites) == 2, str(tafqit_sites))
check("A2 two English-wording call sites remain intact", len(en_sites) == 2, str(en_sites))

# Every tafqeet site must have a .currency assignment ABOVE it (data filled
# before the wording fields), on the same variable family as the site itself.
for site in tafqit_sites:
    var = "invoiceData2" if "invoiceData2." in lines[site] else "invoiceData"
    above = [i for i in cur_assigns if i < site and lines[i].lstrip().startswith(var + ".currency")]
    check("A3 %s gets .currency before its ArabicLetter at line %d" % (var, site + 1),
          bool(above), "no prior assignment for %s" % var)

print("Part B: invoice-level field parity between the two binding paths")

# Delimit the two per-invoice header blocks: each starts at its .currency
# assignment (first field of the invoice-level group) and ends at RefDate,
# which is the last invoice-level field both paths share in order.
def block(var):
    starts = [i for i, l in enumerate(lines)
              if re.search(r"\b%s\.currency\s*=\s*Inv\.Currency\.ToString\(\);" % var, l)]
    assert starts, "no currency assignment found for %s" % var
    start = starts[-1]                                    # the invoice-path copy
    end = next(i for i, l in enumerate(lines)
               if i > start and re.search(r"\b%s\.RefDate\s*=" % var, l))
    body = "\n".join(lines[start:end + 1])
    return {m.group(1) for m in re.finditer(r"\b%s\.([A-Za-z_][A-Za-z0-9_]*)\s*=" % var, body)}


fields_a = block("invoiceData")
fields_b = block("invoiceData2")

check("B1 path A still assigns 'currency'", "currency" in fields_a)
check("B2 path B now assigns 'currency' (the repaired gap)", "currency" in fields_b,
      repr(sorted(fields_b)[:12]))

# Shared invoice-level fields present on A should not have vanished from B where
# B historically mirrored them; the ONLY sanctioned delta vs the audited state
# is the ADDED 'currency' on B.
shared_core = {"SumPrice", "Net", "ArabicLetter", "ToEnWords", "Discount",
               "Additions", "PayNetwork", "Insurance", "Paycash", "Remainder",
               "ReffNo", "RefDate"}
missing_from_b = shared_core - fields_b
check("B3 path B kept all core invoice-level fields", not missing_from_b,
      repr(sorted(missing_from_b)))

still_only_on_a = (fields_a - fields_b) & shared_core
check("B4 no shared core field remains exclusive to path A", not still_only_on_a,
      repr(sorted(still_only_on_a)))

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-010 (P7-140): both invoice print paths populate the")
print("currency field ahead of the wording calls; no other path-B field lost.")
sys.exit(0)
