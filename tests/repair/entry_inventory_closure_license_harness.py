#!/usr/bin/env python3
"""Source assertions and independent simplified models; NOT C# or SQL Server tests."""
from pathlib import Path
from decimal import Decimal
import sqlite3
root=Path(__file__).resolve().parents[2]/'SmartAuditERP'
def load(n):return (root/n).read_text(encoding='utf-8-sig')
def part(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def ordered(s,*parts):
 i=-1
 for t in parts:i=s.index(t,i+1)
 return True
entry=load('Class/EntryOper.cs')
validation=part(entry,'private static bool ValidateEntryBeforeSave(', 'public bool SaveEnty(')
for text in ('entry == null', 'string.IsNullOrWhiteSpace(entry.EntryGlobalID)', 'entry.Accounts == null',
 'account == null', 'int.TryParse(account.Code', 'code <= 0', 'int.TryParse(account.CCcode',
 'double.IsNaN(account.Debt)', 'double.IsInfinity(account.Credit)', 'account.Debt < 0',
 'account.Credit < 0', '(account.Debt > 0 && account.Credit > 0)', 'count == 0',
 'debit <= 0m', 'credit <= 0m', 'debit != credit', 'catch (OverflowException)'):
 assert text in validation,text
save=part(entry,'public bool SaveEnty(', '#endregion')
assert ordered(save,'ValidateEntryBeforeSave(entry', 'return false;', 'MainClass.ConnObj()', 'conn.BeginTransaction()', 'WriteEntryInTransaction(entry, conn, transaction, null)')
writer=part(entry,'internal void WriteEntryInTransaction(', 'public bool SaveEnty(')
assert ordered(writer, 'ValidateEntryBeforeSave(entry', 'expectedNew.HasValue', 'DELETE FROM Entry_Sub')
# Model policy only. C# uses Convert.ToDecimal(double) and is not executed here.
def valid(rows):
 if not rows:return False
 debit=credit=Decimal(0)
 for code,cc,d,c in rows:
  try:
   if int(code)<=0: return False
   int(cc); d=Decimal(d); c=Decimal(c)
   if not d.is_finite() or not c.is_finite() or d<0 or c<0 or (d>0 and c>0):return False
   debit+=d;credit+=c
  except (ValueError,TypeError,ArithmeticError):return False
 return debit>0 and credit>0 and debit==credit
base=[('100','-1','10','0'),('200','-1','0','10'),('222','-1','0','0')]
assert valid(base) and not valid([])
for rows in ([('0','-1','1','0'),('2','-1','0','1')],
 [('1','x','1','0'),('2','-1','0','1')], [('1','-1','NaN','0'),('2','-1','0','1')],
 [('1','-1','-1','0'),('2','-1','0','1')], [('1','-1','2','1'),('2','-1','0','1')],
 [('1','-1','0','0')], [('1','-1','10','0'),('2','-1','0','9')]):assert not valid(rows)
assert not valid([('1','-1','1.004','0'),('2','-1','0','1.003')])
assert valid([('1','-1','1.004','0'),('2','-1','0','1.004')])
assert not valid([('1','-1','1.006','0'),('2','-1','0','1.003')])
# Illustrates desired no-mutation-on-validation failure, not a SQL Server transaction.
db=sqlite3.connect(':memory:');db.execute('create table lines(v int)');db.execute('insert into lines values(42)')
invalid=[('1','-1','10','0'),('2','-1','0','9')]
if valid(invalid):db.execute('delete from lines')
assert db.execute('select v from lines').fetchall()==[(42,)]

inventory=load('Form_WPF/frmSafeGrd.xaml.cs')
calc=part(inventory,'public void CalcStock1()', 'private DataTable GetStockData(')
assert all(x in calc for x in ('ISDone = false','_Finished = false','_inventoryItems.Clear()','UpdateSummaries()', 'غير متاح'))
assert not any(x in calc for x in ('GetStockData(', 'GetAvgCost(', 'GetRecentPurchPrice(', '_inventoryItems.Add('))
approve=part(inventory,'private void BtnAprroved_Click(', 'private void BtnShowItem_Click(')
assert 'ISDone = false' in approve and 'ISDone = true' not in approve
for a,b in [('private void SearchByName()', 'private void SearchByCode()'),('private void SearchByCode()', 'private void OpenItemSearch()')]:
 s=part(inventory,a,b);assert '@search' in s and 'Parameters.Add("@search"' in s and "N'{txtItem" not in s

shift=load('Form_WPF/frmCloseShift.xaml.cs')
assert 'throw new InvalidOperationException' in part(shift,'public bool NoInvsFound(', 'public void closeShift(')
assert 'ShowOrdinaryCloseUnavailable();' in part(shift,'public void closeShift(', 'private void GetGlobalIdClose(')
for path,starts in [('Home.xaml.cs',['stripCloseCasher_Click','stripMarineCloseCasher_Click']),('Form_WPF/frmPOS.xaml.cs',['btnCloseDay_Click']),('Form_WPF/frmInvPOS.xaml.cs',['btnCloseDay_Click']),('Form_WPF/frminvoice.xaml.cs',['btnCloseDay_Click'])]:
 s=load(path)
 for start in starts:
  body=s[s.index('private void '+start+'('):]; body=body[:body.index('\n        }')]
  assert 'ShowOrdinaryCloseUnavailable();' in body and 'IsCashierClosed' not in body
android=load('Form_WPF/ClosShiftAndroid.xaml.cs');body=part(android,'public void closeShift(', '#region')
assert 'ShowOrdinaryCloseUnavailable();' in body and 'SaveEnty(' not in body
handler=part(android,'private void btnclose_Click(', 'private void ClosShiftAndroid_Load(')
assert 'this.closeShift(1);' in handler and 'closeofday =' not in handler
reader=part(android,'private CloseShift GetCloseData(', '#endregion')
assert 'set cash=tot_net' not in reader.lower() and 'set visa=tot_net' not in reader.lower()

permission=part(load('Class/Common.cs'), 'public static bool AllowEdit(', 'public static bool CheckProiedAcc(')
for check in ('MainClass.UserID <= 0', '@formName', '@userId', 'Parameters.Add("@formName"',
              'dt.Rows.Count == 1', '!= DBNull.Value', 'catch\n            {\n                return false;'):
 assert check in permission, check
assert 'ISNULL(IS_Edit,1)' not in permission
for f in ('Form_WPF/frmInvSale.xaml.cs','Form_WPF/frmInvPOS.xaml.cs'):
 assert 'allowEditInvoice = false;' in load(f)
# Simulate exact one explicit grant: zero, absent, null, duplicate and error deny.
def grant(rows, failure=False): return not failure and len(rows)==1 and rows[0] is True
assert grant([True]) and not any(grant(x) for x in ([],[None],[False],[True,True],[True,False]))
assert not grant([True],True)

for path in ('Form_WPF/FrmUpdate.xaml.cs','Form_WPF/frmServerSetting.xaml.cs'):
 s=load(path);assert 'UpdateLicenseEndDate' not in s and 'UPDATE License SET LicenseExpire' not in s
# Keep the separately scoped online license path outside this guarantee.
assert 'UpdateLicenseEndDate' in load('Class/ManagerOnline.cs')
print('PASS: entry validation, disabled unsafe valuation/closures and non-renewing connect/update (static + synthetic)')
