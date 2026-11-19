#!/usr/bin/env python3
"""Read-only B24/R4h documentary guards, NEVER application acceptance.

Protect673 artifacts/all319 dictionaries, ALLnext_phase/evidence/raw320CRLF/
G210/827 originals/three entry freezes. ALL44 protected B23 cases run with
OWN319 and explicit presetB23 in an isolated child with suite-local A path.
No protected edits/skips/global Path/shared subprocess mutation/disk overlay.
148 cancel cleanup without seed ownership,149 wrong last-row identity before
hydration,150 old foundIndex after removal; confirmed source-local on supplied
inputs, not WPF/SQL or saved results.143/146 traces not recounted/extended;
144/145/147 and financial/ACL/stock/save/production barriers remain.7B/7
partial,R4i/B25 proposed,7C unstarted,8 unauthorized on this audit path.
Independent repairs never merged or presumed synchronized here.
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
from validate_item_ingress_part import historical_record_errors as historical28_errors

ENTRY='f37c37ca6581c4d1546bf0e073326572f4b7af36'
SNAPSHOT='evidence/findings-through-07B23.csv'
SNAPSHOT_SHA='e26c66b1d3008512aa230d8bc56bd8e02073622355a17e369ec9f368725f3dcb'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B23.json'
SHARED_SHA='6e7378bd4b3184b87ac08fb6072c4907a324f23b03fa58ff56a509259ec911f4'
PROVENANCE_SHA='4c5e1be172c4c0009bb88dfe560c11473082b4740e955752c16af748725af79c'
B23_CHECK_SHA='48ed3dfb7ef48a4f07cb054f1cfb50c7ab47f45fc08e9b4517e32f493034a056'
WITNESS_SHA='6397c680ab8419cd1b9129d2efc57c62d29c2d2d4127bce724655bf09fb3679e'
HISTORICAL_RUN_SHA='47dc6b0f7704f4b98a7dd71f4c0588f68cb497159941a5a1bbf6b488c50eceb4'  # Actual29 OWN captures; capture-time tools retained, archive never regenerated.
SCOPE_FILE='review-scope-07B24.csv'
DOCUMENTARY='none-documentary-metadata'
NEW_IDS=['P7-148','P7-149','P7-150']
PART_DOCS=('PHASE-07B24.md','ROW-OWNERSHIP-CONTRACTS-07B24.md','VALIDATION-07B24.md','PHASE-07-REMAINING-07B24.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS=(('row-ownership-lineage','RO7B24-',10),('repeat-outcome-lineage','DO7B24-',8),
 ('feature-implementation-matrix','FE7B24-',18),('report-invariants','INV7B24-',18),
 ('acceptance-tests','P7B24T-',36),('report-reconciliation','RC7B24-',6),
 ('root-adjudication','AD7B24-',10),('residual-disposition','RS7B24-',14),
 ('split-register','SP7B24-',3),('handoffs','H7B24-',6),('questions','Q7B24-',6),
 ('remaining-workplan','RW7B24-',10),('continuation-backlog','BK7B24-',10))
SENTINELS={f'{p}{n:02d}'for p,ns in(
 ('FE7B24-',range(16,19)),('INV7B24-',range(16,19)),('P7B24T-',range(31,37)),
 ('RC7B24-',(6,)),('AD7B24-',(9,10)),('RS7B24-',range(1,15)),
 ('H7B24-',range(1,7)),('Q7B24-',range(1,7)))for n in ns}
OWNERSHIP_BOUNDARIES=['entry-context','selected-reference','picker-cancel','invalid-confirmation','last-row-target',
 'existing-increment','index-shift','out-of-range-control','stored-aggregate','property-notification']
OUTCOME_BOUNDARIES=['wire-map','active-lookup','purchase-wire2','purchase-wire1','duplicate-cancel',
 'initial-hidden-wire','production-control','batch-and-failure-limits']
DEDUP_DEPTH='all319-title-certainty-summaries-plus-path-filtered-metadata-and-selected-nearest-bodies-source-chains-not-all-historical-bodies'

@contextmanager
def historical_b23_inputs(v,frozen319,texts,raw):
    """Context-local exact OWN319 path; never mutate pathlib/globals/disk."""
    if len(frozen319)!=319 or len({r.get('id')for r in frozen319})!=319:raise ValueError('Exactly319 distinct B23 OWN rows required')
    if set(texts)!=set(SHARED_DOCS) or any(not isinstance(s,str)for s in texts.values()):raise ValueError('Exactly three frozen shared texts required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):raise ValueError('Exact frozen noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except(UnicodeError,csv.Error)as exc:raise ValueError('Malformed319 frozen registry')from exc
    if parsed!=frozen319 or raw.count(b'\r\n')!=320 or not raw.endswith(b'\r\n') or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n')):
        raise ValueError('319 rows/raw320CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):return raw if self.resolve()==target else super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            if self.resolve()==target:return io.StringIO(raw.decode(encoding or'utf-8',errors or'strict'),newline=None).read()
            return super().read_text(encoding=encoding,errors=errors)
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen319,texts):yield
    finally:v.AUDIT=original

class HistoricalB23Subprocess:
    """Exact B23 suite argv only; unrelated subprocess calls remain identical."""
    def __init__(self,backend,python,tool_dir):
        self.backend=backend
        self.expected=[python,'-B',str(tool_dir/'test_item_ingress_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_item_ingress_tests_07B24.py'),'--through-part','B23']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)

class HistoricalB23ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB23Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess'else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)

@contextmanager
def historical_b23_validation(v,report,prior,prov,frozen319):
    ck=v.check
    for name,digest in(('evidence/provenance-07B24.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),
      (SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B23.json',B23_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B24 immutable entry:'+name)
    ck(prov['historical_artifact_count']==673 and len(frozen319)==319,'B24 entry673/319')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
       and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B24 entry freeze identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B24 protected643-to673 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B23.json'));suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='3276579931925bff37bbf45c5b43efb7fbcd0118'
       and old['findings']['total_open_not_remediated']==319 and old['original_project_hashes_matching']==827
       and old['validation']['errors']==[]and old['validation']['current_output_record_pending_first_write_not_placeholder']is False,
       'B24 genuine B23 capture3276579, not completed entryf37c37c')
    ck(len(suites)==24 and sum(s['tests_reported']for s in suites.values())==650
       and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B24 genuine B23 actual650/24/643')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY
       and prov['genuine_B23_check_sha256']==B23_CHECK_SHA and prov['genuine_B23_check_record_checkout']==old['checkout_head'],'B24 completed pushed B23 entry identity')
    ck(prov['phase7B23_entry_consistency']==dict(original_hashes_matching=827,findings=319,audit_file_count=678,
       documentary_cases=650,self_test_suites=24,errors=[],erp_runtime_tests_executed=0),'B24 independently checked entry consistency')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB23ValidatorView(v)
    with historical_b23_inputs(view,frozen319,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_item_ingress_audit_validator.py']
    record.update(historical_parser_cutoff='B23-not-current-B24-default',all_original_cases_executed_unmodified=True,
       dedicated_child_launcher='tools/run_historical_item_ingress_tests_07B24.py',actual_subprocess_argv=view.subprocess.actual,
       no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B23-319-not-current-state',
       phase_7B23_historical_input_mode='OWN319-exact320CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B23-test-child',
       phase_7B23_adapter_context=dict(entry_provenance='evidence/provenance-07B24.json',adapter_protected_artifacts_checked=673,
         current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
         B23_parser_assertions_are_historical_preset_not_current_default=True,B23_suite_own_A_uses_context_local_registry_path=True))

def registry_preservation_errors(previous,current,raw,frozen):
    errors=[]
    if len(previous)!=319 or current[:319]!=previous:errors.append('B24 all319 exact fields/ALLnext_phase/evidence')
    if len(current)!=322 or[r.get('id')for r in current[319:]]!=NEW_IDS:errors.append('B24 only appended148..150')
    if type(raw)is not bytes or type(frozen)is not bytes or not raw.startswith(frozen) or raw.startswith(b'\xef\xbb\xbf')or raw.count(b'\r\n')!=323 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n')):
        errors.append('B24 exact319 raw prefix/323CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B24 raw/row mismatch')
        except(UnicodeError,csv.Error):errors.append('B24 malformed registry')
    return errors

def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=210 or rows(current)[:210]!=rows(previous):return['B24 G01..210 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{n:02d}'for n in range(1,216)]:return['B24 G211..215 only exact order']
    return[]

def ledger_errors(ownership,outcome):
    errors=[]
    for data,names,label in((ownership,OWNERSHIP_BOUNDARIES,'ownership'),(outcome,OUTCOME_BOUNDARIES,'outcome')):
        if len(data)!=len(names)or[r.get('boundary')for r in data]!=names:errors.append('B24 ordered boundaries:'+label)
        for r in data:
            for k in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(r.get(k),str)or not r[k].strip():errors.append('B24 '+label+' responsibility:'+k)
            if r.get('runtime_status')!='not-executed':errors.append('B24 '+label+' runtime overclaim')
    for data,expected in((ownership,{2:'in-range-cleanup-without-seed-ownership',4:'unrelated-last-reference-mutated-no-add',6:'old-index-after-removal-not-rebased',7:'guarded-missed-recalc-not-asserted-exception'}),
       (outcome,{0:'same143-reversal-not-recounted',2:'target149-independent-of-button-labels143',3:'recalc150-independent-of-last-target149',5:'same143-hidden-wire-not-user-click',7:'same146-batch-and-unmodelled-failure-not-new-roots'})):
        if len(data)in (8,10)and any(data[i].get('observation')!=s for i,s in expected.items()):errors.append('B24 root/guard/homologue boundaries')
    return errors

def current_link_errors(features,invariants,tests):
    errors=[]
    if(len(features),len(invariants),len(tests))!=(18,18,36):errors.append('B24 FE18/INV18/T36')
    for n,(fe,inv)in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):errors.append('B24 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or';'.join(t['id']for t in related)!=fe.get('acceptance_ids'):errors.append('B24 two reverse-linked plans per capability')
        if n<=3 and(fe.get('finding_ids')!=NEW_IDS[n-1]or any(t.get('plan_kind')!='finding-specific'or t.get('finding_ids')!=NEW_IDS[n-1]for t in related)):errors.append('B24 three distinct finding-specific plans')
        for k in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(fe.get(k),str)or not fe[k].strip():errors.append('B24 capability responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=18 or len({r.get('acceptance_criterion')for r in tests})!=36:errors.append('B24 distinct substantive invariants/criteria')
    if any(r.get('status')!='not-executed'for r in tests):errors.append('B24 acceptance never executed')
    return errors

def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return['B24 all14 exact upstream residuals required']
    errors=[]
    for old,new in zip(upstream,current):
        if new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B23.csv'or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids'):errors.append('B24 upstream residual identity/hash/contracts')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B24 residual responsibility:'+k)
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B24 no lost old required input')
        mapped={x.replace('7B23-','7B24-')for x in old.get('current_handoff_or_split_ids','').split(';')if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B24 no lost mapped route')
        if new.get('disposition')!=old.get('disposition')or new.get('disposition')not in {'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':errors.append('B24 no residual approval/runtime overclaim')
    return errors

def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return['B24 exactlythree upstream static splits']
    errors=[]
    for old,new in zip(upstream,current):
        if new.get('upstream_split_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/split-register-07B23.csv'or new.get('upstream_row_sha256')!=row_sha(old)or not new.get('required_input','').startswith(old.get('required_input','')):errors.append('B24 split ancestry/no lost input')
        for k in('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B24 reasoned split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started'or new.get('runtime_status')!='not-executed':errors.append('B24 split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work)!=10:return['B24 four B packages/six C axes']
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4h-row-ownership-delivered-residuals-open']+['planned-not-started']*6
    errors=[]
    if[r.get('status')for r in work]!=expected or[r.get('part_family')for r in work]!=['7B']*4+['7C']*6:errors.append('B24 boundedR4h/six C unstarted not closure')
    if any(r.get('runtime_status')!='not-executed'or r.get('counts_are_sessions_or_completion_percent')!='false'for r in work):errors.append('B24 no runtime/sessions/percent overclaim')
    return errors

def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','dotnet_wpf_sql_or_excel_executed','phase7C_started','phase8_authorized_or_started','application_remediation_performed','all477_sources_or_all11_constructors_body_reviewed','financial_price_unit_merge_or_basket_policy_invented'):
        if w.get(k)is not False:errors.append('B24 false-only boundary:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B24 integer-zero boundary:'+k)
    for k in('B_R4h_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained','selected_paths_strict_utf8_decode','historical143_and146_not_recounted_or_extended'):
        if w.get(k)is not True:errors.append('B24 true-only boundary:'+k)
    for k,n in(('illustration_count',14),('lexical_check_count',14),('selected_source_paths',10),('selected_repeat_consumers',3)):
        if type(w.get(k))is not int or w[k]!=n:errors.append('B24 exact witness count:'+k)
    err=w.get('retained_additive_B10_arithmetic_erratum',{})
    if err!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)or any(type(err.get(k))is not int for k in('local_cost','reference_cost','equality1_control'))or err.get('protected_G138_not_rewritten')is not True:errors.append('B24 B10 additive10vs120/equality1=10/G138 retained')
    return errors

def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count'))is not int or h['historical_mode_count']!=29 or len(modes)!=29:return['B24 exactly29 actual OWN modes required']
    errors=historical28_errors(dict(historical_mode_count=28,historical_modes=modes[:28],errors=h.get('errors')))
    last=modes[-1]
    for k,value in dict(mode='B23',findings_total=319,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=650,audit_checker_self_test_suite_count=24).items():
        if last.get(k)!=value or type(last.get(k))is not type(value):errors.append('B24 B23 OWN319/650/24:'+k)
    child=last.get('historical_B23_child')or{}
    for k,value in dict(tests_reported=44,expected_tests=44,process_exit_code=0,result='passed',historical_parser_cutoff='B23-not-current-B24-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_item_ingress_tests_07B24.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True).items():
        if child.get(k)!=value or type(child.get(k))is not type(value):errors.append('B24 B23 ALL44 explicit child:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(last.get(k))is not int or last[k]!=0:errors.append('B24 no historical ERP/SQL')
    if not isinstance(last.get('stdout_sha256'),str)or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256'])is None:errors.append('B24 historical stdout identity')
    return errors

def validate_source(v,row,scope):
    if'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B24 undeclared documentary sentinel:'+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B24 fabricated source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
        try:expanded=expanded_source_evidence(row['evidence'])
        except ValueError as exc:v.check(False,'B24 invalid scoped source '+row['id']+':'+str(exc));return
        v.scoped_evidence(expanded,scope,row['id']+' boundedB24',phase=7)

def extend_row_ownership(v,report,prov,frozen319):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[319:]
    for error in registry_preservation_errors(frozen319,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id']for r in current})==322,'B24 distinct322 IDs');ck(rows('evidence/historical-extensions-07B24.csv')==[],'B24 zero historical extensions')
    v.distributions(new,dict(Medium=3),dict(confirmed=3),'B24 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B24 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B24 exact heading/registry')
    lookup={r['id']:r for r in current}
    for n in('P4-014','P7-132','P7-145'):ck(lookup[n]['certainty']=='potential','B24 retained potential:'+n)
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k]is False,'B24 no implicit start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch']is True,'B24 no repair-to-audit merge')
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k])is int and prov[k]==0,'B24 no ERP/SQL:'+k)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==10,'B24 ten bounded source paths')
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-row-ownership-repeat-recalculation-slices-not-runtime-certified'and bool(r['focus']),'B24 scope identity/depth');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B24-{n:02d}'for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B24.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B24 incompleteCSV:'+r['id']);validate_source(v,r,scope)
            if'runtime_status'in r:ck(r['runtime_status']=='not-executed','B24 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B24-','INV7B24-','P7B24T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['RO7B24-'],tables['DO7B24-']):ck(False,error)
    ck(all(f['status']=='confirmed-source-local'for f in fe[:3]),'B24 three source-local causes not ERP')
    v.proposed_tests(tests,'7B24');fids,iids,tids=[{r['id']for r in pool}for pool in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['RO7B24-']+tables['DO7B24-'],fids,'feature_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B24 '+label)
    for r in tables['RC7B24-']:
        fs=[f for f in fe if f['id']in r['feature_ids'].split(';')]
        unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        evidence=';'.join(dict.fromkeys(x for f in fs if f['evidence']!=DOCUMENTARY for x in f['evidence'].split(';')))or DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==evidence,'B24 exact RC source/FE lineage');v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B24-'],rows('evidence/residual-disposition-07B23.csv'))+split_errors(tables['SP7B24-'],rows('evidence/split-register-07B23.csv'))+remaining_work_errors(tables['RW7B24-']):ck(False,error)
    hids={r['id']for r in tables['H7B24-']};sids={r['id']for r in tables['SP7B24-']};v.related(tables['RS7B24-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B24-'],hids,'handoff_ids')
    for r in tables['H7B24-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B24 no invented approval')
    for r in tables['Q7B24-']:ck(r['status']=='unanswered-no-secrets-requested','B24 no invented policy answer')
    for n,r in enumerate(tables['BK7B24-'],1):ck(r['prior_backlog_id']==f'BK7B23-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B24 backlog ancestry/uncompleted')
    ck([r['status']for r in tables['BK7B24-'][2:6]]==['not-started']*4,'B24 C axes unstarted')
    ad=tables['AD7B24-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B24 onlythree new adjudicated roots')
    ck([r['current_root_ids']for r in ad if r['decision']=='same-cause-homologues-not-extended-or-recounted']==['P7-143','P7-146'],'B24 no143/146 recount or extension')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B24 adjudication source chain')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B24 honest comparison depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv'for n in range(2,8)]+[f'review-scope-07B{n}.csv'for n in range(1,24)]
    before={r['path']for n in prior_names for r in rows(n)};paths=set(scope)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(original.keys()-(before|paths)),complement_kinds=dict(collections.Counter(original[p]['kind']for p in original.keys()-(before|paths))))
    ck(bk==dict(selected_paths=10,prior_union=418,overlap=9,new=1,union=419,complement=408,complement_kinds={'source':343,'generated-artifact':61,'project-or-resource':4}),'B24 scope not completion percent')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B24.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B23.md','evidence/split-register-07B23.csv','evidence/residual-disposition-07B23.csv']and decision['selected_upstream_split']=='SP7B23-01'and decision['entry']==ENTRY and decision['bookkeeping']==bk,'B24 authority/reasoned scope')
    ck(set(decision['new_paths'])==paths-before and decision['historical_metadata_screen_count']==319 and decision['historical_body_review_claim']is False and decision['historical_comparison_depth']==DEDUP_DEPTH,'B24 scope/comparison depth')
    for k in('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k]is False,'B24 scope permission/count boundary')
    ck(v.sha(v.AUDIT/'evidence/row-ownership-witnesses-07B24.json')==WITNESS_SHA,'B24 actual witness stdout')
    witness,match=v.recompute('evidence/row-ownership-witnesses-07B24.json','tools/check_row_ownership_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B24 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B24-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B24-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,14);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B24 witness not runtime/policy acceptance');validate_source(v,r,scope)
    reads=witness['bounded_source_reads_not_semantic_coverage'];ck(len(reads)==34 and{r['path']for r in reads}==paths,'B24 actual34 bounded reads10paths')
    for r in reads:
        ck(r['encoding']=='strict-utf-8'and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review']is True,'B24 bounded reads not body certification');v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B24 lexical read',phase=7)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,error)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B24.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B24 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B24.md','PHASE-07-REMAINING-07B24.md','7B25','غير مأذونة','f37c37c','10ba215')),'B24 shared index current boundary:'+name)
    hist_path='evidence/historical-mode-verification-07B24.json';ck(HISTORICAL_RUN_SHA is not None and(v.AUDIT/hist_path).is_file(),'B24 genuine29 captured')
    if(v.AUDIT/hist_path).is_file():
        ck(v.sha(v.AUDIT/hist_path)==HISTORICAL_RUN_SHA,'B24 actual historical29 identity');historical=v.json.loads(v.read(v.AUDIT/hist_path))
        for error in historical_record_errors(historical):ck(False,error)
        ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD and historical['branch']==v.BRANCH,'B24 historical source/entry/capture')
        report['phase_7B24_executed_historical_documentary_modes']=dict(record=hist_path,sha256=HISTORICAL_RUN_SHA,modes_reported=29,all_documentary_exit_codes_zero=True,B23_OWN319_raw320CRLF_and_historical44_child=True,null_means_aggregate_not_reported_not_zero=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_row_ownership_witnesses.py','validate_row_ownership_part.py','run_historical_item_ingress_tests_07B24.py','test_row_ownership_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:ck(False,'B24 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None;passed=run.returncode==0 and count==44
    ck(passed,'B24 44 documentary self-tests/count: '+(run.stderr[-5000:]if not passed else''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=44,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n)for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B24-322-bounded-R4h-row-ownership-not-7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,25))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B25-proposed-R4i-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=150,phase_7B24=3,total_open_not_remediated=322,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:10,'phase_7B24_prior_union':418,'phase_7B24_overlap_with_prior_union':9,'phase_7B24_new_paths':1,'unique_union_not_line_or_execution_coverage':419,'inventory_only_no_selected_scope':408})
    report['phase_7B23_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=673,historical_check_record_overwritten=False,genuine_b23_stdout_sha256_unchanged=B23_CHECK_SHA,partial7B24_append_only_extensions=[],all319_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B24_row_ownership_trace_limits']=dict(selected_row_ownership_boundaries=10,selected_repeat_outcome_boundaries=8,selected_repeat_consumers_not_census=3,selected_paths_are_bounded_slices=10,all477_sources_or_all11_dialog_constructors_body_reviewed=False,current_features_or_documentary_contracts=18,invariants_not_executed_tests=18,acceptance_plans_not_executed=36,residual_inputs=14,explicit_further_static_splits=3,B_R4h_delivered_not_whole_R4_SP01_or7B_closure=True,retained_potential_roots_not_promoted=['P4-014','P7-132','P7-145'],prior143_and146_homologues_not_recounted_or_extended=True,prior144_and147_not_recounted_or_extended=True,basket_unit_conversion_price_merge_or_SDK_policy_invented=False,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synced_not_asserted=True)
    report['evidence_rows'].update(phase_7B24_illustrations_not_erp_tests=14,phase_7B24_lexical_checks_not_erp_tests=14,phase_7B24_bounded_source_reads_not_semantic_coverage=34,phase_7B24_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=(
      'Read-only bounded7B24/R4h:673 protected artifacts/319 EXACT dictionaries and ALLnext_phase/evidence/raw320CRLFprefix/G210/827 originals/three freezes. '
      '148 Medium confirmed source-local: picker false/invalid cleanup removes any in-range current row without owned-seed test.149 Medium confirmed source-local: duplicate wire2 sets Count-1 and writes identity into unrelated last row without Add; proof before hydration, one duplicate sufficient. '
      '150 Medium confirmed source-local: wire1 increments existing quantity then removes earlier row but calls CalcRowValues(oldfoundIndex), recalculating the following row or guarded null; no thrown exception asserted. '
      'Supplied stable current row, normal return/active unique successful lookup and flat ratio1/noVAT/nodiscount integer40vs50 examples are not WPF/SQL/Excel/.NET formatting/tax/pricing/merge acceptance or saved/printed loss. '
      '143 reversed1/2 including hidden initial-account wire and production/Purch consumers,146 shared-cursor batch homologue not recounted or extended.144/145/147 and034/035/136..142 unchanged;145/014/132 remain potential,020/021 and financial/ACL/stock/save/production barriers retained. '
      'RO10/DO8,34 bounded text reads across10 paths and3 selected repeat consumers are not all11 constructor bodies/all477 sources/allcallgraph/capability census or455 historicalFE rereviews.319 title/certainty summaries plus path-filtered metadata and named nearest bodies/chains, not all319 bodies or all evidence paths manually rereviewed. '
      '10slice paths/9overlap/1new->419/complement408 not percentage or408 C tasks.18FE/INV36 acceptance plans NOT executed;14 residuals/3splits/HQ6 preserve all ancestry/input/route/disposition, not14 approvals. R4i/B25 proposed;7B/7 partial;7C unstarted;8 unauthorized here. '
      'B23 OWN319/raw320CRLF/indexes and ALL44 protected cases in explicit presetB23 child with suite-local A path;B22/40,B21/36,B20/32,B19/36,B18/28 unchanged. Actual current B24 CLI/parser/entrypoint independently tested44 cases;API main defaultB15 retained. '
      'No protected edits/skips/globalPath/shared subprocess mutation/disk overlay/rebaseline/archive rewrite. Source10ba/completedB23push-entryf37c37c/genuineB23stdoutcapture3276579 distinct. Actual29 captures retain capture-time tools, not final-wholesale/postpush replay. '
      'B10 additive10vs120/equality1=10/G138 retained. No application import/build/C#/VB/.NET/WPF/SQL/provider/SDK/UtilitiesProj/ToDataTable/REPX/scanner/printer/business data/secrets/remediation/operational measurement/acceptance. '
      'Independent repairs separate branch/conversation, not assumed started/synchronized;no repair-to-audit merge. next_phase8 planning not permission on this audit path.')
