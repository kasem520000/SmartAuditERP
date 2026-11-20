#!/usr/bin/env python3
"""Source contracts and independent models. Does not run C#, WPF, SQL or Office."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[2]/'SmartAuditERP'
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def part(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def check(label,condition):
 if not condition:raise AssertionError(label)
 print('PASS',label)
def ordered(s,ls):
 k=-1
 for item in ls:
  k=s.find(item,k+1)
  if k<0:return False
 return True

activity=read('Form_WPF/frmRptItemsActivity.xaml.cs')
a=part(activity,'// R-135 (P7-056)', '// حساب الرصيد')
def activity_contract(s):
 return all(x in s for x in [
 'transToVal = GetSumVal(itemDbId, 8, 1, branchFilter, extraFilter, dateFrom, dateTo, isProcOnInv: true)',
 'transFrVal = GetSumVal(itemDbId, 8, 2, branchFilter, extraFilter, dateFrom, dateTo, isProcOnInv: true)',
 'safeAdjVal = GetSumVal(itemDbId, 7, 1, branchFilter, extraFilter, dateFrom, dateTo, isProcOnSub: true)',
 'safeAdjRet = GetSumVal(itemDbId, 7, 2, branchFilter, extraFilter, dateFrom, dateTo, isProcOnSub: true)'])
check('activity transfer uses 8/head; adjustment uses 7/detail',activity_contract(a))
check('activity swapped type mutant detected',not activity_contract(a.replace('itemDbId, 8, 1','itemDbId, 7, 1')))
adjust=read('Form_WPF/frmSafeAdjust.xaml.cs');transfer=read('Form_WPF/frmInventoryTransfer.xaml.cs')
check('adjustment writer places type 7 in header and direction in line','SqlDbType.Int     ).Value = 7;' in adjust and 'SqlDbType.Int     ).Value = procType;' in adjust)
check('transfer writer creates head directions 1 and 2','public int InvType = 8;' in transfer and 'public int ProcType = 2;' in transfer and '_invoic.ProcType = 1;' in transfer)
for adjustment_in,adjustment_out,transfer_in,transfer_out,expected in [(7,2,3,4,4),(0,8,0,0,-8),(0,0,4,1,3)]:
 check('activity signs model '+str((adjustment_in,adjustment_out,transfer_in,transfer_out)),adjustment_in-adjustment_out+transfer_in-transfer_out==expected)

income=read('Form_WPF/IncomeStatementForm.xaml.cs'); handler=part(income,'private void btnExport_Click(', 'private void ExportToExcel(');writer=part(income,'private void ExportToExcel(', '#endregion')
def export_contract(h,w):return all(x in h for x in ['Filter = "CSV Files (*.csv)|*.csv"','DefaultExt = ".csv"','AddExtension = true','Path.GetExtension(saveDialog.FileName)','StringComparison.OrdinalIgnoreCase']) and ordered(h,['Path.GetExtension(saveDialog.FileName)','ExportToExcel(saveDialog.FileName);','"تم التصدير بنجاح!', 'Process.Start(new ProcessStartInfo(saveDialog.FileName)']) and 'SpreadsheetExport.Begin(filePath, SpreadsheetExport.CsvDelimiter)' in w and '.Replace(".xlsx", ".csv")' not in w
check('income CSV uses selected path for writer, success message and open',export_contract(handler,writer))
check('renamed-path mutant detected',not export_contract(handler,writer.replace('Begin(filePath,','Begin(filePath.Replace(".xlsx", ".csv"),')))
for suffix,accepted in [('.csv',True),('.CSV',True),('.xlsx',False),('',False)]:check('income extension model '+suffix,(suffix.lower()=='.csv')==accepted)

stock=read('Form_WPF/frmMezanyaArba7.xaml.cs');calc=part(stock,'// حساب المخزون','DataRow[] inventoryExisting');approve=part(stock,'private void BtnStock_Click(', '#endregion')
def stock_contract(c,a):return '(_hasApprovedStock || _Stock != 0.0)' in c and ordered(a,['safeGrd.ShowDialog();','if (safeGrd.ISDone)','_Stock = safeGrd._stockTotal;','_hasApprovedStock = true;'])
check('approved zero is distinct from no stock choice',stock_contract(calc,approve))
check('zero sentinel mutant detected',not stock_contract(calc.replace('(_hasApprovedStock || _Stock != 0.0)','_Stock != 0.0'),approve))
for done,value,auto,result in [(False,0,42,42),(True,0,42,0),(True,20,42,20),(False,20,42,20)]:
 actual=value if done or value!=0 else auto
 check(f'approved stock model {done} {value}',actual==result)

logs=read('Form_WPF/frmrptUsersRecords.xaml.cs');xaml=read('Form_WPF/frmrptUsersRecords.xaml');ET.fromstring(xaml)
show=part(logs,'private async void ShowResults()', '#endregion'); invalid=part(logs,'private void InvalidateResults()', 'private async void ShowResults()')
def request_contract(s):return (ordered(s,['long request = ++_requestGeneration;','LogList.Clear();','await Task.Run(', 'if (_isClosed || request != _requestGeneration) return;', 'var rows = new List<UserLogRow>();', 'foreach (var row in rows) LogList.Add(row);']) and s.count('if (_isClosed || request != _requestGeneration) return;')==2 and 'new SqlConnection(_connectionString)' in s and 'command.Parameters.Add("@EmpId", SqlDbType.Int)' in s and 'cmbUsers.SelectedIndex < 0' in s and 'int.TryParse(cmbUsers.SelectedValue?.ToString(), out int selectedId)' in s and 'selectedId <= 0' not in s and 'selectedId < 0' not in s and 'LogList.Clear();' in s[s.index('catch (Exception ex)'):])
check('request publication, stale failure and independent connection guarded',request_contract(show))
check('stale request guard mutant detected',not request_contract(show.replace('if (_isClosed || request != _requestGeneration) return;', '',1)))
check('zero-valued employee IDs are not rejected by an invented positivity rule','selectedId <= 0' not in show and 'selectedId < 0' not in show)
check('connection captured at construction before later query use','_connectionString = conn.ConnectionString;' in logs and logs.index('_connectionString = conn.ConnectionString;')<logs.index('private void LoadEmps()'))
check('filter changes and window close invalidate outstanding results','SelectionChanged="cmbUsers_SelectionChanged"' in xaml and 'if (IsLoaded) InvalidateResults();' in logs and '_isClosed = true;' in invalid and '_requestGeneration++;' in invalid and 'LogList?.Clear();' in invalid)
# Deterministic scheduler model, not async WPF/SQL execution.
class Model:
 def __init__(self):self.gen=0;self.closed=False;self.rows=[];self.errors=[]
 def start(self):self.gen+=1;self.rows=[];return self.gen
 def invalidate(self):self.gen+=1;self.rows=[]
 def close(self):self.closed=True;self.invalidate()
 def finish(self,g,rows=None,fail=False):
  if self.closed or g!=self.gen:return
  if fail:self.rows=[];self.errors.append(g)
  else:self.rows=list(rows)
m=Model();a=m.start();b=m.start();m.finish(b,['B']);m.finish(a,['A']);check('newer result wins even if older completes last',m.rows==['B'])
m=Model();a=m.start();b=m.start();m.finish(b,['B']);m.finish(a,fail=True);check('stale failure does not clear or alert',m.rows==['B'] and not m.errors)
m=Model();a=m.start();m.invalidate();m.finish(a,['A']);check('filter change invalidates in-flight result',not m.rows)
m=Model();a=m.start();m.close();m.finish(a,['A']);check('closed window ignores result',not m.rows)
m=Model();a=m.start();m.finish(a,fail=True);check('current failure leaves no rows and reports error',not m.rows and m.errors==[a])
print('PASS — source contracts and models only; no C#, WPF, SQL, Office or ERP acceptance.')
