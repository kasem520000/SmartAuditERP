# -*- coding: utf-8 -*-
"""Repair R-092 / R-093 - audit finding P7-161 (Medium, confirmed):
"a missing navigation target, or a failure in its reader, zeroes the invoice editor that is on
screen without distinguishing the outcome".

The reader `InvoiceOper.BindingInvoice(ref InvoiceDGV, string)` fills the instance it is handed and
nulls that reference both when the query returns no row and when it throws. `Navigate` used to clear
the editor first, so the instance the reader filled was already a replacement, and when the reader
came back empty the editor published a blank invoice of its own: the document the user was looking
at was gone, "there is no next invoice" and "the load failed" looked identical, and two resets with
two numbering reads ran to produce it.

R-092 repairs the two editors the finding names (frmInvPurch, frmInvSale). R-093 is a grounded
expansion to the four other screens that navigate through the same reader with the same shape
(frmInvInputOutput, frmInvPOS, frmInventoryTransfer, frmcontract - the last through its own
contract reader, which nulls its reference the same way).

Part A models the reader, Part B the editor before and after, Part C witnesses the source, Part D
records what was deliberately NOT built. No .NET toolchain exists here, so nothing is a runtime
claim: no editor was opened, no query was run, no message box was shown.
"""
import glob
import io
import sys

FAILS = []
CHECKS = [0]


def check(name, cond, detail=""):
    CHECKS[0] += 1
    if not cond:
        FAILS.append("%s%s" % (name, ("  [%s]" % detail) if detail else ""))
        print("  FAIL  " + name)
    else:
        print("  ok    " + name)


def src(rel):
    return io.open(rel, encoding="utf-8", errors="replace").read()


def nav_slice(text, start, end):
    """The Navigate method: the end landmark is searched for after the start, never before it."""
    i = text.index(start)
    return text[i:text.index(end, i)]


def ordered(text, *landmarks):
    positions = []
    for mark in landmarks:
        if text.count(mark) != 1:
            return False
        positions.append(text.index(mark))
    return positions == sorted(positions)


F = "SmartAuditERP/Form_WPF/"
PUR = src(F + "frmInvPurch.xaml.cs")
SAL = src(F + "frmInvSale.xaml.cs")
INOUT = src(F + "frmInvInputOutput.xaml.cs")
POS = src(F + "frmInvPOS.xaml.cs")
TRF = src(F + "frmInventoryTransfer.xaml.cs")
CTR = src(F + "frmcontract.xaml.cs")
OPER = src("SmartAuditERP/Class/InvoiceOper.cs")
OPER_C = src("SmartAuditERP/Class/InvoiceOperContract.cs")

# ═══════════════════════════ Part A: the reader ═══════════════════════════
NEW_NUMBER = 41          # what the numbering filter hands back for a fresh document
DEFAULT_DATE = "today"


class Invoice:
    """The editing instance: a header, its items, and the flags the reader sets."""

    def __init__(self, no=NEW_NUMBER, gid=None, items=(), is_new=True):
        self.no = no
        self.gid = gid
        self.items = list(items)
        self.is_new = is_new
        self.is_printed = False
        self.is_loaded = False
        self.is_updated = False
        self.vat = 0.0

    def signature(self):
        return (self.no, self.gid, tuple(self.items), self.is_new, self.is_printed,
                self.is_loaded, self.vat)


def reader(target, outcome, row=None):
    """BindingInvoice(ref Invo, sql): fills the instance handed to it on a found row and nulls the
    reference on an empty result and on an exception. It never invents an instance, and on the two
    null outcomes it has not touched the one it was given."""
    if target is None:
        return None                       # dereferencing nothing throws; the catch nulls the ref
    if outcome == "found":
        target.no = row["no"]
        target.gid = row["gid"]
        target.items = list(row["items"])
        target.vat = row["vat"]
        target.is_new = False
        target.is_printed = True
        target.is_loaded = False
        return target
    return None                           # "empty" (no rows) or "failed" (the catch)


ROW = {"no": 107, "gid": "G-107", "items": ["item-a", "item-b"], "vat": 15.0}

print("Part A: what the reader does, and what it cannot tell the caller")

held = Invoice(no=99, gid="G-99", items=["kept"])
filled = reader(held, "found", ROW)
check("A1 the reader fills the instance it was handed and marks it loaded rather than new",
      filled is held and held.no == 107 and held.gid == "G-107" and held.items == ROW["items"]
      and held.is_new is False and held.is_printed is True)
before = held.signature()
check("A2 an empty result nulls the reference and leaves the instance untouched",
      reader(held, "empty") is None and held.signature() == before,
      "after=%r" % (held.signature(),))
check("A3 a reader failure nulls the reference and leaves the instance untouched too",
      reader(held, "failed") is None and held.signature() == before)
check("A4 the reader never invents an instance: handed nothing it returns nothing",
      reader(None, "found", ROW) is None and reader(None, "empty") is None)
check("A5 empty and failed are the same observable, which is the finding's missing distinction",
      reader(held, "empty") == reader(held, "failed") is None)

# ═══════════════════ Part B: the editor before and after the repair ═══════════════════


class Editor:
    """One invoice editor: the instance it is showing, the grid's items, the bound controls, and
    the counters that make the cost of a needless reset visible."""

    def __init__(self, invoice=None, items=(), controls=None):
        self.invoic = invoice
        self.items = list(items)
        self.controls = dict(controls or {})
        self.resets = 0
        self.numbering_reads = 0
        self.published = []

    def clr(self):
        """CLR: defaults back into the controls, a fresh instance, an empty grid, and
        ResetInvoice -> LoadInvNo, which reads the numbering filter and raises ISNew."""
        self.resets += 1
        self.controls = {"no": "", "date": DEFAULT_DATE}
        self.invoic = Invoice()
        self.items = []
        self.numbering_reads += 1
        self.invoic.no = NEW_NUMBER
        self.invoic.is_new = True

    def bind(self):
        """BindingDGV + BindingControls: the controls and the grid follow the published invoice."""
        self.controls = {"no": str(self.invoic.no), "date": DEFAULT_DATE}
        self.items = list(self.invoic.items)
        self.published.append(self.invoic)

    def state(self):
        return (None if self.invoic is None else self.invoic.signature(),
                tuple(self.items), tuple(sorted(self.controls.items())),
                self.resets, self.numbering_reads, len(self.published))


def navigate_legacy(ed, outcome, row=None):
    """Clear first, then read through the editor's own reference, then blank on a null."""
    if ed.invoic is not None:
        ed.clr()
    ed.invoic = reader(ed.invoic, outcome, row)
    if ed.invoic is not None:
        ed.bind()
    else:
        ed.invoic = Invoice()
        ed.clr()


def navigate_fixed(ed, outcome, row=None):
    """Resolve first: read into an instance of its own, publish only what was found."""
    target = reader(Invoice(), outcome, row)
    if target is None:
        return
    if ed.invoic is not None:
        ed.clr()
    ed.invoic = target
    ed.bind()


def navigate_transfer(ed, outcome, row=None, is_loading=False, fixed=True):
    """The transfer screen keeps its own reset condition, and while loading it fills the instance
    it already holds instead of a fresh one."""
    will_clear = ed.invoic is not None and not is_loading
    if not fixed:
        if will_clear:
            ed.clr()
        ed.invoic = reader(ed.invoic, outcome, row)
        if ed.invoic is None:
            ed.invoic = Invoice()
            return
    else:
        target = Invoice() if (will_clear or ed.invoic is None) else ed.invoic
        target = reader(target, outcome, row)
        if target is None:
            return
        if will_clear:
            ed.clr()
        ed.invoic = target
    ed.bind()


def check_before_clear(ed, answer):
    """The standing guard: true means stay with the draft, so the command does not run."""
    if ed.invoic is None:
        return False
    if (len(ed.items) > 0 and ed.invoic.is_new) or ed.invoic.is_updated:
        return answer == "no"
    return False


def toolbar(ed, navigate, answer, outcome, row=None):
    if not check_before_clear(ed, answer):
        navigate(ed, outcome, row)
        return "ran"
    return "blocked"


def dirty_editor():
    inv = Invoice(no=55, gid="G-55", items=["draft-line"], is_new=True)
    return Editor(invoice=inv, items=["draft-line"], controls={"no": "55", "date": DEFAULT_DATE})


def clean_editor():
    inv = Invoice(no=55, gid="G-55", items=["saved-line"], is_new=False)
    inv.is_printed = True
    return Editor(invoice=inv, items=["saved-line"], controls={"no": "55", "date": DEFAULT_DATE})


print()
print("Part B: what the editor did, and what it does now")

ed = dirty_editor()
kept = ed.invoic
navigate_legacy(ed, "found", ROW)
check("B1 legacy, a found target: one reset, one numbering read, the loaded invoice published",
      ed.resets == 1 and ed.numbering_reads == 1 and ed.invoic.no == 107 and
      ed.items == ROW["items"] and ed.controls["no"] == "107" and len(ed.published) == 1 and
      ed.invoic is not kept, "state=%r" % (ed.state(),))

ed = dirty_editor()
kept = ed.invoic
navigate_legacy(ed, "empty")
legacy_empty = ed.state()
check("B2 legacy, no target: the draft is gone and a blank invoice is published after two resets",
      ed.invoic is not kept and ed.invoic.is_new is True and ed.invoic.no == NEW_NUMBER and
      ed.items == [] and ed.controls["no"] == "" and ed.resets == 2 and ed.numbering_reads == 2 and
      len(ed.published) == 0, "state=%r" % (legacy_empty,))

ed = dirty_editor()
navigate_legacy(ed, "failed")
check("B3 legacy, a failed reader: observably identical to no target at all",
      ed.state() == legacy_empty, "failed=%r empty=%r" % (ed.state(), legacy_empty))

ed = clean_editor()
kept = ed.invoic
navigate_legacy(ed, "empty")
check("B4 legacy, a clean saved invoice and no target: the saved document is destroyed too",
      ed.invoic is not kept and kept.no == 55 and ed.invoic.is_new is True and ed.resets == 2)

ed = Editor(invoice=None)
navigate_legacy(ed, "found", ROW)
legacy_no_original = ed.state()
check("B5 legacy, no invoice at all: the reader is handed nothing, so nothing loads",
      ed.invoic.is_new is True and ed.invoic.no == NEW_NUMBER and ed.resets == 1 and
      len(ed.published) == 0, "state=%r" % (legacy_no_original,))

ed = dirty_editor()
navigate_fixed(ed, "found", ROW)
check("B6 repaired, a found target: the successful path did not move",
      ed.resets == 1 and ed.numbering_reads == 1 and ed.invoic.no == 107 and
      ed.items == ROW["items"] and ed.controls["no"] == "107" and len(ed.published) == 1)

ed = dirty_editor()
kept = ed.invoic
kept_state = ed.state()
navigate_fixed(ed, "empty")
check("B7 repaired, no target: the draft stays exactly as it stood and nothing was reset",
      ed.invoic is kept and ed.state() == kept_state and ed.resets == 0 and
      ed.numbering_reads == 0 and len(ed.published) == 0, "state=%r" % (ed.state(),))

ed = dirty_editor()
kept = ed.invoic
navigate_fixed(ed, "failed")
check("B8 repaired, a failed reader: preserved the same way, and still not told apart",
      ed.invoic is kept and ed.resets == 0 and ed.numbering_reads == 0)

ed = clean_editor()
kept = ed.invoic
navigate_fixed(ed, "empty")
check("B9 repaired, a clean saved invoice and no target: the saved document survives",
      ed.invoic is kept and kept.no == 55 and kept.is_new is False and ed.resets == 0)

ed = Editor(invoice=None)
navigate_fixed(ed, "found", ROW)
check("B10 repaired, no invoice at all: the target is read into its own instance, so it loads",
      ed.invoic.no == 107 and ed.items == ROW["items"] and ed.resets == 0 and
      len(ed.published) == 1, "state=%r legacy=%r" % (ed.state(), legacy_no_original))

ed = dirty_editor()
navigate_fixed(ed, "empty")
check("B11 no implicit blank invoice: ISNew and the number still belong to the document shown",
      ed.invoic.is_new is True and ed.invoic.no == 55 and ed.items == ["draft-line"] and
      ed.controls["no"] == "55")

ed = dirty_editor()
held = ed.invoic
navigate_transfer(ed, "found", ROW, is_loading=True)
check("B12 the transfer loading path still fills the instance it holds, without a reset",
      ed.invoic is held and held.no == 107 and ed.resets == 0 and ed.numbering_reads == 0)

ed = dirty_editor()
held = ed.invoic
held_state = ed.state()
navigate_transfer(ed, "empty", is_loading=True)
check("B13 the transfer loading path on no target: the held instance is still the editor's",
      ed.invoic is held and ed.state() == held_state)

ed = dirty_editor()
navigate_transfer(ed, "found", ROW, is_loading=False)
check("B14 the transfer reset still runs on its own condition when it is not loading",
      ed.resets == 1 and ed.numbering_reads == 1 and ed.invoic.no == 107)

ed = dirty_editor()
check("B15 the leave decision still precedes the first write, in both models",
      toolbar(ed, navigate_legacy, "no", "found", ROW) == "blocked" and ed.resets == 0 and
      ed.numbering_reads == 0 and len(ed.published) == 0 and
      toolbar(ed, navigate_fixed, "no", "found", ROW) == "blocked" and ed.resets == 0)
ed = dirty_editor()
check("B16 yes leaves the draft and clean never asks, so the command runs in both models",
      toolbar(ed, navigate_fixed, "yes", "found", ROW) == "ran" and ed.invoic.no == 107 and
      toolbar(clean_editor(), navigate_fixed, "yes", "found", ROW) == "ran")

# ═══════════════════════════ Part C: the source ═══════════════════════════
print()
print("Part C: static witnesses over the six screens and the two readers")

pur_nav = nav_slice(PUR, "public void Navigate(string sqlStr)", "private void btnFirst_Click")
check("C1 purchase: read into its own instance, refuse to publish nothing, then reset and bind",
      ordered(pur_nav, "InvoiceDGV target = new InvoiceDGV();",
              "InvoiceOper.BindingInvoice(ref target, sqlStr);", "if (target == null) return;",
              "this.CLR();", "this.Invoic = target;", "this.BindingDGV();",
              "this.BindingControls();",
              "this.ckZeroVAT.IsChecked = (this.Invoic.VAT == 0.0);") and
      pur_nav.count("this.CLR();") == 1 and
      "this.Invoic = new InvoiceDGV();" not in pur_nav and
      "BindingInvoice(ref this.Invoic" not in pur_nav)

sal_nav = nav_slice(SAL, "public void Navigate(string sqlStr)", "private bool CheckBeforeClear()")
check("C2 sale: the same order, and its own found-block statements preserved",
      ordered(sal_nav, "InvoiceDGV target = new InvoiceDGV();",
              "InvoiceOper.BindingInvoice(ref target, sqlStr);", "if (target == null) return;",
              "if (Invoic != null) CLR();", "Invoic = target;",
              "new SolidColorBrush(Color.FromRgb(245, 245, 245));", "BindingDGV();",
              "BindingControls();") and
      sal_nav.count("CLR();") == 1 and "Invoic = new InvoiceDGV();" not in sal_nav and
      "BindingInvoice(ref Invoic" not in sal_nav)

io_nav = nav_slice(INOUT, "public void Navigate(string sqlStr)", "private void btnFirst_Click")
check("C3 input/output: its unconditional reset stays, only after a found target",
      ordered(io_nav, "InvoiceDGV target = new InvoiceDGV();",
              "InvoiceOper.BindingInvoice(ref target, sqlStr);", "if (target == null) return;",
              "CLR();", "Invoic = target;", "RefreshGrid();", "BindingControls();") and
      io_nav.count("CLR();") == 1 and "Invoic = new InvoiceDGV();" not in io_nav)

pos_nav = nav_slice(POS, "public void Navigate(string sqlStr)", "#endregion")
check("C4 point of sale: the items collection and the grid source are still attached after publish",
      ordered(pos_nav, "InvoiceDGV target = new InvoiceDGV();",
              "InvoiceOper.BindingInvoice(ref target, sqlStr);", "if (target == null) return;",
              "CLR();", "Invoic = target;",
              "_invoiceItems = new ObservableCollection<InvoiceItem>(",
              "GridControl1.ItemsSource = _invoiceItems;", "BindingDGV(true);",
              "BindingControls();") and
      pos_nav.count("CLR();") == 1 and "Invoic = new InvoiceDGV();" not in pos_nav)

trf_nav = nav_slice(TRF, "private bool TryNavigate(string sqlStr, string expectedGlobalId)", "catch (Exception ex)")
check("C5 transfer: the loading path keeps its instance and its own reset condition",
      ordered(trf_nav, "bool willClear = _invoic != null && !_isLoading;",
              "InvoiceDGV target = (willClear || _invoic == null)", ": _invoic;",
              "InvoiceOper.BindingInvoice(ref target, sqlStr);", "if (target == null) return false;",
              "if (willClear)", "CLR();", "_invoic = target;") and
      trf_nav.count("CLR();") == 1 and "_invoic = new InvoiceDGV();" not in trf_nav and
      TRF.count("if (_invoic != null && !_isLoading)") == 4,
      "the other guarded commands keep their own test")

ctr_nav = nav_slice(CTR, "public void Navigate(string sqlQuery)", "private void btnFirst_Click")
check("C6 contracts: the same contract against its own reader and its own document type",
      ordered(ctr_nav, "Invoicecontract target = new Invoicecontract();",
              "InvoiceOperContract.BindingInvoice(ref target, sqlQuery);",
              "if (target == null) return;", "if (Invoic != null) CLR();", "Invoic = target;",
              "GridControl1.ItemsSource = Invoic.InvoiceItems;", "GridControl1.RefreshData();",
              "BindingDGV();", "BindingControls();") and
      ctr_nav.count("CLR();") == 1 and "Invoic = new Invoicecontract();" not in ctr_nav)

check("C7 neither reader was touched: both still null their reference on empty and on failure",
      OPER.count("Invo = null;") == 2 and OPER_C.count("Invo = null;") == 2 and
      "Repair R-092" not in OPER and "Repair R-093" not in OPER and
      "Repair R-092" not in OPER_C and "Repair R-093" not in OPER_C and
      OPER.count("public static void BindingInvoice(ref InvoiceDGV Invo, string sqlstr)") == 1 and
      OPER.count("if (sqlDataReader.HasRows)") >= 1)

for label, text, handlers in (
        ("purchase", PUR, ("btnFirst_Click", "btnPrevious_Click", "btnNext_Click", "btnLast_Click")),
        ("sale", SAL, ("btnFirst_Click", "btnLast_Click", "btnNext_Click", "btnPrevious_Click"))):
    qualified = "this." if label == "purchase" else ""
    ok = True
    for h in handlers:
        i = text.index("private void %s(object sender, RoutedEventArgs e)" % h)
        body = text[i:text.index("Navigate(", i)]
        ok = ok and ("%sCheckBeforeClear()" % qualified) in body
    check("C8 the four %s toolbar commands still ask the standing guard before navigating" % label,
          ok and text.count("if (!%sCheckBeforeClear())" % qualified) == 5)

tagged = {}
for path in sorted(glob.glob(F + "*.cs")):
    text = src(path)
    tags = [t for t in ("R-092", "R-093") if "Repair %s (audit finding P7-161)" % t in text]
    if tags:
        tagged[path.split("/")[-1]] = tags
check("C9 exactly six screens carry the repair, two named by the finding and four expanded",
      tagged == {"frmInvPurch.xaml.cs": ["R-092"], "frmInvSale.xaml.cs": ["R-092"],
                 "frmInvInputOutput.xaml.cs": ["R-093"], "frmInvPOS.xaml.cs": ["R-093"],
                 "frmInventoryTransfer.xaml.cs": ["R-093"], "frmcontract.xaml.cs": ["R-093"]},
      "tagged=%s" % (tagged,))

screens, in_class = [], []
for path in sorted(glob.glob("SmartAuditERP/**/*.cs", recursive=True)):
    body = src(path)
    for i, line in enumerate(body.splitlines(), 1):
        if "BindingInvoice(ref" in line and "public static void" not in line:
            (screens if path.startswith(F) else in_class).append("%s:%d" % (path.split("/")[-1], i))
check("C11 the six screens are every screen caller of the two readers, so no seventh navigates this way",
      sorted(c.split(":")[0] for c in screens) == sorted(
          ["frmInvPurch.xaml.cs", "frmInvSale.xaml.cs", "frmInvInputOutput.xaml.cs",
           "frmInvPOS.xaml.cs", "frmInventoryTransfer.xaml.cs", "frmcontract.xaml.cs"]) and
      len(screens) == 6, "screens=%s" % (screens,))
check("C12 the two other callers stay inside InsertFromInv, another finding's territory, untouched",
      len(in_class) == 2 and
      OPER.count("InvoiceOper.BindingInvoice(ref Invo,") == 1 and
      OPER_C.count("InvoiceOperContract.BindingInvoice(ref Invo,") == 1 and
      OPER.count("public static void InsertFromInv(ref InvoiceDGV Invo, int Ptype)") == 1 and
      OPER_C.count("public static void InsertFromInv(ref Invoicecontract Invo, int Ptype)") == 1 and
      "Repair R-092" not in OPER and "Repair R-093" not in OPER and
      "Repair R-092" not in OPER_C and "Repair R-093" not in OPER_C,
      "in_class=%s" % (in_class,))

# Other guarded commands may be added; inspect the original two repair sites,
# not a whole-file count that treats an additional guard as a regression.
check("C10 the earlier navigation repairs are still in place in both named editors",
      all(ordered(text[text.index("Repair " + repair):text.index("Navigate(", text.index(guard, text.index("Repair " + repair))) + len("Navigate(")],
                  "Repair " + repair, guard, "Navigate(")
          for text, guard in ((PUR, "if (this.CheckBeforeClear()) return;"),
                              (SAL, "if (CheckBeforeClear()) return;"))
          for repair in ("R-081", "R-086 (audit finding P7-159")) and
      PUR.count("bool accepted = frm.isDone") == 1 and SAL.count("bool accepted = frm.isDone") == 1)

# ═══════════════ Part D: what was deliberately not built ═══════════════
print()
print("Part D: the owner-bound design was not implemented")

app_source = b""
for path in glob.glob("SmartAuditERP/**/*.cs", recursive=True):
    app_source += open(path, "rb").read()
check("D1 no full typed navigation outcome, request or document reference entered the application",
      all(tok not in app_source for tok in (b"LoadOutcome", b"NavigationRequest", b"ReaderOutcome",
                                            b"enum NavigationResult")) and
      all(tok not in (pur_nav + sal_nav + io_nav + pos_nav + trf_nav + ctr_nav)
          for tok in ("Outcome", "enum ", "working copy")))
check("D2 all six public void navigation APIs and a single target per screen are retained",
      all(text.count("private void Navigate") == 0 and text.count("public void Navigate(string") == 1
          for text in (PUR, SAL, INOUT, POS, TRF, CTR)) and
      PUR.count("InvoiceDGV target") == 1 and SAL.count("InvoiceDGV target") == 1 and
      INOUT.count("InvoiceDGV target") == 1 and POS.count("InvoiceDGV target") == 1 and
      TRF.count("InvoiceDGV target") == 1 and CTR.count("Invoicecontract target") == 1)
check("D3 no message, dialog or log was added for the two silent outcomes",
      all(tok not in (pur_nav + sal_nav + io_nav + pos_nav + trf_nav + ctr_nav)
          for tok in ("MessageBox", "DXMessageBox", "Logger.", "ShowError")))

print()
if FAILS:
    print("RESULT: FAIL (%d of %d checks)" % (len(FAILS), CHECKS[0]))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - %d checks. A navigation target is resolved before the editor is replaced:" % CHECKS[0])
print("a found invoice publishes exactly as before, and an absent or failed target leaves the")
print("document on screen untouched, with no implicit blank invoice and no needless reset.")
sys.exit(0)
