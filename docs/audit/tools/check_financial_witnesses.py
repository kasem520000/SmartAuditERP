#!/usr/bin/env python3
"""Independent algebraic illustrations for phase 3 -- NOT tests of ERP code.

The equations below were manually transcribed from cited source slices. Python
Decimal/boolean/list operations check the illustrations, not C#, WPF, SQL, DTOs,
provider rounding, deployment, transaction behaviour or accounting compliance.
No application code is imported, compiled, loaded or executed. No SQL or network.
Output goes to stdout; a caller may save it as evidence/arithmetic-witnesses-03.json.
"""
from __future__ import annotations

from decimal import Decimal as D, ROUND_HALF_EVEN
import json


def main() -> int:
    cases: list[dict] = []

    def record(n: int, title: str, findings: list[str], evidence: str,
               inputs: dict, transcribed_result: dict, reference: dict,
               limit: str) -> None:
        cases.append({
            "id": f"ALG3-{n:02d}", "title": title,
            "finding_ids": findings, "evidence": evidence,
            "inputs": inputs, "transcribed_equation_result": transcribed_result,
            "reference_or_invariant": reference,
            "illustration_assertions_passed": True,
            "source_application_executed": False, "limit": limit,
        })

    # 1. A disjunction with true cannot reject an out-of-range date.
    allowed = {name: within or True for name, within in
               (("before_start", False), ("inside", True), ("after_end", False))}
    assert list(allowed.values()) == [True, True, True]
    record(1, "Unconditional period allowance", ["P3-001"],
           "SmartAuditERP/Class/Common.cs:1289-1301",
           {"is_within_period": [False, True, False]}, allowed,
           {"allow_only_inside_open_period": [False, True, False]},
           "Boolean equivalence only; connection/UI/date parsing not exercised.")

    # 2. The live receipt binder only constructs lines for a positive Payment.
    counts = {str(p): (2 if p > 0 else 0) for p in (D("0"), D("-1"), D("100"))}
    assert counts == {"0": 0, "-1": 0, "100": 2}
    record(2, "Nonpositive receipt produces an empty line list", ["P3-002"],
           "SmartAuditERP/Class/ReceiptOper.cs:44-138;SmartAuditERP/Class/EntryOper.cs:898-920",
           {"payment": ["0", "-1", "100"], "VAT": "0"},
           {"line_counts_under_the_positive_payment_condition": counts},
           {"nonpositive_cash_receipt": "Reject before any write, unless explicitly modelled as a different document"},
           "Models the branch/list only; it does not persist or prove a deployed database accepts an empty journal.")

    # 3. Away from midpoint cases, two-decimal comparison can accept unequal raw amounts.
    debit, credit = D("100.001"), D("100.004")
    rounded_equal = (debit.quantize(D("0.01"), rounding=ROUND_HALF_EVEN) ==
                     credit.quantize(D("0.01"), rounding=ROUND_HALF_EVEN))
    assert rounded_equal and debit - credit == D("-0.003")
    record(3, "Rounded equality is not equality of stored raw values", ["P3-007"],
           "SmartAuditERP/Form_WPF/FrmNewEntry.xaml.cs:729-740;SmartAuditERP/Form_WPF/FrmNewEntry.xaml.cs:780-791;SmartAuditERP/Class/EntryOper.cs:904-905",
           {"debit": debit, "credit": credit},
           {"equal_after_two_decimal_rounding": rounded_equal, "raw_difference": debit - credit},
           {"required": "Balance the amounts actually quantized and stored under an approved currency policy"},
           "Decimal illustration, not a simulation of every .NET double/provider/midpoint or currency policy.")

    # 4. Minimal cash sale in the reclose binder, no discounts/additions/insurance.
    cash, sales, vat, custody = D("115"), D("100"), D("15"), D("115")
    lines = [
        {"role": "cash_sales", "debit": cash, "credit": D(0)},
        {"role": "sales", "debit": D(0), "credit": sales},
        {"role": "VAT_through_positive_AddAccount", "debit": vat, "credit": D(0)},
        {"role": "cash_settlement", "debit": D(0), "credit": cash},
        {"role": "closing_custody", "debit": custody, "credit": D(0)},
    ]
    sd, sc = sum(x["debit"] for x in lines), sum(x["credit"] for x in lines)
    assert (sd, sc, sd - sc) == (D(245), D(215), D(30))
    record(4, "Reclose VAT direction", ["P3-012", "P3-002"],
           "SmartAuditERP/Class/EntryOper.cs:44-55;SmartAuditERP/Class/EntryOper.cs:433-487;SmartAuditERP/Class/EntryOper.cs:603-608;SmartAuditERP/Class/EntryOper.cs:637-655;SmartAuditERP/Class/EntryOper.cs:686-693;SmartAuditERP/Class/EntryOper.cs:754-795",
           {"InvoiceType": 3, "ProcType": 1, "PayType": 1, "PaymentStatus": 1,
            "Cash": cash, "InvTotal": sales, "VAT": vat, "CashierBalance": custody,
            "other_monetary_fields": "0"},
           {"lines": lines, "debit_sum": sd, "credit_sum": sc, "difference": sd - sc},
           {"required_difference": "0", "VAT_on_positive_sale": "credit"},
           "Transcribes only this minimal, valid-account scenario; database lookups, DTO constructors and save are not run.")

    # 5. Standard network bank path (BankId <= 2), no VAT/cash/other amounts.
    sale, refund = D(100), D(20)
    bank_debit = sale + refund
    sd, sc = bank_debit + refund, sale
    assert (bank_debit, sd, sc, sd - sc) == (D(120), D(140), D(100), D(40))
    record(5, "Reclose standard-network refund is added", ["P3-013", "P3-002"],
           "SmartAuditERP/Class/EntryOper.cs:489-548;SmartAuditERP/Class/EntryOper.cs:610-618;SmartAuditERP/Class/EntryOper.cs:637-674",
           {"InvoiceType": 3, "PayType": 2, "BankId": 1, "PaymentStatus": 1,
            "sale_ProcType": 1, "refund_ProcType": 2,
            "sale_InvTotal_and_Mada": sale, "refund_InvTotal_and_Mada": refund,
            "CashierBalance": "0", "cash_VAT_and_other_amounts": "0"},
           {"bank_debit": bank_debit, "return_debit": refund,
            "sales_credit": sale, "debit_sum": sd, "credit_sum": sc, "difference": sd - sc},
           {"bank_net_debit": sale - refund, "required_difference": "0"},
           "Minimal standard-bank path only, not an assertion that every bank-ID path has the same error.")

    # 6. Prior balance exists outside the selected interval; zero current/opening movement.
    prior, opening, movement = D(100), D(0), D(0)
    leaf_final = opening + movement + prior
    parent_final = opening + movement
    secondary_only_final = opening + movement
    assert (leaf_final, parent_final, secondary_only_final) == (D(100), D(0), D(0))
    record(6, "Trial-balance carryforward lost on parent/secondary-only rows", ["P3-019"],
           "SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml.cs:292-344;SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml.cs:396-448;SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml.cs:455-486",
           {"prior_debit": prior, "opening_entries_in_interval": opening, "current_movement": movement,
            "previous_balance_requested": True},
           {"leaf_final": leaf_final, "parent_final": parent_final,
            "secondary_only_final": secondary_only_final},
           {"all_views_final": prior},
           "One leaf and its parent; does not exercise tree construction, SQL or WPF rendering.")

    # 7. ABS balances plus a subtotal row included again in the KPI.
    gross, returns, discounts = D(1000), D(100), D(50)
    total_revenue = gross + returns + discounts
    table_net_sales = total_revenue - returns - discounts
    card_revenue = total_revenue + table_net_sales
    correct_net_sales = gross - returns - discounts
    assert (table_net_sales, card_revenue, correct_net_sales) == (D(1000), D(2150), D(850))
    record(7, "Income table ignores contra revenue; KPI counts subtotal twice", ["P3-020"],
           "SmartAuditERP/Form_WPF/IncomeStatementForm.xaml.cs:295-316;SmartAuditERP/Form_WPF/IncomeStatementForm.xaml.cs:423-464;SmartAuditERP/Form_WPF/IncomeStatementForm.xaml.cs:601-605",
           {"4100001_credit": gross, "4100002_debit": returns,
            "4100003_debit": discounts, "inventory_purchases_expenses_and_other_revenue": "0"},
           {"table_net_sales": table_net_sales, "revenue_KPI": card_revenue},
           {"correct_net_sales": correct_net_sales},
           "Uses the report's stated contra-account meanings; all other P&L components zero to isolate the two equations.")

    # 8. Prior balance is Debit-Credit but liability/revenue movement is Credit-Debit.
    prior_credit, next_credit = D(100), D(50)
    carried = -prior_credit
    after_next = carried + next_credit
    without_prior = next_credit
    assert after_next == D(-50) and without_prior >= 0
    record(8, "Liability running-balance convention changes midstream", ["P3-021"],
           "SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:195-239;SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:262-274;SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:348-368",
           {"account_prefix": "2", "prior_credit": prior_credit, "new_credit": next_credit},
           {"carried_D_minus_C": carried, "after_new_C_minus_D": after_next,
            "shown_magnitude": abs(after_next), "no_prior_positive_credit_label": "مدين"},
           {"final_magnitude": prior_credit + next_credit, "nature": "دائن"},
           "Algebra/display-label illustration, not a rendering or account-statement acceptance test.")

    print(json.dumps({
        "audit_date_utc": "2026-11-16",
        "method": "Independent manually transcribed algebra only; NOT source/application/runtime acceptance tests",
        "illustration_count": len(cases), "illustrations": cases,
        "erp_runtime_tests_executed": 0, "sql_or_external_service_tests_executed": 0,
        "application_code_imported_or_executed": False,
        "note": "Passed assertions mean the illustrations are arithmetically self-consistent, not that the ERP passed or failed an executed test.",
    }, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
