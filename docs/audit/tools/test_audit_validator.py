#!/usr/bin/env python3
"""Tests of AUDIT-DOCUMENT CHECKER helpers only, never SmartAuditERP tests.

Stdlib; imports only the sibling audit validator. Uses synthetic dictionaries
and range strings, no application imports, Git command, SQL, COM, build, file
writes or network. No finding is remediated/closed by passing these tests.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("audit_document_validator", Path(__file__).with_name("validate_audit.py"))
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class AuditDocumentCheckerTests(unittest.TestCase):
    def setUp(self):
        validator.ERRORS.clear()
        self.original = {
            "id": "P1-001", "severity": "High", "certainty": "potential", "type": "synthetic",
            "status": "open-not-remediated", "title": "synthetic audit row",
            "evidence": "example.cs:1-2", "next_phase": "7;8",
        }

    def tearDown(self):
        validator.ERRORS.clear()

    def test_partial_phase_preserves_followups_with_append_only_extension(self):
        updated = dict(self.original, evidence=self.original["evidence"] + ";example.cs:3-4")
        result = validator.transition([self.original], [updated], 7, {"P1-001"}, preserve_followups=True)
        self.assertEqual(result, ["P1-001"])
        self.assertEqual(validator.ERRORS, [])
        self.assertEqual(updated["next_phase"], "7;8")

    def test_partial_phase_rejects_silently_dropping_phase7(self):
        updated = dict(self.original, next_phase="8")
        validator.transition([self.original], [updated], 7, set(), preserve_followups=True)
        self.assertTrue(any("next_phase" in e for e in validator.ERRORS))

    def test_completed_historical_phase_rule_remains_separate(self):
        original = dict(self.original, next_phase="3;8")
        updated = dict(original, next_phase="8")
        validator.transition([original], [updated], 3, set())
        self.assertEqual(validator.ERRORS, [])

    def test_historical_core_classification_change_is_rejected(self):
        updated = dict(self.original, severity="Medium")
        validator.transition([self.original], [updated], 7, set(), preserve_followups=True)
        self.assertTrue(any("core field changed" in e for e in validator.ERRORS))

    def test_historical_evidence_cannot_be_replaced(self):
        updated = dict(self.original, evidence="different.cs:1-2")
        validator.transition([self.original], [updated], 7, {"P1-001"}, preserve_followups=True)
        self.assertTrue(any("removed/replaced" in e for e in validator.ERRORS))

    def test_undeclared_extension_is_rejected(self):
        updated = dict(self.original, evidence=self.original["evidence"] + ";example.cs:3-4")
        validator.transition([self.original], [updated], 7, set(), preserve_followups=True)
        self.assertTrue(any("Undeclared evidence extension" in e for e in validator.ERRORS))

    def test_acceptance_plan_cannot_claim_execution(self):
        proposed = {k: "synthetic nonempty text" for k in (
            "scenario", "prerequisites", "procedure", "acceptance_criterion", "safety_controls", "invariant_ids", "evidence")}
        proposed.update(id="P7T-01", status="not-executed")
        validator.proposed_tests([proposed], "P7A")
        self.assertEqual(validator.ERRORS, [])
        executed = copy.deepcopy(proposed)
        executed["status"] = "passed"
        validator.proposed_tests([executed], "P7A")
        self.assertTrue(any("execution claim" in e for e in validator.ERRORS))

    def test_unknown_feature_association_is_rejected(self):
        validator.related([{"id": "P7T-01", "feature_ids": "FE7-01;FE7-99"}], {"FE7-01"}, "feature_ids")
        self.assertTrue(any("FE7-99" in e for e in validator.ERRORS))

    def test_source_slice_outside_selected_range_is_rejected(self):
        scope = {"example.cs": [(1, 4), (8, 12)]}
        validator.scoped_evidence("example.cs:2-3", scope, "synthetic", phase=7)
        self.assertEqual(validator.ERRORS, [])
        validator.scoped_evidence("example.cs:3-9", scope, "synthetic", phase=7)
        self.assertTrue(any("outside selected scope" in e for e in validator.ERRORS))

    def test_malformed_range_is_not_silently_accepted(self):
        self.assertEqual(validator.spans("1-3;8;10–12"), [(1, 3), (8, 8), (10, 12)])
        with self.assertRaises(ValueError):
            validator.spans("1-3;not-a-range")


if __name__ == "__main__":
    unittest.main(verbosity=2)
