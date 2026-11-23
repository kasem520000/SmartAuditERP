using System;
using System.Security.Cryptography;

namespace SmartAuditERP.Class.Security
{
    /// <summary>
    /// إصلاح المرحلة الأولى للنتائج:
    ///   P1-008 (Critical/security): بوابات إدارية بكلمات ثابتة وحساب دعم بتوليد متوقع
    ///   P1-009 (High/secrets): حفظ كلمات مرور التطبيق وقاعدة البيانات نصياً
    ///   P1-010 (High/secrets): تخزين واسترجاع كلمات مرور المستخدمين كنص أصلي
    ///
    /// يستبدل كل مقارنة/تخزين نصي لكلمات المرور بتجزئة PBKDF2-HMAC-SHA256
    /// (ملح عشوائي لكل كلمة + 100,000 تكرار + مقارنة زمن-ثابت).
    /// يستهدف net8.0-windows — يستخدم RandomNumberGenerator وCryptographicOperations.
    /// </summary>
    public static class PasswordHasher
    {
        private const int SaltSize = 16;        // ملح 128-بت
        private const int KeySize = 32;         // مفتاح مشتق 256-بت
        private const int Iterations = 100000;  // خط الأساس OWASP لـ PBKDF2-SHA256

        /// <summary>
        /// صيغة التخزين: PBKDF2$iterations$saltBase64$hashBase64
        /// (صيغة ذاتية الوصف تسمح بترقية المعاملات مستقبلاً دون كسر القديم)
        /// </summary>
        public static string Hash(string password)
        {
            if (string.IsNullOrEmpty(password))
                throw new ArgumentException("Password must not be empty.", nameof(password));

            byte[] salt = RandomNumberGenerator.GetBytes(SaltSize);

            using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, Iterations, HashAlgorithmName.SHA256))
            {
                byte[] key = pbkdf2.GetBytes(KeySize);
                return "PBKDF2$" + Iterations + "$" + Convert.ToBase64String(salt) + "$" + Convert.ToBase64String(key);
            }
        }

        /// <summary>
        /// تحقق fail-closed: أي غياب/تلف/صيغة غير معروفة في المخزن = رفض الدخول.
        /// يشمل ذلك (منذ مسحة التحقق) التجزئة الفارغة/القصيرة والتكرارات المرضية.
        /// </summary>
        public static bool Verify(string password, string stored)
        {
            if (string.IsNullOrEmpty(stored)) return false;
            if (password == null) password = "";

            string[] parts = stored.Split('$');
            if (parts.Length != 4 || parts[0] != "PBKDF2") return false;

            int iterations;
            // سقف التكرارات يمنع قيمًا مرضية (مثل 999,999,999) من تعليق الدخول —
            // القيم المشروعة يولدها Hash() عند 100,000 والسقف يترك 50× رأس ترقية.
            if (!int.TryParse(parts[1], out iterations) || iterations < 1 || iterations > 5_000_000)
                return false;

            byte[] salt, expected;
            try
            {
                salt = Convert.FromBase64String(parts[2]);
                expected = Convert.FromBase64String(parts[3]);
            }
            catch (FormatException) { return false; }

            // تحصين مسحة التحقق (verification sweep): تجزئة فارغة/قصيرة كانت تقبل
            // أي كلمة مرور — GetBytes(0) يعيد مصفوفة فارغة وFixedTimeEquals(فارغ,فارغ)=true.
            // أي قيمة مخزنة أقصر من 128-بت مرفوضة مهما كان باقي الصيغة سليمًا.
            if (expected.Length < 16) return false;

            using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, iterations, HashAlgorithmName.SHA256))
            {
                byte[] actual = pbkdf2.GetBytes(expected.Length);
                return FixedTimeEquals(actual, expected);
            }
        }

        /// <summary>
        /// مقارنة زمن-ثابت تمنع هجمات قياس التوقيت على المقارنة.
        /// </summary>
        private static bool FixedTimeEquals(byte[] a, byte[] b)
        {
            if (a == null || b == null || a.Length != b.Length) return false;
            return CryptographicOperations.FixedTimeEquals(a, b);
        }

        /// <summary>
        /// مهاجرة P1-010: يُستدعى بعد دخول ناجح بالنص القديم لتحويل الصف إلى التجزئة
        /// ثم تصفير عمود النص القديم. أي قيمة لا تبدأ بـ PBKDF2$ تعتبر تحتاج مهاجرة.
        /// </summary>
        public static bool NeedsMigration(string stored)
        {
            return !(stored != null && stored.StartsWith("PBKDF2$", StringComparison.Ordinal));
        }
    }
}
