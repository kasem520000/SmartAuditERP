#!/usr/bin/env python3
"""44 read-only documentary cases; NOT WPF/SQL/row/financial acceptance.

ALL650 prior cases remain unmodified, including ALL44 B23 in an isolated child
with OWN319/raw320CRLF/indexes/presetB23. Actual current B24 parser/entrypoint,
context-local adapters, immutable captures and supplied inert row models only.
"""
from __future__ import annotations
import ast,copy,csv,hashlib,io,json
from pathlib import Path
import subprocess,sys
from types import SimpleNamespace
import unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_row_ownership_part as b24
from validate_item_ingress_part import historical_b22_inputs
from check_row_ownership_witnesses import checked_rows,consumer_controls,duplicate_dispatch,number,picker_cleanup,purchase_batch_homologue,row
A=Path(__file__).resolve().parents[1]

class RowOwnershipAuditTests(unittest.TestCase):
    def old(self,n=319):
        return[dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
          type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data)
        return s.getvalue().encode()
    def current(self):return self.old()+[self.old(1)[0]|dict(id=n,next_phase='8')for n in b24.NEW_IDS]
    def texts(self):return{n:'FROZEN:'+n for n in b24.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b24.historical_b23_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def table(self,name):return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))
    def groups(self,end):return'\n'.join(f'| G-{n:02d} | exact |'for n in range(1,end+1))+'\n'
    def contracts(self):
        fe=[];iv=[];tests=[]
        for n in range(1,19):
            fid=f'FE-{n:02d}';iid=f'INV-{n:02d}';root=b24.NEW_IDS[n-1]if n<=3 else'H'
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}'for i in(2*n-1,2*n)))
            fe.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            iv.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,
              plan_kind='finding-specific'if n<=3 else'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fe,iv,tests
    def residuals(self):
        old=[dict(id=f'RS7B23-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='upstream redacted',
          disposition='external-handoff',current_handoff_or_split_ids='H7B23-03')for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B23.csv',
          upstream_row_sha256=b24.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',
          owner_role='owner',required_redacted_input='upstream redacted; new contract',impact_if_unavailable='blocked',
          next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B24-03',
          disposition='external-handoff',runtime_status='not-executed')for r in old]
        return new,old
    def splits(self):
        old=[dict(id=f'SP7B23-{n:02d}',required_input='upstream redacted')for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B23.csv',upstream_row_sha256=b24.row_sha(r),
          title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',
          required_input='upstream redacted; new contract',next_static_action='source trace',static_exit_criterion='exit',
          status='explicit-further-static-split-not-started',runtime_status='not-executed')for r in old]
        return new,old
    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open',
          'bounded-R4h-row-ownership-delivered-residuals-open']+['planned-not-started']*6
        return[dict(part_family='7B'if n<4 else'7C',status=s,runtime_status='not-executed',
          counts_are_sessions_or_completion_percent='false')for n,s in enumerate(states)]
    def witness(self):return json.loads((A/'evidence/row-ownership-witnesses-07B24.json').read_text())
    def history_fixture(self):
        """Synthetic29 SCHEMA fixture, NEVER evidence that29 modes really ran."""
        h=json.loads((A/'evidence/historical-mode-verification-07B23.json').read_text());m=copy.deepcopy(h['historical_modes'])
        m.append(dict(mode='B23',findings_total=319,registry_used=b24.SNAPSHOT,process_exit_code=0,validation_errors=[],
          original_project_hashes_matching=827,audit_checker_self_test_cases_reported=650,audit_checker_self_test_suite_count=24,
          erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,
          historical_B23_child=dict(tests_reported=44,expected_tests=44,process_exit_code=0,result='passed',
            historical_parser_cutoff='B23-not-current-B24-default',all_original_cases_executed_unmodified=True,
            dedicated_child_launcher='tools/run_historical_item_ingress_tests_07B24.py',
            no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=29,historical_modes=m,errors=[])
    def sample(self):return[row('input-X',90),row('existing-A',11),row('last-Z',22,'4','5')]

    def test_01_OWN319_exact_raw320CRLF_and_three_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old())
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
    def test_02_reject_bad_OWN_rows_raw_BOM_LF_type_texts(self):
        f=self.fake();old=self.old();raw=self.raw(old)
        for rs,ts,b in((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),
          (old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw),(old,self.texts(),bytearray(raw))):
            with self.assertRaises(ValueError):
                with b24.historical_b23_inputs(f,rs,ts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b24.historical_b23_inputs(f,old,self.texts(),self.raw(old)):pass
    def test_03_context_local_Path_not_global_bytes_text_or_other_overlay(self):
        f=self.fake();before=Path.read_bytes,Path.read_text
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text),before)
            self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual(type(f.AUDIT)(__file__).read_text(),Path(__file__).read_text())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_text()
    def test_04_nested_OWN316_and_exception_restoration(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b22_inputs(f,self.old(316),self.texts(),self.raw(self.old(316))):
                self.assertEqual(len(f.rows('findings.csv')),316)
            self.assertEqual(len(f.rows('findings.csv')),319)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_05_OWN_row_and_text_copy_isolation(self):
        f=self.fake();old=self.old();ts=self.texts();saved=copy.deepcopy(old)
        with b24.historical_b23_inputs(f,old,ts,self.raw(old)):
            x=f.rows('findings.csv');x[0]['next_phase']='bad'
            self.assertEqual(f.rows('findings.csv'),saved);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertEqual(old,saved);self.assertEqual(ts,self.texts())
    def test_06_all319_fields_ALLnextphase_evidence_rawprefix(self):
        old=self.old();cur=self.current();self.assertEqual(b24.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed'
            self.assertTrue(b24.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)
    def test_07_only148_149_150_raw323CRLF_noBOM(self):
        old=self.old();cur=self.current()
        for bad in(cur[:-1],cur+[dict(cur[-1])],cur[:319]+list(reversed(cur[319:]))):
            self.assertTrue(b24.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in(self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):
            self.assertTrue(b24.registry_preservation_errors(old,cur,raw,self.raw(old)))
    def test_08_exact_G210_append211through215_only(self):
        self.assertEqual(b24.group_row_errors(self.groups(210),self.groups(215)),[])
        for bad in(self.groups(214),self.groups(216),self.groups(215).replace('G-99','G-98'),
          self.groups(215).replace('| G-01 | exact','| G-01 | changed')):
            self.assertTrue(b24.group_row_errors(self.groups(210),bad))
    def test_09_source_sentinel_and_same_file_range_expansion(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,
          evidence=lambda*a:calls.append(a),scoped_evidence=lambda*a,**k:calls.append((a,k)))
        for gate in('FE7B24-16','AD7B24-09','AD7B24-10'):
            b24.validate_source(f,dict(id=gate,evidence=b24.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]))
        b24.validate_source(f,dict(id='UNKNOWN',evidence=b24.DOCUMENTARY),{})
        b24.validate_source(f,dict(id='FE7B24-16',evidence='a.cs:1-2'),{});self.assertEqual((len(errors),len(calls)),(2,2))
        self.assertEqual(b24.expanded_source_evidence('a.cs:1-2;5;b.cs:7;9-10'),'a.cs:1-2;a.cs:5;b.cs:7;b.cs:9-10')
        for bad in('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b24.expanded_source_evidence(bad)
    def test_10_ordered_RO10_DO8_root_and_guard_boundaries(self):
        ro=self.table('row-ownership-lineage-07B24.csv');do=self.table('repeat-outcome-lineage-07B24.csv')
        self.assertEqual(b24.ledger_errors(ro,do),[])
        for pool,other in((ro,do),(do,ro)):
            bad=copy.deepcopy(pool);bad[0],bad[1]=bad[1],bad[0]
            self.assertTrue(b24.ledger_errors(bad,other)if pool is ro else b24.ledger_errors(other,bad))
        for pool,i in((ro,2),(ro,4),(ro,6),(ro,7),(do,0),(do,2),(do,3),(do,5),(do,7)):
            bad=copy.deepcopy(pool);bad[i]['observation']='all-accepted'
            self.assertTrue(b24.ledger_errors(bad,do)if pool is ro else b24.ledger_errors(ro,bad))
    def test_11_ledger_responsibilities_not_vacuous_or_runtime(self):
        ro=self.table('row-ownership-lineage-07B24.csv');do=self.table('repeat-outcome-lineage-07B24.csv')
        for k in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable',
                 'next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(do);bad[0][k]='';self.assertTrue(b24.ledger_errors(ro,bad),k)
        bad=copy.deepcopy(ro);bad[0]['runtime_status']='passed';self.assertTrue(b24.ledger_errors(bad,do))
        self.assertTrue(b24.ledger_errors(ro[:-1],do))
    def test_12_FE18_INV18_T36_reverse_links_and_three_roots(self):
        self.assertEqual(b24.current_link_errors(*self.contracts()),[])
        for pool,key in((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            parts=self.contracts();parts[pool][0][key]='changed';self.assertTrue(b24.current_link_errors(*parts),key)
        fs,iv,ts=self.contracts();self.assertTrue(b24.current_link_errors(fs,iv,ts[:-1]))
    def test_13_distinct_invariants_criteria_and_feature_responsibilities(self):
        for k in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            fs,iv,ts=self.contracts();fs[0][k]='';self.assertTrue(b24.current_link_errors(fs,iv,ts),k)
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b24.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b24.current_link_errors(fs,iv,ts))
    def test_14_all14_residual_ancestor_rowsha_contract_ids(self):
        cur,old=self.residuals();self.assertEqual(b24.residual_errors(cur,old),[])
        for k in('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            cur,old=self.residuals();cur[0][k]='changed';self.assertTrue(b24.residual_errors(cur,old),k)
        self.assertTrue(b24.residual_errors(cur[:-1],old))
    def test_15_residual_inputs_routes_disposition_not_approved(self):
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            cur,old=self.residuals();cur[0][k]='';self.assertTrue(b24.residual_errors(cur,old),k)
        for k,val in(('required_redacted_input','lost'),('disposition','approved'),('runtime_status','passed'),('current_handoff_or_split_ids','H7B24-06')):
            cur,old=self.residuals();cur[0][k]=val;self.assertTrue(b24.residual_errors(cur,old),k)
    def test_16_three_splits_exact_ancestry_inputs_reasoned_not_started(self):
        cur,old=self.splits();self.assertEqual(b24.split_errors(cur,old),[])
        for k in cur[0]:
            cur,old=self.splits();cur[0][k]='';self.assertTrue(b24.split_errors(cur,old),k)
        cur,old=self.splits();cur[0]['required_input']='replacement';self.assertTrue(b24.split_errors(cur,old))
    def test_17_boundedR4h_fourB_sixC_unstarted_no_sessions_percent(self):
        self.assertEqual(b24.remaining_work_errors(self.work()),[])
        for n,k,val in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),
          (0,'counts_are_sessions_or_completion_percent','true'),(0,'part_family','7C')):
            work=self.work();work[n][k]=val;self.assertTrue(b24.remaining_work_errors(work),k)
        self.assertTrue(b24.remaining_work_errors(self.work()[:-1]))
    def test_18_metadata_strict_boolean_integer_and_B10_addendum(self):
        self.assertEqual(b24.witness_metadata_errors(self.witness()),[])
        for k,val in(('application_code_imported_or_executed',0),('dotnet_wpf_sql_or_excel_executed',None),
          ('erp_runtime_tests_executed',False),('illustration_count',14.0),('B_R4h_bounded_not_whole7B_closure',1),
          ('phase7C_started',True),('phase8_authorized_or_started',True),('historical143_and146_not_recounted_or_extended',1)):
            self.assertTrue(b24.witness_metadata_errors(self.witness()|{k:val}),k)
        bad=self.witness();bad['retained_additive_B10_arithmetic_erratum']['reference_cost']=10
        self.assertTrue(b24.witness_metadata_errors(bad))
    def test_19_actual_witness_stdout_hash_and_readonly_recompute(self):
        self.assertEqual(hashlib.sha256((A/'evidence/row-ownership-witnesses-07B24.json').read_bytes()).hexdigest(),b24.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_row_ownership_witnesses.py')],capture_output=True,text=True,timeout=25)
        self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,'');self.assertEqual(json.loads(run.stdout),self.witness())
    def test_20_synthetic29_schema_OWN319_ALL44_not_genuine_execution(self):
        h=self.history_fixture();self.assertEqual(b24.historical_record_errors(h),[])
        for n,k,val in((28,'findings_total',322),(28,'registry_used','findings.csv'),(28,'stdout_sha256','bad'),
          (28,'audit_checker_self_test_cases_reported',694),(0,'audit_checker_self_test_cases_reported',0),
          (28,'erp_runtime_tests_executed',False)):
            h=self.history_fixture();h['historical_modes'][n][k]=val;self.assertTrue(b24.historical_record_errors(h),k)
        h=self.history_fixture();h['historical_modes'][-1]['historical_B23_child']['suite_own_registry_path_is_context_local_not_global']=False
        self.assertTrue(b24.historical_record_errors(h));h=self.history_fixture();h['historical_modes']=h['historical_modes'][:-1]
        self.assertTrue(b24.historical_record_errors(h))
    def test_21_actual29_capture_identity_separate_from_schema_fixture(self):
        raw=(A/'evidence/historical-mode-verification-07B24.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b24.HISTORICAL_RUN_SHA)
        h=json.loads(raw);self.assertEqual(b24.historical_record_errors(h),[]);self.assertEqual(h['checkout_head'],b24.ENTRY)
        self.assertEqual(h['current_actual_CLI_default'],'B24');self.assertEqual(h['historical_mode_count'],29)
    def test_22_populated_current_row_is_removed_on_false_result(self):
        p=picker_cleanup(self.sample(),0,False,-1)
        self.assertEqual((p['removed_ref'],[r['ref']for r in p['rows']]),('input-X',['existing-A','last-Z']))
        self.assertTrue(p['cleanup_has_no_empty_seed_ownership_test']);self.assertFalse(p['application_executed'])
    def test_23_invalid_confirmation_and_positive_branch_limit(self):
        self.assertEqual(picker_cleanup(self.sample(),0,True,0)['removed_ref'],'input-X')
        p=picker_cleanup(self.sample(),0,True,11);self.assertEqual(p['rows'],self.sample())
        self.assertTrue(p['positive_confirmation_branch_not_modelled']);self.assertIsNone(p['removed_ref'])
    def test_24_owned_blank_seed_and_out_of_range_controls(self):
        seed=row('seed',0,'0','0');self.assertEqual(picker_cleanup(self.sample()+[seed],3,False,-1)['removed_ref'],'seed')
        for i in(-1,3):self.assertIsNone(picker_cleanup(self.sample(),i,False,-1)['removed_ref'])
    def test_25_cleanup_types_and_result_copy_isolation(self):
        rows=self.sample();saved=copy.deepcopy(rows);p=picker_cleanup(rows,0,False,-1);p['rows'][0]['qty']='99';self.assertEqual(rows,saved)
        for index,done,item in((True,False,-1),(0,0,-1),(0,False,False)):
            with self.assertRaises(ValueError):picker_cleanup(rows,index,done,item)
    def test_26_wire2_clobbers_unrelated_last_identity_before_hydration(self):
        p=duplicate_dispatch(self.sample(),0,11,2)
        self.assertEqual(p['overwritten_unrelated_ref'],'last-Z');self.assertEqual(len(p['rows']),3)
        self.assertEqual(p['rows'][-1]['item_id'],11);self.assertTrue(p['identity_only_before_hydration'])
        self.assertTrue(p['buttons_not_semantically_repaired']);self.assertFalse(p['application_executed'])
    def test_27_wire2_blank_seed_and_matching_last_counterexamples(self):
        for rows,current in((self.sample()[:2]+[row('seed',0,'0','0')],2),([self.sample()[1]],0)):
            p=duplicate_dispatch(rows,current,11,2);self.assertIsNone(p['overwritten_unrelated_ref']);self.assertEqual(len(p['rows']),len(rows))
    def test_28_wire1_recalculates_following_ref_flat40_vs50(self):
        p=duplicate_dispatch(self.sample(),0,11,1)
        self.assertEqual((p['removed_ref'],p['calculated_ref'],p['attempted_calculation_index']),('input-X','last-Z',1))
        self.assertEqual(p['stale_flat_derived_refs'],['existing-A'])
        self.assertEqual((number(p['flat_stored_sum']),number(p['flat_quantity_reference_sum'])),(40,50))
    def test_29_wire1_old_index_guarded_null_not_exception(self):
        p=duplicate_dispatch(self.sample()[:2],0,11,1)
        self.assertIsNone(p['calculated_ref']);self.assertEqual(p['attempted_calculation_index'],1)
        self.assertEqual(p['stale_flat_derived_refs'],['existing-A'])
    def test_30_wire1_current_after_or_equal_keeps_correct_reference(self):
        a,b,z=self.sample()
        for rows,current in(([b,a],1),([b,z],0)):
            p=duplicate_dispatch(rows,current,11,1);self.assertEqual(p['calculated_ref'],'existing-A');self.assertEqual(p['stale_flat_derived_refs'],[])
        self.assertIsNone(duplicate_dispatch([b,z],0,11,1)['removed_ref'])
    def test_31_wire0_and3_local_no_row_mutation_not_all_cancel_acceptance(self):
        for action in(0,3):
            p=duplicate_dispatch(self.sample(),0,11,action);self.assertEqual(p['rows'],self.sample())
            self.assertIsNone(p['removed_ref']);self.assertIsNone(p['calculated_ref'])
    def test_32_duplicate_strict_index_ID_action_unique_hit_and_copy(self):
        rows=self.sample();saved=copy.deepcopy(rows);p=duplicate_dispatch(rows,0,11,1);p['rows'][0]['ref']='altered';self.assertEqual(rows,saved)
        for index,item,action in((True,11,1),(-1,11,1),(0,True,1),(0,11,True),(0,11,4),(0,99,1)):
            with self.assertRaises(ValueError):duplicate_dispatch(rows,index,item,action)
        with self.assertRaises(ValueError):duplicate_dispatch(rows+[row('second-A',11)],0,11,1)
    def test_33_batch_homologue_same146_no_recount_and_copy(self):
        prefix=[90];ids=[11,22];p=purchase_batch_homologue(prefix,ids,0)
        self.assertEqual((p['rows'],prefix,ids),([22],[90],[11,22]));self.assertTrue(p['same_cause_146_not_new_or_extended'])
        self.assertEqual(purchase_batch_homologue([90],[11],0)['rows'],[11])
        for args in(([90],[90],0),([90],[11,11],0),([90],[True],0),([90],[11],True),([90],[],0)):
            with self.assertRaises(ValueError):purchase_batch_homologue(*args)
    def test_34_three_consumer_controls_same143_hidden_wire_and_append(self):
        p={i:consumer_controls(i)for i in range(4)}
        self.assertFalse(p[1]['initial_account_accepts_only_wire2']);self.assertTrue(p[2]['initial_account_accepts_only_wire2'])
        self.assertTrue(all(x['initial_quantity_button_hidden']and x['same_cause_143_not_new_or_extended']for x in p.values()))
        self.assertEqual(p[2]['production_effect'],'append-new-reference');self.assertFalse(p[2]['financial_or_production_acceptance'])
        for bad in(True,4,-1,'2'):
            with self.assertRaises(ValueError):consumer_controls(bad)
    def test_35_flat_rows_exact_schema_refs_types_finite_and_initial_consistency(self):
        for rows in([row('A',11),row('A',22)],[row('A',True)],[row('A',11)|dict(extra='x')],
          [row('A',11)|dict(derived='0')],[row('A',11)|dict(qty='NaN')],[row('A',11)|dict(price='Infinity')],
          [row('A',11)|dict(qty=2)],[row('A',11)|dict(qty='-1')],{},[dict(ref='')]):
            with self.assertRaises(ValueError):checked_rows(rows)
        rows=self.sample();out=checked_rows(rows);out[0]['ref']='changed';self.assertEqual(rows,self.sample())
    def test_36_real_ledgers_root_links_and_zero_historical_extensions(self):
        ro=self.table('row-ownership-lineage-07B24.csv');do=self.table('repeat-outcome-lineage-07B24.csv')
        self.assertEqual(ro[2]['finding_ids'],'P7-148');self.assertEqual(ro[4]['finding_ids'],'P7-149');self.assertEqual(ro[6]['finding_ids'],'P7-150')
        self.assertEqual(do[0]['finding_ids'],'P7-143');self.assertEqual(do[7]['finding_ids'],'P7-146')
        self.assertEqual(self.table('historical-extensions-07B24.csv'),[])
    def test_37_ACTUAL_B24_parser_versioned_B23_and_API_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in(('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'),('PHASE7_B18_CLI','B18'),
          ('PHASE7_B19_CLI','B19'),('PHASE7_B20_CLI','B20'),('PHASE7_B21_CLI','B21'),('PHASE7_B22_CLI','B22'),('PHASE7_B23_CLI','B23')):
            self.assertEqual(getattr(v,name)['default'],part)
        p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B24')
        for part in('A',)+tuple('B'+str(n)for n in range(1,25)):
            self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(p.parse_args(['--through-phase','2']).through_phase,2)
    def test_38_real_entrypoint_routes_historical23_before_current_ownership(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]))
        self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'))
        self.assertLess(body.index('historical_b22_validation('),body.index('historical_b23_validation('))
        self.assertLess(body.index('historical_b23_validation('),body.index('extend_row_ownership('))
        self.assertIn('extend_item_ingress(historical_b23,',body);self.assertIn("phase7_part == 'B23'",body)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser')))
    def test_39_exact_argv_redirect_preserves_other_calls_positionals_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda*a,**k:calls.append((a,k))or'sentinel')
        proxy=b24.HistoricalB23Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in(proxy.expected+['--different'],['python','-B','/else/test_item_ingress_audit_validator.py']):
            proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs);self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))
    def test_40_facade_restore_no_shared_subprocess_or_Path_mutation(self):
        backend=SimpleNamespace(run=lambda*a,**k:'sentinel');f=self.fake();f.subprocess=backend;f.sys=SimpleNamespace(executable='python')
        view=b24.HistoricalB23ValidatorView(f);original=subprocess.run,Path.read_bytes,Path.read_text;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertEqual((subprocess.run,Path.read_bytes,Path.read_text),original)
                self.assertEqual(len(view.rows('findings.csv')),319);raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_41_historical_child_ALL44_local_suite_A_restore_and_protected_hashes(self):
        p=A/'tools';s=ast.unparse(ast.parse((p/'run_historical_item_ingress_tests_07B24.py').read_text()))
        for token in('loadTestsFromModule(historical_tests)','suite.countTestCases() != 44','result.testsRun != 44 or result.skipped',
          'historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B23_CLI','b24.historical_b23_inputs('):
            self.assertIn(token,s)
        self.assertNotIn('unittest.skip',s);prov=json.loads((A/'evidence/provenance-07B24.json').read_text())
        for name in('test_item_ingress_audit_validator.py','validate_item_ingress_part.py','check_item_ingress_witnesses.py',
          'run_historical_contract_item_tests_07B23.py','test_contract_item_audit_validator.py',
          'test_amountword_contract_audit_validator.py','test_barcode_contract_audit_validator.py','test_navigation_contract_audit_validator.py'):
            self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])
    def test_42_real_frozen319_raw320_all_fields_potential_barriers_no_extensions(self):
        raw=(A/b24.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')))
        self.assertEqual(b24.registry_preservation_errors(old,cur,now,raw),[]);self.assertEqual(cur[:319],old)
        lookup={r['id']:r for r in cur}
        for name in('P4-014','P7-132','P7-145'):self.assertEqual(lookup[name]['certainty'],'potential')
        self.assertEqual(self.table('historical-extensions-07B24.csv'),[])
        for name,digest in((b24.SNAPSHOT,b24.SNAPSHOT_SHA),(b24.SHARED_SNAPSHOT,b24.SHARED_SHA),('evidence/provenance-07B24.json',b24.PROVENANCE_SHA)):
            self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
    def test_43_scope10_9overlap1new_union419_and34reads3consumers_not_census(self):
        d=json.loads((A/'evidence/scope-decision-07B24.json').read_text());b=d['bookkeeping']
        self.assertEqual(tuple(b[k]for k in('selected_paths','prior_union','overlap','new','union','complement')),(10,418,9,1,419,408))
        self.assertEqual(b['complement_kinds'],{'source':343,'generated-artifact':61,'project-or-resource':4})
        self.assertEqual(d['selected_upstream_split'],'SP7B23-01');self.assertFalse(d['historical_body_review_claim'])
        for k in('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):self.assertIs(d[k],False)
        w=self.witness();self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),w['selected_repeat_consumers']),(34,3))
        self.assertFalse(w['all477_sources_or_all11_constructors_body_reviewed']);self.assertTrue(w['selected_paths_strict_utf8_decode'])
    def test_44_three_new_certainty_roots_two_same_cause_comparisons_full_residuals(self):
        cur=list(csv.DictReader(io.StringIO((A/'findings.csv').read_text(),newline='')))
        self.assertEqual([r['certainty']for r in cur[319:]],['confirmed']*3)
        ad=self.table('root-adjudication-07B24.csv');self.assertEqual([r['current_root_ids']for r in ad if r['decision']=='new-local-root'],b24.NEW_IDS)
        self.assertEqual([r['current_root_ids']for r in ad if r['decision']=='same-cause-homologues-not-extended-or-recounted'],['P7-143','P7-146'])
        self.assertTrue(all(r['comparison_depth']==b24.DEDUP_DEPTH for r in ad))
        self.assertEqual(b24.residual_errors(self.table('residual-disposition-07B24.csv'),self.table('residual-disposition-07B23.csv')),[])
        self.assertEqual(b24.split_errors(self.table('split-register-07B24.csv'),self.table('split-register-07B23.csv')),[])

if __name__=='__main__':unittest.main()
