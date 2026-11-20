#!/usr/bin/env python3
"""ALL52 protected B27 cases, OWN329/raw330CRLF/indexes, explicit presetB27.

Historical B27 assertions describe that cutoff, not current B28 default.
Suite-local A uses the context-local OWN registry Path. No protected edits,
skips/filter, process-global Path/shared subprocess patch or disk overlay.
Actual current B28 parser/routing is tested independently by its new suite.
"""
from __future__ import annotations
import argparse
import csv
import io
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--through-part', required=True, choices=('B27',))
    parser.parse_args()
    import validate_audit as v
    import validate_search_snapshot_part as b28
    import test_invoice_search_audit_validator as historical_tests
    raw = (v.AUDIT / b28.SNAPSHOT).read_bytes()
    if (v.sha(v.AUDIT / b28.SNAPSHOT) != b28.SNAPSHOT_SHA
            or v.sha(v.AUDIT / b28.SHARED_SNAPSHOT) != b28.SHARED_SHA):
        raise ValueError('B27 OWN inputs must match frozen byte identities')
    frozen = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    texts = json.loads((v.AUDIT / b28.SHARED_SNAPSHOT).read_text())['files']
    original_preset, original_a = v.PHASE7_LIVE_CLI, historical_tests.A
    try:
        v.PHASE7_LIVE_CLI = dict(v.PHASE7_B27_CLI)
        with b28.historical_b27_inputs(v, frozen, texts, raw):
            historical_tests.A = v.AUDIT
            suite = unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases() != 52:
                raise ValueError('Exactly ALL52 original B27 cases required')
            print('Historical B27 child: ALL52 original cases; OWN329/raw330CRLF/indexes; '
                  'suite-local A and explicit presetB27; NOT current B28 or ERP.', file=sys.stderr)
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            if result.testsRun != 52 or result.skipped:
                raise ValueError('No B27 case may be skipped/filtered')
            return 0 if result.wasSuccessful() else 1
    finally:
        historical_tests.A = original_a
        v.PHASE7_LIVE_CLI = original_preset


if __name__ == '__main__':
    raise SystemExit(main())
