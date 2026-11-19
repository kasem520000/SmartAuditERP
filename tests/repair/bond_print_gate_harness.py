#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-011 (audit finding P7-141) in
SmartAuditERP/Form_WPF/frmSandD.xaml.cs and frmSandQAndroid.xaml.cs.

Finding: RptPrint() only rejected an EMPTY value; BindToData() then evaluated
    double netVal = double.TryParse(txtVal.Text, out v) ? v : 0;
and copied the ORIGINAL text into Bond.BondVal. Any non-numeric text therefore
printed as the words-of-ZERO (InvoiceOper.ToArabicLetter(0, ...)) beside its raw
text - a payment bond whose amount and its legal wording contradict each other.
The repair rejects unparseable values up front with the same warning UX pattern
already used for the empty case; valid numbers (including a deliberate zero)
print exactly as before.

No .NET toolchain exists here, so this harness models the gate sequence
pre/post fix and proves:
  * pre-fix reproduces the inconsistency (zero-wording next to non-numeric text);
  * post-fix blocks exactly the inconsistent inputs and nothing else;
  * legitimate values keep identical print payloads across the fix.
It also witnesses statically that both forms now parse-guard inside RptPrint
immediately after the empty-value guard, using the same TryParse semantics.

Culture caveat (documented per work rules): real double.TryParse is
culture-dependent; the model uses invariant parsing, matching the C# when the
thread culture parses '.' decimals. Digit-shape cases outside that profile are
environment-dependent by nature and cannot be settled in this sandbox.

Run: python3 tests/repair/bond_print_gate_harness.py
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


def parse_val(text):
    """Invariant double.TryParse stand-in."""
    try:
        return True, float(text)
    except (TypeError, ValueError):
        return False, 0.0


def tafqeet(value):
    return "WORDS(%g)" % value          # opaque token; only identity matters


class PrintOutcome:
    def __init__(self, blocked, reason=None, bond_val=None, words=None):
        self.blocked = blocked
        self.reason = reason
        self.bond_val = bond_val
        self.words = words

    @property
    def inconsistent(self):
        if self.blocked:
            return False
        ok, val = parse_val(self.bond_val)
        if not ok:
            # A bond whose amount text cannot even be read as a number but was
            # still printed IS the audited defect (its wording says zero).
            return True
        shown_as_zero = self.words == tafqeet(0.0)
        return shown_as_zero != (val == 0.0)


def rptprint_old(text):
    if text is None or text.strip() == "":
        return PrintOutcome(True, "empty")
    ok, v = parse_val(text)
    net = v if ok else 0.0              # legacy silent coercion
    return PrintOutcome(False, None, bond_val=text, words=tafqeet(net))


def rptprint_new(text):
    if text is None or text.strip() == "":
        return PrintOutcome(True, "empty")
    ok, _ = parse_val(text)
    if not ok:                          # Repair R-011 gate
        return PrintOutcome(True, "non-numeric")
    _, v = parse_val(text)
    return PrintOutcome(False, None, bond_val=text, words=tafqeet(v))


print("Part A: behavioural model of the print gate")

# NOTE: "١٢٣" (Arabic-Indic digits) parses successfully here exactly as it does
# under .NET cultures whose TryParse accepts those digit shapes - it therefore
# yields a CONSISTENT bond and belongs with the valid inputs, not the defect
# class. The model's membership rule is simply "whatever the parser accepts".
valid = ["0", "0.00", "1500", "1500.75", "-25.5", "1e3", "١٢٣"]
invalid = ["abc", "12.5x", "1,500", "--3", "nan-ish", " ", "   \t "]

# A1. Pre-fix reproduces the audited defect.
repro = [t for t in invalid if t.strip() != "" and not rptprint_old(t).blocked
         and rptprint_old(t).inconsistent]
check("A1 pre-fix prints contradictory bonds for all non-numeric texts (%d/%d)"
      % (len(repro), len([t for t in invalid if t.strip()])),
      len(repro) == len([t for t in invalid if t.strip()]), str(repro))
example = rptprint_old("abc")
check("A1 example 'abc' -> zero words beside original text",
      example.words == "WORDS(0)" and example.bond_val == "abc")

# A2. Post-fix blocks exactly the inconsistent class.
for t in invalid:
    o = rptprint_new(t)
    if t.strip() == "":
        check("A2 empty stays blocked (%r)" % t, o.blocked and o.reason == "empty")
    else:
        check("A2 non-numeric now blocked (%r)" % t,
              o.blocked and o.reason == "non-numeric")

# A3. Legitimate values unchanged, payload byte-identical across the fix.
for t in valid:
    old, new = rptprint_old(t), rptprint_new(t)
    check("A3 valid %r prints identically pre/post fix" % t,
          not new.blocked and new.bond_val == old.bond_val and new.words == old.words,
          "%s vs %s" % ((old.bond_val, old.words), (new.bond_val, new.words)))

# A4. No outcome under the fix is ever internally inconsistent.
allinputs = valid + invalid
check("A4 post-fix never emits an inconsistent bond",
      not any(rptprint_new(t).inconsistent for t in allinputs))

print("Part B: static witnesses in both Android bond forms")

FORMS = ["SmartAuditERP/Form_WPF/frmSandD.xaml.cs",
         "SmartAuditERP/Form_WPF/frmSandQAndroid.xaml.cs"]
GUARD_RE = re.compile(
    r"لا توجد قيمة بالسند\..*?return;\s*\}\s*"                       # empty guard block...
    r"(?:[^\n]*\n){0,9}?"                                            # comment lines
    r"\s*if\s*\(!double\.TryParse\(txtVal\.Text,\s*out\s+_\)\)",     # followed by the new gate
    re.S)

for path in FORMS:
    src = open(path, encoding="utf-8").read()
    m = GUARD_RE.search(src)
    check("B1 %s guards non-numeric value right after the empty guard" % path.split('/')[-1],
          m is not None)
    # The guard sits inside RptPrint, ahead of BindToData consumption.
    rp = src.find("public void RptPrint(int printType)")
    bd = src.find("private DataSet BindToData()")
    gpos = m.start() if m else -1
    check("B2 %s gate lies between RptPrint entry and BindToData" % path.split('/')[-1],
          rp != -1 and bd != -1 and rp < gpos < bd)
    # Legacy silent coercion remains documented as the downstream fallback only.
    check("B3 %s keeps the original BindToData coercion untouched" % path.split('/')[-1],
          "double.TryParse(txtVal.Text, out double v) ? v : 0" in src)
    check("B4 %s warns in Arabic with the form's existing UX" % path.split('/')[-1],
          "قيمة السند ليست رقماً صالحاً." in src)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-011 (P7-141): non-numeric bond values can no longer")
print("reach printing as words-of-zero beside their raw text; valid amounts")
print("(including zero) print exactly as before, on both bond forms.")
sys.exit(0)
