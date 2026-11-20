#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-050 (audit finding P5-003), R-051 (P5-014)
and R-052 (P5-017). No .NET/MQTT/broker/SQL Server toolchain exists here, so
each repair is validated as a behavioural model of its exact contract plus
static witnesses over the repaired code.

R-050/P5-003: the offline item queue was written with key 'itemid' but read
through a different type's '.id', so every replay carried id 0 until the
queue was cleared. The reader now binds the writer's real contract.
R-051/P5-014: the serial existence probe keyed on the row id instead of the
item id; it now probes the natural identity the insert establishes.
R-052/P5-017: the periodic definitions sync ran only while its timestamp
was fresh; the due comparison is now horizon-correct.

Run: python3 tests/repair/sync_contract_harness.py
Exit 0 on PASS.
"""
import json
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


SENDDATA = open("SmartAuditERP/Class/SendData.cs", encoding="utf-8").read()
RECEIVED = open("SmartAuditERP/Class/ReceivedData.cs", encoding="utf-8").read()
SYNC = open("SmartAuditERP/Class/Sync.cs", encoding="utf-8").read()

print("Part A: R-050 / P5-003 - the queue round-trip keeps the identity")


class ItemIdOff:                                        # writer's model (verbatim shape)
    def __init__(self, itemid):
        self.itemid = itemid


class ListItems:                                        # legacy reader's model
    def __init__(self):
        self.id = None                                  # never populated from {"itemid": ...}


def writer_payload(ids):
    return json.dumps([{"itemid": i} for i in ids])     # frmItems.AddItemLocally output


def reader(rules, payload):
    """returns the published item ids and whether the file was then cleared."""
    sent = []
    rows = json.loads(payload)
    for raw in rows:
        if rules == "legacy":
            obj = ListItems()                           # bound to the wrong type
            obj.id = raw.get("id")                      # key absent -> stays None
            item_id = obj.id if obj.id is not None else 0
        else:
            obj = ItemIdOff(raw["itemid"])              # binds the writer's key
            item_id = obj.itemid
            if item_id <= 0:                            # skip non-positive identities
                continue
        sent.append(item_id)
    cleared = True                                      # File.WriteAllText(empty) always ran
    return sent, cleared


sent_l, cleared_l = reader("legacy", writer_payload([7]))
check("A1 legacy replay published id 0 AND wiped the queue (bug reproduced)",
      sent_l == [0] and cleared_l is True)
sent_f, _ = reader("fixed", writer_payload([7]))
check("A2 repaired replay carries the true queued identity", sent_f == [7])
check("A3 multiple queued items all survive the round trip in order",
      reader("fixed", writer_payload([3, 9, 11]))[0] == [3, 9, 11])
check("A4 zero/negative payloads are skipped, never published",
      reader("fixed", writer_payload([0, -4, 5]))[0] == [5])

m = SENDDATA.split("public static void SendStoredItems()")[1].split("InvGlobalID.json")[0]
check("A5 the reader now binds ItemIdOff/itemid and guards positivity",
      "JsonConvert.DeserializeObject<List<ItemIdOff>>(value)" in m and
      "item_ID = item.itemid;" in m and "if (item_ID <= 0)" in m and
      "item_ID = item.id;" not in m and
      "DeserializeObject<List<ListItems>>(value)" not in m)

print("Part B: R-051 / P5-014 - the probe matches the established identity")


def upsert(rules, table, incoming):
    """incoming: dict(Id=row-key, ItemId, SerialNo); mirrors the three statements."""
    probe_itemid = incoming["Id"] if rules == "legacy" else incoming["ItemId"]
    exists = any(r["ItemId"] == probe_itemid and r["SerialNo"] == incoming["SerialNo"]
                 for r in table)
    if exists:
        for r in table:                                 # UPDATE ... WHERE Id=@Id
            if r["Id"] == incoming["Id"]:
                r.update(incoming)
        return "updated"
    table.append(dict(incoming))                        # INSERT
    return "inserted"


tbl = [{"Id": 1, "ItemId": 42, "SerialNo": "SN-9"}]
verdict = upsert("legacy", tbl, {"Id": 1, "ItemId": 42, "SerialNo": "SN-9"})
check("B1 legacy classified a stored serial as absent and re-inserted it (bug)",
      verdict == "inserted" and len(tbl) == 2)
tbl = [{"Id": 1, "ItemId": 42, "SerialNo": "SN-9"}]
verdict = upsert("fixed", tbl, {"Id": 1, "ItemId": 42, "SerialNo": "SN-9"})
check("B2 repaired replay of the same message converges on the update branch",
      verdict == "updated" and len(tbl) == 1)
tbl = [{"Id": 1, "ItemId": 42, "SerialNo": "SN-9"}]
verdict = upsert("fixed", tbl, {"Id": 99, "ItemId": 42, "SerialNo": "SN-9"})
check("B3 a fresh row id for an existing natural key updates nothing, inserts nothing",
      verdict == "updated" and len(tbl) == 1)

ins = RECEIVED.split("public static void InsertItemSerialNo")[1]
ins = ins[: ins.index("public static")]                    # the whole method body only
probe_i = ins.index('sqlCommand.Parameters.AddWithValue("@ItemId", itemSerialNo.ItemId);')
upd_i = ins.index("UPDATE ItemSerialNo SET")
check("B4 probe and insert now share one ItemId source; UPDATE-by-Id unchanged",
      ins.count('sqlCommand.Parameters.AddWithValue("@ItemId", itemSerialNo.ItemId);') == 1 and
      'sqlCommand.Parameters.AddWithValue("@ItemId", itemSerialNo.Id);' not in ins and
      probe_i < upd_i and
      'sqlCommand2.Parameters.AddWithValue("@Id", itemSerialNo.Id);' in ins)

print("Part C: R-052 / P5-017 - catch-up fires when due")


def due(rules, last_sync_hour, now_hour, interval=2.0):
    """True when a cards-sync cycle starts under each predicate."""
    if rules == "legacy":
        return (last_sync_hour + interval) >= now_hour   # fresh-only window
    return (last_sync_hour + interval) <= now_hour       # reached/passed horizon


check("C1 legacy synced right after success but stalled once stale (bug reproduced)",
      due("legacy", 0.0, 0.5) is True and due("legacy", 0.0, 5.0) is False)
check("C2 repaired schedule waits for the horizon, then catches up however late",
      due("fixed", 0.0, 0.5) is False and due("fixed", 0.0, 5.0) is True)
check("C3 exactly-at-the-horizon fires (boundary inclusive both ways at equality)",
      due("fixed", 0.0, 2.0) is True and due("legacy", 0.0, 2.0) is True)
gate = SYNC.split("مزامنة البيانات الرئيسية")[1][:900]
check("C4 the gate is horizon-correct with the misleading comment corrected",
      "CardsLastSync.AddHours(2.0), DateTime.Now) <= 0)" in gate and
      ">= 0)" not in gate and "AddHours(2) >= Now" not in gate and
      "Repair R-052" in gate)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - the offline queue keeps identities, serial replays converge,")
print("and definitions sync catches up after absence instead of stalling.")
sys.exit(0)
