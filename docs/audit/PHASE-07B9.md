# الجزء 7B9 — ملخص سندات العميل/المورد وأندرويد وتقارير الرواتب

**مرجع التدقيق المعلن:** 2026-11-16 UTC. مصدر التطبيق الأصلي `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. **7B9 تسليم ساكن جزئي؛ 7B و 7 غير مكتملتين. 7B10 معلنة للباقي، 7C لم تبدأ، والمرحلة 8 غير مأذونة ولم تبدأ.** لا تشغيل/قبول/قياس ERP أو معالجة تطبيق.

بناء على طلب المستخدم الجديد بالاستمرار ودفع جميع التوثيقات، **دُفعت ملفات التدقيق الـ 274 حتى 7B8 فعلياً** إلى الفرع نفسه عند `3612700aa19ecdd077bc7dabf79eb61136015054` قبل بدء 7B9. تحقق أن البعيد السابق `d0ae6b3` يضيف 204 مسارات تدقيق فقط:199 محفوظة مطابقة بايتياً، والخمسة الأخرى فهارس/سجل/مدقق حي تطورت عمداً. التزام لقطة التوثيق `8b657c9` ثم دمج ancestry محتفظ باللقطة المراجعة حفظا كامل 274 بصمة؛ **لا دفع قسري ولا إعادة كتابة للالتزامات أو مصدر التطبيق أو checks التاريخية.** أصبحت هوية checkout عند الدخول 3612700 بينما المصدر 10ba؛ checksB8 تحتفظ بمشاهدة checkout10ba وقت تسليمها، لا يعاد توليدها لتطابق الدفع الأحدث. [provenanceB9](evidence/provenance-07B9.json) يسجل هذه الحدود؛ فرق metadata الحالي ليس اختلاف مصدر أو فقد أدلة.

## 1. الحصيلة وحدود الأسماء والنطاق

قُرئت الأجسام و XAML المحلية كاملة لـ **frmSummaryQ و frmRptSalary و frmRptReseved**، مع DTOs محلية ومقاطع مختارة من الكاتب/المخطط/المداخل/الطفل. **SummaryQ هو ملخص سندات الأنواع 5/6/10، وليس قائمة قيود الأستاذ. و frmRptReseved تقرير الرواتب المستحقة من Salary_Res، وليس حجزاً بحرياً.** كما أن SalaryRow العام لتقرير الصرف ليس SalaryRow المتداخل في FrmReseved. لا تصحيح تخميني لتاريخ محمي بسبب تشابه الاسم.

| المقياس | الحصيلة المحدودة |
| --- | --- |
| الجديد | نتيجتان P7-109 و P7-110، متوسطتان:1 confirmed محلياً و 1 potential، مفتوحتان دون معالجة. |
| السابق | 11 امتداداً تحت أصولها، مع حفظ 280 core وكل next_phase؛ لا finding لكل query/زر/conversion. |
| التراكمي | 282 مفتوحة:2 حرجة/175 عالية/104 متوسطة/1 منخفضة؛ 245 confirmed/30 potential/7 repository-gap. |
| المسارات | 19 مختارة، 17 تتداخل مع 373 و 2 جديدة؛ اتحاد 375 ومكمل 452 inventory-only، فضلاً عن مقاطع لم تختَر داخل 375. |
| الأجسام المحلية | 976 سطراً C# +1471 XAML =2447؛ مقاطع DTO إضافية 48 سطراً، لا كل feature/caller/child أو schema/ACL/نشر. |
| المصفوفة | 20 صف FE و 20 ثابت INV و 6 عقود RC و 6 H و 6 Q و 10 مجموعات استمرار. |
| القبول | 22 خطة كلها not-executed:4 خاصة بالجديد+11 انحدار أصل+5 عقود+2 بوابة. |
| فحوص الوثائق | 18 نموذجاً يدوياً+18 ملاحظة نصية؛ 24 حالة اصطناعية جديدة لمدقق الوثائق فقط، لا ERP. |

**confirmed** تعارض محلي بشروطه، لا واقعة بيانات إنتاج أو كشف أشخاص. **potential** لا ترتقي من fixture/Python. النموذج الذي يكرر سند 100 إلى 200 لا يثبت وجود مستخدمين مكررين في النشر؛ كما لا يعني غياب Branch predicate محلياً انتفاء كل تفويض خادم. قراءة تقرير رواتب لا تمنح حكماً على قانون الرواتب/الضرائب أو موقع التطبيق من موقع المستخدم.

## حفظ المصدر والتاريخ

- ثُبتت لقطة الدخول **مرة واحدة**: [سجل 280](evidence/findings-through-07B8.csv)، SHA256=`83a128fea7d8dd7c15b1e9ef7daaf1064850ffc70d1a6ea5f4ac149708d4c33f`؛ [فهارس B8 الدقيقة](evidence/shared-indexes-through-07B8.json)، SHA256=`3352cbd299295853e83e078579ab4f78455f5a3754d532d6df23a45b0169b2e2`. لا إعادة تهيئة snapshots أو baseline.
- تحمي provenanceB9 **269 ملفاً تاريخياً غير قابل للتعديل**، بينها كامل تقارير وأدوات وشواهد و checksB8. ملفات القديم الحية القابلة للتحديث المعلن فقط:README/PLAN/IMPROVEMENTS/findings/validate_audit. **أول 280 نتيجة في كل حقولها غير الدليل وكل next_phase محفوظة**، مع بادئات الدليل و 11 ذيلاً معلناً فقط؛ لا إعادة تصنيف/إغلاق أو replan خفي.
- [checksB8 الحقيقي](evidence/checks-07B8.json) بقي SHA256=`598f4ec4865b2a1e21a90b84860cfc59b13296fc7831dba8962d568cc4cec9ef` دون إعادة كتابة بعد الدفع. محول B9 يعطي helperB8 frozen280 وفهارسه الأصلية **في الذاكرة عند المسارات المنطقية الدقيقة**، ولا يمرر له 282 أو فهارس اليوم. كل الأجزاء الأسبق بمدخلاتها الخاصة كذلك.
- **G01–128 صفوف توصيات محفوظة حرفياً**، وتضاف G129–134 فقط؛ ليست نتائج أخرى. findings الحي يبقى CRLF. مصدر 827 path/hash يفحص مستقلاً عن ancestry وصافي دلتا شجرة Git docs-only؛ ليس ذلك توقيعاً أو إثبات كل تاريخ وسيط أو تفويضاً لمعالجة.
- ساعة البيئة المشاهدة في الدخول `2026-11-18T05:11:52.627050+00:00` منفصلة عن المرجع المعلن 16 نوفمبر وعن مواعيد الأرشيف؛ لا تاريخ تشغيل/قبول تطبيق مستنتج منها.

## النطاق المقروء

| المسار | الأسطر المختارة | حد القراءة |
| --- | --- | --- |
| `SmartAuditERP/Class/MainClass.cs` | `45-49` | مصنع اتصال جديد فقط؛ لا كل ملكية/تسريب موارد. |
| `SmartAuditERP/Class/Reseved.cs` | `268-345` | binder القديم DataRow وبوابة NULL فقط؛ لا كل SaveReceipt1 أو قبول قيد. |
| `SmartAuditERP/Class_WPF/ResevedRow.cs` | `1-15` | DTO رأس تقرير الاستحقاق فقط. |
| `SmartAuditERP/Class_WPF/SalaryRow.cs` | `1-16` | DTO صف تقرير الرواتب؛ ليس SalaryRow المتداخل في FrmReseved. |
| `SmartAuditERP/Class_WPF/StockSyncItem.cs` | `21-37` | ReceiptQItem فقط داخل ملف StockSyncItem؛ لا بقية مزامنة المخزون. |
| `SmartAuditERP/Form_WPF/FrmReseved.xaml` | `329-357` | بداية Grid واختيار IsSelected مقابل DataView فقط، لا كل واجهته. |
| `SmartAuditERP/Form_WPF/FrmReseved.xaml.cs` | `37-104;355-429;888-907` | المصدر الداخلي و Loaded/CLR والجزء المختار من save ونوع صفه؛ لا بقية محرر الاستحقاق أو ترحيله. |
| `SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs` | `210-249` | شاهد مقابل:lookup بالموظف ثم insert/update؛ لا بيانات/كلمات مرور فعلية ولا إغلاق كل الهوية. |
| `SmartAuditERP/Form_WPF/frmRptReseved.xaml` | `1-394` | جسم/XAML محلي كامل لـ frmRptReseved فقط؛ لا كل caller/child/template/schema/ACL أو نشر/قبول. Reseved هنا استحقاق رواتب لا حجز بحري. |
| `SmartAuditERP/Form_WPF/frmRptReseved.xaml.cs` | `1-226` | جسم/XAML محلي كامل لـ frmRptReseved فقط؛ لا كل caller/child/template/schema/ACL أو نشر/قبول. Reseved هنا استحقاق رواتب لا حجز بحري. |
| `SmartAuditERP/Form_WPF/frmRptSalary.xaml` | `1-490` | جسم/XAML محلي كامل لـ frmRptSalary فقط؛ لا كل caller/child/template/schema/ACL أو نشر/قبول. Reseved هنا استحقاق رواتب لا حجز بحري. |
| `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs` | `1-191` | جسم/XAML محلي كامل لـ frmRptSalary فقط؛ لا كل caller/child/template/schema/ACL أو نشر/قبول. Reseved هنا استحقاق رواتب لا حجز بحري. |
| `SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs` | `340-354;359-398;471-487;531-553` | RecalcNet و Navigate/ReadData ومقاطع writer الصافي/الهوية فقط؛ لا دورة صرف كاملة أو GL. |
| `SmartAuditERP/Form_WPF/frmSandQ.xaml.cs` | `624-683;914-929` | Navigate/ReadData وهوية كاتب سند 5 فقط، لا حفظ/تعديل/حذف أو تفويض الطفل كله. |
| `SmartAuditERP/Form_WPF/frmSummaryQ.xaml` | `1-587` | جسم/XAML محلي كامل لـ frmSummaryQ فقط؛ لا كل caller/child/template/schema/ACL أو نشر/قبول. Reseved هنا استحقاق رواتب لا حجز بحري. |
| `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs` | `1-559` | جسم/XAML محلي كامل لـ frmSummaryQ فقط؛ لا كل caller/child/template/schema/ACL أو نشر/قبول. Reseved هنا استحقاق رواتب لا حجز بحري. |
| `SmartAuditERP/Home.xaml` | `414-416;461-463;525-531` | ربط قوائم السندات والرواتب وحالات IsEnabled فقط؛ لا إتاحة دور منشور. |
| `SmartAuditERP/Home.xaml.cs` | `125-126;176-177;242-243;3037-3043;3369-3375;3643-3646` | static refs ومداخل التقارير/المحررين وتطبيق Apply قبل Show فقط؛ لا كل Home أو ACL. |
| `SmartAuditERP/Properties/Resources.resx` | `38-58;242-275;714-751;1496-1532;1778-1800;2166-2179;4523-4554` | DDL محلي للحساب/الفرع/الموظف/السند/SalaryPay/Users/Salary_Res/details؛ لا كل schema/ترحيلات أو بيانات نشر. |

[scope19](review-scope-07B9.csv)، [دفتر 827](evidence/coverage-ledger-07B9.csv)، [98 مرشح ملف](evidence/report-candidate-disposition-07B9.csv) و[52 شاشة](evidence/report-screen-disposition-07B9.csv) حصر وتتبع لا نسب اكتمال ميزات أو إتاحة. الاسم/all-lines/ظهور طفل في Navigate لا يمنحه تغطية الأب. الباقي 7B10/7C ظاهر، أو يلزم استبعاد مسند/جزء إضافي.

## 2. النتائج الجديدة

### P7-109 — معيار فترة تقرير الرواتب يتسع إلى كل الفترات عند فشل تحويل الشهر أو السنة

**الخطورة:** متوسطة؛ **الإثبات:** `confirmed`؛ `open-not-remediated`؛ `next_phase=8` تخطيط لا إذن تشغيل أو إصلاح.

عند إلغاء كل الفترة، لا يضاف شرط الشهر/السنة إلا إذا نجح int.TryParse لكليهما. إدخال شهر غير رقمي أو سنة فارغة يترك condWhere فارغاً ويطلب كل SalaryPay غير المحذوفة بدلاً من رفض المعيار. الشهر الرقمي13 يضيف شرط 13 وقد يعيد صفراً، وليس حالة التوسيع نفسها.

**الأثر المحدود:** اتساع نتيجة مالية/شخصية إلى غير الفترة التي قصدها المستخدم وفقدان دقة معيار التقرير، دون إثبات وصول دور غير مفوض. المسار الافتراضي كل الفترة صريح ومشروع إذا فوضته السياسة، وليس هو حالة الفشل.

**المقترح، غير المنفذ:** تحقق إلزامي من سنة/شهر صالحين ومجالهما قبل مسح أو استعلام؛ المعيار غير الصالح لا يتحول إلى all-period. حافظ على صلاحيات نطاق الفرع مستقلة.

**التحقق اللاحق:** P7B9T-01 و P7B9T-02، كلاهما not-executed. اختبر أيضاً السنة الفارغة/المدخل الصحيح و 0/13 كرفض مجال مستقل؛ لا SQL حي.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:57-88`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml:181-225`.

### P7-110 — ربط ملخص السندات بالمستخدم عبر الموظف قد يكرر السند ومبلغه عند تعدد صفوف المستخدمين

**الخطورة:** متوسطة؛ **الإثبات:** `potential`؛ `open-not-remediated`؛ `next_phase=8` تخطيط لا إذن تشغيل أو إصلاح.

LEFT JOIN Users.emp=Receipts.EmpId لا يحدد صف مستخدم واحداً ولا يستبعد المحذوف، ثم كل صف ينقل إلى المجموعة ويجمع Payment. في fixture لموظف 7 ومستخدمين 11/12 وسند 100 تظهر نسختان ومجموع 200. DDL المحلي يقيد Users.id فقط؛ لكن شاشة المستخدمين تبحث بالموظف وتحدث الموجود، وهي شاهد على قصد التفرد لا ضماناً ذرياً. وجود تكرار منشور أو قيد خارجي لم يفحص، لذلك يبقى الخطر potential ولا يعد التقرير أو الهوية مخترقين.

**الأثر المحدود:** انحراف عدد الصفوف وإجمالي Payment إن سمح المخطط/البيانات المنشوران بأكثر من Users row لنفس EmpId. القيد الخارجي/المطابقة الفعلية لم يفحصا. UI lookup/update شاهد مقابل، فلا زعم تضاعف دائم أو خلل في مبلغ السند المحفوظ نفسه.

**المقترح، غير المنفذ:** عقد هوية الموظف/المستخدم وتعدد الحسابات وتاريخ الاسم أولاً؛ مصدر اسم مفرد لا يغير حبيبة السند، ومصالحة GlobalID/عدد الصفوف/المبلغ. لا DISTINCT على القيم المالية أو حذف مستخدمين/بيانات عشوائياً لإخفاء السبب.

**التحقق اللاحق:** P7B9T-03 و P7B9T-04، كلاهما not-executed. قارن مستخدماً واحداً/متعددين/محذوفاً وسندين مستقلين متساويي المبلغ؛ لا DISTINCT مالي أو حذف بيانات للعلاج.

**الدليل:** `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:233-251`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:277-315`؛ `SmartAuditERP/Properties/Resources.resx:2166-2179`؛ `SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs:210-249`.

## 3. الامتدادات المعلنة بلا نتائج مكررة

| الامتداد | الأصل | الملاحظة وحدها | المعالجة المقترحة | الدليل |
| --- | --- | --- | --- | --- |
| EX7B9-01 | P1-004 | SummaryQ يقرأ SettingPrint ثم يفحص rptSummaryD.repx وينتهي إلى SetStatus فارغة؛ وجود ملف قالب لا ينفذ renderer. لا إعادة كتابة فجوة القوالب التاريخية أو افتراض قالب منشور. | manifest/DTO وتبعية مستهلكة فعلاً، مع تنفيذ قدرة أو تعطيلها صراحة؛ لا قالب فارغ للعلاج. | `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:145-168`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:514-545` |
| EX7B9-02 | P1-013 | تطبيق Home للصلاحيات يسبق Show للتقارير الثلاثة، وبعض القوائم disabled. الأطفال يعرضون من داخل التقارير بلا Apply محلي ظاهر. النتيجة التاريخية potential محفوظة؛ هذا لا يثبت فشل حارس الطفل/الخادم أو إتاحة دور منشور. | مصفوفة دور×مدخل×عرض/تفاصيل/إنشاء/تصدير×فرع وحارس حد موثوق، ثم اختبار مستقل معتمد لا فحص visual-tree فقط. | `SmartAuditERP/Home.xaml.cs:3037-3043`؛ `SmartAuditERP/Home.xaml.cs:3369-3375`؛ `SmartAuditERP/Home.xaml.cs:3645-3646`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:424-451`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:129-155`؛ `SmartAuditERP/Form_WPF/frmRptReseved.xaml.cs:155-168`؛ `SmartAuditERP/Home.xaml:414-416`؛ `SmartAuditERP/Home.xaml:461-463`؛ `SmartAuditERP/Home.xaml:525-531` |
| EX7B9-03 | P1-030 | التقارير الثلاثة static محفوظة في Home وأمر الخروج Close؛ الاستدعاء التالي يستعمل instance نفسها. Hide لتقرير الاستحقاق بعد فتح child مسار آخر، وليس إصلاحاً لـ Close/reopen. | عمر نافذة/جلسة صريح وإنشاء نسخة بعد Closed؛ اختبر close/reopen وتبديل المستخدم والفرع دون تعميم على new children. | `SmartAuditERP/Home.xaml.cs:125-126`؛ `SmartAuditERP/Home.xaml.cs:176-177`؛ `SmartAuditERP/Home.xaml.cs:242-243`؛ `SmartAuditERP/Home.xaml.cs:3037-3043`؛ `SmartAuditERP/Home.xaml.cs:3645-3646`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:374-374`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:166-167`؛ `SmartAuditERP/Form_WPF/frmRptReseved.xaml.cs:202-203` |
| EX7B9-04 | P1-033 | تفاصيل النوع 5 تفتح frmSandQ فعلاً بنوع+GlobalID؛ 6 و 10 رسالتان واستدعاءاتهما معلقة. طباعة/معاينة SummaryQ وبحث الحساب stubs؛ Salary يعلن صراحة أن الطباعة/المعاينة غير مفعلة. لا finding لكل زر، ولا وصف النوع 5 فارغاً أو Salary قدرة طباعة منفذة. | حسم متطلب كل أمر؛ تنفيذ موثق أو تعطيل معلن، مع اختبار أثر لا وجود رسالة/ملف؛ لا يرث طفل 10 تغطية من تعليق. | `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:376-378`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:424-471`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:514-545`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml:295-314`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml:506-519`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:165-180`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml:475-485` |
| EX7B9-05 | P2-010 | SummaryQ يختار Branches.id ويقرأ الاسم بـ BranchId ويستبدل NULL BranchID بـ 1. LoadAccounts يطلب Branch بينما DDL المحلي Acc_branch. تقريرا الرواتب لا يضيفان predicate فرع في المصدر المحلي رغم وجود عمود branch؛ لا يثبت ذلك وحده تجاوز تفويض خارجي. | هوية فرع canonical وتقاطع مفوض مستقل عن كل/عدم اختيار، وتطابق عمود الدليل وإصدار المخطط؛ لا أسماء افتراضية لفرع مجهول أو افتراض بيانات منشورة مختلفة. | `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:80-117`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:196-207`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:233-251`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:350-362`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:75-86`؛ `SmartAuditERP/Form_WPF/frmRptReseved.xaml.cs:62-68`؛ `SmartAuditERP/Properties/Resources.resx:38-58`؛ `SmartAuditERP/Properties/Resources.resx:242-275` |
| EX7B9-06 | P3-023 | تقرير الاستحقاق يبني ToShortDateString ويستعمل Date<=يوم النهاية، فيستبعد أوقاته اللاحقة إذا فسر SQL النص كما قصد. الثقافة/لغة SQL عقد إضافي. SummaryQ شاهد مقابل: DateTime typed وحد أعلى < اليوم التالي، فلا ينسب إليه خلل منتصف الليل نفسه. | فترات typed نصف مفتوحة مع دقة/timezone وسياسة invalid/NULL date؛ لا استبدال تنسيق نصي ثقافي بآخر. | `SmartAuditERP/Form_WPF/frmRptReseved.xaml.cs:188-199`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:214-224`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:256-267` |
| EX7B9-07 | P7-002 | التقرير يملأ DataView و IDs قبل Show، ثم Loaded للطفل ينفذ CLR ويمسح IDs ولا يعيد تعبئة _salarySource. يسبق ذلك حاجز إعداد عند حساب موظف NULL/غير موجود: ISNULL(AccCode,'') ثم Convert.ToInt32 قد يفشل قبل الفتح؛ يذكر تحت عقد تسليم التفاصيل نفسه لا finding آخر لكل conversion. Accounts_Index.Code محلياً int؛ لا نفترض أكواد دليل حرفية صالحة. | مسار Load/DTO typed واحد يحفظ الهوية والفترة والمصدر الداخلي بعد Loaded ويعالج حساباً مجهولاً صراحة؛ اختبر بوابات الإعداد ثم التحميل كلّاً مستقلاً، لا عرض جدول فقط. | `SmartAuditERP/Form_WPF/frmRptReseved.xaml.cs:107-168`؛ `SmartAuditERP/Form_WPF/FrmReseved.xaml.cs:37-64`؛ `SmartAuditERP/Form_WPF/FrmReseved.xaml.cs:76-104`؛ `SmartAuditERP/Form_WPF/FrmReseved.xaml.cs:355-370`؛ `SmartAuditERP/Form_WPF/FrmReseved.xaml:329-357`؛ `SmartAuditERP/Properties/Resources.resx:38-58`؛ `SmartAuditERP/Properties/Resources.resx:734-749` |
| EX7B9-08 | P7-006 | تقرير الرواتب يعيد net=basic+houses+travel+add-sub ولا يستهلك salary_net المقروء من SQL؛ المحرر يعيد تحميل salary_net المحفوظ. قد يعرض التقرير 125 بينما السند/المحفوظ 100 في fixture العيب السابق. إعادة الحساب في التقرير لا تصلح writer ولا تعني أن الصافي المالي أو GL تمت مصالحته. | مصدر صافي موحد بإصدار وسياسة تقريب/NULL، ومصالحة القيم المحفوظة/المعروضة والمستند/GL؛ لا UPDATE تصحيحي من التقرير أو ترقيع بيانات. | `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:75-121`؛ `SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs:359-398`؛ `SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs:471-487`؛ `SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs:531-553` |
| EX7B9-09 | P7-046 | SummaryQ و Salary يمسحان الصفوف قبل التعبئة ويحدثان الإجمالي بعد نهاية النجاح فقط؛ الفشل قد يبقي إجمالي A فوق قائمة فارغة/جزئية B. Salary يحول أعمدة DDL قابلة NULL مباشرة، و GetBranchName/SetStatus في SummaryQ يخفيان نوعاً من الفشل. مسار العرض متزامن، فلا يكرر P7-107 أو P7-054 تلقائياً. | حالة result/error/partial ونشر rows+total ذري أو لقطة قديمة موسومة، وتحويل nullable بعقد؛ لا صفر/اسم فارغ بديل لصحة المصدر. | `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:174-179`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:269-322`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:350-362`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:545-545`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:57-61`؛ `SmartAuditERP/Form_WPF/frmRptSalary.xaml.cs:92-127`؛ `SmartAuditERP/Properties/Resources.resx:1785-1793` |
| EX7B9-10 | P7-048 | زر تصدير Excel يحفظ CSV معلناً ذلك في dialog، لكن يبني 11 عموداً بتنسيق N2 ونص خام بلا ترميز. فاصلة الألوف/اسم يحوي فاصلة أو quote/newline لا يحقق round-trip. لا P7-050 لأن الامتداد/المحتوى CSV هنا متوافقان. | مرمز CSV لكل الحقول وثقافة مخطط موثقة واختبارات round-trip11 خلية؛ لا تبديل بيانات العميل لإرضاء delimiter. | `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:396-410`؛ `SmartAuditERP/Form_WPF/frmSummaryQ.xaml:571-577` |
| EX7B9-11 | P7-049 | النص الخام يرسل إلى CSV ثم ShellExecute؛ أثر الصيغ معلق بعقد المستهلك ولم ينفذ. using block يغلق الكاتب قبل Process.Start، شاهد مقابل لـ P7-108؛ finalize/escaping لا يثبتان نصاً خاملاً. | نص خامل وفق المستهلك المعلن وسياسة فتح مستقلة، لا Office أو محرك صيغة حقيقي في هذا التدقيق؛ الخطر التاريخي يبقى potential. | `SmartAuditERP/Form_WPF/frmSummaryQ.xaml.cs:396-414` |

### حدود سببية وشواهد مقابلة

- **P7-109** خطأ سياسة المعيار عند parsefailure، لا P7-068 الخاصة بفهرس 0 أو مجرد بطء عرض. **P7-110** شرط حبيبة join وإثراء اسم، لا P2-007 لخلط id/emp في إدارة الهوية ولا P7-076 لعمود Safe_Emps المفقود. لا نتيجة لكل JOIN.
- **P7-002** لم يعالج: قد يفشل إعداد AccCode المجهول قبل فتح الطفل؛ وإذا عبرت بوابة الإعداد فالـ DataView والـ IDs يعينان **قبل Show** ثم Loaded يستدعي CLR. المصدر الذي يحفظه الطفل `_salarySource` غير DataView المعروض. لا يُفترض تجاوز هذا الحاجز للحكم على قيد لاحق؛ عيوب binder/Emp السابقة باقية P7-001/003.
- **P7-006** لا تغلق لأن تقرير Salary يعيد الحساب: التقرير قد يعرض 125 والمحرر/الكاتب يحملان 100 من salary_net. مصدر الحقيقة والتقريب/NULL ومطابقة GL والسياسة مستقلة؛ لا UPDATE/ترحيل تصحيحي في التدقيق.
- **SummaryQ يستعمل DateTime typed وحداً أعلى نصف مفتوح فعلاً**، بخلاف نص نهاية يوم Reseved. ويفتح النوع 5 بـ receiptType+GlobalID؛ فلا تعميم P3-023/P7-061 عليه. SalaryPay.id مفتاح أساسي في DDL المحلي، وليس رقم مستند محلياً مكرراً بالفرع دون دليل.
- **CSV يغلق using block قبل Process.Start**؛ لا امتداد P7-108. file dialog يعلن CSV والمحتوى CSV، لا TSV أو P7-050 رغم عنوان زر Excel. P7-048 للنحو و P7-049 المحتملة للمستهلك عقدان مختلفان عن finalize.
- SummaryQ لا renderer بعد فحص REPX؛ هو stub تحت P1-033/P1-004، لا FlowDocument محجوب P7-097. Salary يعلن عدم تفعيل الطباعة/المعاينة؛ لا نختلق طباعة له أو لتقرير Reseved، ولا عيباً جديداً لكل زر.
- قراءة Code للحساب من lookup تستند إلى int في DDL المحلي و combo غير editable؛ **لا امتداد P1-011 من interpolation وحده**. عمود Branch في LoadAccounts لا يطابق Acc_branch المحلي ويخفي SetStatus الخطأ؛ هذه بوابة مخطط/نطاق وليست دليلاً على SQL injection منشور.
- عرض هذه التقارير متزامن في UI، لا Task/Thread فيمسارات Show المختارة؛ **لا امتداد P7-054 أو P7-107**. مسح rows قبل نجاح Fill/update-total يدخل P7-046، لا finding آخر لكل catch. N+1 لـ GetBranchName و Fill متزامن/no paging مؤشرات مصدر لا قياس latency/index/leak. صلاحيات Home و static/Close معروفة بلا تعميم غياب حارس خارجي أو تسريب موارد شامل.

## 4. المعالجات والباقي

الأولوية المقترحة: رفض معيار الشهر/السنة غير الصالح قبل الطلب، تثبيت حبيبة السند/هوية المستخدم بعقد تفرد/تعدد معلن دون إخفاء مالي بـ DISTINCT، هوية فرع و BranchScope موحدان، مصدر صافي/NULL/تقريب ومصالحة GL مستقلة، تحميل typed للطفل بعد Loaded ومن مصدر حفظه نفسه، ثم نشر rows/total ذري وعمر جلسة/نافذة واضح و CSV encoder ومستهلك نص خامل وقدرات معطلة أو منفذة صراحة. لا إصلاح تطبيق في هذا الجزء.

التفصيل في[مصفوفة 20/20 وعقود 6](RECEIPT-PAYROLL-REPORTS-07B9.md)، و[22 خطة وحدود التحقق](VALIDATION-07B9.md)، و[IMPROVEMENTS](IMPROVEMENTS.md) G129–134. الدليل الفعلي للمدقق يحفظ في[checksB9](evidence/checks-07B9.json)، لا شهادة مالية/أمنية أو نجاح اختبارات ERP.

**التالي 7B10** لبقية التقارير/callers/children/output/template/schema/ACL والإتاحة أو استبعادات مسندة وأجزاء إضافية. **7C لم تبدأ** لبقية HR/PM/بحري/UI ودورة النوافذ/events/resources/timers/async/connections والاختصارات/RTL/accessibility/cultures/messages وأداء المصدر. لا إغلاق 7B/7 إلا بمصفوفة قدرة×شاشة×implementation×test/استبعاد حقيقية؛ **8 غير مأذونة**، واستمرار المستخدم/دفع التوثيق لا يأذن بناء/تشغيل/قياس/معالجة.
