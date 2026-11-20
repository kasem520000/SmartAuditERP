#!/usr/bin/env python3
"""B27/R4k INERT invoice-search predicate/selection illustrations, not ERP tests.

Only supplied records and explicit handler calls are modeled. No SQL/DataView
parser, WPF scheduling, SDK constructor, database state, permission, acceptance,
remediation or saved-loss execution. GlobalID is retained: not the local-number
identity loss of061. Caller eligibility is not a deployed ACL certificate.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
P = 'SmartAuditERP/Form_WPF/'
C = 'SmartAuditERP/Class/'
SOURCE_SLICES = {
    P + 'frmInvoiceSrch.xaml.cs': [(1, 698)],
    P + 'frmInvoiceSrch.xaml': [(1, 561)],
    P + 'frmInventoryTransfer.xaml.cs': [(402, 453), (1642, 1686)],
    P + 'frmInventoryTransfer.xaml': [(485, 505), (1465, 1475)],
    P + 'frmInvPurch.xaml.cs': [(65, 84), (481, 548), (2641, 2662)],
    P + 'frmInvPurch.xaml': [(1325, 1335)],
    C + 'InvoiceOper.cs': [(3219, 3290)],
}


def integer(n, low=0, high=30):
    if type(n) is not int or not low <= n <= high:
        raise ValueError('Exact bounded fixture integer required, not bool/enum/SQL conversion')
    return n


def records():
    def row(gid, kind, proc, status=1, day=2, branch=1, deleted=False, local_id=7):
        return dict(global_id=gid, kind=kind, proc=proc, status=status, day=day,
                    branch=branch, deleted=deleted, local_id=local_id, pay=1)
    return [row('T_SEND', 8, 2), row('T_OK', 8, 1), row('T_NOT_ELIGIBLE', 8, 1, status=0),
            row('T_OTHER_DAY', 8, 1, day=7), row('P_REQUESTED', 1, 1), row('A_TYPE20', 20, 1),
            row('T_OTHER_BRANCH', 8, 1, branch=2), row('T_DELETED', 8, 1, deleted=True),
            row('C_TYPE23', 23, 1)]


def checked(data):
    if not isinstance(data, list):
        raise ValueError('Explicit supplied record list required')
    fields = {'global_id', 'kind', 'proc', 'status', 'day', 'branch', 'deleted', 'local_id', 'pay'}
    for r in data:
        if not isinstance(r, dict) or set(r) != fields:
            raise ValueError('Exact supplied record shape required; no external DTO defaults')
        gid = r['global_id']
        if not isinstance(gid, str) or not 1 <= len(gid) <= 64 or not all(c.isascii() and (c.isalnum() or c == '_') for c in gid):
            raise ValueError('Synthetic non-secret GlobalID token required')
        for k in ('kind', 'proc', 'status', 'day', 'branch', 'local_id'):
            integer(r[k], 0 if k == 'status' else 1)
        integer(r['pay'], -1)
        if type(r['deleted']) is not bool:
            raise ValueError('Exact fixture deletion bool required')
    if len({r['global_id'] for r in data}) != len(data):
        raise ValueError('Unique supplied GlobalIDs; no deployed uniqueness assertion')
    return copy.deepcopy(data)


def condition_after(action, cond):
    if cond not in ('empty', 'caller-status1', 'dates'):
        raise ValueError('Explicit condition SOURCE kind, never arbitrary SQL')
    if action not in ('unchanged', 'from-date', 'to-date', 'clear'):
        raise ValueError('Only explicit selected handler actions')
    return 'dates' if action in ('from-date', 'to-date') else 'empty' if action == 'clear' else cond


def source_rows(data, requested_type, server_proc, branch=1, cond='empty', window=(2, 2)):
    """Predicate-subset illustration of BuildLoadQuery, NOT a SQL interpreter."""
    data = checked(data)
    integer(requested_type, 1)
    integer(server_proc, 1, 4)
    integer(branch, 1)
    condition_after('unchanged', cond)
    if type(window) is not tuple or len(window) != 2:
        raise ValueError('Explicit ordinal-day pair required; no .NET calendar semantics')
    lo, hi = window
    integer(lo, 1)
    integer(hi, lo)
    return [r for r in data if not r['deleted']
            and (r['kind'] == requested_type if requested_type == 23 else r['kind'] in (20, requested_type))
            and (requested_type == 14 or r['branch'] == branch)
            and r['proc'] == server_proc
            and (cond != 'caller-status1' or r['status'] == 1)
            and (cond != 'dates' or lo <= r['day'] <= hi)]


def display_rows(loaded, selected_proc):
    """Only the proc-type part of DataView filtering, not DataView execution."""
    integer(selected_proc, 0, 4)
    return [r for r in checked(loaded) if selected_proc == 0 or r['proc'] == selected_proc]


def result_of(row=None):
    """Selected subset actually returned to callers; no modal event execution."""
    if row is None:
        return dict(ISDone=False, InvGlobalID='-1', ProcType=1, PayType=1)
    r = checked([row])[0]
    return dict(ISDone=True, InvGlobalID=r['global_id'], ProcType=r['proc'], PayType=r['pay'])


def consumer_lookup(data, selected, branch=1):
    """Purchase/receive caller's GID+branch predicate; not actual Navigate/SQL."""
    integer(branch, 1)
    if not isinstance(selected, dict) or set(selected) != {'ISDone', 'InvGlobalID', 'ProcType', 'PayType'}:
        raise ValueError('Exact supplied selection result required')
    if type(selected['ISDone']) is not bool or not isinstance(selected['InvGlobalID'], str):
        raise ValueError('Strict supplied selection state required')
    integer(selected['ProcType'], 1, 4)
    integer(selected['PayType'], -1)
    data = checked(data)
    matches = [r for r in data if selected['ISDone'] and selected['InvGlobalID'] != '-1'
               and r['global_id'] == selected['InvGlobalID'] and r['branch'] == branch]
    return dict(supplied_where_fields=['branch', 'InvGlobalID'], matches=matches,
                reader_mapped_type=matches[0]['kind'] if matches else None,
                source_application_or_SQL_executed=False,
                no_deployed_schema_uniqueness_or_save_success_claim=True)


def build():
    sources, reads = {}, []
    for path, spans in SOURCE_SLICES.items():
        raw = (ROOT / path).read_bytes()
        lines = raw.decode('utf8').splitlines(keepends=True)
        sources[path] = lines
        for a, b in spans:
            if not 1 <= a <= b <= len(lines):
                raise ValueError('Selected text range outside source')
            reads.append(dict(path=path, start=a, end=b, encoding='strict-utf-8',
                source_sha256=hashlib.sha256(raw).hexdigest(),
                selected_text_utf8_sha256=hashlib.sha256(''.join(lines[a-1:b]).encode()).hexdigest(),
                whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True,
                whole_local_file_selected=a == 1 and b == len(lines)))
    def text(path, a, b):
        if not any(lo <= a <= b <= hi for lo, hi in SOURCE_SLICES[path]):
            raise ValueError('Observation outside declared slice')
        return ''.join(sources[path][a-1:b])
    sc, sx = P+'frmInvoiceSrch.xaml.cs', P+'frmInvoiceSrch.xaml'
    tc, tx = P+'frmInventoryTransfer.xaml.cs', P+'frmInventoryTransfer.xaml'
    pc, px, reader = P+'frmInvPurch.xaml.cs', P+'frmInvPurch.xaml', C+'InvoiceOper.cs'
    def ev(*args):
        return ';'.join(f'{p}:{a}-{b}' for p, a, b in args)
    ep = ev((sc, 73, 86), (sc, 140, 143), (sc, 336, 345), (sc, 427, 481),
            (sc, 510, 519), (sx, 229, 235), (tc, 1642, 1657), (tx, 1469, 1473))
    ec = ev((tc, 1659, 1685), (tx, 492, 497), (sc, 189, 211), (sc, 236, 254),
            (sc, 336, 345), (sc, 267, 284), (tc, 402, 453))
    et = ev((sc, 348, 408), (sc, 570, 596), (sc, 674, 690), (sc, 267, 284),
            (pc, 65, 84), (pc, 2641, 2662), (pc, 481, 502), (px, 1329, 1333), (reader, 3219, 3290))
    alg = []
    def add(root, title, result, ok, evidence, limit):
        alg.append(dict(id=f'ALG7B27-{len(alg)+1:02d}', finding_ids=root, title=title, result=result,
            illustration_assertions_passed=bool(ok), source_application_executed=False, evidence=evidence, limit=limit))
    data = records()
    transfers = [r for r in data if r['kind'] == 8]
    loaded = source_rows(transfers, 8, 2)
    r = display_rows(loaded, 1)
    add('P7-155', 'Changing selected process2 to1 cannot recover source rows', r, r == [], ep,
        'Explicit successful supplied query and handler call, not WPF event order or a real empty database.')
    r = display_rows(loaded, 0)
    add('P7-155', 'All selection still contains only server process2', r, len(r) == 1 and {x['proc'] for x in r} == {2}, ep,
        'The All option cannot broaden the already restricted snapshot; no UI/SQL run.')
    r = display_rows(loaded, 2)
    add('P7-155', 'Selecting the original process2 is a positive control', r, [x['global_id'] for x in r] == ['T_SEND'], ep,
        'Agreement for the original criterion does not validate switching criteria.')
    r = display_rows(source_rows(transfers, 8, 1), 1)
    add('P7-155', 'Fresh server process1 has the records absent from old snapshot', r, any(x['global_id'] == 'T_OK' for x in r), ep,
        'Counterfactual predicate control, not an application fix or executed reload.')
    r = source_rows(transfers, 8, 1, cond='caller-status1')
    add('P7-156', 'Initial caller eligibility excludes status0', r, 'T_NOT_ELIGIBLE' not in [x['global_id'] for x in r], ec,
        'Status meanings remain external; the caller explicitly requires the literal value1.')
    for action in ('from-date', 'to-date'):
        cond = condition_after(action, 'caller-status1')
        r = source_rows(transfers, 8, 1, cond=cond)
        add('P7-156', action+' replaces rather than combines caller predicate', dict(cond=cond, rows=r),
            any(x['global_id'] == 'T_NOT_ELIGIBLE' for x in r), ec,
            'Same156 root for both date handlers; ordinal-day fixture, not DateTime/culture/provider semantics.')
    cond = condition_after('clear', 'caller-status1')
    r = source_rows(transfers, 8, 1, cond=cond)
    add('P7-156', 'Clear removes the caller condition and reloads', dict(cond=cond, rows=r),
        any(x['status'] == 0 for x in r), ec, 'Reset of optional fields is not authorization to remove mandatory eligibility.')
    r = source_rows(transfers, 8, 1, cond='dates')
    add('P7-156', 'Branch and deletion remain guarded after Cond replacement', r,
        all(x['branch'] == 1 and not x['deleted'] for x in r), ec,
        'Positive local guards, not a deployed ACL, schema or concurrency acceptance claim.')
    add('P7-156', 'The new date condition actually filters a distinct day', r,
        all(x['day'] == 2 for x in r) and 'T_OTHER_DAY' not in [x['global_id'] for x in r], ec,
        'Only a bounded predicate contrast, not an end-of-day/timezone/.NET parser oracle.')
    purchases = source_rows(data, 1, 1)
    add('P7-157', 'A purchase type1 request also admits type20', purchases,
        {x['kind'] for x in purchases} == {1, 20}, et,
        'Supplied distinct GlobalIDs and successful source rows; no deployed access or saved mutation observed.')
    alien = next(x for x in purchases if x['kind'] == 20)
    selected = result_of(alien)
    add('P7-157', 'Selection retains GlobalID but does not carry an allowed type', selected,
        selected['ISDone'] and selected['InvGlobalID'] == 'A_TYPE20' and 'kind' not in selected, et,
        'Not061 local-number identity loss; no requirement inferred for every DTO or all callers.')
    r = consumer_lookup(data, selected)
    add('P7-157', 'Purchase consumer GID+branch lookup maps the type20 source', r,
        r['reader_mapped_type'] == 20, et,
        'Only the selected reader/type boundary, not a completed Navigate render, invoice save or loss.')
    selected_ok = result_of(next(x for x in purchases if x['kind'] == 1))
    r = consumer_lookup(data, selected_ok)
    add('P7-157', 'Requested type1 record remains a positive control', r,
        r['reader_mapped_type'] == 1, et, 'Ordinary success does not justify unconditional type20 for purchase/transfer.')
    r = source_rows(data, 23, 1)
    add('P7-157', 'Special type23 branch is exact and does not append20', r,
        len(r) == 1 and r[0]['kind'] == 23, et, 'The separate InvContratct table is a text contrast, not its schema acceptance.')
    r = consumer_lookup(data, result_of())
    add('P7-157', 'Default not-done result is not consumed', r,
        r['matches'] == [], et, 'No all-modal-path certification, actual Close/Hide behavior not executed.')
    r = consumer_lookup(data, selected, branch=2)
    add('P7-157', 'Consumer branch mismatch is a positive nonmatch control', r,
        r['matches'] == [], et, 'Does not prove deployed authorization or type/eligibility revalidation.')
    same_no = [x for x in purchases if x['local_id'] == 7]
    r = consumer_lookup(data, selected_ok)
    add('P7-157', 'Equal local numbers do not confuse the retained GlobalID lookup', r,
        len(same_no) == 2 and r['matches'][0]['global_id'] == 'P_REQUESTED', et,
        'A narrowing control distinguishing this cause from061; uniqueness is supplied, not measured.')
    lost_eligibility = next(x for x in source_rows(transfers, 8, 1, cond='dates') if x['status'] == 0)
    r = consumer_lookup(data, result_of(lost_eligibility))
    add('P7-156', 'Receive caller consumes selected GID without restoring status predicate', r,
        len(r['matches']) == 1 and r['matches'][0]['status'] == 0, ec,
        'No assertion of actual stock receipt or final save; literal caller constraint alone is established.')
    r = source_rows(data, 20, 1)
    add('P7-157', 'Request20 matches its record once despite OR20', r,
        len(r) == 1 and r[0]['kind'] == 20, et,
        'Logical OR is not UNION duplication; type20 may be intentional in specifically authorized caller contracts.')
    lexical = []
    def lex(root, title, ok, evidence, limit):
        lexical.append(dict(id=f'ST7B27-{len(lexical)+1:02d}', finding_ids=root, title=title,
            documented_text_observation_matches=bool(ok), source_application_executed=False, evidence=evidence, limit=limit))
    s = lambda a, b: text(sc, a, b)
    lex('H7B27-03', 'Local search XAML wires Loaded and key/selection handlers',
        all(t in text(sx, 1, 561) for t in ('Loaded="Window_Loaded"', 'KeyDown="Window_KeyDown"',
            'SelectionChanged="dgvItems_SelectionChanged"', 'MouseDoubleClick="dgvItems_MouseDoubleClick"')),
        ev((sx, 1, 14), (sx, 398, 425)), 'Literal wiring only, not event sequence, focus, rendering or7C lifecycle review.')
    lex('P7-155', 'SQL appends fixed public ProcType', 'condClause += $" and inv.proc_type = {ProcType}";' in s(336, 345), ep,
        'Query text and supplied integers only, not SQL execution.')
    lex('P7-155', 'Process change only applies an in-memory filter', 'ApplyFilter();' in s(140, 143)
        and 'LoadInvoices' not in s(140, 143) and 'ProcType =' not in s(140, 143), ep,
        'A selected field is not the fixed public field; does not depend on invented scheduler behavior.')
    lex('P7-155', 'Transfer options include All and two different processes',
        'Items.Add(isAr ? "الكل"' in s(427, 481) and 'case 8:' in s(427, 481)
        and 'Receive Invoice' in s(427, 481) and 'Send Transfer' in s(427, 481), ep,
        'Options exist locally, unlike unpopulated operation list120; support of every enum is not assumed.')
    lex('P7-155', 'Selected procIndex filters only the loaded table',
        'int procIndex = cmbProcType.SelectedIndex;' in s(510, 519)
        and 'conditions.Add($"proc_type = {procIndex}");' in s(510, 519)
        and 'new DataView(_masterTable)' in s(490, 507), ep,
        'No DataView expression/parser execution; fixture models the integer predicate only.')
    lex('P7-155', 'Transfer search caller starts process2 without disabling selector',
        'ProcType = 2, InvType = 8' in text(tc, 1642, 1657)
        and 'IsEnabled = false' not in text(tc, 1642, 1657), ep,
        'Selected local caller, not all callers or an assertion about external permissions/settings.')
    lex('P7-156', 'Receive caller supplies mandatory status1 before modal',
        all(t in text(tc, 1659, 1685) for t in ('frm.ProcType = 1;', 'frm.InvType = 8;',
            'frm.Cond += " AND InvoiceStatus = 1";', 'frm.cmbProcType.IsEnabled = false;')),
        ec, 'No meaning of numeric status or deployed ACL invented.')
    for a, b, title in ((189, 199, 'From-date'), (201, 211, 'To-date')):
        lex('P7-156', title+' assigns date Cond and clears/reloads table',
            all(t in s(a, b) for t in ('Cond = " and inv.date >= @date1 and inv.date <= @date2 ";',
                '_masterTable.Clear();', 'LoadInvoices();')), ec,
            'Both handlers are manifestations of156, not two findings or actual WPF event counts.')
    lex('P7-156', 'Clear empties Cond before explicit reload',
        all(t in s(236, 254) for t in ('Cond                     = string.Empty;', '_masterTable.Clear();', 'LoadInvoices();')),
        ec, 'Explicit handler sequence; external caller status predicate is not retained in another local field.')
    lex('P7-156', 'Builder copies Cond and does not restore InvoiceStatus',
        'string condClause = Cond;' in s(336, 345) and 'InvoiceStatus' not in s(336, 408), ec,
        'Selected query text, not a global statement about save/database constraints.')
    lex('P7-157', 'Non23 SQL unconditionally adds type20 while23 is exact',
        'if (InvType == 23)' in s(348, 408) and 'AND  inv_type       = {InvType}' in s(348, 408)
        and 'AND  (inv_type = 20 OR inv_type = {InvType})' in s(348, 408), et,
        'Widening adjudicated only against selected purchase/transfer caller contracts, not all POS/Android unions.')
    lex('P7-157', 'Local row projection omits source type branch and eligibility status',
        all(t in s(570, 596) for t in ('InvGlobalID', 'ProcType', 'PaymentStatus'))
        and all(t not in s(674, 690) for t in ('InvoiceType', 'Branch', 'InvoiceStatus')),
        et, 'PaymentStatus is not InvoiceStatus; external DTO defaults are irrelevant to this local class.')
    lex('P7-156;P7-157', 'Ordinary selection returns GID proc pay without eligibility test',
        all(t in s(267, 284) for t in ('ISDone      = true;', 'InvGlobalID = row.InvGlobalID;', 'Hide();'))
        and 'InvoiceStatus' not in s(267, 284), ev((sc, 267, 284), (sc, 94, 109), (sc, 286, 303)),
        'Return-button special check and modal lifetime are separate contracts, not a claim every route is safe.')
    lex('P7-157', 'Purchase starts type1 and search consumes only GID+branch',
        'this.InvType  = 1;' in text(pc, 65, 84) and 'frm.InvType  = this.InvType;' in text(pc, 2641, 2662)
        and 'where branch={MainClass.BranchNo}' in text(pc, 2641, 2662), et,
        'Positive caller scope; no financial save or permission bypass execution.')
    lex('P7-157', 'Purchase Navigate passes SQL to reader while first navigation explicitly restricts type',
        'InvoiceOper.BindingInvoice(ref this.Invoic, sqlStr);' in text(pc, 481, 502)
        and 'where inv_type={this.InvType}' in text(pc, 504, 548), et,
        'Reader handoff boundary, not proof of the whole loaded form or a subsequent write.')
    lex('P7-156', 'Receive return path does not re-add mandatory status',
        'AND InvGlobalID=N\'{frm.InvGlobalID}\'' in text(tc, 1672, 1673)
        and 'InvoiceStatus' not in text(tc, 402, 453), ec,
        'Does not certify atomic receipt, stock or save; those barriers remain open.')
    lex('P7-157', 'Reader executes supplied SQL and maps actual source type and status',
        all(t in text(reader, 3219, 3290) for t in ('new SqlCommand(sqlstr, sqlConnection)',
            'Invo.InvoiceType = (InvoiceType)Conversions.ToInteger(sqlDataReader["inv_type"]);',
            'Invo.InvoiceStatus = Conversions.ToInteger(sqlDataReader["InvoiceStatus"]);')),
        et, 'Text observation only: no query, SDK, SQL reader or invoice constructor executed.')
    lex('H7B27-03', 'Optional period controls and reset are wired in XAML',
        all(t in text(sx, 238, 270) for t in ('IsChecked="True"', 'Checked="ckTotalPeriod_CheckedChanged"',
            'Unchecked="ckTotalPeriod_CheckedChanged"', 'IsEnabled="False"', 'SelectedDateChanged='))
        and 'Click="btnClear_Click"' in text(sx, 345, 353), ev((sx, 238, 270), (sx, 345, 353), (sc, 223, 229)),
        'All-period toggle, postponed filtering and event reentrancy remain explicit leads, not extra roots.')
    lex('H7B27-04', 'Branch deletion and exact23 remain positive local contrasts',
        'if (InvType != 14)' in s(336, 345) and s(348, 408).count('WHERE  inv.IS_Deleted = 0') == 2,
        ev((sc, 336, 408)), 'Branch exception14 and table23 need caller/schema policy, not automatic findings or ACL acceptance.')
    errors = [r['id'] for r in alg if not r['illustration_assertions_passed']]
    errors += [r['id'] for r in lexical if not r['documented_text_observation_matches']]
    return dict(audit_reference_date_utc='2026-11-16', source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',
        entry_checkout='6eedc0640e3432c14ca0875b7f1c7806ea1e3f64',
        application_code_imported_or_executed=False, dotnet_wpf_sql_or_DataView_executed=False,
        application_remediation_performed=False, phase7C_started=False, phase8_authorized_or_started=False,
        erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0, scanner_or_printer_tests_executed=0,
        B_R4k_bounded_not_whole7B_closure=True, unresolved_external_contracts_and_explicit_splits_retained=True,
        selected_paths_strict_utf8_decode=True, all_callers_or_external_DTOs_body_reviewed=False,
        actual_WPF_event_order_or_count_claimed=False, financial_or_status_policy_invented=False,
        external_DTO_constructor_defaults_assumed=False, database_commit_or_saved_loss_claimed=False,
        prior045_061_073_074_120_132_not_recounted_or_extended=True,
        retained_additive_B10_arithmetic_erratum=dict(local_cost=10, reference_cost=120, equality1_control=10, protected_G138_not_rewritten=True),
        illustration_count=len(alg), lexical_check_count=len(lexical), illustrations=alg,
        static_lexical_contract_checks=lexical, bounded_source_reads_not_semantic_coverage=reads,
        selected_source_paths=len(SOURCE_SLICES), whole_local_search_files_selected=2, source_read_slice_count=len(reads),
        unadjudicated_source_leads_not_additional_findings=['all-period-toggle/state and postponed-query/client-filter asymmetry',
            'DataView literal apostrophe same074-family without extension', 'return-button versus ordinary-selection policy',
            'remaining caller allow-sets, Dirty/Cancel/failure and external WPF settings'],
        limit='Locally whole698C#/561XAML search plus11 selected reads7paths is not all callers/DTOs/477bodies/census/455FE.155 fixed serverProc snapshot versus selected clientProc;156 caller status1 erased by date/reset;157 unconditional20 broadens purchase/transfer allowed types, GlobalID retained and consumer type mapped. Supplied rows and explicit actions only, no SQL/DataView/WPF/.NET/provider/SDK/event/calendar/culture/ACL/stock/save/financial/production acceptance, remediations or saved losses. No extra period/quote/return-button roots; prior045/061/073/074/120/132 and all old metadata preserved.7B/7 partial,R4l/B28 proposed,7C unstarted,8 unauthorized;independent repairs not presumed started/synchronized.', errors=errors)


if __name__ == '__main__':
    result = build()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if result['errors'] else 0)
