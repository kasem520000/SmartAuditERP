#!/usr/bin/env python3
"""52 documentary checker cases, NOT32 integrated acceptance plans or ERP.

All934 previous cases retained; ALL48 B29 unchanged in their explicit OWN331
child with historical107-source assertion INPUTS. Actual B30 parser/source/
111 tools tested here, never satisfied by the old AST text input view.
Synthetic35 fixtures only test schema and are NOT execution evidence.
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
import validate_import_cancel_part as b30
from validate_dirty_navigation_part import historical_b28_inputs
from check_import_cancel_witnesses import (SOURCE_SLICES,EV_EXTENSION,small_int,editor,result,config,number_result,guard_denies,trace)
A=Path(__file__).resolve().parents[1]


class ImportCancelAuditTests(unittest.TestCase):
    def old(self,n=331):
        data=[dict(id=f'PX-{i:03d}',severity='High',certainty='potential',type='synthetic-only',status='open-not-remediated',title='fixture-title',evidence='a.cs:1-2',next_phase='7;8') for i in range(n)]
        if n==331:data[-1]['id']='P7-159'
        return data
    def raw(self,data):
        s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(data[0]),lineterminator='\r\n');w.writeheader();w.writerows(data);return s.getvalue().encode()
    def extension(self):return [dict(finding_id='P7-159',appended_evidence=EV_EXTENSION,reason='Explicit artificial accepted-import source extension of159 only; not an extra root.')]
    def current(self):
        old=self.old();old[-1]['evidence']+=';'+EV_EXTENSION
        return old+[self.old(1)[0]|dict(id='P7-160',next_phase='8')]
    def texts(self):return {n:'FROZEN:'+n for n in b30.SHARED_DOCS}
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda n:[dict(id='LIVE:'+n)])
    def sources(self):
        raw=b'# fixture historical dispatcher text, not executed\n'
        return {'tools/validate_audit.py':hashlib.sha256(raw).hexdigest()}|{f'tools/fixture_{i:03d}.py':'a'*64 for i in range(106)},raw
    def context(self,f):return b30.historical_b29_inputs(f,self.old(),self.texts(),self.raw(self.old()),*self.sources())
    def table(self,stem):return list(csv.DictReader(io.StringIO((A/'evidence'/stem).read_text(),newline='')))
    def groups(self,end):return '\n'.join(f'| G-{n:02d} | exact |' for n in range(1,end+1))+'\n'
    def witness(self):return json.loads((A/'evidence/import-cancel-witnesses-07B30.json').read_bytes())
    def state(self,**changes):return dict(ref='fixture-EDITOR-A',gid='fixture-DOC-A',invoice_no=7,combined_id='fixture-COMBINED-A',note='fixture-note',is_new=False,is_printed=True,is_updated=True,invoice_type=1,proc_type=1,impact=1,items=[dict(line=f'fixture-L{i}',item_type=t,impact=1) for i,t in enumerate((1,3,5),1)])|changes
    def target(self):return self.state(ref='fixture-EDITOR-B',gid='fixture-DOC-B',combined_id='fixture-COMBINED-B')
    def selected(self,**changes):return dict(done=False,gid='-1')|changes
    def cfg(self,surface='purchase',**changes):return dict(invoice_type=1 if surface=='purchase' else 2,proc_type=1,impact=1 if surface=='purchase' else -1,code='fixture-CODE-P-' if surface=='purchase' else 'fixture-CODE-S-')|changes
    def num(self,**changes):return dict(kind='supplied-normal',value=41)|changes
    def run_model(self,surface='purchase',**kwargs):return trace(surface,self.state(),self.selected(),self.cfg(surface),self.num(),**kwargs)
    def contracts(self):
        fs,ivs,ts=[],[],[]
        for n in range(1,17):
            fid,iid=f'FE-{n:02d}',f'INV-{n:02d}';root='P7-160' if n<=2 else ('P7-159' if n<=4 else 'H')
            common=dict(finding_ids=root,evidence='a.cs:1-2',acceptance_ids=';'.join(f'T-{i:02d}' for i in (2*n-1,2*n)))
            fs.append(dict(id=fid,owner_role='owner',required_redacted_input='redacted',impact_if_unavailable='blocked',next_step='step',limit='bounded',**common))
            ivs.append(dict(id=iid,feature_ids=fid,required_invariant='invariant'+str(n),**common))
            for i in (2*n-1,2*n):ts.append(dict(id=f'T-{i:02d}',feature_ids=fid,invariant_ids=iid,finding_ids=root,plan_kind='finding-specific' if n<=4 else 'documentary',status='not-executed',acceptance_criterion='criterion'+str(i)))
        return fs,ivs,ts
    def residuals(self):
        old=[dict(id=f'RS7B29-{n:02d}',upstream_contract_ids=f'H-OLD-{n}',required_redacted_input='full upstream input',disposition='external-handoff',current_handoff_or_split_ids='H7B29-03;H7B29-04') for n in range(1,15)]
        new=[dict(upstream_residual_id=r['id'],upstream_artifact='evidence/residual-disposition-07B29.csv',upstream_row_sha256=b30.row_sha(r),upstream_contract_ids=r['upstream_contract_ids'],required_redacted_input='full upstream input; new',local_result='bounded result',owner_role='owner',impact_if_unavailable='blocked',next_step='step',static_exit_criterion='criterion',current_handoff_or_split_ids='H7B30-03;H7B30-04',disposition='external-handoff',runtime_status='not-executed') for r in old]
        return new,old
    def splits(self):
        old=[dict(id=f'SP7B29-{n:02d}',required_input='full upstream input') for n in range(1,4)]
        new=[dict(upstream_split_id=r['id'],upstream_artifact='evidence/split-register-07B29.csv',upstream_row_sha256=b30.row_sha(r),title='named split',candidate_scope_not_certified='bounded capability',reason_for_split='reason',owner_role='owner',required_input='full upstream input; new',next_static_action='trace',static_exit_criterion='exit',status='explicit-further-static-split-not-started',runtime_status='not-executed') for r in old]
        return new,old
    def work(self):
        states=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4n-import-cancel-delivered-residuals-open']+['planned-not-started']*6
        return [dict(part_family='7B' if i<4 else '7C',status=s,runtime_status='not-executed',counts_are_sessions_or_completion_percent='false') for i,s in enumerate(states)]
    def history_fixture(self):
        """Synthetic35 SCHEMA only; copied prefixes are not new process evidence."""
        modes=copy.deepcopy(json.loads((A/'evidence/historical-mode-verification-07B29-release.json').read_bytes())['historical_modes'])
        child=dict(tests_reported=48,expected_tests=48,process_exit_code=0,result='passed',historical_parser_cutoff='B29-not-current-B30-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_dirty_navigation_tests_07B30.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True,historical_source_assertion_input_count=107,auxiliary_dispatcher_text_sha256=b30.DISPATCHER_SHA,historical_source_assertions_not_current_execution_tool_inventory=True)
        modes.append(dict(mode='B29',findings_total=331,registry_used=b30.SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=934,audit_checker_self_test_suite_count=30,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,stdout_sha256='a'*64,historical_B29_child=child))
        return dict(historical_mode_count=35,historical_modes=modes,errors=[])

    def test_01_OWN331_exact_raw332CRLF_three_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.rows('findings.csv'),self.old());self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old()));self.assertEqual(f.read(f.AUDIT/'README.md'),'FROZEN:README.md')
            self.assertEqual(list(csv.DictReader(io.StringIO((f.AUDIT/'findings.csv').read_text(),newline=''))),self.old())
    def test_02_reject_bad_rows_BOM_LF_source_vector_dispatch_text(self):
        old,raw,sources=self.old(),self.raw(self.old()),self.sources()
        for data,texts,b,src,text in ((old[:-1],self.texts(),raw,*sources),(old,self.texts(),b'\xef\xbb\xbf'+raw,*sources),(old,self.texts(),raw.replace(b'\r\n',b'\n'),*sources),(old,{'README.md':'only'},raw,*sources),(old,self.texts(),bytearray(raw),*sources),(old,self.texts(),raw,{},sources[1]),(old,self.texts(),raw,sources[0],sources[1]+b'x')):
            with self.assertRaises(ValueError):
                with b30.historical_b29_inputs(self.fake(),data,texts,b,src,text):pass
        duplicate=self.old();duplicate[0]['id']=duplicate[1]['id']
        with self.assertRaises(ValueError):
            with b30.historical_b29_inputs(self.fake(),duplicate,self.texts(),self.raw(duplicate),*sources):pass
    def test_03_historical107_glob_and_text_are_context_local_not_Path_patch(self):
        f=self.fake();original=(Path.read_bytes,Path.read_text,Path.glob);sources,raw=self.sources()
        with self.context(f):
            self.assertEqual((Path.read_bytes,Path.read_text,Path.glob),original)
            self.assertEqual({p.relative_to(f.AUDIT).as_posix() for p in (f.AUDIT/'tools').glob('*.py')},set(sources))
            self.assertEqual((f.AUDIT/'tools/validate_audit.py').read_bytes(),raw);self.assertEqual((f.AUDIT/'tools/validate_audit.py').read_text(),raw.decode())
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes());self.assertEqual((f.AUDIT/'q/../findings.csv').read_bytes(),self.raw(self.old()))
            self.assertNotIn('tools/test_import_cancel_audit_validator.py',sources)
    def test_04_nested_OWN330_and_exception_restore(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):
            with historical_b28_inputs(f,self.old(330),self.texts(),self.raw(self.old(330))):self.assertEqual(len(f.rows('findings.csv')),330)
            self.assertEqual(len(f.rows('findings.csv')),331)
        with self.assertRaises(RuntimeError):
            with self.context(f):raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_05_input_copy_isolation_nonmatching_paths_and_code_identity(self):
        f,old,texts=self.fake(),self.old(),self.texts();saved=copy.deepcopy(old);code=v.main.__code__;file=v.__file__
        with b30.historical_b29_inputs(f,old,texts,self.raw(old),*self.sources()):
            data=f.rows('findings.csv');data[0]['title']='changed';self.assertEqual(f.rows('findings.csv'),saved);self.assertEqual(f.rows('else/findings.csv'),[dict(id='LIVE:else/findings.csv')])
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/other/findings.csv').read_text()
        self.assertEqual(old,saved);self.assertEqual(texts,self.texts());self.assertIs(v.main.__code__,code);self.assertEqual(v.__file__,file)
    def test_06_all331_fields_except_exact159_evidence_tail(self):
        old,cur=self.old(),self.current();self.assertEqual(b30.registry_preservation_errors(old,cur,self.raw(cur),self.raw(old),self.extension()),[])
        for i in (0,329,330):
            for key in old[i]:
                bad=copy.deepcopy(cur);bad[i][key]='changed';self.assertTrue(b30.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),self.extension()),(i,key))
    def test_07_extension_only159_exact_one_tail_manifest(self):
        ext=self.extension();self.assertEqual(b30.extension_errors(ext),[])
        for bad in ([],ext+ext,[ext[0]|dict(finding_id='P7-046')],[ext[0]|dict(appended_evidence=EV_EXTENSION+';a.cs:2')],[ext[0]|dict(reason='')],[ext[0]|dict(extra='unscoped')]):self.assertTrue(b30.extension_errors(bad))
        cur=self.current();cur[330]['evidence']+=';'+EV_EXTENSION;self.assertTrue(b30.registry_preservation_errors(self.old(),cur,self.raw(cur),self.raw(self.old()),ext))
    def test_08_only160_append_raw333CRLF_noBOM_first330_rawprefix(self):
        old,cur=self.old(),self.current()
        for bad in (cur[:-1],cur+[dict(cur[-1])],cur[:-1]+[cur[-1]|dict(id='P7-161')]):self.assertTrue(b30.registry_preservation_errors(old,bad,self.raw(bad),self.raw(old),self.extension()))
        for raw in (self.raw(cur).replace(b'\r\n',b'\n'),b'\xef\xbb\xbf'+self.raw(cur),self.raw(cur)[:-2]):self.assertTrue(b30.registry_preservation_errors(old,cur,raw,self.raw(old),self.extension()))
        frozen=self.raw(old);self.assertTrue(self.raw(cur).startswith(b''.join(frozen.splitlines(keepends=True)[:-1])));self.assertFalse(self.raw(cur).startswith(frozen))
    def test_09_G01to236_exact_only237to240(self):
        self.assertEqual(b30.group_row_errors(self.groups(236),self.groups(240)),[])
        for bad in (self.groups(239),self.groups(241),self.groups(240).replace('G-99','G-98'),self.groups(240).replace('| G-01 | exact','| G-01 | changed')):self.assertTrue(b30.group_row_errors(self.groups(236),bad))
    def test_10_sentinels_expanded_source_union_RC(self):
        errors,calls=[],[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for gate in ('FE7B30-15','RC7B30-05','RC7B30-06','AD7B30-07','AD7B30-08'):b30.validate_source(f,dict(id=gate,evidence=b30.DOCUMENTARY),{})
        self.assertEqual((errors,calls),([],[]));b30.validate_source(f,dict(id='UNKNOWN',evidence=b30.DOCUMENTARY),{});b30.validate_source(f,dict(id='FE7B30-15',evidence='a.cs:1-2'),{});self.assertEqual((len(errors),len(calls)),(2,2))
        fs=[dict(evidence='a.cs:1-2;3;b.cs:7'),dict(evidence='a.cs:1-2;5;b.cs:7;9-10'),dict(evidence=b30.DOCUMENTARY)]
        self.assertEqual(b30.source_evidence_union(fs),'a.cs:1-2;a.cs:3;b.cs:7;a.cs:5;b.cs:9-10')
        for bad in ('5;a.cs:1-2','a.cs:1-2;unscoped','a.cs:'):
            with self.assertRaises(ValueError):b30.expanded_source_evidence(bad)
        fe=self.table('feature-implementation-matrix-07B30.csv')
        for r in self.table('report-reconciliation-07B30.csv'):self.assertEqual(r['evidence'],b30.source_evidence_union([f for f in fe if f['id'] in r['feature_ids'].split(';')]))
    def test_11_ordered_IC8_IR8_exact_observations(self):
        parts=[self.table('import-conversion-lineage-07B30.csv'),self.table('import-return-lineage-07B30.csv')];self.assertEqual(b30.ledger_errors(*parts),[])
        for pool in (0,1):
            bad=copy.deepcopy(parts);bad[pool][0],bad[pool][1]=bad[pool][1],bad[pool][0];self.assertTrue(b30.ledger_errors(*bad))
            for i in range(8):
                bad=copy.deepcopy(parts);bad[pool][i]['observation']='all-accepted';self.assertTrue(b30.ledger_errors(*bad))
    def test_12_lineage_responsibilities_no_runtime(self):
        ic,ir=self.table('import-conversion-lineage-07B30.csv'),self.table('import-return-lineage-07B30.csv')
        for key in ('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
            bad=copy.deepcopy(ir);bad[0][key]='';self.assertTrue(b30.ledger_errors(ic,bad),key)
        bad=copy.deepcopy(ic);bad[0]['runtime_status']='passed';self.assertTrue(b30.ledger_errors(bad,ir))
    def test_13_FE16_INV16_T32_new160_and_existing159(self):
        self.assertEqual(b30.current_link_errors(*self.contracts()),[])
        for pool,key in ((0,'acceptance_ids'),(1,'feature_ids'),(2,'feature_ids'),(2,'status'),(2,'finding_ids')):
            data=self.contracts();data[pool][0][key]='changed';self.assertTrue(b30.current_link_errors(*data))
        for index in (0,1,2,3):
            data=self.contracts();data[0][index]['finding_ids']='P7-161';self.assertTrue(b30.current_link_errors(*data))
    def test_14_distinct_criteria_substantive_fields(self):
        for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            fs,iv,ts=self.contracts();fs[0][key]='';self.assertTrue(b30.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();iv[1]['required_invariant']=iv[0]['required_invariant'];self.assertTrue(b30.current_link_errors(fs,iv,ts))
        fs,iv,ts=self.contracts();ts[1]['acceptance_criterion']=ts[0]['acceptance_criterion'];self.assertTrue(b30.current_link_errors(fs,iv,ts));self.assertTrue(b30.current_link_errors(fs,iv,ts[:-1]))
    def test_15_RS14_exact_ancestry_rowSHA_contracts(self):
        new,old=self.residuals();self.assertEqual(b30.residual_errors(new,old),[])
        for key in ('upstream_residual_id','upstream_artifact','upstream_row_sha256','upstream_contract_ids'):
            bad=copy.deepcopy(new);bad[0][key]='changed';self.assertTrue(b30.residual_errors(bad,old))
        self.assertTrue(b30.residual_errors(new[:-1],old))
    def test_16_full_old_inputs_all_mapped_routes_dispositions(self):
        new,old=self.residuals()
        for key,val in (('required_redacted_input','only new'),('current_handoff_or_split_ids','H7B30-03'),('disposition','approved'),('runtime_status','passed'),('local_result','')):
            bad=copy.deepcopy(new);bad[0][key]=val;self.assertTrue(b30.residual_errors(bad,old))
    def test_17_SP3_ancestry_full_input_future_split_not_started(self):
        new,old=self.splits();self.assertEqual(b30.split_errors(new,old),[])
        for key in ('upstream_split_id','upstream_artifact','upstream_row_sha256','required_input','reason_for_split','status','runtime_status'):
            bad=copy.deepcopy(new);bad[0][key]='changed' if key!='reason_for_split' else '';self.assertTrue(b30.split_errors(bad,old))
        self.assertTrue(b30.split_errors(new[:-1],old))
    def test_18_boundedR4n_fourB_sixC_unstarted(self):
        self.assertEqual(b30.remaining_work_errors(self.work()),[])
        for i,key,val in ((3,'status','complete'),(4,'status','started'),(0,'part_family','7C'),(0,'runtime_status','passed'),(0,'counts_are_sessions_or_completion_percent','true')):
            data=self.work();data[i][key]=val;self.assertTrue(b30.remaining_work_errors(data))
    def test_19_witness_strict_metadata_and_retained_B10_addendum(self):
        w=self.witness();self.assertEqual(b30.witness_metadata_errors(w),[])
        for key in ('application_code_imported_or_executed','actual_WPF_chrome_close_result_or_event_schedule_claimed','SDK_setter_defaults_or_reentrancy_modeled','database_commit_or_saved_loss_claimed'):
            self.assertTrue(b30.witness_metadata_errors(w|{key:0}));self.assertTrue(b30.witness_metadata_errors(w|{key:True}))
        for key in ('illustration_count','whole_local_files_selected','erp_runtime_tests_executed'):self.assertTrue(b30.witness_metadata_errors(w|{key:True}))
        self.assertTrue(b30.witness_metadata_errors(w|{'retained_additive_B10_arithmetic_erratum':dict(local_cost=20,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)}))
    def test_20_actual_witness_bytes_and_readonly_recompute(self):
        raw=(A/'evidence/import-cancel-witnesses-07B30.json').read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),b30.WITNESS_SHA)
        run=subprocess.run([sys.executable,'-B',str(A/'tools/check_import_cancel_witnesses.py')],capture_output=True,timeout=20);self.assertEqual((run.returncode,run.stderr),(0,b''));self.assertEqual(run.stdout,raw)
        self.assertTrue(all(x['illustration_assertions_passed'] is True and x['source_application_executed'] is False for x in self.witness()['illustrations']))
    def test_21_nonaccepted_purchase_retains_ref_not_values(self):
        t=self.run_model();st=t['state_at_pre_binding_boundary'];self.assertFalse(t['navigate_called']);self.assertTrue(t['old_editor_ref_still_current']);self.assertEqual((st['ref'],st['note'],st['invoice_no'],st['is_new']),('fixture-EDITOR-A','',41,True));self.assertTrue(t['binding_controls_attempted'])
    def test_22_nonaccepted_sale_later_flags_not_postevent_claim(self):
        t=self.run_model('sale');st=t['state_at_pre_binding_boundary'];self.assertFalse(t['navigate_called']);self.assertEqual((st['is_new'],st['is_printed'],st['is_updated']),(True,False,False));self.assertTrue(t['scalar_or_item_changes_at_boundary']);self.assertFalse(self.witness()['SDK_setter_defaults_or_reentrancy_modeled'])
    def test_23_sale_item_types3_5_zero_others_current_impact(self):
        t=self.run_model('sale');self.assertEqual([x['impact'] for x in t['state_at_pre_binding_boundary']['items']],[-1,0,0]);self.assertEqual([x['line'] for x in t['state_at_pre_binding_boundary']['items']],['fixture-L1','fixture-L2','fixture-L3'])
        p=self.run_model();self.assertEqual(p['state_at_pre_binding_boundary']['items'],self.state()['items'])
    def test_24_false_with_valid_GID_still_converts_without_Navigate(self):
        for sf in ('purchase','sale'):
            t=trace(sf,self.state(),self.selected(gid='fixture-DOC-B'),self.cfg(sf),self.num());self.assertFalse(t['navigate_called']);self.assertTrue(t['tail_attempted']);self.assertTrue(t['old_editor_ref_still_current'])
    def test_25_done_with_minusone_still_converts(self):
        for sf in ('purchase','sale'):
            t=trace(sf,self.state(),self.selected(done=True),self.cfg(sf),self.num());self.assertFalse(t['accepted_result_not_abandon_decision']);self.assertTrue(t['number_helper_called'])
    def test_26_accepted_purchase_is_existing159_extension(self):
        t=trace('purchase',self.state(),self.selected(done=True,gid='fixture-DOC-B'),self.cfg(),self.num(),after_navigate=self.target());self.assertTrue(t['navigate_called']);self.assertFalse(t['dirty_guard_called']);self.assertFalse(t['old_editor_ref_still_current']);self.assertEqual(t['state_at_pre_binding_boundary']['gid'],'fixture-DOC-B');self.assertEqual(b30.EXTENDED_IDS,['P7-159'])
    def test_27_accepted_sale_same159_not161(self):
        t=trace('sale',self.state(),self.selected(done=True,gid='fixture-DOC-B'),self.cfg('sale'),self.num(),after_navigate=self.target());self.assertTrue(t['navigate_called']);self.assertFalse(t['dirty_guard_called']);self.assertEqual(b30.NEW_IDS,['P7-160']);self.assertFalse(self.witness()['all_callers_or_external_DTOs_body_reviewed'])
    def test_28_number_failure_purchase_note_earlier_flags_not_reached(self):
        t=trace('purchase',self.state(),self.selected(),self.cfg(),dict(kind='supplied-failure'));st=t['state_at_pre_binding_boundary'];self.assertEqual((st['note'],st['invoice_no'],st['is_new']),('',7,False));self.assertFalse(t['later_flags_assigned']);self.assertFalse(t['binding_controls_attempted'])
    def test_29_number_failure_sale_items_earlier_print_update_unchanged(self):
        t=trace('sale',self.state(),self.selected(),self.cfg('sale'),dict(kind='supplied-failure'));st=t['state_at_pre_binding_boundary'];self.assertEqual([x['impact'] for x in st['items']],[-1,0,0]);self.assertEqual((st['is_new'],st['is_printed'],st['is_updated']),(False,True,True));self.assertFalse(t['binding_controls_attempted']);self.assertFalse(self.witness()['provider_failure_observed'])
    def test_30_ShowDialog_nonreturn_no_tail_no_downstream_result(self):
        for sf in ('purchase','sale'):
            t=trace(sf,self.state(),self.selected(),self.cfg(sf),dialog_return='supplied-showdialog-exception');self.assertFalse(t['tail_attempted']);self.assertFalse(t['number_helper_called']);self.assertEqual(t['state_at_pre_binding_boundary'],self.state())
            with self.assertRaises(ValueError):trace(sf,self.state(),self.selected(),self.cfg(sf),self.num(),dialog_return='supplied-showdialog-exception')
    def test_31_matching_values_can_mask_reached_tail(self):
        st=self.state(note='',is_new=True,invoice_no=41,combined_id='fixture-CODE-P-41');t=trace('purchase',st,self.selected(),self.cfg(),self.num());self.assertTrue(t['tail_attempted']);self.assertFalse(t['scalar_or_item_changes_at_boundary']);self.assertEqual(t['state_at_pre_binding_boundary'],st)
    def test_32_purchase_no_explicit_print_update_reset_or_new_GlobalID(self):
        t=self.run_model();st=t['state_at_pre_binding_boundary'];self.assertEqual((st['is_printed'],st['is_updated'],st['gid'],st['combined_id']),(True,True,'fixture-DOC-A','fixture-CODE-P-41'));self.assertFalse(t['global_id_assigned_by_conversion_tail']);self.assertFalse(self.witness()['new_GlobalID_allocated_or_SQL_write_claimed'])
    def test_33_empty_sale_items_still_header_conversion(self):
        st=self.state(items=[]);t=trace('sale',st,self.selected(),self.cfg('sale'),self.num());self.assertEqual(t['state_at_pre_binding_boundary']['items'],[]);self.assertEqual(t['state_at_pre_binding_boundary']['invoice_no'],41);self.assertTrue(t['later_flags_assigned'])
    def test_34_clean_and_new_flags_are_supplied_not_necessary_for160(self):
        for st in (self.state(is_updated=False),self.state(is_new=True,is_updated=False)):
            t=trace('sale',st,self.selected(),self.cfg('sale'),self.num());self.assertTrue(t['tail_attempted']);self.assertTrue(t['scalar_or_item_changes_at_boundary'])
        self.assertTrue(self.witness()['normal_nonaccepted_return_and_nonnull_editor_are_supplied'])
    def test_35_adjacent_guard_No_Yes_and_thresholds_explicit(self):
        for sf in ('purchase','sale'):
            self.assertTrue(guard_denies(sf,self.state(),2,'No'));self.assertFalse(guard_denies(sf,self.state(),2,'Yes'));self.assertFalse(guard_denies(sf,self.state(is_updated=False),2,'No'))
        st=self.state(is_new=True,is_updated=False);self.assertTrue(guard_denies('purchase',st,1,'No'));self.assertFalse(guard_denies('sale',st,1,'No'))
        for args in (('sale',st,True,'No'),('other',st,1,'No'),('sale',st,1,False)):
            with self.assertRaises(ValueError):guard_denies(*args)
    def test_36_result_shape_no_arbitrary_id_or_bool(self):
        for bad in (None,[],{},self.selected(done=1),self.selected(gid=None),self.selected(gid=''),self.selected(gid="' OR 1=1"),self.selected()|dict(abandon=True)):
            with self.assertRaises(ValueError):result(bad)
        self.assertEqual(result(self.selected()),self.selected())
    def test_37_editor_strict_nonnull_items_flags_identity_domains(self):
        for bad in (None,[],self.state()|dict(extra=1),self.state(ref='business-ref'),self.state(gid=''),self.state(is_new=1),self.state(invoice_no=True),self.state(items=None),self.state(items=[None]),self.state(items=[dict(line='fixture-L1',item_type=True,impact=1)]),self.state(items=[dict(line='fixture-L1',item_type=1,impact=1)]*2)):
            with self.assertRaises(ValueError):editor(bad)
        for val in (True,False,1.0,'1',None,-1,1000):
            with self.assertRaises(ValueError):small_int(val)
    def test_38_config_and_number_strict_bounded_shapes(self):
        for bad in (None,{},self.cfg(invoice_type=True),self.cfg(code='business-prefix'),self.cfg()|dict(extra=1)):
            with self.assertRaises(ValueError):config(bad)
        for bad in (None,{},self.num(value=True),self.num(value=1000),dict(kind='supplied-failure',value=41),dict(kind='observed-SQL',value=41)):
            with self.assertRaises(ValueError):number_result(bad)
    def test_39_copy_isolation_reject_unreached_outcomes_unknown_surfaces(self):
        st,res,cfg,num=self.state(),self.selected(),self.cfg(),self.num();saved=copy.deepcopy((st,res,cfg,num));t=trace('purchase',st,res,cfg,num);t['state_at_pre_binding_boundary']['items'][0]['impact']=-1;self.assertEqual((st,res,cfg,num),saved)
        for kwargs in (dict(after_navigate=self.target()),dict(dialog_return=True),dict(dialog_return='unknown')):
            with self.assertRaises(ValueError):trace('purchase',st,res,cfg,num,**kwargs)
        for after in (None,self.state(),self.target()|dict(gid='fixture-DOC-A')):
            with self.assertRaises(ValueError):trace('purchase',st,self.selected(done=True,gid='fixture-DOC-B'),cfg,num,after_navigate=after)
        with self.assertRaises(ValueError):trace('unknown',st,res,cfg,num)
    def test_40_ACTUAL_B30_parser_versionedB29_API15(self):
        self.assertEqual(v.main.__defaults__,('B15',));self.assertEqual(v.PHASE7_B29_CLI['default'],'B29');self.assertEqual(v.PHASE7_LIVE_CLI['default'],'B30')
        for name,part in (('PHASE7_B16_CLI','B16'),('PHASE7_CURRENT_CLI','B17'))+tuple((f'PHASE7_B{n}_CLI',f'B{n}') for n in range(18,30)):self.assertEqual(getattr(v,name)['default'],part)
        parser=v.build_cli_parser();self.assertEqual(parser.parse_args([]).phase7_part,'B30')
        for part in ('A',)+tuple('B'+str(n) for n in range(1,31)):self.assertEqual(parser.parse_args(['--phase7-part',part]).phase7_part,part)
        self.assertEqual(parser.parse_args(['--through-phase','2']).through_phase,2)
    def test_41_ACTUAL_source_19gates_B29_historical_before_currentB30(self):
        self.assertEqual(Path(v.__file__).resolve(),(A/'tools/validate_audit.py').resolve());live=Path(v.__file__).read_bytes();self.assertNotEqual(hashlib.sha256(live).hexdigest(),b30.DISPATCHER_SHA)
        tree=ast.parse(live);main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main');body=ast.unparse(main)
        for left,right in (('historical_b28_validation(','historical_b29_validation('),('historical_b29_validation(','extend_import_cancel(')):self.assertLess(body.index(left),body.index(right))
        self.assertIn('extend_dirty_navigation(historical_b29,',body);self.assertIn("phase7_part == 'B29'",body)
        blocks=[n for n in tree.body if isinstance(n,ast.If) and ast.unparse(n.test)=="__name__ == '__main__'"];self.assertEqual(len(blocks),1);self.assertIn('build_cli_parser().parse_args()',ast.unparse(blocks[0]));self.assertIn('main(args.through_phase, args.phase7_part)',ast.unparse(blocks[0]))
        gates=[n.test for n in ast.walk(main) if isinstance(n,ast.If) and isinstance(n.test,ast.Compare) and len(n.test.ops)==1 and isinstance(n.test.ops[0],ast.In) and isinstance(n.test.left,ast.Name) and n.test.left.id=='phase7_part']
        actual=[set(ast.literal_eval(g.comparators[0])) for g in gates];expected=[{f'B{i}' for i in range(first,31)} for first in range(1,20)];self.assertEqual(actual,expected)
        for index in range(19):
            mutant=copy.deepcopy(actual);mutant[index].remove('B30')
            with self.assertRaises(AssertionError):self.assertEqual(mutant,expected)
        self.assertIn('PHASE7_LIVE_CLI',ast.unparse(next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='build_cli_parser')))
        actual_sources={p.relative_to(A).as_posix() for p in (A/'tools').glob('*.py')};self.assertEqual(len(actual_sources),111);self.assertIn('tools/test_import_cancel_audit_validator.py',actual_sources)
    def test_42_exact_argv_proxy_preserves_backend_other_args_kwargs(self):
        calls=[];backend=SimpleNamespace(run=lambda *a,**k:calls.append((a,k)) or 'sentinel');proxy=b30.HistoricalB29Subprocess(backend,'python',Path('/a/tools'));kwargs=dict(cwd='/a',capture_output=True,text=True,timeout=60)
        self.assertEqual(proxy.run(list(proxy.expected),**kwargs),'sentinel');self.assertEqual(calls[-1],((proxy.actual,),kwargs))
        for args in (proxy.expected+['--different'],['python','-B','/else/test_dirty_navigation_audit_validator.py']):proxy.run(args,**kwargs);self.assertEqual(calls[-1],((args,),kwargs))
        proxy.run(tuple(proxy.expected),'positional',**kwargs);self.assertEqual(calls[-1],((tuple(proxy.expected),'positional'),kwargs))
    def test_43_view_restore_no_global_Path_subprocess_patch(self):
        backend=SimpleNamespace(run=lambda *a,**k:'sentinel');f=self.fake();f.subprocess,f.sys=backend,SimpleNamespace(executable='python');view=b30.HistoricalB29ValidatorView(f);original=subprocess.run,Path.read_bytes,Path.read_text,Path.glob;before=f.AUDIT,f.read,f.rows
        with self.assertRaises(RuntimeError):
            with self.context(view):
                self.assertIs(f.subprocess,backend);self.assertEqual((subprocess.run,Path.read_bytes,Path.read_text,Path.glob),original);self.assertEqual(len(view.rows('findings.csv')),331);raise RuntimeError('fixture')
        self.assertTrue(all(x is y for x,y in zip(before,(f.AUDIT,f.read,f.rows))))
    def test_44_ALL48_child_localA_preset_and_source_input_restoration(self):
        tools=A/'tools';src=ast.unparse(ast.parse((tools/'run_historical_dirty_navigation_tests_07B30.py').read_text()))
        for token in ('loadTestsFromModule(historical_tests)','suite.countTestCases() != 48','run.testsRun != 48 or run.skipped','historical_tests.A = v.AUDIT','historical_tests.A = original_a','v.PHASE7_LIVE_CLI = original_preset','v.__file__ = original_file','v.PHASE7_B29_CLI','b30.historical_b29_inputs('):self.assertIn(token,src)
        self.assertNotIn('unittest.skip',src);prov=json.loads((A/'evidence/provenance-07B30.json').read_bytes())
        for name in ('test_dirty_navigation_audit_validator.py','validate_dirty_navigation_part.py','check_dirty_navigation_witnesses.py','run_historical_search_snapshot_tests_07B29.py','test_search_snapshot_audit_validator.py','validate_search_snapshot_part.py','test_invoice_search_audit_validator.py','validate_invoice_search_part.py','test_bulk_product_audit_validator.py','validate_bulk_product_part.py','test_property_dialog_audit_validator.py','validate_property_dialog_part.py','test_row_ownership_audit_validator.py','validate_row_ownership_part.py'):
            self.assertEqual(hashlib.sha256((tools/name).read_bytes()).hexdigest(),prov['historical_artifact_sha256']['tools/'+name])
    def test_45_ACTUAL35_archive_and_single_inverse_pin_tool_identity(self):
        p=A/'evidence/historical-mode-verification-07B30.json';raw=p.read_bytes();h=json.loads(raw);self.assertEqual(hashlib.sha256(raw).hexdigest(),b30.HISTORICAL_RUN_SHA);self.assertEqual(b30.historical_record_errors(h),[])
        self.assertEqual((h['checkout_head'],h['source_head'],h['branch']),(b30.ENTRY,v.HEAD,v.BRANCH));self.assertTrue(all(m['stdout_bytes']>0 and m['stderr_bytes']==0 and m['process_exit_code']==0 for m in h['historical_modes']))
        sources={p.relative_to(A).as_posix():p.read_bytes() for p in sorted((A/'tools').glob('*.py'))};self.assertEqual(len(sources),111);self.assertEqual(b30.capture_source_errors(h,sources),[])
        for key in ('tools/validate_import_cancel_part.py','tools/test_import_cancel_audit_validator.py','tools/validate_audit.py'):
            changed=dict(sources);changed[key]+=b'\n';self.assertTrue(b30.capture_source_errors(h,changed))
        self.assertTrue(b30.capture_source_errors(h,{}));self.assertNotEqual(h['historical_modes'][-1]['stdout_sha256'],self.history_fixture()['historical_modes'][-1]['stdout_sha256'])
    def test_46_synthetic35_schema_not_actual_process_evidence(self):
        h=self.history_fixture();self.assertEqual(b30.historical_record_errors(h),[])
        for key,val in (('registry_used','findings.csv'),('findings_total',332),('process_exit_code',True),('audit_checker_self_test_cases_reported',986),('erp_runtime_tests_executed',True)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1][key]=val;self.assertTrue(b30.historical_record_errors(bad),key)
        for key,val in (('tests_reported',47),('historical_source_assertion_input_count',111),('auxiliary_dispatcher_text_sha256','b'*64),('historical_source_assertions_not_current_execution_tool_inventory',1)):
            bad=copy.deepcopy(h);bad['historical_modes'][-1]['historical_B29_child'][key]=val;self.assertTrue(b30.historical_record_errors(bad),key)
        self.assertTrue(b30.historical_record_errors(h|dict(historical_mode_count=True)))
    def test_47_actual331_core_evidence_exception_barriers_freezes(self):
        raw=(A/b30.SNAPSHOT).read_bytes();old=list(csv.DictReader(io.StringIO(raw.decode(),newline='')));now=(A/'findings.csv').read_bytes();cur=list(csv.DictReader(io.StringIO(now.decode(),newline='')));ext=self.table('historical-extensions-07B30.csv')
        self.assertEqual(b30.registry_preservation_errors(old,cur,now,raw,ext),[]);self.assertEqual(cur[:330],old[:330])
        for a,b in zip(old,cur):self.assertEqual({k:x for k,x in a.items() if k!='evidence'},{k:x for k,x in b.items() if k!='evidence'})
        lookup={r['id']:r for r in cur}
        for root in ('P4-014','P7-132','P7-145'):self.assertEqual(lookup[root]['certainty'],'potential')
        for root in ('P7-046','P7-158'):self.assertEqual(lookup[root],next(r for r in old if r['id']==root))
        for n,h in ((b30.SNAPSHOT,b30.SNAPSHOT_SHA),(b30.SHARED_SNAPSHOT,b30.SHARED_SHA),('evidence/provenance-07B30.json',b30.PROVENANCE_SHA),(b30.DISPATCHER_SNAPSHOT,b30.DISPATCHER_SHA)):self.assertEqual(hashlib.sha256((A/n).read_bytes()).hexdigest(),h)
    def test_48_scope7_overlap6_new1_union427_14reads_2wholechild(self):
        d=json.loads((A/'evidence/scope-decision-07B30.json').read_bytes());self.assertEqual(tuple(d['bookkeeping'][k] for k in ('selected_paths','prior_union','overlap','new','union','complement')),(7,426,6,1,427,400))
        self.assertEqual((d['historical_metadata_screen_count'],d['path_matched_metadata_rows']),(331,78));self.assertFalse(d['historical_body_review_claim']);self.assertEqual(d['selected_upstream_split'],'SP7B29-01')
        w=self.witness();self.assertEqual((len(w['bounded_source_reads_not_semantic_coverage']),w['whole_local_files_selected']),(14,2));tuples=[]
        for r in w['bounded_source_reads_not_semantic_coverage']:
            raw=(A.parents[1]/r['path']).read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),r['sha256']);self.assertLessEqual(r['end'],len(raw.decode('utf8').splitlines()));tuples.append((r['path'],r['start'],r['end'],r['whole_local_file_selected']))
            if r['whole_local_file_selected']:self.assertEqual((r['start'],r['end']),(1,len(raw.decode('utf8').splitlines())))
        self.assertEqual(tuple(tuples),SOURCE_SLICES)
    def test_49_one160_one159_extension_no_editor_recount(self):
        ad=self.table('root-adjudication-07B30.csv');self.assertEqual(len(ad),8);self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='new-local-root'],['P7-160']);self.assertEqual([r['current_root_ids'] for r in ad if r['decision']=='extended-existing-root-not-new'],['P7-159']);self.assertTrue(all(r['comparison_depth']==b30.DEDUP_DEPTH for r in ad))
        self.assertEqual(ad[0]['nearest_prior_root_ids'].split(';'),['P7-159','P7-148','P4-015','P7-091','P7-151']);self.assertEqual(ad[1]['decision'],'same-root-second-editor-not-new')
    def test_50_actual_RS_SP_and_substantive_two_plans_per_capability(self):
        self.assertEqual(b30.residual_errors(self.table('residual-disposition-07B30.csv'),self.table('residual-disposition-07B29.csv')),[]);self.assertEqual(b30.split_errors(self.table('split-register-07B30.csv'),self.table('split-register-07B29.csv')),[])
        fe,iv,plans=[self.table(n+'-07B30.csv') for n in ('feature-implementation-matrix','report-invariants','acceptance-tests')];self.assertEqual(b30.current_link_errors(fe,iv,plans),[])
        for row in fe:
            for key in ('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):self.assertGreater(len(row[key]),20,(row['id'],key))
            linked=[t for t in plans if t['feature_ids']==row['id']];self.assertEqual(len(linked),2);self.assertEqual(len({t['acceptance_criterion'] for t in linked}),2)
            for t in linked:self.assertEqual(t['status'],'not-executed');self.assertGreater(len(t['procedure']),35);self.assertGreater(len(t['acceptance_criterion']),35);self.assertIn('not-executed',t['safety_controls']);self.assertIn('إذن',t['prerequisites'])
    def test_51_date_rawclock_source_capture_delivery_and_AST_input_distinct(self):
        p=json.loads((A/'evidence/provenance-07B30.json').read_bytes());note=(A/'DATE-IDENTITY-NOTE-07B30.md').read_text();self.assertEqual(b30.date_identity_errors(p,note),[]);self.assertEqual(p['audit_reference_date_utc'],'2026-11-16');self.assertIn(p['environment_clock_observed_utc'],note)
        self.assertTrue(b30.date_identity_errors(p|dict(audit_reference_date_utc='changed'),note));self.assertTrue(b30.date_identity_errors(p,note.replace(b30.DISPATCHER_SHA,'changed')))
        old=json.loads((A/'evidence/checks-07B29.json').read_bytes());self.assertEqual(old['checkout_head'],'dda1eafab4188b00a7d6c3e435e7391bd0e09cda');self.assertNotEqual(old['checkout_head'],b30.ENTRY);self.assertEqual(p['entry_actual_subprocess_receipt']['entry'],b30.ENTRY)
        self.assertEqual(p['dispatcher_source_at_entry']['bytes'],98822);self.assertEqual(len(p['historical_checker_sources_at_entry']),107);self.assertEqual(p['historical_checker_sources_at_entry']['tools/validate_audit.py'],b30.DISPATCHER_SHA)
    def test_52_collector_stdlib_only_protected867_and_new_tool_syntax(self):
        tree=ast.parse((A/'tools/check_import_cancel_witnesses.py').read_text());imports=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):imports.update(x.name.split('.')[0] for x in node.names)
            elif isinstance(node,ast.ImportFrom):imports.add(node.module.split('.')[0])
        self.assertEqual(imports,{'__future__','copy','hashlib','json','pathlib','re'});self.assertFalse(any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in {'eval','exec','__import__'} for n in ast.walk(tree)))
        p=json.loads((A/'evidence/provenance-07B30.json').read_bytes());self.assertEqual(len(p['historical_artifact_sha256']),867);self.assertTrue(all(hashlib.sha256((A/n).read_bytes()).hexdigest()==h for n,h in p['historical_artifact_sha256'].items()))
        for n in ('validate_import_cancel_part.py','run_historical_dirty_navigation_tests_07B30.py','test_import_cancel_audit_validator.py'):ast.parse((A/'tools'/n).read_text(),filename=n)


if __name__=='__main__':
    unittest.main()
