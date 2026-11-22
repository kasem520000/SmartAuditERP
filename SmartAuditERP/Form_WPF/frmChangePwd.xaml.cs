using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Input;
using SmartAuditERP.Form_WPF;
using MessageBox = System.Windows.MessageBox;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmChangePwd : Window
    {
        #region ── Fields ─────────────────────────────────────

        private SqlConnection conn;

        #endregion

        #region ── Constructor ────────────────────────────────

        public frmChangePwd()
        {
            InitializeComponent();
            conn = MainClass.ConnObj();
        }

        #endregion

        #region ── Window Events ──────────────────────────────

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            LoadUserData();
        }

        private void Header_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
                DragMove();
        }

        #endregion

        #region ── Data Loading ───────────────────────────────

        private void LoadUserData()
        {
            try
            {
                SqlDataAdapter adapter = new SqlDataAdapter(
                    $"SELECT username, pwd FROM users WHERE emp = {MainClass.UserID}",
                    conn);

                DataTable dataTable = new DataTable();
                adapter.Fill(dataTable);

                if (dataTable.Rows.Count > 0)
                {
                    txtUser.Text = dataTable.Rows[0]["username"]?.ToString() ?? string.Empty;
                    txtPass.Password = dataTable.Rows[0]["pwd"]?.ToString() ?? string.Empty;
                }
            }
            catch
            {
            }
        }

        #endregion

        #region ── Button Events ──────────────────────────────

        private void btnClose_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(txtPass.Password))
                {
                    MessageBox.Show("ادخل كلمة المرور",
                        "⚠️ تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                    txtPass.Focus();
                    return;
                }

                if (conn.State != ConnectionState.Open)
                    conn.Open();

                // FIX P1-011: استبدال الإدراج النصي بكلمة المرور داخل SQL
                // بمعاملات لمنع حقن SQL عبر حقل كلمة المرور.
                var updateCmd = new SqlCommand(
                    "UPDATE Users SET pwd = @pwd WHERE emp = @emp",
                    conn);
                updateCmd.Parameters.Add("@pwd", SqlDbType.NVarChar).Value = txtPass.Password;
                updateCmd.Parameters.Add("@emp", SqlDbType.Int).Value = MainClass.UserID;
                updateCmd.ExecuteNonQuery();

                MessageBox.Show("تم الحفظ بنجاح ✅",
                    "نجاح", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "خطأ أثناء الحفظ" + Environment.NewLine + "تفاصيل الخطأ: " + ex.Message,
                    "❌ خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                if (conn.State != ConnectionState.Closed)
                    conn.Close();
            }
        }

        #endregion
    }
}