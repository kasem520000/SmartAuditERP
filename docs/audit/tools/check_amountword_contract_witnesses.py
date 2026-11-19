#!/usr/bin/env python3
"""Read bounded text and compute inert/manual 7B21 illustrations, NEVER ERP.

No application imports, C#/VB/.NET format/parse evaluation, DB/provider/template,
printer, external services, real business data, remediation or acceptance.
ASCII strings and supplied parse outcomes below are NOT .NET conformance tests.
Qualified-token discovery masks comments/strings; not a semantic callgraph,
reflection/delegate/alias census or a review of every scanned C# body.
"""
from __future__ import annotations
import csv
from decimal import Decimal, ROUND_HALF_EVEN
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
AUDIT=ROOT/'docs/audit'
C='SmartAuditERP/Class/'
F='SmartAuditERP/Form_WPF/'


def sha(data):return hashlib.sha256(data).hexdigest()


def mask_noncode(text):
    """Length/line preserving mask, including ordinary/verbatim strings/chars.

    Interpolated strings are deliberately masked as whole strings: expressions
    inside them are outside discovery, not proof that no call exists there.
    """
    out=list(text);i=0;n=len(text)
    def blank(a,b):
        for k in range(a,b):
            if out[k]not in'\r\n':out[k]=' '
    while i<n:
        start=i
        if text.startswith('//',i):
            end=text.find('\n',i+2);i=n if end<0 else end;blank(start,i)
        elif text.startswith('/*',i):
            end=text.find('*/',i+2)
            if end<0:raise ValueError('Unterminated comment in documentary tokenizer')
            i=end+2;blank(start,i)
        elif text.startswith('@"',i):
            i+=2
            while i<n:
                if text.startswith('""',i):i+=2
                elif text[i]=='"':i+=1;break
                else:i+=1
            else:raise ValueError('Unterminated verbatim string')
            blank(start,i)
        elif text[i]in'"\'':
            quote=text[i];i+=1
            while i<n:
                if text[i]=='\\':i+=2
                elif text[i]==quote:i+=1;break
                else:i+=1
            else:raise ValueError('Unterminated string/character literal')
            blank(start,min(i,n))
        else:i+=1
    return''.join(out)


def qualified_calls(text,path,method='ToArabicLetter',receiver='InvoiceOper'):
    masked=mask_noncode(text);result=[]
    pattern=re.compile(r'\b'+receiver+r'\s*\.\s*'+re.escape(method)+r'\s*\(')
    for m in pattern.finditer(masked):
        left=m.end()-1;depth=1;right=left+1
        while right<len(masked)and depth:
            if masked[right]=='(':depth+=1
            elif masked[right]==')':depth-=1
            right+=1
        if depth:raise ValueError('Unbalanced qualified call token')
        call=text[m.start():right]
        result.append(dict(source_path=path,method=method,call_line_start=text.count('\n',0,m.start())+1,
            call_line_end=text.count('\n',0,right-1)+1,call_text_sha256=sha(call.encode()),
            inert_argument_expression=' '.join(text[left+1:right-1].split()),not_type_or_runtime_resolution=True))
    return result


def manual_fixed_positions(formatted_ascii):
    """Reinterpret only the fixed twelve positions visible in SFormatNumber.

    Input is a supplied unsigned ASCII digit string (already padded to >=12),
    not a .NET formatted double. Return magnitude, not Arabic words/grammar.
    """
    if not isinstance(formatted_ascii,str)or re.fullmatch('[0-9]{12,}',formatted_ascii)is None:
        raise ValueError('Supplied unsigned padded ASCII digits required')
    groups=[formatted_ascii[0:3],formatted_ascii[3:6],formatted_ascii[6:9],formatted_ascii[9:12]]
    magnitude=sum(int(g)*10**p for g,p in zip(groups,(9,6,3,0)))
    return dict(supplied_digits=formatted_ascii,selected_groups=groups,selected_magnitude=str(magnitude),unread_tail=formatted_ascii[12:])


def manual_projection(source_currency,primary):
    if not isinstance(source_currency,str)or type(primary)is not bool:raise ValueError('Inert token and branch flag required')
    return dict(currency=source_currency if primary else'',arabic_currency_input=source_currency,english_currency_input=source_currency)


def manual_parse_boundary(raw,parse_succeeded,parsed_value='0'):
    """Outcome boolean supplied by caller, never infer .NET parsing from Python."""
    if not isinstance(raw,str)or type(parse_succeeded)is not bool:raise ValueError('Raw text and supplied boolean outcome required')
    return dict(BondVal=raw,word_numeric_input=str(Decimal(parsed_value))if parse_succeeded else'0',parse_health_in_Bond=False)


def manual_currency_family(code):
    ar_major={2:'Dollar',12:'Egyptian-pound',13:'Sudanese-pound',15:'Syrian-lira'}.get(code,'Riyal')
    ar_minor={2:'Cent',12:'Piastre',13:'Piastre'}.get(code,'Halala')
    en={2:('Dollar','Cent'),4:('Dirham','Fil'),9:('Pound','Penny'),10:('Euro','Cent'),11:('Yen','Sen'),8:('Riyal','Halala')}.get(code,('Riyal','Halala'))
    return dict(numeric_source_branch=code,arabic_major_family=ar_major,arabic_minor_family=ar_minor,english_major_family=en[0],english_minor_family=en[1])


def manual_ordinal(enum_values,index):
    if type(index)is not int or not 0<=index<len(enum_values):raise ValueError('In-range synthetic index required')
    return dict(displayed_synthetic_value=enum_values[index],persisted_index=index,read_numeric_cast_input=index,
                identity_preserved=enum_values[index]==index,actual_sdk_enum_not_supplied=True)


def main():
    reads=[];illustrations=[];checks=[];errors=[]
    def read(path,a,b):
        lines=(ROOT/path).read_text(encoding='utf-8-sig').splitlines(keepends=True)
        if not 1<=a<=b<=len(lines):raise ValueError('Invalid bounded range:'+path)
        text=''.join(lines[a-1:b]);reads.append(dict(path=path,start=a,end=b,sha256=sha(text.encode()),purpose='bounded-inert-source-text-not-semantic-or-runtime-coverage'))
        return text
    def source(*items):return';'.join(f'{p}:{a}-{b}'for p,a,b in items)
    def illustration(n,title,value,condition,roots,evidence,limit):
        ok=bool(condition)
        illustrations.append(dict(id=f'ALG7B21-{n:02d}',title=title,manual_model=value,illustration_assertions_passed=ok,finding_ids=roots,evidence=evidence,limit=limit,source_application_executed=False))
        if not ok:errors.append(f'ALG7B21-{n:02d}')
    def static(n,title,ok,roots,evidence,limit):
        checks.append(dict(id=f'ST7B21-{n:02d}',title=title,documented_text_observation_matches=bool(ok),finding_ids=roots,evidence=evidence,limit=limit,source_application_executed=False))
        if not ok:errors.append(f'ST7B21-{n:02d}')
    limit='Supplied ASCII/Decimal/boolean toy only; no C#/VB/.NET format/parse/words, SQL, template or printer execution; no approved currency/precision/sign/zero policy.'
    width=source((C+'InvoiceOper.cs',550,591),(C+'InvoiceOper.cs',707,795))
    a=manual_fixed_positions('999999999999')
    illustration(1,'Twelve supplied positions retain magnitude',a,a['selected_magnitude']=='999999999999'and a['unread_tail']=='','P7-139',width,limit)
    a=manual_fixed_positions('1000000000000')
    illustration(2,'Thirteen supplied digits select only first twelve',a,a['selected_magnitude']=='100000000000'and a['unread_tail']=='0','P7-139',width,limit)
    a,b=manual_fixed_positions('1000000000000'),manual_fixed_positions('1000000000001')
    illustration(3,'Two distinct wide integers collide before word grammar',dict(left=a,right=b),a['selected_magnitude']==b['selected_magnitude']and a['supplied_digits']!=b['supplied_digits'],'P7-139',width,limit)
    ev=source((C+'InvoiceData.cs',53,56),(C+'Print.cs',708,750),(C+'Print.cs',977,987),(C+'Print.cs',1051,1075),(C+'Print.cs',1141,1156))
    a,b=manual_projection('CURRENCY-TOKEN',True),manual_projection('CURRENCY-TOKEN',False)
    illustration(4,'Alternate DTO drops currency while both word inputs retain it',dict(primary=a,alternate=b),a['currency']=='CURRENCY-TOKEN'and b['currency']==''and b['arabic_currency_input']==a['arabic_currency_input'],'P7-140',ev,limit+' Token is not an SDK enum or printed label.')
    bad,zero=manual_parse_boundary('bad',False),manual_parse_boundary('0',True,'0')
    pe=source((F+'frmSandD.xaml.cs',1233,1330),(F+'frmSandQAndroid.xaml.cs',1030,1127),(C+'Bond.cs',40,44),(C+'Bond.cs',60,64))
    illustration(5,'Failure and genuine zero share word input but not raw amount',dict(failure=bad,zero=zero),bad['word_numeric_input']==zero['word_numeric_input']=='0'and bad['BondVal']!=zero['BondVal']and not bad['parse_health_in_Bond'],'P7-141',pe,limit+' Parse failure supplied, not performed.')
    a=manual_parse_boundary('12.5',True,'12.5')
    illustration(6,'Successful supplied parse is a counterexample to blanket failure',a,a['BondVal']==a['word_numeric_input']=='12.5','P7-141',pe,limit)
    supplied='19.999';fraction=supplied.split('.')[1][:2];rounded=str(Decimal(supplied).quantize(Decimal('.01'),rounding=ROUND_HALF_EVEN))
    illustration(7,'Retained034 fraction prefix is not normalization',dict(supplied_dot_string=supplied,prefix=fraction,illustrative_half_even=rounded),fraction=='99'and rounded=='20.00','P7-034',source((C+'InvoiceOper.cs',550,575),(C+'Print.cs',737,750)),limit+' Half-even is illustrative, NOT a chosen money policy. Primary Print preformats first.')
    a,b=manual_currency_family(4),manual_currency_family(2)
    illustration(8,'Retained035 branch drift with numeric2 counterexample',dict(code4=a,code2=b),a['arabic_major_family']!=a['english_major_family']and b['arabic_major_family']==b['english_major_family'],'P7-035',source((C+'InvoiceOper.cs',972,1170)),limit+' Families summarize literal local branches, not SDK enum mappings or grammar.')
    a,b=manual_ordinal([1,2,8],2),manual_ordinal([0,1,2],2)
    illustration(9,'Index/value mismatch requires actual external enum contract',dict(hypothetical_nonidentity=a,identity_counterexample=b),not a['identity_preserved']and b['identity_preserved'],'H7B21-04',source((F+'frmSettings.xaml.cs',333,352),(F+'frmSettings.xaml.cs',1028,1032),(F+'frmSettings.xaml.cs',1655,1661),(C+'InvoiceObj.cs',262,270)),limit+' Hypothetical enum is explicitly NOT the unavailable SDK definition; no new finding.')
    raw=''+' '+'';closing=' فقط لا غير';result=raw+closing
    illustration(10,'Separators plus closing phrase do not express numeric zero',dict(supplied_empty_group_and_zero_suffix=raw,source_style_nonempty_test=raw!='',separator_and_closing=result),raw!=''and'صفر'not in result,'H7B21-01',source((C+'InvoiceOper.cs',550,575),(C+'InvoiceOper.cs',972,1021)),limit+' Inert concatenation using supplied empty group output; exact VB/null/culture behavior not executed, required wording unresolved.')
    supplied='-000000000001';positions=[supplied[i:i+3]for i in(0,3,6,9)]
    illustration(11,'Signed formatted string lies outside unsigned positional proof',dict(supplied_signed_string=supplied,groups=positions,unread_tail=supplied[12:],sign_is_not_a_digit=supplied[0]=='-'),supplied[0]=='-'and len(supplied)==13,'H7B21-01',source((C+'InvoiceOper.cs',577,591),(C+'InvoiceOper.cs',707,795)),limit+' No assertion that .NET actually formats a negative value to this string; do not infer a production sign defect.')
    a=dict(debit='20',credit='120',word_magnitude='100',side='credit');b=dict(debit='120',credit='20',word_magnitude='100',side='debit')
    illustration(12,'Magnitude plus side can represent either ledger direction',dict(credit_case=a,debit_case=b),a['word_magnitude']==b['word_magnitude']and a['side']!=b['side'],'H7B21-01',source((F+'frmAccountsStatement.xaml.cs',708,747),(F+'frmCostCenterBalance.xaml.cs',632,651)),limit+' Sign/side semantics need an owner; no requirement to prepend minus to an absolute balance.')

    w=read(C+'InvoiceOper.cs',550,795)
    static(1,'Fixed twelve-position groups with no length branch in converter',all(x in w for x in('"000000000000"','Strings.Mid(str, 12, 1)','Strings.Mid(str, 7, 3)','Strings.Mid(str, 4, 3)','Strings.Mid(str, 1, 3)'))and not re.search(r'if\s*\([^\n]*(?:str.Length|Len\(str\))',w),'P7-139',width,'Exact local instructions, not formatted runtime output or proof a deployed amount reaches the boundary.')
    primary=read(C+'Print.cs',708,750);alternate=read(C+'Print.cs',977,1156);dto=read(C+'InvoiceData.cs',53,56)
    static(2,'Primary currency assigned, alternate not assigned on selected construction-to-return span','invoiceData.currency = Inv.Currency.ToString()'in primary and re.search(r'invoiceData2\.currency\s*=',alternate)is None and 'public string currency { get; set; } = string.Empty' in dto and 'list.Add(invoiceData2)'in alternate,'P7-140',ev,'Local DTO omission only. External ToDataTable/template aliases can change presentation; no blank printed invoice was observed.')
    d=read(F+'frmSandD.xaml.cs',1233,1330);q=read(F+'frmSandQAndroid.xaml.cs',1030,1127)
    static(3,'Two receipt print boundaries keep raw BondVal but ignore parse failure',all(re.search(r'double\.TryParse\(txtVal.Text, out double v\) \? v : 0',s)and re.search(r'BondVal\s*=\s*txtVal.Text',s)and 'IsNullOrWhiteSpace(txtVal.Text)'in s and 'ToArabicLetter(netVal,'in s for s in(d,q)),'P7-141',pe,'Whitespace guard is not a parse guard. Conditions include valid template path/Foundation access; no saved-zero claim.')
    dx=read(F+'frmSandD.xaml',64,93)+read(F+'frmSandD.xaml',345,348);qx=read(F+'frmSandQAndroid.xaml',65,94)+read(F+'frmSandQAndroid.xaml',322,325);dh=read(F+'frmSandD.xaml.cs',1092,1122)
    static(4,'Selected receipt fields/styles have no numeric input mask; D handler only updates parsed values','x:Name="txtVal"'in dx and 'x:Name="txtVal"'in qx and all('PreviewTextInput'not in s and 'EventSetter'not in s and 'IsReadOnly'not in s for s in(dx,qx))and 'double.TryParse(txtVal.Text' in dh and 'txtVal.Text ='not in dh.split('private void txtValD_TextChanged')[0],'P7-141',source((F+'frmSandD.xaml',64,93),(F+'frmSandD.xaml',345,348),(F+'frmSandD.xaml.cs',1092,1122),(F+'frmSandQAndroid.xaml',65,94),(F+'frmSandQAndroid.xaml',322,325)),'Selected local XAML/styles and event only; no rendering, global styles or WPF event timing acceptance.')
    static(5,'Both languages consume formatted primary Net and raw alternate Net','ToArabicLetter(Conversions.ToDouble(invoiceData.Net), Inv.Currency)'in primary and 'SpellNumberEDP(invoiceData.Net, Inv.Currency)'in primary and 'ToArabicLetter(Inv.Net, Inv.Currency)'in alternate and 'SpellNumberEDP(Conversions.ToString(Inv.Net), Inv.Currency)'in alternate,'P7-034',source((C+'Print.cs',737,750),(C+'Print.cs',1051,1075)),'Primary preformat is counterevidence to a universal raw-fraction truncation claim; no language/runtime output equality established.')
    ar=read(C+'InvoiceOper.cs',550,575)
    static(6,'Fixed dot and first two fractional characters remain prior034','Strings.Split(Conversions.ToString(givenNumber), ".")'in ar and 'Substring(0, 2)'in ar,'P7-034',source((C+'InvoiceOper.cs',550,575)),'Recheck of retained root, no new row/evidence extension and no approved precision policy.')
    currencies=read(C+'InvoiceOper.cs',972,1170)
    static(7,'Local numeric currency branches are asymmetric; numeric2 present in both',all(x in currencies for x in('Conversions.ToString(12)','Conversions.ToString(13)','Conversions.ToString(4)','right = "Dirham"','"Dollar"')),'P7-035',source((C+'InvoiceOper.cs',972,1170)),'Compare literal numeric branches only; do not invent external enum values or complete currency support.')
    common=read(C+'Common.cs',768,788);settings=read(F+'frmSettings.xaml.cs',2772,2791)
    receipts=[read(F+n+'.xaml.cs',a,b)for n,a,b in(('frmSandD',1285,1313),('frmSandQAndroid',1082,1110),('frmSandQD',1388,1411),('frmSandSD',1339,1365),('frmSandVAT',1200,1214))]
    static(8,'Five receipt callers use settings key13, with local settings13 counterevidence',all('GetCurrencytosand(13)'in s for s in receipts)and '@InvId' in common and 'return 1;'in common and 'rbRecieptVAT)) return 13' in settings,'H7B21-03',source((C+'Common.cs',768,788),(F+'frmSettings.xaml.cs',2772,2791),(F+'frmSandD.xaml.cs',1285,1313),(F+'frmSandQAndroid.xaml.cs',1082,1110),(F+'frmSandQD.xaml.cs',1388,1411),(F+'frmSandSD.xaml.cs',1339,1365),(F+'frmSandVAT.xaml.cs',1200,1214)),'Shared13 may be intended policy; different ReceiptType numbers alone are NOT a new currency-setting finding.')
    salary=read(F+'frmSalaryPay.xaml.cs',835,867);employee=read(F+'frmEmpSalaryAddSub.xaml.cs',973,984);sx=read(F+'frmSalaryPay.xaml',368,374)
    static(9,'Two HR word callers omit currency; salary net is locally read-only','ToArabicLetter(netVal)'in salary and re.search(r'ToArabicLetter\(\s*Convert.ToDouble\(txtVal.Text\)\)',employee)is not None and 'IsReadOnly="True"'in sx,'H7B21-01',source((F+'frmSalaryPay.xaml.cs',835,867),(F+'frmEmpSalaryAddSub.xaml.cs',973,984),(F+'frmSalaryPay.xaml',368,374)),'Default SAR usage is source fact, not proof multi-currency HR is required;006 financial/recalculation root remains unchanged.')
    statement=read(F+'frmAccountsStatement.xaml.cs',708,747);cost=read(F+'frmCostCenterBalance.xaml.cs',632,651);account=read(F+'frmAccountBalance.xaml.cs',453,462)
    static(10,'Statement/cost carry magnitude and side; AccountBalance uses literal0.00 selector',all(x in statement for x in('totalCredit - totalDebit','totalDebit - totalCredit','BalanceInperiod = "0"'))and 'BalanceType = "دائن"'in cost and 'txtBalance1.Text != "0.00"'in account,'H7B21-01',source((F+'frmAccountsStatement.xaml.cs',708,747),(F+'frmCostCenterBalance.xaml.cs',632,651),(F+'frmAccountBalance.xaml.cs',453,462)),'Direction encoded by side is counterevidence to blanket lost-negative claims. Literal selector needs format/DTO contract, not an assumed new root.')
    load=read(F+'frmSettings.xaml.cs',333,352);restore=read(F+'frmSettings.xaml.cs',1028,1032);save=read(F+'frmSettings.xaml.cs',1655,1661);obj=read(C+'InvoiceObj.cs',262,270)
    static(11,'Enum objects displayed but index persisted/restored and cast numerically',all(x in load for x in('Enum.GetValues(typeof(Currency))','Items.Add(currencyValue)'))and 'cmbCurrency.SelectedIndex = Convert.ToInt32(row["Currency"])'in restore and '"@Currency", cmbCurrency.SelectedIndex' in save and '(Currency)Conversions.ToInteger(dataTable.Rows[0]["Currency"])'in obj,'H7B21-04',source((F+'frmSettings.xaml.cs',333,352),(F+'frmSettings.xaml.cs',1028,1032),(F+'frmSettings.xaml.cs',1655,1661),(C+'InvoiceObj.cs',262,270)),'Potential index/value ambiguity is an unanswered dependency contract, not a new finding without actual enum evidence. Identity mapping is a counterexample.')
    helper=read(C+'Number2Arabic.cs',261,328);vat=read(F+'frmSandVAT.xaml.cs',1200,1214)+read(F+'frmSandVAT.xaml.cs',1330,1345)
    static(12,'Legacy helper and VAT numeric catch do not establish approved replacement or words','public static string ameral' in helper and 'double.Parse(strNnumber)'in helper and 'netValDouble.ToString("N2")'in vat and 'ArabicLetter = arabicLetter'in vat,'H7B21-02',source((C+'Number2Arabic.cs',261,328),(F+'frmSandVAT.xaml.cs',1200,1214),(F+'frmSandVAT.xaml.cs',1330,1345)),'Fallback numeric N2 in word field is source-bound and owner/template health contract remains open; no rendered report, replacement or absence proof.')
    inventory=list(csv.DictReader((AUDIT/'evidence/inventory.csv').open(encoding='utf-8',newline='')))
    paths=sorted(r['path']for r in inventory if r['kind']=='source'and r['path'].endswith('.cs'))
    calls=[];english=[];external_legacy=[];replacement_paths=[]
    for path in paths:
        data=(ROOT/path).read_bytes()
        try:text=data.decode('utf-8-sig')
        except UnicodeDecodeError:
            text=data.decode('utf-8-sig',errors='replace');replacement_paths.append(path)
        calls+=qualified_calls(text,path);english+=qualified_calls(text,path,'SpellNumberEDP',r'[A-Za-z_]\w*')
        if path!=C+'Number2Arabic.cs':
            external_legacy+=qualified_calls(text,path,'ameral','Number2Arabic')
    discovery=dict(source_csharp_paths_lexically_scanned=len(paths),literal_qualified_arabic_calls=calls,literal_qualified_english_calls=english,
        lexical_utf8_replacement_paths_not_encoding_acceptance=replacement_paths,
        external_qualified_Number2Arabic_ameral_calls_discovered=external_legacy,not_complete_callgraph_or_capability_census=True,
        scanned_bodies_not_reviewed=True,masked_interpolated_string_expressions_aliases_reflection_delegates_and_external_components_not_resolved=True)
    result=dict(phase='7B21-partial-static-amountword-contracts',application_code_imported_or_executed=False,dotnet_or_visualbasic_format_parse_or_words_executed=False,
        scanner_template_or_printer_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        B_R4e_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,
        illustration_count=len(illustrations),static_lexical_contract_check_count=len(checks),illustrations=illustrations,static_lexical_contract_checks=checks,
        bounded_source_reads_not_semantic_coverage=reads,qualified_literal_discovery=discovery,
        retained_additive_B10_arithmetic_erratum=dict(entered_quantity=2,equality=12,base_unit_cost=5,local_cost=10,reference_cost=120,archive_rewritten=False),errors=errors)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if errors else 0


if __name__=='__main__':raise SystemExit(main())
