using System;
using System.Data;
using System.Data.SqlClient;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;
using log4net;
using zkemkeeper;

namespace SmartAuditERP
{

	public class FingerPrintDevice
	{
		public static CZKEM axCZKEM1 = (CZKEM)Activator.CreateInstance(Marshal.GetTypeFromCLSID(new Guid("00853A19-BD51-419B-9269-2DABE57EB61F")));

		public static bool ISconnectedBar = false;

		private static SqlConnection conn = MainClass.ConnObj();

		private static int iMachineNumber;

		private static readonly ILog Logger = LogManager.GetLogger(typeof(FingerPrintDevice));
		private static int _importRunning;
		// Process-local only: after an uncertain commit or device clear, do not
		// automatically replay the same log during this application session.
		private static int _replayRiskLocked;

		[DllImport("kernel32", CharSet = CharSet.Ansi, ExactSpelling = true, SetLastError = true)]
		private static extern void Sleep(long dwMilliseconds);

		public static void ConnectFPscanner(string IP, string Port)
		{
			try
			{
				FingerPrintDevice.ISconnectedBar = FingerPrintDevice.axCZKEM1.Connect_Net(IP, Convert.ToInt32(Port));
				if (FingerPrintDevice.ISconnectedBar)
				{
					FingerPrintDevice.iMachineNumber = 1;
					FingerPrintDevice.axCZKEM1.RegEvent(FingerPrintDevice.iMachineNumber, 65535);
				}
				else
				{
					int dwErrorCode = default(int);
					FingerPrintDevice.axCZKEM1.GetLastError(ref dwErrorCode);
				}
			}
			catch (Exception projectError)
			{
				ProjectData.SetProjectError(projectError);
				ProjectData.ClearProjectError();
			}
		}

		public static void loadAttendData()
		{
			if (Interlocked.CompareExchange(ref _importRunning, 1, 0) != 0) return;
			bool enableAttemptNeeded = false;
			bool committed = false;
			bool alreadyLocked = Volatile.Read(ref _replayRiskLocked) != 0;
			SqlTransaction sqlTransaction = null;
			try
			{
				if (Volatile.Read(ref _replayRiskLocked) != 0) return;
				if (FingerPrintDevice.conn.State != ConnectionState.Open)
					FingerPrintDevice.conn.Open();
				sqlTransaction = FingerPrintDevice.conn.BeginTransaction();
				new SqlCommand();
				new ListViewItem("Items", 0);
				// Repair R-118 (P7-008): even an exception during the COM call
				// can leave the actual device state unknown; always attempt recovery.
				enableAttemptNeeded = true;
				if (!FingerPrintDevice.axCZKEM1.EnableDevice(FingerPrintDevice.iMachineNumber, bFlag: false))
				{
					Logger.Error("Fingerprint device disable failed; import was not started.");
					return;
				}
				if (FingerPrintDevice.axCZKEM1.ReadGeneralLogData(FingerPrintDevice.iMachineNumber))
				{
					int dwTMachineNumber = default(int);
					int dwEnrollNumber = default(int);
					int dwEMachineNumber = default(int);
					int dwVerifyMode = default(int);
					int dwInOutMode = default(int);
					int dwYear = default(int);
					int dwMonth = default(int);
					int dwDay = default(int);
					int dwHour = default(int);
					int dwMinute = default(int);
					while (FingerPrintDevice.axCZKEM1.GetGeneralLogData(FingerPrintDevice.iMachineNumber, ref dwTMachineNumber, ref dwEnrollNumber, ref dwEMachineNumber, ref dwVerifyMode, ref dwInOutMode, ref dwYear, ref dwMonth, ref dwDay, ref dwHour, ref dwMinute))
					{
						SqlCommand sqlCommand;
						sqlCommand = new SqlCommand("AddGdata", FingerPrintDevice.conn, sqlTransaction);
						sqlCommand.CommandType = CommandType.StoredProcedure;
						sqlCommand.Parameters.Add("@_machineNumber", SqlDbType.Int).Value = FingerPrintDevice.iMachineNumber;
						sqlCommand.Parameters.Add("@_enrollNumber", SqlDbType.Int).Value = dwEnrollNumber;
						sqlCommand.Parameters.Add("@_enrollMachineNumber", SqlDbType.Int).Value = dwTMachineNumber;
						sqlCommand.Parameters.Add("@_verifyMode", SqlDbType.Int).Value = dwVerifyMode;
						sqlCommand.Parameters.Add("@_inOutMode", SqlDbType.Int).Value = dwInOutMode;
						sqlCommand.Parameters.Add("@_year", SqlDbType.Int).Value = dwYear;
						sqlCommand.Parameters.Add("@_month", SqlDbType.Int).Value = dwMonth;
						sqlCommand.Parameters.Add("@_day", SqlDbType.Int).Value = dwDay;
						sqlCommand.Parameters.Add("@_hour", SqlDbType.Int).Value = dwHour;
						sqlCommand.Parameters.Add("@_minute", SqlDbType.Int).Value = dwMinute;
						sqlCommand.Parameters.Add("@takeJoureny", SqlDbType.Int).Value = 0;
						sqlCommand.Parameters.Add("@_statu", SqlDbType.Bit).Value = dwInOutMode;
						sqlCommand.ExecuteNonQuery();
					}
					// Commit and device clear cannot be one transaction. Latch before
					// commit; only a confirmed clear permits another automatic import.
					Volatile.Write(ref _replayRiskLocked, 1);
					sqlTransaction.Commit();
					committed = true;
					if (FingerPrintDevice.axCZKEM1.ClearGLog(FingerPrintDevice.iMachineNumber))
					{
						Volatile.Write(ref _replayRiskLocked, 0);
						FingerPrintDevice.axCZKEM1.RefreshData(FingerPrintDevice.iMachineNumber);
					}
				}
				else
				{
					int dwErrorCode = default(int);
					FingerPrintDevice.axCZKEM1.GetLastError(ref dwErrorCode);
					if (dwErrorCode == 0)
					{
					}
				}
			}
			catch (Exception ex)
			{
				Logger.Error("Fingerprint import failed (" + ex.GetType().Name + ").");
			}
			finally
			{
				if (sqlTransaction != null && !committed)
				{
					try { sqlTransaction.Rollback(); }
					catch (Exception ex)
					{
						Volatile.Write(ref _replayRiskLocked, 1);
						Logger.Error("Fingerprint rollback was not confirmed (" + ex.GetType().Name + ").");
					}
				}
				if (enableAttemptNeeded)
				{
					try
					{
						if (!FingerPrintDevice.axCZKEM1.EnableDevice(FingerPrintDevice.iMachineNumber, bFlag: true))
							Logger.Error("Fingerprint device re-enable failed; manual intervention may be required.");
					}
					catch (Exception ex)
					{
						Logger.Error("Fingerprint device re-enable failed (" + ex.GetType().Name + ").");
					}
				}
				try
				{
					if (FingerPrintDevice.conn.State != ConnectionState.Closed)
						FingerPrintDevice.conn.Close();
				}
				catch (Exception ex)
				{
					Logger.Error("Fingerprint connection cleanup failed (" + ex.GetType().Name + ").");
				}
				bool needsReconciliation = Volatile.Read(ref _replayRiskLocked) != 0;
				Interlocked.Exchange(ref _importRunning, 0);
				if (needsReconciliation && !alreadyLocked)
				{
					Logger.Error("Fingerprint automatic import stopped: reconcile database and device logs before restarting.");
					try
					{
						MessageBox.Show("توقف استيراد البصمة لتجنب التكرار. راجع سجل الجهاز وقاعدة البيانات قبل إعادة تشغيل البرنامج.",
							"تنبيه", MessageBoxButtons.OK, MessageBoxIcon.Warning);
					}
					catch (Exception ex)
					{
						Logger.Error("Fingerprint operator alert failed (" + ex.GetType().Name + ").");
					}
				}
			}
		}
	}
}