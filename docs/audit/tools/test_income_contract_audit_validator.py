#!/usr/bin/env python3
"""32 isolated B12 synthetic DOCUMENTATION-checker cases, NOT ERP tests.

Artificial dictionaries/ranges/text and a local in-memory exact-path overlay;
no ERP import/build/SQL/WPF/Office/export/shell, real data or file writes.
Prior266 checker cases remain protected; these add32, not27 passed ERP plans.
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
import validate_income_contract_part as b12
from validate_statement_contract_part import historical_b10_inputs


class IncomeContractAuditTests(unittest.TestCase):
    def fake(self):return SimpleNamespace(AUDIT=Path('/synthetic/audit'),read=lambda p:'LIVE:'+str(p),rows=lambda p:[dict(id='LIVE:'+p)])
    def old(self,n=287):return [dict(id=f'P-X{i:03d}',title='synthetic',severity='High',certainty='confirmed',type='synthetic-only',status='open-not-remediated',next_phase='7;8',evidence='a.cs:1-2') for i in range(n)]
    def raw(self,old=None):
        old=self.old() if old is None else old;s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(old[0]),lineterminator='\r\n');w.writeheader();w.writerows(old);return s.getvalue().encode()
    def texts(self):return {n:'FROZEN:'+n for n in b12.SHARED_DOCS}
    def context(self,f):return b12.historical_b11_inputs(f,self.old(),self.texts(),self.raw())
    def transition(self):
        old=self.old(2);now=copy.deepcopy(old);now[0]['evidence']+=';b.cs:3-4';return old,now,[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
    def item(self,p='a.cs',lines='10',kind='csharp-source'):return dict(path=p,lines=lines,kind=kind)
    def scope(self,p='a.cs',ranges='2-4'):return dict(path=p,ranges=ranges,review_state='synthetic-only')
    def groups(self,n=146):return '\n'.join(f'| G-{i:02d} | exact row |' for i in range(1,n+1))+'\n'
    def erratum(self):return dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False)
    def metadata(self):return dict(phase='7B12-partial-static-audit',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,spreadsheet_or_formula_interpreter_executed=False,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=22,static_lexical_contract_check_count=22,
        default_aggregate_gate_not_assumed_resolved=True,supplied_sql_not_certified_deployed=True,
        stock_child_schema_not_assumed_resolved=True,manual_metric_models_not_financial_acceptance=True,
        retained_additive_B10_arithmetic_erratum=self.erratum())

    def test_01_exact_frozen287_rows_and_logical_index_paths(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(len(f.rows('findings.csv')),287)
            for n in b12.SHARED_DOCS:self.assertEqual(f.read(f.AUDIT/n),'FROZEN:'+n)
    def test_02_direct_bytes_overlay_is_local_not_pathlib_patch(self):
        f=self.fake();method=Path.read_bytes
        with self.context(f):
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw());self.assertIs(Path.read_bytes,method)
            self.assertEqual(str(f.AUDIT/'findings.csv'),'/synthetic/audit/findings.csv')
    def test_03_normal_exit_restores_all_objects(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.context(f):pass
        for a,b in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(a,b)
    def test_04_exception_exit_restores_all_objects(self):
        f=self.fake();before=f.AUDIT,f.read,f.rows
        with self.assertRaisesRegex(RuntimeError,'synthetic'):
            with self.context(f):raise RuntimeError('synthetic')
        for a,b in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(a,b)
    def test_05_nested_b10_restores_b11_rows_text_bytes(self):
        f=self.fake()
        with self.context(f):
            with historical_b10_inputs(f,self.old(285),{n:'B10:'+n for n in b12.SHARED_DOCS},self.raw(self.old(285))):
                self.assertEqual(len(f.rows('findings.csv')),285);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B10:PLAN.md')
                self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(self.old(285)))
            self.assertEqual(len(f.rows('findings.csv')),287);self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
    def test_06_nested_exception_restores_outer_context(self):
        f=self.fake()
        with self.context(f):
            with self.assertRaisesRegex(RuntimeError,'synthetic'):
                with historical_b10_inputs(f,self.old(285),self.texts(),self.raw(self.old(285))):raise RuntimeError('synthetic')
            self.assertEqual(len(f.rows('findings.csv')),287);self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())
    def test_07_wrong_count_and_duplicate_ids_rejected(self):
        duplicate=self.old();duplicate[-1]['id']=duplicate[0]['id']
        for bad in (self.old(285),self.old(286),self.old(288),duplicate):
            with self.assertRaises(ValueError):
                with b12.historical_b11_inputs(self.fake(),bad,self.texts(),self.raw(bad)):pass
    def test_08_three_exact_string_index_texts_required(self):
        for bad in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            f=self.fake();before=f.AUDIT,f.read,f.rows
            with self.assertRaises(ValueError):
                with b12.historical_b11_inputs(f,self.old(),bad,self.raw()):pass
            for a,b in zip((f.AUDIT,f.read,f.rows),before):self.assertIs(a,b)
    def test_09_raw_bytes_rows_CRLF_noBOM_must_agree(self):
        for bad in (None,'not bytes',b'\xef\xbb\xbf'+self.raw(),self.raw().replace(b'\r\n',b'\n'),self.raw().replace(b'synthetic',b'changed',1),self.raw()+b'\r\n',b'\xff'):
            with self.assertRaises(ValueError):
                with b12.historical_b11_inputs(self.fake(),self.old(),self.texts(),bad):pass
    def test_10_rows_are_fresh_copies_other_rows_delegate(self):
        f=self.fake();old=self.old()
        with b12.historical_b11_inputs(f,old,self.texts(),self.raw(old)):
            f.rows('findings.csv')[0]['title']='changed';self.assertEqual(f.rows('findings.csv')[0]['title'],'synthetic')
            self.assertEqual(old[0]['title'],'synthetic');self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')])
    def test_11_non_target_paths_delegate_success_and_missing(self):
        f=self.fake()
        with self.context(f):
            self.assertEqual(f.read(Path('/elsewhere/README.md')),'LIVE:/elsewhere/README.md')
            with self.assertRaises(FileNotFoundError):type(f.AUDIT)('/synthetic/elsewhere/findings.csv').read_bytes()
            with self.assertRaises(FileNotFoundError):(f.AUDIT/'other.csv').read_bytes()
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())
    def test_12_union_complement_are_bookkeeping_only(self):
        r=b12.build_current_ledger([self.item()],[('7B11',[self.scope(ranges='2-3')]),('7B12',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(r['declared_range_union_not_reading_certification'],'2-3;7-8');self.assertEqual(r['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertEqual(r['phase7B11_ranges'],'2-3');self.assertEqual(r['phase7B12_ranges'],'7-8');self.assertIn('not-closed',r['continuation_bucket']);self.assertEqual(r['runtime_status'],'not-executed')
    def test_13_full_lines_never_close_feature(self):
        p='frmRptSynthetic.cs';r=b12.build_candidate_disposition([self.item(p)],[('7B12',[self.scope(p,'1-10')])])[0]
        self.assertEqual(r['phase7B12_ranges'],'1-10');self.assertEqual(r['coverage_state'],'selected-slices-not-whole-feature-closed');self.assertIn('required',r['disposition'])
    def test_14_binary_and_fingerprint_do_not_become_reports(self):
        r=b12.build_current_ledger([self.item('x.dll','',kind='generated-artifact')],[],v.spans)[0]
        self.assertEqual(r['line_range_state'],'binary-metadata-not-executed');self.assertIn('not-authorized',r['continuation_bucket'])
        r=b12.build_candidate_disposition([self.item('FingerPrintDevice.cs')],[])[0];self.assertIn('lexical-false-positive',r['disposition'])
    def test_15_each_body_requires_own_full_xaml(self):
        for name in b12.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';inv=[self.item(p),self.item(p+'.cs')]
            r=b12.build_screen_disposition(inv,[('7B12',[self.scope(p,'1-10'),self.scope(p+'.cs','1-10')])])[0]
            self.assertEqual(r['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
            for selected in ([self.scope(p+'.cs','1-10')],[self.scope(p,'1-9'),self.scope(p+'.cs','1-10')]):
                r=b12.build_screen_disposition(inv,[('7B12',selected)])[0];self.assertNotEqual(r['coverage_level'],'bounded-local-body-and-xaml-not-whole-feature-certified')
    def test_16_parent_review_does_not_promote_child(self):
        p='SmartAuditERP/Form_WPF/frmRptParent.xaml';c='SmartAuditERP/Form_WPF/frmRptChild.xaml'
        by={r['screen']:r for r in b12.build_screen_disposition([self.item(p),self.item(p+'.cs'),self.item(c),self.item(c+'.cs')],[('7B12',[self.scope(p+'.cs','1-10')])])}
        self.assertEqual(by['frmRptChild']['coverage_level'],'inventory-only-not-implementation-reviewed')
    def test_17_known_names_with_no_ranges_not_promoted(self):
        for name in b12.REVIEWED_BODIES:
            p='SmartAuditERP/Form_WPF/'+name+'.xaml';r=b12.build_screen_disposition([self.item(p),self.item(p+'.cs')],[])[0]
            self.assertEqual(r['phase7B12_body_ranges'],'none');self.assertEqual(r['coverage_level'],'inventory-only-not-implementation-reviewed')
    def test_18_all_cores_and_every_followup_immutable(self):
        for field in ('title','severity','certainty','type','status','next_phase'):
            old,now,m=self.transition();now[1][field]='changed';self.assertTrue(any('.'+field in e for e in b12.registry_transition_errors(old,now,m)))
    def test_19_exact_declared_append_tails_only(self):
        old,now,m=self.transition();self.assertEqual(b12.registry_transition_errors(old,now,m),[])
        for bad in ([],m*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):self.assertTrue(b12.registry_transition_errors(old,now,bad))
        now[0]['evidence']+=';c.cs:5-6';self.assertTrue(b12.registry_transition_errors(old,now,m));now[0]['evidence']='b.cs:3-4';self.assertTrue(b12.registry_transition_errors(old,now,m))
    def test_20_exact146_group_prefix_allows_new_rows(self):
        prior=self.groups();self.assertEqual(b12.group_row_errors(prior,prior+'\nAdditive prose\n| G-147 | new |\n'),[])
    def test_21_old_group_whitespace_order_count_rejected(self):
        prior=self.groups()
        for bad in (prior.replace('exact row','exact  row',1),prior.replace('| G-01 |','| G-02 |',1),self.groups(145)):self.assertTrue(b12.group_row_errors(prior,bad))
        self.assertTrue(b12.group_row_errors(self.groups(147),prior))
    def test_22_reverse_links_are_exact(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')];tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b12.bidirectional_errors(pool,tests,'feature_ids'));pool[0]['acceptance_ids']='T1;T2';self.assertEqual(b12.bidirectional_errors(pool,tests,'feature_ids'),[])
    def test_23_feature_vocabulary_and_inventory_sentinel(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b12.feature_level_errors([row]),[])
        for bad in (row|{'coverage_level':'source-reviewed'},row|{'evidence':'a.cs:1-2'},row|{'implementation_status':'complete'}):self.assertTrue(b12.feature_level_errors([bad]))
        row|=dict(implementation_status='reviewed-contract-unresolved-not-global-absence',coverage_level='bounded-contract-not-whole-feature',evidence='a.cs:1-2');self.assertEqual(b12.feature_level_errors([row]),[])
    def test_24_false_only_execution_flags_integer_zero_counts(self):
        self.assertEqual(b12.witness_metadata_errors(self.metadata()),[])
        for k in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for x in (True,None,0):self.assertTrue(b12.witness_metadata_errors(self.metadata()|{k:x}))
        for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for x in (1,False,None,'0'):self.assertTrue(b12.witness_metadata_errors(self.metadata()|{k:x}))
    def test_25_four_causal_boundaries_are_true_only(self):
        for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed','stock_child_schema_not_assumed_resolved','manual_metric_models_not_financial_acceptance'):
            for x in (False,None,1,'true'):self.assertTrue(b12.witness_metadata_errors(self.metadata()|{k:x}))
    def test_26_inventory_gate_has_no_fabricated_source(self):
        errors=[];calls=[];f=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append(a))
        b12.validate_source(f,dict(id='RC7B12-06',evidence='none-inventory-only'),{});self.assertEqual(errors,[]);self.assertEqual(calls,[])
        b12.validate_source(f,dict(id='RC7B12-06',evidence='x.cs:1-2'),{});self.assertTrue(errors)
    def test_27_bookkeeping_builders_do_not_mutate_inputs(self):
        inv=[self.item('frmRptSynthetic.cs')];labelled=[('7B12',[self.scope('frmRptSynthetic.cs','1-10')])];before=copy.deepcopy((inv,labelled))
        b12.build_current_ledger(inv,labelled,v.spans);b12.build_candidate_disposition(inv,labelled);b12.build_screen_disposition(inv,labelled);self.assertEqual((inv,labelled),before)
    def test_28_counts_and_prior_roots_not_renumbered(self):
        counts={n:c for n,_,c in b12.TABLE_SPECS};self.assertEqual(counts['acceptance-tests'],27);self.assertEqual(counts['feature-implementation-matrix'],25);self.assertEqual(len(b12.EXTENDED_FINDINGS),16)
        self.assertTrue({'P3-019','P3-020','P4-008','P7-065','P7-097','P7-098'}<=b12.EXTENDED_FINDINGS)
        self.assertTrue({'P7-116','P7-117','P3-022','P7-054','P7-093','P7-095','P7-111','P7-113','P7-114','P7-115'}.isdisjoint(b12.EXTENDED_FINDINGS))
    def test_29_retained_erratum_exact_typed_and_no_rewrite(self):
        self.assertEqual(b12.arithmetic_erratum_errors(self.erratum()),[])
        for bad in (None,{},self.erratum()|{'local_cost':20},self.erratum()|{'reference_cost':10},self.erratum()|{'local_cost':10.0},self.erratum()|{'archive_rewritten':True},self.erratum()|{'archive_rewritten':0}):self.assertTrue(b12.arithmetic_erratum_errors(bad))
    def test_30_phase_and_22_witness_counts_are_typed(self):
        for patch in ({'phase':'ERP-certified'},{'illustration_count':21},{'illustration_count':22.0},{'static_lexical_contract_check_count':True},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'local_cost':20}}):self.assertTrue(b12.witness_metadata_errors(self.metadata()|patch))
    def test_31_proposed_output_identity_distinguishes_explicit_conversion(self):
        good=dict(chosen_path='report.xlsx',effective_path='report.xlsx',displayed_path='report.xlsx',opened_path='report.xlsx',format='XLSX')
        self.assertEqual(b12.output_identity_errors(good),[])
        mismatch=good|{'effective_path':'report.csv'};self.assertTrue(b12.output_identity_errors(mismatch))
        conversion=good|dict(effective_path='report.csv',displayed_path='report.csv',opened_path='report.csv',format='CSV')
        self.assertTrue(b12.output_identity_errors(conversion));self.assertEqual(b12.output_identity_errors(conversion|{'explicit_conversion_confirmed':True}),[])
        for bad in (None,{},good|{'opened_path':''},conversion|{'explicit_conversion_confirmed':1}):self.assertTrue(b12.output_identity_errors(bad))
    def test_32_proposed_stock_shape_distinguishes_zero_unset_and_failed(self):
        zero=dict(approved=True,has_value=True,value=0,health='valid');self.assertEqual(b12.stock_selection_errors(zero),[])
        unset=dict(approved=False,has_value=False,value=None,health='not-requested');self.assertEqual(b12.stock_selection_errors(unset),[])
        for bad in (None,{},zero|{'approved':1},zero|{'has_value':0},zero|{'value':True},zero|{'value':None},zero|{'health':'failed'},zero|{'has_value':False},unset|{'value':0}):self.assertTrue(b12.stock_selection_errors(bad))


if __name__=='__main__':unittest.main()
