#!/usr/bin/env python3
"""Documentary-tool tests only. No ERP/WPF/SQL/SDK/provider execution.

Mutations are in-memory fixtures. Repository evidence and the legacy dispatcher
are never rewritten, overlaid, rebased, skipped, monkey-patched or re-executed
as historical code. A synthetic approval fixture is not an actual approval.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from build_7b_census import (ROOT, compact_spans, decode_source, numeric_spans,
                             read_rows, row_sha, sha, xml_entries)
import validate_7b_completion as checker

A = ROOT / 'docs/audit'
E = A / 'evidence'


class SpanAndDiscoveryTests(unittest.TestCase):
    def test_singleton_range_is_not_discarded(self):
        self.assertEqual(numeric_spans('332'), [(332, 332)])

    def test_mixed_inclusive_range_formats(self):
        self.assertEqual(numeric_spans('1-3; 5,7–9،12'), [(1, 3), (5, 5), (7, 9), (12, 12)])

    def test_range_compaction_round_trip(self):
        lines = {1, 2, 3, 7, 8, 11}
        self.assertEqual(compact_spans(lines), '1-3;7-8;11')
        self.assertEqual({n for a, b in numeric_spans(compact_spans(lines)) for n in range(a, b + 1)}, lines)

    def test_invalid_ranges_rejected(self):
        for value in ('0', '4-2', 'all-lines', '1:4'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                numeric_spans(value)

    def test_utf8_bom_and_cp1256_are_read_only(self):
        text = 'قراءة المصدر فقط'
        self.assertEqual(decode_source(b'\xef\xbb\xbf' + text.encode('utf8'))[0], text)
        legacy = text.encode('cp1256')
        self.assertEqual(decode_source(legacy), (text, 'cp1256-strict-read-only-fallback'))
        self.assertEqual(legacy, text.encode('cp1256'))

    def test_utf16_bom_is_not_a_compiler_claim(self):
        text = '<Window />'
        self.assertEqual(decode_source(text.encode('utf16')), (text, 'utf-16-bom'))

    def test_xaml_click_is_only_possible_entry(self):
        result, xclass, error = xml_entries('<Window xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" x:Class="App.Sample"><Button Click="OnClick"/></Window>', {'OnClick'})
        self.assertEqual((xclass, error), ('App.Sample', None))
        self.assertEqual(result[0]['handler'], 'OnClick')
        self.assertIn('not-registration-proof', result[0]['kind'])

    def test_xaml_command_binding_is_not_resolved_as_handler(self):
        entries, _, error = xml_entries('<Window><Button Command="{Binding PrintCommand}" /></Window>', set())
        self.assertIsNone(error)
        self.assertEqual(entries[0]['kind'], 'command-attribute-not-binding-resolved')
        self.assertIsNone(entries[0]['handler'])
        self.assertIsNone(entries[0]['literal_command_name'])

    def test_malformed_xml_remains_explicit(self):
        _, _, error = xml_entries('<Window><Button></Window>', set())
        self.assertIsNotNone(error)

    def test_comments_do_not_create_xaml_events(self):
        entries, _, error = xml_entries('<Window><!-- <Button Click="Hidden" /> --></Window>', {'Hidden'})
        self.assertEqual(entries, [])
        self.assertIsNone(error)


class ClosurePolicyTests(unittest.TestCase):
    def setUp(self):
        self.inputs = json.loads((E / 'closure-inputs-07B38.json').read_bytes())
        self.caps = read_rows(E / 'capability-register-07B38.csv')

    def hypothetical_complete(self):
        # In-memory policy test ONLY; no actual scope/family/handoff approval.
        inputs = deepcopy(self.inputs)
        for key in checker.APPROVAL_FIELDS:
            inputs[key] = {'decision': 'approved', 'owner_role': 'synthetic unit fixture',
                           'source_evidence': 'synthetic unit fixture, not a user decision'}
        for key in checker.CLOSURE_FLAGS:
            inputs[key] = True
        caps = deepcopy(self.caps)
        for cap in caps:
            cap['local_semantic_obligations_complete'] = 'true'
            cap['whole_capability_certified'] = 'true'
        return inputs, caps

    def test_current_whole7B_remains_open(self):
        decision = checker.evaluate_closure(self.inputs, self.caps)
        self.assertFalse(decision['whole_7B_complete'])
        self.assertIn('scope_approval-not-approved', decision['blockers'])

    def test_integrity_and_large_counts_never_close_scope(self):
        self.inputs.update(integrity_ok=True, findings=335, documentary_cases=999999,
                           source_count=477, historical_FE_rows=797, tests_passed=True)
        self.assertFalse(checker.evaluate_closure(self.inputs, self.caps)['whole_7B_complete'])

    def test_external_handoff_is_not_whole_family_approval(self):
        inputs, caps = self.hypothetical_complete()
        inputs['whole_family_approval'] = None
        result = checker.evaluate_closure(inputs, caps)
        self.assertFalse(result['whole_7B_complete'])
        self.assertIn('whole_family_approval-not-approved', result['blockers'])

    def test_scope_approval_cannot_excuse_local_omissions(self):
        inputs, caps = self.hypothetical_complete()
        inputs['all_local_semantic_obligations_complete'] = False
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_open_candidate_dispositions_block_completion(self):
        inputs, caps = self.hypothetical_complete()
        inputs['all_required_candidates_dispositioned'] = False
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_unadjudicated_source_observations_block_completion(self):
        inputs, caps = self.hypothetical_complete()
        inputs['all_open_observations_adjudicated'] = False
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_each_capability_must_have_a_decision(self):
        inputs, caps = self.hypothetical_complete()
        caps[3]['whole_capability_certified'] = 'false'
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_each_capability_local_obligation_must_be_complete(self):
        inputs, caps = self.hypothetical_complete()
        caps[-1]['local_semantic_obligations_complete'] = 'false'
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_empty_register_cannot_vacuously_complete(self):
        inputs, _ = self.hypothetical_complete()
        self.assertFalse(checker.evaluate_closure(inputs, [])['whole_7B_complete'])

    def test_approval_string_and_bare_boolean_rejected(self):
        for fake in (True, 'approved', {}, {'decision': 'approved'}):
            self.assertFalse(checker.is_approval(fake))

    def test_truthy_string_is_not_proof(self):
        inputs, caps = self.hypothetical_complete()
        inputs['all_local_semantic_obligations_complete'] = 'true'
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_phase7C_and8_are_not_silently_started(self):
        for key in ('phase_7C_started', 'phase_8_authorized'):
            inputs, caps = self.hypothetical_complete()
            inputs[key] = True
            self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_repair_execution_cannot_be_called_audit_only(self):
        inputs, caps = self.hypothetical_complete()
        inputs['application_remediation_performed'] = True
        self.assertFalse(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])

    def test_policy_is_not_permanently_hardcoded_to_open(self):
        inputs, caps = self.hypothetical_complete()
        self.assertTrue(checker.evaluate_closure(inputs, caps)['whole_7B_complete'])
        # The hypothetical fixtures are not the persisted real evidence.
        self.assertIsNone(json.loads((E / 'closure-inputs-07B38.json').read_bytes())['scope_approval'])


class LineageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lineage = read_rows(E / 'feature-lineage-07B38.csv')
        cls.upstream, cls.hashes = {}, {}
        for part in range(1, 38):
            rel = f'evidence/feature-implementation-matrix-07B{part}.csv'
            cls.upstream[f'7B{part}'] = read_rows(A / rel)
            cls.hashes[rel] = sha((A / rel).read_bytes())

    def errors(self, rows):
        return checker.lineage_errors(rows, self.upstream, self.hashes)

    def test_all797_rows_reconcile_exactly(self):
        self.assertEqual(len(self.lineage), 797)
        self.assertEqual(self.errors(self.lineage), [])

    def test_omitted_last_row_fails(self):
        self.assertIn('lineage row count/omission', self.errors(self.lineage[:-1]))

    def test_duplicate_identity_fails(self):
        data = deepcopy(self.lineage)
        data[-1] = deepcopy(data[-2])
        self.assertIn('lineage duplicate upstream identity', self.errors(data))

    def test_reordered_rows_fail_even_if_set_is_same(self):
        data = deepcopy(self.lineage)
        data[0], data[1] = data[1], data[0]
        self.assertTrue(self.errors(data))

    def test_changed_upstream_file_hash_fails(self):
        data = deepcopy(self.lineage)
        data[0]['upstream_file_sha256'] = '0' * 64
        self.assertTrue(self.errors(data))

    def test_changed_dictionary_with_old_row_hash_fails(self):
        data = deepcopy(self.lineage)
        original = json.loads(data[0]['canonical_row_json'])
        original['implementation_status'] = 'invented-complete'
        data[0]['canonical_row_json'] = json.dumps(original)
        self.assertTrue(self.errors(data))

    def test_evidence_and_acceptance_not_retyped(self):
        data = deepcopy(self.lineage)
        data[0]['prior_evidence'] = 'invented source'
        data[1]['prior_acceptance_ids'] = 'invented passed test'
        self.assertTrue(self.errors(data))

    def test_dictionary_hash_is_key_order_independent(self):
        self.assertEqual(row_sha({'a': 'ع', 'b': 'b'}), row_sha({'b': 'b', 'a': 'ع'}))


class RepositoryIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = checker.validate()
        cls.census = json.loads((E / 'capability-census-07B38.json').read_bytes())

    def test_integrity_pass_is_distinct_from_closure(self):
        self.assertEqual(self.report['integrity_errors'], [])
        self.assertTrue(self.report['integrity_ok'])
        self.assertFalse(self.report['closure']['whole_7B_complete'])

    def test_generated_csharp_is_not_source_parse_denominator(self):
        self.assertEqual(len(self.census['source_files']), 477)
        self.assertTrue(all('/obj/' not in r['path'] for r in self.census['source_files']))
        self.assertEqual(len(self.census['xaml_files']), 277)

    def test_many_Show_homonyms_are_not_certified_report_calls(self):
        show = [r for r in self.census['candidate_sites'] if r['target'] == 'Show']
        self.assertEqual(len(show), 3419)
        self.assertTrue(all('not-type-resolved' in r['kind'] for r in show))
        self.assertFalse(self.census['capability_denominator_agreed'])

    def test_direct_dialog_counts_and_owner_reuse(self):
        rows = read_rows(E / 'direct-dialog-contracts-07B38.csv')
        self.assertEqual(len(rows), 49)
        self.assertEqual(sum(r['target'] == 'frmItemsSrch' for r in rows), 28)
        self.assertEqual(sum(r['target'] == 'frmInvoiceSrch' for r in rows), 16)
        self.assertEqual(len({(r['path'], r['owner_start'], r['owner_end']) for r in rows}), 47)

    def test_selected_nonaccept_paths_are_not_equated(self):
        rows = read_rows(E / 'direct-dialog-contracts-07B38.csv')
        find = lambda name: next(r for r in rows if r['path'].endswith('/' + name) and r['target'] == 'frmItemsSrch')
        self.assertIn('P7-148', find('frmPurchInv.xaml.cs')['nonaccept_or_followup_boundary'])
        self.assertIn('ItemId<=0', find('frmSalePurch.xaml.cs')['nonaccept_or_followup_boundary'])
        self.assertIn('ISDone=false', find('frmPOS.xaml.cs')['nonaccept_or_followup_boundary'])
        self.assertIn('SelectedId', find('frmStocksSync.xaml.cs')['nonaccept_or_followup_boundary'])

    def test_purchinv_key_difference_stays_unadjudicated(self):
        inputs = json.loads((E / 'closure-inputs-07B38.json').read_bytes())
        self.assertFalse(inputs['all_open_observations_adjudicated'])
        self.assertEqual(len(inputs['unresolved_observations']), 2)
        raw = decode_source((ROOT / 'SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs').read_bytes())[0]
        self.assertIn('double.Parse(frm.InvGlobalID)', raw)
        self.assertIn('where proc_id={frm.InvGlobalID}', raw)
        self.assertEqual(len(read_rows(A / 'findings.csv')), 335)

    def test_legacy_top139_and_new_recursive_tools_are_explicit(self):
        self.assertEqual(self.report['counts']['legacy_top_level_python_tools_unchanged'], 139)
        self.assertEqual(len(self.report['new_checker_source_sha256']), 3)
        self.assertEqual(self.report['counts']['all_recursive_audit_python_tools'], 142)
        self.assertFalse(self.report['legacy_dispatcher_modified'])

    def test_require_complete_cli_returns2_not_false_success(self):
        p = subprocess.run([sys.executable, '-B', str(Path(checker.__file__)), '--require-complete'],
                           cwd=ROOT, capture_output=True, check=False)
        self.assertEqual(p.returncode, 2)
        result = json.loads(p.stdout)
        self.assertEqual(result['integrity_errors'], [])
        self.assertFalse(result['closure']['whole_7B_complete'])
        self.assertEqual(p.stderr, b'')

    def test_existing_snapshot_cannot_be_overwritten_by_builder(self):
        path = E / 'capability-census-07B38.json'
        before = sha(path.read_bytes())
        p = subprocess.run([sys.executable, '-B', str(Path(checker.__file__).with_name('build_7b_census.py')),
                            '--output', str(path)], cwd=ROOT, capture_output=True, check=False)
        self.assertEqual(p.returncode, 2)
        self.assertIn(b'Refusing to overwrite', p.stderr)
        self.assertEqual(sha(path.read_bytes()), before)

    def test_source_reference_supports_singleton(self):
        self.assertEqual(checker.check_references('SmartAuditERP/Class/listItemBarcode.cs:6'), [])
        self.assertTrue(checker.check_references('SmartAuditERP/Class/listItemBarcode.cs:11'))

    def test_no_ERP_or_repair_or_phase_permission_from_documentary_success(self):
        for key in ('application_remediation_performed', 'phase_7C_started', 'phase_8_authorized'):
            self.assertIs(self.report[key], False)
        self.assertEqual(self.report['ERP_or_SQL_runtime_tests_executed'], 0)


if __name__ == '__main__':
    unittest.main()
