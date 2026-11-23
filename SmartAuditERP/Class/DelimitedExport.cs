using System;
using System.Collections.Generic;
using System.Data;
using System.Globalization;
using System.IO;
using System.Text;

namespace SmartAuditERP
{
    /// <summary>
    /// P7-048/049/050 (الشريحة السادسة من المرحلة السابعة): كاتب موحّد للملفات
    /// المفصولة (CSV/TSV) بترميز خلايا صحيح لكل شاشات التقارير.
    ///
    /// العقد:
    /// (١) الفاصل يُشتق من امتداد الملف نفسه (.csv = فاصلة، وإلا TAB) — لا يكتب
    ///     نصاً بفاصلٍ تحت امتداد لا يطابقه.
    /// (٢) خلية CSV تُرمَّز وفق RFC 4180: أي خلية تحوي الفاصلة أو علامة الاقتباس
    ///     أو سطراً جديداً تُحاط بعلامتي اقتباس وتُضاعف علامات الاقتباس الداخلية —
    ///     قيم تنسيق الألوف («1,234.50») تبقى خلية واحدة لا تنشطر عمودين.
    /// (٣) خلية TSV (لا معيار اقتباس لها): محارف الجدول/السطر الجديد داخل القيمة
    ///     تُستبدل بمسافة كي لا تنكسر بنية الأعمدة.
    /// (٤) P7-049: بادئات الصيغ (= + @ أو «-» غير رقمية) تُحيَّد بمسافة بادئة قبل
    ///     الكتابة فلا تُفسَّر الخلية صيغةً عند فتح الملف ببرنامج جداول؛ الأرقام
    ///     السالبة الحقيقية تبقى أرقاماً.
    /// (٥) الملف يُكتب UTF-8 مع BOM (سلوك Encoding.UTF8 في File.WriteAllText)
    ///     كي يتعرف Excel على العربية تلقائياً.
    /// </summary>
    public static class DelimitedExport
    {
        /// <summary>مرشح حوار الحفظ الصادق: ما يُعرض هو ما يُكتب فعلاً.</summary>
        public const string CsvTsvFilter =
            "CSV Files (*.csv)|*.csv|TSV Files (*.tsv)|*.tsv";

        /// <summary>مرشح يشمل Excel حقيقياً (ClosedXML) مع CSV/TSV.</summary>
        public const string ExcelCsvTsvFilter =
            "Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|TSV Files (*.tsv)|*.tsv";

        /// <summary>مرشح يشمل Excel حقيقياً وCSV مع HTML (مصدّرات الجداول HTML القائمة).</summary>
        public const string ExcelCsvHtmlFilter =
            "Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|HTML Files (*.html)|*.html";

        /// <summary>الفاصل وفق امتداد الملف: فاصلة لـ.csv وTAB لما سواه (tsv).</summary>
        public static char DelimiterForFile(string filePath)
            => !string.IsNullOrEmpty(filePath)
               && filePath.EndsWith(".csv", StringComparison.OrdinalIgnoreCase)
                ? ','
                : '\t';

        /// <summary>
        /// P7-049: يحيّد بادئات الصيغ. «=» و«+» و«@» دائماً؛ و«-» حين لا تكون
        /// القيمة رقماً سالساً حقيقياً (فالرقم السالب لا يُلمس).
        /// </summary>
        public static string NeutralizeFormulaPrefix(string value)
        {
            if (string.IsNullOrEmpty(value)) return value ?? string.Empty;

            char c0 = value[0];
            if (c0 == '=' || c0 == '+' || c0 == '@')
                return " " + value;

            if (c0 == '-' && value.Length > 1 &&
                !double.TryParse(value, NumberStyles.Any,
                    CultureInfo.InvariantCulture, out _) &&
                !double.TryParse(value, NumberStyles.Any,
                    CultureInfo.CurrentCulture, out _))
                return " " + value;

            return value;
        }

        /// <summary>
        /// P7-048: ترميز خلية واحدة وفق الفاصل — اقتباس RFC 4180 للفاصلة،
        /// وتنظيف محارف التحكم لـ TSV.
        /// </summary>
        public static string EncodeCell(string value, char delimiter)
        {
            if (string.IsNullOrEmpty(value)) return string.Empty;

            value = NeutralizeFormulaPrefix(value);

            if (delimiter == ',')
            {
                if (value.IndexOf(',') >= 0 || value.IndexOf('"') >= 0 ||
                    value.IndexOf('\r') >= 0 || value.IndexOf('\n') >= 0)
                {
                    return "\"" + value.Replace("\"", "\"\"") + "\"";
                }
                return value;
            }

            // TSV: لا معيار اقتباس — استبدال محارف بنية الصف بمسافة
            if (value.IndexOf('\t') >= 0) value = value.Replace('\t', ' ');
            if (value.IndexOf('\r') >= 0) value = value.Replace('\r', ' ');
            if (value.IndexOf('\n') >= 0) value = value.Replace('\n', ' ');
            return value;
        }

        /// <summary>
        /// يكتب الملف المفصول كاملاً: صفاً للرأس ثم صفوف البيانات.
        /// الفاصل من امتداد filePath.
        /// </summary>
        public static void WriteFile(
            string filePath, string[] header, IEnumerable<string[]> rows)
        {
            if (string.IsNullOrEmpty(filePath))
                throw new ArgumentException("مسار التصدير فارغ", nameof(filePath));

            char d = DelimiterForFile(filePath);
            var sb = new StringBuilder();

            AppendRecord(sb, header, d);
            if (rows != null)
            {
                foreach (var row in rows)
                    AppendRecord(sb, row, d);
            }

            File.WriteAllText(filePath, sb.ToString(), Encoding.UTF8);
        }

        /// <summary>يكتب DataTable (الرأس من أعمدتها) بترميز الخلايا الموحّد.</summary>
        public static void WriteDataTable(string filePath, DataTable dt)
        {
            if (dt == null) throw new ArgumentNullException(nameof(dt));
            if (string.IsNullOrEmpty(filePath))
                throw new ArgumentException("مسار التصدير فارغ", nameof(filePath));

            char d = DelimiterForFile(filePath);
            var sb = new StringBuilder();

            var header = new string[dt.Columns.Count];
            for (int c = 0; c < dt.Columns.Count; c++)
                header[c] = dt.Columns[c].ColumnName;
            AppendRecord(sb, header, d);

            foreach (DataRow row in dt.Rows)
            {
                var cells = new string[dt.Columns.Count];
                for (int c = 0; c < dt.Columns.Count; c++)
                {
                    object v = row[c];
                    cells[c] = v == null || v == DBNull.Value
                        ? string.Empty
                        : v.ToString();
                }
                AppendRecord(sb, cells, d);
            }

            File.WriteAllText(filePath, sb.ToString(), Encoding.UTF8);
        }

        private static void AppendRecord(StringBuilder sb, string[] cells, char d)
        {
            if (cells == null || cells.Length == 0)
            {
                sb.AppendLine();
                return;
            }

            for (int i = 0; i < cells.Length; i++)
            {
                if (i > 0) sb.Append(d);
                sb.Append(EncodeCell(cells[i] ?? string.Empty, d));
            }
            sb.AppendLine();
        }
    }
}
