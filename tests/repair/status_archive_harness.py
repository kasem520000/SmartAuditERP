#!/usr/bin/env python3
"""Checks derived repair archive coverage, classifications and pinned inputs."""
import collections
import csv
import importlib.util
import re
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
check('each original finding has exactly one status', len(by_id) == len(rows) == len(findings) == 335 and
      set(by_id) == {r['id'] for r in findings})
with (ROOT / 'docs/repairs/STATUS_ARCHIVE.csv').open(encoding='utf-8-sig', newline='') as f:
    saved = list(csv.DictReader(f))
check('saved CSV equals rebuilt records', saved == rows)
counts = collections.Counter(r['repair_status'] for r in rows)
check('all four states are mutually exclusive and exhaustive', set(counts) ==
      {'closed_in_scope', 'partial_open', 'deferred_blocked', 'pending_review'} and sum(counts.values()) == len(rows))
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
check('warehouse name repair is in scope; access and branch findings remain open',
      by_id['P7-087']['repair_status'] == 'closed_in_scope' and by_id['P7-087']['repair_ids'] == 'R-101'
      and by_id['P2-011']['repair_status'] == 'deferred_blocked'
      and by_id['P7-088']['repair_status'] == 'pending_review')
check('date layout and sale printer-state repairs are recorded in scope',
      by_id['P7-089']['repair_status'] == 'closed_in_scope' and by_id['P7-089']['repair_ids'] == 'R-102'
      and by_id['P7-163']['repair_status'] == 'closed_in_scope' and by_id['P7-163']['repair_ids'] == 'R-103')
check('batch report and packing fixes classified conservatively',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-081', 'R-104'), ('P7-153', 'R-106'), ('P7-068', 'R-107')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-106', 'R-105'), ('P7-123', 'R-108')])
      and all(by_id[fid]['repair_status'] != 'closed_in_scope' for fid in ('P7-124', 'P7-154')))
check('period, tax, and scoped activity batch remains conservative',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-086', 'R-110'), ('P7-122', 'R-111'), ('P7-130', 'R-112')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-124', 'R-109'), ('P7-129', 'R-111')])
      and by_id['P7-123']['repair_status'] == 'partial_open')
check('follow-up batch and previously fixed export are recorded with scope',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-042', 'R-113'), ('P7-105', 'R-114'), ('P7-099', 'R-119'), ('P7-108', 'R-083')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-096', 'R-115'), ('P7-091', 'R-116'), ('P7-003', 'R-117'), ('P7-008', 'R-118')])
      and by_id['P7-009']['repair_status'] != 'closed_in_scope')
check('editor and period batch has bounded and partial classifications',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-007', 'R-120'), ('P7-148', 'R-122'), ('P7-097', 'R-124'), ('P7-126', 'R-125')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-023', 'R-121'), ('P7-151', 'R-123')])
      and all(by_id[fid]['repair_status'] != 'closed_in_scope' for fid in ('P7-022', 'P7-024', 'P7-152')))
check('serial VAT POS duplicate batch classifications retain partial scope',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-128', 'R-127'), ('P7-075', 'R-129')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-135', 'R-126'), ('P7-143', 'R-128')])
      and rules['audit_delivery'] == 'B36')
check('rental production print purchase and HTML batch has bounded statuses',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-074', 'R-130'), ('P7-119', 'R-132'), ('P7-098', 'R-134')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-134', 'R-131')])
      and by_id['P7-150']['repair_status'] == 'partial_open' and by_id['P7-150']['repair_ids'] == 'R-133; R-204'
      and by_id['P7-149']['repair_status'] != 'closed_in_scope')
check('activity, export, approved stock and logs batch statuses',
      all(by_id[fid]['repair_status'] == 'closed_in_scope' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-116', 'R-136'), ('P7-107', 'R-138')])
      and all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-056', 'R-135'), ('P7-117', 'R-137')])
      and by_id['P7-057']['repair_status'] != 'closed_in_scope')
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
check('B35 linked return scope remains open', all(by_id[fid]['repair_status'] == 'partial_open' for fid in ('P7-159', 'P7-160')) and 'R-161' in by_id['P7-159']['repair_ids'] and by_id['P4-013']['repair_status'] == 'deferred_blocked')
check('period and totals batch keeps bounded classifications',
      by_id['P7-062']['repair_status'] == 'closed_in_scope' and by_id['P7-062']['repair_ids'] == 'R-162' and
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-111', 'R-163'), ('P7-112', 'R-164'), ('P7-127', 'R-165'),
                           ('P7-073', 'R-166'), ('P7-094', 'R-167'), ('P7-006', 'R-168'), ('P7-120', 'R-169')]))
check('inventory payroll barcode and navigation batch stays bounded',
      by_id['P7-076']['repair_status'] == 'closed_in_scope' and by_id['P7-076']['repair_ids'] == 'R-171' and
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-005', 'R-170'), ('P7-092', 'R-172'), ('P7-138', 'R-173'),
                           ('P7-064', 'R-174'), ('P7-057', 'R-175'), ('P7-045', 'R-176'), ('P7-113', 'R-177')]))

check('financial guard and reports remain partial after payroll load follow-up',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-001', 'R-178'), ('P7-029', 'R-179'), ('P7-051', 'R-180'),
                           ('P7-070', 'R-181'), ('P7-078', 'R-182'), ('P7-100', 'R-183')])
      and by_id['P7-002']['repair_status'] == 'partial_open' and by_id['P7-002']['repair_ids'] == 'R-184')

check('payroll navigation and sales report findings remain partial',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-002', 'R-184'), ('P7-041', 'R-185'), ('P7-066', 'R-186'),
                           ('P7-067', 'R-187'), ('P7-080', 'R-188'), ('P7-095', 'R-189')])
      and by_id['P7-001']['repair_status'] == 'partial_open'
      and by_id['P7-082']['repair_status'] == 'pending_review')

check('booking project and activity batch remains partial and guarded',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-022', 'R-190'), ('P7-015', 'R-191'), ('P7-016', 'R-192; R-197'),
                           ('P7-017', 'R-193'), ('P7-058', 'R-194'), ('P7-010', 'R-195')])
      and by_id['P7-023']['repair_status'] == 'partial_open'
      and by_id['P7-011']['repair_status'] == 'partial_open')

check('project file, picker and contract findings remain partial',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-019', 'R-196'), ('P7-145', 'R-198'), ('P7-037', 'R-199'),
                           ('P7-011', 'R-200'), ('P7-012', 'R-201'), ('P7-013', 'R-202')])
      and by_id['P7-016']['repair_ids'] == 'R-192; R-197'
      and rules['audit_commit'].startswith('a83cb66')
      and all(by_id[fid]['repair_status'] == 'partial_open' for fid in ('P7-157', 'P7-159', 'P7-160')))

check('purchase and packing batch remains partial',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-149', 'R-203'), ('P7-150', 'R-133; R-204'), ('P7-152', 'R-205')]))

check('cost statement and guarded report batch stays partial',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-052', 'R-206; R-212'), ('P7-053', 'R-207; R-213'), ('P7-114', 'R-208'),
                           ('P7-090', 'R-209'), ('P7-071', 'R-210'), ('P7-069', 'R-211')]))

check('cost, line discount, price and serial follow-up remains partial',
      all(by_id[fid]['repair_status'] == 'partial_open' and by_id[fid]['repair_ids'] == rid
          for fid, rid in [('P7-052', 'R-206; R-212'), ('P7-053', 'R-207; R-213'),
                           ('P7-083', 'R-214'), ('P7-154', 'R-215'),
                           ('P7-033', 'R-216'), ('P7-043', 'R-217')]))

owner = (ROOT / 'docs/repairs/OWNER_DECISIONS.md').read_text(encoding='utf-8')
sections = {
    'deferred_blocked': owner.split('## أولاً:', 1)[1].split('## ثانياً:', 1)[0],
    'partial_open': owner.split('## ثانياً:', 1)[1].split('## ثالثاً:', 1)[0],
}
for status, section in sections.items():
    listed = re.findall(r'^- \*\*(P[1-7]-\d{3})(?:\s|\*)', section, re.M)
    expected = {row['id'] for row in rows if row['repair_status'] == status}
    check('owner list matches ' + status, len(listed) == len(set(listed)) and set(listed) == expected)

print('RESULT: PASS — archive consistency checks; classifications are not WPF or SQL acceptance.')
