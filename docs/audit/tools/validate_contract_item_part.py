#!/usr/bin/env python3
"""7B22/R4f bounded contract-item documentary checks, NEVER ERP acceptance.

Protect613 prior artifacts/313 exact rows/ALLnext_phase/evidence/raw314CRLF/
G200/827 originals/three entry freezes. B21 OWN313/raw314CRLF/indexes are
context-local and ALL36 original B21 cases run in an explicit historical child.
Earlier B20/32, B19/36 and B18/28 remain unchanged. Current CLI B22 and API B15
are independent. No protected edits/skips/global Path or subprocess mutation,
disk overlay/rebaseline/archive rewrite/application import or execution.
Unit-price provenance, repeat action and import line-result are local causes;
136/137/138 homologues and026 are not re-counted or extended. A stable accepted
Code guard is counterevidence to claiming an actual barcode/scanner entry.
No required Wscale3 support/SDK enum/price conversion/duplicate policy invented.
7B/7 partial; R4g/B23 proposed; six C axes unstarted;8 unauthorized.
"""
from __future__ import annotations

import collections
from contextlib import contextmanager
import csv
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from validate_financial_report_part import historical_b1_inputs, bidirectional_errors
from validate_amountword_contract_part import (
    expanded_source_evidence, historical_record_errors as historical26_errors)

ENTRY = 'b1f9524e552c36a05e1b351e2e12fd450ba051aa'
SNAPSHOT = 'evidence/findings-through-07B21.csv'
SNAPSHOT_SHA = 'f1616cae0ea2363f5b459716b56298067b9d47f16b94c85e62ab7249459032f0'
SHARED_SNAPSHOT = 'evidence/shared-indexes-through-07B21.json'
SHARED_SHA = '51984aa3813743612a03c925b0bbd1b40abbda2943ec1e2d745266a3bb12c272'
PROVENANCE_SHA = 'b76437da81084deb5cb9622c24aef8c4d6d8992108ee7b8ac86667c3e87b6228'
B21_CHECK_SHA = '02ed265704efe56144f104e2b991debe488aa410d7ee586536fe78e3fdba3177'
WITNESS_SHA = 'a911a378abc7da84b865bd939c66b27bcac1fd095b9227e7f5c1f4ad61f2455a'
HISTORICAL_RUN_SHA = '9451c55565541fa72d7304ee81f8f039f1cb1d8bde535b2c91082a7bdc0197f2'  # Actual27 OWN captures; capture-time tool identities retained, no archive regeneration.
SCOPE_FILE = 'review-scope-07B22.csv'
DOCUMENTARY = 'none-documentary-metadata'
NEW_IDS = ['P7-142', 'P7-143', 'P7-144']
PART_DOCS = ('PHASE-07B22.md', 'CONTRACT-ITEM-CONTRACTS-07B22.md',
             'VALIDATION-07B22.md', 'PHASE-07-REMAINING-07B22.md')
SHARED_DOCS = ('README.md', 'PLAN.md', 'IMPROVEMENTS.md')
TABLE_SPECS = (
    ('entry-reachability','EN7B22-',8), ('unit-price-lineage','UP7B22-',8),
    ('feature-implementation-matrix','FE7B22-',18), ('report-invariants','INV7B22-',18),
    ('acceptance-tests','P7B22T-',36), ('report-reconciliation','RC7B22-',6),
    ('root-adjudication','AD7B22-',10), ('residual-disposition','RS7B22-',14),
    ('split-register','SP7B22-',3), ('handoffs','H7B22-',6), ('questions','Q7B22-',6),
    ('remaining-workplan','RW7B22-',10), ('continuation-backlog','BK7B22-',10))
SENTINELS = {
    f'{prefix}{n:02d}' for prefix, nums in (
        ('FE7B22-',range(16,19)), ('INV7B22-',range(16,19)),
        ('P7B22T-',range(31,37)), ('RC7B22-',(6,)), ('AD7B22-',(10,)),
        ('RS7B22-',range(1,15)), ('H7B22-',range(1,7)), ('Q7B22-',range(1,7)))
    for n in nums}
ENTRY_BOUNDARIES = ['import-menu','invoice-wizard','SearchByCode','ReadBarcode',
                    'SearchByID','addNewItem','legacy-decoder','mode3-compatibility']
PRICE_BOUNDARIES = ['base-unit-writer','supplied-DDL','legacy-unit-load',
                    'legacy-customer-override','main-customer-override',
                    'no-override-control','same-unit-control','policy-and-type-lineage']


def row_sha(row):
    return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,
                                    separators=(',',':')).encode()).hexdigest()


@contextmanager
def historical_b21_inputs(v, frozen313, texts, raw):
    """Only OWN313 read_bytes plus existing three-text adapter; no disk writes."""
    if len(frozen313)!=313 or len({r.get('id') for r in frozen313})!=313:
        raise ValueError('Exactly313 distinct B21 OWN rows required')
    if set(texts)!=set(SHARED_DOCS) or any(not isinstance(t,str) for t in texts.values()):
        raise ValueError('Exactly three frozen shared texts required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM frozen bytes required')
    try:
        parsed = list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except (UnicodeError,csv.Error) as exc:
        raise ValueError('Malformed313 frozen registry') from exc
    if (parsed!=frozen313 or raw.count(b'\r\n')!=314 or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n',b'') for x in (b'\r',b'\n'))):
        raise ValueError('313 rows/raw314CRLF disagree')
    original = v.AUDIT
    target = (original/'findings.csv').resolve()

    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve()==target else super().read_bytes()

    try:
        v.AUDIT = FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen313,texts):
            yield
    finally:
        v.AUDIT = original


class HistoricalB21Subprocess:
    """Redirect only the EXACT protected B21 suite argv, with kwargs intact."""
    def __init__(self,backend,python,tool_dir):
        self.backend = backend
        self.expected = [python,'-B',str(tool_dir/'test_amountword_contract_audit_validator.py')]
        self.actual = [python,'-B',str(tool_dir/'run_historical_amountword_tests_07B22.py'),
                       '--through-part','B21']

    def __getattr__(self,name):
        return getattr(self.backend,name)

    def run(self,args,*pos,**kwargs):
        return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB21ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB21Subprocess(
            target.subprocess,target.sys.executable,target.AUDIT/'tools'))

    def __getattr__(self,name):
        return self._subprocess if name=='subprocess' else getattr(self._target,name)

    def __setattr__(self,name,value):
        setattr(self._target,name,value)


@contextmanager
def historical_b21_validation(v,report,prior,prov,frozen313):
    ck = v.check
    for name,digest in (('evidence/provenance-07B22.json',PROVENANCE_SHA),
                        (SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),
                        ('evidence/checks-07B21.json',B21_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B22 immutable entry:'+name)
    ck(prov['historical_artifact_count']==613 and len(frozen313)==313,'B22 entry613/313')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and
       prov['registry_at_entry_sha256']==SNAPSHOT_SHA and
       prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and
       prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B22 entry freeze identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h
           for n,h in prior['historical_artifact_sha256'].items()),
       'B22 protected583-to613 continuity')
    old = v.json.loads(v.read(v.AUDIT/'evidence/checks-07B21.json'))
    suites = old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='c2c895d0df0e4f106c4e5c2853219aa04303e002' and
       old['findings']['total_open_not_remediated']==313 and
       old['original_project_hashes_matching']==827 and old['validation']['errors']==[] and
       old['validation']['current_output_record_pending_first_write_not_placeholder'] is False,
       'B22 genuine B21 capturec2c, not delivered b1f entry')
    ck(len(suites)==22 and sum(x['tests_reported'] for x in suites.values())==566 and
       old['historical_artifact_sha256']==prior['historical_artifact_sha256'],
       'B22 archived B21 actual566/22/583 result')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
       and prov['genuine_B21_check_sha256']==B21_CHECK_SHA and
       prov['genuine_B21_check_record_checkout']==old['checkout_head'],
       'B22 completed pushed B21 entry identity')
    ck(prov['phase7B21_entry_consistency']==dict(original_hashes_matching=827,
       findings=313,audit_file_count=618,documentary_cases=566,self_test_suites=22,
       errors=[],erp_runtime_tests_executed=0),'B22 entry baseline independently checked')
    metadata = prov['restored_metadata_reconciliation']
    ck(metadata['verified_working_blobs_against_delivered_remote_git_tree']==1445 and
       metadata['working_application_and_audit_bytes_preserved'] is True and
       metadata['metadata_only_reset_mixed_same_branch'] is True,
       'B22 restored metadata reconciled only after exact blob equality')
    texts = v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    view = HistoricalB21ValidatorView(v)
    with historical_b21_inputs(view,frozen313,texts,(v.AUDIT/SNAPSHOT).read_bytes()):
        yield view
    record = report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][
        'test_amountword_contract_audit_validator.py']
    record.update(historical_parser_cutoff='B21-not-current-B22-default',
                  all_original_cases_executed_unmodified=True,
                  dedicated_child_launcher='tools/run_historical_amountword_tests_07B22.py',
                  actual_subprocess_argv=view.subprocess.actual,
                  no_test_skips_or_global_subprocess_or_path_patch=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B21-313-not-current-state',
                  phase_7B21_historical_input_mode=
                  'OWN313-exact314CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B21-test-child',
                  phase_7B21_adapter_context=dict(entry_provenance='evidence/provenance-07B22.json',
                      adapter_protected_artifacts_checked=613,
                      current_registry_and_shared_indexes_not_inputs=True,
                      archived_stdout_not_rewritten_after_push=True,
                      B21_parser_assertions_are_historical_preset_not_current_default=True))


def registry_preservation_errors(previous,current,raw,frozen):
    errors=[]
    if len(previous)!=313 or current[:313]!=previous:
        errors.append('B22 all313 exact fields/ALLnext_phase/evidence')
    if len(current)!=316 or [r.get('id') for r in current[313:]]!=NEW_IDS:
        errors.append('B22 only appended142..144')
    if (type(raw) is not bytes or type(frozen) is not bytes or not raw.startswith(frozen)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=317
            or not raw.endswith(b'\r\n')
            or any(x in raw.replace(b'\r\n',b'') for x in (b'\r',b'\n'))):
        errors.append('B22 exact313 raw prefix/317CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:
                errors.append('B22 raw/rows mismatch')
        except (UnicodeError,csv.Error):
            errors.append('B22 malformed registry')
    return errors


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    old,new=rows(previous),rows(current)
    if len(old)!=200 or new[:200]!=old:
        return ['B22 G01..200 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{i:02d}' for i in range(1,206)]:
        return ['B22 G201..205 only, exact order']
    return []


def ledger_errors(entry,prices):
    errors=[]
    for data,names,label in ((entry,ENTRY_BOUNDARIES,'entry'),(prices,PRICE_BOUNDARIES,'price')):
        if len(data)!=8 or [r.get('boundary') for r in data]!=names:
            errors.append('B22 eight ordered '+label+' boundaries')
        for r in data:
            for k in ('owner_role','required_redacted_input','impact_if_unavailable',
                      'next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(r.get(k),str) or not r[k].strip():
                    errors.append('B22 '+label+' responsibility:'+k)
            if r.get('runtime_status')!='not-executed':
                errors.append('B22 '+label+' runtime overclaim')
    if len(entry)==8 and (entry[2].get('reachability_observation')!=
            'direct-ID-branch-when-stable-accepted-Code' or entry[3].get('reachability_observation')!=
            'conditional-fallback-not-scanner-entry-proof' or entry[7].get('reachability_observation')!=
            'owner-support-unresolved-not-new-finding'):
        errors.append('B22 stable guard/conditional fallback/mode3 not accepted support')
    if len(prices)==8 and prices[3].get('observation')!='price-unit-not-selected-or-converted':
        errors.append('B22 foreign-unit customer projection is the cause, not resolver026')
    return errors


def current_link_errors(features,invariants,tests):
    errors=[]
    if (len(features),len(invariants),len(tests))!=(18,18,36):
        errors.append('B22 FE18/INV18/T36')
    for n,(fe,inv) in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id') or any(
                inv.get(k)!=fe.get(k) for k in ('finding_ids','evidence','acceptance_ids')):
            errors.append('B22 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or ';'.join(t['id'] for t in related)!=fe.get('acceptance_ids'):
            errors.append('B22 two reverse-linked plans per feature')
        if n<=3 and (fe.get('finding_ids')!=NEW_IDS[n-1] or any(
                t.get('plan_kind')!='finding-specific' or t.get('finding_ids')!=NEW_IDS[n-1]
                for t in related)):
            errors.append('B22 three independent causes/plans')
        for k in ('owner_role','required_redacted_input','impact_if_unavailable','next_step'):
            if not isinstance(fe.get(k),str) or not fe[k].strip():
                errors.append('B22 feature responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')
    errors+=bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant') for r in invariants})!=18 or len({
            r.get('acceptance_criterion') for r in tests})!=36:
        errors.append('B22 distinct substantive invariants/criteria')
    if any(r.get('status')!='not-executed' for r in tests):
        errors.append('B22 acceptance never executed')
    return errors


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:
        return ['B22 all14 upstream residuals required']
    errors=[]
    for old,new in zip(upstream,current):
        if (new.get('upstream_residual_id')!=old.get('id') or
                new.get('upstream_artifact')!='evidence/residual-disposition-07B21.csv' or
                new.get('upstream_row_sha256')!=row_sha(old) or
                new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):
            errors.append('B22 upstream residual identity/hash/contracts')
        for k in ('local_result','owner_role','required_redacted_input','impact_if_unavailable',
                  'next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str) or not new[k].strip():
                errors.append('B22 residual responsibility:'+k)
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):
            errors.append('B22 no lost old required input')
        mapped={x.replace('7B21-','7B22-') for x in
                old.get('current_handoff_or_split_ids','').split(';') if x}
        if not mapped <= set(new.get('current_handoff_or_split_ids','').split(';')):
            errors.append('B22 no lost mapped handoff/split responsibility')
        if (new.get('disposition')!=old.get('disposition') or
                new.get('disposition') not in {'external-handoff','split-explicitly','assessment-source-bound'} or
                new.get('runtime_status')!='not-executed'):
            errors.append('B22 no residual approval/runtime overclaim')
    return errors


def split_errors(current,upstream):
    errors=[]
    if len(current)!=3 or len(upstream)!=3:
        return ['B22 exactlythree upstream further static splits']
    for old,new in zip(upstream,current):
        if (new.get('upstream_split_id')!=old.get('id') or
                new.get('upstream_artifact')!='evidence/split-register-07B21.csv' or
                new.get('upstream_row_sha256')!=row_sha(old) or
                not new.get('required_input','').startswith(old.get('required_input',''))):
            errors.append('B22 split ancestry/no lost old required input')
        for k in ('title','candidate_scope_not_certified','reason_for_split','owner_role',
                  'required_input','next_static_action','static_exit_criterion'):
            if not isinstance(new.get(k),str) or not new[k].strip():
                errors.append('B22 reasoned split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started' or new.get('runtime_status')!='not-executed':
            errors.append('B22 further split not started/accepted')
    return errors


def remaining_work_errors(work):
    if len(work)!=10:
        return ['B22 four B packages/six C axes']
    expected=['bounded-parent-contract-delivered-residuals-open']*2+[
        'bounded-shared-contract-delivered-residuals-open',
        'bounded-R4f-contract-items-delivered-residuals-open']+['planned-not-started']*6
    errors=[]
    if [r.get('status') for r in work]!=expected or [r.get('part_family') for r in work]!=['7B']*4+['7C']*6:
        errors.append('B22 boundedR4f/six C unstarted, not closure')
    if any(r.get('runtime_status')!='not-executed' or
           r.get('counts_are_sessions_or_completion_percent')!='false' for r in work):
        errors.append('B22 no runtime/session/percentage overclaim')
    return errors


def witness_metadata_errors(w):
    errors=[]
    for k in ('application_code_imported_or_executed','dotnet_wpf_sql_or_excel_executed',
              'phase7C_started','phase8_authorized_or_started'):
        if w.get(k) is not False:
            errors.append('B22 false-only boundary:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed',
              'scanner_or_printer_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:
            errors.append('B22 integer-zero boundary:'+k)
    for k in ('B_R4f_bounded_not_whole7B_closure',
              'unresolved_external_contracts_and_explicit_splits_retained'):
        if w.get(k) is not True:
            errors.append('B22 true-only boundary:'+k)
    for k in ('illustration_count','lexical_check_count'):
        if type(w.get(k)) is not int or w[k]!=12:
            errors.append('B22 exact12 witness count:'+k)
    e=w.get('retained_additive_B10_arithmetic_erratum',{})
    if (e!=dict(local_cost=10,reference_cost=120,equality1_control=10,
                protected_G138_not_rewritten=True) or
            any(type(e.get(k)) is not int for k in ('local_cost','reference_cost','equality1_control')) or
            e.get('protected_G138_not_rewritten') is not True):
        errors.append('B22 additiveB10 10vs120/equality1=10/G138 retained')
    return errors


def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count')) is not int or h['historical_mode_count']!=27 or len(modes)!=27:
        return ['B22 exactly27 actual OWN records required']
    errors=historical26_errors(dict(historical_mode_count=26,historical_modes=modes[:26],
                                   errors=h.get('errors')))
    last=modes[-1]
    if (last.get('mode')!='B21' or last.get('findings_total')!=313 or
            last.get('registry_used')!=SNAPSHOT or last.get('process_exit_code')!=0 or
            last.get('validation_errors')!=[] or last.get('original_project_hashes_matching')!=827):
        errors.append('B22 B21 historical OWN313, not live316')
    if (last.get('audit_checker_self_test_cases_reported'),last.get('audit_checker_self_test_suite_count'))!=(566,22):
        errors.append('B22 actual historicalB21 aggregate566/22')
    child=last.get('historical_B21_child') or {}
    expected=dict(tests_reported=36,expected_tests=36,process_exit_code=0,result='passed',
                  historical_parser_cutoff='B21-not-current-B22-default',
                  all_original_cases_executed_unmodified=True,
                  dedicated_child_launcher='tools/run_historical_amountword_tests_07B22.py',
                  no_test_skips_or_global_subprocess_or_path_patch=True)
    for k,value in expected.items():
        if child.get(k)!=value or type(child.get(k)) is not type(value):
            errors.append('B22 B21 ALL36 explicit historical child:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(last.get(k)) is not int or last[k]!=0:
            errors.append('B22 no historical ERP/SQL run')
    if not isinstance(last.get('stdout_sha256'),str) or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256']) is None:
        errors.append('B22 historical stdout identity')
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:
        return
    if row['evidence']==DOCUMENTARY:
        v.check(row['id'] in SENTINELS,'B22 undeclared documentary sentinel:'+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B22 fabricated source for documentary gate:'+row['id'])
        v.evidence(row['evidence'],row['id'])
        try:
            expanded=expanded_source_evidence(row['evidence'])
        except ValueError as exc:
            v.check(False,'B22 invalid scoped source '+row['id']+':'+str(exc))
            return
        v.scoped_evidence(expanded,scope,row['id']+' boundedB22',phase=7)


def extend_contract_items(v,report,prov,frozen313):
    ck,rows=v.check,v.rows
    current=rows('findings.csv')
    new=current[313:]
    for error in registry_preservation_errors(frozen313,current,(v.AUDIT/'findings.csv').read_bytes(),
                                              (v.AUDIT/SNAPSHOT).read_bytes()):
        ck(False,error)
    ck(len({r['id'] for r in current})==316,'B22 distinct316 IDs')
    ck(rows('evidence/historical-extensions-07B22.csv')==[],'B22 zero historical extensions')
    v.distributions(new,dict(Medium=3),dict(confirmed=3),'B22 only')
    for r in new:
        ck((r['type'],r['status'],r['next_phase'])==
           ('implementation-defect','open-not-remediated','8'),'B22 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==
       [(r['id'],r['title']) for r in new],'B22 heading/registry exact')
    for k in ('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):
        ck(prov[k] is False,'B22 no implicit start:'+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        ck(type(prov[k]) is int and prov[k]==0,'B22 no ERP/SQL:'+k)
    selected=rows(SCOPE_FILE)
    scope={r['path']:v.spans(r['ranges']) for r in selected}
    original={r['path'] for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==12,'B22 twelve bounded scope paths')
    for r in selected:
        ck(r['path'] in original and r['review_state']==
           'selected-static-contract-item-pricing-repeat-import-reachability-slices-not-runtime-certified'
           and bool(r['focus']),'B22 selected scope identity/depth')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:
        validate_source(v,r,scope)
    known={r['id'] for r in current}|{f'H7B22-{n:02d}' for n in range(1,7)}
    tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B22.csv')
        tables[prefix]=data
        v.sequential(data,prefix,count)
        if data and 'finding_ids' in data[0]:
            v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str) and x.strip() for x in r.values()),'B22 incompleteCSV:'+r['id'])
            validate_source(v,r,scope)
            if 'runtime_status' in r:
                ck(r['runtime_status']=='not-executed','B22 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x] for x in ('FE7B22-','INV7B22-','P7B22T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['EN7B22-'],tables['UP7B22-']):
        ck(False,error)
    v.proposed_tests(tests,'7B22')
    fids,iids,tids=[{r['id'] for r in pool} for pool in (fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids')
    v.related(fe+inv,tids,'acceptance_ids')
    v.related(tables['EN7B22-']+tables['UP7B22-'],fids,'feature_ids')
    for pool,label in ((fe,'features'),(inv,'invariants'),(tests,'plans')):
        v.covered(new,pool,'B22 '+label)
    for r in tables['RC7B22-']:
        fs=[f for f in fe if f['id'] in r['feature_ids'].split(';')]
        unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        evidence=';'.join(dict.fromkeys(x for f in fs if f['evidence']!=DOCUMENTARY
                                       for x in f['evidence'].split(';'))) or DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids') and r['acceptance_ids']==unique('acceptance_ids')
           and r['evidence']==evidence,'B22 exact RC source/FE lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in (residual_errors(tables['RS7B22-'],rows('evidence/residual-disposition-07B21.csv'))+
                  split_errors(tables['SP7B22-'],rows('evidence/split-register-07B21.csv'))+
                  remaining_work_errors(tables['RW7B22-'])):
        ck(False,error)
    hids={r['id'] for r in tables['H7B22-']}
    sids={r['id'] for r in tables['SP7B22-']}
    v.related(tables['RS7B22-'],hids|sids,'current_handoff_or_split_ids')
    v.related(tables['Q7B22-'],hids,'handoff_ids')
    for r in tables['H7B22-']:
        ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B22 no invented approval')
    for r in tables['Q7B22-']:
        ck(r['status']=='unanswered-no-secrets-requested','B22 no invented policy answer')
    for n,r in enumerate(tables['BK7B22-'],1):
        ck(r['prior_backlog_id']==f'BK7B21-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}'
           and r['status']!='complete','B22 backlog ancestry/uncompleted')
    ck([r['status'] for r in tables['BK7B22-'][2:6]]==['not-started']*4,'B22 C axes remain unstarted')
    ad=tables['AD7B22-']
    v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids'] for r in ad if r['decision']=='new-local-root']==NEW_IDS,
       'B22 only three adjudicated new causes')
    for r,a in zip(new,ad):
        ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B22 adjudication source chain')
    ck(all(r['comparison_depth']==
           'all313-registry-titles-classifications-evidence-paths-plus-selected-nearest-source-chains-not-all-historical-bodies'
           for r in ad),'B22 honest dedup depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv' for n in range(2,8)]+[
        f'review-scope-07B{n}.csv' for n in range(1,22)]
    before={r['path'] for name in prior_names for r in rows(name)}
    paths=set(scope)
    ck((len(before),len(paths&before),len(paths-before),len(before|paths),
        len(original-(before|paths)))==(412,8,4,416,411),'B22 paths not completion percentage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B22.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B21.md','evidence/split-register-07B21.csv']
       and decision['selected_upstream_split']=='SP7B21-03'
       and decision['bounded_cross_boundary_split']=='SP7B21-01' and decision['entry']==ENTRY
       and decision['bookkeeping']==dict(selected_paths=12,prior_union=412,overlap=8,new=4,
            union=416,complement=411,complement_kinds={'source':346,'generated-artifact':61,'project-or-resource':4}),
       'B22 authority/reasoned scope')
    ck(v.sha(v.AUDIT/'evidence/contract-item-witnesses-07B22.json')==WITNESS_SHA,'B22 actual witness stdout')
    witness,match=v.recompute('evidence/contract-item-witnesses-07B22.json','tools/check_contract_item_witnesses.py')
    for error in witness_metadata_errors(witness):
        ck(False,error)
    ck(witness['errors']==[],'B22 witness observations')
    for key,prefix,flag in (('illustrations','ALG7B22-','illustration_assertions_passed'),
                            ('static_lexical_contract_checks','ST7B22-','documented_text_observation_matches')):
        data=witness[key]
        v.sequential(data,prefix,12);v.related(data,known)
        for r in data:
            ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),
               'B22 witness not runtime/policy acceptance')
            validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B22 lexical read',phase=7)
    ck(len(witness['bounded_source_reads_not_semantic_coverage'])==31,'B22 actual31 bounded text reads')
    discovery=witness['qualified_literal_discovery']
    ck(discovery['not_complete_callgraph_or_capability_census'] is True
       and discovery['scanned_bodies_not_reviewed'] is True
       and discovery['source_csharp_paths_lexically_scanned']==477
       and len(discovery['legacy_SearchForBarcode'])==len(discovery['legacy_GetItemByIDcontract'])==1
       and len(discovery['lexical_utf8_replacement_paths_not_encoding_acceptance'])==4,
       'B22 lexical discovery/encoding/reachability limits')
    ck([(r['source_path'],r['call_line_start'],r['call_line_end'])
        for r in discovery['legacy_SearchForBarcode']]==[
        ('SmartAuditERP/Form_WPF/frmcontract.xaml.cs',1795,1796)],'B22 exact selected static token')
    ck([(r['source_path'],r['call_line_start'],r['call_line_end'])
        for r in discovery['legacy_GetItemByIDcontract']]==[
        ('SmartAuditERP/Form_WPF/frmcontract.xaml.cs',1752,1753)],'B22 exact selected new-instance token')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):
        ck(False,error)
    pending=False
    source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):
                continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B22.json').resolve() and not target.exists():
                pending=True
                continue
            v.LINK_COUNT+=1;ck(target.exists(),'B22 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),
                                  scope,name,phase=7)
    for name in SHARED_DOCS:
        ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B22.md',
            'PHASE-07-REMAINING-07B22.md','7B23','غير مأذونة','b1f9524','10ba215')),
            'B22 shared index current boundary:'+name)
    hist_path='evidence/historical-mode-verification-07B22.json'
    ck(HISTORICAL_RUN_SHA is not None and (v.AUDIT/hist_path).is_file(),
       'B22 historical27 genuinely captured')
    if (v.AUDIT/hist_path).is_file():
        ck(v.sha(v.AUDIT/hist_path)==HISTORICAL_RUN_SHA,'B22 actual historical27 identities')
        historical=v.json.loads(v.read(v.AUDIT/hist_path))
        for error in historical_record_errors(historical):
            ck(False,error)
        ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD
           and historical['branch']==v.BRANCH,'B22 historical source/entry/capture')
        report['phase_7B22_executed_historical_documentary_modes']=dict(record=hist_path,
            sha256=HISTORICAL_RUN_SHA,modes_reported=27,all_documentary_exit_codes_zero=True,
            B21_OWN313_raw314CRLF_and_historical36_child=True,
            null_means_aggregate_not_reported_not_zero=True,
            not_original_metric_replay_or_erp_tests=True)
    tools=['check_contract_item_witnesses.py','validate_contract_item_part.py',
           'run_historical_amountword_tests_07B22.py','test_contract_item_audit_validator.py']
    for name in tools:
        try:
            v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:
            ck(False,'B22 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_contract_item_audit_validator.py')],
                         cwd=v.ROOT,capture_output=True,text=True,timeout=45)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout)
    count=int(m[1]) if m else None
    passed=run.returncode==0 and count==40
    ck(passed,'B22 40 documentary self-tests/count: '+(run.stderr[-3000:] if not passed else ''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(
        tests_reported=count,expected_tests=40,process_exit_code=run.returncode,
        result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({
        'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B22-316-bounded-R4f-contract-items-not-7B-or-runtime-closure',
        phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,23))+'-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B23-proposed-R4g-explicit-SP01-SP02-SP03-and-external-contracts',
                                 '7C-six-axes-not-started'],
        registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],
        date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=144,phase_7B22=3,total_open_not_remediated=316,
        severity=dict(collections.Counter(r['severity'] for r in current)),
        certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:12,'phase_7B22_prior_union':412,
        'phase_7B22_overlap_with_prior_union':8,'phase_7B22_new_paths':4,
        'unique_union_not_line_or_execution_coverage':416,'inventory_only_no_selected_scope':411})
    report['phase_7B21_historical_evidence']=dict(frozen_registry=SNAPSHOT,
        frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=613,
        historical_check_record_overwritten=False,genuine_b21_stdout_sha256_unchanged=B21_CHECK_SHA,
        partial7B22_append_only_extensions=[],
        all313_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B22_contract_item_trace_limits']=dict(
        selected_entry_boundaries=8,selected_unit_price_boundaries=8,
        qualified_legacy_static_tokens=1,explicit_new_instance_tokens=1,
        stable_Code_guard_is_counterevidence_not_dead_code_or_scanner_reachability_proof=True,
        source_csharp_paths_lexically_scanned_not_bodies=477,selected_paths_are_bounded_slices=12,
        current_features_or_documentary_contracts=18,invariants_not_executed_tests=18,
        acceptance_plans_not_executed=36,residual_inputs=14,explicit_further_static_splits=3,
        B_R4f_delivered_not_whole_R4_SP03_or7B_closure=True,
        retained_potential_roots_not_promoted=['P4-014','P7-132'],
        prior136_137_138_and026_not_recounted_or_extended=True,
        external_enum_unit_conversion_duplicate_policy_or_Wscale3_support_invented=False,
        C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B22_illustrations_not_erp_tests=12,
        phase_7B22_lexical_checks_not_erp_tests=12,
        phase_7B22_bounded_source_reads_not_semantic_coverage=31,
        phase_7B22_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=(
        'Read-only bounded7B22/R4f:613 protected artifacts/313 EXACT rows and ALLnext_phase/evidence/raw314CRLFprefix/G200/827 originals/three entry freezes. '
        'Three Medium confirmed source-local causes142..144: customer scalar price loses price-unit identity after unit load in two implementations; '
        'repeat-dialog visible add/new labels emit2/1 while selected loaders consume1=increment and2=new; contract importer void result then code+last-index '
        'projection can miss a merged nonlast line or mutate last matching line after Action3 no-insertion. No C#/WPF/modal/Excel/SQL/SDK execution or saved/printed effect observed. '
        'Stable accepted Code guard normally selects direct-ID path; two matching query outcomes are supplied assumptions, not an atomicity/actual-scanner/dead-code proof. '
        'Legacy barcode136/137/138 and resolver026 homologues not re-counted/extended; main mode3 versus legacy1/2 is an unresolved support question, not a new required capability. '
        'Same-unit/no-override and no-insert loader controls constrain findings, not acceptance; caller may still mutate after cancel. Hypothetical ratio12/reference96 is not approved conversion/discount/VAT/duplicate policy. '
        'EN8/UP8 and477 lexical scans with4 UTF8 replacement paths/1static+1explicit-new-instance token are not body reviews/allcallgraph/census;12slice paths/8overlap/4new→416/complement411 not completion percentage or411 C tasks;455 historicalFE not rereviewed. '
        '18FE/INV36 acceptance plans NOT executed;14 residuals/3splits/HQ6 not external approvals. R4g/B23 proposed;7B/7 partial;6C unstarted;8 unauthorized. '
        'B21 OWN313/exact314CRLF/indexes in memory and ALL36 original cases in explicit historical presetB21 child; B20/32,B19/36,B18/28 unchanged. Current B22 CLI/default independently tested40 cases; API main defaultB15 retained. '
        'No protected edits/skips/globalPath or subprocess mutation/disk overlay/rebaseline/archive rewrite. Source10ba/B22 completedB21push-entryb1f9524/genuineB21stdoutcapturec2c895d distinct. '
        'Restored Git metadata was aligned by same-branch mixed reset only after all1445 worktree blobs matched delivered Git objects, zero application/audit byte writes. '
        'Genuine27 historical captures carry actual capture-time tool identities; not a claim of wholesale final-code/postpush rerun. B10 additive10vs120/equality1=10/G138 retained. '
        'Financial/ACL/stock/save and production020/021 barriers,034/035/136..141 unchanged;014/132 potential. No application import/build/provider/UtilitiesProj/ToDataTable/REPX/scanner/printer/business data/secrets/remediation/operational measurement/acceptance. next_phase8 planning not permission.')
