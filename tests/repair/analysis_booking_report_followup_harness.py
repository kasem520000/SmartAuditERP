#!/usr/bin/env python3
"""Source contracts and synthetic models; no WPF, C# execution or SQL Server."""
from pathlib import Path
import math
import sqlite3

R = Path(__file__).resolve().parents[2] / 'SmartAuditERP/Form_WPF'
def read(name): return (R / (name + '.xaml.cs')).read_text(encoding='utf-8-sig')
def part(s, start, end): return s[s.index(start):s.index(end, s.index(start))]
def ordered(s, *tokens):
    i = -1
    for token in tokens: i = s.index(token, i + 1)
    return True

analysis = read('frmRptInvAnalysis')
assert 'if (!_analysisRunning) return;' in analysis and 'e.Cancel = true;' in analysis
validate = part(analysis, 'private bool ValidateAnalysisSelection()', 'private void btnShow_Click(')
assert all(t in validate for t in ('!txtDateFrom.SelectedDate.HasValue', '!txtDateTo.SelectedDate.HasValue', 'DateTime.MaxValue.Date', '> txtDateTo.SelectedDate.Value.Date'))
launch = part(analysis, 'private void btnShow_Click(', 'private void ShowResult()')
assert all(t in launch for t in ('chkAllStock, cmbStock', 'chkAllSafe, cmbSafe', 'chkAllCust, cmbCust', 'chkAllEmp, cmbEmp', 'chkAllSales, cmbSales', 'txtDateFrom, txtDateTo'))
assert 'InvalidateAnalysisResult();' in launch and 'catch (Exception ex)' in launch
for t in ('combo.SelectionChanged += AnalysisFilter_SelectionChanged',
          'check.Checked += AnalysisFilter_CheckedChanged', 'check.Unchecked += AnalysisFilter_CheckedChanged',
          'check.Indeterminate += AnalysisFilter_CheckedChanged',
          'txtDateFrom.SelectedDateChanged += AnalysisFilter_SelectionChanged',
          'txtDateTo.SelectedDateChanged += AnalysisFilter_SelectionChanged'):
    assert t in analysis
for mode in ('Group','Item','Cust','Salesman','Emp','Month','Day','Stock'):
    body = part(analysis, 'private void ShowResult'+mode+'()', '#endregion')
    assert 'date>=@date1 and date<=@date2' not in body
    assert 'date>=@date1 and date<@date2' in body
    assert 'catch\n            {' in body and 'throw;' in body
    assert 'dateFrom.ToShortDateString()' not in body
assert 'date <=@date2' in part(analysis,'private double CalcUnitCost(', 'private void AddRowToGrid(')

book=read('frmBookingM')
save=part(book,'private void Save()', '#region Navigation')
assert ordered(save, 'if (_bookingNeedsReview)', 'txtDate.EditValue is DateTime', 'int.TryParse(hour.Text',
               'minuteVal >= 60', 'item.Quantity != Math.Truncate(item.Quantity)',
               'conn.BeginTransaction()', 'commitStarted = true;', 'transaction.Commit();',
               'committed = true;', 'transaction.Dispose();', 'transaction = null;')
assert 'catch { rollbackFailed = true; }' in save
assert ordered(save, 'TryFiniteBookingAmount(txtPrice.Text', 'conn.BeginTransaction()')
assert 'double.IsNaN(value)' in book and 'double.IsInfinity(value)' in book
assert 'cleanupError != null' in save and 'conn1.Close()' in save
assert 'if (commitStarted || committed || rollbackFailed)' in save
assert '_bookingNeedsReview = true;' in save and 'ProcID = previousProcId;' in save
assert '_bookingNeedsReview = false' not in book
# This is a window-local guard, not idempotence or actual DB execution.
def simulate(before_commit_error=False, commit_error=False, rollback_error=False, ui_error=False):
    commit_started = False
    committed = False
    if before_commit_error: return rollback_error, not rollback_error
    commit_started = True
    if commit_error: return commit_started or rollback_error, False
    committed = True
    if ui_error: return committed, False
    return False, True
assert simulate(before_commit_error=True)==(False,True)
assert simulate(before_commit_error=True,rollback_error=True)==(True,False)
assert simulate(commit_error=True)==(True,False)
assert simulate(ui_error=True)==(True,False)
assert simulate()==(False,True)
for h,m,expected in [(0,30,True),(1,0,True),(0,0,False),(-1,10,False),(1,60,False),(1,-1,False)]:
    assert (h>=0 and 0<=m<60 and (h!=0 or m!=0)) == expected
for qty,expected in [(1,True),(3,True),(1.5,False),(0,False),(-1,False),(float('nan'),False),(float('inf'),False)]:
    valid=math.isfinite(qty) and 0<qty<=2**31-1 and qty==math.trunc(qty)
    assert valid == expected

act=read('frmNkdTotSalePurchActCust')
assert 'if (!_calculating) return;' in act and 'e.Cancel = true;' in act
show=part(act,'private void btnShow_Click(', 'private void CalcStock(')
assert ordered(show,'if (_calculating) return;', 'InvalidateResult();', 'DateTime from', 'DateTime toExclusive',
               'int version = _criteriaVersion;', 'controls[i].IsEnabled = false;', '_calculating = true;', 'new Thread(')
assert 'if (version != _criteriaVersion) return;' in show and 'ShowError(ex)' in show
calc=part(act,'private void CalcStock(', 'private void ExecuteItemQuery(')
for t in ('inv.inv_type=1 and inv.proc_type=1 and inv_sub.proc_type=1',
          'inv.inv_type=1 and inv.proc_type=2 and inv_sub.proc_type=2',
          'inv.inv_type IN (2,3) and inv.proc_type=1 and inv_sub.proc_type=2',
          'inv.inv_type IN (2,3) and inv.proc_type=2 and inv_sub.proc_type=1',
          'date>=@date1 and date<@date2', 'netPTotal != 0.0 || netSTotal != 0.0',
          'stagedRows.Add(', 'if (version != _criteriaVersion) return;'):
    assert t in calc, t
assert calc.count('sum(val1*exchange_price)')==4
query=part(act,'private void ExecuteItemQuery(', '#endregion')
assert 'catch' not in query and 'DateTime date1, DateTime date2' in query and 'throw new InvalidOperationException' in query

# Independent fixture: line direction, returns, noncommercial and exclusive day end.
c=sqlite3.connect(':memory:')
c.execute('create table m(kind int, op int, direction int, qty real, amount real, date text, deleted int)')
c.executemany('insert into m values(?,?,?,?,?,?,?)',[
 (1,1,1,1,100,'2026-11-19 12:00',0),(1,2,2,1,80,'2026-11-19 13:00',0),
 (2,1,2,2,60,'2026-11-19 14:00',0),(2,2,1,1,10,'2026-11-19 15:00',0),
 (3,1,2,1,200,'2026-11-19 16:00',0),(3,2,1,1,20,'2026-11-19 17:00',0),
 (4,1,1,1,7,'2026-11-19 18:00',0),(1,1,1,1,999,'2026-11-20 00:00',0),
 (1,1,1,1,999,'2026-11-19 18:00',1)])
def aggregate(types,op,direction):
    return c.execute('select coalesce(sum(qty),0),coalesce(sum(amount),0) from m where kind in ('+','.join('?'*len(types))+') and op=? and direction=? and date>=? and date<? and deleted=0',(*types,op,direction,'2026-11-19','2026-11-20')).fetchone()
def net(types,nd,rd):
    a=aggregate(types,1,nd);b=aggregate(types,2,rd);return tuple(x-y for x,y in zip(a,b))
assert net((1,),1,2)==(0,20)
assert net((2,3),2,1)==(1,230)
assert any(net((1,),1,2)) # zero quantity but nonzero amount remains visible
assert not ('2026-11-20 00:00' < '2026-11-20')
print('PASS: report filter lifecycle, date boundaries, booking safeguards, and bounded commercial fixture')
