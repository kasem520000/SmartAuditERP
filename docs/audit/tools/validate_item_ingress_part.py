#!/usr/bin/env python3
"""Read-only B23/R4g picker/batch/seed-hydration documentary checks, NEVER ERP.

Protect643 historical artifacts,316 exact dictionaries/ALLnext_phase/evidence/
raw317CRLF prefix/G205/827 originals/three entry freezes. ALL40 B22 cases run
in an explicit historical child with OWN316/raw317CRLF/indexes and module-local
A path for the suite's registry read. No protected edits/skips/global Path or
shared subprocess mutation/disk overlay/rebaseline/archive rewrite.
145 potential pending final-selection/basket contract;146 batch cursor and147
seed replacement are source-local causes independent of143/144. Homologues143
not counted/extended.11 literal dialog constructions/477 lexical scans are not
body reviews/all callers/census.7B/7 partial;R4h/B24 proposed;7C unstarted;8
unauthorized. Independent repairs never merged or assumed synchronized here.
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
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,bidirectional_errors
from validate_contract_item_part import row_sha,expanded_source_evidence
from validate_contract_item_part import historical_record_errors as historical27_errors

ENTRY='3276579931925bff37bbf45c5b43efb7fbcd0118'
SNAPSHOT='evidence/findings-through-07B22.csv'
SNAPSHOT_SHA='81671191c1841bca1c7a7e0f3e7725644104b1d654992f5dc44b00dbdd0d5ce3'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B22.json'
SHARED_SHA='c1195fa8e009432b41bdfaba60f7d052c2f3d9c42b10d0782a29883929b880ea'
PROVENANCE_SHA='1eb22ab37d41094004c9acf8a0888322d51eb38b888334894b9105cfe27e06ed'
B22_CHECK_SHA='07b0374689310636a1267aacc30bee808950718fbf390cad91b65d7539a4d3ae'
WITNESS_SHA='ebca4a9a8faf1546b62dd91235af469c96b5c9d3322c843861680a6069b2f61e'
HISTORICAL_RUN_SHA='b67d3ecc7125f6cbfe163ca35a805895846789351800de539ef76469b28283d6'  # Actual28 OWN captures; capture-time tools retained, archive never regenerated.
SCOPE_FILE='review-scope-07B23.csv'
DOCUMENTARY='none-documentary-metadata'
NEW_IDS=['P7-145','P7-146','P7-147']
PART_DOCS=('PHASE-07B23.md','ITEM-INGRESS-CONTRACTS-07B23.md','VALIDATION-07B23.md','PHASE-07-REMAINING-07B23.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS=(('selection-batch-lineage','SB7B23-',8),('import-field-lineage','IM7B23-',8),
 ('feature-implementation-matrix','FE7B23-',18),('report-invariants','INV7B23-',18),
 ('acceptance-tests','P7B23T-',36),('report-reconciliation','RC7B23-',6),
 ('root-adjudication','AD7B23-',10),('residual-disposition','RS7B23-',14),
 ('split-register','SP7B23-',3),('handoffs','H7B23-',6),('questions','Q7B23-',6),
 ('remaining-workplan','RW7B23-',10),('continuation-backlog','BK7B23-',10))
SENTINELS={f'{p}{n:02d}'for p,ns in(
 ('FE7B23-',range(16,19)),('INV7B23-',range(16,19)),('P7B23T-',range(31,37)),
 ('RC7B23-',(6,)),('AD7B23-',(10,)),('RS7B23-',range(1,15)),
 ('H7B23-',range(1,7)),('Q7B23-',range(1,7)))for n in ns}
SELECTION_BOUNDARIES=['picker-events','selection-history','confirmation','sales-entry',
 'sales-loop','sales-loader','purchase-loop','no-confirm-control']
IMPORT_BOUNDARIES=['wizard-output','import-seed','description','unit','quantity','price',
 'replacement-identity','report-and-failure-limits']
DEDUP_DEPTH='all316-registry-titles-classifications-evidence-paths-plus-selected-nearest-bodies-and-source-chains-not-all-historical-bodies'

@contextmanager
def historical_b22_inputs(v,frozen316,texts,raw):
    """OWN316 only; a context-local Path subclass, NEVER pathlib/global/disk patch.

    read_text is needed for the protected B22 suite's own A/registry read;
    unmodified suite receives this SAME path class in its isolated child.
    Real unrelated paths/reads still use pathlib. read_bytes retains exactCRLF;
    read_text follows normal universal-newline text decoding.
    """
    if len(frozen316)!=316 or len({r.get('id')for r in frozen316})!=316:
        raise ValueError('Exactly316 distinct B22 OWN rows required')
    if set(texts)!=set(SHARED_DOCS) or any(not isinstance(s,str)for s in texts.values()):
        raise ValueError('Exactly three frozen shared texts required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact frozen noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except(UnicodeError,csv.Error)as exc:raise ValueError('Malformed316 frozen registry')from exc
    if(parsed!=frozen316 or raw.count(b'\r\n')!=317 or not raw.endswith(b'\r\n')
       or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n'))):
        raise ValueError('316 rows/raw317CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve()==target else super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            if self.resolve()==target:
                return io.StringIO(raw.decode(encoding or 'utf-8',errors or 'strict'),newline=None).read()
            return super().read_text(encoding=encoding,errors=errors)
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen316,texts):yield
    finally:v.AUDIT=original

class HistoricalB22Subprocess:
    """Redirect the exact protected B22 suite argv only; all other calls intact."""
    def __init__(self,backend,python,tool_dir):
        self.backend=backend
        self.expected=[python,'-B',str(tool_dir/'test_contract_item_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_contract_item_tests_07B23.py'),'--through-part','B22']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):
        return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)

class HistoricalB22ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB22Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess'else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)

@contextmanager
def historical_b22_validation(v,report,prior,prov,frozen316):
    ck=v.check
    for name,digest in(('evidence/provenance-07B23.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),
      (SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B22.json',B22_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B23 immutable entry:'+name)
    ck(prov['historical_artifact_count']==643 and len(frozen316)==316,'B23 entry643/316')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
       and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,
       'B23 entry freeze identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),
       'B23 protected613-to643 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B22.json'))
    suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='b1f9524e552c36a05e1b351e2e12fd450ba051aa'
       and old['findings']['total_open_not_remediated']==316 and old['original_project_hashes_matching']==827
       and old['validation']['errors']==[]
       and old['validation']['current_output_record_pending_first_write_not_placeholder']is False,
       'B23 genuine B22 captureb1f, not completed entry3276579')
    ck(len(suites)==23 and sum(r['tests_reported']for r in suites.values())==606
       and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],
       'B23 archived B22 actual606/23/613 result')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
       and prov['genuine_B22_check_sha256']==B22_CHECK_SHA
       and prov['genuine_B22_check_record_checkout']==old['checkout_head'],'B23 completed pushed B22 entry identity')
    ck(prov['phase7B22_entry_consistency']==dict(original_hashes_matching=827,findings=316,
       audit_file_count=648,documentary_cases=606,self_test_suites=23,errors=[],erp_runtime_tests_executed=0),
       'B23 independently checked entry consistency')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB22ValidatorView(v)
    with historical_b22_inputs(view,frozen316,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_contract_item_audit_validator.py']
    record.update(historical_parser_cutoff='B22-not-current-B23-default',all_original_cases_executed_unmodified=True,
       dedicated_child_launcher='tools/run_historical_contract_item_tests_07B23.py',actual_subprocess_argv=view.subprocess.actual,
       no_test_skips_or_global_subprocess_or_path_patch=True,
       suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B22-316-not-current-state',
       phase_7B22_historical_input_mode='OWN316-exact317CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B22-test-child',
       phase_7B22_adapter_context=dict(entry_provenance='evidence/provenance-07B23.json',adapter_protected_artifacts_checked=643,
          current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
          B22_parser_assertions_are_historical_preset_not_current_default=True,
          B22_suite_own_A_uses_context_local_registry_path=True))

def registry_preservation_errors(previous,current,raw,frozen):
    errors=[]
    if len(previous)!=316 or current[:316]!=previous:errors.append('B23 all316 exact fields/ALLnext_phase/evidence')
    if len(current)!=319 or[r.get('id')for r in current[316:]]!=NEW_IDS:errors.append('B23 only appended145..147')
    if(type(raw)is not bytes or type(frozen)is not bytes or not raw.startswith(frozen)
       or raw.startswith(b'\xef\xbb\xbf')or raw.count(b'\r\n')!=320 or not raw.endswith(b'\r\n')
       or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n'))):
        errors.append('B23 exact316 raw prefix/320CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B23 raw/row mismatch')
        except(UnicodeError,csv.Error):errors.append('B23 malformed registry')
    return errors

def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    old,new=rows(previous),rows(current)
    if len(old)!=205 or new[:205]!=old:return['B23 G01..205 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{n:02d}'for n in range(1,211)]:
        return['B23 G206..210 only, exact order']
    return[]

def ledger_errors(selection,imports):
    errors=[]
    for data,names,label in((selection,SELECTION_BOUNDARIES,'selection'),(imports,IMPORT_BOUNDARIES,'import')):
        if len(data)!=8 or[r.get('boundary')for r in data]!=names:errors.append('B23 ordered8 '+label+' boundaries')
        for r in data:
            for k in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable',
                     'next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(r.get(k),str)or not r[k].strip():errors.append('B23 '+label+' responsibility:'+k)
            if r.get('runtime_status')!='not-executed':errors.append('B23 '+label+' runtime overclaim')
    for data,checks in((selection,{1:'adds-without-deselection-reconciliation-policy-unresolved',
       4:'cursor-left-at-last-successful-row-between-iterations',5:'removes-current-in-range-even-if-nonempty',
       6:'per-iteration-empty-seed-control-not-all-editors'}),
       (imports,{1:'fields-populate-seed-before-it-is-replaced',
          6:'unique-success-without-duplicate-or-last-index-projection',
          7:'literal-entry-and-success-assumptions-not-deployment'})):
        if len(data)==8 and any(data[i].get('observation')!=s for i,s in checks.items()):
            errors.append('B23 source cause/potential/control/entry limits')
    return errors

def current_link_errors(features,invariants,tests):
    errors=[]
    if(len(features),len(invariants),len(tests))!=(18,18,36):errors.append('B23 FE18/INV18/T36')
    for n,(fe,inv)in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):
            errors.append('B23 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or';'.join(t['id']for t in related)!=fe.get('acceptance_ids'):errors.append('B23 two reverse-linked plans per feature')
        if n<=3 and(fe.get('finding_ids')!=NEW_IDS[n-1]or any(t.get('plan_kind')!='finding-specific'
           or t.get('finding_ids')!=NEW_IDS[n-1]for t in related)):errors.append('B23 three distinct finding-specific plans')
        for k in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(fe.get(k),str)or not fe[k].strip():errors.append('B23 feature responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=18 or len({r.get('acceptance_criterion')for r in tests})!=36:
        errors.append('B23 distinct substantive invariants/criteria')
    if any(r.get('status')!='not-executed'for r in tests):errors.append('B23 acceptance never executed')
    return errors

def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return['B23 all14 exact upstream residuals required']
    errors=[]
    for old,new in zip(upstream,current):
        if(new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B22.csv'
           or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):
            errors.append('B23 upstream residual identity/hash/contracts')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step',
                 'static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B23 residual responsibility:'+k)
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):
            errors.append('B23 no lost old required input')
        mapped={x.replace('7B22-','7B23-')for x in old.get('current_handoff_or_split_ids','').split(';')if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B23 no lost mapped route')
        if(new.get('disposition')!=old.get('disposition')or new.get('disposition')not in{
           'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed'):
            errors.append('B23 no residual approval/runtime overclaim')
    return errors

def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return['B23 exactlythree upstream further static splits']
    errors=[]
    for old,new in zip(upstream,current):
        if(new.get('upstream_split_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/split-register-07B22.csv'
           or new.get('upstream_row_sha256')!=row_sha(old)
           or not new.get('required_input','').startswith(old.get('required_input',''))):errors.append('B23 split ancestry/no lost input')
        for k in('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B23 reasoned split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started'or new.get('runtime_status')!='not-executed':errors.append('B23 further split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work)!=10:return['B23 four B packages/six C axes']
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open',
       'bounded-R4g-item-ingress-delivered-residuals-open']+['planned-not-started']*6
    errors=[]
    if[r.get('status')for r in work]!=expected or[r.get('part_family')for r in work]!=['7B']*4+['7C']*6:
        errors.append('B23 boundedR4g/six C unstarted, not closure')
    if any(r.get('runtime_status')!='not-executed'or r.get('counts_are_sessions_or_completion_percent')!='false'for r in work):
        errors.append('B23 no runtime/session/percentage overclaim')
    return errors

def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','dotnet_wpf_sql_or_excel_executed','phase7C_started',
             'phase8_authorized_or_started','application_remediation_performed'):
        if w.get(k)is not False:errors.append('B23 false-only boundary:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B23 integer-zero boundary:'+k)
    for k in('B_R4g_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained'):
        if w.get(k)is not True:errors.append('B23 true-only boundary:'+k)
    for k in('illustration_count','lexical_check_count'):
        if type(w.get(k))is not int or w[k]!=12:errors.append('B23 exact12 witness count:'+k)
    err=w.get('retained_additive_B10_arithmetic_erratum',{})
    if(err!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)
       or any(type(err.get(k))is not int for k in('local_cost','reference_cost','equality1_control'))
       or err.get('protected_G138_not_rewritten')is not True):errors.append('B23 additiveB10 10vs120/equality1=10/G138 retained')
    return errors

def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count'))is not int or h['historical_mode_count']!=28 or len(modes)!=28:
        return['B23 exactly28 actual OWN records required']
    errors=historical27_errors(dict(historical_mode_count=27,historical_modes=modes[:27],errors=h.get('errors')))
    last=modes[-1]
    for k,value in dict(mode='B22',findings_total=316,registry_used=SNAPSHOT,process_exit_code=0,
       validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=606,
       audit_checker_self_test_suite_count=23).items():
        if last.get(k)!=value or type(last.get(k))is not type(value):errors.append('B23 B22 OWN316/606/23:'+k)
    child=last.get('historical_B22_child')or{}
    for k,value in dict(tests_reported=40,expected_tests=40,process_exit_code=0,result='passed',
       historical_parser_cutoff='B22-not-current-B23-default',all_original_cases_executed_unmodified=True,
       dedicated_child_launcher='tools/run_historical_contract_item_tests_07B23.py',
       no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True).items():
        if child.get(k)!=value or type(child.get(k))is not type(value):errors.append('B23 B22 ALL40 explicit child:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(last.get(k))is not int or last[k]!=0:errors.append('B23 no historical ERP/SQL run')
    if not isinstance(last.get('stdout_sha256'),str)or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256'])is None:
        errors.append('B23 historical stdout identity')
    return errors

def validate_source(v,row,scope):
    if'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B23 undeclared documentary sentinel:'+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B23 fabricated source for documentary gate:'+row['id'])
        v.evidence(row['evidence'],row['id'])
        try:expanded=expanded_source_evidence(row['evidence'])
        except ValueError as exc:v.check(False,'B23 invalid scoped source '+row['id']+':'+str(exc));return
        v.scoped_evidence(expanded,scope,row['id']+' boundedB23',phase=7)

def extend_item_ingress(v,report,prov,frozen316):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[316:]
    for error in registry_preservation_errors(frozen316,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id']for r in current})==319,'B23 distinct319 IDs')
    ck(rows('evidence/historical-extensions-07B23.csv')==[],'B23 zero historical extensions')
    v.distributions(new,dict(Medium=3),dict(potential=1,confirmed=2),'B23 only')
    ck([r['certainty']for r in new]==['potential','confirmed','confirmed'],'B23 selection145 remains potential, source146/147 confirmed')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B23 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B23 exact heading/registry')
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):
        ck(prov[k]is False,'B23 no implicit start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch']is True,'B23 no repair-to-audit merge')
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        ck(type(prov[k])is int and prov[k]==0,'B23 no ERP/SQL:'+k)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected}
    original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==12,'B23 twelve bounded scope paths')
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-item-picker-batch-import-hydration-slices-not-runtime-certified'
           and bool(r['focus']),'B23 scope identity/depth');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B23-{n:02d}'for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B23.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B23 incompleteCSV:'+r['id']);validate_source(v,r,scope)
            if'runtime_status'in r:ck(r['runtime_status']=='not-executed','B23 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B23-','INV7B23-','P7B23T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['SB7B23-'],tables['IM7B23-']):ck(False,error)
    ck(fe[0]['status']=='potential-contract-dependent','B23 no145 policy certainty invented')
    v.proposed_tests(tests,'7B23');fids,iids,tids=[{r['id']for r in pool}for pool in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids')
    v.related(tables['SB7B23-']+tables['IM7B23-'],fids,'feature_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B23 '+label)
    for r in tables['RC7B23-']:
        fs=[f for f in fe if f['id']in r['feature_ids'].split(';')]
        unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        evidence=';'.join(dict.fromkeys(x for f in fs if f['evidence']!=DOCUMENTARY for x in f['evidence'].split(';')))or DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==evidence,'B23 exact RC source/FE lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in(residual_errors(tables['RS7B23-'],rows('evidence/residual-disposition-07B22.csv'))+
       split_errors(tables['SP7B23-'],rows('evidence/split-register-07B22.csv'))+remaining_work_errors(tables['RW7B23-'])):ck(False,error)
    hids={r['id']for r in tables['H7B23-']};sids={r['id']for r in tables['SP7B23-']}
    v.related(tables['RS7B23-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B23-'],hids,'handoff_ids')
    for r in tables['H7B23-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B23 no invented approval')
    for r in tables['Q7B23-']:ck(r['status']=='unanswered-no-secrets-requested','B23 no invented policy answer')
    for n,r in enumerate(tables['BK7B23-'],1):
        ck(r['prior_backlog_id']==f'BK7B22-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B23 backlog ancestry/uncompleted')
    ck([r['status']for r in tables['BK7B23-'][2:6]]==['not-started']*4,'B23 C axes remain unstarted')
    ad=tables['AD7B23-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B23 onlythree adjudicated causes')
    ck(ad[3]['current_root_ids']=='P7-143'and ad[3]['decision']=='same-cause-homologues-not-extended-or-recounted','B23 no143 recount/extension')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B23 adjudication source chain')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B23 honest dedup depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv'for n in range(2,8)]+[f'review-scope-07B{n}.csv'for n in range(1,23)]
    before={r['path']for name in prior_names for r in rows(name)};paths=set(scope)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),
       complement=len(original.keys()-(before|paths)),complement_kinds=dict(collections.Counter(original[p]['kind']for p in original.keys()-(before|paths))))
    ck(bk==dict(selected_paths=12,prior_union=416,overlap=10,new=2,union=418,complement=409,
       complement_kinds={'source':344,'generated-artifact':61,'project-or-resource':4}),'B23 scope not completion percent')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B23.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B22.md','evidence/split-register-07B22.csv','evidence/residual-disposition-07B22.csv']
       and decision['selected_upstream_split']=='SP7B22-01'and decision['entry']==ENTRY and decision['bookkeeping']==bk,'B23 authority/reasoned scope')
    ck(set(decision['new_paths'])==paths-before and decision['historical_metadata_screen_count']==316
       and decision['historical_body_review_claim']is False,'B23 scope/depth provenance')
    for k in('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k]is False,'B23 scope permission/count boundary')
    ck(v.sha(v.AUDIT/'evidence/item-ingress-witnesses-07B23.json')==WITNESS_SHA,'B23 actual witness stdout')
    witness,match=v.recompute('evidence/item-ingress-witnesses-07B23.json','tools/check_item_ingress_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B23 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B23-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B23-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,12);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B23 witness not runtime/policy acceptance')
            validate_source(v,r,scope)
    reads=witness['bounded_source_reads_not_semantic_coverage']
    ck(len(reads)==29 and{r['path']for r in reads}==paths,'B23 actual29 bounded reads12 paths')
    for r in reads:v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B23 lexical read',phase=7)
    discovery=witness['constructor_discovery'];tokens=discovery['exact_new_MsgExistItem_tokens']
    ck(discovery['source_csharp_paths_lexically_scanned']==477 and len(tokens)==11 and len({r['path']for r in tokens})==7
       and len(discovery['strict_utf8_fallback_cp1256_paths_not_compiler_acceptance'])==4
       and discovery['not_complete_callgraph_or_runtime_reachability']is True and discovery['scanned_bodies_not_reviewed']is True,
       'B23 literal discovery/encoding not body coverage')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,error)
    pending=False
    source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B23.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B23 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:
        ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B23.md','PHASE-07-REMAINING-07B23.md','7B24','غير مأذونة','3276579','10ba215')),
           'B23 shared index current boundary:'+name)
    hist_path='evidence/historical-mode-verification-07B23.json'
    ck(HISTORICAL_RUN_SHA is not None and(v.AUDIT/hist_path).is_file(),'B23 historical28 genuinely captured')
    if(v.AUDIT/hist_path).is_file():
        ck(v.sha(v.AUDIT/hist_path)==HISTORICAL_RUN_SHA,'B23 actual historical28 identities')
        historical=v.json.loads(v.read(v.AUDIT/hist_path))
        for error in historical_record_errors(historical):ck(False,error)
        ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD and historical['branch']==v.BRANCH,'B23 historical source/entry/capture')
        report['phase_7B23_executed_historical_documentary_modes']=dict(record=hist_path,sha256=HISTORICAL_RUN_SHA,modes_reported=28,
           all_documentary_exit_codes_zero=True,B22_OWN316_raw317CRLF_and_historical40_child=True,
           null_means_aggregate_not_reported_not_zero=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_item_ingress_witnesses.py','validate_item_ingress_part.py','run_historical_contract_item_tests_07B23.py','test_item_ingress_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:ck(False,'B23 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=55)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None
    passed=run.returncode==0 and count==44
    ck(passed,'B23 44 documentary self-tests/count: '+(run.stderr[-4000:]if not passed else''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=44,
       process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n)for n in['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B23-319-bounded-R4g-item-ingress-not-7B-or-runtime-closure',
       phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,24))+'-partial-not-complete7B-or7',
       phase_7_remaining_parts=['7B24-proposed-R4h-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],
       registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=147,phase_7B23=3,total_open_not_remediated=319,
       severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:12,'phase_7B23_prior_union':416,'phase_7B23_overlap_with_prior_union':10,'phase_7B23_new_paths':2,
       'unique_union_not_line_or_execution_coverage':418,'inventory_only_no_selected_scope':409})
    report['phase_7B22_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,
       frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=643,historical_check_record_overwritten=False,
       genuine_b22_stdout_sha256_unchanged=B22_CHECK_SHA,partial7B23_append_only_extensions=[],
       all316_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B23_item_ingress_trace_limits']=dict(selected_selection_batch_boundaries=8,selected_import_field_boundaries=8,
       source_csharp_paths_lexically_scanned_not_bodies=477,exact_new_MsgExistItem_tokens=11,token_source_paths=7,
       strict_utf8_fallback_cp1256_paths_not_compiler_acceptance=4,selected_paths_are_bounded_slices=12,
       current_features_or_documentary_contracts=18,invariants_not_executed_tests=18,acceptance_plans_not_executed=36,
       residual_inputs=14,explicit_further_static_splits=3,B_R4g_delivered_not_whole_R4_SP01_or7B_closure=True,
       retained_potential_roots_not_promoted=['P4-014','P7-132'],current145_potential_pending_selection_contract=True,
       prior143_homologues_not_recounted_or_extended=True,prior144_not_recounted_or_extended=True,
       basket_unit_conversion_price_priority_duplicate_or_SDK_policy_invented=False,
       C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synced_not_asserted=True)
    report['evidence_rows'].update(phase_7B23_illustrations_not_erp_tests=12,phase_7B23_lexical_checks_not_erp_tests=12,
       phase_7B23_bounded_source_reads_not_semantic_coverage=29,phase_7B23_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=(
       'Read-only bounded7B23/R4g:643 protected artifacts/316 EXACT dictionaries and ALLnext_phase/evidence/raw317CRLFprefix/G205/827 originals/three freezes. '
       '145 Medium potential: picker accumulates ever-selected IDs without deselection reconciliation; final-selection versus intentional cumulative basket contract unresolved. '
       '146 Medium confirmed source-local: sales foreach retains cursor on last appended row; next distinct successful lookup removes that nonempty row before append. '
       '147 Medium confirmed source-local: two selected importers populate seed description/unit/quantity/positivePrice then successful unique Code->ID lookup removes seed, '
       'constructs a fresh row without those fields and hydrates defaults. No duplicate/143 or code+last-index projection144 needed. rdAuto off and successful active unique lookups '
       'with normal returns are supplied assumptions, not SQL/WPF/Excel execution, policy or persisted loss. Equal-default/single/cancel controls limit claims, not acceptance. '
       '143 reversed1/2 homologues in two selected consumers not recounted or extended;142/026 and034/035/136..144 unchanged. No basket/price/conversion/merge/SDK policy invented. '
       'SB8/IM8,29 bounded text reads,477 lexical scans/11 literal MsgExistItem constructors across7 paths/four strictUTF8->cp1256 read-only fallbacks are not body reviews/allcallgraph/capability census/compiler encoding approval. '
       '12slice paths/10overlap/2new->418/complement409 not percentage or409 C tasks;455 historicalFE not rereviewed;316 registry metadata summaries plus selected nearest bodies/chains not all316 bodies. '
       '18FE/INV36 acceptance plans NOT executed;14 residuals/3splits/HQ6 retain all ancestry/input/route/disposition, not14 external approvals. R4h/B24 proposed;7B/7 partial;7C unstarted;8 unauthorized. '
       'B22 OWN316/raw317CRLF/indexes and ALL40 protected cases in explicit historical presetB22 child with local suite A path; B21/36,B20/32,B19/36,B18/28 unchanged. '
       'Actual current B23 CLI/parser/entrypoint tested independently44 cases; API main defaultB15 retained. No protected edits/skips/globalPath or shared subprocess mutation/disk overlay/rebaseline/archive rewrite. '
       'Source10ba/completedB22push-entry3276579/genuineB22stdoutcaptureb1f9524 distinct. Actual28 historical captures retain capture-time tools, not a claim of final-wholesale/postpush replay. '
       'B10 additive10vs120/equality1=10/G138 retained.014/132 potential and020/021 financial/ACL/stock/save/production barriers remain. '
       'No application import/build/C#/VB/.NET/WPF/SQL/provider/SDK/UtilitiesProj/ToDataTable/REPX/scanner/printer/business data/secrets/remediation/operational measurement/acceptance. '
       'Independent repairs are a separate branch/conversation, not assumed started/synchronized; no repair-to-audit merge. next_phase8 planning not permission.')
