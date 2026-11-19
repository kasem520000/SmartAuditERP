#!/usr/bin/env python3
"""28 documentary-helper cases; earlier434 cases remain frozen and unchanged.

Synthetic rows/text/models and audit-only parser/adapter APIs. NOT ERP tests,
no application imports/build/C#/SQL/WPF/SDK/Office/provider/interpreter/device,
secrets, real business data, remediation or operational measurement.
"""
from __future__ import annotations
import ast
import copy
import csv
import hashlib
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_caller_request_part as b18
from validate_consolidation_part import historical_b16_inputs
from check_caller_request_witnesses import split_arguments,extract_calls,party_filter,first_key


class CallerRequestAuditTests(unittest.TestCase):
    def old(self,n=300):
        return [dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
            type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]

    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()

    def current(self):return self.old()+[self.old(1)[0]|dict(id=f'P7-{i}',next_phase='8')for i in(129,130)]
    def texts(self):return {n:'FROZEN:'+n for n in b18.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b18.historical_b17_inputs(f,self.old(),self.texts(),self.raw(self.old()))

    def ledger(self):
        current=[];expected=[]
        modes=[m for m,n in b18.ROLE_COUNTS.items()for _ in range(n)]
        for i,mode in enumerate(modes):
            path=f'fake/{i%10}.cs';args=['7','5','22'if mode not in{'all-party-item-command','selected-party-id-omitted'}else'-1','1']
            actual=dict(source_path=path,call_line_start=i+1,call_line_end=i+1,call_text_sha256=hashlib.sha256(str(i).encode()).hexdigest(),lexical_args=args);expected.append(actual)
            roots='P7-130'if mode=='selected-party-id-omitted'else'P7-122;P7-059'if mode=='all-party-item-command'else'P7-129'
            current.append(dict(id=f'CL-{i:02d}',**{k:str(actual[k])for k in actual if k!='lexical_args'},
                lexical_args_json=__import__('json').dumps(args),party_mode=mode,forwarded_party_id=args[2],forwarded_party_kind=args[3],finding_ids=roots,runtime_status='not-executed',reachability_limit='not all callgraph'))
        return current,expected,477

    def contracts(self):
        mapping=[1]*5+[2]*2+list(range(3,13))+[13]*2+[14]*5
        tests=[dict(id=f'T-{i:02d}',feature_ids=f'FE-{n:02d}',invariant_ids=f'INV-{n:02d}',finding_ids=f'P7-{128+n}'if n<=2 else'H',
            plan_kind='finding-specific'if n<=2 else'documentary-scope-or-authorization-gate',status='not-executed',acceptance_criterion='criterion'+str(i))for i,n in enumerate(mapping,1)]
        features=[];invariants=[]
        for n in range(1,15):
            common=dict(finding_ids=f'P7-{128+n}'if n<=2 else'H',evidence='a.cs:1-2',acceptance_ids=';'.join(t['id']for t in tests if t['feature_ids']==f'FE-{n:02d}'))
            features.append(dict(id=f'FE-{n:02d}',**common));invariants.append(dict(id=f'INV-{n:02d}',feature_ids=f'FE-{n:02d}',required_invariant='invariant'+str(n),**common))
        return features,invariants,tests

    def residual(self):
        up=[dict(id=f'RS7B17-{i:02d}',upstream_contract_ids=f'H-OLD-{i};Q-OLD-{i}',description='prior')for i in range(1,15)]
        cur=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B17.csv',upstream_row_sha256=b18.row_sha(r),
            upstream_contract_ids=r['upstream_contract_ids'],disposition='external-handoff',local_result='bounded result',owner_role='owner',required_redacted_input='redacted input',
            impact_if_unavailable='acceptance blocked',next_step='named followup',static_exit_criterion='source-bound disposition',current_handoff_or_split_ids='H7B18-01',runtime_status='not-executed')for r in up]
        return cur,up

    def work(self):
        statuses=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4b-direct-callers-delivered-residuals-open']+['planned-not-started']*6
        work=[dict(part_family='7B'if i<4 else'7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false')for i,s in enumerate(statuses)]
        splits=[dict(title='static split',candidate_scope_not_certified='named capability',reason_for_split='bounded scope',owner_role='owner',required_input='redacted map',next_static_action='source trace',static_exit_criterion='reasoned disposition',status='explicit-further-static-split-not-started',runtime_status='not-executed')for _ in range(3)]
        return work,splits

    def metadata(self):
        return dict(phase='7B18-partial-static-direct-caller-requests',application_code_imported_or_executed=False,application_remediation_performed=False,
            real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,
            erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=12,static_lexical_contract_check_count=12,
            B_R4b_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,
            retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False))

    def test_01_OWN300_exact_rows_indexes_and_raw301CRLF(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')

    def test_02_no_global_patch_or_unrelated_registry_overlay(self):
        f=self.fake();method=Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,method);self.assertEqual((f.AUDIT/'x'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(f.rows('other/findings.csv'),[dict(id='LIVE:other/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/elsewhere/findings.csv').read_bytes()

    def test_03_normal_exception_restore_all_identities(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):pass
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_04_wrong_counts_and_duplicates_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in(self.old(299),self.old(302),duplicate):
            with self.assertRaises(ValueError):
                with b18.historical_b17_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass

    def test_05_exact_CRLF_noBOM_trailing_rows_disagreement(self):
        raw=self.raw(self.old())
        for bad in(None,'text',b'\xef\xbb\xbf'+raw,raw.replace(b'\r\n',b'\n'),raw+b'\r',raw+b'\r\n',raw.replace(b'synthetic',b'changed',1),b'\xff'):
            with self.assertRaises(ValueError):
                with b18.historical_b17_inputs(self.fake(),self.old(),self.texts(),bad):pass

    def test_06_exact_index_keys_copies_and_failed_entry_restore(self):
        for texts in({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            f=self.fake();before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b18.historical_b17_inputs(f,self.old(),texts,self.raw(self.old())):pass
            self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))
        f=self.fake();old=self.old();texts=self.texts()
        with b18.historical_b17_inputs(f,old,texts,self.raw(old)):
            texts['PLAN.md']='changed';f.rows('findings.csv')[0]['title']='changed'
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md');self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic')

    def test_07_nested_B16_OWN299_exception_back_to300(self):
        f=self.fake();inner=self.old(299)
        with self.context(f):
            with self.assertRaises(RuntimeError):
                with historical_b16_inputs(f,inner,self.texts(),self.raw(inner)):
                    self.assertEqual(len(f.rows('findings.csv')),299);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(inner));raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),300);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))

    def test_08_ALL300_fields_rawprefix_and_only_two_new_roots(self):
        old,cur=self.old(),self.current();raw,frozen=self.raw(cur),self.raw(old)
        self.assertEqual(b18.registry_preservation_errors(old,cur,raw,frozen),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]+='changed';self.assertTrue(b18.registry_preservation_errors(old,bad,self.raw(bad),frozen))
        for bad in(raw+b'\r',b'\xef\xbb\xbf'+raw,raw.replace(b'\r\n',b'\n')):self.assertTrue(b18.registry_preservation_errors(old,cur,bad,frozen))
        self.assertTrue(b18.registry_preservation_errors(old,cur[::-1],self.raw(cur[::-1]),frozen))

    def test_09_G180_exact_rows_not_substring_presence(self):
        old='\n'.join(f'| G-{n:02d} | exact |'for n in range(1,181))+'\n'
        self.assertEqual(b18.group_row_errors(old,old+'| G-181 | new |\n'),[])
        self.assertTrue(b18.group_row_errors(old,old.replace('| G-06 | exact','| G-06 | changed')+old))

    def test_10_balanced_inert_args_nested_commas_and_quotes(self):
        self.assertEqual(split_arguments('a[Get(1, 2)], f("x,y"), -1, 1'),['a[Get(1, 2)]','f("x,y")','-1','1'])

    def test_11_exact_literal_line_end_args_and_sha(self):
        text='// text\nfrm.LastProcess(7,\n 5, 22, 1);\n';call=extract_calls(text)[0]
        self.assertEqual((call['call_line_start'],call['call_line_end']),(2,3));self.assertEqual(call['lexical_args'],['7','5','22','1'])
        self.assertEqual(call['call_text_sha256'],hashlib.sha256('frm.LastProcess(7,\n 5, 22, 1)'.encode()).hexdigest())
        self.assertEqual(extract_calls('LastProcess(7,5,22,1);'),[]) # NOT all callgraph.

    def test_12_invalid_inert_input_not_evaluated(self):
        for bad in('7,,1,1','f(7, 1','7,]','"unterminated'):
            with self.assertRaises(ValueError):split_arguments(bad)
        with self.assertRaises(ValueError):extract_calls('frm.LastProcess(7, 5, 22, 1')

    def test_13_positive_ID_wrong_kind_conditional_lookup_loss(self):
        parties=[(11,1),(22,2)];records=[('other',11,5,1),('target',22,5,2)]
        self.assertIsNone(party_filter(22,1,parties));self.assertEqual(first_key(records,party_filter(22,1,parties)),'other')
        self.assertEqual(first_key(records,party_filter(22,2,parties)),'target')

    def test_14_type3_masks_and_matching_InvPurch_not_every_request_fails(self):
        parties=[(11,1),(22,2),(33,3)]
        self.assertEqual(party_filter(33,1,parties),party_filter(33,2,parties));self.assertEqual(party_filter(22,2,parties),22)
        with self.assertRaises(ValueError):party_filter(22,9,parties)

    def test_15_missing_ID_independent_of_kind_general_sentinel_legitimate(self):
        self.assertIsNone(party_filter(-1,1,[(11,1)]));self.assertIsNone(party_filter(-1,2,[(11,1)]))
        self.assertEqual(party_filter(11,1,[(11,1)]),11)
        records=[('S',22,5,1),('C',11,5,2)]
        self.assertEqual(first_key(records,None),'S');self.assertEqual(first_key(records,11),'C');self.assertIsNone(first_key(records,44))

    def test_16_party_kind_correction_does_not_fix_store_or_order(self):
        records=[('outside-old',22,9,1),('inside-old',22,5,2),('inside-new',22,5,3),('outside-new',22,8,4)]
        self.assertEqual(first_key(records,22),'outside-old');self.assertEqual(first_key(records,22,5),'inside-old')
        self.assertEqual(first_key(records,22,5,True),'inside-new');self.assertEqual(first_key(records,22,None,True),'outside-new')

    def test_17_exact_ledger_lineage_19_calls_10_paths(self):self.assertEqual(b18.ledger_errors(*self.ledger()),[])

    def test_18_ledger_missing_duplicate_reorder_args_hash_or_location_rejected(self):
        cur,exp,scanned=self.ledger()
        for bad in(cur[:-1],cur+[cur[0]],cur[::-1]):self.assertTrue(b18.ledger_errors(bad,exp,scanned))
        for key in('source_path','call_line_start','call_line_end','call_text_sha256','lexical_args_json','forwarded_party_id','forwarded_party_kind'):
            bad=copy.deepcopy(cur);bad[0][key]='bad';self.assertTrue(b18.ledger_errors(bad,exp,scanned))

    def test_19_context_root_mode_and_runtime_not_inferred_from_count(self):
        cur,exp,n=self.ledger()
        for patch in({'party_mode':'complete'},{'finding_ids':'P7-130'},{'runtime_status':'passed'},{'reachability_limit':''}):
            bad=copy.deepcopy(cur);bad[0]|=patch;self.assertTrue(b18.ledger_errors(bad,exp,n))
        self.assertTrue(b18.ledger_errors(cur,exp,491))

    def test_20_FE_INV_T_exact_bidirectional_and_two_root_plans(self):self.assertEqual(b18.current_link_errors(*self.contracts()),[])

    def test_21_wrong_lineage_execution_duplicate_criterion_or_wrong_cause(self):
        for key in('feature_ids','finding_ids','evidence','acceptance_ids'):
            fe,inv,tests=self.contracts();inv[0][key]='wrong';self.assertTrue(b18.current_link_errors(fe,inv,tests))
        for patch in({'status':'passed'},{'finding_ids':'P7-130'},{'feature_ids':'FE-02'}):
            fe,inv,tests=self.contracts();tests[0]|=patch;self.assertTrue(b18.current_link_errors(fe,inv,tests))
        fe,inv,tests=self.contracts();tests[1]['acceptance_criterion']=tests[0]['acceptance_criterion'];self.assertTrue(b18.current_link_errors(fe,inv,tests))

    def test_22_all14_residuals_exact_lineage_order_and_hash(self):
        cur,up=self.residual();self.assertEqual(b18.residual_errors(cur,up),[])
        for bad in(cur[:-1],cur+[cur[0]],cur[::-1]):self.assertTrue(b18.residual_errors(bad,up))
        cur[0]['upstream_row_sha256']='bad';self.assertTrue(b18.residual_errors(cur,up))

    def test_23_residual_owner_input_impact_step_exit_not_approval(self):
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            cur,up=self.residual();cur[0][key]=' ';self.assertTrue(b18.residual_errors(cur,up))
        for patch in({'disposition':'complete'},{'runtime_status':'passed'}):
            cur,up=self.residual();cur[0]|=patch;self.assertTrue(b18.residual_errors(cur,up))

    def test_24_R4b_residuals_and_six_C_unstarted_explicit_split_reason(self):
        work,splits=self.work();before=copy.deepcopy(work);self.assertEqual(b18.remaining_work_errors(work,splits),[]);self.assertEqual(work,before)
        for i,key,value in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            work,splits=self.work();work[i][key]=value;self.assertTrue(b18.remaining_work_errors(work,splits))
        for key in('candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            work,splits=self.work();splits[0][key]=' ';self.assertTrue(b18.remaining_work_errors(work,splits))

    def test_25_strict_metadata_boolean_integer_and_additive_erratum(self):
        self.assertEqual(b18.witness_metadata_errors(self.metadata()),[])
        for key,value in(('application_code_imported_or_executed',0),('erp_runtime_tests_executed',False),('phase7C_started',True),('phase8_authorized_or_started',None),('B_R4b_bounded_not_whole7B_closure',1),('illustration_count',12.0)):
            self.assertTrue(b18.witness_metadata_errors(self.metadata()|{key:value}))
        bad=self.metadata();bad['retained_additive_B10_arithmetic_erratum']['local_cost']=20;self.assertTrue(b18.witness_metadata_errors(bad))

    def test_26_declared_metadata_sentinels_vs_real_scoped_source(self):
        errors,calls=[],[];fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b18.validate_source(fake,dict(id='FE7B18-10',evidence=b18.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b18.validate_source(fake,dict(id='UNKNOWN',evidence=b18.DOCUMENTARY),{});self.assertEqual(len(errors),1)
        b18.validate_source(fake,dict(id='FE7B18-01',evidence='a.cs:1-2'),{});self.assertEqual(len(calls),2)
        b18.validate_source(fake,dict(id='FE7B18-10',evidence='a.cs:1-2'),{});self.assertEqual(len(errors),2)

    def test_27_ACTUAL_parser_B18_legacy_B17_base_B16_option_B15_API(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B16_CLI['default'],'B16');self.assertEqual(v.PHASE7_CURRENT_CLI['default'],'B17')
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B18')
        for n in('A','B15','B16','B17','B18'):self.assertEqual(parser.parse_args(['--phase7-part',n]).phase7_part,n)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)

    def test_28_entrypoint_uses_actual_parser_not_only_compatibility_descriptor(self):
        tree=ast.parse(Path(v.__file__).read_text())
        blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);text=ast.unparse(blocks[0])
        self.assertIn('build_cli_parser().parse_args()',text);self.assertIn('main(args.through_phase, args.phase7_part)',text)
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser']
        self.assertEqual(len(funcs),1);self.assertIn('PHASE7_LIVE_CLI',ast.unparse(funcs[0]))


if __name__=='__main__':unittest.main()
