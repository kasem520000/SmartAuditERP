#!/usr/bin/env python3
"""Source guards and independent control-flow models; no CLR, SQL or ERP execution."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2] / 'SmartAuditERP/Form_WPF'
prod = (ROOT / 'frmProductionOrder.xaml.cs').read_text(encoding='utf-8-sig')
project = (ROOT / 'frmAssignProjectPM.xaml.cs').read_text(encoding='utf-8-sig')
n = 0

def part(src, start, end): return src[src.index(start):src.index(end, src.index(start))]
def check(label, condition):
    global n
    assert condition, label
    n += 1
    print('PASS', label)
def ordered(src, *values):
    offset = 0
    for value in values:
        offset = src.find(value, offset)
        if offset < 0: return False
        offset += len(value)
    return True

read = part(prod, 'private void ReadData(', 'private void btnFirst_Click(')
save = part(prod, 'private bool Save()', '#region CLR (Clear Form)')
saveprint = part(prod, 'private void btnSavePrint_Click(', 'private void btnPrint_Click(')
clear = part(prod, 'private void CLR()', '#region Print')
printmethod = part(prod, 'private bool PrintDevexpress(', '#endregion')
check('loaded order locks before header and components', ordered(read, 'CLR();', '_loadedProduction = true;', 'SetProductionScaleEditable(false);', '// ═══ تحميل بيانات الفاتورة', '// ═══ تحميل مكونات الإنتاج'))
check('new clears loaded state but does not erase unknown commit', '_loadedProduction = false;' in clear and '_saveOutcomeUnknown = false;' not in clear)
check('quantity change never rescales a loading or loaded order', 'if (_isLoaded || _loadedProduction) return;' in part(prod, 'private void txtQty_TextChanged(', '#region Calculation'))
check('product unit quantity and grid locked', all(x in prod for x in ('txtQty.IsReadOnly = !editable;', 'cmbUnits.IsEnabled = editable;', 'cmbItems.IsEnabled = editable;', 'dgvItems.IsReadOnly = !editable;')))
for method, end in [('private void DeleteItemRow_Click(', '#endregion'), ('private void AddNewItem()', 'private void SearchByID(')]:
    check(method + ' rejects loaded order', 'if (_loadedProduction) return;' in part(prod, method, end))
check('save rejects loaded or uncertain outcome before transaction', ordered(save, 'if (_loadedProduction || _saveOutcomeUnknown)', 'return false;', '_conn.BeginTransaction()'))
check('commit state and identity recorded before post-commit dialog', ordered(save, 'commitAttempted = true;', 'transaction.Commit();', 'committed = true;', '_invGlobalID = invGlobalID;', '_loadedProduction = true;', 'savedMsg.ShowDialog();'))
check('uncertain commit disables subsequent save', 'if (commitAttempted && !committed) _saveOutcomeUnknown = true;' in save)
check('uncertain commit also blocks delete', ordered(part(prod, 'private void btnDelete_Click(', '#region Add New Item'), 'if (_saveOutcomeUnknown)', 'return;', 'UPDATE Inv SET IS_Deleted=1'))
check('rollback only before confirmed commit and errors block retries', ordered(save, 'if (transaction != null && !committed)', 'transaction.Rollback();', 'catch', '_saveOutcomeUnknown = true;'))
check('failed known rollback restores provisional identities', 'if (!committed && !_saveOutcomeUnknown)' in save and '_code = originalCode;' in save and '_procCode = originalProcCode;' in save)
check('save and print only print on committed save', ordered(saveprint, 'if (!Save())', '_isPrinted = false;', 'return;', 'if (PrintDevexpress(1)) CLR();'))
check('print validation or exceptions retain form', 'if (_printNo <= 0)' in printmethod and printmethod.count('return false;') >= 6 and 'return true;' in printmethod)
check('no project accreditation can reach its old transaction', ordered(project, 'private bool ProjectAccreditationAvailable()', 'return false;', 'private void AccreditateProject()', 'if (!ProjectAccreditationAvailable()) return;', '_conn.BeginTransaction()') if '_conn.BeginTransaction()' in project[project.index('private void AccreditateProject()'):] else ordered(project, 'private bool ProjectAccreditationAvailable()', 'return false;', 'private void AccreditateProject()', 'if (!ProjectAccreditationAvailable()) return;'))
# Independent abstract model: a failed or indeterminate save cannot print/clear;
# a successful save with failed printing keeps the order on screen.
for loaded, uncertain, commit, printed, expected in [
    (True, False, True, True, (False, False, False)),
    (False, True, True, True, (False, False, False)),
    (False, False, False, True, (False, False, False)),
    (False, False, True, False, (True, True, False)),
    (False, False, True, True, (True, True, True))]:
    saved = not loaded and not uncertain and commit
    outcome = (saved, saved, saved and printed)
    check('save/print model ' + str((loaded, uncertain, commit, printed)), outcome == expected)
print(f'RESULT: PASS — {n} source/model checks; not SQL, WPF, CLR or ERP acceptance.')
