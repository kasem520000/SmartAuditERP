using DevExpress.Xpf.Core;
using System;
using System.Data;
using System.Data.SqlClient;
using System.Windows;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmInvRptType : DevExpress.Xpf.Core.ThemedWindow
    {
        // ══════════════════════════════════════════════════════════
        #region Private Fields

        private readonly SqlConnection _conn;

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Constructor

        public frmInvRptType()
        {
            InitializeComponent();

            _conn = MainClass.ConnObj();

            // P7-103 fix: استرجاع القيمة المحفوظة عند الفتح — كان الحوار
            // يبدأ دائماً على A4 ولا يعرض ما حُفظ سابقاً
            Loaded += FrmInvRptType_Loaded;
        }

        #endregion

        #region Window Events

        private void FrmInvRptType_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_conn.State != ConnectionState.Open)
                    _conn.Open();

                using var cmd = new SqlCommand(
                    "SELECT val FROM sett WHERE id=1", _conn);
                object saved = cmd.ExecuteScalar();

                if (saved != null && saved != DBNull.Value
                    && Convert.ToInt32(saved) == 2)
                    RadioButton2.IsChecked = true;
                else
                    RadioButton1.IsChecked = true;
            }
            catch
            {
                /* بلا سجل محفوظ يبقى الافتراضي A4 كما كان */
            }
            finally
            {
                if (_conn.State == ConnectionState.Open)
                    _conn.Close();
            }
        }

        #endregion

        // ══════════════════════════════════════════════════════════
        #region Button Events

        private void Button2_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void Button1_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_conn.State != ConnectionState.Open)
                    _conn.Open();

                int printTypeVal = RadioButton2.IsChecked == true ? 2 : 1;

                // P7-104 fix: حفظ محقَّق — كان يعلن النجاح دون فحص الصف
                // المتأثر (صف sett id=1 غير موجود أصلاً في قاعدة نظيفة
                // = نجاح كاذب بلا أي كتابة). الآن upsert: تحديث، وإن لم
                // يُوجد الصف يُدرج، والمعاملة معلمة
                int affected;
                using (var cmd = new SqlCommand(
                    "UPDATE sett SET val=@val WHERE id=1", _conn))
                {
                    cmd.Parameters.Add("@val", SqlDbType.Int).Value = printTypeVal;
                    affected = cmd.ExecuteNonQuery();
                }

                if (affected == 0)
                {
                    using var ins = new SqlCommand(
                        "INSERT INTO sett(id, val) VALUES(1, @val)", _conn);
                    ins.Parameters.Add("@val", SqlDbType.Int).Value = printTypeVal;
                    ins.ExecuteNonQuery();
                }

                DXMessageBox.Show(
                    "تم الحفظ بنجاح ✅",
                    "حفظ",
                    MessageBoxButton.OK,
                    MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(
                    $"خطأ في الحفظ:\n{ex.Message}",
                    "خطأ",
                    MessageBoxButton.OK,
                    MessageBoxImage.Error);
            }
            finally
            {
                if (_conn.State == ConnectionState.Open)
                    _conn.Close();
            }
        }

        #endregion
    }
}