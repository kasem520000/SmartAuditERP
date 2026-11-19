#!/usr/bin/env python3
"""7B21/R4e bounded amountword/currency documentary checks, NEVER ERP.

Protect583 artifacts/310 EXACT rows/ALLnext_phase/evidence/raw311CRLF prefix/
G195/827 originals and three entry freezes. B20 OWN310/raw311CRLF/indexes
in memory; ALL32 protected cases in an explicit historical B20-preset child.
Earlier B19/36 and B18/28 children remain unchanged. Current B21 default and
entrypoint tested independently. No protected edits/skips/global Path or
subprocess patch/disk overlay/rebaseline/archive rewrite/application import/
C#/VB/.NET/WPF/SQL/provider/SDK/DTO/ToDataTable/REPX/printer/scanner/business
execution, remediation, operational measurement or acceptance. Numeric local
currency cases are NOT an external enum or approved precision/sign/zero policy.
12 AR/2 EN qualified tokens and24 slice paths are not the whole callgraph or a
capability census. 7B/7 partial; R4f/B22 proposed;7C unstarted;8 unauthorized.
"""
from __future__ import annotations
from contextlib import contextmanager
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
from validate_financial_report_part import historical_b1_inputs,bidirectional_errors
from validate_statement_contract_part import arithmetic_erratum_errors
from validate_barcode_contract_part import expanded_source_evidence,historical_record_errors as historical25_errors

ENTRY='c2c895d0df0e4f106c4e5c2853219aa04303e002'
SNAPSHOT='evidence/findings-through-07B20.csv';SNAPSHOT_SHA='18b353c138536a98b3aa426bf2e03662df6133d3acccb034232918ed4dcb24d0'
SHARED_SNAPSHOT='evidence/shared-indexes-through-07B20.json';SHARED_SHA='2e5fdc450260f88b69b3172161237681fd7be0d58f45ae7bd7cc7ae76c4f3565'
PROVENANCE_SHA='4ca4356932a6c1689e3af6558b545697d6e35f4a7d491baf736f88ca2324a175'
B20_CHECK_SHA='93667de46adad6443573ac1822db56440678a86d28ee6fe26793e880bd57f766'
WITNESS_SHA='2129f522533abbbea9e455ebdd3a61d047f02f24bffe7448d1e800d140e99b42'
HISTORICAL_RUN_SHA='5ea5719515ba74f4ac7e3a2f7301cf66ed3a399dc9f5748344393d0797888279' # Actual26 OWN captures; capture-time tools recorded, no archive regeneration.
SCOPE_FILE='review-scope-07B21.csv';DOCUMENTARY='none-documentary-metadata'
PART_DOCS=('PHASE-07B21.md','AMOUNTWORD-CONTRACTS-07B21.md','VALIDATION-07B21.md','PHASE-07-REMAINING-07B21.md')
SHARED_DOCS=('README.md','PLAN.md','IMPROVEMENTS.md')
NEW_IDS=['P7-139','P7-140','P7-141']
TABLE_SPECS=(('amountword-callers','WC7B21-',12),('currency-branches','CM7B21-',10),('feature-implementation-matrix','FE7B21-',18),
 ('report-invariants','INV7B21-',18),('acceptance-tests','P7B21T-',36),('report-reconciliation','RC7B21-',6),('root-adjudication','AD7B21-',10),
 ('residual-disposition','RS7B21-',14),('split-register','SP7B21-',3),('handoffs','H7B21-',6),('questions','Q7B21-',6),('remaining-workplan','RW7B21-',10),('continuation-backlog','BK7B21-',10))
SENTINELS={f'{prefix}{n:02d}'for prefix,nums in(('FE7B21-',range(16,19)),('INV7B21-',range(16,19)),('P7B21T-',range(31,37)),
 ('RC7B21-',(6,)),('AD7B21-',(10,)),('RS7B21-',range(1,15)),('H7B21-',range(1,7)),('Q7B21-',range(1,7)))for n in nums}
CALLER_SHAPES=(
 ('Print.InvoiceItems','formatted-Net','explicit-Inv.Currency'),
 ('Print.Items-when-InvoiceItems-empty','raw-Inv.Net','explicit-Inv.Currency'),
 ('frmAccountBalance','literal-zero-selector-text','default-Currency.SAR'),
 ('frmAccountsStatement','absolute-debit-credit-difference','default-Currency.SAR'),
 ('frmCostCenterBalance','selected-positive-balance-text','default-Currency.SAR'),
 ('frmEmpSalaryAddSub','txtVal.Text','default-Currency.SAR'),
 ('frmSalaryPay','read-only-local-txtNet.Text','default-Currency.SAR'),
 ('frmSandD','editable-local-txtVal.Text','explicit-SettingGeneral-key13'),
 ('frmSandQAndroid','editable-local-txtVal.Text','explicit-SettingGeneral-key13'),
 ('frmSandQD','txtVal.Text-whitespace-to0','explicit-SettingGeneral-key13'),
 ('frmSandSD','txtVal.Text-empty-to0','explicit-SettingGeneral-key13'),
 ('frmSandVAT','txtNetVal.Text-not-gross-BondVal','explicit-SettingGeneral-key13'))


def row_sha(row):return hashlib.sha256(json.dumps(row,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()


@contextmanager
def historical_b20_inputs(v,frozen310,texts,raw):
    """Only exact OWN registry reads plus the existing three-text adapter.

    The Path subclass belongs to this v.AUDIT instance only: pathlib.Path and
    the real filesystem are never patched, written or overlaid.
    """
    if len(frozen310)!=310 or len({r.get('id')for r in frozen310})!=310:raise ValueError('Exactly310 distinct B20 OWN rows required')
    if set(texts)!=set(SHARED_DOCS)or any(not isinstance(t,str)for t in texts.values()):raise ValueError('Exactly three frozen shared texts required')
    if type(raw)is not bytes or raw.startswith(b'\xef\xbb\xbf'):raise ValueError('Exact noBOM bytes required')
    try:parsed=list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))
    except(UnicodeError,csv.Error)as e:raise ValueError('Malformed310 frozen registry')from e
    if(parsed!=frozen310 or raw.count(b'\r\n')!=311 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n'))):raise ValueError('310 rows/raw311CRLF disagree')
    original=v.AUDIT;target=(original/'findings.csv').resolve()
    class FrozenRegistryPath(type(original)):
        def read_bytes(self):return raw if self.resolve()==target else super().read_bytes()
    try:
        v.AUDIT=FrozenRegistryPath(original)
        with historical_b1_inputs(v,frozen310,texts):yield
    finally:v.AUDIT=original


class HistoricalB20Subprocess:
    """Redirect only the exact protected B20-test argv, preserving all kwargs."""
    def __init__(self,backend,python,tool_dir):
        self.backend=backend;self.expected=[python,'-B',str(tool_dir/'test_barcode_contract_audit_validator.py')]
        self.actual=[python,'-B',str(tool_dir/'run_historical_barcode_tests_07B21.py'),'--through-part','B20']
    def __getattr__(self,name):return getattr(self.backend,name)
    def run(self,args,*pos,**kwargs):return self.backend.run(self.actual if args==self.expected else args,*pos,**kwargs)


class HistoricalB20ValidatorView:
    def __init__(self,target):
        object.__setattr__(self,'_target',target);object.__setattr__(self,'_subprocess',HistoricalB20Subprocess(target.subprocess,target.sys.executable,target.AUDIT/'tools'))
    def __getattr__(self,name):return self._subprocess if name=='subprocess'else getattr(self._target,name)
    def __setattr__(self,name,value):setattr(self._target,name,value)


@contextmanager
def historical_b20_validation(v,report,prior,prov,frozen310):
    """The real protected B20 extension still runs; inputs/cutoff are explicit."""
    ck=v.check
    for name,digest in(('evidence/provenance-07B21.json',PROVENANCE_SHA),(SNAPSHOT,SNAPSHOT_SHA),(SHARED_SNAPSHOT,SHARED_SHA),('evidence/checks-07B20.json',B20_CHECK_SHA)):
        ck(v.sha(v.AUDIT/name)==digest,'B21 immutable entry:'+name)
    ck(prov['historical_artifact_count']==583 and len(frozen310)==310,'B21 entry583/310')
    ck(prov['registry_at_entry_snapshot']==SNAPSHOT and prov['registry_at_entry_sha256']==SNAPSHOT_SHA and prov['shared_indexes_at_entry']==SHARED_SNAPSHOT and prov['shared_indexes_at_entry_sha256']==SHARED_SHA,'B21 frozen entry names/hashes')
    ck(all(prov['historical_artifact_sha256'].get(n)==h for n,h in prior['historical_artifact_sha256'].items()),'B21 protected553-to583 continuity')
    old=v.json.loads(v.read(v.AUDIT/'evidence/checks-07B20.json'));suites=old['validation']['audit_only_checker_self_tests_executed_not_erp_tests']
    ck(old['checkout_head']=='ac20e3104f84fefbc62779e22d2c9b9621802340'and old['findings']['total_open_not_remediated']==310 and old['validation']['errors']==[]and old['original_project_hashes_matching']==827 and old['validation']['current_output_record_pending_first_write_not_placeholder']is False,'B21 genuine B20 stdout, not delivered c2c895d HEAD')
    ck(len(suites)==21 and sum(r['tests_reported']for r in suites.values())==530 and old['historical_artifact_sha256']==prior['historical_artifact_sha256'],'B21 archived B20 actual documentary result')
    ck(prov['checkout_head_at_entry']==prov['remote_current_branch_tip_observed_at_entry']==ENTRY and prov['genuine_B20_check_sha256']==B20_CHECK_SHA and prov['genuine_B20_check_record_checkout']==old['checkout_head'],'B21 delivered pushed B20 entry identity')
    ck(prov['phase7B20_entry_consistency']==dict(original_hashes_matching=827,findings=310,audit_file_count=588,documentary_cases=530,self_test_suites=21,errors=[],erp_runtime_tests_executed=0),'B21 completed B20 entry counts')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files'];view=HistoricalB20ValidatorView(v)
    with historical_b20_inputs(view,frozen310,texts,(v.AUDIT/SNAPSHOT).read_bytes()):yield view
    record=report['validation']['audit_only_checker_self_tests_executed_not_erp_tests']['test_barcode_contract_audit_validator.py']
    record.update(historical_parser_cutoff='B20-not-current-B21-default',all_original_cases_executed_unmodified=True,dedicated_child_launcher='tools/run_historical_barcode_tests_07B21.py',actual_subprocess_argv=view.subprocess.actual,no_test_skips_or_global_subprocess_or_path_patch=True)
    report.update(registry_used=SNAPSHOT,validation_scope='historical-through7B20-310-not-current-state',
        phase_7B20_historical_input_mode='OWN310-exact311CRLF-bytes-exact-indexes-in-memory-and-explicit-historical-B20-test-child',
        phase_7B20_adapter_context=dict(entry_provenance='evidence/provenance-07B21.json',adapter_protected_artifacts_checked=583,current_registry_and_shared_indexes_not_inputs=True,archived_stdout_not_rewritten_after_push=True,B20_parser_assertions_are_historical_preset_not_current_default=True))


def registry_preservation_errors(previous,current,raw,frozen):
    errors=[]
    if len(previous)!=310 or current[:310]!=previous:errors.append('B21 all310 exact fields/ALLnext_phase/evidence')
    if len(current)!=313 or[r.get('id')for r in current[310:]]!=NEW_IDS:errors.append('B21 only appended139..141')
    if(type(raw)is not bytes or type(frozen)is not bytes or not raw.startswith(frozen)or raw.startswith(b'\xef\xbb\xbf')or raw.count(b'\r\n')!=314 or not raw.endswith(b'\r\n')or any(x in raw.replace(b'\r\n',b'')for x in(b'\r',b'\n'))):errors.append('B21 exact310 raw prefix/314CRLF/noBOM')
    else:
        try:
            if list(csv.DictReader(io.StringIO(raw.decode('utf-8'),newline='')))!=current:errors.append('B21 raw/rows mismatch')
        except(UnicodeError,csv.Error):errors.append('B21 malformed registry')
    return errors


def group_row_errors(previous,current):
    rows=lambda s:re.findall(r'^\| G-\d{2,3} \|.*$',s,re.M);old,new=rows(previous),rows(current)
    if len(old)!=195 or new[:195]!=old:return ['B21 G01..195 exact prior rows']
    if re.findall(r'^\| (G-\d{2,3}) \|',current,re.M)!=[f'G-{i:02d}'for i in range(1,201)]:return ['B21 G196..200 only, exact order']
    return []


def caller_errors(current,literals):
    if len(current)!=12 or len(literals)!=12:return ['B21 exact12 selected qualified Arabic tokens required']
    errors=[];key=lambda r:(r['source_path'],str(r['call_line_start']),str(r['call_line_end']));lookup={key(r):r for r in literals}
    if len(lookup)!=12:errors.append('B21 distinct qualified token keys')
    if[tuple(r.get(k)for k in('caller','amount_source','word_currency_source'))for r in current]!=list(CALLER_SHAPES):errors.append('B21 named12 ordered input/currency boundaries')
    for r in current:
        actual=lookup.get(key(r))
        if actual is None or any(r.get(k)!=actual[k]for k in('call_text_sha256','inert_argument_expression')):errors.append('B21 literal line/argument/hash lineage')
        expected='SmartAuditERP/Class/Print.cs'if r.get('caller','').startswith('Print.')else'SmartAuditERP/Form_WPF/'+r.get('caller','')+'.xaml.cs'
        if r.get('source_path')!=expected:errors.append('B21 declared caller/source path')
        for k in('report_amount_field','parse_or_projection_boundary','owner_role','required_redacted_input','impact_if_unavailable','next_step','limit'):
            if not isinstance(r.get(k),str)or not r[k].strip():errors.append('B21 caller missing responsibility:'+k)
        if r.get('runtime_status')!='not-executed':errors.append('B21 caller runtime overclaim')
    if{key(r)for r in current}!=set(lookup):errors.append('B21 all12 token keys exactly once')
    return errors


def currency_branch_errors(data):
    errors=[];codes=['2','4','8','9','10','11','12','13','15','other']
    if len(data)!=10 or[r.get('numeric_local_branch_not_sdk_enum')for r in data]!=codes:return ['B21 ten ordered local numeric branches, not SDK enum']
    for r,code in zip(data,codes):
        code=int(code)if code!='other'else code
        ar=({2:'دولار',12:'جنيه مصري',13:'جنيه سوداني',15:'ليرة سورية'}.get(code,'ريال-default'),{2:'سنت',12:'قرش',13:'قرش'}.get(code,'هللة-default'))
        en={2:('Dollar','Cent'),4:('Dirham','Fil'),8:('Riyal','Halala'),9:('Pound','Penny'),10:('Euro','Cent'),11:('Yen','Sen')}.get(code,('Riyal-default','Halala-default'))
        if tuple(r.get(k)for k in('arabic_major_family','arabic_minor_family','english_major_family','english_minor_family'))!=ar+en:errors.append('B21 literal local branch families')
        if r.get('adjudication')!='retained035-no-new-finding'or r.get('finding_ids')!='P7-035'or r.get('runtime_status')!='not-executed'or not r.get('limit','').strip():errors.append('B21 currency not approved enum/new root/runtime')
    return errors


def current_link_errors(features,invariants,tests):
    errors=[]
    if(len(features),len(invariants),len(tests))!=(18,18,36):errors.append('B21 FE18/INV18/T36')
    for n,(fe,inv)in enumerate(zip(features,invariants),1):
        if inv.get('feature_ids')!=fe.get('id')or any(inv.get(k)!=fe.get(k)for k in('finding_ids','evidence','acceptance_ids')):errors.append('B21 exact FE/INV lineage')
        related=[t for t in tests if t.get('feature_ids')==fe.get('id')]
        if len(related)!=2 or';'.join(t['id']for t in related)!=fe.get('acceptance_ids'):errors.append('B21 two reverse-linked plans per feature')
        if n<=3 and(fe.get('finding_ids')!=NEW_IDS[n-1]or any(t.get('plan_kind')!='finding-specific'or t.get('finding_ids')!=NEW_IDS[n-1]for t in related)):errors.append('B21 three independent new roots/plans')
        for k in('owner_role','required_redacted_input','impact_if_unavailable','next_step'):
            if not isinstance(fe.get(k),str)or not fe[k].strip():errors.append('B21 feature responsibility:'+k)
    errors+=bidirectional_errors(features,tests,'feature_ids')+bidirectional_errors(invariants,tests,'invariant_ids')
    if len({r.get('required_invariant')for r in invariants})!=18 or len({r.get('acceptance_criterion')for r in tests})!=36:errors.append('B21 distinct substantive invariants/criteria')
    if any(r.get('status')!='not-executed'for r in tests):errors.append('B21 acceptance never executed')
    return errors


def residual_errors(current,upstream):
    if len(current)!=14 or len(upstream)!=14:return ['B21 all14 upstream residual identities required']
    errors=[]
    for old,new in zip(upstream,current):
        if(new.get('upstream_residual_id')!=old.get('id')or new.get('upstream_artifact')!='evidence/residual-disposition-07B20.csv'or new.get('upstream_row_sha256')!=row_sha(old)or new.get('upstream_contract_ids')!=old.get('upstream_contract_ids')):errors.append('B21 exact upstream residual identity/hash/contracts')
        for k in('local_result','owner_role','required_redacted_input','impact_if_unavailable','next_step','static_exit_criterion','current_handoff_or_split_ids'):
            if not isinstance(new.get(k),str)or not new[k].strip():errors.append('B21 residual responsibility:'+k)
        if not new.get('required_redacted_input','').startswith(old.get('required_redacted_input','')):errors.append('B21 no lost old required input')
        if new.get('disposition')not in{'external-handoff','split-explicitly','assessment-source-bound'}or new.get('runtime_status')!='not-executed':errors.append('B21 no residual approval/execution overclaim')
    return errors


def remaining_work_errors(work,splits):
    from validate_barcode_contract_part import remaining_work_errors as b20_errors
    adapted=[dict(r)for r in work]
    if len(adapted)!=10 or adapted[3].get('status')!='bounded-R4e-amountwords-delivered-residuals-open':return ['B21 boundedR4e status, not whole7B closure']
    adapted[3]['status']='bounded-R4d-barcode-delivered-residuals-open'
    return ['B21 '+e for e in b20_errors(adapted,splits)]


def witness_metadata_errors(w):
    errors=[]
    for k in('application_code_imported_or_executed','dotnet_or_visualbasic_format_parse_or_words_executed','scanner_template_or_printer_executed','application_remediation_performed','real_business_or_secret_data_used','spreadsheet_or_formula_interpreter_executed','phase7C_started','phase8_authorized_or_started'):
        if w.get(k)is not False:errors.append('B21 false-only boundary:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(w.get(k))is not int or w[k]!=0:errors.append('B21 integer-zero boundary:'+k)
    for k in('B_R4e_bounded_not_whole7B_closure','prior_roots_not_assumed_remediated','unresolved_external_contracts_and_explicit_splits_retained'):
        if w.get(k)is not True:errors.append('B21 true-only boundary:'+k)
    for k in('illustration_count','static_lexical_contract_check_count'):
        if type(w.get(k))is not int or w[k]!=12:errors.append('B21 exact12 illustrative/lexical count:'+k)
    if w.get('phase')!='7B21-partial-static-amountword-contracts':errors.append('B21 witness phase')
    return errors+arithmetic_erratum_errors(w.get('retained_additive_B10_arithmetic_erratum'))


def historical_record_errors(h):
    modes=h.get('historical_modes',[]);errors=[]
    if type(h.get('historical_mode_count'))is not int or h['historical_mode_count']!=26 or len(modes)!=26:return ['B21 exactly26 OWN records required']
    errors+=historical25_errors(dict(historical_mode_count=25,historical_modes=modes[:25],errors=h.get('errors')))
    last=modes[-1];child=last.get('historical_B20_child')or{}
    if last.get('mode')!='B20'or last.get('findings_total')!=310 or last.get('registry_used')!=SNAPSHOT or last.get('process_exit_code')!=0 or last.get('validation_errors')!=[]or last.get('original_project_hashes_matching')!=827:errors.append('B21 B20 historical OWN310 identity, not live313')
    if(last.get('audit_checker_self_test_cases_reported'),last.get('audit_checker_self_test_suite_count'))!=(530,21):errors.append('B21 genuine B20 aggregate530/21')
    if(child.get('tests_reported')!=32 or child.get('expected_tests')!=32 or child.get('process_exit_code')!=0 or child.get('result')!='passed'or child.get('historical_parser_cutoff')!='B20-not-current-B21-default'or child.get('all_original_cases_executed_unmodified')is not True or child.get('dedicated_child_launcher')!='tools/run_historical_barcode_tests_07B21.py'or child.get('no_test_skips_or_global_subprocess_or_path_patch')is not True):errors.append('B21 B20 all32 explicit historical child')
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):
        if type(last.get(k))is not int or last[k]!=0:errors.append('B21 no historical ERP/SQL run')
    if not isinstance(last.get('stdout_sha256'),str)or re.fullmatch('[0-9a-f]{64}',last['stdout_sha256'])is None:errors.append('B21 historical stdout hash')
    return errors


def validate_source(v,row,scope):
    if'evidence'not in row:return
    if row['evidence']==DOCUMENTARY:v.check(row['id']in SENTINELS,'B21 undeclared documentary sentinel:'+row['id'])
    else:
        v.check(row['id']not in SENTINELS,'B21 fabricated source for documentary gate:'+row['id']);v.evidence(row['evidence'],row['id'])
        try:expanded=expanded_source_evidence(row['evidence'])
        except ValueError as e:v.check(False,'B21 invalid scoped source '+row['id']+':'+str(e));return
        v.scoped_evidence(expanded,scope,row['id']+' boundedB21',phase=7)


def extend_amountword_contracts(v,report,prov,frozen310):
    ck,rows=v.check,v.rows;current=rows('findings.csv');new=current[310:]
    for e in registry_preservation_errors(frozen310,current,(v.AUDIT/'findings.csv').read_bytes(),(v.AUDIT/SNAPSHOT).read_bytes()):ck(False,e)
    ck(len({r['id']for r in current})==313,'B21 distinct313 IDs');ck(rows('evidence/historical-extensions-07B21.csv')==[],'B21 zero prior registry extensions')
    v.distributions(new,dict(Medium=3),dict(confirmed=3),'B21 only')
    for r in new:ck((r['type'],r['status'],r['next_phase'])==('implementation-defect','open-not-remediated','8'),'B21 finding/permission state')
    ck(re.findall(r'^### (P7-\d{3}) — (.+)$',v.read(v.AUDIT/PART_DOCS[0]),re.M)==[(r['id'],r['title'])for r in new],'B21 heading/registry exact')
    for k in('phase8_authorized_or_started','phase7C_started','application_remediation_performed'):ck(prov[k]is False,'B21 no implicit start:'+k)
    for k in('erp_runtime_tests_executed','sql_or_external_service_tests_executed'):ck(type(prov[k])is int and prov[k]==0,'B21 no ERP/SQL:'+k)
    selected=rows(SCOPE_FILE);scope={r['path']:v.spans(r['ranges'])for r in selected};original={r['path']for r in rows('evidence/inventory.csv')}
    ck(len(selected)==len(scope)==24,'B21 selected24 bounded paths')
    for r in selected:
        ck(r['path']in original and r['review_state']=='selected-static-amountword-caller-currency-domain-projection-slices-not-runtime-certified'and bool(r['focus']),'B21 selected scope identity/depth');v.source_ref(r['path'],r['ranges'],SCOPE_FILE)
    for r in new:validate_source(v,r,scope)
    known={r['id']for r in current}|{f'H7B21-{n:02d}'for n in range(1,7)};tables={}
    for name,prefix,count in TABLE_SPECS:
        data=rows('evidence/'+name+'-07B21.csv');tables[prefix]=data;v.sequential(data,prefix,count)
        if data and'finding_ids'in data[0]:v.related(data,known)
        for r in data:
            ck(all(isinstance(x,str)and x.strip()for x in r.values()),'B21 incomplete CSV:'+r['id']);validate_source(v,r,scope)
            if'runtime_status'in r:ck(r['runtime_status']=='not-executed','B21 runtime overclaim:'+r['id'])
    fe,inv,tests=[tables[x]for x in('FE7B21-','INV7B21-','P7B21T-')]
    for e in current_link_errors(fe,inv,tests):ck(False,e)
    v.proposed_tests(tests,'7B21');fids,iids,tids=[{r['id']for r in pool}for pool in(fe,inv,tests)]
    v.related(tests,fids,'feature_ids');v.related(tests,iids,'invariant_ids');v.related(fe+inv,tids,'acceptance_ids');v.related(tables['WC7B21-'],fids,'feature_ids')
    for pool,label in((fe,'features'),(inv,'invariants'),(tests,'plans')):v.covered(new,pool,'B21 '+label)
    for r in tables['RC7B21-']:
        fs=[f for f in fe if f['id']in r['feature_ids'].split(';')];unique=lambda k:';'.join(dict.fromkeys(x for f in fs for x in f[k].split(';')))
        expected=';'.join(dict.fromkeys(x for f in fs if f['evidence']!=DOCUMENTARY for x in f['evidence'].split(';')))or DOCUMENTARY
        ck(r['finding_ids']==unique('finding_ids')and r['acceptance_ids']==unique('acceptance_ids')and r['evidence']==expected,'B21 RC exact source/FE lineage');v.related([r],fids,'feature_ids');v.related([r],tids,'acceptance_ids')
    for e in residual_errors(tables['RS7B21-'],rows('evidence/residual-disposition-07B20.csv'))+remaining_work_errors(tables['RW7B21-'],tables['SP7B21-'])+currency_branch_errors(tables['CM7B21-']):ck(False,e)
    hids={r['id']for r in tables['H7B21-']};sids={r['id']for r in tables['SP7B21-']};v.related(tables['RS7B21-'],hids|sids,'current_handoff_or_split_ids');v.related(tables['Q7B21-'],hids,'handoff_ids')
    for r in tables['H7B21-']:ck(r['status']=='external-contract-or-policy-unresolved-not-absence-proof','B21 no invented handoff approval')
    for r in tables['Q7B21-']:ck(r['status']=='unanswered-no-secrets-requested','B21 no invented policy answer')
    for n,r in enumerate(tables['BK7B21-'],1):ck(r['prior_backlog_id']==f'BK7B20-{n:02d}'and r['original_backlog_id']==f'BK7-{n:02d}'and r['status']!='complete','B21 backlog ancestry/uncompleted')
    ck([r['status']for r in tables['BK7B21-'][2:6]]==['not-started']*4,'B21 C axes remain unstarted')
    ad=tables['AD7B21-'];v.related(ad,known,'current_root_ids');v.related(ad,known,'nearest_prior_root_ids');ck([r['current_root_ids']for r in ad if r['decision']=='new-local-root']==NEW_IDS,'B21 only three adjudicated causes')
    for r,a in zip(new,ad):ck(set(r['evidence'].split(';'))<=set(a['evidence'].split(';')),'B21 adjudication source chain')
    ck(all(r['comparison_depth']=='all310-registry-titles-classifications-plus-selected-nearest-source-chains-not-all-historical-bodies'for r in ad),'B21 honest dedup depth')
    prior_names=['review-scope.csv']+[f'review-scope-{n:02d}.csv'for n in range(2,8)]+[f'review-scope-07B{n}.csv'for n in range(1,21)]
    before={r['path']for name in prior_names for r in rows(name)};paths=set(scope)
    ck((len(before),len(paths&before),len(paths-before),len(before|paths),len(original-(before|paths)))==(410,22,2,412,415),'B21 paths not a completion percentage')
    decision=v.json.loads(v.read(v.AUDIT/'evidence/scope-decision-07B21.json'))
    ck(decision['authority']==['PHASE-07-REMAINING-07B20.md','evidence/split-register-07B20.csv']and decision['selected_upstream_split']=='SP7B20-03'and decision['entry']==ENTRY and decision['bookkeeping']==dict(selected_paths=24,prior_union=410,overlap=22,new=2,union=412,complement=415,complement_kinds={'source':350,'generated-artifact':61,'project-or-resource':4}),'B21 authority/reasoned scope')
    ck(v.sha(v.AUDIT/'evidence/amountword-contract-witnesses-07B21.json')==WITNESS_SHA,'B21 genuine first witness capture')
    witness,match=v.recompute('evidence/amountword-contract-witnesses-07B21.json','tools/check_amountword_contract_witnesses.py')
    for e in witness_metadata_errors(witness):ck(False,e)
    ck(witness['errors']==[],'B21 witness observations')
    for key,prefix,flag in(('illustrations','ALG7B21-','illustration_assertions_passed'),('static_lexical_contract_checks','ST7B21-','documented_text_observation_matches')):
        data=witness[key];v.sequential(data,prefix,12);v.related(data,known)
        for r in data:
            ck(r[flag]is True and r['source_application_executed']is False and bool(r['limit']),'B21 witness not runtime/currency-policy acceptance');validate_source(v,r,scope)
    for r in witness['bounded_source_reads_not_semantic_coverage']:v.scoped_evidence(f'{r["path"]}:{r["start"]}-{r["end"]}',scope,'B21 lexical read',phase=7)
    ck(len(witness['bounded_source_reads_not_semantic_coverage'])==33,'B21 actual33 bounded lexical reads')
    discovery=witness['qualified_literal_discovery'];ck(discovery['not_complete_callgraph_or_capability_census']is True and discovery['scanned_bodies_not_reviewed']is True and discovery['source_csharp_paths_lexically_scanned']==477 and len(discovery['literal_qualified_english_calls'])==2 and len(discovery['lexical_utf8_replacement_paths_not_encoding_acceptance'])==4,'B21 lexical scan/encoding limits')
    for e in caller_errors(tables['WC7B21-'],discovery['literal_qualified_arabic_calls']):ck(False,e)
    ck(discovery['external_qualified_Number2Arabic_ameral_calls_discovered']==[],'B21 no external qualified legacy helper token discovered, not absence proof')
    texts=v.json.loads(v.read(v.AUDIT/SHARED_SNAPSHOT))['files']
    for e in group_row_errors(texts['IMPROVEMENTS.md'],v.read(v.AUDIT/'IMPROVEMENTS.md')):ck(False,e)
    pending=False;source=re.compile(r'((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings)):(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)')
    for name in PART_DOCS+SHARED_DOCS:
        doc=v.AUDIT/name;text=v.read(doc)
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)',text):
            url=urlsplit(m[1])
            if url.scheme or m[1].startswith('#'):continue
            target=(doc.parent/unquote(url.path)).resolve()
            if target==(v.AUDIT/'evidence/checks-07B21.json').resolve()and not target.exists():pending=True;continue
            v.LINK_COUNT+=1;ck(target.exists(),'B21 broken link:'+name+':'+m[1])
        for m in source.finditer(text):
            v.source_ref(m[1],m[2],name)
            if name in PART_DOCS:v.scoped_evidence(';'.join(f'{m[1]}:{a}-{b}'for a,b in v.spans(m[2])),scope,name,phase=7)
    for name in SHARED_DOCS:ck(all(t in v.read(v.AUDIT/name)for t in('PHASE-07B21.md','PHASE-07-REMAINING-07B21.md','7B22','غير مأذونة','c2c895d','10ba215')),'B21 shared index current boundary:'+name)
    hist_path='evidence/historical-mode-verification-07B21.json';ck(HISTORICAL_RUN_SHA is not None and(v.AUDIT/hist_path).is_file(),'B21 historical26 genuinely captured')
    if(v.AUDIT/hist_path).is_file():
        ck(v.sha(v.AUDIT/hist_path)==HISTORICAL_RUN_SHA,'B21 actual historical26 identities');historical=v.json.loads(v.read(v.AUDIT/hist_path))
        for e in historical_record_errors(historical):ck(False,e)
        ck(historical['checkout_head']==ENTRY and historical['source_head']==v.HEAD and historical['branch']==v.BRANCH,'B21 historical modes source/entry')
        report['phase_7B21_executed_historical_documentary_modes']=dict(record=hist_path,sha256=HISTORICAL_RUN_SHA,modes_reported=26,all_documentary_exit_codes_zero=True,B20_OWN310_raw311CRLF_and_historical32_child=True,null_means_aggregate_not_reported_not_zero=True,not_original_metric_replay_or_erp_tests=True)
    tools=['check_amountword_contract_witnesses.py','validate_amountword_contract_part.py','run_historical_barcode_tests_07B21.py','test_amountword_contract_audit_validator.py']
    for name in tools:
        try:v.ast.parse(v.read(v.AUDIT/'tools'/name),filename=name)
        except SyntaxError as e:ck(False,'B21 syntax:'+str(e))
    run=v.subprocess.run([v.sys.executable,'-B',str(v.AUDIT/'tools/test_amountword_contract_audit_validator.py')],cwd=v.ROOT,capture_output=True,text=True,timeout=30)
    m=re.search(r'Ran (\d+) tests? in ',run.stderr+'\n'+run.stdout);count=int(m[1])if m else None;passed=run.returncode==0 and count==36;ck(passed,'B21 36 documentary self-tests/count')
    report['validation']['audit_only_checker_self_tests_executed_not_erp_tests'][tools[-1]]=dict(tests_reported=count,expected_tests=36,process_exit_code=run.returncode,result='passed'if passed else'failed-or-unrecognized',erp_code_imported_or_executed=False)
    report['validation']['audit_only_python_tools_syntax_checked']+=tools;report['validation']['current_audit_checker_source_sha256_not_original_application'].update({'tools/'+n:v.sha(v.AUDIT/'tools'/n)for n in['validate_audit.py']+tools})
    report.update(validation_scope='current-through7B21-313-bounded-R4e-amountword-contracts-not-7B-or-runtime-closure',phase_7_delivery='7A+'+'+'.join('7B'+str(n)for n in range(1,22))+'-partial-not-complete7B-or7',phase_7_remaining_parts=['7B22-proposed-R4f-explicit-SP01-SP02-SP03-and-external-contracts','7C-six-axes-not-started'],registry_used='findings.csv',historical_artifact_sha256=prov['historical_artifact_sha256'],date_semantics=prov['date_semantics'])
    report['findings'].update(phase_7=141,phase_7B21=3,total_open_not_remediated=313,severity=dict(collections.Counter(r['severity']for r in current)),certainty=dict(collections.Counter(r['certainty']for r in current)))
    report['scope_files'].update({SCOPE_FILE:24,'phase_7B21_prior_union':410,'phase_7B21_overlap_with_prior_union':22,'phase_7B21_new_paths':2,'unique_union_not_line_or_execution_coverage':412,'inventory_only_no_selected_scope':415})
    report['phase_7B20_historical_evidence']=dict(frozen_registry=SNAPSHOT,frozen_registry_sha256_matches=v.sha(v.AUDIT/SNAPSHOT)==SNAPSHOT_SHA,frozen_shared_indexes=SHARED_SNAPSHOT,earlier_report_evidence_artifacts_hash_checked=583,historical_check_record_overwritten=False,genuine_b20_stdout_sha256_unchanged=B20_CHECK_SHA,partial7B21_append_only_extensions=[],all310_rows_including_ALL_next_phase_evidence_and_raw_prefix_preserved=True)
    report['phase_7B21_amountword_trace_limits']=dict(literal_qualified_arabic_calls=12,literal_qualified_english_calls=2,named_WPF_caller_paths=10,source_csharp_paths_lexically_scanned_not_body_reviews=477,selected_paths_are_bounded_slices=24,current_FE_or_documentary_contracts=18,invariants_not_executed_tests=18,acceptance_plans_not_executed=36,residual_inputs=14,explicit_further_static_splits=3,B_R4e_delivered_not_whole_R4_SP03_or7B_closure=True,retained_potential_roots_not_promoted=['P4-014','P7-132'],external_enum_or_precision_sign_zero_policy_invented=False,C_axes_not_started=6,counts_are_sessions_or_completion_percent=False)
    report['evidence_rows'].update(phase_7B21_illustrations_not_erp_tests=12,phase_7B21_lexical_checks_not_erp_tests=12,phase_7B21_bounded_source_reads_not_semantic_coverage=len(witness['bounded_source_reads_not_semantic_coverage']),phase_7B21_witness_recomputed_matches_saved=match)
    report['validation']['current_output_record_pending_first_write_not_placeholder']=pending
    report['validation']['limit']='Read-only bounded7B21/R4e:583 protected artifacts/310 EXACT fields including ALLnext_phase/evidence/raw311CRLFprefix/G195/3freezes/827 originals. Three Medium confirmed local causes139..141: fixed twelve-position magnitude without upper-domain guard, alternate invoice local currency DTO omission, receipt D/QAndroid failed amount parse→word-input0 while raw BondVal retained. Conditional source proofs, no actual .NET/VB parse/format/word output, printed blank currency, saved zero or large deployed amount observed.034/035 rechecked not recounted or extended. Primary preformatted Net, code2 partial currency consistency, shared settings13 and magnitude+side/read-only salary are counterevidence, not acceptance. External Currency enum/index mapping, major/minor precision/sign/zero/grammar/support/SDK/tabletype/template contracts remain unapproved; no invented policy or country inference.12AR/2EN qualified tokens from477 lexical source scans (four UTF8 replacement scans not encoding acceptance) are not477 body reviews/allcallgraph/capability census;24 slice paths/22overlap/2new→union412/complement415 not a completion percentage.18FE/INV36 acceptance plans NOT executed;14 residuals/3splits/6H/Q not external approvals. R4f/B22 proposed;7B/7 partial;6C axes unstarted;8 unauthorized. B20 OWN310/exact311CRLF/indexes in memory and ALL32 originals in explicit historical child presetB20; current B21 CLI/default independently tested36 cases. Earlier B19/36 and B18/28 children retained. No protected edits/skips/global Path or subprocess patch/disk overlay/rebaseline/archive rewrite. Source10ba/completedB20push-entryc2c895d/genuineB20stdoutac20e31 distinct.12 supplied ASCII/Decimal/boolean manual models and12 lexical checks/33 bounded reads are not ERP/C#/VB/WPF/SQL/UtilitiesProj/REPX/culture/SDK/symbology/scanner/printer/business acceptance. B10 additive10vs120 erratum retained. Financial/ACL/stock/save/production020/021 barriers and136..138 remain;014/132 potential unchanged. No application import/build/provider/external service/business data/secrets/remediation/operational measurement. next_phase8 planning is not permission.'
