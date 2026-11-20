#!/usr/bin/env python3
"""Static contracts and bounded state models only; does not execute C# or dialogs."""
from pathlib import Path
R = Path(__file__).resolve().parents[2] / 'SmartAuditERP/Form_WPF'
def read(name): return (R / name).read_text(encoding='utf-8-sig')
def part(s, a, b): return s[s.index(a):s.index(b, s.index(a))]
def ordered(s, xs):
 p=-1
 for x in xs:
  p=s.find(x,p+1)
  if p<0:return False
 return True
def check(name,v):
 if not v:raise AssertionError(name)
 print('PASS',name)
purch=read('frmInvPurch.xaml.cs');sale=read('frmInvSale.xaml.cs')
p=part(purch,'private void btnInsertLinkedInv_Click(', 'private void PrepareReturnInvoice(')
s=part(sale,'private void InsertLinkedReturn(', 'private void InsertLinkedFromQuotation(')
def pc(x):return ordered(x,['if (this.CheckBeforeClear()) return;', 'this.CLR();', 'this.InvType == 1 && this.ProcType == 2', 'this.CLR();', 'InvoiceOper.InsertFromInv(ref this.Invoic, 1);']) and 'this.btnNew_Click(sender, e);' not in x
def sc(x):return ordered(x,['if (CheckBeforeClear()) return;', 'if (MainClass.ReturnYearPreviews)', 'MainClass.connstr =', 'CLR();','InvoiceOper.InsertFromInv(ref Invoic, 1);'])
check('purchase existing stay result gates both clears and import',pc(p))
check('removing purchase return mutant rejected',not pc(p.replace('if (this.CheckBeforeClear()) return;','this.CheckBeforeClear();')))
check('sale existing stay result gates connection switch and clear',sc(s))
check('removing sale return mutant rejected',not sc(s.replace('if (CheckBeforeClear()) return;','CheckBeforeClear();')))
check('ordinary New handler still uses original guard', 'if (!this.CheckBeforeClear())\n                this.CLR();' in purch)
# Abstraction with the existing guard's boolean return, not a UI/DTO simulation.
def run(stay, old):
 if stay:return old, []
 return 'cleared',['clear','import']
check('refused abandon preserves original model',run(True,'draft')==('draft',[]))
check('allowed abandon reaches old conversion model',run(False,'draft')==('cleared',['clear','import']))
check('cancel after clear remains an explicit unresolved risk',p.index('this.CLR();') < p.index('InsertFromInv(') and s.index('CLR();') < s.index('InsertFromInv('))
print('PASS — scoped source and models only; no CLR/WPF/SQL or ERP acceptance.')
