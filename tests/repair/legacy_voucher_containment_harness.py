#!/usr/bin/env python3
"""Legacy receipt containment / two balance views: source witnesses and SQLite models.
Does not execute CLR, WPF, SQL Server locks, or ERP posting/accounting policy.
"""
from pathlib import Path
import sqlite3
ROOT=Path(__file__).resolve().parents[2]/'SmartAuditERP'
receipt=(ROOT/'Class/ReceiptOper.cs').read_text(encoding='utf-8-sig')
def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def ordered(s,*parts):
 p=-1
 for part in parts:p=s.index(part,p+1)
 return True
queue=section(receipt,'public static bool LegacyReceiptRowsClear(', 'public Entry BindReceiptToEntry(')
for name in ('SandQ','SandVAT','SandSD','SandQD','SandD'):
 assert f'case "{name}":' in queue
 assert f'FROM dbo.{name} WHERE branch=@branch OR branch IS NULL' in queue
assert 'default:' in queue and 'branch <= 0' in queue and 'catch (Exception ex)' in queue
assert 'command.Parameters.Add("@branch", SqlDbType.Int)' in queue
assert 'Convert.ToInt64(result) != 0' in queue and 'return false;' in queue
save_locked=section(receipt,'private bool SaveReceiptLocked(', 'private static void InsertReceiptDocuments(')
assert 'Receipt.BranchID.Value != MainClass.BranchNo' in save_locked
assert not any(word in queue.upper() for word in ('DELETE FROM','UPDATE ','INSERT INTO'))
forms={'frmSandQ':'SandQ','frmSandVAT':'SandVAT','frmSandSD':'SandSD',
       'frmSandQD':'SandQD','frmSandD':'SandD','frmSandQAndroid':'SandQ'}
for form,table in forms.items():
 s=(ROOT/'Form_WPF'/f'{form}.xaml.cs').read_text(encoding='utf-8-sig')
 restore=section(s,'private void RestorePreviousReceipt()', '\n        #endregion')
 assert f'LegacyReceiptRowsClear("{table}", MainClass.BranchNo)' in restore
 assert not any(word in restore.upper() for word in ('DELETE FROM','UPDATE ','INSERT INTO','SAVERECEIPT2('))
 delete=section(s,'private void btnDelete_Click(', '\n        private void ')
 if form in ('frmSandQ','frmSandVAT'):
  guard=section(s,'private bool VoucherMutationAvailable()', 'private async void btnSave_Click(')
  assert 'return false;' in guard
  save=section(s,'private async void btnSave_Click(', '\n        private void btnDelete_Click(')
  assert ordered(save,'if (!VoucherMutationAvailable()) return;', 'new SqlCommand(upsertSql')
  assert ordered(delete,'if (!VoucherMutationAvailable()) return;', 'UPDATE Receipts SET ISDeleted=1')
 else:
  save=section(s,'private async void btnSave_Click(', 'private async Task SaveReceiptCore(')
  assert f'if (!ReceiptOper.LegacyReceiptRowsClear("{table}", MainClass.BranchNo)) return;' in save
  assert f'if (!ReceiptOper.LegacyReceiptRowsClear("{table}", MainClass.BranchNo)) return;' in delete


legacy=(ROOT/'Form_WPF/frmVATvoucher.xaml.cs').read_text(encoding='utf-8-sig')
legacy_guard=section(legacy,'private bool LegacyVoucherMutationAvailable()', 'private void btnSave_Click(')
assert 'return false;' in legacy_guard
legacy_save=section(legacy,'private void btnSave_Click(', 'private void InsertEntrySub(')
legacy_delete=section(legacy,'private void btnDelete_Click(', '\n        #endregion')
assert ordered(legacy_save,'if (!LegacyVoucherMutationAvailable()) return;', 'conn.BeginTransaction()', 'DELETE FROM Entry WHERE id=')
assert ordered(legacy_delete,'if (!LegacyVoucherMutationAvailable()) return;', 'UPDATE SandVAT SET IS_Deleted=1', 'UPDATE Entry SET state=2')

for form in ('frmSandQ','frmSandQD'):
 s=(ROOT/'Form_WPF'/f'{form}.xaml.cs').read_text(encoding='utf-8-sig')
 bal=section(s,'private void GetCustBalance()', '\n        #endregion')
 assert bal.count('txtBalance.Text = string.Empty;') >= 2
 assert bal.count('txtBalanceType.Text = string.Empty;') >= 2
 assert 'Entry.date<@endExclusive' in bal and '.Date.AddDays(1)' in bal
 assert 'COUNT_BIG(Entry_sub.dept)' in bal and 'COUNT_BIG(Entry_sub.credit)' in bal
 assert '!= count' in bal and 'double.IsFinite(dept - credit)' in bal
 assert 'Entry_sub.acc_no=@account' in bal and 'SqlDbType.Int).Value = accCode' in bal
 if form=='frmSandQ':
  assert 'AName=@name' in bal and 'Parameters.Add("@name", SqlDbType.NVarChar)' in bal and 'codeDt.Rows.Count != 1' in bal

# Model conservative queue checks: other branches do not block; NULL does.
db=sqlite3.connect(':memory:');db.execute('create table legacy(branch int, deleted int)')
def clear(branch):
 if branch<=0:return False
 try:return db.execute('select count(*) from legacy where branch=? or branch is null',(branch,)).fetchone()[0]==0
 except sqlite3.Error:return False
assert clear(1) and not clear(-1)
db.executemany('insert into legacy values (?,?)',[(2,0),(3,1)]);assert clear(1) and not clear(2)
db.execute('insert into legacy values (?,?)',(None,1));assert not clear(1)
rows=db.execute('select * from legacy order by branch').fetchall();assert len(rows)==3
db.execute('drop table legacy');assert not clear(1)
# Model literal name matching, uniqueness, a half-open day, and NULL detection.
db=sqlite3.connect(':memory:');db.executescript('create table accounts(name text,code int);create table lines(date text,debt real,credit real);')
db.executemany('insert into accounts values (?,?)',[("O'Brien",1),('twice',2),('twice',3)])
def account(name):
 rows=db.execute('select code from accounts where name=?',(name,)).fetchall()
 return rows[0][0] if len(rows)==1 else None
assert account("O'Brien")==1 and account("x' OR 1=1 --") is None and account('twice') is None
db.executemany('insert into lines values (?,?,?)', [('2026-01-01 23:59:59.999',10,0),('2026-01-02 00:00:00',999,0)])
def totals():
 count,dc,cc,d,c=db.execute("select count(*),count(debt),count(credit),sum(debt),sum(credit) from lines where date<?",('2026-01-02',)).fetchone()
 return None if count!=dc or count!=cc else (d or 0,c or 0)
assert totals()==(10,0)
db.execute('insert into lines values (?,?,?)',('2026-01-01 12:00:00',None,0));assert totals() is None
print('PASS: legacy row preservation, gated voucher writes and balance safeguards (synthetic models)')
