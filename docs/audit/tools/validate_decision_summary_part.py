#!/usr/bin/env python3
"""Read-only PARTIAL7B8 documentary checks, not ERP or acceptance tests.

B7 receives its frozen276 registry and exact delivered shared texts IN MEMORY.
All246 prior nonmutable artifacts, original827 source hashes, all historical
followups and G01..122 rows stay protected. Local source10ba and historical
remote docs pushd0ae are separate identities; no history is reconstructed.
Three local bodies/XAML do not close their children/callers/outputs or7B/7.
"""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import collections,re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_financial_controls_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors as prior_feature_errors)
from validate_pos_totals_part import NONREGEX_SCREENS

SCOPE_FILE='review-scope-07B8.csv'
PART_DOCS=('PHASE-07B8.md','DECISION-SUMMARY-LOGS-07B8.md','VALIDATION-07B8.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B7.csv'
SNAPSHOT_SHA='1b9b7bbd35723035fc69431a46a9b6033306792c5c5ee13d9c15cc6c03c2dc80'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B7.json'
SHARED_SHA='5bee3da15f6342cd7e184b9d485931233acac2d110788d1cd4ddcb8f770a27a9'
B7_CHECK_SHA='25043dbf69013f010a3f063938ea5377862bb9c11d02ea01447a5d51a7ded5c3'
EXTENDED_FINDINGS={'P1-004','P1-013','P1-030','P1-033','P2-010','P3-023','P7-039','P7-040','P7-045','P7-046','P7-048','P7-049','P7-054','P7-056','P7-057','P7-080','P7-084'}
REVIEWED_BODIES=('frmDecisionHelp','frmSummaryD','frmrptUsersRecords')
HISTORICAL_NAME_ALIASES={'frmUsersRecords':'frmrptUsersRecords'}
# These rows are documentary/inventory gates, never source-implementation claims.
SENTINELS={'FE7B8-27','INV7B8-27','FE7B8-28','INV7B8-28','H7B8-06','Q7B8-06','P7B8T-31','P7B8T-32'}
TABLE_SPECS=(('acceptance-tests','P7B8T-',32),('feature-implementation-matrix','FE7B8-',28),('report-invariants','INV7B8-',28),('report-reconciliation','RC7B8-',8),('historical-extensions','EX7B8-',17),('handoffs','H7B8-',6),('questions','Q7B8-',6),('continuation-backlog','BK7B8-',10))


@contextmanager
def historical_b7_inputs(v,frozen276,shared_texts):
    if len(frozen276)!=276 or len({x['id'] for x in frozen276})!=276:
        raise ValueError('Exactly276 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen276,shared_texts):yield


def validate_frozen_b7(v,report,prov_b7,frozen270,prov_b8,frozen276):
    ck=v.check
    ck(prov_b8['registry_at_entry_snapshot']==SNAPSHOT and prov_b8['registry_at_entry_sha256']==SNAPSHOT_SHA,'B8 frozen276 identity changed')
    ck(prov_b8['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov_b8['shared_indexes_at_entry_sha256']==SHARED_SHA and v.sha(v.AUDIT/SHARED_SNAPSHOT)==SHARED_SHA,'B8 exact B7 indexes changed')
    ck(prov_b8['phase7B7_entry_consistency']==dict(original_hashes_matching=827,findings=276,phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B8 entry no longer describes deliveredB7')
    for p,digest in prov_b7['historical_artifact_sha256'].items():
        ck(prov_b8['historical_artifact_sha256'].get(p)==digest,'223-to246 historical continuity failed: '+p)
    ck(prov_b8['genuine_B7_check_sha256']==B7_CHECK_SHA and v.sha(v.AUDIT/'evidence/checks-07B7.json')==B7_CHECK_SHA,'Genuine archived B7 stdout changed')
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B7.json'))
    ck(saved['validation']['errors']==[] and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False and saved['findings']['total_open_not_remediated']==276 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov_b7['historical_artifact_sha256'],'Archived B7 checks no longer describe genuine276/827/223')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    from validate_financial_controls_part import extend_financial_controls
    with historical_b7_inputs(v,frozen276,texts):extend_financial_controls(v,report,prov_b7,frozen270)
    report['registry_used']=SNAPSHOT;report['validation_scope']='historical-through7B7-276-not-current-state'
    report['phase_7B7_historical_input_mode']='frozen276-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B7_adapter_context']=dict(entry_provenance='evidence/provenance-07B8.json',adapter_protected_artifacts_checked=246,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True,archived_checkout_metadata_not_rewritten_for_current_checkout=True)
    report['validation']['limit']+=' HistoricalB7 uses frozen276/exact delivered indexes IN MEMORY, not live registry/indexes. Archived B7 stdout stays byte-protected; current checkout/source-delta metadata may differ, not an archived byte replay or rebaseline.'


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    result=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B8' for x in scope}
    for x in result:
        p=x['path'];x['phase7B8_ranges']=selected.get(p,'none')
        if x['inventory_kind']=='generated-artifact':continue
        if p in selected:
            bucket='7B8-bounded-slices-further-7B9-or-7C-not-closed'
            work='ثلاثة أجسام/XAML وعقود دعم محددة في7B8 فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول.7B9/7C أو استبعاد مسند، ولا ترقية all-lines إلى ميزة مكتملة.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I) or Path(p).stem.removesuffix('.xaml') in NONREGEX_SCREENS:
            bucket='7B9-report-candidate-or-prior-slices-not-feature-closed'
            work='7B9 معلنة للباقي من عقود التقارير والمتصلين/الأطفال/المخرجات أو استبعادات مسندة؛ لا اكتمال من اسم/حصر/loader.7C لم تبدأ.'
        else:
            bucket='7B9-or-7C-source-ui-resource-slices-not-complete'
            work='بقية القدرات/المقاطع أو استبعاد مسند؛7C لم تبدأ، ولا Thread/Fill/loop دليل قياس latency/leak/index أو إذن تشغيل.'
        x['continuation_bucket']=bucket;x['next_scope_work']=work
    return result


def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B8' for x in scope}
    for x in result:
        x['phase7B8_ranges']=selected.get(x['path'],'none')
        if Path(x['path']).name=='FingerPrintDevice.cs':continue
        x['disposition']='7B9-further-slices-contract-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف لفظي لا98 ميزة؛ الجسم المحلي لا كل caller/child/template/schema/ACL/نشر/قبول. لا إغلاق7B من قراءة ثلاثة أجسام أخرى؛7B9 معلنة.'
    return result


def build_screen_disposition(inventory,labelled_scopes):
    result=prior_screens(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B8' for x in scope}
    for n,x in enumerate(result,1):
        x['id']=f'SC7B8-{n:02d}';x['phase7B8_body_ranges']=selected.get(x['body_path'],'none')
        x['historical_name_mapping']='frmUsersRecords means frmrptUsersRecords; no such separate source body; historical artifacts unchanged' if x['screen']=='frmrptUsersRecords' else 'none-needed'
        x['disposition']='7B9-or-7C-further-contracts-or-reasoned-exclusion-required'
        if x['screen'] in REVIEWED_BODIES and x['body_path'] in selected:
            x['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified'
            x['reason']='جسم وXAML محليان في7B8 مع support منتقى؛ الإتاحة والخيط والمخطط/الهوية/القالب/السياسة ما زالت حواجز منفصلة. لا كل مدخل أوطفل أو مخرج مقبول.'
        else:
            x['reason']='حصر أو مقاطع سابقة بحسب الحقول؛ لا ترقية بقية جسم/طفل من مراجعة الأب أو Query/Nav slice؛7B9/7C أو استبعاد مسند، لا اكتمال7.'
    return result


def feature_level_errors(features):return [x.replace('B7','B8') for x in prior_feature_errors(features)]


def witness_metadata_errors(w):
    errors=[]
    for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(key) is not False:errors.append('B8 witness false-only flag: '+key)
    for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(key)) is not int or w[key]!=0:errors.append('B8 witness zero-only count: '+key)
    if w.get('phase')!='7B8-partial-static-audit':errors.append('B8 witness phase mismatch')
    for key in ('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(key)) is not int or w[key]!=20:errors.append('B8 witness count mismatch: '+key)
    return errors


def group_row_errors(previous_text,current_text):
    prior=re.findall(r'^\| G-\d{2,3} \|.*$',previous_text,re.M)
    current=re.findall(r'^\| G-\d{2,3} \|.*$',current_text,re.M)
    return [] if len(prior)==122 and current[:122]==prior else ['Historical G01–122 exact rows changed']


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':v.check(row['id'] in SENTINELS,'Undeclared B8 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B8 documentary/inventory boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B8',phase=7)


def extend_decision_summary(v,report,prov,frozen276):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==246 and len(frozen276)==276,'B8 protected entry count mismatch')
    identity=report['source_reference_validation']
    ck(identity['audited_application_reference']==v.HEAD and identity['reference_ancestor_of_checkout'] is True and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B8 source/checkout integrity mismatch')
    ck(prov['checkout_head_at_entry']==v.HEAD and prov['remote_current_branch_tip_observed_at_entry']==prov['prior_delivery_checkout_saved_in_B7']=='d0ae6b318c47451dd7e10a416f07566a7b3f1dc7' and prov['local_prior_docs_commit_object_available_at_entry'] is False,'B8 actual entry/remote observation boundary changed')
    ck(prov['erp_runtime_tests_executed']==0 and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False,'B8 entry wrongly authorizes/executes runtime or remediation')
    current=r('findings.csv');new=current[276:];extensions=r('evidence/historical-extensions-07B8.csv')
    ext=v.transition(frozen276,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen276,current,extensions):ck(False,err)
    ck(len(current)==280 and len({x['id'] for x in current})==280,'B8 current count/uniqueness mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(105,109)],'B8 new finding IDs/order mismatch')
    v.distributions(new,{'Medium':4},{'confirmed':3,'potential':1},'bounded7B8 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B8 new status/type/followup mismatch: '+x['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B8.md'),re.M)==[(x['id'],x['title']) for x in new],'B8 report titles/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    ck(len(scopes)==23 and len({x['path'] for x in scopes})==23,'B8 scope count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B8 scope path/state mismatch: '+x['path']);v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        for suffix in ('.xaml.cs','.xaml'):
            p='SmartAuditERP/Form_WPF/'+name+suffix
            ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B8 body/XAML span mismatch: '+p)
    specs=TABLE_SPECS
    known={x['id'] for x in current}|{f'H7B8-{n:02d}' for n in range(1,7)};tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename+'-07B8.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for key,value in x.items():ck(bool(value),f'Incomplete B8 cell: {x["id"]}.{key}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B8 runtime claim: '+x['id'])
    tests,features,invariants,rc=[tables[k] for k in ('P7B8T-','FE7B8-','INV7B8-','RC7B8-')]
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B8');v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids');v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B8 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B8 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*8+['historical-root-regression']*17+['cross-cutting-contract']*5+['documentary-scope-or-authorization-gate']*2,'B8 plan kind/order mismatch')
    ck([x['finding_ids'] for x in features[:4]]==[x['id'] for x in new],'B8 primary feature/new finding mapping mismatch')
    ck([x['finding_ids'] for x in features[4:21]]==[x['finding_ids'] for x in extensions] and {x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B8 feature/extension mapping mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B8 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B8 RC plan links mismatch: '+x['id'])
        fids={f for fe in features if fe['id'] in x['feature_ids'].split(';') for f in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=fids,'B8 RC finding not in linked features: '+x['id'])
    v.related(tables['Q7B8-'],{x['id'] for x in tables['H7B8-']},'handoff_ids')
    for x in tables['H7B8-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B8 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B8-']:ck(x['status']=='unanswered-no-secrets-requested','B8 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B8-'],1):ck(x['prior_backlog_id']==f'BK7B7-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B9','7C','7B9/7C'} and x['status']!='complete','B8 backlog origin/part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B8-'][2:6]]==['not-started']*4,'B8 accidentally starts7C')
    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv'))]+[(f'7B{n}',r(f'review-scope-07B{n}.csv')) for n in range(1,8)]+[('7B8',scopes)]
    ck(r('evidence/coverage-ledger-07B8.csv')==build_current_ledger(inventory,labelled,v.spans),'B8 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B8.csv');screens=r('evidence/report-screen-disposition-07B8.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B8 filename98 candidate mismatch')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B8 screen35+17 candidate mismatch');v.sequential(screens,'SC7B8-',52)
    byscreen={x['screen']:x for x in screens}
    ck('frmUsersRecords' not in byscreen and all(name in byscreen for name in REVIEWED_BODIES),'B8 wrong actual screen identity/alias created')
    for name in REVIEWED_BODIES:ck(byscreen[name]['phase7B8_body_ranges']!='none' and byscreen[name]['coverage_level']=='bounded-local-body-and-xaml-not-whole-feature-certified','B8 local body incorrectly deferred or whole-feature promoted: '+name)
    ck('historical artifacts unchanged' in byscreen['frmrptUsersRecords']['historical_name_mapping'],'B8 actual log name mapping absent')
    prior={x['path'] for _,s in labelled[:-1] for x in s};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(363,23,13,10,373,454),'B8 prior/selected/overlap/new/union/complement mismatch')
    witness,match=v.recompute('evidence/report-witnesses-07B8.json','tools/check_decision_summary_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks'];v.sequential(algebra,'ALG7B8-',20);v.sequential(lexical,'ST7B8-',20);v.related(algebra+lexical,known)
    for err in witness_metadata_errors(witness):ck(False,err)
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B8 witness fail/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B8 bounded lexical read',phase=7)
    for filename,pattern,expected in (
        ('PHASE-07B8.md',r'^\| (EX7B8-\d{2}) \|',[x['id'] for x in extensions]),
        ('DECISION-SUMMARY-LOGS-07B8.md',r'^\| (FE7B8-\d{2}) —',[x['id'] for x in features]),
        ('DECISION-SUMMARY-LOGS-07B8.md',r'^\| (INV7B8-\d{2}) \|',[x['id'] for x in invariants]),
        ('DECISION-SUMMARY-LOGS-07B8.md',r'^### (RC7B8-\d{2}) —',[x['id'] for x in rc]),
        ('DECISION-SUMMARY-LOGS-07B8.md',r'^\| (H7B8-\d{2}) —',[x['id'] for x in tables['H7B8-']]),
        ('DECISION-SUMMARY-LOGS-07B8.md',r'^\| (Q7B8-\d{2}) \|',[x['id'] for x in tables['Q7B8-']]),
        ('DECISION-SUMMARY-LOGS-07B8.md',r'^\| (BK7B8-\d{2}) \|',[x['id'] for x in tables['BK7B8-']]),
        ('VALIDATION-07B8.md',r'^\| (P7B8T-\d{2}) \|',[x['id'] for x in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,129)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B8 Markdown ID/order mismatch: '+filename)
    pending=False
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B8.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B8 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B8T-\d{2}\b',planids),(r'\bFE7B8-\d{2}\b',feids),(r'\bINV7B8-\d{2}\b',ivids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B8 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            f=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[f[0]]=f[1:]
    for label,expected in (('التراكمي المفتوح',[280,2,175,102,1]),('7B8 — جديدة',[4,0,0,4,0]),('7B8 — إضافة محدودة',[23,13,10,373])):ck(summary.get(label)==list(map(str,expected)),'Current B8 README numeric mismatch: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for err in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,err)
    for filename in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/filename) for x in ('PHASE-07B8.md','7B9','7C','غير مأذونة','d0ae6b3','10ba215')),'Current index lacks B8/B9/C/8/pushed-checkout boundary: '+filename)
    tools=['check_decision_summary_witnesses.py','validate_decision_summary_part.py','test_decision_summary_audit_validator.py']
    for filename in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B8 audit-tool syntax: '+filename+':'+str(ex))
    completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_decision_summary_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout);count=int(m[1]) if m else None;passed=completed.returncode==0 and count==28;ck(passed,'B8 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_decision_summary_audit_validator.py']=dict(tests_reported=count,expected_tests=28,process_exit_code=completed.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py']+tools})
    report['validation_scope']='current-through7B8-280-plus-frozen-history-not-runtime-certification'
    report['phase_7_delivery']='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8-partial-not-complete7B-or7'
    report['phase_7_remaining_parts']=['7B9-announced-not-started','7C-not-started'];report['registry_used']='findings.csv'
    report['findings'].update(phase_7=108,phase_7B8=4,total_open_not_remediated=280,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:23,'phase_7B7_union_frozen':363,'phase_7B8_overlap_with_prior_union':13,'phase_7B8_new_paths':10,'unique_union_not_line_or_execution_coverage':373,'inventory_only_no_selected_scope':454})
    report['phase_7B7_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=246,historical_check_record_overwritten=False,genuine_b7_check_sha256_unchanged=B7_CHECK_SHA,partial7B8_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all276=True,next_phase_replans_during_partial7={},historical_remaining_parts_and_checkout_are_observations_at_delivery_not_current=True)
    report['historical_artifact_sha256']=prov['historical_artifact_sha256'];report['date_semantics']=prov['date_semantics']
    report['phase_7B8_entry_checkout_observation_not_new_source_reference']={k:prov[k] for k in ('checkout_head_at_entry','remote_current_branch_tip_observed_at_entry','prior_delivery_checkout_saved_in_B7','local_prior_docs_commit_object_available_at_entry','checkout_context')}
    report['evidence_rows'].update(dict(phase_7B8_feature_rows_not_completed_features=28,phase_7B8_invariants_not_passed_tests=28,phase_7B8_source_reconciliation_contracts_not_executed_financial_acceptance=8,phase_7B8_unexecuted_acceptance_or_gate_plans=32,phase_7B8_direct_finding_plans=8,phase_7B8_historical_regression_plans=17,phase_7B8_cross_contract_plans=5,phase_7B8_documentary_scope_authorization_gate_plans=2,phase_7B8_historical_extensions_not_new_findings=17,phase_7B8_unresolved_handoffs=6,phase_7B8_unanswered_questions=6,phase_7B8_continuation_groups_not_complete=10,phase_7B8_original_paths_in_ledger=827,phase_7B8_filename_candidates_not_feature_count=98,phase_7B8_screen_candidates_35_regex_plus17_curated_not_feature_count=52,phase_7B8_independent_illustrations_not_erp_tests=20,phase_7B8_bounded_literal_checks_not_application_tests=20,phase_7B8_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only original827 paths/hashes; source10ba ancestry/net docs-only-checkout tree delta; protected246 prior nonmutable hashes; exact276 historical cores/ALLnext_phase and17 declared evidence tails; exact G01..122 rows; IDs/distributions/links/source bounds/scope inclusion; inventory/candidate/range bookkeeping; independent hand-selected documentary NULL/key/schedule/event-order/arithmetic contrasts and bounded lexical observations; isolated synthetic checker tests ONLY. Historical A/B1..B7 each use OWN frozen registries/exact indexes IN MEMORY, never current280/live indexes; archived files/checks/helpers/baselines unchanged, current metrics NOT archived byte replay. Entry actual checkout10ba differs from historical docs pushd0ae; no fetch/reset/reconstruction/rebaseline/commit/push/PR to manufacture metadata. Three bodies/local XAML/support are not all callers/children/templates/schema/ACL/deployment. DecisionHelp downstream movement calculations CONDITIONAL on passing earlier WPF worker-control access gate P7-054. No blanket P7-041 quantity-times-price claim, P7-061 local-number-only receipt navigation, no-REPX-load in DecisionHelp or off-thread-controls in logs. P7-108 consumer timing/partial-file effect remains POTENTIAL, P7-049 remains POTENTIAL. Producer callsites exist; cloud/offline EmpID/appender mapping, privacy/retention/event completeness and actual menu enablement remain unresolved.7B9 announced,7C not started,8 unauthorized. No ERP/C#/SQL/WPF/Office/COM/SDK/provider/device/formula/IO export/shell execution, remediation, real business/secret data, financial/security/compliance certificate or all-bugs/whole-feature completeness claim.'
