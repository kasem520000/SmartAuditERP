#!/usr/bin/env python3
"""R-250: source witnesses and fault models only; not .NET, SQL Server or WPF."""
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory

root=Path(__file__).resolve().parents[2]/'SmartAuditERP'
receipt=(root/'Class/ReceiptOper.cs').read_text(encoding='utf-8-sig')
entry=(root/'Class/EntryOper.cs').read_text(encoding='utf-8-sig')
body=receipt.split('private bool SaveReceiptLocked(')[1].split('private static void InsertReceiptDocuments(')[0]
attach=receipt.split('private static void InsertReceiptDocuments(')[1].split('public bool SaveReceipt2(')[0]
writer=entry.split('internal void WriteEntryInTransaction(')[1].split('public bool SaveEnty(')[0]
def ordered(s,*parts):
 pos=-1
 for p in parts: pos=s.index(p,pos+1)
 return True
assert ordered(body,'Entr == null','connection.Open()', 'BeginTransaction()', 'WITH (UPDLOCK, HOLDLOCK)',
               'sqlCommand3.ExecuteNonQuery()', 'WriteEntryInTransaction(Entr, connection, transaction, IsNew)',
               'InsertReceiptDocuments(documents, Receipt.GlobalID, connection, transaction, copiedFiles)',
               'commitStarted = true', 'transaction.Commit()', 'return true')
assert 'Receipt.EntryGlobalID, Entr.EntryGlobalID' in body
assert 'Receipt.BranchID.Value != Entr.Branch' in body and 'IsNew == exists' in body
assert 'EntryGlobalID=@entry AND GlobalID<>@receipt' in body
assert 'transaction.Rollback()' in body and 'commitStarted || !rollbackConfirmed' in body
assert ordered(body,'if (unknown)', 'receiptSaveNeedsReview = true;', 'else', 'foreach (string path in copiedFiles)')
assert 'Receipt.GlobalID + "، معرّف القيد: " + Receipt.EntryGlobalID' in body
assert 'lock (ReceiptSaveGate)' in receipt and 'if (receiptSaveNeedsReview)' in receipt
assert 'ValidateEntryBeforeSave(entry' in writer and 'expectedNew.Value != isNew' in writer
assert 'conn, transaction' in writer and 'conn.BeginTransaction()' not in writer
assert 'FileMode.CreateNew' in attach and 'Guid.NewGuid()' in attach and 'copiedFiles.Add(destination)' in attach
assert 'connection, transaction' in attach and 'MAX(id)' not in attach and 'overwrite' not in attach
for f in ('frmSandSD','frmSandQD','frmSandD','frmSandQAndroid'):
 s=(root/'Form_WPF'/f'{f}.xaml.cs').read_text(encoding='utf-8-sig')
 assert 'private string[] _receiptFiles;' in s and '.SaveReceipt(receipt, entry, isNew, _receiptFiles)' in s
 assert 'ReceiptOper.filePathDocument =' not in s
 save=s[s.index('.SaveReceipt(receipt, entry, isNew, _receiptFiles)'):]
 assert ordered(save, 'if (!saved)' if f in ('frmSandSD','frmSandQD') else 'if (isNew)', 'Code = receipt.ReceiptNo;', '_receiptFiles = null;')
 assert 'if (isNew) { Code = -1; GlobalID = "-1"; EntryGlobalID = "-1"; }' in save

# Independent fault injection of intended transaction and cleanup policy using SQLite.
# This models neither SQL Server locking, actual C# execution, nor filesystem durability.
def run(stage, update=False):
 db=sqlite3.connect(':memory:')
 db.executescript('create table receipts(id text primary key, val int); create table journal(id text primary key, val int); create table docs(id text);')
 if update:
  db.execute("insert into receipts values ('r',1)");db.execute("insert into journal values ('e',1)");db.commit()
 with TemporaryDirectory() as d:
  copied=Path(d)/'new'; outcome='failure'; unknown=False
  try:
   db.execute('begin')
   db.execute("insert or replace into receipts values ('r',2)")
   if stage=='receipt': raise ValueError()
   db.execute("insert or replace into journal values ('e',2)")
   if stage=='journal': raise ValueError()
   copied.write_text('file')
   if stage=='file': raise ValueError()
   db.execute("insert into docs values ('r')")
   if stage=='metadata': raise ValueError()
   db.commit()
   if stage=='unknown_commit': unknown=True;raise ValueError()
   outcome='success'
  except ValueError:
   if not unknown:
    db.rollback()
    copied.unlink(missing_ok=True)
  rows=(db.execute('select * from receipts').fetchall(),db.execute('select * from journal').fetchall(),db.execute('select * from docs').fetchall())
  return outcome,unknown,rows,copied.exists()
for update in (False,True):
 for stage in ('receipt','journal','file','metadata'):
  out,unknown,rows,exists=run(stage,update)
  assert out=='failure' and not unknown and not exists
  assert rows==(([('r',1)],[('e',1)],[]) if update else ([],[],[]))
 out,unknown,rows,exists=run('success',update)
 assert (out,unknown,rows,exists)==('success',False,([('r',2)],[('e',2)],[('r',)]),True)
 out,unknown,rows,exists=run('unknown_commit',update)
 assert out=='failure' and unknown and exists and rows==([('r',2)],[('e',2)],[('r',)])
# Name-based mappings in these seven save-time lookups are parameterized and
# ambiguous rows are refused. Other lookups, branch authorization and the
# authoritative account mapping remain out of scope.
lookups={'frmSandSD': [('daCustAcc','dtCustAcc'),('daStock','dtStock')],
 'frmSandQD':[('daStock','dtStock')], 'frmSandD':[('accAdapter1','dt1'),('accAdapter2','dt2')],
 'frmSandQAndroid':[('acc1','dt1'),('acc2','dt2')]}
for name, pairs in lookups.items():
 s=(root/'Form_WPF'/f'{name}.xaml.cs').read_text(encoding='utf-8-sig')
 for adapter,table in pairs:
  section=s[s.index('var '+adapter+' = new SqlDataAdapter('):]
  section=section[:section.index('تعذر تحديد حساب وحيد')]
  assert 'AName=@accountName' in section
  assert adapter+'.SelectCommand.Parameters.Add("@accountName", SqlDbType.NVarChar)' in section
  assert 'if ('+table+'.Rows.Count == 1)' in section and 'else' in section

assert 'type=@type AND IS_Deleted=0' in writer
assert 'reader["ReceiptType"] == DBNull.Value' in body and 'Convert.ToInt32(reader["ReceiptNo"]) != Receipt.ReceiptNo' in body
# SQLite demonstrates the intended literal-name and ambiguity rule only.
db=sqlite3.connect(':memory:')
db.execute('create table accounts(name text, code int)')
db.executemany('insert into accounts values (?,?)', [("O'Brien",1),('same',2),('same',3)])
def resolve(name):
 rows=db.execute('select code from accounts where name=?',(name,)).fetchall()
 return rows[0][0] if len(rows)==1 else None
assert resolve("O'Brien")==1 and resolve("x' OR 1=1 --") is None and resolve('same') is None
print('PASS: receipt atomicity and lookup witnesses with synthetic models')
