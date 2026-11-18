#!/usr/bin/env python3
"""Offline audit illustrations and separate bounded literal-source observations.

Stdlib only. No application imports, C#/VB/Newtonsoft/SQL/SDK evaluation, assembly
loading, network, payment, tax submission, browser, SMTP, licensing or OS-clock
changes. The examples are manually transcribed, synthetic counterexamples under
stated assumptions, not evidence of a deployed incident or ERP acceptance tests.
Source checks examine text, not a compiler/ABI or a vendor response contract.
JSON to stdout only; this script never writes the workspace.
"""
from __future__ import annotations

from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def refs(*parts: str) -> str:
    return ";".join("SmartAuditERP/" + part for part in parts)


def text_slice(path: str, first: int, last: int) -> str:
    data = (ROOT / "SmartAuditERP" / path).read_bytes()
    try:
        lines = data.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        lines = data.decode("cp1256", errors="replace").splitlines()
    assert 1 <= first <= last <= len(lines)
    return "\n".join(lines[first - 1:last])


def main() -> dict:
    illustrations, lexical = [], []

    def case(title, findings, inputs, observation, assertion, limit, evidence):
        assert assertion, title
        illustrations.append(dict(
            id=f"ALG6-{len(illustrations)+1:02d}", title=title,
            finding_ids=findings, manually_transcribed_inputs=inputs,
            calculated_observation=observation,
            illustration_assertions_passed=bool(assertion),
            source_application_executed=False, limit=limit, evidence=evidence))

    def static(title, findings, observation, assertion, limit, evidence):
        assert assertion, title
        lexical.append(dict(
            id=f"ST6-{len(lexical)+1:02d}", title=title, finding_ids=findings,
            literal_text_observation=observation,
            documented_text_observation_matches=bool(assertion),
            source_application_executed=False, limit=limit, evidence=evidence))

    value = "123"  # Deliberately not a real taxpayer identifier.
    tax_gate = len(value.strip()) == 15 and value.strip().startswith("3") and value.strip().endswith("3")
    helper_standard = value is not None and value != ""
    nonnumeric = "3" + "A" * 13 + "3"
    gate_accepts_nonnumeric_shape = len(nonnumeric) == 15 and nonnumeric.startswith("3") and nonnumeric.endswith("3")
    case("Different VAT predicates", ["P6-001"], {"synthetic_vat_text": value},
         {"tax_gate": tax_gate, "helper_standard": helper_standard,
          "shape_gate_can_accept_nonnumeric_text": gate_accepts_nonnumeric_shape},
         not tax_gate and helper_standard and gate_accepts_nonnumeric_shape,
         "ASCII predicate transcription only. Not Customer DTO, SQL, taxpayer validation or a real invoice-type decision.",
         refs("Class/ZatcaService.cs:78-124", "Class/InvoiceOper.cs:5211-5243"))

    bucket = {"amount": Decimal("0"), "rate": None}
    for rate, share in [(Decimal("5"), Decimal("2")), (Decimal("15"), Decimal("3"))]:
        bucket["amount"] += share
        bucket["rate"] = rate
    case("Two positive rates share one allowance object", ["P6-003"],
         {"synthetic_rate_share_pairs": [["5", "2"], ["15", "3"]]},
         {"bucket_amount": str(bucket["amount"]), "last_rate": str(bucket["rate"])},
         bucket == {"amount": Decimal("5"), "rate": Decimal("15")},
         "Two stipulated positive-rate groups; not proof the business uses mixed rates or that an SDK serializes the object unchanged.",
         refs("Class/ZatcaService.cs:231-263"))

    q, p = Decimal("1.234"), Decimal("10.126")
    raw_amount = (q * p).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
    early_amount = (q.quantize(Decimal(".01"), rounding=ROUND_HALF_EVEN) *
                    p.quantize(Decimal(".01"), rounding=ROUND_HALF_EVEN)).quantize(Decimal(".01"))
    midpoint_even = Decimal("1.005").quantize(Decimal(".01"), rounding=ROUND_HALF_EVEN)
    midpoint_up = Decimal("1.005").quantize(Decimal(".01"), rounding=ROUND_HALF_UP)
    case("Early quantity/price rounding and midpoint distinction", ["P6-004"],
         {"quantity": str(q), "price": str(p), "exact_decimal_midpoint": "1.005"},
         {"rounded_final_amount": str(raw_amount), "early_rounded_inputs_amount": str(early_amount),
          "exact_decimal_half_even": str(midpoint_even), "exact_decimal_half_up": str(midpoint_up)},
         raw_amount != early_amount and midpoint_even != midpoint_up,
         "Exact Python Decimal illustration, NOT .NET double-to-decimal, Math.Round binary midpoint behavior, SDK arithmetic or tax approval.",
         refs("Class/ZatcaService.cs:277-342"))

    issued = [{"scope": "Sale", "number": 40, "uuid": "synthetic-a"},
              {"scope": "Return", "number": 7, "uuid": "synthetic-b"}]
    wanted_previous = issued[-1]["uuid"]
    next_sale_no = 41
    per_type_previous = next(r["uuid"] for r in issued if r["scope"] == "Sale" and r["number"] == next_sale_no - 1)
    case("Per-type previous number under a shared issuing unit assumption", ["P6-005"],
         {"stipulated_unit_is_shared": True, "issued": issued, "next_sale_no": next_sale_no},
         {"last_unit_document": wanted_previous, "number_minus_one_same_type": per_type_previous},
         wanted_previous != per_type_previous,
         "Conditional list model only; EGS/POS boundaries, numbering policy, actual hashes and external UUID generation are unresolved.",
         refs("Class/InvoiceOper.cs:5276-5323", "Class/ZatcaService.cs:116-124"))

    sdk_reply = {"error_message": None, "error_messages": [], "status": "PENDING_SYNTHETIC"}
    no_errors = sdk_reply["error_message"] is None and len(sdk_reply["error_messages"]) == 0
    explicit_accepted = sdk_reply["status"] in {"CLEARED", "REPORTED"}
    case("No-error predicate is not an explicit accepted-state predicate", ["P6-006"], sdk_reply,
         {"no_errors": no_errors, "explicit_accepted": explicit_accepted}, no_errors and not explicit_accepted,
         "A synthetic response shape, not a claim the SDK can emit it or that its defaults have been executed.",
         refs("Class/ZatcaService.cs:379-417", "Form_WPF/frmZatcaSetting.xaml.cs:900-909"))

    q = Decimal("0.4")
    rounded_integer_q = int(q.quantize(Decimal("1"), rounding=ROUND_HALF_EVEN))
    original_sales = q * Decimal("10")
    case("ETA invoice quantity can become zero while value is nonzero", ["P6-013"],
         {"quantity": str(q), "price": "10"},
         {"integer_rounded_quantity": rounded_integer_q, "original_quantity_sales": str(original_sales)},
         rounded_integer_q == 0 and original_sales == Decimal("4"),
         "Arithmetic transcription for an unambiguous non-midpoint input; not execution of the external InvoiceLine setter or wire serializer.",
         refs("Class/EtaService.cs:34-58"))

    reference = "SYNTHETIC-ORIGINAL-17"
    boolean_text = str("" == reference)
    case("Reference comparison becomes Boolean text", ["P6-014"], {"reference": reference},
         {"modelled_boolean_text": boolean_text}, boolean_text == "False" and boolean_text != reference,
         "Python Boolean spelling illustrates the comparison, not a call to Microsoft.VisualBasic Conversions or SDK reference normalization.",
         refs("Class/EtaService.cs:171-186"))

    original = datetime(2026, 1, 2, 1, 25, tzinfo=timezone(timedelta(hours=3)))
    true_utc = original.astimezone(timezone.utc)
    date_only_as_utc = datetime.combine(original.date(), datetime.min.time(), tzinfo=timezone.utc)
    case("Date truncation and a literal Z are not UTC conversion", ["P6-015"],
         {"synthetic_original": original.isoformat()},
         {"actual_utc_in_illustration": true_utc.isoformat(), "date_only_labelled_utc": date_only_as_utc.isoformat()},
         true_utc != date_only_as_utc and true_utc.date() != original.date(),
         "Stipulated offset and exact datetime illustration only; no machine clock, C# culture/Kind, timezone database or receipt serializer tested.",
         refs("Class/EtaService.cs:179-182", "Class/EtaReciptService.cs:100-105"))

    def receipt_outcome(status):
        updated_uuid = status == "200"
        returned = True  # The reached, nonexception path stipulated here.
        return {"uuid_update_branch": updated_uuid, "returned": returned}
    receipt_result = receipt_outcome("SYNTHETIC_NON_SUCCESS")
    invoice_result = False  # Local result has no true assignment in the selected method.
    case("Opposite local Boolean outcome contracts", ["P6-016", "P6-017"],
         {"synthetic_sdk_status": "SYNTHETIC_NON_SUCCESS", "nonexception_path": True},
         {"receipt": receipt_result, "invoice_local_default_return": invoice_result},
         not receipt_result["uuid_update_branch"] and receipt_result["returned"] and not invoice_result,
         "Manual control-flow summary only; the SDK status string is NOT assumed to be raw HTTP. No API call, tables or persistence executed.",
         refs("Class/EtaService.cs:248-299", "Class/EtaReciptService.cs:217-234"))

    line_net, vat = Decimal("100"), Decimal("15")
    erp_net = line_net + vat
    receipt_header_net = erp_net
    case("Receipt pre-tax line total versus final ERP Net", ["P6-018"],
         {"synthetic_line_net": str(line_net), "vat": str(vat), "discount": "0"},
         {"erp_final_net": str(erp_net), "header_net_from_adapter": str(receipt_header_net), "sum_line_net": str(line_net)},
         receipt_header_net == Decimal("115") and receipt_header_net != line_net,
         "A minimal stipulated financial fixture; not evidence of actual DTO recalculation, serialized payload, ETA rejection or accounting certification.",
         refs("Class/EtaReciptService.cs:28-61", "Class/EtaReciptService.cs:108-149", "Class/InvoiceOper.cs:4189-4221"))

    events = ["remote_approved", "late_local_amount_check_failed", "user_retries"]
    remote_attempt_count_if_no_external_dedup = 2
    case("Conditional remote side effect before a local rejection", ["P6-020", "P6-021"],
         {"stipulated_schedule": events, "external_dedup_assumed_absent_for_example_only": True},
         {"possible_attempts_in_this_schedule": remote_attempt_count_if_no_external_dedup},
         events.index("remote_approved") < events.index("late_local_amount_check_failed") and remote_attempt_count_if_no_external_dedup == 2,
         "Hypothetical schedule, NOT a double-charge proof, actual terminal invocation, vendor idempotency result or concurrency test.",
         refs("Form_WPF/frmPOSBill.xaml.cs:460-519", "Form_WPF/frmPOSPay.xaml.cs:428-464"))

    old_rows, ui_rows = ["synthetic-bank-mapping"], []
    saved_rows = ui_rows.copy() if len(ui_rows) > 0 else old_rows.copy()
    case("Empty mapping selection skips the replacement block", ["P6-023"],
         {"old_rows": old_rows, "ui_rows_after_deleting_last": ui_rows}, {"modelled_saved_rows": saved_rows},
         saved_rows == old_rows and saved_rows != ui_rows,
         "Sequential list effect only, not SQL constraints/transactions/triggers, cloud routing or an actual account mapping change.",
         refs("Form_WPF/frmCloudPaymentSetting.xaml.cs:249-260", "Form_WPF/frmCloudPaymentSetting.xaml.cs:310-345"))

    anchor = datetime(2026, 1, 1)
    expiry = datetime(2026, 1, 5)
    observed_later = datetime(2026, 1, 20)
    selected_offline_now = anchor
    case("Fixed last-verified fallback does not advance", ["P6-027"],
         {"anchor": anchor.isoformat(), "expiry": expiry.isoformat(), "stipulated_later_time": observed_later.isoformat(), "ntp_result": None},
         {"selected_comparison_time": selected_offline_now.isoformat(),
          "expired_against_anchor": expiry < selected_offline_now, "expired_against_later": expiry < observed_later},
         not expiry < selected_offline_now and expiry < observed_later,
         "Stipulated cache and failed-NTP branch only; no real license, AES/hash generation, file modification, clock/NTP operation or entitlement bypass executed.",
         refs("Class/DeviceLicenseManager.cs:226-246", "Class/DeviceLicenseManager.cs:391-419"))

    def phone_text(value):
        value = value.strip()
        return value if value.startswith("966") else "966" + value.lstrip("0")
    phones = {value: phone_text(value) for value in ("+9665XXXXXXXX", "+9677XXXXXXXX", "009665XXXXXXXX")}
    case("Prefix-only phone transformation", ["P6-032"], {"synthetic_unusable_phone_markers": list(phones)}, phones,
         phones["+9677XXXXXXXX"].startswith("966+967") and phones["009665XXXXXXXX"].startswith("966966"),
         "Text markers deliberately not dialable; not E.164 validation, WhatsApp URL handling, contact existence or actual misdelivery.",
         refs("Class/WhatsAppSender.cs:107-118"))

    details = text_slice("Class/SupportTicketApiClient.cs", 120, 149)
    dto = text_slice("Class/TicketDetailsResponse.cs", 1, 8)
    dropped = 'JsonConvert.DeserializeObject<TicketDetailsApiResponse>(responseBody);' in details
    bare_success = 'return new TicketDetailsResponse { Success = true };' in details
    static("Ticket details object is discarded at the local boundary", ["P6-024"],
           {"discarded_expression_present": dropped, "success_object_without_ticket_present": bare_success,
            "ticket_auto_property_without_initializer_present": 'public TicketDetails Ticket { get; set; }' in dto},
           dropped and bare_success and 'Ticket =' not in details,
           "Literal source observation, not JSON deserialization or UI/NRE execution; remote response schema is unknown.",
           refs("Class/SupportTicketApiClient.cs:120-149", "Class/TicketDetailsResponse.cs:1-8"))

    inserts = []
    for start, end, label in ((350, 370, "PCSID fresh branch"), (1056, 1081, "import fresh branch")):
        snippet = text_slice("Form_WPF/frmZatcaSetting.xaml.cs", start, end)
        strings = " ".join(re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', snippet))
        match = re.search(r"INSERT INTO ZatcaCredential\s*\(([^)]*)\)\s*VALUES\s*\(([^)]*)\)", strings, re.I)
        assert match, label
        columns = [v.strip() for v in match[1].split(",")]
        values = [v.strip() for v in match[2].split(",")]
        supplied = sorted(set(re.findall(r'Parameters\.Add\("(@\w+)"', snippet)))
        required = sorted(set(re.findall(r"@\w+", match[2])))
        inserts.append(dict(branch=label, column_count=len(columns), value_count=len(values),
                            required_parameter_names=required, supplied_parameter_names=supplied,
                            unbound_parameter_names=sorted(set(required) - set(supplied))))
    static("Fresh ZATCA credential INSERT text shapes", ["P6-011"], inserts,
           all(r["column_count"] == 8 and r["value_count"] == 7 for r in inserts) and
           len(inserts[0]["unbound_parameter_names"]) == 3 and inserts[1]["unbound_parameter_names"] == [],
           "Bounded string/parameter-name extraction only, not SQL parsing/execution, schema/ABI checking, reachability of count==0 or a migration test. No credential values emitted.",
           refs("Form_WPF/frmZatcaSetting.xaml.cs:350-370", "Form_WPF/frmZatcaSetting.xaml.cs:1056-1081"))

    inv_eta = text_slice("Class/EtaService.cs", 20, 300)
    receipt_eta = text_slice("Class/EtaReciptService.cs", 217, 234)
    eta_observation = {"invoice_result_true_assignment_count": len(re.findall(r"\bresult\s*=\s*true\b", inv_eta)),
                       "invoice_default_result_present": 'bool result = default(bool);' in inv_eta,
                       "receipt_true_return_after_status_block_present": 'result = true;' in receipt_eta and
                           receipt_eta.index('result = true;') > receipt_eta.index('UpdateInvoiceStatus')}
    static("Different ETA local return contracts", ["P6-016", "P6-017"], eta_observation,
           eta_observation == {"invoice_result_true_assignment_count": 0, "invoice_default_result_present": True,
                               "receipt_true_return_after_status_block_present": True},
           "Literal selected-method observation only; external SDK control flow, enums, HTTP semantics and actual tables not executed.",
           refs("Class/EtaService.cs:20-300", "Class/EtaReciptService.cs:217-234"))

    bill = text_slice("Form_WPF/frmPOSBill.xaml.cs", 437, 519)
    pay = text_slice("Form_WPF/frmPOSPay.xaml.cs", 402, 464)
    order = {"bill_await_pay_before_multi_amount_gate": bill.index('await GeideaPament.Pay') < bill.index('if (_payment.PayType == 4'),
             "bill_old_pay_before_positive_net_gate": bill.index('UtilitiesProj.Geidea.Pay') < bill.index('if (netVal <= 0'),
             "pay_old_pay_before_multi_amount_gate": pay.index('UtilitiesProj.Geidea.Pay') < pay.index('if (Invoic.PayType == 4'),
             "pay_has_prior_rem_guard": pay.index('if (rem < 0') < pay.index('UtilitiesProj.Geidea.Pay')}
    static("Terminal call and selected validation textual order", ["P6-020", "P6-021"], order,
           all(order.values()),
           "Text order in selected methods, not WPF event/interleaving analysis, vendor approval or proof every input reaches these branches. Prior rem guard explicitly retained.",
           refs("Form_WPF/frmPOSBill.xaml.cs:437-519", "Form_WPF/frmPOSPay.xaml.cs:402-464"))

    normal = text_slice("Class/InvoiceOper.cs", 1, 5520)
    contract = text_slice("Class/InvoiceOperContract.cs", 911, 926)
    flag_observation = {"ordinary_InvoiceOper_flag_occurrences": normal.count('ZatcaSyncManual'),
                        "contract_uses_flag_in_send_gate": '|| !MainSetting.ZatcaSyncManual' in contract,
                        "setting_exists": 'ZatcaSyncManual' in text_slice("Class/MainSetting.cs", 12, 18)}
    static("Manual flag has a real contract consumer", ["P6-002"], flag_observation,
           flag_observation == {"ordinary_InvoiceOper_flag_occurrences": 0, "contract_uses_flag_in_send_gate": True,
                                "setting_exists": True},
           "Bounded lexical presence/absence, not proof of global non-use, runtime cache behavior or all external/reflection-based readers.",
           refs("Class/InvoiceOper.cs:1473-1495", "Class/InvoiceOper.cs:1854-1884", "Class/InvoiceOperContract.cs:911-926", "Class/MainSetting.cs:12-18"))

    # Search original tracked C# text only; absence of these direct call patterns
    # never excludes reflection/generated/external callers or certifies all files.
    tracked = subprocess.check_output(['git', 'ls-files', '-z', '--', '*.cs'], cwd=ROOT).decode().split('\0')
    source_texts = []
    for path in tracked:
        if not path or not path.startswith('SmartAuditERP/'):
            continue
        data = (ROOT / path).read_bytes()
        source_texts.append(data.decode('utf-8-sig', errors='replace'))
    joined = '\n'.join(source_texts)
    search_patterns = {
        "new_FrmSallah_direct": r"\bnew\s+(?:[\w:]+\.)?FrmSallah\s*\(",
        "new_SallaAuth_direct": r"\bnew\s+(?:[\w:]+\.)?SallaAuth\s*\(",
        "dot_ConnectGeidea_call": r"\.ConnectGeidea\s*\(",
        "dot_ProcessSale_call": r"\.ProcessSale\s*\(",
        "dot_TestConnection_call": r"neoleapService\.TestConnection\s*\(",
    }
    counts = {key: len(re.findall(pattern, joined)) for key, pattern in search_patterns.items()}
    static("Direct-call search separates sample/unused helpers from active test caller", ["P6-021", "P6-022", "P6-029", "P6-030"], counts,
           counts == {"new_FrmSallah_direct": 0, "new_SallaAuth_direct": 0,
                      "dot_ConnectGeidea_call": 0, "dot_ProcessSale_call": 0, "dot_TestConnection_call": 1},
           "Regex over tracked C# only (including comments), NOT semantic call graph, complete-file manual review, external/reflective/generated caller exclusion or runtime reachability certification.",
           refs("Class/Geidea.cs:1-58", "Class/NeoleapService.cs:23-83", "Class/SallaAuth.cs:10-33",
                "Form_WPF/FrmSallah.xaml.cs:30-35", "Home.xaml.cs:3877-3886", "Form_WPF/frmSettings.xaml.cs:4047-4066"))

    android = text_slice("Form_WPF/ClosShiftAndroid.xaml.cs", 1732, 1754)
    ordinary = text_slice("Form_WPF/frmCloseShift.xaml.cs", 1579, 1586)
    email_observation = {"android_send_call_text_count_in_selected_branch": android.count('this.SendEmail(xtraReport);'),
                         "android_case3_send_then_break_present": bool(re.search(r'case 3:\s*this.SendEmail\(xtraReport\);\s*break;', android)),
                         "ordinary_case3_send_then_return_present": bool(re.search(r'SendEmail\(report\);\s*return;', ordinary))}
    static("Conditional Android double dispatch with ordinary-path counterexample", ["P6-035"], email_observation,
           email_observation == {"android_send_call_text_count_in_selected_branch": 2,
                                 "android_case3_send_then_break_present": True,
                                 "ordinary_case3_send_then_return_present": True},
           "Branch text only; Type==3, printer/report/ActiveAuto/internet and earlier lifecycle guards are required. Not SMTP or report execution, nor a claim every close sends twice.",
           refs("Form_WPF/ClosShiftAndroid.xaml.cs:1732-1764", "Form_WPF/frmCloseShift.xaml.cs:1579-1586"))

    assert len(illustrations) == 14 and len(lexical) == 7
    return dict(
        audit_reference_date_utc="2026-11-16", method="Independent synthetic manually transcribed illustrations plus separately labelled bounded literal-source checks; NOT ERP/SDK/provider acceptance or compliance certification",
        application_code_imported_or_executed=False, erp_runtime_tests_executed=0,
        sql_or_external_service_tests_executed=0, application_remediation_performed=False,
        secrets_or_real_provider_payloads_used=False,
        illustration_count=len(illustrations), illustrations=illustrations,
        static_lexical_contract_check_count=len(lexical), static_lexical_contract_checks=lexical)


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
