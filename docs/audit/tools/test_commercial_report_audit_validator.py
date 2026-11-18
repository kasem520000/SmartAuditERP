#!/usr/bin/env python3
"""18 synthetic self-tests for new documentary helpers, NOT ERP tests.

No application import/build, SQL, WPF, binary, device, network or file write.
Previously delivered10+14+20 tests/helpers remain protected and unchanged.
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
import validate_commercial_report_part as b3


class CommercialReportAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[{'id':'LIVE:'+p}])
    def texts(self):return {name:'FROZEN:'+name for name in b3.SHARED_DOCS}
    def old(self,n=237):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def transition(self):
        old=self.old(2);current=copy.deepcopy(old);current[0]['evidence']+=';b.cs:3-4'
        return old,current,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-ranges-not-semantic-coverage')

    def test_01_b2_frozen237_and_exact_index_paths_are_used(self):
        fake=self.fake()
        with b3.historical_b2_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.read(fake.AUDIT/'README.md'),'FROZEN:README.md')
            self.assertEqual(len(fake.rows('findings.csv')),237)

    def test_02_same_basename_elsewhere_does_not_use_snapshot(self):
        fake=self.fake()
        with b3.historical_b2_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')

    def test_03_registry_is_copied_and_other_csv_is_forwarded(self):
        fake=self.fake();old=self.old()
        with b3.historical_b2_inputs(fake,old,self.texts()):
            rows=fake.rows('findings.csv');rows[0]['title']='MUTATED'
            self.assertEqual(fake.rows('findings.csv')[0]['title'],'synthetic')
            self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(fake.rows('other.csv'),[dict(id='LIVE:other.csv')])

    def test_04_adapter_restores_function_identities_on_normal_and_exception_exit(self):
        fake=self.fake();read,rows=fake.read,fake.rows
        with b3.historical_b2_inputs(fake,self.old(),self.texts()):pass
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b3.historical_b2_inputs(fake,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)

    def test_05_wrong_count_or_duplicate_snapshot_id_is_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(236),self.old(238),duplicate):
            with self.assertRaises(ValueError):
                with b3.historical_b2_inputs(self.fake(),bad,self.texts()):pass

    def test_06_shared_snapshot_requires_exact_three_text_values(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b3.historical_b2_inputs(self.fake(),self.old(),bad):pass

    def test_07_exact_manifest_tail_preserves_core_and_every_schedule(self):
        old,current,manifest=self.transition()
        self.assertEqual(b3.registry_transition_errors(old,current,manifest),[])

    def test_08_historical_classification_or_title_change_is_rejected(self):
        for field,value in (('severity','Critical'),('certainty','potential'),('title','altered'),('status','closed')):
            old,current,manifest=self.transition();current[0][field]=value
            self.assertTrue(any('.'+field in x for x in b3.registry_transition_errors(old,current,manifest)))

    def test_09_any_historical_followup_change_is_rejected(self):
        old,current,manifest=self.transition();current[1]['next_phase']='8'
        self.assertTrue(any('.next_phase' in x for x in b3.registry_transition_errors(old,current,manifest)))

    def test_10_missing_replaced_duplicate_or_unknown_extension_is_rejected(self):
        old,current,manifest=self.transition()
        self.assertTrue(b3.registry_transition_errors(old,current,[]))
        self.assertTrue(b3.registry_transition_errors(old,current,manifest*2))
        self.assertTrue(b3.registry_transition_errors(old,current,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]))
        current[0]['evidence']='b.cs:3-4'
        self.assertTrue(b3.registry_transition_errors(old,current,manifest))

    def test_11_b3_ledger_preserves_ranges_and_their_complement(self):
        labelled=[('7A',[self.scope(ranges='2-3')]),('7B3',[self.scope(ranges='7-8')])]
        row=b3.build_current_ledger([self.item()],labelled,v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8')
        self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(row['phase7B3_ranges'],'7-8')
        self.assertIn('not-closed',row['continuation_bucket'])
        self.assertEqual(row['runtime_status'],'not-executed')

    def test_12_binary_artifact_is_not_an_application_test(self):
        row=b3.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed')
        self.assertIn('not-authorized',row['continuation_bucket'])

    def test_13_name_candidates_keep_fingerprint_false_positive_and_no_completion(self):
        rows=b3.build_candidate_disposition([self.item('FingerPrintDevice.cs'),self.item('frmRptExample.cs')],[])
        self.assertIn('lexical-false-positive',rows[0]['disposition'])
        self.assertEqual(rows[1]['phase7B3_ranges'],'none')
        self.assertIn('required',rows[1]['disposition'])

    def test_14_complete_declared_text_span_does_not_close_a_feature(self):
        p='frmRptExample.cs';row=b3.build_candidate_disposition([self.item(p)],[('7B3',[self.scope(p,'1-10')])])[0]
        self.assertEqual(row['coverage_state'],'selected-slices-not-whole-feature-closed')
        self.assertEqual(row['runtime_status'],'not-executed')
        self.assertIn('7B4',row['disposition'])

    def test_15_nonregex_screen_is_explicit_inventory_only_not_silently_excluded(self):
        p='SmartAuditERP/Form_WPF/frmAccountBalance.xaml'
        row=b3.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
        self.assertIn('nonregex',row['selection_basis'])
        self.assertEqual(row['coverage_level'],'inventory-only-not-implementation-reviewed')
        self.assertEqual(row['phase7B3_body_ranges'],'none')

    def test_16_launcher_ranges_do_not_cover_its_children(self):
        parent='SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml';child='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml'
        inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        rows=b3.build_screen_disposition(inv,[('7B3',[self.scope(parent+'.cs','1-10')])])
        by={x['screen']:x for x in rows}
        self.assertIn('local-body',by['frmNkdFoundRpt']['coverage_level'])
        self.assertEqual(by['frmActsInvTotal']['coverage_level'],'inventory-only-not-implementation-reviewed')
        self.assertEqual(by['frmActsInvTotal']['selected_phase_ids'],'none')

    def test_17_inventory_only_feature_cannot_be_promoted_or_closed(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b3.feature_level_errors([row]),[])
        self.assertTrue(b3.feature_level_errors([row|{'coverage_level':'selected-source-slices'}]))
        self.assertTrue(b3.feature_level_errors([row|{'implementation_status':'complete'}]))

    def test_18_missing_reverse_acceptance_link_is_rejected(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b3.bidirectional_errors(pool,tests,'feature_ids'))
        pool[0]['acceptance_ids']='T1;T2'
        self.assertEqual(b3.bidirectional_errors(pool,tests,'feature_ids'),[])


if __name__=='__main__':unittest.main()
