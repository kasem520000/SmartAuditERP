using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace SmartAuditUpdater
{
    /// <summary>
    /// إصلاح المرحلة الأولى للنتيجة:
    ///   P1-020 (High/update-security): تثبيت حزمة التحديث دون تحقق توقيع
    ///                                   أو بيان موثوق للملفات
    ///
    /// عقد المانيفست (نص UTF-8 بأسطر LF):
    ///   SHA256 &lt;hex&gt; &lt;مسار-نسبي&gt;        سطر لكل ملف
    ///   SIG &lt;base64&gt;                       سطر أخير: توقيع RSA-SHA256 فوق كل ما قبله
    ///
    /// المفتاح الخاص يبقى مع خطوة الإصدار فقط (خارج المستودع وخارج التطبيق).
    /// المفتاح العام يُضمَّن هنا في PublicKeyXml عند أول إصدار موقّع.
    /// أي فشل في أي خطوة = رفض الحزمة كاملة (fail-closed) — لا نسخة ملف واحدة قبل نجاح التحقق كله.
    /// </summary>
    public static class ManifestSignatureVerifier
    {
        // TODO(دمج): استبدل بالمفتاح العام الفعلي عند تجهيز خطوة الإصدار الموقعة.
        private const string PublicKeyXml =
            "<RSAKeyValue><Modulus>REPLACE_WITH_RELEASE_PUBLIC_KEY</Modulus><Exponent>AQAB</Exponent></RSAKeyValue>";

        /// <param name="manifestPath">مسار ملف المانيفست المنزَّل مع الحزمة.</param>
        /// <param name="packageRoot">مجلد الحزمة المنزولة (كل المسارات النسبية تُحل داخله).</param>
        /// <returns>true فقط إذا نجح توقيع المانيفست وتطابقت تجزئة كل ملف مدرج.</returns>
        public static bool VerifyManifest(string manifestPath, string packageRoot)
        {
            try
            {
                string[] lines = File.ReadAllLines(manifestPath, Encoding.UTF8);
                if (lines == null || lines.Length < 2) return false;

                // السطر الأخير يحمل التوقيع فوق كل الأسطر قبله.
                string sigLine = lines[lines.Length - 1];
                if (sigLine == null || !sigLine.StartsWith("SIG ", StringComparison.Ordinal)) return false;
                byte[] signature;
                try { signature = Convert.FromBase64String(sigLine.Substring(4).Trim()); }
                catch (FormatException) { return false; }

                var payload = new StringBuilder();
                for (int i = 0; i < lines.Length - 1; i++)
                    payload.Append(lines[i]).Append('\n');

                using (var rsa = new RSACryptoServiceProvider())
                {
                    rsa.FromXmlString(PublicKeyXml);
                    byte[] data = Encoding.UTF8.GetBytes(payload.ToString());
                    bool sigOk = rsa.VerifyData(data, signature, CryptoConfig.MapNameToOID("SHA256"));
                    if (!sigOk) return false; // مانيفست معدَّل — أوقف التثبيت فوراً
                }

                // التوقيع سليم → تحقق من تجزئة كل ملف قبل نسخ أي شيء.
                string rootFull = Path.GetFullPath(packageRoot);
                foreach (string line in lines)
                {
                    if (line == null || line.Length == 0) continue;
                    if (line.StartsWith("SIG ", StringComparison.Ordinal)) continue;

                    string[] parts = line.Split(' ');
                    if (parts.Length != 3 || parts[0] != "SHA256") return false;

                    // حارس اجتياز المسار: المسار النسبي لا يخرج من جذر الحزمة.
                    string full = Path.GetFullPath(Path.Combine(rootFull, parts[2]));
                    if (!full.StartsWith(rootFull, StringComparison.OrdinalIgnoreCase)) return false;
                    if (!File.Exists(full)) return false;

                    using (var sha = SHA256.Create())
                    using (var fs = File.OpenRead(full))
                    {
                        string actualHex = ToHex(sha.ComputeHash(fs));
                        if (!string.Equals(actualHex, parts[1], StringComparison.OrdinalIgnoreCase))
                            return false; // ملف معدَّل/تالف — أوقف التثبيت
                    }
                }
                return true;
            }
            catch
            {
                return false; // أي استثناء = رفض الحزمة (fail-closed)
            }
        }

        /// <summary>أداة مساعدة لخطوة الإصدار: توليد أسطر المانيفست (تُستخدم خارج التطبيق).</summary>
        public static string BuildManifestEntry(string packageRoot, string relativePath)
        {
            using (var sha = SHA256.Create())
            using (var fs = File.OpenRead(Path.Combine(packageRoot, relativePath)))
            {
                return "SHA256 " + ToHex(sha.ComputeHash(fs)) + " " + relativePath.Replace('\\', '/');
            }
        }

        private static string ToHex(byte[] bytes)
        {
            var sb = new StringBuilder(bytes.Length * 2);
            foreach (byte b in bytes) sb.Append(b.ToString("x2"));
            return sb.ToString();
        }
    }
}
