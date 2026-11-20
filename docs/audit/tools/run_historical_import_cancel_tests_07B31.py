#!/usr/bin/env python3
"""Run ALL52 unchanged B30 cases with exact OWN332/presetB30/source inputs.

B30 tests40/41/45 assert their real B30 parser,canonical dispatcher TEXT and
111 capture identities. In this explicit HISTORY child only, inject a local
Path TYPE/A and presetB30 as declared assertion inputs. No shared pathlib,
subprocess,old code execution,disk overlay,skip,protected edit or rebaseline.
Real B31 parser/AST and115 tools are independently checked by the B31 suite.
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
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--through-part',required=True,choices=('B30',));parser.parse_args()
    import validate_audit as v
    import validate_navigation_load_part as b31
    import test_import_cancel_audit_validator as historical_tests
    for name,h in ((b31.SNAPSHOT,b31.SNAPSHOT_SHA),(b31.SHARED_SNAPSHOT,b31.SHARED_SHA),(b31.DISPATCHER_SNAPSHOT,b31.DISPATCHER_SHA),('evidence/provenance-07B31.json',b31.PROVENANCE_SHA)):
        if v.sha(v.AUDIT/name)!=h:raise ValueError('B30 OWN input mismatch:'+name)
    raw=(v.AUDIT/b31.SNAPSHOT).read_bytes();frozen=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));texts=json.loads((v.AUDIT/b31.SHARED_SNAPSHOT).read_bytes())['files'];prov=json.loads((v.AUDIT/'evidence/provenance-07B31.json').read_bytes());dispatcher=(v.AUDIT/b31.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset,original_a,original_path=v.PHASE7_LIVE_CLI,historical_tests.A,historical_tests.Path
    original_file,original_code=v.__file__,v.main.__code__
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B30_CLI)
        with b31.historical_b30_inputs(v,frozen,texts,raw,prov['historical_checker_sources_at_entry'],dispatcher):
            historical_tests.A=v.AUDIT
            historical_tests.Path=type(v.AUDIT)
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=52:raise ValueError('Exactly ALL52 original B30 cases required')
            print('Historical B30: ALL52 UNMODIFIED cases; OWN332/raw333CRLF/indexes/presetB30; module-local A/Path for exact111 source-assertion inputs/dispatcher TEXT. NOT current B31 parser/115 execution tools,NOT old code or ERP.',file=sys.stderr)
            run=unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun!=52 or run.skipped:raise ValueError('No B30 case may be filtered or skipped')
            if v.__file__!=original_file or v.main.__code__ is not original_code:raise ValueError('Executing dispatcher identity must never change')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a
        historical_tests.Path=original_path
        v.PHASE7_LIVE_CLI=original_preset


if __name__=='__main__':
    raise SystemExit(main())
