#!/usr/bin/env python3
"""Read-only B29/R4m documentary checks, NOT application acceptance.

One root159: accepted invoice search bypasses the existing dirty-editor guard
in sales/purchase, then Navigate clears/replaces the editor before the reader.
Explicit dirty flags/counts, normal CLR completion, fresh result and stipulated
reader outcomes ONLY. No WPF/C#/SQL/SDK/provider/save or measured loss.
Protect829/all330 exact dictionaries/ALLnext_phase/evidence/raw331CRLF/G232/
827 originals/three freezes. ALL48 protected B28 cases use explicit OWN330/
raw331CRLF/indexes/presetB28 child with suite-local A, no skips/global patches/
shared-subprocess mutation/disk overlay/rebaseline/archive rewrite. Seven old
paths/22 slices/zero whole files, NOT all bodies/callers/DTOs/455FE.7B/7partial,
R4n/B30proposed,7Cunstarted,8unauthorized; independent repair start/sync unknown.
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
from validate_search_snapshot_part import historical_record_errors as historical33_errors
ENTRY = 'dda1eafab4188b00a7d6c3e435e7391bd0e09cda'
SNAPSHOT = 'evidence/findings-through-07B28.csv'
SNAPSHOT_SHA = '352c92c6afef478ad16fd1982fc30edf11fbcd112e997d8d9323829ef6d30225'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B28.json'
SHARED_SHA = 'a0f7505dc287ab36cf3244575852a3e81caf2fd940939e3428a2ec08c38494be'
PROVENANCE_SHA = '94ad6f3f434114978f1dbc37ef1ac770334e3e2315f5fa99c956bb6e0be3d6c7'
B28_CHECK_SHA = 'a67d0637e39bffc72b358b97aff3b821b21cf49e64caf874b6c4714d4f5bf46b'
WITNESS_SHA = '43c6254cfaefc07b12bf087affa901820079a8d1157c568b49fa8eed2bb6f0f9'
HISTORICAL_RUN_SHA = '338dfa9ae86a743e33a8656875325474f6e38d19f3d4478deddf1481cd3f9cc6'  # Pin only after exclusive actual34 capture.
SCOPE_FILE = 'review-scope-07B29.csv'
DOCUMENTARY = 'none-documentary-metadata'
NEW_IDS = ['P7-159']
EXTENDED_IDS = []
PART_DOCS = ('PHASE-07B29.md','DIRTY-NAVIGATION-CONTRACTS-07B29.md','VALIDATION-07B29.md',
             'PHASE-07-REMAINING-07B29.md','DATE-IDENTITY-NOTE-07B29.md')
SHARED_DOCS = ('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS = (
 ('dirty-navigation-lineage','DN7B29-',8),('navigation-outcome-lineage','NO7B29-',6),
 ('feature-implementation-matrix','FE7B29-',16),('report-invariants','INV7B29-',16),
 ('acceptance-tests','P7B29T-',32),('report-reconciliation','RC7B29-',6),
 ('root-adjudication','AD7B29-',8),('residual-disposition','RS7B29-',14),('split-register','SP7B29-',3),
 ('handoffs','H7B29-',6),('questions','Q7B29-',6),('remaining-workplan','RW7B29-',10),('continuation-backlog','BK7B29-',10))
SENTINELS = {f'{p}{n:02d}' for p,ns in (('FE7B29-',range(15,17)),('INV7B29-',range(15,17)),
 ('P7B29T-',range(29,33)),('RC7B29-',(5,6)),('AD7B29-',(7,8)),('RS7B29-',range(1,15)),('H7B29-',range(1,7)),('Q7B29-',range(1,7))) for n in ns}
DIRTY_BOUNDARIES = ['own-command-wiring','fresh-chooser-result','accepted-target-result','purchase-consumer',
 'sale-consumer','clear-before-reader','editor-reference-boundary','reader-outcome-boundary']
OUTCOME_BOUNDARIES = ['fresh-not-done','invalid-sentinel','guarded-decline','guarded-allow','clean-control','parent-closing']
DEDUP_DEPTH = 'all330-title-metadata-screen-plus80-path-matched-rows-and-selected-nearest-body-source-chains-not-all-historical-bodies'

@contextmanager
def historical_b28_inputs(v, frozen330, texts, raw):
    """Exact OWN330 input in a context-local path, never a global pathlib patch."""
    if len(frozen330) != 330 or len({r.get('id') for r in frozen330}) != 330:
        raise ValueError('Exactly330 distinct B28 OWN rows required')
    if set(texts) != set(SHARED_DOCS) or any(not isinstance(s, str) for s in texts.values()):
        raise ValueError('Exactly three frozen shared texts required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM frozen bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('Malformed330 frozen registry') from exc
    if (parsed != frozen330 or raw.count(b'\r\n') != 331 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        raise ValueError('330 rows/raw331CRLF disagree')
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
        with historical_b1_inputs(v, frozen330, texts):
            yield
    finally:
        v.AUDIT = original

class HistoricalB28Subprocess:
    """Redirect ONLY the exact protected B28 suite argv; preserve other calls."""
    def __init__(self, backend, python, tool_dir):
        self.backend = backend
        self.expected = [python, '-B', str(tool_dir / 'test_search_snapshot_audit_validator.py')]
        self.actual = [python, '-B', str(tool_dir / 'run_historical_search_snapshot_tests_07B29.py'),
                       '--through-part', 'B28']

    def __getattr__(self, name):
        return getattr(self.backend, name)

    def run(self, args, *pos, **kwargs):
        return self.backend.run(self.actual if args == self.expected else args, *pos, **kwargs)

class HistoricalB28ValidatorView:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)
        object.__setattr__(self, '_subprocess', HistoricalB28Subprocess(
            target.subprocess, target.sys.executable, target.AUDIT / 'tools'))

    def __getattr__(self, name):
        return self._subprocess if name == 'subprocess' else getattr(self._target, name)

    def __setattr__(self, name, value):
        setattr(self._target, name, value)

@contextmanager
def historical_b28_validation(v,report,prior,prov,frozen330):
    ck=v.check
    for name,digest in (('evidence/provenance-07B29.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),
                        (SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B28.json',B28_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B29 immutable entry:'+name)
    ck(prov['historical_artifact_count']==829 and len(frozen330)==330,'B29 protected829/OWN330')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
       and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B29 exact entry identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B29 protected797-to829 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B28.json'));suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='436446091caf82c05ec01817bed5d18b4ea9fb34' and old['findings']['total_open_not_remediated']==330
       and old['original_project_hashes_matching']==827 and old['validation']['errors']==[]
       and old['validation']['current_output_record_pending_first_write_not_placeholder'] is False,'B29 original B28 capture436 not deliverydda')
    ck(len(suites)==29 and sum(s['tests_reported'] for s in suites.values())==886
       and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B29 genuine B28 886/29/797')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
       and prov['genuine_B28_check_sha256']==B28_CHECK_SHA and prov['genuine_B28_check_record_checkout']==old['checkout_head'],'B29 completed pushed B28 entry')
    ck(prov['phase7B28_entry_consistency']==dict(original_hashes_matching=827,findings=330,audit_file_count=834,
       documentary_cases=886,self_test_suites=29,errors=[],erp_runtime_tests_executed=0),'B29 independent entry consistency')
    receipt=prov['entry_actual_subprocess_receipt']
    ck(receipt['entry']==ENTRY and receipt['findings']==330 and receipt['originals']==827 and receipt['cases']==886 and receipt['suites']==29
       and receipt['errors']==[] and type(receipt['process_exit_code']) is int and receipt['process_exit_code']==0
       and receipt['stderr_bytes']==0 and receipt['stdout_sha256']=='afe048aaa6ba95d690eda7ee3420504ca1109ff86ee65c0682f4916e0bb24781','B29 actual fresh entry receipt not old official relabel')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB28ValidatorView(v)
    with historical_b28_inputs(view,frozen330,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    rec=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_search_snapshot_audit_validator.py']
    rec.update(historical_parser_cutoff='B28-not-current-B29-default',all_original_cases_executed_unmodified=True,
       dedicated_child_launcher='tools/run_historical_search_snapshot_tests_07B29.py',actual_subprocess_argv=view.subprocess.actual,
       no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B28-330-not-current-state',
       phase_7B28_historical_input_mode='OWN330-exact331CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B28-test-child',
       phase_7B28_adapter_context=dict(entry_provenance='evidence/provenance-07B29.json',adapter_protected_artifacts_checked=829,
          current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
          B28_parser_assertions_are_historical_preset_not_current_default=True,B28_suite_own_A_uses_context_local_registry_path=True))

def registry_preservation_errors(previous, current, raw, frozen):
    errors = []
    if len(previous) != 330 or current[:330] != previous:
        errors.append('B29 all330 exact fields/ALLnext_phase/evidence')
    if len(current) != 331 or [r.get('id') for r in current[330:]] != NEW_IDS:
        errors.append('B29 only appended159')
    if (type(raw) is not bytes or type(frozen) is not bytes or not raw.startswith(frozen)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n') != 332 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        errors.append('B29 exact330 rawprefix/332CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline=''))) != current:
                errors.append('B29 raw/rows disagree')
        except (UnicodeError, csv.Error):
            errors.append('B29 malformed registry')
    return errors

def group_row_errors(previous, current):
    rows = lambda s: re.findall(r'^\| G-\d{2,3} \|.*$', s, re.M)
    if len(rows(previous)) != 232 or rows(current)[:232] != rows(previous):
        return ['B29 G01..232 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|', current, re.M) != [f'G-{n:02d}' for n in range(1, 237)]:
        return ['B29 only G233..236 exact order']
    return []

def residual_errors(current, upstream):
    if len(current) != 14 or len(upstream) != 14:
        return ['B29 all14 upstream residuals required']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_residual_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/residual-disposition-07B28.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or new.get('upstream_contract_ids') != old.get('upstream_contract_ids')):
            errors.append('B29 residual ancestry/hash/contracts')
        for k in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                  'next_step', 'static_exit_criterion', 'current_handoff_or_split_ids'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B29 residual responsibility:' + k)
        if not new.get('required_redacted_input', '').startswith(old.get('required_redacted_input', '')):
            errors.append('B29 no lost old input')
        mapped = {x.replace('7B28-', '7B29-') for x in old.get('current_handoff_or_split_ids', '').split(';') if x}
        if not mapped <= set(new.get('current_handoff_or_split_ids', '').split(';')):
            errors.append('B29 no lost mapped route')
        if (new.get('disposition') != old.get('disposition')
                or new.get('disposition') not in {'external-handoff', 'split-explicitly', 'assessment-source-bound'}
                or new.get('runtime_status') != 'not-executed'):
            errors.append('B29 no residual approval/runtime overclaim')
    return errors

def split_errors(current, upstream):
    if len(current) != 3 or len(upstream) != 3:
        return ['B29 exactlythree upstream splits']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_split_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/split-register-07B28.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or not new.get('required_input', '').startswith(old.get('required_input', ''))):
            errors.append('B29 split ancestry/no lost input')
        for k in ('title', 'candidate_scope_not_certified', 'reason_for_split', 'owner_role', 'required_input',
                  'next_static_action', 'static_exit_criterion'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B29 split responsibility:' + k)
        if new.get('status') != 'explicit-further-static-split-not-started' or new.get('runtime_status') != 'not-executed':
            errors.append('B29 split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work) != 10:
        return ['B29 fourB/sixC axes']
    expected = (['bounded-parent-contract-delivered-residuals-open'] * 2
                + ['bounded-shared-contract-delivered-residuals-open', 'bounded-R4m-dirty-navigation-delivered-residuals-open']
                + ['planned-not-started'] * 6)
    errors = []
    if [r.get('status') for r in work] != expected or [r.get('part_family') for r in work] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('B29 boundedR4m/sixC unstarted not closure')
    if any(r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false' for r in work):
        errors.append('B29 no runtime/sessions/percent overclaim')
    return errors

def current_link_errors(features,invariants,tests):
    errors=[]
    if (len(features),len(invariants),len(tests))!=(16,16,32):errors.append('B29 FE16/INV16/T32')
    for n,(fe,inv) in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id') or any(inv.get(k)!=fe.get(k) for k in ('finding_ids','evidence','acceptance_ids')):errors.append('B29 FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or ';'.join(t['id'] for t in related)!=fe.get('acceptance_ids'):errors.append('B29 two reverse-linked plans')
        if n<=2:
            root='P7-159'
            if fe.get('finding_ids')!=root or any(t.get('finding_ids')!=root or t.get('plan_kind')!='finding-specific' for t in related):errors.append('B29 first-two-same159 finding-specific plans')
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(fe.get(k),str) or not fe[k].strip():errors.append('B29 capability responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant') for r in invariants})!=16 or len({r.get('acceptance_criterion') for r in tests})!=32:errors.append('B29 distinct substantive invariant/criteria')
    if any(t.get('status')!='not-executed' for t in tests):errors.append('B29 integrated plans never executed')
    return errors

def ledger_errors(dirty,outcomes):
    errors=[]
    observations=(['wired-search-entry-not-permission-proof','fresh-not-done-and-sentinel-explicit','accepted-target-is-not-abandon-decision',
      'purchase-accepted-search-omits-existing-dirty-guard','sale-manifestation-same159-not160','both-Navigate-clear-before-BindingInvoice',
      'editor-ref-replaced-view-cleared-not-all-refs-destroyed','supplied-success-or-null-never-supplies-abandon-approval'],
      ['no-direct-Navigate-on-fresh-not-done','done-with-minus-one-does-not-Navigate','existing-No-blocks-selected-navigation',
       'existing-Yes-allows-reset-not-target-acceptance','clean-guard-needs-no-unsaved-prompt','Closing-guard-is-not-Navigate-interceptor'])
    for data,bounds,obs in zip((dirty,outcomes),(DIRTY_BOUNDARIES,OUTCOME_BOUNDARIES),observations):
        if len(data)!=len(bounds) or [r.get('boundary') for r in data]!=bounds or [r.get('observation') for r in data]!=obs:errors.append('B29 ordered dirty8/outcome6')
        for row in data:
            for k in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(row.get(k),str) or not row[k].strip():errors.append('B29 lineage responsibility:'+k)
            if row.get('runtime_status')!='not-executed':errors.append('B29 no lineage runtime claim')
    return errors


def extension_errors(extensions):
    return [] if type(extensions) is list and extensions==[] else ['B29 no existing-root extension or recount permitted']


def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_SDK_executed','application_remediation_performed',
      'phase7C_started','phase8_authorized_or_started','all_callers_or_external_DTOs_body_reviewed','actual_WPF_event_order_or_count_claimed',
      'dirty_flag_propagation_or_constructor_defaults_assumed','provider_failure_observed','database_commit_or_saved_loss_claimed','external_references_or_GC_modeled'):
        if w.get(k) is not False:errors.append('B29 false-only boundary:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:errors.append('B29 integer-zero boundary:'+k)
    for k in ('B_R4m_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained','selected_paths_strict_utf8_decode','prior015_046_061_091_132_148_151_155_158_not_recounted'):
        if w.get(k) is not True:errors.append('B29 true-only boundary:'+k)
    for k,n in (('illustration_count',16),('lexical_check_count',16),('selected_source_paths',7),('whole_local_files_selected',0),('source_read_slice_count',22)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B29 exact count:'+k)
    e=w.get('retained_additive_B10_arithmetic_erratum',{})
    if (e!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)
        or any(type(e.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or e.get('protected_G138_not_rewritten') is not True):errors.append('B29 retained B10 additive correction')
    if w.get('audit_reference_date_utc')!='2026-11-16' or w.get('entry_checkout')!=ENTRY:errors.append('B29 session-date/entry identity')
    if w.get('new_root_ids')!=NEW_IDS or w.get('extended_existing_root_ids')!=[] or len(w.get('unadjudicated_source_leads_not_additional_findings',[]))!=4:errors.append('B29 only159/no extension boundary')
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16' or not isinstance(prov.get('environment_clock_observed_utc'),str):errors.append('B29 session-date/raw-clock fields')
    for token in ('2026-11-16',prov.get('environment_clock_observed_utc','MISSING'),ENTRY,'436446091caf82c05ec01817bed5d18b4ea9fb34',B28_CHECK_SHA,'249546','829','330','834',WITNESS_SHA):
        if token not in note:errors.append('B29 additive identity:'+token)
    if prov.get('genuine_B28_check_record_checkout')==ENTRY:errors.append('B29 official capture is not delivery')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=34 or len(modes)!=34:return ['B29 exactly34 actual OWN modes required']
    errors=historical33_errors(dict(historical_mode_count=33,historical_modes=modes[:33],errors=h.get('errors')))
    last=modes[-1]
    expected=dict(mode='B28',findings_total=330,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],
       original_project_hashes_matching=827,audit_checker_self_test_cases_reported=886,audit_checker_self_test_suite_count=29,
       erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0)
    for k,value in expected.items():
        if last.get(k)!=value or type(last.get(k)) is not type(value):errors.append('B29 B28 OWN330/886/29:'+k)
    child=last.get('historical_B28_child') or {}
    expected=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',historical_parser_cutoff='B28-not-current-B29-default',
       all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_search_snapshot_tests_07B29.py',
       no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    for k,value in expected.items():
        if child.get(k)!=value or type(child.get(k)) is not type(value):errors.append('B29 B28 ALL48 child:'+k)
    if not isinstance(last.get('stdout_sha256'),str) or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:errors.append('B29 actual stdout identity')
    return errors


def capture_source_errors(history,source_bytes):
    """A single later pin is reversible in memory; NEVER replace capture hashes."""
    expected=history.get('checker_sources_at_capture',{});errors=[]
    if set(expected)!=set(source_bytes):return ['B29 capture-tool set changed']
    own='tools/validate_dirty_navigation_part.py'
    for name,raw in source_bytes.items():
        if name==own:
            line="HISTORICAL_RUN_SHA = '"+str(HISTORICAL_RUN_SHA)+"'  # Pin only after exclusive actual34 capture."
            target='HISTORICAL_RUN_SHA = None  # Pin only after exclusive actual34 capture.'
            text=raw.decode('utf8')
            if HISTORICAL_RUN_SHA is None or text.count(line)!=1:
                errors.append('B29 exact-one final capture pin required');continue
            raw=text.replace(line,target).encode('utf8')
        if hashlib.sha256(raw).hexdigest()!=expected[name]:errors.append('B29 changed capture-tool beyond documented single pin:'+name)
    return errors

def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == DOCUMENTARY:
        v.check(row['id'] in SENTINELS, 'B29 undeclared documentary sentinel:' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B29 fabricated source for documentary gate:' + row['id'])
        v.evidence(row['evidence'], row['id'])
        try:
            expanded = expanded_source_evidence(row['evidence'])
        except ValueError as exc:
            v.check(False, 'B29 invalid source ' + row['id'] + ':' + str(exc))
            return
        v.scoped_evidence(expanded, scope, row['id'] + ' boundedB29', phase=7)

def extend_dirty_navigation(v,report,prov,frozen330):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[330:]
    for error in registry_preservation_errors(frozen330,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id'] for r in current})==331,'B29 distinct331 IDs');v.distributions(new,dict(Medium=1),dict(confirmed=1),'B29 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B29 finding state is not permission')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B29 exact registry/report title')
    lookup={r['id']:r for r in current}
    for n in ('P4-014','P7-132','P7-145'):ck(lookup[n]['certainty']=='potential','B29 retained potential:'+n)
    for k in ('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k] is False,'B29 no implicit start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B29 no repair merge')
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B29 no ERP/SQL:'+k)
    for error in date_identity_errors(prov,v.read(v.AUDIT/'DATE-IDENTITY-NOTE-07B29.md')):ck(False,error)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==7,'B29 seven bounded old paths')
    for r in selected:
        ck(r['path'] in original and r['review_state']=='bounded-static-command-reference-reader-slices-not-whole-files-or-runtime' and bool(r['focus']),'B29 bounded scope identity')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    ext=rows('evidence/historical-extensions-07B29.csv')
    for error in extension_errors(ext):ck(False,error)
    ck(lookup['P7-046']==next(r for r in frozen330 if r['id']=='P7-046') and lookup['P7-158']==frozen330[-1],'B29 B28 roots/extension preserved, not recounted')
    known={r['id'] for r in current}|{f'H7B29-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B29.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str) and x.strip() for x in r.values()),'B29 completeCSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B29 no runtime:'+r['id'])
    fe,inv,tests=[tables[x] for x in ('FE7B29-','INV7B29-','P7B29T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['DN7B29-'],tables['NO7B29-']):ck(False,error)
    ck(fe[0]['status']==fe[1]['status']=='confirmed-source-local','B29 two manifestations one159')
    v.proposed_tests(tests,'7B29');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['DN7B29-']+tables['NO7B29-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B29 '+label)
    for r in tables['RC7B29-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ck(r['finding_ids']==unique('finding_ids') and r['acceptance_ids']==unique('acceptance_ids') and r['evidence']==source_evidence_union(fs),'B29 expanded-before-dedup RC lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B29-'],rows('evidence/residual-disposition-07B28.csv'))+split_errors(tables['SP7B29-'],rows('evidence/split-register-07B28.csv'))+remaining_work_errors(tables['RW7B29-']):ck(False,error)
    hids={r['id'] for r in tables['H7B29-']};sids={r['id'] for r in tables['SP7B29-']}
    v.related(tables['RS7B29-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B29-'],hids,'handoff_ids')
    for r in tables['H7B29-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B29 no invented approval')
    for r in tables['Q7B29-']:ck(r['status']=='unanswered-no-secrets-requested','B29 no invented answer')
    for n,r in enumerate(tables['BK7B29-'],1):ck(r['prior_backlog_id']==f'BK7B28-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B29 backlog ancestry/uncompleted')
    ck([r['status'] for r in tables['BK7B29-'][2:6]]==['not-started']*4,'B29 C axes unstarted')
    ad=tables['AD7B29-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B29 only one159')
    ck(not any(r['decision']=='extended-existing-root-not-new' for r in ad),'B29 no historical root extended')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B29 honest dedup depth')
    ck(set(new[0]['evidence'].split(';'))<=set(ad[0]['evidence'].split(';')),'B29 adjudicated new source chain')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,29)]
    before={r['path'] for n in prior_names for r in rows(n)};paths=set(scope);rem=original.keys()-(before|paths)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(bk==dict(selected_paths=7,prior_union=426,overlap=7,new=0,union=426,complement=401,complement_kinds={'source':336,'generated-artifact':61,'project-or-resource':4}),'B29 counts are bookkeeping not percentages')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B29.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B28.md','evidence/split-register-07B28.csv','evidence/residual-disposition-07B28.csv'] and decision['selected_upstream_split']=='SP7B28-01' and decision['entry']==ENTRY and decision['bookkeeping']==bk,'B29 bounded authority')
    ck(set(decision['new_paths'])==paths-before and decision['historical_metadata_screen_count']==330 and decision['path_matched_metadata_rows']==80 and decision['historical_body_review_claim'] is False and decision['historical_comparison_depth']==DEDUP_DEPTH,'B29 metadata not whole-body review')
    ck(decision['bounded_read_slice_count']==22 and decision['whole_local_files']==0 and decision['one_new_root']==NEW_IDS and decision['existing_root_extensions']==[],'B29 bounded22/whole0/root1/ext0')
    for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k] is False,'B29 scope permission:'+k)
    wp='evidence/dirty-navigation-witnesses-07B29.json';ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B29 immutable witness stdout')
    witness,match=v.recompute(wp,'tools/check_dirty_navigation_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B29 successful inert/lexical observations')
    for key,prefix,flag in (('illustrations','ALG7B29-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B29-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,16);v.related(data,known)
        for r in data:ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B29 inert witness boundary');validate_source(v,r,scope)
    reads=witness['bounded_source_reads_not_semantic_coverage'];ck(len(reads)==22 and {r['path'] for r in reads}==paths,'B29 exactly22 reads seven paths')
    ck(all(r['whole_local_file_selected'] is False for r in reads),'B29 no whole-file claim')
    for r in reads:
        ck(r['encoding']=='strict-utf-8' and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True and v.sha(v.ROOT/r['path'])==r['sha256'],'B29 source hash/depth')
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B29 source read',phase=7)
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
            if target==(v.AUDIT/'evidence/checks-07B29.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B29 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B29.md','PHASE-07-REMAINING-07B29.md','7B30','غير مأذونة','dda1eaf','10ba215')),'B29 shared current boundary:'+name)
    hp='evidence/historical-mode-verification-07B29-release.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B29 actual34 captured')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B29 actual34 archive identity');history=v.json.loads(v.read(v.AUDIT/hp))
        for error in historical_record_errors(history):ck(False,error)
        ck(history['checkout_head']==ENTRY and history['source_head']==v.HEAD and history['branch']==v.BRANCH,'B29 historical capture entry/source')
        sources={p.relative_to(v.AUDIT).as_posix():p.read_bytes() for p in sorted((v.AUDIT/'tools').glob('*.py'))}
        for error in capture_source_errors(history,sources):ck(False,error)
        report['phase_7B29_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=34,all_documentary_exit_codes_zero=True,B28_OWN330_raw331CRLF_and_historical48_child=True,B27_ALL52_B26_ALL48_B25_ALL44_B24_ALL44_retained=True,null_means_unreported_not_zero=True,capture_tool_count=len(sources),only_later_single_pin_reversible_in_memory=True,not_final_or_postpush_wholesale_replay=True)
    tools=['check_dirty_navigation_witnesses.py','validate_dirty_navigation_part.py','run_historical_search_snapshot_tests_07B29.py','test_dirty_navigation_audit_validator.py']
    for n in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/n),filename=n)
        except SyntaxError as exc:ck(False,'B29 audit-tool syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==48
    ck(passed,'B29 48 documentary cases/count: '+(run.stderr[-8000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=48,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B29-331-bounded-R4m-dirty-navigation-not7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,30))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B30-proposed-R4n-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=159,phase_7B29=1,total_open_not_remediated=331,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:7,'phase_7B29_prior_union':426,'phase_7B29_overlap_with_prior_union':7,'phase_7B29_new_paths':0,'unique_union_not_line_or_execution_coverage':426,'inventory_only_no_selected_scope':401})
    report['phase_7B28_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_evidence_artifacts_hash_checked=829,historical_check_record_overwritten=False,genuine_B28_stdout_sha256_unchanged=B28_CHECK_SHA,all330_dictionaries_ALLnext_phase_evidence_rawprefix_preserved=True)
    report['phase_7B29_dirty_navigation_trace_limits']=dict(dirty_navigation_boundaries=8,navigation_outcome_boundaries=6,bounded_source_reads=22,selected_paths=7,new_union_paths=0,whole_local_files=0,current_features_or_documentary_contracts=16,invariants_not_executed_tests=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_further_static_splits=3,new_root_ids=NEW_IDS,existing_root_extensions=ext,B_R4m_delivered_not_whole_SP01_R4_or7B_closure=True,retained_potential_roots=['P4-014','P7-132','P7-145'],supplied_dirty_flags_and_normal_CLR_completion_not_DTO_defaults=True,accepted_target_not_abandon_decision=True,reader_success_or_null_only_supplied_not_provider_observed=True,database_commit_or_saved_loss_claimed=False,all_callers_or_external_DTOs_body_reviewed=False,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synchronized_not_asserted=True)
    report['evidence_rows'].update(phase_7B29_illustrations_not_ERP_tests=16,phase_7B29_lexical_checks_not_ERP_tests=16,phase_7B29_bounded_source_reads_not_semantic_coverage=22,phase_7B29_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only bounded7B29/R4m:829protected/all330exact dictionaries/ALLnext_phase/evidence/raw331CRLFprefix/G232/827 originals/3freezes. One Medium confirmed-source-local root159: accepted invoice search in purchase/sale omits existing CheckBeforeClear then Navigate replaces/clears editor before BindingInvoice. Explicit supplied dirty flags/UI-count and normal CLR completion; fresh not-done/sentinel/guardNo/Yes/clean controls; old editor no longer current is not GC/all-references/saved loss. Reader success-header/null outcomes are stipulated, not actual provider/SQL or full hydration/render/save acceptance. Closing guard is not assumed an interceptor for Navigate;no WPF event order/count/placeholder/dirty propagation/DTO constructor defaults inferred. Seven existing paths/22 bounded slices/whole0,not all callers/reader/fields/477bodies/census455FE.330metadata screen/80pathmatches plus selected nearest bodies/chains,not all330bodies.7/7overlap/0new->426/complement401 not percent or401Ctasks.16FE/INV/32integrated plans NOT executed;RS14/SP3/HQ6 preserve ancestry/fulloldinputprefix/allmappedroutes/dispositions,not14approvals.014/132/145potential and020/021financial/ACL/stock/save/production barriers unchanged.015/046/061/091/148/151/155–158notrecounted;no root160 or new046extension. Other callers/writers/fields/Product/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome,census,SDK/currency/precision/templates remain7B. ALL48originalB28 cases via OWN330/raw331CRLF/indexes/presetB28 child with suite-localA;52B27/48B26/44B25/44B24 and earlier preserved. Actual currentCLI B29/versionedB28/API15 separately checked. No protected edits/skips/globalPath/sharedsubprocess mutation/diskoverlay/rebaseline/archive rewrite. Actual34 archive has capture-time hashes;onlysingle later pin inverted in memory,not final/postpush wholesale replay. Session reference2026-11-16 and raw observed environment clock distinct;application source10ba/officialB28capture436/deliveredB28entrydda/freshentryrun not relabelled. B10additive10vs120/equality1=10/G138 retained.7B/7partial,R4n/B30proposed,7Cunstarted,8unauthorized;repair start/syncunknown;next_phase8planningonly.')
