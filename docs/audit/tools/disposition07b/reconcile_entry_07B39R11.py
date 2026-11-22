#!/usr/bin/env python3
"""One NEW R11 entry hydration, not replay/reconstruction of the lost R10 work.

Only audit files independently verified byte-identical to the already-published
R4 preservation archive may be removed as checkout collisions. That original
archive is reused in Git, never duplicated or reconstructed. Source files,
repository root and .git are not removed/moved/reset. Stay on the fixed branch.
"""
from __future__ import annotations
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[4]
E = ROOT / 'docs/audit/evidence'
TAG = '07B39R11'
BRANCH = 'arena/94ae8414-smartauditerp'
ENTRY_HEAD = '10ba215152f722c8808aea0bb672c1d1d4d9d711'
R9 = 'dbf2760a6e7d2961736283b5faebc769e062a115'
REMOTE = '0f6559cf6853cc580b6fe3a2c63100e40f673453'
ARCHIVE = 'docs/audit/evidence/untracked-entry-docs-07B39R4.tar.gz'
ARCHIVE_SHA = '2ab6e6d3df2e30b038cb3c9f99ac957d6e13b59b119b074207535b2e19b3cc87'
ABSENT_LOCAL_COMMITS = ('729ef18aeac45d04e62c8315de3c690be0241ec5', '164a304252b3c46bb5f2eebabbc19681196353d2')


def git(*args): return subprocess.check_output(['git', *args], cwd=ROOT)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def clock(): return datetime.now(timezone.utc).isoformat()
def ident(raw): return dict(bytes=len(raw), sha256=sha(raw))
def pin(rel): return dict(path=rel, **ident((ROOT / rel).read_bytes()))
def exclusive(name, obj):
    with (E / name).open('x', encoding='utf8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2); f.write('\n')


def main():
    names = [s + '-' + TAG + ext for s, ext in (
        ('entry-before-hydration', '.json'), ('entry-hydration-receipt', '.json'),
        ('entry-hydration-forward', '.stdout.txt'), ('entry-hydration-forward', '.stderr.txt'))]
    if any((E / n).exists() for n in names): raise FileExistsError('Preserve this entry event; no rerun/overwrite')
    if git('branch', '--show-current').decode().strip() != BRANCH or git('rev-parse', 'HEAD').decode().strip() != ENTRY_HEAD:
        raise ValueError('Unexpected branch/entry HEAD; do not apply an old recovery plan')
    if git('rev-parse', 'origin/' + BRANCH).decode().strip() != REMOTE: raise ValueError('Remote changed; inspect first')
    if git('diff', '--name-only') or git('diff', '--cached', '--name-only'): raise ValueError('Unexpected tracked edits')
    for commit in ABSENT_LOCAL_COMMITS:
        if subprocess.run(['git', 'cat-file', '-e', commit + '^{commit}'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            raise ValueError('Prior commit is now available; recover it rather than declaring it absent')
    source_changes = git('diff', '--name-only', ENTRY_HEAD, REMOTE, '--', 'SmartAuditERP', 'SmartAuditUpdater', 'SmartAuditERP.sln')
    if source_changes: raise ValueError('Published source differences require independent review, not hydration')
    inventory_raw = git('show', R9 + ':docs/audit/evidence/inventory.csv')
    inventory = list(csv.DictReader(io.StringIO(inventory_raw.decode('utf-8-sig'), newline='')))
    source_ids = {r['path']: dict(bytes=int(r['bytes']), sha256=r['sha256']) for r in inventory}
    if len(source_ids) != 827: raise ValueError('Expected canonical827 inventory')
    for rel, expected in source_ids.items():
        if ident((ROOT / rel).read_bytes()) != expected: raise ValueError('Application source differs: ' + rel)
    published_paths = git('ls-tree', '-r', '--name-only', REMOTE, 'docs/audit').decode().splitlines()
    if len(published_paths) != 1686: raise ValueError('Unexpected published audit count')
    archive_raw = git('show', R9 + ':' + ARCHIVE)
    if len(archive_raw) != 14560801 or sha(archive_raw) != ARCHIVE_SHA: raise ValueError('Original preservation archive differs')
    original_paths = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'docs').rglob('*')
        if p.is_file() and TAG not in p.name)
    if len(original_paths) != 1216 or not set(original_paths) <= set(published_paths): raise ValueError('Unreviewed untracked originals')
    before = {}
    with tarfile.open(fileobj=io.BytesIO(archive_raw), mode='r:gz') as tar:
        members = {m.name: m for m in tar.getmembers() if m.isfile()}
        if set(members) != set(original_paths): raise ValueError('Not the exact archived original1216 set')
        for rel in original_paths:
            stream = tar.extractfile(members[rel])
            with stream: archived = stream.read()
            current = (ROOT / rel).read_bytes()
            if current != archived: raise ValueError('Do not remove unpreserved collision: ' + rel)
            before[rel] = ident(current)
    started = clock()
    entry = dict(schema_version=1, kind='R11-actual-cold-entry-identity-before-new-hydration-not-lost-R10-restoration',
        assessment_reference_date_utc='2026-11-16', raw_clocks_are_calendar_authority=False,
        raw_started_clock_verbatim=started, branch=BRANCH, entry_HEAD=ENTRY_HEAD, published_R9_HEAD=R9,
        observed_remote_HEAD=REMOTE, application_sources=source_ids, exact_original1216_untracked_audit_files=before,
        reused_original_R4_archive=dict(published_at=R9, path=ARCHIVE, **ident(archive_raw)),
        prior_reported_local_commits_absent_in_current_object_store=list(ABSENT_LOCAL_COMMITS),
        attempts_to_fetch_exact_prior_commits='Both explicit git fetch origin <SHA> attempts actually returned128: upload-pack: not our ref. This is a transcription of tool observations, not independently captured raw stderr files.',
        locally_reported_R10_evidence_files_available=False, prior_R10_578_capture_recovered=False,
        prior_R10_counts_recreated_or_recertified=False, current_entry_is_not_a_rerun_of_the_R10_recovery_script=True,
        authorization='Continue reconciliation within approved26-capability7B only. Remote gate documents are repository evidence, not current user authorization to start7C/8.',
        application_execution_count=0, whole_7B_static_assessment_complete=False,
        phase7C_started_by_this_work=False, phase8_authorized_by_this_work=False,
        python_entry_tool=pin('docs/audit/tools/disposition07b/reconcile_entry_' + TAG + '.py'))
    exclusive(names[0], entry)
    # Remove only byte-verified untracked collisions. Their original bytes are
    # already in the exact published archive above, which ff will materialize.
    for rel in original_paths: (ROOT / rel).unlink()
    with (E / names[2]).open('xb') as out, (E / names[3]).open('xb') as err:
        process = subprocess.run(['git', 'merge', '--ff-only', 'origin/' + BRANCH], cwd=ROOT, stdout=out, stderr=err, check=False)
    if process.returncode: raise RuntimeError('Forward checkout failed; preserve streams and inspect, never rerun removals blindly')
    if git('rev-parse', 'HEAD').decode().strip() != REMOTE: raise ValueError('Wrong forward HEAD')
    for rel, expected in source_ids.items():
        if ident((ROOT / rel).read_bytes()) != expected: raise ValueError('Source changed during hydration: ' + rel)
    for rel in published_paths:
        if (ROOT / rel).read_bytes() != git('show', REMOTE + ':' + rel): raise ValueError('Published checkout differs: ' + rel)
    receipt = dict(schema_version=1, kind='R11-new-entry-forward-receipt-preserving-original-archive-not-lost-local-R10',
        assessment_reference_date_utc='2026-11-16', raw_clocks_are_calendar_authority=False,
        raw_started_clock_verbatim=started, raw_finished_clock_verbatim=clock(),
        branch=BRANCH, old_HEAD=ENTRY_HEAD, forward_HEAD=REMOTE, forward_exit_code=process.returncode,
        original_audit_files_verified_in_reused_archive=1216, published_audit_files_checked=1686,
        original_archive_duplicated=False, source_files_unchanged=827,
        original_archive_restored=pin(ARCHIVE), entry_before=pin('docs/audit/evidence/' + names[0]),
        stdout=pin('docs/audit/evidence/' + names[2]), stderr=pin('docs/audit/evidence/' + names[3]),
        lost_local_R10_deliverable_reconstructed=False, lost_R10_578_tests_recertified=False,
        remote_7C_gate_adopted_as_authorization=False, remote_new_finding_ids_accepted_without_review=False,
        application_execution_count=0, whole_7B_static_assessment_complete=False,
        phase7C_started_by_this_work=False, phase8_authorized_by_this_work=False)
    exclusive(names[1], receipt)
    print(json.dumps(dict(forward_HEAD=REMOTE, original1216_preserved=True, published_audit_files=1686,
        source_files_unchanged=827, prior_local_R10_available=False, prior578_recertified=False,
        forward_is_not_acceptance_of_remote_phase_or_root_decisions=True), indent=2))
    return 0


if __name__ == '__main__': sys.exit(main())
