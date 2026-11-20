#!/usr/bin/env python3
"""Read-only B26/R4j documentary guards, NEVER bulk-edit/SQL/ERP acceptance.

Preserve734 artifacts/all324 dictionaries/ALLnext_phase/evidence/raw325CRLF
prefix/G219/827 originals/three entry freezes. ALL44 protected B25 cases use
OWN324/presetB25/indexes and a suite-local A in an isolated child. B24 remains
separately versioned. No protected edit/skip/global Path/shared subprocess
mutation/disk overlay/rebaseline/archive rewrite.153 is a constant assignment
replacing validated packing input;154 is general scalar/child price divergence,
not026 resolver policy,142 customer override,151 outcome or152 feedback.
Whole local378C#/469XAML bulk editor +15 reads/9paths is NOT a capability census,
all Product fields/callers/SDK defaults or financial/unit policy certification.
7B/7 partial,R4k/B27 proposed,7C unstarted,8 unauthorized; repairs independent.
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
from validate_property_dialog_part import historical_record_errors as historical30_errors, source_evidence_union

ENTRY = 'dd38f97e844dc60ea64ae00fa40ef588e49752d7'
SNAPSHOT = 'evidence/findings-through-07B25.csv'
SNAPSHOT_SHA = 'ae6a586e17c1c9ea855f74f0c08b968714ce0a837022e45cf94c68c999dda0b7'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B25.json'
SHARED_SHA = '2fd58ab2cefc671b6b196cf363e3551a656a869b46f8c36dab86ba627a50069e'
PROVENANCE_SHA = '9f54294d9b63bd6ea39ec097732c3e07db3a5fe3ca517b87a4159cbe8551f3ca'
B25_CHECK_SHA = '82e5fdc23dc719341a8992d3f1b696f71c985de31285eae4df4b4963ebbee437'
WITNESS_SHA = '8d9d2b53efdf54a382e47fad286cc2ec17c13e580316be1548d86f28bb61b65b'
HISTORICAL_RUN_SHA = 'e77cca247569f3700c95d2ac2d3de84d7f092177acba79ae55b9dfbc43a000a6'  # Actual31 OWN captures retain capture-time tool hashes, never regenerate.
SCOPE_FILE = 'review-scope-07B26.csv'
DOCUMENTARY = 'none-documentary-metadata'
NEW_IDS = ['P7-153', 'P7-154']
PART_DOCS = ('PHASE-07B26.md', 'BULK-PRODUCT-CONTRACTS-07B26.md',
             'VALIDATION-07B26.md', 'PHASE-07-REMAINING-07B26.md', 'DATE-IDENTITY-NOTE-07B26.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
TABLE_SPECS = (
    ('bulk-edit-lineage', 'BE7B26-', 8), ('product-write-lineage', 'PW7B26-', 8),
    ('feature-implementation-matrix', 'FE7B26-', 16), ('report-invariants', 'INV7B26-', 16),
    ('acceptance-tests', 'P7B26T-', 32), ('report-reconciliation', 'RC7B26-', 4),
    ('root-adjudication', 'AD7B26-', 8), ('residual-disposition', 'RS7B26-', 14),
    ('split-register', 'SP7B26-', 3), ('handoffs', 'H7B26-', 6), ('questions', 'Q7B26-', 6),
    ('remaining-workplan', 'RW7B26-', 10), ('continuation-backlog', 'BK7B26-', 10),
)
SENTINELS = {f'{p}{n:02d}' for p, ns in (
    ('FE7B26-', range(15, 17)), ('INV7B26-', range(15, 17)), ('P7B26T-', range(29, 33)),
    ('AD7B26-', (7, 8)), ('RS7B26-', range(1, 15)), ('H7B26-', range(1, 7)),
    ('Q7B26-', range(1, 7))) for n in ns}
BULK_BOUNDARIES = ['directory-selection', 'mode-input', 'packing-assignment', 'general-header-prices',
                   'selected-unit-gate', 'price-command-flags', 'four-price-operations', 'single-editor-controls']
WRITER_BOUNDARIES = ['hydrated-product-units', 'header-parameters', 'unit-delete-insert-parameters',
                     'matched-unit-consumer', 'no-unit-fallback', 'normal-writer-gate', 'sdk-defaults-limit',
                     'packing-downstream']
DEDUP_DEPTH = 'all324-title-certainty-summaries-plus-path-filtered-metadata-and-selected-nearest-doc-bodies-source-chains-not-all-historical-bodies'


@contextmanager
def historical_b25_inputs(v, frozen324, texts, raw):
    """Exact OWN324 input in a context-local path, never a global pathlib patch."""
    if len(frozen324) != 324 or len({r.get('id') for r in frozen324}) != 324:
        raise ValueError('Exactly324 distinct B25 OWN rows required')
    if set(texts) != set(SHARED_DOCS) or any(not isinstance(s, str) for s in texts.values()):
        raise ValueError('Exactly three frozen shared texts required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM frozen bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('Malformed324 frozen registry') from exc
    if (parsed != frozen324 or raw.count(b'\r\n') != 325 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        raise ValueError('324 rows/raw325CRLF disagree')
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
        with historical_b1_inputs(v, frozen324, texts):
            yield
    finally:
        v.AUDIT = original


class HistoricalB25Subprocess:
    """Redirect ONLY the exact protected B25 suite argv; preserve other calls."""
    def __init__(self, backend, python, tool_dir):
        self.backend = backend
        self.expected = [python, '-B', str(tool_dir / 'test_property_dialog_audit_validator.py')]
        self.actual = [python, '-B', str(tool_dir / 'run_historical_property_dialog_tests_07B26.py'),
                       '--through-part', 'B25']

    def __getattr__(self, name):
        return getattr(self.backend, name)

    def run(self, args, *pos, **kwargs):
        return self.backend.run(self.actual if args == self.expected else args, *pos, **kwargs)


class HistoricalB25ValidatorView:
    def __init__(self, target):
        object.__setattr__(self, '_target', target)
        object.__setattr__(self, '_subprocess', HistoricalB25Subprocess(
            target.subprocess, target.sys.executable, target.AUDIT / 'tools'))

    def __getattr__(self, name):
        return self._subprocess if name == 'subprocess' else getattr(self._target, name)

    def __setattr__(self, name, value):
        setattr(self._target, name, value)


@contextmanager
def historical_b25_validation(v, report, prior, prov, frozen324):
    ck = v.check
    for name, digest in (('evidence/provenance-07B26.json', PROVENANCE_SHA), (SNAPSHOT, SNAPSHOT_SHA),
                         (SHARED_SNAPSHOT, SHARED_SHA), ('evidence/checks-07B25.json', B25_CHECK_SHA)):
        ck(v.sha(v.AUDIT / name) == digest, 'B26 immutable entry:' + name)
    ck(prov['historical_artifact_count'] == 734 and len(frozen324) == 324, 'B26 entry734/324')
    ck(prov['registry_at_entry_snapshot'] == SNAPSHOT and prov['registry_at_entry_sha256'] == SNAPSHOT_SHA
       and prov['shared_indexes_at_entry'] == SHARED_SNAPSHOT
       and prov['shared_indexes_at_entry_sha256'] == SHARED_SHA, 'B26 frozen entry identities')
    ck(all(prov['historical_artifact_sha256'].get(n) == h
           for n, h in prior['historical_artifact_sha256'].items()), 'B26 protected703-to734 continuity')
    old = v.json.loads(v.read(v.AUDIT / 'evidence/checks-07B25.json'))
    suites = old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head'] == '45a2a504db4f82927a286ce425f21a82bcee7a84'
       and old['findings']['total_open_not_remediated'] == 324 and old['original_project_hashes_matching'] == 827
       and old['validation']['errors'] == []
       and old['validation']['current_output_record_pending_first_write_not_placeholder'] is False,
       'B26 genuine B25 capture45a2a50, not delivery-entrydd38f97')
    ck(len(suites) == 26 and sum(s['tests_reported'] for s in suites.values()) == 738
       and old['historical_artifact_sha256'] == prior['historical_artifact_sha256'], 'B26 B25 actual738/26/703')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY
       and prov['genuine_B25_check_sha256'] == B25_CHECK_SHA
       and prov['genuine_B25_check_record_checkout'] == old['checkout_head'], 'B26 completed pushed B25 entry')
    ck(prov['phase7B25_entry_consistency'] == dict(original_hashes_matching=827, findings=324,
       audit_file_count=739, documentary_cases=738, self_test_suites=26, errors=[], erp_runtime_tests_executed=0),
       'B26 independent entry consistency')
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    view = HistoricalB25ValidatorView(v)
    with historical_b25_inputs(view, frozen324, texts, (v.AUDIT / SNAPSHOT).read_bytes()):
        yield view
    record = report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][
        'test_property_dialog_audit_validator.py']
    record.update(historical_parser_cutoff='B25-not-current-B26-default', all_original_cases_executed_unmodified=True,
                  dedicated_child_launcher='tools/run_historical_property_dialog_tests_07B26.py',
                  actual_subprocess_argv=view.subprocess.actual, no_test_skips_or_global_subprocess_or_path_patch=True,
                  suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT, validation_scope='historical-through7B25-324-not-current-state',
                  phase_7B25_historical_input_mode='OWN324-exact325CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B25-test-child',
                  phase_7B25_adapter_context=dict(entry_provenance='evidence/provenance-07B26.json',
                      adapter_protected_artifacts_checked=734, current_registry_and_shared_indexes_not_inputs=True,
                      archived_stdout_not_rewritten_after_push=True,
                      B25_parser_assertions_are_historical_preset_not_current_default=True,
                      B25_suite_own_A_uses_context_local_registry_path=True))


def registry_preservation_errors(previous, current, raw, frozen):
    errors = []
    if len(previous) != 324 or current[:324] != previous:
        errors.append('B26 all324 exact fields/ALLnext_phase/evidence')
    if len(current) != 326 or [r.get('id') for r in current[324:]] != NEW_IDS:
        errors.append('B26 only appended153/154')
    if (type(raw) is not bytes or type(frozen) is not bytes or not raw.startswith(frozen)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n') != 327 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n', b'') for x in (b'\r', b'\n'))):
        errors.append('B26 exact324 rawprefix/327CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline=''))) != current:
                errors.append('B26 raw/rows disagree')
        except (UnicodeError, csv.Error):
            errors.append('B26 malformed registry')
    return errors


def group_row_errors(previous, current):
    rows = lambda s: re.findall(r'^\| G-\d{2,3} \|.*$', s, re.M)
    if len(rows(previous)) != 219 or rows(current)[:219] != rows(previous):
        return ['B26 G01..219 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|', current, re.M) != [f'G-{n:02d}' for n in range(1, 224)]:
        return ['B26 only G220..223 exact order']
    return []


def ledger_errors(bulk, writer):
    errors = []
    for data, names, label in ((bulk, BULK_BOUNDARIES, 'bulk'), (writer, WRITER_BOUNDARIES, 'writer')):
        if len(data) != 8 or [r.get('boundary') for r in data] != names:
            errors.append('B26 ordered boundaries:' + label)
        for row in data:
            for key in ('source_to_output', 'observation', 'owner_role', 'required_redacted_input',
                        'impact_if_unavailable', 'next_step', 'limit', 'feature_ids', 'finding_ids', 'evidence'):
                if not isinstance(row.get(key), str) or not row[key].strip():
                    errors.append('B26 ' + label + ' responsibility:' + key)
            if row.get('runtime_status') != 'not-executed':
                errors.append('B26 ' + label + ' runtime overclaim')
    for data, expected in (
        (bulk, {2: 'validated-input-replaced-by-constant2', 3: 'general-header-edit-leaves-existing-unit-stale',
                4: 'same-unit-selection-positive-control-not-remap-approval',
                5: 'separate-command-intent-not-third-finding', 6: 'all-unit-arithmetic-control-not-business-policy'}),
        (writer, {0: 'supplied-source-rows-not-SDK-constructor-defaults',
                  1: 'parameter-plan-not-SQL-execution', 2: 'separate-header-child-price-sources-no-auto-reconciliation',
                  3: 'same-unit-default-no-customer-override-isolates154',
                  4: 'fallback-is-control-not-pricing026-closure',
                  6: 'no-BOM-zero-field-loss-from-unknown-DTO-defaults',
                  7: 'same-FillValue-route-not-recount151-or152'})):
        if len(data) == 8 and any(data[n].get('observation') != value for n, value in expected.items()):
            errors.append('B26 root/command/parameter/default limits')
    return errors


def current_link_errors(features, invariants, tests):
    errors = []
    if (len(features), len(invariants), len(tests)) != (16, 16, 32):
        errors.append('B26 FE16/INV16/T32')
    for n, (fe, inv) in enumerate(zip(features, invariants), 1):
        if inv.get('feature_ids') != fe.get('id') or any(inv.get(k) != fe.get(k)
                for k in ('finding_ids', 'evidence', 'acceptance_ids')):
            errors.append('B26 exact FE/INV lineage')
        related = [t for t in tests if t.get('feature_ids') == fe.get('id')]
        if len(related) != 2 or ';'.join(t['id'] for t in related) != fe.get('acceptance_ids'):
            errors.append('B26 two reverse-linked plans per capability')
        if n <= 2 and (fe.get('finding_ids') != NEW_IDS[n - 1]
                or any(t.get('plan_kind') != 'finding-specific' or t.get('finding_ids') != NEW_IDS[n - 1]
                       for t in related)):
            errors.append('B26 two distinct finding-specific plans')
        for k in ('owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step', 'limit'):
            if not isinstance(fe.get(k), str) or not fe[k].strip():
                errors.append('B26 capability responsibility:' + k)
    errors += bidirectional_errors(features, tests, 'feature_ids') + bidirectional_errors(invariants, tests, 'invariant_ids')
    if len({r.get('required_invariant') for r in invariants}) != 16 or len({r.get('acceptance_criterion') for r in tests}) != 32:
        errors.append('B26 distinct substantive invariants/criteria')
    if any(r.get('status') != 'not-executed' for r in tests):
        errors.append('B26 acceptance never executed')
    return errors


def residual_errors(current, upstream):
    if len(current) != 14 or len(upstream) != 14:
        return ['B26 all14 upstream residuals required']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_residual_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/residual-disposition-07B25.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or new.get('upstream_contract_ids') != old.get('upstream_contract_ids')):
            errors.append('B26 residual ancestry/hash/contracts')
        for k in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                  'next_step', 'static_exit_criterion', 'current_handoff_or_split_ids'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B26 residual responsibility:' + k)
        if not new.get('required_redacted_input', '').startswith(old.get('required_redacted_input', '')):
            errors.append('B26 no lost old input')
        mapped = {x.replace('7B25-', '7B26-') for x in old.get('current_handoff_or_split_ids', '').split(';') if x}
        if not mapped <= set(new.get('current_handoff_or_split_ids', '').split(';')):
            errors.append('B26 no lost mapped route')
        if (new.get('disposition') != old.get('disposition')
                or new.get('disposition') not in {'external-handoff', 'split-explicitly', 'assessment-source-bound'}
                or new.get('runtime_status') != 'not-executed'):
            errors.append('B26 no residual approval/runtime overclaim')
    return errors


def split_errors(current, upstream):
    if len(current) != 3 or len(upstream) != 3:
        return ['B26 exactlythree upstream splits']
    errors = []
    for old, new in zip(upstream, current):
        if (new.get('upstream_split_id') != old.get('id')
                or new.get('upstream_artifact') != 'evidence/split-register-07B25.csv'
                or new.get('upstream_row_sha256') != row_sha(old)
                or not new.get('required_input', '').startswith(old.get('required_input', ''))):
            errors.append('B26 split ancestry/no lost input')
        for k in ('title', 'candidate_scope_not_certified', 'reason_for_split', 'owner_role', 'required_input',
                  'next_static_action', 'static_exit_criterion'):
            if not isinstance(new.get(k), str) or not new[k].strip():
                errors.append('B26 split responsibility:' + k)
        if new.get('status') != 'explicit-further-static-split-not-started' or new.get('runtime_status') != 'not-executed':
            errors.append('B26 split not started/accepted')
    return errors


def remaining_work_errors(work):
    if len(work) != 10:
        return ['B26 fourB/sixC axes']
    expected = (['bounded-parent-contract-delivered-residuals-open'] * 2
                + ['bounded-shared-contract-delivered-residuals-open', 'bounded-R4j-bulk-product-delivered-residuals-open']
                + ['planned-not-started'] * 6)
    errors = []
    if [r.get('status') for r in work] != expected or [r.get('part_family') for r in work] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('B26 boundedR4j/sixC unstarted not closure')
    if any(r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false' for r in work):
        errors.append('B26 no runtime/sessions/percent overclaim')
    return errors


def witness_metadata_errors(w):
    errors = []
    for k in ('application_code_imported_or_executed', 'dotnet_wpf_sql_or_excel_executed', 'application_remediation_performed',
              'phase7C_started', 'phase8_authorized_or_started', 'all_callers_or_external_DTOs_body_reviewed',
              'actual_WPF_event_order_or_count_claimed', 'financial_or_unit_conversion_policy_invented',
              'external_DTO_constructor_defaults_assumed', 'database_commit_or_saved_loss_claimed'):
        if w.get(k) is not False:
            errors.append('B26 false-only boundary:' + k)
    for k in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed', 'scanner_or_printer_tests_executed'):
        if type(w.get(k)) is not int or w[k] != 0:
            errors.append('B26 integer-zero boundary:' + k)
    for k in ('B_R4j_bounded_not_whole7B_closure', 'unresolved_external_contracts_and_explicit_splits_retained',
              'selected_paths_strict_utf8_decode', 'prior026_142_151_152_not_recounted_or_extended'):
        if w.get(k) is not True:
            errors.append('B26 true-only boundary:' + k)
    for k, n in (('illustration_count', 16), ('lexical_check_count', 16), ('selected_source_paths', 9),
                 ('whole_local_editor_files_selected', 2), ('source_read_slice_count', 15)):
        if type(w.get(k)) is not int or w[k] != n:
            errors.append('B26 exact witness count:' + k)
    err = w.get('retained_additive_B10_arithmetic_erratum', {})
    if (err != dict(local_cost=10, reference_cost=120, equality1_control=10, protected_G138_not_rewritten=True)
            or any(type(err.get(k)) is not int for k in ('local_cost', 'reference_cost', 'equality1_control'))
            or err.get('protected_G138_not_rewritten') is not True):
        errors.append('B26 retained B10 additive identity')
    if w.get('audit_reference_date_utc') != '2026-11-16' or w.get('entry_checkout') != ENTRY:
        errors.append('B26 captured witness reference/entry identity')
    return errors


def date_identity_errors(prov, note):
    errors = []
    if (prov.get('audit_reference_date_utc') != '2026-11-16'
            or prov.get('environment_clock_observed_utc') != '2026-11-20T00:28:14.175407+00:00'):
        errors.append('B26 reference16 and observed20 retained separately')
    for token in ('2026-11-16', '2026-11-20', ENTRY, '45a2a504db4f82927a286ce425f21a82bcee7a84',
                  B25_CHECK_SHA, '218939', '734', '324', '739', WITNESS_SHA):
        if token not in note:
            errors.append('B26 additive date/capture identity:' + token)
    if prov.get('genuine_B25_check_record_checkout') == ENTRY:
        errors.append('B26 capture cannot be relabelled delivery')
    return errors


def historical_record_errors(h):
    modes = h.get('historical_modes', [])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count'] != 31 or len(modes) != 31:
        return ['B26 exactly31 actual OWN modes required']
    errors = historical30_errors(dict(historical_mode_count=30, historical_modes=modes[:30], errors=h.get('errors')))
    last = modes[-1]
    for k, value in dict(mode='B25', findings_total=324, registry_used=SNAPSHOT, process_exit_code=0,
                         validation_errors=[], original_project_hashes_matching=827,
                         audit_checker_self_test_cases_reported=738, audit_checker_self_test_suite_count=26).items():
        if last.get(k) != value or type(last.get(k)) is not type(value):
            errors.append('B26 B25 OWN324/738/26:' + k)
    child = last.get('historical_B25_child') or {}
    for k, value in dict(tests_reported=44, expected_tests=44, process_exit_code=0, result='passed',
                         historical_parser_cutoff='B25-not-current-B26-default',
                         all_original_cases_executed_unmodified=True,
                         dedicated_child_launcher='tools/run_historical_property_dialog_tests_07B26.py',
                         no_test_skips_or_global_subprocess_or_path_patch=True,
                         suite_own_registry_path_is_context_local_not_global=True).items():
        if child.get(k) != value or type(child.get(k)) is not type(value):
            errors.append('B26 B25 ALL44 explicit child:' + k)
    for k in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
        if type(last.get(k)) is not int or last[k] != 0:
            errors.append('B26 no historical ERP/SQL')
    if not isinstance(last.get('stdout_sha256'), str) or re.fullmatch('[0-9a-f]{64}', last['stdout_sha256']) is None:
        errors.append('B26 historical stdout identity')
    return errors


def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == DOCUMENTARY:
        v.check(row['id'] in SENTINELS, 'B26 undeclared documentary sentinel:' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B26 fabricated source for documentary gate:' + row['id'])
        v.evidence(row['evidence'], row['id'])
        try:
            expanded = expanded_source_evidence(row['evidence'])
        except ValueError as exc:
            v.check(False, 'B26 invalid source ' + row['id'] + ':' + str(exc))
            return
        v.scoped_evidence(expanded, scope, row['id'] + ' boundedB26', phase=7)


def extend_bulk_products(v, report, prov, frozen324):
    ck, rows = v.check, v.rows
    current = rows('findings.csv')
    new = current[324:]
    for error in registry_preservation_errors(frozen324, current, (v.AUDIT / 'findings.csv').read_bytes(), (v.AUDIT / SNAPSHOT).read_bytes()):
        ck(False, error)
    ck(len({r['id'] for r in current}) == 326, 'B26 distinct326 IDs')
    ck(rows('evidence/historical-extensions-07B26.csv') == [], 'B26 zero historical extensions')
    v.distributions(new, dict(Medium=2), dict(confirmed=2), 'B26 only')
    for r in new:
        ck((r['type'], r['status'], r['next_phase']) == ('implementation-defect', 'open-not-remediated', '8'), 'B26 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$', v.read(v.AUDIT / PART_DOCS[0]), re.M)
       == [(r['id'], r['title']) for r in new], 'B26 heading/registry exact')
    lookup = {r['id']: r for r in current}
    for name in ('P4-014', 'P7-132', 'P7-145'):
        ck(lookup[name]['certainty'] == 'potential', 'B26 retained potential:' + name)
    for k in ('phase8_authorized_or_started', 'phase7C_started', 'application_remediation_performed'):
        ck(prov[k] is False, 'B26 no implicit start:' + k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch'] is True, 'B26 no repair-to-audit merge')
    for k in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
        ck(type(prov[k]) is int and prov[k] == 0, 'B26 no ERP/SQL:' + k)
    for error in date_identity_errors(prov, v.read(v.AUDIT / 'DATE-IDENTITY-NOTE-07B26.md')):
        ck(False, error)

    selected = rows(SCOPE_FILE)
    scope = {r['path']: v.spans(r['ranges']) for r in selected}
    original = {r['path']: r for r in rows('evidence/inventory.csv')}
    ck(len(selected) == len(scope) == 9, 'B26 nine bounded source paths')
    for r in selected:
        ck(r['path'] in original and r['review_state'] == 'whole-local-bulk-editor-or-selected-surrounding-static-slices-not-runtime-certified'
           and bool(r['focus']), 'B26 scope identity/depth')
        v.source_ref(r['path'], r['ranges'], SCOPE_FILE)
    for r in new:
        validate_source(v, r, scope)
    known = {r['id'] for r in current} | {f'H7B26-{n:02d}' for n in range(1, 7)}
    tables = {}
    for name, prefix, count in TABLE_SPECS:
        data = rows('evidence/' + name + '-07B26.csv')
        tables[prefix] = data
        v.sequential(data, prefix, count)
        if data and 'finding_ids' in data[0]:
            v.related(data, known)
        for r in data:
            ck(all(isinstance(x, str) and x.strip() for x in r.values()), 'B26 incompleteCSV:' + r['id'])
            validate_source(v, r, scope)
            if 'runtime_status' in r:
                ck(r['runtime_status'] == 'not-executed', 'B26 runtime overclaim:' + r['id'])
    fe, inv, tests = [tables[x] for x in ('FE7B26-', 'INV7B26-', 'P7B26T-')]
    for error in current_link_errors(fe, inv, tests) + ledger_errors(tables['BE7B26-'], tables['PW7B26-']):
        ck(False, error)
    ck(all(f['status'] == 'confirmed-source-local' for f in fe[:2]), 'B26 two source-local causes only')
    v.proposed_tests(tests, '7B26')
    fids, iids, tids = [{r['id'] for r in pool} for pool in (fe, inv, tests)]
    v.related(tests, fids, 'feature_ids')
    v.related(tests, iids, 'invariant_ids')
    v.related(fe + inv, tids, 'acceptance_ids')
    v.related(tables['BE7B26-'] + tables['PW7B26-'], fids, 'feature_ids')
    for pool, label in ((fe, 'features'), (inv, 'invariants'), (tests, 'plans')):
        v.covered(new, pool, 'B26 ' + label)
    for r in tables['RC7B26-']:
        fs = [f for f in fe if f['id'] in r['feature_ids'].split(';')]
        unique = lambda k: ';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        ck(r['finding_ids'] == unique('finding_ids') and r['acceptance_ids'] == unique('acceptance_ids')
           and r['evidence'] == source_evidence_union(fs), 'B26 exact expanded-before-dedup RC lineage')
        v.related([r], fids, 'feature_ids')
        v.related([r], tids, 'acceptance_ids')
    for error in (residual_errors(tables['RS7B26-'], rows('evidence/residual-disposition-07B25.csv'))
                  + split_errors(tables['SP7B26-'], rows('evidence/split-register-07B25.csv'))
                  + remaining_work_errors(tables['RW7B26-'])):
        ck(False, error)
    hids = {r['id'] for r in tables['H7B26-']}
    sids = {r['id'] for r in tables['SP7B26-']}
    v.related(tables['RS7B26-'], hids | sids, 'current_handoff_or_split_ids')
    v.related(tables['Q7B26-'], hids, 'handoff_ids')
    for r in tables['H7B26-']:
        ck(r['status'] == 'external-contract-or-policy-unresolved-not-absence-proof', 'B26 no invented approval')
    for r in tables['Q7B26-']:
        ck(r['status'] == 'unanswered-no-secrets-requested', 'B26 no invented answer')
    for n, r in enumerate(tables['BK7B26-'], 1):
        ck(r['prior_backlog_id'] == f'BK7B25-{n:02d}' and r['original_backlog_id'] == f'BK7-{n:02d}'
           and r['status'] != 'complete', 'B26 backlog ancestry/uncompleted')
    ck([r['status'] for r in tables['BK7B26-'][2:6]] == ['not-started'] * 4, 'B26 C axes unstarted')
    ad = tables['AD7B26-']
    v.related(ad, known, 'current_root_ids')
    v.related(ad, known, 'nearest_prior_root_ids')
    ck([r['current_root_ids'] for r in ad if r['decision'] == 'new-local-root'] == NEW_IDS, 'B26 onlytwo adjudicated new roots')
    ck([r['current_root_ids'] for r in ad if r['decision'] == 'same-current-root-command-controls-not-separate-finding']
       == ['P7-154'], 'B26 sale/purchase/command controls not third root')
    for r, a in zip(new, ad):
        ck(set(r['evidence'].split(';')) <= set(a['evidence'].split(';')), 'B26 adjudication source chain')
    ck(all(r['comparison_depth'] == DEDUP_DEPTH for r in ad), 'B26 honest comparison depth')

    prior_names = (['review-scope.csv'] + [f'review-scope-{n:02d}.csv' for n in range(2, 8)]
                   + [f'review-scope-07B{n}.csv' for n in range(1, 26)])
    before = {r['path'] for name in prior_names for r in rows(name)}
    paths = set(scope)
    complement = original.keys() - (before | paths)
    bk = dict(selected_paths=len(paths), prior_union=len(before), overlap=len(paths & before),
              new=len(paths - before), union=len(before | paths), complement=len(complement),
              complement_kinds=dict(collections.Counter(original[p]['kind'] for p in complement)))
    ck(bk == dict(selected_paths=9, prior_union=421, overlap=5, new=4, union=425, complement=402,
                  complement_kinds={'source': 337, 'generated-artifact': 61, 'project-or-resource': 4}),
       'B26 scope not completion percentage')
    decision = v.json.loads(v.read(v.AUDIT / 'evidence/scope-decision-07B26.json'))
    ck(decision['authority'] == ['PHASE-07-REMAINING-07B25.md', 'evidence/split-register-07B25.csv',
                                 'evidence/residual-disposition-07B25.csv']
       and decision['selected_upstream_split'] == 'SP7B25-01' and decision['entry'] == ENTRY
       and decision['bookkeeping'] == bk, 'B26 authority/reasoned scope')
    ck(set(decision['new_paths']) == paths - before and decision['historical_metadata_screen_count'] == 324
       and decision['historical_body_review_claim'] is False and decision['historical_comparison_depth'] == DEDUP_DEPTH,
       'B26 comparison depth')
    ck(decision['bounded_read_slice_count'] == 15 and decision['whole_local_editor_files'] == 2
       and decision['whole_local_editor_lines'] == dict(code_behind=378, xaml=469), 'B26 exact local editor depth')
    for k in ('phase7C_started', 'phase8_authorized_or_started', 'counts_are_completion_percent_or_sessions'):
        ck(decision[k] is False, 'B26 scope permission/count boundary')
    ck(v.sha(v.AUDIT / 'evidence/bulk-product-witnesses-07B26.json') == WITNESS_SHA, 'B26 immutable witness stdout')
    witness, match = v.recompute('evidence/bulk-product-witnesses-07B26.json', 'tools/check_bulk_product_witnesses.py')
    for error in witness_metadata_errors(witness):
        ck(False, error)
    ck(witness['errors'] == [], 'B26 witness observations')
    for key, prefix, flag in (('illustrations', 'ALG7B26-', 'illustration_assertions_passed'),
                              ('static_lexical_contract_checks', 'ST7B26-', 'documented_text_observation_matches')):
        data = witness[key]
        v.sequential(data, prefix, 16)
        v.related(data, known)
        for r in data:
            ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']), 'B26 witness not runtime/policy acceptance')
            validate_source(v, r, scope)
    reads = witness['bounded_source_reads_not_semantic_coverage']
    ck(len(reads) == 15 and {r['path'] for r in reads} == paths, 'B26 actual15 text reads9paths')
    ck(sum(r['whole_local_file_selected'] is True for r in reads) == 2, 'B26 exactlytwo locally whole editor files')
    for r in reads:
        ck(r['encoding'] == 'strict-utf-8' and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review'] is True,
           'B26 reads not whole-feature certification')
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}', scope, 'B26 source read', phase=7)

    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'], v.read(v.AUDIT / 'IMPROVEMENTS.md')):
        ck(False, error)
    pending = False
    source = re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS + SHARED_DOCS:
        doc = v.AUDIT / name
        text = v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', text):
            url = urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):
                continue
            target = (doc.parent / unquote(url.path)).resolve()
            if target == (v.AUDIT / 'evidence/checks-07B26.json').resolve() and not target.exists():
                pending = True
                continue
            v.LINK_COUNT += 1
            ck(target.exists(), 'B26 broken link:' + name + ':' + m[1])
        for m in source.finditer(text):
            v.source_ref(m[1], m[2], name)
            if name in PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a, b in v.spans(m[2])), scope, name, phase=7)
    for name in SHARED_DOCS:
        ck(all(t in v.read(v.AUDIT / name) for t in ('PHASE-07B26.md', 'PHASE-07-REMAINING-07B26.md',
                                                    '7B27', 'غير مأذونة', 'dd38f97', '10ba215')),
           'B26 shared index current boundary:' + name)
    hp = 'evidence/historical-mode-verification-07B26.json'
    ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT / hp).is_file(), 'B26 genuine31 captured')
    if (v.AUDIT / hp).is_file():
        ck(v.sha(v.AUDIT / hp) == HISTORICAL_RUN_SHA, 'B26 actual historical31 identity')
        history = v.json.loads(v.read(v.AUDIT / hp))
        for error in historical_record_errors(history):
            ck(False, error)
        ck(history['checkout_head'] == ENTRY and history['source_head'] == v.HEAD and history['branch'] == v.BRANCH,
           'B26 historical source/entry/capture')
        report['phase_7B26_executed_historical_documentary_modes'] = dict(record=hp, sha256=HISTORICAL_RUN_SHA,
            modes_reported=31, all_documentary_exit_codes_zero=True, B25_OWN324_raw325CRLF_and_historical44_child=True,
            B24_OWN322_raw323CRLF_and_historical44_child_retained=True,
            null_means_aggregate_not_reported_not_zero=True, not_original_metric_replay_or_erp_tests=True)
    tools = ['check_bulk_product_witnesses.py', 'validate_bulk_product_part.py',
             'run_historical_property_dialog_tests_07B26.py', 'test_bulk_product_audit_validator.py']
    for name in tools:
        try:
            v.ast.parse(v.read(v.AUDIT / 'tools' / name), filename=name)
        except SyntaxError as exc:
            ck(False, 'B26 syntax:' + str(exc))
    run = v.subprocess.run([v.sys.executable, '-B', str(v.AUDIT / 'tools' / tools[-1])], cwd=v.ROOT,
                           capture_output=True, text=True, timeout=60)
    m = re.search(r'Ran (\d+) tests? in ', run.stderr + '\n' + run.stdout)
    count = int(m[1]) if m else None
    passed = run.returncode == 0 and count == 48
    ck(passed, 'B26 48 documentary self-tests/count: ' + (run.stderr[-7000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]] = dict(
        tests_reported=count, expected_tests=48, process_exit_code=run.returncode,
        result='passed' if passed else 'failed-or-unrecognized', erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked'] += tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update(
        {'tools/' + name: v.sha(v.AUDIT / 'tools' / name) for name in ['validate_audit.py'] + tools})
    report.update(validation_scope='current-through7B26-326-bounded-R4j-bulk-product-not-7B-or-runtime-closure',
                  phase_7_delivery='7A+' + '+'.join('7B' + str(n) for n in range(1, 27)) + '-partial-not-complete7B-or7',
                  phase_7_remaining_parts=['7B27-proposed-R4k-explicit-SP01-SP02-SP03-and-external-contracts',
                                           '7C-six-axes-not-started'], registry_used='findings.csv',
                  historical_artifact_sha256=prov['historical_artifact_sha256'], date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=154, phase_7B26=2, total_open_not_remediated=326,
                             severity=dict(collections.Counter(r['severity'] for r in current)),
                             certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE: 9, 'phase_7B26_prior_union': 421,
        'phase_7B26_overlap_with_prior_union': 5, 'phase_7B26_new_paths': 4,
        'unique_union_not_line_or_execution_coverage': 425, 'inventory_only_no_selected_scope': 402})
    report['phase_7B25_historical_evidence'] = dict(frozen_registry=SNAPSHOT,
        frozen_registry_sha256_matches=v.sha(v.AUDIT / SNAPSHOT) == SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT, earlier_report_evidence_artifacts_hash_checked=734,
        historical_check_record_overwritten=False, genuine_b25_stdout_sha256_unchanged=B25_CHECK_SHA,
        partial7B26_append_only_extensions=[], all324_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B26_bulk_product_trace_limits'] = dict(selected_bulk_boundaries=8, selected_writer_boundaries=8,
        bounded_source_reads=15, selected_paths=9, whole_local_editor_files=2, whole_local_editor_lines=847,
        all_callers_or_SDK_DTOs_body_reviewed=False, current_features_or_documentary_contracts=16,
        invariants_not_executed_tests=16, acceptance_plans_not_executed=32, residual_inputs=14,
        explicit_further_static_splits=3, B_R4j_delivered_not_whole_R4_SP01_or7B_closure=True,
        retained_potential_roots_not_promoted=['P4-014', 'P7-132', 'P7-145'],
        packing12_and24_to2_input2_fixed_point_and_zero_unselected_controls=True,
        general_sale20_unit10_purchase8_unit6_are_supplied_local_parameter_consumer_maps=True,
        same_unit_selection_and_no_unit_fallback_and_four_price_commands_are_controls_not_policy_acceptance=True,
        no_third_checkbox_BOM_zero_field_or_DTO_default_root=True, database_commit_or_saved_loss_claimed=False,
        prior026_142_151_152_not_recounted_or_extended=True, C_axes_not_started=6,
        counts_are_sessions_or_completion_percent=False, repair_conversation_started_or_synced_not_asserted=True)
    report['evidence_rows'].update(phase_7B26_illustrations_not_erp_tests=16, phase_7B26_lexical_checks_not_erp_tests=16,
        phase_7B26_bounded_source_reads_not_semantic_coverage=15, phase_7B26_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder'] = pending
    report['validation']['limit'] = (
        'Read-only bounded7B26/R4j:734 protected artifacts/all324 EXACT dictionaries and ALLnext_phase/evidence/'
        'raw325CRLFprefix/G219/827 originals/three entry freezes.153 Medium confirmed source-local: valid packing '
        'input12 or24 validated for property2 then PackingValue=2.0, header @FillValue and attached column map; '
        'downstream FillRatio/dialog width text trace, input2 fixed-point,zero/unselected/other-property controls. '
        '154 Medium confirmed source-local: general scalar sale20/purchase8 vs supplied existing main-unit10/6, '
        'optional selected-unit gate, independent header/child writer parameter inputs and matched-unit early return. '
        'Same-unit selection synchronizes and missing-unit fallback uses header; four separate price-operation '
        'commands consult flags and update all supplied units. Not third checkbox finding, not pricing026/customer142, '
        'outcome151/feedback152/tombstone021/employee028 or production133/134 recount or historical extension. '
        'No SDK constructor/default0, lost BOM/parent/image/fields, unit-remap/ratio/duplicate policy or SqlInt '
        'conversion inferred. Supplied positive IDs,Product-shaped data,valid integers,Default/no-customer override '
        'and normal writer-success path are assumptions, not SQL/WPF/commit or saved loss observations. '
        'Whole local editor378C#/469XAML plus15 reads9paths NOT all callers/SDK DTOs/477 bodies/callgraph/455FE '
        'or capability census.324 title/certainty summaries plus path-filtered metadata and named nearest docs/chains, '
        'not all324 bodies or all their evidence paths manually reviewed.9paths/5overlap/4new->425/complement402 '
        'not percentage or402 C tasks.16FE/INV32 plans NOT executed;14 residuals/3splits/HQ6 preserve every '
        'ancestry/input-prefix/mapped-route/disposition, not14 approvals.014/132/145 potential,020/021 and '
        'financial/ACL/stock/save/production barriers unchanged. '
        'B25 OWN324/raw325CRLF/indexes and ALL44 protected cases in explicit presetB25 child with suite-local A; '
        'B24 OWN322/ALL44 remains separately versioned; B23/44,B22/40,B21/36,B20/32,B19/36,B18/28 unchanged. '
        'Actual B26 CLI and API main defaultB15 tested separately. No protected edits/skips/globalPath/shared '
        'subprocess mutation/disk overlay/rebaseline/archive rewrite. Actual31 OWN captures retain capture-time '
        'tool hashes, not final-wholesale or postpush replay. Reference2026-11-16 and observed sandbox2026-11-20 '
        'are distinct; no retiming B25capture45a2a50 as delivery-entrydd38f97. B10 additive10vs120/equality1=10/'
        'protectedG138 retained. No application import/build/C#/VB/.NET/WPF/SQL/provider/SDK/UtilitiesProj/'
        'ToDataTable/REPX/scanner/printer/business data/secrets/remediation/measurement/acceptance.7B/7 partial,'
        'R4k/B27 proposed,7C unstarted,8 unauthorized here;independent repairs not presumed started/synchronized,'
        'no repair-to-audit merge;next_phase8 planning not permission.')
