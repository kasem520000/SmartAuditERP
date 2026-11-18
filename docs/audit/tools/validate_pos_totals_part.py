#!/usr/bin/env python3
"""Read-only PARTIAL7B6 documentary checks, never ERP acceptance.

Protected B5 receives exactly frozen266 and its own exact shared-index texts
at original logical paths IN MEMORY. No archived helper/report/check is changed.
The audited application reference is separate from docs-only checkout commits:
ancestry/net docs path delta AND independent original827 path/hash checks remain.
No application import/build, SQL, WPF/Office/COM/provider/binary execution/writes.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_sales_report_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors as prior_feature_errors,
    NONREGEX_SCREENS)

SCOPE_FILE='review-scope-07B6.csv'
PART_DOCS=('PHASE-07B6.md','POS-ACTS-TOTALS-07B6.md','VALIDATION-07B6.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B5.csv'
SNAPSHOT_SHA='05204ad5a40eed6a6a276b949c3c679e6f506f139a6470394f1489706a882619'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B5.json'
EXTENDED_FINDINGS={'P1-004','P1-013','P1-030','P1-033','P2-010','P3-023','P7-040','P7-041','P7-045','P7-046','P7-048','P7-049','P7-050','P7-061','P7-080','P7-084'}
SENTINELS={'FE7B6-25','FE7B6-26','INV7B6-18','INV7B6-19','H7B6-06','Q7B6-06','P7B6T-30','P7B6T-31'}
REVIEWED_BODIES=('frmItemsalesdetailsPos','frmActsInvTotal','frmNkdTotSalePurch')


@contextmanager
def historical_b5_inputs(v,frozen266,shared_texts):
    if len(frozen266)!=266 or len({x['id'] for x in frozen266})!=266:
        raise ValueError('Exactly266 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen266,shared_texts):yield


def validate_frozen_b5(v,report,prov_b5,frozen261,prov_b6,frozen266):
    ck=v.check
    ck(prov_b6['registry_at_entry_snapshot']==SNAPSHOT and prov_b6['registry_at_entry_sha256']==SNAPSHOT_SHA,'B6 frozen266 identity changed')
    ck(prov_b6['shared_indexes_at_entry']==SHARED_SNAPSHOT,'B6 frozen B5 indexes identity changed')
    ck(v.sha(v.AUDIT/SHARED_SNAPSHOT)==prov_b6['shared_indexes_at_entry_sha256'],'B6 frozen exact index bytes changed')
    ck(prov_b6['phase7B5_entry_consistency']==dict(original_hashes_matching=827,findings=266,phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B6 entry no longer describes deliveredB5')
    for p,digest in prov_b5['historical_artifact_sha256'].items():
        ck(prov_b6['historical_artifact_sha256'].get(p)==digest,'178-to199 historical continuity failed: '+p)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B5.json'))
    ck(saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==266 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov_b5['historical_artifact_sha256'],'Protected B5 checks no longer describe delivered266/827/178')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    from validate_sales_report_part import extend_sales_report
    with historical_b5_inputs(v,frozen266,texts):extend_sales_report(v,report,prov_b5,frozen261)
    report['registry_used']=SNAPSHOT
    report['validation_scope']='historical-through7B5-266-not-current-state'
    report['phase_7B5_historical_input_mode']='frozen266-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B5_adapter_context']=dict(entry_provenance='evidence/provenance-07B6.json',adapter_protected_artifacts_checked=199,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True)
    report['validation']['limit']+=' HistoricalB5 uses frozen266 and exact B5 shared-index texts IN MEMORY. Source10ba is not replaced by docs-only checkoutd0ae. Current-checker metrics are not archived check-byte replays; no historical file is rewritten.'


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    result=prior_ledger(inventory,labelled_scopes,parse_ranges)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B6' for x in scope}
    for x in result:
        p=x['path'];x['phase7B6_ranges']=selected.get(p,'none')
        if x['inventory_kind']=='generated-artifact':continue
        if p in selected:
            bucket='7B6-bounded-slices-further-7B7-or-7C-not-closed'
            work='ثلاثة أجسام وXAMLها ومقاطع دعم محددة في7B6؛ لا كل caller/template/سياسة/نشر/قبول. استكمل7B7/7C أو استبعد بسبب؛ all-lines لا يكمل ميزة.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I) or Path(p).stem.removesuffix('.xaml') in NONREGEX_SCREENS:
            bucket='7B7-report-candidate-or-prior-slices-not-feature-closed'
            work='7B7 معلنة لبقية المالية/الإخراج وغيرregex والأطفال؛ لا ترقية من أسماء/launcher/اتحاد نطاقات إلى اكتمال feature.'
        else:
            bucket='7B7-or-7C-source-ui-resource-slices-not-complete'
            work='بقية المقاطع/القدرات أو استبعاد مسند؛7C لم تبدأ. موارد/أداء مصدرية leads لا leak/latency/index مثبتة أو إذن تشغيل.'
        x['continuation_bucket']=bucket;x['next_scope_work']=work
    return result


def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B6' for x in scope}
    for x in result:
        x['phase7B6_ranges']=selected.get(x['path'],'none')
        if Path(x['path']).name=='FingerPrintDevice.cs':continue
        x['disposition']='7B7-further-slices-contract-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف لفظي لا98 ميزة؛ مقاطع B6 والتاريخ لا تغطي كل caller/template/schema/ACL/نشر/قبول.7B7 معلنة بدلاً من إغلاق7B.'
    return result


def build_screen_disposition(inventory,labelled_scopes):
    result=prior_screens(inventory,labelled_scopes)
    selected={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B6' for x in scope}
    for n,x in enumerate(result,1):
        x['id']=f'SC7B6-{n:02d}';x['phase7B6_body_ranges']=selected.get(x['body_path'],'none')
        x['disposition']='7B7-or-7C-further-slices-contracts-or-reasoned-exclusion-required'
        if x['screen'] in REVIEWED_BODIES and x['body_path'] in selected:
            x['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified'
            x['reason']='الجسم وXAML المحليان قرئا في7B6 بنطاق محدد؛ لا كل caller/قالب/سياسة/نشر أو قبول، ولا يشمل ذلك أي طفل آخر.'
        else:
            x['reason']='حصر اسمي/مقاطع سابقة فقط وفق الحقول؛ استكمل7B7/7C أو استبعد بسبب. قراءة launcher لا تغطي الطفل، وall-lines لا يثبت كامل الميزة.'
    return result


def feature_level_errors(features):return [x.replace('B5','B6') for x in prior_feature_errors(features)]


def witness_metadata_errors(w):
    errors=[]
    for key in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(key) is not False:errors.append('B6 witness false-only flag: '+key)
    for key in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(key)) is not int or w[key]!=0:errors.append('B6 witness zero-only count: '+key)
    if w.get('phase')!='7B6-partial-static-audit':errors.append('B6 witness phase mismatch')
    if w.get('illustration_count')!=20 or w.get('static_lexical_contract_check_count')!=20:errors.append('B6 witness count mismatch')
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':v.check(row['id'] in SENTINELS,'Undeclared B6 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B6 inventory-only boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id']);v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B6',phase=7)


def extend_pos_totals(v,report,prov,frozen266):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==199 and len(frozen266)==266,'B6 protected entry count mismatch')
    identity=report['source_reference_validation']
    ck(identity['audited_application_reference']==v.HEAD and identity['reference_ancestor_of_checkout'] is True and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B6 source vs checkout integrity mismatch')
    ck(prov['checkout_head_at_entry']==prov['pushed_documentation_commit_before_continuation']=='d0ae6b318c47451dd7e10a416f07566a7b3f1dc7' and prov['documentation_only_changes_since_source_reference']==dict(paths=204,all_under='docs/audit/',original827_hashes_verified=True,application_paths_changed=[]),'B6 documentation entry metadata changed')
    current=r('findings.csv');new=current[266:];extensions=r('evidence/historical-extensions-07B6.csv')
    ext=v.transition(frozen266,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen266,current,extensions):ck(False,err)
    ck(len(current)==270 and len({x['id'] for x in current})==270,'B6 current count/uniqueness mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(95,99)],'B6 new finding IDs/order mismatch')
    v.distributions(new,{'High':1,'Medium':3},{'confirmed':4},'bounded7B6 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B6 classification/status/followup mismatch: '+x['id'])
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B6.md'),re.M)==[(x['id'],x['title']) for x in new],'B6 report title/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    ck(len(scopes)==13 and len({x['path'] for x in scopes})==13,'B6 scope count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B6 scope path/state mismatch: '+x['path']);v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        for ext0 in ('.xaml.cs','.xaml'):
            p='SmartAuditERP/Form_WPF/'+name+ext0
            ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B6 body/XAML span mismatch: '+p)
    specs=(('acceptance-tests','P7B6T-',31),('feature-implementation-matrix','FE7B6-',26),('report-invariants','INV7B6-',19),('report-reconciliation','RC7B6-',7),('historical-extensions','EX7B6-',16),('handoffs','H7B6-',6),('questions','Q7B6-',6),('continuation-backlog','BK7B6-',10))
    known={x['id'] for x in current}|{f'H7B6-{n:02d}' for n in range(1,7)};tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename+'-07B6.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for key,value in x.items():ck(bool(value),f'Incomplete B6 cell: {x["id"]}.{key}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B6 runtime claim: '+x['id'])
    tests,features,invariants,rc=[tables[k] for k in ('P7B6T-','FE7B6-','INV7B6-','RC7B6-')]
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B6');v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids');v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B6 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B6 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*8+['historical-root-regression']*16+['cross-cutting-contract']*5+['documentary-scope-or-authorization-gate']*2,'B6 plan kind/order mismatch')
    ck([x['finding_ids'] for x in features[:4]]==[x['id'] for x in new],'B6 primary feature/finding mapping mismatch')
    ck([x['finding_ids'] for x in features[4:20]]==[x['finding_ids'] for x in extensions] and {x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B6 feature/extension mapping mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B6 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B6 RC plan links mismatch: '+x['id'])
        fids={f for fe in features if fe['id'] in x['feature_ids'].split(';') for f in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=fids,'B6 RC finding not in linked features: '+x['id'])
    v.related(tables['Q7B6-'],{x['id'] for x in tables['H7B6-']},'handoff_ids')
    for x in tables['H7B6-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B6 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B6-']:ck(x['status']=='unanswered-no-secrets-requested','B6 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B6-'],1):ck(x['prior_backlog_id']==f'BK7B5-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B7','7C','7B7/7C'} and x['status']!='complete','B6 backlog origin/part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B6-'][2:6]]==['not-started']*4,'B6 accidentally starts7C')
    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv'))]+[(f'7B{n}',r(f'review-scope-07B{n}.csv')) for n in range(1,6)]+[('7B6',scopes)]
    ck(r('evidence/coverage-ledger-07B6.csv')==build_current_ledger(inventory,labelled,v.spans),'B6 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B6.csv');screens=r('evidence/report-screen-disposition-07B6.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B6 filename98 candidate mismatch')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B6 screen35+17 candidate mismatch');v.sequential(screens,'SC7B6-',52)
    prior={x['path'] for _,scope0 in labelled[:-1] for x in scope0};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(347,13,7,6,353,474),'B6 prior/selected/overlap/new/union/complement mismatch')
    witness,match=v.recompute('evidence/report-witnesses-07B6.json','tools/check_pos_totals_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks'];v.sequential(algebra,'ALG7B6-',20);v.sequential(lexical,'ST7B6-',20);v.related(algebra+lexical,known)
    for err in witness_metadata_errors(witness):ck(False,err)
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B6 witness fail/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B6 bounded lexical read',phase=7)
    for filename,pattern,expected in (
        ('PHASE-07B6.md',r'^\| (EX7B6-\d{2}) \|',[x['id'] for x in extensions]),
        ('POS-ACTS-TOTALS-07B6.md',r'^\| (FE7B6-\d{2}) —',[x['id'] for x in features]),
        ('POS-ACTS-TOTALS-07B6.md',r'^\| (INV7B6-\d{2}) \|',[x['id'] for x in invariants]),
        ('POS-ACTS-TOTALS-07B6.md',r'^### (RC7B6-\d{2}) —',[x['id'] for x in rc]),
        ('POS-ACTS-TOTALS-07B6.md',r'^\| (H7B6-\d{2}) —',[x['id'] for x in tables['H7B6-']]),
        ('POS-ACTS-TOTALS-07B6.md',r'^\| (Q7B6-\d{2}) \|',[x['id'] for x in tables['Q7B6-']]),
        ('POS-ACTS-TOTALS-07B6.md',r'^\| (BK7B6-\d{2}) \|',[x['id'] for x in tables['BK7B6-']]),
        ('VALIDATION-07B6.md',r'^\| (P7B6T-\d{2}) \|',[x['id'] for x in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,117)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B6 Markdown ID/order mismatch: '+filename)
    pending=False
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B6.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B6 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B6T-\d{2}\b',planids),(r'\bFE7B6-\d{2}\b',feids),(r'\bINV7B6-\d{2}\b',ivids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B6 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            f=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[f[0]]=f[1:]
    for label,expected in (('التراكمي المفتوح',[270,2,174,93,1]),('7B6 — جديدة',[4,0,1,3,0]),('7B6 — إضافة محدودة',[13,7,6,353])):ck(summary.get(label)==list(map(str,expected)),'Current B6 README numeric mismatch: '+label)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];oldgroups=re.findall(r'^\| G-\d{2,3} \|.*$',texts['IMPROVEMENTS.md'],re.M);livegroups=re.findall(r'^\| G-\d{2,3} \|.*$',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)
    ck(len(oldgroups)==110 and livegroups[:110]==oldgroups,'Historical G01–110 exact rows changed')
    for filename in SHARED_DOCS:ck(all(x in v.read(v.AUDIT/filename) for x in ('PHASE-07B6.md','7B7','7C','غير مأذونة','d0ae6b3')),'Current index lacks B6/B7/C/8 or pushed-checkout boundary: '+filename)
    tools=['check_pos_totals_witnesses.py','validate_pos_totals_part.py','test_pos_totals_audit_validator.py']
    for filename in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B6 audit-tool syntax: '+filename+':'+str(ex))
    completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_pos_totals_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout);count=int(m[1]) if m else None;passed=completed.returncode==0 and count==28;ck(passed,'B6 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_pos_totals_audit_validator.py']=dict(tests_reported=count,expected_tests=28,process_exit_code=completed.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py','audit_source_identity.py']+tools})
    report['validation_scope']='current-through7B6-270-plus-frozen-history-not-runtime-certification';report['phase_7_delivery']='7A+7B1+7B2+7B3+7B4+7B5+7B6-partial-not-complete7B-or7';report['phase_7_remaining_parts']=['7B7-announced-not-started','7C-not-started'];report['registry_used']='findings.csv'
    report['findings'].update(phase_7=98,phase_7B6=4,total_open_not_remediated=270,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:13,'phase_7B5_union_frozen':347,'phase_7B6_overlap_with_prior_union':7,'phase_7B6_new_paths':6,'unique_union_not_line_or_execution_coverage':353,'inventory_only_no_selected_scope':474})
    report['phase_7B5_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=199,historical_check_record_overwritten=False,partial7B6_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all266=True,next_phase_replans_during_partial7={})
    report['historical_artifact_sha256']=prov['historical_artifact_sha256'];report['date_semantics']=prov['date_semantics']
    report['evidence_rows'].update(dict(phase_7B6_feature_rows_not_completed_features=26,phase_7B6_invariants_not_passed_tests=19,phase_7B6_source_reconciliation_contracts_not_executed_financial_acceptance=7,phase_7B6_unexecuted_acceptance_or_gate_plans=31,phase_7B6_direct_finding_plans=8,phase_7B6_historical_regression_plans=16,phase_7B6_cross_contract_plans=5,phase_7B6_documentary_scope_authorization_gate_plans=2,phase_7B6_historical_extensions_not_new_findings=16,phase_7B6_unresolved_handoffs=6,phase_7B6_unanswered_questions=6,phase_7B6_continuation_groups_not_complete=10,phase_7B6_original_paths_in_ledger=827,phase_7B6_filename_candidates_not_feature_count=98,phase_7B6_screen_candidates_35_regex_plus17_curated_not_feature_count=52,phase_7B6_independent_illustrations_not_erp_tests=20,phase_7B6_bounded_literal_checks_not_application_tests=20,phase_7B6_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only original827 paths/hashes, source10ba ancestry/docs-only checkout tree delta, protected199 hashes, exact266 registry cores/tails/ALL followups and G01–110 rows, IDs/distributions/links/bounds/scope inclusion, candidate/range bookkeeping, independent hand-selected illustrations, bounded lexical observations and isolated synthetic documentary-checker tests ONLY.7A/B1/B2/B3/B4/B5 use OWN frozen registries/indexes, never current270. New metrics are not archived-check byte replays; baselines/history unchanged. Three bodies and local XAML with bounded support do not certify every caller/child/template/deployment/ACL/financial policy. Acts uses Dispatcher and POS copies signed summaries directly: no blanket P7-054/P7-093 extension. HTML raw interpolation is confirmed, not script/formula execution; XLS HTML is not proven universally rejected.7B7 announced,7C not started,8 unauthorized. No ERP/C#/SQL/WPF/SDK/COM/Office/provider execution, remediation, financial/security/compliance certificate, all-bugs claim or production data.'
