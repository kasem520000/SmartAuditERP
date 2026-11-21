#!/usr/bin/env python3
"""Documentary/mutation tests only; no ERP/SQL/WPF/provider/SDK execution."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

import verify_recovery_exit as v


class ExitBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.authority = v.load_json('scope-approval-recovered-07B39R1.json')
        self.caps = v.rows('capability-recovery-state-07B39R1.csv')
        self.policies = v.rows('policy-boundaries-07B39R1.csv')

    def result(self):
        return v.evaluate_exit(self.authority, self.caps, self.policies)

    def synthetic_complete_fixture(self):
        # Unit-test data ONLY, never written over real evidence or called a review.
        for cap in self.caps:
            cap['local_semantic_obligations_complete'] = 'true'
            cap['independent_exit_review'] = 'verified-with-source-evidence'
            cap['local_completion_evidence'] = 'synthetic-unit-test-source-evidence'

    def test_actual_state_is_open_not_another_green_completion_claim(self):
        r = self.result()
        self.assertFalse(r['whole_7B_static_assessment_complete'])
        self.assertEqual(len(r['blockers']), 52)

    def test_authorized_static_handoff_exit_is_possible_in_unit_fixture(self):
        self.synthetic_complete_fixture()
        self.assertTrue(self.result()['whole_7B_static_assessment_complete'])
        self.assertFalse(self.result()['external_contracts_certified'])

    def test_scope_approval_is_not_local_completion(self):
        self.authority['blanket_completion_approval'] = True
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_missing_scope_blocks_even_synthetic_complete_local_work(self):
        self.synthetic_complete_fixture()
        self.authority['whole7b_scope'] = None
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_handoff_ids_or_counts_do_not_complete_local_work(self):
        for cap in self.caps:
            cap['external_boundary_count'] = 401
            cap['handoff_id'] = 'owner-assigned-not-review-proof'
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_one_local_flag_blocks_the_whole_exit(self):
        self.synthetic_complete_fixture()
        self.caps[18]['local_semantic_obligations_complete'] = 'false'
        self.assertIn('CAP7B38-D19:readable-local-evidence-open', self.result()['blockers'])

    def test_completed_status_without_source_evidence_does_not_pass(self):
        self.synthetic_complete_fixture()
        self.caps[20]['local_completion_evidence'] = ''
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_completed_status_without_independent_adjudication_does_not_pass(self):
        self.synthetic_complete_fixture()
        self.caps[20]['independent_exit_review'] = 'counted-by-index'
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_readable_work_cannot_become_external_by_label(self):
        self.synthetic_complete_fixture()
        self.caps[0]['readable_local_work_transferred_to_external'] = 'true'
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_missing_capability_is_not_silently_excluded(self):
        self.synthetic_complete_fixture()
        self.caps.pop()
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_duplicate_capability_cannot_replace_missing_one(self):
        self.synthetic_complete_fixture()
        self.caps[-1] = deepcopy(self.caps[0])
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_each_policy_must_belong_to_its_specific_capability(self):
        self.synthetic_complete_fixture()
        for cid, family in sorted(v.REQUIRED_POLICY_PAIRS):
            with self.subTest(capability=cid, policy=family):
                subset = [p for p in self.policies if (p['capability_id'], p['policy_family']) != (cid, family)]
                # Adding the same family elsewhere is specifically insufficient.
                elsewhere = deepcopy(self.policies[0]); elsewhere['capability_id'] = 'CAP7B38-D26'; elsewhere['policy_family'] = family
                r = v.evaluate_exit(self.authority, self.caps, subset + [elsewhere])
                self.assertIn(cid + ':' + family + ':specific-policy-owner-boundary-missing', r['blockers'])

    def test_external_owner_input_impact_action_exit_are_all_required(self):
        self.synthetic_complete_fixture()
        for field in ['source_evidence', 'owner_role', 'required_redacted_input', 'absence_impact', 'next_action', 'static_exit_criterion']:
            with self.subTest(field=field):
                policy = deepcopy(self.policies); policy[0][field] = ''
                self.assertFalse(v.evaluate_exit(self.authority, self.caps, policy)['whole_7B_static_assessment_complete'])

    def test_scope_authority_never_certifies_a_contract(self):
        self.synthetic_complete_fixture()
        self.policies[0]['certified'] = 'true'
        self.assertFalse(self.result()['whole_7B_static_assessment_complete'])

    def test_phase_and_remediation_barriers_are_explicit(self):
        r = self.result()
        for key in ['phase7_complete','phase7C_started','phase8_authorized','application_remediation_performed','external_contracts_certified']:
            self.assertIs(r[key], False)
        self.assertEqual(r['application_execution_count'], 0)
        self.assertEqual(r['repair_start_and_synchronization'], 'unknown')


class StructuralControlFlowTests(unittest.TestCase):
    def fixture(self, body):
        return 'class Editor { void F() { ' + body + ' } }'

    def test_unbraced_condition_gates_only_navigate(self):
        r = v.import_tail(self.fixture('if (dlg.isDone && dlg.InvGID != "-1") Navigate("q"); target.ISNew = true;'), 'F')
        self.assertEqual(r['consequence_type'], 'expression_statement')
        self.assertEqual(r['assignments_in_following_sibling_statements'], ['target.ISNew'])

    def test_braced_conversion_is_inside_acceptance_not_after_it(self):
        r = v.import_tail(self.fixture('if (dlg.isDone && dlg.InvGID != "-1") { Navigate("q"); target.ISNew = true; }'), 'F')
        self.assertEqual(r['consequence_type'], 'block')
        self.assertEqual(r['assignments_in_consequence'], ['target.ISNew'])
        self.assertEqual(r['assignments_in_following_sibling_statements'], [])

    def test_comment_braces_do_not_change_ast_consequence(self):
        r = v.import_tail(self.fixture('if (dlg.isDone) /* { } */ Navigate("q"); /* } { */ target.ISNew = true;'), 'F')
        self.assertEqual(r['consequence_type'], 'expression_statement')

    def test_try_catch_does_not_move_the_guarded_statement(self):
        r = v.import_tail(self.fixture('try { if (dlg.isDone) Navigate("q"); target.ISNew = true; } catch { ShowError(); }'), 'F')
        self.assertIn('target.ISNew', r['assignments_in_following_sibling_statements'])

    def test_navigate_without_if_is_not_invented_as_guarded(self):
        with self.assertRaisesRegex(ValueError, 'not nested'):
            v.import_tail(self.fixture('Navigate("q"); target.ISNew = true;'), 'F')

    def test_ambiguous_same_name_methods_fail_instead_of_selecting_one(self):
        with self.assertRaisesRegex(ValueError, 'expected one declaration'):
            v.import_tail('class E { void F() {} void F(int n) {} }', 'F')

    def test_invalid_csharp_is_not_repaired(self):
        with self.assertRaisesRegex(ValueError, 'parse error'):
            v.Syntax('class E { void F( }')

    def test_comments_are_not_executable_output_requests(self):
        source = v.Syntax('class E { void F() { /* report.Print(); */ SetStatus(); } }')
        self.assertEqual([c['function'] for c in source.calls(source.method('F'))], ['SetStatus'])

    def test_own_xaml_binding_is_found(self):
        r = v.own_wiring('class E { void F() {} }', '<Window><Button Click="F"/></Window>', 'F')
        self.assertEqual(r['own_xaml_literal_references'][0]['attribute'], 'Click')

    def test_programmatic_binding_is_not_confused_with_declaration(self):
        r = v.own_wiring('class E { void F() {} void G() { b.Click += F; } }', '<Window/>', 'F')
        self.assertEqual(len(r['own_code_simple_method_group_assignments']), 1)
        self.assertEqual(r['own_code_direct_invocations'], [])

    def test_declaration_alone_is_not_reachable_ui_proof(self):
        r = v.own_wiring('class E { void F() { } }', '<Window/>', 'F')
        self.assertFalse(r['own_xaml_literal_references'])
        self.assertFalse(r['own_code_direct_invocations'])
        self.assertFalse(r['own_code_simple_method_group_assignments'])
        self.assertIn('Not typed reachability', r['limit'])


class PresentSourceCauseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load_json('source-facts-07B39R1.json')

    def method(self, stem, name):
        return next(r for r in self.facts['methods'][stem] if r['method'] == name)

    def text(self, stem, name):
        source = v.Syntax(v.decode((v.ROOT / f'SmartAuditERP/Form_WPF/{stem}.xaml.cs').read_bytes()))
        return source.text(source.method(name))

    def test_current_transfer_has_tail_but_no_found_own_binding(self):
        r = self.facts['import_tails']['frmInventoryTransfer']
        self.assertIn('_invoic.ISNew', r['assignments_in_following_sibling_statements'])
        self.assertFalse(self.facts['wiring']['frmInventoryTransfer']['StripImportInv_Click']['own_xaml_literal_references'])

    def test_current_inputoutput_is_a_guarded_negative_control(self):
        r = self.facts['import_tails']['frmInvInputOutput']
        self.assertIn('Invoic.ISNew', r['assignments_in_consequence'])
        self.assertFalse(r['assignments_in_following_sibling_statements'])

    def test_current_pos_tail_has_literal_own_xaml_wiring(self):
        self.assertIn('Invoic.ISNew', self.facts['import_tails']['frmInvPOS']['assignments_in_following_sibling_statements'])
        self.assertTrue(self.facts['wiring']['frmInvPOS']['StripImportInv_Click']['own_xaml_literal_references'])

    def test_key_producer_is_separate_text_key_not_proc_identity(self):
        assignments = self.method('InvoiceOper','GetInvoiceGlobalID')['assignments']
        globals_ = [r['right'] for r in assignments if r['left'] == 'InvGlobalID']
        self.assertEqual(len(globals_), 2)
        self.assertTrue(all('"-"' in rhs for rhs in globals_))
        handler = self.text('frmPurchInv','btnInvSrch_Click')
        self.assertIn('double.Parse(frm.InvGlobalID)', handler)
        self.assertIn('where proc_id={frm.InvGlobalID}', handler)

    def test_return_guard_failure_is_not_a_typed_no_return_found(self):
        text = self.text('frmInvoiceSrch','IsPreviousReturned')
        self.assertIn('Reff_No     = {invGlobalID}', text)
        self.assertIn('catch { return false; }', text)
        self.assertIn('inv_type    = 3', text)
        handler = self.text('frmInvoiceSrch','BtnReturn_Click')
        self.assertLess(handler.index('IsPreviousReturned'), handler.index('ISDone      = true'))

    def test_success_only_routes_have_the_reviewed_call_sets_not_a_writer(self):
        expected = {
          ('frmInvPurch','stripExport_Click'): {'MessageBox.Show','dlg.ShowDialog','this.IsInvExist'},
          ('frmCloseShift','ExportToExcel'): {'ShowError','ShowSuccess','saveDialog.ShowDialog'},
          ('frmEmpInvs','BtnExport_Click'): {'DXMessageBox.Show','Process.Start','ShowError','ShowWarning','saveDialog.ShowDialog'},
          ('frmAccountsDirectory','ExportToExcel'): {'MessageBox.Show'},
        }
        for (stem, name), calls in expected.items():
            with self.subTest(stem=stem, method=name):
                self.assertEqual({c['function'] for c in self.method(stem,name)['calls']}, calls)

    def test_local_sync_lists_are_not_populated_before_external_converter(self):
        for stem, variable in [('frmEntriesSyncStatus','inventoryList'),('frmReceiptsSyncStatus','list')]:
            with self.subTest(stem=stem):
                text = self.text(stem,'BindToData')
                self.assertIn('new List<InventoryData>()', text)
                self.assertIn('ToDataTable(' + variable + ')', text)
                self.assertNotIn(variable + '.Add(', text)
                self.assertNotIn(variable + '.AddRange(', text)

    def test_contract_print_and_view_are_not_the_save_print_placeholder(self):
        for name in ['btnPrint_Click', 'btnView_Click']:
            self.assertIn('RptPrint', {c['function'] for c in self.method('frmcontract',name)['calls']})
        self.assertNotIn('RptPrint', {c['function'] for c in self.method('frmcontract','SaveAndPrint')['calls']})
        self.assertEqual(self.method('frmPrintBill','print')['calls'], [])

    def test_source_fact_derivation_matches_exclusive_captured_facts(self):
        self.assertEqual(v.derive_source_facts(), self.facts)


class PreservationAndProvenanceTests(unittest.TestCase):
    def test_original_registry_is_still_all335_raw336crlf(self):
        raw = (v.AUDIT / 'findings.csv').read_bytes()
        self.assertEqual(v.sha(raw), 'ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a')
        self.assertEqual(raw.count(b'\r\n'), 336)
        self.assertEqual(len(v.rows('../findings.csv')), 335)

    def test_ancestry_retains_full_dictionaries_not_only_counts(self):
        ancestry = v.load_json('ancestry-recovery-map-07B39R1.json')
        self.assertEqual([len(b['records']) for b in ancestry['bundles']], [14,3,10,10])
        for bundle in ancestry['bundles']:
            for row in bundle['records']:
                self.assertEqual(v.canonical_sha(row['canonical_upstream_row']), row['upstream_row_sha256'])
        self.assertTrue(all(not f['static_assessment_complete'] for f in ancestry['family_exits']))

    def test_historical_B38_nulls_are_not_retroactively_approved(self):
        old = v.load_json('closure-inputs-07B38.json')
        self.assertIsNone(old['scope_approval'])
        self.assertIsNone(old['external_handoff_acceptance'])
        self.assertIsNone(old['whole_family_approval'])
        self.assertFalse(old['whole_7B_complete'])

    def test_new_reference_label_does_not_retimestamp_or_certify_raw_clocks(self):
        date = v.load_json('date-prospective-07B39R1.json')
        self.assertFalse(date['historical_artifacts_retimestamped'])
        self.assertFalse(date['clock_is_calendar_certification'])
        self.assertFalse(date['earlier_author_date_note_is_user_authority'])
        self.assertIn('user_designated_assessment_reference_date_utc', date)
        # Deliberately no assertion that a pinned calendar literal proves UTC authority.

    def test_missing_prior_B39_logs_are_not_retroactively_repaired(self):
        log = v.load_json('source-review-log-07B39R1.json')
        self.assertFalse(log['prior_B39_log05_available'])
        self.assertFalse(log['prior_B39_log05_claims_authenticated'])
        self.assertFalse(log['retroactive_backfill_of_prior_reads'])
        self.assertTrue(all(not r['whole_file_review_claimed'] for r in log['reviewed_ranges']))

    def test_new_roots_and_extensions_have_distinct_counting(self):
        new = v.rows('findings-additions-07B39R1.csv')
        extensions = v.load_json('finding-extensions-07B39R1.json')
        self.assertEqual(len(new), 4)
        self.assertEqual([r['finding_id'] for r in extensions['extensions']], ['P7-050','P1-033','P7-160'])
        self.assertEqual([len(r['routes']) for r in extensions['extensions']], [7,6,1])
        self.assertEqual(extensions['new_roots'], 0)

    def test_full_current_integrity_does_not_say_complete(self):
        report = v.validate()
        self.assertTrue(report['integrity_ok'], report['errors'])
        self.assertFalse(report['static_exit']['whole_7B_static_assessment_complete'])
        self.assertEqual(report['counts']['effective_findings_with_supplement'], 339)


if __name__ == '__main__':
    unittest.main()
