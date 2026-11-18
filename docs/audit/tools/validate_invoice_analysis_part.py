#!/usr/bin/env python3
"""Read-only bounded PARTIAL7B4 documentary checks; NOT ERP acceptance.

Protected B3 helpers/reports/checks are not edited. B3 reads its own frozen248
and exact three shared-index texts IN MEMORY at the original logical paths.
The additive current layer checks261, selected ranges, cross-links, bookkeeping,
independent illustrations and synthetic checker self-tests only. No C#/SQL/WPF,
Office/COM, binary, device or provider code is imported, built or executed.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_commercial_report_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,NONREGEX_SCREENS)

SCOPE_FILE='review-scope-07B4.csv'
PART_DOCS=('PHASE-07B4.md','INVOICE-ANALYSIS-REPORTS-07B4.md','VALIDATION-07B4.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B3.csv'
SNAPSHOT_SHA='993dbf53411cc2f495136bc699f3960ab2a10d6e9eb699d44d643195bac4f13f'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B3.json'
EXTENDED_FINDINGS={'P1-004','P1-011','P1-013','P1-033','P2-001','P2-010','P2-011','P3-023','P4-007','P7-041','P7-045','P7-046','P7-048','P7-049','P7-054','P7-055','P7-061'}
SENTINELS={'FE7B4-35','FE7B4-36','INV7B4-21','INV7B4-22','H7B4-05','H7B4-06','Q7B4-05','Q7B4-06','P7B4T-47','P7B4T-48'}
REVIEWED_BODIES=('frmRptInvAnalysis','frmRptItemsProfitDetails','frmRptInvNotfic','frmRptInvPurchaseDetails')


@contextmanager
def historical_b3_inputs(v,frozen248,shared_texts):
    if len(frozen248)!=248 or len({x['id'] for x in frozen248})!=248:
        raise ValueError('Exactly248 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen248,shared_texts):yield


def validate_frozen_b3(v,report,prov_b3,frozen237,prov_b4,frozen248):
    ck=v.check
    ck(prov_b4['registry_at_entry_snapshot']==SNAPSHOT and prov_b4['registry_at_entry_sha256']==SNAPSHOT_SHA,'B4 frozen248 identity changed')
    ck(prov_b4['shared_indexes_at_entry']==SHARED_SNAPSHOT,'B4 frozen B3 indexes identity changed')
    ck(prov_b4['phase7B3_entry_consistency']==dict(original_hashes_matching=827,findings=248,phase_7_delivery='7A+7B1+7B2+7B3-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B4 entry metadata no longer describes delivered B3')
    for path,digest in prov_b3['historical_artifact_sha256'].items():ck(prov_b4['historical_artifact_sha256'].get(path)==digest,'132-to155 historical continuity failed: '+path)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B3.json'))
    ck(saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==248 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov_b3['historical_artifact_sha256'],'Protected B3 checks no longer describe delivered248/827/132')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    from validate_commercial_report_part import extend_commercial_report
    with historical_b3_inputs(v,frozen248,texts):extend_commercial_report(v,report,prov_b3,frozen237)
    report['registry_used']=SNAPSHOT
    report['validation_scope']='historical-through7B3-248-not-current-state'
    report['phase_7B3_historical_input_mode']='frozen248-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B3_adapter_context']=dict(entry_provenance='evidence/provenance-07B4.json',adapter_protected_artifacts_checked=155,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True)
    report['validation']['limit']+=' HistoricalB3 uses frozen248 and exact B3 shared-index texts in memory. Its remaining-part labels are historical, not current. New-checker metrics need not reproduce protected checks bytes; no historical file is rewritten.'


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    result=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B4' for x in scope}
    for x in result:
        path=x['path'];x['phase7B4_ranges']=selected.get(path,'none')
        if x['inventory_kind']=='generated-artifact':continue
        if path in selected:
            bucket='7B4-bounded-slices-further-7B5-or-7C-not-closed'
            work='مقاطع7B4 فقط، منها أربعة أجسام محلية ومقاطع XAML/دعم. لا كل caller/قالب/نشر/قبول؛7B5/7C أو استبعاد مسند، لا اكتمال من اتحاد الأسطر.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(path).name,re.I) or Path(path).stem.removesuffix('.xaml') in NONREGEX_SCREENS:
            bucket='7B5-report-candidate-or-prior-slices-not-feature-closed'
            work='استكمل أجسام البيع/POS/Android/المقاطع المالية/الإخراج ومرشحي غيرregex والأطفال، أو استبعد بسبب موثق؛ قراءة launcher/helper لا تغطي الطفل.'
        else:
            bucket='7B5-or-7C-source-ui-resource-slices-not-complete'
            work='بقية المقاطع/القدرات أو استبعاد مسند؛7C لم تبدأ. لا latency/index/تسرب مثبت من هذا الدفتر أو مؤشرات مصدر فقط.'
        x['continuation_bucket']=bucket;x['next_scope_work']=work
    return result


def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B4' for x in scope}
    for x in result:
        x['phase7B4_ranges']=selected.get(x['path'],'none')
        if Path(x['path']).name=='FingerPrintDevice.cs':continue
        x['disposition']='7B5-further-slices-contract-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف لفظي لا98 ميزة؛ مقاطع7B4/التاريخ لا تغطي كل source/caller/template/schema/ACL/نشر/قبول. قد تعلن أجزاء7B أخرى.'
    return result


def build_screen_disposition(inventory,labelled_scopes):
    result=prior_screens(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B4' for x in scope}
    for n,x in enumerate(result,1):
        x['id']=f'SC7B4-{n:02d}';x['phase7B4_body_ranges']=selected.get(x['body_path'],'none')
        x['disposition']='7B5-or-7C-further-slices-contracts-or-reasoned-exclusion-required'
        if x['screen'] in REVIEWED_BODIES:
            x['coverage_level']='bounded-local-body-and-selected-xaml-not-whole-feature-certified'
            x['reason']='جسم محلي ومقاطع XAML محددة في7B4؛ لا كل طفل/قالب/نشر/سياسة أو قبول. حواجز الخيط/الإتاحة/البناء مستقلة.'
        else:x['reason']=x['reason'].replace('7B4/7C','7B5/7C')
    return result


def feature_level_errors(features):
    errors=[]
    allowed={'implemented-with-observed-defects','rechecked-prior-root-not-new-finding','counterevidence-not-global-closure','reviewed-contract-unresolved-not-global-absence','source-only-resource-performance-lead-not-runtime-measured','deferred-not-implementation-reviewed'}
    for x in features:
        if x['implementation_status'] not in allowed:errors.append('Unknown/closed B4 feature state: '+x['id'])
        deferred=x['implementation_status']=='deferred-not-implementation-reviewed'
        if deferred!=(x['coverage_level']=='inventory-only-not-implementation-reviewed') or deferred!=(x['evidence']=='none-inventory-only'):errors.append('Inventory-only B4 feature promoted/mislabelled: '+x['id'])
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':v.check(row['id'] in SENTINELS,'Undeclared B4 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B4 inventory-only boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B4',phase=7)


def extend_invoice_analysis(v,report,prov,frozen248):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==155 and len(frozen248)==248,'B4 protected entry count mismatch')
    current=r('findings.csv');new=current[248:];extensions=r('evidence/historical-extensions-07B4.csv')
    ext=v.transition(frozen248,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen248,current,extensions):ck(False,err)
    ck(len(current)==261 and len({x['id'] for x in current})==261,'B4 current count/uniqueness mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(77,90)],'B4 new finding IDs/order mismatch')
    v.distributions(new,{'High':7,'Medium':6},{'confirmed':13},'bounded7B4 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B4 classification/status/followup mismatch: '+x['id'])
    heads=re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B4.md'),re.M)
    ck(heads==[(x['id'],x['title']) for x in new],'B4 report title/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    ck(len(scopes)==18 and len({x['path'] for x in scopes})==18,'B4 scope count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B4 scope path/state mismatch: '+x['path']);v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        p='SmartAuditERP/Form_WPF/'+name+'.xaml.cs'
        ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B4 body span mismatch: '+name)
    specs=(('acceptance-tests','P7B4T-',48),('feature-implementation-matrix','FE7B4-',36),('report-invariants','INV7B4-',22),('report-reconciliation','RC7B4-',8),('historical-extensions','EX7B4-',17),('handoffs','H7B4-',6),('questions','Q7B4-',6),('continuation-backlog','BK7B4-',10))
    known={x['id'] for x in current}|{f'H7B4-{n:02d}' for n in range(1,7)};tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename+'-07B4.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for key,value in x.items():ck(bool(value),f'Incomplete B4 cell: {x["id"]}.{key}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B4 runtime claim: '+x['id'])
    tests,features,invariants,rc=[tables[k] for k in ('P7B4T-','FE7B4-','INV7B4-','RC7B4-')]
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B4');v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids');v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B4 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B4 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*26+['historical-root-regression']*17+['cross-cutting-contract']*3+['documentary-scope-or-authorization-gate']*2,'B4 plan kinds/order mismatch')
    ck([x['finding_ids'] for x in features[:13]]==[x['id'] for x in new],'B4 primary feature/finding mapping mismatch')
    ck([x['finding_ids'] for x in features[13:30]]==[x['finding_ids'] for x in extensions] and {x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B4 historical feature/extension mapping mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B4 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B4 RC plan links mismatch: '+x['id'])
        findings={f for fe in features if fe['id'] in x['feature_ids'].split(';') for f in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=findings,'B4 RC finding not in linked features: '+x['id'])
    v.related(tables['Q7B4-'],{x['id'] for x in tables['H7B4-']},'handoff_ids')
    for x in tables['H7B4-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B4 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B4-']:ck(x['status']=='unanswered-no-secrets-requested','B4 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B4-'],1):ck(x['prior_backlog_id']==f'BK7B3-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B5','7C','7B5/7C'} and x['status']!='complete','B4 backlog origin/part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B4-'][2:6]]==['not-started']*4,'B4 accidentally starts7C')
    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv'))]+[(part,r(f'review-scope-0{part}.csv')) for part in ('7B1','7B2','7B3')]+[('7B4',scopes)]
    ck(r('evidence/coverage-ledger-07B4.csv')==build_current_ledger(inventory,labelled,v.spans),'B4 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B4.csv');screens=r('evidence/report-screen-disposition-07B4.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B4 filename98 candidate mismatch')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B4 screen35+17 candidate mismatch');v.sequential(screens,'SC7B4-',52)
    prior={x['path'] for _,scope0 in labelled[:-1] for x in scope0};selected=set(scope);union=prior|selected
    # Exact source-scope bookkeeping, never a completion ratio.
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(326,18,10,8,334,493),'B4 prior/selected/overlap/new/union/complement mismatch')
    witness,match=v.recompute('evidence/report-witnesses-07B4.json','tools/check_invoice_analysis_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks'];v.sequential(algebra,'ALG7B4-',23);v.sequential(lexical,'ST7B4-',18);v.related(algebra+lexical,known)
    ck(witness['phase']=='7B4-partial-static-audit' and witness['illustration_count']==23 and witness['static_lexical_contract_check_count']==18 and witness['application_code_imported_or_executed'] is False and witness['erp_runtime_tests_executed']==0 and witness['sql_or_external_service_tests_executed']==0 and witness['application_remediation_performed'] is False and witness['real_business_or_secret_data_used'] is False and witness['spreadsheet_or_formula_interpreter_executed'] is False,'B4 witness metadata/claim mismatch')
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B4 witness fail/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B4 bounded lexical read',phase=7)
    for filename,pattern,expected in (
        ('PHASE-07B4.md',r'^\| (EX7B4-\d{2}) \|',[x['id'] for x in extensions]),
        ('INVOICE-ANALYSIS-REPORTS-07B4.md',r'^\| (FE7B4-\d{2}) —',[x['id'] for x in features]),
        ('INVOICE-ANALYSIS-REPORTS-07B4.md',r'^\| (INV7B4-\d{2}) \|',[x['id'] for x in invariants]),
        ('INVOICE-ANALYSIS-REPORTS-07B4.md',r'^### (RC7B4-\d{2}) —',[x['id'] for x in rc]),
        ('INVOICE-ANALYSIS-REPORTS-07B4.md',r'^\| (H7B4-\d{2}) —',[x['id'] for x in tables['H7B4-']]),
        ('INVOICE-ANALYSIS-REPORTS-07B4.md',r'^\| (Q7B4-\d{2}) \|',[x['id'] for x in tables['Q7B4-']]),
        ('INVOICE-ANALYSIS-REPORTS-07B4.md',r'^\| (BK7B4-\d{2}) \|',[x['id'] for x in tables['BK7B4-']]),
        ('VALIDATION-07B4.md',r'^\| (P7B4T-\d{2}) \|',[x['id'] for x in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,105)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B4 Markdown ID/order mismatch: '+filename)
    pending=False
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B4.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B4 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B4T-\d{2}\b',planids),(r'\bFE7B4-\d{2}\b',feids),(r'\bINV7B4-\d{2}\b',ivids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B4 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            fields=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[fields[0]]=fields[1:]
    for label,expected in (('التراكمي المفتوح',[261,2,170,88,1]),('7B4 — جديدة',[13,0,7,6,0]),('7B4 — إضافة محدودة',[18,len(selected&prior),len(selected-prior),len(union)])):ck(summary.get(label)==list(map(str,expected)),'Current B4 README numeric mismatch: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];oldgroups=re.findall(r'^\| G-\d{2} \|.*$',texts['IMPROVEMENTS.md'],re.M);livegroups=re.findall(r'^\| G-\d{2,3} \|.*$',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)
    ck(len(oldgroups)==96 and livegroups[:96]==oldgroups,'Historical G01–96 bodies changed')
    for filename in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/filename) for x in ('PHASE-07B4.md','7B5','7C','غير مأذونة')),'Current index lacks B4/B5/C/8 boundary: '+filename)
    tools=['check_invoice_analysis_witnesses.py','validate_invoice_analysis_part.py','test_invoice_analysis_audit_validator.py']
    for filename in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B4 audit-tool syntax: '+filename+':'+str(ex))
    completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_invoice_analysis_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout);count=int(m[1]) if m else None;passed=completed.returncode==0 and count==20;ck(passed,'B4 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_invoice_analysis_audit_validator.py']=dict(tests_reported=count,expected_tests=20,process_exit_code=completed.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py']+tools})
    report['validation_scope']='current-through7B4-261-plus-frozen-history-not-runtime-certification';report['phase_7_delivery']='7A+7B1+7B2+7B3+7B4-partial-not-complete7B-or7';report['phase_7_remaining_parts']=['7B5-announced-not-started','7C-not-started'];report['registry_used']='findings.csv'
    report['findings'].update(phase_7=89,phase_7B4=13,total_open_not_remediated=261,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:18,'phase_7B3_union_frozen':326,'phase_7B4_overlap_with_prior_union':len(selected&prior),'phase_7B4_new_paths':len(selected-prior),'unique_union_not_line_or_execution_coverage':len(union),'inventory_only_no_selected_scope':len(paths-union)})
    report['phase_7B3_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=155,historical_check_record_overwritten=False,partial7B4_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all248=True,next_phase_replans_during_partial7={})
    report['historical_artifact_sha256']=prov['historical_artifact_sha256'];report['date_semantics']=prov['date_semantics']
    report['evidence_rows'].update(dict(phase_7B4_feature_rows_not_completed_features=36,phase_7B4_invariants_not_passed_tests=22,phase_7B4_source_reconciliation_contracts_not_executed_financial_acceptance=8,phase_7B4_unexecuted_acceptance_or_gate_plans=48,phase_7B4_direct_finding_plans=26,phase_7B4_historical_regression_plans=17,phase_7B4_cross_contract_plans=3,phase_7B4_documentary_scope_authorization_gate_plans=2,phase_7B4_historical_extensions_not_new_findings=17,phase_7B4_unresolved_handoffs=6,phase_7B4_unanswered_questions=6,phase_7B4_continuation_groups_not_complete=10,phase_7B4_original_paths_in_ledger=827,phase_7B4_filename_candidates_not_feature_count=98,phase_7B4_screen_candidates_35_regex_plus17_curated_not_feature_count=52,phase_7B4_independent_illustrations_not_erp_tests=23,phase_7B4_bounded_literal_checks_not_application_tests=18,phase_7B4_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only original827/protected155 hashes, exact registry tails/core/all248 followups, IDs/distributions/links/bounds/scope inclusion, range/candidate bookkeeping, cross-links, independent manual illustrations, bounded lexical observations and synthetic documentary-checker self-tests ONLY.7A/B1/B2/B3 use their OWN frozen registries/indexes, never current261. Metrics are not original-check byte replays. Four local C# bodies plus selected XAML/support do NOT certify all callers/children/templates/deployment/financial policies. Analysis thread/disabled-entry/build/schema gates precede downstream acceptance.7B5 announced and7C not started;8 unauthorized. No ERP/C#/SQL/WPF/SDK/COM/Office/provider execution, financial/security/compliance certification, all-bugs claim, remediation or production data.'
