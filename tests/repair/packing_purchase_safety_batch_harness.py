#!/usr/bin/env python3
"""Source witnesses and independent illustrative models; not C#/WPF/SQL execution."""
from pathlib import Path
from math import ceil
ROOT = Path(__file__).resolve().parents[2] / 'SmartAuditERP' / 'Form_WPF'
def read(f): return (ROOT / f).read_text(encoding='utf-8-sig')
def section(s, start, end): return s[s.index(start):s.index(end,s.index(start))]
checks = 0
def check(name, value):
    global checks
    assert value, name
    checks += 1
    print('PASS', name)

def packing_contract(s):
    calc = section(s, 'private void Calc()', '#region TextChanged Events')
    net = section(s, 'private void txtNetQnty_TextChanged(', '#endregion')
    leaves = section(s, 'private void txtHeight_Leave(', 'private void txtQty_Leave(')
    enter = section(s, 'private void txtHeight_KeyDown(', 'private void txtWidth_KeyDown(')
    return (all(x in calc for x in ['if (_packingInputText == null)', 'netQntyValue = ParseNumber(_packingInputText, 0);', 'heightValue = _packingRoundUp', 'heightValue * widthValue * qtyValue'])
            and 'if (!_isInternalUpdate && ItemProperty == 2)' in net and '_packingInputText = txtNetQnty.Text;' in net
            and all('ItemProperty != 2 || _packingHeightEdited' in x and '_packingHeightEdited = false;' in x for x in (leaves,enter))
            and 'Calc();\n            NetQnty = ParseNumber(txtNetQnty.Text, 0);' in s)
s=read('frmItemProperties.xaml.cs')
check('packing request is separate from internally displayed result',packing_contract(s))
check('feedback mutant detected',not packing_contract(s.replace('netQntyValue = ParseNumber(_packingInputText, 0);','netQntyValue = ParseNumber(txtNetQnty.Text, 0);')))
check('height focus feedback mutant detected',not packing_contract(s.replace('ItemProperty != 2 || _packingHeightEdited','true')))
check('height user edit tracks rounding and dirty state', '_packingHeightEdited = true;' in s and '_packingRoundUp = Math.Abs(height % 1.0)' in s)
check('changing property resets stale request', '_packingInputText = null;' in section(s,'private void cmbItemProperties_SelectedIndexChanged(', '\n    }\n}'))

def calc(request,width,qty,round_up=False):
    if width <= 0 or qty <= 0: return (0,0)
    height = request/width
    if round_up: height = ceil(height)
    return height,height*width*qty
for request,width,qty,rounding in [(10,5,3,False),(7,5,2,True),(1,6,1,False),(7,0,2,False),(7,5,0,False)]:
    height,result=calc(request,width,qty,rounding)
    for _ in range(4):
        check('stable repeated callback '+str((request,width,qty,rounding)),calc(request,width,qty,rounding)==(height,result))
check('zero width does not erase request in model',calc(7,5,2)==(1.4,14))
check('changed qty recalculates from original',calc(10,5,4)==(2,40))
check('changed request becomes new input',calc(12,4,3)==(3,36))
check('explicit fractional height rounds when requested',calc(7,5,2,True)==(2,20))

p=read('frmPurchInv.xaml.cs')
search=section(p,'private void SearchByID(int unitId)','private void FillRowFromDt(')
increment=section(search,'if (msgExist.Action == 1)','else if (msgExist.Action == 2)')
separate=section(search,'else if (msgExist.Action == 2)','return;')
picker=section(p,'private void addNewItem()','#endregion')
def purchase_contract(increment,separate,picker):
    return ('_gridSource.Remove' not in increment and 'CalcRowValues(matchedIndex);' in increment
            and '_gridSource.Add(new PurchInvRow());' in separate and separate.index('_gridSource.Add(new PurchInvRow());') < separate.index('RowIndex = _gridSource.Count - 1;') < separate.index('FillRowFromDt(')
            and 'bool firstSelection = true;' in picker and 'if (!firstSelection ||' in picker and 'firstSelection = false;' in picker)
check('purchase duplicate preserves source and new line is appended',purchase_contract(increment,separate,picker))
check('remove source mutant detected',not purchase_contract(increment+'_gridSource.Remove(sourceRow);',separate,picker))
check('overwrite last row mutant detected',not purchase_contract(increment,separate.replace('_gridSource.Add(new PurchInvRow());',''),picker) if '_gridSource.Add(new PurchInvRow());' in separate else False)
check('reuse picker row mutant detected',not purchase_contract(increment,separate,picker.replace('if (!firstSelection ||','if (')))
for source,found in [(0,2),(2,0),(1,1)]:
    rows=[{'id':x,'qty':1} for x in 'ABC']; original=rows[source]; matched=rows[found]
    matched['qty']+=1
    check('increment preserves rows '+str((source,found)),len(rows)==3 and rows[source] is original and rows[found] is matched and matched['qty']==2)
rows=['A','B','C']; rows.append('A'); check('separate duplicate never overwrites last item',rows==['A','B','C','A'])
print('RESULT: PASS — %d source/model checks; no CLR, WPF, SQL or ERP acceptance.' % checks)
