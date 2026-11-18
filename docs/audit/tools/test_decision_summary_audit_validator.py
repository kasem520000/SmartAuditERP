#!/usr/bin/env python3
"""28 isolated synthetic B8 documentation-checker tests, NOT ERP tests.

Artificial dictionaries/ranges/text/path labels only. No application imports,
build/SQL/WPF/Office/provider/device/formula execution or filesystem writes.
The protected156 prior checker cases and original827 hash guards stay intact.
"""
from __future__ import annotations
import copy,sys,unittest
from pathlib import Path
from types import SimpleNamespace
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_decision_summary_part as b8
from validate_financial_controls_part import historical_b6_inputs


class DecisionSummaryAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[dict(id='LIVE:'+p)])
    def texts(self):return {n:'FROZEN:'+n for n in b8.SHARED_DOCS}
    def old(self,n=276):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def transition(self):
        old=self.old(2);now=copy.deepcopy(old);now[0]['evidence']+=';b.cs:3-4'
        return old,now,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-ranges-not-semantic-coverage')
    def metadata(self):return dict(phase='7B8-partial-static-audit',application_code_imported_or_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=20,static_lexical_contract_check_count=20)
    def groups(self):return '\n'.join(f'| G-{n:02d} | kept exactly |' for n in range(1,123))+'\n'

    def test_01_frozen276_and_exact_logical_paths(self):
        f=self.fake()
        with b8.historical_b7_inputs(f,self.old(),self.texts()):
            self.assertEqual(len(f.rows('findings.csv')),276)
            for name in b8.SHARED_DOCS:self.assertEqual(f.read(f.AUDIT/name),'FROZEN:'+name)

    def test_02_normal_exit_restores_reader_and_registry(self):
        f=self.fake();read,rows=f.read,f.rows
        with b8.historical_b7_inputs(f,self.old(),self.texts()):pass
        self.assertIs(f.read,read);self.assertIs(f.rows,rows)

    def test_03_exception_restores_reader_and_registry(self):
        f=self.fake();read,rows=f.read,f.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with b8.historical_b7_inputs(f,self.old(),self.texts()):raise RuntimeError('synthetic')
        self.assertIs(f.read,read);self.assertIs(f.rows,rows)

    def test_04_no_basename_overlay_or_snapshot_alias_mutation(self):
        f=self.fake();old=self.old()
        with b8.historical_b7_inputs(f,old,self.texts()):
            self.assertEqual(f.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            f.rows('findings.csv')[0]['title']='ALTERED';self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic');self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')])

    def test_05_wrong_count_or_duplicate_historical_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(270),self.old(275),self.old(277),duplicate):
            with self.assertRaises(ValueError):
                with b8.historical_b7_inputs(self.fake(),bad,self.texts()):pass

    def test_06_exact_three_shared_index_string_values_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b8.historical_b7_inputs(self.fake(),self.old(),bad):pass

    def test_07_nested_b6_adapter_restores_outer_b7_cutoff(self):
        f=self.fake()
        with b8.historical_b7_inputs(f,self.old(),self.texts()):
            with historical_b6_inputs(f,self.old(270),{n:'B6:'+n for n in b8.SHARED_DOCS}):
                self.assertEqual(len(f.rows('findings.csv')),270);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B6:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')),276);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')

    def test_08_current_range_union_and_line_complement_are_bookkeeping_only(self):
        x=b8.build_current_ledger([self.item()],[('7B7',[self.scope(ranges='2-3')]),('7B8',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(x['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(x['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(x['phase7B7_ranges'],'2-3');self.assertEqual(x['phase7B8_ranges'],'7-8');self.assertIn('not-closed',x['continuation_bucket']);self.assertEqual(x['runtime_status'],'not-executed')

    def test_09_all_lines_do_not_close_a_feature(self):
        p='frmRptExample.cs';x=b8.build_candidate_disposition([self.item(p)],[('7B8',[self.scope(p,'1-10')])])[0]
        self.assertEqual(x['coverage_state'],'selected-slices-not-whole-feature-closed');self.assertEqual(x['phase7B8_ranges'],'1-10');self.assertIn('required',x['disposition'])

    def test_10_binary_metadata_never_execution_coverage(self):
        x=b8.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(x['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',x['continuation_bucket'])

    def test_11_each_of_three_actual_bodies_requires_its_own_scope(self):
        for name in b8.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv=[self.item(p),self.item(p+'.cs')]
            before=b8.build_screen_disposition(inv,[])[0];after=b8.build_screen_disposition(inv,[('7B8',[self.scope(p+'.cs','1-10')])])[0]
            self.assertEqual(before['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertEqual(after['phase7B8_body_ranges'],'1-10');self.assertIn('not-whole-feature',after['coverage_level'])

    def test_12_parent_does_not_promote_another_body(self):
        parent='SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml';child='SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml';inv=[self.item(parent),self.item(parent+'.cs'),self.item(child),self.item(child+'.cs')]
        by={x['screen']:x for x in b8.build_screen_disposition(inv,[('7B8',[self.scope(parent+'.cs','1-10')])])}
        self.assertEqual(by['frmNkdTotSalePurchActCust']['coverage_level'],'inventory-only-not-implementation-reviewed')

    def test_13_body_names_without_own_selected_ranges_not_promoted(self):
        inv=[]
        for name in b8.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv += [self.item(p),self.item(p+'.cs')]
        for x in b8.build_screen_disposition(inv,[]):
            self.assertEqual(x['phase7B8_body_ranges'],'none');self.assertEqual(x['coverage_level'],'inventory-only-not-implementation-reviewed');self.assertIn('required',x['disposition'])

    def test_14_fingerprint_lexical_match_not_a_business_report(self):
        x=b8.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0]
        self.assertIn('lexical-false-positive',x['disposition']);self.assertEqual(x['runtime_status'],'not-executed')

    def test_15_each_historical_core_field_change_rejected(self):
        for field,value in (('title','changed'),('severity','Critical'),('certainty','potential'),('type','other'),('status','closed')):
            old,now,manifest=self.transition();now[0][field]=value
            self.assertTrue(any('.'+field in e for e in b8.registry_transition_errors(old,now,manifest)))

    def test_16_followups_preserved_even_without_evidence_tail(self):
        old,now,manifest=self.transition();self.assertEqual(b8.registry_transition_errors(old,now,manifest),[])
        now[1]['next_phase']='8';self.assertTrue(any('.next_phase' in e for e in b8.registry_transition_errors(old,now,manifest)))

    def test_17_missing_duplicate_unknown_tail_manifest_rejected(self):
        old,now,manifest=self.transition()
        for bad in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b8.registry_transition_errors(old,now,bad))

    def test_18_replacement_or_extra_undeclared_evidence_tail_rejected(self):
        old,now,manifest=self.transition();now[0]['evidence']='b.cs:3-4';self.assertTrue(b8.registry_transition_errors(old,now,manifest))
        old,now,manifest=self.transition();now[0]['evidence']+=';c.cs:5-6';self.assertTrue(b8.registry_transition_errors(old,now,manifest))

    def test_19_exact122_group_rows_allow_new_rows_only_after_prefix(self):
        prior=self.groups();self.assertEqual(b8.group_row_errors(prior,prior+'| G-123 | new |\n'),[])

    def test_20_group_row_whitespace_removal_reorder_and_old_count_rejected(self):
        prior=self.groups()
        for changed in (prior.replace('kept exactly','kept  exactly',1),prior.replace('| G-01 | kept exactly |\n',''),prior.replace('| G-01 |','| G-02 |',1)):
            self.assertTrue(b8.group_row_errors(prior,changed))
        self.assertTrue(b8.group_row_errors(prior+'| G-123 | old extra |\n',prior))

    def test_21_reverse_plan_links_must_be_exact(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b8.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b8.bidirectional_errors(pool,tests,'feature_ids'),[])

    def test_22_deferred_or_closed_features_cannot_be_promoted(self):
        x=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b8.feature_level_errors([x]),[])
        for bad in (x|{'coverage_level':'source-reviewed'},x|{'implementation_status':'complete'},x|{'evidence':'some.cs:1-10'}):self.assertTrue(b8.feature_level_errors([bad]))

    def test_23_execution_metadata_flags_are_false_only_and_counts_integer_zero(self):
        self.assertEqual(b8.witness_metadata_errors(self.metadata()),[])
        for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for val in (True,None,0):self.assertTrue(b8.witness_metadata_errors(self.metadata()|{key:val}))
        for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for val in (1,None,False,'0'):self.assertTrue(b8.witness_metadata_errors(self.metadata()|{key:val}))

    def test_24_phase_and_exact_witness_counts_not_runtime_acceptance(self):
        for bad in ({'phase':'runtime-certified'},{'illustration_count':19},{'illustration_count':20.0},{'static_lexical_contract_check_count':21},{'static_lexical_contract_check_count':None}):self.assertTrue(b8.witness_metadata_errors(self.metadata()|bad))


    def test_25_historical_name_maps_to_actual_body_not_a_fourth_screen(self):
        self.assertEqual(b8.HISTORICAL_NAME_ALIASES,{'frmUsersRecords':'frmrptUsersRecords'})
        self.assertNotIn('frmUsersRecords',b8.REVIEWED_BODIES)
        self.assertIn('frmrptUsersRecords',b8.REVIEWED_BODIES)

    def test_26_actual_log_body_needs_own_range_and_preserves_alias_annotation(self):
        p='SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml'
        inv=[self.item(p),self.item(p+'.cs')]
        x=b8.build_screen_disposition(inv,[('7B8',[self.scope(p+'.cs','1-10')])])[0]
        self.assertEqual(x['screen'],'frmrptUsersRecords');self.assertEqual(x['phase7B8_body_ranges'],'1-10')
        self.assertIn('historical artifacts unchanged',x['historical_name_mapping'])
        self.assertIn('not-whole-feature',x['coverage_level'])

    def test_27_no_source_sentinels_are_declared_and_cannot_be_promoted(self):
        errors=[];calls=[]
        f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**kw:calls.append(a))
        b8.validate_source(f,dict(id='FE7B8-27',evidence='none-inventory-only'),{})
        self.assertEqual(errors,[]);self.assertEqual(calls,[])
        b8.validate_source(f,dict(id='FE7B8-27',evidence='x.cs:1-2'),{})
        self.assertTrue(errors)
        errors.clear();b8.validate_source(f,dict(id='FE7B8-01',evidence='none-inventory-only'),{})
        self.assertTrue(errors)

    def test_28_all_plan_rows_counted_as_unexecuted_not_checker_tests(self):
        specs={name:(prefix,count) for name,prefix,count in b8.TABLE_SPECS}
        self.assertEqual(specs['acceptance-tests'],('P7B8T-',32))
        self.assertEqual(specs['feature-implementation-matrix'],('FE7B8-',28))
        errors=[];old=v.ERRORS;v.ERRORS=errors
        try:
            row={k:'synthetic-only' for k in ('scenario','prerequisites','procedure','acceptance_criterion','safety_controls','invariant_ids','evidence')}
            row.update(id='P7B8T-01',status='not-executed');v.proposed_tests([row],'7B8')
            self.assertEqual(errors,[]);row['status']='passed';v.proposed_tests([row],'7B8');self.assertTrue(errors)
        finally:v.ERRORS=old


if __name__=='__main__':unittest.main()
