#!/usr/bin/env python3
"""7B18/R4b inert lexical witnesses and independent request illustrations.

No app imports/build/C#/SQL/WPF/REPX/Office/COM/interpreters/providers/devices,
real data, remediation or operational measurement. Discovery searches original
C# text excluding bin/obj: NOT an AST/callgraph or a feature coverage census.
"""
from __future__ import annotations
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[3]
F='SmartAuditERP/Form_WPF/'
D=F+'frmRptItemsActivityDetailed.xaml.cs';DX=F+'frmRptItemsActivityDetailed.xaml'
LIMIT=('نموذج مستقل لعضوية طلب افتراضي، لا تنفيذ C#/SQL/WPF أو حساب مالي. '
       'يفترض نجاح المصادر وتهيئة lookup وبيانات مؤهلة؛ أثر selected-index مشروط بغياب تطابق. '
       'لا يثبت حدوث إنتاج أو تجاوز ACL أو دقة كل تقرير.7B/7 جزئيتان؛7C لم تبدأ؛8 غير مأذونة.')
LEX_LIMIT=('ملاحظات نصية محدودة، لا AST دلالي أو كل callgraph أو إثبات ترتيب Loaded في التشغيل. '
           'وجود مسار أو Apply لا يثبت الوصول المنشور أو grants أو سلامة الحفظ/القالب.')


def decoded(path):
    raw=path.read_bytes()
    try:return raw.decode('utf-8-sig')
    except UnicodeDecodeError:return raw.decode('cp1256')


def refs(*slices):return ';'.join(f'{p}:{a}-{b}'for p,a,b in slices)


def split_arguments(text):
    """Balanced inert tokens only; not a C# expression parser or evaluator."""
    args=[];begin=0;depth=0;quote=None;escaped=False
    for i,c in enumerate(text):
        if quote:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c==quote:quote=None
        elif c in('\"',"'"):quote=c
        elif c in '([{':depth+=1
        elif c in ')]}':
            depth-=1
            if depth<0:raise ValueError('Unbalanced inert arguments')
        elif c==','and depth==0:args.append(re.sub(r'\s+',' ',text[begin:i].strip()));begin=i+1
    if quote or depth:raise ValueError('Unbalanced inert arguments')
    args.append(re.sub(r'\s+',' ',text[begin:].strip()))
    if any(not x for x in args):raise ValueError('Empty inert argument')
    return args


def extract_calls(text):
    """The literal pattern object.LastProcess(...), not indirect call reachability."""
    result=[]
    for m in re.finditer(r'\b(\w+)\.LastProcess\s*\(',text):
        depth=1;quote=None;escaped=False;i=m.end()
        while i<len(text)and depth:
            c=text[i]
            if quote:
                if escaped:escaped=False
                elif c=='\\':escaped=True
                elif c==quote:quote=None
            elif c in('\"',"'"):quote=c
            elif c=='(':depth+=1
            elif c==')':depth-=1
            i+=1
        if depth:raise ValueError('Unclosed literal call')
        raw=text[m.start():i]
        result.append(dict(call_line_start=text.count('\n',0,m.start())+1,
            call_line_end=text.count('\n',0,i-1)+1,receiver=m.group(1),
            lexical_args=split_arguments(text[m.end():i-1]),
            call_text_sha256=hashlib.sha256(raw.encode()).hexdigest()))
    return result


def discover_calls():
    inventory=list(csv.DictReader(io.StringIO((ROOT/'docs/audit/evidence/inventory.csv').read_bytes().decode(),newline='')))
    paths=sorted(r['path']for r in inventory if r['path'].endswith('.cs')and not any(x in r['path'].split('/')for x in('bin','obj')))
    calls=[]
    for path in paths:
        calls += [dict(source_path=path,**x)for x in extract_calls(decoded(ROOT/path))]
    return calls,len(paths)


def party_filter(party_id,forwarded_kind,parties):
    """Independent identity/lookup hand model, not .NET selection semantics.

    The caller has already chosen a positive ID from its own declared list.
    If the receiver lookup cannot select that ID, its guarded filter is absent.
    """
    if forwarded_kind not in(1,2):raise ValueError('Synthetic kind must be1 or2')
    if party_id<=0:return None
    return party_id if any(pid==party_id and kind in(forwarded_kind,3)for pid,kind in parties)else None


def first_key(records,party=None,store=None,descending=False):
    # records: hypothetical (key,partyId,storeId,timeOrdinal), already eligible.
    eligible=[r for r in records if(party is None or r[1]==party)and(store is None or r[2]==store)]
    eligible.sort(key=lambda r:r[3],reverse=descending)
    return eligible[0][0]if eligible else None


class Witness:
    def __init__(self):self.alg=[];self.lex=[];self.reads={};self.errors=[]
    def text(self,p,a,b):
        lines=decoded(ROOT/p).splitlines()
        if not 1<=a<=b<=len(lines):raise ValueError('Bounded source range')
        s='\n'.join(lines[a-1:b]);self.reads[p,a,b]=dict(path=p,start=a,end=b,selected_text_sha256=hashlib.sha256(s.encode()).hexdigest());return s
    def illustration(self,title,roots,evidence,ok,details):
        n=len(self.alg)+1
        if not ok:self.errors.append(f'ALG7B18-{n:02d}')
        self.alg.append(dict(id=f'ALG7B18-{n:02d}',title=title,finding_ids=roots,evidence=evidence,
            illustration_assertions_passed=bool(ok),details=details,source_application_executed=False,limit=LIMIT))
    def lexical(self,title,roots,checks,absent=(),condition=True):
        ok=bool(condition);slices=[]
        for p,a,b,tokens in checks:
            t=self.text(p,a,b);ok=ok and all(x in t for x in tokens);slices.append((p,a,b))
        for p,a,b,tokens in absent:
            t=self.text(p,a,b);ok=ok and all(x not in t for x in tokens);slices.append((p,a,b))
        n=len(self.lex)+1
        if not ok:self.errors.append(f'ST7B18-{n:02d}')
        self.lex.append(dict(id=f'ST7B18-{n:02d}',title=title,finding_ids=roots,evidence=refs(*dict.fromkeys(slices)),
            documented_text_observation_matches=ok,source_application_executed=False,limit=LEX_LIMIT))


def main():
    w=Witness();parties=[(11,1),(22,2),(33,3)]
    rows=[('other',11,5,1),('target',22,5,2)]
    base=refs((D,169,188),(D,209,235),(D,268,275),(D,695,715))
    wrong=party_filter(22,1,parties);right=party_filter(22,2,parties)
    w.illustration('مورد2 يرسلkind1 فيفقد قيد الطرف عند عدم التطابق','P7-129',refs((F+'frmSalePurch.xaml.cs',275,316),(F+'frmSalePurch.xaml.cs',2242,2254))+';'+base,
        wrong is None and first_key(rows,wrong)=='other'and first_key(rows,right)=='target',dict(parent_id=22,parent_kind=2,forwarded_kind=1,selected_lookup_match=False,local='other',reference='target'))
    w.illustration('تصحيحkind وحده يعيد قيد الطرف في نموذج129','P7-129',base,
        right==22 and first_key(rows,right)=='target',dict(positive_id_unchanged=22,correct_kind=2,filter=right,not_all_amounts_certified=True))
    w.illustration('الطرف المشترك3 يخفي عدم اتساقkind','P7-129',base,
        party_filter(33,1,parties)==party_filter(33,2,parties)==33,dict(shared_party=33,kind3_in_both_lists=True,not_every_request_fails=True))
    posrows=[('supplier',22,5,1),('customer',11,5,2)]
    w.illustration('POS يرسلkind2 لطرف عميل1','P7-129',refs((F+'frmInvPOS.xaml.cs',1230,1241),(F+'frmInvPOS.xaml.cs',2658,2680))+';'+base,
        party_filter(11,2,parties)is None and first_key(posrows,None)=='supplier'and first_key(posrows,11)=='customer',dict(parent_customer=11,forwarded_kind=2,local='supplier',reference='customer'))
    w.illustration('InputOutput5 عميل لكنconst2؛4/14 مورد كشاهد مقابل','P7-129',refs((F+'frmInvInputOutput.xaml.cs',253,273),(F+'frmInvInputOutput.xaml.cs',1294,1308))+';'+base,
        party_filter(11,2,parties)is None and party_filter(22,2,parties)==22,dict(invtype5_expected_kind=1,invtype4_14_expected_kind=2,forwarded_kind=2))
    omitted=party_filter(-1,1,parties)
    w.illustration('أمر العميل يمرر-1 ولو كان الطرف موجباً في الأب','P7-130',refs((F+'frmInvInOutput.xaml',551,559),(F+'frmInvInOutput.xaml.cs',2607,2623))+';'+base,
        omitted is None and first_key(posrows,omitted)=='supplier'and first_key(posrows,11)=='customer',dict(parent_positive_party=11,forwarded_id=-1,local='supplier',reference='customer'))
    w.illustration('تغييرkind لا يستعيدID المحذوف130','P7-130',base,
        party_filter(-1,1,parties)is None and party_filter(-1,2,parties)is None and party_filter(11,1,parties)==11,dict(kind_only_fix_insufficient=True,id_must_be_forwarded=True))
    w.illustration('المتصل الصحيحInvPurch يرسلkind2 للمورد','P7-129',refs((F+'frmInvPurch.xaml.cs',231,258),(F+'frmInvPurch.xaml.cs',1152,1167))+';'+base,
        party_filter(22,2,parties)==22,dict(counterexample='matching positive supplier ID and kind2',warehouse_and_sort_roots_still_open=True))
    stores=[('outside-old',22,9,1),('inside',22,5,2),('outside-new',22,8,3)]
    w.illustration('إصلاحPartyKind لا يصلحall-store122','P7-122;P7-129',refs((D,209,235),(D,253,260),(DX,288,296)),
        first_key(stores,22,None)=='outside-old'and first_key(stores,22,5)=='inside'and first_key(stores,22,None,True)=='outside-new',dict(party_filter_fixed=22,store_argument=5,local_store_filter=None,reference='inside'))
    times=[('old',22,5,1),('new',22,5,2)]
    w.illustration('بعد تثبيت النطاق يبقىASC مقابلlatest059','P7-059',refs((D,261,266),(D,289,304)),
        first_key(times,22,5)=='old'and first_key(times,22,5,True)=='new',dict(same_party=22,same_store=5,local='old',reference='new',equal_times_not_ordered_by_this_model=True))
    before=dict(item=7,branch=None);after=dict(item=7,branch=1)
    w.illustration('طلب قبل التحميل ليس لقطة UI بعدها؛ دون تفسير.NET','P7-045;H7B18-03',refs((D,55,95),(D,275,283),(F+'frmInvPurch.xaml.cs',1123,1135)),
        before!=after,dict(before_load=before,after_load_ui=after,loaded_order_and_datebox_defaults_not_runtime_tested=True))
    w.illustration('sentinel-1 مشروع لأمر المادة العام لا لأمر الطرف','P7-130;H7B18-03',refs((F+'frmInvInOutput.xaml',551,559),(F+'frmInvInOutput.xaml.cs',2589,2623)),
        first_key(posrows,None)=='supplier'and first_key(posrows,11)=='customer',dict(all_party_request='general item command',selected_party_request='client-labelled command',not_every_minus1_is_a_defect=True))
    w.lexical('موردا SalePurch/PurchInv مقابل kind1','P7-129',[(F+'frmSalePurch.xaml.cs',275,316,('int custType = 2;','type={custType} or type=3')),(F+'frmSalePurch.xaml.cs',2242,2254,('Convert.ToInt32(cmbClient.SelectedValue), 1)',)),(F+'frmPurchInv.xaml.cs',215,242,('int type = 2;','LoadData.Customers(type)')),(F+'frmPurchInv.xaml.cs',2433,2446,('frm.LastProcess(itemId, storeId, custId, 1)',))])
    w.lexical('POS يحفظ هوية عميل ثم يمرر kind2','P7-129',[(F+'frmInvPOS.xaml.cs',2658,2680,('frm.Type = 1;','Invoic.Customer = frm.ClientId;')),(F+'frmInvPOS.xaml.cs',1230,1241,('Invoic.Customer, 2)',)),(F+'frmSrchClient.xaml.cs',96,125,('type={Type} OR type=3','Type == 1'))])
    w.lexical('المحررات العامة تختار المورد عند InvType1','P7-129',[(F+'frmcontract.xaml.cs',424,448,('if (InvType == 1)','customerType = 2;')),(F+'frmcontract.xaml.cs',1573,1595,('SafeGetSelectedValue<int>(cmbClient), 1)',)),(F+'frmSalesInvoice.xaml.cs',296,325,('(InvType == 1) ? 2 : 1',)),(F+'frmSalesInvoice.xaml.cs',2540,2555,('Convert.ToInt32(cmbClient.SelectedValue), 1)',)),(F+'frmInvSale.xaml.cs',489,511,('if (InvType == 1)','type = 2;')),(F+'frmInvSale.xaml.cs',1213,1227,('custId, 1)',))])
    w.lexical('InputOutput ينقل kind2 حتى خارج نمط المورد','P7-129',[(F+'frmInvInputOutput.xaml.cs',253,273,('if (InvType == 4 || InvType == 14)','int type = 1;','type = 2;')),(F+'frmInvInputOutput.xaml.cs',1294,1308,('custId, 2)',))])
    w.lexical('InvPurch شاهد نقل kind2 المطابق','P7-129',[(F+'frmInvPurch.xaml.cs',231,258,('int type = 2;','LoadData.Customers(type)')),(F+'frmInvPurch.xaml.cs',1152,1167,('GetSelectedId(this.cmbClient), 2)',))])
    w.lexical('معالج label العميل الفعلي ليس المستنتج من الاسم','P7-130',[(F+'frmInvInOutput.xaml',554,559,('Header="📊 آخر حركة للعميل"','Click="StripLastItem_Click"')),(F+'frmInvInOutput.xaml.cs',2607,2623,('private void StripLastItem_Click','reportWindow.LastProcess(row.ItemId, row.StoreId, -1, 1)'))],[(F+'frmInvInOutput.xaml.cs',2607,2623,('cmbClient','Invoic.Customer'))])
    w.lexical('الطرف الموجب والقائمة والحارس في المستقبل','P7-129;P7-130',[(D,169,188,('WHERE (type={clientType} OR type=3)','cmbClients.SelectedIndex      = -1;')),(D,209,235,('if (clientId > 0)','if (clientType == 1)','chkSuplier.IsChecked = true;','cmbClients.SelectedValue = clientId;')),(D,268,275,('cmbClients.SelectedIndex > -1','Inv.cust_id={cmbClients.SelectedValue}')),(D,695,715,('if (!IsLoaded) return;','loadclients(1);','loadclients(2);')),(DX,390,412,('GroupName="ClientGroup"','IsChecked="True"'))])
    w.lexical('مخزن API تحت علم كل لا يعطل122','P7-122',[(D,209,235,('cmbSafes.SelectedValue = storeId;',)),(D,253,260,('if (chkAll.IsChecked != true','Inv_sub.store={cmbSafes.SelectedValue}')),(DX,288,296,('IsChecked="True"',))],[(D,209,235,('chkAll.IsChecked = false',))])
    w.lexical('TOP1 مع ASC يبقى059','P7-059',[(D,261,266,('condTop = " top (1) "',)),(D,289,304,('ORDER BY inv.date ASC',))])
    pre=[('frmcontract',1532,1550,'form'),('frmSalesInvoice',2527,2539,'frm'),('frmSalePurch',2228,2240,'form'),('frmInventoryTransfer',1442,1461,'frm'),('frmInvSale',1185,1197,'frm'),('frmInvPurch',1123,1135,'frm'),('frmInvPOS',1197,1211,'frm'),('frmInvInputOutput',1263,1276,'dlg')]
    ordered=all(w.text(F+n+'.xaml.cs',a,b).index(var+'.ShowResult();')<w.text(F+n+'.xaml.cs',a,b).index(var+'.ShowDialog();')for n,a,b,var in pre)
    w.lexical('ثمانية مداخل تفصيلية تستعلم قبل ShowDialog','P7-045;H7B18-03',[(F+n+'.xaml.cs',a,b,(var+'.ShowResult();',var+'.ShowDialog();'))for n,a,b,var in pre]+[(D,82,95,('LoadSafes();','LoadBranches();'))],condition=ordered)
    w.lexical('الفتح التفصيلي برقم محلي مقابل GlobalID في القائمة','P7-061',[(D,1011,1045,('OpenInvoiceByType(invType, invNoStr)','id={invNo}')),(F+'frmRptInventory.xaml.cs',490,508,('invTxt.InvGlobalID','switch (cmbType.SelectedIndex)')),(F+'frmRptInventory.xaml.cs',545,639,('InvGlobalID=N\'{globalId}\'','private void OpenSafeAdjust')),(F+'frmRptInventory.xaml',453,489,('Tag="{Binding InvGlobalID}"','Tag="{Binding}"'))])
    calls,scanned=discover_calls()
    w.lexical('19 موضعاً نصياً مباشراً في10 ملفات، لا كل callgraph','H7B18-06',[(F+'frmInventoryTransfer.xaml.cs',1358,1381,('MkMenu("📈 آخر حركة", ItemLastActivity)',)),(F+'frmInvInOutput.xaml.cs',2589,2623,('reportWindow.LastProcess(',))],condition=len(calls)==19 and len({r['source_path']for r in calls})==10 and scanned==477 and all(len(x['lexical_args'])==4 for x in calls))
    result=dict(phase='7B18-partial-static-direct-caller-requests',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        phase7C_started=False,phase8_authorized_or_started=False,illustration_count=len(w.alg),static_lexical_contract_check_count=len(w.lex),
        illustrations=w.alg,static_lexical_contract_checks=w.lex,bounded_source_reads_not_semantic_coverage=list(w.reads.values()),
        direct_literal_discovery=dict(original_CSharp_files_excluding_bin_obj_scanned_not_body_reviews=scanned,literal_calls=calls,literal_calls_count=len(calls),source_path_count=len({r['source_path']for r in calls}),not_complete_callgraph_or_feature_census=True),
        B_R4b_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False),errors=w.errors,limit=LIMIT)
    print(json.dumps(result,ensure_ascii=False,indent=2));return bool(w.errors)


if __name__=='__main__':sys.exit(main())
