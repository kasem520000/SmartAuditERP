using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.IO;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using System.Windows.Forms;
using AuditorAPI.Models;
using SmartAuditERP.Form_WPF;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace SmartAuditERP
{

	public class ReceiptOper
	{
		public static string[] filePathDocument;

		public Entry BindReceiptToEntry(Receipt Receipt)
		{
			Entry result;
			try
			{
				Entry entry;
				entry = new Entry();
				List<Account> list;
				list = new List<Account>();
				new Account();
				entry.EntryGlobalID = Receipt.EntryGlobalID;
				entry.ClientCode = Sync.ClientCode;
				entry.EntryNo = Conversions.ToInteger(Receipt.EntryGlobalID.Substring(checked(Receipt.EntryGlobalID.LastIndexOf("-") + 1)));
				entry.EntryDate = Receipt.ReceiptDate.Value;
				entry.ReffNo = Conversions.ToString(Receipt.ReceiptNo);
				entry.RefDate = Receipt.ReceiptDate.Value;
				entry.Type = (EntryType)Receipt.ReceiptType.Value;
				entry.State = 1;
				entry.Note = Receipt.Notes;
				entry.Branch = Receipt.BranchID.Value;
				entry.EmpID = Receipt.EmpId.Value;
				entry.DistBranch = Sync.DistBranch;
				entry.BranchType = Sync.BranchType;
				double? payment;
				payment = Receipt.Payment;
				if ((payment.HasValue ? new bool?(payment.GetValueOrDefault() > 0.0) : ((bool?)null)) == true)
				{
					Account account;
					account = new Account();
					account.EntryGlobalID = entry.EntryGlobalID;
					account.EntryNo = entry.EntryNo;
					account.Name = Receipt.CreditAcc;
					account.Code = Receipt.CreditAcc;
					account.Debt = 0.0;
					account.Credit = Receipt.NetVal.Value;
					account.Note = Receipt.Notes;
					int? receiptType;
					receiptType = Receipt.ReceiptType;
					bool? flag;
					flag = (receiptType.HasValue ? new bool?(receiptType == 5) : ((bool?)null));
					receiptType = Receipt.ReceiptType;
					bool? flag2;
					flag2 = (receiptType.HasValue ? new bool?(receiptType == 7) : ((bool?)null));
					if (((flag ?? false) ? new bool?(true) : ((!flag2.HasValue) ? ((bool?)null) : ((flag2 == true) | flag))) == true)
					{
						account.CCcode = Receipt.Cccode;
					}
					else
					{
						account.CCcode = Conversions.ToString(-1);
					}
					receiptType = Receipt.ReceiptType;
					if ((receiptType.HasValue ? new bool?(receiptType == 10) : ((bool?)null)) == true)
					{
						entry.Type = EntryType.ClientVoucher;
					}
					receiptType = Receipt.SalesManID;
					if ((receiptType.HasValue ? new bool?(receiptType != -1) : ((bool?)null)) == true)
					{
						account.salesman = Receipt.SalesManID.Value;
					}
					else
					{
						account.salesman = -1;
					}
					list.Add(account);
					account = new Account();
					account.EntryGlobalID = entry.EntryGlobalID;
					account.EntryNo = entry.EntryNo;
					account.Name = Receipt.DebitAcc;
					account.Code = Receipt.DebitAcc;
					account.Debt = Receipt.Payment.Value;
					account.Credit = 0.0;
					account.Note = Receipt.Notes;
					receiptType = Receipt.ReceiptType;
					bool? flag3;
					flag3 = (receiptType.HasValue ? new bool?(receiptType == 6) : ((bool?)null));
					receiptType = Receipt.ReceiptType;
					bool? flag4;
					flag4 = (receiptType.HasValue ? new bool?(receiptType == 8) : ((bool?)null));
					flag2 = ((flag3 ?? false) ? new bool?(true) : ((!flag4.HasValue) ? ((bool?)null) : ((flag4 == true) | flag3)));
					receiptType = Receipt.ReceiptType;
					flag = (receiptType.HasValue ? new bool?(receiptType == 9) : ((bool?)null));
					if (((flag2 ?? false) ? new bool?(true) : ((!flag.HasValue) ? ((bool?)null) : ((flag == true) | flag2))) == true)
					{
						account.CCcode = Receipt.Cccode;
					}
					else
					{
						account.CCcode = Conversions.ToString(-1);
					}
					receiptType = Receipt.SalesManID;
					if ((receiptType.HasValue ? new bool?(receiptType != -1) : ((bool?)null)) == true)
					{
						account.salesman = Receipt.SalesManID.Value;
					}
					else
					{
						account.salesman = -1;
					}
					list.Add(account);
					payment = Receipt.VAT;
					if ((payment.HasValue ? new bool?(payment.GetValueOrDefault() > 0.0) : ((bool?)null)) == true)
					{
						account = new Account();
						account.EntryGlobalID = entry.EntryGlobalID;
						account.EntryNo = entry.EntryNo;
						account.Name = "الضريبة المضافة ";
						account.Code = Receipt.VATCode;
						account.Debt = Receipt.VAT.Value;
						account.Credit = 0.0;
						account.Note = Receipt.Notes;
						account.CCcode = Conversions.ToString(-1);
						account.salesman = -1;
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

		private static readonly object ReceiptSaveGate = new object();
		private static bool receiptSaveNeedsReview;

		public bool SaveReceipt(Receipt Receipt, Entry Entr, bool IsNew)
		{
			// Compatibility for external callers; local editors use the instance-owned overload.
			string[] files = filePathDocument == null ? null : (string[])filePathDocument.Clone();
			return SaveReceipt(Receipt, Entr, IsNew, files);
		}

		public bool SaveReceipt(Receipt Receipt, Entry Entr, bool IsNew, string[] documents)
		{
			lock (ReceiptSaveGate)
			{
				if (receiptSaveNeedsReview)
				{
					MessageBox.Show("نتيجة حفظ سابقة غير مؤكدة؛ راجع السند والقيد والمرفقات قبل إعادة المحاولة أو إعادة تشغيل البرنامج.", "تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
					return false;
				}
				return SaveReceiptLocked(Receipt, Entr, IsNew, documents == null ? null : (string[])documents.Clone());
			}
		}

		private bool SaveReceiptLocked(Receipt Receipt, Entry Entr, bool IsNew, string[] documents)
		{
			if (Receipt == null || Entr == null || string.IsNullOrWhiteSpace(Receipt.GlobalID) ||
				string.IsNullOrWhiteSpace(Receipt.EntryGlobalID) ||
				!string.Equals(Receipt.EntryGlobalID, Entr.EntryGlobalID, StringComparison.Ordinal) ||
				!Receipt.BranchID.HasValue || Receipt.BranchID.Value <= 0 || Receipt.BranchID.Value != Entr.Branch ||
				!Receipt.ReceiptType.HasValue || Receipt.ReceiptType.Value != (int)Entr.Type)
			{
				MessageBox.Show("هوية السند أو القيد أو الفرع غير صالحة أو غير متطابقة؛ لم يتم الحفظ.", "تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
				return false;
			}

			SqlConnection connection = null;
			SqlTransaction transaction = null;
			bool commitStarted = false;
			bool committed = false;
			var copiedFiles = new List<string>();
			try
			{
				connection = MainClass.ConnObj();
				connection.Open();
				transaction = connection.BeginTransaction();
				if (MainClass.IsTrial)
				{
					using SqlCommand trial = new SqlCommand("SELECT ISNULL(MAX(id),0) FROM Entry", connection, transaction);
					using SqlCommand trialInv = new SqlCommand("SELECT ISNULL(MAX(Proc_id),0) FROM Inv", connection, transaction);
					if (Convert.ToDouble(trial.ExecuteScalar()) >= 50.0 || Convert.ToDouble(trialInv.ExecuteScalar()) >= 100.0)
						throw new InvalidOperationException("تم بلوغ الحد المسموح للنسخة التجريبية.");
				}

				// Lock the receipt identity; never silently insert over an existing document
				// or relink an existing receipt to another entry or branch.
				using (SqlCommand check = new SqlCommand(
					"SELECT EntryGlobalID, BranchID, ISDeleted, ReceiptType, ReceiptNo FROM Receipts WITH (UPDLOCK, HOLDLOCK) WHERE GlobalID=@id", connection, transaction))
				{
					check.Parameters.Add("@id", SqlDbType.NVarChar).Value = Receipt.GlobalID;
					using SqlDataReader reader = check.ExecuteReader();
					bool exists = reader.Read();
					if (IsNew == exists)
						throw new InvalidOperationException("حالة السند لا تطابق السجل المحفوظ؛ راجع الهوية قبل المحاولة.");
					if (exists && (reader["EntryGlobalID"] == DBNull.Value || reader["BranchID"] == DBNull.Value ||
						reader["ISDeleted"] == DBNull.Value || Convert.ToBoolean(reader["ISDeleted"]) ||
						reader["ReceiptType"] == DBNull.Value || Convert.ToInt32(reader["ReceiptType"]) != Receipt.ReceiptType.Value ||
						Convert.ToInt32(reader["ReceiptNo"]) != Receipt.ReceiptNo ||
						!string.Equals(Convert.ToString(reader["EntryGlobalID"]), Receipt.EntryGlobalID, StringComparison.Ordinal) ||
						Convert.ToInt32(reader["BranchID"]) != Receipt.BranchID.Value))
						throw new InvalidOperationException("ربط السند أو فرعه لا يطابق السجل المحفوظ.");
				}

				// Prevent a second receipt from claiming the same journal through this path.
				using (SqlCommand links = new SqlCommand(
					"SELECT COUNT(*) FROM Receipts WITH (UPDLOCK, HOLDLOCK) WHERE EntryGlobalID=@entry AND GlobalID<>@receipt", connection, transaction))
				{
					links.Parameters.Add("@entry", SqlDbType.NVarChar).Value = Receipt.EntryGlobalID;
					links.Parameters.Add("@receipt", SqlDbType.NVarChar).Value = Receipt.GlobalID;
					if (Convert.ToInt32(links.ExecuteScalar()) != 0)
						throw new InvalidOperationException("القيد مرتبط بسند آخر؛ راجع السجلات قبل الحفظ.");
				}

				using SqlCommand sqlCommand3 = ((!IsNew) ? new SqlCommand(StoredQueries.UpdateReceipt, connection, transaction) : new SqlCommand(StoredQueries.InsertReceipt, connection, transaction));
				sqlCommand3.Parameters.Add("@GlobalID", SqlDbType.VarChar).Value = Receipt.GlobalID;
				sqlCommand3.Parameters.Add("@ReceiptNo", SqlDbType.Int).Value = Receipt.ReceiptNo;
				sqlCommand3.Parameters.Add("@ReceiptDate", SqlDbType.DateTime).Value = Receipt.ReceiptDate;
				sqlCommand3.Parameters.Add("@EmpId", SqlDbType.Int).Value = Receipt.EmpId;
				sqlCommand3.Parameters.Add("@ClientID", SqlDbType.Int).Value = Receipt.ClientID;
				sqlCommand3.Parameters.Add("@state", SqlDbType.Int).Value = Receipt.State;
				sqlCommand3.Parameters.Add("@CreditAcc", SqlDbType.NVarChar).Value = Receipt.CreditAcc;
				sqlCommand3.Parameters.Add("@DebitAcc", SqlDbType.NVarChar).Value = Receipt.DebitAcc;
				sqlCommand3.Parameters.Add("@Payment", SqlDbType.Float).Value = Receipt.Payment;
				sqlCommand3.Parameters.Add("@VAT", SqlDbType.Float).Value = Receipt.VAT;
				sqlCommand3.Parameters.Add("@NetVal", SqlDbType.Float).Value = Receipt.NetVal;
				sqlCommand3.Parameters.Add("@BranchID", SqlDbType.Int).Value = Receipt.BranchID;
				sqlCommand3.Parameters.Add("@ReceiptType", SqlDbType.Int).Value = Receipt.ReceiptType;
				sqlCommand3.Parameters.Add("@PaymentType", SqlDbType.Int).Value = Receipt.PaymentType;
				sqlCommand3.Parameters.Add("@BankID", SqlDbType.Int).Value = Receipt.BankId;
				sqlCommand3.Parameters.Add("@TreasuryID", SqlDbType.Int).Value = Receipt.TreasuryID;
				sqlCommand3.Parameters.Add("@SalesManID", SqlDbType.Int).Value = Receipt.SalesManID;
				sqlCommand3.Parameters.Add("@CheckNo", SqlDbType.NVarChar).Value = Receipt.CheckNo;
				sqlCommand3.Parameters.Add("@Checkbank", SqlDbType.NVarChar).Value = Receipt.Checkbank;
				sqlCommand3.Parameters.Add("@CheckDate", SqlDbType.DateTime).Value = Receipt.CheckDate;
				sqlCommand3.Parameters.Add("@CheckState", SqlDbType.NVarChar).Value = Receipt.CheckState;
				sqlCommand3.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = Receipt.EntryGlobalID;
				sqlCommand3.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = Receipt.Notes;
				sqlCommand3.Parameters.Add("@Cccode", SqlDbType.NVarChar).Value = Receipt.Cccode;
				sqlCommand3.Parameters.Add("@ReffNo", SqlDbType.NVarChar).Value = Receipt.ReffNo;
				sqlCommand3.Parameters.Add("@Reffdate", SqlDbType.DateTime).Value = Receipt.Reffdate;
				sqlCommand3.Parameters.Add("@Sync", SqlDbType.Bit).Value = Receipt.Sync;
				sqlCommand3.Parameters.Add("@ISDeleted", SqlDbType.Bit).Value = Receipt.ISDeleted;
				sqlCommand3.Parameters.Add("@Recipient", SqlDbType.NVarChar).Value = Receipt.Recipient;
				sqlCommand3.ExecuteNonQuery();

				new EntryOper().WriteEntryInTransaction(Entr, connection, transaction, IsNew);
				InsertReceiptDocuments(documents, Receipt.GlobalID, connection, transaction, copiedFiles);
				commitStarted = true;
				transaction.Commit();
				committed = true;
				return true;
			}
			catch (Exception ex)
			{
				bool rollbackConfirmed = transaction == null;
				if (transaction != null && !commitStarted)
				{
					try { transaction.Rollback(); rollbackConfirmed = true; }
					catch { rollbackConfirmed = false; }
				}
				bool unknown = commitStarted || !rollbackConfirmed;
				if (unknown)
					receiptSaveNeedsReview = true;
				else
				{
					// Only delete new copies after confirmed rollback; unknown commit must
					// retain them in case the database contains references to them.
					foreach (string path in copiedFiles)
					{
						try { if (File.Exists(path)) File.Delete(path); }
						catch { receiptSaveNeedsReview = true; }
					}
				}
				string message = unknown || receiptSaveNeedsReview
					? "نتيجة السند أو التنظيف غير مؤكدة؛ راجع قاعدة البيانات والمرفقات قبل إعادة المحاولة."
					: "تعذر حفظ السند والقيد؛ لم تُعتمد المعاملة.";
				MessageBox.Show(message + Environment.NewLine + "معرّف السند: " + Receipt.GlobalID + "، معرّف القيد: " + Receipt.EntryGlobalID + Environment.NewLine + ex.Message, "تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
				return false;
			}
			finally
			{
				try { if (transaction != null) transaction.Dispose(); } catch { if (!committed) receiptSaveNeedsReview = true; }
				try { if (connection != null) connection.Dispose(); } catch { if (!committed) receiptSaveNeedsReview = true; }
			}
		}

		private static void InsertReceiptDocuments(string[] files, string receiptId, SqlConnection connection,
			SqlTransaction transaction, List<string> copiedFiles)
		{
			if (files == null || files.Length == 0) return;
			string root = Properties.Settings.Default.DocsRootPath;
			if (string.IsNullOrWhiteSpace(root)) throw new InvalidOperationException("مسار المرفقات غير محدد.");
			Directory.CreateDirectory(root);
			foreach (string source in files)
			{
				if (string.IsNullOrWhiteSpace(source)) throw new InvalidOperationException("مسار المرفق غير صالح.");
				string destination = Path.Combine(root, "Receipt-" + Guid.NewGuid().ToString("N") + Path.GetExtension(source));
				using (FileStream input = File.OpenRead(source))
				using (FileStream output = new FileStream(destination, FileMode.CreateNew, FileAccess.Write, FileShare.None))
				{
					copiedFiles.Add(destination);
					input.CopyTo(output);
				}
				using SqlCommand command = new SqlCommand(
					"INSERT INTO Documents (FileName, FileUrl, GlobalID, type) VALUES (@name,@path,@id,3)", connection, transaction);
				command.Parameters.Add("@name", SqlDbType.NVarChar).Value = Path.GetFileName(source);
				command.Parameters.Add("@path", SqlDbType.NVarChar).Value = destination;
				command.Parameters.Add("@id", SqlDbType.NVarChar).Value = receiptId;
				command.ExecuteNonQuery();
			}
		}

		public bool SaveReceipt2(Receipt Receipt)
		{
			new SqlCommand();
			SqlConnection sqlConnection;
			sqlConnection = MainClass.ConnObj();
			if (sqlConnection.State != ConnectionState.Open)
			{
				sqlConnection.Open();
			}
			SqlTransaction sqlTransaction;
			sqlTransaction = sqlConnection.BeginTransaction();
			bool result;
			try
			{
				SqlCommand sqlCommand;
				sqlCommand = new SqlCommand(StoredQueries.InsertReceipt, sqlConnection, sqlTransaction);
				sqlCommand.Parameters.Add("@GlobalID", SqlDbType.VarChar).Value = Receipt.GlobalID;
				sqlCommand.Parameters.Add("@ReceiptNo", SqlDbType.Int).Value = Receipt.ReceiptNo;
				sqlCommand.Parameters.Add("@ReceiptDate", SqlDbType.DateTime).Value = Receipt.ReceiptDate;
				sqlCommand.Parameters.Add("@EmpId", SqlDbType.Int).Value = Receipt.EmpId;
				sqlCommand.Parameters.Add("@ClientID", SqlDbType.Int).Value = Receipt.ClientID;
				sqlCommand.Parameters.Add("@state", SqlDbType.Int).Value = Receipt.State;
				sqlCommand.Parameters.Add("@CreditAcc", SqlDbType.NVarChar).Value = Receipt.CreditAcc;
				sqlCommand.Parameters.Add("@DebitAcc", SqlDbType.NVarChar).Value = Receipt.DebitAcc;
				sqlCommand.Parameters.Add("@Payment", SqlDbType.Float).Value = Receipt.Payment;
				sqlCommand.Parameters.Add("@VAT", SqlDbType.Float).Value = Receipt.VAT;
				sqlCommand.Parameters.Add("@NetVal", SqlDbType.Float).Value = Receipt.NetVal;
				sqlCommand.Parameters.Add("@BranchID", SqlDbType.Int).Value = Receipt.BranchID;
				sqlCommand.Parameters.Add("@ReceiptType", SqlDbType.Int).Value = Receipt.ReceiptType;
				sqlCommand.Parameters.Add("@PaymentType", SqlDbType.Int).Value = Receipt.PaymentType;
				sqlCommand.Parameters.Add("@BankID", SqlDbType.Int).Value = Receipt.BankId;
				sqlCommand.Parameters.Add("@TreasuryID", SqlDbType.Int).Value = Receipt.TreasuryID;
				sqlCommand.Parameters.Add("@SalesManID", SqlDbType.Int).Value = Receipt.SalesManID;
				sqlCommand.Parameters.Add("@CheckNo", SqlDbType.NVarChar).Value = Receipt.CheckNo;
				sqlCommand.Parameters.Add("@Checkbank", SqlDbType.NVarChar).Value = Receipt.Checkbank;
				sqlCommand.Parameters.Add("@CheckDate", SqlDbType.DateTime).Value = Receipt.CheckDate;
				sqlCommand.Parameters.Add("@CheckState", SqlDbType.NVarChar).Value = Receipt.CheckState;
				sqlCommand.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = Receipt.EntryGlobalID;
				sqlCommand.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = Receipt.Notes;
				sqlCommand.Parameters.Add("@Cccode", SqlDbType.NVarChar).Value = Receipt.Cccode;
				sqlCommand.Parameters.Add("@ReffNo", SqlDbType.NVarChar).Value = Receipt.ReffNo;
				sqlCommand.Parameters.Add("@Reffdate", SqlDbType.DateTime).Value = Receipt.Reffdate;
				sqlCommand.Parameters.Add("@Sync", SqlDbType.Bit).Value = Receipt.Sync;
				sqlCommand.Parameters.Add("@ISDeleted", SqlDbType.Bit).Value = Receipt.ISDeleted;
				sqlCommand.ExecuteNonQuery();
				sqlTransaction.Commit();
				result = true;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2;
				ex2 = ex;
				sqlTransaction.Rollback();
				string text;
				text = "خطأ اثناء عمل تحديث السندات ";
				if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
				{
					text = "error in saving";
				}
				MessageBox.Show((Operators.CompareString(MainClass.Language, "ar", TextCompare: false) != 0) ? (text + Environment.NewLine + "Error details: " + ex2.Message) : (text + Environment.NewLine + "تفاصيل الخطأ: " + ex2.Message), "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
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

		public bool DeleteReceipt(string ReceiptGID, string EntryGID)
		{
			new SqlCommand();
			SqlConnection sqlConnection;
			sqlConnection = MainClass.ConnObj();
			if (sqlConnection.State != ConnectionState.Open)
			{
				sqlConnection.Open();
			}
			SqlTransaction sqlTransaction;
			sqlTransaction = sqlConnection.BeginTransaction();
			string text;
			text = "";
			bool result = default(bool);
			try
			{
				if (Sync.ActiveSync & (Sync.SyncType > 0))
				{
					text = " , Sync=0 ";
				}
				new SqlCommand("update Receipts set ISDeleted=1 " + text + " where branchID=" + Conversions.ToString(MainClass.BranchNo) + " and GlobalID=N'" + ReceiptGID + "'", sqlConnection, sqlTransaction).ExecuteNonQuery();
				new SqlCommand("update Entry set state=2 ,IS_Deleted=1 " + text + "  where branch=" + Conversions.ToString(MainClass.BranchNo) + " and GlobalID=N'" + EntryGID + "'", sqlConnection, sqlTransaction).ExecuteNonQuery();
				sqlTransaction.Commit();
				result = true;
				return result;
			}
			catch (Exception projectError)
			{
				ProjectData.SetProjectError(projectError);
				sqlTransaction.Rollback();
				ProjectData.ClearProjectError();
			}
			finally
			{
				if (sqlConnection.State != ConnectionState.Closed)
				{
					sqlConnection.Close();
				}
				sqlTransaction.Dispose();
			}
			return result;
		}

		// The two editors build their journal before entering this shared SQL unit of work.
		public sealed class NoteDraft
		{
			public int Number, Type, Branch, InvoiceNo, UserId, CustomerId;
			public double Discount, Net, InvoiceValue;
			public DateTime Date;
			public string Notes;
			public bool IsNew;
			public Entry Journal;
		}

		public bool SaveCreditDebtNote(NoteDraft draft)
		{
			lock (NoteDeleteGate)
			{
				if (noteDeleteNeedsReview)
				{
					MessageBox.Show("نتيجة حفظ أو حذف إشعار سابقة غير مؤكدة؛ راجعها قبل المحاولة.", "تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
					return false;
				}
				return SaveCreditDebtNoteLocked(draft);
			}
		}

		private bool SaveCreditDebtNoteLocked(NoteDraft d)
		{
			if (d == null || d.Journal == null || d.Number <= 0 || d.Branch <= 0 ||
				d.Branch != MainClass.BranchNo || (d.Type != 1 && d.Type != 2) || d.CustomerId <= 0 || d.Date < new DateTime(1753, 1, 1) ||
				(d.InvoiceNo != -1 && d.InvoiceNo <= 0) || !double.IsFinite(d.Discount) || d.Discount <= 0 ||
				!double.IsFinite(d.Net) || !double.IsFinite(d.InvoiceValue) ||
				string.IsNullOrWhiteSpace(d.Journal.EntryGlobalID) || d.Journal.EntryGlobalID == "-1" ||
				d.Journal.Branch != d.Branch || d.Journal.State != 1 || d.Journal.ISDeleted != false ||
				(d.IsNew && d.Journal.EntryNo <= 0) || (int)d.Journal.Type != (d.Type == 1 ? 16 : 17) ||
				!int.TryParse(d.Journal.ReffNo, out int reference) || reference != d.Number || d.Journal.EntryDate != d.Date)
			{
				MessageBox.Show("بيانات الإشعار أو القيد غير صالحة أو غير متطابقة؛ لم يتم الحفظ.", "تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
				return false;
			}
			SqlConnection connection = null;
			SqlTransaction transaction = null;
			bool commitStarted = false;
			try
			{
				connection = MainClass.ConnObj();
				connection.Open();
				transaction = connection.BeginTransaction();
				int noteId = -1;
				using (SqlCommand find = new SqlCommand(
					"SELECT TOP (2) Id, BranchId, IS_Deleted FROM CreditDeptNotes WITH (UPDLOCK,HOLDLOCK) WHERE Doc_No=@number AND Doc_Type=@type", connection, transaction))
				{
					find.Parameters.Add("@number", SqlDbType.Int).Value = d.Number;
					find.Parameters.Add("@type", SqlDbType.Int).Value = d.Type;
					using SqlDataReader reader = find.ExecuteReader();
					bool exists = reader.Read();
					if (d.IsNew && exists) throw new InvalidOperationException("رقم الإشعار مستخدم؛ أعد اختيار رقم جديد.");
					if (!d.IsNew)
					{
						if (!exists || reader.IsDBNull(1) || Convert.ToInt32(reader["BranchId"]) != d.Branch ||
							reader.IsDBNull(2) || Convert.ToBoolean(reader["IS_Deleted"]))
							throw new InvalidOperationException("الإشعار أو فرعه أو حالة حذفه غير مطابقة.");
						noteId = Convert.ToInt32(reader["Id"]);
						if (reader.Read()) throw new InvalidOperationException("رقم الإشعار مكرر؛ يلزم المصالحة.");
					}
				}
				using (SqlCommand find = new SqlCommand(
					"SELECT TOP (2) GlobalID, IS_Deleted, state, id FROM Entry WITH (UPDLOCK,HOLDLOCK) WHERE branch=@branch AND type=@type AND doc_no=@number", connection, transaction))
				{
					find.Parameters.Add("@branch", SqlDbType.Int).Value = d.Branch;
					find.Parameters.Add("@type", SqlDbType.Int).Value = (int)d.Journal.Type;
					find.Parameters.Add("@number", SqlDbType.Int).Value = d.Number;
					using SqlDataReader reader = find.ExecuteReader();
					bool exists = reader.Read();
					if (d.IsNew && exists) throw new InvalidOperationException("يوجد قيد بهذا الرقم والنوع والفرع؛ يلزم المصالحة.");
					if (!d.IsNew)
					{
						if (!exists || reader.IsDBNull(0) || !string.Equals(reader.GetString(0), d.Journal.EntryGlobalID, StringComparison.Ordinal) ||
							reader.IsDBNull(1) || Convert.ToBoolean(reader["IS_Deleted"]) || reader.IsDBNull(2) || Convert.ToInt32(reader["state"]) != 1)
							throw new InvalidOperationException("القيد المرتبط مفقود أو غير مطابق أو غير نشط.");
						if (reader.IsDBNull(3)) throw new InvalidOperationException("رقم القيد المرتبط غير معروف.");
						int existingEntryNo = Convert.ToInt32(reader["id"]);
						if (reader.Read()) throw new InvalidOperationException("القيد المرتبط غير فريد؛ يلزم المصالحة.");
						d.Journal.EntryNo = existingEntryNo;
						if (d.Journal.Accounts != null)
							foreach (Account account in d.Journal.Accounts)
								if (account != null) account.EntryNo = existingEntryNo;
					}
				}
				if (d.Journal.Accounts == null) throw new InvalidOperationException("بنود القيد غير متوفرة.");
				Account firstAccount = null;
				foreach (Account account in d.Journal.Accounts) { firstAccount = account; break; }
				if (firstAccount == null || !int.TryParse(firstAccount.Code, out int partyCode) || partyCode <= 0 ||
					(d.Type == 1 && (firstAccount.Debt != d.Discount || firstAccount.Credit != 0)) ||
					(d.Type == 2 && (firstAccount.Credit != d.Discount || firstAccount.Debt != 0)))
					throw new InvalidOperationException("بند الطرف في القيد لا يطابق الإشعار.");
				using (SqlCommand party = new SqlCommand(
					"SELECT AccountCode FROM Customers WITH (UPDLOCK,HOLDLOCK) WHERE id=@id AND IS_Deleted=0 AND type IN (@partyType,3)", connection, transaction))
				{
					party.Parameters.Add("@id", SqlDbType.Int).Value = d.CustomerId;
					party.Parameters.Add("@partyType", SqlDbType.Int).Value = d.Type == 1 ? 2 : 1;
					object stored = party.ExecuteScalar();
					if (stored == null || stored == DBNull.Value || Convert.ToInt32(stored) != partyCode)
						throw new InvalidOperationException("حساب الطرف غير موجود أو تغير قبل الحفظ.");
				}
				decimal debit = 0m, credit = 0m;
				foreach (Account account in d.Journal.Accounts)
				{
					if (account == null || !double.IsFinite(account.Debt) || !double.IsFinite(account.Credit))
						throw new InvalidOperationException("مبلغ القيد غير صالح.");
					debit += Convert.ToDecimal(account.Debt);
					credit += Convert.ToDecimal(account.Credit);
				}
				decimal noteAmount = Convert.ToDecimal(d.Discount);
				if (debit != noteAmount || credit != noteAmount)
					throw new InvalidOperationException("مبلغ القيد لا يطابق خصم الإشعار.");
				string sql = d.IsNew
					? "INSERT INTO CreditDeptNotes (Doc_No,Doc_Type,Inv_No,Discount,Net,Date,IS_Deleted,Edit_Date,emp_id,notes,cust_id,Inv_Val,BranchId) VALUES (@number,@type,@invoice,@discount,@net,@date,0,@editDate,@user,@notes,@customer,@invVal,@branch)"
					: "UPDATE CreditDeptNotes SET Inv_No=@invoice,Discount=@discount,Net=@net,Date=@date,Edit_Date=@editDate,emp_id=@user,notes=@notes,cust_id=@customer,Inv_Val=@invVal WHERE Id=@id AND BranchId=@branch AND Doc_No=@number AND Doc_Type=@type AND IS_Deleted=0";
				using (SqlCommand cmd = new SqlCommand(sql, connection, transaction))
				{
					cmd.Parameters.Add("@number", SqlDbType.Int).Value = d.Number;
					cmd.Parameters.Add("@type", SqlDbType.Int).Value = d.Type;
					cmd.Parameters.Add("@invoice", SqlDbType.Int).Value = d.InvoiceNo;
					cmd.Parameters.Add("@discount", SqlDbType.Float).Value = d.Discount;
					cmd.Parameters.Add("@net", SqlDbType.Float).Value = d.Net;
					cmd.Parameters.Add("@date", SqlDbType.DateTime).Value = d.Date;
					cmd.Parameters.Add("@editDate", SqlDbType.DateTime).Value = DateTime.Now;
					cmd.Parameters.Add("@user", SqlDbType.Int).Value = d.UserId;
					cmd.Parameters.Add("@notes", SqlDbType.NVarChar).Value = d.Notes ?? string.Empty;
					cmd.Parameters.Add("@customer", SqlDbType.Int).Value = d.CustomerId;
					cmd.Parameters.Add("@invVal", SqlDbType.Float).Value = d.InvoiceValue;
					cmd.Parameters.Add("@branch", SqlDbType.Int).Value = d.Branch;
					if (!d.IsNew) cmd.Parameters.Add("@id", SqlDbType.Int).Value = noteId;
					if (cmd.ExecuteNonQuery() != 1) throw new InvalidOperationException("لم يُكتب إشعار وحيد.");
				}
				new EntryOper().WriteEntryInTransaction(d.Journal, connection, transaction, d.IsNew);
				commitStarted = true;
				transaction.Commit();
				return true;
			}
			catch (Exception ex)
			{
				bool rollbackConfirmed = transaction == null;
				if (transaction != null && !commitStarted)
				{
					try { transaction.Rollback(); rollbackConfirmed = true; } catch { rollbackConfirmed = false; }
				}
				if (commitStarted || !rollbackConfirmed) noteDeleteNeedsReview = true;
				string prefix = noteDeleteNeedsReview ? "نتيجة حفظ الإشعار غير مؤكدة؛ راجع قاعدة البيانات قبل إعادة المحاولة." : "تعذر حفظ الإشعار والقيد.";
				MessageBox.Show(prefix + Environment.NewLine + "النوع: " + d.Type + "، الرقم: " + d.Number + "، الفرع: " + d.Branch + "، القيد: " + d.Journal.EntryGlobalID + Environment.NewLine + ex.Message,
					"تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
				return false;
			}
			finally
			{
				try { transaction?.Dispose(); } catch { noteDeleteNeedsReview = true; }
				try { connection?.Dispose(); } catch { noteDeleteNeedsReview = true; }
			}
		}

		private static readonly object NoteDeleteGate = new object();
		private static bool noteDeleteNeedsReview;

		public bool DeleteCreditNote(int Doc_No, int Doc_Type, string EntryGID)
		{
			lock (NoteDeleteGate)
			{
				if (noteDeleteNeedsReview)
				{
					MessageBox.Show("نتيجة حفظ أو حذف إشعار سابقة غير مؤكدة؛ راجعها قبل إعادة المحاولة.", "تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
					return false;
				}
				return DeleteCreditNoteLocked(Doc_No, Doc_Type, EntryGID);
			}
		}

		private bool DeleteCreditNoteLocked(int number, int noteType, string entryId)
		{
			int branch = MainClass.BranchNo;
			if (number <= 0 || branch <= 0 || (noteType != 1 && noteType != 2) ||
				string.IsNullOrWhiteSpace(entryId) || entryId == "-1") return false;
			int entryType = noteType == 1 ? 16 : 17;
			SqlTransaction transaction = null;
			bool commitStarted = false;
			SqlConnection connection = null;
			try
			{
				connection = MainClass.ConnObj();
				connection.Open();
				transaction = connection.BeginTransaction();
				int noteId;
				using (SqlCommand find = new SqlCommand(
					"SELECT TOP (2) Id, BranchId, IS_Deleted FROM CreditDeptNotes WITH (UPDLOCK,HOLDLOCK) WHERE Doc_No=@number AND Doc_Type=@type", connection, transaction))
				{
					find.Parameters.Add("@number", SqlDbType.Int).Value = number;
					find.Parameters.Add("@type", SqlDbType.Int).Value = noteType;
					using SqlDataReader reader = find.ExecuteReader();
					if (!reader.Read() || reader.IsDBNull(1) || Convert.ToInt32(reader["BranchId"]) != branch ||
						reader.IsDBNull(2) || Convert.ToBoolean(reader["IS_Deleted"]))
						throw new InvalidOperationException("الإشعار مفقود أو محذوف أو فرعه غير واضح.");
					noteId = Convert.ToInt32(reader["Id"]);
					if (reader.Read()) throw new InvalidOperationException("رقم الإشعار مكرر؛ يلزم المصالحة.");
				}
				using (SqlCommand find = new SqlCommand(
					"SELECT TOP (2) GlobalID, IS_Deleted, state FROM Entry WITH (UPDLOCK,HOLDLOCK) WHERE branch=@branch AND type=@type AND doc_no=@number", connection, transaction))
				{
					find.Parameters.Add("@branch", SqlDbType.Int).Value = branch;
					find.Parameters.Add("@type", SqlDbType.Int).Value = entryType;
					find.Parameters.Add("@number", SqlDbType.Int).Value = number;
					using SqlDataReader reader = find.ExecuteReader();
					if (!reader.Read() || reader.IsDBNull(0) || !string.Equals(reader.GetString(0), entryId, StringComparison.Ordinal) ||
						reader.IsDBNull(1) || Convert.ToBoolean(reader["IS_Deleted"]) || reader.IsDBNull(2) || Convert.ToInt32(reader["state"]) != 1)
						throw new InvalidOperationException("القيد المرتبط مفقود أو غير مطابق أو غير نشط.");
					if (reader.Read()) throw new InvalidOperationException("القيد المرتبط غير فريد؛ يلزم المصالحة.");
				}
				using (SqlCommand update = new SqlCommand("UPDATE CreditDeptNotes SET IS_Deleted=1 WHERE Id=@id AND BranchId=@branch AND IS_Deleted=0", connection, transaction))
				{
					update.Parameters.Add("@id", SqlDbType.Int).Value = noteId;
					update.Parameters.Add("@branch", SqlDbType.Int).Value = branch;
					if (update.ExecuteNonQuery() != 1) throw new InvalidOperationException("لم يُحدَّث إشعار وحيد.");
				}
				using (SqlCommand update = new SqlCommand("UPDATE Entry SET state=2, IS_Deleted=1 WHERE GlobalID=@id AND branch=@branch AND type=@type AND doc_no=@number AND IS_Deleted=0 AND state=1", connection, transaction))
				{
					update.Parameters.Add("@id", SqlDbType.VarChar).Value = entryId;
					update.Parameters.Add("@branch", SqlDbType.Int).Value = branch;
					update.Parameters.Add("@type", SqlDbType.Int).Value = entryType;
					update.Parameters.Add("@number", SqlDbType.Int).Value = number;
					if (update.ExecuteNonQuery() != 1) throw new InvalidOperationException("لم يُحدَّث قيد وحيد.");
				}
				commitStarted = true;
				transaction.Commit();
				return true;
			}
			catch (Exception ex)
			{
				bool rollbackConfirmed = transaction == null;
				if (transaction != null && !commitStarted)
				{
					try { transaction.Rollback(); rollbackConfirmed = true; } catch { rollbackConfirmed = false; }
				}
				if (commitStarted || !rollbackConfirmed) noteDeleteNeedsReview = true;
				string prefix = noteDeleteNeedsReview ? "نتيجة الحذف غير مؤكدة، راجع الإشعار والقيد قبل إعادة المحاولة." : "تعذر حذف الإشعار والقيد.";
				MessageBox.Show(prefix + Environment.NewLine + "النوع: " + noteType + "، الرقم: " + number + "، الفرع: " + branch + "، القيد: " + entryId + Environment.NewLine + ex.Message,
					"تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
				return false;
			}
			finally
			{
				try { transaction?.Dispose(); } catch { noteDeleteNeedsReview = true; }
				try { connection?.Dispose(); } catch { noteDeleteNeedsReview = true; }
			}
		}


		public static int ReceiptNo(int ReceiptType)
		{
			SqlConnection sqlConnection;
			sqlConnection = MainClass.ConnObj();
			if (sqlConnection.State != ConnectionState.Open)
			{
				sqlConnection.Open();
			}
			new SqlCommand();
			return checked((int)Math.Round(Convert.ToDouble(Operators.ConcatenateObject("", new SqlCommand("select ISNULL(MAX(ReceiptNo), 0) from Receipts where ReceiptType=" + Conversions.ToString(ReceiptType) + " and branchID=" + Conversions.ToString(MainClass.BranchNo), sqlConnection).ExecuteScalar())) + 1.0));
		}

		public static string ReceipTypeName(int ReceiptType)
		{
			string result;
			result = "";
			switch (ReceiptType)
			{
				case 5:
					result = "سند قبض من عميل";
					break;
				case 6:
					result = "سند صرف لمورد";
					break;
				case 7:
					result = "سند قبض ";
					break;
				case 8:
					result = "سند صرف";
					break;
				case 9:
					result = "سند صرف ضريبة";
					break;
				case 26:
					result = "سند صرف راتب ";
					break;
				case 10:
					result = "سند قبض أندرويد";
					break;
			}
			return result;
		}

		// Structured search contract: callers cannot pass SQL fragments.
		public static DataTable LoadReceipts(int receiptType, int branchId, string receiptNumber,
			string reference, bool allDates, DateTime startDate, DateTime endDate)
		{
			int? number = null;
			if (!string.IsNullOrWhiteSpace(receiptNumber))
			{
				if (!int.TryParse(receiptNumber.Trim(), out int parsed) || parsed <= 0)
					throw new ArgumentException("رقم السند غير صالح.");
				number = parsed;
			}
			if (!allDates && (startDate.Date < new DateTime(1753, 1, 1) ||
				endDate.Date < startDate.Date || endDate.Date == DateTime.MaxValue.Date))
				throw new ArgumentException("فترة البحث غير صالحة.");

			string sql = "SELECT Receipts.GlobalID, Receipts.ReceiptNo, Receipts.ReceiptDate, " +
				"Receipts.Payment, Employees.name, Receipts.ClientID FROM Receipts " +
				"INNER JOIN Employees ON Receipts.EmpId=Employees.id " +
				"WHERE Receipts.ISDeleted=0 AND Receipts.ReceiptType=@type ";
			if (branchId != -1) sql += "AND Receipts.BranchID=@branch ";
			if (number.HasValue) sql += "AND Receipts.ReceiptNo=@number ";
			else if (!string.IsNullOrWhiteSpace(reference)) sql += "AND Receipts.ReffNo=@reference ";
			if (!allDates) sql += "AND Receipts.ReceiptDate>=@start AND Receipts.ReceiptDate<@endExclusive ";
			sql += "ORDER BY Receipts.ReceiptNo";

			using SqlConnection connection = MainClass.ConnObj();
			using SqlCommand command = new SqlCommand(sql, connection);
			command.Parameters.Add("@type", SqlDbType.Int).Value = receiptType;
			if (branchId != -1) command.Parameters.Add("@branch", SqlDbType.Int).Value = branchId;
			if (number.HasValue) command.Parameters.Add("@number", SqlDbType.Int).Value = number.Value;
			else if (!string.IsNullOrWhiteSpace(reference)) command.Parameters.Add("@reference", SqlDbType.NVarChar).Value = reference;
			if (!allDates)
			{
				command.Parameters.Add("@start", SqlDbType.DateTime).Value = startDate.Date;
				command.Parameters.Add("@endExclusive", SqlDbType.DateTime).Value = endDate.Date.AddDays(1);
			}
			using SqlDataAdapter adapter = new SqlDataAdapter(command);
			var result = new DataTable();
			adapter.Fill(result);
			return result; // Propagate failure: empty is not an error result.
		}

		public async Task SyncReceipt(Receipt receipt, Entry Eny, bool IsNew)
		{
			ReceiptCRUD receiptCRUD;
			receiptCRUD = new ReceiptCRUD(Sync.APIUrl);
			EntryCRUD entryCRUD;
			entryCRUD = new EntryCRUD(Sync.APIUrl);
			List<Receipt> list;
			list = new List<Receipt>();
			List<Entry> list2;
			list2 = new List<Entry>();
			Eny.Received = false;
			receipt.Received = false;
			if (Sync.ValidAPIUrl)
			{
				list = (List<Receipt>)(await receiptCRUD.PostReceiptsOnline(receipt, IsNew));
				list2 = (List<Entry>)(await entryCRUD.PostEntriesOnline(Eny, IsNew));
			}
			else
			{
				receiptCRUD.AddReceiptLocally(receipt, IsNew);
				entryCRUD.AddEntryLocally(Eny, IsNew);
			}
			new SqlCommand();
			SqlConnection sqlConnection;
			sqlConnection = MainClass.ConnObj();
			if (list.Count > 0)
			{
				if (sqlConnection.State != ConnectionState.Open)
				{
					sqlConnection.Open();
				}
				foreach (Receipt item in list)
				{
					receipt = item;
					new SqlCommand("update Receipts set Sync=1 where GlobalID=N'" + receipt.GlobalID + "'", sqlConnection).ExecuteNonQuery();
				}
			}
			if (list2.Count <= 0)
			{
				return;
			}
			if (sqlConnection.State != ConnectionState.Open)
			{
				sqlConnection.Open();
			}
			foreach (Entry item2 in list2)
			{
				new SqlCommand("update Entry set Sync=1 where GlobalID=N'" + item2.EntryGlobalID + "'", sqlConnection).ExecuteNonQuery();
			}
		}

		public void ReadReceiptOnline(Receipt Receipt)
		{
			SqlConnection sqlConnection;
			sqlConnection = MainClass.ConnObj();
			if (sqlConnection.State != ConnectionState.Open)
			{
				sqlConnection.Open();
			}
			SqlTransaction sqlTransaction;
			sqlTransaction = sqlConnection.BeginTransaction();
			new SqlCommand();
			bool flag;
			flag = true;
			try
			{
				if (Convert.ToDouble(Operators.ConcatenateObject("", new SqlCommand("Select COUNT(*) from Receipts where GlobalID= N'" + Receipt.GlobalID + "'", sqlConnection, sqlTransaction).ExecuteScalar())) > 0.0)
				{
					flag = false;
				}
				SqlCommand sqlCommand;
				sqlCommand = ((!flag) ? new SqlCommand(StoredQueries.UpdateReceipt, sqlConnection, sqlTransaction) : new SqlCommand(StoredQueries.InsertReceipt, sqlConnection, sqlTransaction));
				sqlCommand.Parameters.Add("@GlobalID", SqlDbType.NVarChar).Value = Receipt.GlobalID;
				sqlCommand.Parameters.Add("@ReceiptNo", SqlDbType.Int).Value = Receipt.ReceiptNo;
				sqlCommand.Parameters.Add("@ReceiptDate", SqlDbType.DateTime).Value = Receipt.ReceiptDate;
				sqlCommand.Parameters.Add("@EmpId", SqlDbType.Int).Value = Receipt.EmpId;
				sqlCommand.Parameters.Add("@ClientID", SqlDbType.Int).Value = Receipt.ClientID;
				sqlCommand.Parameters.Add("@state", SqlDbType.Int).Value = Receipt.State;
				sqlCommand.Parameters.Add("@CreditAcc", SqlDbType.NVarChar).Value = Receipt.CreditAcc;
				sqlCommand.Parameters.Add("@DebitAcc", SqlDbType.NVarChar).Value = Receipt.DebitAcc;
				sqlCommand.Parameters.Add("@Payment", SqlDbType.Float).Value = Receipt.Payment;
				sqlCommand.Parameters.Add("@VAT", SqlDbType.Float).Value = Receipt.VAT;
				sqlCommand.Parameters.Add("@NetVal", SqlDbType.Float).Value = Receipt.NetVal;
				sqlCommand.Parameters.Add("@BranchID", SqlDbType.Int).Value = Receipt.BranchID;
				sqlCommand.Parameters.Add("@ReceiptType", SqlDbType.Int).Value = Receipt.ReceiptType;
				sqlCommand.Parameters.Add("@PaymentType", SqlDbType.Int).Value = Receipt.PaymentType;
				sqlCommand.Parameters.Add("@BankID", SqlDbType.Int).Value = Receipt.BankId;
				sqlCommand.Parameters.Add("@TreasuryID", SqlDbType.Int).Value = Receipt.TreasuryID;
				sqlCommand.Parameters.Add("@SalesManID", SqlDbType.Int).Value = Receipt.SalesManID;
				sqlCommand.Parameters.Add("@CheckNo", SqlDbType.NVarChar).Value = Receipt.CheckNo;
				sqlCommand.Parameters.Add("@Checkbank", SqlDbType.NVarChar).Value = Receipt.Checkbank;
				sqlCommand.Parameters.Add("@CheckDate", SqlDbType.DateTime).Value = Receipt.CheckDate;
				sqlCommand.Parameters.Add("@CheckState", SqlDbType.NVarChar).Value = Receipt.CheckState;
				sqlCommand.Parameters.Add("@EntryGlobalID", SqlDbType.NVarChar).Value = Receipt.EntryGlobalID;
				sqlCommand.Parameters.Add("@Notes", SqlDbType.NVarChar).Value = Receipt.Notes;
				sqlCommand.Parameters.Add("@Cccode", SqlDbType.NVarChar).Value = Receipt.Cccode;
				sqlCommand.Parameters.Add("@ReffNo", SqlDbType.NVarChar).Value = Receipt.ReffNo;
				sqlCommand.Parameters.Add("@Reffdate", SqlDbType.DateTime).Value = Receipt.Reffdate;
				sqlCommand.Parameters.Add("@Sync", SqlDbType.Bit).Value = 1;
				sqlCommand.Parameters.Add("@ISDeleted", SqlDbType.Bit).Value = Receipt.ISDeleted;
				sqlCommand.Parameters.Add("@Recipient", SqlDbType.NVarChar).Value = Receipt.Recipient;
				sqlCommand.ExecuteNonQuery();
				if (string.IsNullOrEmpty(Receipt.EntryGlobalID))
				{
					int? receiptType;
					receiptType = Receipt.ReceiptType;
					if ((receiptType.HasValue ? new bool?(receiptType == 10) : ((bool?)null)) == true)
					{
						if (string.IsNullOrEmpty(Receipt.CreditAcc))
						{
							Receipt.CreditAcc = Conversions.ToString(ReceiptOper.GetCodeCustomerbyid(Receipt.ClientID.Value));
						}
						string EntryGlobalId;
						EntryGlobalId = "";
						int EntryNo;
						EntryNo = 0;
						new Entry();
						ReceiptOper receiptOper;
						receiptOper = new ReceiptOper();
						if (Convert.ToDouble(Operators.ConcatenateObject("", new SqlCommand(("Select COUNT(*) from Entry where type=5 and doc_no=" + Conversions.ToString(Receipt.ReceiptNo)) ?? "", sqlConnection, sqlTransaction).ExecuteScalar())) > 0.0)
						{
							SqlDataReader sqlDataReader;
							sqlDataReader = new SqlCommand(("Select GlobalID from Entry where type=5 and doc_no=" + Conversions.ToString(Receipt.ReceiptNo)) ?? "", sqlConnection, sqlTransaction).ExecuteReader();
							sqlDataReader.Read();
							if (sqlDataReader.HasRows)
							{
								EntryGlobalId = sqlDataReader["GlobalID"].ToString();
							}
							sqlDataReader.Close();
						}
						if (string.IsNullOrEmpty(EntryGlobalId))
						{
							EntryOper.GetEntryGlobalID(ref EntryGlobalId, ref EntryNo);
						}
						Receipt.EntryGlobalID = EntryGlobalId;
						Entry entry;
						entry = receiptOper.BindReceiptToEntry(Receipt);
						if (!new EntryOper().SaveEnty(entry))
						{
							sqlTransaction.Rollback();
							string text;
							text = "خطأ أثناء الحفظ";
							if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
							{
								text = "error in saving";
							}
							MessageBox.Show(text, "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
						}
					}
				}
				sqlTransaction.Commit();
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2;
				ex2 = ex;
				sqlTransaction.Rollback();
				string text2;
				text2 = "خطأ أثناء المزامنة";
				if (Operators.CompareString(MainClass.Language, "en", TextCompare: false) == 0)
				{
					text2 = "error in saving";
				}
				MessageBox.Show((Operators.CompareString(MainClass.Language, "ar", TextCompare: false) != 0) ? (text2 + Environment.NewLine + "Error details: " + ex2.Message) : (text2 + Environment.NewLine + "تفاصيل الخطأ: " + ex2.Message), "", MessageBoxButtons.OK, MessageBoxIcon.Hand);
				ProjectData.ClearProjectError();
			}
			finally
			{
				if (sqlConnection.State != ConnectionState.Closed)
				{
					sqlConnection.Close();
				}
			}
		}

		public Receipt BindReceiptByID(string GlID)
		{
			Receipt receipt;
			receipt = new Receipt();
			SqlDataAdapter sqlDataAdapter;
			sqlDataAdapter = new SqlDataAdapter(selectConnection: MainClass.ConnObj(), selectCommandText: "select * from Receipts where  GlobalID=N'" + GlID + "' ");
			DataTable dataTable;
			dataTable = new DataTable();
			sqlDataAdapter.Fill(dataTable);
			if (dataTable.Rows.Count > 0)
			{
				receipt.GlobalID = Conversions.ToString(dataTable.Rows[0]["GlobalID"]);
				receipt.EntryGlobalID = Conversions.ToString(dataTable.Rows[0]["EntryGlobalID"]);
				receipt.ReceiptNo = Conversions.ToInteger(dataTable.Rows[0]["ReceiptNo"]);
				receipt.BranchID = checked((int)Math.Round(Conversion.Val(Operators.ConcatenateObject("", dataTable.Rows[0]["branchID"]))));
				receipt.ReceiptType = (int?)dataTable.Rows[0]["ReceiptType"];
				receipt.State = (int?)dataTable.Rows[0]["State"];
				receipt.Payment = (double?)dataTable.Rows[0]["Payment"];
				receipt.VAT = (double?)dataTable.Rows[0]["VAT"];
				receipt.NetVal = (double?)dataTable.Rows[0]["NetVal"];
				receipt.ReceiptDate = (DateTime?)dataTable.Rows[0]["ReceiptDate"];
				receipt.ReffNo = Conversions.ToString(dataTable.Rows[0]["ReffNo"]);
				receipt.Reffdate = (DateTime?)dataTable.Rows[0]["Reffdate"];
				receipt.ISDeleted = (bool?)dataTable.Rows[0]["ISDeleted"];
				receipt.Notes = Conversions.ToString(dataTable.Rows[0]["Notes"]);
				receipt.EmpId = (int?)dataTable.Rows[0]["EmpId"];
				receipt.CreditAcc = Conversions.ToString(dataTable.Rows[0]["CreditAcc"]);
				receipt.DebitAcc = Conversions.ToString(dataTable.Rows[0]["DebitAcc"]);
				receipt.ClientID = (int?)dataTable.Rows[0]["ClientID"];
				receipt.BankId = (int?)dataTable.Rows[0]["BankId"];
				receipt.TreasuryID = (int?)dataTable.Rows[0]["TreasuryID"];
				receipt.SalesManID = (int?)dataTable.Rows[0]["SalesManID"];
				receipt.PaymentType = (int?)dataTable.Rows[0]["PaymentType"];
				receipt.CheckState = (int?)dataTable.Rows[0]["CheckState"];
				receipt.CheckDate = (DateTime?)dataTable.Rows[0]["CheckDate"];
				receipt.CheckNo = Conversions.ToString(dataTable.Rows[0]["CheckNo"]);
				receipt.Checkbank = Conversions.ToString(dataTable.Rows[0]["Checkbank"]);
				receipt.Cccode = Conversions.ToString(dataTable.Rows[0]["Cccode"]);
				receipt.Sync = (bool?)dataTable.Rows[0]["Sync"];
				receipt.ClientCode = Sync.ClientCode;
				receipt.BranchType = Sync.BranchType;
				receipt.DistBranch = Sync.DistBranch;
			}
			return receipt;
		}

		public static void insertDocument(string InvGlobalID)
		{
			string docsRootPath;
			docsRootPath = Properties.Settings.Default.DocsRootPath;
			if (!Directory.Exists(docsRootPath))
			{
				Directory.CreateDirectory(docsRootPath);
			}
			SqlConnection sqlConnection;
			sqlConnection = new SqlConnection(MainClass.connstr);
			string text;
			text = docsRootPath;
			if (!Directory.Exists(text))
			{
				Directory.CreateDirectory(text);
			}
			string[] array;
			array = ReceiptOper.filePathDocument;
			foreach (string text2 in array)
			{
				if (sqlConnection.State == ConnectionState.Open)
				{
					sqlConnection.Close();
				}
				sqlConnection.Open();
				string text3;
				text3 = Path.Combine(text, "Receipt" + Conversions.ToString(Convert.ToInt32(RuntimeHelpers.GetObjectValue(new SqlCommand("SELECT ISNULL(MAX(id), 0) + 1 FROM Documents", sqlConnection).ExecuteScalar()))) + Path.GetExtension(text2));
				string fileName;
				fileName = Path.GetFileName(text2);
				File.Copy(text2, text3, overwrite: true);
				using SqlCommand sqlCommand = new SqlCommand("INSERT INTO Documents (FileName, FileUrl,GlobalID,type) VALUES (@FileName, @FileUrl,@GlobalID,3)", sqlConnection);
				sqlCommand.Parameters.AddWithValue("@FileName", fileName);
				sqlCommand.Parameters.AddWithValue("@FileUrl", text3);
				sqlCommand.Parameters.AddWithValue("@GlobalID", InvGlobalID);
				sqlCommand.ExecuteNonQuery();
			}
			sqlConnection.Close();
		}

		public static object getdocuments(ref DataTable dtt, string InvGlobalID)
		{
			SqlConnection sqlConnection;
			sqlConnection = new SqlConnection(MainClass.connstr);
			SqlCommand sqlCommand;
			sqlCommand = new SqlCommand("SELECT Id,FileName, Fileurl FROM Documents WHERE type=3 and GlobalID = @GlobalID", sqlConnection);
			sqlCommand.Parameters.AddWithValue("@GlobalID", InvGlobalID);
			SqlDataAdapter sqlDataAdapter;
			sqlDataAdapter = new SqlDataAdapter(sqlCommand);
			DataTable dataTable;
			dataTable = new DataTable();
			try
			{
				sqlConnection.Open();
				sqlDataAdapter.Fill(dataTable);
				if (dataTable.Rows.Count > 0)
				{
					dtt = dataTable;
				}
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				MessageBox.Show("حدث خطأ أثناء استرجاع البيانات: " + ex.Message);
				ProjectData.ClearProjectError();
			}
			finally
			{
				sqlConnection.Close();
			}
			object result = default(object);
			return result;
		}

		public static object GetCodeCustomerbyid(int id)
		{
			SqlConnection sqlConnection;
			sqlConnection = new SqlConnection(MainClass.connstr);
			SqlCommand sqlCommand;
			sqlCommand = new SqlCommand("SELECT AccountCode FROM Customers WHERE id=@id ", sqlConnection);
			sqlCommand.Parameters.AddWithValue("@id", id);
			SqlDataAdapter sqlDataAdapter;
			sqlDataAdapter = new SqlDataAdapter(sqlCommand);
			DataTable dataTable;
			dataTable = new DataTable();
			object result = default(object);
			try
			{
				sqlConnection.Open();
				sqlDataAdapter.Fill(dataTable);
				result = ((dataTable.Rows.Count <= 0) ? Conversions.ToInteger("-1") : Conversions.ToInteger(dataTable.Rows[0]["AccountCode"]));
				return result;
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				MessageBox.Show("حدث خطأ أثناء استرجاع البيانات: " + ex.Message);
				ProjectData.ClearProjectError();
			}
			finally
			{
				sqlConnection.Close();
			}
			return result;
		}
	}
}