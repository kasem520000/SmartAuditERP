using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using Newtonsoft.Json;

namespace SmartAuditERP
{
    /// <summary>
    /// P5-004 / P5-005 fix: مساعد طابور المزامنة دون الاتصال.
    /// المشاكل القديمة:
    ///  - كتابة الطابور كانت «اقرأ الملف كله ثم أعد كتابته» بدون قفل ولا كتابة ذرّية،
    ///    فتُفقد إدخالات بسباق بين الحفظ المتزامن وتفريغ المؤقت (SendStoredItems)
    ///    أو بانقطاع أثناء إعادة الكتابة (truncate-then-write).
    ///  - ملفا الطابور (Itemid.json / InvGlobalID.json) لا يحملان سياق الجلسة
    ///    (العميل/الفرع/قاعدة البيانات) فيُفرَّغ الطابور بعد تغيير قاعدة البيانات
    ///    بنشر إدخالات تُقرأ من قاعدة بيانات أخرى.
    /// العقد الجديد:
    ///  - كل عملية قراءة/إلحاق/كتابة داخل قفل واحد على مستوى التطبيق.
    ///  - الكتابة ذرّية: ملف مؤقت ثم استبدال (File.Replace مع احتياط Copy).
    ///  - الدوال تحترم إدخالات قديمة بلا سياق (تُعامل بسياق الجلسة الحالية
    ///    للتوافق مع الملفات الموجودة قبل الترقية).
    /// </summary>
    internal static class OfflineQueue
    {
        private static readonly object FileLock = new object();

        public static readonly string ItemsQueuePath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory, "Data", "Itemid.json");

        public static readonly string InvoicesQueuePath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory, "Data", "InvGlobalID.json");

        /// <summary>هل إدخال الطابور مكتوب بسياق الجلسة الحالية؟ (الإدخال بلا سياق = قديم متوافق)</summary>
        public static bool MatchesCurrentSession(string clientCode, string branchNo, string dataBase)
        {
            if (string.IsNullOrEmpty(clientCode) && string.IsNullOrEmpty(branchNo) && string.IsNullOrEmpty(dataBase))
            {
                return true; // إدخال قديم قبل الترقية — عامل بسياق الجلسة الحالية
            }
            bool clientOk = string.IsNullOrEmpty(clientCode)
                || string.Equals(clientCode, Sync.ClientCode ?? "", StringComparison.Ordinal);
            bool branchOk = string.IsNullOrEmpty(branchNo)
                || string.Equals(branchNo, MainClass.BranchNo.ToString(), StringComparison.Ordinal);
            bool dbOk = string.IsNullOrEmpty(dataBase)
                || string.Equals(dataBase, MainClass.DataBaseAutoName ?? "", StringComparison.Ordinal);
            return clientOk && branchOk && dbOk;
        }

        public static List<T> ReadAll<T>(string path)
        {
            lock (FileLock)
            {
                return ReadAllNoLock<T>(path);
            }
        }

        /// <summary>إلحاق إدخال واحد بالطابور بشكل ذرّي ومقفول.</summary>
        public static void Append<T>(string path, T entry)
        {
            if (entry == null) return;
            lock (FileLock)
            {
                List<T> list = ReadAllNoLock<T>(path);
                list.Add(entry);
                WriteAllNoLock(path, list);
            }
        }

        public static void WriteAll<T>(string path, List<T> entries)
        {
            lock (FileLock)
            {
                WriteAllNoLock(path, entries);
            }
        }

        private static List<T> ReadAllNoLock<T>(string path)
        {
            var list = new List<T>();
            try
            {
                if (File.Exists(path))
                {
                    string json = File.ReadAllText(path, Encoding.UTF8);
                    if (!string.IsNullOrWhiteSpace(json))
                    {
                        list = JsonConvert.DeserializeObject<List<T>>(json) ?? new List<T>();
                    }
                }
            }
            catch
            {
                // ملف تالف: لا نُسقط التطبيق — نبدأ من قائمة فارغة (الملف يُعاد كتابته ذرّيًا)
                list = new List<T>();
            }
            return list;
        }

        private static void WriteAllNoLock<T>(string path, List<T> entries)
        {
            string dir = Path.GetDirectoryName(path);
            if (!string.IsNullOrEmpty(dir))
            {
                Directory.CreateDirectory(dir);
            }
            string json = JsonConvert.SerializeObject(entries, Formatting.Indented);
            string tmpPath = path + ".tmp";
            File.WriteAllText(tmpPath, json, Encoding.UTF8);
            try
            {
                if (File.Exists(path))
                {
                    File.Replace(tmpPath, path, null);
                }
                else
                {
                    File.Move(tmpPath, path);
                }
            }
            catch (PlatformNotSupportedException)
            {
                // File.Replace غير مدعوم (مثلاً FAT) — بديل آمن
                File.Copy(tmpPath, path, overwrite: true);
                try { File.Delete(tmpPath); } catch { }
            }
            catch (IOException)
            {
                File.Copy(tmpPath, path, overwrite: true);
                try { File.Delete(tmpPath); } catch { }
            }
        }
    }
}
