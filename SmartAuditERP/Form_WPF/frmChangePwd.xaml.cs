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
                // P1-010 fix: كلمة المرور لا تُعرض نصاً في الواجهة أبداً — الاسم فقط.
                // P1-011 fix: استعلام بارامترات.
                SqlDataAdapter adapter = new SqlDataAdapter(
                    "SELECT username FROM users WHERE emp = @emp",
                    conn);
                adapter.SelectCommand.Parameters.Add("@emp", SqlDbType.Int).Value = MainClass.UserID;

                DataTable dataTable = new DataTable();
                adapter.Fill(dataTable);

                if (dataTable.Rows.Count > 0)
                {
                    txtUser.Text = dataTable.Rows[0]["username"]?.ToString() ?? string.Empty;
                }
                txtPass.Password = ""; // حقل إدخال لكلمة جديدة — لا يُملأ من القاعدة
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

                // P1-011 fix: تحديث بارامترات — لا حشر نص في SQL.
                // P1-010 fix: تُخزن تجزئة PBKDF2 في pwd_hash ويُصفّر عمود النص القديم.
                string newHash = Class.Security.PasswordHasher.Hash(txtPass.Password);

                if (conn.State != ConnectionState.Open)
                    conn.Open();

                using (var cmd = new SqlCommand(
                    "UPDATE Users SET pwd_hash = @hash, pwd = N'' " +
                    "WHERE emp = @emp",
                    conn))
                {
                    cmd.Parameters.Add("@hash", SqlDbType.NVarChar, 512).Value = newHash;
                    cmd.Parameters.Add("@emp", SqlDbType.Int).Value = MainClass.UserID;
                    cmd.ExecuteNonQuery();
                }

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