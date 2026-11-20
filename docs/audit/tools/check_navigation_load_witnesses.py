#!/usr/bin/env python3
"""Inert B31/R4o navigation/read-outcome illustrations, NOT C#/SQL/WPF tests.

Only strict UTF-8 reads and finite Python fixture traces. The complete local
BindingInvoice method3219..3508 is selected, not its whole file, every helper,
DTO setter, provider, schema, collection default, event order or all callers.
No SQL/ERP imports, connections, dynamic execution, repair, saved-loss or GC.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]
ENTRY='038a18b74acb92c35a6172d4619fee5712424489'
P='SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs';S='SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
PX='SmartAuditERP/Form_WPF/frmInvPurch.xaml';SX='SmartAuditERP/Form_WPF/frmInvSale.xaml';O='SmartAuditERP/Class/InvoiceOper.cs'
SOURCE_SLICES=((P,281,298),(P,350,444),(P,445,548),(P,1531,1587),
 (S,558,570),(S,1447,1467),(S,1546,1679),(S,2597,2639),
 (PX,371,385),(PX,1337,1352),(SX,333,338),(SX,1220,1234),(O,2789,2808),(O,3219,3508))
EVIDENCE=';'.join(f'{p}:{a}-{z}' for p,a,z in SOURCE_SLICES)
READ_OUTCOMES=('empty','outer-failed-before-header','outer-failed-after-header','found','row-caught-nonnull')


def bounded_int(value,lo=0,hi=999):
    if type(value) is not int or not lo<=value<=hi:raise ValueError('Bounded exact int, not bool/coercion')
    return value


def editor(value):
    if value is None:return None
    if type(value) is not dict or set(value)!={'ref','gid','is_new','is_updated'}:raise ValueError('Exact supplied editor shape')
    if any(type(value[k]) is not bool for k in ('is_new','is_updated')):raise ValueError('Supplied strict flags')
    if any(type(value[k]) is not str or re.fullmatch('fixture-[A-Za-z0-9-]+',value[k]) is None for k in ('ref','gid')):raise ValueError('Fixture tokens only; no business identity')
    return copy.deepcopy(value)


def guard_denies(surface,original,view_count,decision):
    if surface not in ('purchase','sale'):raise ValueError('Selected surface only')
    original=editor(original);bounded_int(view_count)
    if decision not in ('Yes','No') or type(decision) is not str:raise ValueError('Explicit supplied Yes/No')
    if original is None:return False
    dirty=((view_count>(0 if surface=='purchase' else 1)) and original['is_new']) or original['is_updated']
    return dirty and decision=='No'


def trace(surface,command,original,reader_kind,reset_plan,view_count=2,decision='No',candidate=41):
    """Model ordering at supplied external boundaries, not a replacement reader.

    Each reset_plan entry supplies normal return or failure AT its number call;
    all preceding ordinary setters/controls/collections return. No constructor
    defaults, final event/UI state, schema health or target hydration inferred.
    """
    if surface not in ('purchase','sale') or command not in ('first','previous','next','last'):raise ValueError('Bounded toolbar entry')
    original=editor(original);bounded_int(candidate,1);bounded_int(view_count)
    if type(reset_plan) not in (list,tuple) or any(x not in ('normal','number-failed') or type(x) is not str for x in reset_plan):raise ValueError('Explicit finite reset outcomes')
    denied=guard_denies(surface,original,view_count,decision)
    if reader_kind is not None and reader_kind not in READ_OUTCOMES:raise ValueError('Supplied reader boundary kind')
    events=['guard-denied' if denied else 'guard-allows'];state=copy.deepcopy(original);allocations=0;resets=0;number_calls=0;reader_called=False;fallback=False;bind=False;escaped=False;temporary_target=False
    def allocate(label):
        nonlocal state,allocations
        allocations+=1;events.append(label+'.new-editor-ref')
        state=dict(ref=f'fixture-FRESH-{allocations}',gid='SDK-default-not-modeled',is_new=None,is_printed=None,number=None,target_completeness='not-established')
    def reset(label):
        nonlocal resets,number_calls,state,escaped
        if resets>=len(reset_plan):raise ValueError('Missing reached reset outcome')
        outcome=reset_plan[resets];resets+=1
        if surface=='sale':events.append(label+'.old-grid-source-unbound')
        allocate(label)
        if surface=='purchase':events.append(label+'.old-visible-list-cleared')
        number_calls+=1;events.append(label+'.number-boundary')
        if outcome=='number-failed':
            events.append(label+('.number-failure-swallowed-by-CLR' if surface=='purchase' else '.number-failure-escapes-CLR'))
            escaped=surface=='sale';return not escaped
        state.update(is_new=True,is_printed=False,number=candidate)
        events.append(label+'.explicit-reset-flags-after-normal-number')
        return True
    if not denied:
        proceed=True
        if original is not None:proceed=reset('pre-read')
        if proceed:
            if reader_kind is None:raise ValueError('Reached reader requires supplied outcome')
            if original is None and reader_kind in ('found','row-caught-nonnull'):raise ValueError('Non-null reader target requires working editor')
            reader_called=True;events.append('reader.'+reader_kind)
            if reader_kind in ('empty','outer-failed-before-header','outer-failed-after-header'):
                temporary_target=reader_kind=='outer-failed-after-header';state=None;events.append('reader.ref-null')
            else:
                state.update(gid='fixture-DOC-B',is_new=False,is_printed=True,target_completeness='supplied-found-boundary-not-full-hydration' if reader_kind=='found' else 'per-row-caught-partial-not-proven-complete')
            if state is None:
                fallback=True;allocate('null-branch');reset('fallback')
            else:bind=True;events.append('nonnull.branch-BindingDGV-and-controls-attempted')
        elif reader_kind is not None:raise ValueError('Unreached reader outcome cannot be supplied')
    elif reader_kind is not None:raise ValueError('Guard denied; no reader outcome input allowed')
    if resets!=len(reset_plan):raise ValueError('Unreached reset outcomes cannot be supplied')
    return dict(surface=surface,command=command,guard_denied=denied,reader_called=reader_called,reader_kind=reader_kind,
      reset_cycles=resets,explicit_new_expressions_reached=allocations,number_helper_calls=number_calls,
      fallback_reached=fallback,binding_attempted=bind,exception_escaped=escaped,
      temporary_target_header_then_outer_null=temporary_target,events=events,state_at_source_boundary=state,
      original_editor_ref_still_current=original is not None and state is not None and state['ref']==original['ref'],
      supplied_target_hydration_not_executed=True,stable_post_event_state_claimed=False,application_code_executed=False)


def build():
    source={};reads=[]
    for path,a,z in SOURCE_SLICES:
        raw=(ROOT/path).read_bytes();ls=raw.decode('utf8',errors='strict').splitlines();assert 1<=a<=z<=len(ls)
        source[(path,a,z)]='\n'.join(ls[a-1:z])
        reads.append(dict(path=path,start=a,end=z,encoding='strict-utf-8',sha256=hashlib.sha256(raw).hexdigest(),whole_local_file_selected=False,whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True))
    text=lambda p,a,z:source[(p,a,z)]
    pn=text(P,445,548);sn=text(S,1546,1679);pr=text(P,1531,1587);rd=text(O,3219,3508)
    lexical=[
      ('purchase-four-toolbar-clicks',all(f'Click="btn{x}_Click"' in text(PX,1337,1352) for x in ('First','Previous','Next','Last')),f'{PX}:1337-1352'),
      ('sale-four-toolbar-clicks',all(f'Click="btn{x}_Click"' in text(SX,1220,1234) for x in ('First','Previous','Next','Last')),f'{SX}:1220-1234'),
      ('purchase-toolbar-has-guard',pn.count('!this.CheckBeforeClear()')==4,f'{P}:504-546'),
      ('sale-toolbar-has-guard',text(S,2597,2639).count('!CheckBeforeClear()')==4,f'{S}:2597-2639'),
      ('purchase-clears-before-reader',pn.index('this.CLR();')<pn.index('InvoiceOper.BindingInvoice(ref this.Invoic, sqlStr)'),f'{P}:481-502'),
      ('sale-clears-before-reader',sn.index('if (Invoic != null) CLR();')<sn.index('InvoiceOper.BindingInvoice(ref Invoic, sqlStr)'),f'{S}:1643-1660'),
      ('purchase-CLR-replaces-and-clears-before-reset',pr.index('this.Invoic = new InvoiceDGV();')<pr.index('_invoiceItems.Clear();')<pr.index('this.ResetInvoice();')<pr.index('catch { }'),f'{P}:1531-1568'),
      ('sale-CLR-reset-outside-local-catch',sn.index('catch (Exception ex)')<sn.index('GridControl1.ItemsSource = null;')<sn.index('Invoic = new InvoiceDGV();')<sn.index('ResetInvoice();'),f'{S}:1607-1641'),
      ('reader-void-ref-contract','public static void BindingInvoice(ref InvoiceDGV Invo, string sqlstr)' in rd,f'{O}:3219-3236'),
      ('reader-no-row-sets-null',bool(re.search(r'else\s*\{\s*Invo = null;\s*\}\s*\}\s*catch \(Exception projectError5\)',rd)),f'{O}:3496-3508'),
      ('reader-outer-exception-same-null',bool(re.search(r'catch \(Exception projectError5\).*Invo = null;',rd,re.S)),f'{O}:3502-3508'),
      ('row-local-exception-is-not-outer-null',bool(re.search(r'catch \(Exception projectError4\)\s*\{\s*ProjectData.SetProjectError\(projectError4\);\s*ProjectData.ClearProjectError\(\);\s*\}',rd)),f'{O}:3476-3487'),
      ('purchase-null-branch-allocates-and-clears',bool(re.search(r'else\s*\{\s*this.Invoic = new InvoiceDGV\(\);\s*this.CLR\(\);',pn)),f'{P}:481-502'),
      ('sale-null-branch-allocates-and-clears',bool(re.search(r'else\s*\{\s*Invoic = new InvoiceDGV\(\);\s*CLR\(\);',sn)),f'{S}:1643-1660'),
      ('purchase-reset-number-precedes-new-flag',text(P,350,444).index('this.LoadInvNo();')<text(P,350,444).index('this.Invoic.ISNew         = true;'),f'{P}:350-407'),
      ('sale-reset-number-precedes-new-flag',sn.index('LoadInvNo();')<sn.index('Invoic.ISNew = true;'),f'{S}:1546-1605'),
      ('purchase-number-publishes-candidate','this.txtNo.Text         = this.Invoic.InvoiceNo.ToString();' in text(P,281,298),f'{P}:281-298'),
      ('sale-number-publishes-candidate','txtNo.Text = Invoic.InvoiceNo.ToString();' in text(S,558,570),f'{S}:558-570'),
      ('candidate-is-MAX-plus-one-not-reservation','MAX(id)' in text(O,2789,2808) and '.ExecuteScalar()' in text(O,2789,2808),f'{O}:2789-2808'),
      ('InvoiceNo-really-reads-id-not-a-key-domain-defect','Invo.InvoiceNo = checked((int)Math.Round(Convert.ToDouble(Operators.ConcatenateObject("", sqlDataReader["id"]))));' in rd,f'{O}:3271-3285')]
    illustrations=[];old=dict(ref='fixture-EDITOR-A',gid='fixture-DOC-A',is_new=False,is_updated=False)
    def add(label,sf,kind,plan,expected,original=old,decision='No',command='next'):
        t=trace(sf,command,original,kind,plan,decision=decision)
        ok=all(t[k]==value and type(t[k]) is type(value) for k,value in expected.items())
        illustrations.append(dict(id=f'ALG7B31-{len(illustrations)+1:02d}',label=label,finding_ids='P7-161' if not t['guard_denied'] else 'H7B31-03',evidence=EVIDENCE,
          supplied_inputs=dict(surface=sf,command=command,original=original,reader_kind=kind,reset_plan=plan,view_count=2,decision=decision,candidate_number=41),trace=t,expected=expected,illustration_assertions_passed=ok,source_application_executed=False,
          limit='Finite fixture ordering only. Ordinary preceding dependencies, reset-number outcome and reader boundary supplied; no SDK defaults/SQL rows/provider failure,stable events,saved loss or GC inferred.'))
    for kind in ('empty','outer-failed-before-header','outer-failed-after-header'):
        for sf in ('purchase','sale'):add(kind,sf,kind,['normal','normal'],dict(reset_cycles=2,number_helper_calls=2,fallback_reached=True,original_editor_ref_still_current=False,binding_attempted=False,exception_escaped=False))
    for kind in ('found','row-caught-nonnull'):
        for sf in ('purchase','sale'):add(kind,sf,kind,['normal'],dict(reset_cycles=1,fallback_reached=False,binding_attempted=True,original_editor_ref_still_current=False))
    dirty=old|dict(is_updated=True)
    for sf in ('purchase','sale'):add('guard-No-stops-before-first-write',sf,None,[],dict(guard_denied=True,reader_called=False,reset_cycles=0,original_editor_ref_still_current=True),original=dirty)
    for sf in ('purchase','sale'):add('guard-Yes-is-not-reader-success',sf,'empty',['normal','normal'],dict(guard_denied=False,reader_called=True,fallback_reached=True,original_editor_ref_still_current=False),original=dirty,decision='Yes')
    add('purchase-first-number-failure-swallowed', 'purchase','empty',['number-failed','normal'],dict(reader_called=True,fallback_reached=True,exception_escaped=False,reset_cycles=2))
    add('sale-first-number-failure-escapes-before-reader','sale',None,['number-failed'],dict(reader_called=False,fallback_reached=False,exception_escaped=True,reset_cycles=1,original_editor_ref_still_current=False))
    for sf in ('purchase','sale'):add('fallback-number-failure',sf,'empty',['normal','number-failed'],dict(reader_called=True,fallback_reached=True,exception_escaped=sf=='sale',reset_cycles=2))
    for sf in ('purchase','sale'):add('null-original-no-old-invoice-to-preserve',sf,'empty',['normal'],dict(reader_called=True,reset_cycles=1,fallback_reached=True,number_helper_calls=1),original=None,command='first')
    checks=[dict(id=f'ST7B31-{i:02d}',boundary=n,documented_text_observation_matches=ok,evidence=ev,finding_ids='P7-161',source_application_executed=False,limit='Lexical observation in selected static source,not C#/VB compilation or provider/SDK semantics.') for i,(n,ok,ev) in enumerate(lexical,1)]
    errors=[r['id'] for r in illustrations if r['illustration_assertions_passed'] is not True]+[r['id'] for r in checks if r['documented_text_observation_matches'] is not True]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,new_root_ids=['P7-161'],extended_existing_root_ids=[],illustration_count=len(illustrations),lexical_check_count=len(checks),selected_source_paths=5,source_read_slice_count=14,whole_local_files_selected=0,whole_reader_method_selected_lines=290,bounded_source_reads_not_semantic_coverage=reads,illustrations=illustrations,static_lexical_contract_checks=checks,errors=errors,
      application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,provider_failure_observed=False,SDK_defaults_or_row_hydration_executed=False,stable_post_event_state_claimed=False,database_commit_or_saved_loss_claimed=False,original_reference_release_or_GC_claimed=False,application_remediation_performed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,
      reset_and_reader_outcomes_are_supplied=True,per_row_caught_exception_is_not_outer_null=True,guard_No_prevents_first_write=True,all332_historical_bodies_or_all_callers_reviewed=False,
      retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
      unadjudicated_leads_not_extra_findings=['Per-row swallowed errors and partial hydration need independent source/schema/DTO chain;not another finding here.','Connection/reader ownership not measured;no leak claim.','Dirty-notification propagation not settled;159 remains unchanged.','Actual provider,SDK constructor/collection,setter,binding and schema outcomes remain external contracts.'])


if __name__=='__main__':
    data=build();print(json.dumps(data,ensure_ascii=False,indent=2));raise SystemExit(1 if data['errors'] else 0)
