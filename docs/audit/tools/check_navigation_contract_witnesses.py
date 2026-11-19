#!/usr/bin/env python3
"""Read-only documentary models and bounded lexical observations for7B19/R4c.

Never import/compile/execute application/C#/WPF/SQL/DTO/provider/printer or real
business data. Manually transcribed pure models below are illustrations, NOT
.NET runtime semantics, a SQL parser or deployment acceptance. Decimal values
avoid midpoint cases and do not certify binary double behavior. Literal scans
cover ONLY declared two-parent slices, NOT a complete callgraph/capability census.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import re
from decimal import Decimal, ROUND_HALF_EVEN
from datetime import datetime

ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/';C='SmartAuditERP/Class/';RES='SmartAuditERP/Properties/Resources.resx'
READ_SPECS={
 'detail-dispatch':(F+'frmRptItemsActivityDetailed.xaml.cs',1011,1191),
 'inventory-dispatch':(F+'frmRptInventory.xaml.cs',490,635),
 'detail-row':(F+'frmRptItemsActivityDetailed.xaml.cs',285,309),
 'detail-button':(F+'frmRptItemsActivityDetailed.xaml',708,720),
 'inventory-button':(F+'frmRptInventory.xaml',454,486),
 'sale-hook':(F+'frmInvSale.xaml',1,16),
 'sale-constructor':(F+'frmInvSale.xaml.cs',67,94),
 'sale-loaded':(F+'frmInvSale.xaml.cs',123,235),
 'sale-reset':(F+'frmInvSale.xaml.cs',1546,1610),
 'sale-navigate':(F+'frmInvSale.xaml.cs',1643,1661),
 'sale-dirty':(F+'frmInvSale.xaml.cs',1663,1682),
 'sale-save':(F+'frmInvSale.xaml.cs',1860,1912),
 'sale-buttons':(F+'frmInvSale.xaml.cs',2537,2570),
 'purchase-hook':(F+'frmInvPurch.xaml',1,16),
 'purchase-loaded':(F+'frmInvPurch.xaml.cs',97,160),
 'purchase-reset':(F+'frmInvPurch.xaml.cs',350,407),
 'purchase-navigate':(F+'frmInvPurch.xaml.cs',481,504),
 'purchase-toolbar':(F+'frmInvPurch.xaml.cs',506,546),
 'purchase-save':(F+'frmInvPurch.xaml.cs',1196,1335),
 'purchase-dirty':(F+'frmInvPurch.xaml.cs',1571,1589),
 'pos-hook':(F+'frmInvPOS.xaml',1,16),
 'pos-loaded':(F+'frmInvPOS.xaml.cs',210,270),
 'pos-reset':(F+'frmInvPOS.xaml.cs',512,553),
 'pos-dirty':(F+'frmInvPOS.xaml.cs',621,641),
 'pos-binding':(F+'frmInvPOS.xaml.cs',1009,1028),
 'pos-navigate':(F+'frmInvPOS.xaml.cs',1861,1881),
 'pos-pay-guard':(F+'frmInvPOS.xaml.cs',1901,1974),
 'pos-paybill':(F+'frmInvPOS.xaml.cs',2012,2056),
 'pos-save':(F+'frmInvPOS.xaml.cs',2170,2211),
 'io-hook':(F+'frmInvInputOutput.xaml',1,16),
 'io-loaded':(F+'frmInvInputOutput.xaml.cs',94,130),
 'io-reset':(F+'frmInvInputOutput.xaml.cs',162,201),
 'io-navigate':(F+'frmInvInputOutput.xaml.cs',483,500),
 'io-toolbar-save':(F+'frmInvInputOutput.xaml.cs',502,618),
 'io-dirty':(F+'frmInvInputOutput.xaml.cs',690,710),
 'transfer-hook':(F+'frmInventoryTransfer.xaml',1,18),
 'transfer-loaded':(F+'frmInventoryTransfer.xaml.cs',126,160),
 'transfer-reset':(F+'frmInventoryTransfer.xaml.cs',286,328),
 'transfer-navigate':(F+'frmInventoryTransfer.xaml.cs',402,451),
 'transfer-dirty':(F+'frmInventoryTransfer.xaml.cs',523,544),
 'transfer-save':(F+'frmInventoryTransfer.xaml.cs',797,1029),
 'transfer-buttons':(F+'frmInventoryTransfer.xaml.cs',1520,1563),
 'production-hook':(F+'frmProductionOrder.xaml',1,16),
 'production-loaded':(F+'frmProductionOrder.xaml.cs',100,124),
 'production-edit':(F+'frmProductionOrder.xaml.cs',510,578),
 'production-navigate':(F+'frmProductionOrder.xaml.cs',854,884),
 'production-read':(F+'frmProductionOrder.xaml.cs',884,1022),
 'production-toolbar':(F+'frmProductionOrder.xaml.cs',1026,1070),
 'production-identity':(F+'frmProductionOrder.xaml.cs',1274,1335),
 'production-params':(F+'frmProductionOrder.xaml.cs',1352,1423),
 'production-save':(F+'frmProductionOrder.xaml.cs',1425,1497),
 'production-class':(F+'frmProductionOrder.xaml.cs',1907,2022),
 'production-grid':(F+'frmProductionOrder.xaml',487,511),
 'safe-hook':(F+'frmSafeAdjust.xaml',1,16),
 'safe-loaded':(F+'frmSafeAdjust.xaml.cs',113,151),
 'safe-navigate':(F+'frmSafeAdjust.xaml.cs',1096,1103),
 'safe-read':(F+'frmSafeAdjust.xaml.cs',1105,1206),
 'safe-save':(F+'frmSafeAdjust.xaml.cs',908,979),
 'safe-buttons':(F+'frmSafeAdjust.xaml.cs',1368,1418),
 'binder':(C+'InvoiceOper.cs',3219,3281),
 'binder-end':(C+'InvoiceOper.cs',3496,3509),
 'mapping-date':(C+'InvoiceOper.cs',4186,4248),
 'writer-date':(C+'InvoiceOper.cs',1497,1535),
 'queries':(C+'StoredQueries.cs',6,10),
 'period':(C+'Common.cs',1271,1301),
 'edit-UI':(C+'Common.cs',1435,1490),
 'schema-inv':(RES,954,1017),
 'schema-adjust':(RES,1692,1726),
}


def text(path):
    raw=(ROOT/path).read_bytes()
    try:return raw.decode('utf-8-sig')
    except UnicodeDecodeError:return raw.decode('cp1256')


def evidence(*names):
    return ';'.join(f'{p}:{a}-{b}'for p,a,b in(READ_SPECS[n]for n in names))


def extract_literal_navigations(source,source_path,start_line=1):
    """Balanced delimiters/quoted strings for these inert literal call tokens.

    Does not resolve comments/conditional compilation/receivers/reflection or C#
    syntax; no evaluation. Only `f.Navigate` / `frm.Navigate` bounded scan.
    """
    result=[]
    for m in re.finditer(r'\b(?:f|frm)\.Navigate\s*\(',source):
        i=m.end();depth=1;quote=False;escaped=False
        while i<len(source)and depth:
            ch=source[i]
            if quote:
                if escaped:escaped=False
                elif ch=='\\':escaped=True
                elif ch=='"':quote=False
            elif ch=='"':quote=True
            elif ch=='(':depth+=1
            elif ch==')':depth-=1
            i+=1
        if depth or quote:raise ValueError('Unclosed bounded inert Navigate token')
        call=source[m.start():i]
        result.append(dict(source_path=source_path,call_line_start=start_line+source.count('\n',0,m.start()),
            call_line_end=start_line+source.count('\n',0,i-1),call_text_sha256=hashlib.sha256(call.encode()).hexdigest(),
            inert_argument_expression=source[m.end():i-1].strip()))
    return result


def fields_from_create(fragment,table):
    """Inert bracketed column names in a bounded known CREATE block, not SQL."""
    m=re.search(r'CREATE TABLE \[dbo\]\.\['+re.escape(table)+r'\]\((.*?)(?:CONSTRAINT|\) ON)',fragment,re.S|re.I)
    if not m:raise ValueError('Known bounded CREATE shape not found')
    return sorted(set(re.findall(r'^\s*\[([A-Za-z_][A-Za-z_0-9]*)\]',m[1],re.M)),key=str.casefold)


def after_lifecycle(*,navigate_before_loaded):
    """Illustrative order only; DOES NOT dispatch WPF/events/DTO setters."""
    value=dict(ISNew=True,branch='session',document='new')
    def nav():value.update(ISNew=False,branch='document-branch',document='loaded')
    def reset():value.update(ISNew=True,branch='session',document='loaded')
    if navigate_before_loaded:nav();reset()
    else:reset();nav()
    return value


def production_qty_edit(old,base,equality,new_qty):
    return old if base<=0 else (new_qty*base*equality).quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN)


def production_unit_edit(base,product_equality,product_qty):
    return (product_equality*base*product_qty).quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN)


def rehydrate_component(quantity,price):
    q,p=(x.quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN)for x in(quantity,price))
    return dict(quantity=str(q),price=str(p),total=str((q*p).quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN)))


def pos_save_date(original,now,*,is_new,electronic):
    return now if is_new or not electronic else original


def build():
    reads=[];fragments={};errors=[]
    for name,(path,a,b)in READ_SPECS.items():
        lines=text(path).splitlines();assert 1<=a<=b<=len(lines),(name,a,b,len(lines))
        fragment='\n'.join(lines[a-1:b]);fragments[name]=fragment
        reads.append(dict(name=name,path=path,start=a,end=b,normalized_text_sha256=hashlib.sha256(fragment.encode()).hexdigest(),not_semantic_coverage=True))
    calls=[]
    for name in('detail-dispatch','inventory-dispatch'):
        path,a,_=READ_SPECS[name];calls+=extract_literal_navigations(fragments[name],path,a)
    alg=[];lex=[]
    def model(title,fids,keys,inputs,observed,expected,limit):
        passed=observed==expected
        row=dict(id=f'ALG7B19-{len(alg)+1:02d}',title=title,finding_ids=fids,evidence=evidence(*keys),inputs=inputs,
            observed_illustration=observed,expected_illustration=expected,illustration_assertions_passed=passed,source_application_executed=False,limit=limit)
        alg.append(row)
        if not passed:errors.append(row['id'])
    D=Decimal
    limit='نموذج مستقل منقول يدوياً، لا تنفيذ C#/WPF/SQL أو إثبات حادث نشر/حفظ. القيم اصطناعية ولا تصديق لسياسة دقة أو تحويل خارجية.'
    inv=fields_from_create(fragments['schema-inv'],'Inv');adjust=fields_from_create(fragments['schema-adjust'],'SafesAdjust')
    model('عقد Is_Approved ليس من أعمدة Inv المرفقة','P7-131',('schema-inv','schema-adjust','safe-read'),{'required':'Is_Approved'},
        {'in_Inv':'Is_Approved'in inv,'in_SafesAdjust':'Is_Approved'in adjust},{'in_Inv':False,'in_SafesAdjust':True},limit+' لا نفترض مخطط النشر أو خلو تحديثاته؛ المرفق فقط.')
    model('الترتيب يغير loaded/new في النموذج','P7-132',('detail-dispatch','sale-loaded','sale-reset','binder'),{},
        [after_lifecycle(navigate_before_loaded=x)['ISNew']for x in(True,False)],[True,False],limit+' هذا شرط ترتيب توضيحي، لا قياس Loaded أو إثبات حفظ نسخة جديدة.')
    model('ضبط الهوية وحده لا يحرس Reset المتأخر','P7-132',('inventory-dispatch','transfer-reset','binder'),{},
        [after_lifecycle(navigate_before_loaded=x)['branch']for x in(True,False)],['session','document-branch'],limit)
    model('BaseQty الافتراضية صفر تجعل حدث الكمية يتجاوز المكون','P7-133',('production-read','production-class','production-edit'),{'old':'8','base':'0','eq':'1','new_product_qty':'3'},
        str(production_qty_edit(D('8'),D('0'),D('1'),D('3'))),'8',limit+' الحارس BaseQty>0 يمنع التصفير هنا، لذلك لا نزعم أن حدث الكمية يصفر السطور.')
    model('حدث وحدة المنتج لا يملك حارس BaseQty>0','P7-133',('production-read','production-class','production-edit'),{'base':'0','product_eq':'12','product_qty':'3'},
        str(production_unit_edit(D('0'),D('12'),D('3'))),'0.00',limit+' الفرع مشروط باختيار وحدة ووجود perc؛ لا حفظ ناجح مفترض مع حاجز P4-020.')
    model('المكون المهيأ يظل غير صفري؛ لا كل BOM يفشل','P7-133;P4-022',('production-edit','production-class'),{'base':'2','component_eq':'3','product_qty':'3'},
        str(production_qty_edit(D('8'),D('2'),D('3'),D('3'))),'18.00',limit+' لا يحسم أي معادلة تحويل هي الصحيحة؛ P4-022 باقية.')
    model('تقريب كمية صغيرة عند القراءة يفقدها من الكائن','P7-134',('production-read','production-grid'),{'quantity':'0.004','price':'1000.004'},
        rehydrate_component(D('0.004'),D('1000.004')),{'quantity':'0.00','price':'1000.00','total':'0.00'},limit+' ليس StringFormat وحده؛ لا تعميم سلوك double عند المنتصف.')
    model('تقريب السعر مستقل عن فقد معامل BOM','P7-134',('production-read','production-save'),{'quantity':'2','price':'1.234'},
        rehydrate_component(D('2'),D('1.234')),{'quantity':'2.00','price':'1.23','total':'2.46'},limit+' القيمة الأصلية 2.468؛ العرض المحلي يتغير قبل عقد الحفظ المحجوب.')
    model('قيمة مضبوطة إلى منزلتين شاهد غير متضرر','P7-134',('production-read',),{'quantity':'2.00','price':'1.25'},
        rehydrate_component(D('2.00'),D('1.25')),{'quantity':'2.00','price':'1.25','total':'2.50'},limit)
    old=datetime(2025,12,31,23,59);now=datetime(2026,1,2,12,0)
    model('تعديل POS غير إلكتروني يعيد تاريخ المستند إلى الآن','P7-135',('pos-save','writer-date','queries'),{'original':old.isoformat(),'now':now.isoformat(),'ISNew':False,'electronic':False},
        pos_save_date(old,now,is_new=False,electronic=False).isoformat(),now.isoformat(),limit+' المسار مشروط بالسماح بالحفظ ونجاح الكاتب؛ لم تتغير قاعدة فعلية.')
    model('الموجود الإلكتروني لا يقع في استبدال التاريخ نفسه','P7-135',('pos-save',),{'ISNew':False,'electronic':True},
        pos_save_date(old,now,is_new=False,electronic=True).isoformat(),old.isoformat(),limit+' قد تمنع حراس أخرى التعديل؛ ليس قبولاً ضريبياً.')
    model('تاريخ الفحص/العرض قد يختلف عن تاريخ طلب الكتابة','P7-135;P3-001',('pos-binding','pos-pay-guard','pos-save','period'),{'shown':old.isoformat()},
        old.date()!=pos_save_date(old,now,is_new=False,electronic=False).date(),True,limit+' P3-001 حارس الفترة معروف دائماً true، فلا ندعي اختراق فترة فعالة جديدة.')
    docs=[dict(global_id='A-7',local_no=7,branch='A'),dict(global_id='B-7',local_no=7,branch='B')]
    model('الرقم المحلي لا يميز فرعين؛ مقارنة GlobalID ليست ACL','P7-061',('detail-row','detail-dispatch','inventory-dispatch'),{'documents':docs},
        [len([d for d in docs if d['local_no']==7]),len([d for d in docs if d['global_id']=='B-7'])],[2,1],limit+' لا SQL أو ترتيب أول صف منفذ أو عضو allowed-set مثبت.')
    model('نافذة جديدة لا تثبت فقد مسودة لعدم استدعاء الحارس في Navigate','H7B19-03',('detail-dispatch','inventory-dispatch','sale-dirty','sale-navigate'),{'receiver_created_fresh':True,'unsaved_receiver_state':False},
        bool(True and False),False,limit+' عدم CheckBeforeClear داخل Navigate وحده ليس finding مستقلة؛ المداخل تعرّف new window.')
    def static(title,fids,keys,ok,observation):
        row=dict(id=f'ST7B19-{len(lex)+1:02d}',title=title,finding_ids=fids,evidence=evidence(*keys),observation=observation,
            documented_text_observation_matches=bool(ok),source_application_executed=False,limit='فحص نصي محدود للمقاطع المسماة فقط؛ ليس AST/callgraph أو تنفيذ WPF/SQL أو ACL أو ضمان سلامة نشر أو قراءة كامل الملفات.')
        lex.append(row)
        if not ok:errors.append(row['id'])
    s=fragments
    static('طلب inventorySafeAdjust من Inv وقارئ Is_Approved','P7-131',('inventory-dispatch','safe-read'),
        'AND inv_type=7'in s['inventory-dispatch']and 'FROM Inv WHERE'in s['inventory-dispatch']and'dr["Is_Approved"]'in s['safe-read'],
        'OpenSafeAdjust يمرر SELECT* من Inv؛ ReadData يقرأ Is_Approved قبل SafesAdjust_Sub.')
    static('DDL المرفق يفصل المصدرين','P7-131',('schema-inv','schema-adjust'), 'Is_Approved'not in inv and'Is_Approved'in adjust,
        'غياب Is_Approved من CREATE Inv المرفق، وحضوره في SafesAdjust؛ لا شهادة schema حقيقي.')
    static('helper التفصيلي configure قبل Show في كليهما','P7-132',('detail-dispatch',),
        s['detail-dispatch'].index('configure(form)')<s['detail-dispatch'].index('form.Show()')and s['detail-dispatch'].index('configure(window)')<s['detail-dispatch'].index('window.Show()'),
        'OpenForm و OpenWindow ينفذان lambda/Navigate قبل Show؛ .NET timing غير منفذ.')
    helpers=re.findall(r'private void (Open\w+)\([^\{]+\{(.*?)(?=\n        private|\n        #endregion|\Z)',s['inventory-dispatch'],re.S)
    static('خمسة helpers للمخزون تنشر Show قبل Navigate','H7B19-03',('inventory-dispatch',),
        len(helpers)==5 and all(body.index('frm.Show()')<body.index('frm.Navigate(')for _,body in helpers),
        'مصدر5helpers لايثبت أن Loaded اكتمل عند Navigate ولا اعتماد محرر/حفظ.')
    names=('sale','purchase','pos','io','transfer')
    static('ربط Loaded ونداء reset في خمسة أوراق','P7-132',tuple(n+'-hook'for n in names)+tuple(n+'-loaded'for n in names),
        all('Loaded="'in s[n+'-hook']and'ResetInvoice()'in s[n+'-loaded']for n in names),
        'XAML Loaded و CS ResetInvoice موجودان؛ لا نفترض فشل كل تحميل أو صحة SDK/event-generation.')
    static('المحمل المشترك false/null','H7B19-03',('binder','binder-end'),
        'Invo.ISNew = false'in s['binder']and'Invo = null'in s['binder-end'],
        'BindingInvoice يغير ISNew=false عند الصف، ويستعمل null لغياب الصف أو الاستثناء؛ لا health مفصول مثبت.')
    static('خمسة ResetInvoice تعيد حالة الجديد','P7-132',tuple(n+'-reset'for n in names),
        all(re.search(r'(?:Invoic|_invoic)\.ISNew\s*=\s*true',s[n+'-reset'])and'MainClass.BranchNo'in s[n+'-reset']for n in names),
        'إعادة الجديد والفرع بعد قراءة صف موجود سبب مستقل عن label/localNo في061؛ أثر الواجهة محتمل مشروط.')
    constructor=s['production-read'].split('_itemsSource.Add(new ProductionItemRow',1)[1].split('});',1)[0]
    static('إعادة بناء المكون بلا BaseQty أو UnitEquality','P7-133',('production-read','production-class'),
        'BaseQty ='not in constructor and'UnitEquality ='not in constructor and'private double _baseQty;'in s['production-class']and'private double _unitEquality = 1'in s['production-class'],
        'النوع المحلي يعرف double _baseQty بلا initializer، و equality=1؛ initializer بعد القراءة لا ينقل معامل الوصفة.')
    qty=s['production-edit'].split('private void txtQty_TextChanged',1)[1]
    static('حارس الكمية BaseQty>0 شاهد ضد دعوى التصفير التلقائي','P7-133',('production-edit',),
        'row.BaseQty > 0'in qty and'qty * row.BaseQty * row.UnitEquality'in qty,
        'مع BaseQty0 يتجاوز مكوناً محملاً؛ ليس صفراً من هذا الحدث.')
    unit=s['production-edit'].split('private void txtQty_TextChanged',1)[0]
    static('حدث الوحدة يضرب BaseQty بلا شرطها','P7-133;P4-022',('production-edit',),
        'perc * row.BaseQty * qty'in unit and'row.BaseQty > 0'not in unit and'if (_isLoaded) return'in unit,
        'صفر مشروط بخروج _isLoaded ووجود وحدة/perc؛ الاختلاف عن معادلة كمية ذاتBaseQty موجب يبقى P4-022.')
    static('تقريب qty/price في الكائن لا StringFormat فقط','P7-134',('production-read','production-grid'),
        'Math.Round(Convert.ToDouble(row["val1"]), 2)'in s['production-read']and'Math.Round(Convert.ToDouble(row["exchange_price"]), 2)'in s['production-read']and'Qty = qty'in constructor and'Price = price'in constructor,
        'Math.Round يسبق initializer و Total؛ مصب StringFormat=N2 شيء آخر.')
    static('الحفظ يستهلك row.Qty و row.Price وحاجز المعاملات محفوظ','P7-133;P7-134;P4-020',('production-save','production-params','queries'),
        'Value = row.Qty'in s['production-save']and'Value = row.Price'in s['production-save']and'@TotalWithholdingTax'in s['queries']and'@TotalWithholdingTax'not in s['production-params'],
        'binding مبين لكن الرأس يفتقد معاملة مطلوبة في StoredQueries المرفق؛ لا حفظ خاطئ منفذ أو متجاوز للحاجز.')
    static('POS يبدل التاريخ بعد mapping وقبل حفظه','P7-135',('pos-save','pos-pay-guard','pos-binding','writer-date','queries'),
        s['pos-save'].index('MappingInvoice')<s['pos-save'].index('!EnableE_Invoice && !Invoic.ISNew')<s['pos-save'].index('SaveInvoice(')and'Value = inv.InvDate'in s['writer-date']and'date=@date'in s['queries']and'CheckProiedAcc(txtDate_Value)'in s['pos-pay-guard'],
        'فرع nonElectronic/existing يضع DateTime.Now في invoice.InvDate بينما الفحص/العرض بالقديم؛ لا ادعاء إقفال منشور.')
    navigate_names=('sale','purchase','pos','io','transfer','production','safe')
    static('Navigate في الأوراق المختارة ليس عقد dirty موحداً','H7B19-03',tuple(n+'-navigate'for n in navigate_names)+('sale-dirty','purchase-toolbar','transfer-dirty'),
        all('CheckBeforeClear'not in s[n+'-navigate']for n in navigate_names)and'CheckBeforeClear'in s['purchase-toolbar'],
        'الغياب داخل المقاطع لا يثبت ACL أو فقد مسودة؛ callers ينشئون نوافذ جديدة وبعض toolbar يفحص قبل Navigate.')
    if len(calls)!=19:errors.append('Expected19 bounded literal navigation call tokens')
    return dict(phase='7B19-partial-static-navigation-contracts',illustration_count=len(alg),static_lexical_contract_check_count=len(lex),
        illustrations=alg,static_lexical_contract_checks=lex,bounded_source_reads_not_semantic_coverage=reads,
        navigation_literal_discovery=dict(parent_path_count=2,literal_call_tokens=len(calls),declared_route_instances_not_unique_calls=22,
            leaf_count=7,literal_calls=calls,not_complete_callgraph_or_capability_census=True),
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False),
        B_R4c_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,
        application_code_imported_or_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,errors=errors)


if __name__=='__main__':
    result=build();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errors']))
