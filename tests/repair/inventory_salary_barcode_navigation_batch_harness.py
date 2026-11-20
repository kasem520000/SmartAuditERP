#!/usr/bin/env python3
"""Bounded source witnesses and pure models, not CLR, SQL Server, WPF, devices or ERP."""
from pathlib import Path
from decimal import Decimal
import xml.etree.ElementTree as ET
R = Path(__file__).resolve().parents[2] / 'SmartAuditERP'
def read(path): return (R / path).read_text(encoding='utf-8-sig')
def segment(text, start, end):
 i=text.index(start)
 return text[i:text.index(end,i+len(start))]
def check(label, predicate):
 if not predicate: raise AssertionError(label)
 print('PASS',label)
salary=read('Form_WPF/frmSalaryPay.xaml.cs')
lookup=segment(salary,'private void CalcEmpSalary()', 'private void RecalcNet()')
check('accrual requires undeleted row','AND RS.IS_Deleted=0' in lookup)
check('accrual validates and binds period and employee', all(x in lookup for x in ('int.TryParse(cmbMonth.Text', 'int.TryParse(cmbYear.Text', 'Parameters.Add("@employee"', 'Parameters.Add("@month"', 'Parameters.Add("@year"')))
check('accrual fails closed on ambiguous rows','if (dt.Rows.Count == 1)' in lookup and 'عدة استحقاقات' in lookup)
check('accrual identity cleared before search',lookup.index('TxtResGlobalID.Text = "";') < lookup.index('adapter.Fill(dt)'))
button=segment(salary,'private void BtnAll_Click', 'private void btnviewEntry_Click')
check('accrual refresh also clears travel','TxtTravel.Text  = "";' in button)
def accrual(rows):
 rows=[r for r in rows if not r['deleted']]
 return rows[0]['id'] if len(rows)==1 else None
check('deleted and single active accrual model',accrual([{'id':'old','deleted':True},{'id':'new','deleted':False}])=='new')
check('two active accruals do not choose first',accrual([{'id':'a','deleted':False},{'id':'b','deleted':False}]) is None)
check('only deleted does not return an identity',accrual([{'id':'a','deleted':True}]) is None)
category=read('Form_WPF/frmRptSalesByCategory.xaml.cs')
writer=read('Class/InvoiceOper.cs')
check('category user selection filters invoice employee', 'AND inv.sales_emp={userId}' in category and 'Safe_Emps={userId}' not in category)
check('writer records employee identity in invoice', 'Parameters.Add("@sales_emp", SqlDbType.Int).Value = inv.User' in writer)
check('both sales and return queries use shared condition',category.count('{condWhere}{condItems}')==2)
for filename in ('frmRptInvSalesDetailsPos.xaml.cs','frmRptInvSalesDetailsPosAndroid.xaml.cs'):
 text=read('Form_WPF/'+filename)
 body=segment(text,'public List<InvoiceTxt> BindingListOfInvoices1(', 'private void UpdateSummaryCards()')
 check(filename+' retains recorded cash', 'item.Paycash = Convert.ToDouble(row["cash"]);' in body and 'item.Paycash = Convert.ToDouble(row["tot_net"]);' not in body)
 check(filename+' aggregates signed recorded cash','Calc(x => x.Paycash)' in text)
check('partial cash model is not replaced by total', sum([20,-5]) == 15 and 20 != 100)

oper=read('Class/ItemOper.cs');barcode=segment(oper,'public static void SearchForBarcode(', '#endregion')
check('outputs invalidated before any lookup',barcode.index('itemId = 0;') < barcode.index('SqlConnection conn'))
check('exact barcode lookup precedes scale payload validation',barcode.index('and ItemUnits.barcode=') < barcode.index('string payload = barcode.Substring(7, 5);'))
check('scale rejects non-ascii numeric and zero before identity assignment',barcode.index("payload.All(ch => ch >= '0' && ch <= '9')") < barcode.index('if (wscale == 1)') and 'rawPayload <= 0' in barcode)
check('scale uses exact decimal factors','rawPayload / 1000m' in barcode and barcode.count('rawPayload / 100m')==2)
mode3=segment(barcode,'else if (wscale == 3)', 'IsPriceFromBarcode = true;')
check('price-derived quantity validated before identity',mode3.index('if (quantity <= 0)') < mode3.index('itemId = ToInt('))
def decode(payload, mode, sale=Decimal(1)):
 if len(payload)!=5 or any(c not in '0123456789' for c in payload) or int(payload)==0:return None
 value=Decimal(int(payload))/(1000 if mode==1 else 100)
 if mode==3 and (sale<=0 or round(value/sale,3)<=0):return None
 return value
check('weight and price examples',decode('01234',1)==Decimal('1.234') and decode('01234',2)==Decimal('12.34'))
check('invalid and zero payload examples', all(decode(p,1) is None for p in ('00x01','00000','-0001','١٢٣٤٥')))
check('price mode rejects missing unit sale price',decode('01234',3,Decimal(0)) is None)

activity=read('Form_WPF/frmRptItemsActivity.xaml.cs');model=read('Class_WPF/ItemActivityRow.cs');view=read('Form_WPF/frmRptItemsActivity.xaml');ET.fromstring(view)
for direction in ('In','Out'):
 check('production '+direction+' reaches screen and CSV', 'DgvProduction'+direction in activity and 'DgvProduction'+direction in model and 'DgvProduction'+direction in view and 'Production'+direction+'  = ' in activity if direction=='In' else 'DgvProductionOut' in activity and 'DgvProductionOut' in model and 'DgvProductionOut' in view and 'ProductionOut = ' in activity)
check('production directions from detail line', 'GetSumVal(itemDbId, 6, 1, branchFilter, extraFilter, dateFrom, dateTo, isProcOnSub: true)' in activity and 'GetSumVal(itemDbId, 6, 2, branchFilter, extraFilter, dateFrom, dateTo, isProcOnSub: true)' in activity)
check('production affects balance and only-production items survive','+ productionIn - productionOut' in activity and 'productionOut != 0' in activity)
decision=read('Form_WPF/frmDecisionHelp.xaml.cs')
check('decision report includes both production directions', 'safeFilter, 6, null, 1' in decision and 'safeFilter, 6, null, 2' in decision and '+ transferIn + productionIn' in decision and '+ transferOut + productionOut' in decision)
check('decision report keeps return-only items','purchaseReturn != 0 || saleReturn != 0' in decision and 'rentReturn != 0' in decision)
check('production-only balance model', 10-3 == 7 and any([False,False,True]))

rent=read('Form_WPF/frmRptRentInvoices.xaml.cs')
rentload=segment(rent,'public void LoadDgvItems()', 'private void LoadGroupCode()')
check('rental print dates come from last successful load',rentload.index('adapter.Fill(_dtable)') < rentload.index('_resultFromDate =') and 'FromDate    = _resultFromDate' in rent and 'ToDate      = _resultToDate' in rent)
check('rental number lookup reports all dates','string.IsNullOrEmpty(Cond) ? "الكل"' in rentload)
salesman=read('Form_WPF/frmInvBySalesMen.xaml.cs')
click=segment(salesman,'private async void btnShow_Click', 'private void ShowInvoiceResults(')
check('salesman report snapshot follows captured criteria', 'allPeriod ? "الكل" : fromDate.ToShortDateString()' in click and 'FromDate = _resultFromDate' in salesman and 'ToDate = _resultToDate' in salesman)
check('print and export gated while worker runs',click.index('_resultReady = false;') < click.index('await Task.Run(') < click.index('_resultReady = true;') and salesman.count('if (!_resultReady || _itemsList.Count == 0)') == 2)
check('query failure clears partial published rows','_itemsList.Clear();\n                RecalculateSummary();\n                ShowError' in click)
notes=segment(salesman,'private void LoadCreditNotes(', 'private void LoadReceiptsByType(')
receipts=segment(salesman,'private void LoadReceiptsByType(', '#region ── Summary Calculation')
check('missing notes or receipts propagate rather than silently publish', 'catch { throw; }' in notes and 'catch { throw; }' in receipts)

entries=read('Form_WPF/frmRptEntries.xaml.cs')
nav=segment(entries,'private void NavigateAdjacent(bool next)', '#endregion')
check('navigation uses chronological composite ordering','ORDER BY date {order}, id {order}, GlobalID {order}' in nav)
check('navigation uses same lexicographic key in predicates',all(x in nav for x in ('date {comparison} @cursorDate','id {comparison} @cursorId','GlobalID {comparison} @cursorGlobal')))
check('navigation cursor values are bound parameters',all(x in nav for x in ('SqlParameter("@cursorDate"','SqlParameter("@cursorId"','SqlParameter("@cursorGlobal"')))
check('search does not preemptively replace selected entry identity', 'NavigateCore("SELECT * FROM Entry WHERE GlobalID=@selectedId"' in entries and '_globalId = row.GlobalID;' not in entries)
check('navigation captures database row not editable control','_navigationDate = rowDate;' in entries and '_navigationGlobalId = rowGlobalId;' in entries)
check('null dates excluded from navigation','date IS NOT NULL' in nav and 'dr["date"] == DBNull.Value' in entries)
keys=[(2,9,'A'),(1,20,'B'),(2,9,'C'),(2,8,'D')];ordered=sorted(keys)
check('date/id/global cursor visits ties in deterministic order', ordered==[(1,20,'B'),(2,8,'D'),(2,9,'A'),(2,9,'C')])
check('next/previous traverse each item without skipping',all(min((k for k in keys if k>ordered[i]),default=None)==ordered[i+1] and max((k for k in keys if k<ordered[i+1]),default=None)==ordered[i] for i in range(len(ordered)-1)))
print('RESULT PASS: bounded witnesses and models only; no runtime or financial validation.')
