#!/usr/bin/env python3
"""24 independent manual illustrations +24 bounded lexical B15 observations.

ONLY stdlib/inert source reads, not a translation/interpreter of C#/SQL/WPF.
No application import/build/runtime/REPX/Office/COM/provider/device/printer/
formula/HTML/shell/business export/real data/secrets/measurement/remediation.
Invented dates, employees and amounts are not production or current-day facts.
"""
from __future__ import annotations
from datetime import date, datetime, timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
F = 'SmartAuditERP/Form_WPF/'
C = 'SmartAuditERP/Class/'
P, PX = F + 'FrmReseved.xaml.cs', F + 'FrmReseved.xaml'
T, TX = F + 'frmTaxRptPeriod.xaml.cs', F + 'frmTaxRptPeriod.xaml'
D, DX = F + 'frmTaxInvDetails.xaml.cs', F + 'frmTaxInvDetails.xaml'
RS, EO, PR = C + 'Reseved.cs', C + 'EntryOper.cs', C + 'Print.cs'
RD, TD = C + 'resvdPrint.cs', C + 'RptTaxData.cs'
H, HX, MC = 'SmartAuditERP/Home.xaml.cs', 'SmartAuditERP/Home.xaml', C + 'MainClass.cs'
RES = 'SmartAuditERP/Properties/Resources.resx'
LIMIT = ('مثال يدوي مستقل بموظفين ومبالغ وتواريخ خيالية؛ ليس ترجمة أو تشغيل C#/SQL/WPF أو قبولاً مالياً. '
         'لا سياسة رواتب أو فئة ضريبة قانونية مفترضة. الوالدان C# كامل سابقاً7A/B1؛ الطفل مقاطع لا كل العقود، '
         'وHome الحالي يفتحfrmVATReturn لا الوالد المحلي. R1/R2 ببقايا، و7C لم تبدأ و8 غير مأذونة. '
         'لا اعتماديات أو مخطط نشر أو طباعة أو بيانات أعمال أو قياس أو معالجة فُعّلت.')
TEXT_LIMIT = ('tokens في نطاقات نصية محددة فقط، لا semantic AST/callgraph/compile/overload resolution '
              'أو SQL/WPF rendering أو تفويض نشر أو صحة مالية أو حكم latency/leak/index.')


def ref(*triples):
    return ';'.join(f'{p}:{a}-{b}' for p, a, b in triples)


class Witness:
    def __init__(self):
        self.alg, self.lex, self.errors, self.reads = [], [], [], {}

    def require(self, ok, message):
        if not ok:
            self.errors.append(message)

    def text(self, path, start, end):
        lines = (ROOT / path).read_text(encoding='utf-8-sig').splitlines()
        self.require(1 <= start <= end <= len(lines), 'Bounded read: ' + path)
        value = '\n'.join(lines[start-1:end])
        self.reads[(path, start, end)] = dict(path=path, start=start, end=end,
                                              selected_text_sha256=hashlib.sha256(value.encode()).hexdigest())
        return value

    def illustration(self, n, title, roots, evidence, ok, details):
        self.require(ok, 'ALG ' + str(n))
        self.alg.append(dict(id=f'ALG7B15-{n:02d}', title=title, finding_ids=roots, evidence=evidence,
                             illustration_assertions_passed=bool(ok), details=details,
                             source_application_executed=False, limit=LIMIT))

    def lexical(self, n, title, roots, checks, absent=(), observation=None):
        ok, refs = True, []
        for path, start, end, tokens in checks:
            text = self.text(path, start, end)
            refs.append((path, start, end))
            for token in tokens:
                ok = (token in text) and ok
        for path, start, end, tokens in absent:
            text = self.text(path, start, end)
            refs.append((path, start, end))
            for token in tokens:
                ok = (token not in text) and ok
        if observation:
            ok = bool(observation['matches']) and ok
        self.require(ok, 'ST ' + str(n))
        row = dict(id=f'ST7B15-{n:02d}', title=title, finding_ids=roots, evidence=ref(*dict.fromkeys(refs)),
                   documented_text_observation_matches=bool(ok), source_application_executed=False, limit=TEXT_LIMIT)
        if observation:
            row['additional_inert_text_observation'] = observation
        self.lex.append(row)


def build():
    w = Witness()
    a, l = w.illustration, w.lexical
    requested, reset_current = (2025, 2), (2026, 5)
    a(1, 'عرض فترة صالحة لا يساوي reset إلى الفترة الحالية', 'P7-123', ref((P, 76, 104), (P, 226, 259), (P, 303, 307), (PX, 239, 260), (PX, 484, 489)),
      requested != reset_current,
      dict(invented_requested_period=requested, invented_system_period=reset_current,
           manual_local_query_period=reset_current, reference_query_period=requested,
           controls_also_reset_not_falsely_claimed_unchanged=True, not_parse_failure=True))
    try:
        date(2026, 2, 31)
        invalid_in_stdlib_only = False
    except ValueError:
        invalid_in_stdlib_only = True
    a(2, 'يوم31 غير موجود في فبراير ولا يثبت إعادة حسابه', 'P7-124', ref((P, 226, 244), (P, 374, 429)),
      invalid_in_stdlib_only and Decimal('100') != Decimal('200'),
      dict(invented_system_day=31, selected_period=[2026, 2], prior_amount='100', required_recomputed_amount='200',
           manual_event_order=['change-selection', 'rewrite-notes', 'impossible-date', 'skip-reload', 'old-selected-row-stays'],
           save_period_reads_live_selection=True, python_date_counterexample_not_DotNet_execution=True,
           validity_workdate_positive_net_assumed_only_for_example=True, prior_null_posting_root_not_assumed_fixed=True))
    a(3, 'اختيار فرعB مع قبض فرعA يخلط مكونات الإقرار', 'P7-125', ref((T, 273, 307), (T, 499, 523), (T, 557, 563), (T, 708, 724)),
      200 + 10 == 210 and 200 + 30 == 230 and Decimal('30') + Decimal('1.5') != Decimal('34.5'),
      dict(invented_session_branch='A', allowed_selected_branch='B', invoices_B_base=200,
           receipts_A_base=10, receipts_B_base=30, local_mixed_base=210, reference_B_base=230,
           local_mixed_vat='31.5', reference_B_vat='34.5', legal_rate_not_inferred=True,
           parent_instantiation_and_successful_lookup_are_conditions_not_runtime_facts=True))
    a(4, 'ربع→شهر:Unchecked الآخر يعطل القائمة الجديدة', 'P7-126', ref((T, 895, 927), (TX, 333, 387)),
      [True, False][-1] is False,
      dict(manual_month_combo_enable_assignments=[True, False], final_month_checked=True, final_quarter_checked=False,
           final_both_combos_enabled=False, final_date_edit_enabled=False,
           trace=['month-checked:enable-month', 'uncheck-previously-checked-quarter', 'quarter-unchecked:disable-both'],
           first_enable_without_other_checked_can_work=True, not_WPF_event_execution=True))
    a(5, 'كل الفروع لا يعني branch=-1 ولا فرع الجلسة', 'P7-125;P2-010', ref((T, 273, 307), (T, 499, 523), (T, 937, 943)),
      100 + 200 + 10 == 310 and 100 + 200 + 10 + 30 == 340,
      dict(local_all_with_session_A=310, reference_authorized_A_B=340, sentinel_minus1_is_not_all_equality=True,
           branch_minus1_rows_not_assumed_absent=True, allowed_set_not_derived_from_UI=True,
           canonical_id_BranchId_Code_contract_unresolved=True))
    a(6, 'شهر→ربع والضبط الأول حالتان مختلفتان', 'P7-126', ref((T, 895, 927), (TX, 333, 387)),
      dict(quarter_enabled=False, monthly_enabled=False) != dict(quarter_enabled=True, monthly_enabled=False),
      dict(manual_quarter_combo_enable_assignments=[True, False], final_quarter_checked=True,
           dates_reenabled_by_month_unchecked=True, previous_other_checked_required=True,
           repeated_assignment_false_to_false_does_not_imply_same_event=True,
           first_quarter_activation_reference=dict(quarter_enabled=True, monthly_enabled=False),
           options_present=dict(quarters=4, months=12), not_missing_options_or_index_mapping=True))
    a(7, 'نوع الصف وعقد نتيجة القيد لا يصلحهما نص النجاح', 'P7-001;P3-002', ref((P, 355, 429), (P, 875, 904), (RS, 224, 267), (RS, 296, 345)),
      'FrmReseved.SalaryRow' != 'System.Data.DataRow' and bool(None) is False,
      dict(manual_supplied_type='FrmReseved.SalaryRow', binder_expected='System.Data.DataRow',
           binder_error_returns=None, local_skip_null_allows_document_success=True,
           bool_SaveReceipt1_not_checked_by_caller=True, no_cast_exception_or_SQL_executed=True))
    a(8, 'تحقق صف بعد اعتماد السابق ليس validate-all/commit-all', 'P3-003', ref((P, 374, 429), (P, 446, 494), (RS, 131, 267), (EO, 850, 935)),
      ['employee-A'] != [],
      dict(manual_rows=[dict(employee='A', valid=True), dict(employee='B', valid=False)],
           sequential_write_before_second_validation=['employee-A'], reference_atomic_failed_batch=[],
           journal_transaction_exists_but_separate=True, delete_has_real_SalaryPay_guard=True,
           no_fault_injection_or_persisted_rows_observed=True))
    a(9, 'معرف مبني من رقم عرض أقدم قد لا يطابق رقم الحفظ', 'P3-005', ref((P, 110, 129), (P, 355, 385), (P, 819, 835), (EO, 1264, 1289)),
      '1-5' != '1-6',
      dict(invented_preview_next_id=5, invented_later_next_id=6, global_from_preview='1-5', saved_header_numeric_id=6,
           reference_allocate_once=['1-6', 6], concurrent_writer_not_executed=True,
           existing_MAX_check_not_atomic_reservation=True))
    a(10, 'DataView مرئي ومصدر حفظ فارغ ليسا نموذجاً واحداً', 'P7-002', ref((F+'frmRptReseved.xaml.cs', 155, 173), (P, 37, 64), (P, 76, 104), (PX, 329, 357)),
      len(['visible-row']) == 1 and len([]) == 0,
      dict(manual_visible_source='DataView', internal_salary_source=[], visible_data_rows=1,
           reset_hidden_identity='', selected_save_source_count=0,
           not_claiming_CLR_removes_DataView=True, current_period_defaults_do_not_restore_loaded_period=True))
    a(11, 'إعادة تحميل Emp المفقود لا تستعيد هوية7', 'P7-003', ref((P, 493, 543), (P, 600, 624), (P, 660, 721), (P, 755, 813)),
      0 != 7,
      dict(invented_query_employee_id=7, unassigned_int_default=0, saved_if_reselected=0,
           bank_lookup_uses_row_Emp=True, reloaded_rows_default_unselected=True,
           no_employee_zero_or_deployed_FK_assumed=True))
    a(12, 'طباعة كل الصفوف ليست اختيار الحفظ الجزئي', 'P7-045', ref((P, 355, 370), (P, 583, 655), (T, 700, 749)),
      100 + 200 == 300 and 300 != 100,
      dict(invented_rows=[dict(employee='A', amount=100, selected=True), dict(employee='B', amount=200, selected=False)],
           intended_saved_subset_total=100, local_print_source_all_total=300,
           dirty_date_metadata_can_differ_from_saved_snapshot=True, hidden_global_presence_not_snapshot_validation=True,
           not_assuming_previous_binding_success=True))
    base = Decimal('100')
    header_divided = base / Decimal('1.15')
    a(13, 'بند0% لا يقسم بمعدل رأس15% وخصمه ليس صفراً تلقائياً', 'P7-043', ref((T, 345, 420), (C+'InvoiceOper.cs', 1595, 1602), (C+'ItemOper.cs', 1389, 1421)),
      header_divided != base and base - Decimal('10') == 90,
      dict(invented_no_tax_line='100', invented_header_rate='15', local_no_tax_base=str(header_divided),
           reference_no_tax_base='100', header_discount_example='10', local_exempt_after_ignored_discount='100',
           reference_if_policy_allocates_all_to_exempt='90', legal_classification_and_mixed_discount_policy_unresolved=True,
           per_invoice_PriceIncVAT_is_used_not_current_setting=True))
    a(14, 'الإجمالي المسمي للمبيعات لا يساوي إسقاط المعفى', 'P7-044', ref((T, 557, 563), (T, 649, 655), (T, 708, 740), (TX, 573, 608), (TX, 714, 751)),
      100 + 70 == 170 and 100 != 170,
      dict(invented_taxed_base=100, invented_no_tax_base=70, local_total_base=100, reference_row_sum=170,
           no_tax_VAT=0, VAT_need_not_change_when_base_total_changes=True, not_double_counting_subtotal=True))
    a(15, 'شامل115 وضريبة15 ليسا أساس115 قبل الضريبة', 'P7-051', ref((T, 524, 563), (T, 708, 722), (TX, 635, 681)),
      115 - 15 == 100 and 115 != 100,
      dict(invented_rental_total_includes_VAT=115, stored_tax=15, local_base_cell=115,
           reference_base_if_inclusive_contract=100, other_rental_insurance_additions_types_not_certified=True))
    a(16, 'خليتان من جيلين لا تصبحان تقريراً صحيحاً تحت عنوانB', 'P7-046', ref((T, 427, 523), (T, 649, 675), (T, 700, 749)),
      dict(sale=200, tax=15) != dict(sale=200, tax=30),
      dict(manual_old_A=dict(sale=100, tax=15), requested_B=dict(sale=200, tax=30),
           partial_publish_if_late_source_fails=dict(sale=200, tax=15), required_health='failed-or-explicit-partial',
           zero_parse_fallback_not_valid_zero_proof=True, no_database_fault_injection=True))
    end = datetime(2026, 1, 31)
    midnight_next = end + timedelta(days=1)
    late = end + timedelta(hours=23, minutes=59, seconds=59, microseconds=999000)
    following_noon = midnight_next + timedelta(hours=12)
    child_to = end + timedelta(hours=23, minutes=59, seconds=59)
    a(17, 'مدى الأب السليم ونافذةPOS الطفل الموسعة مختلفان', 'P3-023', ref((P, 150, 189), (T, 268, 269), (T, 450, 464), (D, 238, 275), (D, 521, 585)),
      end <= late < midnight_next and not (late < child_to) and following_noon < child_to + timedelta(hours=24) and not (following_noon < midnight_next),
      dict(parent_half_open_includes_last_fraction=True, parent_excludes_next_day=True,
           child_main_exclusive_235959_loses_fraction=True, child_POS_plus24_includes_next_day_noon=True,
           culture_and_calendar_not_runtime_certified=True))
    a(18, 'نقل تاريخين لا ينقل BranchSet أو أهلية مصادر الأب كلها', 'P7-045;H7B15-04', ref((T, 847, 887), (D, 77, 151), (D, 208, 306), (DX, 179, 214), (DX, 252, 272)),
      dict(branch='B', types=[2, 3, 20, 21, 22]) != dict(branch='all', types=[2, 3, 20]),
      dict(manual_parent_request=dict(branch='B', types=[2, 3, 20, 21, 22]),
           selected_child_defaults_after_LoadBranches=dict(branch='all', types=[2, 3, 20]),
           dates_forwarded=True, branch_not_forwarded_in_selected_callers=True,
           subset_may_be_legitimate_if_declared=True, no_forced_parent_child_total_equality=True,
           child_body_and_output_not_wholly_reviewed=True))
    a(19, 'تعريف البنك الحالي ليس لقطة الإصدار السابقة', 'P7-032', ref((P, 583, 655), (RD, 3, 30)),
      'synthetic-bank-at-issue' != 'synthetic-bank-now',
      dict(inert_old_bank_label='synthetic-bank-at-issue', inert_current_bank_label='synthetic-bank-now',
           local_reprint_master_source='current-Employees', immutable_issued_snapshot_not_read_here=True,
           policy_for_current_vs_historical_reprint_unresolved=True, real_bank_data_used=False))
    a(20, 'ملف قالب موجود أوcopies مستهلكة لا يثبتان نجاحoutput أوflags', 'P1-004;P7-031;H7B15-03', ref((P, 547, 585), (PR, 148, 221), (T, 180, 211), (T, 760, 817), (RD, 1, 32), (TD, 1, 46)),
      2 > 0 and 'file-exists' != 'spool-accepted',
      dict(local_DTO_property_counts=dict(resvdPrint=26, RptTaxData=35), copies_positive_example=2,
           copies_are_consumed=True, tax_subreports_loaded_without_flag_guard=True,
           external_template_shape_unknown=True, print_helper_error_outcome_not_returned=True,
           no_REPX_or_printer_execution=True))
    a(21, 'أسماءIconButton وForms seed لا تثبتان حارسcommand أوcaller', 'P1-013;P2-001;P2-010;H7B15-05', ref((PX, 500, 526), (MC, 416, 455), (H, 2706, 2713), (RES, 2825, 2825), (HX, 345, 345)),
      'IconButton5' != 'btnSave' and 'frmVATReturn' != 'frmTaxRptPeriod',
      dict(local_save_control_name='IconButton5', name_guard_expected='btnSave',
           Forms_seed_parent='frmTaxRptPeriod', Home_tax_handler_target='frmVATReturn', tax_menu_initially_disabled=True,
           no_production_reachability_or_ACL_bypass_asserted=True, branch_filter_not_allowed_set=True))
    a(22, 'الدقة والأهلية والفئة الضريبية عقود لا أسماءحقول', 'P3-007;H7B15-01;H7B15-02', ref((P, 150, 219), (RS, 201, 231), (RES, 4539, 4553), (T, 345, 420), (TX, 787, 860)),
      Decimal('0.1') + Decimal('0.2') == Decimal('0.3') and (0.1 + 0.2) != 0.3,
      dict(stdlib_decimal_sum='0.3', stdlib_binary_float_sum=repr(0.1+0.2), not_DotNet_or_SQL_precision_test=True,
           zero_tax_category='unknown-without-policy', selected_salary_column_not_entitlement_proof=True,
           blank_previous_period_not_no_business_proof=True, jurisdiction_not_inferred_from_location=True))
    a(23, 'حلقات مصدر مرشحة للقياس لا زمن مقاس', 'H7B15-05', ref((P, 588, 624), (T, 345, 395), (T, 460, 488), (P, 57, 69), (PX, 13, 14)),
      3 * 2 == 6 and 1 + 3 == 4,
      dict(invented_three_invoices_two_part_queries_each=6, invented_three_employees_Foundation_plus_bank_queries=4,
           excludes_other_sources_and_helpers=True, observed_SQL_roundtrips=0, latency_measurements=0,
           index_or_leak_verdict='not-measured', Closing_closes_connections_is_positive_not_dispose_or_leak_certification=True,
           C_axes_not_started=True))
    a(24, 'زوالفئتيالعمقليسصفراًفيالعقودالمتبقية', 'H7B15-06', 'none-inventory-only',
      2 - 2 == 0 and 1876 + 1441 == 3317 and 392 + 3 == 395 and 827 - 395 == 432,
      dict(old_categories_at_entry=2, of_them_prior_full_CSharp=2, B15_own_xaml_contract_upgrades=2,
           newly_full_parent_CSharp=0, remaining_old_category=0, remaining_contracts_not_zero_or_closed=True,
           scope_paths=20, overlaps=17, new_paths=3, union=395, complement=432,
           B_planning_groups=4, R1_R2_status='bounded-local-delivered-residuals-open', C_unstarted_axes=6,
           counts_not_sessions_or_completion_percent=True, historical_protected_artifacts=413, immutable_core_rows=294))

    l(1, 'عرض يستعملCLR وdefaults شهر/سنة رغم خيارات صالحة', 'P7-123', [
        (P, 23, 50, ('_loaded        = false', 'ObservableCollection<SalaryRow>')),
        (P, 76, 104, ('DateTime.Now.Month', 'cmbMonth.SelectedIndex = currentMonth - 1', 'DateTime.Now.ToString("yyyy")')),
        (P, 303, 307, ('_loaded = true', 'CLR();', 'LoadEmpData(cond);')),
        (PX, 239, 260, ('SelectionChanged="cmbMonth_SelectionChanged"', 'Content="12"')),
        (PX, 484, 489, ('Click="BtnAll_Click"',))])
    l(2, 'تغييرNotes ثمNow.Day ثمLoad داخلcatchفارغ', 'P7-124', [
        (P, 226, 244, ('row.Notes = note', 'new DateTime(year, month, DateTime.Now.Day)', 'LoadEmpData(cond);', 'catch { }')),
        (P, 374, 429, ('ValidateWorkDate(row.Emp)', '_Month        = GetSelectedMonthInt()', '_year         = GetSelectedYearInt()', '_Net          = row.Net_Sal')),
        (PX, 242, 251, ('SelectionChanged="cmbMonth_SelectionChanged"',))])
    l(3, 'مصدرقبض10يثبتMainBranchخلافhelpersالفروع', 'P7-125', [
        (T, 273, 307, ('GetBranchConditionInv', 'cmbBranches.SelectedValue', 'GetBranchConditionBranchID')),
        (T, 444, 455, ('string branchBranch', 'GetBranchConditionBranchID()')),
        (T, 499, 523, ('ReceiptType=10 AND branchID={MainClass.BranchNo}', 'txtReceiptsVAT')),
        (T, 608, 642, ('{branchBranch}', '{branchEntry}')),
        (TX, 220, 236, ('Checked="chkAllBranches_CheckedChanged"', 'Unchecked="chkAllBranches_CheckedChanged"'))],
        [(T, 499, 523, ('{branchBranch}', 'cmbBranches.SelectedValue', 'chkAllBranches'))])
    quarter_options = w.text(TX, 344, 354).count('<ComboBoxItem ')
    month_options = w.text(TX, 369, 387).count('<ComboBoxItem ')
    l(4, 'Checked/Uncheckedمتبادلانبعدتمكينالقائمةوخيارات4/12موجودة', 'P7-126', [
        (TX, 333, 387, ('Checked="ckQuart_CheckedChanged"', 'Unchecked="ckQuart_CheckedChanged"', 'Checked="ckMonthly_CheckedChanged"', 'Unchecked="ckMonthly_CheckedChanged"')),
        (T, 895, 927, ('cmbMonthly.IsEnabled = true', 'ckQuart.IsChecked = false', 'cmbQuartars.IsEnabled = true', 'ckMonthly.IsChecked = false')),
        (T, 827, 837, ('ShowDetails22();',))], observation=dict(matches=quarter_options == 4 and month_options == 12,
                                                            inert_quarter_option_count=quarter_options, inert_month_option_count=month_options))
    l(5, 'SalaryRow إلىDataRow وnullلايمنعSaveReceipt1', 'P7-001', [
        (P, 355, 429, ('new ArrayList()', 'selectedRows.Add(row)', 'reseved.SaveReceipt1(resvd, reseved.BindreservedToEntry')),
        (P, 875, 904, ('public class SalaryRow', 'public int     Emp')),
        (RS, 296, 345, ('dataRow = (DataRow)dt[i]', 'result = null')),
        (RS, 224, 267, ('if (Entr != null', 'result = true'))],
        [(P, 355, 429, ('if (!reseved.SaveReceipt1',))])
    l(6, 'تحققصفوكتابةثمصفآخرومعاملةقيدمستقلة', 'P3-003', [
        (P, 374, 429, ('foreach (SalaryRow row in selectedRows)', 'ValidateWorkDate', 'SaveReceipt1')),
        (RS, 131, 267, ('MainClass.ConnObj()', 'sqlCommand.ExecuteNonQuery()', 'new EntryOper().SaveEnty')),
        (EO, 850, 935, ('conn.BeginTransaction()', 'transaction.Commit()', 'transaction.Rollback()')),
        (P, 446, 494, ('SELECT COUNT(*) FROM SalaryPay', 'UPDATE Salary_Res', 'UPDATE Entry'))])
    l(7, 'callerDataViewقبلShowوCLRهويةومصدرودوناستعادةmonth/year', 'P7-002', [
        (F+'frmRptReseved.xaml.cs', 155, 173, ('new FrmReseved()', 'detailDt.DefaultView', 'frmReseved.Show()')),
        (P, 57, 104, ('CLR();', '_salarySource.Clear()', 'TxtGlobalID.Text      = ""')),
        (F+'frmRptEntries.xaml.cs', 591, 600, ('frm.Show()', 'SR.month, SR.year')),
        (P, 736, 757, ('txtDate.DateTime', 'IsNew = false'))],
        [(P, 736, 757, ('cmbMonth', 'cmbYear'))])
    l(8, 'E.idموجودلكنEmpغيرمسندفيمنشئيreload', 'P7-003', [
        (P, 660, 689, ('ISNULL(E.id,0)', 'SELECT')),
        (P, 689, 715, ('_salarySource.Add(new SalaryRow', 'Empnam')),
        (P, 762, 780, ('ISNULL(E.id,0)',)),
        (P, 791, 804, ('_salarySource.Add(new SalaryRow', 'Empnam')),
        (P, 600, 624, ("WHERE id='{row.Emp}'", 'CardNo', 'BankNo'))],
        [(P, 689, 715, ('Emp =', 'Emp=', 'Emp        =', 'Emp       =')),
         (P, 791, 804, ('Emp =', 'Emp=', 'Emp        =', 'Emp       ='))])
    l(9, 'MAX+1ورقمعرضقبلرقمحفظبلاreservation', 'P3-005', [
        (P, 110, 129, ('SELECT ISNULL(MAX(id),0)', 'resNo      = num')),
        (P, 355, 385, ('{MainClass.BranchNo}-{txtNo.Text}', 'resNo = (int)MaX_ID')),
        (P, 819, 835, ('SELECT MAX({columnName}) FROM {tableName}',)),
        (EO, 1264, 1289, ('SELECT ISNULL(MAX(id), 0)', 'entryNo++', 'SELECT COUNT(*)'))])
    l(10, 'updateبالمعرفواستبدالبنودالقيددونexpected-versionمحلي', 'P3-006', [
        (RS, 170, 231, ('update  Salary_Res set', 'update  Salary_Res_Details set', 'where GlobalID=@GlobalID')),
        (EO, 862, 908, ('DELETE FROM Entry_Sub', 'StoredQueries.UpdateEntry'))],
        [(RS, 170, 231, ('expectedVersion', 'rowversion')), (EO, 862, 908, ('expectedVersion',))])
    l(11, 'decimalواجهةوSqlDbType.FloatوDDLfloat', 'P3-007', [
        (P, 888, 907, ('public decimal BasicSal', 'public decimal Sal_Sub')),
        (RS, 201, 231, ('SqlDbType.Float', 'rs._Basic', 'rs._Net')),
        (RES, 4539, 4553, ('[Basic] [float]', '[Net] [float]')),
        (T, 649, 663, ('Math.Round(', 'ToString(Common.DigitsNo)'))])
    l(12, 'نصفمدىالأبسليمحدياًوPOSالطفليضيفيوماًآخر', 'P3-023', [
        (P, 150, 189, ('new DateTime(year, month, 1)', 'SqlDbType.Date', 'endDate.AddDays(1)')),
        (T, 268, 269, ('txtDateFrom.DateTime.Date', 'txtDateTo.DateTime.Date.AddDays(1)')),
        (T, 450, 464, ('date>=@date1 AND date<@date2', 'date2')),
        (D, 238, 275, ('23:59:59', 'toDate.AddHours(24)')),
        (D, 521, 585, ('toDate.AddHours(24).ToShortDateString()',))])
    l(13, 'CalcيستخدمعلمالرأسالمحفوظوNOTAXينقسمبمعدله', 'P7-043', [
        (T, 345, 420, ('invRow["PriceIncVAT"]', 'invRow["VATPercent"]', 'Inv_Sub.taxval = 0', 'if (filterVatMode == "TAXED") baseNet -= minusBase', 'totalBase /= 1.0 + vatPercent / 100.0')),
        (C+'InvoiceOper.cs', 1545, 1571, ('inv.PriceIncVAT', 'inv.VATperc')),
        (C+'InvoiceOper.cs', 1595, 1602, ('invoiceItem.ItemQuantity', 'invoiceItem.ItemPrice', 'invoiceItem.ItemVat'))],
        [(T, 345, 420, ('PricIncVATSale', 'PricIncVATPOS'))])
    l(14, 'المعفىإلىA5/C5وإجماليA6/C6منمجموعبدونه', 'P7-044', [
        (T, 557, 563, ('SafeDouble(txtNetSale.Text)', 'SafeDouble(txtReceipts.Text)', 'SafeDouble(txtIncomes.Text)')),
        (T, 649, 655, ('SafeDouble(txtNetPurch.Text) + expTotal',)),
        (T, 708, 740, ('A5 = GetCellText(txtSalesOutTax)', 'A6 = GetCellText(txtNetSales)', 'C5 = GetCellText(txtPurchOutTax)', 'C6 = GetCellText(txtNetPurches)')),
        (TX, 573, 608, ('المشتريات المعفاة', 'اجمالي المشتريات')),
        (TX, 714, 751, ('المبيعات المعفاة', 'إجمالي المبيعات'))])
    l(15, 'renttot_netفيعمودصافيA2والضريبةبجانبهاB2', 'P7-051', [
        (T, 524, 563, ('SUM(tot_net)', 'SUM(tax)', 'SetCellText(txtIncomes,', 'proc_type=2')),
        (T, 708, 722, ('A2 = GetCellText(txtIncomes)', 'B2 = GetCellText(txtIncomesVAT)')),
        (TX, 635, 681, ('الصافي', 'txtIncomes', 'txtIncomesVAT'))])
    l(16, 'selected-saveوall-printومعاييرDTOوطلبطفلغيركامل', 'P7-045', [
        (P, 355, 370, ('row.IsSelected', 'selectedRows.Add(row)')),
        (P, 583, 655, ('foreach (var row in _salarySource)', 'Dateresevd = txtDate.DateTime.ToString()')),
        (T, 700, 749, ('FromDate = txtDateFrom.DateTime', 'ToDate = txtDateTo.DateTime')),
        (T, 847, 887, ('frm.Invtype = 2', 'frm.Invtype = 1', 'frm.ckTotalPeriod.IsChecked = false', 'frm.ShowInvs()')),
        (D, 130, 151, ('cmbBranches.SelectedIndex     = -1',))],
        [(T, 847, 887, ('frm.cmbBranches', 'frm.chkAllBranches'))])
    l(17, 'SafeDouble0ونشرخلاياقبلcatchوcatchسطرطفل', 'P7-046', [
        (T, 328, 338, ('return 0.0', 'double.TryParse', 'int.TryParse')),
        (T, 492, 523, ('SetCellText(txtNetSale', 'SetCellText(txtReceipts')),
        (T, 649, 675, ('SetCellText(txtNetPurches', 'catch (Exception ex)')),
        (D, 282, 290, ('ProcessInvoiceRow', 'catch { }')),
        (D, 521, 614, ('catch { }',))])
    l(18, 'FoundationوEmployeebankالحاليانوقتprint', 'P7-032', [
        (P, 583, 655, ('SELECT * FROM Foundation', "WHERE id='{row.Emp}'", 'Common.GetEmpName(MainClass.EmpNo)', 'BankAcc    = bankNo')),
        (RD, 3, 30, ('BankAcc', 'CardNo', 'PrintDate'))])
    l(19, 'Print.Printingيرجعvoidويلتقطفشلالقالبأوالطابعة', 'P7-031', [
        (P, 547, 585, ('File.Exists(path)', '_print.Printing(printType, BindToData()')),
        (PR, 148, 221, ('public void Printing(', 'XtraReport.FromFile', 'xtraReport.Print()', 'catch (Exception projectError)', 'ProjectData.ClearProjectError()'))])
    rd_names = re.findall(r'public string (\w+) \{ get; set; \}', w.text(RD, 1, 32))
    td_names = re.findall(r'public string (\w+) \{ get; set; \}', w.text(TD, 1, 46))
    l(20, 'DTOsمحلية26/35وقوالبوcopiesتستهلكفعلاً', 'P1-004;H7B15-03', [
        (RD, 1, 32, ('class resvdPrint', 'BankAcc')),
        (TD, 1, 46, ('class RptTaxData', 'A6', 'D6')),
        (PR, 54, 145, ('SettingPrint where Inv_Id=', 'PrintHeader', 'PrintNo')),
        (T, 180, 211, ('SettingPrint WHERE Inv_Id=14', 'PrintHeader', 'PrintNo')),
        (T, 760, 817, ('MainClass.ReportsPath', 'TaxRptPeriod.repx', 'header.repx', 'footer.repx', 'i <= PrintNo'))],
        observation=dict(matches=len(rd_names) == 26 and len(td_names) == 35,
                         local_resvdPrint_property_count=len(rd_names), local_RptTaxData_property_count=len(td_names)))
    l(21, 'IconButtonnameوApplyقبلShowوHomeينشئالبديل', 'P1-013;P2-001', [
        (PX, 500, 526, ('x:Name="IconButton5"', 'x:Name="IconButton7"', 'x:Name="IconButton6"', 'x:Name="IconButton3"')),
        (MC, 416, 455, ('name == "btnSave"', 'name == "btnDelete"', 'VisualTreeHelper.GetChildrenCount')),
        (T, 847, 887, ('MainClass.ApplyPermissionToForm(frm)', 'frm.Show()')),
        (H, 2706, 2713, ('new frmVATReturn()',)),
        (HX, 345, 345, ('IsEnabled="False"',)),
        (RES, 2825, 2825, ("N'frmTaxRptPeriod'",))])
    l(22, 'BranchIdASIdمقابلidوعينةكاتبBranchIDلاACLنشر', 'P2-010;H7B15-05', [
        (T, 129, 151, ('SELECT BranchId AS Id', 'cmbBranches.SelectedValue = MainClass.BranchNo')),
        (D, 130, 151, ('SELECT id, name FROM Branches', 'Accounting.BranchCondition')),
        (RES, 242, 275, ('[id] [int] IDENTITY', 'BranchId int null', 'Code varchar')),
        (F+'frmSandVAT.xaml.cs', 709, 808, ('"@BranchID", MainClass.BranchNo', '"@Payment", payVal', '"@NetVal", netVal'))])
    l(23, 'اتصالانمحليانوClosingمربوطواستعلاماتداخلحلقات', 'H7B15-05;P1-030', [
        (P, 44, 69, ('conn   = MainClass.ConnObj()', 'conn1  = MainClass.ConnObj()', 'conn?.Close()', 'conn1?.Close()')),
        (PX, 13, 14, ('Closing="Window_Closing"',)),
        (P, 588, 624, ('foreach (var row in _salarySource)', 'SELECT ISNULL(CardNo')),
        (T, 460, 488, ('foreach (DataRow row in dt.Rows)', 'CalcInvoicePart(row, "TAXED")', 'CalcInvoicePart(row, "NOTAX")')),
        (H, 239, 243, ('_FrmReseved ??',))])
    l(24, 'ثوابتوفراغاتالمرحلوextraVATدونسياسةقالبمصادق', 'H7B15-02;H7B15-03', [
        (TX, 787, 860, ('Label14', 'Label63', 'Label64', 'txtExtraVAT', 'Text=" "')),
        (T, 708, 749, ('E = GetCellText(Label64)', 'F = GetCellText(Label63)', 'G = GetCellText(Label14)', 'H = GetCellText(txtNetTax)'))],
        [(TD, 1, 46, ('public string ExtraVAT', 'public string BranchID'))])
    return dict(
        phase='7B15-partial-static-audit', application_code_imported_or_executed=False,
        application_remediation_performed=False, real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False, erp_runtime_tests_executed=0,
        sql_or_external_service_tests_executed=0, parents_csharp_already_full_7A_B1=True,
        child_selected_slices_not_parent_depth=True, tax_home_route_is_alternate_not_parent_certified=True,
        B_R1_R2_residual_contracts_not_closed=True, supplied_sql_not_certified_deployed=True,
        progress_categories_not_wholly_unread_counts=True,
        parent_source_lines_not_first_coverage=dict(csharp=1876, xaml=1441, total=3317),
        illustration_count=len(w.alg), static_lexical_contract_check_count=len(w.lex),
        illustrations=w.alg, static_lexical_contract_checks=w.lex,
        bounded_source_reads_not_semantic_coverage=list(w.reads.values()),
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2, equality=12, base_unit_cost=5,
                                                      local_cost=10, reference_cost=120, archive_rewritten=False),
        errors=w.errors, limit=LIMIT,
    )


if __name__ == '__main__':
    value = build()
    print(json.dumps(value, ensure_ascii=False, indent=2))
    raise SystemExit(bool(value['errors']))
