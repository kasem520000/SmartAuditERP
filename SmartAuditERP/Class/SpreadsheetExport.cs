using System;
using System.Collections.Generic;
using System.Data;
using System.Globalization;
using System.IO;
using System.Text;

namespace SmartAuditERP
{
    /// <summary>
    /// Repair R-082 (audit finding P7-048): one delimited-text writer for the report exports, with
    /// an announced schema, instead of a hand-rolled loop per screen.
    ///
    /// Announced schema (identical for every caller):
    ///   delimiter  ',' for CSV and '\t' for TSV (CsvDelimiter / TsvDelimiter);
    ///   quoting    a cell is wrapped in '"' when it holds the delimiter, a quote, CR or LF, and
    ///              every quote inside it is doubled, so no value can add a column or a record;
    ///   record end CRLF, and never inside an unquoted cell;
    ///   money      Money() writes an invariant two-decimal number with no thousands separator, so
    ///              a machine reader parses one field instead of two;
    ///   encoding   UTF-8 with preamble, exactly as these screens already wrote it, so Arabic text
    ///              survives the spreadsheet programs that open these files.
    ///
    /// Round-trip guarantee: EncodeCell never drops or rewrites content - it only wraps and doubles
    /// quotes - so a reader that follows the same announced schema recovers the original text.
    /// </summary>
    public static class SpreadsheetExport
    {
        public const char CsvDelimiter = ',';
        public const char TsvDelimiter = '\t';
        public const char QuoteChar = '"';
        public const string RecordNewline = "\r\n";

        /// <summary>Machine-readable money: invariant culture, two decimals, no group separator.</summary>
        public static string Money(double value)
        {
            return value.ToString("0.00", CultureInfo.InvariantCulture);
        }

        /// <summary>Same, for screens whose money fields are decimal.</summary>
        public static string Money(decimal value)
        {
            return value.ToString("0.00", CultureInfo.InvariantCulture);
        }

        /// <summary>
        /// Money cell for a row property of any type, so no caller has to know the property's
        /// declared type to export it safely: numbers leave invariant with two decimals and no
        /// group separator, an already formatted text passes through unchanged, and anything else
        /// is written as text.
        /// </summary>
        public static string Money(object value)
        {
            switch (value)
            {
                case null:
                    return string.Empty;
                case string text:
                    return text;
                case double d:
                    return Money(d);
                case decimal m:
                    return Money(m);
                case float f:
                    return Money((double)f);
                case int i:
                    return Money((double)i);
                case long l:
                    return Money((double)l);
                case short sh:
                    return Money((double)sh);
                default:
                    return Text(value);
            }
        }

        /// <summary>
        /// Text cell for a value of any type: strings pass through byte for byte, and every other
        /// value is formatted in the invariant culture so a decimal separator can never depend on
        /// the machine locale and split a bare field.
        /// </summary>
        public static string Text(object value)
        {
            switch (value)
            {
                case null:
                    return string.Empty;
                case string text:
                    return text;
                case IFormattable formattable:
                    return formattable.ToString(null, CultureInfo.InvariantCulture);
                default:
                    return value.ToString() ?? string.Empty;
            }
        }

        /// <summary>
        /// Starts a delimited file with the announced schema. Call sites need no collection or
        /// LINQ imports: Header and Row take the cells of one record each.
        /// </summary>
        public static ExportFile Begin(string path, char delimiter)
        {
            return new ExportFile(path, delimiter);
        }

        /// <summary>One delimited file being composed record by record.</summary>
        public sealed class ExportFile
        {
            private readonly string _path;
            private readonly char _delimiter;
            private readonly List<string> _header = new List<string>();
            private readonly List<List<string>> _rows = new List<List<string>>();
            private bool _hasHeader;

            internal ExportFile(string path, char delimiter)
            {
                _path = path;
                _delimiter = delimiter;
            }

            /// <summary>Sets the header record; cells are encoded when the file is saved.</summary>
            public ExportFile Header(params string[] cells)
            {
                _hasHeader = true;
                _header.Clear();
                _header.AddRange(cells);
                return this;
            }

            /// <summary>Adds one data record; cells are encoded when the file is saved.</summary>
            public ExportFile Row(params string[] cells)
            {
                var row = new List<string>(cells.Length);
                row.AddRange(cells);
                _rows.Add(row);
                return this;
            }

            /// <summary>Writes the file under the announced schema.</summary>
            public void Save()
            {
                Write(_path, _delimiter, _hasHeader ? _header : null, _rows);
            }
        }

        /// <summary>
        /// Encodes one cell for the announced schema. Content is preserved byte for byte: the cell
        /// is quoted when it could otherwise break the structure, and inner quotes are doubled.
        /// </summary>
        public static string EncodeCell(string text, char delimiter)
        {
            text ??= string.Empty;

            bool mustQuote = text.IndexOf(delimiter) >= 0
                             || text.IndexOf(QuoteChar) >= 0
                             || text.IndexOf('\r') >= 0
                             || text.IndexOf('\n') >= 0;

            if (!mustQuote) return text;

            return QuoteChar + text.Replace("\"", "\"\"") + QuoteChar;
        }

        /// <summary>Encodes one record: every cell encoded, then joined by the delimiter.</summary>
        public static string EncodeRow(IEnumerable<string> cells, char delimiter)
        {
            var sb = new StringBuilder();
            bool first = true;

            foreach (string cell in cells)
            {
                if (!first) sb.Append(delimiter);
                sb.Append(EncodeCell(cell, delimiter));
                first = false;
            }

            return sb.ToString();
        }

        /// <summary>
        /// Writes a header record and the data records to <paramref name="path"/> under the
        /// announced schema. <paramref name="header"/> may be null for a headerless file.
        /// </summary>
        public static void Write(
            string path,
            char delimiter,
            IEnumerable<string> header,
            IEnumerable<IEnumerable<string>> rows)
        {
            using (var sw = new StreamWriter(path, false, Encoding.UTF8))
            {
                sw.NewLine = RecordNewline;

                if (header != null)
                    sw.WriteLine(EncodeRow(header, delimiter));

                if (rows != null)
                {
                    foreach (IEnumerable<string> row in rows)
                        sw.WriteLine(EncodeRow(row, delimiter));
                }
            }
        }

        /// <summary>
        /// Writes a whole DataTable - column names as the header, cell text as the values - under
        /// the announced schema. Cells already formatted for display keep their text; quoting is
        /// what preserves the structure, so nothing has to be rewritten or truncated.
        /// </summary>
        public static void WriteDataTable(string path, DataTable table, char delimiter)
        {
            if (table == null) throw new ArgumentNullException(nameof(table));

            var header = new List<string>(table.Columns.Count);
            foreach (DataColumn column in table.Columns)
                header.Add(column.ColumnName);

            var rows = new List<List<string>>(table.Rows.Count);
            foreach (DataRow row in table.Rows)
            {
                var cells = new List<string>(table.Columns.Count);
                for (int c = 0; c < table.Columns.Count; c++)
                    cells.Add(row[c]?.ToString() ?? string.Empty);
                rows.Add(cells);
            }

            Write(path, delimiter, header, rows);
        }
    }
}
