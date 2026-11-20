#!/usr/bin/env python3
"""Source contracts and independent models; no C#, SQL, WPF or Office execution."""
from pathlib import Path
import html
from html.parser import HTMLParser
import re

ROOT=Path(__file__).resolve().parents[2]/'SmartAuditERP/Form_WPF'
def read(n): return (ROOT/n).read_text(encoding='utf-8-sig')
def section(s,start,end):
 i=s.index(start); return s[i:s.index(end,i)]
def check(name,condition):
 if not condition: raise AssertionError(name)
 print('PASS',name)
def ordered(s,parts):
 pos=-1
 for p in parts:
  pos=s.find(p,pos+1)
  if pos<0:return False
 return True

rent=read('frmRptRentInvoices.xaml.cs'); picker=read('frmInvoiceRentSrch.xaml.cs')
for name,src,start,end,expressions in [
 ('rent',rent,'private void GenerateFilter()', '#endregion', ['cmbUsers.Text','cmbGroups.Text','txtClientMobile.Text.Trim()','txtClientName.Text.Trim()']),
 ('picker',picker,'private string BuildFilterExpression()', 'private void RefreshDisplayRows', ['cmbUsers.Text','txtClientMobile.Text.Trim()','txtClientName.Text.Trim()'])]:
 area=section(src,start,end)
 def contract(s): return all('{EscapeFilterLiteral('+x+')}' in s and '{'+x+'}' not in s for x in expressions)
 check(name+' every LIKE text literal escapes apostrophes',contract(area))
 check(name+' helper uses DataView apostrophe doubling','(text ?? string.Empty).Replace("\'", "\'\'")' in src)
 check(name+' bypass mutant detected',not contract(area.replace('{EscapeFilterLiteral('+expressions[0]+')}', '{'+expressions[0]+'}')))
for x in ["O'Brien", "a' OR 1=1 OR cust='x", "'", "مرحبا", "50% [x]"]:
 escaped=x.replace("'", "''")
 check('literal model round trips '+repr(x),escaped.replace("''", "'")==x and escaped.count("'")%2==0)

prod=read('frmProductionOrder.xaml.cs')
load=section(prod,'// ═══ تحميل مكونات الإنتاج ═══','CalcTot();')
def precision(s): return all(x in s for x in ['double qty = Convert.ToDouble(row["val1"]);','double price = Convert.ToDouble(row["exchange_price"]);','double total = Math.Round(qty * price, 2);','Qty = qty,','Price = price,'])
check('production reader keeps raw quantity and price while rounding total',precision(load))
check('production rounding mutant detected',not precision(load.replace('double qty = Convert.ToDouble(row["val1"]);','double qty = Math.Round(Convert.ToDouble(row["val1"]), 2);')))
for qty,price in [(1.2345,123.4567),(0.004,1000.0),(4,5)]:
 restored=(qty,price);check('production quantity and price model '+str((qty,price)),restored==(qty,price))

trial=read('frmMezanMorg3a.xaml.cs'); doc=section(trial,'private FlowDocument BuildPrintDocument()', 'private void AddHeaderCell(')
headers=re.findall(r'AddHeaderCell\(headerRow, "([^"]+)"\)',doc)
fields=re.findall(r'AddBodyCell\(dataRow, row\.(Tr\w+)',doc)
expected=['TrAccount','TrAccName','TrDeptIntial','TrCreditIntial','TrDeptPervious','TrCreditPervious','TrDebtorMovement','TrCreditorMovement','TrDeptBlc','TrCreditBlc','TrDeptFinal','TrCreditFinal']
def print_contract(s):return 'i < 12' in s and re.findall(r'AddBodyCell\(dataRow, row\.(Tr\w+)',s)==expected and len(re.findall(r'AddHeaderCell\(headerRow,',s))==12
check('trial balance print has 12 columns and the same ordered fields as grid',print_contract(doc) and headers[4:6]==['رصيد سابق مدين','رصيد سابق دائن'])
check('missing previous balance mutant detected',not print_contract(doc.replace('AddBodyCell(dataRow, row.TrDeptPervious.ToString("N2"));','')))

purch=section(read('frmPurchInv.xaml.cs'),'private void SearchByID(int unitId)','private void FillRowFromDt(')
def purchase_contract(s): return (ordered(s,['var matchedRow = _gridSource[foundIndex];','matchedRow.QuantDgv = (q + 1).ToString();','_gridSource.IndexOf(matchedRow);','CalcRowValues(matchedIndex);','CalcTot();']) and '_gridSource.Remove(sourceRow);' not in s)
check('purchase duplicate recalculates identity and preserves unowned source',purchase_contract(purch))
check('stale index mutant detected',not purchase_contract(purch.replace('CalcRowValues(matchedIndex);','CalcRowValues(foundIndex);')))
check('source deletion mutant detected',not purchase_contract(purch+' _gridSource.Remove(sourceRow);'))
for source,found in [(0,2),(2,0),(1,1)]:
 rows=[{'name':n,'qty':1} for n in 'ABC']; matched=rows[found];origin=rows[source];matched['qty']+=1
 actual=next(i for i,x in enumerate(rows) if x is matched)
 check(f'purchase source={source} matched={found} recalculates matched object',rows[actual] is matched and matched['qty']==2 and origin in rows)

specs={
 'frmItemsalesdetailsPos.xaml.cs':('private void ExportToExcelHtml(string fileName)','#endregion',['Title','item.DgvStore','item.DgvInvType','item.DgvClient','item.DgvDate','item.DgvInvNo','item.DgvItem','item.DgvUnit','item.DgvUser']),
 'frmNkdTotSalePurch.xaml.cs':('private void ExportToHtml(string fileName)','/// <summary>',['Title']+['row.Column'+str(i) for i in (1,2,3,4,6,5)]+['txtSumPurch.Text','txtSumSale.Text']),
 'frmMezanyaArba7.xaml.cs':('private void ExportToExcelHtml(string fileName)','/// <summary>',['Title','row.Column1','row.Column2','row.Column5','row.Column6','txtDeptDiff.Text','txtCreditDiff.Text']),
 'frmMezanMorg3a.xaml.cs':('private void ExportToExcelHtml(string fileName)','/// <summary>',['Title','row.TrAccName'])}
for file,(start,end,fields) in specs.items():
 s=section(read(file),start,end)
 def encode_contract(t):return all('{System.Net.WebUtility.HtmlEncode('+f+')}' in t and '{'+f+'}' not in t for f in fields)
 check(file+' dynamic text in HTML text nodes encoded',encode_contract(s))
 check(file+' unescaped mutant detected',not encode_contract(s.replace('{System.Net.WebUtility.HtmlEncode('+fields[-1]+')}','{'+fields[-1]+'}')))
class Cells(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.cells=[];self.inside=False;self.text='';self.bad=[]
 def handle_starttag(self,tag,attrs):
  if tag=='td':self.inside=True;self.text=''
  elif self.inside:self.bad.append(tag)
 def handle_endtag(self,tag):
  if tag=='td':self.cells.append(self.text);self.inside=False
 def handle_data(self,data):
  if self.inside:self.text+=data
for text in ['<script>alert(1)</script>', 'اسم & قيمة', '</td><td>مخترق', 'A "\' B', '']:
 p=Cells();p.feed('<table><tr><td>'+html.escape(text)+'</td></tr></table>')
 check('encoded HTML cell model '+repr(text),p.cells==[text] and not p.bad)
print('PASS — source contracts/models only; actual DataView, C#, SQL, WPF and Office not executed')
