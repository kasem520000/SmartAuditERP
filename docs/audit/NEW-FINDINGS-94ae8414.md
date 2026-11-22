# الأخطاء الجديدة المكتشفة — غير الموثقة سابقاً

**التاريخ:** 2026-02-27 · **الفرع المرجعي:** `arena/94ae8414-smartauditerp`
**المصدر:** تدقيق مستقل تالٍ لتدقيق الوكيل السابق (335 نتيجة في `findings.csv`) عبر وكيلي اكتشاف متوازيين (D1: مسح شامل، D2: أنظمة فرعية معمقة) + اكتشافات المدقق الرئيسي.
**قاعدة الاستبعاد:** كل مرشح جرى مطابقته مع `findings.csv` (بأسماء الملفات ونطاقات الأسطر ومواضيع النتائج) — لا تكرار مع أي نتيجة موثقة.

---

## ملخص

26 خطأً جديداً: **10 عالية، 13 متوسطة، 3 منخفضة**. المعرفات `NEW-001..NEW-026` هي المعرفات المرجعية المستخدمة في تعليقات الإصلاح (`// FIX NEW-xxx`) وفي `findings.csv` المحدّث وفي خطة الإصلاح.

## أخطاء جديدة عالية الخطورة

### NEW-001 — حقن SQL في رقم سند الصرف [عالية] [sql-injection] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmPaymentVoucher.xaml.cs:~457-463`
- **الكود:** `INSERT INTO SandSD (...) VALUES ({txtNo.Text}, @date, ...)` — الرقم من مربع النص يُدرج نصياً بينما بقية الأعمدة معاملات.
- **الأثر:** قيمة مصنوعة في حقل الرقم تنفذ SQL داخل معاملة مالية.
- **الإصلاح:** معاملة `@id` (انظر FIXES-LOG).

### NEW-002 — حقن SQL وابتلاع صامت في حسابات العملاء [عالية] [sql-injection + swallowed-failure] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmClientPM.xaml.cs:~435-439, 520-572`
- **الكود:** إدراج حساب العميل في `Accounts_Index` ببناء نصي كامل (`VALUES(N'{txtAccCode.Text}',N'{txtName.Text}',...)`) + `catch { }` يخفي أي فشل (عميل بلا حساب مالي دون تنبيه). التحديث (`UpdateExistingAccount`) بنفس النمط.
- **الإصلاح:** معاملات كاملة في الفحص/الإدراج/التحديث.

### NEW-003 — حقن SQL وخطأ غير مرئي في حفظ التراخيص [عالية] [sql-injection + silent-failure] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmLicenseManagment.xaml.cs:~425-448`
- **الكود:** `delete from LicenseDevices where DeviceID='{txtUID.Text}'` نصي، وفشل الحفظ كله يُكتب في `Console.WriteLine` فقط (غير مرئي في WPF).
- **الإصلاح:** معامل `@DeviceID` + إظهار الخطأ للمستخدم.

### NEW-004 — حقن SQL في الموردين [عالية] [sql-injection] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmSuppliers.xaml.cs:~129-158`
- **الكود:** فحص التكرار والإدراج والتحديث كلها ببناء نصي باسم المورد ورقم الضريبة.
- **الإصلاح:** معاملات كاملة.

### NEW-005 — حقن SQL في الوظائف والإدارات [متوسطة→عالية] [sql-injection] — ✅ مُصلَح
- **الملف:** `frmJobs.xaml.cs:~115,121` و`frmManagement.xaml.cs:~120,126`
- **الكود:** `insert into jobs(name) values('{txtName.Text}')` ونظيره في Managements.
- **الإصلاح:** معاملات.

### NEW-006 — حقن SQL/DDL في معالج إعادة التدوير [عالية] [sql-injection + server-administration] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmRecyclingData.xaml.cs:~205-207, 330-340`
- **الكود:** فحص التكرار يدمج `txtDbName` نصياً في استعلام على `master`، و`CREATE DATABASE` يدمج `txtPath.Text` في `FILENAME` (حقن + موضع ملفات عشوائي على السيرفر).
- **الإصلاح:** معامل SQL للاسم + تحقق `^[A-Za-z0-9_]+$` للمعرف + تحقق مسار مطلق لـFILENAME.

### NEW-007 — حقن SQL في إدارة قواعد البيانات [عالية] [sql-injection] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmDBManagment.xaml.cs:~172-175`
- **الكود:** فحص تكرار الاسم يدمج `dbDisplayName` نصياً في استعلام على `master`.
- **الإصلاح:** معامل + تحقق معرف في `CreateDatabaseOnServer`.

### NEW-008 — ابتلاع فشل سكربتات إنشاء القاعدة ثم إعلان نجاح كامل [عالية] [false-success] — ✅ مُصلَح
- **الملف:** `frmRecyclingData.xaml.cs:~233-241` و`frmDBManagment.xaml.cs:~205-239`
- **الكود:** كل سكربت Schema يُنفذ داخل `try { } catch { }` فارغ ثم `«تمت عملية إنشاء قاعدة البيانات بنجاح»`.
- **الأثر:** قاعدة ناقصة الجداول/القيود تُعلن ناجحة للمدير.
- **الإصلاح:** تتبع عدد السكربتات الفاشلة وتحذير صريح بعدد منها.

### NEW-009 — حذف وإدراج عرض العميل يُبتلع فشله ويُعرض النجاح [عالية] [swallowed-failure + no-transaction] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmOffers.xaml.cs:~413-459`
- **الكود:** عند التعديل: `delete from OfferForClient ...` ثم INSERT داخل `catch { }` فارغ؛ المستدعي يعرض حوار النجاح دائماً — فشل المنتصف يترك العرض **محذوف التفاصيل** دون علم المستخدم.
- **الإصلاح:** الحذف+الإدراج في معاملة واحدة مع Rollback ورسالة خطأ.

### NEW-010 — تحويل الدفع للبنك يعدّل الجدول الخطأ [عالية] [wrong-table] — ✅ مُصلَح
- **الملف:** `SmartAuditERP/Form_WPF/frmInvSalContactDetails.xaml.cs:~948-954`
- **الكود:** `UPDATE inv SET pay_type=2 ...` بينما الشبكة محملة من `InvContratct` وجميع العمليات الشقيقة (نقدي/آجل/تغيير عميل/شيكات) تعدّل `InvContratct`.
- **الأثر:** تحويل بنكي يفسد صفوف جدول `inv` غير ذات الصلة ويترك السجل المعروض بلا تغيير، ثم `RegenerateEntry` يعيد بناء القيد من بيانات غير متسقة.
- **الإصلاح:** `UPDATE InvContratct ... WHERE branch=@branch AND InvGlobalID=@InvGlobalID` أسوة بالشقيقات.

### NEW-011 — تنفيذ روابط غير موثوقة عبر Shell [متوسطة] [file-trust-boundary] — ✅ مُصلَح
- **الملف:** `frmSentEinvoice.xaml.cs:~177-180` و`Class/EtaService.cs:~347`
- **الكود:** `Process.Start(new ProcessStartInfo(publicUrl.Text){UseShellExecute=true})` بقيمة من الشبكة/قاعدة البيانات دون تقييد المخطط؛ وفي EtaService قيمة من استجابة ويب مباشرة.
- **الإصلاح:** `Uri.TryCreate` + قصر المخطط على http/https قبل الفتح.

### NEW-012 — نداء HTTP مكشوف ومهمَل عبر GetDataAPI [متوسطة] [transport-security] — ✅ مُصلَح
- **الملف:** `Class/GetDataAPI.cs:12` + المستدعي `frmNewProjectPM.xaml.cs:~45-49`
- **الكود:** `await new HttpClient().GetAsync("http://update.auditorerp.cloud/...")` — النداء الوحيد غير المشفر في الكود، يُستدعى مهمَلاً غير منتظر عند فتح نافذة مشروع جديد.
- **الإصلاح:** التحويل إلى https.

### NEW-013 — عشوائية غير آمنة لتوليد الباركود [منخفضة] [insecure-randomness] — ✅ مُصلَح
- **الملف:** `frmItems.xaml.cs:~1869-1876`
- **الكود:** `new Random().Next(4344, 34355353)` لباركود يُمسح في POS (قابل للتوقع والتصادم).
- **الإصلاح:** `RandomNumberGenerator.GetInt32`.

### NEW-014 — مولّدات المعرفات تفشل مفتوحاً عبر ExecuteScalarSafe [عالية] [fail-open-id-generation] — ⏳ مؤجل (خطة المرحلة 2)
- **الملف:** `Class/Common.cs:2390-2402` + مولدات `GetCustomerId/GetTreasuryId/GetEmployeeId/GetInventoryId/GetBankId` في `794-895`
- **الكود:** `catch { return 0; }` يحول أي فشل SQL إلى «المعرف حر» — عند خطأ عابر يُعاد معرف موجود أصلاً → تصادم مفاتيح أو تحديث صف خاطئ.
- **لماذا مؤجل:** يتطلب إعادة تصميم مسار توليد المعرفات واختباراً على قاعدة حقيقية.

### NEW-015 — ترميز مبلغ الدفع في Geidea بثقافة الجهاز [متوسطة] [monetary-encoding] — ⏳ مؤجل (كود كامن بلا مستدعين حالياً)
- **الملف:** `Class/Geidea.cs:~50-55`
- **الكود:** `Conversions.ToString(Payment * 100.0)` — `4.35*100 = 434.99999999999994`، وفي ar-SA قد يظهر فاصل عشري عربي يفسد الرسالة المرسلة لجهاز الدفع. (المسار الحي يستخدم UtilitiesProj.Geidea.Pay.)
- **الإصلاح الموصى به عند التفعيل:** حساب decimal + InvariantCulture.

### NEW-016 — حقل الطابق في إيصالات ETA يستلم المنطقة البريدية [منخفضة] [data-mapping] — ✅ مُصلَح
- **الملف:** `Class/EtaReciptService.cs:210-213`
- **الكود:** `pos_seller.floor = ...["PostalZone"]` (نسخ لصق من السطر السابق) — عنوان البائع المرسل لهيئة الضرائب خاطئ عند ضبط المنطقة البريدية.
- **الإصلاح:** `floor = "1"` أسوة بـEtaService.

### NEW-017 — Process.Start(string) في EtaService يفشل صامتاً على net8 [متوسطة] [silent-feature-failure] — ✅ مُصلَح (ضمن NEW-011)
- **الملف:** `Class/EtaService.cs:335-354`
- **الكود:** على net8.0-windows يعود `Process.Start(string)` بـ`UseShellExecute=false` فيرمي Win32Exception لروابط https، والcatch يبتلعه — ميزة طباعة الفاتورة الإلكترونية تموت بصمت. (عولج ضمن إصلاح NEW-011 بـUseShellExecute=true وتقييد المخطط.)

### NEW-018 — فحص الاتصال للترخيص عبر HTTP مكشوف [منخفضة] [transport-security] — ✅ مُصلَح
- **الملف:** `Class/DeviceLicenseManager.cs:149-167`
- **الكود:** `webClient.OpenRead("http://clients3.google.com/generate_204")` — يقرر مسار الترخيص أونلاين/أوفلاين عبر قناة قابلة للتزوير.
- **الإصلاح:** `https://www.google.com/generate_204`.

### NEW-019 — استيراد البصمات يجمد الواجهة ويفشل بصمت [متوسطة] [ui-freeze + silent-failure] — ⏳ مؤجل (خطة المرحلة 3)
- **الملف:** `Class/FingerPrintDevice.cs:48-120` + `Home.xaml.cs:609-612`
- **الكود:** قراءة جهاز COM + معاملة DB على خيط الواجهة كل 60 ثانية (DispatcherTimer)، بلا فحص `ISconnectedBar`، وبلا Rollback/سجل عند الخطأ.
- **لماذا مؤجل:** يتطلب نقل العمل لخيط خلفي وإعادة هيكلة دورة المؤقت.

### NEW-020 — رابط تحديث قديم مثبت على wp-content بموقع طرف ثالث [عالية] [supply-chain] — ✅ مُصلَح
- **الملف:** `Form_WPF/FrmUpdate.xaml.cs:19`
- **الكود:** `UrlZipFile = "https://dhit.com.sa/wp-content/uploads/update.zip"` — حزمة تنفيذية تُنزّل من مجلد رفع ووردبريس لموقع خارجي (بديل سهل لأي من يخترق الموقع) ثم تُفك فوق مجلد التطبيق دون أي تحقق. (تعليق الكود يظهر أن المصدر كان GitHub releases.)
- **الإصلاح:** أزيل الرابط المثبت؛ يُقرأ من `UpdateConfig.json` (LegacyUpdateUrl — https إلزامي) وعند غيابه يُعطّل التحديث الأونلاين في هذه الشاشة القديمة مع توجيه لآلية GitHub+SmartAuditUpdater الحديثة.

### NEW-021 — بيانات FTP للنسخ الاحتياطي مثبتة في الكود [عالية] [hardcoded-credentials] — ✅ مُصلَح (ضمن P1-015)
- **الملف:** `Form_WPF/frmBackupRstore.xaml.cs:697-721`
- **الكود:** `ftp://173.212.208.114/...` + `new NetworkCredential("backup_user", "PASSWORD")` — سيرفر وبيانات دخول داخل ثنائي التطبيق الموزع.
- **الإصلاح:** `BackupUpload.json` (Host/Username/Password/EnableSsl) بلا قيم افتراضية — لا رفع دون ضبط صريح.

### NEW-022 — تعطيل btnSave بشرط canNew في مسارات WinForms [منخفضة] [permissions-mapping] — ✅ مُصلَح
- **الملف:** `Class/MainClass.cs:565, 597`
- **الكود:** `if (!canNew && name == "btnSave") disable = true;` في كلا الزائدَين — خطأ نسخ من نسخة WPF الصحيحة (`btnNew`).
- **الإصلاح:** فحص `btnNew` الصحيح.

### NEW-023 — المحدّث بلا حارس تشغيل أحادي وبفحص إغلاق لمرة واحدة [متوسطة] [race-condition] — ✅ مُصلَح
- **الملف:** `SmartAuditUpdater/MainWindow.xaml.cs`
- **الكود:** لا Mutex — نسختان من update.exe تحذفان مجلد `UpdateTemp` تحت بعضهما؛ وفحص إغلاق البرنامج في الخطوة 0 فقط — إعادة تشغيل التطبيق أثناء النسخ تُنتج مزيجاً قديماً/جديداً يُعلن ناجحاً (يرتبط بـP1-022).
- **الإصلاح:** Mutex مسمى + إعادة فحص/إغلاق قبل التثبيت مباشرة.

### NEW-024 — توقيع الترخيص حساس للتقويم المحلي [متوسطة] [culture-crypto] — ✅ مُصلَح
- **الملف:** `Class/DeviceLicenseManager.cs:81`
- **الكود:** `ExpireDate.ToString("yyyyMMdd")` بثقافة الجهاز — على ar-SA (أم القرى) أو th-TH يختلف النص الموقّع فتُرفض تراخيص صحيحة ويُدفع المستخدم للنسخة التجريبية قسرياً.
- **الإصلاح:** `ToString("yyyyMMdd", CultureInfo.InvariantCulture)`.

### NEW-025 — معامل داخل علامات اقتباس يجعل GetUnitID تعيد -1 دائماً [متوسطة] [broken-query] — ✅ مُصلَح
- **الملف:** `Class/Common.cs:~276`
- **الكود:** `"select id from units where name=N'@Name'"` — المعامل داخل النص فيقارن بالسلسلة الحرفية `@Name` ولا يطابق شيئاً أبداً.
- **الإصلاح:** `name=@Name`.

### NEW-026 — بادئة N قبل المعامل تكسر إدراج مجالات العمل [متوسطة] [sql-syntax] — ✅ مُصلَح
- **الملف:** `Form_WPF/frmActs.xaml.cs:229`
- **الكود:** `INSERT INTO Acts(name) VALUES(N@name)` — خطأ نحوي T-SQL يفشل الإدراج دائماً.
- **الإصلاح:** `VALUES(@name)`.

---

## إحصاءات

| الحالة | العدد |
|---|---|
| مُصلَح في هذا الفرع (`fix/94ae8414-security-remediation`) | 22 |
| مؤجل إلى خطة المراحل (NEW-014، NEW-015، NEW-019) | 3 |
| مُدمج ضمن إصلاح نتيجة أخرى (NEW-017 ضمن NEW-011) | 1 |
| **الإجمالي** | **26** |
