using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using DevExpress.Xpf.Core;
using DevExpress.XtraReports.UI;
using UtilitiesProj;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmRptSalesByCategory : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Nested Classes

        public class CategoryNode
        {
            public int    CategoryId   { get; set; }
            public string Code         { get; set; } = "";
            public string Name         { get; set; } = "";
            public double TotalQty     { get; set; }
            public double ItemTotal    { get; set; }
            public double ItemVat      { get; set; }
            public double ItemNet      { get; set; }
            public double InvDiscount  { get; set; }

            public ObservableCollection<ItemDetailNode> ItemDetails { get; set; }
                = new ObservableCollection<ItemDetailNode>();
        }

        public class ItemDetailNode
        {
            public int    ItemId       { get; set; }
            public int    CategoryId   { get; set; }
            public string ItemName     { get; set; } = "";
            public string ItemCode     { get; set; } = "";
            public double Qty          { get; set; }
            public double Total        { get; set; }
            public double ItemVat      { get; set; }
            public double ItemNet      { get; set; }
            public double InvDiscount  { get; set; }
        }

        #endregion

        #region Fields

        private SqlConnection conn;
        private ObservableCollection<CategoryNode> CategoryList;

        #endregion

        #region Constructor

        public frmRptSalesByCategory()
        {
            InitializeComponent();
            conn         = MainClass.ConnObj();
            CategoryList = new ObservableCollection<CategoryNode>();
            trvCategories.ItemsSource = CategoryList;
        }

        #endregion

        #region Window Loaded

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            txtStartDate.DateTime = DateTime.Today;
            txtEndDate.DateTime   = DateTime.Today;

            bool isAr = string.Equals(MainClass.Language, "ar",
                                       StringComparison.OrdinalIgnoreCase);

            cmbInvType.Items.Add(isAr ? "مبيعات"  : "Sales Inv");
            cmbInvType.Items.Add(isAr ? "نقطة بيع" : "POS");
            cmbInvType.SelectedIndex = 0;

            LoadGroup();
            LoadBranches();
            LoadSalesmen();
            LoadUsers();
        }

        #endregion

        #region Load Helpers

        private void LoadGroup()
        {
            var adapter = new SqlDataAdapter(
                "SELECT CategoryId, name FROM ItemsCategory WHERE IS_Deleted=0",
                conn);
            var dt = new DataTable();
            adapter.Fill(dt);

            cmbCategry.DisplayMemberPath = "name";
            cmbCategry.SelectedValuePath  = "CategoryId";
            cmbCategry.ItemsSource        = dt.DefaultView;
        }

        private void LoadBranches()
        {
            var adapter = new SqlDataAdapter(
                "SELECT BranchId, name FROM Branches WHERE IS_Deleted=0",
                conn);
            var dt = new DataTable();
            adapter.Fill(dt);

            cmbBranch.DisplayMemberPath = "name";
            cmbBranch.SelectedValuePath  = "BranchId";
            cmbBranch.ItemsSource        = dt.DefaultView;
        }

        private void LoadSalesmen()
        {
            var adapter = new SqlDataAdapter(
                "SELECT id, name FROM salesmen", conn);
            var dt = new DataTable();
            adapter.Fill(dt);

            cmbSalesman.DisplayMemberPath = "name";
            cmbSalesman.SelectedValuePath  = "id";
            cmbSalesman.ItemsSource        = dt.DefaultView;
        }

        private void LoadUsers()
        {
            var adapter = new SqlDataAdapter(
                "SELECT id, name FROM Employees WHERE IS_Deleted=0", conn);
            var dt = new DataTable();
            adapter.Fill(dt);

            cmbUser.DisplayMemberPath = "name";
            cmbUser.SelectedValuePath  = "id";
            cmbUser.ItemsSource        = dt.DefaultView;
        }

        #endregion

        #region Load Data (Main)

        // P7-046 fix: النتيجة bool — اكتمل النشر الذري أم لا (بوابة الطباعة P7-045)
        private bool LoadDgv()
        {
            try
            {
                // P7-046 fix: التجميع في قائمة محلية (Master-Detail) — لا نشر
                // تدريجي أثناء الاستعلامات
                var categories = new List<CategoryNode>();

                string condCat   = "";
                string condItems = "";

                // المجموعة
                // P7-068 fix: أول اختيار فعلي يدخل المرشح — الشرط القديم
                // «SelectedIndex > 0» كان يتخطى أول مجموعة/مستخدم/فرع
                // حقيقي (القوائم مربوطة بالبيانات بلا بند «الكل» placeholder)
                if (CheckBoxgroup.IsChecked != true &&
                    cmbCategry.SelectedIndex > -1 &&
                    cmbCategry.SelectedValue != null)
                {
                    condCat   = $" AND CategoryId={cmbCategry.SelectedValue}";
                    condItems = $" AND Items.group_id={cmbCategry.SelectedValue}";
                }

                // نوع الفاتورة
                string invTypeCond = cmbInvType.SelectedIndex == 0
                    ? "AND inv.inv_type=2"
                    : "AND inv.inv_type=3";

                string condWhere = invTypeCond;

                // المستخدم
                if (Che_user.IsChecked != true &&
                    cmbUser.SelectedIndex > -1 &&
                    cmbUser.SelectedValue != null)
                    // P7-076 fix: عمود مستخدم الفاتورة هو inv.sales_emp
                    // (عقد InsertInv: @sales_emp=MainClass.EmpNo وقائمة
                    // المستخدمين من Employees) — Safe_Emps عمود في جدول
                    // ربط الخزائن بالموظفين لا وجود له في عقد هذا
                    // الاستعلام (Items/inv_sub/inv) فيفشل الفلترة بالاستثناء
                    condWhere += $" AND inv.sales_emp={cmbUser.SelectedValue}";

                // الفترة
                if (Che_time.IsChecked != true)
                    condWhere += " AND date BETWEEN @date1 AND @date2";

                // الفرع
                if (chk_branch.IsChecked != true &&
                    cmbBranch.SelectedIndex > -1 &&
                    cmbBranch.SelectedValue != null)
                    condWhere += $" AND inv.branch={cmbBranch.SelectedValue}";

                // المندوب
                if (chkSalesman.IsChecked != true &&
                    cmbSalesman.SelectedValue != null)
                    condWhere += $" AND inv.salesman={cmbSalesman.SelectedValue}";

                condWhere += " AND inv_sub.ProductId=0";

                // جلب المجموعات
                var catAdapter = new SqlDataAdapter(
                    "SELECT CategoryId, Name, Code " +
                    $"FROM ItemsCategory WHERE IS_Deleted=0{condCat}", conn);
                var catDt = new DataTable();
                catAdapter.Fill(catDt);

                // جلب الأصناف
                // P7-069 fix: الضريبة والصافي من بيانات البنود (taxval)
                // لا من نسبة 15% ثابتة؛ P7-070 fix: وزن توزيع خصم الفاتورة
                // إجمالي السطر (qty×price) لا سعر الوحدة وحده
                string itemSql =
                    "SELECT ItemName, ItemCode, " +
                    "SUM(stockin - stockout) AS qty, " +
                    "SUM((ItemTotal1 - InvoiceDiscount1) " +
                    " - (ItemTotal2 - InvoiceDiscount2)) AS total, " +
                    "SUM(taxval1 - taxval2) AS itemvat, " +
                    "SUM((ItemTotal1 - InvoiceDiscount1) " +
                    " - (ItemTotal2 - InvoiceDiscount2)) " +
                    "+ SUM(taxval1 - taxval2) AS itemNet, " +
                    "SUM(InvoiceDiscount1 - InvoiceDiscount2) AS InvDiscount, " +
                    "ItemId, CategoryId " +
                    "FROM (" +
                    "SELECT SUM(ROUND(((val1 * ItemPriceWithoutVAT) * minus / " +
                    "NULLIF(InvSum,0)),2)) AS InvoiceDiscount1, " +
                    "0 AS InvoiceDiscount2, SUM(val) AS stockin, " +
                    "0 AS stockout, " +
                    "SUM(inv_sub.taxval) AS taxval1, 0 AS taxval2, " +
                    "SUM((val1 * ItemPriceWithoutVAT) - inv_sub.discount) AS ItemTotal1, " +
                    "0 AS ItemTotal2, Items.id AS ItemId, " +
                    "Items.group_id AS CategoryId, " +
                    "Items.code AS ItemCode, Items.name AS ItemName " +
                    "FROM Items JOIN inv_sub ON Items.Id=inv_sub.ItemId " +
                    "JOIN inv ON inv.InvGlobalID=inv_sub.InvGlobalID " +
                    $"WHERE Items.IS_Deleted=0 AND inv.proc_type=1 " +
                    $"AND inv.IS_Deleted=0 {condWhere}{condItems} " +
                    "GROUP BY Items.id, Items.name, Items.code, Items.group_id " +
                    "UNION ALL " +
                    "SELECT 0, SUM(ROUND(((val1 * ItemPriceWithoutVAT) * minus / " +
                    "NULLIF(InvSum,0)),2)), 0, SUM(val), " +
                    "0, SUM(inv_sub.taxval), " +
                    "SUM((val1 * ItemPriceWithoutVAT) - inv_sub.discount), " +
                    "Items.id, Items.group_id, Items.code, Items.name " +
                    "FROM Items JOIN inv_sub ON Items.Id=inv_sub.ItemId " +
                    "JOIN inv ON inv.InvGlobalID=inv_sub.InvGlobalID " +
                    $"WHERE Items.IS_Deleted=0 AND inv.proc_type=2 " +
                    $"AND inv.IS_Deleted=0 {condWhere}{condItems} " +
                    "GROUP BY Items.id, Items.name, Items.code, Items.group_id" +
                    ") AS dt " +
                    "GROUP BY ItemId, ItemName, ItemCode, CategoryId";

                var itemAdapter = new SqlDataAdapter(itemSql, conn);
                itemAdapter.SelectCommand.Parameters.Add(
                    "@date1", SqlDbType.DateTime).Value =
                    txtStartDate.DateTime.ToShortDateString();
                itemAdapter.SelectCommand.Parameters.Add(
                    "@date2", SqlDbType.DateTime).Value =
                    txtEndDate.DateTime.AddDays(1).ToShortDateString();

                var itemDt = new DataTable();
                itemAdapter.Fill(itemDt);

                // بناء هيكل Master-Detail
                foreach (DataRow catRow in catDt.Rows)
                {
                    int catId = Convert.ToInt32(catRow["CategoryId"]);

                    var node = new CategoryNode
                    {
                        CategoryId = catId,
                        Code = catRow["Code"]?.ToString() ?? "",
                        Name = catRow["Name"]?.ToString() ?? "",
                    };

                    // إضافة أصناف المجموعة
                    var items = itemDt.AsEnumerable()
                        .Where(r => Convert.ToInt32(r["CategoryId"]) == catId)
                        .ToList();

                    foreach (var itemRow in items)
                    {
                        double qty      = SafeDouble(itemRow["qty"]);
                        double total    = SafeDouble(itemRow["total"]);
                        double itemVat  = SafeDouble(itemRow["itemvat"]);
                        double itemNet  = SafeDouble(itemRow["itemNet"]);
                        double invDisc  = SafeDouble(itemRow["InvDiscount"]);

                        node.ItemDetails.Add(new ItemDetailNode
                        {
                            ItemId      = Convert.ToInt32(itemRow["ItemId"]),
                            CategoryId  = catId,
                            ItemName    = itemRow["ItemName"]?.ToString() ?? "",
                            ItemCode    = itemRow["ItemCode"]?.ToString() ?? "",
                            Qty         = Math.Round(qty, 2),
                            Total       = Math.Round(total, 2),
                            ItemVat     = Math.Round(itemVat, 2),
                            ItemNet     = Math.Round(itemNet, 2),
                            InvDiscount = Math.Round(invDisc, 2),
                        });
                    }

                    // حساب إجماليات المجموعة
                    node.TotalQty    = Math.Round(node.ItemDetails.Sum(x => x.Qty), 2);
                    node.ItemTotal   = Math.Round(node.ItemDetails.Sum(x => x.Total), 2);
                    node.ItemVat     = Math.Round(node.ItemDetails.Sum(x => x.ItemVat), 2);
                    node.ItemNet     = Math.Round(node.ItemDetails.Sum(x => x.ItemNet), 2);
                    node.InvDiscount = Math.Round(node.ItemDetails.Sum(x => x.InvDiscount), 2);

                    // فقط اضف المجموعات التي لها أصناف
                    if (node.ItemDetails.Count > 0)
                        categories.Add(node);
                }

                // ══ نقطة النشر الواحدة (P7-046) ══
                CategoryList.Clear();
                foreach (var c in categories) CategoryList.Add(c);

                // تحديث بطاقات الملخص
                lblTotQty.Text   = CategoryList.Sum(x => x.TotalQty).ToString("N2");
                lblTotTotal.Text = CategoryList.Sum(x => x.ItemTotal).ToString("N2");
                lblTotVat.Text   = CategoryList.Sum(x => x.ItemVat).ToString("N2");
                lblTotNet.Text   = CategoryList.Sum(x => x.ItemNet).ToString("N2");
                return true;
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ في تحميل البيانات:\n{ex.Message}",
                                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
                return false;
            }
        }

        private double SafeDouble(object val)
        {
            if (val == null || val == DBNull.Value) return 0.0;
            return double.TryParse(val.ToString(), out double r) ? r : 0.0;
        }

        #endregion

        #region CheckBox Events

        private void Che_user_CheckedChanged(object sender, RoutedEventArgs e)
        {
            // V-044 fix: الحدث ينطلق أثناء InitializeComponent (قيمة ابتدائية في XAML)
            // قبل إنشاء عناصر معرفة بعده — النداء المبكر كان يرمي NRE ويُفشل فتح النافذة
            if (cmbUser == null) return;
            if (!IsLoaded) return;
            cmbUser.IsEnabled = Che_user.IsChecked != true;
        }

        private void Che_time_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = Che_time.IsChecked == true;
            txtStartDate.IsEnabled = !isAll;
            txtEndDate.IsEnabled   = !isAll;
        }

        private void CheckBoxgroup_CheckedChanged(object sender, RoutedEventArgs e)
        {
            // V-044 fix: الحدث ينطلق أثناء InitializeComponent (قيمة ابتدائية في XAML)
            // قبل إنشاء عناصر معرفة بعده — النداء المبكر كان يرمي NRE ويُفشل فتح النافذة
            if (cmbCategry == null) return;
            if (!IsLoaded) return;
            cmbCategry.IsEnabled = CheckBoxgroup.IsChecked != true;
        }

        private void chk_branch_CheckedChanged(object sender, RoutedEventArgs e)
        {
            // V-044 fix: الحدث ينطلق أثناء InitializeComponent (قيمة ابتدائية في XAML)
            // قبل إنشاء عناصر معرفة بعده — النداء المبكر كان يرمي NRE ويُفشل فتح النافذة
            if (cmbBranch == null) return;
            if (!IsLoaded) return;
            cmbBranch.IsEnabled = chk_branch.IsChecked != true;
        }

        private void chkSalesman_CheckedChanged(object sender, RoutedEventArgs e)
        {
            // V-044 fix: الحدث ينطلق أثناء InitializeComponent (قيمة ابتدائية في XAML)
            // قبل إنشاء عناصر معرفة بعده — النداء المبكر كان يرمي NRE ويُفشل فتح النافذة
            if (cmbSalesman == null) return;
            if (!IsLoaded) return;
            cmbSalesman.IsEnabled = chkSalesman.IsChecked != true;
        }

        #endregion

        #region Button Events

        private void btnShow_Click(object sender, RoutedEventArgs e)
        {
            LoadDgv();
        }

        private void btnClose_Click(object sender, RoutedEventArgs e)
            => Close();

        private void btnPreview_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                PrintReport(2);
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void btnPrint_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                PrintReport(1);
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void btnExportExcel_Click(object sender, RoutedEventArgs e)
        {
            if (CategoryList == null || CategoryList.Count == 0)
            {
                DXMessageBox.Show("لا توجد بيانات للتصدير.", "تنبيه",
                                MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            try
            {
                string path = System.IO.Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
                    $"مبيعات_مجموعات_{DateTime.Now:yyyyMMdd_HHmm}.csv");

                // P7-048/049 fix: ترميز الخلايا الموحّد — الفاصلة والاقتباس
                // والأسطر وبادئات الصيغ وقيم الألوف كلها خلية واحدة سليمة
                DelimitedExport.WriteFile(path,
                    new[]
                    {
                        "اسم المجموعة", "رمز المجموعة", "اسم الصنف", "رمز الصنف",
                        "الكمية", "الإجمالي", "الضريبة", "الصافي", "الخصم"
                    },
                    CategoryList.SelectMany(cat => cat.ItemDetails.Select(item => new[]
                    {
                        cat.Name,
                        cat.Code,
                        item.ItemName,
                        item.ItemCode,
                        item.Qty.ToString("N2"),
                        item.Total.ToString("N2"),
                        item.ItemVat.ToString("N2"),
                        item.ItemNet.ToString("N2"),
                        item.InvDiscount.ToString("N2")
                    })));

                Process.Start(new ProcessStartInfo(path)
                { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ في التصدير:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region Print

        private void PrintReport(int printMode)
        {
            try
            {
                // P7-045 fix: إعادة الحساب بمعايير الواجهة الحالية قبل الربط —
                // النتيجة الفارغة يمسكها فحص القائمة الفارغة أدناه
                if (!LoadDgv()) return;

                if (CategoryList == null || CategoryList.Count == 0)
                {
                    DXMessageBox.Show("لا توجد بيانات للطباعة.", "تنبيه",
                                    MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                string rptUrl  = MainClass.ReportsPath;
                string printer = MainClass.ReportsPrinter;
                string rptName = "RptItemSalesByCategory.repx";

                string fullPath = System.IO.Path.Combine(rptUrl, rptName);

                if (string.IsNullOrEmpty(rptUrl) ||
                    !Directory.Exists(rptUrl)    ||
                    !File.Exists(fullPath))
                {
                    DXMessageBox.Show("مسار التقرير غير موجود.", "خطأ",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                var report = XtraReport.FromFile(fullPath);
                report.DataSource = BuildReportDataSet();

                if (string.IsNullOrEmpty(printer))
                {
                    DXMessageBox.Show("يجب تحديد الطابعة من الإعدادات.", "تنبيه",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                report.PrinterName = printer;

                if (printMode == 1)
                    report.Print();
                else
                    report.ShowPreviewDialog();

                report.Dispose();
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ في الطباعة:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public DataSet BuildReportDataSet()
        {
            // P7-071 fix: مصدر الطباعة ينقل البنود ومجاميعها لا رأساً
            // واحداً فقط — كان التقرير المطبوع يظهر الرأس وفراغاً تحته
            var list = new List<InventoryData>();

            string address = "", foundation = "", vatNo = "";
            if (Common.FoundationInfoDT.Rows.Count > 0)
            {
                address    = Common.FoundationInfoDT.Rows[0]["Address"]?.ToString() ?? "";
                foundation = Common.FoundationInfoDT.Rows[0]["nameA"]?.ToString() ?? "";
                vatNo      = Common.FoundationInfoDT.Rows[0]["tax_no"]?.ToString() ?? "";
            }

            foreach (var cat in CategoryList)
            {
                foreach (var item in cat.ItemDetails)
                {
                    list.Add(new InventoryData
                    {
                        ProcessType   = Title,
                        InventoryType = Title,
                        FromDate      = txtStartDate.DateTime.ToShortDateString(),
                        ToDate        = txtEndDate.DateTime.ToShortDateString(),
                        BranchName    = cmbBranch.Text,
                        User          = Common.GetEmpName(MainClass.EmpNo),
                        PrintDate     = DateTime.Now.ToShortDateString(),
                        Address       = address,
                        Foundation    = foundation,
                        VATNo         = vatNo,

                        CategoryName  = cat.Name,
                        CategoryCode  = cat.Code,
                        ItemName      = item.ItemName,
                        ItemCode      = item.ItemCode,
                        Quantity      = item.Qty.ToString("N2"),
                        Total         = item.Total.ToString("N2"),
                        Tax           = item.ItemVat.ToString("N2"),
                        Net           = item.ItemNet.ToString("N2"),
                        ItemDiscount  = item.InvDiscount.ToString("N2"),

                        // المجاميع الكلية من بطاقات الشاشة
                        SumQty        = lblTotQty.Text,
                        Sum           = lblTotTotal.Text,
                        SumTax        = lblTotVat.Text,
                        NetTotal      = lblTotNet.Text,
                    });
                }
            }

            var ds = new DataSet("Name");
            ds.Tables.Add(global::UtilitiesProj.Common.ToDataTable(list));
            return ds;
        }

        #endregion
    }
}