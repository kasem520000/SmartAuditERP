namespace SmartAuditERP
{

        public class ItemIdOff
        {
                public int itemid { get; set; }

                // P5-005 fix: سياق الجلسة عند كتابة الإدخال في الطابور — الإدخال
                // يُفرَّغ فقط عندما يطابق سياق الجلسة الحالية (توافق: الإدخالات القديمة
                // بلا سياق تُعامل بسياق الجلسة الحالية).
                public string ClientCode { get; set; }

                public string BranchNo { get; set; }

                public string DataBase { get; set; }
        }
}