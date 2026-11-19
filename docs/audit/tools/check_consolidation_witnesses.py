#!/usr/bin/env python3
"""B17 R4a: inert source observations and independent hand-model illustrations.

Not an ERP/C#/SQL/VB/WPF interpreter, not financial acceptance. No application
imports, build, external templates, Office/COM, shell/printing/export, real data,
remediation or operational measurement. All historical archives are read-only.
"""
from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
F, C = 'SmartAuditERP/Form_WPF/', 'SmartAuditERP/Class/'
D, DX = F+'frmTaxInvDetails.xaml.cs', F+'frmTaxInvDetails.xaml'
IO, PR = C+'InvoiceOper.cs', C+'Print.cs'
LIMIT = ('نموذج يدوي مستقل بأسماء وأعداد افتراضية؛ ليس ترجمة/تنفيذ المصدر أو قبول ضريبي/مالي. '
         'يفترض صفوفاً مؤهلة وقراءة ناجحة؛ لا يثبت نشر schema أو حدوث الخلل في الإنتاج. '
         '7B/7 جزئيتان؛7C لم تبدأ؛8 غير مأذونة. لا معالجة أو قياس.')
LEX_LIMIT = ('تطابق/غياب نص في شرائح معلنة فقط، لا AST دلالي أو كل callgraph أو نتيجة build/SQL/WPF/REPX. '
             'وجود DTO أو DDL أو Apply لا يثبت عقد نشر أو تفويضاً أو قبولاً.')


def ref(*slices):
    return ';'.join(f'{p}:{a}-{b}' for p, a, b in slices)


def no_sub_membership(flag, mode, records):
    """Independent state-only hand model of the described guards, NOT C#.

    Not the VAT/money calculator; no InvoiceObj, DB, date parsing or lookup.
    Inputs are already eligible, successfully read zero/positive-tax records.
    """
    included = []
    for key, tax in records:
        selected_tax = 0
        if mode == 'without':
            if tax == 0:
                flag = False
        elif mode == 'with':
            if tax > 0:
                selected_tax = tax
        elif mode == 'all':
            if tax == 0:
                flag = False
            selected_tax = tax
        else:
            raise ValueError('Unsupported synthetic mode')
        if mode == 'with' and selected_tax == 0:
            continue
        if not flag and mode == 'with':
            continue
        if flag and mode == 'without':
            continue
        included.append(key)
    return flag, included


def independent_membership(mode, records):
    return [key for key, tax in records if mode == 'all' or (mode == 'with' and tax > 0) or (mode == 'without' and tax == 0)]


class Witness:
    def __init__(self):
        self.alg, self.lex, self.errors, self.reads = [], [], [], {}

    def text(self, path, start, end):
        raw = (ROOT/path).read_bytes()
        try:
            lines = raw.decode('utf-8-sig').splitlines()
        except UnicodeDecodeError:
            lines = raw.decode('cp1256', errors='replace').splitlines()
        if not 1 <= start <= end <= len(lines):
            raise ValueError('Out of bounded source: '+path)
        text = '\n'.join(lines[start-1:end])
        self.reads[path, start, end] = dict(path=path, start=start, end=end,
            selected_text_sha256=hashlib.sha256(text.encode()).hexdigest())
        return text

    def illustration(self, title, roots, evidence, condition, details):
        n = len(self.alg)+1
        if not condition:
            self.errors.append(f'ALG{n} independent illustration mismatch')
        self.alg.append(dict(id=f'ALG7B17-{n:02d}', title=title, finding_ids=roots,
            evidence=evidence, illustration_assertions_passed=bool(condition), details=details,
            source_application_executed=False, limit=LIMIT))

    def lexical(self, title, roots, checks, absent=(), condition=True):
        ok, slices = bool(condition), []
        for path, a, b, tokens in checks:
            text = self.text(path, a, b)
            slices.append((path, a, b))
            ok = all(token in text for token in tokens) and ok
        for path, a, b, tokens in absent:
            text = self.text(path, a, b)
            slices.append((path, a, b))
            ok = all(token not in text for token in tokens) and ok
        n = len(self.lex)+1
        if not ok:
            self.errors.append(f'ST{n} bounded text observation mismatch')
        self.lex.append(dict(id=f'ST7B17-{n:02d}', title=title, finding_ids=roots,
            evidence=ref(*dict.fromkeys(slices)), documented_text_observation_matches=ok,
            source_application_executed=False, limit=LEX_LIMIT))


def main():
    w = Witness()
    T, Z = [('T', 15)], [('Z', 0)]
    base = ref((D,38,45),(D,208,217),(D,280,310),(D,318,338),(D,442,511),(D,619,624))
    cold = no_sub_membership(True, 'with', T)
    seed = no_sub_membership(True, 'without', Z)
    warm = no_sub_membership(seed[0], 'with', T)
    w.illustration('cold with-VAT شاهد إدراج T', 'P7-128', base,
        cold == (True,['T']) and independent_membership('with',T)==['T'],
        dict(initial_flag=True, mode='with', records=T, local=cold[1], independent=['T']))
    w.illustration('warm after no-VAT يسقط نفس T', 'P7-128', base,
        seed==(False,['Z']) and warm==(False,[]) and cold[1]!=warm[1],
        dict(seed=seed, local=warm[1], independent=['T'], main_sub_tables_empty=True))
    forward = no_sub_membership(True,'without',Z+T)
    reverse = no_sub_membership(True,'without',T+Z)
    w.illustration('أهلية no-VAT تتغير بترتيب صفين أيضاً', 'P7-128', ref((D,442,511)),
        forward==(False,['Z','T']) and reverse==(False,['Z']) and independent_membership('without',Z+T)==['Z'],
        dict(local_Z_then_T=forward[1], local_T_then_Z=reverse[1], independent=['Z'],
             note='أهلية فقط؛ لا ادعاء أن مبالغ T المنشورة سليمة أو أن هذه معادلة VAT كاملة.'))
    # The main early return precedes the reset: an empty sub-table cannot heal it.
    unchanged_flag = seed[0]
    w.illustration('main early-return لا يمس العلم false', 'P7-128', ref((D,318,338),(D,442,511)),
        no_sub_membership(unchanged_flag,'with',T)[1]==[],
        dict(main_sub_table_empty=True, flag_after_early_return=unchanged_flag, local=[]))
    w.illustration('وجود main-row ذي بنود يعيد true كشاهد مقابل', 'P7-128', ref((D,318,338),(D,442,511)),
        no_sub_membership(True,'with',T)[1]==['T'] and warm[1]==[],
        dict(main_with_nonempty_sub_table_resets_flag=True, local=['T'], same_T_not_always_omitted=True))
    all_seed = no_sub_membership(True,'all',Z)
    positive_after_zero = no_sub_membership(True,'with',Z+T)
    w.illustration('all-VAT قد يورث false؛ zero في with وحده لا يفعل', 'P7-128', ref((D,463,486)),
        all_seed[0] is False and no_sub_membership(all_seed[0],'with',T)[1]==[] and positive_after_zero==(True,['T']),
        dict(all_seed_flag=all_seed[0], warm_after_all=[], cold_with_zero_then_T=positive_after_zero[1]))
    units, barcodes = [('other','X')], []
    local_cross_join = [(u,b) for u in units for b in barcodes if u[1]=='X' or b[1]=='X']
    reverse_join = [(u,b) for u in [] for b in [('other','X')]]
    w.illustration('crossjoin فارغ مع duplicate في أي جهة', 'P7-036', ref((F+'frmMultiBarcode.xaml.cs',75,149)),
        local_cross_join==[] and reverse_join==[] and any(code=='X' for _,code in units),
        dict(local_cartesian_match_count=0, independent_exists=True, deployed_constraint_not_tested=True))
    w.illustration('رمز عبوة مع سعر أساس مستقل', 'P7-037', ref((F+'frmPrintBarcode.xaml.cs',215,245),(F+'frmPrintBarcode.xaml.cs',337,354),(C+'Common.cs',560,578),(F+'frmItemsBarcode.xaml.cs',281,309)),
        10 != 120 and 'PACK-X'=='PACK-X',
        dict(label_barcode='PACK-X', hypothetical_base_price=10, hypothetical_unit_price=120,
             described_local_base_price=10, policy_for_example='label unit is pack', no_render_or_business_export=True))
    fraction_prefix = '19.999'.split('.')[1][:2]
    reference = str(Decimal('19.999').quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))
    w.illustration('قص أول رقمين مقابل سياسة مثال معلنة', 'P7-034', ref((IO,550,575),(PR,737,750)),
        fraction_prefix=='99' and reference=='20.00',
        dict(explicit_hypothetical_policy='two decimals HALF_UP for this illustration only',
             input_text='19.999', local_fraction_prefix=fraction_prefix, reference_numeric_text=reference,
             actual_VB_culture_or_words_not_executed=True))
    w.illustration('تفرع اسم العملة code4 مقابل شاهد code2', 'P7-035', ref((IO,987,1066),(IO,1098,1159)),
        'ريال'!='Dirham' and 'Dollar'=='Dollar',
        dict(code4_arabic_fallback_major='ريال', code4_english_major='Dirham',
             code2_both_currency_family='Dollar/Cent', enum_identity_or_legal_policy_not_inferred=True))
    w.lexical('field/reset/ShowInvs لا يعيدان IsVAT عند بدء الطلب','P7-128',
        [(D,38,45,('IsVAT        = true',)),(D,208,217,('invoiceRows.Clear();','ResetSummaries();')),
         (D,619,624,('NetBeforVat',))],[(D,208,217,('IsVAT',)),(D,619,624,('IsVAT',))])
    w.lexical('استدعاء main يسبق no-sub وخيارات UI في النافذة ذاتها','P7-128',
        [(D,280,310,('ProcessInvoiceRow(mainTable, i, invoiceObj);','if (Invtype == 1)','ProcessPurchasesWithoutSubs(')),
         (D,741,744,('ShowInvs();',)),(DX,226,248,('rbAllVat','rbWithVAT','rbNoVAT')),
         (DX,276,282,('Click="btnShow_Click"',)),(F+'frmTaxRptPeriod.xaml.cs',868,887,('frm.Invtype = 1;','frm.ShowInvs();'))],
        condition=w.text(D,280,310).index('ProcessInvoiceRow(')<w.text(D,280,310).index('ProcessPurchasesWithoutSubs('))
    main_text = w.text(D,318,338)
    w.lexical('return إذا خلا subTable يسبق إعادةtrue','P7-128',
        [(D,318,338,('if (subTable.Rows.Count <= 0) return;','IsVAT = true;'))],
        condition=main_text.index('return;')<main_text.index('IsVAT = true;'))
    w.lexical('no-sub يضعfalse ولا يعيدtrue قبل guard','P7-128',
        [(D,442,486,('NOT IN (SELECT InvGlobalID FROM Inv_Sub)','if (tax == 0) { IsVAT = false;',
                       'if (tax > 0) { InvSum = total;','if (!IsVAT && rbWithVAT.IsChecked == true) continue;'))],
        [(D,442,511,('IsVAT = true;',))])
    dispatch=w.text(D,789,876)
    w.lexical('حد dispatch الستة مقابل Income/Android وزر كلصف','P7-061;H7B17-03',
        [(D,568,613,('ReceiptType=10','DgvInvType1    = ""','DgvInvGlobalID = ""')),
         (D,660,670,('invType == 20','مبيع أندرويد')),(D,789,876,('row.DgvInvType == "مصروفات"','ReceiptType=9','InvGlobalID=N')),
         (DX,474,486,('Tag="{Binding}"','Click="BtnDetails_Click"'))],
        [(D,789,876,('invType1 == 20','ReceiptType=10'))],condition=sum(dispatch.count(f'invType1 == {n}')for n in(1,2,3))==6)
    w.lexical('مقدار عربي من نص محلي وقص الكسر ومستهلكان','P7-034',
        [(IO,550,575,('Strings.Split(Conversions.ToString(givenNumber), ".")','Substring(0, 2)')),
         (PR,737,750,('ToArabicLetter(Conversions.ToDouble(invoiceData.Net), Inv.Currency)',)),
         (PR,1051,1065,('ToArabicLetter(Inv.Net, Inv.Currency)',))])
    w.lexical('case العملة والتفقيط الافتراضي في سند محدد','P7-035',
        [(IO,987,1066,('Conversions.ToString(2)','ريال','هللة')),(IO,1098,1159,('Conversions.ToString(4)','Dirham','Fils')),
         (F+'frmEmpSalaryAddSub.xaml.cs',975,982,('InvoiceOper.ToArabicLetter(','Convert.ToDouble(txtVal.Text))'))])
    w.lexical('crossjoin فحص مستقل عن insert parameters','P7-036',
        [(F+'frmMultiBarcode.xaml.cs',75,149,('from ItemUnits,Itembarcodes where','if (!IsValidBarcode(txtBarcode.Text))','values(@ItemId,@barcode)')),
         (F+'frmItems.xaml.cs',1879,1889,('new frmMultiBarcode()',)),
         ('SmartAuditERP/Properties/Resources.resx',410,432,('CREATE TABLE [dbo].[Itembarcodes]','CREATE TABLE [dbo].[ItemUnits]'))])
    w.lexical('رد unitId لا يدخل سعرالملصق؛ شاهد IU.sale','P7-037',
        [(F+'frmPrintBarcode.xaml.cs',215,245,('ref itemId, ref unitId, ref itemPrice','ItemBarcode   = barcode.Trim()','Common.GetItemPrice(itemId)')),
         (F+'frmPrintBarcode.xaml.cs',337,354,('Price      = item.ItemSalePrice.ToString()','Barcode    = item.ItemBarcode')),
         (C+'Common.cs',560,578,('select isnull(sale_price,0)',)),
         (C+'ItemOper.cs',1920,1948,('unitId = ToInt(dt.Rows[0]["unit"])','itemPrice = default;')),
         (F+'frmItemsBarcode.xaml.cs',281,309,('IU.sale','row["sale"]'))])
    w.lexical('متصلان محددان وvoid/copies/PDF لا كلcallgraph','P7-029;P7-030;P7-031;H7B17-02',
        [(F+'frmSalesInvoice.xaml.cs',1199,1264,('DELETE FROM ItemSerialNo','print.BindToData(inv)')),
         (F+'frmInvSale.xaml.cs',2065,2124,('Microsoft Print to PDF','print.BindToData(inv)')),
         (PR,148,221,('public void Printing(','PrintNo > 0','xtraReport.Print();','catch (Exception'))])
    result=dict(phase='7B17-partial-static-consolidation',application_code_imported_or_executed=False,
        application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,erp_runtime_tests_executed=0,
        sql_or_external_service_tests_executed=0,illustration_count=len(w.alg),
        static_lexical_contract_check_count=len(w.lex),historical_metadata_rows_not_unique_features=455,
        historical_metadata_aggregation_not_new_source_review=True,B_R4a_not_whole7B_closure=True,
        unresolved_external_contracts_and_explicit_splits_retained=True,phase7C_started=False,
        phase8_authorized_or_started=False,supplied_DDL_not_deployed_schema_certification=True,
        illustrations=w.alg,static_lexical_contract_checks=w.lex,
        bounded_source_reads_not_semantic_coverage=list(w.reads.values()),
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,
            local_cost=10,reference_cost=120,archive_rewritten=False),errors=w.errors,limit=LIMIT)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return bool(w.errors)


if __name__=='__main__':
    sys.exit(main())
