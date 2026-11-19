#!/usr/bin/env python3
"""20 independent manual illustrations +20 bounded lexical B16 observations.

Stdlib/inert source text ONLY; not a C#/SQL/WPF translator or interpreter.
No app import/build/runtime/REPX/Office/provider/device/printer/real business
export/shell/secrets/remediation/operational measurement or financial approval.
"""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
F, C = 'SmartAuditERP/Form_WPF/', 'SmartAuditERP/Class/'
D, DX = F+'frmTaxInvDetails.xaml.cs', F+'frmTaxInvDetails.xaml'
V, VX = F+'frmVATReturn.xaml.cs', F+'frmVATReturn.xaml'
PR, RP = C+'Print.cs', C+'Report.cs'
S, SX = F+'frmSettings.xaml.cs', F+'frmSettings.xaml'
CO, MC, RES = C+'Common.cs', C+'MainClass.cs', 'SmartAuditERP/Properties/Resources.resx'
LIMIT = ('مثال يدوي مستقل بأعداد وتواريخ ومفاتيح خيالية، لا ترجمة/تنفيذ C#/SQL/WPF أو قبول مالي أو قانون ضريبي. '
         'R1/R2/R3 محليات وبقايا مفتوحة؛3 أزواج body/own-XAML خارج حصر52 القديم، لا كلfeature/caller. '
         'القوالب وDLLالمحوّل ومخطط النشر وACL والسياسة غير مصادق عليها.7C لم تبدأ و8 غير مأذونة.')
TEXT_LIMIT = ('tokens/غياب نص في مقطع محدد فقط؛ لا semantic AST/callgraph/compile/overload resolution أوSQL/WPF/REPX rendering، '
              'ولا تفويض نشر أو عيب index/leak/latency مقاس أو قبول مالي.')


def ref(*triples):
    return ';'.join(f'{p}:{a}-{b}' for p, a, b in triples)


class Witness:
    def __init__(self):
        self.alg, self.lex, self.errors, self.reads = [], [], [], {}

    def require(self, ok, message):
        if not ok:
            self.errors.append(message)

    def text(self, path, start, end):
        lines = (ROOT/path).read_text(encoding='utf-8-sig').splitlines()
        self.require(1 <= start <= end <= len(lines), 'Bounded read: '+path)
        value = '\n'.join(lines[start-1:end])
        self.reads[(path, start, end)] = dict(path=path, start=start, end=end,
                                            selected_text_sha256=hashlib.sha256(value.encode()).hexdigest())
        return value

    def illustration(self, n, title, roots, evidence, ok, details):
        self.require(ok, 'ALG '+str(n))
        self.alg.append(dict(id=f'ALG7B16-{n:02d}', title=title, finding_ids=roots, evidence=evidence,
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
        self.require(ok, 'ST '+str(n))
        row = dict(id=f'ST7B16-{n:02d}', title=title, finding_ids=roots, evidence=ref(*dict.fromkeys(refs)),
                   documented_text_observation_matches=bool(ok), source_application_executed=False, limit=TEXT_LIMIT)
        if observation:
            row['additional_inert_text_observation'] = observation
        self.lex.append(row)


def build():
    w = Witness()
    a, l = w.illustration, w.lexical
    a(1, 'بلا ضريبة: بيع100 ومرتجع40 ليس صافي100', 'P7-127', ref((V,406,435),(V,529,554),(V,622,636),(V,815,845)),
      100-40 == 60 and 100 != 60 and 50-20 == 30,
      dict(invented_sales=100, invented_sales_return=40, reference_signed_component=60, manual_local_component=100,
           invented_purchases=50, invented_purchase_return=20, reference_purchase_component=30, manual_local_purchase_component=50,
           both_switches_one_reducer_root=True, not_SQL_or_DotNet_execution=True))
    a(2, 'مرتجع فقط: إغفال المكوّن ينتج0 لا-40', 'P7-127', ref((V,421,434),(V,542,553)),
      0-40 == -40 and -40 != 0,
      dict(invented_return_only=40, manual_local_component=0, reference_signed_component=-40,
           sales_and_purchase_same_omission=True, no_unobserved_business_loss_asserted=True))
    a(3, 'بيع فقط وVAT0 شاهدان لا يثبتان تغيير المستحق', 'P7-127', ref((V,423,433),(V,544,552),(V,637,644)),
      100-0 == 100 and Decimal('0')-Decimal('0') == 0,
      dict(reference_sale_only=100, manual_local_sale_only=100, no_tax_component_VAT=0,
           omitted_disclosed_base_need_not_change_payable_VAT=True, legal_category_not_inferred_from_taxval_zero=True,
           labels_taxable_not_generic_total_are_not_automatically_root044=True))
    a(4, 'علم رأس شامل لا يجعل بند0tax ذا معدل الرأس', 'P7-043', ref((V,344,392),(V,471,518)),
      Decimal('100')/Decimal('1.15') != Decimal('100'),
      dict(invented_zero_tax_line_base='100', invented_header_rate='15', manual_header_division=str(Decimal('100')/Decimal('1.15')),
           reference_if_line_zero_rate='100', discount_allocation_policy_external=True,
           purchase_non_taxable_branch_does_not_divide_is_counterexample=True, prior_writer_barriers_not_assumed_fixed=True))
    a(5, 'XML ليس حزمةXLSX؛ لا تفسير صيغة', 'P7-050', ref((D,894,925)),
      b'<TaxInvoices>' != b'PK\x03\x04',
      dict(inert_symbolic_XML_prefix='<TaxInvoices>', inert_symbolic_zip_prefix='PK',
           manual_declared_extension='xlsx', actual_writer_kind_from_text='DataTable.WriteXml',
           no_actual_business_file_or_spreadsheet_created_or_opened=True,
           not_extending_CSV_escaping048_formula049_or_open_writer108=True))
    end = datetime(2026,1,31,23,59,59)
    last_fraction = end+timedelta(microseconds=999000)
    tomorrow_noon = datetime(2026,2,1,12)
    a(6, 'نهاية رئيسية23:59:59 وPOS+24 ليستنافذةواحدة', 'P3-023', ref((V,314,322),(D,234,275),(D,451,457)),
      not last_fraction < end and tomorrow_noon < end+timedelta(hours=24) and not tomorrow_noon < datetime(2026,2,1),
      dict(manual_main_exclusive_end='2026-01-31T23:59:59', reference_next_midnight='2026-02-01T00:00:00',
           main_loses_last_fraction=True, POS_add24_includes_next_day_noon=True,
           date_parameter_culture_calendar_not_runtime_certified=True))
    a(7, 'اختيارB مع سنداتA يمزج BranchSet', 'P7-125', ref((D,238,242),(D,521,530),(D,572,580),(V,564,577)),
      200+10 == 210 and 200+30 == 230 and 210 != 230,
      dict(invented_session='A', invented_selected='B', invoices_B=200, receipts_A=10, receipts_B=30,
           manual_local_mixed=210, reference_B=230, VAT_parent_receipt9_uses_selected_branch_counterexample=True,
           not_deployed_ACL_or_visibility_proof=True))
    a(8, 'كل الفروع بعدB لا يساوي B فقط', 'P7-088', ref((D,238,242),(D,752,755),(DX,265,275)),
      {'B'} != {'A','B'},
      dict(manual_selected_before_all='B', selected_index_stays_nonnegative=True, local_invoice_branch_set=['B'],
           required_declared_allowed_all_set=['A','B'], first_open_selected_minus1_can_work=True,
           allowed_set_cannot_be_derived_from_UI_alone=True))
    a(9, 'all-period للمصدرين لا يعني فواتيرقديمة فقط', 'P7-112', ref((D,238,239),(D,292,304),(D,521,530),(D,572,580)),
      100+200+30 == 330 and 100+200+10+30 == 340,
      dict(invented_old_invoice=100, invented_current_invoice=200, invented_old_receipt=10, invented_current_receipt=30,
           manual_mixed_period_total=330, reference_all_period_total=340,
           separate_from_last_fraction_boundary023=True))
    a(10, 'فهرس rent-return5 لا يحقق>5', 'P7-099', ref((D,104,119),(D,763,777)),
      not (5>5) and 6>5,
      dict(manual_rent_index=4, manual_rent_return_index=5, handler_return_condition='index > 5',
           illustrative_previous_proc=1, Inv_Type_reassigned_to_Invtype_before_unmatched_branch=True,
           Marine_visible_required_not_observed=True, type_options_exist_not_root120=True,
           not_executing_event_or_proving_all_type4_reachability=True))
    a(11, 'canonical id لا يستنتج من وجود id وBranchId', 'P2-010;H7B16-04', ref((V,119,153),(D,128,151),(RES,242,276)),
      7 != 107,
      dict(invented_Branches_id=7, invented_BranchId=107, columns_both_supplied=True,
           difference_only_possibility_not_observed_mapping_defect=True,
           alias_Id_not_missing_column_proof=True, request_id_contract_and_grants_external=True))
    a(12, 'اختلاف SourceSet قد يكون subset لا خطأمجموع', 'H7B16-01;H7B16-03', ref((V,348,392),(V,564,615),(V,676,715),(D,220,304)),
      {2,3,20} < {2,3,20,21,22},
      dict(manual_child_invoice_types=[2,3,20], manual_VAT_invoice_types=[2,3,20,21,22],
           Entry_type10_not_same_as_Receipts_type10=True, child_receipt10_not_automatically_parent_tax_source=True,
           difference_requires_declared_metric_eligibility_not_forced_equality=True))
    a(13, 'جمع جزئي ليس نجاحاً كاملاً ولا صفراًصحيحاً', 'P7-046', ref((D,208,215),(D,280,310),(D,723,735),(V,619,658)),
      100 != 100+200 and 'parse-failed' != 'valid-zero',
      dict(invented_first_row_amount=100, invented_late_row_amount=200, local_partial_if_late_failure=100,
           reference_complete=300, required_health='failed-or-explicit-partial',
           VAT_uses_local_numeric_accumulators_until_publication_counterexample=True, no_SQL_fault_injection=True))
    a(14, 'معاييرB فوق نتيجةA ليست لقطةB', 'P7-045', ref((D,948,984),(V,287,295),(V,676,715),(V,815,846)),
      ('period-A',100) != ('period-B',100),
      dict(invented_computed_period='A', edited_live_period='B', stale_amount=100,
           DTO_live_metadata='B', hasLoadedData_write_not_request_fingerprint=True,
           child_branch_not_forwarded_by_named_callers=True, no_WPF_event_execution=True))
    a(15, 'ReceiptNo ليس DocumentRef؛ فواتيرGlobalIDشاهد', 'P7-061', ref((D,543,563),(D,785,868),(F+'frmSandVAT.xaml.cs',528,622),(RES,1496,1532)),
      ('A',9,5,'synthetic-GA') != ('B',9,5,'synthetic-GB'),
      dict(invented_same_local_receipt_no=5, branch_A='synthetic-GA', branch_B='synthetic-GB',
           local_child_expense_global_id='', source_DDL_primary_key='GlobalID',
           receiver_executes_supplied_SQL_then_first_Read=True, invoice_1_2_3_GlobalID_is_carried_counterexample=True,
           duplicate_deployed_rows_or_wrong_open_not_observed=True))
    a(16, 'إعداد حالي غير شامل لا يعيد تفسير شامل115', 'P7-095', ref((D,246,251),(D,280,280),(D,381,400),(D,463,491),(C+'InvoiceObj.cs',113,184),(C+'InvoiceOper.cs',1559,1573)),
      115-15 == 100 and 115 != 100,
      dict(invented_issued_inclusive=True, invented_current_setting_inclusive=False, invented_stored_sum=115,
           invented_VAT=15, manual_current_setting_base=115, reference_if_stored_inclusive=100,
           child_query_does_not_select_stored_PriceIncVAT=True, VAT_parent_does_use_stored_flag=True,
           not_legal_policy_or_repaired_writer_assumption=True))
    a(17, 'DTO string لا يثبت نوعاًمالياًأوقالباً', 'H7B16-02', ref((C+'InventoryData.cs',1,303),(C+'resvdPrint.cs',1,32),(C+'RptTaxData.cs',1,46),(RP,533,611)),
      isinstance('100.00',str) and not isinstance('100.00',Decimal),
      dict(inert_display_amount='100.00', currency_not_carried_by_this_string=True,
           empty_string_not_complete_schema_or_health=True, local_DTOs_exist=True,
           external_ToDataTable_implementation_and_REPX_not_executed=True))
    a(18, 'Print0 وReport0 لهما فرعان مختلفان', 'P7-030;H7B16-02', ref((PR,195,218),(RP,503,529),(D,1038,1049)),
      1 != 0,
      dict(manual_Print_type1_count0_fallthrough_calls=1, manual_Report_count0_loop_calls=0,
           manual_child_count0_loop_calls=0, preview_type2_not_same_as_print=True,
           no_printer_spool_or_output_acceptance=True, policy_and_cancel_contract_unresolved=True))
    a(19, 'إعداد0 و6 و12/14 ليست أولوية موحّدةمثبتة', 'H7B16-02;H7B16-03', ref((S,2087,2205),(S,2898,2960),(CO,901,942),(D,160,195),(D,989,1059),(F+'frmTaxRptPeriod.xaml.cs',180,211)),
      len({0,6,12,14}) == 4,
      dict(inert_default_row=0, settings_report_choice_row=6, selected_child_reader_row=12, old_parent_reader_row=14,
           active_path_overwrites_some_loaded_settings_from_MainClass=True, no_deployed_setting_rows_assumed=True,
           picker_empty_close_retains_default_not_new_cancel_bug=True, no_unrequested_policy_choice=True))
    a(20, '30 مساراً و14 disposition ليست إنهاء7B', 'H7B16-06', 'none-inventory-only',
      26+4 == 30 and 395+4 == 399 and 827-399 == 428 and 33+19 == 52 and 12+2 == 14,
      dict(scope_paths=30, overlap=26, new_paths=4, union=399, inventory_only=428,
           original_hashes=827, protected_artifacts=440, historical_core_rows=298,
           frozen_screen_candidates=52, supplemental_full_local_pairs_outside52=3, newly_full_CSharp=2, prior_full_picker=1,
           upstream_H_Q_dispositions=12, explicit_further_splits=2, B_planning_groups=4, C_axes_not_started=6,
           not_sessions_or_completion_percent=True, no_external_approval_or_phase8_authorization=True))

    l(1, 'المبيعات تعيدproc2 وNonTaxable وتضيفcase1', 'P7-127', [
        (V,348,395,('inv.proc_type IN (1, 2)', 'SUM(NonTaxableBase) AS TotalNonTaxable', 'GROUP BY proc_type')),
        (V,406,428,('double salesBase', 'row["TotalNonTaxable"]', 'salesNotTax += nonTaxable;'))])
    l(2, 'case2 للمبيعات يطرح3 مقاييس دونبلاالضريبة', 'P7-127', [
        (V,429,434,('case 2:', 'salesBase -= netBase;', 'salesVAT -= vatAmt;', 'extraVAT -= extraVatAmt;', 'break;'))],
      absent=[(V,429,434,('salesNotTax',))])
    l(3, 'المشتريات تعيدالمكونفيqueryوتسقطهفيcase2', 'P7-127', [
        (V,471,518,('inv.proc_type IN (1, 2)', 'SUM(NonTaxableBase) AS TotalNonTaxable')),
        (V,529,548,('row["TotalNonTaxable"]', 'purchNotTax += nonTaxable;')),
        (V,549,553,('purchBase -= netBase;', 'purchVAT -= vatAmt;', 'break;'))],
      absent=[(V,549,553,('purchNotTax',))])
    l(4, 'نشرالصفينثمA5/B5/C5 وlabelsالخاضعشاهدتفريق', 'P7-127', [
        (V,622,636,('lblsalesnotax.Text = salesNotTax.ToString', 'lblpurchnotax.Text = purchNotTax.ToString')),
        (V,815,845,('A5 = lblsalesnotax.Text', 'B5 = lblsalesnotax.Text', 'C5 = lblpurchnotax.Text')),
        (VX,476,520,('صافي المبيعات الخاضعة للضريبة:', 'المبيعات المعفاة من الضريبة:')),
        (VX,626,666,('المشتريات المعفاة من الضريبة:',))])
    l(5, 'xlsxمعWriteXml ثمفتحبعدعودةالكاتب', 'P7-050', [
        (D,894,925,('Filter      = "Excel Files|*.xlsx"', 'table.WriteXml(saveDialog.FileName);', 'Process.Start(new ProcessStartInfo(saveDialog.FileName)')),
        (DX,580,585,('تصدير Excel', 'Click="btnExportExcel_Click"'))])
    l(6, 'طفلالتاريخيستعملإعدادنوعحاليلاعَلمالرأس', 'P7-095', [
        (D,246,251,('VATPercent,InvCost',)), (D,280,280,('new InvoiceObj(Invtype, 1)',)),
        (D,381,400,('if (invoiceObj.PriceIncVAT)', 'InvVAT = ToDouble(mainTable.Rows[i]["tax"])')),
        (C+'InvoiceObj.cs',113,184,('select * from SettingGeneral where Inv_Id=', 'this.PriceIncVAT = Conversions.ToBoolean')),
        (C+'InvoiceOper.cs',1559,1573,('@PriceIncVAT', '@VATPercent'))],
      absent=[(D,246,251,('PriceIncVAT',))])
    l(7, 'فرعجلسةللسندوقيمةاختيارللفواتيرمعallلايمحوها', 'P7-125;P7-088', [
        (D,238,242,('cmbBranches.SelectedIndex > -1', 'inv.branch={cmbBranches.SelectedValue}')),
        (D,521,530,('ReceiptType=9', 'MainClass.BranchNo')),
        (D,572,580,('ReceiptType=10', 'MainClass.BranchNo')),
        (D,752,755,('cmbBranches.IsEnabled = chkAllBranches.IsChecked != true;',)),
        (V,564,577,('BranchID = {branchId}',))],
      absent=[(D,752,755,('SelectedIndex = -1',))])
    l(8, 'كلالفترةيحذفdateFilterلكنreceiptmethodsمؤرخةدائماً', 'P7-112;P3-023', [
        (D,238,239,('ckTotalPeriod.IsChecked != true', 'date<@date2')),
        (D,246,275,('23:59:59', 'toDate.AddHours(24)')),
        (D,521,530,('ReceiptDate>=@date1 AND ReceiptDate<@date2',)),
        (D,572,580,('ReceiptDate>=@date1', 'ReceiptDate<@date2')),
        (V,314,322,('23, 59, 59',))],
      absent=[(D,521,530,('ckTotalPeriod',)), (D,572,580,('ckTotalPeriod',))])
    l(9, 'قائمةrentreturnموجودةوفهرسها5وشرطhandler>5', 'P7-099', [
        (D,104,119,('مرتجع تأجير', 'Rent Return', 'Home.StripMarine.Visibility')),
        (D,763,777,('Inv_Type = Invtype;', 'idx == 4', 'idx >  5'))],
      absent=[(D,763,777,('idx == 5',))])
    l(10, 'سندمصروفيفقدGlobalIDويستعملReceiptNoومستقبلهReadمرة', 'P7-061', [
        (D,543,563,('DgvInvType     = "مصروفات"', 'DgvInvGlobalID = ""')),
        (D,785,807,('row.DgvInvType == "مصروفات"', 'ReceiptNo={row.DgvInvNo}')),
        (F+'frmSandVAT.xaml.cs',528,555,('new SqlCommand(sqlQuery, conn).ExecuteReader()', 'reader.Read();', 'reader["GlobalID"]')),
        (RES,1496,1532,('GlobalID', 'PRIMARY KEY', 'BranchID'))],
      absent=[(D,791,798,('BranchID', 'GlobalID'))])
    l(11, 'فاتورة1/2/3تحملGlobalIDفلايعُمّمفقدReceiptNo', 'P7-061;H7B16-03', [
        (D,429,438,('DgvInvGlobalID = mainTable.Rows[i]["InvGlobalID"].ToString()',)),
        (D,805,868,('inv_type=1 AND InvGlobalID', 'inv_type=2 AND InvGlobalID', 'inv_type=3 AND InvGlobalID')),
        (F+'frmInvPurch.xaml.cs',481,503,('InvoiceOper.BindingInvoice',)),
        (F+'frmInvSale.xaml.cs',1643,1660,('InvoiceOper.BindingInvoice',)),
        (F+'frmInvPOS.xaml.cs',1861,1880,('InvoiceOper.BindingInvoice',))])
    l(12, 'SourceSetالأب/الطفليختلفونفعلاًولاطلبBranchمشترك', 'H7B16-01;H7B16-03;P7-045', [
        (V,348,395,('inv.inv_type IN (2, 3, 20, 21, 22)',)),
        (V,676,715,('form.Invtype = 1;', 'form.Invtype = 2;', 'form.ShowInvs();')),
        (D,220,232,('inv_type=3', 'inv_type=20')),
        (D,128,151,('cmbBranches.SelectedIndex     = -1;',))],
      absent=[(V,676,715,('cmbBranch', 'hasLoadedData'))])
    l(13, 'معاييرحيةفيDTOوhasLoadedDataغيرمحروسفيprint', 'P7-045', [
        (V,287,295,('cmbBranch.IsEnabled',)),
        (V,815,846,('FromDate   = dtFrom.DateTime', 'A1 = lblSalesTaxableValue.Text')),
        (D,948,984,('FromDate       = txtDateFrom.DateTime', 'foreach (var row in invoiceRows)'))],
      absent=[(V,734,813,('hasLoadedData',)),(V,676,715,('hasLoadedData',))])
    l(14, 'childClear/perrowcatch/parse0؛VATpublishesبعدالحساب', 'P7-046;P3-007', [
        (D,208,215,('invoiceRows.Clear();', 'ResetSummaries();')),
        (D,282,304,('ProcessInvoiceRow(mainTable, i, invoiceObj);', 'catch { }')),
        (D,723,735,('return 0;', 'double.TryParse', 'int.TryParse')),
        (V,619,658,('lblSalesTaxableValue.Text', 'lblPurchTaxableValue.Text', 'hasLoadedData = true;'))])
    dto_counts = {name:len(re.findall(r'public string\s+\w+\s*\{\s*get;', w.text(C+name,1,end)))
                  for name,end in [('InventoryData.cs',303),('resvdPrint.cs',32),('RptTaxData.cs',46)]}
    l(15, 'DTOsمحليةstring-default؛26/35خاصيةعدنصي', 'H7B16-02', [
        (C+'InventoryData.cs',1,303,('class InventoryData', 'public string', 'string.Empty')),
        (C+'resvdPrint.cs',1,32,('class resvdPrint',)),(C+'RptTaxData.cs',1,46,('class RptTaxData',))],
      observation=dict(matches=dto_counts['resvdPrint.cs']==26 and dto_counts['RptTaxData.cs']==35,
                       string_property_counts_by_inert_regex=dto_counts, not_template_compatibility_or_semantic_coverage=True))
    l(16, 'Reportoverloadsوemptycatchقائم؛nullbridge055لميعالج', 'P7-055;H7B16-02', [
        (RP,380,461,('BindToData(GridView GridView1, string rptType, string FromDate, string ToDate)', 'result = new DataSet();')),
        (RP,533,611,('DataTable dt,', 'string sumTotal = "0"', 'foreach (DataRow row in dt.Rows)', 'return new DataSet();')),
        (F+'frmRptInventory.xaml.cs',728,750,('null, // GridView2 غير مستخدم في WPF',))])
    l(17, 'Printflagsوpicker/cancel/kitchenبلامتطلبنجاحخارجي', 'P7-030;P7-031;H7B16-02', [
        (PR,54,146,('SettingPrint where Inv_Id=', 'PrinterSettings where Inv_Id=', 'this.PrintHeader', 'this.PrintNo')),
        (PR,148,221,('frmPrinter2.ShowDialog();', 'frmPrinter2.SelectedPrinter', 'if (this.PrintHeader)', 'if (this.PrintFooter)', 'type == 1 && PrintNo > 0', '"rptPOS2.repx"')),
        (F+'frmPrinter.xaml.cs',90,108,('SelectedRptName = printer.RptName;', 'SelectedPrinter = printer.Printer;', 'this.Close();')),
        (F+'frmPrinter.xaml',1,14,('Loaded="Window_Loaded"',))])
    l(18, 'مخرجاتR1/R2ثلاثةDTOومساراتdirect/sharedبحدودها', 'H7B16-02', [
        (F+'frmRptItemsActivity.xaml.cs',563,580,('rptItemsTotalGrd.repx', 'MainClass.ReportsPrinter')),
        (F+'frmRptItemsActivityDetailed.xaml.cs',617,656,('new InventoryData', 'global::UtilitiesProj.Common.ToDataTable')),
        (F+'frmRptItemsExpiration.xaml.cs',265,320,('new InventoryData', 'RptItemsExpiration.repx', 'new Report().Printing')),
        (F+'FrmReseved.xaml.cs',547,585,('RptResevedSalary.repx', '_print.Printing')),
        (F+'frmTaxRptPeriod.xaml.cs',700,817,('new RptTaxData', 'TaxRptPeriod.repx')),
        (D,989,1059,('rptTaxInvDetailsPurchase.repx', 'rptTaxInvDetailsSales.repx', 'header.repx', 'footer.repx')),
        (V,734,813,('TaxRptPeriodNew.repx',))])
    l(19, 'settingsموصولةبرمجياًوتكتب6مقابلdefaults0/readers12', 'H7B16-02', [
        (S,97,159,('RegisterEvents();', 'btnprintsettings.Click += btnprintsettings_Click', 'ckReports.Checked += ckReports_CheckedChanged')),
        (S,2087,2205,('if (IsChecked(ckReports)) selectedInvId = 6;', 'MainClass.ReportsPath = Path.GetDirectoryName(reportPath)', 'MainClass.ReportsPrinter = cashierPrinterName')),
        (S,2898,2960,('LoadprintSetting(0);', 'LoadprintSetting(6);')),
        (CO,901,942,('SettingPrint where Inv_Id=0', 'GetDefaultPrinter()')),
        (D,160,195,('SettingPrint WHERE Inv_Id=12',))])
    l(20, 'HomeالفعليةوApplyوالأسماءليستACLأومخططنشر', 'P1-013;P2-001;P2-010;H7B16-04', [
        ('SmartAuditERP/Home.xaml.cs',2706,2713,('new frmVATReturn()', 'MainClass.ApplyPermissionToForm', 'frm.Show();')),
        ('SmartAuditERP/Home.xaml',345,345,('IsEnabled="False"',)),
        (MC,349,455,('if (dt.Rows.Count == 0) return;', 'name == "btnPrint"', 'VisualTreeHelper.GetChildrenCount')),
        (VX,339,375,('x:Name="BtnPrint"', 'x:Name="Button3"')),
        (RES,242,276,('[id]', 'BranchId', 'Code'))])
    return dict(
        phase='7B16-partial-static-audit', application_code_imported_or_executed=False,
        application_remediation_performed=False, real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False, erp_runtime_tests_executed=0,
        sql_or_external_service_tests_executed=0, illustration_count=len(w.alg), static_lexical_contract_check_count=len(w.lex),
        child_and_actual_VAT_caller_full_local_not_whole_features=True, picker_csharp_already_full_B1=True,
        frozen52_denominator_not_silently_expanded=True, B_R1_R2_R3_residual_contracts_not_closed=True,
        supplied_sql_not_certified_deployed=True, manual_metric_models_not_financial_acceptance=True,
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False),
        illustrations=w.alg, static_lexical_contract_checks=w.lex,
        bounded_source_reads_not_semantic_coverage=[w.reads[k] for k in sorted(w.reads)], errors=w.errors,
        limit=LIMIT+' '+TEXT_LIMIT)


if __name__ == '__main__':
    print(json.dumps(build(), ensure_ascii=False, indent=2))
