using System;

namespace SmartAuditERP
{
    public class AccountingPeriod
    {
        public int PeriodID { get; set; }
        public string PeriodName { get; set; }
        public DateTime StartDate { get; set; }
        public DateTime EndDate { get; set; }
        public bool IsActive { get; set; }
        public bool IsClosed { get; set; }
        public string ClosedBy { get; set; }
        public DateTime? ClosedDate { get; set; }

        // P3-018 fix: سجل إعادة الفتح — من أعاد الفتح ومتى وكم مرة
        // (الأعمدة تُنشأ في AlterDb؛ القيم القديمة null/0)
        public string ReopenedBy { get; set; }
        public DateTime? ReopenedDate { get; set; }
        public int ReopenCount { get; set; }

        public string Notes { get; set; }
        public DateTime CreatedDate { get; set; }
    }
}