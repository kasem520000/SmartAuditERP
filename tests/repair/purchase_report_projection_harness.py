#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-080 against audit finding P7-047 (High,
confirmed): the purchase-details report projection put the additional-tax RATE
into the ExtraVAT money column, filled TotalTax/Paycash/PayATM with a literal
zero, and Report.BindToData stamped four summary fields with a constant "0"
even though the rows carried Paid and Remainder.

No .NET/DevExpress/SQL toolchain exists here, so the repair is validated as a
behavioural model of the projection and of the tax accumulation it relies on
(InvoiceOper accumulates Invo.VAT += num + num2, i.e. the persisted tax column
already carries the additional tax), plus static witnesses over the repaired
sources. Mirrors acceptance P7BT-37 and P7BT-38, which cannot be executed here.

Run: python3 tests/repair/purchase_report_projection_harness.py
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


PUR = open("SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs", encoding="utf-8").read()
RPT = open("SmartAuditERP/Class/Report.cs", encoding="utf-8").read()

FMT = "{:,.2f}"


def money(value):
    return FMT.format(value)


# ── the tax accumulation the projection relies on (InvoiceOper, item loop) ──
def accumulate(items, vat_perc, extra_perc, price_inc_vat=False):
    """Returns the header figures persisted to Inv: tax (= VAT), ExtraVAT, Total, Net."""
    sum_price = total = vat = extra = net = 0.0
    for item in items:
        num3 = item["sum"] - item["discount"]          # ItemTotalPrice
        num = num2 = 0.0
        if num3 > 0 and item["vat_perc"] > 0:
            if price_inc_vat:
                num = num3 - num3 / (1.0 + item["vat_perc"] / 100.0)
                num3 -= num
                if item["extra_applied"] and extra_perc > 0:
                    num2 = num3 - num3 / (1.0 + extra_perc / 100.0)
                    num3 -= num2
                item_total = num3
            else:
                if item["extra_applied"] and extra_perc > 0:
                    num2 = num3 * (extra_perc / 100.0)
                num = (num3 + num2) * (item["vat_perc"] / 100.0)
                item_total = num3
        else:
            item_total = num3
        if vat_perc == 0.0:
            num = 0.0
        sum_price += item["sum"]
        net += num3 + num + num2
        extra += num2
        vat += num + num2                               # the persisted tax carries the extra
        total += item_total
    return {"sumPrice": sum_price, "Total": total, "tax": vat,
            "ExtraVAT": extra, "Net": net}


print("Part A: the tax column really carries the additional tax (no double count)")

ACC = accumulate([{"sum": 1000.0, "discount": 0.0, "vat_perc": 15.0, "extra_applied": True}],
                 vat_perc=15.0, extra_perc=5.0)
check("A1 the accumulated tax equals main VAT plus the additional amount",
      abs(ACC["tax"] - (1050.0 * 0.15 + 50.0)) < 1e-9 and abs(ACC["ExtraVAT"] - 50.0) < 1e-9 and
      abs((ACC["tax"] - ACC["ExtraVAT"]) - 157.5) < 1e-9)
ACC_INC = accumulate([{"sum": 1150.0, "discount": 0.0, "vat_perc": 15.0, "extra_applied": True}],
                     vat_perc=15.0, extra_perc=5.0, price_inc_vat=True)
check("A2 and on the prices-include-VAT path too, so tax - extra is the main VAT",
      ACC_INC["ExtraVAT"] > 0 and ACC_INC["tax"] > ACC_INC["ExtraVAT"])


# ── the rows as the loaded result set carries them (select Inv.*) ──
def db_row(base, extra_perc=5.0, cash=0.0, visa=0.0, paid=None, pay_type=1,
           payment_status=1, columns=None):
    items = [{"sum": base, "discount": 0.0, "vat_perc": 15.0, "extra_applied": True}]
    acc = accumulate(items, vat_perc=15.0, extra_perc=extra_perc)
    tot_net = acc["Net"]
    row = {"tax": acc["tax"], "ExtraVAT": acc["ExtraVAT"], "cash": cash, "visa": visa,
           "tot_net": tot_net, "InvTotal": acc["Total"], "sumPrice": acc["sumPrice"],
           "paid": tot_net if paid is None else paid, "pay_type": pay_type,
           "PaymentStatus": payment_status}
    if columns is not None:                       # a result set missing some money columns
        row = {k: v for k, v in row.items() if k in columns}
    return row


def load(row, extra_perc_from_settings):
    """The screen's row model: what the loader keeps, and which columns were unavailable."""
    unavailable = set()

    def amount(source, published):
        """Reads a money column; a result set that does not carry it marks the PUBLISHED
        column unavailable, exactly as the repaired loader does."""
        if source not in row:
            unavailable.add(published)
            return 0.0
        return row[source]

    extra = amount("ExtraVAT", "ExtraVAT")
    tax_total = amount("tax", "TotalTax")
    main_vat = (tax_total - extra) if (tax_total - extra) > 0 else tax_total
    model = {"VAT": tax_total,                      # unchanged: the grid and the five summaries
             "ExtraVAT": extra,
             "TotalTax": main_vat + extra,
             "Paycash": amount("cash", "Paycash"),
             "PayATM": amount("visa", "PayATM"),
             "Paid": row.get("paid", 0.0),
             "Remainder": row.get("paid", 0.0) - row.get("tot_net", 0.0),
             "ExtraVATPerc": extra_perc_from_settings}
    if row.get("pay_type") == 1 and row.get("PaymentStatus") == 1:
        model["Paycash"] = row.get("tot_net", model["Paycash"])   # settled cash invoice
    return model, unavailable


def project_legacy(model):
    """BuildDataTableForReport before the repair."""
    return {"VAT": money(model["VAT"]),
            "ExtraVAT": money(model["ExtraVATPerc"]),   # the RATE in a money column
            "TotalTax": money(0), "Paycash": money(0), "PayATM": money(0),
            "Paid": money(model["Paid"]), "Remainder": money(model["Remainder"])}


def project_fixed(model, unavailable):
    """BuildDataTableForReport after the repair."""
    def cell(value, column):
        return "" if column in unavailable else money(value)
    return {"VAT": money(model["VAT"]),
            "ExtraVAT": cell(model["ExtraVAT"], "ExtraVAT"),
            "TotalTax": cell(model["TotalTax"], "TotalTax"),
            "Paycash": cell(model["Paycash"], "Paycash"),
            "PayATM": cell(model["PayATM"], "PayATM"),
            "ExtraVATPerc": money(model["ExtraVATPerc"]),
            "Paid": money(model["Paid"]), "Remainder": money(model["Remainder"])}


def summaries_legacy(_table):
    return {"SummaryExtraTax": money(0), "SummaryTotalTax": money(0),
            "SummaryPaid": money(0), "SummaryRemainder": money(0)}


def summaries_fixed(table, column):
    """Report.SumColumn: the sum of the same rows, or unavailable - never a constant."""
    key = {"SummaryExtraTax": "ExtraVAT", "SummaryTotalTax": "TotalTax",
           "SummaryPaid": "Paid", "SummaryRemainder": "Remainder"}[column]
    if not table or key not in table[0]:
        return ""
    total = 0.0
    for projected in table:
        try:
            total += float(projected[key].replace(",", ""))
        except ValueError:
            return ""
    return money(round(total, 2))


print()
print("Part B: P7BT-37 - one additional rate, two different amounts, documented payments")

ROWS = [db_row(100.0, cash=105.0), db_row(200.0, visa=240.0, pay_type=2, payment_status=0)]
MODELS = [load(r, 5.0) for r in ROWS]
LEG = [project_legacy(m) for m, _ in MODELS]
FIX = [project_fixed(m, u) for m, u in MODELS]

check("B1 the legacy sheet published the rate as a money amount: 5.00 for both invoices",
      LEG[0]["ExtraVAT"] == "5.00" and LEG[1]["ExtraVAT"] == "5.00")
check("B2 the repaired sheet publishes the amounts 5.00 and 10.00, and keeps the rate in its own column",
      FIX[0]["ExtraVAT"] == "5.00" and FIX[1]["ExtraVAT"] == "10.00" and
      FIX[0]["ExtraVATPerc"] == "5.00" and FIX[1]["ExtraVATPerc"] == "5.00")
check("B3 the two invoices are no longer indistinguishable in the money column",
      FIX[0]["ExtraVAT"] != FIX[1]["ExtraVAT"] and LEG[0]["ExtraVAT"] == LEG[1]["ExtraVAT"])
check("B4 total tax is main + additional instead of a zero beside a positive VAT",
      LEG[0]["TotalTax"] == "0.00" and FIX[0]["TotalTax"] == money(MODELS[0][0]["VAT"]) and
      FIX[1]["TotalTax"] == money(MODELS[1][0]["VAT"]) and FIX[0]["TotalTax"] != "0.00")
check("B5 payments come from the source: cash on the settled cash invoice, network on the card one",
      LEG[0]["Paycash"] == "0.00" and LEG[1]["PayATM"] == "0.00" and
      FIX[0]["Paycash"] == money(ROWS[0]["tot_net"]) and FIX[0]["PayATM"] == "0.00" and
      FIX[1]["PayATM"] == "240.00")
SETTLED = db_row(100.0, cash=30.0, pay_type=1, payment_status=1)
UNSETTLED = db_row(100.0, cash=30.0, pay_type=1, payment_status=0)
check("B6 the settled-cash rule matches the sibling screens, and an unsettled one keeps its cash column",
      project_fixed(*load(SETTLED, 5.0))["Paycash"] == money(SETTLED["tot_net"]) and
      project_fixed(*load(UNSETTLED, 5.0))["Paycash"] == "30.00" and
      project_legacy(load(SETTLED, 5.0)[0])["Paycash"] == "0.00")

print()
print("Part C: P7BT-38 - summaries from the same rows, with their own signs")

MIXED = [db_row(100.0, cash=105.0, paid=105.0), db_row(200.0, visa=240.0, pay_type=2,
         payment_status=0, paid=100.0), db_row(-50.0, cash=-52.5, paid=-52.5, pay_type=1,
         payment_status=0)]
MIXED_MODELS = [load(r, 5.0) for r in MIXED]
LEG_TABLE = [project_legacy(m) for m, _ in MIXED_MODELS]
FIX_TABLE = [project_fixed(m, u) for m, u in MIXED_MODELS]
LEG_SUMS = summaries_legacy(LEG_TABLE)
FIX_SUMS = {k: summaries_fixed(FIX_TABLE, k) for k in
            ("SummaryExtraTax", "SummaryTotalTax", "SummaryPaid", "SummaryRemainder")}

expected_extra = money(sum(m["ExtraVAT"] for m, _ in MIXED_MODELS))
expected_total = money(sum(m["TotalTax"] for m, _ in MIXED_MODELS))
expected_paid = money(sum(m["Paid"] for m, _ in MIXED_MODELS))
expected_remainder = money(sum(m["Remainder"] for m, _ in MIXED_MODELS))
check("C1 the legacy sheet stamped four constant zeros over non-zero details",
      LEG_SUMS == {"SummaryExtraTax": "0.00", "SummaryTotalTax": "0.00",
                   "SummaryPaid": "0.00", "SummaryRemainder": "0.00"} and
      any(float(p["Paid"].replace(",", "")) != 0 for p in LEG_TABLE))
check("C2 the repaired summaries are the sums of the very rows published, signs included",
      FIX_SUMS["SummaryExtraTax"] == expected_extra and
      FIX_SUMS["SummaryTotalTax"] == expected_total and
      FIX_SUMS["SummaryPaid"] == expected_paid and
      FIX_SUMS["SummaryRemainder"] == expected_remainder)
check("C3 a return row keeps its sign, so the totals are not a sum of absolutes",
      float(FIX_TABLE[2]["Paid"].replace(",", "")) < 0 and
      float(FIX_SUMS["SummaryPaid"].replace(",", ""))
      == round(sum(float(p["Paid"].replace(",", "")) for p in FIX_TABLE), 2))
check("C4 the five primary summaries still come from the screen labels, untouched by this repair",
      PUR.count("sumTotal: lblSumTotal.Text,") == 1 and
      PUR.count("sumNetFinal: lblSumNetFinal.Text);") == 1 and
      RPT.count("Sum = sumTotal,") == 1 and RPT.count("NetTotal = sumNetFinal,") == 1)

print()
print("Part D: unavailable is published as unavailable, never as an invented number")

PARTIAL = db_row(100.0, cash=105.0, columns={"tax", "ExtraVAT", "paid", "tot_net",
                                             "pay_type", "PaymentStatus", "InvTotal"})
P_MODEL, P_UNAVAIL = load(PARTIAL, 5.0)
P_FIX = project_fixed(P_MODEL, P_UNAVAIL)
check("D1 a result set without the payment columns records them unavailable",
      P_UNAVAIL == {"Paycash", "PayATM"} and P_FIX["Paycash"] == "" and P_FIX["PayATM"] == "")
check("D2 the legacy projection published a fabricated 0.00 for the same missing columns",
      project_legacy(P_MODEL)["Paycash"] == "0.00" and project_legacy(P_MODEL)["PayATM"] == "0.00")
check("D3 the columns that were loaded still publish their real amounts",
      P_FIX["ExtraVAT"] == "5.00" and P_FIX["TotalTax"] == money(P_MODEL["VAT"]))
check("D4 a summary over a table missing the column is unavailable, not zero",
      summaries_fixed([{"ExtraVAT": "5.00"}], "SummaryPaid") == "" and
      summaries_fixed([], "SummaryPaid") == "")
check("D5 a cell that is not a number makes the summary unavailable instead of a partial total",
      summaries_fixed([{"Paid": "105.00"}, {"Paid": ""}], "SummaryPaid") == "" and
      summaries_fixed([{"Paid": "105.00"}, {"Paid": "50.00"}], "SummaryPaid") == "155.00")

print()
print("Part E: static witnesses over the repaired sources")

_loader_start = PUR.index("invoiceTxt.TotDiscount = invoiceTxt.InvDiscount;")
loader = PUR[_loader_start:PUR.index("// التواريخ", _loader_start)]
builder = PUR[PUR.index("private DataTable BuildDataTableForReport()"):
              PUR.index("private void btnExportExcel_Click")]
check("E1 the loader reads the amounts from the row and derives the total tax",
      loader.count('ReadAmount(row, "ExtraVAT", out bool extraKnown)') == 1 and
      loader.count('ReadAmount(row, "tax", out bool totalTaxKnown)') == 1 and
      loader.count("invoiceTxt.TotalTax = mainVat + extraAmount;") == 1 and
      loader.count("double mainVat = (taxTotal - extraAmount) > 0") == 1 and
      loader.count('ReadAmount(row, "cash", out bool cashKnown)') == 1 and
      loader.count('ReadAmount(row, "visa", out bool atmKnown)') == 1 and
      loader.count('ReadInt(row, "PaymentStatus") == 1') == 1)
check("E2 the projection publishes amounts and keeps the rate in its own named column",
      'AmountText(row.ExtraVAT, "ExtraVAT")' in builder and
      'AmountText(row.TotalTax, "TotalTax")' in builder and
      'AmountText(row.Paycash, "Paycash")' in builder and
      'AmountText(row.PayATM, "PayATM")' in builder and
      builder.count("row.ExtraVATPerc.ToString(fmt));") == 1 and
      builder.count('dt.Columns.Add("ExtraVATPerc", typeof(string));') == 1 and
      '"0", "0", "0");' not in PUR and
      builder.index('dt.Columns.Add("ExtraVATPerc"') > builder.index('dt.Columns.Add("PayATM"'))
check("E3 unavailability is tracked per load and published as an empty cell",
      PUR.count("_unavailableAmountColumns") == 7 and
      PUR.count("_unavailableAmountColumns.Clear();") == 1 and
      PUR.count("? string.Empty\n                : value.ToString(Common.DigitsNo ?? \"N2\");") == 1 and
      PUR.count("private static double ReadAmount(DataRow row, string column, out bool known)") == 1)
check("E4 the query and the rate assignment the grid binds are untouched",
      PUR.count('"select Inv.*,"') == 1 and
      PUR.count("ExtraVATPerc = invoiceObj.AdditionalTax,") == 1 and
      PUR.count("VAT = Convert.ToDouble(row[\"tax\"]),") == 1)
binder = RPT[RPT.index("public DataSet BindToData(\n            DataTable dt,"):]
check("E5 the four summaries are derived from the rows and the constants are gone",
      binder.count('SumColumn(dt, "ExtraVAT")') == 1 and
      binder.count('SumColumn(dt, "TotalTax")') == 1 and
      binder.count('SumColumn(dt, "Paid")') == 1 and
      binder.count('SumColumn(dt, "Remainder")') == 1 and
      "SummaryExtraTax = sumExtraTax," in binder and
      "SummaryRemainder = sumRemainder," in binder and
      'SummaryExtraTax = "0",' not in RPT and 'SummaryPaid = "0",' not in RPT)
check("E6 the sum helper refuses a missing column and a non-numeric cell, and rounds like the sheet",
      RPT.count("private static string SumColumn(DataTable dt, string column)") == 1 and
      RPT.count("if (dt == null || !dt.Columns.Contains(column)) return string.Empty;") == 1 and
      RPT.count("NumberStyles.Any,\n                        CultureInfo.CurrentCulture, out double value)") == 1 and
      RPT.count("return Math.Round(sum, 2).ToString(Common.DigitsNo ?? \"N2\");") == 1 and
      RPT.count("using System.Globalization;") == 1)
check("E7 the grid-based overload other screens use is untouched",
      RPT.count('inventoryData.SummaryExtraTax = GridView1.Columns["ExtraVAT"].SummaryText;') == 1 and
      RPT.count('inventoryData.SummaryPaid = GridView1.Columns["Paid"].SummaryText;') == 1 and
      RPT.count("Repair R-080") == 2 and PUR.count("Repair R-080") == 7)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - the purchase report projects amounts with explicit units, derives its")
print("summaries from the same rows, and publishes unavailable data as unavailable.")
sys.exit(0)
