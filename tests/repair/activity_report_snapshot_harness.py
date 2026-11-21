#!/usr/bin/env python3
"""Static contracts plus independent SQLite and state models; not CLR, WPF or SQL Server."""
from pathlib import Path
import sqlite3
s=(Path(__file__).resolve().parents[2]/'SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs').read_text(encoding='utf-8-sig')
def section(a,b):return s[s.index(a):s.index(b,s.index(a))]
def ordered(t,*xs):
 i=-1
 for x in xs:
  i=t.find(x,i+1)
  if i<0:return False
 return True
def check(label,v):
 assert v,label
 print('PASS',label)
show=section('public void ShowResult()', '/// <summary>')
printed=section('private DataSet BuildReportDataSet()', '#endregion')
check('single-branch selection required and integer-parameterized',all(x in show for x in ['cmbBranches.SelectedIndex < 0','int.TryParse(Convert.ToString(cmbBranches.SelectedValue), out branchFilter)','branchFilter <= 0','condBranch = "inv.branch=@branch and "','Parameters.Add("@branch", SqlDbType.Int).Value = branchFilter']) and 'inv.branch={cmbBranches.SelectedValue}' not in show)
check('specific store and client must be positive', 'storeFilter <= 0' in show and 'clientFilter <= 0' in show)
check('date range is half-open, validated and skipped for all and last',all(x in show for x in ['cbLastProcess.IsChecked != true && ckTotalPeriod.IsChecked != true','startDate < new DateTime(1753, 1, 1)','endDate == DateTime.MaxValue.Date','startDate > endDate','endDate.AddDays(1)','date>=@date1 and date<@date2','if (boundedPeriod)']) and 'date<=@date2' not in show)
check('failure clears partial rows and total',ordered(show,'ActivityList.Add(item);','catch (Exception ex)','ActivityList.Clear();','txtTotStock.Text = string.Empty;'))
check('metadata captured only after loading rows',ordered(show,'adapter.Fill(dt);','ActivityList.Add(item);','txtTotStock.Text = balance','_reportSafe = safeLabel','_reportFrom = fromLabel'))
check('print uses captured metadata not live filter controls',all(x in printed for x in ['SafeMain      = _reportSafe','SafeMainCode  = _reportSafeCode','Clint         = _reportClient','MainItemName  = _reportItemName','MainItemCode  = _reportItemCode','FromDate      = _reportFrom','ToDate        = _reportTo']) and all(x not in printed for x in ['cmbSafes.','cmbClients.','txtDateFrom.','txtDateTo.','txtItemName.','txtItemCode.']))
check('all and last period labels describe query, not controls', '"آخر حركة" : "الكل"' in show and 'fromLabel = startDate.ToShortDateString()' in show)
db=sqlite3.connect(':memory:');db.execute('create table movements(branch int, date text)');db.executemany('insert into movements values (?,?)',[(1,'2024-02-29 00:00:00'),(1,'2024-02-29 23:59:59'),(1,'2024-03-01 00:00:00'),(2,'2024-02-29 12:00:00')]);result=db.execute('select date from movements where branch=? and date>=? and date<? order by date',(1,'2024-02-29','2024-03-01')).fetchall()
check('half-open date and branch model',len(result)==2 and all(x[0].startswith('2024-02-29') for x in result))
# Separate state model, not execution of C# or WPF event handlers.
state={'rows':[1,2],'from':'old'}; state['rows']=[]
try:
 state['rows'].append(3)
 raise ValueError('bad row')
except ValueError:
 state['rows'].clear();state['from']=''
check('partial-result failure model',state=={'rows':[],'from':''})
print('RESULT: PASS — static and independent models only')
