using System;
using System.Collections;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using AuditorAPI.Models;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace SmartAuditERP
{

        public class Reseved
        {
                public class resvd
                {
                        public string GlobalID;

                        public int _id;

                        public int BranchID;

                        public string EntryGlobalID;

                        public int ReceiptType;

                        public bool State;

                        public DateTime ReceiptDate;

                        public bool ISDeleted;

                        public string Notes;

                        public string _name;

                        public string CreditAcc;

                        public string DebitAcc;

                        public decimal _Basic;

                        public decimal _Houses;

                        public decimal _Travel;

                        public decimal _saladd;

                        public decimal _salsub;

                        public decimal _Net;

                        public string Cccode;

                        public string Sync;

                        public int _res_emp;

                        public int _Month;

                        public int _year;

                        public resvd()
                        {
                                this.GlobalID = "";
                                this._id = 0;
                                this.BranchID = 1;
                                this.EntryGlobalID = "";
                                this.ReceiptType = 27;
                                this.State = true;
                                this.ReceiptDate = DateAndTime.Now.Date;
                                this.ISDeleted = false;
                                this.Notes = "";
                                this._name = "";
                                this.CreditAcc = "";
                                this.DebitAcc = "";
                                this._Basic = default(decimal);
                                this._Houses = default(decimal);
                                this._Travel = default(decimal);
                                this._saladd = default(decimal);
                                this._salsub = default(decimal);
                                this._Net = default(decimal);
                                this.Cccode = "";
                                this.Sync = "";
                                this._res_emp = 0;
                                this._Month = 0;
                                this._year = 0;
                        }
                }

                public bool insertSalaryres()
                {
                        new SqlCommand();
                        new SqlDataAdapter();
                        DataTable dataTable;
                        dataTable = new DataTable();
                        SqlConnection sqlConnection;
                        sqlConnection = MainClass.ConnObj();
                        if (sqlConnection.State != ConnectionState.Open)
                        {
                                sqlConnection.Open();
                        }
                        SqlCommand sqlCommand;
                        sqlCommand = new SqlCommand("select GlobalID from Salary_Res where id=@id", sqlConnection);
                        resvd resvd = default(resvd);
                        sqlCommand.Parameters.Add("@id", SqlDbType.Int).Value = resvd._id;
                        new SqlDataAdapter(sqlCommand).Fill(dataTable);
                        if (dataTable.Rows.Count > 0)
                        {
                                sqlCommand = new SqlCommand("delete from Salary_Res where GlobalID=@GlobalID", sqlConnection);
                                sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = resvd.GlobalID;
                                sqlCommand.ExecuteNonQuery();
                                sqlCommand = new SqlCommand("insert into Salary_Res(GlobalID,date,month,year,IS_Deleted,branch,notes,EntryGlobalID) values(@GlobalID,@date,@month,@year,@IS_Deleted,@branch,@notes,@EntryGlobalID)", sqlConnection);
                                sqlCommand.Parameters.Add("@id", SqlDbType.Int).Value = resvd._id;
                                sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = resvd.GlobalID;
                                sqlCommand.Parameters.Add("@date", SqlDbType.DateTime).Value = resvd.ReceiptDate;
                                sqlCommand.Parameters.Add("@month", SqlDbType.Int).Value = resvd._Month;
                                sqlCommand.Parameters.Add("@year", SqlDbType.Int).Value = resvd._year;
                                sqlCommand.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value = resvd.ISDeleted;
                                sqlCommand.Parameters.Add("@Branch", SqlDbType.Int).Value = resvd.BranchID;
                                sqlCommand.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = resvd.Notes;
                                sqlCommand.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = resvd.EntryGlobalID;
                                sqlCommand.ExecuteNonQuery();
                                Interaction.MsgBox("تمت العمليات بنجاح ");
                        }
                        return true;
                }

                public bool SaveReceipt1(resvd rs, Entry Entr, bool IsNew)
                {
                        // P7-001 fix: الحجز بلا قيده مرفوض (fail-closed) — كان القيد
                        // امتيازاً اختيارياً: null يمرر الحفظ كاملاً ثم تعود الدالة true
                        if (Entr == null)
                        {
                                string text0;
                                text0 = "لا يمكن حفظ الاستحقاق دون قيده";
                                if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                {
                                        text0 = "cannot save the accrual without its entry";
                                }
                                MessageBox.Show(text0, "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                return false;
                        }
                        new SqlCommand();
                        new SqlDataAdapter();
                        DataTable dataTable;
                        dataTable = new DataTable();
                        SqlConnection sqlConnection;
                        sqlConnection = MainClass.ConnObj();
                        if (sqlConnection.State != ConnectionState.Open)
                        {
                                sqlConnection.Open();
                        }
                        bool result;
                        SqlTransaction sqlTransaction;
                        sqlTransaction = null;
                        try
                        {
                                SqlCommand sqlCommand;
                                sqlCommand = new SqlCommand("select GlobalID from Salary_Res where id=@id", sqlConnection);
                                sqlCommand.Parameters.Add("@id", SqlDbType.Int).Value = rs._id;
                                new SqlDataAdapter(sqlCommand).Fill(dataTable);
                                if (dataTable.Rows.Count > 0)
                                {
                                        IsNew = false;
                                }
                                // P3-003 fix: معاملة واحدة لحجز الراتب وقيده — لا كتابة بعد التحقق
                                // خارجها ولا افتراق بين الحجز وقيمه المحاسبية
                                sqlTransaction = sqlConnection.BeginTransaction();
                                if (IsNew)
                                {
                                        sqlCommand = new SqlCommand("insert into Salary_Res(id,GlobalID,date,month,year,IS_Deleted,branch,notes,EntryGlobalID) values(@id,@GlobalID,@date,@month,@year,@IS_Deleted,@branch,@notes,@EntryGlobalID)", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.Add("@id", SqlDbType.Int).Value = rs._id;
                                        sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = rs.GlobalID;
                                        sqlCommand.Parameters.Add("@date", SqlDbType.DateTime).Value = rs.ReceiptDate;
                                        sqlCommand.Parameters.Add("@month", SqlDbType.Int).Value = rs._Month;
                                        sqlCommand.Parameters.Add("@year", SqlDbType.Int).Value = rs._year;
                                        sqlCommand.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value = rs.ISDeleted;
                                        sqlCommand.Parameters.Add("@Branch", SqlDbType.Int).Value = rs.BranchID;
                                        sqlCommand.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = rs.Notes;
                                        sqlCommand.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = rs.EntryGlobalID;
                                        sqlCommand.ExecuteNonQuery();
                                }
                                else
                                {
                                        sqlCommand = new SqlCommand("update  Salary_Res set date=@date,month=@month,year=@year,branch=@branch,notes=@notes,EntryGlobalID=@EntryGlobalID where GlobalID=@GlobalID", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = rs.GlobalID;
                                        sqlCommand.Parameters.Add("@date", SqlDbType.DateTime).Value = rs.ReceiptDate;
                                        sqlCommand.Parameters.Add("@month", SqlDbType.Int).Value = rs._Month;
                                        sqlCommand.Parameters.Add("@year", SqlDbType.Int).Value = rs._year;
                                        sqlCommand.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value = rs.ISDeleted;
                                        sqlCommand.Parameters.Add("@Branch", SqlDbType.Int).Value = rs.BranchID;
                                        sqlCommand.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = rs.Notes;
                                        sqlCommand.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = rs.EntryGlobalID;
                                        sqlCommand.ExecuteNonQuery();
                                }
                                sqlCommand = new SqlCommand("select GlobalID from Salary_Res_Details where GlobalID=@GlobalID and res_emp=@res_emp", sqlConnection, sqlTransaction);
                                sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = rs.GlobalID;
                                sqlCommand.Parameters.Add("@res_emp", SqlDbType.Int).Value = rs._res_emp;
                                new SqlDataAdapter();
                                DataTable dataTable2;
                                dataTable2 = new DataTable();
                                bool flag;
                                flag = true;
                                new SqlDataAdapter(sqlCommand).Fill(dataTable2);
                                if (dataTable2.Rows.Count > 0)
                                {
                                        flag = false;
                                }
                                if (flag)
                                {
                                        if (sqlConnection.State != ConnectionState.Open)
                                        {
                                                sqlConnection.Open();
                                        }
                                        sqlCommand = new SqlCommand("insert into Salary_Res_Details(GlobalID,res_emp,Basic,Houses,Travel,sal_add,sal_sub,Net) values(@GlobalID,@res_emp,@Basic,@Houses,@Travel,@sal_add,@sal_sub,@Net)", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = rs.GlobalID;
                                        sqlCommand.Parameters.Add("@res_emp", SqlDbType.Int).Value = rs._res_emp;
                                        sqlCommand.Parameters.Add("@Basic", SqlDbType.Float).Value = rs._Basic;
                                        sqlCommand.Parameters.Add("@Houses", SqlDbType.Float).Value = rs._Houses;
                                        sqlCommand.Parameters.Add("@Travel", SqlDbType.Float).Value = rs._Travel;
                                        sqlCommand.Parameters.Add("@sal_add", SqlDbType.Float).Value = rs._saladd;
                                        sqlCommand.Parameters.Add("@sal_sub", SqlDbType.Float).Value = rs._salsub;
                                        sqlCommand.Parameters.Add("@Net", SqlDbType.Float).Value = rs._Net;
                                }
                                else
                                {
                                        if (sqlConnection.State != ConnectionState.Open)
                                        {
                                                sqlConnection.Open();
                                        }
                                        sqlCommand = new SqlCommand("update  Salary_Res_Details set res_emp=@res_emp,Basic=@Basic,Houses=@Houses,Travel=@Travel,sal_add=@sal_add,sal_sub=@sal_sub,Net=@Net where GlobalID=@GlobalID and res_emp=@res_emp ", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = rs.GlobalID;
                                        sqlCommand.Parameters.Add("@res_emp", SqlDbType.Int).Value = rs._res_emp;
                                        sqlCommand.Parameters.Add("@Basic", SqlDbType.Float).Value = rs._Basic;
                                        sqlCommand.Parameters.Add("@Houses", SqlDbType.Float).Value = rs._Houses;
                                        sqlCommand.Parameters.Add("@Travel", SqlDbType.Float).Value = rs._Travel;
                                        sqlCommand.Parameters.Add("@sal_add", SqlDbType.Float).Value = rs._saladd;
                                        sqlCommand.Parameters.Add("@sal_sub", SqlDbType.Float).Value = rs._salsub;
                                        sqlCommand.Parameters.Add("@Net", SqlDbType.Float).Value = rs._Net;
                                }
                                sqlCommand.ExecuteNonQuery();
                                // P3-003 fix: القيد داخل معاملة الحجز نفسها ونية المستدعي الصريحة
                                // (IsNew بعد تسوية فحص الوجود) — النجاح يعتمد الحجز وقيمه معاً
                                // P7-001 fix: Entr مضمون غير فارغ بحارس بداية الدالة
                                if (!new EntryOper().SaveEnty(Entr, sqlConnection, sqlTransaction, IsNew))
                                {
                                        try
                                        {
                                                sqlTransaction.Rollback();
                                        }
                                        catch
                                        {
                                        }
                                        string text;
                                        text = "خطأ أثناء الحفظ";
                                        if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                        {
                                                text = "error in saving";
                                        }
                                        MessageBox.Show(text, "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                        result = false;
                                }
                                else
                                {
                                        sqlTransaction.Commit();
                                        result = true;
                                }
                        }
                        catch (Exception ex)
                        {
                                ProjectData.SetProjectError(ex);
                                // P3-003 fix: تراجع حراس عن أي كتابة معلّقة ثم رسالة الخطأ
                                try
                                {
                                        sqlTransaction?.Rollback();
                                }
                                catch
                                {
                                }
                                Exception ex2;
                                ex2 = ex;
                                string text2;
                                text2 = "خطأ أثناء حفظ القيد";
                                if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                {
                                        text2 = "error in saving";
                                }
                                MessageBox.Show((Operators.CompareString(MainClass.Language, "ar", TextCompare: false) != 0) ? (text2 + Environment.NewLine + "Error details: " + ex2.Message) : (text2 + Environment.NewLine + "تفاصيل الخطأ: " + ex2.Message), "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                result = false;
                                ProjectData.ClearProjectError();
                        }
                        finally
                        {
                                if (sqlConnection.State != ConnectionState.Closed)
                                {
                                        sqlConnection.Close();
                                }
                        }
                        return result;
                }

                // P7-001 fix: رابط مطبوع بصفوف الشاشة نفسها (SalaryRow) — المسار القديم
                // كان يقيد عناصر ArrayList كـDataRow فيرمي استثناءً في أول صف ويعيد
                // null، ثم يمرر الشاشة null إلى الحفظ فيتم الاستحقاق بلا قيد ويعلن
                // النجاح. البناء الآن لكل صف موجب الصافي: دائن حساب الموظف (AccCode)
                // ومدين حساب التكلفة (DebitAcc) — قيد المجموعة يُبنى مرة واحدة.
                public Entry BindreservedToEntry(resvd Receipt, System.Collections.Generic.List<SmartAuditERP.Form_WPF.FrmReseved.SalaryRow> rows)
                {
                        checked
                        {
                                Entry result;
                                try
                                {
                                        Entry entry;
                                        entry = new Entry();
                                        List<Account> list;
                                        list = new List<Account>();
                                        new Account();
                                        new resvd();
                                        entry.EntryGlobalID = Receipt.EntryGlobalID;
                                        entry.ClientCode = Sync.ClientCode;
                                        entry.EntryNo = Conversions.ToInteger(Receipt.EntryGlobalID.Substring(Receipt.EntryGlobalID.LastIndexOf("-") + 1));
                                        entry.EntryDate = Receipt.ReceiptDate;
                                        entry.ReffNo = Conversions.ToString(Receipt._id);
                                        entry.RefDate = Receipt.ReceiptDate;
                                        entry.Type = unchecked((EntryType)Receipt.ReceiptType);
                                        entry.State = 1;
                                        entry.Note = Receipt.Notes;
                                        entry.Branch = Receipt.BranchID;
                                        entry.EmpID = MainClass.EmpNo;
                                        entry.DistBranch = Sync.DistBranch;
                                        entry.BranchType = Sync.BranchType;
                                        foreach (SmartAuditERP.Form_WPF.FrmReseved.SalaryRow current in rows)
                                        {
                                                if (decimal.Compare(current.Net_Sal, 0m) > 0)
                                                {
                                                        Account account;
                                                        account = new Account();
                                                        account.EntryGlobalID = entry.EntryGlobalID;
                                                        account.EntryNo = entry.EntryNo;
                                                        account.Name = Conversions.ToString(current.AccCode);
                                                        account.Code = Conversions.ToString(current.AccCode);
                                                        account.Debt = 0.0;
                                                        account.Credit = Convert.ToDouble(current.Net_Sal);
                                                        account.Note = Receipt.Notes;
                                                        account.CCcode = Conversions.ToString(-1);
                                                        list.Add(account);
                                                        account = new Account();
                                                        account.EntryGlobalID = entry.EntryGlobalID;
                                                        account.EntryNo = entry.EntryNo;
                                                        account.Name = Receipt.DebitAcc;
                                                        account.Code = Receipt.DebitAcc;
                                                        account.Debt = Convert.ToDouble(current.Net_Sal);
                                                        account.Credit = 0.0;
                                                        account.Note = Receipt.Notes;
                                                        account.CCcode = Receipt.Cccode;
                                                        list.Add(account);
                                                }
                                        }
                                        entry.Accounts = list;
                                        result = entry;
                                }
                                catch (Exception ex)
                                {
                                        ProjectData.SetProjectError(ex);
                                        Exception ex2;
                                        ex2 = ex;
                                        string text;
                                        text = "error in Binding data";
                                        if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                        {
                                                text = "error in Binding data";
                                        }
                                        MessageBox.Show((Operators.CompareString(MainClass.Language, "ar", TextCompare: false) != 0) ? (text + Environment.NewLine + "Error details: " + ex2.Message) : (text + Environment.NewLine + "تفاصيل الخطأ: " + ex2.Message), "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                        result = null;
                                        ProjectData.ClearProjectError();
                                }
                                return result;
                        }
                }

                // P7-001 fix: استحقاق المجموعة وقيدها نتيجة واحدة: رأس Salary_Res
                // يُكتب مرة (لا مرة لكل موظف)، تفاصيل كل موظف بالوجود المحروس
                // (UPDLOCK+HOLDLOCK)، والقيد الواحد للدفعة كلها — كل ذلك داخل
                // معاملة واحدة، والقيد شرط النجاح (Entr==null = رفض). النتيجة
                // bool تفحصها الشاشة قبل أي رسالة نجاح.
                public bool SaveReceipts(System.Collections.Generic.List<resvd> rows, Entry Entr, bool IsNew)
                {
                        bool result;
                        SqlConnection sqlConnection;
                        sqlConnection = MainClass.ConnObj();
                        if (sqlConnection.State != ConnectionState.Open)
                        {
                                sqlConnection.Open();
                        }
                        SqlTransaction sqlTransaction;
                        sqlTransaction = null;
                        try
                        {
                                if (rows == null || rows.Count == 0 || Entr == null)
                                {
                                        string text0;
                                        text0 = "لا يوجد ما يُحفظ أو القيد مفقود";
                                        if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                        {
                                                text0 = "nothing to save or the entry is missing";
                                        }
                                        MessageBox.Show(text0, "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                        result = false;
                                }
                                else
                                {
                                        sqlTransaction = sqlConnection.BeginTransaction();
                                        resvd rs;
                                        rs = rows[0];
                                        SqlCommand sqlCommand;
                                        sqlCommand = new SqlCommand("select GlobalID from Salary_Res with (UPDLOCK, HOLDLOCK) where id=@id", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.Add("@id", SqlDbType.Int).Value = rs._id;
                                        DataTable dataTable;
                                        dataTable = new DataTable();
                                        new SqlDataAdapter(sqlCommand).Fill(dataTable);
                                        if (dataTable.Rows.Count > 0)
                                        {
                                                IsNew = false;
                                        }
                                        if (IsNew)
                                        {
                                                sqlCommand = new SqlCommand("insert into Salary_Res(id,GlobalID,date,month,year,IS_Deleted,branch,notes,EntryGlobalID) values(@id,@GlobalID,@date,@month,@year,@IS_Deleted,@branch,@notes,@EntryGlobalID)", sqlConnection, sqlTransaction);
                                        }
                                        else
                                        {
                                                sqlCommand = new SqlCommand("update  Salary_Res set date=@date,month=@month,year=@year,branch=@branch,notes=@notes,EntryGlobalID=@EntryGlobalID where GlobalID=@GlobalID", sqlConnection, sqlTransaction);
                                        }
                                        sqlCommand.Parameters.Add("@id", SqlDbType.Int).Value = rs._id;
                                        sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = rs.GlobalID;
                                        sqlCommand.Parameters.Add("@date", SqlDbType.DateTime).Value = rs.ReceiptDate;
                                        sqlCommand.Parameters.Add("@month", SqlDbType.Int).Value = rs._Month;
                                        sqlCommand.Parameters.Add("@year", SqlDbType.Int).Value = rs._year;
                                        sqlCommand.Parameters.Add("@IS_Deleted", SqlDbType.Bit).Value = rs.ISDeleted;
                                        sqlCommand.Parameters.Add("@Branch", SqlDbType.Int).Value = rs.BranchID;
                                        sqlCommand.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = rs.Notes;
                                        sqlCommand.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = rs.EntryGlobalID;
                                        sqlCommand.ExecuteNonQuery();
                                        foreach (resvd current in rows)
                                        {
                                                sqlCommand = new SqlCommand("select GlobalID from Salary_Res_Details with (UPDLOCK, HOLDLOCK) where GlobalID=@GlobalID and res_emp=@res_emp", sqlConnection, sqlTransaction);
                                                sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = current.GlobalID;
                                                sqlCommand.Parameters.Add("@res_emp", SqlDbType.Int).Value = current._res_emp;
                                                DataTable dataTable2;
                                                dataTable2 = new DataTable();
                                                new SqlDataAdapter(sqlCommand).Fill(dataTable2);
                                                bool flag;
                                                flag = dataTable2.Rows.Count == 0;
                                                if (flag)
                                                {
                                                        sqlCommand = new SqlCommand("insert into Salary_Res_Details(GlobalID,res_emp,Basic,Houses,Travel,sal_add,sal_sub,Net) values(@GlobalID,@res_emp,@Basic,@Houses,@Travel,@sal_add,@sal_sub,@Net)", sqlConnection, sqlTransaction);
                                                }
                                                else
                                                {
                                                        sqlCommand = new SqlCommand("update  Salary_Res_Details set res_emp=@res_emp,Basic=@Basic,Houses=@Houses,Travel=@Travel,sal_add=@sal_add,sal_sub=@sal_sub,Net=@Net where GlobalID=@GlobalID and res_emp=@res_emp ", sqlConnection, sqlTransaction);
                                                }
                                                sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = current.GlobalID;
                                                sqlCommand.Parameters.Add("@res_emp", SqlDbType.Int).Value = current._res_emp;
                                                sqlCommand.Parameters.Add("@Basic", SqlDbType.Float).Value = current._Basic;
                                                sqlCommand.Parameters.Add("@Houses", SqlDbType.Float).Value = current._Houses;
                                                sqlCommand.Parameters.Add("@Travel", SqlDbType.Float).Value = current._Travel;
                                                sqlCommand.Parameters.Add("@sal_add", SqlDbType.Float).Value = current._saladd;
                                                sqlCommand.Parameters.Add("@sal_sub", SqlDbType.Float).Value = current._salsub;
                                                sqlCommand.Parameters.Add("@Net", SqlDbType.Float).Value = current._Net;
                                                sqlCommand.ExecuteNonQuery();
                                        }
                                        // P7-001 fix: القيد شرط الالتزام — فشله يتراجع بكل الحجز
                                        if (!new EntryOper().SaveEnty(Entr, sqlConnection, sqlTransaction, IsNew))
                                        {
                                                try
                                                {
                                                        sqlTransaction.Rollback();
                                                }
                                                catch
                                                {
                                                }
                                                string text;
                                                text = "خطأ أثناء الحفظ";
                                                if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                                {
                                                        text = "error in saving";
                                                }
                                                MessageBox.Show(text, "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                                result = false;
                                        }
                                        else
                                        {
                                                sqlTransaction.Commit();
                                                result = true;
                                        }
                                }
                        }
                        catch (Exception ex)
                        {
                                ProjectData.SetProjectError(ex);
                                // P3-003 fix: تراجع حراس عن أي كتابة معلّقة ثم رسالة الخطأ
                                try
                                {
                                        sqlTransaction?.Rollback();
                                }
                                catch
                                {
                                }
                                Exception ex2;
                                ex2 = ex;
                                string text2;
                                text2 = "خطأ أثناء حفظ الاستحقاق";
                                if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
                                {
                                        text2 = "error in saving";
                                }
                                MessageBox.Show((Operators.CompareString(MainClass.Language, "ar", TextCompare: false) != 0) ? (text2 + Environment.NewLine + "Error details: " + ex2.Message) : (text2 + Environment.NewLine + "تفاصيل الخطأ: " + ex2.Message), "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
                                result = false;
                                ProjectData.ClearProjectError();
                        }
                        finally
                        {
                                if (sqlConnection.State != ConnectionState.Closed)
                                {
                                        sqlConnection.Close();
                                }
                        }
                        return result;
                }
        }
}