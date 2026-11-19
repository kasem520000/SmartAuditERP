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
                // Repair R-017 (audit findings P1-021/P1-022/P1-023, bounded part): every non-success
                // exit used to RETURN here without clearing _isUpdating or enabling close, leaving a
                // failed update window that could not be dismissed normally; and failures below were
                // swallowed into "success anyway". Route each failure through FailTerminal so the user
                // always ends on a closable, clearly-failed state - mirroring the general catch arm.
                if (!downloaded)
                {
                    FailTerminal("❌ فشل تحميل التحديث!");
                    return;
                }

                // 3) نسخ احتياطي (إلزامي قبل أي تعديل - P1-023)
                bool backedUp = await BackupOldFiles();
                if (!backedUp)
                {
                    FailTerminal("❌ فشل النسخ الاحتياطي! لن يتم تعديل الملفات.");
                    return;
                }

                // 4) تثبيت التحديث
                bool installed = await InstallUpdate();
                if (!installed)
                {
                    FailTerminal("❌ فشل تثبيت التحديث!");
                    return;
                }

                // 5) تنظيف
                await CleanUp();

                // 6) اكتمل التحديث
                Dispatcher.Invoke(() =>
                {
                    SetSuccess();
                    _isUpdating = false;
                    EnableClose(true);
                });
            }
            catch (Exception ex)
            {
                FailTerminal("❌ فشل التحديث!");
                Dispatcher.Invoke(() => AddLog($"❌ خطأ عام: {ex.Message}"));
            }
        }

        // Repair R-017 (P1-021): one terminal-failure state for every failed branch, identical in
        // spirit to the former general-catch handling: mark the error UI, stop the "updating" flag
        // so Window_Closing no longer cancels the close, and turn the close button into a plain
        // red "إغلاق". No success wording can ever reach this path.
        private void FailTerminal(string message)
        {
            Dispatcher.Invoke(() =>
            {
                SetError(message);
                _isUpdating = false;
                EnableClose(false);
            });
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

                // إغلاق إجباري إذا لزم
                var remaining = Process.GetProcessesByName(MainProcessName);
                if (remaining.Length > 0)
                {
                    AddLog("⚠️ محاولة إغلاق البرنامج إجبارياً...");
                    foreach (var p in remaining)
                    {
                        try
                        {
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

        #region ══════════════════ Step 2: Backup ══════════════════

        private Task<bool> BackupOldFiles()
        {
            // Repair R-017 (audit finding P1-023, bounded part): backup failure used to log
            // "المتابعة رغم ذلك" and the install ran anyway - updates could proceed with no
            // working way back. Report success/failure instead; RunUpdateProcess now refuses to
            // modify any file unless this step succeeded. Full staging/rollback architecture
            // remains documented as needs-input work (TRACKER backlog, P1-023 residual).
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

                    if (Directory.Exists(extractTemp))
                        Directory.Delete(extractTemp, true);

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
                    AddLog($"❌ فشل النسخ الاحتياطي: {ex.Message}");
                    AddLog("لن تتم متابعة التحديث دون نسخة احتياطية ناجحة.");
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

                    bool anyCopyFailed = false;   // R-017 / P1-022: honest install result

                    for (int i = 0; i < files.Length; i++)
                    {
                        string src = files[i];
                        string rel = src.Substring(
                            extractFolder.Length).TrimStart('\\', '/');
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

                        // Repair R-017 (audit finding P1-022): a file that still could not be
                        // copied after five attempts used to draw only a warning while the step
                        // announced "all files succeeded" and returned true - leaving a mixed set
                        // of versions behind a success message. Track the failure and fail the
                        // whole install instead; no success wording is emitted in that case.
                        bool failedThisFile = !copied;
                        if (failedThisFile)
                        {
                            anyCopyFailed = true;
                            AddLog($"  ❌ تعذر نسخ: {rel}");
                        }

                        int pct = (i + 1) * 100 / files.Length;
                        Dispatcher.Invoke(() => SetProgress(pct));
                    }

                    AddLog("");
                    if (anyCopyFailed)
                    {
                        AddLog("❌ فشل التحديث: تعذر نسخ بعض الملفات بعد المحاولات.");
                        return false;
                    }
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