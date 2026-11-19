#!/usr/bin/env python3
"""B14:24 manual illustrations +24 bounded lexical observations, NOT ERP tests.

Only Python stdlib and inert source reads. No application import/build/C#/SQL/
WPF/REPX/Office/COM/formula/HTML interpreter/business export/consumer launch,
printer, real data/secrets, remediation or operational measurement. Sketches
are independent invented examples, not a translation/interpreter of the source.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/'; C='SmartAuditERP/Class/'; CW='SmartAuditERP/Class_WPF/'
I=F+'frmRptInventory.xaml.cs'; IX=F+'frmRptInventory.xaml'
S=F+'frmRptItemsActivity.xaml.cs'; SX=F+'frmRptItemsActivity.xaml'
D=F+'frmRptItemsActivityDetailed.xaml.cs'; DX=F+'frmRptItemsActivityDetailed.xaml'
E=F+'frmRptItemsExpiration.xaml.cs'; EX=F+'frmRptItemsExpiration.xaml'
IV=C+'Inventory.cs'; RP=C+'Report.cs'; MC=C+'MainClass.cs'; IO=C+'InvoiceOper.cs'; ID=C+'InventoryData.cs'
R='SmartAuditERP/Properties/Resources.resx'; H='SmartAuditERP/Home.xaml.cs'; HX='SmartAuditERP/Home.xaml'
P=F+'frmInvPurch.xaml.cs'; W=F+'frmProductionOrder.xaml.cs'
LIMIT=('مثال يدوي مستقل ببيانات خيالية ونصوص خاملة، لا ترجمة أو تشغيل C#/SQL/WPF/REPX/Office، '
       'ولا قبول ERP أو مال أو ACL. لا ملفات أعمال أو shell أو مفسر HTML/صيغة أو طباعة أو معالجة أو قياس. '
       'المصدر المرفق ليس مخطط النشر؛ كل body محلي لا يعني كل caller/child/template/schema/ACL. '
       'B-R1 تبقي عقوداً محالة، و4 حزم B و6 محاور C ليست جلسات مضمونة أو نسبة اكتمال؛8 غير مأذونة.')
TEXT_LIMIT=('وجود/غياب tokens في النطاقات المحددة فقط؛ لا AST دلالي أو overload resolution أو compile '
            'أو callgraph كامل أو SQL/WPF/rendering أو صحة مالية/تفويض نشر/تسرب/فهرس/زمن مقاس.')


def ref(*ranges):return ';'.join(f'{p}:{a}-{b}' for p,a,b in ranges)


class Witness:
    def __init__(self):self.errors=[];self.alg=[];self.lex=[];self.reads={}
    def require(self,ok,message):
        if not ok:self.errors.append(message)
    def text(self,p,a,b):
        lines=(ROOT/p).read_text(encoding='utf-8-sig').splitlines()
        self.require(1<=a<=b<=len(lines),'Bounded range: '+p)
        value='\n'.join(lines[a-1:b])
        self.reads[(p,a,b)]=dict(path=p,start=a,end=b,selected_text_sha256=hashlib.sha256(value.encode()).hexdigest())
        return value
    def illustration(self,n,title,roots,evidence,passed,details):
        self.require(passed,'ALG '+str(n))
        self.alg.append(dict(id=f'ALG7B14-{n:02d}',title=title,finding_ids=roots,evidence=evidence,
            illustration_assertions_passed=bool(passed),details=details,source_application_executed=False,limit=LIMIT))
    def lexical(self,n,title,roots,checks,absent=()):
        ok=True;refs=[]
        for p,a,b,tokens in checks:
            text=self.text(p,a,b);refs.append((p,a,b))
            for token in tokens:ok=bool(token in text) and ok
        for p,a,b,tokens in absent:
            text=self.text(p,a,b);refs.append((p,a,b))
            for token in tokens:ok=bool(token not in text) and ok
        self.require(ok,'ST '+str(n))
        self.lex.append(dict(id=f'ST7B14-{n:02d}',title=title,finding_ids=roots,evidence=ref(*dict.fromkeys(refs)),
            documented_text_observation_matches=ok,source_application_executed=False,limit=TEXT_LIMIT))


def build():
    w=Witness();a=w.illustration;l=w.lexical
    # Hand-selected illustrations, not C# or SQL evaluation.
    options=[];selected=-1;all_types=False
    local_condition_added=(not all_types and selected!=-1)
    a(1,'قائمة خيارات خالية لا تصل إلى switch ذي13 حالة','P7-120',ref((D,55,94),(D,280,287),(D,416,464),(DX,424,433)),
      not options and not local_condition_added and selected==-1,
      dict(options=options,selected=selected,local_condition_added=local_condition_added,reference_health='invalid-selection-not-all',switch_cases_do_not_supply_options=True))
    default_width,saved_width=90,170
    a(2,'كتابة مظهر دون قراءة لا تعيد المظهر في نافذة جديدة','P7-121',ref((D,70,94),(D,938,1004),(DX,801,805)),
      default_width!=saved_width,
      dict(default_width=default_width,saved_width=saved_width,new_window_without_read=default_width,reset_deletes_only=True,xml_is_inert_no_file_written=True))
    events=[dict(store=3,day=1),dict(store=2,day=2),dict(store=1,day=3)]
    requested_store=2;scoped=[r for r in events if r['store']==requested_store]
    a(3,'قيد المخزن الموجب مفقود قبل TOP سواء صعد الترتيب أم هبط','P7-122',ref((D,209,235),(D,253,260),(DX,288,296),(P,1139,1167)),
      events[0]['store']!=2 and events[-1]['store']!=2 and scoped==[events[1]],
      dict(requested_store=2,all_flag_default=True,selected_value_assigned=2,local_predicate_added=False,local_oldest=events[0],local_newest_if_sort_only_fixed=events[-1],reference_store_row=scoped[0],not_observed_query=True))
    base_qty,invoice_qty,equality,price=map(Decimal,('24','2','12','120'))
    local_avg=base_qty*price/base_qty;reference_avg=invoice_qty*price/base_qty
    a(4,'كمية الأساس وسعر العبوة يضخمان متوسط وقيمة المخزون','P7-041',ref((S,364,428),(IO,2073,2076),(D,292,296)),
      local_avg==120 and reference_avg==10 and base_qty*local_avg==2880 and invoice_qty*price==240,
      dict(base_quantity=str(base_qty),invoice_quantity=str(invoice_qty),equality=str(equality),unit_price=str(price),local_avg=str(local_avg),reference_base_avg=str(reference_avg),local_total='2880',reference_total='240',assumptions='one incoming line,no discounts,otherwise-correct eligibility and quantities'))
    a(5,'التسوية7 والمناقلة8 تتبادلان أسماء أعمدة التجميعي','P7-056',ref((S,232,294),(SX,649,700),(R,3054,3064)),
      dict(transfer=5,adjust=9)!=dict(transfer=9,adjust=5),
      dict(local_named_columns=dict(transfer=5,adjust=9),reference_named_columns=dict(transfer=9,adjust=5),grand_sum_can_still_match=True,supplied_seed_not_deployed=True))
    a(6,'وجود إنتاج فقط لا يمر من hasMovement الذي لا يقرأ6','P7-057',ref((S,232,268),(W,1425,1494)),
      not any([0]*13) and 10-3==7,
      dict(local_thirteen_read_sums=[0]*13,production_in=10,production_out=3,local_has_movement=False,reference_stock_movement=7,production_save_P4_020_not_assumed_fixed=True))
    customers=[dict(customer=7,qty=2),dict(customer=8,qty=5)]
    a(7,'حارس العميل الفارغ لا يغيّر query حتى مع ID صالح','P7-058',ref((S,199,205),(S,312,347),(S,904,943),(SX,413,446)),
      sum(x['qty'] for x in customers)==7 and sum(x['qty'] for x in customers if x['customer']==7)==2,
      dict(local_all=7,reference_customer7=2,LoadClients_does_create_id_source=True,Items_ItemsSource_gate_assumed_past_only_for_sketch=True))
    a(8,'أقدم وآخر ليسا TOP واحداً عند الترتيب نفسه','P7-059',ref((D,261,266),(D,289,304)),
      sorted([3,1,2])[0]==1 and sorted([3,1,2],reverse=True)[0]==3,
      dict(local_date_rank=1,reference_latest_rank=3,equal_timestamp_needs_stable_identity=True,store_predicate_is_separate_root=True))
    a(9,'الرأس1 لا يحدد اتجاه مكون line2','P7-060',ref((D,319,356),(W,1425,1494)),
      10+3==13 and 10-3==7,
      dict(header_direction=1,product_line_direction=1,component_line_direction=2,local_net_using_header=13,reference_net_using_line=7,save_gate_preserved=True))
    refs=[('global-A',1,5),('global-B',2,5)]
    a(10,'رقم محلي ونص لغة لا يحلان محل DocumentRef','P7-061',ref((D,359,387),(D,1011,1172),(CW+'ItemActivityRow_ActivityDetailed.cs',13,40),(R,954,977)),
      len({r[2] for r in refs})==1 and len({r[0] for r in refs})==2 and 'Purchase'!='فاتورة مشتريات',
      dict(local_id=5,possible_document_refs=refs,language_is_display_not_identity=True,no_deployment_duplicates_or_child_open_observed=True))
    a(11,'رقم الفاتورة5 لا يساوي الملاحظة memo','P7-063',ref((I,657,667),(IO,3725,3746)),
      str(5)!='memo',dict(InvoiceNo=5,InvNote='memo',csv_under_invoice_number='memo',external_InvNo_alias_not_invented=True))
    start=datetime(2026,1,1);end=datetime(2026,1,2);noon=end+timedelta(hours=12);next_midnight=end+timedelta(days=1)
    a(12,'نهاية منتصف اليوم مفقودة وبداية الغد داخلة وفق المقارنة','P3-023',ref((S,191,205),(S,336,346),(D,261,266),(D,306,313),(I,375,406),(IX,280,309)),
      not(start<=noon<=end) and start<=next_midnight<=next_midnight and not(start<=next_midnight<next_midnight),
      dict(aggregate_excludes_noon_on_end_day=True,detailed_includes_next_midnight=True,inventory_235900_excludes_235930=True,reference_day_range='inclusive-start/exclusive-next-day',not_SQL_executed=True))
    a(13,'نطاق كمية مخزن وفترة لا يحدد سياسة متوسط كل الزمن','P4-007',ref((S,187,205),(S,264,269),(S,364,432),(R,3738,3749)),
      10!=20,dict(selected_store_period_qty=10,cost_source_all_time_other_store_example=20,policy_current_vs_asof='unresolved',certainty='potential',local_unit_defect_separate_P7_041=True))
    a(14,'GlobalID محفوظ لكن route من combo حي قد يختلف','P7-045',ref((I,490,518),(D,609,648),(E,269,300)),
      'rowTypeA'!='liveComboB',dict(row_GlobalID='global-A',row_ProcType=1,row_route='rowTypeA',live_route='liveComboB',positive_row_identity_not_denied=True,live_header_may_also_differ=True))
    a(15,'empty الصحيح والفشل الذي صار empty ليسا الصحة نفسها','P7-046',ref((S,348,361),(IV,354,378),(E,151,159),(E,194,210),(D,319,413)),
      dict(rows=[],card=0,health='valid-empty')!=dict(rows=[],card=0,health='failed'),
      dict(helper_failure_rows=[],valid_empty_rows=[],same_visible_count=0,required_health_states=['valid-empty','failed','partial'],UpdateSummary_empty_counterevidence=True,no_fault_injection=True))
    a(16,'تغيير الاسم وحده لا يبطل ID قديم في النموذج','P7-085',ref((S,434,510),(D,812,824),(E,215,263)),
      dict(text='B',id=7)!=dict(text='B',id=None),dict(selected_A_id=7,edited_text='B',local_retained_id=7,reference_dirty_id=None,reset_and_name_search_are_positive_controls=True))
    sample=['A"B','1,234.00','line1\nline2'];buf=io.StringIO(newline='');csv.writer(buf).writerow(sample)
    a(17,'quote حول النص دون escaping لا يضمن CSV round-trip','P7-048',ref((I,657,680),(S,730,765),(D,912,935),(E,335,365)),
      next(csv.reader(io.StringIO(buf.getvalue(),newline='')))==sample and len('1,234.00,memo'.split(','))==3,
      dict(reference_stdlib_roundtrip=sample,intended_raw_fields=2,raw_comma_parts=3,quoted_forms_still_need_double_quotes=True,no_business_file=True))
    a(18,'ترميز CSV بنيوي وسياسة text-cell عقدان مختلفان','P7-049',ref((I,657,680),(S,730,765),(D,912,935),(E,335,365)),
      'csv-quoted'!='typed-text',dict(probe='INERT_FORMULA_PREFIX_LABEL',csv_quoting='syntax-only',required_consumer_policy='text-or-approved-typed-cell',certainty='potential',formula_or_consumer_executed=False))
    detailed_order=['write','launch','scope-dispose'];other_order=['write','block-dispose','launch']
    a(19,'using-var التفصيلي ينتهي بعد launch، والآخرون قبله','P7-108',ref((D,902,940),(S,730,765),(E,335,365),(I,675,680)),
      detailed_order.index('launch')<detailed_order.index('scope-dispose') and other_order.index('block-dispose')<other_order.index('launch'),
      dict(detailed_events=detailed_order,other_events=other_order,certainty='potential',truncated_file_not_observed=True,WriteAllText_is_completion_before_return=True))
    batches=[(1,1,7,'2026-01-31',5),(1,1,7,'2026-02-28',3),(1,2,7,'2026-01-31',5),(2,1,7,'2026-01-31',5)]
    a(20,'حبيبة الصلاحية لا تخفي المخزن والفرع مثل UNION تقييم آخر','H7B14-01;H7B14-02',ref((IV,354,378),(R,3724,3736),(R,48125,48132),(CW+'ItemExpirationRow.cs',1,17)),
      len({r[:4] for r in batches})==4 and len({r[2] for r in batches})==1,
      dict(grain=['branch','store','item','expiryDate'],batch_rows=4,distinct_items=1,positive_stock_only=True,not_P4_009_automatic_collapse=True,local_helper_exists=True,supplied_function_not_certified_deployed=True))
    today=date(2026,1,31);expires=date(2026,2,1)
    a(21,'DATEDIFF حدود تقويم مستقلة وToday ليس أقل من Today','H7B14-01',ref((E,194,210),(R,3731,3736)),
      expires.month-today.month==1 and (expires-today).days==1 and not(today<today),
      dict(independent_year_boundaries=0,independent_month_boundaries=1,independent_day_boundaries=1,not_decomposed_0year_1month_1day_duration=True,expiry_today_excluded_from_expired_count=True,null_expiry_not_expired=True,policy_not_finalized=True))
    a(22,'DTO محلي وحملان يحتاجان كائناً، لا اختيار compiler مفترض','P1-004;P7-055;H7B14-02',ref((I,725,741),(RP,380,406),(RP,531,553),(D,609,650),(ID,1,303)),
      4==4 and 5>0,
      dict(GridView_required_args=4,DataTable_required_args=4,DataTable_additional_optional_args=5,actual_source_object=None,overload_or_build_not_certified=True,detailed_Quantity_field='',external_template_balance='unknown-not-asserted-empty',copies_is_consumed=True))
    a(23,'قائمة disabled وApply وعمر الاتصال ليست قبول ACL أو قياساً','P1-013;P2-010;P2-011;H7B14-03;H7B14-04',ref((H,2872,2888),(H,2949,2962),(HX,379,389),(S,70,97),(SX,1,14),(S,224,268),(MC,349,455)),
      13*2==26 and 'handler-exists'!='event-wired',
      dict(aggregate_source_sum_queries_for_two_items=26,additional_average_queries_not_included=True,comment_single_query_not_adopted=True,aggregate_Closing_handler_present=True,own_xaml_Closing_hook_absent=True,deployed_ACL='unknown',latency_index_leak='not-measured',seven_C_not_started=True))
    a(24,'ست فئات قديمة فيها خمس أجسام كاملة؛ أربع ترقيات تترك اثنتين','H7B14-06','none-inventory-only',6-4==2 and 5-3==2,
      dict(old_categories_at_entry=6,of_them_prior_full_CSharp=5,local_B14_body_xaml_upgrades=4,of_four_prior_full_CSharp=3,newly_full_CSharp_among_four=1,remaining_old_category=2,B_planning_groups_retained=4,C_unstarted_axes=6,not_whole_B_R1_closed=True,counts_not_sessions_or_completion_percent=True))

    l(1,'ComboBox بلا مصدر وخياراتها لا تعبأ محلياً','P7-120',[
        (DX,98,107,('x:Key="ModernComboBox"',)),(DX,424,433,('x:Name="cmbProcType"','SelectionChanged="cmbProcType_SelectionChanged"/>')),
        (D,55,94,('LoadSafes();','LoadBranches();','LoadPrintSettings();')),(D,280,287,('cmbProcType.SelectedIndex != -1','BuildProcTypeCondition')),
        (D,416,464,('12 =>','_  => ""')),(D,678,688,('cmbProcType.IsEnabled','SelectedIndex = -1')),(MC,331,342,('public static void DoApplyUserSett',))],
        [(D,1,1196,('cmbProcType.ItemsSource','cmbProcType.Items.')),(DX,424,433,('ItemsSource=','ComboBoxItem'))])
    l(2,'مسار مظهر يكتب ويحذف دون قارئ محلي مرفق','P7-121',[
        (D,70,94,('RptItemsActivityDetailed.xml','StyleFolder')),(D,938,1004,('MenuItemSaveSetting_Click','XmlTextWriter','WriteStartElement("GridLayout")','WriteAttributeString("Width"','File.Delete(StyleFile)')),
        (DX,801,805,('Click="btnDgvSettings_Click"',))],
        [(D,1,1196,('ReadAllText','XmlReader','XmlDocument','XDocument','LoadLayout','ReadXml'))])
    l(3,'LastProcess يضبط selected store لا all flag','P7-122',[
        (D,209,235,('if (storeId > 0)','cmbSafes.SelectedValue = storeId;','ShowResult();')),
        (D,253,260,('chkAll.IsChecked != true','Inv_sub.store=')),(DX,288,296,('x:Name="chkAll"','IsChecked="True"')),
        (P,1139,1167,('frm.Show();','frm.LastProcess(item.ItemId, item.InvertoryId'))],
        [(D,209,235,('chkAll.IsChecked = false','chkAll.IsChecked=false'))])
    l(4,'val وval1 وسعر الوحدة ومقام التحويل معرّفة في الكاتب','P7-041',[
        (IO,2073,2076,('item.UnitEquality','item.PrimaryQnty','item.Quantity','item.Price')),
        (IO,5030,5034,('PrimaryQnty','UnitEquality')),(S,364,428,('SUM(val * exchange_price)','totalCostValue / totalQty')),
        (D,292,296,('exchange_price/NULLIF(UnitEquality,0)','val*(exchange_price/NULLIF(UnitEquality,0))'))])
    l(5,'النوعان7 و8 يذهبان إلى الأعمدة المتبادلة','P7-056',[
        (S,232,294,('transToVal = GetSumVal(itemDbId, 7','safeAdjVal = GetSumVal(itemDbId, 8','DgvTransTo','DgvSafeAdj')),
        (R,3054,3064,('تسوية','مناقلة')),(SX,649,700,('DgvTransTo','DgvSafeAdj'))])
    l(6,'قائمة13 مجموعاً بلا نوع6 ثم حارس حذف بلا حركة','P7-057',[
        (S,232,268,('GetSumVal(itemDbId, 9','GetSumVal(itemDbId, 8','if (!hasMovement) continue;')),
        (W,1425,1494,('"@proc_type"','"@InvGlobalID"'))],[(S,232,268,('GetSumVal(itemDbId, 6',))])
    l(7,'LoadClients يملأ id فعلاً لكن كتلة العميل لا ترشح','P7-058',[
        (S,199,205,('cmbClients.SelectedIndex > -1','نتجاهله')),(S,904,943,('ItemsSource','SelectedValuePath','id')),
        (SX,413,446,('ComboBoxItem',))],[(S,312,347,('cust_id','customerId'))])
    l(8,'TOP1 مع ORDER BY ASC وآخرحركة في API','P7-059',[
        (D,209,235,('cbLastProcess.IsChecked = true',)),(D,261,266,('top (1)',)),(D,289,304,('ORDER BY inv.date ASC',)),
        (D,745,758,('cbLastProcess.IsChecked',))])
    l(9,'استثناء اتجاه السطر للنوع7 فقط لا للإنتاج6','P7-060',[
        (D,319,356,('invType == 7','ProcType={procTypeSub}','ProcType={procType}','if (isInput == 1)')),
        (W,1360,1366,('ProcType',)),(W,1425,1494,('SqlDbType.Int).Value = 1','SqlDbType.Int).Value = 2'))])
    l(10,'DTO عرض بلا GlobalID وroute نصي وSQL رقم محلي','P7-061',[
        (D,359,387,('NameEn','DgvInvNo','row["id"]')),(D,1011,1172,('case "فاتورة مشتريات"','WHERE id={invNo}')),
        (R,954,977,('InvGlobalID',)),(R,1012,1017,('PRIMARY KEY',)),(CW+'ItemActivityRow_ActivityDetailed.cs',13,40,('DgvInvType','DgvInvNo'))],
        [(CW+'ItemActivityRow_ActivityDetailed.cs',1,40,('GlobalID','BranchId','LineId'))])
    l(11,'CSV يكتب InvNote والكاتب يسند id إلى InvoiceNo','P7-063',[
        (I,657,667,('inv.InvNote','رقم الفاتورة')),(IO,3725,3746,('invoiceTxt.InvoiceNo','invoiceTxt.InvNote','["id"]','["notes"]'))])
    l(12,'الفترة تمرر end.Date مقابل end.Date+24','P3-023',[
        (S,191,205,('Inv.date<=@date2',)),(S,336,346,('Value = dateTo.Date',)),(D,261,266,('date<=@date2',)),
        (D,306,313,('txtDateTo.DateTime.Date.AddHours(24)',)),(I,375,406,('BETWEEN @date1 AND @date2',)),(IX,280,309,('00:00','23:59'))])
    l(13,'CalcAvgCost يأخذ branch فقط لا extraFilter أو cutoff','P4-007',[
        (S,264,269,('CalcAvgCost(itemDbId, branchFilter)',)),(S,364,432,('CalcAvgCost(int itemId, string branchFilter)','Currency_Lastprice_Sub','inv.proc_type=3')),
        (R,3738,3749,('@store','exchange_price*inv_sub.val1'))],[(S,364,432,('extraFilter','@date1','@date2'))])
    l(14,'هوية الصف محفوظة لكن route/DTO من controls حية','P7-045',[
        (I,490,518,('invTxt.InvGlobalID','invTxt.ProcType','switch (cmbType.SelectedIndex)')),
        (D,609,648,('SafeMain','cmbSafes.Text','MainItemName','txtItemName.Text','txtDateFrom.DateTime')),
        (E,269,300,('cmbSafes','txtItemName'))])
    l(15,'catch إلى صفر/empty وUpdateSummary للـempty موجودة','P7-046',[
        (S,348,361,('catch','return 0.0')),(IV,354,378,('catch (Exception ex)','return new DataTable()')),
        (E,151,159,('UpdateSummary();','return;')),(E,194,210,('_gridData.Count','DateTime.Today')),
        (D,391,413,('ActivityList.Add(item);','txtTotStock.Text','catch'))])
    l(16,'نص الصنف وKeyDown دون TextChanged يبطل ID','P7-085',[
        (S,434,510,('selectedItemId',)),(D,471,531,('SelectedId',)),(D,812,824,('SearchByName()',)),(E,215,263,('ItemId',)),
        (SX,324,342,('txtItemName','txtItemCode')),(DX,323,341,('txtItemName','txtItemCode')),(EX,323,327,('txtItemName',))],
        [(SX,324,342,('TextChanged=',)),(DX,323,341,('TextChanged=',)),(EX,323,327,('TextChanged=',))])
    l(17,'CSV خام في اثنين وquote غير كامل في اثنين','P7-048',[
        (I,657,680,('StringBuilder','inv.InvNote','File.WriteAllText')),(D,912,935,('DgvItemName','DgvBlc:N2')),
        (S,730,765,('StreamWriter','DgvItemName','row.ItemArray')),(E,335,365,('StreamWriter','ItemName'))],
        [(S,730,765,('.Replace(',)),(E,335,365,('.Replace(',))])
    l(18,'نصوص الاسم/الملاحظة والطرف تصل إلى CSV','P7-049',[
        (I,657,680,('inv.InvNote',)),(S,730,765,('r.DgvItemName',)),(D,912,935,('item.DgvClient','item.DgvRefNo')),
        (E,335,365,('r.ItemName',))])
    l(19,'تفصيلي using-var؛الثلاثة الأخرى تنهي الكتابة قبل launch','P7-108',[
        (D,902,940,('using var writer','Process.Start')),(S,730,765,('using (var sw','Process.Start')),
        (E,335,365,('using (var sw','Process.Start')),(I,675,680,('File.WriteAllText','Process.Start'))],
        [(D,902,935,('writer.Flush','writer.Dispose'))])
    l(20,'helper محلي وUDF بداية وترقية يحتفظان بالهوية','H7B14-01;H7B14-02',[
        (IV,1,12,('namespace SmartAuditERP',)),(IV,354,378,('ItemsExpirationStock(string cond)','dbo.ItemsExpirationStock()','ItemStock > 0')),
        (R,3724,3736,('tb.BranchId','tb.store','SUM(stockIn-stockOut)','CAST(expire_date AS DATE)')),
        (R,48125,48132,('IF NOT EXISTS','ItemsExpirationStock','tb.BranchId','tb.store'))])
    l(21,'DATEDIFF مستقلة والعد rows والمقارنة strict less','H7B14-01',[
        (R,3731,3736,('DATEDIFF(YEAR','DATEDIFF(MONTH','DATEDIFF(DAY','GETDATE()')),
        (E,194,210,('_gridData.Count.ToString()','r.ItemExpire.HasValue','r.ItemExpire.Value < DateTime.Today')),
        (CW+'ItemExpirationRow.cs',1,17,('DateTime?','RemaindeDays'))])
    l(22,'حملان بأربع إلزامية وDTO محلي وREPX مستعمل فعلاً','P1-004;P7-055;H7B14-02',[
        (I,725,741,('null, // GridView2',)),(RP,380,406,('BindToData(GridView GridView1','GridView1.RowCount')),
        (RP,531,553,('DataTable dt','string sumTotal = "0"','string sumNetFinal = "0"','dt.Rows')),
        (D,531,650,('XtraReport.FromFile','i <= PrintNo','Quantity      = ""','SumBalance')),
        (ID,1,14,('class InventoryData',))])
    l(23,'Home new/Apply وdisabled، Closing للتجميعي غير موصولة محلياً','P1-013;P2-010;P2-011;H7B14-03;H7B14-04',[
        (H,2872,2888,('new frmRptItemsActivityDetailed','ApplyPermissionToForm','new frmRptItemsActivity')),
        (H,2949,2962,('new frmRptInventory','new frmRptItemsExpiration')),(HX,379,389,('IsEnabled="False"',)),
        (S,70,97,('Window_Closing','conn?.Close()')),(SX,1,14,('Loaded=',)),(I,114,117,('Window_Closing','_conn?.Close()')),
        (IX,14,15,('Closing="Window_Closing"',)),(MC,349,455,('btnPrint','btnShow'))],[(SX,1,14,('Closing=',))])
    l(24,'قيود الفروع/المخازن الإيجابية موجودة لكن ليست سياسة نشر','P2-010;P2-011',[
        (I,177,213,('FROM Branches','BranchPermissions')),(S,103,119,('FROM Safes','IS_Deleted=0')),
        (D,101,113,('FROM Safes','IS_Deleted=0')),(D,274,279,('cmbBranches.SelectedValue',)),
        (E,98,118,('BranchCondition',)),(E,138,151,('StoreID=','BranchId='))])
    return dict(phase='7B14-partial-static-audit',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,default_aggregate_gate_not_assumed_resolved=True,
        supplied_sql_not_certified_deployed=True,progress_categories_not_wholly_unread_counts=True,
        local_expiry_helper_and_dto_not_claimed_missing=True,B_R1_residual_contracts_not_closed=True,
        illustration_count=len(w.alg),static_lexical_contract_check_count=len(w.lex),illustrations=w.alg,
        static_lexical_contract_checks=w.lex,bounded_source_reads_not_semantic_coverage=list(w.reads.values()),
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False),
        errors=w.errors,limit=LIMIT)


if __name__=='__main__':
    value=build();print(json.dumps(value,ensure_ascii=False,indent=2));raise SystemExit(bool(value['errors']))
