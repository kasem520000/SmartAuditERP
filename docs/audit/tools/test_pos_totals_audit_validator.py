#!/usr/bin/env python3
"""28 isolated synthetic B6 documentary-checker tests, NOT ERP tests.

Artificial dictionaries/ranges/path labels and a fake Git callback only.
No application import/build/SQL/WPF/Office/provider, file writes or network.
Original827 hash checks stay mandatory in the main validator, not replaced by
these identity fixtures. The protected104 prior checker cases are unchanged.
"""
from __future__ import annotations
import copy
from pathlib import Path
from types import SimpleNamespace
import subprocess,sys,unittest
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_pos_totals_part as b6
import audit_source_identity as identity
from validate_sales_report_part import historical_b4_inputs


class PosTotalsAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[dict(id='LIVE:'+p)])
    def texts(self):return {n:'FROZEN:'+n for n in b6.SHARED_DOCS}
    def old(self,n=266):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def transition(self):
        old=self.old(2);current=copy.deepcopy(old);current[0]['evidence']+=';b.cs:3-4'
        return old,current,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-ranges-not-semantic-coverage')
    def metadata(self):return dict(phase='7B6-partial-static-audit',application_code_imported_or_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=20,static_lexical_contract_check_count=20)
    def bind(self,**kw):return identity.identity_errors(kw.get('reference','a'*40),kw.get('checkout','b'*40),kw.get('ancestor',True),kw.get('paths',['docs/audit/report.md']))

    def test_01_frozen266_and_exact_logical_paths(self):
        fake=self.fake()
        with b6.historical_b5_inputs(fake,self.old(),self.texts()):
            self.assertEqual(len(fake.rows('findings.csv')),266);self.assertEqual(fake.read(fake.AUDIT/'README.md'),'FROZEN:README.md')

    def test_02_restoration_on_normal_and_exceptional_exit(self):
        fake=self.fake();read,rows=fake.read,fake.rows
        with b6.historical_b5_inputs(fake,self.old(),self.texts()):pass
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b6.historical_b5_inputs(fake,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(fake.read,read);self.assertIs(fake.rows,rows)

    def test_03_no_basename_overlay_no_alias_mutation_others_forwarded(self):
        fake=self.fake();old=self.old()
        with b6.historical_b5_inputs(fake,old,self.texts()):
            self.assertEqual(fake.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            fake.rows('findings.csv')[0]['title']='ALTERED';self.assertEqual(fake.rows('findings.csv')[0]['title'],'synthetic');self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(fake.rows('other.csv'),[dict(id='LIVE:other.csv')])

    def test_04_wrong_count_and_duplicate_ids_rejected(self):
        dupe=self.old();dupe[-1]['id']=dupe[0]['id']
        for bad in (self.old(265),self.old(267),dupe):
            with self.assertRaises(ValueError):
                with b6.historical_b5_inputs(self.fake(),bad,self.texts()):pass

    def test_05_exact_three_string_shared_texts_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b6.historical_b5_inputs(self.fake(),self.old(),bad):pass

    def test_06_nested_b4_restores_outer_b5_cutoff(self):
        fake=self.fake()
        with b6.historical_b5_inputs(fake,self.old(),self.texts()):
            with historical_b4_inputs(fake,self.old(261),{n:'B4:'+n for n in b6.SHARED_DOCS}):
                self.assertEqual(len(fake.rows('findings.csv')),261);self.assertEqual(fake.read(fake.AUDIT/'PLAN.md'),'B4:PLAN.md')
            self.assertEqual(len(fake.rows('findings.csv')),266);self.assertEqual(fake.read(fake.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')

    def test_07_all_lines_do_not_close_a_feature(self):
        p='frmRptExample.cs';x=b6.build_candidate_disposition([self.item(p)],[('7B6',[self.scope(p,'1-10')])])[0]
        self.assertEqual(x['coverage_state'],'selected-slices-not-whole-feature-closed');self.assertEqual(x['phase7B6_ranges'],'1-10');self.assertIn('required',x['disposition'])

    def test_08_each_old_core_change_rejected(self):
        for field,value in (('title','changed'),('severity','Critical'),('certainty','potential'),('type','different'),('status','closed')):
            old,current,manifest=self.transition();current[0][field]=value
            self.assertTrue(any('.'+field in e for e in b6.registry_transition_errors(old,current,manifest)))

    def test_09_followups_preserved_for_unextended_rows(self):
        old,current,manifest=self.transition();self.assertEqual(b6.registry_transition_errors(old,current,manifest),[])
        current[1]['next_phase']='8';self.assertTrue(any('.next_phase' in e for e in b6.registry_transition_errors(old,current,manifest)))

    def test_10_missing_duplicate_unknown_or_replaced_tail_rejected(self):
        old,current,manifest=self.transition()
        for bad in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b6.registry_transition_errors(old,current,bad))
        current[0]['evidence']='b.cs:3-4';self.assertTrue(b6.registry_transition_errors(old,current,manifest))

    def test_11_b6_range_union_and_complement_bookkeeping_only(self):
        x=b6.build_current_ledger([self.item()],[('7A',[self.scope(ranges='2-3')]),('7B6',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(x['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(x['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(x['phase7B6_ranges'],'7-8');self.assertIn('not-closed',x['continuation_bucket']);self.assertEqual(x['runtime_status'],'not-executed')

    def test_12_binary_metadata_never_execution_coverage(self):
        x=b6.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(x['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',x['continuation_bucket'])

    def test_13_curated_child_review_requires_its_own_selected_body(self):
        p='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml';inv=[self.item(p),self.item(p+'.cs')]
        before=b6.build_screen_disposition(inv,[])[0];after=b6.build_screen_disposition(inv,[('7B6',[self.scope(p+'.cs','1-10')])])[0]
        self.assertIn('nonregex',before['selection_basis']);self.assertEqual(before['coverage_level'],'inventory-only-not-implementation-reviewed')
        self.assertEqual(after['phase7B6_body_ranges'],'1-10');self.assertIn('not-whole-feature',after['coverage_level'])

    def test_14_launcher_does_not_promote_another_child(self):
        parent='SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml';child='SmartAuditERP/Form_WPF/frmActsInvTotal.xaml';inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        by={x['screen']:x for x in b6.build_screen_disposition(inv,[('7B6',[self.scope(parent+'.cs','1-10')])])}
        self.assertEqual(by['frmActsInvTotal']['coverage_level'],'inventory-only-not-implementation-reviewed')

    def test_15_confusable_pos_bodies_remain_separate(self):
        prior='SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml';now='SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml';inv=[self.item(prior),self.item(prior+'.cs'),self.item(now),self.item(now+'.cs')]
        by={x['screen']:x for x in b6.build_screen_disposition(inv,[('7B5',[self.scope(prior+'.cs','1-10')]),('7B6',[self.scope(now+'.cs','1-10')])])}
        self.assertEqual(by['frmRptItemsSalesDetailsPOS']['phase7B6_body_ranges'],'none');self.assertEqual(by['frmItemsalesdetailsPos']['phase7B6_body_ranges'],'1-10')

    def test_16_fingerprint_regex_match_is_not_a_business_report(self):
        x=b6.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0]
        self.assertIn('lexical-false-positive',x['disposition']);self.assertEqual(x['runtime_status'],'not-executed')

    def test_17_deferred_features_cannot_be_promoted_or_closed(self):
        x=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b6.feature_level_errors([x]),[])
        for bad in (x|{'coverage_level':'source-reviewed'},x|{'implementation_status':'complete'}):self.assertTrue(b6.feature_level_errors([bad]))

    def test_18_exact_reverse_plan_associations_required(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b6.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b6.bidirectional_errors(pool,tests,'feature_ids'),[])

    def test_19_false_only_execution_flags_not_omitted_or_coerced(self):
        self.assertEqual(b6.witness_metadata_errors(self.metadata()),[])
        for field in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for value in (True,None,0):self.assertTrue(b6.witness_metadata_errors(self.metadata()|{field:value}))

    def test_20_exact_counts_and_phase_not_runtime_acceptance(self):
        for field in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for value in (1,None,False,'0'):self.assertTrue(b6.witness_metadata_errors(self.metadata()|{field:value}))
        for bad in ({'phase':'runtime-certified'},{'illustration_count':19},{'static_lexical_contract_check_count':21}):self.assertTrue(b6.witness_metadata_errors(self.metadata()|bad))

    def test_21_same_source_checkout_no_delta_accepted(self):self.assertEqual(self.bind(checkout='a'*40,paths=[]),[])

    def test_22_docs_only_descendant_delta_accepted(self):self.assertEqual(self.bind(paths=['docs/audit/report.md','docs/audit/evidence/checks.json']),[])

    def test_23_ancestry_must_be_boolean_true(self):
        for ancestor in (False,None,1,'true'):self.assertTrue(self.bind(ancestor=ancestor))

    def test_24_full_hex_source_and_checkout_identities_required(self):
        for value in ('HEAD','a'*39,'A'*40,'g'*40,None):
            self.assertTrue(self.bind(reference=value));self.assertTrue(self.bind(checkout=value))

    def test_25_any_application_or_nonaudit_delta_rejected(self):
        for p in ('SmartAuditERP/Class/ItemOper.cs','SmartAuditUpdater/app.config','SmartAuditERP.sln','README.md','docs/other.md','docs/auditor/f.md'):
            self.assertTrue(self.bind(paths=['docs/audit/report.md',p]))

    def test_26_canonical_audit_paths_no_traversal_or_controls(self):
        for p in ('/docs/audit/x','docs/audit/../x','docs/audit/./x','docs/audit//x','docs/audit/x/','docs/audit/x\\y','docs/audit'):
            self.assertTrue(self.bind(paths=[p]),p)
        for code in (*range(32),127):
            p='docs/audit/x'+chr(code)+'y';self.assertTrue(self.bind(paths=[p]),repr(p))

    def test_27_contradictory_deltas_duplicates_and_bad_types_rejected(self):
        self.assertTrue(self.bind(checkout='a'*40));self.assertTrue(self.bind(paths=[]))
        for paths in (['docs/audit/x']*2,None,'docs/audit/x',[None]):self.assertTrue(self.bind(paths=paths))

    def test_28_inspection_fake_git_ancestry_failure_not_suppressed(self):
        calls=[]
        def fake(*args):
            calls.append(args)
            if args==('rev-parse','HEAD'):return 'b'*40
            if args[0]=='merge-base':raise subprocess.CalledProcessError(1,['git',*args])
            if args[0]=='diff':return 'docs/audit/report.md\0'
            raise AssertionError(args)
        meta,errors=identity.inspect_identity('a'*40,fake)
        self.assertTrue(errors);self.assertIs(meta['reference_ancestor_of_checkout'],False);self.assertIs(meta['all_committed_net_delta_paths_under_docs_audit'],False)
        self.assertTrue(meta['original827_paths_and_hashes_checked_separately']);self.assertEqual(meta['committed_net_delta_path_count'],1);self.assertEqual(len(calls),3)


if __name__=='__main__':unittest.main()
