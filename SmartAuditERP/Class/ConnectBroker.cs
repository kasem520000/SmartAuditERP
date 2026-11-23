using System;
using System.Data.SqlClient;
using System.Net.NetworkInformation;
using System.Timers;
using AuditorAPI.Models;
using Microsoft.VisualBasic.CompilerServices;
using uPLibrary.Networking.M2Mqtt;

namespace SmartAuditERP
{

        [StandardModule]
        internal sealed class ConnectBroker
        {
                public static MqttClient mqttClient;

                public static string ClientCode = "1006";

                public static string connString = "";

                public static SqlConnection conn = MainClass.CreateSqlConnection(ConnectBroker.connString);

                public static string lastErrorMsg;

                public static AESencDEC ConEncrypt = new AESencDEC();

                public static string _passcode = "";

                private static System.Windows.Forms.Timer sendTimer;

                // P5-001 (مكمل V-016): صار عاماً — إعادة التوصيل في SendData تحتاج
                // نفس هوية الجلسة (كانت private فيمنع الوصول CS0122)
                public static string clientId = "xxxx";

                public static string _IpServer = "";

                // P1-014 fix: إعدادات أمان اتصال الوسيط — TLS واعتماد قابلان للتهيئة
                // من جدول SettingSync (أعمدة MqttPort/MqttUseTls/MqttUser/MqttPass).
                // الافتراضي يراعي التوافق مع النشر القائم (1883/بلا TLS)؛ تفعيل الأمان
                // ضبط MqttUseTls=1 و MqttPort=8883 واعتماد الوسيط — موثق في REPAIR-LOG.
                public static int _mqttPort = 1883;

                public static bool _mqttUseTls = false;

                public static string _mqttUser = "";

                public static string _mqttPass = "";

                public static bool _syncItems = false;

                public static bool _syncOper = false;

                public static bool _syncDefinitions = false;

                public static bool IsConnectedToBroker(string Connstring)
                {
                        bool result = default(bool);
                        try
                        {
                                // P5-001 fix: جلسة واحدة مستقرة — لا يُستبدل العميل ولا هوية الجلسة
                                // عند كل فحص. الفحص يعيد استخدام العميل المتصل، والمقطوع يعاد
                                // توصيله بنفس clientId حتى تبقى معالجات الاستقبال (المشتركة
                                // على هذه النسخة) واشتراكات الجلسة سارية. عميل جديد يُنشأ مرة
                                // واحدة فقط عند عدم وجوده.
                                if (ConnectBroker.mqttClient != null && ConnectBroker.mqttClient.IsConnected)
                                {
                                        return true;
                                }

                                // P1-014 fix: المنفذ وTLS من الإعدادات، والاتصال باعتماد الوسيط عند توفره.
                                MqttSslProtocols sslProtocol = ConnectBroker._mqttUseTls
                                        ? MqttSslProtocols.TLSv1_2
                                        : MqttSslProtocols.None;

                                if (ConnectBroker.mqttClient == null)
                                {
                                        ConnectBroker.mqttClient = new MqttClient(
                                                ConnectBroker._IpServer,
                                                ConnectBroker._mqttPort,
                                                ConnectBroker._mqttUseTls,
                                                null, null, sslProtocol);
                                        ConnectBroker.clientId = Guid.NewGuid().ToString();
                                }

                                if (string.IsNullOrEmpty(ConnectBroker.clientId))
                                {
                                        ConnectBroker.clientId = Guid.NewGuid().ToString();
                                }

                                if (!string.IsNullOrEmpty(ConnectBroker._mqttUser))
                                {
                                        // P1-014 fix: بيانات اعتماد الوسيط (المخزنة DPAPI) عند تهيئتها
                                        string plainPass = Class.Security.SecretProtector
                                                .Unprotect(ConnectBroker._mqttPass) ?? "";
                                        ConnectBroker.mqttClient.Connect(
                                                ConnectBroker.clientId,
                                                ConnectBroker._mqttUser,
                                                plainPass);
                                }
                                else
                                {
                                        ConnectBroker.mqttClient.Connect(ConnectBroker.clientId);
                                }

                                if (ConnectBroker.mqttClient.IsConnected)
                                {
                                        result = true;
                                        return result;
                                }
                                Console.WriteLine("Failed to connect to the broker.");
                                result = false;
                                return result;
                        }
                        catch (OutOfMemoryException ex)
                        {
                                ProjectData.SetProjectError(ex);
                                Console.WriteLine("Memory error: " + ex.Message);
                                GC.Collect();
                                ProjectData.ClearProjectError();
                        }
                        catch (Exception ex2)
                        {
                                ProjectData.SetProjectError(ex2);
                                Console.WriteLine("Error: " + ex2.Message);
                                ProjectData.ClearProjectError();
                        }
                        return result;
                }

                public static bool IsConnectedToInternet()
                {
                        bool result;
                        try
                        {
                                // P5-002 fix: الفحص أصبح TCP إلى الوسيط نفسه (الوجهة الفعلية)
                                // بدل ICMP إلى عنوان إنترنت خارجي — ICMP محجوب كثيرًا في
                                // شبكات تسمح بـ MQTT فوق TCP، فكان بوابة الوصول تمنع
                                // المزامنة بلا سبب.
                                result = ConnectBroker.CanReachBrokerTcp();
                        }
                        catch (Exception projectError)
                        {
                                ProjectData.SetProjectError(projectError);
                                result = false;
                                ProjectData.ClearProjectError();
                        }
                        return result;
                }

                // P5-002 fix: فحص TCP قصير المهلة إلى وسيط MQTT المُعدّ.
                private static bool CanReachBrokerTcp()
                {
                    try
                    {
                        if (string.IsNullOrEmpty(ConnectBroker._IpServer))
                        {
                            return false;
                        }
                        using (System.Net.Sockets.TcpClient tcp = new System.Net.Sockets.TcpClient())
                        {
                            IAsyncResult ar = tcp.BeginConnect(
                                ConnectBroker._IpServer,
                                ConnectBroker._mqttPort,
                                null,
                                null);
                            bool reached = ar.AsyncWaitHandle.WaitOne(3000);
                            if (reached && tcp.Connected)
                            {
                                tcp.EndConnect(ar);
                                return true;
                            }
                            return false;
                        }
                    }
                    catch
                    {
                        return false;
                    }
                }

                public static bool CheckConnectionAndBroker()
                {
                        // P5-002 fix: البوابة لم تعد ICMP ثم إعادة اتصال مزدوجة — محاولة
                        // الاتصال الفعلية بالوسيط هي الفيصل (تعيد استخدام الجلسة، P5-001).
                        return ConnectBroker.IsConnectedToBroker(ConnectBroker.connString);
                }
        }
}