#!/usr/bin/env python3
"""52 NEW B37 documentary cases,NOT32 operational plans or ERP acceptance.

ALL1294 prior cases unchanged. Synthetic42 fixture is schema data,not proof of
actual historical subprocesses. LIVE37/139 execution tools independent from
child-local historical135 assertions/exact dispatcher TEXT for OWN B36.
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
import validate_transfer_picker_part as b37
from check_transfer_picker_witnesses import header,checked_header,request,command,abandon_guard,ROUTES,NUMBER_BOUNDARIES,SOURCE_SLICES,CONTEXT_SLICES,WHOLE_REREADS
from check_invoice_picker_witnesses import flag,number,token
A=Path(__file__).resolve().parents[1]


class TransferPickerAuditTests(unittest.TestCase):
    def old(self):return [dict(id=f'PX-{n:03d}',severity='Medium',certainty='potential',type='synthetic-only',status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for n in range(335)]

    def raw(self,rows):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\r\n');w.writeheader();w.writerows(rows);return s.getvalue().encode()

    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])

    def texts(self):return {n:'FROZEN:'+n for n in b37.SHARED_DOCS}

    def sources(self):
        raw=b'# synthetic historical dispatcher assertion TEXT,NOT executed\n'
        return ({'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{n:03d}.py':'a'*64 for n in range(134)}),raw

    def context(self,f):return b37.historical_b36_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())

    def table(self,stem,part=37):
        with (A/'evidence'/f'{stem}-07B{part}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

    def groups(self,n):return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1,n+1))+'\n'

    def witness(self):return json.loads((A/'evidence/transfer-picker-witnesses-07B37.json').read_bytes())

    def history_fixture(self):
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B36.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B36-not-current-B37-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_invoice_picker_tests_07B37.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=135,auxiliary_dispatcher_text_sha256=b37.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B36',findings_total=335,registry_used=b37.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1294,audit_checker_self_test_suite_count=37,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B36_child=child))
        return dict(historical_mode_count=42,historical_modes=modes,errors=[])

    def test_01_OWN335_raw336_readbytes_text_open(self):
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
                with b37.historical_b36_inputs(self.fake(),*args):pass
        old[0]['id']=old[1]['id']
        with self.assertRaises(ValueError):
            with b37.historical_b36_inputs(self.fake(),old,self.texts(),self.raw(old),*src):pass

    def test_03_nested_rows_and_exception_restore(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            p=f.AUDIT;r=f.rows('findings.csv');r[0]['title']='changed';self.assertEqual(f.rows('findings.csv'),self.old())
            with self.context(f):self.assertEqual(len(f.rows('findings.csv')),335)
            self.assertIs(f.AUDIT,p)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_04_readonly_canonical_local_Path_not_global(self):
        f=self.fake();methods=Path.read_bytes,Path.read_text,Path.open,Path.glob;src,raw=self.sources()
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertEqual(len(list((f.AUDIT/'tools').glob('*.py'))),135)
            p=f.AUDIT/'tools/validate_audit.py';self.assertEqual(p.read_bytes(),raw)
            with p.open('rb') as s:self.assertEqual(s.read(),raw)
            for mode in ('w','a','r+','wb'):
                with self.assertRaises(ValueError):p.open(mode)
            self.assertEqual(p.resolve(),Path('/synthetic/audit/tools/validate_audit.py'));self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())

    def test_05_exact_list_argv_proxy_no_shared_subprocess(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'ok');proxy=b37.HistoricalB36Subprocess(backend,'python',Path('/a/tools'));kw=dict(cwd='/a',timeout=60,capture_output=True,text=True)
        self.assertEqual(proxy.run(list(proxy.expected),**kw),'ok');self.assertEqual(calls[-1],((proxy.actual,),kw))
        for args in (tuple(proxy.expected),proxy.expected+['--other'],['python','-B','/other/test.py']):proxy.run(args,**kw);self.assertEqual(calls[-1],((args,),kw))
        f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b37.HistoricalB36ValidatorView(f);original=subprocess.run
        with self.context(view):self.assertIs(subprocess.run,original);self.assertIs(f.subprocess,backend)

    def test_06_ALL335_every_field_exact(self):
        old=self.old();self.assertEqual(b37.registry_preservation_errors(old,copy.deepcopy(old),self.raw(old),self.raw(old),[]),[])
        for n in (0,330,331,332,333,334):
            for k in old[n]:
                bad=copy.deepcopy(old);bad[n][k]='changed';self.assertTrue(b37.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]),(n,k))

    def test_07_entire_raw336_not_prefix_CRLF_noBOM(self):
        old=self.old();raw=self.raw(old)
        for bad in (raw+b'\r\n',raw.replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+raw,raw[:-2],raw.replace(b'fixture-title',b'other',1)):self.assertTrue(b37.registry_preservation_errors(old,old,bad,raw,[]))

    def test_08_zero_new_roots_and_extensions(self):
        old=self.old()
        for bad in (old[:-1],old+[old[-1]|dict(id='P7-164')],old[:-1]+[old[-1]|dict(id='P7-164')]):self.assertTrue(b37.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]))
        self.assertTrue(b37.registry_preservation_errors(old,old,self.raw(old),self.raw(old),[dict(finding_id='P7-157')]))

    def test_09_G264_exact_only265_to268(self):
        self.assertEqual(b37.group_row_errors(self.groups(264),self.groups(268)),[])
        for bad in (self.groups(267),self.groups(269),self.groups(268).replace('| G-01 | exact','| G-01 | changed'),self.groups(268).replace('G-264','G-263')):self.assertTrue(b37.group_row_errors(self.groups(264),bad))

    def test_10_documentary_sentinels_no_fake_source(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b37.validate_source(f,dict(id='FE7B37-15',evidence=b37.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b37.validate_source(f,dict(id='FE7B37-01',evidence=b37.DOCUMENTARY),{});self.assertTrue(errors)
        errors.clear();b37.validate_source(f,dict(id='FE7B37-15',evidence='a.cs:1-2'),{});self.assertTrue(errors)

    def test_11_TR8_TT8_ordered_exact_unions(self):
        pq,pr,fe=[self.table(n) for n in ('transfer-request-lineage','transfer-tail-lineage','feature-implementation-matrix')];self.assertEqual(b37.ledger_errors(pq,pr,fe),[])
        for pool,index,k in ((pq,0,'source_to_output'),(pr,3,'evidence'),(pq,1,'finding_ids'),(pr,7,'feature_ids')):
            bad=copy.deepcopy(pool);bad[index][k]+=';changed';self.assertTrue(b37.ledger_errors(bad,pr,fe) if pool is pq else b37.ledger_errors(pq,bad,fe))
        self.assertTrue(b37.ledger_errors(pq[::-1],pr,fe))

    def test_12_lineage_owner_inputs_and_limits(self):
        pq,pr,fe=[self.table(n) for n in ('transfer-request-lineage','transfer-tail-lineage','feature-implementation-matrix')]
        for pool in (pq,pr):
            for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','runtime_status'):
                bad=copy.deepcopy(pool);bad[0][k]='';self.assertTrue(b37.ledger_errors(bad,pr,fe) if pool is pq else b37.ledger_errors(pq,bad,fe))

    def test_13_FE16_INV16_T32_bidirectional_links(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b37.current_link_errors(*data),[])
        for i,k in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'invariant_ids'),(0,'finding_ids')):
            bad=copy.deepcopy(data);bad[i][0][k]='P7-164';self.assertTrue(b37.current_link_errors(*bad))

    def test_14_each_capability_entry_source_output_owner_exit(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')]
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim','static_exit_criterion'):
            bad=copy.deepcopy(data);bad[0][0][k]='short';self.assertTrue(b37.current_link_errors(*bad),k)
        for k in ('procedure','acceptance_criterion','owner_role'):
            bad=copy.deepcopy(data);bad[2][0][k]='short';self.assertTrue(b37.current_link_errors(*bad))

    def test_15_RS14_ancestry_hash_contracts(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',36);self.assertEqual(b37.residual_errors(cur,old),[])
        for k in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(cur);bad[0][k]='changed';self.assertTrue(b37.residual_errors(bad,old))

    def test_16_full_input_mapped_routes_dispositions(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',36)
        for k,val in (('required_redacted_input','new-short-input'),('current_handoff_or_split_ids','H7B37-06'),('disposition','accepted'),('runtime_status','passed')):
            bad=copy.deepcopy(cur);bad[2][k]=val;self.assertTrue(b37.residual_errors(bad,old))

    def test_17_SP3_full_input_and_future_not_started(self):
        cur,old=self.table('split-register'),self.table('split-register',36);self.assertEqual(b37.split_errors(cur,old),[])
        for k,val in (('upstream_row_sha256','changed'),('required_input','replacement'),('status','complete'),('owner_role','')):
            bad=copy.deepcopy(cur);bad[0][k]=val;self.assertTrue(b37.split_errors(bad,old))

    def test_18_fourB_sixC_work_and_backlog_ancestry(self):
        rw=self.table('remaining-workplan');self.assertEqual(b37.remaining_work_errors(rw),[])
        for k,val in (('part_family','7C'),('status','complete'),('runtime_status','passed'),('counts_are_sessions_or_completion_percent','true')):
            bad=copy.deepcopy(rw);bad[3][k]=val;self.assertTrue(b37.remaining_work_errors(bad))
        for n,(old,new) in enumerate(zip(self.table('continuation-backlog',36),self.table('continuation-backlog')),1):
            self.assertEqual((new['prior_backlog_id'],new['original_backlog_id']),(f'BK7B36-{n:02d}',f'BK7-{n:02d}'));self.assertTrue(new['required_work'].startswith(old['required_work']));self.assertEqual(new['status'],old['status'])

    def test_19_witness_strict_counts_flags_and_erratum(self):
        w=self.witness();self.assertEqual(b37.witness_metadata_errors(w),[])
        for k,val in (('illustration_count',True),('erp_runtime_tests_executed',False),('modal_header_field_number_and_failure_values_supplied',1),('real_query_or_conversion_failures_executed',0),('whole_local_source_bodies_reread',1),('new_root_ids',['P7-164'])):self.assertTrue(b37.witness_metadata_errors(w|{k:val}))
        bad=copy.deepcopy(w);bad['retained_additive_B10_arithmetic_erratum']['local_cost']=True;self.assertTrue(b37.witness_metadata_errors(bad))

    def test_20_witness_actual_subprocess_exact_bytes(self):
        r=subprocess.run([sys.executable,'-B',str(A/'tools/check_transfer_picker_witnesses.py')],cwd=A.parents[1],capture_output=True,timeout=30);self.assertEqual((r.returncode,r.stderr),(0,b''));self.assertEqual(r.stdout,(A/'evidence/transfer-picker-witnesses-07B37.json').read_bytes())

    def test_21_four_command_specific_requests(self):
        self.assertEqual([(request(r)['proc'],request(r)['inv_type']) for r in ROUTES],[(2,8),(1,8),(1,14),(1,1)])
        self.assertFalse(request('search')['local_proc_disable_instruction_present']);self.assertTrue(all(request(r)['local_proc_disable_instruction_present'] for r in ROUTES[1:]))
        self.assertEqual(request('receive')['mandatory_status_predicate'],'InvoiceStatus-equals-1');self.assertEqual(request('order')['mandatory_status_predicate'],'none')

    def test_22_search_nonaccept_no_tail_control(self):
        for done,gid in ((False,'-1'),(False,'doc-B'),(True,'-1')):
            s=command('search',header(),done=done,gid=gid);self.assertFalse(s['navigate_requested']);self.assertEqual(s['header'],s['before']['header']);self.assertIsNone(s['number_request'])

    def test_23_receive_nonaccept_writes_operation_and_label(self):
        s=command('receive',header());self.assertFalse(s['navigate_requested']);self.assertEqual((s['header']['proc'],s['field_proc'],s['label']),(1,1,'visible'));self.assertEqual(s['number_request']['proc_type'],1);self.assertFalse(s['new_flag_tail_reached'])
        self.assertLess(s['events'].index('header-ProcType-written-1'),s['events'].index('field-ProcType-written-1'));self.assertLess(s['events'].index('field-ProcType-written-1'),s['events'].index('LoadInvoiceNumber-called-using-editor-fields'))

    def test_24_order_nonaccept_conversion_tail(self):
        s=command('order',header());self.assertFalse(s['navigate_requested']);self.assertEqual((s['header']['kind'],s['header']['proc'],s['header']['is_new']),('SafesTransferTo',2,True));self.assertEqual(s['field_proc'],2)

    def test_25_purchase_nonaccept_same_mechanism_not_new_root(self):
        s=command('purchase',header());self.assertEqual(s['header'],command('order',header())['header']);self.assertTrue(s['new_flag_tail_reached']);self.assertEqual(s['request']['inv_type'],1);self.assertEqual(self.witness()['new_root_ids'],[])

    def test_26_false_or_sentinel_skip_Navigate_only(self):
        for route in ROUTES[1:]:
            for done,gid in ((False,'-1'),(False,'doc-B'),(True,'-1')):
                s=command(route,header(),done=done,gid=gid);self.assertFalse(s['navigate_requested']);self.assertIsNotNone(s['number_request'])

    def test_27_empty_gid_only_sentinel_gate_not_DocumentRef_validation(self):
        for route in ROUTES:
            s=command(route,header(),done=True,gid='');self.assertTrue(s['navigate_requested']);self.assertFalse(s['typed_load_success_proved'])

    def test_28_modal_nonreturn_and_exception_boundaries(self):
        for route in ROUTES:
            for modal in ('not-returned','throws-before-return'):
                s=command(route,header(),modal=modal,done=True,gid='doc-B');self.assertEqual(s['header'],s['before']['header']);self.assertIsNone(s['number_request']);self.assertFalse(s['navigate_requested'])

    def test_29_clean_and_dirty_are_supplied_not_guard_calls(self):
        for dirty in (False,True):
            s=command('order',header(),dirty=dirty);self.assertTrue(s['new_flag_tail_reached']);self.assertFalse(s['check_before_clear_called']);self.assertEqual(s['dirty_supplied'],dirty)

    def test_30_accepted_target_not_abandon_decision_with_supplied_output(self):
        h=header(slot='head-B',gid='doc-B');s=command('receive',header(),dirty=True,done=True,gid='doc-B',navigate='replacement-supplied',replacement=h);self.assertTrue(s['navigate_requested']);self.assertFalse(s['check_before_clear_called']);self.assertEqual(s['header']['slot'],'head-B');self.assertFalse(s['typed_load_success_proved']);self.assertEqual(h['invoice_no'],7)

    def test_31_adjacent_abandon_guard_controls_not_actual_prompt(self):
        self.assertTrue(abandon_guard(updated=True,answer='No')['blocks_navigation']);self.assertFalse(abandon_guard(updated=True,answer='Yes')['blocks_navigation']);self.assertTrue(abandon_guard(is_new=True,row_count=1)['blocks_navigation']);self.assertFalse(abandon_guard(is_new=True,row_count=0)['blocks_navigation']);self.assertFalse(abandon_guard()['runtime_dialog_observed'])

    def test_32_null_fallback_requires_snapshot_and_does_not_prove_load(self):
        s=command('order',header(),done=True,gid='doc-B',navigate='null-fallback-supplied',replacement=header(slot='fallback-supplied'));self.assertTrue(s['new_flag_tail_reached']);self.assertFalse(s['typed_load_success_proved']);self.assertEqual(s['header']['slot'],'fallback-supplied')
        with self.assertRaises(ValueError):command('order',header(),navigate='null-fallback-supplied')
        s=command('order',header(),done=True,gid='doc-B',navigate='escapes-Navigate');self.assertIsNone(s['number_request']);self.assertFalse(s['new_flag_tail_reached'])

    def test_33_helper_catch_before_number_can_reach_ISNew(self):
        s=command('purchase',header(),number_boundary='caught-before-number');self.assertEqual((s['header']['invoice_no'],s['header']['combined']),(7,'combined-A'));self.assertTrue(s['new_flag_tail_reached']);self.assertIn('helper-catch-and-error-report-return-supplied',s['events'])

    def test_34_helper_catch_after_number_can_reach_label_with_old_combined(self):
        s=command('receive',header(),number_boundary='caught-after-number');self.assertEqual((s['header']['invoice_no'],s['header']['combined'],s['label']),(41,'combined-A','visible'));self.assertFalse(s['typed_load_success_proved'])

    def test_35_helper_nonreturn_distinct_from_catch_return(self):
        for route in ROUTES[1:]:
            s=command(route,header(),number_boundary='escapes-helper');self.assertFalse(s['new_flag_tail_reached']);self.assertEqual(s['label'],'collapsed');self.assertEqual(s['header']['invoice_no'],7);self.assertIsNotNone(s['number_request'])

    def test_36_field1_header2_difference_unresolved_policy(self):
        a=command('receive',header())
        for route in ('order','purchase'):
            s=command(route,a['header'],field_proc=a['field_proc']);self.assertEqual((s['header']['proc'],s['field_proc'],s['number_request']['proc_type']),(2,1,1));self.assertTrue(self.witness()['field_header_proc_difference_policy_unresolved']);self.assertFalse(s['number_reserved'])

    def test_37_gid_not_written_and_same_candidate_control(self):
        for route in ROUTES[1:]:
            s=command(route,header(),candidate=7);self.assertEqual((s['header']['gid'],s['header']['invoice_no']),('doc-A',7));self.assertEqual(s['header']['slot'],'head-A');self.assertFalse(s['SDK_setters_or_aliasing_or_final_UI_state_proved']);self.assertFalse(s['application_source_or_provider_executed'])

    def test_38_supplied_null_header_stops_before_field_write(self):
        for route in ROUTES[1:]:
            s=command(route,None);self.assertIsNone(s['header']);self.assertEqual(s['field_proc'],2);self.assertIsNone(s['number_request']);self.assertFalse(s['new_flag_tail_reached'])

    def test_39_strict_boundaries_no_bool_int_alias_or_unknown_defaults(self):
        for val in (None,1,'x'*81,'x\n','/real/file','+966555'):
            with self.assertRaises(ValueError):token(val)
        for val in (True,False,-1,65,1.0,'1'):
            with self.assertRaises(ValueError):number(val)
        for val in (0,1,None,'true'):
            with self.assertRaises(ValueError):flag(val)
        for fn in (lambda:checked_header({}),lambda:header(proc=True),lambda:command('other',header()),lambda:command('order',header(),candidate=True),lambda:command('order',header(),done=1),lambda:command('search',header(),replacement={}),lambda:command('order',header(),modal='chrome-X'),lambda:command('order',header(),number_boundary='actual-provider-error')):
            with self.assertRaises(ValueError):fn()

    def test_40_exclusions_and_query_predicate_boundaries_not_certification(self):
        self.assertEqual([request(r)['branch_predicate_at_Navigate'] for r in ROUTES],[True,True,False,False]);self.assertFalse(any(request(r)['kind_proc_deleted_or_status_rechecked_at_Navigate'] for r in ROUTES));w=self.witness();self.assertFalse(w['source_enum_or_external_InvoiceDGV_contract_proved']);self.assertFalse(w['dialog_modal_return_or_Loaded_order_observed']);self.assertTrue(w['previous_year_return_button_and_other_callers_not_certified']);self.assertEqual(w['whole_local_source_bodies_reread'],0)

    def test_41_ACTUAL_LIVE37_versioned36_API15_parser(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B36_CLI['default'],'B36');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B37');p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B37')
        for part in ('A',)+tuple(f'B{n}' for n in range(1,38)):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        for n in range(18,37):self.assertEqual(getattr(v,f'PHASE7_B{n}_CLI')['default'],f'B{n}')

    def test_42_ACTUAL_19_AST_gates_B36_before_current(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());raw=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(raw).hexdigest(),b37.DISPATCHER_SHA)
        tree=ast.parse(raw);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main);self.assertLess(body.index('historical_b35_validation('),body.index('historical_b36_validation('));self.assertLess(body.index('historical_b36_validation('),body.index('extend_transfer_picker('));self.assertIn('extend_invoice_picker(historical_b36,',body)
        actual=[set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part'];expected=[{f'B{i}' for i in range(first,38)} for first in range(1,20)];self.assertEqual(actual,expected)
        for n in range(19):
            bad=copy.deepcopy(actual);bad[n].remove('B37')
            with self.assertRaises(AssertionError):self.assertEqual(bad,expected)
        block=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'");self.assertIn('build_cli_parser().parse_args()',ast.unparse(block))

    def test_43_ALL52_launcher_restore_no_old_dispatcher_code(self):
        src=ast.unparse(ast.parse((A/'tools/run_historical_invoice_picker_tests_07B37.py').read_text()))
        for text in ('suite.countTestCases() != 52','run.testsRun != 52 or run.skipped','loadTestsFromModule(historical_tests)','historical_tests.A = v.AUDIT','historical_tests.Path = type(v.AUDIT)','historical_tests.A = original_a','historical_tests.Path = original_path','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B36_CLI','b37.historical_b36_inputs('):self.assertIn(text,src)
        for text in ('unittest.skip','v.__file__ =','Path.read_bytes =','Path.open =','exec('):self.assertNotIn(text,src)

    def test_44_historical135_assertions_not_current139_execution_tools(self):
        prov=json.loads((A/'evidence/provenance-07B37.json').read_bytes());self.assertEqual(len(prov['historical_checker_sources_at_entry']),135);self.assertEqual(len(list((A/'tools').glob('*.py'))),139)
        raw=(A/b37.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));texts=json.loads((A/b37.SHARED_SNAPSHOT).read_bytes())['files'];before=v.AUDIT,v.read,v.rows;code,file=v.main.__code__,v.__file__;methods=Path.read_bytes,Path.read_text,Path.open,Path.glob
        with b37.historical_b36_inputs(v,old,texts,raw,prov['historical_checker_sources_at_entry'],(A/b37.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT/'tools').glob('*.py'))),135);self.assertEqual(hashlib.sha256(type(v.AUDIT)(v.__file__).read_bytes()).hexdigest(),b37.DISPATCHER_SHA)
            with (v.AUDIT/'findings.csv').open(newline='') as f:self.assertEqual(list(csv.DictReader(f)),old)
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
        self.assertTrue(all(x is y for x,y in zip(before,(v.AUDIT,v.read,v.rows))))

    def test_45_protected1173_registry_raw_and_potentials(self):
        prov=json.loads((A/'evidence/provenance-07B37.json').read_bytes());h=prov['historical_artifact_sha256'];self.assertEqual(len(h),1173);self.assertEqual(h['findings.csv'],b37.SNAPSHOT_SHA);self.assertNotIn('findings.csv',prov['declared_mutable_entry_paths']);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==s for n,s in h.items()))
        raw=(A/b37.SNAPSHOT).read_bytes();self.assertEqual((A/'findings.csv').read_bytes(),raw);rows=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        for root in ('P4-014','P7-108','P7-132','P7-145'):self.assertEqual(next(r for r in rows if r['id']==root)['certainty'],'potential')

    def test_46_scope_four_old_paths_no_whole_zero_new_completions(self):
        d=json.loads((A/'evidence/scope-decision-07B37.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(4,428,4,0,428,399));self.assertEqual((d['historical_metadata_screen_count'],d['parent_path_matched_metadata_rows'],d['selected_prior_report_sections'],d['additional_selected_extension_contract_sections']),(335,71,8,2));self.assertEqual((d['whole_local_source_bodies_reread'],d['newly_completed_local_files']),(0,0))
        w=self.witness()
        for k,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('context_reads_not_command_certification',CONTEXT_SLICES),('whole_local_rereads_not_new_completions',WHOLE_REREADS)):
            self.assertEqual(tuple((r['path'],r['start'],r['end']) for r in w[k]),declared)
            for r in w[k]:self.assertEqual(hashlib.sha256((A.parents[1]/r['path']).read_bytes()).hexdigest(),r['sha256'])
        screen=json.loads((A/'evidence/dedup-screen-07B37.json').read_bytes());rows=list(csv.DictReader(io.StringIO((A/b37.SNAPSHOT).read_text(),newline='')));self.assertEqual(b37.dedup_errors(screen,rows),[])
        for k,val in (('all_historical_bodies_reviewed',True),('new_root_ids',['P7-164']),('selected_prior_finding_sections',[]),('old_046_B28_extension_retained_not_reextended',False)):self.assertTrue(b37.dedup_errors(screen|{k:val},rows))

    def test_47_no164_no_registry_tail_or_implicit_certainty_transfer(self):
        ad=self.table('root-adjudication');self.assertFalse(any(r['decision'] in ('new-local-root','extended-existing-root-not-new') for r in ad));self.assertEqual(self.table('historical-extensions'),[]);self.assertEqual([r['current_root_ids'] for r in ad[:2]],['P7-159','P7-160'])
        with (A/'findings.csv').open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),335);self.assertEqual(rows[-1]['id'],'P7-163');self.assertNotIn('P7-164',{r['id'] for r in rows});self.assertEqual((A/'findings.csv').read_bytes(),(A/b37.SNAPSHOT).read_bytes())
        old_ext=(A/'evidence/historical-extensions-07B28.csv').read_bytes();self.assertIn(b'P7-046',old_ext)

    def test_48_full_inputs_two_distinct_unexecuted_plans_per_FE(self):
        self.assertEqual(b37.residual_errors(self.table('residual-disposition'),self.table('residual-disposition',36)),[]);self.assertEqual(b37.split_errors(self.table('split-register'),self.table('split-register',36)),[]);data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b37.current_link_errors(*data),[])
        for f in data[0]:
            linked=[t for t in data[2] if t['feature_ids']==f['id']];self.assertEqual(len(linked),2);self.assertNotEqual(linked[0]['acceptance_criterion'],linked[1]['acceptance_criterion'])
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertIn('إذن',t['prerequisites']);self.assertIn('not-executed',t['safety_controls'])
        for stem in ('handoffs','questions'):
            for old,new in zip(self.table(stem,36),self.table(stem)):self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))

    def test_49_reference16_raw_clock_capture9769_deliverya83_distinct(self):
        p=json.loads((A/'evidence/provenance-07B37.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B37.md').read_text();self.assertEqual(b37.date_identity_errors(p,note),[]);self.assertTrue(b37.date_identity_errors(p|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b37.date_identity_errors(p,note.replace(b37.B36_CHECK_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B36.json').read_bytes());self.assertEqual(old['checkout_head'],'9769e29b8ce34f720fd660a475800f5c3bf9b7fa');self.assertNotEqual(old['checkout_head'],b37.ENTRY)

    def test_50_synthetic42_schema_not_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b37.historical_record_errors(h),[])
        for k,val in (('registry_used','findings.csv'),('findings_total',336),('process_exit_code',True),('audit_checker_self_test_cases_reported',1346),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][k]=val;self.assertTrue(b37.historical_record_errors(bad))
        for k,val in (('tests_reported',51),('historical_source_assertion_input_count',139),('test_module_Path_and_A_are_historical_assertion_inputs_only',1),('auxiliary_dispatcher_text_sha256','b'*64)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B36_child'][k]=val;self.assertTrue(b37.historical_record_errors(bad))
        self.assertTrue(b37.historical_record_errors(h|dict(historical_mode_count=True)))

    def test_51_ACTUAL42_archive139_single_inverse_pin_proof(self):
        raw=(A/'evidence/historical-mode-verification-07B37.json').read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b37.HISTORICAL_RUN_SHA);self.assertEqual(b37.historical_record_errors(h),[]);self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b37.ENTRY,v.HEAD,v.BRANCH))
        sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),139);self.assertEqual(b37.capture_source_errors(h,sources),[])
        for k in ('tools/validate_transfer_picker_part.py','tools/test_transfer_picker_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[k]+=b'\n';self.assertTrue(b37.capture_source_errors(h,changed))
        self.assertTrue(b37.capture_source_errors(h,{}));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']));self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        proof=json.loads((A/'evidence/capture-time-identity-07B37.json').read_bytes());self.assertEqual((proof['archive_bytes'],proof['archive_sha256'],proof['capture_tool_set_count'],proof['unchanged_capture_tool_count'],proof['raw_stdout_identities_temporarily_rechecked']),(len(raw),b37.HISTORICAL_RUN_SHA,139,138,42));self.assertTrue(proof['exact_inverse_reconstructs_capture_time_bytes']);self.assertFalse(proof['wholesale42_replayed_after_pin'])

    def test_52_actual139_AST_safe_imports_and_all_B36_records_protected(self):
        tools=list((A/'tools').glob('*.py'));self.assertEqual(len(tools),139)
        for p in tools:ast.parse(p.read_text(),filename=str(p))
        tree=ast.parse((A/'tools/check_transfer_picker_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','pathlib','check_invoice_picker_witnesses'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        h=json.loads((A/'evidence/provenance-07B37.json').read_bytes())['historical_artifact_sha256']
        for n in ('findings.csv','evidence/checks-07B36.json','evidence/official-capture-receipt-07B36.json','evidence/historical-mode-verification-07B36.json','evidence/capture-time-identity-07B36.json','evidence/invoice-picker-witnesses-07B36.json','tools/test_invoice_picker_audit_validator.py','tools/validate_invoice_picker_part.py','tools/run_historical_linked_return_tests_07B36.py','DATE-IDENTITY-NOTE-07B36.md','evidence/tool-warning-note-07B34.json','evidence/witness-precheck-note-07B36.json'):
            self.assertIn(n,h);self.assertEqual(hashlib.sha256((A/n).read_bytes()).hexdigest(),h[n])
        note=json.loads((A/'evidence/witness-precheck-note-07B36.json').read_bytes());self.assertEqual(note['process_exit_code'],1);self.assertIn('utf8-sig',note['error']);self.assertFalse(note['application_source_or_protected_artifacts_changed']);self.assertFalse(note['validator_or_historical_tests_relaxed'])


if __name__=='__main__':unittest.main()
