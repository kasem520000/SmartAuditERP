#!/usr/bin/env python3
"""Read-only B28/R4l documentary checks, never application acceptance.

One new158 (empty max guard), one additive046 source-failure publication chain.
Protect797/all329 exact dictionaries/ALLnext_phase/evidence/raw330CRLF/G228/
827 originals/three freezes. ALL52 original B27 cases use explicit OWN329/
raw330CRLF/indexes/presetB27 child with suite-local A. No skips/protected edits/
global Path/shared subprocess patches/disk overlays/rebaseline/archive rewrite.
Five existing paths/six reads, locally whole698C#/561XAML search, not all callers,
reader/DTOs/477bodies/capability census/455FE.16FE/INV/32plans not-executed;
7B/7 partial,R4m/B29 proposed,7C unstarted,8 unauthorized. No ERP/SQL/DataView/
WPF/.NET/SDK/provider/financial/stock/save/remediation or measured loss.
"""
from __future__ import annotations
import collections
from contextlib import contextmanager
import csv
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,bidirectional_errors
from validate_contract_item_part import row_sha,expanded_source_evidence
from validate_property_dialog_part import source_evidence_union
from validate_invoice_search_part import historical_record_errors as historical32_errors
ENTRY = '436446091caf82c05ec01817bed5d18b4ea9fb34'
SNAPSHOT = 'evidence/findings-through-07B27.csv'
SNAPSHOT_SHA = '02991248c302ccad9a293c13f2352d636e2a754f8e9efd9f3b739950514e67fc'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B27.json'
SHARED_SHA = '9b49467df1629279d9281c67d959b8df7559671c03de9ee122f4e65ccb71af5e'
PROVENANCE_SHA = '65cc59c8dd13e00104b8d644e3f180328acd4eb46cfd4eacf1a1a46ba4e3e627'
B27_CHECK_SHA = 'a8c7c93372d1d0c20c78498fa44252f04bb5f415036b9df7df690f5ad68b02cb'
WITNESS_SHA = '91baacdbd5c81090c40b93c27187822494a51103ac5ee0a7aec94974746dd9fb'
HISTORICAL_RUN_SHA = '817fcc6dc17a9993d6ed057455422dab7c23011dec58dfb5c3ed79a270fc3aa6'  # Actual33 capture, not synthetic fixture or post-pin replay.
SCOPE_FILE = 'review-scope-07B28.csv'
DOCUMENTARY = 'none-documentary-metadata'
NEW_IDS = ['P7-158']
EXTENDED_IDS = ['P7-046']
PART_DOCS = ('PHASE-07B28.md','SEARCH-SNAPSHOT-CONTRACTS-07B28.md','VALIDATION-07B28.md',
             'PHASE-07-REMAINING-07B28.md','DATE-IDENTITY-NOTE-07B28.md')
SHARED_DOCS = ('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS = (
 ('load-health-lineage','LH7B28-',8),('filter-removal-lineage','FR7B28-',6),
 ('feature-implementation-matrix','FE7B28-',16),('report-invariants','INV7B28-',16),
 ('acceptance-tests','P7B28T-',32),('report-reconciliation','RC7B28-',6),
 ('root-adjudication','AD7B28-',8),('residual-disposition','RS7B28-',14),('split-register','SP7B28-',3),
 ('handoffs','H7B28-',6),('questions','Q7B28-',6),('remaining-workplan','RW7B28-',10),('continuation-backlog','BK7B28-',10))
SENTINELS = {f'{p}{n:02d}' for p,ns in (('FE7B28-',range(15,17)),('INV7B28-',range(15,17)),
 ('P7B28T-',range(29,33)),('RC7B28-',(5,6)),('AD7B28-',(7,8)),('RS7B28-',range(1,15)),('H7B28-',range(1,7)),('Q7B28-',range(1,7))) for n in ns}
HEALTH_BOUNDARIES = ['independent-master-display','explicit-new-date-request','fill-before-publication','ordinary-selection-surface',
 'selected-purchase-consumer','selected-reader-boundary','success-empty-failure-controls','external-health-contract']
FILTER_BOUNDARIES = ['maximum-nonempty','maximum-empty','minimum-empty-control','wider-max-control','clear-reload-control','fresh-empty-control']
DEDUP_DEPTH = 'all329-title-severity-certainty-summaries-plus-path-filtered-metadata-and-selected-nearest-doc-bodies-source-chains-not-all-historical-bodies'

@contextmanager
def historical_b27_inputs(v, frozen329, texts, raw):
    """Exact OWN329 input in a context-local path, never a global pathlib patch."""
    if len(frozen329) != 329 or len({r.get('id') for r in frozen329}) != 329:
        raise ValueError('Exactly329 distinct B27 OWN rows required')
    if set(texts) != set(SHARED_DOCS) or any(not isinstance(s, str) for s in texts.values()):
        raise ValueError('Exactly three frozen shared texts required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM frozen bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('Malformed329 frozen registry') from exc
    if (parsed != frozen329 or raw.count(b'\r\n') != 330 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        raise ValueError('329 rows/raw330CRLF disagree')
    original = v.AUDIT
    target = (original / 'findings.csv').resolve()

    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve() == target else super().read_bytes()

        def read_text(self, encoding=None, errors=None):
            if self.resolve() == target:
                return io.StringIO(raw.decode(encoding or 'utf-8', errors or 'strict'), newline=None).read()
            return super().read_text(encoding=encoding, errors=errors)

    try:
        v.AUDIT = FrozenRegistryPath(original)
        with historical_b1_inputs(v, frozen329, texts):
            yield
    finally:
        v.AUDIT = original

class HistoricalB27Subprocess:
    """Redirect ONLY the exact protected B27 suite argv; preserve other calls."""
    def __init__(self, backend, python, tool_dir):
        self.backend = backend
        self.expected = [python, '-B', str(tool_dir / 'test_invoice_search_audit_validator.py')]
        self.actual = [python, '-B', str(tool_dir / 'run_historical_invoice_search_tests_07B28.py'),
                       '--through-part', 'B27']

    def __getattr__(self, name):
        return getattr(self.backend, name)

    def run(self, args, *pos, **kwargs):
        return self.backend.run(self.actual if args == self.expected else args, *pos, **kwargs)

class HistoricalB27ValidatorView:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)
        object.__setattr__(self, '_subprocess', HistoricalB27Subprocess(
            target.subprocess, target.sys.executable, target.AUDIT / 'tools'))

    def __getattr__(self, name):
        return self._subprocess if name == 'subprocess' else getattr(self._target, name)

    def __setattr__(self, name, value):
        setattr(self._target, name, value)

@contextmanager
def historical_b27_validation(v,report,prior,prov,frozen329):
    ck=v.check
    for name,digest in (('evidence/provenance-07B28.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),
                        (SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B27.json',B27_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B28 immutable entry:'+name)
    ck(prov['historical_artifact_count']==797 and len(frozen329)==329,'B28 protected797/OWN329')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
       and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B28 frozen entry identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B28 protected765-to797 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B27.json'));suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='6eedc0640e3432c14ca0875b7f1c7806ea1e3f64' and old['findings']['total_open_not_remediated']==329
       and old['original_project_hashes_matching']==827 and old['validation']['errors']==[]
       and old['validation']['current_output_record_pending_first_write_not_placeholder'] is False,'B28 B27 genuine capture6eed not delivery436')
    ck(len(suites)==28 and sum(s['tests_reported'] for s in suites.values())==838
       and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B28 genuine B27 838/28/765')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
       and prov['genuine_B27_check_sha256']==B27_CHECK_SHA and prov['genuine_B27_check_record_checkout']==old['checkout_head'],'B28 completed pushed B27 entry')
    ck(prov['phase7B27_entry_consistency']==dict(original_hashes_matching=827,findings=329,audit_file_count=802,
       documentary_cases=838,self_test_suites=28,errors=[],erp_runtime_tests_executed=0),'B28 actual independent entry consistency')
    recovery=prov['local_git_history_reconciliation']
    ck(recovery['initial_local_tip']==v.HEAD and recovery['remote_delivered_tip']==ENTRY
       and all(recovery[k] is True for k in recovery if k not in ('initial_local_tip','remote_delivered_tip')),'B28 file-preserving history reconciliation not a new source')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB27ValidatorView(v)
    with historical_b27_inputs(view,frozen329,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    rec=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_invoice_search_audit_validator.py']
    rec.update(historical_parser_cutoff='B27-not-current-B28-default',all_original_cases_executed_unmodified=True,
       dedicated_child_launcher='tools/run_historical_invoice_search_tests_07B28.py',actual_subprocess_argv=view.subprocess.actual,
       no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B27-329-not-current-state',
       phase_7B27_historical_input_mode='OWN329-exact330CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B27-test-child',
       phase_7B27_adapter_context=dict(entry_provenance='evidence/provenance-07B28.json',adapter_protected_artifacts_checked=797,
          current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
          B27_parser_assertions_are_historical_preset_not_current_default=True,B27_suite_own_A_uses_context_local_registry_path=True))

def registry_preservation_errors(previous, current, raw, frozen):
    errors = []
    if len(previous) != 329 or current[:329] != previous:
        errors.append('B28 all329 exact fields/ALLnext_phase/evidence')
    if len(current) != 330 or [r.get('id') for r in current[329:]] != NEW_IDS:
        errors.append('B28 only appended158')
    if (type(raw) is not bytes or type(frozen) is not bytes or not raw.startswith(frozen)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n') != 331 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        errors.append('B28 exact329 rawprefix/331CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline=''))) != current:
                errors.append('B28 raw/rows disagree')
        except (UnicodeError, csv.Error):
            errors.append('B28 malformed registry')
    return errors

def group_row_errors(previous, current):
    rows = lambda s: re.findall(r'^\| G-\d{2,3} \|.*$', s, re.M)
    if len(rows(previous)) != 228 or rows(current)[:228] != rows(previous):
        return ['B28 G01..228 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|', current, re.M) != [f'G-{n:02d}' for n in range(1, 233)]:
        return ['B28 only G229..232 exact order']
    return []

def residual_errors(current, upstream):
    if len(current) != 14 or len(upstream) != 14:
        return ['B28 all14 upstream residuals required']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_residual_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/residual-disposition-07B27.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or new.get('upstream_contract_ids') != old.get('upstream_contract_ids')):
            errors.append('B28 residual ancestry/hash/contracts')
        for k in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                  'next_step', 'static_exit_criterion', 'current_handoff_or_split_ids'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B28 residual responsibility:' + k)
        if not new.get('required_redacted_input', '').startswith(old.get('required_redacted_input', '')):
            errors.append('B28 no lost old input')
        mapped = {x.replace('7B27-', '7B28-') for x in old.get('current_handoff_or_split_ids', '').split(';') if x}
        if not mapped <= set(new.get('current_handoff_or_split_ids', '').split(';')):
            errors.append('B28 no lost mapped route')
        if (new.get('disposition') != old.get('disposition')
                or new.get('disposition') not in {'external-handoff', 'split-explicitly', 'assessment-source-bound'}
                or new.get('runtime_status') != 'not-executed'):
            errors.append('B28 no residual approval/runtime overclaim')
    return errors

def split_errors(current, upstream):
    if len(current) != 3 or len(upstream) != 3:
        return ['B28 exactlythree upstream splits']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_split_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/split-register-07B27.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or not new.get('required_input', '').startswith(old.get('required_input', ''))):
            errors.append('B28 split ancestry/no lost input')
        for k in ('title', 'candidate_scope_not_certified', 'reason_for_split', 'owner_role', 'required_input',
                  'next_static_action', 'static_exit_criterion'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B28 split responsibility:' + k)
        if new.get('status') != 'explicit-further-static-split-not-started' or new.get('runtime_status') != 'not-executed':
            errors.append('B28 split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work) != 10:
        return ['B28 fourB/sixC axes']
    expected = (['bounded-parent-contract-delivered-residuals-open'] * 2
                + ['bounded-shared-contract-delivered-residuals-open', 'bounded-R4l-search-snapshot-delivered-residuals-open']
                + ['planned-not-started'] * 6)
    errors = []
    if [r.get('status') for r in work] != expected or [r.get('part_family') for r in work] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('B28 boundedR4l/sixC unstarted not closure')
    if any(r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false' for r in work):
        errors.append('B28 no runtime/sessions/percent overclaim')
    return errors

def current_link_errors(features,invariants,tests):
    errors=[]
    if (len(features),len(invariants),len(tests))!=(16,16,32):errors.append('B28 FE16/INV16/T32')
    for n,(fe,inv) in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id') or any(inv.get(k)!=fe.get(k) for k in ('finding_ids','evidence','acceptance_ids')):errors.append('B28 FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or ';'.join(t['id'] for t in related)!=fe.get('acceptance_ids'):errors.append('B28 two reverse-linked plans')
        if n<=2:
            root=('P7-158','P7-046')[n-1]
            if fe.get('finding_ids')!=root or any(t.get('finding_ids')!=root or t.get('plan_kind')!='finding-specific' for t in related):errors.append('B28 one new158 one existing046 plans')
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(fe.get(k),str) or not fe[k].strip():errors.append('B28 capability responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant') for r in invariants})!=16 or len({r.get('acceptance_criterion') for r in tests})!=32:errors.append('B28 distinct substantive invariant/criteria')
    if any(t.get('status')!='not-executed' for t in tests):errors.append('B28 integrated plans never executed')
    return errors


def ledger_errors(health,filters):
    errors=[]
    observations=(['master-clear-does-not-clear-independent-display','both-date-handlers-clear-master-reload-not-event-count',
      'failure-before-refresh-retains-old-display-existing046','done-GID-from-old-display-no-health-gate',
      'GID-branch-do-not-certify-request-success','reader-maps-identity-not-request-outcome',
      'successful-empty-distinct-from-failed-unknown','period-parser-return-provider-DTO-remain-unresolved'],
      ['valid-nonempty-max-applies-filter','empty-max-skips-filter-new158-not-fixed-source155',
       'minimum-empty-unconditionally-applies-filter','nonempty30-restores20-from-existing-master',
       'explicit-clear-success-recovers-not-156-approval','empty-alone-needs-prior-stale-view'])
    for data,bounds,obs in zip((health,filters),(HEALTH_BOUNDARIES,FILTER_BOUNDARIES),observations):
        if len(data)!=len(bounds) or [r.get('boundary') for r in data]!=bounds or [r.get('observation') for r in data]!=obs:errors.append('B28 ordered health8/filter6 observations')
        for row in data:
            for k in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(row.get(k),str) or not row[k].strip():errors.append('B28 lineage responsibility:'+k)
            if row.get('runtime_status')!='not-executed':errors.append('B28 lineage runtime overclaim')
    return errors


def extension_errors(extensions):
    from check_search_snapshot_witnesses import EV_LOAD,EV_CONSUMER
    if len(extensions)!=1 or extensions[0].get('finding_id')!='P7-046':return ['B28 exactly one046 extension, not another root']
    row=extensions[0]
    if row.get('appended_evidence')!=EV_LOAD+';'+EV_CONSUMER or not row.get('reason','').strip():return ['B28 exact046 additive source chain/limit']
    return []


def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_DataView_executed','application_remediation_performed',
      'phase7C_started','phase8_authorized_or_started','all_callers_or_external_DTOs_body_reviewed','actual_WPF_event_order_or_count_claimed',
      'financial_or_status_policy_invented','external_DTO_constructor_defaults_assumed','database_commit_or_saved_loss_claimed','provider_failure_or_partial_fill_observed'):
        if w.get(k) is not False:errors.append('B28 false-only boundary:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:errors.append('B28 integer-zero boundary:'+k)
    for k in ('B_R4l_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained','selected_paths_strict_utf8_decode','prior045_046_085_155_156_157_not_recounted'):
        if w.get(k) is not True:errors.append('B28 true-only boundary:'+k)
    for k,n in (('illustration_count',16),('lexical_check_count',16),('selected_source_paths',5),('whole_local_search_files_selected',2),('source_read_slice_count',6)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B28 exact count:'+k)
    e=w.get('retained_additive_B10_arithmetic_erratum',{})
    if (e!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)
        or any(type(e.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or e.get('protected_G138_not_rewritten') is not True):errors.append('B28 retained additive B10 correction')
    if w.get('audit_reference_date_utc')!='2026-11-16' or w.get('entry_checkout')!=ENTRY:errors.append('B28 reference/entry')
    if w.get('new_root_ids')!=NEW_IDS or w.get('extended_existing_root_ids')!=EXTENDED_IDS or len(w.get('unadjudicated_source_leads_not_additional_findings',[]))!=4:errors.append('B28 no recount/extra-root boundary')
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or not isinstance(prov.get('environment_clock_observed_utc'),str):errors.append('B28 date source fields')
    for token in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,'6eedc0640e3432c14ca0875b7f1c7806ea1e3f64',B27_CHECK_SHA,'238566','797','329','802',WITNESS_SHA):
        if token not in note:errors.append('B28 additive identity:'+token)
    if prov.get('genuine_B27_check_record_checkout')==ENTRY:errors.append('B28 capture cannot be relabelled delivery')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=33 or len(modes)!=33:return ['B28 exactly33 actual OWN modes required']
    errors=historical32_errors(dict(historical_mode_count=32,historical_modes=modes[:32],errors=h.get('errors')))
    last=modes[-1]
    expected=dict(mode='B27',findings_total=329,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],
       original_project_hashes_matching=827,audit_checker_self_test_cases_reported=838,audit_checker_self_test_suite_count=28,
       erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0)
    for k,value in expected.items():
        if last.get(k)!=value or type(last.get(k)) is not type(value):errors.append('B28 B27 OWN329/838/28:'+k)
    child=last.get('historical_B27_child') or {}
    expected=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B27-not-current-B28-default',
       all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_invoice_search_tests_07B28.py',
       no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    for k,value in expected.items():
        if child.get(k)!=value or type(child.get(k)) is not type(value):errors.append('B28 B27 ALL52 child:'+k)
    if not isinstance(last.get('stdout_sha256'),str) or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B28 historical stdout identity')
    return errors

def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == DOCUMENTARY:
        v.check(row['id'] in SENTINELS, 'B28 undeclared documentary sentinel:' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B28 fabricated source for documentary gate:' + row['id'])
        v.evidence(row['evidence'], row['id'])
        try:
            expanded = expanded_source_evidence(row['evidence'])
        except ValueError as exc:
            v.check(False, 'B28 invalid source ' + row['id'] + ':' + str(exc))
            return
        v.scoped_evidence(expanded, scope, row['id'] + ' boundedB28', phase=7)

def extend_search_snapshot(v,report,prov,frozen329):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[329:]
    for error in registry_preservation_errors(frozen329,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id'] for r in current})==330,'B28 distinct330 IDs');v.distributions(new,dict(Medium=1),dict(confirmed=1),'B28 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B28 finding permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B28 heading/registry exact')
    lookup={r['id']:r for r in current}
    for n in ('P4-014','P7-132','P7-145'):ck(lookup[n]['certainty']=='potential','B28 retained potential:'+n)
    for k in ('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k] is False,'B28 no implicit start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B28 no repair merge')
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B28 no ERP/SQL:'+k)
    for error in date_identity_errors(prov,v.read(v.AUDIT/'DATE-IDENTITY-NOTE-07B28.md')):ck(False,error)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==5,'B28 five bounded existing paths')
    for r in selected:
        ck(r['path'] in original and r['review_state']=='whole-local-search-or-selected-consumer-reader-static-slices-not-runtime-certified' and bool(r['focus']),'B28 scope identity/depth')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    ext=rows('evidence/historical-extensions-07B28.csv')
    for error in extension_errors(ext):ck(False,error)
    for n,r in enumerate(ext,1):validate_source(v,dict(id=f'EX7B28-{n:02d}',evidence=r['appended_evidence']),scope)
    ck(lookup['P7-046']==next(r for r in frozen329 if r['id']=='P7-046'),'B28 extension never rewrites046 dictionary')
    known={r['id'] for r in current}|{f'H7B28-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B28.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str) and x.strip() for x in r.values()),'B28 completeCSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B28 no runtime claim:'+r['id'])
    fe,inv,tests=[tables[x] for x in ('FE7B28-','INV7B28-','P7B28T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['LH7B28-'],tables['FR7B28-']):ck(False,error)
    ck(fe[0]['status']=='confirmed-source-local' and fe[1]['status']=='confirmed-existing-root-extension','B28 one new one extension')
    v.proposed_tests(tests,'7B28');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['LH7B28-']+tables['FR7B28-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B28 '+label)
    ck(all(any('P7-046' in r['finding_ids'].split(';') for r in pool) for pool in (fe,inv,tests)),'B28 extension has independent plans/invariant')
    for r in tables['RC7B28-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ck(r['finding_ids']==unique('finding_ids') and r['acceptance_ids']==unique('acceptance_ids') and r['evidence']==source_evidence_union(fs),'B28 expanded-before-dedup RC lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B28-'],rows('evidence/residual-disposition-07B27.csv'))+split_errors(tables['SP7B28-'],rows('evidence/split-register-07B27.csv'))+remaining_work_errors(tables['RW7B28-']):ck(False,error)
    hids={r['id'] for r in tables['H7B28-']};sids={r['id'] for r in tables['SP7B28-']}
    v.related(tables['RS7B28-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B28-'],hids,'handoff_ids')
    for r in tables['H7B28-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B28 no invented approval')
    for r in tables['Q7B28-']:ck(r['status']=='unanswered-no-secrets-requested','B28 no invented answer')
    for n,r in enumerate(tables['BK7B28-'],1):ck(r['prior_backlog_id']==f'BK7B27-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B28 backlog ancestry/uncompleted')
    ck([r['status'] for r in tables['BK7B28-'][2:6]]==['not-started']*4,'B28 C axes unstarted')
    ad=tables['AD7B28-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B28 only one new158')
    ck([r['current_root_ids'] for r in ad if r['decision']=='extended-existing-root-not-new']==EXTENDED_IDS,'B28 existing046 not new159')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B28 honest dedup depth')
    ck(set(new[0]['evidence'].split(';'))<=set(ad[0]['evidence'].split(';')),'B28 adjudicated source chain')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,28)]
    before={r['path'] for n in prior_names for r in rows(n)};paths=set(scope);rem=original.keys()-(before|paths)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(bk==dict(selected_paths=5,prior_union=426,overlap=5,new=0,union=426,complement=401,complement_kinds={'source':336,'generated-artifact':61,'project-or-resource':4}),'B28 bookkeeping not percentage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B28.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B27.md','evidence/split-register-07B27.csv','evidence/residual-disposition-07B27.csv'] and decision['selected_upstream_split']=='SP7B27-01' and decision['entry']==ENTRY and decision['bookkeeping']==bk,'B28 reasoned scope authority')
    ck(set(decision['new_paths'])==paths-before and decision['historical_metadata_screen_count']==329 and decision['historical_body_review_claim'] is False and decision['historical_comparison_depth']==DEDUP_DEPTH,'B28 comparison depth')
    ck(decision['bounded_read_slice_count']==6 and decision['whole_local_search_files']==2 and decision['whole_local_search_lines']==dict(code_behind=698,xaml=561),'B28 whole local only')
    ck(decision['one_new_root']==NEW_IDS and decision['one_existing_root_extended']==EXTENDED_IDS,'B28 no padded count')
    for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k] is False,'B28 scope permission:'+k)
    wp='evidence/search-snapshot-witnesses-07B28.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B28 immutable successful witness stdout')
    witness,match=v.recompute(wp,'tools/check_search_snapshot_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B28 successful witness observations')
    for key,prefix,flag in (('illustrations','ALG7B28-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B28-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,16);v.related(data,known)
        for r in data:ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B28 witness inert');validate_source(v,r,scope)
    reads=witness['bounded_source_reads_not_semantic_coverage'];ck(len(reads)==6 and {r['path'] for r in reads}==paths,'B28 actual six reads five paths')
    ck(sum(r['whole_local_file_selected'] is True for r in reads)==2,'B28 onlytwo locally whole search files')
    for r in reads:
        ck(r['encoding']=='strict-utf-8' and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True and v.sha(v.ROOT/r['path'])==r['sha256'],'B28 hashes/depth')
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B28 source read',phase=7)
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
            if target==(v.AUDIT/'evidence/checks-07B28.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B28 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B28.md','PHASE-07-REMAINING-07B28.md','7B29','غير مأذونة','4364460','10ba215')),'B28 shared current boundary:'+name)
    hp='evidence/historical-mode-verification-07B28.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B28 actual33 captured')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B28 actual33 archive identity');history=v.json.loads(v.read(v.AUDIT/hp))
        for error in historical_record_errors(history):ck(False,error)
        ck(history['checkout_head']==ENTRY and history['source_head']==v.HEAD and history['branch']==v.BRANCH,'B28 historical source/entry/capture')
        report['phase_7B28_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=33,all_documentary_exit_codes_zero=True,B27_OWN329_raw330CRLF_and_historical52_child=True,B26_ALL48_B25_ALL44_B24_ALL44_retained=True,null_means_unreported_not_zero=True,not_original_metric_replay_or_ERP_tests=True)
    tools=['check_search_snapshot_witnesses.py','validate_search_snapshot_part.py','run_historical_invoice_search_tests_07B28.py','test_search_snapshot_audit_validator.py']
    for n in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/n),filename=n)
        except SyntaxError as exc:ck(False,'B28 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==48
    ck(passed,'B28 48 documentary tests/count: '+(run.stderr[-7000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=48,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B28-330-bounded-R4l-search-snapshot-not-7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,29))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B29-proposed-R4m-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=158,phase_7B28=1,total_open_not_remediated=330,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:5,'phase_7B28_prior_union':426,'phase_7B28_overlap_with_prior_union':5,'phase_7B28_new_paths':0,'unique_union_not_line_or_execution_coverage':426,'inventory_only_no_selected_scope':401})
    report['phase_7B27_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=797,historical_check_record_overwritten=False,genuine_B27_stdout_sha256_unchanged=B27_CHECK_SHA,all329_dictionaries_ALLnext_phase_evidence_rawprefix_preserved=True)
    report['phase_7B28_search_snapshot_trace_limits']=dict(load_health_boundaries=8,filter_removal_boundaries=6,bounded_source_reads=6,selected_paths=5,new_union_paths=0,whole_local_search_files=2,whole_local_search_lines=1259,current_features_or_documentary_contracts=16,invariants_not_executed_tests=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_further_static_splits=3,new_root_ids=NEW_IDS,additive_existing_root_extensions=ext,B_R4l_delivered_not_whole_SP01_R4_or7B_closure=True,retained_potential_roots=['P4-014','P7-132','P7-145'],actual_provider_failure_or_partial_fill_observed=False,stale_display_model_extends046_not_new159=True,missing_max_empty_branch_not_fixed_SQL_source155=True,period_postponed_quoting_return_leads_not_additional_findings=True,database_commit_or_saved_loss_claimed=False,all_callers_or_external_DTOs_body_reviewed=False,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synchronized_not_asserted=True)
    report['evidence_rows'].update(phase_7B28_illustrations_not_ERP_tests=16,phase_7B28_lexical_checks_not_ERP_tests=16,phase_7B28_bounded_source_reads_not_semantic_coverage=6,phase_7B28_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only bounded7B28/R4l:797 protected/all329 exact dictionaries/ALLnext_phase/evidence/raw330CRLFprefix/G228/827 originals/3freezes. One Medium local root158 empty max skips ApplyFilter despite complete master. Additive046 source-failure publication chain, not new159: supplied old independent display survives stipulated Fill failure and ordinary selection exports old valid GID. No real failure/partial-fill/provider/DataView/WPF/.NET/calendar/culture/SDK/DTO/ACL/stock/save/financial/production execution, remediation or saved loss. Five existing paths/six reads,whole698C#/561XAML locally,not all callers/reader/fields/477bodies/census/455FE.329 metadata summaries plus selected nearest docs/chains,not all329 bodies. Scope5/5overlap/0new->426/complement401 not coverage percentage or401 C tasks.16FE/INV/32 integrated plans NOT executed;RS14/SP3/HQ6 preserve ancestry/full old input prefixes/all mapped routes/dispositions,not14 approvals.014/132/145 potential and020/021 financial/ACL/stock/save/production barriers unchanged.155/156/157/045/085 not recounted;period/postpone/quoting/return/DTO/health contracts stay open. ALL52 B27 original cases in OWN329/raw330CRLF/indexes/presetB27 child with suite-local A;B26/48,B25/44,B24/44 and all earlier cases preserved. Actual currentCLI B28/versionedB27/API15 separately checked. No protected edits/skips/globalPath/sharedsubprocess mutation/diskoverlay/rebaseline/archive rewrite. Actual33 archive has capture-time checker hashes,not final-wholesale or postpush replay. Reference date,observed clock,source10ba,B27capture6eed and completed delivery-entry436 remain distinct. Local Git pointer reconciled only after802 file blobs matched remote,without changing bytes. B10 additive10vs120/equality1=10/protectedG138 retained.7B/7 partial,R4m/B29 proposed,7C unstarted,8 unauthorized;independent repair start/sync unknown;next_phase8 planning only.')
