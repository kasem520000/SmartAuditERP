#!/usr/bin/env python3
"""Read-only PARTIAL7B10 documentary checks. Never ERP acceptance.

Protect292 prior immutable artifacts, frozen282 cores/ALL followups and G01..134.
B9 receives its OWN exact registry/index inputs IN MEMORY without editing its
protected helper/reports/stdout. Source10ba is distinct from docs checkouta254.
Three local bodies/XAML are not whole report features or a phase7 exit.
"""
from __future__ import annotations

from contextlib import contextmanager
import collections
import re
from urllib.parse import unquote, urlsplit

from validate_financial_report_part import (
    historical_b1_inputs, registry_transition_errors, bidirectional_errors,
)
from validate_receipt_payroll_part import (
    build_current_ledger as prior_ledger,
    build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,
    feature_level_errors as prior_feature_errors,
)

SCOPE_FILE = 'review-scope-07B10.csv'
PART_DOCS = ('PHASE-07B10.md', 'SALESMAN-REPORT-CONTRACTS-07B10.md', 'VALIDATION-07B10.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
SNAPSHOT = 'evidence/findings-through-07B9.csv'
SNAPSHOT_SHA = '7b85f5eeb359220a53d93085dcf0d18d700ba4a965b9b3156171e819e7979d19'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B9.json'
SHARED_SHA = '8d3ae3f18066925b56af0747d9475f9ac2883c0ad072805f833ea613e3e65475'
B9_CHECK_SHA = 'fbd73a272131261240ab7fb29270b45642c314538c55e04301db0e6905996e91'
ENTRY_CHECKOUT = 'a2541ed204e62493f93cfb811ba5f81ad3206942'
EXTENDED_FINDINGS = {
    'P1-004', 'P1-013', 'P1-033', 'P2-010', 'P3-023', 'P7-041', 'P7-045',
    'P7-046', 'P7-054', 'P7-061', 'P7-069', 'P7-085', 'P7-095',
}
REVIEWED_BODIES = ('frmInvBySalesMen', 'frmRptItemsProfit', 'frmRptSalesInPeriod')
SENTINELS = {
    'RC7B10-06', 'FE7B10-22', 'INV7B10-22', 'FE7B10-23', 'INV7B10-23',
    'H7B10-06', 'Q7B10-06', 'P7B10T-25', 'P7B10T-26',
}
TABLE_SPECS = (
    ('acceptance-tests', 'P7B10T-', 26),
    ('feature-implementation-matrix', 'FE7B10-', 23),
    ('report-invariants', 'INV7B10-', 23),
    ('report-reconciliation', 'RC7B10-', 6),
    ('historical-extensions', 'EX7B10-', 13),
    ('handoffs', 'H7B10-', 6),
    ('questions', 'Q7B10-', 6),
    ('continuation-backlog', 'BK7B10-', 10),
)


@contextmanager
def historical_b9_inputs(v, frozen282, texts):
    """Exact logical-path overlay, with restoration/deep-copy in prior adapter."""
    if len(frozen282) != 282 or len({x['id'] for x in frozen282}) != 282:
        raise ValueError('Exactly282 distinct historical registry rows required')
    with historical_b1_inputs(v, frozen282, texts):
        yield


def validate_frozen_b9(v, report, prov_b9, frozen280, prov_b10, frozen282):
    ck = v.check
    ck(prov_b10['registry_at_entry_snapshot'] == SNAPSHOT and
       prov_b10['registry_at_entry_sha256'] == SNAPSHOT_SHA,
       'B10 frozen282 identity changed')
    ck(prov_b10['shared_indexes_at_entry'] == SHARED_SNAPSHOT and
       prov_b10['shared_indexes_at_entry_sha256'] == SHARED_SHA and
       v.sha(v.AUDIT / SHARED_SNAPSHOT) == SHARED_SHA,
       'B10 exact delivered B9 indexes changed')
    expected = dict(original_hashes_matching=827, findings=282,
                    phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9-partial-not-complete7B-or7',
                    errors=[], erp_runtime_tests_executed=0)
    ck(prov_b10['phase7B9_entry_consistency'] == expected,
       'B10 entry no longer describes the delivered B9 check')
    for path, digest in prov_b9['historical_artifact_sha256'].items():
        ck(prov_b10['historical_artifact_sha256'].get(path) == digest,
           '269-to292 historical continuity failed: ' + path)
    ck(prov_b10['genuine_B9_check_sha256'] == B9_CHECK_SHA and
       v.sha(v.AUDIT / 'evidence/checks-07B9.json') == B9_CHECK_SHA,
       'Genuine archived B9 stdout changed')
    saved = v.json.loads(v.read(v.AUDIT / 'evidence/checks-07B9.json'))
    ck(saved['validation']['errors'] == [] and
       saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False and
       saved['findings']['total_open_not_remediated'] == 282 and
       saved['original_project_hashes_matching'] == 827 and
       saved['historical_artifact_sha256'] == prov_b9['historical_artifact_sha256'],
       'Archived B9 stdout no longer genuine282/827/269')
    from validate_receipt_payroll_part import extend_receipt_payroll
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    with historical_b9_inputs(v, frozen282, texts):
        extend_receipt_payroll(v, report, prov_b9, frozen280)
    report['registry_used'] = SNAPSHOT
    report['validation_scope'] = 'historical-through7B9-282-not-current-state'
    report['phase_7B9_historical_input_mode'] = 'frozen282-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B9_adapter_context'] = dict(
        entry_provenance='evidence/provenance-07B10.json',
        adapter_protected_artifacts_checked=292,
        current_registry_and_shared_indexes_not_inputs=True,
        historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True,
        archived_stdout_not_rewritten_after_authorized_push=True,
    )
    report['validation']['limit'] += (
        ' HistoricalB9 receives frozen282/exact delivered shared texts IN MEMORY, '
        'never current285/live indexes. Archived B9 stdout checkout3612700 stays '
        'byte-protected; a current docs-only checkout observation is not archive replay.'
    )


def build_current_ledger(inventory, labelled_scopes, parse_ranges):
    result = prior_ledger(inventory, labelled_scopes, parse_ranges)
    selected = {x['path']: x['ranges'] for label, scope in labelled_scopes
                if label == '7B10' for x in scope}
    for row in result:
        row['phase7B10_ranges'] = selected.get(row['path'], 'none')
        if row['inventory_kind'] == 'generated-artifact':
            continue
        row['continuation_bucket'] = '7B11-or-7C-further-contracts-not-closed'
        row['next_scope_work'] = (
            'بقية القدرات/callers/children/output/template/schema/ACL أو استبعاد مسند؛ '
            '7B11 معلنة و7C لم تبدأ. كل الأسطر/اسم/parent لا يغلق ميزة؛ '
            'لا قياس latency/leak/index من نص المصدر.'
        )
    return result


def build_candidate_disposition(inventory, labelled_scopes):
    result = prior_candidates(inventory, labelled_scopes)
    selected = {x['path']: x['ranges'] for label, scope in labelled_scopes
                if label == '7B10' for x in scope}
    for row in result:
        row['phase7B10_ranges'] = selected.get(row['path'], 'none')
        if row['disposition'].startswith('lexical-false-positive'):
            continue
        row['disposition'] = '7B11-further-contracts-or-reasoned-exclusion-required'
        row['reason'] = (
            '98 مرشح ملف فرز أسماء لا98 ميزة؛ B10 يستكمل عقوداً منتقاة ولا يعيد عد '
            'أرباح/حركة الفترة المشمولتين فيB1. المندوبون explicit nonregex screen؛ '
            'لا كلcaller/child/template/schema/ACL/نشر/قبول؛7B11/7C أو استبعاد مسند.'
        )
    return result


def build_screen_disposition(inventory, labelled_scopes):
    result = prior_screens(inventory, labelled_scopes)
    selected = {x['path']: x['ranges'] for label, scope in labelled_scopes
                if label == '7B10' for x in scope}
    full = {x['path']: '1-' + str(x['lines']) for x in inventory
            if str(x['lines']).isdigit()}
    for n, row in enumerate(result, 1):
        row['id'] = f'SC7B10-{n:02d}'
        row['phase7B10_body_ranges'] = selected.get(row['body_path'], 'none')
        row['disposition'] = '7B11-or-7C-further-contracts-or-reasoned-exclusion-required'
        if (row['screen'] in REVIEWED_BODIES and
                all(path in full and selected.get(path) == full[path]
                    for path in (row['path'], row['body_path']))):
            row['coverage_level'] = 'bounded-local-body-and-xaml-not-whole-feature-certified'
            row['reason'] = (
                'جسم/XAML محليان ودعم محدد في7B10؛ أرباح/حركة الفترة لهماB1 سابقة، '
                'فلا عد جديد لمجرد إعادة القراءة. worker بوابة سابقة للمندوبين؛ '
                'لا كلمدخل/طفل/قالب/schema/ACL/نشر/قبول؛7B11/7C.'
            )
        else:
            row['reason'] = (
                'حصر أو مقاطع/أجسام محلية سابقة بحسب الحقول، لا كل العقود أو النشر؛ '
                'child لا يرث تغطية parent.7B11/7C أو استبعاد مسند.'
            )
    return result


def feature_level_errors(features):
    return [x.replace('B9', 'B10') for x in prior_feature_errors(features)]


def group_row_errors(previous_text, current_text):
    old = re.findall(r'^\| G-\d{2,3} \|.*$', previous_text, re.M)
    now = re.findall(r'^\| G-\d{2,3} \|.*$', current_text, re.M)
    return [] if len(old) == 134 and now[:134] == old else ['Historical G01–134 exact rows changed']


def witness_metadata_errors(w):
    errors = []
    for key in ('application_code_imported_or_executed', 'application_remediation_performed',
                'real_business_or_secret_data_used', 'spreadsheet_or_formula_interpreter_executed'):
        if w.get(key) is not False:
            errors.append('B10 witness false-only flag: ' + key)
    for key in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
        if type(w.get(key)) is not int or w[key] != 0:
            errors.append('B10 witness zero-only count: ' + key)
    for key in ('upstream_thread_gate_not_assumed_resolved',
                'notes_compatibility_not_assumed_in_deployment'):
        if w.get(key) is not True:
            errors.append('B10 witness causal boundary lost: ' + key)
    if w.get('phase') != '7B10-partial-static-audit':
        errors.append('B10 witness phase mismatch')
    for key in ('illustration_count', 'static_lexical_contract_check_count'):
        if type(w.get(key)) is not int or w[key] != 20:
            errors.append('B10 witness count mismatch: ' + key)
    return errors


def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == 'none-inventory-only':
        v.check(row['id'] in SENTINELS, 'Undeclared B10 no-source sentinel: ' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B10 documentary/inventory boundary lost: ' + row['id'])
        v.evidence(row['evidence'], row['id'])
        v.scoped_evidence(row['evidence'], scope, row['id'] + ' bounded7B10', phase=7)


def extend_salesman_contracts(v, report, prov, frozen282):
    ck, rows = v.check, v.rows
    ck(prov['historical_artifact_count'] == 292 and len(frozen282) == 282,
       'B10 protected entry count mismatch')
    ident = report['source_reference_validation']
    ck(ident['audited_application_reference'] == v.HEAD and
       ident['reference_ancestor_of_checkout'] is True and
       ident['all_committed_net_delta_paths_under_docs_audit'] is True and
       report['original_project_hashes_matching'] == 827,
       'B10 source/checkout integrity mismatch')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY_CHECKOUT,
       'B10 actual entry after the previously completed B9 push changed')
    reconcile = prov['entry_checkout_reconciliation']
    ck(reconcile['initial_restored_checkout'] == v.HEAD and
       reconcile['all297_workspace_document_bytes_matched_authorized_remote_before_fast_forward'] is True and
       reconcile['application_byte_changes'] is False,
       'B10 entry reconciliation boundary changed')
    ck(prov['erp_runtime_tests_executed'] == 0 and
       prov['application_remediation_performed'] is False and
       prov['phase8_authorized_or_started'] is False,
       'B10 entry falsely authorizes runtime/remediation')

    current = rows('findings.csv')
    new = current[282:]
    extensions = rows('evidence/historical-extensions-07B10.csv')
    ext = v.transition(frozen282, current, 7, EXTENDED_FINDINGS, preserve_followups=True)
    for error in registry_transition_errors(frozen282, current, extensions):
        ck(False, error)
    ck(len(current) == len({x['id'] for x in current}) == 285, 'B10 registry count/uniqueness mismatch')
    ck([x['id'] for x in new] == ['P7-111', 'P7-112', 'P7-113'], 'B10 new IDs/order mismatch')
    v.distributions(new, {'Medium': 3}, {'confirmed': 3}, 'bounded7B10 only')
    for row in new:
        ck(row['status'] == 'open-not-remediated' and row['next_phase'] == '8' and
           row['type'] == 'implementation-defect' and bool(row['title']),
           'B10 new status/type/followup mismatch: ' + row['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$', v.read(v.AUDIT / 'PHASE-07B10.md'), re.M) ==
       [(x['id'], x['title']) for x in new], 'B10 report headings/registry mismatch')
    raw = (v.AUDIT / 'findings.csv').read_bytes()
    ck(raw.count(b'\r\n') == 286 and b'\n' not in raw.replace(b'\r\n', b''),
       'B10 live registry lost the historical CRLF convention')

    scopes = rows(SCOPE_FILE)
    inventory = rows('evidence/inventory.csv')
    paths = {x['path'] for x in inventory}
    scope = {x['path']: v.spans(x['ranges']) for x in scopes}
    ck(len(scopes) == len(scope) == 23, 'B10 scope count/duplicates mismatch')
    for row in scopes:
        ck(row['path'] in paths and row['review_state'] == 'selected-static-source-slices-not-runtime-certified'
           and bool(row['focus']), 'B10 scope state/path mismatch: ' + row['path'])
        v.source_ref(row['path'], row['ranges'], SCOPE_FILE)
    for row in new:
        validate_source(v, row, scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml.cs', '.xaml'):
            path = 'SmartAuditERP/Form_WPF/' + name + suffix
            ck(scope.get(path) == [(1, len(v.read(v.ROOT / path).splitlines()))],
               'B10 body/XAML range mismatch: ' + path)

    known = {x['id'] for x in current} | {f'H7B10-{n:02d}' for n in range(1, 7)}
    tables = {}
    for name, prefix, count in TABLE_SPECS:
        data = rows('evidence/' + name + '-07B10.csv')
        tables[prefix] = data
        v.sequential(data, prefix, count)
        v.related(data, known)
        for row in data:
            for key, value in row.items():
                ck(bool(value), f'Incomplete B10 cell: {row["id"]}.{key}')
            validate_source(v, row, scope)
            if 'runtime_status' in row:
                ck(row['runtime_status'] == 'not-executed', 'B10 runtime claim: ' + row['id'])
    tests, features, invariants, rc = [tables[k] for k in ('P7B10T-', 'FE7B10-', 'INV7B10-', 'RC7B10-')]
    tids = {x['id'] for x in tests}
    fids = {x['id'] for x in features}
    iids = {x['id'] for x in invariants}
    v.proposed_tests(tests, '7B10')
    v.related(tests, fids, 'feature_ids')
    v.related(tests, iids, 'invariant_ids')
    v.related(features + invariants, tids, 'acceptance_ids')
    for pool, field in ((features, 'feature_ids'), (invariants, 'invariant_ids')):
        for error in bidirectional_errors(pool, tests, field):
            ck(False, error)
    for error in feature_level_errors(features):
        ck(False, error)
    for pool, label in ((tests, 'plans'), (features, 'features'), (invariants, 'invariants')):
        v.covered(new, pool, 'B10 ' + label)
    for row in new:
        ck(len([t for t in tests if t['plan_kind'] == 'finding-specific' and
                t['finding_ids'] == row['id']]) == 2,
           'B10 finding lacks two direct plans: ' + row['id'])
    ck([x['plan_kind'] for x in tests] == ['finding-specific'] * 6 +
       ['historical-root-regression'] * 13 + ['cross-cutting-contract'] * 5 +
       ['documentary-scope-or-authorization-gate'] * 2, 'B10 plan kinds/order mismatch')
    ck([x['finding_ids'] for x in features[:3]] == [x['id'] for x in new] and
       [x['finding_ids'] for x in features[3:16]] == [x['finding_ids'] for x in extensions] and
       {x['finding_ids'] for x in extensions} == EXTENDED_FINDINGS,
       'B10 new-feature/extension mapping mismatch')
    for row in extensions:
        ck(row['followup_policy'] == 'unchanged-during-partial7', 'B10 hidden followup replan: ' + row['id'])
    for row in rc:
        v.related([row], fids, 'feature_ids')
        v.related([row], tids, 'acceptance_ids')
        expected = [t['id'] for t in tests if set(t['feature_ids'].split(';')) & set(row['feature_ids'].split(';'))]
        ck(row['acceptance_ids'].split(';') == expected and bool(expected), 'B10 RC plan links mismatch: ' + row['id'])
        roots = {root for f in features if f['id'] in row['feature_ids'].split(';')
                 for root in f['finding_ids'].split(';')}
        ck(set(row['finding_ids'].split(';')) <= roots, 'B10 RC roots not in features: ' + row['id'])
    v.related(tables['Q7B10-'], {x['id'] for x in tables['H7B10-']}, 'handoff_ids')
    for row in tables['H7B10-']:
        ck(row['status'] == 'external-contract-or-policy-unresolved-not-absence-proof', 'B10 handoff falsely resolved: ' + row['id'])
    for row in tables['Q7B10-']:
        ck(row['status'] == 'unanswered-no-secrets-requested', 'B10 question falsely resolved: ' + row['id'])
    for n, row in enumerate(tables['BK7B10-'], 1):
        ck(row['prior_backlog_id'] == f'BK7B9-{n:02d}' and row['original_backlog_id'] == f'BK7-{n:02d}' and
           row['part'] in {'7B11', '7C', '7B11/7C'} and row['status'] != 'complete',
           'B10 backlog origin/part/closure mismatch: ' + row['id'])
    ck([x['status'] for x in tables['BK7B10-'][2:6]] == ['not-started'] * 4, 'B10 accidentally starts7C')

    labelled = [(str(n), rows('review-scope.csv' if n == 1 else f'review-scope-{n:02d}.csv'))
                for n in range(1, 7)] + [('7A', rows('review-scope-07.csv'))]
    labelled += [(f'7B{n}', rows(f'review-scope-07B{n}.csv')) for n in range(1, 10)] + [('7B10', scopes)]
    ck(rows('evidence/coverage-ledger-07B10.csv') == build_current_ledger(inventory, labelled, v.spans),
       'B10 ledger recomputation mismatch')
    candidates = rows('evidence/report-candidate-disposition-07B10.csv')
    screens = rows('evidence/report-screen-disposition-07B10.csv')
    ck(len(candidates) == 98 and candidates == build_candidate_disposition(inventory, labelled), 'B10 filename98 triage mismatch')
    ck(len(screens) == 52 and screens == build_screen_disposition(inventory, labelled), 'B10 screen52 triage mismatch')
    v.sequential(screens, 'SC7B10-', 52)
    by_screen = {x['screen']: x for x in screens}
    for name in REVIEWED_BODIES:
        ck(by_screen[name]['phase7B10_body_ranges'] != 'none' and
           by_screen[name]['coverage_level'] == 'bounded-local-body-and-xaml-not-whole-feature-certified',
           'B10 local body incorrectly deferred/promoted: ' + name)
    ck(by_screen['frmInvBySalesMen']['selection_basis'] == 'explicit-nonregex-source-candidate-not-a-feature-claim',
       'B10 changes filename triage into a feature inventory')
    prior = {x['path'] for _, selected in labelled[:-1] for x in selected}
    selected = set(scope)
    union = prior | selected
    ck((len(prior), len(selected), len(selected & prior), len(selected - prior), len(union), len(paths - union)) ==
       (375, 23, 17, 6, 381, 446), 'B10 scope union bookkeeping mismatch')

    witness, match = v.recompute('evidence/report-witnesses-07B10.json', 'tools/check_salesman_contract_witnesses.py')
    alg, lex = witness['illustrations'], witness['static_lexical_contract_checks']
    v.sequential(alg, 'ALG7B10-', 20)
    v.sequential(lex, 'ST7B10-', 20)
    v.related(alg + lex, known)
    for error in witness_metadata_errors(witness):
        ck(False, error)
    for row in alg + lex:
        flag = 'illustration_assertions_passed' if row['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(row[flag] is True and row['source_application_executed'] is False and bool(row['limit']),
           'B10 witness fail/overclaim: ' + row['id'])
        validate_source(v, row, scope)
    for row in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{row["path"]}:{row["start"]}-{row["end"]}', scope, 'B10 bounded lexical read', phase=7)

    patterns = [
        ('PHASE-07B10.md', r'^\| (EX7B10-\d{2}) \|', [x['id'] for x in extensions]),
        ('SALESMAN-REPORT-CONTRACTS-07B10.md', r'^\| (FE7B10-\d{2}) —', [x['id'] for x in features]),
        ('SALESMAN-REPORT-CONTRACTS-07B10.md', r'^\| (INV7B10-\d{2}) \|', [x['id'] for x in invariants]),
        ('SALESMAN-REPORT-CONTRACTS-07B10.md', r'^### (RC7B10-\d{2}) —', [x['id'] for x in rc]),
        ('SALESMAN-REPORT-CONTRACTS-07B10.md', r'^\| (H7B10-\d{2}) —', [x['id'] for x in tables['H7B10-']]),
        ('SALESMAN-REPORT-CONTRACTS-07B10.md', r'^\| (Q7B10-\d{2}) \|', [x['id'] for x in tables['Q7B10-']]),
        ('SALESMAN-REPORT-CONTRACTS-07B10.md', r'^\| (BK7B10-\d{2}) \|', [x['id'] for x in tables['BK7B10-']]),
        ('VALIDATION-07B10.md', r'^\| (P7B10T-\d{2}) \|', [x['id'] for x in tests]),
        ('IMPROVEMENTS.md', r'^\| (G-\d{2,3}) \|', [f'G-{n:02d}' for n in range(1, 141)]),
    ]
    for filename, pattern, expected in patterns:
        ck(re.findall(pattern, v.read(v.AUDIT / filename), re.M) == expected,
           'B10 Markdown ID/order mismatch: ' + filename)
    pending = False
    source_pattern = re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS + SHARED_DOCS:
        doc = v.AUDIT / filename
        content = v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', content):
            parsed = urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):
                continue
            target = (doc.parent / unquote(parsed.path)).resolve()
            if target == (v.AUDIT / 'evidence/checks-07B10.json').resolve() and not target.exists():
                pending = True
                continue
            v.LINK_COUNT += 1
            ck(target.exists(), 'Broken B10 link in ' + filename + ':' + m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1], m[2], filename)
            if filename in PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a, b in v.spans(m[2])), scope, filename, phase=7)
        for pattern, ids in ((r'\bP7B10T-\d{2}\b', tids), (r'\bFE7B10-\d{2}\b', fids), (r'\bINV7B10-\d{2}\b', iids)):
            for item in re.findall(pattern, content):
                ck(item in ids, 'Unknown B10 ID in ' + filename + ':' + item)
    summary = {}
    for line in v.read(v.AUDIT / 'README.md').splitlines():
        if line.startswith('|'):
            fields = [x.strip() for x in line.replace('**', '').strip('|').split('|')]
            summary[fields[0]] = fields[1:]
    for label, expected in (('التراكمي المفتوح', [285, 2, 175, 107, 1]),
                            ('7B10 — جديدة', [3, 0, 0, 3, 0]),
                            ('7B10 — إضافة محدودة', [23, 17, 6, 381])):
        ck(summary.get(label) == list(map(str, expected)), 'Current B10 README numeric mismatch: ' + label)
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'], v.read(v.AUDIT / 'IMPROVEMENTS.md')):
        ck(False, error)
    for name in SHARED_DOCS:
        ck(all(x in v.read(v.AUDIT / name) for x in ('PHASE-07B10.md', '7B11', '7C', 'غير مأذونة', 'a2541ed', '10ba215')),
           'Current index lacks B10/B11/C/8/source-checkout boundary: ' + name)
    tools = ['check_salesman_contract_witnesses.py', 'validate_salesman_contract_part.py', 'test_salesman_contract_audit_validator.py']
    for name in tools:
        try:
            v.ast.parse(v.read(v.AUDIT / 'tools' / name), filename=name)
        except SyntaxError as error:
            ck(False, 'B10 audit-tool syntax: ' + name + ':' + str(error))
    process = v.subprocess.run([v.sys.executable, '-B', str(v.AUDIT / 'tools/test_salesman_contract_audit_validator.py')],
                               cwd=v.ROOT, capture_output=True, text=True, timeout=30)
    m = re.search(r'Ran (\d+) tests? in ', process.stderr + '\n' + process.stdout)
    count = int(m[1]) if m else None
    passed = process.returncode == 0 and count == 28
    ck(passed, 'B10 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_salesman_contract_audit_validator.py'] = dict(
        tests_reported=count, expected_tests=28, process_exit_code=process.returncode,
        result='passed' if passed else 'failed-or-unrecognized', erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked'] += tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update(
        {'tools/' + name: v.sha(v.AUDIT / 'tools' / name) for name in ['validate_audit.py'] + tools})
    report.update(
        validation_scope='current-through7B10-285-plus-frozen-history-not-runtime-certification',
        phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9+7B10-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B11-announced-not-started', '7C-not-started'],
        registry_used='findings.csv', historical_artifact_sha256=prov['historical_artifact_sha256'],
        date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=113, phase_7B10=3, total_open_not_remediated=285,
                              severity=dict(collections.Counter(x['severity'] for x in current)),
                              certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE: 23, 'phase_7B9_union_frozen': 375,
                                  'phase_7B10_overlap_with_prior_union': 17, 'phase_7B10_new_paths': 6,
                                  'unique_union_not_line_or_execution_coverage': 381,
                                  'inventory_only_no_selected_scope': 446})
    report['phase_7B9_historical_evidence'] = dict(
        frozen_registry=SNAPSHOT, frozen_registry_sha256_matches=v.sha(v.AUDIT / SNAPSHOT) == SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT, earlier_report_evidence_artifacts_hash_checked=292,
        historical_check_record_overwritten=False, genuine_b9_check_sha256_unchanged=B9_CHECK_SHA,
        partial7B10_append_only_evidence_extensions_without_reclassification=ext,
        next_phase_followups_preserved_for_all282=True, next_phase_replans_during_partial7={},
        historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True)
    report['phase_7B10_entry_checkout_reconciliation'] = reconcile
    report['evidence_rows'].update(dict(
        phase_7B10_feature_rows_not_completed_features=23, phase_7B10_invariants_not_passed_tests=23,
        phase_7B10_reconciliation_contracts_not_executed_financial_acceptance=6,
        phase_7B10_unexecuted_acceptance_or_gate_plans=26, phase_7B10_direct_finding_plans=6,
        phase_7B10_historical_regression_plans=13, phase_7B10_cross_contract_plans=5,
        phase_7B10_documentary_scope_authorization_gate_plans=2,
        phase_7B10_historical_extensions_not_new_findings=13, phase_7B10_unresolved_handoffs=6,
        phase_7B10_unanswered_questions=6, phase_7B10_continuation_groups_not_complete=10,
        phase_7B10_original_paths_in_ledger=827, phase_7B10_filename_candidates_not_feature_count=98,
        phase_7B10_screen_candidates_not_feature_count=52,
        phase_7B10_independent_illustrations_not_erp_tests=20,
        phase_7B10_bounded_literal_checks_not_application_tests=20,
        phase_7B10_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder'] = pending
    report['validation']['limit'] = (
        'Read-only documentation checker: original827 path/hash identity plus source10ba ancestry/net docs-only delta; '
        'protected292 historical artifacts including genuine B9 stdout checkout3612700 and all old helpers/reports; '
        'exact282 historical cores/ALLnext_phase/evidence prefixes with13 declared tails; exactG01..134 rows. '
        'All historical A/B1..B9 get their OWN frozen registry/exact shared texts IN MEMORY, never current285/live indexes; '
        'current metadata is not archived byte replay or whole-history attestation. Entrya254 is the already completed '
        'B9 documentation push, reconciled by exact297 bytes, not a new push/reset/rebaseline. '
        '23 selected paths/three bodies+XAML are not every caller/child/template/schema/ACL/deployment. '
        'B1 profit/movement findings are rechecked, not renumbered. Salesman worker/WPF gate P7-054 precedes '
        'population/arithmetic; downstream manual contrasts explicitly isolate it, never assume its remediation. '
        'Notes-vs-CreditDeptNotes is a confirmed LOCAL reader/writer/supplied-schema mismatch, not proof no deployed '
        'view/synonym exists; alias must resolve before data/deletion/time consequences are evaluated. '
        'Unsigned value-vs-signed commissions and all-period mixed-source membership are distinct from print-bridge '
        'summary loss, endpoint cutoff, failed parsing and post-query criteria drift. Fixed115, saved-VAT flag, '
        'unit/cost, stale item id, branch, navigation and failures retain old roots. '
        'ClosedXML typed XLSX cells and helper return/dispose before shell are counterevidence to copying CSV '
        'escaping/formula/finalization claims here; IsPostpone binding matches DTO. N+1/Fill/no paging are leads '
        'not measured latency/leak/index judgments.20 manual+20 bounded lexical observations and28 new synthetic '
        'checker cases are documentary only;26 ERP/contract/gate plans remain not-executed. '
        '7B/7 partial,7B11 announced,7C not started,8 unauthorized. No application import/build/C#/SQL/WPF/Office/'
        'formula/device/provider/process/shell/actual export IO execution, remediation, real data/secrets or '
        'financial/security/compliance/whole-feature certification.'
    )
