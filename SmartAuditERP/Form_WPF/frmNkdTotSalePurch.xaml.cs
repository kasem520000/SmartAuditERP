using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;
using DevExpress.Xpf.Core;
using Microsoft.Win32;
using Brushes = System.Windows.Media.Brushes;
using Color = System.Windows.Media.Color;
using ColorConverter = System.Windows.Media.ColorConverter;
using FontFamily = System.Windows.Media.FontFamily;
using PrintDialog = System.Windows.Controls.PrintDialog;
using SaveFileDialog = Microsoft.Win32.SaveFileDialog;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmNkdTotSalePurch : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;
        private bool   PrintHeader = true;
        private bool   PrintFooter = true;
        private bool   PrintStamp  = true;
        private int    PrintType   = 0;
        private int    PrintNo     = 1;
        private string defPrinter  = "";
        private string RptName     = "";
        private string RptUrl      = "";

        private ObservableCollection<SalePurchRow> _rows;

        #endregion

        #region Constructor

        public frmNkdTotSalePurch()
        {
            conn  = MainClass.ConnObj();
            _rows = new ObservableCollection<SalePurchRow>();
            InitializeComponent();
        }

        #endregion

        #region Load

        private void frmNkdTotSalePurch_Load(object sender, RoutedEventArgs e)
        {
            txtDateFrom.SelectedDate = DateTime.Today;
            txtDateTo.SelectedDate   = DateTime.Today;
            dgvItems.ItemsSource     = _rows;
            LoadPrintSettings();
        }

        #endregion

        #region CheckBox

        private void ckTotalPeriod_CheckedChanged(object sender, RoutedEventArgs e)
        {
            bool allPeriod = ckTotalPeriod.IsChecked == true;
            if (txtDateFrom != null) txtDateFrom.IsEnabled = !allPeriod;
            if (txtDateTo != null)   txtDateTo.IsEnabled   = !allPeriod;
        }

        #endregion

        #region Show Result

        private void Button1_Click(object sender, RoutedEventArgs e)
        {
            _rows.Clear();
            txtSumPurch.Text = "0.00";
            txtSumSale.Text  = "0.00";
            CalcStock();
        }

        private void CalcStock()
        {
            try
            {
                SqlDataAdapter itemAdapter = new SqlDataAdapter(
                    "select id,name,nameEN from Items where IS_Deleted=0 order by id", conn);
                DataTable itemsDt = new DataTable();
                itemAdapter.Fill(itemsDt);

                double totalPurch = 0.0;
                double totalSale  = 0.0;

                string branchFilter = MainClass.BranchNo != -1
                    ? $"inv.branch={MainClass.BranchNo} and "
                    : "";

                string dateFilter = ckTotalPeriod.IsChecked != true
                    ? " date>=@date1 and date<=@date2 and "
                    : "";

                DateTime dtFrom = txtDateFrom.SelectedDate ?? DateTime.Today;
                DateTime dtTo   = (txtDateTo.SelectedDate ?? DateTime.Today).AddHours(24);

                Dispatcher.Invoke(() =>
                {
                    ProgressBar1.Visibility = Visibility.Visible;
                    ProgressBar1.Maximum    = itemsDt.Rows.Count;
                    ProgressBar1.Value      = 0;
                });

                for (int i = 0; i < itemsDt.Rows.Count; i++)
                {
                    object itemId   = itemsDt.Rows[i]["id"];
                    string itemName = string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                        ? itemsDt.Rows[i]["name"].ToString()
                        : itemsDt.Rows[i]["nameEN"].ToString();

                    double purchQty = 0, purchTotal = 0;
                    double purchRetQty = 0, purchRetTotal = 0;
                    double saleQty = 0, saleTotal = 0;
                    double saleRetQty = 0, saleRetTotal = 0;

                    // مشتريات
                    ExecuteQuery($"select sum(val),sum(val*exchange_price) from inv,inv_sub where {branchFilter} Inv_Sub.ItemId={itemId} and {dateFilter} inv.inv_type=1 and inv.proc_type=1 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                        conn, dtFrom.ToShortDateString(), dtTo.ToString(), ref purchQty, ref purchTotal);

                    // مرتجع مشتريات
                    ExecuteQuery($"select sum(val),sum(val*exchange_price) from inv,inv_sub where {branchFilter} Inv_Sub.ItemId={itemId} and {dateFilter} inv.inv_type=1 and inv.proc_type=2 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                        conn, dtFrom.ToShortDateString(), dtTo.ToString(), ref purchRetQty, ref purchRetTotal);

                    // مبيعات
                    ExecuteQuery($"select sum(val),sum(val*exchange_price) from inv,inv_sub where {branchFilter} Inv_Sub.ItemId={itemId} and {dateFilter} inv.inv_type=2 and inv.proc_type=1 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                        conn, dtFrom.ToShortDateString(), dtTo.ToString(), ref saleQty, ref saleTotal);

                    // مرتجع مبيعات
                    ExecuteQuery($"select sum(val),sum(val*exchange_price) from inv,inv_sub where {branchFilter} Inv_Sub.ItemId={itemId} and {dateFilter} inv.inv_type=2 and inv.proc_type=2 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                        conn, dtFrom.ToShortDateString(), dtTo.ToString(), ref saleRetQty, ref saleRetTotal);

                    // POS مبيعات
                    double posQty = 0, posTotal = 0;
                    ExecuteQuery($"select sum(val),sum(val*exchange_price) from inv,inv_sub where {branchFilter} Inv_Sub.ItemId={itemId} and {dateFilter} inv.inv_type=3 and inv.proc_type=1 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                        conn, dtFrom.ToShortDateString(), dtTo.ToString(), ref posQty, ref posTotal);
                    saleQty   += posQty;
                    saleTotal += posTotal;

                    // مرتجع POS
                    double posRetQty = 0, posRetTotal = 0;
                    ExecuteQuery($"select sum(val),sum(val*exchange_price) from inv,inv_sub where {branchFilter} Inv_Sub.ItemId={itemId} and {dateFilter} inv.inv_type=3 and inv.proc_type=2 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                        conn, dtFrom.ToShortDateString(), dtTo.ToString(), ref posRetQty, ref posRetTotal);
                    saleRetQty   += posRetQty;
                    saleRetTotal += posRetTotal;

                    double netPurchQty   = purchQty   - purchRetQty;
                    double netPurchTotal = purchTotal  - purchRetTotal;
                    double netSaleQty    = saleQty     - saleRetQty;
                    double netSaleTotal  = saleTotal   - saleRetTotal;

                    if (netPurchQty != 0.0 || netSaleQty != 0.0)
                    {
                        totalPurch += netPurchTotal;
                        totalSale  += netSaleTotal;

                        Dispatcher.Invoke(() =>
                        {
                            _rows.Add(new SalePurchRow
                            {
                                Column1 = itemsDt.Rows[i]["id"].ToString(),
                                Column2 = itemName,
                                Column3 = netPurchQty.ToString("N4"),
                                Column4 = netPurchTotal.ToString("N4"),
                                Column6 = netSaleQty.ToString("N4"),
                                Column5 = netSaleTotal.ToString("N4")
                            });
                        });
                    }

                    Dispatcher.Invoke(() => ProgressBar1.Value++);
                }

                Dispatcher.Invoke(() =>
                {
                    txtSumPurch.Text        = totalPurch.ToString("N2");
                    txtSumSale.Text         = totalSale.ToString("N2");
                    ProgressBar1.Visibility = Visibility.Collapsed;
                });
            }
            catch (Exception ex)
            {
                Dispatcher.Invoke(() => ShowError(ex));
            }
        }

        private void ExecuteQuery(string sql, SqlConnection conn, string date1, string date2,
            ref double qty, ref double total)
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(sql, conn);

                if (sql.Contains("@date1"))
                {
                    adapter.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value = date1;
                    adapter.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value = date2;
                }

                DataTable dt = new DataTable();
                adapter.Fill(dt);

                if (dt.Rows.Count > 0 && !string.IsNullOrEmpty(dt.Rows[0][0]?.ToString()))
                {
                    double.TryParse(dt.Rows[0][0].ToString(), out qty);
                    double val = 0;
                    double.TryParse(dt.Rows[0][1].ToString(), out val);
                    total = Math.Round(val, 4);
                }
            }
            catch { }
        }

        #endregion

        #region Print & Export

        private void btnPreview_Click(object sender, RoutedEventArgs e) { PrintDevexpress(2); }
        private void btnPrint_Click(object sender, RoutedEventArgs e)   { PrintDevexpress(1); }

        private void btnExport_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_rows.Count == 0)
                {
                    DXMessageBox.Show("لا توجد بيانات للتصدير", "", MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                // P7-050 fix: الامتداد المعروض هو المكتوب فعلاً — xlsx ملف Excel
                // حقيقي (ClosedXML)، وcsv بترميز الخلايا الموحّد (P7-048/049)،
                // وhtml لجدول HTML الحقيقي (كان يعرض xls/csv ويكتب HTML دائماً)
                SaveFileDialog saveDialog = new SaveFileDialog
                {
                    FileName   = "إجمالي_المبيعات_والمشتريات",
                    Filter     = DelimitedExport.ExcelCsvHtmlFilter
                };

                if (saveDialog.ShowDialog() != true) return;

                string exportPath = saveDialog.FileName;
                if (exportPath.EndsWith(".html", StringComparison.OrdinalIgnoreCase))
                {
                    ExportToHtml(exportPath);
                }
                else if (exportPath.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase))
                {
                    ExportToExcelClosedXml(exportPath);
                }
                else
                {
                    ExportToCsv(exportPath);
                }

                Process.Start(new ProcessStartInfo(exportPath) { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        /// <summary>
        /// P7-050 fix: CSV بترميز الخلايا الموحّد — الفاصلة والاقتباسات والأسطر
        /// وبادئات الصيغ ترميز صحيح (P7-048/049).
        /// </summary>
        private void ExportToCsv(string fileName)
        {
            DelimitedExport.WriteFile(fileName,
                new[]
                {
                    "رقم الصنف", "الصنف", "الكمية (مشتريات)", "الإجمالي (مشتريات)",
                    "الكمية (مبيعات)", "الإجمالي (مبيعات)"
                },
                _rows.Select(r => new[]
                {
                    r.Column1, r.Column2, r.Column3, r.Column4, r.Column6, r.Column5
                }));
        }

        /// <summary>
        /// P7-050 fix: ملف xlsx حقيقي عبر ClosedXML — القيم الرقمية تُكتب أرقاماً.
        /// </summary>
        private void ExportToExcelClosedXml(string fileName)
        {
            using var workbook = new ClosedXML.Excel.XLWorkbook();
            var worksheet = workbook.Worksheets.Add("المبيعات والمشتريات");

            string[] headers =
            {
                "رقم الصنف", "الصنف", "الكمية (مشتريات)", "الإجمالي (مشتريات)",
                "الكمية (مبيعات)", "الإجمالي (مبيعات)"
            };
            for (int c = 0; c < headers.Length; c++)
            {
                var cell = worksheet.Cell(1, c + 1);
                cell.Value = headers[c];
                cell.Style.Font.Bold = true;
            }

            int rowIdx = 2;
            foreach (SalePurchRow row in _rows)
            {
                WriteSheetCell(worksheet, rowIdx, 1, row.Column1);
                WriteSheetCell(worksheet, rowIdx, 2, row.Column2);
                WriteSheetCell(worksheet, rowIdx, 3, row.Column3);
                WriteSheetCell(worksheet, rowIdx, 4, row.Column4);
                WriteSheetCell(worksheet, rowIdx, 5, row.Column6);
                WriteSheetCell(worksheet, rowIdx, 6, row.Column5);
                rowIdx++;
            }

            worksheet.Columns().AdjustToContents();
            workbook.SaveAs(fileName);
        }

        /// <summary>
        /// يكتب الخلية رقماً إن كانت قيمتها رقماً نصياً، وإلا نصاً محيَّد بادئات الصيغ.
        /// </summary>
        private static void WriteSheetCell(
            ClosedXML.Excel.IXLWorksheet worksheet, int row, int col, string value)
        {
            if (double.TryParse(value,
                    System.Globalization.NumberStyles.Any,
                    System.Globalization.CultureInfo.InvariantCulture,
                    out double d))
            {
                worksheet.Cell(row, col).Value = d;
                worksheet.Cell(row, col).Style.NumberFormat.Format = "#,##0.00";
            }
            else
            {
                worksheet.Cell(row, col).Value =
                    DelimitedExport.NeutralizeFormulaPrefix(value ?? "");
            }
        }

        // P7-098 fix: ترميز HTML لنصوص البيانات
        private static string EscapeHtml(string value)
            => (value ?? "").Replace("&", "&amp;")
                             .Replace("<", "&lt;")
                             .Replace(">", "&gt;");

        private void ExportToHtml(string fileName)
        {
            StringBuilder sb = new StringBuilder();
            sb.AppendLine("<html><head><meta charset='utf-8'/>");
            sb.AppendLine("<style>table{border-collapse:collapse;font-family:Tahoma;font-size:11px;}");
            sb.AppendLine("th,td{border:1px solid #999;padding:4px;text-align:center;}");
            sb.AppendLine("th{background:#DDE7FF;font-weight:bold;}</style></head>");
            sb.AppendLine("<body dir='rtl'>");
            sb.AppendLine($"<h2 style='text-align:center;'>{EscapeHtml(Title)}</h2>");
            sb.AppendLine("<table><tr>");
            sb.AppendLine("<th>رقم الصنف</th><th>الصنف</th>");
            sb.AppendLine("<th>الكمية (مشتريات)</th><th>الإجمالي (مشتريات)</th>");
            sb.AppendLine("<th>الكمية (مبيعات)</th><th>الإجمالي (مبيعات)</th>");
            sb.AppendLine("</tr>");

            foreach (SalePurchRow row in _rows)
            {
                sb.AppendLine("<tr>");
                // P7-098 fix: ترميز HTML لنصوص البيانات
                sb.AppendLine($"<td>{EscapeHtml(row.Column1)}</td><td>{EscapeHtml(row.Column2)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(row.Column3)}</td><td>{EscapeHtml(row.Column4)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(row.Column6)}</td><td>{EscapeHtml(row.Column5)}</td>");
                sb.AppendLine("</tr>");
            }

            sb.AppendLine($"<tr><td colspan='3'><b>إجمالي المشتريات</b></td><td>{EscapeHtml(txtSumPurch.Text)}</td><td><b>إجمالي المبيعات</b></td><td>{EscapeHtml(txtSumSale.Text)}</td></tr>");
            sb.AppendLine("</table></body></html>");
            File.WriteAllText(fileName, sb.ToString(), Encoding.UTF8);
        }

        private void PrintDevexpress(int printMode)
        {
            try
            {
                RptUrl     = MainClass.ReportsPath;
                RptName    = "rptNkdTotSalePurch.repx";
                defPrinter = MainClass.ReportsPrinter;

                if (_rows.Count == 0)
                {
                    DXMessageBox.Show("لا توجد عمليات بالجدول", "", MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                // P7-097 fix: مسار الطباعة FlowDocument لا يحمّل ملف
                // REPX أصلًا — فحص وجوده كان يحجب الطباعة/المعاينة
                // على ملف لا يعتمد عليه المسار

                FlowDocument document = BuildPrintDocument();

                if (printMode == 2)
                {
                    System.Windows.Window pw = new System.Windows.Window
                    {
                        Title                 = "معاينة قبل الطباعة",
                        Width                 = 950,
                        Height                = 700,
                        WindowStartupLocation = WindowStartupLocation.CenterScreen,
                        FlowDirection         = System.Windows.FlowDirection.RightToLeft,
                        Background            = Brushes.White
                    };
                    pw.Content = new DocumentViewer { Document = document };
                    pw.ShowDialog();
                }
                else
                {
                    PrintDialog pd = new PrintDialog();
                    if (pd.ShowDialog() == true)
                    {
                        document.PageHeight  = pd.PrintableAreaHeight;
                        document.PageWidth   = pd.PrintableAreaWidth;
                        document.PagePadding = new Thickness(25);
                        document.ColumnGap   = 0;
                        document.ColumnWidth = pd.PrintableAreaWidth;

                        IDocumentPaginatorSource src = document;
                        for (int i = 0; i < PrintNo; i++)
                            pd.PrintDocument(src.DocumentPaginator, Title);
                    }
                }
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        private FlowDocument BuildPrintDocument()
        {
            FlowDocument doc = new FlowDocument
            {
                FlowDirection = System.Windows.FlowDirection.RightToLeft,
                FontFamily    = new FontFamily("Tahoma"),
                FontSize      = 9,
                PagePadding   = new Thickness(15),
                ColumnWidth   = 900
            };

            doc.Blocks.Add(new Paragraph(new Run(Title))
            {
                FontSize = 14, FontWeight = FontWeights.Bold,
                TextAlignment = TextAlignment.Center,
                Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#213A7A"))
            });

            string period = ckTotalPeriod.IsChecked == true
                ? "كل الفترة"
                : $"من {txtDateFrom.SelectedDate?.ToShortDateString()} إلى {txtDateTo.SelectedDate?.ToShortDateString()}";

            doc.Blocks.Add(new Paragraph(new Run($"📅 الفترة: {period}"))
            {
                FontSize = 11, FontWeight = FontWeights.Bold, Margin = new Thickness(0, 0, 0, 10)
            });

            Table table = new Table { CellSpacing = 0 };
            for (int i = 0; i < 6; i++)
                table.Columns.Add(new TableColumn());

            TableRowGroup group = new TableRowGroup();
            table.RowGroups.Add(group);

            TableRow headerRow = new TableRow();
            group.Rows.Add(headerRow);
            AddHeaderCell(headerRow, "رقم الصنف");
            AddHeaderCell(headerRow, "الصنف");
            AddHeaderCell(headerRow, "الكمية (مشتريات)");
            AddHeaderCell(headerRow, "الإجمالي (مشتريات)");
            AddHeaderCell(headerRow, "الكمية (مبيعات)");
            AddHeaderCell(headerRow, "الإجمالي (مبيعات)");

            foreach (SalePurchRow row in _rows)
            {
                TableRow dataRow = new TableRow();
                group.Rows.Add(dataRow);
                AddBodyCell(dataRow, row.Column1);
                AddBodyCell(dataRow, row.Column2);
                AddBodyCell(dataRow, row.Column3);
                AddBodyCell(dataRow, row.Column4);
                AddBodyCell(dataRow, row.Column6);
                AddBodyCell(dataRow, row.Column5);
            }

            doc.Blocks.Add(table);

            Paragraph summary = new Paragraph { Margin = new Thickness(0, 10, 0, 0), FontWeight = FontWeights.Bold };
            summary.Inlines.Add(new Run($"إجمالي المشتريات: {txtSumPurch.Text}   |   إجمالي المبيعات: {txtSumSale.Text}"));
            doc.Blocks.Add(summary);

            return doc;
        }

        private void AddHeaderCell(TableRow row, string text)
        {
            TableCell cell = new TableCell(new Paragraph(new Run(text)))
            {
                Background      = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#DDE7FF")),
                BorderBrush     = Brushes.Gray,
                BorderThickness = new Thickness(0.5),
                Padding         = new Thickness(4)
            };
            cell.Blocks.FirstBlock.SetValue(TextElement.FontWeightProperty, FontWeights.Bold);
            cell.Blocks.FirstBlock.SetValue(Block.TextAlignmentProperty, TextAlignment.Center);
            row.Cells.Add(cell);
        }

        private void AddBodyCell(TableRow row, string text)
        {
            TableCell cell = new TableCell(new Paragraph(new Run(text ?? "")))
            {
                BorderBrush     = Brushes.Gray,
                BorderThickness = new Thickness(0.5),
                Padding         = new Thickness(3)
            };
            cell.Blocks.FirstBlock.SetValue(Block.TextAlignmentProperty, TextAlignment.Center);
            row.Cells.Add(cell);
        }

        private void LoadPrintSettings()
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter("select * from SettingPrint where Inv_Id=12", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                if (dt.Rows.Count != 1) return;

                PrintType   = Convert.ToInt32(dt.Rows[0]["printType"]);
                PrintFooter = Convert.ToBoolean(dt.Rows[0]["PrintFooter"]);
                PrintHeader = Convert.ToBoolean(dt.Rows[0]["PrintHeader"]);
                PrintStamp  = Convert.ToBoolean(dt.Rows[0]["PrintStamp"]);
                defPrinter  = dt.Rows[0]["CasherPrinter"]?.ToString() ?? "";

                if (string.IsNullOrEmpty(defPrinter))
                    defPrinter = Common.GetDefaultPrinter();

                PrintNo = Convert.ToInt32(dt.Rows[0]["printNo"]);
            }
            catch { }
        }

        #endregion

        #region Close

        private void Button4_Click(object sender, RoutedEventArgs e) => Close();

        #endregion

        #region Helpers

        private void ShowError(Exception ex)
        {
            DXMessageBox.Show("خطأ" + Environment.NewLine + ex.Message,
                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion
    }

    public class SalePurchRow
    {
        public string Column1 { get; set; }
        public string Column2 { get; set; }
        public string Column3 { get; set; }
        public string Column4 { get; set; }
        public string Column6 { get; set; }
        public string Column5 { get; set; }
    }
}