#!/usr/bin/env python3
"""Static contracts + SQLite fixtures, not C#/SQL Server/security acceptance."""
from pathlib import Path
import sqlite3
root=Path(__file__).resolve().parents[2]/'SmartAuditERP/Form_WPF'
def load(n): return (root/(n+'.xaml.cs')).read_text(encoding='utf-8-sig')
def section(s,a,b): return s[s.index(a):s.index(b,s.index(a))]
def before(s,a,b): assert s.index(a)<s.index(b),(a,b)
server=load('frmServerSetting'); recycle=load('frmDataRecycling')
for s in (server,recycle):
 for bad in ('CREATE LOGIN [auditor]', 'ALTER SERVER ROLE [sysadmin]', 'ALTER LOGIN sa', 'ALTER ROLE [db_owner] ADD MEMBER'):
  assert bad not in s
setup=section(server,'private void ExecuteDbSetup(', '#endregion')
assert 'throw new InvalidOperationException' in setup and 'ExecuteNonQuery' not in setup
for name in ('btnCreateDatabase_Click','btnRestoreFromScript_Click'):
 body=section(server,'private void '+name+'(', '\n        private void ')
 before(body,'EnsureDatabaseProvisioningAvailable();','localConn.Open();')
assert 'throw new InvalidOperationException' in section(server,'private static void EnsureDatabaseProvisioningAvailable()', 'private void ExecuteDbSetup(')
next_=section(recycle,'private void BtnNext_Click(', 'private void BtnPrevious_Click(')
before(next_,'if (_currentStep == 6) EnsureRecyclingAvailable();','_currentStep++;')
for a,z,write in [('private void CreateDatabase()', '#endregion', 'masterConn.Open()'),('private void ApplyRecycling()', '#endregion', 'ExecuteWithErrorHandling(')]:
 body=section(recycle,a,z);before(body,'EnsureRecyclingAvailable();',write)
assert 'throw new InvalidOperationException' in section(recycle,'private static void EnsureRecyclingAvailable()', 'private void CreateDatabase()')
check=load('frmCheckPwd'); switch=section(check,'switch (CheckType)', 'private void CheckDatabasePassword(')
for n in (0,100,200,300,400): assert 'case '+str(n)+':' in switch
assert 'Iscorrect = false;' in switch and 'ValidateFixedPassword' not in check
assert 'case 1:' in switch and 'CheckDatabasePassword(enteredPassword);' in switch
admin=section(load('frmLogServerSettings'),'private void Check()', '#endregion')
assert 'Iscorrect = false;' in admin and 'Iscorrect = true' not in admin
login=load('frmUserLogin'); local=section(login,'public async Task<bool> OfflineLogin(', '\n        private void ')
assert 'if (SecureLogin) return false;' in local
assert 'SecureLogin ?' not in local and 'AddWithValue("@Password", txtPwd.Password)' in local
before(local,'if (dt.Rows.Count > 1)', 'dt.Rows[0]["emp"]')
before(local,'Convert.ToInt32(dt.Rows[0]["emp"]) <= 0','bool hasAccess = dtEmpBranch.Rows.Count > 0;')
assert 'CombinedPwd' not in login and '|| Convert.ToInt32(dt.Rows[0]["emp"]) == 0' not in local
close=load('frmCloseShift'); query=section(close,'private string BuildGetCloseDataQuery(', 'private void ProcessGetCloseDataRow(')
assert 'ExecuteNonQuery' not in query and 'UPDATE [Inv]' not in query
assert 'cash IS NULL OR tot_net IS NULL OR cash > tot_net' in query
for p in ('branch = @Branch','sales_emp = @EmpId','Inv.date >= @date1','Inv.date <= @date2','Inv.IS_Deleted = 0'): assert p in query
calc=section(close,'private CloseShift GetCloseData(', 'private string BuildGetCloseDataQuery(')
before(calc,'adapter.Fill(dataTable);', 'row["InvalidCashCount"]')
before(calc,'row["InvalidCashCount"]','ProcessGetCloseDataRow(closeShift, row)')
assert 'return null;' in calc and 'if (reCloseData == null)' in close

# Test the same grouping policy over synthetic rows; fixtures are not SQL Server execution.
c=sqlite3.connect(':memory:');c.execute('create table Inv(branch int, emp int, date text, deleted int, kind int, op int, cash real, net real)')
c.executemany('insert into Inv values (?,?,?,?,?,?,?,?)',[
 (1,7,'2026-01-02',0,2,1,10,10),(1,7,'2026-01-02',0,2,1,3,4),
 (2,7,'2026-01-02',0,2,1,100,1),(1,8,'2026-01-02',0,2,1,100,1),
 (1,7,'2026-01-03',0,2,1,100,1),(1,7,'2026-01-02',1,2,1,100,1)])
def selected():
 return c.execute('select sum(case when cash is null or net is null or cash>net then 1 else 0 end),sum(cash) from Inv where branch=? and emp=? and date>=? and date<=? and deleted=0 and kind in (2,3) and op in (1,2)',(1,7,'2026-01-02','2026-01-02')).fetchone()
assert selected()==(0,13)
c.execute('insert into Inv values (1,7,\'2026-01-02\',0,3,2,NULL,10)');assert selected()[0]==1
c.execute('insert into Inv values (1,7,\'2026-01-02\',0,2,1,5,4)');assert selected()[0]==2
assert c.execute('select cash,net from Inv where branch=2').fetchone()==(100,1)
print('PASS: fail-closed local privileged paths and readonly shift query (static and synthetic only)')
