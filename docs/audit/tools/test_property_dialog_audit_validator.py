#!/usr/bin/env python3
"""44 documentary self-tests, NOT WPF/property/packing/business acceptance.

ALL694 protected prior cases remain unchanged, including ALL44 B24 in its
OWN322/raw323CRLF/indexes/presetB24 child. Synthetic history fixtures test
schema only; the actual30 archive has a separate identity test. Exact inert
models are not .NET parsers/formatters, WPF schedules, SDK DTOs or ERP tests.
"""
from __future__ import annotations
import ast,copy,csv,hashlib,io,json
from fractions import Fraction
from pathlib import Path
import subprocess,sys
from types import SimpleNamespace
import unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_property_dialog_part as b25
from validate_row_ownership_part import historical_b23_inputs
from check_property_dialog_witnesses import append_on_normal_loader_return,calc,checked_state,exact_text,item,modal,number,project,state
A=Path(__file__).resolve().parents[1]

class PropertyDialogAuditTests(unittest.TestCase):
    def old(self,n=322):return[dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]
    def raw(self,data):
        stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=list(data[0]),lineterminator='\r\n');writer.writeheader();writer.writerows(data);return stream.getvalue().encode()
    def current(self):return self.old()+[self.old(1)[0]|dict(id=n,next_phase='8')for n in b25.NEW_IDS]
    def texts(self):return{n:'FROZEN:'+n for n in b25.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b25.historical_b24_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def table(self,name):return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))
    def groups(self,end):return'\n'.join(f'| G-{n:02d} | exact |'for n in range(1,end+1))+'\n'
    def contracts(self):
        fe=[];iv=[];tests=[]
        for n in range(1,17):
            fid=f'FE-{n:02d}';iid=f'INV-{n:02d}';root=b25.NEW_IDS[n-1]if n<=2 else'H'
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}'for i in(2*n-1,2*n)))
            fe.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            iv.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,plan_kind='finding-specific'if n<=2 else'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fe,iv,tests
    def residuals(self):
        old=[dict(id=f'RS7B24-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='upstream redacted',disposition='external-handoff',current_handoff_or_split_ids='H7B24-03;H7B24-04')for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B24.csv',upstream_row_sha256=b25.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',owner_role='owner',required_redacted_input='upstream redacted; new contract',impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B25-03;H7B25-04',disposition='external-handoff',runtime_status='not-executed')for r in old]
        return new,old
    def splits(self):
        old=[dict(id=f'SP7B24-{n:02d}',required_input='upstream redacted')for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B24.csv',upstream_row_sha256=b25.row_sha(r),title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='upstream redacted; new contract',next_static_action='source trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed')for r in old]
        return new,old
    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4i-property-dialog-delivered-residuals-open']+['planned-not-started']*6
        return[dict(part_family='7B'if n<4 else'7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false')for n,s in enumerate(states)]
    def witness(self):return json.loads((A/'evidence/property-dialog-witnesses-07B25.json').read_text())
    def history_fixture(self):
        """Synthetic30 SCHEMA fixture, NEVER proof that30 modes actually ran."""
        old=json.loads((A/'evidence/historical-mode-verification-07B24.json').read_text());m=copy.deepcopy(old['historical_modes'])
        m.append(dict(mode='B24',findings_total=322,registry_used=b25.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=694,audit_checker_self_test_suite_count=25,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B24_child=dict(tests_reported=44,expected_tests=44,process_exit_code=0,result='passed',historical_parser_cutoff='B24-not-current-B25-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_row_ownership_tests_07B25.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=30,historical_modes=m,errors=[])

    def test_01_OWN322_exact_raw323CRLF_three_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old())
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
    def test_02_reject_bad_OWN_rows_bytes_BOM_LF_texts(self):
        f=self.fake();old=self.old();raw=self.raw(old)
        for data,texts,b in((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),(old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw),(old,self.texts(),bytearray(raw))):
            with self.assertRaises(ValueError):
                with b25.historical_b24_inputs(f,data,texts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b25.historical_b24_inputs(f,old,self.texts(),self.raw(old)):pass
    def test_03_context_local_Path_not_process_global_or_disk_overlay(self):
        f=self.fake();before=Path.read_bytes,Path.read_text
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text),before)
            self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual(type(f.AUDIT)(__file__).read_text(),Path(__file__).read_text())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_text()
    def test_04_nested_OWN319_and_exception_restoration(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b23_inputs(f,self.old(319),self.texts(),self.raw(self.old(319))):self.assertEqual(len(f.rows('findings.csv')),319)
            self.assertEqual(len(f.rows('findings.csv')),322);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_05_frozen_rows_texts_copy_isolation(self):
        f=self.fake();old=self.old();texts=self.texts();saved=copy.deepcopy(old)
        with b25.historical_b24_inputs(f,old,texts,self.raw(old)):
            data=f.rows('findings.csv');data[0]['next_phase']='bad';self.assertEqual(f.rows('findings.csv'),saved)
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertEqual(old,saved);self.assertEqual(texts,self.texts())
    def test_06_all322_fields_ALLnextphase_evidence_and_rawprefix(self):
        old=self.old();cur=self.current();self.assertEqual(b25.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed';self.assertTrue(b25.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)
    def test_07_only151_152_append_raw325CRLF_noBOM(self):
        old=self.old();cur=self.current()
        for bad in(cur[:-1],cur+[dict(cur[-1])],cur[:322]+list(reversed(cur[322:]))):self.assertTrue(b25.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in(self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):self.assertTrue(b25.registry_preservation_errors(old,cur,raw,self.raw(old)))
    def test_08_exact_G215_append216through219_only(self):
        self.assertEqual(b25.group_row_errors(self.groups(215),self.groups(219)),[])
        for bad in(self.groups(218),self.groups(220),self.groups(219).replace('G-99','G-98'),self.groups(219).replace('| G-01 | exact','| G-01 | changed')):self.assertTrue(b25.group_row_errors(self.groups(215),bad))
    def test_09_explicit_source_sentinels_and_range_expansion(self):
        errors=[];calls=[];fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,evidence=lambda*a:calls.append(a),scoped_evidence=lambda*a,**k:calls.append((a,k)))
        for gate in('FE7B25-15','AD7B25-07','AD7B25-08'):b25.validate_source(fake,dict(id=gate,evidence=b25.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]))
        b25.validate_source(fake,dict(id='UNKNOWN',evidence=b25.DOCUMENTARY),{});b25.validate_source(fake,dict(id='FE7B25-15',evidence='a.cs:1-2'),{})
        self.assertEqual((len(errors),len(calls)),(2,2));self.assertEqual(b25.expanded_source_evidence('a.cs:1-2;5;b.cs:7;9-10'),'a.cs:1-2;a.cs:5;b.cs:7;b.cs:9-10')
        for bad in('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b25.expanded_source_evidence(bad)
        # A repeated path-bearing fragment must not detach its next bare range.
        features=[dict(evidence='a.cs:1-2;3;b.cs:7'),dict(evidence='a.cs:1-2;5;b.cs:7;9-10'),dict(evidence=b25.DOCUMENTARY)]
        self.assertEqual(b25.source_evidence_union(features),'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5;b.cs:9-10')
        self.assertEqual(b25.source_evidence_union([dict(evidence=b25.DOCUMENTARY)]),b25.DOCUMENTARY)
        self.assertEqual(b25.source_evidence_union([]),b25.DOCUMENTARY)
        rc=self.table('report-reconciliation-07B25.csv');fe=self.table('feature-implementation-matrix-07B25.csv')
        for row in rc:
            related=[f for f in fe if f['id']in row['feature_ids'].split(';')]
            self.assertEqual(row['evidence'],b25.source_evidence_union(related))
        self.assertIn('SmartAuditERP/Form_WPF/frmItemProperties.xaml.cs:33-66',rc[0]['evidence'])
        self.assertNotIn('SmartAuditERP/Class/ItemOper.cs:33-66',rc[0]['evidence'])
    def test_10_ordered_DG8_PK8_result_guard_and_reachability_limits(self):
        dg=self.table('dialog-result-lineage-07B25.csv');pk=self.table('packing-calculation-lineage-07B25.csv');self.assertEqual(b25.ledger_errors(dg,pk),[])
        for pool,other in((dg,pk),(pk,dg)):
            bad=copy.deepcopy(pool);bad[0],bad[1]=bad[1],bad[0];self.assertTrue(b25.ledger_errors(bad,other)if pool is dg else b25.ledger_errors(other,bad))
        for pool,index in((dg,2),(dg,5),(dg,6),(dg,7),(pk,0),(pk,1),(pk,2),(pk,5),(pk,7)):
            bad=copy.deepcopy(pool);bad[index]['observation']='all-accepted';self.assertTrue(b25.ledger_errors(bad,pk)if pool is dg else b25.ledger_errors(dg,bad))
    def test_11_ledger_responsibilities_not_empty_or_executed(self):
        dg=self.table('dialog-result-lineage-07B25.csv');pk=self.table('packing-calculation-lineage-07B25.csv')
        for key in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(pk);bad[0][key]='';self.assertTrue(b25.ledger_errors(dg,bad),key)
        bad=copy.deepcopy(dg);bad[0]['runtime_status']='passed';self.assertTrue(b25.ledger_errors(bad,pk));self.assertTrue(b25.ledger_errors(dg[:-1],pk))
    def test_12_FE16_INV16_T32_reverse_links_and_two_roots(self):
        self.assertEqual(b25.current_link_errors(*self.contracts()),[])
        for pool,key in((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            parts=self.contracts();parts[pool][0][key]='changed';self.assertTrue(b25.current_link_errors(*parts),key)
        fs,iv,ts=self.contracts();self.assertTrue(b25.current_link_errors(fs,iv,ts[:-1]))
    def test_13_distinct_invariants_criteria_and_responsibilities(self):
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            fs,iv,ts=self.contracts();fs[0][key]='';self.assertTrue(b25.current_link_errors(fs,iv,ts),key)
        fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b25.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b25.current_link_errors(fs,iv,ts))
    def test_14_all14_residual_ancestry_hash_contracts(self):
        current,old=self.residuals();self.assertEqual(b25.residual_errors(current,old),[])
        for key in('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            current,old=self.residuals();current[0][key]='changed';self.assertTrue(b25.residual_errors(current,old),key)
        self.assertTrue(b25.residual_errors(current[:-1],old))
    def test_15_full_old_inputs_all_routes_and_no_approval(self):
        for key in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            current,old=self.residuals();current[0][key]='';self.assertTrue(b25.residual_errors(current,old),key)
        for key,value in(('required_redacted_input','lost'),('disposition','approved'),('runtime_status','passed'),('current_handoff_or_split_ids','H7B25-03')):
            current,old=self.residuals();current[0][key]=value;self.assertTrue(b25.residual_errors(current,old),key)
    def test_16_three_split_ancestries_full_inputs_and_reasons(self):
        current,old=self.splits();self.assertEqual(b25.split_errors(current,old),[])
        for key in current[0]:
            current,old=self.splits();current[0][key]='';self.assertTrue(b25.split_errors(current,old),key)
        current,old=self.splits();current[0]['required_input']='replacement';self.assertTrue(b25.split_errors(current,old))
    def test_17_boundedR4i_fourB_sixC_unstarted_no_sessions_or_percent(self):
        self.assertEqual(b25.remaining_work_errors(self.work()),[])
        for index,key,value in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true'),(0,'part_family','7C')):
            work=self.work();work[index][key]=value;self.assertTrue(b25.remaining_work_errors(work),key)
        self.assertTrue(b25.remaining_work_errors(self.work()[:-1]))
    def test_18_witness_strict_bool_integer_limits_and_B10_addendum(self):
        self.assertEqual(b25.witness_metadata_errors(self.witness()),[])
        for key,value in(('application_code_imported_or_executed',0),('erp_runtime_tests_executed',False),('illustration_count',16.0),('B_R4i_bounded_not_whole7B_closure',1),('actual_WPF_event_order_or_count_claimed',True),('Invoicecontract_and_InvoiceDGV_overloads_kept_distinct',1),('phase7C_started',True),('phase8_authorized_or_started',True)):
            self.assertTrue(b25.witness_metadata_errors(self.witness()|{key:value}),key)
        bad=self.witness();bad['retained_additive_B10_arithmetic_erratum']['reference_cost']=10;self.assertTrue(b25.witness_metadata_errors(bad))
    def test_19_actual_witness_stdout_hash_readonly_recompute(self):
        self.assertEqual(hashlib.sha256((A/'evidence/property-dialog-witnesses-07B25.json').read_bytes()).hexdigest(),b25.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_property_dialog_witnesses.py')],capture_output=True,text=True,timeout=25)
        self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,'');self.assertEqual(json.loads(run.stdout),self.witness())
    def test_20_synthetic30_schema_OWN322_ALL44_not_actual_execution(self):
        self.assertEqual(b25.historical_record_errors(self.history_fixture()),[])
        for index,key,value in((29,'findings_total',324),(29,'registry_used','findings.csv'),(29,'stdout_sha256','bad'),(29,'audit_checker_self_test_cases_reported',738),(0,'audit_checker_self_test_cases_reported',0),(29,'erp_runtime_tests_executed',False)):
            h=self.history_fixture();h['historical_modes'][index][key]=value;self.assertTrue(b25.historical_record_errors(h),key)
        h=self.history_fixture();h['historical_modes'][-1]['historical_B24_child']['suite_own_registry_path_is_context_local_not_global']=False;self.assertTrue(b25.historical_record_errors(h))
        h=self.history_fixture();h['historical_modes']=h['historical_modes'][:-1];self.assertTrue(b25.historical_record_errors(h))
    def test_21_actual30_archive_identity_separate_from_synthetic_fixture(self):
        raw=(A/'evidence/historical-mode-verification-07B25.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b25.HISTORICAL_RUN_SHA)
        h=json.loads(raw);self.assertEqual(b25.historical_record_errors(h),[]);self.assertEqual(h['checkout_head'],b25.ENTRY)
        self.assertEqual(h['current_actual_CLI_default'],'B25');self.assertEqual(h['historical_mode_count'],30)
    def test_22_nontrue_area_projects_fresh_zero_not_original_quantity(self):
        original=item(3);p=project(original,modal(state(3,net='60'),False))
        self.assertEqual((p['item']['qty'],p['item']['detail_qty']),('0','0'));self.assertNotEqual(p['item']['description'],original['description'])
        self.assertTrue(p['caller_ignores_supplied_dialog_outcome']);self.assertFalse(p['application_executed'])
    def test_23_null_return_and_positive_text_are_not_confirmation(self):
        st=state(net='60');m=modal(st,None);self.assertEqual((m['field_net'],m['state']['net_text']),('0','60'))
        self.assertEqual(project(item(2),m)['item']['qty'],'0');self.assertFalse(m['insert_handler_supplied_as_executed'])
    def test_24_insert_positive_controls_packing_fill_vs_geometry(self):
        p=project(item(2),modal(state(),True))['item'];self.assertEqual((p['qty'],p['fill_value']),('20','2'))
        p=project(item(3),modal(state(3,'4','5','2','40'),True))['item'];self.assertEqual((p['qty'],p['detail_qty'],p['height'],p['width'],p['fill_value']),('40','40','4','5','0'))
    def test_25_no_detail_guard_and_other_branch_are_not_serial_noop_claim(self):
        p=project(item(3),None,False);self.assertEqual(p['item'],item(3));self.assertFalse(p['projection_performed']);self.assertFalse(p['unmodelled_other_branch'])
        p=project(item(5),None);self.assertFalse(p['projection_performed']);self.assertTrue(p['unmodelled_other_branch']);self.assertFalse(p['application_executed'])
    def test_26_modal_strict_outcomes_state_and_copy_isolation(self):
        st=state();saved=copy.deepcopy(st);m=modal(st,False);m['state']['height']='999';self.assertEqual(st,saved)
        for bad in(0,1,'true',[],{}):
            with self.assertRaises(ValueError):modal(st,bad)
        with self.assertRaises(ValueError):checked_state(st|{'extra':'x'})
    def test_27_projection_strict_schema_metadata_types_field_and_copy(self):
        original=item(2);m=modal(state(),False);saved=copy.deepcopy((original,m));p=project(original,m);p['item']['description']='changed';self.assertEqual((original,m),saved)
        for bad in(original|{'extra':'x'},original|{'ref':''},original|{'qty':'NaN'},original|{'property':True}):
            with self.assertRaises(ValueError):project(bad,m)
        for bad in(m|{'field_net':'60'},m|{'application_executed':True},m|{'accepted':0},m|{'insert_handler_supplied_as_executed':1}):
            with self.assertRaises(ValueError):project(original,bad)
        with self.assertRaises(ValueError):project(original,m,1)
    def test_28_append_after_normal_loader_return_not_final_save_claim(self):
        prefix=['line-X'];p=project(item(3),modal(state(3,net='60'),False));result=append_on_normal_loader_return(prefix,p)
        self.assertEqual((result['refs'],result['appended_qty']),(['line-X','line-A'],'0'));self.assertEqual(prefix,['line-X']);self.assertTrue(result['successful_lookup_and_normal_loader_return_supplied'])
        for bad in(['line-A'],['X','X'],[1],None):
            with self.assertRaises(ValueError):append_on_normal_loader_return(bad,p)
    def test_29_sequential_packing_integer20_to60_to180(self):
        st=state();saved=copy.deepcopy(st);a=calc(st);b=calc(a['state'])
        self.assertEqual((a['state']['net_text'],b['state']['net_text']),('60','180'));self.assertEqual((a['state']['height'],b['state']['height']),('2','6'))
        self.assertEqual(st,saved);self.assertEqual(a['state']['qty'],b['state']['qty']);self.assertFalse(b['application_executed'])
    def test_30_quantity_one_idempotence_is_a_control_not_approval(self):
        a=calc(state(qty='1'));b=calc(a['state']);self.assertEqual(a['state'],b['state']);self.assertEqual(a['state']['net_text'],'20')
    def test_31_zero_width_and_quantity_guards(self):
        for st in(state(width='0'),state(qty='0')):
            result=calc(st);self.assertEqual((result['state']['height'],result['state']['net_text']),('0','0'))
    def test_32_area_and_linear_formula_sequential_controls(self):
        for prop,expected in((3,'60'),(4,'72')):
            a=calc(state(prop));b=calc(a['state']);self.assertEqual(a['state'],b['state']);self.assertEqual(a['state']['net_text'],expected)
    def test_33_internal_guard_suppresses_nested_not_next_call(self):
        st=state();guarded=calc(st,True);self.assertEqual(guarded['state'],st);self.assertTrue(guarded['suppressed_nested_call'])
        self.assertEqual(calc(guarded['state'])['state']['net_text'],'60')
        with self.assertRaises(ValueError):calc(st,1)
    def test_34_fractional_previous_height_selects_same_source_ceiling_branch(self):
        st=state(height='2.5',net='21',qty='2');result=calc(st)['state'];self.assertEqual((result['height'],result['net_text']),('3','60'))
        for bad in(st|{'property':True},st|{'property':5},st|{'height':'-1'},st|{'qty':3},st|{'net_text':'Infinity'}):
            with self.assertRaises(ValueError):calc(bad)
    def test_35_exact_fixture_domain_is_not_dotnet_culture_or_rounding(self):
        for bad in(True,1,None,'NaN','Infinity','-1',' 1 ','1,5','1e3','01','', '1/2'):
            with self.assertRaises(ValueError):number(bad)
        self.assertEqual(number('1.25'),Fraction(5,4));self.assertEqual(exact_text(Fraction(1,8)),'0.125')
        for bad in(Fraction(1,3),Fraction(1,16),Fraction(-1)):
            with self.assertRaises(ValueError):exact_text(bad)
    def test_36_actual_ledgers_roots_and_zero_extensions(self):
        dg=self.table('dialog-result-lineage-07B25.csv');pk=self.table('packing-calculation-lineage-07B25.csv')
        self.assertEqual(dg[2]['finding_ids'],'P7-151');self.assertEqual(pk[0]['finding_ids'],'P7-152')
        self.assertEqual(dg[5]['finding_ids'],'H7B25-03');self.assertEqual(dg[6]['finding_ids'],'H7B25-03');self.assertEqual(self.table('historical-extensions-07B25.csv'),[])
    def test_37_ACTUAL_B25_parser_versioned_B24_and_API_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in(('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'),('PHASE7_B18_CLI','B18'),('PHASE7_B19_CLI','B19'),('PHASE7_B20_CLI','B20'),('PHASE7_B21_CLI','B21'),('PHASE7_B22_CLI','B22'),('PHASE7_B23_CLI','B23'),('PHASE7_B24_CLI','B24')):self.assertEqual(getattr(v,name)['default'],part)
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B25')
        for part in('A',)+tuple('B'+str(n)for n in range(1,26)):self.assertEqual(parser.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)
    def test_38_real_entrypoint_historical24_before_current_properties(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'))
        self.assertLess(body.index('historical_b23_validation('),body.index('historical_b24_validation('));self.assertLess(body.index('historical_b24_validation('),body.index('extend_property_dialogs('))
        self.assertIn('extend_row_ownership(historical_b24,',body);self.assertIn("phase7_part == 'B24'",body)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser')))
    def test_39_exact_argv_proxy_preserves_unrelated_calls_and_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda*a,**k:calls.append((a,k))or'sentinel');proxy=b25.HistoricalB24Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in(proxy.expected+['--different'],['python','-B','/else/test_row_ownership_audit_validator.py']):proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs);self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))
    def test_40_view_restores_context_without_shared_subprocess_Path_mutation(self):
        backend=SimpleNamespace(run=lambda*a,**k:'sentinel');f=self.fake();f.subprocess=backend;f.sys=SimpleNamespace(executable='python');view=b25.HistoricalB24ValidatorView(f)
        original=subprocess.run,Path.read_bytes,Path.read_text;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertEqual((subprocess.run,Path.read_bytes,Path.read_text),original);self.assertEqual(len(view.rows('findings.csv')),322);raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_41_historical_child_ALL44_local_A_restore_and_protected_tools(self):
        tools=A/'tools';source=ast.unparse(ast.parse((tools/'run_historical_row_ownership_tests_07B25.py').read_text()))
        for token in('loadTestsFromModule(historical_tests)','suite.countTestCases() != 44','result.testsRun != 44 or result.skipped','historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B24_CLI','b25.historical_b24_inputs('):self.assertIn(token,source)
        self.assertNotIn('unittest.skip',source);prov=json.loads((A/'evidence/provenance-07B25.json').read_text())
        for name in('test_row_ownership_audit_validator.py','validate_row_ownership_part.py','check_row_ownership_witnesses.py','run_historical_item_ingress_tests_07B24.py','test_item_ingress_audit_validator.py','test_contract_item_audit_validator.py','test_amountword_contract_audit_validator.py','test_barcode_contract_audit_validator.py','test_navigation_contract_audit_validator.py'):
            self.assertEqual(hashlib.sha256((tools/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])
    def test_42_actual322_raw323_fields_potential_barriers_and_frozen_hashes(self):
        raw=(A/b25.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')))
        self.assertEqual(b25.registry_preservation_errors(old,cur,now,raw),[]);self.assertEqual(cur[:322],old)
        lookup={r['id']:r for r in cur}
        for name in('P4-014','P7-132','P7-145'):self.assertEqual(lookup[name]['certainty'],'potential')
        self.assertEqual(self.table('historical-extensions-07B25.csv'),[])
        for name,digest in((b25.SNAPSHOT,b25.SNAPSHOT_SHA),(b25.SHARED_SNAPSHOT,b25.SHARED_SHA),('evidence/provenance-07B25.json',b25.PROVENANCE_SHA)):
            self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)
    def test_43_scope10_8overlap2new_union421_23reads2wholefiles_not_census(self):
        decision=json.loads((A/'evidence/scope-decision-07B25.json').read_text());book=decision['bookkeeping']
        self.assertEqual(tuple(book[k]for k in('selected_paths','prior_union','overlap','new','union','complement')),(10,419,8,2,421,406));self.assertEqual(book['complement_kinds'],{'source':341,'generated-artifact':61,'project-or-resource':4})
        self.assertEqual(decision['selected_upstream_split'],'SP7B24-01');self.assertFalse(decision['historical_body_review_claim'])
        for key in('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):self.assertIs(decision[key],False)
        w=self.witness();self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),w['whole_local_dialog_files_selected']),(23,2));self.assertFalse(w['all_callers_or_external_DTOs_body_reviewed']);self.assertTrue(w['selected_paths_strict_utf8_decode'])
    def test_44_two_new_roots_residuals_and_additive_clock_capture_identity(self):
        cur=list(csv.DictReader(io.StringIO((A/'findings.csv').read_text(),newline='')));self.assertEqual([r['certainty']for r in cur[322:]],['confirmed']*2)
        ad=self.table('root-adjudication-07B25.csv');self.assertEqual([r['current_root_ids']for r in ad if r['decision']=='new-local-root'],b25.NEW_IDS)
        self.assertEqual([r['current_root_ids']for r in ad if r['decision']=='same-current-root-second-helper-not-separate-finding'],['P7-151']);self.assertTrue(all(r['comparison_depth']==b25.DEDUP_DEPTH for r in ad))
        self.assertEqual(b25.residual_errors(self.table('residual-disposition-07B25.csv'),self.table('residual-disposition-07B24.csv')),[]);self.assertEqual(b25.split_errors(self.table('split-register-07B25.csv'),self.table('split-register-07B24.csv')),[])
        prov=json.loads((A/'evidence/provenance-07B25.json').read_text());note=(A/'DATE-IDENTITY-NOTE-07B25.md').read_text();self.assertEqual(b25.date_identity_errors(prov,note),[])
        self.assertTrue(b25.date_identity_errors(prov|{'audit_reference_date_utc':'2026-11-19'},note));self.assertTrue(b25.date_identity_errors(prov,note.replace(b25.B24_CHECK_SHA,'changed')))
        self.assertEqual(hashlib.sha256((A/'evidence/checks-07B24.json').read_bytes()).hexdigest(),b25.B24_CHECK_SHA)

if __name__=='__main__':unittest.main()
