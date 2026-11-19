#!/usr/bin/env python3
"""40 read-only documentary cases, NOT item/import/pricing/ERP acceptance.

All prior566 cases remain unmodified. B21 ALL36 run under explicit historical
presetB21, alongside B20/32,B19/36,B18/28 children. These cases independently
inspect today's actual B22 parser/entrypoint, provenance and inert models.
No application imports, production data, protected edits/skips/global patches.
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

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_contract_item_part as b22
from validate_amountword_contract_part import historical_b20_inputs
from check_contract_item_witnesses import (
    supplied_price_projection, supplied_dialog_transition,
    supplied_import_projection, supplied_stable_entry_guard)
from check_amountword_contract_witnesses import mask_noncode, qualified_calls

A = Path(__file__).resolve().parents[1]


class ContractItemAuditTests(unittest.TestCase):
    def old(self, n=313):
        return [dict(id=f'PX-{i:03d}', title='synthetic', severity='High',
                     certainty='potential', type='synthetic-only',
                     status='open-not-remediated', next_phase='7;8',
                     evidence='a.cs:1-2') for i in range(n)]

    def raw(self, data):
        s = io.StringIO(newline='')
        w = csv.DictWriter(s, fieldnames=list(data[0]), lineterminator='\r\n')
        w.writeheader(); w.writerows(data)
        return s.getvalue().encode()

    def current(self):
        return self.old()+[self.old(1)[0] | dict(id=n, next_phase='8') for n in b22.NEW_IDS]

    def texts(self):
        return {n:'FROZEN:'+n for n in b22.SHARED_DOCS}

    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'),
            read=lambda p:'LIVE:'+str(p), rows=lambda n:[dict(id='LIVE:'+n)])

    def context(self, fake):
        return b22.historical_b21_inputs(fake,self.old(),self.texts(),self.raw(self.old()))

    def groups(self, end):
        return '\n'.join(f'| G-{n:02d} | exact |' for n in range(1,end+1))+'\n'

    def table(self, name):
        return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))

    def contracts(self):
        features=[]; invariants=[]; tests=[]
        for n in range(1,19):
            fid=f'FE-{n:02d}'; iid=f'INV-{n:02d}'
            roots=b22.NEW_IDS[n-1] if n<=3 else 'H'
            accept=';'.join(f'T-{i:02d}' for i in (2*n-1,2*n))
            common=dict(finding_ids=roots,evidence='a.cs:1-2',acceptance_ids=accept)
            features.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',
                impact_if_unavailable='blocked',next_step='bounded action',**common))
            invariants.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in (2*n-1,2*n):
                tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,
                    finding_ids=roots,plan_kind='finding-specific' if n<=3 else 'documentary',
                    status='not-executed',acceptance_criterion='criterion'+str(i)))
        return features,invariants,tests

    def residuals(self):
        old=[dict(id=f'RS7B21-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',
            description='prior',required_redacted_input='upstream redacted',
            disposition='external-handoff',current_handoff_or_split_ids='H7B21-03')
            for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],
            upstream_artifact='evidence/residual-disposition-07B21.csv',
            upstream_row_sha256=b22.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],
            local_result='bounded result',owner_role='owner',
            required_redacted_input='upstream redacted; new source contract',
            impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',
            current_handoff_or_split_ids='H7B22-03',disposition='external-handoff',
            runtime_status='not-executed') for r in old]
        return new,old

    def splits(self):
        old=[dict(id=f'SP7B21-{n:02d}',required_input='upstream redacted') for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B21.csv',
            upstream_row_sha256=b22.row_sha(r),title='named split',
            candidate_scope_not_certified='bounded capability',reason_for_split='bounded reason',
            owner_role='owner',required_input='upstream redacted; new contract',
            next_static_action='source trace',static_exit_criterion='exit',
            status='explicit-further-static-split-not-started',runtime_status='not-executed') for r in old]
        return new,old

    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+[
            'bounded-shared-contract-delivered-residuals-open',
            'bounded-R4f-contract-items-delivered-residuals-open']+['planned-not-started']*6
        return [dict(part_family='7B' if n<4 else '7C',status=s,runtime_status='not-executed',
            counts_are_sessions_or_completion_percent='false') for n,s in enumerate(states)]

    def witness(self):
        return json.loads((A/'evidence/contract-item-witnesses-07B22.json').read_text())

    def history_fixture(self):
        """Synthetic27 schema fixture; NEVER evidence that27 modes really ran."""
        h=json.loads((A/'evidence/historical-mode-verification-07B21.json').read_text())
        modes=copy.deepcopy(h['historical_modes'])
        modes.append(dict(mode='B21',process_exit_code=0,validation_errors=[],
            original_project_hashes_matching=827,findings_total=313,registry_used=b22.SNAPSHOT,
            erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
            audit_checker_self_test_cases_reported=566,audit_checker_self_test_suite_count=22,
            stdout_sha256='a'*64,historical_B21_child=dict(tests_reported=36,expected_tests=36,
                process_exit_code=0,result='passed',historical_parser_cutoff='B21-not-current-B22-default',
                all_original_cases_executed_unmodified=True,
                dedicated_child_launcher='tools/run_historical_amountword_tests_07B22.py',
                no_test_skips_or_global_subprocess_or_path_patch=True)))
        return dict(historical_mode_count=27,historical_modes=modes,errors=[])

    def lines(self, last=False):
        a=dict(code='A',index=2 if last else 1,quantity='4',price='10',description='old-A')
        b=dict(code='B',index=1 if last else 2,quantity='2',price='20',description='old-B')
        return [b,a] if last else [a,b]

    def imported(self):
        return dict(code='A',quantity='7',price='50',description='import-A')

    def test_01_OWN313_rows_raw314CRLF_three_frozen_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old())
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_reject_nonexact_rows_raw_BOM_LF_text_keys(self):
        f=self.fake(); old=self.old(); raw=self.raw(old)
        for rs,texts,b in ((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),
            (old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw),
            (old,self.texts(),bytearray(raw))):
            with self.assertRaises(ValueError):
                with b22.historical_b21_inputs(f,rs,texts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b22.historical_b21_inputs(f,old,self.texts(),self.raw(old)):pass

    def test_03_no_global_Path_or_unrelated_file_overlay(self):
        f=self.fake(); before=Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,before)
            self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_bytes()

    def test_04_exception_restoration_and_nested_OWN310(self):
        f=self.fake(); before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b20_inputs(f,self.old(310),self.texts(),self.raw(self.old(310))):
                self.assertEqual(len(f.rows('findings.csv')),310)
            self.assertEqual(len(f.rows('findings.csv')),313)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_05_copy_isolation_of_rows_and_shared_texts(self):
        f=self.fake(); old=self.old(); texts=self.texts(); saved=copy.deepcopy(old)
        with b22.historical_b21_inputs(f,old,texts,self.raw(old)):
            x=f.rows('findings.csv'); x[0]['next_phase']='bad'
            self.assertEqual(f.rows('findings.csv'),saved)
            self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
        self.assertEqual(old,saved); self.assertEqual(texts,self.texts())

    def test_06_all313_fields_ALLnextphase_evidence_rawprefix(self):
        old=self.old(); cur=self.current()
        self.assertEqual(b22.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur); bad[0][key]='changed'
            self.assertTrue(b22.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)

    def test_07_only142_143_144_raw317CRLF_noBOM(self):
        old=self.old(); cur=self.current()
        for bad in (cur[:-1],cur+[dict(cur[-1])],cur[:313]+list(reversed(cur[313:]))):
            self.assertTrue(b22.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in (self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):
            self.assertTrue(b22.registry_preservation_errors(old,cur,raw,self.raw(old)))

    def test_08_exact_G200_append201through205_only(self):
        self.assertEqual(b22.group_row_errors(self.groups(200),self.groups(205)),[])
        for bad in (self.groups(204),self.groups(206),self.groups(205).replace('G-99','G-98'),
                    self.groups(205).replace('| G-01 | exact','| G-01 | changed')):
            self.assertTrue(b22.group_row_errors(self.groups(200),bad))

    def test_09_source_sentinel_and_same_file_range_expansion(self):
        errors=[]; calls=[]
        fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,
            evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b22.validate_source(fake,dict(id='FE7B22-16',evidence=b22.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]))
        b22.validate_source(fake,dict(id='UNKNOWN',evidence=b22.DOCUMENTARY),{})
        b22.validate_source(fake,dict(id='FE7B22-16',evidence='a.cs:1-2'),{})
        self.assertEqual(len(errors),2); self.assertEqual(len(calls),2)
        self.assertEqual(b22.expanded_source_evidence('a.cs:1-2;5;b.cs:7;9-10'),
                         'a.cs:1-2;a.cs:5;b.cs:7;b.cs:9-10')
        for bad in ('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:',' :1'):
            with self.assertRaises(ValueError):b22.expanded_source_evidence(bad)

    def test_10_EN8_UP8_order_stable_guard_and_support_limits(self):
        en=self.table('entry-reachability-07B22.csv'); up=self.table('unit-price-lineage-07B22.csv')
        self.assertEqual(b22.ledger_errors(en,up),[])
        for rows in (en,up):
            bad=copy.deepcopy(rows); bad[0],bad[1]=bad[1],bad[0]
            self.assertTrue(b22.ledger_errors(bad,up) if rows is en else b22.ledger_errors(en,bad))
        for n in (2,3,7):
            bad=copy.deepcopy(en); bad[n]['reachability_observation']='actually-scanned-and-supported'
            self.assertTrue(b22.ledger_errors(bad,up))

    def test_11_ledger_responsibility_not_vacuous_or_runtime(self):
        en=self.table('entry-reachability-07B22.csv'); up=self.table('unit-price-lineage-07B22.csv')
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step',
                    'limit','feature_ids','finding_ids','evidence','runtime_status'):
            bad=copy.deepcopy(en); bad[0][key]=''
            self.assertTrue(b22.ledger_errors(bad,up),key)
        self.assertTrue(b22.ledger_errors(en[:-1],up))
        bad=copy.deepcopy(up); bad[3]['observation']='resolver026-only'
        self.assertTrue(b22.ledger_errors(en,bad))

    def test_12_FE18_INV18_T36_bidirectional_roots_not_executed(self):
        self.assertEqual(b22.current_link_errors(*self.contracts()),[])
        for pool,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),
                         (2,'status'),(2,'finding_ids')):
            parts=self.contracts(); parts[pool][0][key]='changed'
            self.assertTrue(b22.current_link_errors(*parts),key)
        fs,iv,ts=self.contracts(); self.assertTrue(b22.current_link_errors(fs,iv,ts[:-1]))

    def test_13_distinct_invariants_criteria_and_feature_responsibilities(self):
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step'):
            fs,iv,ts=self.contracts(); fs[0][key]=''
            self.assertTrue(b22.current_link_errors(fs,iv,ts),key)
        fs,iv,ts=self.contracts(); ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion']
        self.assertTrue(b22.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts(); iv[1]['required_invariant']=iv[0]['required_invariant']
        self.assertTrue(b22.current_link_errors(fs,iv,ts))

    def test_14_all14_residual_ancestor_rowhash_contract_ids(self):
        cur,old=self.residuals(); self.assertEqual(b22.residual_errors(cur,old),[])
        for key in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            cur,old=self.residuals(); cur[0][key]='changed'
            self.assertTrue(b22.residual_errors(cur,old),key)
        self.assertTrue(b22.residual_errors(cur[:-1],old))

    def test_15_residual_inputs_responsibility_disposition_mapping_not_approved(self):
        for key in ('local_result','owner_role','required_redacted_input','impact_if_unavailable',
                    'next_step','static_exit_criterion','current_handoff_or_split_ids'):
            cur,old=self.residuals(); cur[0][key]=''
            self.assertTrue(b22.residual_errors(cur,old),key)
        for key,value in (('required_redacted_input','lost-upstream-input'),('disposition','approved'),
                          ('runtime_status','passed'),('current_handoff_or_split_ids','H7B22-06')):
            cur,old=self.residuals(); cur[0][key]=value
            self.assertTrue(b22.residual_errors(cur,old),key)

    def test_16_three_splits_exact_ancestor_inputs_and_reasoned_not_started(self):
        cur,old=self.splits(); self.assertEqual(b22.split_errors(cur,old),[])
        for key in cur[0]:
            cur,old=self.splits(); cur[0][key]=''
            self.assertTrue(b22.split_errors(cur,old),key)
        cur,old=self.splits(); cur[0]['required_input']='replacement loses prior'
        self.assertTrue(b22.split_errors(cur,old)); self.assertTrue(b22.split_errors(cur[:-1],old))

    def test_17_boundedR4f_fourB_sixC_unstarted_no_sessions_percentage(self):
        self.assertEqual(b22.remaining_work_errors(self.work()),[])
        for n,key,value in ((3,'status','complete'),(4,'status','in-progress'),
            (0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true'),
            (0,'part_family','7C')):
            work=self.work(); work[n][key]=value
            self.assertTrue(b22.remaining_work_errors(work),key)
        self.assertTrue(b22.remaining_work_errors(self.work()[:-1]))

    def test_18_strict_boolean_integer_metadata_and_additiveB10_erratum(self):
        self.assertEqual(b22.witness_metadata_errors(self.witness()),[])
        for key,value in (('application_code_imported_or_executed',0),
            ('dotnet_wpf_sql_or_excel_executed',None),('erp_runtime_tests_executed',False),
            ('illustration_count',12.0),('B_R4f_bounded_not_whole7B_closure',1),
            ('phase7C_started',True),('phase8_authorized_or_started',True)):
            self.assertTrue(b22.witness_metadata_errors(self.witness() | {key:value}),key)
        bad=self.witness(); bad['retained_additive_B10_arithmetic_erratum']['reference_cost']=10
        self.assertTrue(b22.witness_metadata_errors(bad))

    def test_19_actual_witness_stdout_hash_and_deterministic_readonly_recompute(self):
        p=A/'evidence/contract-item-witnesses-07B22.json'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),b22.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_contract_item_witnesses.py')],
            capture_output=True,text=True,timeout=25)
        self.assertEqual(run.returncode,0,run.stderr); self.assertEqual(run.stderr,'')
        self.assertEqual(json.loads(run.stdout),self.witness()); self.assertEqual(self.witness()['errors'],[])

    def test_20_genuine27_capture_and_separate_synthetic_fixture_OWN313_ALL36_null_not_zero(self):
        saved=(A/'evidence/historical-mode-verification-07B22.json').read_bytes()
        self.assertEqual(hashlib.sha256(saved).hexdigest(),b22.HISTORICAL_RUN_SHA)
        self.assertEqual(b22.historical_record_errors(json.loads(saved)),[])
        self.assertEqual(b22.historical_record_errors(self.history_fixture()),[])
        for n,key,value in ((26,'findings_total',316),(26,'registry_used','findings.csv'),
            (26,'stdout_sha256','bad'),(26,'audit_checker_self_test_cases_reported',606),
            (0,'audit_checker_self_test_cases_reported',0),(26,'erp_runtime_tests_executed',False)):
            h=self.history_fixture(); h['historical_modes'][n][key]=value
            self.assertTrue(b22.historical_record_errors(h),key)
        h=self.history_fixture(); h['historical_modes'][-1]['historical_B21_child'][
            'all_original_cases_executed_unmodified']=False
        self.assertTrue(b22.historical_record_errors(h))
        h=self.history_fixture(); h['historical_modes']=h['historical_modes'][:-1]
        self.assertTrue(b22.historical_record_errors(h))

    def test_21_supplied_foreign_unit_price_projection_not_conversion_policy(self):
        p=supplied_price_projection('PACK','12','120','EACH','8',True)
        self.assertEqual((p['line_unit_after'],p['projected_line_price']),('PACK','8'))
        self.assertTrue(p['crossed_unit_without_conversion'])
        self.assertEqual(p['hypothetical_linear_reference_only'],'96')
        self.assertTrue(p['actual_pricing_policy_not_supplied'])

    def test_22_same_unit_and_no_override_counterexamples(self):
        p=supplied_price_projection('EACH','1','10','EACH','8',True)
        self.assertFalse(p['crossed_unit_without_conversion']); self.assertEqual(p['projected_line_price'],'8')
        p=supplied_price_projection('PACK','12','120','EACH','8',False)
        self.assertFalse(p['crossed_unit_without_conversion']); self.assertEqual(p['projected_line_price'],'120')

    def test_23_price_model_exact_supplied_types_finite_positive_ratio(self):
        for args in (('PACK','12','120','EACH','8',1),('PACK',12,'120','EACH','8',True),
            ('PACK','0','120','EACH','8',True),('PACK','-1','120','EACH','8',True),
            ('PACK','NaN','120','EACH','8',True),('PACK','12','Infinity','EACH','8',True)):
            with self.assertRaises(ValueError):supplied_price_projection(*args)

    def test_24_add_quantity_emits2_but_model_builds_new_row(self):
        p=supplied_dialog_transition(2)
        self.assertEqual((p['rows_after'],p['existing_quantity_after']),(2,'4'))
        self.assertEqual(p['consumer_effect'],'break-then-build-new-row')
        self.assertFalse(p['wpf_or_new_row_loading_executed'])

    def test_25_new_line_emits1_but_model_increments_existing(self):
        p=supplied_dialog_transition(1)
        self.assertEqual((p['rows_after'],p['existing_quantity_after']),(1,'5'))
        self.assertEqual(p['consumer_effect'],'increment-existing-and-return')

    def test_26_actions0_3_loader_noop_and_reject_nonlocal_actions(self):
        for action in (0,3):
            p=supplied_dialog_transition(action)
            self.assertEqual((p['rows_after'],p['existing_quantity_after']),(1,'4'))
        for action in (False,True,'1',4,-1):
            with self.assertRaises(ValueError):supplied_dialog_transition(action)
        with self.assertRaises(ValueError):supplied_dialog_transition(1,'Infinity')

    def test_27_import_nonlast_merged_target_not_projected(self):
        p=supplied_import_projection(self.lines(),self.imported(),1)
        self.assertEqual(p['import_projection_touched_indices'],[])
        self.assertEqual((p['lines'][0]['quantity'],p['lines'][0]['price']),('5','10'))
        self.assertTrue(p['success_message_after_loop_unconditional_in_model'])

    def test_28_import_last_matching_line_control_receives_supplied_values(self):
        p=supplied_import_projection(self.lines(last=True),self.imported(),1)
        self.assertEqual(p['import_projection_touched_indices'],[2])
        self.assertEqual((p['lines'][-1]['quantity'],p['lines'][-1]['price']),('7','50'))
        self.assertTrue(p['imported_values_supplied_not_business_policy'])

    def test_29_cancel3_still_overwrites_matching_last_line_independent_of1_2(self):
        p=supplied_import_projection(self.lines(last=True),self.imported(),3)
        self.assertEqual(p['import_projection_touched_indices'],[2])
        self.assertEqual((p['lines'][-1]['quantity'],p['lines'][-1]['price'],
                          p['lines'][-1]['description']),('7','50','import-A'))
        self.assertTrue(p['real_result_or_cancellation_contract_not_executed'])

    def test_30_cancel_controls_depend_on_position_and_positive_import_price(self):
        for action in (0,3):
            p=supplied_import_projection(self.lines(),self.imported(),action)
            self.assertEqual(p['lines'],self.lines()); self.assertEqual(p['import_projection_touched_indices'],[])
            p=supplied_import_projection(self.lines(last=True),self.imported() | dict(price='0'),action)
            self.assertEqual(p['lines'][-1]['price'],'10'); self.assertEqual(p['lines'][-1]['quantity'],'7')

    def test_31_import_model_deepcopies_inert_inputs_and_rejects_wrong_shapes(self):
        lines=self.lines(); imported=self.imported(); original=copy.deepcopy((lines,imported))
        supplied_import_projection(lines,imported,2)
        self.assertEqual((lines,imported),original)
        for ls,im,ac in (([],imported,1),(lines,imported,False),(lines,imported | dict(extra='x'),1),
                          ([lines[0] | dict(index='1')],imported,1)):
            with self.assertRaises(ValueError):supplied_import_projection(ls,im,ac)

    def test_32_stable_entry_guard_all_supplied_outcomes_not_runtime(self):
        for valid,match,direct,fallback in ((True,True,True,False),(True,False,False,True),
                                         (False,True,False,False),(False,False,False,False)):
            p=supplied_stable_entry_guard(valid,match)
            self.assertEqual((p['direct_id_branch'],p['barcode_fallback']),(direct,fallback))
            self.assertTrue(p['database_stability_not_observed'])
            self.assertTrue(p['raw_method_fallback_is_not_a_scanner_entry_contract'])
        for a,b in ((1,True),(True,0),('true',False)):
            with self.assertRaises(ValueError):supplied_stable_entry_guard(a,b)

    def test_33_token_discovery_masks_comments_strings_and_explicit_new_receiver(self):
        text='// ItemOpercontract.SearchForBarcode(0);\nvar s="ItemOpercontract.SearchForBarcode(1)";\nItemOpercontract.SearchForBarcode(fn("a)"), ref qty);\nnew ItemOpercontract().GetItemByIDcontract(2, 3);'
        masked=mask_noncode(text)
        self.assertEqual((len(masked),masked.count('\n')),(len(text),text.count('\n')))
        static=qualified_calls(text,'toy.cs',method='SearchForBarcode',receiver='ItemOpercontract')
        instance=qualified_calls(text,'toy.cs',method='GetItemByIDcontract',
            receiver=r'new\s+ItemOpercontract\s*\(\s*\)')
        self.assertEqual((len(static),len(instance)),(1,1)); self.assertEqual(instance[0]['call_line_start'],4)
        self.assertTrue(static[0]['not_type_or_runtime_resolution'])
        self.assertEqual(qualified_calls('Other.SearchForBarcode(1)','toy.cs',
            method='SearchForBarcode',receiver='ItemOpercontract'),[])

    def test_34_ACTUAL_B22_parser_B21_versioned_bases_API_B15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in (('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'),
            ('PHASE7_B18_CLI','B18'),('PHASE7_B19_CLI','B19'),('PHASE7_B20_CLI','B20'),
            ('PHASE7_B21_CLI','B21')):
            self.assertEqual(getattr(v,name)['default'],part)
        p=v.build_cli_parser(); self.assertEqual(p.parse_args([]).phase7_part,'B22')
        self.assertEqual(p.parse_args(['--through-phase','2']).through_phase,2)
        for part in ('A',)+tuple('B'+str(n) for n in range(1,23)):
            self.assertEqual(p.parse_args(['--phase7-part',part]).phase7_part,part)

    def test_35_real_entrypoint_historical21_context_before_current_not_proxy_default(self):
        tree=ast.parse(Path(v.__file__).read_text())
        blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1)
        self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]))
        self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main'))
        self.assertLess(body.index('historical_b20_validation('),body.index('historical_b21_validation('))
        self.assertLess(body.index('historical_b21_validation('),body.index('extend_contract_items('))
        self.assertIn('extend_amountword_contracts(historical_b21,',body)
        self.assertIn("phase7_part == 'B21'",body)
        self.assertIn('historical_b19_validation(',body)
        parser=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_cli_parser')
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(parser))

    def test_36_exact_argv_redirect_preserves_unrelated_calls_positionals_kwargs(self):
        calls=[]; backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'sentinel')
        proxy=b22.HistoricalB21Subprocess(backend,'python',Path('/a/tools'))
        kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel')
        self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in (proxy.expected+['--different'],['python','-B','/else/test_amountword_contract_audit_validator.py']):
            proxy.run(args,**kwargs); self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs)
        self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))

    def test_37_facade_restore_without_shared_subprocess_or_Path_mutation(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel')
        f=self.fake(); f.subprocess=backend; f.sys=SimpleNamespace(executable='python')
        view=b22.HistoricalB21ValidatorView(f); real_run=subprocess.run; path_read=Path.read_bytes
        before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend); self.assertIs(subprocess.run,real_run)
                self.assertIs(Path.read_bytes,path_read); self.assertEqual(len(view.rows('findings.csv')),313)
                raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_38_historical_child_ALL36_original_no_skip_restores_protected_hashes(self):
        p=Path(__file__).parent
        s=ast.unparse(ast.parse((p/'run_historical_amountword_tests_07B22.py').read_text()))
        for token in ('loadTestsFromModule(historical_tests)','suite.countTestCases() != 36',
            'result.testsRun != 36 or result.skipped','v.PHASE7_LIVE_CLI = original','v.PHASE7_B21_CLI'):
            self.assertIn(token,s)
        self.assertNotIn('unittest.skip',s)
        prov=json.loads((A/'evidence/provenance-07B22.json').read_text())
        for name in ('test_amountword_contract_audit_validator.py','validate_amountword_contract_part.py',
            'test_barcode_contract_audit_validator.py','test_navigation_contract_audit_validator.py',
            'test_caller_request_audit_validator.py','run_historical_barcode_tests_07B21.py',
            'run_historical_navigation_tests_07B20.py','run_historical_caller_request_tests_07B19.py'):
            self.assertEqual(hashlib.sha256((p/name).read_bytes()).hexdigest(),
                             prov['historical_artifact_sha256']['tools/'+name])

    def test_39_frozen313_raw_potential_barriers_neighbors_zero_extensions(self):
        old=list(csv.DictReader(io.StringIO((A/b22.SNAPSHOT).read_text(),newline='')))
        cur=list(csv.DictReader(io.StringIO((A/'findings.csv').read_text(),newline='')))
        self.assertEqual(b22.registry_preservation_errors(old,cur,(A/'findings.csv').read_bytes(),
                                                         (A/b22.SNAPSHOT).read_bytes()),[])
        lookup={r['id']:r for r in cur}
        for name in ('P4-026','P4-028','P7-034','P7-035','P7-136','P7-137','P7-138',
                     'P7-139','P7-140','P7-141'):
            self.assertEqual(lookup[name],next(r for r in old if r['id']==name))
        for name in ('P4-014','P7-132'):self.assertEqual(lookup[name]['certainty'],'potential')
        self.assertEqual(self.table('historical-extensions-07B22.csv'),[])
        for name,digest in ((b22.SNAPSHOT,b22.SNAPSHOT_SHA),(b22.SHARED_SNAPSHOT,b22.SHARED_SHA),
                           ('evidence/provenance-07B22.json',b22.PROVENANCE_SHA)):
            self.assertEqual(hashlib.sha256((A/name).read_bytes()).hexdigest(),digest)

    def test_40_scope12_8overlap4new_union416_not_census_mode3_not_support(self):
        d=json.loads((A/'evidence/scope-decision-07B22.json').read_text()); b=d['bookkeeping']
        self.assertEqual(tuple(b[k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),
                         (12,412,8,4,416,411))
        self.assertEqual(b['complement_kinds'],{'source':346,'generated-artifact':61,'project-or-resource':4})
        self.assertEqual(d['selected_upstream_split'],'SP7B21-03')
        self.assertEqual(d['bounded_cross_boundary_split'],'SP7B21-01')
        for k in ('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):
            self.assertIs(d[k],False)
        w=self.witness(); discovery=w['qualified_literal_discovery']
        self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),
                          discovery['source_csharp_paths_lexically_scanned']),(31,477))
        self.assertEqual((len(discovery['legacy_SearchForBarcode']),
                          len(discovery['legacy_GetItemByIDcontract'])),(1,1))
        self.assertEqual(len(discovery['lexical_utf8_replacement_paths_not_encoding_acceptance']),4)
        self.assertTrue(w['illustrations'][-1]['supplied_result']['mode3_support_policy_not_supplied'])
        self.assertTrue(discovery['not_complete_callgraph_or_capability_census'])


if __name__=='__main__':
    unittest.main()
