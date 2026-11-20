#!/usr/bin/env python3
"""B37/R4u transfer-command request/tail documentary witnesses,NOT ERP.

Four previously selected paths,16 contract and5 context slices,no whole file.
Normal modal returns,header/field snapshots,SDK setters,number values and
failure boundaries are SUPPLIED,not observed WPF/provider/SQL/SDK behavior.
Same split acceptance/conversion mechanism as160;accepted Navigate/CLR is
compared with159 without editing registry evidence or transferring certainty.
Field ProcType versus header ProcType is unresolved policy,not a new defect.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
from check_invoice_picker_witnesses import flag,number,token
ROOT=Path(__file__).resolve().parents[3]
ENTRY='a83cb66108241ad51ab4f08fbff3fe5f361d58a0'
CS='SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs';X='SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml';IO='SmartAuditERP/Class/InvoiceOper.cs';PICKER='SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs'
SOURCE_SLICES=((CS,39,40),(CS,329,347),(CS,402,420),(CS,497,522),(CS,523,544),
 (CS,1642,1657),(CS,1659,1685),(CS,1687,1711),(CS,1713,1738),
 (X,492,505),(X,1469,1473),(X,1483,1496),(IO,2789,2808),
 (IO,3219,3246),(IO,3496,3508),(PICKER,49,66))
CONTEXT_SLICES=((CS,286,328),(CS,421,453),(CS,1618,1640),(CS,1967,1987),(PICKER,88,132))
WHOLE_REREADS=()
ROUTES=('search','receive','order','purchase')
NUMBER_BOUNDARIES=('success','caught-before-number','caught-after-number','escapes-helper')
SCOPE_RANGES={CS:'39-40;286-347;402-453;497-544;1618-1738;1967-1987',X:'492-505;1469-1473;1483-1496',IO:'2789-2808;3219-3246;3496-3508',PICKER:'49-66;88-132'}


def header(slot='head-A',kind='fixture-kind',proc=2,is_new=False,invoice_no=7,combined='combined-A',gid='doc-A',note='fixture-note'):
    return dict(slot=token(slot),kind=token(kind),proc=number(proc),is_new=flag(is_new),invoice_no=number(invoice_no,0,999999),combined=token(combined),gid=token(gid,empty=True),note=token(note,empty=True))


def checked_header(h):
    if h is None:return None
    if type(h) is not dict or set(h)!=set(header()):raise ValueError('exact supplied header snapshot,no inferred DTO defaults')
    return header(**h)


def request(route):
    if type(route) is not str or route not in ROUTES:raise ValueError('four named command routes only')
    return dict(route=route,proc=2 if route=='search' else 1,inv_type={'search':8,'receive':8,'order':14,'purchase':1}[route],
        local_proc_disable_instruction_present=route!='search',mandatory_status_predicate='InvoiceStatus-equals-1' if route=='receive' else 'none',
        branch_predicate_at_Navigate=route in {'search','receive'},
        kind_proc_deleted_or_status_rechecked_at_Navigate=False,
        permission_settings_effects_or_runtime_control_enablement_proved=False)


def command(route,current,*,field_proc=2,field_type=8,label='collapsed',dirty=False,done=False,gid='-1',
            modal='normal',navigate='kept-supplied',replacement=None,number_boundary='success',candidate=41):
    """Inert boundary model;does not call or interpret C#/SQL/SDK/application.

    Accepted Navigate output is an explicitly supplied snapshot,not a simulated
    hydration/default/alias contract. A null fallback snapshot must be supplied
    too. Nonaccept never applies it. Every modeled SDK setter is assumed to
    complete until an explicitly supplied number/null boundary stops the path.
    """
    req=request(route);current=checked_header(current);replacement=checked_header(replacement)
    field_proc=number(field_proc);field_type=number(field_type);dirty=flag(dirty);done=flag(done);gid=token(gid,empty=True);candidate=number(candidate,0,999999)
    if type(label) is not str or label not in {'collapsed','visible'}:raise ValueError('supplied label state')
    if type(modal) is not str or modal not in {'normal','not-returned','throws-before-return'}:raise ValueError('supplied modal boundary,not gesture inference')
    if type(navigate) is not str or navigate not in {'kept-supplied','replacement-supplied','null-fallback-supplied','escapes-Navigate'}:raise ValueError('supplied Navigate boundary,not LoadOutcome')
    if type(number_boundary) is not str or number_boundary not in NUMBER_BOUNDARIES:raise ValueError('supplied number failure boundary only')
    if navigate in {'replacement-supplied','null-fallback-supplied'} and replacement is None:raise ValueError('fallback/replacement fields must be supplied,not DTO defaults')
    before=dict(header=copy.deepcopy(current),field_proc=field_proc,field_type=field_type,label=label)
    s=dict(request=req,before=before,header=copy.deepcopy(current),field_proc=field_proc,field_type=field_type,label=label,
        dirty_supplied=dirty,modal_boundary_supplied=modal,navigate_requested=False,check_before_clear_called=False,
        number_request=None,events=['ShowDialog-requested'],new_flag_tail_reached=False,
        typed_load_success_proved=False,SDK_setters_or_aliasing_or_final_UI_state_proved=False,
        application_source_or_provider_executed=False,number_reserved=False)
    if modal!='normal':
        if modal=='throws-before-return':s['events'].append('outer-error-handler-boundary-supplied')
        return s
    s['events'].append('normal-modal-return-supplied')
    if done and gid!='-1':
        s['navigate_requested']=True;s['events'].append('Navigate-requested-without-local-CheckBeforeClear')
        if navigate=='escapes-Navigate':s['events'].append('nonreturn-from-Navigate-supplied');return s
        if navigate in {'replacement-supplied','null-fallback-supplied'}:s['header']=copy.deepcopy(replacement)
        s['events'].append('Navigate-void-return-and-output-snapshot-supplied')
    if route=='search':return s
    if s['header'] is None:s['events'].append('null-header-dereference-boundary-supplied-outer-catch');return s
    if route=='receive':
        s['header']['proc']=1;s['events'].append('header-ProcType-written-1')
        s['field_proc']=1;s['events'].append('field-ProcType-written-1')
    else:
        s['header']['kind']='SafesTransferTo';s['events'].append('header-InvoiceType-written-symbolic-SafesTransferTo')
        s['header']['proc']=2;s['events'].append('header-ProcType-written-2-not-field')
    s['number_request']=dict(inv_type=s['field_type'],proc_type=s['field_proc'],candidate_supplied=candidate,not_from_header_proc=True)
    s['events'].append('LoadInvoiceNumber-called-using-editor-fields')
    if number_boundary=='escapes-helper':s['events'].append('helper-nonreturn-supplied-not-all-errors-caught');return s
    if number_boundary in {'success','caught-after-number'}:
        s['header']['invoice_no']=candidate;s['events'].append('header-InvoiceNo-written-with-supplied-candidate')
    if number_boundary=='success':
        s['header']['combined']=f'fixture-code-{s["field_proc"]}-{candidate}'
        s['events'].append('combined-id-symbolic-write-after-text-not-entity-reservation')
    else:s['events'].append('helper-catch-and-error-report-return-supplied')
    s['events'].append('LoadInvoiceNumber-returned-no-typed-success')
    if route=='receive':s['label']='visible';s['events'].append('receive-label-visible-instruction-reached')
    else:
        s['header']['is_new']=True;s['new_flag_tail_reached']=True;s['events'].append('ISNew-true-instruction-reached')
    return s


def abandon_guard(*,is_new=False,row_count=0,updated=False,answer='No'):
    is_new=flag(is_new);row_count=number(row_count,0,999999);updated=flag(updated)
    if type(answer) is not str or answer not in {'No','Yes'}:raise ValueError('supplied answer,not WPF interaction')
    asks=(is_new and row_count>0) or updated
    return dict(prompt_condition_supplied=asks,blocks_navigation=asks and answer=='No',runtime_dialog_observed=False)


def build():
    reads=[];context=[]
    for declared,dest,mode in ((SOURCE_SLICES,reads,'selected-contract-slice'),(CONTEXT_SLICES,context,'context-not-certified-command')):
        for path,start,end in declared:
            raw=(ROOT/path).read_bytes();lines=raw.decode('utf-8-sig').splitlines();assert 1<=start<=end<=len(lines)
            dest.append(dict(path=path,start=start,end=end,total_lines=len(lines),sha256=hashlib.sha256(raw).hexdigest(),read_mode=mode))
    def text(path,start,end):return '\n'.join((ROOT/path).read_text(encoding='utf-8-sig').splitlines()[start-1:end])
    examples=[]
    def ex(n,title,value,ok,roots,evidence):examples.append(dict(id=f'ALG7B37-{n:02d}',title=title,value=value,assertions_passed=bool(ok),finding_ids=roots,evidence=evidence,source_application_executed=False,limit='رؤوس وأعلام ورجوع طبيعي وحدود فشل وأرقام موردة؛لا WPF/SQL/SDK أو final UI/aliasing أو نجاح حفظ أو حجز رقم.'))
    q=[request(r) for r in ROUTES];ex(1,'four command requests not one universal picker contract',q,[(x['proc'],x['inv_type']) for x in q]==[(2,8),(1,8),(1,14),(1,1)],'H7B37-01',f'{CS}:1642-1738')
    s=command('search',header());ex(2,'ordinary search nonaccept is no-tail control',s,s['header']==s['before']['header'] and s['number_request'] is None,'P7-160',f'{CS}:1642-1657')
    s=command('receive',header());ex(3,'nonaccept receive writes header and editor operation then numbering and label',s,not s['navigate_requested'] and s['field_proc']==s['header']['proc']==1 and s['label']=='visible','P7-160',f'{CS}:1659-1685')
    s=command('order',header());ex(4,'nonaccept order conversion tail still reached',s,not s['navigate_requested'] and s['header']['kind']=='SafesTransferTo' and s['header']['is_new'],'P7-160',f'{CS}:1687-1711')
    s=command('purchase',header());ex(5,'nonaccept purchase shares mechanism160 not a per-button defect',s,not s['navigate_requested'] and s['new_flag_tail_reached'],'P7-160',f'{CS}:1713-1738')
    s=command('order',header(),done=True,gid='-1');ex(6,'sentinel also skips only Navigate not conversion tail',s,not s['navigate_requested'] and s['new_flag_tail_reached'],'P7-160',f'{CS}:1687-1711')
    s=command('receive',header(),done=True,gid='',navigate='kept-supplied');ex(7,'sentinel test not a validated nonempty DocumentRef',s,s['navigate_requested'] and not s['typed_load_success_proved'],'H7B37-01',f'{CS}:1659-1685')
    s=command('purchase',header(),modal='not-returned');ex(8,'ShowDialog request is not supplied return',s,s['header']==s['before']['header'] and s['number_request'] is None,'P7-160',f'{CS}:1713-1738')
    s=command('receive',header(),modal='throws-before-return');ex(9,'pre-return exception boundary does not reach tail',s,s['field_proc']==2 and s['number_request'] is None,'H7B37-05',f'{CS}:1659-1685')
    s=command('order',header(),dirty=False);ex(10,'clean nonaccept also reaches tail independently of dirty policy',s,s['new_flag_tail_reached'] and not s['check_before_clear_called'],'P7-160',f'{CS}:1687-1711;{CS}:523-544')
    s=command('receive',header(),dirty=True,done=True,gid='doc-B',navigate='replacement-supplied',replacement=header(slot='head-B',gid='doc-B'));ex(11,'accepted target not AbandonDecision159 and supplied Navigate output',s,s['navigate_requested'] and not s['check_before_clear_called'] and s['header']['slot']=='head-B','P7-159',f'{CS}:1659-1685;{CS}:402-420')
    g=abandon_guard(updated=True,answer='No');ex(12,'adjacent guarded navigation No control only',g,g['blocks_navigation'],'P7-159',f'{CS}:523-544;{CS}:1618-1640')
    s=command('order',header(),done=True,gid='doc-B',navigate='null-fallback-supplied',replacement=header(slot='fallback-supplied',gid='fixture-fallback'));ex(13,'void Navigate null fallback is not typed successful load',s,s['new_flag_tail_reached'] and not s['typed_load_success_proved'],'H7B37-02',f'{CS}:402-420;{CS}:1687-1711;{IO}:3496-3508')
    s=command('purchase',header(),number_boundary='caught-before-number');ex(14,'helper catch can return then ISNew true with previous number',s,s['header']['invoice_no']==7 and s['new_flag_tail_reached'],'H7B37-05',f'{CS}:329-347;{CS}:1713-1738')
    s=command('receive',header(),number_boundary='caught-after-number');ex(15,'caught after number can leave prior combined and still label instruction',s,s['header']['invoice_no']==41 and s['header']['combined']=='combined-A' and s['label']=='visible','H7B37-05',f'{CS}:329-347;{CS}:1659-1685')
    s=command('order',header(),number_boundary='escapes-helper');ex(16,'nonreturn boundary unlike caught-return stops new flag',s,not s['new_flag_tail_reached'] and s['header']['proc']==2,'H7B37-05',f'{CS}:329-347;{CS}:1687-1711')
    a=command('receive',header());s=command('order',a['header'],field_proc=a['field_proc']);ex(17,'field1 remains numbering request while header2 is written;policy unresolved',s,s['header']['proc']==2 and s['number_request']['proc_type']==1,'H7B37-04',f'{CS}:329-347;{CS}:1659-1711')
    s=command('purchase',header(),candidate=7);ex(18,'unchanged candidate need not hide other conversion writes',s,s['header']['invoice_no']==7 and s['new_flag_tail_reached'] and s['header']['gid']=='doc-A','P7-160',f'{CS}:1713-1738;{IO}:2789-2808')
    s=command('receive',None);ex(19,'supplied null header stops at first dereference,not default invention',s,s['header'] is None and s['field_proc']==2 and s['number_request'] is None,'H7B37-02',f'{CS}:1659-1685')
    q=request('order');ex(20,'order and purchase gid-only versus receive branch predicate;support unresolved',q,not q['branch_predicate_at_Navigate'] and request('receive')['branch_predicate_at_Navigate'],'H7B37-04',f'{CS}:1659-1738')
    lexical=[]
    def lex(n,title,path,start,end,predicate,roots):
        chunk=text(path,start,end);lexical.append(dict(id=f'ST7B37-{n:02d}',title=title,evidence=f'{path}:{start}-{end}',finding_ids=roots,documented_text_observation_matches=bool(predicate(chunk)),source_application_executed=False,limit='فحص نصوص وحدود ساكنة فقط؛لا تنفيذ تعليمات C# أو تكافؤ كل SDK/events أو فرض عيب لكل اختلاف سياسة.'))
    lex(1,'receive XAML wiring',X,492,505,lambda t:'Click="btnReceiveQuantity_Click"' in t and 'Click="BtnInvertoryOrder_Click"' in t,'P7-160')
    lex(2,'footer two routes plus reused order handler',X,1483,1496,lambda t:'Click="btnInsertPurch_Click"' in t and 'Click="BtnInvertoryOrder_Click"' in t,'P7-160')
    lex(3,'ordinary search request and no post-Navigate number tail',CS,1642,1657,lambda t:'ProcType = 2, InvType = 8' in t and 'LoadInvoiceNumber' not in t and '_invoic.ProcType =' not in t,'P7-160')
    lex(4,'receive request1/8 and mandatory condition',CS,1659,1672,lambda t:'frm.ProcType = 1;' in t and 'frm.InvType = 8;' in t and ' AND InvoiceStatus = 1' in t,'P7-156')
    lex(5,'receive single-statement gate before unconditional tail',CS,1671,1685,lambda t:t.index('if (frm.ISDone &&')<t.index('Navigate(')<t.index('_invoic.ProcType = 1;')<t.index('\n                ProcType = 1;\n')<t.index('LoadInvoiceNumber();')<t.index('Visibility.Visible'),'P7-160')
    lex(6,'order request1/14',CS,1687,1700,lambda t:'frm.ProcType = 1;' in t and 'frm.InvType = 14;' in t,'H7B37-01')
    lex(7,'order conversion after gated Navigate',CS,1699,1711,lambda t:t.index('Navigate(')<t.index('_invoic.InvoiceType = InvoiceType.SafesTransferTo;')<t.index('_invoic.ProcType = 2;')<t.index('LoadInvoiceNumber();')<t.index('_invoic.ISNew = true;'),'P7-160')
    lex(8,'purchase request1/1',CS,1713,1726,lambda t:'frm.ProcType = 1;' in t and 'frm.InvType = 1;' in t,'H7B37-01')
    lex(9,'purchase same unguarded conversion tail',CS,1725,1738,lambda t:t.index('Navigate(')<t.index('_invoic.InvoiceType = InvoiceType.SafesTransferTo;')<t.index('_invoic.ProcType = 2;')<t.index('LoadInvoiceNumber();')<t.index('_invoic.ISNew = true;'),'P7-160')
    lex(10,'number helper uses editor fields not header operation',CS,329,347,lambda t:'InvoiceOper.InvoiceNo(InvType, ProcType, _invObj.Prefixe)' in t and '_invoic.ProcType' not in t and 'ProcType.ToString()' in t,'H7B37-04')
    lex(11,'helper local catch and error report after number/text/combined sequence',CS,329,347,lambda t:t.index('_invoic.InvoiceNo =')<t.index('txtNo.Text =')<t.index('_invoic.InvCombinedId =')<t.index('catch (Exception ex)')<t.index('ShowError('),'H7B37-05')
    lex(12,'no editor ProcType2 write in order/purchase tails',CS,1687,1738,lambda t:t.count('_invoic.ProcType = 2;')==2 and '\n                ProcType = 2;' not in t,'H7B37-04')
    lex(13,'Navigate clears before reader and has null new fallback',CS,402,420,lambda t:t.index('CLR();')<t.index('BindingInvoice(ref _invoic')<t.index('if (_invoic == null)')<t.index('_invoic = new InvoiceDGV();') and 'CheckBeforeClear' not in t,'P7-159')
    lex(14,'CLR new assignment ordered,not all side effects certified',CS,497,522,lambda t:t.index('LoadInvoiceNumber();')<t.index('GridControl1.ItemsSource = null;')<t.index('_invoic = new InvoiceDGV();')<t.index('ResetInvoice();'),'P7-159')
    lex(15,'guard is local and adjacent four navigation handlers call it',CS,1618,1640,lambda t:t.count('if (!CheckBeforeClear())')==4,'P7-159')
    lex(16,'picker commands do not call that guard locally',CS,1642,1738,lambda t:'CheckBeforeClear' not in t and t.count('frm.ShowDialog();')==4,'P7-159')
    lex(17,'InvoiceNo reads MAX+1 by field request not reservation',IO,2789,2808,lambda t:'MAX(id)' in t and 'proc_type=' in t and 'Prefixe' in t and 'INSERT ' not in t and 'UPDATE ' not in t,'H7B37-04')
    lex(18,'reader null exit and outer catch retained not entire hydration',IO,3496,3508,lambda t:t.count('Invo = null;')==2 and 'catch (Exception' in t,'H7B37-02')
    lex(19,'fresh picker false and sentinel explicit,not all closing paths',PICKER,49,66,lambda t:'InvGlobalID  = "-1";' in t and 'ISDone       = false;' in t,'P7-160')
    lex(20,'another row-edit context explicitly syncs field,not all callers reviewed',CS,1967,1987,lambda t:'ProcType = _invoic.ProcType;' in t and 'LoadInvoiceNumber();' in t,'H7B37-04')
    errors=[r['id'] for r in examples if not r['assertions_passed']]+[r['id'] for r in lexical if not r['documented_text_observation_matches']]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,new_root_ids=[],extended_existing_root_ids=[],existing_roots_deepened_without_registry_change=['P7-159','P7-160'],application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,dialog_modal_return_or_Loaded_order_observed=False,real_query_or_conversion_failures_executed=False,source_enum_or_external_InvoiceDGV_contract_proved=False,all_callers_or_historical_bodies_certified=False,modal_header_field_number_and_failure_values_supplied=True,number_helper_catch_return_distinct_from_nonreturn=True,field_header_proc_difference_policy_unresolved=True,previous_year_return_button_and_other_callers_not_certified=True,repair_start_or_sync_known=False,phase7C_started=False,phase8_authorized_or_started=False,application_remediation_performed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,illustration_count=20,lexical_check_count=20,selected_source_paths=4,contract_slices=16,context_slices=5,whole_local_source_bodies_reread=0,newly_completed_local_files=0,illustrations=examples,static_lexical_contract_checks=lexical,bounded_source_reads_not_semantic_coverage=reads,context_reads_not_command_certification=context,whole_local_rereads_not_new_completions=[],retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),errors=errors)


if __name__=='__main__':
    value=build();print(json.dumps(value,ensure_ascii=False,indent=2));raise SystemExit(bool(value['errors']))
