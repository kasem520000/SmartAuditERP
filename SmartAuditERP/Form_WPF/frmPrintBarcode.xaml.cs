using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Drawing.Printing;
using System.IO;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using DevExpress.Xpf.Core;
using DevExpress.XtraReports.UI;
using Button = System.Windows.Controls.Button;
using KeyEventArgs = System.Windows.Input.KeyEventArgs;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmPrintBarcode : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Model

        public class ItemDgv
        {
            public int      RowIndex      { get; set; }
            public string   ItemCode      { get; set; }
            public string   ItemName      { get; set; }
            public string   ItemBarcode   { get; set; }
            public int      ItemQty       { get; set; }
            public double   ItemSalePrice { get; set; }
            public DateTime ItemProDate   { get; set; }
            public DateTime ItemExpDate   { get; set; }
        }

        #endregion

        #region Fields

        private SqlConnection _conn;
        private string        _foundation = "";

        public List<ItemDgv> ItemList { get; set; }

        private ObservableCollection<ItemDgv> _itemsSource
            = new ObservableCollection<ItemDgv>();

        #endregion

        #region Constructor

        public frmPrintBarcode()
        {
            InitializeComponent();
            _conn    = MainClass.ConnObj();
            ItemList = new List<ItemDgv>();
            dgvItems.ItemsSource = _itemsSource;
        }

        #endregion

        #region Window Events

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            LoadPrinters();
            LoadFoundationData();
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key != Key.Return) return;

            if (txtItemBarcode.IsFocused)
            {
                if (!string.IsNullOrEmpty(txtItemBarcode.Text))
                {
                    ReadBarcode(txtItemBarcode.Text);
                    txtItemBarcode.Text = "";
                }
            }
            else if (txtItemName.IsFocused)
            {
                SearchByName();
                txtItemName.Text = "";
            }
            else if (txtItemCode.IsFocused)
            {
                SearchByCode();
                txtItemCode.Text = "";
            }
        }

        #endregion

        #region Load

        private void LoadPrinters()
        {
            foreach (string printer in PrinterSettings.InstalledPrinters)
                cmbPrinters.Items.Add(printer);
        }

        private void LoadFoundationData()
        {
            try
            {
                using (var da = new SqlDataAdapter("SELECT * FROM Foundation", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count > 0)
                        _foundation = dt.Rows[0]["nameA"].ToString();
                }
            }
            catch { }
        }

        private void UpdateGrid()
        {
            _itemsSource.Clear();
            foreach (var item in ItemList)
                _itemsSource.Add(item);
        }

        #endregion

        #region Search

        private void btnSearch_Click(object sender, RoutedEventArgs e) => AddNewItem();

        private void AddNewItem()
        {
            var srch = new frmItemsSrch();
            MainClass.ApplyPermissionToForm(srch);
            MainClass.DoApplyUserSett(srch);
            srch.sql    = "SELECT id, name, nameEN, sale_price, unit FROM Items WHERE IS_Deleted=0 ORDER BY id";
            srch.search = "SELECT id, name, nameEN, sale_price, unit FROM Items";
            srch.Itemname       = "";
            srch.txtSrchNm.Text = txtItemName.Text;
            srch.ShowDialog();

            if (srch.ISDone && srch.ItemId > 0)
            {
                for (int i = 0; i < srch.Itemlist.Count; i++)
                {
                    ItemList.Add(new ItemDgv
                    {
                        RowIndex      = ItemList.Count + 1,
                        ItemCode      = Common.GetItemCode(srch.Itemlist[i]),
                        ItemName      = Common.GetItemName(srch.Itemlist[i]),
                        ItemBarcode   = Common.GetItemBarcode(srch.Itemlist[i]),
                        ItemSalePrice = Common.GetItemPrice(srch.Itemlist[i]),
                        ItemQty       = 1,
                        ItemProDate   = DateTime.Now.Date,
                        ItemExpDate   = DateTime.Now.Date
                    });
                }
                UpdateGrid();
            }
        }

        private void SearchByName()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    $"SELECT name,id,Code,barcode,sale_price FROM Items WHERE IS_Deleted=0 AND name=N'{txtItemName.Text}'",
                    _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count > 0)
                        AddRowFromDataRow(dt.Rows[0]);
                    else
                        AddNewItem();
                }
            }
            catch { }
        }

        private void SearchByCode()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    $"SELECT name,id,Code,barcode,sale_price FROM Items WHERE IS_Deleted=0 AND Code=N'{txtItemCode.Text}'",
                    _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count > 0)
                        AddRowFromDataRow(dt.Rows[0]);
                    else
                        AddNewItem();
                }
            }
            catch { }
        }

        private void AddRowFromDataRow(DataRow row)
        {
            ItemList.Add(new ItemDgv
            {
                RowIndex      = ItemList.Count + 1,
                ItemCode      = row["Code"].ToString(),
                ItemName      = row["name"].ToString(),
                ItemBarcode   = row["barcode"].ToString(),
                ItemSalePrice = Convert.ToDouble(row["sale_price"]),
                ItemQty       = 1,
                ItemProDate   = DateTime.Now.Date,
                ItemExpDate   = DateTime.Now.Date
            });
            UpdateGrid();
        }

        private void ReadBarcode(string barcode)
        {
            try
            {
                string scanned = (barcode ?? "").Trim();
                if (scanned.Length == 0 || scanned.Length > 50)
                {
                    DXMessageBox.Show("الباركود فارغ أو أطول من الحد المسموح.");
                    return;
                }

                // Only an exact, unique unit barcode carries an unambiguous
                // unit price. Scale payloads and aliases without a unit mapping
                // must not be printed with the item header price by guesswork.
                using (var cmd = new SqlCommand(
                    "SELECT I.id, I.code, I.name, U.unit, U.sale " +
                    "FROM ItemUnits U INNER JOIN Items I ON I.id=U.ItemId " +
                    "WHERE I.IS_Deleted=0 AND U.barcode=@barcode", _conn))
                {
                    cmd.Parameters.Add("@barcode", SqlDbType.NVarChar, 50).Value = scanned;
                    var dt = new DataTable();
                    using (var da = new SqlDataAdapter(cmd)) da.Fill(dt);
                    if (dt.Rows.Count != 1 || dt.Rows[0]["unit"] == DBNull.Value ||
                        Convert.ToInt32(dt.Rows[0]["unit"]) <= 0 || dt.Rows[0]["sale"] == DBNull.Value)
                    {
                        DXMessageBox.Show("تعذر تحديد وحدة وسعر وحيدين لهذا الباركود؛ لا يمكن إنشاء الملصق.");
                        return;
                    }
                    double price = Convert.ToDouble(dt.Rows[0]["sale"]);
                    if (double.IsNaN(price) || double.IsInfinity(price))
                    {
                        DXMessageBox.Show("سعر الوحدة غير صالح لطباعة الملصق.");
                        return;
                    }
                    var item = new ItemDgv
                    {
                        RowIndex      = ItemList.Count + 1,
                        ItemCode      = dt.Rows[0]["code"].ToString(),
                        ItemName      = dt.Rows[0]["name"].ToString(),
                        ItemBarcode   = scanned,
                        ItemSalePrice = price,
                        ItemQty       = 1,
                        ItemProDate   = DateTime.Now.Date,
                        ItemExpDate   = DateTime.Now.Date
                    };
                    ItemList.Add(item);
                    txtItemCode.Text = item.ItemCode;
                    txtItemName.Text = item.ItemName;
                    txtItemBarcode.Text = scanned;
                    UpdateGrid();
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show("تعذر قراءة الباركود: " + ex.Message);
            }
        }

        #endregion

        #region Delete Row

        private void DeleteRow_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button btn && btn.Tag is ItemDgv item)
            {
                var answer = DXMessageBox.Show(
                    MainClass.Language == "en"
                        ? "Are you sure to delete?"
                        : "هل أنت متأكد من الحذف؟",
                    MainClass.Language == "en"
                        ? "Confirmation"
                        : "رسالة تأكيد",
                    MessageBoxButton.YesNo,
                    MessageBoxImage.Question);

                if (answer != MessageBoxResult.Yes) return;

                ItemList.Remove(item);

                // إعادة ترقيم
                int idx = 1;
                foreach (var i in ItemList)
                    i.RowIndex = idx++;

                UpdateGrid();
            }
        }

        #endregion

        #region Clear

        private void Clear()
        {
            ItemList.Clear();
            _itemsSource.Clear();
            txtItemBarcode.Text = "";
            txtItemCode.Text    = "";
            txtItemName.Text    = "";
        }

        #endregion

        #region Button Events

        private void BtnNew_Click(object sender, RoutedEventArgs e) => Clear();

        private void btnClose_Click(object sender, RoutedEventArgs e) => this.Close();

        private void BtnPrint_Click(object sender, RoutedEventArgs e)
        {
            if (cmbPrinters.SelectedItem == null)
            {
                DXMessageBox.Show(
                    MainClass.Language == "ar"
                        ? "يجب تحديد الطابعة"
                        : "Please select printer",
                    "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            foreach (var item in ItemList)
            {
                if (item.ItemQty > 0)
                    PrintBarcode(item);
            }
        }

        private void ChkPrintExpir_CheckedChanged(object sender, RoutedEventArgs e)
        {
            bool show = ChkPrintExpir.IsChecked == true;
            colProDate.Visibility = show ? Visibility.Visible : Visibility.Collapsed;
            colExpDate.Visibility = show ? Visibility.Visible : Visibility.Collapsed;
        }

        #endregion

        #region Print

        private DataSet BindToData(ItemDgv item)
        {
            var invoiceData = new InvoiceData
            {
                ItemName   = item.ItemName,
                ItemNo     = item.ItemCode,
                Price      = item.ItemSalePrice.ToString(),
                Barcode    = item.ItemBarcode,
                ProDate    = ChkPrintExpir.IsChecked == true ? item.ItemProDate.ToString() : "",
                ExpDate    = ChkPrintExpir.IsChecked == true ? item.ItemExpDate.ToString() : "",
                Foundation = _foundation
            };

            var list = new List<InvoiceData> { invoiceData };
            var ds   = new DataSet("Name");
            var dt   = global::UtilitiesProj.Common.ToDataTable(list);
            ds.Tables.Add(dt);
            return ds;
        }

        private void PrintBarcode(ItemDgv item)
        {
            string reportsPath = MainClass.ReportsPath;
            string reportFile  = Path.Combine(reportsPath, "Barcode.repx");

            if (!Directory.Exists(reportsPath) || !File.Exists(reportFile))
            {
                DXMessageBox.Show("مسار التقارير غير موجود أو تم تعديله",
                    "خطأ", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            var report = XtraReport.FromFile(reportFile);
            report.DataSource  = BindToData(item);
            report.PrinterName = cmbPrinters.SelectedItem.ToString();

            if (item.ItemQty == 0)
            {
                DXMessageBox.Show("يجب تحديد كمية الطباعة",
                    "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            for (int i = 0; i < item.ItemQty; i++)
                report.Print();
        }

        #endregion
    }
}