#!/usr/bin/env python3
"""22 isolated synthetic B5 documentary-checker tests, NOT ERP tests.

Only artificial dictionaries/ranges/path labels. No application import, SQL,
WPF/Office, provider, formula interpreter, binary, network or file writes.
The protected 82 earlier checker tests are not modified or reclassified.
"""
from __future__ import annotations
import copy
from pathlib import Path
from types import SimpleNamespace
import sys,unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_sales_report_part as b5
from validate_invoice_analysis_part import historical_b3_inputs


class SalesReportAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[{'id':'LIVE:'+p}])
    def texts(self):return {name:'FROZEN:'+name for name in b5.SHARED_DOCS}
    def old(self,n=261):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def transition(self):
        old=self.old(2);current=copy.deepcopy(old);current[0]['evidence']+=';b.cs:3-4'
        return old,current,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-ranges-not-semantic-coverage')
    def metadata(self):return dict(phase='7B5-partial-static-audit',application_code_imported_or_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=20,static_lexical_contract_check_count=20)

    def test_01_frozen261_and_exact_index_paths(self):
        fake=self.fake()
        with b5.historical_b4_inputs(fake,self.old(),self.texts()):
            self.assertEqual(fake.read(fake.AUDIT/'README.md'),'FROZEN:README.md');self.assertEqual(len(fake.rows('findings.csv')),261)

    def test_02_same_basename_elsewhere_is_not_overlaid(self):
        fake=self.fake()
        with b5.historical_b4_inputs(fake,self.old(),self.texts()):self.assertEqual(fake.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')

    def test_03_registry_copy_and_other_inputs_forwarded(self):
        fake=self.fake();old=self.old()
        with b5.historical_b4_inputs(fake,old,self.texts()):
            rows=fake.rows('findings.csv');rows[0]['title']='MUTATED'
            self.assertEqual(fake.rows('findings.csv')[0]['title'],'synthetic');self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(fake.rows('other.csv'),[dict(id='LIVE:other.csv')])

    def test_04_read_and_rows_restored_after_normal_or_exceptional_exit(self):
        fake=self.fake();read,rows=fake.read,fake.rows
        with b5.historical_b4_inputs(fake,self.old(),self.texts()):pass
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b5.historical_b4_inputs(fake,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)

    def test_05_wrong_count_or_duplicate_historical_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(260),self.old(262),duplicate):
            with self.assertRaises(ValueError):
                with b5.historical_b4_inputs(self.fake(),bad,self.texts()):pass

    def test_06_exact_three_string_index_texts_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b5.historical_b4_inputs(self.fake(),self.old(),bad):pass

    def test_07_nested_history_restores_the_outer_cutoff(self):
        fake=self.fake();original=fake.rows;inner={name:'B3:'+name for name in b5.SHARED_DOCS}
        with b5.historical_b4_inputs(fake,self.old(),self.texts()):
            with historical_b3_inputs(fake,self.old(248),inner):
                self.assertEqual(len(fake.rows('findings.csv')),248);self.assertEqual(fake.read(fake.AUDIT/'PLAN.md'),'B3:PLAN.md')
            self.assertEqual(len(fake.rows('findings.csv')),261);self.assertEqual(fake.read(fake.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
        self.assertIs(fake.rows,original)

    def test_08_each_historical_core_mutation_is_rejected(self):
        for field,value in (('severity','Critical'),('certainty','potential'),('type','different'),('title','altered'),('status','closed')):
            old,current,manifest=self.transition();current[0][field]=value
            self.assertTrue(any('.'+field in x for x in b5.registry_transition_errors(old,current,manifest)))

    def test_09_followups_preserved_for_unextended_rows_too(self):
        old,current,manifest=self.transition();self.assertEqual(b5.registry_transition_errors(old,current,manifest),[])
        current[1]['next_phase']='8';self.assertTrue(any('.next_phase' in x for x in b5.registry_transition_errors(old,current,manifest)))

    def test_10_missing_unknown_duplicate_or_replaced_tail_rejected(self):
        old,current,manifest=self.transition()
        for bad in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b5.registry_transition_errors(old,current,bad))
        current[0]['evidence']='b.cs:3-4';self.assertTrue(b5.registry_transition_errors(old,current,manifest))

    def test_11_b5_ranges_and_complement_are_bookkeeping_only(self):
        row=b5.build_current_ledger([self.item()],[('7A',[self.scope(ranges='2-3')]),('7B5',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(row['phase7B5_ranges'],'7-8');self.assertIn('not-closed',row['continuation_bucket']);self.assertEqual(row['runtime_status'],'not-executed')

    def test_12_binary_metadata_is_not_executable_coverage(self):
        row=b5.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',row['continuation_bucket'])

    def test_13_regex_false_positive_is_not_a_report_feature(self):
        rows=b5.build_candidate_disposition([self.item('FingerPrintDevice.cs'),self.item('frmRptExample.cs')],[])
        self.assertIn('lexical-false-positive',rows[0]['disposition']);self.assertEqual(rows[1]['phase7B5_ranges'],'none');self.assertIn('7B6',rows[1]['disposition'])

    def test_14_all_source_lines_do_not_certify_feature_completion(self):
        p='frmRptExample.cs';row=b5.build_candidate_disposition([self.item(p)],[('7B5',[self.scope(p,'1-10')])])[0]
        self.assertEqual(row['coverage_state'],'selected-slices-not-whole-feature-closed');self.assertEqual(row['runtime_status'],'not-executed');self.assertIn('required',row['disposition'])

    def test_15_curated_nonregex_child_is_inventory_only(self):
        p='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml';row=b5.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
        self.assertIn('nonregex',row['selection_basis']);self.assertEqual(row['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertEqual(row['phase7B5_body_ranges'],'none')

    def test_16_launcher_scope_does_not_promote_a_child(self):
        parent='SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml';child='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml'
        inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        by={x['screen']:x for x in b5.build_screen_disposition(inv,[('7B3',[self.scope(parent+'.cs','1-10')])])}
        self.assertIn('local-body',by['frmNkdFoundRpt']['coverage_level']);self.assertEqual(by['frmActsInvTotal']['coverage_level'],'inventory-only-not-implementation-reviewed')

    def test_17_confusable_pos_screens_are_not_interchangeable(self):
        parent='SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml';child='SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml'
        inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        by={x['screen']:x for x in b5.build_screen_disposition(inv,[('7B5',[self.scope(parent+'.cs','1-10')])])}
        self.assertEqual(by['frmRptItemsSalesDetailsPOS']['phase7B5_body_ranges'],'1-10');self.assertEqual(by['frmItemsalesdetailsPos']['phase7B5_body_ranges'],'none')
        self.assertEqual(by['frmItemsalesdetailsPos']['coverage_level'],'inventory-only-not-implementation-reviewed')

    def test_18_deferred_rows_cannot_be_promoted_or_closed(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b5.feature_level_errors([row]),[])
        for bad in (row|{'coverage_level':'selected-source-slices'},row|{'implementation_status':'complete'}):self.assertTrue(b5.feature_level_errors([bad]))

    def test_19_reverse_acceptance_links_must_be_exact(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b5.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b5.bidirectional_errors(pool,tests,'feature_ids'),[])

    def test_20_contract_and_resource_leads_are_not_certified(self):
        for state in ('reviewed-contract-unresolved-not-global-absence','source-only-resource-performance-lead-not-runtime-measured'):
            row=dict(id='FE-X',implementation_status=state,coverage_level='selected-source-slices-not-whole-feature-certification',evidence='a.cs:2-3')
            self.assertEqual(b5.feature_level_errors([row]),[]);self.assertTrue(b5.feature_level_errors([row|{'implementation_status':'runtime-certified'}]))

    def test_21_false_execution_flags_cannot_be_set_or_omitted(self):
        self.assertEqual(b5.witness_metadata_errors(self.metadata()),[])
        for field in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for value in (True,None,0):self.assertTrue(b5.witness_metadata_errors(self.metadata()|{field:value}))

    def test_22_execution_counts_phase_and_illustration_counts_are_not_acceptance(self):
        for field in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for value in (1,None,False,'0'):self.assertTrue(b5.witness_metadata_errors(self.metadata()|{field:value}))
        for bad in ({'phase':'runtime-certified'},{'illustration_count':19},{'static_lexical_contract_check_count':21}):self.assertTrue(b5.witness_metadata_errors(self.metadata()|bad))


if __name__=='__main__':unittest.main()
