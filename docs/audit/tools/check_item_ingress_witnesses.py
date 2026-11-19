#!/usr/bin/env python3
"""Read-only B23 supplied models and bounded lexical observations, NEVER ERP.

No application imports/C#/WPF/SQL/provider/Excel/SDK or policy execution.
Selection145 is potential pending final-selection versus cumulative-basket
contract; the accumulated IDs are a source-local observation, not a UI trial.
Batch146 and import147 are independent of duplicate-action143 and void/last-
index144. Models assume successful, distinct item lookups and rdAuto off unless
stated. Prices/units are supplied labels, not approved financial policy.
"""
from __future__ import annotations
import copy
import csv
from decimal import Decimal, InvalidOperation
import hashlib,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
from check_amountword_contract_witnesses import mask_noncode
ROOT=Path(__file__).resolve().parents[3]
BASE='SmartAuditERP/Form_WPF/'
READS=[
 ('frmItemsSrch.xaml.cs',1,55),('frmItemsSrch.xaml.cs',294,338),
 ('frmItemsSrch.xaml',596,614),('frmSalesInvoice.xaml.cs',183,203),
 ('frmSalesInvoice.xaml.cs',1364,1510),('frmSalesInvoice.xaml.cs',1514,1640),
 ('frmSalesInvoice.xaml.cs',2473,2477),('frmSalesInvoice.xaml.cs',2636,2681),
 ('frmSalesInvoice.xaml.cs',3048,3100),('frmSalesInvoice.xaml',1,16),
 ('frmSalesInvoice.xaml',518,550),('frmSalesInvoice.xaml',1098,1111),
 ('frmSalePurch.xaml.cs',408,619),('frmSalePurch.xaml.cs',780,813),
 ('frmSalePurch.xaml.cs',2347,2384),('frmSalePurch.xaml.cs',2800,2845),
 ('frmSalePurch.xaml',1,15),('frmSalePurch.xaml',735,789),
 ('frmInvSumByType.xaml.cs',275,321),('frmInvSumByType.xaml',416,430),
 ('frmImportDataGeneral.xaml.cs',38,55),('frmImportDataGeneral.xaml.cs',370,382),
 ('frmImportDataGeneral.xaml.cs',429,442),('frmImportDataGeneral.xaml.cs',996,1057),
 ('frmImportDataGeneral.xaml.cs',1188,1199),('frmImportDataGeneral.xaml',439,452),
 ('frmImportDataGeneral.xaml',601,609),('MsgExistItem.xaml.cs',1,57),
 ('MsgExistItem.xaml',59,134)]
NO_RUNTIME='Source-local text or supplied Python model only; no WPF event/order/modal/SQL/Excel or saved/printed/stock effect observed.'
def decimal_text(value):
    if not isinstance(value,str):raise ValueError('Supplied numeric text required')
    try:d=Decimal(value)
    except InvalidOperation as e:raise ValueError('Invalid supplied decimal') from e
    if not d.is_finite():raise ValueError('Finite supplied decimal required')
    return format(d,'f')
def ids(value):
    if not isinstance(value,list) or any(type(i) is not int or i<=0 for i in value):
        raise ValueError('List of positive exact integer IDs required')
    if len(value)!=len(set(value)):raise ValueError('Distinct supplied IDs required')
    return list(value)
def selection_history(snapshots,final_id,confirmed=True):
    if type(confirmed) is not bool or type(final_id) is not int or final_id<=0 or not isinstance(snapshots,list) or not snapshots:
        raise ValueError('Explicit selection history/final ID/confirmation required')
    history=[ids(s) for s in snapshots]
    if final_id not in history[-1]:raise ValueError('Final ID must be selected in final supplied snapshot')
    accumulated=[]
    for snapshot in history:
        for item in snapshot:
            if item not in accumulated:accumulated.append(item)
    if final_id in accumulated:accumulated.remove(final_id)
    accumulated.append(final_id)
    return dict(final_selected_ids=history[-1],returned_itemlist_if_confirmed=accumulated,
                accepted_batch=accumulated if confirmed else [],
                stale_vs_current_selection=[x for x in accumulated if x not in history[-1]],
                selection_semantics_owner_unresolved=True,wpf_executed=False)
def sales_batch(prefix,selected,confirmed=True):
    before=ids(prefix);batch=ids(selected)
    if set(before)&set(batch):raise ValueError('Distinct successful nonduplicate lookups only')
    if type(confirmed) is not bool:raise ValueError('Explicit confirmation bool required')
    rows=list(before);cursor=len(rows);removed=[]
    for item in batch if confirmed else []:
        if cursor<len(rows):removed.append(rows.pop(cursor))
        rows.append(item);cursor=len(rows)-1
    return dict(rows=rows,removed_prior_batch_ids=removed,
                all_lookups_successful_supplied=True,duplicate_dialog_executed=False,
                application_executed=False)
def purchase_batch_control(prefix,selected,confirmed=True):
    before=ids(prefix);batch=ids(selected)
    if set(before)&set(batch) or type(confirmed) is not bool:raise ValueError('Distinct/explicit control required')
    # The inspected caller appends an empty seed for EACH item, and its loader
    # removes only an empty ItemId<=0 seed before appending a hydrated row.
    rows=list(before)
    for item in batch if confirmed else []:rows.append(item)
    return dict(rows=rows,per_iteration_empty_seed_supplied=True,application_executed=False)
def import_hydration(seed,catalog,lookup_success=True,editor='sales'):
    fields={'code','description','unit','quantity','price'}
    if not isinstance(seed,dict) or set(seed)!=fields or not isinstance(catalog,dict) or set(catalog)!={'item_id','unit','price'}:
        raise ValueError('Exact inert seed/catalog shapes required')
    if type(lookup_success) is not bool or editor not in ('sales','purchase') or type(catalog['item_id']) is not int or catalog['item_id']<=0:
        raise ValueError('Explicit bounded hydration inputs required')
    if any(not isinstance(seed[k],str) for k in fields) or not isinstance(catalog['unit'],str) or not catalog['unit']:
        raise ValueError('Inert supplied strings required')
    source=copy.deepcopy(seed);source['quantity']=decimal_text(source['quantity']);source['price']=decimal_text(source['price'])
    quote=decimal_text(catalog['price'])
    after=(dict(code=source['code'],description='',unit=catalog['unit'],quantity='1',price=quote)
           if lookup_success else copy.deepcopy(source))
    return dict(editor=editor,before_seed=source,after_hydration=after,
                fields_changed=[k for k in ('description','unit','quantity','price') if source[k]!=after[k]],
                successful_lookup_supplied=lookup_success,rdAuto_off_supplied=True,
                failed_or_no_match_branch_not_modelled=not lookup_success,
                duplicate_dialog_needed=False,actual_price_or_conversion_policy_accepted=False,
                application_executed=False)
def decode(path):
    raw=path.read_bytes()
    try:return raw.decode('utf-8-sig'),'utf-8-sig-read-only'
    except UnicodeDecodeError:return raw.decode('cp1256'),'cp1256-read-only-not-compiler-acceptance'
def text(name,a,b):
    s,_=decode(ROOT/BASE/name);return '\n'.join(s.splitlines()[a-1:b])
def ev(*parts):return ';'.join(BASE+p for p in parts)
def msg_constructors(source,path):
    """Literal new tokens only; mask comments/strings, keep source line numbers."""
    masked=mask_noncode(source)
    return [dict(path=path,line=masked.count('\n',0,m.start())+1)
            for m in re.finditer(r'\bnew\s+MsgExistItem\s*\(',masked)]
def build():
    illustrations=[];static=[];reads=[];errors=[]
    def model(n,roots,title,result,expect,evidence,limit=NO_RUNTIME):
        ok=expect(result)
        illustrations.append(dict(id=f'ALG7B23-{n:02d}',finding_ids=roots,title=title,
          supplied_result=result,illustration_assertions_passed=ok,
          source_application_executed=False,evidence=evidence,limit=limit))
        if not ok:errors.append(f'model{n}')
    picker=ev('frmItemsSrch.xaml.cs:294-338','frmItemsSrch.xaml:596-614')
    batch=ev('frmSalesInvoice.xaml.cs:1393-1510','frmSalesInvoice.xaml.cs:2473-2477')
    imports=ev('frmSalesInvoice.xaml.cs:2636-2681','frmSalesInvoice.xaml.cs:1393-1510','frmSalesInvoice.xaml.cs:1514-1640','frmSalePurch.xaml.cs:2347-2384','frmSalePurch.xaml.cs:436-619')
    model(1,'P7-145','A selected then deselected; B confirmed',selection_history([[11],[22]],22),lambda p:p['accepted_batch']==[11,22] and p['stale_vs_current_selection']==[11],picker,'Accumulation is observed in the model; whether an intentional cumulative basket is required remains an owner contract, so145 stays potential. '+NO_RUNTIME)
    model(2,'P7-145','One stable selection control',selection_history([[22]],22),lambda p:p['stale_vs_current_selection']==[] and p['accepted_batch']==[22],picker)
    model(3,'P7-145','Deduplication is not removal reconciliation',selection_history([[11,22],[22]],22),lambda p:p['accepted_batch']==[11,22] and len(set(p['accepted_batch']))==2,picker)
    model(4,'P7-145','ISDone false consumer control',selection_history([[11],[22]],22,False),lambda p:p['accepted_batch']==[],picker)
    model(5,'P7-146','Two distinct successful picks replace prior batch row',sales_batch([90],[11,22]),lambda p:p['rows']==[90,22] and p['removed_prior_batch_ids']==[11],batch)
    model(6,'P7-146','One pick preserves prefix control',sales_batch([90],[11]),lambda p:p['rows']==[90,11] and not p['removed_prior_batch_ids'],batch)
    model(7,'P7-146','Cancelled picker leaves prefix control',sales_batch([90],[11,22],False),lambda p:p['rows']==[90],batch)
    model(8,'P7-146','Other selected editor seeds each iteration',purchase_batch_control([90],[11,22]),lambda p:p['rows']==[90,11,22],ev('frmSalePurch.xaml.cs:780-813','frmSalePurch.xaml.cs:436-501'))
    seed=dict(code='A',description='import-A',unit='PACK',quantity='7',price='50');catalog=dict(item_id=11,unit='EACH',price='20')
    model(9,'P7-147','Sales import seed discarded before hydration',import_hydration(seed,catalog),lambda p:p['after_hydration']==dict(code='A',description='',unit='EACH',quantity='1',price='20') and len(p['fields_changed'])==4,imports)
    model(10,'P7-147','Purchase import same cause separate implementation',import_hydration(seed,catalog,editor='purchase'),lambda p:len(p['fields_changed'])==4,imports)
    same=dict(code='A',description='',unit='EACH',quantity='1',price='20')
    model(11,'P7-147','Equal-to-default import control',import_hydration(same,catalog),lambda p:p['fields_changed']==[],imports)
    model(12,'P7-147','No successful lookup is outside hydration-loss proof',import_hydration(seed,catalog,False),lambda p:p['fields_changed']==[],imports,'The failed/no-match branch is outside this model, not accepted failure handling. '+NO_RUNTIME)
    def lexical(n,roots,title,ok,evidence,limit=NO_RUNTIME):
        static.append(dict(id=f'ST7B23-{n:02d}',finding_ids=roots,title=title,
          documented_text_observation_matches=bool(ok),source_application_executed=False,
          evidence=evidence,limit=limit))
        if not ok:errors.append(f'lexical{n}')
    s=text('frmItemsSrch.xaml.cs',298,310)
    lexical(1,'P7-145','Selection handler adds current members without removal',all(x in s for x in ('GridControl1.SelectedItems','!Itemlist.Contains(itemId)','Itemlist.Add(itemId)')) and 'Itemlist.Clear' not in s and 'Itemlist.Remove' not in s,picker)
    s=text('frmItemsSrch.xaml.cs',318,338)
    lexical(2,'P7-145','Confirmation removes/readds current ID only',all(x in s for x in ('Itemlist.Remove(itemId)','ISDone = true','Itemlist.Add(itemId)','Close()')),picker)
    s=text('frmItemsSrch.xaml',596,614)
    lexical(3,'P7-145','Extended full-row selection wired to handlers',all(x in s for x in ('SelectionMode="Extended"','SelectionChanged="GridControl1_SelectionChanged"','KeyDown="GridControl1_KeyDown"')),picker)
    s=text('frmSalesInvoice.xaml.cs',1393,1510)
    lexical(4,'P7-146','Sales batch cursor and unconditional in-range removal',all(x in s for x in ('if (RowIndex < _itemsSource.Count)','_itemsSource.RemoveAt(RowIndex)','foreach (int id in frm.Itemlist)','RowIndex = _itemsSource.Count - 1')),batch)
    s=text('frmSalePurch.xaml.cs',436,501)+text('frmSalePurch.xaml.cs',780,813)
    lexical(5,'P7-146','Per-iteration empty seed and empty-only deletion control',all(x in s for x in ('_itemsSource[RowIndex].ItemId <= 0','var emptyRow = new InvItemRow_frmSale()','_itemsSource.Add(emptyRow)')),ev('frmSalePurch.xaml.cs:436-501','frmSalePurch.xaml.cs:780-813'))
    s=text('frmSalesInvoice.xaml.cs',2636,2681)
    lexical(6,'P7-147','Sales import seed then void lookup',all(x in s for x in ('Description = frm.dtInvSel','Quantity = Convert.ToDouble','newRow.Price = importPrice','_itemsSource.Add(newRow)','SearchByCode()')),imports)
    s=text('frmSalePurch.xaml.cs',2347,2384)
    lexical(7,'P7-147','Purchase import seed then void lookup',all(x in s for x in ('Description = r[','Quantity = Convert.ToDouble','emptyRow.Price = price','_itemsSource.Add(emptyRow)','SearchByCode()')),imports)
    s=text('frmSalesInvoice.xaml.cs',1364,1510)+text('frmSalePurch.xaml.cs',408,501)
    lexical(8,'P7-147','Both Code lookup paths hydrate with unitId zero',s.count('SearchByID(0)')>=2,imports)
    s=text('frmSalesInvoice.xaml.cs',3048,3100)+text('frmSalePurch.xaml.cs',2800,2845)
    lexical(9,'P7-147','Replacement models default description to empty',s.count('private string _description = ""')==2,ev('frmSalesInvoice.xaml.cs:3048-3100','frmSalePurch.xaml.cs:2800-2845'))
    s=text('frmImportDataGeneral.xaml.cs',996,1057)
    lexical(10,'P7-147','Wizard emits mapped fields only after Code guard',all(x in s for x in ('IsItemExist(itemCode)','dtInvSel.Rows.Add(itemCode, description, unitId','quantity, Math.Round(price, 2)','ISDone = true')),ev('frmImportDataGeneral.xaml.cs:996-1057','frmImportDataGeneral.xaml.cs:1188-1199'))
    s=text('frmInvSumByType.xaml.cs',275,321)
    lexical(11,'H7B23-03','Report has literal constructors for selected editors',all(x in s for x in ('new frmSalePurch()','new frmSalesInvoice()','.Show()','.Navigate(')),ev('frmInvSumByType.xaml.cs:275-321','frmInvSumByType.xaml:416-430'),'Literal report reachability only; no ACL, Loaded timing, branch identity or save acceptance. '+NO_RUNTIME)
    s=text('frmSalesInvoice.xaml.cs',1393,1477)+text('frmSalePurch.xaml.cs',436,501)
    lexical(12,'P7-143','Other selected consumers keep reversed1/2 homologue',s.count('.Action == 1')>=2 and '.Action != 2' in s,ev('frmSalesInvoice.xaml.cs:1393-1477','frmSalePurch.xaml.cs:436-501','MsgExistItem.xaml.cs:34-53','MsgExistItem.xaml:59-134'),'Same143 cause only; no registry extension or new duplicate finding, no modal execution. '+NO_RUNTIME)
    for name,a,b in READS:
        path=ROOT/BASE/name;s,encoding=decode(path);ls=s.splitlines()
        if not 1<=a<=b<=len(ls):raise ValueError('Read bounds:'+name)
        reads.append(dict(path=BASE+name,start=a,end=b,encoding_observation=encoding,
          path_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
          bounded_text_sha256=hashlib.sha256('\n'.join(ls[a-1:b]).encode()).hexdigest(),
          not_body_or_runtime_coverage=True))
    with (ROOT/'docs/audit/evidence/inventory.csv').open(encoding='utf-8',newline='') as stream:
        paths=[ROOT/r['path'] for r in csv.DictReader(stream)
               if r['path'].endswith('.cs') and r['kind']=='source']
    matches=[];fallback=[]
    for path in paths:
        s,encoding=decode(path)
        if encoding.startswith('cp1256'):fallback.append(path.relative_to(ROOT).as_posix())
        matches.extend(msg_constructors(s,path.relative_to(ROOT).as_posix()))
    return dict(audit_reference_date_utc='2026-11-16',source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',
      application_code_imported_or_executed=False,dotnet_wpf_sql_or_excel_executed=False,
      B_R4g_bounded_not_whole7B_closure=True,
      unresolved_external_contracts_and_explicit_splits_retained=True,
      erp_runtime_tests_executed=0,
      sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,
      phase7C_started=False,phase8_authorized_or_started=False,application_remediation_performed=False,
      illustration_count=len(illustrations),lexical_check_count=len(static),illustrations=illustrations,
      static_lexical_contract_checks=static,bounded_source_reads_not_semantic_coverage=reads,
      constructor_discovery=dict(source_csharp_paths_lexically_scanned=len(paths),
        exact_new_MsgExistItem_tokens=matches,strict_utf8_fallback_cp1256_paths_not_compiler_acceptance=fallback,
        not_complete_callgraph_or_runtime_reachability=True,scanned_bodies_not_reviewed=True),
      retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
      limit='316 historical registry titles/classifications/evidence-path summaries screened plus selected nearest source chains, not all historical bodies.12 bounded paths not all consumers/census.145 potential pending selection contract;146/147 source-local with supplied success/normal-return assumptions; no save/print/financial loss observed. No pricing/merge/basket/SDK policy invented.7B/7 partial;R4h/B24 proposed;7C unstarted;8 unauthorized. Parallel repairs not merged into audit branch.',errors=errors)
if __name__=='__main__':
    result=build();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errors']))
