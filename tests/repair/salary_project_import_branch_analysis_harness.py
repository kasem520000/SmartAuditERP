#!/usr/bin/env python3
"""Source contracts and independent models only, not CLR/WPF/SQL Server acceptance."""
from pathlib import Path
import sqlite3
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2] / 'SmartAuditERP/Form_WPF'
N = 0

def read(name):
    raw = (ROOT / name).read_bytes()
    try: return raw.decode('utf-8-sig')
    except UnicodeDecodeError: return raw.decode('cp1256')
def part(s, start, end): return s[s.index(start):s.index(end, s.index(start))]
def check(label, ok):
    global N
    assert ok, label
    N += 1
    print('PASS', label)
def ordered(s, *values):
    i = 0
    for v in values:
        i = s.find(v, i)
        if i < 0: return False
        i += len(v)
    return True

salary = read('frmSalaryPay.xaml.cs')
check('salary mutation availability explicitly false', ordered(salary, 'private bool SalaryMutationAvailable()', 'DXMessageBox.Show(', 'return false;'))
check('salary insert and update guarded before database', ordered(salary, 'private async void btnSave_Click(', 'if (!SalaryMutationAvailable()) return;', 'conn.Open();', 'UPDATE SalaryPay', 'INSERT INTO SalaryPay'))
check('salary deletion guarded before all writes', ordered(salary, 'private void btnDelete_Click(', 'if (!SalaryMutationAvailable()) return;', 'UPDATE SalaryPay', 'UPDATE Receipts', 'DeleteReceipt('))
for name in ('frmContractPM.xaml.cs', 'frmCashVoucherPM.xaml.cs'):
    s = read(name)
    check(name + ' refuses manual journal save', ordered(s, 'private bool ProjectJournalSaveAvailable()', 'return false;', 'private void btnSave_Click(', 'if (!ProjectJournalSaveAvailable()) return;', 'BeginTransaction()'))
check('accreditation separately remains guarded', 'if (!ProjectAccreditationAvailable()) return;' in read('frmAssignProjectPM.xaml.cs'))
voucher = read('frmCashVoucherPM.xaml.cs')
check('voucher deletion cannot update document and entry separately', ordered(voucher, 'private void btnDelete_Click(', 'if (!ProjectJournalSaveAvailable()) return;', 'UPDATE SandQD', 'UPDATE Entry'))
for name in ('frmcontract.xaml.cs', 'frmSalesInvoice.xaml.cs', 'frmSalePurch.xaml.cs'):
    s = read(name)
    check(name + ' reports import disabled', ordered(s, 'private bool CanImportInvoiceRows()', 'MessageBox.Show(', 'return false;'))
    imp = part(s, 'private void stripImport_Click(', '\n        private void ')
    check(name + ' stops before import dialog or mutation', ordered(imp, 'if (!CanImportInvoiceRows()) return;', 'new frmImportDataGeneral()', 'ShowDialog()', 'SearchByCode('))

for name, method, allbox, items in [
    ('frmRptIncomeStatement', 'public void ShowResult(', 'chkAllBranches', '_dataSource'),
    ('frmMezanyaArba7', 'private void ShowResult()', 'ckAllBranches', '_rows'),
    ('IncomeStatementForm', 'private void btnShow_Click(', 'chkAllBranches', '_incomeRows')]:
    s = read(name+'.xaml.cs'); ET.fromstring(read(name+'.xaml'))
    check(name + ' rejects all or missing/invalid single branch', ordered(s[s.index(method):], allbox+'.IsChecked == true', 'cmbBranches.SelectedIndex < 0', 'cmbBranches.SelectedValue == null', 'int.TryParse(', 'return;'))
    check(name + ' branch changes invalidate displayed rows', 'SelectionChanged="cmbBranches_SelectionChanged"' in read(name+'.xaml') and ordered(s, 'private void cmbBranches_SelectionChanged(', 'if (IsLoaded) InvalidateBranchResult();', 'private void InvalidateBranchResult()', items+'.Clear();'))
    check(name + ' all-branches toggle invalidates result', 'InvalidateBranchResult();' in part(s, 'private void '+ ('ckAllBranches_CheckedChanged' if name=='frmMezanyaArba7' else ('chkAllBranches_Changed' if name=='frmRptIncomeStatement' else 'chkAllBranches_CheckedChanged')), 'private void cmbBranches_SelectionChanged'))
legacy = read('frmRptIncomeStatement.xaml.cs')
check('public legacy entry requires argument equals UI branch', 'selectedBranch != branch' in legacy and 'Entry_sub.branch={selectedBranch}' in legacy)
mez = read('frmMezanyaArba7.xaml.cs')
check('balance branch change also invalidates manually approved stock', ordered(mez, 'private void InvalidateBranchResult()', '_hasApprovedStock = false;', '_Stock = 0;'))

analysis = read('frmRptInvAnalysis.xaml.cs'); ET.fromstring(read('frmRptInvAnalysis.xaml'))
launch = part(analysis, 'private void btnShow_Click(', 'private void ShowResult()')
check('analysis validates on UI before thread starts', ordered(launch, 'InvalidateAnalysisResult();', 'ValidateAnalysisSelection()', 'new Thread('))
check('filtered group blocked for header aggregates before thread', ordered(launch, 'chkAllGroups.IsChecked != true', 'rdItem.IsChecked == true || rdGroup.IsChecked == true', 'return;', 'new Thread('))
check('analysis disallows reentry and freezes group and modes', all(v in launch for v in ('if (_analysisRunning) return;', '_analysisRunning = true;', 'chkAllGroups, cmbGroups, rdStock, rdCust, rdItem', 'controls[i].IsEnabled = false;', 'controls[i].IsEnabled = enabled[i];', '_analysisRunning = false;')))
for mode in ('Cust', 'Salesman', 'Emp', 'Month', 'Day', 'Stock'):
    method = part(analysis, 'private void ShowResult'+mode+'()', '#endregion')
    check('captured filtered group refused in '+mode, ordered(method, 'bool allGroups = GetCheckState(chkAllGroups);', 'if (!allGroups)', 'return;', 'ItemsCategory.id={groupVal}'))
check('group and mode changes invalidate result', 'SelectionChanged="cmbGroups_SelectionChanged"' in read('frmRptInvAnalysis.xaml') and analysis.count('if (IsLoaded) InvalidateAnalysisResult();') >= 10)
check('obsolete worker cannot publish rows or totals', 'if (_activeAnalysisVersion == _analysisVersion) _itemsSource.Add(row);' in analysis and analysis.count('if (_activeAnalysisVersion != _analysisVersion) return;') >= 2)
check('cannot print/export during calculation', 'private void PrintDevexpress(int type)\n        {\n            if (_analysisRunning) return;' in analysis and 'private void btnExport_Click(object sender, RoutedEventArgs e)\n        {\n            if (_analysisRunning) return;' in analysis)

purchase = read('frmRptInvPurchaseDetails.xaml.cs'); ET.fromstring(read('frmRptInvPurchaseDetails.xaml'))
view = part(purchase, 'private void btnView_Click(', 'private void ShowInvoice()')
check('purchase branch guard clears old result first', ordered(view, 'InvalidateBranchResults();', 'chkAllBranches.IsChecked == true', 'return;', 'CollectQueryParams(branchId)'))
check('restricted session requires matching positive branch', '(MainClass.BranchNo <= 0 || branchId != MainClass.BranchNo)' in view)
check('purchase single branch uses validated integer', 'whereClause += $"inv.branch={branchId} and ";' in purchase)
check('purchase branch change invalidates in-flight result', 'SelectionChanged="cmbBranches_SelectionChanged"' in read('frmRptInvPurchaseDetails.xaml') and 'requestBranchVersion != _branchFilterVersion' in view and 'if (IsLoaded) InvalidateBranchResults();' in purchase)
check('legacy external SQL API remains outside screen guard', 'BindingListOfInvoices1Async(p, sqlstr, withItems)' in purchase)

# Independent illustrative SQLite dataset: selecting a line category cannot use
# the whole invoice header as that category's revenue.
db=sqlite3.connect(':memory:')
db.executescript('CREATE TABLE inv(id INT, branch INT, net REAL); CREATE TABLE line(inv INT, category INT, value REAL); INSERT INTO inv VALUES (1,1,100),(2,2,80); INSERT INTO line VALUES (1,1,25),(1,2,75),(2,1,80);')
header=db.execute('SELECT SUM(net) FROM inv WHERE id IN (SELECT inv FROM line WHERE category=1)').fetchone()[0]
lines=db.execute('SELECT SUM(value) FROM line WHERE category=1').fetchone()[0]
check('mixed category demonstrates whole-header mismatch', header==180 and lines==105 and header!=lines)
check('single branch model preserves scope', db.execute('SELECT SUM(net) FROM inv WHERE branch=?',(1,)).fetchone()[0]==100)
for all_groups,mode,allowed in [(False,'cust',False),(False,'stock',False),(False,'item',True),(False,'group',True),(True,'cust',True)]:
    check('analysis guard model '+str((all_groups,mode)), (all_groups or mode in ('item','group'))==allowed)
for all_branches,selected,restricted,current,allowed in [(True,1,False,1,False),(False,None,False,1,False),(False,1,True,1,True),(False,2,True,1,False),(False,2,False,1,True),(False,1,True,-1,False)]:
    ok=not all_branches and selected is not None and selected>0 and (not restricted or (current>0 and selected==current))
    check('purchase scope model '+str((all_branches,selected,restricted,current)), ok==allowed)
print(f'RESULT: PASS — {N} source/model checks; not CLR, WPF, SQL Server, accounting or ERP acceptance.')
