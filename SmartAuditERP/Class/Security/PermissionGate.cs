using System;

namespace SmartAuditERP.Class.Security
{
    /// <summary>
    /// إصلاح المرحلة الأولى للنتيجة:
    ///   P1-012 (High/authorization): تطبيق الصلاحيات لا يرفض افتراضياً عند
    ///                                 غياب السجل أو فشل الاستعلام
    ///
    /// قاعدة واحدة لا استثناء فيها: كل شك = منع (fail-closed).
    /// أي مسار في التطبيق كان يسمح عند غياب صف الصلاحية أو عند استثناء الاستعلام
    /// يمر عبر هذه البوابة بدلاً من منطقه الخاص.
    /// </summary>
    public static class PermissionGate
    {
        public enum Decision
        {
            Allow = 1,
            Deny = 0
        }

        /// <param name="querySucceeded">false عند أي استثناء في استعلام الصلاحيات أو غياب الجدول الناتج.</param>
        /// <param name="permissionRowExists">true فقط إذا قُرئ صف صلاحيات فعلي للمستخدم/الشاشة.</param>
        /// <param name="permissionValue">قيمة الصلاحية عندما يوجد الصف.</param>
        public static Decision Decide(bool querySucceeded, bool permissionRowExists, bool permissionValue)
        {
            if (!querySucceeded) return Decision.Deny;        // فشل الاستعلام = منع
            if (!permissionRowExists) return Decision.Deny;   // لا صف = منع (لا «الافتراضي مسموح»)
            return permissionValue ? Decision.Allow : Decision.Deny;
        }

        /// <summary>
        /// مسار التسجيل الموحد للمنع — يستخدم هوية مستخدم الجلسة الفعلية
        /// (يرتبط بإصلاح P1-031: لا DB_NAME() كاسم مستخدم طرفي).
        /// لا يرمي أبداً: فشل التسجيل لا يفتح الباب.
        /// </summary>
        public static void LogDeny(string sessionUser, string permissionKey, string reason)
        {
            try
            {
                // نقطة الدمج: التوصيل بمغسلة سجل التطبيق الفعلية عند التنفيذ.
                System.Diagnostics.Trace.WriteLine(string.Format(
                    "PERM-DENY user={0} key={1} reason={2} at={3:o}",
                    sessionUser ?? "?", permissionKey ?? "?", reason ?? "?", DateTime.UtcNow));
            }
            catch
            {
                // ابتلاع مقصود وموثق: التسجيل لا يعطل قرار المنع.
            }
        }

        // ---------------------------------------------------------------------
        // نمط الدمج في MainClass.cs:383-455 وكل المستدعين (94 موقعاً موثقة لـ P1-013):
        //   var d = PermissionGate.Decide(queryOk, rowExists, value);
        //   if (d == PermissionGate.Decision.Deny)
        //   {
        //       PermissionGate.LogDeny(Session.User, key, reason);
        //       HideAndDisable(target);   // إخفاء + تعطيل معاً (P1-001 الخاصة بالأزرار لا تكفي وحدها)
        //       return;
        //   }
        // ---------------------------------------------------------------------
    }
}
