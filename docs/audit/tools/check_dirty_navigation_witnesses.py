#!/usr/bin/env python3
"""B29/R4m finite reference/control-flow illustrations, NOT C#/WPF/SQL tests.

Explicit dirty flags/counts, fresh chooser outcomes and normal CLR completion
are supplied. No DTO constructor, WPF schedule, provider behavior, financial
state, garbage collection, external references or saved loss is inferred.
One accepted-search guard-omission root159; no cancellation/failure recount.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
ENTRY = 'dda1eafab4188b00a7d6c3e435e7391bd0e09cda'
C = 'SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs'
X = 'SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml'
P = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs'
PX = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml'
S = 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
SX = 'SmartAuditERP/Form_WPF/frmInvSale.xaml'
I = 'SmartAuditERP/Class/InvoiceOper.cs'
SOURCE_SLICES = ((C,49,66,False),(C,89,131,False),(C,260,284,False),
 (X,1,16,False),(X,391,414,False),(P,36,88,False),(P,350,418,False),
 (P,481,548,False),(P,1531,1593,False),(P,2641,2662,False),(P,2738,2751,False),
 (PX,1,17,False),(PX,1322,1353,False),(S,66,95,False),(S,236,250,False),
 (S,1546,1679,False),(S,2563,2575,False),(S,2597,2657,False),
 (SX,1,17,False),(SX,1220,1234,False),(I,3219,3246,False),(I,3497,3508,False))
EV_PURCHASE = f'{P}:481-548;{P}:1531-1593;{P}:2641-2662;{PX}:1322-1353'
EV_SALE = f'{S}:1607-1679;{S}:2597-2657;{SX}:1220-1234'
EV_FINDING = EV_PURCHASE+';'+EV_SALE
EV_CHOOSER = f'{C}:49-66;{C}:89-131;{C}:260-284;{X}:1-16;{X}:391-414'
EV_READER = f'{I}:3219-3246;{I}:3497-3508;{P}:481-502;{S}:1643-1660'
EV_CLOSING = f'{P}:2738-2751;{PX}:1-17;{S}:66-95;{S}:236-250;{SX}:1-17'


def bounded_count(value):
    if type(value) is not int or not 0 <= value <= 12:
        raise ValueError('Explicit small non-Boolean UI-count fixture required')
    return value


def editor(value):
    if type(value) is not dict or set(value) != {'ref','is_new','is_updated','guard_rows'}:
        raise ValueError('Explicit editor-ref/flags/guard-count, not an external DTO')
    if type(value['ref']) is not str or re.fullmatch(r'fixture-DRAFT-[AB]',value['ref']) is None:
        raise ValueError('Only artificial editor-reference tokens')
    if any(type(value[k]) is not bool for k in ('is_new','is_updated')):
        raise ValueError('Dirty flags must be actual Booleans')
    bounded_count(value['guard_rows'])
    return copy.deepcopy(value)


def selected(value):
    if (type(value) is not dict or set(value) != {'done','gid'} or type(value['done']) is not bool
        or type(value['gid']) is not str or value['gid'] not in ('-1','fixture-DOC-A','fixture-DOC-B')):
        raise ValueError('Explicit bounded chooser result, not arbitrary identifiers/defaults')
    return copy.deepcopy(value)


def dirty_trigger(surface, value):
    value=editor(value)
    if surface not in ('purchase','sale'):
        raise ValueError('Only the two selected editor guards')
    threshold=0 if surface=='purchase' else 1
    return (value['guard_rows']>threshold and value['is_new']) or value['is_updated']


def trace(surface, command, before, result=None, answer=None, reader_outcome=None):
    """A finite boundary model, not a translation/interpreter of the application.

    guard_rows is explicitly the relevant UI collection count, NOT a claim
    about placeholder rows or every edit's IsUpdated propagation. No-op means
    no direct Navigate/CLR in the selected caller, NOT dialog/global purity.
    Reference replacement is the observation; no constructor fields modeled.
    """
    before=editor(before); dirty=dirty_trigger(surface,before)
    if command not in ('search','first','last','next','previous','new'):
        raise ValueError('Only explicitly selected commands')
    if answer not in (None,'Yes','No') or type(answer) not in (type(None),str):
        raise ValueError('Explicit finite guard answer required')
    guard=command!='search'; prompt=guard and dirty
    if prompt and answer not in ('Yes','No'):
        raise ValueError('A reached dirty prompt needs an explicitly supplied answer')
    if not prompt and answer is not None:
        raise ValueError('Cannot invent an answer to a prompt not reached')
    if command=='search':
        result=selected(result); proceed=result['done'] and result['gid']!='-1'
    else:
        if result is not None:
            raise ValueError('Non-search commands do not consume chooser results')
        proceed=not (prompt and answer=='No')
    nav=proceed and command!='new'; clear=proceed
    outcome=('boundary-only' if nav else 'not-reached') if reader_outcome is None else reader_outcome
    if type(outcome) is not str or outcome not in ('not-reached','boundary-only','supplied-success','supplied-no-rows','supplied-outer-failure'):
        raise ValueError('No arbitrary provider/failure execution or unknown outcome oracle')
    if (nav and outcome=='not-reached') or (not nav and outcome!='not-reached'):
        raise ValueError('Reader outcome contradicts the explicit control path')
    markers=[]
    if clear:
        markers=(['replace-editor-reference','clear-independent-view','reset-new-editor'] if surface=='purchase'
                 else ['detach-view-source','replace-editor-reference','reset-new-editor'])
    null=nav and outcome in ('supplied-no-rows','supplied-outer-failure')
    return dict(surface=surface,command=command,dirty_condition_if_checked=dirty,
      dirty_guard_called=guard,prompt_branch_reached=prompt,navigate_called=nav,clear_called=clear,
      editor_reference_replaced_before_reader=clear,clear_markers=markers,reader_boundary_reached=nav,
      reader_outcome_supplied=outcome,header_gid_assignment_only=(result['gid'] if command=='search' else 'fixture-DOC-B') if nav and outcome=='supplied-success' else None,
      reader_returned_null_in_supplied_case=null,caller_followup_fresh_reset_attempted=null,
      editor_ref_after_boundary='fixture-RESET-2' if null else ('fixture-RESET-1' if clear else before['ref']),
      old_editor_ref_still_current=not clear,constructor_fields_or_remaining_references_modeled=False)


def collect():
    texts={}; reads=[]
    for path,start,end,whole in SOURCE_SLICES:
        raw=(ROOT/path).read_bytes(); lines=raw.decode('utf-8',errors='strict').splitlines()
        if not 1<=start<=end<=len(lines) or whole:
            raise ValueError('B29 bounded-only source range changed:'+path)
        texts.setdefault(path,lines)
        reads.append(dict(path=path,start=start,end=end,whole_local_file_selected=False,
          sha256=hashlib.sha256(raw).hexdigest(),encoding='strict-utf-8',whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True))
    get=lambda p,a,b:'\n'.join(texts[p][a-1:b])
    updated=dict(ref='fixture-DRAFT-A',is_new=False,is_updated=True,guard_rows=2)
    fresh=dict(ref='fixture-DRAFT-B',is_new=True,is_updated=False,guard_rows=1)
    clean=updated|dict(is_updated=False)
    yes=dict(done=True,gid='fixture-DOC-B'); no=dict(done=False,gid='-1')
    cases=[]
    def case(title,evidence,actual,expected,limit):
        cases.append(dict(id=f'ALG7B29-{len(cases)+1:02d}',title=title,finding_ids='P7-159',evidence=evidence,
          actual=copy.deepcopy(actual),expected=copy.deepcopy(expected),illustration_assertions_passed=actual==expected,
          source_application_executed=False,limit=limit))
    brief=lambda t:tuple(t[k] for k in ('dirty_condition_if_checked','dirty_guard_called','prompt_branch_reached','clear_called','old_editor_ref_still_current'))
    lim='Supplied dirty flags/UI-count and normal selected CLR completion; only editor-reference/control-flow boundary, not WPF events, DTO defaults, actual provider behavior or saved loss.'
    case('Purchase accepted search bypasses dirty guard',EV_PURCHASE,brief(trace('purchase','search',updated,yes)),(True,False,False,True,False),lim)
    case('Sale accepted search is the same guard-omission root',EV_SALE,brief(trace('sale','search',updated,yes)),(True,False,False,True,False),'Same159, not a second finding160. '+lim)
    case('New purchase with supplied one-row guard count also reaches reset',EV_PURCHASE,brief(trace('purchase','search',fresh,yes)),(True,False,False,True,False),lim)
    case('New sale uses explicitly supplied greater-than-one UI count',EV_SALE,brief(trace('sale','search',fresh|dict(guard_rows=2),yes)),(True,False,False,True,False),'No placeholder-row or IsUpdated propagation assumption. '+lim)
    case('Fresh not-done chooser does not directly call Navigate',EV_CHOOSER+';'+EV_PURCHASE+';'+EV_SALE,[brief(trace(s,'search',updated,no)) for s in ('purchase','sale')],[(True,False,False,False,True)]*2,'Fresh result/no prior acceptance is explicit. This is not a global no-side-effect or WPF Close/Hide guarantee.')
    case('Done with minus-one sentinel is rejected by both callers',EV_PURCHASE+';'+EV_SALE,[brief(trace(s,'search',updated,dict(done=True,gid='-1'))) for s in ('purchase','sale')],[(True,False,False,False,True)]*2,lim)
    case('Guarded purchase first with No retains current editor',EV_PURCHASE,brief(trace('purchase','first',updated,answer='No')),(True,True,True,False,True),'Existing positive guard control, not a newly implemented remedy. '+lim)
    case('Guarded sale last with No retains current editor',EV_SALE,brief(trace('sale','last',updated,answer='No')),(True,True,True,False,True),lim)
    case('Guarded purchase next with explicit Yes can reset',EV_PURCHASE,brief(trace('purchase','next',updated,answer='Yes')),(True,True,True,True,False),'Approval concerns abandoning the editor, not eligibility/ACL/stock/save acceptance. '+lim)
    case('Guarded sale previous with explicit Yes can reset',EV_SALE,brief(trace('sale','previous',updated,answer='Yes')),(True,True,True,True,False),lim)
    case('Clean state does not require an unsaved-edit prompt',EV_PURCHASE+';'+EV_SALE,[brief(trace(s,'first',clean)) for s in ('purchase','sale')],[(False,True,False,True,False)]*2,'Does not assert all navigation must always prompt. No dirty-classification completeness certified.')
    success=trace('purchase','search',updated,yes,reader_outcome='supplied-success')
    case('Supplied successful header assignment occurs after old-ref replacement',EV_PURCHASE+';'+EV_READER,(success['editor_ref_after_boundary'],success['header_gid_assignment_only'],success['old_editor_ref_still_current']),('fixture-RESET-1','fixture-DOC-B',False),'Header assignment only, NOT complete BindingInvoice hydration/render/save; replacement object is filled, not assumed to be a new target object. '+lim)
    empty=trace('purchase','search',updated,yes,reader_outcome='supplied-no-rows')
    case('Supplied no-row reader reaches followup reset, not old-state restore',EV_READER+';'+EV_PURCHASE,(empty['reader_returned_null_in_supplied_case'],empty['caller_followup_fresh_reset_attempted'],empty['old_editor_ref_still_current']),(True,True,False),'Finite null-return boundary from source; no no-row SQL result observed. No extra failure finding or046 extension.')
    fail=trace('sale','search',updated,yes,reader_outcome='supplied-outer-failure')
    case('Supplied outer failure also reaches null/fresh-reset boundary',EV_READER+';'+EV_SALE,(fail['reader_returned_null_in_supplied_case'],fail['caller_followup_fresh_reset_attempted'],fail['old_editor_ref_still_current']),(True,True,False),'Stipulated failure, not induced SQL/provider or a failure-atomicity acceptance test. Root159 already exists on success.')
    case('Guarded New with No declines reset in both editors',f'{P}:1571-1593;{S}:1662-1679;{S}:2563-2575',[brief(trace(s,'new',updated,answer='No')) for s in ('purchase','sale')],[(True,True,True,False,True)]*2,lim)
    cancelled=trace('sale','search',updated,no); retry=trace('sale','search',updated,yes)
    case('A fresh cancel then accepted retry does not supply abandon approval',EV_CHOOSER+';'+EV_SALE,(cancelled['clear_called'],retry['dirty_guard_called'],retry['clear_called']),(False,False,True),'Two explicit result invocations, not a WPF reopen/default-retention schedule. Cancel is not reclassified as a failed acceptance.')
    lexical=[]
    def textcase(title,evidence,condition,limit=lim):
        lexical.append(dict(id=f'ST7B29-{len(lexical)+1:02d}',title=title,finding_ids='P7-159',evidence=evidence,documented_text_observation_matches=bool(condition),source_application_executed=False,limit='Lexical observation only. '+limit))
    for surface,path in (('purchase',P),('sale',S)):
        t=get(path,2641,2662 if path==P else 2657)
        textcase(surface+' accepted-search caller has done/GID but no CheckBeforeClear',f'{path}:2641-'+('2662' if path==P else '2657'),all(x in t for x in ('new frmInvoiceSrch()','frm.ShowDialog();','frm.ISDone','frm.InvGlobalID','Navigate(')) and 'CheckBeforeClear' not in t)
    textcase('Purchase own XAML wires the selected search button',f'{PX}:1322-1353','Click="btnInvSrch_Click_1"' in get(PX,1322,1353) and 'Click="btnFirst_Click"' in get(PX,1322,1353))
    textcase('Sale own XAML wires search among navigation buttons',f'{SX}:1220-1234',all('Click="'+n+'"' in get(SX,1220,1234) for n in ('btnFirst_Click','btnPrevious_Click','btnInvSrch_Click','btnNext_Click','btnLast_Click')))
    for path,a,b,clr,reader in ((P,481,502,'this.CLR();','InvoiceOper.BindingInvoice(ref this.Invoic, sqlStr);'),(S,1643,1660,'CLR();','InvoiceOper.BindingInvoice(ref Invoic, sqlStr);')):
        t=get(path,a,b);textcase('Navigate clears before reader without a dirty guard',f'{path}:{a}-{b}',t.index(clr)<t.index(reader) and 'CheckBeforeClear' not in t)
    t=get(P,1531,1569)
    textcase('Purchase CLR replaces editor and explicitly clears independent view',f'{P}:1531-1569',t.index('this.Invoic = new InvoiceDGV();')<t.index('_invoiceItems.Clear();')<t.index('this.ResetInvoice();') and 'CheckBeforeClear' not in t)
    t=get(S,1607,1641)
    textcase('Sale CLR detaches binding and replaces editor',f'{S}:1607-1641',t.index('GridControl1.ItemsSource = null;')<t.index('Invoic = new InvoiceDGV();')<t.index('ResetInvoice();') and 'CheckBeforeClear' not in t)
    textcase('Purchase existing guard uses positive collection count or updated flag',f'{P}:1571-1587',all(x in get(P,1571,1587) for x in ('_invoiceItems.Count > 0 && this.Invoic.ISNew','this.Invoic.IsUpdated','MessageBoxResult.No')))
    textcase('Sale existing guard uses UI count greater than one or updated flag',f'{S}:1662-1679',all(x in get(S,1662,1679) for x in ('GridControl1.Items.Count > 1 && Invoic.ISNew','Invoic.IsUpdated','MessageBoxResult.No')))
    textcase('Four neighboring purchase navigation commands invoke the guard',f'{P}:504-548',get(P,504,548).count('CheckBeforeClear()')==4)
    textcase('Four neighboring sale navigation commands invoke the guard',f'{S}:2597-2639',get(S,2597,2639).count('CheckBeforeClear()')==4)
    textcase('Local chooser constructor explicitly initializes fresh not-done/sentinel',f'{C}:49-66','ISDone       = false;' in get(C,49,66) and 'InvGlobalID  = "-1";' in get(C,49,66))
    textcase('Ordinary selection handlers assign done and identity; own events wired',EV_CHOOSER,all(x in get(C,89,116)+get(C,267,284) for x in ('ISDone      = true;','InvGlobalID = row.InvGlobalID;')) and 'MouseDoubleClick="dgvItems_MouseDoubleClick"' in get(X,391,414) and 'KeyDown="Window_KeyDown"' in get(X,1,16))
    t=get(C,89,131)
    textcase('Fresh close/cancel does not itself set acceptance; parent guards are Closing handlers',EV_CHOOSER+';'+EV_CLOSING,'Key.Escape) Close();' in t and 'ISDone' not in get(C,123,131) and 'Closing="frmSalePurch_FormClosing"' in get(PX,1,17) and 'Closing="Window_Closing"' in get(SX,1,17) and 'e.Cancel' in get(P,2738,2751)+get(S,236,250),'No claim about WPF child/parent event order or complete dialog/global side effects; Close button also touches ReturnYearPreviews/connection-string globals.')
    t=get(I,3219,3246);tail=get(I,3497,3508)
    textcase('Reader assigns header GID on HasRows and null on no-row/outer failure',EV_READER,'if (sqlDataReader.HasRows)' in t and 'Invo.InvGlobalID = Conversions.ToString(sqlDataReader["InvGlobalID"]);' in t and tail.count('Invo = null;')==2,'Only selected head/tail, not complete reader/DTO/body acceptance; provider outcomes stipulated.')
    errors=[r['id'] for r in cases if r['illustration_assertions_passed'] is not True]+[r['id'] for r in lexical if r['documented_text_observation_matches'] is not True]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',
      method='Strict source hashes/lexical observations and finite supplied dirty-state/reference-boundary illustrations; never C#/WPF/.NET/SQL execution',
      application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,application_remediation_performed=False,
      phase7C_started=False,phase8_authorized_or_started=False,all_callers_or_external_DTOs_body_reviewed=False,
      actual_WPF_event_order_or_count_claimed=False,dirty_flag_propagation_or_constructor_defaults_assumed=False,
      provider_failure_observed=False,database_commit_or_saved_loss_claimed=False,external_references_or_GC_modeled=False,
      erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,
      B_R4m_bounded_not_whole7B_closure=True,unresolved_external_contracts_and_explicit_splits_retained=True,
      selected_paths_strict_utf8_decode=True,prior015_046_061_091_132_148_151_155_158_not_recounted=True,
      new_root_ids=['P7-159'],extended_existing_root_ids=[],illustration_count=len(cases),lexical_check_count=len(lexical),
      selected_source_paths=len({r[0] for r in SOURCE_SLICES}),whole_local_files_selected=0,source_read_slice_count=len(reads),
      retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
      unadjudicated_source_leads_not_additional_findings=['other Navigate callers/fields/writers/output and full reader/DTO','IsUpdated/placeholder classification and WPF event ordering','period/postponed/quoting/return/eligibility/failure policies','Product/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome and external contracts'],
      bounded_source_reads_not_semantic_coverage=reads,illustrations=cases,static_lexical_contract_checks=lexical,errors=errors)


if __name__=='__main__':
    result=collect();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errors']))
