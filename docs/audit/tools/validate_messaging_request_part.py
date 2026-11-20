#!/usr/bin/env python3
"""Read-only B34/R4r request/await documentary checks,NOT ERP acceptance.

ZERO new roots and ZERO registry evidence extensions. P6-031/033 already
state shared chat/file interleaving;B34 deepens boundaries/controls without
recounting. ALL335 dictionaries and ENTIRE raw336CRLF bytes,including the
registry itself within1018/1022 protected entry materials,are immutable.
ALL1138 earlier cases incl52 B33 retained. Historical B33 OWN335/indexes/
preset33 uses123 source assertion identities and dispatcher TEXT through
child module-local A/Path only;not old code/global Path/shared-subprocess
mutation,overlay,protected edits,skips or rebaseline. Current LIVE34/versioned33/
API15/19 gates/127 execution tools checked separately. Actual39 exclusive
historical processes,only this helper's later sole pin inverted in memory.
20 contract+8 context/5 prior paths/0 wholefiles,union427/complement400 not
455FE/capability coverage.32 operational plans NOT executed. Opaque schedule,
DOM/element readiness,return and file-version flags SUPPLIED;no file bytes,
upload,provider acceptance/delivery,save,financial loss or SDK dirty proof.
Stored IWebElement is not silently retargeted after navigation. P6-031/032/
033/034/035 and107/108/132/145/163 retain their own scope/classification.
All SP01..03 remain7B;7B/7 partial,7C unstarted,8 unauthorized,repair start/sync
unknown. Session reference2026-11-16 and raw clocks distinct,not rewritten.
"""
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
from validate_output_route_part import historical_record_errors as historical38_errors
from check_messaging_request_witnesses import SOURCE_SLICES,EXPLORATORY_SLICES

ENTRY='dea2244267d74dd540af59c6e63b0f4362ab8c1c'
SNAPSHOT='evidence/findings-through-07B33.csv'
SNAPSHOT_SHA='ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B33.json'
SHARED_SHA='1a5ca8a8c507b9b45d1cceab171254370e402a753c7161400f804945d6c35c3f'
PROVENANCE_SHA='7896bd97cd77ddd7a334d6cf19c253f73aefff26c74d8b263302e06a0f76d65d'
DISPATCHER_SNAPSHOT='evidence/dispatcher-through-07B33.py.txt'
DISPATCHER_SHA='0c77fc3fb8d5d125dc9f22253c52295c85fef02f3d8cc319c4cbcc4e6ca3d13c'
B33_CHECK_SHA='48252270a6185a7c8274ecbd4c76ebc459ce92fdfcf73386975cd72c2445c171'
B33_RECEIPT_SHA='70d0533ae50c71871a6b41c82aed109e4d2154f2ca440ef1a9bd6fc0610faca0'
WITNESS_SHA='4739d9360470ac44abdd73577878a69e96fd7e20acb3901aa7941f2b1c2d7614'
HISTORICAL_RUN_SHA = 'd46dcd461814a12e3c4ac56d478e4e38159750a79c0ed83ed82377c5a05f0a0f'  # Pin only after exclusive actual39 capture.
DOCUMENTARY='none-documentary-metadata'
SCOPE_FILE='review-scope-07B34.csv'
NEW_IDS=[]
DEEPENED_IDS=['P6-031','P6-033']
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
PART_DOCS=('PHASE-07B34.md','WHATSAPP-REQUEST-CONTRACTS-07B34.md','VALIDATION-07B34.md',
           'PHASE-07-REMAINING-07B34.md','DATE-IDENTITY-NOTE-07B34.md')
TABLE_SPECS=(('request-ownership-lineage','RQ7B34-',8),('await-boundary-lineage','AW7B34-',8),
 ('feature-implementation-matrix','FE7B34-',16),('report-invariants','INV7B34-',16),
 ('acceptance-tests','P7B34T-',32),('report-reconciliation','RC7B34-',6),
 ('root-adjudication','AD7B34-',8),('residual-disposition','RS7B34-',14),
 ('split-register','SP7B34-',3),('handoffs','H7B34-',6),('questions','Q7B34-',6),
 ('remaining-workplan','RW7B34-',10),('continuation-backlog','BK7B34-',10))
SENTINELS={f'{p}{n:02d}' for p,ns in (
 ('RQ7B34-',(8,)),('AW7B34-',(8,)),('FE7B34-',(15,16)),('INV7B34-',(15,16)),
 ('P7B34T-',range(29,33)),('RC7B34-',(5,6)),('AD7B34-',(6,7)),
 ('RS7B34-',range(1,15)),('H7B34-',range(1,7)),('Q7B34-',range(1,7))) for n in ns}
DEDUP_DEPTH='all335-title-metadata-and33-five-path-registry-rows-plus20-selected-prior-report-bodies-and-bounded-request-source-not-all-historical-bodies'
RQ_GROUPS=((0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13),(14,15))
AW_GROUPS=((3,),(4,),(5,),(6,7),(8,),(9,10),(11,),(14,15))
FEATURE_ROOTS=('P6-033','P6-033','P6-031','P6-031;P6-033','P6-033','P6-033',
 'P6-033','P6-033','P6-033','P6-033','P6-033','P6-031;P6-033',
 'P6-032;P6-033','P6-034','H7B34-06','H7B34-06')


@contextmanager
def historical_b33_inputs(v,frozen335,texts,raw,sources,dispatcher):
    """OWN assertion data through a local Path subtype,never old Python code."""
    if (type(frozen335) is not list or len(frozen335)!=335
        or any(type(r) is not dict for r in frozen335)
        or len({r.get('id') for r in frozen335})!=335):
        raise ValueError('Exactly335 distinct OWN B33 rows')
    if type(texts) is not dict or set(texts)!=set(SHARED_DOCS) or any(type(s) is not str for s in texts.values()):
        raise ValueError('Three OWN shared index strings')
    if (type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=336
        or not raw.endswith(b'\r\n') or any(c in raw.replace(b'\r\n',b'') for c in (b'\r',b'\n'))):
        raise ValueError('OWN335/raw336CRLF/noBOM required')
    try:
        parsed=list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))
    except (UnicodeError,csv.Error) as exc:
        raise ValueError('Malformed OWN raw') from exc
    if parsed!=frozen335:
        raise ValueError('OWN rows/raw mismatch')
    if (type(sources) is not dict or len(sources)!=123
        or any(type(n) is not str or re.fullmatch(r'tools/[A-Za-z0-9_]+\.py',n) is None
               or type(h) is not str or re.fullmatch('[0-9a-f]{64}',h) is None for n,h in sources.items())
        or type(dispatcher) is not bytes or not dispatcher
        or sources.get('tools/validate_audit.py')!=hashlib.sha256(dispatcher).hexdigest()):
        raise ValueError('Exactly123 historical assertion identities and dispatcher TEXT')
    dispatcher.decode('utf8',errors='strict')
    original=v.AUDIT
    registry=(original/'findings.csv').resolve();dispatch=(original/'tools/validate_audit.py').resolve()
    tool_dir=(original/'tools').resolve();names=tuple(sorted(sources))
    class HistoricalOwnPath(type(original)):
        def read_bytes(self):
            resolved=self.resolve()
            if resolved==registry:return raw
            if resolved==dispatch:return dispatcher
            return super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            if self.resolve() in (registry,dispatch):
                return io.StringIO(self.read_bytes().decode(encoding or 'utf8',errors or 'strict'),newline=None).read()
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
    finally:
        v.AUDIT=original


class HistoricalB33Subprocess:
    def __init__(self,backend,python,tools):
        self.backend=backend
        self.expected=[python,'-B',str(tools/'test_output_route_audit_validator.py')]
        self.actual=[python,'-B',str(tools/'run_historical_output_route_tests_07B34.py'),'--through-part','B33']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):
        return self.backend.run(self.actual if type(args) is list and args==self.expected else args,*pos,**kwargs)


class HistoricalB33ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB33Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess' else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b33_validation(v,report,prior,prov,frozen335):
    ck=v.check
    for name,digest in ((SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),
        (DISPATCHER_SNAPSHOT,DISPATCHER_SHA),('evidence/provenance-07B34.json',PROVENANCE_SHA),
        ('evidence/checks-07B33.json',B33_CHECK_SHA),('evidence/official-capture-receipt-07B33.json',B33_RECEIPT_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B34 immutable entry:'+name)
    ck(prov['historical_artifact_count']==len(prov['historical_artifact_sha256'])==1018
       and prov['entry_artifact_count']==1022 and len(frozen335)==335,'B34 protected1018/OWN335')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B34 protected976→1018 continuity')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B34 pushed entry dea2244')
    ck(prov['declared_mutable_entry_paths']==sorted(SHARED_DOCS+('tools/validate_audit.py',))
       and prov['historical_artifact_sha256'].get('findings.csv')==SNAPSHOT_SHA,'B34 registry protected not mutable')
    ck((prov['registry_at_entry_snapshot'],prov['registry_at_entry_sha256'],prov['shared_indexes_at_entry'],prov['shared_indexes_at_entry_sha256'])
       ==(SNAPSHOT,SNAPSHOT_SHA,SHARED_SNAPSHOT,SHARED_SHA),'B34 OWN input identities')
    old=json.loads(v.read(v.AUDIT/'evidence/checks-07B33.json'));vv=old['validation'];s=vv['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='3f747085b8f91762f7626dd45331ca1f5ba9e9c1'
       and old['findings']['total_open_not_remediated']==335 and old['original_project_hashes_matching']==827
       and vv['errors']==[] and vv['current_output_record_pending_first_write_not_placeholder'] is False,'B34 genuine B33 capture at3f747 not dea2244')
    ck(len(s)==34 and sum(x['tests_reported'] for x in s.values())==1138
       and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B34 retained1138/34/976 official')
    er=prov['entry_actual_subprocess_receipt']
    ck(tuple(er.get(k) for k in ('checkout_head','process_exit_code','validation_errors','findings','originals_matching','documentary_cases','documentary_suites','outer_stderr_bytes'))
       ==(ENTRY,0,[],335,827,1138,34,0) and er['all1022_entry_artifacts_unchanged'] is True,'B34 actual independent entry1138/34')
    ep=v.AUDIT/prov['entry_stdout_retained_as_captured']
    ck(v.sha(ep)==er['stdout_sha256'] and len(ep.read_bytes())==er['stdout_bytes'],'B34 direct entry stdout identity')
    sources=prov['historical_checker_sources_at_entry']
    ck(len(sources)==123 and sources['tools/validate_audit.py']==DISPATCHER_SHA
       and prov['dispatcher_source_at_entry']==dict(path=DISPATCHER_SNAPSHOT,bytes=106098,sha256=DISPATCHER_SHA),'B34 historical123 assertions not actual127 tools')
    view=HistoricalB33ValidatorView(v);texts=json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b33_inputs(view,frozen335,texts,(v.AUDIT/SNAPSHOT).read_bytes(),sources,(v.AUDIT/DISPATCHER_SNAPSHOT).read_bytes()):
        yield view
    child=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_output_route_audit_validator.py']
    child.update(historical_parser_cutoff='B33-not-current-B34-default',all_original_cases_executed_unmodified=True,
        dedicated_child_launcher='tools/run_historical_output_route_tests_07B34.py',actual_subprocess_argv=view.subprocess.actual,
        no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,
        test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=123,
        auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B33-335-not-current-B34-state',
        phase_7B33_historical_input_mode='OWN335-raw336CRLF-indexes-presetB33-ALL52-child-module-local-A-Path-and123-source-assertion-inputs',
        phase_7B33_adapter_context=dict(entry_provenance='evidence/provenance-07B34.json',adapter_protected_artifacts_checked=1018,
            old_dispatcher_TEXT_not_executed=True,module_local_Path_type_for_source_reads_not_process_global=True,
            archived_stdout_not_rewritten_after_push=True,current_indexes_not_inputs=True))


def registry_preservation_errors(previous,current,raw,frozen,extensions):
    errors=[]
    if type(extensions) is not list or extensions!=[]:errors.append('B34 zero evidence extensions')
    if len(previous)!=335 or len(current)!=335 or current!=previous:
        errors.append('B34 ALL335 dictionaries/every field exact,no new roots')
    if type(raw) is not bytes or type(frozen) is not bytes:return errors+['B34 exact bytes required']
    if raw!=frozen:errors.append('B34 ENTIRE raw336 bytes exact,not just prefix')
    for data in (frozen,raw):
        if (data.startswith(b'\xef\xbb\xbf') or data.count(b'\r\n')!=336 or not data.endswith(b'\r\n')
            or any(c in data.replace(b'\r\n',b'') for c in (b'\r',b'\n'))):errors.append('B34 CRLF/noBOM')
    try:
        if (list(csv.DictReader(io.StringIO(raw.decode(),newline='')))!=current
            or list(csv.DictReader(io.StringIO(frozen.decode(),newline='')))!=previous):errors.append('B34 rows/raw mismatch')
    except (UnicodeError,csv.Error):errors.append('B34 malformed raw')
    return errors


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=252 or rows(current)[:252]!=rows(previous):return ['B34 G01..252 exact']
    return [] if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)==[f'G-{n:02d}' for n in range(1,257)] else ['B34 only G253..256 ordered']


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B34 ALL14 residuals']
    errors=[]
    for old,new in zip(upstream,current):
        if tuple(new.get(k) for k in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'))!=(old.get('id'),'evidence/residual-disposition-07B33.csv',row_sha(old),old.get('upstream_contract_ids')):errors.append('B34 residual ancestry/hash/contracts')
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B34 full upstream residual input prefix')
        mapped={x.replace('7B33-','7B34-') for x in old.get('current_handoff_or_split_ids','').split(';') if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B34 all mapped routes')
        if (new.get('disposition')!=old.get('disposition') or new.get('disposition') not in {'external-handoff','split-explicitly','assessment-source-bound'} or new.get('runtime_status')!='not-executed'):errors.append('B34 unchanged disposition not approval')
        for key in ('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):
            if type(new.get(key)) is not str or len(new[key])<20:errors.append('B34 substantive residual:'+key)
    return errors


def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return ['B34 ALL3 splits']
    errors=[]
    for old,new in zip(upstream,current):
        if (new.get('upstream_split_id'),new.get('upstream_artifact'),new.get('upstream_row_sha256'))!=(old.get('id'),'evidence/split-register-07B33.csv',row_sha(old)):errors.append('B34 split ancestry/hash')
        if not new.get('required_input','').startswith(old.get('required_input','')):errors.append('B34 full upstream split input')
        for key in ('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if type(new.get(key)) is not str or not new[key].strip():errors.append('B34 split responsibility:'+key)
        if new.get('status')!='explicit-further-static-split-not-started' or new.get('runtime_status')!='not-executed':errors.append('B34 future split not completed')
    return errors


def remaining_work_errors(data):
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4r-request-await-delivered-residuals-open']+['planned-not-started']*6
    if len(data)!=10:return ['B34 fourB sixC']
    return ['B34 work/permission'] if any(r.get('part_family')!=('7B' if i<4 else '7C') or r.get('status')!=expected[i] or r.get('runtime_status')!='not-executed' or r.get('counts_are_sessions_or_completion_percent')!='false' for i,r in enumerate(data)) else []


def current_link_errors(fe,inv,plans):
    if (len(fe),len(inv),len(plans))!=(16,16,32):return ['B34 FE16/INV16/T32']
    errors=[]
    for n,(f,i) in enumerate(zip(fe,inv),1):
        tids=';'.join(f'P7B34T-{k:02d}' for k in (2*n-1,2*n))
        if (f.get('id'),i.get('id'),i.get('feature_ids'),f.get('acceptance_ids'),i.get('acceptance_ids'),i.get('finding_ids'),f.get('finding_ids'))!=(f'FE7B34-{n:02d}',f'INV7B34-{n:02d}',f.get('id'),tids,tids,FEATURE_ROOTS[n-1],FEATURE_ROOTS[n-1]):errors.append('B34 exact links/retained roots')
        for t in plans[2*n-2:2*n]:
            if (t.get('feature_ids'),t.get('invariant_ids'),t.get('finding_ids'),t.get('status'))!=(f.get('id'),i.get('id'),f.get('finding_ids'),'not-executed'):errors.append('B34 linked plan nonexecution')
            for key in ('procedure','acceptance_criterion'):
                if type(t.get(key)) is not str or len(t[key])<35:errors.append('B34 substantive plan:'+key)
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim'):
            if type(f.get(key)) is not str or len(f[key])<20:errors.append('B34 capability responsibility:'+key)
    if len({r.get('required_invariant') for r in inv})!=16 or len({r.get('acceptance_criterion') for r in plans})!=32:errors.append('B34 distinct invariants/criteria')
    return errors


def ledger_errors(requests,awaits,fe):
    if len(fe)!=16:return ['B34 linked FE16']
    errors=[]
    for pool,groups,prefix in ((requests,RQ_GROUPS,'RQ7B34-'),(awaits,AW_GROUPS,'AW7B34-')):
        if len(pool)!=8:errors.append('B34 RQ8/AW8');continue
        for n,(r,indices) in enumerate(zip(pool,groups),1):
            fs=[fe[i] for i in indices];roots=';'.join(dict.fromkeys(x for f in fs for x in f['finding_ids'].split(';')))
            route=' | '.join(f['entry_point']+' → '+f['output_boundary'] for f in fs)
            if (r.get('id'),r.get('feature_ids'),r.get('finding_ids'),r.get('evidence'),r.get('source_to_output'),r.get('boundary'))!=(f'{prefix}{n:02d}',';'.join(f['id'] for f in fs),roots,source_evidence_union(fs),route,fs[0]['capability']):errors.append('B34 exact ordered request/await unions')
            for key in ('source_to_output','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence','observation'):
                if type(r.get(key)) is not str or not r[key].strip():errors.append('B34 lineage responsibility:'+key)
            if r.get('runtime_status')!='not-executed':errors.append('B34 lineage not runtime')
    return errors


def witness_metadata_errors(w):
    errors=[]
    for key in ('application_code_imported_or_executed','dotnet_wpf_sql_or_SDK_executed','browser_driver_provider_PDF_or_messages_executed','provider_acceptance_or_delivery_or_file_bytes_upload_proved','saved_invoice_dirty_DTO_contract_proved','application_remediation_performed','phase7C_started','phase8_authorized_or_started','all_callers_or_historical_bodies_certified'):
        if w.get(key) is not False:errors.append('B34 false-only:'+key)
    for key in ('schedule_targets_readiness_and_version_tokens_are_supplied','stored_elements_not_silently_retargeted','path_handoff_not_content_upload_or_delivery_proof','prior_roots_already_describe_this_mechanism'):
        if w.get(key) is not True:errors.append('B34 true-only:'+key)
    for key,n in (('illustration_count',20),('lexical_check_count',20),('selected_source_paths',5),('selected_contract_slices',20),('context_slices_not_certified',8),('whole_local_files_selected',0),('erp_runtime_tests_executed',0),('sql_or_external_service_tests_executed',0)):
        if type(w.get(key)) is not int or w[key]!=n:errors.append('B34 exact count:'+key)
    if (w.get('new_root_ids')!=[] or w.get('extended_existing_root_ids')!=[] or w.get('existing_roots_deepened_without_registry_change')!=DEEPENED_IDS or w.get('entry_checkout')!=ENTRY or w.get('audit_reference_date_utc')!='2026-11-16'):errors.append('B34 no new roots/reference/entry')
    e=w.get('retained_additive_B10_arithmetic_erratum',{})
    if e!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True) or any(type(e.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or e.get('protected_G138_not_rewritten') is not True:errors.append('B34 B10 additive erratum')
    return errors


def historical_record_errors(history):
    modes=history.get('historical_modes',[])
    if type(history.get('historical_mode_count')) is not int or history['historical_mode_count']!=39 or len(modes)!=39:return ['B34 exactly39 actual OWN modes']
    errors=historical38_errors(dict(historical_mode_count=38,historical_modes=modes[:38],errors=history.get('errors')))
    expected=dict(mode='B33',findings_total=335,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1138,audit_checker_self_test_suite_count=34,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0)
    last=modes[-1]
    for key,val in expected.items():
        if last.get(key)!=val or type(last.get(key)) is not type(val):errors.append('B34 OWN335/1138/34:'+key)
    expected_child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B33-not-current-B34-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_output_route_tests_07B34.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=123,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
    for key,val in expected_child.items():
        actual=(last.get('historical_B33_child') or {}).get(key)
        if actual!=val or type(actual) is not type(val):errors.append('B34 ALL52 B33 child:'+key)
    if type(last.get('stdout_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B34 stdout identity required')
    return errors


def capture_source_errors(history,sources):
    expected=history.get('checker_sources_at_capture',{})
    if set(expected)!=set(sources) or len(expected)!=127:return ['B34 capture tool set127']
    errors=[]
    for name,raw in sources.items():
        if name=='tools/validate_messaging_request_part.py':
            final="HISTORICAL_RUN_SHA = '"+str(HISTORICAL_RUN_SHA)+"'  # Pin only after exclusive actual39 capture."
            initial='HISTORICAL_RUN_SHA = None  # Pin only after exclusive actual39 capture.'
            text=raw.decode()
            if HISTORICAL_RUN_SHA is None or text.count(final)!=1:errors.append('B34 exact final pin required');continue
            raw=text.replace(final,initial).encode()
        if hashlib.sha256(raw).hexdigest()!=expected[name]:errors.append('B34 tool changed beyond single inverse pin:'+name)
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or type(prov.get('environment_clock_observed_utc')) is not str:errors.append('B34 reference/raw fields distinct')
    for val in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,'3f747085b8f91762f7626dd45331ca1f5ba9e9c1',B33_CHECK_SHA,B33_RECEIPT_SHA,DISPATCHER_SHA,WITNESS_SHA,'1018','1022','335','123','127'):
        if val not in note:errors.append('B34 identity:'+val)
    return errors


def dedup_errors(screen,frozen335):
    errors=[];meta=[{k:r[k] for k in ('id','title','severity','certainty','type','status')} for r in frozen335]
    if (screen.get('comparison_depth')!=DEDUP_DEPTH or screen.get('title_metadata_rows')!=meta
        or screen.get('all_historical_bodies_reviewed') is not False or screen.get('new_root_ids')!=[]
        or screen.get('existing_root_extensions')!=[] or screen.get('existing_roots_deepened_without_registry_change')!=DEEPENED_IDS
        or screen.get('registry_entire_raw_bytes_unchanged') is not True):errors.append('B34 honest zero-root metadata/body screen')
    paths=screen.get('five_path_screen',[])
    if len(paths)!=5 or len(set(paths))!=5:errors.append('B34 exact5 paths')
    matched=[r for r in frozen335 if any(p+':' in r['evidence'] for p in paths)]
    if len(matched)!=33 or screen.get('path_matching_registry_rows')!=[dict(id=r['id'],row_sha256=row_sha(r)) for r in matched]:errors.append('B34 exact33 path-matched rows')
    bodies=screen.get('selected_prior_finding_sections',[])
    if len(bodies)!=20 or len({r.get('finding_id') for r in bodies})!=20:errors.append('B34 selected20 bodies not all')
    if not {'P6-031','P6-033'}<={r.get('finding_id') for r in bodies}:errors.append('B34 existing interleaving roots must be compared')
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']==DOCUMENTARY:
        v.check(row['id'] in SENTINELS,'B34 undeclared documentary sentinel:'+row['id']);return
    v.check(row['id'] not in SENTINELS,'B34 fabricated source for documentary gate:'+row['id'])
    v.evidence(row['evidence'],row['id'])
    try:expanded=expanded_source_evidence(row['evidence'])
    except ValueError as exc:v.check(False,'B34 malformed evidence:'+str(exc));return
    v.scoped_evidence(expanded,scope,row['id']+' boundedB34',phase=7)


def extend_messaging_request(v,report,prov,frozen335):
    ck,rows=v.check,v.rows;current=rows('findings.csv');lookup={r['id']:r for r in current}
    for err in registry_preservation_errors(frozen335,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes(),rows('evidence/historical-extensions-07B34.csv')):ck(False,err)
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[],'B34 zero new finding headers')
    for root in ('P4-014','P7-108','P7-132','P7-145'):ck(lookup[root]['certainty']=='potential','B34 retained potential:'+root)
    ck(prov['new_root_ids']==[] and prov['existing_registry_evidence_extensions']==[] and prov['existing_roots_deepened_without_registry_change']==DEEPENED_IDS,'B34 no recount')
    for key in ('phase7C_started','phase8_authorized_or_started','application_remediation_performed','repair_start_or_sync_known'):ck(prov[key] is False,'B34 no start/sync:'+key)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B34 independent repair')
    for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[key]) is int and prov[key]==0,'B34 no runtime:'+key)
    for err in date_identity_errors(prov,v.read(v.AUDIT/PART_DOCS[4])):ck(False,err)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==5,'B34 five bounded paths')
    for r in selected:
        ck(r['path'] in original and r['review_state']=='bounded-request-await-and-context-not-whole-file-or-runtime' and bool(r['focus']),'B34 scope boundary')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    tables={};known=set(lookup)|{f'H7B34-{n:02d}' for n in range(1,7)}
    for stem,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+stem+'-07B34.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(type(x) is str and x.strip() for x in r.values()),'B34 complete CSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B34 no runtime claim:'+r['id'])
    fe,inv,plans=[tables[p] for p in ('FE7B34-','INV7B34-','P7B34T-')]
    for err in current_link_errors(fe,inv,plans)+ledger_errors(tables['RQ7B34-'],tables['AW7B34-'],fe):ck(False,err)
    v.proposed_tests(plans,'7B34');fids,iids,tids=[{r['id'] for r in p} for p in (fe,inv,plans)]
    v.related(plans,fids,'feature_ids');v.related(plans,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids')
    v.related(tables['RQ7B34-']+tables['AW7B34-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(plans,'plans')):v.covered([lookup[r] for r in DEEPENED_IDS],pool,'B34 existing roots '+label)
    for r in tables['RC7B34-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];unique=lambda key:';'.join(dict.fromkeys(x for f in fs for x in f[key].split(';')))
        ck(r['evidence']==source_evidence_union(fs) and r['finding_ids']==unique('finding_ids') and r['acceptance_ids']==unique('acceptance_ids'),'B34 exact reconciliation union');v.related([r],fids,'feature_ids')
    for err in residual_errors(tables['RS7B34-'],rows('evidence/residual-disposition-07B33.csv'))+split_errors(tables['SP7B34-'],rows('evidence/split-register-07B33.csv'))+remaining_work_errors(tables['RW7B34-']):ck(False,err)
    hids={r['id'] for r in tables['H7B34-']};sids={r['id'] for r in tables['SP7B34-']}
    v.related(tables['RS7B34-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B34-'],hids,'handoff_ids')
    for stem in ('handoffs','questions'):
        for old,r in zip(rows(f'evidence/{stem}-07B33.csv'),rows(f'evidence/{stem}-07B34.csv')):ck(r['required_redacted_input'].startswith(old['required_redacted_input']),'B34 ALL H/Q upstream input prefixes')
    ck(all(r['status']=='external-contract-or-policy-unresolved-not-absence-proof' for r in tables['H7B34-']),'B34 H unresolved')
    ck(all(r['status']=='unanswered-no-secrets-requested' for r in tables['Q7B34-']),'B34 Q unanswered')
    for n,r in enumerate(tables['BK7B34-'],1):ck(r['prior_backlog_id']==f'BK7B33-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B34 backlog ancestry')
    ck([r['status'] for r in tables['BK7B34-'][2:6]]==['not-started']*4,'B34 C unstarted')
    ad=tables['AD7B34-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck(not any(r['decision'] in ('new-local-root','extended-existing-root-not-new') for r in ad),'B34 no new root or registry extension')
    ck([r['current_root_ids'] for r in ad if r['decision']=='existing-mechanism-deepened-no-registry-change']==['P6-031;P6-033','P6-033'] and all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B34 honest prior mechanism depth')
    screen=json.loads(v.read(v.AUDIT/'evidence/dedup-screen-07B34.json'))
    for err in dedup_errors(screen,frozen335):ck(False,err)
    for r in screen['selected_prior_finding_sections']:
        ck(v.sha(v.AUDIT/r['artifact'])==r['artifact_sha256'],'B34 compared report identity');lines=v.read(v.AUDIT/r['artifact']).splitlines()
        ck(1<=r['start']<=r['end']<=len(lines) and lines[r['start']-1].startswith('### '+r['finding_id']+' '),'B34 selected body boundary')
        section=('\n'.join(lines[r['start']-1:r['end']])+'\n').encode();ck(hashlib.sha256(section).hexdigest()==r['section_utf8_sha256'],'B34 compared body hash')
    names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,34)]
    before={r['path'] for n in names for r in rows(n)};paths=set(scope);rem=original.keys()-(before|paths)
    book=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(book==dict(selected_paths=5,prior_union=427,overlap=5,new=0,union=427,complement=400,complement_kinds={'source':335,'generated-artifact':61,'project-or-resource':4}),'B34 path bookkeeping not completion')
    decision=json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B34.json'))
    ck(decision['bookkeeping']==book and decision['selected_upstream_split']=='SP7B33-01' and decision['entry']==ENTRY and decision['historical_metadata_screen_count']==335 and decision['parent_path_matched_metadata_rows']==33 and decision['selected_prior_report_sections']==20 and decision['all_historical_bodies_reviewed'] is False,'B34 bounded authority/dedup')
    ck((decision['selected_contract_slices'],decision['exploratory_context_slices'],decision['whole_local_files'])==(20,8,0) and decision['new_root_ids']==[] and decision['existing_root_extensions']==[] and decision['registry_entire_raw_bytes_unchanged'] is True,'B34 bounded zero-root slice')
    for key in ('selected_capability','entry_point','source_contract','output_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):ck(type(decision.get(key)) is str and len(decision[key])>20,'B34 scoped responsibility:'+key)
    ck(type(decision.get('exclusions')) is list and len(decision['exclusions'])==4,'B34 exclusions')
    for key in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions','repair_start_sync_known'):ck(decision[key] is False,'B34 no authority:'+key)
    wp='evidence/messaging-request-witnesses-07B34.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B34 immutable witness')
    witness,match=v.recompute(wp,'tools/check_messaging_request_witnesses.py')
    for err in witness_metadata_errors(witness):ck(False,err)
    ck(witness['errors']==[],'B34 inert witness pass')
    for key,prefix,flag in (('illustrations','ALG7B34-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B34-','documented_text_observation_matches')):
        v.sequential(witness[key],prefix,20);v.related(witness[key],known)
        for r in witness[key]:
            ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B34 witness safety');validate_source(v,r,scope)
    for key,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('exploratory_source_reads_not_capability_certification',EXPLORATORY_SLICES)):
        data=witness[key];ck(tuple((r['path'],r['start'],r['end']) for r in data)==declared,'B34 declared reads')
        for r in data:
            ck(r['whole_local_file_selected'] is False and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True and v.sha(v.ROOT/r['path'])==r['sha256'],'B34 read identity')
            v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B34 source read',phase=7)
    oldtexts=json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for err in group_row_errors(oldtexts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,err)
    pending=False
    source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            u=urlsplit(m[1]);target=(doc.parent/unquote(u.path)).resolve()
            if u.scheme or m[1].startswith('#'):continue
            if target==(v.AUDIT/'evidence/checks-07B34.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B34 local link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{z}' for a,z in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B34.md','PHASE-07-REMAINING-07B34.md','7B35','غير مأذونة','dea2244','10ba215')),'B34 shared entrypoint:'+name)
    hp='evidence/historical-mode-verification-07B34.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B34 actual39 exists')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B34 actual39 identity');history=json.loads(v.read(v.AUDIT/hp))
        for err in historical_record_errors(history):ck(False,err)
        ck((history['checkout_head'],history['source_head'],history['branch'])==(ENTRY,v.HEAD,v.BRANCH),'B34 history identity')
        sources={p.relative_to(v.AUDIT).as_posix():p.read_bytes() for p in sorted((v.AUDIT/'tools').glob('*.py'))}
        for err in capture_source_errors(history,sources):ck(False,err)
        report['phase_7B34_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=39,capture_time_tool_count=127,historical_B33_source_assertion_inputs_not_execution_inventory=123,all_original52_B33_and1138_prior_cases_preserved=True,null_aggregates_unreported_not_zero=True,single_later_pin_only_inverted_in_memory=True,not_final_or_postpush_wholesale_replay=True)
    tools=['check_messaging_request_witnesses.py','validate_messaging_request_part.py','run_historical_output_route_tests_07B34.py','test_messaging_request_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:ck(False,'B34 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==52
    ck(passed,'B34 ALL52 documentary cases: '+(run.stderr[-14000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=52,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    execution={p.relative_to(v.AUDIT).as_posix():v.sha(p) for p in sorted((v.AUDIT/'tools').glob('*.py'))};ck(len(execution)==127,'B34 full127 execution inventory')
    report['validation']['current_execution_tool_inventory_sha256_not_original_application']=execution
    report.update(registry_used='findings.csv',validation_scope='current-through7B34-335-bounded-R4r-request-await-zero-new-roots-not7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,35))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B35-proposed-R4s-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=163,phase_7B34=0,total_open_not_remediated=335,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:5,'phase_7B34_prior_union':427,'phase_7B34_overlap_with_prior_union':5,'phase_7B34_new_paths':0,'unique_union_not_line_or_execution_coverage':427,'inventory_only_no_selected_scope':400})
    report['phase_7B33_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256=SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_evidence_artifacts_hash_checked=1018,historical_check_record_overwritten=False,genuine_B33_stdout_sha256_unchanged=B33_CHECK_SHA,genuine_B33_receipt_sha256_unchanged=B33_RECEIPT_SHA,all335_dictionaries_ALLnext_phase_evidence_status_classification_exact=True,entire_raw336CRLF_bytes_exact=True,auxiliary_dispatcher_TEXT_not_executed=DISPATCHER_SNAPSHOT)
    report['phase_7B34_request_await_trace_limits']=dict(request_ownership_boundaries=8,await_boundaries=8,selected_source_paths=5,contract_slices=20,context_slices_not_certified=8,whole_files=0,new_union_paths=0,new_root_ids=[],existing_root_extensions=[],existing_roots_deepened_without_registry_change=DEEPENED_IDS,features=16,invariants_not_executed=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_splits=3,source_interleaving_not_observed_message_or_file_bytes=True,stored_elements_not_silently_retargeted=True,readiness_and_interleaving_are_supplied=True,unknown_DTO_SDK_DOM_contracts_remain_unknown=True,all_callers_or_historical_bodies_reviewed=False,repair_start_sync_unknown=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B34_illustrations_not_ERP_tests=20,phase_7B34_lexical_checks_not_ERP_tests=20,phase_7B34_contract_reads_not_whole_files=20,phase_7B34_context_reads_not_capability_certification=8,phase_7B34_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=__doc__+' Actual39 summaries/raw stdout identities,not full streams or final/postpin/postpush wholesale replay. All32 B34/B33/B32/B31/B30/B29/B28 and36 B27 acceptance plans not-executed. Potential014/108/132/145,020/021 and financial/ACL/stock/save/production barriers remain. B10 additive10vs120/equality1=10/G138 retained;next_phase8 planning only.'
