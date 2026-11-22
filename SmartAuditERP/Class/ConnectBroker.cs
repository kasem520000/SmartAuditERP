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

                public static SqlConnection conn = new SqlConnection(ConnectBroker.connString);

                public static string lastErrorMsg;

                public static AESencDEC ConEncrypt = new AESencDEC();

                public static string _passcode = "";

                private static System.Windows.Forms.Timer sendTimer;

                private static string clientId = "xxxx";

                public static string _IpServer = "";

                public static bool _syncItems = false;

                public static bool _syncOper = false;

                public static bool _syncDefinitions = false;

                public static bool IsConnectedToBroker(string Connstring)
                {
                        bool result = default(bool);
                        try
                        {
                                // FIX P1-014: دعم TLS وبيانات مصادقة للوسيط عبر ملف
                                // SyncBroker.json (المفاتيح: Port / Secure / Username / Password).
                                // الافتراضي يبقى كما هو (1883 بدون TLS) للحفاظ على
                                // التوافق، وعند ضبط Secure=true يتصل عبر TLS 1.2.
                                int brokerPort = SecureConfig.ReadInt("SyncBroker.json", "Port", 1883);
                                bool brokerSecure = SecureConfig.ReadBool("SyncBroker.json", "Secure", false);
                                string brokerUser = SecureConfig.ReadValue("SyncBroker.json", "Username");
                                string brokerPass = SecureConfig.ReadValue("SyncBroker.json", "Password");

                                ConnectBroker.mqttClient = new MqttClient(
                                        ConnectBroker._IpServer,
                                        brokerPort,
                                        brokerSecure,
                                        null,
                                        null,
                                        brokerSecure ? MqttSslProtocols.TLSv1_2 : MqttSslProtocols.None);
                                ConnectBroker.clientId = Guid.NewGuid().ToString();
                                if (!string.IsNullOrEmpty(brokerUser))
                                {
                                        ConnectBroker.mqttClient.Connect(ConnectBroker.clientId, brokerUser, brokerPass ?? "");
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
                                result = new Ping().Send("8.8.8.8").Status == IPStatus.Success;
                        }
                        catch (Exception projectError)
                        {
                                ProjectData.SetProjectError(projectError);
                                result = false;
                                ProjectData.ClearProjectError();
                        }
                        return result;
                }

                public static bool CheckConnectionAndBroker()
                {
                        bool result;
                        if (ConnectBroker.IsConnectedToInternet())
                        {
                                if (!ConnectBroker.IsConnectedToBroker(ConnectBroker.connString))
                                {
                                        try
                                        {
                                                ConnectBroker.mqttClient.Connect(ConnectBroker.clientId);
                                        }
                                        catch (Exception projectError)
                                        {
                                                ProjectData.SetProjectError(projectError);
                                                result = false;
                                                ProjectData.ClearProjectError();
                                                goto IL_004b;
                                        }
                                }
                                result = true;
                        }
                        else
                        {
                                result = false;
                        }
                        goto IL_004b;
                IL_004b:
                        return result;
                }
        }
}