#!/usr/bin/env python3
"""PARTIAL7B16/B-R3 documentary consistency, NEVER ERP acceptance.

440 protected artifacts/298 immutable cores/ALLnext_phase/exactG01..170.
Historical B15 gets OWN298 rows/exact original299CRLF bytes/three index texts
IN MEMORY, not live299 rows; no protected edits, global pathlib patch, disk
overlay, rebaseline or archive rewrite. Two newly full CSharp bodies and one
prior-full picker get explicit own-XAML depth outside the frozen52 screens;
not three whole features or an expanded feature denominator. Source10ba,
completed B15 push/entry16f and genuine B15 stdout checkout789 are distinct.
One local reducer root/17 exact tails; R1/R2/R3 residuals have14 dispositions,
not external approvals. R4/B17 proposed; C unstarted;8 unauthorized. No app
import/build/C#/SQL/WPF/REPX/Office/provider/device/interpreter/measurement.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
import csv
import io
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
from validate_financial_report_part import historical_b1_inputs, registry_transition_errors, bidirectional_errors
from validate_accrual_tax_part import (
    build_current_ledger as prior_ledger, build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens, feature_level_errors, arithmetic_erratum_errors,
)

SCOPE_FILE = 'review-scope-07B16.csv'
PART_DOCS = ('PHASE-07B16.md', 'SHARED-CONTRACTS-07B16.md', 'VALIDATION-07B16.md', 'PHASE-07-REMAINING-07B16.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
SNAPSHOT = 'evidence/findings-through-07B15.csv'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B15.json'
SNAPSHOT_SHA = 'd2e46062c9d437057265d30637485c122449a90b33fa3d7a3a62437697012370'
SHARED_SHA = '3526361f8452611444e17d92ef549bccb83a08e5880f1456ac7c37220bb7ff92'
PROVENANCE_SHA = '4950c36c8a02328c0cc1680cfc97958897767579f8e0fe8d7c579162ec2acc1f'
B15_CHECK_SHA = 'b8e937f80ccec245fd280cbab02f15f5652aec02a4b29a75ab669861568b4039'
PRIOR_PROVENANCE_SHA = 'ac4977145152f1c787dd2e4fd9f414b49789c204dabfc21c99222349354323cf'
ENTRY_CHECKOUT = '16f3fd42f24183db5906bd06517b8dc10a7b9b36'
REVIEWED_BODIES = ('frmTaxInvDetails', 'frmVATReturn', 'frmPrinter')
EXTENDED_FINDINGS = {
    'P1-004', 'P1-013', 'P2-001', 'P2-010', 'P3-007', 'P3-023',
    'P7-032', 'P7-043', 'P7-045', 'P7-046', 'P7-050', 'P7-061',
    'P7-088', 'P7-095', 'P7-099', 'P7-112', 'P7-125',
}
TABLE_SPECS = (
    ('acceptance-tests', 'P7B16T-', 25), ('feature-implementation-matrix', 'FE7B16-', 24),
    ('report-invariants', 'INV7B16-', 24), ('report-reconciliation', 'RC7B16-', 6),
    ('historical-extensions', 'EX7B16-', 17), ('handoffs', 'H7B16-', 6),
    ('questions', 'Q7B16-', 6), ('continuation-backlog', 'BK7B16-', 10),
    ('root-adjudication', 'AD7B16-', 9), ('residual-disposition', 'RS7B16-', 14),
)
SENTINELS = {
    'FE7B16-23', 'FE7B16-24', 'INV7B16-23', 'INV7B16-24', 'RC7B16-06',
    'H7B16-06', 'Q7B16-06', 'P7B16T-24', 'P7B16T-25', 'AD7B16-09',
    'RS7B16-06', 'RS7B16-12', 'RS7B16-13', 'RS7B16-14', 'ALG7B16-20',
}


@contextmanager
def historical_b15_inputs(v, frozen298, texts, raw):
    """Only one exact logical registry path; nested/exception restoration too."""
    if len(frozen298) != 298 or len({r['id'] for r in frozen298}) != 298:
        raise ValueError('Exactly298 distinct historical rows required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as e:
        raise ValueError('Malformed frozen registry') from e
    if (parsed != frozen298 or raw.count(b'\r\n') != 299 or not raw.endswith(b'\r\n')
            or any(c in raw.replace(b'\r\n', b'') for c in (b'\r', b'\n'))):
        raise ValueError('Frozen298 rows/bytes/CRLF disagree')
    original = v.AUDIT
    target = Path(original / 'findings.csv').resolve()

    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve() == target else super().read_bytes()

    try:
        v.AUDIT = FrozenRegistryPath(original)
        with historical_b1_inputs(v, frozen298, texts):
            yield
    finally:
        v.AUDIT = original


def validate_frozen_b15(v, report, prior, frozen294, prov, frozen298):
    ck = v.check
    for p, digest in [
        ('evidence/provenance-07B16.json', PROVENANCE_SHA), (SNAPSHOT, SNAPSHOT_SHA),
        (SHARED_SNAPSHOT, SHARED_SHA), ('evidence/checks-07B15.json', B15_CHECK_SHA),
    ]:
        ck(v.sha(v.AUDIT / p) == digest, 'B16 immutable entry identity: ' + p)
    ck(prov['registry_at_entry_snapshot'] == SNAPSHOT and prov['registry_at_entry_sha256'] == SNAPSHOT_SHA
       and prov['shared_indexes_at_entry'] == SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256'] == SHARED_SHA,
       'B16 snapshot context')
    for p, digest in prior['historical_artifact_sha256'].items():
        ck(prov['historical_artifact_sha256'].get(p) == digest, '413-to440 continuity: ' + p)
    saved = v.json.loads(v.read(v.AUDIT / 'evidence/checks-07B15.json'))
    ck(saved['checkout_head'] == '789b04cb485948aa89e153f4b501efa27164c109'
       and saved['findings']['total_open_not_remediated'] == 298 and saved['original_project_hashes_matching'] == 827
       and saved['validation']['errors'] == [] and saved['historical_artifact_sha256'] == prior['historical_artifact_sha256']
       and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False,
       'B15 genuine stdout changed')
    ck(prov['genuine_B15_check_sha256'] == B15_CHECK_SHA and prov['prior_provenance_B15_sha256'] == PRIOR_PROVENANCE_SHA
       and prov['genuine_B15_check_record_checkout'] == saved['checkout_head'], 'B16 prior stdout/provenance identity')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY_CHECKOUT,
       'B16 completed B15 push/entry identity')
    ck(prov['phase7B15_entry_consistency'] == dict(
        original_hashes_matching=827, findings=298,
        phase_7_delivery='7A+' + '+'.join('7B' + str(n) for n in range(1, 16)) + '-partial-not-complete7B-or7',
        audit_file_count=445, errors=[], erp_runtime_tests_executed=0), 'B16 prior delivery context')
    from validate_accrual_tax_part import extend_accrual_tax
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    with historical_b15_inputs(v, frozen298, texts, (v.AUDIT / SNAPSHOT).read_bytes()):
        extend_accrual_tax(v, report, prior, frozen294)
    report.update(registry_used=SNAPSHOT, validation_scope='historical-through7B15-298-not-current-state',
                  phase_7B15_historical_input_mode='frozen298-rows-and-exact-CRLF-bytes-and-exact-indexes-in-memory')
    report['phase_7B15_adapter_context'] = dict(
        entry_provenance='evidence/provenance-07B16.json', adapter_protected_artifacts_checked=440,
        current_registry_and_shared_indexes_not_inputs=True, archived_stdout_not_rewritten_after_push=True)


def build_current_ledger(inventory, labelled, spans):
    out = prior_ledger(inventory, labelled, spans)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B16' for r in s}
    for r in out:
        r['phase7B16_ranges'] = selected.get(r['path'], 'none')
        if r['inventory_kind'] != 'generated-artifact':
            r.update(continuation_bucket='7B17-R4-or-explicit-split-or-7C-contract-not-closed',
                     next_scope_work='R1/R2/R3 محليات مع بقايا محددة و14 disposition؛ التالي B17/R4 مقترح ساكن أو split معلن. لا كل caller/feature من full body، و52/98 ثابتة ليست مقاماً للاكتمال.7C لم تبدأ و8 غير مأذونة.')
    return out


def build_candidate_disposition(inventory, labelled):
    out = prior_candidates(inventory, labelled)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B16' for r in s}
    for r in out:
        r['phase7B16_ranges'] = selected.get(r['path'], 'none')
        if not r['disposition'].startswith('lexical-false-positive'):
            r.update(disposition='7B17-R4-or-explicit-split-further-contract-required',
                     reason='98 فرز أسماء محفوظ لا تعداد كل القدرات. VAT/TaxInvDetails لا يضافان سراً إلى مقام52 القديم؛ ملحق depth3 يوضح عمقهما والـpicker. بقايا R1/R2/R3 لها external-handoff أو split معلن، لا closure.')
    return out


def build_screen_disposition(inventory, labelled):
    out = prior_screens(inventory, labelled)
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B16' for r in s}
    for n, r in enumerate(out, 1):
        r['id'] = f'SC7B16-{n:02d}'
        r['phase7B16_body_ranges'] = selected.get(r['body_path'], 'none')
        r['disposition'] = '7B17-R4-or-explicit-split-or-7C-contract-required'
        r['reason'] = '52 مرشح شاشة سابقين ثابتون؛ لا ترقيات جديدة ضمنهم فيB16 ولا نسبة اكتمال. ملحق3 محليات خارج هذا الحصر يصرح بعمقها؛ R1/R2/R3 external/split باقية، لا كل feature أو بدء7C.'
    return out


def depth_clarification(inventory, labelled, spans):
    before = [(k, s) for k, s in labelled if k != '7B16']
    selected = {r['path']: r['ranges'] for k, s in labelled if k == '7B16' for r in s}
    frozen_screens = {r['screen'] for r in prior_screens(inventory, before)}
    full = {r['path']: '1-' + str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    out = []
    for n, name in enumerate(REVIEWED_BODIES, 1):
        xaml = 'SmartAuditERP/Form_WPF/' + name + '.xaml'
        body = xaml + '.cs'
        phases = [k for k, s in before if any(r['path'] == body and r['ranges'] == full[body] for r in s)]
        current_full = all(selected.get(p) == full[p] for p in (body, xaml))
        out.append(dict(id=f'DEP7B16-{n:02d}', screen=name, body_path=body, xaml_path=xaml,
                        present_in_frozen52_screen_candidates='true' if name in frozen_screens else 'false',
                        prior_full_local_csharp_declared='true' if phases else 'false', prior_full_body_scope_ids=';'.join(phases) or 'none',
                        b16_full_local_body_and_xaml='true' if current_full else 'false',
                        newly_full_local_csharp_in_declared_scopes='false' if phases else 'true',
                        interpretation='ملحق عمق خارج52 الثابتة، لا ميزة مكتملة أو مقام جديد. طفل TaxInvDetails كان مقاطع B15؛ VAT مستدع مستقل؛ picker C# كامل B1 سابقاً. جسم/XAML محلي لا كلcaller/template/schema/ACL/policy.',
                        runtime_status='not-executed'))
    return out


def remaining_work_errors(plan, depth):
    errors = []
    expected = ['bounded-parent-contract-delivered-residuals-open'] * 2 + ['bounded-shared-contract-delivered-residuals-open'] + ['planned-not-started'] * 7
    if len(plan) != 10 or [r.get('part_family') for r in plan] != ['7B'] * 4 + ['7C'] * 6:
        errors.append('B16 retain4 B planning groups/6 unstarted C axes, not sessions')
    for n, r in enumerate(plan):
        for k in ('id', 'title', 'candidate_scope_not_certified', 'expected_deliverable', 'static_exit_criterion', 'dependencies_and_uncertainty'):
            if not isinstance(r.get(k), str) or not r[k].strip():
                errors.append('B16 missing work field: ' + str(r.get('id', '?')) + '.' + k)
        if r.get('status') != expected[min(n, 9)] or r.get('runtime_status') != 'not-executed' or r.get('counts_are_sessions_or_completion_percent') != 'false':
            errors.append('B16 work status/authorization overclaim: ' + str(r.get('id', '?')))
    if len(depth) != 3 or sum(r.get('prior_full_local_csharp_declared') == 'true' for r in depth) != 1 or sum(r.get('newly_full_local_csharp_in_declared_scopes') == 'true' for r in depth) != 2:
        errors.append('B16 depth: three local pairs/two newly full bodies/one prior full picker')
    if any(r.get('present_in_frozen52_screen_candidates') != 'false' or r.get('b16_full_local_body_and_xaml') != 'true' for r in depth):
        errors.append('B16 supplemental3 must not silently change frozen52 denominator or claim whole features')
    return errors


def group_row_errors(previous, current):
    rows = lambda t: re.findall(r'^\| G-\d{2,3} \|.*$', t, re.M)
    return [] if len(rows(previous)) == 170 and rows(current)[:170] == rows(previous) else ['Historical G01–170 exact rows changed']


def plan_structure_errors(tests, new_ids, extensions):
    errors = []
    expected = ['finding-specific'] * 2 + ['historical-root-regression'] * 17 + ['cross-cutting-contract'] * 4 + ['documentary-scope-or-authorization-gate'] * 2
    if [r.get('plan_kind') for r in tests] != expected or any(r.get('status') != 'not-executed' for r in tests):
        errors.append('B16 acceptance kinds/order/not-executed')
    if new_ids != ['P7-127']:
        errors.append('B16 one distinct reducer root only')
    if [r.get('finding_ids') for r in tests[:2]] != ['P7-127'] * 2:
        errors.append('B16 two direct root plans')
    if any(r.get('feature_ids') != 'FE7B16-01' or r.get('invariant_ids') != 'INV7B16-01' for r in tests[:2]):
        errors.append('B16 direct plan/feature/invariant mapping')
    if [r.get('finding_ids') for r in tests[2:19]] != [r.get('finding_ids') for r in extensions]:
        errors.append('B16 historical regression/manifest order')
    return errors


def adjudication_errors(data):
    errors = []
    if len(data) != 9 or data[0].get('current_root_ids') != 'P7-127' or data[0].get('decision') != 'new-local-root' or sum(r.get('decision') == 'new-local-root' for r in data) != 1:
        errors.append('B16 one new adjudicated reducer root, not new callers')
    for r in data:
        if r.get('comparison_depth') != 'all298-titles-classifications-evidence-paths-plus-selected-nearest-chains-not-all-historical-chains':
            errors.append('B16 dedup depth overclaim')
        if not r.get('nearest_prior_root_ids') or not isinstance(r.get('reason'), str) or not r['reason'].strip():
            errors.append('B16 nearest root/reason missing')
        if r.get('runtime_status') != 'not-executed':
            errors.append('B16 adjudication runtime overclaim')
    return errors


def residual_errors(data):
    errors = []
    expected = [f'H7B{part}-{n:02d};Q7B{part}-{n:02d}' for part in (14, 15) for n in range(1, 7)]
    if len(data) != 14 or [r.get('upstream_contract_ids') for r in data[:12]] != expected:
        errors.append('B16 all12 named R1/R2 upstream H/Q contracts need ordered dispositions plus2 explicit splits')
    allowed = {'bounded-source-reviewed-external-contract-remains-open', 'documentary-boundary-retained-not-closure', 'explicit-further-split-no-new-source-claim'}
    for r in data:
        for k in ('upstream_artifacts', 'current_handoff_ids', 'local_result', 'owner_role', 'required_input_and_impact', 'next_step'):
            if not isinstance(r.get(k), str) or not r[k].strip():
                errors.append('B16 unresolved residual missing field: ' + str(r.get('id', '?')) + '.' + k)
        if r.get('disposition') not in allowed or r.get('runtime_status') != 'not-executed':
            errors.append('B16 residual must remain explicitly bounded/external/split, not closed')
    if len(data) >= 14 and any(r.get('disposition') != 'explicit-further-split-no-new-source-claim' for r in data[12:]):
        errors.append('B16 wider callers/barcode/amount-words explicit split retained')
    return errors


def contract_link_errors(features, invariants, extensions, reconciliations):
    """Current-part linked evidence, not source-semantic or policy certification."""
    errors = []
    fe = {r['id']: r for r in features}
    for row in invariants:
        other = fe.get(row['id'].replace('INV7B16-', 'FE7B16-'))
        if not other or any(row.get(k) != other.get(k) for k in ('finding_ids', 'evidence', 'acceptance_ids')):
            errors.append('B16 invariant/feature lineage mismatch: ' + row['id'])
    for row in extensions:
        matches = [r for r in features if r.get('finding_ids') == row.get('finding_ids')]
        if len(matches) != 1 or any(row.get(k) != matches[0].get(k) for k in ('evidence', 'title')):
            errors.append('B16 extension/feature evidence mismatch: ' + row['id'])
    for row in reconciliations:
        associated = [fe.get(k) for k in row.get('feature_ids', '').split(';')]
        if not associated or any(r is None for r in associated):
            errors.append('B16 RC feature unknown: ' + row['id'])
            continue
        unique = lambda key: ';'.join(dict.fromkeys(x for r in associated for x in r[key].split(';')))
        if row.get('finding_ids') != unique('finding_ids') or row.get('evidence') != unique('evidence'):
            errors.append('B16 RC source/root lineage mismatch: ' + row['id'])
    return errors


def witness_metadata_errors(w):
    errors = []
    for k in ('application_code_imported_or_executed', 'application_remediation_performed', 'real_business_or_secret_data_used', 'spreadsheet_or_formula_interpreter_executed'):
        if w.get(k) is not False:
            errors.append('B16 false-only flag: ' + k)
    for k in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
        if type(w.get(k)) is not int or w[k] != 0:
            errors.append('B16 integer-zero count: ' + k)
    for k in ('child_and_actual_VAT_caller_full_local_not_whole_features', 'picker_csharp_already_full_B1', 'frozen52_denominator_not_silently_expanded', 'B_R1_R2_R3_residual_contracts_not_closed', 'supplied_sql_not_certified_deployed', 'manual_metric_models_not_financial_acceptance'):
        if w.get(k) is not True:
            errors.append('B16 boundary: ' + k)
    for k in ('illustration_count', 'static_lexical_contract_check_count'):
        if type(w.get(k)) is not int or w[k] != 20:
            errors.append('B16 witness count: ' + k)
    if w.get('phase') != '7B16-partial-static-audit':
        errors.append('B16 witness phase')
    return errors + arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def validate_source(v, row, scope):
    if 'evidence' not in row:
        return
    if row['evidence'] == 'none-inventory-only':
        v.check(row['id'] in SENTINELS, 'B16 undeclared no-source sentinel: ' + str(row['id']))
    else:
        v.check(row['id'] not in SENTINELS, 'B16 fabricated inventory evidence: ' + str(row['id']))
        v.evidence(row['evidence'], str(row['id']))
        v.scoped_evidence(row['evidence'], scope, str(row['id']) + ' boundedB16', phase=7)


def extend_shared_contracts(v, report, prov, frozen298):
    ck, rows = v.check, v.rows
    current = rows('findings.csv')
    new = current[298:]
    extensions = rows('evidence/historical-extensions-07B16.csv')
    ck(prov['historical_artifact_count'] == 440 and len(frozen298) == 298, 'B16 entry count')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY_CHECKOUT, 'B16 entry checkout')
    ck(prov['erp_runtime_tests_executed'] == 0 and prov['sql_or_external_service_tests_executed'] == 0
       and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False, 'B16 execution/remediation boundary')
    identity = report['source_reference_validation']
    ck(identity['audited_application_reference'] == v.HEAD and identity['reference_ancestor_of_checkout'] is True
       and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching'] == 827, 'B16 source identity')
    ext = v.transition(frozen298, current, 7, EXTENDED_FINDINGS, preserve_followups=True)
    for error in registry_transition_errors(frozen298, current, extensions):
        ck(False, error)
    ck(len(current) == len({r['id'] for r in current}) == 299 and [r['id'] for r in new] == ['P7-127'], 'B16 registry/newID')
    v.distributions(new, {'Medium': 1}, {'confirmed': 1}, 'boundedB16 only')
    for r in new:
        ck(r['type'] == 'implementation-defect' and r['status'] == 'open-not-remediated' and r['next_phase'] == '8', 'B16 finding state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$', v.read(v.AUDIT / PART_DOCS[0]), re.M) == [(r['id'], r['title']) for r in new], 'B16 headings/registry')
    raw = (v.AUDIT / 'findings.csv').read_bytes()
    ck(not raw.startswith(b'\xef\xbb\xbf') and raw.count(b'\r\n') == 300 and b'\n' not in raw.replace(b'\r\n', b''), 'B16 noBOM/CRLF registry')
    selected = rows(SCOPE_FILE)
    scope = {r['path']: v.spans(r['ranges']) for r in selected}
    inventory = rows('evidence/inventory.csv')
    paths = {r['path'] for r in inventory}
    ck(len(selected) == len(scope) == 30, 'B16 selected30 paths')
    for r in selected:
        ck(r['path'] in paths and r['review_state'] == 'selected-static-source-slices-not-runtime-certified' and bool(r['focus']), 'B16 scope: ' + r['path'])
        v.source_ref(r['path'], r['ranges'], SCOPE_FILE)
    for r in new:
        validate_source(v, r, scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml', '.xaml.cs'):
            p = 'SmartAuditERP/Form_WPF/' + name + suffix
            ck(scope.get(p) == [(1, len(v.read(v.ROOT / p).splitlines()))], 'B16 own local body/XAML: ' + p)
    ck(scope.get('SmartAuditERP/Class/Report.cs') == [(1, 611)], 'B16 Report local full body')
    ck(scope.get('SmartAuditERP/Class/Print.cs') == [(54, 221)], 'B16 Print is selected only, not its invoice binder')
    known = {r['id'] for r in current} | {f'H7B16-{n:02d}' for n in range(1, 7)}
    tables = {}
    for name, prefix, count in TABLE_SPECS:
        data = rows('evidence/' + name + '-07B16.csv')
        tables[prefix] = data
        v.sequential(data, prefix, count)
        v.related(data, known)
        for r in data:
            for k, value in r.items():
                ck(bool(value), 'B16 incomplete cell: ' + str(r['id']) + '.' + k)
            validate_source(v, r, scope)
            if 'runtime_status' in r:
                ck(r['runtime_status'] == 'not-executed', 'B16 runtime overclaim')
    tests, features, invs, rc = [tables[k] for k in ('P7B16T-', 'FE7B16-', 'INV7B16-', 'RC7B16-')]
    tids, fids, iids = [{r['id'] for r in pool} for pool in (tests, features, invs)]
    v.proposed_tests(tests, '7B16')
    v.related(tests, fids, 'feature_ids')
    v.related(tests, iids, 'invariant_ids')
    v.related(features + invs, tids, 'acceptance_ids')
    for pool, field in ((features, 'feature_ids'), (invs, 'invariant_ids')):
        for error in bidirectional_errors(pool, tests, field):
            ck(False, error)
    for error in (feature_level_errors(features) + plan_structure_errors(tests, [r['id'] for r in new], extensions)
                  + contract_link_errors(features, invs, extensions, rc)):
        ck(False, error)
    ck(len({r['required_invariant'] for r in invs}) == 24
       and len({r['acceptance_criterion'] for r in tests}) == 25,
       'B16 invariants/acceptance must be distinct substantive contracts, not repeated boilerplate')
    for pool, label in ((tests, 'plans'), (features, 'features'), (invs, 'invariants')):
        v.covered(new, pool, 'B16 ' + label)
    ck({r['finding_ids'] for r in extensions} == EXTENDED_FINDINGS
       and [r['finding_ids'] for r in features[1:18]] == [r['finding_ids'] for r in extensions], 'B16 exact extension mapping')
    for r in extensions:
        ck(r['followup_policy'] == 'unchanged-during-partial7', 'B16 hidden replan')
    for r in rc:
        v.related([r], fids, 'feature_ids')
        v.related([r], tids, 'acceptance_ids')
        expected = [t['id'] for t in tests if set(t['feature_ids'].split(';')) & set(r['feature_ids'].split(';'))]
        ck(r['acceptance_ids'].split(';') == expected and bool(expected), 'B16 RC reverse links')
    hids = {r['id'] for r in tables['H7B16-']}
    v.related(tables['Q7B16-'], hids, 'handoff_ids')
    for r in tables['H7B16-']:
        ck(r['status'] == 'external-contract-or-policy-unresolved-not-absence-proof', 'B16 handoff')
    for r in tables['Q7B16-']:
        ck(r['status'] == 'unanswered-no-secrets-requested', 'B16 question')
    residuals = tables['RS7B16-']
    for error in residual_errors(residuals):
        ck(False, error)
    v.related(residuals, hids, 'current_handoff_ids')
    for r in residuals:
        for p in r['upstream_artifacts'].split(';'):
            ck((v.AUDIT / p).is_file(), 'B16 upstream artifact missing: ' + p)
    for n, r in enumerate(tables['BK7B16-'], 1):
        ck(r['prior_backlog_id'] == f'BK7B15-{n:02d}' and r['original_backlog_id'] == f'BK7-{n:02d}' and r['status'] != 'complete', 'B16 backlog ancestry')
    ck([r['status'] for r in tables['BK7B16-'][2:6]] == ['not-started'] * 4, 'B16 accidentally startsC')
    ad = tables['AD7B16-']
    v.related(ad, known, 'current_root_ids')
    v.related(ad, known, 'nearest_prior_root_ids')
    for error in adjudication_errors(ad):
        ck(False, error)
    for n, indices in enumerate(((0,), (11,), (14,), (12,), (13, 15, 16, 17), (9, 10), (8,), (1, 2, 3, 4, 5, 6, 7))):
        required_refs = {ref for i in indices for ref in features[i]['evidence'].split(';')}
        ck(required_refs <= set(ad[n]['evidence'].split(';')), 'B16 adjudication evidence unrelated to root: ' + ad[n]['id'])
    labelled = [(str(n), rows('review-scope.csv' if n == 1 else f'review-scope-{n:02d}.csv')) for n in range(1, 7)]
    labelled += [('7A', rows('review-scope-07.csv'))] + [(f'7B{n}', rows(f'review-scope-07B{n}.csv')) for n in range(1, 16)] + [('7B16', selected)]
    ck(rows('evidence/coverage-ledger-07B16.csv') == build_current_ledger(inventory, labelled, v.spans), 'B16 ledger')
    candidates = rows('evidence/report-candidate-disposition-07B16.csv')
    screens = rows('evidence/report-screen-disposition-07B16.csv')
    ck(len(candidates) == 98 and candidates == build_candidate_disposition(inventory, labelled), 'B16 filename triage')
    ck(len(screens) == 52 and screens == build_screen_disposition(inventory, labelled), 'B16 frozen52 screen triage')
    v.sequential(screens, 'SC7B16-', 52)
    ck(collections.Counter(r['coverage_level'] for r in screens) == {
        'bounded-local-body-and-xaml-not-whole-feature-certified': 33,
        'bounded-local-body-and-selected-xaml-not-whole-feature-certified': 19}, 'B16 frozen52 count not new feature coverage')
    before = {r['path'] for _, s in labelled[:-1] for r in s}
    selected_paths = set(scope)
    book = (len(before), len(selected_paths & before), len(selected_paths - before), len(before | selected_paths), len(paths - (before | selected_paths)))
    ck(book == (395, 26, 4, 399, 428), 'B16 union bookkeeping')
    depth = rows('evidence/report-depth-clarification-07B16.csv')
    plan = rows('evidence/remaining-workplan-07B16.csv')
    v.sequential(depth, 'DEP7B16-', 3)
    v.sequential(plan, 'RW7B16-', 10)
    ck(depth == depth_clarification(inventory, labelled, v.spans), 'B16 depth clarification')
    for error in remaining_work_errors(plan, depth):
        ck(False, error)
    witness, match = v.recompute('evidence/report-witnesses-07B16.json', 'tools/check_shared_contract_witnesses.py')
    alg, lex = witness['illustrations'], witness['static_lexical_contract_checks']
    v.sequential(alg, 'ALG7B16-', 20)
    v.sequential(lex, 'ST7B16-', 20)
    v.related(alg + lex, known)
    for error in witness_metadata_errors(witness):
        ck(False, error)
    ck(witness['errors'] == [], 'B16 witness observations failed')
    for r in alg + lex:
        flag = 'illustration_assertions_passed' if r['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']), 'B16 witness overclaim')
        validate_source(v, r, scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}', scope, 'B16 bounded lexical read', phase=7)
    patterns = [
        (PART_DOCS[0], r'^\| (EX7B16-\d{2}) \|', [r['id'] for r in extensions]),
        (PART_DOCS[0], r'^\| (AD7B16-\d{2}) \|', [r['id'] for r in ad]),
        (PART_DOCS[1], r'^\| (FE7B16-\d{2}) —', [r['id'] for r in features]),
        (PART_DOCS[1], r'^\| (INV7B16-\d{2}) \|', [r['id'] for r in invs]),
        (PART_DOCS[1], r'^### (RC7B16-\d{2}) —', [r['id'] for r in rc]),
        (PART_DOCS[2], r'^\| (P7B16T-\d{2}) \|', [r['id'] for r in tests]),
        (PART_DOCS[3], r'^\| (DEP7B16-\d{2}) \|', [r['id'] for r in depth]),
        (PART_DOCS[3], r'^\| (RS7B16-\d{2}) \|', [r['id'] for r in residuals]),
        (PART_DOCS[3], r'^\| (RW7B16-\d{2}) \|', [r['id'] for r in plan]),
        ('IMPROVEMENTS.md', r'^\| (G-\d{2,3}) \|', [f'G-{n:02d}' for n in range(1, 177)]),
    ]
    for file, pattern, expected in patterns:
        ck(re.findall(pattern, v.read(v.AUDIT / file), re.M) == expected, 'B16 Markdown IDs: ' + file)
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
            if target == (v.AUDIT / 'evidence/checks-07B16.json').resolve() and not target.exists():
                pending = True
                continue
            v.LINK_COUNT += 1
            ck(target.exists(), 'B16 broken link: ' + name + ':' + m[1])
        for m in source.finditer(text):
            v.source_ref(m[1], m[2], name)
            if name in PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a, b in v.spans(m[2])), scope, name, phase=7)
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'], v.read(v.AUDIT / 'IMPROVEMENTS.md')):
        ck(False, error)
    for name in SHARED_DOCS:
        ck(all(t in v.read(v.AUDIT / name) for t in ('PHASE-07B16.md', 'PHASE-07-REMAINING-07B16.md', '7B17', 'غير مأذونة', '16f3fd4', '10ba215')), 'B16 current index boundary: ' + name)
    tools = ['check_shared_contract_witnesses.py', 'validate_shared_contract_part.py', 'test_shared_contract_audit_validator.py']
    for name in tools:
        try:
            v.ast.parse(v.read(v.AUDIT / 'tools' / name), filename=name)
        except SyntaxError as e:
            ck(False, 'B16 syntax: ' + str(e))
    run = v.subprocess.run([v.sys.executable, '-B', str(v.AUDIT / 'tools/test_shared_contract_audit_validator.py')], cwd=v.ROOT, capture_output=True, text=True, timeout=30)
    m = re.search(r'Ran (\d+) tests? in ', run.stderr + '\n' + run.stdout)
    count = int(m[1]) if m else None
    passed = run.returncode == 0 and count == 28
    ck(passed, 'B16 synthetic documentation self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_shared_contract_audit_validator.py'] = dict(
        tests_reported=count, expected_tests=28, process_exit_code=run.returncode, result='passed' if passed else 'failed-or-unrecognized', erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked'] += tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/' + n: v.sha(v.AUDIT / 'tools' / n) for n in ['validate_audit.py'] + tools})
    report.update(validation_scope='current-through7B16-299-plus-frozen-history-not-runtime-certification',
                  phase_7_delivery='7A+' + '+'.join('7B' + str(n) for n in range(1, 17)) + '-partial-not-complete7B-or7',
                  phase_7_remaining_parts=['7B17-proposed-R4-with-R1-R2-R3-external-residuals-or-explicit-further-split', '7C-six-axes-not-started'],
                  registry_used='findings.csv', historical_artifact_sha256=prov['historical_artifact_sha256'], date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=127, phase_7B16=1, total_open_not_remediated=299,
                              severity=dict(collections.Counter(r['severity'] for r in current)), certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE: 30, 'phase_7B15_union_frozen': 395, 'phase_7B16_overlap_with_prior_union': 26,
                                  'phase_7B16_new_paths': 4, 'unique_union_not_line_or_execution_coverage': 399, 'inventory_only_no_selected_scope': 428})
    report['phase_7B15_historical_evidence'] = dict(
        frozen_registry=SNAPSHOT, frozen_registry_sha256_matches=v.sha(v.AUDIT / SNAPSHOT) == SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT, earlier_report_evidence_artifacts_hash_checked=440,
        historical_check_record_overwritten=False, genuine_b15_check_sha256_unchanged=B15_CHECK_SHA,
        partial7B16_append_only_evidence_extensions_without_reclassification=ext, next_phase_followups_preserved_for_all298=True,
        next_phase_replans_during_partial7={})
    report['phase_7B16_remaining_work_not_completion_percentage'] = dict(
        frozen_screen_candidates=52, frozen_depth_categories=dict(local_body_and_xaml=33, local_body_selected_xaml=19),
        supplemental_local_body_and_own_xaml_contracts_outside_frozen52=3, newly_full_local_CSharp_among_three=2,
        picker_CSharp_already_full_B1=True, residual_dispositions=14, external_contracts_or_splits_not_closed=True,
        B_planning_groups_retained_with_R1_R2_R3_residuals=4, C_axes_not_started=6,
        counts_are_guaranteed_sessions_or_completion_percent=False)
    report['evidence_rows'].update(dict(
        phase_7B16_feature_rows_not_completed_features=24, phase_7B16_invariants_not_passed_tests=24,
        phase_7B16_reconciliation_contracts_not_financial_acceptance=6, phase_7B16_unexecuted_acceptance_or_gate_plans=25,
        phase_7B16_historical_extensions_not_new_findings=17, phase_7B16_nearest_root_adjudication_rows=9,
        phase_7B16_unresolved_handoffs=6, phase_7B16_unanswered_questions=6, phase_7B16_backlog_groups=10,
        phase_7B16_residual_dispositions_not_external_approvals=14,
        phase_7B16_filename_candidates_not_features=98, phase_7B16_screen_candidates_not_features=52,
        phase_7B16_illustrations_not_erp_tests=20, phase_7B16_lexical_checks_not_erp_tests=20,
        phase_7B16_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),
        phase_7B16_witness_recomputed_matches_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder'] = pending
    report['validation']['limit'] = (
        'Read-only documentary B16:440 protected artifacts/298 immutable cores/ALLnext_phase/exact prefixes plus17 declared tails/exactG01..170/three entry freezes/source10ba original827. '
        'Completed B15 push/entry16f3fd4 is separate from genuine B15 stdout checkout789b04c; archives never rewritten after push. '
        'Historical helpers receive OWN frozen rows/texts/rawCRLF bytes IN MEMORY, not live299; no global pathlib patch, disk overlay, protected helper edit or rebaseline. '
        'One local reducer root127: VAT caller queries return NonTaxable for both directions but omit subtracting that component in case2; sales and purchases share one root. '
        'Not parent total-exempt044, commission absolute Value111, SQL membership084 or rate/discount043; VAT zero need not change. '
        '17 exact historical tails retain all classifications/followups; XML under XLSX extends050, not formula049 or writer108; invoice1/2/3 openers carry GlobalID while expense receipt loses it. '
        'Current type settings reinterpret child historical PriceIncVAT095; parent/VAT stored flags are counterexamples. All-period112/sessionbranch125/stale-all088/index099 retain their roots. '
        'VAT totals labeled taxable do not automatically extend044; VAT Checked-only periods do not extend126; receipt9 uses selected branch, so125 not automatically assigned to VAT. '
        'Three supplemental local body/own-XAML pairs outside frozen52; picker CSharp already fullB1; child previously slicedB15; not all features/callers. Report local full, Print only54..221. '
        'Local DTOs and Report/Print exist; external UtilitiesProj ToDataTable/REPX/manifest/settings-precedence/schema/grants/policies unresolved. '
        'R1 null bridge055/default worker054 and all prior barriers not assumed fixed; overload resolution/build not executed. '
        'All298 titles/classifications/evidence paths plus selected nearest chains, NOT all historical chains or all callgraphs. '
        '14 explicit upstream residual dispositions include12 R1/R2 H/Q inputs and2 further splits for wider callers/barcode/amount-words; not external approvals or whole7B closure. '
        'Four B planning groups retain R1/R2/R3 residuals, R4/B17 proposed; six C axes unstarted; no session/percentage promise. Additive B10 erratum10vs120 retained. '
        '20 manual+20 lexical+28 new synthetic documentary cases; all25 acceptance/gate plans not-executed. '
        'No application import/build/C#/SQL/WPF/SDK/REPX/Office/COM/formula/HTML interpreter/provider/device/printer/business export/shell/remediation/real data/secrets/operational measurement. '
        '7B/7 partial;7C unstarted;8 unauthorized. next_phase8 planning is not authorization.'
    )
