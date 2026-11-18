#!/usr/bin/env python3
"""Read-only PARTIAL7B12 documentary checks, NEVER ERP acceptance.

Protect338 prior artifacts, frozen287 cores/ALL followups and exactG01..146.
B11 gets OWN frozen287 registry bytes/rows and exact delivered indexes IN MEMORY.
The local Path subclass overlays only the exact logical registry read_bytes;
no pathlib-global patch, filesystem overlay, protected-helper edit or rebaseline.
Supplied SQL/child schema is not certified deployed; P3-022 is not assumed fixed.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
import csv
import io
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from validate_financial_report_part import (
    historical_b1_inputs, registry_transition_errors, bidirectional_errors,
)
from validate_statement_contract_part import (
    build_current_ledger as prior_ledger, build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens, feature_level_errors as prior_feature_errors,
    arithmetic_erratum_errors,
)

SCOPE_FILE='review-scope-07B12.csv'
PART_DOCS=('PHASE-07B12.md','INCOME-BALANCE-CONTRACTS-07B12.md','VALIDATION-07B12.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B11.csv'
SNAPSHOT_SHA='72a30548eebe7a14a8eeffed62cc76fc45879a3a900037f3731813a7caf0a2da'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B11.json'
SHARED_SHA='46b91067fcdfd70de3eb62017dad0202d2226f305e50ffc5523ff7521f050732'
PROVENANCE_SHA='d91d49ed7e7a7c064628b1e7b3e5c7a5795f1a6ea06d7925f6525e220688b8a4'
B11_CHECK_SHA='f6e6a05b0bf6aa4f15efa93af34bd35aef940fa1bd66081bda029a9adf38a349'
ENTRY_CHECKOUT='670ae77c05709a85bcf52c6c9a2c73b4eb0c2d7e'
EXTENDED_FINDINGS={
    'P1-004','P1-013','P1-033','P2-010','P3-019','P3-020','P3-023','P4-008',
    'P7-045','P7-046','P7-048','P7-049','P7-050','P7-065','P7-097','P7-098',
}
REVIEWED_BODIES=('IncomeStatementForm','frmRptIncomeStatement','frmMezanyaArba7')
SENTINELS={
    'FE7B12-24','FE7B12-25','INV7B12-24','INV7B12-25',
    'RC7B12-06','H7B12-06','Q7B12-06','P7B12T-26','P7B12T-27',
}
TABLE_SPECS=(
    ('acceptance-tests','P7B12T-',27),('feature-implementation-matrix','FE7B12-',25),
    ('report-invariants','INV7B12-',25),('report-reconciliation','RC7B12-',6),
    ('historical-extensions','EX7B12-',16),('handoffs','H7B12-',6),
    ('questions','Q7B12-',6),('continuation-backlog','BK7B12-',10),
)


@contextmanager
def historical_b11_inputs(v,frozen287,texts,raw):
    """Exact logical-path rows/text/CRLF bytes; delegate and restore on errors.

    Protected B11 reads its registry bytes directly, so a rows/text-only adapter
    is insufficient. This local Path subclass affects exactly one resolved path
    in this context; other files and pathlib.Path itself are never patched.
    """
    if len(frozen287)!=287 or len({r['id'] for r in frozen287})!=287:
        raise ValueError('Exactly287 distinct historical registry rows required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact historical UTF8/noBOM bytes required')
    try:
        parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except (UnicodeError,csv.Error) as exc:
        raise ValueError('Historical registry bytes malformed') from exc
    if parsed!=frozen287 or raw.count(b'\r\n')!=288 or b'\n' in raw.replace(b'\r\n',b''):
        raise ValueError('Frozen287 bytes/rows/CRLF disagree')
    original_audit=v.AUDIT;target=Path(original_audit/'findings.csv').resolve()
    class FrozenRegistryPath(type(original_audit)):
        def read_bytes(self):
            if self.resolve()==target:return raw
            return super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original_audit)
        with historical_b1_inputs(v,frozen287,texts):yield
    finally:
        v.AUDIT=original_audit


def validate_frozen_b11(v,report,prior,frozen285,prov,frozen287):
    ck=v.check
    ck(v.sha(v.AUDIT/'evidence/provenance-07B12.json')==PROVENANCE_SHA,'B12 one-time provenance identity changed')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and
       v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,'B12 frozen287 identity changed')
    ck(prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA and
       v.sha(v.AUDIT/SHARED_SNAPSHOT)==SHARED_SHA,'B12 frozen exact B11 indexes changed')
    ck(prov['phase7B11_entry_consistency']==dict(original_hashes_matching=827,findings=287,
       phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9+7B10+7B11-partial-not-complete7B-or7',
       errors=[],erp_runtime_tests_executed=0),'B12 entry no longer describes delivered B11')
    for p,digest in prior['historical_artifact_sha256'].items():
        ck(prov['historical_artifact_sha256'].get(p)==digest,'315-to338 continuity: '+p)
    ck(prov['genuine_B11_check_sha256']==B11_CHECK_SHA and v.sha(v.AUDIT/'evidence/checks-07B11.json')==B11_CHECK_SHA,
       'Genuine B11 stdout changed')
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B11.json'))
    ck(saved['validation']['errors']==[] and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False and
       saved['findings']['total_open_not_remediated']==287 and saved['original_project_hashes_matching']==827 and
       saved['historical_artifact_sha256']==prior['historical_artifact_sha256'] and
       saved['checkout_head']=='1fbac9e34ede90396f212bd03390a1a737c351e6','B11 archived287/827/315/checkout changed')
    from validate_statement_contract_part import extend_statement_contracts
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];raw=(v.AUDIT/SNAPSHOT).read_bytes()
    with historical_b11_inputs(v,frozen287,texts,raw):
        extend_statement_contracts(v,report,prior,frozen285)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B11-287-not-current-state',
        phase_7B11_historical_input_mode='frozen287-rows-and-CRLF-bytes-plus-exact-shared-index-texts-in-memory')
    report['phase_7B11_adapter_context']=dict(entry_provenance='evidence/provenance-07B12.json',adapter_protected_artifacts_checked=338,
        current_registry_bytes_rows_and_shared_indexes_not_inputs=True,
        historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True,
        archived_stdout_not_rewritten_after_authorized_push=True)
    report['validation']['limit']+=(
        ' Historical B11 gets OWN frozen287 rows AND exact original CRLF bytes at one logical registry path and '
        'exact delivered indexes IN MEMORY, not current289/live files. Its read_bytes guard and immutable helper '
        'are preserved. B11 genuine stdout checkout1fbac9e remains byte-protected after pushed checkout670ae77.'
    )


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    out=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={r['path']:r['ranges'] for label,scope in labelled_scopes if label=='7B12' for r in scope}
    for r in out:
        r['phase7B12_ranges']=selected.get(r['path'],'none')
        if r['inventory_kind']!='generated-artifact':
            r['continuation_bucket']='7B13-or-7C-further-contracts-not-closed'
            r['next_scope_work']='بقية القدرات والمتصلين والأطفال والقوالب والمخطط والتفويض والسياسة أو استبعاد مسند؛7B13 معلنة و7C لم تبدأ. لا اكتمال من كل أسطر جسم ولا قياس index/leak/latency من النص.'
    return out


def build_candidate_disposition(inventory,labelled_scopes):
    out=prior_candidates(inventory,labelled_scopes)
    selected={r['path']:r['ranges'] for label,scope in labelled_scopes if label=='7B12' for r in scope}
    for r in out:
        r['phase7B12_ranges']=selected.get(r['path'],'none')
        if not r['disposition'].startswith('lexical-false-positive'):
            r['disposition']='7B13-further-contracts-or-reasoned-exclusion-required'
            r['reason']='98 مرشح ملف فرز أسماء لا ميزات مكتملة؛ الأسماء المنسقة خارج regex محفوظة. جسم محلي أو child slice لا يغلق كل قدرة/caller/template/schema/ACL/نشر/قبول؛7B13/7C أو استبعاد مسند.'
    return out


def build_screen_disposition(inventory,labelled_scopes):
    out=prior_screens(inventory,labelled_scopes)
    selected={r['path']:r['ranges'] for label,scope in labelled_scopes if label=='7B12' for r in scope}
    full={r['path']:'1-'+str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    for n,r in enumerate(out,1):
        r['id']=f'SC7B12-{n:02d}';r['phase7B12_body_ranges']=selected.get(r['body_path'],'none')
        r['disposition']='7B13-or-7C-further-contracts-or-reasoned-exclusion-required'
        if r['screen'] in REVIEWED_BODIES and all(p in full and selected.get(p)==full[p] for p in (r['path'],r['body_path'])):
            r['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified'
            r['reason']='استكمال جسم/XAML محلي في7B12 بعد مقاطع3/4/7A/B2؛ لا إعادة عد الأصول أو وراثة طفل لتغطية أبيه. بقية caller/template/schema/ACL/سياسة/نشر/قبول غير مغلقة؛7B13/7C.'
        else:
            r['reason']='حصر أو مقاطع/أجسام محلية سابقة بحسب الحقول، لا كل العقود؛ child لا يرث تغطية parent.7B13/7C أو استبعاد مسند.'
    return out


def feature_level_errors(features):return [e.replace('B11','B12') for e in prior_feature_errors(features)]


def group_row_errors(previous,current):
    old=re.findall(r'^\| G-\d{2,3} \|.*$',previous,re.M);now=re.findall(r'^\| G-\d{2,3} \|.*$',current,re.M)
    return [] if len(old)==146 and now[:146]==old else ['Historical G01–146 exact rows changed']


def witness_metadata_errors(w):
    out=[]
    for k in ('application_code_imported_or_executed','application_remediation_performed',
              'real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(k) is not False:out.append('B12 false-only flag: '+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:out.append('B12 integer-zero count: '+k)
    for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed',
              'stock_child_schema_not_assumed_resolved','manual_metric_models_not_financial_acceptance'):
        if w.get(k) is not True:out.append('B12 causal boundary: '+k)
    if w.get('phase')!='7B12-partial-static-audit':out.append('B12 witness phase')
    for k in ('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k)) is not int or w[k]!=22:out.append('B12 witness count: '+k)
    out+=arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))
    return out


def output_identity_errors(value):
    """Validate a synthetic proposed output contract, NOT run ERP export code."""
    if not isinstance(value,dict):return ['Missing output identity contract']
    keys=('chosen_path','effective_path','displayed_path','opened_path','format')
    if any(type(value.get(k)) is not str or not value[k] for k in keys):return ['Incomplete output identity contract']
    if not (value['effective_path']==value['displayed_path']==value['opened_path']):return ['Output path identity mismatch']
    if value['effective_path']!=value['chosen_path'] and value.get('explicit_conversion_confirmed') is not True:
        return ['Unannounced output path conversion']
    return []


def stock_selection_errors(value):
    """Synthetic proposed typed-selection shape; zero valid, unset not zero."""
    if not isinstance(value,dict):return ['Missing stock selection contract']
    if type(value.get('approved')) is not bool or type(value.get('has_value')) is not bool:
        return ['Stock approval/presence must be explicit booleans']
    if value['approved'] and not value['has_value']:return ['Approved stock value missing']
    if value['has_value']:
        if type(value.get('value')) not in (int,float):return ['Stock numeric value missing or boolean']
        if value.get('health')!='valid':return ['Stock selection source is not valid']
    elif value.get('value') is not None:return ['Unset stock is not a numeric zero']
    return []


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':
        v.check(row['id'] in SENTINELS,'Undeclared B12 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B12 documentary/inventory boundary: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B12',phase=7)


def extend_income_contracts(v,report,prov,frozen287):
    ck,rows=v.check,v.rows
    ck(prov['historical_artifact_count']==338 and len(frozen287)==287,'B12 entry count')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY_CHECKOUT,'B12 actual entry checkout')
    rec=prov['entry_checkout_reconciliation']
    ck(rec['initial_restored_checkout']==v.HEAD and rec['all343_workspace_document_bytes_matched_authorized_remote_before_fast_forward'] is True and
       rec['application_byte_changes'] is False,'B12 reconciliation boundary')
    ident=report['source_reference_validation']
    ck(ident['audited_application_reference']==v.HEAD and ident['reference_ancestor_of_checkout'] is True and
       ident['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B12 source identity')
    ck(prov['erp_runtime_tests_executed']==0 and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False,'B12 execution/remediation claim')
    current=rows('findings.csv');new=current[287:];extensions=rows('evidence/historical-extensions-07B12.csv')
    ext=v.transition(frozen287,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for e in registry_transition_errors(frozen287,current,extensions):ck(False,e)
    ck(len(current)==len({r['id'] for r in current})==289,'B12 count/uniqueness')
    ck([r['id'] for r in new]==['P7-116','P7-117'],'B12 new IDs')
    v.distributions(new,{'Medium':2},{'confirmed':2},'bounded7B12 only')
    for r in new:ck(r['status']=='open-not-remediated' and r['next_phase']=='8' and r['type']=='implementation-defect' and bool(r['title']),'B12 status/type/followup: '+r['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B12 headings/registry')
    raw=(v.AUDIT/'findings.csv').read_bytes()
    ck(not raw.startswith(b'\xef\xbb\xbf') and raw.count(b'\r\n')==290 and b'\n' not in raw.replace(b'\r\n',b''),'B12 CRLF/noBOM registry')
    scopes=rows(SCOPE_FILE);inventory=rows('evidence/inventory.csv');paths={r['path'] for r in inventory};scope={r['path']:v.spans(r['ranges']) for r in scopes}
    ck(len(scopes)==len(scope)==17,'B12 scope count/duplicates')
    for r in scopes:
        ck(r['path'] in paths and r['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(r['focus']),'B12 scope: '+r['path'])
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml.cs','.xaml'):
            p='SmartAuditERP/Form_WPF/'+name+suffix
            ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B12 full local body/XAML: '+p)
    known={r['id'] for r in current}|{f'H7B12-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B12.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for r in data:
            for k,value in r.items():ck(bool(value),f'Incomplete B12 cell: {r["id"]}.{k}')
            validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B12 runtime claim: '+r['id'])
    tests,features,invs,rc=[tables[k] for k in ('P7B12T-','FE7B12-','INV7B12-','RC7B12-')]
    tids={r['id'] for r in tests};fids={r['id'] for r in features};iids={r['id'] for r in invs}
    v.proposed_tests(tests,'7B12');v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(features+invs,tids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invs,'invariant_ids')):
        for e in bidirectional_errors(pool,tests,field):ck(False,e)
    for e in feature_level_errors(features):ck(False,e)
    for pool,label in ((tests,'plans'),(features,'features'),(invs,'invariants')):v.covered(new,pool,'B12 '+label)
    for r in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==r['id']])==2,'B12 finding lacks two direct plans: '+r['id'])
    ck([r['plan_kind'] for r in tests]==['finding-specific']*4+['historical-root-regression']*16+['cross-cutting-contract']*5+['documentary-scope-or-authorization-gate']*2,'B12 plan kinds/order')
    ck([r['finding_ids'] for r in features[:2]]==[r['id'] for r in new] and
       [r['finding_ids'] for r in features[2:18]]==[r['finding_ids'] for r in extensions] and
       {r['finding_ids'] for r in extensions}==EXTENDED_FINDINGS,'B12 new/extension mapping')
    for r in extensions:ck(r['followup_policy']=='unchanged-during-partial7','B12 hidden replan: '+r['id'])
    for r in rc:
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(r['feature_ids'].split(';'))]
        ck(r['acceptance_ids'].split(';')==expected and bool(expected),'B12 RC links: '+r['id'])
        roots={root for f in features if f['id'] in r['feature_ids'].split(';') for root in f['finding_ids'].split(';')}
        ck(set(r['finding_ids'].split(';'))<=roots,'B12 RC roots: '+r['id'])
    v.related(tables['Q7B12-'],{r['id'] for r in tables['H7B12-']},'handoff_ids')
    for r in tables['H7B12-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B12 handoff falsely resolved')
    for r in tables['Q7B12-']:ck(r['status']=='unanswered-no-secrets-requested','B12 question falsely resolved')
    for n,r in enumerate(tables['BK7B12-'],1):
        ck(r['prior_backlog_id']==f'BK7B11-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and
           r['part'] in {'7B13','7C','7B13/7C'} and r['status']!='complete','B12 backlog: '+r['id'])
    ck([r['status'] for r in tables['BK7B12-'][2:6]]==['not-started']*4,'B12 accidentally starts7C')
    labelled=[(str(n),rows('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]+[('7A',rows('review-scope-07.csv'))]
    labelled += [(f'7B{n}',rows(f'review-scope-07B{n}.csv')) for n in range(1,12)]+[('7B12',scopes)]
    ck(rows('evidence/coverage-ledger-07B12.csv')==build_current_ledger(inventory,labelled,v.spans),'B12 ledger recomputation')
    candidates=rows('evidence/report-candidate-disposition-07B12.csv');screens=rows('evidence/report-screen-disposition-07B12.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B12 filename98 triage')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B12 screen52 triage');v.sequential(screens,'SC7B12-',52)
    by={r['screen']:r for r in screens}
    for name in REVIEWED_BODIES:ck(by[name]['phase7B12_body_ranges']!='none' and by[name]['coverage_level']=='bounded-local-body-and-xaml-not-whole-feature-certified','B12 body depth: '+name)
    prior={r['path'] for _,selected in labelled[:-1] for r in selected};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(386,17,14,3,389,438),'B12 scope union bookkeeping')
    witness,match=v.recompute('evidence/report-witnesses-07B12.json','tools/check_income_contract_witnesses.py')
    alg,lex=witness['illustrations'],witness['static_lexical_contract_checks'];v.sequential(alg,'ALG7B12-',22);v.sequential(lex,'ST7B12-',22);v.related(alg+lex,known)
    for e in witness_metadata_errors(witness):ck(False,e)
    for r in alg+lex:
        flag='illustration_assertions_passed' if r['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B12 witness overclaim: '+r['id']);validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B12 bounded lexical read',phase=7)
    patterns=[
        (PART_DOCS[0],r'^\| (EX7B12-\d{2}) \|',[r['id'] for r in extensions]),
        (PART_DOCS[1],r'^\| (FE7B12-\d{2}) —',[r['id'] for r in features]),
        (PART_DOCS[1],r'^\| (INV7B12-\d{2}) \|',[r['id'] for r in invs]),
        (PART_DOCS[1],r'^### (RC7B12-\d{2}) —',[r['id'] for r in rc]),
        (PART_DOCS[1],r'^\| (H7B12-\d{2}) —',[r['id'] for r in tables['H7B12-']]),
        (PART_DOCS[1],r'^\| (Q7B12-\d{2}) \|',[r['id'] for r in tables['Q7B12-']]),
        (PART_DOCS[1],r'^\| (BK7B12-\d{2}) \|',[r['id'] for r in tables['BK7B12-']]),
        (PART_DOCS[2],r'^\| (P7B12T-\d{2}) \|',[r['id'] for r in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,153)]),
    ]
    for filename,pattern,expected in patterns:ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B12 Markdown IDs: '+filename)
    pending=False
    src=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B12.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B12 broken link: '+filename+':'+m[1])
        for m in src.finditer(text):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pat,ids in ((r'\bP7B12T-\d{2}\b',tids),(r'\bFE7B12-\d{2}\b',fids),(r'\bINV7B12-\d{2}\b',iids)):
            for item in re.findall(pat,text):ck(item in ids,'B12 unknown ID: '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            fields=[s.strip() for s in line.replace('**','').strip('|').split('|')];summary[fields[0]]=fields[1:]
    for label,expected in (('التراكمي المفتوح',[289,2,176,110,1]),('7B12 — جديدة',[2,0,0,2,0]),('7B12 — إضافة محدودة',[17,14,3,389])):
        ck(summary.get(label)==list(map(str,expected)),'B12 README counts: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    for name in SHARED_DOCS:
        ck(all(s in v.read(v.AUDIT/name) for s in ('PHASE-07B12.md','7B13','7C','غير مأذونة','670ae77','10ba215')),'B12 index lacks boundaries: '+name)
    tools=['check_income_contract_witnesses.py','validate_income_contract_part.py','test_income_contract_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B12 tool syntax: '+name+':'+str(e))
    process=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_income_contract_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',process.stderr+'\n'+process.stdout);count=int(m[1]) if m else None
    passed=process.returncode==0 and count==32;ck(passed,'B12 helper self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_income_contract_audit_validator.py']=dict(tests_reported=count,expected_tests=32,process_exit_code=process.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B12-289-plus-frozen-history-not-runtime-certification',
        phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9+7B10+7B11+7B12-partial-not-complete7B-or7',
        phase_7_remaining_parts=['7B13-announced-not-started','7C-not-started'],registry_used='findings.csv',
        historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=117,phase_7B12=2,total_open_not_remediated=289,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:17,'phase_7B11_union_frozen':386,'phase_7B12_overlap_with_prior_union':14,
        'phase_7B12_new_paths':3,'unique_union_not_line_or_execution_coverage':389,'inventory_only_no_selected_scope':438})
    report['phase_7B11_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=338,historical_check_record_overwritten=False,
        genuine_b11_check_sha256_unchanged=B11_CHECK_SHA,partial7B12_append_only_evidence_extensions_without_reclassification=ext,
        next_phase_followups_preserved_for_all287=True,next_phase_replans_during_partial7={},
        historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True)
    report['phase_7B12_entry_checkout_reconciliation']=rec
    report['phase_7B12_retained_additive_arithmetic_erratum']=witness['retained_additive_B10_arithmetic_erratum']
    report['evidence_rows'].update(dict(
        phase_7B12_feature_rows_not_completed_features=25,phase_7B12_invariants_not_passed_tests=25,
        phase_7B12_reconciliation_contracts_not_executed_financial_acceptance=6,
        phase_7B12_unexecuted_acceptance_or_gate_plans=27,phase_7B12_direct_finding_plans=4,
        phase_7B12_historical_regression_plans=16,phase_7B12_cross_contract_plans=5,phase_7B12_documentary_scope_authorization_gate_plans=2,
        phase_7B12_historical_extensions_not_new_findings=16,phase_7B12_unresolved_handoffs=6,phase_7B12_unanswered_questions=6,
        phase_7B12_continuation_groups_not_complete=10,phase_7B12_original_paths_in_ledger=827,
        phase_7B12_filename_candidates_not_feature_count=98,phase_7B12_screen_candidates_not_feature_count=52,
        phase_7B12_independent_illustrations_not_erp_tests=22,phase_7B12_bounded_literal_checks_not_application_tests=22,
        phase_7B12_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']=(
        'Read-only documentary checker: original827 path/hashes and source10ba ancestry/net docs-only delta;338 protected prior artifacts '
        'including genuine B11stdout checkout1fbac9e, B10checkouta254, B9checkout3612700 and B8checkout10ba. Frozen287 cores/ALLnext_phase/'
        'exact evidence prefixes with16 declared tails; exactG01..146. HistoricalA/B1..B11 get OWN frozen rows/bytes/exact indexes IN MEMORY '
        'without protected-code changes, overlay writes or global pathlib patch. Entry670ae77 is an already completed343-file B11 docs push, '
        'not pending or an application rebaseline.17 selected paths/three local bodies+XAML+DTOs/selected stock child are not all capability/'
        'caller/child/template/schema/ACL/policy/deployment contracts. P7-116 is a local effective-output-path mismatch, not a stub, '
        'wrong-extension-only duplicate or writer-finalization defect: StreamWriter using completes before caller success/launch. '
        'P7-117 conflates approved numeric zero with unset and silently chooses auto stock; legitimate zero must be accepted or explicitly '
        'rejected under a policy, not confused with cancellation. The stock child P4-030 schema/source-health gate is not assumed fixed; '
        'hand-selected valid-zero inputs isolate the sentinel cause, not certify any empty child as financially valid. '
        'P3-020 ABS/summary/COGS-zero/expense-prefix/other-revenue, P3-019 period-versus-closing, P3-023 endpoints, P4-008 as-of, P7-065 branch '
        'sets, P7-045 snapshots, P7-046 failure-as-zero, CSV/HTML/REPX roots remain deduplicated. Supplied InventoryCost CREATE/ALTER are '
        'not certified deployed; InventoryCostForBalanceSheet exists but these parents call InventoryCost. The local old-income XAML has '
        'no txtFirstVal names and its calculated first stock is not consumed by totals: bounded functional gap, not a new opening-policy '
        'finding. Stock replacement/addition, tree rollup, currency, FinalAcc/code-pattern metrics and balanced-after-plug meaning need '
        'an accounting contract; do not force equal totals. Main new income menu has no explicit IsEnabledFalse, the other two do; Apply '
        'before Show/new instances/using/finally/Closing are bounded positive evidence, not deployed role or leak/performance certification. '
        'Default statement aggregate P3-022 remains in its own earlier parent; no invented worker/aggregate gate in these synchronous '
        'parents. Additive B10 erratum10 versus120 is retained without editing historical prose/G138/checks.22 manual+22 lexical+32 new '
        'synthetic checker cases are not ERP tests;27 acceptance/gate plans remain not-executed.7B/7 partial,7B13 announced,7C unstarted, '
        '8 unauthorized. No application import/build/C#/SQL/WPF/Office/COM/REPX/formula/HTML interpreter/printer/device/provider/actual '
        'export/shell execution, remediation, real data/secrets, financial/security/compliance acceptance or index/leak/latency measurement.'
    )
