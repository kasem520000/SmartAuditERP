using System;
using System.Security.Cryptography;
using System.Text;

namespace SmartAuditERP.Class.Security
{
    /// <summary>
    /// إصلاح المرحلة الأولى للنتائج:
    ///   P1-009 (High/secrets): «تذكرني» يحفظ كلمة المرور نصياً — يصبح DPAPI مشفراً
    ///   P1-014 (High/transport-security): بيانات اعتماد وسيط MQTT — تُقرأ من هذا المخزن لا من نص الكود
    ///   P1-015 (High/backup-security): اعتماد FTP الثابت — يُخزن هنا بدلاً من النص الصريح
    ///
    /// نطاق DPAPI: CurrentUser — نفس حساب ويندوز الذي حفظ السر هو من يقرؤه فقط.
    /// القاعدة: أي فشل فك (مستخدم مختلف/تلف/قيمة قديمة نصية) = إرجاع null
    /// والمستدعي يطلب الإدخال من جديد — لا يقع أبداً إلى «استخدم النص كما هو».
    /// مرجع التجميع: System.Security (أضفه للمشروع إن لم يكن مضافاً).
    /// </summary>
    public static class SecretProtector
    {
        // إنتروبيا خاصة بالتطبيق تربط السر بهذا البرنامج تحديداً.
        private static readonly byte[] Entropy = Encoding.UTF8.GetBytes("SmartAuditERP.v1.secret");

        /// <summary>يشفّر نصاً ويعيد Base64 جاهزاً للحفظ في الإعدادات/القاعدة.</summary>
        public static string Protect(string plain)
        {
            if (plain == null) return null;
            byte[] plainBytes = Encoding.UTF8.GetBytes(plain);
            byte[] cipher = ProtectedData.Protect(plainBytes, Entropy, DataProtectionScope.CurrentUser);
            return Convert.ToBase64String(cipher);
        }

        /// <summary>يفك Base64 المشفر؛ null عند أي فشل (fail-closed).</summary>
        public static string Unprotect(string protectedBase64)
        {
            if (string.IsNullOrEmpty(protectedBase64)) return null;
            try
            {
                byte[] cipher = Convert.FromBase64String(protectedBase64);
                byte[] plain = ProtectedData.Unprotect(cipher, Entropy, DataProtectionScope.CurrentUser);
                return Encoding.UTF8.GetString(plain);
            }
            catch (CryptographicException)
            {
                return null; // مستخدم مختلف أو بيانات معدلة — تعامل كغير موجودة
            }
            catch (FormatException)
            {
                return null; // قيمة قديمة بنص صريح — أجبر إعادة الإدخال، لا تستخدمها أبداً
            }
        }

        // ---------------------------------------------------------------------
        // نقاط الدمج (تحدَّث في REPAIR-LOG-STAGE1 عند التنفيذ الفعلي):
        //  1) frmUserLogin «تذكرني»:  settings.RememberedPwd = SecretProtector.Protect(pwd)
        //     وعند التحميل: pwd = SecretProtector.Unprotect(settings.RememberedPwd) ?? ""
        //     كلمة مرور SQL لا تُحفظ إطلاقاً مع «تذكرني» (قرار P1-009) — تُطلب كل جلسة.
        //  2) ConnectBroker: بيانات الوسيط من SecretProtector لا من ثوابت الكود،
        //     والاتصال يُبنى مع TLS افتراضياً (P1-014).
        //  3) frmBackupRstore: اعتماد FTP عبر SecretProtector + EnableSsl (P1-015).
        // ---------------------------------------------------------------------
    }
}
