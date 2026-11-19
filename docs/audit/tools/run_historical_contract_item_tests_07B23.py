#!/usr/bin/env python3
"""ALL40 protected B22 cases with explicit OWN316 inputs and B22 parser preset.

B22 assertions describe its historical cutoff, not today's B23 default. The
suite's A/registry read receives the context-local Path subclass used by the
validator; no protected file changes, skip/filter, global pathlib/subprocess
patch or disk overlay. Current B23 parser/entrypoint tested independently.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
from pathlib import Path
import sys
import unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-part',required=True,choices=('B22',))
    parser.parse_args()
    import validate_audit as v
    import validate_item_ingress_part as b23
    import test_contract_item_audit_validator as historical_tests
    raw=(v.AUDIT/b23.SNAPSHOT).read_bytes()
    if v.sha(v.AUDIT/b23.SNAPSHOT)!=b23.SNAPSHOT_SHA or v.sha(v.AUDIT/b23.SHARED_SNAPSHOT)!=b23.SHARED_SHA:
        raise ValueError('B22 historical input hashes must match frozen identities')
    frozen=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    texts=json.loads((v.AUDIT/b23.SHARED_SNAPSHOT).read_text())['files']
    original_preset,original_a=v.PHASE7_LIVE_CLI,historical_tests.A
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B22_CLI)
        with b23.historical_b22_inputs(v,frozen,texts,raw):
            historical_tests.A=v.AUDIT
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=40:raise ValueError('Exactly ALL40 original B22 cases required')
            print('Historical B22 child: ALL40 original cases; OWN316/raw317CRLF/indexes; '
                  'suite-local A registry path and explicit presetB22; NOT current B23 or ERP.',file=sys.stderr)
            result=unittest.TextTestRunner(verbosity=1).run(suite)
            if result.testsRun!=40 or result.skipped:raise ValueError('No B22 case may be skipped/filtered')
            return 0 if result.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a
        v.PHASE7_LIVE_CLI=original_preset

if __name__=='__main__':raise SystemExit(main())
