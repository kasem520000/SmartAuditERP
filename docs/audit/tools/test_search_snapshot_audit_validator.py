#!/usr/bin/env python3
"""48 documentary cases, NOT32 integrated acceptance plans or ERP tests.

All838 earlier cases are retained. ALL52 original B27 cases use OWN329/
raw330CRLF/indexes/presetB27 and suite-local A in a separate child. Synthetic33
schema rejection fixtures are distinct from the actual33 captured archive.
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
import validate_search_snapshot_part as b28
from validate_invoice_search_part import historical_b26_inputs
from check_search_snapshot_witnesses import (SOURCE_SLICES,consumer_lookup,filtered,integer,literal,
    maximum_changed,minimum_changed,records,reload_result,selected_result,gids)
A=Path(__file__).resolve().parents[1]


class SearchSnapshotAuditTests(unittest.TestCase):
    def old(self,n=329):
        return [dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
          type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]

    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()

    def current(self):return self.old()+[self.old(1)[0]|dict(id='P7-158',next_phase='8')]
    def texts(self):return {n:'FROZEN:'+n for n in b28.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b28.historical_b27_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def table(self,name):return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))
    def groups(self,end):return '\n'.join(f'| G-{n:02d} | exact |' for n in range(1,end+1))+'\n'
    def data(self):return [dict(gid='fixture-A',net=5,day=10,branch=1),dict(gid='fixture-B',net=20,day=20,branch=1)]
    def witness(self):return json.loads((A/'evidence/search-snapshot-witnesses-07B28.json').read_bytes())

    def contracts(self):
        fs,ivs,tests=[],[],[]
        for n in range(1,17):
            fid,iid=f'FE-{n:02d}',f'INV-{n:02d}';root=('P7-158','P7-046')[n-1] if n<=2 else 'H'
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}' for i in (2*n-1,2*n)))
            fs.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            ivs.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in (2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,plan_kind='finding-specific' if n<=2 else 'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fs,ivs,tests

    def residuals(self):
        old=[dict(id=f'RS7B27-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='full upstream input',disposition='external-handoff',current_handoff_or_split_ids='H7B27-03;H7B27-04') for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B27.csv',upstream_row_sha256=b28.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',owner_role='owner',required_redacted_input='full upstream input; new',impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B28-03;H7B28-04',disposition='external-handoff',runtime_status='not-executed') for r in old]
        return new,old

    def splits(self):
        old=[dict(id=f'SP7B27-{n:02d}',required_input='full upstream input') for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B27.csv',upstream_row_sha256=b28.row_sha(r),title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='full upstream input; new',next_static_action='trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed') for r in old]
        return new,old

    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4l-search-snapshot-delivered-residuals-open']+['planned-not-started']*6
        return [dict(part_family='7B' if i<4 else '7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false') for i,s in enumerate(states)]

    def history_fixture(self):
        """Synthetic33 SCHEMA fixture, NEVER evidence that33 modes executed."""
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B27.json').read_bytes())['historical_modes'])
        modes.append(dict(mode='B27',findings_total=329,registry_used=b28.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=838,audit_checker_self_test_suite_count=28,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B27_child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B27-not-current-B28-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_invoice_search_tests_07B28.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=33,historical_modes=modes,errors=[])

    def test_01_OWN329_exact_raw330CRLF_three_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old())
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old())
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_reject_bad_OWN_rows_BOM_LF_bytes_texts(self):
        f,old,raw=self.fake(),self.old(),self.raw(self.old())
        for data,texts,b in ((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),(old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw),(old,self.texts(),bytearray(raw))):
            with self.assertRaises(ValueError):
                with b28.historical_b27_inputs(f,data,texts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b28.historical_b27_inputs(f,old,self.texts(),self.raw(old)):pass

    def test_03_context_local_Path_not_global_or_overlay(self):
        f=self.fake();before=Path.read_bytes,Path.read_text
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text),before)
            self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_text()

    def test_04_nested_OWN326_and_exception_restoration(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b26_inputs(f,self.old(326),self.texts(),self.raw(self.old(326))):self.assertEqual(len(f.rows('findings.csv')),326)
            self.assertEqual(len(f.rows('findings.csv')),329)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_05_frozen_rows_texts_copy_isolation(self):
        f,old,texts=self.fake(),self.old(),self.texts();saved=copy.deepcopy(old)
        with b28.historical_b27_inputs(f,old,texts,self.raw(old)):
            data=f.rows('findings.csv');data[0]['next_phase']='bad'
            self.assertEqual(f.rows('findings.csv'),saved);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertEqual(old,saved);self.assertEqual(texts,self.texts())

    def test_06_all329_exact_fields_ALLnextphase_evidence_rawprefix(self):
        old,cur=self.old(),self.current()
        self.assertEqual(b28.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed'
            self.assertTrue(b28.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)

    def test_07_only158_append_raw331CRLF_noBOM(self):
        old,cur=self.old(),self.current()
        for bad in (cur[:-1],cur+[dict(cur[-1])],cur[:-1]+[cur[-1]|dict(id='P7-159')]):self.assertTrue(b28.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in (self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):self.assertTrue(b28.registry_preservation_errors(old,cur,raw,self.raw(old)))

    def test_08_G01to228_exact_only229to232_appended(self):
        self.assertEqual(b28.group_row_errors(self.groups(228),self.groups(232)),[])
        for bad in (self.groups(227),self.groups(229),self.groups(232).replace('G-99','G-98'),self.groups(232).replace('| G-01 | exact','| G-01 | changed')):self.assertTrue(b28.group_row_errors(self.groups(228),bad))

    def test_09_documentary_sentinel_expand_before_dedup_RC(self):
        errors,calls=[],[]
        f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for gate in ('FE7B28-15','RC7B28-05','RC7B28-06','AD7B28-07','AD7B28-08'):b28.validate_source(f,dict(id=gate,evidence=b28.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]))
        b28.validate_source(f,dict(id='UNKNOWN',evidence=b28.DOCUMENTARY),{});b28.validate_source(f,dict(id='FE7B28-15',evidence='a.cs:1-2'),{})
        self.assertEqual((len(errors),len(calls)),(2,2))
        fs=[dict(evidence='a.cs:1-2;3;b.cs:7'),dict(evidence='a.cs:1-2;5;b.cs:7;9-10'),dict(evidence=b28.DOCUMENTARY)]
        self.assertEqual(b28.source_evidence_union(fs),'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5;b.cs:9-10')
        for bad in ('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b28.expanded_source_evidence(bad)
        fe=self.table('feature-implementation-matrix-07B28.csv')
        for r in self.table('report-reconciliation-07B28.csv'):self.assertEqual(r['evidence'],b28.source_evidence_union([f for f in fe if f['id'] in r['feature_ids'].split(';')]))

    def test_10_ordered_LH8_FR6_reject_reordering_or_changed_observations(self):
        parts=[self.table('load-health-lineage-07B28.csv'),self.table('filter-removal-lineage-07B28.csv')]
        self.assertEqual(b28.ledger_errors(*parts),[])
        for p in (0,1):
            bad=copy.deepcopy(parts);bad[p][0],bad[p][1]=bad[p][1],bad[p][0];self.assertTrue(b28.ledger_errors(*bad))
            for i in range(len(parts[p])):
                bad=copy.deepcopy(parts);bad[p][i]['observation']='all-accepted';self.assertTrue(b28.ledger_errors(*bad))

    def test_11_lineage_responsibilities_nonempty_not_executed(self):
        lh,fr=self.table('load-health-lineage-07B28.csv'),self.table('filter-removal-lineage-07B28.csv')
        for key in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(fr);bad[0][key]='';self.assertTrue(b28.ledger_errors(lh,bad),key)
        bad=copy.deepcopy(lh);bad[0]['runtime_status']='passed';self.assertTrue(b28.ledger_errors(bad,fr))

    def test_12_FE16_INV16_T32_first_new158_then_existing046(self):
        self.assertEqual(b28.current_link_errors(*self.contracts()),[])
        for pool,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            parts=self.contracts();parts[pool][0][key]='changed';self.assertTrue(b28.current_link_errors(*parts))
        fs,iv,ts=self.contracts();self.assertTrue(b28.current_link_errors(fs,iv,ts[:-1]))
        fs,iv,ts=self.contracts();fs[1]['finding_ids']='P7-159';self.assertTrue(b28.current_link_errors(fs,iv,ts))

    def test_13_distinct_invariants_criteria_and_capability_responsibilities(self):
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            fs,iv,ts=self.contracts();fs[0][key]='';self.assertTrue(b28.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b28.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b28.current_link_errors(fs,iv,ts))

    def test_14_all14_residual_ancestry_rowsha_contracts(self):
        new,old=self.residuals();self.assertEqual(b28.residual_errors(new,old),[])
        for k in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(new);bad[0][k]='changed';self.assertTrue(b28.residual_errors(bad,old))
        self.assertTrue(b28.residual_errors(new[:-1],old))

    def test_15_full_old_inputs_all_routes_no_approval_or_runtime(self):
        new,old=self.residuals()
        for k,value in (('required_redacted_input','only new'),('current_handoff_or_split_ids','H7B28-03'),('disposition','approved'),('runtime_status','passed'),('local_result','')):
            bad=copy.deepcopy(new);bad[0][k]=value;self.assertTrue(b28.residual_errors(bad,old),k)

    def test_16_all_three_split_ancestries_full_input_and_unstarted(self):
        new,old=self.splits();self.assertEqual(b28.split_errors(new,old),[])
        for k in ('upstream_split_id','upstream_artifact','upstream_row_sha256','required_input','reason_for_split','status','runtime_status'):
            bad=copy.deepcopy(new);bad[0][k]='changed' if k not in ('reason_for_split',) else '';self.assertTrue(b28.split_errors(bad,old),k)
        self.assertTrue(b28.split_errors(new[:-1],old))

    def test_17_fourB_boundedR4l_sixC_unstarted_not_percent_or_sessions(self):
        self.assertEqual(b28.remaining_work_errors(self.work()),[])
        for i,key,value in ((3,'status','complete'),(4,'status','started'),(0,'part_family','7C'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            bad=self.work();bad[i][key]=value;self.assertTrue(b28.remaining_work_errors(bad))

    def test_18_witness_strict_boolean_integer_limits_B10_addendum(self):
        w=self.witness();self.assertEqual(b28.witness_metadata_errors(w),[])
        for key in ('application_code_imported_or_executed','actual_WPF_event_order_or_count_claimed','provider_failure_or_partial_fill_observed','database_commit_or_saved_loss_claimed'):
            self.assertTrue(b28.witness_metadata_errors(w|{key:0}));self.assertTrue(b28.witness_metadata_errors(w|{key:True}))
        for key in ('illustration_count','selected_source_paths','erp_runtime_tests_executed'):
            self.assertTrue(b28.witness_metadata_errors(w|{key:True}))
        self.assertTrue(b28.witness_metadata_errors(w|{'retained_additive_B10_arithmetic_erratum':dict(local_cost=20,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)}))

    def test_19_actual_witness_hash_and_readonly_CLI_recompute(self):
        raw=(A/'evidence/search-snapshot-witnesses-07B28.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b28.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_search_snapshot_witnesses.py')],capture_output=True,timeout=20)
        self.assertEqual((run.returncode,run.stderr),(0,b''));self.assertEqual(run.stdout,raw)
        self.assertTrue(all(x['illustration_assertions_passed'] is True and x['source_application_executed'] is False for x in self.witness()['illustrations']))

    def test_20_synthetic33_schema_OWN329_ALL52_not_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b28.historical_record_errors(h),[])
        for key,value in (('registry_used','findings.csv'),('findings_total',330),('process_exit_code',True),('audit_checker_self_test_cases_reported',886),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=value;self.assertTrue(b28.historical_record_errors(bad),key)
        bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B27_child']['tests_reported']=51;self.assertTrue(b28.historical_record_errors(bad))
        self.assertTrue(b28.historical_record_errors(h|{'historical_mode_count':True}))

    def test_21_actual33_archive_identity_separate_from_schema_fixture(self):
        p=A/'evidence/historical-mode-verification-07B28.json';raw=p.read_bytes();h=json.loads(raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b28.HISTORICAL_RUN_SHA);self.assertEqual(b28.historical_record_errors(h),[])
        self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b28.ENTRY,v.HEAD,v.BRANCH))
        self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']))
        self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])

    def test_22_max10_then_empty_leaves_stale_view_with_complete_master(self):
        rows=self.data();old=filtered(rows,'0','10');got=maximum_changed(rows,old,'0','')
        self.assertEqual(gids(old),['fixture-A']);self.assertEqual(gids(got['display']),['fixture-A']);self.assertFalse(got['apply_filter_called'])
        self.assertEqual(gids(filtered(rows,got['minimum_text'],got['maximum_text'])),['fixture-A','fixture-B'])

    def test_23_ASCII_whitespace_same_empty_branch_not_second_root(self):
        rows=self.data();old=filtered(rows,'0','10')
        for text in ('',' ',' \t','\r\n'):
            got=maximum_changed(rows,old,'0',text);self.assertEqual(got['display'],old);self.assertIs(got['apply_filter_called'],False)

    def test_24_nonblank_wider30_recovers_from_same_master(self):
        rows=self.data();got=maximum_changed(rows,filtered(rows,'0','10'),'0','30')
        self.assertEqual(gids(got['display']),['fixture-A','fixture-B']);self.assertTrue(got['apply_filter_called'])
        implicit=maximum_changed(rows,rows,'','10');self.assertEqual(implicit['minimum_text'],'0');self.assertEqual(gids(implicit['display']),['fixture-A'])

    def test_25_empty_minimum_unconditionally_reapplies(self):
        rows=self.data();got=minimum_changed(rows,'','')
        self.assertEqual(gids(got['display']),['fixture-A','fixture-B']);self.assertTrue(got['apply_filter_called'])
        self.assertEqual(gids(minimum_changed(rows,'30','10')['display']),['fixture-B'])

    def test_26_another_explicit_minimum_action_can_refresh_old_max_view(self):
        rows=self.data();empty=maximum_changed(rows,filtered(rows,'0','10'),'0','')
        self.assertEqual(gids(empty['display']),['fixture-A'])
        got=minimum_changed(rows,empty['maximum_text'],'0');self.assertEqual(gids(got['display']),['fixture-A','fixture-B'])

    def test_27_Clear_success_and_initial_empty_are_narrow_controls(self):
        rows=self.data();old=filtered(rows,'0','10')
        self.assertEqual(reload_result(old,rows,'success')['display'],rows)
        self.assertEqual(maximum_changed(rows,rows,'','')['display'],rows)
        self.assertEqual(maximum_changed(rows,old,'0','0')['display'],[])

    def test_28_stipulated_fill_failure_empty_master_old_display(self):
        a=self.data()[:1];got=reload_result(a,[],'failed-before-fill')
        self.assertEqual(got['master'],[]);self.assertEqual(got['display'],a)
        self.assertFalse(got['apply_filter_reached']);self.assertTrue(got['console_catch_taken']);self.assertFalse(got['source_health_flag_or_invalidation_written'])

    def test_29_partial_master_is_supplied_hypothesis_not_observed_provider(self):
        a,b=self.data()[:1],self.data()[1:];got=reload_result(a,b,'failed-with-supplied-partial-master')
        self.assertEqual((got['master'],got['display']),(b,a));self.assertFalse(self.witness()['provider_failure_or_partial_fill_observed'])
        self.assertEqual(b28.EXTENDED_IDS,['P7-046']);self.assertEqual(b28.NEW_IDS,['P7-158'])

    def test_30_ordinary_selection_exports_stale_valid_GID_consumer_boundary(self):
        rows=self.data();got=reload_result(rows[:1],[],'failed-before-fill');result=selected_result(got['display'],0)
        self.assertEqual(result,dict(done=True,gid='fixture-A'))
        selected=consumer_lookup(result,rows,1);self.assertEqual([r['day'] for r in selected],[10]);self.assertNotEqual(selected[0]['day'],20)

    def test_31_successful_new_and_successful_empty_publish_replacement(self):
        rows=self.data();self.assertEqual(reload_result(rows[:1],rows[1:],'success')['display'],rows[1:])
        got=reload_result(rows[:1],[],'success');self.assertEqual(got['display'],[]);self.assertTrue(got['apply_filter_reached']);self.assertFalse(got['console_catch_taken'])

    def test_32_not_done_sentinel_and_branch_mismatch_not_consumed(self):
        rows=self.data();self.assertEqual(consumer_lookup(selected_result([],None),rows,1),[])
        self.assertEqual(consumer_lookup(dict(done=True,gid='-1'),rows,1),[])
        self.assertEqual(consumer_lookup(selected_result(rows,0),rows,2),[])
        for bad in (dict(done=1,gid='fixture-A'),dict(done=True,gid=None),dict(done=True,gid='fixture-A',health=True)):
            with self.assertRaises(ValueError):consumer_lookup(bad,rows,1)

    def test_33_strict_supplied_record_shape_uniqueness_and_numeric_types(self):
        for bad in (None,{},self.data()*2,[self.data()[0]|{'extra':1}],[self.data()[0]|{'gid':'real-secret'}],[self.data()[0]|{'net':True}],[self.data()[0]|{'day':-1}]):
            with self.assertRaises(ValueError):records(bad)
        self.assertEqual(records(self.data()),self.data())
        for value in (True,False,1.0,'1',None,-1,100001):
            with self.assertRaises(ValueError):integer(value)

    def test_34_literal_restricted_ASCII_domain_not_dotnet_culture_parser(self):
        for text in ('1.5','1,5','-1','NaN','Infinity','١','1 OR 1=1',None,True,'99999999'):
            with self.assertRaises(ValueError):literal(text)
        self.assertEqual((literal('0'),literal('10'),literal(' \t')),(0,10,None))

    def test_35_fixture_helpers_preserve_inputs_and_reject_unbounded_text(self):
        rows=self.data();saved=copy.deepcopy(rows);old=filtered(rows,'0','10')
        got=maximum_changed(rows,old,'0','');got['display'][0]['net']=99
        self.assertEqual(rows,saved);self.assertEqual(old,filtered(rows,'0','10'))
        for text in ('bad',[],123):
            with self.assertRaises(ValueError):maximum_changed(rows,old,'0',text)
            with self.assertRaises(ValueError):minimum_changed(rows,'',text)

    def test_36_explicit_reload_outcomes_no_arbitrary_provider_execution(self):
        for outcome in ('unknown','throw-SQL',None,True):
            with self.assertRaises(ValueError):reload_result([],[],outcome)
        with self.assertRaises(ValueError):reload_result([],self.data(),'failed-before-fill')
        with self.assertRaises(ValueError):reload_result([],[],'success',maximum_text='1.1')

    def test_37_explicit_selection_index_and_gesture_not_WPF_schedule(self):
        rows=self.data()
        self.assertEqual(selected_result(rows,0,'enter-with-explicit-valid-row-index'),selected_result(rows,0))
        for index in (True,-1,2,'0'):
            with self.assertRaises(ValueError):selected_result(rows,index)
        with self.assertRaises(ValueError):selected_result(rows,0,'BtnReturn_Click')
        with self.assertRaises(ValueError):consumer_lookup(dict(done=True,gid='fixture-A'),rows,True)

    def test_38_ACTUAL_B28_parser_versionedB27_and_API15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in (('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'))+tuple((f'PHASE7_B{n}_CLI',f'B{n}') for n in range(18,28)):self.assertEqual(getattr(v,name)['default'],part)
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B28')
        for part in ('A',)+tuple('B'+str(n) for n in range(1,29)):self.assertEqual(parser.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)

    def test_39_actual_entrypoint_OWN27_before_current28(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main'))
        self.assertLess(body.index('historical_b26_validation('),body.index('historical_b27_validation('));self.assertLess(body.index('historical_b27_validation('),body.index('extend_search_snapshot('))
        self.assertIn('extend_invoice_search(historical_b27,',body);self.assertIn("phase7_part == 'B27'",body)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_cli_parser')))

    def test_40_exact_argv_proxy_preserves_other_calls_args_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'sentinel');proxy=b28.HistoricalB27Subprocess(backend,'python',Path('/a/tools'))
        kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in (proxy.expected+['--different'],['python','-B','/else/test_invoice_search_audit_validator.py']):
            proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs);self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))

    def test_41_view_exception_restore_no_global_Path_or_shared_subprocess(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel');f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b28.HistoricalB27ValidatorView(f)
        original=subprocess.run,Path.read_bytes,Path.read_text;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertEqual((subprocess.run,Path.read_bytes,Path.read_text),original);self.assertEqual(len(view.rows('findings.csv')),329);raise RuntimeError('synthetic')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_42_child_ALL52_localA_and_protected27_26_25_24_tools(self):
        tools=A/'tools';src=ast.unparse(ast.parse((tools/'run_historical_invoice_search_tests_07B28.py').read_text()))
        for token in ('loadTestsFromModule(historical_tests)','suite.countTestCases() != 52','result.testsRun != 52 or result.skipped','historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B27_CLI','b28.historical_b27_inputs('):self.assertIn(token,src)
        self.assertNotIn('unittest.skip',src)
        prov=json.loads((A/'evidence/provenance-07B28.json').read_bytes())
        for name in ('test_invoice_search_audit_validator.py','validate_invoice_search_part.py','check_invoice_search_witnesses.py','run_historical_bulk_product_tests_07B27.py','test_bulk_product_audit_validator.py','validate_bulk_product_part.py','run_historical_property_dialog_tests_07B26.py','test_property_dialog_audit_validator.py','validate_property_dialog_part.py','run_historical_row_ownership_tests_07B25.py','test_row_ownership_audit_validator.py','validate_row_ownership_part.py'):
            self.assertEqual(hashlib.sha256((tools/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])

    def test_43_actual329_fields_barriers_three_freezes_one046_extension(self):
        raw=(A/b28.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')))
        self.assertEqual(b28.registry_preservation_errors(old,cur,now,raw),[]);self.assertEqual(cur[:329],old)
        lookup={r['id']:r for r in cur}
        for root in ('P4-014','P7-132','P7-145'):self.assertEqual(lookup[root]['certainty'],'potential')
        ext=self.table('historical-extensions-07B28.csv');self.assertEqual(b28.extension_errors(ext),[])
        self.assertTrue(b28.extension_errors([]));self.assertTrue(b28.extension_errors(ext+ext));self.assertTrue(b28.extension_errors([ext[0]|dict(finding_id='P7-159')]))
        for n,h in ((b28.SNAPSHOT,b28.SNAPSHOT_SHA),(b28.SHARED_SNAPSHOT,b28.SHARED_SHA),('evidence/provenance-07B28.json',b28.PROVENANCE_SHA)):self.assertEqual(hashlib.sha256((A/n).read_bytes()).hexdigest(),h)

    def test_44_scope5_overlap5_new0_union426_sixreads_two_whole(self):
        d=json.loads((A/'evidence/scope-decision-07B28.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(5,426,5,0,426,401))
        self.assertEqual(d['historical_metadata_screen_count'],329);self.assertFalse(d['historical_body_review_claim']);self.assertEqual(d['selected_upstream_split'],'SP7B27-01')
        w=self.witness();self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),w['whole_local_search_files_selected']),(6,2))
        tuples=[]
        for r in w['bounded_source_reads_not_semantic_coverage']:
            raw=(A.parents[1]/r['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);self.assertLessEqual(r['end'],len(raw.decode('utf8').splitlines()));tuples.append((r['path'],r['start'],r['end'],r['whole_local_file_selected']))
        self.assertEqual(tuple(tuples),SOURCE_SLICES)

    def test_45_one158_one046_adjudication_no_recount_or_extra_roots(self):
        ad=self.table('root-adjudication-07B28.csv');self.assertEqual(len(ad),8)
        self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='new-local-root'],['P7-158']);self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='extended-existing-root-not-new'],['P7-046'])
        self.assertTrue(all(r['comparison_depth']==b28.DEDUP_DEPTH for r in ad));self.assertEqual(ad[0]['nearest_prior_root_ids'].split(';'),['P7-155','P7-045','P7-085'])
        self.assertEqual(ad[4]['decision'],'unadjudicated-leads-not-extra-findings')

    def test_46_actual14_residuals_three_splits_every_capability_two_substantive_plans(self):
        self.assertEqual(b28.residual_errors(self.table('residual-disposition-07B28.csv'),self.table('residual-disposition-07B27.csv')),[]);self.assertEqual(b28.split_errors(self.table('split-register-07B28.csv'),self.table('split-register-07B27.csv')),[])
        fe,iv,plans=[self.table(n+'-07B28.csv') for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b28.current_link_errors(fe,iv,plans),[])
        for r in fe:
            for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):self.assertGreater(len(r[key]),20,(r['id'],key))
            linked=[t for t in plans if t['feature_ids']==r['id']];self.assertEqual(len(linked),2);self.assertEqual(len({t['acceptance_criterion'] for t in linked}),2)
            for t in linked:
                self.assertEqual(t['status'],'not-executed');self.assertGreater(len(t['procedure']),35);self.assertGreater(len(t['acceptance_criterion']),35);self.assertIn('not-executed',t['safety_controls']);self.assertIn('إذن',t['prerequisites'])

    def test_47_reference_clock_source_capture_delivery_and_file_preserving_recovery(self):
        prov=json.loads((A/'evidence/provenance-07B28.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B28.md').read_text();self.assertEqual(b28.date_identity_errors(prov,note),[])
        self.assertTrue(b28.date_identity_errors(prov|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b28.date_identity_errors(prov,note.replace(b28.B27_CHECK_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B27.json').read_bytes());self.assertEqual(old['checkout_head'],'6eedc0640e3432c14ca0875b7f1c7806ea1e3f64');self.assertNotEqual(old['checkout_head'],b28.ENTRY)
        recovery=prov['local_git_history_reconciliation'];self.assertEqual(recovery['initial_local_tip'],v.HEAD);self.assertEqual(recovery['remote_delivered_tip'],b28.ENTRY);self.assertTrue(recovery['all802_audit_git_blobs_compared_before_reconciliation'])

    def test_48_collector_stdlib_only_no_application_execution_protected797(self):
        tree=ast.parse((A/'tools/check_search_snapshot_witnesses.py').read_text());imports=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):imports.update(x.name.split('.')[0] for x in node.names)
            elif isinstance(node,ast.ImportFrom):imports.add(node.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','pathlib','re'})
        self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        prov=json.loads((A/'evidence/provenance-07B28.json').read_bytes());self.assertEqual(len(prov['historical_artifact_sha256']),797)
        self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==h for n,h in prov['historical_artifact_sha256'].items()))
        for n in ('validate_search_snapshot_part.py','run_historical_invoice_search_tests_07B28.py','test_search_snapshot_audit_validator.py'):ast.parse((A/'tools'/n).read_text(),filename=n)


if __name__=='__main__':
    unittest.main()
