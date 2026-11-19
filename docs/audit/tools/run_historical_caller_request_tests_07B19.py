#!/usr/bin/env python3
"""Execute ALL28 unmodified B18 cases with an explicit historical parser preset.

A dedicated child process, ONLY --through-part B18. No disk overlay/test edits,
no test method replacement/skips/filtering, no global subprocess/Path patches.
The historical B18 parser assertions describe B18's preset, not the current B19
CLI default; current B19 tests independently inspect the real default/entrypoint.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-part',required=True,choices=('B18',))
    args=parser.parse_args()
    import validate_audit as v
    import test_caller_request_audit_validator as historical_tests
    original=v.PHASE7_LIVE_CLI
    try:
        # Versioned options base, isolated in this explicitly named child only.
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B18_CLI)
        suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
        if suite.countTestCases()!=28:raise ValueError('Exactly ALL28 B18 cases required')
        print('Historical B18 child: ALL28 original cases; parser preset B18; NOT current B19 default or ERP tests.',file=sys.stderr)
        result=unittest.TextTestRunner(verbosity=1).run(suite)
        if result.testsRun!=28 or result.skipped:raise ValueError('No B18 case may be skipped/filtered')
        return 0 if result.wasSuccessful()else 1
    finally:
        v.PHASE7_LIVE_CLI=original


if __name__=='__main__':raise SystemExit(main())
