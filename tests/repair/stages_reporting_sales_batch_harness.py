#!/usr/bin/env python3
"""Source contracts and independent models; not C#, SQL, WPF, or ERP tests."""
from pathlib import Path
from datetime import datetime, timedelta
from decimal import Decimal
R = Path(__file__).resolve().parents[2] / 'SmartAuditERP/Form_WPF'
def read(name): return (R / name).read_text(encoding='utf-8-sig')
def part(s, start, end): return s[s.index(start):s.index(end, s.index(start))]
def check(name, value):
    if not value: raise AssertionError(name)
    print('PASS', name)
def ordered(s, values):
    cursor = -1
    for value in values:
        cursor = s.find(value, cursor + 1)
        if cursor < 0: return False
    return True

stages = part(read('frmProjectStagesPM.xaml.cs'), 'private void btnSave_Click(', '#region Helpers')
def tx_contract(s):
    return (ordered(s, ['BeginTransaction()', 'DELETE FROM PM_GroupStages', 'INSERT INTO PM_GroupStages', 'tx.Commit();', 'committed = true;', 'IsDone = true;', 'savedMsg.ShowDialog()'])
            and s.count('_conn, tx)') == 2 and 'tx.Rollback()' in s and 'string errMsg = committed' in s and '@GroupCode' in s)
check('delete and inserts share a transaction and UI follows commit', tx_contract(stages))
check('missing transaction binding mutant rejected', not tx_contract(stages.replace('_conn, tx)', '_conn)', 1)))
def replace_model(original, replacement, fail_at=None):
    working = []
    for idx, value in enumerate(replacement):
        if idx == fail_at: return original[:]
        working.append(value)
    return working
check('failed second insert leaves original model', replace_model([1, 2], [3, 4], 1) == [1, 2])
check('successful and empty replacements model existing policy', replace_model([1], [2, 3]) == [2, 3] and replace_model([1], []) == [])

produced = part(read('frmRptProducedItems.xaml.cs'), 'private void LoadComponents(', '#endregion')
writer = read('frmProductionOrder.xaml.cs')
check('component reader aliases and groups writer item identity', 'SELECT inv_sub.ItemId AS ComponentId' in produced and 'GROUP BY inv_sub.ItemId' in produced and 'row["ComponentId"]' in produced and 'ProductId' in writer and 'ItemId' in writer)
check('obsolete group by component alias absent', 'GROUP BY ComponentId' not in produced)

sales = part(read('frmRptSalesInPeriod.xaml.cs'), 'private void CalcStock()', 'private (double qty, double total) GetSaleData')
check('return-only guard and net signs', 'qty == 0.0 && retQty == 0.0' in sales and 'qty - retQty' in sales and 'total - retTot' in sales)
for q, ret, expected in [(0, 2, -2), (5, 2, 3), (2, 2, 0)]:
    check('return model '+str((q,ret)), not (q == 0 and ret == 0) and q-ret == expected)

invoice = read('frmSalesInvoice.xaml.cs'); batch = part(invoice, 'private void AddNewItem()', '#endregion')
lookup = part(invoice, 'private void SearchByID(', 'private void AddNewItem()')
barcode = part(invoice, 'private void ReadBarcode()', 'private void SearchByName()')
check('batch retains initial edit target and appends subsequent selections', ordered(batch, ['bool firstSelection = true;', 'foreach (int id in frm.Itemlist)', 'if (!firstSelection ||', 'RowIndex = _itemsSource.Count;', 'SearchByID(0);', 'firstSelection = false;']))
check('search guards negative row and empty barcode appends', 'RowIndex >= 0 && RowIndex < _itemsSource.Count' in lookup and ordered(barcode, ['if (string.IsNullOrEmpty(barcode))', 'RowIndex = _itemsSource.Count;', 'AddNewItem();']))
def batch_model(initial, row_index, selections):
    rows = initial[:]
    for n, item in enumerate(selections):
        if n or row_index < 0 or row_index > len(rows): row_index = len(rows)
        if row_index < len(rows): rows.pop(row_index)
        rows.append(item); row_index = len(rows)-1
    return rows
check('append multiple unique items', batch_model(['old'], 1, ['a','b','c']) == ['old','a','b','c'])
check('edit first item only then append', batch_model(['old','edit'], 1, ['a','b']) == ['old','a','b'])

analysis = read('frmRptInvAnalysis.xaml.cs'); cost = part(analysis, 'private double CalcUnitCost(', 'private void AddRowToGrid(')
check('both cost divisors retain fractional aggregate quantities', cost.count('double totalQty = 0.0;') == 2 and cost.count('totalQty += q;') == 4 and '(int)Math.Round(q)' not in cost)
check('fractional example divisor does not vanish', Decimal('12') / Decimal('0.4') == 30)
month = part(analysis, 'private void ShowResultMonth()', '#region ShowResultDay')
def month_contract(s):
    return ('GetDateFrom().Date' in s and 'GetDateTo().Date' in s and 'dateTo == DateTime.MaxValue.Date' in s and 'dateFrom > dateTo' in s and s.count('date<@date2') == 2 and 'date<=@date2' not in s and s.count('.Value = rangeStart;') == 3 and s.count('.Value = rangeEndExclusive;') == 3 and 'monthStart > dateFrom ? monthStart : dateFrom' in s and 'nextMonth < requestedEndExclusive' in s)
check('month discovery and three queries use clipped half-open intervals', month_contract(month))
check('inclusive end mutant rejected', not month_contract(month.replace('date<@date2', 'date<=@date2', 1)))
def interval(month_start, next_month, start, end): return max(month_start,start), min(next_month,end+timedelta(days=1))
d = lambda x: datetime.fromisoformat(x)
a,b=interval(d('2024-02-01'),d('2024-03-01'),d('2024-02-15'),d('2024-03-05'))
check('partial leap month clipped at both boundaries', (a,b)==(d('2024-02-15'),d('2024-03-01')))
a,b=interval(d('2024-03-01'),d('2024-04-01'),d('2024-02-15'),d('2024-03-05'))
check('end day inclusive but following midnight excluded', a==d('2024-03-01') and d('2024-03-05T23:59:59') < b and not d('2024-03-06') < b)

level = part(read('frmMezanMorg3a.xaml.cs'), 'private void FilterByLevel(', 'private void UpdateRowCount(')
check('level filter expands bounded visited frontiers', all(v in level for v in ['new HashSet<int>()', 'level < maxLevel', 'frontier.Contains(node.TrParentAcc)', 'visibleCodes.Add(node.TrAccount)', 'frontier = next;']))
def visible(nodes, depth):
    found = {n for n,p in nodes if p == 0}; frontier = set(found)
    for _ in range(depth):
        frontier = {n for n,p in nodes if p in frontier and n not in found}; found |= frontier
    return found
nodes=[(1,0),(2,1),(3,2),(4,3),(5,6),(6,5)]
check('root, child, grandchild levels and disconnected cycle', [visible(nodes,d) for d in (0,1,2)] == [{1},{1,2},{1,2,3}])
print('PASS — source contracts and models only; no CLR, SQL, WPF or ERP acceptance.')
