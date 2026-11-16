// Updates/VersionInfo.cs
using System;

namespace SmartAuditERP.Updates
{
    public class VersionInfo
    {
        public string Version { get; set; }
        public string VersionText { get; set; }
        public string Description { get; set; }
        public int TypeUpdates { get; set; }
        public string PublishDate { get; set; }
    }

    public enum TypeUpdate
    {
        Normal = 0,
        Critical = 1
    }
}