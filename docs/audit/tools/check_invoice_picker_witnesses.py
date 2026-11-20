#!/usr/bin/env python3
"""B36/R4t inert request/picker-result witnesses. NOT ERP/WPF/SQL/SDK tests.

Reread local picker C#698 already whole in B27/B28;selected own-XAML/helper
slices only. New cross-caller contract,not newly completed files or new roots.
Rows,selection indices,modal returns,connection tokens and failure boundaries
are supplied. Local InvoiceSrchRow auto-properties known;InvoiceDGV/SDK,enum
mapping,ConnObj implementation,framework Close/Hide/chrome and Loaded order
unresolved. Return button/previous-year controls do not certify those commands.
Zero roots/extensions;ALL335/raw336 unchanged;P7-157/160 documentary deepening.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
ENTRY='9769e29b8ce34f720fd660a475800f5c3bf9b7fa'
CS='SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs';X='SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml';IO='SmartAuditERP/Class/InvoiceOper.cs'
SOURCE_SLICES=((CS,22,32),(CS,49,66),(CS,73,86),(CS,88,116),(CS,123,132),
 (CS,261,284),(CS,310,334),(CS,336,345),(CS,378,408),(CS,492,519),
 (CS,567,596),(CS,674,698),(IO,3941,3951),(IO,3976,3985),
 (IO,4002,4013),(X,1,14),(X,172,187),(X,229,238),(X,391,420),(X,524,546))
CONTEXT_SLICES=((CS,138,254),(CS,286,303),(CS,348,377),(CS,603,619),(CS,621,636),(IO,3952,3975))
WHOLE_REREADS=((CS,1,698),)


def flag(v):
    if type(v) is not bool:raise ValueError('supplied exact bool')
    return v


def number(v,minimum=0,maximum=64):
    if type(v) is not int or not minimum<=v<=maximum:raise ValueError('bounded integer,not bool')
    return v


def token(v,empty=False):
    if type(v) is not str or len(v)>80 or (not v and not empty) or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for c in v):raise ValueError('inert ASCII token only,no real path/query/phone')
    return v


def row(gid='doc-A',proc=1,pay=1):return dict(gid=token(gid,empty=True),proc=number(proc),pay=number(pay,-1))


def checked_row(r):
    if type(r) is not dict or set(r)!={'gid','proc','pay'}:raise ValueError('exact local payload gid/proc/pay only')
    return row(r['gid'],r['proc'],r['pay'])


def rows_input(rows):
    if type(rows) is not list or len(rows)>64:raise ValueError('bounded supplied row models')
    return [checked_row(r) for r in rows]


def fresh():
    return dict(done=False,gid='-1',proc=1,pay=1,inv_type=6,events=[],lookup_called=False,
                modal_result_not_inferred=True,source_application_executed=False)


def request(proc=1,inv_type=1,branch=1,before_conn='conn-A',later_conn='conn-A',credit_hint=0):
    proc,inv_type,branch,credit_hint=[number(v) for v in (proc,inv_type,branch,credit_hint)]
    before_conn,later_conn=token(before_conn),token(later_conn)
    return dict(proc=proc,inv_type=inv_type,branch=branch,credit_hint=credit_hint,
        constructor_connection_token=before_conn,later_global_connection_token=later_conn,
        events=['InitializeComponent-called','ConnObj-called-before-caller-inputs','local-defaults-set',
                'caller-permission-settings-calls-unresolved','caller-ProcType-assigned','caller-InvType-branch-assigned','ShowDialog-requested'],
        immutable_request_object_in_source=False,enum_numeric_mapping_proved=False,
        connection_content_or_liveness_or_ownership_proved=False)


def source_row(gid='doc-A',kind=1,proc=1,branch=1,deleted=False):
    return dict(gid=token(gid,empty=True),kind=number(kind),proc=number(proc),branch=number(branch),deleted=flag(deleted))


def query_select(sources,req):
    if type(sources) is not list or len(sources)>64:raise ValueError('bounded symbolic source')
    for s in sources:
        if type(s) is not dict or set(s)!={'gid','kind','proc','branch','deleted'}:raise ValueError('symbolic predicate source fields')
        source_row(**s)
    wanted,proc,branch=[number(req[k]) for k in ('inv_type','proc','branch')]
    # Documentary predicate projection,NOT SQL/DataView/provider evaluation.
    return [dict(s) for s in sources if not s['deleted'] and (wanted==14 or s['branch']==branch)
            and s['proc']==proc and (s['kind']==wanted if wanted==23 else s['kind'] in {20,wanted})]


def local_proc_filter(master,selected_index):
    selected_index=number(selected_index,-1);master=rows_input(master)
    return [dict(r) for r in master if selected_index<=0 or r['proc']==selected_index]


def accept(route,rows,index=-1,selected=None,tag=None,lookup='absent',previous_year=False):
    rows=rows_input(rows);index=number(index,-1);previous_year=flag(previous_year)
    selected=None if selected is None else checked_row(selected);tag=None if tag is None else checked_row(tag)
    if route not in {'enter','double','escape','close-button','return-button'} or lookup not in {'found','absent','failed'}:raise ValueError('explicit local route/bounded lookup only')
    s=fresh();s['previous_year_flag_after']=previous_year;s['global_connection_restore_requested']=False
    chosen=None
    if route=='enter':
        if 0<=index<len(rows):chosen=rows[index]
        else:
            if rows:s['events'].append('SelectedIndex-zero-and-scroll-requested-not-observed-SelectionChanged')
            return s
    elif route=='double':
        chosen=selected
        if chosen is None:return s
    elif route=='return-button':
        s['control_only_not_selected_linked_command']=True
        if tag is None:return s
        s['lookup_called']=True;s['lookup_outcome_supplied']=lookup
        if lookup=='found':s['events'].append('prior-return-warning-and-return');return s
        chosen=tag;s['events'].append('lookup-false-including-catch-false-not-typed-Failed')
    else:
        if route=='close-button' and previous_year:
            s['previous_year_flag_after']=False;s['global_connection_restore_requested']=True
        s['events'].append('Close-requested-without-local-acceptance');return s
    if route!='return-button':s['done']=True;s['events'].append('ISDone-written-before-three-payload-fields')
    s.update(chosen);s['events'].append('gid-proc-pay-copied-from-supplied-local-row')
    if route=='return-button':s['done']=True;s['events'].append('ISDone-written-after-payload')
    s['events'].append('Close-requested' if route=='enter' else 'Hide-requested')
    return s


def caller_gate(s,dialog_returned):
    dialog_returned=flag(dialog_returned);done=flag(s['done']);gid=token(s['gid'],empty=True)
    return dict(dialog_return_supplied=dialog_returned,first_result_gate=dialog_returned and done and gid!='-1',
        binding_requested=dialog_returned and done and gid!='-1',typed_load_success_proved=False,
        query_predicates_at_this_boundary=['IS_Deleted=0','InvGlobalID=chosen'],
        requested_type_proc_branch_rechecked_here=False,application_source_executed=False)


def refresh(old,incoming,stage='none',prefix=0):
    old,incoming=rows_input(old),rows_input(incoming);prefix=number(prefix)
    if stage not in {'none','before-clear','after-clear','during-row'}:raise ValueError('supplied boundary,not actual DataAdapter/Convert failure')
    if prefix>len(incoming):raise ValueError('supplied prefix within incoming')
    display=[dict(r) for r in old] if stage=='before-clear' else []
    if stage=='none':display=[dict(r) for r in incoming]
    elif stage=='during-row':display=[dict(r) for r in incoming[:prefix]]
    return dict(display=display,stage_supplied=stage,typed_health_returned=False,
                actual_DataView_or_conversion_or_provider_executed=False,
                complete_hydration_or_UI_snapshot_proved=False)


def build():
    reads=[];context=[];whole=[]
    for declared,dest,mode in ((SOURCE_SLICES,reads,'selected-contract-slice'),(CONTEXT_SLICES,context,'context-not-certified-command'),(WHOLE_REREADS,whole,'whole-local-body-reread-already-B27-B28-not-new-completion')):
        for path,start,end in declared:
            raw=(ROOT/path).read_bytes();lines=raw.decode('utf-8-sig').splitlines();assert 1<=start<=end<=len(lines)
            dest.append(dict(path=path,start=start,end=end,total_lines=len(lines),sha256=hashlib.sha256(raw).hexdigest(),read_mode=mode,prior_whole_body_parts=['B27','B28'] if dest is whole else []))
    def text(path,start,end):return '\n'.join((ROOT/path).read_text(encoding='utf-8-sig').splitlines()[start-1:end])
    a,b=row(),row('doc-B');examples=[]
    def example(n,title,value,ok,roots,evidence):
        examples.append(dict(id=f'ALG7B36-{n:02d}',title=title,value=value,assertions_passed=bool(ok),finding_ids=roots,evidence=evidence,source_application_executed=False,limit='قيم وصفوف وحدود رجوع وفشل موردة؛لا WPF/SQL/SDK أو إعادة تأريخ أو اعتماد لكل المتصلين.'))
    s=fresh();example(1,'fresh local defaults,not InvoiceDGV defaults',s,not s['done'] and s['gid']=='-1','P7-160',f'{CS}:49-66')
    q=request();example(2,'constructor then caller inputs',q,q['events'].index('ConnObj-called-before-caller-inputs')<q['events'].index('caller-ProcType-assigned'),'P7-160',f'{IO}:3941-3951;{CS}:49-66')
    q=request(later_conn='conn-B');example(3,'connection token captured before supplied later global value',q,q['constructor_connection_token']=='conn-A' and not q['connection_content_or_liveness_or_ownership_proved'],'H7B36-02',f'{CS}:49-66')
    sources=[source_row(),source_row('doc-B',kind=20),source_row('doc-C',kind=1,branch=2),source_row('doc-D',kind=1,deleted=True)]
    z=query_select(sources,request());example(4,'same allowed-set root157,not a new caller finding',z,[r['gid'] for r in z]==['doc-A','doc-B'],'P7-157',f'{CS}:378-408')
    z=query_select([source_row(kind=23),source_row('doc-B',kind=20)],request(inv_type=23));example(5,'contract branch23 exact-kind control only',z,len(z)==1 and z[0]['kind']==23,'P7-157',f'{CS}:348-408')
    z=query_select([source_row(kind=20)],request(inv_type=20));example(6,'OR20 not UNION duplicate',z,len(z)==1,'P7-157',f'{CS}:378-408')
    z=local_proc_filter([a],2);example(7,'changing local proc cannot add excluded source rows',z,z==[] and local_proc_filter([a],0)==[a],'P7-155',f'{CS}:336-345;{CS}:510-519')
    s=accept('enter',[a,b],index=1);example(8,'Enter publishes indexed local payload then Close request',s,s['done'] and s['gid']=='doc-B' and s['events'][-1]=='Close-requested','P7-160',f'{CS}:88-116')
    s=accept('enter',[a]);example(9,'invalid index requests selection,no acceptance in this call',s,not s['done'] and bool(s['events']),'P7-160',f'{CS}:88-116')
    s=accept('enter',[]);example(10,'empty Enter leaves fresh result',s,not s['done'] and s['events']==[],'P7-160',f'{CS}:88-116')
    s=accept('double',[a,b],index=0,selected=b);example(11,'double-click uses supplied SelectedItem,not index assertion',s,s['gid']=='doc-B' and s['events'][-1]=='Hide-requested','P7-160',f'{CS}:261-284')
    s=accept('double',[a]);example(12,'null selected-item control',s,not s['done'],'P7-160',f'{CS}:266-284')
    s=accept('escape',[a]);example(13,'fresh Escape local result not accepted',s,not s['done'] and s['gid']=='-1','P7-160',f'{CS}:88-116')
    s=accept('close-button',[a]);example(14,'current-year Close button,no global restore branch',s,not s['global_connection_restore_requested'] and not s['done'],'P7-160',f'{CS}:123-132')
    s=caller_gate(dict(done=True,gid=''),True);example(15,'only sentinel exclusion does not reject empty string',s,s['first_result_gate'] and not caller_gate(dict(done=True,gid='-1'),True)['first_result_gate'],'P7-160',f'{IO}:3976-3982')
    s=caller_gate(accept('enter',[a],index=0),False);example(16,'Close request alone does not supply modal return',s,not s['binding_requested'],'P7-160',f'{IO}:3976-3982;{CS}:88-116')
    s=refresh([a],[b],'before-clear');example(17,'before-clear failure supplied,old display control already046B28',s,s['display']==[a],'P7-046',f'{CS}:492-508;{CS}:567-596')
    s=refresh([a],[a,b],'during-row',1);example(18,'supplied conversion boundary exposes prefix,not actual provider experiment',s,s['display']==[a] and not s['typed_health_returned'],'H7B36-02',f'{CS}:567-596')
    s=accept('return-button',[a],tag=a,lookup='failed');example(19,'separate button lookup context,not certified linked gesture',s,s['done'] and not accept('return-button',[a],tag=a,lookup='found')['done'],'H7B36-03',f'{CS}:286-303;{CS}:603-619')
    s=dict(local_payload_fields=['gid','proc','pay'],source_type_branch_InvoiceStatus_in_payload=False,InvoiceDGV_contract_proved=False);example(20,'known local row payload is not external document contract',s,not s['InvoiceDGV_contract_proved'],'P7-157',f'{CS}:674-698;{IO}:3976-3985')
    lexical=[]
    def lex(n,title,path,start,end,predicate,roots):
        chunk=text(path,start,end);lexical.append(dict(id=f'ST7B36-{n:02d}',title=title,evidence=f'{path}:{start}-{end}',finding_ids=roots,documented_text_observation_matches=bool(predicate(chunk)),source_application_executed=False,limit='فحص نصي لحد معلن،لا trace إطار أو تنفيذ SQL/DTO أو كفاية كل الحراس.'))
    lex(1,'constructor connection before defaults',CS,49,66,lambda t:t.index('MainClass.ConnObj()')<t.index('ProcType     = 1'),'H7B36-02')
    lex(2,'fresh sentinel and false local',CS,49,66,lambda t:'InvGlobalID  = "-1"' in t and 'ISDone       = false' in t,'P7-160')
    lex(3,'caller settings before request fields',IO,3941,3951,lambda t:t.index('DoApplyUserSett')<t.index('ProcType = Ptype'),'P7-160')
    lex(4,'Loaded ordered calls,not observed event count',CS,73,86,lambda t:t.index('LoadProcessTypes();')<t.index('LoadInvoices();')<t.index('ApplyColumnVisibility();'),'P7-155')
    lex(5,'Enter indexed row and done before gid',CS,88,108,lambda t:t.index('_displayRows[_rowIndex]')<t.index('ISDone      = true')<t.index('InvGlobalID = row.InvGlobalID')<t.index('Close();'),'P7-160')
    lex(6,'invalid-index branch selection request only',CS,107,116,lambda t:'dgvItems.SelectedIndex = 0' in t and 'ISDone' not in t,'P7-160')
    lex(7,'row index follows selected index locally',CS,261,265,lambda t:'_rowIndex = dgvItems.SelectedIndex;' in t,'P7-160')
    lex(8,'double-click row null control then Hide',CS,266,284,lambda t:'SelectedItem as InvoiceSrchRow' in t and 'if (row == null) return;' in t and 'Hide();' in t,'P7-160')
    lex(9,'Escape directly requests Close',CS,109,116,lambda t:'Key.Escape) Close();' in t,'P7-160')
    lex(10,'Close button only has explicit global restoration branch',CS,123,132,lambda t:'MainClass.ReturnYearPreviews = false' in t and 'MainClass.connstr = MainClass.originalConnStr' in t and 'ISDone' not in t,'H7B36-04')
    lex(11,'Fill precedes ApplyFilter',CS,310,334,lambda t:t.index('adapter.Fill(_masterTable);')<t.index('ApplyFilter();')<t.index('catch'),'P7-046')
    lex(12,'unconditional original-proc predicate',CS,336,345,lambda t:'inv.proc_type = {ProcType}' in t,'P7-155')
    lex(13,'noncontract query permits20 OR requested',CS,378,408,lambda t:'(inv_type = 20 OR inv_type = {InvType})' in t,'P7-157')
    lex(14,'local selected-index filter not source request write',CS,510,519,lambda t:'cmbProcType.SelectedIndex' in t and 'proc_type = {procIndex}' in t and 'ProcType =' not in t,'P7-155')
    lex(15,'display clear before row conversions',CS,567,596,lambda t:t.index('_displayRows.Clear();')<t.index('foreach')<t.index('SafeInt(rv["proc_type"])'),'H7B36-02')
    lex(16,'local model explicitly auto-properties',CS,674,698,lambda t:'InvGlobalID        { get; set; }' in t and 'ProcType           { get; set; }' in t and 'InvoiceStatus' not in t,'P7-157')
    lex(17,'XAML uses full-row single selection and double event',X,397,414,lambda t:'SelectionMode="Single"' in t and 'SelectionUnit="FullRow"' in t and 'MouseDoubleClick="dgvItems_MouseDoubleClick"' in t,'P7-160')
    lex(18,'source caller gate then gid-only bind boundary',IO,3976,3985,lambda t:'frmInvoiceSrch2.ISDone &' in t and 'InvGlobalID, "-1"' in t and 'IS_Deleted=0 and InvGlobalID=' in t and 'inv_type=' not in t,'P7-157;P7-160')
    lex(19,'return button is distinct Tag-and-lookup route',CS,286,303,lambda t:'btn.Tag is not InvoiceSrchRow row' in t and 'IsPreviousReturned(row.InvGlobalID)' in t and t.index('InvGlobalID =')<t.index('ISDone      = true'),'H7B36-03')
    lex(20,'return column ProcType2 only in local method',CS,621,636,lambda t:'ColReturnInv.Visibility = ProcType == 2' in t,'H7B36-03')
    errors=[r['id'] for r in examples if not r['assertions_passed']]+[r['id'] for r in lexical if not r['documented_text_observation_matches']]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,new_root_ids=[],extended_existing_root_ids=[],existing_roots_deepened_without_registry_change=['P7-157','P7-160'],application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,dialog_modal_return_or_Loaded_order_observed=False,real_query_or_conversion_failures_executed=False,source_enum_or_external_InvoiceDGV_contract_proved=False,all_callers_or_historical_bodies_certified=False,local_InvoiceSrchRow_auto_properties_known=True,selection_connection_modal_and_failure_values_supplied=True,return_button_and_previous_year_controls_not_certified=True,repair_start_or_sync_known=False,phase7C_started=False,phase8_authorized_or_started=False,application_remediation_performed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=20,lexical_check_count=20,selected_source_paths=3,contract_slices=20,context_slices=6,whole_local_source_bodies_reread=1,newly_completed_local_files=0,prior_whole_body_review_parts=['B27','B28'],illustrations=examples,static_lexical_contract_checks=lexical,bounded_source_reads_not_semantic_coverage=reads,context_reads_not_command_certification=context,whole_local_rereads_not_new_completions=whole,retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),errors=errors)


if __name__=='__main__':
    value=build();print(json.dumps(value,ensure_ascii=False,indent=2));raise SystemExit(bool(value['errors']))
