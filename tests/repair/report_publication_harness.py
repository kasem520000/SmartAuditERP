#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-078 and R-079, both against audit finding
P7-046 (partial UI publication) - R-078 for the tax period report itself and
R-079 for the extension recorded in audit slice B28 (a failed search source
leaving the previous snapshot selectable). No .NET/WPF/SQL toolchain exists
here, so each repair is validated as a behavioural model of its publication
contract plus static witnesses over the repaired code.

Run: python3 tests/repair/report_publication_harness.py
Exit 0 on PASS.
"""
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


TAX = open("SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml.cs", encoding="utf-8").read()
SRCH = open("SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs", encoding="utf-8").read()

print("Part A: R-078 / P7-046 - the tax report publishes once, or not at all")

CELLS = ["txtNetSale", "txtTaxNetSale", "txtExtraVAT", "txtSalesOutTax", "txtSalesNoTax",
         "txtReceipts", "txtReceiptsVAT", "txtIncomes", "txtIncomesVAT",
         "txtNetSales", "txtNetSaleTax",
         "txtNetPurch", "txtTaxNetPurch", "txtPurchOutTax", "txtNoTaxPurch",
         "txtExpenseNet", "txtExpenseVAT", "txtNetPurches", "txtNetPurchTax", "txtNetTax"]

# The sources ShowDetails22 walks, in order, and the cells each one publishes.
SOURCES = [("sales", ["txtNetSale", "txtTaxNetSale", "txtExtraVAT", "txtSalesOutTax", "txtSalesNoTax"]),
           ("receipts", ["txtReceipts", "txtReceiptsVAT"]),
           ("rent", ["txtIncomes", "txtIncomesVAT"]),
           ("salesTotals", ["txtNetSales", "txtNetSaleTax"]),
           ("purchases", ["txtNetPurch", "txtTaxNetPurch", "txtPurchOutTax", "txtNoTaxPurch"]),
           ("expenses", ["txtExpenseNet", "txtExpenseVAT"]),
           ("purchaseTotals", ["txtNetPurches", "txtNetPurchTax"]),
           ("netVAT", ["txtNetTax"])]


def compute(data):
    """The arithmetic of ShowDetails22, independent of where the values are stored."""
    net_sale = round(data["saleBase"] - data["saleRetBase"], 2)
    tax_net_sale = round(data["saleTax"] - data["saleRetTax"], 2)
    receipt_vat = data["receiptNetVal"] - data["receiptTotal"]
    rent = data["rentNet"] - data["rentRet"]
    rent_vat = data["rentTax"] - data["rentRetTax"]
    net_sales = round(net_sale + data["receiptTotal"] + rent, 2)
    net_sales_tax = round(tax_net_sale + receipt_vat + rent_vat, 2)
    net_purch = round(data["purchBase"] - data["purchRetBase"], 2)
    tax_net_purch = round(data["purchTax"] - data["purchRetTax"], 2)
    net_purches = round(net_purch + data["expTotal"], 2)
    net_purches_tax = round(tax_net_purch + data["expVAT"], 2)
    net_vat = round(net_sales_tax - net_purches_tax, 6)
    return {
        "txtNetSale": str(net_sale), "txtTaxNetSale": str(tax_net_sale),
        "txtExtraVAT": str(round(data["extra"], 2)),
        "txtSalesOutTax": str(round(data["saleNoTaxBase"], 2)),
        "txtSalesNoTax": str(round(data["saleNoTaxTax"], 2)),
        "txtReceipts": str(data["receiptTotal"]), "txtReceiptsVAT": str(receipt_vat),
        "txtIncomes": str(rent), "txtIncomesVAT": str(rent_vat),
        "txtNetSales": str(net_sales), "txtNetSaleTax": str(net_sales_tax),
        "txtNetPurch": str(net_purch), "txtTaxNetPurch": str(tax_net_purch),
        "txtPurchOutTax": str(round(data["purchNoTaxBase"], 2)),
        "txtNoTaxPurch": str(round(data["purchNoTaxTax"], 2)),
        "txtExpenseNet": str(data["expTotal"]), "txtExpenseVAT": str(data["expVAT"]),
        "txtNetPurches": str(net_purches), "txtNetPurchTax": str(net_purches_tax),
        "txtNetTax": (str(net_vat) + "    (مستحق الدفع للهيئة)    ") if net_vat > 0
                     else (str(net_vat) + "   (غير مستحق)    "),
    }


PERIOD_A = {"saleBase": 1000.0, "saleRetBase": 100.0, "saleTax": 150.0, "saleRetTax": 15.0,
            "extra": 5.0, "saleNoTaxBase": 40.0, "saleNoTaxTax": 3.0,
            "receiptTotal": 200.0, "receiptNetVal": 230.0,
            "rentNet": 500.0, "rentTax": 75.0, "rentRet": 50.0, "rentRetTax": 7.5,
            "purchBase": 600.0, "purchRetBase": 60.0, "purchTax": 90.0, "purchRetTax": 9.0,
            "purchNoTaxBase": 20.0, "purchNoTaxTax": 1.5,
            "expTotal": 120.0, "expVAT": 18.0}
PERIOD_B = dict(PERIOD_A, saleBase=2500.0, saleTax=375.0, rentNet=900.0, expTotal=300.0)
EMPTY = {k: 0.0 for k in PERIOD_A}


def run(rules, cells, data, fail_at=None):
    """One ShowDetails22 run. Returns (cells, published, error_shown)."""
    values = compute(data)
    published, error = False, False
    if rules == "legacy":
        for name, owned in SOURCES:                 # published as each source completes
            if name == fail_at:
                error = True
                return cells, False, error          # outer catch only shows a message
            for c in owned:
                cells[c] = values[c]
        return cells, False, error                  # no notion of a complete report
    locals_ = {}
    try:
        for name, owned in SOURCES:                 # computed in memory only
            if name == fail_at:
                raise RuntimeError("source %s failed" % name)
            for c in owned:
                locals_[c] = values[c]
        for c in CELLS:                             # one publication pass
            cells[c] = locals_[c]
        published = True
    except RuntimeError:
        published, error = False, True
        for c in CELLS:
            cells[c] = ""
    return cells, published, error


def print_report(rules, cells, published):
    """PrintDevexpress + BindToData: the printed sheet is built from the live cells."""
    if rules == "fixed" and not published:
        return "refused"
    return "printed:" + "|".join(cells[c] for c in CELLS)


fresh = {c: "" for c in CELLS}
leg_a, _p, _e = run("legacy", dict(fresh), PERIOD_A)
fix_a, fix_a_pub, _e = run("fixed", dict(fresh), PERIOD_A)
check("A1 a complete run publishes the same values under both rules",
      leg_a == fix_a and fix_a_pub is True and
      fix_a["txtNetTax"].endswith("(مستحق الدفع للهيئة)    "))
leg_b, _, _ = run("legacy", dict(leg_a), PERIOD_B)
fix_b, fix_b_pub, _ = run("fixed", dict(fix_a), PERIOD_B)
check("A2 a second complete period agrees too, rent returns and expenses included",
      leg_b == fix_b and fix_b_pub is True and fix_b["txtIncomes"] == str(900.0 - 50.0))

mixed, mixed_pub, mixed_err = run("legacy", dict(leg_a), PERIOD_B, fail_at="rent")
check("A3 a late failure used to leave new sales beside the old rent and old VAT net (bug)",
      mixed_err is True and
      mixed["txtNetSale"] == str(round(PERIOD_B["saleBase"] - PERIOD_B["saleRetBase"], 2)) and
      mixed["txtIncomes"] == leg_a["txtIncomes"] and mixed["txtNetTax"] == leg_a["txtNetTax"])
check("A4 and that mixed sheet was printable, because nothing marked it incomplete",
      print_report("legacy", mixed, mixed_pub).startswith("printed:") and
      leg_a["txtNetSales"] in print_report("legacy", mixed, mixed_pub))

inv, inv_pub, inv_err = run("fixed", dict(fix_a), PERIOD_B, fail_at="rent")
check("A5 the repaired run publishes nothing from a partial pass and invalidates the report",
      inv_err is True and inv_pub is False and all(inv[c] == "" for c in CELLS))
check("A6 print and preview refuse that state instead of emitting stale numbers",
      print_report("fixed", inv, inv_pub) == "refused")
rec, rec_pub, _ = run("fixed", dict(inv), PERIOD_B)
check("A7 a later successful run publishes fully again and is printable",
      rec_pub is True and rec == fix_b and print_report("fixed", rec, rec_pub).startswith("printed:"))
check("A8 printing before any successful show is refused too",
      print_report("fixed", dict(fresh), False) == "refused" and
      print_report("legacy", dict(fresh), False).startswith("printed:"))
zero, zero_pub, zero_err = run("fixed", dict(fresh), EMPTY)
check("A9 a known-empty period is a result, not a failure: zeros published and printable",
      zero_err is False and zero_pub is True and zero["txtNetSale"] == "0.0" and
      print_report("fixed", zero, zero_pub).startswith("printed:"))

show = TAX[TAX.index("private void ShowDetails22()"):TAX.index("private void ClearReportCells()")]
gate = TAX[TAX.index("private void PrintDevexpress(int printMode)"):]
check("A10 static: the cells are written in one pass after the last source, with no read-back",
      show.count("SetCellText(txt") == 19 and "SafeDouble(txt" not in TAX and
      show.index("SetCellText(txtNetSale, netSaleVal.ToString());") > show.index("sqlEntry") and
      show.index("_reportPublished = true;") > show.index("SetCellText(txtNetPurchTax"))
check("A11 static: the catch invalidates and clears instead of only reporting the error",
      "_reportPublished = false;" in show and "ClearReportCells();" in show and
      show.index("_reportPublished = false;") < show.index("ClearReportCells();") and
      "لم يُنشر أي جزء منه" in show and
      TAX.count("SetCellText(txtNetSale, string.Empty);") == 1 and TAX.count("string.Empty);") == 19)
check("A12 static: the print gate precedes report building, and the sheet still comes from the cells",
      gate.index("if (!_reportPublished)") < gate.index("RptUrl = MainClass.ReportsPath;") and
      gate.index("if (!_reportPublished)") < gate.index("report.DataSource = BindToData();") and
      "لا يمكن طباعة التقرير أو معاينته قبل عرض نتائج مكتملة ناجحة" in gate and
      TAX.count("GetCellText(txt") == 19 and TAX.count("new SqlDataAdapter") == 12)

print()
print("Part B: R-079 / P7-046 ext. B28 - a failed search source cannot be accepted")


class SearchDialog:
    """frmInvoiceSrch: master snapshot, displayed rows, and the three acceptance paths."""

    def __init__(self, rules):
        self.rules = rules
        self.master = []
        self.display = []
        self.row_index = -1
        self.valid = False
        self.status = ""
        self.log = []

    def load(self, rows, ok=True):
        if self.rules == "legacy":
            self.master = []
        else:
            self.master = []
        if not ok:
            self.log.append("source-failed")
            if self.rules == "fixed":
                self.valid = False
                self.display = []
                self.row_index = -1
                self.status = "load-failed"
            return                                  # legacy: Console.WriteLine only
        self.master = list(rows)
        self.display = list(rows)
        self.status = "count:%d" % len(self.display)
        if self.rules == "fixed":
            self.valid = True

    def select(self, index):
        self.row_index = index

    def accept_enter(self):
        if self.rules == "fixed":
            if not (self.valid and self.row_index > -1 and self.row_index < len(self.display)):
                return None
        else:
            if not (self.row_index > -1 and self.row_index < len(self.display)):
                return None
        return self.display[self.row_index]["InvGlobalID"]

    def accept_double_click(self):
        row = self.display[self.row_index] if 0 <= self.row_index < len(self.display) else None
        if row is None:
            return None
        if self.rules == "fixed" and not self.valid:
            return None
        return row["InvGlobalID"]

    def accept_return_button(self, row):
        if row is None:
            return None
        if self.rules == "fixed" and not self.valid:
            return None
        return row["InvGlobalID"]


ROWS_A = [{"InvGlobalID": "G-1"}, {"InvGlobalID": "G-2"}]
ROWS_B = [{"InvGlobalID": "G-9"}]

leg, fix = SearchDialog("legacy"), SearchDialog("fixed")
leg.load(ROWS_A); fix.load(ROWS_A)
check("B1 a successful load publishes the rows and, in the repaired form, marks them valid",
      leg.display == fix.display == ROWS_A and fix.valid is True and fix.status == "count:2")
leg.select(1); fix.select(1)
check("B2 acceptance works on a valid snapshot under both rules",
      leg.accept_enter() == fix.accept_enter() == "G-2" and
      leg.accept_double_click() == fix.accept_double_click() == "G-2")

stale_row = dict(fix.display[1])
leg.load(ROWS_B, ok=False); fix.load(ROWS_B, ok=False)
check("B3 a failed reload left the previous rows on screen and selectable (bug reproduced)",
      leg.display == ROWS_A and leg.accept_enter() == "G-2" and
      leg.accept_double_click() == "G-2" and leg.accept_return_button(stale_row) == "G-2")
check("B4 the repaired form publishes the failure: no rows, no index, an explicit status",
      fix.display == [] and fix.row_index == -1 and fix.valid is False and
      fix.status == "load-failed")
check("B5 and all three acceptance paths refuse the stale document",
      fix.accept_enter() is None and fix.accept_double_click() is None and
      fix.accept_return_button(stale_row) is None)
fix.load(ROWS_B)
fix.select(0)
check("B6 a later successful load restores acceptance of the NEW snapshot only",
      fix.valid is True and fix.status == "count:1" and fix.accept_enter() == "G-9" and
      fix.accept_return_button({"InvGlobalID": "G-9"}) == "G-9")
empty = SearchDialog("fixed"); empty.load([])
check("B7 a known-empty result stays valid and is not reported as a failure",
      empty.valid is True and empty.status == "count:0" and empty.display == [] and
      empty.accept_enter() is None)
loader = SRCH[SRCH.index("public void LoadInvoices()"):SRCH.index("private void BuildLoadQuery()")]
check("B8 static: validity is set only after the fill, and the catch publishes the failure",
      SRCH.count("adapter.Fill(_masterTable);\n                ApplyFilter();\n                _snapshotValid = true;") == 1 and
      loader.count("_snapshotValid = true;") == 1 and loader.count("_snapshotValid = false;") == 1 and
      loader.count("_displayRows.Clear();") == 1 and loader.count("_rowIndex = -1;") == 1 and
      loader.index("ApplyFilter();") < loader.index("_snapshotValid = true;") and
      loader.index("_snapshotValid = false;") < loader.index("_displayRows.Clear();") and
      SRCH.count("_displayRows.Clear();") == 2 and SRCH.count("_rowIndex = -1;") == 1 and
      "⚠ فشل تحميل نتائج البحث، لا توجد نتائج صالحة للاختيار" in SRCH and
      "⚠ Loading the search results failed; nothing valid to select" in SRCH)
check("B9 static: the three acceptance paths carry the guard",
      SRCH.count("if (_snapshotValid && _rowIndex > -1 && _rowIndex < _displayRows.Count)") == 1 and
      SRCH.count("if (row == null || !_snapshotValid) return;") == 1 and
      SRCH.count("if (!_snapshotValid) return;") == 1 and
      SRCH.count("Repair R-079") == 5)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - the tax report publishes in one pass or not at all and cannot be printed")
print("partial, and a failed search source no longer leaves a stale document selectable.")
sys.exit(0)
