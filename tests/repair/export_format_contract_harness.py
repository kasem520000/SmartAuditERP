# -*- coding: utf-8 -*-
"""Repair R-088 / R-089 / R-090 / R-091 - audit finding P7-050 (Medium, confirmed):
"the purchase export offers XLSX and CSV but writes TSV whichever extension is chosen".

The finding is a contract defect: the save dialog announces a container and the writer produces
another one, so the file on disk is never what its name promises - text under *.xlsx, tabs where a
*.csv reader expects commas, an XML document under a workbook name, an HTML document under *.csv.

Seven evidence files are in scope here:
  frmRptInvPurchaseDetails (R-088 branch + R-091 real workbook), frmRptKhzna and frmTaxInvDetails
  (R-089 announce what is written, R-091 real workbook for the tax screen), frmNkdTotSalePurch,
  frmMezanyaArba7 and frmMezanMorg3a (R-090 real CSV for *.csv, honest label for the HTML *.xls),
  frmItemsalesdetailsPos (R-090 label only - it already branched).

Part A models the contract: what a screen announces, what it writes for each announced option, and
what a reader of that extension expects. Part B witnesses the source. Part C proves the workbook
calls are the project's own already-compiling ClosedXML idiom, not an invented API.

No .NET toolchain exists in this environment, so nothing here is a runtime claim: no workbook, CSV
or HTML file was produced or opened, and no screen was executed.
"""
import io
import os
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


F = "SmartAuditERP/Form_WPF/"
PUR = src(F + "frmRptInvPurchaseDetails.xaml.cs")
KHZ = src(F + "frmRptKhzna.xaml.cs")
TAX = src(F + "frmTaxInvDetails.xaml.cs")
NKD = src(F + "frmNkdTotSalePurch.xaml.cs")
MEZ = src(F + "frmMezanyaArba7.xaml.cs")
TRIAL = src(F + "frmMezanMorg3a.xaml.cs")
POS = src(F + "frmItemsalesdetailsPos.xaml.cs")
WRITER = src("SmartAuditERP/Class/SpreadsheetExport.cs")
PRECEDENT = "".join(src(F + f) for f in
                    ("frmAccountsStatement.xaml.cs", "frmInvDetails.xaml.cs",
                     "frmInvBySalesMen.xaml.cs"))

# ══════════════════════════════ the announced delimited schema ══════════════════════════════
COMMA, TAB, NL, QUOTE = ",", "\t", "\r\n", '"'

WORKBOOK, COMMA_TEXT, TAB_TEXT, HTML_DOC, XML_DOC, NOTHING = (
    "workbook", "comma-separated text", "tab-separated text",
    "HTML document", "XML document", "nothing")

# what a reader expects from an extension, given the label the dialog shows for it
EXPECTS = {".xlsx": WORKBOOK, ".csv": COMMA_TEXT, ".txt": TAB_TEXT,
           ".xls": HTML_DOC, ".xml": XML_DOC}


def encode(cells, delim):
    out = []
    for c in cells:
        c = "" if c is None else str(c)
        if delim in c or QUOTE in c or "\r" in c or "\n" in c:
            c = QUOTE + c.replace(QUOTE, QUOTE + QUOTE) + QUOTE
        out.append(c)
    return delim.join(out)


def write_delimited(header, rows, delim):
    return NL.join([encode(header, delim)] + [encode(r, delim) for r in rows]) + NL


def parse(text, delim):
    records, row, cell = [], [], ""
    quoted = False
    i = 0
    while i < len(text):
        ch = text[i]
        if quoted:
            if ch == QUOTE:
                if i + 1 < len(text) and text[i + 1] == QUOTE:
                    cell += QUOTE
                    i += 1
                else:
                    quoted = False
            else:
                cell += ch
        elif ch == QUOTE:
            quoted = True
        elif ch == delim:
            row.append(cell)
            cell = ""
        elif text.startswith(NL, i):
            row.append(cell)
            cell = ""
            records.append(row)
            row = []
            i += len(NL) - 1
        elif ch == "\n":
            row.append(cell)
            cell = ""
            records.append(row)
            row = []
        else:
            cell += ch
        i += 1
    if cell or row:
        row.append(cell)
        records.append(row)
    return records


def ordered(text, *landmarks):
    """True when every landmark occurs exactly once and in this order. A landmark a mutation
    removed must fail a named check, not raise and hide which witness would have caught it."""
    positions = []
    for mark in landmarks:
        if text.count(mark) != 1:
            return False
        positions.append(text.index(mark))
    return positions == sorted(positions)


def records_of(art, delim):
    """Records of an artifact; a refused export wrote nothing, so it has no records at all."""
    return parse(art["text"], delim) if art.get("text") else []


def rec(records, i, j=None):
    """Safe accessor: a mutation that lost a record or a cell must fail a named check, not raise
    and hide every witness after it."""
    if i >= len(records):
        return None
    if j is None:
        return records[i]
    row = records[i]
    return row[j] if j < len(row) else None


def ext_of(name):
    return os.path.splitext(name)[1].lower()


def artifact(kind, text=None):
    return {"kind": kind, "text": text}


# ── the purchase-details projection: 25 columns, one of them an integer, money already formatted ─
PUR_HEADER = ["AutoIncrementID", "InvoiceTypeTxt", "InvGlobalID", "InvoiceNo", "ReffNo", "InvDate",
              "InvoiceTime", "PaymentTxt", "ClientTxt", "SumPrice", "TotDiscount", "Total", "VAT",
              "Net", "InvertoryName", "BranchTxt", "UserTxt", "ProcType", "Paid", "Remainder",
              "ExtraVAT", "TotalTax", "Paycash", "PayATM", "ExtraVATPerc"]
PUR_ROWS = [
    [7, "مشتريات", "G-1", "101", "", "01/11/2026 09:15 ص", "09:15", "نقداً",
     'شركة "البحر" للتجارة، الحديدة', "1,250.00", "0.00", "1,250.00", "0.00", "1,250.00",
     "المخزن الرئيسي", "الفرع 1", "admin", 1, "1,250.00", "0.00", "0.00", "0.00", "0.00",
     "0.00", "0.00"],
    [8, "مرتجع", "G-2", "102", "101", "02/11/2026 10:20 م", "10:20", "آجل",
     "عميل\tبسطر جديد", "75.50", "5.50", "70.00", "0.00", "70.00",
     "المخزن الرئيسي", "الفرع 1", "cashier", 2, "0.00", "70.00", "0.00", "0.00", "0.00",
     "0.00", "0.00"]]


def purchase_legacy(name, table):
    """Every offered extension landed in the same tab writer."""
    return artifact(TAB_TEXT, write_delimited(table[0], table[1], TAB))


def purchase_fixed(name, table):
    ext = ext_of(name)
    if ext == ".xlsx":
        return artifact(WORKBOOK)
    if ext == ".csv":
        return artifact(COMMA_TEXT, write_delimited(table[0], table[1], COMMA))
    if ext == ".txt":
        return artifact(TAB_TEXT, write_delimited(table[0], table[1], TAB))
    return artifact(NOTHING)          # refused before writing


PUR_TABLE = (PUR_HEADER, PUR_ROWS)

# ── the treasury screen: one writer (comma), eight announced columns ──
KHZ_HEADER = ["م", "العملية", "الرقم", "التاريخ", "وارد", "صادر", "الرصيد", "البيان"]
KHZ_ROWS = [["1", "سند قبض", "55", "01/11/2026", "1,500.00", "0.00", "1,500.00", "دفعة، نقدية"],
            ["2", "سند صرف", "12", "02/11/2026", "0.00", "250.75", "1,249.25", 'مصاريف "نثرية"']]


def khzna_legacy(name, default_ext=None):
    return artifact(COMMA_TEXT, write_delimited(KHZ_HEADER, KHZ_ROWS, COMMA))


def khzna_fixed(name, default_ext=".csv"):
    if not ext_of(name):
        name += default_ext           # the dialog appends DefaultExt to a nameless default
    if ext_of(name) != ".csv":
        return artifact(NOTHING)
    return artifact(COMMA_TEXT, write_delimited(KHZ_HEADER, KHZ_ROWS, COMMA))


# ── the tax screen: nine columns, XML under a workbook name ──
TAX_HEADER = ["نوع الفاتورة", "رقم الفاتورة", "التاريخ", "العميل", "المجموع", "الخصم",
              "الصافي قبل الضريبة", "الضريبة", "الصافي"]
TAX_ROWS = [["مبيعات", "1001", "01/11/2026", "عميل، أول", "1,150.00", "0.00", "1,000.00",
             "150.00", "1,150.00"],
            ["مرتجع", "1002", "02/11/2026", 'عميل "ثانٍ"', "115.00", "0.00", "100.00",
             "15.00", "115.00"]]


def tax_legacy(name):
    return artifact(XML_DOC, "<TaxInvoices>%s</TaxInvoices>" % len(TAX_ROWS))


def tax_fixed(name):
    ext = ext_of(name)
    if ext == ".xlsx":
        return artifact(WORKBOOK)
    if ext == ".csv":
        return artifact(COMMA_TEXT, write_delimited(TAX_HEADER, TAX_ROWS, COMMA))
    return artifact(NOTHING)


# ── the three HTML-table screens ──
NKD_HEADER = ["رقم الصنف", "الصنف", "الكمية (مشتريات)", "الإجمالي (مشتريات)",
              "الكمية (مبيعات)", "الإجمالي (مبيعات)"]
# the row model keeps the legacy property order Column1..Column4, Column6, Column5
NKD_ROWS = [["101", "صنف، أول", "10", "1,000.00", "4", "480.00"],
            ["102", 'صنف "ثانٍ"', "5", "250.50", "0", "0.00"]]
NKD_TOTALS = ["إجمالي المشتريات", "", "", "1,250.50", "إجمالي المبيعات", "480.00"]

MEZ_HEADER = ["الحساب", "إسم الحساب", "رصيد مدين", "رصيد دائن"]
MEZ_ROWS = [["1101", "الصندوق", "5,000.00", "0.00"], ["2101", "الموردون", "0.00", "3,200.75"]]
MEZ_TOTALS = ["الإجمالي", "", "5,000.00", "3,200.75"]

TRIAL_HEADER = ["الحساب", "اسم الحساب", "افتتاحي مدين", "افتتاحي دائن", "رصيد سابق مدين",
                "رصيد سابق دائن", "حركة مدين", "حركة دائن", "رصيد مدين", "رصيد دائن",
                "ختامي مدين", "ختامي دائن"]
TRIAL_DECIMALS = ["1234.5", "0", "75.25"]


def money(value):
    """SpreadsheetExport.Money: invariant, two decimals, no group separator."""
    return "%.2f" % float(value)


def display_n2(value):
    """what the HTML table interpolates with :N2 - grouped, and locale dependent."""
    return "{:,.2f}".format(float(value))


def html_table(headers, body_rows, totals=None):
    out = ["<html><head><meta charset='utf-8'/>", "<body dir='rtl'>", "<table><tr>"]
    out.append("".join("<th>%s</th>" % h for h in headers))
    out.append("</tr>")
    for r in body_rows:
        out.append("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>")
    if totals:
        out.append("<tr>" + "".join("<td>%s</td>" % c for c in totals if c != "") + "</tr>")
    out.append("</table></body></html>")
    return "".join(out)


def html_screen_legacy(name, headers, rows, totals=None):
    """both offered extensions went to the same HTML writer"""
    return artifact(HTML_DOC, html_table(headers, rows, totals))


def html_screen_fixed(name, headers, rows, totals=None):
    ext = ext_of(name)
    if ext == ".csv":
        return artifact(COMMA_TEXT, write_delimited(
            headers, rows + ([totals] if totals else []), COMMA))
    if ext == ".xls":
        return artifact(HTML_DOC, html_table(headers, rows, totals))
    return artifact(NOTHING)


print("Part A: the announced format and the written format")

check("A1 the legacy purchase export wrote tab-separated text under an announced *.xlsx",
      purchase_legacy("فواتير_مشتريات_20261119.xlsx", PUR_TABLE)["kind"] == TAB_TEXT and
      EXPECTS[".xlsx"] == WORKBOOK and
      purchase_legacy("فواتير_مشتريات_20261119.xlsx", PUR_TABLE)["kind"] != EXPECTS[".xlsx"])
legacy_csv_choice = purchase_legacy("report.csv", PUR_TABLE)
legacy_csv_head = legacy_csv_choice["text"].split(NL)[0]
check("A2 and under an announced *.csv it wrote tabs where a CSV reader expects commas",
      legacy_csv_choice["kind"] == TAB_TEXT and EXPECTS[".csv"] == COMMA_TEXT and
      legacy_csv_choice["kind"] != EXPECTS[".csv"] and
      TAB in legacy_csv_head and COMMA not in legacy_csv_head,
      "head=%r" % (legacy_csv_head[:40],))
check("A3 the repaired purchase export gives every announced option a writer of its own",
      all(purchase_fixed(n, PUR_TABLE)["kind"] == EXPECTS[e]
          for n, e in (("report.xlsx", ".xlsx"), ("report.csv", ".csv"), ("report.txt", ".txt"))))
check("A4 a container the screen cannot produce is refused before anything is written",
      all(purchase_fixed(n, PUR_TABLE)["kind"] == NOTHING and
          purchase_fixed(n, PUR_TABLE)["text"] is None
          for n in ("report.xls", "report.pdf", "report.xlsx.bak")))
csv_art = purchase_fixed("report.csv", PUR_TABLE)
txt_art = purchase_fixed("report.txt", PUR_TABLE)
csv_records = records_of(csv_art, COMMA)
check("A5 the three containers carry one and the same projection",
      csv_records == records_of(txt_art, TAB) ==
      [[str(c) for c in h] for h in [PUR_HEADER]] + [[str(c) for c in r] for r in PUR_ROWS],
      "comma=%r" % (rec(csv_records, 1) or [],))
check("A5b a client name holding a comma and a quote survives the comma container as one cell",
      rec(csv_records, 1, 8) == 'شركة "البحر" للتجارة، الحديدة' and
      len(rec(csv_records, 1) or []) == 25)
check("A5c a note holding a tab survives the comma container without adding a column",
      rec(csv_records, 2, 8) == "عميل\tبسطر جديد" and
      len(rec(csv_records, 2) or []) == 25)

check("A6 the legacy treasury export announced *.xlsx as a second option and wrote commas",
      khzna_legacy("حركة_صندوق.xlsx")["kind"] == COMMA_TEXT != EXPECTS[".xlsx"])
check("A6b and its nameless default left the shell to invent an extension",
      ext_of("حركة_صندوق_20261119_0915") == "" and
      khzna_legacy("حركة_صندوق_20261119_0915")["kind"] == COMMA_TEXT)
check("A7 the repaired treasury export announces one format, writes it, and names the default",
      khzna_fixed("حركة_صندوق_20261119_0915")["kind"] == EXPECTS[".csv"] and
      khzna_fixed("حركة_صندوق.csv")["kind"] == EXPECTS[".csv"] and
      parse(khzna_fixed("x.csv")["text"], COMMA)[0] == KHZ_HEADER)

check("A8 the legacy tax export wrote an XML document under an announced *.xlsx",
      tax_legacy("TaxInvoices_Export.xlsx")["kind"] == XML_DOC != EXPECTS[".xlsx"])
tax_csv = tax_fixed("TaxInvoices_Export.csv")
tax_records = records_of(tax_csv, COMMA)
check("A9 the repaired tax export writes a workbook for *.xlsx and commas for *.csv",
      tax_fixed("TaxInvoices_Export.xlsx")["kind"] == EXPECTS[".xlsx"] and
      tax_csv["kind"] == EXPECTS[".csv"])
check("A9b the CSV keeps the nine announced columns and every cell the XML document carried",
      rec(tax_records, 0) == TAX_HEADER and
      rec(tax_records, 1) == TAX_ROWS[0] and
      rec(tax_records, 2, 3) == 'عميل "ثانٍ"' and
      all(len(r) == 9 for r in tax_records))

check("A10 all three HTML-table screens wrote an HTML document under an announced *.csv",
      all(html_screen_legacy("report.csv", h, r, t)["kind"] == HTML_DOC != EXPECTS[".csv"]
          for h, r, t in ((NKD_HEADER, NKD_ROWS, NKD_TOTALS),
                          (MEZ_HEADER, MEZ_ROWS, MEZ_TOTALS),
                          (TRIAL_HEADER, [], None))))
check("A11 repaired, *.csv is a comma file and *.xls keeps the HTML table its label now names",
      all(html_screen_fixed("report.csv", h, r, t)["kind"] == EXPECTS[".csv"] and
          html_screen_fixed("report.xls", h, r, t)["kind"] == EXPECTS[".xls"]
          for h, r, t in ((NKD_HEADER, NKD_ROWS, NKD_TOTALS),
                          (MEZ_HEADER, MEZ_ROWS, MEZ_TOTALS),
                          (TRIAL_HEADER, [], None))))
nkd_csv = html_screen_fixed("report.csv", NKD_HEADER, NKD_ROWS, NKD_TOTALS)
nkd_records = records_of(nkd_csv, COMMA)
check("A12 the cash CSV keeps the HTML column order (sales quantity before sales total)",
      rec(nkd_records, 0) == NKD_HEADER and rec(nkd_records, 1) == NKD_ROWS[0] and
      rec(nkd_records, 1, 4) == "4" and rec(nkd_records, 1, 5) == "480.00")
check("A12b its totals record keeps six cells instead of collapsing into a shorter line",
      len(rec(nkd_records, 3) or []) == 6 and rec(nkd_records, 3) == NKD_TOTALS and
      rec(nkd_records, 3, 1) == "" and rec(nkd_records, 3, 2) == "")
mez_csv = html_screen_fixed("report.csv", MEZ_HEADER, MEZ_ROWS, MEZ_TOTALS)
mez_records = records_of(mez_csv, COMMA)
check("A13 the profit-and-loss CSV keeps four columns and a four-cell totals record",
      rec(mez_records, 0) == MEZ_HEADER and all(len(r) == 4 for r in mez_records) and
      rec(mez_records, 3) == MEZ_TOTALS)
TRIAL_MONEY = TRIAL_DECIMALS * 3 + TRIAL_DECIMALS[:1]        # ten amounts, like the screen
assert len(TRIAL_MONEY) == 10 and len(TRIAL_HEADER) == 12
trial_csv = html_screen_fixed("report.csv", TRIAL_HEADER,
                              [["1101", "الصندوق"] + [money(d) for d in TRIAL_MONEY]], None)
trial_records = records_of(trial_csv, COMMA)
check("A14 the trial-balance CSV leaves money machine-readable while the HTML keeps its display",
      rec(trial_records, 0) == TRIAL_HEADER and len(rec(trial_records, 1) or []) == 12 and
      rec(trial_records, 1, 2) == "1234.50" and rec(trial_records, 1, 3) == "0.00" and
      display_n2("1234.5") == "1,234.50" and
      "<td>1,234.50</td>" in (html_screen_fixed("report.xls", TRIAL_HEADER,
                                                [["1101", "الصندوق", display_n2("1234.5")]],
                                                None)["text"] or ""))
POS_LEGACY_LABEL = "Excel File (*.xls)|*.xls|CSV File (*.csv)|*.csv"
POS_FIXED_LABEL = "Excel File - HTML table (*.xls)|*.xls|CSV File (*.csv)|*.csv"


def pos_screen(name):
    """The POS screen already routed each extension to its own writer, before this batch and after
    it; the only thing that changed is what the *.xls option calls itself."""
    ext = ext_of(name)
    if ext == ".csv":
        return artifact(COMMA_TEXT, write_delimited(MEZ_HEADER, MEZ_ROWS, COMMA))
    if ext == ".xls":
        return artifact(HTML_DOC, html_table(MEZ_HEADER, MEZ_ROWS))
    return artifact(NOTHING)


check("A15 the POS screen already branched, so only its label changed and no artifact moved",
      POS_LEGACY_LABEL != POS_FIXED_LABEL and
      all(pos_screen(n)["kind"] == EXPECTS[ext_of(n)] for n in ("report.csv", "report.xls")) and
      "HTML table" not in POS_LEGACY_LABEL and "HTML table" in POS_FIXED_LABEL)

print()
print("Part B: static witnesses over the seven evidence files")


def between(text, start, end):
    i = text.index(start)
    return text[i:text.index(end, i)]


pur_handler = between(PUR, "private void btnExportExcel_Click", "#endregion")
check("B1 the purchase dialog announces exactly the three containers it can write",
      pur_handler.count('Filter = "Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|"') == 1 and
      pur_handler.count('+ "Text - tab separated (*.txt)|*.txt",') == 1 and
      pur_handler.count('DefaultExt = ".xlsx",') == 1 and
      pur_handler.count(".xlsx\"") >= 1 and
      pur_handler.count("Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv\",\n") == 0)
check("B2 the purchase branch reads the chosen extension before any writer runs",
      ordered(pur_handler, 'bool asCsv = dlg.FileName.EndsWith(".csv"',
              "var dt = BuildDataTableForReport();", "if (asWorkbook)",
              "SpreadsheetExport.WriteDataTable(") and
      pur_handler.count("asCsv ? SpreadsheetExport.CsvDelimiter : SpreadsheetExport.TsvDelimiter")
      == 1)
check("B3 the refusal happens before the table is even built, so no file is left behind",
      ordered(pur_handler, "if (!asCsv && !asText && !asWorkbook)",
              "var dt = BuildDataTableForReport();") and
      pur_handler.count("صيغة غير مدعومة للتصدير") == 1)
check("B3b the workbook branch is the one that runs for *.xlsx, not the delimited writer",
      pur_handler.count("if (asWorkbook)") == 1 and
      ordered(pur_handler, "if (asWorkbook)", "workbook.SaveAs(dlg.FileName);",
              "SpreadsheetExport.WriteDataTable(") and
      pur_handler.count("ClosedXML.Excel.XLWorkbook") == 1)
check("B4 the private tab writer R-082 had delegated to is gone and the shared one is called once",
      PUR.count("ExportDataTableToTsv") == 0 and
      PUR.count("SpreadsheetExport.WriteDataTable(") == 1 and
      PUR.count("sb.AppendLine") == 0)
check("B5 the purchase projection that feeds the printed report is untouched",
      PUR.count("private DataTable BuildDataTableForReport()") == 1 and
      PUR.count('dt.Columns.Add("ExtraVATPerc", typeof(string));') == 1 and
      PUR.count("BuildDataTableForReport()") == 3)

khz_handler = between(KHZ, "var dlg = new Microsoft.Win32.SaveFileDialog", "export.Save();")
check("B6 the treasury dialog announces one format, matching its one writer",
      khz_handler.count('Filter     = "CSV Files (*.csv)|*.csv",') == 1 and
      khz_handler.count('DefaultExt = ".csv",') == 1 and
      KHZ.count("Excel Files (*.xlsx)") == 0 and
      KHZ.count("SpreadsheetExport.Begin(path, SpreadsheetExport.CsvDelimiter)") == 1)
check("B7 the treasury columns and cells did not move",
      KHZ.count('export.Header("م", "العملية", "الرقم", "التاريخ", "وارد", "صادر", "الرصيد", '
                '"البيان");') == 1 and
      KHZ.count("SpreadsheetExport.Money(row.") == 3 and
      KHZ.count("SpreadsheetExport.Text(row.") == 5)

tax_handler = between(TAX, "private void btnExportExcel_Click", "private void btnPreview_Click")
check("B8 the tax screen writes a workbook for *.xlsx and commas for *.csv, and no XML at all",
      TAX.count("WriteXml") == 0 and
      tax_handler.count('Filter      = "Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv",') == 1
      and tax_handler.count('DefaultExt  = ".xlsx",') == 1 and
      tax_handler.count('saveDialog.FileName.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase)')
      == 1 and
      tax_handler.count("workbook.Worksheets.Add(table, ") == 1 and
      tax_handler.count("SpreadsheetExport.WriteDataTable(\n"
                        "                        saveDialog.FileName, table, "
                        "SpreadsheetExport.CsvDelimiter);") == 1)
check("B9 the tax table keeps its nine announced columns and its rows",
      TAX.count("table.Columns.Add(") == 9 and
      TAX.count('var table = new DataTable("TaxInvoices");') == 1 and
      TAX.count("row.DgvNetBeforVat, row.DgvVAT, row.DgvNet);") == 1)

SCREENS = (
    ("Nkd", NKD, 6, "ExportToHtml", "private void PrintDevexpress(int printMode)"),
    ("MezanyaArba7", MEZ, 4, "ExportToExcelHtml", "private void PrintDevexpress(int printMode)"),
    ("MezanMorg3a", TRIAL, 12, "ExportToExcelHtml", "private void LoadPrintSettings()"),
)
for name, text, columns, html_writer, end_landmark in SCREENS:
    handler = between(text, "SaveFileDialog saveDialog = new SaveFileDialog", end_landmark)
    check("B10-%s the dialog labels the HTML option and the branch follows the extension" % name,
          text.count('"Excel File - HTML table (*.xls)|*.xls|CSV File (*.csv)|*.csv"') == 1 and
          handler.count('saveDialog.FileName.EndsWith(".csv", StringComparison.OrdinalIgnoreCase)')
          == 1 and
          handler.count("ExportToCsv(saveDialog.FileName);") == 1 and
          handler.count("%s(saveDialog.FileName);" % html_writer) == 1)
    csv_method = between(text, "private void ExportToCsv(string fileName)", end_landmark)
    check("B11-%s the new CSV writer announces %d columns through the shared writer" % (name, columns),
          text.count("private void ExportToCsv(string fileName)") == 1 and
          csv_method.count("SpreadsheetExport.Begin(fileName, SpreadsheetExport.CsvDelimiter)") == 1
          and csv_method.count("AppendLine") == 0 and csv_method.count("WriteAllText") == 0 and
          csv_method.count("export.Header(") == 1 and
          csv_method.count("export.Save();") == 1)
    check("B12-%s the HTML writer this screen always had is untouched" % name,
          text.count("private void %s(string fileName)" % html_writer) == 1 and
          text.count("File.WriteAllText(fileName, sb.ToString(), Encoding.UTF8);") == 1)

check("B13 the cash CSV writer keeps the sales pair in the HTML order and a six-cell total",
      NKD.count("SpreadsheetExport.Text(row.Column6),") == 1 and
      ordered(NKD, "SpreadsheetExport.Text(row.Column6),",
              "SpreadsheetExport.Text(row.Column5));") and
      NKD.count('export.Row("إجمالي المشتريات", "", "",') == 1 and
      NKD.count('export.Header("رقم الصنف", "الصنف",') == 1)
check("B14 the profit-and-loss CSV writer keeps four columns and a four-cell total",
      MEZ.count('export.Header("الحساب", "إسم الحساب", "رصيد مدين", "رصيد دائن");') == 1 and
      MEZ.count('export.Row("الإجمالي", "",') == 1 and
      MEZ.count("SpreadsheetExport.Text(row.Column5),") == 1)
check("B15 the trial-balance CSV writer keeps twelve columns, text codes and machine money",
      TRIAL.count('export.Header("الحساب", "اسم الحساب",') == 1 and
      TRIAL.count("SpreadsheetExport.Money(row.Tr") == 10 and
      TRIAL.count("SpreadsheetExport.Text(row.TrAccount),") == 1 and
      TRIAL.count("SpreadsheetExport.Text(row.TrAccName),") == 1 and
      TRIAL.count(":N2}</td>") == 10,
      "display formatting stays in the HTML table")
check("B16 the POS screen gained no writer: only the label of the option changed",
      POS.count('"Excel File - HTML table (*.xls)|*.xls|CSV File (*.csv)|*.csv"') == 1 and
      POS.count("private void ExportToCsv(string fileName)") == 1 and
      POS.count("private void ExportToExcelHtml(string fileName)") == 1 and
      POS.count("ExportToExcelHtml") == 2 and
      POS.count("Repair R-090") == 1)

print()
print("Part C: scope, precedent and the untouched shared schema")

tagged = {}
for path in sorted(os.listdir(F)):
    if not path.endswith(".cs"):
        continue
    text = src(F + path)
    hits = [tag for tag in ("R-088", "R-089", "R-090", "R-091")
            if "Repair %s (audit finding P7-050)" % tag in text]
    if hits:
        tagged[path] = hits
check("C1 exactly the seven evidence files carry a P7-050 repair tag",
      sorted(tagged) == sorted(("frmRptInvPurchaseDetails.xaml.cs", "frmRptKhzna.xaml.cs",
                                "frmTaxInvDetails.xaml.cs", "frmNkdTotSalePurch.xaml.cs",
                                "frmMezanyaArba7.xaml.cs", "frmMezanMorg3a.xaml.cs",
                                "frmItemsalesdetailsPos.xaml.cs")),
      "tagged=%s" % (sorted(tagged),))
check("C2 each tag sits where it belongs",
      tagged["frmRptInvPurchaseDetails.xaml.cs"] == ["R-088", "R-091"] and
      tagged["frmRptKhzna.xaml.cs"] == ["R-089"] and
      tagged["frmTaxInvDetails.xaml.cs"] == ["R-089", "R-091"] and
      tagged["frmNkdTotSalePurch.xaml.cs"] == ["R-090"] and
      tagged["frmMezanyaArba7.xaml.cs"] == ["R-090"] and
      tagged["frmMezanMorg3a.xaml.cs"] == ["R-090"] and
      tagged["frmItemsalesdetailsPos.xaml.cs"] == ["R-090"],
      "tagged=%s" % (tagged,))

API_FORMS = ["new ClosedXML.Excel.XLWorkbook()", ".Worksheets.Add(", ".RightToLeft = true;",
             ".Columns().AdjustToContents();", "workbook.SaveAs("]
check("C3 every workbook call used here is the project's own already-compiling ClosedXML idiom",
      all(PRECEDENT.count(form) >= 1 for form in API_FORMS) and
      PUR.count("new ClosedXML.Excel.XLWorkbook()") == 1 and
      TAX.count("new ClosedXML.Excel.XLWorkbook()") == 1 and
      PRECEDENT.count("workbook.Worksheets.Add(dt, ") == 1,
      "missing=%s" % [f for f in API_FORMS if PRECEDENT.count(f) == 0])
check("C4 no new package, no new using and no COM interop entered either screen",
      PUR.count("using ClosedXML") == 0 and TAX.count("using ClosedXML") == 0 and
      PUR.count("GetTypeFromProgID") == 0 and TAX.count("GetTypeFromProgID") == 0 and
      PUR.count("GetTypeFromCLSID") == 0 and TAX.count("GetTypeFromCLSID") == 0)
check("C5 the shared writer and its announced schema were not touched by this batch",
      WRITER.count("Repair R-088") == 0 and WRITER.count("Repair R-089") == 0 and
      WRITER.count("Repair R-090") == 0 and WRITER.count("Repair R-091") == 0 and
      WRITER.count("public const char CsvDelimiter = ',';") == 1 and
      WRITER.count("public const char TsvDelimiter = '\\t';") == 1)
check("C6 the child dialogs of the two screens still open the file the writer produced",
      pur_handler.count("new System.Diagnostics.ProcessStartInfo(dlg.FileName)") == 1 and
      tax_handler.count("Process.Start(new ProcessStartInfo(saveDialog.FileName)") == 1)

print()
if FAILS:
    print("RESULT: FAIL (%d of %d checks)" % (len(FAILS), CHECKS[0]))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - %d checks. Every announced container now has a writer of its own:" % CHECKS[0])
print("a real workbook for *.xlsx, comma CSV for *.csv, tab text for *.txt, and the HTML *.xls")
print("option says what it is; a container a screen cannot produce is refused before writing.")
sys.exit(0)
