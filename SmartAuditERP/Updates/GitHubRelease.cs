// P1-025 fix: عقد حزمة إصدار GitHub — استبدال التحليل اليدوي للنص (IndexOf)
// بنموذج بيانات مطبوع عبر Newtonsoft.Json، مع عقد اختيار أصول صريح:
// يقبل أصلاً واحداً بامتداد .zip؛ إن تعددت الأصول يرشّح اسم update*.zip،
// وإن لم يوجد مرشح فريد يرفض بدل أخذ «أول مرفق» بأي حال.
using System.Collections.Generic;
using Newtonsoft.Json;

namespace SmartAuditERP.Updates
{
    public class GitHubRelease
    {
        [JsonProperty("tag_name")]
        public string TagName { get; set; }

        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("body")]
        public string Body { get; set; }

        [JsonProperty("published_at")]
        public string PublishedAt { get; set; }

        [JsonProperty("assets")]
        public List<GitHubAsset> Assets { get; set; } = new List<GitHubAsset>();

        /// <summary>
        /// اختيار أصل التحديث وفق العقد: .zip واحد؛ أو update*.zip عند التعدد؛
        /// يعيد null إن لم يوجد مرشح فريد (رفض صريح لا أول مرفق).
        /// </summary>
        public GitHubAsset SelectUpdateAsset()
        {
            if (Assets == null || Assets.Count == 0) return null;

            var zips = Assets.FindAll(a =>
                !string.IsNullOrEmpty(a.BrowserDownloadUrl) &&
                a.BrowserDownloadUrl.EndsWith(".zip",
                    System.StringComparison.OrdinalIgnoreCase));

            if (zips.Count == 0) return null;
            if (zips.Count == 1) return zips[0];

            // تعدد: رشّح باسم update*.zip — إن لم ينحسم إلى واحد فرفض
            var named = zips.FindAll(a =>
                !string.IsNullOrEmpty(a.Name) &&
                a.Name.StartsWith("update",
                    System.StringComparison.OrdinalIgnoreCase));

            if (named.Count == 1) return named[0];
            return null;
        }
    }

    public class GitHubAsset
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("size")]
        public long Size { get; set; }

        [JsonProperty("browser_download_url")]
        public string BrowserDownloadUrl { get; set; }
    }
}
