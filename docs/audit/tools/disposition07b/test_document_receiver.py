#!/usr/bin/env python3
"""Read-only R4 syntax/identity/adjudication regressions; no ERP/SQL/WPF fixtures.

Source mutation cases reparse C# text in memory. They do not implement or execute
C# behavior in Python. Evidence mutations operate only in temporary directories.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import verify_document_receiver as v


class DocumentReceiverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)
        cls.reads = v.load(v.READS)

    def changed_source(self, rel, old, new):
        text = v.base.decode((v.ROOT / rel).read_bytes())
        self.assertEqual(text.count(old), 1, 'Mutation must select exactly one real source occurrence')
        result = copy.deepcopy(self.facts)
        result['methods'][rel] = v.source_methods(text.replace(old, new, 1), v.CONTEXTS[rel])
        return result

    def bad_evidence(self, name, mutate):
        names = (v.FACTS, v.READS, v.REVIEW, v.ITEM, v.SCREEN, v.ROUTES, v.BOUNDARIES,
                 'findings-additions-07B39R1.csv', 'capability-register-07B38.csv')
        with tempfile.TemporaryDirectory(prefix='smartaudit-r4-negative-') as folder:
            ev = Path(folder)
            for source in names:
                shutil.copyfile(v.EV / source, ev / source)
            obj = json.loads((ev / name).read_bytes())
            mutate(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev)

    def test_actual_facts_rederive_from_original_source(self):
        self.assertEqual(v.derive(), self.facts)

    def test_current_source_claims_and_read_union(self):
        self.assertEqual(v.item_errors(self.facts), [])
        self.assertEqual(v.receiver_errors(self.facts), [])
        self.assertEqual(v.route_errors(self.facts), [])
        self.assertEqual(v.read_errors(self.reads, self.facts), [])

    def test_recorded_adjudications_are_consistent_not_exits(self):
        self.assertEqual(v.evidence_errors(), [])
        self.assertFalse(v.verify()['whole_7B_static_assessment_complete'])

    def test_item_loaded_must_copy_the_fresh_request(self):
        f = self.changed_source(v.AGG, 'selectedItemId = ItemId;', 'selectedItemId = 0;')
        self.assertTrue(v.item_errors(f))

    def test_clearing_all_flag_would_change_the_current_claim(self):
        f = self.changed_source(v.AGG, 'selectedItemId = ItemId;',
                                'selectedItemId = ItemId; chkAll.IsChecked = false;')
        self.assertTrue(v.item_errors(f))

    def test_existing_item_predicate_is_actually_flag_gated(self):
        f = self.changed_source(v.AGG, 'if (!chkAll.IsChecked == true)', 'if (selectedItemId > 0)')
        self.assertTrue(v.item_errors(f))

    def test_all_items_xaml_default_is_not_an_unrelated_checkbox(self):
        f = copy.deepcopy(self.facts)
        target = next(x for x in f['xml_elements'][v.AGG[:-3]] if x['attributes'].get('Name') == 'chkAll')
        target['attributes']['IsChecked'] = 'False'
        self.assertTrue(v.item_errors(f))

    def test_own_loaded_wiring_is_required(self):
        f = copy.deepcopy(self.facts)
        target = next(x for x in f['xml_elements'][v.AGG[:-3]] if 'Loaded' in x['attributes'])
        target['attributes']['Loaded'] = 'AnotherHandler'
        self.assertTrue(v.item_errors(f))

    def test_three_exact_positive_request_sources_not_only_count(self):
        for stem in v.CALLERS:
            with self.subTest(stem=stem):
                f = copy.deepcopy(self.facts)
                m = v.method(f, v.P + stem + '.xaml.cs', 'StripItemProcess_Click')
                target = next(x for x in m['assignments'] if x['left'] == 'ItemId' or x['left'].endswith('.ItemId'))
                target['right'] = '-1'
                self.assertTrue(v.item_errors(f))

    def test_equal_count_wrong_report_creation_is_rejected_without_crash(self):
        f = self.changed_source(v.P + 'frmPurchInv.xaml.cs',
                                'new frmRptItemsActivity { ItemId = id }',
                                'new AnotherReport { ItemId = id }')
        self.assertTrue(v.item_errors(f))

    def test_request_must_precede_display(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.P + 'frmInvInOutput.xaml.cs', 'StripItemProcess_Click')
        next(x for x in m['assignments'] if x['left'].endswith('.ItemId'))['line'] = 99999
        self.assertTrue(v.item_errors(f))

    def test_item_scope_does_not_reuse_prior_store_predicate(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.DET, 'ShowResult')
        target = next(a for a in m['assignments'] if 'Inv_Sub.ItemId={SelectedId}' in a['right'])
        target['ancestors'] = []
        self.assertTrue(v.item_errors(f))

    def test_prior_root_really_retains_the_all_store_default(self):
        f = self.changed_source(v.DET, 'cmbSafes.SelectedValue = storeId;',
                                'cmbSafes.SelectedValue = storeId; chkAll.IsChecked = false;')
        self.assertTrue(v.item_errors(f))

    def test_current_receiver_is_void_with_ref_not_a_typed_outcome(self):
        f = self.changed_source(v.IP,
                                'public static void BindingInvoice(ref InvoiceDGV Invo, string sqlstr)',
                                'public static bool BindingInvoice(ref InvoiceDGV Invo, string sqlstr)')
        self.assertTrue(v.receiver_errors(f))

    def test_query_forwarding_does_not_invent_an_added_branch_guard(self):
        f = self.changed_source(v.IP, 'new SqlCommand(sqlstr, sqlConnection)',
                                'new SqlCommand(sqlstr + " AND branch=@branch", sqlConnection)')
        self.assertTrue(v.receiver_errors(f))

    def test_null_no_header_and_outer_failed_are_distinct_source_arms(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        target = next(a for a in m['assignments'] if a['left'] == 'Invo' and any(x['kind'] == 'catch' for x in a['ancestors']))
        target['right'] = 'new InvoiceDGV()'
        self.assertTrue(v.receiver_errors(f))

    def test_first_header_read_has_hasrows_scope(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        next(c for c in m['calls'] if c['function'] == 'sqlDataReader.Read')['ancestors'] = []
        self.assertTrue(v.receiver_errors(f))

    def test_loaded_identity_is_the_row_not_the_request_name(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        next(a for a in m['assignments'] if a['left'] == 'Invo.InvGlobalID')['right'] = 'sqlstr'
        self.assertTrue(v.receiver_errors(f))

    def test_header_flags_are_not_relabelled_health_success(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        next(a for a in m['assignments'] if a['left'] == 'Invo.IsLoaded')['right'] = 'true'
        self.assertTrue(v.receiver_errors(f))

    def test_row_catch_is_not_silently_relabelled_as_throwing(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        next(c for c in m['catches'] if 'projectError4' in c['declaration'])['body'] = '{ throw; }'
        self.assertTrue(v.receiver_errors(f))

    def test_totals_order_is_before_row_publication(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        next(a for a in m['assignments'] if a['left'] == 'Invo.SumCost')['line'] = 99999
        self.assertTrue(v.receiver_errors(f))

    def test_detail_query_binds_loaded_global_id_and_product_filter(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        target = next(c for c in m['creations'] if c['type'] == 'SqlDataAdapter' and 'ProductId = 0' in c['arguments'])
        target['arguments'] = target['arguments'].replace('Invo.InvGlobalID', 'Invo.InvoiceNo')
        self.assertTrue(v.receiver_errors(f))

    def test_cost_center_uses_current_branch_not_implicitly_loaded_branch(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.IP, 'BindingInvoice')
        target = next(c for c in m['creations'] if 'select CCcode from Entry_sub' in c['arguments'])
        target['arguments'] = target['arguments'].replace('MainClass.BranchNo', 'Invo.Branch')
        self.assertTrue(v.receiver_errors(f))

    def test_detail_helper_has_no_own_swallowing_catch(self):
        f = copy.deepcopy(self.facts)
        v.method(f, v.IP, 'BindingItemDetails')['catches'] = [{'body': '{}'}]
        self.assertTrue(v.receiver_errors(f))

    def test_glass_and_cost_helper_catches_are_not_item_detail_catch(self):
        for name in ('glassOtions', 'BindingCostDetaile'):
            with self.subTest(name=name):
                f = copy.deepcopy(self.facts)
                v.method(f, v.IP, name)['catches'] = []
                self.assertTrue(v.receiver_errors(f))

    def test_each_of_five_wrappers_forwards_the_request(self):
        for stem in v.WRAPPERS:
            with self.subTest(stem=stem):
                f = copy.deepcopy(self.facts)
                m = v.method(f, v.P + stem + '.xaml.cs', 'Navigate')
                next(c for c in m['calls'] if c['function'] == 'InvoiceOper.BindingInvoice')['function'] = 'AnotherReader'
                self.assertTrue(v.receiver_errors(f))

    def test_wrappers_do_not_invent_an_internal_dirty_guard(self):
        f = copy.deepcopy(self.facts)
        v.method(f, v.P + 'frmInvSale.xaml.cs', 'Navigate')['calls'].append({'function': 'CheckBeforeClear'})
        self.assertTrue(v.receiver_errors(f))

    def test_route_identity_not_inferred_from_twenty_six_count(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.DET, 'OpenInvoiceByType')
        target = next(c for c in m['calls'] if c['function'] == 'f.Navigate')
        target['arguments'] = target['arguments'].replace('id={invNo}', "InvGlobalID=N'{invNo}'")
        self.assertEqual(len(v.request_rows(f)), len(v.request_rows(self.facts)))
        self.assertTrue(v.route_errors(f))

    def test_configure_before_show_is_not_show_before_navigate(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.DET, 'OpenForm')
        next(c for c in m['calls'] if c['function'] == 'configure')['line'] = 99999
        self.assertTrue(v.route_errors(f))

    def test_read_registration_does_not_claim_unread_tail(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'] = [r for r in reads['reads'] if not (r['path'] == v.IP and r['start'] == 3390)]
        self.assertTrue(v.read_errors(reads, self.facts))

    def test_read_range_hash_and_extraction_limit_are_enforced(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'][0]['decoded_range_utf8_sha256'] = '0' * 64
        reads['extraction_equals_reading'] = True
        self.assertGreaterEqual(len(v.read_errors(reads, self.facts)), 2)

    def test_new_root_number_cannot_replace_existing_extension(self):
        errors = self.bad_evidence(v.ITEM, lambda x: x.update(root_id='P7-174', decision='new-root', new_finding_ids=['P7-174']))
        self.assertTrue(errors)

    def test_equal_count_wrong_focused_root_dictionary_is_rejected(self):
        def mutate(x):
            x['focused_root_reviews']['P7-122']['canonical_prior_row']['title'] = 'Other issue'
        self.assertTrue(self.bad_evidence(v.ITEM, mutate))

    def test_extension_cannot_claim_all_missing345_dictionaries_screened(self):
        self.assertTrue(self.bad_evidence(v.ITEM, lambda x: x.update(all345_prior_findings_deduplicated=True)))

    def test_extension_is_not_historical_root_remediation(self):
        self.assertTrue(self.bad_evidence(v.ITEM, lambda x: x.update(historical_root_fields_rewritten=True)))

    def test_exact_available339_rows_are_preserved(self):
        self.assertTrue(self.bad_evidence(v.SCREEN, lambda x: x['available_prior_rows'].reverse()))

    def test_same_count_wrong_route_target_is_rejected(self):
        def mutate(x):
            x['individual_dispositions'][0]['syntactically_named_target'] = 'frmSandVAT'
        self.assertTrue(self.bad_evidence(v.ROUTES, mutate))

    def test_alias_or_compiler_binding_not_claimed_from_name_tail(self):
        def mutate(x):
            x['individual_dispositions'][0]['target_is_type_bound_by_compiler'] = True
        self.assertTrue(self.bad_evidence(v.ROUTES, mutate))

    def test_exact_canonical_capability_not_a_similarly_named_row(self):
        def mutate(x):
            x['capabilities'][v.TARGETS[0]]['canonical_capability_row']['id'] = v.TARGETS[1]
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_status_flags_cannot_turn_local_work_into_exit(self):
        def mutate(x):
            x['capabilities'][v.TARGETS[2]]['local_semantic_obligations_complete'] = True
            x['capabilities'][v.TARGETS[2]]['whole_capability_certified'] = True
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_readable_alternative_receiver_not_externalized(self):
        def mutate(x):
            x['capabilities'][v.TARGETS[0]]['readable_local_work_externalized'] = True
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_named_local_remainder_cannot_be_replaced_by_empty_field(self):
        def mutate(x):
            x['capabilities'][v.TARGETS[2]]['remaining_readable_local'] = []
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_whole_receiver_body_review_cannot_be_substituted_by_metadata(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.update(R3_shared_receiver_metadata_only_blocker_replaced_by='metadata-only')))

    def test_eight_outcomes_cannot_be_duplicated_to_hide_omission(self):
        def mutate(x):
            x['receiver_outcomes'][0] = copy.deepcopy(x['receiver_outcomes'][1])
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_source_outcome_is_not_an_observed_provider_failure(self):
        def mutate(x):
            x['receiver_outcomes'][1]['observed_in_ERP'] = True
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_unavailable_R2_R3_tests_cannot_be_recertified(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.update(R2_R3_files_recovered=True, prior196_tests_recertified=True)))

    def test_assessment_date_is_current_authority_not_raw_clock(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.update(assessment_reference_date_utc='2026-11-21', raw_clocks_are_calendar_authority=True)))

    def test_three_individual_boundaries_remain_unprovided_uncertified(self):
        rows = v.base.rows(v.BOUNDARIES)
        self.assertEqual({x['id'] for x in rows}, {'EXT-R4-MODEL', 'EXT-R4-DEPLOYED-IDENTITY', 'EXT-R4-LOAD-POLICY'})
        self.assertTrue(all(x['provided'] == x['certified'] == 'false' for x in rows))
        self.assertTrue(all(x['remaining_readable_local'] for x in rows))

    def test_cli_readonly_verification_has_no_input_writes(self):
        names = (v.FACTS, v.READS, v.ITEM, v.SCREEN, v.REVIEW, v.ROUTES, v.BOUNDARIES)
        before = [v.identity('docs/audit/evidence/' + n) for n in names]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        p = subprocess.run([sys.executable, '-B', '-W', 'error::ResourceWarning', str(Path(v.__file__)), '--verify', '--rederive'], cwd=v.ROOT, env=env, capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertEqual(json.loads(p.stdout)['errors'], [])
        self.assertEqual(before, [v.identity('docs/audit/evidence/' + n) for n in names])

    def test_cli_completion_gate_is_open_despite_integrity_pass(self):
        p = subprocess.run([sys.executable, '-B', str(Path(v.__file__)), '--verify', '--require-complete'], cwd=v.ROOT,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertEqual(json.loads(p.stdout)['errors'], [])
        self.assertFalse(json.loads(p.stdout)['whole_7B_static_assessment_complete'])


if __name__ == '__main__':
    unittest.main()
