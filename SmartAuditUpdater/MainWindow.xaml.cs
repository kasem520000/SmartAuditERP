using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace SmartAuditUpdater
{
    public partial class MainWindow : Window
    {
        #region ══════════════════ Fields ══════════════════

        private string _downloadUrl = "";
        private string _newVersion = "";
        private string _oldVersion = "";
        private string _appFolder = "";
        private string _tempFolder = "";
        private string _backupFolder = "";
        private string _zipPath = "";

        private bool _isUpdating = true;

        // اسم ملف البرنامج الرئيسي
        private const string MainExeName = "SmartAuditERP.exe";
        private const string MainProcessName = "SmartAuditERP";

        #endregion

        #region ══════════════════ Constructor ══════════════════

        public MainWindow()
        {
            InitializeComponent();
            Loaded += MainWindow_Loaded;
        }

        #endregion

        #region ══════════════════ Load ══════════════════

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            // ═══ قراءة Arguments ═══
            string[] args = Environment.GetCommandLineArgs();

            if (args.Length < 4)
            {
                AddLog("❌ خطأ: لم يتم تمرير معلومات التحديث!");
                AddLog("الاستخدام:");
                AddLog("update.exe \"رابط_التحميل\" \"الإصدار_الجديد\" \"الإصدار_القديم\"");
                SetError("❌ بيانات غير كافية");
                EnableClose(false);
                return;
            }

            _downloadUrl = args[1];
            _newVersion = args[2];
            _oldVersion = args[3];
            _appFolder = AppDomain.CurrentDomain.BaseDirectory;
            _tempFolder = Path.Combine(_appFolder, "UpdateTemp");
            _backupFolder = Path.Combine(_appFolder, "Backups");

            AddLog("═══════════════════════════════════");
            AddLog("     بدء عملية التحديث             ");
            AddLog("═══════════════════════════════════");
            AddLog($"الإصدار القديم : {_oldVersion}");
            AddLog($"الإصدار الجديد : {_newVersion}");
            AddLog($"مجلد البرنامج  : {_appFolder}");
            AddLog("");

            // ═══ تشغيل عملية التحديث ═══
            Task.Run(() => RunUpdateProcess());
        }

        #endregion

        #region ══════════════════ Update Process ══════════════════

        private async Task RunUpdateProcess()
        {
            try
            {
                // 1) انتظار إغلاق البرنامج الرئيسي
                await WaitForMainAppToClose();

                // 2) تحميل الملف
                bool downloaded = await DownloadUpdate();
                if (!downloaded) return;

                // 3) P1-020 fix: تحقق سلامة/توقيع الحزمة قبل أي تثبيت
                bool verified = await VerifyPackageIntegrity();
                if (!verified) return;

                // 4) نسخ احتياطي — P1-023 fix: فشله يوقف التحديث
                bool backedUp = await BackupOldFiles();
                if (!backedUp) return;

                // 5) تثبيت التحديث
                bool installed = await InstallUpdate();
                if (!installed)
                {
                    // P1-023 fix: استعادة تلقائية من النسخة الاحتياطية عند فشل التثبيت
                    await RestoreFromBackup();
                    return;
                }

                // 6) تنظيف
                await CleanUp();

                // 7) اكتمل التحديث
                Dispatcher.Invoke(() =>
                {
                    SetSuccess();
                    _isUpdating = false;
                    EnableClose(true);
                });
            }
            catch (Exception ex)
            {
                Dispatcher.Invoke(() =>
                {
                    AddLog($"❌ خطأ عام: {ex.Message}");
                    SetError("❌ فشل التحديث!");
                    _isUpdating = false;
                    EnableClose(false);
                });
            }
            finally
            {
                // P1-021 fix: كل مسارات الخروج تطلق الإغلاق — لا يبقى الإغلاق ممنوعاً أبداً
                Dispatcher.Invoke(() =>
                {
                    _isUpdating = false;
                    if (!btnClose.IsEnabled)
                        EnableClose(false);
                });
            }
        }

        #endregion

        #region ══════════════════ Step 0: Wait ══════════════════

        private Task WaitForMainAppToClose()
        {
            return Task.Run(() =>
            {
                UpdateStep("⏳ انتظار إغلاق البرنامج الرئيسي...");
                AddLog($"البحث عن عملية: {MainProcessName}");

                int waited = 0;

                while (waited < 30)
                {
                    var procs = Process.GetProcessesByName(MainProcessName);
                    if (procs.Length == 0)
                    {
                        AddLog("✅ البرنامج الرئيسي مغلق");
                        break;
                    }

                    Thread.Sleep(1000);
                    waited++;

                    Dispatcher.Invoke(() =>
                        txtDetails.Text = $"انتظار إغلاق البرنامج... {waited} ثانية");
                }

                // إغلاق إجباري إذا لزم — P1-024 fix: لا يُقتل إلا ما كان فعلاً من
                // مجلد هذا التثبيت (تحقق مسار الملف التنفيذي)، لا كل عملية بالاسم.
                var remaining = Process.GetProcessesByName(MainProcessName);
                if (remaining.Length > 0)
                {
                    AddLog("⚠️ محاولة إغلاق البرنامج إجبارياً...");
                    foreach (var p in remaining)
                    {
                        try
                        {
                            string procPath = null;
                            try { procPath = p.MainModule?.FileName; }
                            catch { /* وصول مرفوض = ليس ملفنا بأمان */ }

                            if (procPath == null ||
                                !procPath.StartsWith(_appFolder,
                                    StringComparison.OrdinalIgnoreCase))
                            {
                                AddLog($"  ↩️ تخطي عملية خارج مجلد التثبيت: {p.Id}");
                                continue;
                            }

                            p.Kill();
                            p.WaitForExit(5000);
                        }
                        catch { }
                    }
                    AddLog("✅ تم إغلاق البرنامج إجبارياً");
                }

                Thread.Sleep(1000);
                Dispatcher.Invoke(() => txtDetails.Text = "");
            });
        }

        #endregion

        #region ══════════════════ Step 1: Download ══════════════════

        private Task<bool> DownloadUpdate()
        {
            var tcs = new TaskCompletionSource<bool>();

            Dispatcher.Invoke(() =>
            {
                UpdateStep("📥 الخطوة 1: تحميل ملف التحديث...");
                SetProgress(0);
            });

            AddLog($"رابط التحميل: {_downloadUrl}");

            try
            {
                // تجهيز المجلد المؤقت
                if (Directory.Exists(_tempFolder))
                    Directory.Delete(_tempFolder, true);
                Directory.CreateDirectory(_tempFolder);

                _zipPath = Path.Combine(_tempFolder, "update.zip");

                var client = new WebClient();

                client.DownloadProgressChanged += (s, e) =>
                {
                    Dispatcher.Invoke(() =>
                    {
                        SetProgress(e.ProgressPercentage);

                        double receivedMb =
                            e.BytesReceived / 1024.0 / 1024.0;
                        double totalMb =
                            e.TotalBytesToReceive / 1024.0 / 1024.0;

                        txtStatus.Text =
                            $"تم تحميل {receivedMb:F2} MB " +
                            $"من {totalMb:F2} MB";
                    });
                };

                client.DownloadFileCompleted += (s, e) =>
                {
                    if (e.Error != null)
                    {
                        AddLog($"❌ فشل التحميل: {e.Error.Message}");
                        Dispatcher.Invoke(() =>
                            SetError("❌ فشل تحميل التحديث!"));
                        tcs.SetResult(false);
                        return;
                    }

                    long fileSizeMb =
                        new FileInfo(_zipPath).Length / 1024 / 1024;
                    AddLog($"✅ تم التحميل ({fileSizeMb} MB)");
                    AddLog("");

                    tcs.SetResult(true);
                };

                client.DownloadFileAsync(new Uri(_downloadUrl), _zipPath);
            }
            catch (Exception ex)
            {
                AddLog($"❌ خطأ: {ex.Message}");
                Dispatcher.Invoke(() =>
                    SetError("❌ فشل التحديث!"));
                tcs.SetResult(false);
            }

            return tcs.Task;
        }

        #endregion

        #region ══════════════════ Step 1.5: Integrity (P1-020) ══════════════════

        /// <summary>
        /// P1-020 fix: لا تثبيت لحزمة لم تُتحقق سلامتها.
        /// الأولوية: مانيفست موقّع (RSA-SHA256 عبر ManifestSignatureVerifier) ثم ملف
        /// تجزئة جانبي update.zip.sha256. الحزم القديمة غير الموقعة تمر بتحذير مسجل
        /// (خطة التوقيع موثقة في REPAIR-LOG-STAGE1 — خط الإصدار عليه توليد المانيفست).
        /// </summary>
        private Task<bool> VerifyPackageIntegrity()
        {
            return Task.Run(() =>
            {
                UpdateStep("🔐 التحقق من سلامة الحزمة...");

                try
                {
                    // استخراج مؤقت للتحقق
                    string extractFolder = Path.Combine(_tempFolder, "extracted");
                    if (!Directory.Exists(extractFolder))
                    {
                        ZipFile.ExtractToDirectory(_zipPath, extractFolder);
                    }

                    // 1) مانيفست موقّع؟
                    string manifestPath = Path.Combine(extractFolder, "manifest.txt");
                    if (File.Exists(manifestPath))
                    {
                        bool ok = ManifestSignatureVerifier.VerifyManifest(
                            manifestPath, extractFolder);
                        if (!ok)
                        {
                            AddLog("❌ فشل تحقق توقيع/تجزئة المانيفست — رفض الحزمة");
                            Dispatcher.Invoke(() =>
                                SetError("❌ حزمة غير موثوقة — تم رفض التحديث!"));
                            return false;
                        }
                        AddLog("✅ تحقق توقيع المانيفست وتجزئة كل ملف");
                        return true;
                    }

                    // 2) ملف تجزئة جانبي للحزمة المضغوطة؟
                    string shaPath = _zipPath + ".sha256";
                    string remoteSha = TryDownloadText(_downloadUrl + ".sha256");
                    if (!string.IsNullOrEmpty(remoteSha))
                    {
                        using (var sha = System.Security.Cryptography.SHA256.Create())
                        using (var fs = File.OpenRead(_zipPath))
                        {
                            string actual = Convert.ToHexString(
                                sha.ComputeHash(fs)).ToLowerInvariant();
                            string expected = remoteSha.Trim().ToLowerInvariant();
                            if (!string.Equals(actual, expected,
                                StringComparison.Ordinal))
                            {
                                AddLog("❌ عدم تطابق SHA256 للحزمة — رفض التحديث");
                                Dispatcher.Invoke(() =>
                                    SetError("❌ حزمة تالفة/معدلة — تم رفض التحديث!"));
                                return false;
                            }
                        }
                        AddLog("✅ تطابق SHA256 للحزمة");
                        return true;
                    }

                    // 3) حزمة قديمة بلا توقيع — توافق موثق بتحذير صريح
                    AddLog("⚠️ الحزمة بلا مانيفست موقّع ولا تجزئة — " +
                           "استمرار بضمان خادم التحميل فقط (خطة التوقيع في REPAIR-LOG)");
                    return true;
                }
                catch (Exception ex)
                {
                    AddLog($"❌ خطأ التحقق من السلامة: {ex.Message}");
                    Dispatcher.Invoke(() =>
                        SetError("❌ فشل التحقق من الحزمة!"));
                    return false;
                }
            });
        }

        private string TryDownloadText(string url)
        {
            try
            {
                using (var client = new WebClient())
                {
                    return client.DownloadString(url);
                }
            }
            catch
            {
                return null;
            }
        }

        #endregion

        #region ══════════════════ Step 2: Backup ══════════════════

        /// <summary>
        /// P1-023 fix: تعيد false عند فشل النسخ الاحتياطي — الفشل يوقف التحديث.
        /// </summary>
        private Task<bool> BackupOldFiles()
        {
            return Task.Run(() =>
            {
                UpdateStep("💾 الخطوة 2: نسخ احتياطي للملفات القديمة...");
                Dispatcher.Invoke(() => SetProgress(0));

                try
                {
                    if (!Directory.Exists(_backupFolder))
                        Directory.CreateDirectory(_backupFolder);

                    string backupZip = Path.Combine(
                        _backupFolder,
                        $"Backup_v{_oldVersion}.zip");

                    if (File.Exists(backupZip))
                        File.Delete(backupZip);

                    // استخراج مؤقت لمعرفة الملفات
                    string extractTemp =
                        Path.Combine(_tempFolder, "extracted");

                    if (!Directory.Exists(extractTemp))
                        ZipFile.ExtractToDirectory(_zipPath, extractTemp);

                    AddLog("✅ تم استخراج ملفات التحديث مؤقتاً");

                    // جمع الملفات للنسخ الاحتياطي
                    string[] updateFiles = Directory.GetFiles(
                        extractTemp, "*.*",
                        SearchOption.AllDirectories);

                    var filesToBackup = new List<string>();

                    foreach (string f in updateFiles)
                    {
                        string rel = f.Substring(
                            extractTemp.Length).TrimStart('\\', '/');
                        string existing = Path.Combine(_appFolder, rel);

                        if (File.Exists(existing))
                        {
                            filesToBackup.Add(rel);
                            AddLog($"  💾 {rel}");
                        }
                        else
                        {
                            AddLog($"  🆕 جديد: {rel}");
                        }
                    }

                    // إنشاء ملف النسخة الاحتياطية
                    if (filesToBackup.Count > 0)
                    {
                        using (var zip = ZipFile.Open(
                            backupZip, ZipArchiveMode.Create))
                        {
                            for (int i = 0; i < filesToBackup.Count; i++)
                            {
                                string full = Path.Combine(
                                    _appFolder, filesToBackup[i]);

                                if (File.Exists(full))
                                    zip.CreateEntryFromFile(
                                        full, filesToBackup[i]);

                                int pct = (i + 1) * 100
                                          / filesToBackup.Count;
                                Dispatcher.Invoke(() => SetProgress(pct));
                            }
                        }

                        // P1-023 fix: تحقق صلاحية النسخة (موجودة + غير فارغة) قبل السماح بالتحديث
                        var backupInfo = new FileInfo(backupZip);
                        if (!backupInfo.Exists || backupInfo.Length == 0)
                        {
                            AddLog("❌ النسخة الاحتياطية غير صالحة — إيقاف التحديث");
                            Dispatcher.Invoke(() =>
                                SetError("❌ فشل النسخ الاحتياطي — تم إيقاف التحديث!"));
                            return false;
                        }

                        AddLog($"✅ نسخة احتياطية: " +
                               $"{filesToBackup.Count} ملف");
                    }
                    else
                    {
                        AddLog("ℹ️ لا توجد ملفات تحتاج نسخ احتياطي");
                    }

                    AddLog("");
                    return true;
                }
                catch (Exception ex)
                {
                    // P1-023 fix: لا «متابعة رغم ذلك» — فشل النسخ يوقف التحديث
                    AddLog($"❌ فشل النسخ الاحتياطي: {ex.Message} — إيقاف التحديث");
                    Dispatcher.Invoke(() =>
                        SetError("❌ فشل النسخ الاحتياطي — تم إيقاف التحديث!"));
                    return false;
                }
            });
        }

        #endregion

        #region ══════════════════ Step 3: Install ══════════════════

        private Task<bool> InstallUpdate()
        {
            return Task.Run(() =>
            {
                UpdateStep("📦 الخطوة 3: تثبيت ملفات التحديث...");
                Dispatcher.Invoke(() => SetProgress(0));

                try
                {
                    string extractFolder =
                        Path.Combine(_tempFolder, "extracted");

                    string[] files = Directory.GetFiles(
                        extractFolder, "*.*",
                        SearchOption.AllDirectories);

                    AddLog($"عدد الملفات: {files.Length}");

                    // P1-022 fix: تتبع الفشل — أي ملف فشل نسخه يمنع إعلان النجاح
                    var failedFiles = new List<string>();

                    for (int i = 0; i < files.Length; i++)
                    {
                        string src = files[i];
                        string rel = src.Substring(
                            extractFolder.Length).TrimStart('\\', '/');

                        // المانيفست ليس ملف تطبيق — لا يُثبت في مجلد البرنامج
                        if (rel.Equals("manifest.txt",
                            StringComparison.OrdinalIgnoreCase))
                            continue;

                        string dest = Path.Combine(_appFolder, rel);

                        // إنشاء المجلدات
                        string destDir = Path.GetDirectoryName(dest);
                        if (!Directory.Exists(destDir))
                            Directory.CreateDirectory(destDir);

                        // نسخ مع إعادة المحاولة
                        bool copied = false;
                        int retries = 0;

                        while (!copied && retries < 5)
                        {
                            try
                            {
                                File.Copy(src, dest, overwrite: true);
                                copied = true;
                                AddLog($"  ✅ {rel}");
                            }
                            catch (IOException)
                            {
                                retries++;
                                AddLog($"  ⏳ مقفل، محاولة {retries}/5: {rel}");
                                Thread.Sleep(2000);
                            }
                        }

                        if (!copied)
                        {
                            // P1-022 fix: لا نجاح كاذب — الفشل يُسجل ويُمنع إعلان النجاح
                            failedFiles.Add(rel);
                            AddLog($"  ❌ تعذر نسخ: {rel}");
                        }

                        int pct = (i + 1) * 100 / files.Length;
                        Dispatcher.Invoke(() => SetProgress(pct));
                    }

                    if (failedFiles.Count > 0)
                    {
                        AddLog($"❌ فشل تثبيت {failedFiles.Count} ملف — " +
                               "لا يُعلن نجاح التحديث");
                        Dispatcher.Invoke(() =>
                            SetError($"❌ فشل تثبيت {failedFiles.Count} ملف!"));
                        return false;
                    }

                    AddLog("");
                    AddLog("✅ تم تثبيت جميع الملفات بنجاح!");
                    return true;
                }
                catch (Exception ex)
                {
                    AddLog($"❌ خطأ في التثبيت: {ex.Message}");
                    Dispatcher.Invoke(() =>
                        SetError("❌ فشل التثبيت!"));
                    return false;
                }
            });
        }

        #endregion

        #region ══════════════════ Step 3.5: Restore (P1-023) ══════════════════

        /// <summary>
        /// P1-023 fix: استعادة تلقائية من النسخة الاحتياطية عند فشل التثبيت.
        /// </summary>
        private Task RestoreFromBackup()
        {
            return Task.Run(() =>
            {
                try
                {
                    UpdateStep("♻️ استعادة الملفات من النسخة الاحتياطية...");

                    string backupZip = Path.Combine(
                        _backupFolder,
                        $"Backup_v{_oldVersion}.zip");

                    if (!File.Exists(backupZip))
                    {
                        AddLog("⚠️ لا نسخة احتياطية للاستعادة");
                        return;
                    }

                    using (var zip = ZipFile.OpenRead(backupZip))
                    {
                        foreach (var entry in zip.Entries)
                        {
                            if (string.IsNullOrEmpty(entry.Name))
                                continue; // مجلد

                            string dest = Path.Combine(_appFolder, entry.FullName);
                            string destDir = Path.GetDirectoryName(dest);
                            if (!Directory.Exists(destDir))
                                Directory.CreateDirectory(destDir);

                            entry.ExtractToFile(dest, overwrite: true);
                            AddLog($"  ♻️ {entry.FullName}");
                        }
                    }

                    AddLog("✅ تمت الاستعادة إلى الإصدار السابق");
                }
                catch (Exception ex)
                {
                    AddLog($"❌ فشل الاستعادة: {ex.Message} — " +
                           $"النسخة الاحتياطية متاحة يدوياً في {_backupFolder}");
                }
            });
        }

        #endregion

        #region ══════════════════ Step 4: Cleanup ══════════════════

        private Task CleanUp()
        {
            return Task.Run(() =>
            {
                UpdateStep("🧹 الخطوة 4: تنظيف الملفات المؤقتة...");
                Dispatcher.Invoke(() => SetProgress(50));

                try
                {
                    if (Directory.Exists(_tempFolder))
                    {
                        Directory.Delete(_tempFolder, true);
                        AddLog("✅ تم حذف المجلد المؤقت");
                    }

                    Dispatcher.Invoke(() => SetProgress(100));

                    AddLog("");
                    AddLog("═══════════════════════════════════");
                    AddLog($"✅ تم التحديث إلى الإصدار {_newVersion}");
                    AddLog("═══════════════════════════════════");
                }
                catch (Exception ex)
                {
                    AddLog($"⚠️ تحذير في التنظيف: {ex.Message}");
                }
            });
        }

        #endregion

        #region ══════════════════ Button Events ══════════════════

        private void BtnClose_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                string mainExe = Path.Combine(_appFolder, MainExeName);
                if (File.Exists(mainExe))
                {
                    Process.Start(new ProcessStartInfo(mainExe)
                    {
                        UseShellExecute = true
                    });
                }
            }
            catch { }

            Application.Current.Shutdown();
        }

        private void Window_Closing(object sender,
            System.ComponentModel.CancelEventArgs e)
        {
            if (_isUpdating)
            {
                e.Cancel = true;
                MessageBox.Show(
                    "لا يمكن إغلاق النافذة أثناء التحديث!",
                    "تنبيه",
                    MessageBoxButton.OK,
                    MessageBoxImage.Warning);
            }
        }

        #endregion

        #region ══════════════════ UI Helpers ══════════════════

        private void UpdateStep(string stepText)
        {
            Dispatcher.Invoke(() =>
            {
                txtStep.Text = stepText;
            });
            AddLog(stepText);
        }

        private void AddLog(string text)
        {
            Dispatcher.Invoke(() =>
            {
                string time = DateTime.Now.ToString("HH:mm:ss");
                txtLog.Text += $"{time}  {text}\n";
                logScroll.ScrollToEnd();
            });
        }

        private void SetProgress(int value)
        {
            prgBar.Value = Math.Max(0, Math.Min(100, value));
            txtPercent.Text = $"{prgBar.Value}%";
        }

        private void EnableClose(bool launch)
        {
            btnClose.IsEnabled = true;

            if (launch)
            {
                btnClose.Content = "🚀 إغلاق وتشغيل البرنامج";
            }
            else
            {
                btnClose.Content = "❌ إغلاق";

                // تغيير لون الزر للأحمر
                btnClose.Template = null;
                btnClose.Background =
                    new SolidColorBrush(Color.FromRgb(0xB9, 0x2F, 0x2F));
                btnClose.Foreground = Brushes.White;
            }
        }

        private void SetSuccess()
        {
            txtTitle.Text = "✅ اكتمل التحديث بنجاح!";
            txtSubTitle.Text = $"تم التحديث إلى الإصدار {_newVersion}";
            txtHeaderIcon.Text = "✅";
            txtStep.Text = $"✅ تم تثبيت الإصدار {_newVersion} بنجاح";

            // تغيير لون الهيدر للأخضر
            var header = (Border)((Grid)Content).Children[0];
            header.Background = new LinearGradientBrush(
                Color.FromRgb(0x2C, 0xC3, 0x6B),
                Color.FromRgb(0x1B, 0x8E, 0x4A),
                new System.Windows.Point(0, 0),
                new System.Windows.Point(1, 0));
        }

        private void SetError(string message)
        {
            txtTitle.Text = "❌ فشل التحديث";
            txtSubTitle.Text = message;
            txtHeaderIcon.Text = "❌";
            txtStep.Text = message;

            var header = (Border)((Grid)Content).Children[0];
            header.Background = new LinearGradientBrush(
                Color.FromRgb(0xE3, 0x56, 0x56),
                Color.FromRgb(0xB9, 0x2F, 0x2F),
                new System.Windows.Point(0, 0),
                new System.Windows.Point(1, 0));
        }

        #endregion
    }
}