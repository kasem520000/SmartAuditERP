#!/usr/bin/env python3
"""Independent documentary illustrations + bounded literal observations for B4.

Stdlib only. Does NOT import/execute SmartAuditERP, C#, SQL, WPF, third-party
assemblies, formulas, Office/COM or providers. Numbers are hand-selected
fixtures, not ERP outputs or proof of policy/schema/deployment correctness.
Reads explicit text spans only for lexical observations, never invokes them.
Prints deterministic JSON; does not write files or update a baseline.
"""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal,ROUND_HALF_EVEN,ROUND_FLOOR
import hashlib,json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/'
AN=F+'frmRptInvAnalysis.xaml.cs';AX=F+'frmRptInvAnalysis.xaml'
PR=F+'frmRptItemsProfitDetails.xaml.cs';PX=F+'frmRptItemsProfitDetails.xaml'
NO=F+'frmRptInvNotfic.xaml.cs';PU=F+'frmRptInvPurchaseDetails.xaml.cs'
IO='SmartAuditERP/Class/InvoiceOper.cs';IT='SmartAuditERP/Class/ItemOper.cs';CO='SmartAuditERP/Class/Common.cs';RP='SmartAuditERP/Class/Report.cs';RS='SmartAuditERP/Properties/Resources.resx'
D=Decimal
ILL=[];ST=[];READS={}
LIMIT='Independent manual illustration only; not a translation/execution of C#/SQL, policy choice, financial/ACL certification or deployed result. Analysis thread/disabled-entry/build/schema gates precede any downstream ERP acceptance.'
TEXT_LIMIT='Bounded literal/structural text observation only, not a C# call graph, SQL evaluation, WPF rendering or proof of semantic coverage. No application code executed.'
def evidence(*pairs):return ';'.join(f'{p}:{a}-{b}' for p,a,b in pairs)
def illustration(title,findings,inputs,observed,reference,expected_difference,refs):
 assert (observed!=reference) is expected_difference
 ILL.append(dict(id=f'ALG7B4-{len(ILL)+1:02d}',title=title,finding_ids=findings,hand_selected_inputs=inputs,manual_observation_model=observed,independent_reference=reference,difference_expected=expected_difference,illustration_assertions_passed=True,evidence=refs,source_application_executed=False,limit=LIMIT))
def span(path,a,b):
 lines=(ROOT/path).read_text(encoding='utf-8-sig').splitlines();assert 1<=a<=b<=len(lines)
 text='\n'.join(lines[a-1:b]);READS[(path,a,b)]=dict(path=path,start=a,end=b,selected_text_sha256=hashlib.sha256(text.encode()).hexdigest())
 return text
def literal(title,findings,pairs,predicate,description):
 texts=[span(*p) for p in pairs];ok=bool(predicate(texts));assert ok,title
 ST.append(dict(id=f'ST7B4-{len(ST)+1:02d}',title=title,finding_ids=findings,documented_observation=description,documented_text_observation_matches=ok,evidence=evidence(*pairs),source_application_executed=False,limit=TEXT_LIMIT))

def main():
 # These miniature models are authored independently. No parsing/transpiling SQL.
 q=D('0.4');value=D('4');den=q.quantize(D('1'),rounding=ROUND_HALF_EVEN);assert den==0
 illustration('Fractional positive quantity collapses to fallback','P7-077',dict(quantity='0.4',value='4',fallback='99',unit_equality=1),dict(rounded_denominator='0',selected_unit_cost='99'),dict(denominator='0.4',selected_unit_cost=str(value/q)),True,evidence((AN,493,610)))
 q=D('0.6');value=D('6');den=q.quantize(D('1'),rounding=ROUND_HALF_EVEN);assert den==1
 illustration('Rounding quantity changes average even without zero','P7-077',dict(quantity='0.6',value='6'),dict(unit_cost=str(value/den)),dict(unit_cost=str(value/q)),True,evidence((AN,493,610)))
 qty=[D(1),D(3)];cost=[D(10),D(20)];weighted=sum(q*c for q,c in zip(qty,cost));last=sum(qty)*cost[-1];assert (weighted,last)==(70,80)
 illustration('Last cost is applied to all quantities','P7-078',dict(quantities=['1','3'],costs=['10','20']),dict(total_cost=str(last)),dict(total_cost=str(weighted)),True,evidence((AN,826,860)))
 reverse=sum(qty)*cost[0];assert reverse==40
 illustration('Reordering changes a last-cost fold','P7-078',dict(first_order_cost='80',reversed_pairs=[['3','20'],['1','10']]),dict(reversed_total=str(reverse)),dict(reversed_total=str(weighted)),True,evidence((AN,826,860)))
 rows=[(datetime(2026,1,5),100),(datetime(2026,1,15),200),(datetime(2026,1,25),300)]
 wanted=sum(v for t,v in rows if datetime(2026,1,10)<=t<datetime(2026,1,21));month=sum(v for t,v in rows if datetime(2026,1,1)<=t<=datetime(2026,1,31));assert (wanted,month)==(200,600)
 illustration('Month bucket is not clipped to requested middle days','P7-079',dict(request='2026-01-10 through 2026-01-20',day_values=[[5,100],[15,200],[25,300]]),dict(amount=month),dict(amount=wanted),True,evidence((AN,1285,1373)))
 rows2=[(datetime(2026,1,5),100),(datetime(2026,1,25),200),(datetime(2026,2,5),300),(datetime(2026,2,20),400)]
 ref=sum(v for t,v in rows2 if datetime(2026,1,20)<=t<datetime(2026,2,11));expanded=sum(v for _,v in rows2);assert (ref,expanded)==(500,1000)
 illustration('Two selected months still need request intersection','P7-079',dict(request='2026-01-20 through 2026-02-10',rows=[[t.isoformat(),v] for t,v in rows2]),dict(amount=expanded),dict(amount=ref),True,evidence((AN,1285,1373)))
 illustration('Ignored employee criterion keeps both users','P7-080',dict(employee_amounts={'11':100,'22':200},selected_employee=11,dimension='Item'),dict(amount=300),dict(amount=100),True,evidence((AN,765,808),(AN,1154,1198)))
 illustration('Group dimension enumerates both despite selected group','P7-080',dict(group_amounts={'A':100,'B':200},selected_group='A'),dict(rows=['A','B'],amount=300),dict(rows=['A'],amount=100),True,evidence((AN,637,679)))
 illustration('Warehouse value is not a treasury ID','P7-081',dict(warehouse_id=3,treasury_id=7,warehouse_treasury_rows=[[3,3,100],[3,7,200]]),dict(stock_filter=3,amount=100),dict(stock_filter=7,amount=200),True,evidence((AN,1583,1600),(IO,1533,1534)))
 illustration('Header revenue with filtered-line cost mixes grain','P7-082',dict(category_A=dict(amount=100,cost=60),category_B=dict(amount=300,cost=180),selected='A'),dict(amount=400,cost=60,profit=340),dict(amount=100,cost=60,profit=40),True,evidence((AN,923,995)))
 illustration('MIN deduplicates a head but does not allocate it','P7-082',dict(joined_header_values=[400,400],selected_line_amount=100),dict(min_per_global_id=400),dict(selected_line_amount=100),True,evidence((AN,950,973)))
 illustration('Gross minus cost is not discounted profit','P7-083',dict(gross=100,line_discount=10,header_discount=0,tax=0,reference_cost=60),dict(net=100,discount=0,profit=40),dict(net=90,discount=10,profit=30),True,evidence((AN,691,755),(AN,817,880)))
 movements=[dict(inv_type=2,hproc=1,sproc=2,amount=100),dict(inv_type=3,hproc=1,sproc=2,amount=200),dict(inv_type=2,hproc=2,sproc=1,amount=20)]
 selected=sum(x['amount'] for x in movements if x['hproc']==1 and ((x['inv_type']==2 and x['sproc']==2) or (x['inv_type']==3 and x['sproc']==3)))
 reference=sum(x['amount']*(1 if x['hproc']==1 else -1) for x in movements);assert(selected,reference)==(100,280)
 illustration('Hand-selected type predicates drop normal POS and returns','P7-084',dict(movements=movements),dict(stock_amount=selected,other_h1_s2_amount=300),dict(net_amount=reference),True,evidence((AN,1599,1683),(RS,3028,3064)))
 illustration('Stock quantity and amount eligibility can differ','P7-084',dict(sale_qty=1,sale_amount=100,pos_qty=3,pos_amount=200,base_cost=10),dict(amount=100,quantity=4,cost=40),dict(amount=300,quantity=4,cost=40),True,evidence((AN,1599,1683)))
 illustration('Editable caption is not a resolved identity','P7-085',dict(initial_resolved_id=11,initial_caption='A',edited_caption='B',B_id=22,enter_pressed=False),dict(query_item_id=11,caption='B'),dict(required_state='reject-or-resolve-B-before-query',query_item_id_if_resolved=22,caption='B'),True,evidence((PR,193,210),(PR,546,558),(PR,837,852)))
 def notice(tax,extra):
  tax=D(tax);extra=D(extra);vat=tax-extra if tax-extra>0 else tax;total=tax
  if vat<=0:vat=tax;total=vat+extra
  return dict(VAT=str(vat),ExtraVAT=str(extra),TotalTax=str(total))
 assert notice('20','5')==dict(VAT='15',ExtraVAT='5',TotalTax='20')
 illustration('Separate writer taxes versus aggregate reader assumption','P7-086',dict(stored_ordinary_VAT='20',stored_additional='5'),notice('20','5'),dict(VAT='20',ExtraVAT='5',TotalTax='25'),True,evidence((NO,438,455),(IO,1546,1546),(IO,1560,1560),(IT,1635,1641)))
 illustration('Equal components expose nonadditive tax columns','P7-086',dict(stored_ordinary_VAT='5',stored_additional='5'),notice('5','5'),dict(VAT='5',ExtraVAT='5',TotalTax='10'),True,evidence((NO,438,455)))
 safes={3:'warehouse-A'};stocks={3:'treasury-B'}
 illustration('Numeric overlap is not entity equality','P7-087',dict(Inv_safe=3,Safes=safes,Stocks=stocks),dict(InvertoryName=stocks.get(3)),dict(InvertoryName=safes.get(3)),True,evidence((PU,705,723),(CO,133,151),(IO,1533,1534)))
 illustration('All checkbox leaves prior selected branch in criteria','P7-088',dict(branch_amounts={'A':100,'B':200},selected='A',all_checked=True,authorized=['A','B']),dict(query_branch='A',amount=100),dict(query_branch='authorized-A-and-B',amount=300),True,evidence((PU,342,350),(PU,1125,1129)))
 illustration('Two default Grid.Column assignments share a cell','P7-089',dict(manually_transcribed_columns={'from':None,'to':None},wpf_default_column=0),dict(from_column=0,to_column=0,distinct_cells=False),dict(required_distinct_cells=True,no_render_claim=True),True,evidence((AX,299,335)))
 amount=D(10)*D(50);qty=D(10);wrong=amount/qty;right=D(50)/qty;assert(wrong,right)==(50,5)
 illustration('Base quantity times pack price distorts cost basis','P7-041',dict(base_qty='10',sales_unit_qty='1',sales_unit_price='50'),dict(value=str(amount),base_unit_cost=str(wrong)),dict(value='50',base_unit_cost=str(right)),True,evidence((AN,500,509),(IO,1593,1597),(IT,1394,1404)))
 # Predicate illustration isolates selection, not the financial correctness of a cost policy.
 candidates=[dict(kind='purchase',inv_type=1,hproc=1,sproc=1),dict(kind='nonpurchase-input',inv_type=9,hproc=1,sproc=1),dict(kind='purchase-return',inv_type=1,hproc=2,sproc=2)]
 actual=[x['kind'] for x in candidates if (x['hproc']==1 and x['sproc']==1) or x['hproc']==3]
 illustration('Unrestricted incoming selection and proc3 return selector','P4-007',dict(candidates=candidates,assumed_reference_policy='purchase-and-purchase-return-only-not-policy-certification'),dict(eligible=actual),dict(eligible=['purchase','purchase-return']),True,evidence((AN,500,525),(RS,3044,3050)))
 illustration('Detailed report local counterexample: single discount and signed summary','P7-085;P4-007',dict(gross=100,discount=10,cost=60,sale_measure=100,return_measure=20),dict(line_profit=100-10-60,signed_summary=100-20),dict(line_profit=30,signed_summary=80),False,evidence((PR,285,343),(PR,384,397)))

 literal('Integer-rounded quantity denominator','P7-077',[(AN,493,610)],lambda t:t[0].count('int totalQty = 0;')==2 and t[0].count('totalQty += (int)Math.Round(q);')==4,'Two helpers declare an integer denominator and four additions round aggregated quantities before division.')
 literal('Item last cost fold and absent ordering in selected query','P7-078',[(AN,826,860)],lambda t:'lastUnitCost = CalcUnitCost' in t[0] and 'totalQtyForCost * lastUnitCost' in t[0] and 'order by' not in t[0].lower(),'Selected item/date query and fold use a replaced lastUnitCost, not an accumulated quantity-cost product.')
 literal('Month bucket parameters are rebuilt','P7-079',[(AN,1285,1373)],lambda t:'DateTime monthStart' in t[0] and 'DateTime monthEnd = new DateTime' in t[0] and t[0].count('Value = monthStart;')>=2 and 'Math.Max' not in t[0],'Month parameters are assigned from monthStart/monthEnd in the bounded selected text; lexical observation only.')
 pairs=[(AN,a,b) for a,b in [(637,679),(765,808),(898,938),(1026,1068),(1285,1327),(1424,1466),(1559,1600)]]+[(AN,1154,1198)]
 literal('Employee filter absent in seven selected filter-build spans','P7-080',pairs,lambda t:all('sales_emp=' not in s for s in t[:-1]) and 'sales_emp=' in t[-1] and 'chkAllGroups' not in t[0],'Seven bounded builder spans have no employee clause; Emp has one. Group builder does not consult its own group checkbox.')
 literal('Wrong treasury operand in stock mode','P7-081',[(AN,1583,1600)],lambda t:'safeVal = GetSelectedValue(cmbSafe)' in t[0] and '[stock]={stockSelVal}' in t[0],'safeVal is loaded but the treasury predicate interpolates stockSelVal in the selected block.')
 literal('Filtered headers and filtered detail costs have different grain','P7-082',[(AN,923,995)],lambda t:'ItemsCategory.id={groupVal}' in t[0] and 'min(tot_net)' in t[0] and 'group by inv.InvGlobalID' in t[0] and 'group by inv_sub.ItemId,inv.date' in t[0],'Header MIN-per-GlobalID and line/date quantity projection occur under the same category filter.')
 literal('Gross line sums and zero discount in Group/Item','P7-083',[(AN,691,755),(AN,817,880)],lambda t:all('sum(val1*exchange_price)' in s and ('netDiscount = 0' in s) for s in t),'Both selected branches take raw line price sums and set discount zero.')
 literal('Stock-mode POS proc3 versus supplied ordinary POS type','P7-084',[(AN,1599,1683),(RS,3036,3038),(IO,1613,1621)],lambda t:'inv.inv_type=3' in t[0] and 'inv_sub.proc_type=3' in t[0] and "(5, 3, 1," in t[1] and 'InvertoryImpact == 2' in t[2],'Selected stock predicates require POS direction3, unlike ordinary outgoing direction2 in supplied type/writer contracts.')
 literal('Item identity resolution is event-specific','P7-085',[(PR,193,210),(PR,546,558),(PX,292,313),(PR,665,684)],lambda t:'Inv_Sub.ItemId={SelectedId}' in t[0] and 'Key.Return' in t[1] and 'KeyDown=' in t[2] and 'TextChanged=' not in t[2] and 'SelectedId' not in t[3],'Display uses SelectedId and a nonempty name guard; the selected editable controls resolve on Enter and show no TextChanged identity invalidation.')
 literal('Reader aggregate tax assumption versus separate writer fields','P7-086',[(NO,438,455),(IO,1546,1546),(IO,1560,1560),(IT,1635,1641)],lambda t:'taxTotal - extraVAT' in t[0] and 'inv.TotalTax     = taxTotal' in t[0] and 'inv.VAT' in t[1] and 'inv.ExtraVAT' in t[2] and 'invo.Total + invo.VAT + invo.ExtraVAT' in t[3],'Reader subtracts additional tax from taxTotal, while writer and calculator keep ordinary/additional taxes separate.')
 literal('Optimized store lookup joins Stocks not Safes','P7-087',[(PU,705,723),(CO,133,151)],lambda t:'left join Stocks    on inv.safe' in t[0] and 'Select Safes.name from Safes' in t[1],'Optimized name source differs from the local GetStoreName entity.')
 literal('Branch-all handler leaves selected ID and collector ignores checkbox','P7-088',[(PU,342,350),(PU,1125,1129)],lambda t:'SelectedIndex > -1' in t[0] and 'chkAllBranches' not in t[0] and 'IsEnabled' in t[1] and 'SelectedIndex' not in t[1],'Collector tests selected index only; bounded all-handler only enables/disables the combo.')
 literal('Both date pickers have no Grid.Column in their local attributes','P7-089',[(AX,299,335)],lambda t:len(re.findall(r'<DatePicker\b[^>]*x:Name="txtDate(?:From|To)"[^>]*/>',t[0],re.S))==2 and all('Grid.Column' not in x for x in re.findall(r'<DatePicker\b[^>]*/>',t[0],re.S)),'The two DatePicker tags share the same parent and default column; no WPF renderer executed.')
 literal('Search TextBoxes interpolated in SQL literal','P1-011',[(PR,575,628)],lambda t:"name=N'{txtItemName.Text}'" in t[0] and "Code=N'{txtItemCode.Text}'" in t[0] and '.Parameters.Add' not in t[0],'The selected search methods interpolate raw text inside SQL literals; no attack string or database executed.')
 literal('Thread start precedes direct WPF validation reads','P7-054',[(AN,258,280)],lambda t:'new Thread(ShowResult)' in t[0] and 'chkAllStock.IsChecked' in t[0] and t[0].index('chkAllStock.IsChecked')<t[0].index('Dispatcher.Invoke'),'First direct WPF access is before the dispatcher callback in the selected ShowResult entry.')
 literal('Notification print passes null; two local overloads exist','P7-055',[(NO,790,809),(RP,380,406),(RP,531,553)],lambda t:'report.BindToData(' in t[0] and 'null,' in t[0] and 'GridView GridView1' in t[1] and 'DataTable dt,' in t[2],'No invoice list is passed; overload/build ambiguity is a separate earlier gate, not proof a blank page was rendered.')
 literal('Report metadata reads current controls with existing row loop','P7-045',[(PR,821,856),(PU,795,815)],lambda t:'ProfitList.Select' in t[0] and 'txtDateFrom.DateTime' in t[0] and 'txtItemName.Text' in t[0] and 'txtFromDate.EditValue' in t[1],'Current control metadata accompanies previously loaded collections, without a frozen request object in these bounded bridges.')
 literal('Local counterevidence: UI capture and signed detail summary','P7-054;P7-085',[(PU,430,482),(PR,285,343),(PR,384,397)],lambda t:t[0].index('CollectQueryParams()')<t[0].index('Task.Run(') and 'DgvAvgCost' in t[1] and 'DgvTotAvg' in t[1] and 'sales.Sum(s) - returns.Sum(s)' in t[2],'Purchase captures criteria before worker; detailed profits separates unit/total costs and subtracts returns locally. This does not certify the rest.')
 assert len(ILL)==23 and len(ST)==18
 result=dict(phase='7B4-partial-static-audit',purpose='Documentary manual illustrations and bounded text observations only; not ERP acceptance',application_code_imported_or_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,illustration_count=len(ILL),static_lexical_contract_check_count=len(ST),illustrations=ILL,static_lexical_contract_checks=ST,bounded_source_reads_not_semantic_coverage=[READS[k] for k in sorted(READS)])
 print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
