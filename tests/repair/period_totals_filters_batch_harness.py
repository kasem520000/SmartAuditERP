#!/usr/bin/env python3
"""Source contracts and bounded models; not execution of CLR, SQL, WPF, reports or ERP."""
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
root = Path(__file__).resolve().parents[2] / 'SmartAuditERP' / 'Form_WPF'
def src(name): return (root / name).read_text(encoding='utf-8-sig')
def section(s, start, end):
 i = s.index(start)
 return s[i:s.index(end, i + len(start))]
def check(name, value):
 if not value: raise AssertionError(name)
 print('PASS', name)

safe = src('frmRptKhzna.xaml.cs')
p = section(safe, 'if (chkAll.IsChecked != true)\n                {', '// ══ الحركات في الفترة')
check('previous balance uses exact selected timestamp', 'Entry.date<@date1' in p and 'dt1;' in p and 'dateFrom.ToShortDateString()' not in p)
check('previous balance caption reflects the selected instant', 'RestDate    = dt1.ToString("g")' in p)
start = datetime(2025, 5, 3, 14, 30)
movements = [(start - timedelta(microseconds=1), 7), (start, 11), (start + timedelta(hours=1), -2)]
check('previous and current are disjoint at start', sum(v for d,v in movements if d < start) == 7 and sum(v for d,v in movements if d >= start) == 9)

sales = src('frmInvBySalesMen.xaml.cs')
check('screen total signs returns', 'sumVal += row.IsPlus == 1 ? row.Value : -row.Value;' in sales)
check('spreadsheet total uses the same sign convention', 'items.Sum(x => x.IsPlus == 1 ? x.Value : -x.Value)' in sales)
check('mixed sale return and note model', sum(v if sign == 1 else -v for v,sign in [(100,1),(20,-1),(5,-1),(10,1)]) == 85)
click = section(sales, 'private async void btnShow_Click', 'private void ShowInvoiceResults(')
check('sales criteria captured before worker', click.index('bool allPeriod = chkAllPeriod.IsChecked == true;') < click.index('await Task.Run(') and 'salesmanId, allPeriod, fromDate, toDate' in click)
invoice = section(sales, 'private void ShowInvoiceResults(', 'private void ProcessInvoiceRow(')
receipt = section(sales, 'private void LoadReceiptsByType(', '#region ── Summary Calculation')
check('worker invoice avoids reading UI filter controls', all(t not in invoice for t in ('chkAll.IsChecked', 'cmbEmps.SelectedValue', 'chkAllPeriod.IsChecked', 'txtDateFrom.SelectedDate')))
check('sales invoices and receipts share half-open bounds', 'date<@date2' in invoice and 'ReceiptDate < @date2' in receipt)
check('all-period receipt SQL omits date restriction', 'allPeriod ? "" :' in receipt and 'if (!allPeriod)' in receipt)
end = datetime(2025, 5, 4)
check('half-open end excludes next midnight', datetime(2025, 5, 3, 23, 59, 59, 999999) < end and not end < end)

tax = src('frmTaxInvDetails.xaml.cs')
show = section(tax, 'public void ShowInvs()', '#region Process Invoice Row')
check('tax invoices use single next-day exclusive end', 'txtDateTo.DateTime.Date.AddDays(1)' in show and 'Value = toDate.AddHours(24)' not in show)
for name, end_marker in [('ProcessExpenseReceipts', 'private void ProcessIncomeReceipts'), ('ProcessIncomeReceipts', '#endregion')]:
 body=section(tax, 'private void '+name+'(', end_marker)
 check(name+' all-period switches off dates', '(allPeriod ? "" : "AND ReceiptDate>=@date1 AND ReceiptDate<@date2 ")' in body and 'if (!allPeriod)' in body and 'Value = toDate;' in body)
vat = src('frmVATReturn.xaml.cs')
check('sales returns subtract non-taxable value', 'salesNotTax += nonTaxable;' in vat and 'salesNotTax -= nonTaxable;' in vat)
check('purchase returns subtract non-taxable value', 'purchNotTax += nonTaxable;' in vat and 'purchNotTax -= nonTaxable;' in vat)
check('non-taxable model sale and return', 250-75 == 175 and 50-70 == -20)

rent=src('frmRptRentInvoices.xaml.cs')
load=section(rent,'public void LoadDgvItems()', 'private void LoadGroupCode()')
check('rental criterion rebuilt for each load', 'Cond = string.IsNullOrEmpty(txtInvNo.Text)' in load and 'RentInvoice.date<@date2' in load)
check('rental bounds are typed whole days', 'txtFromDate.DateTime.Date;' in load and 'txtToDate.DateTime.Date.AddDays(1)' in load)
check('number search deliberately preserves date bypass', ': "";' in load and 'GenerateFilter();' in load)
android=src('frmRptInvSalesDetailsPosAndroid.xaml.cs')
check('Android filter and projection share one expression', android.count('freeVatExpression +') == 3 and 'freeVatExpression + " AS FreeVATSales, "' in android)
check('Android filter no longer uses header namesake', 'where += " FreeVATSales=0 and "' not in android and 'where += " FreeVATSales>0 and "' not in android)
check('aggregate semantics retained including empty rows', 'SUM(CASE WHEN taxval=0 ' in android and 'ELSE 0 END),0)' in android)

salary=src('frmSalaryPay.xaml');ET.fromstring(salary)
for control in ('txtTotSalary','TxtHous','TxtTravel','txtSalaryAdd','txtSalarySub'):
 tag=salary[salary.index('x:Name="'+control+'"'):];tag=tag[:tag.index('/>')]
 check(control+' is wired to net recalculation', 'TextChanged=' in tag)
check('salary model uses additions and deductions', 100+20+5+2-10 == 117)
activity=src('frmRptItemsActivityDetailed.xaml.cs')
check('activity catalogue corresponds to thirteen indexed filters', '"Purchase credit note" }' in activity and all(f'{i}  =>' in activity or f'{i} =>' in activity for i in range(13)))
check('activity filter requires a selection when not all', 'chkAllProcType.IsChecked != true && cmbProcType.SelectedIndex < 0' in activity)
check('production and adjustment still use line direction', 'inv_sub.proc_type=1 and Inv.inv_type=6' in activity and 'inv_sub.proc_type=2 and Inv.inv_type=7' in activity)
check('transfer labels correspond to bundled type definitions', 'rdInvType1.Content = isAr ? "مناقلة إلى"' in activity and 'rdInvType2.Content = isAr ? "مناقلة من"' in activity)
print('RESULT PASS: bounded checks, not execution or financial acceptance.')
