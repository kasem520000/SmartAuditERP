#!/usr/bin/env python3
"""20 isolated synthetic documentary-checker self-tests, NOT ERP tests.

No application import/build/SQL/WPF/Office/network or file write. Protected
10+14+20+18 earlier checker tests remain untouched. Fixtures are checker data,
not SmartAuditERP acceptance and not proof of financial or UI correctness.
"""
from __future__ import annotations
import copy
from pathlib import Path
from types import SimpleNamespace
import sys
import unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_invoice_analysis_part as b4
from validate_commercial_report_part import historical_b2_inputs


class InvoiceAnalysisAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[{'id':'LIVE:'+p}])
    def texts(self):return {name:'FROZEN:'+name for name in b4.SHARED_DOCS}
    def old(self,n=248):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def transition(self):
        old=self.old(2);current=copy.deepcopy(old);current[0]['evidence']+=';b.cs:3-4'
        return old,current,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-ranges-not-semantic-coverage')

    def test_01_frozen248_and_exact_index_paths(self):
        fake=self.fake()
        with b4.historical_b3_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.read(fake.AUDIT/'README.md'),'FROZEN:README.md')
            self.assertEqual(len(fake.rows('findings.csv')),248)

    def test_02_same_basename_elsewhere_is_not_overlaid(self):
        fake=self.fake()
        with b4.historical_b3_inputs(fake,self.old(),self.texts()):self.assertEqual(fake.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')

    def test_03_registry_copy_and_forwarding(self):
        fake=self.fake();old=self.old()
        with b4.historical_b3_inputs(fake,old,self.texts()):
            rows=fake.rows('findings.csv');rows[0]['title']='MUTATED'
            self.assertEqual(fake.rows('findings.csv')[0]['title'],'synthetic');self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(fake.rows('other.csv'),[dict(id='LIVE:other.csv')])

    def test_04_restore_read_rows_on_exit_and_exception(self):
        fake=self.fake();read,rows=fake.read,fake.rows
        with b4.historical_b3_inputs(fake,self.old(),self.texts()):pass
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b4.historical_b3_inputs(fake,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)

    def test_05_wrong_count_and_duplicate_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(247),self.old(249),duplicate):
            with self.assertRaises(ValueError):
                with b4.historical_b3_inputs(self.fake(),bad,self.texts()):pass

    def test_06_exact_three_frozen_texts_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b4.historical_b3_inputs(self.fake(),self.old(),bad):pass

    def test_07_exact_tail_preserves_all_old_fields(self):
        old,current,manifest=self.transition();self.assertEqual(b4.registry_transition_errors(old,current,manifest),[])

    def test_08_historical_classification_title_type_status_mutation_rejected(self):
        for field,value in (('severity','Critical'),('certainty','potential'),('type','different'),('title','altered'),('status','closed')):
            old,current,manifest=self.transition();current[0][field]=value
            self.assertTrue(any('.'+field in x for x in b4.registry_transition_errors(old,current,manifest)))

    def test_09_every_followup_is_preserved_not_only_extended_rows(self):
        old,current,manifest=self.transition();current[1]['next_phase']='8'
        self.assertTrue(any('.next_phase' in x for x in b4.registry_transition_errors(old,current,manifest)))

    def test_10_missing_unknown_duplicate_and_replaced_tail_rejected(self):
        old,current,manifest=self.transition()
        for bad in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b4.registry_transition_errors(old,current,bad))
        current[0]['evidence']='b.cs:3-4';self.assertTrue(b4.registry_transition_errors(old,current,manifest))

    def test_11_b4_ledger_ranges_and_complement(self):
        row=b4.build_current_ledger([self.item()],[('7A',[self.scope(ranges='2-3')]),('7B4',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(row['phase7B4_ranges'],'7-8');self.assertIn('not-closed',row['continuation_bucket']);self.assertEqual(row['runtime_status'],'not-executed')

    def test_12_binary_remains_metadata_and_execution_unauthorized(self):
        row=b4.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',row['continuation_bucket'])

    def test_13_name_false_positive_keeps_no_feature_claim(self):
        rows=b4.build_candidate_disposition([self.item('FingerPrintDevice.cs'),self.item('frmRptExample.cs')],[])
        self.assertIn('lexical-false-positive',rows[0]['disposition']);self.assertEqual(rows[1]['phase7B4_ranges'],'none');self.assertIn('required',rows[1]['disposition'])

    def test_14_full_text_span_does_not_close_report_feature(self):
        p='frmRptExample.cs';row=b4.build_candidate_disposition([self.item(p)],[('7B4',[self.scope(p,'1-10')])])[0]
        self.assertEqual(row['coverage_state'],'selected-slices-not-whole-feature-closed');self.assertEqual(row['runtime_status'],'not-executed');self.assertIn('7B5',row['disposition'])

    def test_15_curated_nonregex_screen_is_inventory_only(self):
        p='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml';row=b4.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
        self.assertIn('nonregex',row['selection_basis']);self.assertEqual(row['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertEqual(row['phase7B4_body_ranges'],'none')

    def test_16_launcher_scope_does_not_promote_children(self):
        parent='SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml';child='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml'
        inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        rows=b4.build_screen_disposition(inv,[('7B3',[self.scope(parent+'.cs','1-10')])]);by={x['screen']:x for x in rows}
        self.assertIn('local-body',by['frmNkdFoundRpt']['coverage_level']);self.assertEqual(by['frmActsInvTotal']['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertEqual(by['frmActsInvTotal']['selected_phase_ids'],'none')

    def test_17_deferred_feature_cannot_be_promoted_or_closed(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b4.feature_level_errors([row]),[])
        for bad in (row|{'coverage_level':'selected-source-slices'},row|{'implementation_status':'complete'}):self.assertTrue(b4.feature_level_errors([bad]))

    def test_18_reverse_acceptance_link_must_be_exact(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b4.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b4.bidirectional_errors(pool,tests,'feature_ids'),[])

    def test_19_contract_and_performance_leads_are_not_certified_features(self):
        for state in ('reviewed-contract-unresolved-not-global-absence','source-only-resource-performance-lead-not-runtime-measured'):
            row=dict(id='FE-X',implementation_status=state,coverage_level='selected-source-slices-not-whole-feature-certification',evidence='a.cs:2-3')
            self.assertEqual(b4.feature_level_errors([row]),[]);self.assertTrue(b4.feature_level_errors([row|{'implementation_status':'runtime-certified'}]))

    def test_20_nested_historical_adapters_restore_outer_cutoff(self):
        fake=self.fake();original=fake.rows;outer=self.texts();inner={name:'B2:'+name for name in b4.SHARED_DOCS}
        with b4.historical_b3_inputs(fake,self.old(),outer):
            with historical_b2_inputs(fake,self.old(237),inner):
                self.assertEqual(len(fake.rows('findings.csv')),237);self.assertEqual(fake.read(fake.AUDIT/'PLAN.md'),'B2:PLAN.md')
            self.assertEqual(len(fake.rows('findings.csv')),248);self.assertEqual(fake.read(fake.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertIs(fake.rows,original)


if __name__=='__main__':unittest.main()
