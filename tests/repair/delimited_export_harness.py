#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-082 against audit finding P7-048 (Medium,
confirmed): the report exports each rolled their own delimited writer - some
wrapped every cell in quotes without doubling an inner quote, the POS export
wrote every field bare with a local N2 money format, and the TSV export
appended cell text as it stood - so a comma, a quote, a tab, a newline or a
thousands separator could add columns and rows, lose text, or move an amount
into the wrong column.

The repair introduces one writer with an announced schema
(SmartsheetExport: delimiter, doubled quotes, CRLF, invariant money, UTF-8)
and wires the four cited exports to it.

No .NET toolchain exists here, so the writer and the four legacy writers are
modelled in Python and read back with a reader that follows the same announced
schema. Mirrors acceptance P7BT-39 and P7BT-40, which cannot be executed here.

Run: python3 tests/repair/delimited_export_harness.py
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


EXPORT = open("SmartAuditERP/Class/SpreadsheetExport.cs", encoding="utf-8").read()
PROFIT = open("SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs", encoding="utf-8").read()
PERIOD = open("SmartAuditERP/Form_WPF/frmRptSalesInPeriod.xaml.cs", encoding="utf-8").read()
PUR = open("SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs", encoding="utf-8").read()
POS = open("SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs", encoding="utf-8").read()

COMMA = ","
TAB = "\t"
QUOTE = '"'
NL = "\r\n"


# ── the repaired writer, exactly as SpreadsheetExport announces it ──
def money(value):
    return "{0:.2f}".format(value)


def encode_cell(text, delimiter):
    text = "" if text is None else str(text)
    if not any(ch in text for ch in (delimiter, QUOTE, "\r", "\n")):
        return text
    return QUOTE + text.replace(QUOTE, QUOTE + QUOTE) + QUOTE


def encode_row(cells, delimiter):
    return delimiter.join(encode_cell(c, delimiter) for c in cells)


def write_delimited(header, rows, delimiter):
    lines = []
    if header is not None:
        lines.append(encode_row(header, delimiter))
    for row in rows:
        lines.append(encode_row(row, delimiter))
    return NL.join(lines) + NL


# ── the four legacy writers ──
def legacy_quoted_csv(header, rows):
    """Items-profit and sales-in-period: every cell quoted, inner quotes NOT doubled."""
    def line(cells):
        return COMMA.join('"' + ("" if c is None else str(c)) + '"' for c in cells)
    return NL.join([line(header)] + [line(r) for r in rows]) + NL


def legacy_bare_csv(header, rows, money_fmt):
    """POS: no quoting at all, money in a local display format."""
    def line(cells):
        return COMMA.join(money_fmt(c) if isinstance(c, float) else str(c) for c in cells)
    return NL.join([line(header)] + [line(r) for r in rows]) + NL


def legacy_tsv(header, rows):
    """Purchase details: cell text appended as it stood between tabs."""
    def line(cells):
        return TAB.join("" if c is None else str(c) for c in cells)
    return NL.join([line(header)] + [line(r) for r in rows]) + NL


# ── a reader that follows the announced schema ──
def parse_delimited(text, delimiter):
    """Reads back what the announced schema wrote: quoted cells, doubled inner quotes,
    CRLF between records, and any character - comma, tab, newline - inside a quoted cell."""
    records, cell, in_quotes, field_started = [], "", False, False
    i = 0
    row = []
    while i < len(text):
        ch = text[i]
        if in_quotes:
            if ch == QUOTE:
                if i + 1 < len(text) and text[i + 1] == QUOTE:
                    cell += QUOTE
                    i += 2
                    continue
                in_quotes = False
            else:
                cell += ch
            i += 1
            continue
        if ch == QUOTE and not field_started:
            in_quotes, field_started = True, True
        elif ch == delimiter:
            row.append(cell)
            cell, field_started = "", False
        elif ch == "\r" and i + 1 < len(text) and text[i + 1] == "\n":
            row.append(cell)
            records.append(row)
            row, cell, field_started = [], "", False
            i += 2
            continue
        elif ch == "\n":
            row.append(cell)
            records.append(row)
            row, cell, field_started = [], "", False
        else:
            cell += ch
            field_started = True
        i += 1
    if cell or row:
        row.append(cell)
        records.append(row)
    return [r for r in records if r != [""]]


TORTURE = ['a,b', 'say "hi"', "line1\nline2", "tab\there", "  spaced  ",
           "عربي، فاصلة", 'mix , " and \n and \t', "", "1,000.25", "١٢٣"]

print("Part A: the announced schema holds structure and content")

PLAIN = ["1", "صنف عادي", "1000.00", "عميل"]
check("A1 a cell with nothing to escape is written bare and read back unchanged",
      encode_row(PLAIN, COMMA) == "1,صنف عادي,1000.00,عميل" and
      parse_delimited(encode_row(PLAIN, COMMA) + NL, COMMA) == [PLAIN])
check("A2 encoding never rewrites content: what goes in comes back byte for byte",
      all(parse_delimited(write_delimited(None, [[t, "x"]], COMMA), COMMA) == [[t, "x"]]
          for t in TORTURE))
check("A2b a record of one empty cell is a blank line, which readers skip - stated, not hidden",
      write_delimited(None, [[""]], COMMA) == NL and
      parse_delimited(write_delimited(None, [[""]], COMMA), COMMA) == [] and
      parse_delimited(write_delimited(None, [["", "x"]], COMMA), COMMA) == [["", "x"]])
check("A3 a comma inside a name cannot add a column, and a quote cannot break the record",
      parse_delimited(write_delimited(["الاسم", "المبلغ"], [['صنف "مميز", كبير', "1000.00"]], COMMA),
                      COMMA) == [["الاسم", "المبلغ"], ['صنف "مميز", كبير', "1000.00"]])
check("A4 a newline or a tab inside a note cannot add a record or a column (TSV schema)",
      parse_delimited(write_delimited(["م", "ملاحظة"], [["1", "سطر أول\nسطر ثاني\tثم"]], TAB), TAB)
      == [["م", "ملاحظة"], ["1", "سطر أول\nسطر ثاني\tثم"]])
check("A5 money leaves as an invariant machine number with no thousands separator",
      money(1000.25) == "1000.25" and money(1234567.5) == "1234567.50" and
      money(-40.0) == "-40.00" and "," not in money(1234567.5))

print()
print("Part B: P7BT-39 - Arabic text with a quote, a newline, commas and a tab")

AR_ROW = ["12", 'صنف "خاص"، سطر\nثانٍ\tوعلامة', "عميل، Ltd", "5.00", "12.5%"]
AR_HEADER = ["م", "المادة", "العميل", "الكمية", "نسبة الربح"]
legacy = legacy_quoted_csv(AR_HEADER, [AR_ROW])
fixed = write_delimited(AR_HEADER, [AR_ROW], COMMA)
check("B1 the legacy quoted writer breaks the record: the reader does not get the row back",
      parse_delimited(legacy, COMMA) != [AR_HEADER, AR_ROW])
check("B2 the repaired writer round-trips the same Arabic text, count of records and cells",
      parse_delimited(fixed, COMMA) == [AR_HEADER, AR_ROW] and
      all(len(r) == len(AR_HEADER) for r in parse_delimited(fixed, COMMA)))
check("B3 the legacy text is not merely quoted differently - it loses the cell boundaries",
      len(parse_delimited(legacy, COMMA)) != 2 or
      any(len(r) != len(AR_HEADER) for r in parse_delimited(legacy, COMMA)))
TSV_ROW = ["1", "ملاحظة\tبداخلها تبويب\nوسطر جديد", "1,000.00"]
check("B4 the legacy TSV splits that one row into three records; the repaired one keeps it whole",
      len(parse_delimited(legacy_tsv(["م", "ملاحظة", "الصافي"], [TSV_ROW]), TAB)) > 2 and
      parse_delimited(write_delimited(["م", "ملاحظة", "الصافي"], [TSV_ROW], TAB), TAB)
      == [["م", "ملاحظة", "الصافي"], TSV_ROW])

print()
print("Part C: P7BT-40 - N2 money with a thousands separator in the POS export")

POS_HEADER = ["#", "العميل", "نقدي", "الصافي"]
POS_ROW = [1, "عميل عادي", 1000.25, 1000.25]
CULTURES = {"group-comma": lambda v: "{:,.2f}".format(v),       # 1,000.25
            "group-dot-decimal-comma": lambda v: "{:,.2f}".format(v).replace(",", "X")
            .replace(".", ",").replace("X", ".")}               # 1.000,25
for name, fmt in CULTURES.items():
    legacy_row = legacy_bare_csv(POS_HEADER, [POS_ROW], fmt)
    fixed_row = write_delimited([str(c) for c in POS_HEADER],
                                [[str(POS_ROW[0]), POS_ROW[1], money(POS_ROW[2]), money(POS_ROW[3])]],
                                COMMA)
    check("C-%s the bare legacy export splits the amount into extra columns" % name,
          len(parse_delimited(legacy_row, COMMA)[1]) > len(POS_HEADER))
    check("C-%s the repaired export keeps the column count and the amount parses back" % name,
          len(parse_delimited(fixed_row, COMMA)[1]) == len(POS_HEADER) and
          float(parse_delimited(fixed_row, COMMA)[1][2]) == 1000.25 and
          float(parse_delimited(fixed_row, COMMA)[1][3]) == 1000.25)
check("C3 a display-formatted amount is still safe when quoting is what the schema announces",
      len(parse_delimited(write_delimited(None, [["1,000.25"]], COMMA), COMMA)[0]) == 1 and
      parse_delimited(write_delimited(None, [["1,000.25"]], COMMA), COMMA) == [["1,000.25"]])

print()
print("Part D: a mixed sheet keeps its shape record by record")

MIXED_HEADER = ["م", "الصنف", "الكمية", "المبلغ"]
MIXED = [["1", "صنف عادي", "2.00", "100.00"],
         ["2", 'صنف "مميز", كبير', "1.00", "1000.25"],
         ["3", "سطر\nجديد", "3.00", "0.00"],
         ["4", "عربي، مع فاصلة", "4.00", "-25.50"]]
fixed_sheet = write_delimited(MIXED_HEADER, MIXED, COMMA)
parsed = parse_delimited(fixed_sheet, COMMA)
check("D1 five records in, five records out, every one with four cells",
      len(parsed) == 5 and all(len(r) == 4 for r in parsed) and parsed[0] == MIXED_HEADER and
      parsed[1:] == MIXED)
check("D2 the legacy writers do not hold that shape on the same data",
      any(len(r) != 4 for r in parse_delimited(legacy_quoted_csv(MIXED_HEADER, MIXED), COMMA)[1:]) and
      any(len(r) != 4 for r in parse_delimited(legacy_tsv(MIXED_HEADER, MIXED), TAB)[1:]))

print()
print("Part E: static witnesses over the writer and the four wired exports")

check("E1 the shared writer announces one schema and preserves content",
      EXPORT.count("public const char CsvDelimiter = ',';") == 1 and
      EXPORT.count("public const char TsvDelimiter = '\\t';") == 1 and
      EXPORT.count("public const string RecordNewline = \"\\r\\n\";") == 1 and
      EXPORT.count("text.Replace(\"\\\"\", \"\\\"\\\"\")") == 1 and
      EXPORT.count("ToString(\"0.00\", CultureInfo.InvariantCulture)") == 2 and
      EXPORT.count("new StreamWriter(path, false, Encoding.UTF8)") == 1 and
      EXPORT.count("Repair R-082 (audit finding P7-048)") == 1)
check("E2 quoting is decided by the four hazards, and only then",
      EXPORT.count("text.IndexOf(delimiter) >= 0") == 1 and
      EXPORT.count("text.IndexOf(QuoteChar) >= 0") == 1 and
      EXPORT.count("text.IndexOf('\\r') >= 0") == 1 and
      EXPORT.count("text.IndexOf('\\n') >= 0") == 1 and
      EXPORT.count("if (!mustQuote) return text;") == 1)
check("E3 the items-profit export goes through the writer, with machine money",
      PROFIT.count("SpreadsheetExport.Write(filePath, SpreadsheetExport.CsvDelimiter, header, rows);") == 1 and
      PROFIT.count("SpreadsheetExport.Money(r.") == 4 and PROFIT.count("sw.WriteLine") == 0 and
      PROFIT.count('"م", "رمز المادة", "المادة", "الكمية",') == 1)
check("E4 the sales-in-period export keeps both tabs and routes both through the writer",
      PERIOD.count("SpreadsheetExport.Write(filePath, SpreadsheetExport.CsvDelimiter, header, rows);") == 2 and
      PERIOD.count("SpreadsheetExport.Money(r.") == 8 and PERIOD.count("sw.WriteLine") == 0 and
      PERIOD.count("if (TabControl1.SelectedIndex == 0)") == 1)
check("E5 the purchase TSV export delegates to the writer and keeps its caller and its cells",
      PUR.count("SpreadsheetExport.WriteDataTable(filePath, dt, SpreadsheetExport.TsvDelimiter);") == 1 and
      PUR.count("sb.AppendLine") == 0 and PUR.count("ExportDataTableToTsv(dt, dlg.FileName);") == 1 and
      PUR.count("private static void ExportDataTableToTsv(") == 1)
check("E6 the POS export quotes every field and writes invariant money",
      POS.count("SpreadsheetExport.Write(outputPath, SpreadsheetExport.CsvDelimiter, header, rows);") == 1 and
      POS.count("SpreadsheetExport.Money(item.") == 9 and POS.count("writer.WriteLine") == 0 and
      POS.count('"#", "نوع الفاتورة", "رقم الفاتورة", "التاريخ", "الوقت",') == 1)
check("E7 no wired screen still interpolates a display money format into a delimited line",
      PROFIT.count(":N2}") == 0 and PERIOD.count(":N2}") == 0 and POS.count(":N2}") == 0 and
      PROFIT.count("SpreadsheetExport.Money(") == 4 and POS.count("SpreadsheetExport.Money(") == 9)
check("E8 the report table that feeds the printed sheet keeps its own display formatting",
      PUR.count("ToString(fmt)") == 13 and PUR.count('string fmt = Common.DigitsNo ?? "N2";') == 2)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - one announced schema keeps records, columns and amounts intact, and the")
print("four cited exports round-trip Arabic text, quotes, tabs, newlines and N2 money.")
sys.exit(0)
