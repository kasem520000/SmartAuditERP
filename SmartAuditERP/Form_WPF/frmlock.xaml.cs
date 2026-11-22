using DevExpress.Xpf.Core;
using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using KeyEventArgs = System.Windows.Input.KeyEventArgs;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmlock : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;

        public int    operNo    { get; set; }
        public bool   Iscorrect { get; set; } = false;
        public bool   isfirst   { get; set; } = true;
        public bool   AllowChar { get; set; } = false;
        public bool   Secured   { get; set; } = false;
        public bool   is_close  { get; set; } = false;

        private string _calcFunc   = "";
        private bool   _hasDecimal = false;
        private double _valHolder1 = 0.0;
        private double _valHolder2 = 0.0;

        #endregion

        #region Constructor

        public frmlock()
        {
            conn = MainClass.ConnObj();
            InitializeComponent();
        }

        #endregion

        #region Load

        private void Frm_Calculator_Load(object sender, RoutedEventArgs e)
        {
            txtPass.Focus();
        }

        #endregion

        #region Password Field

        private void txtPass_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
                Check();
        }

        private string GetPassword()
        {
            return txtPass.Password;
        }

        private void AppendToPassword(string digit)
        {
            txtPass.Password += digit;
        }

        #endregion

        #region Check

        private void Check()
        {
            try
            {
                string passwordText = GetPassword();

                if (string.IsNullOrEmpty(passwordText))
                {
                    DXMessageBox.Show("يرجى إدخال كلمة المرور", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                double numericCode = 0;
                double.TryParse(passwordText, out numericCode);

                // P1-011 fix: كلا الاستعلامين بارامترات — لا حشر نص في SQL.
                // P1-010 fix: التحقق من كلمة المرور عبر التجزئة (pwd_hash) أولاً
                // ثم النص القديم مع مهاجرة فورية إلى التجزئة.
                SqlDataAdapter adapterSecure = new SqlDataAdapter(
                    "select * from Users where emp=@emp and SecureCode=@code and LoginSecode=1",
                    conn);
                adapterSecure.SelectCommand.Parameters.Add("@emp", SqlDbType.Int).Value = MainClass.UserID;
                adapterSecure.SelectCommand.Parameters.Add("@code", SqlDbType.Int).Value = (int)numericCode;
                DataTable dtSecure = new DataTable();
                adapterSecure.Fill(dtSecure);

                bool unlocked = dtSecure.Rows.Count == 1;

                if (!unlocked)
                {
                    SqlDataAdapter adapterPwd = new SqlDataAdapter(
                        "select id, pwd, pwd_hash from Users where emp=@emp",
                        conn);
                    adapterPwd.SelectCommand.Parameters.Add("@emp", SqlDbType.Int).Value = MainClass.UserID;
                    DataTable dtPwd = new DataTable();
                    adapterPwd.Fill(dtPwd);

                    foreach (DataRow r in dtPwd.Rows)
                    {
                        string storedHash = r["pwd_hash"] as string;
                        if (!string.IsNullOrEmpty(storedHash) &&
                            Class.Security.PasswordHasher.Verify(passwordText, storedHash))
                        {
                            unlocked = true;
                            break;
                        }
                    }

                    if (!unlocked)
                    {
                        foreach (DataRow r in dtPwd.Rows)
                        {
                            string legacyPwd = r["pwd"] as string;
                            if (!string.IsNullOrEmpty(legacyPwd) &&
                                string.Equals(passwordText, legacyPwd, StringComparison.Ordinal))
                            {
                                // مهاجرة لمرة واحدة: خزّن التجزئة وصفّر النص
                                try
                                {
                                    string hash = Class.Security.PasswordHasher.Hash(legacyPwd);
                                    using (var upd = new SqlCommand(
                                        "UPDATE Users SET pwd_hash=@hash, pwd=N'' WHERE id=@id",
                                        conn))
                                    {
                                        upd.Parameters.Add("@hash", SqlDbType.NVarChar, 512).Value = hash;
                                        upd.Parameters.Add("@id", SqlDbType.Int).Value = Convert.ToInt32(r["id"]);
                                        if (conn.State != ConnectionState.Open) conn.Open();
                                        upd.ExecuteNonQuery();
                                    }
                                }
                                catch { /* فشل المهاجرة لا يمنع فتح القفل */ }
                                unlocked = true;
                                break;
                            }
                        }
                    }
                }

                if (unlocked)
                {
                    Iscorrect = true;
                    Close();
                }
                else
                {
                    DXMessageBox.Show("كلمة المرور المدخلة غير صحيحة", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show("خطأ Error details: " + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region Buttons

        private void btnUnlock_Click(object sender, RoutedEventArgs e)
        {
            Check();
        }

        private void cmd0_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("0");
        }

        private void cmd135_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("1");
        }

        private void cmd2_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("2");
        }

        private void cmd3_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("3");
        }

        private void cmd4_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("4");
        }

        private void cmd5_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("5");
        }

        private void cmd6_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("6");
        }

        private void cmd7_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("7");
        }

        private void cmd8_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("8");
        }

        private void cmd9_Click(object sender, RoutedEventArgs e)
        {
            AppendDigit("9");
        }

        private void AppendDigit(string digit)
        {
            if (isfirst)
            {
                txtPass.Clear();
                isfirst = false;
            }
            AppendToPassword(digit);
            txtPass.Focus();
        }

        private void cmdClearAll_Click(object sender, RoutedEventArgs e)
        {
            txtPass.Clear();
            _valHolder1  = 0.0;
            _valHolder2  = 0.0;
            _calcFunc    = "";
            _hasDecimal  = false;
            isfirst      = true;
            txtPass.Focus();
        }

        #endregion

        #region Advanced Login

        private void LinkLabel1_LinkClicked(object sender, MouseButtonEventArgs e)
        {
            try
            {
                // P2-002 fix: «الدخول المتقدم» لا يُخفي نافذة القفل إلا إذا تم
                // دخول كامل ناجح فعلاً — نكشف ذلك بتغير MainClass.LoginDate
                // (يُضبط عند كل دخول ناجح في frmUserLogin.Login).
                // الإلغاء يعيد المستخدم إلى شاشة القفل نفسها، لا إلى التطبيق.
                var beforeLogin = MainClass.LoginDate;
                var frmUserLogin = new frmUserLogin();
                Topmost = false;
                frmUserLogin.ShowDialog();

                if (MainClass.LoginDate != beforeLogin)
                {
                    Iscorrect = true; // دخول كامل ناجح عبر المسار المتقدم
                    Hide();
                }
            }
            catch { }
        }

        #endregion

        #region Window Events

        private void Frm_Calculator_Click(object sender, MouseButtonEventArgs e)
        {
            txtPass.Focus();
        }

        private void Frm_Calculator_KeyDown(object sender, KeyEventArgs e)
        {
            txtPass.Focus();
        }

        #endregion
    }
}