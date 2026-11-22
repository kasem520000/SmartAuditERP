#!/usr/bin/env python3
"""R8 read-only source/evidence guards: LastProcess and linked invoice insertion.

These parse original C#/XAML and audit JSON, never compile/run ERP, SQL, WPF,
providers, devices, SDKs, reports or business arithmetic. A rejected mutation
invalidates an audit assertion, NOT a proposed application fix. Coverage/hashes
are not an actual-reading, calendar, WPF scheduling, DTO-alias, authorization,
financial, all-routes or capability/family exit certificate.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys
import xml.parsers.expat

import verify_entry_source as previous

base, legacy, prior = previous.base, previous.previous, previous.prior
ROOT, AUDIT, EV, P, C = previous.ROOT, previous.AUDIT, previous.EV, previous.P, previous.C
load, identity, norm = previous.load, previous.identity, previous.norm
method, calls, assignments, guarded = previous.method, previous.calls, previous.assignments, previous.guarded
source_methods = previous.source_methods
# User-requested prospective assessment label, not a wall-clock/today assertion.
# The session date remains 2026-11-16; preserve the R8 entry's old label verbatim.
TAG, DATE = '07B39R8', '2026-11-21'
SESSION_DATE = '2026-11-16'
DATE_NOTE = 'reference-date-provenance-' + TAG + '.json'
BASE_HEAD = 'b642fe80dfb4bca3a6b218faf82d07ec42dd3d8c'
ENTRY = 'entry-identities-' + TAG + '.json'
FACTS = 'linked-activity-source-facts-' + TAG + '.json'
READS = 'linked-activity-source-review-log-' + TAG + '.json'
MATRIX = 'linked-activity-call-matrix-' + TAG + '.json'
REVIEW = 'linked-activity-dispositions-' + TAG + '.json'
ROOTS = 'linked-activity-root-adjudication-' + TAG + '.json'
WORK = 'linked-activity-local-worklist-' + TAG + '.json'
OLD_WORK = previous.OLD_WORK
PACKET = (ENTRY, DATE_NOTE, FACTS, READS, MATRIX, ROOTS, WORK, REVIEW)
MC, IP, IPC, LD = [C + s + '.cs' for s in ('MainClass', 'InvoiceOper', 'InvoiceOperContract', 'LoadData')]
IO, POS, PURCH, SALE, OLDIO, TRANS, OLDPURCH, OLDSALE, SALES, CONTRACT, DET, SEARCH, ITEMS = [
    P + s + '.xaml.cs' for s in ('frmInvInputOutput', 'frmInvPOS', 'frmInvPurch', 'frmInvSale',
    'frmInvInOutput', 'frmInventoryTransfer', 'frmPurchInv', 'frmSalePurch', 'frmSalesInvoice',
    'frmcontract', 'frmRptItemsActivityDetailed', 'frmInvoiceSrch', 'frmInvoiceItems')]
TARGETS = ('CAP7B38-D08', 'CAP7B38-D17', 'CAP7B38-D19', 'CAP7B38-D21', 'CAP7B38-D22', 'CAP7B38-D25')
DECISIONS = {'R8D-LAST-INPUTS', 'R8D-LAST-FILTERS', 'R8D-LAST-ORDER', 'R8D-REOPEN',
    'R8D-SCOPE', 'R8D-LINKED-CANCEL', 'R8D-LINKED-GUARD', 'R8D-LINKED-HEALTH',
    'R8D-CONTRACT-TARGET', 'R8D-LINE-IDENTITY', 'R8D-SEARCH-ELIGIBILITY'}
FOCUSED = ('P1-012', 'P7-059', 'P7-060', 'P7-061', 'P7-120', 'P7-121', 'P7-122',
    'P7-129', 'P7-130', 'P7-132', 'P7-144', 'P7-149', 'P7-150', 'P7-155', 'P7-156',
    'P7-157', 'P7-158', 'P7-159', 'P7-160', 'P7-161')
CANDIDATES = {
    'R8C-STORE': 'P7-122', 'R8C-EARLIEST': 'P7-059', 'R8C-PARTY-TYPE': 'P7-129',
    'R8C-LEGACY-PARTY': 'P7-130', 'R8C-REOPEN-IDENTITY': 'P7-061',
    'R8C-LIFECYCLE': 'P7-132', 'R8C-LINKED-CANCEL': 'P7-160',
    'R8C-PURCHASE-STAY': None, 'R8C-LINKED-HEALTH': 'P7-161',
    'R8C-PERMISSION': 'P1-012', 'R8C-CONTRACT-LINES': None, 'R8C-LINE-IDENTITY': None,
    'R8C-YEAR-REQUEST': None, 'R8C-YEAR-RESTORE': None,
}
CONTEXTS = {
    MC: ['ConnObj', 'DoApplyUserSett@System.Windows.Window', 'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions'],
    LD: ['Customers'], IP: ['InsertFromInv', 'BindingInvoice', 'InvoiceNo', 'OrderNo'],
    IPC: ['InsertFromInv', 'BindingInvoice'],
    IO: ['ctor:frmInvInputOutput', 'Window_Loaded', 'LoadData1', 'LoadCustomers', 'ResetInvoice',
         'RefreshGrid', 'BindingControls', 'Navigate', 'CLR', 'LoadInvNo', 'btnNew_Click',
         'CheckBeforeClear', 'cmbClient_SelectionChanged', 'GridControl1_SelectionChanged',
         'CtxItemLastActivity_Click', 'CtxClientActivity_Click', 'btnInsertLinkedInv_Click'],
    POS: ['ctor:frmInvPOS', 'BindingDGV', 'ResetInvoice', 'CLR', 'LoadInvNo', 'GridControl1_SelectionChanged',
          'CtxItemLastActivity_Click', 'CtxClientActivity_Click', 'RetSales_Click', 'InsertFromInv', 'btnPostPon_Click'],
    PURCH: ['ctor:frmInvPurch', 'BindingDGV', 'ResetInvoice', 'CLR', 'LoadCustomers', 'LoadInvNo',
            'btnNew_Click', 'CheckBeforeClear', 'GetSelectedId', 'MenuItemLastActivity_Click',
            'MenuClientActivity_Click', 'ItemLastActivity', 'ItemClientActivity',
            'btnInsertLinkedInv_Click', 'PrepareReturnInvoice'],
    SALE: ['ctor:frmInvSale', 'BindingDGV', 'ResetInvoice', 'CLR', 'LoadCustomers', 'LoadInvNo',
           'btnInsertLinkedInv_Click', 'btnNew_Click', 'CheckBeforeClear', 'GetSelectedValue',
           'MenuItemLastActivity_Click', 'MenuClientActivity_Click', 'ItemLastActivity',
           'ItemClientActivity', 'InsertLinkedReturn', 'InsertLinkedFromQuotation', 'InsertLinkedCreditNote'],
    OLDIO: ['ctor:frmInvInOutput', 'SearchByID', 'ReadData', 'GetSelectedStoreId', 'LoadItemInf',
            'LoadCustomers', 'ToInt', 'dgvItems_SelectionChanged', 'StripClientLastItem_Click', 'StripLastItem_Click'],
    TRANS: ['ctor:frmInventoryTransfer', 'Window_Loaded', 'Navigate', 'ResetInvoice', 'CLR', 'BindingDGV',
            'GC1_GetFocused', 'SafeInt', 'SetupContextMenu', 'MkMenu', 'ItemLastActivity'],
    OLDPURCH: ['ctor:frmPurchInv', 'SearchByID', 'ReadData', 'addNewItem', 'ReadBarcode', 'btnAddRow_Click',
               'FillRowFromDt', 'LoadItemInf', 'SetRowCellValue', 'LoadCustomers', 'GetRowAt', 'GetRowCellValue',
               'GetFocusedRowIndex', 'GridControl1_SelectionChanged', 'StripItemLastActivity_Click', 'StripClientLastActivity_Click'],
    OLDSALE: ['Window_Loaded', 'SearchByID', 'AddNewItem', 'ReadBarcode', 'LoadInvSubItems', 'StripItemSearch_Click',
              'stripImport_Click', 'GetStoreId', 'LoadItemInf', 'SearchByCode', 'LoadCustomers',
              'dgvItems_SelectionChanged', 'StripClientLastItem_Click', 'StripLastItem_Click'],
    SALES: ['ctor:frmSalesInvoice', 'ReadData', 'SearchByID', 'stripImport_Click', 'LoadItemInf', 'SearchByCode',
            'LoadCustomers', 'dgvItems_SelectionChanged', 'StripClientLastItem_Click', 'StripLastItem_Click'],
    CONTRACT: ['ctor:frmcontract', 'frmcontract_Load', 'SetupGridEvents', 'SetupButtonEvents', 'SetupComboBoxEvents',
               'CLR', 'ResetInvoice', 'BindingDGV', 'LoadCustomers', 'LoadInvNo', 'GetInvoiceNo',
               'SafeGetSelectedValue', 'GetGridCellInt', 'GridView1_ShowGridMenu', 'AddMenuItem',
               'ItemLastActivity', 'ItemClientActivity', 'btnInsertLinkedInv_Click', 'CheckBeforeClear'],
    DET: ['ctor:frmRptItemsActivityDetailed', 'Window_Loaded', 'LoadSafes', 'LoadBranches', 'LoadPrintSettings',
          'loadclients', 'GetsafeName', 'LastProcess', 'ShowResult', 'BuildProcTypeCondition',
          'chkAll_CheckedChanged', 'chkAllBranches_CheckedChanged', 'chkAllProcType_CheckedChanged',
          'chkAllClients_CheckedChanged', 'chkClients_CheckedChanged', 'chkSuplier_CheckedChanged',
          'ChekAllItems_CheckedChanged', 'ckTotalPeriod_CheckedChanged', 'cbLastProcess_CheckedChanged',
          'cmbProcType_SelectionChanged', 'btnDgvSettings_Click', 'MenuItemSaveSetting_Click',
          'MenuItemDefualtSetting_Click', 'btnOpenInvoice_Click', 'OpenInvoiceByType', 'OpenForm', 'OpenWindow'],
    SEARCH: ['ctor:frmInvoiceSrch', 'Window_Loaded', 'Window_KeyDown', 'btnClose_Click',
             'cmbProcType_SelectionChanged', 'txtFromDate_SelectedDateChanged', 'txtToDate_SelectedDateChanged',
             'btnClear_Click', 'dgvItems_SelectionChanged', 'dgvItems_MouseDoubleClick', 'BtnReturn_Click',
             'LoadInvoices', 'BuildLoadQuery', 'LoadProcessTypes', 'ApplyFilter', 'BuildFilterExpression',
             'RefreshDisplayRows', 'IsPreviousReturned', 'ApplyColumnVisibility'],
    ITEMS: ['ctor:frmInvoiceItems', 'Window_Loaded', 'Window_KeyDown', 'btnClose_Click', 'btnadd_Click',
            'btnAddall_Click', 'GridControl1_CellEditEnding', 'LoadData', 'BuildLoadQuery',
            'InsertSelectedItems', 'RemoveNonSelectedItems', 'CloseWithoutResult'],
}
XML_SELECTED = {}
for _rel in (IO, POS, PURCH, SALE, OLDIO, TRANS, OLDPURCH, OLDSALE, SALES, CONTRACT):
    XML_SELECTED[_rel[:-3]] = {'GridControl1', 'dgvItems', 'cmbClient', 'LookUpEdit1', 'CmbYearPreviews'}
for _r in load(OLD_WORK)['calls']:
    if _r['family'] != 'entry-source': XML_SELECTED[_r['path'][:-3]].add(_r['containing_selector'])
for _rel in (PURCH, SALE): XML_SELECTED[_rel[:-3]] |= {'MenuItemLastActivity_Click', 'MenuClientActivity_Click'}
XML_SELECTED[POS[:-3]].add('RetSales_Click')
XML_SELECTED[CONTRACT[:-3]] |= {'GridView1', 'btnInsertLinkedInv'}
XML_SELECTED[TRANS[:-3]].add('GridView1')
XML_SELECTED[SEARCH[:-3]] = {'dgvItems', 'ColReturnInv', 'Window_KeyDown', 'btnClose_Click', 'BtnReturn_Click',
    'dgvItems_MouseDoubleClick', 'dgvItems_SelectionChanged', 'cmbProcType'}
XML_SELECTED[ITEMS[:-3]] = {'GridControl1', 'btnadd', 'btnAddall', 'btnClose', 'Window_KeyDown', 'GridControl1_CellEditEnding'}
XML_SELECTED[DET[:-3]] = {'chkAll', 'chkAllBranches', 'ChekAllItems', 'ckTotalPeriod', 'cbLastProcess',
    'chkAllClients', 'chkClients', 'chkSuplier', 'cmbClients', 'chkAllProcType', 'cmbProcType', 'btnOpenInvoice_Click'}
TEXT_RANGES = {
    'mutable-session-fields': (MC, 25, 49), 'shared-year-flag': (MC, 122, 122),
    'transfer-focused-row-property': (TRANS, 63, 67),
    'legacy-local-item-row-class': (OLDIO, 2813, 3111),
    'purchase-local-string-row-class': (OLDPURCH, 2460, 2497),
    'sale-purchase-local-row-class': (OLDSALE, 2800, 2849),
    'sales-invoice-local-row-class': (SALES, 3050, 3101),
    'activity-result-row-class': ('SmartAuditERP/Class_WPF/ItemActivityRow_ActivityDetailed.cs', 1, 40),
    'search-public-result-fields': (SEARCH, 23, 31), 'search-row-identity-fields': (SEARCH, 674, 690),
    'items-public-input-fields': (ITEMS, 23, 33),
    'external-AuditorAPI-reference': ('SmartAuditERP/SmartAuditERP.csproj', 25, 32),
}


def original_calls():
    return [r for r in load(OLD_WORK)['calls'] if r['family'] != 'entry-source']


def selected_call_sites(text, rel):
    """Fresh syntax in the ten carried owner files, not compiler/alias/reflection closure.

    R6 ids are attached by owner/member/function occurrence order, NOT invented
    as new capabilities. Exact original row dictionaries are preserved separately.
    """
    parsed = base.Syntax(text)
    templates = defaultdict(list)
    for row in original_calls():
        if row['path'] == rel:
            templates[(row['containing_selector'], row['function_syntax'])].append(row)
    seen, result = defaultdict(int), []
    for n in base.walk(parsed.tree.root_node):
        if n.type != 'invocation_expression': continue
        function = parsed.text(n.child_by_field_name('function'))
        family = ('last-process' if function.rsplit('.', 1)[-1] == 'LastProcess' else
                  'linked-insert' if function in ('InvoiceOper.InsertFromInv', 'InvoiceOperContract.InsertFromInv') else None)
        if not family: continue
        owner = n.parent
        while owner and owner.type not in ('method_declaration', 'constructor_declaration'): owner = owner.parent
        if owner is None: raise ValueError('A selected call has no local containing method')
        selector = parsed.text(owner.child_by_field_name('name'))
        key = (selector, function); index = seen[key]; seen[key] += 1
        template = templates[key][index] if index < len(templates[key]) else None
        argnode = n.child_by_field_name('arguments'); args = parsed.text(argnode)
        variable = function.rsplit('.', 1)[0]
        owncalls = [x for x in base.walk(owner) if x.type == 'invocation_expression']
        def positions(member):
            return [x.start_point.row + 1 for x in owncalls
                    if parsed.text(x.child_by_field_name('function')) == variable + '.' + member]
        result.append({'original_call_id': template['id'] if template else None, 'family': family,
            'path': rel, 'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
            'function_syntax': function, 'argument_syntax': args,
            'arguments': [parsed.text(x) for x in argnode.named_children],
            'argument_utf8_sha256': base.sha(args.encode('utf8')), 'containing_selector': selector,
            'containing_context_start': owner.start_point.row + 1, 'containing_context_end': owner.end_point.row + 1,
            'containing_context_utf8_sha256': base.sha(parsed.text(owner).encode('utf8')),
            'ancestors': legacy.ancestors(parsed, n, owner),
            'same_owner_Show_lines': positions('Show') if family == 'last-process' else [],
            'same_owner_Activate_lines': positions('Activate') if family == 'last-process' else [],
            'compiler_bound_target': False})
    return result


def reopen_sites(text):
    parsed = base.Syntax(text); owner = legacy.selected_node(parsed, 'OpenInvoiceByType'); result = []
    for n in base.walk(owner):
        if n.type != 'invocation_expression' or not parsed.text(n.child_by_field_name('function')).endswith('.Navigate'): continue
        outer, section, current = None, None, n.parent
        while current and current != owner:
            if current.type == 'invocation_expression':
                f = parsed.text(current.child_by_field_name('function'))
                if f.startswith(('OpenForm<', 'OpenWindow<')): outer = f
            if current.type == 'switch_section': section = current
            current = current.parent
        if not outer or section is None: raise ValueError('Unclassified report reopen site')
        labels = [parsed.text(c) for c in section.named_children if c.type == 'constant_pattern']
        # The C# grammar emits adjacent, label-only switch_sections for aliases.
        # Keep their labels as well; counting Navigate nodes alone loses two cases.
        sibling = section.prev_named_sibling
        while sibling is not None and sibling.type == 'switch_section':
            if any(c.type not in ('constant_pattern', 'comment') for c in sibling.named_children): break
            labels = [parsed.text(c) for c in sibling.named_children if c.type == 'constant_pattern'] + labels
            sibling = sibling.prev_named_sibling
        result.append({'id': 'R8OPEN-' + str(len(result) + 1).zfill(2),
            'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
            'opener_function_syntax': outer, 'receiver_type_syntax': outer.split('<', 1)[1].rsplit('>', 1)[0],
            'case_label_syntax': labels, 'arguments_syntax': parsed.text(n.child_by_field_name('arguments')),
            'compiler_bound_target': False})
    return result


def xml_elements(text, needles):
    roots = []; parser = xml.parsers.expat.ParserCreate(namespace_separator='|')
    def first(name, attrs):
        if not roots: roots.append({'element': name.rsplit('|', 1)[-1], 'line': parser.CurrentLineNumber,
            'attributes': {k.rsplit('|', 1)[-1]: value for k, value in attrs.items()}})
    parser.StartElementHandler = first; parser.Parse(text.encode('utf8'), True)
    return roots + [e for e in legacy.xml_facts(text, needles) if e != roots[0]]


def derive(root: Path = ROOT):
    facts = {'schema_version': 1, 'kind': 'R8-bounded-source-syntax-not-runtime-or-reading-proof',
        'source_identity': {}, 'methods': {}, 'xml_elements': {}, 'text_ranges': {}, 'call_sites': [],
        'application_execution_count': 0, 'whole_7B_static_assessment_complete': False}
    for rel, sels in CONTEXTS.items():
        raw = (root / rel).read_bytes(); text = base.decode(raw)
        facts['source_identity'][rel] = identity(rel, root)
        facts['methods'][rel] = source_methods(text, sels)
    for rel in sorted({r['path'] for r in original_calls()}):
        facts['call_sites'] += selected_call_sites(base.decode((root / rel).read_bytes()), rel)
    for rel, needles in XML_SELECTED.items():
        facts['source_identity'][rel] = identity(rel, root)
        facts['xml_elements'][rel] = xml_elements(base.decode((root / rel).read_bytes()), needles)
    for key, (rel, a, b) in TEXT_RANGES.items():
        text = prior.prior.text_range(base.decode((root / rel).read_bytes()), a, b)
        facts['source_identity'][rel] = identity(rel, root)
        facts['text_ranges'][key] = {'path': rel, 'start': a, 'end': b, 'text': text,
            'decoded_range_utf8_sha256': base.sha(text.encode('utf8'))}
    facts['reopen_sites'] = reopen_sites(base.decode((root / DET).read_bytes()))
    return facts


def source_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('source:' + label)
    def m(rel, sel): return method(facts, rel, sel)
    def has(rel, sel, *snippets):
        code = norm(m(rel, sel)['syntax_text']); return all(norm(s) in code for s in snippets)
    def x(rel, name):
        return next((e['attributes'] for e in facts['xml_elements'][rel[:-3]] if e['attributes'].get('Name') == name), {})
    original = original_calls(); sites = facts['call_sites']; by_id = {s['original_call_id']: s for s in sites}
    need(len(sites) == len(original) == 30 and set(by_id) == {r['id'] for r in original}, 'same30-original-call-identities-not-alias-census')
    for old in original:
        s = by_id.get(old['id'], {}); f = m(old['path'], old['containing_selector'])
        need(s.get('path') == old['path'] and s.get('family') == old['family']
             and s.get('containing_selector') == old['containing_selector']
             and s.get('function_syntax') == old['function_syntax']
             and norm(s.get('argument_syntax', '')) == norm(old['argument_syntax']), 'exact-current-call-arguments:' + old['id'])
        need(s.get('containing_context_utf8_sha256') == f['syntax_utf8_sha256']
             and s.get('compiler_bound_target') is False, 'full-containing-context-and-lexical-limit:' + old['id'])
        if old['family'] == 'last-process':
            function = s.get('function_syntax', ''); variable = function.rsplit('.', 1)[0]
            show = calls(f, variable + '.Show'); requests = calls(f, function)
            need(len(show) == len(requests) == 1 and show[0]['line'] < requests[0]['line']
                 and calls(f, 'MainClass.ApplyPermissionToForm') and calls(f, 'MainClass.DoApplyUserSett'),
                 'written-show-before-four-int-request-not-WPF-schedule:' + old['id'])
    api = m(DET, 'LastProcess')
    need(api['return_type'] == 'void' and norm(api['parameters']) == '(intitemId,intstoreId,intclientId,intclientType)', 'LastProcess-four-ints-no-origin-or-result')
    need(has(DET, 'LastProcess', 'if (itemId > 0) SelectedId = itemId;', 'if (clientId > 0)',
             'if (clientType == 1)', 'chkClients.IsChecked = true;', 'else', 'chkSuplier.IsChecked = true;',
             'cmbClients.SelectedValue = clientId;', 'if (storeId > 0)', 'cmbSafes.SelectedValue = storeId;',
             'if (itemId > 0 || clientId > 0)', 'cbLastProcess.IsChecked = true;', 'ShowResult();'), 'positive-only-request-writes-and-trigger')
    need(not assignments(api, 'chkAll.IsChecked') and x(DET, 'chkAll').get('IsChecked') == 'True', 'store-request-does-not-clear-XAML-all-stores')
    result = m(DET, 'ShowResult')
    need(has(DET, 'ShowResult', 'chkAll.IsChecked != true &&', 'cmbSafes.SelectedValue != null', 'and Inv_sub.store={cmbSafes.SelectedValue}',
             'if (SelectedId != -1)', 'and Inv_Sub.ItemId={SelectedId}', 'chkAllClients.IsChecked != true &&',
             'cmbClients.SelectedIndex > -1 &&', 'cmbClients.SelectedValue != null', 'and Inv.cust_id={cmbClients.SelectedValue}'), 'filters-use-written-UI-guards-not-only-arguments')
    need(has(DET, 'ShowResult', 'if (cbLastProcess.IsChecked == true)', 'condTop = " top (1) ";',
             'else if (ckTotalPeriod.IsChecked != true)', 'ORDER BY inv.date ASC'), 'top1-is-ascending-and-last-mode-bypasses-date-predicate')
    need(has(DET, 'ShowResult', 'chkAllBranches.IsChecked != true &&', 'cmbBranches.SelectedIndex != -1 &&',
             'cmbBranches.SelectedValue != null', 'inv.branch={cmbBranches.SelectedValue} and ', 'ActivityList.Clear();',
             'new SqlDataAdapter(sql, conn)', 'Inv.InvGlobalID=Inv_Sub.InvGlobalID', 'AND Inv_Sub.proc_type IN(1,2)',
             'AND Inv.IS_Deleted=0', 'ActivityList.Add(item);') and result['return_type'] == 'void'
             and len(result['catches']) == 1 and not result['throws'], 'UI-branch-query-void-clear-and-caught-failure-not-typed-health')
    need(has(DET, 'ShowResult', 'if (typeDt.Rows.Count == 0) continue;', 'if (isInput == 0) continue;',
             'DgvInvType   = invTypeTxt', 'DgvInvNo     = row["id"]?.ToString() ?? ""',
             'typeDt.Rows[0]["NameEn"]', 'int procTypeSub = Convert.ToInt32(row["ProcTypeSub"]);',
             'string rightCond = invType == 7'), 'row-skips-and-display-key-not-full-document-ref')
    need(has(DET, 'ctor:frmRptItemsActivityDetailed', 'conn = MainClass.ConnObj();', 'conn1 = MainClass.ConnObj();', 'SelectedId = -1;')
             and has(DET, 'Window_Loaded', 'LoadSafes();', 'LoadBranches();', 'LoadPrintSettings();')
             and has(DET, 'LoadBranches', 'cmbBranches.SelectedValue = MainClass.BranchNo;'), 'receiver-fresh-global-capture-not-parent-or-year-provenance')
    need(has(MC, 'ConnObj', 'conn = new SqlConnection(connstr);', 'return conn;')
             and 'originalConnStr = connstr' in facts['text_ranges']['mutable-session-fields']['text'], 'global-factory-and-single-shared-backup')
    for sel, val in (('chkClients_CheckedChanged', '1'), ('chkSuplier_CheckedChanged', '2')):
        need(has(DET, sel, 'if (!IsLoaded) return;', f'loadclients({val});')
                 and has(DET, 'loadclients', 'WHERE (type={clientType} OR type=3)', 'cmbClients.SelectedIndex = -1;'), 'party-selector-load-guard:' + sel)
    need(has(LD, 'Customers', 'or type=3', 'and IS_Deleted=0')
             and has(IO, 'LoadCustomers', 'int type = 1;', 'if (InvType == 4 || InvType == 14)', 'type = 2;', 'LoadData.Customers(type)')
             and has(PURCH, 'LoadCustomers', 'int type = 2;', 'LoadData.Customers(type)')
             and has(OLDPURCH, 'LoadCustomers', 'int type = 2;', 'LoadData.Customers(type)')
             and has(OLDSALE, 'LoadCustomers', 'int custType = 2;', 'type={custType} or type=3')
             and has(POS, 'btnPostPon_Click', 'frm.Type = 1;', 'Invoic.Customer = frm.ClientId;'), 'actual-party-loaders-counterexample-not-every-caller-mismatch')
    need(has(IO, 'GridControl1_SelectionChanged', '_selectedItem = GridControl1.SelectedItem as InvoiceItem;')
             and has(IO, 'RefreshGrid', 'GridControl1.ItemsSource = _invoiceItems;')
             and has(OLDPURCH, 'GetRowAt', 'index >= 0 && index < _gridSource.Count', 'return null;')
             and has(OLDPURCH, 'GetRowCellValue', 'typeof(PurchInvRow).GetProperty(column)?.GetValue(row)')
             and has(OLDPURCH, 'GetFocusedRowIndex', 'GridControl1.SelectedItem is PurchInvRow row', '_gridSource.IndexOf(row)', 'return -1;'), 'selected-row-and-reflection-antecedents')
    need(has(OLDIO, 'ctor:frmInvInOutput', 'invoiceItems = new ObservableCollection<InvoiceItemRowModel>();',
             'dgvItems.ItemsSource = invoiceItems;')
             and has(OLDIO, 'SearchByID', 'ItemId = itemId,', 'StoreId = GetSelectedStoreId(),', 'invoiceItems.Add(row);')
             and has(OLDIO, 'ReadData', 'InvGlobalID=N', 'ItemId = itemId,', 'StoreId = storeId,', 'invoiceItems.Add(row);')
             and has(OLDIO, 'LoadItemInf', 'row.StoreId = currentStoreId;'), 'legacy-row-producers-local-typed-identities-not-unavailable-DTOs')
    need(has(OLDPURCH, 'ctor:frmPurchInv', '_gridSource = new ObservableCollection<PurchInvRow>();',
             'GridControl1.ItemsSource = _gridSource;')
             and has(OLDPURCH, 'FillRowFromDt', 'row.ItemIdDgv = dr["id"].ToString();')
             and has(OLDPURCH, 'LoadItemInf', 'row.StoreDgv = cmbStore.SelectedValue?.ToString() ?? "0";')
             and has(OLDPURCH, 'ReadData', 'select * from Inv_Sub where proc_id={ProcCode}',
                      'ItemIdDgv = itemId.ToString(),', 'StoreDgv = storeVal')
             and has(OLDPURCH, 'btnAddRow_Click', '_gridSource.Add(new PurchInvRow', 'GridControl1.SelectedIndex = RowIndex;'),
             'purchase-string-row-producers-plus-blank-selection-not-valid-request-proof')
    for rel, sel in ((OLDSALE, 'LoadInvSubItems'), (SALES, 'ReadData')):
        need(has(rel, sel, 'ItemId = itemId,', 'StoreId = storeId', '_itemsSource.Add(row);')
             and has(rel, 'LoadItemInf', 'StoreId =')
             and has(rel, 'stripImport_Click', 'SearchByCode();')
             and has(rel, 'SearchByCode', 'SearchByID(0);'), 'legacy-sale-id-store-producer-chain:' + rel)
    need(has(OLDSALE, 'GetStoreId', 'return 1;')
             and has(SALES, 'LoadItemInf', 'Convert.ToInt32(cmbStore.SelectedValue) : 0;'), 'legacy-store-fallbacks-one-versus-zero-not-uniform-sentinel')
    need(has(TRANS, 'SafeInt', 'if (v == null || v == DBNull.Value)', 'return d;', 'int.TryParse(v.ToString(), out int r) ? r : d')
             and has(TRANS, 'GC1_GetFocused', 'GridControl1.GetCellValue(GC1_FocusedRow, fieldName)')
             and has(CONTRACT, 'GetGridCellInt', 'value == null ? 0 : Convert.ToInt32(value)')
             and has(CONTRACT, 'SafeGetSelectedValue', 'catch { return default; }')
             and has(SALE, 'GetSelectedValue', 'catch { }', 'return default(T);'), 'conversion-fallbacks-differ-not-uniform-valid-selection')
    oldxml = facts['xml_elements'][OLDIO[:-3]]
    need(any(e['attributes'].get('Click') == 'StripLastItem_Click' and 'للعميل' in e['attributes'].get('Header', '') for e in oldxml)
             and any(e['attributes'].get('Click') == 'StripClientLastItem_Click' and 'للمادة' in e['attributes'].get('Header', '') for e in oldxml), 'legacy-menu-purpose-from-XAML-not-handler-name')
    need(has(CONTRACT, 'SetupGridEvents', 'tableView.ShowGridMenu += GridView1_ShowGridMenu;')
             and has(CONTRACT, 'AddMenuItem', 'item.Click += handler;')
             and has(TRANS, 'SetupContextMenu', 'MkMenu("📈 آخر حركة", ItemLastActivity)', 'GridControl1.ContextMenu = menu;')
             and has(TRANS, 'MkMenu', 'mi.Click += (s, e) => act();'), 'dynamic-menu-written-wiring-not-observed-reachability')
    reopened = facts['reopen_sites']
    expected_types = ['frmInvSale', 'frmInvSale', 'frmInvPurch', 'frmInvPurch', 'frmInvPOS', 'frmInvPOS',
        'frmInvPurch', 'frmInvInputOutput', 'frmInvInputOutput', 'frmProductionOrder', 'frmProductionOrder',
        'frmInventoryTransfer', 'frmInventoryTransfer', 'frmSafeAdjust']
    need(len(reopened) == 14 and [s['receiver_type_syntax'] for s in reopened] == expected_types, 'fourteen-literal-reopen-sites-not-fourteen-new-receiver-assessments')
    expected_labels = [['فاتورة مبيعات'], ['مرتجع مبيعات', 'مرتجع مبيعات '], ['فاتورة مشتريات'],
        ['مرتجع مشتريات'], ['نقطة بيع'], ['مرتجع نقطة بيع'], ['بضاعة أول مدة'], ['فاتورة الإدخال'],
        ['فاتورة الإخراج'], ['إنتاج'], ['مستهلك في الإنتاج'], ['مناقلة إلى'], ['مناقلة من'],
        ['تسوية جردية مدخلة', 'تسوية جردية مخرجة']]
    need([s['case_label_syntax'] for s in reopened] == [[json.dumps(t, ensure_ascii=False) for t in labels]
        for labels in expected_labels], 'all16-literal-case-labels-including-two-adjacent-label-only-sections')
    for s in reopened:
        need('id={invNo}' in s['arguments_syntax'] and 'branch' not in s['arguments_syntax'].lower()
             and 'InvGlobalID' not in s['arguments_syntax'] and s['compiler_bound_target'] is False,
             'local-number-and-missing-branch-origin-in-exact-reopen-query:' + s['id'])
    rowtext = facts['text_ranges']['activity-result-row-class']['text']
    need('public string DgvInvType' in rowtext and 'public string DgvInvNo' in rowtext
             and all(s not in rowtext for s in ('InvGlobalID', 'BranchId', 'DatabaseName')), 'local-result-class-does-not-invent-document-ref-fields')
    for sel in ('OpenForm', 'OpenWindow'):
        f = m(DET, sel); cfg = calls(f, 'configure'); shows = [c for c in f['calls'] if c['function'].endswith('.Show')]
        need(len(cfg) == len(shows) == 1 and cfg[0]['line'] < shows[0]['line'], 'configure-before-show-not-Loaded-order-proof:' + sel)
    need(has(DET, 'btnOpenInvoice_Click', 'btn.Tag is ItemActivityRow_ActivityDetailed item', 'OpenInvoiceByType(invType, invNoStr);')
             and any(e['attributes'].get('Click') == 'btnOpenInvoice_Click' and e['attributes'].get('Tag') == '{Binding}'
                     for e in facts['xml_elements'][DET[:-3]]), 'row-button-binds-row-not-sender-current-item-assumption')
    for rel, binder, dtype, table in ((IP, 'InvoiceOper.BindingInvoice', 'InvoiceDGV', 'Inv'),
                                      (IPC, 'InvoiceOperContract.BindingInvoice', 'Invoicecontract', 'InvContratct')):
        helper = m(rel, 'InsertFromInv'); picker = calls(helper, 'frmInvoiceSrch2.ShowDialog')
        bind = calls(helper, binder); items = calls(helper, 'frmInvoiceItems2.ShowDialog')
        need(helper['return_type'] == 'void' and norm(helper['parameters']) == f'(ref{dtype}Invo,intPtype)', 'void-ref-helper-signature:' + rel)
        need(has(rel, 'InsertFromInv', 'if (!(frmInvoiceSrch2.ISDone & (Operators.CompareString(frmInvoiceSrch2.InvGlobalID, "-1", TextCompare: false) != 0)))',
                 f"select * from {table} where IS_Deleted=0 and InvGlobalID=N'", 'frmInvoiceItems2.InvGlobalId = frmInvoiceSrch2.InvGlobalID;',
                 'frmInvoiceItems2.InvType = (int)Invo.InvoiceType;')
                 and len(picker) == len(bind) == len(items) == 1 and picker[0]['line'] < bind[0]['line'] < items[0]['line']
                 and not helper['finally_clauses'] and not helper['throws'], 'first-picker-guard-ref-load-before-second-acceptance:' + rel)
        binding = m(rel, 'BindingInvoice')
        need(binding['return_type'] == 'void' and len(assignments(binding, 'Invo', 'null')) == 2
                 and has(rel, 'BindingInvoice', 'Invo.InvGlobalID =', 'Invo.Branch =', 'Invo.InvoiceItems.Add(Itm);', 'MainClass.ConnObj()')
                 and not calls(binding, 'Invo.InvoiceItems.Clear') and not binding['throws'], 'binder-writes-current-ref-null-or-row-skips-not-detached-seed:' + rel)
        need(any(c['declaration'] == '(Exception projectError4)' and 'Invo = null' not in c['body'] for c in binding['catches']), 'per-row-catch-not-complete-health:' + rel)
    need(has(IP, 'InsertFromInv', 'frmInvoiceItems2.inv = Invo;', 'if (frmInvoiceItems2.ISDone)', 'Invo = frmInvoiceItems2.inv;')
             and has(IPC, 'InsertFromInv', 'frmInvoiceItems2.invcontract = Invo;', 'if (!frmInvoiceItems2.ISDone)')
             and not assignments(m(IPC, 'InsertFromInv'), 'Invo', 'frmInvoiceItems2.invcontract'), 'ordinary-conditional-rebind-versus-empty-contract-result-branch')
    need(has(ITEMS, 'ctor:frmInvoiceItems', 'inv = new InvoiceDGV();', 'invcontract = new Invoicecontract();', 'ISDone = false;')
             and has(ITEMS, 'InsertSelectedItems', 'foreach (var invoiceItem in inv.InvoiceItems)',
                     'if (invoiceItem.ItemId == selectedRow.Item_ID)', 'invoiceItem.ItemQuantity = selectedRow.ItemQty;',
                     'invoiceItem.ItemDiscount = selectedRow.ItemDiscount;', 'RemoveNonSelectedItems(selectedRows);', 'ISDone = true;')
             and 'invcontract' not in m(ITEMS, 'InsertSelectedItems')['syntax_text'], 'contract-query-does-not-redirect-selected-item-writer-target')
    need(has(ITEMS, 'RemoveNonSelectedItems', 'selectedRows.Select(r => r.Item_ID).ToHashSet()',
             '!selectedIds.Contains(i.ItemId)', 'inv.InvoiceItems.Remove(item)')
             and has(ITEMS, 'BuildLoadQuery', 'if (InvType == 23)', 'InvContratct_Sub', 'Inv_Sub.ProductId   = 0', 'RowQty')
             and x(ITEMS, 'GridControl1').get('SelectionMode') == 'Extended', 'selection-identity-is-ItemId-not-document-line-unit-or-row-ref')
    need(has(ITEMS, 'CloseWithoutResult', 'invcontract = new Invoicecontract();', 'inv = new InvoiceDGV();', 'ISDone = false;', 'Close();')
             and has(ITEMS, 'btnAddall_Click', 'ISDone = true;', 'MainClass.ReturnYearPreviews = false;', 'MainClass.connstr = MainClass.originalConnStr;')
             and has(ITEMS, 'btnadd_Click', 'InsertSelectedItems();', 'if (MainClass.ReturnYearPreviews)', 'MainClass.connstr = MainClass.originalConnStr;')
             and not assignments(m(ITEMS, 'btnadd_Click'), 'MainClass.ReturnYearPreviews'), 'different-item-exits-not-rollback-or-uniform-year-restoration')
    need(has(SEARCH, 'btnClose_Click', 'MainClass.ReturnYearPreviews = false;', 'MainClass.connstr = MainClass.originalConnStr;')
             and has(SEARCH, 'Window_KeyDown', 'else if (e.Key == Key.Escape) Close();')
             and not assignments(m(SEARCH, 'Window_KeyDown'), 'MainClass.connstr'), 'search-close-button-versus-escape-restoration-difference')
    for rel in (SEARCH, ITEMS):
        need('Closing' not in facts['xml_elements'][rel[:-3]][0]['attributes'], 'no-declared-child-XAML-closing-normalizer:' + rel)
    need(has(PURCH, 'btnInsertLinkedInv_Click', 'this.btnNew_Click(sender, e);')
             and has(PURCH, 'btnNew_Click', 'if (!this.CheckBeforeClear())', 'this.CLR();')
             and m(PURCH, 'btnNew_Click')['return_type'] == 'void'
             and has(PURCH, 'CheckBeforeClear', 'MessageBoxResult.No;')
             and len(m(PURCH, 'btnInsertLinkedInv_Click')['returns']) == 0, 'purchase-new-callee-No-is-not-propagated-to-linked-caller')
    need(has(IO, 'btnInsertLinkedInv_Click', 'if (ProcType == 2)', 'CLR();', 'Invoic.ISNew = true;', 'RefreshGrid();')
             and not calls(m(IO, 'btnInsertLinkedInv_Click'), 'CheckBeforeClear')
             and has(POS, 'RetSales_Click', 'CLR();', 'if (!pwdFrm.Iscorrect) return;', 'InsertFromInv(1);', 'linkedInvRet = true;')
             and calls(m(POS, 'RetSales_Click'), 'CLR')[0]['line'] < calls(m(POS, 'RetSales_Click'), 'pwdFrm.ShowDialog')[0]['line'], 'linked-parent-preclear-and-POS-password-sequence-not-outcome-gated')
    for rel, sel in ((POS, 'InsertFromInv'), (PURCH, 'PrepareReturnInvoice'),
                      (SALE, 'InsertLinkedReturn'), (SALE, 'InsertLinkedFromQuotation'),
                      (SALE, 'InsertLinkedCreditNote'), (CONTRACT, 'btnInsertLinkedInv_Click')):
        new_write = 'this.Invoic.ISNew = true;' if rel == PURCH else 'ISNew = true;'
        need('ISDone' not in m(rel, sel)['syntax_text'] and has(rel, sel, new_write),
             'parent-no-shared-helper-acceptance-result:' + rel + ':' + sel)
    for rel, sel in ((SALE, 'InsertLinkedReturn'), (SALE, 'InsertLinkedFromQuotation'),
                      (SALE, 'InsertLinkedCreditNote'), (CONTRACT, 'btnInsertLinkedInv_Click')):
        need(has(rel, sel, 'MainClass.originalConnStr = MainClass.connstr;', 'MainClass.ReturnYearPreviews',
                 'CmbYearPreviews.SelectedValue', 'MainClass.ConnObj()')
                 and not m(rel, sel)['finally_clauses'], 'linked-previous-year-switch-without-caller-finally:' + rel + ':' + sel)
    need(has(SEARCH, 'BuildLoadQuery', 'if (InvType != 14)', 'inv.branch = {MainClass.BranchNo}',
             'inv.proc_type = {ProcType}', '(inv_type = 20 OR inv_type = {InvType})', 'FROM   InvContratct inv')
             and has(SEARCH, 'BuildFilterExpression', 'conditions.Add($"proc_type = {procIndex}")')
             and has(SEARCH, 'cmbProcType_SelectionChanged', 'ApplyFilter();')
             and not calls(m(SEARCH, 'cmbProcType_SelectionChanged'), 'LoadInvoices'), 'selector-eligibility-keeps-existing155-and157-roots')
    need(has(MC, 'ApplyPermissionToForm@System.Windows.Window', 'if (dt.Rows.Count == 0) return;', 'ApplyWpfPermissions(')
             and has(MC, 'ApplyWpfPermissions', 'btn.IsEnabled = false;')
             and not m(MC, 'DoApplyUserSett@System.Windows.Window')['assignments'], 'generic-button-permissions-not-document-allowed-set-or-UI-filter-reset')
    for rel in (IO, TRANS):
        need(m(rel, 'Navigate')['return_type'] == 'void' and calls(m(rel, 'Navigate'), 'InvoiceOper.BindingInvoice')
                 and calls(m(rel, 'Window_Loaded'), 'ResetInvoice'), 'newly-read-reopen-core-not-typed-health-or-event-order:' + rel)
    return errors


def source_basis_errors(basis, facts):
    errors = []
    for row in basis:
        rel, sel = row.get('path'), row.get('selector')
        if sel:
            f = facts['methods'].get(rel, {}).get(sel, {})
            if any(row.get(k) != f.get(k) for k in ('start', 'end', 'syntax_utf8_sha256')):
                errors.append('basis:method:' + str(rel) + ':' + str(sel))
        else:
            known = facts['text_ranges'].get(row.get('text_range_key'), {})
            if any(row.get(k) != known.get(k) for k in ('path', 'start', 'end', 'decoded_range_utf8_sha256')):
                errors.append('basis:text-range:' + str(row.get('text_range_key')))
    return errors


def preservation_errors(entry, root: Path = ROOT):
    errors = []
    if entry.get('HEAD') != BASE_HEAD or entry.get('branch') != 'arena/94ae8414-smartauditerp' or len(entry.get('preserved_tracked_audit_inputs', {})) != 1538:
        errors.append('preservation:clean-published-R7-entry')
    for rel, expected in entry.get('preserved_tracked_audit_inputs', {}).items():
        raw = (root / rel).read_bytes(); same = {'bytes': len(raw), 'sha256': base.sha(raw)} == expected
        if not same and rel in prior.prior.MUTABLE_INDEXES:
            same = len(raw) > expected['bytes'] and base.sha(raw[-expected['bytes']:]) == expected['sha256']
        if not same: errors.append('preservation:prior-audit:' + rel)
    inventory = {r['path']: {'bytes': int(r['bytes']), 'sha256': r['sha256']} for r in base.rows('inventory.csv')}
    if entry.get('application_sources') != inventory or len(inventory) != 827: errors.append('preservation:entry-inventory')
    for rel, expected in inventory.items():
        raw = (root / rel).read_bytes()
        if {'bytes': len(raw), 'sha256': base.sha(raw)} != expected: errors.append('preservation:application:' + rel)
    for pin in entry.get('pinned_inputs', []):
        if identity(pin['path'], root) != pin: errors.append('preservation:entry-pin:' + pin['path'])
    return errors


def evidence_errors(ev: Path = EV):
    facts, matrix, review, roots, work = [load(n, ev) for n in (FACTS, MATRIX, REVIEW, ROOTS, WORK)]
    errors = []
    def need(ok, label):
        if not ok: errors.append('evidence:' + label)
    note = load(DATE_NOTE, ev)
    need(note.get('requested_prospective_assessment_label_utc') == DATE
         and note.get('session_reference_date_utc') == SESSION_DATE
         and note.get('entry_original_assessment_reference_date_utc') == load(ENTRY, ev).get('assessment_reference_date_utc') == SESSION_DATE
         and note.get('requested_label_is_claim_about_today') is False
         and note.get('frozen_R4_R7_or_R8_entry_dates_rewritten') is False
         and note.get('past_calendar_or_display_chronology_authenticated') is False,
         'prospective-reference-label-not-today-or-retroactive-calendar-proof')
    originals = original_calls(); sites = {s['original_call_id']: s for s in facts['call_sites']}
    for key, family, count in (('last_process_calls', 'last-process', 19), ('linked_insert_calls', 'linked-insert', 11)):
        old = [r for r in originals if r['family'] == family]; rows = matrix.get(key, [])
        need([r.get('original_R6_call_row') for r in rows] == old and len(rows) == count, 'exact-carried-original-rows:' + family)
        for row in rows:
            original = row['original_R6_call_row']; rid = original['id']; f = method(facts, original['path'], original['containing_selector'])
            need(row.get('current_source_site') == sites.get(rid)
                 and row.get('whole_containing_context_sha256') == f['syntax_utf8_sha256']
                 and row.get('whole_containing_body_read_in_R8') is True
                 and row.get('compiler_binding_or_runtime_reachability_certified') is False
                 and row.get('whole_route_or_capability_certified') is False
                 and row.get('accepted_external_handoff') is False
                 and bool(row.get('remaining_readable_local')) and bool(row.get('connection_year_disposition'))
                 and set(row.get('source_decision_ids', [])) <= DECISIONS and bool(row.get('source_decision_ids')),
                 'per-call-context-and-qualification:' + rid)
            errors += source_basis_errors(row.get('antecedent_source_basis', []), facts)
            need(bool(row.get('antecedent_source_basis')), 'argument-antecedents-not-only-call-spelling:' + rid)
            if family == 'last-process':
                need(set(row.get('source_to_argument_trace', {})) == {'item', 'store', 'party', 'party_type'}
                     and all(row['source_to_argument_trace'].values()) and bool(row.get('menu_intent_disposition'))
                     and bool(row.get('filter_disposition')) and bool(row.get('scope_allowed_set_disposition'))
                     and row.get('shared_receiver_contract_id') == 'R8-LAST-RECEIVER', 'individual-input-filter-scope:' + rid)
            else:
                need(set(row.get('path_dispositions', {})) == {'BeforeRequest', 'FirstPickerCancelled', 'SecondPickerCancelled', 'Accepted', 'EmptyOrFailedOrPartial'}
                     and all(row['path_dispositions'].values()) and bool(row.get('parent_publication_disposition'))
                     and row.get('explicit_typed_acceptance_result_returned') is False, 'individual-parent-cancel-accept-health:' + rid)
    receiver = matrix.get('shared_receiver_contract', {})
    need(receiver.get('id') == 'R8-LAST-RECEIVER'
         and receiver.get('method_sha256') == method(facts, DET, 'LastProcess')['syntax_utf8_sha256']
         and receiver.get('outcome_labels_are_audit_categories_not_CSharp_return_types') is True
         and set(receiver.get('source_outcomes', {})) == {'NoRequest', 'Requested', 'Empty', 'Failed', 'Partial', 'Denied'}, 'shared-void-outcome-contract-not-typed-success')
    need([r.get('source_site') for r in matrix.get('report_reopen_routes', [])] == facts['reopen_sites'], 'fourteen-query-site-identities-not-count-only')
    carried_core_facts = load('entry-source-source-facts-07B39R7.json')
    for row in matrix.get('report_reopen_routes', []):
        sid = row.get('source_site', {}).get('id', '?')
        need(bool(row.get('identity_scope_disposition')) and bool(row.get('core_receiver_evidence_disposition'))
             and row.get('whole_receiver_Save_allowed_edit_or_document_set_certified') is False,
             'qualified-reopen-route:' + sid)
        errors += source_basis_errors(row.get('freshly_read_R8_core_source_basis', []), facts)
        rel = P + row['source_site']['receiver_type_syntax'] + '.xaml.cs'
        expected_core = {s: {k: f[k] for k in ('start', 'end', 'syntax_utf8_sha256')}
            for s, f in carried_core_facts['methods'].get(rel, {}).items()
            if s.startswith('ctor:') or s == 'Navigate'}
        need(row.get('carried_R7_core_contexts') == expected_core, 'exact-carried-R7-core-not-fresh-R8-read:' + sid)
    decisions = review.get('source_decisions', [])
    need({r.get('id') for r in decisions} == DECISIONS and len(decisions) == len(DECISIONS), 'eleven-independent-source-decisions')
    for row in decisions:
        errors += source_basis_errors(row.get('source_basis', []), facts)
        need(bool(row.get('source_basis')) and bool(row.get('source_disposition')) and bool(row.get('counterevidence_and_limit'))
             and row.get('observed_in_ERP') is False and row.get('is_capability_exit') is False, 'qualified-decision:' + row.get('id', '?'))
    caps = {r['id']: r for r in base.rows('capability-register-07B38.csv')}
    need(set(review.get('capabilities', {})) == set(TARGETS), 'six-bounded-capabilities-not26-semantic-reviews')
    for cid, row in review.get('capabilities', {}).items():
        need(row.get('canonical_capability_row') == caps.get(cid)
             and row.get('whole_capability_certified') is False and row.get('local_semantic_obligations_complete') is False
             and row.get('readable_local_externalized') is False and bool(row.get('remaining_readable_local')),
             'named-capability-open-obligations:' + cid)
    actual = base.rows('findings.csv', AUDIT) + base.rows('findings-additions-07B39R1.csv'); canon = {r['id']: r for r in actual}
    need(roots.get('available_prior_rows') == actual and len(actual) == 339, 'all339-available-dictionaries-preserved-not-new-read-claim')
    focused = roots.get('focused_root_reviews', {})
    need(set(focused) == set(FOCUSED), 'twenty-focused-comparisons-not-all339-reread')
    for rid, row in focused.items():
        need(row.get('canonical_prior_row') == canon.get(rid) and bool(row.get('reason')), 'canonical-root-unchanged:' + rid)
    candidates = roots.get('candidate_dispositions', [])
    need(len(candidates) == len(CANDIDATES) and {r.get('id'): r.get('root_id') for r in candidates} == CANDIDATES, 'fourteen-source-question-root-identities')
    for row in candidates:
        need(row.get('novelty_certified') is False and row.get('observed_financial_or_provider_failure') is False
             and row.get('accepted_external_handoff') is False and bool(row.get('remaining_local'))
             and bool(row.get('source_disposition')), 'qualified-candidate:' + row.get('id', '?'))
    life = next((r for r in candidates if r['id'] == 'R8C-LIFECYCLE'), {})
    need(life.get('prior_certainty_preserved') == 'potential', '132-not-promoted-by-source-order')
    need(roots.get('new_finding_ids') == [] and roots.get('historical_root_fields_rewritten') is False
         and roots.get('all345_roots_screened') is False and roots.get('all339_semantically_reread_in_R8') is False
         and roots.get('missing_six_dictionaries_reconstructed') is False, 'no-invented-root-novelty-or-missing-history')
    orig37 = load(OLD_WORK)['calls']
    need([r.get('original_R6_call_row') for r in work.get('original37_ancestry', [])] == orig37
         and work.get('original_R6_discovery_or_read_flags_rewritten') is False
         and work.get('repository_alias_reflection_or_all_D17_census_complete') is False
         and work.get('all_receiver_helpers_Save_allowed_edit_or_document_sets_complete') is False,
         'all37-ancestry-and-local-remainder-not-erased')
    pending = sorted({(r['path'], r['containing_selector'], r['containing_context_start'], r['containing_context_end'])
                      for r in originals if r['family'] == 'linked-insert' and not r['containing_context_selected_and_read_in_R6']})
    need(work.get('three_original_pending_linked_bodies') == [list(x) for x in pending] and len(pending) == 3, 'same-three-body-obligations-now-displayed-not-old-flags-rewritten')
    for row in work.get('remaining_readable_local_tasks', []):
        need(bool(row.get('id')) and bool(row.get('source_paths_or_prior_evidence')) and bool(row.get('next_action'))
             and row.get('externalized') is False, 'remaining-local-owner:' + row.get('id', '?'))
    need(len(work.get('remaining_readable_local_tasks', [])) >= 5, 'substantive-readable-local-work-still-open')
    for row in review.get('unavailable_contracts_not_accepted_as_handoffs', []):
        need(all(bool(row.get(k)) for k in ('source_basis', 'owner_role', 'required_redacted_input', 'absence_impact', 'next_action', 'static_disposition'))
             and row.get('accepted_external_handoff') is False and bool(row.get('readable_local_not_delegated')), 'owned-unavailable-contract-not-local-work-substitute')
        errors += source_basis_errors(row.get('source_basis', []), facts)
    for name in (DATE_NOTE, READS, MATRIX, REVIEW, ROOTS, WORK):
        obj = load(name, ev)
        need(obj.get('assessment_reference_date_utc') == DATE and obj.get('raw_clocks_are_calendar_authority') is False,
             'declared-reference-only-not-calendar-authentication:' + name)
        need(obj.get('application_execution_count') == 0 and obj.get('whole_7B_static_assessment_complete') is False
             and obj.get('phase7C_started') is False and obj.get('phase8_authorized') is False
             and obj.get('prior196_tests_recertified') is False and obj.get('R2_R3_files_recovered') is False
             and obj.get('new_accepted_external_handoffs') == 0, 'static-open-scope:' + name)
        need(bool(obj.get('pinned_inputs')), 'explicit-versioned-inputs:' + name)
        for pin in obj.get('pinned_inputs', []): need(identity(pin['path']) == pin, 'pinned-input-changed:' + pin['path'])
    return errors


def verify(rederive=False, ev: Path = EV):
    facts = load(FACTS, ev); errors = []
    for rel, pin in facts['source_identity'].items():
        if identity(rel) != pin: errors.append('source-identity:' + rel)
    if rederive and derive() != facts: errors.append('fresh-source-rederivation-differs')
    errors += source_errors(facts) + prior.read_errors(load(READS, ev), facts)
    errors += preservation_errors(load(ENTRY, ev)) + evidence_errors(ev)
    return {'schema_version': 1, 'errors': errors,
        'selected_complete_method_contexts': sum(len(fs) for fs in facts['methods'].values()),
        'source_identities': len(facts['source_identity']), 'original_LastProcess_calls': 19,
        'original_linked_insert_calls': 11, 'original_pending_linked_bodies_read': 3,
        'report_reopen_query_sites': len(facts['reopen_sites']), 'source_decisions': len(DECISIONS),
        'capability_exit_certificates_issued': 0, 'four_family_exit_certificates_issued': 0,
        'new_accepted_external_handoffs': 0, 'whole_7B_static_assessment_complete': False,
        'application_execution_count': 0, 'phase7C_started': False, 'phase8_authorized': False,
        'limit': 'Recorded source/evidence/coverage guards, not actual reading, calendar, WPF timing, DTO behavior, all Save/allowed-edit/document sets, runtime, financial or whole-capability acceptance.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true'); parser.add_argument('--rederive', action='store_true')
    parser.add_argument('--require-complete', action='store_true'); args = parser.parse_args(argv)
    try: result = verify(args.rederive)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({'errors': [f'{type(exc).__name__}: {exc}'], 'whole_7B_static_assessment_complete': False}, ensure_ascii=False)); return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 2 if args.require_complete else 0


if __name__ == '__main__':
    sys.exit(main())
