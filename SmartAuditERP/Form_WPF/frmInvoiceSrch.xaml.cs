using DevExpress.Xpf.Core;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Button = System.Windows.Controls.Button;
using KeyEventArgs = System.Windows.Input.KeyEventArgs;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmInvoiceSrch : DevExpress.Xpf.Core.ThemedWindow
    {
        // ══════════════════════════════════════════════════════════
        #region Public Fields

        public int    selectedCli;
        public int    StoreId;
        public string sql;
        public string Cond;
        public int    ProcType;
        public int    PayType;
        public string InvGlobalID;
        public int    InvType;
        public bool   ISDone;
        public int    Inv_typeCridet;
        // Repair R-077 (audit finding P7-157): the inv_type of the row the caller accepted;
        // -1 while nothing was accepted.
        public int    SelectedInvType;
        // Repair R-079 (audit finding P7-046, extension B28): whether the rows the caller could
        // accept came from a source that actually succeeded for the current request, so a
        // consumer can separate a valid document id from a valid search result.
        public bool   SnapshotValid => _snapshotValid;

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Private Fields

        private readonly SqlConnection               _conn;
        private string                               _loadQuery;
        private DataTable                            _masterTable;
        private int                                  _rowIndex;
        private ObservableCollection<InvoiceSrchRow> _displayRows;
        // Repair R-075 (audit finding P7-155): the proc_type criterion the master snapshot was
        // actually loaded with, so a process change can tell 'already loaded' from 'must reload'.
        private int                                  _snapshotProc;
        // Repair R-076 (audit finding P7-156): the mandatory condition the CALLER supplied before
        // ShowDialog (document eligibility), kept apart from the optional filters this form owns.
        private string                               _callerCond;
        // Repair R-079 (audit finding P7-046, extension B28): whether the displayed rows come from
        // a source that actually succeeded; a failed load must not leave the previous snapshot
        // selectable as if it answered the current request.
        private bool                                 _snapshotValid;

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Constructor

        public frmInvoiceSrch()
        {
            InitializeComponent();

            _conn        = MainClass.ConnObj();
            StoreId      = 1;
            ProcType     = 1;
            PayType      = 1;
            InvGlobalID  = "-1";
            InvType      = 6;
            ISDone       = false;
            SelectedInvType = -1;
            _masterTable = new DataTable();
            _rowIndex    = -1;
            _displayRows = new ObservableCollection<InvoiceSrchRow>();
            Cond         = string.Empty;
            _snapshotProc = -1;
            _callerCond   = string.Empty;
            _snapshotValid = false;

            dgvItems.ItemsSource = _displayRows;
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Window Events

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            // Repair R-076 (audit finding P7-156): capture the caller's eligibility condition
            // before anything here can touch Cond, so the date handlers and Clear can restore it
            // instead of replacing it. Callers such as the transfer receive button pass
            // `Cond += " AND InvoiceStatus = 1"` and rely on it for the whole dialog lifetime.
            _callerCond = Cond ?? string.Empty;

            txtFromDate.SelectedDate = DateTime.Today;
            txtToDate.SelectedDate   = DateTime.Today;

            LoadUsers();
            LoadProcessTypes();

            // Repair R-075 (audit finding P7-155): the snapshot is about to be loaded with this
            // ProcType, and assigning SelectedIndex below raises SelectionChanged; recording it
            // first keeps that programmatic selection from triggering a redundant reload.
            _snapshotProc = ProcType;

            if (cmbProcType.Items.Count > ProcType)
                cmbProcType.SelectedIndex = ProcType;

            LoadInvoices();
            ApplyColumnVisibility();
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
            {
                // Repair R-079 (audit finding P7-046, extension B28): never accept from a snapshot
                // whose source failed, whatever the last selected index was.
                if (_snapshotValid && _rowIndex > -1 && _rowIndex < _displayRows.Count)
                {
                    try
                    {
                        var row     = _displayRows[_rowIndex];
                        ISDone      = true;
                        InvGlobalID = row.InvGlobalID;
                        ProcType    = row.ProcType;
                        PayType     = row.PayType;
                        SelectedInvType = row.SourceInvType;
                        Close();
                    }
                    catch { }
                    return;
                }

                if (_displayRows.Count > 0)
                {
                    dgvItems.SelectedIndex = 0;
                    dgvItems.ScrollIntoView(_displayRows[0]);
                }
            }
            else if (e.Key == Key.Up)   NavigateUp();
            else if (e.Key == Key.Down)  NavigateDown();
            else if (e.Key == Key.Escape) Close();
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Header/Close Events

        private void btnClose_Click(object sender, RoutedEventArgs e)
        {
            if (MainClass.ReturnYearPreviews)
            {
                MainClass.ReturnYearPreviews = false;
                MainClass.connstr = MainClass.originalConnStr;
            }
            Close();
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Filter Events

        private void cmbProcType_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // Repair R-075 (audit finding P7-155): BuildLoadQuery bakes `inv.proc_type = {ProcType}`
            // into the master snapshot, so changing this combo used to re-filter only the rows the
            // ORIGINAL process type had already admitted: choosing another process showed an empty
            // grid and the item labelled 'All' showed one process. The source criterion now follows
            // the selection - index 0 means no process restriction, any other index reloads with
            // that proc_type - and BuildFilterExpression stays as a matching control on the reload.
            int wanted = cmbProcType.SelectedIndex;
            if (wanted < 0) return;

            if (wanted == _snapshotProc)
            {
                ApplyFilter();
                return;
            }

            ProcType = wanted;
            _masterTable.Clear();
            LoadInvoices();
        }

        private void txtInvNo_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void txtClientName_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void txtClientMobile_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void txtSrchreffNo_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void txtTableNoSearch_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void TxtNotes_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void txtMinPrice_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void txtMaxPrice_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (!string.IsNullOrWhiteSpace(txtMaxPrice.Text) &&
                string.IsNullOrWhiteSpace(txtMinPrice.Text))
                txtMinPrice.Text = "0";

            // Repair R-074 (audit finding P7-158): the re-filter used to live inside the
            // "a ceiling is present" branch, so clearing the field left the grid on the previous
            // restricted snapshot until some other control happened to filter again. The predicate
            // builder already omits the ceiling when the text does not parse, so filtering on every
            // edit - the empty and whitespace cases included - widens the view back immediately.
            ApplyFilter();
        }

        private void txtFromDate_SelectedDateChanged(object sender, SelectionChangedEventArgs e)
        {
            if (txtFromDate.IsEnabled)
            {
                // Repair R-076 (audit finding P7-156): intersect with the caller's condition;
                // assigning the date clause alone dropped the document eligibility it passed.
                Cond = _callerCond + " and inv.date >= @date1 and inv.date <= @date2 ";
                _masterTable.Clear();
                LoadInvoices();
            }
        }

        private void txtToDate_SelectedDateChanged(object sender, SelectionChangedEventArgs e)
        {
            if (txtToDate.IsEnabled)
            {
                // Repair R-076 (audit finding P7-156): intersect with the caller's condition;
                // assigning the date clause alone dropped the document eligibility it passed.
                Cond = _callerCond + " and inv.date >= @date1 and inv.date <= @date2 ";
                _masterTable.Clear();
                LoadInvoices();
            }
        }

        private void cmbUsers_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ApplyFilter();
        }

        private void btnPostPone_CheckedChanged(object sender, RoutedEventArgs e)
        {
            ApplyFilter();
        }

        private void ckUnPaid_CheckedChanged(object sender, RoutedEventArgs e)
        {
            ApplyFilter();
        }

        private void ckTotalPeriod_CheckedChanged(object sender, RoutedEventArgs e)
        {
            bool isAllPeriod       = ckTotalPeriod.IsChecked ?? true;
            txtFromDate.IsEnabled  = !isAllPeriod;
            txtToDate.IsEnabled    = !isAllPeriod;
        }

        private void txtFilter_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Up)    NavigateUp();
            else if (e.Key == Key.Down) NavigateDown();
        }

        private void btnClear_Click(object sender, RoutedEventArgs e)
        {
            txtMaxPrice.Text         = "";
            txtMinPrice.Text         = "";
            txtInvNo.Text            = "";
            txtClientName.Text       = "";
            txtClientMobile.Text     = "";
            txtSrchreffNo.Text       = "";
            txtTableNoSearch.Text    = "";
            TxtNotes.Text            = "";
            cmbUsers.SelectedIndex   = -1;
            // Repair R-076 (audit finding P7-156): Clear resets THIS form's optional filters; the
            // caller's mandatory eligibility condition is not this form's to drop.
            Cond                     = _callerCond;

            if (cmbProcType.Items.Count > 1)
                cmbProcType.SelectedIndex = 1;

            _masterTable.Clear();
            LoadInvoices();
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Grid Events

        private void dgvItems_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            _rowIndex = dgvItems.SelectedIndex;
        }

        private void dgvItems_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            try
            {
                var row = dgvItems.SelectedItem as InvoiceSrchRow;
                if (row == null || !_snapshotValid) return;   // Repair R-079 (P7-046 ext. B28)

                ISDone      = true;
                InvGlobalID = row.InvGlobalID;
                ProcType    = row.ProcType;
                PayType     = row.PayType;
                SelectedInvType = row.SourceInvType;
                Hide();
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message, "خطأ",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void BtnReturn_Click(object sender, RoutedEventArgs e)
        {
            if (sender is not Button btn) return;
            if (btn.Tag is not InvoiceSrchRow row) return;
            if (!_snapshotValid) return;   // Repair R-079 (P7-046 ext. B28): stale snapshot

            if (IsPreviousReturned(row.InvGlobalID))
            {
                DXMessageBox.Show("الفاتورة تم إرجاعها سابقاً", "تنبيه",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            InvGlobalID = row.InvGlobalID;
            ProcType    = row.ProcType;
            PayType     = row.PayType;
            SelectedInvType = row.SourceInvType;
            ISDone      = true;
            Hide();
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Data Loading

        public void LoadInvoices()
        {
            try
            {
                BuildLoadQuery();
                _snapshotProc = ProcType;   // Repair R-075 (P7-155): criterion now in the snapshot

                var adapter = new SqlDataAdapter(_loadQuery, _conn);

                if (!string.IsNullOrWhiteSpace(Cond) && Cond.Contains("@date"))
                {
                    DateTime toDate = (txtToDate.SelectedDate ?? DateTime.Today).AddHours(24);
                    adapter.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value =
                        (txtFromDate.SelectedDate ?? DateTime.Today).ToShortDateString();
                    adapter.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value =
                        toDate;
                }

                adapter.Fill(_masterTable);
                ApplyFilter();
                _snapshotValid = true;
            }
            catch (Exception ex)
            {
                // Repair R-079 (audit finding P7-046, extension B28): the master table may already
                // have been cleared by the caller and the fill may have failed halfway, while the
                // display still held the PREVIOUS successful rows - selectable, so a caller could
                // accept a document this request never returned. A failed load now publishes
                // failure: no rows, no acceptance, and a status saying the source failed. A
                // known-empty result is a different state and still shows its zero count.
                _snapshotValid = false;
                _displayRows.Clear();
                _rowIndex = -1;
                lblStatus.Text = MainClass.Language == "ar"
                    ? "⚠ فشل تحميل نتائج البحث، لا توجد نتائج صالحة للاختيار"
                    : "⚠ Loading the search results failed; nothing valid to select";
                Console.WriteLine(ex.Message);
            }
        }

        private void BuildLoadQuery()
        {
            string condClause = Cond;

            if (InvType != 14)
                condClause += $" and inv.branch = {MainClass.BranchNo}";

            // Repair R-075 (audit finding P7-155): ProcType 0 is the "All" selection, which must
            // widen the source instead of silently keeping the criterion of the opening caller.
            if (ProcType > 0)
                condClause += $" and inv.proc_type = {ProcType}";

            if (btnPostPone.IsChecked == true)
                condClause += " and inv.Pay_type = -1";

            if (InvType == 23)
            {
                _loadQuery = $@"
                    SELECT inv.InvGlobalID,
                           inv.proc_type,
                           inv.inv_type      AS SourceInvType,
                           inv.id             AS id,
                           inv.Reff_No        AS ReffNo,
                           inv.tot_net        AS Net,
                           inv.Pay_type       AS PayType,
                           inv.date,
                           inv.PaymentStatus,
                           (SELECT ISNULL(Customers.name,'')
                            FROM Customers WHERE inv.cust_id = Customers.id) AS cust,
                           inv.notes,
                           inv.CashCustomerName,
                           inv.CashCustomerMobile,
                           (SELECT ISNULL(Customers.mobile,'')
                            FROM Customers WHERE inv.cust_id = Customers.id) AS mobile,
                           ISNULL(inv.TableNo,'') AS TableNo,
                           (SELECT ISNULL(Users.username,'')
                            FROM Users WHERE inv.sales_emp = Users.emp) AS emp
                    FROM   InvContratct inv
                    LEFT JOIN Customers ON inv.cust_id    = Customers.id
                    LEFT JOIN Users     ON inv.sales_emp  = Users.emp
                    LEFT JOIN Branches  ON inv.branch     = Branches.id
                    WHERE  inv.IS_Deleted = 0
                      AND  inv_type       = {InvType}
                      {condClause}
                    ORDER BY inv.id DESC";
            }
            else
            {
                _loadQuery = $@"
                    SELECT inv.InvGlobalID,
                           inv.proc_type,
                           inv.inv_type      AS SourceInvType,
                           inv.id             AS id,
                           inv.Reff_No        AS ReffNo,
                           inv.tot_net        AS Net,
                           inv.Pay_type       AS PayType,
                           inv.date,
                           inv.PaymentStatus,
                           (SELECT ISNULL(Customers.name,'')
                            FROM Customers WHERE inv.cust_id = Customers.id) AS cust,
                           inv.notes,
                           inv.CashCustomerName,
                           inv.CashCustomerMobile,
                           (SELECT ISNULL(Customers.mobile,'')
                            FROM Customers WHERE inv.cust_id = Customers.id) AS mobile,
                           ISNULL(inv.TableNo,'') AS TableNo,
                           (SELECT ISNULL(Users.username,'')
                            FROM Users WHERE inv.sales_emp = Users.emp) AS emp
                    FROM   Inv
                    LEFT JOIN Customers ON inv.cust_id   = Customers.id
                    LEFT JOIN Users     ON inv.sales_emp = Users.emp
                    LEFT JOIN Branches  ON inv.branch    = Branches.id
                    WHERE  inv.IS_Deleted = 0
                      AND  (inv_type = 20 OR inv_type = {InvType})
                      {condClause}
                    ORDER BY inv.id DESC";
            }
        }

        public void LoadUsers()
        {
            try
            {
                var table = new DataTable();
                new SqlDataAdapter(
                    "SELECT emp, username FROM Users WHERE IS_Deleted = 0 AND id > 0 ORDER BY emp",
                    _conn).Fill(table);

                cmbUsers.ItemsSource       = table.DefaultView;
                cmbUsers.DisplayMemberPath = "username";
                cmbUsers.SelectedValuePath = "emp";
                cmbUsers.SelectedIndex     = -1;
            }
            catch { }
        }

        public void LoadProcessTypes()
        {
            cmbProcType.Items.Clear();
            bool isAr = MainClass.Language == "ar";

            cmbProcType.Items.Add(isAr ? "الكل" : "All");

            switch (InvType)
            {
                case 1:
                    cmbProcType.Items.Add(isAr ? "مشتريات"    : "Purchase Invoice");
                    cmbProcType.Items.Add(isAr ? "مرتجع"      : "Return");
                    break;

                case 9:
                    cmbProcType.Items.Add(isAr ? "أول المدة"  : "Goods first term");
                    break;

                case 2:
                case 3:
                    cmbProcType.Items.Add(isAr ? "مبيعات"     : "Sales Invoice");
                    cmbProcType.Items.Add(isAr ? "مرتجع"      : "Return");
                    cmbProcType.Items.Add(isAr ? "معلق"       : "Hold");
                    cmbProcType.Items.Add(isAr ? "عرض سعر"    : "Quotation");
                    break;

                case 4:
                    cmbProcType.Items.Add(isAr ? "فاتورة إدخال" : "Input Invoice");
                    break;

                case 5:
                    cmbProcType.Items.Add(isAr ? "فاتورة إخراج" : "Output Invoice");
                    break;

                case 8:
                    cmbProcType.Items.Add(isAr ? "فاتورة إستلام" : "Receive Invoice");
                    cmbProcType.Items.Add(isAr ? "فاتورة إرسال"  : "Send Transfer");
                    break;

                case 14:
                    cmbProcType.Items.Add(isAr ? "طلب بضاعة"  : "Inventory Order");
                    break;

                case 21:
                case 22:
                    cmbProcType.Items.Add(isAr ? "إشعار مدين" : "Debit Notice");
                    cmbProcType.Items.Add(isAr ? "إشعار دائن" : "Credit Notice");
                    break;

                case 23:
                    cmbProcType.Items.Add(isAr ? "فاتورة مقاولات" : "Contract Invoice");
                    break;

                default:
                    cmbProcType.Items.Add(isAr ? "فاتورة" : "Invoice");
                    cmbProcType.Items.Add(isAr ? "مرتجع"  : "Return");
                    break;
            }
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Filter Logic

        private void ApplyFilter()
        {
            if (_masterTable == null) return;

            try
            {
                string filterExpr = BuildFilterExpression();

                var view = new DataView(_masterTable)
                {
                    RowFilter = filterExpr
                };

                RefreshDisplayRows(view);
            }
            catch { }
        }

        private string BuildFilterExpression()
        {
            var conditions = new List<string>();

            // نوع العملية
            int procIndex = cmbProcType.SelectedIndex;
            if (procIndex > 0)
                conditions.Add($"proc_type = {procIndex}");

            // رقم الفاتورة
            if (!string.IsNullOrWhiteSpace(txtInvNo.Text) &&
                int.TryParse(txtInvNo.Text.Trim(), out int invNo))
                conditions.Add($"id = {invNo}");

            // رقم المرجع
            if (!string.IsNullOrWhiteSpace(txtSrchreffNo.Text))
                conditions.Add($"ReffNo LIKE '%{txtSrchreffNo.Text.Trim()}%'");

            // العميل
            if (!string.IsNullOrWhiteSpace(txtClientName.Text))
                conditions.Add($"(cust LIKE '%{txtClientName.Text.Trim()}%'" +
                               $" OR CashCustomerName LIKE '%{txtClientName.Text.Trim()}%')");

            // جوال العميل
            if (!string.IsNullOrWhiteSpace(txtClientMobile.Text))
                conditions.Add($"(mobile LIKE '%{txtClientMobile.Text.Trim()}%'" +
                               $" OR CashCustomerMobile LIKE '%{txtClientMobile.Text.Trim()}%')");

            // المستخدم
            if (cmbUsers.SelectedIndex > -1 && !string.IsNullOrWhiteSpace(cmbUsers.Text))
                conditions.Add($"emp LIKE '%{cmbUsers.Text.Trim()}%'");

            // رقم الطاولة
            if (!string.IsNullOrWhiteSpace(txtTableNoSearch.Text))
                conditions.Add($"TableNo LIKE '%{txtTableNoSearch.Text.Trim()}%'");

            // البيان
            if (!string.IsNullOrWhiteSpace(TxtNotes.Text))
                conditions.Add($"notes LIKE '%{TxtNotes.Text.Trim()}%'");

            // الصافي
            if (double.TryParse(txtMinPrice.Text, out double minPrice))
                conditions.Add($"Net >= {minPrice}");
            if (double.TryParse(txtMaxPrice.Text, out double maxPrice))
                conditions.Add($"Net <= {maxPrice}");

            // آجل
            if (btnPostPone.IsChecked == true)
                conditions.Add("PayType = -1");

            // غير مدفوعة
            if (ckUnPaid.IsChecked == true)
                conditions.Add("(PaymentStatus = 0 OR PaymentStatus = 2)");

            return string.Join(" AND ", conditions);
        }

        private void RefreshDisplayRows(DataView view)
        {
            _displayRows.Clear();

            foreach (DataRowView rv in view)
            {
                _displayRows.Add(new InvoiceSrchRow
                {
                    InvGlobalID      = rv["InvGlobalID"]?.ToString()      ?? "",
                    ProcType         = SafeInt(rv["proc_type"]),
                    SourceInvType    = SafeInt(rv["SourceInvType"]),
                    Id               = SafeInt(rv["id"]),
                    ReffNo           = rv["ReffNo"]?.ToString()           ?? "",
                    Net              = SafeDouble(rv["Net"]),
                    PayType          = SafeInt(rv["PayType"]),
                    InvDate          = rv["date"] == DBNull.Value
                                        ? DateTime.MinValue
                                        : Convert.ToDateTime(rv["date"]),
                    PaymentStatus    = SafeInt(rv["PaymentStatus"]),
                    CustomerName     = rv["cust"]?.ToString()             ?? "",
                    Notes            = rv["notes"]?.ToString()            ?? "",
                    CashCustomerName = rv["CashCustomerName"]?.ToString() ?? "",
                    CashCustomerMobile = rv["CashCustomerMobile"]?.ToString() ?? "",
                    Mobile           = rv["mobile"]?.ToString()           ?? "",
                    TableNo          = rv["TableNo"]?.ToString()          ?? "",
                    EmpName          = rv["emp"]?.ToString()              ?? ""
                });
            }

            UpdateStatus();
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Business Logic

        private bool IsPreviousReturned(string invGlobalID)
        {
            try
            {
                string query = $@"
                    SELECT id FROM Inv
                    WHERE  proc_type   = 2
                      AND  inv_type    = 3
                      AND  Reff_No     = {invGlobalID}
                      AND  IS_Deleted  = 0";

                var table = new DataTable();
                new SqlDataAdapter(query, _conn).Fill(table);
                return table.Rows.Count >= 1;
            }
            catch { return false; }
        }

        private void ApplyColumnVisibility()
        {
            // إظهار/إخفاء عمود الطاولة
            if (ColReturnInv != null)
                ColReturnInv.Visibility = ProcType == 2
                    ? Visibility.Visible
                    : Visibility.Collapsed;

            // تغيير تسمية العميل حسب نوع الفاتورة
            bool isAr = MainClass.Language == "ar";
            if (InvType == 1)
            {
                lblClient.Text = isAr ? "المورد:" : "Supplier:";
                lblClientMobile.Text = isAr ? "جوال المورد:" : "Supplier Mobile:";
            }
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Navigation & UI Helpers

        private void NavigateUp()
        {
            if (dgvItems.SelectedIndex > 0)
                dgvItems.SelectedIndex--;
        }

        private void NavigateDown()
        {
            if (dgvItems.SelectedIndex < _displayRows.Count - 1)
                dgvItems.SelectedIndex++;
        }

        private void UpdateStatus()
        {
            lblStatus.Text = MainClass.Language == "ar"
                ? $"🧾 إجمالي الفواتير: {_displayRows.Count}"
                : $"🧾 Total Invoices: {_displayRows.Count}";
        }

        private static int SafeInt(object value)
            => value == null || value == DBNull.Value ? 0 : Convert.ToInt32(value);

        private static double SafeDouble(object value)
            => value == null || value == DBNull.Value ? 0.0 : Convert.ToDouble(value);

        #endregion
    }

    // ══════════════════════════════════════════════════════════════
    #region Model: InvoiceSrchRow

    public class InvoiceSrchRow : INotifyPropertyChanged
    {
        public string   InvGlobalID        { get; set; }
        public int      ProcType           { get; set; }
        // Repair R-077 (audit finding P7-157): the source document type, so a consumer can tell
        // whether the picked row is inside the set it asked for.
        public int      SourceInvType      { get; set; }
        public int      Id                 { get; set; }
        public string   ReffNo             { get; set; }
        public double   Net                { get; set; }
        public int      PayType            { get; set; }
        public DateTime InvDate            { get; set; }
        public int      PaymentStatus      { get; set; }
        public string   CustomerName       { get; set; }
        public string   Notes              { get; set; }
        public string   CashCustomerName   { get; set; }
        public string   CashCustomerMobile { get; set; }
        public string   Mobile             { get; set; }
        public string   TableNo            { get; set; }
        public string   EmpName            { get; set; }

        public event PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string name)
            => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }

    #endregion
}