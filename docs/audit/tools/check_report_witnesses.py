#!/usr/bin/env python3
"""Audit-owned illustrations and BOUNDED literal-source observations for partial7B1.

Only Python stdlib, synthetic values and explicitly bounded text reads. No ERP,
C#/VisualBasic/DevExpress imports, SQL evaluator, application build, binary, COM,
printer, spreadsheet interpreter, browser, network, external service or writes.
A manually transcribed model is NOT an execution of the C#/VB implementation.
Passing these assertions verifies the documented example, NOT ERP acceptance.
"""
from __future__ import annotations
import csv
from decimal import Decimal as D, ROUND_HALF_UP
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[3]
C = 'SmartAuditERP/Class/'
F = 'SmartAuditERP/Form_WPF/'
ILLUSTRATIONS = []
LEXICAL = []
READS: list[dict] = []

def illustration(n, name, findings, evidence, model, limit):
    ILLUSTRATIONS.append(dict(id=f'ALG7B-{n:02d}', name=name, finding_ids=findings,
        evidence=evidence, synthetic_model=model, source_application_executed=False,
        illustration_assertions_passed=True, limit=limit))

def cut(path, start, end):
    lines = (ROOT/path).read_text(encoding='utf-8-sig').splitlines()
    assert 1 <= start <= end <= len(lines)
    ref = f'{path}:{start}-{end}'
    READS.append(dict(path=path,start=start,end=end))
    return '\n'.join(lines[start-1:end]), ref

def lexical(n, name, findings, evidence, observations, limit):
    assert observations and all(observations.values()), (n, observations)
    LEXICAL.append(dict(id=f'ST7B-{n:02d}',name=name,finding_ids=findings,evidence=evidence,
        observations=observations,source_application_executed=False,
        documented_text_observation_matches=True,limit=limit))

# Models below deliberately do not emulate a runtime/database/spreadsheet.
def copy_count(mode, count):
    if mode == 1 and count > 0:
        return count
    if mode == 2:
        return 0
    return 1
copies = {str(n):copy_count(1,n) for n in (-1,0,1,3)}
assert copies == {'-1':1,'0':1,'1':1,'3':3} and copy_count(2,0)==0
illustration(1,'فروع عدد النسخ عند مدخل المحرك','P7-030',C+'Print.cs:195-218',
    {'mode_1_count_to_model_requests':copies,'mode_2_zero_copies_model_print_requests':0},
    'نسخ يدوي لقرار if/else فقط؛ لا طابعة ولا فشل قالب أو callback، وحراس بعض المستدعين قد تمنع وصول الصفر.')

fraction = '1.999'.split('.')[1][:2]
assert fraction == '99' and D('1.999').quantize(D('.01'),rounding=ROUND_HALF_UP)==D('2.00')
illustration(2,'بتر الكسر مقابل تقريب مبلغ موحد','P7-034',C+'InvoiceOper.cs:550-577',
    {'synthetic_input_text':'1.999','literal_two_character_fraction':fraction,'two_digit_half_up_reference':'2.00'},
    'Python string/Decimal على نص مفترض عند حد split؛ لا VB Conversions أو صياغة لغوية كاملة. Print الرئيسي قد يقرب Net قبل الاستدعاء.')
comma_parts = '12,25'.split('.')
assert comma_parts == ['12,25']
illustration(3,'فاصل عشري مختلف لا ينتج جزء كسر عند split بالنقطة','P7-034',C+'InvoiceOper.cs:550-577',
    {'synthetic_decimal_comma_text':'12,25','parts_after_literal_dot_split':comma_parts,'fraction_branch_condition':len(comma_parts)>=2},
    'يثبت حد الفصل النصي في النموذج فقط، لا نتيجة parsing أو Floor أو ثقافة Windows فعلية ولا قائمة الثقافات المدعومة.')

ar_names = {12:'جنيه مصري',13:'جنيه سوداني'}
en_branches = {2:'Dollar',4:'Dirham',9:'Pound',10:'Euro',11:'Yen',8:'Riyal'}
assert en_branches.get(12,'Riyal')=='Riyal' and ar_names[12]=='جنيه مصري'
illustration(4,'اختلاف فروع أسماء الرمز نفسه','P7-035',C+'InvoiceOper.cs:972-1169',
    {'synthetic_numeric_code':12,'arabic_explicit_branch':ar_names[12],'english_fallback_branch':en_branches.get(12,'Riyal')},
    'كتالوج فرعي منقول يدوياً من الأرقام المحلية، لا استخراج enum أو عقد DLL أو مصادقة أسماء قانونية لكل العملات.')

units=[{'item':1,'barcode':'UNIT-A'}]
alternatives=[]
product_matches=[(u,b) for u in units for b in alternatives if
    (u['barcode']=='UNIT-A' and u['item']!=2) or (b['barcode']=='UNIT-A' and b['item']!=2)]
independent_exists=any(u['barcode']=='UNIT-A' and u['item']!=2 for u in units)
assert product_matches==[] and independent_exists
illustration(5,'حاصل ضرب بجدول فارغ يخفي باركود الجدول الآخر','P7-036',F+'frmMultiBarcode.xaml.cs:75-98',
    {'unit_rows':1,'alternative_rows':0,'cartesian_match_count':len(product_matches),'independent_unit_exists':independent_exists},
    'جبر مجموعات/قوائم مستقلة، لا SQL Server أو collation أو constraint؛ قيد نشر خارجي قد يمنع INSERT لاحقاً.')

base_price, unit_price = D('10'), D('100')
assert base_price != unit_price
illustration(6,'سعر تعريف الصنف لا يساوي سعر وحدة الرمز','P7-037',F+'frmPrintBarcode.xaml.cs:215-241'+';'+C+'Common.cs:560-578',
    {'synthetic_base_price':str(base_price),'synthetic_scanned_pack_price':str(unit_price),'model_label_from_base':str(base_price)},
    'عينة أسعار اصطناعية عند مدخل DTO؛ لا ماسح/ضريبة أو تطبيق فعلي. مسار الوحدة اليدوي يقرأ IU.sale وهو counterexample.')

gross, discount, cost = D('100'),D('10'),D('60')
legacy_net = gross - 2*discount
reference_net = gross-discount
assert legacy_net==D('80') and reference_net==D('90')
illustration(7,'خصم POS المضاعف عند خرج helper','P7-038',F+'frmRptItemsProfit.xaml.cs:183-231',
    {'helper_gross':'100','helper_discount':'10','header_share':'0','cost':'60','model_net':str(legacy_net),
     'model_profit':str(legacy_net-cost),'single_discount_net':str(reference_net),'single_discount_profit':str(reference_net-cost)},
    'مدخل عند مخرجات GetSaleData مفترض سليم، لا فحص صحة SQL/VAT/تكلفة تاريخية أو نجاح حفظ مستند.')
qty, unit_cost = D('10'),D('3')
assert qty*unit_cost==D('30')
illustration(8,'إجمالي لا متوسط وحدة','P7-039',F+'frmRptItemsProfit.xaml.cs:236-250'+';'+F+'frmRptItemsProfit.xaml:463-470',
    {'quantity':'10','unit_cost':'3','model_labeled_average_field':str(qty*unit_cost),'actual_fixture_unit_cost':str(unit_cost)},
    'معنى حقل المثال فقط؛ لا weighted-average inventory policy أو قالب REPX اختبر.')

sale_qty, ret_qty, sale_value, ret_value = D('0'),D('2'),D('0'),D('60')
model_included = sale_qty != 0
assert not model_included and sale_value-ret_value==D('-60')
illustration(9,'مرتجع فقط لا يمر شرط وجود البيع','P7-040',F+'frmRptSalesInPeriod.xaml.cs:119-150',
    {'sale_quantity':'0','return_quantity':'2','model_row_included':model_included,'signed_reference_quantity':str(sale_qty-ret_qty),'signed_reference_value':str(sale_value-ret_value)},
    'قرار نموذج مستقل؛ لا تنفيذ SELECT أو إرجاع أصلي أو مقارنة tot_net مع مبلغ قبل الضريبة بلا تسوية.')

entry_qty, equality, price = D('1'),D('12'),D('120')
base_qty=entry_qty*equality
assert base_qty*price==D('1440') and entry_qty*price==D('120')
illustration(10,'كمية الأساس مضروبة بسعر العبوة','P7-041',F+'frmRptSalesInPeriod.xaml.cs:169-176'+';'+C+'InvoiceOper.cs:1592-1599',
    {'val_base':str(base_qty),'val1_entry':str(entry_qty),'exchange_price_per_pack':str(price),'model_value':str(base_qty*price),'unit_consistent_value':str(entry_qty*price)},
    'عقد val/val1 من الكاتب المقروء ومثال أحادي السطر؛ لا يعني SUM(val1) جمعاً صحيحاً لوحدات مختلفة أو ربحاً معتمداً.')

fields={'items_total':'','invoice_total':'100.00'}
model_summary=fields['items_total']
assert model_summary=='' and model_summary != fields['invoice_total']
illustration(11,'المجموع بعد Clear من تبويب آخر','P7-042',F+'frmRptSalesInPeriod.xaml.cs:282-296'+';'+F+'frmRptSalesInPeriod.xaml.cs:325-355',
    {'post_clear_and_invoice_load_fields':fields,'model_SumSell':model_summary},
    'قواميس تمثل الإسناد فقط؛ لا WPF أو binding/layout أو جمع القالب الخارجي.')

exempt_base, header_rate = D('100'),D('.15')
model_exempt = exempt_base/(1+header_rate)
assert model_exempt.quantize(D('.0001'))==D('86.9565') and exempt_base-D('10')==D('90')
illustration(12,'قسمة جزء صفر ضريبة بمعدل رأس آخر وخصمه المهمل','P7-043',F+'frmTaxRptPeriod.xaml.cs:345-420',
    {'synthetic_zero_tax_line_gross':'100','header_rate':'0.15','model_inclusive_exempt_base_4dp':str(model_exempt.quantize(D('.0001'))),
     'reference_zero_rate_line_base':'100','all_exempt_header_discount':'10','model_NOTAX_after_header_discount':'100','discounted_reference_if_policy_applies':'90'},
    'عينتان منفصلتان منقولتان يدوياً، لا فئة ضريبية قانونية أو توزيع خصم متعدد المعدلات معتمد أو SQL/VB نفذ.')

components={'taxed_base':D('100'),'exempt_base':D('50'),'receipts_base':D('0'),'rent_base':D('0')}
model_total=components['taxed_base']+components['receipts_base']+components['rent_base']
assert model_total==D('100') and sum(components.values())==D('150')
illustration(13,'المكون المعفى خارج الإجمالي المسمى','P7-044',F+'frmTaxRptPeriod.xaml.cs:557-563'+';'+F+'frmTaxRptPeriod.xaml.cs:649-655',
    {'model_total':str(model_total),'sum_of_fixture_components':str(sum(components.values())),'reference_exempt_vat':'0'},
    'مثال جمع أساس فقط؛ لا إضافة VAT إلى أساس أو حكم بأن netVAT يتغير بالمعفى دائماً.')

old={'criteria':'A','sales':100,'purchases':40,'net_vat':9}
partial=dict(old)
partial['sales']=200
partial['criteria']='B'
assert partial['sales']==200 and partial['purchases']==40
illustration(14,'هوية معايير جديدة ونشر جزئي قبل فشل مصدر','P7-045;P7-046',F+'frmTaxRptPeriod.xaml.cs:492-524'+';'+F+'frmTaxRptPeriod.xaml.cs:650-675'+';'+F+'frmTaxRptPeriod.xaml.cs:700-749',
    {'old_fixture':old,'manually_modeled_after_sales_update_and_later_failure':partial},
    'انتقالات قاموس اصطناعي لا C#/dispatcher/SQL أو fault injection حقيقي؛ P7-045 تغيير معايير بعد عرض، و046 فشل داخل عرض، جذران متميزان.')

percentage, base, vat = D('5'),D('200'),D('30')
amount=base*percentage/100
assert amount==D('10') and amount != percentage
illustration(15,'نسبة في حقل مبلغ وأصفار غير مشتقة','P7-047',F+'frmRptInvPurchaseDetails.xaml.cs:869-878'+';'+C+'Report.cs:583-594',
    {'fixture_rate_percent':'5','fixture_base':'200','fixture_extra_amount':str(amount),'model_ExtraVAT_from_rate':str(percentage),'fixture_VAT':str(vat),'model_TotalTax_literal':'0','model_SummaryPaid_literal':'0'},
    'نموذج projection فقط لا أن كل الفواتير ذات5% أو أن ExtraVAT/الدفعات حُمّلت سليماً من المصدر؛ القيم غير المحملة ليست صفراً مثبتاً.')

synthetic_name='صنف "ألف", كبير'
naive_quoted='"'+synthetic_name+'"'
try:
    list(csv.reader(io.StringIO(naive_quoted),strict=True))
except csv.Error:
    malformed=True
else:
    malformed=False
unquoted_pos=list(csv.reader(io.StringIO('A,1,000.25,B')))[0]
tsv_rows='Id\tName\n1\tألف\nباء\n'.splitlines()
assert malformed and len(unquoted_pos)==4 and len(tsv_rows)==3
illustration(16,'بنية ملف محدد الفواصل من دون ترميز الخلايا','P7-048',F+'frmRptItemsProfit.xaml.cs:561-584'+';'+F+'frmRptInvSalesDetailsPos.xaml.cs:668-691'+';'+F+'frmRptInvPurchaseDetails.xaml.cs:912-937',
    {'naive_internal_quote_rejected_by_python_csv_strict':malformed,'synthetic_three_fields_with_unquoted_thousands_actual_fields':len(unquoted_pos),'tsv_embedded_newline_model_lines':len(tsv_rows)},
    'قارئ Python stdlib لنصوص مولدة بيد التدقيق فقط، لا إعادة تنفيذ writer C# ولا اختبار Excel/الأجهزة. CSV محاط صحيحاً يحفظ الفاصلة المجردة وهو counterexample.')
formula_text=list(csv.reader(io.StringIO('"=1+1"')))[0][0]
assert formula_text=='=1+1' and formula_text.startswith('=')
illustration(17,'اقتباس CSV لا يمحو بادئة الصيغة','P7-049',F+'frmRptItemsProfit.xaml.cs:561-591',
    {'benign_synthetic_text_only':formula_text,'prefix_survives_csv_decoding':formula_text.startswith('='),'spreadsheet_opened_or_evaluated':False},
    'لا eval أو قارئ جداول أو shell/شبكة؛ بقاء بادئة نصية ليس exploit أو إثبات أن قارئاً معيناً سيفعلها مع ProtectedView.')

synthetic_tsv='Id\tName\n1\tصنف\n'.encode('utf-8')
assert not zipfile.is_zipfile(io.BytesIO(synthetic_tsv))
illustration(18,'بايتات TSV ليست حزمة XLSX','P7-050',F+'frmRptInvPurchaseDetails.xaml.cs:882-937',
    {'synthetic_selected_extension':'.xlsx','model_writer_kind':'UTF8 tab-delimited text','synthetic_bytes_are_zip_container':False},
    'فحص محايد لعينة bytes اصطناعية لا ملف ERP مولداً أو رفض/تحذير Excel مرصوداً؛ لا يثبت أمن ZIP من مجرد صيغته.')

rent_base, rent_tax = D('100'), D('15')
rent_gross=rent_base+rent_tax
assert rent_gross==D('115') and rent_gross-rent_tax==rent_base
illustration(19,'إجمالي التأجير الشامل لا يساوي أساسه قبل الضريبة','P7-051',F+'frminvoice.xaml.cs:722-755'+';'+F+'frminvoice.xaml.cs:1624-1650'+';'+F+'frmTaxRptPeriod.xaml.cs:524-563',
    {'synthetic_net_rent_base':str(rent_base),'tax':str(rent_tax),'writer_tot_net_from_NetVal':str(rent_gross),'model_report_rent_base':str(rent_gross),'reported_tax_from_separate_column':str(rent_tax)},
    'كاتب/قارئ منقولان يدوياً لعينة بلا خصم/تأمين/إضافات؛ لا دورة حفظ أو SQL نفذت. خطأ الأساس لا يعني ضريبة مستحقة ثانية لأن التقرير يجمع tax المنفصلة.')

s,e=cut(C+'Print.cs',195,221)
lexical(1,'حدود فرع نسخ الطباعة','P7-030;P7-031',e,
    {'positive_count_guard_present':'type == 1 && PrintNo > 0' in s,'preview_guard_present':'else if (type == 2)' in s,'fallthrough_print_present':'else\n\t\t\t\t{\n\t\t\t\t\txtraReport.Print();' in s,'exception_handler_without_message_or_return':'catch (Exception projectError)' in s and 'MessageBox' not in s},
    'مطابقة نصية محدودة لا تنفيذ للقرار أو printer runtime.')
a,ea=cut(F+'frmSalesInvoice.xaml.cs',904,909)
b,eb=cut(F+'frmSalesInvoice.xaml.cs',1199,1227)
lexical(2,'caller معاينة وربط فيه أوامر سيريال','P7-029',ea+';'+eb,
    {'view_calls_builder_before_report':'BindToInvoice()' in a and 'RptPrint(inv, 2)' in a,'serial_delete_inside_builder':'DELETE FROM ItemSerialNo' in b,'serial_insert_helper_call':'SaveSerialNo(' in b},
    'شواهد حرفية موجبة داخل المقاطع، لا callgraph شامل أو تشغيل SQL/إثبات فشل نشر.')
s,e=cut(F+'frmRptItemsProfit.xaml.cs',183,231)
lexical(3,'خصم POS والمعادلة النهائية','P7-038',e,
    {'pos_double_discount':'r3.discount * 2' in s,'subtract_accumulated_discount':'salesTotal - salesDiscount - salesInvDisc' in s},
    'اسم helper وقيم SQL لا ينفذان؛ المثال المالي يعلن حد مدخله.')
a,ea=cut(C+'InvoiceOper.cs',1592,1599)
b,eb=cut(F+'frmRptSalesInPeriod.xaml.cs',163,176)
lexical(4,'معاملات الكاتب مقابل مبلغ التقرير','P7-041',ea+';'+eb,
    {'val_primary':'"@val", SqlDbType.Float).Value = invoiceItem.ItemPrimaryQnty' in a,
     'val1_entry':'"@val1", SqlDbType.Float).Value = invoiceItem.ItemQuantity' in a,
     'price_entry':'"@exchange_price", SqlDbType.Float).Value = invoiceItem.ItemPrice' in a,
     'query_uses_val_times_price':'SUM(val * exchange_price)' in b},
    'فحص أسماء/تعابير حرفية مع عقود محلية فقط لا تنفيذ command binding/SQL.')
s,e=cut(F+'frmTaxRptPeriod.xaml.cs',345,420)
lexical(5,'قسمة الرأس لا تحرس NOTAX وخصم الرأس يحرس TAXED','P7-043',e,
    {'notax_clause':'filterVatMode == "NOTAX"' in s,'header_rate_division':'totalBase /= 1.0 + vatPercent / 100.0' in s,'header_discount_taxed_only':'if (filterVatMode == "TAXED") baseNet -= minusBase' in s},
    'وجود تعابير محددة لا إثبات صحة كل فرع أو legal category أو query result.')
a,ea=cut(F+'frmTaxRptPeriod.xaml.cs',557,563)
b,eb=cut(F+'frmTaxRptPeriod.xaml.cs',649,655)
lexical(6,'مكونات إجماليي الأساس لا تسمي حقلي المعفى','P7-044',ea+';'+eb,
    {'sales_formula_components':'txtNetSale.Text' in a and 'txtReceipts.Text' in a and 'txtIncomes.Text' in a,
     'sales_exempt_not_in_this_expression':'txtSalesOutTax' not in a,
     'purchase_formula_components':'txtNetPurch.Text' in b and '+ expTotal' in b,
     'purchase_exempt_not_in_this_expression':'txtPurchOutTax' not in b},
    'الغياب داخل expression معلوم الحدود فقط، لا غياب وظيفة/فئة من كامل البرنامج.')
a,ea=cut(F+'frmRptInvPurchaseDetails.xaml.cs',869,878)
b,eb=cut(C+'Report.cs',583,594)
lexical(7,'إسقاط نسبة وأصفار للخرج','P7-047',ea+';'+eb,
    {'rate_in_row_position':'row.ExtraVATPerc.ToString(fmt)' in a,'three_zero_literals':'"0", "0", "0"' in a,
     'summary_extra_zero':'SummaryExtraTax = "0"' in b,'summary_paid_zero':'SummaryPaid = "0"' in b},
    'العقد الموضعـي يراجع مع الأعمدة المعلنة؛ لا إثبات قالب خارجي أو تحميل كامل لكل الفواتير.')
s,e=cut(F+'frmRptInvPurchaseDetails.xaml.cs',882,937)
lexical(8,'خيار XLSX يمر إلى writer نص Tab','P7-050',e,
    {'xlsx_filter_present':'Excel Files (*.xlsx)' in s,'same_tsv_call':'ExportDataTableToTsv(dt, dlg.FileName)' in s,'tab_delimiter':'sb.Append(\'\\t\')' in s,'utf8_file_write':'File.WriteAllText(filePath, sb.ToString(), Encoding.UTF8)' in s},
    'موجب نصياً في متصل/كاتب محدود لا تجربة قارئ Excel أو تحقق كامل OfficeOpenXML.')
a,ea=cut(C+'Print.cs',670,673)
b,eb=cut(C+'Print.cs',946,965)
lexical(9,'اختزال تفاصيل السيريال/الدفعة','P7-033',ea+';'+eb,
    {'loop_over_details':'foreach (InvoiceItemDetail' in a,'single_serial_assignment':'invoiceData.ItemSerialNo = invoiceItemDetail.ItemSerialNo' in a,
     'item_scoped_detail_query':'InvGlobalID=@InvGlobalID and ItemId=@ItemId' in b,'first_read_only_in_cut':'sqlDataReader2.Read();' in b},
    'لا شمول لكل query/DTO خارجي أو إثبات نتيجة ORDER بلا SQL؛ هذه تعابير موجبة محددة.')
s,e=cut(F+'frmItemsBarcode.xaml.cs',367,383)
assert '\u200f\u200fBarcode2.repx' in s
lexical(10,'عقد اسم قالب باركود بمقدمتَي RLM','P1-004',e,
    {'two_RLM_literal_before_Barcode2':'\u200f\u200fBarcode2.repx' in s,'file_exists_is_checked':'File.Exists(fullPath)' in s},
    'حروف U+200F موجودة في الاسم الحرفي؛ ليست دليلاً على فشل ملف نشر غائب عن المستودع ولا افتراض ASCII للاسم الصحيح.')

a,ea=cut(F+'frminvoice.xaml.cs',722,755)
b,eb=cut(F+'frminvoice.xaml.cs',1624,1650)
c,ec=cut(F+'frmTaxRptPeriod.xaml.cs',524,535)
lexical(11,'مصدر NetVal الشامل وكاتب tot_net وقارئه إلى الأساس','P7-051',ea+';'+eb+';'+ec,
    {'net_includes_tax':'Math.Round(rentVal + taxVal, 2)' in a,
     'gross_parameter_from_NetVal':'"@tot_net",         SqlDbType.Float).Value   = this.NetVal' in b,
     'rent_report_uses_tot_net':'SetCellText(txtIncomes,' in c and 'SafeDouble(dt.Rows[0]["tot_net"])' in c},
    'مطابقة نصية موجبة محدودة لا تنفيذ للكاتب أو إثبات عبور حواجز الحفظ أو صحة كل كاتب آخر لـRentInvoice.')

print(json.dumps({
    'phase':'7B1-partial-static-audit','audit_reference_date_utc':'2026-11-16',
    'method':'Manually transcribed synthetic illustrations plus separately labelled bounded literal-source checks; NOT application tests',
    'application_code_imported_or_executed':False,'erp_runtime_tests_executed':0,
    'sql_or_external_service_tests_executed':0,'application_remediation_performed':False,
    'real_business_or_secret_data_used':False,'spreadsheet_or_formula_interpreter_executed':False,
    'illustration_count':len(ILLUSTRATIONS),'static_lexical_contract_check_count':len(LEXICAL),
    'illustrations':ILLUSTRATIONS,'static_lexical_contract_checks':LEXICAL,
    'bounded_source_reads_not_semantic_coverage':READS,
    'limit':'All assertions are about audit-owned Python values or literal text slices. No C#/VB/SQL/WPF/DevExpress/REPX/driver/provider behavior was executed or certified.'
},ensure_ascii=False,indent=2))
