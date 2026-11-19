#!/usr/bin/env python3
"""24 synthetic documentary-validator cases; not ERP/financial acceptance.

All410 earlier cases remain protected and unchanged. Stdlib and audit helpers
only: artificial rows/strings/metadata, no app import/build/C#/SQL/WPF/REPX,
Office/provider/device/interpreter, secrets, remediation or measurement.
"""
from __future__ import annotations
import argparse
import copy
import csv
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_consolidation_part as b17
from validate_shared_contract_part import historical_b15_inputs
from check_consolidation_witnesses import no_sub_membership


class ConsolidationAuditTests(unittest.TestCase):
    def old(self,n=299):
        return [dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
            type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2')for i in range(n)]

    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n')
        w.writeheader();w.writerows(data);return s.getvalue().encode()

    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])

    def texts(self):return {n:'FROZEN:'+n for n in b17.SHARED_DOCS}

    def context(self,f):return b17.historical_b16_inputs(f,self.old(),self.texts(),self.raw(self.old()))

    def current(self):return self.old()+[self.old(1)[0]|dict(id='P7-128',next_phase='8')]

    def prior_feature(self,n=1,status='implemented-with-observed-defects'):
        return dict(id=f'OLD-{n}',feature='synthetic bounded capability',screen='synthetic',entrypoint_and_calls='request/source/sink',
            implementation_status=status,implementation_observed='prior observation',coverage_level='prior bounded slices',
            finding_ids='OLD-ROOT',evidence='a.cs:1-2',scope_limit='not whole feature',runtime_status='not-executed',acceptance_ids='OLD-T')

    def labelled(self):
        return [(1,'evidence/prior1.csv',[self.prior_feature()]),(2,'evidence/prior2.csv',[self.prior_feature(2,'deferred-not-implementation-reviewed')])]

    def contracts(self):
        tests=[];features=[];invariants=[]
        mapping=[1]*4+[2]*2+list(range(3,12))+[12]*3
        for i,n in enumerate(mapping,1):
            tests.append(dict(id=f'T-{i:02d}',feature_ids=f'FE-{n:02d}',invariant_ids=f'INV-{n:02d}',finding_ids='P7-128'if n==1 else'H',
                plan_kind='finding-specific'if n==1 else'documentary-scope-or-authorization-gate',status='not-executed',acceptance_criterion='criterion'+str(i)))
        for n in range(1,13):
            common=dict(finding_ids='P7-128'if n==1 else'H',evidence='a.cs:1-2',acceptance_ids=';'.join(t['id']for t in tests if t['feature_ids']==f'FE-{n:02d}'))
            features.append(dict(id=f'FE-{n:02d}',**common));invariants.append(dict(id=f'INV-{n:02d}',feature_ids=f'FE-{n:02d}',required_invariant='invariant'+str(n),**common))
        return features,invariants,tests

    def residual(self):
        upstream=[dict(id=f'RS7B16-{i:02d}',upstream_contract_ids=f'H-OLD-{i};Q-OLD-{i}',description='prior')for i in range(1,15)]
        current=[dict(upstream_residual_id=x['id'],upstream_artifact='evidence/residual-disposition-07B16.csv',
            upstream_row_sha256=b17.row_sha(x),upstream_contract_ids=x['upstream_contract_ids'],disposition='external-handoff',
            local_result='bounded result',owner_role='owner',required_redacted_input='redacted schema/policy',impact_if_unavailable='acceptance blocked',
            next_step='named static followup',static_exit_criterion='source-bound disposition',current_handoff_or_split_ids='H7B17-01',runtime_status='not-executed')for x in upstream]
        return current,upstream

    def work(self):
        statuses=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-consolidation-delivered-residuals-open']+['planned-not-started']*6
        work=[dict(part_family='7B'if i<4 else'7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false')for i,s in enumerate(statuses)]
        splits=[dict(title='named static split',candidate_scope_not_certified='selected capability',reason_for_split='bounded capacity',owner_role='owner',required_input='redacted map',next_static_action='source trace',static_exit_criterion='reasoned disposition',status='explicit-further-static-split-not-started',runtime_status='not-executed')for _ in range(3)]
        return work,splits

    def metadata(self):
        return dict(phase='7B17-partial-static-consolidation',application_code_imported_or_executed=False,application_remediation_performed=False,
            real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,
            erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=10,static_lexical_contract_check_count=10,
            historical_metadata_rows_not_unique_features=455,historical_metadata_aggregation_not_new_source_review=True,B_R4a_not_whole7B_closure=True,
            unresolved_external_contracts_and_explicit_splits_retained=True,supplied_DDL_not_deployed_schema_certification=True,
            retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False))

    def test_01_OWN299_exact_indexes_and_raw300CRLF(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old())
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')

    def test_02_no_global_path_patch_or_unrelated_read_overlay(self):
        f=self.fake();method=Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,method)
            self.assertEqual((f.AUDIT/'x'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
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

    def test_04_wrong_counts_or_duplicate_rows_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in(self.old(298),self.old(300),duplicate):
            with self.assertRaises(ValueError):
                with b17.historical_b16_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass

    def test_05_exact_CRLF_noBOM_no_trailing_CR_or_rows_disagreement(self):
        raw=self.raw(self.old())
        for bad in(None,'text',b'\xef\xbb\xbf'+raw,raw.replace(b'\r\n',b'\n'),raw+b'\r',raw+b'\r\n',raw.replace(b'synthetic',b'changed',1),b'\xff'):
            with self.assertRaises(ValueError):
                with b17.historical_b16_inputs(self.fake(),self.old(),self.texts(),bad):pass

    def test_06_exact_index_keys_types_copies_and_failed_entry_restore(self):
        for texts in({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            f=self.fake();before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b17.historical_b16_inputs(f,self.old(),texts,self.raw(self.old())):pass
            self.assertTrue(all(a is b for a,b in zip(before,(f.AUDIT,f.read,f.rows))))
        f=self.fake();old=self.old();texts=self.texts()
        with b17.historical_b16_inputs(f,old,texts,self.raw(old)):
            texts['PLAN.md']='changed';f.rows('findings.csv')[0]['title']='changed'
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
            self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic')

    def test_07_nested_B15_OWN298_and_exception_back_to299(self):
        f=self.fake();inner=self.old(298)
        with self.context(f):
            with self.assertRaises(RuntimeError):
                with historical_b15_inputs(f,inner,self.texts(),self.raw(inner)):
                    self.assertEqual(len(f.rows('findings.csv')),298)
                    self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(inner))
                    raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),299)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))

    def test_08_exact299_ALL_fields_rawprefix_and_only_append128(self):
        old,current=self.old(),self.current();raw=self.raw(current);frozen=self.raw(old)
        self.assertEqual(b17.registry_preservation_errors(old,current,raw,frozen),[])
        for key in old[0]:
            bad=copy.deepcopy(current);bad[0][key]+='changed'
            self.assertTrue(b17.registry_preservation_errors(old,bad,self.raw(bad),frozen))
        for bad in(raw+b'\r',b'\xef\xbb\xbf'+raw,raw.replace(b'\r\n',b'\n')):
            self.assertTrue(b17.registry_preservation_errors(old,current,bad,frozen))
        self.assertTrue(b17.registry_preservation_errors(old,current[:-1],self.raw(current[:-1]),frozen))

    def test_09_G176_exact_rows_not_substring_presence(self):
        old='\n'.join(f'| G-{i:02d} | exact |'for i in range(1,177))+'\n'
        self.assertEqual(b17.group_row_errors(old,old+'| G-177 | new |\n'),[])
        self.assertTrue(b17.group_row_errors(old,old.replace('| G-06 | exact','| G-06 | changed')+old))

    def test_10_frozen_ledger_exact_mapping_source_limit_and_rowsha(self):
        labelled=self.labelled();ledger=b17.build_capability_ledger(labelled)
        self.assertEqual(b17.ledger_errors(ledger,b17.build_capability_ledger(labelled)),[])
        self.assertEqual(ledger[0]['upstream_row_sha256'],b17.row_sha(labelled[0][2][0]))
        self.assertEqual(ledger[0]['prior_limit'],'not whole feature')
        self.assertEqual(ledger[1]['disposition'],'split-explicitly')

    def test_11_ledger_does_not_tolerate_reclassification_or_lost_evidence(self):
        expected=b17.build_capability_ledger(self.labelled())
        for key in('upstream_row_sha256','coverage_level_at_delivery','implementation_status_at_delivery','prior_evidence','prior_limit','prior_acceptance_ids','entry_and_trace','finding_ids_at_delivery'):
            bad=copy.deepcopy(expected);bad[0][key]='silently changed'
            self.assertTrue(b17.ledger_errors(bad,expected))

    def test_12_ledger_missing_duplicate_and_reordered_upstreams(self):
        expected=b17.build_capability_ledger(self.labelled())
        for bad in(expected[:-1],expected+[expected[0]],expected[::-1]):self.assertTrue(b17.ledger_errors(bad,expected))

    def test_13_deferred_external_and_counterevidence_not_upgraded(self):
        self.assertEqual(b17.prior_disposition('launcher-only-children-deferred','x'),('split-explicitly','SP7B17-01'))
        self.assertEqual(b17.prior_disposition('conditional-policy-or-external-contract','قالب'),('external-handoff','H7B17-02'))
        self.assertEqual(b17.prior_disposition('reviewed-contract-unresolved-not-global-absence','تفويض'),('external-handoff','H7B17-04'))
        self.assertEqual(b17.prior_disposition('counterevidence-not-global-closure','x')[0],'assessment-source-bound')

    def test_14_unknown_metadata_status_never_defaults_to_certification(self):
        for bad in('unknown','complete','passed'):
            with self.assertRaises(ValueError):b17.prior_disposition(bad,'synthetic')

    def test_15_current_FE_INV_T_bidirectional_lineage(self):
        self.assertEqual(b17.current_link_errors(*self.contracts()),[])

    def test_16_wrong_evidence_root_or_feature_lineage_rejected(self):
        for key in('feature_ids','finding_ids','evidence','acceptance_ids'):
            fe,inv,tests=self.contracts();inv[0][key]='wrong'
            self.assertTrue(b17.current_link_errors(fe,inv,tests))

    def test_17_plan_execution_duplicate_criterion_and_missing_reverse_link(self):
        for patch in({'status':'passed'},{'finding_ids':'WRONG'},{'feature_ids':'FE-02'}):
            fe,inv,tests=self.contracts();tests[0]|=patch
            self.assertTrue(b17.current_link_errors(fe,inv,tests))
        fe,inv,tests=self.contracts();tests[1]['acceptance_criterion']=tests[0]['acceptance_criterion']
        self.assertTrue(b17.current_link_errors(fe,inv,tests))

    def test_18_all14_upstream_residuals_exact_lineage_and_order(self):
        current,upstream=self.residual();self.assertEqual(b17.residual_errors(current,upstream),[])
        for bad in(current[:-1],current[::-1],current+[current[0]]):self.assertTrue(b17.residual_errors(bad,upstream))
        current[0]['upstream_row_sha256']='bad';self.assertTrue(b17.residual_errors(current,upstream))

    def test_19_residual_owner_input_impact_nextstep_and_no_approval(self):
        for key in('owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            for value in('',' ',None):
                data,upstream=self.residual();data[0][key]=value;self.assertTrue(b17.residual_errors(data,upstream))
        for patch in({'disposition':'complete'},{'runtime_status':'passed'}):
            data,upstream=self.residual();data[0]|=patch;self.assertTrue(b17.residual_errors(data,upstream))

    def test_20_R4a_residuals_not_complete_C_unstarted_and_no_percentage(self):
        self.assertEqual(b17.remaining_work_errors(*self.work()),[])
        for i,key,value in((3,'status','complete'),(4,'status','in-progress'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            work,splits=self.work();work[i][key]=value;self.assertTrue(b17.remaining_work_errors(work,splits))

    def test_21_explicit_split_reason_scope_input_owner_and_exit_required(self):
        for key in('candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            work,splits=self.work();splits[0][key]=' ';self.assertTrue(b17.remaining_work_errors(work,splits))
        work,splits=self.work();splits[0]['status']='complete';self.assertTrue(b17.remaining_work_errors(work,splits))

    def test_22_strict_boolean_integer_metadata_and_additive_erratum(self):
        self.assertEqual(b17.witness_metadata_errors(self.metadata()),[])
        for key,value in(('application_code_imported_or_executed',0),('erp_runtime_tests_executed',False),('phase7C_started',True),('phase8_authorized_or_started',None),('B_R4a_not_whole7B_closure',1),('illustration_count',10.0),('historical_metadata_rows_not_unique_features',455.0)):
            self.assertTrue(b17.witness_metadata_errors(self.metadata()|{key:value}))
        bad=self.metadata();bad['retained_additive_B10_arithmetic_erratum']['local_cost']=20
        self.assertTrue(b17.witness_metadata_errors(bad))

    def test_23_declared_documentary_sentinel_vs_real_scoped_source(self):
        errors,calls=[],[]
        fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg)if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        b17.validate_source(fake,dict(id='FE7B17-09',evidence=b17.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]))
        b17.validate_source(fake,dict(id='UNKNOWN',evidence=b17.DOCUMENTARY),{})
        self.assertEqual(len(errors),1)
        b17.validate_source(fake,dict(id='FE7B17-01',evidence='a.cs:1-2'),{'a.cs':[(1,2)]})
        self.assertEqual(len(calls),2)
        b17.validate_source(fake,dict(id='FE7B17-09',evidence='a.cs:1-2'),{})
        self.assertEqual(len(errors),2)

    def test_24_ACTUAL_B17_parser_B16_option_B15_API_and_state_handmodel_limits(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        self.assertEqual(v.PHASE7_B16_CLI['default'],'B16')
        parser=argparse.ArgumentParser();parser.add_argument('--phase7-part',**v.PHASE7_CURRENT_CLI)
        self.assertEqual(parser.parse_args([]).phase7_part,'B17')
        self.assertEqual(parser.parse_args(['--phase7-part','B16']).phase7_part,'B16')
        self.assertEqual(no_sub_membership(True,'with',[('T',15)]),(True,['T']))
        flag,_=no_sub_membership(True,'without',[('Z',0)])
        self.assertEqual(no_sub_membership(flag,'with',[('T',15)]),(False,[]))
        with self.assertRaises(ValueError):no_sub_membership(True,'unsupported',[]+[('T',15)])


if __name__=='__main__':
    unittest.main()
