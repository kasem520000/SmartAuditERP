#!/usr/bin/env python3
"""B13:20 manual illustrations and20 bounded literal-source observations.

These sketches are NOT translation/execution of C#/SQL or WPF/REPX/Office.
Read inert source only for lexical observations; never import/build ERP, run
queries, interpret HTML/formulas, write business exports, launch consumers,
print, remediate or measure deployment. All example data is invented.
"""
from __future__ import annotations
import hashlib
import html
import json
from decimal import Decimal, ROUND_HALF_EVEN
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/'; CL='SmartAuditERP/Class/'
T=F+'frmMezanMorg3a.xaml.cs'; TX=F+'frmMezanMorg3a.xaml'
R=F+'frmRptBalances.xaml.cs'; C=F+'frmRptCostCenter.xaml.cs'
K=F+'frmRptKhzna.xaml.cs'; KX=F+'frmRptKhzna.xaml'
H='SmartAuditERP/Home.xaml.cs'; HX='SmartAuditERP/Home.xaml'
MC=CL+'MainClass.cs'; AC=CL+'Accounting.cs'; US=CL+'User.cs'
D=CL+'RestrictionData.cs'; KD='SmartAuditERP/Class_WPF/KhznaRow.cs'
AB=F+'frmAccountBalance.xaml.cs'; ABX=F+'frmAccountBalance.xaml'
LIMIT=('تصوير يدوي مستقل لعقد محدود، لا ترجمة أو تشغيل C#/SQL/WPF/REPX/Office أو قبول ERP/مال/ACL. '
       'بيانات خيالية ونصوص خاملة فقط، لا ملفات تصدير فعلية أو طابعة أو shell أو مفسر HTML/صيغة. '
       'لا كل caller/child/template/deployment. P3-022 باقية، والمخطط المرفق ليس شهادة نشر. '
       'أعداد العمق والمسارات مجموعات تنظيم لا نسبة اكتمال أو جلسات مضمونة.')
TEXT_LIMIT=('وجود/غياب tokens داخل المقاطع المحددة فقط؛ لا AST دلالي أو ترجمة أو صحة SQL أو WPF rendering '
            'أو معيار محاسبي أو تفويض/إتاحة نشر أو قياس تسرب/فهرس/زمن.')


def additive_b10_arithmetic_erratum():
    """Retain an additive correction, not a rewrite of protected B10 history."""
    return dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False)


def ref(*ranges):return ';'.join(f'{p}:{a}-{b}' for p,a,b in ranges)


class Witness:
    def __init__(self):self.errors=[]; self.alg=[]; self.lex=[]; self.reads={}
    def require(self,p,message):
        if not p:self.errors.append(message)
    def text(self,p,a,b):
        raw=(ROOT/p).read_bytes()
        try:s=raw.decode('utf-8-sig')
        except UnicodeDecodeError:s=raw.decode('cp1256')
        lines=s.splitlines(); self.require(1<=a<=b<=len(lines),'Bounded range: '+p)
        s='\n'.join(lines[a-1:b])
        self.reads[(p,a,b)]=dict(path=p,start=a,end=b,selected_text_sha256=hashlib.sha256(s.encode()).hexdigest())
        return s
    def illustration(self,n,title,roots,evidence,passed,details):
        self.require(passed,'ALG '+str(n))
        self.alg.append(dict(id=f'ALG7B13-{n:02d}',title=title,finding_ids=roots,evidence=evidence,
            illustration_assertions_passed=bool(passed),details=details,source_application_executed=False,limit=LIMIT))
    def lexical(self,n,title,roots,checks,absent=()):
        ok=True; refs=[]
        for p,a,b,tokens in checks:
            s=self.text(p,a,b); refs.append((p,a,b))
            for token in tokens:ok=bool(token in s) and ok
        for p,a,b,tokens in absent:
            s=self.text(p,a,b); refs.append((p,a,b))
            for token in tokens:ok=bool(token not in s) and ok
        self.require(ok,'ST '+str(n))
        self.lex.append(dict(id=f'ST7B13-{n:02d}',title=title,finding_ids=roots,evidence=ref(*dict.fromkeys(refs)),
            documented_text_observation_matches=ok,source_application_executed=False,limit=TEXT_LIMIT))


def build():
    w=Witness(); a=w.illustration; l=w.lexical
    # Tiny hand-selected sketches below, NOT an interpreter for the source.
    nodes={1:0,11:1,111:11,1111:111}
    def local_level(max_level):
        return [n for n,p in nodes.items() if (p==0 and max_level>=0) or (p!=0 and max_level>=1 and nodes.get(p)==0)]
    a(1,'المستويان2 و3 يعيدان الجذر والأبناء المباشرين فقط','P7-118',ref((T,540,568),(TX,194,198)),
      local_level(0)==[1] and local_level(1)==local_level(2)==[1,11] and 111 not in local_level(2),
      dict(local_level2=local_level(1),local_level3=local_level(2),reference_level3=[1,11,111],all_button_counterevidence=list(nodes)))
    columns=['openingD','openingC','previousD','previousC','moveD','moveC','balanceD','balanceC','finalD','finalC']
    printed=[v for v in columns if not v.startswith('previous')]
    a(2,'الإسقاط المحلي10 حقول مقابل12 في الجدول وHTML','P7-119',ref((T,635,667),(T,794,830),(TX,280,293)),
      len(columns)+2==12 and len(printed)+2==10 and 'previousD' not in printed,
      dict(grid_and_html_fields_with_identity=12,flow_document_fields_with_identity=10,missing=['previousD','previousC'],previous_example=100,closing_example=100))
    opening,previous,movement=0,40,10; leaf_final=opening+previous+movement; parent_final=opening+movement
    a(3,'السابق موجود في الورقة ويسقط من إقفال الأب والمسار الفرعي فقط','P3-019',ref((T,323,345),(T,396,448),(T,455,486)),
      leaf_final==50 and parent_final==10,
      dict(leaf_final=leaf_final,parent_final=parent_final,secondary_previous=0,reference_final=50,period_specific_previous_enabled_assumed=True))
    a(4,'جمع صفوف طبقات الشجرة ليس partition مالية','P3-020',ref((T,455,494),(T,508,534)),
      sum([100,100,100])==300 and sum([100])==100,
      dict(all_three_hierarchy_rows_total=300,one_leaf_partition_total=100,root_only_total=100,not_three_findings=True))
    debit,credit=Decimal('100.04'),Decimal('100.00'); q=Decimal('0.1')
    a(5,'مقارنة الحركة بدقة1 لا تثبت تساوي العرض N2 أو الإقفال','P3-020',ref((T,508,534)),
      debit.quantize(q,rounding=ROUND_HALF_EVEN)==credit.quantize(q,rounding=ROUND_HALF_EVEN) and debit!=credit,
      dict(debit=str(debit),credit=str(credit),difference=str(debit-credit),local_rounded_comparison=True,not_a_certified_currency_tolerance=True))
    a(6,'Balances يضيف opening-only لكن لا يعوض كل السابق','P3-019',ref((R,281,298),(R,345,366),(R,396,425)),
      100+0==100 and 100+50==150,
      dict(opening_only_counterevidence=100,prior_non_type0_not_in_period_sketch=50,local_period_result=100,reference_if_same_contract=150))
    # Direct child recurses to the selected root (parent0); unrelated91 takes9.
    local_parent_results={11:0,91:9}; reference_members={1,11}
    a(7,'المركز الغريب يقبل parent غير المحدد بدلاً من إثبات العضوية','P7-052',ref((C,198,234),(C,417,431),(C,487,505)),
      all(p!=-1 for p in local_parent_results.values()) and 91 not in reference_members,
      dict(local_parent_results=local_parent_results,reference_member_codes=sorted(reference_members),unrelated91_accepted_in_sketch=True,subtype2_sql_filter_counterevidence=True))
    a(8,'أول افتتاحي للمركز يتكرر ولا يوجد union للافتتاحي وحده','P7-053',ref((C,315,376),(C,433,505)),
      100*2==200 and 100+50==150,
      dict(first_matching_center_opening=100,two_movement_accounts_local_reuse=200,two_keyed_openings_reference=150,opening_only_center_local_rows=0,not_balances_opening_only_behavior=True))
    a(9,'اسم الحساب المتساوي لا يمثل مفتاح الحساب','P7-053',ref((C,433,465)),
      len({('name',7),('name',7)})==1 and len({(101,7),(102,7)})==2,
      dict(same_name_center_groups=1,distinct_account_codes=2,uniqueness_requires_contract=True))
    movements=[(9,20),(11,5)]; instant_sum=sum(value for hour,value in movements if hour>=10)
    a(10,'تجميع اليوم مقابل تفصيل يبدأ10:00','P3-023',ref((C,307,349),(C,433,473)),
      instant_sum==5 and sum(v for _,v in movements)==25,
      dict(reference_instant_movement=instant_sum,day_range_movement=25,day_vs_instant_requires_explicit_contract=True))
    a(11,'قطع السابق عند منتصف الليل يترك فجوة حتى وقت البداية','P7-062',ref((K,184,223),(K,240,300)),
      100+5==105 and 100+20+5==125,
      dict(prior_before_midnight=100,unselected_9am=20,selected_after10=5,local_final=105,reference_final=125))
    a(12,'أول اسم صندوق مطابق لا يحسم هوية الحساب','P3-008',ref((K,156,176)),
      [11,22][0]!=22,
      dict(name_matches=[11,22],declared_identity_example=22,first_local_candidate=11,branch_predicate_is_positive_counterevidence=True))
    shared=['A']; display_a=list(shared); shared[:]=['B']; after_filter=list(shared)
    a(13,'المصدر static يسمح بتبديل بيانات A عند فلتر لاحق','P7-045',ref((T,90,91),(T,199,225),(T,549,568)),
      display_a==['A'] and after_filter==['B'],
      dict(A_before=display_a,A_after_filter=after_filter,not_wpf_instances_executed=True))
    parent_criteria=('periodA','branch1'); child_defaults=('periodNow','branchDefault')
    a(14,'اختيار الحساب وحده لا ينقل معايير الأب إلى الطفل','P7-045',ref((T,582,595),(R,455,470),(AB,42,103),(ABX,120,132)),
      parent_criteria!=child_defaults,
      dict(parent_criteria=parent_criteria,child_default_sketch=child_defaults,selection_only_copied='account',aggregate_P3_022_not_assumed_fixed=True))
    partial=dict(rows=[5],card=100,health='unlabelled'); atomic=dict(rows=[],card=None,health='failed')
    a(15,'الصفوف الجزئية والبطاقات السابقة ليست نشراً ذرياً','P7-046',ref((R,238,265),(R,429,449),(K,227,305)),
      partial!=atomic,
      dict(manual_possible_late_failure_state=partial,reference_failed_state=atomic,no_fault_injection=True,cards_not_always_stale=True))
    a(16,'N2 غير المقتبس يمكن أن يقسم الحقول؛ سياسة الخلية مستقلة','P7-048;P7-049',ref((K,403,420),(R,489,510),(C,668,693)),
      len('1,234.00,note'.split(','))==3,
      dict(intended_fields=2,comma_split_fields=3,formula_probe='INERT_TEXT_ONLY',quote_escaping_not_formula_policy=True))
    a(17,'هوية الصيغة مخالفة للامتداد مع بقاء المسار نفسه','P7-050',ref((T,609,667),(K,393,420)),
      ('HTML','xls')!=('XLS','xls') and ('CSV','xlsx')!=('XLSX','xlsx'),
      dict(trial_payload='HTML',trial_options=['xls','csv'],cashbox_payload='CSV',cashbox_options=['csv','xlsx'],selected_path_not_changed_unlike_P7_116=True))
    template_exists=False; rows_ready=True; raw_name='A&B<value>'
    a(18,'بوابة خارجية غير مستعملة وترميز النص عقدان مختلفان','P7-097;P7-098',ref((T,635,667),(T,694,732),(T,843,867)),
      (template_exists and rows_ready)!=rows_ready and html.escape(raw_name)!=raw_name,
      dict(local_gate_permits=False,reference_local_renderer_ready=True,raw_text=raw_name,encoded_text=html.escape(raw_name),flow_run_is_text=True,no_interpreter=True))
    events=['using_var_start','write','success','consumer_launch','scope_exit_dispose']
    a(19,'حد using-var ينتهي بعد إطلاق المستهلك؛ الأثر محتمل','P7-108',ref((K,403,427),(R,505,510),(C,688,693)),
      events.index('consumer_launch')<events.index('scope_exit_dispose'),
      dict(local_event_sketch=events,buffer_or_external_read_not_measured=True,WriteAllText_completes_before_return_counterevidence=True))
    a(20,'تصنيف10 قديم يتضمن8 أجسام C# كاملة سابقاً','H7B13-06','none-inventory-only',10-4==6 and 8>0,
      dict(old_depth_dispositions=10,prior_full_csharp_among_them=8,local_b13_body_xaml_upgrades=4,old_category_remaining=6,
           remaining_B_planning_packages=4,C_unstarted_axes=6,counts_not_sessions_or_completion_percent=True))

    l(1,'أزرار المستوى2/3 وفرع الأب المباشر نفسه','P7-118',[
        (T,540,568,('FilterByLevel(1)','FilterByLevel(2)','maxLevel >= 1','p.TrParentAcc == 0')),
        (TX,194,198,('btnlvl3_Click','المستوى 3'))])
    l(2,'السابق حاضر في الجدول وHTML وغائب عن المستند المحلي','P7-119',[
        (TX,280,293,('TrDeptPervious','TrCreditPervious')),(T,635,667,('TrDeptPervious','TrCreditPervious')),
        (T,794,830,('i < 10','TrDeptIntial','TrDeptFinal'))],[(T,794,830,('TrDeptPervious','TrCreditPervious','سابق'))])
    l(3,'leaf يحسب السابق والمساران الآخران لا يدخلانه في الإقفال','P3-019',[
        (T,396,448,('double num9 = num3 + num7 + num;','account.TrDeptPervious = (decimal)num;')),
        (T,323,345,('double num9 = num3 + num7;','0, 0,')),
        (T,455,486,('root.TrDeptPervious','root.TrDeptFinal = root.TrDeptIntial + root.TrDeptBlc;'))],
        [(T,475,476,('TrDeptPervious','TrCreditPervious'))])
    l(4,'CalcSum يجمع كل صف ظاهر ويقارن الحركة بدقة1','P3-020',[
        (T,508,534,('foreach (AccountNode row in _displayRows)','Math.Round(sumDebt, 1)','Math.Round(sumCredit, 1)','ToString("N2")'))])
    l(5,'Balances افتتاحي مقيد بالفترة مع إضافة opening-only صريحة','P3-019',[
        (R,281,298,('Entry.type=0','{dateCond}','AddHours(24)')),(R,345,366,('if (!exists)','di, ci, 0, 0'))])
    l(6,'GetParent يختار عند عدم المساواة؛التفصيل يجلب الأبناء المباشرين','P7-052',[
        (C,198,234,('if (parentVal != selectedVal)','_parentCode = (int)parentVal;','GetParent((int)parentVal)')),
        (C,273,291,('ParentCode=','costCenterList.Add')),(C,417,431,('ccType == 2','Entry_sub.CCcode='))])
    l(7,'opening center-only/break وتجميع اسم الحساب بلا code','P7-053',[
        (C,352,376,('initRow["CCcode"].ToString() == row["CCcode"].ToString()','break;')),
        (C,433,465,('GROUP BY Entry_sub.CCcode, Accounts_Index.Aname, cost_center.name',)),
        (C,493,505,('initRow["CCcode"].ToString() == row["CCcode"].ToString()','break;'))],
        [(C,493,502,('acc_no','AccName'))])
    l(8,'detail instant مقابل aggregate/opening shortdate+24','P3-023',[
        (C,307,349,('DateTime.Parse','Value = fromDt','Value = toDt','AddHours(24)')),
        (C,433,473,('ToShortDateString()','AddHours(24)')),(R,258,298,('Value = fromDt','Value = toDt','AddHours(24)'))])
    l(9,'ميزان المراجعة يستعمل نهاية يوم نصف مفتوحة في الحركة','P3-023',[
        (T,244,296,('Entry.date>=@date1','Entry.date<@date2','AddHours(24)')),
        (T,365,383,('Entry.date>=@date1','Entry.date<@date2'))])
    l(10,'الصندوق previous shortdate مقابل dt1 للحركة','P7-062',[
        (K,179,257,('dateFrom.Date + startTime','dateFrom.ToShortDateString()','Value = dt1','Entry.date<@date1')),
        (K,266,300,('runBalance += dept - credit','runBalance - priorBalance')),(KX,292,298,('23:59',))])
    l(11,'ربط الحساب بالاسم والفرع ثم أخذ أول صف','P3-008',[
        (K,156,176,('Accounts_Index.AName=Stocks.name','Accounts_Index.acc_branch=Stocks.branch','accDt.Rows[0][0]'))])
    l(12,'Home Apply/new/static و disabled و Close شواهد متمايزة','P1-013;P1-030',[
        (H,95,96,('_frmRptKhzna','??')),(H,2616,2667,('new frmMezanMorg3a','new frmRptBalances','new frmRptCostCenter','ApplyPermissionToForm','frmRptKhzna.Show')),
        (HX,335,340,('IsEnabled="False"','stripShowKhzna_Click','StripRptCostCenter_Click')),(K,372,373,('Close()',))])
    l(13,'static AccountList والطفل account-only بعد Apply','P7-045;P1-013',[
        (T,90,91,('static List<AccountNode> AccountList',)),(T,549,568,('foreach (AccountNode node in AccountList)',)),
        (T,582,595,('ApplyPermissionToForm','Show();','cmbAccounts.SelectedValue','ShowAccountData();')),
        (R,455,470,('ApplyPermissionToForm','cmbAccounts.SelectedValue'))])
    l(14,'افتراضيات الطفل و aggregate gate السابق لا يختفيان','P7-045',[
        (AB,42,103,('DateTime.Now','LoadBranches();')),(ABX,120,132,('btnAggre','IsChecked="True"')),
        (AB,167,250,('row["GlobalID"]','dtResult.Rows.Add'))])
    l(15,'مسح المصادر قبل العمل والبطاقات تحدث لاحقاً','P7-046',[
        (R,238,265,('_balancesSource.Clear();','txtIsBalanced.Text = "";')),(R,429,449,('txtBalance.Text','lblStatus.Text','catch')),
        (K,153,155,('KhznaList.Clear();',)),(K,294,305,('txtTotAll.Text','txtTotPeriod.Text','catch'))])
    l(16,'cashbox CSV خام و WriteAllText قبل shell في الآخرين','P7-048;P7-049;P7-108',[
        (K,403,420,('using var writer','{row.Income:N2}','{row.Note}')),(R,505,510,('File.WriteAllText','Process.Start')),
        (C,688,693,('File.WriteAllText','Process.Start'))])
    l(17,'خيارات xls/csv مع HTML و xlsx مع CSV','P7-050',[
        (T,609,667,('*.xls','*.csv','<html>','File.WriteAllText')),
        (K,393,420,('*.xlsx','*.csv','StreamWriter','writer.WriteLine'))])
    l(18,'trial gate فقط؛الآباء الثلاثة الأخرى تحمل REPX فعلاً','P1-004;P7-097',[
        (T,694,732,('rptMezanMorag3a.repx','File.Exists','BuildPrintDocument')),
        (R,582,608,('XtraReport.FromFile','DataSource = BindToData()')),
        (C,756,778,('XtraReport.FromFile','DataSource = BindToData()')),
        (K,450,471,('XtraReport.FromFile','DataSource = BuildReportDataSet()'))],
        [(T,694,760,('XtraReport.FromFile','LoadLayout'))])
    l(19,'HTML خام مقابل Run نصي و using-var دون finalize قبل launch','P7-098;P7-108',[
        (T,635,667,('{Title}','{row.TrAccName}')),(T,843,867,('new Run(text)',)),
        (K,403,427,('using var writer','Process.Start(new ProcessStartInfo(path)'))],
        [(K,403,427,('writer.Dispose','writer.Flush'))])
    l(20,'فروع الرأس/السطر وClosing وDTO ليست تفويضاً أو قياساً','P1-013;P2-010;P1-004',[
        (T,235,244,('Entry_sub.branch','Entry.branch')),(R,246,256,('Entry_sub.branch','Entry.branch')),
        (C,634,641,('Entry.branch',)),(AC,1,14,('BranchCondition',)),
        (US,108,114,('ShowBranchsAccounts = true','BranchCondition = " "')),
        (MC,349,455,('btnPrint','btnPreview','btnShow')),(R,65,68,('_conn?.Close()',)),(C,63,66,('_conn?.Close()',)),
        (D,31,42,('DeptPervious','CreditPervious')),(KD,8,16,('ProcessNo','Income','Outcome','Balance'))])
    return dict(phase='7B13-partial-static-audit',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        default_aggregate_gate_not_assumed_resolved=True,supplied_sql_not_certified_deployed=True,
        progress_categories_not_wholly_unread_counts=True,illustration_count=len(w.alg),static_lexical_contract_check_count=len(w.lex),
        illustrations=w.alg,static_lexical_contract_checks=w.lex,bounded_source_reads_not_semantic_coverage=list(w.reads.values()),
        retained_additive_B10_arithmetic_erratum=additive_b10_arithmetic_erratum(),errors=w.errors,limit=LIMIT)


if __name__=='__main__':
    result=build(); print(json.dumps(result,ensure_ascii=False,indent=2)); raise SystemExit(bool(result['errors']))
