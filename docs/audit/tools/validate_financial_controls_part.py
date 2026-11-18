#!/usr/bin/env python3
"""Read-only PARTIAL7B7 documentation checks, never ERP/SQL/WPF acceptance.

Protected B6 receives frozen270 and exact delivered indexes at original
logical paths IN MEMORY. B6 helpers/reports/checks are not edited/rebaselined.
Original827 path/hash guards and source10ba/docs-only-checkout separation stay
mandatory. Five bodies/local XAML do not certify callers/templates/deployment.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import collections,re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_pos_totals_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors as prior_feature_errors,
    NONREGEX_SCREENS)

SCOPE_FILE='review-scope-07B7.csv'
PART_DOCS=('PHASE-07B7.md','FINANCIAL-CONTROLS-07B7.md','VALIDATION-07B7.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B6.csv'
SNAPSHOT_SHA='781c9d4bac775f55456f6b54ba66c4190de0ec93f14b50886790121e8d0e1a98'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B6.json'
SHARED_SHA='99af3af80436557ad21e54784602fd7fd913ea3edd5458813bde49e4f24cb058'
B6_CHECK_SHA='b171d38d2f1d12894be879346c689c67900efed10105c5f2fae5ace110e413a0'
EXTENDED_FINDINGS={'P1-004','P1-011','P1-013','P1-030','P1-033','P2-001','P2-010','P2-011','P3-023','P4-010','P7-040','P7-041','P7-045','P7-046','P7-048','P7-049','P7-053','P7-084'}
SENTINELS={'FE7B7-31','INV7B7-31','FE7B7-30','INV7B7-30','H7B7-06','Q7B7-06','P7B7T-36','P7B7T-37'}
REVIEWED_BODIES=('frmCostCenterBalance','frmInvsProfit','frmItemsBalances','frmInvRptType','frmNkdTotSalePurchActCust')
DEFERRED_SCREENS=('frmDecisionHelp','frmSummaryD','frmUsersRecords')


@contextmanager
def historical_b6_inputs(v,frozen270,shared_texts):
    if len(frozen270)!=270 or len({x['id'] for x in frozen270})!=270:
        raise ValueError('Exactly270 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen270,shared_texts):yield


def validate_frozen_b6(v,report,prov_b6,frozen266,prov_b7,frozen270):
    ck=v.check
    ck(prov_b7['registry_at_entry_snapshot']==SNAPSHOT and prov_b7['registry_at_entry_sha256']==SNAPSHOT_SHA,'B7 frozen270 identity changed')
    ck(prov_b7['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov_b7['shared_indexes_at_entry_sha256']==SHARED_SHA and v.sha(v.AUDIT/SHARED_SNAPSHOT)==SHARED_SHA,'B7 frozen exact B6 indexes changed')
    ck(prov_b7['phase7B6_entry_consistency']==dict(original_hashes_matching=827,findings=270,phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B7 entry no longer describes deliveredB6')
    for p,digest in prov_b6['historical_artifact_sha256'].items():
        ck(prov_b7['historical_artifact_sha256'].get(p)==digest,'199-to223 historical continuity failed: '+p)
    ck(v.sha(v.AUDIT/'evidence/checks-07B6.json')==B6_CHECK_SHA,'Genuine archived B6 stdout bytes changed')
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B6.json'))
    ck(saved['validation']['errors']==[] and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False and saved['findings']['total_open_not_remediated']==270 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov_b6['historical_artifact_sha256'],'Protected B6 checks no longer describe delivered270/827/199')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    from validate_pos_totals_part import extend_pos_totals
    with historical_b6_inputs(v,frozen270,texts):extend_pos_totals(v,report,prov_b6,frozen266)
    report['registry_used']=SNAPSHOT;report['validation_scope']='historical-through7B6-270-not-current-state'
    report['phase_7B6_historical_input_mode']='frozen270-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B6_adapter_context']=dict(entry_provenance='evidence/provenance-07B7.json',adapter_protected_artifacts_checked=223,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True)
    report['validation']['limit']+=' HistoricalB6 uses frozen270 and exact delivered B6 indexes IN MEMORY; originalB6 checks bytes stay protected, and current-checker metrics are not their byte replay. No application reference/baseline or historical helper changes.'


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    result=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B7' for x in scope}
    for x in result:
        p=x['path'];x['phase7B7_ranges']=selected.get(p,'none')
        if x['inventory_kind']=='generated-artifact':continue
        if p in selected:
            bucket='7B7-bounded-slices-further-7B8-or-7C-not-closed'
            work='خمسة أجسام وXAMLها ودعم محدد في7B7 فقط؛ لا كل caller/طفل/قالب/سياسة/نشر/قبول. استكمل7B8/7C أو استبعد بسبب؛ all-lines لا يكمل ميزة.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I) or Path(p).stem.removesuffix('.xaml') in NONREGEX_SCREENS:
            bucket='7B8-report-candidate-or-prior-slices-not-feature-closed'
            work='7B8 معلنة لبقية التقارير والمتصلين/الأطفال، ومنها DecisionHelp/SummaryD/UsersRecords؛ لا ترقية من اسم أو launcher أو union إلى اكتمال.'
        else:
            bucket='7B8-or-7C-source-ui-resource-slices-not-complete'
            work='بقية القدرات/المقاطع أو استبعاد مسند؛7C لم تبدأ. مقاطع موارد/تكرار استعلامات ليست إثبات latency/leak/index أو إذن قياس.'
        x['continuation_bucket']=bucket;x['next_scope_work']=work
    return result


def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B7' for x in scope}
    for x in result:
        x['phase7B7_ranges']=selected.get(x['path'],'none')
        if Path(x['path']).name=='FingerPrintDevice.cs':continue
        x['disposition']='7B8-further-slices-contract-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف لفظي لا98 ميزة؛ الجسم المحلي لا كل caller/template/schema/ACL/نشر/قبول.7B8 معلنة ولا إغلاق7B من قراءة helper أو اسم.'
    return result


def build_screen_disposition(inventory,labelled_scopes):
    result=prior_screens(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B7' for x in scope}
    for n,x in enumerate(result,1):
        x['id']=f'SC7B7-{n:02d}';x['phase7B7_body_ranges']=selected.get(x['body_path'],'none')
        x['disposition']='7B8-or-7C-further-slices-contracts-or-reasoned-exclusion-required'
        if x['screen'] in REVIEWED_BODIES and x['body_path'] in selected:
            x['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified'
            x['reason']='الجسم وXAML المحليان قرئا في7B7 ضمن حد صريح؛ لا كل caller/طفل/قالب/سياسة/نشر/قبول. إتاحة أرصدة وعميل لا تثبت من أسمائهما.'
        else:
            x['reason']='حصر/مقاطع سابقة بحسب الحقول فقط؛7B8/7C أو استبعاد مسند. قراءة الأب أو جسر التفاصيل لا تغطي أي طفل، ولا all-lines كامل الميزة.'
    return result


def feature_level_errors(features):return [x.replace('B6','B7') for x in prior_feature_errors(features)]


def witness_metadata_errors(w):
    errors=[]
    for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(key) is not False:errors.append('B7 witness false-only flag: '+key)
    for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(key)) is not int or w[key]!=0:errors.append('B7 witness zero-only count: '+key)
    if w.get('phase')!='7B7-partial-static-audit':errors.append('B7 witness phase mismatch')
    for key in ('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(key)) is not int or w[key]!=22:errors.append('B7 witness count mismatch: '+key)
    return errors


def group_row_errors(previous_text,current_text):
    prior=re.findall(r'^\| G-\d{2,3} \|.*$',previous_text,re.M)
    current=re.findall(r'^\| G-\d{2,3} \|.*$',current_text,re.M)
    return [] if len(prior)==116 and current[:116]==prior else ['Historical G01–116 exact rows changed']


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':v.check(row['id'] in SENTINELS,'Undeclared B7 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B7 inventory-only boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B7',phase=7)


def extend_financial_controls(v,report,prov,frozen270):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==223 and len(frozen270)==270,'B7 protected entry count mismatch')
    identity=report['source_reference_validation']
    ck(identity['audited_application_reference']==v.HEAD and identity['reference_ancestor_of_checkout'] is True and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B7 source/checkout integrity mismatch')
    ck(prov['checkout_head_at_entry']==prov['pushed_documentation_commit_before_continuation']=='d0ae6b318c47451dd7e10a416f07566a7b3f1dc7' and prov['last_pushed_parts']=='1-6 and7A/B1-B5; B6 delivered in working tree, not committed/pushed','B7 actual push/entry boundary changed')
    current=r('findings.csv');new=current[270:];extensions=r('evidence/historical-extensions-07B7.csv')
    ext=v.transition(frozen270,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen270,current,extensions):ck(False,err)
    ck(len(current)==276 and len({x['id'] for x in current})==276,'B7 current count/uniqueness mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(99,105)],'B7 new finding IDs/order mismatch')
    v.distributions(new,{'High':1,'Medium':5},{'confirmed':6},'bounded7B7 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B7 new status/type/followup mismatch: '+x['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B7.md'),re.M)==[(x['id'],x['title']) for x in new],'B7 report titles/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    ck(len(scopes)==19 and len({x['path'] for x in scopes})==19,'B7 scope count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B7 scope path/state mismatch: '+x['path']);v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml.cs','.xaml'):
            p='SmartAuditERP/Form_WPF/'+name+suffix
            ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B7 body/XAML span mismatch: '+p)
    specs=(('acceptance-tests','P7B7T-',37),('feature-implementation-matrix','FE7B7-',31),('report-invariants','INV7B7-',31),('report-reconciliation','RC7B7-',8),('historical-extensions','EX7B7-',18),('handoffs','H7B7-',6),('questions','Q7B7-',6),('continuation-backlog','BK7B7-',10))
    known={x['id'] for x in current}|{f'H7B7-{n:02d}' for n in range(1,7)};tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename+'-07B7.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for key,value in x.items():ck(bool(value),f'Incomplete B7 cell: {x["id"]}.{key}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B7 runtime claim: '+x['id'])
    tests,features,invariants,rc=[tables[k] for k in ('P7B7T-','FE7B7-','INV7B7-','RC7B7-')]
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B7');v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids');v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B7 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B7 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*12+['historical-root-regression']*18+['cross-cutting-contract']*5+['documentary-scope-or-authorization-gate']*2,'B7 plan kind/order mismatch')
    ck([x['finding_ids'] for x in features[:6]]==[x['id'] for x in new],'B7 primary feature/new finding mapping mismatch')
    ck([x['finding_ids'] for x in features[6:24]]==[x['finding_ids'] for x in extensions] and {x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B7 feature/extension mapping mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B7 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B7 RC plan links mismatch: '+x['id'])
        fids={f for fe in features if fe['id'] in x['feature_ids'].split(';') for f in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=fids,'B7 RC finding not in linked features: '+x['id'])
    v.related(tables['Q7B7-'],{x['id'] for x in tables['H7B7-']},'handoff_ids')
    for x in tables['H7B7-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B7 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B7-']:ck(x['status']=='unanswered-no-secrets-requested','B7 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B7-'],1):ck(x['prior_backlog_id']==f'BK7B6-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B8','7C','7B8/7C'} and x['status']!='complete','B7 backlog origin/part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B7-'][2:6]]==['not-started']*4,'B7 accidentally starts7C')
    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv'))]+[(f'7B{n}',r(f'review-scope-07B{n}.csv')) for n in range(1,7)]+[('7B7',scopes)]
    ck(r('evidence/coverage-ledger-07B7.csv')==build_current_ledger(inventory,labelled,v.spans),'B7 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B7.csv');screens=r('evidence/report-screen-disposition-07B7.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B7 filename98 candidate mismatch')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B7 screen35+17 candidate mismatch');v.sequential(screens,'SC7B7-',52)
    for x in screens:
        if x['screen'] in DEFERRED_SCREENS:ck(x['phase7B7_body_ranges']=='none','B7 silently promotes deferred child: '+x['screen'])
    prior={x['path'] for _,s in labelled[:-1] for x in s};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(353,19,9,10,363,464),'B7 prior/selected/overlap/new/union/complement mismatch')
    witness,match=v.recompute('evidence/report-witnesses-07B7.json','tools/check_financial_controls_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks'];v.sequential(algebra,'ALG7B7-',22);v.sequential(lexical,'ST7B7-',22);v.related(algebra+lexical,known)
    for err in witness_metadata_errors(witness):ck(False,err)
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B7 witness fail/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B7 bounded lexical read',phase=7)
    for filename,pattern,expected in (
        ('PHASE-07B7.md',r'^\| (EX7B7-\d{2}) \|',[x['id'] for x in extensions]),
        ('FINANCIAL-CONTROLS-07B7.md',r'^\| (FE7B7-\d{2}) —',[x['id'] for x in features]),
        ('FINANCIAL-CONTROLS-07B7.md',r'^\| (INV7B7-\d{2}) \|',[x['id'] for x in invariants]),
        ('FINANCIAL-CONTROLS-07B7.md',r'^### (RC7B7-\d{2}) —',[x['id'] for x in rc]),
        ('FINANCIAL-CONTROLS-07B7.md',r'^\| (H7B7-\d{2}) —',[x['id'] for x in tables['H7B7-']]),
        ('FINANCIAL-CONTROLS-07B7.md',r'^\| (Q7B7-\d{2}) \|',[x['id'] for x in tables['Q7B7-']]),
        ('FINANCIAL-CONTROLS-07B7.md',r'^\| (BK7B7-\d{2}) \|',[x['id'] for x in tables['BK7B7-']]),
        ('VALIDATION-07B7.md',r'^\| (P7B7T-\d{2}) \|',[x['id'] for x in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,123)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B7 Markdown ID/order mismatch: '+filename)
    pending=False
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B7.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B7 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B7T-\d{2}\b',planids),(r'\bFE7B7-\d{2}\b',feids),(r'\bINV7B7-\d{2}\b',ivids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B7 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            f=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[f[0]]=f[1:]
    for label,expected in (('التراكمي المفتوح',[276,2,175,98,1]),('7B7 — جديدة',[6,0,1,5,0]),('7B7 — إضافة محدودة',[19,9,10,363])):ck(summary.get(label)==list(map(str,expected)),'Current B7 README numeric mismatch: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for err in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,err)
    for filename in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/filename) for x in ('PHASE-07B7.md','7B8','7C','غير مأذونة','d0ae6b3')),'Current index lacks B7/B8/C/8/pushed-checkout boundary: '+filename)
    tools=['check_financial_controls_witnesses.py','validate_financial_controls_part.py','test_financial_controls_audit_validator.py']
    for filename in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B7 audit-tool syntax: '+filename+':'+str(ex))
    completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_financial_controls_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout);count=int(m[1]) if m else None;passed=completed.returncode==0 and count==24;ck(passed,'B7 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_financial_controls_audit_validator.py']=dict(tests_reported=count,expected_tests=24,process_exit_code=completed.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py']+tools})
    report['validation_scope']='current-through7B7-276-plus-frozen-history-not-runtime-certification';report['phase_7_delivery']='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7-partial-not-complete7B-or7';report['phase_7_remaining_parts']=['7B8-announced-not-started','7C-not-started'];report['registry_used']='findings.csv'
    report['findings'].update(phase_7=104,phase_7B7=6,total_open_not_remediated=276,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:19,'phase_7B6_union_frozen':353,'phase_7B7_overlap_with_prior_union':9,'phase_7B7_new_paths':10,'unique_union_not_line_or_execution_coverage':363,'inventory_only_no_selected_scope':464})
    report['phase_7B6_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=223,historical_check_record_overwritten=False,genuine_b6_check_sha256_unchanged=B6_CHECK_SHA,partial7B7_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all270=True,next_phase_replans_during_partial7={})
    report['historical_artifact_sha256']=prov['historical_artifact_sha256'];report['date_semantics']=prov['date_semantics']
    report['evidence_rows'].update(dict(phase_7B7_feature_rows_not_completed_features=31,phase_7B7_invariants_not_passed_tests=31,phase_7B7_source_reconciliation_contracts_not_executed_financial_acceptance=8,phase_7B7_unexecuted_acceptance_or_gate_plans=37,phase_7B7_direct_finding_plans=12,phase_7B7_historical_regression_plans=18,phase_7B7_cross_contract_plans=5,phase_7B7_documentary_scope_authorization_gate_plans=2,phase_7B7_historical_extensions_not_new_findings=18,phase_7B7_unresolved_handoffs=6,phase_7B7_unanswered_questions=6,phase_7B7_continuation_groups_not_complete=10,phase_7B7_original_paths_in_ledger=827,phase_7B7_filename_candidates_not_feature_count=98,phase_7B7_screen_candidates_35_regex_plus17_curated_not_feature_count=52,phase_7B7_independent_illustrations_not_erp_tests=22,phase_7B7_bounded_literal_checks_not_application_tests=22,phase_7B7_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only original827 paths/hashes, source10ba ancestry/docs-only-checkout net tree delta, protected223 hashes, exact270 historical registry cores/evidence tails/ALL followups and G01–116 rows, IDs/distributions/links/source bounds/scope inclusion, inventory/candidate/range bookkeeping, independent hand-selected documentary illustrations, bounded lexical observations and isolated synthetic checker tests ONLY. A/B1/B2/B3/B4/B5/B6 each use OWN frozen registries/indexes, never current276 or live shared texts. Historical files/checks/helpers/baselines unchanged; current metrics not archived byte replay. Five local bodies/XAML do not prove all callers/children/templates/deployment, policy, ACL or full feature coverage. InvsProfit all-branches actually clears selection and print DTO explicitly copies signed summaries: no blanket P7-088/P7-093 extension. ItemsBalances/ActCust reachability remains unresolved, not proved user-visible. UI Custom wiring absence does not establish SDK default text.7B8 announced,7C not started,8 unauthorized. No ERP/C#/SQL/WPF/Office/COM/SDK/provider/device/formula execution, remediation, financial/security/compliance certificate, all-bugs claim or production/secret data.'
