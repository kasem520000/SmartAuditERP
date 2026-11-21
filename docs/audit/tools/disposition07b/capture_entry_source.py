#!/usr/bin/env python3
"""Exclusive R7 Python-audit capture, never ERP/SQL/WPF/provider execution.

A runNN owns its immutable streams, journal, receipt and exact authored consumed
versions archive. After corrections use a NEW run id. A preserved failed suite is
not skipped, patched, expected-green or converted into a completion certificate.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import time

import verify_entry_source as v

D, N = 'docs/audit/tools/disposition07b/', 'docs/audit/tools/census07b/'
AUTHORED = ['docs/audit/evidence/' + n for n in (
    v.ENTRY, v.FACTS, v.READS, v.REVIEW, v.MATRIX, v.WORK, v.ROOTS, v.CORRECTION,
    'entry-recovery-identities-07B39R7.json', 'entry-recovery-receipt-07B39R7.json')]
AUTHORED += [D + n for n in ('verify_entry_source.py', 'test_entry_source.py', 'capture_entry_source.py')]
AUTHORED += ['docs/audit/SOURCE-REVIEW-07B39R7.md']
MODULES = ('test_recovery_exit', 'test_document_receiver', 'test_production_adjustment',
           'test_session_year', 'test_entry_source')


def clock():
    return datetime.now(timezone.utc).isoformat()


def file_id(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': v.base.sha(raw)}


def exclusive_json(path, obj):
    with path.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def capture(run):
    if not re.fullmatch(r'run\d\d', run): raise ValueError('A distinct runNN is required')
    receipt = v.EV / f'validation-current-{run}-receipt-{v.TAG}.json'
    journal = v.EV / f'validation-current-{run}-journal-{v.TAG}.jsonl'
    archive = v.EV / f'validation-consumed-inputs-{run}-{v.TAG}.tar.gz'
    suffix = f'-current-{run}-{v.TAG}'
    py = [sys.executable, '-B', '-W', 'error::ResourceWarning']
    combined_id = 'R1-R4-R5-R6-R7-combined-tests'
    commands = [
        ('R7-verify', py + [D + 'verify_entry_source.py', '--verify', '--rederive'], 0, False),
        (combined_id, py + ['-m', 'unittest', '-v', *MODULES], 0, True),
        ('R6-preserved-integrity', py + [D + 'verify_session_year.py', '--verify', '--rederive'], 0, False),
        ('R5-preserved-integrity', py + [D + 'verify_production_adjustment.py', '--verify', '--rederive'], 0, False),
        ('R4-preserved-integrity', py + [D + 'verify_document_receiver.py', '--verify', '--rederive'], 0, False),
        ('R1-preserved-integrity', py + [D + 'verify_recovery_exit.py', '--rederive'], 0, False),
        ('B38-preserved-integrity', py + [N + 'validate_7b_completion.py', '--reparse'], 0, False),
        ('R7-completion-gate', py + [D + 'verify_entry_source.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('R6-completion-gate', py + [D + 'verify_session_year.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('R5-completion-gate', py + [D + 'verify_production_adjustment.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('R4-completion-gate', py + [D + 'verify_document_receiver.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('R1-completion-gate', py + [D + 'verify_recovery_exit.py', '--require-complete', '--rederive'], 2, False),
        ('B38-preserved-tests', py + ['-m', 'unittest', 'discover', '-s', N.rstrip('/'), '-p', 'test_7b_completion.py', '-v'], 0, True),
    ]
    outputs = {receipt, journal, archive}
    for name, *_ in commands:
        outputs |= {v.EV / (name + suffix + ext) for ext in ('.stdout.txt', '.stderr.txt')}
    collisions = sorted(str(p.relative_to(v.ROOT)) for p in outputs if p.exists())
    if collisions: raise FileExistsError('Preserve existing run; use a new id: ' + ', '.join(collisions))
    for rel in AUTHORED:
        if not (v.ROOT / rel).is_file(): raise FileNotFoundError(rel)
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=v.ROOT, capture_output=True, text=True, check=True).stdout.strip()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=v.ROOT, capture_output=True, text=True, check=True).stdout.strip()
    if branch != 'arena/94ae8414-smartauditerp': raise ValueError('Wrong session branch')
    started = clock()
    paths = {v.ROOT / r['path'] for r in v.base.rows('inventory.csv')}
    paths |= {p for p in v.AUDIT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    before = {p.relative_to(v.ROOT).as_posix(): file_id(p) for p in sorted(paths - outputs)}
    with archive.open('xb') as raw:
        with tarfile.open(fileobj=raw, mode='w:gz') as tar:
            for rel in sorted(AUTHORED): tar.add(v.ROOT / rel, arcname=rel, recursive=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env['PYTHONPATH'] = os.pathsep.join([str(v.ROOT / D), str(v.ROOT / N), env.get('PYTHONPATH', '')])
    records = []
    with journal.open('x', encoding='utf8', newline='\n') as log:
        for name, command, expected, is_suite in commands:
            out, err = (v.EV / (name + suffix + ext) for ext in ('.stdout.txt', '.stderr.txt'))
            raw_start, tick = clock(), time.monotonic()
            with out.open('xb') as stdout, err.open('xb') as stderr:
                process = subprocess.run(command, cwd=v.ROOT, env=env, stdout=stdout, stderr=stderr, check=False)
            row = {'id': name, 'command': command, 'cwd': '.', 'exit_code': process.returncode,
                   'expected_integrity_open_gate_or_green_suite_exit': expected,
                   'expected_exit_matched': process.returncode == expected, 'is_test_suite': is_suite,
                   'raw_started_clock_verbatim': raw_start, 'raw_finished_clock_verbatim': clock(),
                   'wall_seconds': round(time.monotonic() - tick, 6),
                   'stdout': v.identity(out.relative_to(v.ROOT).as_posix()),
                   'stderr': v.identity(err.relative_to(v.ROOT).as_posix())}
            if is_suite:
                text = err.read_text(encoding='utf8')
                match = re.search(r'^Ran (\d+) tests in ([\d.]+)s$', text, re.M)
                cases = re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. (ok|FAIL|ERROR)$', text, re.M)
                row.update({'reported_tests': int(match[1]) if match else None,
                    'reported_unittest_seconds': float(match[2]) if match else None,
                    'actual_verbose_case_lines': len(cases),
                    'actual_case_status_counts': {k: sum(c[2] == k for c in cases) for k in ('ok', 'FAIL', 'ERROR')},
                    'actual_case_partition_by_module': {m: sum(c[1].startswith(m + '.') for c in cases) for m in MODULES} if name == combined_id else {},
                    'assertion_lines_verbatim': re.findall(r'^AssertionError:.*$', text, re.M),
                    'suite_passed': process.returncode == 0})
            else:
                try:
                    obj = json.loads(out.read_bytes())
                    row['reported_errors'] = obj.get('errors', obj.get('integrity_errors'))
                except (ValueError, UnicodeDecodeError): row['reported_errors'] = None
            records.append(row)
            log.write(json.dumps(row, ensure_ascii=False) + '\n')
            log.flush()
    changed = [rel for rel, expected in before.items()
               if not (v.ROOT / rel).is_file() or file_id(v.ROOT / rel) != expected]
    by_id = {r['id']: r for r in records}
    suites_green = all(r['suite_passed'] for r in records if r['is_test_suite'])
    expected_exits = not changed and all(r['expected_exit_matched'] for r in records)
    result = {'schema_version': 1, 'kind': 'actual-exclusive-R7-Python-audit-capture-not-ERP-or-missing196-recertification',
        'assessment_reference_date_utc': v.DATE, 'raw_clocks_are_calendar_authority': False,
        'raw_started_clock_verbatim': started, 'raw_finished_clock_verbatim': clock(),
        'base_HEAD': head, 'branch': branch,
        'parser_packages': {p: version(p) for p in ('tree-sitter', 'tree-sitter-c-sharp')},
        'inputs_before': before, 'inputs_changed_during_capture': changed,
        'exact_authored_consumed_versions_archive': {**v.identity(archive.relative_to(v.ROOT).as_posix()),
            'members': len(AUTHORED), 'member_paths': sorted(AUTHORED)},
        'records': records, 'combined_tests_reported': by_id[combined_id]['reported_tests'],
        'combined_tests_all_passed': by_id[combined_id]['suite_passed'],
        'combined_actual_partition': by_id[combined_id]['actual_case_partition_by_module'],
        'preserved_B38_failure_verbatim': by_id['B38-preserved-tests']['assertion_lines_verbatim'],
        'all_preserved_and_new_suites_passed': suites_green,
        'capture_expected_exits_all_matched': expected_exits,
        'source_review_R7_was_capture_input': True,
        'late_phase_validation_reconciliation_and_index_prefixes_were_capture_inputs': False,
        'receipt_journal_archive_and_new_streams_are_their_own_inputs': False,
        'prior196_tests_recertified': False, 'R2_R3_files_recovered': False,
        'application_execution_count': 0, 'capability_exit_certificates_issued': 0,
        'four_family_exit_certificates_issued': 0, 'whole_7B_static_assessment_complete': False,
        'new_accepted_external_handoffs': 0, 'phase7C_started': False, 'phase8_authorized': False,
        'wrapper_exit_code': 0 if expected_exits and suites_green else 1}
    exclusive_json(receipt, result)
    print(json.dumps({'receipt': str(receipt.relative_to(v.ROOT)), 'input_count': len(before),
        'inputs_changed_during_capture': changed,
        'commands': [{k: r[k] for k in ('id', 'exit_code')} for r in records],
        'combined_tests_reported': result['combined_tests_reported'],
        'combined_tests_all_passed': result['combined_tests_all_passed'],
        'combined_actual_partition': result['combined_actual_partition'],
        'preserved_B38_failure_verbatim': result['preserved_B38_failure_verbatim'],
        'all_preserved_and_new_suites_passed': suites_green,
        'wrapper_exit_code': result['wrapper_exit_code']}, ensure_ascii=False, indent=2))
    return result['wrapper_exit_code']


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    return capture(parser.parse_args(argv).run)


if __name__ == '__main__':
    sys.exit(main())
