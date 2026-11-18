#!/usr/bin/env python3
"""B12 deterministic manual contrasts and bounded inert-source observations.

No ERP import/build/translation, SQL/WPF/REPX/Office, exports or shell. These
hand-selected models do not execute the financial implementation. P3-022 stays
in its own prior statement parent; stock-child P4-030 is not assumed fixed.
Supplied procedures/DDL are not certified deployed. No formula/HTML interpreter.
"""
from __future__ import annotations
import hashlib
import html
import json
from datetime import datetime
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/';C='SmartAuditERP/Class/'
N=F+'IncomeStatementForm.xaml.cs';NX=F+'IncomeStatementForm.xaml'
O=F+'frmRptIncomeStatement.xaml.cs';OX=F+'frmRptIncomeStatement.xaml'
B=F+'frmMezanyaArba7.xaml.cs';BX=F+'frmMezanyaArba7.xaml'
S=F+'frmSafeGrd.xaml.cs';SX=F+'frmSafeGrd.xaml'
RS='SmartAuditERP/Properties/Resources.resx';HM='SmartAuditERP/Home.xaml.cs';HX='SmartAuditERP/Home.xaml'
IC=C+'Inventory.cs';MC=C+'MainClass.cs';DTO=C+'RestrictionData.cs';NR='SmartAuditERP/Class_WPF/IncomeStatementRow.cs'
ILL=[];ST=[];READS={}
LIMIT=('Independent hand-selected documentary contrast, not execution/translation of financial C#/SQL or WPF/REPX/Office, '
       'financial/policy/deployed-schema/ACL acceptance or remediation. Stock-child P4-030 is NOT assumed fixed; a valid '
       'approved-zero model isolates the sentinel cause, not certify an empty child as valid. Prior statement aggregate '
       'P3-022 remains in its own parent. Supplied SQL is not certified deployed. No real data/secrets, actual exports, '
       'formula/HTML interpreter, printer or shell. No measured index/leak/latency.')
TEXT_LIMIT=('Bounded literal/structural observation of inert text only, not semantic callgraph/deployed schema or role/availability '
            'proof, WPF rendering, whole-child review, financial acceptance, operational measurement or application execution.')
def ev(*pairs):return ';'.join(f'{p}:{a}-{b}' for p,a,b in pairs)
def illustration(title,roots,inputs,local,reference,difference,refs):
    assert (local!=reference) is difference,title
    ILL.append(dict(id=f'ALG7B12-{len(ILL)+1:02d}',title=title,finding_ids=roots,hand_selected_inputs=inputs,
        manual_observation_model=local,independent_reference=reference,difference_expected=difference,
        illustration_assertions_passed=True,evidence=refs,source_application_executed=False,limit=LIMIT))
def span(p,a,b):
    raw=(ROOT/p).read_bytes()
    try:text=raw.decode('utf-8-sig')
    except UnicodeDecodeError:text=raw.decode('cp1256',errors='replace')
    lines=text.splitlines();assert 1<=a<=b<=len(lines);text='\n'.join(lines[a-1:b])
    READS[(p,a,b)]=dict(path=p,start=a,end=b,selected_text_sha256=hashlib.sha256(text.encode()).hexdigest());return text

def literal(title,roots,pairs,predicate,description):
    texts=[span(*p) for p in pairs];ok=bool(predicate(texts));assert ok,title
    ST.append(dict(id=f'ST7B12-{len(ST)+1:02d}',title=title,finding_ids=roots,documented_observation=description,
        documented_text_observation_matches=ok,evidence=ev(*pairs),source_application_executed=False,limit=TEXT_LIMIT))


def main():
    chosen='report.xlsx';effective=chosen.replace('.xlsx','.csv')
    illustration('CSV writer changes effective path while caller reports and opens the XLSX choice','P7-116',
        dict(chosen_path=chosen,write_succeeds_assumed=True,actual_filesystem=False),
        dict(written=effective,displayed=chosen,opened=chosen),dict(written=effective,displayed=effective,opened=effective),True,
        ev((N,707,765),(NX,654,660)))
    illustration('An existing chosen XLSX can remain the old candidate despite a successful new CSV write','P7-116',
        dict(chosen_file_preexists_assumed=True,chosen_generation='OLD',effective_generation='NEW',actual_shell=False),
        dict(opened_path=chosen,opened_generation='OLD'),dict(opened_path=effective,opened_generation='NEW'),True,ev((N,726,740),(N,748,765)))
    approved_zero=0;auto=50
    illustration('Approved zero is replaced by auto stock because numeric zero doubles as unset','P7-117',
        dict(approved=True,valid_zero_assumed=True,stock=approved_zero,auto_value=auto,child_schema_gate_isolated_not_fixed=True),
        dict(stock=approved_zero if approved_zero!=0 else auto),dict(stock=0),True,ev((B,317,319),(B,417,433),(S,752,757)))
    illustration('A nonzero override works and a cancelled new child does not replace it','P7-117',
        dict(prior_approved_value=20,child_approved=False,child_default_value=0,auto_value=50),
        dict(stock=20,source='prior-approved'),dict(stock=20,source='prior-approved'),False,
        ev((B,317,319),(B,417,433),(S,42,59)))
    sale,ret,disc=100,20,5;abs_revenue=sale+ret+disc;net_row=abs_revenue-ret-disc
    illustration('ABS returns/discounts plus a synthetic net-sales row inflate the revenue card','P3-020',
        dict(sale_credit=sale,return_debit=ret,discount_debit=disc,other_metrics_isolated=True),
        dict(net_sales_row=net_row,revenue_card=abs_revenue+net_row),dict(net_sales_row=sale-ret-disc,revenue_card=sale-ret-disc),True,
        ev((N,295,316),(N,408,464),(N,597,605)))
    illustration('Legitimate zero COGS triggers fallback that sums detail and summary layers','P3-020',
        dict(opening=0,purchases=30,available=30,closing_stock=30,cogs=0,raw_closing_GL_rows_absent=True),
        dict(cogs_card=30+30+30+0),dict(cogs_card=0),True,ev((N,329,369),(N,606,618)))
    illustration('Expense and other-revenue prefixes can make cards disagree with the final net row','P3-020',
        dict(revenue_isolated_and_aligned=100,cogs=0,expense31=10,expense33=20,other_revenue42=5,duplicate_revenue_gate_isolated=True),
        dict(expense_card=10,net_card=100-10),dict(expense_card=30,net_card=100-30+5),True,
        ev((N,377,399),(N,492,497),(N,622,631)))
    illustration('All-branch GL can be paired with only the current branch stock value','P7-065',
        dict(all_branches=True,current_branch=1,stock_by_branch={'1':50,'2':70},branch_mapping_aligned_assumed=True),
        dict(GL_branch_set=[1,2],stock_value=50),dict(GL_branch_set=[1,2],stock_value=50+70),True,
        ev((N,187,195),(N,672,689),(O,220,236),(O,371,406),(B,196,207),(B,317,319)))
    illustration('Opening-stock fallback lacks the selected branch and period predicates','P7-065;H7B12-02',
        dict(selected_branch=1,GL_opening=0,opening_invoices=[dict(branch=1,value=10),dict(branch=2,value=20)],all_eligible_non_deleted_assumed=True),
        dict(opening=10+20),dict(opening=10),True,ev((N,318,327),(N,649,670)))
    illustration('Period-only balance-sheet GL does not reconstruct nonzero opening balances','P3-019',
        dict(opening_asset=100,opening_liability=100,movement=0,stock=0,closing_policy_assumed=True),
        dict(asset=0,liability=0),dict(asset=100,liability=100),True,ev((B,193,230),(B,334,395)))
    t=datetime(2026,1,1,23,59,30);end=datetime(2026,1,1,23,59);tomorrow=datetime(2026,1,2)
    illustration('Inclusive23:59 still excludes the final30seconds of a whole-day policy','P3-023',
        dict(row=t.isoformat(),entered_end=end.isoformat(),policy='whole-day'),
        dict(included=t<=end),dict(included=t<tomorrow),True,
        ev((N,178,185),(N,413,415),(O,176,189),(O,216,218),(B,193,203)))
    illustration('Supplied valuation ignores its date while an independent as-of membership excludes later movement','P4-008',
        dict(before_value=50,later_change=20,report_date_precedes_later=True,supplied_not_deployed=True),
        dict(valuation=50+20),dict(valuation=50),True,ev((IC,462,472),(RS,48166,48209)))
    illustration('Failed valuation returning zero can masquerade as a higher profit','P7-046',
        dict(revenue=100,cost_before_closing=60,valuation_failed=True,no_SQL_fault_injection=True),
        dict(profit=100-60+0,health='not-labelled'),dict(profit=None,health='failed-stock-source'),True,
        ev((IC,504,530),(N,672,691),(O,332,364)))
    illustration('Clearing rows and cards before a failed GL query counters an always-stale-result claim','P7-046',
        dict(previous_rows=['OLD'],next_GL_result=None,stock_failure_case_separate=True),
        dict(published_rows=[],card_value=0),dict(published_rows=[],card_value=0),False,
        ev((N,170,207),(N,588,595),(B,183,194)))
    illustration('Live print dates can label rows loaded for an earlier period','P7-045',
        dict(loaded_period='A',controls_now='B',reload=False,actual_template_not_loaded=True),
        dict(rows='A',DTO_period='B'),dict(rows='A',DTO_period='A'),True,ev((N,833,860),(O,500,530)))
    illustration('N2 thousands and embedded quotes need real CSV field encoding','P7-048',
        dict(formatted_amount='1,234.50',account_name='A,"B"',actual_export=False,current_UI_culture_does_not_fix_numeric_culture=True),
        dict(encoded_line='A,"B",1,234.50',amount_field_count=2),
        dict(encoded_line='"A,""B""","1,234.50"',amount_field_count=1),True,ev((N,748,765),(O,472,497),(HM,337,341)))
    illustration('CSV quoting alone does not establish a text-only spreadsheet-cell policy','P7-049',
        dict(untrusted_prefix='=',only_inert_prefix_no_formula=True,consumer_behavior_not_executed=True),
        dict(text_cell_policy_declared=False),dict(text_cell_policy_declared=True),True,ev((N,748,765),(O,472,497)))
    illustration('Balance-sheet export writes HTML for either XLS or CSV labels at the same chosen path','P7-050',
        dict(chosen_paths=['report.xls','report.csv'],actual_IO=False),
        dict(effective_kinds=['HTML','HTML']),dict(effective_kinds=['XLS','CSV']),True,ev((B,441,490)))
    name='A&B<value>'
    illustration('Raw HTML cell interpolation differs from escaped account text','P7-098',
        dict(account_name=name,html_interpreter_executed=False),
        dict(cell='<td>'+name+'</td>'),dict(cell='<td>'+html.escape(name)+'</td>'),True,ev((B,469,490)))
    illustration('An unused REPX existence gate blocks an otherwise local document route','P7-097',
        dict(rows_present=True,repx_exists=False,renderer='FlowDocument',actual_WPF=False),
        dict(local_document_route_allowed=False),dict(local_document_route_allowed=True),True,ev((B,493,558),(B,560,610)))
    illustration('Calculated opening stock targets absent local XAML names and is not consumed by totals','P1-033',
        dict(calculated_first_stock=20,local_xaml_names_contain_txtFirstVal=False,successful_query_assumed=True,policy_amount_not_certified=True),
        dict(bound_value=None,total_consumer_exists=False),dict(bound_value=20,total_consumer_exists=True),True,
        ev((O,332,340),(O,395,441),(O,604,609),(OX,1,511)))
    debit,credit=100,80;plug=debit-credit
    illustration('A balancing P&L plug makes totals equal without proving source completeness','H7B12-01;P3-019;P7-046',
        dict(raw_debit=debit,raw_credit=credit,plug=plug,eligibility_or_opening_not_established=True),
        dict(debit=debit,credit=credit+plug,source_completeness='not-established'),
        dict(debit=100,credit=100,source_completeness='not-established'),False,ev((B,354,395),(O,332,364)))

    literal('New-income writer changes path but caller reports and launches the original choice','P7-116',
        [(N,707,765),(NX,654,660)],
        lambda t:'Filter = "Excel Files|*.xlsx"' in t[0] and 'filePath.Replace(".xlsx", ".csv")' in t[0] and 'ExportToExcel(saveDialog.FileName)' in t[0] and 'ProcessStartInfo(saveDialog.FileName)' in t[0] and 'Click="btnExport_Click"' in t[1],
        'Local output-identity defect, distinct from wrong bytes at one path or an empty export stub. Actual file existence and shell behavior not observed.')
    literal('Approved child scalar is consumed only when numerically nonzero','P7-117',
        [(B,27,31),(B,317,319),(B,417,433),(S,752,757),(BX,228,232),(SX,832,838)],
        lambda t:bool(re.search(r'_Stock\s*=\s*0\.0',t[0])) and '_Stock != 0.0' in t[1] and 'if (safeGrd.ISDone)' in t[2] and '_Stock = safeGrd._stockTotal' in t[2] and 'ISDone      = true' in t[3] and '.Sum(x => x.DgvTotalCost)' in t[3] and 'Click="BtnStock_Click"' in t[4] and 'Click="BtnAprroved_Click"' in t[5],
        'has-override is not separate from zero. Valid-zero behavior is isolated; no assumption that every empty child is financially acceptable or schema-valid.')
    literal('Child starts with empty collection and false approval; approve sums while close does not approve','P7-117;H7B12-02',
        [(S,42,59),(S,641,660),(S,752,757),(B,417,433)],
        lambda t:'ISDone      = false' in t[0] and 'new ObservableCollection<InventoryGridItem>()' in t[0] and 'this.Close()' in t[1] and 'ISDone' not in t[1] and 'ISDone      = true' in t[2] and 'BtnAprroved.Visibility = Visibility.Visible' in t[3],
        'A scalar zero is representable at child approval; policy must reject invalid empty explicitly or preserve legitimate zero, not silently replace it.')
    literal('All three GL report sources have local state/deletion eligibility and bounded date parameters','H7B12-01',
        [(N,408,446),(N,470,509),(O,226,242),(B,198,229)],
        lambda t:all('IS_Deleted' in x for x in t) and all(('state' in x or '[state]' in x) for x in t) and all('@date1' in x and '@date2' in x for x in t),
        'Positive source eligibility/parameter evidence: do not copy prior parent-statement missing-state or aggregate/worker gates into these synchronous parents.')
    literal('ABS group balances feed synthetic net-sales and a card that also sums the details','P3-020',
        [(N,295,316),(N,408,464),(N,597,605)],
        lambda t:'totalRevenue - salesReturns - salesDiscounts' in t[0] and 'ABS(COALESCE(SUM(ES.dept)' in t[1] and 'StartsWith("4")' in t[2] and 'Contains("الإيرادات")' in t[2],
        'Existing sign/row-grain root; does not claim all amounts or actual deployed policy are as modeled.')
    literal('Zero COGS activates a sum of every cost-category layer','P3-020',
        [(N,329,369),(N,606,618)],
        lambda t:'"COST-AVAILABLE"' in t[0] and '"COGS"' in t[0] and 'if (cogsFromCode != 0m)' in t[1] and 'Contains("تكلفة البضاعة")' in t[1],
        'Zero is not a missing measure; synthetic detail/summary rows are not independent additive cost entries.')
    literal('Expense groups33to39 and revenue42 differ between table and cards','P3-020',
        [(N,377,399),(N,492,497),(N,622,631)],
        lambda t:'finalNetIncome = netIncomeVal + otherRevenue' in t[0] and 'BETWEEN 33 AND 39' in t[1] and 'StartsWith("31")' in t[2] and 'netIncome = grossProfit - expTotal' in t[2],
        'Same P3-020 aggregation/metric-lineage root; another card does not create another finding.')
    literal('All-branch GL and current-branch closing stock use different branch decisions','P7-065',
        [(N,187,195),(N,672,689),(O,220,236),(O,371,390),(B,196,207),(B,317,319)],
        lambda t:'int branchId = -1' in t[0] and 'chkAllBranches.IsChecked != true' in t[0] and 'int branch = MainClass.BranchNo' in t[1] and 'chkAllBranches.IsChecked != true' in t[1] and 'chkAllBranches.IsChecked != true' in t[2] and 'int branch = MainClass.BranchNo' in t[3] and 'selectedBranch = null' in t[4] and 'MainClass.BranchNo' in t[5],
        'Branch-set mismatch under an all-branches policy, not proof of unauthorized rows or semantics of every -1 parameter in deployment.')
    literal('New-income opening fallback is invoked when nonpositive GL opening and lacks branch/date predicates','P7-065;H7B12-02',
        [(N,318,327),(N,649,670)],
        lambda t:'if (openStock <= 0m)' in t[0] and 'openStock = GetOpenstock()' in t[0] and 'Is_Deleted=0' in t[1] and 'branch' not in t[1].lower() and '@date' not in t[1].lower(),
        'Deleted filter exists; branch/date alignment and definition of opening still require policy. Old-income GetOpenstock is a different, locally unused method.')
    literal('Balance-sheet GL is period-only and its P&L plug precedes balanced indication','P3-019;H7B12-01',
        [(B,193,230),(B,354,395),(BX,198,206)],
        lambda t:'Entry.date BETWEEN @date1 AND @date2' in t[0] and 'Accounts_Index.FinalAcc=1' in t[0] and 'totalCredit += pnlCredit' in t[1] and t[1].index('totalCredit += pnlCredit')<t[1].index('bool isBalanced') and 'IsChecked="True"' in t[2],
        'A selected-period branch lacks separate previous GL here. A plug is not a trial-balance validation or proof of closing-policy correctness.')
    literal('Default23:59 and inclusive BETWEEN differ from a half-open whole-day interval','P3-023',
        [(N,96,102),(N,178,185),(N,413,415),(O,176,189),(O,216,218),(B,193,203),(B,406,411)],
        lambda t:'"23:59"' in t[0] and 'TimeSpan.TryParse(txtEndTime.Text' in t[1] and 'BETWEEN @date1 AND @date2' in t[2] and 'txtEndTime.Text' in t[3] and 'BETWEEN @date1 AND @date2' in t[4] and 'new TimeSpan(23, 59, 0)' in t[5] and 'datePart.Date.Add(ts)' in t[6],
        'Whole-day and explicit-time contracts must be separated; inclusive00seconds does not include the final minute as a whole.')
    literal('Parents call InventoryCost whose supplied CREATE/ALTER declare but do not use date','P4-008',
        [(N,672,689),(O,371,390),(B,317,319),(IC,462,487),(RS,48166,48209)],
        lambda t:all('Inventory.InventoryCost(' in x and 'InventoryCostForBalanceSheet(' not in x for x in t[:3]) and 'public static double InventoryCostForBalanceSheet' in t[3] and len(re.findall(r'@date\b',t[4],re.I))==2,
        'Date is passed by C#; both selected supplied definitions only declare it. This is not deployed-procedure certification.')
    literal('Shared valuation helper catches to zero while report computes profit and balanced state','P7-046',
        [(IC,504,530),(N,672,691),(O,332,368),(B,183,194)],
        lambda t:'return 0.0' in t[0] and 'catch' in t[0] and 'return 0m' in t[1] and 'txtIsBalanced.Text = "✅ الحسابات متوازنة"' in t[2] and '_rows.Clear()' in t[3],
        'Failure-as-zero is a source-health root. Clearing rows/totals before query is counterevidence to a blanket stale-result claim, not a fix for valuation health.')
    literal('Print DTOs read current date controls but omit some new-row semantic dimensions','P7-045;P1-004;H7B12-03',
        [(N,833,860),(O,500,530),(NR,1,32),(DTO,1,172)],
        lambda t:'FromDate = txtFromDate.DateTime' in t[0] and 'ToDate = txtToDate.DateTime' in t[0] and 'ToDate      = txtToDate.DateTime' in t[1] and 'Category' in t[2] and 'Notes' in t[2] and 'Category =' not in t[0] and 'Notes =' not in t[0] and 'public string stockVal' in t[3],
        'Local data-shape and snapshot gap; external template behavior is unresolved, not a proven lost printed metric.')
    literal('CSV interpolation has no quote doubling; old CSV uses unquoted N2','P7-048',
        [(N,748,765),(O,472,497),(HM,337,341)],
        lambda t:'row.AccountName' in t[0] and '.Replace(' not in t[0].split('sw.WriteLine("المجموعة')[1] and 'row.DeptBalance:N2' in t[1] and 'CurrentUICulture' in t[2] and 'CurrentCulture =' not in t[2],
        'Quotes/thousands/current numeric culture need an actual CSV contract. UI language alone is not numeric-format evidence.')
    literal('New export writer finalizes inside using before caller success and optional shell','P7-116;P7-048;H7B12-03',
        [(N,726,765),(O,483,491)],
        lambda t:'using (StreamWriter sw = new StreamWriter' in t[0] and 'ExportToExcel(saveDialog.FileName)' in t[0] and 'Process.Start' in t[0] and 'File.WriteAllText' in t[1],
        'Positive finalization/order evidence, not an unfinished-writer finding copied from a different report; actual I/O was not performed.')
    literal('Account names and notes are written directly without a declared text-cell policy','P7-049',
        [(N,748,765),(O,472,497),(B,469,490)],
        lambda t:'row.AccountName' in t[0] and 'row.Notes' in t[0] and 'row.Name' in t[1] and 'row.Column2' in t[2] and all('Formula' not in x for x in t),
        'Potential spreadsheet-formula interpretation depends on untrusted source and consumer. Text comparison is not formula/HTML execution or an XLSX-wide claim.')
    literal('Balance-sheet XLS/CSV choices both call the same HTML writer','P7-050',
        [(B,441,490)],
        lambda t:'Excel File (*.xls)|*.xls|CSV File (*.csv)|*.csv' in t[0] and 'ExportToExcelHtml(saveDialog.FileName)' in t[0] and '<html>' in t[0] and 'File.WriteAllText(fileName' in t[0],
        'Same chosen path but mismatched format, distinct from new-income changed-path P7-116.')
    literal('HTML interpolates raw text while FlowDocument places it in Run','P7-098',
        [(B,469,490),(B,560,610),(B,626,635)],
        lambda t:'<td>{row.Column1}</td><td>{row.Column2}</td>' in t[0] and 'HtmlEncode' not in t[0] and 'new Run(Title)' in t[1] and 'new Run(text ?? "")' in t[2],
        'Raw HTML root is not automatically a FlowDocument markup parser or proof of consumer compromise.')
    literal('Balance-sheet checks but never loads REPX; the two income parents actually load REPX','P7-097;P1-004',
        [(B,493,558),(N,767,831),(O,532,603)],
        lambda t:'"rptMezanyaArba7.repx"' in t[0] and 'File.Exists(fullPath)' in t[0] and 'BuildPrintDocument()' in t[0] and 'XtraReport.FromFile' not in t[0] and all('XtraReport.FromFile' in x for x in t[1:]),
        'Renderer-specific dependency/capability contract; no claim that every template is absent from deployment.')
    literal('Old-income opening-stock targets are absent from local XAML and unused by totals','P1-033;H7B12-02',
        [(O,332,340),(O,395,441),(O,604,609),(OX,1,511)],
        lambda t:'CalcStockFirstVal()' in t[0] and 'txtFirstVal.Text' in t[1] and 'catch { }' in t[1] and 'FindName("txtFirstVal")' in t[2] and not re.search(r'x:Name="txtFirstVal1?"',t[3]) and 'txtFirstVal' not in t[0],
        'Bounded missing data-binding/consumer gap under P1-033; does not invent an approved opening-stock policy or certify every dynamic deployment namescope.')
    literal('Home uses fresh windows and Apply-before-Show with one default-enabled and two disabled entries','P1-013;P2-010;H7B12-04',
        [(HM,2669,2704),(HX,335,345),(MC,349,455),(B,417,433)],
        lambda t:all('new '+n+'()' in t[0] for n in ('frmRptIncomeStatement','IncomeStatementForm','frmMezanyaArba7')) and t[0].count('ApplyPermissionToForm(frm)')==3 and 'stripIncomeAnalysis2' in t[1] and 'IsEnabled="False"' not in next(l for l in t[1].splitlines() if 'stripIncomeAnalysis2"' in l) and 'name == "btnPreview"' in t[2] and 'name == "Button1"' not in t[2] and 'ApplyPermissionToForm' not in t[3],
        'Local visual-tree/name/child limits remain potential. Disabled menu and Apply/new are counterevidence, not deployed ACL/availability certification.')
    assert len(ILL)==22 and len(ST)==22
    out=dict(phase='7B12-partial-static-audit',application_code_imported_or_executed=False,application_remediation_performed=False,
        real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        default_aggregate_gate_not_assumed_resolved=True,supplied_sql_not_certified_deployed=True,
        stock_child_schema_not_assumed_resolved=True,manual_metric_models_not_financial_acceptance=True,
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False),
        illustration_count=len(ILL),static_lexical_contract_check_count=len(ST),illustrations=ILL,static_lexical_contract_checks=ST,
        bounded_source_reads_not_semantic_coverage=[READS[k] for k in sorted(READS)],errors=[])
    print(json.dumps(out,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
