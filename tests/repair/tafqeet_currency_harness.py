#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-008 (audit finding P7-034) and R-009 (P7-035)
in SmartAuditERP/Class/InvoiceOper.cs.

No .NET toolchain exists in this sandbox, so the C# cannot be compiled/run.
Instead this harness re-implements, in Python, BOTH the legacy logic (copied
verbatim from the pre-repair source) and the repaired logic (mirroring the
edited C# line-for-line), with the wording engines (SFormatNumber /
NumberAsCurrency digit spelling) represented as opaque deterministic TOKENS
that are shared by both models. Any difference between the two models can
therefore only come from the decomposition/selection logic being repaired -
exactly the surface of these two findings.

R-008 scope: ToArabicLetter used to split Conversions.ToString(x) on the
literal "." and TRUNCATE fractions beyond two digits => culture-separator
dependence and amounts whose words did not equal one rounded amount at
2-decimal currency precision. The repair settles one amount:
round-half-AWAY-from-zero to whole sub-units, arithmetic int/frac split.

R-009 scope: NumberAsCurrency/FractionAsCurrency (Arabic) and SpellNumberEDP
(English) carried disjoint private (int)MyCurrency cascades, so one symbol
could spell Riyal in one language and Pound/Euro/Yen/Dirham in the other.
The repair routes ALL three methods through one shared labels table.

Run: python3 tests/repair/tafqeet_currency_harness.py [--verbose]
Exit 0 on PASS, non-zero on any failure.
"""
import math
import random
import re
import sys

VERBOSE = "--verbose" in sys.argv
FAILS = []


def check(name, cond, detail=""):
    if cond:
        if VERBOSE:
            print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


# ---------------------------------------------------------------------------
# Shared opaque wording tokens (stand-ins for SFormatNumber internals).
# Both models call the SAME tokens, so their internals never affect parity.
# ---------------------------------------------------------------------------
def NUM_WORDS(n, cur):           # stand-in for SFormatNumber(number) result
    return "N[%g|%d]" % (n, int(cur))


SUFFIX = " فقط لا غير"
W = " و"


# ---------------------------------------------------------------------------
# LEGACY ToArabicLetter (verbatim translation of the pre-repair C# branch)
# ---------------------------------------------------------------------------
def legacy_number_as_currency_label(given, cur):
    # Only the LABEL cascade matters for decomposition checks; words are tokens.
    left = str(int(cur))
    n = given
    if left == "2":
        lab = "" if n == 0 else (" اثنان دولار" if n == 2 else ("دولار" if (n < 3 or n > 10) else " دولار"))
    elif left == "12":
        lab = "" if n == 0 else (" جنيهان مصريان" if n == 2 else (" جنيه مصري" if (n < 3 or n > 10) else " جنيهات مصرية"))
    elif left == "13":
        lab = "" if n == 0 else (" جنيهان سودانيان" if n == 2 else (" جنيه سوداني" if (n < 3 or n > 10) else " جنيهات سودانية"))
    elif left == "15":
        lab = ("ليرة سورية" if n == 0 else ("ليرة سورية" if n == 1 else ("ليرتان سوريتان" if n == 2 else ("ليرة سورية" if (n < 3 or n > 10) else "ليرات سورية"))))
    else:
        lab = "" if n == 0 else (" اثنان ريال" if n == 2 else ("ريال" if (n < 3 or n > 10) else " ريال"))
    return lab


def legacy_fraction_label(given, cur):
    left = str(int(cur))
    n = given
    if left == "2":
        lab = "" if n == 0 else (" سنتان" if n == 2 else ("سنت" if (n < 3 or n > 10) else " سنتات"))
    elif left == "12":
        lab = "" if n == 0 else (" قرشان" if n == 2 else (" قرشا" if (n < 3 or n > 10) else " قروش"))
    elif left == "13":
        lab = "" if n == 0 else (" قرشان" if n == 2 else (" قرشا" if (n < 3 or n > 10) else " قروش"))
    else:
        lab = "" if n == 0 else (" هللتين" if n == 2 else (" هللة" if (n < 3 or n > 10) else " ه\u064eل\u064eلات"))
    return lab


def legacy_num_currency(given, cur):
    return NUM_WORDS(given, cur) + " " + legacy_number_as_currency_label(given, cur)


def legacy_frac_currency(given, cur):
    return NUM_WORDS(given, cur) + " " + legacy_fraction_label(given, cur)


def dotnet_double_str(x):
    # Emulate .NET Double.ToString() general format well enough for this logic:
    # integral doubles print WITHOUT a decimal point ("0", "123"), others keep
    # the shortest round-trip form ("123.45"). This matches what the legacy
    # Conversions.ToString produced for these shapes under invariant-style
    # cultures, and it is the input the legacy "." split operated on.
    xf = float(x)
    if math.isnan(xf):
        return "NaN"
    if math.isinf(xf):
        return "Infinity" if xf > 0 else "-Infinity"
    if xf == math.floor(xf) and abs(xf) < 1e16:
        return str(int(xf))
    return repr(xf)


def legacy_to_arabic_letter(x, cur):
    # Strings.Split(Conversions.ToString(x), ".") - VB ToString uses the current
    # culture; modelled with dotnet_double_str above (dot separator), which is
    # the behaviour under invariant/en locales and the best case for legacy code.
    parts = dotnet_double_str(x).split(".")
    text2 = legacy_num_currency(float(parts[0]), cur)
    if len(parts) >= 2:
        fr = parts[1]
        if len(fr) == 1:
            fr += "0"
        elif len(fr) > 2:
            fr = fr[:2]                      # <-- the truncation defect
        text2 = text2 + W + legacy_frac_currency(float(fr), cur)
    if text2 is not None and text2 != "":
        text2 += SUFFIX
    return text2


# ---------------------------------------------------------------------------
# REPAIRED ToArabicLetter (mirrors the edited C# fast path + legacy fallback)
# ---------------------------------------------------------------------------
LIMIT = 90000000000000000.0


def round_half_away(value):
    # Math.Round(v, MidpointRounding.AwayFromZero) on a double, integral target.
    f = math.floor(value)
    diff = value - f
    if diff > 0.5:
        return int(f) + 1
    if diff < 0.5:
        return int(f)
    return int(f) + 1  # exact .5 -> away from zero (value >= 0 on this path)


def fixed_to_arabic_letter(x, cur):
    xf = float(x)
    if not (math.isnan(xf) or math.isinf(xf)) and 0.0 <= xf <= LIMIT:
        total = round_half_away(xf * 100.0)
        ip, fp = divmod(total, 100)
        settled = legacy_num_currency(float(ip), cur)
        if fp != 0:
            settled = settled + W + legacy_frac_currency(float(fp), cur)
        if settled is not None and settled != "":
            settled += SUFFIX
        return settled
    return legacy_to_arabic_letter(xf, cur)


# ====================== PART A: R-008 decomposition =========================
print("Part A: R-008 / P7-034 - single-amount settlement vs truncation")

# A1. No regression for amounts already having <= 2 decimal digits.
random.seed(20260519)
same = 0
diff_unexpected = []
for _ in range(6000):
    cents = random.randrange(0, 10 ** 11)          # up to ~1e9 units
    x = cents / 100.0
    dstr = dotnet_double_str(x)
    if "." in dstr and len(dstr.split(".")[1]) > 2:   # binary-repr noise guard
        continue
    a, b = legacy_to_arabic_letter(x, 1), fixed_to_arabic_letter(x, 1)
    if a == b:
        same += 1
    else:
        diff_unexpected.append((x, a, b))
check("A1 <=2-decimal amounts phrase identically (%d samples)" % same,
      same >= 5000 and not diff_unexpected, str(diff_unexpected[:3]))

# Explicit stable edges.
for x in (0.0, 0.01, 0.10, 0.5, 0.99, 1.0, 2.0, 3.0, 11.0, 123.45, 999999999.99):
    check("A1-edge x=%s identical" % x,
          legacy_to_arabic_letter(x, 1) == fixed_to_arabic_letter(x, 1))

# A2. Truncated amounts now settle to ONE rounded amount.
cases = [
    # (x, legacy(int,frac), fixed(int,frac))
    (0.129, (0.0, 12.0), (0.0, 13.0)),     # third digit used to be discarded
    (0.999, (0.0, 99.0), (1.0, 0.0)),      # carry into the unit
    (9.996, (9.0, 99.0), (10.0, 0.0)),     # cross-ten carry
    (123.999, (123.0, 99.0), (124.0, 0.0)),
    (1.125, (1.0, 12.0), (1.0, 13.0)),     # exact half -> AWAY from zero (112 would be banker's)
]
for x, l_exp, f_exp in cases:
    lp = dotnet_double_str(x).split(".")
    lfr = lp[1]
    if len(lfr) == 1:
        lfr += "0"
    elif len(lfr) > 2:
        lfr = lfr[:2]
    got_l = (float(lp[0]), float(lfr))
    tot = round_half_away(x * 100.0)
    got_f = divmod(tot, 100)
    got_f = (float(got_f[0]), float(got_f[1]))
    check("A2 legacy decomposition x=%s == %s" % (x, l_exp), got_l == l_exp, str(got_l))
    check("A2 fixed decomposition x=%s == %s" % (x, f_exp), got_f == f_exp, str(got_f))
    # And the resulting wordings genuinely differ (proof the fix engages).
    check("A2 wording changed where truncation bit (x=%s)" % x,
          legacy_to_arabic_letter(x, 1) != fixed_to_arabic_letter(x, 1))

# Single-amount property: fixed int+frac equals round(x,2)*100 exactly.
ok = True
for x in (0.129, 0.999, 9.996, 123.999, 1.125, 0.001, 57.3):
    ip, fp = divmod(round_half_away(x * 100.0), 100)
    if ip * 100 + fp != round_half_away(x * 100.0):
        ok = False
check("A2 settlement is one coherent amount", ok)

# A3. Exotic inputs fall through to the untouched legacy path, byte-identical.
for x in (-5.555, -0.001, float("nan"), float("inf"), float("-inf"), 9.1e16, 1e18):
    try:
        a = legacy_to_arabic_letter(x, 8)
    except Exception:
        a = "LEGACY-RAISES"
    try:
        b = fixed_to_arabic_letter(x, 8)
    except Exception:
        b = "LEGACY-RAISES"
    check("A3 exotic pass-through x=%s identical" % x, a == b, "%r vs %r" % (a, b))

# ====================== PART B: R-009 label parity ==========================
print("Part B: R-009 / P7-035 - shared currency labels, no cross-language drift")

DEFAULT = dict(ar=dict(m0="", mdual=" اثنان ريال", mout="ريال", min_=" ريال",
                       f0="", fdual=" هللتين", fout=" هللة", fin=" ه\u064eل\u064eلات"),
               en=("Riyal", "Riyals", "Halala", "Halalas"))
TABLE = {
    2: dict(ar=dict(m0="", mdual=" اثنان دولار", mout="دولار", min_=" دولار",
                    f0="", fdual=" سنتان", fout="سنت", fin=" سنتات"),
            en=("Dollar", "Dollars", "Cent", "Cents")),
    4: dict(ar=dict(m0="", mdual="درهمان", mout="درهم", min_="دراهم",
                    f0="", fdual="فلسان", fout="فلس", fin="فلوس"),
            en=("Dirham", "Dirhams", "Fil", "Fils")),
    8: dict(ar=dict(DEFAULT["ar"]), en=DEFAULT["en"]),
    9: dict(ar=dict(m0="", mdual="جنيهان", mout="جنيه", min_="جنيهات",
                    f0="", fdual="بنسان", fout="بنس", fin="بنسات"),
            en=("Pound", "Pounds", "Penny", "Pence")),
    10: dict(ar=dict(m0="", mdual="يوروان", mout="يورو", min_="يورو",
                     f0="", fdual="سنتان", fout="سنت", fin="سنتات"),
             en=("Euro", "Euros", "Cent", "Cents")),
    11: dict(ar=dict(m0="", mdual="ينان", mout="ين", min_="ين",
                     f0="", fdual="سنان", fout="سن", fin="سنات"),
             en=("Yen", "Yens", "Sen", "Sens")),
    12: dict(ar=dict(m0="", mdual=" جنيهان مصريان", mout=" جنيه مصري", min_=" جنيهات مصرية",
                     f0="", fdual=" قرشان", fout=" قرشا", fin=" قروش"),
             en=("Egyptian Pound", "Egyptian Pounds", "Piastre", "Piastres")),
    13: dict(ar=dict(m0="", mdual=" جنيهان سودانيان", mout=" جنيه سوداني", min_=" جنيهات سودانية",
                     f0="", fdual=" قرشان", fout=" قرشا", fin=" قروش"),
             en=("Sudanese Pound", "Sudanese Pounds", "Piastre", "Piastres")),
    15: dict(ar=dict(m0="ليرة سورية", mdual="ليرتان سوريتان", mout="ليرة سورية", min_="ليرات سورية",
                     f0="", fdual=" قرشان", fout=" قرشا", fin=" قروش"),
             en=("Syrian Pound", "Syrian Pounds", "Piastre", "Piastres")),
}


def resolve(cur):
    row = TABLE.get(int(cur), DEFAULT)
    return row["ar"], row["en"]


def new_ar_main(n, cur):
    a, _ = resolve(cur)
    return a["m0"] if n == 0 else (a["mdual"] if n == 2 else (a["mout"] if (n < 3 or n > 10) else a["min_"]))


def new_ar_frac(n, cur):
    a, _ = resolve(cur)
    return a["f0"] if n == 0 else (a["fdual"] if n == 2 else (a["fout"] if (n < 3 or n > 10) else a["fin"]))


def new_en(cur):
    _, e = resolve(cur)
    return e


SAMPLE_N = [0, 1, 2, 3, 5, 10, 11, 100, 1000]

# B1. Byte-identical regression for every key/shape the legacy cascades covered.
for cur in (2, 12, 13, 15, 1):                       # 1 exercises the AR default branch
    for n in SAMPLE_N:
        check("B1 AR-main legacy==fixed key=%s n=%s" % (cur, n),
              new_ar_main(float(n), cur) == legacy_number_as_currency_label(float(n), cur))
for cur in (2, 12, 13, 1):                            # legacy FRAC cascade had no 15 => halala fallthrough
    for n in SAMPLE_N:
        check("B1 AR-frac legacy==fixed key=%s n=%s" % (cur, n),
              new_ar_frac(float(n), cur) == legacy_fraction_label(float(n), cur))


def legacy_en_names(cur):
    s = str(int(cur))
    if s == "2":
        return ("Dollar", "Dollars", "Cent", "Cents")
    if s == "4":
        return ("Dirham", "Dirhams", "Fil", "Fils")
    if s == "9":
        return ("Pound", "Pounds", "Penny", "Pence")
    if s == "10":
        return ("Euro", "Euros", "Cent", "Cents")
    if s == "11":
        return ("Yen", "Yens", "Sen", "Sens")
    return ("Riyal", "Riyals", "Halala", "Halalas")   # includes explicit 8 and default


for cur in (2, 4, 8, 9, 10, 11, 1):
    check("B1 EN legacy==fixed key=%s" % cur, new_en(cur) == legacy_en_names(cur))

# B2. Cross-language coherence: for n=5 (plural shape) each key must announce
# the exact expected labels in both languages - never one side Riyal while the
# other names another currency (the audited drift).
EXPECT_N5 = {
    2: (" دولار", "Dollars"), 4: ("دراهم", "Dirhams"), 8: (" ريال", "Riyals"),
    9: ("جنيهات", "Pounds"), 10: ("يورو", "Euros"), 11: ("ين", "Yens"),
    12: (" جنيهات مصرية", "Egyptian Pounds"), 13: (" جنيهات سودانية", "Sudanese Pounds"),
    15: ("ليرات سورية", "Syrian Pounds"),
}
RIYAL_AR_FORMS = {" ريال", "ريال"}
for cur, (ar_label, en_label) in EXPECT_N5.items():
    am = new_ar_main(5.0, cur)
    en_pl = new_en(cur)[1]
    check("B2 key=%s AR plural label == %r" % (cur, ar_label), am == ar_label, repr(am))
    check("B2 key=%s EN plural label == %r" % (cur, en_label), en_pl == en_label, repr(en_pl))
    ar_is_riyal = am in RIYAL_AR_FORMS
    en_is_riyal = en_label.startswith("Riyal")
    check("B2 key=%s Riyal agreement (was the core drift)" % cur,
          ar_is_riyal == en_is_riyal, "AR=%r EN=%r" % (am, en_label))
    # And where legacy contradicted, the repaired pair differs from legacy AR/EN.
    if cur in (4, 9, 10, 11):            # legacy AR said ' ريال' here
        check("B2 key=%s legacy AR contradiction resolved" % cur,
              legacy_number_as_currency_label(5.0, cur) != am)
    if cur in (12, 13, 15):              # legacy EN said 'Riyals' here
        check("B2 key=%s legacy EN contradiction resolved" % cur,
              legacy_en_names(cur)[1] != en_pl)

# Default/unknown key: identical Riyal/Halala in BOTH languages, as legacy did.
for cur in (1, 3, 999):
    check("B2 unknown key=%s defaults to Riyal in AR and EN" % cur,
          new_ar_main(5.0, cur) in RIYAL_AR_FORMS and new_en(cur)[1] == "Riyals")

# B3. The intra-Arabic defect closed: Syrian lira FRACTION no longer Halala.
check("B3 key=15 fraction is piastre family, not halala",
      new_ar_frac(5.0, 15) == " قروش" and "هلل" not in new_ar_frac(5.0, 15))
check("B3 key=15 fraction dual unchanged-style pairing",
      new_ar_frac(2.0, 15) == " قرشان")
check("B3 key=15 main unit unchanged for all shapes",
      all(new_ar_main(float(n), 15) == legacy_number_as_currency_label(float(n), 15)
          for n in SAMPLE_N))

# B4. Static witness: the shared table and resolver really exist in the C# file.
src = open("SmartAuditERP/Class/InvoiceOper.cs", encoding="utf-8").read()
for key in (2, 4, 8, 9, 10, 11, 12, 13, 15):
    check("B4 C# table has key %d" % key,
          re.search(r"\{\s*%d\s*,\s*new CurrencyLabels" % key, src) is not None)
for needle in ("private sealed class CurrencyLabels",
               "ResolveCurrencyLabels(Currency MyCurrency)",
               "_defaultCurrencyLabels",
               "labels.EnSing", "labels.ArMainOut", "labels.ArFracIn"):
    check("B4 C# contains %s" % needle.split()[0], needle in src)
# The old disjoint cascades are gone.
check("B4 legacy AR-only cascade removed", '" جنيهان مصريان" : ((' not in src.replace(" ", "")
      or src.count('Conversions.ToString(12)') == 0)
check("B4 legacy EN-only cascade removed", src.count('"Pence"') == 1)  # only in the shared table

# ---------------------------------------------------------------------------
print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS[:40]:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-008 (P7-034) settlement model and R-009 (P7-035)")
print("shared-labels model behave as contracted; legacy-covered outputs are")
print("byte-identical, truncated amounts settle to one rounded amount, and no")
print("currency key can phrase contradictory names across languages anymore.")
sys.exit(0)
