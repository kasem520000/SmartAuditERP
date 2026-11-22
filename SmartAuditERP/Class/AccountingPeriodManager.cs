using System;
using System.Collections.Generic;
using System.Data.SqlClient;
using System.Runtime.CompilerServices;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace SmartAuditERP
{

        public class AccountingPeriodManager
        {
                private string connectionString;

                public AccountingPeriodManager(string connString)
                {
                        this.connectionString = "Your Connection String Here";
                        this.connectionString = connString;
                }

                public AccountingPeriod GetActivePeriod()
                {
                        using (SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString))
                        {
                                SqlCommand sqlCommand;
                                sqlCommand = new SqlCommand("SELECT TOP 1 * FROM AccountingPeriods WHERE IsActive = 1", sqlConnection);
                                sqlConnection.Open();
                                SqlDataReader sqlDataReader;
                                sqlDataReader = sqlCommand.ExecuteReader();
                                if (sqlDataReader.Read())
                                {
                                        return new AccountingPeriod
                                        {
                                                PeriodID = Conversions.ToInteger(sqlDataReader["PeriodID"]),
                                                PeriodName = sqlDataReader["PeriodName"].ToString(),
                                                StartDate = Conversions.ToDate(sqlDataReader["StartDate"]),
                                                EndDate = Conversions.ToDate(sqlDataReader["EndDate"]),
                                                IsClosed = Conversions.ToBoolean(sqlDataReader["IsClosed"]),
                                                IsActive = Conversions.ToBoolean(sqlDataReader["IsActive"]),
                                                Notes = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["Notes"])) ? "" : sqlDataReader["Notes"].ToString())
                                        };
                                }
                        }
                        return null;
                }

                public bool AddPeriod(AccountingPeriod period)
                {
                        try
                        {
                            using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                            sqlConnection.Open();
                            // P3-017 fix: فحص التداخل + إلغاء التفعيل + الإدراج معاملة واحدة
                            // بتلميحات قفل — ذرية كاملة لا تتيح فترتين نشطتين بالتزامن
                            using SqlTransaction sqlTransaction = sqlConnection.BeginTransaction();
                            try
                            {
                                        if (this.CheckDateOverlap(period.StartDate, period.EndDate, 0, sqlConnection, sqlTransaction))
                                        {
                                            throw new Exception("يوجد تداخل في التواريخ مع فترة محاسبية أخرى");
                                        }
                                        SqlCommand sqlCommand;
                                        sqlCommand = new SqlCommand("INSERT INTO AccountingPeriods (PeriodName, StartDate, EndDate, IsActive, Notes) VALUES (@Name, @Start, @End, @Active, @Notes)", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.AddWithValue("@Name", period.PeriodName);
                                        sqlCommand.Parameters.AddWithValue("@Start", period.StartDate);
                                        sqlCommand.Parameters.AddWithValue("@End", period.EndDate);
                                        sqlCommand.Parameters.AddWithValue("@Active", period.IsActive);
                                        sqlCommand.Parameters.AddWithValue("@Notes", RuntimeHelpers.GetObjectValue(string.IsNullOrEmpty(period.Notes) ? ((IConvertible)DBNull.Value) : ((IConvertible)period.Notes)));
                                        if (period.IsActive)
                                        {
                                            new SqlCommand("UPDATE AccountingPeriods SET IsActive = 0", sqlConnection, sqlTransaction).ExecuteNonQuery();
                                        }
                                        bool result = sqlCommand.ExecuteNonQuery() > 0;
                                        sqlTransaction.Commit();
                                        return result;
                            }
                            catch
                            {
                                        sqlTransaction.Rollback();
                                        throw;
                            }
                        }
                        catch (Exception ex)
                        {
                            ProjectData.SetProjectError(ex);
                            throw new Exception("خطأ في إضافة الفترة المحاسبية: " + ex.Message);
                        }
                }

                public bool UpdatePeriod(AccountingPeriod period)
                {
                        try
                        {
                            using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                            sqlConnection.Open();
                            // P3-017 fix: فحص التداخل + التحديث + إلغاء التفعيل معاملة واحدة
                            using SqlTransaction sqlTransaction = sqlConnection.BeginTransaction();
                            try
                            {
                                        if (this.CheckDateOverlap(period.StartDate, period.EndDate, period.PeriodID, sqlConnection, sqlTransaction))
                                        {
                                            throw new Exception("يوجد تداخل في التواريخ مع فترة محاسبية أخرى");
                                        }
                                        SqlCommand sqlCommand;
                                        sqlCommand = new SqlCommand("UPDATE AccountingPeriods SET PeriodName = @Name, StartDate = @Start, EndDate = @End, IsActive = @Active, Notes = @Notes WHERE PeriodID = @ID", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.AddWithValue("@ID", period.PeriodID);
                                        sqlCommand.Parameters.AddWithValue("@Name", period.PeriodName);
                                        sqlCommand.Parameters.AddWithValue("@Start", period.StartDate);
                                        sqlCommand.Parameters.AddWithValue("@End", period.EndDate);
                                        sqlCommand.Parameters.AddWithValue("@Active", period.IsActive);
                                        sqlCommand.Parameters.AddWithValue("@Notes", RuntimeHelpers.GetObjectValue(string.IsNullOrEmpty(period.Notes) ? ((IConvertible)DBNull.Value) : ((IConvertible)period.Notes)));
                                        if (period.IsActive)
                                        {
                                            SqlCommand sqlCommand2;
                                            sqlCommand2 = new SqlCommand("UPDATE AccountingPeriods SET IsActive = 0 WHERE PeriodID <> @ID", sqlConnection, sqlTransaction);
                                            sqlCommand2.Parameters.AddWithValue("@ID", period.PeriodID);
                                            sqlCommand2.ExecuteNonQuery();
                                        }
                                        bool result = sqlCommand.ExecuteNonQuery() > 0;
                                        sqlTransaction.Commit();
                                        return result;
                            }
                            catch
                            {
                                        sqlTransaction.Rollback();
                                        throw;
                            }
                        }
                        catch (Exception ex)
                        {
                            ProjectData.SetProjectError(ex);
                            throw new Exception("خطأ في تحديث الفترة المحاسبية: " + ex.Message);
                        }
                }

                public bool ClosePeriod(int periodID, string userName)
                {
                        try
                        {
                                using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                                SqlCommand sqlCommand;
                                sqlCommand = new SqlCommand("UPDATE AccountingPeriods SET IsClosed = 1, ClosedBy = @User, ClosedDate = @Date, IsActive = 0 WHERE PeriodID = @ID", sqlConnection);
                                sqlCommand.Parameters.AddWithValue("@ID", periodID);
                                sqlCommand.Parameters.AddWithValue("@User", userName);
                                sqlCommand.Parameters.AddWithValue("@Date", DateTime.Now);
                                sqlConnection.Open();
                                return sqlCommand.ExecuteNonQuery() > 0;
                        }
                        catch (Exception ex)
                        {
                                ProjectData.SetProjectError(ex);
                                throw new Exception("خطأ في إغلاق الفترة المحاسبية: " + ex.Message);
                        }
                }

                public bool ReopenPeriod(int periodID, string reopenedBy)
                {
                        try
                        {
                            using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                            // P3-018 fix: إعادة الفتح لا تمحو سجل الإقفال — ClosedBy/ClosedDate
                            // يبقيان شهادة من أقفل ومتى؛ هوية إعادة الفتح وتاريخها وعدّادها
                            // يُسجَّلان بالأعمدة الجديدة (AlterDb) بهوية المستخدم التطبيقية
                            SqlCommand sqlCommand;
                            sqlCommand = new SqlCommand("UPDATE AccountingPeriods SET IsClosed = 0, ReopenedBy = @ReopenedBy, ReopenedDate = @ReopenedDate, ReopenCount = ISNULL(ReopenCount, 0) + 1 WHERE PeriodID = @ID", sqlConnection);
                            sqlCommand.Parameters.AddWithValue("@ID", periodID);
                            sqlCommand.Parameters.AddWithValue("@ReopenedBy", reopenedBy ?? "");
                            sqlCommand.Parameters.AddWithValue("@ReopenedDate", DateTime.Now);
                            sqlConnection.Open();
                            return sqlCommand.ExecuteNonQuery() > 0;
                        }
                        catch (Exception ex)
                        {
                            ProjectData.SetProjectError(ex);
                            throw new Exception("خطأ في إعادة فتح الفترة المحاسبية: " + ex.Message);
                        }
                }

                public bool ActivatePeriod(int periodID)
                {
                        try
                        {
                            using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                            sqlConnection.Open();
                            // P3-017 fix: التفعيل عملية ذرية واحدة: فحص الإغلاق + فحص التداخل
                            // مع الفترة النشطة + إلغاء التفعيل + التفعيل — الكل داخل معاملة
                            // بتلميحات قفل فلا تتزامن فترتان نشطتان ولا يتخلل الحالة تحديث ناقص
                            using SqlTransaction sqlTransaction = sqlConnection.BeginTransaction();
                            try
                            {
                                        SqlCommand sqlCommand;
                                        sqlCommand = new SqlCommand("SELECT IsClosed, StartDate, EndDate FROM AccountingPeriods WITH (UPDLOCK, HOLDLOCK) WHERE PeriodID = @ID", sqlConnection, sqlTransaction);
                                        sqlCommand.Parameters.AddWithValue("@ID", periodID);
                                        using SqlDataReader reader = sqlCommand.ExecuteReader();
                                        if (!reader.Read())
                                        {
                                            throw new Exception("الفترة المطلوبة غير موجودة");
                                        }
                                        if (Conversions.ToBoolean(reader["IsClosed"]))
                                        {
                                            throw new Exception("لا يمكن تفعيل فترة محاسبية مغلقة");
                                        }
                                        DateTime start = Conversions.ToDate(reader["StartDate"]);
                                        DateTime end = Conversions.ToDate(reader["EndDate"]);
                                        reader.Close();
                                        // P3-017 fix: فترة تتداخل زمنياً مع فترة نشطة أخرى = رفض
                                        SqlCommand overlapCmd = new SqlCommand("SELECT COUNT(*) FROM AccountingPeriods WITH (UPDLOCK, HOLDLOCK) WHERE IsActive = 1 AND PeriodID <> @ID AND (StartDate <= @End AND EndDate >= @Start)", sqlConnection, sqlTransaction);
                                        overlapCmd.Parameters.AddWithValue("@ID", periodID);
                                        overlapCmd.Parameters.AddWithValue("@Start", start);
                                        overlapCmd.Parameters.AddWithValue("@End", end);
                                        if (Conversions.ToInteger(overlapCmd.ExecuteScalar()) > 0)
                                        {
                                            throw new Exception("لا يمكن تفعيل فترة تتداخل مع فترة نشطة أخرى");
                                        }
                                        new SqlCommand("UPDATE AccountingPeriods SET IsActive = 0", sqlConnection, sqlTransaction).ExecuteNonQuery();
                                        SqlCommand sqlCommand2;
                                        sqlCommand2 = new SqlCommand("UPDATE AccountingPeriods SET IsActive = 1 WHERE PeriodID = @ID", sqlConnection, sqlTransaction);
                                        sqlCommand2.Parameters.AddWithValue("@ID", periodID);
                                        bool result = sqlCommand2.ExecuteNonQuery() > 0;
                                        sqlTransaction.Commit();
                                        return result;
                            }
                            catch
                            {
                                        sqlTransaction.Rollback();
                                        throw;
                            }
                        }
                        catch (Exception ex)
                        {
                            ProjectData.SetProjectError(ex);
                            throw new Exception("خطأ في تفعيل الفترة المحاسبية: " + ex.Message);
                        }
                }

                public List<AccountingPeriod> GetAllPeriods()
                {
                        List<AccountingPeriod> list;
                        list = new List<AccountingPeriod>();
                        using (SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString))
                        {
                                SqlCommand sqlCommand;
                                sqlCommand = new SqlCommand("SELECT * FROM AccountingPeriods ORDER BY StartDate DESC", sqlConnection);
                                sqlConnection.Open();
                                SqlDataReader sqlDataReader;
                                sqlDataReader = sqlCommand.ExecuteReader();
                                while (sqlDataReader.Read())
                                {
                                        list.Add(new AccountingPeriod
                                        {
                                                PeriodID = Conversions.ToInteger(sqlDataReader["PeriodID"]),
                                                PeriodName = sqlDataReader["PeriodName"].ToString(),
                                                StartDate = Conversions.ToDate(sqlDataReader["StartDate"]),
                                                EndDate = Conversions.ToDate(sqlDataReader["EndDate"]),
                                                IsClosed = Conversions.ToBoolean(sqlDataReader["IsClosed"]),
                                                IsActive = Conversions.ToBoolean(sqlDataReader["IsActive"]),
                                                ClosedBy = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["ClosedBy"])) ? "" : sqlDataReader["ClosedBy"].ToString()),
                                                ClosedDate = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["ClosedDate"])) ? DateTime.MinValue : Conversions.ToDate(sqlDataReader["ClosedDate"])),
                                // P3-018 fix: قراءة سجل إعادة الفتح للأعمدة الجديدة
                                ReopenedBy = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["ReopenedBy"])) ? "" : sqlDataReader["ReopenedBy"].ToString()),
                                ReopenedDate = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["ReopenedDate"])) ? null : new DateTime?(Conversions.ToDate(sqlDataReader["ReopenedDate"]))),
                                ReopenCount = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["ReopenCount"])) ? 0 : Conversions.ToInteger(sqlDataReader["ReopenCount"])),
                                                Notes = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["Notes"])) ? "" : sqlDataReader["Notes"].ToString()),
                                                CreatedDate = Conversions.ToDate(sqlDataReader["CreatedDate"])
                                        });
                                }
                        }
                        return list;
                }

                private bool CheckDateOverlap(DateTime startDate, DateTime endDate, int excludePeriodID)
                {
                        using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                        SqlCommand sqlCommand;
                        sqlCommand = new SqlCommand("SELECT COUNT(*) FROM AccountingPeriods WHERE PeriodID <> @ExcludeID AND ((StartDate <= @End AND EndDate >= @Start))", sqlConnection);
                        sqlCommand.Parameters.AddWithValue("@ExcludeID", excludePeriodID);
                        sqlCommand.Parameters.AddWithValue("@Start", startDate);
                        sqlCommand.Parameters.AddWithValue("@End", endDate);
                        sqlConnection.Open();
                        return Conversions.ToInteger(sqlCommand.ExecuteScalar()) > 0;
                }
                // P3-017 fix: فحص التداخل داخل المعاملة — نفس الفحص بتلميحات قفل
                private bool CheckDateOverlap(DateTime startDate, DateTime endDate, int excludePeriodID, SqlConnection conn, SqlTransaction tx)
                {
                        SqlCommand sqlCommand;
                        sqlCommand = new SqlCommand("SELECT COUNT(*) FROM AccountingPeriods WITH (UPDLOCK, HOLDLOCK) WHERE PeriodID <> @ExcludeID AND ((StartDate <= @End AND EndDate >= @Start))", conn, tx);
                        sqlCommand.Parameters.AddWithValue("@ExcludeID", excludePeriodID);
                        sqlCommand.Parameters.AddWithValue("@Start", startDate);
                        sqlCommand.Parameters.AddWithValue("@End", endDate);
                        return Conversions.ToInteger(sqlCommand.ExecuteScalar()) > 0;
                }

                public bool ValidateTransactionDate(DateTime transDate)
                {
                        AccountingPeriod activePeriod;
                        activePeriod = this.GetActivePeriod();
                        if (activePeriod == null)
                        {
                                throw new Exception("لا توجد فترة محاسبية نشطة");
                        }
                        if (activePeriod.IsClosed)
                        {
                                throw new Exception("الفترة المحاسبية مغلقة");
                        }
                        if (DateTime.Compare(transDate, activePeriod.StartDate) < 0 || DateTime.Compare(transDate, activePeriod.EndDate) > 0)
                        {
                                throw new Exception("التاريخ خارج نطاق الفترة المحاسبية النشطة");
                        }
                        return true;
                }

                public bool DeletePeriod(int periodID)
                {
                        try
                        {
                                using SqlConnection sqlConnection = MainClass.CreateSqlConnection(this.connectionString);
                                SqlCommand sqlCommand;
                                sqlCommand = new SqlCommand("DELETE FROM AccountingPeriods WHERE PeriodID = @ID AND IsClosed = 0", sqlConnection);
                                sqlCommand.Parameters.AddWithValue("@ID", periodID);
                                sqlConnection.Open();
                                return sqlCommand.ExecuteNonQuery() > 0;
                        }
                        catch (Exception ex)
                        {
                                ProjectData.SetProjectError(ex);
                                throw new Exception("خطأ في حذف الفترة المحاسبية: " + ex.Message);
                        }
                }
        }
}