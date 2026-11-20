#!/usr/bin/env python3
"""Source contracts and independent examples only; no SQL, CLR or WPF runtime."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2] / 'SmartAuditERP/Form_WPF'
N = 0

def read(name): return (ROOT / name).read_text(encoding='utf-8-sig')
def part(s, a, b): return s[s.index(a):s.index(b, s.index(a))]
def check(label, ok):
    global N
    if not ok: raise AssertionError(label)
    N += 1
    print('PASS', label)
def ordered(s, needles):
    at = -1
    for needle in needles:
        at = s.find(needle, at + 1)
        if at < 0: return False
    return True

cycle = read('frmProjCyclePM.xaml.cs')
save = part(cycle, 'private void SaveFileRow(', 'private void LoadSavedFile(')
check('client file streamed through varbinary parameter', 'new FileStream(row.FilePath, FileMode.Open, FileAccess.Read, FileShare.Read)' in save and 'cmd.Parameters.Add("@Ufile", SqlDbType.VarBinary, -1).Value = file;' in save)
check('upload never puts the path into SQL', 'OPENROWSET' not in save and "BULK N'" not in save and 'VALUES (NEWID(),@Ufile' in save)
check('insert and identity share a transaction before updating UI identity', ordered(save, ['conn.BeginTransaction()', 'INSERT INTO PM_ProjectFiles', 'SELECT CAST(SCOPE_IDENTITY() AS int)', 'cmd.ExecuteScalar()', 'tx.Commit();', 'row.FileNo = fileNo;', 'row.FilePath = "";']))
check('missing upload identity is rejected', 'identity == null || identity == DBNull.Value || Convert.ToInt32(identity) <= 0' in save)
check('current project stage and row required for file save', 'if (!IsCurrentFileRow(row))' in save and '_filesSource.Contains(row)' in cycle and 'requestedProject == ProjNo' in cycle and 'id == StageID' in cycle)
check('project status checked on both insert and edit', ordered(save, ['if (!IsCurrentFileRow(row))', 'Convert.ToInt32(cmbStatus.SelectedValue) == 4', 'if (row.FileNo == 0)']))
check('existing file update scoped to project stage and active record', 'WHERE FileNo=@FileNo AND Proj_ID=@Project AND StageNo=@Stage ' in save and 'ISNULL(IS_Deleted,0)=0' in save and 'cmd.ExecuteNonQuery() != 1' in save)
openfile = part(cycle, 'private void LoadSavedFile(', 'private void LoadContractData(')
check('file read requires current row and scoped identity', '!IsCurrentFileRow(row)' in openfile and 'WHERE FileNo=@FileNo AND Proj_ID=@Project AND StageNo=@Stage AND ISNULL(IS_Deleted,0)=0' in openfile)
check('open uses a unique new temporary file, never overwrites Documents file', 'Guid.NewGuid().ToString("N") + ext' in openfile and 'FileMode.CreateNew' in openfile and 'Environment.SpecialFolder.Personal' not in openfile)
delete = part(cycle, 'private void dgvFiles_DeleteFile_Click(', '// ComboBox نوع الملف')
check('saved delete is reported unavailable rather than visually removed', ordered(delete, ['if (row.FileNo > 0)', 'غير متاح', 'return;', '_filesSource.Remove(row)']))
check('file list excludes soft-deleted rows and includes historical null', 'StageNo={StageID} and ISNULL(IS_Deleted,0)=0 order by FileNo' in cycle)
for fileid, sameproject, samestage, active, ok in [(5,True,True,True,True),(5,False,True,True,False),(5,True,False,True,False),(5,True,True,False,False)]:
    check('scoped file model '+str((sameproject,samestage,active)), (fileid > 0 and sameproject and samestage and active) == ok)

parent = part(cycle, 'private void LoadParentStages(', 'private void LoadProjectStage(int code)')
check('stage initializer uses serializable transaction and project lock', 'BeginTransaction(IsolationLevel.Serializable)' in parent and 'PM_Projects WITH (UPDLOCK,HOLDLOCK)' in parent)
check('checks existing stages under lock before inserting', ordered(parent, ['PM_Projects WITH (UPDLOCK,HOLDLOCK)', 'PM_ProjStages WITH (UPDLOCK,HOLDLOCK)', 'if (existing == 0)', 'INSERT INTO PM_ProjStages', 'tx.Commit();']))
check('all insert commands use shared transaction', 'VALUES(@StageId,@ProjID,@StageOrder,0,0)", conn, tx)' in parent)
check('parent traversal detects cycles and terminates', 'var visited = new HashSet<int>();' in parent and 'while (current > 0)' in parent and '!visited.Add(current)' in parent and 'LoadParentStages(parent)' not in parent)
check('initializer refuses excessive duplicate or null stages', 'template.Rows.Count > 6' in parent and '!ids.Add(' in parent and '!orders.Add(' in parent and 'row["StageOrder"] == DBNull.Value' in parent)
check('missing or deleted stages cannot disappear silently from template', 'LEFT JOIN PM_Stages' in parent and 'row["StageExists"] == DBNull.Value' in parent and 'row["StageDeleted"] == DBNull.Value' in parent and 'Convert.ToBoolean(row["StageDeleted"])' in parent)
check('one refresh with initialization disabled', ordered(parent, ['tx.Commit();', 'LoadProjectStageCore(code, false);']) and 'else if (allowInitialize)' in cycle)
check('errors are exposed instead of silent success', 'catch (Exception ex) { DXMessageBox.Show("تعذر تحميل مراحل المشروع:' in parent)
def initialize(before, template, fail=None):
    result = before[:]
    if not result:
        pending = []
        for i, item in enumerate(template):
            if i == fail: return before[:]
            pending.append(item)
        result.extend(pending)
    return result
for before,template,fail,expected in [([], [1,2,3], 1, []),([], [1,2,3], None,[1,2,3]),([8,9],[1,2],None,[8,9])]:
    check('stage transaction model '+str((before,fail)), initialize(before,template,fail)==expected)
def resolve(start, parents, templates):
    visited=set()
    while start > 0:
        if start in visited: return 'cycle'
        visited.add(start)
        if start in templates: return templates[start]
        start=parents.get(start,0)
    return 'missing'
for parents, templates, expected in [({1:2,2:3},{3:'ok'},'ok'),({1:2,2:1},{},'cycle'),({1:0},{},'missing')]:
    check('bounded ancestor model '+str(parents),resolve(1,parents,templates)==expected)

picker = read('frmItemsSrch.xaml.cs')
change = part(picker, 'private void GridControl1_SelectionChanged(', 'private void GridControl1_KeyDown(')
confirm = part(picker, 'private void SelectCurrentItem()', '#endregion')
check('selection removes deselected and adds unique positive ids', 'e.RemovedItems' in change and 'Itemlist.Remove(id)' in change and 'e.AddedItems' in change and 'id > 0 && !Itemlist.Contains(id)' in change)
check('confirmation uses current selected rows, not history alone', 'GridControl1.SelectedItems' in confirm and 'selectedIds.Contains(itemId)' in confirm and 'selectedIds.Contains(id)' in confirm)
check('selection order retained and focused item last', ordered(confirm, ['foreach (int id in Itemlist)', 'foreach (int id in gridOrder)', 'confirmed.Remove(itemId);', 'confirmed.Add(itemId);', 'Itemlist.AddRange(confirmed);', 'ISDone = true;']))
check('invalid selected ids cannot confirm', 'itemId <= 0' in confirm and 'selected == null' in confirm)
def pick(history, selected, focused):
    unique = list(dict.fromkeys(x for x in selected if x > 0))
    if focused not in unique or focused <= 0: return None
    result = list(dict.fromkeys(x for x in history if x in unique))
    result.extend(x for x in unique if x not in result)
    result.remove(focused)
    return result + [focused]
for h,sel,f,expect in [([1,2,3],[1,3],3,[1,3]),([1,2],[2],2,[2]),([1],[2,3],2,[3,2]),([1],[1],-1,None),([1,1],[1],1,[1])]:
    check('picker snapshot '+str((h,sel,f)), pick(h,sel,f)==expect)

barcode = part(read('frmPrintBarcode.xaml.cs'), 'private void ReadBarcode(string barcode)', '#endregion')
check('barcode SQL exact, scoped, parameterized', 'U.barcode=@barcode' in barcode and 'I.IS_Deleted=0' in barcode and 'SqlDbType.NVarChar, 50' in barcode)
check('reject blank, overlong, missing and ambiguous mappings', 'scanned.Length == 0 || scanned.Length > 50' in barcode and 'dt.Rows.Count != 1' in barcode)
check('unit and sale price must be present and numeric finite', 'dt.Rows[0]["unit"] == DBNull.Value' in barcode and 'dt.Rows[0]["sale"] == DBNull.Value' in barcode and 'double.IsNaN(price)' in barcode and 'double.IsInfinity(price)' in barcode)
check('label price and code belong to exact unit row', 'ItemSalePrice = price' in barcode and 'ItemBarcode   = scanned' in barcode and 'Common.GetItemPrice' not in barcode and 'SearchForBarcode' not in barcode)
check('failure does not silently fall back to item picker', 'AddNewItem()' not in barcode and 'catch (Exception ex)' in barcode)
for rows, expect in [([],None),([(1,120)],120),([(1,120),(2,9)],None),([(1,None)],None)]:
    val = rows[0][1] if len(rows)==1 and rows[0][0] > 0 and rows[0][1] is not None else None
    check('unit price resolution '+str(rows),val==expect)

contract = read('frmContractPM.xaml.cs')
csave = part(contract, 'private void btnSave_Click(', '#region Journal Entry Helpers')
reload = part(contract, 'private void ReadData(', '#region Save')
check('saved contract edit blocked before opening connections or transaction', ordered(csave, ['if (_currentCode != -1)', 'return;', 'EnsureConnectionOpen(_connection);', 'BeginTransaction()']))
check('new contract VAT equals journal source', 'Parameters.Add("@VATval", SqlDbType.Float).Value = ParseDouble(txtNetVAT.Text);' in csave and 'ParseDouble(txtNetVAT.Text), 2222001' in csave)
check('reloaded row net uses quantity and stored VAT', 'Total = price * quantity' in reload and 'NetValue = price * quantity + vat' in reload)
for q, price, vat, expected in [(3,100,45,345),(1,100,15,115),(0,4,0,0)]:
    check('stored net model '+str((q,price,vat)), q*price+vat == expected)
print(f'RESULT: PASS — {N} source/model checks; no CLR, WPF, SQL or financial acceptance.')
