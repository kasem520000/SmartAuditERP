using System;
using System.IO;
using Newtonsoft.Json.Linq;

namespace SmartAuditERP
{
    /// <summary>
    /// قراءة الإعدادات الحساسة من ملفات JSON خارج المستودع بجوار ملف التنفيذ.
    /// بديل آمن عن القيم المثبتة في الكود (كلمات مرور البوابات الإدارية،
    /// بيانات وسيط المزامنة، بيانات رفع النسخ الاحتياطي).
    ///
    /// الملفات المتوقعة (لا تُرفع إلى المستودع وتُنشأ يدوياً عند النشر):
    ///  - AdminGates.json     : كلمات مرور البوابات الإدارية (frmCheckPwd/frmLogServerSettings)
    ///  - SyncBroker.json     : إعدادات وسيط MQTT (منفذ/TLS/مستخدم)
    ///  - BackupUpload.json   : إعدادات رفع النسخة الاحتياطية عبر FTPS
    ///  - UpdateConfig.json   : رابط التحديث القديم (FrmUpdate)
    ///
    /// مثال AdminGates.json:
    /// {
    ///   "Gate0":   "كلمة-مرور-قوية",
    ///   "Gate100": "كلمة-مرور-قوية",
    ///   "Gate200": "كلمة-مرور-قوية",
    ///   "Gate300": "كلمة-مرور-قوية",
    ///   "Gate400": "كلمة-مرور-قوية",
    ///   "LogServer": "كلمة-مرور-قوية"
    /// }
    ///
    /// المرجع: docs/audit/FIXES-LOG-94ae8414.md (إصلاح P1-008 و P1-014 و P1-015 و NEW-021)
    /// </summary>
    public static class SecureConfig
    {
        /// <summary>
        /// قراءة قيمة نصية من ملف إعدادات JSON بجوار ملف التنفيذ.
        /// تعيد null عند غياب الملف أو المفتاح أو عند أي خطأ (مبدأ الإغلاق).
        /// </summary>
        public static string ReadValue(string fileName, string key)
        {
            try
            {
                string path = Path.Combine(
                    AppDomain.CurrentDomain.BaseDirectory, fileName);

                if (!File.Exists(path)) return null;

                string json = File.ReadAllText(path);
                if (string.IsNullOrWhiteSpace(json)) return null;

                JObject obj = JObject.Parse(json);
                JToken token = obj?[key];

                if (token == null || token.Type != JTokenType.String)
                    return null;

                string value = token.ToString();
                return string.IsNullOrWhiteSpace(value) ? null : value;
            }
            catch
            {
                // أي خطأ في قراءة الإعدادات يعامل كعدم وجودها (fail-closed)
                return null;
            }
        }

        /// <summary>
        /// قراءة قيمة رقمية (مع قيمة افتراضية عند الغياب/الخطأ).
        /// </summary>
        public static int ReadInt(string fileName, string key, int defaultValue)
        {
            string raw = ReadValue(fileName, key);
            return int.TryParse(raw, out int value) ? value : defaultValue;
        }

        /// <summary>
        /// قراءة قيمة منطقية (مع قيمة افتراضية عند الغياب/الخطأ).
        /// </summary>
        public static bool ReadBool(string fileName, string key, bool defaultValue)
        {
            string raw = ReadValue(fileName, key);
            return bool.TryParse(raw, out bool value) ? value : defaultValue;
        }
    }
}
