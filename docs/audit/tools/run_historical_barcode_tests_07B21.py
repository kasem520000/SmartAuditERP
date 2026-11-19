#!/usr/bin/env python3
"""Run ALL32 unmodified B20 cases in an explicit historical B20-preset child.

B20 parser assertions describe its historical default, not today's B21 parser.
No protected method edits, skips, filters, disk overlays, global Path or shared
subprocess patches. Current B21 tests inspect the real default independently.
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
    parser.add_argument('--through-part',required=True,choices=('B20',))
    parser.parse_args()
    import validate_audit as v
    import test_barcode_contract_audit_validator as historical_tests
    original=v.PHASE7_LIVE_CLI
    try:
        v.PHASE7_LIVE_CLI=dict(v.PHASE7_B20_CLI)
        suite=unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
        if suite.countTestCases()!=32:raise ValueError('Exactly ALL32 original B20 cases required')
        print('Historical B20 child: ALL32 original cases; explicit parser preset B20; NOT current B21 default or ERP tests.',file=sys.stderr)
        result=unittest.TextTestRunner(verbosity=1).run(suite)
        if result.testsRun!=32 or result.skipped:raise ValueError('No B20 case may be skipped/filtered')
        return 0 if result.wasSuccessful()else 1
    finally:
        v.PHASE7_LIVE_CLI=original


if __name__=='__main__':raise SystemExit(main())
