using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace SmartAuditERP.Class.Security
{
    /// <summary>
    /// إصلاح المرحلة الأولى للنتيجة:
    ///   P1-029 (Medium/sql-batch-parser): تقسيم سكربتات SQL على كل ظهور نصي لـ GO
    ///
    /// الكود القديم يقسم على كل occurrence للسلسلة "GO" فيكسر السكربتات التي تحوي
    /// 'GOLD' أو Goggles أو تعليقاً فيه GO. هذا الفاصل يعترف فقط بسطر GO حقيقي:
    /// بداية سطر + فراغات اختيارية + GO + عدد تكرار اختياري + فراغات + نهاية السطر.
    ///
    /// حد معروف وموثق: GO داخل تعليق كتلي /* ... */ على سطر مستقل سيُعد فاصلاً
    /// (معالجة التعليقات تحتاج lexar كامل). عند اكتشاف حالة كهذه في سكربتات
    /// الترقية الفعلية يوثق القرار في REPAIR-LOG-STAGE1 ويُعالَج السكربت يدوياً.
    /// </summary>
    public static class SqlBatchSplitter
    {
        // (?im) : تجاهل حالة الأحرف + وضع متعدد الأسطر ($ تطابق قبل \n)
        // السطر: فراغات/تابات اختيارية، GO، عدد اختياري، فراغات اختيارية، \r اختياري، نهاية سطر
        private static readonly Regex GoLine = new Regex(
            @"(?im)^[ \t]*GO[ \t]*(?:\d+)?[ \t]*\r?$",
            RegexOptions.Compiled);

        /// <summary>يعيد الدفعات غير الفارغة بترتيبها، جاهزة للتنفيذ دفعة-دفعة.</summary>
        public static List<string> Split(string script)
        {
            var batches = new List<string>();
            if (string.IsNullOrEmpty(script)) return batches;

            MatchCollection matches = GoLine.Matches(script);
            int start = 0;
            foreach (Match m in matches)
            {
                AddIfNonEmpty(batches, script.Substring(start, m.Index - start));
                start = m.Index + m.Length;
            }
            AddIfNonEmpty(batches, script.Substring(start));
            return batches;
        }

        private static void AddIfNonEmpty(List<string> batches, string batch)
        {
            if (!string.IsNullOrWhiteSpace(batch))
                batches.Add(batch.TrimEnd());
        }

        // ---------------------------------------------------------------------
        // نقاط الدمج (P1-029): استبدال كل:
        //   script.Split(new[]{"GO"}, ...) أو Split("GO") أو ما شابه في:
        //     Home.xaml.cs:1914-1917
        //     frmServerSetting.xaml.cs:572-573
        //     (موضعان إضافيان موثقان في evidence)
        // بـ: SqlBatchSplitter.Split(script)
        // ---------------------------------------------------------------------
    }
}
