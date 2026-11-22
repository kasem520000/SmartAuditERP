#!/usr/bin/env python3
"""R11 read-only audit assertions for reconciliation, not application tests.

Strict C# syntax and selected SQL *text* only. Never imports/executes C#,
SQL, WPF, providers, models, SDKs or devices. --derive exclusively creates a
new evidence file; ordinary verification never writes. Source mutations in
Python tests are counterexamples to assertions, NOT application repairs.
Hashes/counts do not prove reading, dates, runtime failure or authorization.
The R10 remote verifier has import-time writes and must NOT be imported.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tarfile

import verify_save_edit as prior

ROOT, AUDIT, EV, base = prior.ROOT, prior.AUDIT, prior.EV, prior.base
TAG, DATE = '07B39R11', '2026-11-16'
D = 'docs/audit/tools/disposition07b/'
E = 'docs/audit/evidence/'
P, C = 'SmartAuditERP/Form_WPF/', 'SmartAuditERP/Class/'
RO, SQ, FS, UL, MC, RC = (C + 'ReceiptOper.cs', C + 'StoredQueries.cs',
    P + 'frmSettings.xaml.cs', P + 'frmUserLogin.xaml.cs', C + 'MainClass.cs',
    P + 'frmRecyclingData.xaml.cs')
RES, PROJ, XML = 'SmartAuditERP/Properties/Resources.resx', 'SmartAuditERP/SmartAuditERP.csproj', P + 'frmSettings.xaml'
RESTORERS = {P + n + '.xaml.cs': table for n, table in (
    ('frmSandD', 'SandD'), ('frmSandSD', 'SandSD'), ('frmSandQD', 'SandQD'),
    ('frmSandQAndroid', 'SandQ'))}
CONTEXTS = {
    RO: ('SaveReceipt', 'SaveReceipt2', 'ReadReceiptOnline'),
    FS: ('ctor:frmSettings', 'RegisterEvents', 'frmUserSettings_Load',
         'EnsureConnectionOpen', 'LoadSettingNotify', 'BtnConnect_Click', 'insert_SettingNotify'),
    UL: ('ctor:frmUserLogin', 'Login', 'LoadBranches', 'ConnectMQTList', 'CheckMqttStat'),
    MC: ('ConnObj',), RC: ('CopySettingsTablesAsync', 'ExecuteSqlAsync', 'EnsureOpen'),
    **{rel: ('RestorePreviousReceipt',) for rel in RESTORERS},
}
CONTEXTS[P + 'frmSandSD.xaml.cs'] += ('SafeOpenConnection', 'SafeCloseConnection')
CONTEXTS[P + 'frmSandQD.xaml.cs'] += ('SafeOpen', 'SafeClose')
TEXT_RANGES = {
    'receipt-base-create': (RES, 1496, 1531),
    'receipt-guarded-create': (RES, 47874, 47912),
    'receipt-recipient-guarded-alter': (RES, 50887, 50892),
    'mqtt-base-create': (RES, 4809, 4837),
    'mqtt-guarded-create': (RES, 50501, 50529),
    'mqtt-ip-guarded-alter': (RES, 50601, 50606),
    'mqtt-flags-guarded-alters': (RES, 50680, 50698),
    'external-model-reference': (PROJ, 28, 36),
    'notify-button-element': (XML, 1949, 1955),
    'receipt-model-namespace': (RO, 1, 12),
}
FACTS = 'reconciliation-source-facts-' + TAG + '.json'
READS = 'reconciliation-source-review-' + TAG + '.json'
REVIEW = 'reconciliation-adjudications-' + TAG + '.json'
LEDGER = 'capability-reconciliation-' + TAG + '.json'
DATE_NOTE = 'reference-date-provenance-' + TAG + '.json'
ENTRY = 'reconciliation-entry-' + TAG + '.json'
HYDRATION = 'entry-before-hydration-' + TAG + '.json'
RESTORATION = 'canonical-register-restoration-' + TAG + '.json'
INDEXES = ('docs/audit/README.md', 'docs/audit/PLAN.md')
ORIGINAL_FINDINGS = {'path': 'docs/audit/findings.csv', 'bytes': 222939,
    'sha256': 'ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a'}
QUESTION_IDS = ('R11Q-RECIPIENT', 'R11Q-RESTORE-IDENTITY', 'R11Q-NOTIFY-REPLACE',
    'R11Q-NOTIFY-BRANCH', 'R11Q-NOTIFY-RESULT', 'R11Q-NOTIFY-SECRETS')
FOCUSED_ROOTS = ('P1-009', 'P1-014', 'P1-017', 'P3-003', 'P3-004', 'P3-005',
    'P3-009', 'P3-010', 'P3-011', 'P5-004', 'P5-012', 'P5-015', 'P5-016',
    'P5-030', 'P5-031', 'P7-164', 'P7-165')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def identity(rel, root=ROOT):
    raw = (root / rel).read_bytes()
    return {'path': rel, 'bytes': len(raw), 'sha256': sha(raw)}


def load(name, ev=EV):
    return json.loads((ev / name).read_bytes())


def exclusive_json(path, value):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def rows(raw):
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline='')))


def dictionary_rows(root=ROOT):
    return rows((root / ORIGINAL_FINDINGS['path']).read_bytes()) + rows((root / (E + 'findings-additions-07B39R1.csv')).read_bytes())


def literal(code):
    # A concatenation may start AND end with quotes without being one literal.
    # Strict whole-file C# parsing still happens independently of this decoder.
    if re.fullmatch(r'@"(?:""|[^"])*"', code, re.S):
        return code[2:-1].replace('""', '"')
    if re.fullmatch(r'"(?:\\.|[^"\\])*"', code, re.S):
        return json.loads(code)
    return None


def interpolated_syntax(code):
    """Retain unevaluated interpolation body; not a decoded SQL command/value."""
    for prefix in ('$@"', '@$"', '$"'):
        if code.startswith(prefix) and code.endswith('"'):
            return code[len(prefix):-1]
    return None


def static_sql_text(command):
    return command['literal_sql'] if command['literal_sql'] is not None else command.get('interpolated_template_syntax')


def selected(parsed, selector):
    constructor = selector.startswith('ctor:')
    name = selector.removeprefix('ctor:')
    kind = 'constructor_declaration' if constructor else 'method_declaration'
    found = [n for n in base.walk(parsed.tree.root_node) if n.type == kind
             and parsed.text(n.child_by_field_name('name')) == name]
    if len(found) != 1:
        raise ValueError('Expected one supplied declaration: ' + selector)
    return found[0]


def arguments(parsed, node):
    args = node.child_by_field_name('arguments')
    return [parsed.text(a) for a in args.named_children] if args else []


def storage_target(parsed, node, stop):
    parent = node.parent
    while parent and parent != stop:
        if parent.type == 'variable_declarator':
            return parsed.text(parent.child_by_field_name('name'))
        if parent.type == 'assignment_expression':
            return parsed.text(parent.child_by_field_name('left'))
        parent = parent.parent
    return None


def source_methods(text, selectors):
    result = prior.source_methods(text, selectors)
    parsed = base.Syntax(text)
    for selector, row in result.items():
        parent = selected(parsed, selector)
        row['parameter_adds'], row['command_expressions'], row['query_references'] = [], [], []
        row['try_regions'] = []
        for n in base.walk(parent):
            if n.type == 'try_statement':
                row['try_regions'].append({'start': n.start_point.row + 1, 'end': n.end_point.row + 1})
            elif n.type == 'invocation_expression':
                name = parsed.text(n.child_by_field_name('function'))
                if name.endswith(('.Parameters.Add', '.Parameters.AddWithValue')):
                    args = arguments(parsed, n)
                    row['parameter_adds'].append({'function': name, 'arguments': args,
                        'name_literal': literal(args[0]) if args else None, 'line': n.start_point.row + 1})
            elif n.type == 'object_creation_expression':
                typ = parsed.text(n.child_by_field_name('type'))
                if typ in ('SqlCommand', 'SqlDataAdapter'):
                    args = arguments(parsed, n)
                    row['command_expressions'].append({'type': typ, 'target_syntax': storage_target(parsed, n, parent),
                        'arguments': args, 'literal_sql': literal(args[0]) if args else None,
                        'interpolated_template_syntax': interpolated_syntax(args[0]) if args else None,
                        'line': n.start_point.row + 1, 'end': n.end_point.row + 1,
                        'ancestors': prior.legacy.ancestors(parsed, n, parent)})
            elif n.type == 'member_access_expression' and parsed.text(n).startswith('StoredQueries.'):
                row['query_references'].append({'text': parsed.text(n), 'line': n.start_point.row + 1})
    return result


def sql_fields(text):
    parsed = base.Syntax(text)
    result = {}
    for n in base.walk(parsed.tree.root_node):
        if n.type != 'variable_declarator':
            continue
        name = parsed.text(n.child_by_field_name('name'))
        if name not in ('InsertReceipt', 'UpdateReceipt'):
            continue
        values = [c for c in n.named_children if c.type in ('string_literal', 'verbatim_string_literal')]
        if len(values) != 1 or name in result:
            raise ValueError('Expected one literal per receipt query')
        sql = literal(parsed.text(values[0]))
        result[name] = {'path': SQ, 'start': n.start_point.row + 1, 'end': n.end_point.row + 1,
            'syntax_utf8_sha256': sha(parsed.text(n).encode('utf8')), 'sql_text': sql,
            'placeholder_names': sorted(set(re.findall(r'@[A-Za-z_][A-Za-z0-9_]*', sql))),
            'provider_binding_or_deployment_certified': False}
    if set(result) != {'InsertReceipt', 'UpdateReceipt'}:
        raise ValueError('Missing receipt query')
    return result


def parse_insert(sql):
    """Selected simple INSERT column/placeholder lists; NOT a SQL parser/engine."""
    match = re.fullmatch(r'\s*INSERT\s+INTO\s+(\S+)\s*\((.*?)\)\s*VALUES\s*\((.*?)\)\s*', sql, re.I | re.S)
    if not match:
        raise ValueError('Expected the supplied simple INSERT syntax')
    raw_columns = [s.strip() for s in match[2].split(',')]
    columns = [s.strip('[]') for s in raw_columns]
    parameters = [s.strip() for s in match[3].split(',')]
    if not all(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', s) for s in columns):
        raise ValueError('Unsupported column syntax')
    if not all(re.fullmatch(r'@[A-Za-z_][A-Za-z0-9_]*', s) for s in parameters):
        raise ValueError('Unsupported VALUES syntax')
    return {'table_syntax': match[1], 'columns': columns, 'parameters': parameters,
        'column_count': len(columns), 'parameter_count': len(parameters),
        'bracketed_column_count_not_total': sum(s.startswith('[') for s in raw_columns)}


def method(facts, rel, selector):
    return facts['methods'][rel][selector]


def calls(row, suffix):
    return [c for c in row['calls'] if c['function'].endswith(suffix)]


def commands(row, prefix):
    return [c for c in row['command_expressions'] if static_sql_text(c) is not None
            and static_sql_text(c).lstrip().casefold().startswith(prefix.casefold())]


def bridge(facts, rel, selector, variable, query):
    row = method(facts, rel, selector)
    raw = [r['name_literal'] for r in row['parameter_adds']
           if r['function'].startswith(variable + '.Parameters.')]
    if not all(isinstance(s, str) for s in raw):
        raise ValueError('A selected parameter name is not a literal')
    required = facts['sql_fields'][query]['placeholder_names']
    supplied = {s.casefold() for s in raw}
    return {'query': query, 'path': rel, 'selector': selector, 'command_variable_syntax': variable,
        'raw_supplied_names': raw, 'literal_add_count': len(raw),
        'casefold_only_missing': sorted(s for s in required if s.casefold() not in supplied),
        'case_only_spelling_differences': sorted(s for s in required if s.casefold() in supplied and s not in raw),
        'casefold_is_a_text_comparison_not_provider_binding': True}


def derive(root=ROOT):
    result = {'schema_version': 1, 'kind': 'R11-fresh-bounded-source-extraction-not-recovered-local-R10',
        'assessment_reference_date_utc': DATE, 'source_identity': {}, 'methods': {}, 'sql_fields': {},
        'text_ranges': {}, 'bridges': {}, 'discovery': {}, 'application_execution_count': 0,
        'runtime_or_all_ingress_or_model_defaults_certified': False, 'extraction_equals_reading': False}
    cache = {}
    for rel, sels in CONTEXTS.items():
        text = cache[rel] = base.decode((root / rel).read_bytes())
        result['source_identity'][rel] = identity(rel, root)
        result['methods'][rel] = source_methods(text, sels)
    cache[SQ] = base.decode((root / SQ).read_bytes())
    result['source_identity'][SQ] = identity(SQ, root)
    result['sql_fields'] = sql_fields(cache[SQ])
    for key, (rel, a, b) in TEXT_RANGES.items():
        if rel not in cache:
            cache[rel] = base.decode((root / rel).read_bytes())
        result['source_identity'][rel] = identity(rel, root)
        text = '\n'.join(cache[rel].splitlines()[a - 1:b])
        result['text_ranges'][key] = {'path': rel, 'start': a, 'end': b, 'text': text,
            'decoded_range_utf8_sha256': sha(text.encode('utf8'))}
    for sel, variable in (('SaveReceipt', 'sqlCommand3'), ('SaveReceipt2', 'sqlCommand'), ('ReadReceiptOnline', 'sqlCommand')):
        result['bridges'][sel] = bridge(result, RO, sel, variable, 'InsertReceipt')
    insert = commands(method(result, FS, 'insert_SettingNotify'), 'INSERT')[0]
    result['notify_insert'] = parse_insert(insert['literal_sql'])
    inventory = rows((root / (E + 'inventory.csv')).read_bytes())
    hits, csharp, definitions, comment_hits, active_calls = [], [], [], [], []
    needles = ('SaveReceipt2', 'Settingmqtt')
    for row in inventory:
        rel = row['path']
        if rel.endswith('.cs'):
            csharp.append(rel)
        text = cache.get(rel)
        if text is None:
            text = base.decode((root / rel).read_bytes())
        if rel.endswith('.cs'):
            for i, line in enumerate(text.splitlines(), 1):
                if re.search(r'\bclass\s+Receipt\b', line):
                    definitions.append({'path': rel, 'line': i, 'text': line.strip()})
        if not any(n.casefold() in text.casefold() for n in needles):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for needle in needles:
                if needle.casefold() in line.casefold():
                    hits.append({'path': rel, 'line': i, 'needle': needle})
        if rel.endswith('.cs') and 'SaveReceipt2' in text:
            parsed = base.Syntax(text)
            for n in base.walk(parsed.tree.root_node):
                if n.type == 'comment' and 'SaveReceipt2' in parsed.text(n):
                    comment_hits.append({'path': rel, 'line': n.start_point.row + 1, 'text': parsed.text(n)})
                if n.type == 'invocation_expression':
                    f = parsed.text(n.child_by_field_name('function'))
                    if f.rsplit('.', 1)[-1] == 'SaveReceipt2':
                        owner = prior.member_owner(parsed, n)
                        active_calls.append({'path': rel, 'line': n.start_point.row + 1,
                            'function_syntax': f, 'owner': parsed.text(owner.child_by_field_name('name')),
                            'compiler_bound_target': False})
    result['discovery'] = {'inventory_paths_scanned': len(inventory), 'csharp_paths_count': len(csharp),
        'inventory_includes_tracked_binary_and_generated_paths_not_827_CSharp_sources': True,
        'needle_occurrences': hits, 'active_SaveReceipt2_literal_invocations': active_calls,
        'SaveReceipt2_comment_occurrences': comment_hits,
        'class_Receipt_definition_spelling_hits_in_CSharp_paths': definitions,
        'absence_search_is_not_model_contract_or_alias_reflection_completeness': True,
        'whole_inventory_human_semantic_read_claimed': False}
    return result


def source_errors(facts):
    errors = []
    def need(ok, label):
        if not ok:
            errors.append('source:' + label)
    def m(rel, sel):
        return method(facts, rel, sel)
    def has(rel, sel, *parts):
        text = prior.norm(m(rel, sel)['syntax_text'])
        return all(prior.norm(s) in text for s in parts)
    ins, upd = facts['sql_fields']['InsertReceipt'], facts['sql_fields']['UpdateReceipt']
    need(len(ins['placeholder_names']) == 29 and '@Recipient' in ins['placeholder_names']
         and '@Recipient' in upd['placeholder_names'], 'receipt-query-placeholders')
    two = m(RO, 'SaveReceipt2')
    need([r['text'] for r in two['query_references']] == ['StoredQueries.InsertReceipt'], 'save2-selects-insert-not-update')
    b = facts['bridges']['SaveReceipt2']
    need(b['literal_add_count'] == 28 and b['casefold_only_missing'] == ['@Recipient']
         and set(b['case_only_spelling_differences']) == {'@BankId', '@State'}, 'save2-only-recipient-omission-under-casefold')
    for sel in ('SaveReceipt', 'ReadReceiptOnline'):
        need(facts['bridges'][sel]['literal_add_count'] == 29
             and facts['bridges'][sel]['casefold_only_missing'] == []
             and has(RO, sel, '"@Recipient"', 'Receipt.Recipient'), 'recipient-counterexample:' + sel)
    need(two['return_type'] == 'bool' and len(calls(two, '.BeginTransaction')) == 1
         and len(calls(two, '.Commit')) == 1 and len(calls(two, '.Rollback')) == 1
         and len(calls(two, '.Open')) == len(calls(two, '.ExecuteNonQuery')) == 1 and bool(two['try_regions'])
         and calls(two, '.Open')[0]['line'] < two['try_regions'][0]['start']
         and calls(two, '.BeginTransaction')[0]['line'] < two['try_regions'][0]['start']
         and calls(two, '.ExecuteNonQuery')[0]['line'] < calls(two, '.Commit')[0]['line']
         and has(RO, 'SaveReceipt2', 'result = true;', 'result = false;', 'return result;', 'sqlConnection.Close();'),
         'save2-written-flow-not-always-false-or-never-throws-proof')
    active = facts['discovery']['active_SaveReceipt2_literal_invocations']
    need(len(active) == 4 and {r['path'] for r in active} == set(RESTORERS)
         and all(r['owner'] == 'RestorePreviousReceipt' for r in active), 'four-active-restore-callers-not-comment')
    need(len(facts['discovery']['SaveReceipt2_comment_occurrences']) == 1, 'comment-not-a-fifth-invocation')
    for rel, table in RESTORERS.items():
        row = m(rel, 'RestorePreviousReceipt')
        read, delete = commands(row, 'SELECT')[0], commands(row, 'DELETE')[0]
        sql = static_sql_text(delete)
        need(len(calls(row, 'SaveReceipt2')) == 1 and table in static_sql_text(read)
             and 'branch' in static_sql_text(read).casefold()
             and re.search(r'where\s+id\s*=', sql, re.I) is not None
             and 'branch' not in sql.casefold() and 'globalid' not in sql.casefold()
             and any(g['kind'] == 'if' and prior.norm(g.get('condition', '')) in ('saved', 'newReceiptOper().SaveReceipt2(receipt)')
                     for g in delete['ancestors']), 'restore-conditional-delete-and-key-scope:' + table)
    need(has(MC, 'ConnObj', 'conn = new SqlConnection(connstr);', 'return conn;'), 'connection-factory-new-object-not-shared-transaction')
    save = m(FS, 'insert_SettingNotify')
    check, delete, insert = commands(save, 'select')[0], commands(save, 'delete')[0], commands(save, 'INSERT')[0]
    need(prior.norm(check['literal_sql']).casefold() == 'select*fromsettingmqttwheredb=@db'
         and prior.norm(delete['literal_sql']).casefold() == 'deletefrom[dbo].[settingmqtt]wheredb=@db'
         and check['line'] < delete['line'] < insert['line']
         and [(r['function'], r['name_literal'], prior.norm(r['arguments'][1])) for r in save['parameter_adds']
              if r['function'].startswith(('checkCommand.', 'deleteCommand.'))] == [
                  ('checkCommand.Parameters.AddWithValue', '@DB', 'CmbTxtDataBase.Text.Trim()'),
                  ('deleteCommand.Parameters.AddWithValue', '@DB', 'CmbTxtDataBase.Text.Trim()')]
         and any(g['kind'] == 'if' and prior.norm(g['condition']) == 'existingTable.Rows.Count>0' for g in delete['ancestors']),
         'notify-conditional-db-replacement')
    need(all(len(c['arguments']) == 2 for c in (check, delete, insert))
         and not calls(save, '.BeginTransaction') and not calls(save, '.Rollback')
         and has(FS, 'EnsureConnectionOpen', 'sqlConnection.Open();')
         and not calls(m(FS, 'EnsureConnectionOpen'), '.BeginTransaction'), 'notify-no-selected-explicit-transaction-not-ambient-proof')
    info = facts['notify_insert']
    added = [r['name_literal'] for r in save['parameter_adds'] if r['function'] == 'insertCommand.Parameters.AddWithValue']
    need(info['column_count'] == info['parameter_count'] == len(added) == 22
         and info['bracketed_column_count_not_total'] == 16 and len(save['parameter_adds']) == 24
         and added == info['parameters'] and [s.casefold() for s in info['columns']] == [s[1:].casefold() for s in info['parameters']],
         'notify-22-columns-22-insert-adds-24-total-not16-or23')
    need(has(FS, 'insert_SettingNotify', '"@BranchId", CmbBranchMqtt.SelectedValue ?? 0',
             '"@pwd", pwdtxt.Text ?? string.Empty', '"@passcode", txtpasscode.Text?.Trim() ?? string.Empty')
         and has(FS, 'insert_SettingNotify', 'catch (Exception ex)', 'MessageBox.Show(ex.Message', 'conn.Close();')
         and save['return_type'] == 'void', 'notify-selected-values-caught-void-result')
    btn = m(FS, 'BtnConnect_Click')
    need(has(FS, 'BtnConnect_Click', 'if (!checkPwdWindow.Iscorrect)', 'CmbBranchMqtt.SelectedValue == null',
             'insert_SettingNotify();', 'btnconnectit.Content = "تم الاتصال بنجاح";', 'ReceivedData.LoadReceived(ConnectBroker.connString);')
         and calls(btn, 'insert_SettingNotify')[0]['line'] < next(r['line'] for r in btn['assignments'] if r['left'] == 'btnconnectit.Content')
         and has(FS, 'RegisterEvents', 'btnconnectit.Click += BtnConnect_Click;')
         and has(FS, 'ctor:frmSettings', 'conn = MainClass.ConnObj();', 'RegisterEvents();'), 'notify-caller-success-after-void-not-persistence-acceptance')
    loadrow = m(FS, 'LoadSettingNotify')
    sql = next(c['literal_sql'] for c in commands(loadrow, 'SELECT') if 'FROM [Settingmqtt]' in c['literal_sql'])
    need('where' not in sql.casefold() and 'order by' not in sql.casefold()
         and has(FS, 'LoadSettingNotify', 'if (reader.Read())', 'CmbBranchMqtt.SelectedValue = reader["BranchId"];')
         and has(FS, 'frmUserSettings_Load', 'LoadSettingNotify();'), 'settings-first-unfiltered-notify-row')
    connrow = m(UL, 'ConnectMQTList')
    need(commands(connrow, 'select')[0]['literal_sql'].casefold() == 'select * from settingmqtt'
         and has(UL, 'ConnectMQTList', 'ElementAtOrDefault(0)', 'if (Home._is_active)', 'row["pwd"]', 'ConnectBroker._syncItems')
         and not any('BranchId' in r['right'] for r in connrow['assignments']), 'mqtt-first-row-no-selected-branch-filter')
    need(has(UL, 'CheckMqttStat', 'select * from Settingmqtt where is_active=1', 'return true;', 'return false;')
         and has(UL, 'LoadBranches', 'if (CheckMqttStat() && !Sync.CheckBranchSync())',
             'select isNull(BranchId,0) as id from Settingmqtt', 'branchId = Convert.ToInt32(dtMqtt.Rows[0][0]);')
         and has(UL, 'Login', 'if (!loginSuccess) return;', 'ConnectMQTList();'), 'login-any-active-versus-first-branch-row-not-ACL')
    for key, count in (('mqtt-base-create', 23), ('mqtt-guarded-create', 19)):
        text = facts['text_ranges'][key]['text']
        cols = re.findall(r'^\s*\[([A-Za-z_][A-Za-z0-9_]*)\]\s*\[', text, re.M)
        need(len(cols) == count and 'BranchId' in cols and 'DB' in cols
             and '[id] ASC' in text and 'UNIQUE' not in text.upper(), 'available-schema-not-db-branch-singleton:' + key)
    need(re.search(r'ALTER\s+TABLE\s+Receipts\s+Add\s+Recipient\s+\[', facts['text_ranges']['receipt-recipient-guarded-alter']['text'], re.I) is not None
         and re.search(r'ALTER\s+TABLE\s+Settingmqtt\s+Add\s+IpServer\s+\[', facts['text_ranges']['mqtt-ip-guarded-alter']['text'], re.I) is not None
         and all(re.search(r'ALTER\s+TABLE\s+Settingmqtt\s+Add\s+' + x + r'\s+\[?bit\b', facts['text_ranges']['mqtt-flags-guarded-alters']['text'], re.I)
                 for x in ('syncItems', 'syncOper', 'syncDefinitions')),
         'available-recipient-and-mqtt-schema-alters-not-deployment')
    need(has(RC, 'CopySettingsTablesAsync', '"Settingmqtt"', 'DROP TABLE', 'SELECT * INTO', 'await ExecuteSqlAsync(dropSql);', 'await ExecuteSqlAsync(copySql);')
         and has(RC, 'ExecuteSqlAsync', 'EnsureOpen(_conn);', 'new SqlCommand(sql, _conn)', 'catch (Exception ex)'),
         'available-maintenance-copy-not-singleton-proof')
    need('AuditorAPI' in facts['text_ranges']['external-model-reference']['text']
         and 'using AuditorAPI.Models;' in facts['text_ranges']['receipt-model-namespace']['text']
         and facts['discovery']['class_Receipt_definition_spelling_hits_in_CSharp_paths'] == [], 'external-model-defaults-not-inferred-from-property-use')
    need(facts['application_execution_count'] == 0 and facts['runtime_or_all_ingress_or_model_defaults_certified'] is False
         and facts['extraction_equals_reading'] is False, 'bounded-static-not-runtime-or-reading-proof')
    return errors


def basis_errors(bases, facts):
    errors = []
    for r in bases:
        rel = r.get('path')
        if 'selector' in r:
            row = facts['methods'].get(rel, {}).get(r['selector'], {})
            keys = ('start', 'end', 'syntax_utf8_sha256')
        elif 'query' in r:
            row = facts['sql_fields'].get(r['query'], {})
            keys = ('start', 'end', 'syntax_utf8_sha256')
        else:
            row = facts['text_ranges'].get(r.get('text_range_key'), {})
            keys = ('start', 'end', 'decoded_range_utf8_sha256')
        if not row or row.get('path', rel) != rel or any(r.get(k) != row.get(k) for k in keys):
            errors.append('evidence:source-basis:' + str(rel))
    return errors


def preservation_errors(entry=None, root=ROOT):
    entry = entry or load(ENTRY)
    hydration = load(HYDRATION)
    errors = []
    def need(ok, label):
        if not ok:
            errors.append('preservation:' + label)
    application = hydration['application_sources']
    need(len(application) == 827, '827-inventoried-application-paths')
    for rel, pin in application.items():
        actual = identity(rel, root)
        need(all(actual[k] == pin[k] for k in ('bytes', 'sha256')), 'application:' + rel)
    expected_files = entry['published_audit_file_identities']
    need(len(expected_files) == 1686, 'published1686-entry')
    for rel, pin in expected_files.items():
        if rel == ORIGINAL_FINDINGS['path']:
            need(identity(rel, root) == ORIGINAL_FINDINGS, 'restored-original335-raw-bytes')
            continue
        raw = (root / rel).read_bytes()
        if rel in INDEXES and (len(raw) != pin['bytes'] or sha(raw) != pin['sha256']):
            need(raw.startswith('# الحالة الحالية — 07B39R11'.encode('utf8'))
                 and len(raw) > pin['bytes'] and sha(raw[-pin['bytes']:]) == pin['sha256'], 'index-verbatim-suffix:' + rel)
        else:
            need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'published-audit:' + rel)
    archive = entry['remote_R10_frozen_archive']
    need(identity(archive['path'], root) == {k: archive[k] for k in ('path', 'bytes', 'sha256')}, 'remote-seven-archive')
    with tarfile.open(root / archive['path'], 'r:gz') as tar:
        need(sorted(tar.getnames()) == sorted(archive['member_paths']) and len(tar.getmembers()) == 7, 'seven-exact-members')
        for pin in entry['remote_R10_frozen_members']:
            stream = tar.extractfile(pin['path'])
            with stream:
                raw = stream.read()
            need(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'remote-member:' + pin['path'])
    ds = dictionary_rows(root)
    need(len(ds) == 339 and len({r['id'] for r in ds}) == 339, '335-plus-R1-four-not341-or345')
    need(len(rows((root / ORIGINAL_FINDINGS['path']).read_bytes())) == 335, '335-canonical-register')
    by_id = {r['id']: r for r in ds}
    for collision in entry['remote_root_id_collisions']:
        need(by_id[collision['id']] == collision['existing_R1_dictionary']
             and collision['remote_R10_dictionary'] != collision['existing_R1_dictionary'], 'R1-ID-not-reused:' + collision['id'])
    need(entry['prior_local_R10']['actual_objects_or_files_available'] is False
         and entry['prior_local_R10']['reported_578_tests_are_current_recovered_capture'] is False, 'missing-local-R10-not-recertified')
    restore = load(RESTORATION)
    need(restore['after'] == {**{k: ORIGINAL_FINDINGS[k] for k in ('bytes', 'sha256')}, 'rows': 335}
         and restore['remote_new_root_numbers_adopted'] is False
         and restore['remote_questions_semantically_rejected_just_because_ID_collision'] is False, 'explicit-prospective-restoration')
    return errors


def evidence_errors(ev=EV, facts=None):
    facts = facts or load(FACTS, ev)
    errors = []
    def need(ok, label):
        if not ok:
            errors.append('evidence:' + label)
    read, review, ledger, date = (load(n, ev) for n in (READS, REVIEW, LEDGER, DATE_NOTE))
    for name, obj in ((READS, read), (REVIEW, review), (LEDGER, ledger)):
        need(obj.get('assessment_reference_date_utc') == DATE and obj.get('raw_clocks_are_calendar_authority') is False, 'prospective-reference-only:' + name)
        need(obj.get('application_execution_count') == 0 and obj.get('whole_7B_static_assessment_complete') is False
             and obj.get('capability_exit_certificates_issued') == obj.get('four_family_exit_certificates_issued') == obj.get('new_accepted_external_handoffs') == 0
             and obj.get('phase7C_started') is False and obj.get('phase8_authorized') is False, '7B-only-open-scope:' + name)
        for pin in obj.get('pinned_inputs', []):
            need(identity(pin['path']) == pin, 'input-pin:' + pin['path'])
    expected = {(rel, s) for rel, sels in CONTEXTS.items() for s in sels}
    actual = [(r.get('path'), r.get('selector')) for r in read.get('selected_method_reviews', [])]
    need(len(actual) == len(expected) and set(actual) == expected, 'selected-body-review-coverage-not-reading-proof')
    need(read.get('extraction_equals_reading') is False and read.get('independent_human_review_claimed') is False
         and read.get('raw_source_display_streams_preserved') is False and read.get('individual_read_timestamps_invented') is False
         and read.get('lost_R10_97_contexts_reconstructed') is False, 'honest-source-review-provenance')
    for r in read.get('selected_method_reviews', []):
        need(bool(r.get('bounded_semantic_review')) and bool(r.get('not_established')), 'method-specific-reason:' + str(r.get('selector')))
        errors += basis_errors([r], facts)
    questions = review.get('source_questions', [])
    need(tuple(r.get('id') for r in questions) == QUESTION_IDS, 'six-nonnumbered-questions')
    for r in questions:
        need(r.get('new_numbered_finding_id') is None and r.get('novelty_certified') is False
             and r.get('observed_provider_or_financial_failure') is False and r.get('accepted_external_handoff') is False
             and all(r.get(k) for k in ('source_disposition', 'counterevidence_and_limits', 'remaining_readable_local', 'source_basis')), 'bounded-question:' + r.get('id', '?'))
        errors += basis_errors(r.get('source_basis', []), facts)
    by_id = {r['id']: r for r in dictionary_rows()}
    compared = review.get('focused_root_comparisons', [])
    need({r.get('id') for r in compared} == set(FOCUSED_ROOTS) and len(compared) == len(FOCUSED_ROOTS), '17-explicit-dictionary-comparisons')
    for r in compared:
        need(r.get('canonical_dictionary_verbatim') == by_id.get(r.get('id'))
             and bool(r.get('comparison_reason')) and r.get('canonical_fields_rewritten') is False
             and r.get('automatic_equivalence_or_novelty') is False, 'root-dictionary-and-qualified-comparison:' + r.get('id', '?'))
    need(review.get('remote_scope_claims_adopted_as_authorization') is False
         and review.get('remote_R10_verifier_executed') is False
         and review.get('all339_semantically_reread') is False and review.get('all345_roots_screened') is False
         and review.get('new_finding_ids') == [] and review.get('lost_local_R10_578_recertified') is False,
         'no-remote-authorization-or-lost-evidence-adoption')
    canonical = {r['id']: r for r in base.rows('capability-register-07B38.csv')}
    caps = ledger.get('capabilities', [])
    need(len(caps) == 26 and {r.get('capability_id') for r in caps} == set(canonical), '26-canonical-capabilities')
    old = load('capability-reconciliation-rev02-07B39R9.json')
    old_caps = {r['capability_id']: r for r in old['capabilities']}
    for r in caps:
        cid = r.get('capability_id')
        need(r.get('canonical_row_verbatim') == canonical.get(cid)
             and r.get('prior_R9_record_canonical_json_sha256') == sha(json.dumps(old_caps.get(cid), ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf8'))
             and r.get('whole_capability_certified') is False and r.get('local_semantic_obligations_complete') is False
             and r.get('readable_local_externalized') is False and bool(r.get('current_nonexit_reason'))
             and bool(r.get('remaining_local_obligation')), 'independent-open-carry:' + str(cid))
    need(ledger.get('original37_R9_ancestry_verbatim') == old['B37_canonical_ancestry_rows']
         and ledger.get('preserved_R8_ancestry_object_verbatim') == old['preserved_R8_ancestry_object_verbatim']
         and ledger.get('original_R6_read_flags_rewritten') is False, '37-and-R6-flags-preserved')
    families = ledger.get('family_nonexit_decisions', [])
    need(len(families) == 4 and {r.get('family') for r in families} == {'R1', 'R2', 'R3', 'R4'}, 'four-families-still-open')
    old_f = {r['family']: r for r in old['independently_authored_R9_family_nonexit_decisions']}
    for r in families:
        need(r.get('prior_R9_record_verbatim') == old_f.get(r.get('family'))
             and r.get('certificate_issued') is False and r.get('accepted_completion_handoff') is False
             and bool(r.get('current_source_backed_nonexit_reason')), 'family-preserved-and-nonexit:' + str(r.get('family')))
    for r in review.get('unavailable_contracts_not_accepted_as_handoffs', []):
        need(all(r.get(k) for k in ('source_basis', 'owner_role', 'required_redacted_input', 'absence_impact', 'next_action', 'static_disposition', 'readable_local_not_delegated'))
             and r.get('accepted_external_handoff') is False, 'individually-qualified-boundary:' + r.get('id', '?'))
        errors += basis_errors(r.get('source_basis', []), facts)
    for r in ledger.get('remaining_local_tasks', []):
        need(r.get('externalized') is False and bool(r.get('owner_role')) and bool(r.get('next_action'))
             and bool(r.get('source_or_prior_evidence')), 'locally-owned-task:' + r.get('id', '?'))
    need(len(ledger.get('remaining_local_tasks', [])) >= 8, 'remaining-local-not-erased')
    need(date.get('prospective_session_reference_date_utc') == DATE
         and date.get('frozen_dates_or_raw_clocks_authenticate_chronology') is False
         and date.get('old_executed_files_relabelled') is False, 'date-not-chronology-attestation')
    return errors


def verify(rederive=False):
    facts = load(FACTS)
    errors = []
    for rel, pin in facts['source_identity'].items():
        if identity(rel) != pin:
            errors.append('source:identity:' + rel)
    if rederive and derive() != facts:
        errors.append('source:fresh-rederivation-differs')
    errors += source_errors(facts) + preservation_errors() + evidence_errors(facts=facts)
    return {'schema_version': 1, 'errors': errors,
        'fresh_selected_method_contexts': sum(map(len, CONTEXTS.values())),
        'selected_source_file_identities': len(facts['source_identity']),
        'active_SaveReceipt2_literal_invocations': len(facts['discovery']['active_SaveReceipt2_literal_invocations']),
        'nonnumbered_source_questions': len(QUESTION_IDS), 'focused_dictionary_comparisons': len(FOCUSED_ROOTS),
        'canonical_capabilities_preserved': 26, 'canonical_ancestry_rows_preserved': 37, 'open_families': 4,
        'available_dictionary_rows': 339, 'new_numbered_findings': 0,
        'application_execution_count': 0, 'whole_7B_static_assessment_complete': False,
        'capability_exit_certificates_issued': 0, 'four_family_exit_certificates_issued': 0,
        'new_accepted_external_handoffs': 0, 'phase7C_started': False, 'phase8_authorized': False,
        'lost_local_R10_578_recertified': False,
        'limit': 'Static audit consistency only; not reading, chronology, provider/runtime behavior, authorization or financial acceptance.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--derive', action='store_true')
    parser.add_argument('--rederive', action='store_true')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.derive:
            if args.require_complete:
                raise ValueError('Derivation is not a completion gate')
            facts = derive()
            exclusive_json(EV / FACTS, facts)
            result = {'written': E + FACTS, 'source_assertion_errors': source_errors(facts)}
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return int(bool(result['source_assertion_errors']))
        result = verify(args.rederive)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({'errors': [f'{type(exc).__name__}: {exc}'], 'whole_7B_static_assessment_complete': False}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 2 if args.require_complete else 0


if __name__ == '__main__':
    sys.exit(main())
