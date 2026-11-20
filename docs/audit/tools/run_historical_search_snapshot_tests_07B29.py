#!/usr/bin/env python3
"""ALL48 protected B28 cases, OWN330/raw331CRLF/indexes, explicit presetB28.

Historical B28 assertions describe that cutoff, not current B29 default.
Suite-local A uses the context-local OWN registry Path. No protected edits,
skips/filter, process-global Path/shared subprocess patch or disk overlay.
Actual current B29 parser/routing is tested independently by its new suite.
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
    parser.add_argument('--through-part', required=True, choices=('B28',))
    parser.parse_args()
    import validate_audit as v
    import validate_dirty_navigation_part as b29
    import test_search_snapshot_audit_validator as historical_tests
    raw = (v.AUDIT / b29.SNAPSHOT).read_bytes()
    if (v.sha(v.AUDIT / b29.SNAPSHOT) != b29.SNAPSHOT_SHA
            or v.sha(v.AUDIT / b29.SHARED_SNAPSHOT) != b29.SHARED_SHA):
        raise ValueError('B28 OWN inputs must match frozen byte identities')
    frozen = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    texts = json.loads((v.AUDIT / b29.SHARED_SNAPSHOT).read_text())['files']
    original_preset, original_a = v.PHASE7_LIVE_CLI, historical_tests.A
    try:
        v.PHASE7_LIVE_CLI = dict(v.PHASE7_B28_CLI)
        with b29.historical_b28_inputs(v, frozen, texts, raw):
            historical_tests.A = v.AUDIT
            suite = unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases() != 48:
                raise ValueError('Exactly ALL48 original B28 cases required')
            print('Historical B28 child: ALL48 original cases; OWN330/raw331CRLF/indexes; '
                  'suite-local A and explicit presetB28; NOT current B29 or ERP.', file=sys.stderr)
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            if result.testsRun != 48 or result.skipped:
                raise ValueError('No B28 case may be skipped/filtered')
            return 0 if result.wasSuccessful() else 1
    finally:
        historical_tests.A = original_a
        v.PHASE7_LIVE_CLI = original_preset


if __name__ == '__main__':
    raise SystemExit(main())
