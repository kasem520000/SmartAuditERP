#!/usr/bin/env python3
"""R9 static Save/edit/source-publication assertions, never an ERP test.

Only Python parses supplied C#/XAML and audit evidence. No compilation, ERP,
SQL/provider/WPF, SDK, reports, devices or business arithmetic is executed.
Source mutations invalidate audit assertions; they are not proposed fixes.
Hashes, lexical calls and coverage do not authenticate reading, dates, a
runtime allowed-set, deployed grants, financial results or capability exits.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

import verify_linked_activity as previous

base, legacy = previous.base, previous.legacy
ROOT, AUDIT, EV, P, C = previous.ROOT, previous.AUDIT, previous.EV, previous.P, previous.C
load, identity, norm = previous.load, previous.identity, previous.norm
method, calls, assignments, guarded = previous.method, previous.calls, previous.assignments, previous.guarded
source_methods = previous.source_methods
TAG, DATE, SESSION_DATE = '07B39R9', '2026-11-16', '2026-11-16'
BASE_HEAD = '23fa5b9eacfd6578dbb77fa5e398b500a2fa5b26'
ENTRY = 'entry-identities-' + TAG + '.json'
DATE_NOTE = 'reference-date-provenance-' + TAG + '.json'
FACTS = 'save-edit-source-facts-' + TAG + '.json'
READS = 'save-edit-source-review-log-' + TAG + '.json'
DISPLAYS = 'save-edit-source-display-ranges-' + TAG + '.json'
MATRIX = 'save-edit-command-matrix-' + TAG + '.json'
REVIEW = 'save-edit-dispositions-' + TAG + '.json'
ROOTS = 'save-edit-root-adjudication-' + TAG + '.json'
WORK = 'save-edit-local-worklist-' + TAG + '.json'
RECOVERY = ('entry-recovery-identities-' + TAG + '.json', 'entry-recovery-receipt-' + TAG + '.json')
PACKET = (ENTRY, *RECOVERY, DATE_NOTE, FACTS, DISPLAYS, READS, MATRIX, ROOTS, WORK, REVIEW)
IO, POS, PURCH, SALE, CONTRACT, TRANS = previous.IO, previous.POS, previous.PURCH, previous.SALE, previous.CONTRACT, previous.TRANS
MC, IP, IPC = previous.MC, previous.IP, previous.IPC
COMMON, FP, STOCK, EO, SQ = [C + n + '.cs' for n in ('Common', 'FormPermission', 'Inventory', 'EntryOper', 'StoredQueries')]
EDITORS = (IO, POS, PURCH, SALE, CONTRACT, TRANS)
TARGETS = ('CAP7B38-D08', 'CAP7B38-D17', 'CAP7B38-D19', 'CAP7B38-D22', 'CAP7B38-D25')
FOCUSED = ('P1-012', 'P1-013', 'P2-006', 'P3-001', 'P3-002', 'P3-003', 'P3-025',
           'P4-014', 'P4-019', 'P4-020', 'P4-031', 'P5-030', 'P6-001', 'P6-007',
           'P7-031', 'P7-061', 'P7-132', 'P7-144', 'P7-135', 'P7-159', 'P7-160', 'P7-161', 'P7-162')
DECISIONS = {'R9D-PERIOD', 'R9D-PERMISSION', 'R9D-IO', 'R9D-PURCHASE',
    'R9D-POS', 'R9D-SALE', 'R9D-CONTRACT', 'R9D-TRANSFER', 'R9D-MAPPING',
    'R9D-ENTRY', 'R9D-STOCK', 'R9D-PUBLICATION', 'R9D-WRITER-SCOPE',
    'R9D-ALTERNATE-OPENERS', 'R9D-IMPORTS'}
CANDIDATES = {
    'R9C-PERIOD': 'P3-001', 'R9C-FAILOPEN': 'P1-012', 'R9C-COMMAND-AUTH': None,
    'R9C-PURCHASE-PARITY': 'P4-031', 'R9C-POS-DATE': 'P7-135',
    'R9C-SALE-DOUBLE-WIRING': 'P7-162', 'R9C-TRANSFER-OUTCOME': 'P4-019',
    'R9C-ENTRY-TRANSACTIONS': 'P3-003', 'R9C-ENTRY-INVARIANTS': 'P3-002',
    'R9C-TAX-COMMIT': 'P6-007', 'R9C-STOCK-CACHE': None,
    'R9C-MAPPING-RETRY': None, 'R9C-POS-TABLES': None,
    'R9C-QUOTATION-CLEAR': None, 'R9C-CONTRACT-PRINT': None,
    'R9C-NULL-ENTRY': None, 'R9C-CONTRACT-FALLBACK': None,
    'R9C-CLOUD-LOCAL-RESULT': None, 'R9C-CONTRACT-PARAMETERS': None,
    'R9C-ALTERNATE-CONTRACT': None, 'R9C-IMPORT-FIRST-MATCH': None,
    'R9C-UI-POLICY-IDENTITY': None,
}
# Selected whole bodies actually displayed in this continuation. Not all methods
# in these files, not the original R6 read flags, and not an alias/reflection census.
CONTEXTS = {'SmartAuditERP/Class/Common.cs': ['AllowEdit',
                                   'ApplyEditAddPermission',
                                   'ApplyEditAddPermissionInternal',
                                   'CheckProiedAcc',
                                   'CheckReffNo',
                                   'GetInventoryBranch'],
 'SmartAuditERP/Class/EntryOper.cs': ['SaveEnty'],
 'SmartAuditERP/Class/FormPermission.cs': ['ApplyFrmPermission@System.Windows.Window',
                                           'ApplyFrmPermission@object',
                                           'ApplyFrmPermissionInternal',
                                           'DisableButton',
                                           'GetBool',
                                           'GetTargetButtons',
                                           'IsSavePermissionButton',
                                           'LoadPermissionData',
                                           'ResolveFormName',
                                           'ctor:FormPermission'],
 'SmartAuditERP/Class/Inventory.cs': ['UpdateItemStock'],
 'SmartAuditERP/Class/InvoiceOper.cs': ['BindToEntry',
                                        'BindingCompositeItems',
                                        'GetInvoiceGlobalID',
                                        'InsertZatcaEncodedInvoice',
                                        'IsTaxCustomer',
                                        'MappingInvoice',
                                        'PayInvoice',
                                        'PayInvoiceWithoutShowPayFrm',
                                        'SaveInvoice',
                                        'SyncInvoice',
                                        'VerifyIsNewInvoice',
                                        'insertDocument',
                                        'isCreditCust'],
 'SmartAuditERP/Class/InvoiceOperContract.cs': ['BindToEntry',
                                                'BindingCompositeItems',
                                                'GetInvoiceGlobalIDcontract',
                                                'MappingInvoicecontract',
                                                'SaveInvoice',
                                                'SyncInvoice',
                                                'insertDocument'],
 'SmartAuditERP/Class/MainClass.cs': ['ApplyPermissionToForm@System.Windows.Window',
                                      'ApplyWpfPermissions',
                                      'ConnObj',
                                      'DoApplyUserSett@System.Windows.Window'],
 'SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs': ['BindingControls',
                                                      'ImportInventoryItems',
                                                      'LoadData1',
                                                      'Navigate',
                                                      'OnKeyDown',
                                                      'PayBill',
                                                      'SaveAndPrint',
                                                      'Window_Loaded',
                                                      'btnSavePrint_Click',
                                                      'btnSave_Click',
                                                      'ctor:frmInvInputOutput'],
 'SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs': ['BackgroundWorker1_DoWork',
                                              'BindingDGV',
                                              'CheckEditable',
                                              'ImportInventoryItems',
                                              'Insert_Table_Order',
                                              'PayBill',
                                              'RptPrint_Tables',
                                              'SaveAndPrint',
                                              'UpdateHoldButtons',
                                              'Update_Table_Order',
                                              'Window_KeyDown',
                                              'Window_Loaded',
                                              'btnHoldOrd_Click',
                                              'btnPay_Click',
                                              'ctor:frmInvPOS',
                                              'loadFonudtion',
                                              'updat_table'],
 'SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs': ['ImportInventoryItems',
                                                'Navigate',
                                                'SaveAndPrint',
                                                'SetPayAmounts',
                                                'btnSavePrint_Click',
                                                'btnSave_Click',
                                                'ctor:frmInvPurch',
                                                'frmInvInOut_KeyDown',
                                                'frmSalePurch_Load'],
 'SmartAuditERP/Form_WPF/frmInvSalContactDetails.xaml.cs': ['BtnShowInv_Click'],
 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs': ['ImportInventoryItems',
                                               'Navigate',
                                               'PayBill',
                                               'SaveAndPrint',
                                               'ValidateInvoice',
                                               'Window_KeyDown',
                                               'Window_Loaded',
                                               'btnRepaid_Click',
                                               'btnSavePrint_Click',
                                               'btnSaveQuotation_Click',
                                               'btnSave_Click',
                                               'ctor:frmInvSale',
                                               'loadFonudtion'],
 'SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs': ['Navigate',
                                                         'RecalculateCost',
                                                         'SaveAndPrint',
                                                         'SaveReceive',
                                                         'SaveSend',
                                                         'Window_KeyDown',
                                                         'Window_Loaded',
                                                         'btnSavePrint_Click',
                                                         'btnSave_Click',
                                                         'ctor:frmInventoryTransfer'],
 'SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs': ['OpenBeginningInventory',
                                                    'OpenInputOutput',
                                                    'OpenInventoryTransfer'],
 'SmartAuditERP/Form_WPF/frmSelectInv.xaml.cs': ['FindOpenedWindow',
                                                 'GenerateInvoice',
                                                 'ShowWindowAndCloseCurrent'],
 'SmartAuditERP/Form_WPF/frmcontract.xaml.cs': ['ConfigurePermissions',
                                                'LoadFoundation',
                                                'Navigate',
                                                'SaveAndPrint',
                                                'SetupButtonEvents',
                                                'SetupComboBoxEvents',
                                                'ValidateInvoice',
                                                'btnSavePrint_Click',
                                                'btnSave_Click',
                                                'ctor:frmcontract',
                                                'frmcontract_KeyDown',
                                                'frmcontract_Load'],
 'SmartAuditERP/Home.xaml.cs': ['BtnPurches_Click',
                                'BtnQutation_Click',
                                'BtnSales_Click',
                                'ToolStripNotficCreditPurch_Click',
                                'ToolStripNotficDeptPurch_Click',
                                'ToolstripNotficCreditSale_Click',
                                'ToolstripNotficDeptsal_Click',
                                'btnPOS2_Click',
                                'stripFirstStock_Click',
                                'stripInputInv_Click',
                                'stripInvertoryOrderInv_Click',
                                'stripOutputInv_Click',
                                'stripPOS_Click',
                                'stripPurchInv_Click',
                                'stripPurchReturn_Click',
                                'stripSaleInv_Click',
                                'stripSaleRetu_Click',
                                'stripShowPrice_Click',
                                'stripTransfer_Click',
                                'stripinvcontract_Click',
                                'stripinvcontractreturn_Click']}
XML_SELECTED = {rel[:-3]: {'btnSave', 'btnSavePrint', 'btnPay', 'btnHoldOrd',
    'btnSaveQuotation', 'btnRepaid'} for rel in EDITORS}
TEXT_RANGES = {
    'ordinary-header-and-line-SQL': (SQ, 6, 10),
    'entry-header-and-line-SQL': (SQ, 16, 20),
    'contract-header-and-line-SQL': (SQ, 46, 50),
    'external-AuditorAPI-reference': ('SmartAuditERP/SmartAuditERP.csproj', 25, 32),
}
QUERY_NAMES = ('InsertInv', 'UpdateInv', 'InsertInvSub', 'InsertEntry', 'UpdateEntry',
               'InsertEntrySub', 'InsertInvcontract', 'UpdateInvcontract', 'InsertInvSubcontract')
COMMAND_OWNERS = {
    IO: ('btnSave_Click', 'btnSavePrint_Click', 'PayBill', 'OnKeyDown'),
    POS: ('btnPay_Click', 'PayBill', 'btnHoldOrd_Click', 'Window_KeyDown'),
    PURCH: ('btnSave_Click', 'btnSavePrint_Click', 'frmInvInOut_KeyDown'),
    SALE: ('btnSave_Click', 'btnSavePrint_Click', 'PayBill', 'btnRepaid_Click', 'btnSaveQuotation_Click', 'Window_KeyDown'),
    CONTRACT: ('btnSave_Click', 'btnSavePrint_Click', 'frmcontract_KeyDown'),
    TRANS: ('btnSave_Click', 'btnSavePrint_Click', 'Window_KeyDown'),
}
OPENER_OWNERS = {'SmartAuditERP/Home.xaml.cs': ['stripTransfer_Click',
                                'stripFirstStock_Click',
                                'stripInputInv_Click',
                                'stripOutputInv_Click',
                                'stripInvertoryOrderInv_Click',
                                'stripPurchInv_Click',
                                'stripPurchReturn_Click',
                                'ToolStripNotficDeptPurch_Click',
                                'ToolStripNotficCreditPurch_Click',
                                'stripPOS_Click',
                                'btnPOS2_Click',
                                'stripSaleInv_Click',
                                'stripSaleRetu_Click',
                                'stripShowPrice_Click',
                                'ToolstripNotficCreditSale_Click',
                                'ToolstripNotficDeptsal_Click',
                                'stripinvcontract_Click',
                                'stripinvcontractreturn_Click',
                                'BtnSales_Click',
                                'BtnPurches_Click',
                                'BtnQutation_Click'],
 'SmartAuditERP/Form_WPF/frmSelectInv.xaml.cs': ['GenerateInvoice'],
 'SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs': ['OpenInventoryTransfer',
                                                    'OpenBeginningInventory',
                                                    'OpenInputOutput'],
 'SmartAuditERP/Form_WPF/frmInvSalContactDetails.xaml.cs': ['BtnShowInv_Click']}
SELECT, RPTINV, CONTACT = [P + n + '.xaml.cs' for n in ('frmSelectInv', 'frmRptInventory', 'frmInvSalContactDetails')]
HOME = 'SmartAuditERP/Home.xaml.cs'
EDITOR_TYPES = frozenset(Path(p).name.removesuffix('.xaml.cs') for p in EDITORS)
CALL_MEMBERS = frozenset(('SaveAndPrint', 'ValidateInvoice', 'PayBill', 'SaveSend',
    'SaveReceive', 'btnSave_Click', 'btnSavePrint_Click', 'btnPay_Click', 'btnHoldOrd_Click',
    'btnRepaid_Click', 'btnSaveQuotation_Click'))


def member_owner(parsed, node):
    owner = node.parent
    while owner and owner.type not in ('method_declaration', 'constructor_declaration'):
        owner = owner.parent
    return owner


def command_sites(text, rel):
    """All literal calls to the selected members in six files, not bound targets."""
    parsed = base.Syntax(text); out = []
    for n in base.walk(parsed.tree.root_node):
        if n.type != 'invocation_expression': continue
        function = parsed.text(n.child_by_field_name('function'))
        if function.rsplit('.', 1)[-1] not in CALL_MEMBERS: continue
        owner = member_owner(parsed, n)
        if owner is None: raise ValueError('Literal command has no containing member')
        name = parsed.text(owner.child_by_field_name('name'))
        selector = ('ctor:' if owner.type == 'constructor_declaration' else '') + name
        out.append({'path': rel, 'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
            'function_syntax': function, 'arguments_syntax': parsed.text(n.child_by_field_name('arguments')),
            'containing_selector': selector, 'containing_context_start': owner.start_point.row + 1,
            'containing_context_end': owner.end_point.row + 1,
            'containing_context_utf8_sha256': base.sha(parsed.text(owner).encode('utf8')),
            'ancestors': legacy.ancestors(parsed, n, owner), 'compiler_bound_target': False,
            'discovery_equals_body_read': False})
    return out


def permission_writes(text, rel):
    parsed = base.Syntax(text); result = []
    for n in base.walk(parsed.tree.root_node):
        if n.type != 'assignment_expression': continue
        left = parsed.text(n.child_by_field_name('left'))
        if norm(left).removeprefix('this.') not in ('allowEditInvoice', 'EnableE_Invoice'): continue
        owner = member_owner(parsed, n)
        if owner is None: raise ValueError('Flag write without selected body')
        selector = ('ctor:' if owner.type == 'constructor_declaration' else '') + parsed.text(owner.child_by_field_name('name'))
        result.append({'path': rel, 'line': n.start_point.row + 1, 'left': left,
            'right': parsed.text(n.child_by_field_name('right')), 'containing_selector': selector,
            'ancestors': legacy.ancestors(parsed, n, owner), 'compiler_bound_target': False})
    return result


def query_fields(text):
    """Decode these nine supplied ordinary C# string literals, never execute SQL."""
    parsed = base.Syntax(text); result = {}
    for n in base.walk(parsed.tree.root_node):
        if n.type != 'variable_declarator': continue
        name = parsed.text(n.child_by_field_name('name'))
        if name not in QUERY_NAMES: continue
        literals = [c for c in n.named_children if c.type == 'string_literal']
        if len(literals) != 1: raise ValueError('Expected one ordinary string literal for ' + name)
        literal = parsed.text(literals[0]); sql = json.loads(literal)
        result[name] = {'path': SQ, 'start': n.start_point.row + 1, 'end': n.end_point.row + 1,
            'csharp_literal': literal, 'sql_text': sql,
            'syntax_utf8_sha256': base.sha(parsed.text(n).encode('utf8')),
            'placeholder_names': sorted(set(re.findall(r'@\w+', sql))),
            'provider_binding_or_deployed_schema_verified': False}
    if set(result) != set(QUERY_NAMES): raise ValueError('Missing/duplicated supplied query declaration')
    return result


def header_parameter_bridges(facts):
    """Bounded lexical bridge for the ordinary/contract header insert+update pair.

    Preserve raw names, including supplied trailing spaces. A trimmed-name set
    comparison is a static counterexample to alleged missing four tax adds,
    not SqlClient binding, deployment, type/default or all-parameter health.
    """
    result = {}
    for rel, variable, names in ((IP, 'sqlCommand3', ('InsertInv', 'UpdateInv')),
                                  (IPC, 'sqlCommand4', ('InsertInvcontract', 'UpdateInvcontract'))):
        f = method(facts, rel, 'SaveInvoice')
        creates = [r for r in f['creations'] if r['type'] == 'SqlCommand'
                   and any(norm(r['arguments']).startswith('(StoredQueries.' + n + ',') for n in names)]
        if len(creates) != 2: raise ValueError('Expected two selected header alternatives in ' + rel)
        a = max(r['end'] for r in creates)
        execute = next(r for r in f['calls'] if r['line'] > a and r['function'] == variable + '.ExecuteNonQuery')
        adds = [r for r in f['calls'] if a < r['line'] < execute['line'] and r['function'] == variable + '.Parameters.Add']
        supplied = [json.loads(re.match(r'\("([^"]*)"', r['arguments'])[0][1:]) for r in adds]
        for name in names:
            required = facts['sql_fields'][name]['placeholder_names']
            result[name] = {'writer_path': rel, 'selector': 'SaveInvoice', 'command_variable_syntax': variable,
                'selected_header_creations': creates, 'first_header_execute': execute,
                'literal_add_calls': adds, 'raw_supplied_parameter_names': supplied,
                'whitespace_trimmed_missing_placeholders': sorted(set(required) - {p.strip() for p in supplied}),
                'provider_binding_or_all_parameter_health_certified': False}
    return result


def derive(root: Path = ROOT):
    facts = {'schema_version': 1, 'kind': 'R9-bounded-Save-edit-lexical-source-facts-not-runtime-or-reading-proof',
        'source_identity': {}, 'methods': {}, 'xml_elements': {}, 'text_ranges': {},
        'literal_command_sites': [], 'permission_flag_writes': [], 'sql_fields': {},
        'selected_alternate_editor_creations': [],
        'application_execution_count': 0, 'whole_7B_static_assessment_complete': False}
    for rel, sels in CONTEXTS.items():
        raw = (root / rel).read_bytes(); text = base.decode(raw)
        facts['source_identity'][rel] = identity(rel, root)
        facts['methods'][rel] = source_methods(text, sels)
        if rel in EDITORS:
            facts['literal_command_sites'] += command_sites(text, rel)
            facts['permission_flag_writes'] += permission_writes(text, rel)
    for rel, needles in XML_SELECTED.items():
        facts['source_identity'][rel] = identity(rel, root)
        facts['xml_elements'][rel] = previous.xml_elements(base.decode((root / rel).read_bytes()), needles)
    for key, (rel, a, b) in TEXT_RANGES.items():
        text = previous.prior.prior.text_range(base.decode((root / rel).read_bytes()), a, b)
        facts['source_identity'][rel] = identity(rel, root)
        facts['text_ranges'][key] = {'path': rel, 'start': a, 'end': b, 'text': text,
            'decoded_range_utf8_sha256': base.sha(text.encode('utf8'))}
    facts['sql_fields'] = query_fields(base.decode((root / SQ).read_bytes()))
    facts['header_parameter_bridges'] = header_parameter_bridges(facts)
    for rel, sels in OPENER_OWNERS.items():
        for sel in sels:
            for row in method(facts, rel, sel)['creations']:
                if row['type'] in EDITOR_TYPES:
                    facts['selected_alternate_editor_creations'].append({'path': rel, 'selector': sel,
                        'creation': row, 'compiler_bound_target': False, 'all_repository_ingress_certified': False})
    return facts


def source_errors(facts):
    errors = []
    def need(ok, label):
        if not ok: errors.append('source:' + label)
    def m(rel, sel): return method(facts, rel, sel)
    def has(rel, sel, *parts):
        text = norm(m(rel, sel)['syntax_text']); return all(norm(p) in text for p in parts)
    def c(rel, sel, name): return calls(m(rel, sel), name)
    def ordered(rel, sel, *names):
        groups = [c(rel, sel, n) for n in names]
        return all(groups) and [g[0]['line'] for g in groups] == sorted(g[0]['line'] for g in groups)
    def x(rel, name):
        return next((e['attributes'] for e in facts['xml_elements'][rel[:-3]] if e['attributes'].get('Name') == name), {})
    period = m(COMMON, 'CheckProiedAcc')
    need(period['return_type'] == 'bool' and has(COMMON, 'CheckProiedAcc',
        'return !(InvoiceDate > end || InvoiceDate < start) || true;', 'return true;')
        and all(norm(r['text']).endswith('true;') for r in period['returns']), 'period-helper-all-written-returns-allow')
    need(has(COMMON, 'AllowEdit', 'select ISNULL(IS_Edit,1) IS_Edit', 'dt.Rows.Count > 0', ': true;', 'catch', 'return true;')
         and norm(m(COMMON, 'AllowEdit')['parameters']) == '(stringfrmName)', 'allow-edit-missing-error-default-true-not-document-ACL')
    need(has(FP, 'ctor:FormPermission', 'Editable = true;', 'Addable = true;')
         and has(FP, 'ApplyFrmPermissionInternal', 'if (permissionTable.Rows.Count <= 0)', 'return;', 'DisableButton(button);', 'Editable = false;')
         and not m(FP, 'ApplyFrmPermissionInternal')['throws'], 'form-permission-default-and-caught-query-not-denied-outcome')
    need(has(FP, 'IsSavePermissionButton', '"btnSave"', '"btnSavePrint"', '"btnPay"', '"btnHoldOrd"')
         and has(MC, 'ApplyWpfPermissions', 'name == "btnSave" || name == "btnSavePrint"', 'btn.IsEnabled = false;')
         and 'btnPay' not in m(MC, 'ApplyWpfPermissions')['syntax_text']
         and has(COMMON, 'ApplyEditAddPermissionInternal', '"btnSave"', '"btnSavePrint"', '!frmPer.Addable && IsNew', '!frmPer.Editable && !IsNew'),
         'different-UI-button-classifiers-not-server-or-command-policy')
    need(has(MC, 'ApplyPermissionToForm@System.Windows.Window', 'if (dt.Rows.Count == 0) return;', 'ApplyWpfPermissions(window, canNew, canSave, canDelete, canSearch, canPrint);')
         and has(MC, 'ConnObj', 'conn = new SqlConnection(connstr);', 'return conn;')
         and not m(MC, 'DoApplyUserSett@System.Windows.Window')['calls'], 'global-connection-and-settings-not-resource-authorization')
    flag_rows = facts['permission_flag_writes']
    contract_roles = [r for r in flag_rows if r['path'] == CONTRACT and norm(r['left']) == 'allowEditInvoice']
    need(len(contract_roles) == 1 and contract_roles[0]['containing_selector'] == 'ctor:frmcontract'
         and contract_roles[0]['right'] == 'true' and not c(CONTRACT, 'ConfigurePermissions', 'Common.AllowEdit'),
         'contract-local-role-flag-only-constructor-true-not-blanket-electronic-bypass')
    need(has(CONTRACT, 'ConfigurePermissions', 'if (!EnableE_Invoice)', 'txtDate.IsEnabled = true;')
         and has(CONTRACT, 'LoadFoundation', 'SELECT EnableE_Invoice FROM Foundation', 'EnableE_Invoice = Convert.ToBoolean('),
         'contract-electronic-policy-is-separate-loaded-setting')
    need(has(POS, 'Window_Loaded', 'allowEditInvoice = Common.AllowEdit("frmInvPOS");')
         and has(SALE, 'Window_Loaded', 'Common.AllowEdit("frmSalePurch5")', 'Common.AllowEdit("frmSalePurch6")', 'Common.AllowEdit("frmInvSale")'),
         'POS-and-sale-conditional-form-lookups-not-loaded-document-set')
    # Every discovered literal command/flag write must have a selected whole body;
    # no count-only replacement of an unreviewed containing member.
    for row in facts['literal_command_sites'] + flag_rows:
        sel = row['containing_selector']; f = facts['methods'].get(row['path'], {}).get(sel)
        need(f is not None, 'complete-owner-for-literal-site:' + row['path'] + ':' + sel)
    for rel, sels in COMMAND_OWNERS.items():
        for sel in sels:
            f = m(rel, sel)
            need(f['return_type'] == 'void' and not any(c['function'].endswith(('.AllowEdit', '.ApplyEditAddPermission')) for c in f['calls'])
                 and not any(t in f['syntax_text'] for t in ('FrmPermission.Editable', 'FrmPermission.Addable', 'btnSave.IsEnabled ==', 'btnSavePrint.IsEnabled ==')),
                 'no-command-role-or-enabled-result-check:' + Path(rel).stem + ':' + sel)
    for rel in EDITORS:
        f = m(rel, 'SaveAndPrint')
        need(f['return_type'] == 'void' and 'async' in f['syntax_text'].split('{', 1)[0]
             and len([q for q in f['calls'] if q['function'].endswith('.SaveInvoice')]) == 1,
             'six-async-void-parents-consume-only-local-bool:' + Path(rel).stem)
    need(has(IO, 'btnSave_Click', 'Common.CheckProiedAcc(', 'netVal <= 0 && InvType != 9', 'Invoic.IsPrinted = false;', 'SaveAndPrint();')
         and not c(IO, 'btnSavePrint_Click', 'Common.CheckProiedAcc')
         and has(IO, 'btnSavePrint_Click', 'Invoic.IsPrinted = true;', 'Invoic.InvGlobalID, Invoic.InvGlobalID')
         and has(IO, 'OnKeyDown', 'if (e.Key == Key.F6) { btnSave_Click(null, null);')
         and has(IO, 'PayBill', 'InvoiceOper.PayInvoice(ref Invoic, InvObj)', 'SaveAndPrint();'), 'IO-distinct-save-print-public-pay-keyboard-paths')
    need(has(PURCH, 'btnSave_Click', 'Common.CheckProiedAcc(', 'Common.CheckReffNo(', 'netVal <= 0.0 && this.InvType != 9', 'SetPayAmounts();')
         and has(PURCH, 'btnSavePrint_Click', '_invoiceItems.Count == 0 || this.Invoic.Net == 0.0', 'item.ItemQuantity <= 0', 'SetPayAmounts();')
         and not c(PURCH, 'btnSavePrint_Click', 'Common.CheckProiedAcc')
         and not c(PURCH, 'btnSavePrint_Click', 'Common.CheckReffNo')
         and has(PURCH, 'frmInvInOut_KeyDown', 'if (e.Key == Key.F6)', 'this.btnSave_Click(sender, e);'), 'purchase-validation-parity-actual-counterchecks-not-blanket-missing-validation')
    need(has(POS, 'btnPay_Click', 'Common.CheckProiedAcc(txtDate_Value)', 'MainClass.EmpNo == 0',
             '!allowEditInvoice &&', '!Invoic.ISNew && Invoic.ProcType != 3 &&', 'Invoic.PaymentStatus == PaymentStatus.Paid')
         and has(POS, 'PayBill', 'EnableE_Invoice &&', '!(InvObj.PaymentStatus && !Invoic.IsUpdated)',
             'if (!InvoiceOper.PayInvoice(ref Invoic, InvObj))', 'SaveAndPrint();'), 'POS-pay-guards-have-specific-status-and-proctype-not-all-edits')
    need(has(POS, 'btnHoldOrd_Click', 'Invoic.InvoiceItems.Count == 0', 'Invoic.ProcType = 3;', 'ProcType = 3;',
             'SaveAndPrint();', 'HoldList[i] = Invoic.InvoiceNo;', 'UpdateHoldButtons();')
         and not c(POS, 'btnHoldOrd_Click', 'Common.CheckProiedAcc')
         and not c(POS, 'btnHoldOrd_Click', 'btnPay_Click')
         and has(POS, 'Window_KeyDown', 'btnPay_Click(null, null);', 'btnHoldOrd_Click(null, null);'), 'POS-hold-is-distinct-command-and-publishes-without-Save-result')
    need(has(POS, 'SaveAndPrint', 'if (Invoic.ISNew)', 'invoice.InvDate = DateTime.Now;',
             'if (!EnableE_Invoice && !Invoic.ISNew)', 'invoice.InvDate = DateTime.Now;'), 'POS-current-date-overwrite-before-writer')
    pos = m(POS, 'SaveAndPrint'); pos_guard = next((q['line'] for q in pos['conditions'] if norm(q['text']) == '!saved'), None)
    need(pos_guard is not None and all(q['line'] < pos_guard for name in ('updat_table', 'Insert_Table_Order', 'Update_Table_Order', 'RptPrint_Tables') for q in c(POS, 'SaveAndPrint', name))
         and all(c(POS, 'SaveAndPrint', name) for name in ('updat_table', 'Insert_Table_Order', 'Update_Table_Order', 'RptPrint_Tables')),
         'POS-table-writes-and-print-call-precede-false-return')
    need(all(m(POS, sel)['catches'] and not m(POS, sel)['throws'] for sel in ('updat_table', 'Insert_Table_Order', 'Update_Table_Order'))
         and c(POS, 'RptPrint_Tables', 'RptPrint') and not c(POS, 'BackgroundWorker1_DoWork', 'SyncInvoice'), 'POS-table-helpers-catch-and-background-worker-is-not-sync-execution')
    need(c(SALE, 'btnSave_Click', 'Common.CheckProiedAcc') and c(SALE, 'btnSavePrint_Click', 'Common.CheckProiedAcc')
         and c(SALE, 'Window_KeyDown', 'ValidateInvoice') and not c(SALE, 'Window_KeyDown', 'btnSave_Click')
         and not c(SALE, 'ValidateInvoice', 'Common.CheckProiedAcc')
         and has(SALE, 'ctor:frmInvSale', 'KeyDown += Window_KeyDown;')
         and facts['xml_elements'][SALE[:-3]][0]['attributes'].get('KeyDown') == 'Window_KeyDown', 'sale-F6-bypasses-button-wrapper-and-has-duplicate-written-wiring')
    need(has(SALE, 'ValidateInvoice', 'Invoic.InvoiceItems.Count == 0', 'item.ItemQuantity <= 0', 'if (confirm == MessageBoxResult.No) return;', 'SaveAndPrint();')
         and has(SALE, 'SaveAndPrint', '!(InvObj.PaymentStatus && !Invoic.IsUpdated)', 'if (!allowEditInvoice)', 'finally', 'IsEnabled = true;'), 'sale-validation-and-edit-exception-are-not-all-command-authorization')
    need(ordered(SALE, 'btnSaveQuotation_Click', 'ValidateInvoice', 'CLR')
         and has(SALE, 'btnSaveQuotation_Click', 'ProcType = 4;', 'Invoic.ProcType = 4;', 'ProcType = 1;', 'Invoic.ProcType = 1;')
         and m(SALE, 'ValidateInvoice')['return_type'] == 'void'
         and c(SALE, 'btnRepaid_Click', 'PayBill') and not c(SALE, 'btnRepaid_Click', 'ValidateInvoice'), 'sale-quotation-clear-and-repaid-use-distinct-void-parent-paths')
    need(c(CONTRACT, 'btnSave_Click', 'Common.CheckProiedAcc') and not c(CONTRACT, 'btnSavePrint_Click', 'Common.CheckProiedAcc')
         and c(CONTRACT, 'btnSavePrint_Click', 'ValidateInvoice')
         and has(CONTRACT, 'SaveAndPrint', 'if (!Invoic.ISNew && (ProcType == 1 || ProcType == 2))', 'if (EnableE_Invoice)', 'if (!allowEditInvoice)')
         and not c(CONTRACT, 'SaveAndPrint', 'RptPrint')
         and has(CONTRACT, 'SaveAndPrint', 'if (saved && Invoic.IsPrinted && print.PrintNo > 0)', 'Invoic.ISNew = false;'), 'contract-field-guard-and-print-flag-not-a-print-call')
    need(x(CONTRACT, 'btnSavePrint').get('Click') is None
         and has(CONTRACT, 'SetupButtonEvents', 'btnSave.Click += btnSave_Click;', 'btnSavePrint.Click += btnSavePrint_Click;')
         and has(CONTRACT, 'ctor:frmcontract', 'this.KeyDown += frmcontract_KeyDown;'), 'contract-code-wiring-not-duplicate-click-assumption')
    need(has(TRANS, 'btnSave_Click', 'Common.CheckProiedAcc(', 'if (_invoic.ProcType == 1)', 'SaveReceive();', 'else if (_invoic.ProcType == 2)', 'SaveSend();')
         and has(TRANS, 'btnSavePrint_Click', 'if (_invoic.ISNew && _invoic.ProcType == 2)', 'SaveReceive();', 'else if (TabControl1.SelectedIndex == 0)', 'SaveAndPrint();')
         and not c(TRANS, 'btnSavePrint_Click', 'SaveSend') and not c(TRANS, 'btnSavePrint_Click', 'Common.CheckProiedAcc'), 'transfer-save-print-route-difference-is-not-naming-intent')
    need(len(c(TRANS, 'SaveReceive', 'SaveAndPrint')) == 2 and len(c(TRANS, 'SaveSend', 'SaveAndPrint')) == 2
         and has(TRANS, 'SaveSend', '_invoic.ISNew = true;', '_invoic.ProcType = 1;', '_invoic.ReffNo = _invoic.InvGlobalID;', 'savedMsg.ShowDialog();')
         and not any(q['function'].endswith('.SaveInvoice') for sel in ('SaveSend', 'SaveReceive') for q in m(TRANS, sel)['calls'])
         and not any('await' in q['function'] for sel in ('SaveSend', 'SaveReceive') for q in m(TRANS, sel)['calls']), 'transfer-two-void-calls-no-shared-success-or-transaction-result')
    for rel, inv in ((IO, 'Invoic'), (POS, 'Invoic'), (PURCH, 'Invoic'), (SALE, 'Invoic'), (CONTRACT, 'Invoic'), (TRANS, '_invoic')):
        writer = [q for q in c(rel, 'SaveAndPrint', 'invoiceOper.SaveInvoice') + c(rel, 'SaveAndPrint', 'operContract.SaveInvoice')]
        stock = c(rel, 'SaveAndPrint', 'Inventory.UpdateItemStock')
        need(len(writer) == len(stock) == 1, 'one-writer-and-cache-call:' + Path(rel).stem)
        if writer and stock:
            need((stock[0]['line'] < writer[0]['line']) == (rel in (IO, PURCH, TRANS)), 'cache-order-relative-to-local-bool:' + Path(rel).stem)
            if rel == POS:
                need(pos_guard < stock[0]['line'] and guarded(stock[0], 'invoice.ProcType == 1 || invoice.ProcType == 2'), 'POS-cache-after-false-return-counterexample')
            if rel in (SALE, CONTRACT):
                need(not any(a.get('kind') == 'if' and norm(a.get('condition', '')) == 'saved' for a in stock[0]['ancestors']), 'sale-contract-cache-not-dominated-by-saved:' + Path(rel).stem)
    need(has(STOCK, 'UpdateItemStock', 'dynamic invDynamic = inv;', 'foreach (Item item in invDynamic.Items)',
             'itemId = {item.ItemNo}', 'rows[0]["Inventory"]', 'rows[0]["Stock"] = currentStock + item.PrimaryQnty;',
             'rows[0]["Stock"] = currentStock - item.PrimaryQnty;', 'Debug.WriteLine(')
         and not any(q['function'].endswith(('ExecuteNonQuery', 'BeginTransaction')) for q in m(STOCK, 'UpdateItemStock')['calls']), 'cache-helper-is-loaded-DataTable-delta-not-persisted-stock-commit')
    need(has(PURCH, 'SaveAndPrint', 'if (entry == null) return;')
         and not any(norm(q['text']) == 'entry==null' for rel in (POS, SALE, CONTRACT) for q in m(rel, 'SaveAndPrint')['conditions'])
         and all(has(rel, 'BindToEntry', 'result = null;') for rel in (IP, IPC)), 'purchase-null-entry-return-counterexample-not-all-parents-safe')
    for rel in (IP, IPC):
        f = m(rel, 'SaveInvoice')
        need(f['return_type'] == 'bool' and norm(f['parameters']) == '(Invoiceinv,EntryEntr,boolIsNew)'
             and has(rel, 'SaveInvoice', 'MainClass.EmpNo < 1', 'if (Entr == null)', 'sqlTransaction.Commit();', 'new EntryOper().SaveEnty(Entr)', 'sqlTransaction.Rollback();')
             and not c(rel, 'SaveInvoice', 'Common.CheckProiedAcc')
             and not c(rel, 'SaveInvoice', 'Common.AllowEdit'), 'writer-invariants-and-null-entry-commit-not-allowed-document-set:' + Path(rel).stem)
    need(has(EO, 'SaveEnty', 'using SqlConnection conn = MainClass.ConnObj();', 'SqlTransaction transaction = conn.BeginTransaction();',
             'transaction.Commit();', 'return true;', 'foreach (Account account in entry.Accounts)')
         and not c(EO, 'SaveEnty', 'Common.CheckProiedAcc')
         and not any(t in m(EO, 'SaveEnty')['syntax_text'] for t in ('Accounts.Count == 0', 'Accounts.Count <= 0', '.Sum(')), 'entry-has-own-commit-without-local-empty-balance-or-period-check')
    for key in ('UpdateInv', 'UpdateInvcontract'):
        sql = facts['sql_fields'][key]['sql_text']; where = re.split(r'\bwhere\b', sql, flags=re.I)[-1]
        need(re.sub(r'[\s;]', '', where).lower() == 'invglobalid=@invglobalid'
             and not facts['sql_fields'][key]['provider_binding_or_deployed_schema_verified'], 'update-key-only-no-origin-branch-year-allowed-set:' + key)
    need(has(COMMON, 'GetInventoryBranch', 'select branch from Safes where id=@Id', ': 1;', 'return 1;')
         and has(TRANS, 'SaveAndPrint', 'invoice.Branch = Common.GetInventoryBranch(SafeInt(cmbSafeTo.SelectedValue));',
             'invoice.Branch = Common.GetInventoryBranch(SafeInt(cmbSafeFrom.SelectedValue));'), 'transfer-mapped-branch-fallback-one-is-not-an-ACL')
    need(has(IP, 'MappingInvoice', 'if (Inv.ISNew)', 'Inv.InvoiceNo = InvoiceOper.InvoiceNo(', 'InvoiceOper.GetInvoiceGlobalID(',
             'invoice.InvoiceItems = Inv.InvoiceItems;', 'invoice.Branch = Inv.Branch;', 'this.BindingCompositeItems(ref Items, Inv.InvertoryImpact);', 'invoice.Items = list;')
         and all(a['right'] == 'false' for a in assignments(m(IP, 'VerifyIsNewInvoice'), 'result')),
         'mapping-is-stateful-but-VerifyIsNewInvoice-never-assigns-true-counterexample')
    need(has(IPC, 'MappingInvoicecontract', 'InvoiceOperContract.GetInvoiceGlobalIDcontract(', 'invoice.InvoiceItems = Inv.InvoiceItems;',
             'invoice.contract_total_value = Inv.contract_total_value;', 'this.BindingCompositeItems(ref Items, Inv.InvertoryImpact);')
         and all(has(rel, 'BindingCompositeItems', 'list = Items;', 'list.Add(invoiceItem);', 'catch') for rel in (IP, IPC)), 'local-composite-helper-is-readable-state-writer-not-missing-DTO-substitute')
    need(has(IP, 'SaveInvoice', 'this.SendZatca(inv);', 'sqlConnection2.BeginTransaction();', 'this.InsertZatcaEncodedInvoice(inv);')
         and ordered(IP, 'SaveInvoice', 'this.SendZatca', 'sqlConnection2.BeginTransaction')
         and has(IPC, 'SaveInvoice', 'zatcaService.IntegrateInvoice(ref inv,', 'sqlConnection3.BeginTransaction();'), 'tax-send-and-local-commit-are-distinct-boundaries-not-provider-success-proof')
    need(has(IP, 'insertDocument', 'File.Copy(text, text2, overwrite: true);', 'new SqlConnection(MainClass.connstr)')
         and has(IPC, 'insertDocument', 'File.Copy(text3, text4, overwrite: true);', 'new SqlConnection(MainClass.connstr)')
         and has(IP, 'InsertZatcaEncodedInvoice', 'sqlConnection = MainClass.ConnObj();'), 'attachment-file-and-encoded-writers-own-connections-not-outer-transaction')
    need(has(IPC, 'SaveInvoice', 'if (inv.InvoiceItems.Count == 0)', 'foreach (Item item in inv.Items)', 'new SqlCommand(StoredQueries.InsertInvSub, sqlConnection3, sqlTransaction)')
         and has(IPC, 'SaveInvoice', 'new SqlCommand(StoredQueries.InsertInvSubcontract, sqlConnection3, sqlTransaction)'), 'contract-ordinary-fallback-line-target-is-not-contract-target')
    need(has(POS, 'SaveAndPrint', 'if (!(await invoiceOper.SyncInvoice(', 'Sync.SyncCloudFirst && !holdbool')
         and not any('!saved' in q['text'] for q in m(TRANS, 'SaveAndPrint')['conditions'])
         and has(TRANS, 'SaveAndPrint', 'if (Home._is_active)', 'SendData.SendDataa('), 'cloud-first-result-checked-but-transfer-broker-not-local-bool-guarded')
    for rel, table in ((IP, 'Inv'), (IPC, 'InvContratct')):
        need(m(rel, 'SyncInvoice')['return_type'] == 'Task<bool>' and has(rel, 'SyncInvoice', 'bool result = default(bool);',
             'if (Sync.BranchType == 4)', 'return true;', 'return result;', 'entryOper.SyncEntry(Eny, IsNew);', 'update ' + table + ' set Sync=1'),
             'sync-local-wrapper-result-not-end-to-end-commit:' + Path(rel).stem)
    need(has(IPC, 'SyncInvoice', 'update Inv set Sync=1 where InvGlobalID=')
         and all(not any('await' in r['text'] for r in m(rel, 'SaveAndPrint')['returns']) for rel in EDITORS), 'contract-noncloud-sync-target-and-void-callers-remain-qualified')
    for name, bridge in facts['header_parameter_bridges'].items():
        need(bridge['whitespace_trimmed_missing_placeholders'] == []
             and {'@QRCode', '@InvoiceHash', '@UUID', '@ZatcaSent'} <= set(bridge['raw_supplied_parameter_names'])
             and bridge['provider_binding_or_all_parameter_health_certified'] is False,
             'header-tax-parameters-are-present-counterexample:' + name)
    for rel, selector in ((HOME, 'stripSaleRetu_Click'), (HOME, 'stripInputInv_Click'), (HOME, 'stripTransfer_Click')):
        need(ordered(rel, selector, 'MainClass.ApplyPermissionToForm', 'frm.Show'), 'opener-UI-lookup-not-command-or-document-ACL:' + selector)
    need(has(HOME, 'stripSaleRetu_Click', 'MainClass.ApplyPermissionToForm(frm);', 'frm.Tag = "SalePurch5";')
         and has(HOME, 'stripPurchInv_Click', 'frm.Name = "frmSalePurch";', 'frm.Tag = "SalePurch";')
         and has(HOME, 'stripinvcontractreturn_Click', 'frm.Name = "frmcontractReturn";', 'frm.Tag = "frmcontract";'),
         'different-Name-Tag-and-lookup-order-need-policy-row-not-runtime-assumption')
    need(has(HOME, 'btnPOS2_Click', 'else if (stripPOS.IsEnabled)')
         and not has(HOME, 'BtnSales_Click', 'stripSaleInv.IsEnabled'), 'one-opener-enabled-check-counterexample-not-all-menu-commands')
    need(has(SELECT, 'GenerateInvoice', 'FindOpenedWindow<frmInvPOS>()', 'openedPosWindow.ImportInventoryItems(itemList);',
             'form.ImportInventoryItems(itemList);')
         and has(SELECT, 'FindOpenedWindow', '.OfType<T>()', '.FirstOrDefault()')
         and has(SELECT, 'ShowWindowAndCloseCurrent', 'targetWindow.Show();', 'targetWindow.Activate();', 'Close();'),
         'alternate-import-can-target-existing-POS-without-new-window-policy-application')
    for rel in (IO, POS, PURCH, SALE):
        need(has(rel, 'ImportInventoryItems', 'SearchByID(importedItem.ItemId, 0,', 'FirstOrDefault(',
                 '== importedItem.ItemId)', 'ItemPrice = importedItem.ItemPrice;', 'ItemQuantity = importedItem.ItemQuantity;')
             and not c(rel, 'ImportInventoryItems', 'Common.AllowEdit'), 'import-first-item-match-is-not-inserted-row-result:' + Path(rel).stem)
    need(has(CONTACT, 'BtnShowInv_Click', 'if (invType == 23)', 'contractForm.InvType = 2;',
             'FROM InvContratct WHERE IS_Deleted=0', 'AND inv_type=23 AND proc_type=', "InvGlobalID=N'{globalId}'")
         and not c(CONTACT, 'BtnShowInv_Click', 'MainClass.ApplyPermissionToForm')
         and ordered(CONTACT, 'BtnShowInv_Click', 'contractForm.Show', 'contractForm.Navigate'),
         'contract-opener-UI-type-two-vs-selected-row-type23-is-not-missing-global-key')
    for sel in OPENER_OWNERS[RPTINV]:
        need(has(RPTINV, sel, "InvGlobalID=N'{globalId}'")
             and ordered(RPTINV, sel, 'frm.Show', 'frm.Navigate'), 'global-key-opener-counterexample-to-all-local-id-claim:' + sel)
    return errors


def read_errors(reads, facts, root: Path = ROOT):
    errors, covered = [], {}
    for row in reads.get('reads', []):
        rel, a, b = row['path'], row['start'], row['end']
        text = previous.prior.prior.text_range(base.decode((root / rel).read_bytes()), a, b)
        if base.sha(text.encode('utf8')) != row['decoded_range_utf8_sha256']:
            errors.append('read:range-identity:' + row['id'])
        covered.setdefault(rel, set()).update(range(a, b + 1))
    selected = [(rel, sel, f['start'], f['end']) for rel, group in facts['methods'].items() for sel, f in group.items()]
    selected += [(r['path'], key, r['start'], r['end']) for key, r in facts['text_ranges'].items()]
    selected += [(rel, 'selected-xml-element', e['line'], e['line']) for rel, group in facts['xml_elements'].items() for e in group]
    for rel, sel, a, b in selected:
        if not set(range(a, b + 1)) <= covered.get(rel, set()): errors.append('read:uncovered:' + rel + ':' + sel)
    if any(reads.get(k) is not False for k in ('extraction_equals_reading', 'independent_human_review_claimed', 'individual_read_timestamps_invented')):
        errors.append('read:no-extraction-or-invented-chronology-as-reading-proof')
    return errors


def preservation_errors(entry, root: Path = ROOT):
    errors = []
    if entry.get('HEAD') != BASE_HEAD or entry.get('branch') != 'arena/94ae8414-smartauditerp' or len(entry.get('preserved_tracked_audit_inputs', {})) != 1604:
        errors.append('preservation:published-R8-entry')
    for rel, expected in entry.get('preserved_tracked_audit_inputs', {}).items():
        raw = (root / rel).read_bytes(); same = {'bytes': len(raw), 'sha256': base.sha(raw)} == expected
        if not same and rel in previous.prior.prior.MUTABLE_INDEXES:
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
    facts, matrix, review, roots, work, note = [load(n, ev) for n in (FACTS, MATRIX, REVIEW, ROOTS, WORK, DATE_NOTE)]
    errors = []
    def need(ok, label):
        if not ok: errors.append('evidence:' + label)
    need(note.get('assessment_reference_date_utc') == note.get('session_reference_date_utc') == DATE
         and note.get('prospective_only') is True and note.get('historical_tests_relabelled_as_current') is False
         and note.get('user_requested_reference_date_authenticated') is False, 'prospective-date-and-attribution-not-historical-recertification')
    for rel, pin in note.get('preserved_prior_identities', {}).items():
        need({k: identity(rel)[k] for k in ('bytes', 'sha256')} == {k: pin[k] for k in ('bytes', 'sha256')}, 'date-correction-preserves-original:' + rel)
    need(matrix.get('literal_command_sites') == facts['literal_command_sites'], 'exact-literal-command-sites-not-count-only')
    expected = [(rel, sel) for rel, names in COMMAND_OWNERS.items() for sel in names]
    rows = matrix.get('command_reviews', [])
    need([(r.get('path'), r.get('entry_selector')) for r in rows] == expected, 'all23-selected-command-owner-identities')
    for row in rows:
        rel, sel = row['path'], row['entry_selector']; f = method(facts, rel, sel)
        need(row.get('whole_entry_context') == {k: f[k] for k in ('start', 'end', 'syntax_utf8_sha256')}
             and row.get('whole_body_displayed_and_assessed_in_R9') is True
             and row.get('compiler_or_runtime_reachability_certified') is False
             and row.get('whole_route_or_capability_certified') is False
             and row.get('accepted_external_handoff') is False
             and set(row.get('decision_ids', [])) <= DECISIONS and bool(row.get('decision_ids')),
             'qualified-command-context:' + rel + ':' + sel)
        for key in ('input_to_validation', 'permission_and_allowed_set', 'writer_entry_stock_transaction', 'publication_and_outcomes', 'counterevidence_and_limit', 'remaining_local'):
            need(bool(row.get(key)), 'command-disposition:' + sel + ':' + key)
        errors += previous.source_basis_errors(row.get('source_basis', []), facts)
    need(matrix.get('selected_alternate_editor_creations') == facts['selected_alternate_editor_creations'], 'exact-selected-alternate-creations-not-all-ingress')
    opener_rows = matrix.get('alternate_opener_reviews', [])
    need([(r.get('path'), r.get('entry_selector')) for r in opener_rows] == [(rel, sel) for rel, sels in OPENER_OWNERS.items() for sel in sels], 'twentysix-selected-opener-owners-not-twentysix-capability-exits')
    for row in opener_rows:
        need(all(bool(row.get(k)) for k in ('configured_request', 'policy_lookup_and_order', 'document_branch_year_and_allowed_set', 'source_basis', 'remaining_local'))
             and row.get('all_ingress_or_runtime_schedule_certified') is False
             and row.get('accepted_external_handoff') is False, 'qualified-alternate-opener:' + row.get('entry_selector', '?'))
        errors += previous.source_basis_errors(row.get('source_basis', []), facts)
    pipelines = matrix.get('editor_pipelines', {})
    need(set(pipelines) == set(EDITORS), 'six-independent-editor-pipelines')
    for rel, row in pipelines.items():
        need(all(bool(row.get(k)) for k in ('input_mapping', 'validation', 'permission', 'writer', 'entry', 'stock', 'transaction', 'publication', 'allowed_set_and_origin', 'remaining_readable_local'))
             and row.get('all_readable_local_obligations_complete') is False
             and row.get('is_capability_exit') is False, 'qualified-editor-pipeline:' + rel)
        errors += previous.source_basis_errors(row.get('source_basis', []), facts)
    decisions = review.get('source_decisions', [])
    need({r.get('id') for r in decisions} == DECISIONS and len(decisions) == len(DECISIONS), 'fifteen-substantive-source-decisions')
    for row in decisions:
        need(bool(row.get('source_disposition')) and bool(row.get('counterevidence_and_limit'))
             and bool(row.get('source_basis')) and row.get('observed_in_ERP') is False
             and row.get('is_capability_exit') is False, 'qualified-source-decision:' + row.get('id', '?'))
        errors += previous.source_basis_errors(row.get('source_basis', []), facts)
    actual = base.rows('findings.csv', AUDIT) + base.rows('findings-additions-07B39R1.csv'); by_id = {r['id']: r for r in actual}
    need(roots.get('available_prior_rows') == actual and len(actual) == 339, '339-original-dictionaries-preserved-not-339-fresh-reviews')
    focused = roots.get('focused_root_reviews', {})
    need(set(focused) == set(FOCUSED), 'twentythree-focused-root-comparisons')
    for rid, row in focused.items():
        need(row.get('canonical_prior_row') == by_id.get(rid) and bool(row.get('reason')), 'unchanged-root-row:' + rid)
    candidates = roots.get('candidate_dispositions', [])
    need(len(candidates) == len(CANDIDATES) and {r.get('id'): r.get('root_id') for r in candidates} == CANDIDATES, 'twentytwo-source-question-identities-not-new-numbered-findings')
    for row in candidates:
        need(row.get('novelty_certified') is False and row.get('accepted_external_handoff') is False
             and row.get('observed_financial_or_provider_failure') is False
             and bool(row.get('source_disposition')) and bool(row.get('remaining_local')),
             'qualified-root-question:' + row.get('id', '?'))
        errors += previous.source_basis_errors(row.get('source_basis', []), facts)
    need(roots.get('new_finding_ids') == [] and roots.get('historical_root_fields_rewritten') is False
         and roots.get('all345_roots_screened') is False and roots.get('all339_semantically_reread_in_R9') is False
         and roots.get('missing_six_dictionaries_reconstructed') is False, 'no-novelty-or-missing-history-certification')
    caps = {r['id']: r for r in base.rows('capability-register-07B38.csv')}
    need(set(review.get('capabilities', {})) == set(TARGETS), 'five-bounded-capabilities-not-all26-fresh-assessments')
    for cid, row in review.get('capabilities', {}).items():
        need(row.get('canonical_capability_row') == caps.get(cid) and row.get('whole_capability_certified') is False
             and row.get('local_semantic_obligations_complete') is False and row.get('readable_local_externalized') is False
             and bool(row.get('remaining_readable_local')), 'named-capability-local-remainder:' + cid)
    original37 = load(previous.OLD_WORK)['calls']
    need(work.get('original37_R6_rows_verbatim') == original37
         and work.get('original_R6_read_flags_rewritten') is False
         and work.get('entire_R8LOCAL_SAVE_EDIT_marked_complete') is False
         and work.get('all_alias_reflection_or_document_ingress_complete') is False, 'original-ancestry-and-unfinished-local-commands-preserved')
    old_tasks = load(previous.WORK)['remaining_readable_local_tasks']
    need(work.get('preserved_R8_local_task_rows_verbatim') == old_tasks, 'R8-local-obligations-not-erased-or-externalized')
    tasks = work.get('remaining_readable_local_tasks', [])
    need(len(tasks) >= 5, 'named-local-successor-work')
    for row in tasks:
        need(bool(row.get('id')) and bool(row.get('source_paths_or_prior_evidence')) and bool(row.get('next_action'))
             and bool(row.get('owner_role')) and row.get('externalized') is False, 'owned-local-task:' + row.get('id', '?'))
    for row in review.get('unavailable_contracts_not_accepted_as_handoffs', []):
        need(all(bool(row.get(k)) for k in ('source_basis', 'owner_role', 'required_redacted_input', 'absence_impact', 'next_action', 'static_disposition', 'readable_local_not_delegated'))
             and row.get('accepted_external_handoff') is False, 'unavailable-is-not-local-work-substitute')
        errors += previous.source_basis_errors(row.get('source_basis', []), facts)
    for name in (READS, MATRIX, ROOTS, WORK, REVIEW):
        obj = load(name, ev)
        need(obj.get('assessment_reference_date_utc') == DATE and obj.get('session_reference_date_utc') == SESSION_DATE
             and obj.get('raw_clocks_are_calendar_authority') is False, 'new-prospective-date-only:' + name)
        need(obj.get('application_execution_count') == 0 and obj.get('whole_7B_static_assessment_complete') is False
             and obj.get('capability_exit_certificates_issued') == obj.get('four_family_exit_certificates_issued') == 0
             and obj.get('new_accepted_external_handoffs') == 0 and obj.get('phase7C_started') is False
             and obj.get('phase8_authorized') is False and obj.get('R2_R3_files_recovered') is False
             and obj.get('prior196_tests_recertified') is False, 'static-open-scope:' + name)
        need(bool(obj.get('pinned_inputs')), 'explicit-versioned-inputs:' + name)
        for pin in obj.get('pinned_inputs', []): need(identity(pin['path']) == pin, 'pinned-input-changed:' + pin['path'])
    return errors


def verify(rederive=False, ev: Path = EV):
    facts = load(FACTS, ev); errors = []
    for rel, pin in facts['source_identity'].items():
        if identity(rel) != pin: errors.append('source-identity:' + rel)
    if rederive and derive() != facts: errors.append('fresh-source-rederivation-differs')
    errors += source_errors(facts) + read_errors(load(READS, ev), facts)
    errors += preservation_errors(load(ENTRY, ev)) + evidence_errors(ev)
    return {'schema_version': 1, 'errors': errors,
        'selected_complete_method_contexts': sum(len(g) for g in facts['methods'].values()),
        'source_identities': len(facts['source_identity']), 'literal_command_calls': len(facts['literal_command_sites']),
        'selected_command_owners': sum(map(len, COMMAND_OWNERS.values())), 'editor_pipelines': 6, 'selected_alternate_opener_owners': sum(map(len, OPENER_OWNERS.values())),
        'source_decisions': len(DECISIONS), 'capability_exit_certificates_issued': 0,
        'four_family_exit_certificates_issued': 0, 'new_accepted_external_handoffs': 0,
        'whole_7B_static_assessment_complete': False, 'application_execution_count': 0,
        'phase7C_started': False, 'phase8_authorized': False,
        'limit': 'Recorded static assertions, not reading/calendar/runtime authorization, provider, financial or capability/family acceptance.'}


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
