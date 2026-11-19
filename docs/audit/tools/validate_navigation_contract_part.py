#!/usr/bin/env python3
"""Bounded documentary7B19/R4c navigation/loader/save-boundary audit, NOT ERP.

523 protected audit artifacts/302 EXACT historical rows/ALLnext_phase/evidence/
raw-prefix/G01..184/827 originals. B18 OWN302/raw303CRLF/indexes IN MEMORY;
its ALL28 original cases execute in a dedicated explicitly historical child with
B18 parser preset. Current default/entrypoint B19 tested separately. No editing
protected helpers/test methods, skips, disk overlays or global Path/subprocess
patches, rebaseline, archive rewrite, application import/build/WPF/C#/SQL/DTO/
provider/interpreter/printer/real data/remediation/measurement/7C/authorization8.
NV22 route instances/19 literal tokens/2 parents/7 leaves and23 selected paths
are NOT allcallgraph/all editors or capability census. R4c bounded; R4d proposed.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,bidirectional_errors
from validate_statement_contract_part import arithmetic_erratum_errors

SCOPE_FILE='review-scope-07B19.csv'
PART_DOCS=('PHASE-07B19.md','NAVIGATION-CONTRACTS-07B19.md','VALIDATION-07B19.md','PHASE-07-REMAINING-07B19.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B18.csv'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B18.json'
SNAPSHOT_SHA='3ed75512f7f998abf3c49f2bc5d27ab6c6d37dffd6521ce59835783da28208a1'
SHARED_SHA='caef7e54e683a42ae98b80a71b7319dac31fbca3ef92a9b69068cf2569fa6c60'
PROVENANCE_SHA='3824fc6427bfbcc8ae45fe25360b8eac6e5356e3161fd3215f558bd236765c00'
B18_CHECK_SHA='abe579df675cf7e0858eb209d8524d6c97cf663205f04b9515d2e76aade87c03'
WITNESS_SHA='eab94591ab49ba379728beaa0d65f19e0a3a26d06fb12b4243660c3079cca836'
HISTORICAL_RUN_SHA='c9bb8f4f1adff9df8d8ce2cb0822a0bdaf0f891ee7cbd9b2b70cb7185ea0c022' # Genuine24 executed OWN-mode record; absent aggregates remain null.
ENTRY='ee393a741a862a605c6c2f688d3f634bd91856ae'
DOCUMENTARY='none-documentary-metadata'
NEW_IDS=[f'P7-{n}'for n in range(131,136)]
TABLE_SPECS=(('navigation-ledger','NV7B19-',22),('leaf-contract-ledger','LC7B19-',7),
 ('feature-implementation-matrix','FE7B19-',18),('report-invariants','INV7B19-',18),
 ('acceptance-tests','P7B19T-',36),('report-reconciliation','RC7B19-',6),
 ('root-adjudication','AD7B19-',9),('residual-disposition','RS7B19-',14),
 ('split-register','SP7B19-',3),('handoffs','H7B19-',6),('questions','Q7B19-',6),
 ('remaining-workplan','RW7B19-',10),('continuation-backlog','BK7B19-',10))
SENTINELS={f'{prefix}{n:02d}'for prefix,nums in(
 ('FE7B19-',(16,17,18)),('INV7B19-',(16,17,18)),('P7B19T-',range(31,37)),
 ('RC7B19-',(6,)),('RS7B19-',range(1,15)),('SP7B19-',range(1,4)),
 ('H7B19-',(2,5,6)),('Q7B19-',(2,5,6)))for n in nums}
LEAVES=('frmInvSale','frmInvPurch','frmInvPOS','frmInvInputOutput','frmProductionOrder','frmInventoryTransfer','frmSafeAdjust')
# Manually reviewed bounded dispatcher shapes, NOT inferred C# receiver types.
NAVIGATION_SHAPES=((0,'2','1'),(0,'2','2'),(1,'1','1'),(1,'1','2'),(2,'3','1'),(2,'3','2'),
 (1,'9','1'),(3,'4','1'),(3,'5','1'),(4,'6','1'),(4,'6','2'),(5,'8','1'),(5,'8','2'),(6,'SafesAdjust','not-in-query'),
 (5,'8','row.ProcType'),(5,'8','row.ProcType'),(1,'9','row.ProcType'),(3,'4','row.ProcType'),
 (3,'5','row.ProcType'),(4,'6','row.ProcType'),(3,'14','row.ProcType'),(6,'7','row.ProcType'))


def row_sha(row):
    return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@contextmanager
def historical_b18_inputs(v,frozen302,texts,raw):
    """Only exact302 logical registry rows/bytes and three frozen shared texts."""
    if len(frozen302)!=302 or len({r['id']for r in frozen302})!=302:raise ValueError('Exactly302 distinct OWN B18 rows required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):raise ValueError('Exact noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except(UnicodeError,csv.Error)as e:raise ValueError('Malformed frozen302 registry')from e
    if(parsed!=frozen302 or raw.count(b'\r\n')!=303 or not raw.endswith(b'\r\n')
       or any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n'))):raise ValueError('Exact frozen302 rows/bytes/303CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen302,texts):yield
    finally:v.AUDIT=original


class HistoricalB18Subprocess:
    """Narrow facade, NEVER mutate the shared subprocess module/run function.

    Only the exact protected B18 self-test argv is redirected to its explicit
    historical launcher; unrelated commands/options/working directory pass through.
    """
    def __init__(self,backend,python,tool_dir):
        self.backend=backend
        self.expected=[python,'-B',str(tool_dir/'test_caller_request_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_caller_request_tests_07B19.py'),'--through-part','B18']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):
        return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB18ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target)
        object.__setattr__(self,'_subprocess',HistoricalB18Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess'else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


def validate_frozen_b18(v,report,prior,frozen300,prov,frozen302):
    ck=v.check
    for name,digest in(('evidence/provenance-07B19.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B18.json',B18_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B19 immutable entry: '+name)
    ck(prov['historical_artifact_count']==523 and len(frozen302)==302,'B19 entry counts')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
       and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B19 entry snapshot names/SHAs')
    for name,digest in prior['historical_artifact_sha256'].items():ck(prov['historical_artifact_sha256'].get(name)==digest,'495-to523 protected continuity: '+name)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B18.json'))
    ck(saved['checkout_head']=='12d2e4b1bc566a860643b8459b16cbc85a6d2c3d'and saved['validation']['errors']==[]
       and saved['findings']['total_open_not_remediated']==302 and saved['original_project_hashes_matching']==827
       and saved['historical_artifact_sha256']==prior['historical_artifact_sha256']
       and saved['validation']['current_output_record_pending_first_write_not_placeholder']is False,'B18 genuine stdout identity not delivered push HEAD')
    ck(prov['genuine_B18_check_sha256']==B18_CHECK_SHA and prov['genuine_B18_check_record_checkout']==saved['checkout_head']
       and prov['prior_provenance_B18_sha256']==v.sha(v.AUDIT/'evidence/provenance-07B18.json'),'B19 prior record identity')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B19 entry follows delivered pushed B18')
    ck(prov['phase7B18_entry_consistency']==dict(original_hashes_matching=827,findings=302,
       phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,19))+'-partial-not-complete7B-or7',audit_file_count=528,errors=[],erp_runtime_tests_executed=0),'B19 completed B18 entry context')
    from validate_caller_request_part import extend_caller_requests
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    view=HistoricalB18ValidatorView(v)
    with historical_b18_inputs(view,frozen302,texts,(v.AUDIT/SNAPSHOT).read_bytes()):extend_caller_requests(view,report,prior,frozen300)
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_caller_request_audit_validator.py']
    record.update(historical_parser_cutoff='B18-not-current-B19-default',all_original_cases_executed_unmodified=True,
       dedicated_child_launcher='tools/run_historical_caller_request_tests_07B19.py',actual_subprocess_argv=view.subprocess.actual,
       no_test_skips_or_global_subprocess_or_path_patch=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B18-302-not-current-state',
       phase_7B18_historical_input_mode='OWN302-exact303CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B18-test-child',
       phase_7B18_adapter_context=dict(entry_provenance='evidence/provenance-07B19.json',adapter_protected_artifacts_checked=523,
          current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,
          B18_parser_assertions_are_historical_preset_not_current_default=True))


def registry_preservation_errors(previous,current,raw,frozen_raw):
    errors=[]
    if len(previous)!=302 or current[:302]!=previous:errors.append('B19 all302 exact rows/ALLnext_phase/evidence')
    if len(current)!=307 or [r.get('id')for r in current[302:]]!=NEW_IDS:errors.append('B19 only five appended roots131..135')
    if(type(raw)is not bytes or type(frozen_raw)is not bytes or not raw.startswith(frozen_raw)
       or raw.startswith(b'\xef\xbb\xbf')or raw.count(b'\r\n')!=308 or not raw.endswith(b'\r\n')
       or any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n'))):errors.append('B19 exact raw302 prefix/current308CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B19 rows/raw bytes disagree')
        except(UnicodeError,csv.Error):errors.append('B19 malformed registry bytes')
    return errors


def group_row_errors(previous,current):
    gr=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    old,new=gr(previous),gr(current)
    if len(old)!=184 or new[:184]!=old:return ['B19 exact G01..184 rows changed']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{i:02d}'for i in range(1,191)]:return ['B19 G185..190 only, exact order']
    return []


def navigation_errors(current,literals):
    errors=[]
    if len(current)!=22 or len(literals)!=19:return ['B19 NV22 instances/19 bounded literal call tokens required']
    lookup={(r['source_path'],str(r['call_line_start']),str(r['call_line_end'])):r for r in literals}
    if len(lookup)!=19:errors.append('B19 distinct19 literal token keys required')
    got=set()
    for n,r in enumerate(current):
        leaf_index,inv_type,proc_type=NAVIGATION_SHAPES[n]
        if(r.get('leaf'),r.get('query_inv_type'),r.get('query_proc_type'))!=(LEAVES[leaf_index],inv_type,proc_type):errors.append('B19 declared bounded dispatcher/leaf/query shape')
        expected_identity='display-label-plus-local-id-no-branch-in-query'if n<14 else'row-InvGlobalID-and-procType-plus-current-type-index'
        if r.get('identity_contract')!=expected_identity:errors.append('B19 document identity lineage not ACL approval')
        key=(r.get('source_path'),r.get('call_line_start'),r.get('call_line_end'));actual=lookup.get(key);got.add(key)
        if actual is None or any(r.get(k)!=actual[k]for k in('call_text_sha256','inert_argument_expression')):errors.append('B19 exact literal line/hash/argument lineage')
        parent='detailed'if n<14 else'inventory'
        if r.get('parent')!=parent or r.get('publication_order')!=('configure-Navigate-before-Show'if parent=='detailed'else'Show-before-Navigate-not-Loaded-completion-proof'):
            errors.append('B19 publisher order source-bound, not WPF acceptance')
        if r.get('leaf')not in LEAVES or r.get('receiver_boundary')!=f'LC7B19-{LEAVES.index(r["leaf"])+1:02d}':errors.append('B19 named leaf/contract link')
        for field in('limit','owner_role','required_redacted_input','impact_if_unavailable','next_step'):
            if not isinstance(r.get(field),str)or not r[field].strip():errors.append('B19 route missing boundary: '+field)
        if r.get('runtime_status')!='not-executed':errors.append('B19 route runtime overclaim')
    if got!=set(lookup)or len({r.get('source_path')for r in current})!=2 or len({r.get('leaf')for r in current})!=7:errors.append('B19 all19 literal keys/two parents/seven selected leaves')
    if [r.get('route_discriminator')for r in current[14:]]!=['cmbType.SelectedIndex='+str(n)for n in range(8)]:errors.append('B19 eight inventory type route instances')
    if current[-1].get('finding_ids')!='P7-131':errors.append('B19 wrong safe table root not generic ACL')
    return errors


def leaf_errors(current):
    errors=[]
    if len(current)!=7 or [r.get('leaf')for r in current]!=list(LEAVES):return ['B19 exactly seven named selected leaf contracts']
    for r in current:
        for k in('entry_and_reader','empty_or_failure_contract','lifecycle_boundary','dirty_guard_boundary','save_guard_boundary',
                  'owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(r.get(k),str)or not r[k].strip():errors.append('B19 leaf missing boundary: '+k)
        if r.get('runtime_status')!='not-executed':errors.append('B19 leaf runtime overclaim')
    return errors


def current_link_errors(features,invariants,tests):
    errors=[]
    if(len(features),len(invariants),len(tests))!=(18,18,36):errors.append('B19 FE18/INV18/T36 counts')
    for n,(fe,inv)in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):errors.append('B19 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or ';'.join(t['id']for t in related)!=fe.get('acceptance_ids'):errors.append('B19 exactly two reverse-linked plans per FE')
        if n<=5 and(fe.get('finding_ids')!=NEW_IDS[n-1]or any(t.get('plan_kind')!='finding-specific'or t.get('finding_ids')!=NEW_IDS[n-1]for t in related)):
            errors.append('B19 independent five new root plans')
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=18 or len({r.get('acceptance_criterion')for r in tests})!=36:errors.append('B19 distinct substantive invariant/criteria')
    if any(t.get('status')!='not-executed'for t in tests):errors.append('B19 acceptance never executed')
    return errors


def residual_errors(current,upstream):
    errors=[]
    if len(current)!=14 or len(upstream)!=14:return ['B19 all14 named B18 residuals required']
    for old,new in zip(upstream,current):
        if(new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B18.csv'
           or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):errors.append('B19 exact upstream residual identity/hash/contracts')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B19 missing residual responsibility: '+k)
        if new.get('disposition')not in{'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':errors.append('B19 residual approval/execution overclaim')
    return errors


def remaining_work_errors(work,splits):
    from validate_caller_request_part import remaining_work_errors as old_errors
    adapted=[dict(r)for r in work]
    if len(adapted)!=10 or adapted[3].get('status')!='bounded-R4c-navigation-delivered-residuals-open':return ['B19 R4c bounded status, not wholeR4/7B closure']
    adapted[3]['status']='bounded-R4b-direct-callers-delivered-residuals-open'
    return ['B19 '+e for e in old_errors(adapted,splits)]


def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used',
             'spreadsheet_or_formula_interpreter_executed','phase7C_started','phase8_authorized_or_started'):
        if w.get(k)is not False:errors.append('B19 false-only boundary: '+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B19 integer-zero boundary: '+k)
    for k in('B_R4c_bounded_not_whole7B_closure','prior_roots_not_assumed_remediated','unresolved_external_contracts_and_explicit_splits_retained'):
        if w.get(k)is not True:errors.append('B19 true-only boundary: '+k)
    for k in('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k))is not int or w[k]!=14:errors.append('B19 14 independent/14 lexical count: '+k)
    if w.get('phase')!='7B19-partial-static-navigation-contracts':errors.append('B19 witness phase')
    return errors+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def historical_record_errors(h):
    errors=[];modes=h.get('historical_modes',[])
    expected=['phase'+str(n)for n in range(2,7)]+['A']+['B'+str(n)for n in range(1,19)]
    counts=[49,74,106,137,172,200,223,237,248,261,266,270,276,280,282,285,287,289,291,294,298,299,300,302]
    registries=['evidence/findings-through-'+f'{n:02d}'+'.csv'for n in range(2,7)]+['evidence/findings-through-07A.csv']+['evidence/findings-through-07B'+str(n)+'.csv'for n in range(1,19)]
    aggregates=[(None,None)]*7+[(44,3),(62,4),(82,5),(104,6),(132,7),(156,8),(184,9),(208,10),(236,11),(266,12),(298,13),(322,14),(350,15),(382,16),(410,17),(434,18),(462,19)]
    spec=dict(zip(expected,zip(counts,registries,aggregates)))
    if type(h.get('historical_mode_count'))is not int or h['historical_mode_count']!=24 or[r.get('mode')for r in modes]!=expected:errors.append('B19 exactly24 historical OWN-mode records')
    if h.get('errors')!=[]:errors.append('B19 historical failures')
    for r in modes:
        if type(r.get('process_exit_code'))is not int or r['process_exit_code']!=0 or r.get('validation_errors')!=[]or r.get('original_project_hashes_matching')!=827:errors.append('B19 historical documentary failure/hash')
        if any(type(r.get(k))is not int or r[k]!=0 for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed')):errors.append('B19 no historical ERP/SQL run')
        for k in('audit_checker_self_test_cases_reported','audit_checker_self_test_suite_count'):
            if r.get(k)is not None and(type(r[k])is not int or r[k]<0):errors.append('B19 absent historical aggregate must be null, not guessed')
        if r.get('mode')in spec:
            count,registry,agg=spec[r['mode']]
            if type(r.get('findings_total'))is not int or r['findings_total']!=count or r.get('registry_used')!=registry:errors.append('B19 historical OWN count/registry, never future live rows')
            if tuple(r.get(k)for k in('audit_checker_self_test_cases_reported','audit_checker_self_test_suite_count'))!=agg:errors.append('B19 genuine reported historical aggregates/nulls, not guesses')
        if r.get('mode')=='B18':
            child=r.get('historical_B18_child')or{}
            if(child.get('tests_reported')!=28 or child.get('expected_tests')!=28 or child.get('process_exit_code')!=0 or child.get('result')!='passed'
               or child.get('historical_parser_cutoff')!='B18-not-current-B19-default' or child.get('all_original_cases_executed_unmodified')is not True
               or child.get('dedicated_child_launcher')!='tools/run_historical_caller_request_tests_07B19.py'
               or child.get('no_test_skips_or_global_subprocess_or_path_patch')is not True):errors.append('B19 historical B18 ALL28 explicit child identity')
        if not isinstance(r.get('stdout_sha256'),str)or re.fullmatch(r'[0-9a-f]{64}',r['stdout_sha256'])is None:errors.append('B19 historical raw stdout SHA')
    return errors


def validate_source(v,row,scope):
    if'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B19 undeclared documentary sentinel: '+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B19 fabricated source for metadata gate: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' boundedB19',phase=7)


def extend_navigation_contracts(v,report,prov,frozen302):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[302:]
    for error in registry_preservation_errors(frozen302,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id']for r in current})==307,'B19 distinct307 IDs')
    ck(rows('evidence/historical-extensions-07B19.csv')==[],'B19 zero historical extensions')
    v.distributions(new,{'High':2,'Medium':3},{'confirmed':4,'potential':1},'B19 only')
    ck([r['certainty']for r in new]==['confirmed','potential','confirmed','confirmed','confirmed'],'B19 lifecycle132 remains conditional potential')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B19 finding/authorization state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B19 exact heading/registry')
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k]is False,'B19 no implicit start: '+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k])is int and prov[k]==0,'B19 no ERP/SQL: '+k)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected}
    ck(len(selected)==len(scope)==23,'B19 23 selected slice paths')
    original={r['path']for r in rows('evidence/inventory.csv')}
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-navigation-loader-save-boundary-slices-not-runtime-certified'and bool(r['focus']),'B19 scope selection')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B19-{n:02d}'for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B19.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B19 incomplete CSV cells: '+r['id'])
            validate_source(v,r,scope)
            if'runtime_status'in r:ck(r['runtime_status']=='not-executed','B19 runtime overclaim: '+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B19-','INV7B19-','P7B19T-')]
    for error in current_link_errors(fe,inv,tests):ck(False,error)
    v.proposed_tests(tests,'7B19')
    fids,iids,tids=[{r['id']for r in pool}for pool in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B19 '+label)
    for r in tables['RC7B19-']:
        fs=[f for f in fe if f['id']in r['feature_ids'].split(';')];unique=lambda key:';'.join(dict.fromkeys(x for f in fs for x in f[key].split(';')))
        refs=[f['evidence']for f in fs if f['evidence']!=DOCUMENTARY]
        expected=';'.join(dict.fromkeys(x for s in refs for x in s.split(';')))if refs else DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==expected,'B19 RC exact FE lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B19-'],rows('evidence/residual-disposition-07B18.csv'))+remaining_work_errors(tables['RW7B19-'],tables['SP7B19-']):ck(False,error)
    hids={r['id']for r in tables['H7B19-']};sids={r['id']for r in tables['SP7B19-']}
    v.related(tables['RS7B19-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B19-'],hids,'handoff_ids')
    for r in tables['H7B19-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B19 no invented approval')
    for r in tables['Q7B19-']:ck(r['status']=='unanswered-no-secrets-requested','B19 no invented policy answer')
    for n,r in enumerate(tables['BK7B19-'],1):ck(r['prior_backlog_id']==f'BK7B18-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B19 backlog ancestry/uncompleted')
    ck([r['status']for r in tables['BK7B19-'][2:6]]==['not-started']*4,'B19 no accidental C start')
    ad=tables['AD7B19-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B19 five adjudicated roots only')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B19 adjudication source chain')
    ck(all(r['comparison_depth']=='all302-registry-titles-classifications-plus-selected-nearest-source-chains-not-all-historical-bodies'for r in ad),'B19 honest dedup depth')
    prev_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv'for n in range(2,8)]+[f'review-scope-07B{n}.csv'for n in range(1,19)]
    before={r['path']for name in prev_names for r in rows(name)};paths=set(scope)
    ck((len(before),len(paths&before),len(paths-before),len(before|paths),len(original-(before|paths)))==(408,21,2,410,417),'B19 selected-path bookkeeping not coverage percentage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B19.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B18.md','evidence/split-register-07B18.csv']and decision['selected_upstream_split']=='SP7B18-01'
       and decision['entry']==ENTRY and decision['bookkeeping']==dict(selected_paths=23,prior_union=408,overlap=21,new=2,union=410,complement=417,complement_kinds={'source':352,'generated-artifact':61,'project-or-resource':4}),'B19 reasoned scope decision/authority')
    ck(v.sha(v.AUDIT/'evidence/navigation-contract-witnesses-07B19.json')==WITNESS_SHA,'B19 genuine first witness capture')
    witness,match=v.recompute('evidence/navigation-contract-witnesses-07B19.json','tools/check_navigation_contract_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B19 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B19-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B19-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,14);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B19 witness not ERP semantics')
            validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B19 lexical read',phase=7)
    discovery=witness['navigation_literal_discovery'];ck(discovery['not_complete_callgraph_or_capability_census']is True,'B19 no callgraph/census claim')
    for error in navigation_errors(tables['NV7B19-'],discovery['literal_calls'])+leaf_errors(tables['LC7B19-']):ck(False,error)
    for r in tables['NV7B19-']:v.related([r],{x['id']for x in tables['LC7B19-']},'receiver_boundary')
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
            if target==(v.AUDIT/'evidence/checks-07B19.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B19 broken link: '+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B19.md','PHASE-07-REMAINING-07B19.md','7B20','غير مأذونة','ee393a7','10ba215')),'B19 current shared index boundary: '+name)
    hist_path='evidence/historical-mode-verification-07B19.json'
    ck(HISTORICAL_RUN_SHA is not None and(v.AUDIT/hist_path).is_file(),'B19 historical24 record captured, not placeholder')
    if(v.AUDIT/hist_path).is_file():
        ck(v.sha(v.AUDIT/hist_path)==HISTORICAL_RUN_SHA,'B19 genuine historical24 raw-output identities')
        historical=v.json.loads(v.read(v.AUDIT/hist_path))
        for error in historical_record_errors(historical):ck(False,error)
        ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD and historical['branch']==v.BRANCH,'B19 historical-mode source/entry identity')
        report['phase_7B19_executed_historical_documentary_modes']=dict(record=hist_path,sha256=HISTORICAL_RUN_SHA,modes_reported=24,all_documentary_exit_codes_zero=True,
            B18_OWN302_raw303CRLF_and_historical_test_child=True,null_means_aggregate_not_reported_not_zero_tests=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_navigation_contract_witnesses.py','validate_navigation_contract_part.py','run_historical_caller_request_tests_07B19.py','test_navigation_contract_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B19 syntax: '+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_navigation_contract_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None
    passed=run.returncode==0 and count==36;ck(passed,'B19 36 documentary self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=36,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name)for name in['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B19-307-bounded-R4c-navigation-contracts-not-7B-or-runtime-closure',
        phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,20))+'-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B20-proposed-R4d-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],
        registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=135,phase_7B19=5,total_open_not_remediated=307,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:23,'phase_7B19_prior_union':408,'phase_7B19_overlap_with_prior_union':21,'phase_7B19_new_paths':2,'unique_union_not_line_or_execution_coverage':410,'inventory_only_no_selected_scope':417})
    report['phase_7B18_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,
        earlier_report_evidence_artifacts_hash_checked=523,historical_check_record_overwritten=False,genuine_b18_stdout_sha256_unchanged=B18_CHECK_SHA,partial7B19_append_only_extensions=[],all302_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B19_navigation_trace_limits']=dict(route_instances_not_unique_calls=22,bounded_literal_Navigate_tokens=19,parent_paths=2,selected_leaf_boundaries_not_whole_editors=7,current_FE_or_documentary_contracts=18,
        current_invariants_not_executed_tests=18,acceptance_plans_not_executed=36,residual_inputs=14,explicit_further_static_splits=3,B_R4c_delivered_not_whole_R4_or7B_closure=True,
        potential_lifecycle_root_requires_WPF_confirmation='P7-132',production_save_parameter_identity_barriers_not_assumed_fixed=['P4-020','P4-021'],C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B19_illustrations_not_erp_tests=14,phase_7B19_lexical_checks_not_erp_tests=14,phase_7B19_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),phase_7B19_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only documentary B19/R4c:523 protected artifacts/302 EXACT rows/ALLnext_phase/evidence/raw303CRLFprefix/G01..184/three freezes/827 originals. Five static roots131..135;132potential WPF initialization risk, not actual event/duplicate-save observation. Safe request Inv versus SafesAdjust.Is_Approved in supplied DDL; deployedschema unresolved. Production loader omits local BaseQty(default0)/UnitEquality(default1); qty-event guard skips, unit-event may zero; early Round2 mutates quantity/price model, not merely display. P4-020 parameter barrier and021 conditional identity preserved; no successful corrupt production save claimed. POS existing/nonElectronic replaces InvDate with Now after old date check; electronic-existing counterevidence, no deployed loss/legal conclusion.061/001/031/017/018/019 and permissions retained without recount or extensions. NV22 route instances from19 bounded literal tokens/2parents/7leaf selected boundaries;23paths/21overlap/2new/union410/complement417 NOT full editors/writers/callgraph/capability census;455 historical FE not rereviewed.18FE/INV36plans all not-executed;14RS3splits6H/Q unresolved;R4d/B20 proposed;6 C axes unstarted;8 unauthorized. B18 OWN302/exact303CRLF/indexes in memory. Its ALL28 original cases execute in explicit historical child B18 preset; current B19default/entrypoint independently tested with36 new synthetic cases. No protected test/helper edits/skips/global subprocess or Path patch/disk overlay/rebaseline/archive rewrite. Source10ba, completed B18push/entryee393a7, genuine B18stdoutcheckout12d2e4b distinct.14 manual models+14 lexical/68 bounded reads are not.NET/SQL semantics or business acceptance. Additive B10 erratum10vs120 retained. No app import/build/C#/SQL/VB/WPF/SDK/DTO/REPX/Office/COM/interpreter/provider/device/printer/business export/application shell/real data/secrets/remediation/measurement.7B/7 partial;7C unstarted;8 unauthorized;next_phase8 planning not permission.')
