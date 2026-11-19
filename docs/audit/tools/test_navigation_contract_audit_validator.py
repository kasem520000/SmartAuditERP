#!/usr/bin/env python3
"""36 NEW documentary-helper cases, not ERP/WPF/SQL/business acceptance.

Prior462 cases/19 suites remain unmodified; B18's28 run in explicit historical
child/preset. Here current actual B19 parser/entrypoint and narrow adapter are
independently tested. Synthetic rows/text/Decimal models; never app imports.
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
from datetime import datetime

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_navigation_contract_part as b19
from validate_caller_request_part import historical_b17_inputs
from check_navigation_contract_witnesses import(extract_literal_navigations,fields_from_create,after_lifecycle,
 production_qty_edit,production_unit_edit,rehydrate_component,pos_save_date)


class NavigationContractAuditTests(unittest.TestCase):
    def old(self,n=302):
        return[dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',type='synthetic-only',
            status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]
    def raw(self,rs):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rs[0]),lineterminator='\r\n');w.writeheader();w.writerows(rs);return s.getvalue().encode()
    def current(self):return self.old()+[self.old(1)[0]|dict(id=f'P7-{n}',next_phase='8')for n in range(131,136)]
    def texts(self):return{n:'FROZEN:'+n for n in b19.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b19.historical_b18_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def groups(self):return'\n'.join(f'| G-{n:02d} | exact |'for n in range(1,185))+'\n'
    def groups_current(self):return self.groups()+'\n'.join(f'| G-{n:02d} | new |'for n in range(185,191))+'\n'
    def navigation(self):
        literal=[dict(source_path='detail.cs'if i<14 else'inventory.cs',call_line_start=i+1,call_line_end=i+1,
            call_text_sha256=hashlib.sha256(str(i).encode()).hexdigest(),inert_argument_expression='"query-'+str(i)+'"')for i in range(19)]
        indices=list(range(14))+[14,14,15,16,16,17,16,18];cur=[]
        leaves=[b19.LEAVES[i]for i in(0,0,1,1,2,2,1,3,3,4,4,5,5,6,5,5,1,3,3,4,3,6)]
        types=['2','2','1','1','3','3','9','4','5','6','6','8','8','SafesAdjust','8','8','9','4','5','6','14','7']
        procs=['1','2','1','2','1','2','1','1','1','1','2','1','2','not-in-query']+['row.ProcType']*8
        for n,(i,leaf)in enumerate(zip(indices,leaves)):
            p='detailed'if n<14 else'inventory';actual=literal[i]
            cur.append(dict(**{k:str(val)for k,val in actual.items()},parent=p,publication_order='configure-Navigate-before-Show'if p=='detailed'else'Show-before-Navigate-not-Loaded-completion-proof',
                query_inv_type=types[n],query_proc_type=procs[n],identity_contract='display-label-plus-local-id-no-branch-in-query'if n<14 else'row-InvGlobalID-and-procType-plus-current-type-index',
                route_discriminator='synthetic label'if n<14 else'cmbType.SelectedIndex='+str(n-14),leaf=leaf,
                receiver_boundary=f'LC7B19-{b19.LEAVES.index(leaf)+1:02d}',finding_ids='P7-131'if n==21 else'H',limit='not WPF semantics',
                owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='named followup',runtime_status='not-executed'))
        return cur,literal
    def leaves(self):
        fields=('entry_and_reader','empty_or_failure_contract','lifecycle_boundary','dirty_guard_boundary','save_guard_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit')
        return[dict(leaf=leaf,runtime_status='not-executed',**{k:'named boundary '+k for k in fields})for leaf in b19.LEAVES]
    def contracts(self):
        features=[];invariants=[];tests=[]
        for n in range(1,19):
            fid=f'FE-{n:02d}';iid=f'INV-{n:02d}';roots=b19.NEW_IDS[n-1]if n<=5 else'H'
            accept=';'.join(f'T-{i:02d}'for i in(2*n-1,2*n));common=dict(finding_ids=roots,evidence='a.cs:1-2',acceptance_ids=accept)
            features.append(dict(id=fid,**common));invariants.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=roots,plan_kind='finding-specific'if n<=5 else'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return features,invariants,tests
    def residual(self):
        up=[dict(id=f'RS7B18-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',description='prior')for n in range(1,15)]
        cur=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B18.csv',upstream_row_sha256=b19.row_sha(r),
            upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',owner_role='owner',required_redacted_input='input',impact_if_unavailable='blocked',
            next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B19-03',disposition='external-handoff',runtime_status='not-executed')for r in up]
        return cur,up
    def work(self):
        statuses=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4c-navigation-delivered-residuals-open']+['planned-not-started']*6
        work=[dict(part_family='7B'if i<4 else'7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false')for i,s in enumerate(statuses)]
        splits=[dict(title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='redacted',next_static_action='source trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed')for _ in range(3)]
        return work,splits
    def metadata(self):
        return dict(phase='7B19-partial-static-navigation-contracts',application_code_imported_or_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,
            spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
            B_R4c_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,illustration_count=14,static_lexical_contract_check_count=14,
            retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False))
    def historical(self):
        names=['phase'+str(n)for n in range(2,7)]+['A']+['B'+str(n)for n in range(1,19)]
        counts=[49,74,106,137,172,200,223,237,248,261,266,270,276,280,282,285,287,289,291,294,298,299,300,302]
        registries=['evidence/findings-through-'+f'{n:02d}'+'.csv'for n in range(2,7)]+['evidence/findings-through-07A.csv']+['evidence/findings-through-07B'+str(n)+'.csv'for n in range(1,19)]
        aggregates=[(None,None)]*7+[(44,3),(62,4),(82,5),(104,6),(132,7),(156,8),(184,9),(208,10),(236,11),(266,12),(298,13),(322,14),(350,15),(382,16),(410,17),(434,18),(462,19)]
        modes=[dict(mode=n,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,findings_total=count,registry_used=registry,
            erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,audit_checker_self_test_cases_reported=agg[0],audit_checker_self_test_suite_count=agg[1],stdout_sha256='a'*64)
            for n,count,registry,agg in zip(names,counts,registries,aggregates)]
        modes[-1]['historical_B18_child']=dict(tests_reported=28,expected_tests=28,process_exit_code=0,result='passed',historical_parser_cutoff='B18-not-current-B19-default',
            all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_caller_request_tests_07B19.py',no_test_skips_or_global_subprocess_or_path_patch=True)
        return dict(historical_mode_count=24,errors=[],historical_modes=modes)

    def test_01_OWN302_rows_exact303CRLF_and_indexes(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
    def test_02_no_global_Path_patch_or_unrelated_overlay(self):
        f=self.fake();method=Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,method);self.assertEqual((f.AUDIT/'x'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(f.rows('other/findings.csv'),[dict(id='LIVE:other/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/elsewhere/findings.csv').read_bytes()
    def test_03_normal_and_exception_restore_all_identities(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):pass
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_04_wrong_counts_and_duplicate_OWN_rows_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in(self.old(300),self.old(307),duplicate):
            with self.assertRaises(ValueError):
                with b19.historical_b18_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass
    def test_05_exact_noBOM_CRLF_trailing_row_consistency(self):
        raw=self.raw(self.old())
        for bad in(None,'text',b'\xef\xbb\xbf'+raw,raw.replace(b'\r\n',b'\n'),raw+b'\r',raw+b'\r\n',raw.replace(b'synthetic',b'changed',1),b'\xff'):
            with self.assertRaises(ValueError):
                with b19.historical_b18_inputs(self.fake(),self.old(),self.texts(),bad):pass
    def test_06_index_keys_copy_safety_failed_entry_restore(self):
        for texts in({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            f=self.fake();before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b19.historical_b18_inputs(f,self.old(),texts,self.raw(self.old())):pass
            self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
        f=self.fake();old=self.old();texts=self.texts()
        with b19.historical_b18_inputs(f,old,texts,self.raw(old)):
            texts['PLAN.md']='changed';f.rows('findings.csv')[0]['title']='changed'
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md');self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic')
    def test_07_nested_B17_OWN300_restores_to302(self):
        f=self.fake();inner=self.old(300)
        with self.context(f):
            with self.assertRaises(RuntimeError):
                with historical_b17_inputs(f,inner,self.texts(),self.raw(inner)):
                    self.assertEqual(len(f.rows('findings.csv')),300);raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),302);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
    def test_08_ALL302_fields_and_nextphase_rawprefix_preserved(self):
        old,cur=self.old(),self.current();frozen=self.raw(old)
        self.assertEqual(b19.registry_preservation_errors(old,cur,self.raw(cur),frozen),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]+='changed';self.assertTrue(b19.registry_preservation_errors(old,bad,self.raw(bad),frozen))
    def test_09_only_five_new_roots_order_and_CRLF_not_LF(self):
        old,cur=self.old(),self.current();raw=self.raw(cur);frozen=self.raw(old)
        for bad in(cur[::-1],cur[:-1],cur+[cur[-1]]):self.assertTrue(b19.registry_preservation_errors(old,bad,self.raw(bad),frozen))
        for bad in(raw+b'\r',b'\xef\xbb\xbf'+raw,raw.replace(b'\r\n',b'\n')):self.assertTrue(b19.registry_preservation_errors(old,cur,bad,frozen))
    def test_10_G184_exact_prefix_six_new_groups_not_substring(self):
        self.assertEqual(b19.group_row_errors(self.groups(),self.groups_current()),[])
        self.assertTrue(b19.group_row_errors(self.groups(),self.groups_current().replace('G-06 | exact','G-06 | changed')))
        self.assertTrue(b19.group_row_errors(self.groups(),self.groups_current()+'| G-191 | extra |\n'))
    def test_11_inert_literal_line_hash_nested_parentheses_inside_string(self):
        call=extract_literal_navigations('x\nf.Navigate($"SELECT (1) FROM t " +\n $"WHERE id={id}");\n','fake.cs',10)[0]
        self.assertEqual((call['call_line_start'],call['call_line_end']),(11,12))
        self.assertEqual(call['inert_argument_expression'],'$"SELECT (1) FROM t " +\n $"WHERE id={id}"')
        self.assertEqual(call['call_text_sha256'],hashlib.sha256('f.Navigate($"SELECT (1) FROM t " +\n $"WHERE id={id}")'.encode()).hexdigest())
    def test_12_nonmatching_not_complete_callgraph_and_unclosed_rejected(self):
        self.assertEqual(extract_literal_navigations('other.Navigate("x"); Navigate("x");','fake.cs'),[])
        with self.assertRaises(ValueError):extract_literal_navigations('f.Navigate("x"','fake.cs')
        # Lexical token discovery does not resolve comments; limitation intentional.
        self.assertEqual(len(extract_literal_navigations('// f.Navigate("inert");','fake.cs')),1)
    def test_13_NV22_instances_exact19_calls_two_parents_seven_leaves(self):self.assertEqual(b19.navigation_errors(*self.navigation()),[])
    def test_14_NV_mutated_line_hash_receiver_order_and_runtime_rejected(self):
        for key in('source_path','call_line_start','call_line_end','call_text_sha256','inert_argument_expression','leaf','receiver_boundary','parent','publication_order','query_inv_type','query_proc_type','identity_contract','limit','owner_role','runtime_status'):
            cur,lit=self.navigation();cur[0][key]='';self.assertTrue(b19.navigation_errors(cur,lit),key)
        cur,lit=self.navigation();self.assertTrue(b19.navigation_errors(cur[:-1],lit));cur[-1]['finding_ids']='H';self.assertTrue(b19.navigation_errors(cur,lit))
        cur,lit=self.navigation();cur[0].update(leaf='frmInvPurch',receiver_boundary='LC7B19-02');self.assertTrue(b19.navigation_errors(cur,lit))
        cur,lit=self.navigation();lit[1]=lit[0];self.assertTrue(b19.navigation_errors(cur,lit))
    def test_15_LC7_exact_selected_boundaries_not_whole_editors(self):
        self.assertEqual(b19.leaf_errors(self.leaves()),[])
        for key in('leaf','empty_or_failure_contract','save_guard_boundary','dirty_guard_boundary','lifecycle_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','runtime_status'):
            cur=self.leaves();cur[0][key]='';self.assertTrue(b19.leaf_errors(cur),key)
    def test_16_FE_INV_T_exact_two_plans_per_contract_five_roots(self):self.assertEqual(b19.current_link_errors(*self.contracts()),[])
    def test_17_bad_lineage_execution_or_duplicate_acceptance_rejected(self):
        for key in('feature_ids','finding_ids','evidence','acceptance_ids'):
            fe,inv,tests=self.contracts();inv[0][key]='wrong';self.assertTrue(b19.current_link_errors(fe,inv,tests))
        for patch in({'status':'passed'},{'finding_ids':'P7-132'},{'feature_ids':'FE-02'},{'plan_kind':'generic'}):
            fe,inv,tests=self.contracts();tests[0]|=patch;self.assertTrue(b19.current_link_errors(fe,inv,tests))
        fe,inv,tests=self.contracts();tests[1]['acceptance_criterion']=tests[0]['acceptance_criterion'];self.assertTrue(b19.current_link_errors(fe,inv,tests))
    def test_18_all14_residuals_exact_upstream_hash_contracts(self):
        cur,up=self.residual();self.assertEqual(b19.residual_errors(cur,up),[])
        for bad in(cur[:-1],cur+[cur[0]],cur[::-1]):self.assertTrue(b19.residual_errors(bad,up))
        for key in('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            cur,up=self.residual();cur[0][key]='wrong';self.assertTrue(b19.residual_errors(cur,up))
    def test_19_residual_owner_input_impact_action_exit_not_approval(self):
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            cur,up=self.residual();cur[0][key]=' ';self.assertTrue(b19.residual_errors(cur,up))
        for patch in({'disposition':'complete'},{'runtime_status':'passed'}):
            cur,up=self.residual();cur[0]|=patch;self.assertTrue(b19.residual_errors(cur,up))
    def test_20_R4c_bounded_and_six_C_unstarted_no_mutation(self):
        work,splits=self.work();before=copy.deepcopy(work);self.assertEqual(b19.remaining_work_errors(work,splits),[]);self.assertEqual(work,before)
        for i,key,value in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            work,splits=self.work();work[i][key]=value;self.assertTrue(b19.remaining_work_errors(work,splits))
    def test_21_split_requires_reason_scope_owner_input_action_exit(self):
        for key in('candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            work,splits=self.work();splits[0][key]=' ';self.assertTrue(b19.remaining_work_errors(work,splits))
        work,splits=self.work();splits[0]['status']='complete';self.assertTrue(b19.remaining_work_errors(work,splits))
    def test_22_strict_boolean_integer_metadata_and_erratum(self):
        self.assertEqual(b19.witness_metadata_errors(self.metadata()),[])
        for key,value in(('application_code_imported_or_executed',0),('erp_runtime_tests_executed',False),('phase7C_started',True),('phase8_authorized_or_started',None),('B_R4c_bounded_not_whole7B_closure',1),('illustration_count',14.0)):
            self.assertTrue(b19.witness_metadata_errors(self.metadata()|{key:value}))
        bad=self.metadata();bad['retained_additive_B10_arithmetic_erratum']['local_cost']=20;self.assertTrue(b19.witness_metadata_errors(bad))
    def test_23_lifecycle_manual_order_counterexample_NOT_WPF(self):
        self.assertTrue(after_lifecycle(navigate_before_loaded=True)['ISNew']);self.assertFalse(after_lifecycle(navigate_before_loaded=False)['ISNew'])
        self.assertEqual(after_lifecycle(navigate_before_loaded=True)['branch'],'session')
    def test_24_BaseQty_zero_qty_guard_skips_not_zeroing(self):
        self.assertEqual(production_qty_edit(D('8'),D('0'),D('1'),D('3')),D('8'))
        self.assertNotEqual(production_qty_edit(D('8'),D('0'),D('1'),D('3')),D('0'))
    def test_25_unit_branch_zero_vs_initialized_nonzero_and_old_factor_root(self):
        self.assertEqual(production_unit_edit(D('0'),D('12'),D('3')),D('0'))
        self.assertEqual(production_qty_edit(D('8'),D('2'),D('1'),D('3')),D('6'))
        self.assertEqual(production_unit_edit(D('2'),D('12'),D('3')),D('72'))
    def test_26_early_quantity_price_rounding_vs_unchanged_two_decimals(self):
        self.assertEqual(rehydrate_component(D('.004'),D('1000.004'))['quantity'],'0.00')
        self.assertEqual(rehydrate_component(D('2'),D('1.234'))['total'],'2.46')
        self.assertEqual(rehydrate_component(D('2'),D('1.25'))['total'],'2.50')
    def test_27_POS_date_existing_nonElectronic_and_counterexamples(self):
        old=datetime(2025,12,31,23,59);now=datetime(2026,1,2,12)
        for is_new,electronic,expected in((False,False,now),(False,True,old),(True,False,now),(True,True,now)):
            self.assertEqual(pos_save_date(old,now,is_new=is_new,electronic=electronic),expected)
        self.assertNotEqual(old.date(),pos_save_date(old,now,is_new=False,electronic=False).date())
    def test_28_bounded_CREATE_column_names_inert_not_SQL_parser(self):
        s='CREATE TABLE [dbo].[Inv](\n [id] int,\n [date] datetime,\n CONSTRAINT [PK] PRIMARY KEY([id]))'
        self.assertEqual(fields_from_create(s,'Inv'),['date','id'])
        with self.assertRaises(ValueError):fields_from_create(s,'SafesAdjust')
    def test_29_ACTUAL_current_B19_parser_B18_B17_B16_bases_API_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B16_CLI['default'],'B16');self.assertEqual(v.PHASE7_CURRENT_CLI['default'],'B17');self.assertEqual(v.PHASE7_B18_CLI['default'],'B18')
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B19')
        for part in('A','B15','B16','B17','B18','B19'):self.assertEqual(parser.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)
    def test_30_actual_entrypoint_and_B18_OWN_before_current_B19(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);s=ast.unparse(blocks[0]);self.assertIn('build_cli_parser().parse_args()',s);self.assertIn('main(args.through_phase, args.phase7_part)',s)
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser'];self.assertEqual(len(funcs),1);self.assertIn('PHASE7_LIVE_CLI',ast.unparse(funcs[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'))
        self.assertLess(body.index('validate_frozen_b18('),body.index('extend_navigation_contracts('));self.assertIn("phase7_part == 'B19'",body)
    def test_31_validator_facade_no_global_subprocess_Path_patch_restore(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel');f=self.fake();f.subprocess=backend;f.sys=SimpleNamespace(executable='python');view=b19.HistoricalB18ValidatorView(f)
        real_run=subprocess.run;path_read=Path.read_bytes;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertIs(subprocess.run,real_run);self.assertIs(Path.read_bytes,path_read);self.assertEqual(len(view.rows('findings.csv')),302);raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_32_redirect_ONLY_exact_protected_B18_argv_preserving_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k))or'sentinel');proxy=b19.HistoricalB18Subprocess(backend,'python',Path('/a/tools'))
        kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=30)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        unrelated=proxy.expected+['--different'];proxy.run(unrelated,**kwargs);self.assertEqual(calls[-1],((unrelated,),kwargs))
        proxy.run(['python','-B','/elsewhere/test_caller_request_audit_validator.py']);self.assertEqual(calls[-1][0][0][-1],'/elsewhere/test_caller_request_audit_validator.py')
    def test_33_historical_child_loads_ALL28_unmodified_no_skip_and_restores(self):
        p=Path(__file__).parent;source=(p/'run_historical_caller_request_tests_07B19.py').read_text();tree=ast.parse(source);s=ast.unparse(tree)
        self.assertIn('loadTestsFromModule(historical_tests)',s);self.assertIn('suite.countTestCases() != 28',s);self.assertIn('result.testsRun != 28 or result.skipped',s)
        self.assertIn('v.PHASE7_LIVE_CLI = original',s);self.assertNotIn('unittest.skip',s)
        prov=json.loads((p.parent/'evidence/provenance-07B19.json').read_text());old=p/'test_caller_request_audit_validator.py'
        self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/test_caller_request_audit_validator.py'])
    def test_34_documentary_sentinels_no_fabricated_source(self):
        errors,calls=[],[];fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b19.validate_source(fake,dict(id='FE7B19-17',evidence=b19.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b19.validate_source(fake,dict(id='UNKNOWN',evidence=b19.DOCUMENTARY),{});self.assertEqual(len(errors),1)
        b19.validate_source(fake,dict(id='FE7B19-01',evidence='a.cs:1-2'),{});self.assertEqual(len(calls),2)
        b19.validate_source(fake,dict(id='FE7B19-17',evidence='a.cs:1-2'),{});self.assertEqual(len(errors),2)
    def test_35_historical24_exact_order_raw_stdout_identity_null_not_guess(self):
        h=self.historical();self.assertEqual(b19.historical_record_errors(h),[])
        for patch in({'mode':'duplicate'},{'process_exit_code':1},{'stdout_sha256':'bad'},{'audit_checker_self_test_cases_reported':False},{'erp_runtime_tests_executed':False}):
            h=self.historical();h['historical_modes'][0]|=patch;self.assertTrue(b19.historical_record_errors(h))
        h=self.historical();h['historical_modes']=h['historical_modes'][:-1];self.assertTrue(b19.historical_record_errors(h))
        for patch in({'findings_total':307},{'registry_used':'findings.csv'},{'audit_checker_self_test_cases_reported':498}):
            h=self.historical();h['historical_modes'][-1]|=patch;self.assertTrue(b19.historical_record_errors(h))
        h=self.historical();h['historical_modes'][-1]['historical_B18_child']['all_original_cases_executed_unmodified']=False;self.assertTrue(b19.historical_record_errors(h))
        h=self.historical();h['historical_modes'][0]['audit_checker_self_test_cases_reported']=0;self.assertTrue(b19.historical_record_errors(h))
    def test_36_declared_scope_bookkeeping_is_not_body_or_percentage(self):
        A=Path(__file__).parents[1];d=json.loads((A/'evidence/scope-decision-07B19.json').read_text());b=d['bookkeeping']
        self.assertEqual((b['selected_paths'],b['prior_union'],b['overlap'],b['new'],b['union'],b['complement']),(23,408,21,2,410,417))
        self.assertEqual(sum(b['complement_kinds'].values()),417);self.assertEqual(d['selected_upstream_split'],'SP7B18-01')
        self.assertEqual((d['route_instances'],d['literal_Navigate_tokens'],d['parent_paths'],d['receiver_leaves']),(22,19,2,7))
        self.assertIs(d['phase7C_started'],False);self.assertIs(d['phase8_authorized_or_started'],False)
        self.assertEqual(d['source_review_state'],'selected-static-navigation-loader-save-boundary-slices-not-runtime-certified')


if __name__=='__main__':unittest.main()
