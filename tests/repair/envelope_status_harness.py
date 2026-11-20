#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-057 (audit finding P5-027) and R-058
(P5-010). No .NET/MQTT/SQL Server toolchain exists here, so each repair is
validated as a behavioural model of its exact contract plus static witnesses
over the repaired code.

Run: python3 tests/repair/envelope_status_harness.py
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


RECVD = open("SmartAuditERP/Class/ReceivedData.cs", encoding="utf-8").read()
ENTRIES = open("SmartAuditERP/Form_WPF/frmEntriesSyncStatus.xaml.cs", encoding="utf-8").read()
RECEIPTS = open("SmartAuditERP/Form_WPF/frmReceiptsSyncStatus.xaml.cs", encoding="utf-8").read()

print("Part A: R-058 / P5-010 - only the leading envelope copy is stripped")
PASSCODE = "SEC123"


def publisher(json_text):                                    # SendData.Concat(str0=passcode, str1=json)
    return PASSCODE + json_text


def receive(rules, wire_plain):                              # models what follows DecryptString(...)
    if rules == "legacy":
        return wire_plain.replace(PASSCODE, "")              # global, anywhere in the payload
    # StripPasscodeEnvelope: one explicit leading copy only
    if PASSCODE and wire_plain.startswith(PASSCODE):
        return wire_plain[ len(PASSCODE):]
    return wire_plain


normal = '[{"name":"محل النور","barcode":"622001"}]'
check("A1 ordinary envelopes decode identically under both rules",
      receive("legacy", publisher(normal)) == receive("fixed", publisher(normal)) == normal)
tainted = '[{"name":"فرع SEC123 الشمالي","note":"تسليم SEC123"}]'
leg = receive("legacy", publisher(tainted))
fix = receive("fixed", publisher(tainted))
check("A2 legacy ate the sequence out of real values (bug reproduced)",
      leg == '[{"name":"فرع  الشمالي","note":"تسليم "}]')
check("A3 repaired handler returns the payload byte-exact", fix == tainted)
key_like = '[{"id":"SEC123","qty":4}]'
check("A4 an identifier EQUAL to the passcode survived where legacy blanked it",
      receive("legacy", publisher(key_like)) == '[{"id":"","qty":4}]' and
      receive("fixed", publisher(key_like)) == key_like)
no_prefix = '[{"x":1}]'
check("A5 messages lacking the prefix pass through untouched (legacy tolerance kept)",
      receive("fixed", no_prefix) == no_prefix == receive("legacy", no_prefix))

helper = RECVD.split("private static string StripPasscodeEnvelope(string decrypted)")[1][:600]
sites = RECVD.count("cipherText = ReceivedData.StripPasscodeEnvelope(")
check("A6 the three handlers call the prefix-stripping helper and the global Replace is gone",
      sites == 3 and
      "decrypted.StartsWith(ReceivedData._passcode)" in helper and
      "return decrypted.Substring(ReceivedData._passcode.Length);" in helper and
      '.Replace(ReceivedData._passcode, "")' not in RECVD)

print("Part B: R-057 / P5-027 - the entries screen stamps delivered rows only")


def entries_run(rules, rows, broker_ok, api_ok):
    """rows: list of (gid, bindable); returns stamped set seen in Entry.Sync."""
    stamped = set()
    entries_to_sync = []
    for gid, bindable in rows:
        if not gid:
            continue
        broker_sent = False
        if broker_ok and bindable:                            # CheckConnectionAndBroker gate
            broker_sent = True                                # both publishes went out
        if rules == "legacy":
            stamped.add(gid)                                  # unconditional pre-stamp per row
        elif broker_sent:
            stamped.add(gid)
        if bindable:
            entries_to_sync.append(gid)
    if api_ok and entries_to_sync:                            # PostEntries success echo
        stamped.update(entries_to_sync)                       # same under both rules
    return stamped


rows = [("g1", True), ("g2", True), ("g3", False)]
check("B1 legacy declared every selected row synced though nothing was delivered (bug)",
      entries_run("legacy", rows, broker_ok=False, api_ok=False) == {"g1", "g2", "g3"})
check("B2 repaired run with all channels down keeps every row Pending",
      entries_run("fixed", rows, broker_ok=False, api_ok=False) == set())
check("B3 broker delivery alone stamps exactly the published rows (unbindable excluded)",
      entries_run("fixed", rows, broker_ok=True, api_ok=False) == {"g1", "g2"})
check("B4 API success stamps its posted set regardless of broker state",
      entries_run("fixed", rows, broker_ok=False, api_ok=True) == {"g1", "g2"})

m = ENTRIES.split("private async void btnSync_Click")[1].split("UpdateEntrySyncStatus(string globalId")[0]
first_guard = m.index("if (brokerSent)")
first_stamp = m.index("UpdateEntrySyncStatus(entryGlobalId, true);")
check("B5 the in-loop stamp sits inside the delivery guard; the API-success stamp survives",
      first_guard < first_stamp and
      "brokerSent = true;" in m and
      m.count("UpdateEntrySyncStatus(") >= 2 and
      "UpdateEntrySyncStatus(postedEntry.EntryGlobalID, true);" in m)

print("Part C: R-057 / P5-027 - the receipts screen stamps after the result")


def receipts_run(rules, gids, broker_ids, api_throws, api_enabled):
    """returns (stamped_set, announced_success)."""
    api_accepted = False
    if api_enabled:
        if api_throws:
            if rules == "fixed":
                api_accepted = False                          # caught + warned
            else:
                pass                                          # legacy: exceptions also skipped await aftermath
        else:
            api_accepted = True
    if rules == "legacy":
        stamped = set(gids)                                   # every selected receipt, before any result
        announced = True                                      # unconditional success toast
        return stamped, announced
    stamped = {g for g in gids if g in broker_ids or api_accepted}
    return stamped, len(stamped) > 0


gids = ["r1", "r2", "r3"]
check("C1 legacy stamped everything and cheered with zero working channels (bug)",
      receipts_run("legacy", gids, set(), api_throws=False, api_enabled=False) == (set(gids), True))
check("C2 repaired run announces honestly and changes nothing without a channel",
      receipts_run("fixed", gids, set(), False, False) == (set(), False))
check("C3 a rejected API (throw) contributes no stamps",
      receipts_run("fixed", gids, set(), True, True) == (set(), False))
check("C4 transport acceptance stamps the batch; broker ids add per-receipt granularity",
      receipts_run("fixed", gids, {"r2"}, False, True) == (set(gids), True) and
      receipts_run("fixed", gids, {"r2"}, True, True) == ({"r2"}, True))

post_i = RECEIPTS.index("await receiptCRUD.PostReceipts(list);")
stamp_i = RECEIPTS.index("UPDATE receipts SET Sync=1 WHERE GlobalID=N'{receipt.GlobalID}'")
check("C5 the await now PRECEDES the status writes and the grid flag follows the stamp set",
      post_i < stamp_i and
      "bool apiAccepted = false;" in RECEIPTS and
      "if (!(brokerSentIds.Contains(receipt.GlobalID) || apiAccepted))" in RECEIPTS and
      "if (!stampedIds.Contains(row.DgvGlobalID))" in RECEIPTS and
      "لم يُسلم أي سند عبر القنوات المتاحة؛ بقيت الحالات دون تغيير." in RECEIPTS)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - envelopes keep their payload intact and sync stamps follow delivery.")
sys.exit(0)
