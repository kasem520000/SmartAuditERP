#!/usr/bin/env python3
"""P7-089: structural XAML witnesses and a supplied grid-layout model.

No WPF rendering, hit testing, keyboard navigation, accessibility technology,
DPI, actual bounds, or ERP acceptance tests are run here.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
xaml = (ROOT / 'SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml').read_text(encoding='utf-8-sig')
code = (ROOT / 'SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs').read_text(encoding='utf-8-sig')
P = '{http://schemas.microsoft.com/winfx/2006/xaml/presentation}'
X = '{http://schemas.microsoft.com/winfx/2006/xaml}'


def by_name(root, name):
    found = [element for element in root.iter() if element.get(X + 'Name') == name]
    if len(found) != 1:
        raise AssertionError('Expected exactly one ' + name)
    return found[0]


def analyze(text):
    root = ET.fromstring(text)
    parents = {child: parent for parent in root.iter() for child in parent}
    start = by_name(root, 'txtDateFrom')
    end = by_name(root, 'txtDateTo')
    a, b = parents[start], parents[end]
    grid = parents[a]
    if a.tag != P + 'StackPanel' or b.tag != P + 'StackPanel' or parents.get(b) is not grid:
        return None
    defs = grid.find(P + 'Grid.ColumnDefinitions')
    if defs is None:
        return None
    cols = [child.get('Width') for child in defs]
    return root, start, end, a, b, grid, cols


def contract(text):
    info = analyze(text)
    if info is None:
        return False
    root, start, end, a, b, grid, cols = info
    return (root.get('FlowDirection') == 'RightToLeft' and
            start.tag == end.tag == P + 'DatePicker' and
            cols == ['*', '10', '*', '10', '*', '10', '*'] and
            a.get('Grid.Column') == '0' and b.get('Grid.Column') == '2' and
            a.get('Grid.ColumnSpan', '1') == b.get('Grid.ColumnSpan', '1') == '1' and
            start.get('AutomationProperties.Name') == 'من تاريخ' and
            end.get('AutomationProperties.Name') == 'إلى تاريخ' and
            any(node.tag == P + 'TextBlock' and node.get('Text') == 'من تاريخ' for node in a) and
            any(node.tag == P + 'TextBlock' and node.get('Text') == 'إلى تاريخ' for node in b) and
            list(grid).index(a) < list(grid).index(b))


count = 0

def check(name, condition):
    global count
    count += 1
    if not condition:
        raise AssertionError(name)
    print('PASS', name)


check('the named date controls have separate labeled grid columns', contract(xaml))
root, start, end, a, b, grid, cols = analyze(xaml)
check('date controls preserve visual settings', all(element.get(key) == value for element in (start, end)
      for key, value in {'Height': '30', 'FontSize': '11', 'SelectedDateFormat': 'Short',
                         'Background': 'White', 'BorderThickness': '1'}.items()))
check('user and customer still use the original columns',
      [e.get('Grid.Column') for e in grid if e.tag == P + 'StackPanel'] == ['0', '2', '4', '6'])
check('both date pickers keep separate SelectedDate initialization',
      'txtDateFrom.SelectedDate = DateTime.Today;' in code and 'txtDateTo.SelectedDate = DateTime.Today;' in code)
start_body = code[code.index('private DateTime GetDateFrom()'):code.index('private DateTime GetDateTo()')]
end_body = code[code.index('private DateTime GetDateTo()'):code.index('private void SetProgress(')]
check('query date readers continue using their respective controls',
      'txtDateFrom.SelectedDate.Value' in start_body and 'txtDateTo.SelectedDate.Value' in end_body and
      'txtDateTo.SelectedDate' not in start_body and 'txtDateFrom.SelectedDate' not in end_body)
check('source retains a repair tag', 'Repair R-102 (audit finding P7-089)' in xaml)

# A supplied mathematical model of four equal star columns with three spacers.
# It checks the intended relationship, not actual WPF measurement or hit testing.
def bounds(width, index, rtl):
    star = (width - 30) / 4
    widths = [star, 10, star, 10, star, 10, star]
    left = sum(widths[:index])
    right = left + widths[index]
    return (width - right, width - left) if rtl else (left, right)


def disjoint(x, y):
    return x[1] <= y[0] or y[1] <= x[0]


check('legacy default column model overlaps', not disjoint(bounds(400, 0, True), bounds(400, 0, True)))
for width in (120, 400, 900):
    for rtl in (False, True):
        check('modeled columns are separate at width %s rtl %s' % (width, rtl),
              disjoint(bounds(width, 0, rtl), bounds(width, 2, rtl)))

mutants = [
    xaml.replace('<StackPanel Grid.Column="2">\n                            <TextBlock Text="إلى تاريخ"',
                 '<StackPanel Grid.Column="0">\n                            <TextBlock Text="إلى تاريخ"', 1),
    xaml.replace('<StackPanel Grid.Column="0">\n                            <TextBlock Text="من تاريخ"',
                 '<StackPanel Grid.Column="0" Grid.ColumnSpan="3">\n                            <TextBlock Text="من تاريخ"', 1),
    xaml.replace('AutomationProperties.Name="من تاريخ"', 'AutomationProperties.Name="تاريخ"', 1),
    xaml.replace('Text="إلى تاريخ" Style="{StaticResource FieldLabel}"',
                 'Text="تاريخ" Style="{StaticResource FieldLabel}"', 1),
]
for index, mutant in enumerate(mutants, 1):
    check('source witness rejects layout mutant %d' % index, not contract(mutant))
print('RESULT: PASS - %d checks; XAML structure and supplied model only.' % count)
