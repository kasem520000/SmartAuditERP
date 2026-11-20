#!/usr/bin/env python3
"""R-109..112: source witnesses, mutations and illustrative models, not ERP."""
from pathlib import Path
import calendar
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
def read(name): return (ROOT / name).read_text(encoding='utf-8-sig')
def part(s, a, b):
    i=s.index(a); return s[i:s.index(b,i)]
def clean(s): return re.sub(r'//[^\n]*|/\*.*?\*/','',s,flags=re.S)
count=0
def check(label, ok):
    global count
    count+=1
    if not ok: raise AssertionError(label)
    print('PASS', label)

res=read('SmartAuditERP/Form_WPF/FrmReseved.xaml.cs')
tax=read('SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs')
writer=read('SmartAuditERP/Class/InvoiceOper.cs')
activity=read('SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs')
parent=read('SmartAuditERP/Form_WPF/frmInvInOutput.xaml.cs')
xaml=read('SmartAuditERP/Form_WPF/frmInvInOutput.xaml')
refresh=clean(part(res,'private void RefreshSelectedPeriod(', '#endregion'))
load=clean(part(res,'public void LoadEmpData(', '#endregion'))
save=clean(part(res,'private void btnSave_Click(', 'private void btnDelete_Click('))
printing=clean(part(res,'private void RptPrint(', 'private DataSet BindToData('))
reset=clean(part(res,'private void CLR()', '#endregion'))
last=clean(part(activity,'public void LastProcess(', '#endregion'))
show=clean(part(activity,'public void ShowResult()', '/// <summary>'))
lookup=clean(part(activity,'private void loadclients(', 'private string GetsafeName('))
party=clean(part(parent,'private void StripLastItem_Click(', 'private void StripItemAvrgCost_Click('))
general=clean(part(parent,'private void StripClientLastItem_Click(', 'private void StripLastItem_Click('))
projection=clean(part(tax,'public List<InvoiceTxt> BindingListOfInvoices1(', 'private void UpdateSummaries(')) if 'private void UpdateSummaries(' in tax else clean(tax)

def period_contract(r,l,s,p):
    return ('DateTime.DaysInMonth(year, month)' in r and r.index('_periodLoadFailed = true;') < r.index('_salarySource.Clear();') < r.index('DateTime.DaysInMonth(year, month)') < r.index('LoadEmpData(cond);')
        and 'Math.Min(DateTime.Now.Day, DateTime.DaysInMonth(year, month))' in r
        and l.index('_periodLoadFailed = true;') < l.index('_salarySource.Clear();') < l.index('da.Fill(dt);') < l.index('_periodLoadFailed = false;')
        and '_salarySource.Clear();' in l[l.index('catch (Exception ex)'):]
        and '_periodLoadFailed' in s and s.index('_periodLoadFailed') < s.index('SaveReceipt1(')
        and '_periodLoadFailed' in p and p.index('_periodLoadFailed') < p.index('_print.Printing('))
def tax_contract(s):
    return (all(x in s for x in ['Convert.ToDouble(row["tax"])','Convert.ToDouble(row["ExtraVAT"])',
            'inv.VAT            = ordinaryVAT;', 'inv.ExtraVAT       = extraVAT;',
            'inv.TotalTax       = Math.Round(ordinaryVAT + extraVAT, 2);']) and 'taxTotal - extraVAT' not in s)
def request_contract(l,s):
    return (all(x in l for x in ['!IsLoaded','clientType != 1 && clientType != 2', 'loadclients((short)clientType);',
              'selectedClient != clientId', 'chkAllClients.IsChecked == true', 'chkAll.IsChecked = false;',
              'selectedStore != storeId', 'chkAll.IsChecked == true', 'ShowResult();', 'catch (Exception ex)'])
        and l.index('chkAll.IsChecked = false;') < l.index('cmbSafes.SelectedValue = storeId;') < l.index('selectedStore != storeId') < l.index('ShowResult();')
        and all(x in s for x in ['cmbSafes.SelectedIndex < 0','cmbClients.SelectedIndex < 0',
                                'Inv_sub.store={storeFilter}', 'Inv.cust_id={clientFilter}']))
def party_contract(s):
    return all(x in s for x in ['GetSelectedClientId()', 'row.ItemId <= 0', 'clientId <= 0',
           'InvType != 4 && InvType != 5', 'cmbClient.SelectedItem is DataRowView selectedParty',
           'InvType == 5 ? 1 : 2', 'LastProcess(row.ItemId, row.StoreId, clientId, clientType)'])

check('period refresh invalidates prior rows and gates failure before output',period_contract(refresh,load,save,printing))
check('old invalid date mutation is detected',not period_contract(refresh.replace('Math.Min(DateTime.Now.Day, DateTime.DaysInMonth(year, month))','DateTime.Now.Day'),load,save,printing))
check('partial data failure mutation detected',not period_contract(refresh,load.replace('_salarySource.Clear();\n                DXMessageBox.Show("خطأ في تحميل البيانات:', 'DXMessageBox.Show("خطأ في تحميل البيانات:'),save,printing))
check('save gate mutation detected',not period_contract(refresh,load,save.replace('_periodLoadFailed','false'),printing))
check('reset suppresses selection handlers during defaults',reset.index('_loaded = false;') < reset.index('cmbMonth.SelectedIndex'))
check('reset invalidates and clears before work, validating only after completion',
      reset.index('_periodLoadFailed = true;') < reset.index('_salarySource.Clear();') < reset.index('txtDate.DateTime') < reset.index('_periodLoadFailed = false;')
      and '_salarySource.Clear();' in reset[reset.index('catch (Exception ex)'):])
check('both period events refresh',res.count('RefreshSelectedPeriod(true);')==1 and res.count('RefreshSelectedPeriod(false);')==1)
check('saved identity prevents recomputing under its ID', 'txtEntryGlobalId.Text' in refresh and 'TxtGlobalID.Text' in refresh and refresh.index('return;') < refresh.index('LoadEmpData(cond);'))
check('tax projection preserves components and derives total',tax_contract(projection))
check('tax subtraction mutant rejected',not tax_contract(projection.replace('inv.VAT            = ordinaryVAT;', 'inv.VAT            = ordinaryVAT - extraVAT;')))
check('writer binds ordinary and extra tax independently',bool(re.search(r'@tax[^\n]*inv\.VAT',writer,re.I)) and bool(re.search(r'@ExtraVAT[^\n]*inv\.ExtraVAT',writer,re.I)))
check('summary and export consume the projection', all(x in tax for x in ['_sumVAT      += inv.VAT;', '_sumExtraVAT += inv.ExtraVAT;', '_sumTotalTax += inv.TotalTax;', 'SpreadsheetExport.Money(inv.TotalTax)']))
check('specific activity requests fail closed and apply both scopes',request_contract(last,show))
check('all-warehouse mutation detected',not request_contract(last.replace('chkAll.IsChecked = false;', 'chkAll.IsChecked = true;'),show))
check('unvalidated party mutation detected',not request_contract(last.replace('selectedClient != clientId','false'),show))
check('later manual query missing selection mutation detected',not request_contract(last,show.replace('cmbSafes.SelectedIndex < 0','false')))
check('client lookup cleared before query and replaced even when empty',lookup.index('cmbClients.ItemsSource = null;') < lookup.index('adapter.Fill(dt);') < lookup.index('cmbClients.ItemsSource        = dt.DefaultView;') and 'dt.Rows.Count > 0' not in lookup)
check('party command sends validated identity and kind',party_contract(party))
check('party ID omission mutant detected',not party_contract(party.replace('row.StoreId, clientId, clientType','row.StoreId, -1, clientType')))
check('all-item command remains all-party', 'LastProcess(row.ItemId, row.StoreId, -1, 1)' in general)
check('xaml connects captions to expected methods', bool(re.search(r'x:Name="StripLastItem"[\s\S]*?Click="StripLastItem_Click"',xaml)) and bool(re.search(r'x:Name="StripClientLastItem"[\s\S]*?Click="StripClientLastItem_Click"',xaml)))

# These models isolate source-level arithmetic/control semantics; they do not run C#.
for y,m,d,want in [(2025,2,31,28),(2024,2,31,29),(2025,4,31,30),(2025,5,15,15)]:
    check('calendar clamp %d-%d day %d' % (y,m,d), min(d,calendar.monthrange(y,m)[1])==want)
for ordinary,extra,expected in [(20,5,(20,5,25)),(20,0,(20,0,20)),(5,5,(5,5,10)),(0,5,(0,5,5))]:
    check('tax components %r' % ((ordinary,extra),),(ordinary,extra,ordinary+extra)==expected)
con=sqlite3.connect(':memory:')
con.execute('create table movements(item int, store int, party int, day int)')
con.executemany('insert into movements values(?,?,?,?)',[(1,3,11,1),(1,2,22,2),(1,2,11,3),(1,1,11,4),(1,2,22,5)])
check('requested store and party select last scoped movement',con.execute('select store,party from movements where item=? and store=? and party=? order by day desc limit 1',(1,2,11)).fetchall()==[(2,11)])
check('all-warehouse control would select another store',con.execute('select store,party from movements where item=? and party=? order by day desc limit 1',(1,11)).fetchall()==[(1,11)])
check('all-party control can select another party',con.execute('select store,party from movements where item=? and store=? order by day desc limit 1',(1,2)).fetchall()==[(2,22)])
for ready,matching,query in [(False,True,False),(True,False,False),(True,True,True)]:
    check('lookup readiness model %r' % ((ready,matching),), (ready and matching)==query)
print('RESULT: PASS — %d checks, not WPF, SQL Server, printing or financial acceptance.' % count)
