#!/usr/bin/env python3
"""Read-only PARTIAL7B11 documentary checks; NEVER ERP acceptance.

Protect315 prior artifacts, frozen285 cores/ALL followups and exactG01..140.
B10 gets its OWN frozen285 registry bytes/rows and exact index texts IN MEMORY.
The path subclass below overlays one exact logical registry path's read_bytes;
no pathlib/global patch, filesystem write, protected-helper edit or rebaseline.
Supplied SQL is not certified deployed SQL. Default aggregate P3-022 remains.
"""
from __future__ import annotations

from contextlib import contextmanager
import collections
import csv
import io
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from validate_financial_report_part import (
    historical_b1_inputs, registry_transition_errors, bidirectional_errors,
)
from validate_salesman_contract_part import (
    build_current_ledger as prior_ledger, build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens, feature_level_errors as prior_feature_errors,
)

SCOPE_FILE = 'review-scope-07B11.csv'
PART_DOCS = ('PHASE-07B11.md', 'ACCOUNT-STATEMENT-CONTRACTS-07B11.md', 'VALIDATION-07B11.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
SNAPSHOT = 'evidence/findings-through-07B10.csv'
SNAPSHOT_SHA = 'ff84ec2f04039249e40115780811f0b0ae4d5afd489a24563c139db5aa68d990'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B10.json'
SHARED_SHA = 'da4b113dea180036d00a5f76d72a9fa0df7a9aff0afc61a0334efb46f247c6d2'
B10_CHECK_SHA = 'f67f0b6ce26504e406866e6b5e70a25c0c958734411ffb7c1217631c4744c6af'
ENTRY_CHECKOUT = '1fbac9e34ede90396f212bd03390a1a737c351e6'
EXTENDED_FINDINGS = {
    'P1-004', 'P1-011', 'P1-013', 'P1-030', 'P1-033', 'P2-010',
    'P3-021', 'P3-022', 'P3-023', 'P7-045', 'P7-046', 'P7-061', 'P7-085', 'P7-099',
}
REVIEWED_BODIES = ('frmAccountBalance', 'frmAccountsStatement', 'frmRptEntries')
SENTINELS = {
    'FE7B11-22', 'INV7B11-22', 'FE7B11-23', 'INV7B11-23',
    'RC7B11-06', 'H7B11-06', 'Q7B11-06', 'P7B11T-24', 'P7B11T-25', 'ALG7B11-20',
}
TABLE_SPECS = (
    ('acceptance-tests', 'P7B11T-', 25), ('feature-implementation-matrix', 'FE7B11-', 23),
    ('report-invariants', 'INV7B11-', 23), ('report-reconciliation', 'RC7B11-', 6),
    ('historical-extensions', 'EX7B11-', 14), ('handoffs', 'H7B11-', 6),
    ('questions', 'Q7B11-', 6), ('continuation-backlog', 'BK7B11-', 10),
)


@contextmanager
def historical_b10_inputs(v, frozen285, texts, raw):
    """Exact logical-path IN-MEMORY rows/text/bytes; restore even on exception.

    ProtectedB10 reads registry bytes directly from v.AUDIT / findings.csv for
    CRLF. Merely overlaying v.rows/read would feed it current287 bytes. A LOCAL
    Path subclass overlays that ONE path with the original frozen bytes. Other
    paths retain normal behavior; no patch to pathlib.Path or disk writes.
    """
    if len(frozen285) != 285 or len({x['id'] for x in frozen285}) != 285:
        raise ValueError('Exactly285 distinct historical registry rows required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact historical UTF8/noBOM bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    except (UnicodeError, csv.Error) as exc:
        raise ValueError('Historical registry bytes malformed') from exc
    if (parsed != frozen285 or raw.count(b'\r\n') != 286 or
            b'\n' in raw.replace(b'\r\n', b'')):
        raise ValueError('Frozen285 bytes/rows/CRLF disagree')
    original_audit = v.AUDIT
    target = Path(original_audit / 'findings.csv').resolve()

    class FrozenRegistryPath(type(original_audit)):
        def read_bytes(self):
            if self.resolve() == target:
                return raw
            return super().read_bytes()

    try:
        v.AUDIT = FrozenRegistryPath(original_audit)
        with historical_b1_inputs(v, frozen285, texts):
            yield
    finally:
        v.AUDIT = original_audit


def validate_frozen_b10(v, report, prior, frozen282, prov, frozen285):
    ck = v.check
    ck(prov['registry_at_entry_snapshot'] == SNAPSHOT and
       prov['registry_at_entry_sha256'] == SNAPSHOT_SHA and
       v.sha(v.AUDIT / SNAPSHOT) == SNAPSHOT_SHA, 'B11 frozen285 identity changed')
    ck(prov['shared_indexes_at_entry'] == SHARED_SNAPSHOT and
       prov['shared_indexes_at_entry_sha256'] == SHARED_SHA and
       v.sha(v.AUDIT / SHARED_SNAPSHOT) == SHARED_SHA, 'B11 frozen exact B10 indexes changed')
    ck(prov['phase7B10_entry_consistency'] == dict(
        original_hashes_matching=827, findings=285,
        phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9+7B10-partial-not-complete7B-or7',
        errors=[], erp_runtime_tests_executed=0), 'B11 entry no longer describes deliveredB10')
    for p, digest in prior['historical_artifact_sha256'].items():
        ck(prov['historical_artifact_sha256'].get(p) == digest, '292-to315 historical continuity: ' + p)
    ck(prov['genuine_B10_check_sha256'] == B10_CHECK_SHA and
       v.sha(v.AUDIT / 'evidence/checks-07B10.json') == B10_CHECK_SHA, 'Genuine B10 stdout changed')
    saved = v.json.loads(v.read(v.AUDIT / 'evidence/checks-07B10.json'))
    ck(saved['validation']['errors'] == [] and
       saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False and
       saved['findings']['total_open_not_remediated'] == 285 and
       saved['original_project_hashes_matching'] == 827 and
       saved['historical_artifact_sha256'] == prior['historical_artifact_sha256'], 'B10 archived285/827/292 changed')
    from validate_salesman_contract_part import extend_salesman_contracts
    texts = v.json.loads(v.read(v.AUDIT / SHARED_SNAPSHOT))['files']
    raw = (v.AUDIT / SNAPSHOT).read_bytes()
    with historical_b10_inputs(v, frozen285, texts, raw):
        extend_salesman_contracts(v, report, prior, frozen282)
    report.update(registry_used=SNAPSHOT, validation_scope='historical-through7B10-285-not-current-state',
                  phase_7B10_historical_input_mode='frozen285-rows-and-CRLF-bytes-plus-exact-shared-index-texts-in-memory')
    report['phase_7B10_adapter_context'] = dict(
        entry_provenance='evidence/provenance-07B11.json', adapter_protected_artifacts_checked=315,
        current_registry_bytes_rows_and_shared_indexes_not_inputs=True,
        historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True,
        archived_stdout_not_rewritten_after_authorized_push=True)
    report['validation']['limit'] += (
        ' HistoricalB10 gets OWN frozen285 rows AND original CRLF bytes at the exact logical registry path '
        'and exact delivered index texts IN MEMORY, not current287/live indexes. Its direct read_bytes '
        'guard is preserved without patching pathlib globally or editing protected code. '
        'ArchivedB10 checkouta254/B9checkout3612700 remain byte-protected, not current-checkout replay.'
    )


def build_current_ledger(inventory, labelled_scopes, parse_ranges):
    out = prior_ledger(inventory, labelled_scopes, parse_ranges)
    selected = {r['path']: r['ranges'] for label, scope in labelled_scopes if label == '7B11' for r in scope}
    for r in out:
        r['phase7B11_ranges'] = selected.get(r['path'], 'none')
        if r['inventory_kind'] != 'generated-artifact':
            r['continuation_bucket'] = '7B12-or-7C-further-contracts-not-closed'
            r['next_scope_work'] = 'بقية القدرات والمتصلين والأطفال والقوالب والمخطط والتفويض والسياسة أو استبعاد مسند؛7B12 معلنة و7C لم تبدأ. لا اكتمال من كل أسطر جسم ولا قياس index/leak/latency من نص.'
    return out


def build_candidate_disposition(inventory, labelled_scopes):
    out = prior_candidates(inventory, labelled_scopes)
    selected = {r['path']: r['ranges'] for label, scope in labelled_scopes if label == '7B11' for r in scope}
    for r in out:
        r['phase7B11_ranges'] = selected.get(r['path'], 'none')
        if not r['disposition'].startswith('lexical-false-positive'):
            r['disposition'] = '7B12-further-contracts-or-reasoned-exclusion-required'
            r['reason'] = '98 مرشح ملف فرز أسماء لا ميزات مكتملة؛ كشفا الحساب curated خارج regex. جسم محلي أو child slice لا يغلق كل قدرة/caller/template/schema/ACL/نشر/قبول؛7B12/7C أو استبعاد مسند.'
    return out


def build_screen_disposition(inventory, labelled_scopes):
    out = prior_screens(inventory, labelled_scopes)
    selected = {r['path']: r['ranges'] for label, scope in labelled_scopes if label == '7B11' for r in scope}
    full = {r['path']: '1-' + str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    for n, r in enumerate(out, 1):
        r['id'] = f'SC7B11-{n:02d}'
        r['phase7B11_body_ranges'] = selected.get(r['body_path'], 'none')
        r['disposition'] = '7B12-or-7C-further-contracts-or-reasoned-exclusion-required'
        if (r['screen'] in REVIEWED_BODIES and all(p in full and selected.get(p) == full[p]
                                                 for p in (r['path'], r['body_path']))):
            r['coverage_level'] = 'bounded-local-body-and-xaml-not-whole-feature-certified'
            r['reason'] = 'استكمال جسم/XAML محلي في7B11 بعد مقاطع2/3/7A/B2؛ لا إعادة عد الأصول أو وراثة طفل لتغطية أبيه. بقية caller/template/schema/ACL/سياسة/نشر/قبول غير مغلقة؛7B12/7C.'
        else:
            r['reason'] = 'حصر أو مقاطع/أجسام محلية سابقة بحسب الحقول، لا كل العقود؛ child لا يرث تغطية parent.7B12/7C أو استبعاد مسند.'
    return out


def feature_level_errors(features):
    return [e.replace('B10', 'B11') for e in prior_feature_errors(features)]


def group_row_errors(previous, current):
    old = re.findall(r'^\| G-\d{2,3} \|.*$', previous, re.M)
    now = re.findall(r'^\| G-\d{2,3} \|.*$', current, re.M)
    return [] if len(old) == 140 and now[:140] == old else ['Historical G01–140 exact rows changed']


def arithmetic_erratum_errors(value):
    """Additive arithmetic prose guard, NOT certification of all audit prose."""
    expected = dict(entered_quantity=2, equality=12, base_unit_cost=5,
                    local_cost=10, reference_cost=120, archive_rewritten=False)
    return [] if value == expected and all(type(value[k]) is int for k in expected if k != 'archive_rewritten') and value['archive_rewritten'] is False else ['B11 additive B10 arithmetic erratum mismatch']


def witness_metadata_errors(w):
    out = []
    for k in ('application_code_imported_or_executed', 'application_remediation_performed',
              'real_business_or_secret_data_used', 'spreadsheet_or_formula_interpreter_executed'):
        if w.get(k) is not False: out.append('B11 false-only flag: ' + k)
    for k in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
        if type(w.get(k)) is not int or w[k] != 0: out.append('B11 integer-zero count: ' + k)
    for k in ('default_aggregate_gate_not_assumed_resolved', 'supplied_sql_not_certified_deployed'):
        if w.get(k) is not True: out.append('B11 causal boundary: ' + k)
    if w.get('phase') != '7B11-partial-static-audit': out.append('B11 witness phase')
    for k in ('illustration_count', 'static_lexical_contract_check_count'):
        if type(w.get(k)) is not int or w[k] != 20: out.append('B11 witness count: ' + k)
    out += arithmetic_erratum_errors(w.get('additive_B10_arithmetic_erratum'))
    return out


def validate_source(v, row, scope):
    if 'evidence' not in row: return
    if row['evidence'] == 'none-inventory-only':
        v.check(row['id'] in SENTINELS, 'Undeclared B11 no-source sentinel: ' + row['id'])
    else:
        v.check(row['id'] not in SENTINELS, 'B11 documentary/inventory boundary: ' + row['id'])
        v.evidence(row['evidence'], row['id'])
        v.scoped_evidence(row['evidence'], scope, row['id'] + ' bounded7B11', phase=7)


def extend_statement_contracts(v, report, prov, frozen285):
    ck, rows = v.check, v.rows
    ck(prov['historical_artifact_count'] == 315 and len(frozen285) == 285, 'B11 entry count')
    ck(prov['checkout_head_at_entry'] == prov['remote_current_branch_tip_observed_at_entry'] == ENTRY_CHECKOUT, 'B11 actual entry checkout')
    rec = prov['entry_checkout_reconciliation']
    ck(rec['initial_restored_checkout'] == v.HEAD and
       rec['all320_workspace_document_bytes_matched_authorized_remote_before_fast_forward'] is True and
       rec['application_byte_changes'] is False, 'B11 reconciliation boundary')
    ident = report['source_reference_validation']
    ck(ident['audited_application_reference'] == v.HEAD and ident['reference_ancestor_of_checkout'] is True and
       ident['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching'] == 827, 'B11 source identity')
    ck(prov['erp_runtime_tests_executed'] == 0 and prov['application_remediation_performed'] is False and
       prov['phase8_authorized_or_started'] is False, 'B11 unauthorized execution/remediation claim')
    current = rows('findings.csv'); new = current[285:]
    extensions = rows('evidence/historical-extensions-07B11.csv')
    ext = v.transition(frozen285, current, 7, EXTENDED_FINDINGS, preserve_followups=True)
    for e in registry_transition_errors(frozen285, current, extensions): ck(False, e)
    ck(len(current) == len({r['id'] for r in current}) == 287, 'B11 count/uniqueness')
    ck([r['id'] for r in new] == ['P7-114', 'P7-115'], 'B11 new IDs')
    v.distributions(new, {'High': 1, 'Medium': 1}, {'confirmed': 2}, 'bounded7B11 only')
    for r in new:
        ck(r['status'] == 'open-not-remediated' and r['next_phase'] == '8' and r['type'] == 'implementation-defect' and bool(r['title']), 'B11 status/type/followup: ' + r['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$', v.read(v.AUDIT / PART_DOCS[0]), re.M) == [(r['id'], r['title']) for r in new], 'B11 headings/registry')
    raw = (v.AUDIT / 'findings.csv').read_bytes()
    ck(not raw.startswith(b'\xef\xbb\xbf') and raw.count(b'\r\n') == 288 and b'\n' not in raw.replace(b'\r\n', b''), 'B11 CRLF/noBOM registry')
    scopes = rows(SCOPE_FILE); inventory = rows('evidence/inventory.csv'); paths = {r['path'] for r in inventory}
    scope = {r['path']: v.spans(r['ranges']) for r in scopes}
    ck(len(scopes) == len(scope) == 21, 'B11 scope count/duplicates')
    for r in scopes:
        ck(r['path'] in paths and r['review_state'] == 'selected-static-source-slices-not-runtime-certified' and bool(r['focus']), 'B11 scope: ' + r['path'])
        v.source_ref(r['path'], r['ranges'], SCOPE_FILE)
    for r in new: validate_source(v, r, scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml.cs', '.xaml'):
            p = 'SmartAuditERP/Form_WPF/' + name + suffix
            ck(scope.get(p) == [(1, len(v.read(v.ROOT / p).splitlines()))], 'B11 full local body/XAML: ' + p)
    known = {r['id'] for r in current} | {f'H7B11-{n:02d}' for n in range(1, 7)}
    tables = {}
    for name, prefix, count in TABLE_SPECS:
        data = rows('evidence/' + name + '-07B11.csv'); tables[prefix] = data
        v.sequential(data, prefix, count); v.related(data, known)
        for r in data:
            for k, value in r.items(): ck(bool(value), f'Incomplete B11 cell: {r["id"]}.{k}')
            validate_source(v, r, scope)
            if 'runtime_status' in r: ck(r['runtime_status'] == 'not-executed', 'B11 runtime claim: ' + r['id'])
    tests, features, invs, rc = [tables[k] for k in ('P7B11T-', 'FE7B11-', 'INV7B11-', 'RC7B11-')]
    tids = {r['id'] for r in tests}; fids = {r['id'] for r in features}; iids = {r['id'] for r in invs}
    v.proposed_tests(tests, '7B11'); v.related(tests, fids, 'feature_ids'); v.related(tests, iids, 'invariant_ids')
    v.related(features + invs, tids, 'acceptance_ids')
    for pool, field in ((features, 'feature_ids'), (invs, 'invariant_ids')):
        for e in bidirectional_errors(pool, tests, field): ck(False, e)
    for e in feature_level_errors(features): ck(False, e)
    for pool, label in ((tests, 'plans'), (features, 'features'), (invs, 'invariants')): v.covered(new, pool, 'B11 ' + label)
    for r in new:
        ck(len([t for t in tests if t['plan_kind'] == 'finding-specific' and t['finding_ids'] == r['id']]) == 2, 'B11 finding lacks two direct plans: ' + r['id'])
    ck([r['plan_kind'] for r in tests] == ['finding-specific'] * 4 + ['historical-root-regression'] * 14 + ['cross-cutting-contract'] * 5 + ['documentary-scope-or-authorization-gate'] * 2, 'B11 plan kinds/order')
    ck([r['finding_ids'] for r in features[:2]] == [r['id'] for r in new] and
       [r['finding_ids'] for r in features[2:16]] == [r['finding_ids'] for r in extensions] and
       {r['finding_ids'] for r in extensions} == EXTENDED_FINDINGS, 'B11 new/extension mapping')
    for r in extensions: ck(r['followup_policy'] == 'unchanged-during-partial7', 'B11 hidden replan: ' + r['id'])
    for r in rc:
        v.related([r], fids, 'feature_ids'); v.related([r], tids, 'acceptance_ids')
        expected = [t['id'] for t in tests if set(t['feature_ids'].split(';')) & set(r['feature_ids'].split(';'))]
        ck(r['acceptance_ids'].split(';') == expected and bool(expected), 'B11 RC links: ' + r['id'])
        roots = {root for f in features if f['id'] in r['feature_ids'].split(';') for root in f['finding_ids'].split(';')}
        ck(set(r['finding_ids'].split(';')) <= roots, 'B11 RC roots: ' + r['id'])
    v.related(tables['Q7B11-'], {r['id'] for r in tables['H7B11-']}, 'handoff_ids')
    for r in tables['H7B11-']: ck(r['status'] == 'external-contract-or-policy-unresolved-not-absence-proof', 'B11 handoff falsely resolved')
    for r in tables['Q7B11-']: ck(r['status'] == 'unanswered-no-secrets-requested', 'B11 question falsely resolved')
    for n, r in enumerate(tables['BK7B11-'], 1):
        ck(r['prior_backlog_id'] == f'BK7B10-{n:02d}' and r['original_backlog_id'] == f'BK7-{n:02d}' and r['part'] in {'7B12','7C','7B12/7C'} and r['status'] != 'complete', 'B11 backlog: ' + r['id'])
    ck([r['status'] for r in tables['BK7B11-'][2:6]] == ['not-started'] * 4, 'B11 accidentally starts7C')
    labelled = [(str(n), rows('review-scope.csv' if n == 1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)] + [('7A', rows('review-scope-07.csv'))]
    labelled += [(f'7B{n}', rows(f'review-scope-07B{n}.csv')) for n in range(1,11)] + [('7B11', scopes)]
    ck(rows('evidence/coverage-ledger-07B11.csv') == build_current_ledger(inventory, labelled, v.spans), 'B11 ledger recomputation')
    candidates = rows('evidence/report-candidate-disposition-07B11.csv'); screens = rows('evidence/report-screen-disposition-07B11.csv')
    ck(len(candidates) == 98 and candidates == build_candidate_disposition(inventory, labelled), 'B11 filename98 triage')
    ck(len(screens) == 52 and screens == build_screen_disposition(inventory, labelled), 'B11 screen52 triage')
    v.sequential(screens, 'SC7B11-', 52)
    by = {r['screen']: r for r in screens}
    for name in REVIEWED_BODIES:
        ck(by[name]['phase7B11_body_ranges'] != 'none' and by[name]['coverage_level'] == 'bounded-local-body-and-xaml-not-whole-feature-certified', 'B11 body depth: ' + name)
    prior = {r['path'] for _, selected in labelled[:-1] for r in selected}; selected = set(scope); union = prior | selected
    ck((len(prior),len(selected),len(selected & prior),len(selected-prior),len(union),len(paths-union)) == (381,21,16,5,386,441), 'B11 scope union bookkeeping')
    witness, match = v.recompute('evidence/report-witnesses-07B11.json', 'tools/check_statement_contract_witnesses.py')
    alg, lex = witness['illustrations'], witness['static_lexical_contract_checks']
    v.sequential(alg, 'ALG7B11-', 20); v.sequential(lex, 'ST7B11-', 20); v.related(alg+lex, known)
    for e in witness_metadata_errors(witness): ck(False, e)
    for r in alg + lex:
        flag = 'illustration_assertions_passed' if r['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']), 'B11 witness overclaim: ' + r['id'])
        validate_source(v, r, scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}', scope, 'B11 bounded lexical read', phase=7)
    patterns = [
        (PART_DOCS[0], r'^\| (EX7B11-\d{2}) \|', [r['id'] for r in extensions]),
        (PART_DOCS[1], r'^\| (FE7B11-\d{2}) —', [r['id'] for r in features]),
        (PART_DOCS[1], r'^\| (INV7B11-\d{2}) \|', [r['id'] for r in invs]),
        (PART_DOCS[1], r'^### (RC7B11-\d{2}) —', [r['id'] for r in rc]),
        (PART_DOCS[1], r'^\| (H7B11-\d{2}) —', [r['id'] for r in tables['H7B11-']]),
        (PART_DOCS[1], r'^\| (Q7B11-\d{2}) \|', [r['id'] for r in tables['Q7B11-']]),
        (PART_DOCS[1], r'^\| (BK7B11-\d{2}) \|', [r['id'] for r in tables['BK7B11-']]),
        (PART_DOCS[2], r'^\| (P7B11T-\d{2}) \|', [r['id'] for r in tests]),
        ('IMPROVEMENTS.md', r'^\| (G-\d{2,3}) \|', [f'G-{n:02d}' for n in range(1,147)]),
    ]
    for filename, pattern, expected in patterns:
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M) == expected, 'B11 Markdown IDs: ' + filename)
    pending = False
    src = re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS + SHARED_DOCS:
        doc = v.AUDIT / filename; text = v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', text):
            parsed = urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'): continue
            target = (doc.parent / unquote(parsed.path)).resolve()
            if target == (v.AUDIT/'evidence/checks-07B11.json').resolve() and not target.exists(): pending = True; continue
            v.LINK_COUNT += 1; ck(target.exists(), 'B11 broken link: ' + filename + ':' + m[1])
        for m in src.finditer(text):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS: v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pat, ids in ((r'\bP7B11T-\d{2}\b',tids),(r'\bFE7B11-\d{2}\b',fids),(r'\bINV7B11-\d{2}\b',iids)):
            for item in re.findall(pat,text): ck(item in ids, 'B11 unknown ID: ' + filename + ':' + item)
    summary = {}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            fields=[s.strip() for s in line.replace('**','').strip('|').split('|')];summary[fields[0]]=fields[1:]
    for label, expected in (('التراكمي المفتوح',[287,2,176,108,1]),('7B11 — جديدة',[2,0,1,1,0]),('7B11 — إضافة محدودة',[21,16,5,386])):
        ck(summary.get(label) == list(map(str,expected)), 'B11 README counts: ' + label)
    texts = v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')): ck(False,e)
    for name in SHARED_DOCS:
        ck(all(s in v.read(v.AUDIT/name) for s in ('PHASE-07B11.md','7B12','7C','غير مأذونة','1fbac9e','10ba215')), 'B11 index lacks boundaries: ' + name)
    for name in (PART_DOCS[0],'IMPROVEMENTS.md'):
        text=v.read(v.AUDIT/name)
        ck('2×5=10' in text and '2×12×5=120' in text and 'تصويب' in text, 'B11 additive arithmetic erratum missing: ' + name)
    tools=['check_statement_contract_witnesses.py','validate_statement_contract_part.py','test_statement_contract_audit_validator.py']
    for name in tools:
        try: v.ast.parse(v.read(v.AUDIT/'tools'/name), filename=name)
        except SyntaxError as e: ck(False,'B11 tool syntax: ' + name + ':' + str(e))
    process=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_statement_contract_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',process.stderr+'\n'+process.stdout);count=int(m[1]) if m else None
    passed=process.returncode==0 and count==30;ck(passed,'B11 helper self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_statement_contract_audit_validator.py']=dict(tests_reported=count,expected_tests=30,process_exit_code=process.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B11-287-plus-frozen-history-not-runtime-certification',
        phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9+7B10+7B11-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B12-announced-not-started','7C-not-started'],registry_used='findings.csv',
        historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=115,phase_7B11=2,total_open_not_remediated=287,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:21,'phase_7B10_union_frozen':381,'phase_7B11_overlap_with_prior_union':16,'phase_7B11_new_paths':5,'unique_union_not_line_or_execution_coverage':386,'inventory_only_no_selected_scope':441})
    report['phase_7B10_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=315,historical_check_record_overwritten=False,
        genuine_b10_check_sha256_unchanged=B10_CHECK_SHA,partial7B11_append_only_evidence_extensions_without_reclassification=ext,
        next_phase_followups_preserved_for_all285=True,next_phase_replans_during_partial7={},historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True)
    report['phase_7B11_entry_checkout_reconciliation']=rec
    report['phase_7B11_additive_arithmetic_erratum']=witness['additive_B10_arithmetic_erratum']
    report['evidence_rows'].update(dict(
        phase_7B11_feature_rows_not_completed_features=23,phase_7B11_invariants_not_passed_tests=23,
        phase_7B11_reconciliation_contracts_not_executed_financial_acceptance=6,
        phase_7B11_unexecuted_acceptance_or_gate_plans=25,phase_7B11_direct_finding_plans=4,
        phase_7B11_historical_regression_plans=14,phase_7B11_cross_contract_plans=5,phase_7B11_documentary_scope_authorization_gate_plans=2,
        phase_7B11_historical_extensions_not_new_findings=14,phase_7B11_unresolved_handoffs=6,phase_7B11_unanswered_questions=6,
        phase_7B11_continuation_groups_not_complete=10,phase_7B11_original_paths_in_ledger=827,phase_7B11_filename_candidates_not_feature_count=98,
        phase_7B11_screen_candidates_not_feature_count=52,phase_7B11_independent_illustrations_not_erp_tests=20,
        phase_7B11_bounded_literal_checks_not_application_tests=20,phase_7B11_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=(
        'Read-only documentary checker: original827 path/hashes and source10ba ancestry/net docs-only delta;315 protected prior artifacts '
        'including genuine B10stdout checkouta254 and B9checkout3612700. Frozen285 cores/ALLnext_phase/exact evidence prefixes with14 declared '
        'tails; exactG01..140 rows. HistoricalA/B1..B10 use OWN frozen rows/bytes/exact index texts IN MEMORY, not current287/live files. '
        'B10 direct registry read_bytes is overlaid at one exact logical path via a local Path subclass, never protected-code edits/disk writes/global '
        'pathlib patches. Entry1fbac9e is an already completed320-file B10 docs push, not pending or a source rebaseline. '
        '21 selected paths/three local bodies+XAML/DTO are not all caller/child/template/schema/ACL/policy/deployment contracts. '
        'P7-114 is the confirmed LOCAL supplied-SQL eligibility difference, not certification of deployed SP/schema or observation of cancelled rows. '
        'P7-115 changes the queried database on a second request with unchanged year selection, distinct from post-display print criteria drift. '
        'Default aggregate missing-subNotes P3-022 remains an upstream gate for a populated aggregate result; downstream hand models isolate it '
        'using detail/well-formed rows, not assume its remediation. State/branch/type/sign/endpoints/failure/snapshot/identity/capability roots are not '
        'renumbered. Main-account Type1/lookupType2 and detail Excel stub are functional gaps underP1-033. Main Excel uses typed ClosedXML/XLSX '
        'and SaveAs/dispose before shell; no automatic CSV/formula/finalization claim. EntryOper branch-qualified invoice route is counterevidence '
        'to copying the journal viewer local-number/no-branch route everywhere. Apply-before-Show/disabled menu/new instances are counterevidence, '
        'not deployed role certification; current sources do not establish every caller availability. Period-only vs closing/branch-id mapping and '
        'external DTO/template/settings need contracts, not forced equal totals. Additive arithmetic erratum:2*5=10 vs2*12*5=120; protected B10 '
        'prose/G138/archive are not rewritten and structural checks do not certify all prose.20 manual+20 lexical+30 new synthetic checker cases '
        'are documentation-only;25 acceptance/gate plans not-executed.7B/7 partial,7B12 announced,7C unstarted,8 unauthorized. '
        'No application import/build/C#/SQL/WPF/Office/formula/device/provider/actual export/shell execution, remediation, real data/secrets, '
        'financial/security/compliance certification or latency/index/leak measurement.'
    )
