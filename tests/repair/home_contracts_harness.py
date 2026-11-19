#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-018 (P1-026), R-021 (P1-030),
R-022 (P1-031), R-023 (P1-025) and R-024 (P1-018). These are UI/connection/
metadata-contract repairs whose runtime surface cannot be executed in this
sandbox (no .NET/WPF/DevExpress), so validation combines:

* behavioural MINI-MODELS where the logic is self-contained enough to mirror
  faithfully (release-asset selection over GitHub-style JSON; cached-window
  reopen semantics);
* STATIC WITNESSES pinning each repaired construct in the actual sources,
  including absence checks for the exact defective patterns.

Run: python3 tests/repair/home_contracts_harness.py
Exit 0 on PASS.
"""
import json
import re
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


HOME = open("SmartAuditERP/Home.xaml.cs", encoding="utf-8").read()
LOGIN = open("SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs", encoding="utf-8").read()
SRVSET = open("SmartAuditERP/Form_WPF/frmServerSetting.xaml.cs", encoding="utf-8").read()
FRMUPD = open("SmartAuditERP/Form_WPF/FrmUpdate.xaml.cs", encoding="utf-8").read()

# ------------------- Part A: R-023 / P1-025 asset selection ------------------
print("Part A: R-023 / P1-025 - one deterministic package per release")


def select_zip_asset(payload):                       # mirror of SelectZipAsset
    try:
        assets = payload.get("assets")
        if not isinstance(assets, list):
            return None
        for a in assets:
            name = (a or {}).get("name", "") or ""
            if name.lower().endswith(".zip"):
                return a
        return None
    except Exception:
        return None


def extract_url(p):
    a = select_zip_asset(p)
    return (a or {}).get("browser_download_url", "") or ""


def extract_name(p):
    a = select_zip_asset(p)
    return (a or {}).get("name") or "update_SmartAuditERP.zip"


def extract_size(p):
    a = select_zip_asset(p)
    try:
        return int((a or {}).get("size", 0))
    except (TypeError, ValueError):
        return 0


REL_MULTI = {
    "tag_name": "v9.9",
    "assets": [
        {"name": "checksums.sha256", "size": 512,
         "browser_download_url": "https://x/checksums.sha256"},
        {"name": "guide.pdf", "size": 900000,
         "browser_download_url": "https://x/guide.pdf"},
        {"name": "update_SmartAuditERP.zip", "size": 42424242,
         "browser_download_url": "https://x/update_SmartAuditERP.zip"},
        {"name": "extra_bundle.bin", "size": 7,
         "browser_download_url": "https://x/extra_bundle.bin"},
    ],
}
check("A1 multi-attachment release selects the ZIP's url (not the first asset)",
      extract_url(REL_MULTI) == "https://x/update_SmartAuditERP.zip")
check("A2 name and size describe that SAME zip asset",
      extract_name(REL_MULTI) == "update_SmartAuditERP.zip"
      and extract_size(REL_MULTI) == 42424242)

REL_REORDERED = dict(REL_MULTI, assets=list(reversed(REL_MULTI["assets"])))
check("A3 selection independent of attachment order",
      extract_url(REL_REORDERED) == extract_url(REL_MULTI))

REL_NOASSETS = {"tag_name": "v1"}
check("A4 missing assets -> safe fallbacks, no crash",
      extract_url(REL_NOASSETS) == "" and extract_name(REL_NOASSETS) ==
      "update_SmartAuditERP.zip" and extract_size(REL_NOASSETS) == 0)

REL_CASE = {"assets": [{"name": "PKG.ZIP", "size": "15",
                        "browser_download_url": "u"}]}
check("A5 case-insensitive .zip match and numeric-coercible size",
      extract_url(REL_CASE) == "u" and extract_size(REL_CASE) == 15)

check("A6 C# sources use the typed selector for all three fields",
      HOME.count("SelectZipAsset(json)") >= 3 and
      'json.IndexOf(key)' not in HOME.split("private Newtonsoft.Json.Linq.JToken SelectZipAsset")[1][:200])
check("A7 IndexOf scraping remnants removed from the extractor region",
      'int keyIdx = json.IndexOf(key);' not in HOME and
      'int assetsIdx = json.IndexOf("\\"assets\\"");' not in HOME)

# ------------------- Part B: R-021 / P1-030 window cache ---------------------
print("Part B: R-021 / P1-030 - closed windows never shown again")


class Window:                                      # minimal WPF-window contract
    def __init__(self, kind):
        self.kind = kind
        self.closed = False
        self.shown_count = 0

    def Show(self):
        if self.closed:                            # WPF throws here
            raise RuntimeError("InvalidOperationException: cannot Show a closed Window")
        self.shown_count += 1

    def Close(self):
        self.closed = True


class LegacyCache:
    def __init__(self, kind):
        self._ref = None
        self.kind = kind

    @property
    def win(self):
        if self._ref is None:
            self._ref = Window(self.kind)
        return self._ref


class FixedCache:
    def __init__(self, kind):
        self._ref = None
        self.kind = kind

    def _create(self):
        w = Window(self.kind)
        original_close = w.Close

        def close_hook():
            original_close()
            self._ref = None                       # Closed => drop the reference
        w.Close = close_hook
        return w

    @property
    def win(self):
        if self._ref is None:
            self._ref = self._create()
        return self._ref


for CacheCls, label in ((LegacyCache, "legacy"), (FixedCache, "fixed")):
    c = CacheCls("treasury")
    c.win.Show(); c.win.Close()
    crashed = False
    try:
        c.win.Show()                               # reopen after close
    except RuntimeError:
        crashed = True
    if label == "legacy":
        check("B1 legacy cache throws InvalidOperationException on reopen (bug reproduced)",
              crashed)
    else:
        check("B2 fixed cache transparently constructs a fresh instance",
              not crashed and c.win.shown_count == 1 and not c.win.closed)

check("B3 both Home caches subscribe to Closed and null their reference",
      HOME.count("f.Closed += (s, e) => { _frmAccountsTree = null; };") == 1 and
      HOME.count("f.Closed += (s, e) => { _frmTreasury = null; };") == 1)
check("B4 lazy accessors route through the hooked factories",
      "_frmAccountsTree ?? (_frmAccountsTree = CreateAccountsTree())" in HOME and
      "_frmTreasury ?? (_frmTreasury = CreateTreasury())" in HOME)
check("B5 old unhooked construction pattern is gone",
      "(_frmAccountsTree = new frmAccountsTree())" not in HOME and
      "(_frmTreasury = new frmTreasury())" not in HOME)

# ------------------- Part C: R-022 / P1-031 log connection --------------------
print("Part C: R-022 / P1-031 - audit-log login identity")
m = re.search(r'if \(MainClass\.Conn_type == 2\)\s*\{[^}]*connectionString = '
              r'"server=" \+ MainClass\.Server \+ ";database=" \+ MainClass\.Database '
              r'\+ ";user id=" \+ (MainClass\.\w+) \+ ";pwd=" \+ MainClass\.NetPwd;',
              HOME, re.S)
check("C1 conn_type==2 log connection now uses the login identity",
      m is not None and m.group(1) == "MainClass.NetUserId",
      m.group(1) if m else "pattern missing")
check("C2 database-name-as-user defect removed",
      '";user id=" + MainClass.Database + ";pwd="' not in HOME)

# ------------------- Part D: R-024 / P1-018 SQL auth honoured -----------------
print("Part D: R-024 / P1-018 - configured SQL Authentication takes effect")


def build_login_conn(conn_type, use_server_auth, net_user):   # model of the load path
    sql_auth = conn_type == 2 or (use_server_auth and bool(net_user))
    return "SQLAUTH" if sql_auth else "TRUSTED"


check("D1 terminal mode still sql-auth", build_login_conn(2, False, "") == "SQLAUTH")
check("D2 local WITHOUT server auth stays trusted (unchanged default)",
      build_login_conn(1, False, "") == "TRUSTED")
check("D3 local WITH opted-in server auth now sql-auth (the fix)",
      build_login_conn(1, True, "svc_login") == "SQLAUTH")
check("D4 empty stored user does not half-enable sql-auth",
      build_login_conn(1, True, "") == "TRUSTED")

check("D5 login source gates on UseServerAuth && NetUserid",
      "(MainClass.UseServerAuth && !string.IsNullOrEmpty(NetUserid))" in LOGIN and
      "bool useSqlAuth = conn_type == 2 ||" in LOGIN)
check("D6 server-settings local branch honours chkServerAuth",
      "chkServerAuth.IsChecked == true" in SRVSET and
      "user id={txtUser.Text}; pwd={txtPWD.Password};" in SRVSET)

# ------------------- Part E: R-018 / P1-026 legacy updater ---------------------
print("Part E: R-018 / P1-026 - completion follows verified results")
check("E1 async outcome checked before replacement",
      "if (ev.Error != null)" in FRMUPD and "if (ev.Cancelled)" in FRMUPD and
      FRMUPD.index("if (ev.Error != null)") < FRMUPD.index("if (!ReplaceFiles()) return;"))
check("E2 ReplaceFiles reports success/failure",
      "private bool ReplaceFiles()" in FRMUPD and "return false;" in FRMUPD)
check("E3 manual path guards page advance on the result",
      "proceed = ReplaceFiles();" in FRMUPD and "if (!proceed) return;" in FRMUPD)
check("E4 license-date side effect left untouched for P1-032 policy work",
      "UpdateLicenseEndDate();" in FRMUPD)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS[:40]:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-018/R-021/R-022/R-023/R-024 contracts hold: releases")
print("select one deterministic package, closed windows respawn instead of")
print("throwing, the audit log connects with the real login, SQL auth flags")
print("are honoured, and legacy-update completion follows verified results.")
sys.exit(0)
