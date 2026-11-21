#!/usr/bin/env python3
"""R4 read-only, syntax-only evidence checker, not ERP execution or an exit oracle.

Re-established after R2/R3 files proved unavailable. Uses the recovered R1 parser
and its pinned requirements; never reconstructs those absent captures or results.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import re
import sys
import xml.parsers.expat

import verify_recovery_exit as base

ROOT = base.ROOT
EV = base.EV
TAG = '07B39R4'
FACTS = 'document-receiver-source-facts-' + TAG + '.json'
READS = 'document-receiver-source-review-log-' + TAG + '.json'
REVIEW = 'document-receiver-dispositions-' + TAG + '.json'
ITEM = 'item-entry-root-adjudication-' + TAG + '.json'
SCREEN = 'item-entry-prior-root-screen-' + TAG + '.json'
ROUTES = 'document-open-request-matrix-' + TAG + '.json'
SNAPSHOT = 'recovered-baseline-' + TAG + '.json'
BOUNDARIES = 'document-receiver-external-boundaries-' + TAG + '.csv'
P = 'SmartAuditERP/Form_WPF/'
C = 'SmartAuditERP/Class/'
IP = C + 'InvoiceOper.cs'
AGG = P + 'frmRptItemsActivity.xaml.cs'
DET = P + 'frmRptItemsActivityDetailed.xaml.cs'
INV = P + 'frmRptInventory.xaml.cs'
TAX = P + 'frmTaxInvDetails.xaml.cs'
CALLERS = ('frmInvInOutput', 'frmPOS', 'frmPurchInv')
WRAPPERS = ('frmInvSale', 'frmInvPurch', 'frmInvPOS', 'frmInvInputOutput', 'frmInventoryTransfer')
TARGETS = ('CAP7B38-D08', 'CAP7B38-D16', 'CAP7B38-D17')
FOCUSED = ('P7-045', 'P7-058', 'P7-085', 'P7-122', 'P7-129', 'P7-130')
SHARED = ('Navigate', 'CLR', 'ResetInvoice', 'BindingControls')
CONTEXTS = {
    IP: ['GetEntryGlobalID', 'BindingInvoice', 'BindingCostDetaile', 'BindingItemDetails', 'glassOtions'],
    C + 'EntryOper.cs': ['GenerateEntryGlobalIDByEntryNo'],
    C + 'MainClass.cs': ['DoApplyUserSett@System.Windows.Window',
                        'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions'],
    AGG: ['ctor:frmRptItemsActivity', 'Window_Loaded', 'LoadPrintSettings', 'LoadSafes',
          'LoadGroups', 'LoadBranch', 'CalcStock', 'chkAll_CheckedChanged', 'btnSearchItem_Click'],
    DET: ['LastProcess', 'ShowResult', 'btnOpenInvoice_Click', 'OpenInvoiceByType', 'OpenForm', 'OpenWindow'],
    INV: ['BtnShowInv_Click', 'OpenInventoryTransfer', 'OpenBeginningInventory',
          'OpenInputOutput', 'OpenProductionOrder', 'OpenSafeAdjust'],
    TAX: ['BtnDetails_Click', 'OpenDetailsWindow'],
    **{P + stem + '.xaml.cs': ['StripItemProcess_Click'] for stem in CALLERS},
    **{P + stem + '.xaml.cs': list(SHARED) + ['BindingDGV', 'LoadInvNo']
       for stem in ('frmInvSale', 'frmInvPurch', 'frmInvPOS')},
    P + 'frmInvInputOutput.xaml.cs': list(SHARED) + ['RefreshGrid', 'LoadInvNo'],
    P + 'frmInventoryTransfer.xaml.cs': list(SHARED) + ['BindingDGV', 'LoadInvoiceNumber',
                                                     'LoadSafes', 'GC1_Refresh', 'ShowError'],
    # Deliberately narrow alternative receivers; no whole ReadData/hydration claim.
    P + 'frmProductionOrder.xaml.cs': ['Navigate'],
    P + 'frmSafeAdjust.xaml.cs': ['Navigate'],
    P + 'frmSandVAT.xaml.cs': ['Navigate', 'ReadData'],
}
XML_SELECTED = {
    P + 'frmRptItemsActivity.xaml': {'chkAll', 'Window_Loaded'},
    P + 'frmRptItemsActivityDetailed.xaml': {'chkAll'},
    **{P + stem + '.xaml': {'StripItemProcess_Click'} for stem in CALLERS},
}


def load(name: str, ev: Path = EV):
    return base.load_json(name, ev)


def identity(rel: str, root: Path = ROOT):
    raw = (root / rel).read_bytes()
    return {'path': rel, 'bytes': len(raw), 'sha256': base.sha(raw)}


def norm(text: str):
    return re.sub(r'\s+', '', text)


def ancestors(parsed, node, stop):
    """Lexical containing scopes only, not a runtime call/exception trace."""
    out = []
    child = node
    parent = node.parent
    while parent and parent != stop:
        if parent.type == 'if_statement':
            consequence = parent.child_by_field_name('consequence')
            side = 'consequence' if consequence and consequence.start_byte <= child.start_byte and child.end_byte <= consequence.end_byte else 'alternative'
            out.append({'kind': 'if', 'condition': parsed.text(parent.child_by_field_name('condition')),
                        'side': side, 'line': parent.start_point.row + 1})
        elif parent.type == 'catch_clause':
            decl = next((c for c in parent.named_children if c.type == 'catch_declaration'), None)
            out.append({'kind': 'catch', 'declaration': parsed.text(decl), 'line': parent.start_point.row + 1})
        elif parent.type in ('for_statement', 'foreach_statement', 'while_statement'):
            out.append({'kind': parent.type, 'line': parent.start_point.row + 1})
        child, parent = parent, parent.parent
    return out


def selected_node(parsed, selector):
    kind = 'constructor_declaration' if selector.startswith('ctor:') else 'method_declaration'
    s = selector.removeprefix('ctor:')
    name, _, qualifier = s.partition('@')
    nodes = [n for n in base.walk(parsed.tree.root_node) if n.type == kind
             and parsed.text(n.child_by_field_name('name')) == name
             and (not qualifier or qualifier in parsed.text(n.child_by_field_name('parameters')))]
    if len(nodes) != 1:
        raise ValueError(f'{selector}: expected exactly one declaration; got {len(nodes)}')
    return nodes[0]


def source_methods(text, selectors):
    parsed = base.Syntax(text)
    result = {}
    for selector in selectors:
        node = selected_node(parsed, selector)
        nodes = list(base.walk(node))
        code = parsed.text(node)
        result[selector] = {
            'selector': selector, 'start': node.start_point.row + 1, 'end': node.end_point.row + 1,
            'parameters': parsed.text(node.child_by_field_name('parameters')),
            'return_type': parsed.text(node.child_by_field_name('returns')),
            'syntax_utf8_sha256': base.sha(code.encode('utf8')), 'syntax_text': code,
            'calls': [{'function': parsed.text(n.child_by_field_name('function')),
                       'arguments': parsed.text(n.child_by_field_name('arguments')),
                       'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
                       'ancestors': ancestors(parsed, n, node)}
                      for n in nodes if n.type == 'invocation_expression'],
            'assignments': [{'left': parsed.text(n.child_by_field_name('left')),
                             'right': parsed.text(n.child_by_field_name('right')),
                             'operator': parsed.text(n.children[1]) if len(n.children) > 2 else '',
                             'line': n.start_point.row + 1, 'ancestors': ancestors(parsed, n, node)}
                            for n in nodes if n.type == 'assignment_expression'],
            'creations': [{'type': parsed.text(n.child_by_field_name('type')),
                           'arguments': parsed.text(n.child_by_field_name('arguments')),
                           'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
                           'syntax_text': parsed.text(n), 'ancestors': ancestors(parsed, n, node)}
                          for n in nodes if n.type == 'object_creation_expression'],
            'catches': [{'declaration': parsed.text(next((c for c in n.named_children if c.type == 'catch_declaration'), None)),
                         'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
                         'body': parsed.text(n.child_by_field_name('body')),
                         'ancestors': ancestors(parsed, n, node)}
                        for n in nodes if n.type == 'catch_clause'],
            'returns': [{'text': parsed.text(n), 'line': n.start_point.row + 1}
                        for n in nodes if n.type == 'return_statement'],
        }
    return result


def xml_facts(text, needles):
    parser = xml.parsers.expat.ParserCreate(namespace_separator='|')
    result = []
    def start(name, attrs):
        short = {k.rsplit('|', 1)[-1]: value for k, value in attrs.items()}
        if any(value in needles for value in short.values()):
            result.append({'element': name.rsplit('|', 1)[-1], 'line': parser.CurrentLineNumber,
                           'attributes': short})
    parser.StartElementHandler = start
    parser.Parse(text.encode('utf8'), True)
    return result


def derive(root: Path = ROOT):
    facts = {'schema_version': 1, 'kind': 'new-R4-bounded-syntax-facts-not-R3-reconstruction',
             'source_identity': {}, 'methods': {}, 'xml_elements': {},
             'application_execution_count': 0, 'whole_7B_static_assessment_complete': False}
    for rel, selectors in CONTEXTS.items():
        raw = (root / rel).read_bytes()
        facts['source_identity'][rel] = identity(rel, root)
        facts['methods'][rel] = source_methods(base.decode(raw), selectors)
    for rel, needles in XML_SELECTED.items():
        raw = (root / rel).read_bytes()
        facts['source_identity'][rel] = identity(rel, root)
        facts['xml_elements'][rel] = xml_facts(base.decode(raw), needles)
    rel = 'SmartAuditERP/SmartAuditERP.csproj'
    raw = (root / rel).read_bytes()
    facts['source_identity'][rel] = identity(rel, root)
    facts['UtilitiesProj_reference_lines'] = [{'line': i, 'text': text} for i, text in enumerate(base.decode(raw).splitlines(), 1)
                                             if 'UtilitiesProj' in text]
    return facts


def method(facts, rel, selector):
    return facts['methods'][rel][selector]


def assignments(f, left, right=None):
    return [a for a in f['assignments'] if norm(a['left']) == norm(left)
            and (right is None or norm(a['right']) == norm(right))]


def guarded(record, condition, side='consequence'):
    return any(a['kind'] == 'if' and norm(a['condition']) == norm(condition) and a['side'] == side
               for a in record['ancestors'])


def item_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('item:' + label)
    agg = method(facts, AGG, 'Window_Loaded')
    calls = [c for c in agg['calls'] if c['function'] == 'CalcStock']
    need(assignments(method(facts, AGG, 'ctor:frmRptItemsActivity'), 'ItemId', '-1'), 'constructor-request-default')
    need(any(guarded(a, 'ItemId > 0') for a in assignments(agg, 'selectedItemId', 'ItemId')), 'fresh-positive-request-copy')
    need(len(calls) == 1 and guarded(calls[0], 'ItemId > 0'), 'loaded-calculation-guard')
    for name in ('Window_Loaded', 'LoadPrintSettings', 'LoadSafes', 'LoadGroups', 'LoadBranch'):
        need(not assignments(method(facts, AGG, name), 'chkAll.IsChecked'), 'startup-must-not-be-misreported-as-clearing-all:' + name)
    checks = [r for r in facts['xml_elements'][AGG[:-3]] if r['attributes'].get('Name') == 'chkAll']
    need(len(checks) == 1 and checks[0]['attributes'].get('IsChecked') == 'True', 'own-xaml-all-default')
    need(any(r['attributes'].get('Loaded') == 'Window_Loaded' for r in facts['xml_elements'][AGG[:-3]]), 'own-loaded-wiring')
    calc = method(facts, AGG, 'CalcStock')
    predicates = [a for a in calc['assignments'] if a['left'] == 'itemsSql' and 'AND id={selectedItemId}' in a['right']]
    need(len(predicates) == 1 and guarded(predicates[0], '!chkAll.IsChecked == true'), 'item-predicate-depends-on-all-flag')
    # The historical root remains the positive store request vs all-stores flag, not a different old bug.
    detail = method(facts, DET, 'LastProcess')
    need(any(guarded(a, 'storeId > 0') for a in assignments(detail, 'cmbSafes.SelectedValue', 'storeId')), 'prior-root-positive-store')
    need(not assignments(detail, 'chkAll.IsChecked'), 'prior-root-does-not-clear-all-store-flag')
    x = [r for r in facts['xml_elements'][DET[:-3]] if r['attributes'].get('Name') == 'chkAll']
    need(len(x) == 1 and x[0]['attributes'].get('IsChecked') == 'True', 'prior-root-store-default')
    result = method(facts, DET, 'ShowResult')
    need(any('Inv_sub.store=' in a['right'] and any(g['kind'] == 'if' and 'chkAll.IsChecked != true' in g['condition'] for g in a['ancestors']) for a in result['assignments']), 'prior-root-store-predicate')
    need(any('Inv_Sub.ItemId={SelectedId}' in a['right'] and guarded(a, 'SelectedId != -1') for a in result['assignments']), 'counterexample-detail-direct-item-filter')
    for stem in CALLERS:
        f = method(facts, P + stem + '.xaml.cs', 'StripItemProcess_Click')
        creations = [a for a in f['creations'] if a['type'] == 'frmRptItemsActivity']
        writes = [a for a in f['assignments'] if a['left'] == 'ItemId' or a['left'].endswith('.ItemId')]
        need(len(creations) == 1 and len(writes) == 1 and writes[0]['right'] == ('row.ItemId' if stem == 'frmInvInOutput' else 'id'), 'exact-caller-request:' + stem)
        displays = [c for c in f['calls'] if c['function'].endswith('.ShowDialog')]
        need(len(displays) == len(creations) == len(writes) == 1 and creations[0]['line'] <= writes[0]['line'] < displays[0]['line'], 'request-before-display:' + stem)
        need(any(r['attributes'].get('Click') == 'StripItemProcess_Click' for r in facts['xml_elements'][P + stem + '.xaml']), 'own-menu-wiring:' + stem)
    for selector in ('DoApplyUserSett@System.Windows.Window', 'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions'):
        f = method(facts, C + 'MainClass.cs', selector)
        need(not any('IsChecked' in a['left'] or 'ItemId' in a['left'] for a in f['assignments']), 'readable-local-helper-not-an-invented-filter-reset:' + selector)
    return errors


def receiver_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('receiver:' + label)
    f = method(facts, IP, 'BindingInvoice')
    need(f['return_type'] == 'void' and norm(f['parameters']) == '(refInvoiceDGVInvo,stringsqlstr)', 'void-ref-signature')
    commands = [c for c in f['creations'] if c['type'] == 'SqlCommand']
    need(len(commands) == 1 and norm(commands[0]['arguments']) == '(sqlstr,sqlConnection)', 'caller-query-forwarded-without-added-scope')
    reads = [c for c in f['calls'] if c['function'] == 'sqlDataReader.Read']
    need(len(reads) == 1 and guarded(reads[0], 'sqlDataReader.HasRows'), 'one-first-header-read')
    nulls = assignments(f, 'Invo', 'null')
    need(len(nulls) == 2 and any(guarded(a, 'sqlDataReader.HasRows', 'alternative') for a in nulls)
         and any(any(x['kind'] == 'catch' and 'projectError5' in x['declaration'] for x in a['ancestors']) for a in nulls), 'empty-and-outer-failed-collapse-to-null')
    need(assignments(f, 'Invo.ISNew', 'false') and assignments(f, 'Invo.IsPrinted', 'true')
         and assignments(f, 'Invo.IsLoaded', 'false'), 'header-state-not-a-health-enum')
    need(any('sqlDataReader["InvGlobalID"]' in a['right'] for a in assignments(f, 'Invo.InvGlobalID'))
         and any('sqlDataReader["branch"]' in a['right'] for a in assignments(f, 'Invo.Branch')), 'loaded-identity-comes-from-row')
    need(len(f['catches']) == 5 and all('throw' not in c['body'] for c in f['catches']), 'five-distinct-catch-scopes-not-universal-success')
    add = [c for c in f['calls'] if c['function'] == 'Invo.InvoiceItems.Add']
    need(len(add) == 1 and norm(add[0]['arguments']) == '(Itm)', 'item-publication')
    if add:
        need(all(any(a['kind'] == 'for_statement' for a in c['ancestors']) for c in add), 'publication-in-row-loop')
        totals = [a for a in f['assignments'] if a['left'] in ('Invo.TotDiscount', 'Invo.SumPrice', 'Invo.SumCost')]
        need(len(totals) == 4 and max(a['line'] for a in totals) < add[0]['line'], 'totals-mutate-before-row-add')
        helper_calls = [c for c in f['calls'] if c['function'] in ('InvoiceOper.BindingItemDetails', 'InvoiceOper.glassOtions')]
        need(len(helper_calls) == 2 and all(c['line'] < add[0]['line'] for c in helper_calls), 'row-delegates-before-add')
    detail_sql = [c for c in f['creations'] if c['type'] == 'SqlDataAdapter' and 'ProductId = 0' in c['arguments']]
    need(len(detail_sql) == 1 and 'Inv.InvGlobalID' in detail_sql[0]['arguments'] and 'Invo.InvGlobalID' in detail_sql[0]['arguments'], 'detail-key-plus-product-filter')
    cc = [c for c in f['creations'] if c['type'] == 'SqlDataAdapter' and 'select CCcode from Entry_sub' in c['arguments']]
    need(len(cc) == 1 and 'MainClass.BranchNo' in cc[0]['arguments'] and 'Invo.EntryGlobalID' in cc[0]['arguments'] and 'Invo.InvAccCode' in cc[0]['arguments'], 'cost-center-is-current-branch-not-loaded-row-branch')
    need(not method(facts, IP, 'BindingItemDetails')['catches'], 'item-detail-error-escapes-to-row-catch')
    for name in ('glassOtions', 'BindingCostDetaile'):
        h = method(facts, IP, name)
        need(len(h['catches']) == 1 and not h['returns'] and 'throw' not in h['catches'][0]['body'], 'helper-catch-return-no-health:' + name)
    need(any('EntryID' in c['arguments'] and '["branch"]' in c['arguments'] for c in f['calls'] if c['function'] == 'InvoiceOper.GetEntryGlobalID'), 'entry-lookup-uses-loaded-branch')
    need('Sync.ActiveSync' in method(facts, C + 'EntryOper.cs', 'GenerateEntryGlobalIDByEntryNo')['syntax_text'], 'fallback-key-is-conditional-local-generation-not-lookup-success')
    for stem in WRAPPERS:
        w = method(facts, P + stem + '.xaml.cs', 'Navigate')
        binds = [c for c in w['calls'] if c['function'] == 'InvoiceOper.BindingInvoice']
        need(w['return_type'] == 'void' and len(binds) == 1 and 'sqlStr' in binds[0]['arguments'], 'wrapper-forwards-void-ref:' + stem)
        need(not any(c['function'].endswith('CheckBeforeClear') for c in w['calls']), 'no-internal-dirty-guard:' + stem)
        need(len(binds) == 1 and any(c['function'] in ('CLR', 'this.CLR') and c['line'] < binds[0]['line'] for c in w['calls']), 'local-reset-before-receiver:' + stem)
    return errors


def request_rows(facts):
    rows = []
    for rel in (INV, DET, TAX):
        for selector, f in facts['methods'][rel].items():
            for call in f['calls']:
                if not call['function'].endswith('.Navigate'): continue
                arg = call['arguments']
                key = 'InvGlobalID' if 'InvGlobalID' in arg else 'ReceiptNo' if 'ReceiptNo' in arg else 'local-id'
                rows.append({'path': rel, 'selector': selector, 'line': call['line'], 'function': call['function'],
                             'argument_expression': arg, 'argument_expression_sha256': base.sha(arg.encode('utf8')),
                             'key_syntax': key, 'lexical_ancestors': call['ancestors'],
                             'source_method_sha256': f['syntax_utf8_sha256']})
    return rows


def route_errors(facts):
    rows = request_rows(facts)
    errors = []
    inv = [r for r in rows if r['path'] == INV]
    det = [r for r in rows if r['path'] == DET]
    tax = [r for r in rows if r['path'] == TAX]
    if len(inv) != 5 or any(r['key_syntax'] != 'InvGlobalID' for r in inv): errors.append('routes:inventory-five-global-key-call-sites')
    if len(det) != 14 or any(r['key_syntax'] != 'local-id' for r in det): errors.append('routes:detail-fourteen-local-number-call-sites')
    if len(tax) != 7 or sum(r['key_syntax'] == 'InvGlobalID' for r in tax) != 6 or sum(r['key_syntax'] == 'ReceiptNo' for r in tax) != 1: errors.append('routes:tax-six-global-one-receipt-number')
    if any(re.search(r'\bbranch\s*=', r['argument_expression'], re.I) for r in rows): errors.append('routes:explicit-branch-absence-must-not-be-misreported')
    for name in ('OpenForm', 'OpenWindow'):
        f = method(facts, DET, name)
        configure = [c for c in f['calls'] if c['function'] == 'configure']
        show = [c for c in f['calls'] if c['function'].endswith('.Show')]
        if len(configure) != 1 or len(show) != 1 or configure[0]['line'] >= show[0]['line']: errors.append('routes:configure-before-show:' + name)
    return errors


def read_errors(reads, facts, root: Path = ROOT):
    errors = []
    ranges = {}
    for row in reads.get('reads', []):
        rel = row['path']
        lines = base.decode((root / rel).read_bytes()).splitlines(keepends=True)
        start, end = row['start'], row['end']
        if not 1 <= start <= end <= len(lines):
            errors.append('read:invalid-range:' + rel); continue
        text = ''.join(lines[start - 1:end])
        if base.sha(text.encode('utf8')) != row['decoded_range_utf8_sha256']: errors.append('read:changed-range:' + rel)
        ranges.setdefault(rel, set()).update(range(start, end + 1))
    for rel, methods in facts['methods'].items():
        for name, f in methods.items():
            if not set(range(f['start'], f['end'] + 1)) <= ranges.get(rel, set()): errors.append('read:uncovered-context:' + rel + ':' + name)
    for rel, items in facts['xml_elements'].items():
        for r in items:
            if r['line'] not in ranges.get(rel, set()): errors.append('read:uncovered-xml-element:' + rel)
    if reads.get('extraction_equals_reading') is not False: errors.append('read:extraction-is-not-reading')
    return errors


def lexical_target(facts, row):
    """Selected local syntax naming, not compiler type/alias/virtual resolution."""
    f = method(facts, row['path'], row['selector'])
    if row['path'] == DET:
        candidates = [(c['line'], re.fullmatch(r'Open(?:Form|Window)<(\w+)>', c['function']))
                      for c in f['calls'] if c['line'] <= row['line']]
        candidates = [(line, match[1]) for line, match in candidates if match]
    else:
        candidates = [(c['line'], c['type']) for c in f['creations']
                      if c['type'].startswith('frm') and c['line'] <= row['line']]
    return max(candidates, default=(0, None), key=lambda c: c[0])[1]


def evidence_errors(ev: Path = EV):
    facts, review, item, screen, routes = (load(n, ev) for n in (FACTS, REVIEW, ITEM, SCREEN, ROUTES))
    errors = []
    actual = base.rows('findings.csv', ev=base.AUDIT) + base.rows('findings-additions-07B39R1.csv', ev)
    if len(actual) != 339 or screen.get('available_prior_rows') != actual: errors.append('adjudication:exact-339-available-root-screen')
    focused = {r['id']: r for r in actual if r['id'] in FOCUSED}
    if set(item.get('focused_root_reviews', {})) != set(FOCUSED): errors.append('adjudication:six-focused-root-identities')
    for key, row in item.get('focused_root_reviews', {}).items():
        if row.get('canonical_prior_row') != focused.get(key) or not row.get('reason'): errors.append('adjudication:focused-prior-root:' + key)
    if item.get('decision') != 'same-root-extension' or item.get('root_id') != 'P7-122' or item.get('new_finding_ids') != []: errors.append('adjudication:item-extension-not-new-root')
    if item.get('all345_prior_findings_deduplicated') is not False or screen.get('missing_R2_rows_reconstructed') is not False: errors.append('adjudication:missing-six-rows-must-not-be-invented')
    actual_requests = request_rows(facts)
    if routes.get('requests') != actual_requests: errors.append('adjudication:exact-route-witness-identities-not-count-only')
    bindings = routes.get('individual_dispositions', [])
    if len(bindings) != len(actual_requests): errors.append('adjudication:individual-request-disposition-count')
    for index, (annotation, request) in enumerate(zip(bindings, actual_requests), 1):
        if (annotation.get('id') != f'R4REQ-{index:02d}'
                or annotation.get('source_request_line') != request['line']
                or annotation.get('source_request_path') != request['path']
                or annotation.get('argument_expression_sha256') != request['argument_expression_sha256']
                or annotation.get('syntactically_named_target') != lexical_target(facts, request)
                or annotation.get('target_is_type_bound_by_compiler') is not False):
            errors.append('adjudication:request-identity-target-not-count-only:' + str(index))
    canonical = {r['id']: r for r in base.rows('capability-register-07B38.csv', ev)}
    if set(review.get('capabilities', {})) != set(TARGETS): errors.append('adjudication:three-canonical-capability-identities')
    for cid, row in review.get('capabilities', {}).items():
        if row.get('canonical_capability_row') != canonical.get(cid): errors.append('adjudication:canonical-capability:' + cid)
        if row.get('local_semantic_obligations_complete') is not False or row.get('whole_capability_certified') is not False: errors.append('adjudication:unsupported-capability-exit:' + cid)
        if row.get('readable_local_work_externalized') is not False: errors.append('adjudication:readable-local-cannot-be-externalized:' + cid)
        if not row.get('remaining_readable_local') or not row.get('next_action'): errors.append('adjudication:named-local-remainder:' + cid)
    expected = {'EMPTY', 'OUTER_FAILED', 'HEADER_WITH_NO_DETAIL', 'ROW_PARTIAL', 'OPTIONAL_FIELD_CATCH', 'HELPER_CATCH', 'NORMAL_LOCAL_RETURN', 'PRE_READER_NONRETURN'}
    if len(review.get('receiver_outcomes', [])) != 8 or {r.get('id') for r in review.get('receiver_outcomes', [])} != expected: errors.append('adjudication:eight-distinct-source-health-outcomes')
    for row in review.get('receiver_outcomes', []):
        if row.get('observed_in_ERP') is not False or not row.get('source_basis') or not row.get('limit'): errors.append('adjudication:source-outcome-not-runtime:' + row.get('id', '?'))
    for stem in WRAPPERS:
        row = review.get('wrapper_dispositions', {}).get(stem, {})
        f = method(facts, P + stem + '.xaml.cs', 'Navigate')
        if row.get('source_method_sha256') != f['syntax_utf8_sha256'] or not row.get('null_path') or row.get('typed_health_return') is not False: errors.append('adjudication:wrapper-identity-or-outcome:' + stem)
    if review.get('R2_R3_files_recovered') is not False or review.get('prior196_tests_recertified') is not False: errors.append('adjudication:unavailable-evidence-not-recertified')
    if review.get('R3_shared_receiver_metadata_only_blocker_replaced_by') != 'new-R4-bounded-whole-body-and-five-wrapper-source-review': errors.append('adjudication:whole-body-review-not-replaced-by-old-metadata')
    if item.get('historical_root_fields_rewritten') is not False or item.get('local_candidate_resolution_complete') is not True: errors.append('adjudication:extension-resolves-local-question-not-root-remediation')
    for key, row in item.get('focused_root_reviews', {}).items():
        if row.get('relation_to_candidate') != ('same-root' if key == 'P7-122' else 'distinct-root'): errors.append('adjudication:root-relation:' + key)
    boundaries = base.rows(BOUNDARIES, ev)
    expected_ids = {'EXT-R4-MODEL', 'EXT-R4-DEPLOYED-IDENTITY', 'EXT-R4-LOAD-POLICY'}
    if len(boundaries) != 3 or {r.get('id') for r in boundaries} != expected_ids: errors.append('adjudication:three-individual-new-boundary-identities')
    for row in boundaries:
        required = ('owner_role', 'required_redacted_input', 'source_evidence', 'absence_impact', 'next_action', 'remaining_readable_local', 'static_disposition')
        if any(not row.get(k) for k in required) or row.get('provided') != 'false' or row.get('certified') != 'false': errors.append('adjudication:external-boundary-not-approval:' + row.get('id', '?'))
    for name in (REVIEW, ITEM, SCREEN, ROUTES):
        obj = load(name, ev)
        if obj.get('application_execution_count') != 0 or obj.get('whole_7B_static_assessment_complete') is not False: errors.append('adjudication:no-application-execution-or-7B-exit:' + name)
        if obj.get('assessment_reference_date_utc') != '2026-11-16' or obj.get('raw_clocks_are_calendar_authority') is not False: errors.append('adjudication:prospective-session-date-not-machine-clock:' + name)
        if not obj.get('pinned_inputs'): errors.append('adjudication:missing-input-identities:' + name)
        for row in obj.get('pinned_inputs', []):
            if identity(row['path']) != row: errors.append('adjudication:changed-pinned-input:' + row['path'])
    return errors


def verify(rederive=False, ev: Path = EV):
    facts = load(FACTS, ev)
    errors = []
    for rel, row in facts['source_identity'].items():
        if identity(rel) != row: errors.append('source-identity:' + rel)
    if rederive and facts != derive(): errors.append('fresh-source-rederivation-differs')
    errors += item_errors(facts) + receiver_errors(facts) + route_errors(facts)
    errors += read_errors(load(READS, ev), facts) + evidence_errors(ev)
    return {'schema_version': 1, 'errors': errors, 'contexts': sum(len(v) for v in facts['methods'].values()),
            'source_identities': len(facts['source_identity']), 'request_call_sites': len(request_rows(facts)),
            'capability_exit_certificates_issued': 0, 'application_execution_count': 0,
            'whole_7B_static_assessment_complete': False, 'phase7C_started': False, 'phase8_authorized': False,
            'limit': 'Integrity and bounded source-claim checks only. Not semantic completeness, runtime, SDK/SQL/ACL/financial acceptance, or all repository tests.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='Read-only validation (also default).')
    parser.add_argument('--rederive', action='store_true')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = verify(args.rederive)
    except (ValueError, KeyError, OSError, TypeError) as exc:
        print(json.dumps({'errors': [f'{type(exc).__name__}: {exc}'], 'whole_7B_static_assessment_complete': False}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 2 if args.require_complete else 0


if __name__ == '__main__':
    sys.exit(main())
