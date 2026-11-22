using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Input;
using SmartAuditERP.Class.Security;
using KeyEventArgs = System.Windows.Input.KeyEventArgs;
using MessageBox = System.Windows.MessageBox;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmCheckPwd : Window
    {
        #region ── Public Fields ──────────────────────────────

        public int operNo { get; set; } = 0;
        public bool Iscorrect { get; set; } = false;
        public int CheckType { get; set; } = 1;
        public bool isfirst { get; set; } = true;
        public bool AllowChar { get; set; } = false;
        public bool Secured { get; set; } = false;

        #endregion

        #region ── Private Fields ─────────────────────────────

        private SqlConnection conn;
        private string _calcFunc = string.Empty;
        private bool _hasDecimal = false;
        private double _valHolder1 = 0.0;
        private double _valHolder2 = 0.0;

        #endregion

        #region ── Constructor ────────────────────────────────

        public frmCheckPwd()
        {
            InitializeComponent();
            conn = MainClass.ConnObj();
        }

        #endregion

        #region ── Window Events ──────────────────────────────

        private void Header_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
                DragMove();
        }

        private void txtPass_PreviewKeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return || e.Key == Key.Enter)
            {
                CheckPassword();
                e.Handled = true;
            }
        }

        #endregion

        #region ── Password Check ─────────────────────────────

        // P1-008 fix: كلمات البوابات الإدارية لا تُخزن نصاً في المصدر ولا تُقارن نصاً.
        // تُخزن تجزئات PBKDF2 فقط، وتُقارن عبر PasswordHasher.Verify (زمن-ثابت).
        // أول من يتحقق: تجزئة مخصصة للتثبيت من قاعدة البيانات (تمكّن تغييرها لكل موقع)،
        // ثم تجزئة المصنع الافتراضية.
        // ملاحظة نشر موثقة في REPAIR-LOG-STAGE1: كلمات المصنع أصبحت علنية تاريخياً،
        // فعلى كل تثبيت حساس تعيين كلمة بوابته الخاصة (جدول OperationPermission، عمود pwd_hash).
        private static readonly System.Collections.Generic.Dictionary<int, string> GatePasswordHashes =
            new System.Collections.Generic.Dictionary<int, string>
            {
                { 0,   "PBKDF2$100000$d6Z+r9QiurpjzYFkHYnmew==$nLEQh9ssYW56N0PoiTP+TM2hYEjMQ9QTHP8tHftteOM=" },
                { 100, "PBKDF2$100000$gxvHLCFLack4mnPwRNs8FQ==$F6Inkol75w2jaXISjEx6I1CKA6wTNw+8jxO70y8yp28=" },
                { 200, "PBKDF2$100000$ypAGVuOVyDeSevHMmMlD8g==$p9d18ZY3U4NTTyRrFy8fXxerxu4IT/xYf6GgOr795MA=" },
                { 300, "PBKDF2$100000$+zycvKH0aMMyB2u+HCshuA==$FFxXoHLPF7h1cBFeTvcTK/nTO4w6g2XkUfjW7gMvEBg=" },
                { 400, "PBKDF2$100000$nAo1ayqWdXxE38uv6DbmUA==$xOYNJR450sxmeq+KqssFXkYgsLDLkaBttyt0DJGolD4=" }
            };

        private void CheckPassword()
        {
            try
            {
                string enteredPassword = txtPass.Password;

                if (string.IsNullOrWhiteSpace(enteredPassword))
                {
                    MessageBox.Show(
                        "يرجى ادخال كلمة المرور",
                        "⚠️ تنبيه",
                        MessageBoxButton.OK,
                        MessageBoxImage.Warning);

                    txtPass.Focus();
                    return;
                }

                switch (CheckType)
                {
                    case 1:
                        CheckDatabasePassword(enteredPassword);
                        break;

                    case 0:
                    case 100:
                    case 200:
                    case 300:
                    case 400:
                        VerifyGatePassword(enteredPassword, CheckType);
                        break;

                    default:
                        MessageBox.Show(
                            "نوع التحقق غير معروف",
                            "⚠️ خطأ",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning);
                        break;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "خطأ: " + ex.Message,
                    "❌ خطأ",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error);
            }
        }

        /// <summary>
        /// P1-011 fix: الاستعلام بارامترات SqlCommand بدل حشر كلمة المرور في نص SQL.
        /// P1-008/P1-010: التحقق من pwd_hash (PBKDF2) إن وُجد، وإلا السقوط الآمن إلى النص القديم
        /// مرة واحدة فقط بهدف المهاجرة الفورية إلى التجزئة ثم تصفير النص القديم.
        /// </summary>
        private void CheckDatabasePassword(string enteredPassword)
        {
            // 1) مسار التجزئة المعتمد (العمود الجديد إن أُنشئ لهذا التثبيت)
            const string hashedQuery =
                "SELECT id, pwd_hash FROM OperationPermission " +
                "WHERE IS_Deleted = 0 AND OperNo = @operNo";

            using (SqlCommand cmd = new SqlCommand(hashedQuery, conn))
            {
                cmd.Parameters.Add("@operNo", SqlDbType.Int).Value = operNo;
                using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
                {
                    DataTable dt = new DataTable();
                    adapter.Fill(dt);
                    foreach (DataRow row in dt.Rows)
                    {
                        string storedHash = row["pwd_hash"] as string;
                        if (!string.IsNullOrEmpty(storedHash) &&
                            PasswordHasher.Verify(enteredPassword, storedHash))
                        {
                            Iscorrect = true;
                            Close();
                            return;
                        }
                    }
                }
            }

            // 2) مسار المهاجرة: النص القديم (متوافق مع التثبيتات القائمة) — يُهاجَر فور نجاحه
            const string legacyQuery =
                "SELECT id, pwd FROM OperationPermission " +
                "WHERE IS_Deleted = 0 AND OperNo = @operNo";

            using (SqlCommand cmd = new SqlCommand(legacyQuery, conn))
            {
                cmd.Parameters.Add("@operNo", SqlDbType.Int).Value = operNo;
                using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
                {
                    DataTable dt = new DataTable();
                    adapter.Fill(dt);
                    foreach (DataRow row in dt.Rows)
                    {
                        string legacyPwd = row["pwd"] as string;
                        if (!string.IsNullOrEmpty(legacyPwd) &&
                            string.Equals(enteredPassword, legacyPwd, StringComparison.Ordinal))
                        {
                            MigrateLegacyPasswordToHash(operNo, legacyPwd);
                            Iscorrect = true;
                            Close();
                            return;
                        }
                    }
                }
            }

            MessageBox.Show(
                "برجاء ادخال كلمة المرور بشكل صحيح",
                "⚠️ خطأ",
                MessageBoxButton.OK,
                MessageBoxImage.Warning);

            txtPass.Clear();
            txtPass.Focus();
        }

        /// <summary>
        /// P1-010 fix: بعد آخر دخول ناجح بالنص القديم تُخزن التجزئة ويُصفَّر النص.
        /// فشل التحديث لا يمنع الدخول (تمت المصادقة فعلاً) ويُسجل أثراً فقط.
        /// </summary>
        private void MigrateLegacyPasswordToHash(int operationNo, string legacyPassword)
        {
            try
            {
                string hash = PasswordHasher.Hash(legacyPassword);
                const string migrateSql =
                    "UPDATE OperationPermission SET pwd_hash = @hash, pwd = N'' " +
                    "WHERE IS_Deleted = 0 AND OperNo = @operNo";

                using (SqlCommand cmd = new SqlCommand(migrateSql, conn))
                {
                    cmd.Parameters.Add("@hash", SqlDbType.NVarChar, 512).Value = hash;
                    cmd.Parameters.Add("@operNo", SqlDbType.Int).Value = operationNo;
                    if (conn.State != ConnectionState.Open) conn.Open();
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Trace.WriteLine("PWD-MIGRATE failed oper=" + operationNo + ": " + ex.Message);
            }
        }

        /// <summary>
        /// P1-008 fix: البوابات الإدارية (CheckType 0/100/200/300/400) تتحقق عبر تجزئات
        /// PBKDF2 لا نصوص صريحة. أولوية التحقق: كلمة مخصصة للتثبيت من القاعدة (pwd_hash
        /// لـ OperNo المقابل) ثم تجزئة المصنع. مقارنة زمن-ثابت عبر PasswordHasher.Verify.
        /// </summary>
        private void VerifyGatePassword(string enteredPassword, int gateType)
        {
            // 1) تجاوز لكل تثبيت: إن عُيّنت pwd_hash لهذه البوابة في القاعدة فهي الحاكمة
            try
            {
                const string overrideQuery =
                    "SELECT pwd_hash FROM OperationPermission " +
                    "WHERE IS_Deleted = 0 AND OperNo = @operNo AND pwd_hash IS NOT NULL";

                using (SqlCommand cmd = new SqlCommand(overrideQuery, conn))
                {
                    cmd.Parameters.Add("@operNo", SqlDbType.Int).Value = gateType;
                    using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
                    {
                        DataTable dt = new DataTable();
                        adapter.Fill(dt);
                        foreach (DataRow row in dt.Rows)
                        {
                            string storedHash = row["pwd_hash"] as string;
                            if (!string.IsNullOrEmpty(storedHash))
                            {
                                if (PasswordHasher.Verify(enteredPassword, storedHash))
                                {
                                    Iscorrect = true;
                                    Close();
                                    return;
                                }
                                // وُجدت كلمة مخصصة ولا تطابق: البوابة مغلقة بها فقط
                                ShowGateDenied();
                                return;
                            }
                        }
                    }
                }
            }
            catch
            {
                // فشل الوصول للقاعدة: نسقط إلى تجزئة المصنع — لا نص صريح في أي مسار
            }

            // 2) تجزئة المصنع
            string factoryHash;
            if (GatePasswordHashes.TryGetValue(gateType, out factoryHash) &&
                PasswordHasher.Verify(enteredPassword, factoryHash))
            {
                Iscorrect = true;
                Close();
                return;
            }

            ShowGateDenied();
        }

        private void ShowGateDenied()
        {
            MessageBox.Show(
                "ليس لديك صلاحية، أو أن كلمة المرور المدخلة غير صحيحة",
                "⚠️ خطأ",
                MessageBoxButton.OK,
                MessageBoxImage.Warning);
        }

        #endregion

        #region ── NumPad Shared Handler ──────────────────────

        /// <summary>
        /// معالج موحد لجميع أزرار الأرقام
        /// يُربط بجميع الأزرار: cmd0 ~ cmd9 و cmd135
        /// </summary>
        private void NumPad_Click(object sender, RoutedEventArgs e)
        {
            if (sender is System.Windows.Controls.Button clickedButton)
            {
                if (isfirst)
                {
                    txtPass.Clear();
                    isfirst = false;
                }

                txtPass.Password += clickedButton.Content?.ToString() ?? string.Empty;
                txtPass.Focus();
            }
        }

        #endregion

        #region ── NumPad Individual Handlers ─────────────────
        // ملاحظة: هذه الدوال تستدعي المعالج الموحد NumPad_Click
        // وتم الإبقاء عليها للتوافق مع أي استدعاء خارجي

        private void cmd0_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd0.Content?.ToString() ?? "0");
        }

        private void cmd135_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd135.Content?.ToString() ?? "1");
        }

        private void cmd2_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd2.Content?.ToString() ?? "2");
        }

        private void cmd3_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd3.Content?.ToString() ?? "3");
        }

        private void cmd4_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd4.Content?.ToString() ?? "4");
        }

        private void cmd5_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd5.Content?.ToString() ?? "5");
        }

        private void cmd6_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd6.Content?.ToString() ?? "6");
        }

        private void cmd7_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd7.Content?.ToString() ?? "7");
        }

        private void cmd8_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd8.Content?.ToString() ?? "8");
        }

        private void cmd9_Click(object sender, RoutedEventArgs e)
        {
            AppendDigitToPassword(cmd9.Content?.ToString() ?? "9");
        }

        #endregion

        #region ── Digit Append Helper ────────────────────────

        /// <summary>
        /// إضافة رقم إلى حقل كلمة المرور
        /// </summary>
        private void AppendDigitToPassword(string digit)
        {
            if (isfirst)
            {
                txtPass.Clear();
                isfirst = false;
            }

            txtPass.Password += digit;
            txtPass.Focus();
        }

        #endregion

        #region ── Clear & Check Events ───────────────────────

        private void cmdClearAll_Click(object sender, RoutedEventArgs e)
        {
            txtPass.Clear();
            _valHolder1 = 0.0;
            _valHolder2 = 0.0;
            _calcFunc = string.Empty;
            _hasDecimal = false;
            isfirst = true;
            txtPass.Focus();
        }

        private void CheckPwd_Click(object sender, RoutedEventArgs e)
        {
            CheckPassword();
        }

        private void btnClose_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        #endregion
    }
}