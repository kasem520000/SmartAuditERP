#!/usr/bin/env python3
"""Synthetic tests of NEW AUDIT-CHECKER helpers only, NOT SmartAuditERP tests.

No application imports, subprocesses, file writes, SQL, network, COM, devices,
spreadsheet evaluation or build. Historical ten tests remain unmodified.
"""
from __future__ import annotations
import copy
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate_audit as validator
import validate_report_part as reports


class ReportAuditCheckerTests(unittest.TestCase):
    def setUp(self):
        validator.ERRORS.clear()

    def tearDown(self):
        validator.ERRORS.clear()

    def item(self,path='a.cs',lines='10',kind='csharp-source'):
        return {'path':path,'lines':lines,'kind':kind}

    def scope(self,path='a.cs',ranges='2-4',state='synthetic-slices-only'):
        return {'path':path,'ranges':ranges,'review_state':state}

    def test_merge_overlap_adjacent_and_duplicates(self):
        self.assertEqual(reports.merge_ranges([(8,9),(2,4),(3,5),(6,6),(2,4)]),[(2,6),(8,9)])

    def test_merge_rejects_reverse_zero_and_nonnumeric(self):
        for value in [[(4,2)],[(0,2)],[('1',2)]]:
            with self.assertRaises(ValueError): reports.merge_ranges(value)

    def test_remaining_ranges_are_closed_complement(self):
        self.assertEqual(reports.remaining_ranges(10,[(2,4),(7,9)]),[(1,1),(5,6),(10,10)])
        self.assertEqual(reports.remaining_ranges(10,[(1,10)]),[])

    def test_remaining_rejects_out_of_bounds_or_negative(self):
        with self.assertRaises(ValueError): reports.remaining_ranges(5,[(1,6)])
        with self.assertRaises(ValueError): reports.remaining_ranges(-1,[])

    def test_binary_metadata_is_not_line_coverage(self):
        row=reports.build_ledger([self.item('b.dll','', 'generated-artifact')],[],validator.spans)[0]
        self.assertEqual(row['line_range_state'],'binary-metadata-not-executed')
        self.assertEqual(row['unselected_text_ranges'],'not-a-text-line-model')
        self.assertEqual(row['runtime_status'],'not-executed')
        self.assertEqual(row['continuation_bucket'],'8-artifact-provenance-only-not-authorized')

    def test_zero_line_file_does_not_become_fully_read(self):
        row=reports.build_ledger([self.item(lines='0')],[],validator.spans)[0]
        self.assertEqual(row['line_range_state'],'zero-line-artifact')
        self.assertEqual(row['path_scope_state'],'inventory-only-no-selected-scope')
        with self.assertRaises(ValueError):
            reports.build_ledger([self.item(lines='0')],[('7B1',[self.scope()])],validator.spans)

    def test_historical_spelling_and_depth_stay_separate(self):
        scopes=[('7A',[self.scope(ranges='2-4;6-6',state='metadata-only')]),('7B1',[self.scope(ranges='4-8')])]
        row=reports.build_ledger([self.item()],scopes,validator.spans)[0]
        self.assertEqual(row['phase7A_ranges'],'2-4;6-6')
        self.assertEqual(row['phase7B1_ranges'],'4-8')
        self.assertEqual(row['declared_review_states'],'7A:metadata-only;7B1:synthetic-slices-only')
        self.assertEqual(row['declared_range_union_not_reading_certification'],'2-8')
        self.assertEqual(row['unselected_text_ranges'],'1-1;9-10')

    def test_ledger_preserves_original_order_and_inputs(self):
        inv=[self.item('z.cs'),self.item('a.cs')]
        scopes=[('7B1',[self.scope('a.cs')])]
        before=copy.deepcopy((inv,scopes))
        result=reports.build_ledger(inv,scopes,validator.spans)
        self.assertEqual([x['path'] for x in result],['z.cs','a.cs'])
        self.assertEqual((inv,scopes),before)

    def test_all_lines_in_ranges_is_not_semantic_or_runtime_certification(self):
        row=reports.build_ledger([self.item()],[('7B1',[self.scope(ranges='1-10')])],validator.spans)[0]
        self.assertEqual(row['line_range_state'],'all-lines-in-declared-ranges-not-semantic-certification')
        self.assertEqual(row['path_scope_state'],'selected-path-not-whole-file-certified')
        self.assertEqual(row['runtime_status'],'not-executed')

    def test_report_name_candidate_is_inventory_only(self):
        row=reports.build_ledger([self.item('frmRptSynthetic.cs')],[],validator.spans)[0]
        self.assertEqual(row['path_scope_state'],'inventory-only-no-selected-scope')
        self.assertEqual(row['continuation_bucket'],'7B2-report-print-candidate-by-name-only')

    def test_bidirectional_links_require_exact_order_and_nonempty(self):
        pool=[{'id':'FE7B-01','acceptance_ids':'P7BT-01;P7BT-02'}]
        tests=[{'id':'P7BT-01','feature_ids':'FE7B-01'},{'id':'P7BT-02','feature_ids':'FE7B-01'}]
        self.assertEqual(reports.bidirectional_errors(pool,tests,'feature_ids'),[])
        pool[0]['acceptance_ids']='P7BT-02;P7BT-01'
        self.assertTrue(reports.bidirectional_errors(pool,tests,'feature_ids'))
        pool[0]['acceptance_ids']=''
        self.assertTrue(reports.bidirectional_errors(pool,[],'feature_ids'))

    def test_inventory_sentinel_is_not_allowed_on_finding(self):
        reports.validate_source(validator,{'id':'P7-029','evidence':'none-inventory-only'}, {})
        self.assertTrue(any('Undeclared no-source sentinel' in e for e in validator.ERRORS))
        validator.ERRORS.clear()
        reports.validate_source(validator,{'id':'FE7B-32','evidence':'none-inventory-only'}, {})
        self.assertEqual(validator.ERRORS,[])

    def test_partial_transition_cannot_mutate_original_p7_core_or_schedule(self):
        old={'id':'P7-001','severity':'High','certainty':'confirmed','type':'synthetic','status':'open-not-remediated','title':'synthetic','evidence':'example.cs:1-2','next_phase':'8'}
        for field,value in [('severity','Medium'),('title','changed'),('status','closed'),('next_phase','7;8')]:
            validator.ERRORS.clear()
            validator.transition([old],[dict(old,**{field:value})],7,set(),preserve_followups=True)
            self.assertTrue(validator.ERRORS,field)

    def test_future_plan_cannot_be_renamed_passed(self):
        plan={k:'synthetic bounded text' for k in ('scenario','prerequisites','procedure','acceptance_criterion','safety_controls','invariant_ids','evidence')}
        plan.update(id='P7BT-01',status='passed')
        validator.proposed_tests([plan],'7B1')
        self.assertTrue(any('execution claim' in e for e in validator.ERRORS))


if __name__=='__main__':
    unittest.main(verbosity=2)
