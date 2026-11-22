using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Threading;
using AuditorAPI.Models;
using SmartAuditERP.Form_WPF;
using Button = System.Windows.Controls.Button;
using ComboBox = System.Windows.Controls.ComboBox;
using MessageBox = System.Windows.MessageBox;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmContractPM : Window
    {
        #region Fields

        private SqlConnection _connection;
        private SqlConnection _connectionSecondary;
        private bool _priceIncludesVAT;
        private double _defaultVAT;
        private int _currentCode;
        private int _currentContrId;
        private int _processType;
        private int _restrictionNumber;
        private DispatcherTimer _clockTimer;

        // Observable collections for DataGrids
        public ObservableCollection<ContractTermRow> TermRows { get; set; }
        public ObservableCollection<ContractSearchRow> SearchRows { get; set; }
        public ObservableCollection<TermItem> TermsList { get; set; }

        #endregion

        #region Constructor

        public frmContractPM()
        {
            InitializeComponent();
            DataContext = this;

            _connection = MainClass.ConnObj();
            _connectionSecondary = MainClass.ConnObj();
            _priceIncludesVAT = false;
            _defaultVAT = 0.0;
            _currentCode = -1;
            _currentContrId = -1;
            _processType = 1;
            _restrictionNumber = -1;

            TermRows = new ObservableCollection<ContractTermRow>();
            SearchRows = new ObservableCollection<ContractSearchRow>();
            TermsList = new ObservableCollection<TermItem>();

            dgvterms.ItemsSource = TermRows;
            dgvSrch.ItemsSource = SearchRows;

            Loaded += frmContractPM_Loaded;
        }

        #endregion

        #region Window Events

        private void frmContractPM_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                LoadStocks();
                LoadCustomers();
                LoadBanks();
                LoadTerms();
                LoadContractNumber();
                LoadStatus();
                LoadSalesMen();
                LoadMainSettings();

                txtToDate.SelectedDate = DateTime.Now;
                txtFromDate.SelectedDate = DateTime.Now;
                txtDate.SelectedDate = DateTime.Now;
                txtDateStart.SelectedDate = DateTime.Now;
                txtDateFinish.SelectedDate = DateTime.Now;

                cmbType.SelectedIndex = 1;
                txtuser.Text = MainClass.UserName;

                WindowState = MainClass.Window_State;

                StartClock();
                cmbClient.Focus();
            }
            catch (Exception ex)
            {
                ShowError("خطأ أثناء التحميل", ex);
            }
        }

        #endregion

        #region Clock

        private void StartClock()
        {
            _clockTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromSeconds(1)
            };
            _clockTimer.Tick += (s, e) =>
                txtTime.Text = DateTime.Now.ToString("hh:mm tt");
            _clockTimer.Start();
        }

        #endregion

        #region Clear / Reset

        private void ClearForm()
        {
            TermRows.Clear();
            SearchRows.Clear();
            _currentCode = -1;
            _currentContrId = -1;

            LoadContractNumber();
            cmbType.SelectedIndex = 1;

            txtToDate.SelectedDate = DateTime.Now;
            txtFromDate.SelectedDate = DateTime.Now;
            txtDate.SelectedDate = DateTime.Now;
            txtDateStart.SelectedDate = DateTime.Now;
            txtDateFinish.SelectedDate = DateTime.Now;

            txtReff.Text = "";
            txtPeriod.Text = "";
            txtPayerName.Text = "";
            txtTotPrice.Text = "0";
            txtNetVal.Text = "0";
            txtNetVAT.Text = "0";
            txtSrchNo.Text = "";

            if (cmbTreasury.Items.Count > 0)
                cmbTreasury.SelectedIndex = 0;

            cmbClient.SelectedIndex = -1;
            cmbBanks.SelectedIndex = -1;
            cmbSalesMen.SelectedIndex = -1;
            cmbStatus.SelectedIndex = -1;
        }

        #endregion

        #region Data Loading

        private void LoadMainSettings()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT * FROM SettingGeneral WHERE Inv_Id=5", _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                if (dataTable.Rows.Count == 1)
                {
                    _priceIncludesVAT = Convert.ToBoolean(dataTable.Rows[0]["PriceIncVAT"]);
                    _defaultVAT = Convert.ToDouble(dataTable.Rows[0]["MainVAT"]);
                }
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل الإعدادات", ex);
            }
        }

        private void LoadContractNumber()
        {
            try
            {
                EnsureConnectionOpen(_connection);
                using var cmd = new SqlCommand(
                    "SELECT MAX(ContrNo) FROM PM_ContractInv", _connection);
                double maxNo = ParseDouble(cmd.ExecuteScalar()?.ToString() ?? "0");
                txtNo.Text = ((int)(maxNo + 1)).ToString();
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل رقم العقد", ex);
            }
            finally
            {
                EnsureConnectionClosed(_connection);
            }
        }

        public void LoadStocks()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT id, name FROM Stocks, Stock_Emps " +
                    $"WHERE Stocks.id=Stock_Emps.stock_id " +
                    $"AND emp_id={MainClass.EmpNo} " +
                    $"AND IS_Deleted=0 AND status<>2 ORDER BY id",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                cmbTreasury.DisplayMemberPath = "name";
                cmbTreasury.SelectedValuePath = "id";
                cmbTreasury.ItemsSource = dataTable.DefaultView;
                cmbTreasury.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل الخزائن", ex);
            }
        }

        public void LoadSalesMen()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT id, name FROM salesmen WHERE IS_Deleted=0 ORDER BY id",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                cmbSalesMen.DisplayMemberPath = "name";
                cmbSalesMen.SelectedValuePath = "id";
                cmbSalesMen.ItemsSource = dataTable.DefaultView;
                cmbSalesMen.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل المندوبين", ex);
            }
        }

        public void LoadTerms()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT Code, name FROM PM_Terms WHERE IS_Deleted=0 AND Type=2 ORDER BY Code",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                TermsList.Clear();
                foreach (DataRow row in dataTable.Rows)
                {
                    TermsList.Add(new TermItem
                    {
                        Code = Convert.ToInt32(row["Code"]),
                        Name = row["name"]?.ToString()
                    });
                }
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل البنود", ex);
            }
        }

        public void LoadStatus()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT id, name FROM PM_Status WHERE IS_Deleted=0 ORDER BY id",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                cmbStatus.DisplayMemberPath = "name";
                cmbStatus.SelectedValuePath = "id";
                cmbStatus.ItemsSource = dataTable.DefaultView;
                cmbStatus.SelectedIndex = -1;

                cmbStatusSrch.DisplayMemberPath = "name";
                cmbStatusSrch.SelectedValuePath = "id";
                cmbStatusSrch.ItemsSource = dataTable.DefaultView;
                cmbStatusSrch.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل الحالات", ex);
            }
        }

        public void LoadCustomers()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT id, name FROM Customers WHERE (type=1 OR type=3) ORDER BY id",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                cmbClient.DisplayMemberPath = "name";
                cmbClient.SelectedValuePath = "id";
                cmbClient.ItemsSource = dataTable.DefaultView;
                cmbClient.SelectedIndex = -1;

                var dataTable2 = new DataTable();
                adapter.Fill(dataTable2);

                cmbClientSrch.DisplayMemberPath = "name";
                cmbClientSrch.SelectedValuePath = "id";
                cmbClientSrch.ItemsSource = dataTable2.DefaultView;
                cmbClientSrch.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل العملاء", ex);
            }
        }

        private void LoadBanks()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    "SELECT * FROM Banks WHERE IS_Deleted=0", _connectionSecondary);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                cmbBanks.DisplayMemberPath = "name";
                cmbBanks.SelectedValuePath = "id";
                cmbBanks.ItemsSource = dataTable.DefaultView;
                cmbBanks.SelectedIndex = -1;
            }
            catch { /* Ignore bank load errors */ }
        }

        private void LoadDataGrid(string condition)
        {
            try
            {
                SearchRows.Clear();

                var adapter = new SqlDataAdapter(
                    $"SELECT PM_ContractInv.Contr_id, ContrNo, " +
                    $"PM_ContractInv.Regsdate AS date, " +
                    $"PM_ContractInv.statusPK, Customers.name AS cust " +
                    $"FROM PM_ContractInv, Customers " +
                    $"WHERE PM_ContractInv.IS_Deleted=0 AND {condition} " +
                    $"PM_ContractInv.ClientPK=Customers.id " +
                    $"ORDER BY Contr_id",
                    _connection);

                if (!string.IsNullOrEmpty(condition))
                {
                    DateTime toDateExtended = (txtToDate.SelectedDate ?? DateTime.Now).AddHours(24);
                    adapter.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value =
                        (txtFromDate.SelectedDate ?? DateTime.Now).ToShortDateString();
                    adapter.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value =
                        toDateExtended;
                }

                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                foreach (DataRow row in dataTable.Rows)
                {
                    SearchRows.Add(new ContractSearchRow
                    {
                        ContractId = row["Contr_id"]?.ToString(),
                        ContractNo = row["ContrNo"]?.ToString(),
                        ContractDate = Convert.ToDateTime(row["date"]).ToShortDateString(),
                        ClientName = row["cust"]?.ToString(),
                        StatusName = GetStatusName(Convert.ToInt32(row["statusPK"]))
                    });
                }
            }
            catch (Exception ex)
            {
                ShowError("خطأ في تحميل نتائج البحث", ex);
            }
        }

        public void LoadRequirements(int requirementNumber)
        {
            TermRows.Clear();

            var adapter = new SqlDataAdapter(
                $"SELECT * FROM PM_RequirementSub WHERE IsDeleted=0 AND RequirNo={requirementNumber}",
                _connection);
            var dataTable = new DataTable();
            adapter.Fill(dataTable);

            foreach (DataRow row in dataTable.Rows)
            {
                double price = Convert.ToDouble(row["price"]);
                double quantity = Convert.ToDouble(row["Quntity"]);

                TermRows.Add(new ContractTermRow
                {
                    TermPk = Convert.ToInt32(row["TermPk"]),
                    Quantity = quantity,
                    Price = price,
                    Total = price * quantity
                });
            }
        }

        #endregion

        #region Navigation

        public void Navigate(string sqlQuery)
        {
            dgvSrch.UnselectAll();

            try
            {
                EnsureConnectionOpen(_connection);
                using var command = new SqlCommand(sqlQuery, _connection);
                using var reader = command.ExecuteReader();
                ReadData(reader);
            }
            catch (Exception ex)
            {
                ShowError("خطأ في التنقل", ex);
            }
            finally
            {
                EnsureConnectionClosed(_connection);
            }
        }

        private void btnFirst_Click(object sender, RoutedEventArgs e)
            => Navigate("SELECT TOP 1 * FROM PM_ContractInv WHERE IS_Deleted=0 ORDER BY ContrNo ASC");

        private void btnNext_Click(object sender, RoutedEventArgs e)
            => Navigate($"SELECT TOP 1 * FROM PM_ContractInv WHERE IS_Deleted=0 AND ContrNo>{_currentCode} ORDER BY ContrNo ASC");

        private void btnPrevious_Click(object sender, RoutedEventArgs e)
            => Navigate($"SELECT TOP 1 * FROM PM_ContractInv WHERE IS_Deleted=0 AND ContrNo<{_currentCode} ORDER BY ContrNo DESC");

        private void btnLast_Click(object sender, RoutedEventArgs e)
            => Navigate("SELECT TOP 1 * FROM PM_ContractInv WHERE IS_Deleted=0 ORDER BY ContrNo DESC");

        #endregion

        #region Read Data

        private void ReadData(SqlDataReader reader)
        {
            try
            {
                if (!reader.HasRows)
                {
                    ClearForm();
                    return;
                }

                reader.Read();
                ClearForm();

                _currentCode = Convert.ToInt32(reader["ContrNo"]);
                // P7-010 fix: مفتاح السطر (Contr_id) يُتتبع منفصلاً عن الرقم التجاري
                // (ContrNo) — كان المحدّث يمرر الرقم التجاري إلى معامل المفتاح
                _currentContrId = Convert.ToInt32(reader["Contr_id"]);
                _restrictionNumber = Convert.ToInt32(reader["RestractionPk"]);

                txtNo.Text = _currentCode.ToString();
                txtDate.SelectedDate = Convert.ToDateTime(reader["Regsdate"]);
                txtDateStart.SelectedDate = Convert.ToDateTime(reader["StartDate"]);
                txtDateFinish.SelectedDate = Convert.ToDateTime(reader["Enddate"]);

                cmbStatus.SelectedValue = Convert.ToDouble(reader["statusPk"]);

                int paymentType = Convert.ToInt32(reader["PayType"]);
                cmbType.SelectedIndex = paymentType == -1 ? 0 : paymentType;

                TrySetComboValue(cmbTreasury, reader["TreasuryPk"]);
                TrySetComboValue(cmbBanks, reader["BankId"]);
                TrySetComboValue(cmbClient, reader["ClientPK"]);
                TrySetComboValue(cmbSalesMen, reader["salesman"]);

                txtReff.Text = reader["RefrNo"]?.ToString() ?? "";
                txtPeriod.Text = reader["ExcutePeriod"]?.ToString() ?? "";
                txtTotPrice.Text = reader["TotVal"]?.ToString() ?? "0";
                txtNetVal.Text = reader["NetCost"]?.ToString() ?? "0";
                txtNetVAT.Text = reader["VATval"]?.ToString() ?? "0";
                txtPayerName.Text = reader["PayerName"]?.ToString() ?? "";

                reader.Close();

                // Load sub items
                // P7-013 fix: تحميل البنود يستعيد تكلفة القالب (PM_Terms.cost)
                // ويعيد بناء الصافي بضرب الكمية — كان الصافي يُبنى بلا كمية
                // والتكلفة تضيع فيبقى صفراً عند إعادة الحفظ فيفسد مشروع البند
                var adapter = new SqlDataAdapter(
                    $@"SELECT PM_ContractInvSub.*, ISNULL(PM_Terms.cost,0) AS TermCost " +
                    $@"FROM PM_ContractInvSub " +
                    $@"LEFT JOIN PM_Terms ON PM_ContractInvSub.TermPk=PM_Terms.Code " +
                    $@"WHERE PM_ContractInvSub.ContrNo={_currentCode}",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                foreach (DataRow row in dataTable.Rows)
                {
                    double price = Convert.ToDouble(row["price"]);
                    double quantity = Convert.ToDouble(row["Quntity"]);
                    double vat = Convert.ToDouble(row["VAT"]);
                    double cost = Convert.ToDouble(row["TermCost"]);

                    TermRows.Add(new ContractTermRow
                    {
                        TermPk = Convert.ToInt32(row["TermPk"]),
                        ProjectName = row["notes"]?.ToString(),
                        Quantity = quantity,
                        Price = price,
                        Cost = cost,
                        Total = price * quantity,
                        VAT = vat,
                        // P7-013 fix: نفس حساب المحرر — صافي البند = سعر×كمية + ضريبة
                        NetValue = price * quantity + vat,
                        NetCost = cost * quantity,
                        StatusName = GetStatusName(Convert.ToInt32(row["status"]))
                    });
                }
            }
            catch (Exception ex)
            {
                ShowError("خطأ في قراءة البيانات", ex);
            }
        }

        #endregion

        #region Save

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            EnsureConnectionOpen(_connection);
            EnsureConnectionOpen(_connectionSecondary);

            SqlTransaction transaction = _connection.BeginTransaction();

            try
            {
                // Trial check
                if (MainClass.IsTrial && _currentCode == -1)
                {
                    var trialAdapter = new SqlDataAdapter(
                        "SELECT id FROM Entry", _connectionSecondary);
                    var trialTable = new DataTable();
                    trialAdapter.Fill(trialTable);

                    if (trialTable.Rows.Count >= 20)
                    {
                        string trialMsg = MainClass.Language == "en"
                            ? "Sorry, You reached the maximum entries for trial version."
                            : "نأسف، لقد وصلت لأقصى حد إدخال للنسخة التجريبية.";
                        MessageBox.Show(trialMsg, "تنبيه",
                            MessageBoxButton.OK, MessageBoxImage.Information);
                        return;
                    }
                }

                // Validate client
                if (cmbClient.SelectedIndex == -1)
                {
                    MessageBox.Show("يجب اختيار العميل", "تحقق من البيانات",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    cmbClient.Focus();
                    return;
                }

                // Validate rows
                if (TermRows.Count == 0)
                {
                    MessageBox.Show("يجب استكمال بيانات البند", "تحقق من البيانات",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                foreach (var row in TermRows)
                {
                    if (string.IsNullOrWhiteSpace(row.ProjectName))
                    {
                        MessageBox.Show("يجب إدخال اسم المشروع", "تحقق من البيانات",
                            MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }
                }

                // Get client account code
                int clientAccountCode = GetClientAccountCode();

                // Treasury/Bank IDs
                int treasuryId = -1;
                int treasuryAccCode = 0;
                int paymentTypeId = -1;
                int bankId = -1;
                int bankAccCode = 0;
                int salesmanId = -1;

                if (cmbSalesMen.SelectedIndex > -1)
                    salesmanId = Convert.ToInt32(cmbSalesMen.SelectedValue);

                if (cmbType.SelectedIndex == 1) // Cash
                {
                    if (cmbTreasury.SelectedIndex == -1)
                    {
                        MessageBox.Show("يجب اختيار الخزنة", "تحقق من البيانات",
                            MessageBoxButton.OK, MessageBoxImage.Warning);
                        cmbTreasury.Focus();
                        return;
                    }

                    paymentTypeId = 1;
                    treasuryId = Convert.ToInt32(cmbTreasury.SelectedValue);
                    treasuryAccCode = GetTreasuryAccountCode(treasuryId);
                }
                else if (cmbType.SelectedIndex == 2) // Bank
                {
                    if (cmbBanks.SelectedIndex == -1)
                    {
                        MessageBox.Show("يجب اختيار البنك أو تغيير طريقة الدفع",
                            "تحقق من البيانات", MessageBoxButton.OK, MessageBoxImage.Warning);
                        cmbBanks.Focus();
                        return;
                    }

                    paymentTypeId = 2;
                    bankId = Convert.ToInt32(cmbBanks.SelectedValue);
                    bankAccCode = GetBankAccountCode(bankId);
                }

                // Entry number + GlobalID
                // P7-014 fix: القيد على عقد المخطط الموحد (Entry.GlobalID + Entry_sub)
                // عبر نواة EntryOper.SaveEnty داخل معاملة العقد — الكتابة
                // اليدوية القديمة كانت تستهدف Restrictions_Sub (الاسم قبل
                // الترحيل) وأعمدة ناقصة فتفشل على القواعد المهاجرة أصلاً
                int entryNumber = 0;
                string entryGlobalId = null;
                double netValue = ParseDouble(txtNetVal.Text);

                if (netValue != 0)
                {
                    // P7-014 fix: السجل القديم بلا قيد (RestractionPk<=0) يرمم بقيد جديد
                    bool entryIsNew = _currentCode == -1 || _restrictionNumber <= 0;
                    if (entryIsNew)
                    {
                        EntryOper.GetEntryGlobalID(ref entryGlobalId, ref entryNumber);
                    }
                    else
                    {
                        entryNumber = _restrictionNumber;
                        EntryOper.GenerateEntryGlobalIDByEntryNo(
                            ref entryGlobalId, entryNumber, MainClass.BranchNo);
                    }
                }

                // Build main command
                SqlCommand mainCommand;
                if (_currentCode == -1)
                    mainCommand = new SqlCommand(StoredQueries.InsertContractInv, _connection, transaction);
                else
                {
                    // P7-010 fix: التعديل يستهدف مفتاح السطر Contr_id لا الرقم
                    // التجاري ContrNo — كان الرقم التجاري يمرر إلى معامل
                    // المفتاح فيصيب السطر الخطأ أو لا سطر
                    int targetContrId = _currentContrId;
                    if (targetContrId <= 0)
                    {
                        using var findCmd = new SqlCommand(
                            "SELECT Contr_id FROM PM_ContractInv WHERE ContrNo=@ContrNo",
                            _connection, transaction);
                        findCmd.Parameters.Add("@ContrNo", SqlDbType.Int).Value = _currentCode;
                        var found = findCmd.ExecuteScalar();
                        if (found == null || found == DBNull.Value)
                        {
                            MessageBox.Show("العقد المطلوب تعديله غير موجود", "خطأ",
                                MessageBoxButton.OK, MessageBoxImage.Error);
                            transaction.Rollback();
                            return;
                        }
                        targetContrId = Convert.ToInt32(found);
                    }
                    mainCommand = new SqlCommand(StoredQueries.UpdateContractInv, _connection, transaction);
                    mainCommand.Parameters.Add("@Contr_id", SqlDbType.Int).Value = targetContrId;
                }

                mainCommand.Parameters.Add("@ContrType", SqlDbType.Int).Value = 1;
                mainCommand.Parameters.Add("@Proctype", SqlDbType.Int).Value = _processType;
                mainCommand.Parameters.Add("@ContrNo", SqlDbType.Int).Value = ParseDouble(txtNo.Text);
                mainCommand.Parameters.Add("@RegsDate", SqlDbType.DateTime).Value = txtDate.SelectedDate ?? DateTime.Now;
                mainCommand.Parameters.Add("@StartDate", SqlDbType.DateTime).Value = txtDateStart.SelectedDate ?? DateTime.Now;
                mainCommand.Parameters.Add("@EndDate", SqlDbType.DateTime).Value = txtDateFinish.SelectedDate ?? DateTime.Now;
                mainCommand.Parameters.Add("@statusPk", SqlDbType.Int).Value = cmbStatus.SelectedValue ?? DBNull.Value;
                mainCommand.Parameters.Add("@PayType", SqlDbType.Int).Value = paymentTypeId;
                mainCommand.Parameters.Add("@BankId", SqlDbType.Int).Value = bankId;
                mainCommand.Parameters.Add("@ExcutePeriod", SqlDbType.Int).Value =
                    string.IsNullOrWhiteSpace(txtPeriod.Text) ? (object)DBNull.Value : int.Parse(txtPeriod.Text);
                mainCommand.Parameters.Add("@RefrNo", SqlDbType.Int).Value =
                    string.IsNullOrWhiteSpace(txtReff.Text) ? (object)DBNull.Value : int.Parse(txtReff.Text);
                mainCommand.Parameters.Add("@ClientPk", SqlDbType.Int).Value = cmbClient.SelectedValue;
                mainCommand.Parameters.Add("@EmpNo", SqlDbType.Int).Value = MainClass.EmpNo;
                mainCommand.Parameters.Add("@TreasuryPk", SqlDbType.Int).Value = treasuryId;
                mainCommand.Parameters.Add("@RestractionPk", SqlDbType.Int).Value = entryNumber;
                mainCommand.Parameters.Add("@BranchPK", SqlDbType.Int).Value = MainClass.BranchNo;
                mainCommand.Parameters.Add("@TotVal", SqlDbType.Float).Value = ParseDouble(txtTotPrice.Text);
                // P7-012 fix: ضريبة الرأس تُحفظ كما حُسبت من البنود — كانت تجبر
                // صفراً بينما القيد يستخدمها وتقرير العقد يعرضها
                mainCommand.Parameters.Add("@VATval", SqlDbType.Float).Value = ParseDouble(txtNetVAT.Text);
                mainCommand.Parameters.Add("@discount", SqlDbType.Float).Value = 0;
                mainCommand.Parameters.Add("@NetCost", SqlDbType.Float).Value = netValue;
                mainCommand.Parameters.Add("@Salesman", SqlDbType.Int).Value = salesmanId;
                mainCommand.Parameters.Add("@PayerName", SqlDbType.NVarChar).Value = txtPayerName.Text;
                mainCommand.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value = 0;
                mainCommand.ExecuteNonQuery();

                // Delete existing sub items if editing
                if (_currentCode != -1)
                {
                    new SqlCommand(
                        $"DELETE FROM PM_ContractInvSub WHERE ContrNo={_currentCode}",
                        _connection, transaction).ExecuteNonQuery();
                }

                // Insert sub items + reconcile projects
                int contractNo = (int)ParseDouble(txtNo.Text);
                foreach (var termRow in TermRows)
                {
                    InsertContractSubItem(_connection, transaction, contractNo, termRow);
                    // P7-011 fix: مصالحة المشروعات بدل إنشاء جديد عند كل إعادة حفظ
                    UpsertProject(_connection, transaction, contractNo, termRow, _currentCode != -1);
                }

                // P7-011 fix: مشروعات البنود المحذوفة من التحرير تُقعد (soft delete)
                // — كانت تبقى حية بلا بند يمثلها
                if (_currentCode != -1)
                {
                    RetireAbsentProjects(_connection, transaction, contractNo, TermRows);
                }

                // P7-014 fix: القيد الموحد عبر EntryOper.SaveEnty داخل معاملة العقد
                // (GlobalID + Entry_sub + حراس الهوية والتوازن والترقيم)
                if (netValue != 0)
                {
                    Entry pmEntry = BuildContractEntry(
                        entryGlobalId, entryNumber, clientAccountCode,
                        treasuryAccCode, bankAccCode, paymentTypeId, netValue);
                    bool entryIsNew = _currentCode == -1 || _restrictionNumber <= 0;

                    if (!new EntryOper().SaveEnty(pmEntry, _connection, transaction, entryIsNew))
                    {
                        try { transaction.Rollback(); } catch { }
                        return;
                    }
                }

                transaction.Commit();
                TermRows.Clear();

                var saveMsg = new frmSavedMsg();
                saveMsg.ShowDialog();

                if (saveMsg.Pressed == 1)
                    ClearForm();
                else if (saveMsg.Pressed == 3)
                {
                    TermRows.Clear();
                    ClearForm();
                    Close();
                }
            }
            catch (Exception ex)
            {
                transaction.Rollback();
                ShowError("خطأ أثناء الحفظ", ex);
            }
            finally
            {
                EnsureConnectionClosed(_connection);
                EnsureConnectionClosed(_connectionSecondary);
            }
        }

        #endregion

        #region Journal Entry Helpers

        // P7-014 fix: بناء قيد العقد على نموذج القيود الموحد (Entry) — نفس
        // بنود المحاسبة القديمة (مدين إيرات/ضريبة، دائن العميل، وتسوية النقدي/البنكي)
        // لكن عبر SaveEnty بعقد GlobalID وEntry_sub الكاملين
        private Entry BuildContractEntry(
            string entryGlobalId, int entryNumber, int clientAccountCode,
            int treasuryAccCode, int bankAccCode, int paymentTypeId, double netValue)
        {
            string invoiceNote = $"فاتورة عقد {cmbType.Text} رقم:{txtNo.Text} خاصة العميل:{cmbClient.Text}";

            var entry = new Entry
            {
                EntryGlobalID = entryGlobalId,
                ClientCode = Sync.ClientCode,
                EntryNo = entryNumber,
                EntryDate = txtDate.SelectedDate ?? DateTime.Now,
                ReffNo = txtNo.Text,
                RefDate = txtDate.SelectedDate ?? DateTime.Now,
                Type = (EntryType)(_processType == 1 ? 14 : 24),
                State = 1,
                Note = invoiceNote,
                Branch = MainClass.BranchNo,
                EmpID = MainClass.EmpNo,
                DistBranch = Sync.DistBranch,
                BranchType = Sync.BranchType
            };

            var accounts = new System.Collections.Generic.List<Account>();

            if (_processType == 1)
            {
                accounts.Add(new Account
                {
                    EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                    Name = "4200003", Code = "4200003",
                    Debt = ParseDouble(txtTotPrice.Text), Credit = 0.0,
                    Note = invoiceNote, CCcode = "-1"
                });

                if (ParseDouble(txtNetVAT.Text) > 0)
                    accounts.Add(new Account
                    {
                        EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                        Name = "الضريبة المضافة", Code = "2222001",
                        Debt = ParseDouble(txtNetVAT.Text), Credit = 0.0,
                        Note = $"ض. القيمة المضافة {invoiceNote}", CCcode = "-1"
                    });

                accounts.Add(new Account
                {
                    EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                    Name = cmbClient.Text, Code = clientAccountCode.ToString(),
                    Debt = 0.0, Credit = netValue,
                    Note = invoiceNote, CCcode = "-1"
                });

                if (paymentTypeId == 1) // Cash
                {
                    accounts.Add(new Account
                    {
                        EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                        Name = cmbTreasury.Text, Code = treasuryAccCode.ToString(),
                        Debt = netValue, Credit = 0.0,
                        Note = invoiceNote, CCcode = "-1"
                    });
                    accounts.Add(new Account
                    {
                        EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                        Name = cmbClient.Text, Code = clientAccountCode.ToString(),
                        Debt = 0.0, Credit = netValue,
                        Note = invoiceNote, CCcode = "-1"
                    });
                }
                else if (paymentTypeId == 2) // Bank
                {
                    accounts.Add(new Account
                    {
                        EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                        Name = cmbBanks.Text, Code = bankAccCode.ToString(),
                        Debt = netValue, Credit = 0.0,
                        Note = invoiceNote, CCcode = "-1"
                    });
                    accounts.Add(new Account
                    {
                        EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                        Name = cmbClient.Text, Code = clientAccountCode.ToString(),
                        Debt = 0.0, Credit = netValue,
                        Note = invoiceNote, CCcode = "-1"
                    });
                }
            }
            else // Return contract (24)
            {
                string returnNote = $"فاتورة مرتجع عقد {cmbType.Text} رقم:{txtNo.Text} خاصة العميل:{cmbClient.Text}";
                entry.Note = returnNote;

                accounts.Add(new Account
                {
                    EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                    Name = cmbClient.Text, Code = clientAccountCode.ToString(),
                    Debt = 0.0, Credit = netValue,
                    Note = returnNote, CCcode = "-1"
                });
                accounts.Add(new Account
                {
                    EntryGlobalID = entryGlobalId, EntryNo = entryNumber,
                    Name = "4100002", Code = "4100002",
                    Debt = netValue, Credit = 0.0,
                    Note = returnNote, CCcode = "-1"
                });
            }

            entry.Accounts = accounts;
            return entry;
        }

        private static void InsertContractSubItem(
            SqlConnection conn, SqlTransaction trans,
            int contractNo, ContractTermRow row)
        {
            var cmd = new SqlCommand(
                @"INSERT INTO PM_ContractInvSub
                  (ContrNo,status,TermPk,Quntity,price,VAT,discount,notes)
                  VALUES(@ContrNo,@status,@TermPk,@Quntity,@price,@VAT,@discount,@notes)",
                conn, trans);
            cmd.Parameters.Add("@ContrNo", SqlDbType.Int).Value = contractNo;
            cmd.Parameters.Add("@TermPK", SqlDbType.Int).Value = row.TermPk;
            cmd.Parameters.Add("@Quntity", SqlDbType.Int).Value = (int)row.Quantity;
            cmd.Parameters.Add("@status", SqlDbType.Int).Value = MainClass.BranchNo;
            cmd.Parameters.Add("@price", SqlDbType.Float).Value = row.Price;
            cmd.Parameters.Add("@VAT", SqlDbType.Float).Value = row.VAT;
            cmd.Parameters.Add("@discount", SqlDbType.Float).Value = 0;
            cmd.Parameters.Add("@notes", SqlDbType.NVarChar).Value = row.ProjectName ?? "";
            cmd.ExecuteNonQuery();
        }

        // P7-011 fix: المصالحة — عند التحرير يُحدّث مشروع البند الموجود
        // (بنفس العقد والبند) بدل إنشاء سطر جديد فيتضاعف المشروعات مع كل
        // إعادة حفظ؛ عند الإنشاء يُدرج جديد كالسابق
        private void UpsertProject(
            SqlConnection conn, SqlTransaction trans,
            int contractNo, ContractTermRow row, bool isEdit)
        {
            int existingProjectId = -1;

            if (isEdit)
            {
                using (var findCmd = new SqlCommand(
                    "SELECT TOP 1 id FROM PM_Projects WITH (UPDLOCK, HOLDLOCK) " +
                    "WHERE ContractPk=@ContractPk AND TermPk=@TermPk AND IS_Deleted=0",
                    conn, trans))
                {
                    findCmd.Parameters.Add("@ContractPk", SqlDbType.Int).Value = contractNo;
                    findCmd.Parameters.Add("@TermPk", SqlDbType.Int).Value = row.TermPk;
                    var found = findCmd.ExecuteScalar();
                    if (found != null && found != DBNull.Value)
                        existingProjectId = Convert.ToInt32(found);
                }
            }

            if (existingProjectId != -1)
            {
                var cmd = new SqlCommand(
                    @"UPDATE PM_Projects SET
                      name=@name, TermPk=@TermPk, statusPk=@statusPk,
                      RegsDate=@RegsDate, price=@price, cost=@cost,
                      Quantity=@Quantity, VAT=@VAT, IS_Deleted=0
                      WHERE id=@id",
                    conn, trans);
                cmd.Parameters.Add("@id", SqlDbType.Int).Value = existingProjectId;
                cmd.Parameters.Add("@name", SqlDbType.NVarChar).Value = row.ProjectName ?? "";
                cmd.Parameters.Add("@TermPK", SqlDbType.Int).Value = row.TermPk;
                cmd.Parameters.Add("@Quantity", SqlDbType.Int).Value = (int)row.Quantity;
                cmd.Parameters.Add("@statusPK", SqlDbType.Int).Value = cmbStatus.SelectedValue ?? DBNull.Value;
                cmd.Parameters.Add("@Price", SqlDbType.Float).Value = row.NetValue;
                cmd.Parameters.Add("@cost", SqlDbType.Float).Value = row.NetCost;
                cmd.Parameters.Add("@VAT", SqlDbType.Float).Value = row.VAT;
                cmd.Parameters.Add("@RegsDate", SqlDbType.DateTime).Value = txtDate.SelectedDate ?? DateTime.Now;
                cmd.ExecuteNonQuery();
            }
            else
            {
                int newProjectId;
                using (var maxCmd = new SqlCommand(
                    "SELECT MAX(id) FROM PM_Projects", conn, trans))
                {
                    newProjectId = (int)(ParseDouble(maxCmd.ExecuteScalar()?.ToString()) + 1);
                }

                var cmd = new SqlCommand(
                    @"INSERT INTO PM_Projects
                      (id,name,TermPk,ContractPk,statusPk,RegsDate,price,cost,Quantity,VAT,IS_Deleted)
                      VALUES(@id,@name,@TermPk,@ContractPk,@statusPk,@RegsDate,
                             @price,@cost,@Quantity,@VAT,@IS_Deleted)",
                    conn, trans);
                cmd.Parameters.Add("@id", SqlDbType.Int).Value = newProjectId;
                cmd.Parameters.Add("@ContractPk", SqlDbType.Int).Value = contractNo;
                cmd.Parameters.Add("@name", SqlDbType.NVarChar).Value = row.ProjectName ?? "";
                cmd.Parameters.Add("@TermPK", SqlDbType.Int).Value = row.TermPk;
                cmd.Parameters.Add("@Quantity", SqlDbType.Int).Value = (int)row.Quantity;
                cmd.Parameters.Add("@statusPK", SqlDbType.Int).Value = cmbStatus.SelectedValue ?? DBNull.Value;
                cmd.Parameters.Add("@Price", SqlDbType.Float).Value = row.NetValue;
                cmd.Parameters.Add("@cost", SqlDbType.Float).Value = row.NetCost;
                cmd.Parameters.Add("@VAT", SqlDbType.Float).Value = row.VAT;
                cmd.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value = 0;
                cmd.Parameters.Add("@RegsDate", SqlDbType.DateTime).Value = txtDate.SelectedDate ?? DateTime.Now;
                cmd.ExecuteNonQuery();
            }
        }

        // P7-011 fix: مشروعات العقد التي لم يبق لها بند في التحرير تُقعد منطقياً
        private static void RetireAbsentProjects(
            SqlConnection conn, SqlTransaction trans,
            int contractNo, ObservableCollection<ContractTermRow> rows)
        {
            var termIds = new System.Collections.Generic.List<int>();
            foreach (var row in rows)
                termIds.Add(row.TermPk);

            if (termIds.Count == 0) return;

            string inList = string.Join(",", termIds);
            var cmd = new SqlCommand(
                "UPDATE PM_Projects SET IS_Deleted=1 " +
                $"WHERE ContractPk=@ContractPk AND IS_Deleted=0 AND TermPk NOT IN ({inList})",
                conn, trans);
            cmd.Parameters.Add("@ContractPk", SqlDbType.Int).Value = contractNo;
            cmd.ExecuteNonQuery();
        }

        #endregion

        #region Calculations

        private void RecalculateTotals()
        {
            try
            {
                double totalNet = 0;
                double totalPrice = 0;
                double totalVAT = 0;

                foreach (var row in TermRows)
                {
                    double subtotal = row.Quantity * row.Price;
                    double vat = Math.Round(_defaultVAT / 100.0 * subtotal, 2);
                    double netValue = subtotal + vat;

                    row.Total = subtotal;
                    row.VAT = vat;
                    row.NetValue = netValue;
                    row.NetCost = row.Quantity * row.Cost;

                    totalNet += netValue;
                    totalPrice += subtotal;
                    totalVAT += vat;
                }

                txtNetVal.Text = $"{totalNet:N2}";
                txtTotPrice.Text = $"{totalPrice:N2}";
                txtNetVAT.Text = $"{totalVAT:N2}";

                dgvterms.Items.Refresh();
            }
            catch (Exception ex)
            {
                ShowError("خطأ في الحساب", ex);
            }
        }

        private void LoadTermDetails(ContractTermRow row, int termCode)
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT price, cost, VAT FROM PM_Terms WHERE Code={termCode}",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                if (dataTable.Rows.Count > 0)
                {
                    double price = Convert.ToDouble(dataTable.Rows[0]["price"]);
                    double cost = Convert.ToDouble(dataTable.Rows[0]["cost"]);

                    row.Quantity = 1;
                    row.Price = price;
                    row.Cost = cost;
                    row.VAT = _defaultVAT;
                    row.NetValue = price + _defaultVAT / 100.0 * price;
                    row.NetCost = cost + _defaultVAT / 100.0 * cost;
                }
            }
            catch { }
        }

        #endregion

        #region Search

        private void Search()
        {
            if (!chkAll.IsChecked == true && cmbClientSrch.SelectedValue == null)
            {
                MessageBox.Show(MainClass.Language == "ar"
                    ? "اختر العميل أو الكل"
                    : "Choose client or all",
                    "تنبيه", MessageBoxButton.OK, MessageBoxImage.Warning);
                cmbClientSrch.Focus();
                return;
            }

            string branchPart = MainClass.BranchNo != -1
                ? $"BranchPK={MainClass.BranchNo} AND "
                : "";

            string condition = string.IsNullOrWhiteSpace(txtSrchNo.Text)
                ? $"{branchPart} RegsDate>=@date1 AND RegsDate<=@date2 AND "
                : $"{branchPart} PM_ContractInv.ContrNo={txtSrchNo.Text} AND ";

            if (chkAll.IsChecked != true && cmbClientSrch.SelectedValue != null)
                condition += $" ClientPk={cmbClientSrch.SelectedValue} AND ";

            if (cmbStatusSrch.SelectedIndex > -1)
                condition += $" statusPK={cmbStatusSrch.SelectedValue} AND ";

            LoadDataGrid(condition);
        }

        private void btnSearch_Click(object sender, RoutedEventArgs e)
            => Search();

        private void dgvSrch_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            if (dgvSrch.SelectedItem is ContractSearchRow selectedRow
                && int.TryParse(selectedRow.ContractNo, out int contractNo))
            {
                _currentCode = contractNo;
                Navigate($"SELECT * FROM PM_ContractInv WHERE ContrNo={_currentCode}");
            }
        }

        #endregion

        #region DataGrid Events

        private void dgvterms_CellEditEnding(object sender, DataGridCellEditEndingEventArgs e)
        {
            if (e.Row.Item is ContractTermRow row)
            {
                int colIndex = dgvterms.Columns.IndexOf(e.Column);
                if (colIndex == 2 || colIndex == 3) // Quantity or Price
                    RecalculateTotals();
            }
        }

        private void dgvterms_CurrentCellChanged(object sender, EventArgs e)
        {
            if (dgvterms.CurrentCell.Column != null)
                dgvterms.CommitEdit();
        }

        private void TermComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (sender is ComboBox cb && cb.SelectedValue is int termCode
                && dgvterms.CurrentItem is ContractTermRow row)
            {
                row.TermPk = termCode;
                LoadTermDetails(row, termCode);
                RecalculateTotals();
            }
        }

        private void DeleteTermRow_Click(object sender, RoutedEventArgs e)
        {
            if (sender is Button btn && btn.DataContext is ContractTermRow row)
            {
                var result = MessageBox.Show("هل تريد حذف البند؟", "تأكيد الحذف",
                    MessageBoxButton.YesNo, MessageBoxImage.Question);
                if (result == MessageBoxResult.Yes)
                {
                    TermRows.Remove(row);
                    RecalculateTotals();
                }
            }
        }

        #endregion

        #region ComboBox Events

        private void cmbType_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (cmbType == null) return;

            if (cmbType.SelectedIndex == 2) // Bank
            {
                cmbBanks.SelectedIndex = -1;
                cmbTreasury.SelectedIndex = -1;
                if (cmbClient.Items.Count > 0) cmbClient.SelectedIndex = 0;
                cmbBanks.IsEnabled = true;
                cmbBanks.Focus();
            }
            else
            {
                cmbBanks.IsEnabled = false;
            }

            if (cmbType.SelectedIndex == 1) // Cash
            {
                if (cmbTreasury.Items.Count > 0) cmbTreasury.SelectedIndex = 0;
                if (cmbClient.Items.Count > 0) cmbClient.SelectedIndex = 0;
            }

            if (cmbType.SelectedIndex == 0) // Credit
            {
                cmbTreasury.SelectedIndex = -1;
                cmbClient.SelectedIndex = -1;
                cmbClient.Focus();
            }
        }

        private void cmbStatus_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            // Status changed handler
        }

        private void chkAll_CheckedChanged(object sender, RoutedEventArgs e)
        {
            bool isAllChecked = chkAll.IsChecked == true;
            cmbClientSrch.IsEnabled = !isAllChecked;
            if (isAllChecked)
                cmbClientSrch.SelectedIndex = -1;
        }

        private void txtMobile_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtMobile.Text)) return;

            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT id FROM Customers WHERE mobile=N'{txtMobile.Text.Trim()}' " +
                    $"AND (type=1 OR type=3)",
                    _connection);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);

                if (dataTable.Rows.Count > 0)
                {
                    chkAll.IsChecked = false;
                    cmbClientSrch.SelectedValue = dataTable.Rows[0]["id"];
                }
            }
            catch { }
        }

        #endregion

        #region Button Events

        private void btnNew_Click(object sender, RoutedEventArgs e)
        {
            ClearForm();
            cmbClient.Focus();
        }

        private void btnClose_Click(object sender, RoutedEventArgs e) => Close();

        private void btnDelete_Click(object sender, RoutedEventArgs e)
        {
            // Delete logic placeholder
            MessageBox.Show("يرجى تحديد عقد من البحث أولاً", "تنبيه",
                MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void btnCustAdd_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var form = new frmClientPM();
                MainClass.ApplyPermissionToForm(form);
                MainClass.DoApplyUserSett(form);
                form.Title = "تعريف عميل";
                form.rdClient.IsChecked = true;
                form.rdSupplier.IsChecked = false;
                form.rbOwner.IsChecked = false;
                //form.rdSupplier.Hide();
                //form.rbOwner.Hide();
                //form.rdClient.Hide();
                form.rdSupplier.Visibility = System.Windows.Visibility.Collapsed;
                form.rbOwner.Visibility = System.Windows.Visibility.Collapsed;
                form.rdClient.Visibility = System.Windows.Visibility.Collapsed;
                form.ShowDialog();

                if (form.isDone)
                    LoadCustomers();
            }
            catch (Exception ex)
            {
                ShowError("خطأ في إضافة عميل", ex);
            }
        }

        private void btnAddSaleman_Click(object sender, RoutedEventArgs e)
        {
            var form = new frmSalesMen();
            form.ShowDialog();
            if (form.isDone)
                LoadSalesMen();
        }

        private void Button1_Click(object sender, RoutedEventArgs e)
        {
            // Print mosque contract
        }

        private void Button2_Click(object sender, RoutedEventArgs e)
        {
            // Gift / donation
        }

        private void Button5_Click(object sender, RoutedEventArgs e)
        {
            // Print wells contract
        }

        #endregion

        #region Helper Methods

        private int GetClientAccountCode()
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT Code FROM Accounts_Index WHERE type=2 AND AName='{cmbClient.Text}'",
                    _connectionSecondary);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);
                return dataTable.Rows.Count > 0
                    ? (int)ParseDouble(dataTable.Rows[0][0]?.ToString())
                    : 0;
            }
            catch { return 0; }
        }

        private int GetTreasuryAccountCode(int treasuryId)
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT Acc_Code FROM Stocks WHERE id={treasuryId} " +
                    $"AND IS_Deleted=0 AND branch={MainClass.BranchNo}",
                    _connectionSecondary);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);
                return dataTable.Rows.Count > 0
                    ? (int)ParseDouble(dataTable.Rows[0][0]?.ToString())
                    : 0;
            }
            catch { return 0; }
        }

        private int GetBankAccountCode(int bankId)
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT Acc_Code FROM Banks WHERE id={bankId}",
                    _connectionSecondary);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);
                return dataTable.Rows.Count > 0
                    ? (int)ParseDouble(dataTable.Rows[0]["acc_code"]?.ToString())
                    : 0;
            }
            catch { return 0; }
        }

        private string GetStatusName(int statusId)
        {
            try
            {
                var adapter = new SqlDataAdapter(
                    $"SELECT name FROM PM_Status WHERE id={statusId}",
                    _connectionSecondary);
                var dataTable = new DataTable();
                adapter.Fill(dataTable);
                return dataTable.Rows.Count > 0 ? dataTable.Rows[0][0]?.ToString() ?? "" : "";
            }
            catch { return ""; }
        }

        private static void TrySetComboValue(ComboBox comboBox, object value)
        {
            try
            {
                if (value != null && value != DBNull.Value)
                    comboBox.SelectedValue = value;
            }
            catch { }
        }

        private static double ParseDouble(string text)
        {
            if (string.IsNullOrWhiteSpace(text)) return 0;
            return double.TryParse(text, out double result) ? result : 0;
        }

        private static void EnsureConnectionOpen(SqlConnection connection)
        {
            if (connection.State != ConnectionState.Open)
                connection.Open();
        }

        private static void EnsureConnectionClosed(SqlConnection connection)
        {
            if (connection.State != ConnectionState.Closed)
                connection.Close();
        }

        private static void ShowError(string title, Exception ex)
        {
            MessageBox.Show(
                $"{title}{Environment.NewLine}تفاصيل الخطأ: {ex.Message}",
                "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        #endregion

        #region Data Models

        public class ContractTermRow : System.ComponentModel.INotifyPropertyChanged
        {
            private double _quantity;
            private double _price;

            public int TermPk { get; set; }
            public string TermName { get; set; }
            public string ProjectName { get; set; }
            public double VAT { get; set; }
            public double Total { get; set; }
            public double NetValue { get; set; }
            public double Cost { get; set; }
            public double NetCost { get; set; }
            public string StatusName { get; set; }

            public double Quantity
            {
                get => _quantity;
                set { _quantity = value; OnPropertyChanged(nameof(Quantity)); }
            }

            public double Price
            {
                get => _price;
                set { _price = value; OnPropertyChanged(nameof(Price)); }
            }

            public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;
            protected void OnPropertyChanged(string name)
                => PropertyChanged?.Invoke(this, new System.ComponentModel.PropertyChangedEventArgs(name));
        }

        public class ContractSearchRow
        {
            public string ContractId { get; set; }
            public string ContractNo { get; set; }
            public string ContractDate { get; set; }
            public string ClientName { get; set; }
            public string StatusName { get; set; }
        }

        public class TermItem
        {
            public int Code { get; set; }
            public string Name { get; set; }
        }

        #endregion
    }
}