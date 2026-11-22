# سجل الإصلاحات المنفذة — فرع fix/94ae8414-security-remediation

**التاريخ:** 2026-02-27 · **الأساس:** `arena/94ae8414-smartauditerp`
**الحجم:** 36 ملفاً (35 معدلاً + ملف جديد) — 1167 إدراجاً / 646 حذفاً
**منهجية التوثيق:** كل إصلاح موسوم في الكود بتعليق `// FIX <معرف-النتيجة>` ويُفصَّل هنا بعلاقة «الخطأ ← قبل ← بعد ← الأثر السلوكي ← المخاطرة/التراجع».

> **تنبيه تشغيلي مهم:** بعد هذا الفرع، على مدير النشر إنشاء أربعة ملفات إعدادات بجوار البرنامج (قوالبها `*.example` مرفقة): `AdminGates.json` و`SyncBroker.json` و`BackupUpload.json` و`UpdateConfig.json`. البوابات الإدارية المحمية سابقاً بكلمات مثبتة **لن تعمل قبل ضبط AdminGates.json** — هذا مقصود (fail-closed) بعد إزالة الأبواب الخلفية.

---

## 1. البوابات الخلفية الحرجة (P1-007, P1-008)

### FIX P1-007 — إزالة حساب sysadmin الخلفي
- **الملفان:** `Form_WPF/frmServerSetting.xaml.cs` (ExecuteDbSetup) و`Form_WPF/frmDataRecycling.xaml.cs`
- **قبل:** بعد إنشاء القاعدة تُنفَّذ حزمة أوامر: `CREATE LOGIN [auditor] WITH PASSWORD=N'auditor'` + `ALTER SERVER ROLE [sysadmin] ADD MEMBER [auditor]` + `CREATE USER ... db_owner` + `ALTER LOGIN sa ENABLE` + `ALTER LOGIN sa WITH PASSWORD='auditor'` — كل خطأ يُبتلع (`catch {}`).
- **بعد:** حُذفت الحزمة كلياً من الموقعين؛ تبقى الدالة تنفذ أمر إنشاء القاعدة فقط، مع تعليق توثيقي بالمعرف.
- **الأثر:** أي عملية «إنشاء قاعدة/إعادة تدوير» لم تعد تفتح باباً خلفياً بصلاحيات sysadmin ولا تعبث بحساب sa. **إجراء تكميلي على القواعد القائمة (خارج الكود):** على مدير SQL Server تنفيذ `ALTER SERVER ROLE [sysadmin] DROP MEMBER [auditor];` وتغيير كلمة sa وإسقاط تسجيل auditor إن وُجد.

### FIX P1-008 — إزالة كلمات المرور الثابتة والدخول الخلفي
1. **frmCheckPwd:** أزيلت الحالات الخمس (`auditor`, `auditor2021`, `2020AUDITOR`, `DARH2024`, `auditorzatca`) واستُبدلت بحالة موحدة `ValidateConfiguredGatePassword(entered, "Gate"+CheckType)` تقرأ من `AdminGates.json`. غياب الملف/المفتاح = رسالة «غير مفعلة» ورفض (fail-closed). أيضاً عولج حقن SQL في `CheckDatabasePassword` (معاملات @pwd/@OperNo).
2. **frmUserLogin:** حُذف كتلة «دخول auditor الخاص» (كلمة `auditor+السنة+الشهر`) وحُذف تجاوز `SecureLogin ? "auditor" : txtPwd.Password` — قاعدة `Users` هي مصدر الحقيقة الوحيد الآن. غُيّر توقيع `OfflineLogin(bool,int)` إلى `OfflineLogin(int)` وحُدّث المستدعون الثلاثة.
3. **frmLogServerSettings:** بوابة `auditor/auditor` الثابتة → مفتاح `LogServer` في AdminGates.json بنفس دلالة fail-closed.
- **الأثر:** لم يعد اسم مستخدم «auditor» أو أي قيمة ثابتة في ثنائي التطبيق تفتح شيئاً.

## 2. الأسرار والتخزين (P1-009, P1-015+NEW-021, P1-014)

### FIX P1-009 — StartupData.json
- **قبل:** `Password = txtPwd.Password` و`ServerPassword = MainClass.NetPwd` يكتبان نصاً دائماً.
- **بعد:** لا تُكتب أي كلمة مرور إلا إذا كان «تذكرني» مفعلاً؛ وإلا تُكتب قيم فارغة. (السلوك الوظيفي للدخول السريع عند التذكر كما كان.)
- **ملاحظة:** الحل الجذري (عدم تخزين نص إطلاقاً) يتطلب DPAPI ويُجدول في المرحلة 2 مع التجزئة؛ هذا الإصلاح يوقف التسريب في الحالة الافتراضية.

### FIX P1-015 + NEW-021 — رفع النسخة الاحتياطية
- **قبل:** `ftp://173.212.208.114/...` + `NetworkCredential("backup_user","PASSWORD")` مثبتة، والفشل `catch {}`.
- **بعد:** `BackupUpload.json` (Host/Username/Password/EnableSsl) — لا ملف = لا رفع مع سجل Debug؛ `request.EnableSsl` يدعم FTPS؛ الفشل يُسجل.
- **الأثر:** حُذفت بيانات السيرفر من التطبيق الموزع، ويمكن تشغيل الرفع المشفر.

### FIX P1-014 — MQTT
- **قبل:** `new MqttClient(_IpServer, 1883, secure:false, ..., MqttSslProtocols.None)` + `Connect(clientId)` بلا مصادقة.
- **بعد:** قراءة `SyncBroker.json` (Port/Secure/Username/Password)؛ عند `Secure=true` يتصل TLSv1_2، وعند وجود Username يتصل بمصادقة. الافتراضي بدون ملف = السلوك القديم (توافق كامل للنشر القائم).
- **التكملة التشغيلية:** تجهيز وسيط مشفر وتفعيل الملف — موثقة في FIX-PLAN مرحلة 5.

## 3. حقن SQL (P1-011 + NEW-001..007, NEW-025, NEW-026)

كل المواقع التالية حُوّلت من بناء نصي إلى معاملات `SqlParameter` (نمط موحد: `SqlDbType` صريح):

| الملف | الموضع | ملاحظات |
|---|---|---|
| frmChangePwd | UPDATE Users SET pwd | كانت كلمة المرور داخل النص |
| frmlock | استعلاما Users (SecureCode + pwd) | — |
| frmCheckPwd | OperationPermission | — |
| frmAddUsers | 3 فحوص تكرار + فحص emp + INSERT/UPDATE Users | emp/id صارت معاملات |
| frmCustomers | Search + LoadGrid(params SqlParameter[]) | شروط LIKE بمعاملات `LIKE N'%'+@name+'%'` |
| MainClass | ApplyPermissionToForm | FormName/user_id معاملات |
| Common | CheckProiedAcc | DbAutoName معامل (مع P3-001) |
| frmPaymentVoucher | INSERT SandSD | حقل id كان نصياً (NEW-001) |
| frmClientPM | فحص تكرار + INSERT/UPDATE Accounts_Index | (NEW-002) |
| frmLicenseManagment | DELETE LicenseDevices | (NEW-003) |
| frmSuppliers | فحص + INSERT + UPDATE | (NEW-004) |
| frmJobs / frmManagement | INSERT + UPDATE | (NEW-005) |
| frmRecyclingData | فحص التكرار + استعلام dbid + تحقق DDL | (NEW-006) |
| frmDBManagment | فحص التكرار + dbid + تحقق DDL | (NEW-007) |
| Common.GetUnitID | `name=N'@Name'` → `name=@Name` | كانت لا تطابق شيئاً أبداً (NEW-025) |
| frmActs | `VALUES(N@name)` → `VALUES(@name)` | خطأ نحوي كان يفشل الإدراج (NEW-026) |

**تحقق DDL (لا معاملات في CREATE DATABASE):** اسم القاعدة يجب أن يطابق `^[A-Za-z0-9_]+$`، ومسار الملفات يجب أن يكون مطلقاً (`Path.IsPathRooted`) قبل بناء الأمر — في frmRecyclingData وfrmDBManagment.

## 4. الصلاحيات والدخول والقفل (P1-012, P1-016, P2-002, NEW-022)

### FIX P1-012 — fail-closed
- **قبل:** `if (dt.Rows.Count == 0) return;` (لا سجل = بلا قيود) والاستثناء يُبتلع.
- **بعد:** التمييز بين «نموذج غير مسجل في جدول Forms» (يبقى مفتوحاً كما كان — حفاظاً على التوافق مع النماذج غير المسيّجة) و«نموذج مسجل بلا صلاحية للمستخدم» (رفض كامل لكل الأزرار)، وفي الاستثناء يُطبق رفض كامل مع تسجيل.
- **مخاطرة موثقة:** مستخدم بلا صفوف صلاحيات على نموذج مسجل سيرى أزراره معطلة — هذا هو السلوك الأمني الصحيح.

### FIX P1-016 — إيقاف الإقلاع عند فشل المصادقة
- **بعد:** `if (!ISSecureLogin()) { Shutdown(); return; }` في Window_Loaded، وتحويل الاستدعاء الذاتي اللانهائي في ISSecureLogin إلى حلقة `while`.

### FIX P2-002 — القفل الذي يُتجاوز
- **قبل:** `@lock()` يعرض frmlock ويتجاهل نتيجته؛ ورابط «الدخول المتقدم» يخفي القفل دائماً بعد إغلاق نافذة الدخول.
- **بعد:** (1) `frmUserLogin.SuccessLogin` (حقل كان ميتاً) يُضبط true عند نجاح الدخول فقط. (2) رابط frmlock لا يخفي القفل إلا عند `SuccessLogin=true` وإلا يبقى القفل في المقدمة. (3) `@lock()` حلقة تعيد إظهار القفل حتى `Iscorrect=true`.
- **ملاحظة سلوكية:** إغلاق نافذة القفل بالأشكال/النقر لا يعود ممراً للجلسة — يجب كلمة مرور صحيحة أو دخول كامل ناجح.

### FIX NEW-022 — تعيين btnNew
- في `ApplyWinFormsIconBtnPermission` و`ApplyWinFormsBtnPermission`: `!canNew && name=="btnSave"` → `"btnNew"` (مطابقة لنسخة WPF).

## 5. المحدّث وسلسلة التوريد (P1-020, P1-022, P1-003, P1-002, P1-026 جزئي, NEW-020, NEW-023)

### SmartAuditUpdater/MainWindow.xaml.cs
1. **HTTPS فقط:** أي `_downloadUrl` لا يبدأ بـhttps يُرفض فوراً.
2. **تحقق SHA-256 (P1-020):** خطوة جديدة `VerifyUpdatePackageHashAsync` بعد التحميل: تنزيل `{url}.sha256` — إن وُجد ولم يتطابق = فشل التحديث (fail-closed)؛ إن لم يوجد = تحذير ومتابعة (حفاظ على قناة النشر الحالية حتى إتاحة البصم).
3. **P1-022:** عدّاد `failedCopies` — أي ملف فشل نسخه بعد المحاولات = فشل التثبيت ورسالة توجيه إلى Backups (لم يعد يُعلن «تم تثبيت جميع الملفات بنجاح» كذباً).
4. **NEW-023:** Mutex مسمى `SmartAuditUpdater_SingleInstance` في المشيد (نسخة ثانية تُغلق فوراً) + إعادة فحص/قتل العملية الرئيسية قبل بدء النسخ مباشرة.

### SmartAuditUpdater.csproj
- **P1-003:** `<AssemblyName>update</AssemblyName>` — المخرج يصبح `update.exe` المطابق لما يشغله `Home.xaml.cs`، مع أن MainWindow ظل يعرض تعليمات الاستخدام الصحيحة `update.exe ...`.

### FrmUpdate.xaml.cs (المحدّث القديم)
- **NEW-020:** حذف `UrlZipFile = "https://dhit.com.sa/wp-content/uploads/update.zip"`؛ يُقرأ `LegacyUpdateUrl` من `UpdateConfig.json` (https إلزامي)؛ بدون ضبط: تعطيل الخيار الأونلاين مع رسالة توجيه. **P1-026 جزئي:** فحص `ev.Error` قبل الاستبدال ورفض الروابط غير الصالحة. **P1-003:** إطلاق `update.exe` مع بديل `Updater.exe` القديم.

### SmartAuditERP.csproj
- **P1-002:** `<UseWindowsForms>true</UseWindowsForms>` صراحة.

## 6. سلامة البيانات المالية والوظيفية (P3-001, NEW-008..NEW-010)

### FIX P3-001 — CheckProiedAcc
- **قبل:** `return !(InvoiceDate > end || InvoiceDate < start) || true;` → دائماً true، و`catch { return true; }`.
- **بعد:** إزالة `|| true` (تفعيل الفترة)؛ لا صف فترة نشط = true (لا قيد فترة مضبوط)؛ **catch = false** (فشل فحص الفترة يمنع الترحيل — ضابط مالي).
- **مخاطرة موثقة:** إذا كان سجل الفترة تالفاً/غير متاح مؤقتاً فستُمنع الفواتير حتى الإصلاح — مقصود أمنياً، والفترات السليمة تعمل.

### FIX NEW-008 — فشل سكربتات إنشاء القاعدة
- في frmRecyclingData وfrmDBManagment: عدّاد `failedScripts` + رسالة «فشل N من M سكريبت» بدل النجاح المطلق. (لم يُجعل فادحاً حفاظاً على تشغيل التهيئة الجزئية القابلة للاستكمال — القرار موثق.)

### FIX NEW-009 — عرض العميل في frmOffers
- الحذف+الإدراج داخل معاملة واحدة مع Rollback ورسالة خطأ صريحة بدل `catch {}` + نجاح دائم.

### FIX NEW-010 — التحويل البنكي في frmInvSalContactDetails
- `UPDATE inv` → `UPDATE InvContratct ... WHERE branch=@branch AND InvGlobalID=@InvGlobalID` (مطابقة للعمليات الشقيقة ولجدول الشبكة الفعلي).

## 7. إصلاحات إضافية مؤكدة (NEW-011..013, NEW-016..018, NEW-024)

| المعرف | الملف | الإصلاح |
|---|---|---|
| NEW-011/017 | frmSentEinvoice + EtaService | `Uri.TryCreate` + قصر المخطط على http/https + `UseShellExecute=true` (يعمل على net8 بدل الفشل الصامت) |
| NEW-012 | GetDataAPI.cs | http → https |
| NEW-013 | frmItems | `RandomNumberGenerator.GetInt32` لتوليد الباركود |
| NEW-016 | EtaReciptService | `pos_seller.floor = "1"` بدل قيمة PostalZone |
| NEW-018 | DeviceLicenseManager | فحص الاتصال عبر `https://www.google.com/generate_204` |
| NEW-024 | DeviceLicenseManager | `ToString("yyyyMMdd", InvariantCulture)` لحافظة توقيع الترخيص |

## 8. ملفات جديدة

### `SmartAuditERP/Class/SecureConfig.cs` (جديد)
قارئ JSON خفيف (`Newtonsoft.Json.Linq`) لملفات الإعدادات الحساسة بجوار التنفيذ، يُعيد null عند أي غياب/خطأ (fail-closed). يستخدمه: frmCheckPwd، frmLogServerSettings، ConnectBroker، frmBackupRstore، FrmUpdate.

### قوالب الإعدادات `deploy/*.json.example` (جديدة)
قوالب بلا أسرار: `AdminGates.json.example`، `SyncBroker.json.example`، `BackupUpload.json.example`، `UpdateConfig.json.example` — تُنسى وتُضبط عند النشر.

## 9. توازن الأقواس والتحقق الآلي المتاح

- فحص توازن `{`/`}` لكل ملف معدل: **مطابقة كاملة** (Home.xaml.cs يحمل فارق +1 **سابقاً موجوداً في الأصل** بسبب أقواس داخل نصوص، وتعديلاتنا حافظت على الفارق نفسه).
- لا يتوفر مترجم C#/Windows في بيئة الإعداد هذه — **بوابة ما قبل الدمج:** بناء على ويندوز + اختبار الدخان (موثقة في FIX-PLAN مرحلة 1).

## 10. خريطة النتيجة → الإصلاح (جدول جامع)

| النتيجة | الحالة | الملف/المواضع |
|---|---|---|
| P1-002 | مُصلَح | SmartAuditERP.csproj |
| P1-003 | مُصلَح | SmartAuditUpdater.csproj + FrmUpdate + (Home كان صحيحاً) |
| P1-007 | مُصلَح | frmServerSetting + frmDataRecycling |
| P1-008 | مُصلَح | frmCheckPwd + frmUserLogin + frmLogServerSettings |
| P1-009 | مُصلَح (تخفيف) | frmUserLogin.SaveStartupData |
| P1-011 | مُصلَح | 16 موضعاً (القسم 3) |
| P1-012 | مُصلَح | MainClass.ApplyPermissionToForm |
| P1-014 | مُصلَح (تكويني) | ConnectBroker + SyncBroker.json |
| P1-015 | مُصلَح | frmBackupRstore + BackupUpload.json |
| P1-016 | مُصلَح | Home.Window_Loaded + ISSecureLogin |
| P1-020 | مُصلَح (تحقق مشروط بالبصمة + HTTPS) | SmartAuditUpdater |
| P1-022 | مُصلَح | SmartAuditUpdater.InstallUpdate |
| P1-026 | مُصلَح جزئياً (فحص فشل التحميل والرابط) | FrmUpdate |
| P2-002 | مُصلَح | Home.@lock + frmlock + frmUserLogin.SuccessLogin |
| P3-001 | مُصلَح | Common.CheckProiedAcc |
| NEW-001..013 | مُصلَح (عدا 014/015 مؤجلة) | انظر الأقسام 3/6/7 |
| NEW-016..018 | مُصلَح | القسم 7 |
| NEW-020..024 | مُصلَح | الأقسام 5/3/7 |
| NEW-025, NEW-026 | مُصلَح | القسم 3 |
| البقية (296 نتيجة) | `planned-phase-N` | FIX-PLAN-94ae8414.md |
