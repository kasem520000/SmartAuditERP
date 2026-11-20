#!/usr/bin/env python3
"""52 NEW B36 documentary cases,NOT32 operational plans or ERP acceptance.

ALL1242 prior cases unchanged. Synthetic41 fixture is schema data,not proof of
actual historical subprocesses. Actual LIVE36/135 execution tools independent
from child-local historical131 assertions/dispatcher TEXT for B35.
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
import validate_invoice_picker_part as b36
from check_invoice_picker_witnesses import fresh,request,row,checked_row,rows_input,source_row,query_select,local_proc_filter,accept,caller_gate,refresh,flag,number,token,SOURCE_SLICES,CONTEXT_SLICES,WHOLE_REREADS
A=Path(__file__).resolve().parents[1]


class InvoicePickerAuditTests(unittest.TestCase):
    def old(self):return [dict(id=f'PX-{n:03d}',severity='Medium',certainty='potential',type='synthetic-only',status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for n in range(335)]
    def raw(self,rows):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\r\n');w.writeheader();w.writerows(rows);return s.getvalue().encode()
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def texts(self):return {n:'FROZEN:'+n for n in b36.SHARED_DOCS}
    def sources(self):
        raw=b'# synthetic historical dispatcher assertion TEXT,NOT executed\n'
        return ({'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{n:03d}.py':'a'*64 for n in range(130)}),raw
    def context(self,f):return b36.historical_b35_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())
    def table(self,stem,part=36):
        with (A/'evidence'/f'{stem}-07B{part}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
    def groups(self,n):return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1,n+1))+'\n'
    def witness(self):return json.loads((A/'evidence/invoice-picker-witnesses-07B36.json').read_bytes())
    def history_fixture(self):
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B35.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B35-not-current-B36-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_linked_return_tests_07B36.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=131,auxiliary_dispatcher_text_sha256=b36.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B35',findings_total=335,registry_used=b36.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1242,audit_checker_self_test_suite_count=36,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B35_child=child))
        return dict(historical_mode_count=41,historical_modes=modes,errors=[])

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
                with b36.historical_b35_inputs(self.fake(),*args):pass
        old[0]['id']=old[1]['id']
        with self.assertRaises(ValueError):
            with b36.historical_b35_inputs(self.fake(),old,self.texts(),self.raw(old),*src):pass

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
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertEqual(len(list((f.AUDIT/'tools').glob('*.py'))),131)
            p=f.AUDIT/'tools/validate_audit.py';self.assertEqual(p.read_bytes(),raw)
            with p.open('rb') as s:self.assertEqual(s.read(),raw)
            for mode in ('w','a','r+','wb'):
                with self.assertRaises(ValueError):p.open(mode)
            self.assertEqual(p.resolve(),Path('/synthetic/audit/tools/validate_audit.py'));self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())

    def test_05_exact_list_argv_proxy_no_shared_subprocess(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'ok');proxy=b36.HistoricalB35Subprocess(backend,'python',Path('/a/tools'));kw=dict(cwd='/a',timeout=60,capture_output=True,text=True)
        self.assertEqual(proxy.run(list(proxy.expected),**kw),'ok');self.assertEqual(calls[-1],((proxy.actual,),kw))
        for args in (tuple(proxy.expected),proxy.expected+['--other'],['python','-B','/other/test.py']):proxy.run(args,**kw);self.assertEqual(calls[-1],((args,),kw))
        f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b36.HistoricalB35ValidatorView(f);original=subprocess.run
        with self.context(view):self.assertIs(subprocess.run,original);self.assertIs(f.subprocess,backend)

    def test_06_ALL335_every_field_exact(self):
        old=self.old();self.assertEqual(b36.registry_preservation_errors(old,copy.deepcopy(old),self.raw(old),self.raw(old),[]),[])
        for n in (0,330,331,332,333,334):
            for k in old[n]:
                bad=copy.deepcopy(old);bad[n][k]='changed';self.assertTrue(b36.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]),(n,k))

    def test_07_entire_raw336_not_prefix_CRLF_noBOM(self):
        old=self.old();raw=self.raw(old)
        for bad in (raw+b'\r\n',raw.replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+raw,raw[:-2],raw.replace(b'fixture-title',b'other',1)):self.assertTrue(b36.registry_preservation_errors(old,old,bad,raw,[]))

    def test_08_zero_new_roots_and_extensions(self):
        old=self.old()
        for bad in (old[:-1],old+[old[-1]|dict(id='P7-164')],old[:-1]+[old[-1]|dict(id='P7-164')]):self.assertTrue(b36.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]))
        self.assertTrue(b36.registry_preservation_errors(old,old,self.raw(old),self.raw(old),[dict(finding_id='P7-157')]))

    def test_09_G260_exact_only261_to264(self):
        self.assertEqual(b36.group_row_errors(self.groups(260),self.groups(264)),[])
        for bad in (self.groups(263),self.groups(265),self.groups(264).replace('| G-01 | exact','| G-01 | changed'),self.groups(264).replace('G-260','G-259')):self.assertTrue(b36.group_row_errors(self.groups(260),bad))

    def test_10_documentary_sentinels_no_fake_source(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b36.validate_source(f,dict(id='FE7B36-15',evidence=b36.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b36.validate_source(f,dict(id='FE7B36-01',evidence=b36.DOCUMENTARY),{});self.assertTrue(errors)
        errors.clear();b36.validate_source(f,dict(id='FE7B36-15',evidence='a.cs:1-2'),{});self.assertTrue(errors)

    def test_11_PQ8_PR8_ordered_exact_unions(self):
        pq,pr,fe=[self.table(n) for n in ('picker-request-lineage','picker-result-lineage','feature-implementation-matrix')];self.assertEqual(b36.ledger_errors(pq,pr,fe),[])
        for pool,index,k in ((pq,0,'source_to_output'),(pr,3,'evidence'),(pq,1,'finding_ids'),(pr,7,'feature_ids')):
            bad=copy.deepcopy(pool);bad[index][k]+=';changed';self.assertTrue(b36.ledger_errors(bad,pr,fe) if pool is pq else b36.ledger_errors(pq,bad,fe))
        self.assertTrue(b36.ledger_errors(pq[::-1],pr,fe))

    def test_12_lineage_owner_inputs_and_limits(self):
        pq,pr,fe=[self.table(n) for n in ('picker-request-lineage','picker-result-lineage','feature-implementation-matrix')]
        for pool in (pq,pr):
            for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','runtime_status'):
                bad=copy.deepcopy(pool);bad[0][k]='';self.assertTrue(b36.ledger_errors(bad,pr,fe) if pool is pq else b36.ledger_errors(pq,bad,fe))

    def test_13_FE16_INV16_T32_bidirectional_links(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b36.current_link_errors(*data),[])
        for i,k in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'invariant_ids'),(0,'finding_ids')):
            bad=copy.deepcopy(data);bad[i][0][k]='P7-164';self.assertTrue(b36.current_link_errors(*bad))

    def test_14_each_capability_entry_source_output_owner_exit(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')]
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim','static_exit_criterion'):
            bad=copy.deepcopy(data);bad[0][0][k]='short';self.assertTrue(b36.current_link_errors(*bad),k)
        for k in ('procedure','acceptance_criterion','owner_role'):
            bad=copy.deepcopy(data);bad[2][0][k]='short';self.assertTrue(b36.current_link_errors(*bad))

    def test_15_RS14_ancestry_hash_contracts(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',35);self.assertEqual(b36.residual_errors(cur,old),[])
        for k in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(cur);bad[0][k]='changed';self.assertTrue(b36.residual_errors(bad,old))

    def test_16_full_input_mapped_routes_dispositions(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',35)
        for k,val in (('required_redacted_input','new-short-input'),('current_handoff_or_split_ids','H7B36-06'),('disposition','accepted'),('runtime_status','passed')):
            bad=copy.deepcopy(cur);bad[2][k]=val;self.assertTrue(b36.residual_errors(bad,old))

    def test_17_SP3_full_input_and_future_not_started(self):
        cur,old=self.table('split-register'),self.table('split-register',35);self.assertEqual(b36.split_errors(cur,old),[])
        for k,val in (('upstream_row_sha256','changed'),('required_input','replacement'),('status','complete'),('owner_role','')):
            bad=copy.deepcopy(cur);bad[0][k]=val;self.assertTrue(b36.split_errors(bad,old))

    def test_18_fourB_sixC_work_and_backlog_ancestry(self):
        rw=self.table('remaining-workplan');self.assertEqual(b36.remaining_work_errors(rw),[])
        for k,val in (('part_family','7C'),('status','complete'),('runtime_status','passed'),('counts_are_sessions_or_completion_percent','true')):
            bad=copy.deepcopy(rw);bad[3][k]=val;self.assertTrue(b36.remaining_work_errors(bad))
        for n,(old,new) in enumerate(zip(self.table('continuation-backlog',35),self.table('continuation-backlog')),1):
            self.assertEqual((new['prior_backlog_id'],new['original_backlog_id']),(f'BK7B35-{n:02d}',f'BK7-{n:02d}'));self.assertTrue(new['required_work'].startswith(old['required_work']));self.assertEqual(new['status'],old['status'])

    def test_19_witness_strict_counts_bools_and_erratum(self):
        w=self.witness();self.assertEqual(b36.witness_metadata_errors(w),[])
        for k,val in (('illustration_count',True),('erp_runtime_tests_executed',False),('local_InvoiceSrchRow_auto_properties_known',1),('real_query_or_conversion_failures_executed',0),('newly_completed_local_files',1),('new_root_ids',['P7-164'])):self.assertTrue(b36.witness_metadata_errors(w|{k:val}))
        bad=copy.deepcopy(w);bad['retained_additive_B10_arithmetic_erratum']['local_cost']=True;self.assertTrue(b36.witness_metadata_errors(bad))

    def test_20_witness_actual_subprocess_exact_bytes(self):
        r=subprocess.run([sys.executable,'-B',str(A/'tools/check_invoice_picker_witnesses.py')],cwd=A.parents[1],capture_output=True,timeout=30);self.assertEqual((r.returncode,r.stderr),(0,b''));self.assertEqual(r.stdout,(A/'evidence/invoice-picker-witnesses-07B36.json').read_bytes())

    def test_21_fresh_local_defaults_and_request_order(self):
        s=fresh();self.assertEqual((s['done'],s['gid'],s['proc'],s['pay'],s['inv_type']),(False,'-1',1,1,6))
        q=request(proc=2,inv_type=2);self.assertEqual((q['proc'],q['inv_type']),(2,2));self.assertLess(q['events'].index('ConnObj-called-before-caller-inputs'),q['events'].index('caller-ProcType-assigned'));self.assertFalse(q['immutable_request_object_in_source'])

    def test_22_connection_tokens_not_ownership_or_enum_mapping(self):
        q=request(before_conn='conn-A',later_conn='conn-B',credit_hint=22);self.assertEqual(q['constructor_connection_token'],'conn-A');self.assertEqual(q['later_global_connection_token'],'conn-B')
        self.assertFalse(q['connection_content_or_liveness_or_ownership_proved']);self.assertFalse(q['enum_numeric_mapping_proved'])

    def test_23_allowed20_or_requested_same_root157(self):
        sources=[source_row(kind=1),source_row('doc-B',kind=20),source_row('doc-C',kind=2)];out=query_select(sources,request())
        self.assertEqual([r['gid'] for r in out],['doc-A','doc-B']);self.assertEqual(sources[1]['kind'],20)
        self.assertEqual(query_select(sources,request(credit_hint=22)),out)

    def test_24_branch_deleted_proc_predicate_controls(self):
        rows=[source_row(),source_row('doc-B',branch=2),source_row('doc-C',proc=2),source_row('doc-D',deleted=True)]
        self.assertEqual([r['gid'] for r in query_select(rows,request())],['doc-A'])
        self.assertEqual([r['gid'] for r in query_select(rows,request(proc=2))],['doc-C'])

    def test_25_contract23_exact_and20_no_duplicate_control(self):
        rows=[source_row(kind=23),source_row('doc-B',kind=20)];self.assertEqual([r['kind'] for r in query_select(rows,request(inv_type=23))],[23]);self.assertEqual(len(query_select(rows,request(inv_type=20))),1)

    def test_26_local_proc_filter_cannot_restore_missing_source(self):
        master=[row()];self.assertEqual(local_proc_filter(master,2),[]);self.assertEqual(local_proc_filter(master,0),master);self.assertEqual(local_proc_filter(master,1),master);self.assertEqual(master,[row()])

    def test_27_enter_valid_index_publishes_before_Close_request(self):
        a,b=row(),row('doc-B',2,-1);s=accept('enter',[a,b],index=1);self.assertEqual((s['done'],s['gid'],s['proc'],s['pay']),(True,'doc-B',2,-1))
        self.assertLess(s['events'].index('ISDone-written-before-three-payload-fields'),s['events'].index('gid-proc-pay-copied-from-supplied-local-row'));self.assertEqual(s['events'][-1],'Close-requested');self.assertFalse(s['lookup_called'])

    def test_28_invalid_index_requests_selection_not_acceptance(self):
        for index in (-1,1,64):
            s=accept('enter',[row()],index=index);self.assertFalse(s['done']);self.assertEqual(s['gid'],'-1');self.assertEqual(s['events'],['SelectedIndex-zero-and-scroll-requested-not-observed-SelectionChanged'])
        self.assertEqual(accept('enter',[])['events'],[])

    def test_29_double_SelectedItem_not_supplied_index_or_actual_desync(self):
        a,b=row(),row('doc-B');s=accept('double',[a,b],index=0,selected=b);self.assertEqual(s['gid'],'doc-B');self.assertEqual(s['events'][-1],'Hide-requested');self.assertFalse(s['lookup_called']);self.assertFalse(accept('double',[a])['done'])

    def test_30_current_year_fresh_Escape_and_close_not_accepted(self):
        for route in ('escape','close-button'):
            s=accept(route,[row()],previous_year=False);self.assertEqual((s['done'],s['gid']),(False,'-1'));self.assertFalse(s['global_connection_restore_requested']);self.assertFalse(caller_gate(s,True)['binding_requested'])

    def test_31_previous_year_context_not_end_to_end_certification(self):
        button=accept('close-button',[],previous_year=True);esc=accept('escape',[],previous_year=True)
        self.assertTrue(button['global_connection_restore_requested']);self.assertFalse(button['previous_year_flag_after']);self.assertFalse(esc['global_connection_restore_requested']);self.assertTrue(esc['previous_year_flag_after'])
        self.assertTrue(self.witness()['return_button_and_previous_year_controls_not_certified'])

    def test_32_separate_return_button_requires_Tag_and_lookup(self):
        self.assertFalse(accept('return-button',[row()])['lookup_called']);s=accept('return-button',[row()],tag=row());self.assertTrue(s['lookup_called']);self.assertTrue(s['control_only_not_selected_linked_command']);self.assertTrue(s['done'])

    def test_33_return_lookup_found_rejects_failed_is_catch_false_context(self):
        blocked=accept('return-button',[],tag=row(),lookup='found');failed=accept('return-button',[],tag=row(),lookup='failed');self.assertFalse(blocked['done']);self.assertTrue(failed['done']);self.assertIn('lookup-false-including-catch-false-not-typed-Failed',failed['events'])
        self.assertEqual(self.witness()['new_root_ids'],[])

    def test_34_modal_return_supplied_separately_from_Close_or_Hide(self):
        for route,kw in (('enter',dict(index=0)),('double',dict(selected=row()))):
            s=accept(route,[row()],**kw);self.assertTrue(s['done']);self.assertFalse(caller_gate(s,False)['binding_requested']);self.assertTrue(caller_gate(s,True)['binding_requested']);self.assertTrue(s['modal_result_not_inferred'])

    def test_35_sentinel_only_gate_not_nonempty_DocumentRef(self):
        for done,gid,want in ((False,'doc-A',False),(True,'-1',False),(True,'',True),(True,'doc-A',True)):self.assertEqual(caller_gate(dict(done=done,gid=gid),True)['first_result_gate'],want)

    def test_36_gate_is_not_LoadComplete_or_AcceptedLines(self):
        r=caller_gate(accept('enter',[row()],index=0),True);self.assertTrue(r['binding_requested']);self.assertFalse(r['typed_load_success_proved']);self.assertFalse(r['requested_type_proc_branch_rechecked_here']);self.assertEqual(r['query_predicates_at_this_boundary'],['IS_Deleted=0','InvGlobalID=chosen'])

    def test_37_known_empty_different_from_failure_old046_retained(self):
        a,b=row(),row('doc-B');self.assertEqual(refresh([a],[])['display'],[]);self.assertEqual(refresh([a],[b],'before-clear')['display'],[a]);self.assertFalse(refresh([a],[])['typed_health_returned'])

    def test_38_supplied_prefix_boundary_not_DataAdapter_or_Convert_run(self):
        a,b=row(),row('doc-B');r=refresh([b],[a,b],'during-row',1);self.assertEqual(r['display'],[a]);self.assertFalse(r['actual_DataView_or_conversion_or_provider_executed']);self.assertEqual(refresh([b],[a],'after-clear')['display'],[])

    def test_39_strict_models_eager_validation_no_bool_int_alias(self):
        for val in (None,1,'','x'*81,'x\n','/real/file','+966555'):
            with self.assertRaises(ValueError):token(val)
        for val in (True,False,-1,65,1.0,'1'):
            with self.assertRaises(ValueError):number(val)
        for val in (0,1,None,'true'):
            with self.assertRaises(ValueError):flag(val)
        for r in (dict(gid='doc-A'),row()|dict(kind=1),dict(gid='doc-A',proc=True,pay=1)):
            with self.assertRaises(ValueError):checked_row(r)
        for fn in (lambda:accept('escape',[dict(gid='doc-A')]),lambda:caller_gate(dict(done=False,gid='/real/path'),False),lambda:query_select([source_row()|dict(deleted=1)],request()),lambda:refresh([],[row()],'during-row',2)):
            with self.assertRaises(ValueError):fn()

    def test_40_exclusions_not_silently_inferred_from_known_local_row(self):
        with self.assertRaises(ValueError):accept('chrome-X',[])
        with self.assertRaises(ValueError):refresh([],[],'actual-provider-failure')
        with self.assertRaises(TypeError):request(InvoiceDGV_default=True)
        w=self.witness();self.assertTrue(w['local_InvoiceSrchRow_auto_properties_known']);self.assertFalse(w['source_enum_or_external_InvoiceDGV_contract_proved']);self.assertFalse(w['dialog_modal_return_or_Loaded_order_observed']);self.assertEqual(w['newly_completed_local_files'],0)

    def test_41_ACTUAL_LIVE36_versioned35_API15_parser(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B35_CLI['default'],'B35');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B36');p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B36')
        for part in ('A',)+tuple(f'B{n}' for n in range(1,37)):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        for n in range(18,36):self.assertEqual(getattr(v,f'PHASE7_B{n}_CLI')['default'],f'B{n}')

    def test_42_ACTUAL_19_AST_gates_B35_before_current(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());raw=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(raw).hexdigest(),b36.DISPATCHER_SHA)
        tree=ast.parse(raw);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main);self.assertLess(body.index('historical_b34_validation('),body.index('historical_b35_validation('));self.assertLess(body.index('historical_b35_validation('),body.index('extend_invoice_picker('));self.assertIn('extend_linked_return(historical_b35,',body)
        actual=[set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part'];expected=[{f'B{i}' for i in range(first,37)} for first in range(1,20)];self.assertEqual(actual,expected)
        for n in range(19):
            bad=copy.deepcopy(actual);bad[n].remove('B36')
            with self.assertRaises(AssertionError):self.assertEqual(bad,expected)
        block=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'");self.assertIn('build_cli_parser().parse_args()',ast.unparse(block))

    def test_43_ALL52_launcher_restore_no_old_dispatcher_code(self):
        src=ast.unparse(ast.parse((A/'tools/run_historical_linked_return_tests_07B36.py').read_text()))
        for text in ('suite.countTestCases() != 52','run.testsRun != 52 or run.skipped','loadTestsFromModule(historical_tests)','historical_tests.A = v.AUDIT','historical_tests.Path = type(v.AUDIT)','historical_tests.A = original_a','historical_tests.Path = original_path','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B35_CLI','b36.historical_b35_inputs('):self.assertIn(text,src)
        for text in ('unittest.skip','v.__file__ =','Path.read_bytes =','Path.open =','exec('):self.assertNotIn(text,src)

    def test_44_historical131_assertions_not_current135_execution_tools(self):
        prov=json.loads((A/'evidence/provenance-07B36.json').read_bytes());self.assertEqual(len(prov['historical_checker_sources_at_entry']),131);self.assertEqual(len(list((A/'tools').glob('*.py'))),135)
        raw=(A/b36.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));texts=json.loads((A/b36.SHARED_SNAPSHOT).read_bytes())['files'];before=v.AUDIT,v.read,v.rows;code,file=v.main.__code__,v.__file__;methods=Path.read_bytes,Path.read_text,Path.open,Path.glob
        with b36.historical_b35_inputs(v,old,texts,raw,prov['historical_checker_sources_at_entry'],(A/b36.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT/'tools').glob('*.py'))),131);self.assertEqual(hashlib.sha256(type(v.AUDIT)(v.__file__).read_bytes()).hexdigest(),b36.DISPATCHER_SHA)
            with (v.AUDIT/'findings.csv').open(newline='') as f:self.assertEqual(list(csv.DictReader(f)),old)
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
        self.assertTrue(all(x is y for x,y in zip(before,(v.AUDIT,v.read,v.rows))))

    def test_45_protected1122_registry_raw_and_potentials(self):
        prov=json.loads((A/'evidence/provenance-07B36.json').read_bytes());h=prov['historical_artifact_sha256'];self.assertEqual(len(h),1122);self.assertEqual(h['findings.csv'],b36.SNAPSHOT_SHA);self.assertNotIn('findings.csv',prov['declared_mutable_entry_paths']);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==s for n,s in h.items()))
        raw=(A/b36.SNAPSHOT).read_bytes();self.assertEqual((A/'findings.csv').read_bytes(),raw);rows=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        for root in ('P4-014','P7-108','P7-132','P7-145'):self.assertEqual(next(r for r in rows if r['id']==root)['certainty'],'potential')

    def test_46_scope_three_old_paths_one_reread_zero_new_completions(self):
        d=json.loads((A/'evidence/scope-decision-07B36.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(3,428,3,0,428,399));self.assertEqual((d['historical_metadata_screen_count'],d['parent_path_matched_metadata_rows'],d['selected_prior_report_sections'],d['additional_selected_extension_contract_sections']),(335,69,11,2));self.assertEqual((d['whole_local_source_bodies_reread'],d['newly_completed_local_files']),(1,0));self.assertEqual(d['prior_whole_body_review_parts'],['B27','B28'])
        w=self.witness()
        for k,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('context_reads_not_command_certification',CONTEXT_SLICES),('whole_local_rereads_not_new_completions',WHOLE_REREADS)):
            self.assertEqual(tuple((r['path'],r['start'],r['end']) for r in w[k]),declared)
            for r in w[k]:self.assertEqual(hashlib.sha256((A.parents[1]/r['path']).read_bytes()).hexdigest(),r['sha256'])
        screen=json.loads((A/'evidence/dedup-screen-07B36.json').read_bytes());rows=list(csv.DictReader(io.StringIO((A/b36.SNAPSHOT).read_text(),newline='')));self.assertEqual(b36.dedup_errors(screen,rows),[])
        for k,val in (('all_historical_bodies_reviewed',True),('new_root_ids',['P7-164']),('selected_prior_finding_sections',[]),('old_046_B28_extension_retained_not_reextended',False)):self.assertTrue(b36.dedup_errors(screen|{k:val},rows))

    def test_47_no164_no_registry_tail_or_implicit_certainty_transfer(self):
        ad=self.table('root-adjudication');self.assertFalse(any(r['decision'] in ('new-local-root','extended-existing-root-not-new') for r in ad));self.assertEqual(self.table('historical-extensions'),[]);self.assertEqual([r['current_root_ids'] for r in ad[:2]],['P7-157','P7-160'])
        with (A/'findings.csv').open(newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),335);self.assertEqual(rows[-1]['id'],'P7-163');self.assertNotIn('P7-164',{r['id'] for r in rows});self.assertEqual((A/'findings.csv').read_bytes(),(A/b36.SNAPSHOT).read_bytes())
        old_ext=(A/'evidence/historical-extensions-07B28.csv').read_bytes();self.assertIn(b'P7-046',old_ext)

    def test_48_full_inputs_two_distinct_unexecuted_plans_per_FE(self):
        self.assertEqual(b36.residual_errors(self.table('residual-disposition'),self.table('residual-disposition',35)),[]);self.assertEqual(b36.split_errors(self.table('split-register'),self.table('split-register',35)),[]);data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b36.current_link_errors(*data),[])
        for f in data[0]:
            linked=[t for t in data[2] if t['feature_ids']==f['id']];self.assertEqual(len(linked),2);self.assertNotEqual(linked[0]['acceptance_criterion'],linked[1]['acceptance_criterion'])
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertIn('إذن',t['prerequisites']);self.assertIn('not-executed',t['safety_controls'])
        for stem in ('handoffs','questions'):
            for old,new in zip(self.table(stem,35),self.table(stem)):self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))

    def test_49_reference16_raw_clock_capture_e6_delivery9769_distinct(self):
        p=json.loads((A/'evidence/provenance-07B36.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B36.md').read_text();self.assertEqual(b36.date_identity_errors(p,note),[]);self.assertTrue(b36.date_identity_errors(p|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b36.date_identity_errors(p,note.replace(b36.B35_CHECK_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B35.json').read_bytes());self.assertEqual(old['checkout_head'],'e6f022ab5df771aab9631886ad713a8a7e6dfbfa');self.assertNotEqual(old['checkout_head'],b36.ENTRY)

    def test_50_synthetic41_schema_not_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b36.historical_record_errors(h),[])
        for k,val in (('registry_used','findings.csv'),('findings_total',336),('process_exit_code',True),('audit_checker_self_test_cases_reported',1294),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][k]=val;self.assertTrue(b36.historical_record_errors(bad))
        for k,val in (('tests_reported',51),('historical_source_assertion_input_count',135),('test_module_Path_and_A_are_historical_assertion_inputs_only',1),('auxiliary_dispatcher_text_sha256','b'*64)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B35_child'][k]=val;self.assertTrue(b36.historical_record_errors(bad))
        self.assertTrue(b36.historical_record_errors(h|dict(historical_mode_count=True)))

    def test_51_ACTUAL41_archive135_single_inverse_pin_proof(self):
        raw=(A/'evidence/historical-mode-verification-07B36.json').read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b36.HISTORICAL_RUN_SHA);self.assertEqual(b36.historical_record_errors(h),[]);self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b36.ENTRY,v.HEAD,v.BRANCH))
        sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),135);self.assertEqual(b36.capture_source_errors(h,sources),[])
        for k in ('tools/validate_invoice_picker_part.py','tools/test_invoice_picker_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[k]+=b'\n';self.assertTrue(b36.capture_source_errors(h,changed))
        self.assertTrue(b36.capture_source_errors(h,{}));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']));self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        proof=json.loads((A/'evidence/capture-time-identity-07B36.json').read_bytes());self.assertEqual((proof['archive_bytes'],proof['archive_sha256'],proof['capture_tool_set_count'],proof['unchanged_capture_tool_count'],proof['raw_stdout_identities_temporarily_rechecked']),(len(raw),b36.HISTORICAL_RUN_SHA,135,134,41));self.assertTrue(proof['exact_inverse_reconstructs_capture_time_bytes']);self.assertFalse(proof['wholesale41_replayed_after_pin'])

    def test_52_actual135_AST_stdlib_and_all_B35_records_protected(self):
        tools=list((A/'tools').glob('*.py'));self.assertEqual(len(tools),135)
        for p in tools:ast.parse(p.read_text(),filename=str(p))
        tree=ast.parse((A/'tools/check_invoice_picker_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','hashlib','json','pathlib'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        h=json.loads((A/'evidence/provenance-07B36.json').read_bytes())['historical_artifact_sha256']
        for n in ('findings.csv','evidence/checks-07B35.json','evidence/official-capture-receipt-07B35.json','evidence/historical-mode-verification-07B35.json','evidence/capture-time-identity-07B35.json','evidence/linked-return-witnesses-07B35.json','tools/test_linked_return_audit_validator.py','tools/validate_linked_return_part.py','tools/run_historical_messaging_request_tests_07B35.py','DATE-IDENTITY-NOTE-07B35.md','evidence/tool-warning-note-07B34.json'):
            self.assertIn(n,h);self.assertEqual(hashlib.sha256((A/n).read_bytes()).hexdigest(),h[n])
        note=json.loads((A/'evidence/witness-precheck-note-07B36.json').read_bytes());self.assertEqual(note['process_exit_code'],1);self.assertIn('utf8-sig',note['error']);self.assertFalse(note['application_source_or_protected_artifacts_changed']);self.assertFalse(note['validator_or_historical_tests_relaxed'])


if __name__=='__main__':unittest.main()
