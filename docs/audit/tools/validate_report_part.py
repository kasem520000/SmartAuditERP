#!/usr/bin/env python3
"""Additive PARTIAL7B1 audit-document validation, not ERP acceptance.

Only imported by the sibling validator for the current7B1 view. Historical7A
is validated FIRST against its frozen200-row registry, unchanged scopes/matrices
and saved witnesses. This module validates the transition to the current223,
selected new evidence, cross-links, range ledger, documentation and the NEW
synthetic witnesses. No application import/build/SQL/network/binary/device calls.
"""
from __future__ import annotations
import collections
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

SCOPE_FILE = 'review-scope-07B1.csv'
CURRENT_DOCS = ('PHASE-07B1.md','REPORTS-PRINTING-07B1.md','VALIDATION-07B1.md',
                'README.md','PLAN.md','IMPROVEMENTS.md')
B_PART_DOCS = set(CURRENT_DOCS[:3])
SENTINELS = {'FE7B-32','H7B-07','H7B-08'}
EXTENDED_FINDINGS = {'P1-004','P1-011','P1-013','P2-001','P2-010','P3-023','P4-011'}


def merge_ranges(ranges):
    """Normalize closed integer spans for bookkeeping only, NOT read certification."""
    out = []
    for a,b in sorted(ranges):
        if not (isinstance(a,int) and isinstance(b,int) and 1<=a<=b):
            raise ValueError('Invalid closed source span')
        if out and a<=out[-1][1]+1:
            out[-1]=(out[-1][0],max(out[-1][1],b))
        else:
            out.append((a,b))
    return out


def format_ranges(ranges):
    return ';'.join(f'{a}-{b}' for a,b in ranges) or 'none'


def remaining_ranges(total, merged):
    """Text complement; a binary/empty artifact is NOT inferred from this function."""
    if total < 0:
        raise ValueError('Negative line count')
    cursor,gaps=1,[]
    for a,b in merged:
        if not 1<=a<=b<=total:
            raise ValueError('Declared span outside inventory line count')
        if cursor<a:
            gaps.append((cursor,a-1))
        cursor=b+1
    if cursor<=total:
        gaps.append((cursor,total))
    return gaps


def build_ledger(inventory, labelled_scopes, parse_ranges):
    """One row per ORIGINAL path, in inventory order. No source/file/Git read here.

    labelled_scopes is [(label,[{path,ranges,review_state,...}]),...]. Including
    a historical range preserves historical metadata, never upgrades its depth.
    """
    declared, phases, states, a_spelling, b_spelling={},{},{},{},{}
    for label,scope in labelled_scopes:
        for row in scope:
            p=row['path']
            declared.setdefault(p,[]).extend(parse_ranges(row['ranges']))
            phases.setdefault(p,[]).append(label)
            states.setdefault(p,[]).append(label+':'+row['review_state'])
            if label=='7A': a_spelling[p]=row['ranges']
            if label=='7B1': b_spelling[p]=row['ranges']
    ledger=[]
    for original in inventory:
        p=original['path']
        merged=merge_ranges(declared.get(p,[]))
        total=int(original['lines']) if original['lines'] else None
        if total is None:
            remaining,state='not-a-text-line-model','binary-metadata-not-executed'
        elif not total:
            if merged:
                raise ValueError('Span declared on zero-line artifact')
            remaining,state='none-zero-lines','zero-line-artifact'
        else:
            gaps=remaining_ranges(total,merged)
            remaining=format_ranges(gaps)
            state='partial-or-no-declared-ranges' if gaps else 'all-lines-in-declared-ranges-not-semantic-certification'
        if original['kind']=='generated-artifact':
            bucket='8-artifact-provenance-only-not-authorized'
            work='أصل مخرجات متتبعة؛ لا تشغيل أو ثقة من وجودها. تحقق توريد وبناء مصدر مستقل في8 بإذن لاحق.'
        elif p in b_spelling:
            bucket='7B1-selected-slices-not-whole-file-followup-pending'
            work='نطاق7B1 محدد فقط؛ تتبع بقية القدرات والمتصلين والحقول والمقاطع في7B2/7C أو استبعاد مسند. لا تعد مراجعة الملف كله أو قبولاً.'
        elif re.search(r'(rpt|report|print|barcode|number2arabic)',Path(p).name,re.I):
            bucket='7B2-report-print-candidate-by-name-only'
            work='مرشح بالاسم فقط: تحديد feature/query/source/filter/total/output/ACL أو استبعاد مسند في7B2؛ ليست قراءة تنفيذ جديدة.'
        else:
            bucket='7C-source-ui-resource-candidate-by-name-only'
            work='ترشيح مسار فقط لاستكمال قدرات7C وعمر الموارد/الإتاحة/الثقافات/الأداء أو استبعاد مسند؛ آثار المراحل السابقة لا تثبت شمول القراءة.'
        ledger.append(dict(path=p,inventory_kind=original['kind'],inventory_lines=original['lines'] or 'not-text',
            path_scope_state='selected-path-not-whole-file-certified' if merged else 'inventory-only-no-selected-scope',
            selected_phase_ids=';'.join(phases.get(p,[])) or 'none',
            declared_review_states=';'.join(states.get(p,[])) or 'inventory-only',
            declared_range_union_not_reading_certification=format_ranges(merged),
            unselected_text_ranges=remaining,line_range_state=state,
            phase7A_ranges=a_spelling.get(p,'none'),phase7B1_ranges=b_spelling.get(p,'none'),
            continuation_bucket=bucket,next_scope_work=work,runtime_status='not-executed'))
    return ledger


def bidirectional_errors(pool, tests, field):
    """Pure cross-link check, returns diagnostics, never modifies data."""
    errors=[]
    for row in pool:
        expected=[t['id'] for t in tests if row['id'] in t[field].split(';')]
        if not expected or row['acceptance_ids'].split(';')!=expected:
            errors.append('Reverse acceptance mismatch: '+row['id'])
    return errors


def validate_source(v, row, scope):
    value=row.get('evidence')
    if value is None:
        return
    if value=='none-inventory-only':
        v.check(row['id'] in SENTINELS,'Undeclared no-source sentinel: '+row['id'])
    else:
        v.check(row['id'] not in SENTINELS,'Inventory-only boundary lost: '+row['id'])
        v.evidence(value,row['id'])
        v.scoped_evidence(value,scope,row['id']+' partial7B1',phase=7)


def extend_report(v, report, prov, frozen200):
    """Mutates only an in-memory JSON result, never audit/application files."""
    r=v.rows
    ck=v.check
    current=r('findings.csv')
    newly=current[200:]
    extensions=r('evidence/historical-extensions-07B1.csv')
    ck(len(frozen200)==200 and prov['registry_at_entry_snapshot']=='evidence/findings-through-07A.csv',
       '7B1 entry registry mismatch')
    ck(prov['registry_at_entry_sha256']=='d385df6808ccde05bdec5ddda517b75b9829dc63aea7e8affacd64a2ed392f05',
       'Delivered7A registry SHA mismatch')
    ck(prov['phase7A_entry_consistency']=={'original_hashes_matching':827,'findings':200,'phase_7_delivery':'7A-partial','errors':[],'erp_runtime_tests_executed':0},
       '7B1 entry metadata does not represent delivered partial7A')
    saved7=v.json.loads(v.read(v.AUDIT/'evidence/checks-07.json'))
    ck(saved7['findings']['total_open_not_remediated']==200 and saved7['phase_7_delivery']=='7A-partial'
       and saved7['validation']['errors']==[] and saved7['historical_artifact_sha256']==v.json.loads(v.read(v.AUDIT/'evidence/provenance-07.json'))['historical_artifact_sha256'],
       'Protected7A check record no longer represents its historical successful check')
    ext=v.transition(frozen200,current,7,EXTENDED_FINDINGS,preserve_followups=True)
    ck(len(current)==223 and len({x['id'] for x in current})==223,'Current7B1 registry count/uniqueness mismatch')
    ck([x['id'] for x in newly]==[f'P7-{n:03d}' for n in range(29,52)],'New7B1 findings IDs/order mismatch')
    v.distributions(newly,{'High':11,'Medium':12},{'confirmed':21,'potential':2},'partial7B1 only')
    ck([x['id'] for x in newly if x['certainty']=='potential']==['P7-032','P7-049'],'Unexpected7B1 conditional findings')
    for x in newly:
        ck(x['status']=='open-not-remediated' and x['next_phase']=='8' and bool(x['title']) and bool(x['type']),
           '7B1 classification/status/followup missing or overclaimed: '+x['id'])
    headers=v.re.findall(r'^### (P7-\d{3}) —',v.read(v.AUDIT/'PHASE-07B1.md'),v.re.M)
    ck(headers==[x['id'] for x in newly],'New7B1 report headings/registry mismatch')

    scopes=r(SCOPE_FILE)
    ck(len(scopes)==42 and len({x['path'] for x in scopes})==42,'7B1 selected scope count/duplicates mismatch')
    inventory=r('evidence/inventory.csv')
    paths={x['path'] for x in inventory}
    scope={x['path']:v.spans(x['ranges']) for x in scopes}
    for x in scopes:
        ck(x['path'] in paths,'7B1 scope outside original inventory: '+x['path'])
        ck(x['review_state']=='selected-static-source-slices-not-runtime-certified' and bool(x['focus']),
           '7B1 scope overclaims coverage or lacks focus: '+x['path'])
        v.source_ref(x['path'],x['ranges'],SCOPE_FILE)
    for x in newly:
        validate_source(v,x,scope)

    specifications=(
        ('acceptance-tests-07B1.csv','P7BT-',54),
        ('feature-implementation-matrix-07B1.csv','FE7B-',33),
        ('report-invariants-07B1.csv','INV7B-',20),
        ('report-reconciliation-07B1.csv','RC7B-',6),
        ('output-contracts-07B1.csv','OUT7B-',11),
        ('historical-extensions-07B1.csv','EX7B-',7),
        ('handoffs-07B1.csv','H7B-',8),
        ('questions-07B1.csv','Q7B-',8),
        ('continuation-backlog-07B1.csv','BK7B-',10),
    )
    tables={}
    known={x['id'] for x in current}|{f'H{n}-{i:02d}' for n,count in ((2,3),(3,4),(4,4),(5,4),(6,8),(7,8)) for i in range(1,count+1)}|{f'H7B-{i:02d}' for i in range(1,9)}
    for filename,prefix,count in specifications:
        data=r('evidence/'+filename)
        tables[prefix]=data
        v.sequential(data,prefix,count)
        v.related(data,known)
        for x in data:
            for k,value in x.items():
                ck(bool(value),f'Incomplete7B1 row: {x["id"]}.{k}')
            validate_source(v,x,scope)
            if 'runtime_status' in x:
                ck(x['runtime_status']=='not-executed','7B1 execution claim: '+x['id'])
    tests,features,invariants=tables['P7BT-'],tables['FE7B-'],tables['INV7B-']
    plans={x['id'] for x in tests}
    fe_ids={x['id'] for x in features}
    inv_ids={x['id'] for x in invariants}
    v.proposed_tests(tests,'7B1')
    v.related(tests,fe_ids,'feature_ids')
    v.related(tests,inv_ids,'invariant_ids')
    v.related(features+invariants,plans,'acceptance_ids')
    for pool,field in ((features,'feature_ids'),(invariants,'invariant_ids')):
        for err in bidirectional_errors(pool,tests,field): ck(False,err)
    for pool,label in ((tests,'acceptance'),(features,'feature matrix'),(invariants,'invariant')):
        v.covered(newly,pool,'partial7B1 '+label)
    for x in newly:
        direct=[t for t in tests if t['plan_kind']=='finding-specific' and x['id'] in t['finding_ids'].split(';')]
        ck(len(direct)==2,'7B1 finding lacks exactly two direct unexecuted plans: '+x['id'])
    ck([t['plan_kind'] for t in tests]==['finding-specific']*46+['cross-cutting-regression']*8,
       '7B1 direct/cross-cutting plan distinction mismatch')
    ck([x['finding_ids'] for x in features[:23]]==[x['id'] for x in newly],'7B1 primary feature/finding mapping mismatch')
    for x in features:
        ck(x['implementation_status'] in {'implemented-with-observed-defects','conditional-policy-or-external-contract','deferred-7B2-not-reviewed'},'7B1 implementation overclaim: '+x['id'])
    ck(next(x for x in features if x['id']=='FE7B-32')['coverage_level']=='inventory-only-not-implementation-reviewed',
       '7B2 inventory is being counted as implemented coverage')
    v.related(tables['Q7B-'],{x['id'] for x in tables['H7B-']},'handoff_ids')
    for x in tables['H7B-']:
        ck(x['status']=='external-contract-or-policy-unresolved-not-absence-proof','7B1 unresolved contract reclassified: '+x['id'])
    for x in tables['Q7B-']:
        ck(x['status']=='unanswered-no-secrets-requested','7B1 question falsely resolved: '+x['id'])
    for prefix in ('RC7B-','OUT7B-'):
        v.related(tables[prefix],fe_ids,'feature_ids')
        v.related(tables[prefix],plans,'acceptance_ids')
        for x in tables[prefix]:
            expected=[t['id'] for t in tests if set(t['feature_ids'].split(';'))&set(x['feature_ids'].split(';'))]
            ck(x['acceptance_ids'].split(';')==expected and bool(expected),'7B1 projection/matrix acceptance mismatch: '+x['id'])
    ck({x['finding_ids'] for x in extensions}==EXTENDED_FINDINGS,'7B1 extension manifest mismatch')
    for x in extensions:
        old=next(t for t in frozen200 if t['id']==x['finding_ids'])
        new=next(t for t in current if t['id']==x['finding_ids'])
        ck(new['evidence']==old['evidence']+';'+x['evidence'] and new['next_phase']==old['next_phase'] and x['followup_policy']=='unchanged-during-partial7',
           '7B1 append-only evidence/followup mismatch: '+x['id'])
    for i,x in enumerate(tables['BK7B-'],1):
        ck(x['prior_backlog_id']==f'BK7-{i:02d}' and x['part'] in {'7B2','7C','7B2/7C'} and x['status']!='complete',
           '7B1 continuation collapsed/completed accidentally: '+x['id'])
    ck([x['status'] for x in tables['BK7B-'][2:6]]==['not-started']*4,'7C accidentally marked started in backlog')

    labelled=[(str(i),r('review-scope.csv' if i==1 else f'review-scope-{i:02d}.csv')) for i in range(1,7)]
    labelled += [('7A',r('review-scope-07.csv')),('7B1',scopes)]
    expected_ledger=build_ledger(inventory,labelled,v.spans)
    ledger=r('evidence/coverage-ledger-07B1.csv')
    ck(ledger==expected_ledger,'7B1 coverage ledger differs from scope/range bookkeeping (not semantic certification)')
    prior={x['path'] for _,items in labelled[:-1] for x in items}
    selected=set(scope)
    union=prior|selected
    ck(len(prior)==266,'7A selected-path union changed')
    # Counts below are fixed delivery assertions, not a measured completeness ratio.
    ck(len(selected&prior)==20 and len(selected-prior)==22 and len(union)==288,
       '7B1 overlap/new/union counts mismatch')
    ck(sum(x['path_scope_state']=='inventory-only-no-selected-scope' for x in ledger)==539,
       '7B1 inventory-only count mismatch')

    witness,match=v.recompute('evidence/report-witnesses-07B1.json','tools/check_report_witnesses.py')
    algebra=witness['illustrations']
    lexical=witness['static_lexical_contract_checks']
    v.sequential(algebra,'ALG7B-',19)
    v.sequential(lexical,'ST7B-',11)
    ck(witness['phase']=='7B1-partial-static-audit' and witness['illustration_count']==19 and witness['static_lexical_contract_check_count']==11
       and witness['application_remediation_performed'] is False and witness['real_business_or_secret_data_used'] is False
       and witness['spreadsheet_or_formula_interpreter_executed'] is False,
       '7B1 witness metadata overclaims application/active-content execution')
    v.related(algebra+lexical,known)
    for x in algebra+lexical:
        flag='illustration_assertions_passed' if x['id'].startswith('ALG') else 'documented_text_observation_matches'
        ck(x['source_application_executed'] is False and bool(x['limit']) and x[flag] is True,
           '7B1 illustration/text check claims application execution: '+x['id'])
        validate_source(v,x,scope)
    for x in witness['bounded_source_reads_not_semantic_coverage']:
        v.scoped_evidence(f'{x["path"]}:{x["start"]}-{x["end"]}',scope,'7B1 bounded lexical read',phase=7)

    for filename,pattern,expected in (
        ('VALIDATION-07B1.md',r'^\| (P7BT-\d{2}) \|',[x['id'] for x in tests]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (FE7B-\d{2}) —',[x['id'] for x in features]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (INV7B-\d{2}) \|',[x['id'] for x in invariants]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (RC7B-\d{2}) —',[x['id'] for x in tables['RC7B-']]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (OUT7B-\d{2}) —',[x['id'] for x in tables['OUT7B-']]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (H7B-\d{2}) —',[x['id'] for x in tables['H7B-']]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (Q7B-\d{2}) \|',[x['id'] for x in tables['Q7B-']]),
        ('REPORTS-PRINTING-07B1.md',r'^\| (BK7B-\d{2}) \|',[x['id'] for x in tables['BK7B-']]),
        ('PHASE-07B1.md',r'^\| (EX7B-\d{2}) \|',[x['id'] for x in extensions]),
        ('IMPROVEMENTS.md',r'^\| (G-\d{2}) \|',[f'G-{i:02d}' for i in range(1,81)]),
    ):
        ck(v.re.findall(pattern,v.read(v.AUDIT/filename),v.re.M)==expected,'7B1 Markdown table IDs/order mismatch: '+filename+':'+pattern)
    source_pattern=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for filename in CURRENT_DOCS:
        doc=v.AUDIT/filename
        content=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',content):
            parsed=urlsplit(m[1])
            if parsed.scheme or m[1].startswith('#'): continue
            v.LINK_COUNT+=1
            ck((doc.parent/unquote(parsed.path)).resolve().exists(),'Broken current local link in '+filename+':'+m[1])
        for m in source_pattern.finditer(content):
            v.source_ref(m[1],m[2],filename)
            if filename in B_PART_DOCS:
                v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}' for a,b in v.spans(m[2])),scope,filename,phase=7)
        for m in re.findall(r'\bP7BT-\d{2}\b',content):
            ck(m in plans,'Unknown7B1 acceptance plan in '+filename+':'+m)
        for pattern,ids in ((r'\bFE7B-\d{2}\b',fe_ids),(r'\bINV7B-\d{2}\b',inv_ids)):
            for m in re.findall(pattern,content): ck(m in ids,'Unknown7B1 matrix ID in '+filename+':'+m)
    extra_tools=['check_report_witnesses.py','validate_report_part.py','test_report_audit_validator.py']
    for filename in extra_tools:
        try: v.ast.parse(v.read(v.AUDIT/'tools'/filename),filename=filename)
        except SyntaxError as ex: ck(False,'7B1 audit tool syntax error: '+filename+': '+str(ex))
    report['validation']['audit_only_python_tools_syntax_checked']+=extra_tools
    report['phase_7_delivery']='7A+7B1-partial-not-complete7B-or7'
    report['phase_7_remaining_parts']=['7B2-not-started','7C-not-started']
    report['registry_used']='findings.csv'
    report['findings'].update(phase_7=51,phase_7A=28,phase_7B1=23,total_open_not_remediated=223,
       severity=dict(collections.Counter(x['severity'] for x in current)),certainty=dict(collections.Counter(x['certainty'] for x in current)))
    report['scope_files'].update({SCOPE_FILE:42,'phase_7A_union_frozen':266,'phase_7B1_overlap_with_prior_union':len(selected&prior),
       'phase_7B1_new_paths':len(selected-prior),'inventory_only_no_selected_scope':len(paths-union),'unique_union_not_line_or_execution_coverage':len(union)})
    report['phase_7A_historical_evidence']={'frozen_registry':prov['registry_at_entry_snapshot'],
       'frozen_registry_sha256_matches':v.sha(v.AUDIT/prov['registry_at_entry_snapshot'])==prov['registry_at_entry_sha256'],
       'earlier_report_evidence_artifacts_hash_checked':86,'historical_check_record_overwritten':False,
       'partial7B1_append_only_evidence_extensions_without_reclassification':ext,
       'next_phase_followups_preserved_for_all200':True,'phase7A_validation_inputs_frozen_not_shared_indexes':True,
       'limit':'Historical7A is recomputed with current checker against frozen inputs, not represented as a byte-identical re-execution of original checks-07. Shared indexes excluded from historical view.'}
    report['historical_artifact_sha256']=prov['historical_artifact_sha256']
    report['evidence_rows'].update({
       'phase_7B1_feature_screen_implementation_test_rows_not_completed_features':len(features),
       'phase_7B1_invariants_not_passed_tests':len(invariants),
       'phase_7B1_selected_report_reconciliation_rows_not_gl_acceptance':len(tables['RC7B-']),
       'phase_7B1_output_contract_rows_not_channel_acceptance':len(tables['OUT7B-']),
       'phase_7B1_unexecuted_acceptance_plans':len(tests),
       'phase_7B1_historical_evidence_extensions_not_new_findings':len(extensions),
       'phase_7B1_handoffs_not_absence_proof':8,'phase_7B1_unanswered_policy_contract_questions':8,
       'phase_7B1_continuation_groups_not_completed':10,'phase_7B1_coverage_ledger_original_paths':len(ledger),
       'phase_7B1_independent_illustrations_not_erp_tests':len(algebra),
       'phase_7B1_bounded_static_lexical_checks_not_application_tests':len(lexical),
       'phase_7B1_illustrations_and_text_checks_recomputed_match_saved':match})
    report['validation']['limit']+=' 7B1 extends only documentary/range/cross-link checks; unresolved policies and unreviewed7B2/7C remain.'
