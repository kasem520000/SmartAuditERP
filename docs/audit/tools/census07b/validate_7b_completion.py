#!/usr/bin/env python3
"""Read-only integrity checks and a separate, fail-closed WHOLE-7B closure gate.

A successful integrity exit is NOT a completed audit or ERP acceptance. Use
--require-complete for a nonzero (2) exit when valid evidence still says open.
--reparse optionally regenerates the discovery snapshot IN MEMORY and compares
it exactly, using the pinned syntax-only dependencies. No legacy dispatcher,
Path, subprocess, frozen tests, source, registry or capture is patched.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import re
import sys

from build_7b_census import (BASELINE, ROOT, compact_spans, decode_source,
                             numeric_spans, read_rows, row_sha, sha)

AUDIT = ROOT / 'docs/audit'
EVIDENCE = AUDIT / 'evidence'
SELECTED_DIALOGS = frozenset({'frmItemsSrch', 'frmInvoiceSrch', 'frmInvoiceItems',
                              'frmItemProperties', 'frmEditItems'})
REQUIRED_CAPABILITY_FIELDS = frozenset({'id', 'capability', 'entry_point',
    'source_contract', 'output_boundary', 'excluded_from_claim', 'owner_role',
    'required_redacted_input', 'absence_impact', 'next_action',
    'static_exit_criterion', 'current_handoff_ids'})
CLOSURE_FLAGS = ('all_local_semantic_obligations_complete',
    'all_required_candidates_dispositioned', 'all_open_observations_adjudicated')
APPROVAL_FIELDS = ('scope_approval', 'external_handoff_acceptance', 'whole_family_approval')
REF = re.compile(r'(?P<path>(?:SmartAuditERP|AutoUpdater)/[^;\n]+?\.(?:cs|xaml|resx)):(?P<a>\d+)(?:[-–](?P<b>\d+))?')


def is_approval(record) -> bool:
    return (isinstance(record, dict) and record.get('decision') == 'approved'
            and isinstance(record.get('owner_role'), str) and bool(record['owner_role'].strip())
            and isinstance(record.get('source_evidence'), str) and bool(record['source_evidence'].strip()))


def evaluate_closure(inputs: dict, capabilities: list[dict]) -> dict:
    """Counts, successful tests, dispositions and handoff IDs never grant approval."""
    blockers = []
    for key in APPROVAL_FIELDS:
        if not is_approval(inputs.get(key)):
            blockers.append(key + '-not-approved')
    for key in CLOSURE_FLAGS:
        if inputs.get(key) is not True:
            blockers.append(key + '-not-proven')
    if not capabilities:
        blockers.append('empty-capability-register')
    if any(r.get('local_semantic_obligations_complete') != 'true' for r in capabilities):
        blockers.append('capability-local-obligations-open')
    if any(r.get('whole_capability_certified') != 'true' for r in capabilities):
        blockers.append('whole-capability-decisions-open')
    if inputs.get('phase_7C_started') is not False or inputs.get('phase_8_authorized') is not False:
        blockers.append('phase-boundary-changed')
    if inputs.get('application_remediation_performed') is not False:
        blockers.append('audit-only-boundary-changed')
    return {'whole_7B_complete': not blockers, 'blockers': blockers,
            'meaning': 'Static-audit closure only; never ERP, financial, repair or deployment acceptance.'}


def lineage_errors(actual: list[dict], upstream: dict[str, list[dict]],
                   file_hashes: dict[str, str]) -> list[str]:
    errors = []
    expected = [(part, ordinal, row) for part in range(1, 38)
                for ordinal, row in enumerate(upstream[f'7B{part}'], 1)]
    if len(actual) != len(expected):
        errors.append('lineage row count/omission')
    identities = [(r.get('upstream_artifact'), r.get('upstream_id')) for r in actual]
    if len(identities) != len(set(identities)):
        errors.append('lineage duplicate upstream identity')
    for row, (part, ordinal, old) in zip(actual, expected):
        rel = f'evidence/feature-implementation-matrix-07B{part}.csv'
        if (row.get('part'), row.get('upstream_artifact'), row.get('upstream_ordinal'),
            row.get('upstream_id'), row.get('upstream_row_sha256'), row.get('upstream_file_sha256')) != (
                f'7B{part}', rel, str(ordinal), old['id'], row_sha(old), file_hashes[rel]):
            errors.append('lineage ancestry/ordinal/hash: ' + str(row.get('id')))
        try:
            same = json.loads(row.get('canonical_row_json', '')) == old
        except (TypeError, ValueError):
            same = False
        if not same:
            errors.append('lineage dictionary: ' + str(row.get('id')))
        if row.get('prior_evidence') != old.get('evidence', '') or row.get('prior_acceptance_ids') != old.get('acceptance_ids', ''):
            errors.append('lineage evidence/acceptance rewritten: ' + str(row.get('id')))
    return errors


def check_references(text: str, root: Path = ROOT) -> list[str]:
    errors = []
    for match in REF.finditer(text):
        path = root / match['path']
        if not path.is_file():
            errors.append('Missing source reference: ' + match['path'])
            continue
        total = len(decode_source(path.read_bytes())[0].splitlines())
        first, last = int(match['a']), int(match['b'] or match['a'])
        if not 1 <= first <= last <= total:
            errors.append('Invalid source range: ' + match[0])
    return errors


def validate(audit: Path = AUDIT, *, reparse: bool = False) -> dict:
    root, ev = audit.parents[1], audit / 'evidence'
    errors = []
    groups = []

    def check(ok, message):
        if not ok:
            errors.append(message)

    def data(name):
        return json.loads((ev / name).read_bytes())

    registry_raw = (audit / 'findings.csv').read_bytes()
    registry = read_rows(audit / 'findings.csv')
    inventory = read_rows(ev / 'inventory.csv')
    preservation = data('preservation-07B38.json')
    check(preservation['application_baseline'] == BASELINE, 'application baseline identity')
    check(len(inventory) == 827, '827-original inventory')
    for row in inventory:
        p = root / row['path']
        check(p.is_file() and sha(p.read_bytes()) == row['sha256'], 'original source/artifact drift: ' + row['path'])
    check(sha(registry_raw) == preservation['registry_sha256'] == 'ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a', 'ALL335 raw registry identity')
    check(len(registry) == 335 and len(registry_raw) == 222939 and registry_raw.count(b'\r\n') == 336 and not registry_raw.startswith(b'\xef\xbb\xbf'), 'registry335/raw336CRLF/bytes/BOM')
    check(len(preservation['protected_artifact_sha256']) == 1226, 'protected1226 count')
    for path, expected in preservation['protected_artifact_sha256'].items():
        p = audit / path
        check(p.is_file() and sha(p.read_bytes()) == expected, 'protected audit drift: ' + path)
    top_tools = {p.relative_to(audit).as_posix(): sha(p.read_bytes()) for p in (audit / 'tools').glob('*.py')}
    check(top_tools == preservation['legacy_checker_sha256'] and len(top_tools) == 139, 'legacy139 tools incl dispatcher changed')
    groups.append('827-originals/335-registry/1226-protected/139-legacy-tools')

    census = data('capability-census-07B38.json')
    check(census['application_baseline'] == BASELINE and census['audit_reference_date_utc'] == '2026-11-16', 'census baseline/reference')
    check(census['source_inventory_sha256'] == sha((ev / 'inventory.csv').read_bytes()), 'census inventory hash')
    csharp = {r['path'] for r in inventory if r['kind'] == 'source' and r['path'].endswith('.cs')}
    xaml = {r['path'] for r in inventory if r['kind'] == 'source' and r['path'].endswith('.xaml')}
    check({r['path'] for r in census['source_files']} == csharp and len(csharp) == 477, 'source-kind C# census set')
    check({r['path'] for r in census['xaml_files']} == xaml and len(xaml) == 277, 'source-kind XAML census set')
    files = {r['path']: r for r in census['source_files'] + census['xaml_files']}
    for row in files.values():
        raw = (root / row['path']).read_bytes()
        check(row['sha256'] == sha(raw) and row['lines'] == len(decode_source(raw)[0].splitlines()), 'census file hash/line count: ' + row['path'])
    check(len(census['methods']) == census['summary']['declarations'] == 8997, 'declaration count')
    check(len(census['candidate_sites']) == census['summary']['candidate_sites'] == 4409, 'candidate count')
    check(len(census['xaml_entry_attributes']) == census['summary']['xaml_entry_attributes'] == 4144, 'XAML entry-attribute count')
    for row in census['methods']:
        check(row['path'] in csharp and 1 <= row['start'] <= row['end'] <= files[row['path']]['lines'], 'declaration path/range')
    for row in census['candidate_sites']:
        check(row['path'] in csharp and 1 <= row['line'] <= row['end_line'] <= files[row['path']]['lines'], 'candidate path/range')
    check(census['summary']['csharp_grammar_error_paths'] == [] and census['summary']['xml_error_paths'] == [], 'discovery grammar/XML errors')
    check(census['capability_denominator_agreed'] is False and census['whole_7B_complete'] is False and len(census['limitations']) >= 8, 'discovery promoted to closure')
    check(census['summary']['direct_item_picker_constructions'] == 28 and census['summary']['direct_invoice_picker_constructions'] == 16, 'direct picker counts')
    for row in census['historical_scope_inputs']:
        check(sha((audit / row['path']).read_bytes()) == row['sha256'], 'historical scope input drift')
    namespace = data('census-tool-namespace-note-07B38.json')
    check(sha((audit / namespace['final_builder_path']).read_bytes()) == namespace['final_builder_sha256'], 'final census builder drift')
    check(sha((ev / 'capability-census-07B38.json').read_bytes()) == namespace['snapshot_sha256'], 'exclusive snapshot drift')
    reparsed = False
    if reparse:
        from build_7b_census import build
        check(build(root) == census, 'full fresh in-memory syntax discovery differs from captured snapshot')
        reparsed = True
    groups.append('syntax-discovery-is-not-semantic-review')

    capabilities = read_rows(ev / 'capability-register-07B38.csv')
    cap_ids = {r['id'] for r in capabilities}
    check(len(capabilities) == len(cap_ids) == 26, 'capability proposal26 identities')
    findings = {r['id'] for r in registry}
    handoffs = read_rows(ev / 'handoffs-07B38.csv')
    handoff_ids = {r['id'] for r in handoffs}
    check(len(handoffs) == len(handoff_ids) == 6, 'handoff6 identities')
    for row in capabilities:
        check(all(isinstance(row.get(k), str) and row[k].strip() for k in REQUIRED_CAPABILITY_FIELDS), 'capability boundary/owner/input/exit missing')
        check(set(filter(None, row['related_finding_ids'].split(';'))) <= findings, 'capability finding ID')
        check(set(row['current_handoff_ids'].split(';')) <= handoff_ids, 'capability handoff ID')
        check(row['whole_capability_certified'] == row['local_semantic_obligations_complete'] == 'false', 'unapproved capability silently closed')
    for row in handoffs:
        check(row['approval'] == 'not-received' and row['runtime_status'] == 'not-executed', 'handoff is not approval')
    groups.append('26-proposed-semantic-workstreams-and6-unapproved-handoffs')

    upstream, hashes = {}, {}
    for part in range(1, 38):
        rel = f'evidence/feature-implementation-matrix-07B{part}.csv'
        upstream[f'7B{part}'] = read_rows(audit / rel)
        hashes[rel] = sha((audit / rel).read_bytes())
    lineage = read_rows(ev / 'feature-lineage-07B38.csv')
    errors.extend(lineage_errors(lineage, upstream, hashes))
    check(len(lineage) == 797, 'all797 lineage')
    for row in lineage:
        part = row['part'][2:]
        related = {r['id'] for r in capabilities if part in r['related_part_numbers'].split(';')}
        check(set(row['related_capability_ids'].split(';')) == related and bool(related), 'lineage phase-level navigation links')
        check(row['mapping_basis'] == 'phase-level-many-to-many-navigation-only-not-row-semantic-certification', 'lineage mapping overclaim')
        check(row['current_disposition'] == 'historical-assessment-retained-not-rereviewed-by-indexing', 'lineage rereview overclaim')
    # Independently join the first455 to the old B17 aggregation without retyping.
    old455 = read_rows(ev / 'capability-ledger-07B17.csv')
    check([(r['upstream_artifact'], r['upstream_id'], r['upstream_row_sha256']) for r in lineage[:455]] ==
          [(r['upstream_artifact'], r['upstream_id'], r['upstream_row_sha256']) for r in old455], 'historical455 identity crosswalk')
    groups.append('all797-FE-file-row-provenance-not797-unique-capabilities')

    screens = read_rows(ev / 'screen-crosswalk-07B38.csv')
    check(len(screens) == len(census['seed_screens']) == 55, 'seed screen crosswalk55')
    for row, old in zip(screens, census['seed_screens']):
        check(all(row.get(k) == str(v) for k, v in old.items()), 'seed crosswalk differs from discovery')
        check(row['capability_scope_status'] == 'historical-seed-not-exhaustive-or-certified', 'seed promoted to denominator')
    groups.append('55-historical-seeds-and-inclusive-singleton-range-union')

    dialogs = read_rows(ev / 'direct-dialog-contracts-07B38.csv')
    selected = [s for s in census['candidate_sites'] if s['kind'] == 'constructor-syntax-only' and s['target'] in SELECTED_DIALOGS]
    check(len(dialogs) == len(selected) == 49, 'all49 explicit modal sites')
    for row, site in zip(dialogs, selected):
        check((row['path'], row['target'], row['construction_line'], row['owner'], row['owner_start'], row['owner_end']) ==
              (site['path'], site['target'], str(site['line']), site['owner'], str(site['owner_start']), str(site['owner_end'])), 'modal site ancestry/range')
        check(row['source_sha256'] == files[row['path']]['sha256'], 'modal source hash')
        check(all(row.get(k) for k in ('request_boundary', 'acceptance_guard', 'output_boundary', 'nonaccept_or_followup_boundary', 'interpretation_limit')), 'modal contract fields')
        check(row['runtime_status'] == 'not-executed', 'modal runtime overclaim')
        errors.extend(check_references(row['evidence'], root))
    scope = read_rows(audit / 'review-scope-07B38.csv')
    covered = {}
    for row in scope:
        total = files[row['path']]['lines']
        lines = set()
        for first, last in numeric_spans(row['ranges']):
            check(1 <= first <= last <= total, 'current declared review range')
            lines.update(range(first, last + 1))
        covered[row['path']] = lines
    check(len(scope) == 43, '43 current manually-reviewed source paths')
    check(len({(s['path'], s['owner_start'], s['owner_end']) for s in selected}) == 47, '47 modal owner contexts')
    for site in selected:
        check(set(range(site['owner_start'], site['owner_end'] + 1)) <= covered.get(site['path'], set()), 'modal owner is not in manual review scope')
    groups.append('49-direct-modal-sites-in47-manually-reviewed-owner-contexts')

    residuals = read_rows(ev / 'residual-disposition-07B38.csv')
    old_residuals = read_rows(ev / 'residual-disposition-07B37.csv')
    check(len(residuals) == len(old_residuals) == 14, 'all14 residuals')
    for row, old in zip(residuals, old_residuals):
        check((row['upstream_residual_id'], row['upstream_artifact'], row['upstream_row_sha256'], row['upstream_contract_ids']) ==
              (old['id'], 'evidence/residual-disposition-07B37.csv', row_sha(old), old['upstream_contract_ids']), 'residual ancestry/contracts')
        check(row['disposition'] == row['upstream_disposition'] == old['disposition'], 'residual disposition promoted')
        check(row['upstream_required_input'] == old['required_redacted_input'] and row['required_redacted_input'].startswith(old['required_redacted_input']), 'residual full inherited input prefix')
        check(set(row['capability_ids'].split(';')) <= cap_ids and set(row['current_handoff_ids'].split(';')) <= handoff_ids, 'residual routes')
        check(row['closure_approved'] == 'false', 'residual handoff treated as closure')
    splits = read_rows(ev / 'split-register-07B38.csv')
    old_splits = read_rows(ev / 'split-register-07B37.csv')
    check(len(splits) == len(old_splits) == 3, 'all3 splits')
    for row, old in zip(splits, old_splits):
        check(row['upstream_split_id'] == old['id'] and row['upstream_row_sha256'] == row_sha(old) and json.loads(row['canonical_upstream_row_json']) == old, 'split exact ancestry')
        check(row['whole_split_complete'] == 'false' and set(row['capability_ids'].split(';')) <= cap_ids, 'split silently closed')
    groups.append('RS14/SP3-full-ancestry-inputs-contracts-and-open-dispositions')

    closure_inputs = data('closure-inputs-07B38.json')
    check(closure_inputs['audit_reference_date_utc'] == '2026-11-16', 'current governing reference not raw-clock inference')
    check(closure_inputs['whole_7B_complete'] is False and closure_inputs['repair_start_and_synchronization'] == 'unknown', 'whole7B/repair overclaim')
    for observation in closure_inputs['unresolved_observations']:
        check(observation['capability_id'] in cap_ids and bool(observation['next_action']), 'unresolved observation route')
        errors.extend(check_references(observation['evidence'], root))
    closure = evaluate_closure(closure_inputs, capabilities)
    check(closure['whole_7B_complete'] is False, 'unapproved whole7B closure')
    recursive_tools = sorted((audit / 'tools').rglob('*.py'))
    for path in recursive_tools:
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    groups.append('integrity-success-is-separate-from-fail-closed-completion-gate')
    return {'audit_reference_date_utc': '2026-11-16', 'application_baseline': BASELINE,
        'integrity_errors': errors, 'integrity_check_groups': groups,
        'integrity_ok': not errors, 'closure': closure,
        'counts': {'originals': len(inventory), 'findings_unchanged': len(registry),
            'protected_consumed_artifacts': len(preservation['protected_artifact_sha256']),
            'legacy_top_level_python_tools_unchanged': len(top_tools),
            'all_recursive_audit_python_tools': len(recursive_tools),
            'historical_FE_rows': len(lineage), 'proposed_semantic_workstreams_not_agreed': len(capabilities),
            'source_CSharp_syntax_files': len(csharp), 'source_XAML_XML_files': len(xaml),
            'discovery_candidates_not_semantically_dispositioned': len(census['candidate_sites']),
            'historical_seed_screens_not_denominator': len(screens),
            'direct_modal_sites_reviewed': len(dialogs), 'distinct_modal_owner_contexts': 47,
            'current_review_scope_paths': len(scope)},
        'fresh_full_in_memory_reparse_compared': reparsed,
        'new_checker_source_sha256': {p.relative_to(audit).as_posix(): sha(p.read_bytes())
                                     for p in recursive_tools if p.parent.name == 'census07b'},
        'legacy_dispatcher_modified': False, 'ERP_or_SQL_runtime_tests_executed': 0,
        'application_remediation_performed': False, 'phase_7C_started': False,
        'phase_8_authorized': False,
        'limits': ['All797 rows have exact lineage, not797 distinct capabilities or fresh source reviews.',
            'Syntax discovery, name matching and historical range union do not prove semantic completeness.',
            'Readily reviewable local work remains local; external contracts do not excuse local omissions.',
            'No complete7B/7, runtime, repair synchronization, financial, SDK/template or deployment acceptance.']}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reparse', action='store_true')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    try:
        report = validate(reparse=args.reparse)
    except (OSError, ValueError, KeyError, ImportError) as exc:
        print(json.dumps({'integrity_ok': False, 'integrity_errors': [str(exc)],
                          'closure': {'whole_7B_complete': False}}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['integrity_ok']:
        return 1
    return 2 if args.require_complete and not report['closure']['whole_7B_complete'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
