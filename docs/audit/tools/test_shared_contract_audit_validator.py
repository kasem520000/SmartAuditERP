#!/usr/bin/env python3
"""28 new synthetic DOCUMENTATION-checker cases, NOT ERP acceptance.

Protects all382 prior cases unchanged. Artificial rows/strings/ranges plus
exact-path IN-MEMORY adapters only. No application import/build/runtime,
SQL/WPF/REPX/Office/device/interpreter/real data/remediation/measurement.
"""
from __future__ import annotations
import copy
import csv
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_audit as v
import validate_shared_contract_part as b16
from validate_accrual_tax_part import historical_b14_inputs
from validate_inventory_activity_part import historical_b13_inputs


class SharedContractAuditTests(unittest.TestCase):
    def fake(self):
        return SimpleNamespace(AUDIT=Path('/synthetic/audit'), read=lambda p: 'LIVE:'+str(p),
                               rows=lambda p: [dict(id='LIVE:'+p)])

    def old(self, n=298):
        return [dict(id=f'P-X{i:03d}', title='synthetic', severity='High', certainty='confirmed',
                     type='synthetic-only', status='open-not-remediated', next_phase='7;8', evidence='a.cs:1-2') for i in range(n)]

    def raw(self, data=None):
        data = self.old() if data is None else data
        out = io.StringIO(newline='')
        writer = csv.DictWriter(out, fieldnames=list(data[0]), lineterminator='\r\n')
        writer.writeheader()
        writer.writerows(data)
        return out.getvalue().encode()

    def texts(self):
        return {n:'FROZEN:'+n for n in b16.SHARED_DOCS}

    def context(self, f):
        return b16.historical_b15_inputs(f, self.old(), self.texts(), self.raw())

    def groups(self, n=170):
        return '\n'.join(f'| G-{i:02d} | exact row |' for i in range(1,n+1))+'\n'

    def item(self, path='a.cs', lines='10', kind='source'):
        return dict(path=path, lines=lines, kind=kind)

    def scope(self, path='a.cs', ranges='2-4'):
        return dict(path=path, ranges=ranges, review_state='synthetic-only')

    def plan(self):
        statuses = ['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open']+['planned-not-started']*7
        return [dict(id=f'RW-{i}', part_family='7B' if i<4 else '7C', title='synthetic planning group',
                     candidate_scope_not_certified='bounded scope', expected_deliverable='assessment',
                     static_exit_criterion='reasoned disposition', dependencies_and_uncertainty='external input unresolved',
                     status=statuses[i], runtime_status='not-executed', counts_are_sessions_or_completion_percent='false') for i in range(10)]

    def depth(self):
        return [dict(prior_full_local_csharp_declared='true' if i==2 else 'false',
                     newly_full_local_csharp_in_declared_scopes='false' if i==2 else 'true',
                     present_in_frozen52_screen_candidates='false', b16_full_local_body_and_xaml='true') for i in range(3)]

    def acceptance(self):
        ext = [dict(finding_ids=f'OLD-{i:02d}') for i in range(17)]
        tests = [dict(plan_kind='finding-specific', finding_ids='P7-127', feature_ids='FE7B16-01', invariant_ids='INV7B16-01', status='not-executed') for _ in range(2)]
        tests += [dict(plan_kind='historical-root-regression', finding_ids=e['finding_ids'], status='not-executed') for e in ext]
        for kind, count in [('cross-cutting-contract',4), ('documentary-scope-or-authorization-gate',2)]:
            tests += [dict(plan_kind=kind, finding_ids='HANDOFF', status='not-executed') for _ in range(count)]
        return tests, ['P7-127'], ext

    def adjudication(self):
        return [dict(current_root_ids='P7-127' if i==0 else 'OLD', nearest_prior_root_ids='NEAREST',
                     decision='new-local-root' if i==0 else 'extended-existing-root', reason='source-bound distinction',
                     comparison_depth='all298-titles-classifications-evidence-paths-plus-selected-nearest-chains-not-all-historical-chains',
                     runtime_status='not-executed') for i in range(9)]

    def residual(self):
        ids = [f'H7B{part}-{n:02d};Q7B{part}-{n:02d}' for part in (14,15) for n in range(1,7)]+['WIDER','BARCODE']
        return [dict(id=f'RS-{i}', upstream_contract_ids=up, upstream_artifacts='prior.md', current_handoff_ids='H7B16-01',
                     disposition='bounded-source-reviewed-external-contract-remains-open' if i<12 else 'explicit-further-split-no-new-source-claim',
                     local_result='bounded observation', owner_role='owner', required_input_and_impact='redacted policy/schema',
                     next_step='explicit proposed static split', runtime_status='not-executed') for i,up in enumerate(ids)]

    def erratum(self):
        return dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False)

    def metadata(self):
        return dict(phase='7B16-partial-static-audit', application_code_imported_or_executed=False,
                    application_remediation_performed=False, real_business_or_secret_data_used=False,
                    spreadsheet_or_formula_interpreter_executed=False, erp_runtime_tests_executed=0,
                    sql_or_external_service_tests_executed=0, illustration_count=20, static_lexical_contract_check_count=20,
                    child_and_actual_VAT_caller_full_local_not_whole_features=True, picker_csharp_already_full_B1=True,
                    frozen52_denominator_not_silently_expanded=True, B_R1_R2_R3_residual_contracts_not_closed=True,
                    supplied_sql_not_certified_deployed=True, manual_metric_models_not_financial_acceptance=True,
                    retained_additive_B10_arithmetic_erratum=self.erratum())

    def test_01_OWN298_and_exact_three_indexes(self):
        f = self.fake()
        with self.context(f):
            self.assertEqual(len(f.rows('findings.csv')),298)
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())

    def test_02_exact_logical_path_not_global_pathlib_patch(self):
        f, method = self.fake(), Path.read_bytes
        with self.context(f):
            self.assertIs(Path.read_bytes,method)
            self.assertEqual((f.AUDIT/'unused'/'..'/'findings.csv').read_bytes(),self.raw())
            self.assertEqual(f.rows('unrelated/findings.csv'),[dict(id='LIVE:unrelated/findings.csv')])
            with self.assertRaises(FileNotFoundError):
                type(f.AUDIT)('/synthetic/unrelated/findings.csv').read_bytes()

    def test_03_normal_exception_and_bad_input_restore_identities(self):
        f = self.fake()
        original = f.AUDIT,f.read,f.rows
        with self.context(f):
            pass
        self.assertTrue(all(a is b for a,b in zip((f.AUDIT,f.read,f.rows),original)))
        with self.assertRaises(RuntimeError):
            with self.context(f):
                raise RuntimeError('synthetic')
        self.assertTrue(all(a is b for a,b in zip((f.AUDIT,f.read,f.rows),original)))
        with self.assertRaises(ValueError):
            with b16.historical_b15_inputs(f,self.old(),{},self.raw()):
                pass
        self.assertTrue(all(a is b for a,b in zip((f.AUDIT,f.read,f.rows),original)))

    def test_04_nested_B14_has_OWN294_then_returns298(self):
        f, inner = self.fake(), self.old(294)
        with self.context(f):
            with historical_b14_inputs(f,inner,{n:'B14:'+n for n in b16.SHARED_DOCS},self.raw(inner)):
                self.assertEqual(len(f.rows('findings.csv')),294)
                self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(inner))
                self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'B14:PLAN.md')
            self.assertEqual(len(f.rows('findings.csv')),298)
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())

    def test_05_three_nested_versions_and_inner_exception_do_not_leak(self):
        f, inner, oldest = self.fake(), self.old(294), self.old(291)
        with self.context(f):
            with historical_b14_inputs(f,inner,self.texts(),self.raw(inner)):
                with self.assertRaises(RuntimeError):
                    with historical_b13_inputs(f,oldest,self.texts(),self.raw(oldest)):
                        self.assertEqual(len(f.rows('findings.csv')),291)
                        self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(oldest))
                        raise RuntimeError('synthetic')
                self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw(inner))
            self.assertEqual((f.AUDIT/'findings.csv').read_bytes(),self.raw())

    def test_06_count_duplicates_and_rawCRLF_rows_agreement(self):
        duplicate = self.old()
        duplicate[-1]['id'] = duplicate[0]['id']
        for bad in (self.old(294),self.old(297),self.old(299),duplicate):
            with self.assertRaises(ValueError):
                with b16.historical_b15_inputs(self.fake(),bad,self.texts(),self.raw(bad)):
                    pass
        for bad in (None,'not bytes',b'\xef\xbb\xbf'+self.raw(),self.raw().replace(b'\r\n',b'\n'),self.raw()+b'\r\n',self.raw()+b'\r',self.raw().replace(b'synthetic',b'changed',1),b'\xff'):
            with self.assertRaises(ValueError):
                with b16.historical_b15_inputs(self.fake(),self.old(),self.texts(),bad):
                    pass

    def test_07_exact_index_keys_types_and_fresh_copies(self):
        for texts in ({},self.texts()|{'extra.md':'x'},self.texts()|{'PLAN.md':None}):
            with self.assertRaises(ValueError):
                with b16.historical_b15_inputs(self.fake(),self.old(),texts,self.raw()):
                    pass
        f, old, texts = self.fake(),self.old(),self.texts()
        with b16.historical_b15_inputs(f,old,texts,self.raw(old)):
            texts['PLAN.md']='later-change'
            self.assertEqual(f.read(f.AUDIT/'PLAN.md'),'FROZEN:PLAN.md')
            first, second = f.rows('findings.csv'),f.rows('findings.csv')
            first[0]['title']='changed'
            self.assertEqual(second[0]['title'],'synthetic')
            self.assertEqual(old[0]['title'],'synthetic')

    def test_08_unrelated_reads_delegate_without_disk_overlays(self):
        f = self.fake()
        with self.context(f):
            self.assertEqual(f.rows('other.csv'),[dict(id='LIVE:other.csv')])
            self.assertEqual(f.read(Path('/elsewhere/PLAN.md')),'LIVE:/elsewhere/PLAN.md')
            self.assertEqual(type(f.AUDIT)(__file__).read_bytes(),Path(__file__).read_bytes())

    def test_09_cores_ALLfollowups_and_exact_declared_tails(self):
        old, now = self.old(2),self.old(2)
        now[0]['evidence']+=';b.cs:3-4'
        manifest=[dict(finding_ids=old[0]['id'],evidence='b.cs:3-4')]
        self.assertEqual(b16.registry_transition_errors(old,now,manifest),[])
        for k in ('title','type','certainty','severity','status','next_phase'):
            bad=copy.deepcopy(now)
            bad[1][k]='changed'
            self.assertTrue(b16.registry_transition_errors(old,bad,manifest))
        for wrong in ([],manifest*2,[dict(finding_ids='UNKNOWN',evidence='b.cs:3-4')]):
            self.assertTrue(b16.registry_transition_errors(old,now,wrong))
        for evidence in ('b.cs:3-4','a.cs:1-2;b.cs:3-4;c.cs:5-6'):
            bad=copy.deepcopy(now)
            bad[0]['evidence']=evidence
            self.assertTrue(b16.registry_transition_errors(old,bad,manifest))

    def test_10_exactG170_order_whitespace_and_additive_suffix(self):
        old=self.groups()
        self.assertEqual(b16.group_row_errors(old,old+'| G-171 | new |\n'),[])
        for bad in (old.replace('exact row','exact  row',1),old.replace('| G-01 |','| G-02 |',1),self.groups(169)):
            self.assertTrue(b16.group_row_errors(old,bad))
        self.assertTrue(b16.group_row_errors(self.groups(171),old))

    def test_11_bidirectional_plan_links_not_one_way(self):
        pool=[dict(id='FE-X',acceptance_ids='T1')]
        tests=[dict(id='T1',feature_ids='FE-X'),dict(id='T2',feature_ids='FE-X')]
        self.assertTrue(b16.bidirectional_errors(pool,tests,'feature_ids'))
        pool[0]['acceptance_ids']='T1;T2'
        self.assertEqual(b16.bidirectional_errors(pool,tests,'feature_ids'),[])
        fe=[dict(id='FE7B16-01',title='synthetic',finding_ids='OLD',evidence='a.cs:1-2',acceptance_ids='T1')]
        iv=[fe[0]|{'id':'INV7B16-01'}]
        ex=[dict(id='EX7B16-01',title='synthetic',finding_ids='OLD',evidence='a.cs:1-2')]
        rc=[dict(id='RC7B16-01',feature_ids='FE7B16-01',finding_ids='OLD',evidence='a.cs:1-2')]
        self.assertEqual(b16.contract_link_errors(fe,iv,ex,rc),[])
        for pool_index,patch in [(1,{'evidence':'unrelated.cs:5-6'}),(2,{'evidence':'unrelated.cs:5-6'}),
                                 (3,{'finding_ids':'WRONG'}),(3,{'feature_ids':'UNKNOWN'})]:
            data=copy.deepcopy([fe,iv,ex,rc]);data[pool_index][0]|=patch
            self.assertTrue(b16.contract_link_errors(*data))

    def test_12_feature_vocabulary_inventory_only_no_false_closure(self):
        row=dict(id='FE-X',implementation_status='deferred-not-implementation-reviewed',coverage_level='inventory-only-not-implementation-reviewed',evidence='none-inventory-only')
        self.assertEqual(b16.feature_level_errors([row]),[])
        for patch in ({'coverage_level':'source-reviewed'},{'evidence':'a.cs:1-2'},{'implementation_status':'complete'}):
            self.assertTrue(b16.feature_level_errors([row|patch]))

    def test_13_ledger_is_range_bookkeeping_not_ERP_coverage(self):
        row=b16.build_current_ledger([self.item()],[('7B15',[self.scope(ranges='2-3')]),('7B16',[self.scope(ranges='7-8')])],v.spans)[0]
        self.assertEqual(row['phase7B16_ranges'],'7-8')
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-3;7-8')
        self.assertEqual(row['unselected_text_ranges'],'1-1;4-6;9-10')
        self.assertIn('not-closed',row['continuation_bucket'])
        self.assertEqual(row['runtime_status'],'not-executed')

    def test_14_builders_preserve_inputs_binary_and_lexical_false_positives(self):
        inv=[self.item('FingerPrintDevice.cs'),self.item('x.dll','',kind='generated-artifact')]
        scopes=[('7B16',[self.scope('FingerPrintDevice.cs','1-10')])]
        before=copy.deepcopy((inv,scopes))
        ledger=b16.build_current_ledger(inv,scopes,v.spans)
        candidates=b16.build_candidate_disposition(inv,scopes)
        b16.build_screen_disposition(inv,scopes)
        self.assertEqual((inv,scopes),before)
        self.assertEqual(ledger[1]['line_range_state'],'binary-metadata-not-executed')
        self.assertIn('not-authorized',ledger[1]['continuation_bucket'])
        self.assertIn('lexical-false-positive',candidates[0]['disposition'])

    def test_15_supplemental_depth_does_not_silently_expand_frozen52(self):
        inv, current = [],[]
        for name in b16.REVIEWED_BODIES:
            x='SmartAuditERP/Form_WPF/'+name+'.xaml'
            inv += [self.item(x),self.item(x+'.cs')]
            current += [self.scope(x,'1-10'),self.scope(x+'.cs','1-10')]
        prior=[('7B1',[self.scope('SmartAuditERP/Form_WPF/frmPrinter.xaml.cs','1-10')])]
        depth=b16.depth_clarification(inv,prior+[('7B16',current)],v.spans)
        self.assertEqual(b16.remaining_work_errors(self.plan(),depth),[])
        self.assertEqual(depth[-1]['prior_full_body_scope_ids'],'7B1')
        without_own=[r for r in current if r['path']!='SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml']
        missing=b16.depth_clarification(inv,prior+[('7B16',without_own)],v.spans)
        self.assertEqual(missing[0]['b16_full_local_body_and_xaml'],'false')
        self.assertTrue(b16.remaining_work_errors(self.plan(),missing))

    def test_16_three_local_groups_residuals_R4_C_unstarted_not_sessions(self):
        self.assertEqual(b16.remaining_work_errors(self.plan(),self.depth()),[])
        for i,patch in [(0,{'status':'complete'}),(2,{'status':'planned-not-started'}),(3,{'status':'complete'}),(4,{'status':'in-progress'}),(0,{'part_family':'7C'}),(1,{'runtime_status':'passed'}),(2,{'counts_are_sessions_or_completion_percent':'true'})]:
            data=self.plan();data[i]|=patch
            self.assertTrue(b16.remaining_work_errors(data,self.depth()))

    def test_17_work_fields_and_depth_boundary_mutations(self):
        for field in ('id','title','candidate_scope_not_certified','expected_deliverable','static_exit_criterion','dependencies_and_uncertainty'):
            for value in ('',' ',None):
                data=self.plan();data[1][field]=value
                self.assertTrue(b16.remaining_work_errors(data,self.depth()))
        for patch in ({'present_in_frozen52_screen_candidates':'true'},{'newly_full_local_csharp_in_declared_scopes':'true'},{'b16_full_local_body_and_xaml':'false'}):
            data=self.depth();data[-1]|=patch
            self.assertTrue(b16.remaining_work_errors(self.plan(),data))

    def test_18_exact25_plan_kinds_order_and_not_executed(self):
        tests,ids,ext=self.acceptance()
        self.assertEqual(b16.plan_structure_errors(tests,ids,ext),[])
        for bad in (tests[:-1],[tests[2]]+tests[:2]+tests[3:],[r|{'status':'passed'} if i==24 else r for i,r in enumerate(tests)]):
            self.assertTrue(b16.plan_structure_errors(bad,ids,ext))
        self.assertTrue(b16.plan_structure_errors(tests,ids,list(reversed(ext))))

    def test_19_two_direct_plans_one_root_not_one_per_caller(self):
        tests,ids,ext=self.acceptance()
        for patch in ({'finding_ids':'P7-128'},{'feature_ids':'FE7B16-02'},{'invariant_ids':'INV7B16-02'}):
            data=copy.deepcopy(tests);data[0]|=patch
            self.assertTrue(b16.plan_structure_errors(data,ids,ext))
        self.assertTrue(b16.plan_structure_errors(tests,ids+['P7-128'],ext))

    def test_20_one_adjudicated_root_and_limited_dedup_depth(self):
        data=self.adjudication()
        self.assertEqual(b16.adjudication_errors(data),[])
        for patch in ({'decision':'repeat'},{'current_root_ids':'P7-999'},{'comparison_depth':'all-historical-chains-certified'},{'nearest_prior_root_ids':''},{'reason':None},{'reason':' '},{'runtime_status':'passed'}):
            bad=copy.deepcopy(data);bad[0]|=patch
            self.assertTrue(b16.adjudication_errors(bad))
        bad=copy.deepcopy(data);bad[1]['decision']='new-local-root'
        self.assertTrue(b16.adjudication_errors(bad))

    def test_21_all12_upstream_HQ_residuals_plus2_explicit_splits(self):
        data=self.residual()
        self.assertEqual(b16.residual_errors(data),[])
        for bad in (data[:-1],list(reversed(data)),[r|{'upstream_contract_ids':'WRONG'} if i==1 else r for i,r in enumerate(data)]):
            self.assertTrue(b16.residual_errors(bad))
        bad=copy.deepcopy(data);bad[12]['disposition']='bounded-source-reviewed-external-contract-remains-open'
        self.assertTrue(b16.residual_errors(bad))

    def test_22_residual_owner_impact_nextstep_and_no_approval_claim(self):
        for field in ('upstream_artifacts','current_handoff_ids','local_result','owner_role','required_input_and_impact','next_step'):
            for value in ('',' ',None):
                data=self.residual();data[1][field]=value
                self.assertTrue(b16.residual_errors(data))
        for patch in ({'disposition':'complete'},{'runtime_status':'passed'}):
            data=self.residual();data[0]|=patch
            self.assertTrue(b16.residual_errors(data))

    def test_23_strict_false_integer_zero_and_true_metadata_boundaries(self):
        self.assertEqual(b16.witness_metadata_errors(self.metadata()),[])
        for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
            for value in (True,None,0):
                self.assertTrue(b16.witness_metadata_errors(self.metadata()|{key:value}))
        for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
            for value in (1,False,None,'0'):
                self.assertTrue(b16.witness_metadata_errors(self.metadata()|{key:value}))
        for key in ('child_and_actual_VAT_caller_full_local_not_whole_features','picker_csharp_already_full_B1','frozen52_denominator_not_silently_expanded','B_R1_R2_R3_residual_contracts_not_closed','supplied_sql_not_certified_deployed','manual_metric_models_not_financial_acceptance'):
            for value in (False,None,1,'true'):
                self.assertTrue(b16.witness_metadata_errors(self.metadata()|{key:value}))

    def test_24_witness_counts_phase_and_additive_B10_erratum(self):
        for patch in ({'phase':'ERP-certified'},{'illustration_count':19},{'illustration_count':20.0},{'static_lexical_contract_check_count':True},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'local_cost':20}},{'retained_additive_B10_arithmetic_erratum':self.erratum()|{'archive_rewritten':0}}):
            self.assertTrue(b16.witness_metadata_errors(self.metadata()|patch))

    def test_25_declared_sentinels_and_no_fabricated_source_evidence(self):
        errors,calls=[],[]
        fake=SimpleNamespace(check=lambda ok,msg: errors.append(msg) if not ok else None,
                             evidence=lambda *a:calls.append(a),scoped_evidence=lambda *a,**k:calls.append((a,k)))
        for name in ('ALG7B16-20','RS7B16-06','RS7B16-12','RS7B16-13','RS7B16-14'):
            b16.validate_source(fake,dict(id=name,evidence='none-inventory-only'),{})
        self.assertEqual((errors,calls),([],[]))
        b16.validate_source(fake,dict(id='UNKNOWN',evidence='none-inventory-only'),{})
        b16.validate_source(fake,dict(id='RS7B16-13',evidence='a.cs:1-2'),{'a.cs':[(1,2)]})
        self.assertEqual(len(errors),2)

    def test_26_real_source_evidence_dispatch_and_scope_boundary(self):
        errors,calls=[],[]
        fake=SimpleNamespace(check=lambda ok,msg:errors.append(msg) if not ok else None,
                             evidence=lambda *a:calls.append(('evidence',a)),
                             scoped_evidence=lambda *a,**k:calls.append(('scoped',a,k)))
        scope={'a.cs':[(1,2)]}
        b16.validate_source(fake,dict(id='FE7B16-01',evidence='a.cs:1-2'),scope)
        self.assertEqual(calls[0],('evidence',('a.cs:1-2','FE7B16-01')))
        self.assertEqual(calls[1][1][1],scope)
        self.assertEqual(calls[1][2],dict(phase=7))
        self.assertEqual(errors,[])

    def test_27_exact_table_counts_extensions_and_potential_not_promoted(self):
        counts={n:c for n,_,c in b16.TABLE_SPECS}
        self.assertEqual((counts['acceptance-tests'],counts['feature-implementation-matrix'],counts['root-adjudication'],counts['residual-disposition']),(25,24,9,14))
        self.assertEqual(len(b16.EXTENDED_FINDINGS),17)
        self.assertTrue({'P7-050','P7-095','P7-061','P7-088','P7-099','P7-112','P7-125','P1-013','P7-032'}<=b16.EXTENDED_FINDINGS)
        self.assertTrue({'P7-127','P7-044','P7-051','P7-126','P7-049','P7-108','P4-007'}.isdisjoint(b16.EXTENDED_FINDINGS))

    def test_28_historical_programmatic_B15_default_and_explicit_current_B16_CLI(self):
        # Protected B15 case32 inspects this same public default; do NOT edit it.
        self.assertEqual(v.main.__defaults__,('B15',))
        text=Path(v.__file__).read_text()
        self.assertIn('"B15", "B16"), default="B16"',text)
        self.assertIn('sys.exit(main(args.through_phase, args.phase7_part))',text)
        self.assertEqual(b16.ENTRY_CHECKOUT,'16f3fd42f24183db5906bd06517b8dc10a7b9b36')
        self.assertEqual(len(b16.SNAPSHOT_SHA),64)


if __name__ == '__main__':
    unittest.main()
