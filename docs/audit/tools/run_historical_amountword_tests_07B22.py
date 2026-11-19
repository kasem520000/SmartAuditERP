#!/usr/bin/env python3
"""Run ALL36 unmodified B21 cases with its explicit historical parser preset.

B21 parser assertions describe its own default, NOT today's B22 default. Current
B22 parser/entrypoint tests are independent. No protected test edits, filtering,
skips, filesystem overlay, global Path or shared subprocess mutation.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-part', required=True, choices=('B21',))
    parser.parse_args()
    import validate_audit as v
    import test_amountword_contract_audit_validator as historical_tests
    original = v.PHASE7_LIVE_CLI
    try:
        v.PHASE7_LIVE_CLI = dict(v.PHASE7_B21_CLI)
        suite = unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
        if suite.countTestCases() != 36:
            raise ValueError('Exactly ALL36 original B21 cases required')
        print('Historical B21 child: ALL36 original cases; explicit preset B21; '
              'NOT current B22 default or ERP tests.', file=sys.stderr)
        result = unittest.TextTestRunner(verbosity=1).run(suite)
        if result.testsRun != 36 or result.skipped:
            raise ValueError('No B21 case may be skipped/filtered')
        return 0 if result.wasSuccessful() else 1
    finally:
        v.PHASE7_LIVE_CLI = original


if __name__ == '__main__':
    raise SystemExit(main())
