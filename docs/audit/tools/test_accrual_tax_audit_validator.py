#!/usr/bin/env python3
"""32 new B15 synthetic DOCUMENTATION-checker cases, NOT ERP acceptance.

Retains all350 prior cases in their protected suites. Artificial rows/ranges/
texts plus exact-path IN-MEMORY adapters only. No application import/build/
C#/SQL/WPF/REPX/Office/provider/device/shell/measurement/remediation/real data.
"""
from __future__ import annotations
import copy
import csv
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_accrual_tax_part as b15
from validate_inventory_activity_part import historical_b13_inputs
from validate_trial_balance_part import historical_b12_inputs


class AccrualTaxAuditTests(unittest.TestCase):
    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'), read=lambda p: 'LIVE:' + str(p),
                               rows=lambda p: [dict(id='LIVE:' + p)])

    def old(self, n=294):
        return [dict(id=f'P-X{i:03d}', title='synthetic', severity='High', certainty='confirmed',
                     type='synthetic-only', status='open-not-remediated', next_phase='7;8', evidence='a.cs:1-2') for i in range(n)]

    def raw(self, old=None):
        old = self.old() if old is None else old
        out = io.StringIO(newline='')
        writer = csv.DictWriter(out, fieldnames=list(old[0]), lineterminator='\r\n')
        writer.writeheader()
        writer.writerows(old)
        return out.getvalue().encode()

    def texts(self):
        return {name: 'FROZEN:' + name for name in b15.SHARED_DOCS}

    def context(self, f):
        return b15.historical_b14_inputs(f, self.old(), self.texts(), self.raw())

    def item(self, path='a.cs', lines='10', kind='source'):
        return dict(path=path, lines=lines, kind=kind)

    def scope(self, path='a.cs', ranges='2-4'):
        return dict(path=path, ranges=ranges, review_state='synthetic-only')

    def groups(self, count=164):
        return '\n'.join(f'| G-{i:02d} | exact row |' for i in range(1, count+1)) + '\n'

    def erratum(self):
        return dict(entered_quantity=2, equality=12, base_unit_cost=5, local_cost=10, reference_cost=120, archive_rewritten=False)

    def metadata(self):
        return dict(phase='7B15-partial-static-audit', application_code_imported_or_executed=False,
                    application_remediation_performed=False, real_business_or_secret_data_used=False,
                    spreadsheet_or_formula_interpreter_executed=False, erp_runtime_tests_executed=0,
                    sql_or_external_service_tests_executed=0, illustration_count=24, static_lexical_contract_check_count=24,
                    parents_csharp_already_full_7A_B1=True, child_selected_slices_not_parent_depth=True,
                    tax_home_route_is_alternate_not_parent_certified=True, B_R1_R2_residual_contracts_not_closed=True,
                    supplied_sql_not_certified_deployed=True, progress_categories_not_wholly_unread_counts=True,
                    parent_source_lines_not_first_coverage=dict(csharp=1876, xaml=1441, total=3317),
                    retained_additive_B10_arithmetic_erratum=self.erratum())

    def plan(self):
        return [dict(id=f'RW-{i}', part_family='7B' if i < 4 else '7C', title='synthetic planning group',
                     candidate_scope_not_certified='synthetic bounded scope', expected_deliverable='synthetic assessment',
                     static_exit_criterion='reasoned disposition of each selected contract',
                     dependencies_and_uncertainty='external contract unresolved',
                     status='bounded-parent-contract-delivered-residuals-open' if i < 2 else 'planned-not-started',
                     runtime_status='not-executed', counts_are_sessions_or_completion_percent='false') for i in range(10)]

    def depth(self):
        return [dict(prior_full_local_csharp_declared='true', b15_full_local_body_and_xaml='true',
                     remaining_old_category_after_b15='false') for _ in range(2)]

    def acceptance(self):
        new_ids = [f'P7-{n}' for n in range(123, 127)]
        extensions = [dict(finding_ids=f'OLD-{i:02d}') for i in range(22)]
        tests = []
        for n, fid in enumerate(new_ids, 1):
            for _ in range(2):
                tests.append(dict(finding_ids=fid, feature_ids=f'FE7B15-{n:02d}', invariant_ids=f'INV7B15-{n:02d}',
                                  plan_kind='finding-specific', status='not-executed'))
        tests.extend(dict(finding_ids=e['finding_ids'], plan_kind='historical-root-regression', status='not-executed') for e in extensions)
        for kind, count in [('cross-cutting-contract', 4), ('documentary-scope-or-authorization-gate', 2)]:
            tests.extend(dict(finding_ids='HANDOFF', plan_kind=kind, status='not-executed') for _ in range(count))
        return tests, new_ids, extensions

    def adjudication(self):
        return [dict(current_root_ids=f'P7-{123+i}' if i < 4 else 'OLD', nearest_prior_root_ids='NEAREST',
                     decision='new-local-root' if i < 4 else 'retained-or-extended', reason='source-bound synthetic distinction',
                     comparison_depth='all294-titles-classifications-evidence-paths-plus-selected-nearest-chains-not-all-historical-chains',
                     runtime_status='not-executed') for i in range(10)]

    def test_01_own_frozen294_and_exact_three_index_texts(self):
        f = self.fake()
        with self.context(f):
            self.assertEqual(len(f.rows('findings.csv')), 294)
            for name in b15.SHARED_DOCS:
                self.assertEqual(f.read(f.AUDIT / name), 'FROZEN:' + name)

    def test_02_exact_bytes_at_one_path_not_global_pathlib(self):
        f = self.fake()
        method = Path.read_bytes
        with self.context(f):
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw())
            self.assertIs(Path.read_bytes, method)
            self.assertEqual(str(f.AUDIT / 'findings.csv'), '/synthetic/audit/findings.csv')

    def test_03_normal_exit_restores_object_identities(self):
        f = self.fake()
        before = f.AUDIT, f.read, f.rows
        with self.context(f):
            pass
        for after, old in zip((f.AUDIT, f.read, f.rows), before):
            self.assertIs(after, old)

    def test_04_exception_restores_object_identities(self):
        f = self.fake()
        before = f.AUDIT, f.read, f.rows
        with self.assertRaisesRegex(RuntimeError, 'synthetic'):
            with self.context(f):
                raise RuntimeError('synthetic')
        for after, old in zip((f.AUDIT, f.read, f.rows), before):
            self.assertIs(after, old)

    def test_05_nested_B13_uses_own291_bytes_then_returns294(self):
        f = self.fake()
        inner = self.old(291)
        with self.context(f):
            with historical_b13_inputs(f, inner, {name: 'B13:' + name for name in b15.SHARED_DOCS}, self.raw(inner)):
                self.assertEqual(len(f.rows('findings.csv')), 291)
                self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw(inner))
                self.assertEqual(f.read(f.AUDIT / 'PLAN.md'), 'B13:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')), 294)
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw())
            with self.assertRaises(RuntimeError):
                with historical_b13_inputs(f, inner, self.texts(), self.raw(inner)):
                    raise RuntimeError('synthetic')
            self.assertEqual(f.read(f.AUDIT / 'PLAN.md'), 'FROZEN:PLAN.md')
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw())

    def test_06_three_nested_snapshots_do_not_leak_rows_or_bytes(self):
        f = self.fake()
        rows291, rows289 = self.old(291), self.old(289)
        with self.context(f):
            with historical_b13_inputs(f, rows291, self.texts(), self.raw(rows291)):
                with historical_b12_inputs(f, rows289, {name: 'B12:' + name for name in b15.SHARED_DOCS}, self.raw(rows289)):
                    self.assertEqual(len(f.rows('findings.csv')), 289)
                    self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw(rows289))
                    self.assertEqual(f.read(f.AUDIT / 'README.md'), 'B12:README.md')
                self.assertEqual(len(f.rows('findings.csv')), 291)
                self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw(rows291))
            self.assertEqual(len(f.rows('findings.csv')), 294)
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw())

    def test_07_wrong_counts_and_duplicate_ids_rejected(self):
        duplicate = self.old()
        duplicate[-1]['id'] = duplicate[0]['id']
        for bad in (self.old(291), self.old(293), self.old(295), duplicate):
            with self.assertRaises(ValueError):
                with b15.historical_b14_inputs(self.fake(), bad, self.texts(), self.raw(bad)):
                    pass

    def test_08_exact_raw_bytes_rows_CRLF_noBOM_agreement(self):
        for bad in (None, 'not bytes', b'\xef\xbb\xbf' + self.raw(), self.raw().replace(b'\r\n', b'\n'),
                    self.raw().replace(b'synthetic', b'changed', 1), self.raw() + b'\r\n', b'\xff'):
            with self.assertRaises(ValueError):
                with b15.historical_b14_inputs(self.fake(), self.old(), self.texts(), bad):
                    pass

    def test_09_exact_index_keys_strings_and_restore_on_bad_input(self):
        for bad in ({}, self.texts() | {'extra.md': 'x'}, self.texts() | {'PLAN.md': None}):
            f = self.fake()
            before = f.AUDIT, f.read, f.rows
            with self.assertRaises(ValueError):
                with b15.historical_b14_inputs(f, self.old(), bad, self.raw()):
                    pass
            for after, old in zip((f.AUDIT, f.read, f.rows), before):
                self.assertIs(after, old)

    def test_10_fresh_row_copies_and_captured_text_mapping(self):
        f, old, texts = self.fake(), self.old(), self.texts()
        with b15.historical_b14_inputs(f, old, texts, self.raw(old)):
            texts['PLAN.md'] = 'CHANGED-LATER'
            self.assertEqual(f.read(f.AUDIT / 'PLAN.md'), 'FROZEN:PLAN.md')
            first, second = f.rows('findings.csv'), f.rows('findings.csv')
            first[0]['title'] = 'changed'
            self.assertEqual(second[0]['title'], 'synthetic')
            self.assertEqual(old[0]['title'], 'synthetic')
            self.assertIsNot(first, second)
            self.assertIsNot(first[0], second[0])

    def test_11_unrelated_paths_delegate_including_real_audit_tool_read(self):
        f = self.fake()
        with self.context(f):
            self.assertEqual(f.rows('other.csv'), [dict(id='LIVE:other.csv')])
            self.assertEqual(f.read(Path('/elsewhere/README.md')), 'LIVE:/elsewhere/README.md')
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(), Path(__file__).read_bytes())
            with self.assertRaises(FileNotFoundError):
                type(f.AUDIT)('/synthetic/elsewhere/findings.csv').read_bytes()

    def test_12_cores_all_followups_and_exact_declared_tails(self):
        old = self.old(2)
        now = copy.deepcopy(old)
        now[0]['evidence'] += ';b.cs:3-4'
        manifest = [dict(finding_ids=old[0]['id'], evidence='b.cs:3-4')]
        self.assertEqual(b15.registry_transition_errors(old, now, manifest), [])
        for field in ('title', 'severity', 'certainty', 'type', 'status', 'next_phase'):
            bad = copy.deepcopy(now)
            bad[1][field] = 'changed'
            self.assertTrue(any('.' + field in e for e in b15.registry_transition_errors(old, bad, manifest)))
        for bad in ([], manifest * 2, [dict(finding_ids='UNKNOWN', evidence='b.cs:3-4')]):
            self.assertTrue(b15.registry_transition_errors(old, now, bad))
        for value in ('b.cs:3-4', 'a.cs:1-2;b.cs:3-4;c.cs:5-6'):
            bad = copy.deepcopy(now)
            bad[0]['evidence'] = value
            self.assertTrue(b15.registry_transition_errors(old, bad, manifest))

    def test_13_exact164_group_rows_whitespace_order_new_suffix(self):
        old = self.groups()
        self.assertEqual(b15.group_row_errors(old, old + '\nAdditive prose\n| G-165 | new |\n'), [])
        for bad in (old.replace('exact row', 'exact  row', 1), old.replace('| G-01 |', '| G-02 |', 1), self.groups(163)):
            self.assertTrue(b15.group_row_errors(old, bad))
        self.assertTrue(b15.group_row_errors(self.groups(165), old))

    def test_14_reverse_links_exact_not_one_way(self):
        pool = [dict(id='FE-X', acceptance_ids='T1')]
        tests = [dict(id='T1', feature_ids='FE-X'), dict(id='T2', feature_ids='FE-X')]
        self.assertTrue(b15.bidirectional_errors(pool, tests, 'feature_ids'))
        pool[0]['acceptance_ids'] = 'T1;T2'
        self.assertEqual(b15.bidirectional_errors(pool, tests, 'feature_ids'), [])

    def test_15_feature_vocabulary_and_inventory_only_gate(self):
        row = dict(id='FE-X', implementation_status='deferred-not-implementation-reviewed',
                   coverage_level='inventory-only-not-implementation-reviewed', evidence='none-inventory-only')
        self.assertEqual(b15.feature_level_errors([row]), [])
        for bad in (row | {'coverage_level': 'source-reviewed'}, row | {'evidence': 'a.cs:1-2'}, row | {'implementation_status': 'complete'}):
            self.assertTrue(b15.feature_level_errors([bad]))

    def test_16_ledger_union_complement_not_feature_completion(self):
        row = b15.build_current_ledger([self.item()], [('7B14', [self.scope(ranges='2-3')]), ('7B15', [self.scope(ranges='7-8')])], v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'], '2-3;7-8')
        self.assertEqual(row['unselected_text_ranges'], '1-1;4-6;9-10')
        self.assertEqual(row['phase7B15_ranges'], '7-8')
        self.assertIn('not-closed', row['continuation_bucket'])
        self.assertEqual(row['runtime_status'], 'not-executed')

    def test_17_both_parents_require_their_OWN_full_xaml(self):
        for name in b15.REVIEWED_BODIES:
            p = 'SmartAuditERP/Form_WPF/' + name + '.xaml'
            inventory = [self.item(p), self.item(p + '.cs')]
            row = b15.build_screen_disposition(inventory, [('7B15', [self.scope(p, '1-10'), self.scope(p + '.cs', '1-10')])])[0]
            self.assertEqual(row['coverage_level'], 'bounded-local-body-and-xaml-not-whole-feature-certified')
            for selected in ([self.scope(p + '.cs', '1-10')], [self.scope(p, '1-9'), self.scope(p + '.cs', '1-10')]):
                row = b15.build_screen_disposition(inventory, [('7B15', selected)])[0]
                self.assertNotEqual(row['coverage_level'], 'bounded-local-body-and-xaml-not-whole-feature-certified')

    def test_18_parent_or_known_name_does_not_promote_child_or_unselected(self):
        p = 'SmartAuditERP/Form_WPF/frmRptParent.xaml'
        c = 'SmartAuditERP/Form_WPF/frmRptChild.xaml'
        inventory = [self.item(x) for x in (p, p + '.cs', c, c + '.cs')]
        by = {r['screen']: r for r in b15.build_screen_disposition(inventory, [('7B15', [self.scope(p + '.cs', '1-10')])])}
        self.assertEqual(by['frmRptChild']['coverage_level'], 'inventory-only-not-implementation-reviewed')
        p = 'SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml'
        row = b15.build_screen_disposition([self.item(p), self.item(p + '.cs')], [])[0]
        self.assertEqual(row['phase7B15_body_ranges'], 'none')
        self.assertEqual(row['coverage_level'], 'inventory-only-not-implementation-reviewed')

    def test_19_generated_and_FingerPrint_are_not_features(self):
        row = b15.build_current_ledger([self.item('x.dll', '', kind='generated-artifact')], [], v.spans)[0]
        self.assertEqual(row['line_range_state'], 'binary-metadata-not-executed')
        self.assertIn('not-authorized', row['continuation_bucket'])
        row = b15.build_candidate_disposition([self.item('FingerPrintDevice.cs')], [])[0]
        self.assertIn('lexical-false-positive', row['disposition'])

    def test_20_fourB_first_two_residuals_sixC_not_started(self):
        self.assertEqual(b15.remaining_work_errors(self.plan(), self.depth()), [])
        for index, patch in [(0, {'status': 'complete'}), (1, {'status': 'planned-not-started'}),
                             (2, {'status': 'bounded-parent-contract-delivered-residuals-open'}),
                             (4, {'status': 'in-progress'}), (0, {'part_family': '7C'}),
                             (0, {'runtime_status': 'passed'}), (0, {'counts_are_sessions_or_completion_percent': 'true'})]:
            bad = self.plan()
            bad[index] |= patch
            self.assertTrue(b15.remaining_work_errors(bad, self.depth()))
        self.assertTrue(b15.remaining_work_errors(self.plan()[:-1], self.depth()))

    def test_21_remaining_plan_fields_must_be_substantive(self):
        for field in ('id', 'title', 'candidate_scope_not_certified', 'expected_deliverable', 'static_exit_criterion', 'dependencies_and_uncertainty'):
            for value in ('', ' ', None):
                bad = self.plan()
                bad[1][field] = value
                self.assertTrue(b15.remaining_work_errors(bad, self.depth()))
        for invalid in ({'id': None, 'status': 'complete'}, {'id': None, 'runtime_status': 'passed'}):
            bad = self.plan()
            bad[1] |= invalid
            self.assertTrue(b15.remaining_work_errors(bad, self.depth()))

    def test_22_depth_two_already_full_two_upgrades_zero_category_only(self):
        for bad in (self.depth()[:-1], [r | {'prior_full_local_csharp_declared': 'false'} for r in self.depth()],
                    [r | {'b15_full_local_body_and_xaml': 'false'} for r in self.depth()],
                    [r | {'remaining_old_category_after_b15': 'true'} for r in self.depth()]):
            self.assertTrue(b15.remaining_work_errors(self.plan(), bad))
        inventory, old, before, current = [], [], [], []
        for name, prior_phase in zip(b15.REVIEWED_BODIES, ('7A', '7B1')):
            p = 'SmartAuditERP/Form_WPF/' + name + '.xaml'
            inventory += [self.item(p), self.item(p + '.cs')]
            old.append(dict(screen=name, path=p, body_path=p + '.cs', body_inventory_lines='10', coverage_level='prior-selected-slices-depth-not-upgraded'))
            before.append((prior_phase, [self.scope(p + '.cs', '1-10')]))
            current += [self.scope(p, '1-10'), self.scope(p + '.cs', '1-10')]
        original = b15.prior_screens
        try:
            b15.prior_screens = lambda *_: copy.deepcopy(old)
            depth = b15.depth_clarification(inventory, before + [('7B15', current)], v.spans)
            self.assertEqual(b15.remaining_work_errors(self.plan(), depth), [])
            self.assertEqual([r['prior_full_body_scope_ids'] for r in depth], ['7A', '7B1'])
            missing_own = [r for r in current if r['path'] != old[0]['path']]
            depth = b15.depth_clarification(inventory, before + [('7B15', missing_own)], v.spans)
            self.assertEqual(depth[0]['b15_full_local_body_and_xaml'], 'false')
        finally:
            b15.prior_screens = original

    def test_23_strict_false_integer_zero_and_six_true_boundaries(self):
        self.assertEqual(b15.witness_metadata_errors(self.metadata()), [])
        for key in ('application_code_imported_or_executed', 'application_remediation_performed', 'real_business_or_secret_data_used', 'spreadsheet_or_formula_interpreter_executed'):
            for value in (True, None, 0):
                self.assertTrue(b15.witness_metadata_errors(self.metadata() | {key: value}))
        for key in ('erp_runtime_tests_executed', 'sql_or_external_service_tests_executed'):
            for value in (1, False, None, '0'):
                self.assertTrue(b15.witness_metadata_errors(self.metadata() | {key: value}))
        for key in ('parents_csharp_already_full_7A_B1', 'child_selected_slices_not_parent_depth', 'tax_home_route_is_alternate_not_parent_certified', 'B_R1_R2_residual_contracts_not_closed', 'supplied_sql_not_certified_deployed', 'progress_categories_not_wholly_unread_counts'):
            for value in (False, None, 1, 'true'):
                self.assertTrue(b15.witness_metadata_errors(self.metadata() | {key: value}))

    def test_24_counts_phase_parent_accounting_and_additive_erratum(self):
        for patch in ({'phase': 'ERP-certified'}, {'illustration_count': 23}, {'illustration_count': 24.0},
                      {'static_lexical_contract_check_count': True}, {'parent_source_lines_not_first_coverage': dict(csharp=1876, xaml=1441, total=9999)},
                      {'retained_additive_B10_arithmetic_erratum': self.erratum() | {'local_cost': 20}},
                      {'retained_additive_B10_arithmetic_erratum': self.erratum() | {'archive_rewritten': 0}}):
            self.assertTrue(b15.witness_metadata_errors(self.metadata() | patch))

    def test_25_exact36_plan_kinds_order_and_not_executed(self):
        tests, ids, ext = self.acceptance()
        self.assertEqual(b15.plan_structure_errors(tests, ids, ext), [])
        for bad in (tests[:-1], [tests[8]] + tests[:8] + tests[9:], [r | {'status': 'passed'} if i == 35 else r for i, r in enumerate(tests)]):
            self.assertTrue(b15.plan_structure_errors(bad, ids, ext))
        self.assertTrue(b15.plan_structure_errors(tests, ids, list(reversed(ext))))

    def test_26_two_direct_plans_per_unique_root_and_exact_mapping(self):
        tests, ids, ext = self.acceptance()
        for patch in ({'finding_ids': 'P7-124'}, {'feature_ids': 'FE7B15-02'}, {'invariant_ids': 'INV7B15-02'}):
            bad = copy.deepcopy(tests)
            bad[0] |= patch
            self.assertTrue(b15.plan_structure_errors(bad, ids, ext))
        self.assertTrue(b15.plan_structure_errors(tests, ids[:3], ext))
        self.assertTrue(b15.plan_structure_errors(tests, [ids[0]] * 4, ext))

    def test_27_adjudication_four_new_local_roots_and_limited_depth(self):
        data = self.adjudication()
        self.assertEqual(b15.adjudication_errors(data), [])
        for bad in (data[:-1], [r | {'decision': 'repeat'} if i == 0 else r for i, r in enumerate(data)],
                    [r | {'current_root_ids': 'P7-999'} if i == 2 else r for i, r in enumerate(data)],
                    [r | {'comparison_depth': 'all-historical-chains-certified'} for r in data]):
            self.assertTrue(b15.adjudication_errors(bad))

    def test_28_adjudication_nearest_roots_reasons_and_no_runtime_claim(self):
        for patch in ({'nearest_prior_root_ids': ''}, {'reason': ''}, {'reason': ' '}, {'reason': None}, {'runtime_status': 'passed'}):
            data = self.adjudication()
            data[0] |= patch
            self.assertTrue(b15.adjudication_errors(data))

    def test_29_inventory_sentinels_no_fabrication_and_real_evidence_dispatch(self):
        errors, calls = [], []
        fake = SimpleNamespace(check=lambda ok, msg: errors.append(msg) if not ok else None,
                               evidence=lambda *a: calls.append(('evidence', a)),
                               scoped_evidence=lambda *a, **k: calls.append(('scoped', a, k)))
        for name in ('RC7B15-06', 'ALG7B15-24', 'AD7B15-10'):
            b15.validate_source(fake, dict(id=name, evidence='none-inventory-only'), {})
        self.assertEqual(errors, [])
        self.assertEqual(calls, [])
        scope = {'a.cs': [(1, 2)]}
        b15.validate_source(fake, dict(id='FE7B15-01', evidence='a.cs:1-2'), scope)
        self.assertEqual(calls[0], ('evidence', ('a.cs:1-2', 'FE7B15-01')))
        self.assertEqual(calls[1][1][1], scope)
        self.assertEqual(calls[1][2], dict(phase=7))
        b15.validate_source(fake, dict(id='RC7B15-06', evidence='a.cs:1-2'), scope)
        b15.validate_source(fake, dict(id='UNDECLARED', evidence='none-inventory-only'), scope)
        self.assertEqual(len(errors), 2)

    def test_30_builders_are_pure_not_source_or_execution_coverage(self):
        inventory = [self.item('frmRptSynthetic.cs')]
        labelled = [('7B15', [self.scope('frmRptSynthetic.cs', '1-10')])]
        before = copy.deepcopy((inventory, labelled))
        b15.build_current_ledger(inventory, labelled, v.spans)
        b15.build_candidate_disposition(inventory, labelled)
        b15.build_screen_disposition(inventory, labelled)
        self.assertEqual((inventory, labelled), before)

    def test_31_exact_tables22_extensions_and_no_potential_promotion(self):
        counts = {name: count for name, _, count in b15.TABLE_SPECS}
        self.assertEqual((counts['acceptance-tests'], counts['feature-implementation-matrix'], counts['root-adjudication']), (36, 32, 10))
        self.assertEqual(len(b15.EXTENDED_FINDINGS), 22)
        self.assertTrue({'P7-001', 'P7-002', 'P7-003', 'P7-043', 'P7-044', 'P7-045', 'P7-046', 'P7-051', 'P3-003', 'P3-005'} <= b15.EXTENDED_FINDINGS)
        self.assertTrue({'P7-123', 'P7-124', 'P7-125', 'P7-126', 'P7-049', 'P7-108', 'P4-007', 'P7-095', 'P7-109'}.isdisjoint(b15.EXTENDED_FINDINGS))

    def test_32_same_resolved_path_only_and_retained_main_default_B15(self):
        f = self.fake()
        before = Path.read_bytes
        with self.context(f):
            self.assertEqual((f.AUDIT / 'unused' / '..' / 'findings.csv').read_bytes(), self.raw())
            self.assertIs(Path.read_bytes, before)
            self.assertEqual(f.rows('unrelated/findings.csv'), [dict(id='LIVE:unrelated/findings.csv')])
        self.assertEqual(v.main.__defaults__, ('B15',))


if __name__ == '__main__':
    unittest.main()
