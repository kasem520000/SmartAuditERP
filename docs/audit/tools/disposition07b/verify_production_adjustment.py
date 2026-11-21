#!/usr/bin/env python3
"""R5 bounded, read-only source/evidence checks; never an ERP or SQL test.

Fresh C# syntax is inspected with the pinned R1/B38 Tree-sitter packages. Names
are lexical, not compiler-bound targets. XML resources are read as text, not run
as SQL. Passing checks cannot authenticate a review, calendar, deployed schema,
provider behavior, financial result, or capability/family completion.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path
import re
import sys
import xml.parsers.expat

import verify_document_receiver as previous

base = previous.base
ROOT, EV, AUDIT = base.ROOT, base.EV, base.AUDIT
TAG = '07B39R5'
BASE_HEAD = '5dfce80f3f64b689b946a2e936817d8738bea5c8'
DATE = '2026-11-16'  # Session reference, not a reading of the machine clock.
P, C, CW = previous.P, previous.C, 'SmartAuditERP/Class_WPF/'
PROD, SAFE = P + 'frmProductionOrder.xaml.cs', P + 'frmSafeAdjust.xaml.cs'
INV, DET, LOGIN = previous.INV, previous.DET, P + 'frmUserLogin.xaml.cs'
IP, MC, STOCK, ITEM = previous.IP, C + 'MainClass.cs', C + 'Inventory.cs', C + 'ItemOper.cs'
RESOURCE = 'SmartAuditERP/Properties/Resources.resx'
# run01 inputs stay at their original paths and in their consumed-byte archive.
# Only prospective rev02 documents use the corrected column extractor.
FACTS = 'production-adjustment-source-facts-rev02-' + TAG + '.json'
READS = 'production-adjustment-source-review-log-' + TAG + '.json'
REVIEW = 'production-adjustment-dispositions-rev02-' + TAG + '.json'
ROUTES = 'production-adjustment-request-contracts-rev02-' + TAG + '.json'
ROOTS = 'production-adjustment-root-adjudication-rev02-' + TAG + '.json'
ENTRY = 'entry-identities-' + TAG + '.json'
DATES = 'date-authority-clarification-' + TAG + '.json'
MUTABLE_INDEXES = frozenset('docs/audit/' + n for n in base.MUTABLE_INDEXES)
TARGETS = ('CAP7B38-D08', 'CAP7B38-D17')
FOCUSED = ('P4-017', 'P4-018', 'P4-020', 'P4-021', 'P4-022', 'P7-022',
           'P7-057', 'P7-060', 'P7-061', 'P7-072', 'P7-131', 'P7-132',
           'P7-133', 'P7-134', 'P7-161')

CONTEXTS = {
    PROD: ['ctor:frmProductionOrder', 'Window_Loaded', 'Navigate', 'ReadData', 'CLR',
           'LoadInvNo', 'LoadComponent', 'LoadItemUnits', 'CalcTot', 'CalcStock',
           'GetCurrencyName', 'GetItemCode', 'GetUnitName', 'GetStoreName',
           'cmbItems_SelectionChanged', 'cmbUnits_SelectionChanged', 'txtQty_TextChanged',
           'dgvItems_CellEditEnding', 'EnsureOpen', 'CloseConn', 'Save',
           'dgvSrch_MouseLeftButtonUp', 'btnFirst_Click', 'btnPrevious_Click',
           'btnNext_Click', 'btnLast_Click'],
    SAFE: ['ctor:frmSafeAdjust', 'Window_Loaded', 'Navigate', 'ReadData', 'CLR',
           'LoadAdjustNo', 'LoadSafes', 'LoadGroups', 'LoadBranches', 'CalSums',
           'UpdateRowCount', 'GetUnitName', 'GetUnitId', 'GetCurrencyName', 'GetItemCode',
           'OnRowPropertyChanged', 'dgvItems_CellEditEnding', 'dgvSrch_MouseDoubleClick',
           'cmbSafes_SelectionChanged', 'cmbGroup_SelectionChanged', 'AdjustStock',
           'ExecuteAdjustment', 'SaveAndPrint', 'BindToInvoice', 'GetInvoiceIDs'],
    INV: ['ShowInvoice', 'BtnShowInv_Click', 'OpenProductionOrder', 'OpenSafeAdjust'],
    DET: ['ShowResult', 'btnOpenInvoice_Click', 'OpenInvoiceByType', 'OpenForm', 'OpenWindow'],
    IP: ['InvoiceNo', 'GetInvoiceGlobalID', 'BindingListOfInvoices1'],
    MC: ['ConnObj'], STOCK: ['CalcItemStock'],
    ITEM: ['Cost', 'AvgCost', 'RecentPurchPrice', 'PurchPrice', 'ToDouble'],
    LOGIN: ['BuildConnectionStrings', 'LoadBranches', 'cmbDatabases_SelectionChangeCommitted'],
}
CLASSES = {PROD: ['ProductionItemRow', 'SearchResultRow'],
           CW + 'AdjustItemRow.cs': ['AdjustItemRow', 'AdjustSearchRow'],
           CW + 'ItemActivityRow_ActivityDetailed.cs': ['ItemActivityRow_ActivityDetailed']}
XML_SELECTED = {
    PROD[:-3]: {'Window_Loaded', 'cmbItems', 'cmbUnits', 'txtQty', 'dgvItems',
                 '{Binding BaseQty}', '{Binding Qty, UpdateSourceTrigger=PropertyChanged}',
                 '{Binding Price, UpdateSourceTrigger=PropertyChanged}',
                 '{Binding UnitEquality}', '{Binding UnitId}'},
    SAFE[:-3]: {'Window_Loaded', 'cmbSafes', 'dgvItems', 'dgvSrch', '{Binding Unit}',
                 '{Binding CurrentStock, StringFormat=N2}',
                 '{Binding RealStock, UpdateSourceTrigger=LostFocus}',
                 '{Binding Price, UpdateSourceTrigger=LostFocus}'},
}
# These are explicit, actually reviewed resource intervals, NOT a general SQL parser
# or a claim to have read all 144533 resource lines / every migration in the repo.
RESOURCE_RANGES = {
    'Inv-create': (954, 1017), 'Inv_Sub-create': (1023, 1060),
    'SafesAdjust-create': (1692, 1705), 'SafesAdjust_Sub-create': (1713, 1726),
    'Inv-global-backfill': (47748, 47771),
    'SafesAdjust-stock-and-item-patch': (47828, 47841),
    'Inv-legacy-header-rename': (47988, 47993),
    'CalcItemStock-create': (3545, 3557),
    'CalcItemStock-create-or-alter': (47995, 48025),
    'ItemAvrgCost-create': (3738, 3754),
    'ItemAvrgCost-create-or-alter': (48221, 48255),
    'CalcProductStocks-create': (4214, 4226),
    'CalcProductStocks-if-absent': (49309, 49322),
}
# Additional bounded fields/SQL string declarations support identity/default claims.
TEXT_RANGES = {
    'production-fields': (PROD, 23, 87),
    'adjustment-fields': (SAFE, 28, 86),
    'connection-fields': (MC, 25, 41),
    'shared-invoice-SQL-strings': (C + 'StoredQueries.cs', 4, 10),
}

load = previous.load
identity = previous.identity
norm = previous.norm
method = previous.method
assignments = previous.assignments
guarded = previous.guarded


def source_methods(text, selectors):
    result = previous.source_methods(text, selectors)
    parsed = base.Syntax(text)
    for selector in selectors:
        node = previous.selected_node(parsed, selector)
        nodes = list(base.walk(node))
        result[selector]['conditions'] = [
            {'text': parsed.text(n.child_by_field_name('condition')),
             'line': n.start_point.row + 1,
             'consequence': parsed.text(n.child_by_field_name('consequence')),
             'alternative': parsed.text(n.child_by_field_name('alternative'))}
            for n in nodes if n.type == 'if_statement']
        result[selector]['index_accesses'] = [
            {'text': parsed.text(n), 'line': n.start_point.row + 1,
             'ancestors': previous.ancestors(parsed, n, node)}
            for n in nodes if n.type == 'element_access_expression']
        result[selector]['locals'] = [
            {'text': parsed.text(n), 'line': n.start_point.row + 1}
            for n in nodes if n.type == 'variable_declarator']
        for kind in ('finally_clause', 'using_statement'):
            result[selector][kind + 's'] = [
                {'text': parsed.text(n), 'line': n.start_point.row + 1,
                 'end': n.end_point.row + 1} for n in nodes if n.type == kind]
    return result


def class_facts(text, names):
    parsed = base.Syntax(text)
    result = {}
    for name in names:
        found = [n for n in base.walk(parsed.tree.root_node)
                 if n.type == 'class_declaration'
                 and parsed.text(n.child_by_field_name('name')) == name]
        if len(found) != 1:
            raise ValueError('Expected one local class: ' + name)
        n = found[0]; code = parsed.text(n)
        result[name] = {'start': n.start_point.row + 1, 'end': n.end_point.row + 1,
                        'syntax_text': code, 'syntax_utf8_sha256': base.sha(code.encode('utf8'))}
    return result


def text_range(text, start, end):
    lines = text.splitlines(keepends=True)
    if not 1 <= start <= end <= len(lines):
        raise ValueError('Invalid explicitly selected source interval')
    return ''.join(lines[start - 1:end])


def resource_facts(text):
    # Expat supplies ownership/line coordinates; the fragments remain raw XML SQL.
    owners = []
    parser = xml.parsers.expat.ParserCreate()
    def start(name, attrs):
        if name == 'data':
            owners.append((parser.CurrentLineNumber, attrs['name']))
    parser.StartElementHandler = start
    parser.Parse(text.encode('utf8'), True)
    fragments, tables = {}, {}
    for key, (a, b) in RESOURCE_RANGES.items():
        raw = text_range(text, a, b)
        owner = max((o for o in owners if o[0] <= a), default=(0, None))
        fragments[key] = {'path': RESOURCE, 'start': a, 'end': b,
                          'resource_name': owner[1], 'raw_xml_text': raw,
                          'decoded_range_utf8_sha256': base.sha(raw.encode('utf8'))}
        if key.endswith('-create') and key[:-7] in ('Inv', 'Inv_Sub', 'SafesAdjust', 'SafesAdjust_Sub'):
            sql = html.unescape(raw)
            # A plain identifier MUST have horizontal whitespace before its type.
            # Otherwise case-insensitive backtracking splits CONSTRAINT into
            # CONSTRA + INT. Bracketed identifiers may abut a bracketed type.
            declarations = re.finditer(
                r'^[ \t]*(?:\[(?P<quoted>\w+)\][ \t]*|(?P<plain>\w+)[ \t]+)'
                r'(?:\[(?:varchar|nvarchar|datetime|int|float|bit|decimal)\]|'
                r'(?:varchar|nvarchar|datetime|int|float|bit|decimal)(?=\W|$))',
                sql, re.I | re.M)
            columns = [m['quoted'] or m['plain'] for m in declarations]
            pk = re.search(r'PRIMARY KEY CLUSTERED\s*\((.*?)\)', sql, re.I | re.S)
            tables[key[:-7]] = {'fragment': key, 'columns': columns,
                               'primary_key_columns': re.findall(r'\[(\w+)\]\s+ASC', pk[1], re.I) if pk else [],
                               'is_deployed_schema_attestation': False}
    return {'fragments': fragments, 'tables': tables,
            'limit': 'Selected supplied definitions and patches only; not execution, migration ordering, provider binding, or deployed DDL/FK/version attestation.'}


def derive(root: Path = ROOT):
    result = {'schema_version': 1, 'kind': 'new-R5-bounded-original-source-syntax-and-resource-text',
              'source_identity': {}, 'methods': {}, 'classes': {}, 'xml_elements': {},
              'text_ranges': {}, 'application_execution_count': 0,
              'whole_7B_static_assessment_complete': False}
    all_paths = set(CONTEXTS) | set(CLASSES) | set(XML_SELECTED) | {RESOURCE}
    all_paths |= {row[0] for row in TEXT_RANGES.values()}
    for rel in sorted(all_paths):
        raw = (root / rel).read_bytes(); text = base.decode(raw)
        result['source_identity'][rel] = identity(rel, root)
        if rel in CONTEXTS: result['methods'][rel] = source_methods(text, CONTEXTS[rel])
        if rel in CLASSES: result['classes'][rel] = class_facts(text, CLASSES[rel])
        if rel in XML_SELECTED: result['xml_elements'][rel] = previous.xml_facts(text, XML_SELECTED[rel])
        if rel == RESOURCE: result['resources'] = resource_facts(text)
        for name, (path, a, b) in TEXT_RANGES.items():
            if rel == path:
                code = text_range(text, a, b)
                result['text_ranges'][name] = {'path': rel, 'start': a, 'end': b,
                    'syntax_text': code, 'decoded_range_utf8_sha256': base.sha(code.encode('utf8'))}
    result['requests'] = request_rows(result)
    return result


def calls(f, name):
    return [c for c in f['calls'] if c['function'] == name]


def source_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('source:' + label)
    p, s = method(facts, PROD, 'ReadData'), method(facts, SAFE, 'ReadData')
    pn, sn = method(facts, PROD, 'Navigate'), method(facts, SAFE, 'Navigate')
    pc, sc = method(facts, PROD, 'CLR'), method(facts, SAFE, 'CLR')
    for rel, f in ((PROD, p), (SAFE, s)):
        need(f['return_type'] == 'void' and norm(f['parameters']) == '(SqlDataReaderdr)', 'void-reader:' + rel)
        need(len(calls(f, 'dr.Read')) == len(calls(f, 'dr.Close')) == 1, 'first-header-single-explicit-close:' + rel)
        need(not f['finally_clauses'], 'reader-flag-reset-is-not-finally:' + rel)
    empty_p = [c for c in p['conditions'] if norm(c['text']) == '!dr.HasRows']
    empty_s = [c for c in s['conditions'] if norm(c['text']) == '!dr.HasRows']
    need(len(empty_p) == 1 and norm(empty_p[0]['consequence']) == '{CLR();return;}', 'production-no-header-clears')
    need(len(empty_s) == 1 and norm(empty_s[0]['consequence']) == 'return;', 'adjustment-no-header-does-not-clear')
    pclear, sclear = calls(p, 'CLR'), calls(s, 'CLR')
    need(len(pclear) == 2 and len(sclear) == 1, 'distinct-reset-call-sites')
    need(len(pclear) == 2 and calls(p, 'dr.Read') and assignments(p, '_isLoaded', 'true')
         and calls(p, 'dr.Read')[0]['line'] < pclear[-1]['line'] < assignments(p, '_isLoaded', 'true')[0]['line'], 'production-read-clear-then-load-flag')
    need(len(sclear) == 1 and calls(s, 'dr.Read') and assignments(s, 'Isload', 'true')
         and calls(s, 'dr.Read')[0]['line'] < sclear[0]['line'] < assignments(s, 'Isload', 'true')[0]['line'], 'adjustment-read-clear-then-load-flag')
    need(len(s['catches']) == 1 and not s['finally_clauses']
         and not any(a['left'] == 'Isload' for a in s['assignments'] if any(x['kind'] == 'catch' for x in a['ancestors'])), 'adjustment-catch-does-not-restore-load-flag')
    need(assignments(p, '_isLoaded', 'false') and assignments(s, 'Isload', 'false'), 'flags-clear-on-normal-tail')
    need(len(p['catches']) > 10 and all('throw' not in c['body'] for c in p['catches']), 'production-many-swallowing-scopes')
    need(len(pn['using_statements']) == 2 and len(pn['finally_clauses']) == 1
         and 'CloseConn(_conn)' in pn['finally_clauses'][0]['text'], 'production-command-reader-using-and-finally')
    need(not sn['using_statements'] and not sn['finally_clauses'] and not sn['catches'], 'adjustment-navigate-normal-tail-close-only')
    for f, arg in ((pn, '(sqlQuery, _conn)'), (sn, '(sqlStr, conn)')):
        commands = [c for c in f['creations'] if c['type'] == 'SqlCommand']
        need(len(commands) == 1 and norm(commands[0]['arguments']) == norm(arg), 'forward-caller-sql-without-invented-scope:' + arg)
    adapters = [c for c in p['creations'] if c['type'] == 'SqlDataAdapter']
    need(len(adapters) == 2 and all("InvGlobalID=N'{_invGlobalID}'" in c['arguments'] for c in adapters)
         and any('productId=0' in c['arguments'] for c in adapters)
         and any('productId>0' in c['arguments'] for c in adapters), 'production-two-detail-partitions-by-loaded-global-key')
    row = [c for c in p['creations'] if c['type'] == 'ProductionItemRow']
    need(len(row) == 1 and not assignments(p, 'BaseQty') and not assignments(p, 'UnitEquality'), 'loaded-production-row-omits-base-and-equality')
    need(any('Math.Round(Convert.ToDouble(row["val1"]), 2)' in x['text'] for x in p['locals'])
         and any('Math.Round(Convert.ToDouble(row["exchange_price"]), 2)' in x['text'] for x in p['locals']), 'production-read-rounds-quantity-and-price-before-publication')
    need(calls(p, 'CalcTot') and assignments(p, '_isLoaded', 'false')
         and calls(p, 'CalcTot')[0]['line'] < assignments(p, '_isLoaded', 'false')[0]['line'], 'production-totals-before-normal-flag-tail')
    model = facts['classes'][PROD]['ProductionItemRow']['syntax_text']
    need('private double _baseQty;' in model and 'private double _unitEquality = 1;' in model, 'local-production-model-fields-not-external-DTO-defaults')
    units, qty = method(facts, PROD, 'cmbUnits_SelectionChanged'), method(facts, PROD, 'txtQty_TextChanged')
    need(assignments(units, 'row.Qty', 'Math.Round(perc * row.BaseQty * qty, 2)')
         and assignments(qty, 'row.Qty', 'Math.Round(qty * row.BaseQty * row.UnitEquality, 2)'), 'distinct-existing-unit-versus-quantity-events')
    need(any(guarded(a, '!string.IsNullOrEmpty(row.ItemName) && row.BaseQty > 0') for a in assignments(qty, 'row.Qty')), 'quantity-event-requires-positive-base')
    need(not any('_isLoaded' in c['text'] for c in qty['conditions']), 'quantity-text-event-is-not-load-guarded')
    need(assignments(pc, '_invGlobalID', '"-1"') and assignments(pc, '_procCode', '-1')
         and calls(pc, '_itemsSource.Clear') and calls(pc, 'LoadInvNo') and pc['catches'], 'production-reset-order-and-catch-present')
    need(not assignments(sc, 'cmbSafes.SelectedValue') and not assignments(sc, 'cmbInvBranch.SelectedValue')
         and calls(sc, 'LoadAdjustNo') and calls(sc, 'ItemsList.Clear'), 'adjustment-reset-not-invented-safe-or-branch-reset')
    need(any('dr["Is_Approved"]' in a['right'] for a in assignments(s, 'cmbSatus.SelectedIndex')), 'adjustment-header-requires-approval-column')
    safe_set = assignments(s, 'cmbSafes.SelectedValue')
    need(len(safe_set) == 1 and guarded(safe_set[0], 'cmbSafes.SelectedValue != null'), 'adjustment-safe-assignment-conditional-on-existing-selection')
    sa = [c for c in s['creations'] if c['type'] == 'SqlDataAdapter']
    need(len(sa) == 1 and 'SafesAdjust_Sub WHERE Adjust_id={Code}' in sa[0]['arguments'], 'adjustment-detail-key-is-loaded-header-id')
    need(assignments(s, 'Unit', 'GetUnitName(itemId)') and not any('row["unit"]' in x['text'] for x in s['index_accesses']), 'adjustment-loads-current-item-unit-not-saved-line-unit')
    helper = method(facts, SAFE, 'GetUnitName')
    need('items.unit=units.Id' in helper['syntax_text'] and 'WHERE items.id={itemId}' in helper['syntax_text'], 'adjustment-unit-helper-follows-item-master')
    draft = method(facts, SAFE, 'AdjustStock')
    need(any(a['right'] == 'GetUnitId(item.Unit)' and '@unit' in a['left'] for a in draft['assignments']), 'adjustment-draft-writer-persists-row-unit')
    local = facts['classes'][CW + 'AdjustItemRow.cs']['AdjustItemRow']['syntax_text']
    need('public string Unit' in local and 'RecalcQty();' in local and 'RecalcTotal();' in local, 'local-adjustment-model-read-not-unknown-DTO')
    current, real, price = [assignments(s, name) for name in ('CurrentStock', 'RealStock', 'Price')]
    need(current and real and price and current[0]['line'] < real[0]['line'] < price[0]['line'], 'adjustment-row-initialization-order')
    override = [assignments(s, name) for name in ('adjRow.InQty', 'adjRow.OutQty', 'adjRow.Total')]
    hook = assignments(s, 'adjRow.PropertyChanged')
    need(all(override) and len(hook) == 2 and hook[0]['operator'] == '-=' and hook[1]['operator'] == '+='
         and hook[0]['line'] < min(a[0]['line'] for a in override)
         and max(a[0]['line'] for a in override) < hook[1]['line'], 'adjustment-saved-quantities-override-model-recalc-before-subscription')
    no = method(facts, SAFE, 'LoadAdjustNo')
    need(assignments(no, 'nextNo', 'dt.Rows.Count + 1') and 'SELECT id FROM SafesAdjust' in no['syntax_text'], 'adjustment-number-is-cardinality-not-reservation')
    need('conn1)' in no['syntax_text'] and 'InvoiceOper.InvoiceNo' in method(facts, PROD, 'LoadInvNo')['syntax_text'], 'number-helper-connections-not-active-header-connection')
    factory = method(facts, MC, 'ConnObj')
    need(assignments(factory, 'conn', 'new SqlConnection(connstr)') and len(calls(method(facts, IP, 'InvoiceNo'), 'MainClass.ConnObj')) == 1, 'fresh-local-connection-factory-and-invoice-number-helper')
    build = method(facts, LOGIN, 'BuildConnectionStrings')
    branches = method(facts, LOGIN, 'LoadBranches')
    need(build['syntax_text'].count('MultipleActiveResultSets=true') == 3, 'login-builder-has-three-MARS-arms')
    overwrites = assignments(branches, 'MainClass.connstr')
    need(len(overwrites) == 3 and sum('pwd=' in a['right'] and 'MultipleActiveResultSets' not in a['right'] for a in overwrites) == 2
         and any(a['right'] == 'conn.ConnectionString' for a in overwrites), 'later-login-overwrites-prevent-universal-MARS-claim')
    event = method(facts, SAFE, 'cmbSafes_SelectionChanged')
    need(calls(event, 'LoadGroups') and not any('Isload' in c['text'] for c in event['conditions']), 'safe-selection-handler-not-load-guarded')
    need('conn)' in method(facts, SAFE, 'LoadGroups')['syntax_text']
         and safe_set and safe_set[0]['line'] < calls(s, 'dr.Close')[0]['line'], 'conditional-event-query-precedes-explicit-reader-close')
    for name in ('OpenForm', 'OpenWindow'):
        f = method(facts, DET, name)
        need(calls(f, 'configure') and calls(f, 'configure')[0]['line'] < min(c['line'] for c in f['calls'] if c['function'].endswith('.Show')), 'detail-configures-before-show:' + name)
    for rel in (PROD, SAFE):
        f = method(facts, rel, 'Window_Loaded')
        need(assignments(f, 'txtDate.DateTime'), 'loaded-has-later-date-writes:' + rel)
        need(any(r['attributes'].get('Loaded') == 'Window_Loaded' for r in facts['xml_elements'][rel[:-3]]), 'own-loaded-wiring:' + rel)
    need(any(r['attributes'].get('SelectionChanged') == 'cmbSafes_SelectionChanged' for r in facts['xml_elements'][SAFE[:-3]]), 'own-safe-selection-wiring')
    need(any(r['attributes'].get('Binding') == '{Binding Unit}' and r['attributes'].get('IsReadOnly') != 'True' for r in facts['xml_elements'][SAFE[:-3]]), 'saved-unit-is-an-editable-local-row-field')
    return errors


def resource_errors(facts):
    result, tables = [], facts['resources']['tables']
    def need(ok, label):
        if not ok: result.append('resource:' + label)
    need(set(tables) == {'Inv', 'Inv_Sub', 'SafesAdjust', 'SafesAdjust_Sub'}, 'four-selected-table-identities')
    need(tables['Inv']['primary_key_columns'] == ['InvGlobalID'] and tables['SafesAdjust']['primary_key_columns'] == ['id'], 'different-header-primary-keys')
    need('Is_Approved' not in tables['Inv']['columns'] and 'Is_Approved' in tables['SafesAdjust']['columns'], 'approval-column-supplied-schema-mismatch')
    need('tot_purch' in tables['Inv']['columns']
         and all(c in tables['Inv_Sub']['columns'] for c in ('InvGlobalID', 'ProductId', 'store', 'unit', 'val1', 'exchange_price'))
         and all(c in tables['SafesAdjust_Sub']['columns'] for c in ('Adjust_id', 'ItemId', 'unit', 'CurrentStock', 'RealStock')), 'detail-projection-columns-are-local-not-externalized')
    fragments = facts['resources']['fragments']
    backfill = fragments['Inv-global-backfill']['raw_xml_text']
    need(backfill.count("CONCAT(branch,'-',proc_id)") == 2 and "Inv_sub.proc_id= STable.proc_id" in backfill, 'local-backfill-producer-not-year-or-cloud-key')
    patch = fragments['SafesAdjust-stock-and-item-patch']['raw_xml_text']
    need('Add  [CurrentStock] float NULL' in patch and 'Add  [RealStock] float NULL' in patch
         and "sp_rename 'SafesAdjust_Sub.currency', 'ItemID', 'COLUMN'" in patch, 'readable-adjustment-patches-included')
    need(not any('year' in c.lower() for t in tables.values() for c in t['columns']), 'no-explicit-year-column-in-these-four-create-statements')
    need(all(f['resource_name'] for f in fragments.values()) and all(t['is_deployed_schema_attestation'] is False for t in tables.values()), 'resource-ownership-not-deployment-attestation')
    return result


def request_rows(facts):
    rows = []
    chosen = {INV: ['OpenProductionOrder', 'OpenSafeAdjust'], DET: ['OpenInvoiceByType'],
              PROD: ['dgvSrch_MouseLeftButtonUp', 'btnFirst_Click', 'btnPrevious_Click', 'btnNext_Click', 'btnLast_Click'],
              SAFE: ['dgvSrch_MouseDoubleClick']}
    for rel, names in chosen.items():
        for name in names:
            f = method(facts, rel, name)
            for call in f['calls']:
                if call['function'].rsplit('.', 1)[-1] != 'Navigate': continue
                req = {'path': rel, 'selector': name, 'line': call['line']}
                target = previous.lexical_target(facts, req) if rel in (INV, DET) else Path(rel).name.removesuffix('.xaml.cs')
                if target not in ('frmProductionOrder', 'frmSafeAdjust'): continue
                arg = call['arguments']
                table = re.search(r'\bFROM\s+(Inv|SafesAdjust)\b', arg, re.I)
                rows.append({'path': rel, 'selector': name, 'line': call['line'],
                    'function': call['function'], 'argument_expression': arg,
                    'argument_expression_sha256': base.sha(arg.encode('utf8')),
                    'source_method_sha256': f['syntax_utf8_sha256'],
                    'syntactically_named_target': target, 'target_is_compiler_bound': False,
                    'requested_table_syntax': table[1] if table else None,
                    'key_syntax': 'InvGlobalID' if 'InvGlobalID' in arg else 'local-id' if 'id=' in arg else 'ordered-header',
                    'explicit_branch_predicate_present': bool(re.search(r'\bbranch\s*=', arg, re.I)),
                    'explicit_year_or_database_selector_in_argument': bool(re.search(r'\byear\b|\bUSE\s+\w+', arg, re.I))})
    return rows


def read_errors(reads, facts, root: Path = ROOT):
    errors, covered = [], {}
    for row in reads.get('reads', []):
        rel, a, b = row['path'], row['start'], row['end']
        text = text_range(base.decode((root / rel).read_bytes()), a, b)
        if base.sha(text.encode('utf8')) != row['decoded_range_utf8_sha256']:
            errors.append('read:range-identity:' + row['id'])
        covered.setdefault(rel, set()).update(range(a, b + 1))
    selected = [(rel, name, f['start'], f['end']) for group in ('methods', 'classes')
                for rel, items in facts[group].items() for name, f in items.items()]
    selected += [(r['path'], name, r['start'], r['end']) for name, r in facts['text_ranges'].items()]
    selected += [(RESOURCE, name, r['start'], r['end']) for name, r in facts['resources']['fragments'].items()]
    selected += [(rel, 'xml-element', r['line'], r['line']) for rel, items in facts['xml_elements'].items() for r in items]
    for rel, name, a, b in selected:
        if not set(range(a, b + 1)) <= covered.get(rel, set()): errors.append('read:uncovered:' + rel + ':' + name)
    if reads.get('extraction_equals_reading') is not False or reads.get('individual_read_timestamps_invented') is not False:
        errors.append('read:no-extraction-or-invented-timestamps-as-reading-proof')
    return errors


def preservation_errors(entry, root: Path = ROOT):
    errors = []
    if entry.get('base_HEAD') != BASE_HEAD or len(entry.get('preserved_tracked_audit_inputs', {})) != 1364:
        errors.append('preservation:clean-R4-entry-identity')
    for rel, expected in entry.get('preserved_tracked_audit_inputs', {}).items():
        if rel in MUTABLE_INDEXES: continue
        raw = (root / rel).read_bytes()
        if {'bytes': len(raw), 'sha256': base.sha(raw)} != expected: errors.append('preservation:entry-input:' + rel)
    for row in base.rows('inventory.csv'):
        raw = (root / row['path']).read_bytes()
        if len(raw) != int(row['bytes']) or base.sha(raw) != row['sha256']: errors.append('preservation:application:' + row['path'])
    return errors


def evidence_errors(ev: Path = EV):
    facts, review, routes, roots, dates = [load(n, ev) for n in (FACTS, REVIEW, ROUTES, ROOTS, DATES)]
    errors = []
    def need(ok, label):
        if not ok: errors.append('evidence:' + label)
    need(routes.get('requests') == request_rows(facts), 'exact-request-identities-not-eleven-count')
    annotations = routes.get('individual_dispositions', [])
    need(len(annotations) == 11 and len(routes.get('requests', [])) == 11, 'five-report-six-local-scope-not-repository-census')
    prior = load(previous.ROUTES)
    inherited = { (r['source_request_path'], r['source_request_line']): r for r in prior['individual_dispositions'] }
    for i, (r, a) in enumerate(zip(routes.get('requests', []), annotations), 1):
        old = inherited.get((r['path'], r['line'])) if r['path'] in (INV, DET) else None
        need(a.get('id') == f'R5REQ-{i:02d}' and a.get('argument_expression_sha256') == r['argument_expression_sha256']
             and a.get('source_method_sha256') == r['source_method_sha256']
             and a.get('inherited_R4_request_id') == (old['id'] if old else None), 'individual-request-binding:' + str(i))
        need(bool(a.get('table_key_disposition')) and bool(a.get('health_disposition'))
             and a.get('observed_in_ERP') is False and a.get('is_capability_exit') is False, 'bounded-route-disposition:' + str(i))
    actual = base.rows('findings.csv', AUDIT) + base.rows('findings-additions-07B39R1.csv', ev)
    need(roots.get('available_prior_rows') == actual and len(actual) == 339, 'all-available-original-dictionaries-retained')
    need(set(roots.get('focused_root_reviews', {})) == set(FOCUSED), 'focused-prior-root-identities')
    by_id = {r['id']: r for r in actual}
    for key, value in roots.get('focused_root_reviews', {}).items():
        need(value.get('canonical_prior_row') == by_id.get(key) and bool(value.get('reason')), 'canonical-root-not-renumbered:' + key)
    expected_links = {'R5C-HEADER-TABLE': 'P7-131', 'R5C-PRODUCTION-BASE': 'P7-133', 'R5C-PRODUCTION-ROUND': 'P7-134'}
    candidates = {r['id']: r for r in roots.get('candidate_dispositions', [])}
    for key, target in expected_links.items():
        need(candidates.get(key, {}).get('root_id') == target
             and candidates.get(key, {}).get('disposition') == 'existing-root-new-source-support', 'existing-root-support:' + key)
    unit = candidates.get('R5C-ADJUSTMENT-UNIT', {})
    need(unit.get('root_id') is None and unit.get('disposition') == 'source-discrepancy-recorded-novelty-not-certified'
         and unit.get('all345_roots_screened') is False and unit.get('deployed_or_financial_failure_observed') is False, 'unit-question-not-invented-number-or-runtime-result')
    need(roots.get('new_finding_ids') == [] and roots.get('historical_root_fields_rewritten') is False
         and roots.get('missing_six_R2_dictionaries_reconstructed') is False
         and roots.get('all345_roots_screened') is False
         and roots.get('all_available339_semantically_reread_in_R5') is False, 'no-reconstructed-ledger-or-severity-promotion')
    expected_outcomes = {'P-EMPTY', 'P-HEADER-CAUGHT', 'P-DETAIL-EMPTY', 'P-ROW-PARTIAL',
                         'P-TAIL', 'S-EMPTY', 'S-HEADER-FAIL', 'S-ROW-FAIL', 'S-TAIL', 'PRE-READER-FAIL'}
    outcomes = review.get('reader_outcomes', [])
    need(len(outcomes) == len(expected_outcomes) and {r.get('id') for r in outcomes} == expected_outcomes, 'ten-distinct-bounded-health-outcomes')
    for row in outcomes:
        need(row.get('observed_in_ERP') is False and bool(row.get('source_basis'))
             and bool(row.get('limit')) and bool(row.get('source_disposition')), 'source-outcome-not-runtime:' + row.get('id', '?'))
    obligations = review.get('local_obligation_decisions', [])
    need({r.get('id') for r in obligations} == {'R5L-READER-RESET', 'R5L-FIVE-REPORT-REQUESTS', 'R5L-LOCAL-DDL', 'R5L-EVENT-MODEL', 'R5L-IDENTITY-YEAR'}, 'local-obligations-individually-disposed')
    for row in obligations:
        need(row.get('bounded_source_question_reviewed') is True and row.get('whole_capability_complete') is False
             and row.get('readable_local_externalized') is False and bool(row.get('remaining_local')), 'bounded-local-not-whole-exit:' + row.get('id', '?'))
    need(review.get('new_external_boundary_rows_issued') == 0 and review.get('formal_R4_external_register_replaced') is False, 'existing-boundary-lineage-not-new-counts')
    caps = {r['id']: r for r in base.rows('capability-register-07B38.csv', ev)}
    need(set(review.get('capabilities', {})) == set(TARGETS), 'two-bounded-canonical-capabilities')
    for cid, row in review.get('capabilities', {}).items():
        need(row.get('canonical_capability_row') == caps.get(cid) and row.get('whole_capability_certified') is False
             and row.get('local_semantic_obligations_complete') is False and bool(row.get('remaining_readable_local')), 'canonical-capability-with-named-remainder:' + cid)
    need(dates.get('assessment_reference_date_utc') == DATE and dates.get('raw_clocks_are_calendar_authority') is False
         and dates.get('historical_inputs_rewritten') is False, 'prospective-date-separate-from-raw-clock')
    for name, obj in ((REVIEW, review), (ROUTES, routes), (ROOTS, roots)):
        need(obj.get('assessment_reference_date_utc') == DATE and obj.get('raw_clocks_are_calendar_authority') is False,
             'session-reference-not-calendar-proof:' + name)
        need(obj.get('application_execution_count') == 0 and obj.get('whole_7B_static_assessment_complete') is False
             and obj.get('phase7C_started') is False and obj.get('phase8_authorized') is False, 'scope-and-execution-limits:' + name)
        need(obj.get('R2_R3_files_recovered') is False and obj.get('prior196_tests_recertified') is False, 'missing-captures-not-recertified:' + name)
    for name, obj in ((REVIEW, review), (ROUTES, routes), (ROOTS, roots), (DATES, dates)):
        need(bool(obj.get('pinned_inputs')), 'input-identities:' + name)
        for pin in obj.get('pinned_inputs', []):
            need(identity(pin['path']) == pin, 'changed-pinned-input:' + pin['path'])
    return errors


def verify(rederive=False, ev: Path = EV):
    facts = load(FACTS, ev)
    errors = []
    for rel, expected in facts['source_identity'].items():
        if identity(rel) != expected: errors.append('source-identity:' + rel)
    if rederive and facts != derive(): errors.append('fresh-original-source-rederivation-differs')
    errors += source_errors(facts) + resource_errors(facts)
    errors += read_errors(load(READS, ev), facts) + evidence_errors(ev)
    errors += preservation_errors(load(ENTRY, ev))
    return {'schema_version': 1, 'errors': errors,
            'selected_method_contexts': sum(len(m) for m in facts['methods'].values()),
            'selected_local_classes': sum(len(m) for m in facts['classes'].values()),
            'source_identities': len(facts['source_identity']), 'bounded_request_call_sites': len(facts['requests']),
            'capability_exit_certificates_issued': 0, 'four_family_exit_certificates_issued': 0,
            'whole_7B_static_assessment_complete': False, 'application_execution_count': 0,
            'phase7C_started': False, 'phase8_authorized': False,
            'limit': 'Integrity, selected syntax and recorded source-disposition guards only; no calendar, actual read, all-repository semantics, provider, deployed SQL, financial acceptance, or completion certified.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--rederive', action='store_true')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = verify(args.rederive)
    except (OSError, KeyError, ValueError, TypeError, IndexError) as exc:
        print(json.dumps({'errors': [f'{type(exc).__name__}: {exc}'], 'whole_7B_static_assessment_complete': False}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 2 if args.require_complete else 0


if __name__ == '__main__':
    sys.exit(main())
