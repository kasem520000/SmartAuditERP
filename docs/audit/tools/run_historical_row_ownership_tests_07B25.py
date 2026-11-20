#!/usr/bin/env python3
"""ALL44 protected B24 cases, OWN322/raw323CRLF/indexes, explicit presetB24.

Historical B24 assertions describe that cutoff, not current B25 default.
Suite-local A uses the context-local OWN registry Path. No protected edits,
skips/filter, process-global Path/shared subprocess patch or disk overlay.
Actual current B25 parser/routing is tested independently by its new suite.
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
    parser.add_argument('--through-part',required=True,choices=('B24',))
    parser.parse_args()
    import validate_audit as v
    import validate_property_dialog_part as b25
    import test_row_ownership_audit_validator as historical_tests
    raw=(v.AUDIT/b25.SNAPSHOT).read_bytes()
    if v.sha(v.AUDIT/b25.SNAPSHOT)!=b25.SNAPSHOT_SHA or v.sha(v.AUDIT/b25.SHARED_SNAPSHOT)!=b25.SHARED_SHA:
        raise ValueError('B24 OWN inputs must match frozen byte identities')
    frozen=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    texts=json.loads((v.AUDIT/b25.SHARED_SNAPSHOT).read_text())['files']
    original_preset,original_a=v.PHASE7_LIVE_CLI,historical_tests.A
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B24_CLI)
        with b25.historical_b24_inputs(v,frozen,texts,raw):
            historical_tests.A=v.AUDIT
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=44:raise ValueError('Exactly ALL44 original B24 cases required')
            print('Historical B24 child: ALL44 original cases; OWN322/raw323CRLF/indexes; '
                  'suite-local A and explicit presetB24; NOT current B25 or ERP.',file=sys.stderr)
            result=unittest.TextTestRunner(verbosity=1).run(suite)
            if result.testsRun!=44 or result.skipped:raise ValueError('No B24 case may be skipped/filtered')
            return 0 if result.wasSuccessful()else 1
    finally:
        historical_tests.A=original_a
        v.PHASE7_LIVE_CLI=original_preset

if __name__=='__main__':raise SystemExit(main())
