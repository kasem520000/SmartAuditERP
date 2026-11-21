#!/usr/bin/env python3
"""R6 source-only session/year/linked-result review guards, NOT ERP execution.

Fresh pinned C# syntax and XAML/text coordinates support bounded assertions.
No C# or SQL is compiled/run; no WPF/provider/SDK, live identity, financial result,
calendar, actual human reading or capability/family exit is certified by a pass.
R1/R4/R5/B38 consumed tools, captures and genuine failures are never rewritten.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
import xml.parsers.expat

import verify_production_adjustment as prior

previous = prior.previous
base = prior.base
ROOT, AUDIT, EV = prior.ROOT, prior.AUDIT, prior.EV
TAG, DATE = '07B39R6', '2026-11-16'
BASE_HEAD = '9602467692028e391365e2dbb52e0cb551e45378'
FACTS = 'session-year-source-facts-' + TAG + '.json'
READS = 'session-year-source-review-log-' + TAG + '.json'
REVIEW = 'session-year-dispositions-' + TAG + '.json'
WORK = 'session-year-local-worklist-' + TAG + '.json'
ROOTS = 'session-year-root-adjudication-' + TAG + '.json'
ENTRY = 'entry-identities-' + TAG + '.json'
P, C = previous.P, previous.C
HOME, MC = 'SmartAuditERP/Home.xaml.cs', C + 'MainClass.cs'
LOGIN, SALE = P + 'frmUserLogin.xaml.cs', P + 'frmInvSale.xaml.cs'
SEARCH, ITEMS = P + 'frmInvoiceSrch.xaml.cs', P + 'frmInvoiceItems.xaml.cs'
STMT, BAL = P + 'frmAccountsStatement.xaml.cs', P + 'frmAccountBalance.xaml.cs'
CONTRACT, SETTINGS = P + 'frmcontract.xaml.cs', P + 'frmSettings.xaml.cs'
IP, IPC, ENTRYOPER = C + 'InvoiceOper.cs', C + 'InvoiceOperContract.cs', C + 'EntryOper.cs'
STARTUP, RESOURCE = C + 'StartupData.cs', prior.RESOURCE
OLD_WORK = 'identity-year-local-worklist-rev02-07B39R5.json'
TARGETS = ('CAP7B38-D05', 'CAP7B38-D17', 'CAP7B38-D21', 'CAP7B38-D22')
FOCUSED = ('P1-009', 'P1-017', 'P1-031', 'P2-003', 'P2-012', 'P3-021',
           'P4-012', 'P4-021', 'P7-061', 'P7-115', 'P7-132', 'P7-144', 'P7-160')
CONTEXTS = {
    HOME: ['ctor:Home', 'Window_Loaded', 'checkConn'],
    MC: ['ConnObj'],
    LOGIN: ['ctor:frmUserLogin', 'Window_Loaded', 'Login', 'BuildConnectionStrings',
            'BuildLogConnectionString', 'UpdateHomeStatusBar', 'SaveStartupData',
            'OnlineLogin', 'OfflineLogin', 'LoadData', 'loadDBs', 'LoadBranches',
            'cmbDatabases_SelectionChangeCommitted'],
    SALE: ['ctor:frmInvSale', 'Window_Loaded', 'Window_Closing', 'LoadInvNo',
           'loadDB_by_DbAutoName', 'ResetInvoice', 'CLR', 'Navigate',
           'CheckBeforeClear', 'btnNew_Click', 'btnClose_Click',
           'btnInsertLinkedInv_Click', 'InsertLinkedReturn',
           'InsertLinkedFromQuotation', 'InsertLinkedCreditNote',
           'StripImportInv_Click', 'CmbYearPreviews_DropDownOpened',
           'CmbYearPreviews_SelectionChanged'],
    SEARCH: ['ctor:frmInvoiceSrch', 'Window_Loaded', 'Window_KeyDown', 'btnClose_Click',
             'dgvItems_MouseDoubleClick', 'BtnReturn_Click', 'LoadInvoices', 'BuildLoadQuery'],
    ITEMS: ['ctor:frmInvoiceItems', 'Window_Loaded', 'Window_KeyDown', 'btnClose_Click',
            'btnadd_Click', 'btnAddall_Click', 'LoadData', 'BuildLoadQuery',
            'InsertSelectedItems', 'RemoveNonSelectedItems', 'CloseWithoutResult'],
    STMT: ['ctor:frmAccountsStatement', 'LoadYearPreviews', 'GetAccountStatement',
           'ShowResult', 'btnShow_Click', 'CmbYearPreviews_DropDown',
           'CmbYearPreviews_SelectionChanged', 'BtnShowDetail_Click'],
    BAL: ['ctor:frmAccountBalance', 'ShowAccountData', 'GetPreviousBalance',
          'GetAccountMovements', 'CreateResultTable', 'btnShow_Click',
          'LoadYearPreviewsList', 'CmbYearPreviews_DropDown',
          'CmbYearPreviews_SelectionChanged', 'BtnShowDetail_Click'],
    CONTRACT: ['ctor:frmcontract', 'frmcontract_Load', 'frmcontract_Closing',
               'SetupButtonEvents', 'CLRForm', 'CLR', 'ResetInvoice', 'LoadInvNo',
               'GetInvoiceNo', 'btnInsertLinkedInv_Click'],
    IP: ['InvoiceNo', 'GetInvoiceGlobalID', 'InsertFromInv'],
    IPC: ['InsertFromInv'], ENTRYOPER: ['ShowEntrySource'],
    SETTINGS: ['loadDB_by_DbAutoName', 'GridControl2_ButtonClick', 'GridControl3_ButtonClick',
               'InsertInto_YearPreviews', 'Delete_YearPreviews'],
}
XML_SELECTED = {
    SALE[:-3]: {'CmbYearPreviews', 'btnInsertLinkedInv', 'Window_Closing'},
    SEARCH[:-3]: {'btnClose', 'Window_KeyDown'},
    ITEMS[:-3]: {'btnClose', 'btnadd', 'btnAddall', 'Window_KeyDown'},
    STMT[:-3]: {'CmbYearPreviews', 'btnShow_Click', 'BtnShowDetail_Click'},
    BAL[:-3]: {'CmbYearPreviews', 'btnShow_Click', 'BtnShowDetail_Click'},
    CONTRACT[:-3]: {'CmbYearPreviews', 'btnInsertLinkedInv'},
}
TEXT_RANGES = {
    'mutable-session-fields': (MC, 25, 49),
    'shared-year-flag': (MC, 119, 123),
    'search-connection-fields': (SEARCH, 38, 43),
    'items-connection-field': (ITEMS, 38, 43),
    'balance-connection-field': (BAL, 20, 23),
    'startup-class': (STARTUP, 4, 39),
    'year-registry-create': (RESOURCE, 4798, 4808),
    'year-registry-if-absent': (RESOURCE, 50417, 50431),
    'statement-entry-key-create-fragment': (RESOURCE, 4703, 4725),
    'statement-entry-key-alter-fragment': (RESOURCE, 50285, 50307),
}
load, identity = prior.load, prior.identity
method, assignments, guarded, norm = prior.method, prior.assignments, prior.guarded, prior.norm
def source_methods(text, selectors):
    result = previous.source_methods(text, selectors)
    parsed = base.Syntax(text)
    for name in selectors:
        node = previous.selected_node(parsed, name)
        result[name]['finally_ranges'] = [
            {'start': n.start_point.row + 1, 'end': n.end_point.row + 1}
            for n in base.walk(node) if n.type == 'finally_clause']
    return result


def calls(f, function):
    return [c for c in f['calls'] if norm(c['function']) == norm(function)]


def derive(root: Path = ROOT):
    out = {'schema_version': 1, 'kind': 'new-R6-bounded-source-syntax-not-runtime-or-missing-R2-R3-reconstruction',
           'source_identity': {}, 'methods': {}, 'xml_elements': {}, 'text_ranges': {},
           'application_execution_count': 0, 'whole_7B_static_assessment_complete': False}
    for rel, names in CONTEXTS.items():
        text = base.decode((root / rel).read_bytes())
        out['source_identity'][rel] = identity(rel, root)
        out['methods'][rel] = source_methods(text, names)
    for rel, needles in XML_SELECTED.items():
        text = base.decode((root / rel).read_bytes())
        out['source_identity'][rel] = identity(rel, root)
        selected = previous.xml_facts(text, needles)
        parser = xml.parsers.expat.ParserCreate(namespace_separator='|')
        first = []
        def start(name, attrs):
            if not first:
                first.append({'element': name.rsplit('|', 1)[-1], 'line': parser.CurrentLineNumber,
                              'attributes': {k.rsplit('|', 1)[-1]: v for k, v in attrs.items()}})
        parser.StartElementHandler = start
        parser.Parse(text.encode('utf8'), True)
        out['xml_elements'][rel] = first + [r for r in selected if r != first[0]]
    for name, (rel, a, b) in TEXT_RANGES.items():
        text = prior.text_range(base.decode((root / rel).read_bytes()), a, b)
        out['source_identity'][rel] = identity(rel, root)
        out['text_ranges'][name] = {'path': rel, 'start': a, 'end': b,
            'text': text, 'decoded_range_utf8_sha256': base.sha(text.encode('utf8'))}
    # Discovery is restricted to the same eight literal-qualified owners as R5.
    # Parsing/extraction is not a body-read certificate or alias/reflection census.
    writes = []
    for rel in sorted(load(OLD_WORK)['source_identity']):
        parsed = base.Syntax(base.decode((root / rel).read_bytes()))
        for node in base.walk(parsed.tree.root_node):
            if node.type != 'assignment_expression': continue
            left = parsed.text(node.child_by_field_name('left'))
            if left not in ('MainClass.connstr', 'MainClass.originalConnStr', 'MainClass.Database', 'MainClass.DataBaseName'): continue
            member = node.parent
            while member and member.type not in ('method_declaration', 'constructor_declaration'):
                member = member.parent
            writes.append({'path': rel, 'line': node.start_point.row + 1, 'left': left,
                'containing_member': parsed.text(member.child_by_field_name('name')) if member else None,
                'context_start': member.start_point.row + 1 if member else None,
                'context_end': member.end_point.row + 1 if member else None})
    out['literal_qualified_writes_in_R5_eight_owners'] = sorted(writes, key=lambda r: (r['path'], r['line'], r['left']))
    return out


def source_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('source:' + label)
    def m(rel, name): return method(facts, rel, name)
    def has(rel, name, *snippets):
        code = norm(m(rel, name)['syntax_text'])
        return all(norm(s) in code for s in snippets)
    factory = m(MC, 'ConnObj')
    need(assignments(factory, 'conn', 'new SqlConnection(connstr)') and len(factory['returns']) == 1,
         'factory-captures-connstr-does-not-derive-it-from-Database')
    need('originalConnStr = connstr' in facts['text_ranges']['mutable-session-fields']['text'],
         'original-connection-backup-is-single-shared-field')
    home = m(HOME, 'checkConn')
    need(assignments(home, 'MainClass.Database', 'dbName') and not assignments(home, 'MainClass.connstr')
         and len(home['catches']) == 1, 'home-startup-updates-name-and-local-connection-not-global-string')
    hl = m(HOME, 'Window_Loaded')
    need(calls(hl, 'this.checkConn') and assignments(hl, 'this.conn', 'MainClass.ConnObj()')
         and calls(hl, 'this.checkConn')[0]['line'] < assignments(hl, 'this.conn', 'MainClass.ConnObj()')[0]['line'],
         'home-load-recaptures-global-after-startup-check')
    login, startup = m(LOGIN, 'Login'), m(LOGIN, 'SaveStartupData')
    need(assignments(login, 'MainClass.DataBaseName', 'cmbDatabases.Text')
         and assignments(login, 'txtDatabase', 'cmbDatabases.SelectedValue?.ToString().Trim() ?? ""'),
         'database-display-label-is-distinct-from-selected-physical-name')
    need(has(LOGIN, 'SaveStartupData', 'DatabaseName = cmbDatabases.SelectedValue?.ToString() ?? ""',
             'JsonConvert.SerializeObject(startupData, Formatting.Indented)', 'File.WriteAllText('),
         'startup-persistence-has-physical-name-without-reading-actual-credentials')
    need(has(LOGIN, 'SaveStartupData', 'Remember = chkRemember.IsChecked == true', 'Password = txtPwd.Password'),
         'existing-plaintext-startup-root-not-a-new-id')
    need(has(LOGIN, 'LoadData', 'txtDatabase = startupData.DatabaseName;', 'MainClass.Database = txtDatabase;',
             'cmbDatabases.SelectedValue = txtDatabase;', 'LoadBranches();'), 'load-startup-and-database-selection-path')
    need(has(LOGIN, 'loadDBs', 'master.dbo.DatabasesManagment', 'master.dbo.sysdatabases',
             'cmbDatabases.DisplayMemberPath = "Dbname";', 'cmbDatabases.SelectedValuePath = "name";'),
         'master-catalog-physical-name-versus-label-not-invented-year-partition')
    build = m(LOGIN, 'BuildConnectionStrings')
    need(len(assignments(build, 'MainClass.connstr')) == 3 and build['syntax_text'].count('MultipleActiveResultSets=true') == 3,
         'login-builder-has-MARS-in-three-source-branches')
    branches = m(LOGIN, 'LoadBranches')
    need(len(assignments(branches, 'MainClass.connstr')) == 3
         and assignments(branches, 'MainClass.connstr', 'conn.ConnectionString')
         and 'MultipleActiveResultSets' not in branches['syntax_text'],
         'later-branch-load-may-replace-global-builder-string')
    need(assignments(m(LOGIN, 'cmbDatabases_SelectionChangeCommitted'), 'MainClass.Database', 'dbName')
         and has(LOGIN, 'BuildLogConnectionString', 'Initial Catalog={MainClass.Database}'),
         'database-field-and-log-fallback-remain-separate-provenance')
    for rel, show in ((STMT, 'ShowResult'), (BAL, 'ShowAccountData')):
        f = m(rel, 'btnShow_Click')
        switches = assignments(f, 'MainClass.connstr')
        backups = assignments(f, 'MainClass.originalConnStr', 'MainClass.connstr')
        resets = assignments(f, 'MainClass.ReturnYearPreviews', 'false')
        need(len(backups) == 1 and guarded(backups[0], 'MainClass.ReturnYearPreviews && CmbYearPreviews.SelectedValue != null'),
             'report-switch-requires-global-flag-and-nonnull-selection:' + rel)
        need(len(switches) == 2 and 'database={CmbYearPreviews.SelectedValue};trusted_connection=true' in switches[0]['right']
             and switches[1]['right'] == 'MainClass.originalConnStr', 'report-switch-and-string-restore:' + rel)
        invoke = calls(f, show)
        need(len(invoke) == 1 and len(resets) == 1 and len(switches) == 2
             and switches[0]['line'] < invoke[0]['line'] < switches[1]['line'] < resets[0]['line']
             and len(assignments(f, '_connection', 'MainClass.ConnObj()')) == 2
             and not f['finally_ranges'], 'report-restore-is-normal-tail-not-finally:' + rel)
        need(not any('CmbYearPreviews.Selected' in a['left'] for a in f['assignments']),
             'visible-year-is-not-cleared-with-global-flag:' + rel)
        detail = m(rel, 'BtnShowDetail_Click')
        need(len(calls(detail, 'EntryOper.ShowEntrySource')) == 1
             and 'CmbYearPreviews' not in detail['syntax_text'] and 'MainClass.connstr' not in detail['syntax_text'],
             'detail-forwards-tag-without-database-context:' + rel)
    need(has(STMT, 'CmbYearPreviews_SelectionChanged', 'SelectedIndex >= 0', 'MainClass.ReturnYearPreviews = true;')
         and has(BAL, 'CmbYearPreviews_SelectionChanged', 'SelectedIndex > 0', 'MainClass.ReturnYearPreviews = false;'),
         'main-and-detailed-year-selection-have-different-index-zero-policy')
    for rel, name, row in ((STMT, 'LoadYearPreviews', 'currentRow'), (BAL, 'LoadYearPreviewsList', 'currentYear')):
        need(has(rel, name, 'SELECT Dbname, DbAutoName FROM Year_Previews',
                 row + '["Dbname"] = MainClass.DataBaseName', row + '["DbAutoName"] = MainClass.Database',
                 'Rows.InsertAt(' + row + ', 0)', 'SelectedValuePath = "DbAutoName"'),
             'year-registry-label-key-and-inserted-current-row:' + rel)
    need(has(STMT, 'GetAccountStatement', 'new SqlConnection(_connection.ConnectionString)',
             'new SqlCommand("GetAccountStatement", conn)', 'adapter.Fill(dataTable)'),
         'main-statement-query-copies-window-connection-string')
    need(has(BAL, 'GetAccountMovements', 'SELECT Entry.GlobalID', 'Entry_sub.EntryGlobalID',
             'new SqlDataAdapter(sql, _connection)') and has(BAL, 'ShowAccountData', 'row["GlobalID"]')
         and has(BAL, 'CreateResultTable', 'dt.Columns.Add("DgvGenralNo", typeof(string))'),
         'detailed-statement-entry-key-is-global-not-visible-document-number')
    dispatcher = m(ENTRYOPER, 'ShowEntrySource')
    need(norm(dispatcher['parameters']) == '(stringglid)' and has(ENTRYOPER, 'ShowEntrySource',
             'using SqlConnection conn = MainClass.ConnObj()', 'Entry WHERE GlobalId = N\'{glid}\'',
             'int docNo = Convert.ToInt32(entryRow["id"])', 'EntryID={docNo} AND branch={branch}'),
         'entry-dispatcher-uses-current-global-database-and-loaded-entry-id-branch')
    need('if (entryTable.Rows.Count == 0)' in dispatcher['syntax_text'] and dispatcher['returns'],
         'dispatcher-empty-entry-returns-without-typed-load-outcome')
    for rel, names in ((SALE, ['InsertLinkedReturn', 'InsertLinkedFromQuotation', 'InsertLinkedCreditNote']),
                       (CONTRACT, ['btnInsertLinkedInv_Click'])):
        for name in names:
            f = m(rel, name)
            backup = assignments(f, 'MainClass.originalConnStr', 'MainClass.connstr')
            need(len(backup) == 1 and guarded(backup[0], 'MainClass.ReturnYearPreviews')
                 and len(assignments(f, 'MainClass.connstr')) == 1
                 and 'trusted_connection=true' in assignments(f, 'MainClass.connstr')[0]['right'],
                 'linked-switch-is-shared-backup-and-trusted-auth:' + name)
            call = calls(f, 'InvoiceOperContract.InsertFromInv' if rel == CONTRACT else 'InvoiceOper.InsertFromInv')
            clear, publish = calls(f, 'CLR'), assignments(f, 'Invoic.ISNew', 'true')
            need(len(call) == len(clear) == len(publish) == 1 and clear[0]['line'] < call[0]['line'] < publish[0]['line']
                 and not publish[0]['ancestors'] and not calls(f, 'CheckBeforeClear') and not f['finally_ranges'],
                 'linked-clear-before-void-child-and-unguarded-normal-tail:' + name)
            need(not assignments(f, 'MainClass.ReturnYearPreviews', 'false')
                 and not assignments(f, 'MainClass.connstr', 'MainClass.originalConnStr'),
                 'linked-caller-has-no-own-restore-tail:' + name)
    for rel in (IP, IPC):
        f = m(rel, 'InsertFromInv')
        binder = calls(f, 'InvoiceOperContract.BindingInvoice' if rel == IPC else 'InvoiceOper.BindingInvoice')
        need(f['return_type'] == 'void' and len(binder) == 1 and len(f['returns']) == 1
             and f['returns'][0]['line'] < binder[0]['line']
             and len(calls(f, 'frmInvoiceSrch2.ShowDialog')) == 1 and len(calls(f, 'frmInvoiceItems2.ShowDialog')) == 1,
             'void-linked-helper-has-pre-binding-cancel-return:' + rel)
    need(has(IP, 'InsertFromInv', 'frmInvoiceItems2.inv = Invo', 'if (frmInvoiceItems2.ISDone)', 'Invo = frmInvoiceItems2.inv'),
         'invoice-child-publishes-model-only-on-done-while-header-binding-is-earlier')
    need(has(IPC, 'InsertFromInv', 'frmInvoiceItems2.invcontract = Invo', 'if (!frmInvoiceItems2.ISDone)')
         and not assignments(m(IPC, 'InsertFromInv'), 'Invo', 'frmInvoiceItems2.invcontract'),
         'contract-helper-different-model-field-and-no-written-return-assignment')
    need(has(SALE, 'CLR', 'Invoic = new InvoiceDGV()', 'ResetInvoice()')
         and has(CONTRACT, 'CLR', 'Invoic = new Invoicecontract()', 'ResetInvoice()'),
         'parent-clear-replaces-model-not-a-read-only-preview')
    need(has(SALE, 'LoadInvNo', 'InvoiceOper.InvoiceNo(InvType, ProcType,', 'Invoic.InvCombinedId =')
         and has(IP, 'InvoiceNo', 'MainClass.ConnObj()', 'ISNULL(MAX(id), 0)', 'branch=', 'proc_type='),
         'new-local-number-depends-on-current-global-string-not-parent-connection')
    need(has(CONTRACT, 'GetInvoiceNo', 'MainClass.ConnObj()', 'FROM InvContratct', 'return prefixe;'),
         'contract-number-helper-is-separate-table-and-has-fallback')
    add, alladd = m(ITEMS, 'btnadd_Click'), m(ITEMS, 'btnAddall_Click')
    need(calls(add, 'InsertSelectedItems') and assignments(add, 'MainClass.connstr', 'MainClass.originalConnStr')
         and not assignments(add, 'MainClass.ReturnYearPreviews', 'false'),
         'selected-items-button-restores-string-without-clearing-flag')
    need(assignments(alladd, 'ISDone', 'true') and assignments(alladd, 'MainClass.connstr', 'MainClass.originalConnStr')
         and assignments(alladd, 'MainClass.ReturnYearPreviews', 'false') and calls(alladd, 'Close'),
         'all-items-button-has-distinct-restore-and-flag-tail')
    selected = m(ITEMS, 'InsertSelectedItems')
    need(has(ITEMS, 'InsertSelectedItems', 'selectedRows.Count == 0', 'ISDone = false;', 'return;', 'Close();')
         and selected['return_type'] == 'void' and len(selected['catches']) == 1,
         'selected-items-helper-can-return-empty-or-caught-before-success')
    close = m(ITEMS, 'CloseWithoutResult')
    need(assignments(close, 'ISDone', 'false') and not assignments(close, 'MainClass.connstr')
         and not assignments(close, 'MainClass.ReturnYearPreviews')
         and calls(m(ITEMS, 'btnClose_Click'), 'CloseWithoutResult')
         and calls(m(ITEMS, 'Window_KeyDown'), 'CloseWithoutResult'),
         'items-cancel-path-resets-local-result-without-session-restore')
    searchclose = m(SEARCH, 'btnClose_Click')
    need(assignments(searchclose, 'MainClass.ReturnYearPreviews', 'false')
         and assignments(searchclose, 'MainClass.connstr', 'MainClass.originalConnStr')
         and has(SEARCH, 'Window_KeyDown', 'Key.Escape) Close();')
         and not assignments(m(SEARCH, 'Window_KeyDown'), 'MainClass.connstr'),
         'search-close-button-is-not-escape-or-native-close-contract')
    need(has(SEARCH, 'dgvItems_MouseDoubleClick', 'ISDone = true;', 'InvGlobalID = row.InvGlobalID;', 'Hide();')
         and has(SEARCH, 'Window_KeyDown', 'InvGlobalID = row.InvGlobalID;', 'Close();'),
         'search-accept-passes-global-key-not-displayed-local-id')
    need(has(SEARCH, 'ctor:frmInvoiceSrch', '_conn = MainClass.ConnObj()')
         and has(ITEMS, 'ctor:frmInvoiceItems', '_conn = MainClass.ConnObj()')
         and 'readonly SqlConnection' in facts['text_ranges']['items-connection-field']['text']
         and has(ITEMS, 'LoadData', 'new SqlDataAdapter(query, _conn)')
         and has(SEARCH, 'LoadInvoices', 'new SqlDataAdapter(_loadQuery, _conn)'),
         'children-capture-connections-at-construction-not-retargeted-by-global-restore')
    need(has(CONTRACT, 'SetupButtonEvents', 'btnInsertLinkedInv.Click += btnInsertLinkedInv_Click')
         and has(CONTRACT, 'frmcontract_Load', 'SetupButtonEvents()'),
         'contract-button-is-wired-in-code-not-assumed-unwired-from-XAML')
    need(has(SALE, 'StripImportInv_Click', 'if (frm.isDone &&', 'Invoic.InvNote = "";', 'Invoic.ISNew = true;'),
         'existing-P7-160-import-tail-is-related-not-identical-entry-path')
    for key in ('year-registry-create', 'year-registry-if-absent'):
        text = facts['text_ranges'][key]['text']
        need(all(s in text for s in ('[Year_Previews]', '[Dbname]', '[DbAutoName]', '[IS_Deleted]')),
             'readable-year-registry-DDL-not-an-unavailable-SDK:' + key)
    for key in ('statement-entry-key-create-fragment', 'statement-entry-key-alter-fragment'):
        need('es.EntryGlobalID AS DgvGenralNo' in facts['text_ranges'][key]['text'], 'statement-source-key-alias:' + key)
    need(has(SETTINGS, 'InsertInto_YearPreviews', 'Delete from Year_Previews where Dbname=@Dbname',
             'insert into Year_Previews(Dbname,DbAutoName,Is_Deleted)', '@DbAutoName', 'dbAutoName')
         and has(SETTINGS, 'GridControl2_ButtonClick', 'InsertInto_YearPreviews(row.DbName, row.DbAutoName)'),
         'year-mapping-has-local-parameterized-writer-and-caller')
    for rel in XML_SELECTED:
        elements = facts['xml_elements'][rel]
        if rel in (SEARCH[:-3], ITEMS[:-3]):
            need('Closing' not in elements[0]['attributes'], 'selected-child-XAML-root-does-not-declare-restore-closing:' + rel)
        if rel in (STMT[:-3], BAL[:-3]):
            need(any(e['attributes'].get('Click') == 'BtnShowDetail_Click'
                     and e['attributes'].get('Tag') == '{Binding DgvGenralNo}' for e in elements),
                 'report-detail-XAML-tag-is-global-entry-key:' + rel)
    return errors


def read_errors(reads, facts, root: Path = ROOT):
    errors, covered, ids = [], {}, set()
    for row in reads.get('reads', []):
        if row['id'] in ids: errors.append('read:duplicate-id:' + row['id'])
        ids.add(row['id'])
        text = prior.text_range(base.decode((root / row['path']).read_bytes()), row['start'], row['end'])
        if base.sha(text.encode('utf8')) != row['decoded_range_utf8_sha256']: errors.append('read:range-identity:' + row['id'])
        covered.setdefault(row['path'], set()).update(range(row['start'], row['end'] + 1))
    selected = [(rel, name, f['start'], f['end']) for rel, fs in facts['methods'].items() for name, f in fs.items()]
    selected += [(r['path'], key, r['start'], r['end']) for key, r in facts['text_ranges'].items()]
    selected += [(rel, 'selected-XML-start', r['line'], r['line']) for rel, rs in facts['xml_elements'].items() for r in rs]
    for rel, name, a, b in selected:
        if not set(range(a, b + 1)) <= covered.get(rel, set()): errors.append('read:uncovered:' + rel + ':' + name)
    if any(reads.get(k) is not False for k in ('extraction_equals_reading', 'individual_read_timestamps_invented', 'independent_human_review_claimed')):
        errors.append('read:no-extraction-or-invented-human-trace-as-read-proof')
    return errors


def preservation_errors(entry, root: Path = ROOT):
    errors = []
    if entry.get('HEAD') != BASE_HEAD or len(entry.get('preserved_tracked_audit_inputs', {})) != 1434:
        errors.append('preservation:R6-clean-entry')
    for rel, expected in entry.get('preserved_tracked_audit_inputs', {}).items():
        raw = (root / rel).read_bytes()
        same = {'bytes': len(raw), 'sha256': base.sha(raw)} == expected
        if not same and rel in prior.MUTABLE_INDEXES:
            # Allow ONLY a new index prefix, preserving every original suffix byte.
            suffix = raw[-expected['bytes']:]
            same = len(raw) > expected['bytes'] and base.sha(suffix) == expected['sha256']
        if not same: errors.append('preservation:entry-input:' + rel)
    for row in base.rows('inventory.csv'):
        raw = (root / row['path']).read_bytes()
        if len(raw) != int(row['bytes']) or base.sha(raw) != row['sha256']:
            errors.append('preservation:application:' + row['path'])
    return errors


def evidence_errors(ev: Path = EV):
    facts, review, work, roots = [load(n, ev) for n in (FACTS, REVIEW, WORK, ROOTS)]
    errors = []
    def need(ok, label):
        if not ok: errors.append('evidence:' + label)
    old = load(OLD_WORK)
    keys = ('path', 'line', 'left', 'containing_member', 'context_start', 'context_end')
    oldrows = sorted(({k: row[k] for k in keys} for row in old['writes']), key=lambda r: (r['path'], r['line'], r['left']))
    need(facts.get('literal_qualified_writes_in_R5_eight_owners') == oldrows, 'same27-literal-writes-not-an-expanded-or-alias-census')
    records = work.get('individual_write_dispositions', [])
    need(len(records) == len(oldrows) and len(oldrows) == 27, 'all27-original-write-identities')
    for source, row in zip(oldrows, records):
        need(row.get('original_R5_write_identity') == source, 'exact-old-write-row-not-count-only')
        f = facts['methods'].get(source['path'], {}).get(source['containing_member'], {})
        need(row.get('current_method_sha256') == f.get('syntax_utf8_sha256')
             and row.get('whole_containing_context_read_in_R6') is True
             and row.get('source_disposition_id') in {r.get('id') for r in review.get('source_decisions', [])},
             'write-bound-to-current-full-body-and-decision:' + source['path'] + ':' + str(source['line']))
    pending = sorted({(r['path'], r['containing_member'], r['context_start'], r['context_end']) for r in old['writes'] if not r['whole_context_read_in_R5']})
    need(work.get('twelve_original_pending_bodies') == [list(x) for x in pending] and len(pending) == 12,
         'twelve-individually-carried-body-obligations')
    need(work.get('original_R5_writes_or_read_chronology_rewritten') is False
         and work.get('repository_alias_assignment_census_completed') is False
         and work.get('whole_D17_complete') is False, 'bounded-worklist-not-whole-capability')
    decisions = review.get('source_decisions', [])
    need({r.get('id') for r in decisions} == {'R6D-BOOTSTRAP', 'R6D-REPORT-YEAR', 'R6D-LINKED-PARENT',
          'R6D-SEARCH-EXIT', 'R6D-ITEMS-EXIT', 'R6D-ENTRY-DISPATCH', 'R6D-YEAR-REGISTRY'}, 'individual-source-decision-identities')
    outcomes = review.get('path_outcomes', [])
    expected_outcomes = {'REPORT-NORMAL', 'REPORT-NO-ACCOUNT', 'REPORT-CAUGHT', 'REPORT-ESCAPED',
        'SEARCH-BUTTON-CANCEL', 'SEARCH-ESCAPE', 'SEARCH-ACCEPT', 'ITEMS-NONE', 'ITEMS-SOME',
        'ITEMS-ALL', 'ITEMS-CANCEL', 'LINKED-HELPER-RETURN', 'ENTRY-EMPTY'}
    need(len(outcomes) == len(expected_outcomes) and {r.get('id') for r in outcomes} == expected_outcomes,
         'thirteen-distinct-source-paths-not-runtime-scenarios')
    for row in decisions + outcomes:
        need(bool(row.get('source_basis')) and bool(row.get('source_disposition')) and bool(row.get('limit'))
             and row.get('observed_in_ERP') is False and row.get('is_capability_exit') is False,
             'qualified-source-decision:' + row.get('id', '?'))
    caps = {r['id']: r for r in base.rows('capability-register-07B38.csv')}
    need(set(review.get('capabilities', {})) == set(TARGETS), 'four-bounded-capabilities-not-all26-new-reviews')
    for cid, row in review.get('capabilities', {}).items():
        need(row.get('canonical_capability_row') == caps.get(cid)
             and row.get('whole_capability_certified') is False and row.get('local_semantic_obligations_complete') is False
             and row.get('readable_local_externalized') is False and bool(row.get('remaining_readable_local')),
             'canonical-capability-and-local-remainder:' + cid)
    actual = base.rows('findings.csv', AUDIT) + base.rows('findings-additions-07B39R1.csv')
    need(roots.get('available_prior_rows') == actual and len(actual) == 339, 'exact339-available-prior-dictionaries')
    by_id = {r['id']: r for r in actual}
    need(set(roots.get('focused_root_reviews', {})) == set(FOCUSED), 'focused-root-identity-set')
    for key, row in roots.get('focused_root_reviews', {}).items():
        need(row.get('canonical_prior_row') == by_id.get(key) and bool(row.get('reason')), 'canonical-prior-root:' + key)
    candidate_rows = roots.get('candidate_dispositions', [])
    candidates = {r.get('id'): r for r in candidate_rows}
    need(len(candidate_rows) == 5 and set(candidates) == {'R6C-REPORT-YEAR', 'R6C-LINKED-CANCEL',
         'R6C-YEAR-PROVENANCE', 'R6C-RESTORE-PATH', 'R6C-CONTRACT-RESULT'}, 'five-exact-bounded-candidate-identities')
    need(candidates.get('R6C-REPORT-YEAR', {}).get('root_id') == 'P7-115', 'existing-year-root-not-duplicated')
    need(candidates.get('R6C-LINKED-CANCEL', {}).get('root_id') == 'P7-160', 'same-parent-modal-result-root-extension')
    for key in ('R6C-YEAR-PROVENANCE', 'R6C-RESTORE-PATH', 'R6C-CONTRACT-RESULT'):
        r = candidates.get(key, {})
        need(r.get('root_id') is None and r.get('novelty_certified') is False
             and r.get('observed_financial_or_provider_failure') is False and bool(r.get('remaining_local')),
             'source-question-not-numbered-runtime-result:' + key)
    need(roots.get('new_finding_ids') == [] and roots.get('historical_root_fields_rewritten') is False
         and roots.get('all345_roots_screened') is False and roots.get('all339_semantically_reread_in_R6') is False
         and roots.get('missing_six_dictionaries_reconstructed') is False, 'no-missing-history-reconstruction-or-promotion')
    for name, obj in ((REVIEW, review), (WORK, work), (ROOTS, roots)):
        need(obj.get('assessment_reference_date_utc') == DATE and obj.get('raw_clocks_are_calendar_authority') is False,
             'session-reference-not-calendar-certification:' + name)
        need(obj.get('application_execution_count') == 0 and obj.get('whole_7B_static_assessment_complete') is False
             and obj.get('phase7C_started') is False and obj.get('phase8_authorized') is False
             and obj.get('prior196_tests_recertified') is False and obj.get('R2_R3_files_recovered') is False,
             'static-scope-and-missing-artifacts:' + name)
        need(obj.get('new_accepted_external_handoffs') == 0 and bool(obj.get('pinned_inputs')),
             'no-local-work-externalized:' + name)
        for pin in obj.get('pinned_inputs', []):
            need(identity(pin['path']) == pin, 'changed-pinned-input:' + pin['path'])
    return errors


def verify(rederive=False, ev: Path = EV):
    facts = load(FACTS, ev)
    errors = []
    for rel, expected in facts['source_identity'].items():
        if identity(rel) != expected: errors.append('source-identity:' + rel)
    if rederive and derive() != facts: errors.append('fresh-source-rederivation-differs')
    errors += source_errors(facts) + read_errors(load(READS, ev), facts)
    errors += evidence_errors(ev) + preservation_errors(load(ENTRY, ev))
    return {'schema_version': 1, 'errors': errors,
        'selected_complete_method_contexts': sum(len(v) for v in facts['methods'].values()),
        'source_identities': len(facts['source_identity']),
        'original_pending_bodies_read': 12, 'original_literal_write_rows_disposed': 27,
        'capability_exit_certificates_issued': 0, 'four_family_exit_certificates_issued': 0,
        'whole_7B_static_assessment_complete': False, 'application_execution_count': 0,
        'phase7C_started': False, 'phase8_authorized': False,
        'limit': 'Syntax/identity/recorded-source-disposition guards only. Not actual reading, calendar, runtime, all routes, financial acceptance, missing196 recertification or whole-capability completion.'}


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
