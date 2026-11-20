#!/usr/bin/env python3
"""Source contracts and independent models only; no CLR, WPF or SQL Server."""
from pathlib import Path
from decimal import Decimal as D
from xml.etree import ElementTree as ET
import re

root = Path(__file__).resolve().parents[2] / 'SmartAuditERP'
checks = 0

def read(p):
    return (root / p).read_text(encoding='utf-8-sig')

def check(label, ok):
    global checks
    if not ok:
        raise AssertionError(label)
    checks += 1
    print('PASS', label)

def part(s, a, b):
    return s.split(a, 1)[1].split(b, 1)[0]

editor = read('Form_WPF/FrmReseved.xaml.cs')
report = read('Form_WPF/frmRptReseved.xaml.cs')
open_form = part(report, 'public void LoadDataToGridview(ResevedRow selectedItem)', 'public void PreviewResevd(')
check('report loads after editor loaded/reset on dispatcher', 'editor.Loaded +=' in open_form and 'editor.Dispatcher.BeginInvoke' in open_form and 'editor.OpenSavedDocument(selectedGlobalId)' in open_form)
check('report no longer binds an unrelated DataView', 'GridControl1.ItemsSource' not in open_form and 'detailDt.DefaultView' not in open_form)
check('report remains visible if load fails', open_form.index('if (!editor.OpenSavedDocument') < open_form.index('editor.Close();') < open_form.index('this.Hide();'))
opened = part(editor, 'public bool OpenSavedDocument(string globalId)', 'public void LoadDataToGridview(string entryGlobalId)')
check('header and detail queries parameterized to same id', opened.count('Parameters.Add("@id", SqlDbType.NVarChar).Value = globalId') == 2)
check('reject ambiguous/deleted header and empty details', 'IS_Deleted=0' in opened and 'header.Rows.Count != 1' in opened and 'details.Rows.Count == 0' in opened)
check('complete row snapshot precedes UI publication', opened.index('var rows = new System.Collections.Generic.List<SalaryRow>();') < opened.index('_salarySource.Clear();') and 'foreach (var row in rows) _salarySource.Add(row);' in opened)
check('identity, period, date and stored amount are restored', all(x in opened for x in ('_globalID = savedId', '_entryGlobalID = entryId', 'resNo = documentNo', 'cmbMonth.SelectedIndex = month - 1', 'cmbYear.SelectedItem = year.ToString()', 'txtDate.DateTime = date', 'Net_Sal = Convert.ToDecimal(row["Net"])')))
check('same collection bound to display and save', 'GridControl1.ItemsSource = _salarySource;' in opened and 'foreach (var row in _salarySource)' in editor)
check('loaded document period locked; reset unlocks', 'cmbMonth.IsEnabled = false;' in opened and 'cmbYear.IsEnabled = false;' in opened and 'cmbMonth.IsEnabled = true;' in editor and 'cmbYear.IsEnabled = true;' in editor)
check('payroll null entry safety stop remains', 'Entr == null || Entr.Accounts == null || Entr.Accounts.Count == 0' in read('Class/Reseved.cs'))

resx = ET.parse(root / 'Properties/Resources.resx').getroot()
resources = {x.attrib['name']: x.findtext('value') or '' for x in resx.findall('data')}
names = ['GetSalesByCategory', 'GetSalesByItems', 'GetSalesByOrderType', 'GetSalesByPaymentMethods']
def body(src, verb, name):
    pat = rf'{verb}\s+PROCEDURE \[dbo\]\.\[{name}\].*?\n[ \t]*END(?=\x27\)|\nGO)'
    found = re.findall(pat, src, flags=re.I | re.S)
    if len(found) != 1:
        raise AssertionError((name, verb, len(found)))
    return found[0]

for name in names:
    fresh = body(resources['CrystalLiteDB'], 'CREATE', name)
    create = body(resources['AlterDb'], 'CREATE', name)
    alter = body(resources['AlterDb'], 'ALTER', name)
    check(name + ' upgrade has create and alter bodies', re.sub(r'^CREATE\s+', 'ALTER ', create, count=1, flags=re.I) == alter)
    for mode, text in [('fresh', fresh), ('upgrade-create', create), ('upgrade-alter', alter)]:
        check(name + ' ' + mode + ' filters deleted sales and returns', text.count('inv.IS_Deleted=0') == 2)
        check(name + ' ' + mode + ' sale and return branches retained', 'proc_type=1' in text and 'proc_type=2' in text)
        if name in ('GetSalesByOrderType', 'GetSalesByPaymentMethods'):
            check(name + ' ' + mode + ' applies selected invoice type twice', text.count('(inv_type=@inv_type)') == 2 and '(inv_type=2 or inv_type=3)' not in text)
        if name == 'GetSalesByItems':
            check(name + ' ' + mode + ' uses priced quantity on both branches', text.count('sum(val1*exchange_price)') == 2 and 'sum(val*exchange_price)' not in text)
check('existing POS item aggregate excludes deleted invoices', 'AND inv.IS_Deleted=0' in part(read('Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs'), 'private void ShowResult', 'private DateTime BuildDateTime'))
rows = [(2, False, D(100)), (3, False, D(40)), (2, True, D(99))]
check('chart type and deletion model selected sale', sum(v for typ, deleted, v in rows if typ == 2 and not deleted) == 100)
check('chart type and deletion model selected POS', sum(v for typ, deleted, v in rows if typ == 3 and not deleted) == 40)

expected = {'frmRptSalesInPeriod.xaml.cs': 1, 'frmActsInvTotal.xaml.cs': 1,
            'frmNkdTotSalePurch.xaml.cs': 6, 'frmNkdTotSalePurchActCust.xaml.cs': 4,
            'frmRptItemsActivity.xaml.cs': 2, 'frmRptInvAnalysis.xaml.cs': 4}
for filename, count in expected.items():
    source = read('Form_WPF/' + filename)
    matches = re.findall(r'sum\(val1\s*\*\s*exchange_price\)', source, flags=re.I)
    check(filename + ' priced quantity source witnesses', len(matches) >= count)
check('packaging total model preserves primary qty but prices sale qty', D('2') * D('12') == D('24') and D('2') * D('120') == D('240'))
check('packaging unit cost model converts to base units', D('240') / D('24') == D('10'))

pos = read('Form_WPF/frmItemsalesdetailsPos.xaml.cs')
salesman = read('Form_WPF/frmInvBySalesMen.xaml.cs')
check('POS detail user selection is required and parameterized', 'if (!allUsers)' in pos and 'cmbusers.SelectedValue == null' in pos and 'Inv.sales_emp = @userId' in pos and 'Parameters.Add("@userId", SqlDbType.Int).Value = selectedUser' in pos)
check('POS reads saved flag and never silently infers NULL', 'taxval, Inv.PriceIncVAT' in pos and 'row["PriceIncVAT"] == DBNull.Value' in pos and 'bool priceIncludesVat = Convert.ToBoolean(row["PriceIncVAT"])' in pos)
check('POS failure invalidates rows and displayed sums', '_dataRows.Clear();\n                GridControl1.ItemsSource = null;\n                lblRowCount.Text = "عدد السجلات: 0";\n                CalculateAndShowSummaries();' in pos)
check('salesman uses invoice flag not current settings', 'if (Convert.ToBoolean(row["PriceIncVAT"])) netVal -= taxVal;' in salesman and '_priceIncVAT' not in salesman and 'row["PriceIncVAT"] == DBNull.Value' in salesman)
for inclusive, gross, vat, before, after in [(True, D(115), D(15), D(100), D(115)), (False, D(100), D(15), D(100), D(115))]:
    check('stored tax mode model ' + str(inclusive), (gross-vat if inclusive else gross) == before and (gross if inclusive else gross+vat) == after)

analysis = read('Form_WPF/frmRptInvAnalysis.xaml.cs')
helper = part(analysis, 'private string GetEmployeeFilter()', 'private object GetSelectedValue(')
check('employee filter uses numeric invoice user identity', 'Convert.ToInt32(GetSelectedValue(cmbEmp))' in helper and 'inv.sales_emp={employeeId}' in helper)
for name in ('Group', 'Item', 'Cust', 'Salesman', 'Month', 'Day', 'Stock'):
    section = part(analysis, 'private void ShowResult' + name + '()', '#endregion')
    check(name + ' invoice aggregations share employee filter', 'string employeeFilter = GetEmployeeFilter();' in section and 'string filter = employeeFilter;' in section and ' where " + filter +' in section)
section = part(analysis, 'private void ShowResultGroup()', '#endregion')
check('group dimension uses selected group and matching joined id', '@allGroups=1 OR id=@groupId' in section and 'ItemsCategory.id={dt.Rows[i]["id"]}' in section and 'Items.group_id=ItemsCategory.id' in section)
check('employee dimension filters employees by selected id', 'if (!allEmp)' in part(analysis, 'private void ShowResultEmp()', '#endregion') and 'sales_emp={dt.Rows[i]["id"]}' in part(analysis, 'private void ShowResultEmp()', '#endregion'))
print(f'RESULT: {checks} source/model checks passed; no CLR/WPF/SQL/REPX or accounting acceptance')
