#!/usr/bin/env python3
"""Read-only PARTIAL7B9 documentary checks, never ERP acceptance.

Protect all269 prior nonmutable artifacts and the original827 application
paths/hashes. B8 receives its OWN frozen280 registry/exact shared texts IN
MEMORY. Newly authorized docs-only push3612700 does not redate archived B8
checks (checkout10ba at delivery). Three report bodies are not whole features.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections,re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_decision_summary_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors as prior_feature_errors)

SCOPE_FILE='review-scope-07B9.csv'
PART_DOCS=('PHASE-07B9.md','RECEIPT-PAYROLL-REPORTS-07B9.md','VALIDATION-07B9.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B8.csv'
SNAPSHOT_SHA='83a128fea7d8dd7c15b1e9ef7daaf1064850ffc70d1a6ea5f4ac149708d4c33f'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B8.json'
SHARED_SHA='3352cbd299295853e83e078579ab4f78455f5a3754d532d6df23a45b0169b2e2'
B8_CHECK_SHA='598f4ec4865b2a1e21a90b84860cfc59b13296fc7831dba8962d568cc4cec9ef'
ENTRY_CHECKOUT='3612700aa19ecdd077bc7dabf79eb61136015054'
EXTENDED_FINDINGS={'P1-004','P1-013','P1-030','P1-033','P2-010','P3-023','P7-002','P7-006','P7-046','P7-048','P7-049'}
REVIEWED_BODIES=('frmSummaryQ','frmRptSalary','frmRptReseved')
SENTINELS={'RC7B9-06','FE7B9-19','INV7B9-19','FE7B9-20','INV7B9-20','H7B9-06','Q7B9-06','P7B9T-21','P7B9T-22'}
TABLE_SPECS=(('acceptance-tests','P7B9T-',22),('feature-implementation-matrix','FE7B9-',20),('report-invariants','INV7B9-',20),('report-reconciliation','RC7B9-',6),('historical-extensions','EX7B9-',11),('handoffs','H7B9-',6),('questions','Q7B9-',6),('continuation-backlog','BK7B9-',10))

@contextmanager
def historical_b8_inputs(v,frozen280,texts):
    if len(frozen280)!=280 or len({x['id'] for x in frozen280})!=280:
        raise ValueError('Exactly280 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen280,texts):yield

def validate_frozen_b8(v,report,prov_b8,frozen276,prov_b9,frozen280):
    ck=v.check
    ck(prov_b9['registry_at_entry_snapshot']==SNAPSHOT and prov_b9['registry_at_entry_sha256']==SNAPSHOT_SHA,'B9 frozen280 identity changed')
    ck(prov_b9['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov_b9['shared_indexes_at_entry_sha256']==SHARED_SHA and v.sha(v.AUDIT/SHARED_SNAPSHOT)==SHARED_SHA,'B9 exact B8 indexes changed')
    ck(prov_b9['phase7B8_entry_consistency']==dict(original_hashes_matching=827,findings=280,phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B9 entry no longer describes B8')
    for p,digest in prov_b8['historical_artifact_sha256'].items():ck(prov_b9['historical_artifact_sha256'].get(p)==digest,'246-to269 history continuity failed: '+p)
    ck(prov_b9['genuine_B8_check_sha256']==B8_CHECK_SHA and v.sha(v.AUDIT/'evidence/checks-07B8.json')==B8_CHECK_SHA,'Genuine archived B8 stdout changed')
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B8.json'))
    ck(saved['validation']['errors']==[] and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False and saved['findings']['total_open_not_remediated']==280 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov_b8['historical_artifact_sha256'],'Archived B8 stdout no longer genuine280/827/246')
    from validate_decision_summary_part import extend_decision_summary
    with historical_b8_inputs(v,frozen280,v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']):extend_decision_summary(v,report,prov_b8,frozen276)
    report['registry_used']=SNAPSHOT;report['validation_scope']='historical-through7B8-280-not-current-state'
    report['phase_7B8_historical_input_mode']='frozen280-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B8_adapter_context']=dict(entry_provenance='evidence/provenance-07B9.json',adapter_protected_artifacts_checked=269,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True,archived_stdout_not_rewritten_after_authorized_push=True)
    report['validation']['limit']+=' HistoricalB8 receives frozen280/exact delivered indexes IN MEMORY, never current282/live indexes. Archived stdout280/checkout10ba remains byte-protected; current metadata reflects the newly authorized docs-only history-preserving push, not an archived byte replay.'

def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    result=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={x['path']:x['ranges'] for label,s in labelled_scopes if label=='7B9' for x in s}
    for x in result:
        x['phase7B9_ranges']=selected.get(x['path'],'none')
        if x['inventory_kind']=='generated-artifact':continue
        x['continuation_bucket']='7B10-or-7C-further-contracts-not-closed'
        x['next_scope_work']='بقية القدرات/callers/children/output/schema/ACL/السياسة أو استبعاد مسند؛7B10 معلنة و7C لم تبدأ. لا اكتمال من full local body أو parent أو اسم، ولا latency/leak/index من نص.'
    return result

def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,s in labelled_scopes if label=='7B9' for x in s}
    for x in result:
        x['phase7B9_ranges']=selected.get(x['path'],'none')
        if x['disposition'].startswith('lexical-false-positive'):continue
        x['disposition']='7B10-further-contracts-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف فرز أسماء لا98 ميزة؛ قراءةSummaryQ/Salary/Reseved لا كلcaller/child/template/schema/ACL/نشر/قبول.7B10 معلنة؛Reseved هنا استحقاق رواتب لا حجز بحري.'
    return result

def build_screen_disposition(inventory,labelled_scopes):
    result=prior_screens(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,s in labelled_scopes if label=='7B9' for x in s}
    full_text={x['path']:'1-'+str(x['lines']) for x in inventory if str(x['lines']).isdigit()}
    for n,x in enumerate(result,1):
        x['id']=f'SC7B9-{n:02d}';x['phase7B9_body_ranges']=selected.get(x['body_path'],'none')
        x['disposition']='7B10-or-7C-further-contracts-or-reasoned-exclusion-required'
        if (x['screen'] in REVIEWED_BODIES and
            all(p in full_text and selected.get(p)==full_text[p] for p in (x['path'],x['body_path']))):
            x['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified'
            x['reason']='جسم/XAML محليان ودعم منتقى في7B9؛SummaryQ سندات5/6/10 لا قيودGL، وReseved استحقاقرواتب لاحجزبحري. لاكلمدخل/طفل/قالب/schema/ACL أو قبول؛7B10/7C.'
        else:x['reason']='حصر أو مقاطع/أجسام محلية سابقة بحسب الحقول، ليست كل العقود أو التنفيذ/النشر. لا يرث child تغطية parent؛7B10/7C أو استبعاد مسند.'
    return result

def feature_level_errors(features):return [x.replace('B8','B9') for x in prior_feature_errors(features)]
def group_row_errors(previous_text,current_text):
    old=re.findall(r'^\| G-\d{2,3} \|.*$',previous_text,re.M);now=re.findall(r'^\| G-\d{2,3} \|.*$',current_text,re.M)
    return [] if len(old)==128 and now[:128]==old else ['Historical G01–128 exact rows changed']
def witness_metadata_errors(w):
    errors=[]
    for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(key) is not False:errors.append('B9 witness false-only flag: '+key)
    for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(key)) is not int or w[key]!=0:errors.append('B9 witness zero-only count: '+key)
    if w.get('phase')!='7B9-partial-static-audit':errors.append('B9 witness phase mismatch')
    for key in ('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(key)) is not int or w[key]!=18:errors.append('B9 witness count mismatch: '+key)
    return errors

def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':v.check(row['id'] in SENTINELS,'Undeclared B9 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B9 documentary/inventory boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B9',phase=7)

def extend_receipt_payroll(v,report,prov,frozen280):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==269 and len(frozen280)==280,'B9 protected entry count mismatch')
    ident=report['source_reference_validation']
    ck(ident['audited_application_reference']==v.HEAD and ident['reference_ancestor_of_checkout'] is True and ident['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B9 source/checkout integrity mismatch')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY_CHECKOUT,'B9 actual post-authorized-push entry changed')
    push=prov['authorized_push_before_continuation']
    ck(push['merge_and_push_commit']==ENTRY_CHECKOUT and push['force_push'] is False and push['application_changes'] is False and push['byte_identical_prior_nonmutable_documents']==199 and push['all274_current_document_hashes_preserved_across_merge'] is True,'B9 push receipt boundary changed')
    ck(prov['erp_runtime_tests_executed']==0 and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False,'B9 entry wrongly authorizes/executes runtime or remediation')
    current=r('findings.csv');new=current[280:];extensions=r('evidence/historical-extensions-07B9.csv')
    ext=v.transition(frozen280,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen280,current,extensions):ck(False,err)
    ck(len(current)==282 and len({x['id'] for x in current})==282,'B9 current count/uniqueness mismatch')
    ck([x['id'] for x in new]==['P7-109','P7-110'],'B9 new finding IDs/order mismatch');v.distributions(new,{'Medium':2},{'confirmed':1,'potential':1},'bounded7B9 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B9 new status/type/followup mismatch: '+x['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B9.md'),re.M)==[(x['id'],x['title']) for x in new],'B9 report titles/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory};scope={x['path']:v.spans(x['ranges']) for x in scopes}
    ck(len(scopes)==len(scope)==19,'B9 scope count/duplicates mismatch')
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B9 scope path/state mismatch: '+x['path']);v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml.cs','.xaml'):
            p='SmartAuditERP/Form_WPF/'+name+suffix;ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B9 body/XAML span mismatch: '+p)
    known={x['id'] for x in current}|{f'H7B9-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=r('evidence/'+name+'-07B9.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for key,value in x.items():ck(bool(value),f'Incomplete B9 cell: {x["id"]}.{key}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B9 runtime claim: '+x['id'])
    tests,features,invariants,rc=[tables[k] for k in ('P7B9T-','FE7B9-','INV7B9-','RC7B9-')]
    tids={x['id'] for x in tests};fids={x['id'] for x in features};iids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B9');v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(features+invariants,tids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B9 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B9 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*4+['historical-root-regression']*11+['cross-cutting-contract']*5+['documentary-scope-or-authorization-gate']*2,'B9 plan kinds/order mismatch')
    ck([x['finding_ids'] for x in features[:2]]==[x['id'] for x in new] and [x['finding_ids'] for x in features[2:13]]==[x['finding_ids'] for x in extensions] and {x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B9 feature/extension mapping mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B9 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],fids,'feature_ids');v.related([x],tids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B9 RC plan links mismatch: '+x['id'])
        roots={q for f in features if f['id'] in x['feature_ids'].split(';') for q in f['finding_ids'].split(';')};ck(set(x['finding_ids'].split(';'))<=roots,'B9 RC finding not in linked features: '+x['id'])
    v.related(tables['Q7B9-'],{x['id'] for x in tables['H7B9-']},'handoff_ids')
    for x in tables['H7B9-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B9 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B9-']:ck(x['status']=='unanswered-no-secrets-requested','B9 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B9-'],1):ck(x['prior_backlog_id']==f'BK7B8-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B10','7C','7B10/7C'} and x['status']!='complete','B9 backlog origin/part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B9-'][2:6]]==['not-started']*4,'B9 accidentally starts7C')
    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]+[('7A',r('review-scope-07.csv'))]+[(f'7B{n}',r(f'review-scope-07B{n}.csv')) for n in range(1,9)]+[('7B9',scopes)]
    ck(r('evidence/coverage-ledger-07B9.csv')==build_current_ledger(inventory,labelled,v.spans),'B9 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B9.csv');screens=r('evidence/report-screen-disposition-07B9.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B9 filename98 candidate mismatch');ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B9 screen52 candidate mismatch');v.sequential(screens,'SC7B9-',52)
    by={x['screen']:x for x in screens}
    for name in REVIEWED_BODIES:ck(by[name]['phase7B9_body_ranges']!='none' and by[name]['coverage_level']=='bounded-local-body-and-xaml-not-whole-feature-certified','B9 local body incorrectly deferred/promoted: '+name)
    ck('frmUsersRecords' not in by and 'historical artifacts unchanged' in by['frmrptUsersRecords']['historical_name_mapping'],'B9 loses actual B8 log alias')
    prior={x['path'] for _,s in labelled[:-1] for x in s};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(373,19,17,2,375,452),'B9 scope union bookkeeping mismatch')
    w,match=v.recompute('evidence/report-witnesses-07B9.json','tools/check_receipt_payroll_witnesses.py');alg,lex=w['illustrations'],w['static_lexical_contract_checks']
    v.sequential(alg,'ALG7B9-',18);v.sequential(lex,'ST7B9-',18);v.related(alg+lex,known)
    for err in witness_metadata_errors(w):ck(False,err)
    for x in alg+lex:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B9 witness fail/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in w['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B9 bounded lexical read',phase=7)
    patterns=[('PHASE-07B9.md',r'^\| (EX7B9-\d{2}) \|',[x['id'] for x in extensions]),('RECEIPT-PAYROLL-REPORTS-07B9.md',r'^\| (FE7B9-\d{2}) —',[x['id'] for x in features]),('RECEIPT-PAYROLL-REPORTS-07B9.md',r'^\| (INV7B9-\d{2}) \|',[x['id'] for x in invariants]),('RECEIPT-PAYROLL-REPORTS-07B9.md',r'^### (RC7B9-\d{2}) —',[x['id'] for x in rc]),('RECEIPT-PAYROLL-REPORTS-07B9.md',r'^\| (H7B9-\d{2}) —',[x['id'] for x in tables['H7B9-']]),('RECEIPT-PAYROLL-REPORTS-07B9.md',r'^\| (Q7B9-\d{2}) \|',[x['id'] for x in tables['Q7B9-']]),('RECEIPT-PAYROLL-REPORTS-07B9.md',r'^\| (BK7B9-\d{2}) \|',[x['id'] for x in tables['BK7B9-']]),('VALIDATION-07B9.md',r'^\| (P7B9T-\d{2}) \|',[x['id'] for x in tests]),('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,135)])]
    for filename,pattern,expected in patterns:ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B9 Markdown ID/order mismatch: '+filename)
    pending=False;source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B9.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B9 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B9T-\d{2}\b',tids),(r'\bFE7B9-\d{2}\b',fids),(r'\bINV7B9-\d{2}\b',iids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B9 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            f=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[f[0]]=f[1:]
    for label,expected in (('التراكمي المفتوح',[282,2,175,104,1]),('7B9 — جديدة',[2,0,0,2,0]),('7B9 — إضافة محدودة',[19,17,2,375])):ck(summary.get(label)==list(map(str,expected)),'Current B9 README numeric mismatch: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for err in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,err)
    for name in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/name) for x in ('PHASE-07B9.md','7B10','7C','غير مأذونة','3612700','10ba215')),'Current index lacks B9/B10/C/8/push-source boundary: '+name)
    tools=['check_receipt_payroll_witnesses.py','validate_receipt_payroll_part.py','test_receipt_payroll_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as ex:ck(False,'B9 audit-tool syntax: '+name+':'+str(ex))
    p=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_receipt_payroll_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30);m=re.search(r'Ran (\d+) tests? in ',p.stderr+'\n'+p.stdout);count=int(m[1]) if m else None;passed=p.returncode==0 and count==24;ck(passed,'B9 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_receipt_payroll_audit_validator.py']=dict(tests_reported=count,expected_tests=24,process_exit_code=p.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools;report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+name:v.sha(v.AUDIT/'tools'/name) for name in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B9-282-plus-frozen-history-not-runtime-certification',phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9-partial-not-complete7B-or7',phase_7_remaining_parts=['7B10-announced-not-started','7C-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=110,phase_7B9=2,total_open_not_remediated=282,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:19,'phase_7B8_union_frozen':373,'phase_7B9_overlap_with_prior_union':17,'phase_7B9_new_paths':2,'unique_union_not_line_or_execution_coverage':375,'inventory_only_no_selected_scope':452})
    report['phase_7B8_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=269,historical_check_record_overwritten=False,genuine_b8_check_sha256_unchanged=B8_CHECK_SHA,partial7B9_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all280=True,next_phase_replans_during_partial7={},historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True)
    report['phase_7B9_authorized_push_before_entry']=push
    report['evidence_rows'].update(dict(phase_7B9_feature_rows_not_completed_features=20,phase_7B9_invariants_not_passed_tests=20,phase_7B9_reconciliation_contracts_not_executed_financial_acceptance=6,phase_7B9_unexecuted_acceptance_or_gate_plans=22,phase_7B9_direct_finding_plans=4,phase_7B9_historical_regression_plans=11,phase_7B9_cross_contract_plans=5,phase_7B9_documentary_scope_authorization_gate_plans=2,phase_7B9_historical_extensions_not_new_findings=11,phase_7B9_unresolved_handoffs=6,phase_7B9_unanswered_questions=6,phase_7B9_continuation_groups_not_complete=10,phase_7B9_original_paths_in_ledger=827,phase_7B9_filename_candidates_not_feature_count=98,phase_7B9_screen_candidates_not_feature_count=52,phase_7B9_independent_illustrations_not_erp_tests=18,phase_7B9_bounded_literal_checks_not_application_tests=18,phase_7B9_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only checker: original827 path/hash identity plus source10ba ancestry/net docs-only checkout delta; protected269 prior nonmutable artifacts including genuine B8 stdout/checker/report bytes; exact280 historical cores/ALLnext_phase and11 declared evidence tails; exact G01..128 rows. All historical A/B1..B8 use their OWN frozen registry/index text inputs IN MEMORY, never current282/live indexes; current metrics/checkout are not archived stdout byte replay or whole-history attestation. Entry checkout3612700 is the newly authorized history-preserving docs-only push; no force push/rebaseline or redating old checks.19 selected paths/three report bodies/XAML are not all callers/children/templates/schema/ACL/deployment. SummaryQ is receipts5/6/10, RptReseved is salary accrual, not marine booking. User multiplicity effect P7-110 remains POTENTIAL: local UI lookup/update is counterevidence to an assertion of always-duplicate active users; deployed data/constraints/mapping unresolved. Payroll report recomputation does not remediate stale stored salary_net or establish financial settlement/GL; accrual child initialization/private-source/binder gates persist. Typed half-open SummaryQ dates, type5+GlobalID navigation, writer-block closure before shell and explicitly unavailable Salary printing are counterevidence, not blanket P3-023/P7-061/P7-108/P7-054/P7-107/P7-050 findings. SQL-int-selected account value alone is not proven reachable SQL injection. Source N+1/sync Fill/no paging are not latency/leak/index measurements.18 manual contrasts and18 bounded lexical observations and isolated synthetic checker cases are documentary only;22 ERP/contract/gate plans not executed.7B10 announced,7C not started,8 unauthorized. No ERP/C#/SQL/WPF/Office/COM/SDK/provider/device/formula/process/shell/actual export IO execution, remediation, secrets/business data or completeness/financial/security/compliance certification.'
