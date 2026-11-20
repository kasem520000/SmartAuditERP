#!/usr/bin/env python3
"""52 B32 documentary checker cases,NOT32 acceptance plans or ERP tests.

ALL1034 earlier cases,including48 B31/52 B30,remain unchanged. Historical
B31 assertion inputs115 are distinct from actual current119/parser here.
Synthetic37 schema fixtures are NOT actual subprocess execution evidence.
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
import validate_editor_close_part as b32
from check_editor_close_witnesses import SOURCE_SLICES,EXPLORATORY_SLICES,guard,close_trace,key_trace,header_edit,new_intent
A=Path(__file__).resolve().parents[1]


class EditorCloseAuditTests(unittest.TestCase):
    def old(self):return [dict(id=f'PX-{i:03d}',severity='Medium',certainty='potential',type='synthetic-only',status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for i in range(333)]
    def current(self):return self.old()+[self.old()[0]|dict(id='P7-162',next_phase='8')]
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def texts(self):return {n:'FROZEN:'+n for n in b32.SHARED_DOCS}
    def sources(self):
        raw=b'# fixture historical dispatcher TEXT,not executed\n';return {'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{i:03d}.py':'a'*64 for i in range(114)},raw
    def context(self,f):return b32.historical_b31_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())
    def table(self,stem,part=32):
        with (A/'evidence'/f'{stem}-07B{part}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
    def groups(self,n):return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1,n+1))+'\n'
    def witness(self):return json.loads((A/'evidence/editor-close-witnesses-07B32.json').read_bytes())
    def features(self):return self.table('feature-implementation-matrix')
    def history_fixture(self):
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B31.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',historical_parser_cutoff='B31-not-current-B32-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_navigation_load_tests_07B32.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=115,auxiliary_dispatcher_text_sha256=b32.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B31',findings_total=333,registry_used=b32.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1034,audit_checker_self_test_suite_count=32,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B31_child=child))
        return dict(historical_mode_count=37,historical_modes=modes,errors=[])

    def test_01_OWN333_raw334_three_index_strings(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()));self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old())
    def test_02_reject_bad_rows_raw_BOM_LF_vector_and_TEXT(self):
        old,raw,src=self.old(),self.raw(self.old()),self.sources()
        for args in ((old[:-1],self.texts(),raw,*src),(old,self.texts(),raw.replace(b'\r\n',b'\n'),*src),(old,self.texts(),b'\xef\xbb\xbf'+raw,*src),(old,{'README.md':'only'},raw,*src),(old,self.texts(),bytearray(raw),*src),(old,self.texts(),raw,{},src[1]),(old,self.texts(),raw,src[0],src[1]+b'x')):
            with self.assertRaises(ValueError):
                with b32.historical_b31_inputs(self.fake(),*args):pass
        old[0]['id']=old[1]['id']
        with self.assertRaises(ValueError):
            with b32.historical_b31_inputs(self.fake(),old,self.texts(),self.raw(old),*src):pass
    def test_03_nested_context_copies_and_exception_restore(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            current=f.AUDIT;r=f.rows('findings.csv');r[0]['title']='changed';self.assertEqual(f.rows('findings.csv'),self.old())
            with self.context(f):self.assertEqual(len(f.rows('findings.csv')),333)
            self.assertIs(f.AUDIT,current)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_04_canonical_local_Path_TEXT_not_global(self):
        f=self.fake();original=Path.read_bytes,Path.read_text,Path.glob;src,raw=self.sources()
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text,Path.glob),original);self.assertEqual(len(list((f.AUDIT/'tools').glob('*.py'))),115)
            self.assertEqual((f.AUDIT/'tools/validate_audit.py').read_bytes(),raw);self.assertEqual((f.AUDIT/'tools/validate_audit.py').resolve(),Path('/synthetic/audit/tools/validate_audit.py'))
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes());self.assertEqual(f.rows('other/findings.csv'),[dict(id='LIVE:other/findings.csv')])
    def test_05_exact_argv_proxy_not_shared_subprocess(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'ok');proxy=b32.HistoricalB31Subprocess(backend,'python',Path('/a/tools'));kw=dict(cwd='/a',timeout=60,capture_output=True,text=True)
        self.assertEqual(proxy.run(list(proxy.expected),**kw),'ok');self.assertEqual(calls[-1],((proxy.actual,),kw))
        for args in (tuple(proxy.expected),proxy.expected+['--other'],['python','-B','/other/test_navigation_load_audit_validator.py']):proxy.run(args,**kw);self.assertEqual(calls[-1],((args,),kw))
        f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b32.HistoricalB31ValidatorView(f);original=subprocess.run
        with self.context(view):self.assertIs(subprocess.run,original);self.assertIs(f.subprocess,backend)
    def test_06_ALL333_dictionaries_every_field_preserved(self):
        old,cur=self.old(),self.current();self.assertEqual(b32.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old),[]),[])
        for n in (0,330,331,332):
            for key in old[n]:
                bad=copy.deepcopy(cur);bad[n][key]='changed';self.assertTrue(b32.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]),(n,key))
    def test_07_full_raw334_prefix_CRLF_noBOM(self):
        old,cur=self.old(),self.current();frozen=self.raw(old);self.assertTrue(self.raw(cur).startswith(frozen))
        for bad in (self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2],self.raw(cur).replace(b'fixture-title',b'other',1)):self.assertTrue(b32.registry_preservation_errors(old,cur,bad,frozen,[]))
    def test_08_one162_no_extension_or_per_event_recount(self):
        old,cur=self.old(),self.current()
        for bad in (cur[:-1],cur+[dict(cur[-1])],cur[:-1]+[cur[-1]|dict(id='P7-163')]):self.assertTrue(b32.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]))
        self.assertTrue(b32.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old),[dict(finding_id='P7-132')]))
    def test_09_G244_exact_only245_to248(self):
        self.assertEqual(b32.group_row_errors(self.groups(244),self.groups(248)),[])
        for bad in (self.groups(247),self.groups(249),self.groups(248).replace('| G-01 | exact','| G-01 | changed'),self.groups(248).replace('G-244','G-243')):self.assertTrue(b32.group_row_errors(self.groups(244),bad))
    def test_10_documentary_sentinels_not_fabricated_source(self):
        errors,calls=[],[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for name in ('FE7B32-15','EO7B32-08','AD7B32-08'):b32.validate_source(f,dict(id=name,evidence=b32.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]));b32.validate_source(f,dict(id='UNKNOWN',evidence=b32.DOCUMENTARY),{});b32.validate_source(f,dict(id='FE7B32-15',evidence='a.cs:1-2'),{});self.assertEqual(len(errors),2)
        self.assertEqual(b32.source_evidence_union([dict(evidence='a.cs:1-2;3'),dict(evidence='a.cs:1-2;5')]),'a.cs:1-2;a.cs:3;a.cs:5')
    def test_11_ordered_EO8_DG8_and_exact_feature_unions(self):
        data=self.table('event-ownership-lineage'),self.table('dirty-guard-lineage');fe=self.features();self.assertEqual(b32.ledger_errors(*data,fe),[])
        for pool in (0,1):
            bad=copy.deepcopy(data);bad[pool][0],bad[pool][1]=bad[pool][1],bad[pool][0];self.assertTrue(b32.ledger_errors(*bad,fe))
            for key in ('feature_ids','finding_ids','evidence','source_to_output','boundary'):
                bad=copy.deepcopy(data);bad[pool][0][key]='changed';self.assertTrue(b32.ledger_errors(*bad,fe),key)
    def test_12_lineage_responsibility_and_nonexecution(self):
        data=self.table('event-ownership-lineage'),self.table('dirty-guard-lineage');fe=self.features()
        for key in ('source_to_output','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence','observation'):
            bad=copy.deepcopy(data);bad[1][0][key]='';self.assertTrue(b32.ledger_errors(*bad,fe),key)
        bad=copy.deepcopy(data);bad[0][0]['runtime_status']='passed';self.assertTrue(b32.ledger_errors(*bad,fe))
    def test_13_FE16_INV16_T32_bidirectional(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b32.current_link_errors(*data),[])
        for pool,key in ((0,'acceptance_ids'),(1,'feature_ids'),(1,'finding_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            bad=copy.deepcopy(data);bad[pool][0][key]='changed';self.assertTrue(b32.current_link_errors(*bad))
    def test_14_entry_source_output_exclusion_and_distinct_plans(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')]
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim'):
            bad=copy.deepcopy(data);bad[0][0][key]='';self.assertTrue(b32.current_link_errors(*bad),key)
        for pool,key in ((1,'required_invariant'),(2,'acceptance_criterion')):
            bad=copy.deepcopy(data);bad[pool][1][key]=bad[pool][0][key];self.assertTrue(b32.current_link_errors(*bad))
    def test_15_RS14_upstream_row_SHA_contracts(self):
        old,new=self.table('residual-disposition',31),self.table('residual-disposition');self.assertEqual(b32.residual_errors(new,old),[])
        for key in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(new);bad[0][key]='changed';self.assertTrue(b32.residual_errors(bad,old))
    def test_16_all_old_RS_inputs_routes_dispositions_preserved(self):
        old,new=self.table('residual-disposition',31),self.table('residual-disposition')
        for key,val in (('required_redacted_input','only new'),('current_handoff_or_split_ids','H7B32-01'),('disposition','approved'),('runtime_status','passed'),('local_result','')):
            bad=copy.deepcopy(new);bad[2][key]=val;self.assertTrue(b32.residual_errors(bad,old))
        self.assertTrue(b32.residual_errors(new[:-1],old))
    def test_17_SP3_full_input_prefix_and_future_status(self):
        old,new=self.table('split-register',31),self.table('split-register');self.assertEqual(b32.split_errors(new,old),[])
        for key in ('upstream_split_id','upstream_artifact','upstream_row_sha256','required_input','reason_for_split','status','runtime_status'):
            bad=copy.deepcopy(new);bad[0][key]='changed' if key!='reason_for_split' else '';self.assertTrue(b32.split_errors(bad,old))
    def test_18_RW10_fourB_sixC_BK_ancestry(self):
        work=self.table('remaining-workplan');self.assertEqual(b32.remaining_work_errors(work),[])
        for n,key,val in ((3,'status','complete'),(4,'status','started'),(0,'part_family','7C'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            bad=copy.deepcopy(work);bad[n][key]=val;self.assertTrue(b32.remaining_work_errors(bad))
        for n,r in enumerate(self.table('continuation-backlog'),1):self.assertEqual((r['prior_backlog_id'],r['original_backlog_id']),(f'BK7B31-{n:02d}',f'BK7-{n:02d}'));self.assertNotEqual(r['status'],'complete')
    def test_19_witness_metadata_strict_bools_counts_B10(self):
        w=self.witness();self.assertEqual(b32.witness_metadata_errors(w),[])
        for key in ('application_code_imported_or_executed','persisted_duplicate_save_or_financial_loss_claimed','IsUpdated_propagation_or_SDK_defaults_proved','stable_post_event_state_claimed'):
            for val in (True,0):self.assertTrue(b32.witness_metadata_errors(w|{key:val}))
        for key in ('illustration_count','selected_contract_slices','context_slices_not_certified','erp_runtime_tests_executed'):self.assertTrue(b32.witness_metadata_errors(w|{key:True}))
        bad=copy.deepcopy(w);bad['retained_additive_B10_arithmetic_erratum']['local_cost']=20;self.assertTrue(b32.witness_metadata_errors(bad))
    def test_20_actual_witness_bytes_recomputed_readonly(self):
        raw=(A/'evidence/editor-close-witnesses-07B32.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b32.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_editor_close_witnesses.py')],capture_output=True,timeout=20);self.assertEqual((run.returncode,run.stderr,run.stdout),(0,b'',raw))
        self.assertTrue(all(x['illustration_assertions_passed'] is True and x['source_application_executed'] is False for x in self.witness()['illustrations']))
    def test_21_sale_guard_threshold_is_supplied_not_Grid_execution(self):
        for rows,expected in ((0,False),(1,False),(2,True)):
            self.assertIs(guard('sale',True,False,rows),expected);self.assertFalse(guard('sale',False,False,rows));self.assertTrue(guard('sale',False,True,rows))
    def test_22_purchase_guard_threshold_not_same_as_sale(self):
        for rows,expected in ((0,False),(1,True),(2,True)):
            self.assertIs(guard('purchase',True,False,rows),expected);self.assertFalse(guard('purchase',False,False,rows));self.assertTrue(guard('purchase',False,True,rows))
    def test_23_guard_validates_even_short_circuit_inputs(self):
        for args in (('other',False,False,0),('sale',True,1,2),('sale',1,False,0),('purchase',False,False,True),('sale',False,False,-1),('sale',False,False,1001),('sale',False,False,'2')):
            with self.assertRaises(ValueError):guard(*args)
    def test_24_sale_Yes_Yes_two_prompts_not_observed_close(self):
        t=close_trace('sale',[True,True],['Yes','Yes']);self.assertEqual(t['prompts'],2);self.assertFalse(t['cancel_at_boundary']);self.assertFalse(t['actual_window_closed_claimed']);self.assertEqual(t['invocations'],2)
    def test_25_sale_No_Yes_retains_first_veto(self):
        t=close_trace('sale',[True,True],['No','Yes']);self.assertEqual(t['prompts'],2);self.assertTrue(t['cancel_at_boundary']);self.assertTrue(t['events'][1]['cancel_before']);self.assertTrue(t['events'][1]['cancel_after'])
    def test_26_sale_Yes_No_veto_second(self):
        t=close_trace('sale',[True,True],['Yes','No']);self.assertFalse(t['events'][0]['cancel_after']);self.assertTrue(t['events'][1]['cancel_after']);self.assertTrue(t['cancel_at_boundary'])
    def test_27_sale_No_No_still_one_root(self):
        t=close_trace('sale',[True,True],['No','No']);self.assertEqual(t['prompts'],2);self.assertTrue(t['cancel_at_boundary']);self.assertEqual(self.witness()['new_root_ids'],['P7-162'])
    def test_28_clean_or_changing_guard_not_always_two_prompts(self):
        t=close_trace('sale',[False,False],[]);self.assertEqual(t['prompts'],0)
        t=close_trace('sale',[True,False],['No']);self.assertEqual(t['prompts'],1);self.assertTrue(t['cancel_at_boundary'])
    def test_29_purchase_one_authored_Closing_control(self):
        for reply,cancel in (('Yes',False),('No',True)):
            t=close_trace('purchase',[True],[reply]);self.assertEqual(t['prompts'],1);self.assertIs(t['cancel_at_boundary'],cancel);self.assertFalse(t['actual_window_closed_claimed'])
    def test_30_Cancel_not_Handled_and_other_veto_is_supplied(self):
        sale=close_trace('sale',[True,True],['Yes','Yes'],True);purchase=close_trace('purchase',[True],['Yes'],True)
        self.assertTrue(sale['cancel_at_boundary']);self.assertFalse(purchase['cancel_at_boundary']);self.assertFalse(purchase['actual_window_closed_claimed']);self.assertTrue(sale['Cancel_does_not_short_circuit_this_supplied_invocation_list'])
    def test_31_F6_two_requests_NOT_two_saves(self):
        t=key_trace('F6');self.assertEqual((t['handler_invocations'],t['validation_requests']),(2,2));self.assertFalse(t['successful_saves_inferred']);self.assertFalse(t['handled_at_boundary'])
    def test_32_F5_sets_Handled_and_masks_second(self):
        t=key_trace('F5');self.assertEqual((t['handler_invocations'],t['new_command_requests']),(1,1));self.assertTrue(t['handled_at_boundary']);self.assertFalse(t['events'][1]['invoked']);self.assertEqual(key_trace('F6')['handler_invocations'],2)
    def test_33_initial_Handled_masks_both_ordinary_key_handlers(self):
        for key in ('F5','F6'):
            t=key_trace(key,handled=True);self.assertEqual(t['handler_invocations'],0);self.assertTrue(t['handled_at_boundary']);self.assertFalse(any(x['invoked'] for x in t['events']))
    def test_34_first_callback_nonreturn_does_not_reach_second(self):
        for key in ('F5','F6'):
            t=key_trace(key,returns=[False]);self.assertEqual(t['handler_invocations'],1);self.assertTrue(t['boundary_did_not_return']);self.assertFalse(t['handled_at_boundary']);self.assertFalse(t['successful_saves_inferred'])
    def test_35_close_trace_strict_types_and_reached_replies(self):
        for args in (('sale',[1],['Yes']),('sale',(True,),['Yes']),('sale',[True],[]),('sale',[False],['Yes']),('sale',[True],['Cancel']),('sale',[True],['Yes'],1),('other',[],[]),('sale',[True]*4,['Yes']*4)):
            with self.assertRaises(ValueError):close_trace(*args)
        conditions,replies=[True,True],['No','Yes'];saved=copy.deepcopy((conditions,replies));close_trace('sale',conditions,replies);self.assertEqual((conditions,replies),saved)
    def test_36_key_trace_strict_types_and_unreached_inputs(self):
        for args in (('F1',),('F6',True),('F6',1.0),('F6',4),('F6',-1),('F6',2,1),('F6',2,False,[]),('F6',2,False,[True]),('F6',2,False,[False,True]),('F5',2,False,[True,True]),('F6',2,True,[True]),('F6',2,False,[1,True])):
            with self.assertRaises(ValueError):key_trace(*args)
        self.assertEqual(key_trace('F6',attachments=0)['handler_invocations'],0)
    def test_37_header_profiles_demonstrate_unknown_not_false(self):
        self.assertFalse(header_edit('fixture-A','fixture-B',False,'no-dirty-effect')['is_updated_after']);self.assertTrue(header_edit('fixture-A','fixture-B',False,'dirty-on-value-change')['is_updated_after']);self.assertIsNone(header_edit('fixture-A','fixture-B',False,'unresolved')['is_updated_after'])
        self.assertFalse(header_edit('fixture-A','fixture-A',False,'dirty-on-value-change')['is_updated_after']);self.assertTrue(header_edit('fixture-A','fixture-A',False,'dirty-on-assignment')['is_updated_after'])
    def test_38_header_profile_type_and_preexisting_dirty_control(self):
        for profile in ('no-dirty-effect','dirty-on-value-change','dirty-on-assignment'):self.assertTrue(header_edit('fixture-A','fixture-A',True,profile)['is_updated_after'])
        for args in ((None,'fixture-B',False,'unresolved'),('fixture-A',1,False,'unresolved'),('x'*81,'fixture-B',False,'unresolved'),('fixture-A','fixture-B',1,'unresolved'),('fixture-A','fixture-B',False,'default-SDK-invented')):
            with self.assertRaises(ValueError):header_edit(*args)
        self.assertTrue(header_edit('fixture-A','fixture-B',False,'unresolved')['profile_is_not_actual_SDK_behavior'])
    def test_39_new_No_stops_first_write_Yes_only_reaches_boundary(self):
        for surface in ('sale','purchase'):
            denied=new_intent(surface,False,True,2,'No');self.assertTrue(denied['denied']);self.assertIsNone(denied['first_write_boundary']);self.assertFalse(denied['CLR_or_SDK_executed'])
            allowed=new_intent(surface,False,True,2,'Yes');self.assertFalse(allowed['denied']);self.assertIsNotNone(allowed['first_write_boundary']);self.assertFalse(allowed['CLR_or_SDK_executed'])
        self.assertEqual(new_intent('sale',False,False,0)['first_write_boundary'],'ReturnYearPreviews=false-before-CLR');self.assertEqual(new_intent('purchase',False,False,0)['first_write_boundary'],'CLR-entry-only')
    def test_40_new_only_reached_decision_and_explicit_guard_inputs(self):
        for args in (('sale',False,True,0),('purchase',False,False,0,'No'),('sale',False,True,2,'Cancel'),('sale',1,False,2),('other',False,False,0)):
            with self.assertRaises(ValueError):new_intent(*args)
        self.assertFalse(new_intent('sale',True,False,1)['prompt_required']);self.assertTrue(new_intent('purchase',True,False,1,'No')['prompt_required'])
    def test_41_ACTUAL_B32_parser_versionedB31_API15(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B31_CLI['default'],'B31');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B32');p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B32')
        for part in ('A',)+tuple(f'B{i}' for i in range(1,33)):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        for i in range(18,32):self.assertEqual(getattr(v,f'PHASE7_B{i}_CLI')['default'],f'B{i}')
    def test_42_ACTUAL_19_AST_gates_B31_history_before_current(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());live=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(live).hexdigest(),b32.DISPATCHER_SHA)
        tree=ast.parse(live);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main)
        self.assertLess(body.index('historical_b30_validation('),body.index('historical_b31_validation('));self.assertLess(body.index('historical_b31_validation('),body.index('extend_editor_close('));self.assertIn('extend_navigation_load(historical_b31,',body)
        actual=[set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part'];expected=[{f'B{i}' for i in range(first,33)} for first in range(1,20)];self.assertEqual(actual,expected)
        for n in range(19):
            mutant=copy.deepcopy(actual);mutant[n].remove('B32')
            with self.assertRaises(AssertionError):self.assertEqual(mutant,expected)
        blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"];self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_cli_parser')))
    def test_43_ALL48_launcher_local_A_Path_preset_restore_not_oldcode(self):
        src=ast.unparse(ast.parse((A/'tools/run_historical_navigation_load_tests_07B32.py').read_text()))
        for token in ('suite.countTestCases() != 48','run.testsRun != 48 or run.skipped','loadTestsFromModule(historical_tests)','historical_tests.A = v.AUDIT','historical_tests.Path = type(v.AUDIT)','historical_tests.A = original_a','historical_tests.Path = original_path','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B31_CLI','b32.historical_b31_inputs('):self.assertIn(token,src)
        self.assertNotIn('unittest.skip',src);self.assertNotIn('v.__file__ =',src);self.assertNotIn('Path.read_bytes =',src);self.assertNotIn('exec(',src)
    def test_44_historical115_assertion_inputs_distinct_actual119(self):
        prov=json.loads((A/'evidence/provenance-07B32.json').read_bytes());self.assertEqual(len(prov['historical_checker_sources_at_entry']),115);self.assertEqual(len(list((A/'tools').glob('*.py'))),119)
        with (A/b32.SNAPSHOT).open(newline='',encoding='utf8') as f:old=list(csv.DictReader(f))
        texts=json.loads((A/b32.SHARED_SNAPSHOT).read_bytes())['files'];before=v.AUDIT,v.read,v.rows;code=v.main.__code__;file=v.__file__;path_methods=Path.read_bytes,Path.read_text,Path.glob
        with b32.historical_b31_inputs(v,old,texts,(A/b32.SNAPSHOT).read_bytes(),prov['historical_checker_sources_at_entry'],(A/b32.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT/'tools').glob('*.py'))),115);self.assertEqual(hashlib.sha256(type(v.AUDIT)(v.__file__).read_bytes()).hexdigest(),b32.DISPATCHER_SHA)
            self.assertEqual((Path.read_bytes,Path.read_text,Path.glob),path_methods);self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
        self.assertTrue(all(x is y for x,y in zip(before,(v.AUDIT,v.read,v.rows))))
    def test_45_protected942_ALL333_fullraw_and_potential_roots(self):
        p=json.loads((A/'evidence/provenance-07B32.json').read_bytes());self.assertEqual(len(p['historical_artifact_sha256']),942);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==h for n,h in p['historical_artifact_sha256'].items()))
        raw=(A/b32.SNAPSHOT).read_bytes();cur=(A/'findings.csv').read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));now=list(csv.DictReader(io.StringIO(cur.decode(),newline='')));self.assertEqual(b32.registry_preservation_errors(old,now,cur,raw,self.table('historical-extensions')),[])
        for root in ('P4-014','P7-132','P7-145'):self.assertEqual(next(r for r in now if r['id']==root)['certainty'],'potential')
    def test_46_scope5_overlap5_union427_reads22_context9_not_BAML(self):
        d=json.loads((A/'evidence/scope-decision-07B32.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(5,427,5,0,427,400));self.assertEqual((d['historical_metadata_screen_count'],d['parent_path_matched_metadata_rows'],d['selected_contract_slices'],d['exploratory_context_slices']),(333,27,22,9));self.assertFalse(d['all_historical_bodies_reviewed'])
        w=self.witness();self.assertEqual(w['whole_local_files_selected'],0);self.assertFalse(w['compiled_BAML_or_generated_code_executed'])
        for key,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('exploratory_source_reads_not_capability_certification',EXPLORATORY_SLICES)):
            tuples=[]
            for r in w[key]:
                raw=(A.parents[1]/r['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);self.assertFalse(r['whole_local_file_selected']);self.assertLessEqual(r['end'],len(raw.decode().splitlines()));tuples.append((r['path'],r['start'],r['end']))
            self.assertEqual(tuple(tuples),declared)
    def test_47_one162_not159_160_161_or_setter_guess_132(self):
        ad=self.table('root-adjudication');self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='new-local-root'],['P7-162']);self.assertEqual(self.table('historical-extensions'),[]);self.assertTrue(all(r['comparison_depth']==b32.DEDUP_DEPTH for r in ad))
        self.assertEqual(ad[0]['nearest_prior_root_ids'],'P7-159;P7-160;P7-161;P7-132');self.assertIn('Closing',ad[0]['reason']);self.assertIn('F5',ad[1]['reason']);self.assertIn('potential',ad[2]['reason']);self.assertIn('setter',ad[3]['reason'])
        with (A/'findings.csv').open(encoding='utf8',newline='') as f:current=list(csv.DictReader(f))
        r=current[-1];self.assertEqual((r['id'],r['severity'],r['certainty'],r['type'],r['status'],r['next_phase']),('P7-162','Medium','confirmed','implementation-defect','open-not-remediated','8'))
    def test_48_actual_residual_inputs_and_two_substantive_plans_per_FE(self):
        self.assertEqual(b32.residual_errors(self.table('residual-disposition'),self.table('residual-disposition',31)),[]);self.assertEqual(b32.split_errors(self.table('split-register'),self.table('split-register',31)),[])
        fe,iv,ts=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b32.current_link_errors(fe,iv,ts),[])
        for f in fe:
            linked=[t for t in ts if t['feature_ids']==f['id']];self.assertEqual(len(linked),2)
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertGreaterEqual(len(t['procedure']),35);self.assertGreaterEqual(len(t['acceptance_criterion']),35);self.assertIn('إذن',t['prerequisites']);self.assertIn('not-executed',t['safety_controls'])
        for stem in ('handoffs','questions'):
            for old,new in zip(self.table(stem,31),self.table(stem)):self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))
    def test_49_reference_date_raw_clock_capture_delivery_separate(self):
        p=json.loads((A/'evidence/provenance-07B32.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B32.md').read_text();self.assertEqual(b32.date_identity_errors(p,note),[]);self.assertIn('2026-11-16',note);self.assertIn(p['environment_clock_observed_utc'],note)
        self.assertTrue(b32.date_identity_errors(p|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b32.date_identity_errors(p,note.replace(b32.DISPATCHER_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B31-final.json').read_bytes());self.assertNotEqual(old['checkout_head'],b32.ENTRY);self.assertEqual(old['checkout_head'],'038a18b74acb92c35a6172d4619fee5712424489')
    def test_50_synthetic37_schema_is_not_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b32.historical_record_errors(h),[])
        for key,val in (('registry_used','findings.csv'),('findings_total',334),('process_exit_code',True),('audit_checker_self_test_cases_reported',1086),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=val;self.assertTrue(b32.historical_record_errors(bad))
        for key,val in (('tests_reported',47),('historical_source_assertion_input_count',119),('test_module_Path_and_A_are_historical_assertion_inputs_only',1),('auxiliary_dispatcher_text_sha256','b'*64)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B31_child'][key]=val;self.assertTrue(b32.historical_record_errors(bad))
        self.assertTrue(b32.historical_record_errors(h|dict(historical_mode_count=True)))
    def test_51_ACTUAL37_archive_exact119_single_inverse_pin(self):
        p=A/'evidence/historical-mode-verification-07B32.json';raw=p.read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b32.HISTORICAL_RUN_SHA);self.assertEqual(b32.historical_record_errors(h),[]);self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b32.ENTRY,v.HEAD,v.BRANCH))
        sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),119);self.assertEqual(b32.capture_source_errors(h,sources),[])
        for key in ('tools/validate_editor_close_part.py','tools/test_editor_close_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[key]+=b'\n';self.assertTrue(b32.capture_source_errors(h,changed))
        self.assertTrue(b32.capture_source_errors(h,{}));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']));self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        proof=json.loads((A/'evidence/capture-time-identity-07B32.json').read_bytes());self.assertEqual((proof['archive_bytes'],proof['archive_sha256'],proof['capture_tool_set_count'],proof['unchanged_capture_tool_count'],proof['raw_stdout_identities_temporarily_rechecked']),(len(raw),b32.HISTORICAL_RUN_SHA,119,118,37));self.assertTrue(proof['exact_inverse_reconstructs_capture_time_bytes']);self.assertFalse(proof['wholesale37_replayed_after_pin'])
    def test_52_actual119_AST_stdlib_and_every_B31_capture_preserved(self):
        tools=list((A/'tools').glob('*.py'));self.assertEqual(len(tools),119)
        for p in tools:ast.parse(p.read_text(),filename=str(p))
        tree=ast.parse((A/'tools/check_editor_close_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(x.name.split('.')[0] for x in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','pathlib','re','xml'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        p=json.loads((A/'evidence/provenance-07B32.json').read_bytes());old=p['historical_artifact_sha256']
        for name in ('evidence/historical-mode-verification-07B31.json','evidence/capture-time-identity-07B31.json','evidence/checks-07B31.json','evidence/checks-07B31-release.json','evidence/checks-07B31-final.json','evidence/official-capture-wrapper-source01-07B31.py.txt','evidence/official-capture-wrapper-note01-07B31.json','evidence/documents-at-first-capture-07B31.json','evidence/documents-at-release02-07B31.json','evidence/staged-style-check-note-07B31.json','evidence/new-suite-pre-capture46-attempt01-07B31.txt','evidence/checker-preflight-attempt-01-07B29.json','evidence/historical-mode-verification-07B29-release.json','tools/test_navigation_load_audit_validator.py','tools/test_import_cancel_audit_validator.py','tools/run_historical_import_cancel_tests_07B31.py'):
            self.assertIn(name,old);self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),old[name])


if __name__=='__main__':
    unittest.main()
