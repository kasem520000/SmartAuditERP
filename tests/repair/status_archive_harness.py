#!/usr/bin/env python3
"""Checks derived repair archive coverage, classifications and pinned inputs."""
import collections
import csv
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

# Loading the generator for checks must not leave untracked bytecode in the repo.
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
script = ROOT / 'docs/repairs/tools/build_status_archive.py'
spec = importlib.util.spec_from_file_location('repair_status_archive_builder', script)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def check(label, condition):
    if not condition:
        raise AssertionError(label)
    print('PASS', label)


result = subprocess.run([sys.executable, str(script), '--check'], cwd=ROOT, capture_output=True, text=True)
check('stored archive is reproducible without writes', result.returncode == 0)
rules, findings, tracker, plan = builder.load_inputs()
repairs, blockers = builder.index_docs(tracker, plan, rules, {r['id'] for r in findings})
rows = builder.build_rows(findings, repairs, blockers, rules)
by_id = {r['id']: r for r in rows}
check('each original finding has exactly one status', len(by_id) == len(rows) == len(findings) == 334 and
      set(by_id) == {r['id'] for r in findings})
with (ROOT / 'docs/repairs/STATUS_ARCHIVE.csv').open(encoding='utf-8-sig', newline='') as f:
    saved = list(csv.DictReader(f))
check('saved CSV equals rebuilt records', saved == rows)
counts = collections.Counter(r['repair_status'] for r in rows)
check('all four states are mutually exclusive and exhaustive', set(counts) ==
      {'closed_in_scope', 'partial_open', 'deferred_blocked', 'pending_review'} and sum(counts.values()) == 334)
check('closed findings have repair evidence and no explicit remainder', all(
      r['repair_ids'] and not r['blocker_id'] and r['id'] not in rules['partial']
      for r in rows if r['repair_status'] == 'closed_in_scope'))
check('partial findings retain a documented remainder', all(
      r['repair_ids'] and r['remaining_or_scope'] for r in rows if r['repair_status'] == 'partial_open'))
check('deferred findings retain an explicit blocker and stay open', all(
      r['blocker_id'] and not r['repair_ids'] for r in rows if r['repair_status'] == 'deferred_blocked'))
check('unreviewed findings are not silently called deferred', all(
      not r['blocker_id'] and not r['repair_ids'] for r in rows if r['repair_status'] == 'pending_review'))
check('critical security findings remain blocked', all(by_id[x]['repair_status'] == 'deferred_blocked'
      for x in ('P1-007', 'P1-008')))
check('wider unaddressed lifecycle finding stays partial', by_id['P1-030']['repair_status'] == 'partial_open')
check('all explicitly partial findings stay open', all(by_id[x]['repair_status'] == 'partial_open'
      for x in rules['partial']))
check('P7-049 is blocked while 028 and 157 remain partial', by_id['P7-049']['repair_status'] == 'deferred_blocked'
      and all(by_id[x]['repair_status'] == 'partial_open' for x in ('P7-028', 'P7-157')))
check('sale event repair is recorded in scope', by_id['P7-162']['repair_status'] == 'closed_in_scope'
      and 'R-098' in by_id['P7-162']['repair_ids'])
check('plan-only repairs are included and P5-027 remains partial',
      by_id['P5-010']['repair_ids'] == 'R-058' and by_id['P5-027']['repair_ids'] == 'R-057'
      and by_id['P5-027']['repair_status'] == 'partial_open')
check('shared headings are mapped to correct repairs', all(by_id[k]['repair_ids'] == v for k, v in {
      'P4-001': 'R-042', 'P4-002': 'R-043', 'P5-019': 'R-053', 'P5-022': 'R-055',
      'P6-014': 'R-061', 'P6-016': 'R-062'}.items()))
check('input requests from owner are extracted', 'سياسة الحسابات' in by_id['P1-007']['remaining_or_scope'])
check('audit status is preserved rather than overwritten', all(r['audit_status'] == 'open-not-remediated' for r in rows))
original = builder.AUDIT
with tempfile.TemporaryDirectory() as temp:
    altered = Path(temp) / 'findings.csv'
    altered.write_bytes(original.read_bytes() + b'\n')
    try:
        builder.AUDIT = altered
        try:
            builder.load_inputs()
        except ValueError as exc:
            check('modified audit snapshot fails closed', 'pinned SHA-256' in str(exc))
        else:
            raise AssertionError('modified audit snapshot was accepted')
    finally:
        builder.AUDIT = original
print('RESULT: PASS — archive consistency checks; classifications are not WPF or SQL acceptance.')
