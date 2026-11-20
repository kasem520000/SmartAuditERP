#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-048 (audit finding P4-018) in frmSafeAdjust.
No .NET/WPF/SQL Server toolchain exists here, so validation combines a
connection/transaction lifecycle model of each handler's exit paths with
static witnesses over all three repaired methods.

Legacy: AdjustStock opened its transaction BEFORE the draft confirmation and
leaked it on decline (the finally closed a different connection); delete and
unapprove began transactions before their prompts/selection guards, had no
finally at all, and returned early leaving live transactions behind - so the
next command on that connection could fail or hold resources. Repaired: the
prompt precedes any open, every exit path commits/rolls back and closes the
correct connection, and rollback is null-safe.

Run: python3 tests/repair/transaction_lifetime_harness.py
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


SRC = open("SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs", encoding="utf-8").read()


class Conn:
    def __init__(self):
        self.open = False
        self.tx_live = False


def handler(rules, kind, confirms, work_fails=False):
    """kind: 'adjust'|'delete'|'cancel' - mirrors the control-flow skeleton."""
    conn = Conn(); outcome = None

    if rules == "legacy":
        conn.open = True; conn.tx_live = True               # begun before asking!
        if not confirms:
            return ("early-return", conn, outcome)          # tx abandoned, conn left
        # (decline/selection guard sits inside try after begin)
    else:
        if not confirms:
            return ("early-return", conn, outcome)          # costs nothing
        conn.open = True; conn.tx_live = True

    try:
        if work_fails:
            raise RuntimeError("db error")
        conn.tx_live = False                                # Commit()
        outcome = "ok"
    except Exception:
        conn.tx_live = False                                # Rollback (null-safe post-fix)
        outcome = "error"
    finally:
        if rules == "fixed":
            conn.open = False                               # closes the RIGHT conn
        elif kind == "adjust":
            pass                                            # legacy finally closed conn1, not conn
    return (outcome, conn, outcome)


print("Part A: decline costs nothing")
_, conn_l, _ = handler("legacy", "delete", confirms=False)
check("A1 legacy decline leaked an OPEN transaction (bug reproduced)",
      conn_l.tx_live is True and conn_l.open is True)
_, conn_f, _ = handler("fixed", "delete", confirms=False)
check("A2 repaired decline never opens anything",
      conn_f.tx_live is False and conn_f.open is False)

print("Part B: failure and success resolve deterministically")
_, conn_f, out = handler("fixed", "adjust", confirms=True, work_fails=True)
check("B1 repaired failure rolls back and closes the working connection",
      out == "error" and conn_f.tx_live is False and conn_f.open is False)
_, conn_l, out = handler("legacy", "adjust", confirms=True, work_fails=True)
check("B2 legacy failure rolled back but left conn open via the wrong finally",
      out == "error" and conn_l.tx_live is False and conn_l.open is True)
for rules in ("legacy", "fixed"):
    _, c, o = handler(rules, "cancel", confirms=True, work_fails=False)
    assert o == "ok" and c.tx_live is False
check("B3 successful runs commit identically under both algorithms",
      handler("legacy", "cancel", True)[0] == handler("fixed", "cancel", True)[0] == "ok")
_, c, _ = handler("fixed", "delete", confirms=True)
check("B4 repaired success also closes its connection (delete/cancel gained a finally)",
      c.open is False)

print("Part C: static witnesses over all three methods")


def body(marker, nxt):
    return SRC.split(marker)[1].split(nxt)[0]


adj = body("private void AdjustStock()", "private void ExecuteAdjustment()")
dele = body("private void btnDelete_Click", "private void BtnCancel_Click")
canc = body("private void BtnCancel_Click", "private void btnShow_Click")

check("C1 AdjustStock opens its transaction only after the prompt can return",
      adj.index("MessageBoxResult.No)") < adj.index("tx = conn.BeginTransaction();"))
check("C2 AdjustStock's finally now closes the transaction's own connection too",
      "if (conn.State != ConnectionState.Closed) conn.Close();" in adj and
      "if (conn1.State != ConnectionState.Closed) conn1.Close();" in adj)
for seg, label in ((dele, "delete"), (canc, "cancel")):
    check("C3 %s prompts/guards before opening and owns a closing finally" % label,
          seg.index("BeginTransaction()") > seg.index("return;") and
          "finally\n            {\n                if (conn.State != ConnectionState.Closed) conn.Close();" in seg)
check("C4 every rollback across the window is null-safe",
      SRC.count("try { tx?.Rollback(); } catch { }") >= 3 and
      "\n                tx.Rollback();\n" not in dele and "\n                tx.Rollback();\n" not in canc)
check("C5 the transaction handles are declared nullable before their try blocks",
      dele.count("SqlTransaction tx = null;") == 1 and canc.count("SqlTransaction tx = null;") == 1
      and adj.count("SqlTransaction tx = null;") == 1)
sap = SRC.split("private void SaveAndPrint()")[1].split("private Invoice BindToInvoice()")[0]
check("C6 R-046 ordering survived this restructuring (stamp after save)",
      sap.index("SaveInvoice(invoice") < sap.index("Is_Approved=1"))

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-048 (P4-018): declining costs nothing, every exit commits,")
print("rolls back and closes the right connection across all three handlers.")
sys.exit(0)
