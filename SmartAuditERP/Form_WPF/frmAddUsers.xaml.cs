// frmAddUsers.xaml.cs
using System;
using System.Collections.ObjectModel;
using System.Data;
using System.Data.SqlClient;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace SmartAuditERP.Form_WPF
{
    public partial class frmAddUsers : DevExpress.Xpf.Core.ThemedWindow
    {
        #region Fields

        private SqlConnection conn;
        private int Code = -1;
        private ObservableCollection<UserRowModel> userRows
            = new ObservableCollection<UserRowModel>();

        #endregion

        #region Constructor

        public frmAddUsers()
        {
            InitializeComponent();
            conn = MainClass.ConnObj();
        }

        #endregion

        #region Window Load

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            dgvUsers.ItemsSource = userRows;
            LoadDG();
            LoadEmps();

            if (MainClass.UserID == 0)
                ckDeletedUsers.Visibility = Visibility.Visible;
        }

        #endregion

        #region Load Methods

        public void LoadEmps()
        {
            try
            {
                var da = new SqlDataAdapter(
                    "select id,name from Employees where IS_Deleted=0 order by id", conn);
                var dt = new DataTable();
                da.Fill(dt);
                cmbEmp.ItemsSource = dt.DefaultView;
                cmbEmp.DisplayMemberPath = "name";
                cmbEmp.SelectedValuePath = "id";
                cmbEmp.SelectedIndex = -1;
            }
            catch { }
        }

        private void LoadDG()
        {
            try
            {
                string whereClause = " and Employees.IS_Deleted=0 and Users.IS_Deleted=0 ";
                if (ckDeletedUsers.IsChecked == true)
                    whereClause = "";

                var da = new SqlDataAdapter(
                    "select Users.id as userid, Employees.id as empid, " +
                    "Employees.name, username, pwd, SecureCode, LoginSecode " +
                    "from Employees, Users " +
                    "where Employees.id=Users.emp" + whereClause, conn);

                var dt = new DataTable();
                da.Fill(dt);

                userRows.Clear();
                foreach (DataRow row in dt.Rows)
                {
                    userRows.Add(new UserRowModel
                    {
                        userid = Convert.ToInt32(row["userid"]),
                        empid = Convert.ToInt32(row["empid"]),
                        name = row["name"].ToString(),
                        username = row["username"].ToString(),
                        pwd = row["pwd"].ToString(),
                        SecureCodeVal = row["SecureCode"].ToString(),
                        LoginSecode = Convert.ToBoolean(row["LoginSecode"])
                    });
                }

                dgvUsers.UnselectAll();
            }
            catch { }
        }

        #endregion

        #region CLR (Clear)

        private void CLR()
        {
            cmbEmp.SelectedIndex = -1;
            txtUser.Text = "";
            txtPass.Password = "";
            txtSecureCode.Text = "";
            ckLoginSecode.IsChecked = false;
            Code = -1;
            cmbEmp.Focus();
        }

        #endregion

        #region Button Events

        private void btnNew_Click(object sender, RoutedEventArgs e)
        {
            CLR();
        }

        private void btnSave_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Repair R-030 (audit finding P2-001): pressing Enter in the password field calls
                // this handler directly, and the handler never re-checked whether saving was even
                // permitted - so a user whose btnSave had been disabled by the permission pass
                // (MainClass.ApplyPermissionToForm -> ApplyWpfPermissions sets IsEnabled=false)
                // could still write accounts through the keyboard route. A disabled WPF button
                // cannot raise its own Click, so the only live bypass is this re-entrant path;
                // enforce the platform's own decision here, where every caller funnels through.
                if (!btnSave.IsEnabled)
                {
                    MessageBox.Show("لا تملك صلاحية الحفظ في هذه الشاشة.", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (cmbEmp.SelectedValue == null)
                {
                    MessageBox.Show("اختر موظف", "", MessageBoxButton.OK,
                        MessageBoxImage.Information);
                    cmbEmp.Focus();
                    return;
                }

                if (string.IsNullOrWhiteSpace(txtUser.Text))
                {
                    MessageBox.Show("ادخل اسم المستخدم", "", MessageBoxButton.OK,
                        MessageBoxImage.Information);
                    txtUser.Focus();
                    return;
                }

                if (string.IsNullOrWhiteSpace(txtPass.Password))
                {
                    MessageBox.Show("ادخل كلمة المرور", "", MessageBoxButton.OK,
                        MessageBoxImage.Information);
                    txtPass.Focus();
                    return;
                }

                if (MessageBox.Show("هل أنت متأكد من عملية الحفظ؟", "تأكيد",
                    MessageBoxButton.YesNo, MessageBoxImage.Question)
                    != MessageBoxResult.Yes) return;

                // التحقق من تكرار اسم المستخدم (إضافة جديدة)
                if (Code == -1)
                {
                    // Repair R-015 (audit finding P1-011): the entered username was concatenated
                    // into this uniqueness check; bind it as a typed parameter instead.
                    var dupUserCmd = new SqlCommand(
                        "select emp from Users where username=@username and IS_Deleted=0", conn);
                    dupUserCmd.Parameters.Add("@username", SqlDbType.NVarChar).Value = txtUser.Text;
                    var da = new SqlDataAdapter(dupUserCmd);
                    var dt = new DataTable();
                    da.Fill(dt);
                    if (dt.Rows.Count > 0)
                    {
                        MessageBox.Show("اسم المستخدم مدخل من قبل، ادخل اسم مستخدم آخر",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        txtUser.Focus();
                        return;
                    }
                }

                // التحقق من تكرار الرقم السري (إضافة وتعديل)
                if (!string.IsNullOrWhiteSpace(txtSecureCode.Text))
                {
                    // Repair R-015 (P1-011): bind the secure code as a typed parameter instead of
                    // embedding it in the uniqueness-check text.
                    // Repair R-032 (audit finding P2-008): this check used to run for NEW users
                    // only, so editing an account could silently create a duplicate PIN that later
                    // resolves to whichever row comes first. It now also runs while editing,
                    // excluding the record being edited by its own key (id<>@id keeps @id=-1
                    // harmless on the add path). The database index backing this stays tracked as
                    // owner-input residual (no unique constraint exists in the embedded schema).
                    var dupCodeCmd = new SqlCommand(
                        "select id from Users where SecureCode=@secureCode and IS_Deleted=0 and id<>@id", conn);
                    dupCodeCmd.Parameters.Add("@secureCode", SqlDbType.NVarChar).Value = txtSecureCode.Text;
                    dupCodeCmd.Parameters.Add("@id", SqlDbType.Int).Value = Code;
                    var da2 = new SqlDataAdapter(dupCodeCmd);
                    var dt2 = new DataTable();
                    da2.Fill(dt2);
                    if (dt2.Rows.Count > 0)
                    {
                        MessageBox.Show("الرقم السري مدخل من قبل، ادخل رقم سري آخر",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        txtSecureCode.Focus();
                        return;
                    }
                }

                // التحقق من تكرار اسم المستخدم (تعديل)
                if (Code != -1)
                {
                    // Repair R-015 (P1-011): bind both the edited user key and the entered username
                    // as typed parameters for the edit-mode uniqueness check.
                    // Repair R-029 (audit finding P2-007): @code holds the USERS record id, but the
                    // exclusion compared against emp, so the record being edited was NOT excluded
                    // (editing without renaming always reported a phantom duplicate) and records
                    // whose emp collided with another row's id were wrongly skipped. Exclude by the
                    // actual primary key.
                    var dupEditCmd = new SqlCommand(
                        "select id from Users where id<>@code and username=@username and IS_Deleted=0", conn);
                    dupEditCmd.Parameters.Add("@code", SqlDbType.Int).Value = Code;
                    dupEditCmd.Parameters.Add("@username", SqlDbType.NVarChar).Value = txtUser.Text;
                    var da3 = new SqlDataAdapter(dupEditCmd);
                    var dt3 = new DataTable();
                    da3.Fill(dt3);
                    if (dt3.Rows.Count > 0)
                    {
                        MessageBox.Show("اسم المستخدم مدخل من قبل، ادخل اسم مستخدم آخر",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        txtUser.Focus();
                        return;
                    }
                }

                // التحقق إذا كان الموظف لديه مستخدم مسبق
                var daCheck = new SqlDataAdapter(
                    "select id from Users where emp=" +
                    cmbEmp.SelectedValue, conn);
                var dtCheck = new DataTable();
                daCheck.Fill(dtCheck);
                if (dtCheck.Rows.Count > 0)
                    Code = Convert.ToInt32(dtCheck.Rows[0]["id"]);

                int loginSecode = (ckLoginSecode.IsChecked == true) ? 1 : 0;

                // Repair R-032 (P2-008): a failed numeric parse used to fall through as ZERO and
                // fractions were truncated on cast - "12.7" stored 12, letters stored 0 - so two
                // accounts could converge on the same identity key after normalisation. The PIN is
                // now canonical digits only: required and strictly integral when quick-login is
                // enabled, still optional (stored 0) when it is not, and never silently coerced.
                long pinVal = 0;
                string pinText = txtSecureCode.Text?.Trim() ?? "";
                if (pinText.Length > 0)
                {
                    if (!long.TryParse(pinText, out pinVal) || pinVal < 0 || pinVal > int.MaxValue)
                    {
                        MessageBox.Show("الرقم السري يجب أن يكون رقماً صحيحاً موجباً بلا كسور أو حروف.",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        txtSecureCode.Focus();
                        return;
                    }
                }
                else if (loginSecode == 1)
                {
                    MessageBox.Show("أدخل الرقم السري أو ألغِ تفعيل الدخول به.",
                        "", MessageBoxButton.OK, MessageBoxImage.Warning);
                    txtSecureCode.Focus();
                    return;
                }
                int secureCodeInt = (int)pinVal;

                if (conn.State != ConnectionState.Open) conn.Open();

                SqlCommand cmd;
                if (Code == -1)
                {
                    cmd = new SqlCommand(
                        "insert into Users(emp,username,pwd,SecureCode,LoginSecode,IS_Deleted)" +
                        " values(" + cmbEmp.SelectedValue +
                        ",@username,@pwd," + secureCodeInt +
                        "," + loginSecode + ",0)", conn);
                    cmd.Parameters.Add("@username", SqlDbType.NVarChar).Value = txtUser.Text;
                    cmd.Parameters.Add("@pwd", SqlDbType.NVarChar).Value = txtPass.Password;
                    cmd.ExecuteNonQuery();
                    CLR();
                    cmbEmp.Focus();
                }
                else
                {
                    cmd = new SqlCommand(
                        "update Users set emp=" + cmbEmp.SelectedValue +
                        ",username=@username,pwd=@pwd,SecureCode=" + secureCodeInt +
                        ",LoginSecode=" + loginSecode +
                        ",IS_Deleted=0 where id=" + Code, conn);
                    cmd.Parameters.Add("@username", SqlDbType.NVarChar).Value = txtUser.Text;
                    cmd.Parameters.Add("@pwd", SqlDbType.NVarChar).Value = txtPass.Password;
                    cmd.ExecuteNonQuery();
                    cmbEmp.Focus();
                }

                // إرسال عبر MQTT إذا كان متصلاً
                try
                {
                    var Home = new Home();
                    if (Home._is_active && ConnectBroker.CheckConnectionAndBroker())
                    {
                        string topic = "";
                        ConnectBroker.mqttClient.Publish(
                            ConnectBroker.ClientCode + "Users",
                            Encoding.UTF8.GetBytes(SendData.GetUsers(topic)), 0, true);
                        ConnectBroker.mqttClient.Publish(
                            ConnectBroker.ClientCode + "UserPermissions",
                            Encoding.UTF8.GetBytes(SendData.GetUserPermissions(topic)), 0, true);
                        ConnectBroker.mqttClient.Publish(
                            ConnectBroker.ClientCode + "OperationPermission",
                            Encoding.UTF8.GetBytes(SendData.GetOperationPermission(topic)), 0, true);
                    }
                }
                catch { }

                MessageBox.Show("تم الحفظ", "", MessageBoxButton.OK,
                    MessageBoxImage.Information);
                LoadDG();
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ أثناء الحفظ\n" + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                if (conn.State == ConnectionState.Open) conn.Close();
            }
        }

        private void btnDelete_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (Code == -1)
                {
                    MessageBox.Show("اختر مستخدماً ليتم حذفه", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (Code == 1)
                {
                    MessageBox.Show("لا يمكن حذف مستخدم المدير", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (MessageBox.Show("هل أنت متأكد من حذف المستخدم؟", "تأكيد",
                    MessageBoxButton.YesNo, MessageBoxImage.Question)
                    != MessageBoxResult.Yes) return;

                if (conn.State != ConnectionState.Open) conn.Open();

                // الحصول على رقم الموظف
                var da = new SqlDataAdapter(
                    "select emp from Users where id=" + Code + " and IS_Deleted=0", conn);
                var dt = new DataTable();
                da.Fill(dt);

                if (dt.Rows.Count == 0) return;

                int empId = Convert.ToInt32(dt.Rows[0]["emp"]);

                // التحقق من الفواتير
                using (var cmdCheck = new SqlCommand(
                    "IF EXISTS(SELECT 1 FROM inv where sales_emp=@emp and IS_Deleted=0)" +
                    " SELECT 1 ELSE SELECT 0", conn))
                {
                    cmdCheck.Parameters.Add("@emp", SqlDbType.Int).Value = empId;
                    int hasInv = Convert.ToInt32(cmdCheck.ExecuteScalar());
                    if (hasInv == 1)
                    {
                        MessageBox.Show(
                            string.Equals(MainClass.Language, "ar",
                                StringComparison.OrdinalIgnoreCase)
                                ? "لا يمكن حذف موظف مرتبط بفواتير"
                                : "Cannot delete an employee associated with invoices",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }
                }

                // التحقق من القيود
                using (var cmdCheck2 = new SqlCommand(
                    "IF EXISTS(SELECT 1 FROM Entry where EmpID=@emp and IS_Deleted=0)" +
                    " SELECT 1 ELSE SELECT 0", conn))
                {
                    cmdCheck2.Parameters.Add("@emp", SqlDbType.Int).Value = empId;
                    int hasEntry = Convert.ToInt32(cmdCheck2.ExecuteScalar());
                    if (hasEntry == 1)
                    {
                        MessageBox.Show(
                            string.Equals(MainClass.Language, "ar",
                                StringComparison.OrdinalIgnoreCase)
                                ? "لا يمكن حذف موظف مرتبط بقيود"
                                : "Cannot delete an employee associated with entries",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }
                }

                new SqlCommand(
                    "update Users set IS_Deleted=1 where id=" + Code, conn)
                    .ExecuteNonQuery();

                MessageBox.Show("تم الحذف", "", MessageBoxButton.OK,
                    MessageBoxImage.Information);
                LoadDG();
                CLR();
            }
            catch (Exception ex)
            {
                MessageBox.Show("خطأ أثناء الحذف\n" + ex.Message, "",
                    MessageBoxButton.OK, MessageBoxImage.Error);
            }
            finally
            {
                if (conn.State == ConnectionState.Open) conn.Close();
            }
        }

        private void btnClose_Click(object sender, RoutedEventArgs e)
            => this.Close();

        private void btnPrint_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("سيتم تنفيذ الطباعة قريباً", "",
                MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private void btnAddEmployee_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var frm = new frmEmployees();
                MainClass.ApplyPermissionToForm(frm);
                MainClass.DoApplyUserSett(frm);
                frm.ShowDialog();
                if (frm.IsDone)
                    LoadEmps();
            }
            catch { }
        }

        #endregion

        #region Navigation

        private void Navigate(string sql)
        {
            try
            {
                if (conn.State != ConnectionState.Open) conn.Open();
                using (var cmd = new SqlCommand(sql, conn))
                using (var dr = cmd.ExecuteReader())
                {
                    if (dr.HasRows && dr.Read())
                    {
                        Code = Convert.ToInt32(dr["id"]);
                        cmbEmp.SelectedValue = dr["emp"];
                        txtUser.Text = dr["username"].ToString();
                        txtPass.Password = dr["pwd"].ToString();
                        txtSecureCode.Text = dr["SecureCode"].ToString();
                        ckLoginSecode.IsChecked =
                            Convert.ToBoolean(dr["LoginSecode"]);
                    }
                }
                dgvUsers.UnselectAll();
            }
            catch { }
            finally
            {
                if (conn.State == ConnectionState.Open) conn.Close();
            }
        }

        private void btnFirst_Click(object sender, RoutedEventArgs e)
            => Navigate("select top 1 * from Users where IS_Deleted=0 order by id asc");

        private void btnLast_Click(object sender, RoutedEventArgs e)
            => Navigate("select top 1 * from Users where IS_Deleted=0 order by id desc");

        private void btnNext_Click(object sender, RoutedEventArgs e)
            => Navigate("select top 1 * from Users where IS_Deleted=0 and id>" +
               Code + " order by id asc");

        private void btnPrevious_Click(object sender, RoutedEventArgs e)
            => Navigate("select top 1 * from Users where IS_Deleted=0 and id<" +
               Code + " order by id desc");

        #endregion

        #region DataGrid Events

        private void dgvUsers_MouseLeftButtonUp(object sender, MouseButtonEventArgs e)
        {
            try
            {
                if (dgvUsers.SelectedItem is UserRowModel row)
                    DgvRowChange(row);
            }
            catch { }
        }

        private void Column6_ButtonClick(object sender, RoutedEventArgs e)
        {
            try
            {
                if (sender is Button btn && btn.Tag is UserRowModel row)
                {
                    var frm = new frmUsersPermissions();
                    frm.Show();
                    // Repair R-029 (audit finding P2-007): that combo's SelectedValuePath is "emp"
                    // (the employee link Users.emp = Employees.id), yet the row's USERS record id
                    // was passed. Whenever the two numbers differ the permissions editor opened on
                    // the wrong employee (or none); pass the employee id instead.
                    frm.cmbEmp.SelectedValue = row.empid;
                }
            }
            catch { }
        }

        private void DgvRowChange(UserRowModel row)
        {
            Code = row.userid;
            cmbEmp.SelectedValue = row.empid.ToString();
            txtUser.Text = row.username;
            txtSecureCode.Text = row.SecureCodeVal;
            txtPass.Password = row.pwd;
            ckLoginSecode.IsChecked = row.LoginSecode;
        }

        #endregion

        #region ComboBox Events

        private void cmbEmp_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            try
            {
                Code = -1;
                txtUser.Text = "";
                txtPass.Password = "";

                if (cmbEmp.SelectedValue == null) return;

                var da = new SqlDataAdapter(
                    "select id,username,pwd,SecureCode,LoginSecode " +
                    "from Users where emp=" + cmbEmp.SelectedValue +
                    " and IS_Deleted=0", conn);
                var dt = new DataTable();
                da.Fill(dt);

                if (dt.Rows.Count > 0)
                {
                    var row = dt.Rows[0];
                    double.TryParse(row["id"].ToString(), out double idVal);
                    Code = (int)Math.Round(idVal);
                    txtUser.Text = row["username"].ToString();
                    txtPass.Password = row["pwd"].ToString();
                    txtSecureCode.Text = row["SecureCode"].ToString();
                    ckLoginSecode.IsChecked = Convert.ToBoolean(row["LoginSecode"]);
                }
            }
            catch { }
        }

        #endregion

        #region CheckBox Events

        private void ckDeletedUsers_CheckedChanged(object sender, RoutedEventArgs e)
            => LoadDG();

        #endregion

        #region Keyboard Events

        private void txtPass_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Return)
                btnSave_Click(null, null);
        }

        #endregion
    }

    #region Model Class

    public class UserRowModel : System.ComponentModel.INotifyPropertyChanged
    {
        private int _userid;
        private int _empid;
        private string _name;
        private string _username;
        private string _pwd;
        private string _secureCodeVal;
        private bool _loginSecode;

        public int userid
        {
            get => _userid;
            set { _userid = value; OnPropertyChanged(nameof(userid)); }
        }
        public int empid
        {
            get => _empid;
            set { _empid = value; OnPropertyChanged(nameof(empid)); }
        }
        public string name
        {
            get => _name;
            set { _name = value; OnPropertyChanged(nameof(name)); }
        }
        public string username
        {
            get => _username;
            set { _username = value; OnPropertyChanged(nameof(username)); }
        }
        public string pwd
        {
            get => _pwd;
            set { _pwd = value; OnPropertyChanged(nameof(pwd)); }
        }
        public string SecureCodeVal
        {
            get => _secureCodeVal;
            set { _secureCodeVal = value; OnPropertyChanged(nameof(SecureCodeVal)); }
        }
        public bool LoginSecode
        {
            get => _loginSecode;
            set { _loginSecode = value; OnPropertyChanged(nameof(LoginSecode)); }
        }

        public event System.ComponentModel.PropertyChangedEventHandler PropertyChanged;
        protected void OnPropertyChanged(string name)
            => PropertyChanged?.Invoke(this,
               new System.ComponentModel.PropertyChangedEventArgs(name));
    }

    #endregion
}