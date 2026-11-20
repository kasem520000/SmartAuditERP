#!/usr/bin/env python3
"""52 NEW B35 documentary cases,NOT32 operational acceptance plans or ERP.

All1190 prior cases including ALL52 B34 remain unmodified. Synthetic historical
schema fixtures are never evidence of40 real subprocesses. Zero registry edits.
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
import validate_linked_return_part as b35
from check_linked_return_witnesses import (
    fixture,linked_return,new_command,dirty_predicate,search_gate,select_by_item,
    token,flag,count,SOURCE_SLICES,EXPLORATORY_SLICES,
)
A=Path(__file__).resolve().parents[1]


class LinkedReturnAuditTests(unittest.TestCase):
    def old(self):
        return [dict(id=f'PX-{n:03d}',severity='Medium',certainty='potential',type='synthetic-only',status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for n in range(335)]
    def raw(self,rows):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\r\n');w.writeheader();w.writerows(rows);return s.getvalue().encode()
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def texts(self):return {n:'FROZEN:'+n for n in b35.SHARED_DOCS}
    def sources(self):
        raw=b'# fixture assertion dispatcher TEXT,NOT executed\n'
        return ({'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{n:03d}.py':'a'*64 for n in range(126)}),raw
    def context(self,f):return b35.historical_b34_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())
    def table(self,stem,part=35):
        with (A/'evidence'/f'{stem}-07B{part}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
    def groups(self,n):return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1,n+1))+'\n'
    def witness(self):return json.loads((A/'evidence/linked-return-witnesses-07B35.json').read_bytes())
    def kinds(self,s):return [e['kind'] for e in s['events']]
    def rows_fixture(self):return [dict(line='L-A',item='I-A',quantity=1,discount=0),dict(line='L-B',item='I-A',quantity=2,discount=1),dict(line='L-C',item='I-C',quantity=3,discount=0)]
    def history_fixture(self):
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B34.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B34-not-current-B35-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_messaging_request_tests_07B35.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=127,auxiliary_dispatcher_text_sha256=b35.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B34',findings_total=335,registry_used=b35.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1190,audit_checker_self_test_suite_count=35,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B34_child=child))
        return dict(historical_mode_count=40,historical_modes=modes,errors=[])

    def test_01_OWN335_raw336_readbytes_readtext_open(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            for mode in ('r','rt'):
                with (f.AUDIT/'findings.csv').open(mode,encoding='utf8',newline='') as s:self.assertEqual(list(csv.DictReader(s)),self.old())
            with (f.AUDIT/'findings.csv').open('rb') as s:self.assertEqual(s.read(),self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_reject_bad_rows_raw_indexes_sources_TEXT(self):
        old,raw,src=self.old(),self.raw(self.old()),self.sources()
        for args in ((old[:-1],self.texts(),raw,*src),(old,self.texts(),raw.replace(b'\r\n',b'\n'),*src),(old,self.texts(),b'\xef\xbb\xbf'+raw,*src),(old,self.texts(),bytearray(raw),*src),(old,{'README.md':'only'},raw,*src),(old,self.texts(),raw,{},src[1]),(old,self.texts(),raw,src[0],src[1]+b'x')):
            with self.assertRaises(ValueError):
                with b35.historical_b34_inputs(self.fake(),*args):pass
        old[0]['id']=old[1]['id']
        with self.assertRaises(ValueError):
            with b35.historical_b34_inputs(self.fake(),old,self.texts(),self.raw(old),*src):pass

    def test_03_nested_fresh_rows_and_exception_restore(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            p=f.AUDIT;changed=f.rows('findings.csv');changed[0]['title']='changed';self.assertEqual(f.rows('findings.csv'),self.old())
            with self.context(f):self.assertEqual(len(f.rows('findings.csv')),335)
            self.assertIs(f.AUDIT,p)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_04_readonly_canonical_local_Path_not_global(self):
        f=self.fake();methods=Path.read_bytes,Path.read_text,Path.open,Path.glob;src,raw=self.sources()
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertEqual(len(list((f.AUDIT/'tools').glob('*.py'))),127)
            p=f.AUDIT/'tools/validate_audit.py';self.assertEqual(p.read_bytes(),raw)
            with p.open('rb') as s:self.assertEqual(s.read(),raw)
            for mode in ('w','a','r+','wb'):
                with self.assertRaises(ValueError):p.open(mode)
            self.assertEqual(p.resolve(),Path('/synthetic/audit/tools/validate_audit.py'));self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())

    def test_05_exact_list_argv_proxy_not_shared_subprocess(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'ok')
        proxy=b35.HistoricalB34Subprocess(backend,'python',Path('/a/tools'));kw=dict(cwd='/a',timeout=60,capture_output=True,text=True)
        self.assertEqual(proxy.run(list(proxy.expected),**kw),'ok');self.assertEqual(calls[-1],((proxy.actual,),kw))
        for args in (tuple(proxy.expected),proxy.expected+['--other'],['python','-B','/other/test.py']):proxy.run(args,**kw);self.assertEqual(calls[-1],((args,),kw))
        f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b35.HistoricalB34ValidatorView(f);original=subprocess.run
        with self.context(view):self.assertIs(subprocess.run,original);self.assertIs(f.subprocess,backend)

    def test_06_ALL335_every_field_exact_no_append(self):
        old=self.old();self.assertEqual(b35.registry_preservation_errors(old,copy.deepcopy(old),self.raw(old),self.raw(old),[]),[])
        for n in (0,330,331,332,333,334):
            for key in old[n]:
                bad=copy.deepcopy(old);bad[n][key]='changed';self.assertTrue(b35.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]),(n,key))

    def test_07_ENTIRE_raw336_noBOM_CRLF_not_merely_prefix(self):
        old=self.old();raw=self.raw(old)
        for bad in (raw+b'\r\n',raw.replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+raw,raw[:-2],raw.replace(b'fixture-title',b'other',1)):self.assertTrue(b35.registry_preservation_errors(old,old,bad,raw,[]))

    def test_08_zero_new_roots_zero_evidence_extensions(self):
        old=self.old()
        for bad in (old[:-1],old+[old[-1]|dict(id='P7-164')],old[:-1]+[old[-1]|dict(id='P7-164')]):self.assertTrue(b35.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]))
        self.assertTrue(b35.registry_preservation_errors(old,old,self.raw(old),self.raw(old),[dict(finding_id='P7-160')]))

    def test_09_G256_exact_only257_to260(self):
        self.assertEqual(b35.group_row_errors(self.groups(256),self.groups(260)),[])
        for bad in (self.groups(259),self.groups(261),self.groups(260).replace('| G-01 | exact','| G-01 | changed'),self.groups(260).replace('G-256','G-255')):self.assertTrue(b35.group_row_errors(self.groups(256),bad))

    def test_10_documentary_sentinels_no_invented_source(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b35.validate_source(f,dict(id='FE7B35-14',evidence=b35.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b35.validate_source(f,dict(id='FE7B35-01',evidence=b35.DOCUMENTARY),{});self.assertTrue(errors)
        errors.clear();b35.validate_source(f,dict(id='FE7B35-14',evidence='a.cs:1-2'),{});self.assertTrue(errors)

    def test_11_LN8_NR8_exact_order_and_source_unions(self):
        ln,nr,fe=[self.table(n) for n in ('linked-navigation-lineage','nested-result-lineage','feature-implementation-matrix')];self.assertEqual(b35.ledger_errors(ln,nr,fe),[])
        for pool,index,key in ((ln,0,'source_to_output'),(nr,3,'evidence'),(ln,1,'finding_ids'),(nr,7,'feature_ids')):
            bad=copy.deepcopy(pool);bad[index][key]+=';changed';self.assertTrue(b35.ledger_errors(bad,nr,fe) if pool is ln else b35.ledger_errors(ln,bad,fe))
        self.assertTrue(b35.ledger_errors(ln[::-1],nr,fe))

    def test_12_lineage_owner_input_limits_and_nonexecution(self):
        ln,nr,fe=[self.table(n) for n in ('linked-navigation-lineage','nested-result-lineage','feature-implementation-matrix')]
        for pool in (ln,nr):
            for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','runtime_status'):
                bad=copy.deepcopy(pool);bad[0][key]='';self.assertTrue(b35.ledger_errors(bad,nr,fe) if pool is ln else b35.ledger_errors(ln,bad,fe))

    def test_13_FE16_INV16_T32_bidirectional_root_links(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b35.current_link_errors(*data),[])
        for i,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'invariant_ids'),(0,'finding_ids')):
            bad=copy.deepcopy(data);bad[i][0][key]='P7-164';self.assertTrue(b35.current_link_errors(*bad))

    def test_14_each_capability_owner_entry_source_output_exclusions(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')]
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim'):
            bad=copy.deepcopy(data);bad[0][0][key]='short';self.assertTrue(b35.current_link_errors(*bad),key)
        for key in ('procedure','acceptance_criterion'):
            bad=copy.deepcopy(data);bad[2][0][key]='short';self.assertTrue(b35.current_link_errors(*bad))

    def test_15_RS14_ancestry_SHA_contracts(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',34);self.assertEqual(b35.residual_errors(cur,old),[])
        for key in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(cur);bad[0][key]='changed';self.assertTrue(b35.residual_errors(bad,old))

    def test_16_full_old_inputs_mapped_routes_dispositions_retained(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',34)
        for key,value in (('required_redacted_input','new-short-input'),('current_handoff_or_split_ids','H7B35-06'),('disposition','accepted'),('runtime_status','passed')):
            bad=copy.deepcopy(cur);bad[2][key]=value;self.assertTrue(b35.residual_errors(bad,old))

    def test_17_SP3_input_prefix_and_future_not_started(self):
        cur,old=self.table('split-register'),self.table('split-register',34);self.assertEqual(b35.split_errors(cur,old),[])
        for key,value in (('upstream_row_sha256','changed'),('required_input','replacement'),('status','complete'),('owner_role','')):
            bad=copy.deepcopy(cur);bad[0][key]=value;self.assertTrue(b35.split_errors(bad,old))

    def test_18_fourB_sixC_workplan_BK_ancestry(self):
        rw=self.table('remaining-workplan');self.assertEqual(b35.remaining_work_errors(rw),[])
        for key,value in (('part_family','7C'),('status','complete'),('runtime_status','passed'),('counts_are_sessions_or_completion_percent','true')):
            bad=copy.deepcopy(rw);bad[3][key]=value;self.assertTrue(b35.remaining_work_errors(bad))
        bk=self.table('continuation-backlog');self.assertEqual(len(bk),10)
        for n,r in enumerate(bk,1):self.assertEqual((r['prior_backlog_id'],r['original_backlog_id']),(f'BK7B34-{n:02d}',f'BK7-{n:02d}'))
        self.assertEqual([r['status'] for r in bk[2:6]],['not-started']*4)

    def test_19_witness_metadata_strict_counts_bools_erratum(self):
        w=self.witness();self.assertEqual(b35.witness_metadata_errors(w),[])
        for key,value in (('illustration_count',True),('erp_runtime_tests_executed',False),('stop_before_CalcRows_and_bindings',1),('save_or_number_reservation_or_financial_loss_proved',0),('new_root_ids',['P7-164'])):self.assertTrue(b35.witness_metadata_errors(w|{key:value}))
        bad=copy.deepcopy(w);bad['retained_additive_B10_arithmetic_erratum']['local_cost']=True;self.assertTrue(b35.witness_metadata_errors(bad))

    def test_20_witness_actual_subprocess_recomputes_exact_bytes(self):
        r=subprocess.run([sys.executable,'-B',str(A/'tools/check_linked_return_witnesses.py')],cwd=A.parents[1],capture_output=True,timeout=30)
        self.assertEqual((r.returncode,r.stderr),(0,b''));self.assertEqual(r.stdout,(A/'evidence/linked-return-witnesses-07B35.json').read_bytes())

    def test_21_sale_preclear_before_any_picker_result(self):
        s=fixture(search_done=False,gid='-1');self.assertEqual(s['clear_calls'],1);k=self.kinds(s)
        self.assertLess(k.index('parent-new-assignment-and-completed-reset'),k.index('helper-entered'));self.assertFalse(s['search_gate_passed']);self.assertEqual(s['parent_note'],'')

    def test_22_purchase_No_in_void_new_does_not_stop_caller(self):
        s=fixture('purchase');self.assertTrue(s['events'][0]['guard_asked']);self.assertTrue(s['events'][0]['guard_blocks']);self.assertEqual(s['clear_calls'],1)
        self.assertIn('helper-entered',self.kinds(s));self.assertEqual(s['parent_value'],'source-B')

    def test_23_direct_new_No_control_and_Yes_two_clears(self):
        d=new_command('purchase',updated=True,is_new=False,item_count=2,answer='No');self.assertEqual((d['guard_blocks'],d['clear_calls'],d['current_value']),(True,0,'draft-A'))
        self.assertEqual(fixture('purchase',answer='Yes')['clear_calls'],2);self.assertFalse(d['returns_typed_abandon_decision'])

    def test_24_search_gate_rejects_only_bind_not_parent_tail(self):
        for done,gid in ((False,'DOC-B'),(False,'-1'),(True,'-1')):
            s=fixture(search_done=done,gid=gid);self.assertFalse(s['search_gate_passed']);self.assertIn('parent-conversion-prefix',self.kinds(s))
        self.assertTrue(search_gate(True,''));self.assertTrue(search_gate(True,'DOC-B'))

    def test_25_child_cancel_resets_child_field_not_parent_ref(self):
        s=fixture();self.assertEqual((s['parent_value'],s['child_value'],s['item_done']),('source-B','child-reset-value',False))
        k=self.kinds(s);self.assertLess(k.index('BindingInvoice-ref-boundary-before-item-result'),k.index('CloseWithoutResult-replaces-child-field-not-parent-ref'))
        self.assertNotIn('final-ref-assignment-gated-by-item-done',k);self.assertFalse(next(e for e in s['events'] if e['kind']=='child-field-assigned-from-ref-value')['CLR_aliasing_proved'])

    def test_26_insert_all_explicit_acceptance_control(self):
        s=fixture(item_action='all');self.assertTrue(s['item_done']);self.assertIn('final-ref-assignment-gated-by-item-done',self.kinds(s));self.assertNotIn('CloseWithoutResult-replaces-child-field-not-parent-ref',self.kinds(s))

    def test_27_no_selection_stays_open_then_separate_close(self):
        z=select_by_item(self.rows_fixture(),[]);self.assertEqual((z['done'],z['closed']),(False,False));self.assertEqual(z['rows'],self.rows_fixture())
        s=fixture(item_action='empty-then-close');self.assertFalse(s['item_done']);self.assertIn('empty-selection-returns-without-close-or-accept',self.kinds(s))

    def test_28_existing_ItemId013_retains_both_distinct_lines(self):
        s=select_by_item(self.rows_fixture(),[dict(item='I-A',quantity=7,discount=2)]);self.assertTrue(s['done'])
        self.assertEqual([r['line'] for r in s['rows']],['L-A','L-B']);self.assertEqual({r['quantity'] for r in s['rows']},{7});self.assertEqual({r['discount'] for r in s['rows']},{2})

    def test_29_repeated_ItemId_selection_last_writer_not_new_root(self):
        s=select_by_item(self.rows_fixture(),[dict(item='I-A',quantity=7,discount=2),dict(item='I-A',quantity=4,discount=1)])
        self.assertEqual({r['quantity'] for r in s['rows']},{4});self.assertEqual({r['discount'] for r in s['rows']},{1})

    def test_30_single_line_control_and_model_copies_not_DTO_alias(self):
        rows=self.rows_fixture();before=copy.deepcopy(rows);s=select_by_item(rows,[dict(item='I-C',quantity=5,discount=0)])
        self.assertEqual(rows,before);self.assertEqual(s['rows'],[dict(line='L-C',item='I-C',quantity=5,discount=0)]);self.assertIsNot(s['rows'][0],rows[2])

    def test_31_first_dialog_nonreturn_blocks_parent_tail_not_preclear(self):
        s=fixture(search_returns=False);self.assertEqual(s['terminal'],'search-dialog-nonreturn-supplied');self.assertEqual(s['clear_calls'],1)
        self.assertNotIn('parent-conversion-prefix',self.kinds(s));self.assertNotIn('BindingInvoice-ref-boundary-before-item-result',self.kinds(s))

    def test_32_item_dialog_nonreturn_has_bound_state_no_parent_tail(self):
        s=fixture(items_return=False);self.assertEqual((s['terminal'],s['parent_value']),('item-dialog-nonreturn-supplied','source-B'));self.assertNotIn('parent-conversion-prefix',self.kinds(s))

    def test_33_null_ref_boundary_is_not_successful_conversion(self):
        for editor in ('sale','purchase'):
            s=fixture(editor,reader='null');self.assertIsNone(s['parent_value']);self.assertEqual(s['terminal'],'parent-null-access-boundary-not-success')
            self.assertNotIn('parent-conversion-prefix',self.kinds(s));self.assertIn('helper-catch-after-null-access-no-typed-failure',self.kinds(s))

    def test_34_supplied_partial_nonnull_not_complete_hydration(self):
        s=fixture(reader='partial');self.assertEqual(s['parent_value'],'partial-B');self.assertIn('parent-conversion-prefix',self.kinds(s));self.assertTrue(s['is_new'])
        self.assertFalse(self.witness()['actual_dialog_gesture_or_reference_aliasing_or_complete_hydration_proved'])

    def test_35_helper_catch_before_or_after_bind_returns_no_typed_failure(self):
        before=fixture(helper_fault='before-search-result');after=fixture(helper_fault='after-bind')
        self.assertEqual((before['parent_value'],after['parent_value']),('reset-value','source-B'));self.assertIsNone(after['child_value'])
        for s in (before,after):self.assertIn('parent-conversion-prefix',self.kinds(s));self.assertFalse(s['item_done'])

    def test_36_number_failure_has_distinct_sale_purchase_reference_order(self):
        sale,purch=fixture(number_returns=False),fixture('purchase',number_returns=False)
        self.assertEqual(sale['reference'],'COMBINED-B');self.assertEqual(purch['reference'],'-1')
        self.assertIn('sale-reference-before-number',self.kinds(sale));self.assertNotIn('purchase-reference-after-number',self.kinds(purch))
        for s in (sale,purch):self.assertEqual(s['parent_note'],'');self.assertNotIn('parent-ISNew-written-after-untyped-return',self.kinds(s))
        self.assertEqual((fixture()['reference'],fixture('purchase')['reference']),('COMBINED-B','DOC-B'))

    def test_37_sale_discount_nonreturn_stops_before_ISNew_and_bindings(self):
        s=fixture(discount_returns=False);self.assertEqual(s['terminal'],'discount-nonreturn-before-ISNew-tail');self.assertFalse(s['is_new']);self.assertNotIn('parent-ISNew-written-after-untyped-return',self.kinds(s))
        self.assertEqual(fixture()['terminal'],'before-CalcRows-and-bindings-not-stable-UI-state')

    def test_38_guard_count_thresholds_clean_not_SaveResult(self):
        for c in (0,1,2):
            self.assertEqual(dirty_predicate('sale',updated=False,is_new=True,item_count=c),c>1)
            self.assertEqual(dirty_predicate('purchase',updated=False,is_new=True,item_count=c),c>0)
        s=fixture('purchase',updated=False,is_new=False,item_count=0,search_done=False,gid='-1');self.assertFalse(s['events'][0]['guard_asked']);self.assertEqual(s['clear_calls'],2)

    def test_39_strict_bools_counts_tokens_without_short_circuit_loopholes(self):
        for value in (None,1,'','x'*81,'x\n','/real/file','+966555'):
            with self.assertRaises(ValueError):token(value)
        for value in (True,False,-1,65,1.0,'1'):
            with self.assertRaises(ValueError):count(value)
        for value in (0,1,None,'true'):
            with self.assertRaises(ValueError):flag(value)
        for kw in (dict(updated=True,is_new=0,item_count=2),dict(updated=True,is_new=False,item_count=True)):
            with self.assertRaises(ValueError):dirty_predicate('sale',**kw)
        for kw in (dict(search_returns=1),dict(items_return=0),dict(number_returns=1),dict(discount_returns=0)):
            with self.assertRaises(ValueError):fixture(**kw)

    def test_40_excluded_branches_aliasing_and_runtime_not_silently_inferred(self):
        with self.assertRaises(ValueError):fixture('contract')
        for kw in (dict(reader='guaranteed-complete'),dict(item_action='X-means-null'),dict(helper_fault='all-catches')):
            with self.assertRaises(ValueError):fixture(**kw)
        with self.assertRaises(TypeError):fixture(previous_year=True)
        w=self.witness();self.assertTrue(w['dirty_normal_returns_reader_snapshots_and_failures_are_supplied']);self.assertTrue(w['stop_before_CalcRows_and_bindings'])
        self.assertFalse(w['save_or_number_reservation_or_financial_loss_proved']);self.assertEqual(w['new_root_ids'],[])

    def test_41_ACTUAL_LIVE35_versioned34_API15_parser(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B34_CLI['default'],'B34');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B35')
        p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B35')
        for part in ('A',)+tuple(f'B{n}' for n in range(1,36)):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        for n in range(18,35):self.assertEqual(getattr(v,f'PHASE7_B{n}_CLI')['default'],f'B{n}')

    def test_42_ACTUAL_19_AST_gates_B34_history_before_current(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());raw=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(raw).hexdigest(),b35.DISPATCHER_SHA)
        tree=ast.parse(raw);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main)
        self.assertLess(body.index('historical_b33_validation('),body.index('historical_b34_validation('));self.assertLess(body.index('historical_b34_validation('),body.index('extend_linked_return('));self.assertIn('extend_messaging_request(historical_b34,',body)
        actual=[set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part']
        expected=[{f'B{i}' for i in range(first,36)} for first in range(1,20)];self.assertEqual(actual,expected)
        for n in range(19):
            bad=copy.deepcopy(actual);bad[n].remove('B35')
            with self.assertRaises(AssertionError):self.assertEqual(bad,expected)
        block=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'");self.assertIn('build_cli_parser().parse_args()',ast.unparse(block))

    def test_43_ALL52_launcher_local_restore_no_old_dispatcher_code(self):
        src=ast.unparse(ast.parse((A/'tools/run_historical_messaging_request_tests_07B35.py').read_text()))
        for text in ('suite.countTestCases() != 52','run.testsRun != 52 or run.skipped','loadTestsFromModule(historical_tests)','historical_tests.A = v.AUDIT','historical_tests.Path = type(v.AUDIT)','historical_tests.A = original_a','historical_tests.Path = original_path','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B34_CLI','b35.historical_b34_inputs('):self.assertIn(text,src)
        for text in ('unittest.skip','v.__file__ =','Path.read_bytes =','Path.open =','exec('):self.assertNotIn(text,src)

    def test_44_historical127_assertions_distinct_from_current131(self):
        prov=json.loads((A/'evidence/provenance-07B35.json').read_bytes());self.assertEqual(len(prov['historical_checker_sources_at_entry']),127);self.assertEqual(len(list((A/'tools').glob('*.py'))),131)
        raw=(A/b35.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));texts=json.loads((A/b35.SHARED_SNAPSHOT).read_bytes())['files'];before=v.AUDIT,v.read,v.rows;code,file=v.main.__code__,v.__file__;methods=Path.read_bytes,Path.read_text,Path.open,Path.glob
        with b35.historical_b34_inputs(v,old,texts,raw,prov['historical_checker_sources_at_entry'],(A/b35.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT/'tools').glob('*.py'))),127);self.assertEqual(hashlib.sha256(type(v.AUDIT)(v.__file__).read_bytes()).hexdigest(),b35.DISPATCHER_SHA)
            with (v.AUDIT/'findings.csv').open(newline='') as f:self.assertEqual(list(csv.DictReader(f)),old)
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
        self.assertTrue(all(x is y for x,y in zip(before,(v.AUDIT,v.read,v.rows))))

    def test_45_protected1071_INCLUDES_registry_ALL335_raw336_potentials(self):
        prov=json.loads((A/'evidence/provenance-07B35.json').read_bytes());h=prov['historical_artifact_sha256'];self.assertEqual(len(h),1071);self.assertEqual(h['findings.csv'],b35.SNAPSHOT_SHA)
        self.assertNotIn('findings.csv',prov['declared_mutable_entry_paths']);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==s for n,s in h.items()))
        raw=(A/b35.SNAPSHOT).read_bytes();current=(A/'findings.csv').read_bytes();self.assertEqual(raw,current);rows=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        self.assertEqual(b35.registry_preservation_errors(rows,rows,current,raw,self.table('historical-extensions')),[])
        for root in ('P4-014','P7-108','P7-132','P7-145'):self.assertEqual(next(r for r in rows if r['id']==root)['certainty'],'potential')

    def test_46_scope7_overlap6_union428_24contract11context_dedup15(self):
        d=json.loads((A/'evidence/scope-decision-07B35.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(7,427,6,1,428,399))
        self.assertEqual((d['historical_metadata_screen_count'],d['parent_path_matched_metadata_rows'],d['selected_prior_report_sections'],d['selected_contract_slices'],d['exploratory_context_slices']),(335,83,15,24,11));self.assertFalse(d['all_historical_bodies_reviewed'])
        w=self.witness();self.assertEqual(w['whole_local_files_selected'],0)
        for key,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('exploratory_source_reads_not_capability_certification',EXPLORATORY_SLICES)):
            self.assertEqual(tuple((r['path'],r['start'],r['end']) for r in w[key]),declared)
            for r in w[key]:self.assertFalse(r['whole_local_file_selected']);self.assertEqual(hashlib.sha256((A.parents[1]/r['path']).read_bytes()).hexdigest(),r['sha256'])
        screen=json.loads((A/'evidence/dedup-screen-07B35.json').read_bytes());rows=list(csv.DictReader(io.StringIO((A/b35.SNAPSHOT).read_text(),newline='')));self.assertEqual(b35.dedup_errors(screen,rows),[])
        for key,value in (('all_historical_bodies_reviewed',True),('new_root_ids',['P7-164']),('selected_prior_finding_sections',[])):self.assertTrue(b35.dedup_errors(screen|{key:value},rows))

    def test_47_no164_no_registry_tail_no_implicit_certainty_transfer(self):
        ad=self.table('root-adjudication');self.assertFalse(any(r['decision'] in ('new-local-root','extended-existing-root-not-new') for r in ad));self.assertEqual(self.table('historical-extensions'),[])
        self.assertEqual([r['current_root_ids'] for r in ad[:3]],['P7-159','P7-160','P4-013']);self.assertTrue(all(r['comparison_depth']==b35.DEDUP_DEPTH for r in ad))
        with (A/'findings.csv').open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),335);self.assertEqual(rows[-1]['id'],'P7-163');self.assertNotIn('P7-164',{r['id'] for r in rows})
        self.assertEqual((A/'findings.csv').read_bytes(),(A/b35.SNAPSHOT).read_bytes())

    def test_48_all_inputs_two_distinct_not_executed_plans_per_FE(self):
        self.assertEqual(b35.residual_errors(self.table('residual-disposition'),self.table('residual-disposition',34)),[]);self.assertEqual(b35.split_errors(self.table('split-register'),self.table('split-register',34)),[])
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b35.current_link_errors(*data),[])
        for f in data[0]:
            linked=[t for t in data[2] if t['feature_ids']==f['id']];self.assertEqual(len(linked),2);self.assertNotEqual(linked[0]['acceptance_criterion'],linked[1]['acceptance_criterion'])
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertIn('إذن',t['prerequisites']);self.assertIn('not-executed',t['safety_controls'])
        for stem in ('handoffs','questions'):
            for old,new in zip(self.table(stem,34),self.table(stem)):self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))

    def test_49_reference16_rawclock_B34_capture_dea_delivery_e6f_separate(self):
        prov=json.loads((A/'evidence/provenance-07B35.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B35.md').read_text();self.assertEqual(b35.date_identity_errors(prov,note),[])
        self.assertTrue(b35.date_identity_errors(prov|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b35.date_identity_errors(prov,note.replace(b35.B34_CHECK_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B34.json').read_bytes());self.assertEqual(old['checkout_head'],'dea2244267d74dd540af59c6e63b0f4362ab8c1c');self.assertNotEqual(old['checkout_head'],b35.ENTRY)

    def test_50_synthetic40_schema_fixture_NOT_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b35.historical_record_errors(h),[])
        for key,value in (('registry_used','findings.csv'),('findings_total',336),('process_exit_code',True),('audit_checker_self_test_cases_reported',1242),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=value;self.assertTrue(b35.historical_record_errors(bad))
        for key,value in (('tests_reported',51),('historical_source_assertion_input_count',131),('test_module_Path_and_A_are_historical_assertion_inputs_only',1),('auxiliary_dispatcher_text_sha256','b'*64)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B34_child'][key]=value;self.assertTrue(b35.historical_record_errors(bad))
        self.assertTrue(b35.historical_record_errors(h|dict(historical_mode_count=True)))

    def test_51_ACTUAL40_archive131_single_inverse_pin_proof(self):
        p=A/'evidence/historical-mode-verification-07B35.json';raw=p.read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b35.HISTORICAL_RUN_SHA);self.assertEqual(b35.historical_record_errors(h),[])
        self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b35.ENTRY,v.HEAD,v.BRANCH));sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),131);self.assertEqual(b35.capture_source_errors(h,sources),[])
        for key in ('tools/validate_linked_return_part.py','tools/test_linked_return_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[key]+=b'\n';self.assertTrue(b35.capture_source_errors(h,changed))
        self.assertTrue(b35.capture_source_errors(h,{}));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']))
        self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        proof=json.loads((A/'evidence/capture-time-identity-07B35.json').read_bytes());self.assertEqual((proof['archive_bytes'],proof['archive_sha256'],proof['capture_tool_set_count'],proof['unchanged_capture_tool_count'],proof['raw_stdout_identities_temporarily_rechecked']),(len(raw),b35.HISTORICAL_RUN_SHA,131,130,40));self.assertTrue(proof['exact_inverse_reconstructs_capture_time_bytes']);self.assertFalse(proof['wholesale40_replayed_after_pin'])

    def test_52_actual131_AST_stdlib_and_protected_B34_records(self):
        tools=list((A/'tools').glob('*.py'));self.assertEqual(len(tools),131)
        for p in tools:ast.parse(p.read_text(),filename=str(p))
        tree=ast.parse((A/'tools/check_linked_return_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','hashlib','json','pathlib'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        h=json.loads((A/'evidence/provenance-07B35.json').read_bytes())['historical_artifact_sha256']
        for name in ('findings.csv','evidence/checks-07B34.json','evidence/official-capture-receipt-07B34.json','evidence/historical-mode-verification-07B34.json','evidence/capture-time-identity-07B34.json','evidence/messaging-request-witnesses-07B34.json','tools/test_messaging_request_audit_validator.py','tools/run_historical_output_route_tests_07B34.py','DATE-IDENTITY-NOTE-07B34.md'):
            self.assertIn(name,h);self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),h[name])
        for n in ('witness-precheck-note-07B35.json','witness-precheck-note02-07B35.json'):
            note=json.loads((A/'evidence'/n).read_bytes());self.assertEqual(note['process_exit_code'],1);self.assertFalse(note['application_source_or_protected_artifacts_changed']);self.assertFalse(note['validator_or_historical_tests_relaxed'])


if __name__=='__main__':unittest.main()
