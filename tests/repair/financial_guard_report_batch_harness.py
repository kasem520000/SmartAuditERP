#!/usr/bin/env python3
"""Source contracts and small arithmetic models; not CLR, WPF, or SQL execution."""
from pathlib import Path
from decimal import Decimal as D

root = Path(__file__).resolve().parents[2] / 'SmartAuditERP'
count = 0

def read(path):
    return (root / path).read_text(encoding='utf-8-sig')

def check(name, condition):
    global count
    if not condition:
        raise AssertionError(name)
    count += 1
    print('PASS', name)

def block(text, start, end):
    return text.split(start, 1)[1].split(end, 1)[0]

pay = read('Class/Reseved.cs')
save = block(pay, 'public bool SaveReceipt1(', 'public Entry BindreservedToEntry(')
check('payroll missing or empty entry rejected before connection and writes',
      save.index('Entr == null || Entr.Accounts == null || Entr.Accounts.Count == 0') < save.index('MainClass.ConnObj()') < save.index('insert into Salary_Res'))
check('payroll rejection returns false', 'return false;' in save[:save.index('MainClass.ConnObj()')])
ui = read('Form_WPF/FrmReseved.xaml.cs')
saveui = block(ui, 'private void btnSave_Click(', 'private void btnPrint_Click(')
check('payroll error stops success dialog', saveui.index('if (!reseved.SaveReceipt1(') < saveui.index('return;', saveui.index('if (!reseved.SaveReceipt1(')) < saveui.index('var savedMsg'))
check('payroll contract mismatch not misrepresented as fixed', 'dataRow = (DataRow)dt[i]' in pay and 'foreach (SalaryRow row in selectedRows)' in saveui)

sale = read('Form_WPF/frmSalesInvoice.xaml.cs')
preview = block(sale, 'private void btnView_Click(', 'private void btnClose_Click(')
printing = block(sale, 'private void btnPrint_Click(', 'private void btnView_Click(')
saving = block(sale, 'private async void SaveAndPrint(', 'private Invoice BindToInvoice(')
binding = block(sale, 'private Invoice BindToInvoice(', 'private void RptPrint(')
check('preview and print bind without persistence flag', 'BindToInvoice()' in preview and 'BindToInvoice()' in printing)
check('only save requests serial persistence', sale.count('BindToInvoice(persistSerials: true)') == 1 and 'BindToInvoice(persistSerials: true)' in saving)
check('serial delete and writes gated', binding.index('if (persistSerials && dtSerialNo.Rows.Count > 0)') < binding.index('DELETE FROM ItemSerialNo') < binding.index('SaveSerialNo('))
check('default binding is non-persistent', 'BindToInvoice(bool persistSerials = false)' in sale)
check('existing save is not falsely claimed atomic', 'catch { }' in binding[binding.index('// Serial numbers'):])

tax = read('Form_WPF/frmTaxRptPeriod.xaml.cs')
check('rental return netted before tax base', tax.index('rentNet -= SafeDouble') < tax.index('double rentBase = rentNet - rentVAT;'))
check('rental row and base use same exclusive amount', 'SetCellText(txtIncomes, rentBase.ToString())' in tax and 'netSaleVal + salesOutTaxVal + receiptTotal + rentBase' in tax)
check('tax remains separately included', 'taxNetSaleVal + receiptVAT + rentVAT' in tax and 'SetCellText(txtIncomesVAT, rentVAT.ToString())' in tax)
for gross, vat, expected in [('115', '15', '100'), ('-23', '-3', '-20'), ('0', '0', '0')]:
    check('rental inclusive less tax ' + gross, D(gross) - D(vat) == D(expected))

category = read('Form_WPF/frmRptSalesByCategory.xaml.cs')
check('quantity applied in both category branches', category.count('SUM(ROUND((val1 * ItemPriceWithoutVAT * minus / ') == 2)
for qty, unit, discount, invsum, expected in [('3','10','8','40','6'), ('0.5','20','10','100','1')]:
    check('allocation quantity model ' + qty, D(qty) * D(unit) * D(discount) / D(invsum) == D(expected))

analysis = read('Form_WPF/frmRptInvAnalysis.xaml.cs')
check('last cost fold removed', 'totalQtyForCost * lastUnitCost' not in analysis and 'lastUnitCost = CalcUnitCost' not in analysis)
check('item path accumulates dated row cost', analysis.count('netCost += Math.Round(rowQty * unitCost, 4);') >= 7)
pairs = [(D('1'),D('10')), (D('3'),D('20'))]
check('dated cost order independence model', sum(q*c for q,c in pairs) == D('70') == sum(q*c for q,c in reversed(pairs)))

profit = read('Form_WPF/frmInvsProfit.xaml.cs')
show = block(profit, 'public void ShowInvs(', 'private static double GetDouble(')
where = block(profit, 'private string BuildWhereClause(', '#endregion')
check('stored profit filter removed', 'inv.Invprofit' not in where)
check('profit filter uses same computed value before adding row', show.index('double profit = invTotal - _invAvrgCost;') < show.index('rbNegativeProfit.IsChecked == true && profit >= 0') < show.index('resultTable.Rows.Add('))
check('filter covers positive, negative and zero with skip progress', all(x in show for x in ['rbPositiveProfit.IsChecked == true && profit <= 0','rbZeroProfit.IsChecked == true && profit != 0','ProgressBar1.Value++']))
for amount, kind in [(D('40'), 'positive'), (D('-20'), 'negative'), (D('0'), 'zero')]:
    matches = {'positive': amount > 0, 'negative': amount < 0, 'zero': amount == 0}
    check('profit membership ' + kind, matches[kind] and sum(matches.values()) == 1)
print(f'{count} source/model checks passed; no CLR, SQL, WPF or accounting acceptance')
