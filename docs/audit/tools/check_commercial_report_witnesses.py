#!/usr/bin/env python3
"""Read-only, independent manually transcribed illustrations for PARTIAL7B3.

Stdlib only. Does NOT import/execute the ERP, C#, WPF, SQL, a template, DLL,
spreadsheet/formula interpreter or external service. Lexical observations are
separate from the little models: neither establishes deployed/runtime behavior.
Writes JSON to stdout only. Source slices are explicit; not semantic coverage.
"""
from __future__ import annotations
import csv
from datetime import datetime
from decimal import Decimal as D
import hashlib
import io
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/'
R='SmartAuditERP/Properties/Resources.resx'
C='SmartAuditERP/Class/'
READS={}


def read(path,start,end):
    selected='\n'.join((ROOT/path).read_text(encoding='utf-8-sig').splitlines()[start-1:end])
    READS[(path,start,end)]=dict(path=path,start=start,end=end,selected_text_sha256=hashlib.sha256(selected.encode()).hexdigest())
    return selected


def ev(path,*spans):return ';'.join(f'{path}:{x}' for span in spans for x in span.split(';'))

def compact(s):return re.sub(r'\s+','',s).lower()


def main():
    algebra=[];lexical=[]
    def alg(title,fids,evidence,actual,reference,assertion,limit='Independent manual transcription only; not C#/SQL/WPF/DTO/rendering or deployed-policy acceptance.'):
        assert assertion,title
        algebra.append(dict(id=f'ALG7B3-{len(algebra)+1:02d}',title=title,finding_ids=fids,evidence=evidence,
            manually_transcribed_observed_model=actual,independent_reference_model=reference,
            illustration_assertions_passed=True,source_application_executed=False,limit=limit))
    def st(title,fids,evidence,condition,limit='Bounded literal-source observation only, not a C#/SQL parser, call-graph, deployment or execution proof.'):
        assert condition,title
        lexical.append(dict(id=f'ST7B3-{len(lexical)+1:02d}',title=title,finding_ids=fids,evidence=evidence,
            documented_text_observation_matches=True,source_application_executed=False,limit=limit))

    both={2:D('100'),3:D('200')}
    alg('Requested type versus fixed two-type population','P7-066',ev(R,'4030-4079'),{'type2':str(sum(both.values())),'type3':str(sum(both.values()))},{str(k):str(v) for k,v in both.items()},sum(both.values())!=both[2] and sum(both.values())!=both[3])
    rows=[(D('100'),False,1),(D('50'),True,1),(D('20'),True,-1)]
    a=sum(v*s for v,d,s in rows);b=sum(v*s for v,d,s in rows if not d)
    alg('Deleted sales and deleted return still participate','P7-067',ev(R,'3974-4079'),str(a),str(b),a==130 and b==100)
    idx=0;values=[D('30'),D('70')];a=sum(values) if not idx>0 else values[idx]
    alg('First real selection is not the all sentinel','P7-068',ev(F+'frmRptSalesByCategory.xaml.cs','149-195'),str(a),str(values[idx]),a==100 and values[idx]==30)
    alg('Zero-rate item is assigned fifteen percent','P7-069',ev(F+'frmRptSalesByCategory.xaml.cs','205-230'),{'tax':'15.00','net':'115.00'},{'tax':'0','net':'100'},D('100')*D('.15')==15 and D('100')*D('1.15')==115)
    bases=[(D('100'),D('0')),(D('100'),D('.05')),(D('100'),D('.15'))]
    a=sum(v for v,t in bases)*D('.15');b=sum(v*t for v,t in bases)
    alg('Mixed historical tax rates cannot be replaced by one rate','P7-069',ev(F+'frmRptSalesByCategory.xaml.cs','205-230'),str(a),str(b),a==45 and b==20)
    qty,price,total,discount=D('10'),D('10'),D('100'),D('10')
    a=price*discount/total;b=qty*price*discount/total
    alg('Discount share must include the line amount','P7-070',ev(F+'frmRptSalesByCategory.xaml.cs','205-248')+';'+ev(R,'4393-4453'),{'share':str(a),'base':str(total-a)},{'share':str(b),'base':str(total-b)},a==1 and b==10)
    shares_one=[D('10')*D('10')/D('100')];shares_ten=[D('10')*D('10')/D('100')]*10
    alg('Splitting the same quantity changes the transcribed discount','P7-070',ev(R,'4393-4453'),{'one_line':str(sum(shares_one)),'ten_lines':str(sum(shares_ten))},{'either_shape':'10'},sum(shares_one)==1 and sum(shares_ten)==10)
    source=[{'group':'A','id':1},{'group':'A','id':2},{'group':'B','id':3}];header=[{'title':'synthetic header'}]
    alg('One header cannot carry three unspecified detail identities','P7-071',ev(F+'frmRptSalesByCategory.xaml.cs','490-524'),{'header_objects':len(header),'specified_detail_ids':[]},{'detail_ids':[x['id'] for x in source]},len(header)==1 and not any('id' in x for x in header), 'Manual projection shape only. External ToDataTable/InventoryData/REPX behavior is not executed or guessed.')
    columns={'ItemId','ProductId','val','val1','exchange_price','proc_type'}
    alg('Production reader and supplied column contract disagree','P7-072',ev(F+'frmRptProducedItems.xaml.cs','168-228')+';'+ev(R,'1023-1060'),{'requested':'ComponentId','contract_contains_it':'ComponentId' in columns},{'component_column':'ItemId','parent_column':'ProductId'},'ComponentId' not in columns and 'ItemId' in columns)
    cond='';rent=[('A',D('100')),('B',D('200'))];a=sum(v for d,v in rent);b=sum(v for d,v in rent if d=='A')
    alg('Empty Cond leaves both rental periods in the source','P7-073',ev(F+'frmRptRentInvoices.xaml.cs','161-209;585-591'),{'cond':cond,'amount':str(a)},{'selected_period':'A','amount':str(b)},not cond and a==300 and b==100)
    name="O'Neil";raw="cust LIKE '%"+name+"%'";escaped="cust LIKE '%"+name.replace("'","''")+"%'"
    alg('A normal apostrophe is syntax unless represented as a literal','P7-074',ev(F+'frmRptRentInvoices.xaml.cs','285-335'),raw,escaped,raw.count("'")==3 and escaped.count("'")==4,'String construction/count only, NOT execution of DataView or SQL and NOT an exploit or complete LIKE encoder.')
    state={'all_items':False,'name_enabled':True,'code_enabled':True,'search_enabled':False,'selected_id':None}
    alg('Editable item text is not an ItemId selection','P7-075',ev(F+'frmRptSerialNo.xaml','228-261')+';'+ev(F+'frmRptSerialNo.xaml.cs','291-304'),state,{'search_enabled':True,'selected_id':'validated positive identity or explicit refusal'},state['selected_id'] is None and state['name_enabled'] and not state['search_enabled'],'Manually transcribed local state; does not run WPF, permission hooks or command routing.')
    columns={'sales_emp','ItemId','ProductId','date','branch'}
    alg('Table name is not a source column for the user predicate','P7-076',ev(F+'frmRptSalesByCategory.xaml.cs','173-177')+';'+ev(R,'954-1060;1614-1623'),{'requested_column':'Safe_Emps','in_contract':'Safe_Emps' in columns},{'writer_column':'sales_emp','identity_semantics':'unresolved external contract'},'Safe_Emps' not in columns and 'sales_emp' in columns)
    alg('Initial branch zero becomes database null, not selected branch','P2-010',ev(F+'FrmRptSalesChart.xaml.cs','38-53;279-283'),{'branch_argument':0,'database_value':None},{'branch_scope':'authorized set, not unconditional all'},(None if 0==0 else 0) is None)
    incoming=[('A',D('1')),('B',D('9'))];outgoing=[('A',D('1'))]
    a=sum(v for br,v in incoming)-sum(v for br,v in outgoing if br=='A');b=sum(v for br,v in incoming if br=='A')-sum(v for br,v in outgoing if br=='A')
    alg('All-branch receipts minus one-branch issues creates a phantom serial balance','P4-029',ev(R,'4277-4335'),{'branch_A_balance':str(a),'positive_filter_keeps_it':a>0},{'branch_A_balance':str(b),'positive_filter_keeps_it':b>0},a==9 and b==0)
    alg('Primary quantity times selling-unit price repeats a known unit root','P7-041',ev(R,'4015-4020')+';'+ev(C+'InvoiceOper.cs','1594-1597'),str(D(10)*D(50)),str(D(1)*D(50)),D(10)*D(50)==500 and D(1)*D(50)==50)
    end=datetime(2026,11,30);last=datetime(2026,11,30,12);millisecond=datetime(2026,11,30,23,59,59,500000);endsecond=datetime(2026,11,30,23,59,59)
    alg('Calendar month and final fractional second need exclusive boundaries','P3-023',ev(F+'FrmRptSalesChart.xaml.cs','399-411')+';'+ev(F+'frmRptDailySales.xaml.cs','126-137'),{'last_day_noon_included':last<=end,'last_fractional_second_included':millisecond<=endsecond},{'both_in_same_selected_day_or_month':True},not(last<=end) and not(millisecond<=endsecond))
    alg('Empty reload can leave visible total from the old result','P7-046',ev(F+'frmRptDailySales.xaml.cs','112-118;153-159;193-200'),{'new_rows':[],'new_internal_total':0,'visible_total':100},{'new_rows':[],'visible_total':0},0!=100)
    text='name,amount\nA,1,234.00\n';parsed=list(csv.reader(io.StringIO(text)))
    rent_quote='"O"Neil","100"\n'
    try:list(csv.reader(io.StringIO(rent_quote),strict=True));quote_rejected=False
    except csv.Error:quote_rejected=True
    alg('CSV group separator and unescaped embedded quote break cell structure','P7-048',ev(F+'frmRptDailySales.xaml.cs','208-230')+';'+ev(F+'frmRptRentInvoices.xaml.cs','504-520'),{'header_cells':len(parsed[0]),'data_cells':len(parsed[1]),'wrapped_quote_rejected_by_python_csv':quote_rejected},{'data_cells':2,'literal_quote_preserved':True},len(parsed[1])==3 and quote_rejected,'Python stdlib csv on synthetic text only; NOT Office, a formula interpreter, actual ERP output or a claim that every reader handles every dialect identically.')
    alg('Live controls can label a previously loaded snapshot with a new period','P7-045',ev(F+'frmRptDailySales.xaml.cs','239-272'),{'loaded_period':'A','header_from_controls':'B'},{'header_period':'A or explicitly dirty/blocked'},'A'!='B')

    sql=read(R,4030,4079)+'\n'+read(R,49049,49096)
    st('Type is declared but fixed sales/POS filters appear in both script variants','P7-066',ev(R,'4030-4079;49049-49096'),compact(sql).count('inv_type=2orinv_type=3')==8 and sql.lower().count('@inv_type')==4)
    chart_sql=read(R,3974,4079)+'\n'+read(R,48999,49096)
    st('No delete predicate in these four bounded procedure bodies','P7-067',ev(R,'3974-4079;48999-49096'),'is_deleted' not in chart_sql.lower())
    filters=read(F+'frmRptSalesByCategory.xaml.cs',95,195)
    st('Three >0 guards with DataView loaders, not inserted all sentinels','P7-068',ev(F+'frmRptSalesByCategory.xaml.cs','95-195'),len(re.findall(r'SelectedIndex\s*>\s*0',filters))==3 and '.Items.Add(' not in filters and filters.count('ItemsSource')==4)
    money=read(F+'frmRptSalesByCategory.xaml.cs',205,248)
    st('Literal 0.15 and 1.15, not stored tax fields, in monetary query','P7-069',ev(F+'frmRptSalesByCategory.xaml.cs','205-248'),'* 0.15 AS itemvat' in money and '* 1.15 AS itemNet' in money and 'taxval' not in money.lower() and 'taxperc' not in money.lower())
    category_sql=read(R,4393,4453)+'\n'+read(R,49644,49776)
    st('Unit-price-only share and distinct denominator-zero guards','P7-070',ev(F+'frmRptSalesByCategory.xaml.cs','205-248')+';'+ev(R,'4393-4453;49644-49776'),'ItemPriceWithoutVAT * minus / ' in money and 'NULLIF(InvSum,0)' in money and category_sql.count('exchange_price * minus  /InvSum')==6 and 'NULLIF' not in category_sql)
    projection=read(F+'frmRptSalesByCategory.xaml.cs',490,524)
    st('Print projection creates one header and never enumerates results','P7-071',ev(F+'frmRptSalesByCategory.xaml.cs','490-524'),projection.count('new InventoryData')==1 and projection.count('list.Add(item)')==1 and 'CategoryList' not in projection and 'ItemDetails' not in projection and 'foreach' not in projection)
    components=read(F+'frmRptProducedItems.xaml.cs',168,228);invsub=read(R,1023,1060);catalog=read(R,487,504);writer=read(F+'frmProductionOrder.xaml.cs',1461,1499)
    st('ComponentId belongs to catalog here, not supplied movement table contract','P7-072',ev(F+'frmRptProducedItems.xaml.cs','168-228')+';'+ev(R,'1023-1060;487-504')+';'+ev(F+'frmProductionOrder.xaml.cs','1461-1499'),'SELECT ComponentId' in components and 'ComponentId' not in invsub and 'ComponentId' in catalog and '[ItemId]' in invsub and '@ItemId' in writer and '@ProductId' in writer)
    rent=read(F+'frmRptRentInvoices.xaml.cs',1,717);rent_xaml=read(F+'frmRptRentInvoices.xaml',223,346)
    date_tags=re.findall(r'<dxe:DateEdit\b[^>]*x:Name="txt(?:From|To)Date"[^>]*/>',rent_xaml,re.S)
    st('Rental date handler definitions have no local XAML/programmatic subscription','P7-073',ev(F+'frmRptRentInvoices.xaml.cs','1-717')+';'+ev(F+'frmRptRentInvoices.xaml','223-346'),len(date_tags)==2 and all('Changed=' not in t for t in date_tags) and rent.count('txtFromDate_ValueChanged')==1 and rent.count('txtToDate_ValueChanged')==1 and 'Cond         = "";' in rent)
    generate=read(F+'frmRptRentInvoices.xaml.cs',285,335)
    st('Raw text enters RowFilter expressions without a literal encoder','P7-074',ev(F+'frmRptRentInvoices.xaml.cs','285-335'),'_dataView.RowFilter  = filter;' in generate and "cust LIKE '%{txtClientName.Text.Trim()}%'" in generate and '.Replace(' not in generate)
    valid=[]
    for n,a,b,c1,c2 in [('frmRptSerialNo',228,261,291,304),('frmRptSerialNoSummary',227,259,157,169)]:
        x=read(F+n+'.xaml',a,b);cs=read(F+n+'.xaml.cs',c1,c2)
        btn=re.search(r'<Button\b(?:(?!</Button>).)*?Click="btnSearch_Click"[^>]*/>',x,re.S)
        valid.append(bool(btn and 'IsEnabled="False"' in btn[0]) and 'txtItemCode.IsEnabled = !isAll;' in cs and 'txtItemName.IsEnabled = !isAll;' in cs and 'btn' not in cs.lower())
    st('Item toggle enables text only, not the locally disabled search button','P7-075',ev(F+'frmRptSerialNo.xaml','228-261')+';'+ev(F+'frmRptSerialNo.xaml.cs','291-304')+';'+ev(F+'frmRptSerialNoSummary.xaml','227-259')+';'+ev(F+'frmRptSerialNoSummary.xaml.cs','157-169'),all(valid))
    itemddl=read(R,439,479);invddl=read(R,954,1060);safeemps=read(R,1614,1623);user=read(F+'frmRptSalesByCategory.xaml.cs',132,177);invwriter=read(C+'InvoiceOper.cs',1531,1545)
    st('Safe_Emps predicate differs from supplied source columns and writer','P7-076',ev(F+'frmRptSalesByCategory.xaml.cs','132-177')+';'+ev(R,'439-479;954-1060;1614-1623')+';'+ev(C+'InvoiceOper.cs','1531-1545'),'AND Safe_Emps=' in user and 'Safe_Emps' not in itemddl+invddl and 'CREATE TABLE [dbo].[Safe_Emps]' in safeemps and '@sales_emp' in invwriter)
    initial=read(F+'FrmRptSalesChart.xaml.cs',38,95);branch=read(F+'FrmRptSalesChart.xaml.cs',279,283)
    st('Branch policy code exists, but initial four loaders receive zero','P2-010',ev(F+'FrmRptSalesChart.xaml.cs','38-95;279-283'),initial.count('(0, null, null)')==4 and 'BranchPermissions();' in initial and 'branchId == 0 ? (object)DBNull.Value : branchId' in branch)
    asym=read(R,4277,4335);before,after=asym.split('UNION ALL')
    st('Selected branch occurs only in outgoing half of serial summary','P4-029',ev(R,'4277-4335'),before.count('inv.branch')==0 and after.count('inv.branch')==1 and 'InvertoryImpact=1' in before and 'InvertoryImpact=2' in after)
    process=read(F+'frmRptDailyProcess.xaml.cs',196,257);safe=read(F+'frmRptDailyProcess.xaml.cs',401,412)
    st('Task.Run source reads controls and receipt condition lacks branch/user','P7-054;P2-010;P3-023',ev(F+'frmRptDailyProcess.xaml.cs','196-257;401-412'),'Task.Run(() => ShowResult())' in process and 'txtDateFrom.DateTime' in process and 'chkAllBranches' not in safe and 'cmbusers' not in safe and 'TreasuryID=' in safe)
    monthly=read(R,4085,4103);daily=read(R,3612,3625)
    st('Counterevidence: monthly/daily supplied sources do filter deletion and type','P7-066;P7-067',ev(R,'4085-4103;3612-3625'),'IS_Deleted=0' in monthly and 'inv_type=@inv_type' in monthly and 'IS_Deleted=0' in daily and 'inv_type=@InvType' in daily)
    serial=read(F+'frmRptSerialNo.xaml.cs',121,141)+'\n'+read(F+'frmRptSerialNo.xaml.cs',177,277)
    st('Counterevidence: serial drill preserves GlobalID and numeric type/proc','P7-061',ev(F+'frmRptSerialNo.xaml.cs','121-141;177-277'),'InvGlobalID  = row["InvGlobalID"]' in serial and "InvGlobalID=N'{globalId}'" in serial and 'switch (invTypeNo)' in serial and 'case 2 when procType == 1:' in serial)

    return dict(phase='7B3-partial-static-audit',audit_reference_date_utc='2026-11-16',
        application_code_imported_or_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,illustration_count=len(algebra),
        static_lexical_contract_check_count=len(lexical),illustrations=algebra,static_lexical_contract_checks=lexical,
        bounded_source_reads_not_semantic_coverage=[READS[k] for k in sorted(READS)],
        limit='Manual independent synthetic models plus separately bounded literal observations; not production impact, runtime acceptance, deployed SQL/DTO/template or all-path semantic coverage. No evidence file is written by this tool.')


if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,indent=2))
