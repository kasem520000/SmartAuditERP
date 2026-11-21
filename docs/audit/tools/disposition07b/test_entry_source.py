#!/usr/bin/env python3
"""R7 audit regression/mutation tests of actual source and isolated evidence.

Never run C#, SQL, WPF, business arithmetic, provider/migration/SDK code or access
business rows. Mutation rejection invalidates a recorded claim, not a proposed
application fix. All historical suites and genuine failed streams stay untouched.
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

import verify_entry_source as v


class EntrySourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)
        cls.reads = v.load(v.READS)

    def changed_member(self, rel, selector, old, new, expected=1):
        original = v.base.decode((v.ROOT / rel).read_bytes())
        code = v.method(self.facts, rel, selector)['syntax_text']
        if '\r\n' in code:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        self.assertEqual(code.count(old), expected, 'Mutate actual selected source, not an invented fixture')
        self.assertEqual(original.count(code), 1)
        modified = original.replace(code, code.replace(old, new), 1)
        result = copy.deepcopy(self.facts)
        result['methods'][rel][selector] = v.source_methods(modified, [selector])[selector]
        if rel == v.EO and selector == 'ShowEntrySource': result['navigation_sites'] = v.navigation_sites(modified)
        return result

    def rejected(self, facts):
        self.assertTrue(v.source_errors(facts), 'The source mutation must invalidate a recorded source assertion')

    def bad_evidence(self, name, mutate):
        with tempfile.TemporaryDirectory(prefix='smartaudit-r7-evidence-') as tmp:
            ev = Path(tmp)
            for n in (v.FACTS, v.READS, v.REVIEW, v.MATRIX, v.WORK, v.ROOTS, v.CORRECTION):
                shutil.copyfile(v.EV / n, ev / n)
            obj = json.loads((ev / name).read_bytes())
            mutate(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev)

    def test_facts_rederive_from_original_48_source_identities(self):
        self.assertEqual(v.derive(), self.facts)

    def test_actual_recorded_source_assertions_consistent_not_runtime(self):
        self.assertEqual(v.source_errors(self.facts), [])
        self.assertEqual(self.facts['application_execution_count'], 0)

    def test_displayed_ranges_cover_selected_whole_methods_not_all_helpers(self):
        self.assertEqual(v.prior.read_errors(self.reads, self.facts), [])
        self.assertFalse(self.reads['extraction_equals_reading'])
        self.assertFalse(self.reads['independent_human_review_claimed'])

    def test_all_prior_audit_inputs_and_827_application_sources_preserved(self):
        self.assertEqual(v.preservation_errors(v.load(v.ENTRY)), [])

    def test_all_evidence_links_and_decisions_consistent_not_semantic_or_date_authentication(self):
        self.assertEqual(v.evidence_errors(), [])

    def test_exact_original_seven_callers_and_five_pending_bodies_carried(self):
        old = [r for r in v.load(v.OLD_WORK)['calls'] if r['family'] == 'entry-source']
        work = v.load(v.WORK)
        self.assertEqual([r['original_R6_call_row'] for r in work['individual_caller_dispositions']], old)
        self.assertEqual(len(old), 7)
        self.assertEqual(sum(not r['containing_context_selected_and_read_in_R6'] for r in old), 5)

    def test_seventeen_exact_syntax_sites_are_not_seventeen_distinct_receiver_types(self):
        sites = self.facts['navigation_sites']
        self.assertEqual(len(sites), 17)
        self.assertEqual(len({r['receiver_type_syntax'] for r in sites}), 14)
        self.assertTrue(all(not r['compiler_bound_target'] for r in sites))

    def test_open_completion_gate_exit_two_is_not_green_completion(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out): code = v.main(['--verify', '--require-complete'])
        result = json.loads(out.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(result['errors'], [])
        self.assertFalse(result['whole_7B_static_assessment_complete'])
        self.assertEqual(result['capability_exit_certificates_issued'], 0)

    def test_recovery_restored_published_R6_without_reconstructing_missing_history(self):
        receipt = v.load('entry-recovery-receipt-07B39R7.json')
        self.assertEqual(receipt['restored_HEAD'], v.BASE_HEAD)
        self.assertEqual(receipt['preserved_entry_files'], 1216)
        self.assertEqual(receipt['application_sources_checked_unchanged'], 827)
        self.assertFalse(receipt['missing_R2_R3_reconstructed'])
        self.assertFalse(receipt['new_duplicate_archive_committed'])
        self.assertEqual(v.identity(receipt['existing_R4_archive_identity']['path']), receipt['existing_R4_archive_identity'])
        self.assertFalse((v.ROOT / 'docs/.entry-recovery-07B39R7.tar.gz').exists())

    def test_R6_attribution_note_is_prospective_not_retroactive_authentication(self):
        note = v.load(v.CORRECTION)
        self.assertFalse(note['prior_actual_display_chronology_reconstructed'])
        self.assertFalse(note['R6_consumed_log_rewritten'])
        self.assertTrue(note['prospective_R7_reread_is_not_retroactive_R6_read_certification'])
        self.assertEqual(len(note['preserved_original_R6_range_rows']), 7)

    def test_cost_balance_uses_global_key_not_display_doc_number(self):
        self.rejected(self.changed_member(v.CC, 'LoadPeriodData', 'dt.Rows[i]["GlobalID"].ToString()', 'dt.Rows[i]["doc_no"].ToString()'))

    def test_cost_balance_zero_opening_key_guard_is_not_silently_removed(self):
        self.rejected(self.changed_member(v.CC, 'BtnDetailCell_Click', ' && globalId != "0"', ''))

    def test_customer_key_has_not_been_reinterpreted_as_integer_doc_number(self):
        self.rejected(self.changed_member(v.CU, 'ShowAccount', 'row["GlobalID"]?.ToString()', 'row["doc_no"]?.ToString()'))

    def test_customer_result_key_column_remains_string(self):
        self.rejected(self.changed_member(v.CU, 'BuildResultTable', 'Columns.Add("DgvEntryNo", typeof(string))', 'Columns.Add("DgvEntryNo", typeof(int))'))

    def test_customer_background_query_captures_its_own_global_connection(self):
        self.rejected(self.changed_member(v.CU, 'ShowAccount', 'using (var bgConn = MainClass.ConnObj())', 'using (var bgConn = new SqlConnection(_conn.ConnectionString))'))

    def test_customer_handler_uses_current_item_not_an_invented_sender_row_binding(self):
        self.rejected(self.changed_member(v.CU, 'BtnDetail_CellClick', 'GridControl1.CurrentItem', 'GridControl1.SelectedItem'))

    def test_last_payment_entry_key_is_GlobalID_not_local_id(self):
        self.rejected(self.changed_member(v.LAST, 'ShowResult', 'entryRow["GlobalID"]', 'entryRow["id"]'))

    def test_employee_handler_reads_recorded_key_field_not_date(self):
        self.rejected(self.changed_member(v.EMP, 'BtnDetail_CellClick', 'rowView["DgvEntryNo"]', 'rowView["DgvDate"]'))

    def test_cost_report_aggregate_key_is_empty_not_a_document_reference(self):
        self.rejected(self.changed_member(v.RPT, 'ShowResult', 'DgvEntryGlobalId    = ""', 'DgvEntryGlobalId    = "0"'))

    def test_cost_report_does_not_invent_nonempty_guard_in_original_body(self):
        self.rejected(self.changed_member(v.RPT, 'BtnDetail_Click', 'EntryOper.ShowEntrySource(globalId);', 'if (!string.IsNullOrEmpty(globalId)) EntryOper.ShowEntrySource(globalId);'))

    def test_XAML_cost_balance_click_carries_global_key_not_doc_no(self):
        f = copy.deepcopy(self.facts)
        row = next(r for r in f['xml_elements'][v.CC[:-3]] if r['attributes'].get('Click') == 'BtnDetailCell_Click')
        row['attributes']['Tag'] = '{Binding Path=RowData.Row.DgvEntryNo}'
        self.rejected(f)

    def test_XAML_current_item_button_has_no_fabricated_Tag_key_argument(self):
        f = copy.deepcopy(self.facts)
        row = next(r for r in f['xml_elements'][v.CU[:-3]] if r['attributes'].get('Click') == 'BtnDetail_CellClick')
        row['attributes']['Tag'] = '{Binding DgvEntryNo}'
        self.rejected(f)

    def test_dispatcher_parameter_does_not_carry_a_database_origin(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', '(string glid)', '(string glid, string database)'))

    def test_dispatcher_void_is_not_relabelled_as_a_typed_result(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'public static void ShowEntrySource', 'public static bool ShowEntrySource'))

    def test_dispatcher_uses_current_global_factory_not_original_report_connection(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'using SqlConnection conn = MainClass.ConnObj();', 'using SqlConnection conn = new SqlConnection(MainClass.originalConnStr);'))

    def test_entry_lookup_currently_has_no_invented_IS_Deleted_filter(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', "FROM Entry WHERE GlobalId = N'{glid}'", "FROM Entry WHERE IS_Deleted=0 AND GlobalId = N'{glid}'"))

    def test_invoice_probe_uses_Entry_id_not_doc_no(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'int docNo = Convert.ToInt32(entryRow["id"]);', 'int docNo = Convert.ToInt32(entryRow["doc_no"]);'))

    def test_invoice_probe_retains_loaded_branch(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'EntryID={docNo} AND branch={branch}', 'EntryID={docNo}'))

    def test_invoice_request_has_actual_id_type_proc_and_branch(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'id={invId} AND branch={branch}', 'id={invId}'))

    def test_receiver_type_swap_same_site_count_is_rejected(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'frmInvPurch f = new frmInvPurch();', 'frmInvPOS f = new frmInvPOS();'))

    def test_duplicate_invoice_pair_same_seventeen_count_is_rejected(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'f.Navigate(invQuery(1, 2))', 'f.Navigate(invQuery(1, 1))'))

    def test_receipt_five_query_does_not_accidentally_request_type_six(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'Receipts WHERE ReceiptType=5', 'Receipts WHERE ReceiptType=6'))

    def test_note_query_cannot_be_claimed_branch_scoped_when_original_omits_it(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'Doc_Type=1 AND Doc_No={docNoStr}', 'Doc_Type=1 AND Doc_No={docNoStr} AND BranchId={branchStr}'))

    def test_unknown_invoice_hit_does_not_fall_through_after_six_pairs(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource',
            'f.Show(); f.Navigate(invQuery(3, 2)); f.Activate();\n                }\n                return;',
            'f.Show(); f.Navigate(invQuery(3, 2)); f.Activate();\n                }\n                int unused = 0;'))

    def test_same_physical_line_Show_Navigate_order_is_checked_in_source(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource',
            'f.Show(); f.Navigate(invQuery(1, 1)); f.Activate();',
            'f.Navigate(invQuery(1, 1)); f.Show(); f.Activate();'))

    def test_case_activate_missing_is_not_a_successful_open_receipt(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'fcn.Activate();', 'fcn.Focus();'))

    def test_dispatcher_has_no_fabricated_direct_generic_permission_call(self):
        self.rejected(self.changed_member(v.EO, 'ShowEntrySource', 'sq.Show();', 'MainClass.ApplyPermissionToForm(sq); sq.Show();'))

    def test_purchase_navigate_clears_before_shared_binding(self):
        self.rejected(self.changed_member(v.PURCH, 'Navigate',
            'if (this.Invoic != null)\n                this.CLR();',
            'if (this.Invoic != null)\n                this.txtNo.Text = "";'))

    def test_sale_navigate_first_clear_not_confused_with_empty_else_clear(self):
        self.rejected(self.changed_member(v.SALE, 'Navigate', 'if (Invoic != null) CLR();', 'if (Invoic != null) BindingControls();'))

    def test_POS_navigate_preclear_is_not_erased_by_count_only_guards(self):
        self.rejected(self.changed_member(v.POS, 'Navigate',
            'CLR();\n            InvoiceOper.BindingInvoice', 'BindingControls();\n            InvoiceOper.BindingInvoice'))

    def test_shared_binder_empty_and_outer_failure_are_both_null_not_new_object(self):
        self.rejected(self.changed_member(v.IP, 'BindingInvoice', 'Invo = null;', 'Invo = new InvoiceDGV();', expected=2))

    def test_per_item_catch_does_not_invent_failure_propagation(self):
        self.rejected(self.changed_member(v.IP, 'BindingInvoice',
            'catch (Exception projectError4)\n\t\t\t\t\t\t\t\t{',
            'catch (Exception projectError4)\n\t\t\t\t\t\t\t\t{ throw;'))

    def test_SandQ_post_close_EmpId_reads_are_real_not_assumed_in_all_receipts(self):
        rel = v.P + 'frmSandQ.xaml.cs'
        old = 'reader.Close();\n\n            // تحميل اسم المحرر\n            LoadEditorName(reader["EmpId"] != DBNull.Value\n                ? Convert.ToInt32(reader["EmpId"]) : 0);'
        new = 'int emp = reader["EmpId"] != DBNull.Value ? Convert.ToInt32(reader["EmpId"]) : 0;\n            reader.Close();\n            LoadEditorName(emp);'
        self.rejected(self.changed_member(rel, 'ReadData', old, new))

    def test_SandQ_argument_access_is_not_within_callee_catch(self):
        self.rejected(self.changed_member(v.P + 'frmSandQ.xaml.cs', 'ReadData',
            'LoadEditorName(reader["EmpId"] != DBNull.Value\n                ? Convert.ToInt32(reader["EmpId"]) : 0);',
            'try { LoadEditorName(reader["EmpId"] != DBNull.Value\n                ? Convert.ToInt32(reader["EmpId"]) : 0); } catch { }'))

    def test_SandQD_contrasting_reader_reads_no_field_after_normal_close(self):
        self.rejected(self.changed_member(v.P + 'frmSandQD.xaml.cs', 'ReadData',
            'reader.Close(); // ← الآن آمن', 'reader.Close(); int extra = Convert.ToInt32(reader["EmpId"]); // ← الآن آمن'))

    def test_receipt_empty_branch_returns_before_any_CLR(self):
        self.rejected(self.changed_member(v.P + 'frmSandVAT.xaml.cs', 'ReadData',
            'if (!reader.HasRows) { reader.Close();', 'if (!reader.HasRows) { CLR(); reader.Close();'))

    def test_SandD_normal_tail_is_not_falsely_given_a_finally(self):
        self.rejected(self.changed_member(v.P + 'frmSandD.xaml.cs', 'Navigate',
            'ReadData(dr);', 'try { ReadData(dr); } finally { conn.Close(); }'))

    def test_rental_no_rows_clears_before_return(self):
        self.rejected(self.changed_member(v.RENT, 'ReadData',
            'if (!dr.HasRows) { this.CLR(); return; }', 'if (!dr.HasRows) { return; }'))

    def test_rental_print_flag_has_no_invented_load_result_guard(self):
        self.rejected(self.changed_member(v.RENT, 'Navigate',
            'this.SrchPrint = true;', 'if (false) this.SrchPrint = true;'))

    def test_initial_entry_detail_uses_current_not_loaded_header_branch(self):
        self.rejected(self.changed_member(v.INITIAL, 'ReadDataFromReader',
            'WHERE branch = {MainClass.BranchNo}', 'WHERE branch = 100'))

    def test_manual_entry_distinctly_restores_header_branch_in_UI(self):
        self.rejected(self.changed_member(v.NEW, 'ReadData',
            'txtBranch.Text = dr["branch"].ToString();', 'txtBranch.Text = MainClass.BranchNo.ToString();'))

    def test_credit_note_relooks_up_entry_by_current_branch(self):
        self.rejected(self.changed_member(v.CREDIT, 'ReadData',
            'Code.ToString(), 16, MainClass.BranchNo', 'Code.ToString(), 16, 0'))

    def test_debt_note_relooks_up_entry_by_current_branch(self):
        self.rejected(self.changed_member(v.DEBT, 'ReadData',
            '_currentCode.ToString(), 17, MainClass.BranchNo', '_currentCode.ToString(), 17, 0'))

    def test_global_note_number_counterevidence_is_not_silently_made_branch_local(self):
        self.rejected(self.changed_member(v.DEBT, 'LoadNextNumber',
            'CreditDeptNotes WHERE Doc_Type=2', 'CreditDeptNotes WHERE Doc_Type=2 AND BranchId=1'))

    def test_customer_loaded_later_all_branches_flag_is_not_hidden(self):
        self.rejected(self.changed_member(v.CU, 'FrmCustAccountGet_Loaded',
            'chkAllBranches.IsChecked = true;', 'chkAllBranches.IsChecked = false;'))

    def test_FormPermission_original_default_is_true_not_an_invented_deny(self):
        self.rejected(self.changed_member(v.FP, 'ctor:FormPermission', 'Editable = true;', 'Editable = false;'))

    def test_generic_permission_empty_result_currently_returns_not_throws(self):
        self.rejected(self.changed_member(v.MC, 'ApplyPermissionToForm@System.Windows.Window',
            'if (dt.Rows.Count == 0) return;', 'if (dt.Rows.Count == 0) throw new Exception();'))

    def test_purchase_has_its_own_loaded_permission_call(self):
        self.rejected(self.changed_member(v.PURCH, 'frmSalePurch_Load',
            'this.FrmPermission.ApplyFrmPermission(this);', 'this.txtNo.Text = "";'))

    def test_sale_code_loaded_subscription_is_real_not_XAML_only(self):
        self.rejected(self.changed_member(v.SALE, 'ctor:frmInvSale',
            'Loaded += Window_Loaded;', 'Loaded -= Window_Loaded;'))

    def test_POS_CLR_writes_proc_type_one_even_when_dispatch_request_is_return(self):
        self.rejected(self.changed_member(v.POS, 'CLR', 'ProcType = 1;', 'ProcType = 2;'))

    def test_receipt_Loaded_calls_local_restore_not_an_absent_SDK(self):
        self.rejected(self.changed_member(v.P + 'frmSandQ.xaml.cs', 'Window_Loaded',
            'RestorePreviousReceipt();', 'SetStatus("ready");'))

    def test_legacy_receipt_Q_restore_contains_delete_source_not_a_pure_read(self):
        self.rejected(self.changed_member(v.P + 'frmSandQ.xaml.cs', 'RestorePreviousReceipt',
            'DELETE FROM SandQ WHERE id=', 'SELECT * FROM SandQ WHERE id='))

    def test_legacy_receipt_D_restore_calls_SaveReceipt2_before_delete(self):
        self.rejected(self.changed_member(v.P + 'frmSandD.xaml.cs', 'RestorePreviousReceipt',
            'new ReceiptOper().SaveReceipt2(receipt)', 'new ReceiptOper().SaveReceipt1(receipt)'))

    def test_supplied_Inv_primary_key_is_global_not_local_id(self):
        f = copy.deepcopy(self.facts)
        r = f['text_ranges']['Inv-create']
        r['text'] = r['text'].replace('[InvGlobalID] ASC', '[id] ASC')
        self.rejected(f)

    def test_supplied_note_branch_column_is_not_described_as_absent(self):
        f = copy.deepcopy(self.facts)
        r = f['text_ranges']['CreditDeptNotes-create']
        r['text'] = r['text'].replace('[BranchId] [int] NULL', '')
        self.rejected(f)

    def test_original_call_identity_change_same_row_count_rejected(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda j: j['individual_caller_dispositions'][0]['original_R6_call_row'].__setitem__('line', 999)))

    def test_caller_body_hash_change_rejected(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda j: j['individual_caller_dispositions'][0].__setitem__('current_whole_context_sha256', '0' * 64)))

    def test_pending_LastProcess_identity_cannot_be_dropped(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda j: j['remaining_original_R6_non_entry_calls'].pop()))

    def test_worklist_cannot_claim_whole_D17_complete(self):
        self.assertTrue(self.bad_evidence(v.WORK, lambda j: j.__setitem__('whole_D17_complete', True)))

    def test_matrix_reader_hash_must_match_actual_shared_or_local_reader(self):
        self.assertTrue(self.bad_evidence(v.MATRIX, lambda j: j['routes'][0].__setitem__('reader_whole_context_sha256', '0' * 64)))

    def test_matrix_same_count_receiver_swap_rejected(self):
        self.assertTrue(self.bad_evidence(v.MATRIX, lambda j: j['routes'][0]['source_site'].__setitem__('receiver_type_syntax', 'frmInvPOS')))

    def test_matrix_cannot_omit_Partial_outcome_category(self):
        self.assertTrue(self.bad_evidence(v.MATRIX, lambda j: j['routes'][0]['source_outcomes'].pop('Partial')))

    def test_matrix_cannot_label_audit_categories_actual_CSharp_return_types(self):
        self.assertTrue(self.bad_evidence(v.MATRIX, lambda j: j['routes'][0].__setitem__('outcome_labels_are_audit_categories_not_CSharp_return_types', False)))

    def test_matrix_cannot_claim_runtime_observed(self):
        self.assertTrue(self.bad_evidence(v.MATRIX, lambda j: j['routes'][0].__setitem__('runtime_observed', True)))

    def test_canonical_capability_dictionary_must_be_preserved(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda j: j['capabilities'][v.TARGETS[0]]['canonical_capability_row'].__setitem__('capability', 'changed')))

    def test_review_cannot_claim_whole_7B_complete(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda j: j.__setitem__('whole_7B_static_assessment_complete', True)))

    def test_no_numbered_finding_is_fabricated_in_review(self):
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda j: j['new_numbered_finding_ids'].append('P7-168')))

    def test_historical_potential_is_not_promoted_by_source_tests(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda j: j['focused_root_reviews']['P7-132']['canonical_prior_row'].__setitem__('certainty', 'confirmed')))

    def test_unnumbered_post_close_question_not_automatically_merged_under_generic_navigation_root(self):
        def change(j):
            next(r for r in j['candidate_dispositions'] if r['id'] == 'R7C-RECEIPT-READER')['root_id'] = 'P7-061'
        self.assertTrue(self.bad_evidence(v.ROOTS, change))

    def test_all345_novelty_claim_cannot_be_invented_with_six_rows_missing(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda j: j.__setitem__('all345_roots_screened', True)))

    def test_attribution_note_cannot_reconstruct_prior_display_history(self):
        self.assertTrue(self.bad_evidence(v.CORRECTION, lambda j: j.__setitem__('prior_actual_display_chronology_reconstructed', True)))

    def test_missing_current_reread_range_rejected_not_masked_by_R6_hashes(self):
        def change(j):
            j['reads'] = [r for r in j['reads'] if not (r['path'] == v.STMT and r['start'] == 760)]
        self.assertTrue(self.bad_evidence(v.READS, change))

    def test_read_range_hash_is_not_accepted_when_text_identity_changes(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'][0]['decoded_range_utf8_sha256'] = '0' * 64
        self.assertTrue(v.prior.read_errors(reads, self.facts))

    def test_changed_prior_audit_identity_rejected_without_touching_worktree(self):
        entry = copy.deepcopy(v.load(v.ENTRY))
        key = next(k for k in entry['preserved_tracked_audit_inputs'] if k.endswith('test_session_year.py'))
        entry['preserved_tracked_audit_inputs'][key]['sha256'] = '0' * 64
        self.assertTrue(v.preservation_errors(entry))

    def test_post_recovery_HEAD_identity_cannot_be_relabelled_as_reset_baseline(self):
        entry = copy.deepcopy(v.load(v.ENTRY))
        entry['HEAD'] = '10ba215152f722c8808aea0bb672c1d1d4d9d711'
        self.assertTrue(v.preservation_errors(entry))

    def test_original_findings_raw_336_CRLF_bytes_preserved(self):
        raw = (v.AUDIT / 'findings.csv').read_bytes()
        self.assertEqual(len(raw), 222939)
        self.assertEqual(raw.count(b'\r\n'), 336)
        self.assertEqual(v.base.sha(raw), 'ce8c8b823a9a683d446d73dc4ffe564039f1542b649aeda79acd4c7a6600c42a')


if __name__ == '__main__':
    unittest.main()
