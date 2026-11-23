using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using DevExpress.Xpf.Core;
using DevExpress.XtraReports.UI;
using Button = System.Windows.Controls.Button;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmRptCostCenter : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection _conn;

        private bool   _printHeader = true;
        private bool   _printFooter = true;
        private bool   _printStamp  = true;
        private int    _printType   = 1;
        private int    _printNo     = 1;
        private string _defPrinter  = "";
        private string _rptName     = "";
        private string _rptUrl      = "";

        public  int _Type       = 1;

        private ObservableCollection<CostCenterRow> _dataSource
            = new ObservableCollection<CostCenterRow>();

        #endregion

        #region Constructor

        public frmRptCostCenter()
        {
            InitializeComponent();
            _conn = MainClass.ConnObj();
            GridControl1.ItemsSource = _dataSource;
        }

        #endregion

        #region Window Events

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            txtDateFrom.DateTime = DateTime.Now;
            txtDateTo.DateTime   = DateTime.Now;
            LoadCostCenter();
            LoadAccounts();
            LoadPrintSettings();
            LoadBranches();
        }

        private void Window_Closing(object sender, CancelEventArgs e)
        {
            _conn?.Close();
        }

        #endregion

        #region Load Data

        private void LoadCostCenter()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    "SELECT * FROM cost_center WHERE Code<>0 AND Is_Deleted=0", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count > 0)
                    {
                        cmbCostCenter.ItemsSource       = dt.DefaultView;
                        cmbCostCenter.DisplayMemberPath = "name";
                        cmbCostCenter.SelectedValuePath = "code";
                        cmbCostCenter.SelectedIndex     = -1;
                    }
                }
            }
            catch { }
        }

        private void LoadAccounts()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    "SELECT Code, AName FROM Accounts_Index WHERE type=2 ORDER BY Code", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count > 0)
                    {
                        cmbAccounts.ItemsSource       = dt.DefaultView;
                        cmbAccounts.DisplayMemberPath = "AName";
                        cmbAccounts.SelectedValuePath = "Code";
                        cmbAccounts.SelectedIndex     = -1;
                    }
                }
            }
            catch { }
        }

        private void LoadBranches()
        {
            try
            {
                string branchFilter = "";
                if (MainClass.BranchNo != -1)
                    branchFilter = $" AND id={MainClass.BranchNo}";

                using (var da = new SqlDataAdapter(
                    $"SELECT id, name FROM Branches WHERE IS_Deleted=0 {branchFilter}", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    cmbBranches.ItemsSource       = dt.DefaultView;
                    cmbBranches.DisplayMemberPath = "name";
                    cmbBranches.SelectedValuePath = "id";

                    if (MainClass.BranchNo != -1)
                        cmbBranches.SelectedValue = MainClass.BranchNo;
                    else
                        cmbBranches.SelectedIndex = -1;
                }
            }
            catch { }
        }

        private void LoadPrintSettings()
        {
            try
            {
                using (var da = new SqlDataAdapter(
                    "SELECT * FROM SettingPrint WHERE Inv_Id=14", _conn))
                {
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count == 1)
                    {
                        try { _printType   = Convert.ToInt32(dt.Rows[0]["printType"]);     } catch { }
                        try { _printFooter = Convert.ToBoolean(dt.Rows[0]["PrintFooter"]); } catch { }
                        try { _printHeader = Convert.ToBoolean(dt.Rows[0]["PrintHeader"]); } catch { }
                        try { _printStamp  = Convert.ToBoolean(dt.Rows[0]["PrintStamp"]);  } catch { }
                        try { _defPrinter  = dt.Rows[0]["CasherPrinter"].ToString();       } catch { }
                        try { _printNo     = Convert.ToInt32(dt.Rows[0]["printNo"]);       } catch { }

                        if (string.IsNullOrEmpty(_defPrinter))
                            _defPrinter = Common.GetDefaultPrinter();
                    }
                }
            }
            catch { }
        }

        #endregion

        #region CheckBox Events

        private void chkAll_Changed(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool enabled = (chkAll.IsChecked != true);
            txtDateFrom.IsEnabled  = enabled;
            txtDateTo.IsEnabled    = enabled;
            txtStartTime.IsEnabled = enabled;
            txtEndTime.IsEnabled   = enabled;
        }

        private void chkAllBranches_Changed(object sender, RoutedEventArgs e)
        {
            cmbBranches.IsEnabled = (chkAllBranches.IsChecked != true);
        }

        private void btnAggre_CheckedChanged(object sender, RoutedEventArgs e)
        {
            if (!IsLoaded) return;
            bool isAggre = (btnAggre.IsChecked == true);
            colOperType.Visibility  = isAggre ? Visibility.Collapsed : Visibility.Visible;
            colOperNo.Visibility    = isAggre ? Visibility.Collapsed : Visibility.Visible;
            colDate.Visibility      = isAggre ? Visibility.Collapsed : Visibility.Visible;
            colBtnDetail.Visibility = isAggre ? Visibility.Collapsed : Visibility.Visible;
        }

        #endregion

        #region Cost Center Tree

        // P7-052 fix: إثبات عضوية الشجرة — المركز المختار مع كل أحفاده بكل
        // المستويات؛ العضوية تُبنى مرة واحدة ثم تقيّد بها استعلامات المسارين
        // (كانت قائمة مستوى الأبناء الواحد تسقط الأحفاد وتسقط حركات المركز
        // نفسه متى كان له أبناء، وبوابة GetParent المعطوبة كانت تمر غير
        // التابعين في المسار التجميعي)
        private HashSet<int> GetCostCenterSubtree(int rootCode)
        {
            var members = new HashSet<int> { rootCode };
            var frontier = new List<int> { rootCode };
            try
            {
                if (_conn.State != ConnectionState.Open) _conn.Open();
                while (frontier.Count > 0)
                {
                    var next = new List<int>();
                    foreach (int parentCode in frontier)
                    {
                        using (var cmd = new SqlCommand(
                            "SELECT code FROM cost_center " +
                            "WHERE ParentCode=@parent AND Is_Deleted=0 AND Code<>0", _conn))
                        {
                            cmd.Parameters.Add("@parent", SqlDbType.Int).Value = parentCode;
                            using (var rdr = cmd.ExecuteReader())
                            {
                                while (rdr.Read())
                                {
                                    int code = Convert.ToInt32(rdr["code"]);
                                    if (members.Add(code))
                                        next.Add(code);
                                }
                            }
                        }
                    }
                    frontier = next;
                }
            }
            catch { }
            return members;
        }

        // P7-052 fix: شرط IN معلم — أعضاء الشجرة يقيدون الاستعلام نفسه
        private string BuildCcInClause(HashSet<int> members, out List<SqlParameter> ccParams)
        {
            ccParams = new List<SqlParameter>();
            var names = new List<string>();
            int i = 0;
            foreach (int code in members)
            {
                string name = "@cc" + i;
                ccParams.Add(new SqlParameter(name, SqlDbType.Int) { Value = code });
                names.Add(name);
                i++;
            }
            return string.Join(",", names);
        }

        // P7-053 fix: الافتتاحي مجمَّع لكل (مركز، حساب)
        private class CcInit
        {
            public double Dept;
            public double Credit;
            public string CenterName = "";
            public string AccName    = "";
        }

        private static double ParseD(object v)
        {
            double d;
            double.TryParse(v?.ToString(), out d);
            return d;
        }

        #endregion

        #region Show Button

        private void btnShow_Click(object sender, RoutedEventArgs e)
        {
            if (cmbCostCenter.SelectedIndex == -1)
            {
                DXMessageBox.Show("يرجى اختيار مركز التكلفة",
                    "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (btnDetails.IsChecked == true)
                DetailedResults();
            else if (btnAggre.IsChecked == true)
                ShowResult();
            else
                DXMessageBox.Show("الرجاء اختيار نوع التقرير");
        }

        #endregion

        #region Detailed Results

        // P7-046 fix: النتيجة bool — ويعالج في قائمة محلية ثم ينشر مرة واحدة
        private bool DetailedResults()
        {
            try
            {
                // P7-046 fix: لا نشر تدريجي أثناء الاستعلامات
                var rows = new List<CostCenterRow>();
                ProgressBar1.Value = 0;

                string dateCond   = GetDateCondition();
                string branchCond = GetBranchCondition();
                string accCond    = GetAccountCondition();

                // P7-052 fix: عضوية الشجرة كاملة (المركز المختار + كل أحفاده
                // بكل المستويات) تقيّد الاستعلام مباشرة
                int selectedCc = Convert.ToInt32(cmbCostCenter.SelectedValue);
                var members = GetCostCenterSubtree(selectedCc);
                string ccIn = BuildCcInClause(members, out var ccParams);

                // بناء جدول مؤقت
                var tempTable = new DataTable();
                tempTable.Columns.Add("Code");
                tempTable.Columns.Add("Name");
                tempTable.Columns.Add("DeptInit");
                tempTable.Columns.Add("CreditInit");
                tempTable.Columns.Add("Dept");
                tempTable.Columns.Add("Credit");
                tempTable.Columns.Add("Date");
                tempTable.Columns.Add("DocNo");
                tempTable.Columns.Add("AccName");
                tempTable.Columns.Add("Type");
                tempTable.Columns.Add("EntryGlobalID");

                DateTime fromDt = DateTime.Parse(
                    txtDateFrom.DateTime.ToShortDateString() + " " + (txtStartTime.Text ?? "00:00"));
                DateTime toDt = DateTime.Parse(
                    txtDateTo.DateTime.ToShortDateString() + " " + (txtEndTime.Text ?? "23:59"));

                // حركات الفترة — عضوية الشجرة تقيّد الاستعلام نفسه (استعلام
                // واحد بدل استعلام لكل مركز)، والحساب يُجلب للمطابقة (P7-053)
                var dt4 = new DataTable();
                using (var da = new SqlDataAdapter(
                    $"SELECT Entry_sub.CCcode, cost_center.name, Entry_sub.acc_no, " +
                    $"Entry_sub.dept, Entry_sub.credit, Entry.date, Entry_sub.EntryGlobalID, " +
                    $"Accounts_Index.Aname AS AccName, Entry.type, Entry.doc_no " +
                    $"FROM Entry, Entry_sub, cost_center, Accounts_Index " +
                    $"WHERE {branchCond} Entry.IS_Deleted=0 AND {accCond} " +
                    $"Entry.type<>0 AND Entry.state=1 {dateCond} " +
                    $"AND Entry_sub.acc_no=Accounts_Index.Code " +
                    $"AND Entry.GlobalID=Entry_sub.EntryGlobalID " +
                    $"AND Entry_sub.CCcode=cost_center.code " +
                    $"AND Entry_sub.CCcode IN ({ccIn})", _conn))
                {
                    foreach (SqlParameter p in ccParams)
                        da.SelectCommand.Parameters.Add(p);
                    da.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value = fromDt;
                    da.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value = toDt;
                    da.Fill(dt4);
                }

                // الأرصدة الافتتاحية — بنفس عضوية الشجرة، مجمّعة لكل
                // (مركز، حساب) لا سطراً سطراً (P7-053)
                var dt5 = new DataTable();
                using (var da2 = new SqlDataAdapter(
                    $"SELECT Entry_sub.CCcode, cost_center.name, Entry_sub.acc_no, " +
                    $"SUM(Entry_sub.dept) AS dept, SUM(Entry_sub.credit) AS credit, " +
                    $"Accounts_Index.Aname AS AccName " +
                    $"FROM Entry, Entry_sub, cost_center, Accounts_Index " +
                    $"WHERE {branchCond} Entry.IS_Deleted=0 AND {accCond} " +
                    $"Entry.type=0 AND Entry.state=1 {dateCond} " +
                    $"AND Entry_sub.acc_no=Accounts_Index.Code " +
                    $"AND Entry.GlobalID=Entry_sub.EntryGlobalID " +
                    $"AND Entry_sub.CCcode=cost_center.code " +
                    $"AND Entry_sub.CCcode IN ({ccIn}) " +
                    $"GROUP BY Entry_sub.CCcode, Entry_sub.acc_no, " +
                    $"Accounts_Index.Aname, cost_center.name", _conn))
                {
                    foreach (SqlParameter p in ccParams)
                        da2.SelectCommand.Parameters.Add(p);
                    da2.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value
                        = txtDateFrom.DateTime.ToShortDateString();
                    da2.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value
                        = txtDateTo.DateTime.AddHours(24);
                    da2.Fill(dt5);
                }

                // P7-053 fix: الافتتاحي يطابق المركز والحساب معاً (كان يطابق
                // المركز وحده فيلتقط افتتاحي أول حساب ويكرره على صفوف حسابات
                // المركز الأخرى)
                var initMap = new Dictionary<string, CcInit>();
                foreach (DataRow r in dt5.Rows)
                {
                    string key = r["CCcode"] + "|" + r["acc_no"];
                    CcInit accInit;
                    if (!initMap.TryGetValue(key, out accInit))
                    {
                        accInit = new CcInit
                        {
                            CenterName = r["name"].ToString(),
                            AccName    = r["AccName"].ToString()
                        };
                        initMap[key] = accInit;
                    }
                    accInit.Dept   += ParseD(r["dept"]);
                    accInit.Credit += ParseD(r["credit"]);
                }

                ProgressBar1.Maximum = dt4.Rows.Count > 0 ? dt4.Rows.Count : 1;

                var seenKeys = new HashSet<string>();
                foreach (DataRow row in dt4.Rows)
                {
                    string key = row["CCcode"] + "|" + row["acc_no"];
                    seenKeys.Add(key);

                    double deptInit = 0, creditInit = 0;
                    CcInit accInit;
                    if (initMap.TryGetValue(key, out accInit))
                    {
                        deptInit   = accInit.Dept;
                        creditInit = accInit.Credit;
                    }

                    tempTable.Rows.Add(
                        row["CCcode"], row["name"],
                        deptInit, creditInit, row["dept"], row["credit"],
                        row["date"], row["doc_no"], row["AccName"],
                        row["type"], row["EntryGlobalID"]);

                    ProgressBar1.Value++;
                }

                // P7-053 fix: الافتتاحي بلا حركة في الفترة ينشر صفوفه بحركة
                // صفر (كان يسقط كلياً — مركز/حساب رصيده الافتتاحي وحده لا
                // يظهر في التقرير أبداً)
                foreach (var kv in initMap)
                {
                    if (seenKeys.Contains(kv.Key)) continue;

                    string ccCode = kv.Key.Split('|')[0];
                    tempTable.Rows.Add(
                        ccCode, kv.Value.CenterName,
                        kv.Value.Dept, kv.Value.Credit, 0, 0,
                        DBNull.Value, DBNull.Value, kv.Value.AccName,
                        DBNull.Value, DBNull.Value);
                }

                // بناء النتائج
                ProgressBar1.Maximum = tempTable.Rows.Count > 0 ? tempTable.Rows.Count : 1;
                ProgressBar1.Value   = 0;

                foreach (DataRow row in tempTable.Rows)
                {
                    ProgressBar1.Value++;
                    ProcessAndAddRow(row, isDetailed: true, rows);
                }

                // ══ نقطة النشر الواحدة (P7-046) ══
                _dataSource.Clear();
                foreach (var r in rows) _dataSource.Add(r);

                lblCount.Text = _dataSource.Count.ToString();
                return true;
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
                return false;
            }
        }

        #endregion

        #region Show Result (Aggregated)

        // P7-046 fix: النتيجة bool — اكتمل النشر الذري أم لا (بوابة الطباعة P7-045)
        private bool ShowResult()
        {
            try
            {
                // P7-046 fix: التجميع في قائمة محلية — لا نشر تدريجي؛ فشل مصدر
                // متأخر يترك نتيجة الشاشة السابقة كاملة متسقة
                var rows = new List<CostCenterRow>();
                ProgressBar1.Value = 0;

                string dateCond   = GetDateCondition();
                string branchCond = GetBranchCondition();
                string accCond    = GetAccountCondition();

                // P7-052 fix: عضوية الشجرة تقيّد الاستعلام نفسه — كان المسار
                // التجميعي بلا مرشح CCcode إطلاقاً لمراكز النوع 1 فيجمع كل
                // مراكز القاعدة غير التابعة للمركز المختار، وبوابة GetParent
                // المعطوبة كانت تمر الجميع
                int selectedCc = Convert.ToInt32(cmbCostCenter.SelectedValue);
                var members = GetCostCenterSubtree(selectedCc);
                string ccIn = BuildCcInClause(members, out var ccParams);

                var dt4 = new DataTable();
                using (var da = new SqlDataAdapter(
                    $"SELECT Entry_sub.CCcode, cost_center.name, Entry_sub.acc_no, " +
                    $"SUM(Entry_sub.dept) AS dept, SUM(Entry_sub.credit) AS credit, " +
                    $"Accounts_Index.Aname AS AccName " +
                    $"FROM Entry, Entry_sub, cost_center, Accounts_Index " +
                    $"WHERE {branchCond} Entry.IS_Deleted=0 AND {accCond} " +
                    $"Entry.type<>0 AND Entry.state=1 {dateCond} " +
                    $"AND Entry_sub.CCcode IN ({ccIn}) " +
                    $"AND Entry_sub.acc_no=Accounts_Index.Code " +
                    $"AND Entry.GlobalID=Entry_sub.EntryGlobalID " +
                    $"AND Entry_sub.CCcode=cost_center.code " +
                    $"GROUP BY Entry_sub.CCcode, Entry_sub.acc_no, " +
                    $"Accounts_Index.Aname, cost_center.name",
                    _conn))
                {
                    foreach (SqlParameter p in ccParams)
                        da.SelectCommand.Parameters.Add(p);
                    da.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value
                        = txtDateFrom.DateTime.ToShortDateString();
                    da.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value
                        = txtDateTo.DateTime.AddHours(24);
                    da.Fill(dt4);
                }

                var dt5 = new DataTable();
                using (var da2 = new SqlDataAdapter(
                    $"SELECT Entry_sub.CCcode, cost_center.name, Entry_sub.acc_no, " +
                    $"SUM(Entry_sub.dept) AS dept, SUM(Entry_sub.credit) AS credit, " +
                    $"Accounts_Index.Aname AS AccName " +
                    $"FROM Entry, Entry_sub, cost_center, Accounts_Index " +
                    $"WHERE {branchCond} Entry.IS_Deleted=0 AND {accCond} " +
                    $"Entry.type=0 AND Entry.state=1 {dateCond} " +
                    $"AND Entry_sub.CCcode IN ({ccIn}) " +
                    $"AND Entry_sub.acc_no=Accounts_Index.Code " +
                    $"AND Entry.GlobalID=Entry_sub.EntryGlobalID " +
                    $"AND Entry_sub.CCcode=cost_center.code " +
                    $"GROUP BY Entry_sub.CCcode, Entry_sub.acc_no, " +
                    $"Accounts_Index.Aname, cost_center.name",
                    _conn))
                {
                    foreach (SqlParameter p in ccParams)
                        da2.SelectCommand.Parameters.Add(p);
                    da2.SelectCommand.Parameters.Add("@date1", SqlDbType.DateTime).Value
                        = txtDateFrom.DateTime.ToShortDateString();
                    da2.SelectCommand.Parameters.Add("@date2", SqlDbType.DateTime).Value
                        = txtDateTo.DateTime.AddHours(24);
                    da2.Fill(dt5);
                }

                // P7-053 fix: الافتتاحي مجمّع لكل (مركز، حساب) — كان يطابق
                // المركز وحده فيكرر افتتاحي أول حساب على كل حسابات المركز
                var initMap = new Dictionary<string, CcInit>();
                foreach (DataRow r in dt5.Rows)
                {
                    string key = r["CCcode"] + "|" + r["acc_no"];
                    CcInit accInit;
                    if (!initMap.TryGetValue(key, out accInit))
                    {
                        accInit = new CcInit
                        {
                            CenterName = r["name"].ToString(),
                            AccName    = r["AccName"].ToString()
                        };
                        initMap[key] = accInit;
                    }
                    accInit.Dept   += ParseD(r["dept"]);
                    accInit.Credit += ParseD(r["credit"]);
                }

                var tempTable = new DataTable();
                tempTable.Columns.Add("Code");
                tempTable.Columns.Add("Name");
                tempTable.Columns.Add("DeptInit");
                tempTable.Columns.Add("CreditInit");
                tempTable.Columns.Add("Dept");
                tempTable.Columns.Add("Credit");
                tempTable.Columns.Add("AccName");

                ProgressBar1.Maximum = dt4.Rows.Count > 0 ? dt4.Rows.Count : 1;

                var seenKeys = new HashSet<string>();
                foreach (DataRow row in dt4.Rows)
                {
                    string key = row["CCcode"] + "|" + row["acc_no"];
                    seenKeys.Add(key);

                    double deptInit = 0, creditInit = 0;
                    CcInit accInit;
                    if (initMap.TryGetValue(key, out accInit))
                    {
                        deptInit   = accInit.Dept;
                        creditInit = accInit.Credit;
                    }

                    tempTable.Rows.Add(row["CCcode"], row["name"],
                        deptInit, creditInit, row["dept"], row["credit"], row["AccName"]);
                    ProgressBar1.Value++;
                }

                // P7-053 fix: الافتتاحي بلا حركة في الفترة ينشر صفوفه بحركة
                // صفر (كان يسقط كلياً)
                foreach (var kv in initMap)
                {
                    if (seenKeys.Contains(kv.Key)) continue;

                    string ccCode = kv.Key.Split('|')[0];
                    tempTable.Rows.Add(ccCode, kv.Value.CenterName,
                        kv.Value.Dept, kv.Value.Credit, 0, 0, kv.Value.AccName);
                }

                ProgressBar1.Maximum = tempTable.Rows.Count > 0 ? tempTable.Rows.Count : 1;
                ProgressBar1.Value   = 0;

                foreach (DataRow row in tempTable.Rows)
                {
                    ProgressBar1.Value++;

                    double deptInit   = Math.Round(Convert.ToDouble(row["DeptInit"]),   2);
                    double creditInit = Math.Round(Convert.ToDouble(row["CreditInit"]), 2);
                    double dept       = Math.Round(Convert.ToDouble(row["Dept"]),       2);
                    double credit     = Math.Round(Convert.ToDouble(row["Credit"]),     2);

                    double deptBlc, creditBlc;
                    if (dept >= credit)
                    { deptBlc = dept - credit; creditBlc = 0; }
                    else
                    { deptBlc = 0; creditBlc = credit - dept; }

                    double deptFinal   = deptInit + deptBlc;
                    double creditFinal = creditInit + creditBlc;

                    double finalDebt, finalCredit;
                    if (deptFinal >= creditFinal)
                    { finalDebt = Math.Round(deptFinal - creditFinal, 2); finalCredit = 0; }
                    else
                    { finalDebt = 0; finalCredit = Math.Round(creditFinal - deptFinal, 2); }

                    rows.Add(new CostCenterRow
                    {
                        DgvAccount          = row["Code"].ToString(),
                        DgvCostCenter       = row["Name"].ToString(),
                        DgvDeptIntial       = deptInit,
                        DgvCreditIntial     = creditInit,
                        DgvDebtorMovement   = dept,
                        DgvCreditorMovement = credit,
                        DgvDeptBlc          = deptBlc,
                        DgvCreditBlc        = creditBlc,
                        DgvDeptFinal        = finalDebt,
                        DgvCreditFinal      = finalCredit,
                        DgvAccName          = row["AccName"].ToString(),
                        DgvOperationType    = "",
                        DgvOperationNo      = "",
                        DgvDate             = "",
                        DgvEntryGlobalId    = ""
                    });
                }

                // ══ نقطة النشر الواحدة (P7-046) ══
                _dataSource.Clear();
                foreach (var r in rows) _dataSource.Add(r);

                lblCount.Text = _dataSource.Count.ToString();
                return true;
            }
            catch (Exception ex)
            {
                DXMessageBox.Show(ex.Message);
                return false;
            }
        }

        private void ProcessAndAddRow(DataRow row, bool isDetailed,
            List<CostCenterRow> target)
        {
            try
            {
                double deptInit   = Math.Round(Convert.ToDouble(row["DeptInit"]),   2);
                double creditInit = Math.Round(Convert.ToDouble(row["CreditInit"]), 2);
                double dept       = Math.Round(Convert.ToDouble(row["Dept"]),       2);
                double credit     = Math.Round(Convert.ToDouble(row["Credit"]),     2);

                double deptBlc, creditBlc;
                if (dept >= credit)
                { deptBlc = dept - credit; creditBlc = 0; }
                else
                { deptBlc = 0; creditBlc = credit - dept; }

                double deptFinal   = deptInit + deptBlc;
                double creditFinal = creditInit + creditBlc;

                double finalDebt, finalCredit;
                if (deptFinal >= creditFinal)
                { finalDebt = Math.Round(deptFinal - creditFinal, 2); finalCredit = 0; }
                else
                { finalDebt = 0; finalCredit = Math.Round(creditFinal - deptFinal, 2); }

                string dateStr = "";
                string opType  = "";
                string opNo    = "";
                string globalId = "";

                if (isDetailed)
                {
                    try { dateStr = Convert.ToDateTime(row["Date"]).ToShortDateString(); } catch { }
                    try { int.TryParse(row["Type"].ToString(), out int t); opType = Common.ResrirectionType(t); } catch { }
                    try { opNo    = row["DocNo"].ToString(); } catch { }
                    try { globalId = row["EntryGlobalID"].ToString(); } catch { }
                }

                target.Add(new CostCenterRow
                {
                    DgvAccount          = row["Code"].ToString(),
                    DgvCostCenter       = row["Name"].ToString(),
                    DgvDeptIntial       = deptInit,
                    DgvCreditIntial     = creditInit,
                    DgvDebtorMovement   = dept,
                    DgvCreditorMovement = credit,
                    DgvDeptBlc          = deptBlc,
                    DgvCreditBlc        = creditBlc,
                    DgvDeptFinal        = finalDebt,
                    DgvCreditFinal      = finalCredit,
                    DgvAccName          = row["AccName"].ToString(),
                    DgvOperationType    = opType,
                    DgvOperationNo      = opNo,
                    DgvDate             = dateStr,
                    DgvEntryGlobalId    = globalId
                });
            }
            catch { }
        }

        #endregion

        #region Helper Conditions

        private string GetDateCondition()
        {
            if (chkAll.IsChecked != true)
                return " AND Entry.date>=@date1 AND Entry.date<=@date2 ";
            return "";
        }

        private string GetBranchCondition()
        {
            if (chkAllBranches.IsChecked != true && cmbBranches.SelectedIndex != -1)
                return $"Entry.branch={cmbBranches.SelectedValue} AND ";
            return "";
        }

        private string GetAccountCondition()
        {
            if (cmbAccounts.SelectedIndex != -1)
                return $" Entry_sub.acc_no={cmbAccounts.SelectedValue} AND ";
            return "";
        }

        #endregion

        #region Button Events

        private void BtnDetail_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (sender is Button btn && btn.Tag is string globalId)
                    EntryOper.ShowEntrySource(globalId);
            }
            catch { }
        }

        private void btnPrint_Click(object sender, RoutedEventArgs e) => PrintDevexpress(1);
        private void btnPreview_Click(object sender, RoutedEventArgs e) => PrintDevexpress(2);
        private void btnClose_Click(object sender, RoutedEventArgs e) => this.Close();

        private void btnExportExcel_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (_dataSource.Count == 0) return;

                // P7-048/049 fix: ترميز الخلايا الموحّد — الفاصلة والاقتباس
                // والأسطر وبادئات الصيغ وقيم الألوف كلها خلية واحدة سليمة
                string fileName = "CostCenter_Export.csv";
                DelimitedExport.WriteFile(fileName,
                    new[]
                    {
                        "الرمز", "مركز التكلفة", "رصيد افتتاحي مدين", "رصيد افتتاحي دائن",
                        "حركة مدين", "حركة دائن", "رصيد مدين", "رصيد دائن",
                        "رصيد ختامي مدين", "رصيد ختامي دائن", "اسم الحساب",
                        "العملية", "رقم العملية", "التاريخ"
                    },
                    _dataSource.Select(row => new[]
                    {
                        row.DgvAccount.ToString(),
                        row.DgvCostCenter,
                        row.DgvDeptIntial.ToString("N2"),
                        row.DgvCreditIntial.ToString("N2"),
                        row.DgvDebtorMovement.ToString("N2"),
                        row.DgvCreditorMovement.ToString("N2"),
                        row.DgvDeptBlc.ToString("N2"),
                        row.DgvCreditBlc.ToString("N2"),
                        row.DgvDeptFinal.ToString("N2"),
                        row.DgvCreditFinal.ToString("N2"),
                        row.DgvAccName,
                        row.DgvOperationType,
                        row.DgvOperationNo,
                        row.DgvDate
                    }));

                System.Diagnostics.Process.Start(
                    new System.Diagnostics.ProcessStartInfo(fileName)
                    { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                DXMessageBox.Show("خطأ في التصدير: " + ex.Message);
            }
        }

        #endregion

        #region Print

        private DataSet BindToData()
        {
            var list = new List<RestrictionData>();

            foreach (var row in _dataSource)
            {
                list.Add(new RestrictionData
                {
                    MainAccountName  = cmbAccounts.Text,
                    MainAccountCode  = cmbAccounts.SelectedValue?.ToString() ?? "",
                    MainCostCenter   = cmbCostCenter.Text,
                    CodeMainCostCenter = cmbCostCenter.SelectedValue?.ToString() ?? "",
                    CodeCostCenter   = row.DgvAccount,
                    CostCenter       = row.DgvCostCenter,
                    DeptIntial       = row.DgvDeptIntial.ToString("N2"),
                    CreditIntial     = row.DgvCreditIntial.ToString("N2"),
                    Dept             = row.DgvDebtorMovement.ToString("N2"),
                    Credit           = row.DgvCreditorMovement.ToString("N2"),
                    DeptBalance      = row.DgvDeptBlc.ToString("N2"),
                    CreditBalance    = row.DgvCreditBlc.ToString("N2"),
                    DeptFinal        = row.DgvDeptFinal.ToString("N2"),
                    CreditFinal      = row.DgvCreditFinal.ToString("N2"),
                    AccountName      = row.DgvAccName,
                    InvoiceType      = row.DgvOperationType,
                    InvNo            = row.DgvOperationNo,
                    RestDate         = row.DgvDate,
                    RestrType        = "تقرير مراكز التكلفة",
                    FromDate         = txtDateFrom.DateTime.ToString(),
                    ToDate           = txtDateTo.DateTime.ToString(),
                    User             = Common.GetEmpName(MainClass.EmpNo),
                    PrintDate        = DateTime.Now.ToShortDateString()
                });
            }

            var ds = new DataSet("Name");
            ds.Tables.Add(global::UtilitiesProj.Common.ToDataTable(list));
            return ds;
        }

        private void PrintDevexpress(int printType)
        {
            // P7-045 fix: إعادة الحساب بمعايير الواجهة الحالية قبل الربط —
            // بالمسار نفسه الذي يعرضه الزر (تفصيلي/تجميعي)؛ والنتيجة الفارغة
            // يمسكها فحص الجدول الفارغ أدناه
            if (btnDetails.IsChecked == true)
            {
                if (!DetailedResults()) return;
            }
            else if (!ShowResult()) return;

            _rptUrl = MainClass.ReportsPath;
            _rptName = (btnDetails.IsChecked == true)
                ? "RptCostCenterDetails.repx"
                : "RptCostCenter.repx";
            _defPrinter = MainClass.ReportsPrinter;

            if (_dataSource.Count == 0)
            {
                DXMessageBox.Show("لا توجد عمليات بالجدول",
                    "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            if (string.IsNullOrEmpty(_rptUrl))
            {
                DXMessageBox.Show("يجب تحديد مسار التقرير",
                    "", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            string fullPath = Path.Combine(_rptUrl, _rptName);
            if (!Directory.Exists(_rptUrl) || !File.Exists(fullPath))
            {
                DXMessageBox.Show("المسار الحالي للتقارير غير موجود أو تم تعديله",
                    "خطأ", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            try
            {
                var report = XtraReport.FromFile(fullPath);
                report.DataSource = BindToData();

                string headerPath = Path.Combine(_rptUrl, "header.repx");
                if (File.Exists(headerPath))
                {
                    var headerRpt = XtraReport.FromFile(headerPath);
                    headerRpt.DataSource = Common.FoundationInfoDT;
                    var subHeader = report.FindControl("headerRpt", true) as XRSubreport;
                    if (subHeader != null) subHeader.ReportSource = headerRpt;
                }

                string footerPath = Path.Combine(_rptUrl, "footer.repx");
                if (File.Exists(footerPath))
                {
                    var footerRpt = XtraReport.FromFile(footerPath);
                    footerRpt.DataSource = Common.FoundationInfoDT;
                    var subFooter = report.FindControl("footerRpt", true) as XRSubreport;
                    if (subFooter != null) subFooter.ReportSource = footerRpt;
                }

                if (string.IsNullOrEmpty(_defPrinter))
                {
                    DXMessageBox.Show("يجب تحديد الطابعة من الإعدادات",
                        "", MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                report.PrinterName = _defPrinter;
                if (printType == 1)
                    for (int i = 0; i < _printNo; i++) report.Print();
                else
                    report.ShowPreviewDialog();

                report.Dispose();
            }
            catch (Exception ex)
            {
                DXMessageBox.Show("خطأ في الطباعة: " + ex.Message);
            }
        }

        #endregion

        #region Model

        public class CostCenterRow
        {
            public string DgvAccount          { get; set; }
            public string DgvCostCenter       { get; set; }
            public double DgvDeptIntial       { get; set; }
            public double DgvCreditIntial     { get; set; }
            public double DgvDebtorMovement   { get; set; }
            public double DgvCreditorMovement { get; set; }
            public double DgvDeptBlc          { get; set; }
            public double DgvCreditBlc        { get; set; }
            public double DgvDeptFinal        { get; set; }
            public double DgvCreditFinal      { get; set; }
            public string DgvAccName          { get; set; }
            public string DgvOperationType    { get; set; }
            public string DgvOperationNo      { get; set; }
            public string DgvDate             { get; set; }
            public string DgvEntryGlobalId    { get; set; }
        }

        #endregion
    }
}