#!/usr/bin/env python3
"""PARTIAL7B18/R4b documentary direct-caller requests, NEVER ERP acceptance.

495 protected artifacts/300 EXACT rows and ALLnext_phase/evidence/rawprefix/
G01–180/827 originals. B17 uses OWN300/exact301CRLF and exact shared indexes
in memory; no protected edits/global Path patch/disk overlay/rebaseline or
archive rewrite. CL19/10 and GE10 are lexical lineage, NOT all callgraph,
477 body reviews or a feature census. R4c proposed with explicit residuals.
7B/7 partial;7C unstarted;8 unauthorized. No app import/build/C#/SQL/WPF/
provider/interpreter/device/printer/real data/remediation/operational measure.
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
from urllib.parse import unquote, urlsplit
from validate_financial_report_part import historical_b1_inputs, bidirectional_errors
from validate_statement_contract_part import arithmetic_erratum_errors

SCOPE_FILE='review-scope-07B18.csv'
PART_DOCS=('PHASE-07B18.md','CALLER-REQUEST-CONTRACTS-07B18.md','VALIDATION-07B18.md','PHASE-07-REMAINING-07B18.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B17.csv'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B17.json'
SNAPSHOT_SHA='00f72d7747d431df1ca360960b62603c4ad666b8488eed62f65efe180fa033d7'
SHARED_SHA='f240e93dad10e82a99a2ec9f342886be9ff19f905d1f6571cfe669550240f00f'
PROVENANCE_SHA='e5bc13038b48ffbb406b34a74d08f8b87b941eec08b4099b8dc9db1b9261eff9'
B17_CHECK_SHA='c7b15c520485b017d3f78f9220343ddd819b6ba245d99040d0b87ff4dc2413b6'
WITNESS_SHA='86eb7a2aa3b66a9f5fa2726a81d45c36a667099366c04d8ed1a9f517c03b6060'
HISTORICAL_RUN_SHA='aef815ad43220fd732c535eea5033e6c53ff2a16048318eb3c5f4c3681bfadbd'
ENTRY='12d2e4b1bc566a860643b8459b16cbc85a6d2c3d'
DOCUMENTARY='none-documentary-metadata'
TABLE_SPECS=(('caller-request-ledger','CL7B18-',19),('general-entry-ledger','GE7B18-',10),
 ('feature-implementation-matrix','FE7B18-',14),('report-invariants','INV7B18-',14),
 ('acceptance-tests','P7B18T-',24),('report-reconciliation','RC7B18-',4),
 ('root-adjudication','AD7B18-',6),('residual-disposition','RS7B18-',14),
 ('split-register','SP7B18-',3),('handoffs','H7B18-',6),('questions','Q7B18-',6),
 ('continuation-backlog','BK7B18-',10),('remaining-workplan','RW7B18-',10))
SENTINELS={f'{prefix}{n:02d}'for prefix,indices in(
 ('FE7B18-',[10,13,14]),('INV7B18-',[10,13,14]),('P7B18T-',[15,18,19,20,21,22,23,24]),
 ('H7B18-',range(1,7)),('Q7B18-',range(1,7)),('SP7B18-',range(1,4)),
 ('RS7B18-',[1,2,4,5,6,7,8,9,11,12,13]),('AD7B18-',[6]),('RC7B18-',[4]))for n in indices}
ROLE_COUNTS={'all-party-item-command':10,'selected-party-id-omitted':1,'kind-mismatch':3,
 'conditional-kind-mismatch':4,'matching-kind-counterevidence':1}


def row_sha(row):
    return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@contextmanager
def historical_b17_inputs(v, frozen300, texts, raw):
    """Only the exact logical registry bytes; restore identities on all exits."""
    if len(frozen300)!=300 or len({r['id']for r in frozen300})!=300:
        raise ValueError('Exactly300 distinct historical rows required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except (UnicodeError,csv.Error)as e:raise ValueError('Malformed frozen300 registry')from e
    if (parsed!=frozen300 or raw.count(b'\r\n')!=301 or not raw.endswith(b'\r\n')
            or any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n'))):
        raise ValueError('Exact frozen300 bytes/rows/CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen300,texts):yield
    finally:v.AUDIT=original


def validate_frozen_b17(v,report,prior,frozen299,prov,frozen300):
    """Reuse protected B17 with OWN inputs, never live302 or B16's299."""
    for name,digest in(('evidence/provenance-07B18.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),
                       (SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B17.json',B17_CHECK_SHA)):
        v.check(v.sha(v.AUDIT/name)==digest,'B18 immutable entry: '+name)
    v.check(prov['historical_artifact_count']==495 and len(frozen300)==300,'B18 entry counts')
    v.check(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
        and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B18 entry snapshots')
    for name,digest in prior['historical_artifact_sha256'].items():
        v.check(prov['historical_artifact_sha256'].get(name)==digest,'468-to495 protected continuity: '+name)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B17.json'))
    v.check(saved['checkout_head']=='de0e7cf986152d3a1ce5d2886583ad2bd54d0c07'
        and saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==300
        and saved['original_project_hashes_matching']==827
        and saved['historical_artifact_sha256']==prior['historical_artifact_sha256']
        and saved['validation']['current_output_record_pending_first_write_not_placeholder']is False,'B17 genuine stdout identity')
    v.check(prov['genuine_B17_check_sha256']==B17_CHECK_SHA
        and prov['genuine_B17_check_record_checkout']==saved['checkout_head']
        and prov['prior_provenance_B17_sha256']==v.sha(v.AUDIT/'evidence/provenance-07B17.json'),'B18 previous stdout/provenance')
    v.check(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B18 completed B17 push at entry')
    v.check(prov['phase7B17_entry_consistency']==dict(original_hashes_matching=827,findings=300,
        phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,18))+'-partial-not-complete7B-or7',
        audit_file_count=500,errors=[],erp_runtime_tests_executed=0),'B18 previous delivered context')
    from validate_consolidation_part import extend_consolidation
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b17_inputs(v,frozen300,texts,(v.AUDIT/SNAPSHOT).read_bytes()):
        extend_consolidation(v,report,prior,frozen299)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B17-300-not-current-state',
        phase_7B17_historical_input_mode='frozen300-rows-exact301CRLF-bytes-and-exact-indexes-in-memory',
        phase_7B17_adapter_context=dict(entry_provenance='evidence/provenance-07B18.json',
            adapter_protected_artifacts_checked=495,current_registry_and_shared_indexes_not_inputs=True,
            archived_stdout_not_rewritten_after_push=True))


def registry_preservation_errors(previous,current,raw,frozen_raw):
    errors=[]
    if len(previous)!=300 or current[:300]!=previous:errors.append('B18 all300 exact historical rows/ALLnext_phase/evidence')
    if len(current)!=302 or [r.get('id')for r in current[300:]]!=['P7-129','P7-130']:errors.append('B18 exactly two appended roots129/130')
    if (type(raw)is not bytes or type(frozen_raw)is not bytes or not raw.startswith(frozen_raw)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=303 or not raw.endswith(b'\r\n')
            or any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n'))):
        errors.append('B18 noBOM/exact raw300 prefix/current303CRLF')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B18 rows/raw bytes disagree')
        except (UnicodeError,csv.Error):errors.append('B18 malformed raw bytes')
    return errors


def group_row_errors(previous,current):
    gr=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    return []if len(gr(previous))==180 and gr(current)[:180]==gr(previous)else['B18 historical G01–180 exact rows changed']


def current_link_errors(features,invariants,tests):
    errors=[]
    if (len(features),len(invariants),len(tests))!=(14,14,24):errors.append('B18 current FE/INV/T counts')
    for fe,inv in zip(features,invariants):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):
            errors.append('B18 invariant/feature exact lineage')
        expected=';'.join(t['id']for t in tests if t['feature_ids']==fe['id'])
        if not expected or expected!=fe.get('acceptance_ids'):errors.append('B18 acceptance reverse lineage')
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=14 or len({r.get('acceptance_criterion')for r in tests})!=24:
        errors.append('B18 distinct substantive invariant/criterion contracts')
    if any(t.get('status')!='not-executed'for t in tests):errors.append('B18 acceptance remains unexecuted')
    for n,t in enumerate(tests[:7]):
        if t.get('finding_ids')!=('P7-129'if n<5 else'P7-130')or t.get('plan_kind')!='finding-specific':
            errors.append('B18 five type/two ID independent root plans')
    return errors


def ledger_errors(current,expected,scanned):
    """Compare exact literal tokens/locations/hashes, not C# semantic reachability."""
    errors=[]
    if len(current)!=19 or len(expected)!=19 or scanned!=477:errors.append('B18 CL19/excluded-scan477')
    if len({r.get('source_path')for r in current})!=10:errors.append('B18 ten caller paths')
    keys=[(r.get('source_path'),r.get('call_line_start'),r.get('call_line_end'))for r in current]
    if len(keys)!=len(set(keys)):errors.append('B18 duplicate literal callsite')
    for row,actual in zip(current,expected):
        try:args=json.loads(row['lexical_args_json'])
        except (ValueError,KeyError):args=None
        if any(row.get(k)!=str(actual[k])for k in('source_path','call_line_start','call_line_end','call_text_sha256'))or args!=actual.get('lexical_args'):
            errors.append('B18 exact direct-call lexical lineage')
        if not isinstance(args,list)or len(args)!=4 or row.get('forwarded_party_id')!=args[2]or row.get('forwarded_party_kind')!=args[3]:
            errors.append('B18 four inert args/ID-kind columns')
        if row.get('runtime_status')!='not-executed'or not row.get('reachability_limit'):
            errors.append('B18 callsite execution/reachability overclaim')
    if dict(collections.Counter(r.get('party_mode')for r in current))!=ROLE_COUNTS:errors.append('B18 context role distribution')
    for r in current:
        roots=r.get('finding_ids','').split(';');mode=r.get('party_mode')
        expected_roots={'P7-130'}if mode=='selected-party-id-omitted'else{'P7-129'}if mode in{'kind-mismatch','conditional-kind-mismatch','matching-kind-counterevidence'}else{'H7B18-03'}if r.get('source_path','').endswith('/frmInvInOutput.xaml.cs')else{'P7-122','P7-059'}
        if set(roots)!=expected_roots:errors.append('B18 callsite root/context mismatch')
    return errors


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B18 exactly14 named upstream residuals required']
    errors=[]
    for old,new in zip(upstream,current):
        if (new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B17.csv'
                or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):
            errors.append('B18 exact upstream residual lineage')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B18 missing residual responsibility: '+k)
        if new.get('disposition')not in{'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':
            errors.append('B18 residual approval/execution overclaim')
    return errors


def remaining_work_errors(work,splits):
    from validate_consolidation_part import remaining_work_errors as previous_errors
    # Reuse the previous contract only after replacing today's one advanced status IN MEMORY.
    adapted=[dict(r)for r in work]
    if len(adapted)==10 and adapted[3].get('status')=='bounded-R4b-direct-callers-delivered-residuals-open':
        adapted[3]['status']='bounded-consolidation-delivered-residuals-open'
    else:return ['B18 R4b status required; not wholeR4 closure']
    return ['B18 '+e for e in previous_errors(adapted,splits)]


def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used',
             'spreadsheet_or_formula_interpreter_executed','phase7C_started','phase8_authorized_or_started'):
        if w.get(k)is not False:errors.append('B18 false-only boundary: '+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B18 integer-zero boundary: '+k)
    for k in('B_R4b_bounded_not_whole7B_closure','prior_roots_not_assumed_remediated','unresolved_external_contracts_and_explicit_splits_retained'):
        if w.get(k)is not True:errors.append('B18 true-only boundary: '+k)
    for k in('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k))is not int or w[k]!=12:errors.append('B18 documentary witness count: '+k)
    if w.get('phase')!='7B18-partial-static-direct-caller-requests':errors.append('B18 witness phase')
    return errors+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def validate_source(v,row,scope):
    if 'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B18 undeclared documentary sentinel: '+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B18 fabricated source for documentary row: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' boundedB18',phase=7)


def extend_caller_requests(v,report,prov,frozen300):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[300:]
    ck(v.sha(v.AUDIT/'evidence/caller-request-witnesses-07B18.json')==WITNESS_SHA,'B18 genuine witness first capture')
    historical_path='evidence/historical-mode-verification-07B18.json'
    ck(v.sha(v.AUDIT/historical_path)==HISTORICAL_RUN_SHA,'B18 genuine historical-mode capture')
    historical=v.json.loads(v.read(v.AUDIT/historical_path))
    modes=historical['historical_modes']
    ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD and historical['branch']==v.BRANCH
        and historical['historical_mode_count']==len(modes)==23 and historical['errors']==[], 'B18 historical-mode identity/count')
    ck([r['mode']for r in modes]==['phase'+str(n)for n in range(2,7)]+['A']+['B'+str(n)for n in range(1,18)],'B18 historical-mode order')
    ck(all(r['process_exit_code']==0 and r['validation_errors']==[] and r['original_project_hashes_matching']==827
        and r['erp_runtime_tests_executed']==r['sql_or_external_service_tests_executed']==0 for r in modes),'B18 historical-mode documented results')
    report['phase_7B18_executed_historical_documentary_modes']=dict(record=historical_path,sha256=HISTORICAL_RUN_SHA,
        modes_reported=len(modes),all_documentary_exit_codes_zero=all(r['process_exit_code']==0 for r in modes),not_original_metric_replay_or_erp_tests=True)
    for error in registry_preservation_errors(frozen300,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    ck(len({r['id']for r in current})==302,'B18 distinct302 IDs')
    ck(rows('evidence/historical-extensions-07B18.csv')==[],'B18 zero historical extensions')
    v.distributions(new,{'Medium':2},{'confirmed':2},'B18 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B18 finding/authorization state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B18 heading/registry')
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k]is False,'B18 no implicit runtime/phase: '+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k])is int and prov[k]==0,'B18 zero runtime: '+k)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected}
    ck(len(scope)==len(selected)==29,'B18 selected29 paths')
    original={r['path']for r in rows('evidence/inventory.csv')}
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-request-trace-slices-not-runtime-certified'and bool(r['focus']),'B18 scope selection')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B18-{i:02d}'for i in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B18.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B18 incomplete CSV cells: '+r['id'])
            validate_source(v,r,scope)
            if 'runtime_status'in r:ck(r['runtime_status']=='not-executed','B18 runtime overclaim: '+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B18-','INV7B18-','P7B18T-')]
    for error in current_link_errors(fe,inv,tests):ck(False,error)
    v.proposed_tests(tests,'7B18')
    fids,iids,tids=[{r['id']for r in data}for data in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B18 '+label)
    for r in tables['RC7B18-']:
        associated=[f for f in fe if f['id']in r['feature_ids'].split(';')]
        unique=lambda key:';'.join(dict.fromkeys(x for f in associated for x in f[key].split(';')))
        refs=[f['evidence']for f in associated if f['evidence']!=DOCUMENTARY]
        expected=';'.join(dict.fromkeys(x for s in refs for x in s.split(';')))if refs else DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==expected,'B18 RC exact FE lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for error in residual_errors(tables['RS7B18-'],rows('evidence/residual-disposition-07B17.csv'))+remaining_work_errors(tables['RW7B18-'],tables['SP7B18-']):ck(False,error)
    hids={r['id']for r in tables['H7B18-']};sids={r['id']for r in tables['SP7B18-']}
    v.related(tables['RS7B18-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B18-'],hids,'handoff_ids')
    for r in tables['H7B18-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B18 no invented approval')
    for r in tables['Q7B18-']:ck(r['status']=='unanswered-no-secrets-requested','B18 no invented policy answer')
    for n,r in enumerate(tables['BK7B18-'],1):ck(r['prior_backlog_id']==f'BK7B17-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B18 backlog ancestry/not complete')
    ck([r['status']for r in tables['BK7B18-'][2:6]]==['not-started']*4,'B18 no accidental C start')
    ad=tables['AD7B18-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==['P7-129','P7-130'],'B18 two adjudicated roots')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B18 adjudication source chain')
    ck(all(r['comparison_depth']=='all300-titles-classifications-plus-selected-nearest-source-chains-not-all-historical-chains'for r in ad),'B18 dedup depth not all chains')
    previous_scopes=[rows('review-scope.csv'if n==1 else f'review-scope-{n:02d}.csv')for n in range(1,7)]
    previous_scopes+=[rows('review-scope-07.csv')]+[rows(f'review-scope-07B{n}.csv')for n in range(1,18)]
    before={r['path']for s in previous_scopes for r in s};paths=set(scope)
    ck((len(before),len(paths&before),len(paths-before),len(before|paths),len(original-(before|paths)))==(399,20,9,408,419),'B18 path bookkeeping not percentage/feature coverage')
    witness,match=v.recompute('evidence/caller-request-witnesses-07B18.json','tools/check_caller_request_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B18 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B18-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B18-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,12);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B18 witness boundary')
            validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B18 lexical read',phase=7)
    discovery=witness['direct_literal_discovery']
    ck(discovery['not_complete_callgraph_or_feature_census']is True,'B18 literal census boundary')
    for error in ledger_errors(tables['CL7B18-'],discovery['literal_calls'],discovery['original_CSharp_files_excluding_bin_obj_scanned_not_body_reviews']):ck(False,error)
    ge=tables['GE7B18-'];ck(collections.Counter(r['report_family']for r in ge)=={'detailed':8,'aggregate':2},'B18 general-entry family split')
    ck(all(r['source_publication_order']==('query-before-ShowDialog'if r['report_family']=='detailed'else'ShowDialog-with-ItemId-no-explicit-query')for r in ge),'B18 general-entry order boundary')
    patterns=[(PART_DOCS[0],r'^\| (AD7B18-\d{2}) \|',ad),(PART_DOCS[1],r'^\| (CL7B18-\d{2}) \|',tables['CL7B18-']),
      (PART_DOCS[1],r'^\| (GE7B18-\d{2}) \|',ge),(PART_DOCS[1],r'^\| (FE7B18-\d{2}) —',fe),
      (PART_DOCS[1],r'^\| (INV7B18-\d{2}) \|',inv),(PART_DOCS[1],r'^### (RC7B18-\d{2}) —',tables['RC7B18-']),
      (PART_DOCS[2],r'^\| (P7B18T-\d{2}) \|',tests),(PART_DOCS[3],r'^\| (RS7B18-\d{2}) \|',tables['RS7B18-']),
      (PART_DOCS[3],r'^\| (SP7B18-\d{2}) \|',tables['SP7B18-']),(PART_DOCS[3],r'^\| (RW7B18-\d{2}) \|',tables['RW7B18-'])]
    for name,pattern,pool in patterns:ck(re.findall(pattern,v.read(v.AUDIT/name),re.M)==[r['id']for r in pool],'B18 Markdown IDs: '+name)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for error in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,error)
    ck(re.findall(r'^\| (G-\d{2,3}) \|',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)==[f'G-{n:02d}'for n in range(1,185)],'B18 G181–184 only')
    pending=False
    source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B18.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B18 broken link: '+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B18.md','PHASE-07-REMAINING-07B18.md','7B19','غير مأذونة','12d2e4b','10ba215')),'B18 live index boundary: '+name)
    tools=['check_caller_request_witnesses.py','validate_caller_request_part.py','test_caller_request_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B18 syntax: '+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_caller_request_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None
    passed=run.returncode==0 and count==28;ck(passed,'B18 documentary self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=28,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name)for name in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B18-302-bounded-R4b-direct-caller-requests-not-7B-or-runtime-closure',
        phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,19))+'-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B19-proposed-R4c-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],
        registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=130,phase_7B18=2,total_open_not_remediated=302,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:29,'phase_7B18_prior_union':399,'phase_7B18_overlap_with_prior_union':20,'phase_7B18_new_paths':9,'unique_union_not_line_or_execution_coverage':408,'inventory_only_no_selected_scope':419})
    report['phase_7B17_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=495,historical_check_record_overwritten=False,genuine_b17_stdout_sha256_unchanged=B17_CHECK_SHA,partial7B18_append_only_extensions=[],all300_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B18_request_trace_limits']=dict(literal_calls=19,caller_paths=10,original_CSharp_files_lexically_scanned_not_body_reviews=477,general_entries=10,general_entries_query_before_dialog=8,general_entries_aggregate_not_detailed=2,current_features_or_documentary_contracts_not_completed_features=14,current_invariants_not_executed_tests=14,acceptance_plans_not_executed=24,residual_inputs=14,explicit_further_static_splits=3,B_R4b_delivered_not_whole_R4_or7B_closure=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B18_illustrations_not_erp_tests=12,phase_7B18_lexical_checks_not_erp_tests=12,phase_7B18_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),phase_7B18_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only documentary B18/R4b:495 protected artifacts/300 EXACT historical rows/ALLnext_phase/evidence/rawCRLFprefix/G01..180/three entry freezes/original827. No historical evidence extensions. Two static local causes129 wrong caller party kind with positiveID and130 client-labelled command drops partyID=-1. Wrong-kind conditional missing lookup selection is independent of122 all-store/059 TOP1 ASC/058 aggregate omitted predicate/061 DocumentRef. Pure1/2 and lookup-ready/health assumptions; shared3 and correctInvPurch2->2 counterevidence retained.19 direct literal calls/10 paths from477 original CSharp text files excluding bin/obj is NOT an AST/callgraph or477 body reviews or all features. GE10 has8 detailed ShowResult-before-ShowDialog and2 aggregate routes; WPF timing/DateTimeBox/ACL/runtime correctness NOT inferred.29 selected paths/20overlap/9new/union408/complement419 are not feature denominator;455 historical FE metadata not rereviewed.14 current contracts/invariants,24 acceptance plans all not-executed,14 residual dispositions,3 explicit further splits,6 external H/Q unresolved. R4c/B19 proposed, not wholeR4/7B/7;6 C axes unstarted;8 unauthorized. Historical B17 OWN300/exact301CRLF/indexes in memory, no global Path patch/protected helper edits/disk overlay/rebaseline/archive rewrite. Actual build_cli_parser/defaultB18 tested; historical B17-named compatibility descriptor PHASE7_CURRENT_CLI used as base, API main defaultB15 preserved. Source10ba, completed B17push/entry12d2e4b, genuine B17stdoutcheckoutde0e7cf are distinct; archives never rewritten after push.12 independent models+12 lexical checks+28 synthetic documentary cases; no ERP acceptance. Additive B10 erratum10vs120 retained, not all historical prose certified. No app import/build/C#/SQL/VB/WPF/SDK/REPX/Office/COM/HTML/formula interpreter/provider/device/printer/business export/application shell/real data/secrets/remediation/operational measurement.7B/7 partial;7C unstarted;8 unauthorized;next_phase8 is planning not authorization.')
