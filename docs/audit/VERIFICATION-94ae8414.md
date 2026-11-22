# تقرير التحقق من الأخطاء الموثقة — فرع arena/94ae8414-smartauditerp

**التاريخ:** 2026-02-27 (توقيت موسكو)
**الفرع المُدقَّق:** `arena/94ae8414-smartauditerp` (المصدر مطابق تماماً لـ `main` — الفرع أضاف توثيقاً فقط دون أي تعديل كود)
**المنهجية:** تحقق مستقل بقراءة الكود المصدري عند مواقع الأدلة المذكورة في `findings.csv` (335 نتيجة موثقة من الوكيل السابق)، عبر مدقق رئيسي + وكيلي تحقق متوازيين (V1).

---

## الخلاصة

| البُعد | النتيجة |
|---|---|
| النتائج الموثقة في findings.csv | 335 (2 حرجة، 181 عالية، 151 متوسطة، 1 منخفضة) |
| حالة جميع النتائج | `open-not-remediated` (لم يُصلح أي منها في الفرع) |
| عيّنة التحقق المستقل | **33 نتيجة** (11 حرجة/أمنية + 22 عيّنة ممثلة عبر P1–P7) |
| نتيجة التحقق | **33/33 مؤكدة (100%)** — صفر نتائج غير مؤكدة أو مضللة |
| أخطاء جديدة مكتشفة (غير موثقة) | **26** — انظر `NEW-FINDINGS-94ae8414.md` |

**الحكم:** توثيق الوكيل السابق **دقيق وموثوق به**. كل موقع دليل فحص أظهر العيب الموصوف بالضبط (انعكاسات منطقية مثل `|| true` وبوابة المزامنة المعكوسة، وغياب التحقق/الذرية في مسارات القيود والمخزون والمزامنة وZATCA/ETA والرواتب، وفجوات مستودع حقيقية).

---

## أولاً: التحقق الرئيسي (11 نتيجة حرجة/أمنية)

| المعرف | الخطورة | النوع | الحكم | الدليل الفعلي المرصود |
|---|---|---|---|---|
| P1-007 | Critical | security | **مؤكد** | `frmServerSetting.ExecuteDbSetup` ينشئ LOGIN `auditor` بكلمة مرور `auditor` ويضيفه إلى `sysadmin` و`db_owner` ثم يفعّل `sa` ويغيّر كلمته إلى `auditor` — منسوخة حرفياً أيضاً في `frmDataRecycling.xaml.cs:315-322` |
| P1-008 | Critical | security | **مؤكد** | خمس كلمات مرور ثابتة في `frmCheckPwd` (`auditor`, `auditor2021`, `2020AUDITOR`, `DARH2024`, `auditorzatca`) + دخول خلفي `auditor+السنة+الشهر` في `frmUserLogin:192-208` + تجاوز بكلمة `"auditor"` ثابتة في `OfflineLogin:455` + بوابة `auditor/auditor` في `frmLogServerSettings:52-53` |
| P1-009 | High | secrets | **مؤكد** | `SaveStartupData` يكتب `Password` و`ServerPassword` نصاً صريحاً في `StartupData.json` دائماً بغض النظر عن «تذكرني» |
| P1-010 | High | secrets | **مؤكد** | `Users.pwd` عمود `nvarchar(50)` يخزن كلمات المرور نصاً أصلياً ويقارن بمساواة SQL في كل مسارات الدخول |
| P1-011 | High | sql-injection | **مؤكد** | `frmChangePwd:89-95`: `UPDATE Users SET pwd='{txtPass.Password}'` مباشرة + مواقع مماثلة في frmlock/frmCheckPwd/frmAddUsers/frmCustomers |
| P1-012 | High | authorization | **مؤكد** | `MainClass.ApplyPermissionToForm`: `if (dt.Rows.Count == 0) return;` — غياب سجل الصلاحية = سماح كامل (fail-open)، والاستثناء يُبتلع |
| P1-014 | High | transport-security | **مؤكد** | `ConnectBroker:46`: `new MqttClient(_IpServer, 1883, secure: false, ..., MqttSslProtocols.None)` بدون مصادقة |
| P1-015 | High | backup-security | **مؤكد** | `frmBackupRstore.UploadBackup`: رفع FTP مكشوف مع **بيانات مثبتة في الكود**: السيرفر `173.212.208.114` والمستخدم `backup_user` |
| P1-016 | High | authentication | **مؤكد** | `Home.Window_Loaded:405-408` يستدعي `ISSecureLogin()` ويتجاهل نتيجته ويكمل الإقلاع |
| P1-020 | High | update-security | **مؤكد** | المحدّث ينزّل `update.zip` ويثبته دون أي تحقق توقيع/بصمة |
| P1-022 | High | update-integrity | **مؤكد** | `InstallUpdate`: فشل النسخ بعد 5 محاولات يسجل تحذيراً فقط ثم يعلن «تم تثبيت جميع الملفات بنجاح!» ويعيد `true` |

## ثانياً: عينة الوكيل V1 (22 نتيجة عبر المراحل)

| المعرف | الخطورة | الحكم | ملاحظة التحقق |
|---|---|---|---|
| P3-002 | High | مؤكد | `SaveEnty` يقبل قيوداً بدون بنود (Accounts فارغة → Commit ناجح) ولا فحص توازن |
| P3-012 | High | مؤكد | فروق الضريبة/الإضافات/التأمين الموجبة تُقيَّد في **Debit** بدل Credit عند إغلاق الوردية |
| P4-006 | High | مؤكد | `BindingCostDetaile` يتجاهل سياسة `Common.CostType` ويستخدم المتوسط دائماً (أو صفر عند السالب) |
| P4-014 | High | مؤكد | حماية المخزون تعتمد رصيداً في الذاكرة (`ValiableInvertory`) دون إعادة فحص ذرية عند الحفظ — بيع زائد محتمل |
| P5-006 | High | مؤكد | صندوق الصادر دون اتصال (`Itemid.json`) يُفرَّغ **حتى عند فشل النشر** — فقدان بيانات مزامنة |
| P6-004 | High | مؤكد | ZATCA: تقريب مبكر للكمية/السعر + مقامات غير محمية (`d3`/المجموع) → DivideByZero/NaN |
| P6-013 | High | مؤكد | ETA: `quantity = (int)Math.Round(...)` يفقد الكسور بينما المبالغ محسوبة من الكمية الكسرية |
| P7-004 | High | مؤكد | دفع الرواتب يحفظ `SalaryPay` بـ`EntryGlobalID="-1"` دون إنشاء قيد مالي |
| P2-005 | Medium | مؤكد | TreeView الصلاحيات بدون `HierarchicalDataTemplate` — نموذج خام يُضاف للعناصر مباشرة |
| P3-004 | Medium | مؤكد | `SaveReceipt` مع `Entr==null` يقفز إلى `result=true` بدون Commit → تراجع ضمني مع رسالة نجاح |
| P4-026 | Medium | مؤكد | `LoadUnitInf` يرجع بالسعر الخام قبل تطبيق سياسة التسعير في المسار الرئيسي |
| P5-017 | Medium | مؤكد | بوابة المزامنة **معكوسة**: تعمل فقط إذا كان آخر مزامنة أحدث من ساعتين — تتوقف نهائياً عند التقادم |
| P6-024 | Medium | مؤكد | `GetTicketAsync` يهمل نتيجة التحويل ويعيد `Success=true` مع `Ticket=null` |
| P7-009 | Medium | مؤكد | بصمات الحضور: INSERT غير مشروط بلا مفتاح تفرده → تكرار عند إعادة القراءة |
| P1-017 | Medium | مؤكد | تحديثات حالة الدخول تُطبق على نسخ `Home`/`frmSecurityPnl` جديدة غير معروضة أبداً |
| P2-002 | High | مؤكد | `@lock()` يتجاهل نتيجة `frmlock`، ورابط الدخول المتقدم يخفي القفل دون فحص المصادقة |
| P3-001 | High | مؤكد | `CheckProiedAcc` ينتهي بـ`|| true` — يعيد true دائماً؛ المدقق الصارم `ValidateTransactionDate` بلا مستدعين |
| P3-007 | Medium | مؤكد | فحص التوازن يقارن مبالغ مقربة لخانتين مع تخزين double خام في أعمدة Float |
| P1-001 | High | مؤكد | 31 مرجع DLL إلى `..\..\المكاتب\` غير موجودة + مسار NuGet مطلق لمستخدم بعينه — استنساخ نظيف لا يبني |
| P1-002 | High | مؤكد | `UseWPF` فقط دون `UseWindowsForms` رغم استخدام 37 ملفاً لـ`System.Windows.Forms` |
| P1-003 | High | مؤكد | التطبيق يشغّل `update.exe`/`Updater.exe` بينما مخرج المشروع `SmartAuditUpdater.exe` — تعارض الأسماء |
| P1-004 | High | مؤكد | وقت التشغيل يتطلب `Version.txt` وقوالب `.repx` وإعداد log4net — لا شيء منها في المستودع ولا في csproj |

---

## ملاحظات جوهرية على جودة توثيق الوكيل السابق

1. **الدقة الموقعية عالية**: كل مواقع الأدلة كانت صحيحة أو منزاحة أسطراً قليلة فقط.
2. **لا مبالغات**: لم يُرصد أي عنوان نتيجة لا يسنده الكود فعلاً.
3. **الفجوة الوحيدة**: لم يوثّق الوكيل السابق أخطاءً في ملفات فرعية كاملة (frmPaymentVoucher، frmClientPM، frmSuppliers، frmJobs، frmManagement، frmLicenseManagment، frmOffers، frmRecyclingData/frmDBManagment، GetDataAPI، Geidea.cs، FrmUpdate URL…) — سُدّت في `NEW-FINDINGS-94ae8414.md`.
4. الفرع لم يتضمن أي إصلاح: كل النتائج الـ335 ما تزال `open-not-remediated`.

## الروابط ذات الصلة

- الأخطاء الجديدة: [NEW-FINDINGS-94ae8414.md](NEW-FINDINGS-94ae8414.md)
- خطة الإصلاح متعددة المراحل: [FIX-PLAN-94ae8414.md](FIX-PLAN-94ae8414.md)
- سجل الإصلاحات المنفذة في هذا الفرع: [FIXES-LOG-94ae8414.md](FIXES-LOG-94ae8414.md)
