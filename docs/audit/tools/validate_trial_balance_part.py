#!/usr/bin/env python3
"""PARTIAL7B13 documentary checks, NEVER ERP acceptance or a progress percentage.

Protect361 prior artifacts/289 cores/ALLnext_phase/exactG01..152. B12 reads OWN
frozen289 rows AND original CRLF bytes plus exact indexes IN MEMORY. No protected
helper edit, global pathlib patch, disk overlay, rebaseline or archive rewrite.
Ten old-depth screens were not ten wholly unread bodies: eight had full C#
ranges before B13. A capability/caller/child/template/schema/ACL contract remains
separate from full local ranges.7C unstarted/8 unauthorized; no application I/O.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections,csv,io,re
from pathlib import Path
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_income_contract_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors,arithmetic_erratum_errors,
)
SCOPE_FILE='review-scope-07B13.csv'
PART_DOCS=('PHASE-07B13.md','TRIAL-BALANCE-CONTRACTS-07B13.md','VALIDATION-07B13.md','PHASE-07-REMAINING-07B13.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B12.csv';SHARED_SNAPSHOT='evidence/shared-indexes-through-07B12.json'
SNAPSHOT_SHA='8d8ec245cfe7220135e924c156b2843fa0f78b399ac013e110293d7d58d0bf19'
SHARED_SHA='d60e5294b8c0faaa7f369765a692cc9fa874bba857cf93db263570e30afe0e49'
PROVENANCE_SHA='d8df420ee95089127dee378afdb23d50d3e3f29da17fa57b44ba859a8a2d7060'
B12_CHECK_SHA='53db4eb6537cbae2b9674d690d2457b05cf8d95c8133169b00fd6829212268fa'
ENTRY_CHECKOUT='1182b4e8ce1ee0d74a55d846bf94370dc0ef31b4'
REVIEWED_BODIES=('frmMezanMorg3a','frmRptBalances','frmRptCostCenter','frmRptKhzna')
EXTENDED_FINDINGS={'P1-004','P1-013','P1-030','P2-010','P3-008','P3-019','P3-020','P3-023','P7-045','P7-046','P7-048','P7-049','P7-050','P7-052','P7-053','P7-062','P7-097','P7-098','P7-108'}
TABLE_SPECS=(('acceptance-tests','P7B13T-',29),('feature-implementation-matrix','FE7B13-',27),('report-invariants','INV7B13-',27),('report-reconciliation','RC7B13-',6),('historical-extensions','EX7B13-',19),('handoffs','H7B13-',6),('questions','Q7B13-',6),('continuation-backlog','BK7B13-',10))
SENTINELS={'FE7B13-26','FE7B13-27','INV7B13-26','INV7B13-27','RC7B13-06','H7B13-06','Q7B13-06','P7B13T-28','P7B13T-29','ALG7B13-20'}

@contextmanager
def historical_b12_inputs(v,frozen289,texts,raw):
    """Exact logical path overlay with restoration on normal/error/nested exit."""
    if len(frozen289)!=289 or len({r['id'] for r in frozen289})!=289:raise ValueError('Exactly289 distinct historical rows required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):raise ValueError('Exact noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except (UnicodeError,csv.Error) as e:raise ValueError('Malformed frozen registry') from e
    if parsed!=frozen289 or raw.count(b'\r\n')!=290 or b'\n' in raw.replace(b'\r\n',b''):raise ValueError('Frozen289 rows/bytes/CRLF disagree')
    original=v.AUDIT;target=Path(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen289,texts):yield
    finally:v.AUDIT=original

def validate_frozen_b12(v,report,prior,frozen287,prov,frozen289):
    ck=v.check
    for p,h in [('evidence/provenance-07B13.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B12.json',B12_CHECK_SHA)]:ck(v.sha(v.AUDIT/p)==h,'B13 immutable entry identity: '+p)
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B13 snapshot context')
    for p,h in prior['historical_artifact_sha256'].items():ck(prov['historical_artifact_sha256'].get(p)==h,'338-to361 continuity: '+p)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B12.json'))
    ck(saved['checkout_head']=='670ae77c05709a85bcf52c6c9a2c73b4eb0c2d7e' and saved['findings']['total_open_not_remediated']==289 and saved['original_project_hashes_matching']==827 and saved['validation']['errors']==[] and saved['historical_artifact_sha256']==prior['historical_artifact_sha256'] and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False,'B12 genuine stdout changed')
    ck(prov['genuine_B12_check_sha256']==B12_CHECK_SHA and prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY_CHECKOUT,'B13 entry checkout/push observation')
    ck(prov['phase7B12_entry_consistency']==dict(original_hashes_matching=827,findings=289,phase_7_delivery='7A+7B1+7B2+7B3+7B4+7B5+7B6+7B7+7B8+7B9+7B10+7B11+7B12-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B13 prior delivery context')
    from validate_income_contract_part import extend_income_contracts
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b12_inputs(v,frozen289,texts,(v.AUDIT/SNAPSHOT).read_bytes()):extend_income_contracts(v,report,prior,frozen287)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B12-289-not-current-state',phase_7B12_historical_input_mode='frozen289-rows-and-exact-CRLF-bytes-and-exact-indexes-in-memory')
    report['phase_7B12_adapter_context']=dict(entry_provenance='evidence/provenance-07B13.json',adapter_protected_artifacts_checked=361,current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True)

def build_current_ledger(inventory,labelled,spans):
    out=prior_ledger(inventory,labelled,spans);selected={r['path']:r['ranges'] for k,s in labelled if k=='7B13' for r in s}
    for r in out:
        r['phase7B13_ranges']=selected.get(r['path'],'none')
        if r['inventory_kind']!='generated-artifact':r.update(continuation_bucket='7B14-or-7C-contract-or-reasoned-exclusion-not-closed',next_scope_work='بقية القدرات أو استبعاد مسند وفق خطة4حزم7B و6محاور7C؛لا نسبةاكتمال أو قبولمنعددالأسطر،و7Cلمتبدأ و8غيرمأذونة.')
    return out

def build_candidate_disposition(inventory,labelled):
    out=prior_candidates(inventory,labelled);selected={r['path']:r['ranges'] for k,s in labelled if k=='7B13' for r in s}
    for r in out:
        r['phase7B13_ranges']=selected.get(r['path'],'none')
        if not r['disposition'].startswith('lexical-false-positive'):r.update(disposition='7B14-further-contract-or-reasoned-exclusion-required',reason='98مرشحاسملاfeaturecount؛لاكلcaller/child/template/schema/ACLمنbodyكامل. لايعادعدC#سابقكجسمغيرمقروء.')
    return out

def build_screen_disposition(inventory,labelled):
    out=prior_screens(inventory,labelled);selected={r['path']:r['ranges'] for k,s in labelled if k=='7B13' for r in s};full={r['path']:'1-'+str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    for n,r in enumerate(out,1):
        r['id']=f'SC7B13-{n:02d}';r['phase7B13_body_ranges']=selected.get(r['body_path'],'none');r['disposition']='7B14-or-7C-further-contracts-or-reasoned-exclusion-required'
        if r['screen'] in REVIEWED_BODIES and all(p in full and selected.get(p)==full[p] for p in (r['path'],r['body_path'])):
            r['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified';r['reason']='7B13يكملXAMLوالعقود؛C#لثلاثةمنالأربعةكانكاملاًفيB2،لاعدجديدلقراءتهالأولى. لاكلنشر/طفل/قالب/تفويض.'
        else:r['reason']='تصنيفعمقدفترتاريخيلامقياسغيرالمقروء؛8من10كانتذاتC#كاملقبلB13. تظل capability/contract أو استبعادمسند.'
    return out

def depth_clarification(inventory,labelled,spans):
    """Frozen disposition/category vs explicit prior source ranges, not a new read."""
    before=[(k,s) for k,s in labelled if k!='7B13']
    old=prior_screens(inventory,before)
    current={r['path']:r['ranges'] for k,s in labelled if k=='7B13' for r in s}
    full_ranges={r['path']:'1-'+str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    out=[]
    for r in old:
        if r['coverage_level']!='prior-selected-slices-depth-not-upgraded':continue
        full='1-'+str(r['body_inventory_lines'])
        phases=[k for k,s in before if any(x['path']==r['body_path'] and x['ranges']==full for x in s)]
        upgraded=r['screen'] in REVIEWED_BODIES and all(p in full_ranges and current.get(p)==full_ranges[p] for p in (r['path'],r['body_path']))
        out.append(dict(id=f'DEP7B13-{len(out)+1:02d}',screen=r['screen'],body_path=r['body_path'],prior_category=r['coverage_level'],prior_full_local_csharp_declared='true' if phases else 'false',prior_full_body_scope_ids=';'.join(phases) or 'none',b13_full_local_body_and_xaml='true' if upgraded else 'false',remaining_old_category_after_b13='false' if upgraded else 'true',interpretation='تصنيف عمق سابق لا شاشة غير مقروءة ولا إغلاق كل feature؛السابق محفوظ بلا rewrite.',runtime_status='not-executed'))
    return out

def remaining_work_errors(plan,depth):
    errors=[]
    if len(plan)!=10 or collections.Counter(r.get('part_family') for r in plan)!={'7B':4,'7C':6}:errors.append('Remaining work must be4 B packages and6 unstarted C axes, not percentages')
    for r in plan:
        for field in ('id','part_family','title','candidate_scope_not_certified','expected_deliverable','static_exit_criterion','dependencies_and_uncertainty'):
            if not isinstance(r.get(field),str) or not r[field].strip():errors.append('Remaining work missing substantive field: '+r.get('id','?')+'.'+field)
        if r.get('status')!='planned-not-started' or r.get('runtime_status')!='not-executed' or r.get('counts_are_sessions_or_completion_percent')!='false':errors.append('Remaining work overclaim: '+r.get('id','?'))
    if len(depth)!=10 or sum(r.get('prior_full_local_csharp_declared')=='true' for r in depth)!=8 or sum(r.get('remaining_old_category_after_b13')=='true' for r in depth)!=6:errors.append('Ten old-category screens are not ten wholly unread bodies')
    return errors

def group_row_errors(previous,current):
    rows=lambda t:re.findall(r'^\| G-\d{2,3} \|.*$',t,re.M)
    return [] if len(rows(previous))==152 and rows(current)[:152]==rows(previous) else ['Historical G01–152 rows changed']

def witness_metadata_errors(w):
    out=[]
    for k in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(k) is not False:out.append('B13 false-only flag: '+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:out.append('B13 integer-zero count: '+k)
    for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed','progress_categories_not_wholly_unread_counts'):
        if w.get(k) is not True:out.append('B13 boundary: '+k)
    for k in ('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k)) is not int or w[k]!=20:out.append('B13 count: '+k)
    if w.get('phase')!='7B13-partial-static-audit':out.append('B13 witness phase')
    return out+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))

def validate_source(v,r,scope):
    if 'evidence' not in r:return
    if r['evidence']=='none-inventory-only':v.check(r['id'] in SENTINELS,'B13 undeclared no-source sentinel: '+r['id'])
    else:
        v.check(r['id'] not in SENTINELS,'B13 fabricated inventory evidence: '+r['id']);v.evidence(r['evidence'],r['id']);v.scoped_evidence(r['evidence'],scope,r['id']+' boundedB13',phase=7)

def extend_trial_balance(v,report,prov,frozen289):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[289:];extensions=rows('evidence/historical-extensions-07B13.csv')
    ck(prov['historical_artifact_count']==361 and len(frozen289)==289,'B13 entry count')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY_CHECKOUT,'B13 actual entry checkout')
    ck(prov['erp_runtime_tests_executed']==0 and prov['sql_or_external_service_tests_executed']==0 and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False,'B13 execution/remediation boundary')
    identity=report['source_reference_validation']
    ck(identity['audited_application_reference']==v.HEAD and identity['reference_ancestor_of_checkout'] is True and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B13 source identity')
    ext=v.transition(frozen289,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for e in registry_transition_errors(frozen289,current,extensions):ck(False,e)
    ck(len(current)==len({r['id'] for r in current})==291 and [r['id'] for r in new]==['P7-118','P7-119'],'B13 registry/newIDs')
    v.distributions(new,{'Medium':2},{'confirmed':2},'boundedB13 only')
    for r in new:ck(r['type']=='implementation-defect' and r['status']=='open-not-remediated' and r['next_phase']=='8','B13 finding status/followup')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B13 headings/registry')
    raw=(v.AUDIT/'findings.csv').read_bytes();ck(not raw.startswith(b'\xef\xbb\xbf') and raw.count(b'\r\n')==292 and b'\n' not in raw.replace(b'\r\n',b''),'B13 noBOM/CRLF registry')
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};inventory=rows('evidence/inventory.csv');paths={r['path'] for r in inventory}
    ck(len(selected)==len(scope)==19,'B13 selected count')
    for r in selected:
        ck(r['path'] in paths and r['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(r['focus']),'B13 scope: '+r['path']);v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    for n in REVIEWED_BODIES:
        for suffix in ('.xaml','.xaml.cs'):
            p='SmartAuditERP/Form_WPF/'+n+suffix;ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B13 local body/XAML: '+p)
    known={r['id'] for r in current}|{f'H7B13-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B13.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for r in data:
            for k,value in r.items():ck(bool(value),'B13 incomplete cell: '+r['id']+'.'+k)
            validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B13 runtime overclaim')
    tests,features,invs,rc=[tables[k] for k in ('P7B13T-','FE7B13-','INV7B13-','RC7B13-')];tids={r['id'] for r in tests};fids={r['id'] for r in features};iids={r['id'] for r in invs}
    v.proposed_tests(tests,'7B13');v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(features+invs,tids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invs,'invariant_ids')):
        for e in bidirectional_errors(pool,tests,field):ck(False,e)
    for e in feature_level_errors(features):ck(False,e)
    for pool,label in ((tests,'plans'),(features,'features'),(invs,'invariants')):v.covered(new,pool,'B13 '+label)
    ck([r['plan_kind'] for r in tests]==['finding-specific']*4+['historical-root-regression']*19+['cross-cutting-contract']*4+['documentary-scope-or-authorization-gate']*2,'B13 plan-kind/order')
    ck({r['finding_ids'] for r in extensions}==EXTENDED_FINDINGS and [r['finding_ids'] for r in features[2:21]]==[r['finding_ids'] for r in extensions],'B13 extension mapping')
    for r in new:ck(len([t for t in tests if t['plan_kind']=='finding-specific' and t['finding_ids']==r['id']])==2,'B13 two direct plans: '+r['id'])
    for r in extensions:ck(r['followup_policy']=='unchanged-during-partial7','B13 hidden replan')
    for r in rc:
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids');expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(r['feature_ids'].split(';'))];ck(r['acceptance_ids'].split(';')==expected and bool(expected),'B13 RC links')
    v.related(tables['Q7B13-'],{r['id'] for r in tables['H7B13-']},'handoff_ids')
    for r in tables['H7B13-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B13 handoff')
    for r in tables['Q7B13-']:ck(r['status']=='unanswered-no-secrets-requested','B13 question')
    for n,r in enumerate(tables['BK7B13-'],1):ck(r['prior_backlog_id']==f'BK7B12-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B13 backlog ancestry')
    ck([r['status'] for r in tables['BK7B13-'][2:6]]==['not-started']*4,'B13 accidentally startsC')
    labelled=[(str(n),rows('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]+[('7A',rows('review-scope-07.csv'))]+[(f'7B{n}',rows(f'review-scope-07B{n}.csv')) for n in range(1,13)]+[('7B13',selected)]
    ck(rows('evidence/coverage-ledger-07B13.csv')==build_current_ledger(inventory,labelled,v.spans),'B13 ledger')
    candidates=rows('evidence/report-candidate-disposition-07B13.csv');screens=rows('evidence/report-screen-disposition-07B13.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B13 filename triage');ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B13 screen triage');v.sequential(screens,'SC7B13-',52)
    before={r['path'] for _,s in labelled[:-1] for r in s};s=set(scope);ck((len(before),len(s&before),len(s-before),len(before|s),len(paths-(before|s)))==(389,18,1,390,437),'B13 union bookkeeping')
    depth=rows('evidence/report-depth-clarification-07B13.csv');plan=rows('evidence/remaining-workplan-07B13.csv');v.sequential(depth,'DEP7B13-',10);v.sequential(plan,'RW7B13-',10);ck(depth==depth_clarification(inventory,labelled,v.spans),'B13 depth clarification')
    for e in remaining_work_errors(plan,depth):ck(False,e)
    w,match=v.recompute('evidence/report-witnesses-07B13.json','tools/check_trial_balance_witnesses.py');alg=w['illustrations'];lex=w['static_lexical_contract_checks'];v.sequential(alg,'ALG7B13-',20);v.sequential(lex,'ST7B13-',20);v.related(alg+lex,known)
    for e in witness_metadata_errors(w):ck(False,e)
    ck(w['errors']==[],'B13 witness has failed observations')
    for r in alg+lex:
        flag='illustration_assertions_passed' if r['id'].startswith('ALG') else 'documented_text_observation_matches';ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B13 witness overclaim');validate_source(v,r,scope)
    for r in w['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B13 lexical bounded read',phase=7)
    pats=[(PART_DOCS[0],r'^\| (EX7B13-\d{2}) \|',[r['id'] for r in extensions]),(PART_DOCS[1],r'^\| (FE7B13-\d{2}) —',[r['id'] for r in features]),(PART_DOCS[1],r'^\| (INV7B13-\d{2}) \|',[r['id'] for r in invs]),(PART_DOCS[1],r'^### (RC7B13-\d{2}) —',[r['id'] for r in rc]),(PART_DOCS[2],r'^\| (P7B13T-\d{2}) \|',[r['id'] for r in tests]),(PART_DOCS[3],r'^\| (DEP7B13-\d{2}) \|',[r['id'] for r in depth]),(PART_DOCS[3],r'^\| (RW7B13-\d{2}) \|',[r['id'] for r in plan]),('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,159)])]
    for file,pat,expected in pats:ck(re.findall(pat,v.read(v.AUDIT/file),re.M)==expected,'B13 Markdown IDs: '+file)
    pending=False;src=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B13.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B13 broken link: '+name+':'+m[1])
        for m in src.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,name,phase=7)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B13.md','PHASE-07-REMAINING-07B13.md','7B14','غير مأذونة','1182b4e','10ba215')),'B13 current index boundary: '+name)
    tools=['check_trial_balance_witnesses.py','validate_trial_balance_part.py','test_trial_balance_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B13 syntax: '+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_trial_balance_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30);m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==24;ck(passed,'B13 self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_trial_balance_audit_validator.py']=dict(tests_reported=count,expected_tests=24,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools;report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B13-291-plus-frozen-history-not-runtime-certification',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,14))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B14-planned-in-four-remaining-B-work-packages-not-guaranteed-session-count','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=119,phase_7B13=2,total_open_not_remediated=291,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:19,'phase_7B12_union_frozen':389,'phase_7B13_overlap_with_prior_union':18,'phase_7B13_new_paths':1,'unique_union_not_line_or_execution_coverage':390,'inventory_only_no_selected_scope':437})
    report['phase_7B12_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=361,historical_check_record_overwritten=False,genuine_b12_check_sha256_unchanged=B12_CHECK_SHA,partial7B13_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all289=True,next_phase_replans_during_partial7={})
    report['phase_7B13_remaining_work_not_completion_percentage']=dict(old_disposition_category_at_entry=10,of_those_prior_full_local_CSharp_bodies=8,b13_local_body_and_xaml_contract_upgrades=4,remaining_old_category=6,remaining_B_work_packages=4,C_axes_not_started=6,counts_are_guaranteed_sessions_or_completion_percent=False)
    report['evidence_rows'].update(dict(phase_7B13_feature_rows_not_completed_features=27,phase_7B13_invariants_not_passed_tests=27,phase_7B13_reconciliation_contracts_not_financial_acceptance=6,phase_7B13_unexecuted_acceptance_or_gate_plans=29,phase_7B13_historical_extensions_not_new_findings=19,phase_7B13_unresolved_handoffs=6,phase_7B13_unanswered_questions=6,phase_7B13_backlog_groups=10,phase_7B13_filename_candidates_not_features=98,phase_7B13_screen_candidates_not_features=52,phase_7B13_illustrations_not_erp_tests=20,phase_7B13_lexical_checks_not_erp_tests=20,phase_7B13_witness_recomputed_matches_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only documentary B13:361 protected artifacts,289 immutable cores/ALLnext_phase/exact evidence prefixes plus19 declared tails;G01..152 exact. Original827 source hashes/source10ba versus pushed B12 entry1182b4e and genuine B12 stdout checkout670ae77 stay separate. Historical helpers including B12 get OWN exact frozen rows/text/CRLF bytes IN MEMORY, no protected edits/global pathlib patch/disk overlay/rebaseline/archive rewrite. Four local bodies/XAML include three C# bodies already full in B2, not four first-ever reads. Ten old-depth screens included eight prior full C# bodies; six remain in that category after four local upgrades, NOT all report/capability closure. Four remaining B work packages and six unstarted C axes are planning groups, not guaranteed sessions/percent/time. P7-118 is missing depth2 traversal, not a stub or carryforward; P7-119 is the explicit local FlowDocument previous-column projection, not signed-summary P7-093 or speculation about REPX. Existing roots for carryforward/summary grain/cost-center membership/opening/date/treasury identity/snapshot/partial/CSV/HTML/REPX/finalization remain deduplicated. B12 output-path and zero-stock findings remain, not reused IDs. Statement aggregate P3-022 and supplied-vs-deployed schema gates remain; Apply/new/disabled/Closing/using/WriteAllText/typed GlobalID+branch routing are positive bounded evidence, not deployed authorization, financial acceptance or measured leak/index/latency. B10 additive10vs120 erratum retained without rewrite.20manual+20lexical+24new synthetic checker cases are documentary,29 acceptance/gate plans not-executed.7B/7 partial,7B14 planned,7C unstarted,8 unauthorized. No application import/build/C#/SQL/WPF/REPX/Office/COM/formula/HTML interpreter/provider/device/printer/actual export/shell, remediation, real data/secrets or operational measurements.'
