#!/usr/bin/env python3
"""R-113..119 and earlier R-083: source witnesses and independent models.
No WPF/.NET, SQL Server, COM device, real print or ERP behavior is executed.
"""
from pathlib import Path
import re
import sqlite3

ROOT=Path(__file__).resolve().parents[2]
def read(path): return (ROOT/path).read_text(encoding='utf-8-sig')
def part(s,start,end):
 i=s.index(start);return s[i:s.index(end,i)]
def clean(s):return re.sub(r'//[^\n]*|/\*.*?\*/','',s,flags=re.S)
n=0
def check(label,condition):
 global n
 n+=1
 if not condition:raise AssertionError(label)
 print('PASS',label)

sales=read('SmartAuditERP/Form_WPF/frmRptSalesInPeriod.xaml.cs')
decision=read('SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs')
item=read('SmartAuditERP/Form_WPF/frmItems.xaml.cs')
pos=read('SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs')
salesedit=read('SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs')
search=read('SmartAuditERP/Form_WPF/frmSrchClient.xaml.cs')
accrual=read('SmartAuditERP/Form_WPF/FrmReseved.xaml.cs')
fp=read('SmartAuditERP/Class/FingerPrintDevice.cs')
cost=read('SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs')
logs=read('SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs')
export=read('SmartAuditERP/Class/SpreadsheetExport.cs')
inv=clean(part(sales,'private DataSet BuildReportDataSetInv()', 'private void PrintDevexpress('))
items=clean(part(sales,'private DataSet BuildReportDataSet()', 'private DataSet BuildReportDataSetInv()'))
choice=clean(part(salesedit,'private void toolCustomers_Click(', 'public void Chang_Customer()'))
change=clean(part(salesedit,'public void Chang_Customer()', 'private void RegenerateEntry('))
validate=clean(part(accrual,'private bool ValidateWorkDate(', 'private bool ValidateNetSalaryRow('))
save=clean(part(accrual,'private void btnSave_Click(', 'private void btnDelete_Click('))
load1=clean(part(accrual,'public void LoadDataToGridview(', 'public void Navigate('))
load2=clean(part(accrual,'private void LoadDataToGridview2(', '#endregion'))
fp=clean(fp[fp.index('public static void loadAttendData()'):])
restype=clean(part(cost,'private void cmbEntryType_SelectionChanged(', 'private void cmbAccounts_KeyDown('))
showcost=clean(part(cost,'public void ShowAccount()', 'private string BuildTypeFilter()'))
logexp=clean(part(logs,'private void btnExportExcel_Click(', '#endregion'))
write=clean(part(export,'public static void Write(', 'public static void WriteDataTable('))

def invoice_contract(s): return 'SumSell      = Math.Round(_sumSale2, 2).ToString("N2")' in s and 'SumSell      = txtSumSale.Text' not in s
def group_contract(s):
 s=clean(part(s,'public void LoadGroups()', '\n        }')).lower()
 return s.count('where type=2 order by id')==2

def client_contract(s,c):
 return ('if (addNewItem())' in s and s.index('if (addNewItem())') < s.index('Chang_Customer();')
 and s.index('form.ShowDialog();') < s.index('if (form.ClientId <= 0) return false;') < s.index('Client_id = form.ClientId.ToString();')
 and 'return false;' in s[s.index('catch (Exception ex)'):]
 and c.index('if (_Client_id <= 0)') < c.index('conn.Open();') < c.index('UPDATE inv SET Cust_id'))
def emp_contract(a,b,v,s):
 return (all('Emp       = Convert.ToInt32(row["id"])' in z and 'ISNULL(E.id,0) AS id' in z for z in (a,b))
 and all(z in v for z in ('if (empId <= 0)','if (dt.Rows.Count == 0)','catch (Exception ex)','return false;'))
 and s.index('ValidateWorkDate(row.Emp)') < s.index('EntryOper.GetEntryGlobalID(') < s.index('SaveReceipt1(')
 and '_res_emp      = row.Emp' in s)
def device_contract(s):
 return ('bFlag: true' in s and s.index('try') < s.index('conn.Open()') < s.index('BeginTransaction()') < s.index('enableAttemptNeeded = true;')
 < s.index('bFlag: false') < s.index('ReadGeneralLogData') < s.index('sqlTransaction.Commit()') < s.index('ClearGLog') < s.index('finally')
 and s.index('finally') < s.index('bFlag: true') < s.index('conn.Close()')
 and 'if (!FingerPrintDevice.axCZKEM1.EnableDevice' in s and 'Logger.Error' in s[s.index('finally'):])
def type_contract(s):
 return all(x in s for x in ('selectedIndex >= 0 && selectedIndex <= 13','selectedIndex >= 14 && selectedIndex <= 16','Restype = selectedIndex + 7;', 'Restype = -1;'))

def swap(s,a,b):
 assert a in s,a
 return s.replace(a,b,1)
check('invoice print uses invoice total and item print retains its own',invoice_contract(inv) and 'SumSell      = txtSumSale.Text' in items)
check('wrong-tab mutant detected',not invoice_contract(swap(inv,'Math.Round(_sumSale2, 2).ToString("N2")','txtSumSale.Text')))
check('both group loaders use same eligibility in both languages',group_contract(decision) and group_contract(item))
check('missing non-Arabic type filter mutant detected',not group_contract(swap(decision,'FROM ItemsCategory WHERE type=2 ORDER BY id";', 'FROM ItemsCategory";')))
check('POS retains quantity for multiplication and summaries', 'double val1 = Convert.ToDouble(row["val1"]);' in pos and 'DgvQty = val1,' in pos and 'Math.Round(val1 * exchPrice, 2)' in pos and 'qty += row.DgvQty;' in pos)
check('POS still formats quantities to two places: explicit remainder', 'Binding="{Binding DgvQty, StringFormat=N2}"' in read('SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml'))
check('cancel, missing ID and failed dialog do not invoke change',client_contract(choice,change))
check('cancel guard mutant detected',not client_contract(swap(choice,'if (addNewItem())','if (true)'),change))
check('fresh dialog defaults to zero and sets ID only on selected row', 'public int    ClientId        { get; set; }' in search and 'ClientId   = item.Id;' in search)
check('reload identity and prevalidation cover both paths',emp_contract(load1,load2,validate,save))
check('missing employee assignment mutation detected',not emp_contract(swap(load1,'Emp       = Convert.ToInt32(row["id"]),',''),load2,validate,save))
check('missing employee and query error do not become valid',validate[validate.index('if (dt.Rows.Count == 0)'):].count('return false;')>=3 and 'return false;' in validate[validate.index('catch (Exception ex)'):])
check('device recovery is in finally and protects SQL cleanup',device_contract(fp))
check('missing re-enable finally mutant detected',not device_contract(swap(fp,'bFlag: true','bFlag: false')) if 'bFlag: true' in fp else False)
check('disable result guards import and re-enable result is logged', 'if (!FingerPrintDevice.axCZKEM1.EnableDevice(FingerPrintDevice.iMachineNumber, bFlag: false))' in fp and 'if (!FingerPrintDevice.axCZKEM1.EnableDevice(FingerPrintDevice.iMachineNumber, bFlag: true))' in fp)
check('all three return entry types map and invalid clears selection',type_contract(restype))
check('unreachable return-index mutant detected',not type_contract(swap(restype,'selectedIndex >= 14 && selectedIndex <= 16','selectedIndex >= 21 && selectedIndex <= 23')))
check('missing type rejects before query and clears prior grid', all(x in showcost for x in ('chkEntryType.IsChecked != true && Restype < 0','GridControl1.ItemsSource = null;', 'ClearTotals();')) and showcost.index('Restype < 0') < showcost.index('LoadPeriodData('))
check('existing export saves before shell opens',logexp.index('export.Save();') < logexp.index('Process.Start('))
check('export Save delegates to writer and writer disposes at block end','Write(_path, _delimiter, _hasHeader ? _header : null, _rows);' in export and 'using (var sw = new StreamWriter(' in write)

# Independent fixtures, illustrating boundaries rather than executing production C#.
con=sqlite3.connect(':memory:')
con.execute('create table categories(id integer, name text, nameEn text, type integer)')
con.executemany('insert into categories values(?,?,?,?)',[(10,'Parent','Parent EN',1),(20,'Child','Child EN',2),(21,'Other','',2)])
a=con.execute('select id from categories where type=2 order by id').fetchall()
b=con.execute('select id from categories where type=2 order by id').fetchall()
check('language variants yield identical leaf identities',a==b==[(20,),(21,)])
for idx,expect in [(0,0),(13,13),(14,21),(15,22),(16,23),(-1,None),(17,None)]:
 got=idx if 0<=idx<=13 else idx+7 if 14<=idx<=16 else None
 check('entry-type mapping index %d' % idx,got==expect)
for quantity,price,gross in [(0.004,1000,4),(1.2346,100,123.46),(2,10,20)]:
 check('raw quantity gross %s x %s' % (quantity,price),abs(round(quantity*price,2)-gross)<0.0001)
check('signed invoice summary model',sum(v if p==1 else -v for p,v in [(1,100),(2,25)])==75)
for selected,old_id,changed in [(0,7,False),(7,7,True),(-1,7,False)]:
 calls=[]
 if selected>0:calls.append(selected)
 check('dialog model %d with prior %d' % (selected,old_id),bool(calls)==changed)
for selected in ([1,2],[1,0],[0],[]):
 employees={1,2}; validated=all(x>0 and x in employees for x in selected)
 writes=list(selected) if selected and validated else []
 check('employee batch model %r' % selected,writes==(selected if selected and 0 not in selected else []))

def device_model(failure):
 calls=[];need=False
 try:
  calls.append('open')
  if failure=='open':raise RuntimeError()
  calls.append('transaction');need=True;calls.append('disable')
  if failure=='disable':raise RuntimeError()
  calls.append('read')
  if failure=='read':raise RuntimeError()
  calls.extend(['commit','clear'])
 except RuntimeError:
  pass
 finally:
  if need:calls.append('enable')
  calls.append('close')
 return calls
for failure in (None,'open','disable','read'):
 calls=device_model(failure)
 check('device recovery model %r' % failure, ('enable' in calls)==(failure!='open') and calls[-1]=='close')
print('RESULT: PASS — %d source/model checks, not production execution.'%n)
