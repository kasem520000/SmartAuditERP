#!/usr/bin/env python3
"""R8 source/evidence regression and mutation guards, never an ERP emulator.

Mutations reparse actual original C#/XAML in memory; evidence mutations use
isolated temporary copies. Rejection invalidates an audit claim, not a suggested
application repair. No C#, SQL, WPF, model constructor, SDK or arithmetic runs.
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

import verify_linked_activity as v


class LinkedActivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)
        cls.reads = v.load(v.READS)

    def changed_method(self, rel, selector, old, new, count=1):
        original = v.base.decode((v.ROOT / rel).read_bytes())
        member = v.method(self.facts, rel, selector)['syntax_text']
        if '\r\n' in member:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        self.assertEqual(member.count(old), count, 'Mutate actual selected source, not a synthetic ERP implementation')
        self.assertEqual(original.count(member), 1)
        changed = original.replace(member, member.replace(old, new), 1)
        result = copy.deepcopy(self.facts)
        result['methods'][rel][selector] = v.source_methods(changed, [selector])[selector]
        if rel in {r['path'] for r in v.original_calls()}:
            result['call_sites'] = [s for s in result['call_sites'] if s['path'] != rel] + v.selected_call_sites(changed, rel)
        if rel == v.DET:
            result['reopen_sites'] = v.reopen_sites(changed)
        return result

    def rejected(self, facts, expected_guard):
        errors = v.source_errors(facts)
        self.assertTrue(any(expected_guard in e for e in errors), (expected_guard, errors))

    def mutation(self, rel, selector, old, new, expected_guard, count=1):
        self.rejected(self.changed_method(rel, selector, old, new, count), expected_guard)

    def changed_xml(self, rel, old, new):
        text = v.base.decode((v.ROOT / rel).read_bytes())
        self.assertEqual(text.count(old), 1)
        result = copy.deepcopy(self.facts)
        result['xml_elements'][rel] = v.xml_elements(text.replace(old, new, 1), v.XML_SELECTED[rel])
        return result

    def bad_evidence(self, name, change):
        with tempfile.TemporaryDirectory(prefix='smartaudit-r8-evidence-') as tmp:
            ev = Path(tmp)
            for n in v.PACKET:
                shutil.copyfile(v.EV / n, ev / n)
            obj = json.loads((ev / name).read_bytes())
            change(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev)

    def evidence_rejected(self, name, change, guard):
        errors = self.bad_evidence(name, change)
        self.assertTrue(any(guard in e for e in errors), (guard, errors))

    def test_actual_facts_rederive_from_original_sources(self):
        self.assertEqual(v.derive(), self.facts)

    def test_recorded_source_assertions_consistent_not_runtime(self):
        self.assertEqual(v.source_errors(self.facts), [])
        self.assertEqual(self.facts['application_execution_count'], 0)

    def test_selected_whole_contexts_and_XML_are_covered_not_proof_of_reading(self):
        self.assertEqual(v.prior.read_errors(self.reads, self.facts), [])
        self.assertFalse(self.reads['extraction_equals_reading'])
        self.assertFalse(self.reads['independent_human_review_claimed'])
        self.assertFalse(self.reads['individual_read_timestamps_invented'])

    def test_prior1538_audit_and827_application_sources_preserved(self):
        self.assertEqual(v.preservation_errors(v.load(v.ENTRY)), [])

    def test_individual_call_decisions_and_pins_consistent(self):
        self.assertEqual(v.evidence_errors(), [])

    def test_gate_remains_open_exit_two_not_completion(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream): code = v.main(['--verify', '--require-complete'])
        result = json.loads(stream.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(result['errors'], [])
        self.assertFalse(result['whole_7B_static_assessment_complete'])
        self.assertEqual(result['capability_exit_certificates_issued'], 0)

    def test_thirty_exact_R6_rows_preserved_not_just_new_count(self):
        matrix = v.load(v.MATRIX)
        for key, family in (('last_process_calls', 'last-process'), ('linked_insert_calls', 'linked-insert')):
            self.assertEqual([r['original_R6_call_row'] for r in matrix[key]],
                             [r for r in v.original_calls() if r['family'] == family])

    def test_original_three_pending_linked_bodies_have_current_full_contexts(self):
        work = v.load(v.WORK)
        self.assertEqual(len(work['three_original_pending_linked_bodies']), 3)
        self.assertTrue(work['all_thirty_original_containing_bodies_displayed_and_individually_assessed_in_R8'])
        self.assertFalse(work['original_R6_discovery_or_read_flags_rewritten'])

    def test_fourteen_reopen_sites_retain_sixteen_labels_and_seven_types(self):
        sites = self.facts['reopen_sites']
        self.assertEqual(len(sites), 14)
        self.assertEqual(sum(len(s['case_label_syntax']) for s in sites), 16)
        self.assertEqual(len({s['receiver_type_syntax'] for s in sites}), 7)
        self.assertTrue(all(not s['compiler_bound_target'] for s in sites))

    def test_all_nineteen_Show_before_request_is_written_order_not_Loaded_proof(self):
        sites = [s for s in self.facts['call_sites'] if s['family'] == 'last-process']
        self.assertEqual(len(sites), 19)
        self.assertTrue(all(s['same_owner_Show_lines'][0] < s['line'] for s in sites))
        row = next(r for r in v.load(v.ROOTS)['candidate_dispositions'] if r['id'] == 'R8C-LIFECYCLE')
        self.assertEqual(row['prior_certainty_preserved'], 'potential')

    def test_local_legacy_rows_not_marked_as_unavailable_external_models(self):
        for key in ('legacy-local-item-row-class', 'purchase-local-string-row-class',
                    'sale-purchase-local-row-class', 'sales-invoice-local-row-class'):
            self.assertIn('class ', self.facts['text_ranges'][key]['text'])
        rows = v.load(v.MATRIX)['last_process_calls']
        self.assertTrue(all(r['antecedent_source_basis'] for r in rows))

    def test_actual_purchase_party_type_is_counterexample_to_blanket_mismatch(self):
        rows = {r['original_R6_call_row']['id']: r for r in v.load(v.MATRIX)['last_process_calls']}
        self.assertIn('Counterexample', rows['R6NEXT-017']['source_to_argument_trace']['party_type'])
        self.assertIn('matches', rows['R6NEXT-036']['source_to_argument_trace']['party_type'])
        self.assertIn('contradicts', rows['R6NEXT-029']['source_to_argument_trace']['party_type'])

    def test_legacy_customer_intent_is008_not_misleading007_handler_name(self):
        rows = {r['original_R6_call_row']['id']: r for r in v.load(v.MATRIX)['last_process_calls']}
        self.assertIn('item-labelled', rows['R6NEXT-007']['source_to_argument_trace']['party'])
        self.assertIn('P7-130', rows['R6NEXT-008']['source_to_argument_trace']['party'])

    def test_void_receiver_audit_outcome_categories_are_not_CSharp_results(self):
        receiver = v.load(v.MATRIX)['shared_receiver_contract']
        self.assertTrue(receiver['outcome_labels_are_audit_categories_not_CSharp_return_types'])
        self.assertEqual(set(receiver['source_outcomes']), {'NoRequest', 'Requested', 'Empty', 'Failed', 'Partial', 'Denied'})
        self.assertEqual(v.method(self.facts, v.DET, 'LastProcess')['return_type'], 'void')

    def test_focused_comparisons_do_not_recertify339_or_missing345(self):
        roots = v.load(v.ROOTS)
        self.assertEqual(len(roots['available_prior_rows']), 339)
        self.assertEqual(set(roots['focused_root_reviews']), set(v.FOCUSED))
        self.assertFalse(roots['all339_semantically_reread_in_R8'])
        self.assertFalse(roots['all345_roots_screened'])
        self.assertEqual(roots['new_finding_ids'], [])

    def test_requested_reference_label_does_not_overwrite_session_or_entry_date(self):
        note = v.load(v.DATE_NOTE)
        self.assertEqual(note['requested_prospective_assessment_label_utc'], '2026-11-21')
        self.assertEqual(note['session_reference_date_utc'], '2026-11-16')
        self.assertEqual(v.load(v.ENTRY)['assessment_reference_date_utc'], '2026-11-16')
        self.assertFalse(note['requested_label_is_claim_about_today'])
        self.assertFalse(note['past_calendar_or_display_chronology_authenticated'])

    def test_six_bounded_capabilities_do_not_issue26_or_family_exits(self):
        review = v.load(v.REVIEW)
        self.assertEqual(set(review['capabilities']), set(v.TARGETS))
        self.assertTrue(all(not r['whole_capability_certified'] for r in review['capabilities'].values()))
        self.assertEqual(review['four_family_exit_certificates_issued'], 0)
        self.assertFalse(review['phase7C_started'])
        self.assertFalse(review['phase8_authorized'])

    def test_no_unavailable_contract_accepted_before_readable_local_work(self):
        review = v.load(v.REVIEW)
        self.assertTrue(all(not r['accepted_external_handoff'] and r['readable_local_not_delegated']
                            for r in review['unavailable_contracts_not_accepted_as_handoffs']))
        self.assertTrue(all(not r['externalized'] for r in v.load(v.WORK)['remaining_readable_local_tasks']))

    def test_LastProcess_signature_cannot_be_mistaken_for_origin_aware_request(self):
        self.mutation(v.DET, 'LastProcess', 'int clientType)', 'int clientType, int branch)', 'LastProcess-four-ints')

    def test_positive_item_setter_guard_is_recorded(self):
        self.mutation(v.DET, 'LastProcess', 'if (itemId > 0)', 'if (itemId >= 0)', 'positive-only-request-writes')

    def test_party_type_one_is_customer_not_supplier(self):
        self.mutation(v.DET, 'LastProcess', 'if (clientType == 1)', 'if (clientType != 1)', 'positive-only-request-writes')

    def test_store_assignment_does_not_invent_all_store_toggle(self):
        self.mutation(v.DET, 'LastProcess', 'cmbSafes.SelectedValue = storeId;',
                      'cmbSafes.SelectedValue = storeId;\n            chkAll.IsChecked = false;', 'store-request-does-not-clear')

    def test_default_all_stores_is_read_from_real_XAML(self):
        rel = v.DET[:-3]; text = v.base.decode((v.ROOT / rel).read_bytes())
        start = text.index('x:Name="chkAll"'); end = text.index('/>', start)
        fragment = text[start:end]
        self.assertIn('IsChecked="True"', fragment)
        changed = self.changed_xml(rel, fragment, fragment.replace('IsChecked="True"', 'IsChecked="False"'))
        self.rejected(changed, 'store-request-does-not-clear')

    def test_store_filter_depends_on_UI_all_flag(self):
        self.mutation(v.DET, 'ShowResult', 'chkAll.IsChecked != true &&', 'chkAll.IsChecked == true &&', 'filters-use-written-UI-guards')

    def test_party_filter_requires_actual_UI_selection(self):
        self.mutation(v.DET, 'ShowResult', 'cmbClients.SelectedIndex > -1 &&', 'cmbClients.SelectedIndex > 0 &&', 'filters-use-written-UI-guards')

    def test_branch_predicate_does_not_imply_origin_branch(self):
        self.mutation(v.DET, 'ShowResult', 'inv.branch={cmbBranches.SelectedValue}', 'inv.branch={MainClass.BranchNo}', 'UI-branch-query-void')

    def test_last_mode_top_one_is_recorded_not_repaired(self):
        self.mutation(v.DET, 'ShowResult', ' top (1) ', ' top (2) ', 'top1-is-ascending')

    def test_last_mode_sort_ascending_is_not_silently_changed(self):
        self.mutation(v.DET, 'ShowResult', 'ORDER BY inv.date ASC', 'ORDER BY inv.date DESC', 'top1-is-ascending')

    def test_last_mode_bypasses_period_predicate_in_written_else_if(self):
        self.mutation(v.DET, 'ShowResult', 'else if (ckTotalPeriod.IsChecked != true)', 'if (ckTotalPeriod.IsChecked != true)', 'top1-is-ascending')

    def test_activity_join_uses_global_key_before_output_loses_it(self):
        self.mutation(v.DET, 'ShowResult', 'Inv.InvGlobalID=Inv_Sub.InvGlobalID', 'Inv.proc_id=Inv_Sub.proc_id', 'UI-branch-query-void')

    def test_activity_clear_is_not_a_healthy_outcome(self):
        self.mutation(v.DET, 'ShowResult', 'ActivityList.Clear();', '', 'UI-branch-query-void')

    def test_metadata_skip_can_leave_empty_or_partial_display(self):
        self.mutation(v.DET, 'ShowResult', 'if (typeDt.Rows.Count == 0) continue;', 'if (typeDt.Rows.Count == 0) break;', 'row-skips-and-display-key')

    def test_display_invoice_number_remains_local_id_not_global_key(self):
        self.mutation(v.DET, 'ShowResult', 'row["id"]?.ToString()', 'row["InvGlobalID"]?.ToString()', 'row-skips-and-display-key')

    def test_constructor_report_connection_is_new_global_capture(self):
        self.mutation(v.DET, 'ctor:frmRptItemsActivityDetailed', 'conn1       = MainClass.ConnObj();', 'conn1       = conn;', 'receiver-fresh-global-capture')

    def test_connection_factory_not_invented_as_original_year_restore(self):
        self.mutation(v.MC, 'ConnObj', 'new SqlConnection(connstr)', 'new SqlConnection(originalConnStr)', 'global-factory-and-single-shared-backup')

    def test_customer_loader_type_is_checked_in_actual_purchase_owner(self):
        self.mutation(v.PURCH, 'LoadCustomers', 'int type = 2;', 'int type = 1;', 'actual-party-loaders-counterexample')

    def test_actual_modern_purchase_call_literal_two_not_blanket_one(self):
        self.mutation(v.PURCH, 'ItemClientActivity', 'GetSelectedId(this.cmbClient), 2)', 'GetSelectedId(this.cmbClient), 1)', 'exact-current-call-arguments:R6NEXT-017')

    def test_legacy_purchase_literal_one_is_not_silently_corrected(self):
        self.mutation(v.OLDPURCH, 'StripClientLastActivity_Click', 'LastProcess(itemId, storeId, custId, 1)',
                      'LastProcess(itemId, storeId, custId, 2)', 'exact-current-call-arguments:R6NEXT-029')

    def test_legacy_customer_request_still_omits_party(self):
        self.mutation(v.OLDIO, 'StripLastItem_Click', 'LastProcess(row.ItemId, row.StoreId, -1, 1)',
                      'LastProcess(row.ItemId, row.StoreId, 7, 1)', 'exact-current-call-arguments:R6NEXT-008')

    def test_legacy_menu_intent_cannot_be_inferred_from_handler_name(self):
        rel = v.OLDIO[:-3]
        self.rejected(self.changed_xml(rel, 'Click="StripLastItem_Click"', 'Click="StripClientLastItem_Click"'), 'legacy-menu-purpose-from-XAML')

    def test_local_purchase_reflection_contract_is_not_opaque_external_DTO(self):
        self.mutation(v.OLDPURCH, 'GetRowCellValue', 'GetProperty(column)?.GetValue(row)',
                      'GetField(column)?.GetValue(row)', 'selected-row-and-reflection-antecedents')

    def test_legacy_purchase_line_producer_uses_proc_id_not_global_key(self):
        self.mutation(v.OLDPURCH, 'ReadData', 'Inv_Sub where proc_id={ProcCode}',
                      'Inv_Sub where InvGlobalID={ProcCode}', 'purchase-string-row-producers')

    def test_local_sale_purchase_store_fallback_one_is_not_other_forms_zero(self):
        self.mutation(v.OLDSALE, 'GetStoreId', 'return 1;', 'return 0;', 'legacy-store-fallbacks-one-versus-zero')

    def test_contract_menu_has_actual_CS_subscription(self):
        self.mutation(v.CONTRACT, 'SetupGridEvents', 'tableView.ShowGridMenu += GridView1_ShowGridMenu;', '', 'dynamic-menu-written-wiring')

    def test_transfer_safe_integer_conversion_fallback_is_not_positive_identity(self):
        self.mutation(v.TRANS, 'SafeInt', 'int.TryParse(v.ToString(), out int r) ? r : d',
                      'int.TryParse(v.ToString(), out int r) ? r : 1', 'conversion-fallbacks-differ')

    def test_reopen_queries_do_not_acquire_branch_without_new_assessment(self):
        self.mutation(v.DET, 'OpenInvoiceByType', 'AND inv_type=2 AND proc_type=1 AND id={invNo}',
                      'AND branch=1 AND inv_type=2 AND proc_type=1 AND id={invNo}', 'local-number-and-missing-branch-origin')

    def test_reopen_alias_case_cannot_disappear_in_count_only_extractor(self):
        self.mutation(v.DET, 'OpenInvoiceByType', 'case "مرتجع مبيعات":', '// removed alias', 'all16-literal-case-labels')

    def test_reopen_configure_before_show_is_written_order_only(self):
        self.mutation(v.DET, 'OpenForm',
                      'configure(form);\n            form.WindowState = WindowState.Maximized;\n            form.Show();',
                      'form.WindowState = WindowState.Maximized;\n            form.Show();\n            configure(form);',
                      'configure-before-show-not-Loaded-order-proof')

    def test_activity_local_row_cannot_gain_invented_origin_fields(self):
        result = copy.deepcopy(self.facts)
        row = result['text_ranges']['activity-result-row-class']
        self.assertIn('public string DgvInvType', row['text'])
        row['text'] = row['text'].replace('public string DgvInvType', 'public string BranchId; public string DgvInvType', 1)
        self.rejected(result, 'local-result-class-does-not-invent-document-ref-fields')

    def test_linked_helper_is_void_ref_not_typed_acceptance(self):
        self.mutation(v.IP, 'InsertFromInv', 'public static void InsertFromInv', 'public static bool InsertFromInv', 'void-ref-helper-signature')

    def test_linked_first_picker_guard_is_not_any_truthy_key(self):
        self.mutation(v.IP, 'InsertFromInv', 'frmInvoiceSrch2.ISDone & (Operators.CompareString',
                      'frmInvoiceSrch2.ISDone | (Operators.CompareString', 'first-picker-guard-ref-load')

    def test_ordinary_child_receives_current_ref_model_before_acceptance(self):
        self.mutation(v.IP, 'InsertFromInv', 'frmInvoiceItems2.inv = Invo;', '', 'ordinary-conditional-rebind-versus-empty-contract')

    def test_success_only_ordinary_rebind_is_not_rollback_on_cancel(self):
        self.mutation(v.IP, 'InsertFromInv', 'if (frmInvoiceItems2.ISDone)', 'if (!frmInvoiceItems2.ISDone)', 'ordinary-conditional-rebind-versus-empty-contract')

    def test_contract_result_branch_has_no_transfer(self):
        self.mutation(v.IPC, 'InsertFromInv', 'if (!frmInvoiceItems2.ISDone)',
                      'if (!frmInvoiceItems2.ISDone) Invo = frmInvoiceItems2.invcontract;\n                if (!frmInvoiceItems2.ISDone)', 'ordinary-conditional-rebind-versus-empty-contract')

    def test_contract_selection_query_does_not_redirect_inv_writer(self):
        self.mutation(v.ITEMS, 'InsertSelectedItems', 'inv.InvoiceItems', 'invcontract.InvoiceItems', 'contract-query-does-not-redirect-selected-item-writer-target')

    def test_selected_line_matching_is_item_id_not_RowNo(self):
        self.mutation(v.ITEMS, 'InsertSelectedItems', 'invoiceItem.ItemId == selectedRow.Item_ID',
                      'invoiceItem.ItemId == selectedRow.RowNo', 'contract-query-does-not-redirect-selected-item-writer-target')

    def test_selected_line_removal_uses_item_id_set(self):
        self.mutation(v.ITEMS, 'RemoveNonSelectedItems', 'selectedRows.Select(r => r.Item_ID).ToHashSet()',
                      'selectedRows.Select(r => r.RowNo).ToHashSet()', 'selection-identity-is-ItemId')

    def test_child_cancel_replaces_child_field_not_ref_parent_snapshot(self):
        self.mutation(v.ITEMS, 'CloseWithoutResult', 'invcontract = new Invoicecontract();',
                      'invcontract = null;', 'different-item-exits-not-rollback')

    def test_insert_all_only_acceptance_and_year_flag_are_recorded(self):
        self.mutation(v.ITEMS, 'btnAddall_Click', 'MainClass.ReturnYearPreviews = false;', '', 'different-item-exits-not-rollback')

    def test_selected_button_does_not_clear_year_flag_like_all_button(self):
        self.mutation(v.ITEMS, 'btnadd_Click', 'InsertSelectedItems();',
                      'InsertSelectedItems();\n            MainClass.ReturnYearPreviews = false;', 'different-item-exits-not-rollback')

    def test_search_escape_does_not_invent_button_restore(self):
        self.mutation(v.SEARCH, 'Window_KeyDown', 'else if (e.Key == Key.Escape) Close();',
                      'else if (e.Key == Key.Escape) { MainClass.connstr = MainClass.originalConnStr; Close(); }', 'search-close-button-versus-escape')

    def test_purchase_void_new_guard_does_not_propagate_to_outer(self):
        self.mutation(v.PURCH, 'btnNew_Click', 'if (!this.CheckBeforeClear())', 'if (true)', 'purchase-new-callee-No-is-not-propagated')

    def test_POS_password_check_occurs_after_clear_in_source(self):
        original = v.method(self.facts, v.POS, 'RetSales_Click')['syntax_text']
        old = 'CLR();'; self.assertEqual(original.count(old), 1)
        modified = self.changed_method(v.POS, 'RetSales_Click', old, '')
        # Put the same actual CLR invocation after the actual password guard,
        # reparse the modified source rather than editing AST call positions.
        text = v.base.decode((v.ROOT / v.POS).read_bytes())
        member = v.method(modified, v.POS, 'RetSales_Click')['syntax_text']
        changed = member.replace('if (!pwdFrm.Iscorrect) return;', 'if (!pwdFrm.Iscorrect) return;\n            CLR();')
        text = text.replace(original, changed, 1)
        modified['methods'][v.POS]['RetSales_Click'] = v.source_methods(text, ['RetSales_Click'])['RetSales_Click']
        self.rejected(modified, 'linked-parent-preclear-and-POS-password-sequence')

    def test_IO_linked_preclear_not_hidden_by_guard_elsewhere(self):
        self.mutation(v.IO, 'btnInsertLinkedInv_Click', 'CLR();', '', 'linked-parent-preclear-and-POS-password-sequence')

    def test_parent_does_not_receive_helper_ISDone(self):
        self.mutation(v.POS, 'InsertFromInv', 'Invoic.ISNew = true;',
                      'if (ISDone) Invoic.ISNew = true;', 'parent-no-shared-helper-acceptance-result')

    def test_sales_previous_year_switch_uses_one_shared_backup(self):
        self.mutation(v.SALE, 'InsertLinkedReturn', 'MainClass.originalConnStr = MainClass.connstr;', '', 'linked-previous-year-switch-without-caller-finally')

    def test_central_binder_null_on_empty_or_outer_failure_is_not_health(self):
        self.mutation(v.IP, 'BindingInvoice', 'Invo = null;', '', 'binder-writes-current-ref-null-or-row-skips', count=2)

    def test_central_binder_does_not_clear_item_collection_before_add(self):
        self.mutation(v.IP, 'BindingInvoice', 'Invo.InvoiceItems.Add(Itm);',
                      'Invo.InvoiceItems.Clear(); Invo.InvoiceItems.Add(Itm);', 'binder-writes-current-ref-null-or-row-skips')

    def test_central_binder_per_row_swallow_is_recorded_not_assumed_complete(self):
        self.mutation(v.IP, 'BindingInvoice', 'ProjectData.SetProjectError(projectError4);',
                      'ProjectData.SetProjectError(projectError4); throw;', 'binder-writes-current-ref-null-or-row-skips')

    def test_picker_type20_union_is_existing_root_not_request_type_enforcement(self):
        self.mutation(v.SEARCH, 'BuildLoadQuery', 'inv_type = 20 OR', 'inv_type = 21 OR', 'selector-eligibility-keeps-existing155-and157')

    def test_generic_permission_missing_rows_is_not_automatic_deny(self):
        self.mutation(v.MC, 'ApplyPermissionToForm@System.Windows.Window', 'if (dt.Rows.Count == 0) return;', '', 'generic-button-permissions-not-document-allowed-set')

    def test_same_count_but_changed_original_call_dictionary_rejected(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['last_process_calls'][0]['original_R6_call_row'].update(line=1), 'exact-carried-original-rows')

    def test_dropped_linked_call_rejected(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['linked_insert_calls'].pop(), 'exact-carried-original-rows:linked-insert')

    def test_current_call_hash_not_only_old_identity_rejected_when_changed(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['last_process_calls'][0]['current_source_site'].update(argument_utf8_sha256='bad'), 'per-call-context-and-qualification')

    def test_antecedent_source_hash_tamper_rejected(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['last_process_calls'][0]['antecedent_source_basis'][0].update(syntax_utf8_sha256='bad'), 'basis:method')

    def test_argument_trace_cannot_be_only_four_int_spelling(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['last_process_calls'][0].update(source_to_argument_trace={}), 'individual-input-filter-scope')

    def test_one_call_cannot_omit_connection_year_decision(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['last_process_calls'][0].update(connection_year_disposition=''), 'per-call-context-and-qualification')

    def test_linked_path_cannot_omit_second_picker_cancel(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['linked_insert_calls'][0]['path_dispositions'].pop('SecondPickerCancelled'), 'individual-parent-cancel-accept-health')

    def test_void_helper_cannot_be_relabelled_typed_acceptance(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['linked_insert_calls'][0].update(explicit_typed_acceptance_result_returned=True), 'individual-parent-cancel-accept-health')

    def test_audit_outcomes_cannot_be_relabelled_CSharp_results(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['shared_receiver_contract'].update(outcome_labels_are_audit_categories_not_CSharp_return_types=False), 'shared-void-outcome-contract')

    def test_reopen_carried_core_hash_cannot_be_called_fresh_R8_read(self):
        def change(j):
            contexts = j['report_reopen_routes'][0]['carried_R7_core_contexts']
            contexts[next(iter(contexts))]['syntax_utf8_sha256'] = 'bad'
        self.evidence_rejected(v.MATRIX, change, 'exact-carried-R7-core-not-fresh-R8-read')

    def test_reopen_cannot_certify_whole_Save_edit_or_allowed_set(self):
        self.evidence_rejected(v.MATRIX, lambda j: j['report_reopen_routes'][0].update(whole_receiver_Save_allowed_edit_or_document_set_certified=True), 'qualified-reopen-route')

    def test_six_capability_progress_cannot_be_promoted_to_exit(self):
        self.evidence_rejected(v.REVIEW, lambda j: j['capabilities']['CAP7B38-D17'].update(whole_capability_certified=True), 'named-capability-open-obligations')

    def test_source_decision_cannot_become_observed_ERP_failure(self):
        self.evidence_rejected(v.REVIEW, lambda j: j['source_decisions'][0].update(observed_in_ERP=True), 'qualified-decision')

    def test_existing_potential132_cannot_be_promoted_from_statement_order(self):
        def change(j):
            next(r for r in j['candidate_dispositions'] if r['id'] == 'R8C-LIFECYCLE')['prior_certainty_preserved'] = 'confirmed'
        self.evidence_rejected(v.ROOTS, change, '132-not-promoted')

    def test_original_root_dictionary_cannot_be_rewritten(self):
        self.evidence_rejected(v.ROOTS, lambda j: j['focused_root_reviews']['P7-059']['canonical_prior_row'].update(status='fixed'), 'canonical-root-unchanged')

    def test_missing_six_dictionaries_cannot_be_invented_from_narrative(self):
        self.evidence_rejected(v.ROOTS, lambda j: j.update(missing_six_dictionaries_reconstructed=True), 'no-invented-root-novelty')

    def test_original_R6_read_flags_cannot_be_rewritten(self):
        self.evidence_rejected(v.WORK, lambda j: j.update(original_R6_discovery_or_read_flags_rewritten=True), 'all37-ancestry')

    def test_readable_local_work_cannot_be_replaced_with_external_handoff(self):
        self.evidence_rejected(v.WORK, lambda j: j['remaining_readable_local_tasks'][0].update(externalized=True), 'remaining-local-owner')

    def test_unavailable_model_contract_not_accepted_as_completion(self):
        self.evidence_rejected(v.REVIEW, lambda j: j['unavailable_contracts_not_accepted_as_handoffs'][0].update(accepted_external_handoff=True), 'owned-unavailable-contract')

    def test_requested_label_is_not_current_date_authentication(self):
        self.evidence_rejected(v.DATE_NOTE, lambda j: j.update(requested_label_is_claim_about_today=True), 'prospective-reference-label-not-today')

    def test_recorded_range_hash_does_not_survive_tamper(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'][0]['decoded_range_utf8_sha256'] = 'bad'
        self.assertTrue(any('read:range-identity:' in e for e in v.prior.read_errors(reads, self.facts)))

    def test_recorded_coverage_does_not_prove_independent_human_reading(self):
        reads = copy.deepcopy(self.reads)
        reads['independent_human_review_claimed'] = True
        self.assertTrue(any('no-extraction-or-invented-human' in e for e in v.prior.read_errors(reads, self.facts)))


if __name__ == '__main__':
    unittest.main()
