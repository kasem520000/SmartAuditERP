#!/usr/bin/env python3
"""Read-only recovery/evidence gate; NEVER executes ERP, SQL, SDKs or old dispatchers.

Install the syntax-only dependencies from ../census07b/requirements-census-07B38.txt
into a temporary target. Syntax facts and authored status flags are NOT an
independent proof of semantic completeness. --require-complete exits 2 while
any approved capability still has readable-local work or missing review evidence.
All recovered evidence uses 07B39R1; absent earlier B39 captures are not recreated.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import sys
import xml.parsers.expat

ROOT = Path(__file__).resolve().parents[4]
AUDIT = ROOT / 'docs/audit'
EV = AUDIT / 'evidence'
TAG = '07B39R1'
BASELINE = '10ba215152f722c8808aea0bb672c1d1d4d9d711'
RECOVERED_HEAD = 'f16f3da60c72f243f90f466badc1bade90bf4abd'
CAP_IDS = tuple(f'CAP7B38-D{i:02d}' for i in range(1, 27))
REQUIRED_POLICY_PAIRS = frozenset({('CAP7B38-D02', 'currency'),
    ('CAP7B38-D09', 'VAT'), ('CAP7B38-D10', 'VAT'), ('CAP7B38-D15', 'HR')})
MUTABLE_INDEXES = frozenset({'README.md', 'PLAN.md', 'IMPROVEMENTS.md'})
REF = re.compile(r'(?P<path>SmartAuditERP/[^;\n]+?\.(?:cs|xaml|resx)):(?P<a>\d+)(?:-(?P<b>\d+))?')


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_sha(record: dict) -> str:
    return sha(json.dumps(record, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':')).encode('utf8'))


def load_json(name: str, ev: Path = EV):
    return json.loads((ev / name).read_bytes())


def rows(name: str, ev: Path = EV) -> list[dict]:
    with (ev / name).open(encoding='utf-8-sig', newline='') as stream:
        result = list(csv.DictReader(stream))
    if any(None in r or any(v is None for v in r.values()) for r in result):
        raise ValueError('Malformed CSV: ' + name)
    return result


def decode(raw: bytes) -> str:
    if raw.startswith((b'\xff\xfe', b'\xfe\xff')):
        return raw.decode('utf16')
    try:
        return raw.decode('utf-8-sig')
    except UnicodeDecodeError:
        return raw.decode('cp1256')


def walk(node):
    yield node
    for child in node.named_children:
        yield from walk(child)


class Syntax:
    """A fresh C# syntax tree, not C# execution, binding or WPF observation."""
    def __init__(self, text: str):
        for package, expected in [('tree-sitter', '0.25.2'), ('tree-sitter-c-sharp', '0.23.1')]:
            if version(package) != expected:
                raise ValueError(package + ' version must be ' + expected)
        from tree_sitter import Language, Parser
        import tree_sitter_c_sharp
        self.raw = text.encode('utf8')
        self.tree = Parser(Language(tree_sitter_c_sharp.language())).parse(self.raw)
        if self.tree.root_node.has_error:
            raise ValueError('C# syntax parse error; no repair/reinterpretation attempted')

    def text(self, node) -> str:
        return self.raw[node.start_byte:node.end_byte].decode('utf8') if node else ''

    def method(self, name: str):
        found = [n for n in walk(self.tree.root_node) if n.type == 'method_declaration'
                 and self.text(n.child_by_field_name('name')) == name]
        if len(found) != 1:
            raise ValueError(f'{name}: expected one declaration, found {len(found)}')
        return found[0]

    def calls(self, node) -> list[dict]:
        return [{'function': self.text(n.child_by_field_name('function')),
                 'line': n.start_point.row + 1}
                for n in walk(node) if n.type == 'invocation_expression']

    def method_fact(self, name: str) -> dict:
        node = self.method(name)
        return {'method': name, 'start': node.start_point.row + 1,
                'end': node.end_point.row + 1, 'syntax_utf8_sha256': sha(self.text(node).encode()),
                'calls': self.calls(node),
                'assignments': [{'left': self.text(n.child_by_field_name('left')),
                                 'right': self.text(n.child_by_field_name('right')),
                                 'line': n.start_point.row + 1}
                                for n in walk(node) if n.type == 'assignment_expression']}


def import_tail(text: str, name: str = 'StripImportInv_Click') -> dict:
    """Inspect the actual if consequence and its siblings; do not count braces as text."""
    source = Syntax(text)
    method = source.method(name)
    navigations = [n for n in walk(method) if n.type == 'invocation_expression'
                   and source.text(n.child_by_field_name('function')).rsplit('.', 1)[-1] == 'Navigate']
    if len(navigations) != 1:
        raise ValueError(name + ': expected one syntactic Navigate invocation')
    guard = navigations[0].parent
    while guard and guard != method and guard.type != 'if_statement':
        guard = guard.parent
    if guard is None or guard == method:
        raise ValueError(name + ': Navigate is not nested in an if statement')
    consequence = guard.child_by_field_name('consequence')
    siblings = list(guard.parent.named_children)
    following = siblings[siblings.index(guard) + 1:]
    assignments = []
    for statement in following:
        for n in walk(statement):
            if n.type == 'assignment_expression':
                assignments.append(source.text(n.child_by_field_name('left')))
    inside = [source.text(n.child_by_field_name('left')) for n in walk(consequence)
              if n.type == 'assignment_expression']
    return {'method_start': method.start_point.row + 1, 'method_end': method.end_point.row + 1,
            'guard_line': guard.start_point.row + 1,
            'condition': source.text(guard.child_by_field_name('condition')),
            'consequence_type': consequence.type,
            'assignments_in_consequence': inside,
            'assignments_in_following_sibling_statements': assignments,
            'following_sibling_calls': [call for n in following for call in source.calls(n)],
            'meaning': 'Lexical control-flow boundary only, conditional on normal return and completed earlier setters. No runtime/cancel/alias/default/save/stock claim.'}


def own_wiring(code: str, xaml: str, name: str) -> dict:
    source = Syntax(code)
    xml_hits = []
    parser = xml.parsers.expat.ParserCreate(namespace_separator='|')
    def start(element, attrs):
        for attr, value in attrs.items():
            if value == name:
                xml_hits.append({'line': parser.CurrentLineNumber,
                                 'attribute': attr.rsplit('|', 1)[-1]})
    parser.StartElementHandler = start
    parser.Parse(xaml.encode('utf8'), True)
    direct_calls = [c for c in source.calls(source.tree.root_node)
                    if c['function'].rsplit('.', 1)[-1] == name]
    method_groups = []
    for n in walk(source.tree.root_node):
        if n.type == 'assignment_expression':
            rhs = source.text(n.child_by_field_name('right'))
            if rhs in {name, 'this.' + name}:
                method_groups.append(n.start_point.row + 1)
    return {'own_xaml_literal_references': xml_hits, 'own_code_direct_invocations': direct_calls,
            'own_code_simple_method_group_assignments': method_groups,
            'limit': 'Searched this class code and its own XAML only. Not typed reachability, inherited/reflection/resource binding, authorization, or proof of global unreachability.'}


# Explicitly selected, freshly reviewed contexts; not a hidden whole-repository claim.
METHOD_CONTEXTS = {
 'frmPurchInv': ['btnInvSrch_Click', 'Navigate', 'ReadData'],
 'frmInvoiceSrch': ['RefreshDisplayRows', 'dgvItems_MouseDoubleClick', 'BtnReturn_Click', 'IsPreviousReturned'],
 'frmInvPurch': ['stripExport_Click'],
 'frmCloseShift': ['ExportToExcel'],
 'frmEmpInvs': ['WireUpEvents', 'BtnExport_Click'],
 'frmAccountsDirectory': ['btnExportExcel_Click', 'ExportToExcel'],
 'frmEntriesSyncStatus': ['BindToData', 'PrintDevexpress'],
 'frmReceiptsSyncStatus': ['BindToData', 'PrintDevexpress'],
 'frmInventoryTransfer': ['StripImportInv_Click', 'LoadInvoiceNumber', 'btnInvSrch_Click',
                          'btnReceiveQuantity_Click', 'BtnInvertoryOrder_Click', 'btnInsertPurch_Click'],
 'frmInvInputOutput': ['StripImportInv_Click', 'stripExport_Click', 'ExportDataGridToExcel'],
 'frmInvPOS': ['StripImportInv_Click', 'stripExport_Click', 'ExportDataGridToExcel'],
 'frmInvoiceDeliveries': ['btnExportExcel_Click', 'ExportToExcel'],
 'frmInvSale': ['stripExport_Click', 'ExportDataGridToExcel'],
 'frmCustAccountGet': ['ExportToExcel', 'ExportToCsv', 'BtnExport_Click'],
 'FrmNewEntry': ['btnExport_Click', 'ExportToHtml'],
 'frmNetsales': ['btnExport_Click', 'ExportToExcelHtml'],
 'frmSafeGrd': ['btnPreview_Click', 'btnPrint_Click', 'PrintReport'],
 'frmSafesTransfer': ['btnPrint_Click', 'btnView_Click', 'PrintReport'],
 'frmSandQ': ['btnPrint_Click', 'btnView_Click', 'PrintReceipt'],
 'frmStocksSync': ['btnPrint_Click', 'btnPreview_Click', 'PrintReport'],
 'frmPrintBill': ['Button1_Click', 'print'],
 'frmcontract': ['SetupButtonEvents', 'btnSavePrint_Click', 'btnPrint_Click', 'btnView_Click', 'SaveAndPrint'],
}


def derive_source_facts(root: Path = ROOT) -> dict:
    facts = {'schema_version': 1, 'source_identity': {}, 'methods': {}, 'import_tails': {}, 'wiring': {},
             'execution_count': 0, 'limit': 'Syntactic evidence supporting explicit bounded reviewer conclusions, not binding, runtime, completeness or external certification.'}
    for stem, methods in METHOD_CONTEXTS.items():
        rel = f'SmartAuditERP/Form_WPF/{stem}.xaml.cs'
        raw = (root / rel).read_bytes(); text = decode(raw); parsed = Syntax(text)
        facts['source_identity'][rel] = sha(raw)
        facts['methods'][stem] = [parsed.method_fact(name) for name in methods]
        xrel = rel[:-3]
        xraw = (root / xrel).read_bytes(); facts['source_identity'][xrel] = sha(xraw)
        selected = methods if stem not in {'frmInventoryTransfer', 'frmInvInputOutput', 'frmInvPOS'} else ['StripImportInv_Click']
        facts['wiring'][stem] = {m: own_wiring(text, decode(xraw), m) for m in selected}
        if stem in {'frmInventoryTransfer', 'frmInvInputOutput', 'frmInvPOS'}:
            facts['import_tails'][stem] = import_tail(text)
    # Key producer is separate from selector and consumer; do not infer from a UI label.
    rel = 'SmartAuditERP/Class/InvoiceOper.cs'; raw = (root / rel).read_bytes(); parsed = Syntax(decode(raw))
    facts['source_identity'][rel] = sha(raw)
    facts['methods']['InvoiceOper'] = [parsed.method_fact('GetInvoiceGlobalID'),
        parsed.method_fact('IsPreviousReturned'), parsed.method_fact('ToArabicLetter')]
    return facts


def evaluate_exit(authority: dict, capabilities: list[dict], policies: list[dict]) -> dict:
    """Documentary gate; it cannot authenticate that a reviewer really read every line."""
    blockers = []
    if authority.get('whole7b_scope') != 'approve_scope' or authority.get('approved_capability_ids') != list(CAP_IDS):
        blockers.append('approved-26-capability-scope-not-established')
    if authority.get('whole7b_external_exit') != 'static_with_accepted_handoffs':
        blockers.append('evidence-backed-static-handoff-exit-not-authorized')
    ids = [r.get('capability_id') for r in capabilities]
    if len(ids) != len(set(ids)) or set(ids) != set(CAP_IDS):
        blockers.append('capability-identity-set-missing-extra-or-duplicate')
    for cap in capabilities:
        cid = cap.get('capability_id', '<missing>')
        if cap.get('local_semantic_obligations_complete') != 'true':
            blockers.append(cid + ':readable-local-evidence-open')
        if cap.get('independent_exit_review') != 'verified-with-source-evidence' or not cap.get('local_completion_evidence'):
            blockers.append(cid + ':independent-local-exit-not-established')
        # Labelling readable work as external or assigning an owner never completes it.
        if cap.get('readable_local_work_transferred_to_external') != 'false':
            blockers.append(cid + ':readable-local-work-cannot-be-externalized')
    actual_pairs = {(r.get('capability_id'), r.get('policy_family')) for r in policies}
    for pair in sorted(REQUIRED_POLICY_PAIRS - actual_pairs):
        blockers.append(':'.join(pair) + ':specific-policy-owner-boundary-missing')
    for row in policies:
        required = ('entry_point', 'source_contract', 'output_boundary', 'source_evidence',
                    'exclusions', 'owner_role', 'required_redacted_input', 'absence_impact',
                    'next_action', 'static_exit_criterion')
        if not all(isinstance(row.get(k), str) and row[k].strip() for k in required):
            blockers.append(row.get('id', '<missing>') + ':external-disposition-incomplete')
        if row.get('provided') != 'false' or row.get('certified') != 'false':
            blockers.append(row.get('id', '<missing>') + ':unsupported-contract-certification')
    return {'whole_7B_static_assessment_complete': not blockers, 'blockers': blockers,
            'external_contracts_certified': False, 'phase7_complete': False,
            'phase7C_started': False, 'phase8_authorized': False,
            'application_remediation_performed': False, 'application_execution_count': 0,
            'repair_start_and_synchronization': 'unknown',
            'meaning': 'Integrity and status checks are not independent semantic completeness, financial/operational acceptance, or external contract certification.'}


def reference_errors(text: str, root: Path = ROOT) -> list[str]:
    errors = []
    for m in REF.finditer(text):
        p = root / m['path']
        if not p.is_file():
            errors.append('Missing source: ' + m['path']); continue
        a, b = int(m['a']), int(m['b'] or m['a'])
        if not 1 <= a <= b <= len(decode(p.read_bytes()).splitlines()):
            errors.append('Invalid source range: ' + m[0])
    return errors


def validate(root: Path = ROOT, *, rederive: bool = False) -> dict:
    audit = root / 'docs/audit'; ev = audit / 'evidence'; errors = []; groups = []
    def check(ok, message):
        if not ok:
            errors.append(message)
    identity = load_json('recovered-input-identities-' + TAG + '.json', ev)
    check(identity['recovered_HEAD'] == RECOVERED_HEAD, 'restored branch identity')
    for rel, info in identity['audit_files'].items():
        p = audit / rel
        if not p.is_file():
            errors.append('Missing preserved input: ' + rel); continue
        raw = p.read_bytes()
        if rel in MUTABLE_INDEXES:
            check(len(raw) >= info['bytes'] and sha(raw[-info['bytes']:]) == info['sha256'], 'historical index suffix drift: ' + rel)
        else:
            check(len(raw) == info['bytes'] and sha(raw) == info['sha256'], 'protected input drift: ' + rel)
    inventory = rows('inventory.csv', ev)
    check(len(inventory) == 827, '827 original identities')
    for row in inventory:
        p = root / row['path']; check(p.is_file() and sha(p.read_bytes()) == row['sha256'], 'original drift: ' + row['path'])
    raw = (audit / 'findings.csv').read_bytes(); original = rows('../findings.csv', ev)
    check(len(original) == 335 and len(raw) == 222939 and raw.count(b'\r\n') == 336 and not raw.startswith(b'\xef\xbb\xbf') and sha(raw) == 'ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a', 'raw335/all-fields/336CRLF preservation')
    groups.append('recovered1266-audit-inputs/827-originals/raw335-registry-preserved')
    authority = load_json('scope-approval-recovered-' + TAG + '.json', ev)
    check(authority['scope_register_sha256'] == sha((ev / 'capability-register-07B38.csv').read_bytes()), 'later scope source identity')
    check(authority['reconstructed_original_UI_payload'] is False and authority['blanket_completion_approval'] is False, 'recovered user choice misrepresented')
    historical = load_json('closure-inputs-07B38.json', ev)
    check(historical['scope_approval'] is None and historical['external_handoff_acceptance'] is None and historical['whole_7B_complete'] is False, 'historical B38 approval rewritten')
    date = load_json('date-prospective-' + TAG + '.json', ev)
    check(date['historical_artifacts_retimestamped'] is False and date['clock_is_calendar_certification'] is False, 'capture provenance/calendar promoted')
    groups.append('later-user-scope-and-handoff-authority-not-retroactive-B38-approval')
    review = load_json('source-review-log-' + TAG + '.json', ev)
    for row in review['reviewed_ranges']:
        p = root / row['path']; lines = decode(p.read_bytes()).splitlines()
        check(sha(p.read_bytes()) == row['source_sha256'], 'review source drift: ' + row['path'])
        check(1 <= row['first_line'] <= row['last_line'] <= len(lines), 'review range invalid: ' + row['path'])
        excerpt = '\n'.join(lines[row['first_line']-1:row['last_line']]) + '\n'
        check(sha(excerpt.encode()) == row['normalized_excerpt_sha256'], 'review excerpt drift')
        check(row['whole_file_review_claimed'] is False, 'partial view relabelled whole-file')
    facts = load_json('source-facts-' + TAG + '.json', ev)
    for rel, h in facts['source_identity'].items():
        check(sha((root / rel).read_bytes()) == h, 'source fact input drift: ' + rel)
    if rederive:
        check(derive_source_facts(root) == facts, 'fresh independent syntax facts differ')
    transfer = facts['import_tails']['frmInventoryTransfer']
    guarded = facts['import_tails']['frmInvInputOutput']
    check(transfer['consequence_type'] == 'expression_statement' and '_invoic.ISNew' in transfer['assignments_in_following_sibling_statements'], 'Transfer brace/tail boundary')
    check(guarded['consequence_type'] == 'block' and 'Invoic.ISNew' in guarded['assignments_in_consequence'] and not guarded['assignments_in_following_sibling_statements'], 'guarded InputOutput control conflated')
    wiring = facts['wiring']['frmInventoryTransfer']['StripImportInv_Click']
    check(not wiring['own_xaml_literal_references'] and not wiring['own_code_direct_invocations'] and not wiring['own_code_simple_method_group_assignments'], 'Transfer declaration-only local search changed')
    check(bool(facts['wiring']['frmInvPOS']['StripImportInv_Click']['own_xaml_literal_references']), 'POS own XAML binding absent')
    groups.append('fresh-source-evidence/actual-if-consequence/own-XAML-not-global-reachability')
    caps = rows('capability-recovery-state-' + TAG + '.csv', ev)
    upstream = rows('capability-register-07B38.csv', ev)
    upstream_by_id = {r['id']: r for r in upstream}
    for row in caps:
        old = upstream_by_id.get(row['capability_id'], {})
        check(row['upstream_row_sha256'] == canonical_sha(old) and json.loads(row['canonical_upstream_row_json']) == old, 'full capability ancestry')
    ancestry = load_json('ancestry-recovery-map-' + TAG + '.json', ev)
    for bundle in ancestry['bundles']:
        source_rows = rows(bundle['upstream_artifact'].removeprefix('evidence/'), ev)
        check(bundle['upstream_file_sha256'] == sha((audit / bundle['upstream_artifact']).read_bytes()), 'ancestry file drift')
        check(len(bundle['records']) == len(source_rows), 'ancestry row omission')
        for record, old in zip(bundle['records'], source_rows):
            check(record['canonical_upstream_row'] == old and record['upstream_row_sha256'] == canonical_sha(old), 'ancestry dictionary/hash drift')
    policies = rows('policy-boundaries-' + TAG + '.csv', ev)
    for row in policies:
        errors.extend(reference_errors(row['source_evidence'], root))
    gate = evaluate_exit(authority, caps, policies)
    check(gate['whole_7B_static_assessment_complete'] is False, 'unsubstantiated recovery completion claim')
    groups.append('26-capability-owned-local-blockers/RS14-SP3-RW4-BK10-preserved/no-externalizing-local-work')
    additions = rows('findings-additions-' + TAG + '.csv', ev)
    check([r['id'] for r in additions] == ['P7-164','P7-165','P7-166','P7-167'], 'four re-established root identities')
    check(not ({r['id'] for r in original} & {r['id'] for r in additions}), 'finding double-count')
    for row in additions:
        check(row['certainty'] == 'confirmed' and row['status'] == 'open-not-remediated', 'new root certainty/status')
        errors.extend(reference_errors(row['evidence'], root))
    extensions = load_json('finding-extensions-' + TAG + '.json', ev)
    check([r['finding_id'] for r in extensions['extensions']] == ['P7-050', 'P1-033', 'P7-160'], 'same-root extension identities')
    for extension in extensions['extensions']:
        for route in extension['routes']:
            errors.extend(reference_errors(route['source_evidence'], root))
    groups.append('four-open-roots/three-same-root-extensions/not-one-finding-per-gesture')
    return {'schema_version': 1, 'kind': 'recovery-documentary-integrity-not-completion',
        'integrity_ok': not errors, 'errors': errors, 'groups': groups, 'static_exit': gate,
        'counts': {'original_application_files': len(inventory), 'unchanged_original_findings': len(original),
                   'reestablished_open_roots': len(additions), 'same_root_extensions_not_new_findings': len(extensions['extensions']),
                   'effective_findings_with_supplement': len(original) + len(additions),
                   'effective_severity': dict(Counter(r['severity'] for r in original + additions)),
                   'recovered_historical_audit_files': len(identity['audit_files']),
                   'operative_capability_rows': len(caps), 'specific_policy_records_not_all_external_contracts': len(policies),
                   'all_recursive_audit_python_tools': len(list((audit / 'tools').rglob('*.py')))},
        'fresh_source_syntax_fact_rederivation': rederive,
        'missing_previous_B39_artifacts_recreated': False, 'old_dispatcher_executed': False,
        'application_execution_count': 0, 'application_remediation_performed': False,
        'phase7C_started': False, 'phase8_authorized': False,
        'repair_start_and_synchronization': 'unknown'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true')
    parser.add_argument('--rederive', action='store_true')
    args = parser.parse_args()
    try:
        report = validate(rederive=args.rederive)
    except (OSError, ValueError, KeyError, ImportError) as exc:
        report = {'integrity_ok': False, 'errors': [str(exc)],
                  'static_exit': {'whole_7B_static_assessment_complete': False}}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not report['integrity_ok']:
        return 1
    return 2 if args.require_complete and not report['static_exit']['whole_7B_static_assessment_complete'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
