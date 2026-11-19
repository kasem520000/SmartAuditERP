#!/usr/bin/env python3
"""Bounded 7B20/R4d barcode/scale/label documentary consistency, NOT ERP.

553 protected artifacts/307 EXACT rows/ALLnext_phase/evidence/rawprefix/G190/
827 originals/three entry freezes. B19 OWN307/raw308CRLF/indexes in memory;
ALL36 unmodified B19 cases run in an explicit historical B19 child, separately
from current B20 CLI/default tests. No protected edits/skips/global Path or
subprocess patches/disk overlay/rebaseline/archive rewrite/application import/
build/C#/SQL/WPF/DTO/UtilitiesProj/REPX/scanner/printer/business data/remediation/
measurement. Seven qualified tokens do not mean whole callgraph/census;20 paths
are bounded slices. R4d bounded;7B/7 partial;7C unstarted;8 unauthorized.
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
from validate_navigation_contract_part import historical_record_errors as historical24_errors

ENTRY='ac20e3104f84fefbc62779e22d2c9b9621802340'
SNAPSHOT='evidence/findings-through-07B19.csv';SNAPSHOT_SHA='2dd98fa8749a00126a5d3cad768abf5e331e9a4a3e543ea9304c7cd71b646005'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B19.json';SHARED_SHA='290f7a11bdb52eed6e5e984dbde5827a1a1b91bfa7ab0f7068dfc8a7d2b42c0a'
PROVENANCE_SHA='df4f094b448efa3bf40ca64f34ceef31130aa56f111cf4c375118f3bbc5b4c32'
B19_CHECK_SHA='0d4af1111224664716671586dfde5595aa4114ff9f01f75e4ca531267d08a6ed'
WITNESS_SHA='c9157db08cf3807adcec0351b4c9dec52a6b8941db9ba2e17bcd49f7246b007b'
HISTORICAL_RUN_SHA='76bf627af27599e8ccab44994c10198cb31c2d62617f7a1b73d167d1033d4f55' # Actual25 OWN subprocess captures, not regenerated stdout.
SCOPE_FILE='review-scope-07B20.csv';DOCUMENTARY='none-documentary-metadata'
PART_DOCS=('PHASE-07B20.md','BARCODE-CONTRACTS-07B20.md','VALIDATION-07B20.md','PHASE-07-REMAINING-07B20.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
NEW_IDS=['P7-136','P7-137','P7-138']
TABLE_SPECS=(('barcode-callers','BC7B20-',7),('decoder-contracts','DC7B20-',5),('feature-implementation-matrix','FE7B20-',16),
 ('report-invariants','INV7B20-',16),('acceptance-tests','P7B20T-',32),('report-reconciliation','RC7B20-',5),('root-adjudication','AD7B20-',8),
 ('residual-disposition','RS7B20-',14),('split-register','SP7B20-',3),('handoffs','H7B20-',6),('questions','Q7B20-',6),('remaining-workplan','RW7B20-',10),('continuation-backlog','BK7B20-',10))
SENTINELS={f'{prefix}{n:02d}'for prefix,nums in(('FE7B20-',range(14,17)),('INV7B20-',range(14,17)),('P7B20T-',range(27,33)),
 ('RC7B20-',(4,5)),('RS7B20-',range(1,15)),('SP7B20-',range(1,4)),('H7B20-',range(1,7)),('Q7B20-',range(1,7)))for n in nums}
CALLER_SHAPES={
 'frmInvInputOutput':('identity+unit-only','discarded','discarded','false'),
 'frmInvPOS':('positive-values-only-after-new-line','positive-only','positive-only','positive-qty-or-price'),
 'frmInvPurch':('identity+unit-only','discarded','discarded','false'),
 'frmInvSale':('identity+unit-only','discarded','discarded','false'),
 'frmInventoryTransfer':('identity+unit-selection-only','discarded-support-unresolved','discarded-support-unresolved','false'),
 'frmPrintBarcode':('label-raw-barcode+base-item-price','not-label-copy-count','discarded-use-base-price','not-invoice-line'),
 'frmSafeAdjust':('item-selection-for-stock-not-counted-weight','not-realstock-count','not-selected-price','not-invoice-line')}


def row_sha(row):return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@contextmanager
def historical_b19_inputs(v,frozen307,texts,raw):
    """Exact OWN registry only; all identities restored, even on an exception."""
    if len(frozen307)!=307 or len({r.get('id')for r in frozen307})!=307:raise ValueError('Exactly307 distinct B19 OWN rows required')
    if set(texts)!=set(SHARED_DOCS)or any(not isinstance(t,str)for t in texts.values()):raise ValueError('Exactly three frozen shared texts required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):raise ValueError('Exact noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except(UnicodeError,csv.Error)as e:raise ValueError('Malformed307 frozen registry')from e
    if(parsed!=frozen307 or raw.count(b'\r\n')!=308 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n'))):raise ValueError('307 rows/raw308CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen307,texts):yield
    finally:v.AUDIT=original


class HistoricalB19Subprocess:
    """Exact one-argv facade; no mutation of the shared subprocess module."""
    def __init__(self,backend,python,tool_dir):
        self.backend=backend;self.expected=[python,'-B',str(tool_dir/'test_navigation_contract_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_navigation_tests_07B20.py'),'--through-part','B19']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB19ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target);object.__setattr__(self,'_subprocess',HistoricalB19Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess'else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b19_validation(v,report,prior,prov,frozen307):
    """Main still calls the real protected B19 extension, inside this OWN context."""
    ck=v.check
    for name,digest in(('evidence/provenance-07B20.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B19.json',B19_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B20 immutable entry:'+name)
    ck(prov['historical_artifact_count']==553 and len(frozen307)==307,'B20 entry553/307')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B20 frozen entry names/hashes')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B20 protected523-to553 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B19.json'));suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='ee393a741a862a605c6c2f688d3f634bd91856ae'and old['findings']['total_open_not_remediated']==307 and old['validation']['errors']==[]and old['original_project_hashes_matching']==827 and old['validation']['current_output_record_pending_first_write_not_placeholder']is False,'B20 genuine B19 stdout, not delivered HEAD')
    ck(len(suites)==20 and sum(r['tests_reported']for r in suites.values())==498 and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B20 archived B19 actual documentary result')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY and prov['genuine_B19_check_sha256']==B19_CHECK_SHA and prov['genuine_B19_check_record_checkout']==old['checkout_head'],'B20 delivered pushed B19 entry identity')
    ck(prov['phase7B19_entry_consistency']==dict(original_hashes_matching=827,findings=307,audit_file_count=558,documentary_cases=498,self_test_suites=20,errors=[],erp_runtime_tests_executed=0),'B20 completed B19 entry counts')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB19ValidatorView(v)
    with historical_b19_inputs(view,frozen307,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_navigation_contract_audit_validator.py']
    record.update(historical_parser_cutoff='B19-not-current-B20-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_navigation_tests_07B20.py',actual_subprocess_argv=view.subprocess.actual,no_test_skips_or_global_subprocess_or_path_patch=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B19-307-not-current-state',
        phase_7B19_historical_input_mode='OWN307-exact308CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B19-test-child',
        phase_7B19_adapter_context=dict(entry_provenance='evidence/provenance-07B20.json',adapter_protected_artifacts_checked=553,current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,B19_parser_assertions_are_historical_preset_not_current_default=True))


def registry_preservation_errors(previous,current,raw,frozen):
    errors=[]
    if len(previous)!=307 or current[:307]!=previous:errors.append('B20 all307 exact fields/ALLnext_phase/evidence')
    if len(current)!=310 or[r.get('id')for r in current[307:]]!=NEW_IDS:errors.append('B20 only appended136..138')
    if(type(raw)is not bytes or type(frozen)is not bytes or not raw.startswith(frozen)or raw.startswith(b'\xef\xbb\xbf')or raw.count(b'\r\n')!=311 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n'))):errors.append('B20 exact307 raw prefix/311CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B20 raw/rows mismatch')
        except(UnicodeError,csv.Error):errors.append('B20 malformed registry')
    return errors


def group_row_errors(previous,current):
    g=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M);old,new=g(previous),g(current)
    if len(old)!=190 or new[:190]!=old:return ['B20 G01..190 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{i:02d}'for i in range(1,196)]:return ['B20 G191..195 only, exact order']
    return []


def caller_errors(current,literals):
    if len(current)!=7 or len(literals)!=7:return ['B20 exact seven selected qualified tokens required']
    errors=[];key=lambda r:(r['source_path'],str(r['call_line_start']),str(r['call_line_end']));lookup={key(r):r for r in literals}
    if len(lookup)!=7:errors.append('B20 distinct qualified token keys')
    if[r.get('consumer')for r in current]!=list(CALLER_SHAPES):errors.append('B20 named seven ordered consumers, not all barcode engines')
    for r in current:
        actual=lookup.get(key(r));shape=CALLER_SHAPES.get(r.get('consumer'))
        if actual is None or any(r.get(k)!=actual[k]for k in('call_text_sha256','inert_argument_expression')):errors.append('B20 literal argument/line/hash lineage')
        if shape!=tuple(r.get(k)for k in('reviewed_effect','quantity_handling','price_handling','scale_flag_handling')):errors.append('B20 declared per-consumer value/support boundaries')
        if r.get('source_path')!='SmartAuditERP/Form_WPF/'+r.get('consumer','')+'.xaml.cs':errors.append('B20 declared consumer/source path')
        for k in('entry_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(r.get(k),str)or not r[k].strip():errors.append('B20 caller missing responsibility:'+k)
        if r.get('runtime_status')!='not-executed':errors.append('B20 caller runtime overclaim')
    if {key(r)for r in current}!=set(lookup):errors.append('B20 all seven token keys exactly once')
    return errors


def current_link_errors(features,invariants,tests):
    errors=[]
    if(len(features),len(invariants),len(tests))!=(16,16,32):errors.append('B20 FE16/INV16/T32')
    for n,(fe,inv)in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):errors.append('B20 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or';'.join(t['id']for t in related)!=fe.get('acceptance_ids'):errors.append('B20 two explicit reverse-linked plans per feature')
        if n<=3 and(fe.get('finding_ids')!=NEW_IDS[n-1]or any(t.get('plan_kind')!='finding-specific'or t.get('finding_ids')!=NEW_IDS[n-1]for t in related)):errors.append('B20 three independent new roots/plans')
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=16 or len({r.get('acceptance_criterion')for r in tests})!=32:errors.append('B20 substantive distinct invariants/criteria')
    if any(r.get('status')!='not-executed'for r in tests):errors.append('B20 acceptance never executed')
    return errors


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B20 all14 residual identities required']
    errors=[]
    for old,new in zip(upstream,current):
        if(new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B19.csv'or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):errors.append('B20 exact upstream residual identity/hash/contracts')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B20 residual responsibility:'+k)
        if new.get('disposition')not in{'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':errors.append('B20 no residual approval/execution overclaim')
    return errors


def remaining_work_errors(work,splits):
    from validate_navigation_contract_part import remaining_work_errors as b19_errors
    adapted=[dict(r)for r in work]
    if len(adapted)!=10 or adapted[3].get('status')!='bounded-R4d-barcode-delivered-residuals-open':return ['B20 boundedR4d status, not whole7B closure']
    adapted[3]['status']='bounded-R4c-navigation-delivered-residuals-open'
    return ['B20 '+e for e in b19_errors(adapted,splits)]


def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','scanner_template_or_printer_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed','phase7C_started','phase8_authorized_or_started'):
        if w.get(k)is not False:errors.append('B20 false-only boundary:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B20 integer-zero boundary:'+k)
    for k in('B_R4d_bounded_not_whole7B_closure','prior_roots_not_assumed_remediated','unresolved_external_contracts_and_explicit_splits_retained'):
        if w.get(k)is not True:errors.append('B20 true-only boundary:'+k)
    for k in('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k))is not int or w[k]!=12:errors.append('B20 exact12 illustrative/lexical count:'+k)
    if w.get('phase')!='7B20-partial-static-barcode-contracts':errors.append('B20 witness phase')
    return errors+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def historical_record_errors(h):
    modes=h.get('historical_modes',[]);errors=[]
    if type(h.get('historical_mode_count'))is not int or h['historical_mode_count']!=25 or len(modes)!=25:return ['B20 exactly25 OWN records required']
    errors+=historical24_errors(dict(historical_mode_count=24,historical_modes=modes[:24],errors=h.get('errors')))
    last=modes[-1];child=last.get('historical_B19_child')or{}
    if last.get('mode')!='B19'or last.get('findings_total')!=307 or last.get('registry_used')!=SNAPSHOT or last.get('process_exit_code')!=0 or last.get('validation_errors')!=[]or last.get('original_project_hashes_matching')!=827:errors.append('B20 B19 historical OWN307 identity, not live310')
    if(last.get('audit_checker_self_test_cases_reported'),last.get('audit_checker_self_test_suite_count'))!=(498,20):errors.append('B20 genuine B19 aggregate498/20')
    if(child.get('tests_reported')!=36 or child.get('expected_tests')!=36 or child.get('process_exit_code')!=0 or child.get('result')!='passed'or child.get('historical_parser_cutoff')!='B19-not-current-B20-default'or child.get('all_original_cases_executed_unmodified')is not True or child.get('dedicated_child_launcher')!='tools/run_historical_navigation_tests_07B20.py'or child.get('no_test_skips_or_global_subprocess_or_path_patch')is not True):errors.append('B20 B19 all36 explicit historical child')
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(last.get(k))is not int or last[k]!=0:errors.append('B20 no historical ERP/SQL run')
    if not isinstance(last.get('stdout_sha256'),str)or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256'])is None:errors.append('B20 historical stdout hash')
    return errors


def expanded_source_evidence(value):
    """Expand SAME-file abbreviated ranges for strict scoped_evidence only.

    The raw registry/witness remains unchanged, as accepted by v.evidence().
    A new path resets the prefix; path-only/unknown tokens are not scope proof.
    """
    last=None;parts=[]
    for token in value.split(';'):
        token=token.strip()
        if not token:continue
        if ':'in token:
            last,ranges=token.rsplit(':',1)
            if not last or not ranges:raise ValueError('Empty source path/range')
            parts.append(token)
        elif last and re.fullmatch(r'\d+(?:[-–]\d+)?',token):parts.append(last+':'+token)
        else:raise ValueError('Source range without explicit or preceding same-file path')
    return ';'.join(parts)


def validate_source(v,row,scope):
    if'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B20 undeclared documentary sentinel:'+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B20 fabricated source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
        try:expanded=expanded_source_evidence(row['evidence'])
        except ValueError as e:v.check(False,'B20 invalid scoped source '+row['id']+':'+str(e));return
        v.scoped_evidence(expanded,scope,row['id']+' boundedB20',phase=7)


def extend_barcode_contracts(v,report,prov,frozen307):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[307:]
    for e in registry_preservation_errors(frozen307,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,e)
    ck(len({r['id']for r in current})==310,'B20 distinct310 IDs');ck(rows('evidence/historical-extensions-07B20.csv')==[],'B20 zero prior registry extensions')
    v.distributions(new,dict(High=1,Medium=2),dict(confirmed=3),'B20 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B20 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B20 heading/registry exact')
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k]is False,'B20 no implicit start:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k])is int and prov[k]==0,'B20 no ERP/SQL:'+k)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected};original={r['path']for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==20,'B20 selected20 bounded paths')
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-barcode-codec-consumer-label-slices-not-runtime-certified'and bool(r['focus']),'B20 selected scope identity/depth');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B20-{n:02d}'for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B20.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B20 incomplete CSV:'+r['id']);validate_source(v,r,scope)
            if'runtime_status'in r:ck(r['runtime_status']=='not-executed','B20 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B20-','INV7B20-','P7B20T-')]
    for e in current_link_errors(fe,inv,tests):ck(False,e)
    v.proposed_tests(tests,'7B20');fids,iids,tids=[{r['id']for r in pool}for pool in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['BC7B20-'],fids,'feature_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B20 '+label)
    for r in tables['RC7B20-']:
        fs=[f for f in fe if f['id']in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        expected=';'.join(dict.fromkeys(x for f in fs if f['evidence']!=DOCUMENTARY for x in f['evidence'].split(';')))or DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==expected,'B20 RC exact source/FE lineage');v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for e in residual_errors(tables['RS7B20-'],rows('evidence/residual-disposition-07B19.csv'))+remaining_work_errors(tables['RW7B20-'],tables['SP7B20-']):ck(False,e)
    hids={r['id']for r in tables['H7B20-']};sids={r['id']for r in tables['SP7B20-']};v.related(tables['RS7B20-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B20-'],hids,'handoff_ids')
    for r in tables['H7B20-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B20 no invented handoff approval')
    for r in tables['Q7B20-']:ck(r['status']=='unanswered-no-secrets-requested','B20 no invented policy answer')
    for n,r in enumerate(tables['BK7B20-'],1):ck(r['prior_backlog_id']==f'BK7B19-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B20 backlog ancestry/uncompleted')
    ck([r['status']for r in tables['BK7B20-'][2:6]]==['not-started']*4,'B20 C axes remain unstarted')
    ad=tables['AD7B20-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids');ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B20 three adjudicated causes only')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B20 adjudication source chain')
    ck(all(r['comparison_depth']=='all307-registry-titles-classifications-plus-selected-nearest-source-chains-not-all-historical-bodies'for r in ad),'B20 honest dedup depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv'for n in range(2,8)]+[f'review-scope-07B{n}.csv'for n in range(1,20)]
    before={r['path']for name in prior_names for r in rows(name)};paths=set(scope)
    ck((len(before),len(paths&before),len(paths-before),len(before|paths),len(original-(before|paths)))==(410,20,0,410,417),'B20 selected-path counts not coverage percentage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B20.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B19.md','evidence/split-register-07B19.csv']and decision['selected_upstream_split']=='SP7B19-03'and decision['entry']==ENTRY and decision['bookkeeping']==dict(selected_paths=20,prior_union=410,overlap=20,new=0,union=410,complement=417,complement_kinds={'source':352,'generated-artifact':61,'project-or-resource':4}),'B20 authority/reasoned scope')
    ck(v.sha(v.AUDIT/'evidence/barcode-contract-witnesses-07B20.json')==WITNESS_SHA,'B20 genuine first witness capture')
    witness,match=v.recompute('evidence/barcode-contract-witnesses-07B20.json','tools/check_barcode_contract_witnesses.py')
    for e in witness_metadata_errors(witness):ck(False,e)
    ck(witness['errors']==[],'B20 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B20-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B20-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,12);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B20 witness not runtime/standards acceptance');validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B20 lexical read',phase=7)
    discovery=witness['qualified_literal_discovery'];ck(discovery['not_complete_callgraph_or_capability_census']is True and discovery['not477_body_reviews']is True and discovery['source_csharp_paths_lexically_scanned']==477,'B20 census is lexical only')
    for e in caller_errors(tables['BC7B20-'],discovery['literal_calls']):ck(False,e)
    ck([r['source_kind']for r in tables['DC7B20-']]==['unit-exact','alias-exact','Wscale1','Wscale2','Wscale3'],'B20 decoder five declared source/mode contracts')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B20.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B20 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B20.md','PHASE-07-REMAINING-07B20.md','7B21','غير مأذونة','ac20e31','10ba215')),'B20 shared index current boundary:'+name)
    hist_path='evidence/historical-mode-verification-07B20.json';ck(HISTORICAL_RUN_SHA is not None and(v.AUDIT/hist_path).is_file(),'B20 historical25 genuinely captured')
    if(v.AUDIT/hist_path).is_file():
        ck(v.sha(v.AUDIT/hist_path)==HISTORICAL_RUN_SHA,'B20 actual historical25 identities');historical=v.json.loads(v.read(v.AUDIT/hist_path))
        for e in historical_record_errors(historical):ck(False,e)
        ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD and historical['branch']==v.BRANCH,'B20 historical modes source/entry')
        report['phase_7B20_executed_historical_documentary_modes']=dict(record=hist_path,sha256=HISTORICAL_RUN_SHA,modes_reported=25,all_documentary_exit_codes_zero=True,B19_OWN307_raw308CRLF_and_historical36_child=True,null_means_aggregate_not_reported_not_zero=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_barcode_contract_witnesses.py','validate_barcode_contract_part.py','run_historical_navigation_tests_07B20.py','test_barcode_contract_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B20 syntax:'+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_barcode_contract_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None;passed=run.returncode==0 and count==32;ck(passed,'B20 32 documentary self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=32,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools;report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n)for n in['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B20-310-bounded-R4d-barcode-contracts-not-7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,21))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B21-proposed-R4e-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=138,phase_7B20=3,total_open_not_remediated=310,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:20,'phase_7B20_prior_union':410,'phase_7B20_overlap_with_prior_union':20,'phase_7B20_new_paths':0,'unique_union_not_line_or_execution_coverage':410,'inventory_only_no_selected_scope':417})
    report['phase_7B19_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=553,historical_check_record_overwritten=False,genuine_b19_stdout_sha256_unchanged=B19_CHECK_SHA,partial7B20_append_only_extensions=[],all307_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B20_barcode_trace_limits']=dict(literal_qualified_decoder_calls=7,named_consumer_paths=7,source_csharp_paths_lexically_scanned_not_body_reviews=477,selected_label_projection_boundaries=2,decoder_source_mode_contracts=5,current_FE_or_documentary_contracts=16,invariants_not_executed_tests=16,acceptance_plans_not_executed=32,residual_inputs=14,explicit_further_static_splits=3,B_R4d_delivered_not_whole_R4_SP03_or7B_closure=True,retained_potential_roots_not_promoted=['P4-014','P7-132'],C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B20_illustrations_not_erp_tests=12,phase_7B20_lexical_checks_not_erp_tests=12,phase_7B20_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),phase_7B20_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only bounded7B20/R4d:553 protected artifacts/307 EXACT fields including ALLnext_phase/evidence/raw308CRLFprefix/G190/3freezes/827 originals. Three local causes136..138; no historical registry extensions. Successful scale numeric outputs discarded by Sale/Purch/IO, ambiguous joined unit from base-prefix OR, parse-failure→zero loses health and reaches POS defaults/partial value. Confirmed source instructions, not actual scanner/SQL/.NET/DTO/save or printed artifact. POS positive-output handling is counterevidence, not blanket correctness. Transfer/Safe selection-only intent unresolved; not automatically included in136.037/036/026/028/014 and financial/security/identity/lifecycle roots retained;014/132 potential unchanged. Seven qualified tokens from477 lexical source scans are not477 body reviews/allcallgraph/capability census;20 previously scoped paths only bounded slices, union410/complement417 not a completion percentage.16FE/INV32 acceptance plans NOT executed;14 residuals/3 splits/6H/Q not external approvals. R4e/B21 proposed;7B/7 partial;6C axes unstarted;8 unauthorized. B19 OWN307/exact308CRLF/indexes in memory and ALL36 originals in explicit historical child presetB19; current B20 CLI/default independently tested32 cases. Earlier B18 child all28 remains historical. No protected edits/skips/global Path or subprocess patch/disk overlay/rebaseline/archive rewrite. Source10ba/completedB19push-entryac20e31/genuineB19stdoutee393a7 distinct.12 ASCII/Decimal manual models and12 lexical/50 bounded reads are not C#/VB/WPF/SQL/UtilitiesProj/REPX/culture/checksum/symbology/scanner/printer/business acceptance. B10 additive10vs120 erratum retained. No app import/build/provider/external service/business data/secrets/remediation/operational measurement. next_phase8 planning is not permission.'
