#!/usr/bin/env python3
"""PARTIAL7B14 documentary contracts, NEVER application acceptance.

Protect387 prior artifacts/291 cores/ALLnext_phase/exactG01..158. Historical
B13 receives its OWN291 rows, exact rawCRLF bytes and three exact index texts
IN MEMORY. No protected edits, global pathlib patch, disk overlay, rebaseline
or archive rewrite. Four local parents/XAML include three bodies already full
inB2, not four first-ever C# reviews. B-R1 residuals stay open;7B15/R2 proposed,
7C unstarted,8 unauthorized. No application import/build/execution/remediation.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections,csv,io,re
from pathlib import Path
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,registry_transition_errors,bidirectional_errors
from validate_trial_balance_part import (
    build_current_ledger as prior_ledger,build_candidate_disposition as prior_candidates,
    build_screen_disposition as prior_screens,feature_level_errors,arithmetic_erratum_errors,
)
SCOPE_FILE='review-scope-07B14.csv'
PART_DOCS=('PHASE-07B14.md','INVENTORY-ACTIVITY-CONTRACTS-07B14.md','VALIDATION-07B14.md','PHASE-07-REMAINING-07B14.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
SNAPSHOT='evidence/findings-through-07B13.csv';SHARED_SNAPSHOT='evidence/shared-indexes-through-07B13.json'
SNAPSHOT_SHA='36b7661e42a7fd564ce72e07619f6a5454c54e5ff13bbf8d8f27d750adb8fffa'
SHARED_SHA='db9fd0d80eedde865a19621aa4196811641f320b6ade9d72e44e6de126dc2d4a'
PROVENANCE_SHA='61b8daf25450653ba70b5a425395573fcfcd0af66506510362cee3c5c48655ac'
B13_CHECK_SHA='66b6043658fde124ceec87a994608ff356ce21c53199be63f126d66d83bacf5b'
PRIOR_PROVENANCE_SHA='d8df420ee95089127dee378afdb23d50d3e3f29da17fa57b44ba859a8a2d7060'
ENTRY_CHECKOUT='461ceaf3e14e67e1c5b3f97a202d874746f6523f'
REVIEWED_BODIES=('frmRptInventory','frmRptItemsActivity','frmRptItemsActivityDetailed','frmRptItemsExpiration')
EXTENDED_FINDINGS={'P1-004','P1-013','P2-010','P2-011','P3-023','P4-007','P7-041','P7-045','P7-046','P7-048','P7-049','P7-054','P7-055','P7-056','P7-057','P7-058','P7-059','P7-060','P7-061','P7-063','P7-085','P7-108'}
TABLE_SPECS=(('acceptance-tests','P7B14T-',34),('feature-implementation-matrix','FE7B14-',31),('report-invariants','INV7B14-',31),('report-reconciliation','RC7B14-',6),('historical-extensions','EX7B14-',22),('handoffs','H7B14-',6),('questions','Q7B14-',6),('continuation-backlog','BK7B14-',10))
SENTINELS={'FE7B14-30','FE7B14-31','INV7B14-30','INV7B14-31','RC7B14-06','H7B14-06','Q7B14-06','P7B14T-33','P7B14T-34','ALG7B14-24'}


@contextmanager
def historical_b13_inputs(v,frozen291,texts,raw):
    """One logical path, exact bytes, copied rows/texts; always restore objects."""
    if len(frozen291)!=291 or len({r['id'] for r in frozen291})!=291:
        raise ValueError('Exactly291 distinct historical rows required')
    if type(raw) is not bytes or raw.startswith(b'\xef\xbb\xbf'):
        raise ValueError('Exact noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except (UnicodeError,csv.Error) as e:raise ValueError('Malformed frozen registry') from e
    if parsed!=frozen291 or raw.count(b'\r\n')!=292 or b'\n' in raw.replace(b'\r\n',b''):
        raise ValueError('Frozen291 rows/bytes/CRLF disagree')
    original=v.AUDIT;target=Path(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):
            return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen291,texts):yield
    finally:v.AUDIT=original


def validate_frozen_b13(v,report,prior,frozen289,prov,frozen291):
    ck=v.check
    for p,h in [('evidence/provenance-07B14.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B13.json',B13_CHECK_SHA)]:
        ck(v.sha(v.AUDIT/p)==h,'B14 immutable entry identity: '+p)
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B14 snapshot context')
    for p,h in prior['historical_artifact_sha256'].items():
        ck(prov['historical_artifact_sha256'].get(p)==h,'361-to387 continuity: '+p)
    saved=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B13.json'))
    ck(saved['checkout_head']=='1182b4e8ce1ee0d74a55d846bf94370dc0ef31b4' and saved['findings']['total_open_not_remediated']==291 and saved['original_project_hashes_matching']==827 and saved['validation']['errors']==[] and saved['historical_artifact_sha256']==prior['historical_artifact_sha256'] and saved['validation']['current_output_record_pending_first_write_not_placeholder'] is False,'B13 genuine stdout changed')
    ck(prov['genuine_B13_check_sha256']==B13_CHECK_SHA and prov['prior_provenance_B13_sha256']==PRIOR_PROVENANCE_SHA and prov['genuine_B13_check_record_checkout']==saved['checkout_head'],'B14 prior provenance/stdout identity')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY_CHECKOUT,'B14 entry checkout/push observation')
    ck(prov['phase7B13_entry_consistency']==dict(original_hashes_matching=827,findings=291,phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,14))+'-partial-not-complete7B-or7',errors=[],erp_runtime_tests_executed=0),'B14 prior delivery context')
    reconciliation=prov['entry_checkout_reconciliation']
    ck(reconciliation['initial_restored_checkout']==v.HEAD and reconciliation['all392_workspace_document_bytes_matched_completed_authorized_remote_before_fast_forward'] is True and reconciliation['application_byte_changes'] is False,'B14 same-branch checkout reconciliation')
    from validate_trial_balance_part import extend_trial_balance
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    with historical_b13_inputs(v,frozen291,texts,(v.AUDIT/SNAPSHOT).read_bytes()):
        extend_trial_balance(v,report,prior,frozen289)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B13-291-not-current-state',phase_7B13_historical_input_mode='frozen291-rows-and-exact-CRLF-bytes-and-exact-indexes-in-memory')
    report['phase_7B13_adapter_context']=dict(entry_provenance='evidence/provenance-07B14.json',adapter_protected_artifacts_checked=387,current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True)


def build_current_ledger(inventory,labelled,spans):
    out=prior_ledger(inventory,labelled,spans)
    selected={r['path']:r['ranges'] for k,s in labelled if k=='7B14' for r in s}
    for r in out:
        r['phase7B14_ranges']=selected.get(r['path'],'none')
        if r['inventory_kind']!='generated-artifact':
            r.update(continuation_bucket='7B15-or-7C-contract-or-reasoned-exclusion-not-closed',next_scope_work='استكمال B-R2 ثم العقود المشتركة B-R3 وتجميع B-R4 وبقايا B-R1 المحالة؛ 4 حزم تنظيمية لا4جلسات. 7C بمحاورها6 لم تبدأ، و8 غير مأذونة؛ لا اكتمال قدرات من مدى الأسطر.')
    return out


def build_candidate_disposition(inventory,labelled):
    out=prior_candidates(inventory,labelled)
    selected={r['path']:r['ranges'] for k,s in labelled if k=='7B14' for r in s}
    for r in out:
        r['phase7B14_ranges']=selected.get(r['path'],'none')
        if not r['disposition'].startswith('lexical-false-positive'):
            r.update(disposition='7B15-further-contract-or-reasoned-exclusion-required',reason='98 مرشح اسم لا تعداد قدرات؛ 4 آباء/XAML محلية لا كل caller/child/template/schema/ACL. B-R1 residuals إلى العقود المشتركة؛ لا إعادة عد C# كامل سابقاً كأول قراءة.')
    return out


def build_screen_disposition(inventory,labelled):
    out=prior_screens(inventory,labelled)
    selected={r['path']:r['ranges'] for k,s in labelled if k=='7B14' for r in s}
    full={r['path']:'1-'+str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    for n,r in enumerate(out,1):
        r['id']=f'SC7B14-{n:02d}';r['phase7B14_body_ranges']=selected.get(r['body_path'],'none')
        r['disposition']='7B15-or-7C-further-contracts-or-reasoned-exclusion-required'
        if r['screen'] in REVIEWED_BODIES and all(p in full and selected.get(p)==full[p] for p in (r['path'],r['body_path'])):
            r['coverage_level']='bounded-local-body-and-xaml-not-whole-feature-certified'
            r['reason']='B14 يكمل XAML والعقود المحلية؛ ثلاثة C# كاملة سابقاً فيB2، وdetailed وحده جديد اكتمال الجسم بين الأربعة. لا إغلاق للطفل/القالب/المخطط/ACL أو كل حزمة B-R1.'
        else:r['reason']='تصنيف عمق لا مقام اكتمال؛ خارج الترقيات المحلية تبقى capability/contract أو استبعاد مسند، ولا يبدأ7C من ذكر عمر WPF فيB14.'
    return out


def depth_clarification(inventory,labelled,spans):
    """Six old categories at entry, five prior full bodies, four local upgrades."""
    before=[(k,s) for k,s in labelled if k!='7B14'];old=prior_screens(inventory,before)
    current={r['path']:r['ranges'] for k,s in labelled if k=='7B14' for r in s}
    full_ranges={r['path']:'1-'+str(r['lines']) for r in inventory if str(r['lines']).isdigit()}
    out=[]
    for r in old:
        if r['coverage_level']!='prior-selected-slices-depth-not-upgraded':continue
        full='1-'+str(r['body_inventory_lines'])
        phases=[k for k,s in before if any(x['path']==r['body_path'] and x['ranges']==full for x in s)]
        upgraded=r['screen'] in REVIEWED_BODIES and all(p in full_ranges and current.get(p)==full_ranges[p] for p in (r['path'],r['body_path']))
        out.append(dict(id=f'DEP7B14-{len(out)+1:02d}',screen=r['screen'],body_path=r['body_path'],prior_category=r['coverage_level'],prior_full_local_csharp_declared='true' if phases else 'false',prior_full_body_scope_ids=';'.join(phases) or 'none',b14_full_local_body_and_xaml='true' if upgraded else 'false',remaining_old_category_after_b14='false' if upgraded else 'true',interpretation='ستة تصنيفات عند الدخول، منها خمسة C# كاملة سابقاً؛ أربعة body/XAML محلية تترك اثنتين لا كل بواقي7B. التاريخ محفوظ بلا rewrite، ولا whole-feature من كامل body.',runtime_status='not-executed'))
    return out


def remaining_work_errors(plan,depth):
    errors=[]
    if len(plan)!=10 or collections.Counter(r.get('part_family') for r in plan)!={'7B':4,'7C':6}:
        errors.append('Retain4 B planning groups with R1 residuals and6 unstarted C axes')
    expected_status=['bounded-parent-contract-delivered-residuals-open']+['planned-not-started']*9
    for n,r in enumerate(plan):
        for field in ('id','part_family','title','candidate_scope_not_certified','expected_deliverable','static_exit_criterion','dependencies_and_uncertainty'):
            if not isinstance(r.get(field),str) or not r[field].strip():errors.append('Remaining work missing substantive field: '+r.get('id','?')+'.'+field)
        if r.get('status')!=expected_status[min(n,9)] or r.get('runtime_status')!='not-executed' or r.get('counts_are_sessions_or_completion_percent')!='false':
            errors.append('Remaining work overclaim: '+r.get('id','?'))
    if [r.get('part_family') for r in plan]!=['7B']*4+['7C']*6:errors.append('Remaining work family/order')
    if len(depth)!=6 or sum(r.get('prior_full_local_csharp_declared')=='true' for r in depth)!=5 or sum(r.get('b14_full_local_body_and_xaml')=='true' for r in depth)!=4 or sum(r.get('remaining_old_category_after_b14')=='true' for r in depth)!=2:
        errors.append('Six old categories/five prior full bodies/four local upgrades/two remaining, not unread counts')
    return errors


def group_row_errors(previous,current):
    rows=lambda t:re.findall(r'^\| G-\d{2,3} \|.*$',t,re.M)
    return [] if len(rows(previous))==158 and rows(current)[:158]==rows(previous) else ['Historical G01–158 rows changed']


def witness_metadata_errors(w):
    out=[]
    for k in ('application_code_imported_or_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed'):
        if w.get(k) is not False:out.append('B14 false-only flag: '+k)
    for k in ('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k)) is not int or w[k]!=0:out.append('B14 integer-zero count: '+k)
    for k in ('default_aggregate_gate_not_assumed_resolved','supplied_sql_not_certified_deployed','progress_categories_not_wholly_unread_counts','local_expiry_helper_and_dto_not_claimed_missing','B_R1_residual_contracts_not_closed'):
        if w.get(k) is not True:out.append('B14 boundary: '+k)
    for k in ('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k)) is not int or w[k]!=24:out.append('B14 count: '+k)
    if w.get('phase')!='7B14-partial-static-audit':out.append('B14 witness phase')
    return out+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def plan_structure_errors(tests,new_ids,extensions):
    errors=[]
    expected=['finding-specific']*6+['historical-root-regression']*22+['cross-cutting-contract']*4+['documentary-scope-or-authorization-gate']*2
    if [r.get('plan_kind') for r in tests]!=expected:errors.append('B14 plan-kind/count/order')
    if any(r.get('status')!='not-executed' for r in tests):errors.append('B14 acceptance not executed')
    if len(new_ids)!=3 or len(set(new_ids))!=3:errors.append('B14 three distinct new roots')
    for n,fid in enumerate(new_ids,1):
        direct=[r for r in tests if r.get('plan_kind')=='finding-specific' and r.get('finding_ids')==fid]
        if len(direct)!=2:errors.append('B14 two direct plans: '+fid)
        if any(r.get('feature_ids')!=f'FE7B14-{n:02d}' or r.get('invariant_ids')!=f'INV7B14-{n:02d}' for r in direct):
            errors.append('B14 direct root/feature/invariant mapping: '+fid)
    historical=[r.get('finding_ids') for r in tests if r.get('plan_kind')=='historical-root-regression']
    if historical!=[r['finding_ids'] for r in extensions]:errors.append('B14 historical plan/manifest order')
    return errors


def validate_source(v,r,scope):
    if 'evidence' not in r:return
    if r['evidence']=='none-inventory-only':v.check(r['id'] in SENTINELS,'B14 undeclared no-source sentinel: '+r['id'])
    else:
        v.check(r['id'] not in SENTINELS,'B14 fabricated inventory evidence: '+r['id'])
        v.evidence(r['evidence'],r['id']);v.scoped_evidence(r['evidence'],scope,r['id']+' boundedB14',phase=7)


def extend_inventory_activity(v,report,prov,frozen291):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[291:];extensions=rows('evidence/historical-extensions-07B14.csv')
    ck(prov['historical_artifact_count']==387 and len(frozen291)==291,'B14 entry count')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY_CHECKOUT,'B14 actual entry checkout')
    ck(prov['erp_runtime_tests_executed']==0 and prov['sql_or_external_service_tests_executed']==0 and prov['application_remediation_performed'] is False and prov['phase8_authorized_or_started'] is False,'B14 execution/remediation boundary')
    identity=report['source_reference_validation']
    ck(identity['audited_application_reference']==v.HEAD and identity['reference_ancestor_of_checkout'] is True and identity['all_committed_net_delta_paths_under_docs_audit'] is True and report['original_project_hashes_matching']==827,'B14 source identity')
    ext=v.transition(frozen291,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    for e in registry_transition_errors(frozen291,current,extensions):ck(False,e)
    ck(len(current)==len({r['id'] for r in current})==294 and [r['id'] for r in new]==['P7-120','P7-121','P7-122'],'B14 registry/newIDs')
    v.distributions(new,{'Medium':3},{'confirmed':3},'boundedB14 only')
    for r in new:ck(r['type']=='implementation-defect' and r['status']=='open-not-remediated' and r['next_phase']=='8','B14 finding status/followup')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title']) for r in new],'B14 headings/registry')
    raw=(v.AUDIT/'findings.csv').read_bytes()
    ck(not raw.startswith(b'\xef\xbb\xbf') and raw.count(b'\r\n')==295 and b'\n' not in raw.replace(b'\r\n',b''),'B14 noBOM/CRLF registry')
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges']) for r in selected};inventory=rows('evidence/inventory.csv');paths={r['path'] for r in inventory}
    ck(len(selected)==len(scope)==21,'B14 selected count')
    for r in selected:
        ck(r['path'] in paths and r['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(r['focus']),'B14 scope: '+r['path'])
        v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    for n in REVIEWED_BODIES:
        for suffix in ('.xaml','.xaml.cs'):
            p='SmartAuditERP/Form_WPF/'+n+suffix
            ck(scope.get(p)==[(1,len(v.read(v.ROOT/p).splitlines()))],'B14 local body/XAML: '+p)
    known={r['id'] for r in current}|{f'H7B14-{n:02d}' for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B14.csv');tables[prefix]=data;v.sequential(data,prefix,count);v.related(data,known)
        for r in data:
            for k,value in r.items():ck(bool(value),'B14 incomplete cell: '+r['id']+'.'+k)
            validate_source(v,r,scope)
            if 'runtime_status' in r:ck(r['runtime_status']=='not-executed','B14 runtime overclaim')
    tests,features,invs,rc=[tables[k] for k in ('P7B14T-','FE7B14-','INV7B14-','RC7B14-')]
    tids={r['id'] for r in tests};fids={r['id'] for r in features};iids={r['id'] for r in invs}
    v.proposed_tests(tests,'7B14');v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(features+invs,tids,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invs,'invariant_ids')):
        for e in bidirectional_errors(pool,tests,field):ck(False,e)
    for e in feature_level_errors(features):ck(False,e)
    for pool,label in ((tests,'plans'),(features,'features'),(invs,'invariants')):v.covered(new,pool,'B14 '+label)
    for e in plan_structure_errors(tests,[r['id'] for r in new],extensions):ck(False,e)
    ck({r['finding_ids'] for r in extensions}==EXTENDED_FINDINGS and [r['finding_ids'] for r in features[3:25]]==[r['finding_ids'] for r in extensions],'B14 extension mapping')
    for r in extensions:ck(r['followup_policy']=='unchanged-during-partial7','B14 hidden replan')
    for r in rc:
        v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
        expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(r['feature_ids'].split(';'))]
        ck(r['acceptance_ids'].split(';')==expected and bool(expected),'B14 RC links')
    v.related(tables['Q7B14-'],{r['id'] for r in tables['H7B14-']},'handoff_ids')
    for r in tables['H7B14-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B14 handoff')
    for r in tables['Q7B14-']:ck(r['status']=='unanswered-no-secrets-requested','B14 question')
    for n,r in enumerate(tables['BK7B14-'],1):
        ck(r['prior_backlog_id']==f'BK7B13-{n:02d}' and r['original_backlog_id']==f'BK7-{n:02d}' and r['status']!='complete','B14 backlog ancestry')
    ck([r['status'] for r in tables['BK7B14-'][2:6]]==['not-started']*4,'B14 accidentally startsC')
    labelled=[(str(n),rows('review-scope.csv' if n==1 else f'review-scope-{n:02d}.csv')) for n in range(1,7)]+[('7A',rows('review-scope-07.csv'))]+[(f'7B{n}',rows(f'review-scope-07B{n}.csv')) for n in range(1,14)]+[('7B14',selected)]
    ck(rows('evidence/coverage-ledger-07B14.csv')==build_current_ledger(inventory,labelled,v.spans),'B14 ledger')
    candidates=rows('evidence/report-candidate-disposition-07B14.csv');screens=rows('evidence/report-screen-disposition-07B14.csv')
    ck(len(candidates)==98 and candidates==build_candidate_disposition(inventory,labelled),'B14 filename triage')
    ck(len(screens)==52 and screens==build_screen_disposition(inventory,labelled),'B14 screen triage');v.sequential(screens,'SC7B14-',52)
    before={r['path'] for _,s in labelled[:-1] for r in s};s=set(scope)
    ck((len(before),len(s&before),len(s-before),len(before|s),len(paths-(before|s)))==(390,19,2,392,435),'B14 union bookkeeping')
    depth=rows('evidence/report-depth-clarification-07B14.csv');plan=rows('evidence/remaining-workplan-07B14.csv')
    v.sequential(depth,'DEP7B14-',6);v.sequential(plan,'RW7B14-',10)
    ck(depth==depth_clarification(inventory,labelled,v.spans),'B14 depth clarification')
    for e in remaining_work_errors(plan,depth):ck(False,e)
    w,match=v.recompute('evidence/report-witnesses-07B14.json','tools/check_inventory_activity_witnesses.py')
    alg=w['illustrations'];lex=w['static_lexical_contract_checks'];v.sequential(alg,'ALG7B14-',24);v.sequential(lex,'ST7B14-',24);v.related(alg+lex,known)
    for e in witness_metadata_errors(w):ck(False,e)
    ck(w['errors']==[],'B14 witness has failed observations')
    for r in alg+lex:
        flag='illustration_assertions_passed' if r['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(r[flag] is True and r['source_application_executed'] is False and bool(r['limit']),'B14 witness overclaim');validate_source(v,r,scope)
    for r in w['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B14 lexical bounded read',phase=7)
    pats=[(PART_DOCS[0],r'^\| (EX7B14-\d{2}) \|',[r['id'] for r in extensions]),(PART_DOCS[1],r'^\| (FE7B14-\d{2}) —',[r['id'] for r in features]),(PART_DOCS[1],r'^\| (INV7B14-\d{2}) \|',[r['id'] for r in invs]),(PART_DOCS[1],r'^### (RC7B14-\d{2}) —',[r['id'] for r in rc]),(PART_DOCS[2],r'^\| (P7B14T-\d{2}) \|',[r['id'] for r in tests]),(PART_DOCS[3],r'^\| (DEP7B14-\d{2}) \|',[r['id'] for r in depth]),(PART_DOCS[3],r'^\| (RW7B14-\d{2}) \|',[r['id'] for r in plan]),('IMPROVEMENTS.md',r'^\| (G-\d{2,3}) \|',[f'G-{n:02d}' for n in range(1,165)])]
    for file,pat,expected in pats:ck(re.findall(pat,v.read(v.AUDIT/file),re.M)==expected,'B14 Markdown IDs: '+file)
    pending=False;src=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B14.json').resolve() and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B14 broken link: '+name+':'+m[1])
        for m in src.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,name,phase=7)
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    for name in SHARED_DOCS:
        ck(all(t in v.read(v.AUDIT/name) for t in ('PHASE-07B14.md','PHASE-07-REMAINING-07B14.md','7B15','غير مأذونة','461ceaf','10ba215')),'B14 current index boundary: '+name)
    tools=['check_inventory_activity_witnesses.py','validate_inventory_activity_part.py','test_inventory_activity_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B14 syntax: '+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_inventory_activity_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1]) if m else None;passed=run.returncode==0 and count==28;ck(passed,'B14 self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_inventory_activity_audit_validator.py']=dict(tests_reported=count,expected_tests=28,process_exit_code=run.returncode,result='passed' if passed else 'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools
    report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n) for n in ['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B14-294-plus-frozen-history-not-runtime-certification',phase_7_delivery='7A+'+'+'.join('7B'+str(n) for n in range(1,15))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B15-proposed-R2-with-B_R1-residuals-in-four-planning-groups-not-guaranteed-sessions','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=122,phase_7B14=3,total_open_not_remediated=294,severity=dict(collections.Counter(r['severity'] for r in current)),certainty=dict(collections.Counter(r['certainty'] for r in current)))
    report['scope_files'].update({SCOPE_FILE:21,'phase_7B13_union_frozen':390,'phase_7B14_overlap_with_prior_union':19,'phase_7B14_new_paths':2,'unique_union_not_line_or_execution_coverage':392,'inventory_only_no_selected_scope':435})
    report['phase_7B13_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=387,historical_check_record_overwritten=False,genuine_b13_check_sha256_unchanged=B13_CHECK_SHA,partial7B14_append_only_evidence_extensions_without_reclassification=ext,next_phase_followups_preserved_for_all291=True,next_phase_replans_during_partial7={})
    report['phase_7B14_remaining_work_not_completion_percentage']=dict(old_disposition_category_at_entry=6,of_those_prior_full_local_CSharp_bodies=5,b14_local_body_and_xaml_contract_upgrades=4,of_four_upgrades_prior_full_CSharp=3,newly_full_local_CSharp_among_four=1,remaining_old_category=2,B_planning_groups_retained_with_R1_residuals=4,C_axes_not_started=6,counts_are_guaranteed_sessions_or_completion_percent=False)
    report['evidence_rows'].update(dict(phase_7B14_feature_rows_not_completed_features=31,phase_7B14_invariants_not_passed_tests=31,phase_7B14_reconciliation_contracts_not_financial_acceptance=6,phase_7B14_unexecuted_acceptance_or_gate_plans=34,phase_7B14_historical_extensions_not_new_findings=22,phase_7B14_unresolved_handoffs=6,phase_7B14_unanswered_questions=6,phase_7B14_backlog_groups=10,phase_7B14_filename_candidates_not_features=98,phase_7B14_screen_candidates_not_features=52,phase_7B14_illustrations_not_erp_tests=24,phase_7B14_lexical_checks_not_erp_tests=24,phase_7B14_witness_recomputed_matches_saved=match))
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only documentary B14:387 protected artifacts,291 immutable cores/ALLnext_phase/exact evidence prefixes plus22 declared tails; exactG01..158. Source10ba/original827 differs from completed B13push/entry461ceaf and genuine B13stdout checkout1182. Same-branch entry fast-forward only after392 exact workspace/remote document comparisons, no source change or new reference. Historical helpers including B13 get OWN exact frozen rows/rawCRLF bytes/indextexts IN MEMORY, no protected edits/global pathlib patch/disk overlay/rebaseline/archive rewrite. Three new Medium local defects: unavailable operation-type choices, write-only layout persistence, LastProcess positive-store argument defeated by all-store default; not repeat TOP1/header-direction/ignored-client/stale-item/unit roots. Four local body/XAML upgrades include three CSharp bodies already full inB2 and only detailed newly full; six old categories included five prior full bodies and now leave two, not all report contracts. B-R1 local delivery retains residual caller/child/template/schema/ACL boundaries in four planning groups;7B15/R2 proposed, six C axes unstarted. Local Inventory.ItemsExpirationStock, InventoryData and Report exist; comments/imports are not missing-dependency proof. Supplied UDF retains branch/store/item/date grain and positive-stock only, independent DATEDIFF boundaries, row count not certified distinct-item meaning. Cost-unit P7-041 locally evidenced via val/val1 writer while valuation policy P4-007 remains potential; no assumed P4-008/P4-020/P4-030 or P3-022 fix. CSV syntax P7-048 is separate from potential consumer formulas P7-049 and potential finalize timing P7-108; using blocks and WriteAllText before launch are positive counterevidence. GlobalID routing in inventory remains positive, live combo dispatch is snapshot root P7-045, not indiscriminate identity loss. Apply/new/disabled/Closing/using and valid-empty UpdateSummary do not prove deployed ACL, no leak/index/latency measurement or financial acceptance. Additive B10 arithmetic erratum10vs120 retained without archive rewrite.24 manual+24 lexical+28 new synthetic checker cases are documentary;34 acceptance/gate plans not-executed.7B/7 partial,7C unstarted,8 unauthorized. No application import/build/C#/SQL/WPF/REPX/Office/COM/formula/HTML interpreter/provider/device/printer/actual business export/shell, remediation, real data/secrets or operational measurements.'
