# تسليم المرحلة الثامنة — الإصلاح 1: أمان وتحتية المرحلة الأولى (P1)

**الفرع:** `fix/stage1-p1-security` · **القاعدة:** `arena/94ae8414-smartauditerp` @ `dbf2760` (تسليم R9)
**النطاق:** النتائج P1-001 → P1-033 (33 نتيجة: 2 Critical / 22 High / 8 Medium / 1 Low)

## النتيجة النهائية

| الحالة | العدد | النتائج |
|---|---:|---|
| **remediated-stage1** | 29 | P1-002،003،005،006،007،008،009،010،012،013،014،015،016،017،018،019،020،021،022،023،024،025،026،027،028،029،030،031،032 |
| **remediated-partial-stage1** | 4 | P1-001 (38 DLL خارجية تتطلب ثنائيات المالك)، P1-004 (قوالب .repx من خط الإصدار)، P1-011 (38 موقعًا منخفض الخطورة للمراحل اللاحقة)، P1-033 (كبسات WinForms Designer) |
| متبقٍ مفتوح | 0 | — |

`findings.csv`: تحديث عمود status لـ33 صفًا (CRLF محفوظ بلا BOM؛ 302 صفًا آخر بقيت `open-not-remediated` لمراحل الإصلاح 2–7).

## أبسطة تحتية جديدة
- `Class/Security/PasswordHasher.cs` — PBKDF2-SHA256، 100k تكرار، ملح 128-بت، مقارنة `CryptographicOperations.FixedTimeEquals`، صيغة تخزين ذاتية الوصف.
- `Class/Security/SecretProtector.cs` — DPAPI CurrentUser مع إنتروبيا خاصة بالتطبيق؛ فك فاشل = null (fail-closed).
- `Class/Security/PermissionGate.cs` — قرار Allow/Deny موحد + LogDeny لا يرمي.
- `Class/Security/SqlBatchSplitter.cs` — فاصل دفعات GO حقيقي.
- `SmartAuditUpdater/ManifestSignatureVerifier.cs` — توقيع RSA-SHA256 للمانيفست + تجزئة كل ملف + حارس اجتياز مسار.
- `Updates/GitHubRelease.cs` — عقد إصدار GitHub مطبوع مع عقد اختيار أصول صريح.

## ترحيل قاعدة البيانات (AlterDb — GO جديد ×8)
1. `OperationPermission.pwd_hash nvarchar(512) null`
2. `Users.pwd_hash nvarchar(512) null`
3–6. `SettingSync.MqttPort/MqttUseTls/MqttUser/MqttPass`
7–8. ضمن 8 أعلاه ضمن الدفعات ذات الصلة (إجمالي GO: 546)

## الاختبارات (P1-005)
`tests/SmartAuditERP.SecurityTests` — 24 اختبار xUnit:
- PasswordHasher: الصيغة/الملح/fail-closed/الرفض/المهاجرة/الفراغ.
- SqlBatchSplitter: الفصل الصحيح، لا فصل داخل كلمات/نصوص، حالات GO، الدفعات الفارغة.
- PermissionGate: مصفوفة fail-closed كاملة + LogDeny لا يرمي.
CI: `.github/workflows/build-and-test.yml` — الاختبارات دائمًا؛ البناء الكامل متوقف توافقيًا على توفر `ExternalLibsDir` (P1-001).

## قيود التنفيذ الموثقة (حدود لا ادعاءات)
1. **لم يُبنَ المشروع محليًا** — بيئة التنفيذ بلا dotnet SDK وبلا الـ38 DLL الخارجية (`..\..\المكاتب\`)؛ صحة الترجمة تتأكد عبر CI عند الدفع (البند full-build) — أي فشل ترجمة يظهر هناك ويُصلح فورًا.
2. أرقام أسطر الدليل الأصلية انزاحت بعد التعديلات؛ المُرجِع هو معرف النتيجة (P1-xxx) لا رقم السطر.
3. التوافق التشغيلي قُدّم في مواضع موثقة (P1-014/015/020): المسارات الآمنة مفعلة وقابلة للتهيئة والافتراضي لا يكسر النشر القائم.
4. المهاجرة تدريجية: الدخول القائم بالنص القديم يعمل مرة واحدة ثم يُهاجَر تلقائيًا.

## التحقق المحلي الممكن هنا
- سلامة C#/XML: توازن أقواس كل ملف معدل مطابق لأصله (استُبعدت فروق نصوص المحارب)؛ XML جميع csproj/settings/settings.resx سليم.
- تجزئات البوابات الخمس مولدة ومتحقق منها roundtrip بنفس معاملات PBKDF2.
- findings.csv: 336 سطرًا، تنسيق CRLF، بلا BOM.

## الخطوة التالية
المرحلة 2 (P2 — 16 نتيجة: التفويض والجلسات والمرفقات) وفق الخطة متعددة المراحل، بعد مراجعة/دمج هذا الفرع.
