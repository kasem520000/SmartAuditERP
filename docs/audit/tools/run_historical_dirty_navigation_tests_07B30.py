#!/usr/bin/env python3
"""Run ALL48 protected B29 cases with their OWN331 cutoff, never current B30.

B29 test39 reads dispatcher TEXT for its historical AST assertion; test21
checks its107-tool capture vector. Supply the exact auxiliary TEXT and the
107 logical paths in a context-local A, not a process-global pathlib patch,
old-code execution, disk overlay, rebaseline or hidden test edit. Current B30
parser/AST/111 actual tool identities are checked independently by B30 tests.
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
    parser.add_argument('--through-part',required=True,choices=('B29',))
    parser.parse_args()
    import validate_audit as v
    import validate_import_cancel_part as b30
    import test_dirty_navigation_audit_validator as historical_tests
    for name,digest in ((b30.SNAPSHOT,b30.SNAPSHOT_SHA),(b30.SHARED_SNAPSHOT,b30.SHARED_SHA),
      (b30.DISPATCHER_SNAPSHOT,b30.DISPATCHER_SHA),('evidence/provenance-07B30.json',b30.PROVENANCE_SHA)):
        if v.sha(v.AUDIT/name)!=digest:raise ValueError('B29 immutable OWN input mismatch:'+name)
    raw=(v.AUDIT/b30.SNAPSHOT).read_bytes();frozen=list(csv.DictReader(io.StringIO(raw.decode('utf8'),newline='')))
    texts=json.loads((v.AUDIT/b30.SHARED_SNAPSHOT).read_text())['files']
    prov=json.loads((v.AUDIT/'evidence/provenance-07B30.json').read_text())
    dispatcher=(v.AUDIT/b30.DISPATCHER_SNAPSHOT).read_bytes()
    original_preset,original_a,original_file=v.PHASE7_LIVE_CLI,historical_tests.A,v.__file__
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B29_CLI)
        with b30.historical_b29_inputs(v,frozen,texts,raw,prov['historical_checker_sources_at_entry'],dispatcher):
            historical_tests.A=v.AUDIT
            v.__file__=str(v.AUDIT/b30.DISPATCHER_SNAPSHOT)
            suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases()!=48:raise ValueError('Exactly ALL48 original B29 cases required')
            print('Historical B29: ALL48 UNMODIFIED cases; OWN331/raw332CRLF/indexes/presetB29; '
              'suite-local A and exact107 source-assertion inputs/auxiliary dispatcher TEXT; '
              'NOT current B30 parser or actual execution-tool inventory, NOT ERP.',file=sys.stderr)
            run=unittest.TextTestRunner(verbosity=1).run(suite)
            if run.testsRun!=48 or run.skipped:raise ValueError('No B29 case may be filtered or skipped')
            return 0 if run.wasSuccessful() else 1
    finally:
        historical_tests.A=original_a
        v.PHASE7_LIVE_CLI=original_preset
        v.__file__=original_file


if __name__=='__main__':
    raise SystemExit(main())
