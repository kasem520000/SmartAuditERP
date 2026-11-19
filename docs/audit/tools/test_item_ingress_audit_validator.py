#!/usr/bin/env python3
"""44 read-only documentary cases; NOT picker/import/WPF/financial acceptance.

ALL606 earlier cases remain unmodified, including ALL40 B22 in an explicit
historical OWN316/presetB22 child. Tests inspect the actual current CLI/parser/
entrypoint, local adapters, frozen identities and inert supplied models only.
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
import validate_item_ingress_part as b23
from validate_contract_item_part import historical_b21_inputs
from check_item_ingress_witnesses import selection_history,sales_batch,purchase_batch_control,import_hydration,msg_constructors
A=Path(__file__).resolve().parents[1]

class ItemIngressAuditTests(unittest.TestCase):
    def old(self,n=316):
        return[dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
          type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data)
        return s.getvalue().encode()
    def current(self):return self.old()+[self.old(1)[0]|dict(id=n,next_phase='8')for n in b23.NEW_IDS]
    def texts(self):return{n:'FROZEN:'+n for n in b23.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b23.historical_b22_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def table(self,name):return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))
    def groups(self,end):return'\n'.join(f'| G-{n:02d} | exact |'for n in range(1,end+1))+'\n'
    def contracts(self):
        fe=[];iv=[];tests=[]
        for n in range(1,19):
            fid=f'FE-{n:02d}';iid=f'INV-{n:02d}';root=b23.NEW_IDS[n-1]if n<=3 else'H'
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}'for i in(2*n-1,2*n)))
            fe.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            iv.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,
               plan_kind='finding-specific'if n<=3 else'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fe,iv,tests
    def residuals(self):
        old=[dict(id=f'RS7B22-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='upstream redacted',
          disposition='external-handoff',current_handoff_or_split_ids='H7B22-03')for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B22.csv',
          upstream_row_sha256=b23.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',
          owner_role='owner',required_redacted_input='upstream redacted; new contract',impact_if_unavailable='blocked',
          next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B23-03',
          disposition='external-handoff',runtime_status='not-executed')for r in old]
        return new,old
    def splits(self):
        old=[dict(id=f'SP7B22-{n:02d}',required_input='upstream redacted')for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B22.csv',upstream_row_sha256=b23.row_sha(r),
          title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',
          required_input='upstream redacted; new contract',next_static_action='source trace',static_exit_criterion='exit',
          status='explicit-further-static-split-not-started',runtime_status='not-executed')for r in old]
        return new,old
    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open',
          'bounded-R4g-item-ingress-delivered-residuals-open']+['planned-not-started']*6
        return[dict(part_family='7B'if n<4 else'7C',status=s,runtime_status='not-executed',
          counts_are_sessions_or_completion_percent='false')for n,s in enumerate(states)]
    def witness(self):return json.loads((A/'evidence/item-ingress-witnesses-07B23.json').read_text())
    def history_fixture(self):
        """Synthetic28 SCHEMA fixture, NEVER evidence that28 modes really ran."""
        h=json.loads((A/'evidence/historical-mode-verification-07B22.json').read_text());m=copy.deepcopy(h['historical_modes'])
        m.append(dict(mode='B22',findings_total=316,registry_used=b23.SNAPSHOT,process_exit_code=0,validation_errors=[],
          original_project_hashes_matching=827,audit_checker_self_test_cases_reported=606,audit_checker_self_test_suite_count=23,
          erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,
          historical_B22_child=dict(tests_reported=40,expected_tests=40,process_exit_code=0,result='passed',
            historical_parser_cutoff='B22-not-current-B23-default',all_original_cases_executed_unmodified=True,
            dedicated_child_launcher='tools/run_historical_contract_item_tests_07B23.py',
            no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=28,historical_modes=m,errors=[])
    def seed(self):return dict(code='A',description='import-A',unit='PACK',quantity='7',price='50')
    def catalog(self):return dict(item_id=11,unit='EACH',price='20')

    def test_01_OWN316_exact_raw317CRLF_and_three_texts(self):
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
                with b23.historical_b22_inputs(f,rs,ts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b23.historical_b22_inputs(f,old,self.texts(),self.raw(old)):pass
    def test_03_context_local_Path_not_global_bytes_text_or_other_overlay(self):
        f=self.fake();before=Path.read_bytes,Path.read_text
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text),before)
            self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual(type(f.AUDIT)(__file__).read_text(),Path(__file__).read_text())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_text()
    def test_04_nested_OWN313_and_exception_restoration(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b21_inputs(f,self.old(313),self.texts(),self.raw(self.old(313))):
                self.assertEqual(len(f.rows('findings.csv')),313)
            self.assertEqual(len(f.rows('findings.csv')),316)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_05_OWN_row_and_text_copy_isolation(self):
        f=self.fake();old=self.old();ts=self.texts();saved=copy.deepcopy(old)
        with b23.historical_b22_inputs(f,old,ts,self.raw(old)):
            x=f.rows('findings.csv');x[0]['next_phase']='bad'
            self.assertEqual(f.rows('findings.csv'),saved);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertEqual(old,saved);self.assertEqual(ts,self.texts())
    def test_06_all316_fields_ALLnextphase_evidence_rawprefix(self):
        old=self.old();cur=self.current();self.assertEqual(b23.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed'
            self.assertTrue(b23.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)
    def test_07_only145_146_147_raw320CRLF_noBOM(self):
        old=self.old();cur=self.current()
        for bad in(cur[:-1],cur+[dict(cur[-1])],cur[:316]+list(reversed(cur[316:]))):
            self.assertTrue(b23.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in(self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):
            self.assertTrue(b23.registry_preservation_errors(old,cur,raw,self.raw(old)))
    def test_08_exact_G205_append206through210_only(self):
        self.assertEqual(b23.group_row_errors(self.groups(205),self.groups(210)),[])
        for bad in(self.groups(209),self.groups(211),self.groups(210).replace('G-99','G-98'),
          self.groups(210).replace('| G-01 | exact','| G-01 | changed')):
            self.assertTrue(b23.group_row_errors(self.groups(205),bad))
    def test_09_source_sentinel_and_same_file_range_expansion(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,
          evidence=lambda*a:calls.append(a),scoped_evidence=lambda*a,**k:calls.append((a,k)))
        b23.validate_source(f,dict(id='FE7B23-16',evidence=b23.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b23.validate_source(f,dict(id='UNKNOWN',evidence=b23.DOCUMENTARY),{})
        b23.validate_source(f,dict(id='FE7B23-16',evidence='a.cs:1-2'),{});self.assertEqual((len(errors),len(calls)),(2,2))
        self.assertEqual(b23.expanded_source_evidence('a.cs:1-2;5;b.cs:7;9-10'),'a.cs:1-2;a.cs:5;b.cs:7;b.cs:9-10')
        for bad in('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b23.expanded_source_evidence(bad)
    def test_10_ordered_SB8_IM8_potential_cursor_seed_and_limits(self):
        sb=self.table('selection-batch-lineage-07B23.csv');im=self.table('import-field-lineage-07B23.csv')
        self.assertEqual(b23.ledger_errors(sb,im),[])
        for pool,other in((sb,im),(im,sb)):
            bad=copy.deepcopy(pool);bad[0],bad[1]=bad[1],bad[0]
            self.assertTrue(b23.ledger_errors(bad,other)if pool is sb else b23.ledger_errors(other,bad))
        for i in(1,4,5,6):
            bad=copy.deepcopy(sb);bad[i]['observation']='all-accepted';self.assertTrue(b23.ledger_errors(bad,im))
        bad=copy.deepcopy(im);bad[6]['observation']='same-144-only';self.assertTrue(b23.ledger_errors(sb,bad))
    def test_11_ledger_responsibilities_not_vacuous_or_runtime(self):
        sb=self.table('selection-batch-lineage-07B23.csv');im=self.table('import-field-lineage-07B23.csv')
        for k in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable',
                 'next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(im);bad[0][k]='';self.assertTrue(b23.ledger_errors(sb,bad),k)
        bad=copy.deepcopy(sb);bad[0]['runtime_status']='passed';self.assertTrue(b23.ledger_errors(bad,im))
        self.assertTrue(b23.ledger_errors(sb[:-1],im))
    def test_12_FE18_INV18_T36_reverse_links_and_root_specific(self):
        self.assertEqual(b23.current_link_errors(*self.contracts()),[])
        for pool,key in((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            parts=self.contracts();parts[pool][0][key]='changed';self.assertTrue(b23.current_link_errors(*parts),key)
        fs,iv,ts=self.contracts();self.assertTrue(b23.current_link_errors(fs,iv,ts[:-1]))
    def test_13_distinct_invariants_criteria_and_feature_responsibilities(self):
        for k in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            fs,iv,ts=self.contracts();fs[0][k]='';self.assertTrue(b23.current_link_errors(fs,iv,ts),k)
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b23.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b23.current_link_errors(fs,iv,ts))
    def test_14_all14_residual_ancestor_rowsha_contract_ids(self):
        cur,old=self.residuals();self.assertEqual(b23.residual_errors(cur,old),[])
        for k in('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            cur,old=self.residuals();cur[0][k]='changed';self.assertTrue(b23.residual_errors(cur,old),k)
        self.assertTrue(b23.residual_errors(cur[:-1],old))
    def test_15_residual_inputs_routes_disposition_not_approved(self):
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            cur,old=self.residuals();cur[0][k]='';self.assertTrue(b23.residual_errors(cur,old),k)
        for k,val in(('required_redacted_input','lost'),('disposition','approved'),('runtime_status','passed'),('current_handoff_or_split_ids','H7B23-06')):
            cur,old=self.residuals();cur[0][k]=val;self.assertTrue(b23.residual_errors(cur,old),k)
    def test_16_three_splits_exact_ancestry_inputs_reasoned_not_started(self):
        cur,old=self.splits();self.assertEqual(b23.split_errors(cur,old),[])
        for k in cur[0]:
            cur,old=self.splits();cur[0][k]='';self.assertTrue(b23.split_errors(cur,old),k)
        cur,old=self.splits();cur[0]['required_input']='replacement';self.assertTrue(b23.split_errors(cur,old))
    def test_17_boundedR4g_fourB_sixC_unstarted_no_sessions_percent(self):
        self.assertEqual(b23.remaining_work_errors(self.work()),[])
        for n,k,val in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),
          (0,'counts_are_sessions_or_completion_percent','true'),(0,'part_family','7C')):
            work=self.work();work[n][k]=val;self.assertTrue(b23.remaining_work_errors(work),k)
        self.assertTrue(b23.remaining_work_errors(self.work()[:-1]))
    def test_18_metadata_strict_boolean_integer_and_B10_addendum(self):
        self.assertEqual(b23.witness_metadata_errors(self.witness()),[])
        for k,val in(('application_code_imported_or_executed',0),('dotnet_wpf_sql_or_excel_executed',None),
          ('erp_runtime_tests_executed',False),('illustration_count',12.0),('B_R4g_bounded_not_whole7B_closure',1),
          ('phase7C_started',True),('phase8_authorized_or_started',True)):
            self.assertTrue(b23.witness_metadata_errors(self.witness()|{k:val}),k)
        bad=self.witness();bad['retained_additive_B10_arithmetic_erratum']['reference_cost']=10
        self.assertTrue(b23.witness_metadata_errors(bad))
    def test_19_actual_witness_stdout_hash_and_readonly_recompute(self):
        self.assertEqual(hashlib.sha256((A/'evidence/item-ingress-witnesses-07B23.json').read_bytes()).hexdigest(),b23.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_item_ingress_witnesses.py')],capture_output=True,text=True,timeout=25)
        self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,'');self.assertEqual(json.loads(run.stdout),self.witness())
    def test_20_synthetic28_schema_OWN316_ALL40_not_genuine_execution(self):
        h=self.history_fixture();self.assertEqual(b23.historical_record_errors(h),[])
        for n,k,val in((27,'findings_total',319),(27,'registry_used','findings.csv'),(27,'stdout_sha256','bad'),
          (27,'audit_checker_self_test_cases_reported',650),(0,'audit_checker_self_test_cases_reported',0),
          (27,'erp_runtime_tests_executed',False)):
            h=self.history_fixture();h['historical_modes'][n][k]=val;self.assertTrue(b23.historical_record_errors(h),k)
        h=self.history_fixture();h['historical_modes'][-1]['historical_B22_child']['suite_own_registry_path_is_context_local_not_global']=False
        self.assertTrue(b23.historical_record_errors(h));h=self.history_fixture();h['historical_modes']=h['historical_modes'][:-1]
        self.assertTrue(b23.historical_record_errors(h))
    def test_21_actual28_capture_identity_separate_from_schema_fixture(self):
        raw=(A/'evidence/historical-mode-verification-07B23.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b23.HISTORICAL_RUN_SHA)
        h=json.loads(raw);self.assertEqual(b23.historical_record_errors(h),[]);self.assertEqual(h['checkout_head'],b23.ENTRY)
        self.assertEqual(h['current_actual_CLI_default'],'B23');self.assertEqual(h['historical_mode_count'],28)
    def test_22_selection_deselected_A_stays_in_accumulated_result_potential(self):
        p=selection_history([[11],[22]],22)
        self.assertEqual((p['accepted_batch'],p['stale_vs_current_selection']),([11,22],[11]))
        self.assertTrue(p['selection_semantics_owner_unresolved']);self.assertFalse(p['wpf_executed'])
    def test_23_selection_single_and_ctrl_removal_dedup_not_reconcile(self):
        self.assertEqual(selection_history([[22]],22)['stale_vs_current_selection'],[])
        p=selection_history([[11,22],[22]],22);self.assertEqual(p['accepted_batch'],[11,22])
        self.assertEqual(len(set(p['accepted_batch'])),2)
        self.assertEqual(selection_history([[11,22]],11)['accepted_batch'],[22,11])
    def test_24_ISDone_false_gate_is_local_not_modal_trial(self):
        p=selection_history([[11],[22]],22,False)
        self.assertEqual(p['accepted_batch'],[]);self.assertEqual(p['returned_itemlist_if_confirmed'],[11,22])
    def test_25_selection_exact_IDs_shapes_confirmation(self):
        for args in(([[True]],True),([[11,11]],11),([[0]],0),([[11]],22),([],11),([[11]],11,1)):
            with self.assertRaises(ValueError):selection_history(*args)
    def test_26_distinct_batch_replaces_prior_row_without_repeat_dialog(self):
        p=sales_batch([90],[11,22]);self.assertEqual(p['rows'],[90,22]);self.assertEqual(p['removed_prior_batch_ids'],[11])
        self.assertFalse(p['duplicate_dialog_executed']);self.assertFalse(p['application_executed'])
    def test_27_three_distinct_items_only_last_remains_prefix_retained(self):
        p=sales_batch([90,91],[11,22,33]);self.assertEqual(p['rows'],[90,91,33]);self.assertEqual(p['removed_prior_batch_ids'],[11,22])
        self.assertEqual(sales_batch([],[11,22,33])['rows'],[33])
    def test_28_single_and_cancel_batch_counterexamples(self):
        self.assertEqual(sales_batch([90],[11])['rows'],[90,11]);self.assertEqual(sales_batch([90],[11,22],False)['rows'],[90])
        self.assertEqual(sales_batch([90],[])['rows'],[90])
    def test_29_other_editor_seeds_each_iteration_control(self):
        p=purchase_batch_control([90],[11,22]);self.assertEqual(p['rows'],[90,11,22]);self.assertTrue(p['per_iteration_empty_seed_supplied'])
        self.assertEqual(purchase_batch_control([90],[11],False)['rows'],[90])
    def test_30_batch_reject_duplicate_overlap_boolean_and_copy_isolation(self):
        for fn in(sales_batch,purchase_batch_control):
            before=[90];sel=[11,22];fn(before,sel);self.assertEqual((before,sel),([90],[11,22]))
            for args in(([90],[90]),([90],[11,11]),([90],[True]),([90],[11],1)):
                with self.assertRaises(ValueError):fn(*args)
    def test_31_sales_seed_four_fields_lost_on_supplied_success(self):
        p=import_hydration(self.seed(),self.catalog())
        self.assertEqual(p['fields_changed'],['description','unit','quantity','price'])
        self.assertEqual(p['after_hydration'],dict(code='A',description='',unit='EACH',quantity='1',price='20'))
        self.assertFalse(p['duplicate_dialog_needed']);self.assertFalse(p['actual_price_or_conversion_policy_accepted'])
    def test_32_purchase_same_cause_distinct_implementation(self):
        p=import_hydration(self.seed(),self.catalog(),editor='purchase')
        self.assertEqual(p['editor'],'purchase');self.assertEqual(len(p['fields_changed']),4);self.assertTrue(p['rdAuto_off_supplied'])
    def test_33_equal_default_control_does_not_accept_importer(self):
        same=dict(code='A',description='',unit='EACH',quantity='1',price='20')
        self.assertEqual(import_hydration(same,self.catalog())['fields_changed'],[])
        self.assertEqual(import_hydration(self.seed()|dict(description=''),self.catalog())['fields_changed'],['unit','quantity','price'])
    def test_34_failed_branch_explicitly_outside_model_and_inputs_inert_copied(self):
        seed=self.seed();cat=self.catalog();saved=copy.deepcopy((seed,cat));p=import_hydration(seed,cat,False)
        self.assertEqual((seed,cat),saved);self.assertEqual(p['fields_changed'],[])
        self.assertTrue(p['failed_or_no_match_branch_not_modelled']);self.assertFalse(p['application_executed'])
        p['after_hydration']['description']='changed';self.assertEqual(seed,self.seed())
    def test_35_import_shapes_exact_types_finite_values_no_policy(self):
        for seed,cat,succ,editor in((self.seed()|dict(extra='x'),self.catalog(),True,'sales'),
          (self.seed(),self.catalog()|dict(item_id=True),True,'sales'),(self.seed(),self.catalog(),1,'sales'),
          (self.seed(),self.catalog(),True,'other'),(self.seed()|dict(quantity='NaN'),self.catalog(),True,'sales'),
          (self.seed(),self.catalog()|dict(price='Infinity'),True,'sales'),(self.seed()|dict(price=50),self.catalog(),True,'sales')):
            with self.assertRaises(ValueError):import_hydration(seed,cat,succ,editor)
    def test_36_literal_constructor_discovery_masks_strings_comments_not_callgraph(self):
        s='// new MsgExistItem();\nvar s="new MsgExistItem()";\nnew MsgExistItem(); /* new MsgExistItem(); */\nnew\n MsgExistItem ( );'
        self.assertEqual(msg_constructors(s,'toy.cs'),[dict(path='toy.cs',line=3),dict(path='toy.cs',line=4)])
        self.assertEqual(msg_constructors('new OtherMsgExistItem();','toy.cs'),[])
    def test_37_ACTUAL_B23_parser_versioned_B22_and_API_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in(('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'),('PHASE7_B18_CLI','B18'),
          ('PHASE7_B19_CLI','B19'),('PHASE7_B20_CLI','B20'),('PHASE7_B21_CLI','B21'),('PHASE7_B22_CLI','B22')):
            self.assertEqual(getattr(v,name)['default'],part)
        p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B23')
        for part in('A',)+tuple('B'+str(n)for n in range(1,24)):
            self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(p.parse_args(['--through-phase','2']).through_phase,2)
    def test_38_real_entrypoint_routes_historical22_before_current_ingress(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]))
        self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'))
        self.assertLess(body.index('historical_b21_validation('),body.index('historical_b22_validation('))
        self.assertLess(body.index('historical_b22_validation('),body.index('extend_item_ingress('))
        self.assertIn('extend_contract_items(historical_b22,',body);self.assertIn("phase7_part == 'B22'",body)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser')))
    def test_39_exact_argv_redirect_preserves_other_calls_positionals_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda*a,**k:calls.append((a,k))or'sentinel')
        proxy=b23.HistoricalB22Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in(proxy.expected+['--different'],['python','-B','/else/test_contract_item_audit_validator.py']):
            proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs);self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))
    def test_40_facade_restore_no_shared_subprocess_or_Path_mutation(self):
        backend=SimpleNamespace(run=lambda*a,**k:'sentinel');f=self.fake();f.subprocess=backend;f.sys=SimpleNamespace(executable='python')
        view=b23.HistoricalB22ValidatorView(f);original=subprocess.run,Path.read_bytes,Path.read_text;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertEqual((subprocess.run,Path.read_bytes,Path.read_text),original)
                self.assertEqual(len(view.rows('findings.csv')),316);raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_41_historical_child_ALL40_local_suite_A_restore_and_protected_hashes(self):
        p=A/'tools';s=ast.unparse(ast.parse((p/'run_historical_contract_item_tests_07B23.py').read_text()))
        for token in('loadTestsFromModule(historical_tests)','suite.countTestCases() != 40','result.testsRun != 40 or result.skipped',
          'historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B22_CLI','b23.historical_b22_inputs('):
            self.assertIn(token,s)
        self.assertNotIn('unittest.skip',s);prov=json.loads((A/'evidence/provenance-07B23.json').read_text())
        for name in('test_contract_item_audit_validator.py','validate_contract_item_part.py','check_contract_item_witnesses.py',
          'run_historical_amountword_tests_07B22.py','test_amountword_contract_audit_validator.py',
          'test_barcode_contract_audit_validator.py','test_navigation_contract_audit_validator.py','test_caller_request_audit_validator.py'):
            self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])
    def test_42_real_frozen316_raw317_all_old_rows_potential_barriers_no_extensions(self):
        raw=(A/b23.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')))
        self.assertEqual(b23.registry_preservation_errors(old,cur,now,raw),[]);self.assertEqual(cur[:316],old)
        lookup={r['id']:r for r in cur}
        for name in('P4-014','P7-132'):self.assertEqual(lookup[name]['certainty'],'potential')
        self.assertEqual(self.table('historical-extensions-07B23.csv'),[])
        for name,digest in((b23.SNAPSHOT,b23.SNAPSHOT_SHA),(b23.SHARED_SNAPSHOT,b23.SHARED_SHA),('evidence/provenance-07B23.json',b23.PROVENANCE_SHA)):
            self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
    def test_43_scope12_10overlap2new_union418_not_census_11literal7paths(self):
        d=json.loads((A/'evidence/scope-decision-07B23.json').read_text());b=d['bookkeeping']
        self.assertEqual(tuple(b[k]for k in('selected_paths','prior_union','overlap','new','union','complement')),(12,416,10,2,418,409))
        self.assertEqual(b['complement_kinds'],{'source':344,'generated-artifact':61,'project-or-resource':4})
        self.assertEqual(d['selected_upstream_split'],'SP7B22-01');self.assertFalse(d['historical_body_review_claim'])
        for k in('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):self.assertIs(d[k],False)
        w=self.witness();dis=w['constructor_discovery'];tokens=dis['exact_new_MsgExistItem_tokens']
        self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),dis['source_csharp_paths_lexically_scanned']),(29,477))
        self.assertEqual((len(tokens),len({r['path']for r in tokens})),(11,7));self.assertTrue(dis['not_complete_callgraph_or_runtime_reachability'])
        self.assertEqual(len(dis['strict_utf8_fallback_cp1256_paths_not_compiler_acceptance']),4)
    def test_44_new_certainty_145_potential_two_confirmed_homologue_not_recounted(self):
        cur=list(csv.DictReader(io.StringIO((A/'findings.csv').read_text(),newline='')))
        self.assertEqual([r['certainty']for r in cur[316:]],['potential','confirmed','confirmed'])
        ad=self.table('root-adjudication-07B23.csv');self.assertEqual([r['current_root_ids']for r in ad if r['decision']=='new-local-root'],b23.NEW_IDS)
        self.assertEqual(ad[3]['decision'],'same-cause-homologues-not-extended-or-recounted');self.assertEqual(ad[3]['current_root_ids'],'P7-143')
        self.assertTrue(all(r['comparison_depth']==b23.DEDUP_DEPTH for r in ad))
        self.assertEqual(b23.residual_errors(self.table('residual-disposition-07B23.csv'),self.table('residual-disposition-07B22.csv')),[])
        self.assertEqual(b23.split_errors(self.table('split-register-07B23.csv'),self.table('split-register-07B22.csv')),[])

if __name__=='__main__':unittest.main()
