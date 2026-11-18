#!/usr/bin/env python3
"""24 B13 synthetic DOCUMENTATION-checker cases, not ERP tests.

Artificial dictionaries/text/ranges and exact-path IN-MEMORY adapters only.
No application import/build/C#/SQL/WPF/REPX/Office/export/shell, actual roles,
financial acceptance, deployment measurement, remediation or source writes.
Historical298 synthetic cases and every protected helper stay unchanged.
"""
from __future__ import annotations
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
import validate_trial_balance_part as b13
from validate_income_contract_part import historical_b11_inputs


class TrialBalanceAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[dict(id='LIVE:'+p)])
    def old(self,n=289):
        return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def raw(self,old=None):
        old=self.old() if old is None else old
        s=io.StringIO(newline=''); w=csv.DictWriter(s,fieldnames=list(old[0]),lineterminator='\r\n'); w.writeheader(); w.writerows(old)
        return s.getvalue().encode()
    def texts(self):return {n:'FROZEN:'+n for n in b13.SHARED_DOCS}
    def context(self,f):return b13.historical_b12_inputs(f,self.old(),self.texts(),self.raw())
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-only')
    def groups(self,n=152):return '\n'.join(f'| G-{i:02d} | exact row |' for i in range(1,n+1))+'\n'
    def erratum(self):return dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False)
    def metadata(self):return dict(phase='7B13-partial-static-audit',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=20,static_lexical_contract_check_count=20,
        default_aggregate_gate_not_assumed_resolved=True,supplied_sql_not_certified_deployed=True,
        progress_categories_not_wholly_unread_counts=True,retained_additive_B10_arithmetic_erratum=self.erratum())
    def plan(self):return [dict(id=f'RW-{i}',part_family='7B' if i<4 else '7C',title='synthetic planning group',candidate_scope_not_certified='synthetic bounded scope',expected_deliverable='synthetic assessment',static_exit_criterion='reasoned disposition of each selected contract',dependencies_and_uncertainty='external contract unresolved',status='planned-not-started',runtime_status='not-executed',counts_are_sessions_or_completion_percent='false') for i in range(10)]
    def depth(self):return [dict(prior_full_local_csharp_declared='true' if i<8 else 'false',remaining_old_category_after_b13='true' if i<6 else 'false') for i in range(10)]

    def test_01_frozen289_and_exact_three_index_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(len(f.rows('findings.csv')),289)
            for n in b13.SHARED_DOCS:self.assertEqual(f.read(f.AUDIT/n),'FROZEN:'+n)
    def test_02_bytes_overlay_is_one_path_not_pathlib_patch(self):
        f=self.fake(); method=Path.read_bytes
        with self.context(f):
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw()); self.assertIs(Path.read_bytes,method)
            self.assertEqual(str(f.AUDIT/'findings.csv'),'/synthetic/audit/findings.csv')
    def test_03_normal_exit_restores_all_objects(self):
        f=self.fake(); before=f.AUDIT,f.read,f.rows
        with self.context(f):pass
        for x,y in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(x,y)
    def test_04_exception_restores_all_objects(self):
        f=self.fake(); before=f.AUDIT,f.read,f.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with self.context(f):raise RuntimeError('synthetic')
        for x,y in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(x,y)
    def test_05_nested_b11_normal_and_exception_restore_b12(self):
        f=self.fake(); inner=self.old(287)
        with self.context(f):
            with historical_b11_inputs(f,inner,{n:'B11:'+n for n in b13.SHARED_DOCS},self.raw(inner)):
                self.assertEqual(len(f.rows('findings.csv')),287); self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(inner))
                self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B11:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')),289); self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
            with self.assertRaises(RuntimeError):
                with historical_b11_inputs(f,inner,self.texts(),self.raw(inner)):raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),289); self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
    def test_06_wrong_count_and_duplicate_ids_rejected(self):
        duplicate=self.old(); duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(287),self.old(288),self.old(290),duplicate):
            with self.assertRaises(ValueError):
                with b13.historical_b12_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass
    def test_07_exact_index_keys_and_strings_required_and_restore(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            f=self.fake(); before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b13.historical_b12_inputs(f,self.old(),bad,self.raw()):pass
            for x,y in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(x,y)
    def test_08_raw_CRLF_noBOM_types_and_rows_must_agree(self):
        for bad in (None,'not bytes',b'\xef\xbb\xbf'+self.raw(),self.raw().replace(b'\r\n',b'\n'),self.raw().replace(b'synthetic',b'changed',1),self.raw()+b'\r\n',b'\xff'):
            with self.assertRaises(ValueError):
                with b13.historical_b12_inputs(self.fake(),self.old(),self.texts(),bad):pass
    def test_09_rows_copied_non_target_reads_delegate(self):
        f=self.fake(); old=self.old()
        with b13.historical_b12_inputs(f,old,self.texts(),self.raw(old)):
            f.rows('findings.csv')[0]['title']='changed'; self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic'); self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')]); self.assertEqual(f.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/synthetic/elsewhere/findings.csv').read_bytes()
    def test_10_all_cores_followups_and_exact_append_tails(self):
        old=self.old(2); now=copy.deepcopy(old); now[0]['evidence']+=';b.cs:3-4'; manifest=[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
        self.assertEqual(b13.registry_transition_errors(old,now,manifest),[])
        for field in ('title','severity','certainty','type','status','next_phase'):
            bad=copy.deepcopy(now); bad[1][field]='changed'; self.assertTrue(any('.'+field in e for e in b13.registry_transition_errors(old,bad,manifest)))
        for bad_manifest in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b13.registry_transition_errors(old,now,bad_manifest))
        for tail in ('b.cs:3-4','a.cs:1-2;b.cs:3-4;c.cs:5-6'):
            bad=copy.deepcopy(now); bad[0]['evidence']=tail; self.assertTrue(b13.registry_transition_errors(old,bad,manifest))
    def test_11_exact152_group_rows_order_whitespace_and_new_suffix(self):
        old=self.groups(); self.assertEqual(b13.group_row_errors(old,old+'\nAdditive prose\n| G-153 | new |\n'),[])
        for bad in (old.replace('exact row','exact  row',1),old.replace('| G-01 |','| G-02 |',1),self.groups(151)):self.assertTrue(b13.group_row_errors(old,bad))
        self.assertTrue(b13.group_row_errors(self.groups(153),old))
    def test_12_reverse_links_exact_not_one_way(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')]; tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b13.bidirectional_errors(pool,tests,'feature_ids')); pool[0]['acceptance_ids']='T1;T2'; self.assertEqual(b13.bidirectional_errors(pool,tests,'feature_ids'),[])
    def test_13_feature_vocabulary_and_inventory_only_sentinel(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b13.feature_level_errors([row]),[])
        for bad in (row|{'coverage_level':'source-reviewed'},row|{'evidence':'a.cs:1-2'},row|{'implementation_status':'complete'}):self.assertTrue(b13.feature_level_errors([bad]))
    def test_14_ledger_union_complement_not_semantic_completion(self):
        row=b13.build_current_ledger([self.item()],[('7B12',[self.scope(ranges='2-3')]),('7B13',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8'); self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(row['phase7B13_ranges'],'7-8'); self.assertIn('not-closed',row['continuation_bucket']); self.assertEqual(row['runtime_status'],'not-executed')
    def test_15_each_new_body_requires_own_full_xaml(self):
        for name in b13.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml'; inv=[self.item(p),self.item(p+'.cs')]
            row=b13.build_screen_disposition(inv,[('7B13',[self.scope(p,'1-10'),self.scope(p+'.cs','1-10')])])[0]
            self.assertEqual(row['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
            for selected in ([self.scope(p+'.cs','1-10')],[self.scope(p,'1-9'),self.scope(p+'.cs','1-10')]):
                row=b13.build_screen_disposition(inv,[('7B13',selected)])[0]; self.assertNotEqual(row['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
    def test_16_parent_never_promotes_child_or_unselected_known_name(self):
        p='SmartAuditERP/Form_WPF/frmRptParent.xaml'; c='SmartAuditERP/Form_WPF/frmRptChild.xaml'
        by={r['screen']:r for r in b13.build_screen_disposition([self.item(p),self.item(p+'.cs'),self.item(c),self.item(c+'.cs')],[('7B13',[self.scope(p+'.cs','1-10')])])}
        self.assertEqual(by['frmRptChild']['coverage_level'],'inventory-only-not-implementation-reviewed')
        p='SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml'; row=b13.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
        self.assertEqual(row['phase7B13_body_ranges'],'none'); self.assertEqual(row['coverage_level'],'inventory-only-not-implementation-reviewed')
    def test_17_generated_and_fingerprint_remain_non_features(self):
        row=b13.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed'); self.assertIn('not-authorized',row['continuation_bucket'])
        row=b13.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0]; self.assertIn('lexical-false-positive',row['disposition'])
    def test_18_fourB_sixC_plans_not_sessions_percent_or_started(self):
        self.assertEqual(b13.remaining_work_errors(self.plan(),self.depth()),[])
        patches=[{'part_family':'7C'},{'status':'complete'},{'runtime_status':'passed'},{'counts_are_sessions_or_completion_percent':'true'}]
        for field in ('title','candidate_scope_not_certified','expected_deliverable','static_exit_criterion','dependencies_and_uncertainty'):
            patches.extend([{field:''},{field:'  '},{field:None}])
        for patch in patches:
            bad=self.plan(); bad[0]|=patch; self.assertTrue(b13.remaining_work_errors(bad,self.depth()))
        self.assertTrue(b13.remaining_work_errors(self.plan()[:-1],self.depth()))
    def test_19_ten_categories_include_eight_prior_full_and_six_remaining(self):
        for bad in (self.depth()[:-1],[r|{'prior_full_local_csharp_declared':'false'} for r in self.depth()],[r|{'remaining_old_category_after_b13':'true'} for r in self.depth()]):self.assertTrue(b13.remaining_work_errors(self.plan(),bad))
    def test_20_false_only_flags_integer_zero_and_true_only_boundaries(self):
        self.assertEqual(b13.witness_metadata_errors(self.metadata()),[])
        for k in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for x in (True,None,0):self.assertTrue(b13.witness_metadata_errors(self.metadata()|{k:x}))
        for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for x in (1,False,None,'0'):self.assertTrue(b13.witness_metadata_errors(self.metadata()|{k:x}))
        for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed','progress_categories_not_wholly_unread_counts'):
            for x in (False,None,1,'true'):self.assertTrue(b13.witness_metadata_errors(self.metadata()|{k:x}))
    def test_21_phase_twenty_counts_and_additive_erratum_are_typed(self):
        for patch in ({'phase':'ERP-certified'},{'illustration_count':19},{'illustration_count':20.0},{'static_lexical_contract_check_count':True},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'local_cost':20}},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'archive_rewritten':0}}):self.assertTrue(b13.witness_metadata_errors(self.metadata()|patch))
    def test_22_inventory_sentinels_have_no_fabricated_source(self):
        errors=[]; calls=[]; fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append(a))
        for n in ('RC7B13-06','ALG7B13-20'):b13.validate_source(fake,dict(id=n,evidence='none-inventory-only'),{})
        self.assertEqual(errors,[]); self.assertEqual(calls,[])
        b13.validate_source(fake,dict(id='RC7B13-06',evidence='a.cs:1-2'),{}); self.assertTrue(errors)
    def test_23_builders_are_pure_and_counts_do_not_renumber_roots(self):
        inv=[self.item('frmRptSynthetic.cs')]; labelled=[('7B13',[self.scope('frmRptSynthetic.cs','1-10')])]; before=copy.deepcopy((inv,labelled))
        b13.build_current_ledger(inv,labelled,v.spans); b13.build_candidate_disposition(inv,labelled); b13.build_screen_disposition(inv,labelled); self.assertEqual((inv,labelled),before)
        counts={n:c for n,_,c in b13.TABLE_SPECS}; self.assertEqual(counts['acceptance-tests'],29); self.assertEqual(counts['feature-implementation-matrix'],27); self.assertEqual(len(b13.EXTENDED_FINDINGS),19)
        self.assertTrue({'P3-019','P3-020','P3-023','P7-052','P7-053','P7-062'}<=b13.EXTENDED_FINDINGS)
        self.assertTrue({'P7-118','P7-119','P3-022','P4-030','P7-093','P7-095','P7-116','P7-117'}.isdisjoint(b13.EXTENDED_FINDINGS))
    def test_24_depth_clarification_requires_prior_full_and_current_body_PLUS_xaml(self):
        names=list(b13.REVIEWED_BODIES)+['frmRptSynthetic'+str(n) for n in range(6)]
        inv=[]; old=[]; before=[]; current=[]
        for i,n in enumerate(names):
            p='SmartAuditERP/Form_WPF/'+n+'.xaml'; inv.extend([self.item(p),self.item(p+'.cs')])
            old.append(dict(screen=n,path=p,body_path=p+'.cs',body_inventory_lines='10',coverage_level='prior-selected-slices-depth-not-upgraded'))
            before.append(self.scope(p+'.cs','1-10' if i<8 else '2-4'))
            if i<4:current.extend([self.scope(p,'1-10'),self.scope(p+'.cs','1-10')])
        original=b13.prior_screens
        try:
            b13.prior_screens=lambda *_:copy.deepcopy(old)
            labelled=[('7B2',before),('7B13',current)]
            depth=b13.depth_clarification(inv,labelled,v.spans); self.assertEqual(b13.remaining_work_errors(self.plan(),depth),[])
            self.assertEqual(depth[-1]['prior_full_local_csharp_declared'],'false')
            selected=[r for r in current if r['path']!=old[0]['path']]
            depth=b13.depth_clarification(inv,[('7B2',before),('7B13',selected)],v.spans)
            self.assertEqual(depth[0]['b13_full_local_body_and_xaml'],'false'); self.assertTrue(b13.remaining_work_errors(self.plan(),depth))
        finally:b13.prior_screens=original


if __name__=='__main__':unittest.main()
