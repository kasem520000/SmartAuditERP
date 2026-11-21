#!/usr/bin/env python3
"""Exclusive R5 audit-only capture. Never overwrites a previous run's streams.

Runs only the enumerated Python audit checkers/tests. A preserved historical B38
failure is captured as a failure, not patched, skipped or an accepted green exit.
Use a NEW run id for any successor after changing inputs. Output files/receipt
are not their own inputs. This does not execute ERP, C#, SQL, WPF or providers.
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

import verify_production_adjustment as v

D = 'docs/audit/tools/disposition07b/'
N = 'docs/audit/tools/census07b/'
AUTHORED = [
    'docs/audit/evidence/' + name for name in
    (v.ENTRY, v.DATES, v.FACTS, v.READS, v.ROUTES, v.ROOTS, v.REVIEW,
     'identity-year-local-worklist-rev02-07B39R5.json',
     'capture-correction-run01-to-run02-07B39R5.json',
     'initial-authoring-source-diagnostic-07B39R5.json',
     'initial-authoring-checker-version-07B39R5.txt')]
AUTHORED += [D + name for name in ('verify_production_adjustment.py',
             'test_production_adjustment.py', 'capture_production_adjustment.py')]
AUTHORED += ['docs/audit/SOURCE-REVIEW-07B39R5-rev02.md']


def clock():
    return datetime.now(timezone.utc).isoformat()


def file_id(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': v.base.sha(raw)}


def dump_exclusive(path, obj):
    with path.open('x', encoding='utf8', newline='\n') as out:
        json.dump(obj, out, ensure_ascii=False, indent=2); out.write('\n')


def capture(run):
    if not re.fullmatch(r'run\d\d', run): raise ValueError('Use a distinct runNN identifier')
    suffix = '-current-' + run + '-' + v.TAG
    receipt = v.EV / ('validation-current-' + run + '-receipt-' + v.TAG + '.json')
    journal = v.EV / ('validation-current-' + run + '-journal-' + v.TAG + '.jsonl')
    archive = v.EV / ('validation-consumed-inputs-' + run + '-' + v.TAG + '.tar.gz')
    python = [sys.executable, '-B', '-W', 'error::ResourceWarning']
    commands = [
        ('R5-verify', python + [D + 'verify_production_adjustment.py', '--verify', '--rederive'], 0, False),
        ('R1-R4-R5-combined-tests', python + ['-m', 'unittest', '-v', 'test_recovery_exit', 'test_document_receiver', 'test_production_adjustment'], 0, True),
        ('R4-preserved-integrity', python + [D + 'verify_document_receiver.py', '--verify', '--rederive'], 0, False),
        ('R1-preserved-integrity', python + [D + 'verify_recovery_exit.py', '--rederive'], 0, False),
        ('B38-preserved-integrity', python + [N + 'validate_7b_completion.py', '--reparse'], 0, False),
        ('R5-completion-gate', python + [D + 'verify_production_adjustment.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('R4-completion-gate', python + [D + 'verify_document_receiver.py', '--verify', '--require-complete', '--rederive'], 2, False),
        ('R1-completion-gate', python + [D + 'verify_recovery_exit.py', '--require-complete', '--rederive'], 2, False),
        ('B38-preserved-tests', python + ['-m', 'unittest', 'discover', '-s', N.rstrip('/'), '-p', 'test_7b_completion.py', '-v'], 0, True),
    ]
    output_paths = {receipt, journal, archive}
    for name, *_ in commands:
        output_paths |= {v.EV / (name + suffix + ext) for ext in ('.stdout.txt', '.stderr.txt')}
    existing = [str(p.relative_to(v.ROOT)) for p in output_paths if p.exists()]
    if existing: raise FileExistsError('Preserve prior run; choose a new id: ' + ', '.join(sorted(existing)))
    for rel in AUTHORED:
        if not (v.ROOT / rel).is_file(): raise FileNotFoundError(rel)
    started = clock()
    before = {}
    paths = {v.ROOT / r['path'] for r in v.base.rows('inventory.csv')}
    paths |= {p for p in v.AUDIT.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    for path in sorted(paths - output_paths): before[path.relative_to(v.ROOT).as_posix()] = file_id(path)
    # The new consumed inputs are archived as actual bytes, not regenerated later.
    with archive.open('xb') as raw:
        with tarfile.open(fileobj=raw, mode='w:gz') as tar:
            for rel in sorted(AUTHORED): tar.add(v.ROOT / rel, arcname=rel, recursive=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    parser_path = env.get('PYTHONPATH', '')
    env['PYTHONPATH'] = os.pathsep.join([str(v.ROOT / D), str(v.ROOT / N), parser_path])
    records = []
    with journal.open('x', encoding='utf8', newline='\n') as log:
        for name, command, expected, is_suite in commands:
            out, err = (v.EV / (name + suffix + ext) for ext in ('.stdout.txt', '.stderr.txt'))
            raw_start, tick = clock(), time.monotonic()
            with out.open('xb') as stdout, err.open('xb') as stderr:
                process = subprocess.run(command, cwd=v.ROOT, env=env, stdout=stdout, stderr=stderr, check=False)
            entry = {'id': name, 'command': command, 'cwd': '.', 'exit_code': process.returncode,
                     'expected_integrity_or_open_gate_exit': expected,
                     'expected_exit_matched': process.returncode == expected,
                     'is_test_suite': is_suite, 'raw_started_clock_verbatim': raw_start,
                     'raw_finished_clock_verbatim': clock(), 'wall_seconds': round(time.monotonic() - tick, 6),
                     'stdout': v.identity(out.relative_to(v.ROOT).as_posix()),
                     'stderr': v.identity(err.relative_to(v.ROOT).as_posix())}
            if is_suite:
                text = err.read_text(encoding='utf8')
                match = re.search(r'^Ran (\d+) tests in ([\d.]+)s$', text, re.M)
                entry['reported_tests'] = int(match[1]) if match else None
                entry['reported_unittest_seconds'] = float(match[2]) if match else None
                entry['assertion_lines_verbatim'] = re.findall(r'^AssertionError:.*$', text, re.M)
                entry['suite_passed'] = process.returncode == 0
            else:
                try: entry['reported_errors'] = json.loads(out.read_bytes()).get('errors')
                except (json.JSONDecodeError, UnicodeDecodeError): entry['reported_errors'] = None
            records.append(entry)
            log.write(json.dumps(entry, ensure_ascii=False) + '\n'); log.flush()
    changed = []
    for rel, expected in before.items():
        path = v.ROOT / rel
        if not path.is_file() or file_id(path) != expected: changed.append(rel)
    by_id = {r['id']: r for r in records}
    suites_passed = all(r['suite_passed'] for r in records if r['is_test_suite'])
    capture_ok = not changed and all(r['expected_exit_matched'] for r in records)
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=v.ROOT, check=True, capture_output=True, text=True).stdout.strip()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=v.ROOT, check=True, capture_output=True, text=True).stdout.strip()
    result = {'schema_version': 1, 'kind': 'actual-exclusive-R5-capture-with-preserved-R1-R4-B38-not-missing196-recertification',
              'assessment_reference_date_utc': v.DATE, 'raw_clocks_are_calendar_authority': False,
              'raw_started_clock_verbatim': started, 'raw_finished_clock_verbatim': clock(),
              'base_HEAD': head, 'branch': branch,
              'parser_packages': {p: version(p) for p in ('tree-sitter', 'tree-sitter-c-sharp')},
              'inputs_before': before, 'inputs_changed_during_capture': changed,
              'exact_authored_consumed_versions_archive': {**v.identity(archive.relative_to(v.ROOT).as_posix()),
                    'member_paths': sorted(AUTHORED), 'members': len(AUTHORED)},
              'records': records, 'combined_tests_reported': by_id['R1-R4-R5-combined-tests']['reported_tests'],
              'combined_tests_all_passed': by_id['R1-R4-R5-combined-tests']['suite_passed'],
              'preserved_B38_failure_verbatim': by_id['B38-preserved-tests']['assertion_lines_verbatim'],
              'all_preserved_and_new_suites_passed': suites_passed,
              'capture_expected_exits_all_matched': capture_ok,
              'source_review_R5_was_capture_input': True,
              'late_phase_validation_reconciliation_and_index_prefixes_were_capture_inputs': False,
              'receipt_journal_archive_and_new_streams_are_their_own_inputs': False,
              'R2_R3_files_recovered': False, 'prior196_tests_recertified': False,
              'application_execution_count': 0, 'capability_exit_certificates_issued': 0,
              'four_family_exit_certificates_issued': 0, 'whole_7B_static_assessment_complete': False,
              'phase7C_started': False, 'phase8_authorized': False,
              'wrapper_exit_code': 0 if capture_ok and suites_passed else 1}
    dump_exclusive(receipt, result)
    print(json.dumps({'receipt': str(receipt.relative_to(v.ROOT)), 'input_count': len(before),
          'inputs_changed_during_capture': changed, 'commands': [{k: r[k] for k in ('id', 'exit_code')} for r in records],
          'combined_tests_reported': result['combined_tests_reported'],
          'combined_tests_all_passed': result['combined_tests_all_passed'],
          'preserved_B38_failure_verbatim': result['preserved_B38_failure_verbatim'],
          'all_preserved_and_new_suites_passed': suites_passed,
          'wrapper_exit_code': result['wrapper_exit_code']}, ensure_ascii=False, indent=2))
    return result['wrapper_exit_code']


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True, help='Exclusive new runNN; never reuse an existing run id.')
    args = parser.parse_args(argv)
    return capture(args.run)


if __name__ == '__main__':
    sys.exit(main())
