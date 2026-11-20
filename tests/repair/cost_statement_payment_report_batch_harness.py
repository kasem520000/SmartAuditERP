#!/usr/bin/env python3
"""Witnesses and illustrative models only: not SQL Server, C#, WPF or ERP acceptance."""
from pathlib import Path
import sqlite3
import xml.etree.ElementTree as ET
R = Path(__file__).resolve().parents[2]
F = R / 'SmartAuditERP' / 'Form_WPF'
checks = 0
def read(n): return (F/n).read_text(encoding='utf-8-sig', errors='replace')
def part(s,a,b): return s[s.index(a):s.index(b,s.index(a))]
def check(label, ok):
    global checks
    assert ok, label
    checks += 1
    print('PASS', label)

def membership_contract(s):
    return all(x in s for x in ['_parentCode = -1;', 'int.TryParse(Convert.ToString(cmbCostCenter.SelectedValue)', 'new HashSet<int>()', 'while (visited.Add(current))', 'code=@code AND Is_Deleted=0', 'dt.Rows.Count != 1', 'if (current == selected)', '_parentCode = selected;', 'ParentCode"] == DBNull.Value']) and 'GetParent(' not in s[s.index('{'):]
cost = read('frmRptCostCenter.xaml.cs')
parent=part(cost,'private void GetParent(int code)','        #endregion')
check('membership follows validated, cycle-bounded ancestor chain',membership_contract(parent))
check('cycle detection mutant fails',not membership_contract(parent.replace('while (visited.Add(current))','while (true)')))
check('ambiguous-code mutant fails',not membership_contract(parent.replace('dt.Rows.Count != 1','dt.Rows.Count == 0')))
check('both result modes use membership check',cost.count('GetParent(Convert.ToInt32(row["CCcode"]));')==2)

def member(nodes, selected, start):
    seen=set(); current=start
    while current not in seen:
        seen.add(current)
        candidates=nodes.get(current,[])
        if len(candidates)!=1: return False
        if current==selected:return True
        current=candidates[0]
        if current is None:return False
    return False
nodes={1:[None],2:[1],3:[2],4:[None],5:[6],6:[5],7:[9,1],8:[99]}
for selected,start,want in [(1,1,True),(1,2,True),(1,3,True),(2,3,True),(2,1,False),(1,4,False),(1,5,False),(1,7,False),(1,8,False),(99,8,False)]:
    check('ancestor membership '+str((selected,start)),member(nodes,selected,start)==want)

agg=part(cost,'private void ShowResult()','private void ProcessAndAddRow(')
def opening_contract(s):
    return (s.count('Accounts_Index.Code AS AccCode')==2 and s.count('GROUP BY Entry_sub.CCcode, Accounts_Index.Code, Accounts_Index.Aname, cost_center.name')==2 and 'initRow["AccCode"].ToString() == row["AccCode"].ToString()' in s)
check('aggregate opening matches center and account identity',opening_contract(agg))
check('account omission mutant rejected',not opening_contract(agg.replace('initRow["AccCode"].ToString() == row["AccCode"].ToString()','true')))
db=sqlite3.connect(':memory:')
db.executescript('create table opening(cc int, acc int, amount int); create table movement(cc int, acc int, amount int);')
db.executemany('insert into opening values(?,?,?)',[(1,10,100),(1,20,200),(1,30,300),(2,10,400)])
db.executemany('insert into movement values(?,?,?)',[(1,10,7),(1,20,9),(2,10,8)])
rows=db.execute('select m.cc,m.acc,coalesce(o.amount,0) from movement m left join opening o on o.cc=m.cc and o.acc=m.acc order by m.cc,m.acc').fetchall()
check('model: two accounts in same center retain their own opening',rows==[(1,10,100),(1,20,200),(2,10,400)])
check('model: opening-only account is not in legacy movement driven result',all(r[1]!=30 for r in rows))

res=ET.parse(R/'SmartAuditERP/Properties/Resources.resx').getroot()
values={d.get('name'):d.findtext('value') or '' for d in res.findall('data')}
for name in ('CrystalLiteDB','AlterDb'):
    value=values[name]; start=value.index('Create PROCEDURE [dbo].[GetAccountStatement]'); query=value[start:]
    previous=part(query,'PreviousBalance AS (','MainStatement AS (')
    main=part(query,'MainStatement AS (','-- Combine the previous balance')
    check(name+' prior balance filters active and non-deleted', 'AND e.state = 1' in previous and 'AND e.is_Deleted = 0' in previous)
    check(name+' current statement filters active and non-deleted', 'AND e.state = 1' in main and 'AND e.is_Deleted = 0' in main)
    check(name+' removed-state mutant detected', 'AND e.state = 1' not in main.replace('AND e.state = 1',''))
check('inserted state comments do not break dynamic SQL quoting', "statement's active entries" not in values['AlterDb'] and values['AlterDb'].count('-- Match active entries in the detailed statement') == 2)
# Scan the outer SQL string: doubled quotes belong to the embedded procedure.
dynamic = values['AlterDb']
start = dynamic.index("EXEC('Create PROCEDURE [dbo].[GetAccountStatement]") + len("EXEC('")
idx = start
while idx < len(dynamic):
    if dynamic[idx] == "'":
        if idx + 1 < len(dynamic) and dynamic[idx + 1] == "'":
            idx += 2
            continue
        break
    idx += 1
check('dynamic procedure SQL string closes after the complete body',
      dynamic[start:idx].rstrip().endswith('END;') and dynamic[idx:idx+2] == "')" and dynamic[start:idx].count('AND e.state = 1') == 2)
check('existing upgrade procedure remains conditional, no forced ALTER', "OBJECT_ID('dbo.GetAccountStatement')" in values['AlterDb'] and 'ALTER PROCEDURE [dbo].[GetAccountStatement]' not in values['AlterDb'])
db.execute('create table entry(state int, deleted int, amount int)')
db.executemany('insert into entry values(?,?,?)', [(1,0,10),(0,0,50),(1,1,90),(None,0,100)])
check('active and non-deleted example excludes cancelled, deleted and null state',db.execute('select sum(amount) from entry where state=1 and deleted=0').fetchone()[0]==10)

sales=read('frmRptInvSalesDetails.xaml.cs')
avail=part(sales,'private bool PaymentChangeAvailable()','// ── تحويل إلى نقدي')
check('payment change helper explicitly denies and warns', 'return false;' in avail and 'DXMessageBox.Show' in avail)
for name in ('ToolMenuCash_Click','ToolMenuCredit_Click','ToolMenuVisa_Click'):
    block=part(sales,'private void '+name, '\n        }')
    check(name+' rejects before selected rows and SQL',block.index('if (!PaymentChangeAvailable()) return;')<block.index('GetSelectedItems()'))
    check(name+' guard removal mutant rejected','if (!PaymentChangeAvailable()) return;' not in block.replace('if (!PaymentChangeAvailable()) return;',''))
category=read('frmRptSalesByCategory.xaml.cs')
printmethod=part(category,'private void PrintReport(int printMode)','public DataSet BuildReportDataSet()')
check('category print and preview reject before template output',printmethod.index('if (!CategoryPrintAvailable()) return;')<printmethod.index('XtraReport.FromFile'))
check('print denial is explicit', 'return false;' in part(category,'private bool CategoryPrintAvailable()','private void PrintReport('))
check('show and export warn about fixed-rate tax', 'WarnEstimatedCategoryTax();' in part(category,'private void btnShow_Click','private void btnClose_Click') and 'WarnEstimatedCategoryTax();' in part(category,'private void btnExportExcel_Click','#endregion'))
check('warning states fixed 15 percent and non-use for tax settlement', '15%' in part(category,'private void WarnEstimatedCategoryTax()','private void btnClose_Click') and 'للتسوية الضريبية' in category)

names=[('frmSalesInvoice.xaml.cs','SearchByNameClient','adapter'),('frmSalePurch.xaml.cs','SrchByNameClient','adapter'),('frmPurchInv.xaml.cs','SrchByNameClint','adp')]
for file,client,adp in names:
    text=read(file)
    for method,param in [('SearchByName','@name'),('SearchByCode','@code'),(client,'@name')]:
        section=part(text,'private void '+method+'()', '\n        }')
        check(file+' '+method+' binds '+param, param in section and 'Parameters.Add("'+param+'", SqlDbType.NVarChar, -1)' in section and section.index('Parameters.Add("'+param+'"')<section.index('.Fill('))
    section=part(text,'private void ReadBarcode()', '\n        }')
    check(file+' binds both barcode queries', section.count('Parameters.Add("@barcode", SqlDbType.NVarChar, -1)')==2 and 'barcode=@barcode' in section and "barcode=N'{barcode}'" not in section and 'barcode + "\'' not in section)
    check(file+' barcode binding mutant detected',section.replace('Parameters.Add("@barcode", SqlDbType.NVarChar, -1)','Parameters.Add("@other", SqlDbType.NVarChar, -1)',1).count('Parameters.Add("@barcode", SqlDbType.NVarChar, -1)')!=2)
db.execute('create table items(code text)')
for x in ["O'Brien", 'x', "x' OR 1=1 --", 'صنف عربي']: db.execute('insert into items values(?)',(x,))
for x in ["O'Brien", "x' OR 1=1 --", 'صنف عربي', 'missing']:
    got=db.execute('select code from items where code=?',(x,)).fetchall()
    check('parameter lookup model '+x, got==([(x,)] if x!='missing' else []))
print('RESULT: PASS — %d source/model checks; no CLR, WPF, SQL Server or ERP acceptance.' % checks)
