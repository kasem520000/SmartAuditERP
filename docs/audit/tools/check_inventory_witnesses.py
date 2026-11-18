#!/usr/bin/env python3
"""Audit-only illustrations and lexical parameter checks for phase 4.

No ERP import/build/C# execution/SQL/driver/network/binary loading occurs.
The Decimal/list/state examples below are MANUALLY TRANSCRIBED, independent
illustrations, NOT tests of the application's implementation. The separate
parameter section reads only C# source text and compares literal name sets;
it is not a SQL parser, type checker, build, or deployed-schema verification.
Stdlib only. Deterministic stdout; does not write or change source/evidence.
"""
from __future__ import annotations

from decimal import Decimal, localcontext
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
D = Decimal
CASES: list[dict] = []


def ev(path: str, span: str) -> str:
    return f"SmartAuditERP/{path}:{span}"


def add(number: int, findings: list[str], title: str, inputs: dict, observed: dict,
        expected: dict, evidence: str, limit: str) -> None:
    CASES.append({"id": f"ALG4-{number:02d}", "finding_ids": findings,
                  "kind": "independent-manually-transcribed-illustration",
                  "title": title, "inputs": inputs, "illustrated_source_rule": observed,
                  "comparison_rule": expected, "evidence": evidence,
                  "source_application_executed": False,
                  "illustration_assertions_passed": True, "limit": limit})


def illustrations() -> list[dict]:
    CASES.clear()
    q = D(1)
    returned = -q
    held = -q
    assert returned == -1 and returned != q and held != 0
    add(1, ["P4-001", "P4-002"], "Signed line movement, not header names",
        {"quantity_base": "1", "line_effect_retained": 2},
        {"linked_pos_return_delta": str(returned), "held_sale_delta_if_saved": str(held)},
        {"return_delta": "1", "nonmoving_hold_delta": "0"},
        ev("Form_WPF/frmInvPOS.xaml.cs", "2503-2534") + ";" +
        ev("Form_WPF/frmInvPOS.xaml.cs", "2627-2649") + ";" +
        ev("Properties/Resources.resx", "48019-48023"),
        "Manual signs only; no DTO, caller, SQL, hold reservation policy or commit executed.")

    gross, disc, rate = D(100), D(10), D('.15')
    stale_vat, stale_total = gross * rate, gross
    base = gross - disc
    head_vat, net = base * rate, base * (1 + rate)
    detailed_base = net - stale_vat
    assert (head_vat, net, stale_vat, detailed_base) == (D('13.50'), D('103.50'), D('15'), D('88.50'))
    add(2, ["P4-003"], "Header discount with old line tax",
        {"line_base": "100", "header_discount": "10", "vat_rate": "0.15", "price_includes_vat": False},
        {"header_vat": str(head_vat), "header_net": str(net), "line_vat": str(stale_vat),
         "line_total": str(stale_total), "detailed_net_minus_old_vat": str(detailed_base)},
        {"consistent_line_base": "90", "consistent_line_vat": "13.50"},
        ev("Class/ItemOper.cs", "1533-1643") + ";" + ev("Class/InvoiceOper.cs", "2399-2422"),
        "One line, exclusive VAT, no extra tax/offers/withholding/rounding; no binder or ledger run.")

    withholding = D(2)
    sum_line_net = net - withholding
    overwritten = base + head_vat
    assert overwritten - sum_line_net == withholding
    add(3, ["P4-004"], "Withholding removed by final assignment",
        {"discounted_base": str(base), "vat": str(head_vat), "existing_line_withholding": "2"},
        {"line_net_before_final_assignment": str(sum_line_net), "header_net_after_assignment": str(overwritten)},
        {"header_equals_sum_line_net_under_same_withholding_rule": str(sum_line_net)},
        ev("Class/ItemOper.cs", "1621-1642"),
        "Does not select the legally correct withholding basis after discount or call ETA; internal arithmetic only.")

    def prefix_profit(margins: list[Decimal]) -> Decimal:
        subtotal = total = D(0)
        for margin in margins:
            subtotal += margin
            total += subtotal
        return total
    forward, reverse = prefix_profit([D(10), D(20)]), prefix_profit([D(20), D(10)])
    assert forward == 40 and reverse == 50 and forward != reverse
    add(4, ["P4-005"], "Sum of prefixes versus total profit",
        {"isolated_line_margins": ["10", "20"]},
        {"forward_order": str(forward), "reversed_order": str(reverse)},
        {"order_independent_margin_sum": "30"}, ev("Class/ItemOper.cs", "1494-1505"),
        "Ignores discounts/tax/cost lookup; does not prove which report consumes saved InvProfit.")

    with localcontext() as ctx:
        ctx.prec = 28
        mixed = (D(10)*D(6) + D(1)*D(10)) / D(11)
    assert mixed > 6
    add(5, ["P4-007"], "Incoming sales return at exchange price in average",
        {"purchase_base_qty": "10", "purchase_unit_cost": "6", "return_base_qty": "1", "return_exchange_price": "10"},
        {"illustrated_average": str(mixed)}, {"if_original_cost_return_policy": "6"},
        ev("Properties/Resources.resx", "48246-48250"),
        "Conditional valuation policy example; not moving-average/FIFO implementation or deployed SQL execution.")

    grouped = [(1, D(10), D(100)), (1, D(10), D(100)), (1, D(10), D(200))]
    dedup = set(grouped)
    expected_qty, union_qty = sum(x[1] for x in grouped), sum(x[1] for x in dedup)
    with localcontext() as ctx:
        ctx.prec = 28
        union_avg = sum(x[2] for x in dedup) / union_qty
        all_avg = sum(x[2] for x in grouped) / expected_qty
    assert (expected_qty, union_qty, union_avg) == (D(30), D(20), D(15)) and union_avg != all_avg
    add(6, ["P4-009"], "Projected aggregate deduplication after warehouse omitted",
        {"per_store_projected_rows_without_store": [[str(x) for x in row] for row in grouped]},
        {"union_quantity": str(union_qty), "union_average": str(union_avg)},
        {"union_all_quantity": str(expected_qty), "union_all_average": str(all_avg)},
        ev("Properties/Resources.resx", "48019-48021") + ";" +
        ev("Properties/Resources.resx", "48246-48250"),
        "Python set/list illustration of exact projected equal rows; no SQL NULL/float/collation/query-plan emulation.")

    rows = [{"item": 10, "product": 0}]
    legacy_before = len(rows)
    def expand() -> None:
        alias = rows
        for row in list(rows):
            if row["item"] == 10:
                alias.append({"item": 20, "product": 10})
    expand(); first = len(rows)
    expand(); second = len(rows)
    assert (legacy_before, first, second) == (1, 2, 3)
    add(7, ["P4-011"], "Repeated aliased composite expansion",
        {"parent_item": 10, "one_leaf_component": 20},
        {"legacy_items_before_first_expansion": legacy_before, "after_one_mapping": first, "after_second_mapping": second},
        {"pure_idempotent_expansion_row_count": 2}, ev("Class/InvoiceOper.cs", "4332-4409"),
        "One leaf BOM manually modeled; no actual DB, external DTO setter, recursion or save behavior executed.")

    lines = [{"item": 1, "unit": "box", "qty": D(2)}, {"item": 1, "unit": "piece", "qty": D(5)}]
    for row in lines:
        if row["item"] == 1:
            row["qty"] = D(1)
    retained = [row for row in lines if row["item"] in {1}]
    assert len(retained) == 2 and all(x['qty'] == 1 for x in retained)
    add(8, ["P4-013"], "Item-only selection keeps both original lines",
        {"selected_line": "item1/box/qty1", "second_original_line": "item1/piece/qty5"},
        {"retained_count": len(retained), "retained_quantities": [str(x['qty']) for x in retained]},
        {"only_selected_original_line_retained": 1}, ev("Form_WPF/frmInvoiceItems.xaml.cs", "315-348"),
        "Manual mutation rule; no WPF selection/binding/DTO validation or persistence run.")

    starting = D(1)
    loaded_a = loaded_b = starting
    request_a = request_b = D(1)
    a_allows, b_allows = loaded_a-request_a >= 0, loaded_b-request_b >= 0
    after_two = starting-request_a-request_b
    assert a_allows and b_allows and after_two == -1
    add(9, ["P4-014"], "Two stale snapshots without atomic reservation",
        {"initial_stock": "1", "a_reads": "1", "b_reads": "1", "each_requests": "1"},
        {"a_local_check": a_allows, "b_local_check": b_allows, "if_both_committed_stock": str(after_two)},
        {"with_negative_stock_forbidden_successful_sales_max": 1},
        ev("Class/ItemOper.cs", "1829-1902") + ";" + ev("Class/InvoiceOper.cs", "1580-1628"),
        "Abstract schedule only, not a concurrency test; assumes no server reservation/trigger and both saves succeed.")

    header_paid_before = D(50)
    header_after_open_cancel = D(0)
    refund_row_paid, refund_header_paid = D(50), D(0)
    assert header_paid_before != header_after_open_cancel and refund_row_paid != refund_header_paid
    add(10, ["P4-015", "P4-016"], "Local cancel mutation and no-dialog refund disagreement",
        {"existing_paid_invoice": "50", "new_refund_net": "50"},
        {"paid_after_open_then_cancel_rule": str(header_after_open_cancel),
         "refund_payment_row_paid": str(refund_row_paid), "refund_header_paid": str(refund_header_paid)},
        {"cancel_preserves_header": str(header_paid_before), "refund_header_matches_approved_rows": True},
        ev("Class/InvoiceOper.cs", "4682-4707") + ";" + ev("Form_WPF/frmInvPOS.xaml.cs", "2056-2076"),
        "Two isolated state illustrations; no actual modal, provider transaction, SQL insert or refund attempted.")

    product_equality, component_equality, base_qty, production_qty = D(12), D(1), D(2), D(3)
    by_unit_event = product_equality*base_qty*production_qty
    by_qty_event = production_qty*base_qty*component_equality
    assert by_unit_event == 72 and by_qty_event == 6 and by_unit_event != by_qty_event
    add(11, ["P4-022"], "Unit event versus quantity event",
        {"product_equality": "12", "component_equality": "1", "component_base_qty": "2", "production_qty": "3"},
        {"unit_event_qty": str(by_unit_event), "quantity_event_qty": str(by_qty_event)},
        {"event_order_should_not_change_quantity": True}, ev("Form_WPF/frmProductionOrder.xaml.cs", "518-573"),
        "No correct BOM basis selected; UI/source arithmetic only; actual production save is blocked by P4-020.")

    selected_qty, equality, previous = D(2), D(12), D(1)
    partial_value, full_value = selected_qty*equality, selected_qty
    cumulative_full = previous+full_value
    assert partial_value == 24 and full_value == 2 and cumulative_full == 3
    add(12, ["P4-023"], "Delivery quantity basis and full-after-partial",
        {"invoice_selected_unit_qty": "2", "unit_equality": "12", "previous_delivered_in_selected_units": "1"},
        {"partial_loader_value_tagged_with_selected_unit": str(partial_value),
         "direct_full_value": str(full_value), "if_full_added_after_partial_cumulative": str(cumulative_full)},
        {"selected_unit_total_max": "2", "remaining_selected_qty": "1"},
        ev("Form_WPF/frmInvItemsDeliveries.xaml.cs", "161-172") + ";" +
        ev("Form_WPF/frmInvoiceDeliveries.xaml.cs", "717-733"),
        "Manual quantities only; no WPF, unit interpretation, delivered status filter or SQL test executed.")
    return CASES


def lexical_parameter_checks() -> list[dict]:
    query_path = ROOT / 'SmartAuditERP/Class/StoredQueries.cs'
    prod_path = ROOT / 'SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs'
    query_source = query_path.read_text(encoding='utf-8-sig')
    prod_lines = prod_path.read_text(encoding='utf-8-sig').splitlines()
    specs = [
        ('ST4-01', 'InsertInv', 'cmd', 1358, 1423, 6,
         {'balance_previews', 'totalwithholdingtax'}),
        ('ST4-02', 'UpdateInv', 'cmd', 1358, 1423, 8,
         {'balance_previews', 'totalwithholdingtax'}),
        ('ST4-03', 'InsertInvSub', 'subCmd', 1430, 1458, 10,
         {'withholdingtax', 'withholdingtaxperc', 'itemadditionaltax', 'itemadditionaltaxperc'}),
        ('ST4-04', 'InsertInvSub', 'compCmd', 1465, 1495, 10,
         {'itempricewithoutvat', 'withholdingtax', 'withholdingtaxperc'}),
    ]
    result = []
    for ident, field, command, start, end, query_line, expected_missing in specs:
        match = re.search(r'public static string '+re.escape(field)+r'\s*=\s*"((?:[^"\\]|\\.)*)";', query_source)
        if not match:
            raise AssertionError(f'Query literal not found for lexical inspection: {field}')
        required = {p.lower() for p in re.findall(r'@([A-Za-z_]\w*)', match[1])}
        block = '\n'.join(prod_lines[start-1:end])
        supplied = {p.strip().lower() for p in re.findall(
            re.escape(command)+r'\.Parameters\.Add\(\s*"@([^"\n]+)"', block)}
        missing = required-supplied
        assert missing == expected_missing, (ident, missing, expected_missing)
        result.append({"id": ident, "finding_ids": ["P4-020"], "query_field": field,
                       "command_variable": command, "inspection_kind": "lexical-literal-name-set-difference",
                       "required_unique_parameter_names": len(required),
                       "supplied_unique_parameter_names": len(supplied),
                       "missing_required_parameters_casefolded": sorted(missing),
                       "extra_parameters_not_claimed_as_errors": sorted(supplied-required),
                       "documented_set_difference_matches": True,
                       "evidence": ev('Class/StoredQueries.cs', str(query_line))+';'+
                       ev('Form_WPF/frmProductionOrder.xaml.cs', f'{start}-{end}'),
                       "source_application_executed": False,
                       "limit": "Text-only fixed source ranges; whitespace/case normalized. No C#/SQL parse, parameter type/null checking, dynamic branches or deployed command execution."})
    return result


def main() -> None:
    cases = illustrations()
    contracts = lexical_parameter_checks()
    report = {"audit_date_utc": "2026-11-16", "through_phase": 4,
              "method": "Independent manually transcribed illustrations plus separately labelled literal-source parameter name sets; NOT ERP/C#/SQL tests",
              "illustration_count": len(cases), "illustrations": cases,
              "static_parameter_contract_check_count": len(contracts),
              "static_parameter_contract_checks": contracts,
              "application_code_imported_or_executed": False,
              "erp_runtime_tests_executed": 0, "sql_or_external_service_tests_executed": 0,
              "application_remediation_performed": False}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
