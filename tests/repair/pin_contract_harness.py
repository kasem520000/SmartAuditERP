#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-032 (audit finding P2-008), covering its
five client-side sites. No .NET/WPF/SQL Server toolchain exists here, so
validation combines SQLite models of each data flow with static witnesses.

A. Edit-mode PIN uniqueness - duplicates could be created by editing; the
   repaired check runs on add AND edit, excluding the record by its own id.
B. Canonical PIN normalisation - failed parses and fractions used to
   converge accounts onto truncated/zero keys; strict integral validation
   rejects them, while the empty-PIN-with-quick-login-off flow still stores 0.
C. Security panel exactness - a decimal entry no longer truncates into
   another account's identity.
D. Ambiguous match refusal - PIN login matching several rows is refused
   instead of taking row order as identity.
E. Lock parse-failure arm - non-numeric unlock text can no longer compare
   SecureCode=0.

Documented residual (owner-input): unique index/policy on SecureCode in the
schema, attempt limits and offline revocation - not invented here.

Run: python3 tests/repair/pin_contract_harness.py
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


ADDU = open("SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs", encoding="utf-8").read()
SECP = open("SmartAuditERP/Form_WPF/frmSecurityPnl.xaml.cs", encoding="utf-8").read()
LOGIN = open("SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs", encoding="utf-8").read()
LOCK = open("SmartAuditERP/Form_WPF/frmlock.xaml.cs", encoding="utf-8").read()

print("Part A: P2-008(a) - duplicate PIN detection now covers edits")


def fresh():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE Users (id INT, username TEXT, SecureCode TEXT, IS_Deleted INT)")
    db.executemany("INSERT INTO Users VALUES (?,?,?,0)",
                   [(1, "alice", "4321"), (7, "bob", "9999")])
    return db


def dup_blocks(db, rules, code, secure_code):
    if rules == "legacy" and code != -1:
        return False                                   # legacy skipped the check entirely on edit
    rows = db.execute(
        "SELECT id FROM Users WHERE SecureCode=? AND IS_Deleted=0 AND id<>?",
        (secure_code, code)).fetchall()
    return len(rows) > 0


db = fresh()
check("A1 legacy lets an EDIT assign bob alice's PIN (bug reproduced)",
      dup_blocks(db, "legacy", 7, "4321") is False)
check("A2 repaired edit assigning bob alice's PIN is blocked",
      dup_blocks(db, "fixed", 7, "4321") is True)
check("A3 keeping one's own unchanged PIN stays allowed (self excluded by id)",
      dup_blocks(fresh(), "fixed", 1, "4321") is False)
check("A4 adding a genuinely new duplicate is still blocked",
      dup_blocks(fresh(), "fixed", -1, "9999") is True)
check("A5 source applies the check beyond Code==-1 and binds the exclusion id",
      'if (!string.IsNullOrWhiteSpace(txtSecureCode.Text))' in ADDU and
      "and id<>@id" in ADDU and
      '"@id", SqlDbType.Int).Value = Code;' in ADDU)

print("Part B: P2-008(b) - canonical digits only, never silent defaults")


def validate_pin(rules, text, quick_login_on):
    """returns ('ok', stored_int) | ('reject', None) mirroring the save path."""
    t = (text or "").strip()
    if rules == "legacy":
        try:
            val = float(t)                             # double.TryParse analogue
        except ValueError:
            val = 0.0                                  # out param stays 0 on failure
        return ("ok", int(val))                        # cast truncates
    if t:
        try:
            v = int(t)
        except ValueError:
            return ("reject", None)
        if v < 0 or v > 2147483647:
            return ("reject", None)
        return ("ok", v)
    if quick_login_on:
        return ("reject", None)
    return ("ok", 0)


check("B1 legacy turned letters into PIN zero (convergence bug reproduced)",
      validate_pin("legacy", "abc", True) == ("ok", 0))
check("B2 legacy truncated fractions (12.7 -> 12)",
      validate_pin("legacy", "12.7", True) == ("ok", 12))
check("B3 repaired rejects letters and fractions outright",
      validate_pin("fixed", "abc", True)[0] == "reject" and
      validate_pin("fixed", "12.7", True)[0] == "reject")
check("B4 repaired rejects negatives and overflow",
      validate_pin("fixed", "-5", True)[0] == "reject" and
      validate_pin("fixed", "99999999999999", True)[0] == "reject")
check("B5 quick-login enabled requires an actual PIN",
      validate_pin("fixed", "", True)[0] == "reject")
check("B6 empty PIN with quick-login OFF still stores 0 (unchanged legal flow)",
      validate_pin("fixed", "", False) == ("ok", 0) == validate_pin("legacy", "", False))
check("B7 two formerly-converging inputs can no longer share a key",
      validate_pin("fixed", "abc", True)[0] == "reject" or
      validate_pin("fixed", "abc", True)[1] != validate_pin("fixed", "0", False)[1])
check("B8 source validates strictly and keeps both insert/update on the vetted value",
      "long.TryParse(pinText, out pinVal)" in ADDU and
      ",@username,@pwd," + '" + secureCodeInt +' in ADDU and
      ",SecureCode=\" + secureCodeInt +" in ADDU and
      "(int)secureCodeVal" not in ADDU)

print("Part C: P2-008(c) - security panel compares exact integers")


def panel_identity(rules, pwd):
    if rules == "legacy":
        try:
            v = float(pwd)                             # decimal.TryParse then Convert.ToInt32
        except ValueError:
            return None
        return int(v) if 0 <= v <= 1000000 else None
    t = pwd.strip()
    try:
        v = int(t)
    except ValueError:
        return None
    return v if 0 <= v <= 2147483647 else None


check("C1 legacy authenticated 12.7 AS account 12 (bug reproduced)",
      panel_identity("legacy", "12.7") == 12)
check("C2 repaired rejects fraction input before any lookup",
      panel_identity("fixed", "12.7") is None)
check("C3 plain digits behave identically under both rule sets",
      panel_identity("legacy", "0043") == panel_identity("fixed", "0043") == 43)
check("C4 panel source switched decimal-truncation for strict long parse",
      "decimal.TryParse" not in SECP and
      "long.TryParse(pwd.Trim(), out long pin)" in SECP)

print("Part D: P2-008(d) - ambiguous PIN matches are refused")


def pin_login(rules, rows_matched):
    if rules == "fixed" and rows_matched > 1:
        return "refused-ambiguous"
    return "row-order-wins" if rows_matched >= 1 else "no-match"


check("D1 legacy let row ordering decide identity across duplicates (bug reproduced)",
      pin_login("legacy", 2) == "row-order-wins")
check("D2 repaired refuses while duplicates exist",
      pin_login("fixed", 2) == "refused-ambiguous")
check("D3 unique matches log in exactly as before",
      pin_login("legacy", 1) == pin_login("fixed", 1) == "row-order-wins")
check("D4 refusal guard sits before any Rows[0] use on the PIN branch",
      "Type != 1 && dt.Rows.Count > 1" in LOGIN and
      LOGIN.index("Type != 1 && dt.Rows.Count > 1") < LOGIN.index('dt.Rows[0]["emp"]'))

print("Part E: P2-008(e) - lock: failed parse must not mean PIN zero")


def lock_secure_match(rules, password_text, account_pins):
    """account_pins: list of active SecureCode values for MainClass.UserID."""
    if rules == "legacy":
        try:
            v = int(float(password_text))              # TryParse ignored -> numericCode stayed 0
        except ValueError:
            v = 0
        return v in account_pins
    t = password_text.strip()
    try:
        v = int(t)
    except ValueError:
        return False                                   # PIN arm skipped entirely
    if v < 0 or v > 2147483647:
        return False
    return v in account_pins


check("E1 legacy unlocked with garbage text when the account PIN was 0 (bug reproduced)",
      lock_secure_match("legacy", "not-a-pin", [0]) is True)
check("E2 repaired ignores the PIN arm for non-integral text",
      lock_secure_match("fixed", "not-a-pin", [0]) is False)
check("E3 correct PINs still unlock identically",
      lock_secure_match("legacy", "4321", [4321]) ==
      lock_secure_match("fixed", "4321", [4321]) is True)
check("E4 lock source gates the SecureCode query behind successful parsing",
      "long.TryParse(passwordText.Trim(), out long unlockPin)" in LOCK and
      LOCK.index("long.TryParse(passwordText.Trim()") < LOCK.index("SecureCode={(int)unlockPin}"))

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-032 (P2-008 client-side contract): duplicates caught on")
print("edit, identity keys are canonical digits only, panels compare exactly,")
print("ambiguous PIN matches refuse rather than pick, and unlock garbage can")
print("never equal PIN zero. Schema uniqueness/attempts policy remains owner-input.")
sys.exit(0)
