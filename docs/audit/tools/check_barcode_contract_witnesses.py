#!/usr/bin/env python3
"""7B20 bounded text observations and MANUALLY transcribed barcode illustrations.

No application import/execution, SQL engine, .NET culture/DTO, scanner, template,
ToDataTable, printer, provider, business data, remediation or measurement.
ASCII-only toy models are NOT a C# interpreter, checksum validator or barcode
standard implementation. A regex census of477 C# paths is NOT a body review or
complete callgraph. B20/R4d is bounded;7B/7 partial;7C unstarted;8 unauthorized.
"""
from __future__ import annotations
import csv
from decimal import Decimal as D,ROUND_HALF_EVEN
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
AUDIT=ROOT/'docs/audit';F='SmartAuditERP/Form_WPF/';C='SmartAuditERP/Class/'
SOURCE='10ba215152f722c8808aea0bb672c1d1d4d9d711'


def ascii_int_or_zero(text):
    """Toy for positive ASCII integer pieces and explicit alphabetic failures only."""
    return int(text)if re.fullmatch('[0-9]+',text)else 0


def manual_payload(code,mode,sale='10'):
    """Given a successful selected source row; NOT a DB lookup or real parser."""
    if len(code)!=13:raise ValueError('This illustration requires thirteen characters')
    price=qty=D('0')
    if mode==1:qty=D(ascii_int_or_zero(code[7:9]))+D(ascii_int_or_zero(code[9:12]))/1000
    elif mode in(2,3):
        price=D(ascii_int_or_zero(code[7:10]))+D(ascii_int_or_zero(code[10:12]))/100
        if mode==3 and D(sale)>0:qty=(price/D(sale)).quantize(D('.001'),rounding=ROUND_HALF_EVEN)
    return dict(price=price,quantity=qty)


def manual_consumer(payload,consumer,unit_price='10'):
    """Successful NEW line/default unit, no offers/tax/customer override/merge."""
    price,qty=D(unit_price),D('1');scale=False
    if consumer=='POS':
        scale=payload['price']>0 or payload['quantity']>0
        if payload['price']>0:price=payload['price']
        if payload['quantity']>0:qty=payload['quantity']
    elif consumer not in('Sale','Purch','InputOutput'):raise ValueError('Named invoice consumer required')
    return dict(price=str(price),quantity=str(qty),is_scale=scale)


def manual_prefix_candidates(prefix,base_barcode,units):
    """Relational OR illustration, NOT SQL execution or physical row-order claim."""
    return [dict(u)for u in units if u['barcode']==prefix or base_barcode==prefix]


def manual_priority(unit_exact,alias_exact,thirteen_chars):
    return 'unit-exact'if unit_exact else'alias-exact'if alias_exact else'scale-attempt'if thirteen_chars else'not-found'


def manual_total(quantity,price,is_scale,static_price_flag):
    return price if is_scale and static_price_flag else quantity*price


def literal_calls(text,path):
    """Qualified lexical tokens only; handles balanced comments/quotes, not types."""
    result=[]
    for match in re.finditer(r'\bItemOper\s*\.\s*SearchForBarcode\s*\(',text):
        start=match.start();op=match.end()-1;depth=0;quote=None;i=op;comment=None
        while i<len(text):
            ch=text[i];pair=text[i:i+2]
            if comment=='line':
                if ch=='\n':comment=None
            elif comment=='block':
                if pair=='*/':comment=None;i+=1
            elif quote:
                if ch=='\\':i+=1
                elif ch==quote:quote=None
            elif pair=='//':comment='line';i+=1
            elif pair=='/*':comment='block';i+=1
            elif ch in('\"',"'"):quote=ch
            elif ch=='(':depth+=1
            elif ch==')':
                depth-=1
                if depth==0:break
            i+=1
        if i>=len(text):raise ValueError('Unbalanced inert call token')
        call=text[start:i+1]
        result.append(dict(source_path=path,call_line_start=text.count('\n',0,start)+1,call_line_end=text.count('\n',0,i)+1,
            call_text_sha256=hashlib.sha256(call.encode()).hexdigest(),inert_argument_expression=text[op+1:i],not_type_or_runtime_resolution=True))
    return result


class BoundedReads:
    def __init__(self):self.records={}
    def read(self,path,start,end):
        text=(ROOT/path).read_text(encoding='utf-8-sig');lines=text.splitlines(keepends=True)
        if not 0<start<=end<=len(lines):raise ValueError('Out-of-source bounded read')
        segment=''.join(lines[start-1:end]);key=(path,start,end)
        self.records[key]=dict(path=path,start=start,end=end,source_slice_sha256=hashlib.sha256(segment.encode()).hexdigest(),not_semantic_or_execution_coverage=True)
        return segment


def build_witness():
    read=BoundedReads();illustrations=[];statics=[];errors=[]
    def illustrate(number,title,findings,observed,expected,limit):
        passed=observed==expected
        illustrations.append(dict(id=f'ALG7B20-{number:02d}',title=title,finding_ids=findings,observed=observed,expected=expected,
            illustration_assertions_passed=passed,source_application_executed=False,limit=limit))
        if not passed:errors.append('manual illustration '+str(number))
    model_limit='Manually transcribed ASCII/Decimal illustration only; no SQL/.NET/WPF/DTO, physical order, business policy, checksum or saved invoice demonstrated.'
    weight=manual_payload('2300001025000',1)
    illustrate(1,'Valid weight is discarded by three identity-only invoice callers','P7-136',
        [manual_consumer(weight,n)['quantity']for n in('Sale','Purch','InputOutput')],['1','1','1'],model_limit)
    price=manual_payload('2300001012340',2)
    illustrate(2,'Embedded price is also discarded, not merely fractional quantity','P7-136',
        dict(decoded_price=str(price['price']),invoice_price=manual_consumer(price,'Sale')['price']),dict(decoded_price='12.34',invoice_price='10'),model_limit)
    illustrate(3,'POS consumes a successfully decoded positive weight as counterevidence','P7-136',manual_consumer(weight,'POS'),dict(price='10',quantity='2.5',is_scale=True),model_limit)
    units=[dict(unit=1,barcode='2300001',equality='1',sale='10'),dict(unit=12,barcode='BOX0001',equality='12',sale='120')]
    candidates=manual_prefix_candidates('2300001','2300001',units)
    illustrate(4,'Base-barcode OR admits both unit rows even with distinct barcodes','P7-137',[u['unit']for u in candidates],[1,12],model_limit+' Candidate multiplicity, not proof which SQL row arrives first.')
    illustrate(5,'Either selected unit changes weight-to-base meaning','P7-137',[str(weight['quantity']*D(u['equality']))for u in candidates],['2.5','30.0'],model_limit+' Assumes Wscale1 payload is the base unit; support/unit contract must be supplied.')
    malformed=manual_payload('2300001AABBB0',1)
    illustrate(6,'Alphabetic payload falls to numeric zero and POS ordinary default one','P7-138',manual_consumer(malformed,'POS'),dict(price='10',quantity='1',is_scale=False),model_limit+' Given prefix lookup succeeds and exact lookups do not match.')
    partial=manual_payload('2300001AA2500',1)
    illustrate(7,'Partially malformed payload can still become a positive weight','P7-138',str(partial['quantity']),'0.25',model_limit+' Illustrates loss of parse-failure status, not a .NET parser conformance test.')
    illustrate(8,'Exact unit and alias results precede scale attempt','H7B20-03',
        [manual_priority(*a)for a in((True,True,True),(False,True,True),(False,False,True),(False,False,False))],
        ['unit-exact','alias-exact','scale-attempt','not-found'],model_limit)
    illustrate(9,'Retained static price flag root remains independent','P4-028',
        [str(manual_total(D('2'),D('10'),True,flag))for flag in(False,True)],['20','10'],model_limit+' Does not reset or remediate the actual static field.')
    illustrate(10,'A guard on default one does not validate a later payload quantity','P4-014',
        dict(stock='2',checked_default='1',later_scale_quantity='4',later_exceeds=D('4')>D('2')),dict(stock='2',checked_default='1',later_scale_quantity='4',later_exceeds=True),model_limit+' Retained potential stock/save root; no bypass of deployed server guards or successful save claimed.')
    illustrate(11,'Scanned label keeps a unit barcode but takes base price; selected-unit path differs','P7-037',
        dict(scan_barcode='BOX0001',scan_price='10',selected_unit_price='120'),dict(scan_barcode='BOX0001',scan_price='10',selected_unit_price='120'),model_limit+' Value projection only; UtilitiesProj/REPX/printer not executed.')
    illustrate(12,'Mode3 quantity precision and zero divisor are policy/health boundaries','H7B20-01',
        [str(manual_payload('2300001001000',3,sale=s)['quantity'])for s in('3','0')],['0.333','0'],model_limit+' No required rounding policy or free-item rule inferred from this illustration.')
    def lexical(number,title,findings,checks,evidence,limit):
        passed=all(checks)
        statics.append(dict(id=f'ST7B20-{number:02d}',title=title,finding_ids=findings,evidence=evidence,
            documented_text_observation_matches=passed,source_application_executed=False,limit=limit))
        if not passed:errors.append('bounded lexical observation '+str(number))
    core=read.read(C+'ItemOper.cs',1908,2091);to_double=read.read(C+'ItemOper.cs',93,103)
    lexical(1,'Exact unit then alias then length13 fallthrough','H7B20-03',
        [core.index('// بحث في ItemUnits')<core.index('// بحث في Itembarcodes')<core.index('if (barcode.Length == 13)'),core.count('return;')>=5],C+'ItemOper.cs:1908-2091','Token/order checks, not query execution or complete callgraph.')
    lexical(2,'Scale numeric slices and three modes are explicit','P7-136;H7B20-01',
        [all(t in core for t in('wscale == 1','wscale == 2','wscale == 3','barcode.Substring(7, 2)','barcode.Substring(9, 3)','barcode.Substring(7, 3)','barcode.Substring(10, 2)','decimal.Divide(itemPrice, salePrice)'))],C+'ItemOper.cs:1908-2091','Named literals only; no checksum/symbology or culture contract inferred.')
    lexical(3,'Prefix predicate can match Items barcode for every joined ItemUnits row','P7-137',
        ['ItemUnits.ItemId=items.id'in core,'or Items.barcode=N\'{shortBarcode}\''in core,core.count('dt.Rows[0]["unit"]')>=2,'ORDER BY'not in core.upper()],C+'ItemOper.cs:1908-2091','Unordered candidate selection, not a prediction of physical query order.')
    lexical(4,'Numeric parse returns zero and a successful prefix still assigns identity','P7-138',
        ['double.TryParse(value.ToString(), out double result) ? result : 0'in to_double,'itemId = ToInt(dt.Rows[0]["id"]);'in core,'itemQuantity = new decimal(weightVal);'in core],C+'ItemOper.cs:93-103;1908-2091','Observed fallback; no actual VisualBasic/.NET parse or scanner input executed.')
    sale=read.read(F+'frmInvSale.xaml.cs',667,725);purch=read.read(F+'frmInvPurch.xaml.cs',613,663);io=read.read(F+'frmInvInputOutput.xaml.cs',427,458)
    for n,name,text,var,find in((5,'Sale',sale,'itemQuantity','P7-136'),(6,'Purch',purch,'itemQuantity','P7-136'),(7,'InputOutput',io,'foundQty','P7-136')):
        lexical(n,name+' transports identity but not decoded numeric values',find,
            [text.count(var)==2,re.search(r'ref\s+(?:this\.)?Invoic\s*,\s*false\b',text)is not None,'SearchForBarcode'in text],
            F+{'Sale':'frmInvSale.xaml.cs:667-725','Purch':'frmInvPurch.xaml.cs:613-663','InputOutput':'frmInvInputOutput.xaml.cs:427-458'}[name],
            'Counts/false token are bounded textual observations, not whole dataflow or all editor/writer behavior.')
    pos=read.read(F+'frmInvPOS.xaml.cs',871,955)
    lexical(8,'POS applies positive outputs only after SearchByID guard','P7-138;P4-014',
        ['if (itemQuantity > 0 || itemPrice > 0)'in pos,'invItem.ItemQuantity = Convert.ToDouble(itemQuantity);'in pos,pos.index('SearchByID(itemID')<pos.index('invItem.ItemQuantity ='),pos.count('ItemOper.ISvalidQuantity(')==1],F+'frmInvPOS.xaml.cs:871-955','No server/write guard assessment beyond retained P4-014; source order only.')
    defaults=read.read(C+'ItemOper.cs',729,811);create=read.read(C+'ItemOper.cs',1035,1185);calc=read.read(C+'ItemOper.cs',1367,1430)
    lexical(9,'Default line quantity, scale flag and static total calculation','P7-136;P4-028',
        [defaults.count('newItem.ItemQuantity = 1;')==2,'newItem.IsScaleItem = isScale;'in create,'item.IsScaleItem && IsPriceFromBarcode'in calc],C+'ItemOper.cs:729-811;1035-1185;1367-1430','Successful visible assignments assumed; external DTO semantics not executed.')
    label=read.read(F+'frmPrintBarcode.xaml.cs',215,253);project=read.read(F+'frmPrintBarcode.xaml.cs',337,381);base=read.read(C+'Common.cs',560,578)
    lexical(10,'Scanned-label unit/price dropped and DTO projection remains','P7-037',
        ['ItemSalePrice = Common.GetItemPrice(itemId)'in label,'ItemBarcode   = barcode.Trim()'in label,'sale_price'in base,'Barcode    = item.ItemBarcode'in project,'global::UtilitiesProj.Common.ToDataTable(list)'in project],F+'frmPrintBarcode.xaml.cs:215-253;337-381;'+C+'Common.cs:560-578','Retained037, not a new finding or manifest/printer acceptance.')
    manual=read.read(F+'frmItemsBarcode.xaml.cs',274,328);dispatch=read.read(F+'frmItemsBarcode.xaml.cs',334,488)
    lexical(11,'Selected unit uses item+barcode key and local label copies differ from invoice engine','P7-037;H7B20-02',
        ['IU.sale'in manual,'IU.barcode = @Barcode AND IU.ItemID = @ItemID'in manual,'int.TryParse(txtQuat.Text, out qty);'in dispatch,'for (int i = 0; i < qty; i++)'in dispatch,'xtraReport.ShowPreviewDialog();'in dispatch],F+'frmItemsBarcode.xaml.cs:274-328;334-488','Unit-key counterexample only; no approved VAT/quantity policy, REPX or actual copies measured.')
    writer=read.read(F+'frmItems.xaml.cs',905,925)+read.read(F+'frmItems.xaml.cs',1022,1054)
    lexical(12,'Item editor writes base and extra units with separate barcodes','P7-137',
        ['wscaleVal = 1'in writer,'wscaleVal = 3'in writer,'// Insert default unit'in writer,'foreach (var u in listItemUnit)'in writer,'u.DgvUnitBarcode'in writer],F+'frmItems.xaml.cs:905-925;1022-1054','Source feasibility of multiunit rows, not a real saved fixture or deployed constraints.')
    # Explicitly record selected supporting reads, not whole-file semantic coverage.
    for path,start,end in((F+'frmInventoryTransfer.xaml.cs',575,614),(F+'frmInventoryTransfer.xaml.cs',648,666),(F+'frmSafeAdjust.xaml.cs',618,643),
        (F+'frmSafeAdjust.xaml.cs',291,336),(F+'frmSafeAdjust.xaml.cs',410,436),(C+'ItemOper.cs',491,576),(C+'ItemOper.cs',1829,1902),
        (F+'frmInvPOS.xaml.cs',1901,1978),(F+'frmInvSale.xaml.cs',3590,3597),(F+'frmInvPurch.xaml.cs',2753,2770),(F+'frmInvInputOutput.xaml.cs',988,997),
        (F+'frmInvPOS.xaml.cs',834,850),(F+'frmInventoryTransfer.xaml.cs',167,218),(F+'frmSafeAdjust.xaml.cs',1708,1725),
        (F+'frmPrintBarcode.xaml.cs',50,90),(F+'frmPrintBarcode.xaml.cs',307,325),(F+'frmItemsBarcode.xaml.cs',142,174),(F+'frmItemsBarcode.xaml.cs',206,237),
        (C+'InvoiceData.cs',274,283),(C+'InvoiceData.cs',374,380),(C+'InvoiceData.cs',415,423),
        (F+'frmInvSale.xaml',584,594),(F+'frmInvPurch.xaml',1,16),(F+'frmInvPurch.xaml',591,609),(F+'frmInvInputOutput.xaml',511,522),
        (F+'frmInvPOS.xaml',832,848),(F+'frmInventoryTransfer.xaml',1,18),(F+'frmSafeAdjust.xaml',1,16),
        (F+'frmPrintBarcode.xaml',1,16),(F+'frmPrintBarcode.xaml',199,206),(F+'frmPrintBarcode.xaml',317,336),(F+'frmPrintBarcode.xaml',408,421),
        (F+'frmItemsBarcode.xaml',211,294),(F+'frmItemsBarcode.xaml',358,405)):
        read.read(path,start,end)
    inventory=list(csv.DictReader((AUDIT/'evidence/inventory.csv').open(encoding='utf-8',newline='')))
    csharp=[r['path']for r in inventory if r['path'].endswith('.cs')and not any(x in Path(r['path']).parts for x in('bin','obj'))]
    discovered=[call for path in csharp for call in literal_calls((ROOT/path).read_text(encoding='utf-8-sig',errors='replace'),path)]
    discovered.sort(key=lambda r:(r['source_path'],r['call_line_start']))
    if len(csharp)!=477 or len(discovered)!=7:errors.append('qualified lexical477/7 discovery count')
    old=json.loads((AUDIT/'evidence/navigation-contract-witnesses-07B19.json').read_bytes())
    return dict(audit_reference_date_utc='2026-11-16',source_head=SOURCE,phase='7B20-partial-static-barcode-contracts',
        method='Independent manually transcribed ASCII/Decimal illustrations and bounded literal-source observations only, not SQL/C#/WPF/DTO/UtilitiesProj/REPX/scanner/printer or business acceptance.',
        illustration_count=len(illustrations),illustrations=illustrations,static_lexical_contract_check_count=len(statics),static_lexical_contract_checks=statics,
        bounded_source_reads_not_semantic_coverage=sorted(read.records.values(),key=lambda r:(r['path'],r['start'],r['end'])),
        qualified_literal_discovery=dict(source_csharp_paths_lexically_scanned=len(csharp),literal_call_tokens=len(discovered),literal_calls=discovered,
            not_complete_callgraph_or_capability_census=True,not477_body_reviews=True,scope='Exact qualified spelling ItemOper.SearchForBarcode only; aliases/delegates/reflection/other barcode engines not inferred.'),
        retained_additive_B10_arithmetic_erratum=old['retained_additive_B10_arithmetic_erratum'],
        application_code_imported_or_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        scanner_template_or_printer_executed=False,application_remediation_performed=False,real_business_or_secret_data_used=False,
        spreadsheet_or_formula_interpreter_executed=False,phase7C_started=False,phase8_authorized_or_started=False,
        B_R4d_bounded_not_whole7B_closure=True,prior_roots_not_assumed_remediated=True,unresolved_external_contracts_and_explicit_splits_retained=True,errors=errors)


if __name__=='__main__':
    import sys
    result=build_witness();print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(result['errors']))
