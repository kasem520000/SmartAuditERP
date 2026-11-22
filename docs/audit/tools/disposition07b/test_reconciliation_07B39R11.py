#!/usr/bin/env python3
"""Fresh R11 Python audit tests, not the lost local R10 tests or ERP tests.

Only parse the actual supplied source and mutate it IN MEMORY, or mutate
isolated audit-JSON copies. No C#/SQL/provider/WPF/model execution. Source
mutations invalidate observations; they are not suggested application fixes.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import verify_reconciliation_07B39R11 as v


class ReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)

    def changed_method(self, rel, selector, old, new, count=1):
        original = v.base.decode((v.ROOT / rel).read_bytes())
        member = v.method(self.facts, rel, selector)['syntax_text']
        if '\r\n' in member:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        self.assertEqual(member.count(old), count, 'Mutate an actual supplied spelling')
        self.assertEqual(original.count(member), 1)
        changed = original.replace(member, member.replace(old, new), 1)
        facts = copy.deepcopy(self.facts)
        facts['methods'][rel][selector] = v.source_methods(changed, [selector])[selector]
        if rel == v.RO:
            variable = 'sqlCommand3' if selector == 'SaveReceipt' else 'sqlCommand'
            facts['bridges'][selector] = v.bridge(facts, rel, selector, variable, 'InsertReceipt')
        if rel == v.FS and selector == 'insert_SettingNotify':
            facts['notify_insert'] = v.parse_insert(v.commands(v.method(facts, rel, selector), 'INSERT')[0]['literal_sql'])
        return facts

    def rejected(self, facts, label):
        errors = v.source_errors(facts)
        self.assertIn('source:' + label, errors)

    def mutation(self, rel, selector, old, new, label):
        self.rejected(self.changed_method(rel, selector, old, new), label)

    def range_mutation(self, key, old, new):
        facts = copy.deepcopy(self.facts)
        row = facts['text_ranges'][key]
        self.assertEqual(row['text'].count(old), 1)
        row['text'] = row['text'].replace(old, new, 1)
        row['decoded_range_utf8_sha256'] = v.sha(row['text'].encode('utf8'))
        return facts

    def bad_evidence(self, name, change):
        with tempfile.TemporaryDirectory(prefix='smartaudit-r11-audit-json-') as tmp:
            ev = Path(tmp)
            for n in (v.READS, v.REVIEW, v.LEDGER, v.DATE_NOTE):
                shutil.copyfile(v.EV / n, ev / n)
            obj = json.loads((ev / name).read_bytes())
            change(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev, self.facts)

    def test_actual_source_rederivation_is_fresh_not_lost_R10(self):
        self.assertEqual(v.derive(), self.facts)

    def test_source_guards_match_actual_supplied_source(self):
        self.assertEqual(v.source_errors(self.facts), [])

    def test_27_selected_contexts_13_files_not_26_capability_exits(self):
        self.assertEqual(sum(map(len, v.CONTEXTS.values())), 27)
        self.assertEqual(len(self.facts['source_identity']), 13)
        self.assertEqual(len(v.load(v.LEDGER)['capabilities']), 26)
        self.assertFalse(v.load(v.LEDGER)['all26_freshly_semantically_reread'])

    def test_827_is_inventory_paths_not_827_human_read_CSharp_sources(self):
        d = self.facts['discovery']
        self.assertEqual(d['inventory_paths_scanned'], 827)
        self.assertEqual(d['csharp_paths_count'], 491)
        self.assertTrue(d['inventory_includes_tracked_binary_and_generated_paths_not_827_CSharp_sources'])
        self.assertFalse(d['whole_inventory_human_semantic_read_claimed'])

    def test_missing_recipient_is_a_casefold_text_difference_only(self):
        b = self.facts['bridges']['SaveReceipt2']
        self.assertEqual(b['literal_add_count'], 28)
        self.assertEqual(b['casefold_only_missing'], ['@Recipient'])
        self.assertEqual(b['case_only_spelling_differences'], ['@BankId', '@State'])
        self.assertTrue(b['casefold_is_a_text_comparison_not_provider_binding'])

    def test_other_two_writers_are_explicit_recipient_counterexamples(self):
        for sel in ('SaveReceipt', 'ReadReceiptOnline'):
            b = self.facts['bridges'][sel]
            self.assertEqual(b['literal_add_count'], 29)
            self.assertEqual(b['casefold_only_missing'], [])

    def test_save2_selects_insert_only_not_update(self):
        refs = v.method(self.facts, v.RO, 'SaveReceipt2')['query_references']
        self.assertEqual([r['text'] for r in refs], ['StoredQueries.InsertReceipt'])

    def test_notify22_columns22_insert_adds24_method_adds(self):
        info = self.facts['notify_insert']
        self.assertEqual((info['column_count'], info['parameter_count']), (22, 22))
        self.assertEqual(info['bracketed_column_count_not_total'], 16)
        adds = v.method(self.facts, v.FS, 'insert_SettingNotify')['parameter_adds']
        self.assertEqual(len(adds), 24)
        self.assertEqual(sum(r['function'].startswith('insertCommand.') for r in adds), 22)

    def test_four_active_calls_and_one_comment_are_distinguished(self):
        d = self.facts['discovery']
        self.assertEqual(len(d['active_SaveReceipt2_literal_invocations']), 4)
        self.assertEqual(len(d['SaveReceipt2_comment_occurrences']), 1)
        self.assertEqual(d['SaveReceipt2_comment_occurrences'][0]['line'], 404)

    def test_interpolated_restore_queries_are_not_claimed_decoded_SQL(self):
        r = v.method(self.facts, v.P + 'frmSandD.xaml.cs', 'RestorePreviousReceipt')
        command = v.commands(r, 'DELETE')[0]
        self.assertIsNone(command['literal_sql'])
        self.assertIn('{receipt.ReceiptNo}', command['interpolated_template_syntax'])

    def test_literal_decoder_does_not_treat_concatenation_as_one_literal(self):
        self.assertIsNone(v.literal('"select " + value + " tail"'))
        self.assertIsNone(v.literal('@"select " + value + @" tail"'))
        self.assertEqual(v.literal('"select\\r\\n"'), 'select\r\n')
        self.assertEqual(v.literal('@"a""b"'), 'a"b')

    def test_strict_CSharp_parser_is_not_relaxed_for_invalid_source(self):
        text = v.base.decode((v.ROOT / v.RO).read_bytes())
        bad = text.replace('public bool SaveReceipt2(Receipt Receipt)', 'public bool SaveReceipt2(Receipt Receipt', 1)
        with self.assertRaises(ValueError):
            v.source_methods(bad, ['SaveReceipt2'])

    def test_simple_insert_decoder_rejects_unsupported_values_expression(self):
        with self.assertRaises(ValueError):
            v.parse_insert('INSERT INTO X(a) VALUES(1+2)')

    def test_local_DDL_exists_without_claiming_migration_or_singleton(self):
        ranges = self.facts['text_ranges']
        self.assertIn('CREATE TABLE [dbo].[Settingmqtt]', ranges['mqtt-base-create']['text'])
        self.assertIn('CREATE TABLE [dbo].[Settingmqtt]', ranges['mqtt-guarded-create']['text'])
        self.assertIn('ALTER TABLE Receipts  Add Recipient', ranges['receipt-recipient-guarded-alter']['text'])
        self.assertIn('[id] ASC', ranges['mqtt-base-create']['text'])

    def test_external_model_property_use_is_not_model_definition(self):
        self.assertEqual(self.facts['discovery']['class_Receipt_definition_spelling_hits_in_CSharp_paths'], [])
        self.assertIn('AuditorAPI', self.facts['text_ranges']['external-model-reference']['text'])
        self.assertFalse(self.facts['runtime_or_all_ingress_or_model_defaults_certified'])

    def test_remote_R10_verifier_is_not_imported(self):
        self.assertNotIn('verify_recipient_notify_07B39R10', sys.modules)
        self.assertFalse(v.load(v.REVIEW)['remote_R10_verifier_executed'])

    def test_actual_source_application_and_published_history_preserved(self):
        self.assertEqual(v.preservation_errors(), [])

    def test_actual_authored_evidence_consistent(self):
        self.assertEqual(v.evidence_errors(facts=self.facts), [])

    def test_read_log_explicitly_does_not_invent_display_or_reading_telemetry(self):
        read = v.load(v.READS)
        self.assertFalse(read['extraction_equals_reading'])
        self.assertFalse(read['independent_human_review_claimed'])
        self.assertFalse(read['raw_source_display_streams_preserved'])
        self.assertFalse(read['individual_read_timestamps_invented'])
        self.assertFalse(read['lost_R10_97_contexts_reconstructed'])

    def test_original335_plus_R1_four_and17_explicit_comparisons(self):
        ds = v.dictionary_rows()
        self.assertEqual((len(ds), len({r['id'] for r in ds})), (339, 339))
        self.assertEqual(len(v.load(v.REVIEW)['focused_root_comparisons']), 17)
        self.assertEqual(v.identity('docs/audit/findings.csv'), v.ORIGINAL_FINDINGS)

    def test_six_questions_not_numbered_roots_or_observed_failures(self):
        for q in v.load(v.REVIEW)['source_questions']:
            self.assertIsNone(q['new_numbered_finding_id'])
            self.assertFalse(q['novelty_certified'])
            self.assertFalse(q['observed_provider_or_financial_failure'])
            self.assertFalse(q['accepted_external_handoff'])

    def test_scope_gate_returns_two_not_whole_7B_complete(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            result = v.main(['--require-complete'])
        obj = json.loads(out.getvalue())
        self.assertEqual(result, 2)
        self.assertEqual(obj['errors'], [])
        self.assertFalse(obj['whole_7B_static_assessment_complete'])
        self.assertFalse(obj['phase7C_started'])
        self.assertFalse(obj['phase8_authorized'])

    def test_calendar_note_is_prospective_not_relabelled_history(self):
        note = v.load(v.DATE_NOTE)
        self.assertEqual(note['prospective_session_reference_date_utc'], v.DATE)
        self.assertFalse(note['frozen_dates_or_raw_clocks_authenticate_chronology'])
        self.assertFalse(note['old_executed_files_relabelled'])

    def test_lost_R10_578_capture_is_not_recovered_or_recertified(self):
        entry = v.load(v.ENTRY)['prior_local_R10']
        self.assertFalse(entry['actual_objects_or_files_available'])
        self.assertFalse(entry['reported_578_tests_are_current_recovered_capture'])
        self.assertFalse(v.load(v.LEDGER)['lost_local_R10_recovered'])

    def test_save2_query_swap_invalidates_insert_observation(self):
        self.mutation(v.RO, 'SaveReceipt2', 'StoredQueries.InsertReceipt', 'StoredQueries.UpdateReceipt', 'save2-selects-insert-not-update')

    def test_save2_other_missing_name_is_not_hidden_by_28_count(self):
        self.mutation(v.RO, 'SaveReceipt2', '"@ISDeleted"', '"@Recipient"', 'save2-only-recipient-omission-under-casefold')

    def test_original_writer_missing_recipient_invalidates_counterexample(self):
        self.mutation(v.RO, 'SaveReceipt', '"@Recipient"', '"@OtherRecipient"', 'recipient-counterexample:SaveReceipt')

    def test_online_writer_missing_recipient_invalidates_counterexample(self):
        self.mutation(v.RO, 'ReadReceiptOnline', '"@Recipient"', '"@OtherRecipient"', 'recipient-counterexample:ReadReceiptOnline')

    def test_save2_commit_removed_invalidates_written_flow_not_financial_result(self):
        self.mutation(v.RO, 'SaveReceipt2', 'sqlTransaction.Commit();', 'sqlTransaction.Rollback();', 'save2-written-flow-not-always-false-or-never-throws-proof')

    def test_save2_open_call_removed_has_a_guard_not_index_error(self):
        self.mutation(v.RO, 'SaveReceipt2', 'sqlConnection.Open();', 'sqlConnection.OpenAsync();', 'save2-written-flow-not-always-false-or-never-throws-proof')

    def test_save2_result_contract_change_is_rejected(self):
        self.mutation(v.RO, 'SaveReceipt2', 'public bool SaveReceipt2', 'public int SaveReceipt2', 'save2-written-flow-not-always-false-or-never-throws-proof')

    def test_notify_add_explicit_transaction_invalidates_no_local_transaction_observation(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'EnsureConnectionOpen(conn);', 'EnsureConnectionOpen(conn); conn.BeginTransaction();', 'notify-no-selected-explicit-transaction-not-ambient-proof')

    def test_notify_delete_branch_filter_change_invalidates_db_only_observation(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'delete from [dbo].[Settingmqtt] where DB=@DB', 'delete from [dbo].[Settingmqtt] where DB=@DB AND BranchId=@BranchId', 'notify-conditional-db-replacement')

    def test_notify_check_wrong_parameter_name_is_not_accepted_by_total_count(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'checkCommand.Parameters.AddWithValue("@DB"', 'checkCommand.Parameters.AddWithValue("@OtherDB"', 'notify-conditional-db-replacement')

    def test_notify_delete_guard_reverse_is_rejected(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'existingTable.Rows.Count > 0', 'existingTable.Rows.Count == 0', 'notify-conditional-db-replacement')

    def test_notify_unbracketed_column_removal_is_detected(self):
        self.mutation(v.FS, 'insert_SettingNotify', ',syncDefinitions)', ')', 'notify-22-columns-22-insert-adds-24-total-not16-or23')

    def test_notify_insert_add_name_change_is_detected(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'insertCommand.Parameters.AddWithValue("@syncOper"', 'insertCommand.Parameters.AddWithValue("@OtherFlag"', 'notify-22-columns-22-insert-adds-24-total-not16-or23')

    def test_notify_branch_value_not_inferred_from_column_name_only(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'CmbBranchMqtt.SelectedValue ?? 0', '0', 'notify-selected-values-caught-void-result')

    def test_notify_pwd_expression_changed_invalidates_selected_storage_observation(self):
        self.mutation(v.FS, 'insert_SettingNotify', 'pwdtxt.Text ?? string.Empty', 'Protect(pwdtxt.Text)', 'notify-selected-values-caught-void-result')

    def test_notify_outer_success_text_change_invalidates_caller_observation(self):
        self.mutation(v.FS, 'BtnConnect_Click', 'btnconnectit.Content = "تم الاتصال بنجاح";', 'btnconnectit.Content = "unknown";', 'notify-caller-success-after-void-not-persistence-acceptance')

    def test_notify_button_hook_change_is_rejected(self):
        self.mutation(v.FS, 'RegisterEvents', 'btnconnectit.Click += BtnConnect_Click;', 'btnconnectit.Click -= BtnConnect_Click;', 'notify-caller-success-after-void-not-persistence-acceptance')

    def test_settings_row_filter_change_invalidates_unfiltered_observation(self):
        self.mutation(v.FS, 'LoadSettingNotify', 'FROM [Settingmqtt]', 'FROM [Settingmqtt] WHERE BranchId=1', 'settings-first-unfiltered-notify-row')

    def test_connect_row_filter_change_invalidates_first_unfiltered_observation(self):
        self.mutation(v.UL, 'ConnectMQTList', 'select * from Settingmqtt', 'select * from Settingmqtt where BranchId=1', 'mqtt-first-row-no-selected-branch-filter')

    def test_check_active_condition_change_is_rejected(self):
        self.mutation(v.UL, 'CheckMqttStat', 'where is_active=1', 'where is_active=0', 'login-any-active-versus-first-branch-row-not-ACL')

    def test_branch_row_zero_change_is_rejected(self):
        self.mutation(v.UL, 'LoadBranches', 'dtMqtt.Rows[0][0]', 'dtMqtt.Rows[1][0]', 'login-any-active-versus-first-branch-row-not-ACL')

    def test_connection_factory_object_creation_not_assumed_after_change(self):
        self.mutation(v.MC, 'ConnObj', 'conn = new SqlConnection(connstr);', 'conn = GetConnection(connstr);', 'connection-factory-new-object-not-shared-transaction')

    def test_maintenance_copy_table_removed_is_detected(self):
        self.mutation(v.RC, 'CopySettingsTablesAsync', '"Settingmqtt"', '"OtherSettings"', 'available-maintenance-copy-not-singleton-proof')

    def test_restore_SandD_reversed_direct_guard_is_rejected(self):
        self.mutation(v.P + 'frmSandD.xaml.cs', 'RestorePreviousReceipt', 'if (new ReceiptOper().SaveReceipt2(receipt))', 'if (!new ReceiptOper().SaveReceipt2(receipt))', 'restore-conditional-delete-and-key-scope:SandD')

    def test_restore_SandQAndroid_reversed_direct_guard_is_rejected(self):
        self.mutation(v.P + 'frmSandQAndroid.xaml.cs', 'RestorePreviousReceipt', 'if (new ReceiptOper().SaveReceipt2(receipt))', 'if (!new ReceiptOper().SaveReceipt2(receipt))', 'restore-conditional-delete-and-key-scope:SandQ')

    def test_restore_SandSD_reversed_saved_guard_is_rejected(self):
        self.mutation(v.P + 'frmSandSD.xaml.cs', 'RestorePreviousReceipt', 'if (saved)', 'if (!saved)', 'restore-conditional-delete-and-key-scope:SandSD')

    def test_restore_SandQD_reversed_saved_guard_is_rejected(self):
        self.mutation(v.P + 'frmSandQD.xaml.cs', 'RestorePreviousReceipt', 'if (saved)', 'if (!saved)', 'restore-conditional-delete-and-key-scope:SandQD')

    def test_mqtt_PK_syntax_change_invalidates_selected_id_PK_observation(self):
        f = self.range_mutation('mqtt-base-create', '[id] ASC', '[BranchId] ASC')
        self.rejected(f, 'available-schema-not-db-branch-singleton:mqtt-base-create')

    def test_receipt_alter_different_column_not_accepted_by_substring(self):
        f = self.range_mutation('receipt-recipient-guarded-alter', 'Add Recipient ', 'Add Recipient2 ')
        self.rejected(f, 'available-recipient-and-mqtt-schema-alters-not-deployment')

    def test_mqtt_flag_alter_removed_is_detected_even_if_guard_name_remains(self):
        f = self.range_mutation('mqtt-flags-guarded-alters', 'ADD syncItems bit', 'ADD OtherFlag bit')
        self.rejected(f, 'available-recipient-and-mqtt-schema-alters-not-deployment')

    def test_remote_ID_collision_not_resolved_by_overwriting_R1_dictionary(self):
        e = copy.deepcopy(v.load(v.ENTRY))
        e['remote_root_id_collisions'][0]['existing_R1_dictionary'] = e['remote_root_id_collisions'][0]['remote_R10_dictionary']
        self.assertIn('preservation:R1-ID-not-reused:P7-164', v.preservation_errors(e))

    def test_changed_published_expected_identity_is_rejected(self):
        e = copy.deepcopy(v.load(v.ENTRY))
        e['published_audit_file_identities']['docs/audit/PHASE-07B39R10.md']['bytes'] += 1
        self.assertIn('preservation:published-audit:docs/audit/PHASE-07B39R10.md', v.preservation_errors(e))

    def test_published_entry_not_silently_reduced(self):
        e = copy.deepcopy(v.load(v.ENTRY))
        e['published_audit_file_identities'].pop('docs/audit/PHASE-07B39R10.md')
        self.assertIn('preservation:published1686-entry', v.preservation_errors(e))

    def test_new_finding_number_in_question_is_rejected(self):
        err = self.bad_evidence(v.REVIEW, lambda o: o['source_questions'][0].update(new_numbered_finding_id='P7-168'))
        self.assertIn('evidence:bounded-question:R11Q-RECIPIENT', err)

    def test_provider_failure_claim_cannot_be_promoted_by_source_hash(self):
        err = self.bad_evidence(v.REVIEW, lambda o: o['source_questions'][0].update(observed_provider_or_financial_failure=True))
        self.assertIn('evidence:bounded-question:R11Q-RECIPIENT', err)

    def test_original_root_certainty_cannot_be_silently_changed(self):
        err = self.bad_evidence(v.REVIEW, lambda o: o['focused_root_comparisons'][0]['canonical_dictionary_verbatim'].update(certainty='runtime-confirmed'))
        self.assertIn('evidence:root-dictionary-and-qualified-comparison:P1-009', err)

    def test_bounded_review_is_not_independent_human_reading_attestation(self):
        err = self.bad_evidence(v.READS, lambda o: o.update(independent_human_review_claimed=True))
        self.assertIn('evidence:honest-source-review-provenance', err)

    def test_27_body_review_cannot_omit_a_selected_body(self):
        err = self.bad_evidence(v.READS, lambda o: o['selected_method_reviews'].pop())
        self.assertIn('evidence:selected-body-review-coverage-not-reading-proof', err)

    def test_source_basis_hash_change_is_rejected(self):
        err = self.bad_evidence(v.REVIEW, lambda o: o['source_questions'][0]['source_basis'][0].update(syntax_utf8_sha256='0' * 64))
        self.assertTrue(any(s.startswith('evidence:source-basis:') for s in err))

    def test_external_handoff_cannot_be_accepted_while_local_remains(self):
        err = self.bad_evidence(v.REVIEW, lambda o: o['unavailable_contracts_not_accepted_as_handoffs'][0].update(accepted_external_handoff=True))
        self.assertIn('evidence:individually-qualified-boundary:R11BOUND-MODEL', err)

    def test_remote_report_is_not_user_7C_authorization(self):
        err = self.bad_evidence(v.REVIEW, lambda o: o.update(remote_scope_claims_adopted_as_authorization=True))
        self.assertIn('evidence:no-remote-authorization-or-lost-evidence-adoption', err)

    def test_26_capabilities_cannot_be_reduced_to_receipt_settings_slice(self):
        err = self.bad_evidence(v.LEDGER, lambda o: o['capabilities'].pop())
        self.assertIn('evidence:26-canonical-capabilities', err)

    def test_one_capability_exit_not_issued_by_this_bounded_slice(self):
        err = self.bad_evidence(v.LEDGER, lambda o: o['capabilities'][0].update(whole_capability_certified=True))
        self.assertIn('evidence:independent-open-carry:CAP7B38-D01', err)

    def test_original37_ancestry_cannot_be_replaced_by_new_claim(self):
        ledger = v.load(v.LEDGER)
        self.assertEqual(ledger['original37_R9_ancestry_verbatim'], 37)  # upstream counter, not the rows
        self.assertEqual(sum(len(b['records']) for b in ledger['preserved_R8_ancestry_object_verbatim']['bundles']), 37)
        err = self.bad_evidence(v.LEDGER, lambda o: o['preserved_R8_ancestry_object_verbatim']['bundles'][0]['records'].pop())
        self.assertIn('evidence:37-and-R6-flags-preserved', err)

    def test_family_certificate_not_derived_from_recipient_subquestion(self):
        err = self.bad_evidence(v.LEDGER, lambda o: o['family_nonexit_decisions'][1].update(certificate_issued=True))
        self.assertIn('evidence:family-preserved-and-nonexit:R2', err)

    def test_date_note_cannot_relabel_prior_executed_files(self):
        err = self.bad_evidence(v.DATE_NOTE, lambda o: o.update(old_executed_files_relabelled=True))
        self.assertIn('evidence:date-not-chronology-attestation', err)


if __name__ == '__main__':
    unittest.main()
