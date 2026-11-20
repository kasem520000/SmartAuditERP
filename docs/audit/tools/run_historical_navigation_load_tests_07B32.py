#!/usr/bin/env python3
"""Run ALL48 unmodified B31 cases with OWN333/presetB31/source assertion data.

B31 source assertions require115 historical paths/identities and canonical
B31 dispatcher TEXT. In this explicit HISTORY child only,A and Path TYPE
are test-module local inputs. No old dispatcher code,process-global pathlib
or subprocess mutation,disk overlay,protected-test edit,skip or rebaseline.
B32 tests independently inspect the executing parser/19 gates/119 real tools.
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
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--through-part',required=True,choices=('B31',));parser.parse_args()
    import validate_audit as v
    import validate_editor_close_part as b32
    import test_navigation_load_audit_validator as historical_tests
    for name,h in ((b32.SNAPSHOT,b32.SNAPSHOT_SHA),(b32.SHARED_SNAPSHOT,b32.SHARED_SHA),(b32.DISPATCHER_SNAPSHOT,b32.DISPATCHER_SHA),('evidence/provenance-07B32.json',b32.PROVENANCE_SHA)):
        if v.sha(v.AUDIT/name)!=h:raise ValueError('B31 OWN input mismatch:'+name)
    raw=(v.AUDIT/b32.SNAPSHOT).read_bytes();frozen=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));texts=json.loads((v.AUDIT/b32.SHARED_SNAPSHOT).read_bytes())['files'];prov=json.loads((v.AUDIT/'evidence/provenance-07B32.json').read_bytes());dispatcher=(v.AUDIT/b32.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset,original_a,original_path=v.PHASE7_LIVE_CLI,historical_tests.A,historical_tests.Path
    original_file,original_code=v.__file__,v.main.__code__
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B31_CLI)
        with b32.historical_b31_inputs(v,frozen,texts,raw,prov['historical_checker_sources_at_entry'],dispatcher):
            historical_tests.A=v.AUDIT
            historical_tests.Path=type(v.AUDIT)
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=48:raise ValueError('Exactly ALL48 original B31 cases required')
            print('Historical B31: ALL48 UNMODIFIED cases; OWN333/raw334CRLF/indexes/presetB31; module-local A/Path for exact115 source-assertion inputs/dispatcher TEXT. NOT current B32 parser/119 execution tools,NOT old code or ERP.',file=sys.stderr)
            run=unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun!=48 or run.skipped:raise ValueError('No B31 case may be filtered or skipped')
            if v.__file__!=original_file or v.main.__code__ is not original_code:raise ValueError('Executing dispatcher identity must never change')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a
        historical_tests.Path=original_path
        v.PHASE7_LIVE_CLI=original_preset


if __name__=='__main__':
    raise SystemExit(main())
