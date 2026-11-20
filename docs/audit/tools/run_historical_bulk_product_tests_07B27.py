#!/usr/bin/env python3
"""ALL48 protected B26 cases, OWN326/raw327CRLF/indexes, explicit presetB26.

Historical B26 assertions describe that cutoff, not current B27 default.
Suite-local A uses the context-local OWN registry Path. No protected edits,
skips/filter, process-global Path/shared subprocess patch or disk overlay.
Actual current B27 parser/routing is tested independently by its new suite.
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
    parser.add_argument('--through-part', required=True, choices=('B26',))
    parser.parse_args()
    import validate_audit as v
    import validate_invoice_search_part as b27
    import test_bulk_product_audit_validator as historical_tests
    raw = (v.AUDIT / b27.SNAPSHOT).read_bytes()
    if (v.sha(v.AUDIT / b27.SNAPSHOT) != b27.SNAPSHOT_SHA
            or v.sha(v.AUDIT / b27.SHARED_SNAPSHOT) != b27.SHARED_SHA):
        raise ValueError('B26 OWN inputs must match frozen byte identities')
    frozen = list(csv.DictReader(io.StringIO(raw.decode('utf-8'), newline='')))
    texts = json.loads((v.AUDIT / b27.SHARED_SNAPSHOT).read_text())['files']
    original_preset, original_a = v.PHASE7_LIVE_CLI, historical_tests.A
    try:
        v.PHASE7_LIVE_CLI = dict(v.PHASE7_B26_CLI)
        with b27.historical_b26_inputs(v, frozen, texts, raw):
            historical_tests.A = v.AUDIT
            suite = unittest.defaultTestLoader.loadTestsFromModule(historical_tests)
            if suite.countTestCases() != 48:
                raise ValueError('Exactly ALL48 original B26 cases required')
            print('Historical B26 child: ALL48 original cases; OWN326/raw327CRLF/indexes; '
                  'suite-local A and explicit presetB26; NOT current B27 or ERP.', file=sys.stderr)
            result = unittest.TextTestRunner(verbosity=1).run(suite)
            if result.testsRun != 48 or result.skipped:
                raise ValueError('No B26 case may be skipped/filtered')
            return 0 if result.wasSuccessful() else 1
    finally:
        historical_tests.A = original_a
        v.PHASE7_LIVE_CLI = original_preset


if __name__ == '__main__':
    raise SystemExit(main())
