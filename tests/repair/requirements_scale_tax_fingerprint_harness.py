#!/usr/bin/env python3
"""Source contracts and independent models; not SQL Server, CLR, COM, WPF or ERP tests."""
from pathlib import Path
import sqlite3
import math
ROOT = Path(__file__).resolve().parents[2] / 'SmartAuditERP'
n=0

def read(file): return (ROOT / file).read_text(encoding='utf-8-sig')
def part(s,a,b): return s[s.index(a):s.index(b,s.index(a))]
def check(name, ok):
    global n
    assert ok,name
    n+=1
    print('PASS',name)
def ordered(s,*parts):
    i=0
    for p in parts:
        i=s.find(p,i)
        if i<0: return False
        i+=len(p)
    return True

op=part(read('Class/ItemOper.cs'),'public static void SearchForBarcode(', '#endregion')
check('exact barcode values are parameterized without 100-character truncation',op.count('Parameters.Add("@barcode", SqlDbType.NVarChar, -1).Value = barcode;')==2)
check('scale prefix matched to its unit or item base unit', 'ItemUnits.barcode=@prefix' in op and 'Items.barcode=@prefix and ItemUnits.unit=Items.unit' in op)
check('ambiguous scale matches rejected before identifying item',ordered(op,'adapter.SelectCommand.Parameters.Add("@prefix"','if (dt.Rows.Count > 1)','return;','if (dt.Rows.Count == 1)','itemId = ToInt('))
check('scale prefix parameterized','Parameters.Add("@prefix", SqlDbType.NVarChar, 100).Value = shortBarcode;' in op)
for file,price,qty,identity in [('frmInvSale','itemPrice','itemQuantity','itemID'),('frmInvPurch','itemPrice','itemQuantity','itemID'),('frmInvInputOutput','foundPrice','foundQty','foundItemId')]:
    src=read('Form_WPF/'+file+'.xaml.cs')
    bar=part(src,'private void ReadBarcode(', '\n        private void ')
    check(file+' refuses unhandled payload before insertion',ordered(bar,'bool previousScalePriceFlag = ItemOper.IsPriceFromBarcode;', 'ItemOper.SearchForBarcode(', f'if ({identity} > 0 && ({price} > 0 || {qty} > 0))', 'ItemOper.IsPriceFromBarcode = previousScalePriceFlag;', 'return;', 'SearchByID('))

req=read('Form_WPF/frmRequirementPM.xaml.cs');contract=read('Form_WPF/frmContractPM.xaml.cs');ddl=read('Properties/Resources.resx')
check('shipped requirement sub has only requirement key and no soft delete', ordered(ddl,'CREATE TABLE [dbo].[PM_RequirementSub](', 'CONSTRAINT [PK_PM_RequirementSub]', '[RequirNo] ASC') and 'IsDeleted' not in part(ddl,'CREATE TABLE [dbo].[PM_RequirementSub](', ') ON [PRIMARY]'))
load=part(req,'public static DataTable LoadRequirementLines(', 'private void ReadData(')
check('schema and view definition required before interpreting metadata',ordered(load, "OBJECT_ID(N'dbo.PM_RequirementSub',N'U')", "HAS_PERMS_BY_NAME(N'dbo.PM_RequirementSub'", "COL_LENGTH(N'dbo.PM_RequirementSub',N'IsDeleted')", 'if (schemaState < 0)', 'throw new InvalidOperationException'))
check('optional soft-delete used only when present', '(schemaState == 1 ? " AND IsDeleted=0" : "")' in load)
check('requirement number passed as integer parameter', 'Parameters.Add("@requirement", SqlDbType.Int).Value = requirementNumber;' in load)
check('connection closed only when loader opened it','bool opened = connection.State != ConnectionState.Open;' in load and 'finally { if (opened) connection.Close(); }' in load)
nav=part(req,'private void Navigate(', 'public static DataTable LoadRequirementLines(')
check('navigation materializes header and rejects duplicate selection',ordered(nav,'adapter.Fill(headers);','headers.Rows.Count == 0','headers.Rows.Count != 1','ReadData(headers.Rows[0]);'))
check('search selection does not preemptively mutate identity','_code = row.id;' not in part(req,'private void dgvSrch_MouseDoubleClick(', '#endregion'))
rd=part(req,'private void ReadData(DataRow header)', 'private void btnFirst_Click')
check('lines mapped before clearing form',ordered(rd,'LoadRequirementLines(_conn, code)', 'staged.Add(', 'CLR();', '_code = code;', 'foreach (var row in staged)'))
check('contract line load stages before replacing rows',ordered(contract,'public void LoadRequirements(', 'LoadRequirementLines(_connection, requirementNumber)', 'staged.Add(', 'TermRows.Clear();', 'TermRows.Add(row);'))
check('contract request uses persisted identity and warns about edits',ordered(req,'private void btnAddContract_Click(', 'if (_code <= 0 || _termsSource.Count == 0)', 'MessageBoxResult.Yes', 'frm.LoadRequirements(_code);'))
search=part(req,'private void Search()', 'private void dgvSrch_MouseDoubleClick')
check('requirement search validates and binds user number',ordered(search,'int.TryParse(txtSrchNo.Text.Trim()', 'PM_Requirement.RequirNo=@requirementNumber', 'Parameters.Add("@requirementNumber", SqlDbType.Int)'))
save=part(req,'private void btnSave_Click(', 'private static bool IsExactSqlInt(')
check('unsure outcome and saved orders rejected before transaction', ordered(save,'if (_saveOutcomeUnknown)', 'if (_code != -1)', '_conn.BeginTransaction()'))
check('quantity and reference exact before int write',ordered(save,'!IsExactSqlInt(row.Qty) || !IsExactSqlInt(row.RefNo)', '_conn.BeginTransaction()', '(int)row.Qty', '(int)row.RefNo'))
check('header and detail use same positive integer identity', 'int.TryParse(txtNo.Text, out int reqNo) || reqNo <= 0' in save and save.count('Value      = reqNo;')==2)
check('commit before saved identity and success UI',ordered(save,'commitAttempted = true;', 'transaction.Commit();', 'committed = true;', '_code = reqNo;', 'savedMsg.ShowDialog();'))
check('unknown commit and failed rollback block retry', 'if (commitAttempted && !committed) _saveOutcomeUnknown = true;' in save and ordered(save,'transaction.Rollback();', 'catch', '_saveOutcomeUnknown = true;'))
check('new action does not clear unknown outcome','_saveOutcomeUnknown = false;' not in part(req,'private void CLR()', '#region Load Data'))

tax=read('Form_WPF/frmTaxRptPeriod.xaml.cs');show=part(tax,'private void ShowDetails22()', '#endregion')
check('tax report fails closed before query without session branch',ordered(show,'_reportPublished = false;', 'ClearReportCells();','chkAllBranches.IsChecked == true','branchId != MainClass.BranchNo','return;','string sqlSales'))
check('receipt query uses same branch condition as expenses', 'FROM Receipts WHERE ReceiptType=10 AND {branchBranch}' in show and 'FROM Receipts WHERE ReceiptType=9 AND {branchBranch}' in show and 'branchID={MainClass.BranchNo}' not in show)
check('tax branch checkbox and selection invalidate printable publication',tax.count('_reportPublished = false;')>=5 and ordered(tax,'private void chkAllBranches_CheckedChanged(', '_reportPublished = false;', 'ClearReportCells();', 'private void cmbBranches_SelectionChanged(', '_reportPublished = false;', 'ClearReportCells();'))

fp=read('Class/FingerPrintDevice.cs');imp=part(fp,'public static void loadAttendData()', '\n\t}\n}')
check('only one fingerprint import per process', 'Interlocked.CompareExchange(ref _importRunning, 1, 0) != 0' in imp and 'Interlocked.Exchange(ref _importRunning, 0);' in imp)
check('locked fingerprint replay never touches device or database',ordered(imp,'if (Volatile.Read(ref _replayRiskLocked) != 0) return;', 'conn.Open()', 'EnableDevice('))
check('fingerprint latch held before commit until confirmed clear',ordered(imp,'Volatile.Write(ref _replayRiskLocked, 1);','sqlTransaction.Commit();','committed = true;','if (FingerPrintDevice.axCZKEM1.ClearGLog','Volatile.Write(ref _replayRiskLocked, 0);'))
check('uncommitted transaction attempts rollback and locks on failure', ordered(imp,'if (sqlTransaction != null && !committed)', 'sqlTransaction.Rollback();', 'catch (Exception ex)', 'Volatile.Write(ref _replayRiskLocked, 1);'))
check('new replay lock alerts and logs operator once per session', 'needsReconciliation && !alreadyLocked' in imp and 'MessageBox.Show(' in imp and 'reconcile database and device logs' in imp)
check('device recovery and cleanup still attempted','bFlag: true' in imp and 'conn.Close()' in imp)

# SQLite is an independent illustrative data model, not SQL Server validation.
db=sqlite3.connect(':memory:')
db.executescript("CREATE TABLE Items(id INT,unit INT,barcode TEXT); CREATE TABLE ItemUnits(ItemId INT,unit INT,barcode TEXT); INSERT INTO Items VALUES(1,10,'1234567'); INSERT INTO ItemUnits VALUES(1,10,'base'),(1,11,'carton');")
q='SELECT i.id,u.unit FROM Items i JOIN ItemUnits u ON u.ItemId=i.id WHERE u.barcode=? OR (i.barcode=? AND u.unit=i.unit)'
check('base-prefix chooses base unit not arbitrary alternate',db.execute(q,('1234567','1234567')).fetchall()==[(1,10)])
db.execute("UPDATE ItemUnits SET barcode='1234567' WHERE unit=11")
check('conflicting exact unit and base prefix is ambiguous',len(db.execute(q,('1234567','1234567')).fetchall())==2)
db.execute('CREATE TABLE plain(RequirNo INT, TermPk INT)');db.executemany('INSERT INTO plain VALUES(?,?)',[(2,5),(3,9)])
check('without optional soft-delete all matching rows retained',db.execute('SELECT TermPk FROM plain WHERE RequirNo=?',(2,)).fetchall()==[(5,)])
db.execute('CREATE TABLE extended(RequirNo INT, TermPk INT, IsDeleted INT)');db.executemany('INSERT INTO extended VALUES(?,?,?)',[(2,5,0),(2,6,1),(2,7,None)])
check('with optional soft-delete excludes deleted and null',db.execute('SELECT TermPk FROM extended WHERE RequirNo=? AND IsDeleted=0',(2,)).fetchall()==[(5,)])
for val,valid in [(1.0,True),(2.5,False),(-1.0,True),(float('nan'),False),(float('inf'),False),(2**31,False)]:
    got=math.isfinite(val) and -(2**31)<=val<=2**31-1 and math.trunc(val)==val
    check('integer input model '+repr(val),got==valid)
for committed,cleared,rollback_failed,expected in [(True,True,False,False),(True,False,False,True),(False,False,True,True),(False,False,False,False)]:
    # Unknown commit also latches; represented as committed=True/clear=False.
    got=(committed and not cleared) or rollback_failed
    check('fingerprint reconciliation model '+repr((committed,cleared,rollback_failed)),got==expected)
for all_br,selected,session,expected in [(False,1,1,True),(True,1,1,False),(False,2,1,False),(False,None,1,False),(False,1,-1,False)]:
    got=not all_br and selected is not None and selected>0 and session>0 and selected==session
    check('tax session branch model '+repr((all_br,selected,session)),got==expected)
print(f'RESULT: PASS — {n} source/model checks; not CLR/WPF/SQL Server/COM or financial acceptance.')
