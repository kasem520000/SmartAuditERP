#!/usr/bin/env python3
"""ALL52 original B36 cases,OWN335/raw336/preset36/historical135 assertions.

Dispatcher TEXT/135 identities are child-local A/Path assertion DATA,not old
executable code or actual139 B37 tools. No global Path/shared-subprocess patch,
overlay,protected edits,skips/filter/rebaseline. Restore even on exceptions.
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
    parser.add_argument('--through-part',required=True,choices=('B36',))
    parser.parse_args()
    import validate_audit as v
    import validate_transfer_picker_part as b37
    import test_invoice_picker_audit_validator as historical_tests
    for name,digest in ((b37.SNAPSHOT,b37.SNAPSHOT_SHA),(b37.SHARED_SNAPSHOT,b37.SHARED_SHA),(b37.DISPATCHER_SNAPSHOT,b37.DISPATCHER_SHA),('evidence/provenance-07B37.json',b37.PROVENANCE_SHA)):
        if v.sha(v.AUDIT/name)!=digest:raise ValueError('B36 OWN input mismatch:'+name)
    raw=(v.AUDIT/b37.SNAPSHOT).read_bytes();frozen=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
    texts=json.loads((v.AUDIT/b37.SHARED_SNAPSHOT).read_bytes())['files'];prov=json.loads((v.AUDIT/'evidence/provenance-07B37.json').read_bytes());dispatcher=(v.AUDIT/b37.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset,original_a,original_path=v.PHASE7_LIVE_CLI,historical_tests.A,historical_tests.Path
    original_file,original_code=v.__file__,v.main.__code__
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B36_CLI)
        with b37.historical_b36_inputs(v,frozen,texts,raw,prov['historical_checker_sources_at_entry'],dispatcher):
            historical_tests.A=v.AUDIT;historical_tests.Path=type(v.AUDIT)
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=52:raise ValueError('Exactly ALL52 original B36 cases required')
            print('Historical B36: ALL52 UNMODIFIED;OWN335/raw336CRLF/indexes/presetB36;child-local A/Path for135 historical source assertion identities and dispatcher TEXT;NOT actual LIVE37/139 tools,NOT old code or ERP.',file=sys.stderr)
            run=unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun!=52 or run.skipped:raise ValueError('No B36 case may be skipped or filtered')
            if v.__file__!=original_file or v.main.__code__ is not original_code:raise ValueError('Executing identity must not change')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a;historical_tests.Path=original_path;v.PHASE7_LIVE_CLI=original_preset


if __name__=='__main__':raise SystemExit(main())
