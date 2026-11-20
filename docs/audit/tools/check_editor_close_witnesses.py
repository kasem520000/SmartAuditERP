#!/usr/bin/env python3
"""B32 inert source/dispatch illustrations, not WPF/SDK/SQL execution.

Authored XAML and constructor subscriptions are two representations of two
attachments, not three including imaginary generated code. Closing Cancel is
not KeyDown.Handled. F6 records validation REQUESTS, never successful saves.
Header setter profiles are supplied; an unavailable SDK contract stays unknown.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3]
ENTRY='0bbadbe9f86a7ded7bbb1d2bcce209c7eda551fb'
SC='SmartAuditERP/Form_WPF/frmInvSale.xaml.cs';PC='SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs';SX='SmartAuditERP/Form_WPF/frmInvSale.xaml';PX='SmartAuditERP/Form_WPF/frmInvPurch.xaml';PR='SmartAuditERP/SmartAuditERP.csproj'
SOURCE_SLICES=tuple([(SC,a,z) for a,z in ((65,94),(236,317),(1662,1679),(2563,2574),(3528,3542),(3790,3803))]+[(PC,a,z) for a,z in ((67,88),(1571,1594),(2071,2087),(2738,2753),(2798,2803))]+[(SX,a,z) for a,z in ((1,16),(404,409),(580,585),(1158,1165),(1264,1271))]+[(PX,a,z) for a,z in ((1,16),(525,533),(548,556),(1323,1329),(1431,1439))]+[(PR,130,152)])
EXPLORATORY_SLICES=((SC,3399,3566),(PC,1970,2088),(SC,1780,1889),(SC,200,264),(SC,3710,3807),(PC,2680,2803),(SC,317,351),(PC,89,122),(PR,1,45))
EVIDENCE=f'{SC}:65-94;{SX}:1-16;{SC}:236-317;{PC}:67-88;{PX}:1-16;{PC}:2738-2753'
def flag(v):
    if type(v) is not bool:raise ValueError('Explicit supplied bool,not an SDK inference')
    return v
def count(v):
    if type(v) is not int or not 0<=v<=1000:raise ValueError('Bounded supplied count')
    return v
def guard(editor,is_new,is_updated,rows):
    if editor not in ('sale','purchase'):raise ValueError('Editor')
    flag(is_new);flag(is_updated);count(rows)
    return (rows>(1 if editor=='sale' else 0) and is_new) or is_updated
def close_trace(editor,conditions,replies,initial_cancel=False):
    if editor not in ('sale','purchase') or type(conditions) is not list or len(conditions)>3 or type(replies) is not list:raise ValueError('Explicit invocation list')
    for c in conditions:flag(c)
    if any(type(r) is not str or r not in ('Yes','No') for r in replies) or len(replies)!=sum(conditions):raise ValueError('Exactly the reached replies')
    cancel=flag(initial_cancel);idx=0;events=[]
    for n,condition in enumerate(conditions,1):
        reply=None;before=cancel
        if condition:
            reply=replies[idx];idx+=1
            if editor=='purchase':cancel=reply=='No'
            elif reply=='No':cancel=True
        events.append(dict(invocation=n,guard=condition,reply=reply,cancel_before=before,cancel_after=cancel))
    return dict(editor=editor,invocations=len(conditions),prompts=idx,cancel_at_boundary=cancel,events=events,actual_window_closed_claimed=False,Cancel_does_not_short_circuit_this_supplied_invocation_list=True)
def key_trace(key,attachments=2,handled=False,returns=None):
    if key not in ('F5','F6'):raise ValueError('Only selected keys')
    if type(attachments) is not int or not 0<=attachments<=3:raise ValueError('Attachment bound')
    flag(handled)
    if returns is None:returns=[True]*(0 if handled else (min(attachments,1) if key=='F5' else attachments))
    if type(returns) is not list:raise ValueError('Supplied downstream boundary returns')
    for r in returns:flag(r)
    calls=0;events=[];escaped=False
    for n in range(attachments):
        if handled:events.append(dict(attachment=n+1,invoked=False));continue
        if calls==len(returns):raise ValueError('Missing reached outcome')
        returned=returns[calls];calls+=1;events.append(dict(attachment=n+1,invoked=True,downstream_returned=returned))
        if not returned:escaped=True;break
        if key=='F5':handled=True
    if calls!=len(returns):raise ValueError('Unreached outcomes supplied')
    return dict(key=key,registered_attachments=attachments,handler_invocations=calls,validation_requests=calls if key=='F6' else 0,new_command_requests=calls if key=='F5' else 0,handled_at_boundary=handled,boundary_did_not_return=escaped,events=events,successful_saves_inferred=False,routed_event_mask_rule_is_supplied_standard_contract=True)
def header_edit(before,after,is_updated,profile):
    if type(before) is not str or type(after) is not str or len(before)>80 or len(after)>80:raise ValueError('Redacted bounded strings')
    flag(is_updated)
    if profile not in ('no-dirty-effect','dirty-on-value-change','dirty-on-assignment','unresolved'):raise ValueError('Supplied setter profile')
    updated=None if profile=='unresolved' else is_updated or profile=='dirty-on-assignment' or (profile=='dirty-on-value-change' and before!=after)
    return dict(value_after=after,is_updated_after=updated,profile=profile,profile_is_not_actual_SDK_behavior=True)
def new_intent(editor,is_new,is_updated,rows,reply=None):
    need=guard(editor,is_new,is_updated,rows)
    if (need and reply not in ('Yes','No')) or (not need and reply is not None):raise ValueError('Exactly one reached decision')
    denied=need and reply=='No'
    return dict(prompt_required=need,denied=denied,first_write_boundary=None if denied else ('ReturnYearPreviews=false-before-CLR' if editor=='sale' else 'CLR-entry-only'),CLR_or_SDK_executed=False)
def read_slice(path,a,z):
    raw=(ROOT/path).read_bytes();lines=raw.decode('utf8').splitlines()
    if not (1<=a<=z<=len(lines)):raise ValueError('Out of source range')
    return '\n'.join(lines[a-1:z])
def build():
    sale_ctor=read_slice(SC,65,94);purch_ctor=read_slice(PC,67,88);sx=ET.fromstring((ROOT/SX).read_bytes());px=ET.fromstring((ROOT/PX).read_bytes())
    cs=read_slice(SC,236,250);cp=read_slice(PC,2738,2753);keys=read_slice(SC,252,317);sn=read_slice(SC,2563,2574);pn=read_slice(PC,1571,1594);sh=read_slice(SC,3528,3542);ph=read_slice(PC,2071,2087)
    cases=[('sale-Yes-Yes',close_trace('sale',[True,True],['Yes','Yes']),dict(prompts=2,cancel_at_boundary=False)),('sale-No-Yes',close_trace('sale',[True,True],['No','Yes']),dict(prompts=2,cancel_at_boundary=True)),('sale-Yes-No',close_trace('sale',[True,True],['Yes','No']),dict(prompts=2,cancel_at_boundary=True)),('sale-No-No',close_trace('sale',[True,True],['No','No']),dict(prompts=2,cancel_at_boundary=True)),('sale-clean',close_trace('sale',[False,False],[]),dict(prompts=0,cancel_at_boundary=False)),('sale-existing-veto',close_trace('sale',[True,True],['Yes','Yes'],True),dict(prompts=2,cancel_at_boundary=True)),('purchase-single-No',close_trace('purchase',[True],['No']),dict(prompts=1,cancel_at_boundary=True)),('purchase-single-Yes',close_trace('purchase',[True],['Yes']),dict(prompts=1,cancel_at_boundary=False)),('purchase-existing-veto-source-boundary-only',close_trace('purchase',[True],['Yes'],True),dict(prompts=1,cancel_at_boundary=False)),('changing-guard-not-always-two-prompts',close_trace('sale',[True,False],['No']),dict(prompts=1,cancel_at_boundary=True)),('F6-two-returning-callbacks',key_trace('F6'),dict(handler_invocations=2,validation_requests=2,successful_saves_inferred=False)),('F5-handled-masks-second',key_trace('F5'),dict(handler_invocations=1,new_command_requests=1,handled_at_boundary=True)),('F6-initially-handled',key_trace('F6',handled=True),dict(handler_invocations=0,validation_requests=0)),('F6-first-does-not-return',key_trace('F6',returns=[False]),dict(handler_invocations=1,boundary_did_not_return=True)),('header-profile-no-dirty',header_edit('fixture-A','fixture-B',False,'no-dirty-effect'),dict(is_updated_after=False)),('header-profile-dirty',header_edit('fixture-A','fixture-B',False,'dirty-on-value-change'),dict(is_updated_after=True)),('header-profile-unresolved',header_edit('fixture-A','fixture-B',False,'unresolved'),dict(is_updated_after=None)),('new-sale-No',new_intent('sale',False,True,2,'No'),dict(denied=True,first_write_boundary=None)),('new-purchase-empty-header-only-supplied-false',new_intent('purchase',True,False,0),dict(prompt_required=False,first_write_boundary='CLR-entry-only')),('new-sale-Yes',new_intent('sale',False,True,2,'Yes'),dict(denied=False,first_write_boundary='ReturnYearPreviews=false-before-CLR'))]
    illustrations=[]
    for n,(name,trace,expected) in enumerate(cases,1):
        ok=all(trace[k]==v and type(trace[k]) is type(v) for k,v in expected.items())
        illustrations.append(dict(id=f'ALG7B32-{n:02d}',boundary=name,trace=trace,expected=expected,illustration_assertions_passed=ok,finding_ids='P7-162' if n<=14 else 'H7B32-02',evidence=EVIDENCE,source_application_executed=False,limit='مصدر ومعطيات اصطناعية فقط؛القوائم والحراس والردود ورجوع النداء موردة،لا حوار أوWPF أوSDK أوحفظ أوحالةUI نهائية مرصودة.'))
    checks=[('sale-XAML-three-events',all(sx.get(k)==v for k,v in {'Closing':'Window_Closing','Loaded':'Window_Loaded','KeyDown':'Window_KeyDown'}.items())),('sale-constructor-three-extra-events',all(sale_ctor.count(s)==1 for s in ('Closing += Window_Closing;','Loaded += Window_Loaded;','KeyDown += Window_KeyDown;'))),('InitializeComponent-before-extra-Closing',sale_ctor.index('InitializeComponent();')<sale_ctor.index('Closing += Window_Closing;')),('purchase-XAML-one-declared-Closing',px.get('Closing')=='frmSalePurch_FormClosing'),('purchase-constructor-no-extra-Closing-in-selected-body','Closing +=' not in purch_ctor and 'InitializeComponent();' in purch_ctor),('sale-Closing-only-No-sets-cancel','if (result == MessageBoxResult.No)' in cs and 'e.Cancel = true;' in cs and 'e.Cancel = false' not in cs),('purchase-Closing-assigns-result',bool(re.search(r'e\.Cancel\s*=\s*MessageBox\.Show\(',cp)) and '== MessageBoxResult.No;' in cp),('sale-dirty-predicate', 'GridControl1.Items.Count > 1' in cs and 'Invoic.IsUpdated' in cs),('purchase-dirty-predicate','_invoiceItems.Count > 0' in cp and 'this.Invoic?.IsUpdated == true' in cp),('sale-F5-explicit-Handled',bool(re.search(r'e.Key == Key.F5[\s\S]*?btnNew_Click\(null, null\);\s*e.Handled = true;',keys))),('sale-F6-validation-no-Handled-in-branch','if (e.Key == Key.F6)\n                ValidateInvoice();' in keys),('sale-new-guard-before-first-write',sn.index('CheckBeforeClear()')<sn.index('ReturnYearPreviews = false;')<sn.index('CLR();')),('purchase-new-existing-guard','if (!this.CheckBeforeClear())\n                this.CLR();' in pn),('sale-header-text-wiring',all(x in (ROOT/SX).read_text() for x in ('TextChanged="txtRefNo_TextChanged"','TextChanged="txtNote_TextChanged"'))),('purchase-header-text-wiring',all(x in (ROOT/PX).read_text() for x in ('TextChanged="txtRefNo_TextChanged"','TextChanged="txtNote_TextChanged"'))),('sale-header-setter-contract-not-inferred','Invoic.ReffNo = txtRefNo.Text;' in sh and 'Invoic.InvNote = txtNote.Text;' in sh and 'IsUpdated' not in sh),('purchase-header-null-guards','this.Invoic.ReffNo = this.txtRefNo.Text;' in ph and 'this.Invoic.InvNote = this.txtNote.Text;' in ph and ph.count('if (this.Invoic != null)')==3),('local-comparator-no-literal-caller',len(re.findall(r'\bIsInvoiceChanged\s*\(', (ROOT/SC).read_text()))==1),('SDK-references-not-owning-type-proof',all(x in read_slice(PR,130,152) for x in ('<Reference Include="UtilitiesProj">','<Reference Include="Ws_Auditor">'))),('no-generated-event-count-added',len(SOURCE_SLICES)==22 and len({p for p,_,_ in SOURCE_SLICES})==5)]
    lexical=[dict(id=f'ST7B32-{i:02d}',boundary=name,documented_text_observation_matches=bool(ok),finding_ids='P7-162' if i<=13 else 'H7B32-02',evidence=EVIDENCE,source_application_executed=False,limit='فحص نص/عقد مصدر محدود لاBAML أوbuild أوجدولة أوتعداداشتراكاتوقتتشغيل؛غيابIsUpdatedالصريحليسغيابقدرةSDK.') for i,(name,ok) in enumerate(checks,1)]
    def reads(pool,kind):
        return [dict(path=p,start=a,end=z,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),purpose=kind,whole_local_file_selected=False,whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True) for p,a,z in pool]
    errors=[r['id'] for r in illustrations if not r['illustration_assertions_passed']]+[r['id'] for r in lexical if not r['documented_text_observation_matches']]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,new_root_ids=['P7-162'],extended_existing_root_ids=[],illustration_count=20,lexical_check_count=20,selected_source_paths=5,selected_contract_slices=22,context_slices_not_certified=9,whole_local_files_selected=0,authored_sale_Closing_attachments=2,authored_purchase_Closing_attachments_in_selected_constructor_and_XAML=1,author_source_attachments_not_observed_runtime_count=True,header_setter_profiles_are_supplied_not_SDK_evidence=True,unknown_setter_profile_remains_unknown=True,callbacks_and_event_outcomes_supplied=True,F5_Handled_control_prevents_blanket_duplicate_key_claim=True,validation_requests_not_successful_saves=True,application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,compiled_BAML_or_generated_code_executed=False,persisted_duplicate_save_or_financial_loss_claimed=False,IsUpdated_propagation_or_SDK_defaults_proved=False,stable_post_event_state_claimed=False,application_remediation_performed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),illustrations=illustrations,static_lexical_contract_checks=lexical,bounded_source_reads_not_semantic_coverage=reads(SOURCE_SLICES,'selected-contract'),exploratory_source_reads_not_capability_certification=reads(EXPLORATORY_SLICES,'context-not-whole-feature-review'),errors=errors)
if __name__=='__main__':
    output=build();print(json.dumps(output,ensure_ascii=False,indent=2));raise SystemExit(bool(output['errors']))
