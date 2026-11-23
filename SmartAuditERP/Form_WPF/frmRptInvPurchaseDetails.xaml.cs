using AuditorAPI.Models;
using AuditorAPI.Models.DGVmodels;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmRptInvPurchaseDetails
        : DevExpress.Xpf.Core.ThemedWindow
    {
        #region ══════════════════ Fields ══════════════════

        private SqlConnection conn;

        public int Invtype = 1;
        private int Proc_Type = 1;
        private bool PrintHeader = true;
        private bool PrintFooter = true;
        private bool PrintStamp = true;
        private int PrintType = 1;
        private int PrintNo = 1;
        private string defPrinter = "";
        private string RptName = "";
        private string RptUrl = "";
        private bool IsVAT = true;
        private bool isProcessRunning = false;
        private double defVAT = 0.0;
        private bool PricIncVAT = false;
        private int DgvFontSize = 1;

        private double nTotal = 0, nTotal1 = 0;
        private double nVAT = 0, nVAT1 = 0;
        private double nNet = 0, nNet1 = 0;
        private double sum = 0, sum1 = 0;
        private double Discount = 0, Discount1 = 0;

        private double InvSum = 0.0;
        private double InvDiscount = 0.0;
        private double InvVAT = 0.0;
        private double InvAvrgCost = 0.0;

        private string StyleFile = "";
        private string StyleFolder = "";

        private InvoiceObj InvObj;
        private List<InvoiceTxt> InvoicesList;

        private readonly ObservableCollection<InvoiceTxt> _invoiceRows
            = new ObservableCollection<InvoiceTxt>();

        // ✅ Cache لـ InvoiceObj لتجنب إنشائه مرات عديدة
        private readonly Dictionary<string, InvoiceObj> _invoiceObjCache
            = new Dictionary<string, InvoiceObj>();

        // P7-047 fix: قيم مالية إضافية لكل فاتورة لا يحملها نموذج InvoiceTxt الخارجي
        // (AuditorAPI.dll) — ضريبة إضافية بمبلغها ونقدي/شبكة الفعليين من Inv
        private readonly Dictionary<string, InvFinancialExtras> _invExtras
            = new Dictionary<string, InvFinancialExtras>();

        #endregion

        #region ══════════════════ Inner Model ══════════════════

        /// <summary>
        /// P7-047: مبلغ الضريبة الإضافية وتوزيع الدفع نقدي/شبكة لفاتورة واحدة —
        /// من Inv مباشرة (Inv_Sub.ItemAdditionalTax وInv.cash وInv.visa).
        /// </summary>
        private class InvFinancialExtras
        {
            public double ExtraVATAmt { get; set; }
            public double PayCash { get; set; }
            public double PayAtm { get; set; }
        }

        /// <summary>
        /// يحمل كل قيم UI اللازمة للاستعلام.
        /// يُملأ على UI Thread ثم يُمرَّر للـ Background Thread.
        /// </summary>
        private class QueryParams
        {
            public string WhereClause { get; set; }
            public DateTime DateFrom { get; set; }
            public DateTime DateTo { get; set; }
            public bool UseDateFilter { get; set; }
        }

        #endregion

        #region ══════════════════ Constructor ══════════════════

        public frmRptInvPurchaseDetails()
        {
            InitializeComponent();

            conn = MainClass.ConnObj();

            Invtype = 1;
            Proc_Type = 1;
            PrintHeader = true;
            PrintFooter = true;
            PrintStamp = true;
            PrintNo = 1;
            RptName = "";
            RptUrl = "";
            InvSum = 0.0;
            InvDiscount = 0.0;
            InvVAT = 0.0;
            InvAvrgCost = 0.0;
            IsVAT = true;
            isProcessRunning = false;
            DgvFontSize = 1;

            InvObj = new InvoiceObj(1, 1);

            StyleFile = Path.Combine(MainClass.ReportsPath,
                @"Styles\RptInvPurchDetailsLayout.xml");
            StyleFolder = Path.Combine(MainClass.ReportsPath, "Styles");

            nTotal = nTotal1 = nVAT = nVAT1 =
            nNet = nNet1 = sum = sum1 =
            Discount = Discount1 = 0.0;
        }

        #endregion

        #region ══════════════════ Window Load ══════════════════

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                GridControl2.ItemsSource = _invoiceRows;

                txtFromDate.EditValue = DateTime.Today;
                txtToDate.EditValue = DateTime.Today;
                txtStartTime.Text = "00:00";
                txtEndTime.Text = "23:59";

                bool isAr = string.Equals(
                    MainClass.Language, "ar",
                    StringComparison.OrdinalIgnoreCase);

                if (isAr)
                {
                    cmbType.Items.Add("نقدية");
                    cmbType.Items.Add("آجلة");
                    cmbType.Items.Add("شبكة");
                    cmbType.Items.Add("بنك");
                }
                else
                {
                    cmbType.Items.Add("Cash");
                    cmbType.Items.Add("Postpone");
                    cmbType.Items.Add("ATM");
                    cmbType.Items.Add("Bank");
                }

                LoadEmps();
                LoadSalesMen();
                LoadCustomers();
                LoadprintSetting();
                LoadBranches();
                BranchPermissionsi();
                LoadStores();
                LoadDGvSetting();
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ في التحميل: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region ══════════════════ Load Methods ══════════════════

        private void LoadDGvSetting()
        {
            try
            {
                if (File.Exists(StyleFile))
                {
                    // يمكن تحميل عرض الأعمدة من XML لاحقاً
                }
            }
            catch { }
        }

        private void LoadBranches()
        {
            try
            {
                string whereClause = "";
                if (MainClass.BranchNo != -1 &&
                    !string.Equals(Accounting.BranchCondition, " ",
                        StringComparison.Ordinal))
                    whereClause = " and id=" + MainClass.BranchNo;

                var da = new SqlDataAdapter(
                    "select id,name from Branches " +
                    "where IS_Deleted=0" + whereClause, conn);
                var dt = new DataTable();
                da.Fill(dt);

                cmbBranches.ItemsSource = dt.DefaultView;
                cmbBranches.DisplayMemberPath = "name";
                cmbBranches.SelectedValuePath = "id";
                cmbBranches.SelectedIndex = -1;
            }
            catch { }
        }

        private void BranchPermissionsi()
        {
            if (!string.Equals(Accounting.BranchCondition, " ",
                StringComparison.Ordinal))
            {
                chkAllBranches.IsChecked = false;
                chkAllBranches.Visibility = Visibility.Collapsed;
                cmbBranches.IsEnabled = true;
                if (cmbBranches.Items.Count > 0)
                    cmbBranches.SelectedIndex = 0;
            }
        }

        private void LoadEmps()
        {
            try
            {
                var da = new SqlDataAdapter(
                    "select id,name from Employees " +
                    "where IS_Deleted=0 order by id", conn);
                var dt = new DataTable();
                da.Fill(dt);

                cmbusers.ItemsSource = dt.DefaultView;
                cmbusers.DisplayMemberPath = "name";
                cmbusers.SelectedValuePath = "id";
                cmbusers.SelectedIndex = -1;
            }
            catch { }
        }

        private void LoadCustomers()
        {
            try
            {
                var da = new SqlDataAdapter(
                    "select id,name from Customers " +
                    "where (type=2 or type=3) order by id", conn);
                var dt = new DataTable();
                da.Fill(dt);

                cmbClients.ItemsSource = dt.DefaultView;
                cmbClients.DisplayMemberPath = "name";
                cmbClients.SelectedValuePath = "id";
                cmbClients.SelectedIndex = -1;
            }
            catch { }
        }

        public void LoadSalesMen()
        {
            try
            {
                var da = new SqlDataAdapter(
                    "select id,name from salesmen " +
                    "where IS_Deleted=0 order by id", conn);
                var dt = new DataTable();
                da.Fill(dt);

                cmbSaleman.ItemsSource = dt.DefaultView;
                cmbSaleman.DisplayMemberPath = "name";
                cmbSaleman.SelectedValuePath = "id";
                cmbSaleman.SelectedIndex = -1;
            }
            catch { }
        }

        private void LoadStores()
        {
            try
            {
                var dt = LoadData.Invertories(MainClass.EmpNo);
                cmbStore.ItemsSource = dt.DefaultView;
                cmbStore.DisplayMemberPath = "name";
                cmbStore.SelectedValuePath = "id";
                cmbStore.SelectedIndex = -1;
            }
            catch { }
        }

        private void LoadprintSetting()
        {
            try
            {
                var da = new SqlDataAdapter(
                    "select * from SettingPrint where Inv_Id=12", conn);
                var dt = new DataTable();
                da.Fill(dt);

                if (dt.Rows.Count == 1)
                {
                    try
                    {
                        PrintType = Convert.ToInt32(dt.Rows[0]["printType"]);
                        PrintFooter = Convert.ToBoolean(dt.Rows[0]["PrintFooter"]);
                        PrintHeader = Convert.ToBoolean(dt.Rows[0]["PrintHeader"]);
                        PrintStamp = Convert.ToBoolean(dt.Rows[0]["PrintStamp"]);
                        defPrinter = dt.Rows[0]["CasherPrinter"].ToString();
                        if (string.IsNullOrEmpty(defPrinter))
                            defPrinter = Common.GetDefaultPrinter();
                        PrintNo = Convert.ToInt32(dt.Rows[0]["printNo"]);
                    }
                    catch { }
                }

                var da2 = new SqlDataAdapter(
                    "select * from SettingGeneral where Inv_Id=1", conn);
                var dt2 = new DataTable();
                da2.Fill(dt2);

                if (dt2.Rows.Count == 1)
                {
                    try
                    {
                        PricIncVAT = Convert.ToBoolean(dt2.Rows[0]["PriceIncVAT"]);
                        defVAT = Convert.ToDouble(dt2.Rows[0]["MainVAT"]);
                    }
                    catch { }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region ══════════════════ Collect UI Params ══════════════════

        /// <summary>
        /// يجمع كل قيم UI على UI Thread بأمان
        /// ثم يُمرِّرها للـ Background Thread
        /// </summary>
        private QueryParams CollectQueryParams()
        {
            string whereClause = $"inv.Inv_type={Invtype} and ";

            // فلتر الفرع
            // P7-088 fix: «كل الفروع» يُلغي قيد الفرع — كان الاختيار
            // السابق يبقى مقيداً للاستعلام حتى مع تفعيل الخيار
            if (chkAllBranches.IsChecked != true &&
                cmbBranches.SelectedIndex > -1)
                whereClause +=
                    $"inv.branch={cmbBranches.SelectedValue} and ";

            // فلتر العميل
            if (ckAllClients.IsChecked != true &&
                cmbClients.SelectedIndex > -1)
                whereClause +=
                    $"cust_id={cmbClients.SelectedValue} and ";

            // فلتر المستخدم
            if (ckAllUsers.IsChecked != true &&
                cmbusers.SelectedIndex > -1)
                whereClause +=
                    $"sales_emp={cmbusers.SelectedValue} and ";

            // فلتر المندوب
            if (cbAllSalesmen.IsChecked != true &&
                cmbSaleman.SelectedIndex > -1)
                whereClause +=
                    $"salesman={cmbSaleman.SelectedValue} and ";

            // فلتر المستودع
            if (ckAllStore.IsChecked != true &&
                cmbStore.SelectedIndex > -1)
                whereClause +=
                    $"inv.safe={cmbStore.SelectedValue} and ";

            // نوع العملية
            if (rbAllSales.IsChecked == true)
                whereClause += "(inv.proc_type=1 or inv.proc_type=2) and ";
            else if (rbSales.IsChecked == true)
                whereClause += "inv.proc_type=1 and ";
            else
                whereClause += "inv.proc_type=2 and ";

            // الضريبة
            if (rbWithVat.IsChecked == true)
                whereClause += "FreeVATSales=0 and ";
            else if (rbNoVAT.IsChecked == true)
                whereClause += "FreeVATSales>0 and ";

            // نوع الدفع
            if (ckAllType.IsChecked != true)
            {
                int selIdx = cmbType.SelectedIndex;
                if (selIdx == 1) whereClause += "inv.pay_type=-1 and ";
                else if (selIdx == 0) whereClause += "inv.pay_type=1 and ";
                else if (selIdx == 2) whereClause += "inv.pay_type=2 and bank<=1 and ";
                else if (selIdx == 3) whereClause += "inv.pay_type=2 and bank>1 and ";
            }

            // التواريخ
            DateTime fromDate = txtFromDate.EditValue is DateTime fd
                ? fd : DateTime.Today;
            DateTime toDate = txtToDate.EditValue is DateTime td
                ? td : DateTime.Today;

            if (!TimeSpan.TryParse(txtStartTime.Text, out TimeSpan fromTime))
                fromTime = TimeSpan.Zero;
            if (!TimeSpan.TryParse(txtEndTime.Text, out TimeSpan toTime))
                toTime = new TimeSpan(23, 59, 0);

            DateTime dateFrom = fromDate.Date + fromTime;
            DateTime dateTo = toDate.Date + toTime;

            bool useDateFilter = ckTotalPeriod.IsChecked != true;
            if (useDateFilter)
                whereClause += "date between @date1 and @date2 and ";

            return new QueryParams
            {
                WhereClause = whereClause,
                DateFrom = dateFrom,
                DateTo = dateTo,
                UseDateFilter = useDateFilter
            };
        }

        #endregion

        #region ══════════════════ Show Invoices (Async) ══════════════════

        private void btnView_Click(object sender, RoutedEventArgs e)
        {
            // ✅ منع التكرار
            if (isProcessRunning)
            {
                MessageBox.Show("العملية قيد التنفيذ، انتظر...", "",
                    MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            // ✅ جمع قيم UI على UI Thread
            QueryParams queryParams = null;
            Dispatcher.Invoke(() =>
            {
                queryParams = CollectQueryParams();
            });

            if (queryParams == null) return;

            // ✅ تعطيل الزر أثناء التنفيذ
            btnView.IsEnabled = false;
            isProcessRunning = true;

            // ✅ تصفير البيانات على UI Thread
            GridControl2.ItemsSource = null;
            _invoiceRows.Clear();
            InvoicesList?.Clear();

            // ✅ تشغيل الاستعلام على Background Thread
            Task.Run(() =>
            {
                try
                {
                    var result = BindingListOfInvoices1Async(queryParams);

                    Dispatcher.Invoke(() =>
                    {
                        _invoiceRows.Clear();
                        foreach (var item in result)
                            _invoiceRows.Add(item);

                        GridControl2.ItemsSource = _invoiceRows;
                        CalculateSummary();
                    });
                }
                catch (Exception ex)
                {
                    Dispatcher.Invoke(() =>
                        MessageBox.Show("خطأ في العرض: " + ex.Message, "",
                            MessageBoxButton.OK, MessageBoxImage.Error));
                }
                finally
                {
                    Dispatcher.Invoke(() =>
                    {
                        btnView.IsEnabled = true;
                        isProcessRunning = false;
                    });
                }
            });
        }

        /// <summary>
        /// للتوافق مع الاستدعاءات القديمة من أماكن أخرى
        /// </summary>
        private void ShowInvoice()
        {
            btnView_Click(null, null);
        }

        #endregion

        #region ══════════════════ BindingListOfInvoices1 (Optimized) ══════════════════

        /// <summary>
        /// ✅ النسخة الأصلية - للتوافق مع الاستدعاءات الخارجية
        /// تعمل على UI Thread مع Timeout = 120 ثانية
        /// </summary>
        public List<InvoiceTxt> BindingListOfInvoices1(
            string sqlstr, bool withItems,
            DateTime Date1, DateTime date2)
        {
            var p = new QueryParams
            {
                WhereClause = "",   // غير مستخدم هنا
                DateFrom = Date1,
                DateTo = date2,
                UseDateFilter = true
            };

            // ✅ استدعاء النسخة المحسّنة
            return BindingListOfInvoices1Async(p, sqlstr, withItems);
        }

        /// <summary>
        /// ✅ النسخة المحسّنة - تعمل على Background Thread
        /// - Timeout = 120 ثانية
        /// - اتصال منفصل آمن
        /// - LEFT JOIN Stocks بدل GetStoreName (N+1)
        /// - Cache لـ InvoiceObj
        /// </summary>
        private List<InvoiceTxt> BindingListOfInvoices1Async(
            QueryParams p,
            string overrideSql = null,
            bool withItems = false)
        {
            var list = new List<InvoiceTxt>();

            // P7-047 fix: تُبنى القيم المالية الإضافية مع نفس التحميل — لا تبقى
            // من تحميل سابق فوق بيانات جديدة
            _invExtras.Clear();

            // ✅ بناء الاستعلام المحسّن مع LEFT JOIN للمستودع
            string sql = overrideSql ?? BuildOptimizedSql(p);

            using (var bgConn = MainClass.ConnObj())
            {
                bgConn.Open();

                using (var cmd = new SqlCommand(sql, bgConn))
                {
                    // ✅ Timeout = 120 ثانية بدل الافتراضي 30
                    cmd.CommandTimeout = 120;

                    // ✅ إضافة بارامترات التاريخ فقط إذا لزم
                    if (p.UseDateFilter)
                    {
                        cmd.Parameters.Add(
                            "@date1", SqlDbType.DateTime).Value = p.DateFrom;
                        cmd.Parameters.Add(
                            "@date2", SqlDbType.DateTime).Value = p.DateTo;
                    }

                    var dt = new DataTable();
                    using (var adapter = new SqlDataAdapter(cmd))
                        adapter.Fill(dt);

                    int rowCount = dt.Rows.Count;

                    // ✅ تهيئة ProgressBar على UI Thread
                    Dispatcher.Invoke(() =>
                    {
                        ProgressBar1.Value = 0;
                        ProgressBar1.Maximum = rowCount > 0 ? rowCount : 1;
                    });

                    bool isAr = string.Equals(
                        MainClass.Language, "ar",
                        StringComparison.OrdinalIgnoreCase);

                    for (int i = 0; i < rowCount; i++)
                    {
                        try
                        {
                            DataRow row = dt.Rows[i];

                            int invTypeInt = Convert.ToInt32(row["inv_type"]);
                            int procTypeInt = Convert.ToInt32(row["proc_type"]);

                            double.TryParse(
                                ("" + row["pay_type"]), out double payTypeVal);
                            int payTypeInt = (int)payTypeVal;

                            // نص طريقة الدفع
                            string payText =
                                payTypeVal == -1 ? (isAr ? "آجل" : "Credit") :
                                payTypeVal == 1 ? (isAr ? "نقدي" : "Cash") :
                                payTypeVal == 2 ? (isAr ? "شبكة" : "Card") :
                                payTypeVal == 4 ? (isAr ? "متعدد" : "Multi") :
                                "";

                            string invoiceType = InvoiceOper.GetInvoiceType(
                                invTypeInt, procTypeInt, payTypeInt, 1);

                            // ✅ Cache لـ InvoiceObj
                            var invoiceObj = GetOrCreateInvoiceObj(
                                invTypeInt, procTypeInt);

                            // ✅ اسم المستودع من الاستعلام مباشرةً (بدل N+1)
                            string storeName = overrideSql != null
                                ? Common.GetStoreName(
                                    Convert.ToInt32("" + row["safe"]))
                                : ("" + row["StoreName"]);

                            var invoiceTxt = new InvoiceTxt
                            {
                                ISNew = false,
                                IsPrinted = true,
                                IsLoaded = false,
                                InvGlobalID = "" + row["InvGlobalID"],
                                EntryGlobalID = $"{row["branch"]}-{row["EntryID"]}",
                                ProcType = procTypeInt,
                                AutoIncrementID = i + 1,
                                InvoiceNo = (int)Convert.ToDouble("" + row["id"]),
                                InvoiceType = (InvoiceType)invTypeInt,
                                InvoiceTypeTxt = invoiceType,
                                AdditionalCost = Convert.ToDecimal(row["AdditionalCost"]),
                                InvoiceStatus = Convert.ToInt32(row["InvoiceStatus"]),
                                Treasury = Convert.ToInt32("" + row["stock"]),
                                Store = Convert.ToInt32("" + row["safe"]),
                                InvDiscount = Convert.ToDouble("" + row["minus"]),
                                VAT = Convert.ToDouble(row["tax"]),
                                Paid = Convert.ToDouble("" + row["paid"]),
                                Remainder = Convert.ToDouble(row["paid"]) -
                                                 Convert.ToDouble(row["tot_net"]),
                                InvNote = "" + row["notes"],
                                VATperc = invoiceObj.VAT,
                                ExtraVATPerc = invoiceObj.AdditionalTax,
                                PriceIncVAT = invoiceObj.PriceIncVAT,
                                BranchTxt = "" + row["BranchName"],
                                ReffNo = "" + row["Reff_No"],
                                PayType = payTypeInt,
                                PaymentTxt = payText,
                                Bank = Convert.ToInt32(row["bank"]),
                                Customer = Convert.ToInt32(row["cust_id"]),
                                ClientTxt = row["CustName"] == DBNull.Value
                                                    ? "" : row["CustName"].ToString(),
                                Saleman = Convert.ToInt32("" + row["salesman"]),
                                SalesmanTxt = "" + row["salesman"],
                                User = Convert.ToInt32("" + row["sales_emp"]),
                                UserTxt = row["username"] == DBNull.Value
                                                    ? "" : row["username"].ToString(),
                                InvertoryName = storeName,
                                FreeVATSales = Convert.ToDouble(row["FreeVATSales"]),
                                Total = Convert.ToDouble(row["InvTotal"]),
                                Net = Convert.ToDouble(row["tot_net"])
                            };

                            invoiceTxt.TotDiscount = invoiceTxt.InvDiscount;

                            // P7-047 fix: التقاط القيم المالية الإضافية مع الصف
                            // (مبلغ الضريبة الإضافية من البنود + نقدي/شبكة من Inv)
                            _invExtras[invoiceTxt.InvGlobalID] =
                                new InvFinancialExtras
                                {
                                    ExtraVATAmt = SafeRowDouble(row, "ExtraVATAmt"),
                                    PayCash = SafeRowDouble(row, "cash"),
                                    PayAtm = SafeRowDouble(row, "visa")
                                };

                            // التواريخ
                            if (DateTime.TryParse(
                                    row["date"].ToString(), out DateTime invDate))
                            {
                                invoiceTxt.InvDate = invDate;
                                invoiceTxt.InvTime = invDate;
                                invoiceTxt.InvoiceTime =
                                    invDate.ToString("hh:mm:ss tt");
                            }

                            try
                            {
                                if (DateTime.TryParse(
                                        row["Reff_date"].ToString(),
                                        out DateTime refDate))
                                    invoiceTxt.RefDate = refDate;
                            }
                            catch { }

                            if (!withItems)
                            {
                                invoiceTxt.TotDiscount +=
                                    Convert.ToDouble(row["ItemDiscount"]);
                                invoiceTxt.SumPrice =
                                    Convert.ToDouble(row["sumPrice"]);
                            }

                            list.Add(invoiceTxt);

                            // ✅ تحديث ProgressBar كل 10 صفوف لتقليل overhead
                            if (i % 10 == 0 || i == rowCount - 1)
                            {
                                int progress = i + 1;
                                Dispatcher.Invoke(() =>
                                    ProgressBar1.Value = progress);
                            }
                        }
                        catch { }
                    }
                }
            }

            return list;
        }

        /// <summary>
        /// ✅ بناء الاستعلام المحسّن مع LEFT JOIN للمستودع
        /// بدل استدعاء GetStoreName لكل صف (N+1)
        /// </summary>
        private string BuildOptimizedSql(QueryParams p)
        {
            return
                "select Inv.*," +
                "(SELECT ISNULL(sum(Inv_Sub.val1*Inv_Sub.exchange_price),0) " +
                " from Inv_Sub where InvGlobalID=Inv.InvGlobalID) as sumPrice," +
                "(SELECT ISNULL(sum(discount),0) " +
                " from Inv_Sub where InvGlobalID=Inv.InvGlobalID) as ItemDiscount," +
                // P7-047 fix: مبلغ الضريبة الإضافية من بنود الفاتورة — كان
                // الإسقاط يطبع النسبة مكان المبلغ
                "(SELECT ISNULL(sum(Inv_Sub.ItemAdditionalTax),0) " +
                " from Inv_Sub where InvGlobalID=Inv.InvGlobalID) as ExtraVATAmt," +
                "Customers.name   as CustName," +
                "Users.username   as username," +
                "Branches.name    as BranchName," +
                // P7-087 fix: اسم المستودع من جدوله الصحيح (Safes) —
                // نطاق inv.safe هو معرفات Safes (قائمة المستودعات
                // LoadData.Invertories تقرأ Safes وGetStoreName يقرأ
                // Safes.name) — الربط بـ Stocks كان يجلب اسم خزينة
                // أخرى بمعرف المستودع
                "Safes.name       as StoreName " +   // ✅ بدل GetStoreName
                "from Inv " +
                "left join Customers on inv.cust_id   = Customers.id " +
                "left join Users     on inv.sales_emp = Users.emp " +
                "left join Branches  on inv.branch    = Branches.id " +
                "left join Safes     on inv.safe       = Safes.id " + // ✅ JOIN
                "where " + p.WhereClause +
                " Inv.IS_Deleted=0 order by date desc";
        }

        /// <summary>
        /// ✅ Cache لـ InvoiceObj لتجنب إنشائه مرات عديدة لنفس النوع
        /// </summary>
        private InvoiceObj GetOrCreateInvoiceObj(int invType, int procType)
        {
            string key = $"{invType}_{procType}";
            if (!_invoiceObjCache.TryGetValue(key, out InvoiceObj obj))
            {
                obj = new InvoiceObj(invType, procType);
                _invoiceObjCache[key] = obj;
            }
            return obj;
        }

        /// <summary>
        /// P7-047: قراءة رقم من صف الجدول بلا رمي — أعمدة cash/visa/ExtraVATAmt
        /// قد تكون NULL في قواعد قديمة.
        /// </summary>
        private static double SafeRowDouble(DataRow row, string column)
        {
            if (!row.Table.Columns.Contains(column)) return 0.0;
            object v = row[column];
            if (v == null || v == DBNull.Value) return 0.0;
            return double.TryParse(v.ToString(), out double d) ? d : 0.0;
        }

        #endregion

        #region ══════════════════ Summary ══════════════════

        private void CalculateSummary()
        {
            sum = sum1 = Discount = Discount1 =
            nTotal = nTotal1 = nVAT = nVAT1 =
            nNet = nNet1 = 0;

            foreach (var row in _invoiceRows)
            {
                if (row.ProcType == 1)
                {
                    sum += row.SumPrice;
                    Discount += row.TotDiscount;
                    nTotal += row.Total;
                    nVAT += row.VAT;
                    nNet += row.Net;
                }
                else
                {
                    sum1 += row.SumPrice;
                    Discount1 += row.TotDiscount;
                    nTotal1 += row.Total;
                    nVAT1 += row.VAT;
                    nNet1 += row.Net;
                }
            }

            string fmt = Common.DigitsNo ?? "N2";
            lblSumTotal.Text = (sum - sum1).ToString(fmt);
            lblSumDiscount.Text = (Discount - Discount1).ToString(fmt);
            lblSumNet.Text = (nTotal - nTotal1).ToString(fmt);
            lblSumVAT.Text = (nVAT - nVAT1).ToString(fmt);
            lblSumNetFinal.Text = (nNet - nNet1).ToString(fmt);
        }

        #endregion

        #region ══════════════════ Print / Export ══════════════════

        private void PrintDevexpress(int type)
        {
            try
            {
                RptUrl = MainClass.ReportsPath;
                defPrinter = MainClass.ReportsPrinter;
                RptName = "rptInvSumBySupplier.repx";

                if (_invoiceRows.Count == 0)
                {
                    MessageBox.Show("لا توجد عمليات بالجدول", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                var fromDate = txtFromDate.EditValue is DateTime fd
                    ? fd : DateTime.Today;
                var toDate = txtToDate.EditValue is DateTime td
                    ? td : DateTime.Today;

                // P7-047 fix: مجاميع الحقول المالية التي كان الإسقاط يصفرها
                double xExtra = 0, xExtra1 = 0;
                double xTotalTax = 0, xTotalTax1 = 0;
                double xPaid = 0, xPaid1 = 0;
                double xRemainder = 0, xRemainder1 = 0;
                foreach (var row in _invoiceRows)
                {
                    var ex = _invExtras.TryGetValue(row.InvGlobalID, out var e)
                        ? e : null;
                    double extraAmt = ex?.ExtraVATAmt ?? 0.0;
                    double totalTax = row.VAT + extraAmt;

                    if (row.ProcType == 1)
                    {
                        xExtra += extraAmt;
                        xTotalTax += totalTax;
                        xPaid += row.Paid;
                        xRemainder += row.Remainder;
                    }
                    else
                    {
                        xExtra1 += extraAmt;
                        xTotalTax1 += totalTax;
                        xPaid1 += row.Paid;
                        xRemainder1 += row.Remainder;
                    }
                }

                string fmt = Common.DigitsNo ?? "N2";
                var report = new Report();
                var ds = report.BindToData(
                    BuildDataTableForReport(),
                    cmbType.Text,
                    fromDate.ToString("d"),
                    toDate.ToString("d"),
                    sumTotal: lblSumTotal.Text,
                    sumDiscount: lblSumDiscount.Text,
                    sumNet: lblSumNet.Text,
                    sumVAT: lblSumVAT.Text,
                    sumNetFinal: lblSumNetFinal.Text,
                    sumExtraTax: (xExtra - xExtra1).ToString(fmt),
                    sumTotalTax: (xTotalTax - xTotalTax1).ToString(fmt),
                    sumPaid: (xPaid - xPaid1).ToString(fmt),
                    sumRemainder: (xRemainder - xRemainder1).ToString(fmt));

                report.Printing(type, ds, RptUrl, RptName, defPrinter, 1);
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ في الطباعة: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private DataTable BuildDataTableForReport()
        {
            var dt = new DataTable("Invoices");
            dt.Columns.Add("AutoIncrementID", typeof(int));
            dt.Columns.Add("InvoiceTypeTxt", typeof(string));
            dt.Columns.Add("InvGlobalID", typeof(string));
            dt.Columns.Add("InvoiceNo", typeof(string));
            dt.Columns.Add("ReffNo", typeof(string));
            dt.Columns.Add("InvDate", typeof(string));
            dt.Columns.Add("InvoiceTime", typeof(string));
            dt.Columns.Add("PaymentTxt", typeof(string));
            dt.Columns.Add("ClientTxt", typeof(string));
            dt.Columns.Add("SumPrice", typeof(string));
            dt.Columns.Add("TotDiscount", typeof(string));
            dt.Columns.Add("Total", typeof(string));
            dt.Columns.Add("VAT", typeof(string));
            dt.Columns.Add("Net", typeof(string));
            dt.Columns.Add("InvertoryName", typeof(string));
            dt.Columns.Add("BranchTxt", typeof(string));
            dt.Columns.Add("UserTxt", typeof(string));
            dt.Columns.Add("ProcType", typeof(int));
            dt.Columns.Add("Paid", typeof(string));
            dt.Columns.Add("Remainder", typeof(string));
            dt.Columns.Add("ExtraVAT", typeof(string));
            dt.Columns.Add("TotalTax", typeof(string));
            dt.Columns.Add("Paycash", typeof(string));
            dt.Columns.Add("PayATM", typeof(string));

            string fmt = Common.DigitsNo ?? "N2";

            foreach (var row in _invoiceRows)
            {
                // P7-047 fix: المبالغ لا النسب ولا الأصفار — مبلغ الضريبة الإضافية
                // من بنود الفاتورة، وإجمالي الضريبة = ضريبة الفاتورة + الإضافية،
                // ونقدي/شبكة مما دُفع فعلاً في الفاتورة (Inv.cash / Inv.visa)
                var ex = _invExtras.TryGetValue(row.InvGlobalID, out var extras)
                    ? extras : null;
                double extraVatAmt = ex?.ExtraVATAmt ?? 0.0;
                double totalTax = row.VAT + extraVatAmt;
                double payCash = ex?.PayCash ?? 0.0;
                double payAtm = ex?.PayAtm ?? 0.0;

                dt.Rows.Add(
                    row.AutoIncrementID,
                    row.InvoiceTypeTxt,
                    row.InvGlobalID,
                    row.InvoiceNo.ToString(),
                    row.ReffNo,
                    row.InvDate.ToString("MM/d/yyyy hh:mm tt"),
                    row.InvoiceTime,
                    row.PaymentTxt,
                    row.ClientTxt,
                    row.SumPrice.ToString(fmt),
                    row.TotDiscount.ToString(fmt),
                    row.Total.ToString(fmt),
                    row.VAT.ToString(fmt),
                    row.Net.ToString(fmt),
                    row.InvertoryName,
                    row.BranchTxt,
                    row.UserTxt,
                    row.ProcType,
                    row.Paid.ToString(fmt),
                    row.Remainder.ToString(fmt),
                    extraVatAmt.ToString(fmt),
                    totalTax.ToString(fmt),
                    payCash.ToString(fmt),
                    payAtm.ToString(fmt));
            }
            return dt;
        }

        private void btnExportExcel_Click(object sender, RoutedEventArgs e)
        {
            if (_invoiceRows.Count == 0) return;
            try
            {
                // P7-050 fix: الامتداد المعروض هو المكتوب فعلاً — xlsx ملف
                // Excel حقيقي (ClosedXML)، وcsv/tsv نص مفصول بترميز الخلايا
                // الموحّد (P7-048/049)
                var dlg = new Microsoft.Win32.SaveFileDialog
                {
                    Filter = DelimitedExport.ExcelCsvTsvFilter,
                    FileName = $"فواتير_مشتريات_{DateTime.Now:yyyyMMdd}.xlsx"
                };

                if (dlg.ShowDialog() != true) return;

                string path = dlg.FileName;
                if (path.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase))
                {
                    ExportToExcelClosedXml(path);
                }
                else
                {
                    // P7-048/049: الفاصل وفق الامتداد وترميز الخلايا الموحّد
                    DelimitedExport.WriteDataTable(path, BuildDataTableForReport());
                }

                System.Diagnostics.Process.Start(
                    new System.Diagnostics.ProcessStartInfo(path)
                    { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ في التصدير: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        /// <summary>
        /// P7-050 fix: ملف xlsx حقيقي عبر ClosedXML (نمط frmInvDetails) —
        /// الأعمدة الرقمية تُكتب أرقاماً لا نصاً.
        /// </summary>
        private void ExportToExcelClosedXml(string filePath)
        {
            using var workbook = new ClosedXML.Excel.XLWorkbook();
            var worksheet = workbook.Worksheets.Add("Invoices");

            string[] headers =
            {
                "AutoIncrementID", "InvoiceTypeTxt", "InvGlobalID",
                "InvoiceNo", "ReffNo", "InvDate", "InvoiceTime",
                "PaymentTxt", "ClientTxt", "SumPrice", "TotDiscount",
                "Total", "VAT", "Net", "InvertoryName", "BranchTxt",
                "UserTxt", "ProcType", "Paid", "Remainder",
                "ExtraVAT", "TotalTax", "Paycash", "PayATM"
            };

            for (int c = 0; c < headers.Length; c++)
                worksheet.Cell(1, c + 1).Value = headers[c];

            int rowIdx = 2;
            foreach (var row in _invoiceRows)
            {
                var ex = _invExtras.TryGetValue(row.InvGlobalID, out var extras)
                    ? extras : null;
                double extraVatAmt = ex?.ExtraVATAmt ?? 0.0;

                worksheet.Cell(rowIdx, 1).Value = row.AutoIncrementID;
                worksheet.Cell(rowIdx, 2).Value = row.InvoiceTypeTxt;
                worksheet.Cell(rowIdx, 3).Value = row.InvGlobalID;
                worksheet.Cell(rowIdx, 4).Value = row.InvoiceNo.ToString();
                worksheet.Cell(rowIdx, 5).Value = row.ReffNo;
                worksheet.Cell(rowIdx, 6).Value =
                    row.InvDate.ToString("MM/d/yyyy hh:mm tt");
                worksheet.Cell(rowIdx, 7).Value = row.InvoiceTime;
                worksheet.Cell(rowIdx, 8).Value = row.PaymentTxt;
                worksheet.Cell(rowIdx, 9).Value = row.ClientTxt;
                worksheet.Cell(rowIdx, 10).Value = row.SumPrice;
                worksheet.Cell(rowIdx, 11).Value = row.TotDiscount;
                worksheet.Cell(rowIdx, 12).Value = row.Total;
                worksheet.Cell(rowIdx, 13).Value = row.VAT;
                worksheet.Cell(rowIdx, 14).Value = row.Net;
                worksheet.Cell(rowIdx, 15).Value = row.InvertoryName;
                worksheet.Cell(rowIdx, 16).Value = row.BranchTxt;
                worksheet.Cell(rowIdx, 17).Value = row.UserTxt;
                worksheet.Cell(rowIdx, 18).Value = row.ProcType;
                worksheet.Cell(rowIdx, 19).Value = row.Paid;
                worksheet.Cell(rowIdx, 20).Value = row.Remainder;
                worksheet.Cell(rowIdx, 21).Value = extraVatAmt;
                worksheet.Cell(rowIdx, 22).Value = row.VAT + extraVatAmt;
                worksheet.Cell(rowIdx, 23).Value = ex?.PayCash ?? 0.0;
                worksheet.Cell(rowIdx, 24).Value = ex?.PayAtm ?? 0.0;

                // تنسيق الأعمدة المالية — يبقى الرقم رقماً مع عرض الألوف
                // (صيغة Excel لا صيغة .NET)
                const string numberFormat = "#,##0.00";
                foreach (int col in new[] { 10, 11, 12, 13, 14, 19, 20, 21, 22, 23, 24 })
                    worksheet.Cell(rowIdx, col).Style.NumberFormat.Format = numberFormat;

                rowIdx++;
            }

            worksheet.Columns().AdjustToContents();
            workbook.SaveAs(filePath);
        }

        #endregion

        #region ══════════════════ Font Zoom ══════════════════

        private void btnZoom_Click(object sender, RoutedEventArgs e)
        {
            DgvFontSize++;
            GridControl2.FontSize =
                Math.Min(GridControl2.FontSize + DgvFontSize, 22);
        }

        private void btnZoomOut_Click(object sender, RoutedEventArgs e)
        {
            DgvFontSize = Math.Max(1, DgvFontSize - 1);
            GridControl2.FontSize =
                Math.Max(GridControl2.FontSize - DgvFontSize, 8);
        }

        #endregion

        #region ══════════════════ DGV Settings ══════════════════

        private void BtnSaveDgvSettings_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (!Directory.Exists(StyleFolder))
                    Directory.CreateDirectory(StyleFolder);

                var xml = new StringBuilder();
                xml.AppendLine("<Columns>");
                foreach (var col in GridControl2.Columns)
                {
                    if (col is DataGridTextColumn tc)
                        xml.AppendLine(
                            $"  <Column Name=\"{tc.Header}\"" +
                            $" Width=\"{tc.ActualWidth:F0}\"/>");
                }
                xml.AppendLine("</Columns>");
                File.WriteAllText(StyleFile, xml.ToString());

                MessageBox.Show("تم حفظ مظهر الجدول", "",
                    MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void BtnDefaultSetting_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (File.Exists(StyleFile))
                    File.Delete(StyleFile);

                MessageBox.Show("تمت إعادة الإعدادات الافتراضية", "",
                    MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch { }
        }

        #endregion

        #region ══════════════════ Button Events ══════════════════

        private void btnClose_Click(object sender, RoutedEventArgs e)
            => Close();

        private void btnPreview_Click(object sender, RoutedEventArgs e)
            => PrintDevexpress(2);

        private void btnPrint_Click(object sender, RoutedEventArgs e)
            => PrintDevexpress(1);

        #endregion

        #region ══════════════════ DataGrid Events ══════════════════

        private void GridControl2_MouseLeftButtonUp(
            object sender, MouseButtonEventArgs e)
        { }

        private void RepositoryItemBtnDetails_Click(
            object sender, RoutedEventArgs e)
        {
            try
            {
                if (sender is Button btn && btn.Tag is InvoiceTxt row)
                {
                    var frm = new frmInvoiceDetails();
                    MainClass.ApplyPermissionToForm(frm);
                    MainClass.DoApplyUserSett(frm);
                    frm.btnRecalculateCost.Visibility = Visibility.Collapsed;
                    frm.ISProfit = false;
                    frm.InvGlobalId = row.InvGlobalID;
                    frm.ShowDialog();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void RepositoryItemBtnShowInv_Click(
            object sender, RoutedEventArgs e)
        {
            try
            {
                if (sender is Button btn && btn.Tag is InvoiceTxt row)
                {
                    string invGlobalId = row.InvGlobalID;
                    int procType = row.ProcType;

                    var frm = new frmInvPurch();
                    if (procType == 2)
                        frm.Title = "مرتجع مشتريات";

                    // P2-001 fix (الشريحة الثالثة): صلاحيات المستخدم
                    // تُطبّق على المحرر المفتوح من التقرير قبل Show
                    MainClass.ApplyPermissionToForm(frm);
                    MainClass.DoApplyUserSett(frm);
                    frm.Show();
                    frm.InvType = 1;
                    frm.ProcType = procType;
                    frm.WindowState = WindowState.Maximized;
                    frm.Navigate(
                        "select * from Inv where IS_Deleted=0 " +
                        "and inv_type=1 and proc_type=" + procType +
                        " and InvGlobalID=N'" + invGlobalId + "'");
                    frm.Activate();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region ══════════════════ CheckBox Events ══════════════════

        private void ckAllType_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = ckAllType.IsChecked == true;
            cmbType.IsEnabled = !isAll;
            if (isAll) cmbType.SelectedIndex = -1;
        }

        private void cbAllSalesmen_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = cbAllSalesmen.IsChecked == true;
            cmbSaleman.IsEnabled = !isAll;
            if (isAll) cmbSaleman.SelectedIndex = -1;
        }

        private void ckAllClients_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = ckAllClients.IsChecked == true;
            cmbClients.IsEnabled = !isAll;
            if (isAll) cmbClients.SelectedIndex = -1;
        }

        private void ckAllUsers_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = ckAllUsers.IsChecked == true;
            cmbusers.IsEnabled = !isAll;
            if (isAll) cmbusers.SelectedIndex = -1;
        }

        private void ckTotalPeriod_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool enabled = ckTotalPeriod.IsChecked != true;
            txtFromDate.IsEnabled = enabled;
            txtToDate.IsEnabled = enabled;
            txtStartTime.IsEnabled = enabled;
            txtEndTime.IsEnabled = enabled;
        }

        private void chkAllBranches_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = chkAllBranches.IsChecked == true;
            cmbBranches.IsEnabled = !isAll;
            // P7-088 fix: «الكل» يلغي اختيار الفرع السابق — كان الإبقاء
            // على الاختيار مع تعطيل القائمة يُبقي قيد الفرع المختار
            // سابقاً في استعلام العرض
            if (isAll) cmbBranches.SelectedIndex = -1;
        }

        private void ckAllStore_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAll = ckAllStore.IsChecked == true;
            cmbStore.IsEnabled = !isAll;
            if (isAll) cmbStore.SelectedIndex = -1;
        }

        private void cmbClients_MouseLeftButtonDown(
            object sender, MouseButtonEventArgs e)
        {
            if (ckAllClients.IsChecked != true)
                AddNewClient();
        }

        #endregion

        #region ══════════════════ Helper Methods ══════════════════

        private void AddNewClient()
        {
            try
            {
                var frm = new frmSrchClient();
                MainClass.ApplyPermissionToForm(frm);
                MainClass.DoApplyUserSett(frm);
                frm.Type = 2;
                frm.ShowDialog();

                if (!string.IsNullOrEmpty(frm.Clientname))
                {
                    LoadCustomers();
                    cmbClients.SelectedValue = frm.ClientId;
                }
            }
            catch { }
        }

        #endregion
    }
}