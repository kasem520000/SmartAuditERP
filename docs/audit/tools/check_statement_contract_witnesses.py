#!/usr/bin/env python3
"""Deterministic B11 manual contrasts and bounded inert-source observations.

No ERP imports, translation/build, SQL/WPF/REPX/Office, file exports or shell.
Default populated aggregate P3-022 is not assumed fixed; supplied SPs are not
certified deployed SPs. Hand models isolate gates with well-formed detail rows.
An additive B10 arithmetic erratum leaves all protected prose/checks unchanged.
"""
from __future__ import annotations
import hashlib
import json
from datetime import datetime
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/'; C='SmartAuditERP/Class/'
D=F+'frmAccountBalance.xaml.cs'; DX=F+'frmAccountBalance.xaml'
P=F+'frmAccountsStatement.xaml.cs'; PX=F+'frmAccountsStatement.xaml'
J=F+'frmRptEntries.xaml.cs'; JX=F+'frmRptEntries.xaml'
RS='SmartAuditERP/Properties/Resources.resx'; HM='SmartAuditERP/Home.xaml.cs'; HX='SmartAuditERP/Home.xaml'
EO=C+'EntryOper.cs'; MC=C+'MainClass.cs'; IO=C+'InvoiceOper.cs'
ILL=[]; ST=[]; READS={}
LIMIT=('Independent hand-selected documentary contrast only; NOT C#/SQL/WPF execution or translation, '
       'deployed procedure/schema/ACL/policy acceptance, financial certification or remediation. '
       'The default populated aggregate P3-022 gate is NOT assumed fixed; downstream contrasts isolate '
       'well-formed detail rows. Supplied SQL is not certified deployed. No real data, secrets, exports, '
       'formula interpreter, Office, printer or shell. Synthetic counts are not performance measurements.')
TEXT_LIMIT=('Bounded literal/structural observation of inert source text; NOT a semantic callgraph, '
            'deployed schema/permission/availability proof, SQL execution, WPF rendering, whole-child '
            'review, financial acceptance or measured index/leak/latency. No application execution.')


def ev(*pairs): return ';'.join(f'{p}:{a}-{b}' for p,a,b in pairs)


def illustration(title, roots, inputs, local, reference, difference, refs):
    assert (local != reference) is difference, title
    ILL.append(dict(id=f'ALG7B11-{len(ILL)+1:02d}',title=title,finding_ids=roots,
        hand_selected_inputs=inputs,manual_observation_model=local,independent_reference=reference,
        difference_expected=difference,illustration_assertions_passed=True,evidence=refs,
        source_application_executed=False,limit=LIMIT))


def span(p,a,b):
    raw=(ROOT/p).read_bytes()
    try: text=raw.decode('utf-8-sig')
    except UnicodeDecodeError: text=raw.decode('cp1256',errors='replace')
    lines=text.splitlines(); assert 1<=a<=b<=len(lines)
    text='\n'.join(lines[a-1:b]);READS[(p,a,b)]=dict(path=p,start=a,end=b,selected_text_sha256=hashlib.sha256(text.encode()).hexdigest())
    return text


def literal(title, roots, pairs, predicate, description):
    texts=[span(*p) for p in pairs];ok=bool(predicate(texts));assert ok,title
    ST.append(dict(id=f'ST7B11-{len(ST)+1:02d}',title=title,finding_ids=roots,
        documented_observation=description,documented_text_observation_matches=ok,evidence=ev(*pairs),
        source_application_executed=False,limit=TEXT_LIMIT))


def main():
    states=[dict(state=1,debit=100,deleted=False),dict(state=2,debit=40,deleted=False)]
    illustration('Supplied parent statement admits cancelled as well as approved movements','P7-114',
        dict(rows=states,supplied_definition_not_deployed_certification=True),
        dict(debit=sum(x['debit'] for x in states if not x['deleted'])),
        dict(debit=sum(x['debit'] for x in states if not x['deleted'] and x['state']==1)),True,
        ev((RS,4689,4701),(RS,4721,4735),(D,254,274),(D,314,319),(JX,242,250),(J,226,234)))
    illustration('Approved-only movements are counterevidence to an always-different report total','P7-114',
        dict(rows=[dict(state=1,debit=100)],branch_and_period_and_leaf_grain_aligned=True),
        dict(debit=100),dict(debit=100),False,ev((RS,4721,4735),(D,314,319)))
    illustration('A second Show can switch the queried DB without changing the selected past year','P7-115',
        dict(selected_year='PAST',first_flag=True,flag_after_first=False,current_db='CURRENT',detail_mode_gate_isolated=True),
        dict(requests=['PAST','CURRENT'],visible_selection=['PAST','PAST']),
        dict(requests=['PAST','PAST'],visible_selection=['PAST','PAST']),True,
        ev((D,670,688),(D,839,845),(P,841,858),(P,865,871),(MC,39,49),(MC,115,123)))
    illustration('A current-year selection can legitimately read the same current DB twice','P7-115',
        dict(selected_year='CURRENT',requests_independent=False,no_actual_connection=True),
        dict(requests=['CURRENT','CURRENT']),dict(requests=['CURRENT','CURRENT']),False,
        ev((D,670,688),(D,839,845),(P,841,858)))
    illustration('A populated aggregate projection omits the notes column consumed by its mapper','P3-022',
        dict(mode='aggregate-default',projection=['dept','credit','notes'],consumed_column='subNotes',row_count=1),
        dict(schema_compatible=False),dict(schema_compatible=True),True,
        ev((DX,118,129),(D,304,335),(D,203,241)))
    illustration('Detail schema or zero movements do not take the same missing-column read','P3-022',
        dict(mode='detail',projection=['dept','credit','notes','subNotes'],aggregate_empty_also_skips_loop=True),
        dict(schema_compatible=True),dict(schema_compatible=True),False,
        ev((D,203,241),(D,304,335)))
    illustration('Credit-nature carryforward changes both displayed side and closing magnitude','P3-021',
        dict(previous_debit=0,previous_credit=200,current_debit=0,current_credit=50,first_digit=2,detail_mode=True),
        dict(previous_row_debit=200,previous_row_credit=0,closing_magnitude=abs(-200+50)),
        dict(previous_row_debit=0,previous_row_credit=200,closing_magnitude=abs(-200-50)),True,
        ev((D,209,239),(D,254,274),(D,348,368)))
    row=datetime(2026,1,1,23,59,30);minute_end=datetime(2026,1,1,23,59);next_day=datetime(2026,1,2)
    illustration('Default23:59 exclusive bound drops the final minute of a whole-day policy','P3-023',
        dict(row=row.isoformat(),entered_end=minute_end.isoformat(),whole_day_policy_assumed=True),
        dict(included=row<minute_end),dict(included=row<next_day),True,
        ev((D,40,47),(D,192,208),(D,285,290),(D,322,325),(DX,145,154)))
    illustration('Return-purchase UI index14 is not the supplied return type21','P7-099',
        dict(option_index=14,label='return-purchase',supplied_types={14:'contract',21:'return-purchase'}),
        dict(query_type=14),dict(query_type=21),True,
        ev((D,109,128),(D,299,303),(D,778,782),(RS,3383,3395)))
    illustration('Edited code and retained account selection can describe different accounts','P7-085',
        dict(selected_code=111,selected_name='A',edited_code='222',Enter_pressed=False),
        dict(query_code=222,print_name='A'),dict(query_code=None,print_name='blocked-until-resolved'),True,
        ev((D,167,195),(D,433,445),(D,692,698),(DX,102,107)))
    illustration('A Type2 lookup result need not be a selectable Type1 parent account','P1-033',
        dict(combo_type=1,lookup_type=2,leaf_code=111,combo_codes=[100,200]),
        dict(lookup_result_is_member=111 in [100,200]),dict(lookup_result_is_member=True),True,
        ev((P,85,102),(P,370,444)))
    illustration('The detail Excel success message does not establish that any file was written','P1-033',
        dict(hand_selected_events=['dialog-path','stub-library-message','caller-success','optional-shell'],actual_IO=False),
        dict(file_written=False,success_reported=True),dict(file_written=False,success_reported=False),True,
        ev((D,616,665)))
    candidates=[dict(inv='A',entry_local=7,branch=1),dict(inv='B',entry_local=7,branch=2)]
    illustration('Journal invoice source by local EntryID alone is ambiguous across matching branches','P7-061',
        dict(rows=candidates,selected_entry_global='2-7',selected_branch=2,actual_collision_not_observed=True),
        dict(candidate_invoices=[x['inv'] for x in candidates if x['entry_local']==7]),
        dict(candidate_invoices=[x['inv'] for x in candidates if x['entry_local']==7 and x['branch']==2]),True,
        ev((J,211,220),(J,550,574),(IO,1547,1551),(RS,1012,1017)))
    illustration('EntryOper invoice route retains the branch recovered from the global entry','P7-061;H7B11-04',
        dict(rows=candidates,entry_lookup_yields_branch=2,all_other_routes_not_certified=True),
        dict(candidate_invoices=['B']),dict(candidate_invoices=['B']),False,
        ev((EO,1023,1057),(D,784,792),(P,873,891)))
    illustration('Whitespace permission text can offer all branches but only list one selectable branch','P2-010;H7B11-01',
        dict(BranchCondition=' ',current_branch=1,all_branches_policy_assumed=True,available_branches=[1,2]),
        dict(branch_combo=[1],all_checkbox_available=True),dict(branch_combo=[1,2],all_checkbox_available=True),True,
        ev((P,107,158),(C+'User.cs',108,114)))
    illustration('Live print criteria can label already-loaded rows with a changed account or period','P7-045',
        dict(loaded_period='A',date_control_now='B',reload=False),
        dict(rows='A',print_header='B'),dict(rows='A',print_header='A'),True,
        ev((D,433,468),(P,660,705),(J,630,663),(JX,229,233)))
    illustration('A failed previous-balance source is not a legitimate zero opening balance','P7-046',
        dict(manual_failure_label='previous-query',no_SQL_fault_injection=True),
        dict(value=0,health='unlabelled'),dict(value=None,health='error-or-blocked'),True,
        ev((D,254,280)))
    illustration('Empty parent rows can coexist with totals from the previous nonempty result','P7-046',
        dict(previous_total=100,next_row_count=0,DataView_assigned_before_empty_return=True),
        dict(rows=[],total=100),dict(rows=[],total=0),True,
        ev((P,306,323),(P,330,358)))
    illustration('Main-account typed XLSX finalizes inside using before shell launch','H7B11-03',
        dict(events=['DataTable','XLWorkbook','SaveAs','Dispose','success-message','shell'],actual_export=False,consumer_policy_not_certified=True),
        dict(format='XLSX',finalized_before_shell=True),dict(format='XLSX',finalized_before_shell=True),False,
        ev((P,452,503)))
    illustration('Additive correction of B10 arithmetic prose leaves the protected archive unchanged','H7B11-06',
        dict(entered_quantity=2,equality=12,base_unit_cost=5,archived_prose_local_amount=20,not_source_coverage=True),
        dict(local_cost=2*5,reference_cost=2*12*5,archive_rewritten=False),
        dict(local_cost=10,reference_cost=120,archive_rewritten=False),False,'none-inventory-only')

    literal('Both supplied parent-statement definitions omit e.state in previous and main predicates','P7-114',
        [(RS,4651,4795),(RS,50233,50380),(P,245,265)],
        lambda t: all('PreviousBalance AS' in x and 'MainStatement AS' in x and not re.search(r'\be\.state\b',x,re.I) for x in t[:2]) and 'new SqlCommand("GetAccountStatement"' in t[2],
        'Confirmed LOCAL supplied-SQL eligibility difference; deployed procedure/schema and actual cancelled rows are not established.')
    literal('Detail filters approved state; journal read maps state-1 into approved/cancelled options','P7-114',
        [(D,254,274),(D,314,319),(J,226,234),(JX,242,250)],
        lambda t: all('Entry.state=1' in x for x in t[:2]) and 'Convert.ToInt32(dr["state"]) - 1' in t[2] and 'Content="معتمد"' in t[3] and 'Content="لاغي"' in t[3],
        'State1/2 meanings have selected local UI evidence; all-state audit mode would need explicit separate policy/label, not an inferred deployed policy.')
    literal('Show consumes the global year flag and restores current connection without clearing selected year','P7-115',
        [(D,670,688),(P,841,858),(MC,39,49)],
        lambda t: all('MainClass.ReturnYearPreviews && CmbYearPreviews.SelectedValue != null' in x and 'MainClass.ReturnYearPreviews = false;' in x and 'MainClass.connstr = MainClass.originalConnStr;' in x and 'CmbYearPreviews.SelectedIndex =' not in x for x in t[:2]) and 'new SqlConnection(connstr)' in t[2],
        'A repeated request can use current DB with the same prior-year selection, distinct from changing a printed date after loading rows.')
    literal('The year lists use DbAutoName while selection handlers only set the shared boolean','P7-115;H7B11-02',
        [(D,814,845),(P,205,238),(P,865,871),(MC,115,123),(RS,4798,4810)],
        lambda t: 'SelectedValuePath = "DbAutoName"' in t[0] and 'ReturnYearPreviews = true' in t[0] and 'SelectedValuePath = "DbAutoName"' in t[1] and 'ReturnYearPreviews = true' in t[2] and 'public static bool ReturnYearPreviews = false' in t[3] and '[DbAutoName]' in t[4],
        'Selection persists while the shared one-shot flag changes; database name authorization/schema compatibility remains unresolved, not executed.')
    literal('Aggregate is the XAML default and does not project subNotes read by foreach','P3-022',
        [(DX,118,129),(D,304,335),(D,203,241)],
        lambda t: 'x:Name="btnAggre"' in t[0] and 'IsChecked="True"' in t[0] and 'SUM(Entry_sub.dept)' in t[1] and 'subNotes' not in t[1].split('else // تفصيلي')[0] and 'Entry_sub.notes as subNotes' in t[1] and 'row["subNotes"]' in t[2],
        'Populated aggregate gate persists. Detail/empty counterexamples and hand arithmetic do not repair the application or establish UI success.')
    literal('Previous D-C and credit-nature C-D mix, and DTO carries row balance/status','P3-021',
        [(D,209,239),(D,262,265),(D,348,368),(D,433,451)],
        lambda t: 'runningBalance += (credit - dept)' in t[0] and 'SUM(Entry_sub.dept), 0) - ISNULL(SUM(Entry_sub.credit)' in t[1] and 'credit = balance;' in t[2] and 'Status = item["DgvBalanceStatus"]' in t[3],
        'Existing sign root extends through selected display/DTO evidence, not a new financial finding per output channel.')
    literal('Detail end is parsed at23:59 then passed to a strictly-less-than date predicate','P3-023',
        [(D,40,47),(D,192,208),(D,285,290),(D,322,325),(DX,145,154)],
        lambda t: 'txtEndTime.Text = "23:59"' in t[0] and 'txtEndTime.Text' in t[1] and 'Entry.date < @date2' in t[2] and '"@date2", endDate' in t[3] and 'Text="23:59"' in t[4],
        'Whole-day vs free-time policy must be explicit; typing a timestamp does not supply the missing final minute or certify timezone/culture behavior.')
    literal('Detail uses option index as type ID; journal uses actual EntryTypes.Id instead','P7-099',
        [(D,109,128),(D,778,782),(D,299,303),(RS,3384,3395),(J,104,117),(J,469,478)],
        lambda t: 'مرتجع مشتريات' in t[0] and '_restrictionType = cmbEntryType.SelectedIndex' in t[1] and 'Entry.type={_restrictionType}' in t[2] and "VALUES (21, N'مرتجع مشتريات'" in t[3] and "VALUES (14, N'قيد فاتورة عقد'" in t[3] and 'SelectedValuePath = "Id"' in t[4] and 'Convert.ToInt32(cmbType.SelectedValue)' in t[5],
        'Same prior index/type mismatch root, not a new finding for each misleading return/type label; actual deployed seed semantics need contract.')
    literal('SelectedValue guard does not parameterize the edited detail account code','P1-011;P7-085',
        [(D,167,195),(D,314,327),(D,692,698),(DX,102,107),(D,269,274)],
        lambda t: 'cmbAccounts.SelectedValue == null' in t[0] and 'string accountCode = txtCode.Text;' in t[0] and 'Entry_sub.acc_no={code}' in t[1] and 'txtCode.Text = cmbAccounts.SelectedValue.ToString()' in t[2] and 'IsReadOnly="True"' not in t[3] and 'AddWithValue("@code", code)' in t[4],
        'The previous-balance @code is counterevidence, not protection for another interpolated query. No payload or SQL execution.')
    literal('Parent Type1 combo and Type2 code/name lookups differ; advanced search is a message','P1-033',
        [(P,85,102),(P,370,444),(PX,152,162)],
        lambda t: 'WHERE Type=1' in t[0] and 'WHERE Type=2' in t[1] and "AND type=2" in t[1] and 'وظيفة البحث المتقدم' in t[1] and 'SearchByName' not in t[2],
        'SearchByName is defined but no local XAML event calls it. Do not describe that helper as a proven reachable UI search.')
    literal('Detail Excel helper has no write while caller reports success','P1-033',
        [(D,616,651),(D,653,665)],
        lambda t: 'ExportDataGridToExcel(saveDialog.FileName);' in t[0] and 'تم التصدير بنجاح' in t[0] and 'Process.Start' in t[0] and 'يرجى تثبيت مكتبة' in t[1] and 'SaveAs(' not in t[1],
        'A selected output path is not a written file; no actual filesystem export or shell was executed by this witness.')
    literal('Main Excel writes a workbook inside using and disposes before Process.Start','H7B11-03',
        [(P,452,503)],
        lambda t: 'Filter = "Excel Files|*.xlsx"' in t[0] and 'using (XLWorkbook workbook = new XLWorkbook())' in t[0] and 'workbook.Worksheets.Add(dt' in t[0] and 'workbook.SaveAs' in t[0] and t[0].index('workbook.SaveAs') < t[0].index('Process.Start'),
        'Typed ClosedXML/XLSX is not CSV, and finalization precedes launch. Library/consumer formula behavior is not certified or imported.')
    literal('Journal local EntryID invoice route drops branch; EntryOper selected route keeps it','P7-061',
        [(J,550,574),(IO,1547,1551),(EO,1023,1057),(RS,1012,1017)],
        lambda t: "EntryID=N'{txtNo.Text.Trim()}'" in t[0] and 'branch=' not in t[0] and '"@EntryID", SqlDbType.Int' in t[1] and '"@branch", SqlDbType.Int' in t[1] and 'AND branch={branch}' in t[2] and '[InvGlobalID] ASC' in t[3],
        'Ambiguous candidates require matching local IDs across branches; this is not an observed deployed collision. Global entry lookup alone does not repair an unqualified invoice query.')
    literal('Account row actions pass the global entry key and new-entry child reads that key','P7-061;H7B11-04',
        [(D,784,792),(P,873,891),(EO,1165,1178),(F+'FrmNewEntry.xaml.cs',168,203),(F+'FrmNewEntry.xaml.cs',257,278)],
        lambda t: 'EntryOper.ShowEntrySource(btn.Tag.ToString())' in t[0] and 'EntryOper.ShowEntrySource(genralNo)' in t[1] and 'GlobalId=N\'' in t[2] and 'dr["GlobalID"]' in t[3] and 'ReadData(cmd.ExecuteReader())' in t[4],
        'Selected typed/global routes are positive counterevidence, not a whole-child/global authorization certificate; salary accrual route remains its prior independent handoff.')
    literal('Main branch query and permission trim differ; SP name join uses BranchId not picker id','P2-010;H7B11-01',
        [(P,107,158),(C+'User.cs',108,114),(RS,242,276),(RS,4721,4735)],
        lambda t: '!string.IsNullOrEmpty(Accounting.BranchCondition)' in t[0] and 'Accounting.BranchCondition.Trim() != ""' in t[0] and 'Accounting.BranchCondition = " "' in t[1] and '[id] [int] IDENTITY' in t[2] and 'BranchId int null' in t[2] and 'e.branch = b.BranchId' in t[3],
        'With whitespace permission the branch picker can be restricted while all remains available; this is not itself proof of unauthorized access. Key mapping/deployed uniqueness is unresolved.')
    literal('Print DTOs read live identity/date fields; journal DateEdit is not read-only','P7-045',
        [(D,433,468),(P,660,705),(J,630,663),(JX,229,233)],
        lambda t: 'AccountName = cmbAccounts.Text' in t[0] and 'FromDate = txtDateFrom.SelectedDate' in t[0] and 'AccountCode = cmbAccounts.SelectedValue' in t[1] and 'FromDate = txtDateFrom.SelectedDate' in t[1] and 'RestDate     = dateStr' in t[2] and 'IsReadOnly' not in t[3],
        'Criteria/source labels and rows need one snapshot. P7-115 is a different within-new-request DB-source change; external printed appearance is not certified.')
    literal('Previous balance catches return zero; empty parent returns before CalculateTotals','P7-046',
        [(D,274,280),(P,306,323),(P,741,752)],
        lambda t: 'return 0;' in t[0] and t[1].index('Rows.Count == 0') < t[1].index('CalculateTotals(accountStatement)') and 'return;' in t[1] and 'return dataSet;' in t[2],
        'Failure-as-zero, empty rows with old totals and empty dataset after catch are distinct failure-state contracts, not successful ERP acceptance.')
    literal('All three print paths actually load REPX; header/footer loading ignores the read flags','P1-004;H7B11-03',
        [(D,501,610),(P,505,608),(J,666,733),(D,130,165),(P,153,196),(J,127,154)],
        lambda t: all('XtraReport.FromFile' in x and 'ShowPreviewDialog' in x and '.Print()' in x for x in t[:3]) and '_printHeader' not in t[0] and '_printHeader' not in t[1] and '_printHeader' not in t[2] and all('_printHeader' in x for x in t[3:]),
        'Renderer calls exist unlike a stub; templates/settings/copy count/flags/preview-printer contract remain external or unresolved, not globally absent.')
    literal('Home caches the journal viewer closed by its handler; account callers create fresh windows','P1-030',
        [(HM,85,87),(HM,2582,2615),(J,488,492),(J,72,75),(JX,695,702)],
        lambda t: '_frmRptEntries ??' in t[0] and 'new frmAccountBalance()' in t[1] and 'new frmAccountsStatement()' in t[1] and 'this.Close()' in t[2] and '_conn?.Close()' in t[3] and 'Click="btnClose_Click"' in t[4],
        'Static/Close is a historical lifecycle root, not an actual leak measurement or proof a disabled Home entry is usable in a deployment.')
    literal('Apply-before-Show and disabled accounting menu are counterevidence to blanket ACL absence','P1-013;H7B11-04',
        [(HM,2582,2615),(HX,329,340),(MC,418,455)],
        lambda t: 'ApplyPermissionToForm(frmRptEntries)' in t[0] and 'ApplyPermissionToForm(frm)' in t[0] and 'stripAccountStatement_Click' in t[0] and 'IsEnabled="False"' in t[1] and 'name == "btnPrint"' in t[2],
        'Local visual-tree Apply and menu state are not trusted command/server authorization or proof of deployed entry availability; historical potential is not upgraded.')
    assert len(ILL)==20 and len(ST)==20
    out=dict(phase='7B11-partial-static-audit',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,
        sql_or_external_service_tests_executed=0,default_aggregate_gate_not_assumed_resolved=True,
        supplied_sql_not_certified_deployed=True,
        additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,
            local_cost=10,reference_cost=120,archive_rewritten=False),
        illustration_count=len(ILL),static_lexical_contract_check_count=len(ST),
        illustrations=ILL,static_lexical_contract_checks=ST,
        bounded_source_reads_not_semantic_coverage=[READS[k] for k in sorted(READS)],errors=[])
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
