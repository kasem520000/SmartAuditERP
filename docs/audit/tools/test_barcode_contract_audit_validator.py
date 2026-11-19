#!/usr/bin/env python3
"""32 new synthetic documentary-helper cases, NOT ERP/scanner/SQL acceptance.

All earlier498 cases remain unmodified; B19's36 run in an explicit historical
child/preset. Here actual current B20 parser/entrypoint are tested independently.
No application imports, protected test edits, skipped cases or global patches.
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
from decimal import Decimal as D

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_barcode_contract_part as b20
from validate_navigation_contract_part import historical_b18_inputs
from check_barcode_contract_witnesses import(manual_payload,manual_consumer,manual_prefix_candidates,manual_priority,manual_total,literal_calls)


class BarcodeContractAuditTests(unittest.TestCase):
    def old(self,n=307):return[dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()
    def current(self):return self.old()+[self.old(1)[0]|dict(id=n,next_phase='8')for n in b20.NEW_IDS]
    def texts(self):return{n:'FROZEN:'+n for n in b20.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b20.historical_b19_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def groups(self,end):return'\n'.join(f'| G-{n:02d} | exact |'for n in range(1,end+1))+'\n'
    def callers(self):
        literals=[];current=[]
        for n,(consumer,shape)in enumerate(b20.CALLER_SHAPES.items(),1):
            a=dict(source_path='SmartAuditERP/Form_WPF/'+consumer+'.xaml.cs',call_line_start=n,call_line_end=n,call_text_sha256=hashlib.sha256(str(n).encode()).hexdigest(),inert_argument_expression='"toy-'+str(n)+'"');literals.append(a)
            current.append(dict(**{k:str(v)for k,v in a.items()},consumer=consumer,**dict(zip(('reviewed_effect','quantity_handling','price_handling','scale_flag_handling'),shape)),entry_boundary='named input',owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='bounded followup',limit='not whole callgraph',runtime_status='not-executed'))
        return current,literals
    def contracts(self):
        features=[];invariants=[];tests=[]
        for n in range(1,17):
            fid=f'FE-{n:02d}';iid=f'INV-{n:02d}';roots=b20.NEW_IDS[n-1]if n<=3 else'H';accept=';'.join(f'T-{i:02d}'for i in(2*n-1,2*n));common=dict(finding_ids=roots,evidence='a.cs:1-2',acceptance_ids=accept)
            features.append(dict(id=fid,**common));invariants.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=roots,plan_kind='finding-specific'if n<=3 else'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return features,invariants,tests
    def residuals(self):
        old=[dict(id=f'RS7B19-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',description='prior')for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B19.csv',upstream_row_sha256=b20.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',owner_role='owner',required_redacted_input='input',impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B20-03',disposition='external-handoff',runtime_status='not-executed')for r in old]
        return new,old
    def work(self):
        statuses=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4d-barcode-delivered-residuals-open']+['planned-not-started']*6
        work=[dict(part_family='7B'if i<4 else'7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false')for i,s in enumerate(statuses)]
        splits=[dict(title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='redacted',next_static_action='source trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed')for _ in range(3)]
        return work,splits
    def metadata(self):
        return dict(phase='7B20-partial-static-barcode-contracts',application_code_imported_or_executed=False,scanner_template_or_printer_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,B_R4d_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,illustration_count=12,static_lexical_contract_check_count=12,retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False))
    def history(self):
        names=['phase'+str(n)for n in range(2,7)]+['A']+['B'+str(n)for n in range(1,20)]
        counts=[49,74,106,137,172,200,223,237,248,261,266,270,276,280,282,285,287,289,291,294,298,299,300,302,307]
        registries=['evidence/findings-through-'+f'{n:02d}'+'.csv'for n in range(2,7)]+['evidence/findings-through-07A.csv']+['evidence/findings-through-07B'+str(n)+'.csv'for n in range(1,20)]
        aggregates=[(None,None)]*7+[(44,3),(62,4),(82,5),(104,6),(132,7),(156,8),(184,9),(208,10),(236,11),(266,12),(298,13),(322,14),(350,15),(382,16),(410,17),(434,18),(462,19),(498,20)]
        modes=[dict(mode=n,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,findings_total=count,registry_used=registry,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,audit_checker_self_test_cases_reported=agg[0],audit_checker_self_test_suite_count=agg[1],stdout_sha256='a'*64)for n,count,registry,agg in zip(names,counts,registries,aggregates)]
        modes[-2]['historical_B18_child']=dict(tests_reported=28,expected_tests=28,process_exit_code=0,result='passed',historical_parser_cutoff='B18-not-current-B19-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_caller_request_tests_07B19.py',no_test_skips_or_global_subprocess_or_path_patch=True)
        modes[-1]['historical_B19_child']=dict(tests_reported=36,expected_tests=36,process_exit_code=0,result='passed',historical_parser_cutoff='B19-not-current-B20-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_navigation_tests_07B20.py',no_test_skips_or_global_subprocess_or_path_patch=True)
        return dict(historical_mode_count=25,historical_modes=modes,errors=[])

    def test_01_OWN307_rows_raw308CRLF_and_three_texts(self):
        f=self.fake()
        with self.context(f):self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()));self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
    def test_02_reject_nonexact_OWN_rows_bytes_text_keys(self):
        f=self.fake();old=self.old();raw=self.raw(old)
        for rs,texts,b in((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),(old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw)):
            with self.assertRaises(ValueError):
                with b20.historical_b19_inputs(f,rs,texts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b20.historical_b19_inputs(f,old,self.texts(),self.raw(old)):pass
    def test_03_no_global_Path_or_unrelated_file_overlay(self):
        f=self.fake();before=Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,before);self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')]);self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_bytes()
    def test_04_copy_isolation_restore_on_success_and_exception(self):
        f=self.fake();old=self.old();texts=self.texts();saved=copy.deepcopy(old);before=f.AUDIT,f.read,f.rows
        with b20.historical_b19_inputs(f,old,texts,self.raw(old)):
            x=f.rows('findings.csv');x[0]['next_phase']='bad';self.assertEqual(f.rows('findings.csv'),saved)
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))));self.assertEqual(old,saved)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_05_nested_B18_OWN302_restores_outer307(self):
        f=self.fake()
        with self.context(f):
            with historical_b18_inputs(f,self.old(302),self.texts(),self.raw(self.old(302))):self.assertEqual(len(f.rows('findings.csv')),302)
            self.assertEqual(len(f.rows('findings.csv')),307);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
    def test_06_all307_fields_nextphase_evidence_and_rawprefix_preserved(self):
        old=self.old();cur=self.current();self.assertEqual(b20.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed';self.assertTrue(b20.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)
    def test_07_only_three_roots_raw311CRLF_noBOM(self):
        old=self.old();cur=self.current()
        for bad in(cur[:-1],cur+[dict(cur[-1])],cur[:307]+list(reversed(cur[307:]))):self.assertTrue(b20.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in(self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):self.assertTrue(b20.registry_preservation_errors(old,cur,raw,self.raw(old)))
    def test_08_exact_G190_and_append191through195_only(self):
        self.assertEqual(b20.group_row_errors(self.groups(190),self.groups(195)),[])
        for bad in(self.groups(194),self.groups(196),self.groups(195).replace('G-99','G-98'),self.groups(195).replace('| G-01 | exact','| G-01 | changed')):self.assertTrue(b20.group_row_errors(self.groups(190),bad))
    def test_09_qualified_inert_calls_balanced_quotes_comments_lines_hash(self):
        text='first\nItemOper.SearchForBarcode(\n "a)\\\"", fn(2), /* ) */ ref id);\n'
        r=literal_calls(text,'toy.cs');self.assertEqual(len(r),1);self.assertEqual((r[0]['call_line_start'],r[0]['call_line_end']),(2,3));self.assertIn('fn(2)',r[0]['inert_argument_expression'])
        self.assertEqual(r[0]['call_text_sha256'],hashlib.sha256(text[text.index('ItemOper'):text.index(';')].encode()).hexdigest());self.assertTrue(r[0]['not_type_or_runtime_resolution'])
        self.assertEqual(literal_calls('Other.SearchForBarcode(x)','toy.cs'),[])
        with self.assertRaises(ValueError):literal_calls('ItemOper.SearchForBarcode(fn(', 'toy.cs')
    def test_10_exact_seven_caller_shapes(self):
        cur,lit=self.callers();self.assertEqual(b20.caller_errors(cur,lit),[])
        self.assertEqual(cur[1]['quantity_handling'],'positive-only');self.assertEqual(cur[-1]['quantity_handling'],'not-realstock-count')
    def test_11_reject_caller_lineage_support_or_owner_overclaims(self):
        for key in('call_text_sha256','inert_argument_expression','source_path','call_line_start','consumer','quantity_handling','price_handling','scale_flag_handling','runtime_status'):
            cur,lit=self.callers();cur[0][key]='changed';self.assertTrue(b20.caller_errors(cur,lit),key)
        # Roles and limits are required prose, not hard-coded identities.
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','entry_boundary','limit'):
            cur,lit=self.callers();cur[0][key]='';self.assertTrue(b20.caller_errors(cur,lit),key)
        cur,lit=self.callers();self.assertTrue(b20.caller_errors(cur[:-1],lit));lit[-1]=lit[0];self.assertTrue(b20.caller_errors(cur,lit))
    def test_12_documentary_sentinels_are_explicit_not_fake_source(self):
        errors,calls=[],[];fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b20.validate_source(fake,dict(id='FE7B20-14',evidence=b20.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b20.validate_source(fake,dict(id='UNKNOWN',evidence=b20.DOCUMENTARY),{});self.assertEqual(len(errors),1)
        b20.validate_source(fake,dict(id='FE7B20-01',evidence='a.cs:1-2'),{});self.assertEqual(len(calls),2)
        b20.validate_source(fake,dict(id='FE7B20-14',evidence='a.cs:1-2'),{});self.assertEqual(len(errors),2)
        self.assertEqual(b20.expanded_source_evidence('a.cs:1-2;5;b.cs:7;9-10'),'a.cs:1-2;a.cs:5;b.cs:7;b.cs:9-10')
        for bad in('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:',' :1'):
            with self.assertRaises(ValueError):b20.expanded_source_evidence(bad)
    def test_13_exact_FE16_INV16_T32_bidirectional_not_executed(self):
        self.assertEqual(b20.current_link_errors(*self.contracts()),[])
        for pool,key in((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status')):
            fs,iv,ts=self.contracts();(fs,iv,ts)[pool][0][key]='changed';self.assertTrue(b20.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b20.current_link_errors(fs,iv,ts));self.assertTrue(b20.current_link_errors(fs,iv,ts[:-1]))
    def test_14_all14_residual_id_hash_contract_responsibility(self):
        cur,old=self.residuals();self.assertEqual(b20.residual_errors(cur,old),[])
        for key in cur[0]:
            cur,old=self.residuals();cur[0][key]='';self.assertTrue(b20.residual_errors(cur,old),key)
        cur,old=self.residuals();cur[0]['disposition']='approved';self.assertTrue(b20.residual_errors(cur,old));self.assertTrue(b20.residual_errors(cur[:-1],old))
    def test_15_bounded_R4d_six_C_axes_unstarted_and_reasoned_splits(self):
        work,splits=self.work();self.assertEqual(b20.remaining_work_errors(work,splits),[])
        for i,key,value in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            work,splits=self.work();work[i][key]=value;self.assertTrue(b20.remaining_work_errors(work,splits))
        work,splits=self.work();splits[0]['reason_for_split']='';self.assertTrue(b20.remaining_work_errors(work,splits))
    def test_16_strict_false_integer_zero_counts_and_retained_erratum(self):
        self.assertEqual(b20.witness_metadata_errors(self.metadata()),[])
        for key,value in(('application_code_imported_or_executed',0),('scanner_template_or_printer_executed',None),('erp_runtime_tests_executed',False),('illustration_count',12.0),('B_R4d_bounded_not_whole7B_closure',1),('phase7C_started',True),('phase8_authorized_or_started',True)):
            self.assertTrue(b20.witness_metadata_errors(self.metadata()|{key:value}))
        bad=self.metadata();bad['retained_additive_B10_arithmetic_erratum']['reference_cost']=10;self.assertTrue(b20.witness_metadata_errors(bad))
    def test_17_actual25_record_order_OWN307_counts_historical36_null_not_zero(self):
        self.assertEqual(b20.historical_record_errors(self.history()),[])
        for n,key,value in((24,'findings_total',310),(24,'registry_used','findings.csv'),(24,'stdout_sha256','bad'),(24,'audit_checker_self_test_cases_reported',530),(0,'audit_checker_self_test_cases_reported',0),(0,'erp_runtime_tests_executed',False)):
            h=self.history();h['historical_modes'][n][key]=value;self.assertTrue(b20.historical_record_errors(h))
        h=self.history();h['historical_modes'][-1]['historical_B19_child']['all_original_cases_executed_unmodified']=False;self.assertTrue(b20.historical_record_errors(h));h=self.history();h['historical_modes']=h['historical_modes'][:-1];self.assertTrue(b20.historical_record_errors(h))
    def test_18_manual_weight_payload_discarded_by_named_three_invoices(self):
        p=manual_payload('2300001025000',1);self.assertEqual(p['quantity'],D('2.5'))
        for consumer in('Sale','Purch','InputOutput'):self.assertEqual(manual_consumer(p,consumer),dict(price='10',quantity='1',is_scale=False))
    def test_19_manual_embedded_price_discard_is_not_static_leak(self):
        p=manual_payload('2300001012340',2);self.assertEqual(p['price'],D('12.34'));self.assertEqual(manual_consumer(p,'Sale')['price'],'10');self.assertEqual(manual_consumer(p,'POS')['price'],'12.34')
    def test_20_POS_positive_weight_counterexample_not_blanket_correctness(self):
        self.assertEqual(manual_consumer(manual_payload('2300001025000',1),'POS'),dict(price='10',quantity='2.5',is_scale=True))
        with self.assertRaises(ValueError):manual_consumer(dict(price=D('0'),quantity=D('0')),'unknown')
    def test_21_base_prefix_OR_allows_two_distinct_unit_barcodes(self):
        units=[dict(unit=1,barcode='2300001',equality='1'),dict(unit=12,barcode='BOX0001',equality='12')];r=manual_prefix_candidates('2300001','2300001',units)
        self.assertEqual([x['unit']for x in r],[1,12]);self.assertEqual([D('2.5')*D(x['equality'])for x in r],[D('2.5'),D('30')]);self.assertEqual([x['unit']for x in manual_prefix_candidates('2300001','2300001',list(reversed(units)))],[12,1])
    def test_22_nonbase_unit_specific_prefix_does_not_have_that_multiplicity(self):
        units=[dict(unit=1,barcode='BASE000'),dict(unit=12,barcode='2300001')];self.assertEqual(manual_prefix_candidates('2300001','BASE000',units),[units[1]])
    def test_23_full_alphabetic_payload_zero_does_not_mean_valid_regular_item(self):
        p=manual_payload('2300001AABBB0',1);self.assertEqual(p,dict(price=D('0'),quantity=D('0')));self.assertEqual(manual_consumer(p,'POS'),dict(price='10',quantity='1',is_scale=False))
    def test_24_partial_failure_can_become_positive_quantity(self):
        p=manual_payload('2300001AA2500',1);self.assertEqual(p['quantity'],D('.25'));self.assertEqual(manual_consumer(p,'POS')['quantity'],'0.25')
    def test_25_exact_precedence_and_mode3_rounding_zero_divisor_boundaries(self):
        self.assertEqual(manual_priority(True,True,True),'unit-exact');self.assertEqual(manual_priority(False,True,True),'alias-exact');self.assertEqual(manual_priority(False,False,True),'scale-attempt');self.assertEqual(manual_payload('2300001001000',3,'3')['quantity'],D('.333'));self.assertEqual(manual_payload('2300001001000',3,'0')['quantity'],D('0'))
        with self.assertRaises(ValueError):manual_payload('short',1)
    def test_26_retained_static_flag_model_not_remediation_or_new_root(self):
        self.assertEqual(manual_total(D('2'),D('10'),True,False),D('20'));self.assertEqual(manual_total(D('2'),D('10'),True,True),D('10'));self.assertEqual(manual_total(D('2'),D('10'),False,True),D('20'))
    def test_27_ACTUAL_current_B20_parser_versioned_bases_and_main_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B16_CLI['default'],'B16');self.assertEqual(v.PHASE7_CURRENT_CLI['default'],'B17');self.assertEqual(v.PHASE7_B18_CLI['default'],'B18');self.assertEqual(v.PHASE7_B19_CLI['default'],'B19')
        p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B20');self.assertEqual(p.parse_args(['--through-phase','2']).through_phase,2)
        for part in('A','B15','B16','B17','B18','B19','B20'):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
    def test_28_real_entrypoint_and_historical_B19_context_before_current(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'));self.assertLess(body.index('historical_b19_validation('),body.index('extend_barcode_contracts('));self.assertIn('extend_navigation_contracts(historical_b19,',body);self.assertIn("phase7_part == 'B19'",body)
        parsers=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser'];self.assertEqual(len(parsers),1);self.assertIn('PHASE7_LIVE_CLI',ast.unparse(parsers[0]))
    def test_29_narrow_argv_redirect_keeps_kwargs_and_unrelated_calls(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k))or'sentinel');proxy=b20.HistoricalB19Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=30)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in(proxy.expected+['--different'],['python','-B','/else/test_navigation_contract_audit_validator.py']):proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
    def test_30_facade_context_no_global_subprocess_or_Path_mutation(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel');f=self.fake();f.subprocess=backend;f.sys=SimpleNamespace(executable='python');view=b20.HistoricalB19ValidatorView(f);real_run=subprocess.run;path_read=Path.read_bytes;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):self.assertIs(f.subprocess,backend);self.assertIs(subprocess.run,real_run);self.assertIs(Path.read_bytes,path_read);self.assertEqual(len(view.rows('findings.csv')),307);raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_31_historical_child_ALL36_original_no_skip_and_restores_preset(self):
        p=Path(__file__).parent;s=ast.unparse(ast.parse((p/'run_historical_navigation_tests_07B20.py').read_text()))
        for token in('loadTestsFromModule(historical_tests)','suite.countTestCases() != 36','result.testsRun != 36 or result.skipped','v.PHASE7_LIVE_CLI = original','v.PHASE7_B19_CLI'):self.assertIn(token,s)
        self.assertNotIn('unittest.skip',s);prov=json.loads((p.parent/'evidence/provenance-07B20.json').read_text());self.assertEqual(hashlib.sha256((p/'test_navigation_contract_audit_validator.py').read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/test_navigation_contract_audit_validator.py'])
    def test_32_scope20_old_paths_no_wholebody_or_census_claim(self):
        d=json.loads((Path(__file__).parents[1]/'evidence/scope-decision-07B20.json').read_text());b=d['bookkeeping'];self.assertEqual((b['selected_paths'],b['prior_union'],b['overlap'],b['new'],b['union'],b['complement']),(20,410,20,0,410,417));self.assertEqual(sum(b['complement_kinds'].values()),417)
        self.assertEqual(d['selected_upstream_split'],'SP7B19-03');self.assertEqual((d['literal_qualified_decoder_calls'],d['named_consumer_paths'],d['label_projection_boundaries']),(7,7,2));self.assertIs(d['phase7C_started'],False);self.assertIs(d['phase8_authorized_or_started'],False);self.assertIs(d['counts_are_completion_percent_or_sessions'],False)


if __name__=='__main__':unittest.main()
