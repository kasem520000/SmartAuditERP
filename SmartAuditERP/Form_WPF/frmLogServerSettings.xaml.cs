using DevExpress.Xpf.Core;
using System;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using KeyEventArgs = System.Windows.Input.KeyEventArgs;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmLogServerSettings : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;

        public int  operNo    { get; set; }
        public bool Iscorrect { get; set; } = false;
        public int  CheckType { get; set; } = 1;
        public bool isfirst   { get; set; } = true;
        public bool AllowChar { get; set; } = false;
        public bool Secured   { get; set; } = false;

        #endregion

        #region Constructor

        public frmLogServerSettings()
        {
            conn = MainClass.ConnObj();
            InitializeComponent();
        }

        #endregion

        #region Check

        private void Check()
        {
            try
            {
                string passwordText = txtPass.Password;
                string usernameText = txtUser.Text.Trim();

                if (string.IsNullOrEmpty(passwordText))
                {
                    DXMessageBox.Show("يرجى إدخال كلمة المرور", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                // FIX P1-008: أزيلت بيانات الدخول الثابتة (auditor/auditor)؛
                // تُقرأ كلمة المرور الآن من AdminGates.json (المفتاح LogServer)
                // وعند غيابها تُرفض العملية (fail-closed).
                string expected = SecureConfig.ReadValue("AdminGates.json", "LogServer");

                if (!string.IsNullOrEmpty(expected) &&
                    string.Equals(passwordText, expected, StringComparison.Ordinal))
                {
                    Iscorrect = true;
                    Close();
                }
                else if (string.IsNullOrEmpty(expected))
                {
                    DXMessageBox.Show(
                        "هذه العملية غير مفعلة: لم يتم ضبط كلمة مرور البوابة الإدارية.\n" +
                        "راجع ملف AdminGates.json بجوار البرنامج (المفتاح LogServer).",
                        "غير مفعلة", MessageBoxButton.OK, MessageBoxImage.Stop);
                }
                else
                {
                    DXMessageBox.Show("ليس لديك صلاحية، أو أن كلمة المرور المدخلة غير صحيحة", "",
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

        #region Events

        private void txtPass_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
                Check();
        }

        private void btnLogIn_Click(object sender, RoutedEventArgs e)
        {
            Check();
        }

        #endregion
    }
}