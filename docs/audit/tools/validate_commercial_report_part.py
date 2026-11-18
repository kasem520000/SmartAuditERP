#!/usr/bin/env python3
"""Additive documentary validator for bounded PARTIAL7B3, NOT ERP acceptance.

The protected7B2 helper runs against frozen237 and the exact deliveredB2 index
texts in memory at their original logical paths. No protected file is edited.
This module checks current248, explicit spans, registry tails, cross-links and
inventory bookkeeping. It does not import/build/run C#, SQL, WPF or providers.
"""
from __future__ import annotations
import collections
from contextlib import contextmanager
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import (
    historical_b1_inputs,registry_transition_errors,
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    bidirectional_errors)

SCOPE_FILE='review-scope-07B3.csv'
PART_DOCS=('PHASE-07B3.md','COMMERCIAL-MARINE-REPORTS-07B3.md','VALIDATION-07B3.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B2.csv'
SNAPSHOT_SHA='a666334204d3a79b6b0b1bb324669d5dc0b387c62dba03f80d2c0447248461cb'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B2.json'
EXTENDED_FINDINGS={'P1-004','P1-033','P1-013','P2-001','P2-010','P3-023','P4-029','P7-041','P7-045','P7-046','P7-048','P7-049','P7-054'}
SENTINELS={'FE7B3-28','FE7B3-29','H7B3-05','H7B3-06','Q7B3-05','Q7B3-06','P7B3T-38','P7B3T-39'}
REVIEWED_BODIES=('FrmRptSalesChart','frmRptDailySales','frmRptCategorySaleByDay','frmRptSalesByCategory','frmRptDailyProcess','frmRptProducedItems','frmRptRentInvoices','frmRptSerialNo','frmRptSerialNoSummary','frmNkdFoundRpt')
NONREGEX_SCREENS=('FrmReseved','IncomeStatementForm','frmAccountBalance','frmAccountsStatement','frmActsInvTotal','frmCostCenterBalance','frmDecisionHelp','frmInvBySalesMen','frmInvsProfit','frmItemsBalances','frmItemsalesdetailsPos','frmMezanMorg3a','frmMezanyaArba7','frmNkdTotSalePurch','frmNkdTotSalePurchActCust','frmSummaryD','frmSummaryQ')


@contextmanager
def historical_b2_inputs(v,frozen237,shared_texts):
    """Same pure path-specific adapter, with a separately protected B2 cutoff."""
    if len(frozen237)!=237 or len({x['id'] for x in frozen237})!=237:
        raise ValueError('Exactly237 distinct historical registry rows required')
    with historical_b1_inputs(v,frozen237,shared_texts):yield


def validate_frozen_b2(v,report,prov7b2,frozen223,prior_prov,prov7b3,frozen237):
    ck=v.check
    ck(prov7b3['registry_at_entry_snapshot']==SNAPSHOT and prov7b3['registry_at_entry_sha256']==SNAPSHOT_SHA,'B3 entry frozen registry identity changed')
    ck(prov7b3['shared_indexes_at_entry']==SHARED_SNAPSHOT,'B2 frozen shared-index identity changed')
    ck(prov7b3['phase7B2_entry_consistency']==dict(original_hashes_matching=827,findings=237,phase_7_delivery='7A+7B1+7B2-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B3 entry metadata no longer describes deliveredB2')
    for p,digest in prov7b2['historical_artifact_sha256'].items():
        ck(prov7b3['historical_artifact_sha256'].get(p)==digest,'110-to132 historical continuity failed: '+p)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B2.json'))
    ck(saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==237 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prov7b2['historical_artifact_sha256'],'Saved B2 checks no longer describe delivered237/827/110')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    from validate_financial_report_part import extend_financial_report
    with historical_b2_inputs(v,frozen237,texts):
        extend_financial_report(v,report,prov7b2,frozen223,prior_prov)
    report['registry_used']=SNAPSHOT
    report['validation_scope']='historical-through7B2-237-not-current-state'
    report['phase_7B2_historical_input_mode']='frozen237-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B2_adapter_context']=dict(entry_provenance='evidence/provenance-07B3.json',adapter_protected_artifacts_checked=132,current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True)
    report['validation']['limit']+=' HistoricalB2 uses its protected237 registry and exact original index texts in memory. Its remaining-part labels describe that historical cutoff, not current completion. Current-checker metrics need not replay original check bytes; no historical check/report is rewritten.'


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    """Range bookkeeping only; a full text span is never feature certification."""
    ledger=prior_ledger(inventory,labelled_scopes,parse_ranges)
    b3={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B3' for x in scope}
    for x in ledger:
        p=x['path'];x['phase7B3_ranges']=b3.get(p,'none')
        if x['inventory_kind']=='generated-artifact':continue
        if p in b3:
            bucket='7B3-bounded-slices-further-7B4-or-7C-not-closed'
            work='مقاطع7B3 فقط؛ حتى الجسم المحلي الكامل لا يغطي الأبناء/المتصلين/القوالب/النشر/القبول. استكمل7B4/7C أو استبعاداً مسنداً.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I) or Path(p).stem.removesuffix('.xaml') in NONREGEX_SCREENS:
            bucket='7B4-report-source-candidate-not-feature-closed'
            work='فرز اسم/شاشة أو مقاطع تاريخية فقط؛ يلزم اختيار implementation/source/identity/criteria/totals/output/ACL أو استبعاد مسند، لا إغلاق من اسم.'
        else:
            bucket='7B4-or-7C-remaining-source-ui-resource-not-started'
            work='بقية المقاطع/القدرات أو سبب استبعاد؛7C لم تبدأ. لا مخطط تنفيذ أو فهرس أو زمن أداء أو دورة موارد من هذا الدفتر.'
        x['continuation_bucket']=bucket;x['next_scope_work']=work
    return ledger


def build_candidate_disposition(inventory,labelled_scopes):
    result=prior_candidates(inventory,labelled_scopes)
    b3={x['path']:x['ranges'] for label,scope in labelled_scopes if label=='7B3' for x in scope}
    for x in result:
        x['phase7B3_ranges']=b3.get(x['path'],'none')
        if Path(x['path']).name=='FingerPrintDevice.cs':continue
        x['disposition']='7B4-further-slices-contract-or-reasoned-exclusion-required'
        x['reason']='98 مرشح ملف اسمي لا98 تقريراً/ميزة؛ نطاق7B3 أو السابق لا يغطي كل caller/قالب/نشر/قبول. أضيفت قائمة شاشات أوسع لا قائمة اكتمال.'
    return result


def build_screen_disposition(inventory,labelled_scopes):
    """35 filename candidates plus17 explicitly named nonregex candidates.

    This is NOT an exhaustive inventory of all ERP capabilities. Existence and
    range association do not promote historical depth or transitively review
    children of launchers. All needed identity comes from original inventory.
    """
    lookup={x['path']:x for x in inventory}
    paths=[p for p in lookup if p.startswith('SmartAuditERP/Form_WPF/') and p.endswith('.xaml') and (re.search('rpt|report',Path(p).stem,re.I) or Path(p).stem in NONREGEX_SCREENS)]
    result=[]
    for p in sorted(paths):
        name=Path(p).stem;body=p+'.cs';phases=[label for label,scope in labelled_scopes if any(r['path'] in {p,body} for r in scope)]
        b3=next((r['ranges'] for label,scope in labelled_scopes if label=='7B3' for r in scope if r['path']==body),'none')
        if name in REVIEWED_BODIES:
            state='bounded-local-body-and-selected-xaml-not-whole-feature-certified'
            reason='جسم محلي ومقاطع XAML محددة في7B3؛ لا كل طفل/قالب/مصدر خارجي/نشر/اختبار. مؤسسة النقد launcher فقط.'
        elif phases:
            state='prior-selected-slices-depth-not-upgraded'
            reason='نطاقات تاريخية لا ترقى إلى جسم/ميزة كاملة؛ حدد الباقي في7B4/7C أو استبعاداً مسنداً.'
        else:
            state='inventory-only-not-implementation-reviewed'
            reason='اسم/مرشح شاشة أصلي فقط؛ لم تراجع implementation في هذا الجزء. لا ميزة منفية ولا اكتمال مفترض.'
        result.append(dict(id=f'SC7B3-{len(result)+1:02d}',screen=name,path=p,body_path=body,
            selection_basis='filename-rpt-report-not-a-feature-inventory' if re.search('rpt|report',name,re.I) else 'explicit-nonregex-source-candidate-not-a-feature-claim',
            body_inventory_lines=lookup.get(body,{}).get('lines','not-in-original-inventory'),selected_phase_ids=';'.join(phases) or 'none',phase7B3_body_ranges=b3,
            coverage_level=state,disposition='7B4-or-7C-further-slices-contracts-or-reasoned-exclusion-required',reason=reason,runtime_status='not-executed'))
    return result


def feature_level_errors(features):
    errors=[]
    allowed={'implemented-with-observed-defects','rechecked-prior-root-not-new-finding','counterevidence-not-global-closure','launcher-only-children-deferred','deferred-not-implementation-reviewed'}
    for x in features:
        if x['implementation_status'] not in allowed:errors.append('Unknown/closed feature state: '+x['id'])
        deferred=x['implementation_status']=='deferred-not-implementation-reviewed'
        if deferred!=(x['coverage_level']=='inventory-only-not-implementation-reviewed') or deferred!=(x['evidence']=='none-inventory-only'):
            errors.append('Inventory-only feature promoted/mislabelled: '+x['id'])
    return errors


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    if row['evidence']=='none-inventory-only':
        v.check(row['id'] in SENTINELS,'Undeclared B3 no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'B3 inventory-only boundary lost: '+row['id'])
        v.evidence(row['evidence'],row['id'])
        v.scoped_evidence(row['evidence'],scope,row['id']+' bounded7B3',phase=7)


def extend_commercial_report(v,report,prov,frozen237):
    ck,r=v.check,v.rows
    ck(prov['historical_artifact_count']==132 and len(frozen237)==237,'B3 protected entry count mismatch')
    current=r('findings.csv');new=current[237:];extensions=r('evidence/historical-extensions-07B3.csv')
    ext=v.transition(frozen237,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for err in registry_transition_errors(frozen237,current,extensions):ck(False,err)
    ck(len(current)==248 and len({x['id'] for x in current})==248,'B3 current count/unique IDs mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(66,77)],'B3 new registry IDs/order mismatch')
    v.distributions(new,{'High':6,'Medium':5},{'confirmed':11},'bounded7B3 only')
    for x in new:ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B3 classification/status/schedule mismatch: '+x['id'])
    heads=re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B3.md'),re.M)
    ck(heads==[(x['id'],x['title']) for x in new],'B3 report title/registry mismatch')
    scopes=r(SCOPE_FILE);inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    ck(len(scopes)==27 and len({x['path'] for x in scopes})==27,'B3 scope path count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B3 scope state/path mismatch: '+x['path'])
        v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)
    for name in REVIEWED_BODIES:
        p='SmartAuditERP/Form_WPF/'+name+'.xaml.cs'
        ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B3 declared local body span mismatch: '+name)

    specs=(('acceptance-tests-07B3.csv','P7B3T-',39),('feature-implementation-matrix-07B3.csv','FE7B3-',29),
        ('report-invariants-07B3.csv','INV7B3-',17),('report-reconciliation-07B3.csv','RC7B3-',10),
        ('historical-extensions-07B3.csv','EX7B3-',13),('handoffs-07B3.csv','H7B3-',6),
        ('questions-07B3.csv','Q7B3-',6),('continuation-backlog-07B3.csv','BK7B3-',10))
    known={x['id'] for x in current}|{f'H7B3-{n:02d}' for n in range(1,7)}
    tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename);tables[prefix]=data
        v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for k,value in x.items():ck(bool(value),f'Incomplete B3 cell: {x["id"]}.{k}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B3 runtime claim: '+x['id'])
    tests,features,invariants,rc=tables['P7B3T-'],tables['FE7B3-'],tables['INV7B3-'],tables['RC7B3-']
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B3');v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids')
    v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field):ck(False,err)
    for err in feature_level_errors(features):ck(False,err)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'B3 '+label)
    for x in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']])==2,'B3 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*22+['historical-root-regression']*13+['cross-cutting-contract']*2+['documentary-scope-or-authorization-gate']*2,'B3 plan kinds changed')
    ck([x['finding_ids'] for x in features[:11]]==[x['id'] for x in new],'B3 primary features/new finding mapping changed')
    ck([x['finding_ids'] for x in features[11:24]]==[x['finding_ids'] for x in extensions],'B3 historical features/extensions mismatch')
    ck({x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B3 extension set changed')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B3 historical replan claim: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'B3 RC plan backreference mismatch: '+x['id'])
        findings={f for fe in features if fe['id'] in x['feature_ids'].split(';') for f in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=findings,'B3 RC finding not in its features: '+x['id'])
    v.related(tables['Q7B3-'],{x['id'] for x in tables['H7B3-']},'handoff_ids')
    for x in tables['H7B3-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B3 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B3-']:ck(x['status']=='unanswered-no-secrets-requested','B3 question falsely resolved: '+x['id'])
    for n,x in enumerate(tables['BK7B3-'],1):
        ck(x['prior_backlog_id']==f'BK7B2-{n:02d}' and x['original_backlog_id']==f'BK7-{n:02d}' and x['part'] in {'7B4','7C','7B4/7C'} and x['status']!='complete','B3 backlog origin/remaining-part/closure mismatch: '+x['id'])
    ck([x['status'] for x in tables['BK7B3-'][2:6]]==['not-started']*4,'B3 accidentally starts7C')

    labelled=[(str(n),r('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv')),('7B1',r('review-scope-07B1.csv')),('7B2',r('review-scope-07B2.csv')),('7B3',scopes)]
    ck(r('evidence/coverage-ledger-07B3.csv')==build_current_ledger(inventory,labelled,v.spans),'B3 ledger recomputation mismatch')
    candidates=r('evidence/report-candidate-disposition-07B3.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B3 filename-only98 disposition mismatch')
    screens=r('evidence/report-screen-disposition-07B3.csv')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B3 35+17 screen-candidate disposition mismatch')
    v.sequential(screens,'SC7B3-',52)
    prior={x['path'] for label,scope0 in labelled[:-1] for x in scope0};selected=set(scope);union=prior|selected
    ck((len(prior),len(selected&prior),len(selected-prior),len(union),len(paths-union))==(306,7,20,326,501),'B3 overlap/new/union/inventory-only mismatch')

    witness,match=v.recompute('evidence/report-witnesses-07B3.json','tools/check_commercial_report_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks']
    v.sequential(algebra,'ALG7B3-',20);v.sequential(lexical,'ST7B3-',16);v.related(algebra+lexical,known)
    ck(witness['phase']=='7B3-partial-static-audit' and witness['illustration_count']==20 and witness['static_lexical_contract_check_count']==16 and witness['application_remediation_performed'] is False and witness['real_business_or_secret_data_used'] is False and witness['spreadsheet_or_formula_interpreter_executed'] is False,'B3 witness execution claim')
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B3 witness failure/overclaim: '+x['id']);validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B3 bounded lexical read',phase=7)

    for filename,pattern,expected in (
        ('PHASE-07B3.md',r'^\| (EX7B3-\d{2}) \|',[x['id'] for x in extensions]),
        ('COMMERCIAL-MARINE-REPORTS-07B3.md',r'^\| (FE7B3-\d{2}) —',[x['id'] for x in features]),
        ('COMMERCIAL-MARINE-REPORTS-07B3.md',r'^\| (INV7B3-\d{2}) \|',[x['id'] for x in invariants]),
        ('COMMERCIAL-MARINE-REPORTS-07B3.md',r'^### (RC7B3-\d{2}) —',[x['id'] for x in rc]),
        ('COMMERCIAL-MARINE-REPORTS-07B3.md',r'^\| (H7B3-\d{2}) —',[x['id'] for x in tables['H7B3-']]),
        ('COMMERCIAL-MARINE-REPORTS-07B3.md',r'^\| (Q7B3-\d{2}) \|',[x['id'] for x in tables['Q7B3-']]),
        ('COMMERCIAL-MARINE-REPORTS-07B3.md',r'^\| (BK7B3-\d{2}) \|',[x['id'] for x in tables['BK7B3-']]),
        ('VALIDATION-07B3.md',r'^\| (P7B3T-\d{2}) \|',[x['id'] for x in tests]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2}) \|',[f'G-{n:02d}' for n in range(1,97)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B3 Markdown ID/order mismatch in '+filename)
    pending_output=False
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B3.json').resolve() and not target.exists():pending_output=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'Broken B3 link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B3T-\d{2}\b',planids),(r'\bFE7B3-\d{2}\b',feids),(r'\bINV7B3-\d{2}\b',ivids)):
            for item in re.findall(pattern,content):ck(item in ids,'Unknown B3 ID in '+filename+':'+item)
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            fields=[x.strip() for x in line.replace('**','').strip('|').split('|')];summary[fields[0]]=fields[1:]
    for label,expected in (('التراكمي المفتوح',[248,2,163,82,1]),('7B3 — جديدة',[11,0,6,5,0]),('7B3 — إضافة محدودة',[27,7,20,326])):
        ck(summary.get(label)==list(map(str,expected)),'Current B3 README numeric summary mismatch: '+label)
    previous=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    oldgroups=re.findall(r'^\| G-\d{2} \|.*$',previous['IMPROVEMENTS.md'],re.M)
    livegroups=re.findall(r'^\| G-\d{2} \|.*$',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)
    ck(len(oldgroups)==88 and livegroups[:88]==oldgroups,'Historical G01–88 bodies changed')
    for filename in SHARED_DOCS:
        text=v.read(v.AUDIT/filename)
        ck(all(x in text for x in ('PHASE-07B3.md','7B4','7C','غير مأذونة')),'Current index lacks B3/B4/C/8 boundary: '+filename)

    extra_tools=['check_commercial_report_witnesses.py','validate_commercial_report_part.py','test_commercial_report_audit_validator.py']
    for filename in extra_tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B3 audit-tool syntax error: '+filename+':'+str(ex))
    completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_commercial_report_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout);count=int(m[1]) if m else None
    passed=completed.returncode==0 and count==18;ck(passed,'B3 audit-helper self-tests failed/count mismatch')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_commercial_report_audit_validator.py']=dict(tests_reported=count,expected_tests=18,process_exit_code=completed.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=extra_tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py']+extra_tools})
    report['validation_scope']='current-through7B3-248-plus-frozen-history-not-runtime-certification'
    report['phase_7_delivery']='7A+7B1+7B2+7B3-partial-not-complete7B-or7'
    report['phase_7_remaining_parts']=['7B4-not-started','7C-not-started']
    report['registry_used']='findings.csv'
    report['findings'].update(phase_7=76,phase_7A=28,phase_7B1=23,phase_7B2=14,phase_7B3=11,total_open_not_remediated=248,severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:27,'phase_7B2_union_frozen':306,'phase_7B3_overlap_with_prior_union':7,'phase_7B3_new_paths':20,'unique_union_not_line_or_execution_coverage':326,'inventory_only_no_selected_scope':501})
    report['phase_7B2_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=132,historical_check_record_overwritten=False,partial7B3_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all237=True,next_phase_replans_during_partial7={})
    report['historical_artifact_sha256']=prov['historical_artifact_sha256'];report['date_semantics']=prov['date_semantics']
    report['evidence_rows'].update(dict(phase_7B3_feature_rows_not_completed_features=29,phase_7B3_invariants_not_passed_tests=17,phase_7B3_source_reconciliation_contracts_not_executed_financial_acceptance=10,phase_7B3_unexecuted_acceptance_or_gate_plans=39,phase_7B3_direct_finding_plans=22,phase_7B3_historical_regression_plans=13,phase_7B3_cross_contract_plans=2,phase_7B3_documentary_scope_authorization_gate_plans=2,phase_7B3_historical_extensions_not_new_findings=13,phase_7B3_unresolved_handoffs=6,phase_7B3_unanswered_questions=6,phase_7B3_continuation_groups_not_complete=10,phase_7B3_original_paths_in_ledger=827,phase_7B3_filename_candidates_not_feature_count=98,phase_7B3_screen_candidates_35_regex_plus17_curated_not_feature_count=52,phase_7B3_independent_illustrations_not_erp_tests=20,phase_7B3_bounded_literal_checks_not_application_tests=16,phase_7B3_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending_output
    report['validation']['limit']='Read-only original/protected hashes, exact registry tails/core/all followups, IDs/distributions/links/bounds/scope inclusion, ledger/candidate bookkeeping, cross-links, independent manual illustrations, bounded lexical observations and synthetic audit-checker self-tests ONLY.7A/7B1/7B2 use their own frozen registries/indexes, not current248 or current indexes; current-checker metrics need not equal historical bytes.9 business bodies plus1 launcher and selected XAML/helper/SQL slices do not certify full features/children/queries/templates/deployment.7B4/7C remain not started;8 unauthorized. No ERP/C#/SQL/WPF/SDK/Office execution, semantic/financial/compliance certification, runtime acceptance, production data, all-bugs claim or remediation.'
