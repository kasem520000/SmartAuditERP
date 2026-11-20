#!/usr/bin/env python3
"""Bounded source contracts and synthetic models; not execution of WPF or SQL Server."""
from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[2]
def read(name): return (root / 'SmartAuditERP/Form_WPF' / name).read_text(encoding='utf-8-sig')
def section(src, start, end): return src[src.index(start):src.index(end, src.index(start))]
def ordered(src, tokens):
    pos = -1
    for token in tokens:
        pos = src.index(token, pos + 1)
    return True

trf = read('frmInventoryTransfer.xaml.cs')
handlers = [('btnInvSrch_Click','btnReceiveQuantity_Click'),('btnReceiveQuantity_Click','BtnInvertoryOrder_Click'),
            ('BtnInvertoryOrder_Click','btnInsertPurch_Click'),('btnInsertPurch_Click','stripImport_Click')]
for current, next_ in handlers:
    h = section(trf, 'private void '+current+'(', 'private void '+next_+'(')
    assert ordered(h, ['frm.ShowDialog();', '!frm.ISDone', 'string.IsNullOrWhiteSpace(frm.InvGlobalID)',
                       'if (_isLoading || CheckBeforeClear()) return;', "frm.InvGlobalID.Replace(\"'\", \"''\")",
                       'if (!TryNavigate(', 'ShowMsg(', 'return;'])
    if current != 'btnInvSrch_Click':
        assert h.index('if (!TryNavigate(') < h.index('_invoic.ProcType =') < h.index('LoadInvoiceNumber();')
    assert '"تعذر تحميل الفاتورة المختارة' in h
nav = section(trf, 'private bool TryNavigate(', 'private void BindingDGV(')
assert ordered(nav, ['BindingInvoice(ref target, sqlStr);','if (target == null) return false;',
                     'string.Equals(target.InvGlobalID, expectedGlobalId, StringComparison.Ordinal)',
                     'if (willClear)', 'CLR();', '_invoic = target;'])
assert 'return false;' in nav[nav.index('catch (Exception ex)'):]
guard = section(trf, 'private bool CheckBeforeClear()', '#region')
assert 'catch\n            {\n                return true;' in guard

# Model the exposed bounds, not the legacy reader, DTO setters, or WPF events.
def picker(accepted, gid, loading, stay, read_id, nav_success, current):
    editor = dict(current)
    if not accepted or not gid or gid.isspace() or gid == '-1': return editor, False
    if loading or stay: return editor, False
    if read_id is None or read_id != gid: return editor, False
    # A failure after publish can change editor, so no rollback is claimed.
    editor = {'gid': read_id, 'proc': 'source'}
    if not nav_success: return editor, False
    editor.update(proc='converted', number='candidate')
    return editor, True
old = {'gid':'A', 'proc':'draft'}
for accepted,gid,loading,stay,read_id in [(False,'B',False,False,'B'), (True,'-1',False,False,'B'),
      (True,' ',False,False,'B'), (True,'B',True,False,'B'), (True,'B',False,True,'B'),
      (True,'B',False,False,None), (True,'B',False,False,'C')]:
    assert picker(accepted,gid,loading,stay,read_id,True,old)==(old,False)
assert picker(True,'B',False,False,'B',True,old)[1]
assert picker(True,'B',False,False,'B',False,old)==({'gid':'B','proc':'source'},False)

bal = read('frmItemsBalances.xaml.cs')
fill = section(bal, 'private void FillBalanceData(', 'private void MergeRows(')
assert 'catch' not in fill and 'adapter.Fill(result);' in fill
assert 'row[0] == DBNull.Value || row[1] == DBNull.Value' in fill
assert 'double.IsNaN(val) || double.IsInfinity(val)' in fill
calc = section(bal, 'public void CalcStock(', 'private void FillBalanceData(')
assert ordered(calc, ['_balanceRows.Clear();', 'FillTransferData(', 'MergeRows(balanceTable);',
                      'stagedRows', 'GetCurrencyName(itemId)', 'foreach (BalanceRow row in stagedRows)',
                      '_balanceRows.Add(row);'])
assert '_balanceRows.Clear();' in calc[calc.index('catch (Exception ex)'):]
names = section(bal, 'private string GetCurrencyName(', '#endregion')
assert 'id=@itemId' in names and 'throw new InvalidOperationException' in names and 'catch' not in names
# Deliberately malformed legacy query in a synthetic schema: no final result is published.
c = sqlite3.connect(':memory:')
c.executescript('create table Items(id integer, name text); create table SafesTransfer(id integer); create table SafesTransfer_Sub(transfer_id integer, ItemId integer, ReceivedValue integer);')
published = ['old']
try:
    published.clear()
    c.execute('select currency,sum(ReceivedValue) from SafesTransfer,SafesTransfer_Sub where SafesTransfer.id=SafesTransfer_Sub.transfer_id group by currency').fetchall()
    published.append('invalid partial result')
except sqlite3.OperationalError:
    published.clear()
assert published == []

stubs=[('frmCloseShift.xaml.cs','private void ExportToExcel()','#endregion'),
       ('frmEmpInvs.xaml.cs','private void BtnExport_Click(', '#endregion'),
       ('frmInvPurch.xaml.cs','private void stripExport_Click(', 'private bool IsInvExist()'),
       ('frmAccountBalance.xaml.cs','private void btnExportExcel_Click(', '#endregion'),
       ('frmAccountsDirectory.xaml.cs','private void btnExportExcel_Click(', '#endregion')]
for name,start,end in stubs:
    handler=section(read(name),start,end)
    assert 'لم يُنشأ أي ملف' in handler
    assert all(x not in handler for x in ['SaveFileDialog','Process.Start','ShowSuccess(', 'تم التصدير بنجاح', 'تم حفظ الملف'])
print('PASS: transfer picker gates, balance failure publication, five export warnings')

acts = read('frmActsInvTotal.xaml.cs')
query = section(acts, 'private double CalculateActTotal(', '#endregion')
for x in ['isPurchase ? 1 : 2', 'isPurchase ? 2 : 1', 'inv.inv_type = 1', 'inv.inv_type IN (2,3)',
          'inv.proc_type = @procType', 'inv_sub.proc_type = @subProcType',
          'Value = normalDirection', 'Value = returnDirection', 'inv.date < @dateTo',
          'Value = 1;', 'Value = 2;', 'throw;', 'finally']:
    assert x in query, x
assert 'return 0;' not in query
calc = section(acts, 'private void CalculateReport()', 'private double CalculateActTotal(')
assert ordered(calc, ['DateTime dateFrom', 'SelectedDate.Value.Date.AddDays(1)',
                      'stagedRows', 'CalculateActTotal(', 'stagedRows.Add(',
                      'foreach (ActTotalItem row in stagedRows) _reportData.Add(row)'])
assert '_reportData.Clear();' in calc[calc.index('catch (Exception ex)'):]
# Independent fixture of the documented header kind × operation × line direction.
c = sqlite3.connect(':memory:')
c.execute('create table movement(kind int, op int, direction int, amount real, day text, deleted int)')
c.executemany('insert into movement values(?,?,?,?,?,?)',[
 (1,1,1,100,'2026-11-19 10:00:00',0),(1,2,2,20,'2026-11-19 11:00:00',0),
 (2,1,2,60,'2026-11-19 12:00:00',0),(2,2,1,10,'2026-11-19 13:00:00',0),
 (3,1,2,200,'2026-11-19 14:00:00',0),(3,2,1,20,'2026-11-19 15:00:00',0),
 (4,1,1,7,'2026-11-19 16:00:00',0),(1,1,1,500,'2026-11-20 00:00:00',0),
 (2,1,2,90,'2026-11-19 16:00:00',1),(2,1,1,999,'2026-11-19 16:00:00',0)])
def total(kinds, normal, returned):
    def run(op, direction):
        return c.execute('select coalesce(sum(amount),0) from movement where kind in ('+','.join('?'*len(kinds))+') and op=? and direction=? and day>=? and day<? and deleted=0',(*kinds,op,direction,'2026-11-19','2026-11-20')).fetchone()[0]
    return run(1,normal)-run(2,returned)
assert total((1,),1,2)==80
assert total((2,3),2,1)==230
print('PASS: bounded commercial type and direction fixture; SQL Server and accounting policy remain unverified')
