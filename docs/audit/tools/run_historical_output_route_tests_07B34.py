#!/usr/bin/env python3
"""ALL52 original B33 documentary cases,OWN335/preset33/assertion DATA.

123 historical source identities and canonical dispatcher TEXT are module-local
A/Path inputs only. No old dispatcher code,global pathlib/shared-subprocess
patch,test filtering/skips,protected edits or disk overlay. Current B34 parser/
19 gates/127 execution tools are checked independently by B34's new suite.
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
    parser.add_argument('--through-part',required=True,choices=('B33',))
    parser.parse_args()
    import validate_audit as v
    import validate_messaging_request_part as b34
    import test_output_route_audit_validator as historical_tests
    for name,digest in ((b34.SNAPSHOT,b34.SNAPSHOT_SHA),(b34.SHARED_SNAPSHOT,b34.SHARED_SHA),
        (b34.DISPATCHER_SNAPSHOT,b34.DISPATCHER_SHA),('evidence/provenance-07B34.json',b34.PROVENANCE_SHA)):
        if v.sha(v.AUDIT/name)!=digest:raise ValueError('B33 OWN input mismatch:'+name)
    raw=(v.AUDIT/b34.SNAPSHOT).read_bytes();frozen=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
    texts=json.loads((v.AUDIT/b34.SHARED_SNAPSHOT).read_bytes())['files']
    prov=json.loads((v.AUDIT/'evidence/provenance-07B34.json').read_bytes())
    dispatcher=(v.AUDIT/b34.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset,original_a,original_path=v.PHASE7_LIVE_CLI,historical_tests.A,historical_tests.Path
    original_file,original_code=v.__file__,v.main.__code__
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B33_CLI)
        with b34.historical_b33_inputs(v,frozen,texts,raw,prov['historical_checker_sources_at_entry'],dispatcher):
            historical_tests.A=v.AUDIT
            historical_tests.Path=type(v.AUDIT)
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=52:raise ValueError('Exactly ALL52 original B33 cases required')
            print('Historical B33: ALL52 UNMODIFIED;OWN335/raw336CRLF/indexes/presetB33;'
                  'module-local A/Path for123 source assertion identities/dispatcher TEXT;'
                  'NOT current B34 parser/127 execution tools,NOT old code or ERP.',file=sys.stderr)
            run=unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun!=52 or run.skipped:raise ValueError('No B33 case may be skipped or filtered')
            if v.__file__!=original_file or v.main.__code__ is not original_code:raise ValueError('Executing identity must not change')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a
        historical_tests.Path=original_path
        v.PHASE7_LIVE_CLI=original_preset


if __name__=='__main__':
    raise SystemExit(main())
