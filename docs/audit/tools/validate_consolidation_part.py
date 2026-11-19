#!/usr/bin/env python3
"""PARTIAL7B17/B-R4a documentary consolidation, NEVER ERP acceptance.

468 protected artifacts,299 EXACT prior rows/CRLF bytes/ALLnext_phase, G01–176,
827 original path/hashes. Frozen B16 gets OWN299/current-then indexes and raw
300CRLF bytes IN MEMORY. No protected helper edits, global pathlib patches,
disk overlays/rebaseline, archive rewrites, application execution/remediation.
455 frozen FE metadata rows !=455 unique features or new source reviews.
R4a consolidation plus selected18-path traces !=whole7B closure; R4b/B18 is
proposed with3 explicit splits;7C unstarted,8 unauthorized. Counts not sessions.
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

SCOPE_FILE='review-scope-07B17.csv'
PART_DOCS=('PHASE-07B17.md','REPORTS-CONSOLIDATION-07B17.md','VALIDATION-07B17.md','PHASE-07-REMAINING-07B17.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B16.csv'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B16.json'
SNAPSHOT_SHA='7411a77c6aec4a314190b0ffff7a9790cd1ede6904bf96c288a79a40afa80647'
SHARED_SHA='523b1544f664d3d0762c2c9922c7802b95b23cbf1554daef1b0283cb438a2ff9'
PROVENANCE_SHA='9d9201ebeeaa10952bf0e8aa3c50c9cb407a42810aac5afcffba00f740aa6042'
B16_CHECK_SHA='f5f1c000217736cf0572e44ad553f8fee35b283e7e79af00f5590ae061ad16d9'
ENTRY='de0e7cf986152d3a1ce5d2886583ad2bd54d0c07'
DOCUMENTARY='none-documentary-metadata'
FE_COUNTS=(33,32,29,36,35,26,31,28,20,23,23,25,27,31,32,24)
TABLE_SPECS=(('feature-implementation-matrix','FE7B17-',12),('report-invariants','INV7B17-',12),
 ('acceptance-tests','P7B17T-',18),('report-reconciliation','RC7B17-',4),
 ('root-adjudication','AD7B17-',6),('residual-disposition','RS7B17-',14),
 ('split-register','SP7B17-',3),('handoffs','H7B17-',6),('questions','Q7B17-',6),
 ('continuation-backlog','BK7B17-',10),('remaining-workplan','RW7B17-',10),
 ('aggregation-contracts','FC7B17-',16))
SENTINELS={f'{prefix}{n:02d}'for prefix,indices in (
 ('FE7B17-',range(8,13)),('INV7B17-',range(8,13)),('P7B17T-',range(12,19)),
 ('H7B17-',range(1,7)),('Q7B17-',range(1,7)),('SP7B17-',range(1,4)),
 ('RS7B17-',[1,2,3,4,5,6,7,9,11,12]),('AD7B17-',[6]),('RC7B17-',[3,4]))for n in indices}


def row_sha(row):
    return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@contextmanager
def historical_b16_inputs(v, frozen299, texts, raw):
    """Exact one logical file only; all objects restored on normal/error/nesting."""
    if len(frozen299)!=299 or len({r['id']for r in frozen299})!=299:
        raise ValueError('Exactly299 distinct historical rows required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM bytes required')
    try:
        parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except (UnicodeError,csv.Error)as e:
        raise ValueError('Malformed frozen299 registry')from e
    if (parsed!=frozen299 or raw.count(b'\r\n')!=300 or not raw.endswith(b'\r\n')
            or any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n'))):
        raise ValueError('Exact frozen299 bytes/rows/CRLF disagree')
    original=v.AUDIT
    target=(original/'findings.csv').resolve()

    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen299,texts):
            yield
    finally:
        v.AUDIT=original


def validate_frozen_b16(v,report,prior,frozen298,prov,frozen299):
    for name,digest in [('evidence/provenance-07B17.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),
            (SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B16.json',B16_CHECK_SHA)]:
        v.check(v.sha(v.AUDIT/name)==digest,'B17 immutable entry: '+name)
    v.check(prov['historical_artifact_count']==468 and len(frozen299)==299,'B17 entry counts')
    v.check(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA
        and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B17 entry snapshots')
    for name,digest in prior['historical_artifact_sha256'].items():
        v.check(prov['historical_artifact_sha256'].get(name)==digest,'440-to468 protected continuity: '+name)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B16.json'))
    v.check(saved['checkout_head']=='16f3fd42f24183db5906bd06517b8dc10a7b9b36'
        and saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==299
        and saved['original_project_hashes_matching']==827
        and saved['historical_artifact_sha256']==prior['historical_artifact_sha256']
        and saved['validation']['current_output_record_pending_first_write_not_placeholder']is False,'B16 genuine stdout identity')
    v.check(prov['genuine_B16_check_sha256']==B16_CHECK_SHA
        and prov['genuine_B16_check_record_checkout']==saved['checkout_head']
        and prov['prior_provenance_B16_sha256']==v.sha(v.AUDIT/'evidence/provenance-07B16.json'),'B17 previous record/provenance')
    v.check(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY,'B17 completed B16 push at entry')
    v.check(prov['phase7B16_entry_consistency']==dict(original_hashes_matching=827,findings=299,
        phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,17))+'-partial-not-complete7B-or7',
        audit_file_count=473,errors=[],erp_runtime_tests_executed=0),'B17 prior delivered context')
    from validate_shared_contract_part import extend_shared_contracts
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b16_inputs(v,frozen299,texts,(v.AUDIT/SNAPSHOT).read_bytes()):
        extend_shared_contracts(v,report,prior,frozen298)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B16-299-not-current-state',
        phase_7B16_historical_input_mode='frozen299-rows-exact300CRLF-bytes-and-exact-indexes-in-memory',
        phase_7B16_adapter_context=dict(entry_provenance='evidence/provenance-07B17.json',
            adapter_protected_artifacts_checked=468,current_registry_and_shared_indexes_not_inputs=True,
            archived_stdout_not_rewritten_after_push=True))


def registry_preservation_errors(previous,current,raw,frozen_raw):
    errors=[]
    if len(previous)!=299 or current[:299]!=previous:
        errors.append('B17 all299 exact historical rows/ALLnext_phase/evidence')
    if len(current)!=300 or [r.get('id')for r in current[299:]]!=['P7-128']:
        errors.append('B17 single appended root128')
    if (type(raw)is not bytes or type(frozen_raw)is not bytes or not raw.startswith(frozen_raw)
            or raw.startswith(b'\xef\xbb\xbf') or raw.count(b'\r\n')!=301
            or not raw.endswith(b'\r\n') or any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n'))):
        errors.append('B17 noBOM/exact raw299 prefix/current301CRLF')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:
                errors.append('B17 current rows/raw bytes disagree')
        except (UnicodeError,csv.Error):
            errors.append('B17 malformed current raw bytes')
    return errors


def prior_disposition(status,title):
    """Documentary routing, NOT a semantically approved owner/policy mapping.

    Preserve the original status/depth in the ledger. Status selects the broad
    category; title-token heuristics only choose a provisional Hxx follow-up
    (H03 fallback). No source is rereviewed and no external contract approved.
    """
    allowed={'implemented-with-observed-defects','conditional-policy-or-external-contract',
        'deferred-7B2-not-reviewed','deferred-not-implementation-reviewed',
        'rechecked-prior-root-not-new-finding','counterevidence-not-global-closure',
        'launcher-only-children-deferred','reviewed-contract-unresolved-not-global-absence',
        'source-only-resource-performance-lead-not-runtime-measured'}
    if status not in allowed:
        raise ValueError('Unrecognized historical metadata status, never silently certify: '+status)
    if status.startswith('deferred')or status.startswith('launcher-only'):
        return 'split-explicitly','SP7B17-02'if status.startswith('deferred')else'SP7B17-01'
    if status in {'conditional-policy-or-external-contract','reviewed-contract-unresolved-not-global-absence'}:
        h=('02'if any(t in title for t in('قالب','قوالب','الإخراج','مخرج','المخرج','إعداد','CSV','قنوات'))
           else'04'if any(t in title for t in('تفويض','صلاحيات','schema'))
           else'05'if any(t in title for t in('ثقافة','الثقافة','عمر','موارد','الأداء','ملكية'))
           else'01'if any(t in title for t in('مقياس','المقاييس','مصالحة','مصادر','سياسة','استحقاق','عمولات'))else'03')
        return 'external-handoff','H7B17-'+h
    return 'assessment-source-bound','none-bounded-prior-assessment'


def build_capability_ledger(labelled):
    """Metadata lineage only, never manufacture current semantic/source coverage."""
    out=[]
    for n,artifact,data in labelled:
        for x in data:
            title=x.get('feature',x.get('title'))
            disposition,link=prior_disposition(x['implementation_status'],title)
            out.append(dict(id=f'AG7B17-{len(out)+1:04d}',part=f'7B{n}',upstream_artifact=artifact,
                upstream_id=x['id'],upstream_row_sha256=row_sha(x),feature_or_contract=title,
                screen_or_component=x.get('screen',x.get('screen_or_component')),
                entry_and_trace=x.get('entrypoint_and_calls',x.get('entry_and_trace')),
                implementation_status_at_delivery=x['implementation_status'],coverage_level_at_delivery=x['coverage_level'],
                finding_ids_at_delivery=x['finding_ids'],prior_evidence=x['evidence'],prior_acceptance_ids=x['acceptance_ids'],
                prior_limit=x.get('scope_limit',x.get('limit')),family_contract_id=f'FC7B17-{n:02d}',
                disposition=disposition,handoff_or_split_ids=link,
                assessment_basis='exact-frozen-FE-metadata-lineage-not-current-source-rereview-or-unique-feature-count',
                runtime_status='not-executed'))
    return out


def ledger_errors(current,expected):
    errors=[]
    if current!=expected:
        errors.append('B17 frozen FE ledger exact metadata/order/lineage mismatch')
    pairs=[(r.get('upstream_artifact'),r.get('upstream_id'))for r in current]
    if len(pairs)!=len(set(pairs)):
        errors.append('B17 duplicate upstream FE pair')
    if any(r.get('assessment_basis')!='exact-frozen-FE-metadata-lineage-not-current-source-rereview-or-unique-feature-count'
           or r.get('runtime_status')!='not-executed'for r in current):
        errors.append('B17 metadata ledger coverage/execution overclaim')
    return errors


def current_link_errors(features,invariants,tests):
    errors=[]
    if len(features)!=12 or len(invariants)!=12 or len(tests)!=18:
        errors.append('B17 current FE/INV/T counts')
    for fe,inv in zip(features,invariants):
        if inv.get('feature_ids')!=fe.get('id') or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):
            errors.append('B17 current invariant/feature lineage')
        expected=';'.join(t['id']for t in tests if t['feature_ids']==fe['id'])
        if fe.get('acceptance_ids')!=expected or not expected:
            errors.append('B17 current acceptance reverse lineage')
    for error in bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids'):
        errors.append('B17 '+error)
    if len({r.get('required_invariant')for r in invariants})!=12 or len({r.get('acceptance_criterion')for r in tests})!=18:
        errors.append('B17 substantive distinct invariant/criterion contracts')
    if any(t.get('status')!='not-executed'for t in tests):
        errors.append('B17 acceptance must remain unexecuted')
    if any(t.get('finding_ids')!='P7-128'or t.get('plan_kind')!='finding-specific'for t in tests[:4]):
        errors.append('B17 four direct independent new-root plans')
    return errors


def residual_errors(current,upstream):
    errors=[]
    if len(current)!=14 or len(upstream)!=14:
        return ['B17 exactly14 named upstream residuals required']
    for old,new in zip(upstream,current):
        if (new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_row_sha256')!=row_sha(old)
                or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')
                or new.get('upstream_artifact')!='evidence/residual-disposition-07B16.csv'):
            errors.append('B17 exact upstream residual lineage')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():
                errors.append('B17 missing residual responsibility: '+k)
        if new.get('disposition')not in{'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':
            errors.append('B17 unresolved residual closure/execution overclaim')
    return errors


def remaining_work_errors(work,splits):
    errors=[]
    expected=['bounded-parent-contract-delivered-residuals-open']*2+['bounded-shared-contract-delivered-residuals-open','bounded-consolidation-delivered-residuals-open']+['planned-not-started']*6
    if (len(work)!=10 or [r.get('part_family')for r in work]!=['7B']*4+['7C']*6
            or [r.get('status')for r in work]!=expected):
        errors.append('B17 four B residual groups and six unstarted C axes required')
    for r in work:
        if r.get('runtime_status')!='not-executed'or r.get('counts_are_sessions_or_completion_percent')!='false':
            errors.append('B17 workplan execution/percentage overclaim')
    if len(splits)!=3:
        errors.append('B17 three explicit residual splits required')
    for r in splits:
        if r.get('status')!='explicit-further-static-split-not-started'or r.get('runtime_status')!='not-executed':
            errors.append('B17 split not closure or automatic next-phase start')
        for k in('title','candidate_scope_not_certified','reason_for_split','owner_role','required_input','next_static_action','static_exit_criterion'):
            if not isinstance(r.get(k),str)or not r[k].strip():
                errors.append('B17 missing split field: '+k)
    return errors


def group_row_errors(previous,current):
    gr=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M)
    return []if len(gr(previous))==176 and gr(current)[:176]==gr(previous)else['B17 historical G01–176 exact rows changed']


def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used',
             'spreadsheet_or_formula_interpreter_executed','phase7C_started','phase8_authorized_or_started'):
        if w.get(k)is not False:
            errors.append('B17 false-only boundary: '+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:
            errors.append('B17 integer-zero boundary: '+k)
    for k in('historical_metadata_aggregation_not_new_source_review','B_R4a_not_whole7B_closure',
             'unresolved_external_contracts_and_explicit_splits_retained','supplied_DDL_not_deployed_schema_certification'):
        if w.get(k)is not True:
            errors.append('B17 true-only documentary boundary: '+k)
    for k,n in(('illustration_count',10),('static_lexical_contract_check_count',10),('historical_metadata_rows_not_unique_features',455)):
        if type(w.get(k))is not int or w[k]!=n:
            errors.append('B17 documentary witness count: '+k)
    if w.get('phase')!='7B17-partial-static-consolidation':
        errors.append('B17 witness phase')
    return errors+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def validate_source(v,row,scope):
    if 'evidence'not in row:
        return
    if row['evidence']==DOCUMENTARY:
        v.check(row['id']in SENTINELS,'B17 undeclared documentary sentinel: '+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B17 fabricated source for documentary row: '+row['id'])
        v.evidence(row['evidence'],row['id'])
        v.scoped_evidence(row['evidence'],scope,row['id']+' boundedB17',phase=7)


def extend_consolidation(v,report,prov,frozen299):
    ck,rows=v.check,v.rows
    current=rows('findings.csv');new=current[299:]
    ck(len(current)==len({r['id']for r in current})==300 and [r['id']for r in new]==['P7-128'],'B17 current300/one new root128')
    ck(current[:299]==frozen299,'B17 ALL299 prior rows/fields/evidence/next_phase exact')
    ck(rows('evidence/historical-extensions-07B17.csv')==[],'B17 zero historical extensions')
    raw=(v.AUDIT/'findings.csv').read_bytes()
    ck(raw.startswith((v.AUDIT/SNAPSHOT).read_bytes()) and not raw.startswith(b'\xef\xbb\xbf')
       and raw.count(b'\r\n')==301 and raw.endswith(b'\r\n')
       and not any(c in raw.replace(b'\r\n',b'')for c in(b'\r',b'\n')),'B17 exact raw299 prefix/noBOM/current301CRLF')
    for error in registry_preservation_errors(frozen299,current,raw,(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,error)
    v.distributions(new,{'Medium':1},{'confirmed':1},'B17 only')
    for r in new:
        ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B17 finding/authorization state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B17 heading/registry')
    ck(prov['phase8_authorized_or_started']is False and prov['phase7C_started']is False
       and prov['application_remediation_performed']is False and type(prov['erp_runtime_tests_executed'])is int
       and prov['erp_runtime_tests_executed']==prov['sql_or_external_service_tests_executed']==0,'B17 no runtime/remediation/implicitC8')
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected}
    ck(len(selected)==len(scope)==18,'B17 selected18 paths')
    inventory=rows('evidence/inventory.csv');original={r['path']for r in inventory}
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-source-slices-not-runtime-certified'and bool(r['focus']),'B17 scope selection')
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B17-{n:02d}'for n in range(1,7)}
    tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B17.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if 'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B17 incomplete CSV cells: '+r['id'])
            validate_source(v,r,scope)
            if 'runtime_status'in r:ck(r['runtime_status']=='not-executed','B17 runtime overclaim: '+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B17-','INV7B17-','P7B17T-')]
    for error in current_link_errors(fe,inv,tests):ck(False,error)
    v.proposed_tests(tests,'7B17')
    fids,iids,tids=[{r['id']for r in x}for x in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids')
    v.related(fe+inv,tids,'acceptance_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B17 '+label)
    for r in tables['RC7B17-']:
        associated=[f for f in fe if f['id']in r['feature_ids'].split(';')]
        unique=lambda key:';'.join(dict.fromkeys(x for f in associated for x in f[key].split(';')))
        refs=[f['evidence']for f in associated if f['evidence']!=DOCUMENTARY]
        expected=';'.join(dict.fromkeys(x for s in refs for x in s.split(';')))if refs else DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==expected,'B17 RC exact FE lineage')
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    labelled=[]
    for n,count in enumerate(FE_COUNTS,1):
        artifact=f'evidence/feature-implementation-matrix-07B{n}.csv';data=rows(artifact)
        ck(len(data)==count,'B17 upstream frozen FE count')
        labelled.append((n,artifact,data))
    ledger=rows('evidence/capability-ledger-07B17.csv');v.sequential(ledger,'AG7B17-',455,width=4)
    for error in ledger_errors(ledger,build_capability_ledger(labelled)):ck(False,error)
    ck(collections.Counter(r['disposition']for r in ledger)=={'assessment-source-bound':365,'external-handoff':58,'split-explicitly':32},'B17 ledger categorical dispositions NOT unique feature counts')
    for n,r in enumerate(tables['FC7B17-'],1):
        ck(r['part']==f'7B{n}' and r['aggregation_basis']=='prior-frozen-documentary-contracts-not-new-source-rereview','B17 family metadata-only basis')
        ck(r['upstream_artifacts']==f'evidence/feature-implementation-matrix-07B{n}.csv;evidence/report-reconciliation-07B{n}.csv','B17 family upstream artifacts')
        for p in r['upstream_artifacts'].split(';'):ck((v.AUDIT/p).is_file(),'B17 family artifact exists')
    upstream=rows('evidence/residual-disposition-07B16.csv')
    for error in residual_errors(tables['RS7B17-'],upstream)+remaining_work_errors(tables['RW7B17-'],tables['SP7B17-']):ck(False,error)
    hids={r['id']for r in tables['H7B17-']};sids={r['id']for r in tables['SP7B17-']}
    v.related(tables['RS7B17-'],hids|sids,'current_handoff_or_split_ids')
    v.related(tables['Q7B17-'],hids,'handoff_ids')
    for r in tables['H7B17-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B17 no invented handoff approval')
    for r in tables['Q7B17-']:ck(r['status']=='unanswered-no-secrets-requested','B17 no invented policy answer')
    for n,r in enumerate(tables['BK7B17-'],1):
        ck(r['prior_backlog_id']==f'BK7B16-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B17 backlog ancestry/not complete')
    ck([r['status']for r in tables['BK7B17-'][2:6]]==['not-started']*4,'B17 no accidental C start')
    ad=tables['AD7B17-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids')
    ck(sum(r['decision']=='new-local-root'for r in ad)==1 and ad[0]['current_root_ids']=='P7-128','B17 exactly one adjudicated new root')
    ck(set(new[0]['evidence'].split(';'))<=set(ad[0]['evidence'].split(';')),'B17 adjudication must actually cite root')
    ck(all(r['comparison_depth']=='all299-titles-classifications-plus-selected-nearest-source-chains-not-all-historical-chains'for r in ad),'B17 dedup depth not all chains')
    previous_scopes=[rows('review-scope.csv'if n==1 else f'review-scope-{n:02d}.csv')for n in range(1,7)]
    previous_scopes+=[rows('review-scope-07.csv')]+[rows(f'review-scope-07B{n}.csv')for n in range(1,17)]
    before={r['path']for s in previous_scopes for r in s};paths=set(scope)
    ck((len(before),len(paths&before),len(paths-before),len(before|paths),len(original-(before|paths)))==(399,18,0,399,428),'B17 path bookkeeping not percentage/feature coverage')
    witness,match=v.recompute('evidence/report-witnesses-07B17.json','tools/check_consolidation_witnesses.py')
    for error in witness_metadata_errors(witness):ck(False,error)
    ck(witness['errors']==[],'B17 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B17-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B17-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,10);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B17 witness source/runtime boundary')
            validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B17 lexical read',phase=7)
    patterns=[(PART_DOCS[0],r'^\| (AD7B17-\d{2}) \|',ad),
      (PART_DOCS[1],r'^\| (FC7B17-\d{2}) \|',tables['FC7B17-']),
      (PART_DOCS[1],r'^\| (FE7B17-\d{2}) —',fe),(PART_DOCS[1],r'^\| (INV7B17-\d{2}) \|',inv),
      (PART_DOCS[1],r'^### (RC7B17-\d{2}) —',tables['RC7B17-']),
      (PART_DOCS[2],r'^\| (P7B17T-\d{2}) \|',tests),
      (PART_DOCS[3],r'^\| (RS7B17-\d{2}) \|',tables['RS7B17-']),
      (PART_DOCS[3],r'^\| (SP7B17-\d{2}) \|',tables['SP7B17-']),
      (PART_DOCS[3],r'^\| (RW7B17-\d{2}) \|',tables['RW7B17-'])]
    for name,pattern,pool in patterns:ck(re.findall(pattern,v.read(v.AUDIT/name),re.M)==[r['id']for r in pool],'B17 Markdown IDs: '+name)
    ck(re.findall(r'^\| (G-\d{2,3}) \|',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)==[f'G-{n:02d}'for n in range(1,181)],'B17 G177–180 only')
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
            if target==(v.AUDIT/'evidence/checks-07B17.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B17 broken link: '+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B17.md','PHASE-07-REMAINING-07B17.md','7B18','غير مأذونة','de0e7cf','10ba215')),'B17 live index boundary: '+name)
    tools=['check_consolidation_witnesses.py','validate_consolidation_part.py','test_consolidation_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B17 syntax: '+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_consolidation_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None
    passed=run.returncode==0 and count==24;ck(passed,'B17 documentation self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_consolidation_audit_validator.py']=dict(tests_reported=count,expected_tests=24,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name)for name in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B17-300-bounded-R4a-consolidation-not-7B-or-runtime-closure',
        phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,18))+'-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B18-proposed-R4b-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],
        registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=128,phase_7B17=1,total_open_not_remediated=300,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:18,'phase_7B17_prior_union':399,'phase_7B17_overlap_with_prior_union':18,'phase_7B17_new_paths':0,'unique_union_not_line_or_execution_coverage':399,'inventory_only_no_selected_scope':428})
    report['phase_7B16_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=468,historical_check_record_overwritten=False,genuine_b16_stdout_sha256_unchanged=B16_CHECK_SHA,partial7B17_append_only_extensions=[],all299_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B17_consolidation_limits']=dict(frozen_metadata_rows_not_unique_features=455,prior_part_counts=list(FE_COUNTS),metadata_only_dispositions=dict(collections.Counter(r['disposition']for r in ledger)),family_contracts=16,current_features_or_documentary_contracts_not_completed_features=12,current_invariants_not_executed_tests=12,acceptance_plans_not_executed=18,residual_inputs=14,explicit_further_static_splits=3,B_R4a_delivered_not_whole_R4_or7B_closure=True,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B17_illustrations_not_erp_tests=10,phase_7B17_lexical_checks_not_erp_tests=10,phase_7B17_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),phase_7B17_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=('Read-only documentary B17/R4a:468 protected artifacts/299 EXACT historical rows/ALLnext_phase/evidence/rawCRLFprefix/G01..176/three entry freezes/original827. No historical evidence extensions. One local root128: no-sub IsVAT is not reset per row/request, main empty subtable returns before reset; fresh/warm with-VAT membership differs. Counterexamples main valid-row reset and cold with-VAT preserved. Distinct045/046/095/084/P4-028. Prior roots034..037/029..031/061 rechecked not recounted. Income/Android dispatch boundary observed, required editor policy unresolved. 455 frozen FE metadata rows with exact lineage are NOT455 unique features or current source re-reviews;365 assessed-with-prior-limits/58 external/32 split metadata dispositions.16 family source/request/metric/sink contracts,12 current selected/documentary contracts,14 upstream residual dispositions,3 explicit further splits; none external approvals.18 selected paths all overlap399, complement428;98 filename/52 screen/3 supplemental depth are not feature denominator. R4a bounded delivery, R4b/B18 proposed for wider callers/capability census/amount-words-barcode beyond named traces. Six C axes unstarted;8 unauthorized. No session/percentage promise. Historical helpers receive OWN rows/exactCRLF/indexes IN MEMORY, no global pathlib patch/disk overlay/protected helper edit/rebaseline/archive rewrite. Versioned B16 CLI preset retained as actual choices base; current parser extends it with explicitB17 default, programmatic main defaultB15 preserved for prior API/tests. Source10ba, completed B16push/entryde0e7cf and genuine B16stdoutcheckout16f3fd4 distinct; archives never rewritten after push.10 manual+10 bounded lexical+24 new synthetic documentary cases;all18 acceptance plans not-executed. Additive B10 erratum10vs120 retained, not all prose certified. No application import/build/C#/SQL/VB/WPF/SDK/REPX/Office/COM/HTML/formula interpreter/provider/device/printer/business export/application shell/real data/secrets/remediation/ERP acceptance/operational measurement.7B/7 partial;7C unstarted;8 unauthorized;next_phase8 is planning not authorization.')
