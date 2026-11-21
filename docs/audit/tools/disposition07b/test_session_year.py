#!/usr/bin/env python3
"""R6 audit regressions: mutate original C# syntax or isolated evidence, never ERP.

No arithmetic reimplementation, SQL execution, WPF, credentials or live business
rows. A passing guard checks recorded source assertions, not semantic completeness.
The failed historical B38 expectation and all R1/R4/R5 tests remain untouched.
"""
from __future__ import annotations

import contextlib
import copy
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import verify_session_year as v


class SessionYearTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)
        cls.reads = v.load(v.READS)

    def changed_member(self, rel, selector, old, new, expected=1):
        original = v.base.decode((v.ROOT / rel).read_bytes())
        code = v.method(self.facts, rel, selector)['syntax_text']
        if '\r\n' in code:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        self.assertEqual(code.count(old), expected, 'Mutate the actual selected source, not an invented fixture')
        self.assertEqual(original.count(code), 1)
        changed = original.replace(code, code.replace(old, new), 1)
        result = copy.deepcopy(self.facts)
        result['methods'][rel][selector] = v.source_methods(changed, [selector])[selector]
        return result

    def rejected(self, facts):
        self.assertTrue(v.source_errors(facts), 'Changed source must invalidate at least one recorded source claim')

    def bad_evidence(self, name, mutate):
        with tempfile.TemporaryDirectory(prefix='smartaudit-r6-evidence-') as tmp:
            ev = Path(tmp)
            for n in (v.FACTS, v.REVIEW, v.WORK, v.ROOTS):
                shutil.copyfile(v.EV / n, ev / n)
            obj = json.loads((ev / name).read_bytes())
            mutate(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev)

    def test_facts_rederive_from_original_21_source_identities(self):
        self.assertEqual(v.derive(), self.facts)

    def test_actual_source_guards_are_consistent_not_runtime_acceptance(self):
        self.assertEqual(v.source_errors(self.facts), [])
        self.assertEqual(self.facts['application_execution_count'], 0)

    def test_displayed_read_ranges_cover_every_selected_whole_body(self):
        self.assertEqual(v.read_errors(self.reads, self.facts), [])
        self.assertFalse(self.reads['extraction_equals_reading'])

    def test_original_twelve_pending_body_identities_are_preserved_individually(self):
        old = v.load(v.OLD_WORK)
        pending = {(r['path'], r['containing_member'], r['context_start'], r['context_end'])
                   for r in old['writes'] if not r['whole_context_read_in_R5']}
        self.assertEqual({tuple(r) for r in v.load(v.WORK)['twelve_original_pending_bodies']}, pending)
        for rel, name, start, end in pending:
            f = v.method(self.facts, rel, name)
            self.assertEqual((f['start'], f['end']), (start, end))

    def test_original_application_and_all_1434_prior_audit_inputs_preserved(self):
        self.assertEqual(v.preservation_errors(v.load(v.ENTRY)), [])

    def test_evidence_decisions_and_exact_write_identities_are_consistent(self):
        self.assertEqual(v.evidence_errors(), [])

    def test_open_gate_is_exit_two_not_green_completion_or_test_failure(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = v.main(['--verify', '--require-complete'])
        self.assertEqual(code, 2)
        result = json.loads(out.getvalue())
        self.assertEqual(result['errors'], [])
        self.assertFalse(result['whole_7B_static_assessment_complete'])
        self.assertEqual(result['capability_exit_certificates_issued'], 0)

    def test_connection_factory_does_not_follow_database_name_field_implicitly(self):
        self.rejected(self.changed_member(v.MC, 'ConnObj', 'new SqlConnection(connstr)', 'new SqlConnection(Database)'))

    def test_home_startup_writer_does_not_invent_global_string_rebuild(self):
        self.rejected(self.changed_member(v.HOME, 'checkConn',
            'MainClass.Database = dbName;', 'MainClass.Database = dbName; MainClass.connstr = dbName;'))

    def test_home_loaded_recaptures_global_string_after_startup_check(self):
        self.rejected(self.changed_member(v.HOME, 'Window_Loaded',
            'this.conn = MainClass.ConnObj();', 'this.conn = new SqlConnection(MainClass.Database);'))

    def test_database_display_label_is_not_substituted_for_physical_value(self):
        self.rejected(self.changed_member(v.LOGIN, 'Login',
            'MainClass.DataBaseName = cmbDatabases.Text;', 'MainClass.DataBaseName = txtDatabase;'))

    def test_startup_database_name_uses_selected_value_not_display_text(self):
        self.rejected(self.changed_member(v.LOGIN, 'SaveStartupData',
            'DatabaseName = cmbDatabases.SelectedValue?.ToString() ?? ""', 'DatabaseName = cmbDatabases.Text'))

    def test_master_catalog_value_path_is_not_the_display_alias(self):
        self.rejected(self.changed_member(v.LOGIN, 'loadDBs',
            'cmbDatabases.SelectedValuePath = "name";', 'cmbDatabases.SelectedValuePath = "Dbname";'))

    def test_MARS_in_builder_is_a_local_source_property_not_universal_provider_fact(self):
        self.rejected(self.changed_member(v.LOGIN, 'BuildConnectionStrings',
            'MultipleActiveResultSets=true;', 'MultipleActiveResultSets=false;', expected=3))

    def test_later_branch_loader_fallback_uses_the_actual_connection(self):
        self.rejected(self.changed_member(v.LOGIN, 'LoadBranches',
            'MainClass.connstr = conn.ConnectionString;', 'MainClass.connstr = conn1.ConnectionString;'))

    def test_report_year_switch_requires_both_flag_and_nonnull_selected_value(self):
        self.rejected(self.changed_member(v.STMT, 'btnShow_Click',
            'MainClass.ReturnYearPreviews && CmbYearPreviews.SelectedValue != null', 'MainClass.ReturnYearPreviews'))

    def test_report_restore_clears_the_flag_without_clearing_the_visible_year(self):
        self.rejected(self.changed_member(v.BAL, 'btnShow_Click',
            'MainClass.ReturnYearPreviews = false;', 'MainClass.ReturnYearPreviews = true;'))

    def test_missing_report_restore_flag_is_rejected_without_an_index_error(self):
        self.rejected(self.changed_member(v.STMT, 'btnShow_Click',
            'MainClass.ReturnYearPreviews = false;', 'bool unused = false;'))

    def test_visible_year_cannot_be_claimed_unchanged_if_source_now_clears_it(self):
        self.rejected(self.changed_member(v.STMT, 'btnShow_Click',
            'MainClass.ReturnYearPreviews = false;',
            'MainClass.ReturnYearPreviews = false; CmbYearPreviews.SelectedIndex = -1;'))

    def test_report_restore_is_not_an_unwritten_finally(self):
        self.rejected(self.changed_member(v.STMT, 'btnShow_Click',
            'ShowResult();', 'try { ShowResult(); } finally { }'))

    def test_main_statement_and_detailed_balance_index_zero_policies_differ(self):
        self.rejected(self.changed_member(v.STMT, 'CmbYearPreviews_SelectionChanged',
            'SelectedIndex >= 0', 'SelectedIndex > 0'))

    def test_report_detail_does_not_fabricate_a_database_context_argument(self):
        self.rejected(self.changed_member(v.BAL, 'BtnShowDetail_Click',
            'EntryOper.ShowEntrySource(btn.Tag.ToString());',
            'EntryOper.ShowEntrySource(btn.Tag.ToString() + CmbYearPreviews.Text);'))

    def test_entry_dispatcher_parameter_is_only_the_global_entry_key(self):
        self.rejected(self.changed_member(v.ENTRYOPER, 'ShowEntrySource',
            'ShowEntrySource(string glid)', 'ShowEntrySource(string glid, string year)'))

    def test_entry_dispatcher_uses_the_factory_not_the_prior_report_connection(self):
        self.rejected(self.changed_member(v.ENTRYOPER, 'ShowEntrySource',
            'using SqlConnection conn = MainClass.ConnObj();',
            'using SqlConnection conn = new SqlConnection(MainClass.originalConnStr);'))

    def test_entry_dispatcher_uses_loaded_entry_id_not_doc_no_as_EntryID(self):
        self.rejected(self.changed_member(v.ENTRYOPER, 'ShowEntrySource',
            'int docNo = Convert.ToInt32(entryRow["id"]);', 'int docNo = Convert.ToInt32(entryRow["doc_no"]);'))

    def test_linked_parent_clears_before_opening_the_void_child(self):
        self.rejected(self.changed_member(v.SALE, 'InsertLinkedReturn',
            'CLR();\n            InvoiceOper.InsertFromInv(ref Invoic, 1);',
            'InvoiceOper.InsertFromInv(ref Invoic, 1);\n            CLR();'))

    def test_linked_parent_tail_is_not_falsely_given_an_acceptance_guard(self):
        self.rejected(self.changed_member(v.SALE, 'InsertLinkedReturn',
            'Invoic.ISNew = true;', 'if (false) Invoic.ISNew = true;'))

    def test_linked_parent_does_not_call_the_ordinary_dirty_guard(self):
        self.rejected(self.changed_member(v.SALE, 'InsertLinkedFromQuotation',
            'CLR();', 'if (CheckBeforeClear()) return; CLR();'))

    def test_shared_linked_backup_is_not_an_unwritten_window_local_backup(self):
        self.rejected(self.changed_member(v.SALE, 'InsertLinkedCreditNote',
            'MainClass.originalConnStr = MainClass.connstr;', 'string backup = MainClass.connstr;'))

    def test_linked_caller_has_no_own_restore_finally_or_tail(self):
        self.rejected(self.changed_member(v.SALE, 'InsertLinkedReturn',
            'Invoic.User = MainClass.EmpNo;',
            'Invoic.User = MainClass.EmpNo; MainClass.connstr = MainClass.originalConnStr;'))

    def test_void_helper_pre_binding_cancel_return_is_preserved(self):
        self.rejected(self.changed_member(v.IP, 'InsertFromInv', 'return;', 'throw new InvalidOperationException();'))

    def test_selected_items_restores_string_without_clearing_year_flag(self):
        self.rejected(self.changed_member(v.ITEMS, 'btnadd_Click',
            'MainClass.connstr = MainClass.originalConnStr;',
            'MainClass.connstr = MainClass.originalConnStr; MainClass.ReturnYearPreviews = false;'))

    def test_all_items_has_the_distinct_false_flag_tail(self):
        self.rejected(self.changed_member(v.ITEMS, 'btnAddall_Click',
            'MainClass.ReturnYearPreviews = false;', 'MainClass.ReturnYearPreviews = true;'))

    def test_items_cancel_does_not_invent_session_restoration(self):
        self.rejected(self.changed_member(v.ITEMS, 'CloseWithoutResult',
            'ISDone = false;', 'ISDone = false; MainClass.connstr = MainClass.originalConnStr;'))

    def test_search_escape_is_not_the_explicit_restore_button(self):
        self.rejected(self.changed_member(v.SEARCH, 'Window_KeyDown',
            'else if (e.Key == Key.Escape) Close();', 'else if (e.Key == Key.Escape) btnClose_Click(this, null);'))

    def test_search_button_restores_the_actual_shared_backup(self):
        self.rejected(self.changed_member(v.SEARCH, 'btnClose_Click',
            'MainClass.connstr = MainClass.originalConnStr;', 'MainClass.connstr = MainClass.Database;'))

    def test_child_connection_is_captured_at_construction(self):
        self.rejected(self.changed_member(v.ITEMS, 'ctor:frmInvoiceItems',
            '_conn = MainClass.ConnObj();', '_conn = new SqlConnection(MainClass.Database);'))

    def test_contract_wiring_is_checked_in_code_not_only_XAML(self):
        self.rejected(self.changed_member(v.CONTRACT, 'SetupButtonEvents',
            'btnInsertLinkedInv.Click += btnInsertLinkedInv_Click;',
            'btnInsertLinkedInv.Click -= btnInsertLinkedInv_Click;'))

    def test_contract_helper_passes_the_distinct_contract_model(self):
        self.rejected(self.changed_member(v.IPC, 'InsertFromInv',
            'frmInvoiceItems2.invcontract = Invo;', 'frmInvoiceItems2.invcontract = new Invoicecontract();'))

    def test_contract_helper_does_not_invent_a_result_assignment_back(self):
        self.rejected(self.changed_member(v.IPC, 'InsertFromInv',
            'frmInvoiceItems2.ShowDialog();', 'frmInvoiceItems2.ShowDialog(); Invo = frmInvoiceItems2.invcontract;'))

    def test_new_number_uses_global_factory_not_parent_captured_connection(self):
        self.rejected(self.changed_member(v.IP, 'InvoiceNo',
            'MainClass.ConnObj()', 'new SqlConnection(MainClass.originalConnStr)'))

    def test_year_mapping_writer_uses_both_label_and_physical_name(self):
        self.rejected(self.changed_member(v.SETTINGS, 'InsertInto_YearPreviews',
            'insert into Year_Previews(Dbname,DbAutoName,Is_Deleted)',
            'insert into Year_Previews(Dbname,WrongName,Is_Deleted)'))

    def test_year_registry_is_readable_local_DDL_not_an_assumed_external_model(self):
        facts = copy.deepcopy(self.facts)
        facts['text_ranges']['year-registry-create']['text'] = facts['text_ranges']['year-registry-create']['text'].replace('[DbAutoName]', '[OtherName]')
        self.rejected(facts)

    def test_missing_actual_body_read_cannot_be_hidden_by_other_read_counts(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'] = [r for r in reads['reads'] if not (r['path'] == v.HOME and r['start'] <= 635 <= r['end'])]
        self.assertTrue(v.read_errors(reads, self.facts))

    def test_missing_XAML_detail_tag_read_is_not_covered_by_a_code_body(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'] = [r for r in reads['reads'] if not (r['path'] == v.STMT[:-3] and r['start'] <= 315 <= r['end'])]
        self.assertTrue(v.read_errors(reads, self.facts))

    def test_extraction_is_not_a_substitute_for_reading_or_independent_review(self):
        reads = copy.deepcopy(self.reads)
        reads['extraction_equals_reading'] = True
        self.assertTrue(v.read_errors(reads, self.facts))

    def test_one_duplicate_write_identity_does_not_satisfy_27_rows(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda x: x['individual_write_dispositions'].__setitem__(1, x['individual_write_dispositions'][0])))

    def test_write_disposition_binds_actual_containing_method_hash(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda x: x['individual_write_dispositions'][0].__setitem__('current_method_sha256', '0' * 64)))

    def test_old_discovery_row_is_not_a_new_body_review_certificate(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda x: x['individual_write_dispositions'][0].__setitem__('whole_containing_context_read_in_R6', False)))

    def test_source_decision_is_not_an_observed_ERP_result(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x['source_decisions'][0].__setitem__('observed_in_ERP', True)))

    def test_distinct_outcomes_need_actual_qualified_dispositions(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x['path_outcomes'][1].__setitem__('source_disposition', '')))

    def test_available339_dictionaries_cannot_be_silently_rewritten(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda x: x['available_prior_rows'][0].__setitem__('severity', 'Low')))

    def test_retention_of339_is_not_claimed_as_full_semantic_rereview(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda x: x.__setitem__('all339_semantically_reread_in_R6', True)))

    def test_conditional_year_question_cannot_get_an_invented_numbered_root(self):
        def change(obj):
            row = next(r for r in obj['candidate_dispositions'] if r['id'] == 'R6C-YEAR-PROVENANCE')
            row['root_id'] = 'P7-174'
        self.assertTrue(self.bad_evidence(v.ROOTS, change))

    def test_extra_candidate_cannot_hide_behind_the_five_expected_records(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda x: x['candidate_dispositions'].append({'id': 'made-up', 'root_id': 'P7-174'})))

    def test_existing_year_root_must_remain_P7_115_not_a_duplicate(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda x: x['candidate_dispositions'][0].__setitem__('root_id', 'P7-174')))

    def test_missing_remaining_local_work_cannot_become_a_capability_exit(self):
        def change(obj):
            row = obj['capabilities']['CAP7B38-D17']
            row['whole_capability_certified'] = True
            row['remaining_readable_local'] = []
        self.assertTrue(self.bad_evidence(v.REVIEW, change))

    def test_local_work_is_not_an_accepted_external_handoff(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.__setitem__('new_accepted_external_handoffs', 1)))

    def test_raw_clock_is_not_calendar_authority_and_a_constant_is_not_attestation(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.__setitem__('raw_clocks_are_calendar_authority', True)))
        self.assertFalse(v.load(v.REVIEW)['raw_clocks_are_calendar_authority'])

    def test_missing196_and_R2_R3_are_not_recertified_from_new_tests(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.__setitem__('prior196_tests_recertified', True)))

    def test_canonical_capability_dictionary_is_retained_not_relabelled(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x['capabilities']['CAP7B38-D17']['canonical_capability_row'].__setitem__('whole_capability_certified', 'true')))

    def test_pinned_predecessor_identity_is_not_just_a_narrative_filename(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x['pinned_inputs'][0].__setitem__('sha256', '0' * 64)))


if __name__ == '__main__':
    unittest.main()
