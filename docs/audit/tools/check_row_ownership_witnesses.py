#!/usr/bin/env python3
"""Read-only B24/R4h row-ownership illustrations/lexical observations, NEVER ERP.

Only supplied inert rows and bounded source text are examined. No application
import, compilation, WPF/modal/SQL/provider/SDK/device or business-data execution.
Identity at FillRowFromDt is observed BEFORE hydration; flat integer examples
for recalculation have ratio1/no discount/no VAT, not a financial pricing oracle.
Three selected MsgExistItem consumers, NOT all11 constructions/all477 bodies.
143 reversal/146 batch homologue not recounted or extended.7B/7 partial,7C
unstarted,8 unauthorized here; independent repairs never merged or presumed synced.
"""
from __future__ import annotations
import copy
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
P='SmartAuditERP/Form_WPF/'
SOURCE_SLICES={
 'frmPurchInv.xaml.cs':[(67,103),(133,145),(300,327),(359,457),(500,625),(628,666),(767,808),(2089,2095),(2293,2342),(2378,2378),(2460,2503)],
 'frmPurchInv.xaml':[(1,16),(548,581),(591,605),(632,734),(748,778)],
 'MsgExistItem.xaml.cs':[(1,57)],'MsgExistItem.xaml':[(59,134)],
 'frmItemsSrch.xaml.cs':[(23,60),(294,338),(442,445),(495,499),(571,574)],
 'frmItemsSrch.xaml':[(1,16),(206,214),(596,617)],
 'FrmIntialRestraiction.xaml.cs':[(509,574),(609,612)],
 'FrmIntialRestraiction.xaml':[(1,16),(393,420)],
 'frmProductionOrder.xaml.cs':[(122,126),(1130,1265)],
 'frmProductionOrder.xaml':[(1,16),(443,500)],
}

def number(value):
    if not isinstance(value,str) or not value.strip():raise ValueError('Finite nonnegative decimal strings only')
    try:n=Decimal(value)
    except InvalidOperation as exc:raise ValueError('Malformed decimal')from exc
    if not n.is_finite() or n<0:raise ValueError('Finite nonnegative decimal strings only')
    return n

def checked_rows(rows):
    if not isinstance(rows,list):raise ValueError('List of supplied rows required')
    seen=set()
    for row in rows:
        if not isinstance(row,dict) or set(row)!={'ref','item_id','qty','price','derived'}:raise ValueError('Exact inert row schema required')
        if not isinstance(row['ref'],str) or not row['ref'] or row['ref']in seen:raise ValueError('Distinct nonempty row references required')
        seen.add(row['ref'])
        if type(row['item_id'])is not int or row['item_id']<0:raise ValueError('Nonnegative exact integer item ID required')
        q,p,d=(number(row[k])for k in ('qty','price','derived'))
        if d!=q*p:raise ValueError('Initial flat derived values must be consistent, so new staleness is isolated')
    return copy.deepcopy(rows)

def row(ref,item,qty='2',price='10'):
    return dict(ref=ref,item_id=item,qty=qty,price=price,derived=str(number(qty)*number(price)))

def picker_cleanup(rows,current,is_done,item_id):
    out=checked_rows(rows)
    if type(current)is not int or type(is_done)is not bool or type(item_id)is not int:raise ValueError('Exact index/bool/ID types required')
    if is_done and item_id>0:
        return dict(rows=out,removed_ref=None,positive_confirmation_branch_not_modelled=True,application_executed=False)
    removed=out.pop(current)['ref']if 0<=current<len(out)else None
    return dict(rows=out,removed_ref=removed,positive_confirmation_branch_not_modelled=False,
                cleanup_has_no_empty_seed_ownership_test=True,application_executed=False)

def duplicate_dispatch(rows,current,item_id,action):
    out=checked_rows(rows)
    if type(current)is not int or current<0 or type(item_id)is not int or item_id<=0 or type(action)is not int or action not in (0,1,2,3):
        raise ValueError('Successful lookup/valid wire action and nonnegative index supplied only')
    hits=[i for i,r in enumerate(out)if r['item_id']==item_id]
    if len(hits)!=1:raise ValueError('Exactly one supplied duplicate identity required')
    found=hits[0];existing_ref=out[found]['ref'];removed=None;calculated_ref=None;attempted=None;clobbered=None
    if action==1:
        out[found]['qty']=str(number(out[found]['qty'])+1)
        if current!=found and 0<=current<len(out):removed=out.pop(current)['ref']
        attempted=found
        if 0<=found<len(out) and out[found]['item_id']>0:
            calculated_ref=out[found]['ref']
            out[found]['derived']=str(number(out[found]['qty'])*number(out[found]['price']))
    elif action==2:
        current=len(out)-1
        clobbered=out[current]['ref']if out[current]['item_id']not in (0,item_id)else None
        out[current]['item_id']=item_id
        # Only identity assignment is modelled: LoadItemInf/units/price/rdAuto
        # remain outside this branch model, not falsely assumed to be a noop.
    stale=[r['ref']for r in out if number(r['derived'])!=number(r['qty'])*number(r['price'])]
    return dict(rows=out,wire_action=action,found_index_before_removal=found,existing_ref=existing_ref,
       removed_ref=removed,attempted_calculation_index=attempted,calculated_ref=calculated_ref,
       stale_flat_derived_refs=stale,overwritten_unrelated_ref=clobbered,
       flat_stored_sum=str(sum((number(r['derived'])for r in out),Decimal(0))),
       flat_quantity_reference_sum=str(sum((number(r['qty'])*number(r['price'])for r in out),Decimal(0))),
       identity_only_before_hydration=(action==2),buttons_not_semantically_repaired=True,
       application_executed=False)

def purchase_batch_homologue(prefix,ids,current):
    if not isinstance(prefix,list) or not isinstance(ids,list) or type(current)is not int or not ids:
        raise ValueError('Supplied distinct positive ID lists required')
    if any(type(i)is not int or i<=0 for i in prefix+ids) or len(set(prefix+ids))!=len(prefix+ids):raise ValueError('Distinct positive ID lists only')
    out=list(prefix)
    for item in ids:
        if current<0 or current>=len(out):out.append(0);current=len(out)-1
        out[current]=item
    return dict(rows=out,same_cause_146_not_new_or_extended=True,successful_distinct_lookups_assumed=True,application_executed=False)

def consumer_controls(action):
    if type(action)is not int or action not in (0,1,2,3):raise ValueError('Exact wire0..3 required')
    return dict(initial_account_accepts_only_wire2=(action==2),initial_quantity_button_hidden=True,
      visible_new_line_button_wire=1,production_effect={0:'no-row-mutation',1:'increment-known-reference',2:'append-new-reference',3:'no-row-mutation'}[action],
      same_cause_143_not_new_or_extended=True,financial_or_production_acceptance=False,application_executed=False)

def build():
    source={};reads=[]
    for name,spans in SOURCE_SLICES.items():
        raw=(ROOT/P/name).read_bytes();text=raw.decode('utf-8');lines=text.splitlines(keepends=True);source[name]=lines
        for start,end in spans:
            if not 1<=start<=end<=len(lines):raise ValueError('Out of source range')
            selected=''.join(lines[start-1:end])
            reads.append(dict(path=P+name,start=start,end=end,encoding='strict-utf-8',utf8_BOM_present=raw.startswith(b'\xef\xbb\xbf'),
               source_sha256=hashlib.sha256(raw).hexdigest(),selected_text_utf8_sha256=hashlib.sha256(selected.encode()).hexdigest(),
               whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True))
    def text(name,a,b):
        if not any(lo<=a<=b<=hi for lo,hi in SOURCE_SLICES[name]):raise ValueError('Observation outside declared bounded reads')
        return ''.join(source[name][a-1:b])
    def evidence(*parts):return ';'.join(P+n+':'+str(a)+'-'+str(b)for n,a,b in parts)
    entry=evidence(('frmPurchInv.xaml.cs',133,145),('frmPurchInv.xaml.cs',767,808),('frmPurchInv.xaml.cs',2293,2299),('frmPurchInv.xaml.cs',2378,2378),('frmPurchInv.xaml',558,581),('frmPurchInv.xaml',770,778))
    cancel=entry+';'+evidence(('frmItemsSrch.xaml.cs',23,60),('frmItemsSrch.xaml.cs',442,445),('frmItemsSrch.xaml.cs',495,499),('frmItemsSrch.xaml.cs',571,574),('frmItemsSrch.xaml',206,214))
    target=evidence(('frmPurchInv.xaml.cs',548,625),('frmPurchInv.xaml.cs',628,666),('frmPurchInv.xaml.cs',2293,2327))
    calc=evidence(('frmPurchInv.xaml.cs',300,327),('frmPurchInv.xaml.cs',359,457),('frmPurchInv.xaml.cs',575,587),('frmPurchInv.xaml.cs',2460,2503),('frmPurchInv.xaml',632,734))
    dialog=evidence(('MsgExistItem.xaml.cs',1,57),('MsgExistItem.xaml',59,134),('frmPurchInv.xaml.cs',575,594),('FrmIntialRestraiction.xaml.cs',509,574),('frmProductionOrder.xaml.cs',1185,1212))
    controls=evidence(('FrmIntialRestraiction.xaml.cs',509,574),('FrmIntialRestraiction.xaml',393,420),('frmProductionOrder.xaml.cs',1130,1265),('frmProductionOrder.xaml',443,500))
    a=row('input-X',90);b=row('existing-A',11);z=row('last-Z',22,qty='4',price='5');seed=row('seed',0,qty='0',price='0')
    illustrations=[]
    def alg(root,title,result,assertion,ev,limit):
        illustrations.append(dict(id=f'ALG7B24-{len(illustrations)+1:02d}',finding_ids=root,title=title,result=result,
           illustration_assertions_passed=bool(assertion),source_application_executed=False,evidence=ev,limit=limit))
    r=picker_cleanup([a,b],0,False,-1);alg('P7-148','Cancel removes a nonempty current row',r,r['removed_ref']=='input-X',cancel,'Supplied stable current index and false result; no WPF cancellation/rendering/save observed.')
    r=picker_cleanup([b,seed],1,False,-1);alg('P7-148','Blank-seed cleanup control',r,r['removed_ref']=='seed',cancel,'Removing an actually-owned seed can be appropriate; this control does not prove ownership of any current row.')
    r=picker_cleanup([a,b],0,True,0);alg('P7-148','Confirmed nonpositive ID uses the other destructive cleanup',r,r['removed_ref']=='input-X',cancel,'Supplied invalid confirmed result, not an observed picker failure.')
    r=[picker_cleanup([a],i,False,-1)for i in (-1,1)];alg('P7-148','Out-of-range cleanup guards',r,all(x['removed_ref']is None for x in r),cancel,'Index guards limit the defect; they are not row ownership tests or all-cancel acceptance.')
    r=duplicate_dispatch([a,b,z],0,11,2);alg('P7-149','Wire2 changes unrelated last-row identity',r,r['overwritten_unrelated_ref']=='last-Z' and len(r['rows'])==3,target+';'+dialog,'One duplicate sufficient; identity assignments before hydration only. Reversal143 is separate, no new-line or pricing policy silently accepted.')
    r=duplicate_dispatch([a,b,seed],2,11,2);alg('P7-149','Last-row blank seed control',r,r['overwritten_unrelated_ref']is None and r['rows'][-1]['item_id']==11,target,'A genuine trailing seed masks unrelated-row clobber; no acceptance of all new-line/cancel/unit/price paths.')
    r=duplicate_dispatch([b],0,11,2);alg('P7-149','Single matching last row control',r,r['overwritten_unrelated_ref']is None and len(r['rows'])==1,target,'No unrelated row exists to clobber; lack of a new row and hydration policies remain separate questions.')
    r=duplicate_dispatch([a,b,z],0,11,1);alg('P7-150','Removal before duplicate recalculates the following reference',r,r['calculated_ref']=='last-Z' and r['stale_flat_derived_refs']==['existing-A'] and Decimal(r['flat_stored_sum'])==40 and Decimal(r['flat_quantity_reference_sum'])==50,calc,'Flat ratio1/no VAT/no discount and supplied integers, not .NET formatting/tax/save acceptance. Removal intent not adjudicated.')
    r=duplicate_dispatch([a,b],0,11,1);alg('P7-150','Old index can become out of range and GetRowAt returns null',r,r['calculated_ref']is None and r['stale_flat_derived_refs']==['existing-A'],calc,'Guarded missed recalculation, not an asserted thrown exception; external subsequent recalculation not modelled.')
    r=duplicate_dispatch([b,a],1,11,1);alg('P7-150','Removal after existing row keeps its index',r,r['calculated_ref']=='existing-A' and not r['stale_flat_derived_refs'],calc,'Order control only; does not validate merge policy or financial result.')
    r=duplicate_dispatch([b,z],0,11,1);alg('P7-150','Same current/existing row avoids removal',r,r['removed_ref']is None and not r['stale_flat_derived_refs'],calc,'Equality control only, not a fix for a row before foundIndex.')
    r=[duplicate_dispatch([a,b,z],0,11,k)for k in (0,3)];alg('P7-143','Wire0/3 does not mutate rows in this duplicate branch',r,all(x['rows']==[a,b,z]for x in r),dialog,'Local duplicate dispatch only, NOT picker cleanup148, import144, or all modal/caller cancellation.')
    r=purchase_batch_homologue([90],[11,22],0);alg('P7-146','Shared valid cursor fills the same row for a distinct batch',r,r['rows']==[22],entry+';'+target,'Same batch-boundary cause146; comparison only, not a new finding or historical extension. All positive lookups supplied.')
    r={str(k):consumer_controls(k)for k in (0,1,2,3)};alg('P7-143','Initial-account hidden wire and production append contrast',r,not r['1']['initial_account_accepts_only_wire2'] and r['2']['production_effect']=='append-new-reference' and r['3']['production_effect']=='no-row-mutation',dialog+';'+controls,'Visible new-line wire1 rejected in opening-account path while wire2 button hidden: same143, no actual hidden click. No production save/BOM/ACL acceptance.')
    lexical=[]
    lexical_roots=('P7-148;P7-149','P7-148;P7-149;P7-150','P7-148','P7-148','P7-149;P7-150',
       'P7-149','P7-150','P7-150','P7-150','P7-150','P7-150','P7-148','P7-143','P7-143')
    def lex(title,ok,ev,limit):
        lexical.append(dict(id=f'ST7B24-{len(lexical)+1:02d}',finding_ids=lexical_roots[len(lexical)],title=title,documented_text_observation_matches=bool(ok),source_application_executed=False,evidence=ev,limit=limit))
    pc=lambda a,b:text('frmPurchInv.xaml.cs',a,b)
    lex('F1 and context menu call the picker without appending/resetting the cursor','addNewItem();'in pc(133,145) and 'RowIndex'not in pc(133,145) and '=> addNewItem();'in pc(2378,2378),entry,'Literal entry only; no key event dispatch or live selection observed.')
    lex('Selection and edit callbacks are actually wired','SelectionChanged="GridControl1_SelectionChanged"'in text('frmPurchInv.xaml',548,581) and 'CellEditEnding="GridControl1_CellEditEnding"'in text('frmPurchInv.xaml',548,581) and 'RowIndex = GetFocusedRowIndex();'in pc(2293,2299),entry,'Event wiring not full UX/lifecycle7C, focus scheduling or rendering acceptance.')
    lex('Both picker cleanup branches remove any in-range current row',pc(791,808).count('_gridSource.RemoveAt(RowIndex)')==2 and 'ItemIdDgv'not in pc(791,808),cancel,'Text absence is bounded to this explicit cleanup, not all application cleanup.')
    lex('New picker defaults false and closes without confirming','ISDone { get; set; } = false' in text('frmItemsSrch.xaml.cs',23,60) and 'Close();'in text('frmItemsSrch.xaml.cs',442,445) and 'Close();'in text('frmItemsSrch.xaml.cs',495,499) and 'ISDone'not in text('frmItemsSrch.xaml.cs',571,574),cancel,'No modal/Hide/Close invocation; successful return assumed when evaluating caller.')
    lex('Successful active-Code lookup delegates with unit0','IS_Deleted=0 and Code='in pc(500,523) and 'SearchByID(0);'in pc(500,523),target,'No SQL/uniqueness/schema/grant or unit0 SDK contract accepted.')
    lex('Wire2 selects Count-1 and mutates that row without Add','RowIndex = _gridSource.Count - 1;'in pc(588,593) and 'FillRowFromDt' in pc(588,593) and '_gridSource.Add'not in pc(588,593) and 'row.ItemIdDgv = dr["id"].ToString();'in pc(608,625),target,'Identity before LoadItemInf only; no price policy or persisted overwrite claimed.')
    t=pc(579,587);lex('Wire1 increments, removes, then recalculates the OLD foundIndex',t.index('QuantDgv =')<t.index('_gridSource.RemoveAt(RowIndex)')<t.index('CalcRowValues(foundIndex)'),calc,'Source order, not .NET event scheduling; foundIndex local is not adjusted after RemoveAt.')
    lex('GetRowAt and CalcRowValues guard invalid indices','return null;'in pc(300,305) and 'if (row == null || string.IsNullOrEmpty(row.ItemIdDgv)) return;'in pc(359,399),calc,'Missed calculation may be silent; no exception invented.')
    lex('CalcTot sums stored derived cells rather than rebuilding each line','row.SumPriceDgv' in pc(402,457) and 'sumPrice += sp;'in pc(402,457) and 'qty * price'not in pc(402,457),calc,'Flat stored-sum model does not certify invoice discounts/VAT/totals or saving.')
    lex('QuantDgv setter raises notification without recalculation','OnPC(nameof(QuantDgv))'in pc(2460,2503) and 'CalcRowValues'not in pc(2460,2503),calc,'Bounded model class only; no universal claim about all external subscribers.')
    lex('Quantity and derived totals use distinct bound properties','Binding QuantDgv,'in text('frmPurchInv.xaml',632,734) and 'Binding SumPriceDgv}'in text('frmPurchInv.xaml',632,734),calc,'Not a rendered or measured discrepancy; view update details unexecuted.')
    lex('Explicit Delete has confirmation whereas picker cleanup does not','MessageBoxResult.Yes' in pc(2329,2342) and '_gridSource.Remove(row);'in pc(2329,2342) and 'DXMessageBox'not in pc(791,808),entry+';'+evidence(('frmPurchInv.xaml.cs',2329,2342)),'Contrast only, not a separate missing prompt requirement or delete/ACL acceptance.')
    d=text('MsgExistItem.xaml.cs',1,57);lex('Shared reversed wire mapping remains143 in three selected consumers','Action = 2;'in d and 'Action = 1;'in d and 'إضافة الكمية' in text('MsgExistItem.xaml',59,134) and 'إدراج في بند جديد'in text('MsgExistItem.xaml',59,134) and 'msgExist.Action == 1'in pc(575,594) and 'msgExist.Action == 1'in text('frmProductionOrder.xaml.cs',1130,1265),dialog,'No new finding/extension for another occurrence; not all11 constructor bodies or allcallgraph.')
    init=text('FrmIntialRestraiction.xaml.cs',509,574);prod=text('frmProductionOrder.xaml.cs',1130,1265)
    lex('Initial-account wire2 is hidden; production appends a new reference','btnAddquantity.Visibility = Visibility.Collapsed;'in init and 'if (msgExist.Action != 2) return;'in init and '_itemsSource.Add(newRow);'in prod and 'AppendItemRow(itemId, dt.Rows[0]);'in prod,controls+';'+dialog,'Hidden-button code path is not a tested user action. Existing production020/021/022/133/134 barriers unchanged.')
    errors=[r['id']for r in illustrations if r['illustration_assertions_passed']is not True]+[r['id']for r in lexical if r['documented_text_observation_matches']is not True]
    return dict(audit_reference_date_utc='2026-11-16',source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',entry_checkout='f37c37ca6581c4d1546bf0e073326572f4b7af36',
       application_code_imported_or_executed=False,dotnet_wpf_sql_or_excel_executed=False,phase7C_started=False,phase8_authorized_or_started=False,application_remediation_performed=False,
       erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,
       B_R4h_bounded_not_whole7B_closure=True,unresolved_external_contracts_and_explicit_splits_retained=True,
       retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
       illustration_count=len(illustrations),lexical_check_count=len(lexical),illustrations=illustrations,static_lexical_contract_checks=lexical,
       bounded_source_reads_not_semantic_coverage=reads,selected_source_paths=10,selected_repeat_consumers=3,
       selected_paths_strict_utf8_decode=True,all477_sources_or_all11_constructors_body_reviewed=False,
       historical143_and146_not_recounted_or_extended=True,financial_price_unit_merge_or_basket_policy_invented=False,
       limit='34 bounded textual slices across10 paths, three selected repeat consumers. Supplied normal returns/stable current row/active unique lookup; no WPF/modal/SQL/Excel/build/SDK/REPX/ToDataTable/device/business data/remediation/measurement/acceptance.148 cancel cleanup not seed ownership;149 unrelated last-row identity before hydration independent of143;150 old foundIndex after removal, guarded-null not an asserted exception. Flat ratio1/noVAT/nodiscount integer examples are not .NET/tax/formatting or persisted amounts.143 and146 same-cause traces not recounted/extended;144/145/147 preserved,145/014/132 potential.7B/7 partial,R4i/B25 proposed,7C unstarted,8 unauthorized here. Independent repair conversation neither merged nor assumed started/synchronized.',errors=errors)

if __name__=='__main__':
    result=build();print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(1 if result['errors']else 0)
