using DevExpress.Xpf.Core;
using System;
using System.Collections.Generic;
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
        private readonly string _connectionString;
        private ObservableCollection<UserLogRow> LogList;
        private long _requestGeneration;
        private bool _isClosed;
        #endregion

        #region Constructor
        public frmrptUsersRecords()
        {
            InitializeComponent();
            conn    = MainClass.ConnObj();
            // Capture before the connection is opened, while its authentication
            // details are still available to independently created connections.
            _connectionString = conn.ConnectionString;
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
        // R-138 (P7-107): only the latest request for the current filter may publish.
        private void InvalidateResults()
        {
            _requestGeneration++;
            LogList?.Clear();
        }

        protected override void OnClosed(EventArgs e)
        {
            _isClosed = true;
            InvalidateResults();
            base.OnClosed(e);
        }

        private async void ShowResults()
        {
            long request = ++_requestGeneration;
            LogList.Clear();
            try
            {
                int? employeeId = null;
                if (chkAll.IsChecked != true)
                {
                    if (cmbUsers.SelectedIndex < 0 ||
                        !int.TryParse(cmbUsers.SelectedValue?.ToString(), out int selectedId))
                    {
                        DXMessageBox.Show("يرجى اختيار مستخدم.", "تنبيه",
                                          MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }
                    employeeId = selectedId;
                }

                // Each request owns its connection and results; MainClass.ConnObj
                // mutates global state, so do not call it from the worker.
                var dt = await Task.Run(() =>
                {
                    using (var requestConnection = new SqlConnection(_connectionString))
                    using (var command = requestConnection.CreateCommand())
                    {
                        command.CommandText =
                            "SELECT Log4NetLog.Id, Log4NetLog.LogDate, Logger, Message, " +
                            "Employees.name AS EmpName FROM Log4NetLog " +
                            "LEFT JOIN Employees ON Log4NetLog.EmpID=Employees.id" +
                            (employeeId.HasValue ? " WHERE Log4NetLog.EmpId=@EmpId" : "");
                        if (employeeId.HasValue)
                            command.Parameters.Add("@EmpId", SqlDbType.Int).Value = employeeId.Value;
                        using (var adapter = new SqlDataAdapter(command))
                        {
                            var table = new DataTable();
                            adapter.Fill(table);
                            return table;
                        }
                    }
                });
                if (_isClosed || request != _requestGeneration) return;

                var rows = new List<UserLogRow>();
                foreach (DataRow row in dt.Rows)
                {
                    rows.Add(new UserLogRow
                    {
                        Id      = Convert.ToInt32(row["Id"]),
                        LogDate = Convert.ToDateTime(row["LogDate"]),
                        Logger  = row["Logger"]?.ToString() ?? "",
                        Message = row["Message"]?.ToString() ?? "",
                        EmpName = row["EmpName"]?.ToString() ?? "",
                    });
                }
                foreach (var row in rows) LogList.Add(row);
            }
            catch (Exception ex)
            {
                if (_isClosed || request != _requestGeneration) return;
                LogList.Clear();
                DXMessageBox.Show($"خطأ:\n{ex.Message}", "خطأ",
                                  MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }
        #endregion

        #region CheckBox Events
        private void chkAll_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            InvalidateResults();
            cmbUsers.IsEnabled = chkAll.IsChecked != true;
            if (chkAll.IsChecked == true)
                cmbUsers.SelectedIndex = -1;
        }

        private void cmbUsers_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (IsLoaded) InvalidateResults();
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

                // Repair R-083 (audit finding P7-048): the message cell was wrapped in quotes by
                // hand while the others were bare, and no quote inside any cell was doubled, so a
                // logged message holding a quote or a comma broke the record. The shared writer
                // quotes by rule instead.
                var export = SpreadsheetExport.Begin(path, SpreadsheetExport.CsvDelimiter);
                export.Header("م", "التاريخ", "الجهاز", "العملية", "المستخدم");

                foreach (var item in LogList)
                {
                    export.Row(SpreadsheetExport.Text(item.Id),
                               $"{item.LogDate:MM/d/yyyy hh:mm tt}",
                               SpreadsheetExport.Text(item.Logger),
                               SpreadsheetExport.Text(item.Message),
                               SpreadsheetExport.Text(item.EmpName));
                }

                export.Save();

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