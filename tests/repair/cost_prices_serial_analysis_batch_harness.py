#!/usr/bin/env python3
"""Source checks and models only; does not run CLR, SQL Server, WPF or reports."""
from pathlib import Path
from decimal import Decimal
import sqlite3
R=Path(__file__).resolve().parents[2] / 'SmartAuditERP'
def read(f): return (R/f).read_text(encoding='utf-8-sig',errors='replace')
def part(s,a,b): return s[s.index(a):s.index(b,s.index(a))]
checks=0
def check(name, value):
    global checks
    assert value, name
    checks+=1
    print('PASS',name)

cost=read('Form_WPF/frmRptCostCenter.xaml.cs')
detail=part(cost,'private void DetailedResults()','#region Show Result (Aggregated)')
def walk_contract(s):
    return all(x in s for x in ['SELECT code, ParentCode FROM cost_center WHERE Is_Deleted=0','new Dictionary<int, List<int>>()','new HashSet<int>()','new Queue<int>()','queue.Enqueue(selectedCenter);','if (!visitedCenters.Add(current)) continue;','costCenterList.Add(current);','queue.Enqueue(child);','GetParent(Convert.ToInt32(row["CCcode"]));'])
check('details expand descendants and revalidate membership',walk_contract(detail))
check('cycle check mutant rejected',not walk_contract(detail.replace('if (!visitedCenters.Add(current)) continue;','')))
check('selected-center omission mutant rejected',not walk_contract(detail.replace('queue.Enqueue(selectedCenter);','')))
def descendants(edges,root):
    seen=set();queue=[root];out=[]
    while queue:
        node=queue.pop(0)
        if node in seen:continue
        seen.add(node);out.append(node)
        queue.extend(child for parent,child in edges if parent==node)
    return out
for edges,root,expected in [([(1,2),(2,3),(3,4)],1,[1,2,3,4]), ([(1,2),(2,1),(2,3)],1,[1,2,3]), ([(1,2),(1,2),(8,9)],1,[1,2]), ([],5,[5])]:
    check('descendant traversal '+str((edges,root)),descendants(edges,root)==expected)

agg=part(cost,'private void ShowResult()','private void ProcessAndAddRow(')
def opening_contract(s):
    start=s.index('// Movement-driven rows miss')
    section=s[start:]
    return all(v in section for v in ['foreach (DataRow initRow in dt5.Rows)','foreach (DataRow movementRow in dt4.Rows)','initRow["CCcode"].ToString() == movementRow["CCcode"].ToString()','initRow["AccCode"].ToString() == movementRow["AccCode"].ToString()','if (hasMovement) continue;','GetParent(Convert.ToInt32(initRow["CCcode"]));','deptInit, creditInit, 0, 0, initRow["AccName"]'])
check('unmatched opening-only aggregate rows retain center and account',opening_contract(agg))
check('account comparison mutant detected',not opening_contract(agg.replace('initRow["AccCode"].ToString() == movementRow["AccCode"].ToString()','true')))
check('membership bypass mutant detected',not opening_contract(agg.replace('GetParent(Convert.ToInt32(initRow["CCcode"]));','')))
def combine(movement,opening):
    keys=set(movement)|set(opening)
    return {key:(opening.get(key,0),movement.get(key,0)) for key in keys}
model=combine({(1,10):7,(1,20):9},{(1,10):100,(1,20):200,(1,30):300,(2,10):400})
check('movement and opening-only account coexist',model=={(1,10):(100,7),(1,20):(200,9),(1,30):(300,0),(2,10):(400,0)})
check('movement-only account gets zero opening',combine({(1,9):3},{})[(1,9)]==(0,3))

analysis=read('Form_WPF/frmRptInvAnalysis.xaml.cs')
for begin,end in [('private void ShowResultGroup()','#region ShowResultItem'),('private void ShowResultItem()','#region ShowResultCust')]:
    section=part(analysis,begin,end)
    def discount_contract(s): return all(x in s for x in ['sum(ISNULL(inv_sub.discount,0)) as LineDiscount','double.TryParse(dt2.Rows[0]["LineDiscount"].ToString(), out netDiscount);','netTotal -= netDiscount;','double netProfit = netTotal - netCost;','Column5 = netTotal.ToString("N2")','Column10 = netDiscount.ToString("N2")'])
    check(begin+' uses line discount for total and profit',discount_contract(section))
    check(begin+' no-subtraction mutant rejected',not discount_contract(section.replace('netTotal -= netDiscount;','')))
db=sqlite3.connect(':memory:');db.execute('create table lines(q real, price real, discount real)');db.executemany('insert into lines values(?,?,?)',[(2,50,7),(1,20,None),(0.5,30,3)])
gross,discount=db.execute('select sum(q*price),sum(ifnull(discount,0)) from lines').fetchone()
check('fractional example captures gross and only line discounts',(gross,discount,gross-discount)==(135,10,125))
check('model profit reflects discount',gross-discount-80==45)

edit=read('Form_WPF/frmEditItems.xaml.cs')
save=part(edit,'private void BtnSave_Click(','#region Item Operations (Price Apply)')
def price_contract(s):
    return all(x in s for x in ['if (cmbUnit.SelectedIndex == -1 &&','unit.UnitId != item.MainUnit','if (mainUnit != null)','لم يتم حفظ التعديل.','if (!string.IsNullOrWhiteSpace(txtSalePrice.Text)) mainUnit.SalePrice = item.SalePrice;','if (!string.IsNullOrWhiteSpace(txtPurchPrice.Text)) mainUnit.PurchasePrice = item.PurchPrice;']) and s.index('if (mainUnit != null)')<s.index('new EntityOperations().SaveProducts(products)')
check('bulk edit aligns only explicit prices on existing unique main unit',price_contract(save))
check('sale price mutant detected',not price_contract(save.replace('mainUnit.SalePrice = item.SalePrice;','mainUnit.SalePrice = 0;')))
check('duplicate guard precedes persistence',save.index('الوحدة الرئيسية مكررة')<save.index('return;',save.index('الوحدة الرئيسية مكررة'))<save.index('SaveProducts(products)'))
def sync(units,main,sale=None,purchase=None):
    units=[dict(u) for u in units]; hits=[u for u in units if u['id']==main]
    if len(hits)>1:return None
    if hits:
        if sale is not None:hits[0]['sale']=sale
        if purchase is not None:hits[0]['purchase']=purchase
    return units
units=[dict(id=1,sale=10,purchase=6),dict(id=2,sale=25,purchase=15)]
check('one-sided price edit preserves other prices',sync(units,1,sale=12)==[dict(id=1,sale=12,purchase=6),units[1]])
check('missing main unit not invented',sync(units,3,sale=12)==units)
check('duplicate main unit rejected',sync(units+[dict(id=1,sale=8,purchase=5)],1,sale=12) is None)

tax=read('Form_WPF/frmTaxRptPeriod.xaml.cs')
taxpart=part(tax,'private InvoicePartTotals CalcInvoicePart(', '#endregion')
def untaxed_contract(s):
    return ('if (filterVatMode == "TAXED" && priceIncVat && itemsDiscount > 0.0 && vatPercent > 0.0)' in s
            and 'if (filterVatMode == "TAXED" && priceIncVat && vatPercent > 0.0)' in s
            and 'filterClause = "Inv_Sub.taxval = 0 AND Inv_Sub.ProductId = 0"' in s)
check('untaxed subtotal and line discounts are not divided by header tax rate',untaxed_contract(taxpart))
check('old untaxed subtotal division mutant rejected',not untaxed_contract(taxpart.replace('if (filterVatMode == "TAXED" && priceIncVat && vatPercent > 0.0)','if (priceIncVat && vatPercent > 0.0)')))
check('old untaxed discount division mutant rejected',not untaxed_contract(taxpart.replace('filterVatMode == "TAXED" && priceIncVat && itemsDiscount','priceIncVat && itemsDiscount')))
base=Decimal('100'); line_discount=Decimal('10'); rate=Decimal('1.15')
check('no-tax subset model keeps unscaled values',base-line_discount==Decimal('90'))
check('old divided amount differs from unscaled model',(base-line_discount)/rate != base-line_discount)

printer=read('Class/Print.cs');serial=part(printer,'// The persisted detail reader is keyed','invoiceData.CloudID = Inv.CloudID;')
def serial_contract(s): return all(x in s for x in ['Inv.InvoiceItems.Count(x => x.ItemId == invoiceItem.ItemId) == 1','string.Join(Environment.NewLine,','invoiceItem.InvoiceItemDetails','.Where(detail => !string.IsNullOrWhiteSpace(detail.ItemSerialNo))','.Select(detail => detail.ItemSerialNo)','else','invoiceData.ItemSerialNo = invoiceItemDetail.ItemSerialNo;'])
check('unambiguous item prints all nonempty in-memory serials',serial_contract(serial))
check('duplicate-line guard mutant rejected',not serial_contract(serial.replace('Inv.InvoiceItems.Count(x => x.ItemId == invoiceItem.ItemId) == 1','true')))
check('unresolved duplicate case preserves prior fallback', 'else' in serial and 'invoiceData.ItemSerialNo = invoiceItemDetail.ItemSerialNo;' in serial)
check('empty serial values omitted but order and duplicates retained', '\n'.join(x for x in ['S1','','S2','S1'] if x.strip())=='S1\nS2\nS1')
print('RESULT: PASS — %d source/model checks; not CLR, WPF, SQL Server, print or ERP acceptance.' % checks)
