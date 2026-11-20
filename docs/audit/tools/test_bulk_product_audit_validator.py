#!/usr/bin/env python3
"""48 documentary self-tests, NOT bulk edit, WPF, SQL, SDK or ERP acceptance.

ALL738 protected prior cases remain unchanged, including ALL44 B25 in its
OWN324/raw325CRLF/indexes/presetB25 child. Synthetic31 fixtures test schema
rejection only; the actual31 archive has a separate hash/identity test. Supplied
Product-shaped values do not instantiate SDK DTOs or imply constructor defaults.
"""
from __future__ import annotations

import ast
import copy
import csv
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_bulk_product_part as b26
from validate_property_dialog_part import historical_b24_inputs
from check_bulk_product_witnesses import SOURCE_SLICES, allowed, checked, exact, general, number, parameter_plan, price_operation, product, selected_price

A = Path(__file__).resolve().parents[1]


class BulkProductAuditTests(unittest.TestCase):
    def old(self, n=324):
        return [dict(id=f'PX-{i:03d}', title='synthetic', severity='High', certainty='potential',
                     type='synthetic-only', status='open-not-remediated', next_phase='7;8', evidence='a.cs:1-2') for i in range(n)]

    def raw(self, data):
        s = io.StringIO(newline='')
        w = csv.DictWriter(s, fieldnames=list(data[0]), lineterminator='\r\n')
        w.writeheader()
        w.writerows(data)
        return s.getvalue().encode()

    def current(self):
        return self.old() + [self.old(1)[0] | dict(id=n, next_phase='8') for n in b26.NEW_IDS]

    def texts(self):
        return {n: 'FROZEN:' + n for n in b26.SHARED_DOCS}

    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'), read=lambda p: 'LIVE:' + str(p),
                               rows=lambda n: [dict(id='LIVE:' + n)])

    def context(self, f):
        return b26.historical_b25_inputs(f, self.old(), self.texts(), self.raw(self.old()))

    def table(self, name):
        return list(csv.DictReader(io.StringIO((A / 'evidence' / name).read_text(), newline='')))

    def groups(self, end):
        return '\n'.join(f'| G-{n:02d} | exact |' for n in range(1, end + 1)) + '\n'

    def contracts(self):
        fs, iv, tests = [], [], []
        for n in range(1, 17):
            fid, iid = f'FE-{n:02d}', f'INV-{n:02d}'
            root = b26.NEW_IDS[n - 1] if n <= 2 else 'H'
            common = dict(finding_ids=root, evidence='a.cs:1-2', acceptance_ids=';'.join(f'T-{i:02d}' for i in (2*n-1, 2*n)))
            fs.append(dict(id=fid, owner_role='owner', required_redacted_input='redacted', impact_if_unavailable='blocked',
                           next_step='step', limit='bounded', **common))
            iv.append(dict(id=iid, feature_ids=fid, required_invariant='invariant' + str(n), **common))
            for i in (2*n-1, 2*n):
                tests.append(dict(id=f'T-{i:02d}', feature_ids=fid, invariant_ids=iid, finding_ids=root,
                                  plan_kind='finding-specific' if n <= 2 else 'documentary', status='not-executed',
                                  acceptance_criterion='criterion' + str(i)))
        return fs, iv, tests

    def residuals(self):
        old = [dict(id=f'RS7B25-{n:02d}', upstream_contract_ids=f'H-OLD-{n}', required_redacted_input='upstream redacted',
                    disposition='external-handoff', current_handoff_or_split_ids='H7B25-03;H7B25-04') for n in range(1, 15)]
        new = [dict(upstream_residual_id=r['id'], upstream_artifact='evidence/residual-disposition-07B25.csv',
                    upstream_row_sha256=b26.row_sha(r), upstream_contract_ids=r['upstream_contract_ids'], local_result='bounded result',
                    owner_role='owner', required_redacted_input='upstream redacted; new contract', impact_if_unavailable='blocked',
                    next_step='step', static_exit_criterion='criterion', current_handoff_or_split_ids='H7B26-03;H7B26-04',
                    disposition='external-handoff', runtime_status='not-executed') for r in old]
        return new, old

    def splits(self):
        old = [dict(id=f'SP7B25-{n:02d}', required_input='upstream redacted') for n in range(1, 4)]
        new = [dict(upstream_split_id=r['id'], upstream_artifact='evidence/split-register-07B25.csv',
                    upstream_row_sha256=b26.row_sha(r), title='named split', candidate_scope_not_certified='bounded capability',
                    reason_for_split='reason', owner_role='owner', required_input='upstream redacted; new contract',
                    next_static_action='source trace', static_exit_criterion='exit',
                    status='explicit-further-static-split-not-started', runtime_status='not-executed') for r in old]
        return new, old

    def work(self):
        states = (['bounded-parent-contract-delivered-residuals-open'] * 2
                  + ['bounded-shared-contract-delivered-residuals-open', 'bounded-R4j-bulk-product-delivered-residuals-open']
                  + ['planned-not-started'] * 6)
        return [dict(part_family='7B' if n < 4 else '7C', status=s, runtime_status='not-executed',
                     counts_are_sessions_or_completion_percent='false') for n, s in enumerate(states)]

    def witness(self):
        return json.loads((A / 'evidence/bulk-product-witnesses-07B26.json').read_text())

    def history_fixture(self):
        """Synthetic31 SCHEMA fixture, NEVER proof that31 modes actually ran."""
        old = json.loads((A / 'evidence/historical-mode-verification-07B25.json').read_text())
        modes = copy.deepcopy(old['historical_modes'])
        modes.append(dict(mode='B25', findings_total=324, registry_used=b26.SNAPSHOT, process_exit_code=0,
            validation_errors=[], original_project_hashes_matching=827, audit_checker_self_test_cases_reported=738,
            audit_checker_self_test_suite_count=26, erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0,
            stdout_sha256='a' * 64, historical_B25_child=dict(tests_reported=44, expected_tests=44, process_exit_code=0,
                result='passed', historical_parser_cutoff='B25-not-current-B26-default', all_original_cases_executed_unmodified=True,
                dedicated_child_launcher='tools/run_historical_property_dialog_tests_07B26.py',
                no_test_skips_or_global_subprocess_or_path_patch=True, suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=31, historical_modes=modes, errors=[])

    def test_01_OWN324_exact_raw325CRLF_three_texts(self):
        f = self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'), self.old())
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw(self.old()))
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT / 'findings.csv').read_text(), newline=''))), self.old())
            self.assertEqual(f.read(f.AUDIT / 'README.md'), 'FROZEN:README.md')

    def test_02_reject_bad_OWN_rows_bytes_BOM_LF_texts(self):
        f, old, raw = self.fake(), self.old(), self.raw(self.old())
        for data, texts, b in ((old[:-1], self.texts(), raw), (old, self.texts(), b'\xef\xbb\xbf' + raw),
                               (old, self.texts(), raw.replace(b'\r\n', b'\n')), (old, {'README.md': 'only'}, raw),
                               (old, self.texts(), bytearray(raw))):
            with self.assertRaises(ValueError):
                with b26.historical_b25_inputs(f, data, texts, b):
                    pass
        old[-1]['id'] = old[0]['id']
        with self.assertRaises(ValueError):
            with b26.historical_b25_inputs(f, old, self.texts(), self.raw(old)):
                pass

    def test_03_context_local_Path_not_global_or_disk_overlay(self):
        f = self.fake()
        before = Path.read_bytes, Path.read_text
        with self.context(f):
            self.assertEqual((Path.read_bytes, Path.read_text), before)
            self.assertEqual(f.rows('else/findings.csv'), [dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(), Path(__file__).read_bytes())
            self.assertEqual(type(f.AUDIT)(__file__).read_text(), Path(__file__).read_text())
            self.assertEqual((f.AUDIT / 'q' / '..' / 'findings.csv').read_bytes(), self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):
                type(f.AUDIT)('/other/findings.csv').read_text()

    def test_04_nested_OWN322_and_exception_restoration(self):
        f = self.fake()
        before = f.AUDIT, f.read, f.rows
        with self.context(f):
            with historical_b24_inputs(f, self.old(322), self.texts(), self.raw(self.old(322))):
                self.assertEqual(len(f.rows('findings.csv')), 322)
            self.assertEqual(len(f.rows('findings.csv')), 324)
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):
                raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a, b in zip(before, (f.AUDIT, f.read, f.rows))))

    def test_05_frozen_rows_texts_copy_isolation(self):
        f, old, texts = self.fake(), self.old(), self.texts()
        saved = copy.deepcopy(old)
        with b26.historical_b25_inputs(f, old, texts, self.raw(old)):
            data = f.rows('findings.csv')
            data[0]['next_phase'] = 'bad'
            self.assertEqual(f.rows('findings.csv'), saved)
            self.assertEqual(f.read(f.AUDIT / 'PLAN.md'), 'FROZEN:PLAN.md')
        self.assertEqual(old, saved)
        self.assertEqual(texts, self.texts())

    def test_06_all324_fields_ALLnextphase_evidence_rawprefix(self):
        old, cur = self.old(), self.current()
        self.assertEqual(b26.registry_preservation_errors(old, cur, self.raw(cur), self.raw(old)), [])
        for key in old[0]:
            bad = copy.deepcopy(cur)
            bad[0][key] = 'changed'
            self.assertTrue(b26.registry_preservation_errors(old, bad, self.raw(bad), self.raw(old)), key)

    def test_07_only153_154_append_raw327CRLF_noBOM(self):
        old, cur = self.old(), self.current()
        for bad in (cur[:-1], cur + [dict(cur[-1])], cur[:324] + list(reversed(cur[324:]))):
            self.assertTrue(b26.registry_preservation_errors(old, bad, self.raw(bad), self.raw(old)))
        for raw in (self.raw(cur).replace(b'\r\n', b'\n'), b'\xef\xbb\xbf' + self.raw(cur), self.raw(cur)[:-2]):
            self.assertTrue(b26.registry_preservation_errors(old, cur, raw, self.raw(old)))

    def test_08_exact_G219_append220through223_only(self):
        self.assertEqual(b26.group_row_errors(self.groups(219), self.groups(223)), [])
        for bad in (self.groups(222), self.groups(224), self.groups(223).replace('G-99', 'G-98'),
                    self.groups(223).replace('| G-01 | exact', '| G-01 | changed')):
            self.assertTrue(b26.group_row_errors(self.groups(219), bad))

    def test_09_source_sentinels_expand_before_dedup_RC_regression(self):
        errors, calls = [], []
        fake = SimpleNamespace(check=lambda ok, msg: errors.append(msg) if not ok else None,
                               evidence=lambda *a: calls.append(a), scoped_evidence=lambda *a, **k: calls.append((a, k)))
        for gate in ('FE7B26-15', 'AD7B26-07', 'AD7B26-08'):
            b26.validate_source(fake, dict(id=gate, evidence=b26.DOCUMENTARY), {})
        self.assertEqual((errors, calls), ([], []))
        b26.validate_source(fake, dict(id='UNKNOWN', evidence=b26.DOCUMENTARY), {})
        b26.validate_source(fake, dict(id='FE7B26-15', evidence='a.cs:1-2'), {})
        self.assertEqual((len(errors), len(calls)), (2, 2))
        fs = [dict(evidence='a.cs:1-2;3;b.cs:7'), dict(evidence='a.cs:1-2;5;b.cs:7;9-10'), dict(evidence=b26.DOCUMENTARY)]
        self.assertEqual(b26.source_evidence_union(fs), 'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5;b.cs:9-10')
        self.assertEqual(b26.source_evidence_union([dict(evidence=b26.DOCUMENTARY)]), b26.DOCUMENTARY)
        for bad in ('5;a.cs:1-2', 'a.cs:1-2;unscoped', 'a.cs:'):
            with self.assertRaises(ValueError):
                b26.expanded_source_evidence(bad)
        fe, rc = self.table('feature-implementation-matrix-07B26.csv'), self.table('report-reconciliation-07B26.csv')
        for r in rc:
            self.assertEqual(r['evidence'], b26.source_evidence_union([f for f in fe if f['id'] in r['feature_ids'].split(';')]))

    def test_10_ordered_BE8_PW8_cause_command_and_default_limits(self):
        be, pw = self.table('bulk-edit-lineage-07B26.csv'), self.table('product-write-lineage-07B26.csv')
        self.assertEqual(b26.ledger_errors(be, pw), [])
        for pool, label in ((be, 'bulk'), (pw, 'writer')):
            bad = copy.deepcopy(pool)
            bad[0], bad[1] = bad[1], bad[0]
            self.assertTrue(b26.ledger_errors(bad, pw) if label == 'bulk' else b26.ledger_errors(be, bad))
        for index in (2, 3, 4, 5, 6):
            bad = copy.deepcopy(be)
            bad[index]['observation'] = 'all-accepted'
            self.assertTrue(b26.ledger_errors(bad, pw))
        for index in (0, 1, 2, 3, 4, 6, 7):
            bad = copy.deepcopy(pw)
            bad[index]['observation'] = 'all-accepted'
            self.assertTrue(b26.ledger_errors(be, bad))

    def test_11_ledger_responsibilities_nonempty_not_executed(self):
        be, pw = self.table('bulk-edit-lineage-07B26.csv'), self.table('product-write-lineage-07B26.csv')
        for key in ('source_to_output', 'observation', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                    'next_step', 'limit', 'feature_ids', 'finding_ids', 'evidence'):
            bad = copy.deepcopy(pw)
            bad[0][key] = ''
            self.assertTrue(b26.ledger_errors(be, bad), key)
        bad = copy.deepcopy(be)
        bad[0]['runtime_status'] = 'passed'
        self.assertTrue(b26.ledger_errors(bad, pw))
        self.assertTrue(b26.ledger_errors(be[:-1], pw))

    def test_12_FE16_INV16_T32_reverse_links_two_specific_roots(self):
        self.assertEqual(b26.current_link_errors(*self.contracts()), [])
        for pool, key in ((0, 'acceptance_ids'), (1, 'feature_ids'), (2, 'feature_ids'), (2, 'status'), (2, 'finding_ids')):
            parts = self.contracts()
            parts[pool][0][key] = 'changed'
            self.assertTrue(b26.current_link_errors(*parts), key)
        fs, iv, ts = self.contracts()
        self.assertTrue(b26.current_link_errors(fs, iv, ts[:-1]))

    def test_13_distinct_invariants_criteria_and_responsibilities(self):
        for key in ('owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step', 'limit'):
            fs, iv, ts = self.contracts()
            fs[0][key] = ''
            self.assertTrue(b26.current_link_errors(fs, iv, ts), key)
        fs, iv, ts = self.contracts()
        iv[1]['required_invariant'] = iv[0]['required_invariant']
        self.assertTrue(b26.current_link_errors(fs, iv, ts))
        fs, iv, ts = self.contracts()
        ts[1]['acceptance_criterion'] = ts[0]['acceptance_criterion']
        self.assertTrue(b26.current_link_errors(fs, iv, ts))

    def test_14_all14_residual_ancestry_hash_contracts(self):
        current, old = self.residuals()
        self.assertEqual(b26.residual_errors(current, old), [])
        for key in ('upstream_residual_id', 'upstream_artifact', 'upstream_row_sha256', 'upstream_contract_ids'):
            current, old = self.residuals()
            current[0][key] = 'changed'
            self.assertTrue(b26.residual_errors(current, old), key)
        self.assertTrue(b26.residual_errors(current[:-1], old))

    def test_15_full_old_inputs_all_routes_and_no_approval(self):
        for key in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step',
                    'static_exit_criterion', 'current_handoff_or_split_ids'):
            current, old = self.residuals()
            current[0][key] = ''
            self.assertTrue(b26.residual_errors(current, old), key)
        for key, value in (('required_redacted_input', 'lost'), ('disposition', 'approved'),
                            ('runtime_status', 'passed'), ('current_handoff_or_split_ids', 'H7B26-03')):
            current, old = self.residuals()
            current[0][key] = value
            self.assertTrue(b26.residual_errors(current, old), key)

    def test_16_three_split_ancestries_full_inputs_and_reasons(self):
        current, old = self.splits()
        self.assertEqual(b26.split_errors(current, old), [])
        for key in current[0]:
            current, old = self.splits()
            current[0][key] = ''
            self.assertTrue(b26.split_errors(current, old), key)
        current, old = self.splits()
        current[0]['required_input'] = 'replacement'
        self.assertTrue(b26.split_errors(current, old))

    def test_17_boundedR4j_fourB_sixC_unstarted_no_percent_or_sessions(self):
        self.assertEqual(b26.remaining_work_errors(self.work()), [])
        for index, key, value in ((3, 'status', 'complete'), (4, 'status', 'in-progress'),
                                  (0, 'runtime_status', 'passed'), (0, 'counts_are_sessions_or_completion_percent', 'true'),
                                  (0, 'part_family', '7C')):
            work = self.work()
            work[index][key] = value
            self.assertTrue(b26.remaining_work_errors(work), key)
        self.assertTrue(b26.remaining_work_errors(self.work()[:-1]))

    def test_18_witness_strict_bool_integer_limits_and_B10_addendum(self):
        self.assertEqual(b26.witness_metadata_errors(self.witness()), [])
        for key, value in (('application_code_imported_or_executed', 0), ('erp_runtime_tests_executed', False),
                            ('illustration_count', 16.0), ('B_R4j_bounded_not_whole7B_closure', 1),
                            ('external_DTO_constructor_defaults_assumed', True), ('database_commit_or_saved_loss_claimed', True),
                            ('phase8_authorized_or_started', True), ('phase7C_started', True)):
            self.assertTrue(b26.witness_metadata_errors(self.witness() | {key: value}), key)
        bad = self.witness()
        bad['retained_additive_B10_arithmetic_erratum']['reference_cost'] = 10
        self.assertTrue(b26.witness_metadata_errors(bad))

    def test_19_actual_witness_stdout_hash_readonly_recompute(self):
        raw = (A / 'evidence/bulk-product-witnesses-07B26.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), b26.WITNESS_SHA)
        run = subprocess.run([sys.executable, '-B', str(A / 'tools/check_bulk_product_witnesses.py')],
                             capture_output=True, text=True, timeout=25)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, '')
        self.assertEqual(json.loads(run.stdout), self.witness())

    def test_20_synthetic31_schema_OWN324_ALL44_not_execution_evidence(self):
        self.assertEqual(b26.historical_record_errors(self.history_fixture()), [])
        for index, key, value in ((30, 'findings_total', 326), (30, 'registry_used', 'findings.csv'),
                                  (30, 'stdout_sha256', 'bad'), (30, 'audit_checker_self_test_cases_reported', 786),
                                  (0, 'audit_checker_self_test_cases_reported', 0), (30, 'erp_runtime_tests_executed', False)):
            h = self.history_fixture()
            h['historical_modes'][index][key] = value
            self.assertTrue(b26.historical_record_errors(h), key)
        h = self.history_fixture()
        h['historical_modes'][-1]['historical_B25_child']['suite_own_registry_path_is_context_local_not_global'] = False
        self.assertTrue(b26.historical_record_errors(h))
        h = self.history_fixture()
        h['historical_modes'] = h['historical_modes'][:-1]
        self.assertTrue(b26.historical_record_errors(h))

    def test_21_actual31_archive_identity_separate_from_schema_fixture(self):
        raw = (A / 'evidence/historical-mode-verification-07B26.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), b26.HISTORICAL_RUN_SHA)
        h = json.loads(raw)
        self.assertEqual(b26.historical_record_errors(h), [])
        self.assertEqual(h['checkout_head'], b26.ENTRY)
        self.assertEqual(h['current_actual_CLI_default'], 'B26')
        self.assertEqual(h['historical_mode_count'], 31)
        self.assertTrue(all(m['process_exit_code'] == 0 and m['stderr_bytes'] == 0 for m in h['historical_modes']))

    def test_22_valid_packing12_and24_become2_and_parameter_source(self):
        for value in ('12', '24'):
            result = general(product(), 2, value)
            self.assertFalse(result['rejected'])
            self.assertEqual(result['product']['packing'], '2')
            plan = parameter_plan(result['product'])
            self.assertEqual(plan['header']['@FillValue'], '2')
            self.assertNotEqual(plan['header']['@FillValue'], value)
            self.assertFalse(plan['database_executed'])

    def test_23_input2_fixed_point_is_not_acceptance_of_other_inputs(self):
        p = general(product(), 2, '2')['product']
        self.assertEqual(p['packing'], '2')
        self.assertEqual(parameter_plan(p)['header']['@FillValue'], '2')
        self.assertNotEqual(general(product(), 2, '12')['product']['packing'], '12')

    def test_24_zero_and_empty_packing_reject_before_all_mutation(self):
        p = product()
        for value in ('0', '0.0', None):
            r = general(p, 2, value, sale='20', purchase='8', unit=1)
            self.assertTrue(r['rejected'])
            self.assertEqual(r['product'], p)
            self.assertEqual(r['reason'], 'zero-or-empty-packing')
            self.assertFalse(r['application_executed'])

    def test_25_unselected_other_and_explicit_zero_property_controls(self):
        p = product()
        self.assertEqual(general(p)['product'], p)
        for prop in (0, 3):
            r = general(p, prop)['product']
            self.assertEqual(r['property'], prop)
            self.assertEqual(r['packing'], p['packing'])
        self.assertEqual(p, product())

    def test_26_supplied_product_schema_types_and_copy_no_DTO_defaults(self):
        p = product()
        for bad in (p | {'extra': 'x'}, p | {'id': True}, p | {'main_unit': 0}, p | {'property': 9},
                    p | {'units': None}, p | {'packing': 'NaN'}, p | {'units': [p['units'][0], p['units'][0]]}):
            with self.assertRaises(ValueError):
                checked(bad)
        bad = copy.deepcopy(p)
        bad['units'][0]['id'] = True
        with self.assertRaises(ValueError):
            checked(bad)
        saved = copy.deepcopy(p)
        r = general(p, 2, '12')['product']
        r['units'][0]['sale'] = '999'
        self.assertEqual(p, saved)

    def test_27_local_permission_branch_controls_not_ACL_acceptance(self):
        for opts in (dict(user_edit=False), dict(branch_type=2, sync_type=1)):
            r = general(product(), 2, '12', sale='20', **opts)
            self.assertTrue(r['rejected'])
            self.assertEqual(r['product'], product())
        self.assertTrue(allowed(True, 2, 0))
        self.assertTrue(allowed(True, 1, 1))
        for args in ((1, 1, 0), (True, True, 0), (True, 1, False)):
            with self.assertRaises(ValueError):
                allowed(*args)

    def test_28_sale_general_header20_existing_unit10_default_consumer(self):
        p = general(product(), sale='20')['product']
        self.assertEqual((p['sale'], p['units'][0]['sale']), ('20', '10'))
        self.assertEqual(selected_price(p, 'sale')['value'], '10')
        self.assertEqual(selected_price(p, 'sale')['source'], 'matched-ItemUnits')
        self.assertEqual(parameter_plan(p)['header']['@sale_price'], '20')

    def test_29_purchase_general_header8_unit6_same154_not_second_root(self):
        p = general(product(), purchase='8')['product']
        self.assertEqual((p['purchase'], p['units'][0]['purchase']), ('8', '6'))
        self.assertEqual(selected_price(p, 'purchase')['value'], '6')
        plan = parameter_plan(p)
        self.assertEqual((plan['header']['@purch_price'], plan['unit_rows'][0]['@purch']), ('8', '6'))

    def test_30_general_ignores_flags_separate_price_command_obeys_them(self):
        r = general(product(), sale='20', purchase='8', apply_sale=False, apply_purchase=False)
        self.assertEqual((r['product']['sale'], r['product']['purchase']), ('20', '8'))
        self.assertTrue(r['price_checkboxes_not_consulted'])
        self.assertEqual(price_operation(product(), 1, sale='20', purchase='8'), product())
        self.assertEqual(general(product(), sale='20', apply_sale=True)['product'], r['product'] | {'purchase': '6'})

    def test_31_same_unit_selection_synchronizes_not_remap_certification(self):
        p = general(product(), sale='20', purchase='8', unit=1)['product']
        self.assertEqual((p['main_unit'], p['units'][0]['id']), (1, 1))
        self.assertEqual((p['sale'], p['units'][0]['sale'], p['purchase'], p['units'][0]['purchase']), ('20', '20', '8', '8'))
        self.assertEqual(p['units'][1], product()['units'][1])
        self.assertEqual(selected_price(p, 'sale')['value'], '20')
        # No change of UnitId/ratio, no stock or historical conversion supplied.
        self.assertEqual(p['units'][0]['ratio'], '1')

    def test_32_empty_unit_rows_fallback_control_not_database_absence(self):
        p = product()
        p['units'] = []
        edited = general(p, sale='20', purchase='8')['product']
        # The selected source733..811 contains the sale/Default fallback only;
        # do not promote the inert helper's purchase fallback to reviewed code.
        result = selected_price(edited, 'sale')
        self.assertEqual((result['value'], result['source']), ('20', 'Items-fallback'))
        self.assertTrue(result['SQL_lookup_supplied_not_executed'])
        self.assertEqual(edited['purchase'], '8')  # Header mapping, not a reader claim.
        with self.assertRaises(ValueError):
            selected_price(p, 'unknown')

    def test_33_writer_parameter_sources_independent_subset_not_SQL_commit(self):
        p = general(product(), 2, '24', sale='20')['product']
        saved = copy.deepcopy(p)
        plan = parameter_plan(p)
        self.assertEqual((plan['header']['@FillValue'], plan['header']['@sale_price'], plan['unit_rows'][0]['@sale']), ('2', '20', '10'))
        self.assertFalse(plan['database_executed'])
        self.assertTrue(plan['commit_success_not_assumed'])
        plan['unit_rows'][0]['@sale'] = '999'
        self.assertEqual(p, saved)

    def test_34_four_price_operations_update_each_supplied_unit_controls(self):
        expected = {1: ('10', '10', '10'), 2: ('20', '20', '130'), 3: ('11', '11', '132'), 4: ('9', '9', '108')}
        for kind, values in expected.items():
            r = price_operation(product(), kind, sale='10', apply_sale=True)
            self.assertEqual((r['sale'], r['units'][0]['sale'], r['units'][1]['sale']), values)
            self.assertEqual(r['purchase'], product()['purchase'])
        # Equal increase/replacement across ratios is text tracing, not endorsed policy.
        self.assertEqual(product()['units'][1]['sale'], '120')

    def test_35_price_purchase_flag_and_missing_value_control(self):
        r = price_operation(product(), 2, purchase='2', apply_purchase=True)
        self.assertEqual((r['purchase'], r['units'][0]['purchase'], r['units'][1]['purchase']), ('8', '8', '74'))
        self.assertEqual(r['sale'], product()['sale'])
        self.assertEqual(price_operation(product(), 3, apply_sale=True), product())
        self.assertEqual(price_operation(product(), 1, purchase='8', apply_purchase=False), product())

    def test_36_operation_and_selection_strict_types_fixture_domain_limits(self):
        for kind in (True, 0, 5, '2'):
            with self.assertRaises(ValueError):
                price_operation(product(), kind)
        for opts in (dict(apply_sale=1), dict(unit=True), dict(property_index=True)):
            with self.assertRaises(ValueError):
                general(product(), **opts)
        with self.assertRaises(ValueError):
            price_operation(product(), 1, apply_sale=1)
        with self.assertRaises(ValueError):
            price_operation(product(), 4, sale='101', apply_sale=True)

    def test_37_exact_fixture_domain_not_dotnet_culture_precision_rounding(self):
        for bad in (True, 1, None, 'NaN', 'Infinity', '-1', ' 1 ', '1,5', '1e3', '01', '', '1/2'):
            with self.assertRaises(ValueError):
                number(bad)
        self.assertEqual(number('1.25'), Fraction(5, 4))
        self.assertEqual(exact(Fraction(1, 8)), '0.125')
        for bad in (Fraction(1, 3), Fraction(1, 16), Fraction(-1)):
            with self.assertRaises(ValueError):
                exact(bad)

    def test_38_ACTUAL_B26_parser_versioned_B25_B24_API_B15(self):
        self.assertEqual(v.main.__defaults__, ('B15',))
        for name, part in (('PHASE7_B16_CLI', 'B16'), ('PHASE7_CURRENT_CLI', 'B17')) + tuple((f'PHASE7_B{n}_CLI', f'B{n}') for n in range(18, 26)):
            self.assertEqual(getattr(v, name)['default'], part)
        parser = v.build_cli_parser()
        self.assertEqual(parser.parse_args([]).phase7_part, 'B26')
        for part in ('A',) + tuple('B' + str(n) for n in range(1, 27)):
            self.assertEqual(parser.parse_args(['--phase7-part', part]).phase7_part, part)
        self.assertEqual(parser.parse_args(['--through-phase', '2']).through_phase, 2)

    def test_39_real_entrypoint_historical25_before_current_bulk(self):
        tree = ast.parse(Path(v.__file__).read_text())
        blocks = [n for n in tree.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'"]
        self.assertEqual(len(blocks), 1)
        self.assertIn('build_cli_parser().parse_args()', ast.unparse(blocks[0]))
        self.assertIn('main(args.through_phase, args.phase7_part)', ast.unparse(blocks[0]))
        body = ast.unparse(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main'))
        self.assertLess(body.index('historical_b24_validation('), body.index('historical_b25_validation('))
        self.assertLess(body.index('historical_b25_validation('), body.index('extend_bulk_products('))
        self.assertIn('extend_property_dialogs(historical_b25,', body)
        self.assertIn("phase7_part == 'B25'", body)
        self.assertIn('PHASE7_LIVE_CLI', ast.unparse(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'build_cli_parser')))

    def test_40_exact_argv_proxy_preserves_unrelated_calls_kwargs(self):
        calls = []
        backend = SimpleNamespace(run=lambda *a, **k: calls.append((a, k)) or 'sentinel')
        proxy = b26.HistoricalB25Subprocess(backend, 'python', Path('/a/tools'))
        kwargs = dict(cwd='/a', capture_output=True, text=True, timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected), **kwargs), 'sentinel')
        self.assertEqual(calls[-1], ((proxy.actual,), kwargs))
        for args in (proxy.expected + ['--different'], ['python', '-B', '/else/test_property_dialog_audit_validator.py']):
            proxy.run(args, **kwargs)
            self.assertEqual(calls[-1], ((args,), kwargs))
        proxy.run(tuple(proxy.expected), 'positional', **kwargs)
        self.assertEqual(calls[-1], ((tuple(proxy.expected), 'positional'), kwargs))

    def test_41_view_exception_restore_no_global_Path_or_shared_subprocess_patch(self):
        backend = SimpleNamespace(run=lambda *a, **k: 'sentinel')
        f = self.fake()
        f.subprocess, f.sys = backend, SimpleNamespace(executable='python')
        view = b26.HistoricalB25ValidatorView(f)
        original = subprocess.run, Path.read_bytes, Path.read_text
        before = f.AUDIT, f.read, f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess, backend)
                self.assertEqual((subprocess.run, Path.read_bytes, Path.read_text), original)
                self.assertEqual(len(view.rows('findings.csv')), 324)
                raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a, b in zip(before, (f.AUDIT, f.read, f.rows))))

    def test_42_historical_child_ALL44_local_A_and_protected_B25_B24_tools(self):
        tools = A / 'tools'
        source = ast.unparse(ast.parse((tools / 'run_historical_property_dialog_tests_07B26.py').read_text()))
        for token in ('loadTestsFromModule(historical_tests)', 'suite.countTestCases() != 44',
                      'result.testsRun != 44 or result.skipped', 'historical_tests.A = v.AUDIT',
                      'historical_tests.A = original_a', 'v.PHASE7_LIVE_CLI = original_preset', 'v.PHASE7_B25_CLI',
                      'b26.historical_b25_inputs('):
            self.assertIn(token, source)
        self.assertNotIn('unittest.skip', source)
        prov = json.loads((A / 'evidence/provenance-07B26.json').read_text())
        for name in ('test_property_dialog_audit_validator.py', 'validate_property_dialog_part.py', 'check_property_dialog_witnesses.py',
                     'run_historical_row_ownership_tests_07B25.py', 'test_row_ownership_audit_validator.py',
                     'validate_row_ownership_part.py', 'test_item_ingress_audit_validator.py', 'test_contract_item_audit_validator.py'):
            self.assertEqual(hashlib.sha256((tools / name).read_bytes()).hexdigest(), prov['historical_artifact_sha256']['tools/' + name])

    def test_43_actual324_all_fields_barriers_three_freeze_hashes(self):
        raw = (A / b26.SNAPSHOT).read_bytes()
        old = list(csv.DictReader(io.StringIO(raw.decode(), newline='')))
        now = (A / 'findings.csv').read_bytes()
        cur = list(csv.DictReader(io.StringIO(now.decode(), newline='')))
        self.assertEqual(b26.registry_preservation_errors(old, cur, now, raw), [])
        self.assertEqual(cur[:324], old)
        lookup = {r['id']: r for r in cur}
        for name in ('P4-014', 'P7-132', 'P7-145'):
            self.assertEqual(lookup[name]['certainty'], 'potential')
        self.assertEqual(self.table('historical-extensions-07B26.csv'), [])
        for name, digest in ((b26.SNAPSHOT, b26.SNAPSHOT_SHA), (b26.SHARED_SNAPSHOT, b26.SHARED_SHA),
                              ('evidence/provenance-07B26.json', b26.PROVENANCE_SHA)):
            self.assertEqual(hashlib.sha256((A / name).read_bytes()).hexdigest(), digest)

    def test_44_scope9_overlap5_new4_union425_actual15read_hashes_two_whole(self):
        d = json.loads((A / 'evidence/scope-decision-07B26.json').read_text())
        self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths', 'prior_union', 'overlap', 'new', 'union', 'complement')),
                         (9, 421, 5, 4, 425, 402))
        self.assertEqual(d['bookkeeping']['complement_kinds'], {'source': 337, 'generated-artifact': 61, 'project-or-resource': 4})
        self.assertEqual(d['selected_upstream_split'], 'SP7B25-01')
        self.assertFalse(d['historical_body_review_claim'])
        w = self.witness()
        self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']), w['whole_local_editor_files_selected']), (15, 2))
        actual = {}
        for r in w['bounded_source_reads_not_semantic_coverage']:
            raw = (A.parents[1] / r['path']).read_bytes()
            lines = raw.decode('utf8').splitlines(keepends=True)
            self.assertEqual(hashlib.sha256(raw).hexdigest(), r['source_sha256'])
            self.assertEqual(hashlib.sha256(''.join(lines[r['start']-1:r['end']]).encode()).hexdigest(), r['selected_text_utf8_sha256'])
            actual.setdefault(r['path'], []).append((r['start'], r['end']))
        self.assertEqual(actual, SOURCE_SLICES)

    def test_45_two_adjudicated_roots_nearest_not_recounted_no_third(self):
        ad = self.table('root-adjudication-07B26.csv')
        self.assertEqual([r['current_root_ids'] for r in ad if r['decision'] == 'new-local-root'], b26.NEW_IDS)
        self.assertEqual([r['current_root_ids'] for r in ad if r['decision'] == 'same-current-root-command-controls-not-separate-finding'], ['P7-154'])
        self.assertTrue(all(r['comparison_depth'] == b26.DEDUP_DEPTH for r in ad))
        self.assertIn('P7-152', ad[0]['nearest_prior_root_ids'])
        self.assertIn('P4-026', ad[1]['nearest_prior_root_ids'])
        self.assertIn('P7-142', ad[1]['nearest_prior_root_ids'])
        self.assertIn('P5-021', ad[3]['nearest_prior_root_ids'])
        self.assertEqual(self.table('historical-extensions-07B26.csv'), [])

    def test_46_actual14residuals_three_splits_full_inputs_routes(self):
        rs, old = self.table('residual-disposition-07B26.csv'), self.table('residual-disposition-07B25.csv')
        sp, osp = self.table('split-register-07B26.csv'), self.table('split-register-07B25.csv')
        self.assertEqual(b26.residual_errors(rs, old), [])
        self.assertEqual(b26.split_errors(sp, osp), [])
        fe, iv, plans = [self.table(n + '-07B26.csv') for n in ('feature-implementation-matrix', 'report-invariants', 'acceptance-tests')]
        self.assertEqual(b26.current_link_errors(fe, iv, plans), [])
        self.assertTrue(all(t['status'] == 'not-executed' and t['procedure'] and t['safety_controls'] for t in plans))

    def test_47_additive_reference_clock_capture_identity_not_relabelling(self):
        prov = json.loads((A / 'evidence/provenance-07B26.json').read_text())
        note = (A / 'DATE-IDENTITY-NOTE-07B26.md').read_text()
        self.assertEqual(b26.date_identity_errors(prov, note), [])
        self.assertTrue(b26.date_identity_errors(prov | {'audit_reference_date_utc': '2026-11-20'}, note))
        self.assertTrue(b26.date_identity_errors(prov, note.replace(b26.B25_CHECK_SHA, 'changed')))
        self.assertEqual(hashlib.sha256((A / 'evidence/checks-07B25.json').read_bytes()).hexdigest(), b26.B25_CHECK_SHA)
        old = json.loads((A / 'evidence/checks-07B25.json').read_text())
        self.assertEqual(old['checkout_head'], '45a2a504db4f82927a286ce425f21a82bcee7a84')
        self.assertNotEqual(old['checkout_head'], b26.ENTRY)

    def test_48_collector_stdlib_only_no_app_import_or_execution_and_protected734(self):
        tools = A / 'tools'
        tree = ast.parse((tools / 'check_bulk_product_witnesses.py').read_text())
        imports = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n, ast.ImportFrom):
                imports.add(n.module.split('.')[0])
        self.assertEqual(imports, {'__future__', 'copy', 'fractions', 'hashlib', 'json', 're', 'sys', 'pathlib'})
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {'eval', 'exec', '__import__'} for n in ast.walk(tree)))
        prov = json.loads((A / 'evidence/provenance-07B26.json').read_text())
        self.assertEqual(len(prov['historical_artifact_sha256']), 734)
        self.assertTrue(all(hashlib.sha256((A / n).read_bytes()).hexdigest() == h for n, h in prov['historical_artifact_sha256'].items()))
        for name in ('validate_bulk_product_part.py', 'run_historical_property_dialog_tests_07B26.py',
                     'test_bulk_product_audit_validator.py'):
            ast.parse((tools / name).read_text(), filename=name)


if __name__ == '__main__':
    unittest.main()
