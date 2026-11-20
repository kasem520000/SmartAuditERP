using DevExpress.Xpf.Core;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using Button = System.Windows.Controls.Button;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmRequirementPM : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection _conn;
        private SqlConnection _conn1;

        private bool   _priceIncVAT = false;
        private double _defVAT      = 0;
        private int    _code        = -1;
        private bool _saveOutcomeUnknown;
        private int    _procType    = 1;
        private int    _restrNo     = -1;

        private ObservableCollection<TermRow>   _termsSource  = new ObservableCollection<TermRow>();
        private ObservableCollection<SearchRow> _searchSource = new ObservableCollection<SearchRow>();

        private DataTable _termsTable = new DataTable();

        #endregion

        #region Constructor

        public frmRequirementPM()
        {
            InitializeComponent();
            _conn  = MainClass.ConnObj();
            _conn1 = MainClass.ConnObj();
            dgvterms.ItemsSource = _termsSource;
            dgvSrch.ItemsSource  = _searchSource;
        }

        #endregion

        #region Window Events

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                LoadRequirementNo();
                LoadCountries();
                LoadCites();
                LoadTerms();
                txtToDate.DateTime   = DateTime.Now;
                txtFromDate.DateTime = DateTime.Now;
                txtDate.DateTime     = DateTime.Now;
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
            }
        }

        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _conn?.Close();
            _conn1?.Close();
        }

        #endregion

        #region CLR

        private void CLR()
        {
            _termsSource.Clear();
            _searchSource.Clear();
            _code = -1;

            LoadRequirementNo();

            cmbCities.SelectedIndex  = -1;
            cmbCountry.SelectedIndex = -1;
            txtLocation.Text   = "";
            txtPopulation.Text = "";
            txtTotPrice.Text   = "0";

            txtToDate.DateTime   = DateTime.Now;
            txtFromDate.DateTime = DateTime.Now;
            txtDate.DateTime     = DateTime.Now;
        }

        #endregion

        #region Load Data

        private void LoadRequirementNo()
        {
            try
            {
                EnsureOpen(_conn);
                using (var cmd = new SqlCommand(
                    "SELECT MAX(RequirNo) FROM PM_Requirement", _conn))
                {
                    object r = cmd.ExecuteScalar();
                    int next = (r != DBNull.Value) ? Convert.ToInt32(r) + 1 : 1;
                    txtNo.Text = next.ToString();
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
            }
            finally { CloseConn(_conn); }
        }

        public void LoadCountries()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    "SELECT id, name FROM Countries ORDER BY id", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    cmbCountry.ItemsSource       = dt.DefaultView;
                    cmbCountry.DisplayMemberPath = "name";
                    cmbCountry.SelectedValuePath = "id";
                    cmbCountry.SelectedIndex     = -1;
                }
            }
            catch { }
        }

        public void LoadCites()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    "SELECT id, name FROM Cities ORDER BY id", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    cmbCities.ItemsSource       = dt.DefaultView;
                    cmbCities.DisplayMemberPath = "name";
                    cmbCities.SelectedValuePath = "id";
                    cmbCities.SelectedIndex     = -1;
                }
            }
            catch { }
        }

        public void LoadTerms()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    "SELECT Code, name FROM PM_Terms " +
                    "WHERE IS_Deleted=0 AND Type=2 ORDER BY Code", _conn))
                {
                    _termsTable = new DataTable();
                    da.Fill(_termsTable);

                    // ربط ComboBox في عمود البند
                    var termCol = dgvterms.Columns[0] as DataGridComboBoxColumn;
                    if (termCol != null)
                    {
                        termCol.ItemsSource       = _termsTable.DefaultView;
                        termCol.DisplayMemberPath = "name";
                        termCol.SelectedValuePath = "Code";
                    }
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
            }
        }

        #endregion

        #region Search

        private void btnSearch_Click(object sender, RoutedEventArgs e)
        {
            Search();
        }

        private void Search()
        {
            try
            {
                _searchSource.Clear();
                string cond = "";

                int? searchNumber = null;
                if (!string.IsNullOrWhiteSpace(txtSrchNo.Text))
                {
                    if (!int.TryParse(txtSrchNo.Text.Trim(), out int parsed) || parsed <= 0)
                    {
                        DXMessageBox.Show("رقم طلب الاحتياج غير صالح.", "تنبيه",
                            MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }
                    searchNumber = parsed;
                    cond += "PM_Requirement.RequirNo=@requirementNumber AND ";
                }
                else
                    cond += " PM_Requirement.RequirNo IS NOT NULL AND ";

                using (var da = new SqlDataAdapter(
                    $"SELECT PM_Requirement.RequirNo, Countries.name AS country, " +
                    $"PM_Requirement.RegsDate AS vDate " +
                    $"FROM PM_Requirement LEFT JOIN Countries ON PM_Requirement.Country=Countries.id " +
                    $"WHERE PM_Requirement.IS_Deleted=0 AND {cond} 1=1 ORDER BY RequirNo DESC",
                    _conn))
                {
                    if (searchNumber.HasValue)
                        da.SelectCommand.Parameters.Add("@requirementNumber", SqlDbType.Int).Value = searchNumber.Value;
                    var dt = new DataTable();
                    da.Fill(dt);

                    foreach (DataRow row in dt.Rows)
                    {
                        _searchSource.Add(new SearchRow
                        {
                            id         = Convert.ToInt32(row["RequirNo"]),
                            requireNo  = row["RequirNo"].ToString(),
                            country    = row["country"].ToString(),
                            vDate      = Convert.ToDateTime(row["vDate"]).ToShortDateString()
                        });
                    }
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
            }
        }

        private void dgvSrch_MouseDoubleClick(object sender, MouseButtonEventArgs e)
        {
            if (dgvSrch.SelectedItem is SearchRow row)
            {
                Navigate($"SELECT * FROM PM_Requirement WHERE RequirNo={row.id}");
                TabControl1.SelectedIndex = 0;
            }
        }

        #endregion

        #region Navigation

        private void Navigate(string sqlQuery)
        {
            try
            {
                EnsureOpen(_conn);
                using (var adapter = new SqlDataAdapter(sqlQuery, _conn))
                {
                    var headers = new DataTable();
                    adapter.Fill(headers);
                    if (headers.Rows.Count == 0) { CLR(); return; }
                    if (headers.Rows.Count != 1)
                        throw new InvalidOperationException("رقم طلب الاحتياج غير فريد.");
                    ReadData(headers.Rows[0]);
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
            }
            finally { CloseConn(_conn); }
        }

        // Support the shipped table (no IsDeleted) without resurrecting rows on
        // installations that do have the optional soft-delete column. Refuse if
        // metadata is not visible instead of assuming the column is absent.
        public static DataTable LoadRequirementLines(SqlConnection connection, int requirementNumber)
        {
            if (requirementNumber <= 0) throw new ArgumentOutOfRangeException(nameof(requirementNumber));
            bool opened = connection.State != ConnectionState.Open;
            if (opened) connection.Open();
            try
            {
                int schemaState;
                using (var meta = new SqlCommand(
                    "SELECT CASE WHEN OBJECT_ID(N'dbo.PM_RequirementSub',N'U') IS NULL THEN -1 " +
                    "WHEN ISNULL(HAS_PERMS_BY_NAME(N'dbo.PM_RequirementSub', N'OBJECT', N'VIEW DEFINITION'),0)=0 THEN -2 " +
                    "WHEN COL_LENGTH(N'dbo.PM_RequirementSub',N'IsDeleted') IS NULL THEN 0 ELSE 1 END", connection))
                    schemaState = Convert.ToInt32(meta.ExecuteScalar());
                if (schemaState < 0)
                    throw new InvalidOperationException("تعذر التحقق من مخطط بنود الاحتياج وصلاحية قراءته.");

                string sql = "SELECT TermPk,Quntity,price,status,Reff_No FROM dbo.PM_RequirementSub " +
                    "WHERE RequirNo=@requirement" + (schemaState == 1 ? " AND IsDeleted=0" : "");
                using (var adapter = new SqlDataAdapter(sql, connection))
                {
                    adapter.SelectCommand.Parameters.Add("@requirement", SqlDbType.Int).Value = requirementNumber;
                    var lines = new DataTable();
                    adapter.Fill(lines);
                    return lines;
                }
            }
            finally { if (opened) connection.Close(); }
        }

        private void ReadData(DataRow header)
        {
            int code = Convert.ToInt32(header["RequirNo"]);
            var lines = LoadRequirementLines(_conn, code);
            var staged = new System.Collections.Generic.List<TermRow>();
            foreach (DataRow row in lines.Rows)
            {
                double qty = Convert.ToDouble(row["Quntity"]);
                double price = Convert.ToDouble(row["price"]);
                staged.Add(new TermRow
                {
                    TermCode = Convert.ToInt32(row["TermPk"]),
                    Qty = qty,
                    Price = price,
                    Total = qty * price,
                    Status = Convert.ToBoolean(row["status"]),
                    RefNo = Convert.ToDouble(row["Reff_No"])
                });
            }

            // No reader is open while CLR obtains the next number and closes the
            // connection. A failed line load leaves the prior form untouched.
            CLR();
            _code = code;
            txtNo.Text = _code.ToString();
            if (DateTime.TryParse(header["Regsdate"].ToString(), out DateTime d))
                txtDate.DateTime = d;
            try { cmbCities.SelectedValue = Convert.ToDouble(header["City"]); } catch { }
            try { cmbCountry.SelectedValue = header["Country"]; } catch { }
            txtLocation.Text = header["Address"].ToString();
            txtPopulation.Text = header["Population"].ToString();
            foreach (var row in staged) _termsSource.Add(row);
            CalcTotal();
        }

        private void btnFirst_Click(object sender, RoutedEventArgs e)
            => Navigate("SELECT TOP 1 * FROM PM_Requirement WHERE IS_Deleted=0 ORDER BY RequirNo ASC");
        private void btnPrevious_Click(object sender, RoutedEventArgs e)
            => Navigate($"SELECT TOP 1 * FROM PM_Requirement WHERE IS_Deleted=0 AND RequirNo<{_code} ORDER BY RequirNo DESC");
        private void btnNext_Click(object sender, RoutedEventArgs e)
            => Navigate($"SELECT TOP 1 * FROM PM_Requirement WHERE IS_Deleted=0 AND RequirNo>{_code} ORDER BY RequirNo ASC");
        private void btnLast_Click(object sender, RoutedEventArgs e)
            => Navigate("SELECT TOP 1 * FROM PM_Requirement WHERE IS_Deleted=0 ORDER BY RequirNo DESC");

        #endregion

        #region Calculation

        private void CalcTotal()
        {
            try
            {
                double total = 0;
                foreach (var row in _termsSource)
                    total += row.Qty * row.Price;
                txtTotPrice.Text = $"{total:N2}";
            }
            catch { }
        }

        #endregion

        #region DataGrid Events

        private void DeleteTermRow_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button btn && btn.Tag is TermRow row)
            {
                var answer = DXMessageBox.Show("هل تريد حذف البند؟",
                    "", MessageBoxButton.YesNo, MessageBoxImage.Question);
                if (answer == MessageBoxResult.Yes)
                {
                    _termsSource.Remove(row);
                    CalcTotal();
                }
            }
        }

        #endregion

        #region Action Buttons

        private void btnNew_Click(object sender, RoutedEventArgs e) => CLR();
        private void btnClose_Click(object sender, RoutedEventArgs e) => this.Close();
        private void btnPrint_Click(object sender, RoutedEventArgs e) { }

        private void btnDelete_Click(object sender, RoutedEventArgs e) { }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            if (_saveOutcomeUnknown)
            {
                DXMessageBox.Show("تعذر تأكيد نتيجة الحفظ؛ راجع قاعدة البيانات قبل إعادة المحاولة.",
                    "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            if (_code != -1)
            {
                DXMessageBox.Show("تعديل طلب الاحتياج المحفوظ غير متاح؛ لم يتم حفظ التغييرات.",
                    "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            SqlTransaction transaction = null;
            bool commitAttempted = false, committed = false;
            try
            {
                if (_termsSource.Count == 0)
                {
                    DXMessageBox.Show("يجب استكمال بيانات البند",
                        "", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (!int.TryParse(txtNo.Text, out int reqNo) || reqNo <= 0)
                {
                    DXMessageBox.Show("رقم طلب الاحتياج غير صالح.", "تنبيه",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }
                foreach (var row in _termsSource)
                {
                    // Both fields are INT in the shipped schema. Never silently
                    // round or overflow an edited quantity or reference number.
                    if (!IsExactSqlInt(row.Qty) || !IsExactSqlInt(row.RefNo) ||
                        double.IsNaN(row.Price) || double.IsInfinity(row.Price))
                    {
                        DXMessageBox.Show("تحقق من الكمية والمرجع والسعر؛ الكمية والمرجع يجب أن يكونا عددين صحيحين.",
                            "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }
                }
                EnsureOpen(_conn);
                EnsureOpen(_conn1);
                transaction = _conn.BeginTransaction();

                if (MainClass.IsTrial && _code == -1)
                {
                    using (var da = new SqlDataAdapter("SELECT id FROM Entry", _conn1))
                    {
                        var dt = new DataTable();
                        da.Fill(dt);
                        if (dt.Rows.Count >= 20)
                        {
                            DXMessageBox.Show("نأسف لقد وصلت لأقصى حد إدخال للنسخة التجريبية.",
                                "", MessageBoxButton.OK, MessageBoxImage.Information);
                            return;
                        }
                    }
                }

                if (_code == -1)
                {
                    using (var cmd = new SqlCommand(
                        "INSERT INTO PM_Requirement(RequirNo,Country,City,Address,Population,RegsDate,IS_Deleted) " +
                        "VALUES(@RequirNo,@Country,@City,@Address,@Population,@RegsDate,@IS_Deleted)",
                        _conn, transaction))
                    {
                        cmd.Parameters.Add("@RequirNo",   SqlDbType.Int).Value      = reqNo;
                        cmd.Parameters.Add("@Country",    SqlDbType.Int).Value      = cmbCountry.SelectedValue ?? DBNull.Value;
                        cmd.Parameters.Add("@City",       SqlDbType.Int).Value      = cmbCities.SelectedValue  ?? DBNull.Value;
                        cmd.Parameters.Add("@Address",    SqlDbType.NVarChar).Value = txtLocation.Text;
                        cmd.Parameters.Add("@Population", SqlDbType.Decimal).Value  = double.TryParse(txtPopulation.Text, out double pop) ? pop : 0;
                        cmd.Parameters.Add("@RegsDate",   SqlDbType.DateTime).Value = txtDate.DateTime;
                        cmd.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value      = 0;
                        cmd.ExecuteNonQuery();
                    }

                    // إدراج البنود
                    foreach (var row in _termsSource)
                    {
                        using (var subCmd = new SqlCommand(
                            "INSERT INTO PM_RequirementSub(RequirNo,TermPk,Quntity,price,status,Reff_No) " +
                            "VALUES(@RequirNo,@TermPk,@Quntity,@price,@status,@Reff_No)",
                            _conn, transaction))
                        {
                            subCmd.Parameters.Add("@RequirNo", SqlDbType.Int).Value      = reqNo;
                            subCmd.Parameters.Add("@TermPK",   SqlDbType.Int).Value      = row.TermCode;
                            subCmd.Parameters.Add("@Quntity",  SqlDbType.Int).Value      = (int)row.Qty;
                            subCmd.Parameters.Add("@price",    SqlDbType.Float).Value    = row.Price;
                            subCmd.Parameters.Add("@Reff_No",  SqlDbType.Int).Value      = (int)row.RefNo;
                            subCmd.Parameters.Add("@status",   SqlDbType.Bit).Value      = row.Status;
                            subCmd.ExecuteNonQuery();
                        }
                    }
                }

                commitAttempted = true;
                transaction.Commit();
                committed = true;
                _code = reqNo;

                var savedMsg = new frmSavedMsg();
                savedMsg.ShowDialog();

                if (savedMsg.Pressed == 1)
                    CLR();
                else if (savedMsg.Pressed == 3)
                {
                    CLR();
                    this.Close();
                }
            }
            catch (Exception ex)
            {
                if (commitAttempted && !committed) _saveOutcomeUnknown = true;
                string msg = committed ? "تم الحفظ، لكن حدث خطأ بعده: " + ex.Message
                    : _saveOutcomeUnknown ? "تعذر تأكيد نتيجة الحفظ؛ راجع قاعدة البيانات: " + ex.Message
                    : "خطأ أثناء الحفظ: " + ex.Message;
                DXMessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                if (transaction != null && !committed)
                {
                    try { transaction.Rollback(); }
                    catch
                    {
                        _saveOutcomeUnknown = true;
                        DXMessageBox.Show("تعذر تأكيد التراجع؛ راجع قاعدة البيانات قبل إعادة المحاولة.",
                            "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                    }
                }
                CloseConn(_conn);
                CloseConn(_conn1);
            }
        }

        private static bool IsExactSqlInt(double value)
        {
            return !double.IsNaN(value) && !double.IsInfinity(value) &&
                value >= int.MinValue && value <= int.MaxValue && Math.Truncate(value) == value;
        }

        private void btnAddCountry_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                new frmCountries().ShowDialog();
                LoadCountries();
            }
            catch { }
        }

        private void btnAddCity_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                new frmCities().ShowDialog();
                LoadCites();
            }
            catch { }
        }

        private void btnAddContract_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_code <= 0 || _termsSource.Count == 0)
                {
                    DXMessageBox.Show("افتح طلب احتياج محفوظاً ذا بنود أولاً.", "تنبيه",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }
                if (DXMessageBox.Show("سيتم تحميل البنود المحفوظة فقط، وليس تعديلات الشاشة غير المحفوظة. هل تتابع؟",
                    "تنبيه", MessageBoxButton.YesNo, MessageBoxImage.Question) != MessageBoxResult.Yes)
                    return;
                var frm = new frmContractPM();
                try
                {
                    frm.Show();
                    frm.LoadRequirements(_code);
                    frm.Activate();
                }
                catch
                {
                    frm.Close();
                    throw;
                }
            }
            catch (Exception ex)
            {
                DXMessageBox.Show("تعذر تحميل بنود الاحتياج: " + ex.Message, "خطأ",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region Helpers

        private void EnsureOpen(SqlConnection conn)
        {
            if (conn.State != ConnectionState.Open) conn.Open();
        }

        private void CloseConn(SqlConnection conn)
        {
            if (conn.State != ConnectionState.Closed) conn.Close();
        }

        #endregion

        #region Models

        public class TermRow : INotifyPropertyChanged
        {
            private double _qty;
            private double _price;
            private double _total;

            public int    TermCode { get; set; }
            public double Qty
            {
                get => _qty;
                set { _qty = value; _total = _qty * _price; OnPropertyChanged(nameof(Qty)); OnPropertyChanged(nameof(Total)); }
            }
            public double Price
            {
                get => _price;
                set { _price = value; _total = _qty * _price; OnPropertyChanged(nameof(Price)); OnPropertyChanged(nameof(Total)); }
            }
            public double Total
            {
                get => _total;
                set { _total = value; OnPropertyChanged(nameof(Total)); }
            }
            public double RefNo    { get; set; }
            public bool   Status   { get; set; }

            public event PropertyChangedEventHandler PropertyChanged;
            protected void OnPropertyChanged(string name)
                => PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }

        public class SearchRow
        {
            public int    id        { get; set; }
            public string requireNo { get; set; }
            public string country   { get; set; }
            public string vDate     { get; set; }
        }

        #endregion
    }
}