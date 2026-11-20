#!/usr/bin/env python3
"""Inert B35/R4s linked-return boundary illustrations,NOT ERP execution.

Only current-year sale(2,2)/purchase(1,2) entries are selected. Boolean
returns,dirty state,normal dialog returns,reader snapshots and helper failures
are SUPPLIED,not observed. Tokens describe values at ref/field boundaries,
NOT CLR reference equality,DTO defaults,SDK aliasing or complete hydration.
No application code,SQL,WPF,ShowDialog,provider,number reservation or save.
Zero new roots/registry extensions;compare P4-013/P7-159/P7-160 without
silently extending their frozen evidence or certainty to all linked callers.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
ENTRY='e6f022ab5df771aab9631886ad713a8a7e6dfbfa'
SC='SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
SX='SmartAuditERP/Form_WPF/frmInvSale.xaml'
PC='SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs'
PX='SmartAuditERP/Form_WPF/frmInvPurch.xaml'
IO='SmartAuditERP/Class/InvoiceOper.cs'
IC='SmartAuditERP/Form_WPF/frmInvoiceItems.xaml.cs'
IX='SmartAuditERP/Form_WPF/frmInvoiceItems.xaml'
SOURCE_SLICES=(
 (SC,2721,2733),(SC,2734,2747),(SC,2748,2768),
 (PC,2173,2182),(PC,2207,2232),(IO,3941,3975),(IO,3976,3982),
 (IO,3983,4005),(IO,4006,4015),(IC,28,33),(IC,49,66),
 (IC,73,90),(IC,92,116),(IC,299,339),(IC,340,368),
 (IX,1,14),(IX,161,190),(SX,602,604),(PX,535,542),
 (SC,1607,1641),(SC,1662,1679),(PC,1531,1569),(PC,1571,1593),(SC,2563,2571),
)
EXPLORATORY_SLICES=(
 (SC,177,238),(PC,94,160),(SC,1546,1605),(PC,350,407),
 (SC,558,570),(PC,281,298),(SC,2770,2846),(PC,2183,2205),
 (SC,2848,2863),(IO,3219,3246),(IO,3496,3508),
)
LIMIT=('Supplied current-year branch,dirty flags,normal dialog returns,ref-boundary reader values and '
       'return/failure tokens only. Not CLR pointer equality,SDK defaults/aliasing,complete hydration,'
       'WPF gestures/event order,SQL,number reservation,stock/payment/save or deployed loss proof. '
       'Stop before CalcRows/BindingDGV/BindingControls;other linked/quotation/year/contract paths excluded.')
ROOTS=['P4-013','P7-159','P7-160']


def flag(value):
    if type(value) is not bool:raise ValueError('Explicit bool required,not int/SDK inference')
    return value


def count(value):
    if type(value) is not int or not 0<=value<=64:raise ValueError('Supplied bounded count,not bool')
    return value


def token(value,*,empty=False):
    if (type(value) is not str or not (0 if empty else 1)<=len(value)<=80
        or any(not(c.isascii() and (c.isalnum() or c in '_-:')) for c in value)):
        raise ValueError('Bounded opaque ASCII token,not SQL,path,secret or business text')
    return value


def dirty_predicate(editor,*,updated,is_new,item_count):
    if editor not in ('sale','purchase'):raise ValueError('Only two selected editor routes')
    updated,is_new,item_count=flag(updated),flag(is_new),count(item_count)
    return updated or (is_new and item_count>(1 if editor=='sale' else 0))


def new_command(editor,*,updated,is_new,item_count,answer):
    dirty=dirty_predicate(editor,updated=updated,is_new=is_new,item_count=item_count)
    if answer not in ('Yes','No'):raise ValueError('Supplied Yes/No,not real MessageBox')
    blocked=dirty and answer=='No'
    return dict(guard_asked=dirty,guard_blocks=blocked,clear_calls=0 if blocked else 1,
                current_value='draft-A' if blocked else 'reset-value',returns_typed_abandon_decision=False)


def search_gate(done,gid):
    flag(done);token(gid,empty=True)
    # The local source compares only with -1;this is NOT eligibility/GID validation.
    return done and gid!='-1'


def select_by_item(rows,selected):
    """Copy-only illustration of P4-013's ItemId loops,not a DTO implementation."""
    if type(rows) is not list or type(selected) is not list or len(rows)>64 or len(selected)>64:
        raise ValueError('Bounded synthetic lists only')
    result=[]
    for r in rows:
        if type(r) is not dict or set(r)!={'line','item','quantity','discount'}:raise ValueError('Synthetic row shape')
        result.append(dict(line=token(r['line']),item=token(r['item']),quantity=count(r['quantity']),discount=count(r['discount'])))
    for s in selected:
        if type(s) is not dict or set(s)!={'item','quantity','discount'}:raise ValueError('Synthetic selection shape')
        token(s['item']);count(s['quantity']);count(s['discount'])
    if not selected:return dict(done=False,closed=False,rows=result)
    for s in selected:
        for r in result:
            if r['item']==s['item']:r.update(quantity=s['quantity'],discount=s['discount'])
    ids={s['item'] for s in selected}
    return dict(done=True,closed=True,rows=[r for r in result if r['item'] in ids])


def linked_return(editor,*,updated,is_new,item_count,answer,search_done,gid,
                  reader='found',item_action='cancel',search_returns=True,items_return=True,
                  number_returns=True,discount_returns=True,helper_fault='none'):
    """Bounded operation order with supplied opaque reader outcome,not C# interpreter."""
    dirty=dirty_predicate(editor,updated=updated,is_new=is_new,item_count=item_count)
    if answer not in ('Yes','No'):raise ValueError('Supplied Yes/No required')
    search_gate(search_done,gid)
    if reader not in ('found','partial','null'):raise ValueError('Supplied reader boundary outcome')
    if item_action not in ('cancel','all','selected','empty-then-close'):raise ValueError('Selected child route only')
    if helper_fault not in ('none','before-search-result','after-bind'):raise ValueError('Selected helper catch boundary only')
    for f in (search_returns,items_return,number_returns,discount_returns):flag(f)
    state=dict(editor=editor,parent_value='draft-A',child_value=None,parent_note='draft-note',
        global_id='DOC-A',combined_id='COMBINED-A',reference='ref-A',is_new=is_new,
        search_gate_passed=False,item_done=False,clear_calls=0,events=[],terminal=None)
    def event(kind,**data):state['events'].append(dict(kind=kind,**data))
    def finish(where):state['terminal']=where;return state
    def clear():
        state['clear_calls']+=1;state.update(parent_value='reset-value',parent_note='unknown-constructor-note',
            global_id='unknown-constructor-GID',combined_id='supplied-reset-number',reference='-1',is_new=True)
        event('parent-new-assignment-and-completed-reset',ctor_defaults_inferred=False)
    if editor=='purchase':
        blocked=dirty and answer=='No';event('void-new-command-returned',guard_asked=dirty,guard_blocks=blocked)
        if not blocked:clear()
        # Its caller has no returned decision;selected(1,2) branch clears again.
        clear()
    else:
        event('no-local-abandon-call-in-selected-sale-route');clear()
    event('helper-entered',public_result_type='void')
    if not search_returns:return finish('search-dialog-nonreturn-supplied')
    if helper_fault=='before-search-result':
        event('helper-catch-returned-no-typed-failure')
    elif not search_gate(search_done,gid):
        event('search-gate-rejected-no-BindingInvoice')
    else:
        state['search_gate_passed']=True;event('BindingInvoice-ref-boundary-before-item-result',outcome=reader)
        if reader=='null':
            state['parent_value']=None
            event('helper-catch-after-null-access-no-typed-failure')
        else:
            state.update(parent_value='source-B' if reader=='found' else 'partial-B',parent_note='supplied-loaded-note',
                global_id='DOC-B',combined_id='COMBINED-B',is_new=False)
            if helper_fault=='after-bind':event('helper-catch-returned-after-bound-state')
            else:
                state['child_value']=state['parent_value'];event('child-field-assigned-from-ref-value',CLR_aliasing_proved=False)
                if not items_return:return finish('item-dialog-nonreturn-supplied')
                if item_action in ('cancel','empty-then-close'):
                    if item_action=='empty-then-close':event('empty-selection-returns-without-close-or-accept')
                    state['child_value']='child-reset-value';state['item_done']=False
                    event('CloseWithoutResult-replaces-child-field-not-parent-ref')
                else:
                    state['item_done']=True;event('item-result-accepted',route=item_action)
                    state['parent_value']=state['child_value'];event('final-ref-assignment-gated-by-item-done')
    event('helper-normal-void-return-no-rollback-assignment')
    if state['parent_value'] is None:return finish('parent-null-access-boundary-not-success')
    state['parent_note']='';event('parent-conversion-prefix',proc_type=2,impact=1 if editor=='sale' else 2,payment_scalars_set_to_zero=True)
    if editor=='sale':
        state['reference']=state['combined_id'];event('sale-reference-before-number',value=state['reference'])
    event('LoadInvNo-boundary',returns=number_returns,reservation_proved=False)
    if not number_returns:return finish('number-nonreturn-after-earlier-writes')
    state['combined_id']='supplied-new-number-token'
    if editor=='purchase':
        event('purchase-item-impact-loop-boundary',non_null_items_supplied=True)
        state['reference']=state['global_id'];event('purchase-reference-after-number',value=state['reference'])
    else:
        event('CalcItemsDiscountRates-boundary',returns=discount_returns)
        if not discount_returns:return finish('discount-nonreturn-before-ISNew-tail')
    state['is_new']=True;event('parent-ISNew-written-after-untyped-return')
    return finish('before-CalcRows-and-bindings-not-stable-UI-state')


def fixture(editor='sale',**overrides):
    args=dict(updated=True,is_new=False,item_count=2,answer='No',search_done=True,gid='DOC-B',
              reader='found',item_action='cancel',search_returns=True,items_return=True,
              number_returns=True,discount_returns=True,helper_fault='none')
    return linked_return(editor,**(args|overrides))


def build():
    ev=lambda p,a,z:f'{p}:{a}-{z}'
    alg=[]
    def a(n,title,value,ok,evidence,roots='P7-160'):
        alg.append(dict(id=f'ALG7B35-{n:02d}',title=title,supplied_boundary_trace=value,
            illustration_assertions_passed=bool(ok),finding_ids=roots,evidence=evidence,
            source_application_executed=False,limit=LIMIT))
    sale=fixture();purchase=fixture('purchase')
    a(1,'Sale clears before either picker result',sale,sale['clear_calls']==1 and sale['parent_value']=='source-B',ev(SC,2721,2768),'P7-159;P7-160')
    a(2,'Purchase No returns only from void new;linked branch still clears',purchase,purchase['events'][0]['guard_blocks'] is True and purchase['clear_calls']==1,ev(PC,1571,1593)+';'+ev(PC,2173,2182),'P7-159')
    yes=fixture('purchase',answer='Yes')
    a(3,'Purchase Yes can reach two completed CLR calls',yes,yes['clear_calls']==2,ev(PC,1531,1593)+';'+ev(PC,2173,2182),'P7-159')
    direct=new_command('purchase',updated=True,is_new=False,item_count=2,answer='No')
    a(4,'Direct new No control really blocks its own clear',direct,direct['clear_calls']==0 and direct['current_value']=='draft-A',ev(PC,1571,1593),'P7-159')
    reject=fixture(search_done=False,gid='-1')
    a(5,'Search rejection prevents bind,not preclear or conversion',reject,not reject['search_gate_passed'] and reject['parent_note']=='' and reject['clear_calls']==1,ev(IO,3976,3982)+';'+ev(SC,2748,2768))
    sent=fixture(search_done=True,gid='-1')
    a(6,'Done with sentinel still rejects only helper binding',sent,not sent['search_gate_passed'] and sent['is_new'] is True,ev(IO,3976,3982)+';'+ev(SC,2748,2768))
    a(7,'Nested child cancel does not restore pre-bind ref contents',sale,sale['child_value']=='child-reset-value' and sale['parent_value']=='source-B' and not sale['item_done'],ev(IO,3982,4015)+';'+ev(IC,351,368))
    allrows=fixture(item_action='all')
    a(8,'Insert-all explicit acceptance is a distinct control',allrows,allrows['item_done'] and any(e['kind']=='final-ref-assignment-gated-by-item-done' for e in allrows['events']),ev(IC,105,116)+';'+ev(IO,4002,4007))
    selected=fixture(item_action='selected')
    a(9,'Selected acceptance is supplied,not inferred from modal return',selected,selected['item_done'],ev(IC,299,339)+';'+ev(IO,4002,4007),'P4-013;P7-160')
    empty=fixture(item_action='empty-then-close')
    a(10,'Empty selection stays open before a separately supplied close',empty,not empty['item_done'] and empty['parent_value']=='source-B',ev(IC,299,339)+';'+ev(IC,351,368),'P4-013;P7-160')
    nonsearch=fixture(search_returns=False)
    a(11,'No normal first-dialog return means no parent conversion',nonsearch,nonsearch['terminal']=='search-dialog-nonreturn-supplied' and not any(e['kind']=='parent-conversion-prefix' for e in nonsearch['events']),ev(IO,3976,3982)+';'+ev(SC,2748,2768))
    nonitems=fixture(items_return=False)
    a(12,'No normal item-dialog return leaves bound state,not parent tail',nonitems,nonitems['parent_value']=='source-B' and not any(e['kind']=='parent-conversion-prefix' for e in nonitems['events']),ev(IO,3982,4007))
    null=fixture(reader='null')
    a(13,'Null ref outcome is not a successful converted invoice',null,null['terminal']=='parent-null-access-boundary-not-success' and null['parent_value'] is None,ev(IO,3982,4015)+';'+ev(IO,3496,3508))
    partial=fixture(reader='partial')
    a(14,'Supplied nonnull partial snapshot has no typed completion gate',partial,partial['parent_value']=='partial-B' and partial['is_new'] is True,ev(IO,3982,4015)+';'+ev(SC,2748,2768))
    caught=fixture(helper_fault='after-bind')
    a(15,'Caught helper failure after bound state returns no typed failure',caught,caught['child_value'] is None and caught['parent_note']=='',ev(IO,4008,4015)+';'+ev(SC,2748,2768))
    sn=fixture(number_returns=False);pn=fixture('purchase',number_returns=False)
    a(16,'Number nonreturn follows sale reference but precedes purchase reference',dict(sale=sn,purchase=pn),sn['reference']=='COMBINED-B' and pn['reference']=='-1' and sn['parent_note']==pn['parent_note']=='',ev(SC,2748,2768)+';'+ev(PC,2207,2232))
    a(17,'Sale uses combined ID;purchase uses GlobalID at different orders',dict(sale=sale['reference'],purchase=purchase['reference']),sale['reference']=='COMBINED-B' and purchase['reference']=='DOC-B',ev(SC,2755,2768)+';'+ev(PC,2219,2232))
    rows=[dict(line='L-A',item='I-A',quantity=1,discount=0),dict(line='L-B',item='I-A',quantity=2,discount=1),dict(line='L-C',item='I-C',quantity=3,discount=0)]
    one=select_by_item(rows,[dict(item='I-A',quantity=7,discount=2)])
    a(18,'P4-013 existing ItemId selection updates/keeps both distinct lines',one,[r['line'] for r in one['rows']]==['L-A','L-B'] and {r['quantity'] for r in one['rows']}=={7},ev(IC,299,348),'P4-013')
    last=select_by_item(rows,[dict(item='I-A',quantity=7,discount=2),dict(item='I-A',quantity=4,discount=1)])
    a(19,'Repeated ItemId selections have last-writer effect,not a new root',last,{r['quantity'] for r in last['rows']}=={4},ev(IC,315,348),'P4-013')
    clean=fixture('purchase',updated=False,is_new=False,item_count=0,answer='No',search_done=False,gid='-1')
    a(20,'Clean nonaccept also reaches conversion;dirty notifications not presumed',clean,clean['events'][0]['guard_asked'] is False and clean['clear_calls']==2 and clean['parent_note']=='',ev(PC,1571,1593)+';'+ev(PC,2173,2182)+';'+ev(PC,2207,2232),'P7-159;P7-160')
    def text(p,a,z):return '\n'.join((ROOT/p).read_text().splitlines()[a-1:z])
    static=[]
    def s(n,title,p,a,z,ok,roots='P7-160'):
        static.append(dict(id=f'ST7B35-{n:02d}',title=title,evidence=ev(p,a,z),finding_ids=roots,documented_text_observation_matches=bool(ok),source_application_executed=False,limit='Lexical selected-slice observation only;not compilation,SDK contract,DTO aliasing,UI event order,all callers or operational acceptance.'))
    s(1,'Sale XAML click wiring',SX,602,604,'Click="btnInsertLinkedInv_Click"' in text(SX,602,604),'P7-159')
    s(2,'Purchase XAML wiring and default collapsed state',PX,535,542,'Visibility="Collapsed"' in text(PX,535,542) and 'Click="btnInsertLinkedInv_Click"' in text(PX,535,542),'P7-159')
    s(3,'Sale(2,2) calls linked return',SC,2721,2733,'InvType == 2 && ProcType == 2' in text(SC,2721,2733) and 'InsertLinkedReturn(2, 1)' in text(SC,2721,2733),'P7-159')
    s(4,'Sale CLR precedes void helper then conversion',SC,2746,2768,text(SC,2746,2768).index('CLR();')<text(SC,2746,2768).index('InsertFromInv')<text(SC,2746,2768).index('Invoic.ProcType ='))
    s(5,'Purchase void-new call cannot propagate a typed decision',PC,2173,2182,'this.btnNew_Click(sender, e);' in text(PC,2173,2182) and text(PC,2173,2182).index('this.CLR();')<text(PC,2173,2182).index('InsertFromInv'),'P7-159')
    s(6,'Direct new honors its local guard',PC,1589,1593,'if (!this.CheckBeforeClear())' in text(PC,1589,1593),'P7-159')
    s(7,'Guard No predicate and count are explicit',PC,1571,1587,'MessageBoxResult.No' in text(PC,1571,1587) and '_invoiceItems.Count > 0' in text(PC,1571,1587),'P7-159')
    s(8,'Helper public result is void',IO,3941,3975,'public static void InsertFromInv(ref InvoiceDGV Invo, int Ptype)' in text(IO,3941,3975))
    s(9,'First search gate precedes ref binding',IO,3976,3982,text(IO,3976,3982).index('ISDone')<text(IO,3976,3982).index('BindingInvoice(ref Invo'))
    s(10,'Caller ref hydration precedes nested item result',IO,3976,4007,text(IO,3976,4007).index('BindingInvoice(ref Invo')<text(IO,3976,4007).index('frmInvoiceItems2.ShowDialog()')<text(IO,3976,4007).index('if (frmInvoiceItems2.ISDone)'))
    s(11,'Child field assigned from parent value before ShowDialog',IO,3983,4005,'frmInvoiceItems2.inv = Invo;' in text(IO,3983,4005))
    s(12,'Only final ref assignment is under item ISDone',IO,4002,4007,'if (frmInvoiceItems2.ISDone)' in text(IO,4002,4007) and 'Invo = frmInvoiceItems2.inv;' in text(IO,4002,4007))
    s(13,'Helper catch clears project error without typed rethrow result',IO,4008,4015,'ProjectData.ClearProjectError();' in text(IO,4008,4015) and 'throw;' not in text(IO,4008,4015))
    s(14,'Child starts with explicit ISDone false',IC,49,66,'ISDone = false;' in text(IC,49,66))
    s(15,'Child Close/Escape call CloseWithoutResult',IC,73,97,'e.Key == Key.Escape' in text(IC,73,97) and text(IC,73,97).count('CloseWithoutResult();')==2)
    s(16,'CloseWithoutResult replaces child inv then false and Close',IC,351,368,'inv = new InvoiceDGV();' in text(IC,351,368) and 'ISDone = false;' in text(IC,351,368))
    s(17,'Insert-all writes true without selected-ID projection',IC,105,116,'ISDone = true;' in text(IC,105,116) and 'InsertSelectedItems' not in text(IC,105,116),'P4-013')
    s(18,'Selected update and pruning use ItemId,not original LineRef',IC,299,348,'invoiceItem.ItemId == selectedRow.Item_ID' in text(IC,299,348) and 'selectedIds.Contains(i.ItemId)' in text(IC,299,348),'P4-013')
    s(19,'Sale reference assignment precedes LoadInvNo',SC,2746,2768,text(SC,2746,2768).index('Invoic.ReffNo = Invoic.InvCombinedId;')<text(SC,2746,2768).index('LoadInvNo();'))
    s(20,'Purchase LoadInvNo precedes GlobalID reference',PC,2207,2232,text(PC,2207,2232).index('this.LoadInvNo();')<text(PC,2207,2232).index('this.Invoic.ReffNo   = this.Invoic.InvGlobalID;'))
    def reads(slices):
        out=[]
        for p,a,z in slices:
            raw=(ROOT/p).read_bytes();assert 1<=a<=z<=len(raw.decode().splitlines())
            out.append(dict(path=p,start=a,end=z,sha256=hashlib.sha256(raw).hexdigest(),whole_local_file_selected=False,whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True))
        return out
    errors=[r['id'] for r in alg if not r['illustration_assertions_passed']]+[r['id'] for r in static if not r['documented_text_observation_matches']]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,new_root_ids=[],extended_existing_root_ids=[],existing_roots_deepened_without_registry_change=ROOTS,selected_source_paths=7,selected_contract_slices=24,context_slices_not_certified=11,whole_local_files_selected=0,illustration_count=len(alg),lexical_check_count=len(static),application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,actual_dialog_gesture_or_reference_aliasing_or_complete_hydration_proved=False,save_or_number_reservation_or_financial_loss_proved=False,application_remediation_performed=False,phase7C_started=False,phase8_authorized_or_started=False,all_callers_or_historical_bodies_certified=False,dirty_normal_returns_reader_snapshots_and_failures_are_supplied=True,child_field_reset_not_inferred_parent_ref_rollback=True,stop_before_CalcRows_and_bindings=True,prior_root_classifications_not_promoted=True,retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,bounded_source_reads_not_semantic_coverage=reads(SOURCE_SLICES),exploratory_source_reads_not_capability_certification=reads(EXPLORATORY_SLICES),illustrations=alg,static_lexical_contract_checks=static,errors=errors,limit=LIMIT)


if __name__=='__main__':
    result=build();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(1 if result['errors'] else 0)
