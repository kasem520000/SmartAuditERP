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
			using (SqlConnection sqlConnection = new SqlConnection(this.connectionString))
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
			// Repair R-039 (audit finding P3-017): activating an incoming period used to run the
			// mass-deactivate and the insert as two independent statements on an open connection -
			// a failure between them stranded the table with every period deactivated and the new
			// row missing. All writes of a method now share ONE transaction committed together.
			// (The cross-session overlap race and any schema-level uniqueness guard remain
			// recorded as owner-input barriers - they need server locking / schema change.)
			SqlTransaction transaction = null;
			try
			{
				using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
				if (this.CheckDateOverlap(period.StartDate, period.EndDate, 0))
				{
					throw new Exception("يوجد تداخل في التواريخ مع فترة محاسبية أخرى");
				}
				SqlCommand sqlCommand;
				sqlCommand = new SqlCommand("INSERT INTO AccountingPeriods (PeriodName, StartDate, EndDate, IsActive, Notes) VALUES (@Name, @Start, @End, @Active, @Notes)", sqlConnection);
				sqlCommand.Parameters.AddWithValue("@Name", period.PeriodName);
				sqlCommand.Parameters.AddWithValue("@Start", period.StartDate);
				sqlCommand.Parameters.AddWithValue("@End", period.EndDate);
				sqlCommand.Parameters.AddWithValue("@Active", period.IsActive);
				sqlCommand.Parameters.AddWithValue("@Notes", RuntimeHelpers.GetObjectValue(string.IsNullOrEmpty(period.Notes) ? ((IConvertible)DBNull.Value) : ((IConvertible)period.Notes)));
				sqlConnection.Open();
				transaction = sqlConnection.BeginTransaction();
				sqlCommand.Transaction = transaction;
				if (period.IsActive)
				{
					SqlCommand sqlCommandDeactivate;
					sqlCommandDeactivate = new SqlCommand("UPDATE AccountingPeriods SET IsActive = 0", sqlConnection);
					sqlCommandDeactivate.Transaction = transaction;
					sqlCommandDeactivate.ExecuteNonQuery();
				}
				bool added;
				added = sqlCommand.ExecuteNonQuery() > 0;
				transaction.Commit();
				return added;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				try { transaction?.Rollback(); } catch { }
				throw new Exception("خطأ في إضافة الفترة المحاسبية: " + ex.Message);
			}
		}

		public bool UpdatePeriod(AccountingPeriod period)
		{
			// R-039: same atomicity contract as AddPeriod for the update path.
			SqlTransaction transaction = null;
			try
			{
				using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
				if (this.CheckDateOverlap(period.StartDate, period.EndDate, period.PeriodID))
				{
					throw new Exception("يوجد تداخل في التواريخ مع فترة محاسبية أخرى");
				}
				SqlCommand sqlCommand;
				sqlCommand = new SqlCommand("UPDATE AccountingPeriods SET PeriodName = @Name, StartDate = @Start, EndDate = @End, IsActive = @Active, Notes = @Notes WHERE PeriodID = @ID", sqlConnection);
				sqlCommand.Parameters.AddWithValue("@ID", period.PeriodID);
				sqlCommand.Parameters.AddWithValue("@Name", period.PeriodName);
				sqlCommand.Parameters.AddWithValue("@Start", period.StartDate);
				sqlCommand.Parameters.AddWithValue("@End", period.EndDate);
				sqlCommand.Parameters.AddWithValue("@Active", period.IsActive);
				sqlCommand.Parameters.AddWithValue("@Notes", RuntimeHelpers.GetObjectValue(string.IsNullOrEmpty(period.Notes) ? ((IConvertible)DBNull.Value) : ((IConvertible)period.Notes)));
				sqlConnection.Open();
				transaction = sqlConnection.BeginTransaction();
				sqlCommand.Transaction = transaction;
				if (period.IsActive)
				{
					SqlCommand sqlCommand2;
					sqlCommand2 = new SqlCommand("UPDATE AccountingPeriods SET IsActive = 0 WHERE PeriodID <> @ID", sqlConnection);
					sqlCommand2.Transaction = transaction;
					sqlCommand2.Parameters.AddWithValue("@ID", period.PeriodID);
					sqlCommand2.ExecuteNonQuery();
				}
				bool updated;
				updated = sqlCommand.ExecuteNonQuery() > 0;
				transaction.Commit();
				return updated;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				try { transaction?.Rollback(); } catch { }
				throw new Exception("خطأ في تحديث الفترة المحاسبية: " + ex.Message);
			}
		}

		public bool ClosePeriod(int periodID, string userName)
		{
			try
			{
				using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
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

		public bool ReopenPeriod(int periodID)
		{
			try
			{
				using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
				SqlCommand sqlCommand;
				sqlCommand = new SqlCommand("UPDATE AccountingPeriods SET IsClosed = 0, ClosedBy = NULL, ClosedDate = NULL WHERE PeriodID = @ID", sqlConnection);
				sqlCommand.Parameters.AddWithValue("@ID", periodID);
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
			SqlTransaction transaction = null;
			try
			{
				using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
				sqlConnection.Open();
				// R-039: the guard, the mass-deactivate and the target activation now run inside
				// one transaction - a crash midway can no longer leave the ledger with ZERO active
				// accounting periods while the UI believes it activated one.
				transaction = sqlConnection.BeginTransaction();
				SqlCommand sqlCommand;
				sqlCommand = new SqlCommand("SELECT IsClosed FROM AccountingPeriods WHERE PeriodID = @ID", sqlConnection, transaction);
				sqlCommand.Parameters.AddWithValue("@ID", periodID);
				if (Conversions.ToBoolean(sqlCommand.ExecuteScalar()))
				{
					throw new Exception("لا يمكن تفعيل فترة محاسبية مغلقة");
				}
				SqlCommand sqlCommandClear;
				sqlCommandClear = new SqlCommand("UPDATE AccountingPeriods SET IsActive = 0", sqlConnection, transaction);
				sqlCommandClear.ExecuteNonQuery();
				SqlCommand sqlCommand2;
				sqlCommand2 = new SqlCommand("UPDATE AccountingPeriods SET IsActive = 1 WHERE PeriodID = @ID", sqlConnection, transaction);
				sqlCommand2.Parameters.AddWithValue("@ID", periodID);
				int affected;
				affected = sqlCommand2.ExecuteNonQuery();
				transaction.Commit();
				return affected > 0;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				try { transaction?.Rollback(); } catch { }
				throw new Exception("خطأ في تفعيل الفترة المحاسبية: " + ex.Message);
			}
		}

		public List<AccountingPeriod> GetAllPeriods()
		{
			List<AccountingPeriod> list;
			list = new List<AccountingPeriod>();
			using (SqlConnection sqlConnection = new SqlConnection(this.connectionString))
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
						Notes = (Information.IsDBNull(RuntimeHelpers.GetObjectValue(sqlDataReader["Notes"])) ? "" : sqlDataReader["Notes"].ToString()),
						CreatedDate = Conversions.ToDate(sqlDataReader["CreatedDate"])
					});
				}
			}
			return list;
		}

		private bool CheckDateOverlap(DateTime startDate, DateTime endDate, int excludePeriodID)
		{
			using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
			SqlCommand sqlCommand;
			sqlCommand = new SqlCommand("SELECT COUNT(*) FROM AccountingPeriods WHERE PeriodID <> @ExcludeID AND ((StartDate <= @End AND EndDate >= @Start))", sqlConnection);
			sqlCommand.Parameters.AddWithValue("@ExcludeID", excludePeriodID);
			sqlCommand.Parameters.AddWithValue("@Start", startDate);
			sqlCommand.Parameters.AddWithValue("@End", endDate);
			sqlConnection.Open();
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
				using SqlConnection sqlConnection = new SqlConnection(this.connectionString);
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