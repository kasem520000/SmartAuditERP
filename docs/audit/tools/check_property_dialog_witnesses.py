#!/usr/bin/env python3
"""B25/R4i inert property-dialog illustrations and bounded lexical observations.

NEVER imports or executes ERP/C#/WPF/SQL/SDK code. Exact terminating rational
fixtures isolate result ownership and packing feedback, not .NET parsing,
formatting, event scheduling, financial policy, persistence or UI reachability.
The scalar field NetQnty is distinct from the text control txtNetQnty. A supplied
normal modal return is not an observed cancellation. Two selected helpers are
not a caller census; Invoicecontract and InvoiceDGV overloads stay distinct.
"""
from __future__ import annotations
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[3]
P='SmartAuditERP/Form_WPF/';C='SmartAuditERP/Class/'
SOURCE_SLICES={
 P+'frmItemProperties.xaml.cs':[(1,318)],
 P+'frmItemProperties.xaml':[(1,313)],
 C+'ItemOper.cs':[(491,655),(1047,1056),(1075,1091),(1134,1188),(1367,1410)],
 C+'ItemOpercontract.cs':[(977,1005),(1058,1083),(1171,1192),(1195,1329),(1367,1417)],
 P+'frmInvSale.xaml.cs':[(667,705),(1068,1093),(1413,1445),(3689,3745)],
 P+'frmInvSale.xaml':[(650,663),(882,888)],
 P+'frmInvInputOutput.xaml.cs':[(1146,1195)],
 P+'frmInvInputOutput.xaml':[(722,739)],
 P+'frmItems.xaml.cs':[(905,934),(985,991)],
 P+'frmItems.xaml':[(487,512)],
}

def number(value):
    """Deliberately NOT the application's culture/NumberStyles parser."""
    if not isinstance(value,str)or len(value)>80 or re.fullmatch(r'(?:0|[1-9]\d*)(?:\.\d+)?',value)is None:
        raise ValueError('Only supplied nonnegative finite plain decimal strings, not culture or .NET parsing')
    return Fraction(value)

def exact_text(value):
    """Only <=3-place terminating fixtures; never emulate C# rounding."""
    value=Fraction(value);d=value.denominator;twos=fives=0
    while d%2==0:twos+=1;d//=2
    while d%5==0:fives+=1;d//=5
    places=max(twos,fives)
    if value<0 or d!=1 or places>3:raise ValueError('Nonnegative terminating <=3-place fixtures only; no formatting/rounding oracle')
    if not places:return str(value.numerator)
    n=value.numerator*(10**places//value.denominator)
    return (str(n//10**places)+'.'+str(n%10**places).zfill(places)).rstrip('0').rstrip('.')

def checked_state(state):
    if not isinstance(state,dict)or set(state)!={'property','height','width','qty','net_text'}:raise ValueError('Exact inert dialog-state schema required')
    if type(state['property'])is not int or state['property']not in(2,3,4):raise ValueError('Only properties2..4, not serial or other branches')
    for k in('height','width','qty','net_text'):number(state[k])
    return copy.deepcopy(state)

def state(prop=2,height='2',width='10',qty='3',net='20'):
    return checked_state(dict(property=prop,height=height,width=width,qty=qty,net_text=net))

def calc(state,internal_update=False):
    out=checked_state(state)
    if type(internal_update)is not bool:raise ValueError('Exact bool internal guard required')
    if internal_update:return dict(state=out,suppressed_nested_call=True,application_executed=False)
    p=out['property'];h,w,q,n=(number(out[k])for k in('height','width','qty','net_text'))
    if p==2:
        if w<=0 or q<=0:h=n=Fraction(0)
        else:
            ratio=n/w
            h=ratio if h.denominator==1 else Fraction(-(-ratio.numerator//ratio.denominator))
            n=h*w*q
        out['height']=exact_text(h)
    elif p==3:n=h*w*q
    else:n=(2*h+2*w)*q
    out['net_text']=exact_text(n)
    return dict(state=out,suppressed_nested_call=False,application_executed=False)

def modal(state,accepted):
    out=checked_state(state)
    if accepted is not None and type(accepted)is not bool:raise ValueError('Supplied bool-or-None modal outcome only')
    return dict(accepted=accepted,field_net=out['net_text']if accepted is True else'0',state=out,
      insert_handler_supplied_as_executed=(accepted is True),application_executed=False)

def item(prop=3):
    if type(prop)is not int:raise ValueError('Exact integer property required')
    return dict(ref='line-A',property=prop,qty='6',detail_qty='6',fill_value='3',height='2',width='3',description='original')

def project(original,supplied_modal,detail_present=True):
    keys={'ref','property','qty','detail_qty','fill_value','height','width','description'}
    if not isinstance(original,dict)or set(original)!=keys or not isinstance(original['ref'],str)or not original['ref']or type(original['property'])is not int or not isinstance(original['description'],str):
        raise ValueError('Exact inert item schema/reference required')
    for k in('qty','detail_qty','fill_value','height','width'):number(original[k])
    if type(detail_present)is not bool:raise ValueError('Exact detail guard required')
    out=copy.deepcopy(original)
    if not detail_present:return dict(item=out,projection_performed=False,unmodelled_other_branch=False,application_executed=False)
    if original['property']not in(2,3,4):return dict(item=out,projection_performed=False,unmodelled_other_branch=True,application_executed=False)
    if not isinstance(supplied_modal,dict)or set(supplied_modal)!={'accepted','field_net','state','insert_handler_supplied_as_executed','application_executed'}:
        raise ValueError('Exact supplied modal schema required')
    st=checked_state(supplied_modal['state']);accepted=supplied_modal['accepted']
    if accepted is not None and type(accepted)is not bool:raise ValueError('Exact bool-or-None outcome required')
    if type(supplied_modal['insert_handler_supplied_as_executed'])is not bool or supplied_modal['insert_handler_supplied_as_executed']is not(accepted is True)or supplied_modal['application_executed']is not False:
        raise ValueError('Supplied modal metadata cannot claim execution or contradict confirmation')
    field=supplied_modal['field_net'];number(field)
    if original['property']!=st['property']or field!=(st['net_text']if accepted is True else'0'):raise ValueError('Fresh-dialog scalar field/property must match supplied branch/insert outcome')
    out['qty']=out['detail_qty']=field
    out['description']='height:'+st['height']+';width:'+st['width']+';qty:'+st['qty']
    if out['property']==2:out['fill_value']=st['height']
    else:out.update(fill_value='0',height=st['height'],width=st['width'])
    return dict(item=out,projection_performed=True,unmodelled_other_branch=False,
       caller_ignores_supplied_dialog_outcome=True,application_executed=False)

def append_on_normal_loader_return(prefix,projected):
    if not isinstance(prefix,list)or any(not isinstance(x,str)or not x for x in prefix)or len(set(prefix))!=len(prefix):raise ValueError('Distinct supplied prefix references only')
    if not isinstance(projected,dict)or projected.get('projection_performed')is not True or projected.get('application_executed')is not False:raise ValueError('Supplied local projection required')
    ref=projected['item']['ref']
    if ref in prefix:raise ValueError('New supplied line reference must be distinct')
    return dict(refs=list(prefix)+[ref],appended_qty=projected['item']['qty'],successful_lookup_and_normal_loader_return_supplied=True,application_executed=False)

def build():
    source={};reads=[]
    for path,spans in SOURCE_SLICES.items():
        raw=(ROOT/path).read_bytes();lines=raw.decode('utf-8').splitlines(keepends=True);source[path]=lines
        for start,end in spans:
            if not 1<=start<=end<=len(lines):raise ValueError('Invalid bounded source read')
            reads.append(dict(path=path,start=start,end=end,encoding='strict-utf-8',utf8_BOM_present=raw.startswith(b'\xef\xbb\xbf'),source_sha256=hashlib.sha256(raw).hexdigest(),selected_text_utf8_sha256=hashlib.sha256(''.join(lines[start-1:end]).encode()).hexdigest(),whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True,whole_local_file_selected=(start==1 and end==len(lines))))
    def text(path,a,b):
        if not any(lo<=a<=b<=hi for lo,hi in SOURCE_SLICES[path]):raise ValueError('Observation outside declared slices')
        return ''.join(source[path][a-1:b])
    def ev(*parts):return ';'.join(path+':'+str(a)+'-'+str(b)for path,a,b in parts)
    pc=P+'frmItemProperties.xaml.cs';px=P+'frmItemProperties.xaml';ic=C+'ItemOper.cs';cc=C+'ItemOpercontract.cs'
    cancel=ev((pc,14,26),(pc,302,308),(ic,587,655),(px,263,279))
    packing=ev((pc,123,193),(pc,214,251),(pc,280,297),(px,239,245),(px,263,270))
    guards=ev((ic,587,601),(pc,123,193),(pc,104,109))
    source_ev=ev((ic,549,574),(ic,1181,1188),(P+'frmItems.xaml.cs',911,931),(P+'frmItems.xaml.cs',985,991),(P+'frmItems.xaml',497,511))
    controls=ev((P+'frmInvSale.xaml.cs',1068,1093),(P+'frmInvSale.xaml',650,663),(P+'frmInvSale.xaml',882,888),(P+'frmInvInputOutput.xaml.cs',1146,1195),(P+'frmInvInputOutput.xaml',722,739))
    overload=ev((cc,1171,1192),(cc,1195,1329),(cc,1367,1417))
    illustrations=[]
    def alg(root,title,result,ok,evidence,limit):
        illustrations.append(dict(id=f'ALG7B25-{len(illustrations)+1:02d}',finding_ids=root,title=title,result=result,illustration_assertions_passed=bool(ok),source_application_executed=False,evidence=evidence,limit=limit))
    s=state(3,'2','10','3','60');r=project(item(3),modal(s,False));alg('P7-151','False normal return projects fresh scalar zero',r,r['item']['qty']==r['item']['detail_qty']=='0'and r['item']['description']!='original',cancel,'Supplied false normal return, not observed ShowDialog/Close; in-memory assignments only, no saved loss.')
    r=project(item(2),modal(state(),None));alg('P7-151','Null normal return is also ungated',r,r['item']['qty']=='0',cancel,'A supplied nontrue outcome is not an assertion of which WPF close gesture returns null or false.')
    r=project(item(3),modal(s,True));alg('P7-151','Confirmed insert positive control copies the scalar',r,r['item']['qty']=='60'and r['item']['height']=='2',cancel,'Local positive control; no dimensions/unit/financial policy or operational acceptance.')
    r=project(item(3),None,False);alg('P7-151','No-detail early-return control',r,not r['projection_performed']and r['item']==item(3),guards,'No-detail helper exit only; external DTO collection/null contract not executed.')
    r=project(item(5),None);alg('P4-029','Serial branch explicitly not modelled as a no-op',r,r['unmodelled_other_branch']and not r['projection_performed'],guards,'Serial cancellation already029; unchanged inert input is NOT acceptance or source claim about serial mutation.')
    m=modal(s,False);r=dict(textbox=s['net_text'],scalar=m['field_net']);alg('P7-151','Visible net text is not the public NetQnty field',r,r==dict(textbox='60',scalar='0'),cancel,'Text changes and Calc do not set public scalar; only supplied Insert would. No UI render observed.')
    r=append_on_normal_loader_return(['line-X'],project(item(3),modal(s,False)));alg('P7-151','Successful loader normal return can append the projected zero',r,r['refs']==['line-X','line-A']and r['appended_qty']=='0',cancel+';'+source_ev,'Only source order after successful lookup/normal LoadItemInf return is modelled; no SQL/catch/stock/save acceptance or certainty of final surviving row.')
    r=project(item(2),modal(state(),True));alg('P7-151','Packing confirmation copies FillValue rather than geometric fields',r,r['item']['fill_value']=='2'and r['item']['height']==item(2)['height'],cancel,'Local projection structure, not a validated packing/rounding formula.')
    first=calc(state());second=calc(first['state']);r=dict(first=first,second=second);alg('P7-152','Sequential packing calls feed60 into180 without new business input',r,first['state']['net_text']=='60'and second['state']['net_text']=='180',packing,'Exact integer supplied state and two sequential calls; NOT automatic WPF event order/count or a saved/financial amount.')
    st=state(qty='1');a=calc(st);b=calc(a['state']);r=dict(first=a,second=b);alg('P7-152','Quantity-one idempotence control',r,a['state']==b['state']and a['state']['net_text']=='20',packing,'Control limits feedback; does not validate all packing semantics.')
    r=calc(state(width='0'));alg('P7-152','Zero width has explicit zero guard',r,r['state']['net_text']==r['state']['height']=='0',packing,'Supplied guard only; source allows broader parse domain not emulated.')
    r=calc(state(qty='0'));alg('P7-152','Zero quantity has explicit zero guard',r,r['state']['net_text']==r['state']['height']=='0',packing,'No divide-by-zero failure inferred for this guard.')
    a=calc(state(3));b=calc(a['state']);r=dict(first=a,second=b);alg('P7-152','Area formula recomputes from unchanged dimensions',r,a['state']==b['state']and a['state']['net_text']=='60',packing,'Source property3 contrast, not agreement with a business dimensional contract.')
    a=calc(state(4));b=calc(a['state']);r=dict(first=a,second=b);alg('P7-152','Linear-perimeter formula is a sequential-call control',r,a['state']==b['state']and a['state']['net_text']=='72',packing,'Formula labelled meter in source; no claim that perimeter is the correct domain policy.')
    st=state();r=calc(st,True);alg('P7-152','Internal-update guard suppresses nested invocation only',r,r['state']==st and r['suppressed_nested_call'],packing+';'+guards,'The bool is supplied; synchronous event reentrancy and dispatcher scheduling never executed.')
    st=state(height='2.5',net='21',qty='2');r=calc(st);alg('P7-152','Fractional previous height selects the existing ceiling branch',r,r['state']['height']=='3'and r['state']['net_text']=='60',packing,'Exact terminating rational control of the conditional, not .NET Math.Ceiling/formatting or a newly invented rounding policy; same152, not third finding.')
    lexical=[]
    def lex(root,title,ok,evidence,limit):lexical.append(dict(id=f'ST7B25-{len(lexical)+1:02d}',finding_ids=root,title=title,documented_text_observation_matches=bool(ok),source_application_executed=False,evidence=evidence,limit=limit))
    t=lambda a,b:text(pc,a,b);i=lambda a,b:text(ic,a,b);c=lambda a,b:text(cc,a,b);x=lambda a,b:text(px,a,b)
    lex('P7-151','Fresh scalar zero is assigned only in constructor and Insert',len(re.findall(r'\bNetQnty\s*=',t(1,318)))==2 and 'NetQnty = 0.0;'in t(22,26),cancel,'Whole local code-behind read, not all external reflection/subclass/global behavior.')
    lex('P7-152','Loaded/selection paths invoke mode and calculation','Loaded="frmItemProperties_Load"'in x(1,16)and 'ApplyPropertyMode();'in t(33,66)and 'Calc();'in t(33,66)and 'Calc();'in t(310,314),ev((pc,33,79),(pc,310,314),(px,1,16)),'Literal calls/wiring only; initial-event count/order not simulated.')
    lex('P7-152','Packing makes net textbox editable despite XAML read-only default','txtNetQnty.IsReadOnly = !isPacking;'in t(72,79)and 'IsReadOnly="True"'in x(263,270),ev((pc,72,79),(px,263,270)),'Selected code changes the property; no rendering or user edit observed.')
    lex('P7-152','Quantity change, lost focus and Enter each call Calc','TextChanged="txtQty_TextChanged"'in x(239,245)and 'LostFocus="txtQty_Leave"'in x(239,245)and 'KeyDown="txtQty_KeyDown"'in x(239,245)and all('Calc();'in t(a,b)for a,b in((218,224),(243,246),(279,286))),packing,'Multiple declared event sites, not a claim every gesture triggers all or a specific number/order.')
    lex('P7-152','Net lost-focus and Enter call Calc while its TextChanged is empty','LostFocus="txtNetQnty_Leave"'in x(263,270)and 'KeyDown="txtNetQnty_KeyDown"'in x(263,270)and 'Calc();'in t(248,251)and 'Calc();'in t(289,297)and 'Calc();'not in t(222,225),packing,'Sequential-invocation possibility only; callbacks not executed.')
    lex('P7-152','Internal-update bool resets in finally, not a persistent idempotence key','if (_isInternalUpdate)'in t(123,130)and '_isInternalUpdate = true;'in t(129,140)and 'finally'in t(187,193)and '_isInternalUpdate = false;'in t(187,193),packing,'Source bool guard, no measured race/reentrancy assertion.')
    z=t(140,175);lex('P7-152','Packing reads output text, divides, multiplies quantity and writes it back','ParseNumber(txtNetQnty.Text, 0)'in z and 'heightValue = netQntyValue / widthValue;'in z and 'netQntyValue = heightValue * widthValue * qtyValue;'in z and 'txtNetQnty.Text = FormatNumber(netQntyValue);'in z,packing,'Integer fixture avoids culture/float/rounding; existing ceiling policy remains unresolved.')
    lex('P7-152','Area and linear branches overwrite net from dimensions','netQntyValue = heightValue * widthValue * qtyValue;'in t(173,177)and '((2.0 * heightValue) + (2.0 * widthValue)) * qtyValue;'in t(178,182),packing,'Contrasting equations, not correctness acceptance for property labels or units.')
    z=t(302,307);lex('P7-151','Only Insert captures the public scalar before true and Close',z.index('NetQnty = ParseNumber')<z.index('DialogResult = true')<z.index('Close();')and 'Click="btnInsert_Click"'in x(274,279),cancel+';'+ev((px,274,279)),'Handler order only, no modal result/Close call executed.')
    z=i(622,655);lex('P7-151','Main helper ignores ShowDialog return before description and quantity','frmItemProperties2.ShowDialog();'in z and 'DialogResult'not in z and 'if (frmItemProperties2'not in z and 'newItem.Description = description;'in z,cancel,'Absence scoped to this projection; normal dialog return supplied, not all close behavior.')
    lex('P7-151','Item and first detail both receive the public scalar',i(637,654).count('frmItemProperties2.NetQnty')==4 and 'firstDetail.FillValue ='in i(637,654)and 'firstDetail.ItemHeight ='in i(637,654),cancel,'Local assignments, not external DTO setter/subscriber or persistence acceptance.')
    lex('P7-151','No details/null-first/unsupported property guard the chosen branch','if (newItem.InvoiceItemDetails.Count <= 0) return;'in i(587,601)and 'if (firstDetail == null) return;'in i(587,601)and 'itemProp >= 2 && itemProp <= 4'in i(587,601),guards,'Other properties outside chosen branch are NOT asserted to be no-op; serial029 remains.')
    lex('P7-151;P7-152','Detail property and FillRatio come from source; product UI stores code2 packing','detail.FillRatio = ToDouble(dt.Rows[0]["FillValue"]);'in i(549,574)and 'LoadItemDetails(invo, ref newItem);'in i(549,574)and 'if (propIdx == 2)'in text(P+'frmItems.xaml.cs',911,931)and '<ComboBoxItem>تعبئة</ComboBoxItem>'in text(P+'frmItems.xaml',497,511)and '@FillValue'in text(P+'frmItems.xaml.cs',985,991),source_ev,'SQL/schema/value uniqueness and deployed UI not executed or certified; width positive is a supplied fixture.')
    z=i(1181,1188);lex('P7-151','Main loader appends after LoadItemInf without a dialog outcome',z.index('LoadItemInf(invo, ref newItem);')<z.index('invo.InvoiceItems.Add(newItem);'),source_ev,'Source order only; no assertion about all subsequent stock checks, totals, removals or saving.')
    z=c(1393,1417);lex('P7-151','InvoiceDGV helper homologue is distinct from no-dialog Invoicecontract loader','propForm.ShowDialog();'in z and 'DialogResult'not in z and 'NewItem.ItemQuantity = propForm.NetQnty;'in z and 'LoadItemDetails('not in c(1195,1260)and 'LoadItemDetails(Invo, ref NewItem);'in c(1262,1329),overload,'Same151 cause not new/extended; class name does NOT establish that actual contract entry reaches this InvoiceDGV overload.')
    lex('H7B25-03','Direct editor reachability is explicitly limited, not assumed','ItemOper.LoadItemDetails(Invoic, ref item);'in text(P+'frmInvSale.xaml.cs',1068,1093)and 'Visibility="Collapsed"'in text(P+'frmInvSale.xaml',882,888)and 'return "";'in text(P+'frmInvInputOutput.xaml.cs',1190,1195)and 'MouseDoubleClick="GridControl1_MouseDoubleClick"'in text(P+'frmInvInputOutput.xaml',722,739),controls,'Sale Description hidden by default; layout visibility/SortMemberPath require contract. Input/output helper returns empty, so Description branch not asserted reachable by supplied column. No new missing-feature finding.')
    errors=[r['id']for r in illustrations if r['illustration_assertions_passed']is not True]+[r['id']for r in lexical if r['documented_text_observation_matches']is not True]
    return dict(audit_reference_date_utc='2026-11-16',source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',entry_checkout='45a2a504db4f82927a286ce425f21a82bcee7a84',application_code_imported_or_executed=False,dotnet_wpf_sql_or_excel_executed=False,application_remediation_performed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,B_R4i_bounded_not_whole7B_closure=True,unresolved_external_contracts_and_explicit_splits_retained=True,selected_paths_strict_utf8_decode=True,all_callers_or_external_DTOs_body_reviewed=False,actual_WPF_event_order_or_count_claimed=False,financial_or_packing_policy_invented=False,Invoicecontract_and_InvoiceDGV_overloads_kept_distinct=True,prior_serial029_and_import144_picker148_not_recounted_or_extended=True,retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),illustration_count=len(illustrations),lexical_check_count=len(lexical),illustrations=illustrations,static_lexical_contract_checks=lexical,bounded_source_reads_not_semantic_coverage=reads,selected_source_paths=10,whole_local_dialog_files_selected=2,source_read_slice_count=len(reads),limit='318-line dialog code-behind and313-line XAML locally complete, other paths bounded;23 reads/10paths not all callers/callgraph/capability census/455FE.151 ungated normal-return projection from fresh scalar0,152 output-input feedback on two sequential exact integer calls60->180. No actual modal close, WPF schedule/count, .NET parser/formatter/rounding, SQL/SDK DTO behavior, finance/stock/save/output/operational acceptance. InvoiceDGV homologue not contract support claim; hidden sale Description and empty input/output column helper constrain direct editor routes. Two roots only, zero extensions, retained potential014/132/145 and020/021/barriers.7B/7 partial,R4j/B26 proposed,7C unstarted,8 unauthorized here; independent repairs not merged or presumed started/synchronized.',errors=errors)

if __name__=='__main__':
    result=build();print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(1 if result['errors']else 0)
