#!/usr/bin/env python3
"""B27/R4k read-only documentary checks; NEVER invoice/ERP acceptance.

Protect765 artifacts/all326 exact dictionaries/ALLnext_phase/evidence/
raw327CRLFprefix/G223/827 originals/3freezes. ALL48 protected B26 cases use
OWN326/raw327CRLF/indexes/presetB26 with suite-local A in a separate child;
B25/44 and B24/44 stay separately versioned. No protected edits/skips/global
Path/shared subprocess mutation/disk overlay/rebaseline/archive rewrite.
155 fixed server process vs local selection;156 caller status predicate lost
by date/reset;157 unconditional20 in purchase query and consumer no type check.
GlobalID retained, not061 identity loss. Source predicates and selected fields,
not WPF/DataView/SQL/SDK/provider/ACL/stock/save/calendar/financial execution.
Whole local698C#/561XAML search plus11 reads7paths not all callers/DTOs/477bodies
or455FE/capability census.7B/7 partial,R4l/B28 proposed,7C unstarted,8 unauthorized;
independent repair start/synchronization unknown, next_phase8 planning only.
"""
from __future__ import annotations
import collections
from contextlib import contextmanager
import csv
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from validate_financial_report_part import historical_b1_inputs, bidirectional_errors
from validate_contract_item_part import row_sha, expanded_source_evidence
from validate_property_dialog_part import source_evidence_union
from validate_bulk_product_part import historical_record_errors as historical31_errors

ENTRY = '6eedc0640e3432c14ca0875b7f1c7806ea1e3f64'
SNAPSHOT = 'evidence/findings-through-07B26.csv'
SNAPSHOT_SHA = '0ea4b60648757a98bd602049f22cb82900d0c1d28a2f7674a9e47e04c50ccb81'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B26.json'
SHARED_SHA = 'eed5196df7fb8315640e70ae130bb3d2f6afd56cf49e4829d788573bf8eb2d27'
PROVENANCE_SHA = '4d409375f70407e6f0844bc891a3488a868e663cb9a25ae4767451299edac61d'
B26_CHECK_SHA = 'f80ef7936aca23c3667d44c48821a66dc1704203598ce1ea0bd9ed687edd5895'
WITNESS_SHA = 'bd7ac7a05efd39e44263ef155fcd216555d272c534fe7b098e75e5bbde1d4dd1'
FAILED_WITNESS_SHA = 'bc1a4e4f62d634fe6154af71405063b54976b92f8530bb7583033462194b0009'
HISTORICAL_RUN_SHA = '39c0706f8b13a61a9385f0c9595889141f67846e88b48c43b9116ab58dbd5392'  # Actual32 capture; source hashes are capture-time, not post-pin replay.
SCOPE_FILE = 'review-scope-07B27.csv'
DOCUMENTARY = 'none-documentary-metadata'
NEW_IDS = ['P7-155', 'P7-156', 'P7-157']
PART_DOCS = ('PHASE-07B27.md', 'INVOICE-SEARCH-CONTRACTS-07B27.md',
             'VALIDATION-07B27.md', 'PHASE-07-REMAINING-07B27.md', 'DATE-IDENTITY-NOTE-07B27.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
TABLE_SPECS = (
    ('search-criteria-lineage', 'SC7B27-', 8), ('document-selection-lineage', 'DS7B27-', 8),
    ('feature-implementation-matrix', 'FE7B27-', 18), ('report-invariants', 'INV7B27-', 18),
    ('acceptance-tests', 'P7B27T-', 36), ('report-reconciliation', 'RC7B27-', 6),
    ('root-adjudication', 'AD7B27-', 9), ('residual-disposition', 'RS7B27-', 14),
    ('split-register', 'SP7B27-', 3), ('handoffs', 'H7B27-', 6), ('questions', 'Q7B27-', 6),
    ('remaining-workplan', 'RW7B27-', 10), ('continuation-backlog', 'BK7B27-', 10),
)
SENTINELS = {f'{p}{n:02d}' for p, ns in (
    ('FE7B27-', range(17,19)), ('INV7B27-', range(17,19)), ('P7B27T-', range(33,37)),
    ('AD7B27-', (8,9)), ('RS7B27-', range(1,15)), ('H7B27-', range(1,7)),
    ('Q7B27-', range(1,7))) for n in ns}
CRITERIA_BOUNDARIES = ['caller-fixed-request','SQL-fixed-proc','local-proc-view','caller-eligibility',
                       'date-replacement','reset-condition','type-disjunction','query-health-leads']
SELECTION_BOUNDARIES = ['typed-kind-branch-contract','projection-globalid-retained','selection-return-surface',
    'purchase-caller-scope','purchase-reader-consumer','receive-consumer-eligibility',
    'canonical-navigation-control','documentref-followup-contract']
DEDUP_DEPTH = 'all326-title-certainty-summaries-plus-path-filtered-metadata-and-selected-nearest-doc-bodies-source-chains-not-all-historical-bodies'

@contextmanager
def historical_b26_inputs(v, frozen326, texts, raw):
    """Exact OWN326 input in a context-local path, never a global pathlib patch."""
    if len(frozen326) != 326 or len({r.get('id') for r in frozen326}) != 326:
        raise ValueError('Exactly326 distinct B26 OWN rows required')
    if set(texts) != set(SHARED_DOCS) or any(not isinstance(s, str) for s in texts.values()):
        raise ValueError('Exactly three frozen shared texts required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM frozen bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('Malformed326 frozen registry') from exc
    if (parsed != frozen326 or raw.count(b'\r\n') != 327 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        raise ValueError('326 rows/raw327CRLF disagree')
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
        with historical_b1_inputs(v, frozen326, texts):
            yield
    finally:
        v.AUDIT = original

class HistoricalB26Subprocess:
    """Redirect ONLY the exact protected B26 suite argv; preserve other calls."""
    def __init__(self, backend, python, tool_dir):
        self.backend = backend
        self.expected = [python, '-B', str(tool_dir / 'test_bulk_product_audit_validator.py')]
        self.actual = [python, '-B', str(tool_dir / 'run_historical_bulk_product_tests_07B27.py'),
                       '--through-part', 'B26']

    def __getattr__(self, name):
        return getattr(self.backend, name)

    def run(self, args, *pos, **kwargs):
        return self.backend.run(self.actual if args == self.expected else args, *pos, **kwargs)

class HistoricalB26ValidatorView:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)
        object.__setattr__(self, '_subprocess', HistoricalB26Subprocess(
            target.subprocess, target.sys.executable, target.AUDIT / 'tools'))

    def __getattr__(self, name):
        return self._subprocess if name == 'subprocess' else getattr(self._target, name)

    def __setattr__(self, name, value):
        setattr(self._target, name, value)

@contextmanager
def historical_b26_validation(v, report, prior, prov, frozen326):
    ck = v.check
    for name, digest in (('evidence/provenance-07B27.json', PROVENANCE_SHA), (SNAPSHOT,SNAPSHOT_SHA),
                         (SHARED_SNAPSHOT,SHARED_SHA), ('evidence/checks-07B26.json',B26_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B27 immutable entry:'+name)
    ck(prov['historical_artifact_count']==765 and len(frozen326)==326,'B27 entry765/326')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
       and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,
       'B27 frozen entry identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),
       'B27 protected734-to765 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B26.json'))
    suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='dd38f97e844dc60ea64ae00fa40ef588e49752d7'
       and old['findings']['total_open_not_remediated']==326 and old['original_project_hashes_matching']==827
       and old['validation']['errors']==[] and old['validation']['current_output_record_pending_first_write_not_placeholder'] is False,
       'B27 genuine B26 capturedd38f97 not delivery-entry6eedc06')
    ck(len(suites)==27 and sum(s['tests_reported'] for s in suites.values())==786
       and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B27 B26 actual786/27/734')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
       and prov['genuine_B26_check_sha256']==B26_CHECK_SHA
       and prov['genuine_B26_check_record_checkout']==old['checkout_head'],'B27 completed pushed B26 entry')
    ck(prov['phase7B26_entry_consistency']==dict(original_hashes_matching=827,findings=326,audit_file_count=770,
       documentary_cases=786,self_test_suites=27,errors=[],erp_runtime_tests_executed=0),'B27 independent entry consistency')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    view=HistoricalB26ValidatorView(v)
    with historical_b26_inputs(view,frozen326,texts,(v.AUDIT/SNAPSHOT).read_bytes()):
        yield view
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_bulk_product_audit_validator.py']
    record.update(historical_parser_cutoff='B26-not-current-B27-default',all_original_cases_executed_unmodified=True,
        dedicated_child_launcher='tools/run_historical_bulk_product_tests_07B27.py',actual_subprocess_argv=view.subprocess.actual,
        no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B26-326-not-current-state',
        phase_7B26_historical_input_mode='OWN326-exact327CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B26-test-child',
        phase_7B26_adapter_context=dict(entry_provenance='evidence/provenance-07B27.json',adapter_protected_artifacts_checked=765,
            current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
            B26_parser_assertions_are_historical_preset_not_current_default=True,B26_suite_own_A_uses_context_local_registry_path=True))


def registry_preservation_errors(previous, current, raw, frozen):
    errors = []
    if len(previous) != 326 or current[:326] != previous:
        errors.append('B27 all326 exact fields/ALLnext_phase/evidence')
    if len(current) != 329 or [r.get('id') for r in current[326:]] != NEW_IDS:
        errors.append('B27 only appended155/156/157')
    if (type(raw) is not bytes or type(frozen) is not bytes or not raw.startswith(frozen)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n') != 330 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        errors.append('B27 exact326 rawprefix/330CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline=''))) != current:
                errors.append('B27 raw/rows disagree')
        except (UnicodeError, csv.Error):
            errors.append('B27 malformed registry')
    return errors

def group_row_errors(previous, current):
    rows = lambda s: re.findall(r'^\| G-\d{2,3} \|.*$', s, re.M)
    if len(rows(previous)) != 223 or rows(current)[:223] != rows(previous):
        return ['B27 G01..223 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|', current, re.M) != [f'G-{n:02d}' for n in range(1, 229)]:
        return ['B27 only G224..228 exact order']
    return []

def ledger_errors(criteria, selection):
    errors=[]
    expected_obs=(
      ['selected-transfer-caller-not-census','server-proc-not-selected-combo','local-filter-cannot-broaden-source',
       'literal-status1-required-not-status-policy','date-replaces-not-conjoins-caller-condition',
       'reset-drops-mandatory-caller-predicate','unconditional20-not-universal-allowed-set',
       'period-postpone-quoting-health-leads-not-extra-roots'],
      ['requested1-admits20-before-selection','globalid-retained-not061-local-number-loss',
       'ISDone-GID-proc-pay-not-eligibility-certificate','purchase1-consumer-GID-branch-no-type-recheck',
       'reader-maps-source-type-not-request-type','consumer-does-not-restore-status1',
       'canonical-navigation-type-proc-branch-positive-control','unresolved-DocumentRef-allowedset-dirty-cancel-contract'])
    for data,boundaries,observations,label in zip((criteria,selection),(CRITERIA_BOUNDARIES,SELECTION_BOUNDARIES),expected_obs,('criteria','selection')):
        if len(data)!=8 or [r.get('boundary') for r in data]!=boundaries:
            errors.append('B27 ordered boundaries:'+label)
        if [r.get('observation') for r in data]!=observations:
            errors.append('B27 exact proc/eligibility/type/GID/lead limits:'+label)
        for row in data:
            for key in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(row.get(key),str) or not row[key].strip():
                    errors.append('B27 '+label+' responsibility:'+key)
            if row.get('runtime_status')!='not-executed':errors.append('B27 '+label+' runtime overclaim')
    return errors


def current_link_errors(features, invariants, tests):
    errors = []
    if (len(features), len(invariants), len(tests)) != (18, 18, 36):
        errors.append('B27 FE18/INV18/T36')
    for n, (fe, inv) in enumerate(zip(features, invariants), 1):
        if inv.get('feature_ids') != fe.get('id') or any(inv.get(k) != fe.get(k)
                for k in ('finding_ids', 'evidence', 'acceptance_ids')):
            errors.append('B27 exact FE/INV lineage')
        related = [t for t in tests if t.get('feature_ids') == fe.get('id')]
        if len(related) != 2 or ';'.join(t['id'] for t in related) != fe.get('acceptance_ids'):
            errors.append('B27 two reverse-linked plans per capability')
        if n <= 3 and (fe.get('finding_ids') != NEW_IDS[n - 1]
                or any(t.get('plan_kind') != 'finding-specific' or t.get('finding_ids') != NEW_IDS[n - 1]
                       for t in related)):
            errors.append('B27 three distinct finding-specific plans')
        for k in ('owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step', 'limit'):
            if not isinstance(fe.get(k), str) or not fe[k].strip():
                errors.append('B27 capability responsibility:' + k)
    errors += bidirectional_errors(features, tests, 'feature_ids') + bidirectional_errors(invariants, tests, 'invariant_ids')
    if len({r.get('required_invariant') for r in invariants}) != 18 or len({r.get('acceptance_criterion') for r in tests}) != 36:
        errors.append('B27 distinct substantive invariants/criteria')
    if any(r.get('status') != 'not-executed' for r in tests):
        errors.append('B27 acceptance never executed')
    return errors

def residual_errors(current, upstream):
    if len(current) != 14 or len(upstream) != 14:
        return ['B27 all14 upstream residuals required']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_residual_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/residual-disposition-07B26.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or new.get('upstream_contract_ids') != old.get('upstream_contract_ids')):
            errors.append('B27 residual ancestry/hash/contracts')
        for k in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                  'next_step', 'static_exit_criterion', 'current_handoff_or_split_ids'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B27 residual responsibility:' + k)
        if not new.get('required_redacted_input', '').startswith(old.get('required_redacted_input', '')):
            errors.append('B27 no lost old input')
        mapped = {x.replace('7B26-', '7B27-') for x in old.get('current_handoff_or_split_ids', '').split(';') if x}
        if not mapped <= set(new.get('current_handoff_or_split_ids', '').split(';')):
            errors.append('B27 no lost mapped route')
        if (new.get('disposition') != old.get('disposition')
                or new.get('disposition') not in {'external-handoff', 'split-explicitly', 'assessment-source-bound'}
                or new.get('runtime_status') != 'not-executed'):
            errors.append('B27 no residual approval/runtime overclaim')
    return errors

def split_errors(current, upstream):
    if len(current) != 3 or len(upstream) != 3:
        return ['B27 exactlythree upstream splits']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_split_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/split-register-07B26.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or not new.get('required_input', '').startswith(old.get('required_input', ''))):
            errors.append('B27 split ancestry/no lost input')
        for k in ('title', 'candidate_scope_not_certified', 'reason_for_split', 'owner_role', 'required_input',
                  'next_static_action', 'static_exit_criterion'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B27 split responsibility:' + k)
        if new.get('status') != 'explicit-further-static-split-not-started' or new.get('runtime_status') != 'not-executed':
            errors.append('B27 split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work) != 10:
        return ['B27 fourB/sixC axes']
    expected = (['bounded-parent-contract-delivered-residuals-open'] * 2
                + ['bounded-shared-contract-delivered-residuals-open', 'bounded-R4k-invoice-search-delivered-residuals-open']
                + ['planned-not-started'] * 6)
    errors = []
    if [r.get('status') for r in work] != expected or [r.get('part_family') for r in work] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('B27 boundedR4k/sixC unstarted not closure')
    if any(r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false' for r in work):
        errors.append('B27 no runtime/sessions/percent overclaim')
    return errors

def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_DataView_executed','application_remediation_performed',
              'phase7C_started','phase8_authorized_or_started','all_callers_or_external_DTOs_body_reviewed',
              'actual_WPF_event_order_or_count_claimed','financial_or_status_policy_invented',
              'external_DTO_constructor_defaults_assumed','database_commit_or_saved_loss_claimed'):
        if w.get(k) is not False:errors.append('B27 false-only boundary:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:errors.append('B27 integer-zero boundary:'+k)
    for k in ('B_R4k_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained',
              'selected_paths_strict_utf8_decode','prior045_061_073_074_120_132_not_recounted_or_extended'):
        if w.get(k) is not True:errors.append('B27 true-only boundary:'+k)
    for k,n in (('illustration_count',20),('lexical_check_count',20),('selected_source_paths',7),
                ('whole_local_search_files_selected',2),('source_read_slice_count',11)):
        if type(w.get(k)) is not int or w[k]!=n:errors.append('B27 exact witness count:'+k)
    e=w.get('retained_additive_B10_arithmetic_erratum',{})
    if (e!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)
        or any(type(e.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control'))
        or e.get('protected_G138_not_rewritten') is not True):errors.append('B27 retained B10 identity')
    if w.get('audit_reference_date_utc')!='2026-11-16' or w.get('entry_checkout')!=ENTRY:errors.append('B27 reference/entry identity')
    if len(w.get('unadjudicated_source_leads_not_additional_findings',[]))!=4:errors.append('B27 explicit unadjudicated leads')
    return errors


def date_identity_errors(prov,note):
    errors=[]
    if (prov.get('audit_reference_date_utc')!='2026-11-16'
        or prov.get('environment_clock_observed_utc')!='2026-11-20T01:15:07.156974+00:00'):
        errors.append('B27 reference16 and observed20 separate')
    for t in ('2026-11-16','2026-11-20',ENTRY,'dd38f97e844dc60ea64ae00fa40ef588e49752d7',B26_CHECK_SHA,'228846','765','326','770',WITNESS_SHA,FAILED_WITNESS_SHA):
        if t not in note:errors.append('B27 additive capture identity:'+t)
    if prov.get('genuine_B26_check_record_checkout')==ENTRY:errors.append('B27 capture cannot be relabelled delivery')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=32 or len(modes)!=32:
        return ['B27 exactly32 actual OWN modes required']
    errors=historical31_errors(dict(historical_mode_count=31,historical_modes=modes[:31],errors=h.get('errors')))
    last=modes[-1]
    expected=dict(mode='B26',findings_total=326,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],
        original_project_hashes_matching=827,audit_checker_self_test_cases_reported=786,audit_checker_self_test_suite_count=27,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0)
    for k,val in expected.items():
        if last.get(k)!=val or type(last.get(k)) is not type(val):errors.append('B27 B26 OWN326/786/27:'+k)
    child=last.get('historical_B26_child') or {}
    expected=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',
        historical_parser_cutoff='B26-not-current-B27-default',all_original_cases_executed_unmodified=True,
        dedicated_child_launcher='tools/run_historical_bulk_product_tests_07B27.py',
        no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    for k,val in expected.items():
        if child.get(k)!=val or type(child.get(k)) is not type(val):errors.append('B27 B26 ALL48 explicit child:'+k)
    if not isinstance(last.get('stdout_sha256'),str) or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:
        errors.append('B27 historical stdout identity')
    return errors


def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == DOCUMENTARY:
        v.check(row['id'] in SENTINELS, 'B27 undeclared documentary sentinel:' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B27 fabricated source for documentary gate:' + row['id'])
        v.evidence(row['evidence'], row['id'])
        try:
            expanded = expanded_source_evidence(row['evidence'])
        except ValueError as exc:
            v.check(False, 'B27 invalid source ' + row['id'] + ':' + str(exc))
            return
        v.scoped_evidence(expanded, scope, row['id'] + ' boundedB27', phase=7)

def extend_invoice_search(v,report,prov,frozen326):
    ck,rows=v.check,v.rows
    current=rows('findings.csv');new=current[326:]
    for e in registry_preservation_errors(frozen326,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,e)
    ck(len({r['id'] for r in current})==329,'B27 distinct329 IDs')
    ck(rows('evidence/historical-extensions-07B27.csv')==[],'B27 zero historical extensions')
    v.distributions(new,dict(Medium=3),dict(confirmed=3),'B27 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B27 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B27 heading/registry exact')
    lookup={r['id']:r for r in current}
    for n in ('P4-014','P7-132','P7-145'):ck(lookup[n]['certainty']=='potential','B27 retained potential:'+n)
    for k in ('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k] is False,'B27 no implicit start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True,'B27 no repair-to-audit merge')
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k]) is int and prov[k]==0,'B27 no ERP/SQL:'+k)
    for e in date_identity_errors(prov,v.read(v.AUDIT/'DATE-IDENTITY-NOTE-07B27.md')):ck(False,e)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==7,'B27 seven bounded paths')
    for r in selected:
        ck(r['path'] in original and r['review_state']=='whole-local-invoice-search-or-selected-caller-reader-static-slices-not-runtime-certified' and bool(r['focus']),'B27 scope identity/depth')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id'] for r in current}|{f'H7B27-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B27.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str) and x.strip() for x in r.values()),'B27 incompleteCSV:'+r['id']);validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B27 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x] for x in ('FE7B27-','INV7B27-','P7B27T-')]
    for e in current_link_errors(fe,inv,tests)+ledger_errors(tables['SC7B27-'],tables['DS7B27-']):ck(False,e)
    ck(all(f['status']=='confirmed-source-local' for f in fe[:3]),'B27 three local causes only')
    v.proposed_tests(tests,'7B27');fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids')
    v.related(tables['SC7B27-']+tables['DS7B27-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B27 '+label)
    for r in tables['RC7B27-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')];uniq=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ck(r['finding_ids']==uniq('finding_ids') and r['acceptance_ids']==uniq('acceptance_ids') and r['evidence']==source_evidence_union(fs),'B27 expanded-before-dedup RC lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for e in residual_errors(tables['RS7B27-'],rows('evidence/residual-disposition-07B26.csv'))+split_errors(tables['SP7B27-'],rows('evidence/split-register-07B26.csv'))+remaining_work_errors(tables['RW7B27-']):ck(False,e)
    hids={r['id'] for r in tables['H7B27-']};sids={r['id'] for r in tables['SP7B27-']}
    v.related(tables['RS7B27-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B27-'],hids,'handoff_ids')
    for r in tables['H7B27-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B27 no invented approval')
    for r in tables['Q7B27-']:ck(r['status']=='unanswered-no-secrets-requested','B27 no invented answer')
    for n,r in enumerate(tables['BK7B27-'],1):ck(r['prior_backlog_id']==f'BK7B26-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B27 backlog ancestry/uncompleted')
    ck([r['status'] for r in tables['BK7B27-'][2:6]]==['not-started']*4,'B27 C axes unstarted')
    ad=tables['AD7B27-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B27 onlythree adjudicated roots')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B27 honest comparison depth')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B27 adjudication source chain')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[f'review-scope-07B{n}.csv' for n in range(1,27)]
    before={r['path'] for n in prior_names for r in rows(n)};paths=set(scope);rem=original.keys()-(before|paths)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(rem),complement_kinds=dict(collections.Counter(original[p]['kind'] for p in rem)))
    ck(bk==dict(selected_paths=7,prior_union=425,overlap=6,new=1,union=426,complement=401,complement_kinds={'source':336,'generated-artifact':61,'project-or-resource':4}),'B27 bookkeeping not coverage percent')
    d=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B27.json'))
    ck(d['authority']==['PHASE-07-REMAINING-07B26.md','evidence/split-register-07B26.csv','evidence/residual-disposition-07B26.csv'] and d['selected_upstream_split']=='SP7B26-01' and d['entry']==ENTRY and d['bookkeeping']==bk,'B27 reasoned scope authority')
    ck(set(d['new_paths'])==paths-before and d['historical_metadata_screen_count']==326 and d['historical_body_review_claim'] is False and d['historical_comparison_depth']==DEDUP_DEPTH,'B27 comparison depth')
    ck(d['bounded_read_slice_count']==11 and d['whole_local_search_files']==2 and d['whole_local_search_lines']==dict(code_behind=698,xaml=561),'B27 whole local search only')
    for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(d[k] is False,'B27 scope permission/count boundary')
    wp='evidence/invoice-search-witnesses-07B27.json';fp='evidence/invoice-search-witness-attempt-01-07B27.json'
    ck(v.sha(v.AUDIT/wp)==WITNESS_SHA,'B27 immutable successful stdout')
    ck(v.sha(v.AUDIT/fp)==FAILED_WITNESS_SHA,'B27 failed attempt retained verbatim not passed evidence')
    failed=v.json.loads(v.read(v.AUDIT/fp));ck(failed['errors']==['ST7B27-19'] and failed['static_lexical_contract_checks'][18]['documented_text_observation_matches'] is False,'B27 failed attempt not laundered')
    witness,match=v.recompute(wp,'tools/check_invoice_search_witnesses.py')
    for e in witness_metadata_errors(witness):ck(False,e)
    ck(witness['errors']==[],'B27 successful witness observations')
    for key,prefix,flag in (('illustrations','ALG7B27-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B27-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,20);v.related(data,known)
        for r in data:
            ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B27 witness not runtime or policy acceptance');validate_source(v,r,scope)
    reads=witness['bounded_source_reads_not_semantic_coverage'];ck(len(reads)==11 and {r['path'] for r in reads}==paths,'B27 actual11 reads7paths')
    ck(sum(r['whole_local_file_selected'] is True for r in reads)==2,'B27 exactlytwo locally whole search files')
    for r in reads:
        ck(r['encoding']=='strict-utf-8' and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True,'B27 reads not semantic certification')
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B27 source read',phase=7)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    pending=False
    source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B27.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B27 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B27.md','PHASE-07-REMAINING-07B27.md','7B28','غير مأذونة','6eedc06','10ba215')),'B27 shared index current boundary:'+name)
    hp='evidence/historical-mode-verification-07B27.json';ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hp).is_file(),'B27 genuine32 captured')
    if (v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B27 actual historical32 identity');history=v.json.loads(v.read(v.AUDIT/hp))
        for e in historical_record_errors(history):ck(False,e)
        ck(history['checkout_head']==ENTRY and history['source_head']==v.HEAD and history['branch']==v.BRANCH,'B27 historical source/entry/capture')
        report['phase_7B27_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=32,all_documentary_exit_codes_zero=True,B26_OWN326_raw327CRLF_and_historical48_child=True,B25_OWN324_ALL44_and_B24_OWN322_ALL44_retained=True,null_means_aggregate_unreported_not_zero=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_invoice_search_witnesses.py','validate_invoice_search_part.py','run_historical_bulk_product_tests_07B27.py','test_invoice_search_audit_validator.py']
    for n in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/n),filename=n)
        except SyntaxError as exc:ck(False,'B27 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==52
    ck(passed,'B27 52 documentary self-tests/count: '+(run.stderr[-7000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=52,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B27-329-bounded-R4k-invoice-search-not-7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,28))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B28-proposed-R4l-SP01-SP02-SP03-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=157,phase_7B27=3,total_open_not_remediated=329,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:7,'phase_7B27_prior_union':425,'phase_7B27_overlap_with_prior_union':6,'phase_7B27_new_paths':1,'unique_union_not_line_or_execution_coverage':426,'inventory_only_no_selected_scope':401})
    report['phase_7B26_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=765,historical_check_record_overwritten=False,genuine_b26_stdout_sha256_unchanged=B26_CHECK_SHA,partial7B27_append_only_extensions=[],all326_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B27_invoice_search_trace_limits']=dict(criteria_boundaries=8,selection_boundaries=8,bounded_source_reads=11,selected_paths=7,whole_local_search_files=2,whole_local_search_lines=1259,current_features_or_documentary_contracts=18,invariants_not_executed_tests=18,acceptance_plans_not_executed=36,residual_inputs=14,explicit_further_static_splits=3,B_R4k_delivered_not_whole_SP01_R4_or7B_closure=True,retained_potential_roots=['P4-014','P7-132','P7-145'],server_process2_selected1_empty_All_only2_is_supplied_predicate_model=True,caller_status1_dropped_by_date_or_reset_and_consumer_not_restoring_it=True,request1_admits20_globalid_retained_consumer_maps_source_type=True,period_postpone_return_quoting_health_leads_not_additional_findings=True,database_commit_or_saved_loss_claimed=False,all_callers_or_external_DTOs_body_reviewed=False,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synced_not_asserted=True)
    report['evidence_rows'].update(phase_7B27_illustrations_not_erp_tests=20,phase_7B27_lexical_checks_not_erp_tests=20,phase_7B27_bounded_source_reads_not_semantic_coverage=11,phase_7B27_witness_recomputed_matches_saved=match)
    report['phase_7B27_audit_tool_quality']=dict(failed_new_attempt_retained=fp,failed_attempt_sha256=FAILED_WITNESS_SHA,failed_attempt_errors=['ST7B27-19'],successful_official_witness=wp,successful_witness_sha256=WITNESS_SHA,failed_attempt_not_counted_as_passed_evidence=True,only_new_observation_ranges_corrected_within_already_whole_XAML=True)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only bounded7B27/R4k:765 protected/all326 EXACT dictionaries/ALLnext_phase/evidence/raw327CRLFprefix/G223/827 originals/3freezes. Three Medium source-local roots155 fixed serverProc versus local selectedProc snapshot;156 caller InvoiceStatus1 lost by date/reset Cond replacement, not a business status/ACL policy claim;157 request1 widened by OR20, GlobalID retained but caller GID+branch consumer maps source type20. Supplied rows, explicit handler actions and ordinal-day predicates only, NOT SQL/DataView/.NET/WPF/events/calendar/culture/SDK/provider/permissions/stock/save/financial/production execution, fixes or saved losses. Whole local698C#/561XAML search plus11 reads7paths not all callers/fields/DTOs/477bodies/census/455FE. All326 summaries plus selected nearest docs/chains not all326 bodies. Scope7/6overlap/1new->426/complement401 not percentage or401 C tasks.18FE/INV/36 plans NOT executed;RS14/SP3/HQ6 preserve full ancestry/input-prefix/routes/disposition,not14 approvals. All014/132/145 potential and020/021 financial/ACL/stock/save/production barriers unchanged. Period/postpone/return/074-family/dirty/health leads not extra roots;not045/061/073/120/131/132 or009 recount/extensions. ALL48 B26 protected cases use OWN326/raw327CRLF/indexes/presetB26 child and suite-local A;B25/44 andB24/44 separately retained,B23/44,B22/40,B21/36,B20/32,B19/36,B18/28 unchanged. Actual current CLI B27/API main defaultB15 separately tested. No protected edits/skips/globalPath/sharedsubprocess mutation/disk overlay/rebaseline/archive rewrite. Actual32 archive retains capture-time checker hashes,not final-wholesale/postpush replay. Failed new witness attempt01 remains exact failed evidence;corrected official stdout is separate. Reference2026-11-16 versus observed sandbox2026-11-20 and source10ba/B26capturedd38f97/delivery-entry6eedc06 distinct. B10 additive10vs120/equality1=10/protectedG138 retained.7B/7 partial,R4l/B28 proposed,7C unstarted,8 unauthorized;independent repair start/sync unknown,no repair-to-audit merge;next_phase8 planning only.')
