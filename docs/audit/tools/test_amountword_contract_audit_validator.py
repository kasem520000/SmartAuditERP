#!/usr/bin/env python3
"""36 synthetic/read-only documentary cases, NOT amountword/ERP acceptance.

The earlier530 cases are unmodified; B20's32 use its explicit historical child
and parser preset. These cases independently inspect today's actual B21 default.
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

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_amountword_contract_part as b21
from validate_barcode_contract_part import historical_b19_inputs
from check_amountword_contract_witnesses import(mask_noncode,qualified_calls,manual_fixed_positions,manual_projection,manual_parse_boundary,manual_currency_family,manual_ordinal)

A=Path(__file__).parents[1]


class AmountwordContractAuditTests(unittest.TestCase):
    def old(self,n=310):return[dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()
    def current(self):return self.old()+[self.old(1)[0]|dict(id=n,next_phase='8')for n in b21.NEW_IDS]
    def texts(self):return{n:'FROZEN:'+n for n in b21.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b21.historical_b20_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def groups(self,end):return'\n'.join(f'| G-{n:02d} | exact |'for n in range(1,end+1))+'\n'
    def callers(self):
        literals=[];current=[]
        for n,(caller,amount,currency)in enumerate(b21.CALLER_SHAPES,1):
            path='SmartAuditERP/Class/Print.cs'if caller.startswith('Print.')else'SmartAuditERP/Form_WPF/'+caller+'.xaml.cs'
            a=dict(source_path=path,call_line_start=n,call_line_end=n,call_text_sha256=hashlib.sha256(str(n).encode()).hexdigest(),inert_argument_expression='"toy-'+str(n)+'"');literals.append(a)
            current.append(dict(**{k:str(x)for k,x in a.items()},caller=caller,amount_source=amount,word_currency_source=currency,report_amount_field='named local field',parse_or_projection_boundary='named boundary',owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='bounded followup',limit='not whole callgraph',runtime_status='not-executed'))
        return current,literals
    def contracts(self):
        features=[];invariants=[];tests=[]
        for n in range(1,19):
            fid=f'FE-{n:02d}';iid=f'INV-{n:02d}';roots=b21.NEW_IDS[n-1]if n<=3 else'H';accept=';'.join(f'T-{i:02d}'for i in(2*n-1,2*n));common=dict(finding_ids=roots,evidence='a.cs:1-2',acceptance_ids=accept)
            features.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='bounded action',**common));invariants.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in(2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=roots,plan_kind='finding-specific'if n<=3 else'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return features,invariants,tests
    def residuals(self):
        old=[dict(id=f'RS7B20-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',description='prior',required_redacted_input='upstream redacted')for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B20.csv',upstream_row_sha256=b21.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',owner_role='owner',required_redacted_input='upstream redacted; new source contract',impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B21-03',disposition='external-handoff',runtime_status='not-executed')for r in old]
        return new,old
    def work(self):
        statuses=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4e-amountwords-delivered-residuals-open']+['planned-not-started']*6
        work=[dict(part_family='7B'if i<4 else'7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false')for i,s in enumerate(statuses)]
        splits=[dict(title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='redacted',next_static_action='source trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed')for _ in range(3)]
        return work,splits
    def witness(self):return json.loads((A/'evidence/amountword-contract-witnesses-07B21.json').read_text())
    def history(self):
        """Synthetic26 schema fixture, NEVER evidence that26 modes actually ran."""
        h=json.loads((A/'evidence/historical-mode-verification-07B20.json').read_text())
        modes=copy.deepcopy(h['historical_modes'])
        modes.append(dict(mode='B20',process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,findings_total=310,registry_used=b21.SNAPSHOT,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,audit_checker_self_test_cases_reported=530,audit_checker_self_test_suite_count=21,stdout_sha256='a'*64,historical_B20_child=dict(tests_reported=32,expected_tests=32,process_exit_code=0,result='passed',historical_parser_cutoff='B20-not-current-B21-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_barcode_tests_07B21.py',no_test_skips_or_global_subprocess_or_path_patch=True)))
        return dict(historical_mode_count=26,historical_modes=modes,errors=[])
    def table(self,name):return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))

    def test_01_OWN310_rows_raw311CRLF_three_frozen_texts(self):
        f=self.fake()
        with self.context(f):self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()));self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
    def test_02_reject_nonexact_rows_raw_bytes_BOM_LF_text_keys(self):
        f=self.fake();old=self.old();raw=self.raw(old)
        for rs,texts,b in((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),(old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw),(old,self.texts(),bytearray(raw))):
            with self.assertRaises(ValueError):
                with b21.historical_b20_inputs(f,rs,texts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b21.historical_b20_inputs(f,old,self.texts(),self.raw(old)):pass
    def test_03_no_global_Path_or_unrelated_file_overlay(self):
        f=self.fake();before=Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,before);self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')]);self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_bytes()
    def test_04_copy_isolation_exception_restore_nested307(self):
        f=self.fake();old=self.old();texts=self.texts();saved=copy.deepcopy(old);before=f.AUDIT,f.read,f.rows
        with b21.historical_b20_inputs(f,old,texts,self.raw(old)):
            x=f.rows('findings.csv');x[0]['next_phase']='bad';self.assertEqual(f.rows('findings.csv'),saved)
            with historical_b19_inputs(f,self.old(307),self.texts(),self.raw(self.old(307))):self.assertEqual(len(f.rows('findings.csv')),307)
            self.assertEqual(len(f.rows('findings.csv')),310);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))));self.assertEqual(old,saved)
    def test_05_all310_fields_nextphase_evidence_rawprefix_preserved(self):
        old=self.old();cur=self.current();self.assertEqual(b21.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed';self.assertTrue(b21.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)
    def test_06_only_three_roots_raw314CRLF_noBOM(self):
        old=self.old();cur=self.current()
        for bad in(cur[:-1],cur+[dict(cur[-1])],cur[:310]+list(reversed(cur[310:]))):self.assertTrue(b21.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in(self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):self.assertTrue(b21.registry_preservation_errors(old,cur,raw,self.raw(old)))
    def test_07_exact_G195_append196through200_only(self):
        self.assertEqual(b21.group_row_errors(self.groups(195),self.groups(200)),[])
        for bad in(self.groups(199),self.groups(201),self.groups(200).replace('G-99','G-98'),self.groups(200).replace('| G-01 | exact','| G-01 | changed')):self.assertTrue(b21.group_row_errors(self.groups(195),bad))
    def test_08_mask_comments_ordinary_verbatim_char_strings_preserves_lines(self):
        text='// InvoiceOper.ToArabicLetter(1)\n/* InvoiceOper.ToArabicLetter(2) */\nvar a="InvoiceOper.ToArabicLetter(3)"; var b=@"quote "" InvoiceOper.ToArabicLetter(4)"; char c=\')\';\nInvoiceOper.ToArabicLetter(5);'
        masked=mask_noncode(text);self.assertEqual(len(masked),len(text));self.assertEqual(masked.count('\n'),text.count('\n'));self.assertEqual(len(qualified_calls(text,'toy.cs')),1)
        self.assertEqual(qualified_calls('$"InvoiceOper.ToArabicLetter(6)"','toy.cs'),[])
        for bad in('/* unfinished','"unfinished','@"unfinished'):
            with self.assertRaises(ValueError):mask_noncode(bad)
    def test_09_qualified_balanced_nested_args_line_hash_no_type_resolution(self):
        text='first\nInvoiceOper . ToArabicLetter(\n fn("a)\\\"", 2), /* ) */ currency);\n'
        rows=qualified_calls(text,'toy.cs');self.assertEqual(len(rows),1);r=rows[0];self.assertEqual((r['call_line_start'],r['call_line_end']),(2,3));self.assertIn('fn(',r['inert_argument_expression']);self.assertTrue(r['not_type_or_runtime_resolution'])
        call=text[text.index('InvoiceOper'):text.index(';')];self.assertEqual(r['call_text_sha256'],hashlib.sha256(call.encode()).hexdigest());self.assertEqual(qualified_calls('Other.ToArabicLetter(2)','toy.cs'),[])
        with self.assertRaises(ValueError):qualified_calls('InvoiceOper.ToArabicLetter(fn(','toy.cs')
    def test_10_exact12_caller_shapes_five_defaults_seven_explicit(self):
        cur,lit=self.callers();self.assertEqual(b21.caller_errors(cur,lit),[]);self.assertEqual(sum(r['word_currency_source'].startswith('default-')for r in cur),5);self.assertEqual(len({r['source_path']for r in cur}),11)
    def test_11_reject_caller_lineage_or_owner_empty_not_changed_prose(self):
        for key in('call_text_sha256','inert_argument_expression','source_path','call_line_start','caller','amount_source','word_currency_source','runtime_status'):
            cur,lit=self.callers();cur[0][key]='changed';self.assertTrue(b21.caller_errors(cur,lit),key)
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','report_amount_field','parse_or_projection_boundary','limit'):
            cur,lit=self.callers();cur[0][key]='';self.assertTrue(b21.caller_errors(cur,lit),key)
        cur,lit=self.callers();cur[0]['owner_role']='different nonempty owner';self.assertEqual(b21.caller_errors(cur,lit),[]);self.assertTrue(b21.caller_errors(cur[:-1],lit));lit[-1]=lit[0];self.assertTrue(b21.caller_errors(cur,lit))
    def test_12_ten_numeric_currency_branches_not_enum_or_new035(self):
        data=self.table('currency-branches-07B21.csv');self.assertEqual(b21.currency_branch_errors(data),[])
        for key in('numeric_local_branch_not_sdk_enum','arabic_major_family','arabic_minor_family','english_major_family','english_minor_family','finding_ids','runtime_status','adjudication','limit'):
            bad=copy.deepcopy(data);bad[0][key]='';self.assertTrue(b21.currency_branch_errors(bad),key)
        self.assertTrue(b21.currency_branch_errors(data[:-1]))
    def test_13_documentary_sentinel_not_fabricated_source_and_range_expansion(self):
        errors,calls=[],[];fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b21.validate_source(fake,dict(id='FE7B21-16',evidence=b21.DOCUMENTARY),{});self.assertEqual((errors,calls),([],[]))
        b21.validate_source(fake,dict(id='UNKNOWN',evidence=b21.DOCUMENTARY),{});self.assertEqual(len(errors),1)
        b21.validate_source(fake,dict(id='FE7B21-01',evidence='a.cs:1-2'),{});self.assertEqual(len(calls),2)
        b21.validate_source(fake,dict(id='FE7B21-16',evidence='a.cs:1-2'),{});self.assertEqual(len(errors),2)
        self.assertEqual(b21.expanded_source_evidence('a.cs:1-2;5;b.cs:7;9-10'),'a.cs:1-2;a.cs:5;b.cs:7;b.cs:9-10')
        for bad in('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:',' :1'):
            with self.assertRaises(ValueError):b21.expanded_source_evidence(bad)
    def test_14_FE18_INV18_T36_exact_bidirectional_roots_not_executed(self):
        self.assertEqual(b21.current_link_errors(*self.contracts()),[])
        for pool,key in((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            fs,iv,ts=self.contracts();(fs,iv,ts)[pool][0][key]='changed';self.assertTrue(b21.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();self.assertTrue(b21.current_link_errors(fs,iv,ts[:-1]))
    def test_15_distinct_invariants_criteria_and_feature_responsibilities(self):
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step'):
            fs,iv,ts=self.contracts();fs[0][key]='';self.assertTrue(b21.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b21.current_link_errors(fs,iv,ts));fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b21.current_link_errors(fs,iv,ts))
    def test_16_all14_residual_identity_hash_contract_old_input_responsibility(self):
        cur,old=self.residuals();self.assertEqual(b21.residual_errors(cur,old),[])
        for key in cur[0]:
            cur,old=self.residuals();cur[0][key]='';self.assertTrue(b21.residual_errors(cur,old),key)
        cur,old=self.residuals();cur[0]['required_redacted_input']='replacement-loses-old-input';self.assertTrue(b21.residual_errors(cur,old));cur,old=self.residuals();cur[0]['disposition']='approved';self.assertTrue(b21.residual_errors(cur,old));self.assertTrue(b21.residual_errors(cur[:-1],old))
    def test_17_bounded_R4e_six_C_unstarted_and_reasoned_three_splits(self):
        work,splits=self.work();self.assertEqual(b21.remaining_work_errors(work,splits),[])
        for i,key,value in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            work,splits=self.work();work[i][key]=value;self.assertTrue(b21.remaining_work_errors(work,splits))
        work,splits=self.work();splits[0]['reason_for_split']='';self.assertTrue(b21.remaining_work_errors(work,splits))
    def test_18_strict_false_true_integer_zero_counts_and_B10_erratum(self):
        self.assertEqual(b21.witness_metadata_errors(self.witness()),[])
        for key,value in(('application_code_imported_or_executed',0),('dotnet_or_visualbasic_format_parse_or_words_executed',None),('erp_runtime_tests_executed',False),('illustration_count',12.0),('B_R4e_bounded_not_whole7B_closure',1),('phase7C_started',True),('phase8_authorized_or_started',True)):
            self.assertTrue(b21.witness_metadata_errors(self.witness()|{key:value}))
        bad=self.witness();bad['retained_additive_B10_arithmetic_erratum']['reference_cost']=10;self.assertTrue(b21.witness_metadata_errors(bad))
    def test_19_saved_witness_genuine_hash_and_deterministic_readonly_recompute(self):
        p=A/'evidence/amountword-contract-witnesses-07B21.json';self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),b21.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_amountword_contract_witnesses.py')],capture_output=True,text=True,timeout=20)
        self.assertEqual(run.returncode,0,run.stderr);self.assertEqual(run.stderr,'');self.assertEqual(json.loads(run.stdout),self.witness());self.assertEqual(self.witness()['errors'],[])
    def test_20_genuine26_hash_and_schema_fixture_last310_historical32_null_not_zero(self):
        saved=(A/'evidence/historical-mode-verification-07B21.json').read_bytes()
        self.assertEqual(hashlib.sha256(saved).hexdigest(),b21.HISTORICAL_RUN_SHA)
        self.assertEqual(b21.historical_record_errors(json.loads(saved)),[])
        self.assertEqual(b21.historical_record_errors(self.history()),[])
        for n,key,value in((25,'findings_total',313),(25,'registry_used','findings.csv'),(25,'stdout_sha256','bad'),(25,'audit_checker_self_test_cases_reported',566),(0,'audit_checker_self_test_cases_reported',0),(0,'erp_runtime_tests_executed',False)):
            h=self.history();h['historical_modes'][n][key]=value;self.assertTrue(b21.historical_record_errors(h))
        h=self.history();h['historical_modes'][-1]['historical_B20_child']['all_original_cases_executed_unmodified']=False;self.assertTrue(b21.historical_record_errors(h));h=self.history();h['historical_modes']=h['historical_modes'][:-1];self.assertTrue(b21.historical_record_errors(h))
    def test_21_manual_unsigned12_position_magnitude_control(self):
        r=manual_fixed_positions('999999999999');self.assertEqual(r['selected_magnitude'],'999999999999');self.assertEqual(r['unread_tail'],'');self.assertEqual(manual_fixed_positions('000000000123')['selected_magnitude'],'123')
    def test_22_manual13_positions_lost_tail_and_distinct_inputs_collide(self):
        a,b=manual_fixed_positions('1000000000000'),manual_fixed_positions('1000000000001');self.assertEqual(a['selected_magnitude'],'100000000000');self.assertEqual(a['selected_magnitude'],b['selected_magnitude']);self.assertNotEqual(a['unread_tail'],b['unread_tail'])
    def test_23_manual_model_rejects_unpadded_signed_locale_decimal_or_scientific(self):
        for x in('123','-000000000001','١٠٠٠٠٠٠٠٠٠٠٠','100000000000.0','1E+12',' 100000000000',None):
            with self.assertRaises(ValueError):manual_fixed_positions(x)
    def test_24_manual_currency_projection_omission_not_enum_meaning(self):
        a,b=manual_projection('opaque-token',True),manual_projection('opaque-token',False);self.assertEqual(a['currency'],'opaque-token');self.assertEqual(b['currency'],'');self.assertEqual(a['arabic_currency_input'],b['arabic_currency_input']);self.assertEqual(a['english_currency_input'],b['english_currency_input'])
        with self.assertRaises(ValueError):manual_projection('opaque-token',1)
    def test_25_supplied_parse_failure_and_validzero_same_word_input_rawdiffers(self):
        a,b=manual_parse_boundary('bad',False),manual_parse_boundary('0',True,'0');self.assertEqual(a['word_numeric_input'],b['word_numeric_input']);self.assertNotEqual(a['BondVal'],b['BondVal']);self.assertFalse(a['parse_health_in_Bond']);self.assertEqual(manual_parse_boundary('bad',False,'not-parsed-at-all')['word_numeric_input'],'0')
    def test_26_supplied_parse_success_control_and_boolean_not_dotnet_parser(self):
        r=manual_parse_boundary('12.5',True,'12.5');self.assertEqual(r['BondVal'],r['word_numeric_input']);self.assertEqual(manual_parse_boundary('comma-not-interpreted',True,'12.5')['word_numeric_input'],'12.5')
        for raw,flag in((None,False),('1',0),('1','false')):
            with self.assertRaises(ValueError):manual_parse_boundary(raw,flag)
    def test_27_retained_numeric_currency_families_and_consistent2_control(self):
        for code in(4,12,13,15):
            r=manual_currency_family(code);self.assertNotEqual(r['arabic_major_family'],r['english_major_family'])
        r=manual_currency_family(2);self.assertEqual(r['arabic_major_family'],r['english_major_family']);self.assertEqual(r['arabic_minor_family'],r['english_minor_family'])
    def test_28_hypothetical_ordinal_not_actual_sdk_has_identity_counterexample(self):
        a,b=manual_ordinal([1,2,8],2),manual_ordinal([0,1,2],2);self.assertFalse(a['identity_preserved']);self.assertTrue(b['identity_preserved']);self.assertTrue(a['actual_sdk_enum_not_supplied']);self.assertEqual(a['persisted_index'],2)
        for n in(-1,3,False):
            with self.assertRaises(ValueError):manual_ordinal([0,1,2],n)
    def test_29_zero_signed_side_illustrations_keep_policy_and_runtime_limits(self):
        rows=self.witness()['illustrations'][9:12];self.assertEqual([r['id']for r in rows],['ALG7B21-10','ALG7B21-11','ALG7B21-12'])
        for r in rows:self.assertTrue(r['illustration_assertions_passed']);self.assertFalse(r['source_application_executed']);self.assertTrue(r['finding_ids'].startswith('H7B21-'));self.assertIn('policy',r['limit'])
        w=self.witness();self.assertFalse(w['dotnet_or_visualbasic_format_parse_or_words_executed']);self.assertTrue(w['unresolved_external_contracts_and_explicit_splits_retained'])
    def test_30_all310_preserved_prior034_035_and_potential014_132_no_extensions(self):
        previous=list(csv.DictReader(io.StringIO((A/b21.SNAPSHOT).read_text(),newline='')));current=list(csv.DictReader(io.StringIO((A/'findings.csv').read_text(),newline='')))
        self.assertEqual(current[:310],previous);self.assertTrue((A/'findings.csv').read_bytes().startswith((A/b21.SNAPSHOT).read_bytes()));lookup={r['id']:r for r in current}
        for n in('P7-034','P7-035'):self.assertEqual(lookup[n],next(r for r in previous if r['id']==n))
        for n in('P4-014','P7-132'):self.assertEqual(lookup[n]['certainty'],'potential')
        self.assertEqual(self.table('historical-extensions-07B21.csv'),[])
    def test_31_ACTUAL_B21_parser_versioned_B20_B19_B18_bases_API_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B16_CLI['default'],'B16');self.assertEqual(v.PHASE7_CURRENT_CLI['default'],'B17');self.assertEqual(v.PHASE7_B18_CLI['default'],'B18');self.assertEqual(v.PHASE7_B19_CLI['default'],'B19');self.assertEqual(v.PHASE7_B20_CLI['default'],'B20')
        p=v.build_cli_parser();self.assertEqual(p.parse_args([]).phase7_part,'B21');self.assertEqual(p.parse_args(['--through-phase','2']).through_phase,2)
        for part in('A','B15','B16','B17','B18','B19','B20','B21'):self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)
    def test_32_real_entrypoint_B20_context_before_current_and_B19_retained(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If)and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='main'));self.assertLess(body.index('historical_b20_validation('),body.index('extend_amountword_contracts('));self.assertIn('extend_barcode_contracts(historical_b20,',body);self.assertIn("phase7_part == 'B20'",body);self.assertIn('historical_b19_validation(',body)
        parsers=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='build_cli_parser'];self.assertEqual(len(parsers),1);self.assertIn('PHASE7_LIVE_CLI',ast.unparse(parsers[0]))
    def test_33_narrow_argv_redirect_keeps_unrelated_calls_and_all_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k))or'sentinel');proxy=b21.HistoricalB20Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=30)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in(proxy.expected+['--different'],['python','-B','/else/test_barcode_contract_audit_validator.py']):proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
    def test_34_facade_restore_no_global_subprocess_or_Path_mutation(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel');f=self.fake();f.subprocess=backend;f.sys=SimpleNamespace(executable='python');view=b21.HistoricalB20ValidatorView(f);real_run=subprocess.run;path_read=Path.read_bytes;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):self.assertIs(f.subprocess,backend);self.assertIs(subprocess.run,real_run);self.assertIs(Path.read_bytes,path_read);self.assertEqual(len(view.rows('findings.csv')),310);raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_35_historical_child_ALL32_original_no_skip_restores_and_protected_hashes(self):
        p=Path(__file__).parent;s=ast.unparse(ast.parse((p/'run_historical_barcode_tests_07B21.py').read_text()))
        for token in('loadTestsFromModule(historical_tests)','suite.countTestCases() != 32','result.testsRun != 32 or result.skipped','v.PHASE7_LIVE_CLI = original','v.PHASE7_B20_CLI'):self.assertIn(token,s)
        self.assertNotIn('unittest.skip',s);prov=json.loads((A/'evidence/provenance-07B21.json').read_text())
        for n in('test_barcode_contract_audit_validator.py','test_navigation_contract_audit_validator.py','test_caller_request_audit_validator.py','run_historical_navigation_tests_07B20.py','run_historical_caller_request_tests_07B19.py'):self.assertEqual(hashlib.sha256((p/n).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+n])
    def test_36_scope24_22overlap_2new_union412_not_census_or_completion(self):
        d=json.loads((A/'evidence/scope-decision-07B21.json').read_text());b=d['bookkeeping'];self.assertEqual((b['selected_paths'],b['prior_union'],b['overlap'],b['new'],b['union'],b['complement']),(24,410,22,2,412,415));self.assertEqual(sum(b['complement_kinds'].values()),415)
        self.assertEqual(d['selected_upstream_split'],'SP7B20-03');self.assertEqual((d['literal_qualified_arabic_calls'],d['literal_qualified_english_calls'],d['named_WPF_caller_paths']),(12,2,10));self.assertIs(d['phase7C_started'],False);self.assertIs(d['phase8_authorized_or_started'],False);self.assertIs(d['counts_are_completion_percent_or_sessions'],False)


if __name__=='__main__':unittest.main()
