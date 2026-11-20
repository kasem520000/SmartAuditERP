#!/usr/bin/env python3
"""B30/R4n finite import-return illustrations, NOT C#/WPF/SQL execution.

The child starts not-done/-1. Only Navigate is conditional in the selected
callers; conversion follows any NORMAL dialog return. Non-null editor/items,
ordinary setter completion, candidate number or number-failure boundary and
accepted Navigate's returned editor are explicit supplied fixtures. Nothing
infers WPF chrome/Close bool?, SDK defaults, event reentrancy, hydration, SQL
success, fresh GlobalID, save, lost money, stock movement or operational safety.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
ENTRY = '3589d23a26438300d631790487eafe3aaddef7fb'
C = 'SmartAuditERP/Form_WPF/frmImportInvoice.xaml.cs'
X = 'SmartAuditERP/Form_WPF/frmImportInvoice.xaml'
P = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs'
PX = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml'
S = 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
SX = 'SmartAuditERP/Form_WPF/frmInvSale.xaml'
I = 'SmartAuditERP/Class/InvoiceOper.cs'
SOURCE_SLICES = ((C,1,419,True),(X,1,449,True),
 (P,281,298,False),(P,445,475,False),(P,481,502,False),
 (P,1531,1593,False),(P,2558,2577,False),(PX,1383,1384,False),
 (S,558,570,False),(S,1447,1493,False),(S,1607,1679,False),
 (S,3348,3373,False),(SX,1183,1183,False),(I,2789,2808,False))
EV_PURCHASE = f'{P}:2558-2577;{P}:281-298;{P}:445-475;{PX}:1383-1384'
EV_SALE = f'{S}:3348-3373;{S}:558-570;{S}:1447-1493;{SX}:1183-1183'
EV_CHILD = f'{C}:49-61;{C}:371-389;{X}:1-14;{X}:398-413'
EV_NUMBER = f'{P}:281-298;{S}:558-570;{I}:2789-2808'
EV_GUARD = f'{P}:481-502;{P}:1531-1593;{S}:1607-1679'
EV_FINDING = EV_PURCHASE+';'+EV_SALE+';'+EV_CHILD
EV_EXTENSION = f'{P}:2558-2577;{PX}:1383-1384;{S}:3348-3373;{SX}:1183-1183;{C}:49-61;{C}:371-389;{X}:398-413'


def small_int(value, low=0, high=999):
    if type(value) is not int or not low <= value <= high:
        raise ValueError('Explicit bounded integer; bool is NOT an integer fixture')
    return value


def editor(value):
    keys={'ref','gid','invoice_no','combined_id','note','is_new','is_printed',
          'is_updated','invoice_type','proc_type','impact','items'}
    if type(value) is not dict or set(value)!=keys:
        raise ValueError('Explicit scalar/reference fixture, NOT external InvoiceDGV')
    if value['ref'] not in ('fixture-EDITOR-A','fixture-EDITOR-B') or value['gid'] not in ('fixture-DOC-A','fixture-DOC-B'):
        raise ValueError('Only artificial reference and GlobalID tokens')
    if type(value['combined_id']) is not str or re.fullmatch(r'fixture-(?:COMBINED-[AB]|CODE-[PS]-[0-9]{1,3})',value['combined_id']) is None:
        raise ValueError('Only artificial combined-display identity tokens')
    if value['note'] not in ('fixture-note','') or type(value['note']) is not str:
        raise ValueError('No business text in fixtures')
    if any(type(value[k]) is not bool for k in ('is_new','is_printed','is_updated')):
        raise ValueError('Flags must be actual Booleans, not inferred defaults')
    small_int(value['invoice_no'],1)
    for k,allowed in (('invoice_type',(1,2,9)),('proc_type',(1,2,4)),('impact',(-1,0,1))):
        if type(value[k]) is not int or value[k] not in allowed:
            raise ValueError('Bounded supplied header domain:'+k)
    if type(value['items']) is not list or len(value['items'])>3:
        raise ValueError('Explicit non-null bounded item list required')
    lines=[]
    for item in value['items']:
        if (type(item) is not dict or set(item)!={'line','item_type','impact'}
                or type(item['line']) is not str or item['line'] not in ('fixture-L1','fixture-L2','fixture-L3')
                or type(item['item_type']) is not int or item['item_type'] not in (1,3,5)
                or type(item['impact']) is not int or item['impact'] not in (-1,0,1)):
            raise ValueError('Non-null finite item with explicit identity/type/impact required')
        lines.append(item['line'])
    if len(set(lines))!=len(lines):
        raise ValueError('No duplicate artificial line identity')
    return copy.deepcopy(value)


def result(value):
    if (type(value) is not dict or set(value)!={'done','gid'} or type(value['done']) is not bool
            or type(value['gid']) is not str or value['gid'] not in ('-1','fixture-DOC-A','fixture-DOC-B')):
        raise ValueError('Explicit bounded result, not arbitrary identifiers or bool? oracle')
    return copy.deepcopy(value)


def config(value):
    if (type(value) is not dict or set(value)!={'invoice_type','proc_type','impact','code'}
            or type(value['invoice_type']) is not int or value['invoice_type'] not in (1,2)
            or type(value['proc_type']) is not int or value['proc_type'] not in (1,2,4)
            or type(value['impact']) is not int or value['impact'] not in (-1,0,1)
            or value['code'] not in ('fixture-CODE-P-','fixture-CODE-S-')):
        raise ValueError('Explicit finite current-editor configuration required')
    return copy.deepcopy(value)


def number_result(value):
    if type(value) is not dict or value.get('kind') not in ('supplied-normal','supplied-failure'):
        raise ValueError('A candidate number or failure is SUPPLIED, never queried')
    if value['kind']=='supplied-normal':
        if set(value)!={'kind','value'}:raise ValueError('Exact number-result shape required')
        small_int(value['value'],1)
    elif set(value)!={'kind'}:
        raise ValueError('Failure result cannot invent a returned number')
    return copy.deepcopy(value)


def guard_denies(surface,state,rows,answer):
    state=editor(state);small_int(rows,0,3)
    if surface not in ('purchase','sale') or answer not in ('No','Yes') or type(answer) is not str:
        raise ValueError('Only selected adjacent guard and supplied answer')
    dirty=(rows>(0 if surface=='purchase' else 1) and state['is_new']) or state['is_updated']
    return bool(dirty and answer=='No')


def trace(surface,before,selected,current_config,number=None,after_navigate=None,dialog_return='normal'):
    """Finite field-assignment boundary; output stops BEFORE BindingControls events.

    after_navigate is an explicit non-null fixture for NORMAL accepted Navigate
    completion, not computed hydration. A supplied number failure stops after
    earlier assignments; no exception is induced in SQL, WPF or an SDK setter.
    Nonacceptance neither invokes Navigate nor replaces the current reference,
    but is NOT a no-op for the subsequent conversion tail.
    """
    before=editor(before);selected=result(selected);cfg=config(current_config)
    if surface not in ('purchase','sale') or dialog_return not in ('normal','supplied-showdialog-exception') or type(dialog_return) is not str:
        raise ValueError('Only finite surface and supplied dialog-return boundary')
    accepted=selected['done'] and selected['gid']!='-1';normal=dialog_return=='normal'
    if not normal:
        if number is not None or after_navigate is not None:
            raise ValueError('No downstream outcome for a dialog that did not return normally')
        return dict(surface=surface,accepted_result_not_abandon_decision=accepted,
          dialog_return_boundary=dialog_return,navigate_called=False,dirty_guard_called=False,
          tail_attempted=False,number_helper_called=False,later_flags_assigned=False,
          binding_controls_attempted=False,old_editor_ref_still_current=True,
          global_id_assigned_by_conversion_tail=False,state_at_pre_binding_boundary=before,
          scalar_or_item_changes_at_boundary=False,number_outcome_supplied='not-reached')
    supplied=number_result(number)
    if accepted:
        state=editor(after_navigate)
        if state['ref']==before['ref'] or state['gid']!=selected['gid']:
            raise ValueError('Accepted outcome must explicitly supply a different current editor and selected header GID')
    else:
        if after_navigate is not None:raise ValueError('Nonaccepted result cannot supply a Navigate outcome')
        state=copy.deepcopy(before)
    base=copy.deepcopy(state)
    state['invoice_type']=cfg['invoice_type'];state['proc_type']=cfg['proc_type']
    if surface=='sale':
        state['impact']=cfg['impact']
        for item in state['items']:
            item['impact']=0 if item['item_type'] in (3,5) else state['impact']
    state['note']=''
    completed=supplied['kind']=='supplied-normal'
    if completed:
        state['invoice_no']=supplied['value'];state['combined_id']=cfg['code']+str(supplied['value'])
        state['is_new']=True
        if surface=='sale':state['is_printed']=False;state['is_updated']=False
    return dict(surface=surface,accepted_result_not_abandon_decision=accepted,
      dialog_return_boundary=dialog_return,navigate_called=accepted,dirty_guard_called=False,
      tail_attempted=True,number_helper_called=True,later_flags_assigned=completed,
      binding_controls_attempted=completed,old_editor_ref_still_current=not accepted,
      global_id_assigned_by_conversion_tail=False,state_at_pre_binding_boundary=state,
      scalar_or_item_changes_at_boundary=state!=base,number_outcome_supplied=supplied['kind'])


def collect():
    texts={};reads=[]
    for path,start,end,whole in SOURCE_SLICES:
        raw=(ROOT/path).read_bytes();lines=raw.decode('utf-8',errors='strict').splitlines()
        if not 1<=start<=end<=len(lines) or (whole and (start,end)!=(1,len(lines))):
            raise ValueError('Declared local source depth/range changed:'+path)
        texts.setdefault(path,lines)
        reads.append(dict(path=path,start=start,end=end,whole_local_file_selected=whole,
          sha256=hashlib.sha256(raw).hexdigest(),encoding='strict-utf-8',
          whole_bytes_read_for_hash_and_line_index_not_whole_body_review=not whole))
    get=lambda p,a,b:'\n'.join(texts[p][a-1:b])
    old=dict(ref='fixture-EDITOR-A',gid='fixture-DOC-A',invoice_no=7,combined_id='fixture-COMBINED-A',
      note='fixture-note',is_new=False,is_printed=True,is_updated=True,invoice_type=1,proc_type=1,
      impact=1,items=[dict(line=f'fixture-L{n}',item_type=t,impact=1) for n,t in enumerate((1,3,5),1)])
    target=copy.deepcopy(old)|dict(ref='fixture-EDITOR-B',gid='fixture-DOC-B',combined_id='fixture-COMBINED-B')
    no=dict(done=False,gid='-1');yes=dict(done=True,gid='fixture-DOC-B')
    pcfg=dict(invoice_type=1,proc_type=1,impact=1,code='fixture-CODE-P-')
    scfg=dict(invoice_type=2,proc_type=1,impact=-1,code='fixture-CODE-S-')
    num=dict(kind='supplied-normal',value=41);fail=dict(kind='supplied-failure')
    cases=[]
    lim='Finite supplied non-null editor/items/config and normal setter completion; number outcome supplied, not SQL. Stops at assignments/binding attempt before WPF reentrancy; not financial/save/stock acceptance.'
    def case(title,evidence,actual,expected,limit=lim,root='P7-160'):
        cases.append(dict(id=f'ALG7B30-{len(cases)+1:02d}',title=title,finding_ids=root,evidence=evidence,
          actual=copy.deepcopy(actual),expected=copy.deepcopy(expected),illustration_assertions_passed=actual==expected,
          source_application_executed=False,limit=limit))
    def brief(t):
        st=t['state_at_pre_binding_boundary']
        return (t['navigate_called'],t['old_editor_ref_still_current'],st['note'],st['invoice_no'],st['is_new'],t['binding_controls_attempted'])
    p=trace('purchase',old,no,pcfg,num);s=trace('sale',old,no,scfg,num)
    case('Nonaccepted purchase blocks Navigate but converts current editor',EV_PURCHASE+';'+EV_CHILD,brief(p),(False,True,'',41,True,True))
    case('Nonaccepted sale has same160 plus explicit later flag writes',EV_SALE+';'+EV_CHILD,(brief(s),s['state_at_pre_binding_boundary']['is_printed'],s['state_at_pre_binding_boundary']['is_updated']),((False,True,'',41,True,True),False,False))
    case('Sale types3/5 become zero; other supplied item inherits current impact',EV_SALE,[(x['line'],x['impact']) for x in s['state_at_pre_binding_boundary']['items']],[('fixture-L1',-1),('fixture-L2',0),('fixture-L3',0)])
    case('Not-done with non-sentinel still does not Navigate yet executes tail',EV_PURCHASE,brief(trace('purchase',old,dict(done=False,gid='fixture-DOC-B'),pcfg,num)),(False,True,'',41,True,True))
    case('Done with sentinel also leaves unconditional tail reachable',EV_SALE,brief(trace('sale',old,dict(done=True,gid='-1'),scfg,num)),(False,True,'',41,True,True))
    a=trace('purchase',old,yes,pcfg,num,after_navigate=target)
    case('Accepted purchase import calls Navigate without dirty guard: existing159',EV_EXTENSION+';'+EV_GUARD,(a['navigate_called'],a['dirty_guard_called'],a['old_editor_ref_still_current']),(True,False,False),'Accepted importer is an additive source extension of159, not a second new root. Explicit normal Navigate outcome only. '+lim,root='P7-159')
    a=trace('sale',old,yes,scfg,num,after_navigate=target)
    case('Accepted sale import is the same159 extension',EV_EXTENSION+';'+EV_GUARD,(a['state_at_pre_binding_boundary']['ref'],a['state_at_pre_binding_boundary']['gid'],a['dirty_guard_called']),('fixture-EDITOR-B','fixture-DOC-B',False),root='P7-159')
    p=trace('purchase',old,no,pcfg,fail);s=trace('sale',old,no,scfg,fail)
    case('Supplied number failure does not undo earlier purchase note assignment',EV_PURCHASE+';'+EV_NUMBER,(brief(p),p['later_flags_assigned']),((False,True,'',7,False,False),False),'Earlier local writes precede number-helper call; supplied failure, not an induced provider exception. '+lim)
    case('Supplied sale number failure retains earlier item writes but not later flags',EV_SALE+';'+EV_NUMBER,(brief(s),[x['impact'] for x in s['state_at_pre_binding_boundary']['items']],s['state_at_pre_binding_boundary']['is_printed'],s['state_at_pre_binding_boundary']['is_updated']),((False,True,'',7,False,False),[-1,0,0],True,True))
    clean=old|dict(is_updated=False)
    case('A clean existing editor still reaches the nonaccepted conversion tail',EV_SALE,brief(trace('sale',clean,no,scfg,num)),(False,True,'',41,True,True),'Dirty state is not required for160; clean supplied state isolates cancellation/conversion from159. '+lim)
    empty=copy.deepcopy(old);empty['items']=[]
    case('An explicit empty sale item list does not prevent header conversion',EV_SALE,brief(trace('sale',empty,no,scfg,num)),(False,True,'',41,True,True))
    t=trace('purchase',old,no,pcfg,num)
    case('Number/combined ID rewrite is NOT a new GlobalID or SQL write',EV_PURCHASE+';'+EV_NUMBER,(t['state_at_pre_binding_boundary']['gid'],t['state_at_pre_binding_boundary']['combined_id'],t['global_id_assigned_by_conversion_tail']),('fixture-DOC-A','fixture-CODE-P-41',False))
    t=trace('sale',old,no,scfg,dialog_return='supplied-showdialog-exception')
    case('A dialog that does not return normally never reaches this tail',EV_SALE,(t['tail_attempted'],t['number_helper_called'],t['state_at_pre_binding_boundary']==old),(False,False,True),'Exception is a finite counter-control, not a WPF/provider failure reproduction. No claim that every cancellation returns normally.')
    same=old|dict(note='',is_new=True,invoice_no=41,combined_id='fixture-CODE-P-41')
    t=trace('purchase',same,no,pcfg,num)
    case('Assignments may be value-idempotent on an explicitly matching fixture',EV_PURCHASE,(t['tail_attempted'],t['scalar_or_item_changes_at_boundary']),(True,False),'160 is not a claim that every normal nonaccepted return visibly changes every object. '+lim)
    t=trace('purchase',old,no,pcfg,num)
    case('Purchase tail has no explicit print/update reset at this boundary',EV_PURCHASE,(t['state_at_pre_binding_boundary']['is_printed'],t['state_at_pre_binding_boundary']['is_updated']),(True,True),'Absence of those writes only within selected tail, not SDK setter effects or later binding events. '+lim)
    t=trace('sale',old|dict(proc_type=4,invoice_type=9),no,scfg,num)
    case('Supplied mismatching header type/process are replaced by current config',EV_SALE,(t['state_at_pre_binding_boundary']['invoice_type'],t['state_at_pre_binding_boundary']['proc_type']),(2,1),'No assumption that every real loaded editor starts mismatching current configuration. '+lim)
    first=trace('sale',old,no,scfg,num);second=trace('sale',first['state_at_pre_binding_boundary'],yes,scfg,num,after_navigate=target)
    case('Explicit nonaccept then accepted retry separates160 from159',EV_SALE+';'+EV_CHILD,(first['old_editor_ref_still_current'],first['scalar_or_item_changes_at_boundary'],second['navigate_called'],second['dirty_guard_called']),(True,True,True,False),'Two supplied function invocations, NOT a WPF reopen/event/default-retention schedule. '+lim,root='P7-160;P7-159')
    case('Adjacent New guard with supplied No blocks reset; not an import interceptor',EV_GUARD,[guard_denies(sf,old,2,'No') for sf in ('purchase','sale')],[True,True],'Existing source control with supplied flags/count/No, not MessageBox execution or proof Closing intercepts import.',root='P7-159')
    lexical=[]
    def textcase(title,ev,condition,limit=lim,root='P7-160'):
        lexical.append(dict(id=f'ST7B30-{len(lexical)+1:02d}',title=title,finding_ids=root,evidence=ev,
          documented_text_observation_matches=bool(condition),source_application_executed=False,limit='Lexical, not a C# parser or execution. '+limit))
    c=get(C,1,419);x=get(X,1,449);p=get(P,2558,2577);s=get(S,3348,3373)
    textcase('Explicit fresh child fields remain sentinel/not-done until accept',EV_CHILD,'public string InvGID = "-1";' in c and 'public bool isDone = false;' in c and len(re.findall(r'\bisDone\s*=\s*true\s*;',c))==1)
    textcase('Accept handler assigns GID and done before Close',f'{C}:371-389',c.index('InvGID = globalId;')<c.index('isDone = true;')<c.index('this.Close();'))
    textcase('Child own row button binds GID and invokes accept',f'{X}:398-413','Tag="{Binding InvGlobalId}"' in x and 'Click="BtnImport_Click"' in x)
    textcase('Whole local child has no Closing/closed/dialog-result acceptance override',f'{C}:1-419;{X}:1-449',not any(t in c+x for t in ('Closing=','Closed=','OnClosing','DialogResult','IsCancel=')),'Local absence only: inherited DevExpress/WPF chrome/normal-close bool? and actual event schedule are NOT proven; normal nonaccepted return is supplied.')
    textcase('Purchase own tools menu wires invoice import',f'{PX}:1383-1384','Click="StripImportInv_Click"' in get(PX,1383,1384))
    textcase('Sale own tools menu wires invoice import',f'{SX}:1183-1183','Click="StripImportInv_Click"' in get(SX,1183,1183))
    compact=lambda t:re.sub(r'\s+','',t)
    textcase('Purchase guard encloses Navigate only, closes before conversion',f'{P}:2558-2577',"this.Navigate($\"select*fromInvwhereInvGlobalID=N'{frm.InvGID}'\");}this.Invoic.InvoiceType=" in compact(p))
    textcase('Sale single guarded statement is Navigate; conversion follows',f'{S}:3348-3373',"Navigate(\"select*fromInvwhereInvGlobalID=N'\"+frm.InvGID+\"'\");Invoic.InvoiceType=" in compact(s))
    for path,t,a,b in ((P,p,2558,2577),(S,s,3348,3373)):
        textcase('Accepted '+('purchase' if path==P else 'sale')+' caller lacks CheckBeforeClear',f'{path}:{a}-{b}',all(z in t for z in ('new frmImportInvoice()','frm.ShowDialog();','frm.isDone','frm.InvGID','Navigate(')) and 'CheckBeforeClear' not in t,root='P7-159')
    textcase('Purchase note precedes number helper, ISNew and BindingControls',f'{P}:2558-2577',p.index('this.Invoic.InvNote')<p.index('this.LoadInvNo();')<p.index('this.Invoic.ISNew = true;')<p.index('this.BindingControls();'))
    textcase('Sale item-impact loop precedes note and number helper',f'{S}:3348-3373',s.index('foreach (var item in Invoic.InvoiceItems)')<s.index('Invoic.InvNote = "";')<s.index('LoadInvNo();') and 'item.ItemType == 3 || item.ItemType == 5' in s and 'item.InvertoryImpact = 0;' in s)
    textcase('Sale later flags follow number helper and precede binding',f'{S}:3348-3373',s.index('LoadInvNo();')<s.index('Invoic.ISNew = true;')<s.index('Invoic.IsPrinted = false;')<s.index('Invoic.IsUpdated = false;')<s.index('BindingControls();'))
    textcase('Both number helpers write InvoiceNo/combined ID and UI number',EV_NUMBER,all(all(z in get(path,a,b) for z in ('InvoiceOper.InvoiceNo(','InvCombinedId','txtNo.Text')) for path,a,b in ((P,281,298),(S,558,570))))
    allocator=get(I,2789,2808)
    textcase('Selected shared number helper reads MAX+1 with prefix fallback',f'{I}:2789-2808','ISNULL(MAX(id), 0)' in allocator and 'ExecuteScalar()' in allocator and 'num = Prefixe;' in allocator and not any(t in allocator for t in ('INSERT ','UPDATE ','DELETE ')),'Source SELECT/candidate calculation only; NOT executed allocation/reservation, no concurrency experiment or new GlobalID claim.')
    textcase('Both binding heads can publish number and cleared note',f'{P}:445-475;{S}:1447-1493',all(all(z in get(path,a,b) for z in ('txtNo.Text','InvoiceNo','txtNote.Text','InvNote')) for path,a,b in ((P,445,475),(S,1447,1493))),'Publication assignments/attempt only; binding events, rendering and final stable flags are not modeled.')
    textcase('Both Navigate bodies clear before BindingInvoice',EV_GUARD,all(get(path,a,b).index('CLR();')<get(path,a,b).index('InvoiceOper.BindingInvoice(') for path,a,b in ((P,481,502),(S,1643,1660))),root='P7-159')
    textcase('Existing New guard differs from unconditional import tail',EV_GUARD,'!this.CheckBeforeClear()' in get(P,1589,1593) and 'GridControl1.Items.Count > 1 && Invoic.ISNew' in get(S,1662,1679) and 'CheckBeforeClear' not in p+s,root='P7-159')
    errors=[r['id'] for r in cases if r['illustration_assertions_passed'] is not True]+[r['id'] for r in lexical if r['documented_text_observation_matches'] is not True]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',
      method='Strict UTF8 source hashes/lexical observations and finite supplied import-return/assignment fixtures, NOT application execution',
      application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,application_remediation_performed=False,
      phase7C_started=False,phase8_authorized_or_started=False,all_callers_or_external_DTOs_body_reviewed=False,
      actual_WPF_chrome_close_result_or_event_schedule_claimed=False,SDK_setter_defaults_or_reentrancy_modeled=False,
      provider_failure_observed=False,database_commit_or_saved_loss_claimed=False,new_GlobalID_allocated_or_SQL_write_claimed=False,
      erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,
      normal_nonaccepted_return_and_nonnull_editor_are_supplied=True,number_result_or_failure_is_supplied=True,
      B_R4n_bounded_not_whole7B_closure=True,unresolved_external_contracts_and_explicit_splits_retained=True,
      selected_paths_strict_utf8_decode=True,prior015_046_091_148_151_155_158_not_recounted=True,
      new_root_ids=['P7-160'],extended_existing_root_ids=['P7-159'],illustration_count=len(cases),lexical_check_count=len(lexical),
      selected_source_paths=len({r[0] for r in SOURCE_SLICES}),whole_local_files_selected=2,source_read_slice_count=len(reads),
      retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
      unadjudicated_source_leads_not_additional_findings=['other import/search/linked callers,fields,writers,outputs,branch and allowed-set','all SDK identity/collection/copy/defaults and binding reentrancy','number-failure and copy/load/outcome policies with financial/ACL/stock/save barriers','Product/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome,census455FE,currency/precision/templates'],
      bounded_source_reads_not_semantic_coverage=reads,illustrations=cases,static_lexical_contract_checks=lexical,errors=errors)


if __name__=='__main__':
    output=collect();print(json.dumps(output,ensure_ascii=False,indent=2));raise SystemExit(bool(output['errors']))
