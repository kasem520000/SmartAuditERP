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
using Button = System.Windows.Controls.Button;
using Color = System.Windows.Media.Color;
using ColorConverter = System.Windows.Media.ColorConverter;
using FontFamily = System.Windows.Media.FontFamily;
using PrintDialog = System.Windows.Controls.PrintDialog;
using SaveFileDialog = Microsoft.Win32.SaveFileDialog;
using TextBox = System.Windows.Controls.TextBox;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmItemsalesdetailsPos : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;

        private int SelectedId = -1;
        private bool PrintHeader = true;
        private bool PrintFooter = true;
        private bool PrintStamp = true;
        private int PrintType = 0;
        private int PrintNo = 1;
        private string defPrinter = "";
        private string RptName = "";
        private string RptUrl = "";

        private double Sum1 = 0.0;
        private double Total = 0.0;
        private double qty = 0.0;
        private double PrimaryQnty = 0.0;
        private double VAT1 = 0.0;
        private double ItemSum = 0.0;
        private double ItemDiscount = 0.0;
        private double TotalBeforeTax = 0.0;

        private ObservableCollection<SalesDetailRow> _dataRows;

        #endregion

        #region Constructor

        public frmItemsalesdetailsPos()
        {
            conn = MainClass.ConnObj();
            _dataRows = new ObservableCollection<SalesDetailRow>();
            InitializeComponent();
        }

        #endregion

        #region Load

        private void frmInvDetails_Load(object sender, RoutedEventArgs e)
        {
            txtDateFrom.SelectedDate = DateTime.Today;
            txtDateTo.SelectedDate = DateTime.Today;
            txtStartTime.Text = "00:00";
            txtEndTime.Text = "23:59";

            LoadSafes();
            loadPrintSettings();
            LoadEmps();

            WindowState = MainClass.Window_State == WindowState.Maximized
                ? WindowState.Maximized
                : WindowState.Normal;
        }

        #endregion

        #region Data Loading

        public void LoadSafes()
        {
            try
            {
                string sql = MainClass.BranchNo != -1
                    ? $"select id,name from Safes where branch={MainClass.BranchNo} and status=1 and IS_Deleted=0 order by id"
                    : "select id,name from Safes where status=1 and IS_Deleted=0 order by id";

                // في هذه الواجهة لا يوجد cmbSafes مرئي، لكن الكود محفوظ
            }
            catch { }
        }

        private void LoadEmps()
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "select id,name from Employees where IS_Deleted=0 order by id", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                cmbusers.ItemsSource = dt.DefaultView;
                cmbusers.SelectedIndex = -1;
            }
            catch { }
        }

        private void loadPrintSettings()
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "select * from SettingPrint where Inv_Id=12", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                if (dt.Rows.Count != 1) return;

                try
                {
                    PrintType = Convert.ToInt32(dt.Rows[0]["printType"]);
                    PrintFooter = Convert.ToBoolean(dt.Rows[0]["PrintFooter"]);
                    PrintHeader = Convert.ToBoolean(dt.Rows[0]["PrintHeader"]);
                    PrintStamp = Convert.ToBoolean(dt.Rows[0]["PrintStamp"]);
                    defPrinter = dt.Rows[0]["CasherPrinter"]?.ToString() ?? "";

                    if (string.IsNullOrEmpty(defPrinter))
                        defPrinter = Common.GetDefaultPrinter();

                    PrintNo = Convert.ToInt32(dt.Rows[0]["printNo"]);
                }
                catch { }
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        #endregion

        #region Show Result

        private void btnShow_Click(object sender, RoutedEventArgs e)
        {
            ShowResult1();
        }

        private void ShowResult1()
        {
            try
            {
                _dataRows.Clear();
                GridControl1.ItemsSource = null;

                ResetSummaries();

                StringBuilder filterBuilder = new StringBuilder();

                if (!chkAllPeriod.IsChecked == true)
                {
                    filterBuilder.Append(" AND date >= @date1 AND date <= @date2 ");
                }

                string branchFilter = MainClass.BranchNo != -1
                    ? $"inv.branch={MainClass.BranchNo} AND "
                    : "";

                string sql = $@"
                    SELECT Inv.safe, Inv.proc_type, Inv.inv_type, date, Inv.id, ItemId,
                           ISNULL(val,0) AS val, ISNULL(val1,0) AS val1,
                           ISNULL(exchange_price,0) AS exchange_price,
                           ISNULL(discount,0) AS discount,
                           ((val1 * exchange_price) - discount) AS sum,
                           sales_emp, cust_id, unit, taxval,
                           Inv.PriceIncVAT
                    FROM Inv
                    INNER JOIN Inv_Sub ON Inv.InvGlobalID = Inv_Sub.InvGlobalID
                    WHERE {branchFilter} Inv.inv_type=3 AND Inv_Sub.ItemId > 0 AND Inv.IS_Deleted=0
                    {filterBuilder}
                    ORDER BY date DESC";

                SqlDataAdapter adapter = new SqlDataAdapter(sql, conn);

                DateTime dateFrom = txtDateFrom.SelectedDate ?? DateTime.Today;
                DateTime dateTo = (txtDateTo.SelectedDate ?? DateTime.Today).AddHours(24);

                adapter.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value
                    = dateFrom.ToShortDateString();
                adapter.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value
                    = dateTo.ToShortDateString();

                DataTable queryResult = new DataTable();
                adapter.Fill(queryResult);

                Dispatcher.Invoke(() =>
                {
                    ProgressBar1.Visibility = Visibility.Visible;
                    ProgressBar1.Maximum = queryResult.Rows.Count;
                    ProgressBar1.Value = 0;
                });

                int rowNumber = 0;

                foreach (DataRow row in queryResult.Rows)
                {
                    int procType = Convert.ToInt32(row["proc_type"]);
                    int invType = Convert.ToInt32(row["inv_type"]);

                    InvoiceObj invoiceObj = new InvoiceObj(invType, procType);

                    bool isValidRow = false;
                    bool isPlus = false;
                    string invTypeText = "";

                    if (procType == 1)
                    {
                        invTypeText = "نقطة بيع";
                        isPlus = true;
                        isValidRow = true;
                    }
                    else if (procType == 2)
                    {
                        invTypeText = "مرتجع نقطة البيع";
                        isPlus = false;
                        isValidRow = true;
                    }

                    if (!isValidRow)
                    {
                        Dispatcher.Invoke(() => ProgressBar1.Value++);
                        continue;
                    }

                    double sumVal = Convert.ToDouble(row["sum"]);
                    double taxVal = Convert.ToDouble(row["taxval"]);
                    // P7-096 fix: الكمية الأصلية لضرب السعر — تقريبها قبل
                    // الضرب كان يخالف قيمة السطر (عمود sum) المحسوبة من
                    // الكمية الأصلية (كميات الميزان الثلاثية الخانات)
                    double rawVal1 = Convert.ToDouble(row["val1"]);
                    double val1 = Math.Round(rawVal1, 2);
                    double exchPrice = Convert.ToDouble(row["exchange_price"]);
                    double discount = Convert.ToDouble(row["discount"]);

                    // P7-095 fix: علم شمول السعر للضريبة من الفاتورة المحفوظ
                    // (Inv.PriceIncVAT) — إعادة بناء InvoiceObj من إعدادات
                    // النوع الحالية كان يعيد تفسير فواتير قديمة بالإعداد
                    // الجديد فيظهر قبل/مع الضريبة مقلوبين
                    bool rowPriceIncVAT = Convert.ToBoolean(row["PriceIncVAT"]);

                    double totalBeforeTax = rowPriceIncVAT
                        ? sumVal - taxVal
                        : sumVal;

                    double totalWithTax = rowPriceIncVAT
                        ? sumVal
                        : sumVal + taxVal;

                    rowNumber++;

                    _dataRows.Add(new SalesDetailRow
                    {
                        DgvNo = rowNumber,
                        DgvStore = GetSafeName(Convert.ToInt32(row["safe"])),
                        DgvInvType = invTypeText,
                        DgvClient = GetCustName(Convert.ToInt32(row["cust_id"])),
                        DgvDate = Convert.ToDateTime(row["date"]).ToShortDateString(),
                        DgvInvNo = row["id"].ToString(),
                        DgvItem = GetCurrencyName(Convert.ToInt32(row["ItemId"])),
                        DgvUnit = Common.GetUnitName(Convert.ToInt32(row["unit"])),
                        DgvQty = val1,
                        DgvPrimaryQnty = Convert.ToDouble(row["val"]),
                        DgvPrice = exchPrice,
                        // P7-096 fix: المجموع من الكمية الأصلية
                        DgvItemSum = Math.Round(rawVal1 * exchPrice, 2),
                        DgvItemDiscount = discount,
                        DgvTotalBeforeTax = totalBeforeTax,
                        DgvVAT = taxVal,
                        DgvTotal = totalWithTax,
                        DgvUser = GetEmpName(Convert.ToInt32(row["sales_emp"])),
                        DgvInvGlobalID = "",
                        DgvIsPlus = isPlus ? 0 : 1
                    });

                    Dispatcher.Invoke(() => ProgressBar1.Value++);
                }

                Dispatcher.Invoke(() =>
                {
                    GridControl1.ItemsSource = _dataRows;
                    ProgressBar1.Visibility = Visibility.Collapsed;
                    lblRowCount.Text = $"عدد السجلات: {_dataRows.Count:N0}";
                    CalculateAndShowSummaries();
                });
            }
            catch (Exception ex)
            {
                ShowError(ex);
                ProgressBar1.Visibility = Visibility.Collapsed;
            }
        }

        #endregion

        #region Summaries

        private void ResetSummaries()
        {
            Sum1 = Total = qty = PrimaryQnty = VAT1 = ItemSum = ItemDiscount = TotalBeforeTax = 0.0;
        }

        private void CalculateAndShowSummaries()
        {
            ResetSummaries();

            foreach (SalesDetailRow row in _dataRows)
            {
                bool isReturn = row.DgvIsPlus == 1;

                if (!isReturn)
                {
                    qty += row.DgvQty;
                    PrimaryQnty += row.DgvPrimaryQnty;
                    ItemSum += row.DgvItemSum;
                    ItemDiscount += row.DgvItemDiscount;
                    TotalBeforeTax += row.DgvTotalBeforeTax;
                    VAT1 += row.DgvVAT;
                    Total += row.DgvTotal;
                }
                else
                {
                    qty -= row.DgvQty;
                    PrimaryQnty -= row.DgvPrimaryQnty;
                    ItemSum -= row.DgvItemSum;
                    ItemDiscount -= row.DgvItemDiscount;
                    TotalBeforeTax -= row.DgvTotalBeforeTax;
                    VAT1 -= row.DgvVAT;
                    Total -= row.DgvTotal;
                }
            }

            txtSummaryQty.Text = qty.ToString("N2");
            txtSummaryPrimary.Text = PrimaryQnty.ToString("N2");
            txtSummaryItemSum.Text = ItemSum.ToString("N2");
            txtSummaryDiscount.Text = ItemDiscount.ToString("N2");
            txtSummaryBeforeTax.Text = TotalBeforeTax.ToString("N2");
            txtSummaryVAT.Text = VAT1.ToString("N2");
            txtSummaryTotal.Text = Total.ToString("N2");
        }

        #endregion

        #region Filter Events

        private void ckAllUsers_CheckedChanged(object sender, RoutedEventArgs e)
        {
            // V-044 fix: الحدث ينطلق أثناء InitializeComponent (قيمة ابتدائية في XAML)
            // قبل إنشاء عناصر معرفة بعده — النداء المبكر كان يرمي NRE ويُفشل فتح النافذة
            if (cmbusers == null) return;
            if (!IsLoaded) return;
            cmbusers.IsEnabled = ckAllUsers.IsChecked != true;
            if (ckAllUsers.IsChecked == true)
                cmbusers.SelectedIndex = -1;
        }

        private void ckTotalPeriod_CheckedChanged(object sender, RoutedEventArgs e)
        {
            // V-044 fix: الحدث ينطلق أثناء InitializeComponent (قيمة ابتدائية في XAML)
            // قبل إنشاء عناصر معرفة بعده — النداء المبكر كان يرمي NRE ويُفشل فتح النافذة
            if (txtDateFrom == null || txtDateTo == null || txtEndTime == null || txtStartTime == null) return;
            if (!IsLoaded) return;
            bool enablePeriod = chkAllPeriod.IsChecked != true;
            txtDateFrom.IsEnabled = enablePeriod;
            txtDateTo.IsEnabled = enablePeriod;
            txtStartTime.IsEnabled = enablePeriod;
            txtEndTime.IsEnabled = enablePeriod;
        }

        #endregion

        #region Details Button

        private void Btn_Details_ButtonClick(object sender, RoutedEventArgs e)
        {
            try
            {
                Button btn = sender as Button;
                if (btn == null) return;

                SalesDetailRow row = btn.Tag as SalesDetailRow;
                if (row == null) return;

                string invType = row.DgvInvType;
                string invNo = row.DgvInvNo;

                if (invType == "نقطة بيع")
                {
                    frmInvPOS posForm = new frmInvPOS();
                    posForm.Show();
                    posForm.ProcType = 1;
                    posForm.InvType = 3;
                    posForm.WindowState = WindowState.Maximized;
                    posForm.Navigate($"select * from Inv where IS_Deleted=0 and inv_type=3 and proc_type=1 and id={invNo}");
                    posForm.Activate();
                }
                else if (invType == "مرتجع نقطة البيع")
                {
                    frmInvPOS posForm = new frmInvPOS();
                    posForm.Show();
                    posForm.ProcType = 2;
                    posForm.Title = "مرتجع";
                    posForm.InvType = 3;
                    posForm.WindowState = WindowState.Maximized;
                    posForm.Navigate($"select * from Inv where IS_Deleted=0 and inv_type=3 and proc_type=2 and id={invNo}");
                    posForm.Activate();
                }
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        #endregion

        #region Search

        private void btnSearch_Click(object sender, RoutedEventArgs e)
        {
            addNewItem();
        }

        private void txtItemName_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (e.Key == System.Windows.Input.Key.Return
                && !string.IsNullOrWhiteSpace(((TextBox)sender).Text))
            {
                SearchByName();
            }
        }

        private void txtItemCode_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (e.Key == System.Windows.Input.Key.Return
                && !string.IsNullOrWhiteSpace(((TextBox)sender).Text))
            {
                SearchByCode();
            }
        }

        private void SearchByName()
        {
            // مخصصة للاستخدام المستقبلي
        }

        private void SearchByCode()
        {
            // مخصصة للاستخدام المستقبلي
        }

        private void addNewItem()
        {
            frmItemsSrch srchForm = new frmItemsSrch();
            MainClass.ApplyPermissionToForm(srchForm);
            MainClass.DoApplyUserSett(srchForm);
            srchForm.sql = "select id, name, nameEN, sale_price, unit from Items where IS_Deleted=0 order by id";
            srchForm.search = "select id, name, nameEN, sale_price, unit from Items";
            srchForm.ShowDialog();

            if (srchForm.ISDone && srchForm.ItemId > 0)
            {
                SelectedId = srchForm.ItemId;
            }
        }

        private void GroupBox1_Enter(object sender, RoutedEventArgs e) { }

        #endregion

        #region Print / Export

        private void btnPreview_Click(object sender, RoutedEventArgs e)
        {
            PrintDevexpress(2);
        }

        private void btnPrint_Click(object sender, RoutedEventArgs e)
        {
            PrintDevexpress(1);
        }

        private void PrintDevexpress(int printMode)
        {
            try
            {
                RptUrl = MainClass.ReportsPath;
                RptName = "rptInvDetailsPos.repx";
                defPrinter = MainClass.ReportsPrinter;

                if (_dataRows == null || _dataRows.Count == 0)
                {
                    DXMessageBox.Show("لا توجد عمليات بالجدول", "",
                        MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                // P7-097 fix: مسار الطباعة FlowDocument لا يحمّل ملف REPX
                // أصلًا — فحص وجوده كان يحجب الطباعة/المعاينة على ملف لا
                // يعتمد عليه المسار

                FlowDocument document = BuildPrintDocument();

                if (printMode == 2)
                {
                    ShowPreviewWindow(document);
                }
                else
                {
                    PrintDialog printDialog = new PrintDialog();
                    if (printDialog.ShowDialog() == true)
                    {
                        document.PageHeight = printDialog.PrintableAreaHeight;
                        document.PageWidth = printDialog.PrintableAreaWidth;
                        document.PagePadding = new Thickness(25);
                        document.ColumnGap = 0;
                        document.ColumnWidth = printDialog.PrintableAreaWidth;

                        IDocumentPaginatorSource source = document;
                        printDialog.PrintDocument(source.DocumentPaginator, Title);
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
                FontFamily = new FontFamily("Tahoma"),
                FontSize = 10,
                PagePadding = new Thickness(20),
                ColumnWidth = 1400
            };

            Paragraph title = new Paragraph(new Run(Title))
            {
                FontSize = 16,
                FontWeight = FontWeights.Bold,
                TextAlignment = TextAlignment.Center,
                Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#213A7A"))
            };
            doc.Blocks.Add(title);

            string periodText = chkAllPeriod.IsChecked == true
                ? "كل الفترة"
                : $"من {txtDateFrom.SelectedDate?.ToShortDateString()} إلى {txtDateTo.SelectedDate?.ToShortDateString()}";

            Paragraph info = new Paragraph(new Run($"📅 الفترة: {periodText}"))
            {
                FontSize = 11,
                FontWeight = FontWeights.Bold,
                Margin = new Thickness(0, 0, 0, 10)
            };
            doc.Blocks.Add(info);

            Table table = new Table { CellSpacing = 0 };
            for (int i = 0; i < 10; i++)
                table.Columns.Add(new TableColumn());

            TableRowGroup group = new TableRowGroup();
            table.RowGroups.Add(group);

            TableRow headerRow = new TableRow();
            group.Rows.Add(headerRow);
            AddHeaderCell(headerRow, "م");
            AddHeaderCell(headerRow, "المادة");
            AddHeaderCell(headerRow, "نوع العملية");
            AddHeaderCell(headerRow, "التاريخ");
            AddHeaderCell(headerRow, "الرقم");
            AddHeaderCell(headerRow, "الكمية");
            AddHeaderCell(headerRow, "السعر");
            AddHeaderCell(headerRow, "الخصم");
            AddHeaderCell(headerRow, "الضريبة");
            AddHeaderCell(headerRow, "الإجمالي");

            foreach (SalesDetailRow item in _dataRows)
            {
                TableRow row = new TableRow();
                group.Rows.Add(row);
                AddBodyCell(row, item.DgvNo.ToString());
                AddBodyCell(row, item.DgvItem);
                AddBodyCell(row, item.DgvInvType);
                AddBodyCell(row, item.DgvDate);
                AddBodyCell(row, item.DgvInvNo);
                AddBodyCell(row, item.DgvQty.ToString("N2"));
                AddBodyCell(row, item.DgvPrice.ToString("N2"));
                AddBodyCell(row, item.DgvItemDiscount.ToString("N2"));
                AddBodyCell(row, item.DgvVAT.ToString("N2"));
                AddBodyCell(row, item.DgvTotal.ToString("N2"));
            }

            doc.Blocks.Add(table);

            Paragraph totals = new Paragraph
            {
                Margin = new Thickness(0, 10, 0, 0),
                FontWeight = FontWeights.Bold
            };
            totals.Inlines.Add(new Run($"الكمية: {txtSummaryQty.Text}    "));
            totals.Inlines.Add(new Run($"المجموع: {txtSummaryItemSum.Text}    "));
            totals.Inlines.Add(new Run($"الضريبة: {txtSummaryVAT.Text}    "));
            totals.Inlines.Add(new Run($"الإجمالي: {txtSummaryTotal.Text}"));
            doc.Blocks.Add(totals);

            return doc;
        }

        private void ShowPreviewWindow(FlowDocument document)
        {
            System.Windows.Window previewWindow = new System.Windows.Window
            {
                Title = "معاينة قبل الطباعة",
                Width = 1100,
                Height = 700,
                WindowStartupLocation = WindowStartupLocation.CenterScreen,
                FlowDirection = System.Windows.FlowDirection.RightToLeft,
                Background = Brushes.White
            };

            DocumentViewer viewer = new DocumentViewer { Document = document };
            previewWindow.Content = viewer;
            previewWindow.ShowDialog();
        }

        private void AddHeaderCell(TableRow row, string text)
        {
            TableCell cell = new TableCell(new Paragraph(new Run(text)))
            {
                Background = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#DDE7FF")),
                BorderBrush = Brushes.Gray,
                BorderThickness = new Thickness(0.5),
                Padding = new Thickness(4)
            };
            cell.Blocks.FirstBlock.SetValue(TextElement.FontWeightProperty, FontWeights.Bold);
            cell.Blocks.FirstBlock.SetValue(Block.TextAlignmentProperty, TextAlignment.Center);
            row.Cells.Add(cell);
        }

        private void AddBodyCell(TableRow row, string text)
        {
            TableCell cell = new TableCell(new Paragraph(new Run(text ?? "")))
            {
                BorderBrush = Brushes.Gray,
                BorderThickness = new Thickness(0.5),
                Padding = new Thickness(3)
            };
            cell.Blocks.FirstBlock.SetValue(Block.TextAlignmentProperty, TextAlignment.Center);
            row.Cells.Add(cell);
        }

        private void btnExport_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_dataRows == null || _dataRows.Count == 0)
                {
                    DXMessageBox.Show("لا توجد بيانات للتصدير.", "",
                        MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                // P7-050 fix: الامتداد المعروض هو المكتوب فعلاً — xlsx ملف Excel
                // حقيقي (ClosedXML)، وcsv بترميز الخلايا الموحّد (P7-048/049)،
                // وhtml لجدول HTML الحقيقي (كان خيار xls يكتب HTML)
                SaveFileDialog saveDialog = new SaveFileDialog
                {
                    FileName = Title.Replace(" ", "_"),
                    Filter   = DelimitedExport.ExcelCsvHtmlFilter
                };

                if (saveDialog.ShowDialog() != true) return;

                string exportPath = saveDialog.FileName;
                if (exportPath.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase))
                    ExportToExcelClosedXml(exportPath);
                else if (exportPath.EndsWith(".html", StringComparison.OrdinalIgnoreCase))
                    ExportToExcelHtml(exportPath);
                else
                    ExportToCsv(exportPath);

                Process.Start(new ProcessStartInfo(exportPath) { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        /// <summary>
        /// P7-048/049 fix: CSV بترميز الخلايا الموحّد — الفاصلة والاقتباسات
        /// والأسطر وبادئات الصيغ (كان اقتباس يدوي بلا حماية بادئات الصيغ).
        /// </summary>
        private void ExportToCsv(string fileName)
        {
            DelimitedExport.WriteFile(fileName,
                new[]
                {
                    "م", "المستودع", "نوع العملية", "المورد", "التاريخ",
                    "الرقم", "المادة", "الوحدة", "الكمية", "السعر",
                    "المجموع", "الخصم", "قبل الضريبة", "الضريبة",
                    "الإجمالي", "المستخدم"
                },
                _dataRows.Select(item => new[]
                {
                    item.DgvNo.ToString(),
                    item.DgvStore,
                    item.DgvInvType,
                    item.DgvClient,
                    item.DgvDate,
                    item.DgvInvNo,
                    item.DgvItem,
                    item.DgvUnit,
                    item.DgvQty.ToString("N2"),
                    item.DgvPrice.ToString("N2"),
                    item.DgvItemSum.ToString("N2"),
                    item.DgvItemDiscount.ToString("N2"),
                    item.DgvTotalBeforeTax.ToString("N2"),
                    item.DgvVAT.ToString("N2"),
                    item.DgvTotal.ToString("N2"),
                    item.DgvUser
                }));
        }

        /// <summary>
        /// P7-050 fix: ملف xlsx حقيقي عبر ClosedXML — الأعمدة الرقمية أرقام
        /// (نمط frmInvDetails).
        /// </summary>
        private void ExportToExcelClosedXml(string fileName)
        {
            using var workbook = new ClosedXML.Excel.XLWorkbook();
            var worksheet = workbook.Worksheets.Add("تفاصيل المبيعات");

            string[] headers =
            {
                "م", "المستودع", "نوع العملية", "المورد", "التاريخ",
                "الرقم", "المادة", "الوحدة", "الكمية", "السعر",
                "المجموع", "الخصم", "قبل الضريبة", "الضريبة",
                "الإجمالي", "المستخدم"
            };
            for (int c = 0; c < headers.Length; c++)
            {
                var cell = worksheet.Cell(1, c + 1);
                cell.Value = headers[c];
                cell.Style.Font.Bold = true;
            }

            int rowIdx = 2;
            foreach (SalesDetailRow item in _dataRows)
            {
                worksheet.Cell(rowIdx, 1).Value = item.DgvNo;
                worksheet.Cell(rowIdx, 2).Value = item.DgvStore;
                worksheet.Cell(rowIdx, 3).Value = item.DgvInvType;
                worksheet.Cell(rowIdx, 4).Value = item.DgvClient;
                worksheet.Cell(rowIdx, 5).Value = item.DgvDate;
                worksheet.Cell(rowIdx, 6).Value = item.DgvInvNo;
                worksheet.Cell(rowIdx, 7).Value = item.DgvItem;
                worksheet.Cell(rowIdx, 8).Value = item.DgvUnit;
                worksheet.Cell(rowIdx, 9).Value = item.DgvQty;
                worksheet.Cell(rowIdx, 10).Value = item.DgvPrice;
                worksheet.Cell(rowIdx, 11).Value = item.DgvItemSum;
                worksheet.Cell(rowIdx, 12).Value = item.DgvItemDiscount;
                worksheet.Cell(rowIdx, 13).Value = item.DgvTotalBeforeTax;
                worksheet.Cell(rowIdx, 14).Value = item.DgvVAT;
                worksheet.Cell(rowIdx, 15).Value = item.DgvTotal;
                worksheet.Cell(rowIdx, 16).Value = item.DgvUser;

                const string numberFormat = "#,##0.00";
                foreach (int col in new[] { 9, 10, 11, 12, 13, 14, 15 })
                    worksheet.Cell(rowIdx, col).Style.NumberFormat.Format = numberFormat;

                rowIdx++;
            }

            worksheet.Columns().AdjustToContents();
            workbook.SaveAs(fileName);
        }

        // P7-098 fix: ترميز HTML لنصوص البيانات
        private static string EscapeHtml(string value)
            => (value ?? "").Replace("&", "&amp;")
                             .Replace("<", "&lt;")
                             .Replace(">", "&gt;");

        private void ExportToExcelHtml(string fileName)
        {
            StringBuilder sb = new StringBuilder();
            sb.AppendLine("<html><head><meta charset='utf-8'/>");
            sb.AppendLine("<style>table{border-collapse:collapse;font-family:Tahoma;font-size:11px;}");
            sb.AppendLine("th,td{border:1px solid #999;padding:4px;text-align:center;}");
            sb.AppendLine("th{background:#DDE7FF;font-weight:bold;}</style></head>");
            sb.AppendLine("<body dir='rtl'>");
            sb.AppendLine($"<h2 style='text-align:center;'>{EscapeHtml(Title)}</h2>");
            sb.AppendLine("<table><tr>");
            sb.AppendLine("<th>م</th><th>المستودع</th><th>نوع العملية</th><th>المورد</th><th>التاريخ</th>");
            sb.AppendLine("<th>الرقم</th><th>المادة</th><th>الوحدة</th><th>الكمية</th><th>السعر</th>");
            sb.AppendLine("<th>المجموع</th><th>الخصم</th><th>قبل الضريبة</th><th>الضريبة</th><th>الإجمالي</th><th>المستخدم</th>");
            sb.AppendLine("</tr>");

            foreach (SalesDetailRow item in _dataRows)
            {
                sb.AppendLine("<tr>");
                // P7-098 fix: ترميز HTML لنصوص البيانات — اسم/وحدة/مورد
                // بحروف < > & كان يكسر الجدول أو يحقن ترميزاً
                sb.AppendLine($"<td>{item.DgvNo}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvStore)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvInvType)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvClient)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvDate)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvInvNo)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvItem)}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvUnit)}</td>");
                sb.AppendLine($"<td>{item.DgvQty:N2}</td>");
                sb.AppendLine($"<td>{item.DgvPrice:N2}</td>");
                sb.AppendLine($"<td>{item.DgvItemSum:N2}</td>");
                sb.AppendLine($"<td>{item.DgvItemDiscount:N2}</td>");
                sb.AppendLine($"<td>{item.DgvTotalBeforeTax:N2}</td>");
                sb.AppendLine($"<td>{item.DgvVAT:N2}</td>");
                sb.AppendLine($"<td>{item.DgvTotal:N2}</td>");
                sb.AppendLine($"<td>{EscapeHtml(item.DgvUser)}</td>");
                sb.AppendLine("</tr>");
            }

            sb.AppendLine("</table></body></html>");
            File.WriteAllText(fileName, sb.ToString(), Encoding.UTF8);
        }

        #endregion

        #region Helpers

        private string GetCurrencyName(int currencyId)
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "select name,nameEN from Items where id=" + currencyId, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                if (dt.Rows.Count > 0)
                    return string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                        ? dt.Rows[0][0].ToString()
                        : dt.Rows[0][1].ToString();

                return "";
            }
            catch { return ""; }
        }

        private string GetEmpName(int empId)
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "select name from Employees where id=" + empId, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                return dt.Rows.Count > 0 ? dt.Rows[0][0].ToString() : "";
            }
            catch { return ""; }
        }

        private string GetSafeName(int safeId)
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "select name from Safes where id=" + safeId, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                return dt.Rows.Count > 0 ? dt.Rows[0][0].ToString() : "";
            }
            catch { return ""; }
        }

        private string GetCustName(int custId)
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "select name from Customers where id=" + custId, conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                return dt.Rows.Count > 0 ? dt.Rows[0][0].ToString() : "";
            }
            catch { return ""; }
        }

        private void btnClose_Click(object sender, RoutedEventArgs e) => Close();

        private void ShowError(Exception ex)
        {
            DXMessageBox.Show("خطأ" + Environment.NewLine + "تفاصيل الخطأ: " + ex.Message,
                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion
    }

    public class SalesDetailRow
    {
        public int DgvNo { get; set; }
        public string DgvStore { get; set; }
        public string DgvInvType { get; set; }
        public string DgvClient { get; set; }
        public string DgvDate { get; set; }
        public string DgvInvNo { get; set; }
        public string DgvItem { get; set; }
        public string DgvUnit { get; set; }
        public double DgvQty { get; set; }
        public double DgvPrimaryQnty { get; set; }
        public double DgvPrice { get; set; }
        public double DgvItemSum { get; set; }
        public double DgvItemDiscount { get; set; }
        public double DgvTotalBeforeTax { get; set; }
        public double DgvVAT { get; set; }
        public double DgvTotal { get; set; }
        public string DgvUser { get; set; }
        public string DgvInvGlobalID { get; set; }
        public int DgvIsPlus { get; set; }
    }
}