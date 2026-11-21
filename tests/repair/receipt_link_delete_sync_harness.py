#!/usr/bin/env python3
"""R-257..259: static witnesses and isolated SQLite models, not CLR/SQL Server/WPF."""
from pathlib import Path
import sqlite3
root=Path(__file__).resolve().parents[2]/'SmartAuditERP'
r=(root/'Class/ReceiptOper.cs').read_text(encoding='utf-8-sig')
e=(root/'Class/EntryOper.cs').read_text(encoding='utf-8-sig')
def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def ordered(s,*needles):
 pos=-1
 for v in needles:pos=s.index(v,pos+1)
 return True
save=section(r,'private bool SaveReceiptLocked(', 'private static void InsertReceiptDocuments(')
assert 'journalReference != Receipt.ReceiptNo' in save and 'Receipt.ReceiptDate.Value != Entr.EntryDate' in save
assert 'ReceiptNo=@number AND ReceiptType=@type AND BranchID=@branch AND GlobalID<>@id' in save
assert 'if (exists && reader.Read())' in save and 'if (sqlCommand3.ExecuteNonQuery() != 1)' in save
writer=section(e,'internal void WriteEntryInTransaction(', 'public bool SaveEnty(')
for witness in ('entryCount > 1','state=1 AND id=@number AND doc_no=@reference','account.EntryNo != entry.EntryNo','cmd.ExecuteNonQuery() != 1'):
 assert witness in writer
public=section(r,'public bool DeleteReceipt(', 'private bool DeleteReceiptLocked(')
assert 'lock (ReceiptSaveGate)' in public and 'receiptSaveNeedsReview' in public
body=section(r,'private bool DeleteReceiptLocked(', '// The two editors build their journal')
assert ordered(body,'connection.BeginTransaction()', 'FROM Receipts WITH (UPDLOCK, HOLDLOCK)', 'EntryGlobalID=@entry AND GlobalID<>@receipt', 'FROM Entry WITH (UPDLOCK, HOLDLOCK)', 'UPDATE Receipts SET ISDeleted=1', 'update.ExecuteNonQuery() != 1', 'UPDATE Entry SET state=2', 'update.ExecuteNonQuery() != 1','commitStarted = true','transaction.Commit()')
for witness in ('string.Equals(reader.GetString(0), entryId, StringComparison.Ordinal)', 'Convert.ToInt32(reader["BranchID"]) != branch', 'Convert.ToInt32(reader["type"]) != type', 'Convert.ToInt32(reader["doc_no"]) != number', 'Convert.ToInt32(reader["state"]) != 1', 'commitStarted || !rollbackConfirmed', 'receiptSaveNeedsReview = true'):
 assert witness in body
sync=section(r,'public async Task SyncReceipt(', 'public void ReadReceiptOnline(')
assert ordered(sync,'string receiptId = receipt.GlobalID, entryId = Eny.EntryGlobalID;', 'await receiptCRUD.PostReceiptsOnline', 'await entryCRUD.PostEntriesOnline', 'list.Count > 1', 'UPDATE Receipts SET Sync=1 WHERE GlobalID=@id', 'UPDATE Entry SET Sync=1 WHERE GlobalID=@id')
assert 'list[0].GlobalID, receiptId' in sync and 'list2[0].EntryGlobalID, entryId' in sync
for form in ('frmSandSD','frmSandQD','frmSandD','frmSandQAndroid'):
 s=(root/'Form_WPF'/f'{form}.xaml.cs').read_text(encoding='utf-8-sig')
 wrapper=section(s,'private async void btnSave_Click(', 'private async Task SaveReceiptCore(')
 assert 'if (_receiptSaveInProgress) return;' in wrapper and 'finally { _receiptSaveInProgress = false; }' in wrapper
 main=section(s,'private async Task SaveReceiptCore(', 'private void btnDelete_Click(')
 assert ordered(main,'SaveReceipt(receipt, entry, isNew, _receiptFiles)', 'committed = true;', 'Code = receipt.ReceiptNo;', '_receiptFiles = null;', 'await ')
 assert 'تم حفظ السند محلياً' in main and 'Code = Convert.ToInt32(txtNo.Text)' not in main
 assert 'if (_receiptSaveInProgress) return;' in section(s,'private void btnDelete_Click(', '\n        private void ')

# Independent model of the contract: not SQL Server lock/race behaviour.
def db_new():
 d=sqlite3.connect(':memory:')
 d.executescript('create table receipts(gid text,entry text,branch int,num int,type int,deleted int); create table journal(gid text,branch int,num int,type int,deleted int,state int);')
 d.execute('insert into receipts values (?,?,?,?,?,?)',('r',"e'1",1,7,5,0));d.execute('insert into journal values (?,?,?,?,?,?)',("e'1",1,7,5,0,1));d.commit();return d
def delete(d,rid,eid,branch=1,fail=False):
 try:
  d.execute('begin')
  rows=d.execute('select entry,branch,deleted,num,type from receipts where gid=?',(rid,)).fetchall()
  if len(rows)!=1:raise ValueError()
  link,br,deleted,num,typ=rows[0]
  if (link,br,deleted)!=(eid,branch,0):raise ValueError()
  if d.execute('select count(*) from receipts where entry=? and gid<>?',(eid,rid)).fetchone()[0]:raise ValueError()
  rows=d.execute('select branch,num,type,deleted,state from journal where gid=?',(eid,)).fetchall()
  if rows!=[(branch,num,typ,0,1)]:raise ValueError()
  assert d.execute('update receipts set deleted=1 where gid=?',(rid,)).rowcount==1
  if fail:raise ValueError()
  assert d.execute('update journal set deleted=1,state=2 where gid=?',(eid,)).rowcount==1
  d.commit();return True
 except ValueError:d.rollback();return False
for rid,eid,branch,fail in [('r',"e'1",1,True),('r','wrong',1,False),('r',"e'1",2,False),("r' OR 1=1 --", "e'1",1,False)]:
 d=db_new();assert not delete(d,rid,eid,branch,fail);assert d.execute('select deleted from receipts').fetchone()==(0,);assert d.execute('select deleted,state from journal').fetchone()==(0,1)
d=db_new();d.execute('insert into receipts values (?,?,?,?,?,?)',('other',"e'1",1,8,5,0));d.commit();assert not delete(d,'r',"e'1")
d=db_new();assert delete(d,'r',"e'1") and not delete(d,'r',"e'1");assert d.execute('select deleted,state from journal').fetchone()==(1,2)
# Only exact, unique responses may acknowledge the originally sent identity.
def ack_ok(responses,identity):return len(responses)<=1 and (not responses or responses[0]==identity)
assert ack_ok([], 'r') and ack_ok(['r'],'r') and not ack_ok(['other'],'r') and not ack_ok(['r','r'],'r')
print('PASS: receipt identity, atomic deletion, acknowledgement and UI witnesses/models')
