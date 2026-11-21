#!/usr/bin/env python3
"""R-252..254/H-003: source witnesses and independent SQLite models.
Not .NET, SQL Server, WPF, authorization penetration tests, or accounting acceptance.
"""
from pathlib import Path
import sqlite3
root=Path(__file__).resolve().parents[2]/'SmartAuditERP'
def load(p, encoding='utf-8-sig'): return (root/p).read_text(encoding=encoding)
def part(s,a,b): return s[s.index(a):s.index(b,s.index(a))]
def ordered(s,*parts):
 i=-1
 for x in parts:i=s.index(x,i+1)
 return True
main=load('Class/MainClass.cs');form=load('Class/FormPermission.cs','latin-1');common=load('Class/Common.cs')
wpf=part(main,'public static void ApplyPermissionToForm(System.Windows.Window window)','private static bool[] ReadUiPermissions(')
assert ordered(wpf,'if (!window.IsLoaded)', 'window.Loaded += loaded', 'permissions = ReadUiPermissions(formName)', 'ApplyWpfPermissions(window, permissions[0]')
lookup=part(main,'private static bool[] ReadUiPermissions(', 'private static void ApplyWpfPermissions(')
for x in ('UserID <= 0','Forms.FormName=@formName','user_id=@userId','table.Rows.Count != 1','DBNull.Value','SqlDbType.NVarChar','SqlDbType.Int'):assert x in lookup,x
win=part(main,'public static void ApplyPermissionToForm(System.Windows.Forms.Form frm)','private static void ApplyWinFormsIconBtnPermission(')
assert ordered(win,'bool[] permissions = new bool[5]', 'permissions = ReadUiPermissions(formName)', 'catch (Exception ex)', 'ApplyWinFormsIconBtnPermission(')
fp=part(form,'private void ApplyFrmPermissionInternal(', '#endregion')
assert ordered(fp,'Addable = Editable = Delete = Search = Print = false;', 'MainClass.UserID > 0', 'permissionTable.Rows.Count == 1', 'Addable = GetBool(row, "IS_New")', 'GetTargetButtons(rootElement)')
assert 'GetBool(row, "IS_Save")' in fp and 'catch (Exception ex)' in fp
assert main.count('if (!canNew && (name == "btnNew" || name == "btnSave")) disable = true;') == 2
commonbody=part(common,'private static void ApplyEditAddPermissionInternal(', 'private static IEnumerable<T> FindVisualChildren<T>(')
assert 'button.IsEnabled = false' in commonbody and 'button.IsEnabled = true' not in commonbody
# Model exact-one grant selection; flags are independent of which buttons are discoverable.
def grant(rows,broken=False,user=1):
 if broken or user<=0 or len(rows)!=1:return [False]*5
 return [v is True or v==1 for v in rows[0]]
assert grant([[1,0,None,1,1]])==[True,False,False,True,True]
assert grant([])==[False]*5 and grant([[1]*5,[1]*5])==[False]*5
assert grant([[1]*5],True)==[False]*5 and grant([[1]*5],user=0)==[False]*5
# A safety-disabled button remains disabled even with an add grant.
def apply(current,allowed):return current if allowed else False
assert not apply(False,True) and not apply(True,False) and apply(True,True)

a=load('Class/ReceiptOper.cs'); entry=load('Class/EntryOper.cs')
search=part(a,'public static DataTable LoadReceipts(', 'public async Task SyncReceipt(')
for x in ('int.TryParse(receiptNumber.Trim()', 'parsed <= 0','@type','@branch','@number','@reference','@start','@endExclusive','endDate.Date.AddDays(1)','endDate.Date < startDate.Date','endDate.Date == DateTime.MaxValue.Date','adapter.Fill(result)'):
 assert x in search,x
assert 'string cond' not in search and 'catch' not in search
for name in ['frmSandD','frmSandQAndroid','frmSandSD','frmSandQD']:
 s=load('Form_WPF/'+name+'.xaml.cs');b=part(s,'private void Search()', '#endregion')
 assert 'LoadReceipts(ReceiptType, MainClass.BranchNo,' in b and 'txtSrchNo.Text, txtSrchRef.Text' in b
 assert 'AName=N\'' not in b and 'condition +=' not in b and 'cond +=' not in b and 'catch (Exception ex)' in b
 assert ('SearchList.Clear();' if name in ('frmSandD','frmSandQAndroid') else '_searchItems.Clear();') in b
for name in ['frmSandD','frmSandQAndroid']:
 s=load('Form_WPF/'+name+'.xaml.cs');b=part(s,'private void GetCustBalance()', '#endregion')
 assert 'AName=@accountName' in b and 'dt.Rows.Count != 1' in b and 'SqlDbType.NVarChar' in b
 assert b.count('txtBalance.Text = string.Empty;')==2 and 'catch (Exception ex)' in b
# Demonstrate literal reference matching and a half-open day, not SQL Server.
db=sqlite3.connect(':memory:');db.execute('create table receipts(branch int, typ int, num int, ref text, dt text)')
db.executemany('insert into receipts values(?,?,?,?,?)',[(1,7,1,"O'Brien",'2024-01-01 23:59:59.999'),(1,7,2,'x','2024-01-02 00:00:00'),(2,7,3,'x','2024-01-01 12:00:00')])
def srch(branch,ref): return db.execute('select num from receipts where branch=? and typ=? and ref=? and dt>=? and dt<?',(branch,7,ref,'2024-01-01','2024-01-02')).fetchall()
assert srch(1,"O'Brien")==[(1,)] and srch(1,"x' OR 1=1 --")==[] and srch(1,'x')==[]

note=part(a,'private bool DeleteCreditNoteLocked(', 'public static int ReceiptNo(')
for x in ('branch <= 0','noteType != 1 && noteType != 2','entryId == "-1"','TOP (2) Id, BranchId, IS_Deleted', 'reader.IsDBNull(1)', 'if (reader.Read()) throw', 'TOP (2) GlobalID, IS_Deleted, state', 'StringComparison.Ordinal', 'WHERE Id=@id AND BranchId=@branch', 'doc_no=@number AND IS_Deleted=0 AND state=1','update.ExecuteNonQuery() != 1','commitStarted = true','transaction.Commit()', 'transaction.Rollback()', 'noteDeleteNeedsReview = true'):
 assert x in note,x
assert 'lock (NoteDeleteGate)' in a
readid=part(entry,'public static string ReadEntryGlobalID(', '#endregion')
assert 'int.TryParse(docNo' in readid and 'SELECT TOP (2) GlobalID' in readid and 'reader.Read() ? string.Empty : id' in readid and 'doc_no=@number' in readid

# Models exact-one and paired rollback, including ambiguous and cross-branch history.
def delete(notes, entries, number=11, typ=1, branch=1, gid='e', fail=False):
 db=sqlite3.connect(':memory:')
 db.executescript('create table notes(id int, num int, typ int, branch int, deleted int);create table entries(id text, num int, typ int, branch int, deleted int, state int);')
 db.executemany('insert into notes values(?,?,?,?,?)',notes);db.executemany('insert into entries values(?,?,?,?,?,?)',entries);db.commit()
 before=(db.execute('select * from notes order by id').fetchall(),db.execute('select * from entries order by id').fetchall())
 try:
  db.execute('begin')
  ns=db.execute('select id,branch,deleted from notes where num=? and typ=?',(number,typ)).fetchall()
  es=db.execute('select id,deleted,state from entries where branch=? and typ=? and num=?',(branch,16 if typ==1 else 17,number)).fetchall()
  if len(ns)!=1 or ns[0][1:]!=(branch,0) or len(es)!=1 or es[0]!=(gid,0,1):raise ValueError()
  db.execute('update notes set deleted=1 where id=?',(ns[0][0],))
  if fail:raise ValueError()
  db.execute('update entries set deleted=1,state=2 where id=?',(gid,));db.commit();ok=True
 except ValueError:db.rollback();ok=False
 after=(db.execute('select * from notes order by id').fetchall(),db.execute('select * from entries order by id').fetchall())
 return ok,before,after
n=[(1,11,1,1,0)];e=[('e',11,16,1,0,1)]
ok,before,after=delete(n,e);assert ok and after==([(1,11,1,1,1)],[('e',11,16,1,1,2)])
for ns,es,gid in [(n,e,'wrong'), ([(1,11,1,None,0)],e,'e'), ([(1,11,1,2,0)],e,'e'), (n+[(2,11,1,2,0)],e,'e'),(n,e+[('e2',11,16,1,0,1)],'e'),(n,[],'e')]:
 ok,before,after=delete(ns,es,gid=gid);assert not ok and before==after
ok,before,after=delete(n,e,fail=True);assert not ok and before==after
print('PASS: permission, receipt search and note-delete static witnesses + independent SQLite models')
