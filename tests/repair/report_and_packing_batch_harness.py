#!/usr/bin/env python3
"""Source contracts and small models for R-104..108, not ERP execution."""
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
def read(path):
    return (ROOT / path).read_text(encoding='utf-8-sig')
def section(text, a, b):
    return text[text.index(a):text.index(b, text.index(a))]
def clean(s):
    return re.sub(r'//[^\n]*|/\*.*?\*/', '', s, flags=re.S)
checks = 0
def check(name, result):
    global checks
    checks += 1
    if not result: raise AssertionError(name)
    print('PASS', name)

analysis = read('SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs')
summary = read('SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs')
items = read('SmartAuditERP/Form_WPF/frmEditItems.xaml.cs')
category = read('SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs')
reserved = read('SmartAuditERP/Form_WPF/FrmReseved.xaml.cs')
ops = read('SmartAuditERP/Class/EntityOperations.cs')
stock = clean(section(analysis, 'private void ShowResultStock()', '#endregion'))
cat = clean(section(category, 'private void LoadDgv()', 'private double SafeDouble('))
btn = clean(section(reserved, 'private void BtnAll_Click(', 'private void btnNew_Click('))
def stock_contract(s):
    return ('GetSelectedValue(cmbSafe)' in s and 'if (!allSafe) filter += $"[stock]={safeVal} and ";' in s
            and 'filter += $"[safe]={dt.Rows[i]["id"]} and ";' in s
            and 'GetSelectedValue(cmbStock)' in s)
def net_contract(s):
    return '(ISNULL(Payment, 0) + ISNULL(VAT, 0)) AS DgvNet' in clean(s)
def packing_contract(s):
    s = clean(s)
    return (bool(re.search(r'itemProperty == 2\s*&&\s*\(!double.TryParse\(txtFillVal.Text, out fillVal\) \|\| fillVal == 0\)', s))
            and 'item.PackingValue = fillVal;' in s)
def category_contract(s):
    s = clean(s)
    for checkbox, combo, ident in [('CheckBoxgroup','cmbCategry','categoryId'),('Che_user','cmbUser','userId'),('chk_branch','cmbBranch','branchId'),('chkSalesman','cmbSalesman','salesmanId')]:
        if not re.search(r'%s.IsChecked != true\s*&&\s*\(%s.SelectedIndex < 0 \|\| !int.TryParse\(Convert.ToString\(%s.SelectedValue\), out %s\)\)' % (checkbox, combo, combo, ident), s): return False
    return all(x in s for x in ('AND CategoryId={categoryId}', 'AND Items.group_id={categoryId}',
                                  'AND inv.sales_emp={userId}', 'AND inv.branch={branchId}', 'AND inv.salesman={salesmanId}'))
def button_contract(s):
    s = clean(s)
    return 'CLR();' not in s and s.index('_loaded = true;') < s.index('LoadEmpData(cond);')

check('safe and warehouse selections flow to separate fields', stock_contract(stock))
check('mutant wrong safe ID detected', not stock_contract(stock.replace('[stock]={safeVal}', '[stock]={stockSelVal}')))
check('net normalizes both inputs before addition', net_contract(summary))
check('mutant old NULL propagation detected', not net_contract(summary.replace('ISNULL(Payment, 0) + ISNULL(VAT, 0)', 'Payment + VAT')))
check('displayed components normalize NULL', all('row["%s"] != DBNull.Value' % x in summary for x in ('Payment', 'VAT')))
check('validated packing value is saved', packing_contract(items))
check('old property-code-as-value mutant detected', not packing_contract(items.replace('item.PackingValue = fillVal;', 'item.PackingValue = 2.0;')))
check('writer binds packing value to FillValue', 'Parameters.Add("@FillValue", SqlDbType.Float).Value = Product.PackingValue;' in ops)
check('four scopes validate IDs and include filters', category_contract(cat))
check('old first-row exclusion detected', not category_contract(cat.replace('cmbUser.SelectedIndex < 0', 'cmbUser.SelectedIndex <= 0')))
check('missing salesman guard detected', not category_contract(cat.replace('cmbSalesman.SelectedIndex < 0', 'cmbSalesman.SelectedIndex > 0')))
check('stale results cleared before validation', cat.index('CategoryList.Clear();') < cat.index('int categoryId') < cat.index('var catAdapter'))
catch = cat[cat.index('catch (Exception ex)'):]
check('query failure removes partial result and summaries', 'CategoryList.Clear();' in catch and 'lblTotNet.Text = string.Empty;' in catch)
check('refresh keeps period and identity', button_contract(btn))
check('saved document refresh is rejected before replacing rows',
      btn.index('string.IsNullOrWhiteSpace(txtEntryGlobalId.Text)') < btn.index('return;') < btn.index('LoadEmpData(cond);')
      and 'string.IsNullOrWhiteSpace(TxtGlobalID.Text)' in btn)
check('old reset regression detected', not button_contract(btn.replace('_loaded = true;', '_loaded = true; CLR();')))
check('new command still initializes form', 'CLR();' in clean(section(reserved, 'private void btnNew_Click(', 'private void btnClose_Click(')))
check('employee loader still reads selected period', 'GetSelectedMonth()' in section(reserved, 'public void LoadEmpData(', '#endregion'))

con = sqlite3.connect(':memory:')
con.execute('create table invoice(stock integer, safe integer)')
con.executemany('insert into invoice values (?, ?)', [(7,3),(3,3),(7,4)])
check('different treasury 7 and warehouse 3 select only intended row', con.execute('select * from invoice where stock=? and safe=?',(7,3)).fetchall() == [(7,3)])
check('old warehouse-as-treasury selects different row', con.execute('select * from invoice where stock=? and safe=?',(3,3)).fetchall() == [(3,3)])
for p,v,want in [(100,None,100),(None,15,15),(100,15,115),(None,None,0)]:
    got=con.execute('select coalesce(?,0)+coalesce(?,0)',(p,v)).fetchone()[0]
    check('display-derived net %r %r' % (p,v), got == want)
for val in (12,24,-3):
    check('packing model retains nonzero %s' % val, float(val) != 0 and float(val) == val)
check('packing model rejects zero', float('0') == 0)
for all_checked,index,valid,expected in [(False,0,True,True),(False,-1,False,False),(False,0,False,False),(True,-1,False,True)]:
    check('scope selection model %r' % ((all_checked,index,valid),), (all_checked or (index >= 0 and valid)) == expected)
print('RESULT: PASS — %d checks; source witnesses and illustrative models, not WPF, SQL Server or ERP acceptance.' % checks)
