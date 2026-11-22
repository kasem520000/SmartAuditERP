using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Diagnostics;
using System.IO;
using System.Windows;
using System.Windows.Input;
using DevExpress.Xpf.Core;

namespace SmartAuditERP.Form_WPF
{
    public partial class Frmshowdocument : ThemedWindow
    {
        #region Fields

        public int    type      { get; set; } = 0;
        public string GlobalIdDoc { get; set; } = "";

        private SqlConnection conn;
        private ObservableCollection<DocumentItem> _documents;

        // P2-016 fix: قائمة أنواع مسموح بها للفتح/الحذف — أي نوع آخر من
        // قاعدة البيانات يُرفض صريحًا (لا exe ولا سكربتات ولا مجهول).
        private static readonly string[] AllowedDocExtensions =
        {
            ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".bmp",
            ".tif", ".tiff", ".webp", ".doc", ".docx", ".xls",
            ".xlsx", ".ppt", ".pptx", ".txt", ".csv"
        };

        #endregion

        #region Constructor

        public Frmshowdocument()
        {
            InitializeComponent();

            conn       = new SqlConnection(MainClass.connstr);
            _documents = new ObservableCollection<DocumentItem>();
            DataGridView1.ItemsSource = _documents;
        }

        #endregion

        #region Public Method to Add Rows

        /// <summary>
        /// إضافة صف مستند من الخارج (بدلاً من DataGridView1.Rows.Add)
        /// P2-013/P2-014 fix: docId هو معرف صف Documents الفعلي —
        /// بدونه لا يمكن حذف المرفق المحدد بدقة.
        /// </summary>
        public void AddDocument(int docId, int rowNo, string fileName, string fileUrl)
        {
            _documents.Add(new DocumentItem
            {
                DocId    = docId,
                RowNo    = rowNo,
                FileName = fileName,
                FileUrl  = fileUrl
            });
        }

        #endregion

        #region P2-016 fix: Attachment Path Guard

        /// <summary>
        /// مسار المرفق من قاعدة البيانات لا يُفتح ولا يُحذف إلا إذا كان:
        ///  ١) داخل مجلد المرفقات المعتمد (DocsRootPath) بعد التسوية الكاملة
        ///     للمسار — لا اجتياز مسار خارج الجذر بأي شكل (.. أو مطلق آخر)
        ///  ٢) بامتداد ضمن القائمة المسموحة
        /// أي شك = رفض صريح برسالة (fail-closed).
        /// </summary>
        private static bool IsSanctionedAttachmentPath(string fileUrl, out string reason)
        {
            reason = "";

            if (string.IsNullOrWhiteSpace(fileUrl))
            {
                reason = "مسار المرفق فارغ";
                return false;
            }

            string root;
            try
            {
                root = Properties.Settings.Default.DocsRootPath ?? "";
            }
            catch
            {
                root = "";
            }

            if (string.IsNullOrWhiteSpace(root))
            {
                reason = "مجلد المرفقات المعتمد غير مهيأ (DocsRootPath)";
                return false;
            }

            string fullRoot;
            string fullPath;
            try
            {
                fullRoot = Path.GetFullPath(root).TrimEnd(
                    Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)
                    + Path.DirectorySeparatorChar;
                fullPath = Path.GetFullPath(fileUrl);
            }
            catch
            {
                reason = "مسار المرفق غير صالح";
                return false;
            }

            if (!fullPath.StartsWith(fullRoot, StringComparison.OrdinalIgnoreCase))
            {
                reason = "المرفق خارج مجلد المرفقات المعتمد";
                return false;
            }

            string ext = Path.GetExtension(fullPath)?.ToLowerInvariant() ?? "";
            if (Array.IndexOf(AllowedDocExtensions, ext) < 0)
            {
                reason = "نوع المرفق غير مسموح: " + (string.IsNullOrEmpty(ext) ? "(بلا امتداد)" : ext);
                return false;
            }

            return true;
        }

        #endregion

        #region DataGrid Events

        private void DataGridView1_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (DataGridView1.SelectedItem is DocumentItem doc)
            {
                // P2-016 fix: الفتح من مسار القاعدة يخضع لحارس المسار/النوع.
                if (!IsSanctionedAttachmentPath(doc.FileUrl, out string openReason))
                {
                    DXMessageBox.Show("رُفض فتح المرفق: " + openReason, "المدقق",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (File.Exists(doc.FileUrl))
                {
                    Process.Start(new ProcessStartInfo(doc.FileUrl) { UseShellExecute = true });
                    type       = 0;
                    GlobalIdDoc = "";
                }
                else
                {
                    DXMessageBox.Show("لا يوجد وثائق.", "تنبيه",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                }
            }
        }

        private void BtnDeleteDoc_Click(object sender, RoutedEventArgs e)
        {
            if (sender is System.Windows.Controls.Button btn
                && btn.Tag is DocumentItem doc)
            {
                var confirm = DXMessageBox.Show("هل أنت متأكد من الحذف؟", "المدقق",
                                              MessageBoxButton.YesNo, MessageBoxImage.Question);
                if (confirm != MessageBoxResult.Yes) return;

                // P2-013 fix: كان الحذف يمسح سجلات كل مرفقات المستند
                // (WHERE globalId+type) — الآن يستهدف صف المرفق المحدد
                // بمعرفه الفعلي مع بقاء globalId+type كتحصين إضافي.
                if (doc.DocId <= 0)
                {
                    DXMessageBox.Show(
                        "تعذر تحديد المرفق المحدد بدقة (لا معرف صف) — لا يُحذف شيء.",
                        "المدقق", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                // P2-016 fix: حذف الملف من القرص يخضع لحارس المسار/النوع.
                if (!IsSanctionedAttachmentPath(doc.FileUrl, out string deleteReason))
                {
                    DXMessageBox.Show("رُفض حذف ملف المرفق: " + deleteReason, "المدقق",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                try
                {
                    // حذف من قاعدة البيانات — الصف المحدد حصراً
                    if (conn.State != System.Data.ConnectionState.Open)
                        conn.Open();

                    var cmd = new SqlCommand(
                        "DELETE FROM Documents WHERE Id=@Id AND globalId=@GlobalId AND type=@type",
                        conn);
                    cmd.Parameters.AddWithValue("@Id",       doc.DocId);
                    cmd.Parameters.AddWithValue("@GlobalId", GlobalIdDoc);
                    cmd.Parameters.AddWithValue("@type",     type);
                    int deleted = cmd.ExecuteNonQuery();

                    if (deleted == 0)
                    {
                        DXMessageBox.Show("لم يُعثر على سجل المرفق المحدد — لا يُحذف شيء.",
                            "المدقق", MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }

                    // حذف الملف من القرص (بعد نجاح حذف السجل)
                    if (File.Exists(doc.FileUrl))
                        File.Delete(doc.FileUrl);

                    // إزالة من القائمة
                    _documents.Remove(doc);

                    // إعادة ترقيم الصفوف
                    int n = 1;
                    foreach (var d in _documents)
                        d.RowNo = n++;

                    DXMessageBox.Show("تم الحذف بنجاح", "تم",
                                    MessageBoxButton.OK, MessageBoxImage.Information);

                    type        = 0;
                    GlobalIdDoc = "";
                }
                catch (Exception ex)
                {
                    DXMessageBox.Show("خطأ في الحذف: " + ex.Message, "خطأ",
                                    MessageBoxButton.OK, MessageBoxImage.Error);
                }
                finally
                {
                    if (conn.State != System.Data.ConnectionState.Closed)
                        conn.Close();
                }
            }
        }

        #endregion
    }

    public class DocumentItem : System.ComponentModel.INotifyPropertyChanged
    {
        private int _rowNo;
        private int _docId;

        /// <summary>P2-013/P2-014 fix: معرف صف Documents الفعلي (Id) —
        /// يُستخدم للحذف الدقيق بدل مسح كل مرفقات المستند.</summary>
        public int DocId   { get => _docId; set { _docId = value; OnPropertyChanged(nameof(DocId)); } }
        public int RowNo    { get => _rowNo; set { _rowNo = value; OnPropertyChanged(nameof(RowNo)); } }
        public string FileName { get; set; }
        public string FileUrl  { get; set; }

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(name));
    }
}
