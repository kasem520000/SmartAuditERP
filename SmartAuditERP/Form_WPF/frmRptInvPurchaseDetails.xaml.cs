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
        private int _branchFilterVersion;
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

        // Repair R-080 (audit finding P7-047): money columns the loaded result set did not carry.
        // They are published as unavailable (an empty cell), never as a fabricated zero.
        private readonly HashSet<string> _unavailableAmountColumns
            = new HashSet<string>();

        #endregion

        #region ══════════════════ Inner Model ══════════════════

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
        private QueryParams CollectQueryParams(int branchId)
        {
            string whereClause = $"inv.Inv_type={Invtype} and ";

            // Only an explicitly validated single branch is supported here.
            whereClause += $"inv.branch={branchId} and ";

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

            InvalidateBranchResults();
            if (chkAllBranches.IsChecked == true || cmbBranches.SelectedIndex < 0 ||
                cmbBranches.SelectedValue == null ||
                !int.TryParse(cmbBranches.SelectedValue.ToString(), out int branchId) || branchId <= 0)
            {
                MessageBox.Show("اختر فرعاً واحداً؛ عرض كل الفروع معطل حتى توثيق الصلاحيات ونطاق التقرير.",
                    "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            // The existing sentinel is not a complete authorization contract. When it
            // indicates restriction, fail closed if the session branch is absent or differs.
            if (!string.Equals(Accounting.BranchCondition, " ", StringComparison.Ordinal) &&
                (MainClass.BranchNo <= 0 || branchId != MainClass.BranchNo))
            {
                MessageBox.Show("تعذر التحقق من صلاحية الفرع المحدد.", "تنبيه",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            QueryParams queryParams;
            try { queryParams = CollectQueryParams(branchId); }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ في المرشحات: " + ex.Message, "خطأ",
                    MessageBoxButton.OK, MessageBoxImage.Error);
                return;
            }
            if (queryParams == null) return;
            int requestBranchVersion = _branchFilterVersion;

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
                        if (requestBranchVersion != _branchFilterVersion) return;
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
        /// - LEFT JOIN Safes بدل GetStoreName (N+1)
        /// - Cache لـ InvoiceObj
        /// </summary>
        private List<InvoiceTxt> BindingListOfInvoices1Async(
            QueryParams p,
            string overrideSql = null,
            bool withItems = false)
        {
            var list = new List<InvoiceTxt>();
            _unavailableAmountColumns.Clear();   // Repair R-080 (P7-047): per load, not per row

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

                            // Repair R-080 (audit finding P7-047): the output projection used to put
                            // the additional-tax RATE (ExtraVATPerc) into the ExtraVAT column and to
                            // leave TotalTax, Paycash and PayATM at a literal zero, so the printed
                            // sheet and the exported file mixed a percentage with amounts and stated
                            // financial zeros as facts. The amounts are on the row - the query selects
                            // Inv.* - and Inv.tax already carries the additional tax (InvoiceOper
                            // accumulates VAT += num + num2 and VAT += ExtraVAT), so every figure is
                            // taken from the same row the way the sales-details and notification
                            // screens read these very columns; a column the result set does not carry
                            // is recorded as unavailable instead of being invented as zero.
                            double extraAmount = ReadAmount(row, "ExtraVAT", out bool extraKnown);
                            if (!extraKnown) _unavailableAmountColumns.Add("ExtraVAT");
                            invoiceTxt.ExtraVAT = extraAmount;

                            // Inv.tax is the tax total and already carries the additional tax, so
                            // the main VAT is what remains of it - the sibling screens' convention -
                            // and the total tax published here is main + additional, never a zero
                            // beside a positive VAT.
                            double taxTotal = ReadAmount(row, "tax", out bool totalTaxKnown);
                            if (!totalTaxKnown) _unavailableAmountColumns.Add("TotalTax");
                            double mainVat = (taxTotal - extraAmount) > 0
                                ? taxTotal - extraAmount
                                : taxTotal;
                            invoiceTxt.TotalTax = mainVat + extraAmount;

                            invoiceTxt.Paycash = ReadAmount(row, "cash", out bool cashKnown);
                            if (!cashKnown) _unavailableAmountColumns.Add("Paycash");

                            invoiceTxt.PayATM = ReadAmount(row, "visa", out bool atmKnown);
                            if (!atmKnown) _unavailableAmountColumns.Add("PayATM");

                            // A settled cash invoice is published as paid in full, on the same rule
                            // the sibling screens apply to the same columns.
                            if (payTypeInt == 1 && ReadInt(row, "PaymentStatus") == 1)
                                invoiceTxt.Paycash = ReadAmount(row, "tot_net", out _);

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
        /// <summary>
        /// Repair R-080 (audit finding P7-047): reads a money column when the loaded result set
        /// actually carries it; <paramref name="known"/> is false for a missing column, a DBNull or
        /// a value that is not a number, so the caller publishes "unavailable" rather than a zero.
        /// </summary>
        private static double ReadAmount(DataRow row, string column, out bool known)
        {
            known = row.Table.Columns.Contains(column)
                    && row[column] != DBNull.Value
                    && double.TryParse(Convert.ToString(row[column]), out _);
            return known ? Convert.ToDouble(row[column]) : 0.0;
        }

        /// <summary>Repair R-080 (audit finding P7-047): same rule for a whole-number column.</summary>
        private static int ReadInt(DataRow row, string column)
        {
            return row.Table.Columns.Contains(column)
                   && row[column] != DBNull.Value
                   && int.TryParse(Convert.ToString(row[column]), out int value)
                ? value
                : 0;
        }

        /// <summary>
        /// Repair R-080 (audit finding P7-047): publishes a money value, or an empty cell when the
        /// source result set did not carry that column - unavailable, never an invented zero.
        /// </summary>
        private string AmountText(double value, string column)
        {
            return _unavailableAmountColumns.Contains(column)
                ? string.Empty
                : value.ToString(Common.DigitsNo ?? "N2");
        }

        private string BuildOptimizedSql(QueryParams p)
        {
            // Repair R-101 (audit finding P7-087): Inv.safe is a warehouse id
            // in Safes, not a treasury id in Stocks. Keep missing names as a left join.
            return
                "select Inv.*," +
                "(SELECT ISNULL(sum(Inv_Sub.val1*Inv_Sub.exchange_price),0) " +
                " from Inv_Sub where InvGlobalID=Inv.InvGlobalID) as sumPrice," +
                "(SELECT ISNULL(sum(discount),0) " +
                " from Inv_Sub where InvGlobalID=Inv.InvGlobalID) as ItemDiscount," +
                "Customers.name   as CustName," +
                "Users.username   as username," +
                "Branches.name    as BranchName," +
                "warehouse.name   as StoreName " +   // نفس جدول GetStoreName
                "from Inv " +
                "left join Customers on inv.cust_id   = Customers.id " +
                "left join Users     on inv.sales_emp = Users.emp " +
                "left join Branches  on inv.branch    = Branches.id " +
                "left join Safes warehouse on inv.safe = warehouse.id and inv.safe > 0 " +
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
                    sumNetFinal: lblSumNetFinal.Text);

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
            // Repair R-080 (audit finding P7-047): the rate keeps its own explicitly named column,
            // so ExtraVAT carries an amount and ExtraVATPerc carries a percentage.
            dt.Columns.Add("ExtraVATPerc", typeof(string));

            string fmt = Common.DigitsNo ?? "N2";

            foreach (var row in _invoiceRows)
            {
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
                    AmountText(row.ExtraVAT, "ExtraVAT"),        // amount, was the rate
                    AmountText(row.TotalTax, "TotalTax"),        // was the literal "0"
                    AmountText(row.Paycash, "Paycash"),          // was the literal "0"
                    AmountText(row.PayATM, "PayATM"),            // was the literal "0"
                    row.ExtraVATPerc.ToString(fmt));             // the rate, in its own column
            }
            return dt;
        }

        private void btnExportExcel_Click(object sender, RoutedEventArgs e)
        {
            if (_invoiceRows.Count == 0) return;
            try
            {
                var dlg = new Microsoft.Win32.SaveFileDialog
                {
                    // Repair R-088 (audit finding P7-050): this dialog offered *.xlsx and *.csv while
                    // every choice wrote the same tab-separated text, so the announced extension never
                    // matched the bytes on disk - an *.xlsx file holding text, and a *.csv file holding
                    // tabs where a comma is expected. Repair R-091 then gave each option a writer of
                    // its own instead of dropping one: a real workbook for *.xlsx, comma CSV for *.csv
                    // and tab-separated text for *.txt, all three from the very same table.
                    Filter = "Excel Files (*.xlsx)|*.xlsx|CSV Files (*.csv)|*.csv|"
                             + "Text - tab separated (*.txt)|*.txt",
                    DefaultExt = ".xlsx",
                    FileName = $"فواتير_مشتريات_{DateTime.Now:yyyyMMdd}.xlsx"
                };

                if (dlg.ShowDialog() != true) return;

                // Repair R-088 (audit finding P7-050): a name typed by hand can still ask for a
                // container this screen cannot produce. Refusing before writing is the honest answer,
                // so no file is left behind announcing a format its bytes do not have.
                bool asCsv = dlg.FileName.EndsWith(".csv", StringComparison.OrdinalIgnoreCase);
                bool asText = dlg.FileName.EndsWith(".txt", StringComparison.OrdinalIgnoreCase);
                bool asWorkbook = dlg.FileName.EndsWith(".xlsx", StringComparison.OrdinalIgnoreCase);
                if (!asCsv && !asText && !asWorkbook)
                {
                    MessageBox.Show(
                        "صيغة غير مدعومة للتصدير: اختر Excel (*.xlsx) أو CSV (*.csv) "
                        + "أو نصاً بفاصل جدولة (*.txt).",
                        "", MessageBoxButton.OK, MessageBoxImage.Information);
                    return;
                }

                var dt = BuildDataTableForReport();

                if (asWorkbook)
                {
                    // Repair R-091 (audit finding P7-050): a real workbook, written with the library
                    // the project already references and three other screens already use, so the
                    // *.xlsx bytes are a workbook. Cells keep the table's own types - the two integer
                    // columns leave as numbers and the rest as the text this screen formats for the
                    // printed report - so all three containers carry one and the same projection.
                    using (var workbook = new ClosedXML.Excel.XLWorkbook())
                    {
                        var worksheet = workbook.Worksheets.Add(dt, "فواتير المشتريات");
                        worksheet.RightToLeft = true;
                        worksheet.Columns().AdjustToContents();
                        workbook.SaveAs(dlg.FileName);
                    }
                }
                else
                {
                    // Repair R-088 (audit finding P7-050): the delimiter follows the chosen extension,
                    // so the file matches what the dialog announced. Repair R-082 (audit finding
                    // P7-048) still stands behind it: the shared writer announces one schema (comma or
                    // tab, doubled quotes, CRLF, UTF-8) and quotes whatever could break a record, and
                    // the cells keep the display formatting they were built with, because the same
                    // table feeds the printed report.
                    SpreadsheetExport.WriteDataTable(
                        dlg.FileName,
                        dt,
                        asCsv ? SpreadsheetExport.CsvDelimiter : SpreadsheetExport.TsvDelimiter);
                }

                System.Diagnostics.Process.Start(
                    new System.Diagnostics.ProcessStartInfo(dlg.FileName)
                    { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ في التصدير: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
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

        private void InvalidateBranchResults()
        {
            _branchFilterVersion++;
            _invoiceRows.Clear();
            InvoicesList?.Clear();
            CalculateSummary();
        }

        private void cmbBranches_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (IsLoaded) InvalidateBranchResults();
        }

        private void chkAllBranches_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            InvalidateBranchResults();
            cmbBranches.IsEnabled = chkAllBranches.IsChecked != true;
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