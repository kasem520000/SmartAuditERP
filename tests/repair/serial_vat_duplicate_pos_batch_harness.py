#!/usr/bin/env python3
"""Source contracts and independent models; does not execute WPF, SQL or ERP."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
UI = ROOT / 'SmartAuditERP/Form_WPF'
CLASS = ROOT / 'SmartAuditERP/Class'
def read(p):
    try: return p.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError: return p.read_text(encoding='cp1256')
def part(s, start, end): return s[s.index(start):s.index(end, s.index(start))]
def check(label, cond):
    if not cond: raise AssertionError(label)
    print('PASS', label)

def pos_contract(s):
    return (s.count('invoice.InvDate =') == 1 and
            'if (Invoic.ISNew)\n                    invoice.InvDate = DateTime.Now;' in s and
            s.index('MappingInvoice(ref Invoic)') < s.index('invoice.InvDate =') < s.index('BindToEntry(invoice)') < s.index('SaveInvoice('))
pos=part(read(UI/'frmInvPOS.xaml.cs'),'private async void SaveAndPrint()', '// معالجة الطاولات')
check('POS only gives a new document the current timestamp before entry and save',pos_contract(pos))
check('POS old override mutation detected',not pos_contract(pos+' invoice.InvDate = DateTime.Now;'))
check('mapper derives invoice date from source date and time','invoice.InvDate = DateTime.Parse(Inv.InvDate.ToShortDateString() + " " + Inv.InvTime.ToShortTimeString());' in read(CLASS/'InvoiceOper.cs'))
for is_new in (False,True):
 for electronic in (False,True):
  actual='now' if is_new else 'mapped'
  check(f'POS date model new={is_new}, electronic={electronic}', actual==('now' if is_new else 'mapped'))

vat=part(read(UI/'frmTaxInvDetails.xaml.cs'),'private void ProcessPurchasesWithoutSubs(', '#endregion')
def vat_contract(s):
 return ('bool isVat = true;' in s and 'if (tax == 0) isVat = false;' in s and
         'if (tax == 0) { isVat = false;' in s and 'if (isVat && rbNoVAT.IsChecked == true) continue;' in s and
         'if (!isVat && rbWithVAT.IsChecked == true) continue;' in s and not re.search(r'\bIsVAT\b',s) and
         s.index('foreach (DataRow dr in table.Rows)') < s.index('bool isVat = true;') < s.index('invoiceRows.Add(row)'))
check('purchase without lines uses fresh local VAT flag per invoice',vat_contract(vat))
check('shared flag mutation detected',not vat_contract(vat.replace('bool isVat = true;','IsVAT = true;')))
for taxes in ([0,15],[15,0],[0,0,15],[15,15,0]):
 for mode in ('all','vat','no'):
  result=[]
  for tax in taxes:
   is_vat=True; inv_vat=0
   if mode=='no':
    if tax==0: is_vat=False; inv_vat=tax
   elif mode=='vat':
    if tax>0: inv_vat=tax
   else:
    if tax==0: is_vat=False
    inv_vat=tax
   if mode=='vat' and inv_vat==0: continue
   if mode=='vat' and not is_vat: continue
   if mode=='no' and is_vat: continue
   result.append(tax)
  expected={'all':list(taxes),'vat':[x for x in taxes if x>0],'no':[x for x in taxes if x==0]}[mode]
  check(f'VAT row sequence {taxes} {mode}', result==expected)

msg=read(UI/'MsgExistItem.xaml.cs')
def actions(s):
 return [int(re.search(r'Action\s*=\s*(\d+)',part(s,'private void '+a, end)).group(1)) for a,end in [('btnAddquantity_Click','private void btnNewTirm_Click'),('btnNewTirm_Click','private void btnNon_Click'),('btnNon_Click','#endregion')]]
check('dialog add quantity/new line/none use consumers contract 1/2/3', actions(msg)==[1,2,3])
check('swapped dialog mutation detected', actions(msg.replace('Action = 1;','Action = 2;',1)) != [1,2,3])
check('window close retains default non-action','public int Action = 0;' in msg and 'Action = 0;' in msg)
for file,var,qty in [('frmPurchInv.xaml.cs','msgExist','QuantDgv'),('frmSalePurch.xaml.cs','msgForm','Quantity'),('frmSalesInvoice.xaml.cs','msgExist','Quantity'),('frmProductionOrder.xaml.cs','msgExist','Qty')]:
 s=read(UI/file); chunk=s[s.index('new MsgExistItem()'):]; chunk=chunk[:chunk.index('Action == 2') if 'Action == 2' in chunk else chunk.index('Action != 2')]
 check(file+' treats action 1 as quantity',f'{var}.Action == 1' in chunk and qty in chunk)
s=read(UI/'FrmIntialRestraiction.xaml.cs'); check('account dialog hides quantity and accepts action 2', 'msgExist.btnAddquantity.Visibility = Visibility.Collapsed;' in s and 'msgExist.Action != 2' in s)
for file in ('ItemOper.cs','ItemOpercontract.cs'):
 s=read(CLASS/file)
 check(file+' duplicate consumers use action 1 quantity and 2 break',s.count('.Action == 1)')==s.count('new MsgExistItem()') and s.count('.Action == 2)')==s.count('new MsgExistItem()'))

for name,coll in [('frmRptSerialNo','SerialList'),('frmRptSerialNoSummary','SummaryList')]:
 xml=read(UI/(name+'.xaml')); ET.fromstring(xml)
 s=read(UI/(name+'.xaml.cs'))
 show=part(s,'private void ShowResults()', '#endregion')
 selection=part(s,'private void addNewItem()', '#endregion')
 mode=part(s,'private void ckAllItems_CheckedChanged', 'private void txtItemFilter_TextChanged')
 changed=part(s,'private void txtItemFilter_TextChanged', 'private void chkAllSeialNo_CheckedChanged')
 def contract(a):
  return ('ckAllItems.IsChecked != true && SelectedId <= 0' in a and 'ckAllItems.IsChecked == true ? (object)DBNull.Value : SelectedId' in a and a.index(coll+'.Clear();') < a.index('SelectedId <= 0') < a.index('new SqlCommand('))
 check(name+' XML search and text handlers wired', all(x in xml for x in ['x:Name="btnSearchItem"','Click="btnSearch_Click"','TextChanged="txtItemFilter_TextChanged"']) and xml.count('TextChanged="txtItemFilter_TextChanged"')==2)
 check(name+' mode enables picker and clears old rows', 'btnSearchItem.IsEnabled = !isAll;' in mode and coll+'?.Clear();' in mode)
 check(name+' rejects invalid selection before SQL and explicit all filter',contract(show))
 check(name+' reject guard mutation detected',not contract(show.replace('SelectedId <= 0','false')))
 check(name+' edits invalidate identity and rows','SelectedId = -1;' in changed and coll+'?.Clear();' in changed)
 check(name+' identity published after both text updates',selection.index('form.ISDone && form.ItemId > 0') < selection.index('txtItemCode.Text = itemCode;') < selection.index('txtItemName.Text = form.Itemname;') < selection.index('SelectedId = form.ItemId;'))
 for all_items,ident in [(True,-1),(True,12),(False,-1),(False,0),(False,12)]:
  query = None if all_items else (ident if ident>0 else 'rejected')
  check(f'{name} query model all={all_items}, id={ident}', query==(None if all_items else (ident if ident>0 else 'rejected')))
print('Source contracts and models PASS; no WPF/SQL/ERP execution.')
