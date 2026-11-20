#!/usr/bin/env python3
"""Run ALL52 original B32 cases with OWN334/presetB32/assertion DATA.

119 historical source identities and canonical B32 dispatcher TEXT are local
A/Path inputs only. No old dispatcher code is executed; actual current parser,
19 routing gates and123 execution tools are checked independently by B33.
No test filtering/skips, disk overlay, protected edits, shared subprocess or
process-global pathlib mutation. __file__ and executing main code stay intact.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-part', required=True, choices=('B32',))
    parser.parse_args()
    import validate_audit as v
    import validate_output_route_part as b33
    import test_editor_close_audit_validator as historical_tests

    for name, digest in ((b33.SNAPSHOT, b33.SNAPSHOT_SHA),
                         (b33.SHARED_SNAPSHOT, b33.SHARED_SHA),
                         (b33.DISPATCHER_SNAPSHOT, b33.DISPATCHER_SHA),
                         ('evidence/provenance-07B33.json', b33.PROVENANCE_SHA)):
        if v.sha(v.AUDIT / name) != digest:
            raise ValueError('B32 OWN input mismatch:' + name)
    raw = (v.AUDIT / b33.SNAPSHOT).read_bytes()
    frozen = list(csv.DictReader(io.StringIO(raw.decode(), newline='')))
    texts = json.loads((v.AUDIT / b33.SHARED_SNAPSHOT).read_bytes())['files']
    prov = json.loads((v.AUDIT / 'evidence/provenance-07B33.json').read_bytes())
    dispatcher = (v.AUDIT / b33.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset, original_a, original_path = v.PHASE7_LIVE_CLI, historical_tests.A, historical_tests.Path
    original_file, original_code = v.__file__, v.main.__code__
    try:
        v.PHASE7_LIVE_CLI = dict(v.PHASE7_B32_CLI)
        with b33.historical_b32_inputs(v, frozen, texts, raw,
                prov['historical_checker_sources_at_entry'], dispatcher):
            historical_tests.A = v.AUDIT
            historical_tests.Path = type(v.AUDIT)
            suite = unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases() != 52:
                raise ValueError('Exactly ALL52 original B32 cases required')
            print('Historical B32: ALL52 UNMODIFIED cases; OWN334/raw335CRLF/indexes/'
                  'presetB32; module-local A/Path for119 source assertion identities/dispatcher TEXT. '
                  'NOT current B33 parser/123 execution tools,NOT old code or ERP.', file=sys.stderr)
            run = unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun != 52 or run.skipped:
                raise ValueError('No B32 case may be filtered or skipped')
            if v.__file__ != original_file or v.main.__code__ is not original_code:
                raise ValueError('Executing dispatcher identity must not change')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A = original_a
        historical_tests.Path = original_path
        v.PHASE7_LIVE_CLI = original_preset


if __name__ == '__main__':
    raise SystemExit(main())
