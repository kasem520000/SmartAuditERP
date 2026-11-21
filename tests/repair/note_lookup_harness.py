#!/usr/bin/env python3
"""R-256/H-004: static witnesses + SQLite models; not SQL Server, WPF, or authorization."""
from pathlib import Path
import sqlite3
root=Path(__file__).resolve().parents[2]/'SmartAuditERP/Form_WPF'
def section(s,a,b):return s[s.index(a):s.index(b,s.index(a))]
for name,inv,name_method,picker,balance,num_lookup,invoice_load,amount in [
 ('frmCreditNote','InvoiceSrch','SearchByName','AddNewItem','GetCustBalance','SearchByInvNo','LoadInvData','txtInvVal.Text = string.Empty;'),
 ('frmDebtNote','InvoiceSearch','SearchByClientName','OpenAccountSearch','GetClientBalance','SearchByInvoiceNumber','LoadInvoiceData','txtInvVal.EditValue = null;')]:
 s=(root/(name+'.xaml.cs')).read_text(encoding='utf-8-sig')
 i=section(s,'private void '+inv+'()', 'private void '+num_lookup+'(')
 assert 'InvGlobalID=@globalId' in i and 'Parameters.Add("@globalId", SqlDbType.NVarChar)' in i
 assert 'Rows.Count != 1' in i and 'catch (Exception ex)' in i and amount in i
 n=section(s,'private void '+name_method+'()', 'private void '+picker+'(')
 assert 'name=@name' in n and 'Parameters.Add("@name", SqlDbType.NVarChar)' in n
 assert 'Rows.Count == 1' in n and 'Rows.Count == 0' in n and 'مكرر' in n
 p=s[s.index('private void '+picker+'('):];p=p[:p.index('\n        }')]
 assert 'Rows.Count == 1' in p and 'وحيد' in p
 b=s[s.index('private void '+balance+'()'):];b=b[:b.index('\n        }')]
 assert 'AName=@accountName' in b and 'Parameters.Add("@accountName", SqlDbType.NVarChar)' in b
 assert 'Rows.Count != 1' in b and b.count(amount)>=2
 numeric=section(s,'private void '+num_lookup+'(', 'private void '+name_method+'(' if name=='frmDebtNote' else 'private void IsDiscounted(')
 assert 'Rows.Count > 1' in numeric and 'Rows.Count == 1' in numeric and amount in numeric
 load=s[s.index('private void '+invoice_load+'('):];load=load[:load.index('\n        }')]
 assert amount in load and 'Rows.Count != 1' in load
 assert "AName=N'{" not in s and "name=N'{" not in s and "InvGlobalID=N'{" not in s

# Literal predicates and no first-match when a display name or local invoice ID
# belongs to multiple records. Does not simulate live branch authorization.
db=sqlite3.connect(':memory:')
db.executescript('create table party(id int,name text);create table inv(gid text,number int,branch int);')
db.executemany('insert into party values (?,?)',[(1,"O'Brien"),(2,'duplicate'),(3,'duplicate')])
db.executemany('insert into inv values (?,?,?)',[("a'1",8,1),('b',8,2),('c',9,1)])
def unique(sql,param):
 rows=db.execute(sql,(param,)).fetchall()
 return rows[0] if len(rows)==1 else None
assert unique('select id from party where name=?',"O'Brien")==(1,)
assert unique('select id from party where name=?',"x' OR 1=1 --") is None
assert unique('select id from party where name=?','duplicate') is None
assert unique('select gid from inv where number=?',8) is None
assert unique('select gid from inv where number=?',9)==('c',)
assert unique('select number from inv where gid=?',"a'1")==(8,)
assert unique('select number from inv where gid=?',"x' OR 1=1 --") is None
print('PASS: note lookups reject ambiguity and stale balances (static + synthetic models)')
