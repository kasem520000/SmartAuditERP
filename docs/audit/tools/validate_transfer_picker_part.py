#!/usr/bin/env python3
"""Read-only B37/R4u transfer-picker command/tail documentary audit,NOT ERP.

Three command tails and ordinary search control in four old paths;16contract
and5context slices,no whole file/new completion. Same split acceptance/tail
mechanism160,accepted-target/abandon159 comparison without registry changes
or certainty transfer. ALL335/entire raw336/G264/827 originals/1173 protected
of1177 entry artifacts exact. TR8/TT8/FE16/INV16/RC6/AD8/32 operational plans
NOT executed. RS14/SP3/HQ6/RW10/BK10 retain FULL upstream inputs,hashes,
contracts,routes and dispositions. LIVE37/versioned36/API15/19gates/139 actual
execution tools separate from B36 historical135 assertion identities/exact
canonical dispatcher TEXT via child-local A/Path,NOT old code execution.
ALL1294 prior documentary cases incl ALL52 B36 unmodified,no skips or filters.
Actual42 OWN modes are fresh subprocess captures with139 source identities;
only one later helper pin may be inverted in memory. Archive summaries/raw
stdout identities are not full streams or final/postpin/prose/postpush replay.
Normal modal returns,headers/field snapshots,SDK setter completion,number
candidates and failure boundaries supplied,not WPF/provider/SQL/DTO behavior.
LoadInvoiceNumber local catch-return distinct from nonreturn;void never typed
success. Field ProcType versus header ProcType is unresolved number policy,
not automatically a defect or new root. No inferred DTO defaults,aliasing,
complete hydration,UI rollback/final flags or Close/Hide/chrome/Loaded order.
Previous-year/Return button/other callers,SDK/enum/collections,save/stock/ACL/
financial/production barriers remain7B. 155/156/157/046B28 distinct;potential
014/108/132/145 and020/021 unchanged. B10 additive10vs120/equality1=10/G138.
Governing reference2026-11-16 separate from literal raw sandbox clock dates;
consumed evidence retained,no calendar validation from frozen assertions.
Capture9769/delivery-B37entrya83/source10ba distinct. No ERP/build/C#/VB/.NET/
WPF/SQL/DataView/provider/SDK/REPX/ToDataTable/devices/businessdata/secrets/
save/numberreservation/repair/measurement/operational acceptance. No global
Path/shared-subprocess patch,old dispatcher execution,overlay/rebaseline or
protected edits. 7B/7partial,R4v/B38 or reasoned SP01..03 split,7Cunstarted,
8unauthorized,repair start/syncunknown,next_phase8 planning only,no duration/
session/percent/whole-system completion promise."""
from __future__ import annotations
import collections
from contextlib import contextmanager
import csv
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs
from validate_contract_item_part import row_sha,expanded_source_evidence
from validate_property_dialog_part import source_evidence_union
from validate_invoice_picker_part import historical_record_errors as historical41_errors,registry_preservation_errors
from check_transfer_picker_witnesses import CS,X,IO,PICKER,SOURCE_SLICES,CONTEXT_SLICES,WHOLE_REREADS,SCOPE_RANGES

ENTRY='a83cb66108241ad51ab4f08fbff3fe5f361d58a0'
SNAPSHOT='evidence/findings-through-07B36.csv'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B36.json'
DISPATCHER_SNAPSHOT='evidence/dispatcher-through-07B36.py.txt'
SNAPSHOT_SHA='ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a'
SHARED_SHA='756199d3eb2cc7e60967cd6b2889990ef0225b8c5dc3dfdf234e8ff67ba0c977'
PROVENANCE_SHA='5420e21db371f9f42ecb46aa6ad25e8993b75cd86d37ba934fbcf018a4cc03f0'
DISPATCHER_SHA='18f5d64264b5457f28761644ff9ddd27716b91eb3921e347b08e5368dd302895'
B36_CHECK_SHA='c7fae884e389c814813d6f092403ce1ae33eaa8a33c7dbe56517d39bf590b151'
B36_RECEIPT_SHA='a5c6551bc73eb46bf484a830719f0ae9c6f0b9405c944260850e3eb7c3c3132f'
WITNESS_SHA='49ef0d41357f37d271476167536fb2ee3c5ceb92cc7c2b1d6004b2618c7df06b'
HISTORICAL_RUN_SHA = '12c926533f5a844e3b6dcacc89b52a8f2a6fc72ae204ea1ca8617cfd59d3900b'  # Pin only after exclusive actual42 capture.
DOCUMENTARY='none-documentary-metadata'
SCOPE_FILE='review-scope-07B37.csv'
DEEPENED_IDS=['P7-159','P7-160']
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
PART_DOCS=('PHASE-07B37.md','TRANSFER-PICKER-CONTRACTS-07B37.md','VALIDATION-07B37.md','PHASE-07-REMAINING-07B37.md','DATE-IDENTITY-NOTE-07B37.md')
TABLE_SPECS=(('transfer-request-lineage','TR7B37-',8),('transfer-tail-lineage','TT7B37-',8),('feature-implementation-matrix','FE7B37-',16),('report-invariants','INV7B37-',16),('acceptance-tests','P7B37T-',32),('report-reconciliation','RC7B37-',6),('root-adjudication','AD7B37-',8),('residual-disposition','RS7B37-',14),('split-register','SP7B37-',3),('handoffs','H7B37-',6),('questions','Q7B37-',6),('remaining-workplan','RW7B37-',10),('continuation-backlog','BK7B37-',10))
SENTINELS={f'{p}{n:02d}' for p,ns in (('FE7B37-',(15,16)),('INV7B37-',(15,16)),('P7B37T-',range(29,33)),('RC7B37-',(6,)),('AD7B37-',(8,)),('RS7B37-',range(1,15)),('H7B37-',range(1,7)),('Q7B37-',range(1,7))) for n in ns}
DEDUP_DEPTH='all335-title-metadata-and71-literal-four-path-registry-rows-plus8-prior-finding-sections-and-B28-046-extension-and-B36-first-picker-boundary-not-all-bodies-or-callers'
TR_GROUPS=((0,1),(2,3),(4,5),(6,7),(8,),(9,10),(11,12),(13,14,15))
TT_GROUPS=((0,1),(2,3,4),(5,),(6,),(7,),(8,9),(10,11,12),(13,14,15))
FEATURE_ROOTS=('H7B37-01', 'P7-160', 'P7-160', 'P7-160', 'P7-160', 'P7-160', 'P7-160', 'P7-159', 'H7B37-02', 'H7B37-04', 'H7B37-05', 'H7B37-04', 'P7-156;P7-157', 'H7B37-02', 'H7B37-06', 'H7B37-06')


@contextmanager
def historical_b36_inputs(v,frozen335,texts,raw,sources,dispatcher):
    """Read-only child-local assertion DATA;never an old dispatcher execution."""
    if (type(frozen335) is not list or len(frozen335)!=335 or any(type(r) is not dict for r in frozen335)
        or len({r.get('id') for r in frozen335})!=335):raise ValueError('Exactly335 distinct OWN B36 rows')
    if type(texts) is not dict or set(texts)!=set(SHARED_DOCS) or any(type(s) is not str for s in texts.values()):raise ValueError('Three OWN shared index strings')
    if (type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=336
        or not raw.endswith(b'\r\n') or any(c in raw.replace(b'\r\n',b'') for c in (b'\r',b'\n'))):raise ValueError('OWN335/raw336CRLF/noBOM')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))
    except (UnicodeError,csv.Error) as exc:raise ValueError('Malformed OWN raw') from exc
    if parsed!=frozen335:raise ValueError('OWN rows/raw mismatch')
    if (type(sources) is not dict or len(sources)!=135
        or any(type(n) is not str or re.fullmatch(r'tools/[A-Za-z0-9_]+\.py',n) is None
               or type(h) is not str or re.fullmatch('[0-9a-f]{64}',h) is None for n,h in sources.items())
        or type(dispatcher) is not bytes or not dispatcher
        or sources.get('tools/validate_audit.py')!=hashlib.sha256(dispatcher).hexdigest()):raise ValueError('Exactly135 assertion identities and dispatcher TEXT')
    dispatcher.decode('utf8',errors='strict')
    original=v.AUDIT;registry=(original/'findings.csv').resolve();dispatch=(original/'tools/validate_audit.py').resolve()
    tool_dir=(original/'tools').resolve();names=tuple(sorted(sources))
    class HistoricalOwnPath(type(original)):
        def read_bytes(self):
            resolved=self.resolve()
            if resolved==registry:return raw
            if resolved==dispatch:return dispatcher
            return super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            if self.resolve() in (registry,dispatch):return io.StringIO(self.read_bytes().decode(encoding or 'utf8',errors or 'strict'),newline=None).read()
            return super().read_text(encoding=encoding,errors=errors)
        def open(self,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
            if self.resolve() in (registry,dispatch):
                if mode not in ('r','rt','rb'):raise ValueError('Historical assertion data are read-only')
                if mode=='rb':return io.BytesIO(self.read_bytes())
                return io.StringIO(self.read_bytes().decode(encoding or 'utf8',errors or 'strict'),newline=newline)
            return super().open(mode=mode,buffering=buffering,encoding=encoding,errors=errors,newline=newline)
        def glob(self,pattern,*args,**kwargs):
            if self.resolve()==tool_dir and pattern=='*.py':
                for n in names:yield type(self)(original/n)
            else:yield from super().glob(pattern,*args,**kwargs)
    try:
        v.AUDIT=HistoricalOwnPath(original)
        with historical_b1_inputs(v,frozen335,texts):yield
    finally:v.AUDIT=original



class HistoricalB36Subprocess:
    def __init__(self,backend,python,tools):
        self.backend=backend
        self.expected=[python,'-B',str(tools/'test_invoice_picker_audit_validator.py')]
        self.actual=[python,'-B',str(tools/'run_historical_invoice_picker_tests_07B37.py'),'--through-part','B36']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if type(args) is list and args==self.expected else args,*pos,**kwargs)


class HistoricalB36ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB36Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess' else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b36_validation(v,report,prior,prov,frozen335):
    ck=v.check
    for name,digest in ((SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),(DISPATCHER_SNAPSHOT,DISPATCHER_SHA),('evidence/provenance-07B37.json',PROVENANCE_SHA),('evidence/checks-07B36.json',B36_CHECK_SHA),('evidence/official-capture-receipt-07B36.json',B36_RECEIPT_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B37 immutable input:'+name)
    ck(prov['historical_artifact_count']==len(prov['historical_artifact_sha256'])==1173 and prov['entry_artifact_count']==1177 and len(frozen335)==335,'B37 protected1173/1177/OWN335')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B37 protected1122→1173 continuity')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B37 pushed entrya83cb66')
    ck(prov['declared_mutable_entry_paths']==sorted(SHARED_DOCS+('tools/validate_audit.py',)) and prov['historical_artifact_sha256'].get('findings.csv')==SNAPSHOT_SHA,'B37 registry immutable not mutable')
    old=json.loads(v.read(v.AUDIT/'evidence/checks-07B36.json'));vv=old['validation'];s=vv['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='9769e29b8ce34f720fd660a475800f5c3bf9b7fa' and len(s)==37 and sum(x['tests_reported'] for x in s.values())==1294 and vv['errors']==[] and old['original_project_hashes_matching']==827,'B37 B36 genuine capture9769 not deliverya83')
    ck(old['historical_artifact_sha256']==prior['historical_artifact_sha256'] and vv['current_output_record_pending_first_write_not_placeholder'] is False,'B37 retained B36 actual stdout')
    er=prov['entry_actual_subprocess_receipt']
    ck(tuple(er.get(k) for k in ('checkout_head','process_exit_code','validation_errors','findings','originals_matching','documentary_cases','documentary_suites','outer_stderr_bytes'))==(ENTRY,0,[],335,827,1294,37,0) and er['all1177_entry_artifacts_unchanged'] is True,'B37 independent entry1294/37')
    ep=v.AUDIT/prov['entry_stdout_retained_as_captured'];ck(v.sha(ep)==er['stdout_sha256'] and len(ep.read_bytes())==er['stdout_bytes'],'B37 entry stdout not regenerated')
    sources=prov['historical_checker_sources_at_entry'];ck(len(sources)==135 and sources['tools/validate_audit.py']==DISPATCHER_SHA and prov['dispatcher_source_at_entry']==dict(path=DISPATCHER_SNAPSHOT,bytes=111104,sha256=DISPATCHER_SHA),'B37 historical135 assertion data not actual139 tools')
    view=HistoricalB36ValidatorView(v);texts=json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b36_inputs(view,frozen335,texts,(v.AUDIT/SNAPSHOT).read_bytes(),sources,(v.AUDIT/DISPATCHER_SNAPSHOT).read_bytes()):yield view
    child=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_invoice_picker_audit_validator.py']
    child.update(historical_parser_cutoff='B36-not-current-B37-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_invoice_picker_tests_07B37.py',actual_subprocess_argv=view.subprocess.actual,no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=135,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B36-335-not-current-B37-state',phase_7B36_historical_input_mode='OWN335-raw336CRLF-indexes-presetB36-ALL52-child-module-local-A-Path-and135-source-assertion-inputs',phase_7B36_adapter_context=dict(entry_provenance='evidence/provenance-07B37.json',adapter_protected_artifacts_checked=1173,old_dispatcher_TEXT_not_executed=True,module_local_Path_type_for_source_reads_not_process_global=True,archived_stdout_not_rewritten_after_push=True,current_indexes_not_inputs=True))


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=264 or rows(current)[:264]!=rows(previous):return ['B37 G01..264 exact']
    return [] if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)==[f'G-{n:02d}' for n in range(1,269)] else ['B37 only265..268 ordered']


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B37 ALL14 residuals']
    errors=[]
    for old,new in zip(upstream,current):
        if tuple(new.get(k) for k in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'))!=(old.get('id'),'evidence/residual-disposition-07B36.csv',row_sha(old),old.get('upstream_contract_ids')):errors.append('B37 residual ancestry/hash/contracts')
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B37 full upstream input prefix')
        mapped={x.replace('7B36-','7B37-') for x in old.get('current_handoff_or_split_ids','').split(';') if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B37 ALL mapped routes')
        if new.get('disposition')!=old.get('disposition') or new.get('disposition') not in {'external-handoff','split-explicitly','assessment-source-bound'} or new.get('runtime_status')!='not-executed':errors.append('B37 unchanged disposition not approval')
        for k in ('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):
            if type(new.get(k)) is not str or len(new[k])<20:errors.append('B37 residual responsibility:'+k)
    return errors


def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return ['B37 ALL3 splits']
    errors=[]
    for old,new in zip(upstream,current):
        if (new.get('upstream_split_id'),new.get('upstream_artifact'),new.get('upstream_row_sha256'))!=(old.get('id'),'evidence/split-register-07B36.csv',row_sha(old)):errors.append('B37 split ancestry/hash')
        if not new.get('required_input','').startswith(old.get('required_input','')):errors.append('B37 full split input prefix')
        for k in ('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if type(new.get(k)) is not str or not new[k].strip():errors.append('B37 split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started' or new.get('runtime_status')!='not-executed':errors.append('B37 future split not completed')
    return errors


def remaining_work_errors(rows):
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4u-transfer-command-tail-delivered-residuals-open']+['planned-not-started']*6
    if len(rows)!=10:return ['B37 fourB/sixC']
    return ['B37 work/permission'] if any(r.get('part_family')!=('7B' if i<4 else '7C') or r.get('status')!=expected[i] or r.get('runtime_status')!='not-executed' or r.get('counts_are_sessions_or_completion_percent')!='false' for i,r in enumerate(rows)) else []


def current_link_errors(fe,inv,plans):
    if (len(fe),len(inv),len(plans))!=(16,16,32):return ['B37 FE16/INV16/T32']
    errors=[]
    for n,(f,i) in enumerate(zip(fe,inv),1):
        tids=';'.join(f'P7B37T-{k:02d}' for k in (2*n-1,2*n))
        if (f.get('id'),i.get('id'),i.get('feature_ids'),f.get('acceptance_ids'),i.get('acceptance_ids'),f.get('finding_ids'),i.get('finding_ids'))!=(f'FE7B37-{n:02d}',f'INV7B37-{n:02d}',f.get('id'),tids,tids,FEATURE_ROOTS[n-1],FEATURE_ROOTS[n-1]):errors.append('B37 exact root and plan links')
        for t in plans[2*n-2:2*n]:
            if (t.get('feature_ids'),t.get('invariant_ids'),t.get('finding_ids'),t.get('status'))!=(f.get('id'),i.get('id'),f.get('finding_ids'),'not-executed'):errors.append('B37 plan links/nonexecution')
            for k in ('scenario','owner_role','prerequisites','procedure','acceptance_criterion','safety_controls'):
                if type(t.get(k)) is not str or len(t[k])<20:errors.append('B37 substantive plan:'+k)
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim','static_exit_criterion'):
            if type(f.get(k)) is not str or len(f[k])<20:errors.append('B37 capability responsibility:'+k)
    if len({r.get('required_invariant') for r in inv})!=16 or len({r.get('acceptance_criterion') for r in plans})!=32:errors.append('B37 distinct invariants/criteria')
    return errors


def ledger_errors(requests,results,fe):
    if len(fe)!=16:return ['B37 FE16 for ledgers']
    errors=[]
    for pool,groups,prefix in ((requests,TR_GROUPS,'TR7B37-'),(results,TT_GROUPS,'TT7B37-')):
        if len(pool)!=8:errors.append('B37 TR8/TT8');continue
        for n,(r,indices) in enumerate(zip(pool,groups),1):
            fs=[fe[i] for i in indices];roots=';'.join(dict.fromkeys(x for f in fs for x in f['finding_ids'].split(';')));route=' | '.join(f['entry_point']+' → '+f['output_boundary'] for f in fs)
            if (r.get('id'),r.get('feature_ids'),r.get('finding_ids'),r.get('evidence'),r.get('source_to_output'),r.get('boundary'))!=(f'{prefix}{n:02d}',';'.join(f['id'] for f in fs),roots,source_evidence_union(fs),route,fs[0]['capability']):errors.append('B37 exact ordered request/result union')
            for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','observation'):
                if type(r.get(k)) is not str or not r[k].strip():errors.append('B37 lineage responsibility:'+k)
            if r.get('runtime_status')!='not-executed':errors.append('B37 lineage not runtime')
    return errors


def witness_metadata_errors(w):
    errors=[]
    false_keys=('application_code_imported_or_executed','dotnet_wpf_sql_or_SDK_executed','dialog_modal_return_or_Loaded_order_observed','real_query_or_conversion_failures_executed','source_enum_or_external_InvoiceDGV_contract_proved','all_callers_or_historical_bodies_certified','repair_start_or_sync_known','phase7C_started','phase8_authorized_or_started','application_remediation_performed')
    true_keys=('modal_header_field_number_and_failure_values_supplied','number_helper_catch_return_distinct_from_nonreturn','field_header_proc_difference_policy_unresolved','previous_year_return_button_and_other_callers_not_certified')
    for k in false_keys:
        if w.get(k) is not False:errors.append('B37 false-only:'+k)
    for k in true_keys:
        if w.get(k) is not True:errors.append('B37 true-only:'+k)
    for k,n in (('erp_runtime_tests_executed',0),('sql_or_external_service_tests_executed',0),('illustration_count',20),('lexical_check_count',20),('selected_source_paths',4),('contract_slices',16),('context_slices',5),('whole_local_source_bodies_reread',0),('newly_completed_local_files',0)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B37 strict count:'+k)
    if w.get('new_root_ids')!=[] or w.get('extended_existing_root_ids')!=[] or w.get('existing_roots_deepened_without_registry_change')!=DEEPENED_IDS or w.get('entry_checkout')!=ENTRY or w.get('audit_reference_date_utc')!='2026-11-16':errors.append('B37 zero-root/entry/reference')
    e=w.get('retained_additive_B10_arithmetic_erratum',{})
    if e!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True) or any(type(e.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or e.get('protected_G138_not_rewritten') is not True:errors.append('B37 additive B10 arithmetic')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=42 or len(modes)!=42:return ['B37 exactly42 actual modes']
    errors=historical41_errors(dict(historical_mode_count=41,historical_modes=modes[:41],errors=h.get('errors')))
    last=modes[-1];expected=dict(mode='B36',findings_total=335,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1294,audit_checker_self_test_suite_count=37,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0)
    for k,val in expected.items():
        if last.get(k)!=val or type(last.get(k)) is not type(val):errors.append('B37 OWN335/1294/37:'+k)
    child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B36-not-current-B37-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_invoice_picker_tests_07B37.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=135,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
    for k,val in child.items():
        actual=(last.get('historical_B36_child') or {}).get(k)
        if actual!=val or type(actual) is not type(val):errors.append('B37 ALL52 B36 child:'+k)
    if type(last.get('stdout_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B37 stdout identity required')
    return errors


def capture_source_errors(h,sources):
    expected=h.get('checker_sources_at_capture',{})
    if set(expected)!=set(sources) or len(expected)!=139:return ['B37 capture tool set139']
    errors=[]
    for n,raw in sources.items():
        if n=='tools/validate_transfer_picker_part.py':
            final="HISTORICAL_RUN_SHA = '"+str(HISTORICAL_RUN_SHA)+"'  # Pin only after exclusive actual42 capture."
            initial='HISTORICAL_RUN_SHA = None  # Pin only after exclusive actual42 capture.';s=raw.decode()
            if HISTORICAL_RUN_SHA is None or s.count(final)!=1:errors.append('B37 exact final pin required');continue
            raw=s.replace(final,initial).encode()
        if hashlib.sha256(raw).hexdigest()!=expected[n]:errors.append('B37 tool changed beyond sole inverse pin:'+n)
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or type(prov.get('environment_clock_observed_utc')) is not str or not prov.get('date_authority'):errors.append('B37 governing reference/raw clock distinct')
    for val in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,'9769e29b8ce34f720fd660a475800f5c3bf9b7fa',B36_CHECK_SHA,B36_RECEIPT_SHA,DISPATCHER_SHA,WITNESS_SHA,'1173','1177','335','135','139','129'):
        if val not in note:errors.append('B37 identity:'+val)
    return errors


def dedup_errors(screen,frozen):
    errors=[];meta=[{k:r[k] for k in ('id','title','severity','certainty','type','status')} for r in frozen]
    if screen.get('comparison_depth')!=DEDUP_DEPTH or screen.get('title_metadata_rows')!=meta or screen.get('all_historical_bodies_reviewed') is not False or screen.get('new_root_ids')!=[] or screen.get('existing_root_extensions')!=[] or screen.get('existing_roots_deepened_without_registry_change')!=DEEPENED_IDS or screen.get('registry_entire_raw_bytes_unchanged') is not True or screen.get('source_reread_not_new_completion') is not True or screen.get('field_header_number_difference_is_unresolved_policy_not_new_root') is not True:errors.append('B37 metadata/body depth/zero roots/unresolved policy')
    paths=screen.get('four_path_screen',[]);matched=[r for r in frozen if any(p+':' in r['evidence'] for p in paths)]
    if set(paths)!={CS,X,IO,PICKER} or len(paths)!=4 or len(matched)!=71 or screen.get('path_matching_registry_rows')!=[dict(id=r['id'],row_sha256=row_sha(r)) for r in matched]:errors.append('B37 literal71 path rows')
    sections=screen.get('selected_prior_finding_sections',[])
    if len(sections)!=8 or len({r.get('finding_id') for r in sections})!=8 or not set(DEEPENED_IDS)<={r.get('finding_id') for r in sections}:errors.append('B37 selected8 prior finding sections')
    extra=screen.get('additional_selected_extension_and_contract_sections',[])
    if len(extra)!=2 or [r.get('artifact') for r in extra]!=['PHASE-07B28.md','PHASE-07B36.md'] or screen.get('old_046_B28_extension_retained_not_reextended') is not True:errors.append('B37 retained B28 extension and B36 first-picker boundary')
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id'] in SENTINELS,'B37 undeclared documentary sentinel:'+row['id']);return
    v.check(row['id'] not in SENTINELS,'B37 invented source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
    try:expanded=expanded_source_evidence(row['evidence'])
    except ValueError as exc:v.check(False,'B37 malformed evidence:'+str(exc));return
    v.scoped_evidence(expanded,scope,row['id']+' boundedB37',phase=7)


def extend_transfer_picker(v,report,prov,frozen335):
    ck,rows=v.check,v.rows;current=rows('findings.csv');lookup={r['id']:r for r in current}
    for err in registry_preservation_errors(frozen335,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes(),rows('evidence/historical-extensions-07B37.csv')):ck(False,'B37 '+err)
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[],'B37 zero new finding headers')
    ck(prov['new_root_ids']==[] and prov['existing_registry_evidence_extensions']==[] and prov['existing_roots_deepened_without_registry_change']==DEEPENED_IDS,'B37 no recount/implicit certainty transfer')
    for root in ('P4-014','P7-108','P7-132','P7-145'):ck(lookup[root]['certainty']=='potential','B37 potential retained:'+root)
    for key in ('phase7C_started','phase8_authorized_or_started','application_remediation_performed','repair_start_or_sync_known'):ck(prov[key] is False,'B37 no unauthorized start/sync:'+key)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B37 independent repair')
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B37 no runtime:'+k)
    for e in date_identity_errors(prov,v.read(v.AUDIT/PART_DOCS[4])):ck(False,e)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};inventory={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==4 and set(scope)=={CS,X,IO,PICKER},'B37 four prior paths')
    for r in selected:ck(r['ranges']==SCOPE_RANGES[r['path']] and r['review_state']=='bounded-transfer-command-and-context-slices-not-whole-file-or-runtime' and bool(r['focus']),'B37 bounded no whole/new completion');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    tables={};known=set(lookup)|{f'H7B37-{n:02d}' for n in range(1,7)}
    for stem,prefix,n in TABLE_SPECS:
        data=rows('evidence/'+stem+'-07B37.csv');tables[prefix]=data;v.sequential(data,prefix,n)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(type(x) is str and x.strip() for x in r.values()),'B37 complete CSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B37 runtime not executed:'+r['id'])
    fe,inv,plans=[tables[p] for p in ('FE7B37-','INV7B37-','P7B37T-')]
    for e in current_link_errors(fe,inv,plans)+ledger_errors(tables['TR7B37-'],tables['TT7B37-'],fe):ck(False,e)
    v.proposed_tests(plans,'7B37');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,inv,plans)]
    v.related(plans,fids,'feature_ids');v.related(plans,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['TR7B37-']+tables['TT7B37-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(plans,'plans')):v.covered([lookup[r] for r in DEEPENED_IDS],pool,'B37 deepened '+label)
    for r in tables['RC7B37-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ck(r['evidence']==source_evidence_union(fs) and r['finding_ids']==unique('finding_ids') and r['acceptance_ids']==unique('acceptance_ids'),'B37 exact reconciliation union');v.related([r],fids,'feature_ids')
    for e in residual_errors(tables['RS7B37-'],rows('evidence/residual-disposition-07B36.csv'))+split_errors(tables['SP7B37-'],rows('evidence/split-register-07B36.csv'))+remaining_work_errors(tables['RW7B37-']):ck(False,e)
    hids={r['id'] for r in tables['H7B37-']};sids={r['id'] for r in tables['SP7B37-']};v.related(tables['RS7B37-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B37-'],hids,'handoff_ids')
    for stem in ('handoffs','questions'):
        for old,r in zip(rows(f'evidence/{stem}-07B36.csv'),rows(f'evidence/{stem}-07B37.csv')):ck(r['required_redacted_input'].startswith(old['required_redacted_input']),'B37 ALL H/Q input prefixes')
    ck(all(r['status']=='external-contract-or-policy-unresolved-not-absence-proof' for r in tables['H7B37-']),'B37 H unresolved');ck(all(r['status']=='unanswered-no-secrets-requested' for r in tables['Q7B37-']),'B37 Q unanswered')
    for n,(old,r) in enumerate(zip(rows('evidence/continuation-backlog-07B36.csv'),tables['BK7B37-']),1):ck(r['prior_backlog_id']==old['id']==f'BK7B36-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['required_work'].startswith(old['required_work']) and r['status']==old['status'],'B37 backlog ancestry/input/status')
    ck([r['status'] for r in tables['BK7B37-'][2:6]]==['not-started']*4,'B37 C unstarted')
    ad=tables['AD7B37-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids');ck(all(r['comparison_depth']==DEDUP_DEPTH and r['decision'] not in {'new-local-root','extended-existing-root-not-new'} for r in ad),'B37 no new/extension or inflated depth');ck([r['current_root_ids'] for r in ad[:2]]==DEEPENED_IDS,'B37 related159/160 only')
    screen=json.loads(v.read(v.AUDIT/'evidence/dedup-screen-07B37.json'))
    for e in dedup_errors(screen,frozen335):ck(False,e)
    for r in screen['selected_prior_finding_sections']+screen['additional_selected_extension_and_contract_sections']:
        ck(v.sha(v.AUDIT/r['artifact'])==r['artifact_sha256'],'B37 compared prior artifact identity');ls=v.read(v.AUDIT/r['artifact']).splitlines();ck(1<=r['start']<=r['end']<=len(ls),'B37 compared section boundary');ck(hashlib.sha256(('\n'.join(ls[r['start']-1:r['end']])+'\n').encode()).hexdigest()==r['section_utf8_sha256'],'B37 compared bounded section hash')
    names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,37)]
    before={r['path'] for name in names for r in rows(name)};paths=set(scope);rem=inventory.keys()-(before|paths)
    book=dict(selected_paths=4,prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(paths|before),complement=len(rem),complement_kinds=dict(collections.Counter(inventory[p]['kind'] for p in rem)))
    ck(book==dict(selected_paths=4,prior_union=428,overlap=4,new=0,union=428,complement=399,complement_kinds={'source':334,'generated-artifact':61,'project-or-resource':4}),'B37 path bookkeeping not capability completion')
    decision=json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B37.json'));ck(decision['bookkeeping']==book and decision['entry']==ENTRY and decision['selected_upstream_split']=='SP7B36-01','B37 bounded upstream authority')
    ck((decision['historical_metadata_screen_count'],decision['parent_path_matched_metadata_rows'],decision['selected_prior_report_sections'],decision['additional_selected_extension_contract_sections'],decision['selected_contract_slices'],decision['exploratory_context_slices'],decision['whole_local_source_bodies_reread'],decision['newly_completed_local_files'])==(335,71,8,2,16,5,0,0),'B37 honest bounded metadata/contract counts')
    ck(decision['new_root_ids']==[] and decision['existing_root_extensions']==[] and decision['registry_entire_raw_bytes_unchanged'] is True,'B37 scope zero new/ext')
    for k in ('selected_capability','entry_point','source_contract','output_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):ck(type(decision.get(k)) is str and len(decision[k])>20,'B37 scope responsibility:'+k)
    for k in ('all_historical_bodies_reviewed','counts_are_completion_percent_or_sessions','phase7C_started','phase8_authorized_or_started','repair_start_sync_known'):ck(decision[k] is False,'B37 no authority:'+k)
    ck(type(decision['exclusions']) is list and len(decision['exclusions'])==4,'B37 exclusions')
    wp='evidence/transfer-picker-witnesses-07B37.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B37 immutable witness');w,match=v.recompute(wp,'tools/check_transfer_picker_witnesses.py')
    for e in witness_metadata_errors(w):ck(False,e)
    ck(w['errors']==[],'B37 inert witness pass')
    for k,prefix,passkey in (('illustrations','ALG7B37-','assertions_passed'),('static_lexical_contract_checks','ST7B37-','documented_text_observation_matches')):
        v.sequential(w[k],prefix,20);v.related(w[k],known)
        for r in w[k]:ck(r[passkey] is True and r['source_application_executed'] is False and bool(r['limit']),'B37 witness safety');validate_source(v,r,scope)
    for k,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('context_reads_not_command_certification',CONTEXT_SLICES),('whole_local_rereads_not_new_completions',WHOLE_REREADS)):
        data=w[k];ck(tuple((r['path'],r['start'],r['end']) for r in data)==declared,'B37 declared reads')
        for r in data:ck(v.sha(v.ROOT/r['path'])==r['sha256'],'B37 read source identity');v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B37 source inclusion',phase=7)
    oldtexts=json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(oldtexts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        p=v.AUDIT/name;s=v.read(p)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',s):
            u=urlsplit(m[1]);target=(p.parent/unquote(u.path)).resolve()
            if u.scheme or m[1].startswith('#'):continue
            if target==(v.AUDIT/'evidence/checks-07B37.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B37 local link:'+name+':'+m[1])
        for m in source.finditer(s):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{z}' for a,z in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/name) for x in ('PHASE-07B37.md','PHASE-07-REMAINING-07B37.md','7B38','غير مأذونة','a83cb66','10ba215')),'B37 shared entrypoint:'+name)
    hp='evidence/historical-mode-verification-07B37.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B37 actual42 exists')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B37 actual42 archive identity');h=json.loads(v.read(v.AUDIT/hp))
        for e in historical_record_errors(h):ck(False,e)
        ck((h['checkout_head'],h['source_head'],h['branch'])==(ENTRY,v.HEAD,v.BRANCH),'B37 actual42 context')
        sources={p.relative_to(v.AUDIT).as_posix():p.read_bytes() for p in sorted((v.AUDIT/'tools').glob('*.py'))}
        for e in capture_source_errors(h,sources):ck(False,e)
        report['phase_7B37_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=42,capture_time_tool_count=139,historical_B36_source_assertion_inputs_not_execution_inventory=135,all_original52_B36_and1294_prior_cases_preserved=True,null_aggregates_unreported_not_zero=True,single_later_pin_only_inverted_in_memory=True,not_final_or_postpush_wholesale_replay=True)
    tools=['check_transfer_picker_witnesses.py','validate_transfer_picker_part.py','run_historical_invoice_picker_tests_07B37.py','test_transfer_picker_audit_validator.py']
    for n in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/n),filename=n)
        except SyntaxError as exc:ck(False,'B37 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);n=int(m[1]) if m else None;passed=run.returncode==0 and n==52;ck(passed,'B37 ALL52 documentary cases: '+(run.stderr[-14000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=n,expected_tests=52,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools;report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    execution={p.relative_to(v.AUDIT).as_posix():v.sha(p) for p in sorted((v.AUDIT/'tools').glob('*.py'))};ck(len(execution)==139,'B37 independent139 full tool inventory');report['validation']['current_execution_tool_inventory_sha256_not_original_application']=execution
    report.update(registry_used='findings.csv',validation_scope='current-through7B37-335-bounded-R4u-transfer-command-tail-zero-new-roots-not7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,38))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B38-proposed-R4v-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=163,phase_7B37=0,total_open_not_remediated=335,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:4,'phase_7B37_prior_union':428,'phase_7B37_overlap_with_prior_union':4,'phase_7B37_new_paths':0,'unique_union_not_line_or_execution_coverage':428,'inventory_only_no_selected_scope':399})
    report['phase_7B36_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256=SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_evidence_artifacts_hash_checked=1173,historical_check_record_overwritten=False,genuine_B36_stdout_sha256_unchanged=B36_CHECK_SHA,genuine_B36_receipt_sha256_unchanged=B36_RECEIPT_SHA,all335_dictionaries_ALLnext_phase_evidence_status_classification_exact=True,entire_raw336CRLF_bytes_exact=True,auxiliary_dispatcher_TEXT_not_executed=DISPATCHER_SNAPSHOT)
    report['phase_7B37_transfer_command_tail_trace_limits']=dict(transfer_request_boundaries=8,transfer_tail_boundaries=8,selected_source_paths=4,contract_slices=16,context_slices_not_certified=5,whole_local_source_bodies_reread=0,newly_completed_local_files=0,new_union_paths=0,new_root_ids=[],existing_root_extensions=[],existing_roots_deepened_without_registry_change=DEEPENED_IDS,features=16,invariants_not_executed=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_splits=3,modal_headers_fields_numbers_and_failure_boundaries_supplied_not_observed=True,number_helper_catch_return_distinct_from_nonreturn=True,field_header_operation_difference_unresolved_policy_not_new_root=True,previous_year_return_button_other_callers_and_SDK_not_certified=True,all_callers_or_historical_bodies_reviewed=False,repair_start_sync_unknown=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B37_illustrations_not_ERP_tests=20,phase_7B37_lexical_checks_not_ERP_tests=20,phase_7B37_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending;report['validation']['limit']=__doc__+' Actual42 summaries/raw stdout identities,not full streams or final/postpin/postpush wholesale replay. All32 B37 and all earlier operational plans not-executed. Potential014/108/132/145,020/021 and financial/ACL/stock/save/production barriers unchanged. B10 additive10vs120/equality1=10/G138 retained;next_phase8 planning only.'
