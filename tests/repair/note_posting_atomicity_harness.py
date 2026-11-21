#!/usr/bin/env python3
"""R-255 independent models and source contracts; not CLR, SQL Server or WPF."""
from pathlib import Path
import sqlite3
root=Path(__file__).resolve().parents[2]/'SmartAuditERP'
def load(f):return (root/f).read_text(encoding='utf-8-sig')
def part(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
def order(s,*xs):
 p=-1
 for x in xs:p=s.index(x,p+1)
 return True
r=load('Class/ReceiptOper.cs')
writer=part(r,'private bool SaveCreditDebtNoteLocked(', 'private static readonly object NoteDeleteGate')
for x in ('d.Branch != MainClass.BranchNo','d.Number <= 0','double.IsFinite(d.Discount)',
          'reference != d.Number','d.Journal.EntryDate != d.Date','d.Journal.State != 1','d.Journal.ISDeleted != false','UPDLOCK,HOLDLOCK',
          'd.IsNew && exists','reader.IsDBNull(1)','reader.IsDBNull(2)',
          'reader.Read()) throw','d.Journal.EntryNo = existingEntryNo','account.EntryNo = existingEntryNo',
          'SELECT AccountCode FROM Customers WITH (UPDLOCK,HOLDLOCK)','Convert.ToInt32(stored) != partyCode','firstAccount.Debt != d.Discount','firstAccount.Credit != d.Discount',
          'debit != noteAmount || credit != noteAmount','BranchId) VALUES',
          'WHERE Id=@id AND BranchId=@branch AND Doc_No=@number AND Doc_Type=@type AND IS_Deleted=0',
          'cmd.ExecuteNonQuery() != 1','transaction.Rollback()','commitStarted || !rollbackConfirmed'):
 assert x in writer,x
assert order(writer,'connection.BeginTransaction()', 'SELECT TOP (2) Id, BranchId, IS_Deleted',
             'SELECT TOP (2) GlobalID, IS_Deleted, state, id', 'SELECT AccountCode FROM Customers WITH (UPDLOCK,HOLDLOCK)', 'debit != noteAmount || credit != noteAmount',
             'cmd.ExecuteNonQuery()', 'WriteEntryInTransaction(d.Journal, connection, transaction, d.IsNew)',
             'commitStarted = true', 'transaction.Commit()', 'return true')
assert 'SaveEnty(' not in writer
saver=part(r,'public bool SaveCreditDebtNote(', 'private bool SaveCreditDebtNoteLocked(')
deleter=part(r,'public bool DeleteCreditNote(', 'private bool DeleteCreditNoteLocked(')
for s in (saver,deleter):assert 'lock (NoteDeleteGate)' in s and 'if (noteDeleteNeedsReview)' in s
for name in ('frmCreditNote','frmDebtNote'):
 form=load('Form_WPF/'+name+'.xaml.cs'); save=part(form,'private void Save()', '#endregion' if name=='frmCreditNote' else 'private Entry BuildEntry()')
 assert 'SaveCreditDebtNote(draft)' in save and 'SaveEnty(' not in save and 'BeginTransaction(' not in save
 assert order(save,'bool isNew', 'GetEntryGlobalID(', 'SaveCreditDebtNote(draft)', 'committed = true')
 assert 'if (!double.TryParse' in save and 'double.IsFinite' in save and 'int.TryParse' in save
 assert 'previous < 0' in save and 'discount > invoiceValue - previous' in save and 'net != displayNet' in save
 assert 'InvoiceValue = invoiceValue' in save and ('Code = number;' if name=='frmCreditNote' else '_currentCode = number;') in save
 assert 'تم الحفظ، لكن تعذر تحديث الواجهة' in save

ids=part(load('Class/EntryOper.cs'),'public static void GetEntryGlobalID(', '#endregion')
assert '@branch' in ids and '@globalId' in ids and 'checked(entryNo + 1)' in ids
assert "GlobalID = '{entryGlobalId}'" not in ids

# Transaction tests model intended invariant, not SQL Server isolation, locking,
# triggers, exception delivery or execution of the implementation itself.
def execute(existing=False, failure=None, note_branch=3, note_duplicate=False,
            entry_duplicate=False, foreign_entry=False, wrong_amount=False, party_correct=True):
 db=sqlite3.connect(':memory:')
 db.executescript('create table note(id integer primary key, number int, typ int, branch int, deleted int, date text, val int);'
                  'create table entry(gid text primary key, number int, typ int, branch int, deleted int, state int, id int, date text, val int);'
                  'create table lines(gid text, value int);')
 if existing:
  db.execute("insert into note values(1,8,1,?,0,'old',10)",(note_branch,))
  db.execute("insert into entry values('3-77',8,16,3,0,1,77,'old',10)")
  db.execute("insert into lines values('3-77',10)")
 if note_duplicate:db.execute("insert into note values(2,8,1,9,0,'old',10)")
 if entry_duplicate:db.execute("insert into entry values('other',8,16,3,0,1,78,'old',10)")
 if foreign_entry:db.execute("insert into entry values('3-77',99,4,3,0,1,77,'old',10)")
 db.commit()
 def snapshot():return tuple(db.execute(f'select * from {t} order by 1').fetchall() for t in ('note','entry','lines'))
 before=snapshot()
 try:
  db.execute('begin')
  n=db.execute('select id,branch,deleted from note where number=8 and typ=1').fetchall()
  e=db.execute('select gid,deleted,state,id from entry where branch=3 and typ=16 and number=8').fetchall()
  if existing:
   if len(n)!=1 or n[0][1:]!=(3,0) or len(e)!=1 or e[0][:3]!=('3-77',0,1):raise ValueError()
  elif n or e: raise ValueError()
  if wrong_amount or not party_correct:raise ValueError()
  if existing:db.execute("update note set date='new',val=20 where id=1")
  else:db.execute("insert into note values(1,8,1,3,0,'new',20)")
  if failure=='header':raise ValueError()
  if existing:
   db.execute("update entry set date='new',val=20 where gid='3-77'");db.execute("delete from lines where gid='3-77'")
  else: db.execute("insert into entry values('3-77',8,16,3,0,1,77,'new',20)")
  if failure=='entry':raise ValueError()
  db.execute("insert into lines values('3-77',20)")
  if failure=='line':raise ValueError()
  db.commit();ok=True
 except (ValueError,sqlite3.IntegrityError):
  db.rollback();ok=False
 return ok,before,snapshot()
for existing in (False,True):
 for stage in ('header','entry','line'):
  ok,before,after=execute(existing,failure=stage);assert not ok and before==after
 ok,before,after=execute(existing);assert ok
 assert after==([(1,8,1,3,0,'new',20)],[('3-77',8,16,3,0,1,77,'new',20)],[('3-77',20)])
for kw in ({'existing':True,'note_branch':None},{'existing':True,'note_branch':4},
           {'existing':True,'note_duplicate':True},{'existing':True,'entry_duplicate':True},
           {'existing':False,'foreign_entry':True},{'existing':True,'wrong_amount':True},{'existing':True,'party_correct':False},
           {'existing':False,'note_duplicate':True}):
 ok,before,after=execute(**kw);assert not ok and before==after,kw
# Abstract outcome policy: a lost commit acknowledgement or rollback failure
# blocks both mutation paths in this process, while a confirmed rollback does not.
def review_gate(commit_started, rollback_ok): return commit_started or not rollback_ok
assert not review_gate(False,True)
for started,rolled in ((True,True),(True,False),(False,False)):
 blocked=review_gate(started,rolled)
 assert blocked and all(blocked for action in ('save','delete'))
print('PASS: shared note posting source witnesses and synthetic SQLite fault/identity models')
