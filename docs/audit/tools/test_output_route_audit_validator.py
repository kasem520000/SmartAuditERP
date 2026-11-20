#!/usr/bin/env python3
"""52 B33 documentary checker cases,NOT32 acceptance plans or ERP/device tests.

All1086 earlier cases,including52 B32,are unmodified. Schema fixtures in this
file are NOT subprocess/history execution evidence. Source assertions119 for
B32 remain distinct from actual current123 tools/parser/19 routing gates.
"""
from __future__ import annotations

import ast
import copy
import csv
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
import validate_output_route_part as b33
from check_output_route_witnesses import (
    SOURCE_SLICES, EXPLORATORY_SLICES, PDF, caller_allows, wrapper, engine,
)
A = Path(__file__).resolve().parents[1]


class OutputRouteAuditTests(unittest.TestCase):
    def old(self):
        return [dict(id=f'PX-{n:03d}', severity='Medium', certainty='potential',
                     type='synthetic-only', status='open-not-remediated', title='fixture-title',
                     evidence='a.cs:1-2', next_phase='7;8') for n in range(334)]

    def current(self):
        return self.old() + [self.old()[0] | dict(id='P7-163', next_phase='8')]

    def raw(self, data):
        out = io.StringIO(newline='')
        w = csv.DictWriter(out, fieldnames=list(data[0]), lineterminator='\r\n')
        w.writeheader()
        w.writerows(data)
        return out.getvalue().encode()

    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'), read=lambda p: 'LIVE:' + str(p),
                               rows=lambda n: [dict(id='LIVE:' + n)])

    def texts(self):
        return {n: 'FROZEN:' + n for n in b33.SHARED_DOCS}

    def sources(self):
        raw = b'# fixture historical dispatcher TEXT,not executed\n'
        return ({'tools/validate_audit.py': hashlib.sha256(raw).hexdigest()}
                | {f'tools/fixture_{n:03d}.py': 'a' * 64 for n in range(118)}), raw

    def context(self, f):
        return b33.historical_b32_inputs(f, self.old(), self.texts(), self.raw(self.old()), *self.sources())

    def table(self, stem, part=33):
        with (A / 'evidence' / f'{stem}-07B{part}.csv').open(encoding='utf8', newline='') as f:
            return list(csv.DictReader(f))

    def groups(self, n):
        return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1, n + 1)) + '\n'

    def witness(self):
        return json.loads((A / 'evidence/output-route-witnesses-07B33.json').read_bytes())

    def history_fixture(self):
        modes = copy.deepcopy(json.loads((A / 'evidence/historical-mode-verification-07B32.json').read_bytes())['historical_modes'])
        child = dict(tests_reported=52, expected_tests=52, process_exit_code=0, result='passed',
            historical_parser_cutoff='B32-not-current-B33-default', all_original_cases_executed_unmodified=True,
            dedicated_child_launcher='tools/run_historical_editor_close_tests_07B33.py',
            no_test_skips_or_global_subprocess_or_path_patch=True,
            suite_own_registry_path_is_context_local_not_global=True,
            test_module_Path_and_A_are_historical_assertion_inputs_only=True,
            historical_source_assertion_input_count=119, auxiliary_dispatcher_text_sha256=b33.DISPATCHER_SHA,
            historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B32', findings_total=334, registry_used=b33.SNAPSHOT,
            process_exit_code=0, validation_errors=[], original_project_hashes_matching=827,
            audit_checker_self_test_cases_reported=1086, audit_checker_self_test_suite_count=33,
            erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0,
            stdout_sha256='a' * 64, historical_B32_child=child))
        return dict(historical_mode_count=38, historical_modes=modes, errors=[])

    def test_01_OWN334_raw335_readbytes_readtext_AND_open(self):
        f = self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'), self.old())
            self.assertEqual((f.AUDIT / 'findings.csv').read_bytes(), self.raw(self.old()))
            for mode in ('r', 'rt'):
                with (f.AUDIT / 'findings.csv').open(mode, encoding='utf8', newline='') as stream:
                    self.assertEqual(list(csv.DictReader(stream)), self.old())
            with (f.AUDIT / 'findings.csv').open('rb') as stream:
                self.assertEqual(stream.read(), self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT / 'README.md'), 'FROZEN:README.md')

    def test_02_reject_malformed_OWN_rows_raw_indexes_source_TEXT(self):
        old, raw, src = self.old(), self.raw(self.old()), self.sources()
        bad_inputs = ((old[:-1], self.texts(), raw, *src),
            (old, self.texts(), raw.replace(b'\r\n', b'\n'), *src),
            (old, self.texts(), b'\xef\xbb\xbf' + raw, *src),
            (old, self.texts(), bytearray(raw), *src), (old, {'README.md': 'only'}, raw, *src),
            (old, self.texts(), raw, {}, src[1]), (old, self.texts(), raw, src[0], src[1] + b'x'))
        for args in bad_inputs:
            with self.assertRaises(ValueError):
                with b33.historical_b32_inputs(self.fake(), *args):
                    pass
        old[0]['id'] = old[1]['id']
        with self.assertRaises(ValueError):
            with b33.historical_b32_inputs(self.fake(), old, self.texts(), self.raw(old), *src):
                pass

    def test_03_context_fresh_rows_nested_and_exception_restore(self):
        f = self.fake()
        before = f.AUDIT, f.read, f.rows
        with self.context(f):
            current = f.AUDIT
            changed = f.rows('findings.csv')
            changed[0]['title'] = 'changed'
            self.assertEqual(f.rows('findings.csv'), self.old())
            with self.context(f):
                self.assertEqual(len(f.rows('findings.csv')), 334)
            self.assertIs(f.AUDIT, current)
        with self.assertRaises(RuntimeError):
            with self.context(f):
                raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x, y in zip(before, (f.AUDIT, f.read, f.rows))))

    def test_04_canonical_local_Path_and_readonly_open_not_global(self):
        f = self.fake()
        original = Path.read_bytes, Path.read_text, Path.glob, Path.open
        src, raw = self.sources()
        with self.context(f):
            self.assertEqual((Path.read_bytes, Path.read_text, Path.glob, Path.open), original)
            self.assertEqual(len(list((f.AUDIT / 'tools').glob('*.py'))), 119)
            p = f.AUDIT / 'tools/validate_audit.py'
            self.assertEqual(p.read_bytes(), raw)
            with p.open('rb') as stream:
                self.assertEqual(stream.read(), raw)
            for mode in ('w', 'a', 'r+', 'wb'):
                with self.assertRaises(ValueError):
                    p.open(mode)
            self.assertEqual(p.resolve(), Path('/synthetic/audit/tools/validate_audit.py'))
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(), Path(__file__).read_bytes())
            self.assertEqual(f.rows('other/findings.csv'), [dict(id='LIVE:other/findings.csv')])

    def test_05_exact_list_argv_proxy_not_shared_subprocess(self):
        calls = []
        backend = SimpleNamespace(run=lambda *a, **k: calls.append((a, k)) or 'ok')
        proxy = b33.HistoricalB32Subprocess(backend, 'python', Path('/a/tools'))
        kw = dict(cwd='/a', timeout=60, capture_output=True, text=True)
        self.assertEqual(proxy.run(list(proxy.expected), **kw), 'ok')
        self.assertEqual(calls[-1], ((proxy.actual,), kw))
        for args in (tuple(proxy.expected), proxy.expected + ['--other'], ['python', '-B', '/other/test.py']):
            proxy.run(args, **kw)
            self.assertEqual(calls[-1], ((args,), kw))
        f = self.fake()
        f.subprocess, f.sys = backend, SimpleNamespace(executable='python')
        view = b33.HistoricalB32ValidatorView(f)
        original = subprocess.run
        with self.context(view):
            self.assertIs(subprocess.run, original)
            self.assertIs(f.subprocess, backend)

    def test_06_ALL334_dictionaries_every_field(self):
        old, cur = self.old(), self.current()
        self.assertEqual(b33.registry_preservation_errors(old, cur, self.raw(cur), self.raw(old), []), [])
        for n in (0, 330, 331, 332, 333):
            for key in old[n]:
                bad = copy.deepcopy(cur)
                bad[n][key] = 'changed'
                self.assertTrue(b33.registry_preservation_errors(old, bad, self.raw(bad), self.raw(old), []), (n, key))

    def test_07_entire_raw335_prefix_CRLF_noBOM(self):
        old, cur = self.old(), self.current()
        raw, frozen = self.raw(cur), self.raw(old)
        self.assertTrue(raw.startswith(frozen))
        for bad in (raw.replace(b'\r\n', b'\n'), b'\xef\xbb\xbf' + raw, raw[:-2], raw.replace(b'fixture-title', b'other', 1)):
            self.assertTrue(b33.registry_preservation_errors(old, cur, bad, frozen, []))

    def test_08_one163_no_extensions_or_per_route_recount(self):
        old, cur = self.old(), self.current()
        for bad in (cur[:-1], cur + [dict(cur[-1])], cur[:-1] + [cur[-1] | dict(id='P7-164')]):
            self.assertTrue(b33.registry_preservation_errors(old, bad, self.raw(bad), self.raw(old), []))
        self.assertTrue(b33.registry_preservation_errors(old, cur, self.raw(cur), self.raw(old), [dict(finding_id='P7-031')]))

    def test_09_G248_exact_only249_to252(self):
        self.assertEqual(b33.group_row_errors(self.groups(248), self.groups(252)), [])
        for bad in (self.groups(251), self.groups(253), self.groups(252).replace('| G-01 | exact', '| G-01 | changed'), self.groups(252).replace('G-248', 'G-247')):
            self.assertTrue(b33.group_row_errors(self.groups(248), bad))

    def test_10_documentary_sentinels_never_fabricated_source(self):
        errors, calls = [], []
        f = SimpleNamespace(check=lambda ok, msg: errors.append(msg) if not ok else None,
            evidence=lambda *a: calls.append(a), scoped_evidence=lambda *a, **kw: calls.append((a, kw)))
        for name in ('FE7B33-15', 'OS7B33-08', 'OV7B33-08', 'AD7B33-08'):
            b33.validate_source(f, dict(id=name, evidence=b33.DOCUMENTARY), {})
        self.assertEqual((errors, calls), ([], []))
        b33.validate_source(f, dict(id='UNKNOWN', evidence=b33.DOCUMENTARY), {})
        b33.validate_source(f, dict(id='FE7B33-15', evidence='a.cs:1-2'), {})
        self.assertEqual(len(errors), 2)
        self.assertEqual(b33.source_evidence_union([dict(evidence='a.cs:1-2;3'), dict(evidence='a.cs:1-2;5')]), 'a.cs:1-2;a.cs:3;a.cs:5')

    def test_11_OS8_OV8_order_and_exact_feature_source_unions(self):
        data = self.table('output-state-lineage'), self.table('route-override-lineage')
        fe = self.table('feature-implementation-matrix')
        self.assertEqual(b33.ledger_errors(*data, fe), [])
        for pool in (0, 1):
            bad = copy.deepcopy(data)
            bad[pool][0], bad[pool][1] = bad[pool][1], bad[pool][0]
            self.assertTrue(b33.ledger_errors(*bad, fe))
            for key in ('feature_ids', 'finding_ids', 'evidence', 'source_to_output', 'boundary'):
                bad = copy.deepcopy(data)
                bad[pool][0][key] = 'changed'
                self.assertTrue(b33.ledger_errors(*bad, fe), key)

    def test_12_lineage_responsibility_and_nonexecution(self):
        data = self.table('output-state-lineage'), self.table('route-override-lineage')
        fe = self.table('feature-implementation-matrix')
        for key in ('source_to_output', 'owner_role', 'required_redacted_input', 'impact_if_unavailable',
                    'next_step', 'limit', 'feature_ids', 'finding_ids', 'evidence', 'observation'):
            bad = copy.deepcopy(data)
            bad[1][0][key] = ''
            self.assertTrue(b33.ledger_errors(*bad, fe), key)
        bad = copy.deepcopy(data)
        bad[0][0]['runtime_status'] = 'passed'
        self.assertTrue(b33.ledger_errors(*bad, fe))

    def test_13_FE16_INV16_T32_exact_bidirectional_links(self):
        data = [self.table(n) for n in ('feature-implementation-matrix', 'report-invariants', 'acceptance-tests')]
        self.assertEqual(b33.current_link_errors(*data), [])
        for pool, key in ((0, 'acceptance_ids'), (1, 'feature_ids'), (1, 'finding_ids'), (2, 'feature_ids'), (2, 'status'), (2, 'finding_ids')):
            bad = copy.deepcopy(data)
            bad[pool][0][key] = 'changed'
            self.assertTrue(b33.current_link_errors(*bad))

    def test_14_entry_source_output_exclusion_and_distinct_plans(self):
        data = [self.table(n) for n in ('feature-implementation-matrix', 'report-invariants', 'acceptance-tests')]
        for key in ('owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step',
                    'limit', 'entry_point', 'source_contract', 'output_boundary', 'excluded_from_claim'):
            bad = copy.deepcopy(data)
            bad[0][0][key] = ''
            self.assertTrue(b33.current_link_errors(*bad), key)
        for pool, key in ((1, 'required_invariant'), (2, 'acceptance_criterion')):
            bad = copy.deepcopy(data)
            bad[pool][1][key] = bad[pool][0][key]
            self.assertTrue(b33.current_link_errors(*bad))

    def test_15_RS14_ancestry_SHA_contracts(self):
        old, new = self.table('residual-disposition', 32), self.table('residual-disposition')
        self.assertEqual(b33.residual_errors(new, old), [])
        for key in ('upstream_residual_id', 'upstream_artifact', 'upstream_row_sha256', 'upstream_contract_ids'):
            bad = copy.deepcopy(new)
            bad[0][key] = 'changed'
            self.assertTrue(b33.residual_errors(bad, old))

    def test_16_ALL_old_inputs_routes_dispositions_not_replaced(self):
        old, new = self.table('residual-disposition', 32), self.table('residual-disposition')
        for key, val in (('required_redacted_input', 'only new'), ('current_handoff_or_split_ids', 'H7B33-01'),
                         ('disposition', 'approved'), ('runtime_status', 'passed'), ('local_result', '')):
            bad = copy.deepcopy(new)
            bad[2][key] = val
            self.assertTrue(b33.residual_errors(bad, old))
        self.assertTrue(b33.residual_errors(new[:-1], old))

    def test_17_SP3_full_input_prefix_and_future_status(self):
        old, new = self.table('split-register', 32), self.table('split-register')
        self.assertEqual(b33.split_errors(new, old), [])
        for key in ('upstream_split_id', 'upstream_artifact', 'upstream_row_sha256', 'required_input', 'reason_for_split', 'status', 'runtime_status'):
            bad = copy.deepcopy(new)
            bad[0][key] = 'changed' if key != 'reason_for_split' else ''
            self.assertTrue(b33.split_errors(bad, old))

    def test_18_RW_fourB_sixC_and_BK_ancestry(self):
        work = self.table('remaining-workplan')
        self.assertEqual(b33.remaining_work_errors(work), [])
        for n, key, val in ((3, 'status', 'complete'), (4, 'status', 'started'), (0, 'part_family', '7C'),
                            (0, 'runtime_status', 'passed'), (0, 'counts_are_sessions_or_completion_percent', 'true')):
            bad = copy.deepcopy(work)
            bad[n][key] = val
            self.assertTrue(b33.remaining_work_errors(bad))
        for n, r in enumerate(self.table('continuation-backlog'), 1):
            self.assertEqual((r['prior_backlog_id'], r['original_backlog_id']), (f'BK7B32-{n:02d}', f'BK7-{n:02d}'))
            self.assertNotEqual(r['status'], 'complete')

    def test_19_witness_strict_bools_counts_B10_no_runtime(self):
        w = self.witness()
        self.assertEqual(b33.witness_metadata_errors(w), [])
        for key in ('installed_printer_or_PDF_file_or_paper_output_proved', 'persisted_setting_write_or_financial_loss_claimed', 'application_code_imported_or_executed'):
            for val in (True, 0):
                self.assertTrue(b33.witness_metadata_errors(w | {key: val}))
        for key in ('illustration_count', 'selected_contract_slices', 'context_slices_not_certified', 'erp_runtime_tests_executed'):
            self.assertTrue(b33.witness_metadata_errors(w | {key: True}))
        bad = copy.deepcopy(w)
        bad['retained_additive_B10_arithmetic_erratum']['local_cost'] = 20
        self.assertTrue(b33.witness_metadata_errors(bad))

    def test_20_witness_exact_bytes_recomputed_in_real_process(self):
        raw = (A / 'evidence/output-route-witnesses-07B33.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), b33.WITNESS_SHA)
        run = subprocess.run([sys.executable, '-B', str(A / 'tools/check_output_route_witnesses.py')], capture_output=True, timeout=20)
        self.assertEqual((run.returncode, run.stderr, run.stdout), (0, b'', raw))
        self.assertTrue(all(r['illustration_assertions_passed'] is True and r['source_application_executed'] is False for r in self.witness()['illustrations']))

    def test_21_printed_clean_caller_gate_SUPPLIED_not_DTO_proof(self):
        for printed in (False, True):
            for dirty in (False, True):
                self.assertIs(caller_allows(printed, dirty), printed and not dirty)
        for args in ((1, False), (True, 0), (None, False)):
            with self.assertRaises(ValueError):
                caller_allows(*args)

    def test_22_PDF_then_normal_same_instance_carries_property(self):
        pdf = wrapper('fixture-paper-A', 'pdf')
        normal = wrapper(pdf['shared_after'], 'normal')
        self.assertEqual((pdf['shared_after'], normal['engine_printer_argument']), (PDF, PDF))
        self.assertFalse(pdf['actual_output_proved'])
        self.assertFalse(normal['engine_or_application_executed'])

    def test_23_normal_without_PDF_negative_control(self):
        t = wrapper('fixture-paper-A', 'normal')
        self.assertEqual((t['shared_before'], t['shared_after'], t['engine_printer_argument']), ('fixture-paper-A',) * 3)
        self.assertTrue(t['engine_entered'])

    def test_24_instance_A_does_not_mutate_supplied_B(self):
        initial_a, initial_b = 'fixture-paper-A', 'fixture-paper-B'
        a = wrapper(initial_a, 'pdf')
        b = wrapper(initial_b, 'normal')
        self.assertEqual(a['shared_after'], PDF)
        self.assertEqual(b['shared_after'], initial_b)
        self.assertEqual(initial_a, 'fixture-paper-A')

    def test_25_empty_grid_before_PDF_assignment(self):
        t = wrapper('fixture-paper-A', 'pdf', rows=0)
        self.assertEqual(t['shared_after'], 'fixture-paper-A')
        self.assertEqual(t['stopped_before_assignment'], 'empty-grid')
        self.assertFalse(t['engine_entered'])

    def test_26_missing_url_or_main_report_before_PDF_assignment(self):
        for kwargs, gate in ((dict(url=False), 'missing-url'), (dict(report=False), 'missing-main-report')):
            t = wrapper('fixture-paper-A', 'pdf', **kwargs)
            self.assertEqual(t['stopped_before_assignment'], gate)
            self.assertEqual(t['shared_after'], 'fixture-paper-A')
            self.assertFalse(t['assignment_boundary_reached'])

    def test_27_binding_nonreturn_AFTER_property_write_not_engine_success(self):
        t = wrapper('fixture-paper-A', 'pdf', bind_returns=False)
        self.assertEqual(t['shared_after'], PDF)
        self.assertTrue(t['binding_nonreturn_after_assignment'])
        self.assertFalse(t['engine_entered'])
        self.assertIsNone(t['engine_printer_argument'])
        self.assertEqual(wrapper(t['shared_after'], 'normal')['engine_printer_argument'], PDF)

    def test_28_empty_normal_property_uses_supplied_fallback(self):
        self.assertEqual(wrapper('', 'normal', default_printer='fixture-default')['engine_printer_argument'], 'fixture-default')
        self.assertEqual(wrapper('', 'normal', default_printer='')['engine_printer_argument'], '')

    def test_29_nonempty_property_does_NOT_use_changed_default(self):
        for printer in (PDF, 'fixture-paper-A'):
            t = wrapper(printer, 'normal', default_printer='fixture-changed')
            self.assertEqual(t['shared_after'], printer)
            self.assertEqual(t['engine_printer_argument'], printer)

    def test_30_picker_overrides_local_not_callers_property(self):
        state = wrapper('fixture-paper-A', 'pdf')['shared_after']
        t = engine(state, picker='fixture-picker')
        self.assertEqual(t['report_printer_assignment'], 'fixture-picker')
        self.assertFalse(t['shared_property_written_by_this_engine'])
        self.assertEqual(state, PDF)
        self.assertEqual(wrapper(state, 'normal')['engine_printer_argument'], PDF)

    def test_31_empty_picker_does_not_override_or_imply_cancel(self):
        t = engine(PDF, picker='')
        self.assertEqual(t['report_printer_assignment'], PDF)
        self.assertEqual(t['selected_branch_print_requests'], 1)
        self.assertFalse(t['normal_void_return_proves_output_success'])

    def test_32_type3_template_overrides_picker_only_locally(self):
        t = engine(PDF, output_type=3, picker='fixture-picker', template_printer='fixture-template')
        self.assertEqual(t['report_printer_assignment'], 'fixture-template')
        self.assertFalse(t['shared_property_written_by_this_engine'])
        self.assertEqual(engine(PDF, output_type=3)['report_printer_assignment'], PDF)

    def test_33_type1_ignores_type3_template_control(self):
        self.assertEqual(engine(PDF, output_type=1, template_printer='fixture-template')['report_printer_assignment'], PDF)
        self.assertEqual(engine(PDF, output_type=1, picker='fixture-picker', template_printer='fixture-template')['report_printer_assignment'], 'fixture-picker')

    def test_34_type2_preview_is_not_paper_or_PDF_success(self):
        t = engine(PDF, output_type=2, copies=3, kitchen='fixture-kitchen')
        self.assertEqual((t['selected_branch_print_requests'], t['selected_branch_preview_requests']), (0, 1))
        self.assertFalse(t['kitchen_recursion_boundary'])
        self.assertFalse(t['normal_void_return_proves_output_success'])

    def test_35_template_failure_does_not_restore_property(self):
        state = wrapper('fixture-paper-A', 'pdf')['shared_after']
        t = engine(state, failure='template')
        self.assertIsNone(t['report_printer_assignment'])
        self.assertEqual(t['selected_branch_print_requests'], 0)
        self.assertFalse(t['shared_property_written_by_this_engine'])
        self.assertEqual(state, PDF)

    def test_36_first_output_failure_stops_copy_loop_and_kitchen(self):
        t = engine(PDF, copies=3, kitchen='fixture-kitchen', failure='output')
        self.assertEqual(t['selected_branch_print_requests'], 1)
        self.assertFalse(t['kitchen_recursion_boundary'])
        self.assertFalse(t['normal_void_return_proves_output_success'])
        self.assertFalse(t['shared_property_written_by_this_engine'])

    def test_37_zero_negative_copy_fallthrough_is_existing030(self):
        for copies, count in ((-2, 1), (-1, 1), (0, 1), (1, 1), (3, 3), (20, 20)):
            t = engine(PDF, copies=copies)
            self.assertEqual(t['selected_branch_print_requests'], count)
            self.assertTrue(t['requests_not_successful_or_spooled_copies'])
        self.assertEqual(self.witness()['illustrations'][18]['finding_ids'], 'P7-030')

    def test_38_kitchen_is_separate_request_not_inferred_extra_sheets(self):
        t = engine(PDF, copies=2, kitchen='fixture-kitchen')
        self.assertTrue(t['kitchen_recursion_boundary'])
        self.assertEqual(t['selected_branch_print_requests'], 2)
        for kwargs in (dict(copies=0), dict(output_type=2), dict(output_type=3), dict(failure='template')):
            self.assertFalse(engine(PDF, kitchen='fixture-kitchen', **kwargs)['kitchen_recursion_boundary'])

    def test_39_wrapper_strict_inputs_not_inferred_SDK_or_file_checks(self):
        for kwargs in (dict(rows=True), dict(rows=-1), dict(rows=1001), dict(rows='1'),
                       dict(url=1), dict(report=None), dict(bind_returns=0), dict(default_printer=1)):
            with self.assertRaises(ValueError):
                wrapper('fixture-paper-A', 'pdf', **kwargs)
        for printer, mode in ((None, 'pdf'), ('x' * 81, 'pdf'), ('x\n', 'normal'), ('x', 'email'), ('x', 1)):
            with self.assertRaises(ValueError):
                wrapper(printer, mode)

    def test_40_engine_strict_types_bounded_tokens_and_supplied_failure(self):
        for kwargs in (dict(output_type=True), dict(output_type=0), dict(output_type=4), dict(copies=True),
                       dict(copies=21), dict(copies=-3), dict(picker=None), dict(template_printer=1),
                       dict(kitchen='x\n'), dict(failure='measured'), dict(failure=1)):
            with self.assertRaises(ValueError):
                engine(PDF, **kwargs)
        for printer in (None, 'x' * 81, 'x\r'):
            with self.assertRaises(ValueError):
                engine(printer)

    def test_41_ACTUAL_LIVE33_versioned32_API15_parser(self):
        self.assertEqual(v.main.__defaults__, ('B15',))
        self.assertEqual(v.PHASE7_B32_CLI['default'], 'B32')
        self.assertEqual(v.PHASE7_LIVE_CLI['default'], 'B33')
        parser = v.build_cli_parser()
        self.assertEqual(parser.parse_args([]).phase7_part, 'B33')
        for part in ('A',) + tuple(f'B{i}' for i in range(1, 34)):
            self.assertEqual(parser.parse_args(['--phase7-part', part]).phase7_part, part)
        for n in range(18, 33):
            self.assertEqual(getattr(v, f'PHASE7_B{n}_CLI')['default'], f'B{n}')

    def test_42_ACTUAL_19_AST_gates_B32_history_before_current(self):
        self.assertEqual(Path(v.__file__).resolve(), (A / 'tools/validate_audit.py').resolve())
        live = Path(v.__file__).read_bytes()
        self.assertNotEqual(hashlib.sha256(live).hexdigest(), b33.DISPATCHER_SHA)
        tree = ast.parse(live)
        main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
        body = ast.unparse(main)
        self.assertLess(body.index('historical_b31_validation('), body.index('historical_b32_validation('))
        self.assertLess(body.index('historical_b32_validation('), body.index('extend_output_route('))
        self.assertIn('extend_editor_close(historical_b32,', body)
        actual = [set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main)
            if isinstance(n, ast.If) and isinstance(n.test, ast.Compare) and len(n.test.ops) == 1
            and isinstance(n.test.ops[0], ast.In) and isinstance(n.test.left, ast.Name) and n.test.left.id == 'phase7_part']
        expected = [{f'B{i}' for i in range(first, 34)} for first in range(1, 20)]
        self.assertEqual(actual, expected)
        for n in range(19):
            mutant = copy.deepcopy(actual)
            mutant[n].remove('B33')
            with self.assertRaises(AssertionError):
                self.assertEqual(mutant, expected)
        block = next(n for n in tree.body if isinstance(n, ast.If) and ast.unparse(n.test) == "__name__ == '__main__'")
        self.assertIn('build_cli_parser().parse_args()', ast.unparse(block))

    def test_43_ALL52_launcher_module_local_restore_no_old_code(self):
        src = ast.unparse(ast.parse((A / 'tools/run_historical_editor_close_tests_07B33.py').read_text()))
        for token in ('suite.countTestCases() != 52', 'run.testsRun != 52 or run.skipped',
            'loadTestsFromModule(historical_tests)', 'historical_tests.A = v.AUDIT',
            'historical_tests.Path = type(v.AUDIT)', 'historical_tests.A = original_a',
            'historical_tests.Path = original_path', 'v.PHASE7_LIVE_CLI = original_preset',
            'v.PHASE7_B32_CLI', 'b33.historical_b32_inputs('):
            self.assertIn(token, src)
        for token in ('unittest.skip', 'v.__file__ =', 'Path.read_bytes =', 'Path.open =', 'exec('):
            self.assertNotIn(token, src)

    def test_44_historical119_assertion_inputs_distinct_current123(self):
        prov = json.loads((A / 'evidence/provenance-07B33.json').read_bytes())
        self.assertEqual(len(prov['historical_checker_sources_at_entry']), 119)
        self.assertEqual(len(list((A / 'tools').glob('*.py'))), 123)
        raw = (A / b33.SNAPSHOT).read_bytes()
        old = list(csv.DictReader(io.StringIO(raw.decode(), newline='')))
        texts = json.loads((A / b33.SHARED_SNAPSHOT).read_bytes())['files']
        before = v.AUDIT, v.read, v.rows
        code, file = v.main.__code__, v.__file__
        methods = Path.read_bytes, Path.read_text, Path.glob, Path.open
        with b33.historical_b32_inputs(v, old, texts, raw, prov['historical_checker_sources_at_entry'], (A / b33.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT / 'tools').glob('*.py'))), 119)
            self.assertEqual(hashlib.sha256(type(v.AUDIT)(v.__file__).read_bytes()).hexdigest(), b33.DISPATCHER_SHA)
            with (v.AUDIT / 'findings.csv').open(newline='') as stream:
                self.assertEqual(list(csv.DictReader(stream)), old)
            self.assertEqual((Path.read_bytes, Path.read_text, Path.glob, Path.open), methods)
            self.assertIs(v.main.__code__, code)
            self.assertEqual(v.__file__, file)
        self.assertTrue(all(x is y for x, y in zip(before, (v.AUDIT, v.read, v.rows))))

    def test_45_protected976_ALL334_fullraw_and_potential_roots(self):
        prov = json.loads((A / 'evidence/provenance-07B33.json').read_bytes())
        self.assertEqual(len(prov['historical_artifact_sha256']), 976)
        self.assertTrue(all(hashlib.sha256((A / n).read_bytes()).hexdigest() == h for n, h in prov['historical_artifact_sha256'].items()))
        raw, cur = (A / b33.SNAPSHOT).read_bytes(), (A / 'findings.csv').read_bytes()
        old = list(csv.DictReader(io.StringIO(raw.decode(), newline='')))
        now = list(csv.DictReader(io.StringIO(cur.decode(), newline='')))
        self.assertEqual(b33.registry_preservation_errors(old, now, cur, raw, self.table('historical-extensions')), [])
        for root in ('P4-014', 'P7-132', 'P7-145'):
            self.assertEqual(next(r for r in now if r['id'] == root)['certainty'], 'potential')

    def test_46_scope6_overlap6_union427_reads20_context9_dedup24(self):
        decision = json.loads((A / 'evidence/scope-decision-07B33.json').read_bytes())
        self.assertEqual(tuple(decision['bookkeeping'][k] for k in ('selected_paths', 'prior_union', 'overlap', 'new', 'union', 'complement')), (6, 427, 6, 0, 427, 400))
        self.assertEqual((decision['historical_metadata_screen_count'], decision['parent_path_matched_metadata_rows'], decision['selected_contract_slices'], decision['exploratory_context_slices']), (334, 37, 20, 9))
        self.assertFalse(decision['all_historical_bodies_reviewed'])
        w = self.witness()
        self.assertEqual(w['whole_local_files_selected'], 0)
        for key, declared in (('bounded_source_reads_not_semantic_coverage', SOURCE_SLICES),
                              ('exploratory_source_reads_not_capability_certification', EXPLORATORY_SLICES)):
            tuples = []
            for r in w[key]:
                raw = (A.parents[1] / r['path']).read_bytes()
                self.assertEqual(hashlib.sha256(raw).hexdigest(), r['sha256'])
                self.assertFalse(r['whole_local_file_selected'])
                self.assertLessEqual(r['end'], len(raw.decode().splitlines()))
                tuples.append((r['path'], r['start'], r['end']))
            self.assertEqual(tuple(tuples), declared)
        screen = json.loads((A / 'evidence/dedup-screen-07B33.json').read_bytes())
        old = list(csv.DictReader(io.StringIO((A / b33.SNAPSHOT).read_text(), newline='')))
        self.assertEqual(b33.dedup_errors(screen, old), [])
        for key, val in (('all_historical_bodies_reviewed', True), ('new_root_ids', ['P7-164']), ('selected_prior_finding_sections', [])):
            self.assertTrue(b33.dedup_errors(screen | {key: val}, old))

    def test_47_one163_not_old_output_navigation_or_event_roots(self):
        ad = self.table('root-adjudication')
        self.assertEqual([r['current_root_ids'] for r in ad if r['decision'] == 'new-local-root'], ['P7-163'])
        self.assertEqual(self.table('historical-extensions'), [])
        self.assertTrue(all(r['comparison_depth'] == b33.DEDUP_DEPTH for r in ad))
        self.assertEqual(ad[0]['nearest_prior_root_ids'], 'P7-030;P7-031;P7-103;P7-104')
        with (A / 'findings.csv').open(encoding='utf8', newline='') as stream:
            r = list(csv.DictReader(stream))[-1]
        self.assertEqual((r['id'], r['severity'], r['certainty'], r['type'], r['status'], r['next_phase']), ('P7-163', 'Medium', 'confirmed', 'implementation-defect', 'open-not-remediated', '8'))

    def test_48_all_inputs_and_two_substantive_not_executed_plans_per_FE(self):
        self.assertEqual(b33.residual_errors(self.table('residual-disposition'), self.table('residual-disposition', 32)), [])
        self.assertEqual(b33.split_errors(self.table('split-register'), self.table('split-register', 32)), [])
        data = [self.table(n) for n in ('feature-implementation-matrix', 'report-invariants', 'acceptance-tests')]
        self.assertEqual(b33.current_link_errors(*data), [])
        for f in data[0]:
            linked = [t for t in data[2] if t['feature_ids'] == f['id']]
            self.assertEqual(len(linked), 2)
            for t in linked:
                self.assertEqual(t['status'], 'not-executed')
                self.assertIn('إذن', t['prerequisites'])
                self.assertIn('not-executed', t['safety_controls'])
        for stem in ('handoffs', 'questions'):
            for old, new in zip(self.table(stem, 32), self.table(stem)):
                self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))

    def test_49_reference_date_raw_clock_capture_delivery_separate(self):
        prov = json.loads((A / 'evidence/provenance-07B33.json').read_bytes())
        note = (A / 'DATE-IDENTITY-NOTE-07B33.md').read_text()
        self.assertEqual(b33.date_identity_errors(prov, note), [])
        self.assertIn('2026-11-16', note)
        self.assertIn(prov['environment_clock_observed_utc'], note)
        self.assertTrue(b33.date_identity_errors(prov | dict(audit_reference_date_utc='changed'), note))
        self.assertTrue(b33.date_identity_errors(prov, note.replace(b33.DISPATCHER_SHA, 'changed')))
        old = json.loads((A / 'evidence/checks-07B32.json').read_bytes())
        self.assertEqual(old['checkout_head'], '0bbadbe9f86a7ded7bbb1d2bcce209c7eda551fb')
        self.assertNotEqual(old['checkout_head'], b33.ENTRY)

    def test_50_synthetic38_schema_is_not_execution_evidence(self):
        h = self.history_fixture()
        self.assertEqual(b33.historical_record_errors(h), [])
        for key, val in (('registry_used', 'findings.csv'), ('findings_total', 335), ('process_exit_code', True),
                         ('audit_checker_self_test_cases_reported', 1138), ('erp_runtime_tests_executed', True)):
            bad = copy.deepcopy(h)
            bad['historical_modes'][-1][key] = val
            self.assertTrue(b33.historical_record_errors(bad))
        for key, val in (('tests_reported', 51), ('historical_source_assertion_input_count', 123),
                         ('test_module_Path_and_A_are_historical_assertion_inputs_only', 1), ('auxiliary_dispatcher_text_sha256', 'b' * 64)):
            bad = copy.deepcopy(h)
            bad['historical_modes'][-1]['historical_B32_child'][key] = val
            self.assertTrue(b33.historical_record_errors(bad))
        self.assertTrue(b33.historical_record_errors(h | dict(historical_mode_count=True)))

    def test_51_ACTUAL38_archive123_single_inverse_pin_and_proof(self):
        p = A / 'evidence/historical-mode-verification-07B33.json'
        raw = p.read_bytes()
        h = json.loads(raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), b33.HISTORICAL_RUN_SHA)
        self.assertEqual(b33.historical_record_errors(h), [])
        self.assertEqual((h['checkout_head'], h['source_head'], h['branch']), (b33.ENTRY, v.HEAD, v.BRANCH))
        sources = {p.relative_to(A).as_posix(): p.read_bytes() for p in sorted((A / 'tools').glob('*.py'))}
        self.assertEqual(len(sources), 123)
        self.assertEqual(b33.capture_source_errors(h, sources), [])
        for key in ('tools/validate_output_route_part.py', 'tools/test_output_route_audit_validator.py', 'tools/validate_audit.py'):
            changed = dict(sources)
            changed[key] += b'\n'
            self.assertTrue(b33.capture_source_errors(h, changed))
        self.assertTrue(b33.capture_source_errors(h, {}))
        self.assertTrue(all(m['stdout_bytes'] > 0 and m['stderr_bytes'] == 0 and m['process_exit_code'] == 0 for m in h['historical_modes']))
        self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'], self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        proof = json.loads((A / 'evidence/capture-time-identity-07B33.json').read_bytes())
        self.assertEqual((proof['archive_bytes'], proof['archive_sha256'], proof['capture_tool_set_count'],
            proof['unchanged_capture_tool_count'], proof['raw_stdout_identities_temporarily_rechecked']), (len(raw), b33.HISTORICAL_RUN_SHA, 123, 122, 38))
        self.assertTrue(proof['exact_inverse_reconstructs_capture_time_bytes'])
        self.assertFalse(proof['wholesale38_replayed_after_pin'])

    def test_52_actual123_AST_stdlib_and_B32_captures_attempts_preserved(self):
        tools = list((A / 'tools').glob('*.py'))
        self.assertEqual(len(tools), 123)
        for p in tools:
            ast.parse(p.read_text(), filename=str(p))
        tree = ast.parse((A / 'tools/check_output_route_witnesses.py').read_text())
        imports = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                imports.update(x.name.split('.')[0] for x in n.names)
            elif isinstance(n, ast.ImportFrom):
                imports.add(n.module.split('.')[0])
        self.assertEqual(imports, {'__future__', 'hashlib', 'json', 'pathlib'})
        self.assertFalse(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id in {'eval', 'exec', '__import__'} for n in ast.walk(tree)))
        prov = json.loads((A / 'evidence/provenance-07B33.json').read_bytes())
        old = prov['historical_artifact_sha256']
        for name in ('evidence/historical-mode-verification-07B32.json', 'evidence/capture-time-identity-07B32.json',
            'evidence/checks-07B32.json', 'evidence/official-capture-receipt-07B32.json', 'DATE-IDENTITY-NOTE-07B32.md',
            'tools/test_editor_close_audit_validator.py', 'tools/test_navigation_load_audit_validator.py',
            'tools/run_historical_navigation_load_tests_07B32.py', 'evidence/checks-07B31-final.json',
            'evidence/checker-preflight-attempt-01-07B29.json'):
            self.assertIn(name, old)
            self.assertEqual(hashlib.sha256((A / name).read_bytes()).hexdigest(), old[name])
        failed = json.loads((A / 'evidence/historical-adapter-note01-07B33.json').read_bytes())
        self.assertEqual((failed['observed_exit_code'], failed['observed_tests_reported'], failed['observed_failures']), (1, 52, 1))
        self.assertFalse(failed['historical_success_claim'])
        src = failed['source_before_correction']
        self.assertEqual(hashlib.sha256((A / src['path']).read_bytes()).hexdigest(), src['sha256'])
        corrected = json.loads((A / 'evidence/historical-adapter-note02-07B33.json').read_bytes())
        self.assertEqual(corrected['process_exit_code'], 0)
        for key in ('stdout', 'stderr'):
            r = corrected[key]
            self.assertEqual(hashlib.sha256((A / r['path']).read_bytes()).hexdigest(), r['sha256'])
            self.assertEqual((A / r['path']).stat().st_size, r['bytes'])


if __name__ == '__main__':
    unittest.main()
