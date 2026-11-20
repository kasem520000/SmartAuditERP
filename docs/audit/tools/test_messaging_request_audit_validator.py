#!/usr/bin/env python3
"""52 NEW B34 documentary cases,not32 operational acceptance plans or ERP.

All1138 prior cases incl52 B33 remain unmodified. Synthetic history fixtures
are schema-only,NEVER evidence of actual39 subprocesses. Zero new roots or
registry evidence changes;P6-031/033 already describe this interleaving.
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
import validate_messaging_request_part as b34
from check_messaging_request_witnesses import (
    Trace,pair,race,caller_gate,session_route,token,SOURCE_SLICES,EXPLORATORY_SLICES,
)
A=Path(__file__).resolve().parents[1]


class MessagingRequestAuditTests(unittest.TestCase):
    def old(self):
        return [dict(id=f'PX-{n:03d}',severity='Medium',certainty='potential',type='synthetic-only',
            status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for n in range(335)]
    def raw(self,rows):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(rows[0]),lineterminator='\r\n');w.writeheader();w.writerows(rows)
        return s.getvalue().encode()
    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def texts(self):return {n:'FROZEN:'+n for n in b34.SHARED_DOCS}
    def sources(self):
        raw=b'# fixture assertion dispatcher TEXT,NOT executed\n'
        return ({'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{n:03d}.py':'a'*64 for n in range(122)}),raw
    def context(self,f):return b34.historical_b33_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())
    def table(self,stem,part=34):
        with (A/'evidence'/f'{stem}-07B{part}.csv').open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))
    def groups(self,n):return '\n'.join(f'| G-{i:02d} | exact |' for i in range(1,n+1))+'\n'
    def witness(self):return json.loads((A/'evidence/messaging-request-witnesses-07B34.json').read_bytes())
    def event(self,t,name,kind):return next(e for e in t.events if e['request']==name and e['kind']==kind)
    def advance(self,t,name,actions):
        for action in actions:t.step(name,action)
        return t
    def history_fixture(self):
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B33.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=52,expected_tests=52,process_exit_code=0,result='passed',historical_parser_cutoff='B33-not-current-B34-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_output_route_tests_07B34.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,test_module_Path_and_A_are_historical_assertion_inputs_only=True,historical_source_assertion_input_count=123,auxiliary_dispatcher_text_sha256=b34.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B33',findings_total=335,registry_used=b34.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=1138,audit_checker_self_test_suite_count=34,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B33_child=child))
        return dict(historical_mode_count=39,historical_modes=modes,errors=[])

    def test_01_OWN335_raw336_readbytes_readtext_open(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old())
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            for mode in ('r','rt'):
                with (f.AUDIT/'findings.csv').open(mode,encoding='utf8',newline='') as s:self.assertEqual(list(csv.DictReader(s)),self.old())
            with (f.AUDIT/'findings.csv').open('rb') as s:self.assertEqual(s.read(),self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_reject_bad_rows_raw_indexes_sources_TEXT(self):
        old,raw,src=self.old(),self.raw(self.old()),self.sources()
        for args in ((old[:-1],self.texts(),raw,*src),(old,self.texts(),raw.replace(b'\r\n',b'\n'),*src),
                     (old,self.texts(),b'\xef\xbb\xbf'+raw,*src),(old,self.texts(),bytearray(raw),*src),
                     (old,{'README.md':'only'},raw,*src),(old,self.texts(),raw,{},src[1]),
                     (old,self.texts(),raw,src[0],src[1]+b'x')):
            with self.assertRaises(ValueError):
                with b34.historical_b33_inputs(self.fake(),*args):pass
        old[0]['id']=old[1]['id']
        with self.assertRaises(ValueError):
            with b34.historical_b33_inputs(self.fake(),old,self.texts(),self.raw(old),*src):pass

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
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods)
            self.assertEqual(len(list((f.AUDIT/'tools').glob('*.py'))),123)
            p=f.AUDIT/'tools/validate_audit.py';self.assertEqual(p.read_bytes(),raw)
            with p.open('rb') as s:self.assertEqual(s.read(),raw)
            for mode in ('w','a','r+','wb'):
                with self.assertRaises(ValueError):p.open(mode)
            self.assertEqual(p.resolve(),Path('/synthetic/audit/tools/validate_audit.py'))
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())

    def test_05_exact_list_argv_proxy_not_shared_subprocess(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'ok')
        proxy=b34.HistoricalB33Subprocess(backend,'python',Path('/a/tools'));kw=dict(cwd='/a',timeout=60,capture_output=True,text=True)
        self.assertEqual(proxy.run(list(proxy.expected),**kw),'ok');self.assertEqual(calls[-1],((proxy.actual,),kw))
        for args in (tuple(proxy.expected),proxy.expected+['--other'],['python','-B','/other/test.py']):
            proxy.run(args,**kw);self.assertEqual(calls[-1],((args,),kw))
        f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b34.HistoricalB33ValidatorView(f);original=subprocess.run
        with self.context(view):self.assertIs(subprocess.run,original);self.assertIs(f.subprocess,backend)

    def test_06_ALL335_every_field_exact_no_append(self):
        old=self.old();self.assertEqual(b34.registry_preservation_errors(old,copy.deepcopy(old),self.raw(old),self.raw(old),[]),[])
        for n in (0,330,331,332,333,334):
            for key in old[n]:
                bad=copy.deepcopy(old);bad[n][key]='changed'
                self.assertTrue(b34.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]),(n,key))

    def test_07_ENTIRE_raw336_noBOM_CRLF_not_merely_prefix(self):
        old=self.old();raw=self.raw(old)
        for bad in (raw+b'\r\n',raw.replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+raw,raw[:-2],raw.replace(b'fixture-title',b'other',1)):
            self.assertTrue(b34.registry_preservation_errors(old,old,bad,raw,[]))

    def test_08_zero_new_roots_and_zero_evidence_extensions(self):
        old=self.old()
        for bad in (old[:-1],old+[old[-1]|dict(id='P7-164')],old[:-1]+[old[-1]|dict(id='P7-164')]):
            self.assertTrue(b34.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),[]))
        self.assertTrue(b34.registry_preservation_errors(old,old,self.raw(old),self.raw(old),[dict(finding_id='P6-033')]))

    def test_09_G252_exact_only253_to256(self):
        self.assertEqual(b34.group_row_errors(self.groups(252),self.groups(256)),[])
        for bad in (self.groups(255),self.groups(257),self.groups(256).replace('| G-01 | exact','| G-01 | changed'),self.groups(256).replace('G-252','G-251')):
            self.assertTrue(b34.group_row_errors(self.groups(252),bad))

    def test_10_documentary_sentinels_no_invented_source(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b34.validate_source(f,dict(id='FE7B34-15',evidence=b34.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b34.validate_source(f,dict(id='FE7B34-01',evidence=b34.DOCUMENTARY),{});self.assertTrue(errors)
        errors.clear();b34.validate_source(f,dict(id='FE7B34-15',evidence='a.cs:1-2'),{});self.assertTrue(errors)

    def test_11_RQ8_AW8_exact_order_and_source_unions(self):
        rq,aw,fe=[self.table(n) for n in ('request-ownership-lineage','await-boundary-lineage','feature-implementation-matrix')]
        self.assertEqual(b34.ledger_errors(rq,aw,fe),[])
        for pool,index,key in ((rq,0,'source_to_output'),(aw,3,'evidence'),(rq,1,'finding_ids'),(aw,7,'feature_ids')):
            bad=copy.deepcopy(pool);bad[index][key]+=';changed';args=(bad,aw,fe) if pool is rq else (rq,bad,fe)
            self.assertTrue(b34.ledger_errors(*args))
        self.assertTrue(b34.ledger_errors(rq[::-1],aw,fe))

    def test_12_lineage_owner_input_limits_and_nonexecution(self):
        rq,aw,fe=[self.table(n) for n in ('request-ownership-lineage','await-boundary-lineage','feature-implementation-matrix')]
        for pool in (rq,aw):
            for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','runtime_status'):
                bad=copy.deepcopy(pool);bad[0][key]=''
                self.assertTrue(b34.ledger_errors(bad,aw,fe) if pool is rq else b34.ledger_errors(rq,bad,fe))

    def test_13_FE16_INV16_T32_bidirectional_root_links(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b34.current_link_errors(*data),[])
        for i,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'invariant_ids'),(0,'finding_ids')):
            bad=copy.deepcopy(data);bad[i][0][key]='P7-164';self.assertTrue(b34.current_link_errors(*bad))

    def test_14_each_capability_has_owner_entry_source_output_exclusions(self):
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')]
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','entry_point','source_contract','output_boundary','excluded_from_claim'):
            bad=copy.deepcopy(data);bad[0][0][key]='short';self.assertTrue(b34.current_link_errors(*bad),key)
        for key in ('procedure','acceptance_criterion'):
            bad=copy.deepcopy(data);bad[2][0][key]='short';self.assertTrue(b34.current_link_errors(*bad))

    def test_15_RS14_ancestry_SHA_contracts(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',33);self.assertEqual(b34.residual_errors(cur,old),[])
        for key in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(cur);bad[0][key]='changed';self.assertTrue(b34.residual_errors(bad,old))

    def test_16_full_old_inputs_mapped_routes_dispositions_retained(self):
        cur,old=self.table('residual-disposition'),self.table('residual-disposition',33)
        for key,value in (('required_redacted_input','new-short-input'),('current_handoff_or_split_ids','H7B34-06'),('disposition','accepted'),('runtime_status','passed')):
            bad=copy.deepcopy(cur);bad[2][key]=value;self.assertTrue(b34.residual_errors(bad,old))

    def test_17_SP3_input_prefix_and_future_not_started(self):
        cur,old=self.table('split-register'),self.table('split-register',33);self.assertEqual(b34.split_errors(cur,old),[])
        for key,value in (('upstream_row_sha256','changed'),('required_input','replacement'),('status','complete'),('owner_role','')):
            bad=copy.deepcopy(cur);bad[0][key]=value;self.assertTrue(b34.split_errors(bad,old))

    def test_18_fourB_sixC_workplan_and_BK_ancestry(self):
        rw=self.table('remaining-workplan');self.assertEqual(b34.remaining_work_errors(rw),[])
        for key,value in (('part_family','7C'),('status','complete'),('runtime_status','passed'),('counts_are_sessions_or_completion_percent','true')):
            bad=copy.deepcopy(rw);bad[3][key]=value;self.assertTrue(b34.remaining_work_errors(bad))
        bk=self.table('continuation-backlog');self.assertEqual(len(bk),10)
        for n,r in enumerate(bk,1):self.assertEqual((r['prior_backlog_id'],r['original_backlog_id']),(f'BK7B33-{n:02d}',f'BK7-{n:02d}'))
        self.assertEqual([r['status'] for r in bk[2:6]],['not-started']*4)

    def test_19_witness_metadata_strict_counts_bools_and_erratum(self):
        w=self.witness();self.assertEqual(b34.witness_metadata_errors(w),[])
        for key,value in (('illustration_count',True),('erp_runtime_tests_executed',False),('stored_elements_not_silently_retargeted',1),('provider_acceptance_or_delivery_or_file_bytes_upload_proved',0),('new_root_ids',['P7-164'])):
            self.assertTrue(b34.witness_metadata_errors(w|{key:value}))
        bad=copy.deepcopy(w);bad['retained_additive_B10_arithmetic_erratum']['local_cost']=True;self.assertTrue(b34.witness_metadata_errors(bad))

    def test_20_witness_actual_subprocess_recomputes_exact_bytes(self):
        r=subprocess.run([sys.executable,'-B',str(A/'tools/check_messaging_request_witnesses.py')],cwd=A.parents[1],capture_output=True,timeout=30)
        self.assertEqual((r.returncode,r.stderr),(0,b''));self.assertEqual(r.stdout,(A/'evidence/messaging-request-witnesses-07B34.json').read_bytes())

    def test_21_shared_sender_A_resumes_on_supplied_B_context(self):
        t=race();self.assertEqual(self.event(t,'A','caption-enter-request')['selector_or_element_context'],'target-B')
        self.assertEqual(self.event(t,'A','generic-send-control-click-request')['selector_or_element_context'],'target-B')
        self.assertFalse(t.summary()['delivery_proved'])

    def test_22_sequential_complete_requests_negative_control(self):
        t=pair().run_tail('A').run_tail('B')
        self.assertTrue(all(e['selector_or_element_context']==e['requested_target'] for e in t.events if e['kind']=='generic-send-control-click-request'))

    def test_23_distinct_sender_tokens_control_not_deployed_repair(self):
        t=race(separate_senders=True)
        for name in ('A','B'):self.assertEqual(self.event(t,name,'caption-enter-request')['selector_or_element_context'],'target-'+name)
        self.assertEqual(len(t.dom),2)

    def test_24_same_recipient_removes_cross_target_difference_not_duplicate_intent(self):
        t=race(same_target=True);events=[e for e in t.events if e['kind']=='generic-send-control-click-request']
        self.assertEqual(len(events),2);self.assertEqual({e['selector_or_element_context'] for e in events},{'target-A'})
        self.assertNotEqual(events[0]['request'],events[1]['request'])

    def test_25_blank_caption_skips_text_not_shared_file_selector(self):
        t=race(caption=False);self.assertFalse(any(e['kind']=='caption-enter-request' for e in t.events))
        self.assertEqual(self.event(t,'A','file-path-handed-to-input-not-upload-proof')['selector_or_element_context'],'target-B')

    def test_26_same_path_latest_version_is_token_not_byte_upload_proof(self):
        t=race(same_file=True);e=self.event(t,'A','file-path-handed-to-input-not-upload-proof')
        self.assertEqual((e['requested_version'],e['latest_symbolic_version']),('version-A','version-B'))
        self.assertIs(e['browser_read_bytes_proved'],False);self.assertIs(t.summary()['file_bytes_read_or_uploaded_proved'],False)

    def test_27_distinct_file_keys_not_fix_for_shared_chat(self):
        t=race();e=self.event(t,'A','file-path-handed-to-input-not-upload-proof')
        self.assertEqual((e['latest_symbolic_version'],e['requested_target'],e['selector_or_element_context']),('version-A','target-A','target-B'))

    def test_28_zero_items_blocks_before_prepare_and_session(self):
        t=Trace().add('A','target-A','file-A','v-A',items=0).run_tail('A')
        self.assertEqual(t.requests['A']['stage'],'blocked-before-sender');self.assertEqual((t.files,t.dom),({},{}))

    def test_29_count_not_SaveResult_or_dirty_SDK_proof(self):
        self.assertTrue(caller_gate(1));self.assertFalse(caller_gate(0))
        for bad in (True,False,-1,101,1.0,'1'):
            with self.assertRaises(ValueError):caller_gate(bad)
        with self.assertRaises(TypeError):caller_gate(1,is_printed=True)
        self.assertFalse(self.witness()['saved_invoice_dirty_DTO_contract_proved'])

    def test_30_customer_and_mobile_guards_are_supplied_controls(self):
        for kwargs in (dict(customer_found=False),dict(mobile_present=False)):
            t=Trace().add('A','target-A','file-A','v-A',**kwargs).run_tail('A');self.assertFalse(t.files);self.assertFalse(t.dom)
        for kwargs in (dict(customer_found=1),dict(mobile_present=0)):
            with self.assertRaises(ValueError):caller_gate(1,**kwargs)

    def test_31_mapping_or_export_nonreturn_does_not_reach_sender(self):
        for kwargs in (dict(mapping_returned=False),dict(export_returned=False)):
            t=Trace().add('A','target-A','file-A','v-A',**kwargs).run_tail('A');self.assertFalse(t.dom);self.assertFalse(t.files)

    def test_32_chat_not_ready_false_before_caption(self):
        t=Trace().add('A','target-A','file-A','v-A');self.advance(t,'A',('prepare','navigate'));t.step('A','chat',ready=False)
        self.assertIs(t.requests['A']['result'],False);self.assertFalse(any(e['kind']=='caption-enter-request' for e in t.events))

    def test_33_missing_attach_after_caption_is_partial_boundary(self):
        t=Trace().add('A','target-A','file-A','v-A');self.advance(t,'A',('prepare','navigate','chat','caption-enter'));t.step('A','attach',ready=False)
        self.assertIs(t.requests['A']['result'],False);self.assertTrue(self.event(t,'A','caption-enter-request'));self.assertFalse(any(e['kind']=='file-path-handed-to-input-not-upload-proof' for e in t.events))

    def test_34_missing_file_after_caption_no_handoff(self):
        t=Trace().add('A','target-A','file-A','v-A');self.advance(t,'A',('prepare','navigate','chat','caption-enter','attach'));t.files.clear();t.step('A','file')
        self.assertIs(t.requests['A']['result'],False);self.assertFalse(any(e['kind']=='file-path-handed-to-input-not-upload-proof' for e in t.events))

    def test_35_no_send_button_after_file_input_not_Delivered(self):
        t=Trace().add('A','target-A','file-A','v-A');self.advance(t,'A',('prepare','navigate','chat','caption-enter','attach','file'));t.step('A','send',ready=False)
        self.assertTrue(self.event(t,'A','file-path-handed-to-input-not-upload-proof'));self.assertIs(t.requests['A']['result'],False);self.assertFalse(t.summary()['delivery_proved'])

    def test_36_captured_caption_element_NOT_silently_retargeted(self):
        t=pair();self.advance(t,'A',('prepare','navigate','chat'));self.advance(t,'B',('prepare','navigate'))
        t.step('A','caption-enter',ready=True)
        self.assertEqual(t.dom['sender-S'],'target-B');self.assertEqual(self.event(t,'A','caption-enter-request')['selector_or_element_context'],'target-A')

    def test_37_stale_element_flag_supplied_not_failure_induced(self):
        t=Trace().add('A','target-A','file-A','v-A');self.advance(t,'A',('prepare','navigate','chat'));t.step('A','caption-enter',ready=False)
        self.assertIs(t.requests['A']['result'],False);self.assertFalse(any(e['kind']=='caption-enter-request' for e in t.events))

    def test_38_local_true_click_delay_is_not_provider_or_delivery_receipt(self):
        t=Trace().add('A','target-A','file-A','v-A').run_tail('A')
        self.assertIs(t.requests['A']['result'],True);self.assertFalse(t.summary()['delivery_proved']);self.assertTrue(self.event(t,'A','generic-send-control-click-request'))

    def test_39_handles_reuse_vs_initialize_not_authentication_proof(self):
        self.assertEqual(session_route(present=True,handles_readable=True),'reuse-same-sender')
        self.assertEqual(session_route(present=False,handles_readable=False),session_route(present=True,handles_readable=False))
        for kwargs in (dict(present=1,handles_readable=True),dict(present=True,handles_readable=0)):
            with self.assertRaises(ValueError):session_route(**kwargs)

    def test_40_strict_tokens_flags_stage_and_request_bounds(self):
        for value in (None,1,'','x'*81,'x\n','/real/file','+966555'):
            with self.assertRaises(ValueError):token(value)
        t=Trace().add('A','target-A','file-A','v-A')
        for action in ('navigate','chat','unknown'):
            with self.assertRaises(ValueError):t.step('A',action)
        with self.assertRaises(ValueError):t.add('A','target-X','file-X','v-X')
        with self.assertRaises(ValueError):t.step('A','prepare',ready=1)
        for i in range(1,8):t.add('R'+str(i),'target-X','file-X','v-X')
        with self.assertRaises(ValueError):t.add('NINTH','target-X','file-X','v-X')

    def test_41_ACTUAL_LIVE34_versioned33_API15_parser(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B33_CLI['default'],'B33');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B34')
        p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B34')
        for part in ('A',)+tuple(f'B{n}' for n in range(1,35)):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
        for n in range(18,34):self.assertEqual(getattr(v,f'PHASE7_B{n}_CLI')['default'],f'B{n}')

    def test_42_ACTUAL_19_AST_gates_B33_history_before_current(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());raw=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(raw).hexdigest(),b34.DISPATCHER_SHA)
        tree=ast.parse(raw);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main)
        self.assertLess(body.index('historical_b32_validation('),body.index('historical_b33_validation('));self.assertLess(body.index('historical_b33_validation('),body.index('extend_messaging_request('));self.assertIn('extend_output_route(historical_b33,',body)
        actual=[set(ast.literal_eval(n.test.comparators[0])) for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part']
        expected=[{f'B{i}' for i in range(first,35)} for first in range(1,20)];self.assertEqual(actual,expected)
        for n in range(19):
            bad=copy.deepcopy(actual);bad[n].remove('B34')
            with self.assertRaises(AssertionError):self.assertEqual(bad,expected)
        block=next(n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'");self.assertIn('build_cli_parser().parse_args()',ast.unparse(block))

    def test_43_ALL52_launcher_local_restore_no_old_dispatcher_code(self):
        src=ast.unparse(ast.parse((A/'tools/run_historical_output_route_tests_07B34.py').read_text()))
        for text in ('suite.countTestCases() != 52','run.testsRun != 52 or run.skipped','loadTestsFromModule(historical_tests)','historical_tests.A = v.AUDIT','historical_tests.Path = type(v.AUDIT)','historical_tests.A = original_a','historical_tests.Path = original_path','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B33_CLI','b34.historical_b33_inputs('):self.assertIn(text,src)
        for text in ('unittest.skip','v.__file__ =','Path.read_bytes =','Path.open =','exec('):self.assertNotIn(text,src)

    def test_44_historical123_assertions_distinct_from_current127(self):
        prov=json.loads((A/'evidence/provenance-07B34.json').read_bytes());self.assertEqual(len(prov['historical_checker_sources_at_entry']),123);self.assertEqual(len(list((A/'tools').glob('*.py'))),127)
        raw=(A/b34.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));texts=json.loads((A/b34.SHARED_SNAPSHOT).read_bytes())['files'];before=v.AUDIT,v.read,v.rows;code,file=v.main.__code__,v.__file__;methods=Path.read_bytes,Path.read_text,Path.open,Path.glob
        with b34.historical_b33_inputs(v,old,texts,raw,prov['historical_checker_sources_at_entry'],(A/b34.DISPATCHER_SNAPSHOT).read_bytes()):
            self.assertEqual(len(list((v.AUDIT/'tools').glob('*.py'))),123);self.assertEqual(hashlib.sha256(type(v.AUDIT)(v.__file__).read_bytes()).hexdigest(),b34.DISPATCHER_SHA)
            with (v.AUDIT/'findings.csv').open(newline='') as f:self.assertEqual(list(csv.DictReader(f)),old)
            self.assertEqual((Path.read_bytes,Path.read_text,Path.open,Path.glob),methods);self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
        self.assertTrue(all(x is y for x,y in zip(before,(v.AUDIT,v.read,v.rows))))

    def test_45_protected1018_INCLUDES_registry_ALL335_raw336_potentials(self):
        prov=json.loads((A/'evidence/provenance-07B34.json').read_bytes());h=prov['historical_artifact_sha256'];self.assertEqual(len(h),1018);self.assertEqual(h['findings.csv'],b34.SNAPSHOT_SHA)
        self.assertNotIn('findings.csv',prov['declared_mutable_entry_paths']);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==v for n,v in h.items()))
        raw=(A/b34.SNAPSHOT).read_bytes();current=(A/'findings.csv').read_bytes();self.assertEqual(raw,current);rows=list(csv.DictReader(io.StringIO(raw.decode(),newline='')))
        self.assertEqual(b34.registry_preservation_errors(rows,rows,current,raw,self.table('historical-extensions')),[])
        for root in ('P4-014','P7-108','P7-132','P7-145'):self.assertEqual(next(r for r in rows if r['id']==root)['certainty'],'potential')

    def test_46_scope5_overlap5_union427_20contract_8context_dedup20(self):
        d=json.loads((A/'evidence/scope-decision-07B34.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(5,427,5,0,427,400))
        self.assertEqual((d['historical_metadata_screen_count'],d['parent_path_matched_metadata_rows'],d['selected_prior_report_sections'],d['selected_contract_slices'],d['exploratory_context_slices']),(335,33,20,20,8));self.assertFalse(d['all_historical_bodies_reviewed'])
        w=self.witness();self.assertEqual(w['whole_local_files_selected'],0)
        for key,declared in (('bounded_source_reads_not_semantic_coverage',SOURCE_SLICES),('exploratory_source_reads_not_capability_certification',EXPLORATORY_SLICES)):
            self.assertEqual(tuple((r['path'],r['start'],r['end']) for r in w[key]),declared)
            for r in w[key]:self.assertFalse(r['whole_local_file_selected']);self.assertEqual(hashlib.sha256((A.parents[1]/r['path']).read_bytes()).hexdigest(),r['sha256'])
        screen=json.loads((A/'evidence/dedup-screen-07B34.json').read_bytes());rows=list(csv.DictReader(io.StringIO((A/b34.SNAPSHOT).read_text(),newline='')));self.assertEqual(b34.dedup_errors(screen,rows),[])
        for key,value in (('all_historical_bodies_reviewed',True),('new_root_ids',['P7-164']),('selected_prior_finding_sections',[])):
            self.assertTrue(b34.dedup_errors(screen|{key:value},rows))

    def test_47_existing_P6_031_033_already_describe_interleaving_NO164(self):
        ad=self.table('root-adjudication');self.assertFalse(any(r['decision'] in ('new-local-root','extended-existing-root-not-new') for r in ad));self.assertEqual(self.table('historical-extensions'),[])
        self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='existing-mechanism-deepened-no-registry-change'],['P6-031;P6-033','P6-033']);self.assertTrue(all(r['comparison_depth']==b34.DEDUP_DEPTH for r in ad))
        text=(A/'PHASE-06.md').read_text();self.assertIn('والتداخل قد يغير chat/ملفاً أثناء العملية',text);self.assertIn('serial queue لكل session',text)
        rows=list(csv.DictReader((A/'findings.csv').open(newline='')));self.assertEqual(len(rows),335);self.assertEqual(rows[-1]['id'],'P7-163');self.assertNotIn('P7-164',{r['id'] for r in rows})

    def test_48_all_inputs_and_two_distinct_not_executed_plans_per_FE(self):
        self.assertEqual(b34.residual_errors(self.table('residual-disposition'),self.table('residual-disposition',33)),[]);self.assertEqual(b34.split_errors(self.table('split-register'),self.table('split-register',33)),[])
        data=[self.table(n) for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b34.current_link_errors(*data),[])
        for f in data[0]:
            linked=[t for t in data[2] if t['feature_ids']==f['id']];self.assertEqual(len(linked),2);self.assertNotEqual(linked[0]['acceptance_criterion'],linked[1]['acceptance_criterion'])
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertIn('إذن',t['prerequisites']);self.assertIn('not-executed',t['safety_controls'])
        for stem in ('handoffs','questions'):
            for old,new in zip(self.table(stem,33),self.table(stem)):self.assertTrue(new['required_redacted_input'].startswith(old['required_redacted_input']))

    def test_49_reference16_raw_clock_B33_capture3f747_delivery_dea_separate(self):
        prov=json.loads((A/'evidence/provenance-07B34.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B34.md').read_text();self.assertEqual(b34.date_identity_errors(prov,note),[])
        self.assertTrue(b34.date_identity_errors(prov|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b34.date_identity_errors(prov,note.replace(b34.B33_CHECK_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B33.json').read_bytes());self.assertEqual(old['checkout_head'],'3f747085b8f91762f7626dd45331ca1f5ba9e9c1');self.assertNotEqual(old['checkout_head'],b34.ENTRY)

    def test_50_synthetic39_schema_fixture_is_NOT_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b34.historical_record_errors(h),[])
        for key,value in (('registry_used','findings.csv'),('findings_total',336),('process_exit_code',True),('audit_checker_self_test_cases_reported',1190),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=value;self.assertTrue(b34.historical_record_errors(bad))
        for key,value in (('tests_reported',51),('historical_source_assertion_input_count',127),('test_module_Path_and_A_are_historical_assertion_inputs_only',1),('auxiliary_dispatcher_text_sha256','b'*64)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B33_child'][key]=value;self.assertTrue(b34.historical_record_errors(bad))
        self.assertTrue(b34.historical_record_errors(h|dict(historical_mode_count=True)))

    def test_51_ACTUAL39_archive127_single_inverse_pin_and_proof(self):
        p=A/'evidence/historical-mode-verification-07B34.json';raw=p.read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b34.HISTORICAL_RUN_SHA);self.assertEqual(b34.historical_record_errors(h),[])
        self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b34.ENTRY,v.HEAD,v.BRANCH));sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),127);self.assertEqual(b34.capture_source_errors(h,sources),[])
        for key in ('tools/validate_messaging_request_part.py','tools/test_messaging_request_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[key]+=b'\n';self.assertTrue(b34.capture_source_errors(h,changed))
        self.assertTrue(b34.capture_source_errors(h,{}));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']))
        self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        proof=json.loads((A/'evidence/capture-time-identity-07B34.json').read_bytes());self.assertEqual((proof['archive_bytes'],proof['archive_sha256'],proof['capture_tool_set_count'],proof['unchanged_capture_tool_count'],proof['raw_stdout_identities_temporarily_rechecked']),(len(raw),b34.HISTORICAL_RUN_SHA,127,126,39));self.assertTrue(proof['exact_inverse_reconstructs_capture_time_bytes']);self.assertFalse(proof['wholesale39_replayed_after_pin'])

    def test_52_actual127_AST_stdlib_and_protected_B33_records(self):
        tools=list((A/'tools').glob('*.py'));self.assertEqual(len(tools),127)
        for p in tools:ast.parse(p.read_text(),filename=str(p))
        tree=ast.parse((A/'tools/check_messaging_request_witnesses.py').read_text());imports=set()
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n,ast.ImportFrom):imports.add(n.module.split('.')[0])
        self.assertEqual(imports,{'__future__','hashlib','json','pathlib'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        h=json.loads((A/'evidence/provenance-07B34.json').read_bytes())['historical_artifact_sha256']
        for name in ('findings.csv','evidence/checks-07B33.json','evidence/official-capture-receipt-07B33.json','evidence/historical-mode-verification-07B33.json','evidence/capture-time-identity-07B33.json','evidence/output-route-witnesses-07B33.json','tools/test_output_route_audit_validator.py','tools/run_historical_editor_close_tests_07B33.py','DATE-IDENTITY-NOTE-07B33.md'):
            self.assertIn(name,h);self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),h[name])
        note=json.loads((A/'evidence/scope-preflight-correction-07B34.json').read_bytes())
        failed=(A/note['retained_failed_check']).read_bytes()
        self.assertEqual((note['process_exit_code'],note['error_count'],json.loads(failed)['error_count']),(1,31,31))
        self.assertEqual(hashlib.sha256(failed).hexdigest(),note['retained_stdout_sha256'])
        self.assertEqual(hashlib.sha256((A/b34.SCOPE_FILE).read_bytes()).hexdigest(),note['corrected_scope_sha256'])
        self.assertFalse(note['validator_or_test_code_changed']);self.assertTrue(note['check_is_not_integrated_CLI_or_unit_suite'])


if __name__=='__main__':
    unittest.main()
