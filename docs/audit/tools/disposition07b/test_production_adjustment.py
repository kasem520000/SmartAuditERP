#!/usr/bin/env python3
"""R5 source/identity/disposition regressions, not SQL/WPF/financial scenarios.

C# mutations are reparsed in memory, not compiled or executed. JSON mutations are
isolated copies. No Python translation of business arithmetic is used as a
surrogate ERP test. The fixed assessment reference is not calendar attestation.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import verify_production_adjustment as v


class ProductionAdjustmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.facts = v.load(v.FACTS)
        cls.reads = v.load(v.READS)

    def changed_member(self, rel, selector, old, new, expected=1):
        original = v.base.decode((v.ROOT / rel).read_bytes())
        code = v.method(self.facts, rel, selector)['syntax_text']
        if '\r\n' in code:
            old, new = old.replace('\n', '\r\n'), new.replace('\n', '\r\n')
        self.assertEqual(code.count(old), expected, 'Must mutate actual selected source, not a synthetic fixture')
        self.assertEqual(original.count(code), 1)
        changed = original.replace(code, code.replace(old, new), 1)
        result = copy.deepcopy(self.facts)
        result['methods'][rel] = v.source_methods(changed, v.CONTEXTS[rel])
        if rel in v.CLASSES: result['classes'][rel] = v.class_facts(changed, v.CLASSES[rel])
        return result

    def bad_evidence(self, name, mutate):
        names = (v.FACTS, v.REVIEW, v.ROUTES, v.ROOTS, v.DATES,
                 'findings-additions-07B39R1.csv', 'capability-register-07B38.csv')
        with tempfile.TemporaryDirectory(prefix='smartaudit-r5-evidence-negative-') as tmp:
            ev = Path(tmp)
            for source in names: shutil.copyfile(v.EV / source, ev / source)
            obj = json.loads((ev / name).read_bytes())
            mutate(obj)
            (ev / name).write_text(json.dumps(obj, ensure_ascii=False), encoding='utf8')
            return v.evidence_errors(ev)

    def assert_source_rejected(self, facts):
        self.assertTrue(v.source_errors(facts))

    def test_fresh_facts_rederive_from_original_sources(self):
        self.assertEqual(v.derive(), self.facts)

    def test_current_source_and_supplied_resource_claims(self):
        self.assertEqual(v.source_errors(self.facts), [])
        self.assertEqual(v.resource_errors(self.facts), [])

    def test_actual_read_union_covers_selected_contexts_not_whole_files(self):
        self.assertEqual(v.read_errors(self.reads, self.facts), [])
        self.assertFalse(self.reads['extraction_equals_reading'])

    def test_evidence_is_consistent_but_does_not_certify_exits(self):
        self.assertEqual(v.evidence_errors(), [])
        self.assertFalse(v.load(v.REVIEW)['whole_7B_static_assessment_complete'])

    def test_entry_audit_inputs_and_827_original_sources_are_preserved(self):
        self.assertEqual(v.preservation_errors(v.load(v.ENTRY)), [])

    def test_production_no_header_really_calls_clear(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'if (!dr.HasRows) { CLR(); return; }', 'if (!dr.HasRows) { return; }'))

    def test_adjustment_no_header_is_not_mislabelled_as_clear(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'ReadData',
            'if (!dr.HasRows) return;', 'if (!dr.HasRows) { CLR(); return; }'))

    def test_production_read_reset_and_flag_order(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'dr.Read();\n            CLR();', 'CLR();\n            dr.Read();'))

    def test_adjustment_catch_does_not_invent_a_flag_finally(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'ReadData',
            'catch (Exception ex)\n            {', 'catch (Exception ex)\n            {\n                Isload = false;'))

    def test_missing_normal_flag_tail_is_rejected_without_index_error(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            '_isLoaded = false;', '_isLoaded = true;'))

    def test_production_navigate_has_its_actual_finally_close(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'Navigate',
            'CloseConn(_conn);', 'CloseConn(_conn1);'))

    def test_adjustment_navigate_is_not_given_an_unwritten_using(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'Navigate',
            'ReadData(cmd.ExecuteReader());', 'using (var dr = cmd.ExecuteReader()) { ReadData(dr); }'))

    def test_query_forwarding_does_not_invent_added_branch_scope(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'Navigate',
            'new SqlCommand(sqlQuery, _conn)', 'new SqlCommand(sqlQuery + " AND branch=@branch", _conn)'))

    def test_production_both_detail_partitions_use_loaded_global_id(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            "InvGlobalID=N'{_invGlobalID}'", "InvGlobalID=N'{_code}'", expected=2))

    def test_production_component_partition_is_positive_product_id(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'WHERE productId>0 AND', 'WHERE productId>=0 AND'))

    def test_loaded_base_quantity_is_not_fabricated(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'Qty = qty,', 'BaseQty = qty, Qty = qty,'))

    def test_loaded_unit_equality_is_not_fabricated(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'Qty = qty,', 'UnitEquality = 2, Qty = qty,'))

    def test_quantity_is_rounded_before_editor_publication(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'Math.Round(Convert.ToDouble(row["val1"]), 2)',
            'Math.Round(Convert.ToDouble(row["val1"]), 4)'))

    def test_price_is_rounded_before_editor_publication(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'ReadData',
            'Math.Round(Convert.ToDouble(row["exchange_price"]), 2)',
            'Math.Round(Convert.ToDouble(row["exchange_price"]), 4)'))

    def test_local_model_is_not_an_assumed_external_DTO(self):
        f = copy.deepcopy(self.facts)
        raw = v.base.decode((v.ROOT / v.PROD).read_bytes())
        self.assertEqual(raw.count('private double _baseQty;'), 1)
        f['classes'][v.PROD] = v.class_facts(raw.replace('private double _baseQty;', 'private double _baseQty = 1;', 1), v.CLASSES[v.PROD])
        self.assert_source_rejected(f)

    def test_quantity_handler_positive_base_guard(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'txtQty_TextChanged',
            '!string.IsNullOrEmpty(row.ItemName) && row.BaseQty > 0', '!string.IsNullOrEmpty(row.ItemName)'))

    def test_quantity_text_handler_is_not_invented_as_load_guarded(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'txtQty_TextChanged',
            'if (string.IsNullOrWhiteSpace(txtQty.Text))',
            'if (_isLoaded) return;\n                if (string.IsNullOrWhiteSpace(txtQty.Text))'))

    def test_unit_event_uses_the_distinct_existing_factor(self):
        self.assert_source_rejected(self.changed_member(v.PROD, 'cmbUnits_SelectionChanged',
            'Math.Round(perc * row.BaseQty * qty, 2)',
            'Math.Round(row.UnitEquality * row.BaseQty * qty, 2)'))

    def test_adjustment_reset_does_not_claim_to_reset_safe(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'CLR',
            'SelectedId = -1;', 'SelectedId = -1; cmbSafes.SelectedValue = -1;'))

    def test_adjustment_requires_approval_column_from_header(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'ReadData',
            'dr["Is_Approved"]', 'dr["InvoiceStatus"]'))

    def test_adjustment_safe_assignment_depends_on_existing_selection(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'ReadData',
            'if (cmbSafes.SelectedValue != null)', 'if (dr["safe"] != null)'))

    def test_adjustment_details_use_the_header_id_not_a_global_key(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'ReadData',
            'SafesAdjust_Sub WHERE Adjust_id={Code}', 'SafesAdjust_Sub WHERE InvGlobalID={Code}'))

    def test_adjustment_current_master_unit_is_not_saved_line_unit(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'ReadData',
            'Unit         = GetUnitName(itemId)',
            'Unit         = GetUnitName(Convert.ToInt32(row["unit"]))'))

    def test_adjustment_draft_really_persists_the_row_unit(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'AdjustStock',
            'GetUnitId(item.Unit)', '-1'))

    def test_adjustment_initializer_order_precedes_saved_overrides(self):
        f = copy.deepcopy(self.facts)
        m = v.method(f, v.SAFE, 'ReadData')
        v.assignments(m, 'CurrentStock')[0]['line'] = v.assignments(m, 'RealStock')[0]['line'] + 1
        self.assert_source_rejected(f)

    def test_saved_quantity_overrides_are_not_misdiagnosed_as_only_model_recalc(self):
        f = copy.deepcopy(self.facts)
        v.assignments(v.method(f, v.SAFE, 'ReadData'), 'adjRow.InQty')[0]['left'] = 'anotherRow.InQty'
        self.assert_source_rejected(f)

    def test_adjustment_number_is_the_actual_cardinality_expression(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'LoadAdjustNo',
            'nextNo = dt.Rows.Count + 1;', 'nextNo = dt.Rows.Count + 2;'))

    def test_adjustment_number_helper_uses_the_other_connection(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'LoadAdjustNo',
            '"SELECT id FROM SafesAdjust", conn1)', '"SELECT id FROM SafesAdjust", conn)'))

    def test_factory_body_constructs_a_new_connection(self):
        self.assert_source_rejected(self.changed_member(v.MC, 'ConnObj',
            'conn = new SqlConnection(connstr);', 'conn = conn;'))

    def test_MARS_present_in_builder_is_not_ignored(self):
        self.assert_source_rejected(self.changed_member(v.LOGIN, 'BuildConnectionStrings',
            'MultipleActiveResultSets=true', 'MultipleActiveResultSets=false', expected=3))

    def test_later_login_writes_prevent_universal_MARS_assertion(self):
        f = copy.deepcopy(self.facts)
        a = next(a for a in v.assignments(v.method(f, v.LOGIN, 'LoadBranches'), 'MainClass.connstr') if 'pwd=' in a['right'])
        a['right'] += ' + "MultipleActiveResultSets=true;"'
        self.assert_source_rejected(f)

    def test_safe_selection_event_is_not_given_an_unwritten_load_guard(self):
        self.assert_source_rejected(self.changed_member(v.SAFE, 'cmbSafes_SelectionChanged',
            'try\n            {', 'try\n            {\n                if (Isload) return;'))

    def test_configure_before_show_is_a_source_order_not_show_before_navigate(self):
        f = copy.deepcopy(self.facts)
        v.calls(v.method(f, v.DET, 'OpenWindow'), 'configure')[0]['line'] = 999999
        self.assert_source_rejected(f)

    def test_own_loaded_wiring_is_required_for_lifecycle_claim(self):
        f = copy.deepcopy(self.facts)
        next(x for x in f['xml_elements'][v.PROD[:-3]] if x['attributes'].get('Loaded') == 'Window_Loaded')['attributes']['Loaded'] = 'AnotherHandler'
        self.assert_source_rejected(f)

    def test_adjustment_unit_column_is_locally_editable(self):
        f = copy.deepcopy(self.facts)
        next(x for x in f['xml_elements'][v.SAFE[:-3]] if x['attributes'].get('Binding') == '{Binding Unit}')['attributes']['IsReadOnly'] = 'True'
        self.assert_source_rejected(f)

    def test_compact_DDL_declarations_are_not_silently_omitted(self):
        tables = self.facts['resources']['tables']
        self.assertIn('store', tables['Inv_Sub']['columns'])
        self.assertIn('tot_purch', tables['Inv']['columns'])
        for name, row in tables.items():
            text = self.facts['resources']['fragments'][row['fragment']]['raw_xml_text']
            independent = []
            for line in text.splitlines():
                plain = line.replace('[', '').replace(']', '')
                hit = re.match(r'^\s*(\w+)\s+(varchar|nvarchar|datetime|int|float|bit|decimal)(?=\W|$)', plain, re.I)
                # Whitespace-free bracket adjacency needs a separate lexical split.
                adjacent = re.match(r'^\s*\[(\w+)\]\[(varchar|nvarchar|datetime|int|float|bit|decimal)\]', line, re.I)
                if adjacent: independent.append(adjacent[1])
                elif hit: independent.append(hit[1])
            self.assertEqual(row['columns'], independent, name)
        first = v.load('initial-authoring-source-diagnostic-07B39R5.json')
        self.assertNotIn('store', first['resource_tables']['Inv_Sub']['columns'])
        self.assertEqual(first['source_claim_diagnostic_errors'], [])  # Not falsely relabelled a failed suite.

    def test_supplied_header_primary_keys_are_distinct(self):
        f = copy.deepcopy(self.facts)
        f['resources']['tables']['Inv']['primary_key_columns'] = ['id']
        self.assertTrue(v.resource_errors(f))

    def test_approval_column_is_absent_from_selected_Inv_create(self):
        f = copy.deepcopy(self.facts)
        f['resources']['tables']['Inv']['columns'].append('Is_Approved')
        self.assertTrue(v.resource_errors(f))

    def test_local_adjustment_patch_is_not_externalized(self):
        f = copy.deepcopy(self.facts)
        patch = f['resources']['fragments']['SafesAdjust-stock-and-item-patch']
        patch['raw_xml_text'] = patch['raw_xml_text'].replace("'ItemID'", "'OtherID'")
        self.assertTrue(v.resource_errors(f))

    def test_selected_schema_cannot_be_relabelled_a_deployment_attestation(self):
        f = copy.deepcopy(self.facts)
        f['resources']['tables']['Inv']['is_deployed_schema_attestation'] = True
        self.assertTrue(v.resource_errors(f))

    def test_request_binding_is_not_just_the_count_eleven(self):
        def mutate(x): x['requests'][0]['argument_expression'] += ' AND branch=0'
        self.assertTrue(self.bad_evidence(v.ROUTES, mutate))

    def test_inherited_request_identity_is_not_renamed(self):
        def mutate(x): x['individual_dispositions'][0]['inherited_R4_request_id'] = 'R4REQ-26'
        self.assertTrue(self.bad_evidence(v.ROUTES, mutate))

    def test_canonical_existing_root_dictionary_is_preserved(self):
        def mutate(x): x['focused_root_reviews']['P7-133']['canonical_prior_row']['severity'] = 'High'
        self.assertTrue(self.bad_evidence(v.ROOTS, mutate))

    def test_unit_candidate_cannot_invent_a_numbered_finding(self):
        def mutate(x):
            next(c for c in x['candidate_dispositions'] if c['id'] == 'R5C-ADJUSTMENT-UNIT')['root_id'] = 'P7-174'
        self.assertTrue(self.bad_evidence(v.ROOTS, mutate))

    def test_missing_prior_dictionaries_are_not_claimed_reviewed(self):
        self.assertTrue(self.bad_evidence(v.ROOTS, lambda x: x.update(all345_roots_screened=True)))

    def test_capability_exit_is_not_implied_by_this_slice(self):
        def mutate(x): x['capabilities']['CAP7B38-D17']['whole_capability_certified'] = True
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_readable_local_work_cannot_be_externalized(self):
        def mutate(x): x['local_obligation_decisions'][0]['readable_local_externalized'] = True
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_source_outcome_is_not_an_observed_ERP_failure(self):
        def mutate(x): x['reader_outcomes'][0]['observed_in_ERP'] = True
        self.assertTrue(self.bad_evidence(v.REVIEW, mutate))

    def test_unread_clear_tail_is_not_accepted_as_a_full_read(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'] = [r for r in reads['reads'] if not (r['path'] == v.PROD and r['start'] == 1535)]
        self.assertTrue(v.read_errors(reads, self.facts))

    def test_changed_read_range_hash_is_rejected(self):
        reads = copy.deepcopy(self.reads)
        reads['reads'][0]['decoded_range_utf8_sha256'] = '0' * 64
        self.assertTrue(v.read_errors(reads, self.facts))

    def test_session_date_field_is_not_the_raw_clock_or_calendar_proof(self):
        self.assertFalse(v.load(v.DATES)['raw_clocks_are_calendar_authority'])
        self.assertTrue(self.bad_evidence(v.REVIEW, lambda x: x.update(assessment_reference_date_utc='2026-11-21')))

    def test_completion_CLI_stays_open(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        process = subprocess.run([sys.executable, '-B', '-W', 'error::ResourceWarning',
            str(Path(v.__file__)), '--verify', '--require-complete'], env=env,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(process.returncode, 2, process.stderr.decode('utf8', errors='replace'))
        obj = json.loads(process.stdout)
        self.assertEqual(obj['errors'], [])
        self.assertEqual(obj['capability_exit_certificates_issued'], 0)
        self.assertFalse(obj['whole_7B_static_assessment_complete'])


if __name__ == '__main__':
    unittest.main()
