#!/usr/bin/env python3
"""Offline phase7A audit illustrations and separate literal-source checks.

Stdlib only. Does not import or execute ERP/C#/WPF/SQL/COM/SDK code, load a DLL,
connect to a device/service, build, change clocks, or modify any source/evidence.
Examples below are manually transcribed synthetic models under stated limits;
source checks inspect bounded text, not a compiler, WPF runtime or deployed DDL.
JSON is printed to stdout only. Passing these assertions is NOT ERP acceptance.
"""
from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]


def refs(*parts: str) -> str:
    return ";".join("SmartAuditERP/" + p for p in parts)


def text_slice(path: str, first: int, last: int) -> str:
    lines = (ROOT / "SmartAuditERP" / path).read_text(encoding="utf-8-sig").splitlines()
    assert 1 <= first <= last <= len(lines)
    return "\n".join(lines[first - 1:last])


def main() -> dict:
    illustrations, lexical = [], []

    def case(title, findings, inputs, observation, assertion, limit, evidence):
        assert assertion, title
        illustrations.append(dict(
            id=f"ALG7-{len(illustrations)+1:02d}", title=title,
            finding_ids=findings, manually_transcribed_inputs=inputs,
            calculated_observation=observation,
            illustration_assertions_passed=bool(assertion),
            source_application_executed=False, limit=limit, evidence=evidence))

    def static(title, findings, observation, assertion, limit, evidence):
        assert assertion, title
        lexical.append(dict(
            id=f"ST7-{len(lexical)+1:02d}", title=title, finding_ids=findings,
            literal_text_observation=observation,
            documented_text_observation_matches=bool(assertion),
            source_application_executed=False, limit=limit, evidence=evidence))

    # Symbolic tags, not a Python attempt to execute the .NET cast or exceptions.
    selected_tags, expected_tag = ["nested-SalaryRow", "nested-SalaryRow"], "DataRow"
    compatible = all(tag == expected_tag for tag in selected_tags)
    entry_is_null, result_is_checked = True, False  # Stipulated catch/caller path.
    save_guard_invokes_entry = not entry_is_null
    case("Typed row mismatch can take the null-entry success branch", ["P7-001"],
         {"selected_type_tags": selected_tags, "binder_expected_tag": expected_tag,
          "stipulated_binder_result": "null"},
         {"symbolic_contract_compatible": compatible,
          "entry_save_guard_entered": save_guard_invokes_entry,
          "caller_checks_boolean": result_is_checked},
         not compatible and not save_guard_invokes_entry and not result_is_checked,
         "Symbolic type/branch model only, not .NET casting, exception, WPF or SQL execution; persistence is conditional on schema and preceding writes.",
         refs("Form_WPF/FrmReseved.xaml.cs:355-429", "Class/Reseved.cs:227-244", "Class/Reseved.cs:295-345"))

    loaded = {"Emp": 0, "Empnam": "synthetic-employee", "Net_Sal": "100"}
    incoming_id = 42
    validation_found_rows = 0
    validation_result = True  # no-row path of the selected helper, stipulated.
    case("Reload omission preserves the default employee identifier", ["P7-003"],
         {"synthetic_source_employee_id": incoming_id, "initializer_does_not_assign_Emp": True},
         {"row_Emp": loaded["Emp"], "validation_rows": validation_found_rows,
          "no_row_helper_return": validation_result},
         loaded["Emp"] != incoming_id and loaded["Emp"] == 0 and validation_result,
         "Dictionary/default illustration, not DTO setters, a deployed employee0/FK, a selected WPF row, payroll SQL or production corruption.",
         refs("Form_WPF/FrmReseved.xaml.cs:493-531", "Form_WPF/FrmReseved.xaml.cs:698-711", "Form_WPF/FrmReseved.xaml.cs:791-804", "Form_WPF/FrmReseved.xaml.cs:889-904"))

    basic, old_net = Decimal("100"), Decimal("100")
    after_add = basic + Decimal("20")
    after_sub = basic - Decimal("15")
    case("Editable components disagree with a stale saved net", ["P7-006"],
         {"basic": "100", "independent_add_edit": "20", "independent_sub_edit": "15", "old_net": "100"},
         {"expected_after_add": str(after_add), "expected_after_sub": str(after_sub),
          "net_if_no_recalculation": str(old_net)},
         after_add == 120 and after_sub == 85 and old_net not in (after_add, after_sub),
         "Exact Decimal fixtures, not C# culture/binary arithmetic, WPF events, SQL writes or an actual financial payment.",
         refs("Form_WPF/frmSalaryPay.xaml:328-355", "Form_WPF/frmSalaryPay.xaml.cs:340-354", "Form_WPF/frmSalaryPay.xaml.cs:531-547"))

    current_code = -1  # ClearForm.
    current_code = 7   # A stipulated subsequent MAX(id) result.
    next_operation = "UPDATE" if current_code != -1 else "INSERT"
    booking_code_after_edit = 7
    booking_code_after_clear = booking_code_after_edit  # ClearAll omits reset.
    case("Clearing fields is not resetting edit identity", ["P7-007", "P7-023"],
         {"clear_form_code": -1, "stipulated_subsequent_MAX": 7, "booking_loaded_code": 7},
         {"add_sub_next_operation": next_operation, "booking_code_after_automatic_clear": booking_code_after_clear},
         next_operation == "UPDATE" and booking_code_after_clear == 7,
         "Sequential editor-state transcription only; no concurrent SQL, actual MAX allocation, WPF button presses or overwrite performed. Explicit Booking New is a counterexample that resets Code.",
         refs("Form_WPF/frmEmpSalaryAddSub.xaml.cs:417-421", "Form_WPF/frmEmpSalaryAddSub.xaml.cs:830-844", "Form_WPF/frmEmpSalaryAddSub.xaml.cs:882-897", "Form_WPF/frmBookingM.xaml.cs:502-530", "Form_WPF/frmBookingM.xaml.cs:738-741", "Form_WPF/frmBookingM.xaml.cs:1146-1153"))

    contracts = [{"Contr_id": 10, "ContrNo": 77}, {"Contr_id": 77, "ContrNo": 90}]
    editor_code = 77
    intended = [r["Contr_id"] for r in contracts if r["ContrNo"] == editor_code]
    update_target = [r["Contr_id"] for r in contracts if r["Contr_id"] == editor_code]
    case("Business number used as primary key targets a different head", ["P7-010"],
         {"synthetic_contracts": contracts, "opened_business_number": editor_code},
         {"intended_primary_ids": intended, "primary_ids_matched_by_update": update_target},
         intended == [10] and update_target == [77] and intended != update_target,
         "Two stipulated distinct keys, not deployed numbering/constraints/triggers or a SQL update. Equality in a small database can mask this mismatch.",
         refs("Form_WPF/frmContractPM.xaml.cs:449-470", "Form_WPF/frmContractPM.xaml.cs:649-659", "Class/StoredQueries.cs:24-24", "Properties/Resources.resx:46883-46912"))

    existing_projects = [101, 102]
    recreated_projects = existing_projects + [103, 104]
    case("Re-saving two terms can append two more projects", ["P7-011"],
         {"existing_project_ids": existing_projects, "term_count": 2, "stipulated_commit_on_compatible_schema": True},
         {"project_ids_after_unconditional_inserts": recreated_projects, "old_links_still_point_to": existing_projects},
         len(recreated_projects) == 4 and recreated_projects[:2] == existing_projects,
         "List model conditional on reaching Commit and a compatible schema; P7-014 can block actual inserts. Not evidence of duplicated projects in a deployment.",
         refs("Form_WPF/frmContractPM.xaml.cs:685-701", "Form_WPF/frmContractPM.xaml.cs:835-866"))

    quantity, price, vat = Decimal("10"), Decimal("100"), Decimal("150")
    total = quantity * price
    wrong_net, correct_net = price + vat, total + vat
    header_vat = Decimal("0")
    case("Reloaded term net and saved header tax do not match components", ["P7-012", "P7-013"],
         {"quantity": "10", "unit_price": "100", "line_VAT_amount": "150"},
         {"total": str(total), "reloaded_price_plus_vat": str(wrong_net),
          "required_total_plus_vat": str(correct_net), "forced_header_VAT": str(header_vat)},
         total == 1000 and wrong_net == 250 and correct_net == 1150 and header_vat != vat,
         "Exact Decimal counterexample with a VAT amount, not a legal tax-rate decision, .NET calculation/property setters, SQL, a report or compliance certification.",
         refs("Form_WPF/frmContractPM.xaml.cs:494-517", "Form_WPF/frmContractPM.xaml.cs:677-684"))

    seed = {3: "in-progress", 4: "closed"}
    accredited_status, local_closed_test = 3, 3
    case("One status code has conflicting semantic consumers", ["P7-015"],
         {"transcribed_seed": seed, "accreditation_status": accredited_status, "cycle_closed_constant": local_closed_test},
         {"seed_meaning_after_accreditation": seed[accredited_status],
          "cycle_considers_it_closed": accredited_status == local_closed_test},
         seed[accredited_status] == "in-progress" and accredited_status == local_closed_test and seed[4] == "closed",
         "Seed/consumer symbol model, not the deployed PM_Status lookup, a project transition, closed-state UI rendering or a migration test.",
         refs("Properties/Resources.resx:47111-47117", "Form_WPF/frmAssignProjectPM.xaml.cs:849-855", "Form_WPF/frmProjCyclePM.xaml.cs:299-309", "Form_WPF/frmProjCyclePM.xaml.cs:800-805"))

    required_stages, button_slots = list(range(1, 8)), list(range(1, 7))
    displayed = required_stages[:len(button_slots)]
    empty_stage_validation = all([])
    case("Empty loops pass while a seventh configured stage is not displayed", ["P7-016", "P7-017"],
         {"configured_stage_ids": required_stages, "fixed_button_slots": button_slots, "independent_empty_plan": []},
         {"displayed_stage_ids": displayed, "unreachable_configured_stage_ids": sorted(set(required_stages)-set(displayed)),
          "empty_all_result": empty_stage_validation},
         empty_stage_validation and 7 not in displayed and len(displayed) == 6,
         "Python loop/list illustration, not WPF layout or actual stage approval. Sequential versus parallel business policy and valid empty project types require an explicit contract.",
         refs("Form_WPF/frmProjCyclePM.xaml.cs:299-309", "Form_WPF/frmProjCyclePM.xaml.cs:374-391", "Form_WPF/frmProjCyclePM.xaml:350-375", "Form_WPF/frmProjectStagesPM.xaml.cs:424-439"))

    device_batch = ["synthetic-event-A", "synthetic-event-B", "synthetic-event-C"]
    sql_rows = list(device_batch)
    sql_rows.extend(device_batch)  # Stipulate reread after commit and clear failure.
    case("Commit followed by failed clear requires ingestion idempotency", ["P7-009"],
         {"device_batch": device_batch, "stipulated_clear_result": False, "stipulated_replay": True},
         {"rows_without_inbox_after_two_reads": len(sql_rows), "unique_event_count": len(set(sql_rows))},
         len(sql_rows) == 6 and len(set(sql_rows)) == 3,
         "Conditional list schedule only; no device/COM or SQL. SDK replay semantics, external triggers and a reliable event identity remain unresolved. Commit precedes clear; no pre-commit erasure claim.",
         refs("Class/FingerPrintDevice.cs:73-106", "Properties/Resources.resx:3515-3539"))

    active_ids = [1, 5]
    predicted_number, stipulated_next_identity = len(active_ids) + 1, 6
    case("An active-row display count is not the inserted booking identity", ["P7-022"],
         {"active_booking_ids": active_ids, "stipulated_SQL_next_identity": stipulated_next_identity},
         {"display_number": predicted_number, "addition_parent_if_taken_from_display": predicted_number,
          "real_parent_under_stipulation": stipulated_next_identity},
         predicted_number == 3 and predicted_number != stipulated_next_identity,
         "Stipulated identity-gap example only, not SQL identity allocation or proof of orphan/foreign booking rows; no missing stored-procedure return contract assumed.",
         refs("Form_WPF/frmBookingM.xaml.cs:241-269", "Form_WPF/frmBookingM.xaml.cs:661-674", "Form_WPF/frmBookingM.xaml.cs:711-735", "Properties/Resources.resx:159-178"))

    raw_before = [{"event": 1, "mode": 0}, {"event": 2, "mode": 1}, {"event": 3, "mode": 0}]
    raw_after = [dict(r, mode=1) for r in raw_before]
    case("Day-wide exit update rewrites previously recorded entry modes", ["P7-026"],
         {"same_boat_same_day_events": raw_before, "manual_exit_sets_mode": 1},
         {"events_after_day_predicate": raw_after, "changed_prior_entry_count": sum(a["mode"] != b["mode"] for a, b in zip(raw_before, raw_after))},
         raw_after != raw_before and [r["mode"] for r in raw_after] == [1, 1, 1],
         "List/predicate illustration, not Attendance SQL or payroll attendance. The inspected consumer is marine; no employee identity relationship is inferred.",
         refs("Form_WPF/frmAttendM.xaml.cs:554-588", "Form_WPF/frmHoldM.xaml.cs:470-500"))

    collect = text_slice("Form_WPF/FrmReseved.xaml.cs", 355, 429)
    binder = text_slice("Class/Reseved.cs", 268, 345)
    saver = text_slice("Class/Reseved.cs", 227, 244)
    static("Accrual row tags, cast and nullable entry guard in selected text", ["P7-001"],
           {"caller_collects_rows": "selectedRows.Add(row)" in collect,
            "caller_uses_SalaryRow_loop": "foreach (SalaryRow row in selectedRows)" in collect,
            "binder_contains_DataRow_cast": "dataRow = (DataRow)dt[i]" in binder,
            "binder_returns_null_on_catch": "result = null" in binder,
            "entry_save_is_conditional_on_nonnull": "Entr != null && !new EntryOper().SaveEnty(Entr)" in saver},
           all(token in collect for token in ("selectedRows.Add(row)", "foreach (SalaryRow row in selectedRows)")) and
           "dataRow = (DataRow)dt[i]" in binder and "result = null" in binder and
           "Entr != null && !new EntryOper().SaveEnty(Entr)" in saver,
           "Bounded literal presence, not type checking, .NET exception or transaction execution. Semantic trace and limitations are in the report.",
           refs("Form_WPF/FrmReseved.xaml.cs:355-429", "Class/Reseved.cs:227-244", "Class/Reseved.cs:268-345"))

    reloads = [text_slice("Form_WPF/FrmReseved.xaml.cs", a, b) for a, b in ((698, 711), (791, 804))]
    omitted = [not bool(re.search(r"\bEmp\s*=", block)) for block in reloads]
    static("Both selected reload initializers omit Emp", ["P7-003"],
           {"Emp_assignment_absent_in_each_initializer": omitted,
            "Empnam_present_in_each_initializer": ["Empnam" in s for s in reloads]},
           all(omitted) and all("new SalaryRow" in s and "Empnam" in s for s in reloads),
           "Absence only in the two declared initializer slices, not a global data-flow proof or evaluation of external DTO/default/FK behavior.",
           refs("Form_WPF/FrmReseved.xaml.cs:698-711", "Form_WPF/FrmReseved.xaml.cs:791-804"))

    salary_save = text_slice("Form_WPF/frmSalaryPay.xaml.cs", 427, 566)
    salary_reset = text_slice("Form_WPF/frmSalaryPay.xaml.cs", 89, 118)
    static("SalaryPay writer uses the field without a local financial writer call", ["P7-004"],
           {"SalaryPay_write_text_present": "SalaryPay" in salary_save,
            "EntryOper_or_ReceiptOper_text_present_in_save": bool(re.search(r"\b(?:EntryOper|ReceiptOper)\b", salary_save)),
            "EntryGlobalID_Field_reset_present_in_CLR": "EntryGlobalID_Field" in salary_reset},
           "SalaryPay" in salary_save and "EntryGlobalID_Field" in salary_save and
           not re.search(r"\b(?:EntryOper|ReceiptOper)\b", salary_save) and "EntryGlobalID_Field" not in salary_reset,
           "Local selected-method text only. Does not rule out database triggers or services outside the repository, and makes no collateral-deletion claim about ReceiptOper.",
           refs("Form_WPF/frmSalaryPay.xaml.cs:89-118", "Form_WPF/frmSalaryPay.xaml.cs:427-566"))

    markup = text_slice("Form_WPF/frmSalaryPay.xaml", 328, 355)
    declarations = {}
    for name in ("txtTotSalary", "TxtHous", "TxtTravel", "txtSalaryAdd", "txtSalarySub"):
        match = re.search(r'<TextBox\s+x:Name="' + re.escape(name) + r'"[^>]*?/>', markup, re.S)
        assert match, name
        declarations[name] = "TextChanged=" in match[0]
    static("Salary component event declarations have different recalc wiring", ["P7-006"],
           {"has_TextChanged_in_selected_TextBox": declarations},
           all(declarations[x] for x in ("txtTotSalary", "TxtHous", "TxtTravel")) and
           not declarations["txtSalaryAdd"] and not declarations["txtSalarySub"],
           "Selected XAML declaration check only, not a WPF event/style/rendering test or a global binding analysis; the full local code-behind was separately reviewed.",
           refs("Form_WPF/frmSalaryPay.xaml:328-355"))

    contract_read = text_slice("Form_WPF/frmContractPM.xaml.cs", 449, 470)
    contract_update = text_slice("Form_WPF/frmContractPM.xaml.cs", 649, 659)
    contract_vat = text_slice("Form_WPF/frmContractPM.xaml.cs", 677, 684)
    update_sql = text_slice("Class/StoredQueries.cs", 24, 24)
    static("Contract primary-id parameter and forced zero tax in selected text", ["P7-010", "P7-012"],
           {"read_uses_ContrNo": 'reader["ContrNo"]' in contract_read,
            "update_binds_Contr_id_to_currentCode": bool(re.search(r'"@Contr_id"[^;]*=\s*_currentCode', contract_update)),
            "update_where_uses_Contr_id": "where Contr_id=@Contr_id" in update_sql,
            "header_VAT_parameter_is_zero": bool(re.search(r'"@VATval"[^;]*=\s*0\s*;', contract_vat))},
           'reader["ContrNo"]' in contract_read and
           bool(re.search(r'"@Contr_id"[^;]*=\s*_currentCode', contract_update)) and
           "where Contr_id=@Contr_id" in update_sql and
           bool(re.search(r'"@VATval"[^;]*=\s*0\s*;', contract_vat)),
           "Literal selected C#/SQL strings, not a SQL parser, data update, deployed schema or tax certification.",
           refs("Form_WPF/frmContractPM.xaml.cs:449-470", "Form_WPF/frmContractPM.xaml.cs:649-659", "Form_WPF/frmContractPM.xaml.cs:677-684", "Class/StoredQueries.cs:24-24"))

    requirement_ddl = text_slice("Properties/Resources.resx", 47160, 47177)
    requirement_read = text_slice("Form_WPF/frmRequirementPM.xaml.cs", 278, 306)
    ddl_columns = re.findall(r"^\s*\[([^\]]+)\]\s+\[", requirement_ddl, re.M)
    pk = re.search(r"PRIMARY KEY CLUSTERED\s*\((.*?)\)WITH", requirement_ddl, re.S)
    assert pk
    pk_columns = re.findall(r"\[([^\]]+)\]", pk[1])
    static("Supplied requirement-detail DDL differs from selected readers", ["P7-021"],
           {"declared_columns": ddl_columns, "primary_key_columns": pk_columns,
            "reader_requests_IsDeleted": bool(re.search(r"IsDeleted\s*=\s*0", requirement_read, re.I))},
           "IsDeleted" not in ddl_columns and pk_columns == ["RequirNo"] and
           bool(re.search(r"IsDeleted\s*=\s*0", requirement_read, re.I)),
           "Bounded embedded-DDL/text-name extraction only, not SQL parsing or proof that a deployed schema lacks a later external migration/trigger.",
           refs("Properties/Resources.resx:47160-47177", "Form_WPF/frmRequirementPM.xaml.cs:278-306"))

    sub_sql = text_slice("Class/StoredQueries.cs", 20, 20)
    sub_caller = text_slice("Form_WPF/frmHoldM.xaml.cs", 428, 446)
    required = {x.casefold() for x in re.findall(r"@[A-Za-z_][A-Za-z_0-9]*", sub_sql)}
    supplied = {x.casefold() for x in re.findall(r'Parameters\.Add\("(@[A-Za-z_][A-Za-z_0-9]*)"', sub_caller)}
    static("Hold entry-detail caller omits a required shared SQL parameter", ["P4-020", "P4-025"],
           {"required_parameter_names": sorted(required), "supplied_parameter_names": sorted(supplied),
            "required_minus_supplied": sorted(required-supplied)},
           required - supplied == {"@salesman"} and not supplied - required,
           "Parameter-name set difference only. Not SQL execution or an assessment of every type/length/path. False success is the existing P4-025 root, not a new phase7 finding.",
           refs("Class/StoredQueries.cs:20-20", "Form_WPF/frmHoldM.xaml.cs:428-446"))

    importer = text_slice("Class/FingerPrintDevice.cs", 48, 120)
    finally_text = importer.split("finally", 1)[1]
    static("Biometric text keeps commit before clear but re-enable before finally", ["P7-008", "P7-009"],
           {"commit_before_clear": importer.index("sqlTransaction.Commit()") < importer.index("ClearGLog("),
            "enable_true_text_before_finally": importer.index("bFlag: true") < importer.index("finally"),
            "EnableDevice_present_in_finally_slice": "EnableDevice" in finally_text,
            "open_and_begin_precede_try": importer.index("BeginTransaction()") < importer.index("try")},
           importer.index("sqlTransaction.Commit()") < importer.index("ClearGLog(") and
           importer.index("bFlag: true") < importer.index("finally") and "EnableDevice" not in finally_text and
           importer.index("BeginTransaction()") < importer.index("try"),
           "Textual order/absence only; SDK Boolean semantics, actual disabling/replay/normal exhaustion, exceptions and device recovery are untested. Closing SQL ordinarily rolls back uncommitted work.",
           refs("Class/FingerPrintDevice.cs:48-120"))

    assert len(illustrations) == 12 and len(lexical) == 8
    return dict(
        audit_reference_date_utc="2026-11-16", phase="7A-partial-static-audit",
        method="Independent manually transcribed Python illustrations and separate bounded literal-source checks; NOT ERP/SQL/WPF/COM/SDK tests",
        application_code_imported_or_executed=False,
        erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0,
        application_remediation_performed=False, secrets_or_real_employee_or_device_data_used=False,
        illustration_count=len(illustrations), static_lexical_contract_check_count=len(lexical),
        illustrations=illustrations, static_lexical_contract_checks=lexical,
        limit="Passing audit-owned assertions only documents these stipulated examples/text observations; no build, runtime acceptance, actual data mutation, deployed-incident or financial/compliance certification.")


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, indent=2))
