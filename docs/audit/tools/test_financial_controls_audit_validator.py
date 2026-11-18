#!/usr/bin/env python3
"""24 isolated synthetic B7 documentation-checker tests, NOT ERP tests.

Artificial dictionaries/ranges/text/path labels only. No application imports,
build/SQL/WPF/Office/provider/device/formula execution or filesystem writes.
The protected132 prior checker cases and original827 hash guards stay intact.
"""
from __future__ import annotations
import copy,sys,unittest
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_financial_controls_part as b7
from validate_pos_totals_part import historical_b5_inputs


class FinancialControlsAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[dict(id='LIVE:'+p)])
    def texts(self):return {n:'FROZEN:'+n for n in b7.SHARED_DOCS}
    def old(self,n=270):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def transition(self):
        old=self.old(2);now=copy.deepcopy(old);now[0]['evidence']+=';b.cs:3-4'
        return old,now,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-ranges-not-semantic-coverage')
    def metadata(self):return dict(phase='7B7-partial-static-audit',application_code_imported_or_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=22,static_lexical_contract_check_count=22)
    def groups(self):return '\n'.join(f'| G-{n:02d} | kept exactly |' for n in range(1,117))+'\n'

    def test_01_frozen270_and_exact_logical_paths(self):
        f=self.fake()
        with b7.historical_b6_inputs(f,self.old(),self.texts()):
            self.assertEqual(len(f.rows('findings.csv')),270)
            for name in b7.SHARED_DOCS:self.assertEqual(f.read(f.AUDIT/name),'FROZEN:'+name)

    def test_02_normal_exit_restores_reader_and_registry(self):
        f=self.fake();read,rows=f.read,f.rows
        with b7.historical_b6_inputs(f,self.old(),self.texts()):pass
        self.assertIs(f.read,read);self.assertIs(f.rows,rows)

    def test_03_exception_restores_reader_and_registry(self):
        f=self.fake();read,rows=f.read,f.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b7.historical_b6_inputs(f,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(f.read,read);self.assertIs(f.rows,rows)

    def test_04_no_basename_overlay_or_snapshot_alias_mutation(self):
        f=self.fake();old=self.old()
        with b7.historical_b6_inputs(f,old,self.texts()):
            self.assertEqual(f.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            f.rows('findings.csv')[0]['title']='ALTERED';self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic');self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')])

    def test_05_wrong_count_or_duplicate_historical_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(266),self.old(269),self.old(271),duplicate):
            with self.assertRaises(ValueError):
                with b7.historical_b6_inputs(self.fake(),bad,self.texts()):pass

    def test_06_exact_three_shared_index_string_values_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b7.historical_b6_inputs(self.fake(),self.old(),bad):pass

    def test_07_nested_b5_adapter_restores_outer_b6_cutoff(self):
        f=self.fake()
        with b7.historical_b6_inputs(f,self.old(),self.texts()):
            with historical_b5_inputs(f,self.old(266),{n:'B5:'+n for n in b7.SHARED_DOCS}):
                self.assertEqual(len(f.rows('findings.csv')),266);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B5:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')),270);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')

    def test_08_current_range_union_and_line_complement_are_bookkeeping_only(self):
        x=b7.build_current_ledger([self.item()],[('7B6',[self.scope(ranges='2-3')]),('7B7',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(x['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(x['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(x['phase7B6_ranges'],'2-3');self.assertEqual(x['phase7B7_ranges'],'7-8');self.assertIn('not-closed',x['continuation_bucket']);self.assertEqual(x['runtime_status'],'not-executed')

    def test_09_all_lines_do_not_close_a_feature(self):
        p='frmRptExample.cs';x=b7.build_candidate_disposition([self.item(p)],[('7B7',[self.scope(p,'1-10')])])[0]
        self.assertEqual(x['coverage_state'],'selected-slices-not-whole-feature-closed');self.assertEqual(x['phase7B7_ranges'],'1-10');self.assertIn('required',x['disposition'])

    def test_10_binary_metadata_never_execution_coverage(self):
        x=b7.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(x['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',x['continuation_bucket'])

    def test_11_each_of_five_curated_bodies_requires_its_own_scope(self):
        for name in b7.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv=[self.item(p),self.item(p+'.cs')]
            before=b7.build_screen_disposition(inv,[])[0];after=b7.build_screen_disposition(inv,[('7B7',[self.scope(p+'.cs','1-10')])])[0]
            self.assertEqual(before['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertEqual(after['phase7B7_body_ranges'],'1-10');self.assertIn('not-whole-feature',after['coverage_level'])

    def test_12_parent_does_not_promote_another_body(self):
        parent='SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml';child='SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml';inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        by={x['screen']:x for x in b7.build_screen_disposition(inv,[('7B7',[self.scope(parent+'.cs','1-10')])])}
        self.assertEqual(by['frmNkdTotSalePurchActCust']['coverage_level'],'inventory-only-not-implementation-reviewed')

    def test_13_announced_b8_bodies_are_not_promoted(self):
        inv=[]
        for name in b7.DEFERRED_SCREENS:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv += [self.item(p),self.item(p+'.cs')]
        for x in b7.build_screen_disposition(inv,[]):
            self.assertEqual(x['phase7B7_body_ranges'],'none');self.assertEqual(x['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertIn('required',x['disposition'])

    def test_14_fingerprint_lexical_match_not_a_business_report(self):
        x=b7.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0]
        self.assertIn('lexical-false-positive',x['disposition']);self.assertEqual(x['runtime_status'],'not-executed')

    def test_15_each_historical_core_field_change_rejected(self):
        for field,value in (('title','changed'),('severity','Critical'),('certainty','potential'),('type','other'),('status','closed')):
            old,now,manifest=self.transition();now[0][field]=value
            self.assertTrue(any('.'+field in e for e in b7.registry_transition_errors(old,now,manifest)))

    def test_16_followups_preserved_even_without_evidence_tail(self):
        old,now,manifest=self.transition();self.assertEqual(b7.registry_transition_errors(old,now,manifest),[])
        now[1]['next_phase']='8';self.assertTrue(any('.next_phase' in e for e in b7.registry_transition_errors(old,now,manifest)))

    def test_17_missing_duplicate_unknown_tail_manifest_rejected(self):
        old,now,manifest=self.transition()
        for bad in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b7.registry_transition_errors(old,now,bad))

    def test_18_replacement_or_extra_undeclared_evidence_tail_rejected(self):
        old,now,manifest=self.transition();now[0]['evidence']='b.cs:3-4';self.assertTrue(b7.registry_transition_errors(old,now,manifest))
        old,now,manifest=self.transition();now[0]['evidence']+=';c.cs:5-6';self.assertTrue(b7.registry_transition_errors(old,now,manifest))

    def test_19_exact116_group_rows_allow_new_rows_only_after_prefix(self):
        prior=self.groups();self.assertEqual(b7.group_row_errors(prior,prior+'| G-117 | new |\n'),[])

    def test_20_group_row_whitespace_removal_reorder_and_old_count_rejected(self):
        prior=self.groups()
        for changed in (prior.replace('kept exactly','kept  exactly',1),prior.replace('| G-01 | kept exactly |\n',''),prior.replace('| G-01 |','| G-02 |',1)):
            self.assertTrue(b7.group_row_errors(prior,changed))
        self.assertTrue(b7.group_row_errors(prior+'| G-117 | old extra |\n',prior))

    def test_21_reverse_plan_links_must_be_exact(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b7.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b7.bidirectional_errors(pool,tests,'feature_ids'),[])

    def test_22_deferred_or_closed_features_cannot_be_promoted(self):
        x=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b7.feature_level_errors([x]),[])
        for bad in (x|{'coverage_level':'source-reviewed'},x|{'implementation_status':'complete'},x|{'evidence':'some.cs:1-10'}):self.assertTrue(b7.feature_level_errors([bad]))

    def test_23_execution_metadata_flags_are_false_only_and_counts_integer_zero(self):
        self.assertEqual(b7.witness_metadata_errors(self.metadata()),[])
        for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for val in (True,None,0):self.assertTrue(b7.witness_metadata_errors(self.metadata()|{key:val}))
        for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for val in (1,None,False,'0'):self.assertTrue(b7.witness_metadata_errors(self.metadata()|{key:val}))

    def test_24_phase_and_exact_witness_counts_not_runtime_acceptance(self):
        for bad in ({'phase':'runtime-certified'},{'illustration_count':21},{'illustration_count':22.0},{'static_lexical_contract_check_count':23},{'static_lexical_contract_check_count':None}):self.assertTrue(b7.witness_metadata_errors(self.metadata()|bad))


if __name__=='__main__':unittest.main()
