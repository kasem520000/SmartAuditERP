using DevExpress.Xpf.Core;
using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Threading;
using System.Windows;
using System.Windows.Controls;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmNkdTotSalePurchActCust : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;
        private ObservableCollection<SalePurchActRow> _rows;
        private bool _calculating;
        private int _criteriaVersion;

        #endregion

        #region Constructor

        public frmNkdTotSalePurchActCust()
        {
            conn  = MainClass.ConnObj();
            _rows = new ObservableCollection<SalePurchActRow>();
            InitializeComponent();
            foreach (ComboBox combo in new[] { cmbActs, cmbCust })
                combo.SelectionChanged += CriteriaSelectionChanged;
            foreach (CheckBox check in new[] { chkAllActs, chkAllCust })
            {
                check.Checked += CriteriaCheckedChanged;
                check.Unchecked += CriteriaCheckedChanged;
                check.Indeterminate += CriteriaCheckedChanged;
            }
            txtDateFrom.SelectedDateChanged += CriteriaSelectionChanged;
            txtDateTo.SelectedDateChanged += CriteriaSelectionChanged;
            // A worker still dispatches to this window; closing is deferred, not cancellation.
            Closing += (sender, e) =>
            {
                if (!_calculating) return;
                e.Cancel = true;
                DXMessageBox.Show("انتظر انتهاء حساب التقرير قبل إغلاق النافذة.",
                    "تنبيه", MessageBoxButton.OK, MessageBoxImage.Information);
            };
        }

        private void CriteriaSelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (IsLoaded) InvalidateResult();
        }

        private void CriteriaCheckedChanged(object sender, RoutedEventArgs e)
        {
            if (IsLoaded) InvalidateResult();
        }

        private void InvalidateResult()
        {
            _criteriaVersion++;
            _rows.Clear();
            txtSumPurch.Text = "0.00";
            txtSumSale.Text = "0.00";
        }

        #endregion

        #region Load

        private void frmNkdTotSalePurchActCust_Load(object sender, RoutedEventArgs e)
        {
            txtDateFrom.SelectedDate = DateTime.Today;
            txtDateTo.SelectedDate   = DateTime.Today;
            dgvItems.ItemsSource     = _rows;
            LoadActs();
        }

        public void LoadActs()
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter("select id,name from Acts order by id", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                cmbActs.ItemsSource = dt.DefaultView;
                cmbActs.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        #endregion

        #region CheckBox Events

        private void chkAllActs_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (cmbActs == null) return;

            if (chkAllActs.IsChecked == true)
            {
                cmbActs.IsEnabled  = false;
                cmbCust.IsEnabled  = false;
                if (chkAllCust != null)
                {
                    chkAllCust.IsChecked = true;
                    chkAllCust.IsEnabled = false;
                }
            }
            else
            {
                cmbActs.IsEnabled  = true;
                cmbCust.IsEnabled  = true;
                if (chkAllCust != null)
                {
                    chkAllCust.IsChecked = false;
                    chkAllCust.IsEnabled = true;
                }
            }
        }

        private void chkAllCust_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (cmbCust == null) return;
            cmbCust.IsEnabled = chkAllCust.IsChecked != true;
        }

        private void cmbActs_SelectedIndexChanged(object sender, SelectionChangedEventArgs e)
        {
            try
            {
                if (cmbActs.SelectedValue == null) return;

                SqlDataAdapter adapter = new SqlDataAdapter(
                    $"select id,name from customers where act={cmbActs.SelectedValue} order by id", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                cmbCust.ItemsSource = dt.DefaultView;
                cmbCust.SelectedIndex = -1;
            }
            catch { }
        }

        #endregion

        #region Show Result

        private void btnShow_Click(object sender, RoutedEventArgs e)
        {
            if (_calculating) return;
            InvalidateResult();

            int actId = 0, customerId = 0;
            bool allActs = chkAllActs.IsChecked == true;
            bool allCustomers = !chkAllCust.IsEnabled || chkAllCust.IsChecked == true;
            if (!allActs && (!int.TryParse(Convert.ToString(cmbActs.SelectedValue), out actId) || actId <= 0))
            {
                DXMessageBox.Show("يجب اختيار جهة العمل", "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            if (!allCustomers && (!int.TryParse(Convert.ToString(cmbCust.SelectedValue), out customerId) || customerId <= 0))
            {
                DXMessageBox.Show("يجب اختيار العميل", "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            if (!txtDateFrom.SelectedDate.HasValue || !txtDateTo.SelectedDate.HasValue ||
                txtDateFrom.SelectedDate.Value.Date > txtDateTo.SelectedDate.Value.Date ||
                txtDateTo.SelectedDate.Value.Date == DateTime.MaxValue.Date)
            {
                DXMessageBox.Show("نطاق التاريخ غير صالح", "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            DateTime from = txtDateFrom.SelectedDate.Value.Date;
            DateTime toExclusive = txtDateTo.SelectedDate.Value.Date.AddDays(1);
            int branch = MainClass.BranchNo;
            int version = _criteriaVersion;
            var controls = new Control[] { btnShow, cmbActs, chkAllActs, cmbCust, chkAllCust, txtDateFrom, txtDateTo };
            var enabled = new bool[controls.Length];
            for (int i = 0; i < controls.Length; i++)
            {
                enabled[i] = controls[i].IsEnabled;
                controls[i].IsEnabled = false;
            }
            _calculating = true;
            ProgressBar1.Visibility = Visibility.Visible;
            try
            {
                var worker = new Thread(() =>
                {
                    try { CalcStock(actId, customerId, allActs, allCustomers, branch, from, toExclusive, version); }
                    catch (Exception ex)
                    {
                        Dispatcher.Invoke(() =>
                        {
                            if (version != _criteriaVersion) return;
                            InvalidateResult();
                            ShowError(ex);
                        });
                    }
                    finally
                    {
                        Dispatcher.Invoke(() =>
                        {
                            ProgressBar1.Visibility = Visibility.Collapsed;
                            for (int i = 0; i < controls.Length; i++) controls[i].IsEnabled = enabled[i];
                            _calculating = false;
                        });
                    }
                }) { IsBackground = true };
                worker.SetApartmentState(ApartmentState.STA);
                worker.Start();
            }
            catch
            {
                ProgressBar1.Visibility = Visibility.Collapsed;
                for (int i = 0; i < controls.Length; i++) controls[i].IsEnabled = enabled[i];
                _calculating = false;
                throw;
            }
        }

        private void CalcStock(int actId, int customerId, bool allActs, bool allCustomers,
            int branch, DateTime dateFrom, DateTime dateToExclusive, int version)
        {
            DataTable itemsDt = new DataTable();
            using (var itemAdapter = new SqlDataAdapter(
                "select id,name,nameEN from Items where IS_Deleted=0 order by id", conn))
                itemAdapter.Fill(itemsDt);

            double totalPurch = 0.0, totalSale = 0.0;
            var stagedRows = new System.Collections.Generic.List<SalePurchActRow>();
            string branchFilter = branch != -1 ? $"inv.branch={branch} and " : "";
            string actFilter = allActs ? "" : $"acts.id={actId} and ";
            string custFilter = allCustomers ? "" : $"customers.id={customerId} and ";
            Dispatcher.Invoke(() => { ProgressBar1.Maximum = Math.Max(1, itemsDt.Rows.Count); ProgressBar1.Value = 0; });

            for (int i = 0; i < itemsDt.Rows.Count; i++)
            {
                int itemId = Convert.ToInt32(itemsDt.Rows[i]["id"]);
                string itemName = string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                    ? itemsDt.Rows[i]["name"].ToString() : itemsDt.Rows[i]["nameEN"].ToString();
                string baseWhere = $"inv,inv_sub,customers,acts where {branchFilter} Inv_Sub.ItemId={itemId} and inv.cust_id=customers.id and customers.act=acts.id and {actFilter}{custFilter} date>=@date1 and date<@date2";

                double pQty = 0, pTotal = 0, pRetQty = 0, pRetTotal = 0;
                double sQty = 0, sTotal = 0, sRetQty = 0, sRetTotal = 0;
                ExecuteItemQuery($"select sum(val),sum(val1*exchange_price) from {baseWhere} and inv.inv_type=1 and inv.proc_type=1 and inv_sub.proc_type=1 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                    conn, dateFrom, dateToExclusive, ref pQty, ref pTotal);
                ExecuteItemQuery($"select sum(val),sum(val1*exchange_price) from {baseWhere} and inv.inv_type=1 and inv.proc_type=2 and inv_sub.proc_type=2 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                    conn, dateFrom, dateToExclusive, ref pRetQty, ref pRetTotal);
                ExecuteItemQuery($"select sum(val),sum(val1*exchange_price) from {baseWhere} and inv.inv_type IN (2,3) and inv.proc_type=1 and inv_sub.proc_type=2 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                    conn, dateFrom, dateToExclusive, ref sQty, ref sTotal);
                ExecuteItemQuery($"select sum(val),sum(val1*exchange_price) from {baseWhere} and inv.inv_type IN (2,3) and inv.proc_type=2 and inv_sub.proc_type=1 and inv.InvGlobalID=inv_sub.InvGlobalID and inv.IS_Deleted=0",
                    conn, dateFrom, dateToExclusive, ref sRetQty, ref sRetTotal);

                double netPQty = pQty - pRetQty, netPTotal = pTotal - pRetTotal;
                double netSQty = sQty - sRetQty, netSTotal = sTotal - sRetTotal;
                if (netPQty != 0.0 || netSQty != 0.0 || netPTotal != 0.0 || netSTotal != 0.0)
                {
                    totalPurch += netPTotal;
                    totalSale += netSTotal;
                    stagedRows.Add(new SalePurchActRow
                    {
                        Column1 = itemId.ToString(), Column2 = itemName,
                        Column3 = netPQty.ToString("N4"), Column4 = netPTotal.ToString("N4"),
                        Column6 = netSQty.ToString("N4"), Column5 = netSTotal.ToString("N4")
                    });
                }
                Dispatcher.Invoke(() => { if (version == _criteriaVersion) ProgressBar1.Value++; });
            }
            Dispatcher.Invoke(() =>
            {
                if (version != _criteriaVersion) return;
                _rows.Clear();
                foreach (SalePurchActRow row in stagedRows) _rows.Add(row);
                txtSumPurch.Text = totalPurch.ToString("N2");
                txtSumSale.Text = totalSale.ToString("N2");
            });
        }

        private void ExecuteItemQuery(string sql, SqlConnection conn, DateTime date1, DateTime date2,
            ref double qty, ref double total)
        {
            using (var adapter = new SqlDataAdapter(sql, conn))
            {
                adapter.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value = date1;
                adapter.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value = date2;
                DataTable dt = new DataTable();
                adapter.Fill(dt);
                if (dt.Rows.Count == 0 || (dt.Rows[0][0] == DBNull.Value && dt.Rows[0][1] == DBNull.Value)) return;
                if (dt.Rows[0][0] == DBNull.Value || dt.Rows[0][1] == DBNull.Value)
                    throw new InvalidOperationException("مجاميع حركة الصنف غير مكتملة.");
                qty = Convert.ToDouble(dt.Rows[0][0]);
                total = Convert.ToDouble(dt.Rows[0][1]);
                if (double.IsNaN(qty) || double.IsInfinity(qty) || double.IsNaN(total) || double.IsInfinity(total))
                    throw new InvalidOperationException("مجاميع حركة الصنف غير صالحة.");
                total = Math.Round(total, 4);
            }
        }

        #endregion

        #region Print (Stubs)

        private void btnPreview_Click(object sender, RoutedEventArgs e) { }
        private void btnPrint_Click(object sender, RoutedEventArgs e)   { }

        #endregion

        #region Close & Helpers

        private void btnClose_Click(object sender, RoutedEventArgs e) => Close();

        private void ShowError(Exception ex)
        {
            DXMessageBox.Show("خطأ" + Environment.NewLine + ex.Message,
                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion
    }

    public class SalePurchActRow
    {
        public string Column1 { get; set; }
        public string Column2 { get; set; }
        public string Column3 { get; set; }
        public string Column4 { get; set; }
        public string Column6 { get; set; }
        public string Column5 { get; set; }
    }
}