#!/usr/bin/env python3
"""48 B31 documentary checker cases, NOT32 acceptance plans or ERP tests.

ALL986 previous cases,including52 B30,remain unchanged. Source-assertion
inputs for historical B30 are111; actual current tools115/parser checked here.
Synthetic36 schema fixtures are NOT real subprocess execution evidence.
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
import validate_navigation_load_part as b31
import validate_import_cancel_part as b30
from check_navigation_load_witnesses import SOURCE_SLICES,trace,editor,guard_denies,bounded_int
A=Path(__file__).resolve().parents[1]


class NavigationLoadAuditTests(unittest.TestCase):
    def old(self):return [dict(id=f'PX-{i:03d}',severity='Medium',certainty='potential',type='synthetic-only',status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for i in range(332)]
    def current(self):return self.old()+[self.old()[0]|dict(id='P7-161',next_phase='8')]
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def texts(self):return {n:'FROZEN:'+n for n in b31.SHARED_DOCS}
    def sources(self):
        raw=b'# fixture historical dispatcher TEXT,not executed\n';return {'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{i:03d}.py':'a'*64 for i in range(110)},raw
    def context(self,f):return b31.historical_b30_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())
    def table(self,stem,part='B31'):return list(csv.DictReader((A/'evidence'/f'{stem}-07{part}.csv').open(encoding='utf8',newline='')))
    def groups(self,n):return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1,n+1))+'\n'
    def witness(self):return json.loads((A/'evidence/navigation-load-witnesses-07B31.json').read_bytes())
    def state(self,**changes):return dict(ref='fixture-EDITOR-A',gid='fixture-DOC-A',is_new=False,is_updated=False)|changes
    def run_model(self,surface='purchase',kind='empty',plan=('normal','normal'),**kwargs):return trace(surface,'next',self.state(),kind,plan,**kwargs)
    def history_fixture(self):
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B30.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B30-not-current-B31-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_import_cancel_tests_07B31.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=111,auxiliary_dispatcher_text_sha256=b31.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B30',findings_total=332,registry_used=b31.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=986,audit_checker_self_test_suite_count=31,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B30_child=child))
        return dict(historical_mode_count=36,historical_modes=modes,errors=[])

    def test_01_OWN332_raw333_three_index_strings(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()));self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old())
    def test_02_reject_bad_shape_raw_BOM_LF_source_vector(self):
        old,raw,src=self.old(),self.raw(self.old()),self.sources()
        for args in ((old[:-1],self.texts(),raw,*src),(old,self.texts(),raw.replace(b'\r\n',b'\n'),*src),(old,self.texts(),b'\xef\xbb\xbf'+raw,*src),(old,{'README.md':'only'},raw,*src),(old,self.texts(),bytearray(raw),*src),(old,self.texts(),raw,{},src[1]),(old,self.texts(),raw,src[0],src[1]+b'x')):
            with self.assertRaises(ValueError):
                with b31.historical_b30_inputs(self.fake(),*args):pass
        old[0]['id']=old[1]['id']
        with self.assertRaises(ValueError):
            with b31.historical_b30_inputs(self.fake(),old,self.texts(),self.raw(old),*src):pass
    def test_03_nested_view_and_exception_restore(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            current=f.AUDIT
            with self.context(f):self.assertEqual(len(f.rows('findings.csv')),332)
            self.assertIs(f.AUDIT,current)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_04_local_canonical_Path_reads_not_global_patch(self):
        f=self.fake();original=Path.read_bytes,Path.read_text,Path.glob;src,raw=self.sources()
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text,Path.glob),original);self.assertEqual(len(list((f.AUDIT/'tools').glob('*.py'))),111)
            self.assertEqual((f.AUDIT/'tools/validate_audit.py').read_bytes(),raw);self.assertEqual((f.AUDIT/'tools/validate_audit.py').resolve(),Path('/synthetic/audit/tools/validate_audit.py'))
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes());self.assertEqual(f.rows('other/findings.csv'),[dict(id='LIVE:other/findings.csv')])
    def test_05_exact_argv_proxy_never_shared_subprocess_patch(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'ok');proxy=b31.HistoricalB30Subprocess(backend,'python',Path('/a/tools'));kw=dict(cwd='/a',timeout=60,capture_output=True,text=True)
        self.assertEqual(proxy.run(list(proxy.expected),**kw),'ok');self.assertEqual(calls[-1],((proxy.actual,),kw))
        for args in (tuple(proxy.expected),proxy.expected+['--other'],['python','-B','/other/test_import_cancel_audit_validator.py']):proxy.run(args,**kw);self.assertEqual(calls[-1],((args,),kw))
        f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b31.HistoricalB30ValidatorView(f);original=subprocess.run
        with self.context(view):self.assertIs(subprocess.run,original);self.assertIs(f.subprocess,backend)
    def test_06_all332_fields_and_evidence_exact(self):
        old,cur=self.old(),self.current();self.assertEqual(b31.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old),[]),[])
        for n in (0,330,331):
            for key in old[n]:
                bad=copy.deepcopy(cur);bad[n][key]='changed';self.assertTrue(b31.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]),(n,key))
    def test_07_entire_raw333_prefix_CRLF_noBOM(self):
        old,cur=self.old(),self.current();frozen=self.raw(old);self.assertTrue(self.raw(cur).startswith(frozen))
        for bad in (self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2],self.raw(cur).replace(b'fixture-title',b'other',1)):self.assertTrue(b31.registry_preservation_errors(old,cur,bad,frozen,[]))
    def test_08_one161_no_extensions_or_recount(self):
        old,cur=self.old(),self.current()
        for bad in (cur[:-1],cur+[dict(cur[-1])],cur[:-1]+[cur[-1]|dict(id='P7-162')]):self.assertTrue(b31.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]))
        self.assertTrue(b31.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old),[dict(finding_id='P7-159')]))
    def test_09_G240_exact_only241_to244(self):
        self.assertEqual(b31.group_row_errors(self.groups(240),self.groups(244)),[])
        for bad in (self.groups(243),self.groups(245),self.groups(244).replace('| G-01 | exact','| G-01 | changed'),self.groups(244).replace('G-240','G-239')):self.assertTrue(b31.group_row_errors(self.groups(240),bad))
    def test_10_documentary_sentinels_and_source_union(self):
        errors,calls=[],[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for name in ('FE7B31-15','RC7B31-05','AD7B31-08'):b31.validate_source(f,dict(id=name,evidence=b31.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]));b31.validate_source(f,dict(id='UNKNOWN',evidence=b31.DOCUMENTARY),{});b31.validate_source(f,dict(id='FE7B31-15',evidence='a.cs:1-2'),{});self.assertEqual(len(errors),2)
        fs=[dict(evidence='a.cs:1-2;3;b.cs:7'),dict(evidence='a.cs:1-2;5;b.cs:7')];self.assertEqual(b31.source_evidence_union(fs),'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5')
    def test_11_ordered_NL8_LO8_mutations(self):
        data=self.table('navigation-load-lineage'),self.table('reader-outcome-lineage');self.assertEqual(b31.ledger_errors(*data),[])
        for pool in (0,1):
            bad=copy.deepcopy(data);bad[pool][0],bad[pool][1]=bad[pool][1],bad[pool][0];self.assertTrue(b31.ledger_errors(*bad))
            for n in range(8):
                bad=copy.deepcopy(data);bad[pool][n]['observation']='all-healthy';self.assertTrue(b31.ledger_errors(*bad))
    def test_12_lineage_responsibility_and_nonexecution(self):
        data=self.table('navigation-load-lineage'),self.table('reader-outcome-lineage')
        for key in ('source_to_output','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(data);bad[1][0][key]='';self.assertTrue(b31.ledger_errors(*bad),key)
        bad=copy.deepcopy(data);bad[0][0]['runtime_status']='passed';self.assertTrue(b31.ledger_errors(*bad))
    def test_13_FE16_INV16_T32_bidirectional_links(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b31.current_link_errors(*data),[])
        for pool,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            bad=copy.deepcopy(data);bad[pool][0][key]='changed';self.assertTrue(b31.current_link_errors(*bad))
    def test_14_distinct_criteria_responsibilities_not_generic_plans(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')]
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            bad=copy.deepcopy(data);bad[0][0][key]='';self.assertTrue(b31.current_link_errors(*bad))
        for pool,key in ((1,'required_invariant'),(2,'acceptance_criterion')):
            bad=copy.deepcopy(data);bad[pool][1][key]=bad[pool][0][key];self.assertTrue(b31.current_link_errors(*bad))
    def test_15_RS14_ancestry_rowSHA_contracts(self):
        old,new=self.table('residual-disposition','B30'),self.table('residual-disposition');self.assertEqual(b31.residual_errors(new,old),[])
        for key in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(new);bad[0][key]='changed';self.assertTrue(b31.residual_errors(bad,old))
    def test_16_all_old_inputs_routes_dispositions_retained(self):
        old,new=self.table('residual-disposition','B30'),self.table('residual-disposition')
        for key,val in (('required_redacted_input','only new'),('current_handoff_or_split_ids','H7B31-01'),('disposition','approved'),('runtime_status','passed'),('local_result','')):
            bad=copy.deepcopy(new);bad[2][key]=val;self.assertTrue(b31.residual_errors(bad,old))
        self.assertTrue(b31.residual_errors(new[:-1],old))
    def test_17_SP3_all_old_inputs_prefix_and_future_status(self):
        old,new=self.table('split-register','B30'),self.table('split-register');self.assertEqual(b31.split_errors(new,old),[])
        for key in ('upstream_split_id','upstream_artifact','upstream_row_sha256','required_input','reason_for_split','status','runtime_status'):
            bad=copy.deepcopy(new);bad[0][key]='changed' if key!='reason_for_split' else '';self.assertTrue(b31.split_errors(bad,old))
    def test_18_fourB_sixC_RW10_and_BK_ancestry(self):
        work=self.table('remaining-workplan');self.assertEqual(b31.remaining_work_errors(work),[])
        for n,key,val in ((3,'status','complete'),(4,'status','started'),(0,'part_family','7C'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            bad=copy.deepcopy(work);bad[n][key]=val;self.assertTrue(b31.remaining_work_errors(bad))
        for n,r in enumerate(self.table('continuation-backlog'),1):self.assertEqual((r['prior_backlog_id'],r['original_backlog_id']),(f'BK7B30-{n:02d}',f'BK7-{n:02d}'));self.assertNotEqual(r['status'],'complete')
    def test_19_witness_metadata_strict_bool_count_and_B10(self):
        w=self.witness();self.assertEqual(b31.witness_metadata_errors(w),[])
        for key in ('application_code_imported_or_executed','provider_failure_observed','stable_post_event_state_claimed','database_commit_or_saved_loss_claimed'):
            for val in (True,0):self.assertTrue(b31.witness_metadata_errors(w|{key:val}))
        for key in ('illustration_count','whole_local_files_selected','erp_runtime_tests_executed'):self.assertTrue(b31.witness_metadata_errors(w|{key:True}))
        bad=copy.deepcopy(w);bad['retained_additive_B10_arithmetic_erratum']['local_cost']=20;self.assertTrue(b31.witness_metadata_errors(bad))
    def test_20_actual_witness_bytes_readonly_recompute(self):
        raw=(A/'evidence/navigation-load-witnesses-07B31.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b31.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_navigation_load_witnesses.py')],capture_output=True,timeout=20);self.assertEqual((run.returncode,run.stderr,run.stdout),(0,b'',raw))
        self.assertTrue(all(x['illustration_assertions_passed'] is True and x['source_application_executed'] is False for x in self.witness()['illustrations']))
    def test_21_clean_purchase_known_empty_alone_two_resets(self):
        t=self.run_model();self.assertFalse(t['guard_denied']);self.assertEqual((t['reset_cycles'],t['number_helper_calls'],t['explicit_new_expressions_reached']),(2,2,3));self.assertFalse(t['original_editor_ref_still_current']);self.assertTrue(t['state_at_source_boundary']['is_new']);self.assertFalse(t['binding_attempted'])
    def test_22_clean_sale_known_empty_same161(self):
        t=self.run_model('sale');self.assertEqual(t['reset_cycles'],2);self.assertIn('pre-read.old-grid-source-unbound',t['events']);self.assertFalse(t['original_editor_ref_still_current']);self.assertFalse(t['exception_escaped'])
    def test_23_outer_failure_before_header_same_null_path(self):
        for sf in ('purchase','sale'):
            t=self.run_model(sf,'outer-failed-before-header');self.assertTrue(t['reader_called']);self.assertTrue(t['fallback_reached']);self.assertEqual(t['reset_cycles'],2);self.assertFalse(self.witness()['provider_failure_observed'])
    def test_24_outer_after_header_not_rollback(self):
        for sf in ('purchase','sale'):
            t=self.run_model(sf,'outer-failed-after-header');self.assertTrue(t['temporary_target_header_then_outer_null']);self.assertFalse(t['original_editor_ref_still_current']);self.assertEqual(t['state_at_source_boundary']['gid'],'SDK-default-not-modeled')
    def test_25_found_attempts_binding_not_full_hydration(self):
        for sf in ('purchase','sale'):
            t=self.run_model(sf,'found',('normal',));self.assertEqual(t['reset_cycles'],1);self.assertTrue(t['binding_attempted']);self.assertFalse(t['fallback_reached']);self.assertEqual((t['state_at_source_boundary']['gid'],t['state_at_source_boundary']['is_new']),('fixture-DOC-B',False));self.assertTrue(t['supplied_target_hydration_not_executed'])
    def test_26_inner_row_catch_nonnull_is_not_outer_null(self):
        for sf in ('purchase','sale'):
            t=self.run_model(sf,'row-caught-nonnull',('normal',));self.assertTrue(t['binding_attempted']);self.assertFalse(t['fallback_reached']);self.assertIn('partial',t['state_at_source_boundary']['target_completeness'])
    def test_27_guard_No_stops_before_first_write(self):
        for sf in ('purchase','sale'):
            old=self.state(is_updated=True);t=trace(sf,'first',old,None,[],decision='No');self.assertTrue(t['guard_denied']);self.assertTrue(t['original_editor_ref_still_current']);self.assertEqual(t['state_at_source_boundary'],old);self.assertEqual((t['reset_cycles'],t['reader_called']),(0,False))
    def test_28_guard_Yes_and_clean_not_target_success(self):
        for sf in ('purchase','sale'):
            t=trace(sf,'last',self.state(is_updated=True),'empty',['normal','normal'],decision='Yes');self.assertFalse(t['guard_denied']);self.assertTrue(t['fallback_reached']);self.assertFalse(guard_denies(sf,self.state(),2,'No'))
        st=self.state(is_new=True);self.assertTrue(guard_denies('purchase',st,1,'No'));self.assertFalse(guard_denies('sale',st,1,'No'));self.assertTrue(guard_denies('sale',st,2,'No'))
    def test_29_purchase_first_number_failure_swallowed_then_reader(self):
        t=self.run_model('purchase','empty',['number-failed','normal']);self.assertTrue(t['reader_called']);self.assertFalse(t['exception_escaped']);self.assertIn('pre-read.number-failure-swallowed-by-CLR',t['events']);self.assertTrue(t['state_at_source_boundary']['is_new'])
    def test_30_sale_first_number_failure_escapes_before_reader(self):
        t=self.run_model('sale',None,['number-failed']);self.assertTrue(t['exception_escaped']);self.assertFalse(t['reader_called']);self.assertFalse(t['fallback_reached']);self.assertIsNone(t['state_at_source_boundary']['is_new']);self.assertFalse(t['original_editor_ref_still_current'])
    def test_31_second_number_failure_no_new_flag_default_claim(self):
        for sf in ('purchase','sale'):
            t=self.run_model(sf,'empty',['normal','number-failed']);self.assertEqual(t['exception_escaped'],sf=='sale');self.assertIsNone(t['state_at_source_boundary']['is_new']);self.assertEqual(t['number_helper_calls'],2);self.assertTrue(t['fallback_reached'])
    def test_32_null_original_only_fallback_no_old_editor_to_preserve(self):
        for sf in ('purchase','sale'):
            t=trace(sf,'first',None,'empty',['normal']);self.assertEqual((t['reset_cycles'],t['number_helper_calls'],t['explicit_new_expressions_reached']),(1,1,2));self.assertTrue(t['fallback_reached'])
    def test_33_reject_key_domain_lead_and_number_reservation_inference(self):
        checks=self.witness()['static_lexical_contract_checks'];self.assertTrue(checks[-1]['documented_text_observation_matches']);self.assertIn('InvoiceNo-really-reads-id',checks[-1]['boundary']);self.assertIn('not-reservation',checks[-2]['boundary'])
        for command in ('first','previous','next','last'):
            t=trace('purchase',command,self.state(),'empty',['normal','normal'],candidate=41);self.assertEqual(t['state_at_source_boundary']['number'],41)
    def test_34_strict_editor_flags_counts_tokens_and_guard_types(self):
        for bad in ([],{},self.state(ref='business'),self.state(is_new=1),self.state(gid=''),self.state()|dict(extra=1)):
            with self.assertRaises(ValueError):editor(bad)
        for value in (True,False,1.0,'1',None,-1,1000):
            with self.assertRaises(ValueError):bounded_int(value)
        for args in (('other',self.state(),2,'No'),('sale',self.state(),True,'No'),('sale',self.state(),2,False)):
            with self.assertRaises(ValueError):guard_denies(*args)
    def test_35_unreached_inputs_rejected_and_copy_isolated(self):
        for sf,old,kind,plan in (('purchase',self.state(is_updated=True),'empty',[]),('sale',self.state(),'empty',['number-failed']),('purchase',self.state(),None,['normal']),('purchase',self.state(),'unknown',['normal']),('purchase',None,'found',[]),('purchase',self.state(),'empty',['normal','normal','normal'])):
            with self.assertRaises(ValueError):trace(sf,'next',old,kind,plan)
        st=self.state();saved=copy.deepcopy(st);t=trace('purchase','next',st,'empty',['normal','normal']);t['state_at_source_boundary']['ref']='changed';self.assertEqual(st,saved)
        with self.assertRaises(ValueError):trace('other','next',st,'empty',[])
    def test_36_ACTUAL_B31_parser_versionedB30_API15(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B30_CLI['default'],'B30');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B31');p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B31')
        for part in ('A',)+tuple(f'B{i}' for i in range(1,32)):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        for i in range(18,31):self.assertEqual(getattr(v,f'PHASE7_B{i}_CLI')['default'],f'B{i}')
    def test_37_ACTUAL_source_19gates_B30_history_before_B31(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());live=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(live).hexdigest(),b31.DISPATCHER_SHA)
        tree=ast.parse(live);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main)
        self.assertLess(body.index('historical_b29_validation('),body.index('historical_b30_validation('));self.assertLess(body.index('historical_b30_validation('),body.index('extend_navigation_load('));self.assertIn('extend_import_cancel(historical_b30,',body)
        actual=[set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part'];expected=[{f'B{i}' for i in range(first,32)} for first in range(1,20)];self.assertEqual(actual,expected)
        for n in range(19):
            mutant=copy.deepcopy(actual);mutant[n].remove('B31')
            with self.assertRaises(AssertionError):self.assertEqual(mutant,expected)
        blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"];self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_cli_parser')))
    def test_38_ALL52_launcher_module_local_A_Path_preset_restore(self):
        src=ast.unparse(ast.parse((A/'tools/run_historical_import_cancel_tests_07B31.py').read_text()))
        for token in ('suite.countTestCases() != 52','run.testsRun != 52 or run.skipped','loadTestsFromModule(historical_tests)','historical_tests.A = v.AUDIT','historical_tests.Path = type(v.AUDIT)','historical_tests.A = original_a','historical_tests.Path = original_path','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B30_CLI','b31.historical_b30_inputs('):self.assertIn(token,src)
        self.assertNotIn('unittest.skip',src);self.assertNotIn('v.__file__ =',src);self.assertNotIn('Path.read_bytes =',src)
    def test_39_historical111_assertions_distinct_actual115(self):
        prov=json.loads((A/'evidence/provenance-07B31.json').read_bytes());self.assertEqual(len(prov['historical_checker_sources_at_entry']),111);current={p.relative_to(A).as_posix() for p in (A/'tools').glob('*.py')};self.assertEqual(len(current),115)
        old=list(csv.DictReader((A/b31.SNAPSHOT).open(newline='')));texts=json.loads((A/b31.SHARED_SNAPSHOT).read_bytes())['files'];before=v.AUDIT,v.read,v.rows;code=v.main.__code__;file=v.__file__;path_methods=Path.read_bytes,Path.read_text,Path.glob
        with b31.historical_b30_inputs(v,old,texts,(A/b31.SNAPSHOT).read_bytes(),prov['historical_checker_sources_at_entry'],(A/b31.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT/'tools').glob('*.py'))),111);self.assertEqual(hashlib.sha256((v.AUDIT/'tools/validate_audit.py').read_bytes()).hexdigest(),b31.DISPATCHER_SHA)
            self.assertEqual((Path.read_bytes,Path.read_text,Path.glob),path_methods);self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
        self.assertTrue(all(x is y for x,y in zip(before,(v.AUDIT,v.read,v.rows))))
    def test_40_protected900_and_actual332_fullrawprefix(self):
        p=json.loads((A/'evidence/provenance-07B31.json').read_bytes());self.assertEqual(len(p['historical_artifact_sha256']),900);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==h for n,h in p['historical_artifact_sha256'].items()))
        raw=(A/b31.SNAPSHOT).read_bytes();cur=(A/'findings.csv').read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));now=list(csv.DictReader(io.StringIO(cur.decode(),newline='')));self.assertEqual(b31.registry_preservation_errors(old,now,cur,raw,self.table('historical-extensions')),[])
        for root in ('P4-014','P7-132','P7-145'):self.assertEqual(next(r for r in now if r['id']==root)['certainty'],'potential')
    def test_41_scope5_overlap5_new0_union427_14reads_0whole(self):
        d=json.loads((A/'evidence/scope-decision-07B31.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(5,427,5,0,427,400));self.assertEqual((d['historical_metadata_screen_count'],d['path_matched_metadata_rows'],d['whole_reader_method_lines']),(332,79,290))
        w=self.witness();self.assertEqual(w['whole_local_files_selected'],0);tuples=[]
        for r in w['bounded_source_reads_not_semantic_coverage']:
            raw=(A.parents[1]/r['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);self.assertFalse(r['whole_local_file_selected']);self.assertLessEqual(r['end'],len(raw.decode().splitlines()));tuples.append((r['path'],r['start'],r['end']))
        self.assertEqual(tuple(tuples),SOURCE_SLICES)
    def test_42_root161_known_empty_not_guard159_or_conversion160(self):
        ad=self.table('root-adjudication');self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='new-local-root'],['P7-161']);self.assertEqual(self.table('historical-extensions'),[]);self.assertTrue(all(r['comparison_depth']==b31.DEDUP_DEPTH for r in ad));self.assertEqual(ad[0]['nearest_prior_root_ids'],'P7-159;P7-160;P7-046;P7-132');self.assertIn('clean',ad[0]['reason']);self.assertIn('Empty',ad[0]['reason'])
    def test_43_actual_residuals_splits_and_substantive_two_plans_each(self):
        self.assertEqual(b31.residual_errors(self.table('residual-disposition'),self.table('residual-disposition','B30')),[]);self.assertEqual(b31.split_errors(self.table('split-register'),self.table('split-register','B30')),[])
        fe,iv,ts=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b31.current_link_errors(fe,iv,ts),[])
        for f in fe:
            linked=[t for t in ts if t['feature_ids']==f['id']];self.assertEqual(len(linked),2)
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertGreater(len(t['procedure']),35);self.assertGreater(len(t['acceptance_criterion']),35);self.assertIn('إذن',t['prerequisites']);self.assertIn('not-executed',t['safety_controls'])
        for stem in ('handoffs','questions'):
            for old,new in zip(self.table(stem,'B30'),self.table(stem)):self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))
    def test_44_authoritative_date_rawclock_capture_delivery_separate(self):
        p=json.loads((A/'evidence/provenance-07B31.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B31.md').read_text();self.assertEqual(b31.date_identity_errors(p,note),[]);self.assertIn('2026-11-16',note);self.assertIn(p['environment_clock_observed_utc'],note)
        self.assertTrue(b31.date_identity_errors(p|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b31.date_identity_errors(p,note.replace(b31.DISPATCHER_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B30.json').read_bytes());self.assertNotEqual(old['checkout_head'],b31.ENTRY);self.assertEqual(old['checkout_head'],'3589d23a26438300d631790487eafe3aaddef7fb')
    def test_45_synthetic36_schema_not_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b31.historical_record_errors(h),[])
        for key,val in (('registry_used','findings.csv'),('findings_total',333),('process_exit_code',True),('audit_checker_self_test_cases_reported',1034),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=val;self.assertTrue(b31.historical_record_errors(bad))
        for key,val in (('tests_reported',51),('historical_source_assertion_input_count',115),('test_module_Path_and_A_are_historical_assertion_inputs_only',1),('auxiliary_dispatcher_text_sha256','b'*64)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B30_child'][key]=val;self.assertTrue(b31.historical_record_errors(bad))
        self.assertTrue(b31.historical_record_errors(h|dict(historical_mode_count=True)))
    def test_46_ACTUAL36_archive_single_inverse_pin_current115(self):
        p=A/'evidence/historical-mode-verification-07B31.json';raw=p.read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b31.HISTORICAL_RUN_SHA);self.assertEqual(b31.historical_record_errors(h),[]);self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b31.ENTRY,v.HEAD,v.BRANCH))
        sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),115);self.assertEqual(b31.capture_source_errors(h,sources),[])
        for key in ('tools/validate_navigation_load_part.py','tools/test_navigation_load_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[key]+=b'\n';self.assertTrue(b31.capture_source_errors(h,changed))
        self.assertTrue(b31.capture_source_errors(h,{}));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']));self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
    def test_47_current115_tool_AST_witness_stdlib_only(self):
        tools=list((A/'tools').glob('*.py'));self.assertEqual(len(tools),115)
        for p in tools:ast.parse(p.read_text(),filename=str(p))
        tree=ast.parse((A/'tools/check_navigation_load_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(x.name.split('.')[0] for x in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','pathlib','re'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
    def test_48_B30_history_B29_archives_failure_and_tests_retained(self):
        p=json.loads((A/'evidence/provenance-07B31.json').read_bytes());old=p['historical_artifact_sha256']
        self.assertEqual(hashlib.sha256((A/'evidence/historical-mode-verification-07B30.json').read_bytes()).hexdigest(),'5c7a3741d12389a71f953b491ca8b94040a425562647420f6aa17c953be194d9');self.assertEqual((A/'evidence/capture-time-identity-07B30.json').stat().st_size,7323)
        for name in ('evidence/checker-preflight-attempt-01-07B29.json','evidence/checker-preflight-attempt-01-07B29-note.json','evidence/checker-preflight-sources-07B29.json','evidence/historical-mode-verification-07B29-release.json'):
            self.assertIn(name,old);self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),old[name])
        self.assertEqual(hashlib.sha256((A/'evidence/new-suite-pre-capture46-attempt01-07B31.txt').read_bytes()).hexdigest(),'047e343e1e530ffcc159a4ed6be7b1c00c91965ea0498d7e308f345e3b6ae88f');self.assertEqual(hashlib.sha256((A/'evidence/new-suite-pre-capture46-test-source01-07B31.py.txt').read_bytes()).hexdigest(),'c524bc1c12dcece2bdbf32221d95cf5793c11a732d02f6903bc4542511f82126')
        for name in ('test_import_cancel_audit_validator.py','validate_import_cancel_part.py','run_historical_dirty_navigation_tests_07B30.py','test_dirty_navigation_audit_validator.py','test_search_snapshot_audit_validator.py','test_invoice_search_audit_validator.py'):
            self.assertEqual(hashlib.sha256((A/'tools'/name).read_bytes()).hexdigest(),old['tools/'+name])


if __name__=='__main__':
    unittest.main()
