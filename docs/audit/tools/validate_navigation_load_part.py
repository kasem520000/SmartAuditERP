#!/usr/bin/env python3
"""Read-only B31/R4o toolbar/reader-outcome audit, never ERP acceptance.

One161: known Empty alone replaces a clean current editor BEFORE resolving
its target. Outer-reader failure shares null/fallback; not extra per editor,
command/null/exception/flag.159 missing abandon guard,160 unaccepted-import
conversion and046 failed report/search publication retained, not rewritten.
All332 dictionaries/raw333CRLF full prefix exact;900/905 entry artifacts,
G01..240 and827 originals protected. All986 previous documentary cases retained.
ALL52 original B30 cases use OWN332/indexes/presetB30 with module-local A/Path
and111 exact source-assertion inputs/dispatcher TEXT, never old dispatcher code,
global pathlib/subprocess mutation, disk overlay, skips or rebaseline. Actual
B31 parser/routing and115 tools checked independently.14 bounded slices/5 prior
paths/0whole files; whole290-line reader method not full hydration/SDK/schema.
32 plans not executed;7B/7partial,R4p/B32proposed,7Cunstarted,8unauthorized;
repair start/sync unknown. Date16 authoritative,raw clock observations separate.
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
from validate_import_cancel_part import historical_record_errors as historical35_errors
from check_navigation_load_witnesses import SOURCE_SLICES
ENTRY='038a18b74acb92c35a6172d4619fee5712424489'
SNAPSHOT='evidence/findings-through-07B30.csv';SNAPSHOT_SHA='f9210ca561d60125f974609ef9d7ac1214a630b21931ad5ab4ae3b51cc6f2986'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B30.json';SHARED_SHA='0eeed5a55c0b1867c6656e708c0c72eb6e85657e5b934df3618869c434d7bc05'
PROVENANCE_SHA='64faf18bed41938412a70f40293adf5d4ca4eed01db6e49d12e415262f29a760'
DISPATCHER_SNAPSHOT='evidence/dispatcher-through-07B30.py.txt';DISPATCHER_SHA='d128c772ee052a8c73d72f751bc1fc258a395eb0868072f790da75d9acf220c5'
B30_CHECK_SHA='5610ade5b349f3f852f6a093819beda3d8bd09662d59ed5d88ac6d6e106928d4'
WITNESS_SHA='fe6c611c5870c1caa34ad589753f8509ff23f9e97d8ff46ed0eda2dc4488ddcd'
HISTORICAL_RUN_SHA = '0e7675f906028a0da48e4c5d806474fb08f292c886de77df274576b24e8ab8e1'  # Pin only after exclusive actual36 capture.
DOCUMENTARY='none-documentary-metadata';SCOPE_FILE='review-scope-07B31.csv';NEW_IDS=['P7-161'];EXTENDED_IDS=[]
PART_DOCS=('PHASE-07B31.md','NAVIGATION-LOAD-CONTRACTS-07B31.md','VALIDATION-07B31.md','PHASE-07-REMAINING-07B31.md','DATE-IDENTITY-NOTE-07B31.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS=(('navigation-load-lineage','NL7B31-',8),('reader-outcome-lineage','LO7B31-',8),('feature-implementation-matrix','FE7B31-',16),('report-invariants','INV7B31-',16),('acceptance-tests','P7B31T-',32),('report-reconciliation','RC7B31-',6),('root-adjudication','AD7B31-',8),('residual-disposition','RS7B31-',14),('split-register','SP7B31-',3),('handoffs','H7B31-',6),('questions','Q7B31-',6),('remaining-workplan','RW7B31-',10),('continuation-backlog','BK7B31-',10))
SENTINELS={f'{p}{n:02d}' for p,nums in (('FE7B31-',(15,16)),('INV7B31-',(15,16)),('P7B31T-',range(29,33)),('RC7B31-',(5,6)),('AD7B31-',(7,8)),('RS7B31-',range(1,15)),('H7B31-',range(1,7)),('Q7B31-',range(1,7))) for n in nums}
NAV_BOUNDARIES=['toolbar-wiring','abandon-guard','pre-read-CLR','reader-boundary','nonnull-publish','null-fallback','reset-number-boundary','outcome-and-identity-contract']
NAV_OBSERVATIONS=['eight-toolbar-entrypoints-only','No-stops-before-first-write','original-reference-replaced-before-target-read','void-ref-null-collapses-empty-and-outer-failed','nonnull-attempts-binding-not-full-health','empty-or-outer-failed-reaches-new-and-second-CLR','number-before-ISNew-purchase-swallow-sale-escape','resolve-then-validate-then-publish-proposed-not-implemented']
OUTCOME_BOUNDARIES=['empty-purchase','empty-sale','outer-failed-before-header','outer-failed-after-header','found-nonnull','row-caught-nonnull','first-reset-number-failure','fallback-number-failure']
OUTCOME_OBSERVATIONS=['two-CLR-cycles-after-nonnull-original-and-normal-resets','same161-second-editor-not-another-root','outer-catch-null-not-provider-failure-observed','partial-working-header-can-be-discarded-not-original-restored','one-preclear-then-binding-attempted-not-completeness-proof','inner-row-catch-may-retain-nonnull-not-all-errors-null','purchase-may-continue-sale-stops-before-reader-under-supplied-failure','no-explicit-new-flags-after-supplied-number-failure-no-default-claim']
DEDUP_DEPTH='all332-title-metadata-and79-path-matched-rows-plus-selected-reader-and-nearest-parent-bodies-and-protected-root-reports-not-all-historical-bodies'


@contextmanager
def historical_b30_inputs(v,frozen332,texts,raw,sources,dispatcher):
    """Exact historical ASSERTION data, only through this module's local view.

    canonical dispatcher path retains canonical resolve; its read returns TEXT.
    The dedicated child injects this Path TYPE into its test module only so
    protected Path(v.__file__) source assertions see their exact historical
    source input. No old function/code objects or shared pathlib are replaced.
    """
    if type(frozen332) is not list or len(frozen332)!=332 or len({r.get('id') for r in frozen332})!=332:raise ValueError('Exactly332 distinct OWN B30 rows')
    if type(texts) is not dict or set(texts)!=set(SHARED_DOCS) or any(type(x) is not str for x in texts.values()):raise ValueError('Three OWN shared index strings')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=333 or not raw.endswith(b'\r\n') or any(x in raw.replace(b'\r\n',b'') for x in (b'\r',b'\n')):raise ValueError('OWN332 raw333CRLF noBOM required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))
    except (UnicodeError,csv.Error) as exc:raise ValueError('Malformed OWN raw') from exc
    if parsed!=frozen332:raise ValueError('OWN rows/raw mismatch')
    if (type(sources) is not dict or len(sources)!=111 or any(type(n) is not str or re.fullmatch(r'tools/[A-Za-z0-9_]+\.py',n) is None or type(h) is not str or re.fullmatch('[0-9a-f]{64}',h) is None for n,h in sources.items()) or type(dispatcher) is not bytes or not dispatcher or sources.get('tools/validate_audit.py')!=hashlib.sha256(dispatcher).hexdigest()):raise ValueError('Exactly111 historical source identities and matching TEXT')
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
        with historical_b1_inputs(v,frozen332,texts):yield
    finally:v.AUDIT=original


class HistoricalB30Subprocess:
    def __init__(self,backend,python,tools):
        self.backend=backend;self.expected=[python,'-B',str(tools/'test_import_cancel_audit_validator.py')]
        self.actual=[python,'-B',str(tools/'run_historical_import_cancel_tests_07B31.py'),'--through-part','B30']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB30ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target);object.__setattr__(self,'_subprocess',HistoricalB30Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess' else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b30_validation(v,report,prior,prov,frozen332):
    ck=v.check
    for name,h in ((SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),(DISPATCHER_SNAPSHOT,DISPATCHER_SHA),('evidence/provenance-07B31.json',PROVENANCE_SHA),('evidence/checks-07B30.json',B30_CHECK_SHA)):ck(v.sha(v.AUDIT/name)==h,'B31 immutable entry:'+name)
    ck(prov['historical_artifact_count']==len(prov['historical_artifact_sha256'])==900 and len(frozen332)==332,'B31 protected900/OWN332')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B31 protected867→900 continuity')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B31 pushed entry038a')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B31 own input identities')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B30.json'));vv=old['validation'];s=vv['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='3589d23a26438300d631790487eafe3aaddef7fb' and old['findings']['total_open_not_remediated']==332 and old['original_project_hashes_matching']==827 and vv['errors']==[] and vv['current_output_record_pending_first_write_not_placeholder'] is False,'B31 genuine official B30 captured3589 not delivery038a')
    ck(len(s)==31 and sum(x['tests_reported'] for x in s.values())==986 and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B31 genuine986/31/867')
    r=prov['entry_actual_subprocess_receipt'];ck(r['checkout_head']==ENTRY and r['exit_code']==0 and r['errors']==[] and r['findings']==332 and r['originals']==827 and r['cases']==986 and r['suites']==31 and r['all905_unchanged'] is True and r['stderr_bytes']==0,'B31 actual independent entry986/31')
    src=prov['historical_checker_sources_at_entry'];meta=prov['dispatcher_source_at_entry']
    ck(len(src)==111 and src['tools/validate_audit.py']==DISPATCHER_SHA and meta['path']==DISPATCHER_SNAPSHOT and meta['bytes']==101540 and meta['sha256']==DISPATCHER_SHA,'B31 historical111 assertion inputs not115 execution tools')
    view=HistoricalB30ValidatorView(v);texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b30_inputs(view,frozen332,texts,(v.AUDIT/SNAPSHOT).read_bytes(),src,(v.AUDIT/DISPATCHER_SNAPSHOT).read_bytes()):yield view
    rec=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_import_cancel_audit_validator.py']
    rec.update(historical_parser_cutoff='B30-not-current-B31-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_import_cancel_tests_07B31.py',actual_subprocess_argv=view.subprocess.actual,no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=111,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B30-332-not-current-state',phase_7B30_historical_input_mode='OWN332-raw333CRLF-indexes-presetB30-ALL52-child-module-local-A-Path-and111-source-assertion-inputs',phase_7B30_adapter_context=dict(entry_provenance='evidence/provenance-07B31.json',adapter_protected_artifacts_checked=900,old_dispatcher_TEXT_not_executed=True,module_local_Path_type_for_source_reads_not_process_global=True,archived_stdout_not_rewritten_after_push=True,current_registry_and_indexes_not_inputs=True))


def registry_preservation_errors(previous,current,raw,frozen,extensions):
    errors=[]
    if type(extensions) is not list or extensions!=[]:errors.append('B31 no historical extensions allowed')
    if len(previous)!=332 or len(current)!=333:return errors+['B31 OWN332 plus one161 required']
    if current[:332]!=previous:errors.append('B31 ALL332 dictionaries including159tail160 and ALLnext_phase exact')
    if [r.get('id') for r in current[332:]]!=NEW_IDS or len({r.get('id') for r in current})!=333:errors.append('B31 only one appended161')
    if type(raw) is not bytes or type(frozen) is not bytes:return errors+['B31 exact bytes required']
    for data,n in ((frozen,333),(raw,334)):
        if data.startswith(b'\xef\xbb\xbf') or data.count(b'\r\n')!=n or not data.endswith(b'\r\n') or any(x in data.replace(b'\r\n',b'') for x in (b'\r',b'\n')):errors.append('B31 exact CRLF/noBOM')
    if not raw.startswith(frozen):errors.append('B31 entire old raw333 prefix exact')
    try:
        if list(csv.DictReader(io.StringIO(raw.decode(),newline='')))!=current or list(csv.DictReader(io.StringIO(frozen.decode(),newline='')))!=previous:errors.append('B31 rows/raw mismatch')
    except (UnicodeError,csv.Error):errors.append('B31 malformed raw registry')
    return errors


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=240 or rows(current)[:240]!=rows(previous):return ['B31 G01..240 exact']
    return [] if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)==[f'G-{n:02d}' for n in range(1,245)] else ['B31 only G241..244 ordered']


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B31 all14 residuals']
    errors=[]
    for old,new in zip(upstream,current):
        if (new.get('upstream_residual_id')!=old.get('id') or new.get('upstream_artifact')!='evidence/residual-disposition-07B30.csv' or new.get('upstream_row_sha256')!=row_sha(old) or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):errors.append('B31 residual ancestry/hash/contracts')
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B31 old input full prefix')
        mapped={x.replace('7B30-','7B31-') for x in old.get('current_handoff_or_split_ids','').split(';') if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B31 all mapped routes')
        if new.get('disposition')!=old.get('disposition') or new.get('disposition') not in {'external-handoff','split-explicitly','assessment-source-bound'} or new.get('runtime_status')!='not-executed':errors.append('B31 retained dispositions not approvals')
        for k in ('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion'):
            if type(new.get(k)) is not str or len(new[k])<20:errors.append('B31 substantive residual:'+k)
    return errors


def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return ['B31 all3 splits']
    errors=[]
    for old,new in zip(upstream,current):
        if new.get('upstream_split_id')!=old.get('id') or new.get('upstream_artifact')!='evidence/split-register-07B30.csv' or new.get('upstream_row_sha256')!=row_sha(old):errors.append('B31 split ancestry/hash')
        if not new.get('required_input','').startswith(old.get('required_input','')):errors.append('B31 all old split input')
        for k in ('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if type(new.get(k)) is not str or not new[k].strip():errors.append('B31 split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started' or new.get('runtime_status')!='not-executed':errors.append('B31 future splits not completion/session')
    return errors


def remaining_work_errors(data):
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4o-navigation-load-delivered-residuals-open']+['planned-not-started']*6
    if len(data)!=10:return ['B31 four B six C']
    return ['B31 remaining work or permission'] if any(r.get('part_family')!=('7B' if i<4 else '7C') or r.get('status')!=expected[i] or r.get('runtime_status')!='not-executed' or r.get('counts_are_sessions_or_completion_percent')!='false' for i,r in enumerate(data)) else []


def current_link_errors(fe,inv,plans):
    if (len(fe),len(inv),len(plans))!=(16,16,32):return ['B31 FE16/INV16/T32']
    errors=[]
    for n,(f,i) in enumerate(zip(fe,inv),1):
        tids=';'.join(f'P7B31T-{k:02d}' for k in (2*n-1,2*n));paired=plans[2*n-2:2*n]
        if f.get('id')!=f'FE7B31-{n:02d}' or i.get('id')!=f'INV7B31-{n:02d}' or i.get('feature_ids')!=f.get('id') or f.get('acceptance_ids')!=tids or i.get('acceptance_ids')!=tids:errors.append('B31 exact bidirectional feature/invariant/plan links')
        if n<=4 and (f.get('finding_ids')!='P7-161' or i.get('finding_ids')!='P7-161'):errors.append('B31 root161 capabilities1..4')
        for t in paired:
            if t.get('feature_ids')!=f.get('id') or t.get('invariant_ids')!=i.get('id') or t.get('finding_ids')!=f.get('finding_ids') or t.get('status')!='not-executed':errors.append('B31 linked plan nonexecution')
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if type(f.get(k)) is not str or len(f[k])<20:errors.append('B31 capability responsibility:'+k)
    if len({r.get('required_invariant') for r in inv})!=16 or len({r.get('acceptance_criterion') for r in plans})!=32:errors.append('B31 distinct substantive invariants/criteria')
    return errors


def ledger_errors(navigation,outcomes):
    errors=[]
    for pool,bounds,obs in ((navigation,NAV_BOUNDARIES,NAV_OBSERVATIONS),(outcomes,OUTCOME_BOUNDARIES,OUTCOME_OBSERVATIONS)):
        if len(pool)!=8 or [r.get('boundary') for r in pool]!=bounds or [r.get('observation') for r in pool]!=obs:errors.append('B31 ordered NL8/LO8')
        for r in pool:
            for k in ('source_to_output','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if type(r.get(k)) is not str or not r[k].strip():errors.append('B31 lineage responsibility:'+k)
            if r.get('runtime_status')!='not-executed':errors.append('B31 lineage not runtime')
    return errors


def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_SDK_executed','provider_failure_observed','SDK_defaults_or_row_hydration_executed','stable_post_event_state_claimed','database_commit_or_saved_loss_claimed','original_reference_release_or_GC_claimed','application_remediation_performed','phase7C_started','phase8_authorized_or_started','all332_historical_bodies_or_all_callers_reviewed'):
        if w.get(k) is not False:errors.append('B31 false-only:'+k)
    for k in ('reset_and_reader_outcomes_are_supplied','per_row_caught_exception_is_not_outer_null','guard_No_prevents_first_write'):
        if w.get(k) is not True:errors.append('B31 true-only:'+k)
    for k,n in (('illustration_count',20),('lexical_check_count',20),('selected_source_paths',5),('source_read_slice_count',14),('whole_local_files_selected',0),('whole_reader_method_selected_lines',290),('erp_runtime_tests_executed',0),('sql_or_external_service_tests_executed',0),('scanner_or_printer_tests_executed',0)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B31 exact count:'+k)
    if w.get('new_root_ids')!=NEW_IDS or w.get('extended_existing_root_ids')!=[] or w.get('entry_checkout')!=ENTRY or w.get('audit_reference_date_utc')!='2026-11-16':errors.append('B31 root/date/entry')
    erratum=w.get('retained_additive_B10_arithmetic_erratum',{})
    if erratum!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True) or any(type(erratum.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or erratum.get('protected_G138_not_rewritten') is not True:errors.append('B31 B10 additive erratum')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=36 or len(modes)!=36:return ['B31 exactly36 actual OWN modes']
    errors=historical35_errors(dict(historical_mode_count=35,historical_modes=modes[:35],errors=h.get('errors')))
    last=modes[-1]
    for k,val in dict(mode='B30',findings_total=332,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=986,audit_checker_self_test_suite_count=31,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0).items():
        if last.get(k)!=val or type(last.get(k)) is not type(val):errors.append('B31 OWN332/986/31:'+k)
    for k,val in dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B30-not-current-B31-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_import_cancel_tests_07B31.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=111,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True).items():
        value=(last.get('historical_B30_child') or {}).get(k)
        if value!=val or type(value) is not type(val):errors.append('B31 ALL52 B30 child:'+k)
    if type(last.get('stdout_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B31 stdout SHA required')
    return errors


def capture_source_errors(history,sources):
    expected=history.get('checker_sources_at_capture',{});errors=[]
    if set(expected)!=set(sources) or len(expected)!=115:return ['B31 capture tool set115']
    for name,raw in sources.items():
        if name=='tools/validate_navigation_load_part.py':
            final="HISTORICAL_RUN_SHA = '"+str(HISTORICAL_RUN_SHA)+"'  # Pin only after exclusive actual36 capture."
            initial='HISTORICAL_RUN_SHA = None  # Pin only after exclusive actual36 capture.'
            text=raw.decode()
            if HISTORICAL_RUN_SHA is None or text.count(final)!=1:errors.append('B31 exact final pin required');continue
            raw=text.replace(final,initial).encode()
        if hashlib.sha256(raw).hexdigest()!=expected[name]:errors.append('B31 tool changed beyond single inverse pin:'+name)
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or type(prov.get('environment_clock_observed_utc')) is not str:errors.append('B31 date reference/raw fields')
    for token in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,'3589d23a26438300d631790487eafe3aaddef7fb',B30_CHECK_SHA,DISPATCHER_SHA,WITNESS_SHA,'273892','900','905','332','111','115'):
        if token not in note:errors.append('B31 additive identity:'+token)
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id'] in SENTINELS,'B31 undeclared documentary sentinel:'+row['id']);return
    v.check(row['id'] not in SENTINELS,'B31 fabricated source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
    try:expanded=expanded_source_evidence(row['evidence'])
    except ValueError as exc:v.check(False,'B31 invalid source:'+str(exc));return
    v.scoped_evidence(expanded,scope,row['id']+' boundedB31',phase=7)


def extend_navigation_load(v,report,prov,frozen332):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[332:];ext=rows('evidence/historical-extensions-07B31.csv')
    for err in registry_preservation_errors(frozen332,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes(),ext):ck(False,err)
    v.distributions(new,dict(Medium=1),dict(confirmed=1),'B31 only');ck(len(new)==1,'B31 exactly161')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B31 state not authorization')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B31 exact registry/report title')
    lookup={r['id']:r for r in current}
    for root in ('P4-014','P7-132','P7-145'):ck(lookup[root]['certainty']=='potential','B31 retained potential:'+root)
    for root in ('P7-046','P7-158','P7-159','P7-160','P4-020','P4-021'):ck(lookup[root]==next(r for r in frozen332 if r['id']==root),'B31 prior root exact:'+root)
    for k in ('phase7C_started','phase8_authorized_or_started','application_remediation_performed','repair_start_or_sync_known'):ck(prov[k] is False,'B31 no start or sync:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B31 no runtime:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B31 independent repair')
    for err in date_identity_errors(prov,v.read(v.AUDIT/PART_DOCS[4])):ck(False,err)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==5,'B31 five paths')
    for r in selected:ck(r['path'] in original and r['review_state']=='bounded-static-toolbar-reader-reset-slices-not-whole-file-or-runtime' and bool(r['focus']),'B31 bounded scope');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    tables={};known={r['id'] for r in current}|{f'H7B31-{n:02d}' for n in range(1,7)}
    for stem,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+stem+'-07B31.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(type(x) is str and x.strip() for x in r.values()),'B31 completeCSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B31 no runtime claim:'+r['id'])
    fe,ivs,tests=[tables[x] for x in ('FE7B31-','INV7B31-','P7B31T-')]
    for err in current_link_errors(fe,ivs,tests)+ledger_errors(tables['NL7B31-'],tables['LO7B31-']):ck(False,err)
    v.proposed_tests(tests,'7B31');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,ivs,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+ivs,tids,'acceptance_ids');v.related(tables['NL7B31-']+tables['LO7B31-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(ivs,'invariants'),(tests,'plans')):v.covered(new,pool,'B31 '+label)
    for r in tables['RC7B31-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];uniq=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ev=source_evidence_union(fs) if r['id'] not in ('RC7B31-05','RC7B31-06') else DOCUMENTARY
        ck(r['evidence']==ev and r['finding_ids']==uniq('finding_ids') and r['acceptance_ids']==uniq('acceptance_ids'),'B31 reconciliation exact source/link union');v.related([r],fids,'feature_ids')
    for err in residual_errors(tables['RS7B31-'],rows('evidence/residual-disposition-07B30.csv'))+split_errors(tables['SP7B31-'],rows('evidence/split-register-07B30.csv'))+remaining_work_errors(tables['RW7B31-']):ck(False,err)
    hids={r['id'] for r in tables['H7B31-']};sids={r['id'] for r in tables['SP7B31-']};v.related(tables['RS7B31-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B31-'],hids,'handoff_ids')
    for stem,key in (('H7B31-','required_redacted_input'),('Q7B31-','required_redacted_input')):
        prior=rows('evidence/'+('handoffs' if stem=='H7B31-' else 'questions')+'-07B30.csv')
        for old,r in zip(prior,tables[stem]):ck(r[key].startswith(old[key]),'B31 no lost H/Q input prefix')
    for r in tables['H7B31-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B31 unresolved H')
    for r in tables['Q7B31-']:ck(r['status']=='unanswered-no-secrets-requested','B31 unanswered Q')
    for n,r in enumerate(tables['BK7B31-'],1):ck(r['prior_backlog_id']==f'BK7B30-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B31 backlog ancestry')
    ck([r['status'] for r in tables['BK7B31-'][2:6]]==['not-started']*4,'B31 C unstarted')
    ad=tables['AD7B31-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids');ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS and not any(r['decision']=='extended-existing-root-not-new' for r in ad),'B31 one161 no extension')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B31 honest dedup depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,31)]
    before={r['path'] for name in prior_names for r in rows(name)};paths=set(scope);rem=original.keys()-(before|paths)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(bk==dict(selected_paths=5,prior_union=427,overlap=5,new=0,union=427,complement=400,complement_kinds={'source':335,'generated-artifact':61,'project-or-resource':4}),'B31 path accounting not progress')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B31.json'))
    ck(decision['bookkeeping']==bk and decision['selected_upstream_split']=='SP7B30-01' and decision['entry']==ENTRY and decision['historical_metadata_screen_count']==332 and decision['path_matched_metadata_rows']==79 and decision['historical_body_review_claim'] is False and decision['historical_comparison_depth']==DEDUP_DEPTH,'B31 bounded authority/dedup')
    ck(decision['bounded_read_slice_count']==14 and decision['whole_local_files']==0 and decision['whole_reader_method_lines']==290 and decision['one_new_root']==NEW_IDS and decision['existing_root_extensions']==[],'B31 method not whole file')
    for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k] is False,'B31 no permission:'+k)
    wp='evidence/navigation-load-witnesses-07B31.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B31 immutable witness');w,match=v.recompute(wp,'tools/check_navigation_load_witnesses.py')
    for err in witness_metadata_errors(w):ck(False,err)
    ck(w['errors']==[],'B31 inert witness pass')
    for key,prefix,flag in (('illustrations','ALG7B31-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B31-','documented_text_observation_matches')):
        v.sequential(w[key],prefix,20);v.related(w[key],known)
        for r in w[key]:ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B31 witness safety');validate_source(v,r,scope)
    reads=w['bounded_source_reads_not_semantic_coverage'];ck(tuple((r['path'],r['start'],r['end']) for r in reads)==SOURCE_SLICES,'B31 exact14 reads')
    for r in reads:ck(r['whole_local_file_selected'] is False and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True and v.sha(v.ROOT/r['path'])==r['sha256'],'B31 bounded source identity');v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B31 read',phase=7)
    old_texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for err in group_row_errors(old_texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,err)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            u=urlsplit(m[1]);target=(doc.parent/unquote(u.path)).resolve()
            if u.scheme or m[1].startswith('#'):continue
            if target==(v.AUDIT/'evidence/checks-07B31.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B31 broken local link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{z}' for a,z in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B31.md','PHASE-07-REMAINING-07B31.md','7B32','غير مأذونة','038a18b','10ba215')),'B31 current shared entrypoint:'+name)
    hp='evidence/historical-mode-verification-07B31.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B31 actual36 exists')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B31 actual36 identity');history=v.json.loads(v.read(v.AUDIT/hp))
        for err in historical_record_errors(history):ck(False,err)
        ck((history['checkout_head'],history['source_head'],history['branch'])==(ENTRY,v.HEAD,v.BRANCH),'B31 historical capture entry/source')
        sources={p.relative_to(v.AUDIT).as_posix():p.read_bytes() for p in sorted((v.AUDIT/'tools').glob('*.py'))}
        for err in capture_source_errors(history,sources):ck(False,err)
        report['phase_7B31_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=36,capture_time_tool_count=115,historical_B30_source_assertion_inputs_not_execution_inventory=111,all_original52_B30_and986_prior_cases_preserved=True,null_aggregates_unreported_not_zero=True,single_later_pin_only_inverted_in_memory=True,not_final_or_postpush_wholesale_replay=True)
    tools=['check_navigation_load_witnesses.py','validate_navigation_load_part.py','run_historical_import_cancel_tests_07B31.py','test_navigation_load_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:ck(False,'B31 tool syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60);m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==48
    ck(passed,'B31 ALL48 documentary cases: '+(run.stderr[-12000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=48,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name) for name in ['validate_audit.py']+tools})
    report.update(registry_used='findings.csv',validation_scope='current-through7B31-333-bounded-R4o-navigation-load-not7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,32))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B32-proposed-R4p-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=161,phase_7B31=1,total_open_not_remediated=333,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:5,'phase_7B31_prior_union':427,'phase_7B31_overlap_with_prior_union':5,'phase_7B31_new_paths':0,'unique_union_not_line_or_execution_coverage':427,'inventory_only_no_selected_scope':400})
    report['phase_7B30_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256=SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_evidence_artifacts_hash_checked=900,historical_check_record_overwritten=False,genuine_B30_stdout_sha256_unchanged=B30_CHECK_SHA,all332_dictionaries_ALLnext_phase_evidence_status_classification_exact=True,entire_raw333CRLF_prefix_exact=True,existing159_extension_and160_unchanged=True,auxiliary_dispatcher_text_is_assertion_input_not_executed_code=DISPATCHER_SNAPSHOT)
    report['phase_7B31_navigation_load_trace_limits']=dict(navigation_boundaries=8,reader_outcome_boundaries=8,selected_source_paths=5,bounded_reads=14,whole_files=0,whole_reader_method_lines=290,new_union_paths=0,new_root_ids=NEW_IDS,existing_root_extensions=[],features=16,invariants_not_executed=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_splits=3,known_empty_clean_editor_alone_suffices_not_only_failure=True,guard_No_prevents_first_write=True,outer_catch_null_not_all_inner_errors=True,normal_reset_setters_collections_and_number_outcomes_supplied=True,provider_failure_full_hydration_SDK_defaults_stable_events_saved_loss_GC_not_observed=True,all_callers_or_historical_bodies_reviewed=False,repair_start_sync_unknown=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B31_illustrations_not_ERP_tests=20,phase_7B31_lexical_checks_not_ERP_tests=20,phase_7B31_bounded_reads_not_whole_files=14,phase_7B31_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=__doc__+' Actual36 archives summarize real process stdout identities at capture time,not full streams/final postpin/postpush wholesale replay. Current B31 checker source hashes recorded separately. All32 B31 and B30/B29/B28 plans remain not-executed. No application builds,C#/VB/.NET,WPF,SQL,SDK/provider,printers/scanners,business data,secrets,repair,measurement or operational acceptance. Potential014/132/145,020/021 and financial/ACL/stock/save/production barriers remain. B10 additive10 vs120/equality1=10/G138 preserved. next_phase8 planning only.'
