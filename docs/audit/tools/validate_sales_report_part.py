#!/usr/bin/env python3
"""Read-only additive PARTIAL7B5 documentary checks, NOT ERP acceptance.

B4's protected checker sees ONLY frozen261 and its exact three shared indexes
in memory at the original logical paths. No historical artifact is rewritten.
Current checks cover append-only registry cores/tails/follow-ups, bounded scope,
links/IDs, range bookkeeping, manual models and synthetic checker fixtures.
No C#/SQL/WPF/Office/provider code is imported, built, interpreted or executed.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_invoice_analysis_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors as prior_feature_errors,
    NONREGEX_SCREENS)

SCOPE_FILE='review-scope-07B5.csv'
PART_DOCS=('PHASE-07B5.md','SALES-DETAIL-REPORTS-07B5.md','VALIDATION-07B5.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B4.csv'
SNAPSHOT_SHA='a951b1a4b2e3df5342f82e9a69736a3cf37e7507cb55809d5e5b628e9ca6b258'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B4.json'
EXTENDED_FINDINGS={'P1-004','P1-011','P1-013','P1-030','P1-033','P2-001','P2-010','P2-011','P3-001','P3-002','P3-003','P3-006','P3-023','P7-040','P7-045','P7-046','P7-048','P7-049','P7-067','P7-080','P7-083','P7-085','P7-086','P7-088'}
SENTINELS={'FE7B5-34','FE7B5-35','INV7B5-21','INV7B5-22','H7B5-06','Q7B5-06','P7B5T-38','P7B5T-39'}
REVIEWED_BODIES=('frmRptInvSalesDetails','frmRptInvSalesDetailsPos','frmRptInvSalesDetailsPosAndroid','frmRptItemsSalesDetails','frmRptItemsSalesDetailsPOS')


@contextmanager
def historical_b4_inputs(v,frozen261,shared_texts):
    if len(frozen261)!=261 or len({x['id'] for x in frozen261})!=261:
        raise ValueError('Exactly261 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen261,shared_texts):yield


def validate_frozen_b4(v,report,prov_b4,frozen248,prov_b5,frozen261):
    ck=v.check
    ck(prov_b5['registry_at_entry_snapshot']==SNAPSHOT and prov_b5['registry_at_entry_sha256']==SNAPSHOT_SHA,'B5 frozen261 identity changed')
    ck(prov_b5['shared_indexes_at_entry']==SHARED_SNAPSHOT,'B5 frozen B4 indexes identity changed')
    ck(prov_b5['phase7B4_entry_consistency']==dict(original_hashes_matching=827,findings=261,phase_7_delivery='7A+7B1+7B2+7B3+7B4-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B5 entry metadata no longer describes delivered B4')
    for path,digest in prov_b4['historical_artifact_sha256'].items():
        ck(prov_b5['historical_artifact_sha256'].get(path)==digest,'155-to178 historical continuity failed: '+path)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B4.json'))
    ck(saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==261 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov_b4['historical_artifact_sha256'],'Protected B4 checks no longer describe delivered261/827/155')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    from validate_invoice_analysis_part import extend_invoice_analysis
    with historical_b4_inputs(v,frozen261,texts):extend_invoice_analysis(v,report,prov_b4,frozen248)
    report['registry_used']=SNAPSHOT
    report['validation_scope']='historical-through7B4-261-not-current-state'
    report['phase_7B4_historical_input_mode']='frozen261-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B4_adapter_context']=dict(entry_provenance='evidence/provenance-07B5.json',adapter_protected_artifacts_checked=178,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True)
    report['validation']['limit']+=' HistoricalB4 uses frozen261 and exact B4 shared-index texts IN MEMORY. Remaining-part labels are historical, not current. New-checker metrics need not reproduce protected check bytes; no historical file is rewritten.'


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    result=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B5' for x in scope}
    for x in result:
        p=x['path'];x['phase7B5_ranges']=selected.get(p,'none')
        if x['inventory_kind']=='generated-artifact':continue
        if p in selected:
            bucket='7B5-bounded-slices-further-7B6-or-7C-not-closed'
            work='خمسة أجسام تقارير ومقاطع دعم/XAML محددة في7B5؛ لا كل caller/template/سياسة/نشر/قبول. استكمل7B6/7C أو استبعد بسبب؛ لا اكتمال من اتحاد الأسطر.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I) or Path(p).stem.removesuffix('.xaml') in NONREGEX_SCREENS:
            bucket='7B6-report-candidate-or-prior-slices-not-feature-closed'
            work='7B6 معلنة لبقية المالية/الإخراج وغيرregex والأطفال، ومنها frmItemsalesdetailsPos المختلف و frmActsInvTotal/frmNkdTotSalePurch؛ caller/helper لا يغطيها.'
        else:
            bucket='7B6-or-7C-source-ui-resource-slices-not-complete'
            work='بقية المقاطع/القدرات أو استبعاد مسند؛7C لم تبدأ. مؤشرات موارد/أداء مصدرية لا تسرب/latency/index مثبت أو إذن تشغيل.'
        x['continuation_bucket']=bucket;x['next_scope_work']=work
    return result


def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B5' for x in scope}
    for x in result:
        x['phase7B5_ranges']=selected.get(x['path'],'none')
        if Path(x['path']).name=='FingerPrintDevice.cs':continue
        x['disposition']='7B6-further-slices-contract-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف لفظي لا98 ميزة؛ مقاطع7B5/التاريخ لا تغطي كل caller/template/schema/ACL/نشر/قبول.7B6 معلنة، وقد تلزم أجزاء أخرى قبل إغلاق7.'
    return result


def build_screen_disposition(inventory,labelled_scopes):
    result=prior_screens(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B5' for x in scope}
    for n,x in enumerate(result,1):
        x['id']=f'SC7B5-{n:02d}';x['phase7B5_body_ranges']=selected.get(x['body_path'],'none')
        x['disposition']='7B6-or-7C-further-slices-contracts-or-reasoned-exclusion-required'
        if x['screen'] in REVIEWED_BODIES:
            x['coverage_level']='bounded-local-body-and-selected-xaml-not-whole-feature-certified'
            x['reason']='جسم تقرير محلي ومقاطع XAML/دعم محددة في7B5؛ لا كل طفل/قالب/سياسة/نشر أو قبول. تفويض وبناء ومخطط بوابات منفصلة.'
        else:x['reason']=x['reason'].replace('7B5/7C','7B6/7C')
    return result


def feature_level_errors(features):
    return [x.replace('B4','B5') for x in prior_feature_errors(features)]


def witness_metadata_errors(w):
    errors=[]
    for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(key) is not False:errors.append('B5 witness false-only flag: '+key)
    for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(key)) is not int or w[key]!=0:errors.append('B5 witness zero-only execution count: '+key)
    if w.get('phase')!='7B5-partial-static-audit':errors.append('B5 witness phase mismatch')
    if w.get('illustration_count')!=20 or w.get('static_lexical_contract_check_count')!=20:errors.append('B5 witness count mismatch')
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':v.check(row['id'] in SENTINELS,'Undeclared B5 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B5 inventory-only boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B5',phase=7)


def extend_sales_report(v,report,prov,frozen261):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==178 and len(frozen261)==261,'B5 protected entry count mismatch')
    current=r('findings.csv');new=current[261:];extensions=r('evidence/historical-extensions-07B5.csv')
    ext=v.transition(frozen261,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen261,current,extensions):ck(False,err)
    ck(len(current)==266 and len({x['id'] for x in current})==266,'B5 current count/uniqueness mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(90,95)],'B5 new finding IDs/order mismatch')
    v.distributions(new,{'High':3,'Medium':2},{'confirmed':5},'bounded7B5 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B5 classification/status/followup mismatch: '+x['id'])
    heads=re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B5.md'),re.M)
    ck(heads==[(x['id'],x['title']) for x in new],'B5 report title/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    ck(len(scopes)==26 and len({x['path'] for x in scopes})==26,'B5 scope count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B5 scope path/state mismatch: '+x['path']);v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        p='SmartAuditERP/Form_WPF/'+name+'.xaml.cs'
        ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B5 body span mismatch: '+name)
    ck('SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs' not in scope,'B5 promoted distinct detailed-POS child without its review')
    specs=(('acceptance-tests','P7B5T-',39),('feature-implementation-matrix','FE7B5-',35),('report-invariants','INV7B5-',22),('report-reconciliation','RC7B5-',8),('historical-extensions','EX7B5-',24),('handoffs','H7B5-',6),('questions','Q7B5-',6),('continuation-backlog','BK7B5-',10))
    known={x['id'] for x in current}|{f'H7B5-{n:02d}' for n in range(1,7)};tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename+'-07B5.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for key,value in x.items():ck(bool(value),f'Incomplete B5 cell: {x["id"]}.{key}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B5 runtime claim: '+x['id'])
    tests,features,invariants,rc=[tables[k] for k in ('P7B5T-','FE7B5-','INV7B5-','RC7B5-')]
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B5');v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids');v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B5 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B5 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*10+['historical-root-regression']*24+['cross-cutting-contract']*3+['documentary-scope-or-authorization-gate']*2,'B5 plan kinds/order mismatch')
    ck([x['finding_ids'] for x in features[:5]]==[x['id'] for x in new],'B5 primary feature/finding mapping mismatch')
    ck([x['finding_ids'] for x in features[5:29]]==[x['finding_ids'] for x in extensions] and {x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B5 historical feature/extension mapping mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B5 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B5 RC plan links mismatch: '+x['id'])
        findings={f for fe in features if fe['id'] in x['feature_ids'].split(';') for f in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=findings,'B5 RC finding not in linked features: '+x['id'])
    v.related(tables['Q7B5-'],{x['id'] for x in tables['H7B5-']},'handoff_ids')
    for x in tables['H7B5-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B5 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B5-']:ck(x['status']=='unanswered-no-secrets-requested','B5 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B5-'],1):ck(x['prior_backlog_id']==f'BK7B4-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B6','7C','7B6/7C'} and x['status']!='complete','B5 backlog origin/part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B5-'][2:6]]==['not-started']*4,'B5 accidentally starts7C')
    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv'))]+[(f'7B{n}',r(f'review-scope-07B{n}.csv')) for n in range(1,5)]+[('7B5',scopes)]
    ck(r('evidence/coverage-ledger-07B5.csv')==build_current_ledger(inventory,labelled,v.spans),'B5 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B5.csv');screens=r('evidence/report-screen-disposition-07B5.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B5 filename98 candidate mismatch')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B5 screen35+17 candidate mismatch');v.sequential(screens,'SC7B5-',52)
    prior={x['path'] for _,scope0 in labelled[:-1] for x in scope0};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(334,26,13,13,347,480),'B5 prior/selected/overlap/new/union/complement mismatch')
    witness,match=v.recompute('evidence/report-witnesses-07B5.json','tools/check_sales_report_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks'];v.sequential(algebra,'ALG7B5-',20);v.sequential(lexical,'ST7B5-',20);v.related(algebra+lexical,known)
    for err in witness_metadata_errors(witness):ck(False,err)
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B5 witness fail/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B5 bounded lexical read',phase=7)
    for filename,pattern,expected in (
        ('PHASE-07B5.md',r'^\| (EX7B5-\d{2}) \|',[x['id'] for x in extensions]),
        ('SALES-DETAIL-REPORTS-07B5.md',r'^\| (FE7B5-\d{2}) —',[x['id'] for x in features]),
        ('SALES-DETAIL-REPORTS-07B5.md',r'^\| (INV7B5-\d{2}) \|',[x['id'] for x in invariants]),
        ('SALES-DETAIL-REPORTS-07B5.md',r'^### (RC7B5-\d{2}) —',[x['id'] for x in rc]),
        ('SALES-DETAIL-REPORTS-07B5.md',r'^\| (H7B5-\d{2}) —',[x['id'] for x in tables['H7B5-']]),
        ('SALES-DETAIL-REPORTS-07B5.md',r'^\| (Q7B5-\d{2}) \|',[x['id'] for x in tables['Q7B5-']]),
        ('SALES-DETAIL-REPORTS-07B5.md',r'^\| (BK7B5-\d{2}) \|',[x['id'] for x in tables['BK7B5-']]),
        ('VALIDATION-07B5.md',r'^\| (P7B5T-\d{2}) \|',[x['id'] for x in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,111)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B5 Markdown ID/order mismatch: '+filename)
    pending=False
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B5.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B5 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B5T-\d{2}\b',planids),(r'\bFE7B5-\d{2}\b',feids),(r'\bINV7B5-\d{2}\b',ivids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B5 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            fields=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[fields[0]]=fields[1:]
    for label,expected in (('التراكمي المفتوح',[266,2,173,90,1]),('7B5 — جديدة',[5,0,3,2,0]),('7B5 — إضافة محدودة',[26,13,13,347])):ck(summary.get(label)==list(map(str,expected)),'Current B5 README numeric mismatch: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];oldgroups=re.findall(r'^\| G-\d{2,3} \|.*$',texts['IMPROVEMENTS.md'],re.M);livegroups=re.findall(r'^\| G-\d{2,3} \|.*$',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)
    ck(len(oldgroups)==104 and livegroups[:104]==oldgroups,'Historical G01–104 bodies changed')
    for filename in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/filename) for x in ('PHASE-07B5.md','7B6','7C','غير مأذونة')),'Current index lacks B5/B6/C/8 boundary: '+filename)
    tools=['check_sales_report_witnesses.py','validate_sales_report_part.py','test_sales_report_audit_validator.py']
    for filename in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B5 audit-tool syntax: '+filename+':'+str(ex))
    completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_sales_report_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout);count=int(m[1]) if m else None;passed=completed.returncode==0 and count==22;ck(passed,'B5 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_sales_report_audit_validator.py']=dict(tests_reported=count,expected_tests=22,process_exit_code=completed.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py']+tools})
    report['validation_scope']='current-through7B5-266-plus-frozen-history-not-runtime-certification';report['phase_7_delivery']='7A+7B1+7B2+7B3+7B4+7B5-partial-not-complete7B-or7';report['phase_7_remaining_parts']=['7B6-announced-not-started','7C-not-started'];report['registry_used']='findings.csv'
    report['findings'].update(phase_7=94,phase_7B5=5,total_open_not_remediated=266,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:26,'phase_7B4_union_frozen':334,'phase_7B5_overlap_with_prior_union':13,'phase_7B5_new_paths':13,'unique_union_not_line_or_execution_coverage':347,'inventory_only_no_selected_scope':480})
    report['phase_7B4_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=178,historical_check_record_overwritten=False,partial7B5_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all261=True,next_phase_replans_during_partial7={})
    report['historical_artifact_sha256']=prov['historical_artifact_sha256'];report['date_semantics']=prov['date_semantics']
    report['evidence_rows'].update(dict(phase_7B5_feature_rows_not_completed_features=35,phase_7B5_invariants_not_passed_tests=22,phase_7B5_source_reconciliation_contracts_not_executed_financial_acceptance=8,phase_7B5_unexecuted_acceptance_or_gate_plans=39,phase_7B5_direct_finding_plans=10,phase_7B5_historical_regression_plans=24,phase_7B5_cross_contract_plans=3,phase_7B5_documentary_scope_authorization_gate_plans=2,phase_7B5_historical_extensions_not_new_findings=24,phase_7B5_unresolved_handoffs=6,phase_7B5_unanswered_questions=6,phase_7B5_continuation_groups_not_complete=10,phase_7B5_original_paths_in_ledger=827,phase_7B5_filename_candidates_not_feature_count=98,phase_7B5_screen_candidates_35_regex_plus17_curated_not_feature_count=52,phase_7B5_independent_illustrations_not_erp_tests=20,phase_7B5_bounded_literal_checks_not_application_tests=20,phase_7B5_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only original827/protected178 hashes, exact registry tails/core/all261 followups, IDs/distributions/links/bounds/scope inclusion, range/candidate bookkeeping, independent hand-selected illustrations, bounded lexical observations and synthetic documentary-checker self-tests ONLY.7A/B1/B2/B3/B4 use their OWN frozen registries/indexes, never current266. Metrics are not original-check byte replays. Five report C# bodies, a selected support dialog/models and bounded XAML/writer/caller slices do NOT certify every caller/child/template/deployment/payment/tax/accounting policy. Physical FreeVATSales column is not an invalid-alias claim; no particular DevExpress default SummaryText/renderer output is asserted.7B6 announced and7C not started;8 unauthorized. No ERP/C#/SQL/WPF/SDK/COM/Office/provider execution, financial/security/compliance certification, all-bugs claim, remediation or production data.'
