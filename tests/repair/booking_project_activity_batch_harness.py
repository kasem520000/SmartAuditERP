#!/usr/bin/env python3
"""Source contracts and small independent models, not CLR, WPF or SQL tests."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2] / 'SmartAuditERP'
N = 0

def read(path): return (ROOT / path).read_text(encoding='utf-8-sig')
def part(s, a, b): return s[s.index(a):s.index(b, s.index(a))]
def check(label, ok):
    global N
    if not ok: raise AssertionError(label)
    N += 1
    print('PASS', label)
def ordered(s, parts):
    cursor = -1
    for p in parts:
        cursor = s.find(p, cursor + 1)
        if cursor < 0: return False
    return True

booking = part(read('Form_WPF/frmBookingM.xaml.cs'), 'private void Save()', '#region Navigation')
check('booking ID obtained inside insert scope', 'SELECT CAST(SCOPE_IDENTITY() AS int)' in booking and 'bookingId = Convert.ToInt32(insertedId)' in booking)
check('insert identity failure stops save', 'insertedId == null || insertedId == DBNull.Value' in booking and 'bookingId = Convert.ToInt32(insertedId)) <= 0' in booking)
check('update identifies booking and invoice and requires one active match', 'where Bid=@BookingId AND InvId=@InvID AND IsDeleted=0' in booking and 'cmd.ExecuteNonQuery() != 1' in booking)
check('replacement is parameterized and uses persisted identity', 'DELETE FROM BookingAddition WHERE bookId=@BookingId' in booking and 'deleteAdditions.Parameters.Add("@BookingId", SqlDbType.Int).Value = bookingId' in booking and '(int)bookNo' not in booking)
check('both booking operations and additions precede transaction commit', ordered(booking, ['conn.BeginTransaction()', 'InsertRentInv', 'SCOPE_IDENTITY()', 'DELETE FROM BookingAddition', 'insert into BookingAddition', 'transaction.Commit()']))
check('addition uses resolved ID', 'insertCmd.Parameters.Add("@bookId", SqlDbType.Int).Value =\n                            bookingId;' in booking)
check('catch attempts rollback without hiding failure', 'try { transaction.Rollback(); }' in booking and 'catch { rollbackFailed = true; }' in booking)
def replace_additions(rows, persisted_id, proposal, addition, fail=False):
    working = {k: v[:] for k, v in rows.items()}
    working[persisted_id] = [addition]
    return rows if fail else working
for saved, proposed in [(12, 2), (105, 8), (1, 1)]:
    old = {saved: ['old'], 999: ['other']}
    result = replace_additions(old, saved, proposed, 'new')
    check('addition identity model '+str((saved,proposed)), result[saved] == ['new'] and result[999] == ['other'] and (saved == proposed or proposed not in result))
    check('rollback model '+str(saved), replace_additions(old, saved, proposed, 'new', True) == old)

cycle = read('Form_WPF/frmProjCyclePM.xaml.cs')
resource = read('Properties/Resources.resx')
check('shipped status codes show 3 in progress and 4 closed', "(3, N'تحت التنفيذ', N'Implementation', 0)" in resource and "(4, N'مغلق', N'Closed', 0)" in resource)
check('project close writes shipped closed code', 'cmd.Parameters.Add("@statusPK", SqlDbType.Int).Value      = 4;' in cycle)
check('file and stage UI closed checks use code 4', cycle.count('Convert.ToInt32(cmbStatus.SelectedValue) == 4') == 3 and 'Convert.ToInt32(cmbStatus.SelectedValue) == 3' not in cycle)
contract = part(cycle, 'private void btnCloseContract_Click(', 'private void btnSearch_Click(')
check('contract closure refuses ambiguous identity', 'غير متاح' in contract and 'UPDATE PM_ContractInv' not in contract)
check('stage reload invalidates prior visible and selected stages', ordered(cycle, ['private void LoadProjectStage(int code)', 'Stageslist.Clear();', 'StageID = -1;', '_filesSource.Clear();', 'button.Visibility = Visibility.Collapsed;', 'var adapter = new SqlDataAdapter(']))
check('deleted project and group stage rows excluded', 'PM_ProjStages.IS_Deleted=0' in cycle and 'PM_GroupStages.IS_Deleted=0' in cycle)
previous = part(cycle, 'private bool CheckPreviousStage()', 'private bool CheckAccreditatedStages()')
check('previous file check requires real project, stage list and bounded UI', '!HasCurrentProject() || Stageslist.Count == 0 || Stageslist.Count > 6' in previous)
check('files checked in stage order through selected stage', ordered(previous, ['foreach (var stage in Stageslist)', 'StageNo=@Stage AND ISNULL(IS_Deleted,0)=0', 'cmd.ExecuteScalar()', 'stageId == StageID', 'return selectedFound;']))
check('stage file check parameterized', 'cmd.Parameters.Add("@Project", SqlDbType.Int).Value = ProjNo' in previous and 'cmd.Parameters.Add("@Stage", SqlDbType.Int).Value = stageId' in previous)
close = part(cycle, 'private bool CheckAccreditatedStages()', 'private void OpenFileForRow(')
check('empty or too many stages block project closure', 'Stageslist.Count == 0 || Stageslist.Count > 6' in close)
check('persisted count and null approval checked on close', 'ISNULL(IsAccredit,0)=0' in close and 'count != Stageslist.Count || unapproved != 0' in close)
accredit = part(cycle, 'private void btnAccreditateStage_Click(', 'private void btnCloseProject_Click(')
check('stage approval demands one active unapproved identity', 'AND IS_Deleted=0 AND ISNULL(IsAccredit,0)=0' in accredit and 'AND StageId=@Stage AND IS_Deleted=0)=1' in accredit and 'cmd.ExecuteNonQuery() != 1' in accredit)
plan = part(read('Form_WPF/frmProjectStagesPM.xaml.cs'), 'private void btnSave_Click(', '#region Helpers')
check('stage limit before transaction', ordered(plan, ['_grpStagesSource.Count > 6', 'return;', 'BeginTransaction()']))
for n, persisted, unapproved, expected in [(0,0,0,False),(1,1,0,True),(1,1,1,False),(6,6,0,True),(7,7,0,False),(2,1,0,False)]:
    check('close count model '+str((n,persisted,unapproved)), (0 < n <= 6 and n == persisted and unapproved == 0) == expected)
for available, selected, expected in [([True,True,True],1,True),([False,True],1,False),([True,False],1,False),([True],3,False),([],0,False)]:
    result = 0 <= selected < len(available) and len(available) <= 6 and all(available[:selected+1])
    check('stage file model '+str((available,selected)), result == expected)

activity = read('Form_WPF/frmRptItemsActivity.xaml.cs')
xaml = read('Form_WPF/frmRptItemsActivity.xaml')
ET.fromstring(xaml)
client = part(xaml, '<ComboBox x:Name="cmbClients"', '</StackPanel>')
check('client lookup contains no static items', '<ComboBoxItem>' not in client)
calc = part(activity, 'public void CalcStock()', '// ─── Helper: جلب مجموع val')
check('report refuses unsupported party filter before querying', ordered(calc, ['ClearActivityResults();', 'chkAllClients.IsChecked != true', 'return;', 'string itemsSql']))
check('calculation prevents reentrancy and releases flag', 'if (_calculatingActivity) return;' in calc and 'finally { _calculatingActivity = false; }' in calc)
check('party change during dispatcher invalidates partial calculation', 'partyVersion != _partyFilterVersion' in calc and ordered(calc, ['new Action(() => { }));', 'partyVersion != _partyFilterVersion', 'ClearActivityResults();', 'return;']))
check('each party radio invalidates result and increments generation', activity.count('_partyFilterVersion++;') == 3 and activity.count('ClearActivityResults();') >= 6)
lookup = part(activity, 'private void LoadClients(short clientType)', '#endregion')
check('lookup clears stale data before query and binds empty tables', ordered(lookup, ['cmbClients.ItemsSource = null;', 'adapter.Fill(dt);', 'cmbClients.ItemsSource       = dt.DefaultView;']) and 'if (dt.Rows.Count > 0)' not in lookup)
check('print and export reject partial calculations', 'private void PrintDevexpress(int printMode)\n        {\n            if (_calculatingActivity) return;' in activity and 'private void ExportToExcel()\n        {\n            if (_calculatingActivity) return;' in activity)
print(f'RESULT: PASS — {N} source/model checks; not SQL, WPF, CLR or ERP acceptance.')
