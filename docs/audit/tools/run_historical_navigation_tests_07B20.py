#!/usr/bin/env python3
"""Run ALL36 unmodified B19 cases in an explicit historical B19-preset child.

The historical parser assertions are not today's B20 default. No protected test
method edits, skip/filter, disk overlay or global subprocess/Path patch. Current
B20 tests inspect the actual default and entrypoint independently.
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
    parser.add_argument('--through-part',required=True,choices=('B19',))
    parser.parse_args()
    import validate_audit as v
    import test_navigation_contract_audit_validator as historical_tests
    original=v.PHASE7_LIVE_CLI
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B19_CLI)
        suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
        if suite.countTestCases()!=36:raise ValueError('Exactly ALL36 original B19 cases required')
        print('Historical B19 child: ALL36 original cases; explicit parser preset B19; NOT current B20 default or ERP tests.',file=sys.stderr)
        result=unittest.TextTestRunner(verbosity=1).run(suite)
        if result.testsRun!=36 or result.skipped:raise ValueError('No B19 case may be skipped/filtered')
        return 0 if result.wasSuccessful()else 1
    finally:
        v.PHASE7_LIVE_CLI=original


if __name__=='__main__':raise SystemExit(main())
