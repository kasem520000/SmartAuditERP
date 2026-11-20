#!/usr/bin/env python3
"""Source contracts plus a SQLite selection model, not ERP/SQL Server execution."""
from pathlib import Path
import sqlite3

root = Path(__file__).resolve().parents[2]
def read(p): return (root / p).read_text(encoding='utf-8-sig')
def part(s, a, b): return s[s.index(a):s.index(b, s.index(a))]
item = read('SmartAuditERP/Class/ItemOper.cs')
contract = read('SmartAuditERP/Class/ItemOpercontract.cs')
attend = read('SmartAuditERP/Form_WPF/frmAttendM.xaml.cs')
hold = read('SmartAuditERP/Form_WPF/frmHoldM.xaml.cs')
method = part(item, 'public static void LoadCustomerPrice(', '#endregion')
assert 'p.ItemID=@item AND p.UnitID=@unit AND p.IS_Deleted=0' in method
assert 'SELECT TOP (2)' in method and 'prices.Rows.Count != 1' in method
assert 'newItem.UnitID <= 0' in method
assert 'pricing == 3 || pricing == 4' in method
assert 'RecentPurchPrice(' not in method and 'Cost(' not in method
assert 'newItem.ItemPrice = unitPrice' in method and 'ShowAttentionMsg(' in method
assert method.index('pricing == 3 || pricing == 4') < method.index('SELECT TOP (2)')
for i in (1, 2, 5, 6, 7): assert f'case {i}:' in method
contract_price = part(contract, 'public static void LoadCustomerPrice(', 'public static void LoadItemDetails(')
assert 'ItemOper.LoadCustomerPrice(ref NewItem, CustomerId)' in contract_price
for s in (item, contract):
    assert s.index('LoadUnitInf(ref', s.index('public static void LoadItemInf')) < s.index('LoadCustomerPrice(ref', s.index('public static void LoadItemInf'))
exit_method = part(attend, 'private void MarineExit(', 'private void MarineAttend(')
assert 'MessageBox.Show' in exit_method and 'SqlCommand' not in exit_method and 'attendRows.Remove' not in exit_method
link = part(hold, 'public void SaveInvoiceLink()', '#endregion')
assert 'DXMessageBox.Show' in link and 'SqlCommand' not in link and 'BeginTransaction' not in link
save = part(hold, 'private void btnSave_Click(', 'private void btnDelete_Click(')
assert 'SaveInvoiceLink();' in save and 'تم ربط الفاتورة بنجاح' not in save and 'ClearFields()' not in save
assert 'RecordMarineExit(' not in hold

c = sqlite3.connect(':memory:')
c.execute('create table prices(item int, unit int, deleted int, sale real)')
c.executemany('insert into prices values(?,?,?,?)', [(1,1,0,12),(1,2,0,35),(1,2,1,40),(2,1,0,21),(3,1,0,1),(3,1,0,2)])
def pick(item_id, unit, pricing, current=99):
    if pricing not in range(1,8): return current, False
    if pricing in (3,4): return current, True
    rows = c.execute('select sale from prices where item=? and unit=? and deleted=0 limit 2', (item_id,unit)).fetchall()
    return (rows[0][0], False) if unit > 0 and len(rows) == 1 else (current, True)
assert pick(1,1,1)==(12,False)
assert pick(1,2,1)==(35,False)
assert pick(1,3,1)==(99,True)
assert pick(1,0,1)==(99,True)
assert pick(3,1,1)==(99,True)
assert pick(1,1,3)==(99,True) and pick(1,2,4)==(99,True)
assert pick(1,1,-1)==(99,False)
assert pick(2,1,1)==(21,False)
print('PASS: unit-aware selection model and marine guard source contracts')
