#!/usr/bin/env python3
"""48 documentary cases, NOT32 integrated acceptance plans or ERP tests.

All886 earlier cases are retained. ALL48 original B28 cases use OWN330/
raw331CRLF/indexes/presetB28 and suite-local A in a separate child. Synthetic34
schema fixtures are NOT execution evidence for the actual34 captured archive.
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
import validate_dirty_navigation_part as b29
from validate_search_snapshot_part import historical_b27_inputs
from check_dirty_navigation_witnesses import SOURCE_SLICES,bounded_count,dirty_trigger,editor,selected,trace
A=Path(__file__).resolve().parents[1]


class DirtyNavigationAuditTests(unittest.TestCase):
    def old(self,n=330):
        return [dict(id=f'PX-{i:03d}',title='synthetic',severity='High',certainty='potential',
          type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]

    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()

    def current(self):return self.old()+[self.old(1)[0]|dict(id='P7-159',next_phase='8')]
    def texts(self):return {n:'FROZEN:'+n for n in b29.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def context(self,f):return b29.historical_b28_inputs(f,self.old(),self.texts(),self.raw(self.old()))
    def table(self,name):return list(csv.DictReader(io.StringIO((A/'evidence'/name).read_text(),newline='')))
    def groups(self,end):return '\n'.join(f'| G-{n:02d} | exact |' for n in range(1,end+1))+'\n'
    def state(self,**change):return dict(ref='fixture-DRAFT-A',is_new=False,is_updated=True,guard_rows=2)|change
    def result(self,**change):return dict(done=True,gid='fixture-DOC-B')|change
    def witness(self):return json.loads((A/'evidence/dirty-navigation-witnesses-07B29.json').read_bytes())

    def contracts(self):
        fs,ivs,tests=[],[],[]
        for n in range(1,17):
            fid,iid=f'FE-{n:02d}',f'INV-{n:02d}';root='P7-159' if n<=2 else 'H'
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}' for i in (2*n-1,2*n)))
            fs.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            ivs.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in (2*n-1,2*n):tests.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,plan_kind='finding-specific' if n<=2 else 'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fs,ivs,tests

    def residuals(self):
        old=[dict(id=f'RS7B28-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='full upstream input',disposition='external-handoff',current_handoff_or_split_ids='H7B28-03;H7B28-04') for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B28.csv',upstream_row_sha256=b29.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],local_result='bounded result',owner_role='owner',required_redacted_input='full upstream input; new',impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B29-03;H7B29-04',disposition='external-handoff',runtime_status='not-executed') for r in old]
        return new,old

    def splits(self):
        old=[dict(id=f'SP7B28-{n:02d}',required_input='full upstream input') for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B28.csv',upstream_row_sha256=b29.row_sha(r),title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='full upstream input; new',next_static_action='trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed') for r in old]
        return new,old

    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4m-dirty-navigation-delivered-residuals-open']+['planned-not-started']*6
        return [dict(part_family='7B' if i<4 else '7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false') for i,s in enumerate(states)]

    def history_fixture(self):
        """Synthetic34 SCHEMA fixture, NEVER evidence34 modes executed."""
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B28.json').read_bytes())['historical_modes'])
        modes.append(dict(mode='B28',findings_total=330,registry_used=b29.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=886,audit_checker_self_test_suite_count=29,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B28_child=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',historical_parser_cutoff='B28-not-current-B29-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_search_snapshot_tests_07B29.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)))
        return dict(historical_mode_count=34,historical_modes=modes,errors=[])

    def test_01_OWN330_exact_raw331CRLF_three_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()))
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old());self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_reject_bad_OWN_rows_BOM_LF_bytes_texts(self):
        f,old,raw=self.fake(),self.old(),self.raw(self.old())
        for data,texts,b in ((old[:-1],self.texts(),raw),(old,self.texts(),b'\xef\xbb\xbf'+raw),(old,self.texts(),raw.replace(b'\r\n',b'\n')),(old,{'README.md':'only'},raw),(old,self.texts(),bytearray(raw))):
            with self.assertRaises(ValueError):
                with b29.historical_b28_inputs(f,data,texts,b):pass
        old[-1]['id']=old[0]['id']
        with self.assertRaises(ValueError):
            with b29.historical_b28_inputs(f,old,self.texts(),self.raw(old)):pass

    def test_03_context_local_Path_not_global_or_overlay(self):
        f=self.fake();before=Path.read_bytes,Path.read_text
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text),before);self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes());self.assertEqual((f.AUDIT/'q'/'..'/'findings.csv').read_bytes(),self.raw(self.old()))
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_text()

    def test_04_nested_OWN329_and_exception_restoration(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b27_inputs(f,self.old(329),self.texts(),self.raw(self.old(329))):self.assertEqual(len(f.rows('findings.csv')),329)
            self.assertEqual(len(f.rows('findings.csv')),330)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('synthetic')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_05_rows_texts_copy_isolation(self):
        f,old,texts=self.fake(),self.old(),self.texts();saved=copy.deepcopy(old)
        with b29.historical_b28_inputs(f,old,texts,self.raw(old)):
            data=f.rows('findings.csv');data[0]['next_phase']='bad';self.assertEqual(f.rows('findings.csv'),saved);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertEqual(old,saved);self.assertEqual(texts,self.texts())

    def test_06_all330_exact_fields_ALLnextphase_evidence_rawprefix(self):
        old,cur=self.old(),self.current();self.assertEqual(b29.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old)),[])
        for key in old[0]:
            bad=copy.deepcopy(cur);bad[0][key]='changed';self.assertTrue(b29.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)),key)

    def test_07_only159_append_raw332CRLF_noBOM(self):
        old,cur=self.old(),self.current()
        for bad in (cur[:-1],cur+[dict(cur[-1])],cur[:-1]+[cur[-1]|dict(id='P7-160')]):self.assertTrue(b29.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old)))
        for raw in (self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):self.assertTrue(b29.registry_preservation_errors(old,cur,raw,self.raw(old)))

    def test_08_G01to232_exact_only233to236_appended(self):
        self.assertEqual(b29.group_row_errors(self.groups(232),self.groups(236)),[])
        for bad in (self.groups(231),self.groups(233),self.groups(236).replace('G-99','G-98'),self.groups(236).replace('| G-01 | exact','| G-01 | changed')):self.assertTrue(b29.group_row_errors(self.groups(232),bad))

    def test_09_sentinels_and_expanded_before_dedup_RC(self):
        errors,calls=[],[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for gate in ('FE7B29-15','RC7B29-05','RC7B29-06','AD7B29-07','AD7B29-08'):b29.validate_source(f,dict(id=gate,evidence=b29.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]));b29.validate_source(f,dict(id='UNKNOWN',evidence=b29.DOCUMENTARY),{});b29.validate_source(f,dict(id='FE7B29-15',evidence='a.cs:1-2'),{})
        self.assertEqual((len(errors),len(calls)),(2,2))
        fs=[dict(evidence='a.cs:1-2;3;b.cs:7'),dict(evidence='a.cs:1-2;5;b.cs:7;9-10'),dict(evidence=b29.DOCUMENTARY)]
        self.assertEqual(b29.source_evidence_union(fs),'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5;b.cs:9-10')
        for bad in ('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b29.expanded_source_evidence(bad)
        fe=self.table('feature-implementation-matrix-07B29.csv')
        for r in self.table('report-reconciliation-07B29.csv'):self.assertEqual(r['evidence'],b29.source_evidence_union([f for f in fe if f['id'] in r['feature_ids'].split(';')]))

    def test_10_ordered_DN8_NO6_observations(self):
        parts=[self.table('dirty-navigation-lineage-07B29.csv'),self.table('navigation-outcome-lineage-07B29.csv')];self.assertEqual(b29.ledger_errors(*parts),[])
        for p in (0,1):
            bad=copy.deepcopy(parts);bad[p][0],bad[p][1]=bad[p][1],bad[p][0];self.assertTrue(b29.ledger_errors(*bad))
            for i in range(len(parts[p])):
                bad=copy.deepcopy(parts);bad[p][i]['observation']='all-accepted';self.assertTrue(b29.ledger_errors(*bad))

    def test_11_lineage_responsibility_not_executed(self):
        dn,no=self.table('dirty-navigation-lineage-07B29.csv'),self.table('navigation-outcome-lineage-07B29.csv')
        for key in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(no);bad[0][key]='';self.assertTrue(b29.ledger_errors(dn,bad),key)
        bad=copy.deepcopy(dn);bad[0]['runtime_status']='passed';self.assertTrue(b29.ledger_errors(bad,no))

    def test_12_FE16_INV16_T32_both_editor_manifestations_same159(self):
        self.assertEqual(b29.current_link_errors(*self.contracts()),[])
        for pool,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            parts=self.contracts();parts[pool][0][key]='changed';self.assertTrue(b29.current_link_errors(*parts))
        fs,iv,ts=self.contracts();self.assertTrue(b29.current_link_errors(fs,iv,ts[:-1]));fs[1]['finding_ids']='P7-160';self.assertTrue(b29.current_link_errors(fs,iv,ts))

    def test_13_distinct_invariants_criteria_responsibilities(self):
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            fs,iv,ts=self.contracts();fs[0][key]='';self.assertTrue(b29.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b29.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b29.current_link_errors(fs,iv,ts))

    def test_14_all14_residual_ancestry_rowsha_contracts(self):
        new,old=self.residuals();self.assertEqual(b29.residual_errors(new,old),[])
        for k in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(new);bad[0][k]='changed';self.assertTrue(b29.residual_errors(bad,old))
        self.assertTrue(b29.residual_errors(new[:-1],old))

    def test_15_full_inputs_all_routes_no_approval(self):
        new,old=self.residuals()
        for k,value in (('required_redacted_input','only new'),('current_handoff_or_split_ids','H7B29-03'),('disposition','approved'),('runtime_status','passed'),('local_result','')):
            bad=copy.deepcopy(new);bad[0][k]=value;self.assertTrue(b29.residual_errors(bad,old),k)

    def test_16_all_three_splits_full_inputs_unstarted(self):
        new,old=self.splits();self.assertEqual(b29.split_errors(new,old),[])
        for k in ('upstream_split_id','upstream_artifact','upstream_row_sha256','required_input','reason_for_split','status','runtime_status'):
            bad=copy.deepcopy(new);bad[0][k]='changed' if k!='reason_for_split' else '';self.assertTrue(b29.split_errors(bad,old),k)
        self.assertTrue(b29.split_errors(new[:-1],old))

    def test_17_bounded_R4m_fourB_sixC_unstarted(self):
        self.assertEqual(b29.remaining_work_errors(self.work()),[])
        for i,key,value in ((3,'status','complete'),(4,'status','started'),(0,'part_family','7C'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            bad=self.work();bad[i][key]=value;self.assertTrue(b29.remaining_work_errors(bad))

    def test_18_witness_strict_metadata_and_B10_addendum(self):
        w=self.witness();self.assertEqual(b29.witness_metadata_errors(w),[])
        for key in ('application_code_imported_or_executed','actual_WPF_event_order_or_count_claimed','dirty_flag_propagation_or_constructor_defaults_assumed','database_commit_or_saved_loss_claimed'):
            self.assertTrue(b29.witness_metadata_errors(w|{key:0}));self.assertTrue(b29.witness_metadata_errors(w|{key:True}))
        for key in ('illustration_count','whole_local_files_selected','erp_runtime_tests_executed'):self.assertTrue(b29.witness_metadata_errors(w|{key:True}))
        self.assertTrue(b29.witness_metadata_errors(w|{'retained_additive_B10_arithmetic_erratum':dict(local_cost=20,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)}))

    def test_19_actual_witness_hash_and_readonly_CLI_recompute(self):
        raw=(A/'evidence/dirty-navigation-witnesses-07B29.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b29.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_dirty_navigation_witnesses.py')],capture_output=True,timeout=20)
        self.assertEqual((run.returncode,run.stderr),(0,b''));self.assertEqual(run.stdout,raw)
        self.assertTrue(all(x['illustration_assertions_passed'] is True and x['source_application_executed'] is False for x in self.witness()['illustrations']))

    def test_20_synthetic34_schema_OWN330_ALL48_not_execution_evidence(self):
        h=self.history_fixture();self.assertEqual(b29.historical_record_errors(h),[])
        for key,value in (('registry_used','findings.csv'),('findings_total',331),('process_exit_code',True),('audit_checker_self_test_cases_reported',934),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=value;self.assertTrue(b29.historical_record_errors(bad),key)
        bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B28_child']['tests_reported']=47;self.assertTrue(b29.historical_record_errors(bad));self.assertTrue(b29.historical_record_errors(h|{'historical_mode_count':True}))

    def test_21_actual34_archive_and_single_pin_capture_time_identity(self):
        p=A/'evidence/historical-mode-verification-07B29-release.json';raw=p.read_bytes();h=json.loads(raw)
        self.assertEqual(hashlib.sha256(raw).hexdigest(),b29.HISTORICAL_RUN_SHA);self.assertEqual(b29.historical_record_errors(h),[])
        self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b29.ENTRY,v.HEAD,v.BRANCH))
        self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']))
        self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
        sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(b29.capture_source_errors(h,sources),[])
        changed=dict(sources);changed['tools/validate_dirty_navigation_part.py']+=b'\n';self.assertTrue(b29.capture_source_errors(h,changed))
        changed=dict(sources);changed['tools/test_dirty_navigation_audit_validator.py']+=b'\n';self.assertTrue(b29.capture_source_errors(h,changed))
        self.assertTrue(b29.capture_source_errors(h,{}))

    def test_22_both_updated_editor_search_paths_replace_before_reader(self):
        for surface in ('purchase','sale'):
            got=trace(surface,'search',self.state(),self.result());self.assertTrue(got['dirty_condition_if_checked']);self.assertFalse(got['dirty_guard_called']);self.assertFalse(got['prompt_branch_reached'])
            self.assertTrue(got['navigate_called']);self.assertTrue(got['editor_reference_replaced_before_reader']);self.assertFalse(got['old_editor_ref_still_current'])

    def test_23_new_editor_guard_threshold_is_explicit_not_placeholder_or_new_root(self):
        st=self.state(is_new=True,is_updated=False,guard_rows=1)
        self.assertTrue(dirty_trigger('purchase',st));self.assertFalse(dirty_trigger('sale',st));self.assertTrue(dirty_trigger('sale',st|dict(guard_rows=2)))
        for s in ('purchase','sale'):self.assertTrue(trace(s,'search',st,self.result())['clear_called'])
        self.assertEqual(b29.NEW_IDS,['P7-159']);self.assertFalse(self.witness()['dirty_flag_propagation_or_constructor_defaults_assumed'])

    def test_24_fresh_not_done_has_no_direct_Navigate_CLR(self):
        for s in ('purchase','sale'):
            for gid in ('-1','fixture-DOC-A'):
                got=trace(s,'search',self.state(),self.result(done=False,gid=gid));self.assertFalse(got['navigate_called']);self.assertFalse(got['clear_called']);self.assertTrue(got['old_editor_ref_still_current'])

    def test_25_done_sentinel_rejected_before_clear(self):
        for s in ('purchase','sale'):
            got=trace(s,'search',self.state(),self.result(gid='-1'));self.assertFalse(got['reader_boundary_reached']);self.assertEqual(got['editor_ref_after_boundary'],self.state()['ref'])

    def test_26_all_four_neighboring_commands_No_prevent_clear(self):
        for s in ('purchase','sale'):
            for command in ('first','last','next','previous'):
                got=trace(s,command,self.state(),answer='No');self.assertTrue(got['dirty_guard_called']);self.assertTrue(got['prompt_branch_reached']);self.assertFalse(got['clear_called']);self.assertFalse(got['reader_boundary_reached'])

    def test_27_guarded_Yes_can_reach_reset_without_target_acceptance_claim(self):
        for s in ('purchase','sale'):
            for command in ('first','last','next','previous'):
                got=trace(s,command,self.state(),answer='Yes');self.assertTrue(got['dirty_guard_called']);self.assertTrue(got['prompt_branch_reached']);self.assertTrue(got['clear_called']);self.assertIsNone(got['header_gid_assignment_only'])

    def test_28_clean_control_no_unsaved_prompt_obligation(self):
        for s in ('purchase','sale'):
            st=self.state(is_updated=False)
            for c in ('first','last','next','previous','new','search'):
                got=trace(s,c,st,self.result() if c=='search' else None);self.assertFalse(got['dirty_condition_if_checked']);self.assertFalse(got['prompt_branch_reached']);self.assertTrue(got['clear_called'])

    def test_29_new_command_uses_guard_but_no_reader(self):
        for s in ('purchase','sale'):
            no=trace(s,'new',self.state(),answer='No');yes=trace(s,'new',self.state(),answer='Yes')
            self.assertFalse(no['clear_called']);self.assertTrue(yes['clear_called']);self.assertFalse(yes['navigate_called']);self.assertFalse(yes['reader_boundary_reached'])

    def test_30_clear_markers_are_bounded_surface_specific_not_DTO_fields(self):
        p=trace('purchase','search',self.state(),self.result());s=trace('sale','search',self.state(),self.result())
        self.assertEqual(p['clear_markers'],['replace-editor-reference','clear-independent-view','reset-new-editor']);self.assertEqual(s['clear_markers'],['detach-view-source','replace-editor-reference','reset-new-editor'])
        for got in (p,s):self.assertFalse(got['constructor_fields_or_remaining_references_modeled']);self.assertEqual(got['reader_outcome_supplied'],'boundary-only')

    def test_31_supplied_success_header_identity_not_complete_hydration(self):
        for s in ('purchase','sale'):
            got=trace(s,'search',self.state(),self.result(),reader_outcome='supplied-success');self.assertEqual(got['header_gid_assignment_only'],'fixture-DOC-B');self.assertEqual(got['editor_ref_after_boundary'],'fixture-RESET-1');self.assertFalse(got['old_editor_ref_still_current']);self.assertFalse(got['reader_returned_null_in_supplied_case'])

    def test_32_supplied_no_rows_null_and_followup_reset_not_old_restore(self):
        for s in ('purchase','sale'):
            got=trace(s,'search',self.state(),self.result(),reader_outcome='supplied-no-rows');self.assertTrue(got['reader_returned_null_in_supplied_case']);self.assertTrue(got['caller_followup_fresh_reset_attempted']);self.assertEqual(got['editor_ref_after_boundary'],'fixture-RESET-2');self.assertFalse(got['old_editor_ref_still_current'])

    def test_33_supplied_outer_failure_not_provider_execution_or_extra_root(self):
        for s in ('purchase','sale'):
            got=trace(s,'search',self.state(),self.result(),reader_outcome='supplied-outer-failure');self.assertTrue(got['reader_returned_null_in_supplied_case']);self.assertFalse(got['old_editor_ref_still_current'])
        self.assertFalse(self.witness()['provider_failure_observed']);self.assertEqual(b29.EXTENDED_IDS,[])

    def test_34_strict_editor_shape_flags_and_nonboolean_count(self):
        for bad in (None,[],self.state()|dict(extra=1),self.state(ref='real-secret'),self.state(is_new=1),self.state(is_updated=0),self.state(guard_rows=True),self.state(guard_rows=13)):
            with self.assertRaises(ValueError):editor(bad)
        for bad in (True,False,1.0,'1',None,-1,13):
            with self.assertRaises(ValueError):bounded_count(bad)
        self.assertEqual(editor(self.state()),self.state())

    def test_35_strict_selected_result_not_arbitrary_strings_or_defaults(self):
        for bad in (None,[],{},self.result(done=1),self.result(gid=None),self.result(gid=''),self.result(gid="' OR 1=1"),self.result()|dict(abandon=True)):
            with self.assertRaises(ValueError):selected(bad)
        self.assertEqual(selected(self.result()),self.result())

    def test_36_reject_unreached_answers_unknown_commands_and_provider_outcomes(self):
        for kwargs in (dict(answer='No'),dict(answer=True),dict(reader_outcome='not-reached'),dict(reader_outcome=True),dict(reader_outcome='throw-SQL')):
            with self.assertRaises(ValueError):trace('sale','search',self.state(),self.result(),**kwargs)
        for surface,command,result,answer,outcome in (('other','search',self.result(),None,None),('sale','other',None,None,None),('sale','first',None,None,None),('sale','first',self.result(),'No',None),('sale','first',None,'No','supplied-success')):
            with self.assertRaises(ValueError):trace(surface,command,self.state(),result,answer,outcome)

    def test_37_fixture_functions_copy_inputs_no_hidden_mutation_or_schedule(self):
        state,result=self.state(),self.result();saved=copy.deepcopy((state,result));a=editor(state);b=selected(result);a['is_updated']=False;b['done']=False
        got=trace('sale','search',state,result);got['clear_markers'].append('fake');self.assertEqual((state,result),saved)
        self.assertNotIn('fake',trace('sale','search',state,result)['clear_markers']);self.assertFalse(self.witness()['actual_WPF_event_order_or_count_claimed'])

    def test_38_ACTUAL_B29_parser_versionedB28_and_API15(self):
        self.assertEqual(v.main.__defaults__,('B15',))
        for name,part in (('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'))+tuple((f'PHASE7_B{n}_CLI',f'B{n}') for n in range(18,29)):self.assertEqual(getattr(v,name)['default'],part)
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B29')
        for part in ('A',)+tuple('B'+str(n) for n in range(1,30)):self.assertEqual(parser.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)

    def test_39_actual_entrypoint_OWN28_before_current29(self):
        tree=ast.parse(Path(v.__file__).read_text());blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"]
        self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        body=ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main'))
        self.assertLess(body.index('historical_b27_validation('),body.index('historical_b28_validation('));self.assertLess(body.index('historical_b28_validation('),body.index('extend_dirty_navigation('))
        self.assertIn('extend_search_snapshot(historical_b28,',body);self.assertIn("phase7_part == 'B28'",body)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_cli_parser')))
        # Parser acceptance alone was insufficient in preflight01: B29 must
        # traverse every historical membership gate, not silently return7A.
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        gates=[n.test for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare)
          and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name)
          and n.test.left.id=='phase7_part']
        actual=[set(ast.literal_eval(g.comparators[0])) for g in gates]
        expected=[{f'B{i}' for i in range(first,30)} for first in range(1,20)]
        self.assertEqual(actual,expected);self.assertTrue(all('B29' in gate for gate in actual))
        for index in range(len(actual)):
            mutant=copy.deepcopy(actual);mutant[index].remove('B29')
            with self.assertRaises(AssertionError):self.assertEqual(mutant,expected)
        pre=json.loads((A/'evidence/checker-preflight-attempt-01-07B29.json').read_bytes())
        self.assertEqual((pre['phase_7_delivery'],pre['findings']['total_open_not_remediated']),('7A-partial',200))
        self.assertNotIn('audit_only_checker_self_tests_executed_not_erp_tests',pre['validation'])

    def test_40_exact_argv_proxy_preserves_other_calls_args_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'sentinel');proxy=b29.HistoricalB28Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=45)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in (proxy.expected+['--different'],['python','-B','/else/test_search_snapshot_audit_validator.py']):proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs);self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))

    def test_41_view_exception_restore_no_global_Path_shared_subprocess(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel');f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b29.HistoricalB28ValidatorView(f);original=subprocess.run,Path.read_bytes,Path.read_text;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertEqual((subprocess.run,Path.read_bytes,Path.read_text),original);self.assertEqual(len(view.rows('findings.csv')),330);raise RuntimeError('synthetic')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))

    def test_42_child_ALL48_localA_and_protected_B28_to_B24_tools(self):
        tools=A/'tools';src=ast.unparse(ast.parse((tools/'run_historical_search_snapshot_tests_07B29.py').read_text()))
        for token in ('loadTestsFromModule(historical_tests)','suite.countTestCases() != 48','result.testsRun != 48 or result.skipped','historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset','v.PHASE7_B28_CLI','b29.historical_b28_inputs('):self.assertIn(token,src)
        self.assertNotIn('unittest.skip',src);prov=json.loads((A/'evidence/provenance-07B29.json').read_bytes())
        for name in ('test_search_snapshot_audit_validator.py','validate_search_snapshot_part.py','check_search_snapshot_witnesses.py','run_historical_invoice_search_tests_07B28.py','test_invoice_search_audit_validator.py','validate_invoice_search_part.py','check_invoice_search_witnesses.py','run_historical_bulk_product_tests_07B27.py','test_bulk_product_audit_validator.py','validate_bulk_product_part.py','run_historical_property_dialog_tests_07B26.py','test_property_dialog_audit_validator.py','validate_property_dialog_part.py','run_historical_row_ownership_tests_07B25.py','test_row_ownership_audit_validator.py','validate_row_ownership_part.py'):
            self.assertEqual(hashlib.sha256((tools/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])

    def test_43_all330_fields_barriers_freezes_no_new_extension(self):
        raw=(A/b29.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')))
        self.assertEqual(b29.registry_preservation_errors(old,cur,now,raw),[]);self.assertEqual(cur[:330],old)
        lookup={r['id']:r for r in cur}
        for root in ('P4-014','P7-132','P7-145'):self.assertEqual(lookup[root]['certainty'],'potential')
        for root in ('P7-046','P7-158'):self.assertEqual(lookup[root],next(r for r in old if r['id']==root))
        self.assertEqual(b29.extension_errors(self.table('historical-extensions-07B29.csv')),[]);self.assertTrue(b29.extension_errors([dict(finding_id='P7-046')]))
        for n,h in ((b29.SNAPSHOT,b29.SNAPSHOT_SHA),(b29.SHARED_SNAPSHOT,b29.SHARED_SHA),('evidence/provenance-07B29.json',b29.PROVENANCE_SHA)):self.assertEqual(hashlib.sha256((A/n).read_bytes()).hexdigest(),h)

    def test_44_scope7_overlap7_new0_union426_22reads_whole0(self):
        d=json.loads((A/'evidence/scope-decision-07B29.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(7,426,7,0,426,401))
        self.assertEqual((d['historical_metadata_screen_count'],d['path_matched_metadata_rows']),(330,80));self.assertFalse(d['historical_body_review_claim']);self.assertEqual(d['selected_upstream_split'],'SP7B28-01')
        w=self.witness();self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),w['whole_local_files_selected']),(22,0));tuples=[]
        for r in w['bounded_source_reads_not_semantic_coverage']:
            raw=(A.parents[1]/r['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);self.assertLessEqual(r['end'],len(raw.decode('utf8').splitlines()));tuples.append((r['path'],r['start'],r['end'],r['whole_local_file_selected']))
        self.assertEqual(tuple(tuples),SOURCE_SLICES)

    def test_45_one159_no_extension_no_cancel_or_failure_recount(self):
        ad=self.table('root-adjudication-07B29.csv');self.assertEqual(len(ad),8);self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='new-local-root'],['P7-159'])
        self.assertFalse(any(r['decision']=='extended-existing-root-not-new' for r in ad));self.assertTrue(all(r['comparison_depth']==b29.DEDUP_DEPTH for r in ad))
        self.assertEqual(ad[0]['nearest_prior_root_ids'].split(';'),['P7-148','P4-015','P7-091','P7-151']);self.assertEqual(ad[2]['decision'],'failure-boundary-not-extra-root-or-extension')

    def test_46_actual_residuals_splits_each_capability_two_substantive_plans(self):
        self.assertEqual(b29.residual_errors(self.table('residual-disposition-07B29.csv'),self.table('residual-disposition-07B28.csv')),[]);self.assertEqual(b29.split_errors(self.table('split-register-07B29.csv'),self.table('split-register-07B28.csv')),[])
        fe,iv,plans=[self.table(n+'-07B29.csv') for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b29.current_link_errors(fe,iv,plans),[])
        for r in fe:
            for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):self.assertGreater(len(r[key]),20,(r['id'],key))
            linked=[t for t in plans if t['feature_ids']==r['id']];self.assertEqual(len(linked),2);self.assertEqual(len({t['acceptance_criterion'] for t in linked}),2)
            for t in linked:
                self.assertEqual(t['status'],'not-executed');self.assertGreater(len(t['procedure']),35);self.assertGreater(len(t['acceptance_criterion']),35);self.assertIn('not-executed',t['safety_controls']);self.assertIn('إذن',t['prerequisites'])

    def test_47_session_date_raw_clock_source_capture_delivery_are_distinct(self):
        prov=json.loads((A/'evidence/provenance-07B29.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B29.md').read_text();self.assertEqual(b29.date_identity_errors(prov,note),[])
        self.assertEqual(prov['audit_reference_date_utc'],'2026-11-16');self.assertIn(prov['environment_clock_observed_utc'],note)
        self.assertTrue(b29.date_identity_errors(prov|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b29.date_identity_errors(prov,note.replace(b29.B28_CHECK_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B28.json').read_bytes());self.assertEqual(old['checkout_head'],'436446091caf82c05ec01817bed5d18b4ea9fb34');self.assertNotEqual(old['checkout_head'],b29.ENTRY)
        self.assertEqual(prov['entry_actual_subprocess_receipt']['entry'],b29.ENTRY);self.assertEqual(prov['phase7B28_entry_consistency']['audit_file_count'],834)

    def test_48_collector_stdlib_only_no_app_execution_protected829(self):
        tree=ast.parse((A/'tools/check_dirty_navigation_witnesses.py').read_text());imports=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):imports.update(x.name.split('.')[0] for x in node.names)
            elif isinstance(node,ast.ImportFrom):imports.add(node.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','pathlib','re'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        prov=json.loads((A/'evidence/provenance-07B29.json').read_bytes());self.assertEqual(len(prov['historical_artifact_sha256']),829);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==h for n,h in prov['historical_artifact_sha256'].items()))
        for n in ('validate_dirty_navigation_part.py','run_historical_search_snapshot_tests_07B29.py','test_dirty_navigation_audit_validator.py'):ast.parse((A/'tools'/n).read_text(),filename=n)


if __name__=='__main__':
    unittest.main()
