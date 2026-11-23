using DevExpress.Xpf.Core;
using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmrptUsersRecords : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields
        private SqlConnection conn;
        private ObservableCollection<UserLogRow> LogList;

        // P7-107 fix: جيل الطلب — تمييز نتائج كل ضغطة عرض عن سابقتها
        private int _requestGeneration;
        #endregion

        #region Constructor
        public frmrptUsersRecords()
        {
            InitializeComponent();
            conn    = MainClass.ConnObj();
            LogList = new ObservableCollection<UserLogRow>();
            GridControl1.ItemsSource = LogList;
        }
        #endregion

        #region Window Loaded
        private void Window_Loaded(object sender, RoutedEventArgs e)
            => LoadEmps();
        #endregion

        #region Load Emps
        private void LoadEmps()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT id, name FROM Employees WHERE IS_Deleted=0 ORDER BY id",
                    conn);
                var dt = new DataTable();
                adapter.Fill(dt);

                cmbUsers.DisplayMemberPath = "name";
                cmbUsers.SelectedValuePath  = "id";
                cmbUsers.ItemsSource        = dt.DefaultView;
                cmbUsers.SelectedIndex      = -1;
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        #endregion

        #region ShowResults
        private async void ShowResults()
        {
            // P7-107 fix: تمييز جيل الطلب — الطلبات المتداخلة كانت تضيف
            // نتائجها إلى المجموعة المشتركة بلا تمييز، فنتائج طلب قديم
            // (أبطأ) تُضاف فوق نتائج الطلب الأحدث
            int generation = System.Threading.Interlocked.Increment(
                ref _requestGeneration);

            try
            {
                LogList.Clear();

                string condWhere = "";
                object empSelection = null;
                if (chkAll.IsChecked != true &&
                    cmbUsers.SelectedIndex != -1 &&
                    cmbUsers.SelectedValue != null)
                {
                    empSelection = cmbUsers.SelectedValue;
                    condWhere = " WHERE EmpId=@empId";
                }

                string sql =
                    "SELECT Log4NetLog.Id, Log4NetLog.LogDate, Logger, Message, " +
                    "Employees.name AS EmpName " +
                    "FROM Log4NetLog " +
                    "LEFT JOIN Employees ON Log4NetLog.EmpID=Employees.id" +
                    condWhere;

                // P7-107: اتصال مستقل لكل طلب — التحميل الخلفي لا يتقاسم
                // اتصال النافذة مع طلب متداخل (SqlConnection لا يدعم
                // العمليات المتوازية على الاتصال نفسه)
                using var requestConn = MainClass.ConnObj();
                var adapter = new SqlDataAdapter(sql, requestConn);

                if (condWhere.Length > 0)
                    adapter.SelectCommand.Parameters.AddWithValue(
                        "@empId", empSelection);

                var dt = new DataTable();

                // تحميل في خيط خلفي لتحسين الأداء
                await Task.Run(() => adapter.Fill(dt));

                // التحديث على الـ UI Thread — فقط إن كان هذا الطلب
                // هو الأحدث (P7-107)
                Dispatcher.Invoke(() =>
                {
                    if (generation != _requestGeneration) return;

                    foreach (DataRow row in dt.Rows)
                    {
                        LogList.Add(new UserLogRow
                        {
                            Id      = Convert.ToInt32(row["Id"]),
                            LogDate = Convert.ToDateTime(row["LogDate"]),
                            Logger  = row["Logger"]?.ToString() ?? "",
                            Message = row["Message"]?.ToString() ?? "",
                            EmpName = row["EmpName"]?.ToString() ?? "",
                        });
                    }
                });
            }
            catch (Exception ex)
            {
                Dispatcher.Invoke(() =>
                    DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                    MessageBoxButton.OK, MessageBoxImage.Error));
            }
        }
        #endregion

        #region CheckBox Events
        private void chkAll_CheckedChanged(object sender, RoutedEventArgs e)
        {
            cmbUsers.IsEnabled = chkAll.IsChecked != true;
            if (chkAll.IsChecked == true)
                cmbUsers.SelectedIndex = -1;
        }
        #endregion

        #region Button Events
        private void btnShow_Click(object sender, RoutedEventArgs e)
            => ShowResults();

        private void btnClose_Click(object sender, RoutedEventArgs e)
            => Close();

        private void btnExportExcel_Click(object sender, RoutedEventArgs e)
        {
            if (LogList == null || LogList.Count == 0)
            {
                DXMessageBox.Show("لا توجد بيانات للتصدير.", "تنبيه",
                                MessageBoxButton.OK, MessageBoxImage.Information);
                return;
            }

            try
            {
                string path = System.IO.Path.Combine(
                    Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
                    $"سجلات_مستخدمين_{DateTime.Now:yyyyMMdd_HHmm}.csv");

                // P7-108 fix: الكاتب يُغلق قبل فتح الملف للتطبيق الخارجي —
                // كان Process.Start داخل نطاق using var فيقرأ التطبيق ملفاً
                // غير مكتمل (المخزن المؤقت لم يُفرّغ بعد)
                using (var writer = new System.IO.StreamWriter(
                    path, false, System.Text.Encoding.UTF8))
                {
                    writer.WriteLine("م,التاريخ,الجهاز,العملية,المستخدم");

                    foreach (var item in LogList)
                    {
                        writer.WriteLine(
                            $"{item.Id}," +
                            $"{item.LogDate:MM/d/yyyy hh:mm tt}," +
                            $"{item.Logger}," +
                            $"\"{item.Message}\"," +
                            $"{item.EmpName}");
                    }
                }

                Process.Start(new ProcessStartInfo(path)
                { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        #endregion
    }
}