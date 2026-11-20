#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-070 (audit finding P7-030), R-071 (P7-031),
R-072 (P7-027) and R-073 (P7-028). No .NET/WPF/DevExpress toolchain exists in
this workspace, so each repair is validated as a behavioural model of its exact
contract (copy-count dispatch, outcome propagation, the WPF ItemsSource rule,
parameter binding round-trip) plus static witnesses over the repaired code.

Run: python3 tests/repair/print_employee_harness.py
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


PRINT = open("SmartAuditERP/Class/Print.cs", encoding="utf-8").read()
REPORT = open("SmartAuditERP/Class/Report.cs", encoding="utf-8").read()
INVS = open("SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs", encoding="utf-8").read()
RESV = open("SmartAuditERP/Form_WPF/FrmReseved.xaml.cs", encoding="utf-8").read()
EMPS = open("SmartAuditERP/Form_WPF/frmEmployees.xaml.cs", encoding="utf-8").read()
ENTS = open("SmartAuditERP/Class/EntityOperations.cs", encoding="utf-8").read()

print("Part A: R-070 / P7-030 - the requested copy count is honoured")


def engine(rules, type_, print_no, kitchen=""):
    """Model Print.Printing's output selection. Returns the emitted outputs."""
    out = []
    if rules == "legacy":
        if type_ == 1 and print_no > 0:                 # count guarded the whole branch
            out.append("print")
            for _ in range(2, print_no + 1):
                out.append("print")
            if kitchen != "":
                out.append("kitchen")
        elif type_ == 2:
            out.append("preview")
        else:                                           # type 1 with print_no <= 0 landed here
            out.append("print")
    else:
        if type_ == 1:
            for _ in range(1, print_no + 1):            # 1..PrintNo, so <= 0 emits nothing
                out.append("print")
            if print_no > 0 and kitchen != "":
                out.append("kitchen")
        elif type_ == 2:
            out.append("preview")
        else:
            out.append("print")
    return out


check("A1 a zero copy count used to print one copy anyway (bug reproduced)",
      engine("legacy", 1, 0) == ["print"] and engine("fixed", 1, 0) == [])
check("A2 a negative copy count used to print one copy too; now it prints nothing",
      engine("legacy", 1, -3) == ["print"] and engine("fixed", 1, -3) == [])
check("A3 positive counts are unchanged: exactly PrintNo copies, kitchen copy included",
      all(engine("legacy", 1, n) == engine("fixed", 1, n) == ["print"] * n for n in (1, 2, 5)) and
      engine("legacy", 1, 3, "K1") == engine("fixed", 1, 3, "K1") == ["print"] * 3 + ["kitchen"])
check("A4 preview and the other report types keep their single output under both rules",
      engine("legacy", 2, 0) == engine("fixed", 2, 0) == ["preview"] and
      engine("legacy", 2, 4) == engine("fixed", 2, 4) == ["preview"] and
      engine("legacy", 3, 0) == engine("fixed", 3, 0) == ["print"] and
      engine("legacy", 0, 0) == engine("fixed", 0, 0) == ["print"])
check("A5 no kitchen copy is produced when the main request printed nothing",
      engine("fixed", 1, 0, "K1") == [] and engine("legacy", 1, 0, "K1") == ["print"])
check("A6 static: the count guard is gone, the loop starts at 1, the kitchen copy follows a real print",
      "if (type == 1 && PrintNo > 0)" not in PRINT and
      "\t\t\t\tif (type == 1)\n" in PRINT and
      PRINT.count("for (int i = 1; i <= PrintNo; i = checked(i + 1))") == 1 and
      "if (PrintNo > 0 && Operators.CompareString(kitchenprinter" in PRINT and
      "Repair R-070 (audit finding P7-030)" in PRINT)
check("A7 static: the in-repo precedent it now matches (Report.Printing loops 1..PrintNo)",
      REPORT.count("for (int i = 1; i <= PrintNo; i = checked(i + 1))") == 1)

print()
print("Part B: R-071 / P7-031 - the engine reports its outcome instead of swallowing it")


def printing(rules, template_ok, printer_ok, kitchen_requested=False, kitchen_ok=True):
    """Model the engine plus what its caller can observe. Returns (result, logs, message)."""
    logs, message = [], None
    try:
        if not template_ok:
            raise RuntimeError("template rptInvSales.repx not found")
        if not printer_ok:
            raise RuntimeError("printer offline")
        if kitchen_requested and not kitchen_ok:
            raise RuntimeError("kitchen printer offline")
        ok = True
    except RuntimeError as ex:
        ok = False
        if rules == "fixed":
            logs.append("Print engine  " + str(ex))
    result = ok if rules == "fixed" else None           # void engine: nothing to observe
    if rules == "fixed" and not ok:
        message = "print-failure-shown"
    return result, logs, message


leg = printing("legacy", template_ok=False, printer_ok=True)
fix = printing("fixed", template_ok=False, printer_ok=True)
check("B1 a missing template looked like success to the caller and left no trace (bug reproduced)",
      leg == (None, [], None) and fix[0] is False and len(fix[1]) == 1 and fix[2] == "print-failure-shown")
check("B2 a printer failure is reported and logged too, and the happy path still reports success",
      printing("fixed", True, False)[0] is False and len(printing("fixed", True, False)[1]) == 1 and
      printing("fixed", True, True) == (True, [], None) and
      printing("legacy", True, True)[0] is None)
check("B3 a kitchen-copy failure is part of the request's outcome, not dropped",
      printing("fixed", True, True, kitchen_requested=True, kitchen_ok=False)[0] is False and
      printing("fixed", True, True, kitchen_requested=True, kitchen_ok=True)[0] is True and
      printing("legacy", True, True, kitchen_requested=True, kitchen_ok=False)[0] is None)
check("B4 static: bool signature, logger field, logged and returned failure",
      PRINT.count("public bool Printing(int type, DataSet ds, string RptUrl, string RptName, "
                  "string defPrinter, string kitchenprinter, int PrintNo)") == 1 and
      "public void Printing(" not in PRINT and
      "using log4net;" in PRINT and
      "private static readonly ILog Logger = LogManager.GetLogger(Environment.MachineName);" in PRINT and
      'Logger.Error("Print engine  " + projectError.Message + " " + MainClass.UserName);' in PRINT and
      "return kitchenDone;" in PRINT and PRINT.count("return false;") >= 1)
check("B5 static: the logger idiom matches the one already used in InvoiceOper",
      open("SmartAuditERP/Class/InvoiceOper.cs", encoding="utf-8").read().count(
          "private static readonly ILog Logger = LogManager.GetLogger(Environment.MachineName);") == 1)
inv_tail = INVS[INVS.index("private void RptPrint(Invoice inv, int type)"):]
res_tail = RESV[RESV.index("private void RptPrint(int printType)"):]
check("B6 static: both cited callers consume the outcome and tell the user on failure",
      "if (!print.Printing(type," in inv_tail and
      inv_tail.index("if (!print.Printing(type,") < inv_tail.index("فشلت الطباعة") and
      "if (!_print.Printing(printType, BindToData(), _print.RptUrl," in res_tail and
      res_tail.index("if (!_print.Printing(printType") < res_tail.index("فشلت الطباعة") and
      "Repair R-071 (audit finding P7-031)" in inv_tail and
      "Repair R-071 (audit finding P7-031)" in res_tail)
check("B7 static: the pre-flight validation messages still return before the engine is called",
      inv_tail.index("لا توجد عمليات بالجدول") < inv_tail.index("if (!print.Printing(type,") and
      res_tail.index("لا يمكنك الطباعة قبل الحفظ") < res_tail.index("if (!_print.Printing(printType"))

print()
print("Part C: R-072 / P7-027 - a bound DataGrid is not edited through Items")


class ItemsSourceInUse(Exception):
    pass


class Grid:
    """WPF rule: Items.Clear()/Items.Add() throw once ItemsSource is set."""

    def __init__(self):
        self.source = None
        self.direct = []

    def items_clear(self):
        if self.source is not None:
            raise ItemsSourceInUse("Operation is not valid while ItemsSource is in use.")
        self.direct = []

    def items_add(self, row):
        if self.source is not None:
            raise ItemsSourceInUse("Operation is not valid while ItemsSource is in use.")
        self.direct.append(row)

    def bind(self, rows):
        self.source = rows

    def rows(self):
        return list(self.source) if self.source is not None else list(self.direct)


def load_branches(grid, bound, branch_count=1):
    """LoadBranches: fills the bound list with the default row and re-binds it."""
    del bound[:]
    if branch_count > 0:
        bound.append({"branch": 1})
    grid.source = None
    grid.bind(bound)


def clear_form(rules, grid, bound):
    """ClearForm: returns the resets that actually got applied."""
    applied = ["fields", "combos", "dates"]
    if rules == "legacy":
        grid.items_clear()                              # throws once bound; nothing below runs
    else:
        del bound[:]
        grid.source = None
        grid.bind(bound)
    load_branches(grid, bound)
    applied += ["record-indicators"]
    return applied


def load_employee(rules, grid, bound, db_branches):
    """The load path: its try/catch swallows whatever the Items contract throws."""
    try:
        if rules == "legacy":
            grid.items_clear()
            for row in db_branches:
                grid.items_add(row)
        else:
            del bound[:]
            for row in db_branches:
                bound.append(row)
            grid.source = None
            grid.bind(bound)
    except ItemsSourceInUse:
        pass                                            # catch { /* ignore */ }
    return grid.rows()


def save_branches(grid):
    """The save path reads BranchRowData out of dgvBranches.Items."""
    return [r["branch"] for r in grid.rows() if r["branch"] > 0]


g_leg, b_leg = Grid(), []
load_branches(g_leg, b_leg)                             # first load binds the source
leg_clear = None
try:
    leg_clear = clear_form("legacy", g_leg, b_leg)
except ItemsSourceInUse:
    leg_clear = "aborted"
g_fix, b_fix = Grid(), []
load_branches(g_fix, b_fix)
fix_clear = clear_form("fixed", g_fix, b_fix)
check("C1 ClearForm aborted on every call after the first bind, leaving indicators stale (bug)",
      leg_clear == "aborted" and fix_clear == ["fields", "combos", "dates", "record-indicators"])

db = [{"branch": 2}, {"branch": 5}, {"branch": 7}]
g2, b2 = Grid(), []
load_branches(g2, b2)
shown_leg = load_employee("legacy", g2, b2, db)
g3, b3 = Grid(), []
load_branches(g3, b3)
shown_fix = load_employee("fixed", g3, b3, db)
check("C2 an existing employee's branches were never displayed (the throw was swallowed)",
      shown_leg == [{"branch": 1}] and shown_fix == db)
check("C3 the save below then persisted the wrong membership: one default row instead of three",
      save_branches(g2) == [1] and save_branches(g3) == [2, 5, 7])
g4, b4 = Grid(), []
load_branches(g4, b4)
load_employee("fixed", g4, b4, db)
second = load_employee("fixed", g4, b4, [{"branch": 9}])
check("C4 loading a second employee replaces the rows instead of appending to the shared list",
      second == [{"branch": 9}] and save_branches(g4) == [9])
check("C5 static: no Items.Clear/Items.Add on the bound grid; three bind-after-clear sites remain",
      "dgvBranches.Items.Clear()" not in EMPS and "dgvBranches.Items.Add(" not in EMPS and
      EMPS.count("dgvBranches.ItemsSource = null;") == 3 and
      EMPS.count("dgvBranches.ItemsSource = _employeeBranches;") == 3 and
      EMPS.count("_employeeBranches.Clear();") == 3 and
      EMPS.count("Repair R-072 (audit finding P7-027)") == 2)
check("C6 static: the save path still enumerates the grid items it always read",
      EMPS.count("foreach (var item in dgvBranches.Items)") == 1 and
      EMPS.index("foreach (var item in dgvBranches.Items)") > EMPS.index("Repair R-072"))

print()
print("Part D: R-073 / P7-028 - the food allowance survives a save")


def bind_employee_params(rules, emp):
    """EntityOperations.SaveEmployee parameter binding for the allowance columns."""
    return {
        "@salary_basic": emp.get("Salary", 0),
        "@house": emp.get("Housing", 0),
        "@travel": emp.get("Travel", 0),
        "@salary_other": emp.get("salary_other", 0),
        "@food": 0 if rules == "legacy" else emp.get("Living", 0),
        "@medical": 0,                                   # still a barrier: BLK-P7-028
        "@salary_add": 0,                                # still a barrier: BLK-P7-028
        "@notes": "",                                    # still a barrier: BLK-P7-028
    }


def screen_save_roundtrip(rules, stored_food, typed_food):
    """Load -> edit the screen -> save -> reload. Returns the persisted food column."""
    employee = {"Salary": 4000, "Housing": 500, "Travel": 200, "salary_other": 100,
                "Living": typed_food}                    # form maps Living = ToDecimal(txtFood.Text)
    params = bind_employee_params(rules, employee)
    return params["@food"], {k: params[k] for k in ("@house", "@travel", "@salary_other")}


leg_food, leg_others = screen_save_roundtrip("legacy", stored_food=250, typed_food=300)
fix_food, fix_others = screen_save_roundtrip("fixed", stored_food=250, typed_food=300)
check("D1 saving zeroed the typed food allowance while the mapped allowances survived (bug)",
      leg_food == 0 and fix_food == 300 and
      leg_others == fix_others == {"@house": 500, "@travel": 200, "@salary_other": 100})
check("D2 a caller that supplies no Living (sync DTO default) behaves exactly as before",
      bind_employee_params("fixed", {"Salary": 0, "Housing": 0, "Travel": 0,
                                     "salary_other": 0, "Living": 0})["@food"] ==
      bind_employee_params("legacy", {"Salary": 0, "Housing": 0, "Travel": 0,
                                      "salary_other": 0, "Living": 0})["@food"] == 0)
check("D3 the residual columns are untouched and named as a barrier, not silently 'fixed'",
      bind_employee_params("fixed", {"Living": 7})["@medical"] == 0 and
      bind_employee_params("fixed", {"Living": 7})["@salary_add"] == 0 and
      bind_employee_params("fixed", {"Living": 7})["@notes"] == "")
check("D4 static: the parameter takes the model value and the statement arity is unchanged",
      ENTS.count('sqlCommand.Parameters.Add("@food", SqlDbType.Float).Value = employee.Living;') == 1 and
      '("@food", SqlDbType.Float).Value = 0;' not in ENTS and
      ENTS.count("@food") == 4 and ENTS.count("food=@food") == 2 and
      ENTS.count("medical=@medical") == 2 and ENTS.count("salary_add=@salary_add") == 2 and
      "Repair R-073 (audit finding P7-028)" in ENTS and "BLK-P7-028" in ENTS)
check("D5 static: the screen still maps the food textbox into Living, and loads it back",
      EMPS.count("Living = ToDecimal(txtFood.Text),") == 1 and
      EMPS.count('txtFood.Text = reader["food"].ToString();') == 1)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - copy counts are honoured, print failures reach the caller, the bound")
print("branch grid is edited through its source, and the food allowance survives a save.")
sys.exit(0)
