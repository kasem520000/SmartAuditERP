#!/usr/bin/env python3
"""B26/R4j inert bulk-product illustrations; NEVER ERP/SQL/WPF/SDK execution.

Supplied Product-shaped values, exact terminating rational fixtures and bounded
literal observations only. No external constructor/DTO defaults, business unit
conversion, monetary rounding, culture, deployed permissions or saved loss oracle.
General apply, price operations and writer PARAMETER plans stay distinct.
"""
from __future__ import annotations
import copy
from fractions import Fraction
import hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
P='SmartAuditERP/Form_WPF/';C='SmartAuditERP/Class/'
SOURCE_SLICES={
 P+'frmEditItems.xaml.cs':[(1,378)],P+'frmEditItems.xaml':[(1,469)],
 P+'frmItemsDir.xaml.cs':[(548,578)],P+'frmItemsDir.xaml':[(218,222),(421,433)],
 C+'EntityOperations.cs':[(632,793)],
 C+'ItemOper.cs':[(549,574),(604,620),(733,811),(2467,2610)],
 P+'frmItems.xaml.cs':[(911,932),(979,991),(2020,2097)],
 P+'frmItems.xaml':[(487,512)],C+'StoredQueries.cs':[(34,36)]}

def number(s):
    if not isinstance(s,str)or len(s)>64 or re.fullmatch(r'(?:0|[1-9]\d*)(?:\.\d+)?',s)is None:raise ValueError('Only supplied nonnegative finite plain decimals, not .NET/culture parsing')
    return Fraction(s)

def exact(s):
    f=Fraction(s);d=f.denominator;a=b=0
    while d%2==0:a+=1;d//=2
    while d%5==0:b+=1;d//=5
    n=max(a,b)
    if f<0 or d!=1 or n>3:raise ValueError('Nonnegative <=3-place terminating fixtures only; no rounding oracle')
    if not n:return str(f.numerator)
    v=f.numerator*(10**n//f.denominator)
    return(f'{v//10**n}.{v%10**n:0{n}d}').rstrip('0').rstrip('.')

def product():
    return dict(id=7,main_unit=1,property=2,packing='6',sale='10',purchase='6',units=[dict(id=1,ratio='1',sale='10',purchase='6'),dict(id=2,ratio='12',sale='120',purchase='72')])

def checked(p):
    if not isinstance(p,dict)or set(p)!={'id','main_unit','property','packing','sale','purchase','units'}:raise ValueError('Exact supplied product schema required')
    if any(type(p[k])is not int or p[k]<0 for k in('id','main_unit','property'))or p['id']==0 or p['main_unit']==0 or p['property']>8:raise ValueError('Exact positive identity/nonnegative property required')
    for k in('packing','sale','purchase'):number(p[k])
    if not isinstance(p['units'],list):raise ValueError('Supplied units list required; no SDK defaults assumed')
    for u in p['units']:
        if not isinstance(u,dict)or set(u)!={'id','ratio','sale','purchase'}or type(u['id'])is not int or u['id']<=0:raise ValueError('Exact supplied unit schema required')
        for k in('ratio','sale','purchase'):number(u[k])
    if len({u['id']for u in p['units']})!=len(p['units']):raise ValueError('Distinct supplied unit IDs; no duplicate-unit policy inferred')
    return copy.deepcopy(p)

def allowed(user_edit,branch_type,sync_type):
    if type(user_edit)is not bool or type(branch_type)is not int or type(sync_type)is not int:raise ValueError('Exact supplied permission/branch guard types required')
    return user_edit and not(branch_type==2 and sync_type>0)

def general(p,property_index=None,packing_input=None,sale=None,purchase=None,unit=None,apply_sale=False,apply_purchase=False,user_edit=True,branch_type=1,sync_type=0):
    out=checked(p)
    if any(type(x)is not bool for x in(apply_sale,apply_purchase)):raise ValueError('Exact bool price flags required')
    if property_index is not None and(type(property_index)is not int or not 0<=property_index<=8):raise ValueError('Explicit property index or None required')
    if unit is not None and(type(unit)is not int or unit<=0):raise ValueError('Explicit positive selected unit or None required')
    if not allowed(user_edit,branch_type,sync_type):return dict(product=out,rejected=True,reason='supplied-guard',application_executed=False)
    if property_index==2 and(packing_input is None or number(packing_input)==0):return dict(product=out,rejected=True,reason='zero-or-empty-packing',application_executed=False)
    for k,s in(('sale',sale),('purchase',purchase)):
        if s is not None:number(s);out[k]=s
    if unit is not None:
        for u in out['units']:
            if u['id']==out['main_unit']:u.update(id=unit,sale=out['sale'],purchase=out['purchase'])
        out['main_unit']=unit
    if property_index is not None:
        out['property']=property_index
        if property_index==2:out['packing']='2'
    return dict(product=out,rejected=False,reason='source-assignment-illustration-only',price_checkboxes_not_consulted=True,application_executed=False)

def price_operation(p,kind,sale=None,purchase=None,apply_sale=False,apply_purchase=False):
    out=checked(p)
    if type(kind)is not int or kind not in(1,2,3,4)or any(type(x)is not bool for x in(apply_sale,apply_purchase)):raise ValueError('Exact command/flag types required')
    def op(current,value):
        c,v=number(current),number(value)
        return exact(v if kind==1 else c+v if kind==2 else c*(1+v/100)if kind==3 else c*(1-v/100))
    for k,s,flag in(('sale',sale,apply_sale),('purchase',purchase,apply_purchase)):
        if flag and s is not None:
            out[k]=op(out[k],s)
            for u in out['units']:u[k]=op(u[k],s)
    return out

def parameter_plan(p):
    p=checked(p)
    return dict(header={'@id':p['id'],'@unit':p['main_unit'],'@ItemProperty':p['property'],'@FillValue':p['packing'],'@sale_price':p['sale'],'@purch_price':p['purchase']},unit_rows=[{'@ItemId':p['id'],'@unit':u['id'],'@perc':u['ratio'],'@sale':u['sale'],'@purch':u['purchase']}for u in p['units']],database_executed=False,commit_success_not_assumed=True)

def selected_price(p,side):
    p=checked(p)
    if side not in('sale','purchase'):raise ValueError('Explicit sale/purchase only')
    row=next((u for u in p['units']if u['id']==p['main_unit']),None)
    return dict(value=row[side]if row else p[side],source='matched-ItemUnits'if row else'Items-fallback',SQL_lookup_supplied_not_executed=True)

def build():
    sources={};reads=[]
    for path,spans in SOURCE_SLICES.items():
        raw=(ROOT/path).read_bytes();lines=raw.decode('utf8').splitlines(keepends=True);sources[path]=lines
        for a,b in spans:
            if not 1<=a<=b<=len(lines):raise ValueError('Invalid bounded read')
            reads.append(dict(path=path,start=a,end=b,encoding='strict-utf-8',source_sha256=hashlib.sha256(raw).hexdigest(),selected_text_utf8_sha256=hashlib.sha256(''.join(lines[a-1:b]).encode()).hexdigest(),whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True,whole_local_file_selected=(a==1 and b==len(lines))))
    def text(path,a,b):
        if not any(lo<=a<=b<=hi for lo,hi in SOURCE_SLICES[path]):raise ValueError('Observation outside selected slices')
        return ''.join(sources[path][a-1:b])
    ec=P+'frmEditItems.xaml.cs';ex=P+'frmEditItems.xaml';ic=C+'ItemOper.cs';eo=C+'EntityOperations.cs';sq=C+'StoredQueries.cs'
    def ev(*args):return';'.join(f'{path}:{a}-{b}'for path,a,b in args)
    packing=ev((ec,172,200),(ec,251,267),(ex,202,266),(eo,678,683),(sq,34,36))
    prices=ev((ec,202,234),(ec,264,267),(ec,293,343),(eo,667,712),(ic,733,811),(ic,2500,2545))
    gate=ev((ec,154,170),(ec,277,297))
    alg=[]
    def add(root,title,result,ok,evidence,limit):alg.append(dict(id=f'ALG7B26-{len(alg)+1:02d}',finding_ids=root,title=title,result=result,illustration_assertions_passed=bool(ok),source_application_executed=False,evidence=evidence,limit=limit))
    for supplied in('12','24'):
        r=general(product(),2,supplied);add('P7-153','Validated packing '+supplied+' becomes constant2',r,r['product']['packing']=='2'and not r['rejected'],packing,'Supplied valid integer input; local mapping and parameter plan, not a SQL commit, unit policy or saved loss.')
    r=general(product(),2,'2');add('P7-153','Input2 is a fixed-point control',r,r['product']['packing']=='2',packing,'Coincidental equality is not acceptance of other inputs or business packing semantics.')
    r=general(product(),2,'0');add('P7-153','Zero packing returns before mutation',r,r['rejected']and r['product']==product(),packing,'Fixture covers plain zero only, not .NET parsing, negative-domain policy, NaN or event behavior.')
    r=general(product());add('P7-153','Unselected property preserves supplied packing',r,r['product']['packing']=='6',packing,'Omitted property selection is distinct from explicitly selecting zero; no external DTO defaults assumed.')
    r=general(product(),3);add('P7-153','Other property leaves packing unchanged locally',r,r['product']['property']==3 and r['product']['packing']=='6',packing,'Branch contrast only, not support or dimensional acceptance for every property.')
    p=general(product(),sale='20')['product'];r=dict(plan=parameter_plan(p),consumer=selected_price(p,'sale'));add('P7-154','General sale edit changes header20 but matched unit stays10',r,r['plan']['header']['@sale_price']=='20'and r['consumer']['value']=='10',prices,'Existing main-unit row, default pricing, normal writer-success path and no customer override supplied; SQL/ERP never executed.')
    p=general(product(),purchase='8')['product'];r=dict(plan=parameter_plan(p),consumer=selected_price(p,'purchase'));add('P7-154','General purchase edit changes header8 but unit stays6',r,r['plan']['header']['@purch_price']=='8'and r['consumer']['value']=='6',prices,'Same154 root for purchase, not another finding or statement of all consumers.')
    r=general(product(),sale='20',purchase='8',apply_sale=False,apply_purchase=False);add('P7-154','General command does not consult price-operation checkboxes',r,r['product']['sale']=='20'and r['product']['units'][0]['sale']=='10'and r['price_checkboxes_not_consulted'],prices,'Documented command-boundary contrast within154; no third unchecked-checkbox defect or assumed user intent.')
    p=general(product(),sale='20',purchase='8',unit=1)['product'];r=parameter_plan(p);add('P7-154','Selecting same main unit opens synchronization control',r,r['header']['@sale_price']==r['unit_rows'][0]['@sale']=='20'and r['unit_rows'][0]['@purch']=='8',prices,'Same-unit control only; remapping units, ratios, duplicate IDs, stock or history conversion not certified.')
    q=product();q['units']=[];p=general(q,sale='20')['product'];r=selected_price(p,'sale');add('P7-154','Missing-unit row falls back to updated header',r,r['value']=='20'and r['source']=='Items-fallback',prices,'No-row fallback source contrast, not a claim a database row is absent or a certification of026 pricing policies.')
    r=price_operation(product(),1,sale='20');add('P7-154','Price-operation checkbox false leaves prices unchanged',r,r==product(),prices,'This is the separate command, not the general footer command; UI gesture not executed.')
    r=price_operation(product(),2,sale='10',apply_sale=True);add('P7-154','Increase command updates scalar and each supplied unit',r,r['sale']==r['units'][0]['sale']=='20'and r['units'][1]['sale']=='130',prices,'Literal arithmetic control, not an endorsed equal increase across different unit ratios.')
    r=price_operation(product(),3,sale='10',apply_sale=True);add('P7-154','Percentage-increase command control',r,r['sale']==r['units'][0]['sale']=='11'and r['units'][1]['sale']=='132',prices,'Exact finite fixture, no monetary/currency/rounding or .NET numeric oracle.')
    r=price_operation(product(),4,sale='10',apply_sale=True);add('P7-154','Percentage-decrease command control',r,r['sale']==r['units'][0]['sale']=='9'and r['units'][1]['sale']=='108',prices,'Does not certify pricing policy, later discounts or taxes.')
    r=general(product(),2,'12',sale='20',user_edit=False);add('H7B26-04','Supplied edit permission blocks the local handler',r,r['rejected']and r['product']==product(),gate,'Local positive guard control, not proof of deployed ACL or all entrypoints; financial/ACL/save barriers remain.')
    lexical=[]
    def lex(root,title,ok,evidence,limit):lexical.append(dict(id=f'ST7B26-{len(lexical)+1:02d}',finding_ids=root,title=title,documented_text_observation_matches=bool(ok),source_application_executed=False,evidence=evidence,limit=limit))
    t=lambda a,b:text(ec,a,b);x=lambda a,b:text(ex,a,b);i=lambda a,b:text(ic,a,b);e=lambda a,b:text(eo,a,b)
    lex('H7B26-03','Directory selected IDs reach the bulk modal','Click="BtnEditItem_Click"'in text(P+'frmItemsDir.xaml',218,222)and 'SelectionMode="Extended"'in text(P+'frmItemsDir.xaml',421,433)and all(s in text(P+'frmItemsDir.xaml.cs',548,578)for s in('GridControl1.SelectedItems','itemId > 0','editForm.itemList = Itemlist;','editForm.ShowDialog();')),ev((P+'frmItemsDir.xaml.cs',548,578),(P+'frmItemsDir.xaml',218,222),(P+'frmItemsDir.xaml',421,433)),'One selected entry, not every caller or actual modal/SQL execution.')
    lex('H7B26-03','Loaded wires footer and four independent price commands',all(s in t(28,67)for s in('Loaded += FrmEditItems_Loaded','WireUpEvents();','btnSave.Click += BtnSave_Click;','ItemOperations(1)','ItemOperations(2)','ItemOperations(3)','ItemOperations(4)')),ev((ec,28,67),(ex,398,469)),'Literal wiring only, not Loaded scheduling/count, rendering or7C lifecycle review.')
    lex('P7-153','Packing choice index2 exposes and validates an input','Content="تعبئة"'in x(202,220)and 'txtFillVal.Visibility = Visibility.Visible;'in t(135,145)and 'double.TryParse(txtFillVal.Text, out double fillVal)'in t(172,194),packing,'Local input route only; .NET parsing and product policy not executed.')
    lex('P7-153','Bulk general apply writes constant2 rather than parsed input','if (itemProperty == 2)'in t(251,261)and 'item.PackingValue = 2.0;'in t(251,261)and 'fillVal'not in t(251,261),packing,'Scoped literal assignment; no claim a stored database was changed.')
    lex('P7-153','Single-product counterparts project user packing input','out fillVal'in text(P+'frmItems.xaml.cs',911,932)and '.Value = fillVal;'in text(P+'frmItems.xaml.cs',979,991)and 'PackingValue = ParseDouble(txtFillVal.Text)'in text(P+'frmItems.xaml.cs',2020,2097),ev((P+'frmItems.xaml.cs',911,932),(P+'frmItems.xaml.cs',979,991),(P+'frmItems.xaml.cs',2020,2097),(P+'frmItems.xaml',487,512)),'Control source mapping, not approval of every single-product save or conversion.')
    lex('P7-153;P7-154','Reader hydrates packing and header and per-unit prices',all(s in i(2467,2610)for s in('product.PackingValue = ToDouble(row["FillValue"]);','product.SalePrice = ToDouble(row["sale_price"]);','product.PurchPrice = ToDouble(row["purch_price"]);','SalePrice = ToDouble(uRow["sale"]),','PurchasePrice = ToDouble(uRow["purch"]),')),ev((ic,2467,2610)),'Source producer fields only; successful data rows supplied, no full DTO/default/BOM/health contract acceptance.')
    lex('P7-154','General scalar price edit is outside the selected-unit gate',t(202,234).index('item.SalePrice =')<t(202,234).index('if (cmbUnit.SelectedIndex != -1)')and 'chkSalePrice'not in t(202,234)and 'chkPurchPrice'not in t(202,234),prices,'General path distinct from four price-operation commands; no unchecked-input finding added.')
    lex('P7-154','Only selected-unit gate synchronizes units in general apply','if (unit.UnitId == item.MainUnit)'in t(221,234)and 'unit.SalePrice = item.SalePrice;'in t(221,234)and 'unit.PurchasePrice = item.PurchPrice;'in t(221,234)and 'cmbUnit.EditValue = null;'in t(95,116),prices,'With unselected unit, existing unit values persist locally; changing main-unit identity/ratio needs a separate contract.')
    lex('P7-154','Price-operation command checks flags and updates each unit',all(s in t(293,343)for s in('chkSalePrice.IsChecked == true','chkPurchPrice.IsChecked == true','foreach (var unit in item.ProductUnits)','unit.SalePrice = unitSale;','unit.PurchasePrice = unitPurch;')),prices,'Positive contrast only; not endorsing all-unit arithmetic or business price policy.')
    lex('P7-153;P7-154','Writer binds header packing and prices independently of units',all(s in e(667,712)for s in('.Value = Product.PurchPrice;','.Value = Product.SalePrice;','.Value = Product.PackingValue;','.Value = productUnit.PurchasePrice;','.Value = productUnit.SalePrice;','delete  from ItemUnits')),ev((eo,632,715)),'SQL command construction, not execution, transaction acceptance or stored-loss measurement.')
    lex('P7-153;P7-154','Attached item SQL maps those parameters to matching columns',all(s in text(sq,34,36)for s in('FillValue=@FillValue','sale_price=@sale_price','purch_price=@purch_price','where id=@id')),ev((sq,34,36)),'Attached SQL text only, no schema/grants/deployed trigger or provider execution.')
    lex('P7-154','Existing unit reader uses per-unit price before fallback','newItem.ItemPrice = ToDouble(row["sale"]);'in i(733,771)and 'newItem.ItemPrice = ToDouble(row["purch"]);'in i(733,771)and 'return;'in i(755,771)and 'sale_price as sale'in i(773,811),ev((ic,733,811)),'Default pricing and no customer override supplied to isolate154 from existing026 and142; not whole pricing review.')
    lex('P7-153','Packing value reaches detail ratio and dialog width','detail.FillRatio = ToDouble(dt.Rows[0]["FillValue"]);'in i(549,574)and 'firstDetail.FillRatio.ToString();'in i(604,620),ev((ic,549,574),(ic,604,620)),'Source-local downstream link, not reopening151/152 or approving net calculation/persistence.')
    lex('H7B26-04','Both command handlers retain local edit and branch guards',t(1,378).count('if (!User.EditItemInfo)')==2 and t(1,378).count('if (Sync.BranchType == 2 && Sync.SyncType > 0)')==2,gate,'No new ACL defect/closure from a positive local guard; deployed ACL/SQL grants unresolved.')
    lex('H7B26-04','Writer normal path commits and catch rolls back with finally close',all(s in e(632,793)for s in('sqlTransaction.Commit();','sqlTransaction.Rollback();','finally','sqlConnection.Close();','return result;')),ev((eo,632,793)),'No SQL/commit run or atomicity certification; empty/early-false/resource/concurrency contracts remain open.')
    lex('P7-154','Price operations retain four arithmetic branches',all(s in t(348,364)for s in('1 => val','2 => currentValue + val','3 => currentValue *','4 => currentValue -')),ev((ec,348,364)),'Arithmetic control only, not monetary/ratio/precision policy or .NET execution.')
    errors=[r['id']for r in alg if r['illustration_assertions_passed']is not True]+[r['id']for r in lexical if r['documented_text_observation_matches']is not True]
    return dict(audit_reference_date_utc='2026-11-16',source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',entry_checkout='dd38f97e844dc60ea64ae00fa40ef588e49752d7',application_code_imported_or_executed=False,dotnet_wpf_sql_or_excel_executed=False,application_remediation_performed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,B_R4j_bounded_not_whole7B_closure=True,unresolved_external_contracts_and_explicit_splits_retained=True,selected_paths_strict_utf8_decode=True,all_callers_or_external_DTOs_body_reviewed=False,actual_WPF_event_order_or_count_claimed=False,financial_or_unit_conversion_policy_invented=False,external_DTO_constructor_defaults_assumed=False,database_commit_or_saved_loss_claimed=False,prior026_142_151_152_not_recounted_or_extended=True,retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),illustration_count=len(alg),lexical_check_count=len(lexical),illustrations=alg,static_lexical_contract_checks=lexical,bounded_source_reads_not_semantic_coverage=reads,selected_source_paths=len(SOURCE_SLICES),whole_local_editor_files_selected=2,source_read_slice_count=len(reads),limit='Locally whole bulk editor378C#/469XAML plus15 selected reads/9paths not all product features/callers/SDK DTOs/census/455FE.153 constant2 mapping after supplied valid packing input;154 general header prices differ from preexisting main-unit prices until unit gate opens, writer binds each independently and matched-unit consumer retains old price. Exact supplied integer/terminating fixtures not .NET culture/precision/event/runtime/SQL/commit/save/stock/financial policy. No third checkbox/zero-field/BOM/DTO-default root;026/142/151/152 and sync021 retained.7B/7 partial,R4k/B27 proposed,7C unstarted,8 unauthorized; repairs independent not presumed started/synchronized.',errors=errors)

if __name__=='__main__':
    r=build();print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(1 if r['errors']else 0)
