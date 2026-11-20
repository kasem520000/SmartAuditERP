#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-074 (audit finding P7-158), R-075 (P7-155),
R-076 (P7-156) and R-077 (P7-157) - the invoice-search slice delivered by audit
slices B27/B28. No .NET/WPF/SQL Server toolchain exists here, so each repair is
validated as a behavioural model of its exact contract (filter re-application,
snapshot criterion, condition composition, allowed-set consumption) plus static
witnesses over the repaired code.

Run: python3 tests/repair/invoice_search_harness.py
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


SRCH = open("SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs", encoding="utf-8").read()
PURC = open("SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs", encoding="utf-8").read()

print("Part A: R-074 / P7-158 - clearing the price ceiling re-applies the filter")

ROWS = [{"id": 1, "Net": 5.0}, {"id": 2, "Net": 20.0}]


def build_filter(min_text="", max_text=""):
    """BuildFilterExpression: a bound is added only when its text parses."""
    conds = []
    try:
        conds.append(("min", float(min_text)))
    except (TypeError, ValueError):
        pass
    try:
        conds.append(("max", float(max_text)))
    except (TypeError, ValueError):
        pass
    return conds


def display(rows, conds):
    out = list(rows)
    for kind, value in conds:
        out = [r for r in out if (r["Net"] >= value if kind == "min" else r["Net"] <= value)]
    return [r["id"] for r in out]


def max_price_edit(rules, rows, shown, text):
    """The TextChanged handler for the ceiling field. Returns the display after the edit."""
    if rules == "legacy":
        if text.strip() == "":
            return shown                                # no branch for the empty case: stale view
        return display(rows, build_filter("", text))
    return display(rows, build_filter("", text))        # applied on every meaningful edit


shown = max_price_edit("legacy", ROWS, display(ROWS, []), "10")
check("A1 a ceiling of 10 narrows the view to the 5-net row under both rules",
      shown == [1] and max_price_edit("fixed", ROWS, display(ROWS, []), "10") == [1])
check("A2 clearing the ceiling used to leave the stale narrowed view (bug reproduced)",
      max_price_edit("legacy", ROWS, shown, "") == [1] and
      max_price_edit("fixed", ROWS, shown, "") == [1, 2])
check("A3 whitespace-only clearing behaves like clearing, and a wider ceiling still works",
      max_price_edit("fixed", ROWS, shown, "   ") == [1, 2] and
      max_price_edit("fixed", ROWS, display(ROWS, []), "30") == [1, 2] and
      max_price_edit("legacy", ROWS, display(ROWS, []), "30") == [1, 2])
handler = SRCH[SRCH.index("private void txtMaxPrice_TextChanged"):
               SRCH.index("private void txtFromDate_SelectedDateChanged")]
check("A4 static: the ceiling handler no longer wraps the re-filter in a non-empty test",
      "Repair R-074 (audit finding P7-158)" in handler and
      handler.count("ApplyFilter();") == 1 and
      handler.rstrip().endswith("}") and
      handler.index("txtMinPrice.Text = \"0\";") < handler.index("ApplyFilter();") and
      "if (!string.IsNullOrWhiteSpace(txtMaxPrice.Text))\n            {" not in handler)

print()
print("Part B: R-075 / P7-155 - the source criterion follows the process selection")

SOURCE = [{"id": 11, "proc_type": 1, "inv_type": 8},
          {"id": 12, "proc_type": 2, "inv_type": 8}]


def load_snapshot(proc_criterion, source=SOURCE):
    """BuildLoadQuery + Fill: the criterion is baked into the SQL, so it bounds the snapshot."""
    if proc_criterion > 0:
        return [r for r in source if r["proc_type"] == proc_criterion]
    return list(source)


def local_filter(snapshot, index):
    """BuildFilterExpression: index 0 is 'All', index n compares proc_type = n."""
    if index > 0:
        return [r["id"] for r in snapshot if r["proc_type"] == index]
    return [r["id"] for r in snapshot]


class Dialog:
    def __init__(self, rules, opening_proc):
        self.rules = rules
        self.ProcType = opening_proc
        self.queries = 0
        self._snapshotProc = -1
        self.snapshot = []

    def window_loaded(self):
        if self.rules == "fixed":
            self._snapshotProc = self.ProcType          # recorded before the programmatic select
        self.select(self.ProcType)                      # cmbProcType.SelectedIndex = ProcType
        self.load()

    def load(self):
        self.queries += 1
        self.snapshot = load_snapshot(self.ProcType)
        if self.rules == "fixed":
            self._snapshotProc = self.ProcType

    def select(self, index):
        if self.rules == "legacy":
            return                                      # only ApplyFilter ran; source untouched
        if index < 0 or index == self._snapshotProc:
            return
        self.ProcType = index
        self.snapshot = []
        self.load()

    def visible(self, index):
        return local_filter(self.snapshot, index)


leg, fix = Dialog("legacy", 2), Dialog("fixed", 2)
leg.window_loaded(); fix.window_loaded()
check("B1 both open on the caller's process, and the fixed one loaded exactly once",
      leg.visible(2) == [12] and fix.visible(2) == [12] and fix.queries == 1)
check("B2 selecting another process used to show an empty grid (bug reproduced)",
      leg.visible(1) == [] and fix.select(1) is None and fix.visible(1) == [11])
check("B3 the item labelled 'All' used to show one process only; now it widens the source",
      leg.visible(0) == [12] and fix.select(0) is None and fix.visible(0) == [11, 12])
check("B4 going back to a specific process re-narrows the reloaded source",
      (fix.select(2), fix.visible(2))[1] == [12] and fix.queries == 4)
d = Dialog("fixed", 2); d.window_loaded(); before = d.queries
d.select(2); d.select(-1)
check("B5 re-selecting the loaded criterion (or no selection) does not re-query",
      d.queries == before)
check("B6 static: the criterion is guarded, the snapshot records it, and the handler reloads",
      SRCH.count("if (ProcType > 0)\n                condClause += $\" and inv.proc_type = {ProcType}\";") == 1 and
      SRCH.count("_snapshotProc") == 5 and
      "Repair R-075 (audit finding P7-155)" in SRCH and
      "if (wanted == _snapshotProc)" in SRCH and
      SRCH.index("_snapshotProc = ProcType;") < SRCH.index("if (cmbProcType.Items.Count > ProcType)") and
      "ProcType = wanted;\n            _masterTable.Clear();\n            LoadInvoices();" in SRCH)

print()
print("Part C: R-076 / P7-156 - the caller's eligibility condition survives dates and Clear")

DOCS = [{"id": 21, "inv_type": 8, "InvoiceStatus": 1, "date": "2026-11-19"},
        {"id": 22, "inv_type": 8, "InvoiceStatus": 0, "date": "2026-11-19"},
        {"id": 23, "inv_type": 8, "InvoiceStatus": 1, "date": "2026-11-01"}]


def run_query(cond, date_from=None, date_to=None, source=DOCS):
    """Model of BuildLoadQuery + the @date parameters: Cond is the caller-visible criterion."""
    out = []
    for r in source:
        if "InvoiceStatus = 1" in cond and r["InvoiceStatus"] != 1:
            continue
        if "@date" in cond and date_from and date_to:
            if not (date_from <= r["date"] <= date_to):
                continue
        out.append(r["id"])
    return out


class TransferDialog:
    """The receive-transfer caller: ProcType 1, InvType 8, Cond += ' AND InvoiceStatus = 1'."""

    def __init__(self, rules):
        self.rules = rules
        self.Cond = " AND InvoiceStatus = 1"
        self._callerCond = ""
        self.dates_enabled = False

    def window_loaded(self):
        if self.rules == "fixed":
            self._callerCond = self.Cond or ""

    def enable_dates(self):
        self.dates_enabled = True

    def change_date(self, day):
        if not self.dates_enabled:
            return None
        if self.rules == "legacy":
            self.Cond = " and inv.date >= @date1 and inv.date <= @date2 "
        else:
            self.Cond = self._callerCond + " and inv.date >= @date1 and inv.date <= @date2 "
        return run_query(self.Cond, day, day)

    def clear(self):
        self.Cond = "" if self.rules == "legacy" else self._callerCond
        return run_query(self.Cond)


leg, fix = TransferDialog("legacy"), TransferDialog("fixed")
leg.window_loaded(); fix.window_loaded()
check("C1 the opening query keeps the caller's eligibility under both rules",
      run_query(leg.Cond) == [21, 23] and run_query(fix.Cond) == [21, 23])
leg.enable_dates(); fix.enable_dates()
check("C2 a date change used to admit the ineligible document (bug reproduced)",
      leg.change_date("2026-11-19") == [21, 22] and fix.change_date("2026-11-19") == [21])
check("C3 the new date bound still filters by day (not an empty handler)",
      fix.change_date("2026-11-01") == [23] and leg.change_date("2026-11-01") == [23])
check("C4 Clear used to drop the eligibility too; now it restores it",
      leg.clear() == [21, 22, 23] and fix.clear() == [21, 23])


class PlainDialog(TransferDialog):
    """A caller that passes no condition: behaviour must not change at all."""

    def __init__(self, rules):
        super().__init__(rules)
        self.Cond = ""


pl, pf = PlainDialog("legacy"), PlainDialog("fixed")
pl.window_loaded(); pf.window_loaded(); pl.enable_dates(); pf.enable_dates()
check("C5 a caller with no condition sees identical results under both rules",
      pl.change_date("2026-11-19") == pf.change_date("2026-11-19") == [21, 22] and
      pl.clear() == pf.clear() == [21, 22, 23])
check("C6 static: both date handlers compose, Clear restores, and the capture precedes the dates",
      SRCH.count('Cond = _callerCond + " and inv.date >= @date1 and inv.date <= @date2 ";') == 2 and
      SRCH.count("Cond                     = _callerCond;") == 1 and
      "Cond = string.Empty;" not in SRCH and
      SRCH.index("_callerCond = Cond ?? string.Empty;") < SRCH.index("txtFromDate.SelectedDate = DateTime.Today;") and
      SRCH.count("Repair R-076 (audit finding P7-156)") == 5)
check("C7 static: the caller that supplies the condition is the transfer receive button",
      open("SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs", encoding="utf-8").read().count(
          'frm.Cond += " AND InvoiceStatus = 1";') == 1)

print()
print("Part D: R-077 / P7-157 - an out-of-set document cannot reach the purchase editor")

INV = [{"id": 31, "inv_type": 1, "InvGlobalID": "G-1", "branch": 5},
       {"id": 32, "inv_type": 20, "InvGlobalID": "G-20", "branch": 5}]


def search_query(inv_type, source=INV):
    """BuildLoadQuery: the 23 branch asks for one exact type, the other branch admits type 20
    beside the requested one. R-077 deliberately does NOT change this allowed set - whether 20
    belongs in a purchase request is the owner's policy (BLK-P7-157); the repair makes the type
    visible and lets the consumer refuse what it did not ask for."""
    if inv_type == 23:
        return [r for r in source if r["inv_type"] == 23]
    return [r for r in source if r["inv_type"] in {inv_type, 20}]


def pick(rows, want_type):
    for r in rows:
        if r["inv_type"] == want_type:
            return r
    return rows[-1]


def consumer(rules, row, requested_type, branch=5):
    """frmInvPurch.btnInvSrch_Click_1: what actually reaches the editor."""
    if rules == "fixed":
        if row.get("SourceInvType", 0) > 0 and row["SourceInvType"] != requested_type:
            return "rejected-with-message"
        lookup = [r for r in INV
                  if r["branch"] == branch and r["inv_type"] == requested_type
                  and r["InvGlobalID"] == row["InvGlobalID"]]
    else:
        lookup = [r for r in INV
                  if r["branch"] == branch and r["InvGlobalID"] == row["InvGlobalID"]]
    if not lookup:
        return "no-row"
    return "loaded-type-%d" % lookup[0]["inv_type"]


def with_source_type(rows):
    return [dict(r, SourceInvType=r["inv_type"]) for r in rows]


leg_rows = search_query(1)
fix_rows = with_source_type(search_query(1))
check("D1 the allowed set is untouched: a purchase request still admits the type-20 document",
      [r["inv_type"] for r in leg_rows] == [1, 20] and
      [r["inv_type"] for r in fix_rows] == [1, 20] and
      all("SourceInvType" not in r for r in leg_rows))
check("D2 picking it used to load a type-20 document into the purchase editor (bug reproduced)",
      consumer("legacy", pick(leg_rows, 20), 1) == "loaded-type-20")
check("D3 the repaired consumer rejects it in the open, and the lookup re-asserts the type",
      consumer("fixed", pick(fix_rows, 20), 1) == "rejected-with-message" and
      consumer("fixed", dict(pick(fix_rows, 20), SourceInvType=0), 1) == "no-row")
check("D4 an in-set pick still loads exactly as before",
      consumer("legacy", pick(leg_rows, 1), 1) == "loaded-type-1" and
      consumer("fixed", pick(fix_rows, 1), 1) == "loaded-type-1")
check("D5 controls: a contract request never includes 20, and a 20 request does not duplicate rows",
      search_query(23) == [] and
      len([r for r in with_source_type(search_query(20)) if r["inv_type"] == 20]) == 1)
check("D6 static: both SELECTs carry the source type and the row model exposes it",
      SRCH.count("inv.inv_type      AS SourceInvType,") == 2 and
      SRCH.count('SourceInvType    = SafeInt(rv["SourceInvType"]),') == 1 and
      SRCH.count("public int      SourceInvType      { get; set; }") == 1 and
      SRCH.count("SelectedInvType = row.SourceInvType;") == 3 and
      SRCH.count("public int    SelectedInvType;") == 1 and
      SRCH.count("SelectedInvType = -1;") == 1)
srch_handler = PURC[PURC.index("private void btnInvSrch_Click_1"):]
check("D7 static: the purchase consumer rejects out-of-set picks and re-asserts its own type",
      "Repair R-077 (audit finding P7-157)" in srch_handler and
      "if (frm.SelectedInvType > 0 && frm.SelectedInvType != this.InvType)" in srch_handler and
      srch_handler.index("if (frm.SelectedInvType > 0") < srch_handler.index("this.Navigate(") and
      '"and inv_type={this.InvType} " +' in srch_handler and
      "المستند المحدد ليس من نوع المستندات التي تفتحها هذه الشاشة" in srch_handler)
check("D8 static: the re-asserted criterion matches this form's own navigation idiom",
      PURC.count("inv_type={this.InvType}") == 7)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - a cleared ceiling widens the view again, the process selection reloads its")
print("source, the caller's eligibility survives dates and Clear, and an out-of-set document is")
print("rejected before it can reach the purchase editor.")
sys.exit(0)
