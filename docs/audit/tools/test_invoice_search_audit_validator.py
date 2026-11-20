#!/usr/bin/env python3
"""52 documentary self-tests; NOT invoice, WPF/DataView/SQL or ERP acceptance.

ALL786 earlier protected cases remain unchanged. B26 ALL48 uses OWN326/
raw327CRLF/indexes/presetB26 and suite-local A in an explicit separate child.
B25/44 and B24/44 stay separately versioned. Synthetic32 fixtures check schema
rejection only; actual32 captured archive has its own byte/hash/identity test.
Only supplied records/explicit actions are modeled; no SDK/DTO default or
calendar/culture/status meaning, saved loss or application fix is assumed.
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
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_invoice_search_part as b27
from validate_bulk_product_part import historical_b25_inputs
from check_invoice_search_witnesses import SOURCE_SLICES, checked, condition_after, consumer_lookup, display_rows, integer, records, result_of, source_rows
A=Path(__file__).resolve().parents[1]


class InvoiceSearchAuditTests(unittest.TestCase):
    def old(self,n=326):
        return [dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
             type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]

    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n')
        w.writeheader();w.writerows(data);return s.getvalue().encode()

    def current(self):
        return self.old()+[self.old(1)[0]|dict(id=n,next_phase='8') for n in b27.NEW_IDS]

    def texts(self):
        return {n:'FROZEN:'+n for n in b27.SHARED_DOCS}

    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])

    def context(self,f):
        return b27.historical_b26_inputs(f,self.old(),self.texts(),self.raw(self.old()))

    def table(self,name):
        return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))

    def groups(self,end):
        return '\n'.join(f'| G-{n:02d} | exact |' for n in range(1,end+1))+'\n'

    def contracts(self):
        fs,iv,tests=[],[],[]
        for n in range(1,19):
            fid,iid=f'FE-{n:02d}',f'INV-{n:02d}';root=b27.NEW_IDS[n-1] if n<=3 else 'H'
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}' for i in(2*n-1,2*n)))
            fs.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            iv.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):
                tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,
                    plan_kind='finding-specific' if n<=3 else 'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fs,iv,tests

    def residuals(self):
        old=[dict(id=f'RS7B26-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='upstream redacted',
             disposition='external-handoff',current_handoff_or_split_ids='H7B26-03;H7B26-04') for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B26.csv',
             upstream_row_sha256=b27.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',
             owner_role='owner',required_redacted_input='upstream redacted; new contract',impact_if_unavailable='blocked',
             next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B27-03;H7B27-04',
             disposition='external-handoff',runtime_status='not-executed') for r in old]
        return new,old

    def splits(self):
        old=[dict(id=f'SP7B26-{n:02d}',required_input='upstream redacted') for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B26.csv',upstream_row_sha256=b27.row_sha(r),
             title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',
             required_input='upstream redacted; new contract',next_static_action='trace',static_exit_criterion='exit',
             status='explicit-further-static-split-not-started',runtime_status='not-executed') for r in old]
        return new,old

    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open',
             'bounded-R4k-invoice-search-delivered-residuals-open']+['planned-not-started']*6
        return [dict(part_family='7B' if n<4 else '7C',status=s,runtime_status='not-executed',
             counts_are_sessions_or_completion_percent='false') for n,s in enumerate(states)]

    def witness(self):
        return json.loads((A/'evidence/invoice-search-witnesses-07B27.json').read_bytes())

    def history_fixture(self):
        """Synthetic32 SCHEMA fixture, NEVER proof that32 modes actually ran."""
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B26.json').read_bytes())['historical_modes'])
        modes.append(dict(mode='B26',findings_total=326,registry_used=b27.SNAPSHOT,process_exit_code=0,validation_errors=[],
             original_project_hashes_matching=827,audit_checker_self_test_cases_reported=786,audit_checker_self_test_suite_count=27,
             erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,
             historical_B26_child=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',
                historical_parser_cutoff='B26-not-current-B27-default',all_original_cases_executed_unmodified=True,
                dedicated_child_launcher='tools/run_historical_bulk_product_tests_07B27.py',
                no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=32,historical_modes=modes,errors=[])

    def test_01_OWN326_exact_raw327CRLF_three_texts(self):
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
                with b27.historical_b26_inputs(f, data, texts, b):
                    pass
        old[-1]['id'] = old[0]['id']
        with self.assertRaises(ValueError):
            with b27.historical_b26_inputs(f, old, self.texts(), self.raw(old)):
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

    def test_04_nested_OWN324_and_exception_restoration(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b25_inputs(f,self.old(324),self.texts(),self.raw(self.old(324))):
                self.assertEqual(len(f.rows('findings.csv')),324)
            self.assertEqual(len(f.rows('findings.csv')),326)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_05_frozen_rows_texts_copy_isolation(self):
        f, old, texts = self.fake(), self.old(), self.texts()
        saved = copy.deepcopy(old)
        with b27.historical_b26_inputs(f, old, texts, self.raw(old)):
            data = f.rows('findings.csv')
            data[0]['next_phase'] = 'bad'
            self.assertEqual(f.rows('findings.csv'), saved)
            self.assertEqual(f.read(f.AUDIT / 'PLAN.md'), 'FROZEN:PLAN.md')
        self.assertEqual(old, saved)
        self.assertEqual(texts, self.texts())

    def test_06_all326_fields_ALLnextphase_evidence_rawprefix(self):
        old, cur = self.old(), self.current()
        self.assertEqual(b27.registry_preservation_errors(old, cur, self.raw(cur), self.raw(old)), [])
        for key in old[0]:
            bad = copy.deepcopy(cur)
            bad[0][key] = 'changed'
            self.assertTrue(b27.registry_preservation_errors(old, bad, self.raw(bad), self.raw(old)), key)

    def test_07_only155_156_157_append_raw330CRLF_noBOM(self):
        old, cur = self.old(), self.current()
        for bad in (cur[:-1], cur + [dict(cur[-1])], cur[:326] + list(reversed(cur[326:]))):
            self.assertTrue(b27.registry_preservation_errors(old, bad, self.raw(bad), self.raw(old)))
        for raw in (self.raw(cur).replace(b'\r\n', b'\n'), b'\xef\xbb\xbf' + self.raw(cur), self.raw(cur)[:-2]):
            self.assertTrue(b27.registry_preservation_errors(old, cur, raw, self.raw(old)))

    def test_08_exact_G223_append224through228_only(self):
        self.assertEqual(b27.group_row_errors(self.groups(223), self.groups(228)), [])
        for bad in (self.groups(222), self.groups(224), self.groups(228).replace('G-99', 'G-98'),
                    self.groups(228).replace('| G-01 | exact', '| G-01 | changed')):
            self.assertTrue(b27.group_row_errors(self.groups(223), bad))

    def test_09_sentinels_expand_before_dedup_RC_regression(self):
        errors,calls=[],[]
        f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),
             scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for gate in('FE7B27-17','AD7B27-08','AD7B27-09'):b27.validate_source(f,dict(id=gate,evidence=b27.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]))
        b27.validate_source(f,dict(id='UNKNOWN',evidence=b27.DOCUMENTARY),{})
        b27.validate_source(f,dict(id='FE7B27-17',evidence='a.cs:1-2'),{})
        self.assertEqual((len(errors),len(calls)),(2,2))
        fs=[dict(evidence='a.cs:1-2;3;b.cs:7'),dict(evidence='a.cs:1-2;5;b.cs:7;9-10'),dict(evidence=b27.DOCUMENTARY)]
        self.assertEqual(b27.source_evidence_union(fs),'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5;b.cs:9-10')
        self.assertEqual(b27.source_evidence_union([dict(evidence=b27.DOCUMENTARY)]),b27.DOCUMENTARY)
        for bad in('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b27.expanded_source_evidence(bad)
        fe,rc=self.table('feature-implementation-matrix-07B27.csv'),self.table('report-reconciliation-07B27.csv')
        for r in rc:self.assertEqual(r['evidence'],b27.source_evidence_union([f for f in fe if f['id'] in r['feature_ids'].split(';')]))

    def test_10_ordered_SC8_DS8_proc_eligibility_type_GID_limits(self):
        sc,ds=self.table('search-criteria-lineage-07B27.csv'),self.table('document-selection-lineage-07B27.csv')
        self.assertEqual(b27.ledger_errors(sc,ds),[])
        for pool in(0,1):
            parts=copy.deepcopy([sc,ds]);parts[pool][0],parts[pool][1]=parts[pool][1],parts[pool][0]
            self.assertTrue(b27.ledger_errors(*parts))
            for index in range(8):
                parts=copy.deepcopy([sc,ds]);parts[pool][index]['observation']='all-accepted'
                self.assertTrue(b27.ledger_errors(*parts))

    def test_11_ledger_responsibilities_nonempty_not_executed(self):
        sc,ds=self.table('search-criteria-lineage-07B27.csv'),self.table('document-selection-lineage-07B27.csv')
        for key in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(ds);bad[0][key]='';self.assertTrue(b27.ledger_errors(sc,bad),key)
        bad=copy.deepcopy(sc);bad[0]['runtime_status']='passed';self.assertTrue(b27.ledger_errors(bad,ds))
        self.assertTrue(b27.ledger_errors(sc[:-1],ds))

    def test_12_FE18_INV18_T36_reverse_links_three_specific_roots(self):
        self.assertEqual(b27.current_link_errors(*self.contracts()), [])
        for pool, key in ((0, 'acceptance_ids'), (1, 'feature_ids'), (2, 'feature_ids'), (2, 'status'), (2, 'finding_ids')):
            parts = self.contracts()
            parts[pool][0][key] = 'changed'
            self.assertTrue(b27.current_link_errors(*parts), key)
        fs, iv, ts = self.contracts()
        self.assertTrue(b27.current_link_errors(fs, iv, ts[:-1]))

    def test_13_distinct_invariants_criteria_and_responsibilities(self):
        for key in ('owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step', 'limit'):
            fs, iv, ts = self.contracts()
            fs[0][key] = ''
            self.assertTrue(b27.current_link_errors(fs, iv, ts), key)
        fs, iv, ts = self.contracts()
        iv[1]['required_invariant'] = iv[0]['required_invariant']
        self.assertTrue(b27.current_link_errors(fs, iv, ts))
        fs, iv, ts = self.contracts()
        ts[1]['acceptance_criterion'] = ts[0]['acceptance_criterion']
        self.assertTrue(b27.current_link_errors(fs, iv, ts))

    def test_14_all14_residual_ancestry_hash_contracts(self):
        current, old = self.residuals()
        self.assertEqual(b27.residual_errors(current, old), [])
        for key in ('upstream_residual_id', 'upstream_artifact', 'upstream_row_sha256', 'upstream_contract_ids'):
            current, old = self.residuals()
            current[0][key] = 'changed'
            self.assertTrue(b27.residual_errors(current, old), key)
        self.assertTrue(b27.residual_errors(current[:-1], old))

    def test_15_full_old_inputs_all_routes_and_no_approval(self):
        for key in ('local_result', 'owner_role', 'required_redacted_input', 'impact_if_unavailable', 'next_step',
                    'static_exit_criterion', 'current_handoff_or_split_ids'):
            current, old = self.residuals()
            current[0][key] = ''
            self.assertTrue(b27.residual_errors(current, old), key)
        for key, value in (('required_redacted_input', 'lost'), ('disposition', 'approved'),
                            ('runtime_status', 'passed'), ('current_handoff_or_split_ids', 'H7B27-03')):
            current, old = self.residuals()
            current[0][key] = value
            self.assertTrue(b27.residual_errors(current, old), key)

    def test_16_three_split_ancestries_full_inputs_and_reasons(self):
        current, old = self.splits()
        self.assertEqual(b27.split_errors(current, old), [])
        for key in current[0]:
            current, old = self.splits()
            current[0][key] = ''
            self.assertTrue(b27.split_errors(current, old), key)
        current, old = self.splits()
        current[0]['required_input'] = 'replacement'
        self.assertTrue(b27.split_errors(current, old))

    def test_17_boundedR4k_fourB_sixC_unstarted_no_percent_or_sessions(self):
        self.assertEqual(b27.remaining_work_errors(self.work()), [])
        for index, key, value in ((3, 'status', 'complete'), (4, 'status', 'in-progress'),
                                  (0, 'runtime_status', 'passed'), (0, 'counts_are_sessions_or_completion_percent', 'true'),
                                  (0, 'part_family', '7C')):
            work = self.work()
            work[index][key] = value
            self.assertTrue(b27.remaining_work_errors(work), key)
        self.assertTrue(b27.remaining_work_errors(self.work()[:-1]))

    def test_18_witness_strict_boolean_integer_limits_B10_addendum(self):
        self.assertEqual(b27.witness_metadata_errors(self.witness()),[])
        for key,val in(('application_code_imported_or_executed',0),('erp_runtime_tests_executed',False),
             ('illustration_count',20.0),('B_R4k_bounded_not_whole7B_closure',1),('phase8_authorized_or_started',True),
             ('phase7C_started',True),('actual_WPF_event_order_or_count_claimed',True),('financial_or_status_policy_invented',True),
             ('database_commit_or_saved_loss_claimed',True),('external_DTO_constructor_defaults_assumed',True)):
            self.assertTrue(b27.witness_metadata_errors(self.witness()|{key:val}),key)
        w=self.witness();w['retained_additive_B10_arithmetic_erratum']['reference_cost']=10
        self.assertTrue(b27.witness_metadata_errors(w))

    def test_19_actual_successful_witness_hash_readonly_recompute(self):
        raw=(A/'evidence/invoice-search-witnesses-07B27.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b27.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_invoice_search_witnesses.py')],capture_output=True,text=True,timeout=25)
        self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,'')
        self.assertEqual(json.loads(run.stdout),self.witness())

    def test_20_synthetic32_schema_OWN326_ALL48_not_execution_evidence(self):
        self.assertEqual(b27.historical_record_errors(self.history_fixture()),[])
        for i,k,val in((31,'findings_total',329),(31,'registry_used','findings.csv'),(31,'stdout_sha256','bad'),
             (31,'audit_checker_self_test_cases_reported',838),(0,'audit_checker_self_test_cases_reported',0),
             (31,'erp_runtime_tests_executed',False)):
            h=self.history_fixture();h['historical_modes'][i][k]=val;self.assertTrue(b27.historical_record_errors(h),k)
        h=self.history_fixture();h['historical_modes'][-1]['historical_B26_child']['suite_own_registry_path_is_context_local_not_global']=False
        self.assertTrue(b27.historical_record_errors(h))
        h=self.history_fixture();h['historical_modes'].pop();self.assertTrue(b27.historical_record_errors(h))

    def test_21_actual32_archive_hash_identity_separate_from_schema_fixture(self):
        raw=(A/'evidence/historical-mode-verification-07B27.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b27.HISTORICAL_RUN_SHA)
        h=json.loads(raw);self.assertEqual(b27.historical_record_errors(h),[])
        self.assertEqual(h['checkout_head'],b27.ENTRY);self.assertEqual(h['current_actual_CLI_default'],'B27')
        self.assertEqual(h['historical_mode_count'],32)
        self.assertTrue(all(m['process_exit_code']==0 and m['stderr_bytes']==0 for m in h['historical_modes']))

    def test_22_server2_selected1_empty_All_remains_only2(self):
        loaded=source_rows(records(),8,2)
        self.assertEqual(display_rows(loaded,1),[])
        self.assertEqual({r['proc'] for r in display_rows(loaded,0)},{2})
        self.assertEqual([r['global_id'] for r in loaded],['T_SEND'])

    def test_23_same2_and_fresh1_controls_not_executed_reload(self):
        data=records();saved=copy.deepcopy(data);loaded=source_rows(data,8,2)
        self.assertEqual(display_rows(loaded,2),loaded)
        self.assertIn('T_OK',[r['global_id'] for r in display_rows(source_rows(data,8,1),1)])
        self.assertEqual(data,saved)
        loaded[0]['pay']=999;self.assertEqual(data,saved)

    def test_24_both_explicit_date_actions_drop_status1_same_root156(self):
        initial=source_rows(records(),8,1,cond='caller-status1')
        self.assertNotIn('T_NOT_ELIGIBLE',[r['global_id'] for r in initial])
        for action in('from-date','to-date'):
            cond=condition_after(action,'caller-status1');self.assertEqual(cond,'dates')
            self.assertIn('T_NOT_ELIGIBLE',[r['global_id'] for r in source_rows(records(),8,1,cond=cond)])

    def test_25_clear_drops_mandatory_eligibility_no_WPF_event_count(self):
        self.assertEqual(condition_after('clear','caller-status1'),'empty')
        after=source_rows(records(),8,1,cond=condition_after('clear','caller-status1'))
        self.assertIn(0,{r['status'] for r in after})
        self.assertIn('T_OTHER_DAY',[r['global_id'] for r in after])

    def test_26_date_really_filters_branch_deleted_positive_controls(self):
        after=source_rows(records(),8,1,cond='dates')
        self.assertEqual({r['day'] for r in after},{2})
        self.assertTrue(all(r['branch']==1 and r['deleted'] is False for r in after))
        self.assertNotIn('T_OTHER_DAY',[r['global_id'] for r in after])
        self.assertEqual(source_rows(records(),8,1,cond='dates',window=(7,7))[0]['global_id'],'T_OTHER_DAY')

    def test_27_receive_consumer_does_not_restore_status1_not_stock_save(self):
        row=next(r for r in source_rows(records(),8,1,cond='dates') if r['status']==0)
        result=consumer_lookup(records(),result_of(row))
        self.assertEqual(result['matches'][0]['status'],0)
        self.assertEqual(result['supplied_where_fields'],['branch','InvGlobalID'])
        self.assertFalse(result['source_application_or_SQL_executed'])
        self.assertTrue(result['no_deployed_schema_uniqueness_or_save_success_claim'])

    def test_28_purchase1_source_includes20_not_requested1_only(self):
        rows=source_rows(records(),1,1)
        self.assertEqual({r['kind'] for r in rows},{1,20})
        self.assertEqual({r['global_id'] for r in rows},{'P_REQUESTED','A_TYPE20'})
        self.assertEqual(len(rows),2)

    def test_29_projection_retains_GID_not061_omits_allowed_type(self):
        row=next(r for r in source_rows(records(),1,1) if r['kind']==20);selected=result_of(row)
        self.assertEqual(selected,dict(ISDone=True,InvGlobalID='A_TYPE20',ProcType=1,PayType=1))
        for k in('kind','branch','status','local_id'):self.assertNotIn(k,selected)
        selected['PayType']=4;self.assertEqual(row['pay'],1)

    def test_30_selected_GID_consumer_maps_actual20_type1_control(self):
        rows=source_rows(records(),1,1)
        for row in rows:
            result=consumer_lookup(records(),result_of(row))
            self.assertEqual(result['reader_mapped_type'],row['kind'])
            self.assertEqual(len(result['matches']),1)
            self.assertFalse(result['source_application_or_SQL_executed'])

    def test_31_special23_exact_and_request20_no_OR_duplication(self):
        for requested,expected in((23,'C_TYPE23'),(20,'A_TYPE20')):
            rows=source_rows(records(),requested,1)
            self.assertEqual([r['global_id'] for r in rows],[expected])
            self.assertEqual({r['kind'] for r in rows},{requested})

    def test_32_not_done_sentinel_and_branch_mismatch_not_consumed(self):
        self.assertEqual(consumer_lookup(records(),result_of())['matches'],[])
        row=next(r for r in records() if r['global_id']=='A_TYPE20')
        self.assertEqual(consumer_lookup(records(),result_of(row),branch=2)['matches'],[])
        selected=result_of(row);selected['ISDone']=False
        self.assertEqual(consumer_lookup(records(),selected)['matches'],[])
        selected['ISDone']=True;selected['InvGlobalID']='-1'
        self.assertEqual(consumer_lookup(records(),selected)['matches'],[])

    def test_33_equal_local7_uses_GID_positive_control_not_uniqueness_proof(self):
        rows=source_rows(records(),1,1);self.assertEqual([r['local_id'] for r in rows],[7,7])
        for row in rows:self.assertEqual(consumer_lookup(records(),result_of(row))['matches'],[row])
        self.assertNotEqual(result_of(rows[0])['InvGlobalID'],result_of(rows[1])['InvGlobalID'])

    def test_34_supplied_records_strict_shape_unique_nonsecret_ids_types(self):
        data=records()
        for row in(data[0]|{'extra':1},data[0]|{'kind':True},data[0]|{'deleted':0},data[0]|{'day':0},
             data[0]|{'global_id':'unsafe quote\''},data[0]|{'global_id':''},data[0]|{'pay':False}):
            with self.assertRaises(ValueError):checked([row])
        for bad in(None,{},[data[0],data[0]]):
            with self.assertRaises(ValueError):checked(bad)
        result=checked(data);result[0]['kind']=20;self.assertEqual(data,records())

    def test_35_explicit_actions_condition_domain_not_arbitrary_SQL(self):
        for cond in('empty','dates','caller-status1'):
            self.assertEqual(condition_after('unchanged',cond),cond)
            self.assertEqual(condition_after('clear',cond),'empty')
        for action,cond in(('reload','empty'),('clear','AND secret=1'),('clear',None)):
            with self.assertRaises(ValueError):condition_after(action,cond)

    def test_36_integer_and_ordinal_fixture_bounds_not_calendar_parser(self):
        for n in(True,1.0,'1',None,-1,31):
            with self.assertRaises(ValueError):integer(n)
        for opts in(dict(requested_type=True,server_proc=1),dict(requested_type=1,server_proc=0),
             dict(requested_type=1,server_proc=1,window=[2,2]),dict(requested_type=1,server_proc=1,window=(3,2)),
             dict(requested_type=1,server_proc=1,branch=False)):
            with self.assertRaises(ValueError):source_rows(records(),**opts)
        for selected in(True,-1,5,'1'):
            with self.assertRaises(ValueError):display_rows([],selected)
        self.assertEqual(integer(0),0)

    def test_37_selection_consumer_explicit_shape_no_DTO_defaults(self):
        row=records()[0];selected=result_of(row)
        for bad in(selected|{'extra':1},selected|{'ISDone':1},selected|{'InvGlobalID':None},
             selected|{'ProcType':True},selected|{'PayType':False}):
            with self.assertRaises(ValueError):consumer_lookup(records(),bad)
        with self.assertRaises(ValueError):consumer_lookup(records(),selected,branch=0)
        self.assertEqual(result_of(),dict(ISDone=False,InvGlobalID='-1',ProcType=1,PayType=1))

    def test_38_ACTUAL_B27_parser_versioned_B26_B25_B24_API15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in(('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'))+tuple((f'PHASE7_B{n}_CLI',f'B{n}') for n in range(18,27)):
            self.assertEqual(getattr(v,name)['default'],part)
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B27')
        for part in('A',)+tuple('B'+str(n) for n in range(1,28)):
            self.assertEqual(parser.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)

    def test_39_actual_entrypoint_OWN26_before_current27(self):
        tree=ast.parse(Path(v.__file__).read_text())
        blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]))
        self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'))
        self.assertLess(body.index('historical_b25_validation('),body.index('historical_b26_validation('))
        self.assertLess(body.index('historical_b26_validation('),body.index('extend_invoice_search('))
        self.assertIn('extend_bulk_products(historical_b26,',body);self.assertIn("phase7_part == 'B26'",body)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser')))

    def test_40_exact_argv_proxy_preserves_unrelated_calls_kwargs(self):
        calls = []
        backend = SimpleNamespace(run=lambda *a, **k: calls.append((a, k)) or 'sentinel')
        proxy = b27.HistoricalB26Subprocess(backend, 'python', Path('/a/tools'))
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
        view = b27.HistoricalB26ValidatorView(f)
        original = subprocess.run, Path.read_bytes, Path.read_text
        before = f.AUDIT, f.read, f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess, backend)
                self.assertEqual((subprocess.run, Path.read_bytes, Path.read_text), original)
                self.assertEqual(len(view.rows('findings.csv')), 326)
                raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a, b in zip(before, (f.AUDIT, f.read, f.rows))))

    def test_42_historical_child_ALL48_local_A_and_protected26_25_24_tools(self):
        tools=A/'tools';source=ast.unparse(ast.parse((tools/'run_historical_bulk_product_tests_07B27.py').read_text()))
        for token in('loadTestsFromModule(historical_tests)','suite.countTestCases() != 48','result.testsRun != 48 or result.skipped',
             'historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset',
             'v.PHASE7_B26_CLI','b27.historical_b26_inputs('):self.assertIn(token,source)
        self.assertNotIn('unittest.skip',source)
        prov=json.loads((A/'evidence/provenance-07B27.json').read_bytes())
        for name in('test_bulk_product_audit_validator.py','validate_bulk_product_part.py','check_bulk_product_witnesses.py',
             'run_historical_property_dialog_tests_07B26.py','test_property_dialog_audit_validator.py','validate_property_dialog_part.py',
             'run_historical_row_ownership_tests_07B25.py','test_row_ownership_audit_validator.py','validate_row_ownership_part.py'):
            self.assertEqual(hashlib.sha256((tools/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])

    def test_43_actual326_exact_fields_barriers_three_entry_freezes(self):
        raw=(A/b27.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')))
        self.assertEqual(b27.registry_preservation_errors(old,cur,now,raw),[]);self.assertEqual(cur[:326],old)
        lookup={r['id']:r for r in cur}
        for n in('P4-014','P7-132','P7-145'):self.assertEqual(lookup[n]['certainty'],'potential')
        self.assertEqual(self.table('historical-extensions-07B27.csv'),[])
        for n,h in((b27.SNAPSHOT,b27.SNAPSHOT_SHA),(b27.SHARED_SNAPSHOT,b27.SHARED_SHA),('evidence/provenance-07B27.json',b27.PROVENANCE_SHA)):
            self.assertEqual(hashlib.sha256((A/n).read_bytes()).hexdigest(),h)

    def test_44_scope7_overlap6_new1_union426_actual11reads_two_whole(self):
        d=json.loads((A/'evidence/scope-decision-07B27.json').read_bytes())
        self.assertEqual(tuple(d['bookkeeping'][k] for k in('selected_paths','prior_union','overlap','new','union','complement')),(7,425,6,1,426,401))
        self.assertEqual(d['bookkeeping']['complement_kinds'],dict(source=336,**{'generated-artifact':61,'project-or-resource':4}))
        self.assertEqual(d['selected_upstream_split'],'SP7B26-01');self.assertFalse(d['historical_body_review_claim'])
        self.assertEqual(d['historical_metadata_screen_count'],326);self.assertEqual(d['whole_local_search_lines'],dict(code_behind=698,xaml=561))
        w=self.witness();self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),w['whole_local_search_files_selected']),(11,2))
        actual={}
        for r in w['bounded_source_reads_not_semantic_coverage']:
            raw=(A.parents[1]/r['path']).read_bytes();lines=raw.decode('utf8').splitlines(keepends=True)
            self.assertEqual(hashlib.sha256(raw).hexdigest(),r['source_sha256'])
            self.assertEqual(hashlib.sha256(''.join(lines[r['start']-1:r['end']]).encode()).hexdigest(),r['selected_text_utf8_sha256'])
            actual.setdefault(r['path'],[]).append((r['start'],r['end']))
        self.assertEqual(actual,SOURCE_SLICES)

    def test_45_only_three_adjudicated_roots_prior_nearest_not_recounted(self):
        ad=self.table('root-adjudication-07B27.csv')
        self.assertEqual(len(ad),9);self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='new-local-root'],b27.NEW_IDS)
        self.assertTrue(all(r['comparison_depth']==b27.DEDUP_DEPTH for r in ad))
        for i,ids in((0,['P7-120','P7-073','P7-045']),(1,['P4-019','P7-061','P7-132']),(2,['P7-061','P7-131','P6-009'])):
            self.assertEqual(ad[i]['nearest_prior_root_ids'].split(';'),ids)
        self.assertEqual(ad[3]['decision'],'same-family-text-filter-lead-no-recount-or-extension')
        self.assertEqual(ad[4]['decision'],'unadjudicated-period-postpone-return-leads-not-extra-roots')
        self.assertEqual(self.table('historical-extensions-07B27.csv'),[])

    def test_46_actual14_residuals_three_splits_full_inputs_routes_currentlinks(self):
        rs,old=self.table('residual-disposition-07B27.csv'),self.table('residual-disposition-07B26.csv')
        sp,osp=self.table('split-register-07B27.csv'),self.table('split-register-07B26.csv')
        self.assertEqual(b27.residual_errors(rs,old),[]);self.assertEqual(b27.split_errors(sp,osp),[])
        fe,iv,plans=[self.table(n+'-07B27.csv') for n in('feature-implementation-matrix','report-invariants','acceptance-tests')]
        self.assertEqual(b27.current_link_errors(fe,iv,plans),[])
        self.assertTrue(all(t['status']=='not-executed' and t['procedure'] and t['safety_controls'] for t in plans))

    def test_47_reference_clock_source_capture_delivery_identities_separate(self):
        prov=json.loads((A/'evidence/provenance-07B27.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B27.md').read_text()
        self.assertEqual(b27.date_identity_errors(prov,note),[])
        self.assertTrue(b27.date_identity_errors(prov|{'audit_reference_date_utc':'2026-11-20'},note))
        self.assertTrue(b27.date_identity_errors(prov,note.replace(b27.B26_CHECK_SHA,'changed')))
        self.assertEqual(hashlib.sha256((A/'evidence/checks-07B26.json').read_bytes()).hexdigest(),b27.B26_CHECK_SHA)
        old=json.loads((A/'evidence/checks-07B26.json').read_bytes())
        self.assertEqual(old['checkout_head'],'dd38f97e844dc60ea64ae00fa40ef588e49752d7')
        self.assertNotEqual(old['checkout_head'],b27.ENTRY)

    def test_48_collector_stdlib_only_no_app_execution_and_protected765(self):
        tools=A/'tools';tree=ast.parse((tools/'check_invoice_search_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','sys','pathlib'})
        self.assertFalse(any(isinstance(n,ast.Call)and isinstance(n.func,ast.Name)and n.func.id in{'eval','exec','__import__'} for n in ast.walk(tree)))
        prov=json.loads((A/'evidence/provenance-07B27.json').read_bytes())
        self.assertEqual(len(prov['historical_artifact_sha256']),765)
        self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==h for n,h in prov['historical_artifact_sha256'].items()))
        for n in('validate_invoice_search_part.py','run_historical_bulk_product_tests_07B27.py','test_invoice_search_audit_validator.py'):
            ast.parse((tools/n).read_text(),filename=n)

    def test_49_failed_new_attempt_retained_exact_not_counted_passed(self):
        raw=(A/'evidence/invoice-search-witness-attempt-01-07B27.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b27.FAILED_WITNESS_SHA)
        w=json.loads(raw);self.assertEqual(w['errors'],['ST7B27-19'])
        self.assertFalse(w['static_lexical_contract_checks'][18]['documented_text_observation_matches'])
        self.assertTrue(all(r['illustration_assertions_passed'] for r in w['illustrations']))
        self.assertEqual(self.witness()['errors'],[])
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(),b27.WITNESS_SHA)

    def test_50_all20illustrations20lexical_pass_inert_explicit_limits(self):
        w=self.witness()
        for key,prefix,flag in(('illustrations','ALG7B27-','illustration_assertions_passed'),
             ('static_lexical_contract_checks','ST7B27-','documented_text_observation_matches')):
            self.assertEqual([r['id'] for r in w[key]],[f'{prefix}{i:02d}' for i in range(1,21)])
            self.assertTrue(all(r[flag] is True and r['source_application_executed'] is False and r['limit'] for r in w[key]))
        for k in('actual_WPF_event_order_or_count_claimed','financial_or_status_policy_invented',
             'database_commit_or_saved_loss_claimed','all_callers_or_external_DTOs_body_reviewed'):self.assertIs(w[k],False)
        self.assertEqual(len(w['unadjudicated_source_leads_not_additional_findings']),4)

    def test_51_documentref_followup_not_existing_contract_and_evidence_in_scope(self):
        ds=self.table('document-selection-lineage-07B27.csv');r=ds[-1]
        self.assertEqual(r['boundary'],'documentref-followup-contract');self.assertEqual(r['finding_ids'],'H7B27-03')
        self.assertEqual(r['feature_ids'],'FE7B27-11');self.assertIn('لا تطبيق قائم',r['limit'])
        scope=SOURCE_SLICES
        pools=[self.table(n+'-07B27.csv') for n,_,_ in b27.TABLE_SPECS]
        errors=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:None,
             scoped_evidence=lambda value,sc,location,phase:errors.extend(part for part in value.split(';')
               if not any(a<=int(part.rsplit(':',1)[1].split('-')[0])<=int(part.rsplit(':',1)[1].split('-')[-1])<=b
                 for a,b in sc.get(part.rsplit(':',1)[0],[]))))
        for pool in pools:
            for row in pool:b27.validate_source(f,row,scope)
        self.assertEqual(errors,[])

    def test_52_every_capability_has_substantive_responsibility_two_unexecutedplans(self):
        fe=self.table('feature-implementation-matrix-07B27.csv');plans=self.table('acceptance-tests-07B27.csv')
        self.assertEqual((len(fe),len(plans)),(18,36))
        for r in fe:
            for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
                self.assertGreater(len(r[key]),20,(r['id'],key))
            linked=[t for t in plans if t['feature_ids']==r['id']];self.assertEqual(len(linked),2)
            self.assertEqual(len({t['acceptance_criterion'] for t in linked}),2)
            for t in linked:
                self.assertEqual(t['status'],'not-executed')
                self.assertGreater(len(t['procedure']),35);self.assertGreater(len(t['acceptance_criterion']),35)
                self.assertIn('not-executed',t['safety_controls']);self.assertIn('إذن',t['prerequisites'])


if __name__=='__main__':
    unittest.main()
