#!/usr/bin/env python3
"""Read-only B32/R4p editor event/close/dirty-contract documentary checks.

One162: authored XAML+constructor registration has one owner twice; Closing
may ask twice and returning F6 may request validation twice,NOT two saves.
F5 sets Handled; Cancel does not suppress the next Closing delegate. Supplied
callbacks/flags/replies/SDK setter profiles are NOT observed WPF/DTO behavior.
Header dirty propagation stays unresolved.132 stays potential.159/160/161/046
are exact,not new event/editor/field/null/exception roots.22 contract slices,
9 context slices/5 prior paths/0wholefiles,427/400 bookkeeping not coverage.
ALL333 dictionaries/full raw334CRLF prefix/G244/827 originals and942/947 entry
artifacts retained. ALL1034 original cases,including48 B31 and52 B30,unchanged.
B31 OWN333/indexes/presetB31/module-local A/Path/115 source-assertion inputs
and dispatcher TEXT,not old code or actual119 execution tool inventory. Actual
B32 parser/19 gates/versionedB31/API15/119 tools checked independently. Only
one later helper pin is inverted in memory for the actual37 capture. No skip,
rebaseline,disk overlay,global Path/subprocess mutation or ERP execution.
All32 plans not-executed.7B/7partial,R4q/B33 or reasoned split,7Cunstarted,
8unauthorized,repair start/sync unknown. Reference16,raw clocks separate.
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
from validate_navigation_load_part import historical_record_errors as historical36_errors
from check_editor_close_witnesses import SOURCE_SLICES,EXPLORATORY_SLICES
ENTRY='0bbadbe9f86a7ded7bbb1d2bcce209c7eda551fb'
SNAPSHOT='evidence/findings-through-07B31.csv';SNAPSHOT_SHA='d418c0af34f4806253b5937e947ceb00fe5abc85362e62ef391815f51e51373c'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B31.json';SHARED_SHA='10efcf3bda1de4ce7c4c2423887eb587e57735b0d24da7ea215967b2d216bc2a'
PROVENANCE_SHA='9a732b980b861422d78aee7f87db5f046673b6e529131e020fa1fd5da58915f2'
DISPATCHER_SNAPSHOT='evidence/dispatcher-through-07B31.py.txt';DISPATCHER_SHA='39dec717c7fc9229d0c8e4dcef5741e992eeea8a55342047081c43589be38b03'
B31_CHECK_SHA='ee392f76b76550a20bec4fa15c0787fe7d2716e9711dab15b0ea031d5873de83'
WITNESS_SHA='c22c31dfc7893bfd2c47864434daf8b99700cc71631d740f320a23cbf2ef37c7'
HISTORICAL_RUN_SHA = '04fc018cf00ca03fef80985c04735d41fa3525f051b820afe6e6cf7c67a25f1a'  # Pin only after exclusive actual37 capture.
DOCUMENTARY='none-documentary-metadata';SCOPE_FILE='review-scope-07B32.csv';NEW_IDS=['P7-162'];EXTENDED_IDS=[]
PART_DOCS=('PHASE-07B32.md','EDITOR-CLOSE-CONTRACTS-07B32.md','VALIDATION-07B32.md','PHASE-07-REMAINING-07B32.md','DATE-IDENTITY-NOTE-07B32.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS=(('event-ownership-lineage','EO7B32-',8),('dirty-guard-lineage','DG7B32-',8),('feature-implementation-matrix','FE7B32-',16),('report-invariants','INV7B32-',16),('acceptance-tests','P7B32T-',32),('report-reconciliation','RC7B32-',6),('root-adjudication','AD7B32-',8),('residual-disposition','RS7B32-',14),('split-register','SP7B32-',3),('handoffs','H7B32-',6),('questions','Q7B32-',6),('remaining-workplan','RW7B32-',10),('continuation-backlog','BK7B32-',10))
SENTINELS={f'{p}{n:02d}' for p,nums in (('EO7B32-',(8,)),('FE7B32-',(15,16)),('INV7B32-',(15,16)),('P7B32T-',range(29,33)),('RC7B32-',(5,6)),('AD7B32-',(7,8)),('RS7B32-',range(1,15)),('H7B32-',range(1,7)),('Q7B32-',range(1,7))) for n in nums}
DEDUP_DEPTH='all333-title-metadata-and27-parent-path-rows-plus-selected-event-bodies-and-protected-nearest-root-reports-not-all-historical-bodies'
EVENT_GROUPS=((0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13),(14,15));DIRTY_GROUPS=((6,),(7,),(8,),(9,),(10,),(11,),(12,),(13,))


@contextmanager
def historical_b31_inputs(v,frozen333,texts,raw,sources,dispatcher):
    """Own ASSERTION data,through this module's local Path view only.

    The historical child's local Path(v.__file__) reads canonical historical
    TEXT,not old functions. No process-global pathlib or subprocess patch.
    Each yielded dictionary is fresh; all identities restore on exceptions.
    """
    if type(frozen333) is not list or len(frozen333)!=333 or any(type(r) is not dict for r in frozen333) or len({r.get('id') for r in frozen333})!=333:raise ValueError('Exactly333 distinct OWN B31 rows')
    if type(texts) is not dict or set(texts)!=set(SHARED_DOCS) or any(type(x) is not str for x in texts.values()):raise ValueError('Three OWN shared index strings')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=334 or not raw.endswith(b'\r\n') or any(x in raw.replace(b'\r\n',b'') for x in (b'\r',b'\n')):raise ValueError('OWN333 raw334CRLF noBOM required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))
    except (UnicodeError,csv.Error) as exc:raise ValueError('Malformed OWN raw') from exc
    if parsed!=frozen333:raise ValueError('OWN rows/raw mismatch')
    if (type(sources) is not dict or len(sources)!=115 or any(type(n) is not str or re.fullmatch(r'tools/[A-Za-z0-9_]+\.py',n) is None or type(h) is not str or re.fullmatch('[0-9a-f]{64}',h) is None for n,h in sources.items()) or type(dispatcher) is not bytes or not dispatcher or sources.get('tools/validate_audit.py')!=hashlib.sha256(dispatcher).hexdigest()):raise ValueError('Exactly115 historical source identities and matching TEXT')
    dispatcher.decode('utf8',errors='strict')
    original=v.AUDIT;registry=(original/'findings.csv').resolve();dispatch=(original/'tools/validate_audit.py').resolve();tool_dir=(original/'tools').resolve();names=tuple(sorted(sources))
    class HistoricalOwnPath(type(original)):
        def read_bytes(self):
            resolved=self.resolve()
            if resolved==registry:return raw
            if resolved==dispatch:return dispatcher
            return super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            if self.resolve() in (registry,dispatch):return io.StringIO(self.read_bytes().decode(encoding or 'utf8',errors or 'strict'),newline=None).read()
            return super().read_text(encoding=encoding,errors=errors)
        def glob(self,pattern,*args,**kwargs):
            if self.resolve()==tool_dir and pattern=='*.py':
                for name in names:yield type(self)(original/name)
            else:yield from super().glob(pattern,*args,**kwargs)
    try:
        v.AUDIT=HistoricalOwnPath(original)
        with historical_b1_inputs(v,frozen333,texts):yield
    finally:v.AUDIT=original


class HistoricalB31Subprocess:
    def __init__(self,backend,python,tools):
        self.backend=backend;self.expected=[python,'-B',str(tools/'test_navigation_load_audit_validator.py')]
        self.actual=[python,'-B',str(tools/'run_historical_navigation_load_tests_07B32.py'),'--through-part','B31']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB31ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target);object.__setattr__(self,'_subprocess',HistoricalB31Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess' else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b31_validation(v,report,prior,prov,frozen333):
    ck=v.check
    for name,h in ((SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),(DISPATCHER_SNAPSHOT,DISPATCHER_SHA),('evidence/provenance-07B32.json',PROVENANCE_SHA),('evidence/checks-07B31-final.json',B31_CHECK_SHA)):ck(v.sha(v.AUDIT/name)==h,'B32 immutable entry:'+name)
    ck(prov['historical_artifact_count']==len(prov['historical_artifact_sha256'])==942 and len(frozen333)==333,'B32 protected942/OWN333')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B32 protected900→942 continuity')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B32 pushed entry0bb')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B32 own input identities')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B31-final.json'));vv=old['validation'];s=vv['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='038a18b74acb92c35a6172d4619fee5712424489' and old['findings']['total_open_not_remediated']==333 and old['original_project_hashes_matching']==827 and vv['errors']==[] and vv['current_output_record_pending_first_write_not_placeholder'] is False,'B32 genuine official B31 captured038 not delivery0bb')
    ck(len(s)==32 and sum(x['tests_reported'] for x in s.values())==1034 and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B32 genuine1034/32/900')
    r=prov['entry_actual_subprocess_receipt'];ck(r['checkout_head']==ENTRY and r['exit_code']==0 and r['errors']==[] and r['findings']==333 and r['originals']==827 and r['cases']==1034 and r['suites']==32 and r['all947_unchanged'] is True and r['stderr_bytes']==0,'B32 actual independent entry1034/32')
    src=prov['historical_checker_sources_at_entry'];meta=prov['dispatcher_source_at_entry']
    ck(len(src)==115 and src['tools/validate_audit.py']==DISPATCHER_SHA and meta['path']==DISPATCHER_SNAPSHOT and meta['bytes']==103230 and meta['sha256']==DISPATCHER_SHA,'B32 historical115 assertion inputs not119 execution tools')
    view=HistoricalB31ValidatorView(v);texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b31_inputs(view,frozen333,texts,(v.AUDIT/SNAPSHOT).read_bytes(),src,(v.AUDIT/DISPATCHER_SNAPSHOT).read_bytes()):yield view
    rec=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_navigation_load_audit_validator.py']
    rec.update(historical_parser_cutoff='B31-not-current-B32-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_navigation_load_tests_07B32.py',actual_subprocess_argv=view.subprocess.actual,no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=115,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B31-333-not-current-state',phase_7B31_historical_input_mode='OWN333-raw334CRLF-indexes-presetB31-ALL48-child-module-local-A-Path-and115-source-assertion-inputs',phase_7B31_adapter_context=dict(entry_provenance='evidence/provenance-07B32.json',adapter_protected_artifacts_checked=942,old_dispatcher_TEXT_not_executed=True,module_local_Path_type_for_source_reads_not_process_global=True,archived_stdout_not_rewritten_after_push=True,current_registry_and_indexes_not_inputs=True))


def registry_preservation_errors(previous,current,raw,frozen,extensions):
    errors=[]
    if type(extensions) is not list or extensions!=[]:errors.append('B32 no historical extensions allowed')
    if len(previous)!=333 or len(current)!=334:return errors+['B32 OWN333 plus one162 required']
    if current[:333]!=previous:errors.append('B32 ALL333 dictionaries including159/160/161 and ALLnext_phase exact')
    if [r.get('id') for r in current[333:]]!=NEW_IDS or len({r.get('id') for r in current})!=334:errors.append('B32 only one appended162')
    if type(raw) is not bytes or type(frozen) is not bytes:return errors+['B32 exact bytes required']
    for data,n in ((frozen,334),(raw,335)):
        if data.startswith(b'\xef\xbb\xbf') or data.count(b'\r\n')!=n or not data.endswith(b'\r\n') or any(x in data.replace(b'\r\n',b'') for x in (b'\r',b'\n')):errors.append('B32 exact CRLF/noBOM')
    if not raw.startswith(frozen):errors.append('B32 entire old raw334 prefix exact')
    try:
        if list(csv.DictReader(io.StringIO(raw.decode(),newline='')))!=current or list(csv.DictReader(io.StringIO(frozen.decode(),newline='')))!=previous:errors.append('B32 rows/raw mismatch')
    except (UnicodeError,csv.Error):errors.append('B32 malformed raw registry')
    return errors


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=244 or rows(current)[:244]!=rows(previous):return ['B32 G01..244 exact']
    return [] if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)==[f'G-{n:02d}' for n in range(1,249)] else ['B32 only G245..248 ordered']


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B32 all14 residuals']
    errors=[]
    for old,new in zip(upstream,current):
        if (new.get('upstream_residual_id')!=old.get('id') or new.get('upstream_artifact')!='evidence/residual-disposition-07B31.csv' or new.get('upstream_row_sha256')!=row_sha(old) or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):errors.append('B32 residual ancestry/hash/contracts')
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B32 old input full prefix')
        mapped={x.replace('7B31-','7B32-') for x in old.get('current_handoff_or_split_ids','').split(';') if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B32 all mapped routes')
        if new.get('disposition')!=old.get('disposition') or new.get('disposition') not in {'external-handoff','split-explicitly','assessment-source-bound'} or new.get('runtime_status')!='not-executed':errors.append('B32 retained dispositions not approvals')
        for k in ('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):
            if type(new.get(k)) is not str or len(new[k])<20:errors.append('B32 substantive residual:'+k)
    return errors


def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return ['B32 all3 splits']
    errors=[]
    for old,new in zip(upstream,current):
        if new.get('upstream_split_id')!=old.get('id') or new.get('upstream_artifact')!='evidence/split-register-07B31.csv' or new.get('upstream_row_sha256')!=row_sha(old):errors.append('B32 split ancestry/hash')
        if not new.get('required_input','').startswith(old.get('required_input','')):errors.append('B32 all old split input')
        for k in ('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if type(new.get(k)) is not str or not new[k].strip():errors.append('B32 split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started' or new.get('runtime_status')!='not-executed':errors.append('B32 future splits not completion/session')
    return errors


def remaining_work_errors(data):
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4p-editor-events-delivered-residuals-open']+['planned-not-started']*6
    if len(data)!=10:return ['B32 four B six C']
    return ['B32 remaining work or permission'] if any(r.get('part_family')!=('7B' if i<4 else '7C') or r.get('status')!=expected[i] or r.get('runtime_status')!='not-executed' or r.get('counts_are_sessions_or_completion_percent')!='false' for i,r in enumerate(data)) else []


def current_link_errors(fe,inv,plans):
    if (len(fe),len(inv),len(plans))!=(16,16,32):return ['B32 FE16/INV16/T32']
    errors=[]
    for n,(f,i) in enumerate(zip(fe,inv),1):
        tids=';'.join(f'P7B32T-{k:02d}' for k in (2*n-1,2*n));paired=plans[2*n-2:2*n]
        if f.get('id')!=f'FE7B32-{n:02d}' or i.get('id')!=f'INV7B32-{n:02d}' or i.get('feature_ids')!=f.get('id') or f.get('acceptance_ids')!=tids or i.get('acceptance_ids')!=tids or i.get('finding_ids')!=f.get('finding_ids'):errors.append('B32 exact bidirectional feature/invariant/plan links')
        if n<=4 and f.get('finding_ids')!='P7-162':errors.append('B32 root162 capabilities1..4')
        for t in paired:
            if t.get('feature_ids')!=f.get('id') or t.get('invariant_ids')!=i.get('id') or t.get('finding_ids')!=f.get('finding_ids') or t.get('status')!='not-executed':errors.append('B32 linked plan nonexecution')
            for k in ('procedure','acceptance_criterion'):
                if type(t.get(k)) is not str or len(t[k])<35:errors.append('B32 substantive plan:'+k)
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim'):
            if type(f.get(k)) is not str or len(f[k])<20:errors.append('B32 capability responsibility:'+k)
    if len({r.get('required_invariant') for r in inv})!=16 or len({r.get('acceptance_criterion') for r in plans})!=32:errors.append('B32 distinct substantive invariants/criteria')
    return errors


def ledger_errors(events,dirty,fe):
    if len(fe)!=16:return ['B32 linked FE16 required']
    errors=[]
    for pool,groups,prefix in ((events,EVENT_GROUPS,'EO7B32-'),(dirty,DIRTY_GROUPS,'DG7B32-')):
        if len(pool)!=8:errors.append('B32 EO8/DG8 required');continue
        for n,(r,indices) in enumerate(zip(pool,groups),1):
            fs=[fe[i] for i in indices];roots=';'.join(dict.fromkeys(x for f in fs for x in f['finding_ids'].split(';')))
            ev=DOCUMENTARY if indices[0]>=14 else source_evidence_union(fs)
            route=' | '.join(f['entry_point']+' → '+f['output_boundary'] for f in fs)
            if r.get('id')!=f'{prefix}{n:02d}' or r.get('feature_ids')!=';'.join(f['id'] for f in fs) or r.get('finding_ids')!=roots or r.get('evidence')!=ev or r.get('source_to_output')!=route or r.get('boundary')!=fs[0]['capability']:errors.append('B32 ordered exact event/dirty lineage links/source union')
            for k in ('source_to_output','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence','observation'):
                if type(r.get(k)) is not str or not r[k].strip():errors.append('B32 lineage responsibility:'+k)
            if r.get('runtime_status')!='not-executed':errors.append('B32 lineage not runtime')
    return errors


def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_SDK_executed','compiled_BAML_or_generated_code_executed','persisted_duplicate_save_or_financial_loss_claimed','IsUpdated_propagation_or_SDK_defaults_proved','stable_post_event_state_claimed','application_remediation_performed','phase7C_started','phase8_authorized_or_started'):
        if w.get(k) is not False:errors.append('B32 false-only:'+k)
    for k in ('author_source_attachments_not_observed_runtime_count','header_setter_profiles_are_supplied_not_SDK_evidence','unknown_setter_profile_remains_unknown','callbacks_and_event_outcomes_supplied','F5_Handled_control_prevents_blanket_duplicate_key_claim','validation_requests_not_successful_saves'):
        if w.get(k) is not True:errors.append('B32 true-only:'+k)
    for k,n in (('illustration_count',20),('lexical_check_count',20),('selected_source_paths',5),('selected_contract_slices',22),('context_slices_not_certified',9),('whole_local_files_selected',0),('authored_sale_Closing_attachments',2),('authored_purchase_Closing_attachments_in_selected_constructor_and_XAML',1),('erp_runtime_tests_executed',0),('sql_or_external_service_tests_executed',0)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B32 exact count:'+k)
    if w.get('new_root_ids')!=NEW_IDS or w.get('extended_existing_root_ids')!=[] or w.get('entry_checkout')!=ENTRY or w.get('audit_reference_date_utc')!='2026-11-16':errors.append('B32 root/date/entry')
    erratum=w.get('retained_additive_B10_arithmetic_erratum',{})
    if erratum!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True) or any(type(erratum.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or erratum.get('protected_G138_not_rewritten') is not True:errors.append('B32 B10 additive erratum')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=37 or len(modes)!=37:return ['B32 exactly37 actual OWN modes']
    errors=historical36_errors(dict(historical_mode_count=36,historical_modes=modes[:36],errors=h.get('errors')))
    last=modes[-1]
    for k,val in dict(mode='B31',findings_total=333,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1034,audit_checker_self_test_suite_count=32,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0).items():
        if last.get(k)!=val or type(last.get(k)) is not type(val):errors.append('B32 OWN333/1034/32:'+k)
    for k,val in dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',historical_parser_cutoff='B31-not-current-B32-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_navigation_load_tests_07B32.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=115,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True).items():
        value=(last.get('historical_B31_child') or {}).get(k)
        if value!=val or type(value) is not type(val):errors.append('B32 ALL48 B31 child:'+k)
    if type(last.get('stdout_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B32 stdout SHA required')
    return errors


def capture_source_errors(history,sources):
    expected=history.get('checker_sources_at_capture',{});errors=[]
    if set(expected)!=set(sources) or len(expected)!=119:return ['B32 capture tool set119']
    for name,raw in sources.items():
        if name=='tools/validate_editor_close_part.py':
            final="HISTORICAL_RUN_SHA = '"+str(HISTORICAL_RUN_SHA)+"'  # Pin only after exclusive actual37 capture."
            initial='HISTORICAL_RUN_SHA = None  # Pin only after exclusive actual37 capture.'
            text=raw.decode()
            if HISTORICAL_RUN_SHA is None or text.count(final)!=1:errors.append('B32 exact final pin required');continue
            raw=text.replace(final,initial).encode()
        if hashlib.sha256(raw).hexdigest()!=expected[name]:errors.append('B32 tool changed beyond single inverse pin:'+name)
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or type(prov.get('environment_clock_observed_utc')) is not str:errors.append('B32 date reference/raw fields')
    for token in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,'038a18b74acb92c35a6172d4619fee5712424489',B31_CHECK_SHA,DISPATCHER_SHA,WITNESS_SHA,'283432','942','947','333','115','119'):
        if token not in note:errors.append('B32 additive identity:'+token)
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id'] in SENTINELS,'B32 undeclared documentary sentinel:'+row['id']);return
    v.check(row['id'] not in SENTINELS,'B32 fabricated source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
    try:expanded=expanded_source_evidence(row['evidence'])
    except ValueError as exc:v.check(False,'B32 invalid source:'+str(exc));return
    v.scoped_evidence(expanded,scope,row['id']+' boundedB32',phase=7)


def extend_editor_close(v,report,prov,frozen333):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[333:];ext=rows('evidence/historical-extensions-07B32.csv')
    for err in registry_preservation_errors(frozen333,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes(),ext):ck(False,err)
    v.distributions(new,dict(Medium=1),dict(confirmed=1),'B32 only');ck(len(new)==1,'B32 exactly162')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B32 state not authorization')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B32 exact registry/report title')
    lookup={r['id']:r for r in current}
    for root in ('P4-014','P7-132','P7-145'):ck(lookup[root]['certainty']=='potential','B32 retained potential:'+root)
    for root in ('P7-046','P7-158','P7-159','P7-160','P7-161','P4-020','P4-021'):ck(lookup[root]==next(r for r in frozen333 if r['id']==root),'B32 prior root exact:'+root)
    for k in ('phase7C_started','phase8_authorized_or_started','application_remediation_performed','repair_start_or_sync_known'):ck(prov[k] is False,'B32 no start or sync:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B32 no runtime:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B32 independent repair')
    for err in date_identity_errors(prov,v.read(v.AUDIT/PART_DOCS[4])):ck(False,err)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==5,'B32 five paths')
    for r in selected:ck(r['path'] in original and r['review_state']=='bounded-editor-events-and-context-not-whole-file-or-runtime' and bool(r['focus']),'B32 bounded scope');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    tables={};known={r['id'] for r in current}|{f'H7B32-{n:02d}' for n in range(1,7)}
    for stem,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+stem+'-07B32.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(type(x) is str and x.strip() for x in r.values()),'B32 completeCSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B32 no runtime claim:'+r['id'])
    fe,ivs,tests=[tables[x] for x in ('FE7B32-','INV7B32-','P7B32T-')]
    for err in current_link_errors(fe,ivs,tests)+ledger_errors(tables['EO7B32-'],tables['DG7B32-'],fe):ck(False,err)
    v.proposed_tests(tests,'7B32');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,ivs,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+ivs,tids,'acceptance_ids');v.related(tables['EO7B32-']+tables['DG7B32-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(ivs,'invariants'),(tests,'plans')):v.covered(new,pool,'B32 '+label)
    for r in tables['RC7B32-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];uniq=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ev=source_evidence_union(fs) if r['id'] not in ('RC7B32-05','RC7B32-06') else DOCUMENTARY
        ck(r['evidence']==ev and r['finding_ids']==uniq('finding_ids') and r['acceptance_ids']==uniq('acceptance_ids'),'B32 reconciliation exact source/link union');v.related([r],fids,'feature_ids')
    for err in residual_errors(tables['RS7B32-'],rows('evidence/residual-disposition-07B31.csv'))+split_errors(tables['SP7B32-'],rows('evidence/split-register-07B31.csv'))+remaining_work_errors(tables['RW7B32-']):ck(False,err)
    hids={r['id'] for r in tables['H7B32-']};sids={r['id'] for r in tables['SP7B32-']};v.related(tables['RS7B32-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B32-'],hids,'handoff_ids')
    for stem in ('H7B32-','Q7B32-'):
        prior=rows('evidence/'+('handoffs' if stem=='H7B32-' else 'questions')+'-07B31.csv')
        for old,r in zip(prior,tables[stem]):ck(r['required_redacted_input'].startswith(old['required_redacted_input']),'B32 no lost H/Q input prefix')
    for r in tables['H7B32-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B32 unresolved H')
    for r in tables['Q7B32-']:ck(r['status']=='unanswered-no-secrets-requested','B32 unanswered Q')
    for n,r in enumerate(tables['BK7B32-'],1):ck(r['prior_backlog_id']==f'BK7B31-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B32 backlog ancestry')
    ck([r['status'] for r in tables['BK7B32-'][2:6]]==['not-started']*4,'B32 C unstarted')
    ad=tables['AD7B32-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids');ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS and not any(r['decision']=='extended-existing-root-not-new' for r in ad),'B32 one162 no extension')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B32 honest dedup depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,32)]
    before={r['path'] for name in prior_names for r in rows(name)};paths=set(scope);rem=original.keys()-(before|paths)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(bk==dict(selected_paths=5,prior_union=427,overlap=5,new=0,union=427,complement=400,complement_kinds={'source':335,'generated-artifact':61,'project-or-resource':4}),'B32 path accounting not progress')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B32.json'))
    ck(decision['bookkeeping']==bk and decision['selected_upstream_split']=='SP7B31-01' and decision['entry']==ENTRY and decision['historical_metadata_screen_count']==333 and decision['parent_path_matched_metadata_rows']==27 and decision['all_historical_bodies_reviewed'] is False,'B32 bounded authority/dedup')
    ck(decision['selected_contract_slices']==22 and decision['exploratory_context_slices']==9 and decision['whole_local_files']==0 and decision['new_root_ids']==NEW_IDS and decision['existing_root_extensions']==[],'B32 selected slices not whole capability')
    for k in ('selected_capability','entry_point','source_contract','output_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):ck(type(decision.get(k)) is str and len(decision[k])>20,'B32 scoped responsibility:'+k)
    ck(type(decision.get('exclusions')) is list and len(decision['exclusions'])==4,'B32 explicit exclusions')
    for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k] is False,'B32 no permission:'+k)
    wp='evidence/editor-close-witnesses-07B32.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B32 immutable witness');w,match=v.recompute(wp,'tools/check_editor_close_witnesses.py')
    for err in witness_metadata_errors(w):ck(False,err)
    ck(w['errors']==[],'B32 inert witness pass')
    for key,prefix,flag in (('illustrations','ALG7B32-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B32-','documented_text_observation_matches')):
        v.sequential(w[key],prefix,20);v.related(w[key],known)
        for r in w[key]:ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B32 witness safety');validate_source(v,r,scope)
    for key,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('exploratory_source_reads_not_capability_certification',EXPLORATORY_SLICES)):
        reads=w[key];ck(tuple((r['path'],r['start'],r['end']) for r in reads)==declared,'B32 exact declared read slices')
        for r in reads:ck(r['whole_local_file_selected'] is False and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True and v.sha(v.ROOT/r['path'])==r['sha256'],'B32 bounded source identity');v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B32 read',phase=7)
    old_texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for err in group_row_errors(old_texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,err)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            u=urlsplit(m[1]);target=(doc.parent/unquote(u.path)).resolve()
            if u.scheme or m[1].startswith('#'):continue
            if target==(v.AUDIT/'evidence/checks-07B32.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B32 broken local link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{z}' for a,z in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B32.md','PHASE-07-REMAINING-07B32.md','7B33','غير مأذونة','0bbadbe','10ba215')),'B32 current shared entrypoint:'+name)
    hp='evidence/historical-mode-verification-07B32.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B32 actual37 exists')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B32 actual37 identity');history=v.json.loads(v.read(v.AUDIT/hp))
        for err in historical_record_errors(history):ck(False,err)
        ck((history['checkout_head'],history['source_head'],history['branch'])==(ENTRY,v.HEAD,v.BRANCH),'B32 historical capture entry/source')
        sources={p.relative_to(v.AUDIT).as_posix():p.read_bytes() for p in sorted((v.AUDIT/'tools').glob('*.py'))}
        for err in capture_source_errors(history,sources):ck(False,err)
        report['phase_7B32_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=37,capture_time_tool_count=119,historical_B31_source_assertion_inputs_not_execution_inventory=115,all_original48_B31_and1034_prior_cases_preserved=True,null_aggregates_unreported_not_zero=True,single_later_pin_only_inverted_in_memory=True,not_final_or_postpush_wholesale_replay=True)
    tools=['check_editor_close_witnesses.py','validate_editor_close_part.py','run_historical_navigation_load_tests_07B32.py','test_editor_close_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:ck(False,'B32 tool syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60);m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==52
    ck(passed,'B32 ALL52 documentary cases: '+(run.stderr[-12000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=52,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name) for name in ['validate_audit.py']+tools})
    execution_sources={p.relative_to(v.AUDIT).as_posix():v.sha(p) for p in sorted((v.AUDIT/'tools').glob('*.py'))};ck(len(execution_sources)==119,'B32 actual full119 current tools')
    report['validation']['current_execution_tool_inventory_sha256_not_original_application']=execution_sources
    report.update(registry_used='findings.csv',validation_scope='current-through7B32-334-bounded-R4p-editor-events-not7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,33))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B33-proposed-R4q-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=162,phase_7B32=1,total_open_not_remediated=334,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:5,'phase_7B32_prior_union':427,'phase_7B32_overlap_with_prior_union':5,'phase_7B32_new_paths':0,'unique_union_not_line_or_execution_coverage':427,'inventory_only_no_selected_scope':400})
    report['phase_7B31_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256=SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_evidence_artifacts_hash_checked=942,historical_check_record_overwritten=False,genuine_B31_final_stdout_sha256_unchanged=B31_CHECK_SHA,all333_dictionaries_ALLnext_phase_evidence_status_classification_exact=True,entire_raw334CRLF_prefix_exact=True,existing159_evidence_tail_and160_and161_unchanged=True,auxiliary_dispatcher_text_is_assertion_input_not_executed_code=DISPATCHER_SNAPSHOT)
    report['phase_7B32_editor_event_trace_limits']=dict(event_boundaries=8,dirty_guard_boundaries=8,selected_source_paths=5,contract_slices=22,context_slices_not_certified=9,whole_files=0,new_union_paths=0,new_root_ids=NEW_IDS,existing_root_extensions=[],features=16,invariants_not_executed=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_splits=3,authored_sale_Closing_attachments=2,authored_purchase_Closing_attachments_in_selected_constructor_and_XAML=1,F5_Handled_negative_control=True,F6_counts_validation_requests_not_successful_saves=True,Closing_Cancel_does_not_mask_next_supplied_delegate=True,header_dirty_contract_unresolved_not_absence=True,all_callers_or_historical_bodies_reviewed=False,repair_start_sync_unknown=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B32_illustrations_not_ERP_tests=20,phase_7B32_lexical_checks_not_ERP_tests=20,phase_7B32_contract_reads_not_whole_files=22,phase_7B32_context_reads_not_capability_certification=9,phase_7B32_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=__doc__+' Actual37 summarizes real process stdout identities at capture,not full streams or final/postpin/postpush wholesale replay. Historical B31 assertions115 distinct from actual119 execution tools and reported legacy hash subset. All32 B32 and B31/B30/B29/B28 plans and36 B27 remain not-executed. No application builds,C#/VB/.NET,WPF,SQL,SDK/provider,printers/scanners,business data,secrets,repair,measurement or operational acceptance. Potential014/132/145,020/021 and financial/ACL/stock/save/production barriers remain. B10 additive10 vs120/equality1=10/G138 preserved. next_phase8 planning only.'
