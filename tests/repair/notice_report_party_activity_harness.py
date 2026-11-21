#!/usr/bin/env python3
"""Static contracts and independent models; does not run WPF, CLR, reports or SQL Server."""
from pathlib import Path
from decimal import Decimal
R = Path(__file__).resolve().parents[2] / 'SmartAuditERP' / 'Form_WPF'
def read(n): return (R / (n + '.xaml.cs')).read_bytes().decode('utf-8', errors='replace')
def section(s,a,b): return s[s.index(a):s.index(b,s.index(a))]
def ordered(s,*xs):
    i=-1
    for x in xs:
        i=s.find(x,i+1)
        if i<0:return False
    return True
def check(name, value):
    assert value, name
    print('PASS',name)

notice=read('frmRptInvNotfic')
show=section(notice,'public void ShowInvoice()', '#region BindingListOfInvoices1')
load=section(notice,'public List<InvoiceTxt> BindingListOfInvoices1(', '#region Calculate Summaries')
printing=section(notice,'private void PrintDevexpress(', '#endregion')
check('stale notice rows cleared before load and on failure',show.count('_invoicesList = null;')==2 and ordered(show,'_invoicesList = null;','BindingListOfInvoices1(', '_invoicesList = loaded;', 'CalculateSummaries();'))
check('invalid or missing selection cannot broaden report', all(x in show for x in ['invType != 21 && invType != 22','cmbClients.SelectedIndex < 0','cmbusers.SelectedIndex < 0','cmbSaleman.SelectedIndex < 0','cmbInvType.SelectedIndex < 0','cmbInvType.SelectedIndex > 1']))
check('period captured from successful query not live controls', all(x in show for x in ['bool allPeriod = ckTotalPeriod.IsChecked == true','if (!allPeriod)','TimeSpan.TryParse','fromDate > toDate','allPeriod ? "الكل" : fromDate.ToString()','allPeriod ? "الكل" : toDate.ToString()']) and 'FromDate = _resultFrom' in printing and 'ToDate = _resultTo' in printing and 'txtFromDate' not in printing)
check('failure and duplicate identities cannot publish partial list', all(x in load for x in ['HashSet<string>','string.IsNullOrWhiteSpace(globalId) || !seen.Add(globalId)','catch (Exception ex)','throw new InvalidOperationException','catch\n            {\n                throw;']) and 'catch { }\n                    }' not in load)
check('print projects loaded invoices and summaries without null bridge',all(x in printing for x in ['foreach (var inv in _invoicesList)','new InventoryData','InvType = inv.InvoiceTypeTxt','Tax = inv.VAT.ToString("N2")','ExtraTax = inv.ExtraVAT.ToString("N2")','SummaryTotalTax = _sumTotalTax.ToString("N2")','NetTotal = _sumNet.ToString("N2")','UtilitiesProj.Common.ToDataTable(printRows)','report.Printing(printType, data']) and 'BindToData(' not in printing)
# Representative totals are independent, not a runtime test of conversion or DevExpress.
rows=[dict(total=Decimal('80'),tax=Decimal('12'),extra=Decimal('2')),dict(total=Decimal('20'),tax=Decimal('3'),extra=Decimal('1'))]
check('two-row total model',sum(r['tax']+r['extra'] for r in rows)==Decimal('18'))
check('duplicate model rejects second row',len({r['id'] for r in [{'id':'B-1'},{'id':'B-1'}]})!=2)

activity=read('frmRptItemsActivityDetailed')
last=section(activity,'public void LastProcess(', '#endregion')
check('last activity rejects missing item store and malformed party before query',ordered(last,'itemId <= 0 || storeId <= 0 || (clientId != -1 && clientId <= 0)','throw new InvalidOperationException','ShowResult();'))
cases=[('frmSalePurch','StripClientLastItem_Click','StripLastItem_Click','Convert.ToInt32(cmbClient.SelectedValue), 2);'),('frmPurchInv','StripClientLastActivity_Click','StripItemCost_Click','frm.LastProcess(itemId, storeId, custId, 2);'),('frmSalesInvoice','StripClientLastItem_Click','StripLastItem_Click','Convert.ToInt32(cmbClient.SelectedValue), InvType == 1 ? 2 : 1);'),('frmcontract','private void ItemClientActivity()','private void ItemCost1()','SafeGetSelectedValue<int>(cmbClient), InvType == 1 ? 2 : 1);'),('frmInvSale','private void ItemClientActivity()','private void ItemCost1()','custId, InvType == 1 ? 2 : 1);'),('frmInvInputOutput','CtxClientActivity_Click','CtxItemCost_Click','custId, InvType == 4 || InvType == 14 ? 2 : 1);'),('frmInvPOS','CtxClientActivity_Click','CtxItemSerialNo_Click','Invoic.Customer, 1);')]
for name,a,b,expected in cases:
    check(name+' uses its lookup party type',expected in section(read(name),a,b))
check('supplier no-selection does not become all', 'if (custId <= 0)' in section(read('frmPurchInv'),'StripClientLastActivity_Click','StripItemCost_Click'))
check('POS no-selection does not become all', 'if (Invoic.Customer <= 0)' in section(read('frmInvPOS'),'CtxClientActivity_Click','CtxItemSerialNo_Click'))
check('input/output malformed party cannot become all','custId <= 0' in section(read('frmInvInputOutput'),'CtxClientActivity_Click','CtxItemCost_Click'))
for invtype,lookup in [(4,2),(14,2),(5,1),(15,1)]:
    check('input/output type model '+str(invtype), (2 if invtype in (4,14) else 1)==lookup)
print('All notice report and party activity contracts passed.')
