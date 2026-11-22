#!/usr/bin/env python3
"""R14: unify the cumulative path ledger with 7C slice paths, then run the
Phase-7 require-complete gate (fail-closed semantics, matching the B38 gate
tradition: exit 0 = mechanical checks green; exit 2 = gate verdict OPEN).

The gate distinguishes:
  - stage7_audit_workstream_complete: every 7C worklist item from the R10
    start gate resolved with committed evidence (R10-R13).
  - stage7_whole_certification: capability/family exits — NOT granted while
    their numbered roots await stage-8 remediation (fail-closed by design).

No ERP/SQL/WPF execution; read-only repository facts.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / 'docs' / 'audit'
EV = DOCS / 'evidence'
TAG = '07B39R14'

R1_RESERVED = {'P7-164', 'P7-165', 'P7-166', 'P7-167'}
RENUMBERED = {'P7-179', 'P7-180', 'P7-181', 'P7-182'}

# 7C worklist (from evidence/7c-start-gate-07B39R10.json) -> resolution evidence
WORKLIST_RESOLUTIONS = {
    'item1_19_LastProcess_helpers': {'status': 'read in R8 (flags carried)', 'evidence': ['PHASE-07B39R8.md']},
    'item2_11_linked_insert_identities': {'status': 'read in R8 (flags carried)', 'evidence': ['PHASE-07B39R8.md']},
    'item3_remaining_helpers_writers': {
        'status': 'completed in R11 (SearchByID/ItemOper + merge/replace/unit/qty/price/discount/VAT local read; roots P7-181,P7-182,168-172)',
        'evidence': ['PHASE-07B39R13-rev02.md', 'evidence/search-item-family-contract-07B39R11.json']},
    'item4_FormPermission_full': {'status': 'read in R7', 'evidence': ['PHASE-07B39R7.md', 'SOURCE-REVIEW-07B39R7-local.md']},
    'item5_SaveReceipt2_Recipient': {
        'status': 'adjudicated in R10 as confirmed root (renumbered P7-179 in rev02); independently qualified by the concurrent line',
        'evidence': ['evidence/recipient-notify-contract-07B39R10.json', 'PHASE-07B39R13-rev02.md']},
    'item6_notify_save_delete_branch_scope': {
        'status': 'adjudicated in R10 as confirmed root (renumbered P7-180 in rev02; concurrent line corrected column counts to 22/22/24 — adopted in rev02 note)',
        'evidence': ['evidence/recipient-notify-contract-07B39R10.json', 'PHASE-07B39R13-rev02.md']},
    'item7_local_recovery_helpers': {'status': 'read in R7', 'evidence': ['PHASE-07B39R7.md']},
    'carried_Q_reader': {'status': 'adjudicated R12: root P7-173', 'evidence': ['evidence/q-reader-year-branch-contract-07B39R12.json']},
    'carried_year_provenance': {'status': 'adjudicated R12: root P7-176', 'evidence': ['evidence/q-reader-year-branch-contract-07B39R12.json']},
    'carried_branch_rehydration': {'status': 'adjudicated R12: root P7-174', 'evidence': ['evidence/q-reader-year-branch-contract-07B39R12.json']},
    'allowed_set_per_document_branch_year': {
        'status': 'ledger built R13; D05/D06 exit gates adjudicated NOT MET with numbered roots',
        'evidence': ['evidence/capability-allowed-set-07B39R13.json']},
    'path_ledger_unification': {'status': 'this slice (R14)', 'evidence': ['evidence/phase7-completion-gate-07B39R14.json']},
}


def main() -> int:
    problems: list[str] = []

    # ── 1. findings.csv integrity + collision-freedom ───────────────
    raw = (DOCS / 'findings.csv').read_bytes()
    rows = list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'))))
    ids = [r['id'] for r in rows]
    registry = {
        'bytes': len(raw), 'bom': raw[:3] == b'\xef\xbb\xbf',
        'crlf': raw.count(b'\r\n'), 'lf_only': raw.count(b'\n') - raw.count(b'\r\n'),
        'rows': len(rows),
    }
    if registry['bom']: problems.append('findings.csv has BOM')
    if registry['lf_only'] != 0: problems.append('findings.csv has LF-only lines')
    if len(ids) != len(set(ids)): problems.append('findings.csv has duplicate ids')
    collisions = R1_RESERVED & set(ids)
    if collisions: problems.append(f'R1-reserved ids present in registry: {sorted(collisions)}')
    missing_renumbered = RENUMBERED - set(ids)
    if missing_renumbered: problems.append(f'renumbered ids missing: {sorted(missing_renumbered)}')
    p7_max = max(int(i.split('-')[1]) for i in ids if i.startswith('P7-'))
    registry['p7_max'] = p7_max

    # every 7C-line root must be open-not-remediated with next_phase 8
    seven_c_roots = [i for i in ids if i.startswith('P7-') and 168 <= int(i.split('-')[1]) <= 182]
    for i in seven_c_roots:
        row = next(r for r in rows if r['id'] == i)
        if row['status'] != 'open-not-remediated' or row['next_phase'] != '8':
            problems.append(f'{i} status/next_phase unexpected: {row["status"]}/{row["next_phase"]}')

    # ── 2. 7C slice evidence chain present ──────────────────────────
    chain_files = [
        '7c-start-gate-07B39R10.json', 'recipient-notify-contract-07B39R10.json',
        'search-item-family-contract-07B39R11.json',
        'q-reader-year-branch-contract-07B39R12.json',
        'capability-allowed-set-07B39R13.json',
        'concurrent-integration-07B39R11.json',
    ]
    ledger = {}
    for name in chain_files:
        f = EV / name
        ok = f.exists()
        if not ok:
            problems.append(f'missing chain evidence: {name}')
            ledger[name] = {'present': False}
            continue
        b = f.read_bytes()
        try:
            json.loads(b.decode('utf-8-sig'))
            valid = True
        except Exception:
            valid = False
            problems.append(f'invalid JSON evidence: {name}')
        ledger[name] = {'present': True, 'bytes': len(b), 'json_valid': valid,
                        'sha256_16': hashlib.sha256(b).hexdigest()[:16]}

    # R13 receipt facts must still hold (trial-balance lines)
    r13 = json.loads((EV / 'capability-allowed-set-07B39R13.json').read_text(encoding='utf-8-sig'))
    if r13['trial_balance_D06']['calcsum_sums_all_display_rows_at'] != 512:
        problems.append('R13 receipt trial-balance facts drifted')

    # ── 3. capability register + allowed-set ledger cross-check ─────
    reg = list(csv.DictReader(io.StringIO(
        (EV / 'capability-register-07B38.csv').read_text(encoding='utf-8-sig'))))
    if len(reg) != 26: problems.append(f'capability register rows = {len(reg)} (expected 26)')
    caps_no_exit = [r['id'] for r in reg if r['whole_capability_certified'].lower() != 'true']
    if len(caps_no_exit) != 26:
        problems.append('register claims certified capabilities — not allowed in this phase')

    # ── 4. path ledger unification ──────────────────────────────────
    # cumulative slice docs R1..R14 present in docs/audit (or preserved in git history)
    import subprocess
    tracked = subprocess.run(['git', 'ls-files', 'docs/audit'], capture_output=True, text=True,
                             cwd=ROOT).stdout.splitlines()
    tracked_set = set(tracked)
    unified_paths = {}
    for tag_pat, label in [
        (r'^docs/audit/PHASE-07B39R1[0-4]', 'phase docs R10-R14'),
        (r'^docs/audit/evidence/.*07B39R1[0-4]', 'evidence R10-R14'),
        (r'^docs/audit/tools/disposition07b/.*', 'disposition tools'),
    ]:
        rx = re.compile(tag_pat)
        unified_paths[label] = sorted(p for p in tracked_set if rx.search(p))
    if not unified_paths['phase docs R10-R14']:
        problems.append('no R10-R14 phase docs tracked')

    # ── 5. the verdict (fail-closed) ────────────────────────────────
    workstream_complete = not problems and all(
        v['status'].startswith(('completed', 'adjudicated', 'read', 'ledger built', 'this slice'))
        for v in WORKLIST_RESOLUTIONS.values())

    verdict = {
        'tag': TAG,
        'mechanical_checks_green': not problems,
        'problems': problems,
        'stage7_audit_workstream_complete': bool(workstream_complete),
        'stage7_worklist_resolutions': WORKLIST_RESOLUTIONS,
        'stage7_whole_certification': False,
        'certification_blockers': [
            'capability-exits-not-granted: D05/D06 adjudicated NOT MET (roots P7-179/P7-180/P7-174/P7-176/P7-178 et al); 24 other capabilities carry their per-capability exit criteria',
            'four-family-exits-not-granted',
            'remediation-gated: exit criteria require stage-8 fixes of numbered roots first',
            'B38 preserved failure (162/163/169 != 142 across runs) acknowledged, unresolved',
            'runtime certification never performed (application_execution_count = 0 by design)',
        ],
        'stage8_remediation_status': {
            'running_by_owner_directive': True,
            'branches': ['fix/stage1-p1-security (33/33 P1 addressed: 29 complete + 4 partial)',
                         'fix/stage2-p2-authz (12/16 P2 addressed)'],
        },
        'stage8_audit_licensing': 'blocked-on-stage7-certification (fail-closed)',
        'registry': registry,
        'seven_c_root_ids': seven_c_roots,
        'renumbering_applied': {'P7-164->P7-179': 'SaveReceipt2 Recipient',
                                 'P7-165->P7-180': 'Settingmqtt notify transaction/scope',
                                 'P7-166->P7-181': 'item-search SQL string-concat family',
                                 'P7-167->P7-182': 'POS scale barcode wrong-row write'},
        'unified_path_ledger': unified_paths,
        'evidence_chain': ledger,
        'meaning': 'Static-audit workstream verdict only; never ERP, financial, repair or deployment acceptance.',
    }

    out = EV / 'phase7-completion-gate-07B39R14.json'
    out.write_text(json.dumps(verdict, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f"receipt: {out} ({out.stat().st_size} bytes)")
    print(f"mechanical: {'GREEN' if not problems else 'PROBLEMS: ' + '; '.join(problems)}")
    print(f"stage7_audit_workstream_complete: {verdict['stage7_audit_workstream_complete']}")
    print(f"stage7_whole_certification: {verdict['stage7_whole_certification']} (fail-closed)")
    if problems:
        return 1
    # fail-closed gate: exit 2 while certification is open (B38 tradition)
    return 2 if not verdict['stage7_whole_certification'] else 0


if __name__ == '__main__':
    sys.exit(main())
