#!/usr/bin/env python3
"""Read-only B25/R4i documentary guards; NEVER ERP or packing acceptance.

Preserve703 artifacts/all322 dictionaries/ALLnext_phase/evidence/raw323CRLF/
G215/827 originals/three freezes. ALL44 protected B24 cases use OWN322,
explicit presetB24 and suite-local A in an isolated child. No protected edit,
skip, global Path/shared subprocess mutation, disk overlay or archive rewrite.
151 ungated normal-return scalar projection;152 sequential packing feedback.
Whole local dialog pair does not certify all callers/SDK DTOs/event scheduling.
InvoiceDGV and Invoicecontract remain distinct; hidden/empty editor controls
limit reachability claims.16 capabilities/32 plans NOT executed.7B/7 partial,
R4j/B26 proposed,7C unstarted,8 unauthorized here; repairs independent.
"""
from __future__ import annotations
import collections
from contextlib import contextmanager
import csv
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,bidirectional_errors
from validate_contract_item_part import row_sha,expanded_source_evidence
from validate_row_ownership_part import historical_record_errors as historical29_errors

ENTRY='45a2a504db4f82927a286ce425f21a82bcee7a84'
SNAPSHOT='evidence/findings-through-07B24.csv'
SNAPSHOT_SHA='6fb3e1a7f9dfd0d4fcc9108c4cdc38ac548ba1aad5cd17f8dfc227d1b90574b2'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B24.json'
SHARED_SHA='c3cf3050fbb161ab773a474374ae410c8bb91967fe7e1621593d49bd478e4b47'
PROVENANCE_SHA='78dc1bf807369616d45aad68b7802ec85bffd21d6d976450c35e7f0f83e40631'
B24_CHECK_SHA='5866e39e46d6075ca186059bdf8d860f2d66c3330ac400859ae334fb3d80c69b'
WITNESS_SHA='1a47740eb84428c6bee3dadc1f34f08134b8996aa93b74254ea40f3cfd9d69a4'
HISTORICAL_RUN_SHA='42755c94a5b223159b93bcf38335366646cefd6fab777aaa7222f9e0066442d6'  # Actual30 OWN captures; preserve capture-time tool hashes, never regenerate archive.
SCOPE_FILE='review-scope-07B25.csv'
DOCUMENTARY='none-documentary-metadata'
NEW_IDS=['P7-151','P7-152']
PART_DOCS=('PHASE-07B25.md','PROPERTY-DIALOG-CONTRACTS-07B25.md','VALIDATION-07B25.md','PHASE-07-REMAINING-07B25.md','DATE-IDENTITY-NOTE-07B25.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
TABLE_SPECS=(('dialog-result-lineage','DG7B25-',8),('packing-calculation-lineage','PK7B25-',8),
 ('feature-implementation-matrix','FE7B25-',16),('report-invariants','INV7B25-',16),
 ('acceptance-tests','P7B25T-',32),('report-reconciliation','RC7B25-',4),
 ('root-adjudication','AD7B25-',8),('residual-disposition','RS7B25-',14),
 ('split-register','SP7B25-',3),('handoffs','H7B25-',6),('questions','Q7B25-',6),
 ('remaining-workplan','RW7B25-',10),('continuation-backlog','BK7B25-',10))
SENTINELS={f'{p}{n:02d}'for p,ns in(
 ('FE7B25-',range(15,17)),('INV7B25-',range(15,17)),('P7B25T-',range(29,33)),
 ('AD7B25-',(7,8)),('RS7B25-',range(1,15)),('H7B25-',range(1,7)),('Q7B25-',range(1,7)))for n in ns}
DIALOG_BOUNDARIES=['source-detail','fresh-result','nontrue-return','confirmed-control','append-boundary','sale-editor-gate','input-output-gate','overload-boundary']
PACKING_BOUNDARIES=['source-output-loop','sequential-calls','internal-update-guard','callback-sites','quantity-one-control','zero-controls','other-properties','ceiling-and-culture-limit']
DEDUP_DEPTH='all322-title-certainty-summaries-plus-path-filtered-metadata-and-selected-nearest-bodies-source-chains-not-all-historical-bodies'

@contextmanager
def historical_b24_inputs(v,frozen322,texts,raw):
    """Exact context-local OWN322 path, not a process-global pathlib patch."""
    if len(frozen322)!=322 or len({r.get('id')for r in frozen322})!=322:raise ValueError('Exactly322 distinct B24 OWN rows required')
    if set(texts)!=set(SHARED_DOCS)or any(not isinstance(s,str)for s in texts.values()):raise ValueError('Exactly three frozen shared texts required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):raise ValueError('Exact noBOM frozen bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except(UnicodeError,csv.Error)as exc:raise ValueError('Malformed322 frozen registry')from exc
    if parsed!=frozen322 or raw.count(b'\r\n')!=323 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n')):
        raise ValueError('322 rows/raw323CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):return raw if self.resolve()==target else super().read_bytes()
        def read_text(self,encoding=None,errors=None):
            if self.resolve()==target:return io.StringIO(raw.decode(encoding or'utf-8',errors or'strict'),newline=None).read()
            return super().read_text(encoding=encoding,errors=errors)
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen322,texts):yield
    finally:v.AUDIT=original

class HistoricalB24Subprocess:
    """Redirect ONLY exact B24 test-suite argv, preserving every other call."""
    def __init__(self,backend,python,tool_dir):
        self.backend=backend
        self.expected=[python,'-B',str(tool_dir/'test_row_ownership_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_row_ownership_tests_07B25.py'),'--through-part','B24']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)

class HistoricalB24ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB24Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess'else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)

@contextmanager
def historical_b24_validation(v,report,prior,prov,frozen322):
    ck=v.check
    for name,digest in(('evidence/provenance-07B25.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B24.json',B24_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B25 immutable entry:'+name)
    ck(prov['historical_artifact_count']==703 and len(frozen322)==322,'B25 entry703/322')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B25 frozen entry identities')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B25 protected673-to703 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B24.json'));suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='f37c37ca6581c4d1546bf0e073326572f4b7af36'and old['findings']['total_open_not_remediated']==322 and old['original_project_hashes_matching']==827 and old['validation']['errors']==[]and old['validation']['current_output_record_pending_first_write_not_placeholder']is False,'B25 genuine B24 capturef37c37c, not delivery-entry45a2a50')
    ck(len(suites)==25 and sum(s['tests_reported']for s in suites.values())==694 and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B25 genuine B24 actual694/25/673')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY and prov['genuine_B24_check_sha256']==B24_CHECK_SHA and prov['genuine_B24_check_record_checkout']==old['checkout_head'],'B25 completed pushed B24 entry identity')
    ck(prov['phase7B24_entry_consistency']==dict(original_hashes_matching=827,findings=322,audit_file_count=708,documentary_cases=694,self_test_suites=25,errors=[],erp_runtime_tests_executed=0),'B25 independent entry consistency')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB24ValidatorView(v)
    with historical_b24_inputs(view,frozen322,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_row_ownership_audit_validator.py']
    record.update(historical_parser_cutoff='B24-not-current-B25-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_row_ownership_tests_07B25.py',actual_subprocess_argv=view.subprocess.actual,no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B24-322-not-current-state',phase_7B24_historical_input_mode='OWN322-exact323CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B24-test-child',phase_7B24_adapter_context=dict(entry_provenance='evidence/provenance-07B25.json',adapter_protected_artifacts_checked=703,current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,B24_parser_assertions_are_historical_preset_not_current_default=True,B24_suite_own_A_uses_context_local_registry_path=True))

def registry_preservation_errors(previous,current,raw,frozen):
    errors=[]
    if len(previous)!=322 or current[:322]!=previous:errors.append('B25 all322 exact fields/ALLnext_phase/evidence')
    if len(current)!=324 or[r.get('id')for r in current[322:]]!=NEW_IDS:errors.append('B25 only appended151/152')
    if type(raw)is not bytes or type(frozen)is not bytes or not raw.startswith(frozen)or raw.startswith(b'\xef\xbb\xbf')or raw.count(b'\r\n')!=325 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n')):errors.append('B25 exact322 rawprefix/325CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B25 raw/rows disagree')
        except(UnicodeError,csv.Error):errors.append('B25 malformed registry')
    return errors

def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    if len(rows(previous))!=215 or rows(current)[:215]!=rows(previous):return['B25 G01..215 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{n:02d}'for n in range(1,220)]:return['B25 only G216..219 exact order']
    return[]

def ledger_errors(dialog,packing):
    errors=[]
    for data,names,label in((dialog,DIALOG_BOUNDARIES,'dialog'),(packing,PACKING_BOUNDARIES,'packing')):
        if len(data)!=8 or[r.get('boundary')for r in data]!=names:errors.append('B25 ordered boundaries:'+label)
        for row in data:
            for key in('source_to_output','observation','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit','feature_ids','finding_ids','evidence'):
                if not isinstance(row.get(key),str)or not row[key].strip():errors.append('B25 '+label+' responsibility:'+key)
            if row.get('runtime_status')!='not-executed':errors.append('B25 '+label+' runtime overclaim')
    for data,expected in((dialog,{2:'nontrue-normal-return-writes-zero',5:'hidden-default-no-unconditional-existing-row-reachability',6:'description-branch-not-asserted-reachable',7:'same151-helper-not-actual-contract-dialog-support'}),(packing,{0:'prior-output-reused-as-next-input',1:'integer-feedback-not-WPF-event-count',2:'nested-guard-not-sequential-idempotence',5:'explicit-zero-guard-not-thrown-divide-by-zero',7:'same152-ceiling-branch-not-new-policy-or-dotnet-oracle'})):
        if len(data)==8 and any(data[n].get('observation')!=value for n,value in expected.items()):errors.append('B25 root/reachability/guard limits')
    return errors

def source_evidence_union(features):
    """Expand each feature's shorthand BEFORE deduplication preserves its path.

    Deduplicating bare semicolon fragments can remove a repeated path-bearing
    fragment and silently attach the next bare range to a different source.
    Documentary gates do not contribute invented source locations.
    """
    references=[]
    for feature in features:
        evidence=feature['evidence']
        if evidence!=DOCUMENTARY:references.extend(expanded_source_evidence(evidence).split(';'))
    return ';'.join(dict.fromkeys(references))or DOCUMENTARY


def current_link_errors(features,invariants,tests):
    errors=[]
    if(len(features),len(invariants),len(tests))!=(16,16,32):errors.append('B25 FE16/INV16/T32')
    for n,(fe,inv)in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):errors.append('B25 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or';'.join(t['id']for t in related)!=fe.get('acceptance_ids'):errors.append('B25 two reverse-linked plans per capability')
        if n<=2 and(fe.get('finding_ids')!=NEW_IDS[n-1]or any(t.get('plan_kind')!='finding-specific'or t.get('finding_ids')!=NEW_IDS[n-1]for t in related)):errors.append('B25 two distinct finding-specific plans')
        for k in('owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(fe.get(k),str)or not fe[k].strip():errors.append('B25 capability responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=16 or len({r.get('acceptance_criterion')for r in tests})!=32:errors.append('B25 distinct substantive invariants/criteria')
    if any(r.get('status')!='not-executed'for r in tests):errors.append('B25 acceptance never executed')
    return errors

def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return['B25 all14 upstream residuals required']
    errors=[]
    for old,new in zip(upstream,current):
        if new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B24.csv'or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids'):errors.append('B25 residual ancestry/hash/contracts')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B25 residual responsibility:'+k)
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B25 no lost old input')
        mapped={x.replace('7B24-','7B25-')for x in old.get('current_handoff_or_split_ids','').split(';')if x}
        if not mapped<=set(new.get('current_handoff_or_split_ids','').split(';')):errors.append('B25 no lost mapped route')
        if new.get('disposition')!=old.get('disposition')or new.get('disposition')not in{'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':errors.append('B25 no residual approval/runtime overclaim')
    return errors

def split_errors(current,upstream):
    if len(current)!=3 or len(upstream)!=3:return['B25 exactlythree upstream splits']
    errors=[]
    for old,new in zip(upstream,current):
        if new.get('upstream_split_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/split-register-07B24.csv'or new.get('upstream_row_sha256')!=row_sha(old)or not new.get('required_input','').startswith(old.get('required_input','')):errors.append('B25 split ancestry/no lost input')
        for k in('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B25 split responsibility:'+k)
        if new.get('status')!='explicit-further-static-split-not-started'or new.get('runtime_status')!='not-executed':errors.append('B25 split not started/accepted')
    return errors

def remaining_work_errors(work):
    if len(work)!=10:return['B25 fourB/sixC axes']
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-R4i-property-dialog-delivered-residuals-open']+['planned-not-started']*6
    errors=[]
    if[r.get('status')for r in work]!=expected or[r.get('part_family')for r in work]!=['7B']*4+['7C']*6:errors.append('B25 boundedR4i/sixC unstarted not closure')
    if any(r.get('runtime_status')!='not-executed'or r.get('counts_are_sessions_or_completion_percent')!='false'for r in work):errors.append('B25 no runtime/sessions/percent overclaim')
    return errors

def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','dotnet_wpf_sql_or_excel_executed','application_remediation_performed','phase7C_started','phase8_authorized_or_started','all_callers_or_external_DTOs_body_reviewed','actual_WPF_event_order_or_count_claimed','financial_or_packing_policy_invented'):
        if w.get(k)is not False:errors.append('B25 false-only boundary:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed','scanner_or_printer_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B25 integer-zero boundary:'+k)
    for k in('B_R4i_bounded_not_whole7B_closure','unresolved_external_contracts_and_explicit_splits_retained','selected_paths_strict_utf8_decode','Invoicecontract_and_InvoiceDGV_overloads_kept_distinct','prior_serial029_and_import144_picker148_not_recounted_or_extended'):
        if w.get(k)is not True:errors.append('B25 true-only boundary:'+k)
    for k,n in(('illustration_count',16),('lexical_check_count',16),('selected_source_paths',10),('whole_local_dialog_files_selected',2),('source_read_slice_count',23)):
        if type(w.get(k))is not int or w[k]!=n:errors.append('B25 exact witness count:'+k)
    err=w.get('retained_additive_B10_arithmetic_erratum',{})
    if err!=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True)or any(type(err.get(k))is not int for k in('local_cost','reference_cost','equality1_control'))or err.get('protected_G138_not_rewritten')is not True:errors.append('B25 retained B10 additive identity')
    return errors

def date_identity_errors(prov,note):
    errors=[]
    if prov.get('audit_reference_date_utc')!='2026-11-16'or not str(prov.get('environment_clock_observed_utc','')).startswith('2026-11-19T'):errors.append('B25 reference16 vs observed19 kept distinct')
    for token in('2026-11-16','2026-11-19','45a2a504db4f82927a286ce425f21a82bcee7a84','f37c37ca6581c4d1546bf0e073326572f4b7af36',B24_CHECK_SHA,'208993','703','322'):
        if token not in note:errors.append('B25 additive date/capture identity:'+token)
    if prov.get('genuine_B24_check_record_checkout')=='45a2a504db4f82927a286ce425f21a82bcee7a84':errors.append('B25 capture cannot be relabelled delivery')
    return errors

def historical_record_errors(h):
    modes=h.get('historical_modes',[])
    if type(h.get('historical_mode_count'))is not int or h['historical_mode_count']!=30 or len(modes)!=30:return['B25 exactly30 actual OWN modes required']
    errors=historical29_errors(dict(historical_mode_count=29,historical_modes=modes[:29],errors=h.get('errors')))
    last=modes[-1]
    for k,value in dict(mode='B24',findings_total=322,registry_used=SNAPSHOT,process_exit_code=0,validation_errors=[],original_project_hashes_matching=827,audit_checker_self_test_cases_reported=694,audit_checker_self_test_suite_count=25).items():
        if last.get(k)!=value or type(last.get(k))is not type(value):errors.append('B25 B24 OWN322/694/25:'+k)
    child=last.get('historical_B24_child')or{}
    for k,value in dict(tests_reported=44,expected_tests=44,process_exit_code=0,result='passed',historical_parser_cutoff='B24-not-current-B25-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_row_ownership_tests_07B25.py',no_test_skips_or_global_subprocess_or_path_patch=True,suite_own_registry_path_is_context_local_not_global=True).items():
        if child.get(k)!=value or type(child.get(k))is not type(value):errors.append('B25 B24 ALL44 explicit child:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(last.get(k))is not int or last[k]!=0:errors.append('B25 no historical ERP/SQL')
    if not isinstance(last.get('stdout_sha256'),str)or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256'])is None:errors.append('B25 historical stdout identity')
    return errors

def validate_source(v,row,scope):
    if'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B25 undeclared documentary sentinel:'+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B25 fabricated source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
        try:expanded=expanded_source_evidence(row['evidence'])
        except ValueError as exc:v.check(False,'B25 invalid source '+row['id']+':'+str(exc));return
        v.scoped_evidence(expanded,scope,row['id']+' boundedB25',phase=7)

def extend_property_dialogs(v,report,prov,frozen322):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[322:]
    for error in registry_preservation_errors(frozen322,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id']for r in current})==324,'B25 distinct324 IDs');ck(rows('evidence/historical-extensions-07B25.csv')==[],'B25 zero historical extensions')
    v.distributions(new,dict(Medium=2),dict(confirmed=2),'B25 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B25 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B25 heading/registry exact')
    lookup={r['id']:r for r in current}
    for name in('P4-014','P7-132','P7-145'):ck(lookup[name]['certainty']=='potential','B25 retained potential:'+name)
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k]is False,'B25 no implicit start:'+k)
    ck(prov['parallel_repairs_not_merged_into_audit_branch']is True,'B25 no repair-to-audit merge')
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k])is int and prov[k]==0,'B25 no ERP/SQL:'+k)
    for error in date_identity_errors(prov,v.read(v.AUDIT/'DATE-IDENTITY-NOTE-07B25.md')):ck(False,error)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected};original={r['path']:r for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==10,'B25 ten bounded source paths')
    for r in selected:
        ck(r['path']in original and r['review_state']=='whole-local-property-dialog-or-selected-surrounding-static-slices-not-runtime-certified'and bool(r['focus']),'B25 scope identity/depth');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B25-{n:02d}'for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B25.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B25 incompleteCSV:'+r['id']);validate_source(v,r,scope)
            if'runtime_status'in r:ck(r['runtime_status']=='not-executed','B25 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B25-','INV7B25-','P7B25T-')]
    for error in current_link_errors(fe,inv,tests)+ledger_errors(tables['DG7B25-'],tables['PK7B25-']):ck(False,error)
    ck(all(f['status']=='confirmed-source-local'for f in fe[:2]),'B25 two source-local causes only')
    v.proposed_tests(tests,'7B25');fids,iids,tids=[{r['id']for r in pool}for pool in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['DG7B25-']+tables['PK7B25-'],fids,'feature_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B25 '+label)
    for r in tables['RC7B25-']:
        fs=[f for f in fe if f['id']in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        evidence=source_evidence_union(fs)
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==evidence,'B25 exact RC source/FE lineage');v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B25-'],rows('evidence/residual-disposition-07B24.csv'))+split_errors(tables['SP7B25-'],rows('evidence/split-register-07B24.csv'))+remaining_work_errors(tables['RW7B25-']):ck(False,error)
    hids={r['id']for r in tables['H7B25-']};sids={r['id']for r in tables['SP7B25-']};v.related(tables['RS7B25-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B25-'],hids,'handoff_ids')
    for r in tables['H7B25-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B25 no invented approval')
    for r in tables['Q7B25-']:ck(r['status']=='unanswered-no-secrets-requested','B25 no invented answer')
    for n,r in enumerate(tables['BK7B25-'],1):ck(r['prior_backlog_id']==f'BK7B24-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B25 backlog ancestry/uncompleted')
    ck([r['status']for r in tables['BK7B25-'][2:6]]==['not-started']*4,'B25 C axes unstarted')
    ad=tables['AD7B25-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B25 onlytwo adjudicated new roots')
    ck([r['current_root_ids']for r in ad if r['decision']=='same-current-root-second-helper-not-separate-finding']==['P7-151'],'B25 second helper same151, not third root')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B25 adjudication source chain')
    ck(all(r['comparison_depth']==DEDUP_DEPTH for r in ad),'B25 honest comparison depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv'for n in range(2,8)]+[f'review-scope-07B{n}.csv'for n in range(1,25)]
    before={r['path']for name in prior_names for r in rows(name)};paths=set(scope)
    bk=dict(selected_paths=len(paths),prior_union=len(before),overlap=len(paths&before),new=len(paths-before),union=len(before|paths),complement=len(original.keys()-(before|paths)),complement_kinds=dict(collections.Counter(original[p]['kind']for p in original.keys()-(before|paths))))
    ck(bk==dict(selected_paths=10,prior_union=419,overlap=8,new=2,union=421,complement=406,complement_kinds={'source':341,'generated-artifact':61,'project-or-resource':4}),'B25 scope not completion percentage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B25.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B24.md','evidence/split-register-07B24.csv','evidence/residual-disposition-07B24.csv']and decision['selected_upstream_split']=='SP7B24-01'and decision['entry']==ENTRY and decision['bookkeeping']==bk,'B25 authority/reasoned scope')
    ck(set(decision['new_paths'])==paths-before and decision['historical_metadata_screen_count']==322 and decision['historical_body_review_claim']is False and decision['historical_comparison_depth']==DEDUP_DEPTH,'B25 comparison depth')
    ck(decision['bounded_read_slice_count']==23 and decision['whole_local_dialog_files']==2 and decision['whole_local_dialog_lines']==dict(code_behind=318,xaml=313),'B25 exact local dialog depth, not all callers')
    for k in('phase7C_started','phase8_authorized_or_started','counts_are_completion_percent_or_sessions'):ck(decision[k]is False,'B25 scope permission/count boundary')
    ck(v.sha(v.AUDIT/'evidence/property-dialog-witnesses-07B25.json')==WITNESS_SHA,'B25 immutable actual witness stdout')
    witness,match=v.recompute('evidence/property-dialog-witnesses-07B25.json','tools/check_property_dialog_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B25 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B25-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B25-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,16);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B25 witness not runtime/policy acceptance');validate_source(v,r,scope)
    reads=witness['bounded_source_reads_not_semantic_coverage'];ck(len(reads)==23 and{r['path']for r in reads}==paths,'B25 23 actual text reads10paths')
    ck(sum(r['whole_local_file_selected']is True for r in reads)==2,'B25 exactlytwo locally whole dialog files')
    for r in reads:
        ck(r['encoding']=='strict-utf-8'and r['whole_bytes_read_for_hash_and_line_index_not_whole_body_review']is True,'B25 reads not whole-feature certification');v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B25 source read',phase=7)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,error)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B25.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B25 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B25.md','PHASE-07-REMAINING-07B25.md','7B26','غير مأذونة','45a2a50','10ba215')),'B25 shared index current boundary:'+name)
    hp='evidence/historical-mode-verification-07B25.json';ck(HISTORICAL_RUN_SHA is not None and(v.AUDIT/hp).is_file(),'B25 genuine30 captured')
    if(v.AUDIT/hp).is_file():
        ck(v.sha(v.AUDIT/hp)==HISTORICAL_RUN_SHA,'B25 actual historical30 identity');h=v.json.loads(v.read(v.AUDIT/hp))
        for error in historical_record_errors(h):ck(False,error)
        ck(h['checkout_head']==ENTRY and h['source_head']==v.HEAD and h['branch']==v.BRANCH,'B25 historical source/entry/capture')
        report['phase_7B25_executed_historical_documentary_modes']=dict(record=hp,sha256=HISTORICAL_RUN_SHA,modes_reported=30,all_documentary_exit_codes_zero=True,B24_OWN322_raw323CRLF_and_historical44_child=True,null_means_aggregate_not_reported_not_zero=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_property_dialog_witnesses.py','validate_property_dialog_part.py','run_historical_row_ownership_tests_07B25.py','test_property_dialog_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as exc:ck(False,'B25 syntax:'+str(exc))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/tools[-1])],cwd=v.ROOT,capture_output=True,text=True,timeout=60)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None;passed=run.returncode==0 and count==44
    ck(passed,'B25 44 documentary self-tests/count: '+(run.stderr[-5000:]if not passed else''))
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=44,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name)for name in['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B25-324-bounded-R4i-property-dialog-not-7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,26))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B26-proposed-R4j-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=152,phase_7B25=2,total_open_not_remediated=324,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:10,'phase_7B25_prior_union':419,'phase_7B25_overlap_with_prior_union':8,'phase_7B25_new_paths':2,'unique_union_not_line_or_execution_coverage':421,'inventory_only_no_selected_scope':406})
    report['phase_7B24_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=703,historical_check_record_overwritten=False,genuine_b24_stdout_sha256_unchanged=B24_CHECK_SHA,partial7B25_append_only_extensions=[],all322_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B25_property_dialog_trace_limits']=dict(selected_dialog_boundaries=8,selected_packing_boundaries=8,bounded_source_reads=23,selected_paths=10,whole_local_dialog_files=2,whole_local_dialog_lines=631,all_callers_or_SDK_DTOs_body_reviewed=False,current_features_or_documentary_contracts=16,invariants_not_executed_tests=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_further_static_splits=3,B_R4i_delivered_not_whole_R4_SP01_or7B_closure=True,retained_potential_roots_not_promoted=['P4-014','P7-132','P7-145'],prior_serial029_import144_picker148_not_recounted_or_extended=True,InvoiceDGV_not_actual_Invoicecontract_dialog_support=True,direct_sale_Description_hidden_by_default=True,input_output_column_helper_returns_empty=True,integer60_to180_not_WPF_schedule_or_financial_or_packing_policy_acceptance=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False,repair_conversation_started_or_synced_not_asserted=True)
    report['evidence_rows'].update(phase_7B25_illustrations_not_erp_tests=16,phase_7B25_lexical_checks_not_erp_tests=16,phase_7B25_bounded_source_reads_not_semantic_coverage=23,phase_7B25_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=(
      'Read-only bounded7B25/R4i:703 protected artifacts/322 EXACT dictionaries and ALLnext_phase/evidence/raw323CRLFprefix/G215/827 originals/three freezes. '
      '151 Medium confirmed source-local: property2..4 helper ignores normal nontrue dialog outcome, reads fresh scalarNetQnty0 assigned only by Insert, overwrites item/detail quantities and description; loader Add after normal LoadItemInf return can retain that attempt. No actual modal close, SQL lookup or final saved loss asserted. '
      '152 Medium confirmed source-local: packing reads prior net text, divides by width and multiplies qty into SAME text; two sequential integer supplied calls20->60->180 without new business inputs. Internal bool guards nested calls, resets finally, not sequential idempotence. Qty1/zero and area/perimeter controls, ceiling conditional retained, no business/.NET parser/formatter/rounding/financial policy oracle. '
      'Two locally whole dialog files318C#/313XAML plus23 text reads10paths NOT all callers/SDK DTOs/477 bodies/callgraph/capability census/455FE. InvoiceDGV homologue same151 not third root or actual Invoicecontract support; its loader lacks dialog in selected body. Sale Description collapsed/SortMemberPath-layout contract unresolved; input-output helper returns empty. No unconditional existing-row editor reachability, unsupported/missing-feature/collection runtime or new serial finding inferred. '
      '322 title/certainty summaries plus path-filtered metadata and named nearest bodies/chains, not all322 bodies or all evidence paths manually reviewed.10paths/8overlap/2new->421/complement406 not percent or406 C tasks.16FE/INV32 acceptance plans NOT executed.14 residuals/3splits/HQ6 preserve all ancestry/input/routes/dispositions, not14 approvals.014/132/145 potential,020/021 and financial/ACL/stock/save/production gates unchanged. '
      'B24 OWN322/raw323CRLF/indexes and ALL44 protected cases in explicit presetB24 child with suite-local A;B23/44,B22/40,B21/36,B20/32,B19/36,B18/28 unchanged. Actual B25 CLI and API main defaultB15 tested separately. No protected edits/skips/globalPath/shared subprocess mutation/disk overlay/rebaseline/archive rewrite. '
      'Actual30 OWN captures preserve capture-time tools, NOT final-wholesale/postpush replay. Reference2026-11-16 separate from observed sandbox2026-11-19; additive identity note never relabels B24capturef37c37c as completedB24push-entry45a2a50. Retained B10 additive10vs120/equality1=10/G138. '
      'No application import/build/C#/VB/.NET/WPF/SQL/provider/SDK/UtilitiesProj/ToDataTable/REPX/scanner/printer/business data/secrets/remediation/measurement/acceptance.7B/7 partial,R4j/B26 proposed,7C unstarted,8 unauthorized here. Independent repairs separate,not presumed started/synchronized,no repair-to-audit merge;next_phase8 planning not permission.')
