#!/usr/bin/env python3
"""PARTIAL7B15/B-R2 DOCUMENTATION checks; NEVER ERP or financial acceptance.

413 prior artifacts/294 immutable cores/ALLnext_phase/exactG01..164 protected.
Historical B14 receives OWN294 rows, original noBOM/CRLF bytes and exact three
index texts IN MEMORY. No protected helper edit/global pathlib patch/disk
overlay/rebaseline/archive rewrite. Both parent C# bodies were already full in
7A/B1; two own-XAML/contract upgrades are NOT two first C# reviews. Selected
child slices do not inherit parent depth; Home tax route is frmVATReturn, not
this local parent. R1/R2 residuals explicit; R3/R4 proposed, C unstarted,
8 unauthorized. No application import/build/execution/measurement/remediation.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
import csv
import io
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
from validate_financial_report_part import historical_b1_inputs, registry_transition_errors, bidirectional_errors
from validate_inventory_activity_part import (
    build_current_ledger as prior_ledger, build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens, feature_level_errors, arithmetic_erratum_errors,
)

SCOPE_FILE = 'review-scope-07B15.csv'
PART_DOCS = ('PHASE-07B15.md', 'ACCRUAL-TAX-CONTRACTS-07B15.md', 'VALIDATION-07B15.md', 'PHASE-07-REMAINING-07B15.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
SNAPSHOT = 'evidence/findings-through-07B14.csv'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B14.json'
SNAPSHOT_SHA = '8cd8fdbcee2d522dae32a561f9b41460b1c4b0ddf9ca2d38763015677ffadf16'
SHARED_SHA = 'ae628ed72893c00310314fe239c0c6934324321ec94c5265e43dde964f744a5e'
PROVENANCE_SHA = 'ac4977145152f1c787dd2e4fd9f414b49789c204dabfc21c99222349354323cf'
B14_CHECK_SHA = 'e9d795dde67e358e9b03e46b449a6314e9cff3613a254e832cb433ed789c655a'
PRIOR_PROVENANCE_SHA = '61b8daf25450653ba70b5a425395573fcfcd0af66506510362cee3c5c48655ac'
ENTRY_CHECKOUT = '789b04cb485948aa89e153f4b501efa27164c109'
REVIEWED_BODIES = ('FrmReseved', 'frmTaxRptPeriod')
EXTENDED_FINDINGS = {
    'P1-004', 'P1-011', 'P1-013', 'P1-030', 'P2-001', 'P2-010',
    'P3-002', 'P3-003', 'P3-005', 'P3-006', 'P3-007', 'P3-023',
    'P7-001', 'P7-002', 'P7-003', 'P7-031', 'P7-032', 'P7-043',
    'P7-044', 'P7-045', 'P7-046', 'P7-051',
}
TABLE_SPECS = (
    ('acceptance-tests', 'P7B15T-', 36), ('feature-implementation-matrix', 'FE7B15-', 32),
    ('report-invariants', 'INV7B15-', 32), ('report-reconciliation', 'RC7B15-', 6),
    ('historical-extensions', 'EX7B15-', 22), ('handoffs', 'H7B15-', 6),
    ('questions', 'Q7B15-', 6), ('continuation-backlog', 'BK7B15-', 10),
    ('root-adjudication', 'AD7B15-', 10),
)
SENTINELS = {
    'FE7B15-31', 'FE7B15-32', 'INV7B15-31', 'INV7B15-32', 'RC7B15-06',
    'H7B15-06', 'Q7B15-06', 'P7B15T-35', 'P7B15T-36', 'ALG7B15-24', 'AD7B15-10',
}


@contextmanager
def historical_b14_inputs(v, frozen294, texts, raw):
    """Exact logical path only; copied rows/indexes; restore normal/nested/error exit."""
    if len(frozen294) != 294 or len({r['id'] for r in frozen294}) != 294:
        raise ValueError('Exactly294 distinct historical rows required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as e:
        raise ValueError('Malformed frozen registry') from e
    if parsed != frozen294 or raw.count(b'\r\n') != 295 or b'\n' in raw.replace(b'\r\n', b''):
        raise ValueError('Frozen294 rows/bytes/CRLF disagree')
    original = v.AUDIT
    target = Path(original / 'findings.csv').resolve()

    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve() == target else super().read_bytes()

    try:
        v.AUDIT = FrozenRegistryPath(original)
        with historical_b1_inputs(v, frozen294, texts):
            yield
    finally:
        v.AUDIT = original


def validate_frozen_b14(v, report, prior, frozen291, prov, frozen294):
    ck = v.check
    for p, digest in [
        ('evidence/provenance-07B15.json', PROVENANCE_SHA), (SNAPSHOT, SNAPSHOT_SHA),
        (SHARED_SNAPSHOT, SHARED_SHA), ('evidence/checks-07B14.json', B14_CHECK_SHA),
    ]:
        ck(v.sha(v.AUDIT / p) == digest, 'B15 immutable entry identity: ' + p)
    ck(prov['registry_at_entry_snapshot'] == SNAPSHOT and prov['registry_at_entry_sha256'] == SNAPSHOT_SHA
       and prov['shared_indexes_at_entry'] == SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256'] == SHARED_SHA,
       'B15 snapshot context')
    for p, digest in prior['historical_artifact_sha256'].items():
        ck(prov['historical_artifact_sha256'].get(p) == digest, '387-to413 continuity: ' + p)
    saved = v.json.loads(v.read(v.AUDIT / 'evidence/checks-07B14.json'))
    ck(saved['checkout_head'] == '461ceaf3e14e67e1c5b3f97a202d874746f6523f'
       and saved['findings']['total_open_not_remediated'] == 294 and saved['original_project_hashes_matching'] == 827
       and saved['validation']['errors'] == [] and saved['historical_artifact_sha256'] == prior['historical_artifact_sha256']
       and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False,
       'B14 genuine stdout changed')
    ck(prov['genuine_B14_check_sha256'] == B14_CHECK_SHA and prov['prior_provenance_B14_sha256'] == PRIOR_PROVENANCE_SHA
       and prov['genuine_B14_check_record_checkout'] == saved['checkout_head'], 'B15 prior stdout/provenance identity')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY_CHECKOUT,
       'B15 completed B14 push/entry identity')
    ck(prov['phase7B14_entry_consistency'] == dict(
        original_hashes_matching=827, findings=294,
        phase_7_delivery='7A+' + '+'.join('7B' + str(n) for n in range(1, 15)) + '-partial-not-complete7B-or7',
        audit_file_count=418, errors=[], erp_runtime_tests_executed=0), 'B15 prior delivery context')
    from validate_inventory_activity_part import extend_inventory_activity
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    with historical_b14_inputs(v, frozen294, texts, (v.AUDIT / SNAPSHOT).read_bytes()):
        extend_inventory_activity(v, report, prior, frozen291)
    report.update(registry_used=SNAPSHOT, validation_scope='historical-through7B14-294-not-current-state',
                  phase_7B14_historical_input_mode='frozen294-rows-and-exact-CRLF-bytes-and-exact-indexes-in-memory')
    report['phase_7B14_adapter_context'] = dict(
        entry_provenance='evidence/provenance-07B15.json', adapter_protected_artifacts_checked=413,
        current_registry_and_shared_indexes_not_inputs=True, archived_stdout_not_rewritten_after_push=True)


def build_current_ledger(inventory, labelled, spans):
    out = prior_ledger(inventory, labelled, spans)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B15' for r in s}
    for r in out:
        r['phase7B15_ranges'] = selected.get(r['path'], 'none')
        if r['inventory_kind'] != 'generated-artifact':
            r.update(continuation_bucket='7B16-or-7C-contract-or-reasoned-exclusion-not-closed',
                     next_scope_work='R1/R2 محليات مع بقايا مسماة إلىR3/R4؛ التالي7B16/R3 مقترح. لا whole-feature منbody/XAML ولا child كامل من مقاطع الوالد. أربع حزمB وستة محاورC غير مبدوءة ليست جلسات أو نسباً؛8 غير مأذونة.')
    return out


def build_candidate_disposition(inventory, labelled):
    out = prior_candidates(inventory, labelled)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B15' for r in s}
    for r in out:
        r['phase7B15_ranges'] = selected.get(r['path'], 'none')
        if not r['disposition'].startswith('lexical-false-positive'):
            r.update(disposition='7B16-further-contract-or-reasoned-exclusion-required',
                     reason='98 مرشح اسم لا تعداد قدرات. والدان محليان يكملان own-XAML وعقوداً؛ C# لهما كامل سابقاً7A/B1. زوال الفئة القديمة لا يغلقR1/R2 أو caller/child/template/schema/ACL؛ R3/R4 بقيود صريحة.')
    return out


def build_screen_disposition(inventory, labelled):
    out = prior_screens(inventory, labelled)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B15' for r in s}
    full = {r['path']: '1-' + str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    for n, r in enumerate(out, 1):
        r['id'] = f'SC7B15-{n:02d}'
        r['phase7B15_body_ranges'] = selected.get(r['body_path'], 'none')
        r['disposition'] = '7B16-or-7C-further-contracts-or-reasoned-exclusion-required'
        if r['screen'] in REVIEWED_BODIES and all(p in full and selected.get(p) == full[p] for p in (r['path'], r['body_path'])):
            r['coverage_level'] = 'bounded-local-body-and-xaml-not-whole-feature-certified'
            r['reason'] = 'B15 يكمل own-XAML والعقود المحلية؛ C# للوالدين كامل سابقاً7A/B1 لا أول قراءة. الطفل منتقى لا يرث العمق. Home tax يفتحfrmVATReturn، لا شهادة وصول هذا الوالد أو اكتمالfeature/REPX/schema/ACL.'
        else:
            r['reason'] = 'تصنيف عمق محدود لا مقام اكتمال. خارج الترقيتين المحليات تبقى capability/contract أو استبعاد مسند؛ لا بدء7C أو إغلاقR1/R2 من زوال فئة قديمة.'
    return out


def depth_clarification(inventory, labelled, spans):
    before = [(k, s) for k, s in labelled if k != '7B15']
    old = prior_screens(inventory, before)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B15' for r in s}
    full_ranges = {r['path']: '1-' + str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    out = []
    for r in old:
        if r['coverage_level'] != 'prior-selected-slices-depth-not-upgraded':
            continue
        full = '1-' + str(r['body_inventory_lines'])
        phases = [k for k, s in before if any(x['path'] == r['body_path'] and x['ranges'] == full for x in s)]
        upgraded = r['screen'] in REVIEWED_BODIES and all(p in full_ranges and selected.get(p) == full_ranges[p] for p in (r['path'], r['body_path']))
        out.append(dict(id=f'DEP7B15-{len(out)+1:02d}', screen=r['screen'], body_path=r['body_path'],
                        prior_category=r['coverage_level'], prior_full_local_csharp_declared='true' if phases else 'false',
                        prior_full_body_scope_ids=';'.join(phases) or 'none', b15_full_local_body_and_xaml='true' if upgraded else 'false',
                        remaining_old_category_after_b15='false' if upgraded else 'true',
                        interpretation='فئتان قديمتان لهما C# كامل سابقاً؛ ترقيتاown-XAML/عقود تتركان0 في الفئة فقط، لا0 عقد متبق أو أول قراءتيC# أو إغلاق7B.', runtime_status='not-executed'))
    return out


def remaining_work_errors(plan, depth):
    errors = []
    if len(plan) != 10 or collections.Counter(r.get('part_family') for r in plan) != {'7B': 4, '7C': 6}:
        errors.append('Retain4 B planning groups with R1/R2 residuals and6 unstarted C axes')
    expected = ['bounded-parent-contract-delivered-residuals-open'] * 2 + ['planned-not-started'] * 8
    for n, r in enumerate(plan):
        for field in ('id', 'part_family', 'title', 'candidate_scope_not_certified', 'expected_deliverable', 'static_exit_criterion', 'dependencies_and_uncertainty'):
            if not isinstance(r.get(field), str) or not r[field].strip():
                errors.append('Remaining work missing substantive field: ' + str(r.get('id', '?')) + '.' + field)
        if r.get('status') != expected[min(n, 9)] or r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false':
            errors.append('Remaining work overclaim: ' + str(r.get('id', '?')))
    if [r.get('part_family') for r in plan] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('Remaining work family/order')
    if len(depth) != 2 or sum(r.get('prior_full_local_csharp_declared') == 'true' for r in depth) != 2 or sum(r.get('b15_full_local_body_and_xaml') == 'true' for r in depth) != 2 or any(r.get('remaining_old_category_after_b15') != 'false' for r in depth):
        errors.append('Two old categories/two prior full CSharp/two upgrades/zero category is not whole-feature closure')
    return errors


def group_row_errors(previous, current):
    rows = lambda t: re.findall(r'^\| G-\d{2,3} \|.*$', t, re.M)
    return [] if len(rows(previous)) == 164 and rows(current)[:164] == rows(previous) else ['Historical G01–164 rows changed']


def witness_metadata_errors(w):
    errors = []
    for k in ('application_code_imported_or_executed', 'application_remediation_performed', 'real_business_or_secret_data_used', 'spreadsheet_or_formula_interpreter_executed'):
        if w.get(k) is not False:
            errors.append('B15 false-only flag: ' + k)
    for k in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
        if type(w.get(k)) is not int or w[k] != 0:
            errors.append('B15 integer-zero count: ' + k)
    for k in ('parents_csharp_already_full_7A_B1', 'child_selected_slices_not_parent_depth', 'tax_home_route_is_alternate_not_parent_certified', 'B_R1_R2_residual_contracts_not_closed', 'supplied_sql_not_certified_deployed', 'progress_categories_not_wholly_unread_counts'):
        if w.get(k) is not True:
            errors.append('B15 boundary: ' + k)
    for k in ('illustration_count', 'static_lexical_contract_check_count'):
        if type(w.get(k)) is not int or w[k] != 24:
            errors.append('B15 count: ' + k)
    if w.get('phase') != '7B15-partial-static-audit':
        errors.append('B15 witness phase')
    if w.get('parent_source_lines_not_first_coverage') != dict(csharp=1876, xaml=1441, total=3317):
        errors.append('B15 parent line accounting, not first CSharp reviews')
    return errors + arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def plan_structure_errors(tests, new_ids, extensions):
    errors = []
    expected = ['finding-specific'] * 8 + ['historical-root-regression'] * 22 + ['cross-cutting-contract'] * 4 + ['documentary-scope-or-authorization-gate'] * 2
    if [r.get('plan_kind') for r in tests] != expected:
        errors.append('B15 plan-kind/count/order')
    if any(r.get('status') != 'not-executed' for r in tests):
        errors.append('B15 acceptance not executed')
    if len(new_ids) != 4 or len(set(new_ids)) != 4:
        errors.append('B15 four distinct new roots')
    for n, fid in enumerate(new_ids, 1):
        direct = [r for r in tests if r.get('plan_kind') == 'finding-specific' and r.get('finding_ids') == fid]
        if len(direct) != 2:
            errors.append('B15 two direct plans: ' + fid)
        if any(r.get('feature_ids') != f'FE7B15-{n:02d}' or r.get('invariant_ids') != f'INV7B15-{n:02d}' for r in direct):
            errors.append('B15 direct root/feature/invariant mapping: ' + fid)
    if [r.get('finding_ids') for r in tests if r.get('plan_kind') == 'historical-root-regression'] != [r['finding_ids'] for r in extensions]:
        errors.append('B15 historical plan/manifest order')
    return errors


def adjudication_errors(data):
    errors = []
    if len(data) != 10 or [r.get('decision') for r in data[:4]] != ['new-local-root'] * 4:
        errors.append('B15 adjudication count/direct-root decisions')
    if [r.get('current_root_ids') for r in data[:4]] != [f'P7-{n}' for n in range(123, 127)]:
        errors.append('B15 adjudication new-root order')
    for r in data:
        if r.get('comparison_depth') != 'all294-titles-classifications-evidence-paths-plus-selected-nearest-chains-not-all-historical-chains':
            errors.append('B15 historical comparison depth overclaim')
        if not r.get('nearest_prior_root_ids') or not isinstance(r.get('reason'), str) or not r['reason'].strip():
            errors.append('B15 adjudication lacks nearest roots/reason')
        if r.get('runtime_status') != 'not-executed':
            errors.append('B15 adjudication runtime overclaim')
    return errors


def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == 'none-inventory-only':
        v.check(row['id'] in SENTINELS, 'B15 undeclared no-source sentinel: ' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B15 fabricated inventory evidence: ' + row['id'])
        v.evidence(row['evidence'], row['id'])
        v.scoped_evidence(row['evidence'], scope, row['id'] + ' boundedB15', phase=7)


def extend_accrual_tax(v, report, prov, frozen294):
    ck, rows = v.check, v.rows
    current = rows('findings.csv')
    new = current[294:]
    extensions = rows('evidence/historical-extensions-07B15.csv')
    ck(prov['historical_artifact_count'] == 413 and len(frozen294) == 294, 'B15 entry count')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY_CHECKOUT, 'B15 entry checkout')
    ck(prov['erp_runtime_tests_executed'] == 0 and prov['sql_or_external_service_tests_executed'] == 0
       and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False, 'B15 execution/remediation boundary')
    identity = report['source_reference_validation']
    ck(identity['audited_application_reference'] == v.HEAD and identity['reference_ancestor_of_checkout'] is True
       and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching'] == 827, 'B15 source identity')
    ext = v.transition(frozen294, current, 7, EXTENDED_FINDINGS, preserve_followups=True)
    for error in registry_transition_errors(frozen294, current, extensions):
        ck(False, error)
    ck(len(current) == len({r['id'] for r in current}) == 298 and [r['id'] for r in new] == [f'P7-{n}' for n in range(123, 127)], 'B15 registry/newIDs')
    v.distributions(new, {'High': 2, 'Medium': 2}, {'confirmed': 4}, 'boundedB15 only')
    for r in new:
        ck(r['type'] == 'implementation-defect' and r['status'] == 'open-not-remediated' and r['next_phase'] == '8', 'B15 finding state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$', v.read(v.AUDIT / PART_DOCS[0]), re.M) == [(r['id'], r['title']) for r in new], 'B15 headings/registry')
    raw = (v.AUDIT / 'findings.csv').read_bytes()
    ck(not raw.startswith(b'\xef\xbb\xbf') and raw.count(b'\r\n') == 299 and b'\n' not in raw.replace(b'\r\n', b''), 'B15 noBOM/CRLF registry')
    selected = rows(SCOPE_FILE)
    scope = {r['path']: v.spans(r['ranges']) for r in selected}
    inventory = rows('evidence/inventory.csv')
    paths = {r['path'] for r in inventory}
    ck(len(selected) == len(scope) == 20, 'B15 selected count')
    for r in selected:
        ck(r['path'] in paths and r['review_state'] == 'selected-static-source-slices-not-runtime-certified' and bool(r['focus']), 'B15 scope: ' + r['path'])
        v.source_ref(r['path'], r['ranges'], SCOPE_FILE)
    for r in new:
        validate_source(v, r, scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml', '.xaml.cs'):
            p = 'SmartAuditERP/Form_WPF/' + name + suffix
            ck(scope.get(p) == [(1, len(v.read(v.ROOT / p).splitlines()))], 'B15 own local body/XAML: ' + p)
    child = 'SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml'
    for p in (child, child + '.cs'):
        ck(p in scope and scope[p] != [(1, len(v.read(v.ROOT / p).splitlines()))], 'B15 child slices must not be promoted to full body/XAML')
    known = {r['id'] for r in current} | {f'H7B15-{n:02d}' for n in range(1, 7)}
    tables = {}
    for name, prefix, count in TABLE_SPECS:
        data = rows('evidence/' + name + '-07B15.csv')
        tables[prefix] = data
        v.sequential(data, prefix, count)
        v.related(data, known)
        for r in data:
            for k, value in r.items():
                ck(bool(value), 'B15 incomplete cell: ' + r['id'] + '.' + k)
            validate_source(v, r, scope)
            if 'runtime_status' in r:
                ck(r['runtime_status'] == 'not-executed', 'B15 runtime overclaim')
    tests, features, invs, rc = [tables[k] for k in ('P7B15T-', 'FE7B15-', 'INV7B15-', 'RC7B15-')]
    tids, fids, iids = [{r['id'] for r in pool} for pool in (tests, features, invs)]
    v.proposed_tests(tests, '7B15')
    v.related(tests, fids, 'feature_ids')
    v.related(tests, iids, 'invariant_ids')
    v.related(features + invs, tids, 'acceptance_ids')
    for pool, field in ((features, 'feature_ids'), (invs, 'invariant_ids')):
        for error in bidirectional_errors(pool, tests, field):
            ck(False, error)
    for error in feature_level_errors(features) + plan_structure_errors(tests, [r['id'] for r in new], extensions):
        ck(False, error)
    for pool, label in ((tests, 'plans'), (features, 'features'), (invs, 'invariants')):
        v.covered(new, pool, 'B15 ' + label)
    ck({r['finding_ids'] for r in extensions} == EXTENDED_FINDINGS
       and [r['finding_ids'] for r in features[4:26]] == [r['finding_ids'] for r in extensions], 'B15 exact extension mapping')
    for r in extensions:
        ck(r['followup_policy'] == 'unchanged-during-partial7', 'B15 hidden replan')
    for r in rc:
        v.related([r], fids, 'feature_ids')
        v.related([r], tids, 'acceptance_ids')
        expected = [t['id'] for t in tests if set(t['feature_ids'].split(';')) & set(r['feature_ids'].split(';'))]
        ck(r['acceptance_ids'].split(';') == expected and bool(expected), 'B15 RC reverse links')
    v.related(tables['Q7B15-'], {r['id'] for r in tables['H7B15-']}, 'handoff_ids')
    for r in tables['H7B15-']:
        ck(r['status'] == 'external-contract-or-policy-unresolved-not-absence-proof', 'B15 handoff')
    for r in tables['Q7B15-']:
        ck(r['status'] == 'unanswered-no-secrets-requested', 'B15 question')
    for n, r in enumerate(tables['BK7B15-'], 1):
        ck(r['prior_backlog_id'] == f'BK7B14-{n:02d}' and r['original_backlog_id'] == f'BK7-{n:02d}' and r['status'] != 'complete', 'B15 backlog ancestry')
    ck([r['status'] for r in tables['BK7B15-'][2:6]] == ['not-started'] * 4, 'B15 accidentally startsC')
    ad = tables['AD7B15-']
    v.related(ad, known, 'current_root_ids')
    v.related(ad, known, 'nearest_prior_root_ids')
    for error in adjudication_errors(ad):
        ck(False, error)
    labelled = [(str(n), rows('review-scope.csv' if n == 1 else f'review-scope-{n:02d}.csv')) for n in range(1, 7)]
    labelled += [('7A', rows('review-scope-07.csv'))] + [(f'7B{n}', rows(f'review-scope-07B{n}.csv')) for n in range(1, 15)] + [('7B15', selected)]
    ck(rows('evidence/coverage-ledger-07B15.csv') == build_current_ledger(inventory, labelled, v.spans), 'B15 ledger')
    candidates = rows('evidence/report-candidate-disposition-07B15.csv')
    screens = rows('evidence/report-screen-disposition-07B15.csv')
    ck(len(candidates) == 98 and candidates == build_candidate_disposition(inventory, labelled), 'B15 filename triage')
    ck(len(screens) == 52 and screens == build_screen_disposition(inventory, labelled), 'B15 screen triage')
    v.sequential(screens, 'SC7B15-', 52)
    ck(collections.Counter(r['coverage_level'] for r in screens) == {
        'bounded-local-body-and-xaml-not-whole-feature-certified': 33,
        'bounded-local-body-and-selected-xaml-not-whole-feature-certified': 19}, 'B15 33/19/zero-old are not whole-feature counts')
    before = {r['path'] for _, s in labelled[:-1] for r in s}
    selected_paths = set(scope)
    ck((len(before), len(selected_paths & before), len(selected_paths - before), len(before | selected_paths), len(paths - (before | selected_paths))) == (392, 17, 3, 395, 432), 'B15 union bookkeeping')
    depth = rows('evidence/report-depth-clarification-07B15.csv')
    plan = rows('evidence/remaining-workplan-07B15.csv')
    v.sequential(depth, 'DEP7B15-', 2)
    v.sequential(plan, 'RW7B15-', 10)
    ck(depth == depth_clarification(inventory, labelled, v.spans), 'B15 depth clarification')
    for error in remaining_work_errors(plan, depth):
        ck(False, error)
    witness, match = v.recompute('evidence/report-witnesses-07B15.json', 'tools/check_accrual_tax_witnesses.py')
    alg, lex = witness['illustrations'], witness['static_lexical_contract_checks']
    v.sequential(alg, 'ALG7B15-', 24)
    v.sequential(lex, 'ST7B15-', 24)
    v.related(alg + lex, known)
    for error in witness_metadata_errors(witness):
        ck(False, error)
    ck(witness['errors'] == [], 'B15 witness observations failed')
    for r in alg + lex:
        flag = 'illustration_assertions_passed' if r['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']), 'B15 witness overclaim')
        validate_source(v, r, scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}', scope, 'B15 bounded lexical read', phase=7)
    patterns = [
        (PART_DOCS[0], r'^\| (EX7B15-\d{2}) \|', [r['id'] for r in extensions]),
        (PART_DOCS[0], r'^\| (AD7B15-\d{2}) \|', [r['id'] for r in ad]),
        (PART_DOCS[1], r'^\| (FE7B15-\d{2}) —', [r['id'] for r in features]),
        (PART_DOCS[1], r'^\| (INV7B15-\d{2}) \|', [r['id'] for r in invs]),
        (PART_DOCS[1], r'^### (RC7B15-\d{2}) —', [r['id'] for r in rc]),
        (PART_DOCS[2], r'^\| (P7B15T-\d{2}) \|', [r['id'] for r in tests]),
        (PART_DOCS[3], r'^\| (DEP7B15-\d{2}) \|', [r['id'] for r in depth]),
        (PART_DOCS[3], r'^\| (RW7B15-\d{2}) \|', [r['id'] for r in plan]),
        ('IMPROVEMENTS.md', r'^\| (G-\d{2,3}) \|', [f'G-{n:02d}' for n in range(1, 171)]),
    ]
    for file, pattern, expected in patterns:
        ck(re.findall(pattern, v.read(v.AUDIT / file), re.M) == expected, 'B15 Markdown IDs: ' + file)
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
            if target == (v.AUDIT / 'evidence/checks-07B15.json').resolve() and not target.exists():
                pending = True
                continue
            v.LINK_COUNT += 1
            ck(target.exists(), 'B15 broken link: ' + name + ':' + m[1])
        for m in source.finditer(text):
            v.source_ref(m[1], m[2], name)
            if name in PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a, b in v.spans(m[2])), scope, name, phase=7)
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'], v.read(v.AUDIT / 'IMPROVEMENTS.md')):
        ck(False, error)
    for name in SHARED_DOCS:
        ck(all(t in v.read(v.AUDIT / name) for t in ('PHASE-07B15.md', 'PHASE-07-REMAINING-07B15.md', '7B16', 'غير مأذونة', '789b04c', '10ba215')), 'B15 current index boundary: ' + name)
    tools = ['check_accrual_tax_witnesses.py', 'validate_accrual_tax_part.py', 'test_accrual_tax_audit_validator.py']
    for name in tools:
        try:
            v.ast.parse(v.read(v.AUDIT / 'tools' / name), filename=name)
        except SyntaxError as e:
            ck(False, 'B15 syntax: ' + str(e))
    run = v.subprocess.run([v.sys.executable, '-B', str(v.AUDIT / 'tools/test_accrual_tax_audit_validator.py')], cwd=v.ROOT, capture_output=True, text=True, timeout=30)
    m = re.search(r'Ran (\d+) tests? in ', run.stderr + '\n' + run.stdout)
    count = int(m[1]) if m else None
    passed = run.returncode == 0 and count == 32
    ck(passed, 'B15 self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_accrual_tax_audit_validator.py'] = dict(
        tests_reported=count, expected_tests=32, process_exit_code=run.returncode, result='passed' if passed else 'failed-or-unrecognized', erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked'] += tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/' + n: v.sha(v.AUDIT / 'tools' / n) for n in ['validate_audit.py'] + tools})
    report.update(validation_scope='current-through7B15-298-plus-frozen-history-not-runtime-certification',
                  phase_7_delivery='7A+' + '+'.join('7B' + str(n) for n in range(1, 16)) + '-partial-not-complete7B-or7',
                  phase_7_remaining_parts=['7B16-proposed-R3-with-R1-R2-residuals-in-four-planning-groups-not-guaranteed-sessions', '7C-six-axes-not-started'],
                  registry_used='findings.csv', historical_artifact_sha256=prov['historical_artifact_sha256'], date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=126, phase_7B15=4, total_open_not_remediated=298,
                              severity=dict(collections.Counter(r['severity'] for r in current)), certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE: 20, 'phase_7B14_union_frozen': 392, 'phase_7B15_overlap_with_prior_union': 17,
                                  'phase_7B15_new_paths': 3, 'unique_union_not_line_or_execution_coverage': 395, 'inventory_only_no_selected_scope': 432})
    report['phase_7B14_historical_evidence'] = dict(
        frozen_registry=SNAPSHOT, frozen_registry_sha256_matches=v.sha(v.AUDIT / SNAPSHOT) == SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT, earlier_report_evidence_artifacts_hash_checked=413,
        historical_check_record_overwritten=False, genuine_b14_check_sha256_unchanged=B14_CHECK_SHA,
        partial7B15_append_only_evidence_extensions_without_reclassification=ext, next_phase_followups_preserved_for_all294=True,
        next_phase_replans_during_partial7={})
    report['phase_7B15_remaining_work_not_completion_percentage'] = dict(
        old_disposition_category_at_entry=2, of_those_prior_full_local_CSharp_bodies=2,
        b15_local_body_and_own_xaml_contract_upgrades=2, newly_full_local_parent_CSharp_among_two=0,
        remaining_old_category=0, remaining_old_category_zero_not_all_contracts_complete=True,
        B_planning_groups_retained_with_R1_R2_residuals=4, C_axes_not_started=6,
        counts_are_guaranteed_sessions_or_completion_percent=False)
    report['evidence_rows'].update(dict(
        phase_7B15_feature_rows_not_completed_features=32, phase_7B15_invariants_not_passed_tests=32,
        phase_7B15_reconciliation_contracts_not_financial_acceptance=6, phase_7B15_unexecuted_acceptance_or_gate_plans=36,
        phase_7B15_historical_extensions_not_new_findings=22, phase_7B15_nearest_root_adjudication_rows=10,
        phase_7B15_unresolved_handoffs=6, phase_7B15_unanswered_questions=6, phase_7B15_backlog_groups=10,
        phase_7B15_filename_candidates_not_features=98, phase_7B15_screen_candidates_not_features=52,
        phase_7B15_illustrations_not_erp_tests=24, phase_7B15_lexical_checks_not_erp_tests=24,
        phase_7B15_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),
        phase_7B15_witness_recomputed_matches_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder'] = pending
    report['validation']['limit'] = (
        'Read-only documentary B15:413 protected artifacts/294 immutable cores/ALLnext_phase/exact prefixes plus22 declared tails/exactG01..164/three immutable new freezes/source10ba original827. '
        'Completed B14 push/entry789b04c is separate from genuine B14 stdout checkout461ceaf; archive hashes unchanged, not replayed or rewritten after push. '
        'Historical helpers get OWN frozen rows/texts/rawCRLF bytes IN MEMORY; no global pathlib patch/disk overlay/protected helper edit/rebaseline. '
        'Four source-local roots only: BtnAll resets valid selected period before query, impossible Now.Day blocks shorter-month recompute leaving stale amounts saveable under new period, '
        'ReceiptType10 tax source hardcodes session branch while other components use selection/all, reciprocal Unchecked handlers disable the newly active period combo. '
        'Home tax menu instantiates alternate frmVATReturn, not this local parent; disabled menu/Forms seed do not prove production reachability. '
        'Both parent CSharp bodies already full7A/B1; own-XAML/local contracts complete, selected new child slices not full and no inherited coverage. '
        'DTOs resvdPrint26/RptTaxData35 and Print are local, external REPX/schema/policy/ACL remain unresolved. Parent typed half-open date boundaries are positive counterevidence; child POS end+24 differs. '
        'Typed-row/null/state/Emp/financial atomicity/numbering/precision/tax rate/exempt totals/rent gross/snapshot/health/live-master roots extended not recounted. '
        'All294 titles/classifications/evidence paths plus selected nearest chains considered, NOT all historical chains reread or all callgraphs proved. '
        'Two old-depth upgrades leave zero in that category, NOT zero remaining report contracts or whole features; R1/R2 residuals explicit to proposed R3/R4. '
        'Four B planning groups/six unstarted C axes not sessions/percentages. Additive B10 erratum10vs120 retained. '
        '24 manual+24 lexical+32 new synthetic documentation cases, all36 acceptance/gate plans not-executed. '
        'No application import/build/C#/SQL/WPF/SDK/REPX/Office/COM/formula/HTML interpreter/provider/device/printer/actual business export/shell/remediation/real data/secrets/operational measurements. '
        '7B/7 partial;7C unstarted;8 unauthorized. next_phase8 is planning not authorization.'
    )
