#!/usr/bin/env python3
"""Additive documentary checks for PARTIAL7B2; not application acceptance.

Historical7B1's helper and all its inputs remain frozen. Its current-registry
and shared-index reads are temporarily overlaid IN MEMORY with the exact223
snapshot and original index texts at their logical audit-root paths. No file is
rewritten by this validator. The new layer checks current237, declared spans,
link consistency, independent fixtures and synthetic audit-checker self-tests.
It never imports/builds the ERP or writes any evidence/baseline files.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from validate_report_part import build_ledger, bidirectional_errors

SCOPE_FILE='review-scope-07B2.csv'
PART_DOCS=('PHASE-07B2.md','FINANCIAL-INVENTORY-REPORTS-07B2.md','VALIDATION-07B2.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
EXTENDED_FINDINGS={'P1-011','P1-033','P1-013','P2-001','P2-010','P3-008','P3-019','P3-023','P4-007','P4-008','P7-045','P7-046','P7-048','P7-049','P7-050'}
SENTINELS={'FE7B2-31','FE7B2-32','H7B2-05','H7B2-06','P7B2T-45','P7B2T-46'}
SNAPSHOT='evidence/findings-through-07B1.csv'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B1.json'
SNAPSHOT_SHA='6d5fb444d24b17c986a6703425c8e844cf62c40f1ffbf7a1c8eff437be01dd82'


@contextmanager
def historical_b1_inputs(v, frozen223, shared_texts):
    """Purely in-memory temporary adapters; restore identities even on failure.

    frozen223 and shared_texts must be read from hash-protected entry artifacts
    by the caller. Returning fresh dictionaries prevents the old helper from
    mutating its original snapshot. Actual files/path semantics never change.
    """
    if set(shared_texts)!=set(SHARED_DOCS) or not all(isinstance(x,str) for x in shared_texts.values()):
        raise ValueError('Exactly three frozen shared-index texts required')
    original_read,original_rows=v.read,v.rows
    overrides={(v.AUDIT/name).resolve():content for name,content in shared_texts.items()}
    def historical_read(path):
        key=Path(path).resolve()
        return overrides[key] if key in overrides else original_read(path)
    def historical_rows(relative):
        if relative=='findings.csv':return [dict(x) for x in frozen223]
        return original_rows(relative)
    try:
        v.read,v.rows=historical_read,historical_rows
        yield
    finally:
        v.read,v.rows=original_read,original_rows


def validate_frozen_b1(v, report, prov7b, frozen200, prov7b2, frozen223):
    """Reuse the protected7B1 checker unchanged, against its OWN frozen inputs."""
    v.check(prov7b2['shared_indexes_at_entry']==SHARED_SNAPSHOT,'7B1 index snapshot identity changed')
    snap=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))
    texts=snap['files']
    from validate_report_part import extend_report
    with historical_b1_inputs(v,frozen223,texts):
        extend_report(v,report,prov7b,frozen200)
    report['registry_used']=SNAPSHOT
    report['phase_7B1_historical_input_mode']='frozen223-and-exact-shared-index-texts-at-original-logical-paths'
    report['phase_7B1_recomputed_with_current_checker_not_original_metric_replay']=True
    report['validation_scope']='historical-through7B1-223-not-current-state'
    report['phase_7B1_adapter_context']=dict(entry_provenance='evidence/provenance-07B2.json',adapter_protected_artifacts_checked=110,
        current_registry_and_shared_indexes_not_inputs=True,historical_remaining_parts_are_status_at_delivery_not_current=True)
    report['validation']['limit']+=' HistoricalB1 reads the frozen223 registry and three frozen shared-index texts in memory; current237/new shared indexes are NOT its inputs. Remaining-parts labels describe the historical cutoff, not current delivery. No protected helper/report is rewritten.'


def registry_transition_errors(previous,current,manifest):
    """Pure exact-tail/core/schedule check used by helper mutation tests too."""
    errors=[]
    if len(current)<len(previous):errors.append('Historical registry truncated')
    if [r['id'] for r in current[:len(previous)]]!=[r['id'] for r in previous]:errors.append('Historical registry order changed')
    tails={r['finding_ids']:r['evidence'] for r in manifest}
    if len(tails)!=len(manifest):errors.append('Duplicate extension manifest root')
    known={x['id'] for x in previous}
    if set(tails)-known:errors.append('Extension for unknown historical root')
    for old,new in zip(previous,current):
        fid=old['id']
        for key in old:
            if key=='evidence':continue
            if new.get(key)!=old[key]:errors.append('Historical core/schedule changed: '+fid+'.'+key)
        expected=old['evidence']+(';' + tails[fid] if fid in tails else '')
        if new.get('evidence')!=expected:errors.append('Non-exact historical evidence tail: '+fid)
    return errors


def build_current_ledger(inventory,labelled_scopes,parse_ranges):
    """Frozen bookkeeping algorithm plus explicit B2/future labels, no source I/O."""
    ledger=build_ledger(inventory,labelled_scopes,parse_ranges)
    b2={r['path']:r['ranges'] for label,scope in labelled_scopes if label=='7B2' for r in scope}
    for x in ledger:
        p=x['path'];x['phase7B2_ranges']=b2.get(p,'none')
        if x['inventory_kind']=='generated-artifact':
            x['continuation_bucket']='8-artifact-provenance-only-not-authorized'
            x['next_scope_work']='أصل مخرجات متتبعة؛ لا تشغيل أو ثقة من وجودها. توريد وبناء مصدر مستقل في8 بإذن لاحق.'
        elif p in b2:
            x['continuation_bucket']='7B2-selected-slices-further-7B3-or-7C-work-not-closed'
            x['next_scope_work']='مقاطع7B2 معلنة فقط؛ الباقي والمتصلون والقوالب/السياسات لم يغلقوا. استكمل في7B3/7C أو قدم استبعاداً مسنداً؛ لا قبول.'
        elif re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I):
            x['continuation_bucket']='7B3-name-candidate-or-prior-slices-not-feature-closed'
            x['next_scope_work']='فرز اسم فقط أو مقاطع سابقة؛ حدد feature/query/source/identity/filter/total/output/ACL أو استبعاداً مسنداً. مثال FingerPrintDevice لفظي لا تقرير أعمال تلقائياً.'
        else:
            x['continuation_bucket']='7C-source-ui-resource-candidate-not-started'
            x['next_scope_work']='استكمال قدرات7C ودورة الموارد/الوصول/الثقافات/الأداء أو استبعاد مسند؛ لا ترقية المقاطع التاريخية إلى مراجعة كاملة.'
    return ledger


def build_candidate_disposition(inventory,labelled_scopes):
    """Name-only triage is deliberately NOT a list of completed report features."""
    b2={r['path']:r['ranges'] for label,scope in labelled_scopes if label=='7B2' for r in scope}
    result=[]
    for x in inventory:
        p=x['path']
        if not re.search('(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I):continue
        phases=[label for label,scope in labelled_scopes if any(r['path']==p for r in scope)]
        state='name-only-no-selected-scope' if not phases else 'selected-slices-not-whole-feature-closed'
        if Path(p).name=='FingerPrintDevice.cs':
            disposition='lexical-false-positive-for-report-family-7C-biometric-followup'
            reason='print داخل FingerPrint؛ سبق فحص مقاطع بصمة في7A، ولا يعد تقريراً بسبب الاسم.'
        else:
            disposition='7B3-further-scope-or-reasoned-exclusion-required'
            reason='لا all-callers/templates/schema/runtime coverage من الاسم أو بعض النطاقات. المركزي لا يغطي كل متصل؛ يلزم حسم جزء/استبعاد لاحق.'
        result.append(dict(path=p,selection_basis='filename-regex-only-not-a-feature-inventory',selected_phase_ids=';'.join(phases) or 'none',
            phase7B2_ranges=b2.get(p,'none'),coverage_state=state,disposition=disposition,reason=reason,runtime_status='not-executed'))
    return result


def validate_source(v,row,scope):
    if 'evidence' not in row:return
    e=row['evidence']
    if e=='none-inventory-only':
        v.check(row['id'] in SENTINELS,'Undeclared no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'Inventory-only boundary lost: '+row['id'])
        v.evidence(e,row['id'])
        v.scoped_evidence(e,scope,row['id']+' partial7B2',phase=7)


def extend_financial_report(v,report,prov,frozen223,prior_prov):
    """Add current B2 layer; all changes are to the in-memory result object."""
    ck,r=v.check,v.rows
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and len(frozen223)==223,'7B2 frozen entry mismatch')
    ck(prov['phase7B1_entry_consistency']==dict(original_hashes_matching=827,findings=223,phase_7_delivery='7A+7B1-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'7B2 entry metadata no longer describes deliveredB1')
    for p,digest in prior_prov['historical_artifact_sha256'].items():
        ck(prov['historical_artifact_sha256'].get(p)==digest,'86-to110 historical continuity failed: '+p)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B1.json'))
    ck(saved['validation']['errors']==[] and saved['findings']['total_open_not_remediated']==223 and saved['original_project_hashes_matching']==827 and saved['historical_artifact_sha256']==prior_prov['historical_artifact_sha256'],'Protected B1 check no longer describes its historical successful check')
    current=r('findings.csv');new=current[223:]
    extensions=r('evidence/historical-extensions-07B2.csv')
    ext=v.transition(frozen223,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for e in registry_transition_errors(frozen223,current,extensions):ck(False,e)
    ck(len(current)==237 and len({x['id'] for x in current})==237,'B2 count/uniqueness mismatch')
    ck([x['id'] for x in new]==[f'P7-{n:03d}' for n in range(52,66)],'B2 new finding IDs/order mismatch')
    v.distributions(new,{'High':9,'Medium':5},{'confirmed':14},'partial7B2 only')
    for x in new:
        ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and x['type']=='implementation-defect' and bool(x['title']),'B2 classification/status/followup mismatch: '+x['id'])
    heads=re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/'PHASE-07B2.md'),re.M)
    ck(heads==[(x['id'],x['title']) for x in new],'B2 report heading/title/registry mismatch')
    inventory=r('evidence/inventory.csv');paths={x['path'] for x in inventory}
    scopes=r(SCOPE_FILE)
    ck(len(scopes)==33 and len({x['path'] for x in scopes})==33,'B2 scope count/duplicates mismatch')
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths and x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),'B2 scope path/state mismatch: '+x['path'])
        v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in new:validate_source(v,x,scope)

    specs=(('acceptance-tests-07B2.csv','P7B2T-',46),('feature-implementation-matrix-07B2.csv','FE7B2-',32),
        ('report-invariants-07B2.csv','INV7B2-',18),('report-reconciliation-07B2.csv','RC7B2-',14),
        ('historical-extensions-07B2.csv','EX7B2-',15),('handoffs-07B2.csv','H7B2-',6),
        ('questions-07B2.csv','Q7B2-',6),('continuation-backlog-07B2.csv','BK7B2-',10))
    known={x['id'] for x in current}|{f'H7-{i:02d}' for i in range(1,9)}|{f'H7B-{i:02d}' for i in range(1,9)}|{f'H7B2-{i:02d}' for i in range(1,7)}
    tables={}
    for filename,prefix,count in specs:
        data=r('evidence/'+filename);tables[prefix]=data
        v.sequential(data,prefix,count);v.related(data,known)
        for x in data:
            for k,value in x.items():ck(bool(value),f'Incomplete B2 cell: {x["id"]}.{k}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:ck(x['runtime_status']=='not-executed','B2 runtime claim: '+x['id'])
    tests,features,invariants,rc=tables['P7B2T-'],tables['FE7B2-'],tables['INV7B2-'],tables['RC7B2-']
    planids={x['id'] for x in tests};feids={x['id'] for x in features};ivids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B2')
    v.related(tests,feids,'feature_ids');v.related(tests,ivids,'invariant_ids')
    v.related(features+invariants,planids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for e in bidirectional_errors(pool,tests,field):ck(False,e)
    for pool,label in ((tests,'plans'),(features,'features'),(invariants,'invariants')):v.covered(new,pool,'7B2 '+label)
    for x in new:
        direct=[t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==x['id']]
        ck(len(direct)==2,'B2 finding lacks two direct plans: '+x['id'])
    ck([x['plan_kind'] for x in tests]==['finding-specific']*28+['historical-root-regression']*15+['cross-cutting-contract']*3,'B2 plan-kind distinction changed')
    ck([x['finding_ids'] for x in features[:14]]==[x['id'] for x in new],'Primary B2 feature mapping changed')
    ck([x['finding_ids'] for x in features[14:29]]==[x['finding_ids'] for x in extensions],'Historical B2 feature mapping changed')
    for x in features:
        ck(x['implementation_status'] in {'implemented-with-observed-defects','conditional-policy-or-external-contract','rechecked-prior-root-not-new-finding','deferred-not-implementation-reviewed'},'Feature implementation overclaim: '+x['id'])
    for x in features[-2:]:ck(x['coverage_level']=='inventory-only-not-implementation-reviewed' and x['evidence']=='none-inventory-only','Future feature promoted into source coverage: '+x['id'])
    for x in rc:
        v.related([x],feids,'feature_ids');v.related([x],planids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(x['feature_ids'].split(';'))&set(t['feature_ids'].split(';'))]
        ck(x['acceptance_ids'].split(';')==expected and bool(expected),'RC acceptance reverse mismatch: '+x['id'])
        associated={fid for fe in features if fe['id'] in x['feature_ids'].split(';') for fid in fe['finding_ids'].split(';')}
        ck(set(x['finding_ids'].split(';'))<=associated,'RC finding lacks associated feature: '+x['id'])
    ck({x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'B2 extension manifest root mismatch')
    for x in extensions:ck(x['followup_policy']=='unchanged-during-partial7','B2 extension replan claim: '+x['id'])
    v.related(tables['Q7B2-'],{x['id'] for x in tables['H7B2-']},'handoff_ids')
    for x in tables['H7B2-']:ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','B2 handoff falsely resolved: '+x['id'])
    for x in tables['Q7B2-']:ck(x['status']=='unanswered-no-secrets-requested','B2 question falsely resolved: '+x['id'])
    for i,x in enumerate(tables['BK7B2-'],1):
        ck(x['prior_backlog_id']==f'BK7B-{i:02d}' and x['original_backlog_id']==f'BK7-{i:02d}' and x['part'] in {'7B3','7C','7B3/7C'} and x['status']!='complete','B2 backlog closed/lost mapping: '+x['id'])
    ck([x['status'] for x in tables['BK7B2-'][2:6]]==['not-started']*4,'7C inadvertently started')

    labelled=[(str(i),r('review-scope.csv' if i==1 else f'review-scope-{i:02d}.csv')) for i in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv')),('7B1',r('review-scope-07B1.csv')),('7B2',scopes)]
    ledger=r('evidence/coverage-ledger-07B2.csv')
    ck(ledger==build_current_ledger(inventory,labelled,v.spans),'B2 range ledger mismatch; no reading certification inferred')
    candidates=r('evidence/report-candidate-disposition-07B2.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'98 name-only candidate disposition mismatch')
    prior={x['path'] for _,items in labelled[:-1] for x in items};selected=set(scope);union=prior|selected
    ck(len(prior)==288 and len(selected&prior)==15 and len(selected-prior)==18 and len(union)==306 and len(paths-union)==521,'B2 overlap/new/union/inventory-only mismatch')

    witness,match=v.recompute('evidence/report-witnesses-07B2.json','tools/check_financial_report_witnesses.py')
    algebra,lexical=witness['illustrations'],witness['static_lexical_contract_checks']
    v.sequential(algebra,'ALG7B2-',22);v.sequential(lexical,'ST7B2-',14)
    ck(witness['phase']=='7B2-partial-static-audit' and witness['illustration_count']==22 and witness['static_lexical_contract_check_count']==14 and witness['application_remediation_performed'] is False and witness['real_business_or_secret_data_used'] is False and witness['spreadsheet_or_formula_interpreter_executed'] is False,'B2 witness metadata execution overclaim')
    v.related(algebra+lexical,known)
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x[flag] is True and x['source_application_executed'] is False and bool(x['limit']),'B2 witness failed/overclaimed: '+x['id'])
        validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'B2 bounded lexical read',phase=7)

    for filename,pattern,expected in (
        ('VALIDATION-07B2.md',r'^\| (P7B2T-\d{2}) \|',[x['id'] for x in tests]),
        ('FINANCIAL-INVENTORY-REPORTS-07B2.md',r'^\| (FE7B2-\d{2}) —',[x['id'] for x in features]),
        ('FINANCIAL-INVENTORY-REPORTS-07B2.md',r'^\| (INV7B2-\d{2}) \|',[x['id'] for x in invariants]),
        ('FINANCIAL-INVENTORY-REPORTS-07B2.md',r'^### (RC7B2-\d{2}) —',[x['id'] for x in rc]),
        ('FINANCIAL-INVENTORY-REPORTS-07B2.md',r'^\| (H7B2-\d{2}) —',[x['id'] for x in tables['H7B2-']]),
        ('FINANCIAL-INVENTORY-REPORTS-07B2.md',r'^\| (Q7B2-\d{2}) \|',[x['id'] for x in tables['Q7B2-']]),
        ('FINANCIAL-INVENTORY-REPORTS-07B2.md',r'^\| (BK7B2-\d{2}) \|',[x['id'] for x in tables['BK7B2-']]),
        ('PHASE-07B2.md',r'^\| (EX7B2-\d{2}) \|',[x['id'] for x in extensions]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2}) \|',[f'G-{i:02d}' for i in range(1,89)])):
        ck(re.findall(pattern,v.read(v.AUDIT/filename),re.M)==expected,'B2 Markdown IDs/order mismatch in '+filename+':'+pattern)
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    pending_output=False
    for filename in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/filename;content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(parsed.path)).resolve()
            # The output record is produced AFTER the first check, not fabricated
            # as a placeholder input. Subsequent/final checks verify it exists.
            if target==(v.AUDIT/'evidence/checks-07B2.json').resolve() and not target.exists():
                pending_output=True
                continue
            v.LINK_COUNT+=1
            ck(target.exists(),'Broken B2 current link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for pattern,ids in ((r'\bP7B2T-\d{2}\b',planids),(r'\bFE7B2-\d{2}\b',feids),(r'\bINV7B2-\d{2}\b',ivids)):
            for m in re.findall(pattern,content):ck(m in ids,'Unknown B2 ID in '+filename+':'+m)
    extra_tools=['check_financial_report_witnesses.py','validate_financial_report_part.py','test_financial_report_audit_validator.py']
    for filename in extra_tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex:ck(False,'B2 audit Python syntax error: '+filename+':'+str(ex))
    # Check the live summary, not only CSV IDs or historical virtual indexes.
    summary={}
    for line in v.read(v.AUDIT/'README.md').splitlines():
        if line.startswith('|'):
            fields=[cell.strip() for cell in line.replace('**','').strip('|').split('|')]
            if fields:summary[fields[0]]=fields[1:]
    for label,expected in (('التراكمي المفتوح',[237,2,157,77,1]),('7B2 — جديدة',[14,0,9,5,0]),('7B2 — إضافة محدودة',[33,15,18,306])):
        ck(summary.get(label)==list(map(str,expected)),'Current README numeric summary mismatch: '+label)
    index_snapshot=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    previous_groups=re.findall(r'^\| G-\d{2} \|.*$',index_snapshot['IMPROVEMENTS.md'],re.M)
    live_groups=re.findall(r'^\| G-\d{2} \|.*$',v.read(v.AUDIT/'IMPROVEMENTS.md'),re.M)
    ck(len(previous_groups)==80 and live_groups[:80]==previous_groups,'Historical G01–80 group bodies changed in current index')
    for filename in SHARED_DOCS:
        content=v.read(v.AUDIT/filename)
        ck('PHASE-07B2.md' in content and '7B3' in content and '7C' in content and 'غير مأذونة' in content,'Current shared index lacks B2/remaining-parts/authorization boundary: '+filename)
    # Execute only the reviewed AUDIT helper suites, in isolated Python processes.
    # They import audit modules/synthetic fixtures, never any ERP code. Do not
    # store nondeterministic durations or unittest output in this stable record.
    selftests={}
    for filename,expected in (('test_audit_validator.py',10),('test_report_audit_validator.py',14),('test_financial_report_audit_validator.py',20)):
        completed=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools'/filename)],cwd=v.ROOT,
            capture_output=True,text=True,timeout=30)
        test_summary_match=re.search(r'Ran (\d+) tests? in ',completed.stderr+'\n'+completed.stdout)
        actual_count=int(test_summary_match[1]) if test_summary_match else None
        passed=completed.returncode==0 and actual_count==expected
        ck(passed,'Audit-only helper self-tests failed/count mismatch: '+filename)
        selftests[filename]=dict(tests_reported=actual_count,expected_tests=expected,process_exit_code=completed.returncode,
            result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']=selftests
    report['validation']['current_audit_checker_source_sha256_not_original_application']={
        'tools/'+filename:v.sha(v.AUDIT/'tools'/filename) for filename in ['validate_audit.py']+extra_tools}
    report['validation']['audit_only_python_tools_syntax_checked']+=extra_tools
    report['validation_scope']='current-through7B2-237-plus-frozen-history-not-runtime-certification'
    report['phase_7_delivery']='7A+7B1+7B2-partial-not-complete7B-or7'
    report['phase_7_remaining_parts']=['7B3-not-started','7C-not-started']
    report['registry_used']='findings.csv'
    report['findings'].update(phase_7=65,phase_7A=28,phase_7B1=23,phase_7B2=14,total_open_not_remediated=237,
        severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:33,'phase_7B1_union_frozen':288,'phase_7B2_overlap_with_prior_union':15,'phase_7B2_new_paths':18,
        'unique_union_not_line_or_execution_coverage':306,'inventory_only_no_selected_scope':521})
    report['phase_7B1_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,
        frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=110,historical_check_record_overwritten=False,
        partial7B2_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all223=True,
        next_phase_replans_during_partial7={},limit='HistoricalB1 rerun uses current checker/frozen inputs; metric counts are not asserted byte-identical to original checks-07B1.')
    report['historical_artifact_sha256']=prov['historical_artifact_sha256']
    report['date_semantics']=prov['date_semantics']
    report['evidence_rows'].update(dict(phase_7B2_feature_rows_not_completed_features=32,phase_7B2_invariants_not_passed_tests=18,
        phase_7B2_source_reconciliation_contracts_not_executed_gl_acceptance=14,phase_7B2_unexecuted_acceptance_or_gate_plans=46,
        phase_7B2_direct_finding_plans=28,phase_7B2_historical_regression_plans=15,phase_7B2_cross_cutting_contract_or_gate_plans=3,
        phase_7B2_historical_extensions_not_new_findings=15,phase_7B2_unresolved_handoffs=6,phase_7B2_unanswered_questions=6,
        phase_7B2_continuation_groups_not_complete=10,phase_7B2_original_paths_in_ledger=827,phase_7B2_name_only_candidates_not_report_feature_count=98,
        phase_7B2_independent_illustrations_not_erp_tests=22,phase_7B2_bounded_literal_checks_not_application_tests=14,
        phase_7B2_illustrations_and_text_checks_recomputed_match_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending_output
    report['validation']['limit']='Read-only original/protected artifact hashes, exact registry tails/core/followups, IDs/distributions/links/bounds/selected-range inclusion, ledger/name-only bookkeeping, cross-links, independent illustrations/bounded text checks and synthetic audit-checker self-tests. Historical7A/7B1 use their frozen inputs, not the current registry/shared indexes; this is not byte-identical replay of historical metric counts. CurrentB2 remains partial:7B3 and7C not started;8 unauthorized. No semantic/financial certification, deployed-schema/policy/vendor validation, application imports/build/execution, WPF rendering, real acceptance, remediation or claim that every line/path/feature was reviewed.'
