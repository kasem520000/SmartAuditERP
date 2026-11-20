using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Media;
using DevExpress.Xpf.Core;
using Microsoft.Win32;
using Color = System.Windows.Media.Color;
using ColorConverter = System.Windows.Media.ColorConverter;
using FontFamily = System.Windows.Media.FontFamily;
using PrintDialog = System.Windows.Controls.PrintDialog;
using SaveFileDialog = Microsoft.Win32.SaveFileDialog;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmMezanyaArba7 : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;
        private int    _ParentCode = -1;
        public  int    _Type       = 1;
        public  int    _FormType   = 1;
        public  double _Stock      = 0.0;
        // R-137 (P7-117): zero can be an explicitly approved inventory value.
        private bool _hasApprovedStock;

        private bool   PrintHeader = true;
        private bool   PrintFooter = true;
        private bool   PrintStamp  = true;
        private int    PrintType   = 0;
        private int    PrintNo     = 1;
        private string defPrinter  = "";
        private string RptName     = "";
        private string RptUrl      = "";

        private ObservableCollection<AccountBalanceRow> _rows;

        #endregion

        #region Constructor

        public frmMezanyaArba7()
        {
            conn  = MainClass.ConnObj();
            _rows = new ObservableCollection<AccountBalanceRow>();
            InitializeComponent();
        }

        #endregion

        #region Load

        private void frmMezanyaArba7_Load(object sender, RoutedEventArgs e)
        {
            txtToDate.SelectedDate   = DateTime.Today;
            txtFromDate.SelectedDate = DateTime.Today;
            txtStartTime.Text = "00:00";
            txtEndTime.Text   = "23:59";

            dgvSrch.ItemsSource = _rows;

            LoadPrintSettings();
            LoadBranches();
            BranchPermissionsi();
        }

        #endregion

        #region CheckBox Events

        private void ckTotalPeriod_CheckedChanged(object sender, RoutedEventArgs e)
        {
            bool allPeriod = ckTotalPeriod.IsChecked == true;
            if (txtFromDate   != null) txtFromDate.IsEnabled   = !allPeriod;
            if (txtToDate     != null) txtToDate.IsEnabled     = !allPeriod;
            if (txtStartTime  != null) txtStartTime.IsEnabled  = !allPeriod;
            if (txtEndTime    != null) txtEndTime.IsEnabled    = !allPeriod;
        }

        private void ckAllBranches_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (cmbBranches == null) return;
            if (IsLoaded) InvalidateBranchResult();
            if (ckAllBranches.IsChecked == true)
            {
                cmbBranches.IsEnabled     = false;
                cmbBranches.SelectedIndex = -1;
            }
            else
            {
                cmbBranches.IsEnabled = true;
            }
        }

        private void cmbBranches_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (IsLoaded) InvalidateBranchResult();
        }

        private void InvalidateBranchResult()
        {
            _rows.Clear();
            _hasApprovedStock = false;
            _Stock = 0;
            txtDeptDiff.Text = txtCreditDiff.Text = txtIsBalanced.Text = "";
        }

        #endregion

        #region Branches

        private void LoadBranches()
        {
            try
            {
                string branchFilter = "";
                if (MainClass.BranchNo != -1)
                {
                    branchFilter = string.IsNullOrWhiteSpace(Accounting.BranchCondition)
                        ? ""
                        : $" and id={MainClass.BranchNo}";
                }

                SqlDataAdapter adapter = new SqlDataAdapter(
                    $"select id,name from Branches where IS_Deleted=0 {branchFilter}", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                cmbBranches.ItemsSource = dt.DefaultView;

                if (MainClass.BranchNo != -1)
                    cmbBranches.SelectedValue = MainClass.BranchNo;
                else
                    cmbBranches.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        private void BranchPermissionsi()
        {
            if (!string.IsNullOrWhiteSpace(Accounting.BranchCondition))
            {
                if (cmbBranches.Items.Count > 0)
                    cmbBranches.SelectedIndex = 0;
            }
        }

        #endregion

        #region GetParent

        private void GetParent(int Code)
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    $"select ParentCode from Accounts_Index where Code={Code}", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                if (dt.Rows.Count > 0)
                {
                    double parentVal = 0;
                    double.TryParse(dt.Rows[0][0].ToString(), out parentVal);

                    if (parentVal < 10.0)
                        _ParentCode = Code;
                    else
                        GetParent((int)parentVal);
                }
                else
                {
                    _ParentCode = -1;
                }
            }
            catch { _ParentCode = -1; }
        }

        #endregion

        #region Show Result

        private void btnShow_Click(object sender, RoutedEventArgs e)
        {
            ShowResult();
        }

        private void ShowResult()
        {
            try
            {
                _rows.Clear();
                txtDeptDiff.Text   = "";
                txtCreditDiff.Text = "";
                txtIsBalanced.Text = "";
                txtIsBalanced.Foreground = new SolidColorBrush(Colors.Red);

                DateTime dateTimeFrom = BuildDateTime(txtFromDate.SelectedDate ?? DateTime.Today, txtStartTime.Text, new TimeSpan(0, 0, 0));
                DateTime dateTimeTo   = BuildDateTime(txtToDate.SelectedDate ?? DateTime.Today, txtEndTime.Text, new TimeSpan(23, 59, 0));

                if (ckAllBranches.IsChecked == true || cmbBranches.SelectedIndex < 0 ||
                    cmbBranches.SelectedValue == null ||
                    !int.TryParse(cmbBranches.SelectedValue.ToString(), out int branchId) || branchId <= 0)
                {
                    DXMessageBox.Show("عرض كل الفروع غير متاح حتى توحيد نطاق الأستاذ والمخزون؛ اختر فرعاً واحداً.",
                        "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }
                int? selectedBranch = branchId;

                string whereClause = "WHERE Entry.IS_Deleted=0 AND Entry.state=1 AND Entry.GlobalId=Entry_sub.EntryGlobalId AND Entry_sub.acc_no=Accounts_Index.Code AND Accounts_Index.FinalAcc=1 ";

                if (ckTotalPeriod.IsChecked != true)
                    whereClause += " AND Entry.date BETWEEN @date1 AND @date2 ";

                if (selectedBranch.HasValue)
                    whereClause += " AND Entry_sub.branch=@branch ";

                string sql = $@"
                    SELECT Entry_sub.acc_no AS AccountCode,
                           Accounts_Index.AName AS AccountName,
                           SUM(Entry_sub.dept)   AS Debet,
                           SUM(Entry_sub.credit) AS Credit
                    FROM Entry
                    INNER JOIN Entry_sub ON Entry.GlobalId=Entry_sub.EntryGlobalId
                    INNER JOIN Accounts_Index ON Entry_sub.acc_no=Accounts_Index.Code
                    {whereClause}
                    GROUP BY Entry_sub.acc_no, Accounts_Index.AName";

                DataTable queryResult = new DataTable();
                using (SqlCommand cmd = new SqlCommand(sql, conn))
                {
                    if (ckTotalPeriod.IsChecked != true)
                    {
                        cmd.Parameters.Add("@date1", SqlDbType.DateTime).Value = dateTimeFrom;
                        cmd.Parameters.Add("@date2", SqlDbType.DateTime).Value = dateTimeTo;
                    }

                    if (selectedBranch.HasValue)
                        cmd.Parameters.Add("@branch", SqlDbType.Int).Value = selectedBranch.Value;

                    if (conn.State != System.Data.ConnectionState.Open)
                        conn.Open();

                    using SqlDataAdapter adapter = new SqlDataAdapter(cmd);
                    adapter.Fill(queryResult);
                }
                conn.Close();

                DataTable groupedTable = new DataTable();
                groupedTable.Columns.Add("code",   typeof(int));
                groupedTable.Columns.Add("name",   typeof(string));
                groupedTable.Columns.Add("dept",   typeof(double));
                groupedTable.Columns.Add("credit", typeof(double));

                if (_Type == 1)
                {
                    // تجميع حسب الحساب الرئيسي
                    for (int i = 0; i < queryResult.Rows.Count; i++)
                    {
                        int    accCode = Convert.ToInt32(queryResult.Rows[i]["AccountCode"]);
                        double dept    = 0;
                        double credit  = 0;
                        double.TryParse(queryResult.Rows[i]["Debet"].ToString(), out dept);
                        double.TryParse(queryResult.Rows[i]["Credit"].ToString(), out credit);

                        _ParentCode = -1;
                        GetParent(accCode);

                        int parentCode = _ParentCode > 0 ? _ParentCode : accCode;

                        string accName = "";
                        SqlDataAdapter nameAdapter = new SqlDataAdapter(
                            $"SELECT AName FROM Accounts_Index WHERE Code={parentCode}", conn);
                        DataTable nameDt = new DataTable();
                        nameAdapter.Fill(nameDt);
                        accName = nameDt.Rows.Count > 0
                            ? nameDt.Rows[0][0].ToString()
                            : queryResult.Rows[i]["AccountName"].ToString();

                        DataRow[] existing = groupedTable.Select($"code={parentCode}");
                        if (existing.Length > 0)
                        {
                            existing[0]["dept"]   = Convert.ToDouble(existing[0]["dept"])   + dept;
                            existing[0]["credit"] = Convert.ToDouble(existing[0]["credit"]) + credit;
                        }
                        else
                        {
                            DataRow newRow = groupedTable.NewRow();
                            newRow["code"]   = parentCode;
                            newRow["name"]   = accName;
                            newRow["dept"]   = dept;
                            newRow["credit"] = credit;
                            groupedTable.Rows.Add(newRow);
                        }
                    }
                }
                else
                {
                    for (int j = 0; j < queryResult.Rows.Count; j++)
                    {
                        double dept   = 0;
                        double credit = 0;
                        double.TryParse(queryResult.Rows[j]["Debet"].ToString(), out dept);
                        double.TryParse(queryResult.Rows[j]["Credit"].ToString(), out credit);

                        if (Math.Round(dept, 2) != Math.Round(credit, 2))
                        {
                            DataRow newRow = groupedTable.NewRow();
                            newRow["code"]   = Convert.ToInt32(queryResult.Rows[j]["AccountCode"]);
                            newRow["name"]   = queryResult.Rows[j]["AccountName"].ToString();
                            newRow["dept"]   = dept;
                            newRow["credit"] = credit;
                            groupedTable.Rows.Add(newRow);
                        }
                    }
                }

                // حساب المخزون
                int    inventoryCode = 1270001;
                string inventoryName = "حساب المخزون";
                SqlDataAdapter invNameAdapter = new SqlDataAdapter("SELECT AName FROM Accounts_Index WHERE Code=1270001", conn);
                DataTable invNameDt = new DataTable();
                invNameAdapter.Fill(invNameDt);
                if (invNameDt.Rows.Count > 0)
                    inventoryName = invNameDt.Rows[0][0].ToString();

                double stockCost = (_hasApprovedStock || _Stock != 0.0)
                    ? _Stock
                    : Inventory.InventoryCost(selectedBranch.HasValue ? selectedBranch.Value : MainClass.BranchNo, txtToDate.SelectedDate ?? DateTime.Today);

                DataRow[] inventoryExisting = groupedTable.Select($"code={inventoryCode}");
                if (inventoryExisting.Length > 0)
                    inventoryExisting[0]["dept"] = Convert.ToDouble(inventoryExisting[0]["dept"]) + stockCost;
                else
                {
                    DataRow invRow = groupedTable.NewRow();
                    invRow["code"]   = inventoryCode;
                    invRow["name"]   = inventoryName;
                    invRow["dept"]   = stockCost;
                    invRow["credit"] = 0.0;
                    groupedTable.Rows.Add(invRow);
                }

                double totalDebt = 0.0, totalCredit = 0.0;

                foreach (DataRow row in groupedTable.Rows)
                {
                    double dept   = 0;
                    double credit = 0;
                    double.TryParse(row["dept"].ToString(), out dept);
                    double.TryParse(row["credit"].ToString(), out credit);

                    double debtDisplay   = dept   >= credit ? Math.Round(dept   - credit, 2) : 0;
                    double creditDisplay = credit  > dept   ? Math.Round(credit - dept,   2) : 0;

                    _rows.Add(new AccountBalanceRow
                    {
                        Column1 = row["code"].ToString(),
                        Column2 = row["name"].ToString(),
                        Column5 = debtDisplay.ToString(Common.DigitsNo),
                        Column6 = creditDisplay.ToString(Common.DigitsNo)
                    });

                    totalDebt   += debtDisplay;
                    totalCredit += creditDisplay;
                }

                // صف الأرباح والخسائر
                int    pnlCode = 2130001;
                string pnlName = "أرباح و خسائر";
                SqlDataAdapter pnlAdapter = new SqlDataAdapter("SELECT AName FROM Accounts_Index WHERE Code=2130001", conn);
                DataTable pnlDt = new DataTable();
                pnlAdapter.Fill(pnlDt);
                if (pnlDt.Rows.Count > 0)
                    pnlName = pnlDt.Rows[0][0].ToString();

                double pnlDebt = 0, pnlCredit = 0;
                if (totalDebt > totalCredit)
                    pnlCredit = Math.Round(totalDebt - totalCredit, 2);
                else if (totalCredit > totalDebt)
                    pnlDebt   = Math.Round(totalCredit - totalDebt, 2);

                _rows.Add(new AccountBalanceRow
                {
                    Column1 = pnlCode.ToString(),
                    Column2 = pnlName,
                    Column5 = pnlDebt.ToString(Common.DigitsNo),
                    Column6 = pnlCredit.ToString(Common.DigitsNo)
                });

                totalDebt   += pnlDebt;
                totalCredit += pnlCredit;

                txtDeptDiff.Text   = totalDebt.ToString(Common.DigitsNo);
                txtCreditDiff.Text = totalCredit.ToString(Common.DigitsNo);

                bool isBalanced = Math.Round(totalDebt, 2) == Math.Round(totalCredit, 2);
                txtIsBalanced.Text       = isBalanced ? "✅ الحسابات متوازنة" : "❌ الحسابات غير متوازنة";
                txtIsBalanced.Foreground = isBalanced
                    ? new SolidColorBrush(Colors.Green)
                    : new SolidColorBrush(Colors.Red);

                UpdateRowCount();
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
            finally
            {
                if (conn.State == System.Data.ConnectionState.Open)
                    conn.Close();
            }
        }

        private DateTime BuildDateTime(DateTime datePart, string timeText, TimeSpan defaultTime)
        {
            if (TimeSpan.TryParse(timeText?.Trim(), out TimeSpan ts))
                return datePart.Date.Add(ts);
            return datePart.Date.Add(defaultTime);
        }

        #endregion

        #region Stock

        private void BtnStock_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                frmSafeGrd safeGrd = new frmSafeGrd();
                safeGrd.BtnAprroved.Visibility = Visibility.Visible;
                safeGrd.ShowDialog();

                if (safeGrd.ISDone)
                {
                    _Stock = safeGrd._stockTotal;
                    _hasApprovedStock = true;
                }
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
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

                SaveFileDialog saveDialog = new SaveFileDialog
                {
                    FileName   = "أرباح_وخسائر",
                    // Repair R-090 (audit finding P7-050): both options used to land in the same HTML
                    // writer, so picking *.csv produced an HTML document under a CSV name. The *.xls
                    // option keeps that HTML table - Excel opens it, and the label now says what the
                    // bytes are - while *.csv gets a real comma-separated file from the shared writer.
                    Filter     = "Excel File - HTML table (*.xls)|*.xls|CSV File (*.csv)|*.csv",
                    DefaultExt = ".xls"
                };

                if (saveDialog.ShowDialog() != true) return;

                // Repair R-090 (audit finding P7-050): the written format follows the chosen
                // extension, so *.csv is comma-separated text and *.xls is the HTML table this screen
                // has always written.
                if (saveDialog.FileName.EndsWith(".csv", StringComparison.OrdinalIgnoreCase))
                    ExportToCsv(saveDialog.FileName);
                else
                    ExportToExcelHtml(saveDialog.FileName);
                Process.Start(new ProcessStartInfo(saveDialog.FileName) { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        private void ExportToExcelHtml(string fileName)
        {
            // R-134 (P7-098): HTML text cells must not be interpreted as markup.
            StringBuilder sb = new StringBuilder();
            sb.AppendLine("<html><head><meta charset='utf-8'/>");
            sb.AppendLine("<style>table{border-collapse:collapse;font-family:Tahoma;font-size:11px;}");
            sb.AppendLine("th,td{border:1px solid #999;padding:4px;text-align:center;}");
            sb.AppendLine("th{background:#DDE7FF;font-weight:bold;}</style></head>");
            sb.AppendLine("<body dir='rtl'>");
            sb.AppendLine($"<h2 style='text-align:center;'>{System.Net.WebUtility.HtmlEncode(Title)}</h2>");
            sb.AppendLine("<table><tr><th>الحساب</th><th>إسم الحساب</th><th>رصيد مدين</th><th>رصيد دائن</th></tr>");

            foreach (AccountBalanceRow row in _rows)
            {
                sb.AppendLine("<tr>");
                sb.AppendLine($"<td>{System.Net.WebUtility.HtmlEncode(row.Column1)}</td><td>{System.Net.WebUtility.HtmlEncode(row.Column2)}</td><td>{System.Net.WebUtility.HtmlEncode(row.Column5)}</td><td>{System.Net.WebUtility.HtmlEncode(row.Column6)}</td>");
                sb.AppendLine("</tr>");
            }

            sb.AppendLine($"<tr><td colspan='2'><b>الإجمالي</b></td><td>{System.Net.WebUtility.HtmlEncode(txtDeptDiff.Text)}</td><td>{System.Net.WebUtility.HtmlEncode(txtCreditDiff.Text)}</td></tr>");
            sb.AppendLine("</table></body></html>");

            File.WriteAllText(fileName, sb.ToString(), Encoding.UTF8);
        }

        /// <summary>
        /// Repair R-090 (audit finding P7-050): the same four columns and the same totals record the
        /// HTML table carries, as comma-separated text under the announced schema (comma, doubled
        /// quotes, CRLF, UTF-8). Every cell is the screen's own text and passes through unchanged.
        /// </summary>
        private void ExportToCsv(string fileName)
        {
            var export = SpreadsheetExport.Begin(fileName, SpreadsheetExport.CsvDelimiter);
            export.Header("الحساب", "إسم الحساب", "رصيد مدين", "رصيد دائن");

            foreach (AccountBalanceRow row in _rows)
            {
                export.Row(SpreadsheetExport.Text(row.Column1),
                           SpreadsheetExport.Text(row.Column2),
                           SpreadsheetExport.Text(row.Column5),
                           SpreadsheetExport.Text(row.Column6));
            }

            // The HTML totals line spans two columns under its label; the delimited record keeps the
            // same four-column alignment instead of collapsing into a shorter line.
            export.Row("الإجمالي", "",
                       SpreadsheetExport.Text(txtDeptDiff.Text),
                       SpreadsheetExport.Text(txtCreditDiff.Text));

            export.Save();
        }

        private void PrintDevexpress(int printMode)
        {
            try
            {
                RptUrl     = MainClass.ReportsPath;
                RptName    = "rptMezanyaArba7.repx";
                defPrinter = MainClass.ReportsPrinter;

                if (_rows.Count == 0)
                {
                    DXMessageBox.Show("لا توجد عمليات بالجدول", "", MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                if (string.IsNullOrWhiteSpace(RptUrl))
                {
                    DXMessageBox.Show("يجب تحديد مسار التقرير", "", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                string fullPath = Path.Combine(RptUrl, RptName);
                if (!Directory.Exists(RptUrl) || !File.Exists(fullPath))
                {
                    DXMessageBox.Show("المسار الحالي للتقارير غير موجود أو تم تعديله", "خطأ", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                FlowDocument document = BuildPrintDocument();

                if (printMode == 2)
                {
                    System.Windows.Window previewWindow = new System.Windows.Window
                    {
                        Title                 = "معاينة قبل الطباعة",
                        Width                 = 800,
                        Height                = 650,
                        WindowStartupLocation = WindowStartupLocation.CenterScreen,
                        FlowDirection         = System.Windows.FlowDirection.RightToLeft,
                        Background            = System.Windows.Media.Brushes.White
                    };
                    DocumentViewer viewer = new DocumentViewer { Document = document };
                    previewWindow.Content = viewer;
                    previewWindow.ShowDialog();
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
                FontSize      = 10,
                PagePadding   = new Thickness(20),
                ColumnWidth   = 800
            };

            doc.Blocks.Add(new Paragraph(new Run(Title))
            {
                FontSize = 16, FontWeight = FontWeights.Bold,
                TextAlignment = TextAlignment.Center,
                Foreground = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#213A7A"))
            });

            Table table = new Table { CellSpacing = 0 };
            for (int i = 0; i < 4; i++)
                table.Columns.Add(new TableColumn());

            TableRowGroup group = new TableRowGroup();
            table.RowGroups.Add(group);

            TableRow headerRow = new TableRow();
            group.Rows.Add(headerRow);

            AddHeaderCell(headerRow, "الحساب");
            AddHeaderCell(headerRow, "إسم الحساب");
            AddHeaderCell(headerRow, "رصيد مدين");
            AddHeaderCell(headerRow, "رصيد دائن");

            foreach (AccountBalanceRow row in _rows)
            {
                TableRow dataRow = new TableRow();
                group.Rows.Add(dataRow);
                AddBodyCell(dataRow, row.Column1);
                AddBodyCell(dataRow, row.Column2);
                AddBodyCell(dataRow, row.Column5);
                AddBodyCell(dataRow, row.Column6);
            }

            doc.Blocks.Add(table);

            Paragraph summary = new Paragraph { Margin = new Thickness(0, 10, 0, 0), FontWeight = FontWeights.Bold };
            summary.Inlines.Add(new Run($"إجمالي مدين: {txtDeptDiff.Text}   |   إجمالي دائن: {txtCreditDiff.Text}   |   {txtIsBalanced.Text}"));
            doc.Blocks.Add(summary);

            return doc;
        }

        private void AddHeaderCell(TableRow row, string text)
        {
            TableCell cell = new TableCell(new Paragraph(new Run(text)))
            {
                Background      = new SolidColorBrush((Color)ColorConverter.ConvertFromString("#DDE7FF")),
                BorderBrush     = System.Windows.Media.Brushes.Gray,
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
                BorderBrush     = System.Windows.Media.Brushes.Gray,
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
                RptName = dt.Rows[0]["RptName"]?.ToString() ?? "";
                RptUrl  = dt.Rows[0]["RptUrl"]?.ToString() ?? "";
            }
            catch { }
        }

        #endregion

        #region Close & Helpers

        private void btnClose_Click(object sender, RoutedEventArgs e) => Close();

        private void UpdateRowCount()
        {
            lblRowCount.Text = $"عدد السجلات: {_rows.Count:N0}";
        }

        private void ShowError(Exception ex)
        {
            DXMessageBox.Show("خطأ" + Environment.NewLine + ex.Message,
                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion
    }

    public class AccountBalanceRow
    {
        public string Column1 { get; set; }
        public string Column2 { get; set; }
        public string Column5 { get; set; }
        public string Column6 { get; set; }
    }
}