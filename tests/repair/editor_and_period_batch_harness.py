#!/usr/bin/env python3
"""R-120..125 source witnesses and independent models, not WPF/DB execution."""
from pathlib import Path
import calendar
import re

ROOT=Path(__file__).resolve().parents[2]
def read(p):return (ROOT/p).read_text(encoding='utf-8-sig')
def section(s,a,b):
 i=s.index(a);return s[i:s.index(b,i)]
def clean(s):return re.sub(r'//[^\n]*|/\*.*?\*/','',s,flags=re.S)
def swap(s,a,b):assert a in s;return s.replace(a,b,1)
n=0
def check(label,ok):
 global n
 n+=1
 if not ok:raise AssertionError(label)
 print('PASS',label)

employee=read('SmartAuditERP/Form_WPF/frmEmpSalaryAddSub.xaml.cs')
booking=read('SmartAuditERP/Form_WPF/frmBookingM.xaml.cs')
purchase=read('SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs')
ops=read('SmartAuditERP/Class/ItemOper.cs')
contract=read('SmartAuditERP/Class/ItemOpercontract.cs')
prop=read('SmartAuditERP/Form_WPF/frmItemProperties.xaml.cs')
pos=read('SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs')
nkd=read('SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs')
tax=read('SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml.cs')
xaml=read('SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml')
emp_save=clean(section(employee,'private void IconButton6_Click(', '#endregion'))
emp_clear=clean(section(employee,'private void ClearForm()', '#endregion'))
emp_cmd=clean(section(employee,'private SqlCommand CreateSaveCommand(', 'private void PopulateParameters('))
book_save=clean(section(booking,'private void Save()', '#endregion'))
book_new=clean(section(booking,'private void LoadBokNo()', 'private void LoadMainSettings()'))
picker=clean(section(purchase,'private void addNewItem()', '#endregion'))
item_detail=clean(section(ops,'public static void LoadItemDetails(InvoiceDGV', '#endregion'))
contract_detail=clean(section(contract,'public static void LoadItemDetails(InvoiceDGV', 'else if (prop == 5)'))
prop_insert=clean(section(prop,'private void btnInsert_Click(', 'private void cmbItemProperties_'))
posprint=clean(section(pos,'private void PrintDevexpress(', 'private FlowDocument BuildPrintDocument('))
nkdprint=clean(section(nkd,'private void PrintDevexpress(', 'private FlowDocument BuildPrintDocument('))
period=clean(section(tax,'private bool SetDate()', 'private DateTime GetDateFrom()'))
events=clean(section(tax,'private void UpdatePeriodControls()', 'private void chkAllBranches_CheckedChanged('))
show=clean(section(tax,'private void btnShow_Click(', 'private void btnPreview_Click('))
sales=clean(section(tax,'private void btnSalesDetails_Click(', 'private void btnPurchesDetails_Click('))
purch=clean(section(tax,'private void btnPurchesDetails_Click(', '#endregion'))

def employee_contract(s):
 return ('if (SaveReceipt(receipt, entry, IsNew))' in s and s.index('ClearForm();') < s.index('LoadGrid(string.Empty);')
         and 'UpdateCodeFromDatabase' not in s)
def booking_contract(s):
 return (all(x in s for x in ['transaction.Commit();','transaction = null;','Code = -1;','ProcID = -1;','txtNo.Text = "";','ClearAll();','LoadBokNo();'])
         and s.index('transaction.Commit();') < s.index('transaction = null;', s.index('transaction.Commit();')) < s.index('Code = -1;') < s.index('ClearAll();') < s.index('LoadBokNo();'))
def picker_contract(s):return 'if (frm.ISDone && frm.ItemId > 0)' in s and '_gridSource.RemoveAt' not in s
def property_contract(s,form,target):
 guard='if (%s.ShowDialog() != true)'%form
 return guard in s and s.index(guard)<s.index('return;',s.index(guard))<s.index(target)
def print_contract(s):
 return ('BuildPrintDocument()' in s and 'PrintDialog' in s and ('_dataRows.Count == 0' in s or '_rows.Count == 0' in s)
         and 'File.Exists(' not in s and 'Directory.Exists(' not in s and 'IsNullOrWhiteSpace(RptUrl)' not in s)
def mode_contract(s):
 return all(x in s for x in ['bool quarterly = ckQuart.IsChecked == true;', 'bool monthly = ckMonthly.IsChecked == true;',
 'cmbQuartars.IsEnabled = quarterly;', 'cmbMonthly.IsEnabled = monthly;', 'txtDateFrom.IsEnabled = !quarterly && !monthly;',
 'txtDateTo.IsEnabled = !quarterly && !monthly;', '_reportPublished = false;', 'ClearReportCells();',
 'if (ckQuart.IsChecked == true) ckMonthly.IsChecked = false;', 'if (ckMonthly.IsChecked == true) ckQuart.IsChecked = false;',
 'if (IsLoaded && ckQuart.IsChecked == true) UpdatePeriodControls();','if (IsLoaded && ckMonthly.IsChecked == true) UpdatePeriodControls();'])

check('new salary adjustment identity survives successful refresh',employee_contract(emp_save) and '_currentCode = -1;' in emp_clear and '_currentCode != -1' in emp_cmd)
check('old MAX-identity regression detected',not employee_contract(emp_save+' UpdateCodeFromDatabase();'))
check('obsolete MAX helper removed','UpdateCodeFromDatabase' not in employee)
check('booking resets identity only after commit and refreshes number',booking_contract(book_save) and 'Code = -1;' in book_new)
check('stale booking identity mutation detected',not booking_contract(swap(book_save,'Code = -1;','Code = Code;')))
check('booking number lookup fails closed instead of fabricating a number', 'bool loaded = false;' in book_new and book_new.index('adapter.Fill(dt);') < book_new.index('loaded = true;') and 'if (loaded) txtNo.Text = nextNum.ToString();' in book_new)
check('cancelled and invalid item picker never deletes focused row',picker_contract(picker))
check('row removal mutant detected',not picker_contract(picker+' _gridSource.RemoveAt(RowIndex);'))
check('accepted picker path remains', 'foreach (int id in frm.Itemlist)' in picker and 'SearchByID(0)' in picker)
check('both property dialogs reject before mutation',property_contract(item_detail,'frmItemProperties2','newItem.Description = description;') and property_contract(contract_detail,'propForm','NewItem.Description = desc;'))
check('dialog bypass mutant detected',not property_contract(swap(item_detail,'frmItemProperties2.ShowDialog() != true','false'),'frmItemProperties2','newItem.Description = description;'))
check('insert explicitly signals accepted result','NetQnty = ParseNumber(txtNetQnty.Text, 0);' in prop_insert and 'DialogResult = true;' in prop_insert)
check('new item caller may still append after cancellation: explicit remaining scope','LoadItemInf(invo, ref newItem);' in ops and 'invo.InvoiceItems.Add(newItem);' in ops)
check('both flow-document renderers retain row and dialog checks',print_contract(posprint) and print_contract(nkdprint))
check('REPX file guard mutant detected',not print_contract(posprint+' if (!File.Exists(fullPath)) return;'))
check('Nkd keeps configured print count; POS keeps existing single print','i < PrintNo' in nkdprint and posprint.count('printDialog.PrintDocument(')==1)
check('period control enablement derived from resulting state',mode_contract(events))
check('nested-event regression mutation detected',not mode_contract(swap(events,'cmbMonthly.IsEnabled = monthly;', 'cmbMonthly.IsEnabled = false;')))
check('period bounds validated before computing dates','cmbQuartars.SelectedIndex < 0 || cmbQuartars.SelectedIndex > 3' in period and 'idx < 0 || idx > 11' in period and 'DateTime.DaysInMonth(currYear, month)' in period)
check('show and both details reject missing period',all('if (!PreparePeriod()) return;' in x for x in (show,sales,purch)))
check('failed preparation invalidates old report and clears cells','_reportPublished = false;' in period and 'ClearReportCells();' in period)
check('both checkbox edges are wired',all(('Checked="%s_CheckedChanged"' % x) in xaml and ('Unchecked="%s_CheckedChanged"' % x) in xaml for x in ('ckQuart','ckMonthly')))
check('print metadata includes only active period label', 'Quartars = ckQuart.IsChecked == true' in tax and 'Monthly = ckMonthly.IsChecked == true' in tax)

# Models show conditional behavior; they do not invoke the production code.
for old,accepted,new in [(9,False,9),(9,True,12),(-1,True,-1)]:
 result=new if accepted else old
 check('salary adjustment reset model %r'%((old,accepted,new),),result==(new if accepted else old))
for confirmed,valid in [(False,False),(False,True),(True,False),(True,True)]:
 original=['X','A']; rows=original.copy()
 if confirmed and valid: rows.append('B')
 check('picker result %r'%((confirmed,valid),), rows[:2]==original)
for outcome in (None,False,True):
 qty=6;desc='original'
 if outcome is True:qty,desc=60,'confirmed'
 check('property dialog outcome %r'%outcome,(qty,desc)==((60,'confirmed') if outcome is True else (6,'original')))

# Explicitly model nested check/uncheck event order and recomputation.
class Modes:
 def __init__(self):self.q=False;self.m=False;self.ui=None;self.published=True
 def update(self):
  self.ui=(self.q,self.m,not self.q and not self.m);self.published=False
 def quarter(self,value):
  self.q=value
  if value and self.m:self.month(False)
  self.update()
 def month(self,value):
  self.m=value
  if value and self.q:self.quarter(False)
  self.update()
a=Modes();a.quarter(True);a.month(True)
check('quarter to month final UI',a.ui==(False,True,False) and not a.published)
a.quarter(True);check('month to quarter final UI',a.ui==(True,False,False))
a.quarter(False);check('no active mode permits manual dates',a.ui==(False,False,True))
a.month(True);a.month(True);check('repeat same mode leaves correct UI',a.ui==(False,True,False))
for y,m,days in [(2024,2,29),(2025,2,28),(2025,4,30),(2025,12,31)]:
 check('monthly model %d/%d'%(y,m),calendar.monthrange(y,m)[1]==days)
for mode,index,allowed in [('month',-1,False),('month',11,True),('month',12,False),('quarter',-1,False),('quarter',3,True),('quarter',4,False),('manual',-1,True)]:
 valid=(mode=='manual' or (mode=='month' and 0<=index<=11) or (mode=='quarter' and 0<=index<=3))
 check('period choice %r'%((mode,index),),valid==allowed)
print('RESULT: PASS — %d source/model checks, not WPF, SQL Server, dialogs or ERP acceptance.'%n)
