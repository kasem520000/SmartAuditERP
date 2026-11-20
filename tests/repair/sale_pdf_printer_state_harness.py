#!/usr/bin/env python3
"""P7-163: request-local PDF destination; source witnesses + supplied model.

Does not execute WPF/DevExpress, choose a printer, write PDF, or print a page.
The PDF engine can override the passed destination via its printer picker.
P7B33T-01..32 remain unexecuted acceptance plans.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
sale = (ROOT / 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs').read_text(encoding='utf-8-sig')
engine = (ROOT / 'SmartAuditERP/Class/Print.cs').read_text(encoding='utf-8-sig')
xaml = (ROOT / 'SmartAuditERP/Form_WPF/frmInvSale.xaml').read_text(encoding='utf-8-sig')


def between(text, start, end):
    a = text.index(start)
    return text[a:text.index(end, a)]


def mask_comments(s):
    return re.sub(r'//[^\n]*|/\*.*?\*/', '', s, flags=re.S)


def contract(source):
    pdf = mask_comments(between(source, 'private void RptPrintPDF(', '#endregion'))
    return ('print.defPrinter' not in pdf and
            len(re.findall(r'\bprint\.Printing\s*\(', pdf)) == 1 and
            bool(re.search(r'print\.Printing\s*\(\s*type\s*,\s*print\.BindToData\(inv\)\s*,\s*'
                           r'print\.RptUrl\s*,\s*print\.RptName\s*,\s*"Microsoft Print to PDF"\s*,\s*'
                           r'print\.kitchenprinter\s*,\s*print\.PrintNo\s*\)', pdf)))


count = 0

def check(name, condition):
    global count
    count += 1
    if not condition:
        raise AssertionError(name)
    print('PASS', name)


pdf = between(sale, 'private void RptPrintPDF(', '#endregion')
normal = between(sale, 'private void RptPrint(', 'private void RptPrintPDF(')
click = between(sale, 'private void ExportPDF_Click(', 'private void BTnShowEntry_Click(')
printing = between(engine, 'public bool Printing(', 'public void ShareFileViaWhatsAppWeb(')
# Bound to the following method region rather than assuming the entire class has
# no references: initialization elsewhere intentionally sets the normal printer.
binding = between(engine, 'public DataSet BindToData(Invoice Inv)', 'public DataSet BindToData2(') if 'public DataSet BindToData2(' in engine else engine[engine.index('public DataSet BindToData(Invoice Inv)'):]
check('PDF passes its destination by value without touching the shared printer', contract(sale))
check('PDF guards remain before output', pdf.index('GridControl1.Items.Count == 0') <
      pdf.index('string.IsNullOrEmpty(print.RptUrl)') < pdf.index('File.Exists(path)') < pdf.index('print.Printing('))
check('normal printing keeps its existing empty-printer fallback and argument',
      'if (string.IsNullOrEmpty(print.defPrinter))' in normal and
      'print.defPrinter = MainClass.ReportsPrinter;' in normal and
      'print.defPrinter, print.kitchenprinter, print.PrintNo' in normal)
check('PDF click still uses saved and unchanged invoice guard',
      'Invoic.IsPrinted && !Invoic.IsUpdated' in click and 'RptPrintPDF(' in click)
check('XAML still connects PDF command', 'Click="ExportPDF_Click"' in xaml)
check('engine accepts the destination by value and returns a result', bool(re.search(
      r'public\s+bool\s+Printing\s*\(int type, DataSet ds, string RptUrl, string RptName,\s*'
      r'string defPrinter, string kitchenprinter, int PrintNo\)', engine)))
check('picker can still override the request destination',
      'defPrinter = frmPrinter2.SelectedPrinter;' in printing and 'this.defPrinter =' not in printing)
check('data-binding region does not directly reference the printer property',
      'defPrinter' not in mask_comments(binding))
check('repair is tagged', 'Repair R-103 (audit finding P7-163)' in pdf)

# This is a supplied model at the caller boundary. It does not model a printer
# driver, nor whether the engine/OS makes a file or which destination the picker
# ultimately selects. A callback failure denotes non-return at the call site.
class PrintState:
    def __init__(self, printer):
        self.printer = printer
        self.requests = []

    def pdf(self, passes_gate=True, bind_returns=True, engine_returns=True):
        if not passes_gate:
            return 'guard'
        if not bind_returns:
            return 'bind-failed'
        self.requests.append('Microsoft Print to PDF')
        return 'returned' if engine_returns else 'engine-failed'

    def normal(self, fallback):
        if not self.printer:
            self.printer = fallback
        self.requests.append(self.printer)
        return self.printer


for original in ('Paper A', '', None):
    state = PrintState(original)
    state.pdf()
    check('PDF preserves original printer %r' % original, state.printer == original)
    check('next normal request uses configured/fallback printer %r' % original,
          state.normal('Fallback') == (original or 'Fallback'))
    check('PDF request receives PDF destination %r' % original,
          state.requests == ['Microsoft Print to PDF', original or 'Fallback'])
for gate, bind, engine_returns in [(False, True, True), (True, False, True), (True, True, False)]:
    state = PrintState('Paper A')
    state.pdf(gate, bind, engine_returns)
    check('guard/failure preserves subsequent normal printer %r' % ((gate, bind, engine_returns),),
          state.printer == 'Paper A' and state.normal('Fallback') == 'Paper A')
a, b = PrintState('Paper A'), PrintState('Paper B')
a.pdf()
check('independent instances do not share the modeled printer property',
      a.normal('Fallback') == 'Paper A' and b.normal('Fallback') == 'Paper B')
check('repeated PDF requests do not alter later normal output destination',
      (lambda s: (s.pdf(), s.pdf(), s.normal('Fallback'))[-1])(PrintState('Paper A')) == 'Paper A')

# Witness must reject regressions including restoring the old state write and
# passing the wrong destination. Mutants live in memory and never touch sources.
mutants = [
    sale.replace('"Microsoft Print to PDF", print.kitchenprinter, print.PrintNo);',
                 'print.defPrinter, print.kitchenprinter, print.PrintNo);', 1),
    sale.replace('            print.Printing(type, print.BindToData(inv),\n                print.RptUrl, print.RptName,\n                "Microsoft Print to PDF",',
                 '            print.defPrinter = "Microsoft Print to PDF";\n            print.Printing(type, print.BindToData(inv),\n                print.RptUrl, print.RptName,\n                "Microsoft Print to PDF",', 1),
    sale.replace('"Microsoft Print to PDF", print.kitchenprinter, print.PrintNo);',
                 '"Other Printer", print.kitchenprinter, print.PrintNo);', 1),
]
for i, mutant in enumerate(mutants, 1):
    check('source witness rejects mutant %d' % i, not contract(mutant))
print('RESULT: PASS - %d checks; no printing or WPF execution.' % count)
