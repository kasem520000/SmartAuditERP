#!/usr/bin/env python3
"""28 B14 synthetic DOCUMENTATION-checker cases, not ERP acceptance.

Artificial rows/text/ranges and exact-path IN-MEMORY adapters only; no app
import/build/C#/SQL/WPF/REPX/Office/business export/shell, real roles/data,
measurement or remediation. All322 historical synthetic cases stay intact.
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
import validate_inventory_activity_part as b14
from validate_trial_balance_part import historical_b12_inputs


class InventoryActivityAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[dict(id='LIVE:'+p)])
    def old(self,n=291):
        return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def raw(self,old=None):
        old=self.old() if old is None else old
        out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=list(old[0]),lineterminator='\r\n');w.writeheader();w.writerows(old)
        return out.getvalue().encode()
    def texts(self):return {n:'FROZEN:'+n for n in b14.SHARED_DOCS}
    def context(self,f):return b14.historical_b13_inputs(f,self.old(),self.texts(),self.raw())
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-only')
    def groups(self,n=158):return '\n'.join(f'| G-{i:02d} | exact row |' for i in range(1,n+1))+'\n'
    def erratum(self):return dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False)
    def metadata(self):return dict(phase='7B14-partial-static-audit',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=24,static_lexical_contract_check_count=24,
        default_aggregate_gate_not_assumed_resolved=True,supplied_sql_not_certified_deployed=True,
        progress_categories_not_wholly_unread_counts=True,local_expiry_helper_and_dto_not_claimed_missing=True,
        B_R1_residual_contracts_not_closed=True,retained_additive_B10_arithmetic_erratum=self.erratum())
    def plan(self):
        return [dict(id=f'RW-{i}',part_family='7B' if i<4 else '7C',title='synthetic planning group',candidate_scope_not_certified='synthetic bounded scope',expected_deliverable='synthetic assessment',static_exit_criterion='reasoned disposition of each selected contract',dependencies_and_uncertainty='external contract unresolved',status='bounded-parent-contract-delivered-residuals-open' if i==0 else 'planned-not-started',runtime_status='not-executed',counts_are_sessions_or_completion_percent='false') for i in range(10)]
    def depth(self):
        return [dict(prior_full_local_csharp_declared='true' if i<5 else 'false',b14_full_local_body_and_xaml='true' if i<4 else 'false',remaining_old_category_after_b14='true' if i>=4 else 'false') for i in range(6)]
    def acceptance(self):
        new_ids=['P7-120','P7-121','P7-122'];extensions=[dict(finding_ids=f'OLD-{i:02d}') for i in range(22)];tests=[]
        for n,fid in enumerate(new_ids,1):
            for _ in range(2):tests.append(dict(finding_ids=fid,feature_ids=f'FE7B14-{n:02d}',invariant_ids=f'INV7B14-{n:02d}',plan_kind='finding-specific',status='not-executed'))
        tests.extend(dict(finding_ids=r['finding_ids'],plan_kind='historical-root-regression',status='not-executed') for r in extensions)
        for kind,count in [('cross-cutting-contract',4),('documentary-scope-or-authorization-gate',2)]:
            tests.extend(dict(finding_ids='HANDOFF',plan_kind=kind,status='not-executed') for _ in range(count))
        return tests,new_ids,extensions

    def test_01_own_frozen291_and_exact_three_index_texts(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(len(f.rows('findings.csv')),291)
            for n in b14.SHARED_DOCS:self.assertEqual(f.read(f.AUDIT/n),'FROZEN:'+n)
    def test_02_raw_bytes_override_exact_path_not_global_pathlib(self):
        f=self.fake();method=Path.read_bytes
        with self.context(f):
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw());self.assertIs(Path.read_bytes,method)
            self.assertEqual(str(f.AUDIT/'findings.csv'),'/synthetic/audit/findings.csv')
    def test_03_normal_exit_restores_all_object_identities(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):pass
        for x,y in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(x,y)
    def test_04_exception_restores_all_object_identities(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with self.context(f):raise RuntimeError('synthetic')
        for x,y in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(x,y)
    def test_05_nested_b12_own289_bytes_and_texts_normal_and_exception(self):
        f=self.fake();inner=self.old(289)
        with self.context(f):
            with historical_b12_inputs(f,inner,{n:'B12:'+n for n in b14.SHARED_DOCS},self.raw(inner)):
                self.assertEqual(len(f.rows('findings.csv')),289);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(inner))
                self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B12:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')),291);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
            with self.assertRaises(RuntimeError):
                with historical_b12_inputs(f,inner,self.texts(),self.raw(inner)):raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),291);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
    def test_06_wrong_counts_and_duplicate_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(289),self.old(290),self.old(292),duplicate):
            with self.assertRaises(ValueError):
                with b14.historical_b13_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass
    def test_07_exact_index_keys_and_strings_required_with_restore(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            f=self.fake();before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b14.historical_b13_inputs(f,self.old(),bad,self.raw()):pass
            for x,y in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(x,y)
    def test_08_raw_bytes_rows_CRLF_and_noBOM_must_agree(self):
        for bad in (None,'not bytes',b'\xef\xbb\xbf'+self.raw(),self.raw().replace(b'\r\n',b'\n'),self.raw().replace(b'synthetic',b'changed',1),self.raw()+b'\r\n',b'\xff'):
            with self.assertRaises(ValueError):
                with b14.historical_b13_inputs(self.fake(),self.old(),self.texts(),bad):pass
    def test_09_rows_are_fresh_copies_and_other_paths_delegate(self):
        f=self.fake();old=self.old()
        with b14.historical_b13_inputs(f,old,self.texts(),self.raw(old)):
            f.rows('findings.csv')[0]['title']='changed';self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic');self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')]);self.assertEqual(f.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/synthetic/elsewhere/findings.csv').read_bytes()
    def test_10_all_cores_followups_and_exact_append_only_tails(self):
        old=self.old(2);now=copy.deepcopy(old);now[0]['evidence']+=';b.cs:3-4';manifest=[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
        self.assertEqual(b14.registry_transition_errors(old,now,manifest),[])
        for field in ('title','severity','certainty','type','status','next_phase'):
            bad=copy.deepcopy(now);bad[1][field]='changed';self.assertTrue(any('.'+field in e for e in b14.registry_transition_errors(old,bad,manifest)))
        for bad_manifest in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b14.registry_transition_errors(old,now,bad_manifest))
        for tail in ('b.cs:3-4','a.cs:1-2;b.cs:3-4;c.cs:5-6'):
            bad=copy.deepcopy(now);bad[0]['evidence']=tail;self.assertTrue(b14.registry_transition_errors(old,bad,manifest))
    def test_11_exact158_group_rows_whitespace_order_and_new_suffix(self):
        old=self.groups();self.assertEqual(b14.group_row_errors(old,old+'\nAdditive prose\n| G-159 | new |\n'),[])
        for bad in (old.replace('exact row','exact  row',1),old.replace('| G-01 |','| G-02 |',1),self.groups(157)):self.assertTrue(b14.group_row_errors(old,bad))
        self.assertTrue(b14.group_row_errors(self.groups(159),old))
    def test_12_reverse_links_are_exact_not_one_way(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b14.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b14.bidirectional_errors(pool,tests,'feature_ids'),[])
    def test_13_feature_vocabulary_and_inventory_only_sentinel(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b14.feature_level_errors([row]),[])
        for bad in (row|{'coverage_level':'source-reviewed'},row|{'evidence':'a.cs:1-2'},row|{'implementation_status':'complete'}):self.assertTrue(b14.feature_level_errors([bad]))
    def test_14_ledger_union_complement_is_not_feature_completion(self):
        row=b14.build_current_ledger([self.item()],[('7B13',[self.scope(ranges='2-3')]),('7B14',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(row['phase7B14_ranges'],'7-8');self.assertIn('not-closed',row['continuation_bucket']);self.assertEqual(row['runtime_status'],'not-executed')
    def test_15_each_new_body_requires_its_OWN_full_xaml(self):
        for name in b14.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv=[self.item(p),self.item(p+'.cs')]
            row=b14.build_screen_disposition(inv,[('7B14',[self.scope(p,'1-10'),self.scope(p+'.cs','1-10')])])[0]
            self.assertEqual(row['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
            for selected in ([self.scope(p+'.cs','1-10')],[self.scope(p,'1-9'),self.scope(p+'.cs','1-10')]):
                row=b14.build_screen_disposition(inv,[('7B14',selected)])[0];self.assertNotEqual(row['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
    def test_16_parent_or_unselected_known_name_never_promotes_child(self):
        p='SmartAuditERP/Form_WPF/frmRptParent.xaml';c='SmartAuditERP/Form_WPF/frmRptChild.xaml'
        by={r['screen']:r for r in b14.build_screen_disposition([self.item(p),self.item(p+'.cs'),self.item(c),self.item(c+'.cs')],[('7B14',[self.scope(p+'.cs','1-10')])])}
        self.assertEqual(by['frmRptChild']['coverage_level'],'inventory-only-not-implementation-reviewed')
        p='SmartAuditERP/Form_WPF/frmRptInventory.xaml';row=b14.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
        self.assertEqual(row['phase7B14_body_ranges'],'none');self.assertEqual(row['coverage_level'],'inventory-only-not-implementation-reviewed')
    def test_17_generated_and_FingerPrint_remain_non_features(self):
        row=b14.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',row['continuation_bucket'])
        row=b14.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0];self.assertIn('lexical-false-positive',row['disposition'])
    def test_18_fourB_sixC_substantive_plan_not_sessions_or_complete(self):
        self.assertEqual(b14.remaining_work_errors(self.plan(),self.depth()),[])
        patches=[{'part_family':'7C'},{'status':'complete'},{'status':'planned-not-started'},{'runtime_status':'passed'},{'counts_are_sessions_or_completion_percent':'true'}]
        for field in ('title','candidate_scope_not_certified','expected_deliverable','static_exit_criterion','dependencies_and_uncertainty'):
            patches.extend([{field:''},{field:'  '},{field:None}])
        for patch in patches:
            bad=self.plan();bad[0]|=patch;self.assertTrue(b14.remaining_work_errors(bad,self.depth()))
        self.assertTrue(b14.remaining_work_errors(self.plan()[:-1],self.depth()))
    def test_19_six_categories_five_prior_full_four_upgrades_two_remaining(self):
        for bad in (self.depth()[:-1],[r|{'prior_full_local_csharp_declared':'false'} for r in self.depth()],[r|{'remaining_old_category_after_b14':'true'} for r in self.depth()],[r|{'b14_full_local_body_and_xaml':'false'} for r in self.depth()]):
            self.assertTrue(b14.remaining_work_errors(self.plan(),bad))
    def test_20_typed_false_integer_zero_and_five_true_boundaries(self):
        self.assertEqual(b14.witness_metadata_errors(self.metadata()),[])
        for k in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for x in (True,None,0):self.assertTrue(b14.witness_metadata_errors(self.metadata()|{k:x}))
        for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for x in (1,False,None,'0'):self.assertTrue(b14.witness_metadata_errors(self.metadata()|{k:x}))
        for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed','progress_categories_not_wholly_unread_counts','local_expiry_helper_and_dto_not_claimed_missing','B_R1_residual_contracts_not_closed'):
            for x in (False,None,1,'true'):self.assertTrue(b14.witness_metadata_errors(self.metadata()|{k:x}))
    def test_21_phase_twentyfour_counts_and_additive_erratum_are_typed(self):
        for patch in ({'phase':'ERP-certified'},{'illustration_count':23},{'illustration_count':24.0},{'static_lexical_contract_check_count':True},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'local_cost':20}},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'archive_rewritten':0}}):
            self.assertTrue(b14.witness_metadata_errors(self.metadata()|patch))
    def test_22_inventory_only_sentinels_have_no_fabricated_source(self):
        errors=[];calls=[];fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append(a))
        for n in ('RC7B14-06','ALG7B14-24'):b14.validate_source(fake,dict(id=n,evidence='none-inventory-only'),{})
        self.assertEqual(errors,[]);self.assertEqual(calls,[])
        b14.validate_source(fake,dict(id='RC7B14-06',evidence='a.cs:1-2'),{});self.assertTrue(errors)
    def test_23_builders_pure_counts_and_twenty_two_deduplicated_tails(self):
        inv=[self.item('frmRptSynthetic.cs')];labelled=[('7B14',[self.scope('frmRptSynthetic.cs','1-10')])];before=copy.deepcopy((inv,labelled))
        b14.build_current_ledger(inv,labelled,v.spans);b14.build_candidate_disposition(inv,labelled);b14.build_screen_disposition(inv,labelled);self.assertEqual((inv,labelled),before)
        counts={n:c for n,_,c in b14.TABLE_SPECS};self.assertEqual(counts['acceptance-tests'],34);self.assertEqual(counts['feature-implementation-matrix'],31);self.assertEqual(len(b14.EXTENDED_FINDINGS),22)
        self.assertTrue({'P2-011','P7-041','P7-045','P7-046','P7-049','P7-054','P7-055','P7-056','P7-057','P7-058','P7-059','P7-060','P7-061','P7-063','P7-085','P7-108'}<=b14.EXTENDED_FINDINGS)
        self.assertTrue({'P7-120','P7-121','P7-122','P3-022','P4-030','P4-009','P4-020','P7-075','P7-103'}.isdisjoint(b14.EXTENDED_FINDINGS))
    def test_24_depth_prior_full_AND_current_body_PLUS_xaml(self):
        names=list(b14.REVIEWED_BODIES)+['frmRptSynthetic'+str(n) for n in range(2)]
        inv=[];old=[];before=[];current=[]
        for i,n in enumerate(names):
            p='SmartAuditERP/Form_WPF/'+n+'.xaml';inv.extend([self.item(p),self.item(p+'.cs')])
            old.append(dict(screen=n,path=p,body_path=p+'.cs',body_inventory_lines='10',coverage_level='prior-selected-slices-depth-not-upgraded'))
            before.append(self.scope(p+'.cs','1-10' if i!=2 else '2-4'))
            if i<4:current.extend([self.scope(p,'1-10'),self.scope(p+'.cs','1-10')])
        original=b14.prior_screens
        try:
            b14.prior_screens=lambda *_:copy.deepcopy(old)
            depth=b14.depth_clarification(inv,[('7B2',before),('7B14',current)],v.spans);self.assertEqual(b14.remaining_work_errors(self.plan(),depth),[])
            self.assertEqual(depth[2]['prior_full_local_csharp_declared'],'false');self.assertEqual(depth[2]['b14_full_local_body_and_xaml'],'true')
            selected=[r for r in current if r['path']!=old[0]['path']]
            depth=b14.depth_clarification(inv,[('7B2',before),('7B14',selected)],v.spans)
            self.assertEqual(depth[0]['b14_full_local_body_and_xaml'],'false');self.assertTrue(b14.remaining_work_errors(self.plan(),depth))
        finally:b14.prior_screens=original
    def test_25_acceptance_kind_order_count_and_not_executed_only(self):
        tests,ids,ext=self.acceptance();self.assertEqual(b14.plan_structure_errors(tests,ids,ext),[])
        for bad in (tests[:-1],[tests[6]]+tests[:6]+tests[7:],[r|{'status':'passed'} if i==33 else r for i,r in enumerate(tests)]):self.assertTrue(b14.plan_structure_errors(bad,ids,ext))
        self.assertTrue(b14.plan_structure_errors(tests,ids,list(reversed(ext))))
    def test_26_exactly_two_direct_plans_and_root_feature_invariant_mapping(self):
        tests,ids,ext=self.acceptance()
        for patch in ({'finding_ids':'P7-121'},{'feature_ids':'FE7B14-02'},{'invariant_ids':'INV7B14-02'}):
            bad=copy.deepcopy(tests);bad[0]|=patch;self.assertTrue(b14.plan_structure_errors(bad,ids,ext))
        self.assertTrue(b14.plan_structure_errors(tests,ids[:2],ext));self.assertTrue(b14.plan_structure_errors(tests,[ids[0]]*3,ext))
    def test_27_input_text_mapping_mutation_does_not_change_active_overlay(self):
        f=self.fake();texts=self.texts();old=self.old()
        with b14.historical_b13_inputs(f,old,texts,self.raw(old)):
            texts['PLAN.md']='CHANGED-LATER';self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
            first=f.rows('findings.csv');second=f.rows('findings.csv');self.assertIsNot(first,second);self.assertIsNot(first[0],second[0])
        self.assertTrue(f.read(f.AUDIT/'PLAN.md').startswith('LIVE:'))
    def test_28_real_evidence_dispatch_checks_bounds_without_claiming_execution(self):
        errors=[];calls=[];scope={'a.cs':[(1,2)]}
        fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(('evidence',a)),scoped_evidence=lambda *a,**k:calls.append(('scoped',a,k)))
        row=dict(id='FE7B14-01',evidence='a.cs:1-2')
        b14.validate_source(fake,row,scope);self.assertEqual(errors,[]);self.assertEqual(calls[0],('evidence',('a.cs:1-2','FE7B14-01')))
        self.assertEqual(calls[1][1][1],scope);self.assertEqual(calls[1][2],dict(phase=7))
        b14.validate_source(fake,dict(id='UNDECLARED',evidence='none-inventory-only'),scope);self.assertTrue(errors)


if __name__=='__main__':unittest.main()
