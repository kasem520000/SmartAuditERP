#!/usr/bin/env python3
"""Read-only B30/R4n import-outcome/assignment audit, NOT ERP acceptance.

One new160 for NORMAL NONACCEPTED return reaching conversion of the current
invoice; accepted import only extends159's existing dirty-guard omission.
Non-null editor/items, ordinary setters, number/failure and accepted Navigate
outcome supplied. No inherited chrome/Close bool?, SDK defaults, event schedule,
SQL success/reservation/new GlobalID, stable post-binding state or saved loss.
Protect867/872 entry; all331 old core/evidence prefixes; ONLY159.evidence gains
exact manifest tail; other330 dictionaries and first330 raw rows/header exact.
Original331/raw332CRLF frozen, current332/raw333CRLF. G01–236 and827 originals.
ALL48 B29 tests UNCHANGED in OWN331/raw332CRLF/indexes/presetB29 with suite-local
A. An auxiliary exact dispatcher TEXT and107 source identities are historical
ASSERTION INPUTS, not an old executable dispatcher or actual current tool set.
Current B30 separately checks live source/parser and111 actual tools. No skip,
process-global Path/shared subprocess patch, disk overlay, rebaseline/archive
rewrite. Fourteen reads total: two whole LOCAL child files and12 bounded
parent/support slices;7paths with6overlap+1new ->427/complement400 are
bookkeeping, not all477bodies/455FE/7B.
32 integrated plans NOT executed.7B/7partial,R4o/B31proposed,7Cunstarted,
8unauthorized; repair start/sync unknown. Date context16 and raw clock20 distinct.
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
from validate_financial_report_part import historical_b1_inputs,bidirectional_errors
from validate_contract_item_part import row_sha,expanded_source_evidence
from validate_property_dialog_part import source_evidence_union
from validate_dirty_navigation_part import historical_record_errors as historical34_errors
from check_import_cancel_witnesses import EV_EXTENSION
ENTRY = '3589d23a26438300d631790487eafe3aaddef7fb'
SNAPSHOT = 'evidence/findings-through-07B29.csv'
SNAPSHOT_SHA = '5b3260469f48200d708a737bee4edee8e89afe9082088eacadfffca7bced85bc'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B29.json'
SHARED_SHA = '7674b7d6da2c2d45df6b479ea14605bbfc95b2cf08648bafaa14dba1f3986aa2'
PROVENANCE_SHA = '77970f12239466b562925cf09dcba8559b32064e4f60b36c238d76a2939669fa'
B29_CHECK_SHA = '8a5f7125e27cdba430a1fabe8588b9f61405a1bc2638f49f9a22dc885bf5d522'
DISPATCHER_SNAPSHOT = 'evidence/dispatcher-through-07B29.py.txt'
DISPATCHER_SHA = '75484324013e469c4c6ea32aafa82a0f8440fbb04909b047215edf05e61557bd'
WITNESS_SHA = '9cf9b0467b9f7f14073b7e550a6e7ab75c145844b45d6c76090852f74e44f025'
HISTORICAL_RUN_SHA = '5c7a3741d12389a71f953b491ca8b94040a425562647420f6aa17c953be194d9'  # Pin only after exclusive actual35 capture.
SCOPE_FILE = 'review-scope-07B30.csv'
DOCUMENTARY = 'none-documentary-metadata'
NEW_IDS = ['P7-160']
EXTENDED_IDS = ['P7-159']
PART_DOCS = ('PHASE-07B30.md','IMPORT-CANCEL-CONTRACTS-07B30.md','VALIDATION-07B30.md',
 'PHASE-07-REMAINING-07B30.md','DATE-IDENTITY-NOTE-07B30.md')
SHARED_DOCS = ('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS = (('import-conversion-lineage','IC7B30-',8),('import-return-lineage','IR7B30-',8),
 ('feature-implementation-matrix','FE7B30-',16),('report-invariants','INV7B30-',16),
 ('acceptance-tests','P7B30T-',32),('report-reconciliation','RC7B30-',6),('root-adjudication','AD7B30-',8),
 ('residual-disposition','RS7B30-',14),('split-register','SP7B30-',3),('handoffs','H7B30-',6),
 ('questions','Q7B30-',6),('remaining-workplan','RW7B30-',10),('continuation-backlog','BK7B30-',10))
SENTINELS = {f'{p}{n:02d}' for p,ns in (('FE7B30-',range(15,17)),('INV7B30-',range(15,17)),
 ('P7B30T-',range(29,33)),('RC7B30-',(5,6)),('AD7B30-',(7,8)),('RS7B30-',range(1,15)),
 ('H7B30-',range(1,7)),('Q7B30-',range(1,7))) for n in ns}
CONVERSION_BOUNDARIES = ['own-import-wiring','fresh-child-outcome','guarded-Navigate','purchase-conversion',
 'sale-conversion','number-boundary','flags-and-binding','result-intent-boundary']
RETURN_BOUNDARIES = ['fresh-nonaccepted-return','notdone-with-identity','done-sentinel','accepted-return',
 'number-failure','dialog-nonreturn','value-idempotent-control','existing-guard-No']
DEDUP_DEPTH = 'all331-title-metadata-screen-plus78-path-matched-rows-and-selected-nearest-bodies-source-chains-not-all-historical-bodies'


@contextmanager
def historical_b29_inputs(v,frozen331,texts,raw,entry_sources,dispatcher_bytes):
    """OWN data/source-assertion view local to this v.AUDIT, never pathlib itself.

    Only the OLD source-assertion vector is107. New tools remain on disk and
    execute normally; the current validator tests/counts all111 independently.
    Logical tools/validate_audit.py read -> exact stored TEXT only in this view.
    The caller of the historical TEST CHILD additionally restores its module's
    __file__ pointer for old AST39, not the executing function/code object.
    """
    if len(frozen331)!=331 or len({r.get('id') for r in frozen331})!=331:
        raise ValueError('Exactly331 distinct historical B29 rows required')
    if set(texts)!=set(SHARED_DOCS) or any(type(t) is not str for t in texts.values()):
        raise ValueError('Exactly three frozen shared index strings')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM raw332CRLF bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))
    except (UnicodeError,csv.Error) as exc:raise ValueError('Malformed frozen registry') from exc
    if (parsed!=frozen331 or raw.count(b'\r\n')!=332 or not raw.endswith(b'\r\n')
            or any(t in raw.replace(b'\r\n',b'') for t in (b'\r',b'\n'))):
        raise ValueError('OWN331 rows/raw332CRLF mismatch')
    if (type(entry_sources) is not dict or len(entry_sources)!=107
            or any(not isinstance(n,str) or re.fullmatch(r'tools/[A-Za-z0-9_]+[.]py',n) is None
              or type(h) is not str or re.fullmatch(r'[0-9a-f]{64}',h) is None for n,h in entry_sources.items())
            or type(dispatcher_bytes) is not bytes or not dispatcher_bytes
            or entry_sources.get('tools/validate_audit.py')!=hashlib.sha256(dispatcher_bytes).hexdigest()):
        raise ValueError('Exactly107 historical source identities and matching dispatcher TEXT required')
    dispatcher_bytes.decode('utf8',errors='strict')
    original=v.AUDIT;target=(original/'findings.csv').resolve();dispatch=(original/'tools/validate_audit.py').resolve()
    tool_dir=(original/'tools').resolve();names=tuple(sorted(entry_sources))
    class HistoricalOwnPath(type(original)):
        def read_bytes(self):
            key=self.resolve()
            if key==target:return raw
            if key==dispatch:return dispatcher_bytes
            return super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            key=self.resolve()
            if key in (target,dispatch):
                return io.StringIO(self.read_bytes().decode(encoding or 'utf8',errors or 'strict'),newline=None).read()
            return super().read_text(encoding=encoding,errors=errors)
        def glob(self,pattern,*args,**kwargs):
            if self.resolve()==tool_dir and pattern=='*.py':
                for name in names:yield type(self)(original/name)
            else:yield from super().glob(pattern,*args,**kwargs)
    try:
        v.AUDIT=HistoricalOwnPath(original)
        with historical_b1_inputs(v,frozen331,texts):yield
    finally:v.AUDIT=original


class HistoricalB29Subprocess:
    """Exact argv redirection only, never monkeypatch shared subprocess.run."""
    def __init__(self,backend,python,tool_dir):
        self.backend=backend
        self.expected=[python,'-B',str(tool_dir/'test_dirty_navigation_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_dirty_navigation_tests_07B30.py'),'--through-part','B29']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB29ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB29Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess' else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b29_validation(v,report,prior,prov,frozen331):
    ck=v.check
    for n,h in ((SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),
      ('evidence/provenance-07B30.json',PROVENANCE_SHA),('evidence/checks-07B29.json',B29_CHECK_SHA),
      (DISPATCHER_SNAPSHOT,DISPATCHER_SHA)):
        ck(v.sha(v.AUDIT/n)==h,'B30 immutable entry:'+n)
    ck(prov['historical_artifact_count']==867 and len(prov['historical_artifact_sha256'])==867 and len(frozen331)==331,'B30 protected867/OWN331')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B30 protected829-to867 continuity')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
      and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B30 own entry identities')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B29.json'));s=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='dda1eafab4188b00a7d6c3e435e7391bd0e09cda' and old['findings']['total_open_not_remediated']==331
      and old['original_project_hashes_matching']==827 and old['validation']['errors']==[]
      and old['validation']['current_output_record_pending_first_write_not_placeholder'] is False,'B30 genuine officialB29 capturedda not delivery3589')
    ck(len(s)==30 and sum(x['tests_reported'] for x in s.values())==934 and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B30 genuine B29 934/30/829')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
      and prov['genuine_B29_check_sha256']==B29_CHECK_SHA and prov['genuine_B29_check_record_checkout']==old['checkout_head'],'B30 completed pushed B29 entry3589')
    ck(prov['phase7B29_entry_consistency']==dict(original_hashes_matching=827,findings=331,audit_file_count=872,documentary_cases=934,self_test_suites=30,errors=[],erp_runtime_tests_executed=0),'B30 entry consistency872/331')
    r=prov['entry_actual_subprocess_receipt']
    ck(r['entry']==ENTRY and r['findings']==331 and r['originals']==827 and r['cases']==934 and r['suites']==30 and r['errors']==[]
      and type(r['process_exit_code']) is int and r['process_exit_code']==0 and r['stderr_bytes']==0
      and r['stdout_sha256']=='92bea5846cf6fc66b177365528ba213918b09bb57e0139d44317879516438645'
      and r['all872_entry_artifacts_unchanged'] is True,'B30 actual independent entry receipt')
    sources=prov['historical_checker_sources_at_entry'];meta=prov['dispatcher_source_at_entry']
    ck(len(sources)==107 and meta['path']==DISPATCHER_SNAPSHOT and meta['sha256']==DISPATCHER_SHA
      and meta['bytes']==98822 and sources['tools/validate_audit.py']==DISPATCHER_SHA,'B30 exact historical dispatcher/assertion source vector')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB29ValidatorView(v)
    with historical_b29_inputs(view,frozen331,texts,(v.AUDIT/SNAPSHOT).read_bytes(),sources,(v.AUDIT/DISPATCHER_SNAPSHOT).read_bytes()):yield view
    rec=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_dirty_navigation_audit_validator.py']
    rec.update(historical_parser_cutoff='B29-not-current-B30-default',all_original_cases_executed_unmodified=True,
      dedicated_child_launcher='tools/run_historical_dirty_navigation_tests_07B30.py',actual_subprocess_argv=view.subprocess.actual,
      no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,
      historical_source_assertion_input_count=107,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,
      historical_source_assertions_not_current_execution_tool_inventory=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B29-331-not-current-state',
      phase_7B29_historical_input_mode='OWN331-raw332CRLF-indexes-presetB29-ALL48-child-suite-localA-and107-source-assertion-inputs',
      phase_7B29_adapter_context=dict(entry_provenance='evidence/provenance-07B30.json',adapter_protected_artifacts_checked=867,
      current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
      B29_parser_AST_assertions_are_historical_input_not_actual_B30_default=True,
      auxiliary_dispatcher_is_exact_readonly_text_not_executable_overlay=True,historical_source_assertion_input_count=107))


def extension_errors(extensions):
    if type(extensions) is not list or len(extensions)!=1:return ['B30 exactlyone159 extension']
    row=extensions[0]
    if (set(row)!={'finding_id','appended_evidence','reason'} or row.get('finding_id')!='P7-159'
      or row.get('appended_evidence')!=EV_EXTENSION or type(row.get('reason')) is not str or len(row['reason'])<30):
        return ['B30 only exact159 evidence tail and declared reason']
    return []


def registry_preservation_errors(previous,current,raw,frozen,extensions):
    errors=extension_errors(extensions)
    if len(previous)!=331 or len(current)!=332 or [x.get('id') for x in current[:331]]!=[x.get('id') for x in previous]:
        return errors+['B30 OWN331 plus exactlyone160 required']
    if previous[-1].get('id')!='P7-159' or [r.get('id') for r in current[331:]]!=NEW_IDS:errors.append('B30 only appended160 after old159')
    for old,new in zip(previous,current):
        if set(old)!=set(new):errors.append('B30 old schema changed')
        for k,val in old.items():
            expected=val+';'+EV_EXTENSION if old['id']=='P7-159' and k=='evidence' else val
            if new.get(k)!=expected:errors.append('B30 old field/ALLnext_phase/evidence:'+old['id']+'.'+k)
    if type(raw) is not bytes or type(frozen) is not bytes:return errors+['B30 exact bytes required']
    for data,n,label in ((frozen,332,'frozen331'),(raw,333,'current332')):
        if (data.startswith(b'\xef\xbb\xbf') or data.count(b'\r\n')!=n or not data.endswith(b'\r\n')
          or any(t in data.replace(b'\r\n',b'') for t in (b'\r',b'\n'))):errors.append('B30 exact CRLF/noBOM:'+label)
    if not raw.startswith(b''.join(frozen.splitlines(keepends=True)[:-1])):errors.append('B30 first330 rows/header rawprefix changed')
    try:
        if list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))!=current or list(csv.DictReader(io.StringIO(frozen.decode('utf8'),newline='')))!=previous:errors.append('B30 raw/dictionaries disagree')
    except (UnicodeError,csv.Error):errors.append('B30 malformed raw registry')
    return errors


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=236 or rows(current)[:236]!=rows(previous):return ['B30 G01..236 exact']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{n:02d}' for n in range(1,241)]:return ['B30 only G237..240 in order']
    return []

def residual_errors(current, upstream):
    if len(current) != 14 or len(upstream) != 14:
        return ['B30 all14 upstream residuals required']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_residual_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/residual-disposition-07B29.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or new.get('upstream_contract_ids') != old.get('upstream_contract_ids')):
            errors.append('B30 residual ancestry/hash/contracts')
        for k in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                  'next_step', 'static_exit_criterion', 'current_handoff_or_split_ids'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B30 residual responsibility:' + k)
        if not new.get('required_redacted_input', '').startswith(old.get('required_redacted_input', '')):
            errors.append('B30 no lost old input')
        mapped = {x.replace('7B29-', '7B30-') for x in old.get('current_handoff_or_split_ids', '').split(';') if x}
        if not mapped <= set(new.get('current_handoff_or_split_ids', '').split(';')):
            errors.append('B30 no lost mapped route')
        if (new.get('disposition') != old.get('disposition')
                or new.get('disposition') not in {'external-handoff', 'split-explicitly', 'assessment-source-bound'}
                or new.get('runtime_status') != 'not-executed'):
            errors.append('B30 no residual approval/runtime overclaim')
    return errors

def split_errors(current, upstream):
    if len(current) != 3 or len(upstream) != 3:
        return ['B30 exactlythree upstream splits']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_split_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/split-register-07B29.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or not new.get('required_input', '').startswith(old.get('required_input', ''))):
            errors.append('B30 split ancestry/no lost input')
        for k in ('title', 'candidate_scope_not_certified', 'reason_for_split', 'owner_role', 'required_input',
                  'next_static_action', 'static_exit_criterion'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B30 split responsibility:' + k)
        if new.get('status') != 'explicit-further-static-split-not-started' or new.get('runtime_status') != 'not-executed':
            errors.append('B30 split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work) != 10:
        return ['B30 fourB/sixC axes']
    expected = (['bounded-parent-contract-delivered-residuals-open'] * 2
                + ['bounded-shared-contract-delivered-residuals-open', 'bounded-R4n-import-cancel-delivered-residuals-open']
                + ['planned-not-started'] * 6)
    errors = []
    if [r.get('status') for r in work] != expected or [r.get('part_family') for r in work] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('B30 boundedR4n/sixC unstarted not closure')
    if any(r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false' for r in work):
        errors.append('B30 no runtime/sessions/percent overclaim')
    return errors


def current_link_errors(features,invariants,tests):
    errors=[]
    if (len(features),len(invariants),len(tests))!=(16,16,32):errors.append('B30 FE16/INV16/T32')
    for n,(fe,inv) in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id') or any(inv.get(k)!=fe.get(k) for k in ('finding_ids','evidence','acceptance_ids')):errors.append('B30 FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or ';'.join(t['id'] for t in related)!=fe.get('acceptance_ids'):errors.append('B30 exactlytwo reverse-linked plans')
        if n<=4:
            root='P7-160' if n<=2 else 'P7-159'
            if fe.get('finding_ids')!=root or any(t.get('finding_ids')!=root or t.get('plan_kind')!='finding-specific' for t in related):errors.append('B30 new160 and extension159 split')
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if type(fe.get(k)) is not str or not fe[k].strip():errors.append('B30 capability responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant') for r in invariants})!=16 or len({r.get('acceptance_criterion') for r in tests})!=32:errors.append('B30 distinct substantive criteria')
    if any(t.get('status')!='not-executed' for t in tests):errors.append('B30 integrated plans NOT executed')
    return errors


def ledger_errors(conversion,returns):
    errors=[]
    observations=(['both-tools-menu-entries-wired-not-permission-proof','explicit-not-done-sentinel-until-accept-handler',
      'done-and-nonsentinel-gate-Navigate-only','nonaccepted-purchase-still-clears-note-and-renumbers-current',
      'sale-manifestation-same160-plus-item-and-flag-writes','earlier-writes-before-supplied-candidate-or-failure',
      'later-flags-and-binding-attempt-require-normal-number-return','AcceptedTarget-CopyIntent-AbandonDecision-remain-distinct'],
      ['fresh-false-minusone-blocks-Navigate-not-tail','false-with-valid-token-still-reaches-conversion',
       'true-with-minusone-blocks-Navigate-not-conversion','accepted-import-extends159-not-new161',
       'note-and-sale-items-can-change-before-supplied-number-failure','supplied-ShowDialog-exception-never-reaches-tail',
       'matching-values-can-hide-tail-reachability','adjacent-New-No-denies-reset-not-import-interceptor'])
    for data,bounds,obs in zip((conversion,returns),(CONVERSION_BOUNDARIES,RETURN_BOUNDARIES),observations):
        if len(data)!=8 or [r.get('boundary') for r in data]!=bounds or [r.get('observation') for r in data]!=obs:errors.append('B30 ordered IC8/IR8')
        for r in data:
            for k in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if type(r.get(k)) is not str or not r[k].strip():errors.append('B30 lineage responsibility:'+k)
            if r.get('runtime_status')!='not-executed':errors.append('B30 no lineage runtime')
    return errors


def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_SDK_executed','application_remediation_performed',
      'phase7C_started','phase8_authorized_or_started','all_callers_or_external_DTOs_body_reviewed',
      'actual_WPF_chrome_close_result_or_event_schedule_claimed','SDK_setter_defaults_or_reentrancy_modeled',
      'provider_failure_observed','database_commit_or_saved_loss_claimed','new_GlobalID_allocated_or_SQL_write_claimed'):
        if w.get(k) is not False:errors.append('B30 false-only boundary:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:errors.append('B30 integer-zero:'+k)
    for k in ('normal_nonaccepted_return_and_nonnull_editor_are_supplied','number_result_or_failure_is_supplied',
      'B_R4n_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained',
      'selected_paths_strict_utf8_decode','prior015_046_091_148_151_155_158_not_recounted'):
        if w.get(k) is not True:errors.append('B30 true-only boundary:'+k)
    for k,n in (('illustration_count',18),('lexical_check_count',18),('selected_source_paths',7),('whole_local_files_selected',2),('source_read_slice_count',14)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B30 exact count:'+k)
    erratum=w.get('retained_additive_B10_arithmetic_erratum',{})
    if (erratum!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)
      or any(type(erratum.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or erratum.get('protected_G138_not_rewritten') is not True):errors.append('B30 B10 additive correction')
    if w.get('audit_reference_date_utc')!='2026-11-16' or w.get('entry_checkout')!=ENTRY:errors.append('B30 date/entry')
    if w.get('new_root_ids')!=NEW_IDS or w.get('extended_existing_root_ids')!=EXTENDED_IDS or len(w.get('unadjudicated_source_leads_not_additional_findings',[]))!=4:errors.append('B30 only160/extension159')
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or type(prov.get('environment_clock_observed_utc')) is not str:errors.append('B30 date/raw clock fields')
    for token in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,
      'dda1eafab4188b00a7d6c3e435e7391bd0e09cda',B29_CHECK_SHA,DISPATCHER_SHA,WITNESS_SHA,'259846','867','872','331','107'):
        if token not in note:errors.append('B30 additive identity:'+token)
    if prov.get('genuine_B29_check_record_checkout')==ENTRY:errors.append('B30 official capture is not delivery')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=35 or len(modes)!=35:return ['B30 exactly35 actual OWN modes']
    errors=historical34_errors(dict(historical_mode_count=34,historical_modes=modes[:34],errors=h.get('errors')))
    last=modes[-1]
    expected=dict(mode='B29',findings_total=331,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],
      original_project_hashes_matching=827,audit_checker_self_test_cases_reported=934,audit_checker_self_test_suite_count=30,
      erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0)
    for k,val in expected.items():
        if last.get(k)!=val or type(last.get(k)) is not type(val):errors.append('B30 OWN331/934/30:'+k)
    child=last.get('historical_B29_child') or {}
    expected=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',historical_parser_cutoff='B29-not-current-B30-default',
      all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_dirty_navigation_tests_07B30.py',
      no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,
      historical_source_assertion_input_count=107,auxiliary_dispatcher_text_sha256=DISPATCHER_SHA,
      historical_source_assertions_not_current_execution_tool_inventory=True)
    for k,val in expected.items():
        if child.get(k)!=val or type(child.get(k)) is not type(val):errors.append('B30 ALL48B29 child:'+k)
    if type(last.get('stdout_sha256')) is not str or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B30 actual stdout SHA')
    return errors


def capture_source_errors(history,source_bytes):
    """Only one subsequent helper pin may be reversed IN MEMORY."""
    expected=history.get('checker_sources_at_capture',{});errors=[]
    if set(expected)!=set(source_bytes):return ['B30 actual capture-tool set changed']
    for name,raw in source_bytes.items():
        if name=='tools/validate_import_cancel_part.py':
            final="HISTORICAL_RUN_SHA = '"+str(HISTORICAL_RUN_SHA)+"'  # Pin only after exclusive actual35 capture."
            initial='HISTORICAL_RUN_SHA = None  # Pin only after exclusive actual35 capture.'
            text=raw.decode('utf8')
            if HISTORICAL_RUN_SHA is None or text.count(final)!=1:errors.append('B30 exact-one final pin required');continue
            raw=text.replace(final,initial).encode('utf8')
        if hashlib.sha256(raw).hexdigest()!=expected[name]:errors.append('B30 tool changed beyond single pin:'+name)
    return errors

def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == DOCUMENTARY:
        v.check(row['id'] in SENTINELS, 'B30 undeclared documentary sentinel:' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B30 fabricated source for documentary gate:' + row['id'])
        v.evidence(row['evidence'], row['id'])
        try:
            expanded = expanded_source_evidence(row['evidence'])
        except ValueError as exc:
            v.check(False, 'B30 invalid source ' + row['id'] + ':' + str(exc))
            return
        v.scoped_evidence(expanded, scope, row['id'] + ' boundedB30', phase=7)


def extend_import_cancel(v,report,prov,frozen331):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[331:];ext=rows('evidence/historical-extensions-07B30.csv')
    for error in registry_preservation_errors(frozen331,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes(),ext):ck(False,error)
    ck(len({r['id'] for r in current})==332,'B30 distinct332');v.distributions(new,dict(Medium=1),dict(confirmed=1),'B30 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B30 state not authorization')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B30 exact new registry/report title')
    lookup={r['id']:r for r in current}
    for n in ('P4-014','P7-132','P7-145'):ck(lookup[n]['certainty']=='potential','B30 retained potential:'+n)
    for k in ('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k] is False,'B30 no start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B30 no repair merge')
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B30 no ERP/SQL:'+k)
    for error in date_identity_errors(prov,v.read(v.AUDIT/'DATE-IDENTITY-NOTE-07B30.md')):ck(False,error)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==7,'B30 seven selected paths')
    states={'whole-local-child-body-and-own-XAML-not-all-capabilities-or-runtime','bounded-static-import-number-binding-guard-slices-not-whole-files-or-runtime'}
    for r in selected:
        ck(r['path'] in original and r['review_state'] in states and bool(r['focus']),'B30 scope identity');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    ck(sum(r['review_state'].startswith('whole-local-child') for r in selected)==2,'B30 two whole-local child files only')
    for r in new:validate_source(v,r,scope)
    for n,r in enumerate(ext,1):validate_source(v,dict(id=f'EXT7B30-{n:02d}',evidence=r['appended_evidence']),scope)
    for root in ('P7-046','P7-158'):ck(lookup[root]==next(r for r in frozen331 if r['id']==root),'B30 historical root exact:'+root)
    known={r['id'] for r in current}|{f'H7B30-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B30.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(type(x) is str and x.strip() for x in r.values()),'B30 completeCSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B30 no runtime:'+r['id'])
    fe,inv,tests=[tables[x] for x in ('FE7B30-','INV7B30-','P7B30T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['IC7B30-'],tables['IR7B30-']):ck(False,error)
    ck(fe[0]['status']==fe[1]['status']=='confirmed-source-local' and fe[2]['status']==fe[3]['status']=='additive-source-extension-of-existing159','B30 root160/159 extension not four findings')
    v.proposed_tests(tests,'7B30');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['IC7B30-']+tables['IR7B30-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B30 '+label)
    for r in tables['RC7B30-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ck(r['finding_ids']==unique('finding_ids') and r['acceptance_ids']==unique('acceptance_ids') and r['evidence']==source_evidence_union(fs),'B30 expanded-before-dedup RC')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B30-'],rows('evidence/residual-disposition-07B29.csv'))+split_errors(tables['SP7B30-'],rows('evidence/split-register-07B29.csv'))+remaining_work_errors(tables['RW7B30-']):ck(False,error)
    hids={r['id'] for r in tables['H7B30-']};sids={r['id'] for r in tables['SP7B30-']}
    v.related(tables['RS7B30-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B30-'],hids,'handoff_ids')
    for r in tables['H7B30-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B30 no approval')
    for r in tables['Q7B30-']:ck(r['status']=='unanswered-no-secrets-requested','B30 no invented answer')
    for n,r in enumerate(tables['BK7B30-'],1):ck(r['prior_backlog_id']==f'BK7B29-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B30 backlog ancestry/uncompleted')
    ck([r['status'] for r in tables['BK7B30-'][2:6]]==['not-started']*4,'B30 C unstarted')
    ad=tables['AD7B30-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B30 onlyone160')
    ck([r['current_root_ids'] for r in ad if r['decision']=='extended-existing-root-not-new']==EXTENDED_IDS,'B30 only159 extended')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B30 honest dedup depth')
    ck(set(new[0]['evidence'].split(';'))<=set(ad[0]['evidence'].split(';')),'B30 adjudicated new source chain')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,30)]
    before={r['path'] for n in prior_names for r in rows(n)};paths=set(scope);rem=original.keys()-(before|paths)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(bk==dict(selected_paths=7,prior_union=426,overlap=6,new=1,union=427,complement=400,complement_kinds={'source':335,'generated-artifact':61,'project-or-resource':4}),'B30 bookkeeping not coverage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B30.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B29.md','evidence/split-register-07B29.csv','evidence/residual-disposition-07B29.csv'] and decision['selected_upstream_split']=='SP7B29-01' and decision['entry']==ENTRY and decision['bookkeeping']==bk,'B30 bounded authority')
    ck(set(decision['new_paths'])==paths-before and decision['historical_metadata_screen_count']==331 and decision['path_matched_metadata_rows']==78 and decision['historical_body_review_claim'] is False and decision['historical_comparison_depth']==DEDUP_DEPTH,'B30 honest metadata depth')
    ck(decision['bounded_read_slice_count']==14 and decision['whole_local_files']==2 and decision['one_new_root']==NEW_IDS and decision['existing_root_extensions']==EXTENDED_IDS,'B30 14reads/whole2/root1/ext1')
    for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k] is False,'B30 permission:'+k)
    wp='evidence/import-cancel-witnesses-07B30.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B30 immutable witness')
    w,match=v.recompute(wp,'tools/check_import_cancel_witnesses.py')
    for error in witness_metadata_errors(w):ck(False,error)
    ck(w['errors']==[],'B30 witness inert/lexical pass')
    for key,prefix,flag in (('illustrations','ALG7B30-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B30-','documented_text_observation_matches')):
        data=w[key];v.sequential(data,prefix,18);v.related(data,known)
        for r in data:ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B30 witness boundary');validate_source(v,r,scope)
    reads=w['bounded_source_reads_not_semantic_coverage'];ck(len(reads)==14 and {r['path'] for r in reads}==paths and sum(r['whole_local_file_selected'] for r in reads)==2,'B30 14reads/7paths/twowholechild')
    for r in reads:
        ck(r['encoding']=='strict-utf-8' and type(r['whole_local_file_selected']) is bool and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is (not r['whole_local_file_selected']) and v.sha(v.ROOT/r['path'])==r['sha256'],'B30 source depth/hash')
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B30 source read',phase=7)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,error)
    pending=False
    source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B30.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B30 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B30.md','PHASE-07-REMAINING-07B30.md','7B31','غير مأذونة','3589d23','10ba215')),'B30 shared entrypoint:'+name)
    hp='evidence/historical-mode-verification-07B30.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B30 actual35 capture exists')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B30 actual35 identity');h=v.json.loads(v.read(v.AUDIT/hp))
        for error in historical_record_errors(h):ck(False,error)
        ck(h['checkout_head']==ENTRY and h['source_head']==v.HEAD and h['branch']==v.BRANCH,'B30 actual capture entry/source')
        sources={p.relative_to(v.AUDIT).as_posix():p.read_bytes() for p in sorted((v.AUDIT/'tools').glob('*.py'))}
        ck(len(sources)==111,'B30 actual execution tool count111 distinct from107 OWN input vector')
        for error in capture_source_errors(h,sources):ck(False,error)
        report['phase_7B30_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=35,
          all_documentary_exit_codes_zero=True,B29_OWN331_raw332CRLF_ALL48_and107_source_assertion_inputs=True,
          B28_ALL48_B27_ALL52_B26_ALL48_B25_ALL44_B24_ALL44_retained=True,capture_tool_count=len(sources),
          null_means_unreported_not_zero=True,only_later_single_pin_reversible_in_memory=True,not_final_or_postpush_wholesale_replay=True)
    tools=['check_import_cancel_witnesses.py','validate_import_cancel_part.py','run_historical_dirty_navigation_tests_07B30.py','test_import_cancel_audit_validator.py']
    for n in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/n),filename=n)
        except SyntaxError as exc:ck(False,'B30 audit-tool syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==52
    ck(passed,'B30 52 documentary cases/count: '+(run.stderr[-10000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=52,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B30-332-bounded-R4n-import-cancel-not7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,31))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B31-proposed-R4o-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=160,phase_7B30=1,total_open_not_remediated=332,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:7,'phase_7B30_prior_union':426,'phase_7B30_overlap_with_prior_union':6,'phase_7B30_new_paths':1,'unique_union_not_line_or_execution_coverage':427,'inventory_only_no_selected_scope':400})
    report['phase_7B29_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_evidence_artifacts_hash_checked=867,historical_check_record_overwritten=False,genuine_B29_stdout_sha256_unchanged=B29_CHECK_SHA,all331_core_ALLnext_phase_and_old_evidence_prefixes_preserved=True,only_P7_159_evidence_tail_appended=ext,other330_dictionaries_exact=True,original331_raw332CRLF_preserved_in_snapshot=True,first330_raw_rows_and_header_prefix_exact=True,auxiliary_dispatcher_text_is_assertion_input_not_current_executed_code=DISPATCHER_SNAPSHOT)
    report['phase_7B30_import_cancel_trace_limits']=dict(import_conversion_boundaries=8,import_return_boundaries=8,bounded_source_reads=14,selected_paths=7,new_union_paths=1,whole_local_child_files=2,current_features_or_documentary_contracts=16,invariants_not_executed_tests=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_further_static_splits=3,new_root_ids=NEW_IDS,existing_root_extensions=ext,B_R4n_delivered_not_whole_SP01_R4_or7B_closure=True,retained_potential_roots=['P4-014','P7-132','P7-145'],normal_nonaccepted_return_nonnull_editor_and_normal_setters_supplied=True,number_candidate_or_failure_supplied_not_provider_observed=True,normal_accepted_Navigate_outcome_supplied_not_complete_hydration=True,actual_chrome_Close_bool_or_event_schedule_not_claimed=True,new_GlobalID_or_SQL_write_or_saved_loss_claimed=False,boundary_is_pre_binding_not_post_event_stability=True,all_callers_or_external_DTOs_body_reviewed=False,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synchronized_not_asserted=True)
    report['evidence_rows'].update(phase_7B30_illustrations_not_ERP_tests=18,phase_7B30_lexical_checks_not_ERP_tests=18,phase_7B30_bounded_source_reads_not_semantic_coverage=14,phase_7B30_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only bounded B30/R4n;867 protected of872 entry;OWN331/raw332CRLF snapshot. All331 core/ALLnext_phase/status/classification and old evidence prefixes exact;sole explicit159.evidence manifest tail;other330 dictionaries/first330 raw rows+header exact. Current332/raw333CRLF;new160 once Medium confirmed-source-local. Fresh child defaults false/-1;NORMAL nonaccepted return blocks directNavigate but NOT conversion tail of purchase/sale:note/number/new and saleimpact/items/printed/updated. Explicit nonnull editor/items and ordinary setters;candidate number or failure SUPPLIED. Earlier writes precede number helper;later flags and binding require its normal return. No WPF chrome/Close bool?/event ordering/reentrancy/SDK defaults/stable post-binding state inferred. No SQL/provider/reservation/newGlobalID/save/loss/stock observation. Accepted import is existing159 extension,not new161;target acceptance distinct fromCopyIntent/AbandonDecision. WholeLOCAL child419C#/449XAML only,14reads/7paths with6overlap+1new->427/complement400 bookkeeping not all477bodies/455FE/callers/fields/writers/output. Metadata331/78pathmatches plus selected nearest bodies/chains,not all331bodies.32plansNOTexecuted;IC8/IR8/FE16/INV16/RC6/AD8/RS14/SP3/HQ6 preserve ancestry/fullinputprefix/allmappedroutes/dispositions,not approvals.014/132/145potential,020/021 andfinancial/ACL/stock/save/productionbarriers preserved. Existing015/046/091/148/151/155–158notrecounted. OtherSP01–03 includingProduct/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome,census,SDK/currency/precision/templates remain7B. ALL48originalB29 cases viaOWN331/raw332CRLF/indexes/presetB29/suite-localA plus exact107 historical source-assertion vector and auxiliary dispatcherTEXT;NOT old executable code or actual current tool inventory. CurrentB30 parser/AST/111tools checked independently;APIdefaultB15/versionedB29 distinct. No protected edit/skip/globalPath/sharedsubprocess mutation/diskoverlay/rebaseline/archive rewrite. Actual35 processes summarized with capture-time111tool hashes;onlyone later pin inverted in memory,not final/postpush wholesale replay. Session context2026-11-16 and raw observed clock2026-11-20 have distinct provenance;protectedB29 date note retained,not calibrated/backdated. Application10ba/officialB29capturedondda/B29deliveryandB30entry3589/freshentryrun distinct. B10 additive10vs120/equality1=10/G138 retained.7B/7partial,R4o/B31proposed,7Cunstarted,8unauthorized;repair start/syncunknown;next_phase8planningonly.')
