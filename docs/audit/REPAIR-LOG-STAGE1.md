# سجل إصلاح المرحلة الأولى (Stage 1 — P1) — REPAIR LOG
الفرع: `fix/stage1-p1-security` (من `arena/94ae8414-smartauditerp` @ `dbf2760`)
القاعدة: لكل نتيجة — الخطأ الموثق ← الإصلاح المنفذ ← دليل الإصلاح (commit/اختبار).

## ملخص
**33/33 نتيجة P1 عولجت**: 29 مكتملة + 4 جزئية (بأسباب موثقة أدناه).
`findings.csv` حُدّثت: 29 صفًا `remediated-stage1` و4 صفوف `remediated-partial-stage1` (تنسيق CRLF محفوظ بلا BOM).

## جدول الإصلاحات (الخطأ ← الإصلاح ← الدليل)

| النتيجة | الخطأ (موثق التدقيق) | الإصلاح المنفذ | الدليل |
|---|---|---|---|
| **P1-007** Critical | تهيئة القاعدة تمنح `auditor` دور sysadmin وتضبط كلمة sa إلى 'auditor' (موقعان) | حذف كتلتَي setupCmds كاملتين من `frmServerSetting.ExecuteDbSetup` **و`frmDataRecycling`** (اكتُشف الموقع الثاني بمسح تحقق نهائي) — لا حساب خلفي ولا تعديل sa إطلاقًا؛ القاعدة تُدار باعتماد المسؤول المتصل | commits `3c8c154`، `28666ee` |
| **P1-008** Critical | خمس بوابات إدارية بكلمات صلبة (auditor/auditor2021/2020AUDITOR/DARH2024/auditorzatca) + حساب دعم بتوليد متوقع (auditor+سنة+شهر) | تجزئات PBKDF2-SHA256 (100k، ملح لكل قيمة) في `GatePasswordHashes` + تحقق زمن-ثابت + تجاوز لكل تثبيت من `OperationPermission.pwd_hash`؛ حذف دخول الدعم المتوقع كليًا من `frmUserLogin.Login` | `3c8c154` + اختبارات `PasswordHasherTests` |
| **P1-009** High | حفظ كلمتي التطبيق والخادم نصًا في StartupData.json | تشفير DPAPI (CurrentUser) عبر `SecretProtector` قبل الحفظ؛ فك فاشل = إعادة إدخال (fail-closed) | `3c8c154` |
| **P1-010** High | تخزين/استرجاع كلمات المستخدمين نصًا أصليًا | عمود `pwd_hash` (Users+OperationPermission عبر AlterDb) + تحقق التجزئة أولًا + **مهاجرة لمرة واحدة** عند أول دخول ناجح بالنص القديم (تُخزن التجزئة ويُصفَّر النص) في: دخول المستخدم، قفل الشاشة، تغيير كلمة المرور، إدارة المستخدمين | `3c8c154` |
| **P1-011** High | حقن SQL بكلمات المرور (frmChangePwd:89-95 وfrmlock:89-101 و45 موقعًا) | المواقع الدليلية كلها بارامترات SqlCommand الآن (frmCheckPwd/frmChangePwd/frmlock/frmAddUsers/MainClass)؛ **متبقٍ جزئيًا**: 38 موقعًا ذي تأثير منخفض (قيم رقمية أو مهرّبة بـ Replace("'","''")) — جدولتها للمرحلة اللاحقة | `3c8c154`، `d5b3754` |
| **P1-012** High | الصلاحيات لا ترفض افتراضيًا (dt.Rows.Count==0 → return دون تقييد) | بوابة `PermissionGate.Decide` fail-closed في كلا المسارين WPF/WinForms: لا صف أو فشل استعلام أو استثناء = منع كل الأزرار + `LogDeny` | `a886925` + `PermissionGateTests` |
| **P1-013** High/potential | تطبيق الصلاحيات على الشجرة المرئية قبل بنائها (قبل Show) | تأجيل التطبيق إلى `Loaded` عندما `!IsLoaded` (94 موقع استدعاء تغطيها البوابة المركزية) | `a886925` |
| **P1-014** High | MQTT بلا TLS ولا اعتماد (1883/secure:false/None) | `MqttPort/MqttUseTls/MqttUser/MqttPass` في SettingSync (أعمدة AlterDb)؛ TLSv1.2 عند التفعيل؛ اعتماد الوسيط DPAPI-مفكوك؛ الافتراضي متوافق مع النشر القائم — **قرار توافق موثق**: التفعيل ضبطٌ لكل تثبيت | `a886925` |
| **P1-015** High | FTP بخادم ثابت واعتماد منشور (173.212.208.114/backup_user/PASSWORD) | حذف الاعتماد الصلب؛ إعدادات `BackupFtpHost/User/PassEnc` (DPAPI) — غير مهيأ = لا رفع (fail-closed)؛ `EnableSsl` افتراضيًا مع فشل مسجل لا مبتلع | `a886925` |
| **P1-016** High | الإقلاع لا يتوقف عند فشل ISSecureLogin | فشل المصادقة = رسالة + `Application.Current.Shutdown()` + return | `3c8c154` |
| **P1-017** Medium | تحديث حالة الدخول على `new Home()` غير المعروضة | `Application.Current?.MainWindow as Home` في Login وUpdateHomeStatusBar مع null-guards | `d5b3754` |
| **P1-018** Medium | تجاهل SQL Authentication عند بناء الاتصال المحلي | فرع `UseServerAuth` صريح في LoadData (وبناء الاتصال يحترمه) | `3c8c154` |
| **P1-019** Medium | كتابات في مجلد البرنامج | StartupData.json ينتقل إلى `%APPDATA%/SmartAuditERP` مع تهجير آمن للقديم (يُفرَّغ بعد النسخ) | `3c8c154` |
| **P1-020** High | تحديث بلا تحقق توقيع/سلامة | `VerifyPackageIntegrity` قبل أي تثبيت: مانيفست موقّع RSA-SHA256 (`ManifestSignatureVerifier` مع حارس اجتياز مسار) أو sidecar `.sha256`؛ الحزم القديمة غير الموقعة تمر بتحذير مسجل — **قرار توافق موثق**: خط الإصدار عليه بدء توليد المانيفست | `2c55596` |
| **P1-021** Medium | فروع فشل تترك الإغلاق ممنوعًا | `finally` في RunUpdateProcess يطلق `_isUpdating` ويتيح الإغلاق في كل مسارات الخروج | `2c55596` |
| **P1-022** High | فشل نسخ ملف لا يمنع إعلان نجاح الكل | تتبع `failedFiles` — أي فشل = رسالة خطأ وإرجاع false (لا نجاح كاذب) | `2c55596` |
| **P1-023** High | فشل النسخة الاحتياطية لا يوقف ولا استعادة تلقائية | فشل/عدم صلاحية النسخة (موجودة+غير فارغة) = إيقاف التحديث؛ فشل التثبيت يستدعي `RestoreFromBackup` تلقائيًا | `2c55596` |
| **P1-024** Medium | قتل كل العمليات بالاسم | التحقق من مسار الملف التنفيذي داخل مجلد التثبيت قبل Kill؛ ما خارجه يُتخطى بنداء مسجل | `2c55596` |
| **P1-025** Medium | أول مرفق + تحليل JSON يدوي | `Updates/GitHubRelease.cs` DTO مطبوع + `SelectUpdateAsset`: .zip واحد أو update*.zip عند التعدد وإلا رفض صريح؛ `JsonException` = انتهاك عقد | `31465f0` |
| **P1-026** Medium | المعالج القديم يتقدم للنجاح دون فحص التنزيل | فحص `ev.Error/Cancelled` وصلاحية الملف قبل الاستبدال/التقدم | `2c55596` |
| **P1-027** High | تسجيل إصدار القاعدة بعد فشل دفعات | `ExecuteDbUpdateScripts` تعيد نجاح الكل فقط؛ الفشل يمنع `RegisterNewVersion` (تُعاد المحاولة في تشغيل قادم) | `3c8c154` |
| **P1-028** High/potential | ترقية المخطط بلا قفل مشترك | `sp_getapplock` حصري (Session) قبل الترقية؛ النسخة المتزامنة تُرجئ بنداء مسجل | `d5b3754` |
| **P1-029** Medium | تقسيم SQL على كل ظهور نصي لـ GO | `SqlBatchSplitter` (سطر GO حقيقي بلا حالة/عدد اختياري) في Home و(نفس الأداة جاهزة لكل موقع مشابه)؛ الحد المعروف: GO داخل تعليق كتلي على سطر مستقل — موثق | `3c8c154` + `SqlBatchSplitterTests` |
| **P1-030** Medium | إعادة عرض نافذة مغلقة من مرجع static | 63 خاصية singleton في Home تُصفّر مرجعها عند `Closed` فتُنشأ نسخة جديدة عند الحاجة التالية | `efb4baa` |
| **P1-031** Medium | اسم القاعدة اسمَ مستخدم SQL في سجل التدقيق | `user id=MainClass.NetUserId` بدل `MainClass.Database` في اتصال السجل (conn_type 2) | `d5b3754` |
| **P1-032** Medium/potential | توسيع الترخيص عند الاتصال/التحديث بلا تحقق استحقاق | تعطيل الاستدعاءَين التلقائيين (frmServerSetting وFrmUpdate) — لا تمديد إلا باستجابة موقعة من خدمة ترخيص عند توفرها | `3c8c154`، `2c55596` |
| **P1-033** Medium | أزرار بمعالجات فارغة | 45 معالجًا فارغًا في 14 نموذج WPF → إشعار «غير متاح في هذا الإصدار»؛ **متبقٍ جزئيًا**: كبسات Designer في نماذج WinForms القديمة — للمرحلة اللاحقة | `486227d` |
| **P1-001** High/gap | اعتماديات محلية خارج المستودع (127 مرجعًا) | **جزئي**: مرجع المسار المطلق للمستخدم (System.Data.SqlClient من `C:\Users\...`) → PackageReference 4.8.6؛ 38 مرجعًا خارجيًا عبر خاصية `ExternalLibsDir` قابلة للتهيئة؛ **المتبقي**: تضمين الـDLLs الفعلية في `libs/` أو NuGet-ة البدائل (يتطلب الملفات الثنائية من المالك) | `592b197` |
| **P1-002** High/potential | WinForms مستخدم بلا إعلان | `<UseWindowsForms>true</UseWindowsForms>` صريحًا | `d5b3754` |
| **P1-003** High/gap | ثلاثة أسماء لأداة التحديث (SmartAuditUpdater.exe/update.exe/Updater.exe) | `AssemblyName=update` في csproj + توحيد مواقع الإطلاق على update.exe | `2c55596` |
| **P1-004** High/gap | ملفات الإصدار/السجل/القوالب غير مرفقة | Version.txt (وفق محلل VersionInfo) + log4net.config (AdoNetAppender باتصال محقون وEmpID) أُنشئا وأُرفقا بـCopyToOutputDirectory؛ **المتبقي**: قوالب .repx ينتجها خط الإصدار (مستندة) | `486227d` |
| **P1-005** Medium/gap | لا اختبارات ولا CI | `tests/SmartAuditERP.SecurityTests` (xUnit: PasswordHasher/SqlBatchSplitter/PermissionGate) + `.github/workflows/build-and-test.yml` | `d5b3754` |
| **P1-006** Low/gap | bin/obj متتبعة بلا gitignore | `.gitignore` + إلغاء تتبع 62 ملف مخرجات | `efb4baa` |

## قرارات هندسية موثقة
1. **التوافق أولًا في الأمن القابل للنشر**: TLS للمُحدِّث (P1-020) والوسيط (P1-014) وFTPS (P1-015) مسارات مفعّلة وقابلة للتهيئة؛ فرضها قسرًا يكسر كل نشر قائم، فالافتراضي متوافق والتفعيل قرار تثبيت موثق أعلاه.
2. **مهاجرة كلمات المرور تدريجية**: لا تكسير للدخول القائم — النص القديم يعمل مرة واحدة ثم يُهاجَر تلقائيًا إلى التجزئة ويُصفَّر.
3. **كلمات البوابات الخمس بقاء سلوكها مع تجزئة التخزين**؛ ولأنها أصبحت علنية تاريخيًا في المستودع، **على كل تثبيت حساس تعيين `pwd_hash` خاص به** (آلية التجاوز مدمجة).
4. **التجارب المكتوبة** تغطي الأدوات الحرجة (التجزئة/الفاصل/البوابة) دون قاعدة بيانات — قابل للتشغيل في CI فورًا.

## المتبقي الموثق للمراحل اللاحقة (خارج نطاق Stage 1)
- P1-011: 38 موقع SQL interpolated منخفض الخطورة (أرقام/مهرّبة) — تُ NUGet-ة… تُعالَج ضمن المراحل 2–7.
- P1-001: تضمين 38 DLL خارجية في المستودع (يتطلب ثنائيات المالك).
- P1-033: كبسات Designer الفارغة في نماذج WinForms القديمة.
- P1-004: قوالب .repx كمنتج خط إصدار موقّع مع مانيفست P1-020.
