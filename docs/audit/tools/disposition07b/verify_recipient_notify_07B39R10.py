#!/usr/bin/env python3
"""R10 source guards: SaveReceipt2 @Recipient omission + Settingmqtt notify save/delete contract.

Read-only C# lexical facts for two root adjudications, not compilation, ERP,
SQL, WPF, provider, migration, SDK, authorization or financial acceptance.
Parameter-name comparisons are literal text extraction; they do not certify
SqlClient binding, deployed schema, types, whitespace handling, or runtime
execution. All prior consumed files, failures and missing-history limits are
preserved unchanged.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
C = ROOT / 'SmartAuditERP'
P = C / 'Form_WPF'
EV = ROOT / 'docs' / 'audit' / 'evidence'
TAG = '07B39R10'

SQ = (C / 'Class' / 'StoredQueries.cs').read_text(encoding='utf-8-sig')
RO = (C / 'Class' / 'ReceiptOper.cs').read_text(encoding='utf-8-sig')
FS = (P / 'frmSettings.xaml.cs').read_text(encoding='utf-8-sig')
UL = (P / 'frmUserLogin.xaml.cs').read_text(encoding='utf-8-sig')
CALLER_FILES = {
    'frmSandD': (P / 'frmSandD.xaml.cs').read_text(encoding='utf-8-sig'),
    'frmSandSD': (P / 'frmSandSD.xaml.cs').read_text(encoding='utf-8-sig'),
    'frmSandQD': (P / 'frmSandQD.xaml.cs').read_text(encoding='utf-8-sig'),
    'frmSandQAndroid': (P / 'frmSandQAndroid.xaml.cs').read_text(encoding='utf-8-sig'),
}


def lines(text):
    return text.split('\n')


def find_line(text, needle, start=0):
    for i, l in enumerate(lines(text)):
        if i >= start and needle in l:
            return i + 1
    return None


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def body(text, start_pat, end_pat):
    m = re.search(start_pat, text)
    if not m:
        return None, None, None
    start = m.start()
    m2 = re.search(end_pat, text[start:])
    end = start + (m2.end() if m2 else 0)
    return text[start:end], lines(text[:start]).__len__() + 1, sha(text[start:end])


# ReceiptOper.cs uses TABs (method close = '\n\t\t}\n');
# frmSettings.xaml.cs uses 8 spaces (method close = '\n        }\n').
RO_END = r'\n\t\t\}\n'
FS_END = r'\n        \}\n'


facts = {'schema_version': 1, 'tag': TAG, 'read_only': True,
         'application_execution_count': 0}

# ── 1) InsertReceipt / UpdateReceipt required parameter names ──
ins_m = re.search(r'InsertReceipt\s*=\s*"([^"]*)"', SQ)
upd_m = re.search(r'UpdateReceipt\s*=\s*"([^"]*)"', SQ)
ins_sql = ins_m.group(1) if ins_m else ''
upd_sql = upd_m.group(1) if upd_m else ''
ins_params = sorted(set(re.findall(r'@([A-Za-z_][A-Za-z0-9_]*)', ins_sql)))
upd_params = sorted(set(re.findall(r'@([A-Za-z_][A-Za-z0-9_]*)', upd_sql)))
facts['insert_receipt'] = {
    'unique_parameter_names': ins_params,
    'count': len(ins_params),
    'contains_Recipient': 'Recipient' in ins_params,
    'utf8_sha256_of_query_literal': sha(ins_sql),
}
facts['update_receipt'] = {
    'unique_parameter_names': upd_params,
    'count': len(upd_params),
    'contains_Recipient': 'Recipient' in upd_params,
}

# ── 2) SaveReceipt2 body parameter adds ──
sr2, sr2_line, sr2_hash = body(
    RO, r'public bool SaveReceipt2\(Receipt Receipt\)', RO_END)
sr2_params = re.findall(r'Parameters\.Add\("(@[A-Za-z_][A-Za-z0-9_]*)"', sr2 or '')
sr2_names = sorted({p.lstrip('@') for p in sr2_params})
facts['save_receipt2'] = {
    'body_start_line': sr2_line,
    'body_utf8_sha256': sr2_hash,
    'parameters_added': len(sr2_params),
    'unique_names': sr2_names,
    'adds_Recipient': any(p == '@Recipient' for p in sr2_params),
    'uses_query': 'StoredQueries.InsertReceipt' in (sr2 or ''),
    'execute_line': find_line(RO, 'ExecuteNonQuery()', sr2_line),
}

# ── 3) SaveReceipt v1 and the sync site DO add @Recipient ──
sr1, sr1_line, _ = body(
    RO, r'public bool SaveReceipt\(Receipt Receipt, Entry Entr, bool IsNew\)', RO_END)
sr1_has = '@Recipient' in (sr1 or '')
sr1_line_rec = find_line(sr1 or '', '"@Recipient"')
facts['save_receipt_v1'] = {
    'body_start_line': sr1_line,
    'adds_Recipient': sr1_has,
    'relative_recipient_add_line': sr1_line_rec,
    'reads_model_property_Recipient': bool(re.search(r'Receipt\.Recipient', sr1 or '')),
}
sync_start = find_line(RO, 'StoredQueries.UpdateReceipt', 500)
sync_has = False
sync_rec_line = None
if sync_start:
    window = '\n'.join(lines(RO)[sync_start - 1:sync_start + 35])
    sync_has = '"@Recipient"' in window
    sync_rec_line = find_line(window, '"@Recipient"')
facts['sync_import_site'] = {
    'query_selection_line': sync_start,
    'adds_Recipient_within_35_lines': sync_has,
    'relative_recipient_add_line': sync_rec_line,
    'reads_model_property_Recipient': bool(
        re.search(r'Receipt\.Recipient', '\n'.join(lines(RO)[sync_start - 1:sync_start + 35]))
    ) if sync_start else None,
}

# ── 4) SaveReceipt2 call sites ──
callers = {}
for name, text in CALLER_FILES.items():
    hits = [i + 1 for i, l in enumerate(lines(text)) if 'SaveReceipt2(' in l]
    callers[name] = hits
facts['save_receipt2_call_sites'] = callers

# ── 5) insert_SettingNotify contract ──
isn, isn_line, isn_hash = body(
    FS, r'public void insert_SettingNotify\(\)', FS_END)
isn_text = isn or ''
facts['insert_setting_notify'] = {
    'body_start_line': isn_line,
    'body_utf8_sha256': isn_hash,
    'checks_existing_by': 'where DB=@DB' in isn_text,
    'delete_statement': 'delete from [dbo].[Settingmqtt] where DB=@DB' in isn_text,
    'delete_filters_branch': bool(re.search(
        r'delete[^"]*BranchId', isn_text, re.I)),
    'insert_column_count': (re.search(
        r'INSERT INTO \[dbo\]\.\[Settingmqtt\](.*?)VALUES', isn_text, re.S).group(1)
        .count('[') if 'INSERT INTO' in isn_text else 0),
    'addwithvalue_count': len(re.findall(r'AddWithValue\("(@[A-Za-z_][A-Za-z0-9_]*)"', isn_text)),
    'inserts_branchid': '"@BranchId"' in isn_text,
    'has_transaction': 'BeginTransaction' in isn_text,
    'plaintext_pwd_column_written': '"@pwd"' in isn_text,
    'delete_then_insert_no_rollback_window': (
        'delete from' in isn_text.lower() and 'INSERT INTO' in isn_text
        and 'BeginTransaction' not in isn_text),
}

# ── 6) Settingmqtt consumers in login flow ──
cml_start = find_line(UL, 'public void ConnectMQTList()')
cml_text = '\n'.join(lines(UL)[cml_start - 1:cml_start + 40])
facts['connect_mqt_list'] = {
    'start_line': cml_start,
    'select_all_no_branch_filter': 'select * from Settingmqtt' in cml_text,
    'reads_first_row_only': 'ElementAtOrDefault(0)' in cml_text,
    'reads_branchid_column': 'BranchId' in cml_text,
    'reads_pwd_column': bool(re.search(r'row\["pwd"\]', cml_text)),
}
facts['check_mqtt_stat'] = {
    'line': find_line(UL, 'private bool CheckMqttStat()'),
    'filters_is_active_only': 'Settingmqtt where is_active=1' in UL,
}
facts['branchid_read'] = {
    'line': find_line(UL, 'BranchId,0) as id from Settingmqtt'),
}

# ── 7) adjudication summary (lexical only) ──
# SQL Server parameter matching is case-insensitive; compare accordingly.
ins_lower = {p.lower(): p for p in ins_params}
sr2_lower = {p.lower() for p in sr2_names}
missing_ci = sorted(ins_lower[k] for k in ins_lower.keys() - sr2_lower)
case_only = sorted(
    ins_lower[k] for k in ins_lower.keys() & sr2_lower
    if ins_lower[k] not in sr2_names)
facts['adjudication_lexical'] = {
    'insert_required_minus_save2_added_case_insensitive': missing_ci,
    'case_only_spelling_differences_present': case_only,
    'save2_always_throws_at_execute_lexical_expectation':
        'Recipient' in missing_ci,
    'model_property_exists_via_v1_and_sync_reads':
        facts['save_receipt_v1']['reads_model_property_Recipient'] is True
        and facts['sync_import_site']['reads_model_property_Recipient'] is True,
    'new_root_proposals': [
        {'id': 'P7-164',
         'title': 'SaveReceipt2 omits the @Recipient parameter required by '
                  'InsertReceipt/UpdateReceipt so every legacy receipt '
                  'restore save fails at ExecuteNonQuery with rollback and '
                  'the conditional legacy-row delete never runs',
         'severity': 'High', 'certainty': 'confirmed',
         'type': 'implementation-defect', 'next_phase': '8'},
        {'id': 'P7-165',
         'title': 'MQTT notify settings save deletes the Settingmqtt row by '
                  'DB then re-inserts without a transaction; a failed insert '
                  'after a successful delete leaves the database without '
                  'notify settings, and consumers read the first row with no '
                  'branch filter',
         'severity': 'Medium', 'certainty': 'confirmed',
         'type': 'implementation-defect', 'next_phase': '8'},
    ],
    'not_certified': ['SqlClient binding', 'deployed schema', 'runtime execution',
                      'WPF lifecycle', 'provider behavior', 'financial acceptance'],
}

out = EV / ('recipient-notify-contract-' + TAG + '.json')
out.write_text(json.dumps(facts, ensure_ascii=False, indent=1) + '\n',
               encoding='utf-8')
print(json.dumps({
    'written': str(out.relative_to(ROOT)),
    'insert_params': facts['insert_receipt']['count'],
    'save2_params': facts['save_receipt2']['parameters_added'],
    'missing_from_save2': missing_ci,
    'save2_call_sites': callers,
    'notify_has_transaction': facts['insert_setting_notify']['has_transaction'],
    'notify_delete_filters_branch': facts['insert_setting_notify']['delete_filters_branch'],
    'first_row_only_reader': facts['connect_mqt_list']['reads_first_row_only'],
}, ensure_ascii=False, indent=1))
