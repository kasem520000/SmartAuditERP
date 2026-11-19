#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-014 (audit finding P1-009) and
R-015 (P1-011). No .NET toolchain exists here, so the repaired C# paths are
modelled faithfully and, for the SQL surface, exercised against SQLite:

Part A - R-014 / P1-009 (StartupData.json secrets vs the Remember option):
  The write path used to persist the app password and SQL credentials every
  time; Remember controlled only screen REFILL on load. Model both the writer
  (legacy vs repaired) and the documented reader (UseServerAuth derived from a
  non-empty ServerUserName; password box refilled only when Remember) and
  prove: opted-in payloads stay byte-identical; opted-out payloads carry no
  recoverable secret and no longer re-arm server auth on next launch; all
  non-secret metadata is untouched.

Part B - R-015 / P1-011 (credential paths concatenated into SQL):
  Replays the four repaired credential sites (password change, unlock check,
  operation-permission check, user uniqueness checks) as legacy interpolated
  SQL versus typed-parameter SQL against an in-memory SQLite database:
  * legitimate text containing an apostrophe used to break the statement;
    now it stores/compares as data;
  * the classic tautology used to UNLOCK or validate a permission without a
    matching secret; now it matches nothing;
  * ordinary behaviour (correct password accepted, wrong rejected, real
    duplicates detected, unique names pass) is unchanged.
  Static witnesses additionally pin that the parametrised statements exist in
  the edited sources and the former interpolations are gone.

Run: python3 tests/repair/credential_safety_harness.py
Exit 0 on PASS.
"""
import json
import re
import sqlite3
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


# --------------------------- PART A: R-014 ---------------------------------
print("Part A: R-014 / P1-009 - secrets honour the Remember choice")

META = dict(ConnType="1", Server="srv01", DatabaseName="company_db", Branch="2",
            UserName="cashier1", Language="0")


def legacy_write(remember, app_pwd, net_user, net_pwd, conn_type, use_server_auth):
    d = dict(META, Remember=remember, UserName=META["UserName"],
             Password=app_pwd, ServerUserName="", ServerPassword="")
    if conn_type == 1 and use_server_auth:
        d.update(ServerUserName=net_user, ServerPassword=net_pwd)
    if conn_type == 2:
        d.update(ServerUserName=net_user, ServerPassword=net_pwd)
    return d


def fixed_write(remember, app_pwd, net_user, net_pwd, conn_type, use_server_auth):
    d = legacy_write(remember, app_pwd, net_user, net_pwd, conn_type, use_server_auth)
    if not remember:
        d.update(Password="", ServerUserName="", ServerPassword="")
    return d


def read_path(file_payload):
    """Mirrors frmUserLogin load: UseServerAuth from non-empty ServerUserName;
    refill/clear according to Remember."""
    use_server_auth = bool(file_payload.get("ServerUserName"))
    if file_payload.get("Remember"):
        ui_pwd = file_payload.get("Password", "")
    else:
        ui_pwd = ""
    armed_net_pwd = file_payload.get("ServerPassword") if use_server_auth else None
    return use_server_auth, ui_pwd, armed_net_pwd


for ct, usa in ((1, True), (1, False), (2, True)):
    scen = "conn_type=%s/use_server_auth=%s" % (ct, usa)
    # Opted IN: repaired writer must equal legacy (no regression).
    li = legacy_write(True, "S3cret!", "sa_acc", "NetP@ss", ct, usa)
    fi = fixed_write(True, "S3cret!", "sa_acc", "NetP@ss", ct, usa)
    check("A1 remember=true payload unchanged (%s)" % scen, li == fi,
          "%r vs %r" % (li, fi))

    # Opted OUT: legacy leaks; repair removes every recoverable secret.
    lo = legacy_write(False, "S3cret!", "sa_acc", "NetP@ss", ct, usa)
    fo = fixed_write(False, "S3cret!", "sa_acc", "NetP@ss", ct, usa)
    leak = "S3cret!" in json.dumps(lo, ensure_ascii=False) or \
           ("NetP@ss" in json.dumps(lo, ensure_ascii=False) if (ct == 2 or usa) else False)
    check("A2 legacy reproduces the leak when remembered=false (%s)" % scen,
          leak or ct == 1 and not usa)      # the sql-auth branch is off only here
    clean = "S3cret!" not in json.dumps(fo, ensure_ascii=False) and \
            "NetP@ss" not in json.dumps(fo, ensure_ascii=False)
    check("A3 repaired file carries no recoverable secret (%s)" % scen, clean, repr(fo))

    usa_l, ui_l, arm_l = read_path(lo)
    usa_f, ui_f, arm_f = read_path(fo)
    if ct == 2 or usa:
        check("A4 legacy next launch still arms server creds despite opt-out (%s)" % scen,
              arm_l == "NetP@ss")
        check("A5 repaired next launch does NOT re-arm them (%s)" % scen,
              arm_f is None and usa_f is False)
    check("A6 password box stays empty either way when Remember=false (%s)" % scen,
          ui_l == "" and ui_f == "")

    # Non-secret metadata identical between writers in BOTH modes.
    keys = sorted(k for k in META)
    check("A7 connection metadata untouched (%s)" % scen,
          [lo[k] for k in keys] == [fo[k] for k in keys] ==
          [legacy_write(True, "x", "u", "p", ct, usa)[k] for k in keys])

src_login = open("SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs", encoding="utf-8").read()
check("A8 C# gates the app password on Remember",
      'Password = remember ? txtPwd.Password : ""' in src_login)
check("A9 C# gates both server-auth blocks on Remember",
      src_login.count("if (remember && conn_type == ") == 2)
check("A10 C# keeps non-secret writes unconditional",
      'Server = MainClass.Server,' in src_login and 'UserName = txtUser.Text,' in src_login)

# --------------------------- PART B: R-015 ---------------------------------
print("Part B: R-015 / P1-011 - credential paths as data, never as SQL")


def seed():
    db = sqlite3.connect(":memory:")
    db.executescript("""
      CREATE TABLE Users (id INT, emp INT, username TEXT, pwd TEXT,
                          SecureCode TEXT, LoginSecode INT, IS_Deleted INT);
      INSERT INTO Users VALUES (101,5,'ahmed','secret','1234',1,0),
                               (102,6,'bashir','other','5678',1,0);
      CREATE TABLE OperationPermission (id INT, pwd TEXT, OperNo INT,
                                        IS_Deleted INT, lastChanged TEXT);
      INSERT INTO OperationPermission VALUES (1,'permSecret',42,0,'2026-01-01');
    """)
    return db


def runs(db, sql, params=None):
    cur = db.cursor()
    cur.execute(sql, params or ())
    try:
        rows = cur.fetchall()
    except sqlite3.Error:
        rows = None
    db.commit()
    return rows


EMP = 5

# B1. Password change: apostrophe legitimacy + single-row scope.
db = seed()
apostrophe_pwd = "o'brien"
raised = False
try:
    runs(db, "UPDATE Users SET pwd = '%s' WHERE emp = %d" % (apostrophe_pwd, EMP))
except sqlite3.Error:
    raised = True
check("B1a legacy UPDATE breaks on a legitimate apostrophe password", raised)

db = seed()
runs(db, "UPDATE Users SET pwd = ? WHERE emp = ?", (apostrophe_pwd, EMP))
got = runs(db, "SELECT pwd FROM Users WHERE emp=?", (EMP,))[0][0]
untouched = runs(db, "SELECT pwd FROM Users WHERE emp=6")[0][0]
check("B1b parametrised UPDATE stores the apostrophe password verbatim",
      got == apostrophe_pwd, repr(got))
check("B1c other users untouched by the parametrised UPDATE", untouched == "other")

inj = "x', IS_Deleted=1 WHERE '1'='1"
db = seed()
runs(db, "UPDATE Users SET pwd = ? WHERE emp = ?", (inj, EMP))
deleted_any = runs(db, "SELECT COUNT(*) FROM Users WHERE IS_Deleted=1")[0][0]
stored = runs(db, "SELECT pwd FROM Users WHERE emp=?", (EMP,))[0][0]
check("B1d injected text cannot reshape the statement (rows intact)",
      deleted_any == 0 and stored == inj)

# B2. Unlock check: the audited tautology bypass.
attack = "' OR '1'='1"
db = seed()
old_rows = runs(db, "select * from Users where emp=%d and pwd='%s'" % (EMP, attack))
check("B2a legacy unlock predicate bypassed by tautology (bug reproduced)",
      len(old_rows) > 0)
new_rows = runs(db, "select * from Users where emp=? and pwd=?", (EMP, attack))
check("B2b parametrised unlock rejects the tautology", len(new_rows) == 0)
benign_old = runs(db, "select * from Users where emp=%d and pwd='%s'" % (EMP, "secret"))
benign_new = runs(db, "select * from Users where emp=? and pwd=?", (EMP, "secret"))
check("B2c correct password still unlocks identically",
      len(benign_old) == len(benign_new) == 1)
wrong_new = runs(db, "select * from Users where emp=? and pwd=?", (EMP, "nope"))
check("B2d wrong password still rejected", len(wrong_new) == 0)

# B3. Operation permission check: same tautology class.
db = seed()
old_perm = runs(db, "SELECT id,lastChanged FROM OperationPermission "
                    "WHERE IS_Deleted=0 AND pwd='%s' AND OperNo=%d" % ("' OR 1=1 --", 42))
check("B3a legacy permission check bypassed (bug reproduced)", len(old_perm) > 0)
new_perm = runs(db, "SELECT id,lastChanged FROM OperationPermission "
                    "WHERE IS_Deleted=0 AND pwd=? AND OperNo=?", ("' OR 1=1 --", 42))
check("B3b parametrised permission check refuses it", len(new_perm) == 0)
ok_perm = runs(db, "SELECT id,lastChanged FROM OperationPermission "
                   "WHERE IS_Deleted=0 AND pwd=? AND OperNo=?", ("permSecret", 42))
check("B3c genuine permission password still validates", len(ok_perm) == 1)

# B4. Username/secure-code uniqueness checks keep working, minus injection.
# (The T-SQL N'...' prefix has no SQLite equivalent; the injection semantics
# being modelled are identical without it.)
db = seed()
dup_old = runs(db, "select emp from Users where username='%s' and IS_Deleted=0" % "ahmed")
dup_new = runs(db, "select emp from Users where username=? and IS_Deleted=0", ("ahmed",))
check("B4a existing duplicate still detected by parametrised check",
      len(dup_old) == len(dup_new) == 1)
free_new = runs(db, "select emp from Users where username=? and IS_Deleted=0", ("new_name",))
check("B4b genuinely free username still passes", len(free_new) == 0)
taut_old = runs(db, "select emp from Users where username='%s' and IS_Deleted=0"
                % "' OR '1'='1")
taut_new = runs(db, "select emp from Users where username=? and IS_Deleted=0",
                ("' OR '1'='1",))
check("B4c tautology username matched everyone before, nobody now",
      len(taut_old) == 2 and len(taut_new) == 0)
sc_new = runs(db, "select id from Users where SecureCode=? and IS_Deleted=0", ("1234",))
check("B4d secure-code duplicate still detected", len(sc_new) == 1)
edit_new = runs(db, "select id from Users where emp<>? and username=? and IS_Deleted=0",
                (5, "bashir"))
check("B4e edit-mode self-exclusion still holds", len(edit_new) == 1)

# B5. Static witnesses in the edited sources.
WITNESS = [
    ("SmartAuditERP/Form_WPF/frmChangePwd.xaml.cs",
     ["UPDATE Users SET pwd = @pwd WHERE emp = @emp",
      'changeCmd.Parameters.Add("@pwd", SqlDbType.NVarChar).Value = txtPass.Password;'],
     ['SET pwd = \'{txtPass.Password}\'']),
    ("SmartAuditERP/Form_WPF/frmlock.xaml.cs",
     ["select * from Users where emp=@emp and pwd=@pwd"],
     ["pwd='{passwordText}'"]),
    ("SmartAuditERP/Form_WPF/frmCheckPwd.xaml.cs",
     ["WHERE IS_Deleted = 0 AND pwd = @pwd AND OperNo = @operNo"],
     ["AND pwd = '{enteredPassword}'"]),
    ("SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs",
     ["where username=@username and IS_Deleted=0",
      "where SecureCode=@secureCode and IS_Deleted=0",
      # R-029 (P2-007) moved the edit-mode exclusion from emp to the record's own id;
      # parameterisation (the property this witness guards) is unchanged.
      "where id<>@code and username=@username and IS_Deleted=0"],
     ["username=N'", "SecureCode=N'",
      # must not regress to excluding by emp while @code holds a Users.id (P2-007).
      "where emp<>@code and username=@username"]),
]
for path, needs, gones in WITNESS:
    s = open(path, encoding="utf-8").read()
    for n in needs:
        check("B5 present in %s: %s" % (path.split('/')[-1], n[:42]), n in s)
    for g in gones:
        check("B5 removed from %s: %s" % (path.split('/')[-1], g[:42]), g not in s)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS[:40]:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-014 (P1-009): opted-out logins leave no recoverable")
print("secrets and do not re-arm server auth; opted-in payloads unchanged.")
print("R-015 (P1-011): credential inputs behave as data on all four repaired")
print("paths; tautology bypasses reproduce pre-fix and fail post-fix while")
print("ordinary authentication/uniqueness behaviour is unchanged.")
sys.exit(0)
