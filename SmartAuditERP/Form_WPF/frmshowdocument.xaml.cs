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

        // Repair R-027 (audit findings P2-013/P2-016): every attachment writer copies files into
        // Settings.DocsRootPath and stores that destination as FileUrl, so the canonical root is
        // recoverable here by construction. Open/delete now accept ONLY paths confined under it;
        // anything else (a doctored row, traversal, a UNC outside the store) is refused before any
        // process start or file delete. Full reparse-point resolution and an extension allowlist
        // remain documented owner-input (attachment-store policy), not invented here.
        private static bool TryResolveDocsRoot(out string root)
        {
            root = null;
            try
            {
                string configured = Properties.Settings.Default.DocsRootPath;
                if (string.IsNullOrWhiteSpace(configured)) return false;
                root = System.IO.Path.GetFullPath(configured);
                return true;
            }
            catch { return false; }
        }

        private static bool IsConfinedToStore(string fileUrl)
        {
            if (string.IsNullOrWhiteSpace(fileUrl)) return false;
            if (!TryResolveDocsRoot(out string root)) return false;   // fail closed
            try
            {
                string full = System.IO.Path.GetFullPath(fileUrl);
                string prefix = root.EndsWith(System.IO.Path.DirectorySeparatorChar.ToString())
                    ? root
                    : root + System.IO.Path.DirectorySeparatorChar;
                return full.StartsWith(prefix, StringComparison.OrdinalIgnoreCase);
            }
            catch { return false; }
        }

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
        /// </summary>
        public void AddDocument(int rowNo, string fileName, string fileUrl)
        {
            _documents.Add(new DocumentItem
            {
                RowNo    = rowNo,
                FileName = fileName,
                FileUrl  = fileUrl
            });
        }

        #endregion

        #region DataGrid Events

        private void DataGridView1_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (DataGridView1.SelectedItem is DocumentItem doc)
            {
                // R-027 (P2-016): never hand a DB-supplied path to the shell outside the store.
                if (!IsConfinedToStore(doc.FileUrl))
                {
                    DXMessageBox.Show("مسار المرفق خارج مخزن المستندات المعتمد ولن يُفتح.", "تنبيه",
                                    MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (File.Exists(doc.FileUrl))
                {
                    Process.Start(new ProcessStartInfo(doc.FileUrl) { UseShellExecute = true });
                    // R-027 (P2-013): keep the parent context alive - opening one attachment must
                    // not silently disarm subsequent operations on the same document (the old code
                    // blanked type/GlobalIdDoc here, so a later delete targeted an empty key).
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

                try
                {
                    // حذف من قاعدة البيانات
                    if (conn.State != System.Data.ConnectionState.Open)
                        conn.Open();

                    // R-027 (P2-013): the old statement deleted EVERY attachment row of the parent
                    // document while removing only one file - wiping sibling metadata on any first
                    // delete. Narrow to exactly this row: by its own Id when the caller supplied it
                    // (Documents.Id), otherwise by exact stored path. Siblings survive intact.
                    string sql = doc.DocId >= 0
                        ? "DELETE FROM Documents WHERE globalId=@GlobalId AND type=@type AND Id=@id"
                        : "DELETE FROM Documents WHERE globalId=@GlobalId AND type=@type AND FileUrl=@url";
                    var cmd = new SqlCommand(sql, conn);
                    cmd.Parameters.AddWithValue("@GlobalId", GlobalIdDoc);
                    cmd.Parameters.AddWithValue("@type",     type);
                    if (doc.DocId >= 0)
                        cmd.Parameters.Add("@id", SqlDbType.Int).Value = doc.DocId;
                    else
                        cmd.Parameters.AddWithValue("@url", doc.FileUrl ?? (object)DBNull.Value);
                    cmd.ExecuteNonQuery();

                    // حذف الملف من القرص - R-027 (P2-016): only inside the confined store root.
                    if (IsConfinedToStore(doc.FileUrl) && File.Exists(doc.FileUrl))
                        File.Delete(doc.FileUrl);

                    // إزالة من القائمة المعروضة فعلياً: المتصلون قد يستبدلون ItemsSource بمجموعتهم
                    // الخاصة، فكانت إزالة _documents الداخلية لا تحرك الصف الظاهر إطلاقاً.
                    var source = DataGridView1.ItemsSource as System.Collections.IList;
                    if (source != null && source.Contains(doc))
                        source.Remove(doc);
                    else
                        _documents.Remove(doc);

                    // إعادة ترقيم الصفوف
                    int n = 1;
                    foreach (var d in _documents)
                        d.RowNo = n++;
                    if (source != null && !ReferenceEquals(source, _documents))
                    {
                        n = 1;
                        foreach (var o in source)
                            if (o is DocumentItem di) di.RowNo = n++;
                    }

                    DXMessageBox.Show("تم الحذف بنجاح", "تم",
                                    MessageBoxButton.OK, MessageBoxImage.Information);

                    // R-027 (P2-013): do not blank the parent context after a delete; further rows
                    // of the same document stay deletable with a correct key until the window closes
                    // (fresh per-instance state is guaranteed by callers constructing a new window).
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

        #region Closing

        protected override void OnClosing(System.ComponentModel.CancelEventArgs e)
        {
            base.OnClosing(e);
            if (conn.State != System.Data.ConnectionState.Closed)
                conn.Close();
        }

        #endregion
    }

    /// <summary>نموذج صف جدول المستندات</summary>
    public class DocumentItem : System.ComponentModel.INotifyPropertyChanged
    {
        private int _rowNo;
        public int    RowNo    { get => _rowNo; set { _rowNo = value; OnPropertyChanged(nameof(RowNo)); } }
        public string FileName { get; set; }
        public string FileUrl  { get; set; }

        // R-027 (P2-013): Documents.Id of this row when the caller can supply it (-1 = unknown).
        // Deletion prefers the exact Id and falls back to an exact FileUrl predicate otherwise.
        public int DocId { get; set; } = -1;

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string name) =>
            PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(name));
    }
}