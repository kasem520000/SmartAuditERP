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

            // Repair R-005 (audit finding P7-103): reflect the persisted print default
            // instead of always opening on the XAML default (A4).
            LoadSavedDefault();
        }

        /// <summary>
        /// Reads the saved invoice-print default from 'sett' (id = 1) and selects the
        /// matching radio button. Falls back to the XAML default (A4) if it cannot read.
        /// </summary>
        private void LoadSavedDefault()
        {
            try
            {
                if (_conn.State != ConnectionState.Open)
                    _conn.Open();

                object val = new SqlCommand(
                    "select val from sett where id = 1", _conn).ExecuteScalar();

                if (val != null && val != DBNull.Value &&
                    int.TryParse(val.ToString(), out int printType))
                {
                    bool smallPaper = (printType == 2);
                    RadioButton2.IsChecked = smallPaper;
                    RadioButton1.IsChecked = !smallPaper;
                }
            }
            catch
            {
                // Keep the XAML default (A4) when the setting cannot be loaded.
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

                // Repair R-005 (audit finding P7-104): verify the settings row was actually
                // updated instead of announcing success unconditionally. ExecuteNonQuery
                // returns the affected-row count; 0 means there is no 'sett' row with id = 1
                // to persist into, which must not be reported as a successful save. The value
                // is bound as a parameter rather than interpolated into the SQL text.
                using (SqlCommand cmd = new SqlCommand(
                    "UPDATE sett SET val = @val WHERE id = 1", _conn))
                {
                    cmd.Parameters.Add("@val", SqlDbType.Int).Value = printTypeVal;
                    int affected = cmd.ExecuteNonQuery();

                    if (affected > 0)
                    {
                        DXMessageBox.Show(
                            "تم الحفظ بنجاح ✅",
                            "حفظ",
                            MessageBoxButton.OK,
                            MessageBoxImage.Information);
                    }
                    else
                    {
                        DXMessageBox.Show(
                            "لم يتم الحفظ: لا يوجد صف إعداد قابل للتحديث (id=1).",
                            "حفظ",
                            MessageBoxButton.OK,
                            MessageBoxImage.Warning);
                    }
                }
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