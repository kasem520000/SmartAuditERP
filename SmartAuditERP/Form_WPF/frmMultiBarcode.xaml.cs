using DevExpress.Xpf.Core;
using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Button = System.Windows.Controls.Button;
using KeyEventArgs = System.Windows.Input.KeyEventArgs;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmMultiBarcode : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;
        private ObservableCollection<BarcodeRow> _rows;

        #endregion

        #region Constructor

        public frmMultiBarcode()
        {
            conn  = MainClass.ConnObj();
            _rows = new ObservableCollection<BarcodeRow>();
            InitializeComponent();
        }

        #endregion

        #region Load

        private void frmMultiBarcode_Load(object sender, RoutedEventArgs e)
        {
            dgvData.ItemsSource = _rows;
            txtBarcode.Focus();
        }

        #endregion

        #region Load DG

        public void LoadDG()
        {
            try
            {
                _rows.Clear();

                double itemId = 0;
                double.TryParse(txtNo.Text, out itemId);

                SqlDataAdapter adapter = new SqlDataAdapter(
                    $"select * from Itembarcodes where ItemId={(int)itemId}", conn);
                DataTable dt = new DataTable();
                adapter.Fill(dt);

                foreach (DataRow row in dt.Rows)
                {
                    _rows.Add(new BarcodeRow { Barcode = row["barcode"].ToString() });
                }
            }
            catch (Exception ex)
            {
                ShowError(ex);
            }
        }

        #endregion

        #region Validate Barcode

        private bool IsValidBarcode(string barcode)
        {
            if (string.IsNullOrEmpty(barcode)) return false;

            double itemId = 0;
            double.TryParse(txtNo.Text, out itemId);

            // Repair R-004 (audit finding P7-036): the previous check combined the two
            // tables with a comma cross join ("from ItemUnits,Itembarcodes") -- a CARTESIAN
            // product filtered by an OR. When either table is empty, the product is empty,
            // so a barcode duplicated in the OTHER table was never detected. Check each
            // table independently with UNION ALL so a match in either one is found even if
            // the other table has no rows. Existence (Rows.Count > 0) semantics preserved.
            // Incidental local hardening of this same statement: bind the user-supplied
            // barcode and the item id as parameters instead of interpolating them into the
            // SQL text (does NOT claim to resolve the broad injection family P1-011).
            SqlDataAdapter adapter = new SqlDataAdapter(
                "select ItemId from ItemUnits where barcode=@barcode and ItemId<>@itemId " +
                "union all " +
                "select ItemId from Itembarcodes where barcode=@barcode and ItemId<>@itemId",
                conn);
            adapter.SelectCommand.Parameters.Add(
                "@barcode", SqlDbType.NVarChar).Value = barcode ?? "";
            adapter.SelectCommand.Parameters.Add(
                "@itemId", SqlDbType.Int).Value = (int)itemId;
            DataTable dt = new DataTable();
            adapter.Fill(dt);

            if (dt.Rows.Count > 0)
            {
                string msg = string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                    ? "الباركود تم إدخاله مسبقًا"
                    : "Barcode is previously inserted";

                DXMessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return false;
            }
            return true;
        }

        #endregion

        #region Save

        private void Button1_Click(object sender, RoutedEventArgs e)
        {
            SaveBarcode();
        }

        private void txtBarcode_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
                SaveBarcode();
        }

        private void SaveBarcode()
        {
            try
            {
                if (string.IsNullOrWhiteSpace(txtBarcode.Text))
                {
                    string msg = string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                        ? "ادخل الباركود" : "Enter barcode";
                    DXMessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Warning);
                    txtBarcode.Focus();
                    return;
                }

                if (!IsValidBarcode(txtBarcode.Text))
                {
                    txtBarcode.Focus();
                    return;
                }

                if (conn.State != System.Data.ConnectionState.Open)
                    conn.Open();

                double itemId = 0;
                double.TryParse(txtNo.Text, out itemId);

                SqlCommand cmd = new SqlCommand(
                    "insert into Itembarcodes(ItemId,barcode) values(@ItemId,@barcode)", conn);
                cmd.Parameters.Add("@ItemId",  SqlDbType.Int).Value      = (int)itemId;
                cmd.Parameters.Add("@barcode", SqlDbType.NVarChar).Value = txtBarcode.Text;
                cmd.ExecuteNonQuery();

                txtBarcode.Text = "";
                txtBarcode.Focus();
                LoadDG();

                string successMsg = string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                    ? "تم الحفظ" : "Saved";
                DXMessageBox.Show(successMsg, "", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                string errMsg = string.Equals(MainClass.Language, "en", StringComparison.OrdinalIgnoreCase)
                    ? "error in saving" + Environment.NewLine + "error details: " + ex.Message
                    : "خطأ أثناء الحفظ" + Environment.NewLine + "تفاصيل الخطأ: " + ex.Message;

                DXMessageBox.Show(errMsg, "", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                if (conn.State != System.Data.ConnectionState.Closed)
                    conn.Close();
            }
        }

        #endregion

        #region Delete

        private void btnDelete_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                Button btn = sender as Button;
                if (btn == null) return;

                BarcodeRow row = btn.Tag as BarcodeRow;
                if (row == null) return;

                if (conn.State != System.Data.ConnectionState.Open)
                    conn.Open();

                double itemId = 0;
                double.TryParse(txtNo.Text, out itemId);

                new SqlCommand(
                    $"delete from Itembarcodes where ItemId={(int)itemId} and barcode='{row.Barcode}'",
                    conn).ExecuteNonQuery();

                txtBarcode.Focus();
                LoadDG();

                string successMsg = string.Equals(MainClass.Language, "ar", StringComparison.OrdinalIgnoreCase)
                    ? "تم الحذف" : "Deleted";
                DXMessageBox.Show(successMsg, "", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                string errMsg = string.Equals(MainClass.Language, "en", StringComparison.OrdinalIgnoreCase)
                    ? "error in deleting" + Environment.NewLine + "error details: " + ex.Message
                    : "خطأ أثناء الحذف" + Environment.NewLine + "تفاصيل الخطأ: " + ex.Message;

                DXMessageBox.Show(errMsg, "", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                if (conn.State != System.Data.ConnectionState.Closed)
                    conn.Close();
            }
        }

        #endregion

        #region Helpers

        private void ShowError(Exception ex)
        {
            DXMessageBox.Show("خطأ" + Environment.NewLine + ex.Message,
                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion
    }

    public class BarcodeRow
    {
        public string Barcode { get; set; }
    }
}