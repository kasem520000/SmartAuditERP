using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Input;
using SmartAuditERP.Form_WPF;
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

                    // FIX P1-008: أزيلت كلمات المرور الثابتة المكتوبة في الكود
                    // (auditor / auditor2021 / 2020AUDITOR / DARH2024 / auditorzatca)
                    // وتُقرأ الآن من ملف AdminGates.json بجوار ملف التنفيذ،
                    // وعند غيابها تُرفض العملية (fail-closed).
                    case 0:
                    case 100:
                    case 200:
                    case 300:
                    case 400:
                        ValidateConfiguredGatePassword(enteredPassword, "Gate" + CheckType);
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

        private void CheckDatabasePassword(string enteredPassword)
        {
            // FIX P1-011: استبدال الإدراج النصي بمعاملات SQL لمنع الحقن
            SqlDataAdapter adapter = new SqlDataAdapter(
                "SELECT id, lastChanged FROM OperationPermission " +
                "WHERE IS_Deleted = 0 " +
                "AND pwd = @pwd " +
                "AND OperNo = @OperNo",
                conn);
            adapter.SelectCommand.Parameters.Add("@pwd", SqlDbType.NVarChar).Value = enteredPassword;
            adapter.SelectCommand.Parameters.Add("@OperNo", SqlDbType.Int).Value = operNo;

            DataTable dataTable = new DataTable();
            adapter.Fill(dataTable);

            if (dataTable.Rows.Count == 0)
            {
                MessageBox.Show(
                    "برجاء ادخال كلمة المرور بشكل صحيح",
                    "⚠️ خطأ",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);

                txtPass.Clear();
                txtPass.Focus();
            }
            else
            {
                Iscorrect = true;
                Close();
            }
        }

        /// <summary>
        /// FIX P1-008: التحقق من كلمة مرور البوابة الإدارية من ملف AdminGates.json
        /// (مفتاح Gate0 / Gate100 / Gate200 / Gate300 / Gate400) بدل القيم الثابتة.
        /// لا يوجد ملف أو مفتاح = رفض العملية (fail-closed).
        /// </summary>
        private void ValidateConfiguredGatePassword(string enteredPassword, string gateKey)
        {
            string expected = SecureConfig.ReadValue("AdminGates.json", gateKey);

            if (string.IsNullOrEmpty(expected))
            {
                MessageBox.Show(
                    "هذه العملية غير مفعلة: لم يتم ضبط كلمة مرور البوابة الإدارية.\n" +
                    "راجع ملف AdminGates.json بجوار البرنامج (المفتاح " + gateKey + ").",
                    "غير مفعلة",
                    MessageBoxButton.OK,
                    MessageBoxImage.Stop);
                return;
            }

            if (enteredPassword == expected)
            {
                Iscorrect = true;
                Close();
            }
            else
            {
                MessageBox.Show(
                    "ليس لديك صلاحية، أو أن كلمة المرور المدخلة غير صحيحة",
                    "⚠️ خطأ",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);
            }
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