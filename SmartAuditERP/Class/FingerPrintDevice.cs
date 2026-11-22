using System;
using System.Data;
using System.Data.SqlClient;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using log4net;
using Microsoft.VisualBasic.CompilerServices;
using zkemkeeper;

namespace SmartAuditERP
{

        public class FingerPrintDevice
        {
                public static CZKEM axCZKEM1 = (CZKEM)Activator.CreateInstance(Marshal.GetTypeFromCLSID(new Guid("00853A19-BD51-419B-9269-2DABE57EB61F")));

                public static bool ISconnectedBar = false;

                private static SqlConnection conn = MainClass.ConnObj();

                private static int iMachineNumber;

                private static readonly ILog Logger =
                        LogManager.GetLogger(Environment.MachineName);

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
                        // P7-008 fix (حراسة): لا استيراد قبل اتصال جهاز — المؤقت
                        // يستدعي كل دقيقة حتى مع جهاز غير موصول
                        if (!FingerPrintDevice.ISconnectedBar)
                        {
                                return;
                        }
                        if (FingerPrintDevice.conn.State != ConnectionState.Open)
                        {
                                FingerPrintDevice.conn.Open();
                        }
                        SqlTransaction sqlTransaction;
                        sqlTransaction = FingerPrintDevice.conn.BeginTransaction();
                        // P7-008 fix: إعادة تمكين الجهاز تتبع finally لا المسار
                        // السليم فقط — كان أي استثناء بين التعطيل وإعادة التمكين
                        // (فشل COM أو خطأ SQL في دفعة الإدراج) يبتلعه catch ويترك
                        // الجهاز معطلاً حتى إعادة تشغيل التطبيق
                        bool deviceDisabled = false;
                        int imported = 0;
                        try
                        {
                                new SqlCommand();
                                new ListViewItem("Items", 0);
                                FingerPrintDevice.axCZKEM1.EnableDevice(FingerPrintDevice.iMachineNumber, bFlag: false);
                                deviceDisabled = true;
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
                                                imported = checked(imported + 1);
                                        }
                                        sqlTransaction.Commit();
                                        // P7-009 fix: الالتزام سابق للمسح (النظام القائم) لكن
                                        // فشل المسح يُسجل صريحاً — سجل الجهاز يبقى موجباً
                                        // فيعيد المؤقت قراءته، والحارس داخل الإجراء AddGdata
                                        // يمنع تكرار الإدراج (راجع AlterDb)
                                        if (FingerPrintDevice.axCZKEM1.ClearGLog(FingerPrintDevice.iMachineNumber))
                                        {
                                                FingerPrintDevice.axCZKEM1.RefreshData(FingerPrintDevice.iMachineNumber);
                                        }
                                        else
                                        {
                                                ThreadContext.Properties["Machine"] = FingerPrintDevice.iMachineNumber;
                                                Logger.Warn(
                                                        "فشل مسح سجل البصمة بعد إقرار الدفعة — سيعاد قراءة السجل في الدورة التالية وحارس AddGdata يمنع ازدواج الإدراج");
                                        }
                                        ThreadContext.Properties["Machine"] = FingerPrintDevice.iMachineNumber;
                                        ThreadContext.Properties["Count"] = imported;
                                        Logger.Info("استيراد بصمة ملتزم");
                                }
                                else
                                {
                                        int dwErrorCode = default(int);
                                        FingerPrintDevice.axCZKEM1.GetLastError(ref dwErrorCode);
                                        if (dwErrorCode == 0)
                                        {
                                        }
                                        try
                                        {
                                                sqlTransaction.Rollback();
                                        }
                                        catch
                                        {
                                        }
                                }
                        }
                        catch (Exception projectError)
                        {
                                ProjectData.SetProjectError(projectError);
                                // P7-008 fix: تراجع صريح لمعاملة الدفعة قبل بلع
                                // الاستثناء — لا كتابة معلقة تنتظر إغلاق الاتصال
                                try
                                {
                                        sqlTransaction.Rollback();
                                }
                                catch
                                {
                                }
                                ThreadContext.Properties["Machine"] = FingerPrintDevice.iMachineNumber;
                                Logger.Error(
                                        "فشل استيراد دفعة البصمة — الدفعة غير ملتزمة وسجل الجهاز لم يُمسح",
                                        projectError);
                                ProjectData.ClearProjectError();
                        }
                        finally
                        {
                                // P7-008 fix: إعادة التمكين في finally — أي مسار خروج
                                if (deviceDisabled)
                                {
                                        try
                                        {
                                                FingerPrintDevice.axCZKEM1.EnableDevice(FingerPrintDevice.iMachineNumber, bFlag: true);
                                        }
                                        catch
                                        {
                                        }
                                }
                                if (FingerPrintDevice.conn.State != ConnectionState.Closed)
                                {
                                        FingerPrintDevice.conn.Close();
                                }
                        }
                }
        }
}
