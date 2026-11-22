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
                    var da = new SqlDataAdapter(
                        "select emp from Users where username=N'" +
                        txtUser.Text + "' and IS_Deleted=0", conn);
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

                // التحقق من صحة الرقم السريع وتفرّده (جديدًا وتعديلًا)
                // P2-008 fix: ثلاث علل كانت هنا —
                //  ١) لا فحص تكرار إطلاقًا عند التعديل
                //  ٢) الفحص كان بالنص الخام بينما الكتابة بالقيمة المحوّلة
                //     (double→int) فيفوت تعارضات مثل «12.9» مقابل 12
                //  ٣) فشل التحويل كان يكتب 0 بصمت فيتساوى الجميع
                int secureCodeVal;
                bool hasSecureCode = int.TryParse(txtSecureCode.Text.Trim(), out secureCodeVal);
                if (!string.IsNullOrWhiteSpace(txtSecureCode.Text) && !hasSecureCode)
                {
                    MessageBox.Show("الرقم السريع يجب أن يكون عددًا صحيحًا", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    txtSecureCode.Focus();
                    return;
                }
                if (hasSecureCode && !string.IsNullOrWhiteSpace(txtSecureCode.Text))
                {
                    string excludeCurrent = Code == -1 ? "" : " and id<>@id ";
                    var da2 = new SqlDataAdapter(
                        "select id from Users where SecureCode=@secureCode" +
                        excludeCurrent + "and IS_Deleted=0", conn);
                    da2.SelectCommand.Parameters.Add("@secureCode", SqlDbType.Int).Value = secureCodeVal;
                    if (Code != -1)
                        da2.SelectCommand.Parameters.Add("@id", SqlDbType.Int).Value = Code;
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
                    // P1-011 fix: بارامترات بدل حشر النص في SQL
                    // P2-007 fix: كانت المقارنة emp<>@emp حيث @emp=Code أي
                    // معرف موظف يقارَن بمعرف سجل Users (فضاءان مختلفان)
                    // فيفوت تعارضات أسماء حقيقية؛ الاستبعاد الصحيح هو
                    // سجل المستخدم نفسه: id<>@id.
                    var da3b = new SqlDataAdapter(
                        "select id from Users where id<>@id " +
                        "and username=@username and IS_Deleted=0", conn);
                    da3b.SelectCommand.Parameters.Add("@id", SqlDbType.Int).Value = Code;
                    da3b.SelectCommand.Parameters.Add("@username", SqlDbType.NVarChar, 100).Value = txtUser.Text;
                    var dt3b = new DataTable();
                    da3b.Fill(dt3b);
                    if (dt3b.Rows.Count > 0)
                    {
                        MessageBox.Show("اسم المستخدم مدخل من قبل، ادخل اسم مستخدم آخر",
                            "", MessageBoxButton.OK, MessageBoxImage.Warning);
                        txtUser.Focus();
                        return;
                    }
                }

                // التحقق إذا كان الموظف لديه مستخدم مسبق
                // P1-011 fix: بارامترات
                var daCheck = new SqlDataAdapter(
                    "select id from Users where emp=@emp", conn);
                daCheck.SelectCommand.Parameters.Add("@emp", SqlDbType.Int).Value = cmbEmp.SelectedValue;
                var dtCheck = new DataTable();
                daCheck.Fill(dtCheck);
                if (dtCheck.Rows.Count > 0)
                    Code = Convert.ToInt32(dtCheck.Rows[0]["id"]);

                int loginSecode = (ckLoginSecode.IsChecked == true) ? 1 : 0;

                // secureCodeVal: من فحص P2-008 أعلاه — عدد صحيح مُتحقق منه
                // أو صفر عند الفراغ (SecureCode اختياري).

                // P1-010 fix: كلمة المرور تُخزن تجزئة PBKDF2 في pwd_hash ويُصفّر النص.
                // P1-011 fix: كل القيم بارامترات — لا حشر نص في SQL.
                string pwdHash = Class.Security.PasswordHasher.Hash(txtPass.Password);

                if (conn.State != ConnectionState.Open) conn.Open();

                SqlCommand cmd;
                if (Code == -1)
                {
                    cmd = new SqlCommand(
                        "insert into Users(emp,username,pwd_hash,pwd,SecureCode,LoginSecode,IS_Deleted)" +
                        " values(@emp,@username,@pwdHash,N'',@secureCode,@loginSecode,0)", conn);
                    cmd.Parameters.Add("@emp", SqlDbType.Int).Value = cmbEmp.SelectedValue;
                    cmd.Parameters.Add("@username", SqlDbType.NVarChar).Value = txtUser.Text;
                    cmd.Parameters.Add("@pwdHash", SqlDbType.NVarChar, 512).Value = pwdHash;
                    cmd.Parameters.Add("@secureCode", SqlDbType.Int).Value = secureCodeVal;
                    cmd.Parameters.Add("@loginSecode", SqlDbType.Int).Value = loginSecode;
                    cmd.ExecuteNonQuery();
                    CLR();
                    cmbEmp.Focus();
                }
                else
                {
                    cmd = new SqlCommand(
                        "update Users set emp=@emp,username=@username,pwd_hash=@pwdHash,pwd=N''" +
                        ",SecureCode=@secureCode,LoginSecode=@loginSecode" +
                        ",IS_Deleted=0 where id=@id", conn);
                    cmd.Parameters.Add("@emp", SqlDbType.Int).Value = cmbEmp.SelectedValue;
                    cmd.Parameters.Add("@username", SqlDbType.NVarChar).Value = txtUser.Text;
                    cmd.Parameters.Add("@pwdHash", SqlDbType.NVarChar, 512).Value = pwdHash;
                    cmd.Parameters.Add("@secureCode", SqlDbType.Int).Value = secureCodeVal;
                    cmd.Parameters.Add("@loginSecode", SqlDbType.Int).Value = loginSecode;
                    cmd.Parameters.Add("@id", SqlDbType.Int).Value = Code;
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

                // P2-009 fix: كان تعطيل حساب المستخدم (IS_Deleted=1) محجوباً
                // إذا كان للموظف فواتير أو قيود — حاجزان يحرسان الكيان الخطأ:
                // التعطيل لا يمس سجل الموظف ولا التاريخ المالي إطلاقاً
                // (المستندات تشير لمعرف الموظف الباقي)، فبقي كل من سجّل يوماً
                // حركةً بحسابه نشطاً للأبد — عجز حقيقي في سحب الصلاحيات.
                // حذف الموظف نفسه (شاشة الموظفين) يبقى محروساً بتلك الفحوص.
                // (استعلام معرف الموظف حُذف أيضاً: لم يكن يخدم سوى الحاجزَين.)

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
                // P2-001 fix: زر الشبكة مسار بديل لفتح شاشة صلاحيات المستخدمين —
                // يخضع لنفس بوابة الرؤية التي تضبط مدخل «صلاحيات المستخدمين»
                // في قائمة الشاشة الرئيسية (stripUserPerm)، لا يتجاوزها.
                var home = System.Windows.Application.Current.Windows
                    .OfType<Home>().FirstOrDefault();
                // P2-001 fix + fail-closed: لا نافذة رئيسية = لا يمكن التحقق
                // من البوابة = منع. — P2-007 fix: يُمرر معرف الموظف (empid)
                // لا معرف سجل Users، فقائمة الموظفين مفاتيحها معرفات الموظفين.
                if (home == null || home.stripUserPerm.Visibility != Visibility.Visible)
                {
                    MessageBox.Show(
                        "غير مسموح: لا تملك صلاحية إدارة صلاحيات المستخدمين", "",
                        MessageBoxButton.OK, MessageBoxImage.Warning);
                    return;
                }

                if (sender is Button btn && btn.Tag is UserRowModel row)
                {
                    var frm = new frmUsersPermissions();
                    frm.Show();
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
            // P2-001 fix: مسار Enter البديل يحترم تعطيل btnSave بالصلاحيات —
            // كان يستدعي الحفظ مباشرة حتى والزر معطّل.
            if (e.Key == Key.Return && btnSave.IsEnabled)
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