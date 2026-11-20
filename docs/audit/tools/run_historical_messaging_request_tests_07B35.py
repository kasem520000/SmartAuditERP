#!/usr/bin/env python3
"""ALL52 original B34 documentary cases,OWN335/preset34/assertion DATA.

127 historical source identities and canonical dispatcher TEXT are child-local
A/Path inputs only. No old dispatcher code,global pathlib/shared-subprocess
patch,test skips/filtering,protected edits or disk overlay. B35's new suite
independently checks actual LIVE35/19gates/131 execution tools.
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
    parser.add_argument('--through-part',required=True,choices=('B34',))
    parser.parse_args()
    import validate_audit as v
    import validate_linked_return_part as b35
    import test_messaging_request_audit_validator as historical_tests
    for name,digest in ((b35.SNAPSHOT,b35.SNAPSHOT_SHA),(b35.SHARED_SNAPSHOT,b35.SHARED_SHA),
        (b35.DISPATCHER_SNAPSHOT,b35.DISPATCHER_SHA),('evidence/provenance-07B35.json',b35.PROVENANCE_SHA)):
        if v.sha(v.AUDIT/name)!=digest:raise ValueError('B34 OWN input mismatch:'+name)
    raw=(v.AUDIT/b35.SNAPSHOT).read_bytes();frozen=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
    texts=json.loads((v.AUDIT/b35.SHARED_SNAPSHOT).read_bytes())['files']
    prov=json.loads((v.AUDIT/'evidence/provenance-07B35.json').read_bytes());dispatcher=(v.AUDIT/b35.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset,original_a,original_path=v.PHASE7_LIVE_CLI,historical_tests.A,historical_tests.Path
    original_file,original_code=v.__file__,v.main.__code__
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B34_CLI)
        with b35.historical_b34_inputs(v,frozen,texts,raw,prov['historical_checker_sources_at_entry'],dispatcher):
            historical_tests.A=v.AUDIT;historical_tests.Path=type(v.AUDIT)
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=52:raise ValueError('Exactly ALL52 original B34 cases required')
            print('Historical B34: ALL52 UNMODIFIED;OWN335/raw336CRLF/indexes/presetB34;'
                  'child-local A/Path for127 source assertion identities/dispatcher TEXT;'
                  'NOT current B35 parser/131 execution tools,NOT old code or ERP.',file=sys.stderr)
            run=unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun!=52 or run.skipped:raise ValueError('No B34 case may be skipped or filtered')
            if v.__file__!=original_file or v.main.__code__ is not original_code:raise ValueError('Executing identity must not change')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a;historical_tests.Path=original_path;v.PHASE7_LIVE_CLI=original_preset


if __name__=='__main__':raise SystemExit(main())
