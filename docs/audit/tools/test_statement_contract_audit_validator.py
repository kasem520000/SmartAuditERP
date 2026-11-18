#!/usr/bin/env python3
"""30 isolated B11 synthetic DOCUMENTATION-checker cases, NOT ERP tests.

Artificial dictionaries, inert ranges/text and an in-memory exact-path overlay;
no app import/build/SQL/WPF/Office/export/shell, real data or filesystem writes.
Prior236 checker cases remain protected; these add30, not25 passed ERP plans.
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
import validate_statement_contract_part as b11
from validate_salesman_contract_part import historical_b9_inputs


class StatementContractAuditTests(unittest.TestCase):
    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),
            rows=lambda p:[dict(id='LIVE:'+p)])
    def old(self,n=285):
        return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',
            type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def raw(self,old=None):
        old=self.old() if old is None else old;s=io.StringIO(newline='')
        w=csv.DictWriter(s,fieldnames=list(old[0]),lineterminator='\r\n');w.writeheader();w.writerows(old)
        return s.getvalue().encode('utf-8')
    def texts(self):return {n:'FROZEN:'+n for n in b11.SHARED_DOCS}
    def context(self,f):return b11.historical_b10_inputs(f,self.old(),self.texts(),self.raw())
    def transition(self):
        old=self.old(2);now=copy.deepcopy(old);now[0]['evidence']+=';b.cs:3-4'
        return old,now,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-only')
    def groups(self,n=140):return '\n'.join(f'| G-{i:02d} | exact row |' for i in range(1,n+1))+'\n'
    def erratum(self):return dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False)
    def metadata(self):
        return dict(phase='7B11-partial-static-audit',application_code_imported_or_executed=False,
            application_remediation_performed=False,real_business_or_secret_data_used=False,
            spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,
            sql_or_external_service_tests_executed=0,illustration_count=20,static_lexical_contract_check_count=20,
            default_aggregate_gate_not_assumed_resolved=True,supplied_sql_not_certified_deployed=True,
            additive_B10_arithmetic_erratum=self.erratum())

    def test_01_exact_frozen285_rows_and_logical_index_paths(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(len(f.rows('findings.csv')),285)
            for n in b11.SHARED_DOCS:self.assertEqual(f.read(f.AUDIT/n),'FROZEN:'+n)
    def test_02_direct_registry_bytes_overlay_is_local_not_pathlib_patch(self):
        f=self.fake();method=Path.read_bytes
        with self.context(f):
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
            self.assertIs(Path.read_bytes,method)
            self.assertEqual(str(f.AUDIT/'findings.csv'),'/synthetic/audit/findings.csv')
    def test_03_normal_exit_restores_all_three_objects(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):pass
        for a,b in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(a,b)
    def test_04_exception_exit_restores_all_three_objects(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with self.context(f):raise RuntimeError('synthetic')
        for a,b in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(a,b)
    def test_05_nested_b9_restores_outer_b10_rows_text_and_bytes(self):
        f=self.fake()
        with self.context(f):
            with historical_b9_inputs(f,self.old(282),{n:'B9:'+n for n in b11.SHARED_DOCS}):
                self.assertEqual(len(f.rows('findings.csv')),282)
                self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B9:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')),285)
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
    def test_06_nested_exception_restores_outer_cutoff(self):
        f=self.fake()
        with self.context(f):
            with self.assertRaisesRegex(RuntimeError,'synthetic'):
                with historical_b9_inputs(f,self.old(282),self.texts()):raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),285)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
    def test_07_count_or_duplicate_historical_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(282),self.old(284),self.old(286),duplicate):
            with self.assertRaises(ValueError):
                with b11.historical_b10_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass
    def test_08_exact_three_string_index_texts_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'README.md':None}):
            f=self.fake();before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b11.historical_b10_inputs(f,self.old(),bad,self.raw()):pass
            for a,b in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(a,b)
    def test_09_raw_bytes_must_match_rows_noBOM_CRLF_exact_count(self):
        for bad in (None,'not bytes',b'\xef\xbb\xbf'+self.raw(),self.raw().replace(b'\r\n',b'\n'),
                    self.raw().replace(b'synthetic',b'changed',1),self.raw()+b'\r\n',b'\xff'):
            with self.assertRaises(ValueError):
                with b11.historical_b10_inputs(self.fake(),self.old(),self.texts(),bad):pass
    def test_10_returned_rows_are_deep_enough_copies_and_original_is_immutable(self):
        f=self.fake();old=self.old()
        with b11.historical_b10_inputs(f,old,self.texts(),self.raw(old)):
            f.rows('findings.csv')[0]['title']='changed'
            self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic')
            self.assertEqual(old[0]['title'],'synthetic')
            self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')])
    def test_11_no_basename_overlay_for_other_roots_or_neighbor_files(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            other=type(f.AUDIT)('/synthetic/elsewhere/findings.csv')
            with self.assertRaises(FileNotFoundError):other.read_bytes()
            with self.assertRaises(FileNotFoundError):(f.AUDIT/'not-a-registry.csv').read_bytes()
            # Successful non-target delegation too; inert checker text, no writes.
            delegated=type(f.AUDIT)(__file__)
            self.assertEqual(delegated.read_bytes(),Path(__file__).read_bytes())
    def test_12_range_union_complement_are_bookkeeping_not_coverage_certification(self):
        r=b11.build_current_ledger([self.item()],[('7B10',[self.scope(ranges='2-3')]),('7B11',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(r['declared_range_union_not_reading_certification'],'2-3;7-8')
        self.assertEqual(r['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(r['phase7B10_ranges'],'2-3');self.assertEqual(r['phase7B11_ranges'],'7-8')
        self.assertIn('not-closed',r['continuation_bucket']);self.assertEqual(r['runtime_status'],'not-executed')
    def test_13_all_lines_never_close_a_feature(self):
        p='frmRptSynthetic.cs';r=b11.build_candidate_disposition([self.item(p)],[('7B11',[self.scope(p,'1-10')])])[0]
        self.assertEqual(r['phase7B11_ranges'],'1-10')
        self.assertEqual(r['coverage_state'],'selected-slices-not-whole-feature-closed')
        self.assertIn('required',r['disposition'])
    def test_14_binary_and_fingerprint_do_not_become_report_execution(self):
        r=b11.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(r['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',r['continuation_bucket'])
        r=b11.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0]
        self.assertIn('lexical-false-positive',r['disposition'])
    def test_15_each_reviewed_body_needs_its_own_full_XAML_as_well(self):
        for name in b11.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv=[self.item(p),self.item(p+'.cs')]
            r=b11.build_screen_disposition(inv,[('7B11',[self.scope(p,'1-10'),self.scope(p+'.cs','1-10')])])[0]
            self.assertEqual(r['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
            for selected in ([self.scope(p+'.cs','1-10')],[self.scope(p,'1-9'),self.scope(p+'.cs','1-10')]):
                r=b11.build_screen_disposition(inv,[('7B11',selected)])[0]
                self.assertNotEqual(r['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
    def test_16_parent_does_not_promote_child(self):
        p='SmartAuditERP/Form_WPF/frmRptParent.xaml';c='SmartAuditERP/Form_WPF/frmRptChild.xaml'
        by={r['screen']:r for r in b11.build_screen_disposition([self.item(p),self.item(p+'.cs'),self.item(c),self.item(c+'.cs')],[('7B11',[self.scope(p+'.cs','1-10')])])}
        self.assertEqual(by['frmRptChild']['coverage_level'],'inventory-only-not-implementation-reviewed')
    def test_17_known_names_without_selected_ranges_not_promoted(self):
        for name in b11.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml'
            r=b11.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
            self.assertEqual(r['phase7B11_body_ranges'],'none')
            self.assertEqual(r['coverage_level'],'inventory-only-not-implementation-reviewed')
    def test_18_all_historical_cores_and_every_followup_immutable(self):
        for field in ('title','severity','certainty','type','status','next_phase'):
            old,now,manifest=self.transition();now[1][field]='changed'
            self.assertTrue(any('.'+field in e for e in b11.registry_transition_errors(old,now,manifest)))
    def test_19_exact_declared_tails_only(self):
        old,now,m=self.transition();self.assertEqual(b11.registry_transition_errors(old,now,m),[])
        for bad in ([],m*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b11.registry_transition_errors(old,now,bad))
        now[0]['evidence']+=';c.cs:5-6';self.assertTrue(b11.registry_transition_errors(old,now,m))
        now[0]['evidence']='b.cs:3-4';self.assertTrue(b11.registry_transition_errors(old,now,m))
    def test_20_exact140_group_prefix_allows_additive_erratum_without_rewrite(self):
        prior=self.groups();self.assertEqual(b11.group_row_errors(prior,prior+'\nAdditive erratum\n| G-141 | new |\n'),[])
    def test_21_group_whitespace_reorder_old_count_rejected(self):
        prior=self.groups()
        for bad in (prior.replace('exact row','exact  row',1),prior.replace('| G-01 |','| G-02 |',1),self.groups(139)):
            self.assertTrue(b11.group_row_errors(prior,bad))
        self.assertTrue(b11.group_row_errors(self.groups(141),prior))
    def test_22_reverse_links_must_be_exact(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b11.bidirectional_errors(pool,tests,'feature_ids'))
        pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b11.bidirectional_errors(pool,tests,'feature_ids'),[])
    def test_23_feature_vocabulary_and_inventory_sentinel_consistent(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b11.feature_level_errors([row]),[])
        for bad in (row|{'coverage_level':'source-reviewed'},row|{'evidence':'a.cs:1-2'},row|{'implementation_status':'complete'}):self.assertTrue(b11.feature_level_errors([bad]))
        row|=dict(implementation_status='reviewed-contract-unresolved-not-global-absence',coverage_level='bounded-contract-not-whole-feature',evidence='a.cs:1-2')
        self.assertEqual(b11.feature_level_errors([row]),[])
    def test_24_execution_flags_false_only_and_count_integer_zero(self):
        self.assertEqual(b11.witness_metadata_errors(self.metadata()),[])
        for k in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for x in (True,None,0):self.assertTrue(b11.witness_metadata_errors(self.metadata()|{k:x}))
        for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for x in (1,False,None,'0'):self.assertTrue(b11.witness_metadata_errors(self.metadata()|{k:x}))
    def test_25_default_aggregate_and_deployed_schema_boundaries_true_only(self):
        for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed'):
            for x in (False,None,1,'true'):self.assertTrue(b11.witness_metadata_errors(self.metadata()|{k:x}))
    def test_26_inventory_gate_has_no_fabricated_source(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append(a))
        b11.validate_source(f,dict(id='RC7B11-06',evidence='none-inventory-only'),{})
        self.assertEqual(errors,[]);self.assertEqual(calls,[])
        b11.validate_source(f,dict(id='RC7B11-06',evidence='x.cs:1-2'),{});self.assertTrue(errors)
    def test_27_bookkeeping_builders_do_not_mutate_inputs(self):
        inv=[self.item('frmRptSynthetic.cs')];labelled=[('7B11',[self.scope('frmRptSynthetic.cs','1-10')])];before=copy.deepcopy((inv,labelled))
        b11.build_current_ledger(inv,labelled,v.spans);b11.build_candidate_disposition(inv,labelled);b11.build_screen_disposition(inv,labelled)
        self.assertEqual((inv,labelled),before)
    def test_28_phase_counts_do_not_renumber_prior_roots(self):
        counts={n:c for n,_,c in b11.TABLE_SPECS}
        self.assertEqual(counts['acceptance-tests'],25);self.assertEqual(counts['feature-implementation-matrix'],23)
        self.assertEqual(len(b11.EXTENDED_FINDINGS),14)
        self.assertTrue({'P3-021','P3-022','P7-099','P7-061','P1-033'}<=b11.EXTENDED_FINDINGS)
        self.assertTrue({'P7-114','P7-115','P7-054','P7-064','P7-111','P7-113'}.isdisjoint(b11.EXTENDED_FINDINGS))
    def test_29_arithmetic_erratum_is_exact_typed_and_archive_not_rewritten(self):
        self.assertEqual(b11.arithmetic_erratum_errors(self.erratum()),[])
        for bad in (None,{},self.erratum()|{'local_cost':20},self.erratum()|{'reference_cost':10},
                    self.erratum()|{'local_cost':10.0},self.erratum()|{'archive_rewritten':True},self.erratum()|{'archive_rewritten':0}):
            self.assertTrue(b11.arithmetic_erratum_errors(bad))
    def test_30_witness_counts_types_and_erratum_are_required_not_whole_prose_certification(self):
        for patch in ({'phase':'runtime-certified'},{'illustration_count':19},{'illustration_count':20.0},
                      {'static_lexical_contract_check_count':True},{'additive_B10_arithmetic_erratum':self.erratum()|{'local_cost':20}}):
            self.assertTrue(b11.witness_metadata_errors(self.metadata()|patch))


if __name__=='__main__':unittest.main()
