#!/usr/bin/env python3
"""Exclusive R11 Python-audit capture. No application/SQL/WPF execution.

A new runNN is required after any consumed-input change. Preserve all failed
runs. Green expected for suites/integrities, exit2 for an open completion
gate; the B38 tool-census failure is NEVER relabelled as a passing suite.
Archives pin actual versions, not reading, semantic or chronology authority.
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

import verify_reconciliation_07B39R11 as v

N = 'docs/audit/tools/census07b/'
MODULES = ('test_recovery_exit', 'test_document_receiver', 'test_production_adjustment',
    'test_session_year', 'test_entry_source', 'test_linked_activity', 'test_save_edit',
    'test_reconciliation_07B39R11')
AUTHORED = [v.D + n for n in ('reconcile_entry_07B39R11.py', 'verify_reconciliation_07B39R11.py',
    'test_reconciliation_07B39R11.py', 'capture_reconciliation_07B39R11.py')]
AUTHORED += [v.E + n for n in (v.HYDRATION, v.ENTRY, v.RESTORATION, v.DATE_NOTE, v.FACTS, v.READS, v.REVIEW, v.LEDGER,
    'entry-hydration-forward-07B39R11.stdout.txt', 'entry-hydration-forward-07B39R11.stderr.txt',
    'entry-hydration-receipt-07B39R11.json', 'remote-R10-frozen-07B39R11.tar.gz')]
for run in ('run01', 'run02'):
    AUTHORED += [v.E + f'reconciliation-derivation-{run}-{suffix}' for suffix in (
        'consumed-07B39R11.tar.gz', 'receipt-07B39R11.json', '07B39R11.stdout.txt', '07B39R11.stderr.txt')]
AUTHORED += ['docs/audit/SOURCE-REVIEW-07B39R11.md']
AUTHORED += [v.E + 'development-corrections-07B39R11.json']


def clock():
    return datetime.now(timezone.utc).isoformat()


def capture(run):
    if not re.fullmatch(r'run\d\d', run):
        raise ValueError('Use a new runNN; never overwrite a prior capture')
    receipt = v.EV / f'validation-{run}-receipt-{v.TAG}.json'
    journal = v.EV / f'validation-{run}-journal-{v.TAG}.jsonl'
    archive = v.EV / f'validation-{run}-consumed-{v.TAG}.tar.gz'
    py = [sys.executable, '-B', '-W', 'error::ResourceWarning']
    combined = 'R1-through-R9-plus-R11-tests'
    commands = [
        ('R11-verify', py + [v.D + 'verify_reconciliation_07B39R11.py', '--rederive'], 0, False),
        (combined, py + ['-m', 'unittest', '-v', *MODULES], 0, True),
        ('R9-preserved-integrity', py + [v.D + 'verify_save_edit.py', '--verify', '--rederive'], 0, False),
        ('B38-preserved-integrity', py + [N + 'validate_7b_completion.py', '--reparse'], 0, False),
        ('R11-completion-gate', py + [v.D + 'verify_reconciliation_07B39R11.py', '--require-complete', '--rederive'], 2, False),
        ('R9-completion-gate', py + [v.D + 'verify_save_edit.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('B38-preserved-tests', py + ['-m', 'unittest', 'discover', '-s', N.rstrip('/'), '-p', 'test_7b_completion.py', '-v'], 0, True),
    ]
    outputs = {receipt, journal, archive}
    for name, *_ in commands:
        outputs |= {v.EV / f'{name}-{run}-{v.TAG}{ext}' for ext in ('.stdout.txt', '.stderr.txt')}
    if any(p.exists() for p in outputs):
        raise FileExistsError('This run has existing output; choose a new id')
    for rel in AUTHORED:
        if not (v.ROOT / rel).is_file():
            raise FileNotFoundError(rel)
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=v.ROOT, text=True).strip()
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=v.ROOT, text=True).strip()
    if branch != 'arena/94ae8414-smartauditerp':
        raise ValueError('Wrong session branch')
    paths = {v.ROOT / r['path'] for r in v.base.rows('inventory.csv')}
    paths |= {p for p in v.AUDIT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    before = {p.relative_to(v.ROOT).as_posix(): v.identity(p.relative_to(v.ROOT).as_posix())
              for p in sorted(paths - outputs)}
    with archive.open('xb') as raw:
        with tarfile.open(fileobj=raw, mode='w:gz') as tar:
            for rel in sorted(AUTHORED):
                tar.add(v.ROOT / rel, arcname=rel, recursive=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env['PYTHONPATH'] = os.pathsep.join([str(v.ROOT / v.D), str(v.ROOT / N), env.get('PYTHONPATH', '')])
    started, records = clock(), []
    with journal.open('x', encoding='utf8', newline='\n') as log:
        for name, command, expected, is_suite in commands:
            out, err = (v.EV / f'{name}-{run}-{v.TAG}{ext}' for ext in ('.stdout.txt', '.stderr.txt'))
            start, tick = clock(), time.monotonic()
            with out.open('xb') as stdout, err.open('xb') as stderr:
                process = subprocess.run(command, cwd=v.ROOT, env=env, stdout=stdout, stderr=stderr, check=False)
            row = {'id': name, 'command': command, 'exit_code': process.returncode,
                'expected_green_integrity_suite_or_open_gate_exit': expected,
                'expected_exit_matched': process.returncode == expected, 'is_test_suite': is_suite,
                'raw_started_clock_verbatim': start, 'raw_finished_clock_verbatim': clock(),
                'wall_seconds': round(time.monotonic() - tick, 6),
                'stdout': v.identity(out.relative_to(v.ROOT).as_posix()),
                'stderr': v.identity(err.relative_to(v.ROOT).as_posix())}
            if is_suite:
                text = err.read_text(encoding='utf8')
                match = re.search(r'^Ran (\d+) tests in ([\d.]+)s$', text, re.M)
                cases = re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. (ok|FAIL|ERROR)$', text, re.M)
                row.update(reported_tests=int(match[1]) if match else None,
                    reported_unittest_seconds=float(match[2]) if match else None,
                    actual_verbose_case_lines=len(cases),
                    actual_status_counts={k: sum(c[2] == k for c in cases) for k in ('ok', 'FAIL', 'ERROR')},
                    actual_module_partition={m: sum(c[1].startswith(m + '.') for c in cases) for m in MODULES} if name == combined else {},
                    assertion_lines_verbatim=re.findall(r'^AssertionError:.*$', text, re.M),
                    suite_passed=process.returncode == 0)
            else:
                try:
                    obj = json.loads(out.read_bytes())
                    row['reported_errors'] = obj.get('errors', obj.get('integrity_errors'))
                except (ValueError, UnicodeDecodeError):
                    row['reported_errors'] = None
            records.append(row)
            log.write(json.dumps(row, ensure_ascii=False) + '\n')
            log.flush()
    changed = [rel for rel, pin in before.items() if not (v.ROOT / rel).is_file() or v.identity(rel) != pin]
    suites_green = all(r['suite_passed'] for r in records if r['is_test_suite'])
    matched = not changed and all(r['expected_exit_matched'] for r in records)
    by_id = {r['id']: r for r in records}
    wrapper = 0 if matched and suites_green else 1
    result = {'schema_version': 1, 'kind': 'actual-exclusive-R11-Python-audit-capture-not-recovered-local-R10-or-ERP-run',
        'assessment_reference_date_utc': v.DATE, 'reference_date_note': v.identity(v.E + v.DATE_NOTE),
        'raw_clocks_are_calendar_authority': False, 'raw_started_clock_verbatim': started, 'raw_finished_clock_verbatim': clock(),
        'branch': branch, 'HEAD_at_capture': head,
        'parser_versions': {p: version(p) for p in ('tree-sitter', 'tree-sitter-c-sharp')},
        'inputs_before': before, 'inputs_changed_during_capture': changed,
        'exact_consumed_versions_archive': {**v.identity(archive.relative_to(v.ROOT).as_posix()), 'members': len(AUTHORED), 'member_paths': sorted(AUTHORED)},
        'records': records, 'command_count': len(records), 'raw_stream_count': 2 * len(records),
        'combined_actual_reported_tests': by_id[combined]['reported_tests'],
        'combined_actual_module_partition': by_id[combined]['actual_module_partition'],
        'combined_suite_passed': by_id[combined]['suite_passed'],
        'preserved_B38_actual_assertion_lines': by_id['B38-preserved-tests']['assertion_lines_verbatim'],
        'all_suites_green': suites_green, 'all_command_expectations_matched': matched, 'wrapper_exit_code': wrapper,
        'lost_local_R10_578_capture_recovered_or_recertified': False,
        'old_R2_R3_196_345_49_reconstructed_or_recertified': False,
        'source_review_and_adjudication_were_inputs': True,
        'late_PHASE_VALIDATION_index_prefix_and_publication_receipts_were_inputs': False,
        'this_receipt_journal_archive_streams_are_their_own_inputs': False,
        'application_execution_count': 0, 'whole_7B_static_assessment_complete': False,
        'capability_exit_certificates_issued': 0, 'four_family_exit_certificates_issued': 0,
        'new_accepted_external_handoffs': 0, 'phase7C_started': False, 'phase8_authorized': False}
    v.exclusive_json(receipt, result)
    print(json.dumps({k: result[k] for k in ('combined_actual_reported_tests', 'combined_actual_module_partition',
        'combined_suite_passed', 'preserved_B38_actual_assertion_lines', 'all_suites_green', 'all_command_expectations_matched',
        'inputs_changed_during_capture', 'command_count', 'raw_stream_count', 'wrapper_exit_code')}, ensure_ascii=False, indent=2))
    return wrapper


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    args = parser.parse_args(argv)
    return capture(args.run)


if __name__ == '__main__':
    sys.exit(main())
