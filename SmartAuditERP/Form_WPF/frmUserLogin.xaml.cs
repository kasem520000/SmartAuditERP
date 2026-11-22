using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Data.SqlClient;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using DevExpress.Xpf.Core;
using log4net;
using Newtonsoft.Json;
using SmartAuditERP;
using drHamiedNotify;
using UtilitiesProj;
using Ws_Auditor;
using Ws_Auditor.CashierSerivce;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmUserLogin : ThemedWindow
    {
        #region Fields

        public SqlConnection conn;
        public SqlConnection conn1;

        public string txtDatabase;
        public int SecureCode;
        public string NetUserid;
        public string Netpwd;
        public int conn_type;
        public DateTime datelogin;
        public bool SuccessLogin;
        public bool ISExit;
        public AndroidConfig nss;

        private static readonly ILog Logger =
            LogManager.GetLogger(Environment.MachineName);

        public nService nssd;
        public RSAEncryptDecrypt RSAkeysnssd;

        private int branchId;


        public string SelectedBranch => cmbBranches.Text;
        public string SelectedDatabase => cmbDatabases.Text;
        public string VersionText => lblVersion.Text;
        public int ConnectionType => conn_type;
        #endregion

        #region Constructor

        public frmUserLogin()
        {
            InitializeComponent();

            conn = MainClass.ConnObj();
            conn1 = MainClass.ConnObj();
            txtDatabase = "";
            NetUserid = "";
            Netpwd = "";
            conn_type = 1;
            SuccessLogin = false;
            ISExit = false;
            nss = new AndroidConfig();
            nssd = new nService();
            RSAkeysnssd = new RSAEncryptDecrypt();
            branchId = 1;

            this.Loaded += Window_Loaded;
            this.Closing += Window_Closing;
            this.KeyDown += Window_KeyDown;

            this.FlowDirection = FlowDirection.LeftToRight;
        }

        #endregion

        #region Window Events

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            try
            {
                cmblanguages.SelectedIndex = 0;
                MainClass.EmpNo = -1;
                LoadData();
                this.Activate();
                MainClass.EmpNo = -1;

                var versionInfo = Common.CurrentVersion();
                lblVersion.Text = versionInfo.VersionText;
                lblPublishDate.Text = versionInfo.PublishDate;
                MainClass.CurrentVersion = versionInfo.VersionText;
                try
                {
                    Common.SalesmanSetting();
                    if (MainClass.LoginBG != null)
                    {
                        // يمكن تطبيق الخلفية عبر ImageBrush إذا أردت
                    }
                }
                catch (Exception ex)
                {
                    Logger.Error(ex);
                }
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        private void Window_Closing(object sender, CancelEventArgs e)
        {
            // لا شيء
        }

        private void Window_KeyDown(object sender, KeyEventArgs e)
        {
            try
            {
                if (e.Key == Key.F4)
                    e.Handled = true;
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        #endregion

        #region Login Logic

        public async void Login(int type)
        {
            try
            {
                // P1-017 fix: لا نسخة Home جديدة هنا — المعروضة هي MainWindow.
                var Home = System.Windows.Application.Current?.MainWindow as Home;
                var frmSecurityPnl = new frmSecurityPnl();
                if (type == 1)
                {
                    if (cmbDatabases.SelectedIndex == -1)
                    {
                        MessageBox.Show("يجب اختيار الملف", "",
                            MessageBoxButton.OK, MessageBoxImage.Information);
                        cmbDatabases.Focus();
                        return;
                    }
                    if (cmbBranches.SelectedValue == null)
                    {
                        MessageBox.Show("يجب اختيار الفرع", "",
                            MessageBoxButton.OK, MessageBoxImage.Information);
                        cmbBranches.Focus();
                        return;
                    }
                    if (string.IsNullOrWhiteSpace(txtUser.Text))
                    {
                        MessageBox.Show("ادخل اسم المستخدم", "",
                            MessageBoxButton.OK, MessageBoxImage.Information);
                        txtUser.Focus();
                        return;
                    }
                    if (string.IsNullOrWhiteSpace(txtPwd.Password))
                    {
                        MessageBox.Show("ادخل كلمة المرور", "",
                            MessageBoxButton.OK, MessageBoxImage.Information);
                        txtPwd.Focus();
                        return;
                    }

                    txtDatabase = cmbDatabases.SelectedValue?.ToString().Trim() ?? "";
                }

                // بناء سلسلة الاتصال
                if (!string.IsNullOrEmpty(MainClass.Server))
                {
                    BuildConnectionStrings();
                }

                // P1-008 fix: أُزيل «دخول الدعم الخاص» باسم auditor وكلمة قابلة للتخمين
                // (auditor+السنة+الشهر). لا مسار دخول خاص بعد الآن: كل مستخدم — بمن فيهم
                // حساب دعم إن احتجه الموزّع — يُنشأ في جدول Users بكلمة مجزأة كبقية
                // المستخدمين، ويُدار من شاشة المستخدمين.
                bool SecureLogin = false;

                // اللغة
                MainClass.Language = cmblanguages.SelectedIndex == 0 ? "ar" : "en-us";

                if (MainClass.IsTrial && Home != null)
                    Home.lblIsTrial1.Text = "نسخة تجريبية";

                MainClass.conn = conn;
                MainClass.Conn_type = conn_type;
                MainClass.DataBaseName = cmbDatabases.Text;

                int selectedBranch = 0;
                if (cmbBranches.SelectedValue != null)
                    int.TryParse(cmbBranches.SelectedValue.ToString(), out selectedBranch);

                // تسجيل الدخول (أونلاين أو أوفلاين)
                bool loginSuccess;
                if (Sync.CheckSync(selectedBranch) && !SecureLogin)
                {
                    loginSuccess = Sync.BranchType == 4
                        ? await OnlineLogin(type)
                        : await OfflineLogin(SecureLogin, type);
                }
                else
                {
                    loginSuccess = await OfflineLogin(SecureLogin, type);
                }

                if (!loginSuccess) return;

                // تحديث Log
                if (!string.IsNullOrEmpty(MainClass.Server))
                {
                    string conn3 = BuildLogConnectionString();
                    Common.SetUpLogDbConnection(conn3, "log4net.config");
                    ThreadContext.Properties["EmpID"] = MainClass.EmpNo;
                    Logger.Info("تم تسجيل الدخول للمستخدم " + MainClass.UserName);
                }

                // تحديث شريط الحالة في النافذة الرئيسية
                UpdateHomeStatusBar();

                // حفظ بيانات الجلسة
                SaveStartupData();

                frmSecurityPnl.Secured = true;
                Home?.Activate();
                datelogin = DateTime.Now;
                txtPwd.Clear();
                // في frmUserLogin.cs - دالة Login بعد نجاح الدخول
                //datelogin = DateTime.Now;
                MainClass.LoginDate = datelogin; // ✅ حفظ التاريخ في MainClass
                ConnectMQTList();

                if (type == 1)
                    this.Hide();
            }
            catch (Exception ex)
            {
                string msg = MainClass.Language == "ar"
                    ? "حدث خطأ أثناء الدخول تفاصيل الخطأ: " + ex.Message
                    : "Error in login Error details: " + ex.Message;
                MessageBox.Show(msg, "خطأ", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                this.Cursor = Cursors.Arrow;
            }
        }

        private void BuildConnectionStrings()
        {
            if (conn_type == 1)
            {
                if (MainClass.UseServerAuth)
                {
                    string cs = $"server={MainClass.Server};database={txtDatabase};" +
                                $"MultipleActiveResultSets=true;" +
                                $"user id={MainClass.NetUserId}; pwd={MainClass.NetPwd}";
                    conn = MainClass.CreateSqlConnection(cs);
                    conn1 = MainClass.CreateSqlConnection(cs);
                    MainClass.connstr = cs;
                }
                else
                {
                    string cs = $"server={MainClass.Server};database={txtDatabase};" +
                                $"trusted_connection=true;MultipleActiveResultSets=true;";
                    conn = MainClass.CreateSqlConnection(cs);
                    conn1 = MainClass.CreateSqlConnection(cs);
                    MainClass.connstr = cs;
                }
            }
            else
            {
                string cs = $"server={MainClass.Server};database={txtDatabase};" +
                            $"MultipleActiveResultSets=true;" +
                            $"user id={MainClass.NetUserId}; pwd={MainClass.NetPwd}";
                conn = MainClass.CreateSqlConnection(cs);
                conn1 = MainClass.CreateSqlConnection(cs);
                MainClass.connstr = cs;
            }
        }

        private string BuildLogConnectionString()
        {
            if (conn_type == 1 && MainClass.UseServerAuth)
                return $"server={MainClass.Server};database={txtDatabase};" +
                       $"user id={NetUserid}; pwd={Netpwd}";

            if (conn_type == 2)
                return $"server={MainClass.Server};database={txtDatabase};" +
                       $"user id={NetUserid}; pwd={Netpwd}";

            return $"Data Source={MainClass.Server}; " +
                   $"Initial Catalog={MainClass.Database};Integrated Security=True";
        }

        private void UpdateHomeStatusBar()
        {
            // P1-017 fix: التحديث على نافذة Home المعروضة فعلاً (MainWindow من WPF)،
            // لا على نسخة جديدة لم تُعرض أبداً فتضيع التحديثات.
            var Home = System.Windows.Application.Current?.MainWindow as Home;
            if (Home == null) return;
            if (MainClass.Language == "en-us")
            {
                Home.txtLoggedUser1.Text = "User: " + MainClass.UserName;
                Home.lblBranch1.Text = "Branch: " + cmbBranches.Text;
                Home.lbldbName.Text = "Database: " + cmbDatabases.Text;
                Home.lblVersion.Text = "Version: " + lblVersion.Text;
                Home.lblIsTrial1.Text = "Trial";
            }
            else
            {
                Home.txtLoggedUser1.Text = "المستخدم: " + MainClass.UserName;
                Home.lblBranch1.Text = "الفرع: " + cmbBranches.Text;
                Home.lbldbName.Text = "قاعدة البيانات: " + cmbDatabases.Text;
                Home.lblVersion.Text = "النسخة: " + lblVersion.Text;

                if (conn_type == 2)
                {
                    Home.lblDeviceType.Text = "نوع الجهاز: طرفي";
                    Home.lblDeviceType.Visibility = Visibility.Visible;
                }
                else
                {
                    Home.lblDeviceType.Visibility = Visibility.Collapsed;
                    Home.lblDeviceType.Text = "";
                }
            }
            System.Diagnostics.Debug.WriteLine("User: " + Home.txtLoggedUser1.Text);
            System.Diagnostics.Debug.WriteLine("Branch: " + Home.lblBranch1.Text);
            System.Diagnostics.Debug.WriteLine("Database: " + Home.lbldbName.Text);
            System.Diagnostics.Debug.WriteLine("Version: " + Home.lblVersion.Text);
        }

        private void SaveStartupData()
        {
            // P1-009 fix: كلمتا المرور (التطبيق والخادم) لا تُكتبان نصاً صريحاً أبداً —
            // تُشفّران DPAPI (نطاق مستخدم ويندوز الحالي) قبل الحفظ.
            // P1-019 fix: الحفظ في %APPDATA%/SmartAuditERP لا في مجلد البرنامج.
            var startupData = new StartupData
            {
                Remember = chkRemember.IsChecked == true,
                ConnType = MainClass.Conn_type.ToString(),
                Server = MainClass.Server,
                DatabaseName = cmbDatabases.SelectedValue?.ToString() ?? "",
                Branch = cmbBranches.SelectedValue?.ToString() ?? "",
                UserName = txtUser.Text,
                Password = Class.Security.SecretProtector.Protect(txtPwd.Password),
                Language = cmblanguages.SelectedIndex.ToString()
            };

            if (conn_type == 1 && MainClass.UseServerAuth)
            {
                startupData.ServerUserName = MainClass.NetUserId;
                startupData.ServerPassword = Class.Security.SecretProtector.Protect(MainClass.NetPwd);
            }
            if (conn_type == 2)
            {
                startupData.ServerUserName = MainClass.NetUserId;
                startupData.ServerPassword = Class.Security.SecretProtector.Protect(MainClass.NetPwd);
            }

            string json = JsonConvert.SerializeObject(startupData, Formatting.Indented);
            Directory.CreateDirectory(StartupDataDir);
            File.WriteAllText(StartupDataPath, json);
        }

        #endregion

        #region Online / Offline Login

        public async Task<bool> OnlineLogin(int type)
        {
            try
            {
                if (MainClass.CheckForInternetConnection())
                {
                    var log = new ClsLogin(Sync.APIUrl, "1");
                    var loginTask = Task.Run(() => log.LoginAsync(txtUser.Text, txtPwd.Password));
                    var completed = await Task.WhenAny(loginTask, Task.Delay(5000));

                    if (completed == loginTask)
                    {
                        var frmSecurityPnl = new frmSecurityPnl();
                        User.CurrentCloudUser = await loginTask;
                        if (User.CurrentCloudUser == null)
                        {
                            string msg = cmblanguages.SelectedIndex == 0
                                ? "دخول غير صحيح" : "Failed to login";
                            MessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Information);
                            frmSecurityPnl.Secured = false;
                            txtPwd.Clear();
                            return false;
                        }

                        MainClass.UserID = User.CurrentCloudUser.UserID;
                        MainClass.EmpNo = User.CurrentCloudUser.UserID;
                        MainClass.UserName = User.CurrentCloudUser.UserName;
                        MainClass.BranchNo = User.CurrentCloudUser.Branch_ID.Value;
                        MainClass.UserTreasury = 1;
                        return true;
                    }
                    else
                    {
                        return await OfflineLogin(false, type);
                    }
                }
                else
                {
                    return await OfflineLogin(false, type);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("An error occurred during login. Please try again.",
                    "", MessageBoxButton.OK, MessageBoxImage.Error);
                Logger.Error(ex);
                return false;
            }
        }

        public async Task<bool> OfflineLogin(bool SecureLogin, int Type)
        {
            try
            {
                var frmSecurityPnl = new frmSecurityPnl();
                SqlDataAdapter da;

                if (Type == 1)
                {
                    // P1-010 fix: أُزيل الباب الخلفي SecureLogin?"auditor" — كلمة الدخول
                    // هي ما أدخله المستخدم دائماً، ولا كلمة صلبة في أي مسار.
                    string pwd = txtPwd.Password;
                    da = new SqlDataAdapter(
                        "select * from Users where username=@Username and IS_Deleted=0",
                        conn);
                    da.SelectCommand.Parameters.AddWithValue("@Username", txtUser.Text);

                    DataTable dtUser = new DataTable();
                    da.Fill(dtUser);

                    if (dtUser.Rows.Count == 0)
                    {
                        frmSecurityPnl.Secured = false;
                        string msg = MainClass.Language == "ar" ? "دخول غير صحيح" : "Error login";
                        MessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Information);
                        txtPwd.Clear();
                        txtUser.Focus();
                        return false;
                    }

                    // P1-010 fix: تحقق التجزئة أولاً (pwd_hash) ثم مهاجرة النص القديم لمرة واحدة
                    DataRow userRow = null;
                    foreach (DataRow r in dtUser.Rows)
                    {
                        string storedHash = r["pwd_hash"] as string;
                        if (!string.IsNullOrEmpty(storedHash) &&
                            Class.Security.PasswordHasher.Verify(pwd, storedHash))
                        {
                            userRow = r;
                            break;
                        }
                    }
                    if (userRow == null)
                    {
                        foreach (DataRow r in dtUser.Rows)
                        {
                            string legacyPwd = r["pwd"] as string;
                            if (!string.IsNullOrEmpty(legacyPwd) &&
                                string.Equals(pwd, legacyPwd, StringComparison.Ordinal))
                            {
                                MigrateUserPasswordToHash(conn,
                                    Convert.ToInt32(r["id"]), legacyPwd);
                                userRow = r;
                                break;
                            }
                        }
                    }
                    if (userRow == null)
                    {
                        frmSecurityPnl.Secured = false;
                        string msg = MainClass.Language == "ar" ? "دخول غير صحيح" : "Error login";
                        MessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Information);
                        txtPwd.Clear();
                        txtUser.Focus();
                        return false;
                    }

                    // ابحث بصفتك المستخدم المتحقق منه (الاستعلام الأصلي بقي بمعامل واحد @emp)
                    da = new SqlDataAdapter(
                        "select * from Users where id=@Id and IS_Deleted=0",
                        conn);
                    da.SelectCommand.Parameters.AddWithValue("@Id", userRow["id"]);
                }
                else
                {
                    da = new SqlDataAdapter(
                        "select * from Users where SecureCode=@Password and LoginSecode=1 and IS_Deleted=0",
                        conn);
                    da.SelectCommand.Parameters.AddWithValue("@Password", SecureCode);
                }

                DataTable dt = new DataTable();
                da.Fill(dt);

                if (dt.Rows.Count > 0)
                {
                    // التحقق من صلاحية الفرع
                    var daEmpBranch = new SqlDataAdapter(
                        "select branch from EmpBranches where emp=@emp and branch=@branch", conn);
                    daEmpBranch.SelectCommand.Parameters.AddWithValue("@emp", dt.Rows[0]["emp"]);
                    daEmpBranch.SelectCommand.Parameters.AddWithValue("@branch", cmbBranches.SelectedValue);
                    DataTable dtEmpBranch = new DataTable();
                    daEmpBranch.Fill(dtEmpBranch);

                    bool hasAccess = dtEmpBranch.Rows.Count > 0
                                  || Convert.ToInt32(dt.Rows[0]["emp"]) == 0;

                    if (hasAccess)
                    {
                        this.Cursor = Cursors.Wait;

                        MainClass.UserID = Convert.ToInt32(dt.Rows[0]["emp"]);
                        MainClass.EmpNo = Convert.ToInt32(dt.Rows[0]["emp"]);
                        MainClass.UserName = dt.Rows[0]["username"].ToString();

                        // مستودع الموظف
                        var daEmpTreasury = new SqlDataAdapter(
                            "select Stocks.id from Stocks, Stock_Emps " +
                            "where Stocks.id=Stock_Emps.stock_id " +
                            "and Stock_Emps.emp_id=@emp_id and Stocks.branch=@branch", conn);
                        daEmpTreasury.SelectCommand.Parameters.AddWithValue("@emp_id", dt.Rows[0]["emp"]);
                        daEmpTreasury.SelectCommand.Parameters.AddWithValue("@branch", cmbBranches.SelectedValue);
                        DataTable dtTreasury = new DataTable();
                        daEmpTreasury.Fill(dtTreasury);

                        if (dtTreasury.Rows.Count > 0)
                            MainClass.UserTreasury = Convert.ToInt32(dtTreasury.Rows[0]["id"]);

                        MainClass.BranchNo = Convert.ToInt32(cmbBranches.SelectedValue);
                        MainClass.BranchName = cmbBranches.Text;
                        return true;
                    }
                    else
                    {
                        MessageBox.Show("ليس لديك صلاحية لدخول هذا الفرع", "",
                            MessageBoxButton.OK, MessageBoxImage.Information);
                        cmbBranches.Focus();
                        frmSecurityPnl.Secured = false;
                        return false;
                    }
                }
                else
                {
                    frmSecurityPnl.Secured = false;
                    string msg = MainClass.Language == "ar" ? "دخول غير صحيح" : "Error login";
                    MessageBox.Show(msg, "", MessageBoxButton.OK, MessageBoxImage.Information);
                    txtPwd.Clear();
                    txtUser.Focus();
                    return false;
                }
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
                return false;
            }
        }

        #endregion

        #region Load Data

        // P1-009/P1-019 fix: ملف بيانات الإقلاع ينتقل من مجلد البرنامج (قد يكون للقراءة
        // فقط لمستخدم قياسي) إلى %APPDATA%/SmartAuditERP، وكلمات المرور تُخزن مشفرة
        // DPAPI (نطاق المستخدم الحالي) لا نصاً صريحاً.
        private static string StartupDataDir
            => Path.Combine(
                Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
                "SmartAuditERP");

        private static string StartupDataPath
            => Path.Combine(StartupDataDir, "StartupData.json");

        private static string LegacyStartupDataPath
            => Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "StartupData.json");

        private void MigrateUserPasswordToHash(SqlConnection dbConn, int userId, string legacyPassword)
        {
            // P1-010 fix: مهاجرة كلمة المستخدم النصية إلى تجزئة PBKDF2 وتصفير النص.
            try
            {
                string hash = Class.Security.PasswordHasher.Hash(legacyPassword);
                using (var cmd = new SqlCommand(
                    "UPDATE Users SET pwd_hash=@hash, pwd=N'' WHERE id=@id", dbConn))
                {
                    cmd.Parameters.Add("@hash", SqlDbType.NVarChar, 512).Value = hash;
                    cmd.Parameters.Add("@id", SqlDbType.Int).Value = userId;
                    if (dbConn.State != ConnectionState.Open) dbConn.Open();
                    cmd.ExecuteNonQuery();
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Trace.WriteLine(
                    "USER-PWD-MIGRATE failed id=" + userId + ": " + ex.Message);
            }
        }

        public void LoadData()
        {
            try
            {
                // P1-019 fix: التهجير من مسار مجلد البرنامج القديم إلى APPDATA إن وُجد
                if (!File.Exists(StartupDataPath) && File.Exists(LegacyStartupDataPath))
                {
                    try
                    {
                        Directory.CreateDirectory(StartupDataDir);
                        File.Copy(LegacyStartupDataPath, StartupDataPath, true);
                        // مسح القديم بعد النسخ — لا تبقى نسخة نصية بمجلد البرنامج
                        File.WriteAllText(LegacyStartupDataPath, "{}");
                    }
                    catch { /* مسار قديم للقراءة فقط: نستمر بالمسار الجديد */ }
                }

                if (!File.Exists(StartupDataPath))
                {
                    Directory.CreateDirectory(StartupDataDir);
                    File.Create(StartupDataPath).Dispose();
                    btnQuick.IsEnabled = false;

                    conn = conn_type == 2
                        ? MainClass.CreateSqlConnection($"server={MainClass.Server};user id={NetUserid}; pwd={Netpwd}")
                        : MainClass.CreateSqlConnection($"server={MainClass.Server};trusted_connection=true;");

                    if (conn.State != ConnectionState.Open)
                        conn.Open();

                    loadDBs();
                }
                else
                {
                    string json = File.ReadAllText(StartupDataPath);
                    var startupData = JsonConvert.DeserializeObject<StartupData>(json);

                    if (startupData != null)
                    {
                        chkRemember.IsChecked = startupData.Remember;
                        conn_type = Convert.ToInt32(startupData.ConnType);
                        MainClass.Server = startupData.Server;
                        txtDatabase = startupData.DatabaseName;
                        MainClass.Database = txtDatabase;
                        txtdatabaseName.Text = " " + txtDatabase;

                        MainClass.UseServerAuth = !string.IsNullOrEmpty(startupData.ServerUserName);

                        // P2-012 fix: قراءة سياسة قناة SQL الاختيارية من ملف
                        // الإقلاع — الغياب يبقي الافتراضي المتوافق.
                        if (startupData.SqlEncrypt.HasValue)
                            MainClass.SqlEncrypt = startupData.SqlEncrypt.Value;
                        if (startupData.SqlTrustServerCertificate.HasValue)
                            MainClass.SqlTrustServerCertificate =
                                startupData.SqlTrustServerCertificate.Value;

                        branchId = Convert.ToInt32(startupData.Branch);
                        txtUser.Text = startupData.UserName;

                        int langIdx = 0;
                        int.TryParse(startupData.Language, out langIdx);
                        cmblanguages.SelectedIndex = langIdx;
                        ConvertLanguage();

                        // P1-009 fix: فك تشفير DPAPI لكلمة الخادم؛ فشل الفك (مستخدم ويندوز
                        // مختلف/تلف/قيمة نصية قديمة) = تعامل كغير موجودة وأعد الإدخال.
                        string serverPwd = Class.Security.SecretProtector
                            .Unprotect(startupData.ServerPassword ?? "") ?? "";

                        if (conn_type == 1 && MainClass.UseServerAuth)
                        {
                            MainClass.NetUserId = startupData.ServerUserName;
                            MainClass.NetPwd = serverPwd;
                            NetUserid = startupData.ServerUserName;
                            Netpwd = serverPwd;
                        }
                        if (conn_type == 2)
                        {
                            MainClass.NetUserId = startupData.ServerUserName;
                            MainClass.NetPwd = serverPwd;
                            NetUserid = startupData.ServerUserName;
                            Netpwd = serverPwd;
                        }

                        if (startupData.Remember)
                        {
                            chkRemember.IsChecked = true;
                            // P1-009 fix: كلمة مرور التطبيق تُفك من DPAPI — لا نص صريح
                            txtPwd.Password = Class.Security.SecretProtector
                                .Unprotect(startupData.Password ?? "") ?? "";
                            btnLogin.Focus();
                        }
                        else
                        {
                            txtUser.Text = "";
                            txtPwd.Password = "";
                        }

                        btnQuick.IsEnabled = true;
                    }

                    // بناء الاتصال
                    // P1-018 fix: وضع SQL Authentication للاتصال المحلي (conn_type==1
                    // مع UseServerAuth) لم يعد يُتجاهَل — يُبنى باعتماد SQL لا trusted.
                    if (conn_type == 2)
                    {
                        conn = MainClass.CreateSqlConnection($"server={MainClass.Server};database={txtDatabase};" +
                                            $"user id={NetUserid}; pwd={Netpwd}");
                    }
                    else if (MainClass.UseServerAuth)
                    {
                        conn = MainClass.CreateSqlConnection($"server={MainClass.Server};database={txtDatabase};" +
                                            $"user id={NetUserid}; pwd={Netpwd}");
                    }
                    else
                    {
                        conn = MainClass.CreateSqlConnection($"server={MainClass.Server};database={txtDatabase};" +
                                            $"trusted_connection=true;");
                    }

                    if (conn.State != ConnectionState.Open)
                        conn.Open();

                    loadDBs();

                    cmbDatabases.SelectedValue = txtDatabase;
                    LoadBranches();

                    cmbBranches.SelectedValue = branchId > 0 ? (object)branchId : 1;
                }
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        public void loadDBs()
        {
            try
            {
                string sql = "SELECT sysdatabases.name, DatabasesManagment.Dbname " +
                             "FROM master.dbo.DatabasesManagment, master.dbo.sysdatabases " +
                             "where DatabasesManagment.dbid=sysdatabases.dbid " +
                             "and DatabasesManagment.IsActive=1 and DatabasesManagment.IsDeleted=0 " +
                             "order by DatabasesManagment.ImportanceOrder";

                SqlDataAdapter da = new SqlDataAdapter(sql, conn);
                DataTable dt = new DataTable();
                da.Fill(dt);

                cmbDatabases.ItemsSource = dt.DefaultView;
                cmbDatabases.DisplayMemberPath = "Dbname";
                cmbDatabases.SelectedValuePath = "name";
                cmbDatabases.SelectedIndex = -1;
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        public void LoadBranches()
        {
            try
            {
                if (conn.State != ConnectionState.Open)
                    conn.Open();

                // التأكد من وجود أعمدة IsDefault و IsActive
                string alterSql = @"
                    If Not EXISTS(SELECT * FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME='Branches' AND COLUMN_NAME='IsDefault')
                        ALTER Table Branches Add IsDefault bit NULL;
                    If Not EXISTS(SELECT * FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME='Branches' AND COLUMN_NAME='IsActive')
                        ALTER Table Branches Add IsActive bit NULL;
                    If EXISTS(SELECT * FROM Branches WHERE IsActive Is NULL)
                        UPDATE Branches SET IsActive=0 WHERE IsActive IS NULL;";

                foreach (string stmt in alterSql.Split(';',
                    StringSplitOptions.RemoveEmptyEntries))
                {
                    if (!string.IsNullOrWhiteSpace(stmt))
                    {
                        try
                        {
                            new SqlCommand(stmt.Trim(), conn).ExecuteNonQuery();
                        }
                        catch { /* تجاهل أخطاء ALTER */ }
                    }
                }

                string sql = "select Branchid as id, name from Branches " +
                             "where IS_Deleted=0 and IsActive=0 order by IsDefault desc";

                // التحقق من sync
                if (Sync.CheckBranchSync())
                {
                    sql = "select BranchId as id, name from Branches where BranchId=@BranchId";
                }

                // إعداد connstr
                if (conn_type == 2)
                {
                    MainClass.connstr = $"server={MainClass.Server};database={txtDatabase};" +
                                        $"user id={NetUserid}; pwd={Netpwd}";
                }
                else if (conn_type == 1 && MainClass.UseServerAuth)
                {
                    MainClass.connstr = $"server={MainClass.Server};database={txtDatabase};" +
                                        $"user id={NetUserid}; pwd={Netpwd}";
                }
                else
                {
                    MainClass.connstr = conn.ConnectionString;
                }

                MainClass.conn = conn;

                SqlDataAdapter da = new SqlDataAdapter(sql, conn);
                if (Sync.CheckBranchSync())
                    da.SelectCommand.Parameters.AddWithValue("@BranchId", Sync.BranchId);

                DataTable dt = new DataTable();
                da.Fill(dt);

                // تحقق من MQTT
                if (CheckMqttStat() && !Sync.CheckBranchSync())
                {
                    var daMqtt = new SqlDataAdapter(
                        "select isNull(BranchId,0) as id from Settingmqtt", conn);
                    DataTable dtMqtt = new DataTable();
                    daMqtt.Fill(dtMqtt);

                    if (dtMqtt.Rows.Count > 0)
                    {
                        branchId = Convert.ToInt32(dtMqtt.Rows[0][0]);
                        da = new SqlDataAdapter(
                            "select BranchId as id, name from Branches where BranchId=@BranchId",
                            conn);
                        da.SelectCommand.Parameters.AddWithValue("@BranchId", branchId);
                        dt.Rows.Clear();
                        da.Fill(dt);
                    }
                }

                cmbBranches.ItemsSource = dt.DefaultView;
                cmbBranches.DisplayMemberPath = "name";
                cmbBranches.SelectedValuePath = "id";
                cmbBranches.SelectedIndex = -1;

                if (cmbBranches.Items.Count > 0)
                    cmbBranches.SelectedIndex = 0;

                if (conn.State == ConnectionState.Open)
                    conn.Close();
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        #endregion

        #region Language

        public void ConvertLanguage()
        {
            if (!IsLoaded) return;
            string lang = cmblanguages.SelectedIndex == 0 ? "ar" : "en-us";

            if (lang == "ar")
            {
                this.FlowDirection = FlowDirection.LeftToRight;
                lblWelcomeAr.Text = "مرحباً بكم";
                lblWelcome.Text = "Welcome";
                lblLang.Text = "🌐 اللغة";
                lblDatabase.Text = "🗄️ الملف";
                lblBranch.Text = "🏢 الفرع";
                lblUserName.Text = "👤 اسم المستخدم";
                lblPassword.Text = "🔑 كلمة المرور";
                chkRemember.Content = "🔖 تذكرني";
                btnLogin.Content = "✅ الدخول";
                btnClose.Content = "❌ الخروج";
                btnQuick.Content = "⚡ دخول سريع";
            }
            else
            {
                this.FlowDirection = FlowDirection.RightToLeft;
                lblWelcomeAr.Text = "مرحباً بكم";
                lblWelcome.Text = "Welcome";
                lblLang.Text = "🌐 Language";
                lblDatabase.Text = "🗄️ Database";
                lblBranch.Text = "🏢 Branch";
                lblUserName.Text = "👤 Username";
                lblPassword.Text = "🔑 Password";
                chkRemember.Content = "🔖 Remember me";
                btnLogin.Content = "✅ Login";
                btnClose.Content = "❌ Exit";
                btnQuick.Content = "⚡ Quick Login";
            }

            MainClass.Language = lang;

            try
            {
                Common.SalesmanSetting();
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        #endregion

        #region Button Events

        private void btnLogin_Click(object sender, RoutedEventArgs e)
        {
            Login(1);
            var Home = new Home();
            Home.IsCashierClosed = true;
        }

        private void btnClose_Click(object sender, RoutedEventArgs e)
        {
            var Home = new Home();
            Home.IsCashierClosed = true;
            // إغلاق التطبيق
            System.Windows.Application.Current.Shutdown();
        }

        private void btnQuick_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                this.Topmost = false;
                ISExit = true;
                this.Hide();
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        private void btnServerSetting_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var frmServerSetting = new frmServerSetting();
                MessageBox.Show(
                    "تحذير! إن كنت غير متأكد من هذا الإجراء يرجى التواصل مع الدعم الفني " +
                    "لإجراء أي تعديل يخص السيرفر و قاعدة البيانات",
                    "", MessageBoxButton.OK, MessageBoxImage.Information);

                if (conn_type == 1)
                {
                    if (MainClass.UseServerAuth)
                    {
                        frmServerSetting.txtServer.Text = MainClass.Server;
                        frmServerSetting.lblCurrDatabase.Text = txtDatabase;
                        frmServerSetting.txtUser.Text = NetUserid;
                        frmServerSetting.txtPWD.Password = Netpwd;
                        frmServerSetting.chkServerAuth.IsChecked = true;
                    }
                    else
                    {
                        frmServerSetting.txtServer.Text = MainClass.Server;
                        frmServerSetting.lblCurrDatabase.Text = txtDatabase;
                    }
                }
                else
                {
                    frmServerSetting.rdNetwork.IsChecked = true;
                    frmServerSetting.txtServer.Text = MainClass.Server;
                    frmServerSetting.lblCurrDatabase.Text = txtDatabase;
                    frmServerSetting.txtUser.Text = NetUserid;
                    frmServerSetting.txtPWD.Password = Netpwd;
                }

                MainClass.ApplyPermissionToForm(frmServerSetting);
                MainClass.DoApplyUserSett(frmServerSetting);
                frmServerSetting.ShowDialog();
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        private void LinkLabel1_Click(object sender, MouseButtonEventArgs e)
        {
            btnServerSetting_Click(sender, null);
        }

        #endregion

        #region ComboBox Events

        private void cmblanguages_SelectionChangeCommitted(object sender, SelectionChangedEventArgs e)
        {
            ConvertLanguage();
        }

        private void cmbDatabases_SelectionChangeCommitted(object sender, SelectionChangedEventArgs e)
        {
            try
            {
                if (cmbDatabases.SelectedValue == null) return;

                string dbName = cmbDatabases.SelectedValue.ToString().Trim();

                try
                {
                    if (conn_type == 2)
                    {
                        conn = MainClass.CreateSqlConnection(
                            $"server={MainClass.Server};database={dbName};" +
                            $"user id={MainClass.NetUserId}; pwd={MainClass.NetPwd}");
                    }
                    else if (MainClass.UseServerAuth)
                    {
                        conn = MainClass.CreateSqlConnection(
                            $"server={MainClass.Server};database={dbName};" +
                            $"user id={MainClass.NetUserId}; pwd={MainClass.NetPwd}");
                    }
                    else
                    {
                        conn = MainClass.CreateSqlConnection(
                            $"server={MainClass.Server};database={dbName};trusted_connection=true;");
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("حدث خطأ أثناء الإتصال بالسيرفر تفاصيل الخطأ: " + ex.Message,
                        "", MessageBoxButton.OK, MessageBoxImage.Error);
                    return;
                }

                MainClass.Database = dbName;

                if (conn.State != ConnectionState.Open)
                {
                    conn.Open();
                    LoadBranches();
                    if (cmbBranches.Items.Count > 0)
                        cmbBranches.SelectedValue = branchId;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("حدث خطأ أثناء الإتصال بالسيرفر تفاصيل الخطأ: " + ex.Message,
                    "", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        #endregion

        #region KeyDown Events

        private void txtUser_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
                txtPwd.Focus();
        }

        private void txtPwd_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
                Login(1);
        }

        #endregion

        #region MQTT / Connection

        public void ConnectMQTList()
        {
            try
            {
                var Home = new Home();
                SqlCommand cmd = new SqlCommand("select * from Settingmqtt", conn);
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                DataTable dt = new DataTable();
                da.Fill(dt);

                if (dt.Rows.Count == 0)
                {
                    Home.lblnotify.Visibility = Visibility.Collapsed;
                    return;
                }

                var row = dt.AsEnumerable().ElementAtOrDefault(0);
                if (row == null) return;

                Home._servername = row["servername"].ToString();
                Home._DataBase = row["DB"].ToString();
                Home._pwd = row["pwd"].ToString();
                Home._usrname = row["usrname"].ToString();
                Home._sale = row["sale"].ToString();
                Home._receipt = row["receipt"].ToString();
                Home._income = row["income"].ToString();
                Home._finance = row["finance"].ToString();
                Home._nodeid = 1;
                Home._clientid = row["clientid"].ToString();
                Home._frequency = row["frequency"].ToString();
                Home._passcode = row["passcode"].ToString();
                Home._Itemid = row["inventory"].ToString();
                Home._is_active = Convert.ToBoolean(row["is_active"].ToString());

                if (Home._is_active)
                {
                    nssd._passcode = Home._passcode;
                    nssd.nid = Home._nodeid;
                    nssd.frqid = Home._frequency;
                    nssd.cid = Home._clientid;

                    if (conn.State != ConnectionState.Open)
                        conn.Open();

                    SendData.ClientCode = Home._clientid;
                    SendData._passcode = Home._passcode;
                    ReceivedData._passcode = Home._passcode;
                    SendData.connString = MainClass.connstr;
                    ReceivedData.connString = MainClass.connstr;
                    ConnectBroker.ClientCode = Home._clientid;
                    ConnectBroker._passcode = Home._passcode;
                    ConnectBroker.connString = MainClass.connstr;
                    ConnectBroker._IpServer = row["IpServer"].ToString();
                    // P1-014 fix: تحميل إعدادات أمان الوسيط إن وُجدت (أعمدة اختيارية بأمان)
                    if (row.Table.Columns.Contains("MqttPort"))
                    {
                        int.TryParse(row["MqttPort"]?.ToString(), out int mqttPort);
                        if (mqttPort > 0) ConnectBroker._mqttPort = mqttPort;
                    }
                    if (row.Table.Columns.Contains("MqttUseTls"))
                    {
                        bool.TryParse(row["MqttUseTls"]?.ToString(), out bool mqttTls);
                        ConnectBroker._mqttUseTls = mqttTls;
                    }
                    if (row.Table.Columns.Contains("MqttUser"))
                        ConnectBroker._mqttUser = row["MqttUser"]?.ToString() ?? "";
                    if (row.Table.Columns.Contains("MqttPass"))
                        ConnectBroker._mqttPass = row["MqttPass"]?.ToString() ?? "";
                    ConnectBroker._syncItems = Convert.ToBoolean(row["syncItems"]);
                    ConnectBroker._syncOper = Convert.ToBoolean(row["syncOper"]);
                    ConnectBroker._syncDefinitions = Convert.ToBoolean(row["syncDefinitions"]);

                    if (ConnectBroker.CheckConnectionAndBroker())
                    {
                        Home.lblnotify.Text = "حالة المزامنة نشطة";
                        Home.lblnotify.Foreground = new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Colors.Green);
                        Home.lblnotify.Visibility = Visibility.Visible;
                    }
                    else
                    {
                        Home.lblnotify.Visibility = Visibility.Collapsed;
                        Home.lblnotify.Text = "حالة المزامنة غير نشطة";
                        Home.lblnotify.Foreground = new System.Windows.Media.SolidColorBrush(
                            System.Windows.Media.Colors.Red);
                    }
                }
                else
                {
                    Home.lblnotify.Text = "حالة المزامنة غير نشطة";
                    Home.lblnotify.Foreground = new System.Windows.Media.SolidColorBrush(
                        System.Windows.Media.Colors.Red);
                }
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
            }
        }

        private bool CheckMqttStat()
        {
            try
            {
                var Home = new Home();
                SqlDataAdapter da = new SqlDataAdapter(
                    "select * from Settingmqtt where is_active=1", conn);
                DataTable dt = new DataTable();
                da.Fill(dt);

                if (dt.Rows.Count > 0)
                {
                    Home._is_active = true;
                    return true;
                }
                return false;
            }
            catch (Exception ex)
            {
                Logger.Error(ex);
                return false;
            }
        }

        #endregion

        #region Utility

        public long MUL(long no, int x)
        {
            return checked(no * (long)x);
        }

        public string GetVersion()
        {
            return "20.0.6.4";
        }

        #endregion
    }
}