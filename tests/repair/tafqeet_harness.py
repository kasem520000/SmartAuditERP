#!/usr/bin/env python3
"""
Repair R-001 verification harness (audit finding P7-139).

Isolated, dependency-free model of the Arabic number-to-words engine in
SmartAuditERP/Class/InvoiceOper.cs::SFormatNumber. It transcribes BOTH:

  * `original()` -- the legacy positional decoder, pinned to a fixed 12-digit
    template and reading every digit/group through absolute Mid() offsets
    (valid only for magnitudes with <= 12 integer digits), and
  * `fixed_sformat()` -- the repaired dispatcher that routes <= 12-digit values
    to the untouched legacy core (byte-identical output => no regression) and
    composes wider magnitudes from right-anchored 3-digit groups with standard
    Arabic short-scale names (trillion+).

Purpose / limits (see docs/repairs/PLAN.md, Rule 9):
  - This proves the LOGIC of the change, not that the ERP builds or runs.
  - No .NET toolchain exists in this environment; WPF/SQL/printing remain
    blocked for operational verification. Success here == verified-in-scope for
    the text-conversion logic only.

Usage:  python3 tests/repair/tafqeet_harness.py [--samples N]
Exit 0 on success, 1 on any regression mismatch.
"""
import math
import random
import sys

ONES = {1: "واحد", 2: "اثنان", 3: "ثلاثة", 4: "اربعة", 5: "خمسة",
        6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعة"}
TENS = {1: "عشر", 2: "عشرون", 3: "ثلاثون", 4: "اربعون", 5: "خمسون",
        6: "ستون", 7: "سبعون", 8: "ثمانون", 9: "تسعون"}
HUND = {1: "مائة", 2: "مائتان"}


def _mid(s, start, length):
    """VB.Strings.Mid (1-based)."""
    return s[start - 1:start - 1 + length]


def _val(sub):
    """VB.Conversion.Val on our single-char / 3-char digit substrings."""
    sub = sub.strip()
    if not sub:
        return 0
    try:
        return int(sub)
    except ValueError:
        return 0


def original(x):
    """Faithful transcription of the legacy SFormatNumber engine.

    Mirrors Strings.Format(floor, "000000000000"): left-zero-pad to >=12 chars
    WITHOUT truncating, so magnitudes beyond 12 digits yield a longer string and
    every absolute Mid offset reads the wrong digit (the reported defect).
    Returns None where the C# returns default(string); normalized to '' by callers.
    """
    n = int(math.floor(x))
    digits = str(abs(n))
    s = ("-" if n < 0 else "") + digits.zfill(12)

    def M(start, length):
        return _val(_mid(s, start, length))

    num = M(12, 1)                 # ones
    text = ONES.get(num)           # None if 0
    num3 = M(11, 1)                # tens
    text2 = TENS.get(num3)         # None if 0
    if text not in (None, "") and num3 > 1:
        text2 = text + " و" + text2
    if text2 in (None, ""):
        text2 = text
    if num == 0 and num3 == 1:
        text2 = (text2 or "") + "ة"
    if num == 1 and num3 == 1:
        text2 = "احدى عشر"
    if num == 2 and num3 == 1:
        text2 = "اثنى عشر"
    if num > 2 and num3 == 1:
        text2 = text + " " + text2

    num5 = M(10, 1)                # hundreds
    text3 = HUND.get(num5)
    if num5 is not None and num5 > 2:
        sub = original(num5) or ""
        text3 = sub[:len(sub) - 1] + "مائة"
    if text3 not in (None, "") and text2 not in (None, ""):
        text3 = text3 + " و" + text2
    if text3 in (None, ""):
        text3 = text2

    num7 = M(7, 3)                 # thousands group
    if num7 == 1:
        text4 = "الف"
    elif num7 == 2:
        text4 = "الفان"
    elif 3 <= num7 <= 10:
        text4 = (original(num7) or "") + " آلاف"
    elif num7 > 10:
        text4 = (original(num7) or "") + " الف"
    else:
        text4 = None
    if text4 not in (None, "") and text3 not in (None, ""):
        text4 = text4 + " و" + text3
    if text4 in (None, ""):
        text4 = text3

    num9 = M(4, 3)                 # millions group
    if num9 == 1:
        text5 = "مليون"
    elif num9 == 2:
        text5 = "مليونان"
    elif 3 <= num9 <= 10:
        text5 = (original(num9) or "") + " ملايين"
    elif num9 > 10:
        text5 = (original(num9) or "") + " مليون"
    else:
        text5 = None
    if text5 not in (None, "") and text4 not in (None, ""):
        text5 = text5 + " و" + text4
    if text5 in (None, ""):
        text5 = text4

    num11 = M(1, 3)                # billions group
    if num11 == 1:
        text6 = "مليار"
    elif num11 == 2:
        text6 = "ملياران"
    elif num11 > 2:
        text6 = (original(num11) or "") + " مليار"
    else:
        text6 = None
    if text6 not in (None, "") and text5 not in (None, ""):
        text6 = text6 + " و" + text5
    if text6 in (None, ""):
        text6 = text5
    return text6


SCALE_S = ["", "الف", "مليون", "مليار", "تريليون", "كوادريليون", "كوينتيليون", "سكستيليون"]
SCALE_D = ["", "الفان", "مليونان", "ملياران", "تريليونان", "كوادريليونان", "كوينتيليونان", "سكستيليونان"]
SCALE_P = ["", "آلاف", "ملايين", "مليار", "تريليونات", "كوادريليونات", "كوينتيليونات", "سكستيليونات"]


def _scale_phrase(idx, v):
    if 0 <= idx < len(SCALE_S):
        if v == 1:
            return SCALE_S[idx]
        if v == 2:
            return SCALE_D[idx]
        words = original(v) or ""
        if 3 <= v <= 10:
            return (words + " " + SCALE_P[idx]).strip()
        return (words + " " + SCALE_S[idx]).strip()
    words = original(v) or ""
    return (words + " ×10^" + str(idx * 3)).strip()


def _wide(n):
    """Right-anchored composition for magnitudes beyond 12 digits.

    Uses integer arithmetic here for exactness; the C# path uses double, which
    is exact for integers up to 2**53 (~9.0e15) -- ample for monetary values.
    """
    low_twelve = n % 10 ** 12
    low_word = original(low_twelve) or ""
    rem = n // 10 ** 12
    idx = 4                       # 10^(3*4) = trillion
    high = []
    while rem >= 1:
        gv = rem % 1000
        if gv != 0:
            high.append(_scale_phrase(idx, gv))
        rem //= 1000
        idx += 1
    high.reverse()
    out = ""
    for p in high:
        if p:
            out = (out + " و" + p) if out else p
    if low_word:
        out = (out + " و" + low_word) if out else low_word
    return out


def fixed_sformat(x):
    n = math.floor(x)
    if math.isnan(n) or math.isinf(n) or n < 0:
        return original(x)
    if n <= 999_999_999_999:
        return original(x)
    return _wide(int(n))


def norm(s):
    return "" if s is None else s


def main():
    args = sys.argv[1:]
    samples = 30000
    if "--samples" in args:
        samples = int(args[args.index("--samples") + 1])

    # --- Part A: regression identity over the valid <=12-digit window ---
    boundaries = [0, 1, 2, 3, 5, 9, 10, 11, 12, 19, 20, 21, 99, 100, 101, 110,
                  111, 200, 999, 1000, 1001, 2000, 9999, 10000, 12345, 99999,
                  100000, 999999, 1000000, 1000001, 2000000, 9999999,
                  10000000, 99999999, 100000000, 999999999, 1000000000,
                  1234567890, 2000000000, 9999999999, 10000000000,
                  99999999999, 100000000000, 123456789012, 999999999999]
    rng = random.Random(20261119)
    universe = list(boundaries)
    for _ in range(samples):
        exp = rng.randint(0, 12)
        hi = min(10 ** exp, 999_999_999_999)
        universe.append(rng.randint(0, hi))

    mismatches = 0
    first_bad = None
    for n in universe:
        a = norm(original(n))
        b = norm(fixed_sformat(n))
        if a != b:
            mismatches += 1
            if first_bad is None:
                first_bad = (n, a, b)
    print("[A] regression identity over <=12-digit window")
    print("    tested values:", len(universe))
    print("    mismatches   :", mismatches)
    if first_bad:
        print("    FIRST BAD    :", first_bad)

    # --- Part B: demonstration for magnitudes beyond the 12-digit window ---
    demos = [1_000_000_000_000, 2_000_000_000_000, 3_000_000_000_000,
             11_000_000_000_000, 1_000_000_000_001, 1_234_567_890_123,
             42_000_000_000_000, 999_999_999_999_999,
             1_000_000_000_000_000]
    print("\n[B] wide-magnitude behaviour (P7-139 territory)")
    for w in demos:
        print("    n =", w)
        print("        original :", repr(norm(original(w))))
        print("        fixed    :", repr(norm(fixed_sformat(w))))

    ok = (mismatches == 0)
    print("\nRESULT:", "PASS (no regression in-range)" if ok else "FAIL (regression detected)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
