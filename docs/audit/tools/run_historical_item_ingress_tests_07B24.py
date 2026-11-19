#!/usr/bin/env python3
"""ALL44 protected B23 cases with OWN319/raw320CRLF/indexes and presetB23.

B23 assertions describe its historical cutoff, not today's B24 default. The
suite's A/registry read uses the context-local Path from the OWN319 adapter.
No protected edits/skips/filter/global pathlib/shared subprocess patch or disk
overlay; actual current B24 parser/entrypoint tested independently.
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
    parser.add_argument('--through-part',required=True,choices=('B23',))
    parser.parse_args()
    import validate_audit as v
    import validate_row_ownership_part as b24
    import test_item_ingress_audit_validator as historical_tests
    raw=(v.AUDIT/b24.SNAPSHOT).read_bytes()
    if v.sha(v.AUDIT/b24.SNAPSHOT)!=b24.SNAPSHOT_SHA or v.sha(v.AUDIT/b24.SHARED_SNAPSHOT)!=b24.SHARED_SHA:
        raise ValueError('B23 OWN input hashes must match frozen identities')
    frozen=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    texts=json.loads((v.AUDIT/b24.SHARED_SNAPSHOT).read_text())['files']
    original_preset,original_a=v.PHASE7_LIVE_CLI,historical_tests.A
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B23_CLI)
        with b24.historical_b23_inputs(v,frozen,texts,raw):
            historical_tests.A=v.AUDIT
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=44:raise ValueError('Exactly ALL44 original B23 cases required')
            print('Historical B23 child: ALL44 original cases; OWN319/raw320CRLF/indexes; '
                  'suite-local A and explicit presetB23; NOT current B24 or ERP.',file=sys.stderr)
            result=unittest.TextTestRunner(verbosity=1).run(suite)
            if result.testsRun!=44 or result.skipped:raise ValueError('No B23 case may be skipped/filtered')
            return 0 if result.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a
        v.PHASE7_LIVE_CLI=original_preset

if __name__=='__main__':raise SystemExit(main())
