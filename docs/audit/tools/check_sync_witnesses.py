#!/usr/bin/env python3
"""Audit-only sync illustrations and separate lexical source-contract checks.

Python stdlib only. Manually transcribed counterexamples, NOT C#/Newtonsoft/AES/
SQL/MQTT/HTTP/SDK execution. Does not import application code, load assemblies,
connect, alter the repository, or prove deployed behavior. JSON to stdout only.
A passing assertion means the stated illustration/text observation is coherent,
not that SmartAuditERP passed or failed an executed acceptance test.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]


def evidence(*pairs: tuple[str, str]) -> str:
    return ";".join(f"SmartAuditERP/{path}:{span}" for path, span in pairs)


def read_slice(relative: str, start: int, end: int) -> str:
    data = (ROOT / "SmartAuditERP" / relative).read_bytes()
    try:
        lines = data.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        lines = data.decode("cp1256", errors="replace").splitlines()
    assert 1 <= start <= end <= len(lines)
    return "\n".join(lines[start - 1:end])


def main() -> dict:
    illustrations = []

    def case(n, title, finding_ids, inputs, observation, assertion, limit, refs):
        assert assertion, f"Incoherent audit illustration ALG5-{n:02d}"
        illustrations.append(dict(
            id=f"ALG5-{n:02d}", title=title, finding_ids=finding_ids,
            manually_transcribed_inputs=inputs, calculated_observation=observation,
            illustration_assertions_passed=bool(assertion),
            source_application_executed=False, limit=limit, evidence=refs))

    queued = json.loads('{"itemid":42}')
    looked_up = queued.get("id", 0)
    case(1, "Different queue member names", ["P5-003"], queued,
         {"requested_item": 42, "manually_modelled_id_default": looked_up}, looked_up == 0,
         "Python dictionary/default illustration only, not Newtonsoft contract resolution or ERP serialization execution.",
         evidence(("Class/ItemIdOff.cs", "1-8"), ("Class/ListItems.cs", "6-10"),
                  ("Class/SendData.cs", "715-724")))

    observed = {identifier: identifier.startswith("1")
                for identifier in ("10-8", "1-8", "700-1-8", "100-10-8")}
    case(2, "Text prefix is not origin-branch equality", ["P5-011"],
         {"local_branch_text": "1", "identifiers": list(observed)}, observed,
         observed == {"10-8": True, "1-8": True, "700-1-8": False, "100-10-8": True},
         "ASCII prefix counterexamples only; no DTO parser, broker ACL, ID-generation SQL or real tenant data used.",
         evidence(("Class/ReceivedData.cs", "1171-1176"), ("Class/InvoiceOper.cs", "2887-2896")))

    # Synthetic, intentionally non-secret marker; no application cryptography.
    marker = "QZ"
    payload = json.dumps({"note": "INV-QZ-OK"}, separators=(",", ":"))
    global_removed = (marker + payload).replace(marker, "")
    prefix_only = (marker + payload)[len(marker):]
    case(3, "Global marker replacement mutates JSON values", ["P5-010"],
         {"synthetic_marker": marker, "synthetic_payload": payload},
         {"global_replace": json.loads(global_removed), "prefix_only": json.loads(prefix_only)},
         json.loads(global_removed)["note"] == "INV--OK" and json.loads(prefix_only)["note"] == "INV-QZ-OK",
         "No AESencDEC, encryption, key, MAC or actual payload inspected or executed; string operation illustration only.",
         evidence(("Class/ReceivedData.cs", "350-357"), ("Class/SendData.cs", "559-561")))

    def apply_permission_rows(order):
        rows = []
        for operation in order:
            rows = [dict(row, activated=False) for row in rows if row["operation"] <= 7]
            rows.append({"operation": operation, "activated": True})
        return rows
    forward = apply_permission_rows([9, 10])
    reversed_order = apply_permission_rows([10, 9])
    case(4, "Reset inside the permission-row loop", ["P5-013"], {"operations": [9, 10]},
         {"forward": forward, "reversed": reversed_order},
         forward == [{"operation": 10, "activated": True}] and reversed_order == [{"operation": 9, "activated": True}],
         "List model of the stated delete/disable/insert ordering, not SQL identity, constraint or authorization-engine execution.",
         evidence(("Class/ReceivedData.cs", "1053-1072")))

    # A narrow MQTT topic-level illustration: suffix /# accepts zero levels.
    def matches_hash_filter(filter_value, topic):
        assert filter_value.endswith("/#")
        parent = filter_value[:-2]
        return topic == parent or topic.startswith(parent + "/")
    topic_result = {"bare_matches_Inv_hash": matches_hash_filter("CInv/#", "CInv"),
                    "bare_segment_count": len("Inv".split("/")),
                    "uppercase_Entry_matches_lowercase": matches_hash_filter("Centry/#", "CEntry")}
    case(5, "Bare topic matches wildcard but lacks parser segment", ["P5-007"],
         {"filters": ["CInv/#", "Centry/#"], "topics": ["CInv", "CEntry"]}, topic_result,
         topic_result == {"bare_matches_Inv_hash": True, "bare_segment_count": 1,
                          "uppercase_Entry_matches_lowercase": False},
         "Limited manually stated MQTT matching rule, NOT a broker/protocol conformance suite, M2Mqtt invocation, or packet trace.",
         evidence(("Class/ReceivedData.cs", "79-90"), ("Class/ReceivedData.cs", "158-164"),
                  ("Class/SendData.cs", "738-776")))

    retained = {}
    retained["CItems"] = {"id": "A", "version": 2}
    retained["CItems"] = {"id": "B", "version": 3}
    case(6, "One retained slot is not a delta backlog", ["P5-009"],
         {"publish_order": ["delta A", "delta B"], "same_topic": "CItems"}, retained,
         list(retained.values()) == [{"id": "B", "version": 3}],
         "Single-slot state model under ordinary retained semantics, not proof a deployed broker discarded active deliveries or lacks a separate resnapshot service.",
         evidence(("Class/SendData.cs", "676-691")))

    initial = ["a"]
    writer_a, writer_b = initial.copy(), initial.copy()
    writer_a.append("x")
    writer_b.append("y")
    final_after_two_whole_file_writes = writer_b
    read_before_append = initial.copy()
    after_append = initial + ["z"]
    after_sender_clear = []
    case(7, "Whole-file write and clear counterexample schedules", ["P5-004"],
         {"initial": initial, "writer_a_read_then_append": writer_a, "writer_b_read_then_append": writer_b,
          "sender_read": read_before_append, "new_file_before_clear": after_append},
         {"last_whole_write": final_after_two_whole_file_writes, "after_clear": after_sender_clear},
         "x" not in final_after_two_whole_file_writes and "z" not in after_sender_clear,
         "Two stipulated interleavings only, not a filesystem crash test or evidence of real concurrent ERP processes; no files written.",
         evidence(("Form_WPF/frmItems.xaml.cs", "2142-2155"), ("Class/SendData.cs", "715-725")))

    old = ["old1", "old2"]
    after_delete = []
    after_first_insert_and_stipulated_second_insert_failure = ["new1"]
    after_empty_message = old.copy()  # neither foreach executes
    case(8, "Autocommit replacement and empty-child ambiguity", ["P5-012"],
         {"before": old, "incoming": ["new1", "new2"], "empty_incoming": []},
         {"after_delete": after_delete, "after_failure": after_first_insert_and_stipulated_second_insert_failure,
          "after_empty": after_empty_message},
         after_first_insert_and_stipulated_second_insert_failure == ["new1"] and after_empty_message == old,
         "Manually transcribed sequential list effects only, not SQL/rollback/trigger behavior or proof of financial imbalance on deployed data.",
         evidence(("Class/ReceivedData.cs", "1250-1272"), ("Class/ReceivedData.cs", "1313-1349")))

    now = datetime(2026, 1, 1, 12, tzinfo=timezone.utc)
    fresh, stale = now - timedelta(hours=1), now - timedelta(hours=3)
    due_result = {"fresh_gate": fresh + timedelta(hours=2) >= now,
                  "stale_gate": stale + timedelta(hours=2) >= now}
    fetch_bound, change, checkpoint = now, now + timedelta(minutes=1), now + timedelta(minutes=2)
    case(9, "Inverted freshness and conditional local-now cursor gap", ["P5-017", "P5-018"],
         {"synthetic_now": now.isoformat(), "fetched_at": fetch_bound.isoformat(),
          "change_after_that_entity_fetch": change.isoformat(), "later_checkpoint": checkpoint.isoformat()},
         {**due_result, "change_is_behind_new_checkpoint": change < checkpoint},
         due_result == {"fresh_gate": True, "stale_gate": False} and fetch_bound < change < checkpoint,
         "Datetime ordering only. Actual skipping additionally needs a server updated-since/snapshot contract, inclusivity and clock behavior; no ERP/API execution.",
         evidence(("Class/Sync.cs", "479-487"), ("Class/SyncOperation.cs", "232-248")))

    snapshot = {"product": 42, "branch": 2, "warehouse": 3, "unit": 7, "quantity": 10}
    active_non_cloud_rows = [snapshot.copy(), snapshot.copy()]
    cloud_old_after_empty_guard = [snapshot.copy()]
    case(10, "Stock append and skipped empty replacement", ["P5-023"], {"snapshot": snapshot},
         {"active_noncloud_row_count_after_two_calls": len(active_non_cloud_rows),
          "cloud_old_rows_if_empty_not_applied": len(cloud_old_after_empty_guard)},
         len(active_non_cloud_rows) == 2 and cloud_old_after_empty_guard == [snapshot],
         "Model assumes successful inserts into the supplied no-unique-key shape; deployed constraints may reject rather than accumulate. No SQL or stock recalculation executed.",
         evidence(("Class/EntityOperations.cs", "914-939"), ("Class/SyncOperation.cs", "141-145"),
                  ("Properties/Resources.resx", "3932-3940")))

    n = 3
    case(11, "N whole-batch customer echo invocations", ["P5-022"], {"customers": n},
         {"modelled_calls": n, "rows_carried_across_calls": n * n}, n * n == 9,
         "Counts payload elements in the described branch only; not N squared inserted server rows, not observed traffic, and not proof of an endless echo loop.",
         evidence(("Class/EntityOperations.cs", "1174-1182")))

    to_send, remaining = ["A", "B"], ["C"]
    # Conditional opaque-SDK model, explicitly NOT asserting its implementation.
    failed_batch_after_assumed_clear_and_restore_remaining = remaining.copy()
    case(12, "Conditional cleanup of a rejected cloud batch", ["P5-026"],
         {"to_send": to_send, "remaining": remaining, "assumption": "CLearfiles clears this queue and no SQL rebuild intervenes"},
         {"after_assumed_clear_restore": failed_batch_after_assumed_clear_and_restore_remaining},
         not set(to_send) & set(failed_batch_after_assumed_clear_and_restore_remaining),
         "Counterexample under an explicit external SDK assumption only. Does not inspect or execute InvoiceCRUD.CLearfiles, AddinvoicesLocally or server idempotency/rebuild.",
         evidence(("Class/Sync.cs", "644-685")))

    lexical = []

    def text_check(n, title, finding_ids, observed, match, limit, refs):
        assert match, f"Changed or inaccurate lexical observation ST5-{n:02d}"
        lexical.append(dict(id=f"ST5-{n:02d}", title=title, finding_ids=finding_ids,
                            lexical_observation=observed, documented_text_observation_matches=bool(match),
                            source_application_executed=False, limit=limit, evidence=refs))

    queue_dto = read_slice("Class/ItemIdOff.cs", 1, 8)
    item_dto = read_slice("Class/ListItems.cs", 6, 10)
    queue_reader = read_slice("Class/SendData.cs", 715, 724)
    text_check(1, "Queue/read member spellings", ["P5-003"],
               {"queue_member": "itemid", "reader_type": "List<ListItems>", "read_member": "item.id"},
               bool(re.search(r"int\s+itemid\s*\{", queue_dto)) and
               bool(re.search(r"int\s+id\s*\{", item_dto)) and
               "DeserializeObject<List<ListItems>>" in queue_reader and "item.id" in queue_reader,
               "Literal member/type spellings only, no Newtonsoft runtime contract resolver or converter certification.",
               evidence(("Class/ItemIdOff.cs", "1-8"), ("Class/ListItems.cs", "6-10"), ("Class/SendData.cs", "715-724")))

    reader = read_slice("Class/ReceivedData.cs", 51, 113)
    oper_dispatch = read_slice("Class/ReceivedData.cs", 147, 259)
    arrays = re.findall(r"\{([^{}]+)\}", reader)
    # Select by a distinctive literal to avoid claiming this is a C# parser.
    oper_text = next(a for a in arrays if '"Inv/#"' in a and '"Customers"' in a and '"Items"' not in a)
    definitions_text = next(a for a in arrays if '"Banks"' in a and '"Employee"' in a)
    oper_topics = re.findall(r'"([A-Za-z_/#]+)"', oper_text)
    definition_topics = re.findall(r'"([A-Za-z_/#]+)"', definitions_text)
    cases = re.findall(r'case\s+"([A-Za-z_]+)"\s*:', oper_dispatch)
    missing_cases = sorted(set(["Customers", "AccountCust", "AccountIndex"]) - set(cases))
    missing_subscriptions = sorted(set(["Safe", "Offer", "OfferClient", "OfferItem"]) - set(definition_topics))
    text_check(2, "Literal subscription/dispatch set differences", ["P5-008"],
               {"oper_subscribed": oper_topics, "oper_cases": cases,
                "selected_missing_oper_cases": missing_cases,
                "selected_missing_definition_subscriptions": missing_subscriptions},
               missing_cases == ["AccountCust", "AccountIndex", "Customers"] and
               missing_subscriptions == ["Offer", "OfferClient", "OfferItem", "Safe"],
               "Regex over selected literal arrays/cases only; not a complete C# event analyzer. Other loaded handlers can incidentally process some topics; broker ACL/external subscribers unknown.",
               evidence(("Class/ReceivedData.cs", "51-113"), ("Class/ReceivedData.cs", "147-259")))

    sql_a = read_slice("Properties/Resources.resx", 4214, 4224)
    sql_b = read_slice("Properties/Resources.resx", 49311, 49321)
    inventory_counts = [len(re.findall(r"@Inventory\b", value, re.I)) for value in (sql_a, sql_b)]
    text_check(3, "Stock warehouse argument occurs in declarations only", ["P5-024"],
               {"inventory_token_count_per_literal_procedure": inventory_counts,
                "body_has_inventory_id": [bool(re.search(r"InventoryId", s, re.I)) for s in (sql_a, sql_b)]},
               inventory_counts == [1, 1] and all("InventoryId" not in s for s in (sql_a, sql_b)),
               "Lexical argument/name counts in supplied SQL resource text only; not deployed procedure/schema or SQL execution, collation, plan or constraint analysis.",
               evidence(("Properties/Resources.resx", "4214-4224"), ("Properties/Resources.resx", "49311-49321")))

    sync_noncloud = read_slice("Class/InvoiceOper.cs", 2717, 2740)
    http = read_slice("Class/Sync.cs", 798, 815)
    text_check(4, "Selected outcome/await tokens", ["P5-029"],
               {"noncloud_has_return_result": "return result;" in sync_noncloud,
                "noncloud_has_result_true_assignment": bool(re.search(r"result\s*=\s*true", sync_noncloud)),
                "entry_call_has_await": bool(re.search(r"await\s+entryOper.SyncEntry", sync_noncloud)),
                "http_slice_checks_status_token": "IsSuccessStatusCode" in http or "EnsureSuccessStatusCode" in http},
               "entryOper.SyncEntry(Eny, IsNew);" in sync_noncloud and "return result;" in sync_noncloud and
               not re.search(r"result\s*=\s*true|await\s+entryOper.SyncEntry", sync_noncloud) and
               "await httpClient.PostAsync(" in http and "return true;" in http and
               "IsSuccessStatusCode" not in http and "EnsureSuccessStatusCode" not in http,
               "Presence/absence of tokens in explicitly bounded slices, not control-flow proof for all methods, actual HTTP outcomes or successful GL posting.",
               evidence(("Class/InvoiceOper.cs", "2717-2740"), ("Class/Sync.cs", "798-815")))

    serial = read_slice("Class/ReceivedData.cs", 620, 628)
    text_check(5, "Serial predicate binding versus write binding", ["P5-014"],
               {"existence_ItemId_binding": "itemSerialNo.Id", "write_ItemId_binding": "itemSerialNo.ItemId"},
               'sqlCommand.Parameters.AddWithValue("@ItemId", itemSerialNo.Id);' in serial and
               'sqlCommand2.Parameters.AddWithValue("@ItemId", itemSerialNo.ItemId);' in serial,
               "Literal field mismatch only; no serial policy, IDENTITY/unique constraints, deployed SQL, insert or duplicate replay executed.",
               evidence(("Class/ReceivedData.cs", "620-628")))

    return dict(audit_date_utc="2026-11-16", source_head="10ba215152f722c8808aea0bb672c1d1d4d9d711",
                method="Independent manually transcribed Python state/string/clock illustrations plus separately labelled bounded literal-source lexical checks; NOT ERP acceptance tests",
                application_code_imported_or_executed=False, erp_runtime_tests_executed=0,
                sql_or_external_service_tests_executed=0, application_remediation_performed=False,
                illustration_count=len(illustrations), illustrations=illustrations,
                static_lexical_contract_check_count=len(lexical), static_lexical_contract_checks=lexical)


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
