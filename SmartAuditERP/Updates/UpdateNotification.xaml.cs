// Form_WPF/UpdateNotification.xaml.cs
using SmartAuditERP.Models;
using System.Windows;

namespace SmartAuditERP.Form_WPF
{
    public partial class UpdateNotification
        : DevExpress.Xpf.Core.ThemedWindow
    {
        public bool UserAccepted { get; private set; } = false;

        public UpdateNotification(AppUpdateInfo info)
        {
            InitializeComponent();

            // ✅ تعبئة البيانات بعد InitializeComponent مباشرة
            if (info == null) return;

            txtVersionInfo.Text =
                $"الإصدار الحالي: {MainClass.CurrentVersion}  ←  " +
                $"الإصدار الجديد: {info.NewVersion}";

            txtReleaseTitle.Text = !string.IsNullOrEmpty(info.ReleaseTitle)
                ? info.ReleaseTitle
                : $"الإصدار {info.NewVersion}";

            txtReleaseNotes.Text = !string.IsNullOrEmpty(info.ReleaseNotes)
                ? info.ReleaseNotes
                : "لا توجد ملاحظات";

            txtReleaseDate.Text = !string.IsNullOrEmpty(info.ReleaseDate)
                ? info.ReleaseDate
                : "غير محدد";

            txtFileName.Text = !string.IsNullOrEmpty(info.FileName)
                ? info.FileName
                : "غير محدد";

            txtFileSize.Text = info.FileSize > 0
                ? FormatFileSize(info.FileSize)
                : "غير محدد";
        }

        private static string FormatFileSize(long bytes)
        {
            if (bytes >= 1_073_741_824)
                return $"{bytes / 1_073_741_824.0:F2} GB";
            if (bytes >= 1_048_576)
                return $"{bytes / 1_048_576.0:F1} MB";
            if (bytes >= 1_024)
                return $"{bytes / 1_024.0:F0} KB";
            return $"{bytes} bytes";
        }

        private void BtnUpdate_Click(object sender, RoutedEventArgs e)
        {
            UserAccepted = true;
            Close();
        }

        private void BtnLater_Click(object sender, RoutedEventArgs e)
        {
            UserAccepted = false;
            Close();
        }
    }
}