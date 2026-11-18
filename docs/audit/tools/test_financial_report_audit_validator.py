#!/usr/bin/env python3
"""Synthetic self-tests of the NEW documentary-checker helpers, NOT ERP tests.

No application imports/build/network/SQL/COM/device execution or file writes.
The protected previous10+14 tests remain byte-for-byte unchanged.
"""
from __future__ import annotations
import copy
from pathlib import Path
from types import SimpleNamespace
import unittest
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_financial_report_part as b2


class FinancialReportAuditTests(unittest.TestCase):
    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[{'id':'LIVE:'+p}])

    def texts(self):return {name:'FROZEN:'+name for name in b2.SHARED_DOCS}

    def old(self):
        return [dict(id='P1-X',severity='High',certainty='confirmed',type='test-only',status='open-not-remediated',title='synthetic',evidence='a.cs:1-2',next_phase='7;8')]

    def extended(self):
        old=self.old();new=copy.deepcopy(old);new[0]['evidence']+=';b.cs:3-4'
        return old,new,[dict(finding_ids='P1-X',evidence='b.cs:3-4')]

    def item(self,path='a.cs',lines='10',kind='csharp-source'):
        return dict(path=path,lines=lines,kind=kind)

    def scope(self,path='a.cs',ranges='2-4'):
        return dict(path=path,ranges=ranges,review_state='synthetic-only-not-semantic-coverage')

    def test_01_virtual_index_uses_frozen_text_at_original_path(self):
        fake=self.fake()
        with b2.historical_b1_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.read(fake.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_same_basename_elsewhere_is_not_overlaid(self):
        fake=self.fake()
        with b2.historical_b1_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')

    def test_03_registry_returns_fresh_copy(self):
        fake=self.fake();old=self.old()
        with b2.historical_b1_inputs(fake,old,self.texts()):
            first=fake.rows('findings.csv');first[0]['title']='changed'
            self.assertEqual(fake.rows('findings.csv')[0]['title'],'synthetic')
            self.assertEqual(old[0]['title'],'synthetic')

    def test_04_other_csv_is_forwarded(self):
        fake=self.fake()
        with b2.historical_b1_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.rows('other.csv'),[{'id':'LIVE:other.csv'}])

    def test_05_normal_exit_restores_original_function_identities(self):
        fake=self.fake();read,rows=fake.read,fake.rows
        with b2.historical_b1_inputs(fake,self.old(),self.texts()):pass
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)

    def test_06_exception_restores_original_function_identities(self):
        fake=self.fake();read,rows=fake.read,fake.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b2.historical_b1_inputs(fake,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)

    def test_07_missing_or_extra_shared_index_rejected(self):
        for bad in ({},self.texts()|{'EXTRA.md':'x'}):
            with self.assertRaises(ValueError):
                with b2.historical_b1_inputs(self.fake(),self.old(),bad):pass

    def test_08_nontext_snapshot_value_rejected(self):
        bad=self.texts();bad['PLAN.md']={'not':'text'}
        with self.assertRaises(ValueError):
            with b2.historical_b1_inputs(self.fake(),self.old(),bad):pass

    def test_09_exact_extension_preserves_all_core_and_schedule(self):
        old,new,manifest=self.extended()
        self.assertEqual(b2.registry_transition_errors(old,new,manifest),[])

    def test_10_historical_core_mutation_detected(self):
        old,new,manifest=self.extended();new[0]['severity']='Critical'
        self.assertTrue(any('.severity' in e for e in b2.registry_transition_errors(old,new,manifest)))

    def test_11_historical_next_phase_mutation_detected(self):
        old,new,manifest=self.extended();new[0]['next_phase']='8'
        self.assertTrue(any('.next_phase' in e for e in b2.registry_transition_errors(old,new,manifest)))

    def test_12_undeclared_or_replaced_tail_detected(self):
        old,new,manifest=self.extended()
        self.assertTrue(b2.registry_transition_errors(old,new,[]))
        new[0]['evidence']='b.cs:3-4'
        self.assertTrue(b2.registry_transition_errors(old,new,manifest))

    def test_13_manifest_cannot_repeat_root_or_use_unknown_root(self):
        old,new,manifest=self.extended()
        self.assertTrue(any('Duplicate' in e for e in b2.registry_transition_errors(old,new,manifest*2)))
        self.assertTrue(any('unknown' in e for e in b2.registry_transition_errors(old,new,[dict(finding_ids='UNKNOWN',evidence='x') ])))

    def test_14_registry_truncation_or_reorder_detected(self):
        old=self.old()+[self.old()[0]|{'id':'P1-Y'}]
        self.assertTrue(b2.registry_transition_errors(old,old[:1],[]))
        self.assertTrue(b2.registry_transition_errors(old,list(reversed(old)),[]))

    def test_15_b2_ledger_keeps_old_ranges_and_closed_complement(self):
        labelled=[('7A',[self.scope(ranges='2-3')]),('7B2',[self.scope(ranges='7-8')])]
        row=b2.build_current_ledger([self.item()],labelled,v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8')
        self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(row['phase7B2_ranges'],'7-8')
        self.assertIn('not-closed',row['continuation_bucket'])

    def test_16_binary_generated_artifact_not_report_execution(self):
        row=b2.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed')
        self.assertEqual(row['runtime_status'],'not-executed')
        self.assertIn('not-authorized',row['continuation_bucket'])

    def test_17_name_only_report_candidate_is_not_a_closed_feature(self):
        row=b2.build_candidate_disposition([self.item('frmRptExample.cs')],[])[0]
        self.assertEqual(row['coverage_state'],'name-only-no-selected-scope')
        self.assertEqual(row['phase7B2_ranges'],'none')
        self.assertIn('exclusion-required',row['disposition'])

    def test_18_fingerprint_false_positive_is_explicit(self):
        row=b2.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0]
        self.assertIn('lexical-false-positive',row['disposition'])
        self.assertIn('7C',row['disposition'])

    def test_19_candidate_with_ranges_still_not_whole_feature_closed(self):
        row=b2.build_candidate_disposition([self.item('frmRptExample.cs')],[('7B2',[self.scope('frmRptExample.cs','1-10')])])[0]
        self.assertEqual(row['coverage_state'],'selected-slices-not-whole-feature-closed')
        self.assertEqual(row['runtime_status'],'not-executed')

    def test_20_reverse_acceptance_mutation_detected(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')]
        tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b2.bidirectional_errors(pool,tests,'feature_ids'))
        pool[0]['acceptance_ids']='T1;T2'
        self.assertEqual(b2.bidirectional_errors(pool,tests,'feature_ids'),[])


if __name__=='__main__':unittest.main()
