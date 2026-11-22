using DevExpress.Xpf.Core;
using log4net;
using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Forms;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmLogOut : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        public int Action { get; set; } = -1;

        private static readonly ILog Logger = LogManager.GetLogger(Environment.MachineName);

        #endregion

        #region Constructor

        public frmLogOut()
        {
            InitializeComponent();
        }

        #endregion

        #region Load

        private void frmLogOut_Load(object sender, RoutedEventArgs e)
        {
            // للتوسع المستقبلي
        }

        #endregion

        #region Buttons

        private void btnLock_Click(object sender, RoutedEventArgs e)
        {
            Topmost = false;
            Action = 0;
            Hide();
        }

        private void btnOut_Click(object sender, RoutedEventArgs e)
        {
            MessageBoxResult result = DXMessageBox.Show(
                "هل أنت متأكد من تسجيل الخروج؟",
                "خروج",
                MessageBoxButton.YesNo,
                MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
                Home Home = new Home();
                Action = 1;
                Home.Close();
            }
        }

        private void btnExUser_Click(object sender, RoutedEventArgs e)
        {
            MessageBoxResult result = DXMessageBox.Show(
                "هل أنت متأكد من تبديل المستخدم؟",
                "تبديل مستخدم",
                MessageBoxButton.YesNo,
                MessageBoxImage.Question);

            if (result != MessageBoxResult.Yes) return;

            List<System.Windows.Forms.Form> formsToClose = new List<System.Windows.Forms.Form>();

            foreach (System.Windows.Forms.Form openForm in System.Windows.Forms.Application.OpenForms)
            {
                if (!string.Equals(openForm.Name, "Home", StringComparison.OrdinalIgnoreCase) &&
                    !string.Equals(openForm.Name, "frmLogOut", StringComparison.OrdinalIgnoreCase))
                {
                    formsToClose.Add(openForm);
                }
            }

            foreach (System.Windows.Forms.Form form in formsToClose)
            {
                try { form.Close(); } catch { }
            }

            // P2-003 fix: إغلاق نوافذ WPF المفتوحة من الجلسة السابقة أيضاً —
            // الكود أعلاه كان يغلق نماذج WinForms فقط فتبقى نوافذ WPF (المحررات
            // والتقارير) مفتوحة ببيانات وصلاحيات المستخدم السابق. مرجع كل نافذة
            // static في Home يُصفَّر تلقائياً عند إغلاقها (نمط P1-030) فتُنشأ
            // نسخة جديدة للجلسة الجديدة. تُستثنى Home ونافذتا الدخول/التبديل.
            var wpfWindowsToClose = new List<System.Windows.Window>();
            foreach (System.Windows.Window window in System.Windows.Application.Current.Windows)
            {
                if (window is Home || window is frmLogOut || window is frmUserLogin)
                    continue;
                wpfWindowsToClose.Add(window);
            }
            foreach (var window in wpfWindowsToClose)
            {
                try { window.Close(); } catch { }
            }

            // P2-003 fix: تصفير سياق السحابة من الجلسة السابقة — CurrentCloudUser
            // كان يبقى محملاً بعد التبديل فتستخدمه مسارات المزامنة/السحابة بهوية
            // المستخدم السابق. الدخول الجديد يعيد تعيينه عند نجاحه.
            User.CurrentCloudUser = null;

            ThreadContext.Properties["EmpID"] = MainClass.EmpNo;
            Logger.Info($"تم تسجيل الخروج للمستخدم {MainClass.UserName}");

            Action = 2;
            Hide();
        }

        #endregion
    }
}