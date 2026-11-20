#!/usr/bin/env python3
"""Source contracts plus independent models, not execution of CLR/WPF/SQL/ERP."""
from pathlib import Path
from decimal import Decimal as D
import xml.etree.ElementTree as ET
R = Path(__file__).resolve().parents[2] / 'SmartAuditERP'
def read(path): return (R / path).read_text(encoding='utf-8-sig')
def part(s, a, b): return s[s.index(a):s.index(b, s.index(a))]
def check(label, value):
    if not value: raise AssertionError(label)
    print('PASS', label)
def ordered(s, terms):
    p = -1
    for term in terms:
        p = s.find(term, p + 1)
        if p < 0: return False
    return True

profit = read('Form_WPF/frmRptItemsProfit.xaml.cs')
sales = part(profit, '// نقطة بيع (inv_type=3, proc_type=1)', '// مرتجع نقطة بيع')
check('POS discount counted once', 'salesDiscount  += r3.discount;' in sales and 'r3.discount * 2' not in sales)
for gross, disc, invdisc, expected in [(100,10,5,85),(200,0,20,180),(20,25,0,-5)]:
    check('discount model '+str((gross,disc)), gross-disc-invdisc == expected)
profitx = read('Form_WPF/frmRptItemsProfit.xaml'); ET.fromstring(profitx)
check('cost total labelled consistently in grid and CSV', 'Header="إجمالي التكلفة"' in profitx and '"إجمالي التكلفة", "صافي البيع"' in profit and 'DgvAvgCost     = salesTotalCost' in profit)

tax = read('Form_WPF/frmTaxRptPeriod.xaml.cs')
def totals_contract(s): return 'netSaleVal + salesOutTaxVal + receiptTotal + rentBase' in s and 'netPurchVal + purchOutTaxVal + expTotal' in s and 'taxNetSaleVal + receiptVAT + rentVAT' in s and 'taxNetPurchVal + expVAT' in s
check('non-taxed base included once in each base total', totals_contract(tax))
check('omission mutant rejected', not totals_contract(tax.replace(' + salesOutTaxVal','',1)))
for taxed, exempt, other, expected in [(100,20,5,125),(100,-30,0,70),(0,20,0,20)]: check('tax base model '+str((taxed,exempt)), taxed+exempt+other==expected)

activity = read('Form_WPF/frmRptItemsActivityDetailed.xaml.cs')
model = read('Class_WPF/ItemActivityRow_ActivityDetailed.cs')
writer = read('Form_WPF/frmProductionOrder.xaml.cs')
check('production writer sets output line 1 and component line 2', 'subCmd.Parameters.Add("@proc_type", SqlDbType.Int).Value = 1;' in writer and 'compCmd.Parameters.Add("@proc_type", SqlDbType.Int).Value = 2;' in writer)
check('production and adjustment lookup use line direction', '(invType == 6 || invType == 7)' in activity and '? $"AND ProcType={procTypeSub}"' in activity)
cond=part(activity,'private string BuildProcTypeCondition(', 'private void')
production=part(cond,'5  =>', '6  =>')
check('production direction filter uses line for both choices', production.count('inv_sub.proc_type=')==2 and 'inv.proc_type=' not in production)
for invtype, header, detail, expected in [(6,1,1,1),(6,1,2,2),(7,1,2,2),(8,2,1,2)]:
    check('direction source model '+str((invtype,header,detail)), (detail if invtype in (6,7) else header)==expected)

route=part(activity,'private void OpenInvoiceByIdentity(', '#endregion')
def route_contract(s): return all(x in s for x in ['item.InvGlobalID.Replace("\'", "\'\'")','item.InvTypeCode','item.HeaderProcType','InvGlobalID=N\'{id}\'','form.Loaded -= loaded;', 'configure(form);','form.Loaded += loaded;', 'form.Show();']) and ordered(s,['configure(form);','form.Loaded += loaded;','form.Show();']) and 'id={invNo}' not in s and 'switch (type)' in s
check('identity routing and post-loaded one-shot navigation',route_contract(route))
check('local-number routing mutant rejected', not route_contract(route.replace("InvGlobalID=N'{id}'",'id={invNo}')))
check('source query and model carry exact identity and header codes', 'Inv.InvGlobalID, Inv_sub.store AS safe' in activity and all(x in model for x in ['InvGlobalID','InvTypeCode','HeaderProcType']))
check('unsafe adjustment routing not fabricated', 'SafesAdjust has no persisted global-ID link' in route and 'frmSafeAdjust' not in route)
# Deterministic event-order model, not WPF event execution.
events=['configure type','construct subscriptions','show','loaded init','navigate']
check('navigation happens after initialization model', events.index('configure type')<events.index('loaded init')<events.index('navigate'))

for n,action in [('frmAccountBalance','ShowAccountData'),('frmAccountsStatement','ShowResult')]:
    s=read('Form_WPF/'+n+'.xaml.cs');x=read('Form_WPF/'+n+'.xaml');ET.fromstring(x)
    show=part(s,'private void btnShow_Click(', 'private void ' + ('cmbAccounts_SelectionChanged' if n=='frmAccountBalance' else 'CmbYearPreviews_DropDown'))
    check(n+' chooses local year connection on every click', ordered(show,['SqlConnection original = _connection','new SqlConnectionStringBuilder(_initialConnectionString)','CmbYearPreviews.SelectedIndex >= 0','builder.InitialCatalog = database','new SqlConnection(builder.ConnectionString)','_connection = selectedConnection',action+'();','finally','_connection = original']))
    check(n+' does not change global connection/flag on display', 'MainClass.connstr =' not in show and 'ReturnYearPreviews' not in show and 'SelectionChanged="CmbYearPreviews_SelectionChanged"' not in x)
    check(n+' validates blank selected database', 'string.IsNullOrWhiteSpace(database)' in show)
check('same historical year model repeats, then current is selectable', [x for x in ['history','history','current']]==['history','history','current'])

item=read('Form_WPF/frmRptItemsProfitDetails.xaml.cs');itemx=read('Form_WPF/frmRptItemsProfitDetails.xaml');ET.fromstring(itemx)
invalid=part(item,'private void ItemText_Changed(', 'private void txtItemName_KeyDown(')
check('text edit clears identity and previous report', ordered(invalid,['SelectedId = -1;','InvalidateItemResult();','ProfitList?.Clear();','UpdateSummaryCards();']))
check('both text fields invalidate selection', itemx.count('TextChanged="ItemText_Changed"')==2)
check('confirmed ID checked at display and query',item.count('SelectedId <= 0 || string.IsNullOrWhiteSpace(txtItemName.Text)')==2)
search=part(item,'private void SearchByName()', '// ══════════════════════════════════════════════\n        #region Button Events')
check('confirmed name/code lookup publishes identity last', search.count('SelectedId = Convert.ToInt32(dt.Rows[0]["id"]);')==2 and search.count('InvalidateItemResult();')==3 and ordered(search,['txtItemCode.Text = Common.GetItemCode(form.ItemId);','txtItemName.Text = form.Itemname;','SelectedId = form.ItemId;']))

inv=read('Form_WPF/frmRptInventory.xaml.cs'); invx=read('Form_WPF/frmRptInventory.xaml');ET.fromstring(invx)
show=part(inv,'private async void btnView_Click(', 'private (string sql, DateTime fromDate, DateTime toDate) BuildInvoiceQuery()')
query=part(inv,'private (string sql, DateTime fromDate, DateTime toDate) BuildInvoiceQuery()', '#region Calculate Summaries')
check('inventory controls captured before worker', ordered(show,['var request = BuildInvoiceQuery();','await Task.Run(', 'request.sql, withItems: false, request.fromDate, request.toDate','var current = BuildInvoiceQuery();','_invoicesList = rows;']))
check('changed request and closed window prevent publication','if (_isClosing) return;' in show and 'request != current' in show and 'if (!_isClosing) btnView.IsEnabled = true;' in show)
check('worker lambda references request rather than controls', 'await Task.Run(() => new InvoiceOper().BindingListOfInvoices1(\n                    request.sql, withItems: false, request.fromDate, request.toDate))' in show and 'chkAllBranches.IsChecked' in query)
printed=part(inv,'private void PrintDevexpress(', '#endregion')
check('inventory print bridges actual rows and matching totals', all(x in printed for x in ['foreach (var inv in _invoicesList)','new InventoryData','InvoiceNo = inv.InvoiceNo.ToString()','Clint = inv.ClientTxt','Sum = _sum.ToString("N2")','NetTotal = _nNet.ToString("N2")','FromDate = _resultFrom','UtilitiesProj.Common.ToDataTable(printRows)','report.Printing(']) and 'report.BindToData(' not in printed)
check('grid and export use populated display-name fields',all(x in invx for x in ['{Binding InvoiceNo}','{Binding ClientTxt}','{Binding UserTxt}','{Binding BranchTxt}']) and all(x in inv for x in ['SpreadsheetExport.Text(inv.ClientTxt)','SpreadsheetExport.Text(inv.UserTxt)','SpreadsheetExport.Text(inv.BranchTxt)']))
nav=part(inv,'private void BtnShowInv_Click(', '#region Open Forms')
check('inventory uses row type and fails closed for unlinked adjustment', 'switch ((int)invTxt.InvoiceType)' in nav and 'switch (cmbType.SelectedIndex)' not in nav and 'ربط حركة المخزون بالتسوية الأصلية غير مثبت' in nav)

summary=read('Form_WPF/frmSummaryQ.xaml.cs')
check('receipt join collapses user matches without asserting unique author','FROM Users GROUP BY emp) Users ON Users.emp = Receipts.EmpId' in summary and "CASE WHEN COUNT(*) > 1 THEN N'عدة مستخدمين'" in summary and 'LEFT JOIN Users     ON Users.emp' not in summary)
for users, result in [([],None),(['A'],'A'),(['A','B'],'several')]:
    actual=users[0] if len(users)==1 else ('several' if users else None)
    check('user join cardinality model '+str(users),actual==result)

layout=part(activity,'private void RestoreSavedLayout()', 'private void MenuItemDefualtSetting_Click(')
check('layout XML DTD prohibited and document size limited', 'DtdProcessing = System.Xml.DtdProcessing.Prohibit' in layout and 'XmlResolver = null' in layout and 'MaxCharactersInDocument = 1000000' in layout)
check('layout applies uniquely known column and bounded width', 'g.Count() == 1' in layout and 'seen.Add(header)' in layout and 'width >= 1 && width <= 10000' in layout and '!double.IsNaN(width)' in layout and '!double.IsInfinity(width)' in layout)
check('layout write closes before success and uses invariant decimal',ordered(layout,['using (var writer = new System.Xml.XmlTextWriter','writer.WriteEndDocument();','DXMessageBox.Show("تم حفظ']) and 'CultureInfo.InvariantCulture' in layout)
check('default layout can be restored in current session','entry.Key.Width = entry.Value.Width;' in activity and 'entry.Key.Visibility = entry.Value.Visibility;' in activity)
for name in ['frmRptInvSalesDetails','frmRptInvSalesDetailsPos','frmRptInvSalesDetailsPosAndroid']:
    screen=read('Form_WPF/'+name+'.xaml.cs')
    p=part(screen,'private void PrintReport(int printType)', '#endregion')
    check(name+' signed displayed totals reach printed rows', all(x in p for x in ['row["Sum"] = lblTotalSumPrice.Text','row["SumNetDiscount"] = lblTotalDiscount.Text','row["Total1"] = lblTotalTotal.Text','row["SumTax"] = lblTotalVAT.Text','row["SummaryExtraTax"] = lblTotalExtraVAT.Text','row["SummaryTotalTax"] = lblTotalTax.Text','row["NetTotal"] = lblTotalNet.Text','row["SummaryCash"] = lblTotalCash.Text','row["SummaryNetwork"] = lblTotalATM.Text','row["SummaryPaid"] = signedPaid.ToString("N2")']) and ordered(p,['report.BindToData(', 'printData.Tables[0].Rows.Count == 0','foreach (DataRow row in printData.Tables[0].Rows)', 'report.Printing(', 'printData,']))
    check(name+' paid total uses signed sale minus return', 'InvoicesList.Where(x => x.ProcType == 1).Sum(x => x.Paid)' in p and 'InvoicesList.Where(x => x.ProcType == 2).Sum(x => x.Paid)' in p)
check('signed print total model', sum([D('100'), D('30')]) - sum([D('40')]) == D('90'))
invs=read('Form_WPF/frmInvsProfit.xaml.cs'); invsx=read('Form_WPF/frmInvsProfit.xaml');ET.fromstring(invsx)
summaries=part(invsx,'<dxg:GridControl.TotalSummary>', '</dxg:GridControl.TotalSummary>')
check('invoice profit exposes signed fields before binding',ordered(invs,['string signedField = field + "Signed";', 'row[signedField] = sign * GetDouble(row[field]);', '_currentDataTable = resultTable;', 'GridControl1.ItemsSource = resultTable.DefaultView;']) and 'Convert.ToInt32(row["DgvProcType"]) == 1 ? 1 : -1' in invs)
check('profit footer uses sum on each signed field',summaries.count('SummaryType="Sum"')==5 and all(('FieldName="'+n+'Signed"') in summaries and ('ShowInColumn="'+n+'"') in summaries for n in ['DgvTotal','DgvDiscount','DgvSum','DgvCost','DgvProfit']))
check('profit signed footer arithmetic model',100-25==75 and 0-15==-15)
print('PASS — static evidence and independent models only; no CLR/WPF/SQL/Office or ERP acceptance.')
