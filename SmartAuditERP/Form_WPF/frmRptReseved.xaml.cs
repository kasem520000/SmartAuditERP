using DevExpress.Xpf.Core;
using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using Button = System.Windows.Controls.Button;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmRptReseved : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        public SqlConnection conn;
        public SqlConnection conn1;
        public string cond;

        private ObservableCollection<ResevedRow> ResevedList;

        #endregion

        #region Constructor

        public frmRptReseved()
        {
            InitializeComponent();

            conn  = MainClass.ConnObj();
            conn1 = MainClass.ConnObj();
            cond  = "";

            ResevedList = new ObservableCollection<ResevedRow>();
            GridControl2.ItemsSource = ResevedList;
        }

        #endregion

        #region Window Loaded

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            txtStartDate.DateTime = DateTime.Today;
            txtEndDate.DateTime   = DateTime.Today;
        }

        #endregion

        #region Load Data

        public void LoadData(string filterCond)
        {
            try
            {
                if (conn.State == ConnectionState.Open) conn.Close();
                conn.Open();

                ResevedList.Clear();

                string sql =
                    "SELECT SR.id, SR.Date, SR.EntryGlobalID, SR.GlobalID, " +
                    "B.name, SR.month, SR.year, SR.Notes " +
                    "FROM Salary_Res SR " +
                    "LEFT JOIN Branches B ON B.code=SR.branch " +
                    $"WHERE SR.IS_Deleted=0 {filterCond}";

                var adapter = new SqlDataAdapter(sql, conn);
                var dt = new DataTable();
                adapter.Fill(dt);

                for (int i = 0; i < dt.Rows.Count; i++)
                {
                    DataRow row = dt.Rows[i];
                    ResevedList.Add(new ResevedRow
                    {
                        DgvNo        = i + 1,
                        Id           = Convert.ToInt32(row["id"]),
                        DateRes      = Convert.ToDateTime(row["Date"]),
                        EntryGlobalID = row["EntryGlobalID"]?.ToString() ?? "",
                        GlobalID     = row["GlobalID"]?.ToString() ?? "",
                        branch       = row["name"]?.ToString() ?? "",
                        month        = Convert.ToInt32(row["month"]),
                        year         = Convert.ToInt32(row["year"]),
                        Notes        = row["Notes"]?.ToString() ?? "",
                    });
                }

                conn.Close();
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ في تحميل البيانات:\n{ex.Message}",
                                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
                conn.Close();
            }
        }

        public void LoadDataToGridview(ResevedRow selectedItem)
        {
            try
            {
                // P7-002 fix: الفتح من التقرير عبر محمل النافذة نفسها بعد Show —
                // كان المسار يضبط الهويات قبل Show فيمحوها Window_Loaded/CLR،
                // ويحقن DataView غريباً فوق مصدر الحفظ الداخلي (_salarySource)
                // فتعرض الشاشة بيانات لا يراها محرك الحفظ ولا الطباعة.
                // النمط الآن كتوأمه OpenSalaryReserved: Show ثم Navigate.
                var frmReseved = new FrmReseved();
                frmReseved.Show();
                frmReseved.Navigate(
                    "SELECT SR.id, SR.Date, SR.EntryGlobalID, SR.GlobalID, " +
                    "SR.month, SR.year, SR.Notes " +
                    "FROM Salary_Res SR " +
                    $"WHERE SR.IS_Deleted=0 AND SR.GlobalId=N'{selectedItem.GlobalID}'");
                frmReseved.Activate();
                this.Hide();
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        public void PreviewResevd(ResevedRow item)
            => LoadDataToGridview(item);

        #endregion

        #region Button Events

        private void btnSearch_Click(object sender, RoutedEventArgs e)
        {
            cond = "";

            if (chkall.IsChecked != true)
            {
                string d1 = txtStartDate.DateTime.ToShortDateString();
                string d2 = txtEndDate.DateTime.ToShortDateString();
                cond = $"AND Date>=N'{d1}' AND Date<=N'{d2}'";
            }

            LoadData(cond);
        }

        private void btnClose_Click(object sender, RoutedEventArgs e)
            => Close();

        private void btnviewres_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button btn && btn.Tag is ResevedRow item)
            {
                PreviewResevd(item);
            }
        }

        #endregion

        #region CheckBox Events

        private void chkall_CheckedChanged(object sender, RoutedEventArgs e)
        {
            bool isAll = chkall.IsChecked == true;
            txtStartDate.IsEnabled = !isAll;
            txtEndDate.IsEnabled   = !isAll;
        }

        #endregion
    }
}