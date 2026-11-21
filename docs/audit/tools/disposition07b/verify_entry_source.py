#!/usr/bin/env python3
"""R7 source/evidence guards for report-row -> ShowEntrySource -> receiver.

Read-only C# syntax and selected XAML/DDL text, not compilation, ERP, SQL,
WPF, provider, migration, SDK, authorization or financial acceptance. Lexical
bindings, hashes and coverage cannot authenticate an actual reading, calendar,
event schedule, deployed uniqueness, all routes, or a capability/family exit.
All previous consumed files, failures and missing-history limits are preserved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import xml.parsers.expat

import verify_session_year as prior

base, previous = prior.base, prior.previous
ROOT, AUDIT, EV = prior.ROOT, prior.AUDIT, prior.EV
P, C = prior.P, prior.C
TAG, DATE = '07B39R7', '2026-11-16'
BASE_HEAD = 'de7c56282e4fe1eb5f487e1df7d9f1a88ecc31df'
FACTS = 'entry-source-source-facts-' + TAG + '.json'
READS = 'entry-source-source-review-log-' + TAG + '.json'
REVIEW = 'entry-source-dispositions-' + TAG + '.json'
MATRIX = 'entry-source-request-matrix-' + TAG + '.json'
WORK = 'entry-source-local-worklist-' + TAG + '.json'
ROOTS = 'entry-source-root-adjudication-' + TAG + '.json'
ENTRY = 'entry-identities-' + TAG + '.json'
CORRECTION = 'source-display-attribution-note-' + TAG + '.json'
OLD_WORK = 'navigation-local-next-worklist-07B39R6.json'
MC, EO, IP = C + 'MainClass.cs', C + 'EntryOper.cs', C + 'InvoiceOper.cs'
FP, COMMON = C + 'FormPermission.cs', C + 'Common.cs'
RESOURCE = prior.prior.RESOURCE
STMT, BAL = prior.STMT, prior.BAL
CC, CU, LAST, EMP, RPT = [P + s + '.xaml.cs' for s in (
    'frmCostCenterBalance', 'frmCustAccountGet', 'frmCustLastPay', 'frmEmpAccountGet', 'frmRptCostCenter')]
PURCH, SALE, POS = [P + s + '.xaml.cs' for s in ('frmInvPurch', 'frmInvSale', 'frmInvPOS')]
RENT, INITIAL, NEW, CREDIT, DEBT, ENTRIES = [P + s + '.xaml.cs' for s in (
    'frminvoice', 'FrmIntialRestraiction', 'FrmNewEntry', 'frmCreditNote', 'frmDebtNote', 'frmRptEntries')]
RECEIPTS = {5: 'frmSandQ', 6: 'frmSandD', 7: 'frmSandQD', 8: 'frmSandSD', 9: 'frmSandVAT'}
INVOICES = ((1, 1, 'frmInvPurch'), (1, 2, 'frmInvPurch'),
            (2, 1, 'frmInvSale'), (2, 2, 'frmInvSale'),
            (3, 1, 'frmInvPOS'), (3, 2, 'frmInvPOS'))
OTHER = {3: 'frminvoice', **RECEIPTS, 0: 'FrmIntialRestraiction', 10: 'FrmNewEntry',
         16: 'frmCreditNote', 17: 'frmDebtNote', 13: 'frmRptEntries'}
RECEIVER_READERS = {'frmInvPurch': 'InvoiceOper.BindingInvoice', 'frmInvSale': 'InvoiceOper.BindingInvoice',
    'frmInvPOS': 'InvoiceOper.BindingInvoice', **{s: 'ReadData' for s in (
        'frminvoice', *RECEIPTS.values(), 'FrmNewEntry', 'frmCreditNote', 'frmDebtNote', 'frmRptEntries')},
    'FrmIntialRestraiction': 'ReadDataFromReader'}
TARGETS = ('CAP7B38-D05', 'CAP7B38-D06', 'CAP7B38-D17', 'CAP7B38-D25')
FOCUSED = ('P1-012', 'P1-013', 'P2-006', 'P3-011', 'P3-024', 'P7-061',
           'P7-115', 'P7-132', 'P7-161', 'P7-164')
DECISION_IDS = {'R7D-ROW-KEYS', 'R7D-DISPATCH', 'R7D-INVOICE-HEALTH', 'R7D-RECEIPT-HEALTH',
    'R7D-OTHER-HEALTH', 'R7D-BRANCH', 'R7D-LIFECYCLE', 'R7D-PERMISSION', 'R7D-LEGACY-LOAD'}
CANDIDATE_IDS = {'R7C-YEAR-PROVENANCE', 'R7C-RECEIPT-READER', 'R7C-BRANCH-REHYDRATION',
    'R7C-INVOICE-HEALTH', 'R7C-LIFECYCLE', 'R7C-PERMISSION', 'R7C-LEGACY-LOAD'}
CONTEXTS = {
    MC: ['ConnObj', 'DoApplyUserSett@System.Windows.Window',
         'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions'],
    FP: ['ctor:FormPermission', 'ApplyFrmPermission@object', 'ApplyFrmPermission@System.Windows.Window',
         'ApplyFrmPermissionInternal', 'LoadPermissionData', 'GetBool', 'GetTargetButtons', 'ResolveFormName'],
    COMMON: ['ApplyEditAddPermission', 'ApplyEditAddPermissionInternal'],
    EO: ['ShowEntrySource', 'ReadEntryGlobalID', 'GetEntryGlobalID',
         'GenerateEntryGlobalIDByEntryNo', 'GetEntryNobyType'],
    IP: ['GetEntryGlobalID', 'BindingInvoice'],
    CC: ['ctor:frmCostCenterBalance', 'Window_Loaded', 'BranchPermissions', 'ShowAccount', 'BuildDataTable',
         'BuildDateFilter', 'BuildAccountFilter', 'BuildTypeFilter', 'BuildBranchFilter',
         'LoadPreviousBalance', 'LoadPeriodData', 'BtnDetailCell_Click'],
    CU: ['ctor:frmCustAccountGet', 'FrmCustAccountGet_Loaded', 'ApplyBranchPermissions',
         'CollectUIParameters', 'ShowAccount', 'BuildResultTable', 'BtnDetail_CellClick'],
    LAST: ['ctor:frmCustLastPay', 'FrmCustLastPay_Loaded', 'InitializeResultTable',
           'ShowResult', 'BuildBranchFilter', 'BtnViewDetail_Click'],
    EMP: ['ctor:frmEmpAccountGet', 'FrmEmpAccountGet_Loaded', 'ApplyBranchPermissions',
          'WireUpEvents', 'ShowAccount', 'BuildResultTable', 'BtnDetail_CellClick'],
    RPT: ['ctor:frmRptCostCenter', 'Window_Loaded', 'btnShow_Click', 'DetailedResults', 'ShowResult',
          'ProcessAndAddRow', 'GetDateCondition', 'GetBranchCondition', 'GetAccountCondition', 'BtnDetail_Click'],
    STMT: list(prior.CONTEXTS[STMT]), BAL: list(prior.CONTEXTS[BAL]),
    PURCH: ['ctor:frmInvPurch', 'frmSalePurch_Load', 'ResetInvoice', 'CLR', 'Navigate', 'BindingControls', 'BindingDGV'],
    SALE: ['ctor:frmInvSale', 'Window_Loaded', 'ResetInvoice', 'CLR', 'Navigate', 'BindingControls'],
    POS: ['ctor:frmInvPOS', 'Window_Loaded', 'ResetInvoice', 'CLR', 'Navigate', 'BindingControls'],
    RENT: ['ctor:frminvoice', 'Window_Loaded', 'CLR', 'Navigate', 'ReadData'],
    INITIAL: ['ctor:FrmIntialRestraiction', 'Window_Loaded', 'LoadEntryNumber', 'Navigate',
              'ReadDataFromReader', 'NewEntry', 'ClearAll'],
    NEW: ['ctor:FrmNewEntry', 'FrmAddRestriction_Load', 'LoadResNo', 'Navigate', 'ReadData', 'NewEntry', 'ClearAll'],
    CREDIT: ['ctor:frmCreditNote', 'Window_Loaded', 'LoadNxtNo', 'Navigate', 'ReadData', 'CLR'],
    DEBT: ['ctor:frmDebtNote', 'FrmDebtNote_Loaded', 'LoadNextNumber', 'Navigate', 'ReadData', 'ClearForm'],
    ENTRIES: ['ctor:frmRptEntries', 'Window_Loaded', 'LoadLastEntry', 'GetBranchCondition', 'Navigate', 'ReadData'],
}
for _type, _stem in RECEIPTS.items():
    _names = ['ctor:' + _stem, 'Window_Loaded', 'CLR', 'RestorePreviousReceipt', 'Navigate', 'ReadData']
    _names += {5: ['LoadEditorName', 'EnsureOpen', 'EnsureClose'], 6: ['EnsureConnectionOpen'],
               7: ['SafeOpen', 'SafeClose'], 8: ['SafeOpenConnection', 'SafeCloseConnection'],
               9: ['EnsureOpen', 'EnsureClose']}[_type]
    CONTEXTS[P + _stem + '.xaml.cs'] = _names
XML_SELECTED = {rel[:-3]: set() for rel in CONTEXTS if rel.startswith(P)}
for _rel, _selector in ((CC, 'BtnDetailCell_Click'), (CU, 'BtnDetail_CellClick'),
                       (LAST, 'BtnViewDetail_Click'), (EMP, 'BtnDetail_CellClick'),
                       (RPT, 'BtnDetail_Click'), (STMT, 'BtnShowDetail_Click'), (BAL, 'BtnShowDetail_Click')):
    XML_SELECTED[_rel[:-3]].add(_selector)
TEXT_RANGES = {
    'mutable-connection-fields': (MC, 25, 49),
    'balance-captured-field': (BAL, 20, 23),
    'r6-attribution-statement-print-fragment-only': (STMT, 645, 739),
    'r6-attribution-statement-reflection-tail-only': (STMT, 760, 799),
    'Inv-create': (RESOURCE, 954, 1017),
    'CreditDeptNotes-create': (RESOURCE, 1366, 1387),
    'RentInvoice-create': (RESOURCE, 1431, 1466),
    'Receipts-create': (RESOURCE, 1496, 1532),
    'Entry-create': (RESOURCE, 1538, 1555),
    'Entry-sub-create': (RESOURCE, 1562, 1574),
    'CreditDeptNotes-if-absent': (RESOURCE, 47464, 47488),
    'Receipts-if-absent': (RESOURCE, 47877, 47912),
    'statement-key-create-fragment': (RESOURCE, 4703, 4725),
    'statement-key-alter-fragment': (RESOURCE, 50285, 50307),
}
load, identity, norm = prior.load, prior.identity, prior.norm
method, calls, assignments, guarded = prior.method, prior.calls, prior.assignments, prior.guarded


def source_methods(text, selectors):
    # R5 exposes conditions/index accesses/locals and full finally/using syntax.
    result = prior.prior.source_methods(text, selectors)
    parsed = base.Syntax(text)
    for selector in selectors:
        node = previous.selected_node(parsed, selector)
        result[selector]['throws'] = [{'text': parsed.text(n), 'line': n.start_point.row + 1}
                                      for n in base.walk(node) if n.type in ('throw_statement', 'throw_expression')]
    return result


def navigation_sites(text):
    """Lexical, source-positioned receiver/query pairs, NOT compiler bindings."""
    parsed = base.Syntax(text)
    owner = previous.selected_node(parsed, 'ShowEntrySource')
    out = []
    for node in base.walk(owner):
        if node.type != 'invocation_expression': continue
        function = parsed.text(node.child_by_field_name('function'))
        if not function.endswith('.Navigate'): continue
        variable = function.removesuffix('.Navigate')
        scope = node.parent
        while scope and scope.type not in ('block', 'switch_section'): scope = scope.parent
        declarations = [n for n in base.walk(scope) if n.type == 'variable_declarator'
                        and parsed.text(n.child_by_field_name('name')) == variable and n.start_byte < node.start_byte]
        creations = [n for d in declarations for n in base.walk(d) if n.type == 'object_creation_expression']
        receiver = parsed.text(creations[0].child_by_field_name('type')) if len(creations) == 1 else None
        args = parsed.text(node.child_by_field_name('arguments'))
        case = next((parsed.text(n) for n in scope.named_children if n.type == 'constant_pattern'), None)
        pair = re.fullmatch(r'\(invQuery\((\d+),\s*(\d+)\)\)', args)
        route_id = ('R7NAV-INV-' + pair[1] + pair[2]) if pair else ('R7NAV-ENTRY-' + case.zfill(2)) if case else ('unclassified@' + str(node.start_point.row + 1))
        same_scope_calls = [n for n in base.walk(scope) if n.type == 'invocation_expression']
        def positions(member):
            return [n.start_point.row + 1 for n in same_scope_calls
                    if parsed.text(n.child_by_field_name('function')) == variable + '.' + member]
        out.append({'id': route_id, 'receiver_variable_syntax': variable, 'receiver_type_syntax': receiver,
                    'line': node.start_point.row + 1, 'end': node.end_point.row + 1,
                    'arguments_syntax': args, 'case_label_syntax': case,
                    'lexical_scope_kind': scope.type, 'scope_start': scope.start_point.row + 1,
                    'scope_end': scope.end_point.row + 1,
                    'ancestors': previous.ancestors(parsed, node, owner),
                    'same_scope_Show_lines': positions('Show'), 'same_scope_Activate_lines': positions('Activate'),
                    'compiler_bound_target': False})
    return out


def derive(root: Path = ROOT):
    result = {'schema_version': 1, 'kind': 'R7-bounded-original-source-syntax-not-runtime-or-reading-certificate',
              'source_identity': {}, 'methods': {}, 'xml_elements': {}, 'text_ranges': {},
              'application_execution_count': 0, 'whole_7B_static_assessment_complete': False}
    for rel, selectors in CONTEXTS.items():
        result['source_identity'][rel] = identity(rel, root)
        result['methods'][rel] = source_methods(base.decode((root / rel).read_bytes()), selectors)
    for rel, needles in XML_SELECTED.items():
        text = base.decode((root / rel).read_bytes())
        result['source_identity'][rel] = identity(rel, root)
        selected = previous.xml_facts(text, needles)
        roots = []
        parser = xml.parsers.expat.ParserCreate(namespace_separator='|')
        def first(name, attrs):
            if not roots:
                roots.append({'element': name.rsplit('|', 1)[-1], 'line': parser.CurrentLineNumber,
                              'attributes': {k.rsplit('|', 1)[-1]: value for k, value in attrs.items()}})
        parser.StartElementHandler = first
        parser.Parse(text.encode('utf8'), True)
        result['xml_elements'][rel] = roots + [r for r in selected if r != roots[0]]
    for key, (rel, a, b) in TEXT_RANGES.items():
        text = prior.prior.text_range(base.decode((root / rel).read_bytes()), a, b)
        result['source_identity'][rel] = identity(rel, root)
        result['text_ranges'][key] = {'path': rel, 'start': a, 'end': b, 'text': text,
                                     'decoded_range_utf8_sha256': base.sha(text.encode('utf8'))}
    result['navigation_sites'] = navigation_sites(base.decode((root / EO).read_bytes()))
    return result


def expected_other_query(case):
    if case == 3: return '$"SELECT * FROM RentInvoice WHERE IS_Deleted=0 AND id={docNoStr} AND branch={branchStr}"'
    if case in RECEIPTS:
        return '$"SELECT * FROM Receipts WHERE ReceiptType=' + str(case) + ' AND ISDeleted=0 AND ReceiptNo={docNoStr} AND BranchID={branchStr}"'
    if case in (0, 10, 13):
        return '$"SELECT * FROM Entry WHERE IS_Deleted=0 AND type=' + str(case) + ' AND GlobalId=N\'{glid}\'"'
    return '$"SELECT * FROM CreditDeptNotes WHERE IS_Deleted=0 AND Doc_Type=' + str(case - 15) + ' AND Doc_No={docNoStr}"'


def source_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('source:' + label)
    def m(rel, name): return method(facts, rel, name)
    def has(rel, name, *snippets):
        code = norm(m(rel, name)['syntax_text'])
        return all(norm(s) in code for s in snippets)
    dispatch = m(EO, 'ShowEntrySource')
    need(dispatch['parameters'] == '(string glid)' and dispatch['return_type'] == 'void', 'one-key-void-dispatch-contract')
    need(has(MC, 'ConnObj', 'conn = new SqlConnection(connstr);', 'return conn;')
         and has(EO, 'ShowEntrySource', 'using SqlConnection conn = MainClass.ConnObj();'), 'fresh-global-connection-not-report-snapshot')
    need(has(EO, 'ShowEntrySource', '$"SELECT doc_no, type, id, branch FROM Entry WHERE GlobalId = N\'{glid}\'"',
             'if (entryTable.Rows.Count == 0) return;', 'DataRow entryRow = entryTable.Rows[0];',
             'int docNo = Convert.ToInt32(entryRow["id"]);', 'int branch = Convert.ToInt32(entryRow["branch"]);',
             'WHERE IS_Deleted=0 AND EntryID={docNo} AND branch={branch}',
             'DataRow row = invTable.Rows[0];', 'int invId = Convert.ToInt32(row["id"]);'),
         'first-row-entry-id-and-branch-probe-not-doc-no-or-global-invoice-key')
    need(has(EO, 'ShowEntrySource', 'string invQuery(int it, int pt) =>',
             '$"SELECT * FROM Inv WHERE IS_Deleted=0 AND inv_type={it} AND proc_type={pt} AND id={invId} AND branch={branch}"'),
         'invoice-query-retains-actual-literal-type-proc-id-branch')
    need(not calls(dispatch, 'MainClass.ApplyPermissionToForm') and not calls(dispatch, 'MainClass.DoApplyUserSett')
         and not dispatch['catches'] and not dispatch['throws'], 'dispatcher-no-direct-permission-call-catch-or-written-throw-not-all-app-ACL-proof')
    sites = facts['navigation_sites']
    expected = {'R7NAV-INV-' + str(i) + str(p): s for i, p, s in INVOICES}
    expected.update({'R7NAV-ENTRY-' + str(c).zfill(2): s for c, s in OTHER.items()})
    need(len(sites) == 17 and {r['id']: r['receiver_type_syntax'] for r in sites} == expected, 'exact17-navigate-sites-and14-receiver-types')
    for site in sites:
        rid = site['id']
        need(site['compiler_bound_target'] is False, 'lexical-not-compiler:' + rid)
        # Coordinates alone cannot distinguish calls sharing a physical line.
        # Check the actual written call sequence as well; still not WPF timing.
        variable, args = site['receiver_variable_syntax'], site['arguments_syntax']
        sequence = f'{variable}.Show(); {variable}.Navigate{args}; {variable}.Activate();'
        need(len(site['same_scope_Show_lines']) == len(site['same_scope_Activate_lines']) == 1
             and site['same_scope_Show_lines'][0] <= site['line'] <= site['same_scope_Activate_lines'][0]
             and norm(sequence) in norm(dispatch['syntax_text']), 'show-navigate-activate-written-order:' + rid)
        if rid.startswith('R7NAV-ENTRY-'):
            case = int(site['case_label_syntax'])
            need(norm(site['arguments_syntax']) == norm('(' + expected_other_query(case) + ')'), 'exact-switch-query:' + rid)
        elif rid.startswith('R7NAV-INV-'):
            it, pt = int(rid[-2]), int(rid[-1])
            need(norm(site['arguments_syntax']) == norm(f'(invQuery({it}, {pt}))')
                 and guarded(site, f'invType == {it} && procType == {pt}'), 'six-typed-invoice-arm-guards:' + rid)
    need(has(EO, 'ShowEntrySource', 'f.Show(); f.Navigate(invQuery(3, 2)); f.Activate();\n                }\n                return;'),
         'any-invoice-hit-returns-even-if-no-six-arm-match-not-fallback-success')
    for rel, selector, arg in ((CC, 'BtnDetailCell_Click', 'globalId'), (CU, 'BtnDetail_CellClick', 'entryNumber'),
                              (LAST, 'BtnViewDetail_Click', 'entryNumber'), (EMP, 'BtnDetail_CellClick', 'entryNumber'),
                              (RPT, 'BtnDetail_Click', 'globalId'), (STMT, 'BtnShowDetail_Click', 'genralNo'),
                              (BAL, 'BtnShowDetail_Click', 'btn.Tag.ToString()')):
        f = m(rel, selector)
        cs = calls(f, 'EntryOper.ShowEntrySource')
        need(len(cs) == 1 and norm(cs[0]['arguments']) == norm('(' + arg + ')')
             and 'MainClass.connstr' not in f['syntax_text'] and 'CmbYearPreviews' not in f['syntax_text'], 'seven-one-key-callers:' + rel)
    need(has(CC, 'LoadPeriodData', 'SELECT Entry.GlobalID', 'dt.Rows[i]["GlobalID"].ToString()',
             'globalId, docNo, branch, entryType')
         and has(CC, 'BuildDataTable', 'dt.Columns.Add("DgvGenralNo", typeof(string))', 'dt.Columns.Add("DgvEntryNo", typeof(int))')
         and has(CC, 'LoadPreviousBalance', '"0", 0, ""')
         and has(CC, 'BtnDetailCell_Click', 'btn.Tag is string globalId', '!string.IsNullOrEmpty(globalId) && globalId != "0"'),
         'cost-balance-global-key-distinct-from-doc-no-and-zero-opening-sentinel')
    for rel, show, local, column in ((CU, 'ShowAccount', 'entryNumber', 'DgvEntryNo'),
                                     (EMP, 'ShowAccount', 'entryNumber', 'DgvEntryNo'),
                                     (LAST, 'ShowResult', 'entryGlobalId', 'EntryNo')):
        handler = 'BtnViewDetail_Click' if rel == LAST else 'BtnDetail_CellClick'
        grid = 'dgvItems' if rel == LAST else 'GridControl1'
        need(has(rel, show, 'Entry.GlobalID', '["GlobalID"]', local)
             and has(rel, handler, grid + '.CurrentItem is DataRowView rowView', 'rowView["' + column + '"]?.ToString()')
             and has(rel, 'InitializeResultTable' if rel == LAST else 'BuildResultTable', 'Columns.Add("' + column + '", typeof(string))'),
             'current-item-string-contains-global-key-not-display-number:' + rel)
    need(has(CU, 'ShowAccount', 'using (var bgConn = MainClass.ConnObj())', 'new SqlDataAdapter(query, bgConn)')
         and has(EMP, 'ShowAccount', 'new SqlDataAdapter(query, _conn)')
         and has(LAST, 'ShowResult', 'new SqlDataAdapter(lastEntryQuery, _conn)'), 'caller-connections-have-distinct-capture-times')
    need(has(RPT, 'DetailedResults', 'Entry_sub.EntryGlobalID', 'row["type"], row["EntryGlobalID"]',
             'ProcessAndAddRow(row, isDetailed: true)')
         and has(RPT, 'ProcessAndAddRow', 'globalId = row["EntryGlobalID"].ToString()', 'DgvEntryGlobalId = globalId')
         and has(RPT, 'ShowResult', 'DgvEntryGlobalId = ""')
         and has(RPT, 'BtnDetail_Click', 'btn.Tag is string globalId')
         and len(m(RPT, 'BtnDetail_Click')['conditions']) == 1, 'cost-report-detail-key-versus-empty-aggregate-no-invented-nonempty-guard')
    for rel, show in ((STMT, 'ShowResult'), (BAL, 'ShowAccountData')):
        f = m(rel, 'btnShow_Click')
        invoke, restore = calls(f, show), assignments(f, 'MainClass.connstr', 'MainClass.originalConnStr')
        need(len(invoke) == len(restore) == 1 and invoke[0]['line'] < restore[0]['line']
             and assignments(f, 'MainClass.ReturnYearPreviews', 'false') and not f['finally_clauses'], 'reread-report-restore-is-normal-tail:' + rel)
    for stem, reader in RECEIVER_READERS.items():
        rel = P + stem + '.xaml.cs'
        f = m(rel, 'Navigate')
        need(f['return_type'] == 'void' and bool(calls(f, reader) or calls(f, 'this.' + reader)), 'all14-void-navigate-invoke-readers:' + stem)
        ctor = m(rel, 'ctor:' + stem)
        need(bool(calls(ctor, 'MainClass.ConnObj')), 'all14-constructors-capture-connection:' + stem)
    for rel in (PURCH, SALE, POS):
        nav = m(rel, 'Navigate')
        clear = calls(nav, 'CLR') + calls(nav, 'this.CLR')
        bind = calls(nav, 'InvoiceOper.BindingInvoice')
        need(len(clear) >= 1 and len(bind) == 1 and clear[0]['line'] < bind[0]['line']
             and any(norm(c['text']) in ('Invoic!=null', 'this.Invoic!=null') for c in nav['conditions']), 'invoice-preclear-not-found-status:' + rel)
        need(has(rel, 'ResetInvoice', 'ISNew = true;', 'IsLoaded = false;'), 'invoice-reset-new-state:' + rel)
    binding = m(IP, 'BindingInvoice')
    need(binding['return_type'] == 'void' and binding['parameters'] == '(ref InvoiceDGV Invo, string sqlstr)'
         and has(IP, 'BindingInvoice', 'sqlConnection = MainClass.ConnObj();', 'if (sqlDataReader.HasRows)',
                 'Invo.InvGlobalID =', 'Invo.Branch =', 'Invo.InvoiceItems.Add(Itm);')
         and len(assignments(binding, 'Invo', 'null')) == 2, 'shared-binder-empty-or-outer-failure-null-not-typed-outcome')
    row_catches = [r for r in binding['catches'] if r['declaration'] == '(Exception projectError4)']
    need(len(row_catches) == 1 and 'ClearProjectError' in row_catches[0]['body']
         and 'Invo = null' not in row_catches[0]['body'] and not binding['throws'], 'per-item-catch-may-skip-item-without-failed-result')
    for typ, stem in RECEIPTS.items():
        rel = P + stem + '.xaml.cs'
        reader, nav = m(rel, 'ReadData'), m(rel, 'Navigate')
        need(has(rel, 'ReadData', '["ReceiptNo"]', '["GlobalID"]', '["EntryGlobalID"]', 'CLR();'), 'receipt-reader-binds-all-three-identities:' + stem)
        resets = calls(reader, 'CLR')
        empty = next((c for c in reader['conditions'] if norm(c['text']) in ('!reader.HasRows', '!dr.HasRows')), {})
        need(empty and 'return;' in empty['consequence'] and resets and empty['line'] < resets[0]['line'], 'receipt-empty-before-reset:' + stem)
        if typ == 6:
            need(not nav['catches'] and not nav['finally_clauses']
                 and has(rel, 'Navigate', 'ReadData(dr);', 'dr.Close();', 'conn.Close();'), 'sandD-close-normal-tail-exceptions-not-normalized')
        else:
            need(bool(nav['catches']) and bool(nav['finally_clauses']) and not nav['throws'], 'receipt-navigation-catches-and-finally-not-typed-health:' + stem)
    q = m(P + RECEIPTS[5] + '.xaml.cs', 'ReadData')
    closes = [r for r in calls(q, 'reader.Close') if not guarded(r, '!reader.HasRows')]
    emp_accesses = [r for r in q['index_accesses'] if r['text'] == 'reader["EmpId"]']
    need(len(closes) == 1 and len(emp_accesses) == 2 and all(r['line'] > closes[0]['line'] for r in emp_accesses)
         and calls(q, 'LoadEditorName') and not q['catches'], 'sandQ-EmpId-access-after-reader-close-outside-LoadEditorName-catch')
    for typ in (7, 8, 9):
        f = m(P + RECEIPTS[typ] + '.xaml.cs', 'ReadData')
        closes = [r for r in calls(f, 'reader.Close') if not guarded(r, '!reader.HasRows')]
        accesses = [r for r in f['index_accesses'] if r['text'].startswith('reader[')]
        need(len(closes) == 1 and accesses and all(r['line'] < closes[0]['line'] for r in accesses), 'other-selected-receipt-readers-read-fields-before-close:' + str(typ))
    rental_nav = m(RENT, 'Navigate')
    print_flags, rental_reads = assignments(rental_nav, 'this.SrchPrint', 'true'), calls(rental_nav, 'this.ReadData')
    need(has(RENT, 'ReadData', 'if (!dr.HasRows) { this.CLR(); return; }')
         and bool(m(RENT, 'ReadData')['catches']) and not m(RENT, 'ReadData')['throws']
         and len(print_flags) == len(rental_reads) == 1 and not print_flags[0]['ancestors']
         and rental_reads[0]['line'] < print_flags[0]['line'], 'rental-empty-or-caught-reader-still-normal-void-return-to-print-flag')
    for rel, reader, clear in ((INITIAL, 'ReadDataFromReader', 'ClearAll'), (NEW, 'ReadData', 'ClearAll'),
                               (CREDIT, 'ReadData', 'CLR'), (DEBT, 'ReadData', 'ClearForm'), (ENTRIES, 'ReadData', '_detailSource.Clear')):
        f = m(rel, reader)
        empty = next((c for c in f['conditions'] if norm(c['text']) in ('!reader.HasRows', '!dr.HasRows')), {})
        clears = calls(f, clear)
        need(empty and 'return;' in empty['consequence'] and clears and empty['line'] < clears[0]['line'], 'other-receiver-empty-keeps-existing-state-before-clear:' + rel)
    need(has(INITIAL, 'ReadDataFromReader', 'WHERE branch = {MainClass.BranchNo}', "AND EntryGlobalId = N'{txtEntryGID.Text}'")
         and not has(INITIAL, 'ReadDataFromReader', 'reader["branch"]'), 'initial-entry-header-global-key-detail-current-branch-not-loaded-branch')
    need(has(NEW, 'ReadData', 'txtBranch.Text = dr["branch"].ToString();', "where EntryGlobalId=N'{txtEntryGID.Text}'"), 'manual-entry-different-global-detail-policy-not-all-receivers-same')
    for rel, typ, code, number in ((CREDIT, 16, 'Code', 'LoadNxtNo'), (DEBT, 17, '_currentCode', 'LoadNextNumber')):
        need(has(rel, 'ReadData', code + '.ToString(), ' + str(typ) + ', MainClass.BranchNo')
             and has(rel, number, 'SELECT MAX(Doc_No) FROM CreditDeptNotes', 'WHERE Doc_Type=' + str(typ - 15))
             and 'Branch' not in m(rel, number)['syntax_text'], 'notes-current-branch-entry-relookup-and-global-max-counterevidence:' + rel)
    need(has(EO, 'ReadEntryGlobalID', 'WHERE branch = {branchNo} AND type = {type} AND doc_no = {docNo}', 'MainClass.ConnObj()'), 'note-entry-lookup-scope-is-explicit-not-original-glid')
    need(has(CU, 'ApplyBranchPermissions', 'chkAllBranches.IsChecked = false;')
         and has(CU, 'FrmCustAccountGet_Loaded', 'ApplyBranchPermissions();', 'chkAllBranches.IsChecked = true;')
         and calls(m(CU, 'FrmCustAccountGet_Loaded'), 'ApplyBranchPermissions')[0]['line']
             < assignments(m(CU, 'FrmCustAccountGet_Loaded'), 'chkAllBranches.IsChecked', 'true')[0]['line'], 'customer-load-later-all-flag-overwrites-local-branch-default-not-runtime-ACL-proof')
    need(has(PURCH, 'frmSalePurch_Load', 'this.FrmPermission.ApplyFrmPermission(this);', 'this.ResetInvoice();')
         and has(FP, 'ctor:FormPermission', 'Editable = true;', 'Addable = true;')
         and has(FP, 'ApplyFrmPermissionInternal', 'if (permissionTable.Rows.Count <= 0) return;')
         and has(MC, 'ApplyPermissionToForm@System.Windows.Window', 'if (dt.Rows.Count == 0) return;')
         and len(m(MC, 'ApplyPermissionToForm@System.Windows.Window')['catches']) == 1,
         'existing-permission-default-root-not-universal-absence-or-accepted-document-ACL')
    need(has(SALE, 'ctor:frmInvSale', 'Loaded += Window_Loaded;')
         and facts['xml_elements'][SALE[:-3]][0]['attributes'].get('Loaded') == 'Window_Loaded'
         and has(POS, 'CLR', 'ProcType = 1;') and has(POS, 'Window_Loaded', 'ProcType = 1;'), 'loaded-reset-and-POS-type-writers-are-real-schedule-not-inferred')
    for stem in ('frmInvPurch', 'frmInvSale', 'frmInvPOS'):
        rel = P + stem + '.xaml.cs'
        loader = 'frmSalePurch_Load' if stem == 'frmInvPurch' else 'Window_Loaded'
        need(bool(calls(m(rel, loader), 'ResetInvoice') or calls(m(rel, loader), 'this.ResetInvoice')), 'loaded-reset-hook:' + stem)
    for typ, stem in RECEIPTS.items():
        rel = P + stem + '.xaml.cs'
        restore = m(rel, 'RestorePreviousReceipt')
        need(calls(m(rel, 'Window_Loaded'), 'RestorePreviousReceipt')
             and 'DELETE FROM Sand' in restore['syntax_text'], 'loaded-receipt-restore-source-has-writes-not-run:' + stem)
        if typ in (6, 7, 8): need('SaveReceipt2' in restore['syntax_text'], 'legacy-receipt-migration-call-not-a-pure-read:' + stem)
    for key, table, pk in (('Inv-create', 'Inv', 'InvGlobalID'), ('Receipts-create', 'Receipts', 'GlobalID'),
                           ('Entry-create', 'Entry', 'GlobalID'), ('CreditDeptNotes-create', 'CreditDeptNotes', 'Id'),
                           ('RentInvoice-create', 'RentInvoice', 'proc_id')):
        text = facts['text_ranges'][key]['text']
        need('[dbo].[' + table + ']' in text and 'PRIMARY KEY CLUSTERED' in text and '[' + pk + '] ASC' in text, 'supplied-DDL-key-not-deployed-unique-tuple:' + key)
    for key in ('CreditDeptNotes-create', 'CreditDeptNotes-if-absent'):
        need('[BranchId] [int] NULL' in facts['text_ranges'][key]['text'], 'notes-readable-branch-column:' + key)
    for key in ('statement-key-create-fragment', 'statement-key-alter-fragment'):
        need('es.EntryGlobalID AS DgvGenralNo' in facts['text_ranges'][key]['text'], 'statement-global-key-alias-not-local-doc-no:' + key)
    for rel, selector, tag in ((CC, 'BtnDetailCell_Click', '{Binding Path=RowData.Row.DgvGenralNo}'),
                               (RPT, 'BtnDetail_Click', '{Binding DgvEntryGlobalId}'),
                               (STMT, 'BtnShowDetail_Click', '{Binding DgvGenralNo}'),
                               (BAL, 'BtnShowDetail_Click', '{Binding DgvGenralNo}')):
        need(any(r['attributes'].get('Click') == selector and r['attributes'].get('Tag') == tag
                 for r in facts['xml_elements'][rel[:-3]]), 'XAML-key-click-link:' + rel)
    for rel, selector in ((CU, 'BtnDetail_CellClick'), (LAST, 'BtnViewDetail_Click'), (EMP, 'BtnDetail_CellClick')):
        need(any(r['attributes'].get('Click') == selector and 'Tag' not in r['attributes']
                 for r in facts['xml_elements'][rel[:-3]]), 'XAML-current-item-not-an-invented-per-row-key-argument:' + rel)
    return errors


def preservation_errors(entry, root: Path = ROOT):
    errors = []
    if entry.get('HEAD') != BASE_HEAD or len(entry.get('preserved_tracked_audit_inputs', {})) != 1477:
        errors.append('preservation:post-recovery-R6-entry-identities')
    for rel, expected in entry.get('preserved_tracked_audit_inputs', {}).items():
        raw = (root / rel).read_bytes()
        same = {'bytes': len(raw), 'sha256': base.sha(raw)} == expected
        if not same and rel in prior.prior.MUTABLE_INDEXES:
            same = len(raw) > expected['bytes'] and base.sha(raw[-expected['bytes']:]) == expected['sha256']
        if not same: errors.append('preservation:prior-audit:' + rel)
    for row in base.rows('inventory.csv'):
        raw = (root / row['path']).read_bytes()
        if len(raw) != int(row['bytes']) or base.sha(raw) != row['sha256']: errors.append('preservation:application:' + row['path'])
    for pin in entry.get('pinned_recovery_inputs', []):
        if identity(pin['path'], root) != pin: errors.append('preservation:recovery-note:' + pin['path'])
    return errors


def evidence_errors(ev: Path = EV):
    facts, review, matrix, work, roots, correction = [load(n, ev) for n in (FACTS, REVIEW, MATRIX, WORK, ROOTS, CORRECTION)]
    errors = []
    def need(ok, label):
        if not ok: errors.append('evidence:' + label)
    original = load(OLD_WORK)['calls']
    entry_calls = [r for r in original if r['family'] == 'entry-source']
    dispositions = work.get('individual_caller_dispositions', [])
    need([r.get('original_R6_call_row') for r in dispositions] == entry_calls and len(entry_calls) == 7, 'all-seven-exact-original-call-identities-not-count-only')
    pending = [r['id'] for r in entry_calls if not r['containing_context_selected_and_read_in_R6']]
    need(work.get('five_original_pending_ids') == pending and len(pending) == 5, 'five-original-not-selected-in-R6-not-never-reviewed')
    for r in dispositions:
        old = r['original_R6_call_row']; f = facts['methods'].get(old['path'], {}).get(old['containing_selector'], {})
        need(r.get('current_whole_context_sha256') == f.get('syntax_utf8_sha256')
             and r.get('whole_containing_context_read_in_R7') is True and r.get('source_decision_id') == 'R7D-ROW-KEYS'
             and bool(r.get('source_to_key_trace')) and bool(r.get('connection_scope_disposition')),
             'individual-full-caller-body-and-provenance:' + old['id'])
    need(work.get('remaining_original_R6_non_entry_calls') == [r for r in original if r['family'] != 'entry-source'], 'nineteen-LastProcess-and-eleven-linked-identities-carried-not-recertified')
    need(all(work.get(k) is False for k in ('original_R6_discovery_or_read_flags_rewritten',
             'all_repository_alias_or_reflection_calls_certified', 'whole_D17_complete',
             'all_receiver_helpers_or_Save_paths_complete')) and bool(work.get('remaining_work')),
         'selected-callers-not-whole-navigation-or-all-helpers')
    need(review.get('new_numbered_finding_ids') == [] and review.get('formal_prior_boundary_registers_replaced') is False
         and review.get('all17_requests_have_typed_healthy_results') is False,
         'no-numbered-closure-handoff-register-replacement-or-invented-CSharp-outcomes')
    rows = matrix.get('routes', [])
    need([r.get('source_site') for r in rows] == facts['navigation_sites'], 'every-seventeen-source-site-pair-not-a-numeric-coverage-claim')
    for row in rows:
        site = row['source_site']; stem = site['receiver_type_syntax']; rel = P + stem + '.xaml.cs'
        reader = RECEIVER_READERS[stem]
        rf = method(facts, IP, 'BindingInvoice') if reader == 'InvoiceOper.BindingInvoice' else method(facts, rel, reader)
        need(row.get('receiver_navigate_sha256') == facts['methods'][rel]['Navigate']['syntax_utf8_sha256']
             and row.get('receiver_constructor_sha256') == facts['methods'][rel]['ctor:' + stem]['syntax_utf8_sha256']
             and row.get('reader_selector') == reader and row.get('reader_whole_context_sha256') == rf['syntax_utf8_sha256']
             and row.get('whole_selected_Navigate_and_reader_bodies_read') is True
             and row.get('outcome_labels_are_audit_categories_not_CSharp_return_types') is True
             and bool(row.get('request_identity_disposition')) and bool(row.get('scope_and_allowed_set_disposition'))
             and set(row.get('source_outcomes', {})) == {'FoundPath', 'Empty', 'Failed', 'Partial', 'Unsupported', 'Denied'}
             and all(bool(s) for s in row['source_outcomes'].values())
             and bool(row.get('remaining_readable_local')) and row.get('runtime_observed') is False
             and row.get('whole_receiver_certified') is False and row.get('accepted_external_handoff') is False,
             'route-identity-scope-and-qualified-outcomes:' + site['id'])
    need({r.get('id') for r in review.get('source_decisions', [])} == DECISION_IDS, 'nine-source-decision-identities')
    for row in review.get('source_decisions', []):
        need(bool(row.get('source_basis')) and bool(row.get('source_disposition')) and bool(row.get('limit'))
             and row.get('observed_in_ERP') is False and row.get('is_capability_exit') is False, 'qualified-source-decision:' + row.get('id', '?'))
    caps = {r['id']: r for r in base.rows('capability-register-07B38.csv')}
    need(set(review.get('capabilities', {})) == set(TARGETS), 'four-named-bounded-capabilities')
    for cid, row in review.get('capabilities', {}).items():
        need(row.get('canonical_capability_row') == caps.get(cid) and row.get('whole_capability_certified') is False
             and row.get('local_semantic_obligations_complete') is False and row.get('readable_local_externalized') is False
             and bool(row.get('remaining_readable_local')), 'canonical-capability-and-readable-local-remainder:' + cid)
    actual = base.rows('findings.csv', AUDIT) + base.rows('findings-additions-07B39R1.csv')
    need(roots.get('available_prior_rows') == actual and len(actual) == 339, 'same339-available-dictionaries')
    by_id = {r['id']: r for r in actual}
    need(set(roots.get('focused_root_reviews', {})) == set(FOCUSED), 'ten-focused-roots-not-all339-newly-reviewed')
    for key, row in roots.get('focused_root_reviews', {}).items():
        need(row.get('canonical_prior_row') == by_id.get(key) and bool(row.get('reason')), 'unchanged-canonical-root:' + key)
    candidates = roots.get('candidate_dispositions', [])
    need({r.get('id') for r in candidates} == CANDIDATE_IDS and len(candidates) == len(CANDIDATE_IDS), 'seven-distinct-source-candidates')
    mapped = {r['id']: r for r in candidates}
    for cid, root in (('R7C-INVOICE-HEALTH', 'P7-161'), ('R7C-LIFECYCLE', 'P7-132'), ('R7C-PERMISSION', 'P1-012')):
        need(mapped.get(cid, {}).get('root_id') == root, 'existing-root-not-duplicated:' + cid)
    for cid in CANDIDATE_IDS - {'R7C-INVOICE-HEALTH', 'R7C-LIFECYCLE', 'R7C-PERMISSION'}:
        r = mapped.get(cid, {})
        need(r.get('root_id') is None and r.get('novelty_certified') is False and bool(r.get('remaining_local')),
             'unnumbered-bounded-source-question:' + cid)
    for r in candidates:
        need(r.get('observed_financial_or_provider_failure') is False and bool(r.get('owner_role'))
             and bool(r.get('required_redacted_input')) and bool(r.get('absence_impact'))
             and bool(r.get('next_action')) and r.get('accepted_external_handoff') is False,
             'owned-question-not-an-accepted-handoff:' + r.get('id', '?'))
    need(roots.get('new_finding_ids') == [] and roots.get('historical_root_fields_rewritten') is False
         and roots.get('all345_roots_screened') is False and roots.get('all339_semantically_reread_in_R7') is False
         and roots.get('missing_six_dictionaries_reconstructed') is False, 'no-invented-novelty-history-or-promotion')
    old_reads = load(prior.READS)['reads']
    disputed = [r for r in old_reads if r['id'] in ('R6READ-19', 'R6READ-20', 'R6READ-21', 'R6READ-22', 'R6READ-23', 'R6READ-24', 'R6READ-25')]
    need(correction.get('preserved_original_R6_range_rows') == disputed
         and correction.get('prior_actual_display_chronology_reconstructed') is False
         and correction.get('R6_consumed_log_rewritten') is False
         and correction.get('prospective_R7_reread_is_not_retroactive_R6_read_certification') is True,
         'display-attribution-reread-not-history-rewrite')
    newreads = load(READS, ev)['reads']; cover = {}
    for r in newreads: cover.setdefault(r['path'], set()).update(range(r['start'], r['end'] + 1))
    for r in disputed:
        need(set(range(r['start'], r['end'] + 1)) <= cover.get(r['path'], set()), 'prospective-reread-exact-prior-range:' + r['id'])
    for name, obj in ((REVIEW, review), (MATRIX, matrix), (WORK, work), (ROOTS, roots), (CORRECTION, correction)):
        need(obj.get('assessment_reference_date_utc') == DATE and obj.get('raw_clocks_are_calendar_authority') is False,
             'assessment-reference-not-clock-authentication:' + name)
        need(obj.get('application_execution_count') == 0 and obj.get('whole_7B_static_assessment_complete') is False
             and obj.get('phase7C_started') is False and obj.get('phase8_authorized') is False
             and obj.get('prior196_tests_recertified') is False and obj.get('R2_R3_files_recovered') is False
             and obj.get('new_accepted_external_handoffs') == 0, 'static-open-scope-and-missing-artifacts:' + name)
        need(bool(obj.get('pinned_inputs')), 'explicit-input-identities:' + name)
        for pin in obj.get('pinned_inputs', []): need(identity(pin['path']) == pin, 'changed-pinned-input:' + pin['path'])
    return errors


def verify(rederive=False, ev: Path = EV):
    facts = load(FACTS, ev)
    errors = []
    for rel, pin in facts['source_identity'].items():
        if identity(rel) != pin: errors.append('source-identity:' + rel)
    if rederive and derive() != facts: errors.append('fresh-source-rederivation-differs')
    errors += source_errors(facts) + prior.read_errors(load(READS, ev), facts)
    errors += preservation_errors(load(ENTRY, ev)) + evidence_errors(ev)
    return {'schema_version': 1, 'errors': errors,
            'selected_complete_method_contexts': sum(len(fs) for fs in facts['methods'].values()),
            'selected_source_identities': len(facts['source_identity']), 'original_entry_calls_disposed': 7,
            'five_original_pending_bodies_read': 5, 'dispatcher_navigate_sites': len(facts['navigation_sites']),
            'distinct_receiver_types': len({r['receiver_type_syntax'] for r in facts['navigation_sites']}),
            'capability_exit_certificates_issued': 0, 'four_family_exit_certificates_issued': 0,
            'whole_7B_static_assessment_complete': False, 'application_execution_count': 0,
            'phase7C_started': False, 'phase8_authorized': False,
            'limit': 'Recorded source assertions/identity/coverage only; not reading, calendar, WPF order, all local helpers, deployed schema, authorization, runtime, financial or whole-capability acceptance.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--rederive', action='store_true')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args(argv)
    try:
        result = verify(args.rederive)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({'errors': [f'{type(exc).__name__}: {exc}'], 'whole_7B_static_assessment_complete': False}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 2 if args.require_complete else 0


if __name__ == '__main__':
    sys.exit(main())
