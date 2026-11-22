#!/usr/bin/env python3
"""R9 bounded source/evidence regression and mutation tests, never ERP tests.

Mutate the supplied original C#/XAML/query syntax in memory, or isolated audit
JSON copies. Rejection invalidates an audit assertion; it is not an application
fix. No application construction, SQL, WPF, SDK, provider or business math runs.
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

import verify_save_edit as v


class SaveEditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)
        cls.reads = v.load(v.READS)

    def changed_method(self, rel, selector, old, new, count=1):
        text = v.base.decode((v.ROOT / rel).read_bytes())
        member = v.method(self.facts, rel, selector)['syntax_text']
        if '\r\n' in member:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        self.assertEqual(member.count(old), count, 'Use actual supplied source, not a synthetic ERP implementation')
        self.assertEqual(text.count(member), 1)
        changed = text.replace(member, member.replace(old, new), 1)
        result = copy.deepcopy(self.facts)
        result['methods'][rel][selector] = v.source_methods(changed, [selector])[selector]
        if rel in v.EDITORS:
            result['literal_command_sites'] = [r for r in result['literal_command_sites'] if r['path'] != rel] + v.command_sites(changed, rel)
            result['permission_flag_writes'] = [r for r in result['permission_flag_writes'] if r['path'] != rel] + v.permission_writes(changed, rel)
        if rel in (v.IP, v.IPC) and selector == 'SaveInvoice':
            result['header_parameter_bridges'] = v.header_parameter_bridges(result)
        return result

    def rejected(self, result, guard):
        errors = v.source_errors(result)
        self.assertTrue(any(guard in e for e in errors), (guard, errors))

    def mutation(self, rel, selector, old, new, guard, count=1):
        self.rejected(self.changed_method(rel, selector, old, new, count), guard)

    def bad_evidence(self, name, change):
        with tempfile.TemporaryDirectory(prefix='smartaudit-r9-audit-json-') as tmp:
            ev = Path(tmp)
            for n in v.PACKET: shutil.copyfile(v.EV / n, ev / n)
            obj = json.loads((ev / name).read_bytes()); change(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev)

    def test_actual_selected_facts_rederive_from_supplied_sources(self):
        self.assertEqual(v.derive(), self.facts)

    def test_recorded_source_assertions_consistent_not_an_ERP_run(self):
        self.assertEqual(v.source_errors(self.facts), [])
        self.assertEqual(self.facts['application_execution_count'], 0)

    def test_all_selected_context_ranges_covered_not_reading_or_calendar_proof(self):
        self.assertEqual(v.read_errors(self.reads, self.facts), [])
        self.assertFalse(self.reads['extraction_equals_reading'])
        self.assertFalse(self.reads['independent_human_review_claimed'])
        self.assertFalse(self.reads['individual_read_timestamps_invented'])
        self.assertFalse(self.reads['raw_stdout_preserved'])

    def test_published1604_audit_inputs_and827_application_sources_preserved(self):
        self.assertEqual(v.preservation_errors(v.load(v.ENTRY)), [])

    def test_entry_base_mismatch_is_not_accepted_as_same_branch_provenance(self):
        entry = copy.deepcopy(v.load(v.ENTRY)); entry['HEAD'] = 'not-the-published-R8-head'
        self.assertIn('preservation:published-R8-entry', v.preservation_errors(entry))

    def test_changed_prior_audit_expected_bytes_rejected(self):
        entry = copy.deepcopy(v.load(v.ENTRY)); rel = 'docs/audit/findings.csv'
        entry['preserved_tracked_audit_inputs'][rel]['bytes'] += 1
        self.assertIn('preservation:prior-audit:' + rel, v.preservation_errors(entry))

    def test_application_inventory_not_replaced_by_new_claim(self):
        entry = copy.deepcopy(v.load(v.ENTRY)); entry['application_sources'].pop(next(iter(entry['application_sources'])))
        self.assertIn('preservation:entry-inventory', v.preservation_errors(entry))

    def test_individual_command_opener_root_decisions_and_pins_consistent(self):
        self.assertEqual(v.evidence_errors(), [])

    def test_open_completion_gate_returns_two_not_capability_exit(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out): code = v.main(['--verify', '--require-complete'])
        result = json.loads(out.getvalue())
        self.assertEqual(code, 2); self.assertEqual(result['errors'], [])
        self.assertFalse(result['whole_7B_static_assessment_complete'])
        self.assertEqual(result['capability_exit_certificates_issued'], 0)
        self.assertEqual(result['four_family_exit_certificates_issued'], 0)

    def test_selected23_commands_are_not_literal35_call_count_certificates(self):
        matrix = v.load(v.MATRIX)
        self.assertEqual([(r['path'], r['entry_selector']) for r in matrix['command_reviews']],
            [(rel, s) for rel, names in v.COMMAND_OWNERS.items() for s in names])
        self.assertEqual(matrix['literal_command_sites'], self.facts['literal_command_sites'])
        self.assertTrue(all(not r['whole_route_or_capability_certified'] for r in matrix['command_reviews']))

    def test_selected26_opener_owners_are_not26_capability_assessments(self):
        matrix = v.load(v.MATRIX)
        self.assertEqual(len(matrix['alternate_opener_reviews']), 26)
        self.assertEqual(len(self.facts['selected_alternate_editor_creations']), 31)
        self.assertTrue(all(not r['all_ingress_or_runtime_schedule_certified'] for r in matrix['alternate_opener_reviews']))
        self.assertEqual(set(v.load(v.REVIEW)['capabilities']), set(v.TARGETS))
        self.assertFalse(v.load(v.REVIEW)['all26_capabilities_freshly_semantically_reviewed'])

    def test_five_capability_canonical_rows_preserved_without_exit(self):
        rows = {r['id']: r for r in v.base.rows('capability-register-07B38.csv')}
        for cid, row in v.load(v.REVIEW)['capabilities'].items():
            self.assertEqual(row['canonical_capability_row'], rows[cid])
            self.assertFalse(row['whole_capability_certified'])
            self.assertFalse(row['local_semantic_obligations_complete'])
            self.assertFalse(row['readable_local_externalized'])
            self.assertTrue(row['remaining_readable_local'])

    def test_original37_R6_rows_and_R8_tasks_not_rewritten_or_externalized(self):
        work = v.load(v.WORK)
        self.assertEqual(work['original37_R6_rows_verbatim'], v.load(v.previous.OLD_WORK)['calls'])
        self.assertEqual(work['preserved_R8_local_task_rows_verbatim'], v.load(v.previous.WORK)['remaining_readable_local_tasks'])
        self.assertFalse(work['original_R6_read_flags_rewritten'])
        self.assertFalse(work['entire_R8LOCAL_SAVE_EDIT_marked_complete'])
        self.assertTrue(all(not r['externalized'] for r in work['remaining_readable_local_tasks']))

    def test_contract_alleged_missing_four_parameters_refuted_not_numbered(self):
        bridges = self.facts['header_parameter_bridges']
        for key in ('InsertInvcontract', 'UpdateInvcontract'):
            row = bridges[key]
            self.assertEqual(row['whitespace_trimmed_missing_placeholders'], [])
            self.assertTrue({'@QRCode', '@InvoiceHash', '@UUID', '@ZatcaSent'} <= set(row['raw_supplied_parameter_names']))
            self.assertEqual(len(row['raw_supplied_parameter_names']), 62)
            self.assertFalse(row['provider_binding_or_all_parameter_health_certified'])
        root = next(r for r in v.load(v.ROOTS)['candidate_dispositions'] if r['id'] == 'R9C-CONTRACT-PARAMETERS')
        self.assertEqual(root['disposition'], 'rejected-alleged-missing-four-tax-parameters')
        self.assertIsNone(root['root_id']); self.assertFalse(root['novelty_certified'])

    def test_raw_trailing_parameter_names_preserved_not_provider_normalized(self):
        row = self.facts['header_parameter_bridges']['InsertInvcontract']
        self.assertIn('@Reff_No ', row['raw_supplied_parameter_names'])
        self.assertNotIn('@Reff_No', row['raw_supplied_parameter_names'])
        self.assertFalse(row['provider_binding_or_all_parameter_health_certified'])

    def test_cache_is_DataTable_not_persisted_SQL_stock(self):
        f = v.method(self.facts, v.STOCK, 'UpdateItemStock')
        self.assertIn('rows[0]["Stock"] = currentStock', f['syntax_text'])
        self.assertFalse(any(c['function'].endswith('ExecuteNonQuery') for c in f['calls']))
        self.assertTrue(f['catches'])

    def test_purchase_null_entry_guard_and_POS_stock_guard_are_counterexamples(self):
        self.assertIn('if (entry == null) return;', v.method(self.facts, v.PURCH, 'SaveAndPrint')['syntax_text'])
        pos = v.method(self.facts, v.POS, 'SaveAndPrint')
        guard_line = next(r['line'] for r in pos['conditions'] if v.norm(r['text']) == '!saved')
        self.assertGreater(v.calls(pos, 'Inventory.UpdateItemStock')[0]['line'], guard_line)
        self.assertFalse(v.load(v.REVIEW)['whole_7B_static_assessment_complete'])

    def test_focused23_rows_not_all339_semantic_or_missing345_recertification(self):
        roots = v.load(v.ROOTS)
        self.assertEqual(len(roots['available_prior_rows']), 339)
        self.assertEqual(set(roots['focused_root_reviews']), set(v.FOCUSED))
        self.assertFalse(roots['all339_semantically_reread_in_R9'])
        self.assertFalse(roots['all345_roots_screened'])
        self.assertFalse(roots['missing_six_dictionaries_reconstructed'])
        self.assertEqual(roots['new_finding_ids'], [])

    def test_prior_potential_certainties_not_upgraded_by_current_source_order(self):
        roots = v.load(v.ROOTS)
        for rid in ('P4-014', 'P7-132'):
            self.assertEqual(roots['focused_root_reviews'][rid]['canonical_prior_row']['certainty'], 'potential')
        self.assertFalse(roots['historical_root_fields_rewritten'])

    def test_new16Nov_reference_not_frozen21Nov_or_condensed22Nov_authority(self):
        note = v.load(v.DATE_NOTE)
        self.assertEqual(note['assessment_reference_date_utc'], '2026-11-16')
        self.assertEqual(v.load(v.REVIEW)['assessment_reference_date_utc'], '2026-11-16')
        self.assertEqual(v.load(v.ENTRY)['assessment_reference_date_utc'], '2026-11-21')
        self.assertFalse(note['user_requested_reference_date_authenticated'])
        self.assertFalse(note['historical_tests_relabelled_as_current'])
        self.assertFalse(note['raw_clocks_are_calendar_authority'])

    def test_unavailable_contracts_not_accepted_before_readable_local_followthrough(self):
        review = v.load(v.REVIEW)
        self.assertTrue(all(not r['accepted_external_handoff'] and r['readable_local_not_delegated']
                            for r in review['unavailable_contracts_not_accepted_as_handoffs']))
        self.assertFalse(review['phase7C_started']); self.assertFalse(review['phase8_authorized'])

    def test_read_coverage_gap_rejects_extraction_as_a_complete_source_read(self):
        reads = copy.deepcopy(self.reads); reads['reads'] = [r for r in reads['reads'] if r['path'] != v.IPC]
        self.assertTrue(any('read:uncovered:' + v.IPC in e for e in v.read_errors(reads, self.facts)))

    def test_read_range_hash_mutation_rejected(self):
        reads = copy.deepcopy(self.reads); reads['reads'][0]['decoded_range_utf8_sha256'] = 'changed'
        self.assertTrue(any('read:range-identity' in e for e in v.read_errors(reads, self.facts)))

    def test_invented_read_timestamps_are_not_allowed_as_reading_proof(self):
        reads = copy.deepcopy(self.reads); reads['individual_read_timestamps_invented'] = True
        self.assertIn('read:no-extraction-or-invented-chronology-as-reading-proof', v.read_errors(reads, self.facts))

    def test_real_XAML_KeyDown_subscription_removal_invalidates_duplicate_wiring_assertion(self):
        rel = v.SALE[:-3]; text = v.base.decode((v.ROOT / rel).read_bytes())
        self.assertEqual(text.count('KeyDown="Window_KeyDown"'), 1)
        result = copy.deepcopy(self.facts)
        result['xml_elements'][rel] = v.previous.xml_elements(text.replace('KeyDown="Window_KeyDown"', '', 1), v.XML_SELECTED[rel])
        self.rejected(result, 'sale-F6-bypasses-button-wrapper-and-has-duplicate-written-wiring')

    def test_actual_UpdateInv_where_branch_mutation_invalidates_key_only_assertion(self):
        text = v.base.decode((v.ROOT / v.SQ).read_bytes())
        row = self.facts['sql_fields']['UpdateInv']; literal = row['csharp_literal']
        self.assertEqual(text.count(literal), 1)
        changed = json.dumps(row['sql_text'] + ' AND branch=@branch', ensure_ascii=False)
        result = copy.deepcopy(self.facts); result['sql_fields'] = v.query_fields(text.replace(literal, changed, 1))
        self.rejected(result, 'update-key-only-no-origin-branch-year-allowed-set:UpdateInv')


# Each mutation below exercises a separate source assertion against an actual
# selected original body. Separate named unittest cases are captured verbosely.
SOURCE_MUTATIONS = [
    ('period_true_disjunction', v.COMMON, 'CheckProiedAcc', '|| true', '|| false', 'period-helper-all-written-returns-allow'),
    ('allow_edit_sql_default', v.COMMON, 'AllowEdit', 'ISNULL(IS_Edit,1)', 'ISNULL(IS_Edit,0)', 'allow-edit-missing-error-default-true'),
    ('form_permission_default_edit', v.FP, 'ctor:FormPermission', 'Editable = true;', 'Editable = false;', 'form-permission-default-and-caught-query'),
    ('form_permission_empty_retains', v.FP, 'ApplyFrmPermissionInternal', 'permissionTable.Rows.Count <= 0', 'permissionTable.Rows.Count < 0', 'form-permission-default-and-caught-query'),
    ('form_permission_hold_classifier', v.FP, 'IsSavePermissionButton', '"btnHoldOrd"', '"anotherButton"', 'different-UI-button-classifiers'),
    ('common_add_new_condition', v.COMMON, 'ApplyEditAddPermissionInternal', '!frmPer.Addable && IsNew', '!frmPer.Addable && !IsNew', 'different-UI-button-classifiers'),
    ('global_factory_captured_year', v.MC, 'ConnObj', 'new SqlConnection(connstr)', 'new SqlConnection(originalConnStr)', 'global-connection-and-settings'),
    ('missing_UI_permission_row', v.MC, 'ApplyPermissionToForm@System.Windows.Window', 'dt.Rows.Count == 0', 'dt.Rows.Count < 0', 'global-connection-and-settings'),
    ('contract_role_default', v.CONTRACT, 'ctor:frmcontract', 'allowEditInvoice = true;', 'allowEditInvoice = false;', 'contract-local-role-flag-only-constructor-true'),
    ('contract_electronic_loaded_setting', v.CONTRACT, 'LoadFoundation', 'SELECT EnableE_Invoice FROM Foundation', 'SELECT 0 AS EnableE_Invoice FROM Foundation', 'contract-electronic-policy-is-separate-loaded-setting'),
    ('POS_loaded_form_permission_key', v.POS, 'Window_Loaded', 'Common.AllowEdit("frmInvPOS")', 'Common.AllowEdit("frmInvSale")', 'POS-and-sale-conditional-form-lookups'),
    ('sale_loaded_return_permission_key', v.SALE, 'Window_Loaded', 'Common.AllowEdit("frmSalePurch5")', 'Common.AllowEdit("wrongReturn")', 'POS-and-sale-conditional-form-lookups', 2),
    ('IO_positive_net', v.IO, 'btnSave_Click', 'netVal <= 0 && InvType != 9', 'netVal < 0 && InvType != 9', 'IO-distinct-save-print-public-pay-keyboard'),
    ('IO_same_return_key', v.IO, 'btnSavePrint_Click', 'Invoic.InvGlobalID, Invoic.InvGlobalID', 'Invoic.InvGlobalID, Invoic.ReffNo', 'IO-distinct-save-print-public-pay-keyboard'),
    ('IO_direct_F6', v.IO, 'OnKeyDown', 'btnSave_Click(null, null);', 'btnSavePrint_Click(null, null);', 'IO-distinct-save-print-public-pay-keyboard'),
    ('purchase_reference_warning', v.PURCH, 'btnSave_Click', 'Common.CheckReffNo(', 'Common.OtherReferenceCheck(', 'purchase-validation-parity-actual-counterchecks'),
    ('purchase_print_empty_guard', v.PURCH, 'btnSavePrint_Click', '_invoiceItems.Count == 0 || this.Invoic.Net == 0.0', '_invoiceItems.Count < 0 || this.Invoic.Net == 0.0', 'purchase-validation-parity-actual-counterchecks'),
    ('purchase_print_quantity_guard', v.PURCH, 'btnSavePrint_Click', 'item.ItemQuantity <= 0', 'item.ItemQuantity < 0', 'purchase-validation-parity-actual-counterchecks'),
    ('POS_Paid_status_guard', v.POS, 'btnPay_Click', 'Invoic.PaymentStatus == PaymentStatus.Paid', 'Invoic.PaymentStatus != PaymentStatus.Paid', 'POS-pay-guards-have-specific-status', 2),
    ('POS_public_pay_result', v.POS, 'PayBill', 'if (!InvoiceOper.PayInvoice(ref Invoic, InvObj))', 'if (InvoiceOper.PayInvoice(ref Invoic, InvObj))', 'POS-pay-guards-have-specific-status'),
    ('POS_hold_proc_type', v.POS, 'btnHoldOrd_Click', 'Invoic.ProcType = 3;', 'Invoic.ProcType = 1;', 'POS-hold-is-distinct-command'),
    ('POS_hold_publication_number', v.POS, 'btnHoldOrd_Click', 'HoldList[i] = Invoic.InvoiceNo;', 'HoldList[i] = 0;', 'POS-hold-is-distinct-command'),
    ('POS_new_date_overwrite', v.POS, 'SaveAndPrint', 'invoice.InvDate = DateTime.Now;', 'invoice.InvDate = invoice.InvDate;', 'POS-current-date-overwrite-before-writer', 2),
    ('POS_table_write_call', v.POS, 'SaveAndPrint', 'updat_table(', 'another_table(', 'POS-table-writes-and-print-call-precede-false-return', 2),
    ('POS_table_print_call', v.POS, 'SaveAndPrint', 'RptPrint_Tables(', 'another_print(', 'POS-table-writes-and-print-call-precede-false-return'),
    ('sale_constructor_keyboard_wiring', v.SALE, 'ctor:frmInvSale', 'KeyDown += Window_KeyDown;', 'KeyDown -= Window_KeyDown;', 'sale-F6-bypasses-button-wrapper'),
    ('sale_keyboard_validator', v.SALE, 'Window_KeyDown', 'ValidateInvoice();', 'btnSave_Click(null, null);', 'sale-F6-bypasses-button-wrapper'),
    ('sale_zero_quantity', v.SALE, 'ValidateInvoice', 'item.ItemQuantity <= 0', 'item.ItemQuantity < 0', 'sale-validation-and-edit-exception'),
    ('sale_save_edit_exception', v.SALE, 'SaveAndPrint', '!(InvObj.PaymentStatus && !Invoic.IsUpdated)', '!(InvObj.PaymentStatus && Invoic.IsUpdated)', 'sale-validation-and-edit-exception'),
    ('sale_quotation_proc_type', v.SALE, 'btnSaveQuotation_Click', 'Invoic.ProcType = 4;', 'Invoic.ProcType = 1;', 'sale-quotation-clear-and-repaid'),
    ('sale_quotation_clear', v.SALE, 'btnSaveQuotation_Click', 'CLR();', 'RefreshGrid();', 'sale-quotation-clear-and-repaid'),
    ('contract_print_flag_not_call', v.CONTRACT, 'SaveAndPrint', 'if (saved && Invoic.IsPrinted && print.PrintNo > 0)', 'if (saved && Invoic.IsPrinted && print.PrintNo >= 0)', 'contract-field-guard-and-print-flag'),
    ('contract_code_click_wiring', v.CONTRACT, 'SetupButtonEvents', 'btnSavePrint.Click += btnSavePrint_Click;', 'btnSavePrint.Click -= btnSavePrint_Click;', 'contract-code-wiring-not-duplicate-click-assumption'),
    ('transfer_save_dispatch', v.TRANS, 'btnSave_Click', 'if (_invoic.ProcType == 1)', 'if (_invoic.ProcType == 2)', 'transfer-save-print-route-difference'),
    ('transfer_print_receive_dispatch', v.TRANS, 'btnSavePrint_Click', 'SaveReceive();', 'SaveSend();', 'transfer-save-print-route-difference'),
    ('transfer_send_new_flag', v.TRANS, 'SaveSend', '_invoic.ISNew = true;', '_invoic.ISNew = false;', 'transfer-two-void-calls-no-shared-success'),
    ('transfer_send_success_dialog', v.TRANS, 'SaveSend', 'savedMsg.ShowDialog();', 'savedMsg.Close();', 'transfer-two-void-calls-no-shared-success'),
    ('cache_First_item_key', v.STOCK, 'UpdateItemStock', 'itemId = {item.ItemNo}', 'itemId = {item.Store}', 'cache-helper-is-loaded-DataTable'),
    ('cache_add_delta', v.STOCK, 'UpdateItemStock', 'currentStock + item.PrimaryQnty', 'currentStock - item.PrimaryQnty', 'cache-helper-is-loaded-DataTable'),
    ('purchase_null_entry_counterexample', v.PURCH, 'SaveAndPrint', 'if (entry == null) return;', 'if (entry == null) { }', 'purchase-null-entry-return-counterexample'),
    ('ordinary_writer_employee_check', v.IP, 'SaveInvoice', 'MainClass.EmpNo < 1', 'MainClass.EmpNo < 0', 'writer-invariants-and-null-entry-commit'),
    ('contract_writer_null_entry', v.IPC, 'SaveInvoice', 'if (Entr == null)', 'if (Entr != null)', 'writer-invariants-and-null-entry-commit'),
    ('entry_own_connection', v.EO, 'SaveEnty', 'using SqlConnection conn = MainClass.ConnObj();', 'using SqlConnection conn = suppliedConnection;', 'entry-has-own-commit'),
    ('entry_own_commit', v.EO, 'SaveEnty', 'transaction.Commit();', 'transaction.Rollback();', 'entry-has-own-commit'),
    ('transfer_store_branch_fallback', v.COMMON, 'GetInventoryBranch', 'return 1;', 'return -1;', 'transfer-mapped-branch-fallback-one'),
    ('mapping_collection_assignment', v.IP, 'MappingInvoice', 'invoice.InvoiceItems = Inv.InvoiceItems;', 'invoice.InvoiceItems = null;', 'mapping-is-stateful-but-VerifyIsNewInvoice'),
    ('mapping_VerifyIsNew_never_true', v.IP, 'VerifyIsNewInvoice', 'result = false;', 'result = true;', 'mapping-is-stateful-but-VerifyIsNewInvoice', 2),
    ('contract_mapping_amount', v.IPC, 'MappingInvoicecontract', 'invoice.contract_total_value = Inv.contract_total_value;', 'invoice.contract_total_value = 0;', 'local-composite-helper-is-readable-state-writer'),
    ('ordinary_composite_append', v.IP, 'BindingCompositeItems', 'list.Add(invoiceItem);', 'list.Clear();', 'local-composite-helper-is-readable-state-writer'),
    ('ordinary_tax_send', v.IP, 'SaveInvoice', 'this.SendZatca(inv);', 'this.OtherSend(inv);', 'tax-send-and-local-commit-are-distinct-boundaries', 2),
    ('contract_tax_integration', v.IPC, 'SaveInvoice', 'zatcaService.IntegrateInvoice(ref inv,', 'zatcaService.OtherIntegration(ref inv,', 'tax-send-and-local-commit-are-distinct-boundaries'),
    ('ordinary_attachment_copy', v.IP, 'insertDocument', 'File.Copy(text, text2, overwrite: true);', 'File.Copy(text, text2, overwrite: false);', 'attachment-file-and-encoded-writers-own-connections'),
    ('contract_fallback_normal_lines', v.IPC, 'SaveInvoice', 'StoredQueries.InsertInvSub, sqlConnection3, sqlTransaction', 'StoredQueries.InsertInvSubcontract, sqlConnection3, sqlTransaction', 'contract-ordinary-fallback-line-target'),
    ('POS_cloud_first_condition', v.POS, 'SaveAndPrint', 'Sync.SyncCloudFirst && !holdbool', 'Sync.SyncCloudFirst && holdbool', 'cloud-first-result-checked-but-transfer-broker'),
    ('transfer_broker_activation', v.TRANS, 'SaveAndPrint', 'if (Home._is_active)', 'if (saved && Home._is_active)', 'cloud-first-result-checked-but-transfer-broker'),
    ('ordinary_sync_default_false', v.IP, 'SyncInvoice', 'bool result = default(bool);', 'bool result = true;', 'sync-local-wrapper-result-not-end-to-end'),
    ('contract_sync_noncloud_target', v.IPC, 'SyncInvoice', 'update Inv set Sync=1 where InvGlobalID=', 'update InvContratct set Sync=1 where InvGlobalID=', 'contract-noncloud-sync-target-and-void-callers'),
    ('contract_QRCode_parameter_present', v.IPC, 'SaveInvoice', 'sqlCommand4.Parameters.Add("@QRCode", SqlDbType.NVarChar).Value = inv.QRCode;', '', 'header-tax-parameters-are-present-counterexample'),
    ('contract_UUID_parameter_present', v.IPC, 'SaveInvoice', 'sqlCommand4.Parameters.Add("@UUID", SqlDbType.NVarChar).Value = inv.UUID;', '', 'header-tax-parameters-are-present-counterexample', 2),
    ('home_purchase_Name_key', v.HOME, 'stripPurchInv_Click', 'frm.Name = "frmSalePurch";', 'frm.Name = "frmInvPurch";', 'different-Name-Tag-and-lookup-order'),
    ('home_contract_return_Tag', v.HOME, 'stripinvcontractreturn_Click', 'frm.Tag = "frmcontract";', 'frm.Tag = "frmcontractReturn";', 'different-Name-Tag-and-lookup-order'),
    ('home_one_enabled_check_counterexample', v.HOME, 'btnPOS2_Click', 'else if (stripPOS.IsEnabled)', 'else if (true)', 'one-opener-enabled-check-counterexample'),
    ('existing_POS_import_path', v.SELECT, 'GenerateInvoice', 'openedPosWindow.ImportInventoryItems(itemList);', 'openedPosWindow.Activate();', 'alternate-import-can-target-existing-POS'),
    ('first_opened_window_selection', v.SELECT, 'FindOpenedWindow', '.FirstOrDefault()', '.LastOrDefault()', 'alternate-import-can-target-existing-POS'),
    ('import_IO_first_match', v.IO, 'ImportInventoryItems', 'FirstOrDefault(', 'LastOrDefault(', 'import-first-item-match-is-not-inserted-row-result'),
    ('import_POS_price_overwrite', v.POS, 'ImportInventoryItems', 'existing.ItemPrice = importedItem.ItemPrice;', 'existing.ItemPrice = 0;', 'import-first-item-match-is-not-inserted-row-result'),
    ('import_purchase_quantity_overwrite', v.PURCH, 'ImportInventoryItems', 'found.ItemQuantity = importedItem.ItemQuantity;', 'found.ItemQuantity = 0;', 'import-first-item-match-is-not-inserted-row-result'),
    ('import_sale_key_match', v.SALE, 'ImportInventoryItems', 'i.ItemId == importedItem.ItemId', 'i.ItemId != importedItem.ItemId', 'import-first-item-match-is-not-inserted-row-result'),
    ('contract_opener_UI_type_two', v.CONTACT, 'BtnShowInv_Click', 'contractForm.InvType = 2;', 'contractForm.InvType = 23;', 'contract-opener-UI-type-two-vs-selected-row-type23'),
    ('inventory_report_uses_global_key', v.RPTINV, 'OpenInputOutput', "InvGlobalID=N'{globalId}'", "id={globalId}", 'global-key-opener-counterexample-to-all-local-id-claim'),
]


def register_source_case(row):
    name, rel, sel, old, new, guard, *extra = row
    def test(self): self.mutation(rel, sel, old, new, guard, extra[0] if extra else 1)
    test.__name__ = 'test_source_mutation_' + name
    setattr(SaveEditTests, test.__name__, test)


for _row in SOURCE_MUTATIONS: register_source_case(_row)


EVIDENCE_MUTATIONS = [
    ('date_authority_not_clock', v.DATE_NOTE, lambda d: d.update(assessment_reference_date_utc='2026-11-22'), 'prospective-date-and-attribution'),
    ('date_not_user_attribution', v.DATE_NOTE, lambda d: d.update(user_requested_reference_date_authenticated=True), 'prospective-date-and-attribution'),
    ('literal_command_identity', v.MATRIX, lambda d: d['literal_command_sites'].pop(), 'exact-literal-command-sites'),
    ('no_command_owner_omitted', v.MATRIX, lambda d: d['command_reviews'].pop(), 'all23-selected-command-owner-identities'),
    ('command_source_hash', v.MATRIX, lambda d: d['command_reviews'][0]['whole_entry_context'].update(syntax_utf8_sha256='changed'), 'qualified-command-context'),
    ('command_not_whole_route', v.MATRIX, lambda d: d['command_reviews'][0].update(whole_route_or_capability_certified=True), 'qualified-command-context'),
    ('command_has_validation_disposition', v.MATRIX, lambda d: d['command_reviews'][0].update(input_to_validation=''), 'command-disposition'),
    ('command_no_handoff', v.MATRIX, lambda d: d['command_reviews'][0].update(accepted_external_handoff=True), 'qualified-command-context'),
    ('opener_creation_identity', v.MATRIX, lambda d: d['selected_alternate_editor_creations'].pop(), 'exact-selected-alternate-creations'),
    ('opener_owner_not_missing', v.MATRIX, lambda d: d['alternate_opener_reviews'].pop(), 'twentysix-selected-opener-owners'),
    ('opener_no_runtime_schedule', v.MATRIX, lambda d: d['alternate_opener_reviews'][0].update(all_ingress_or_runtime_schedule_certified=True), 'qualified-alternate-opener'),
    ('opener_has_allowed_set_disposition', v.MATRIX, lambda d: d['alternate_opener_reviews'][0].update(document_branch_year_and_allowed_set=''), 'qualified-alternate-opener'),
    ('pipeline_no_exit', v.MATRIX, lambda d: d['editor_pipelines'][v.POS].update(is_capability_exit=True), 'qualified-editor-pipeline'),
    ('pipeline_has_stock_disposition', v.MATRIX, lambda d: d['editor_pipelines'][v.IO].update(stock=''), 'qualified-editor-pipeline'),
    ('substantive_decision_not_removed', v.REVIEW, lambda d: d['source_decisions'].pop(), 'fifteen-substantive-source-decisions'),
    ('decision_not_observed_ERP', v.REVIEW, lambda d: d['source_decisions'][0].update(observed_in_ERP=True), 'qualified-source-decision'),
    ('basis_coordinate_changed', v.REVIEW, lambda d: d['source_decisions'][0]['source_basis'][0].update(start=1), 'basis:method'),
    ('capability_no_exit', v.REVIEW, lambda d: d['capabilities']['CAP7B38-D19'].update(whole_capability_certified=True), 'named-capability-local-remainder'),
    ('local_not_externalized', v.REVIEW, lambda d: d['capabilities']['CAP7B38-D17'].update(readable_local_externalized=True), 'named-capability-local-remainder'),
    ('no_unavailable_accepted', v.REVIEW, lambda d: d['unavailable_contracts_not_accepted_as_handoffs'][0].update(accepted_external_handoff=True), 'unavailable-is-not-local-work-substitute'),
    ('contract_has_redacted_input', v.REVIEW, lambda d: d['unavailable_contracts_not_accepted_as_handoffs'][0].update(required_redacted_input=''), 'unavailable-is-not-local-work-substitute'),
    ('original_dictionaries_not_removed', v.ROOTS, lambda d: d['available_prior_rows'].pop(), '339-original-dictionaries-preserved'),
    ('prior_root_dictionary_not_rewritten', v.ROOTS, lambda d: d['focused_root_reviews']['P4-014']['canonical_prior_row'].update(certainty='confirmed'), 'unchanged-root-row:P4-014'),
    ('root_candidate_not_numbered', v.ROOTS, lambda d: d['candidate_dispositions'][0].update(novelty_certified=True), 'qualified-root-question'),
    ('no_new_finding_by_count', v.ROOTS, lambda d: d.update(new_finding_ids=['invented']), 'no-novelty-or-missing-history'),
    ('no_missing345_reconstruction', v.ROOTS, lambda d: d.update(missing_six_dictionaries_reconstructed=True), 'no-novelty-or-missing-history'),
    ('original_R6_flags_not_rewritten', v.WORK, lambda d: d.update(original_R6_read_flags_rewritten=True), 'original-ancestry-and-unfinished-local'),
    ('R8_work_not_erased', v.WORK, lambda d: d['preserved_R8_local_task_rows_verbatim'].pop(), 'R8-local-obligations-not-erased'),
    ('save_edit_not_complete', v.WORK, lambda d: d.update(entire_R8LOCAL_SAVE_EDIT_marked_complete=True), 'original-ancestry-and-unfinished-local'),
    ('local_next_action_not_missing', v.WORK, lambda d: d['remaining_readable_local_tasks'][0].update(next_action=''), 'owned-local-task'),
    ('no_phase7C_start', v.REVIEW, lambda d: d.update(phase7C_started=True), 'static-open-scope'),
    ('no_phase8_authorization', v.REVIEW, lambda d: d.update(phase8_authorized=True), 'static-open-scope'),
    ('pin_identity_not_changed', v.REVIEW, lambda d: d['pinned_inputs'][0].update(sha256='changed'), 'pinned-input-changed'),
]


def register_evidence_case(row):
    name, filename, change, guard = row
    def test(self):
        errors = self.bad_evidence(filename, change)
        self.assertTrue(any(guard in e for e in errors), (guard, errors))
    test.__name__ = 'test_evidence_mutation_' + name
    setattr(SaveEditTests, test.__name__, test)


for _row in EVIDENCE_MUTATIONS: register_evidence_case(_row)


if __name__ == '__main__':
    unittest.main(verbosity=2)
