# عقود التنقل ونتيجة التحميل —7B31 / R4o

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**مدخل B31:** تسليم B30 المدفوع `038a18b74acb92c35a6172d4619fee5712424489`؛ **905 مواد تدقيق و332 نتيجة مفتوحة**. مرجع تاريخ المتابعة **2026-11-16 UTC**؛ رصد ساعة البيئة الخام عند التجميد `2026-11-20T18:03:06.407876+00:00` محفوظ بدلالته المستقلة،لا معايرة أوإعادة تأريخ للأرشيف. [التفصيل](DATE-IDENTITY-NOTE-07B31.md).

**تدقيق ساكن فقط؛ لا تعديل للتطبيق أوإصلاح أوتشغيل ERP. R4o شريحة محدودة؛ 7B والمرحلة7 جزئيتان؛ R4p/7B32 مقترح أوتقسيم مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة هنا.** الإصلاح في محادثة وفرع مستقلين،وحالة بدئه وتزامنه غير معلومة. لا دمج repair→audit أوكتابة ملفاته أوإغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[النتيجة](PHASE-07B31.md) · [العقود](NAVIGATION-LOAD-CONTRACTS-07B31.md) · [التحقق](VALIDATION-07B31.md) · [المتبقي](PHASE-07-REMAINING-07B31.md) · [الهوية والتاريخ](DATE-IDENTITY-NOTE-07B31.md) · [النطاق](review-scope-07B31.csv) · [قرار الاختيار](evidence/scope-decision-07B31.json) · [السجل](findings.csv) · [stdout الرسمي](evidence/checks-07B31-final.json)

## 1. الدخول والمصدر والمخرج والاستبعاد

المدخل هوtoolbar صريح فيمحرريالبيعوالشراء،لاكلNavigate. المصدرالأوليcurrenteditor،ومصدرالهدفBindingInvoiceالمحدود؛المخرجبعدالحسمإماهدفمكتملبهويةطلبأونتيجةEmpty/Failed/Partialغيرمنشورةعلىالأصل. هذا **عقدمقترحغيرمنفذ**،لاوصفلإصلاحموجود.

**الأحدث: 7B31/R4o؛ P7-161 واحدة Medium/confirmed مصدرية محلية،وصفر امتدادات تاريخية.** التراكمي **333 نتيجة مفتوحة بلا معالجة: 2Critical / 181High / 149Medium / 1Low؛ 294confirmed / 32potential / 7repository-gap**.

- **يكفي Empty معلومة دون فشل:** في أوامر التنقل المحروسة،يستبدل `CLR` مرجع المحرر قبل قراءة الهدف. `HasRows=false` يضع `null`،ثم يخصص الأب جديداً ويعيد `CLR`؛مع رجوع التصفير والترقيم طبيعياً يصل `ISNew=true`. لا يلزم محرر dirty أوإلغاء حوار أوفشل SQL لإظهار السبب.
- **ضابط قائم لا غياب حارس:** `No` في `CheckBeforeClear` يمنع أول كتابة. `Yes` أوclean لا يشهدان بنجاح قراءة الهدف. P7-159 وذيل دليله من B30 وP7-160 ثابتة وليستا أصلين جديدين هنا.
- **حدود القارئ:** `void/ref/null` يلتقي فيه empty والاستثناء الخارجي؛لكن catch الصف الداخلي قد يبقي `nonnull`. لا تعتبر كل استثناء null،ولا nonnull شهادة اكتمال تحميل.
- **حدود التصفير:** الرقم يسبق أعلام reset. CLR المشتريات قد يبتلع فشل رقم مورّد ويواصل؛في البيع قد يخرج قبل القارئ. لم نُحدث فشل provider أوWPF،ولا نفترض defaults للـSDK أوحالة مستقرة بعد الأحداث أوحذف بيانات محفوظة.
- **عمق محدد:** 14 شريحة في5 مسارات سابقة كلها؛طريقة القارئ290 سطراً كاملة محلياً لا ملفاً كاملاً أوكل helper/SDK/متصل. الاتحاد يبقى427 والمتمم400؛هذا دفتر مسارات لا نسبة قدرات أو400 مهمةC. ترشيح332 metadata و79 صفاً مطابقاً ليس قراءة332/79 متناً.

## 2. دفتر سلسلة التنقل NL8

| الحد | المصدر إلى المخرج | الملاحظة المصدرية وحد الحكم |
|---|---|---|
| NL7B31-01 / toolbar-wiring | toolbar next/previous/first/last بعد حارس يسمح → CLR يستبدل الرأس ويمسح _invoiceItems قبل القارئ؛HasRows=false→null→new+CLR ثانية | `eight-toolbar-entrypoints-only`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-02 / abandon-guard | CheckBeforeClear وMessageBoxResult.No → أوامر toolbar الثمانية تحترم No؛لا CLR أوBindingInvoice عند الرفض | `No-stops-before-first-write`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-03 / pre-read-CLR | toolbar next/previous/first/last بعد حارس يسمح → CLR يستبدل الرأس ويمسح _invoiceItems قبل القارئ؛HasRows=false→null→new+CLR ثانية | `original-reference-replaced-before-target-read`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-04 / reader-boundary | BindingInvoice try/outer-catch → Open/ExecuteReader أوتحويل خارجي إذا فشل إلى outer-catch يضع ref=null؛الأب يعيد CLR | `void-ref-null-collapses-empty-and-outer-failed`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-05 / nonnull-publish | فرع Invoic!=null بعد القارئ → الأب يحاول BindingDGV ثم BindingControls؛القارئ يكتب ISNew=false/IsPrinted=true عند رأس found | `nonnull-attempts-binding-not-full-health`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-06 / null-fallback | toolbar والتحقق ثم Navigate → CLR يفصل مصدر Grid ويستبدل Invoic؛نتيجة null تعيد new+CLR،ولا rollback للأصل | `empty-or-outer-failed-reaches-new-and-second-CLR`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-07 / reset-number-boundary | null branch→new→CLR ثانية → إحلال إضافي بعد empty/outer-failure؛شراء يبتلع الرقم وبيع قد يرمي قبل أعلام ISNew التالية | `number-before-ISNew-purchase-swallow-sale-escape`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |
| NL7B31-08 / outcome-and-identity-contract | عقد المصدر/النتيجة/النشر المقترح غير المنفذ → void+ref وnull يخلطان Empty/Failed،وnonnull لا يثبت completeness؛لا Apply قبل resolve | `resolve-then-validate-then-publish-proposed-not-implemented`؛ عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة. |

## 3. دفتر نتيجة القارئ LO8

| الحد | النتيجة المميزة | المصدر والمقترح وحد الخروج |
|---|---|---|
| LO7B31-01 / empty-purchase | `two-CLR-cycles-after-nonnull-original-and-normal-resets` | toolbar next/previous/first/last بعد حارس يسمح → CLR يستبدل الرأس ويمسح _invoiceItems قبل القارئ؛HasRows=false→null→new+CLR ثانية؛ تحديد Found/Empty/Failed/Partial وBoundary بلا تغيير للأصل حتى نجاح التحضير،وفصل قرار ترك المسودة عن صلاحية الهدف. |
| LO7B31-02 / empty-sale | `same161-second-editor-not-another-root` | toolbar والتحقق ثم Navigate → CLR يفصل مصدر Grid ويستبدل Invoic؛نتيجة null تعيد new+CLR،ولا rollback للأصل؛ تحديد Found/Empty/Failed/Partial وBoundary بلا تغيير للأصل حتى نجاح التحضير،وفصل قرار ترك المسودة عن صلاحية الهدف. |
| LO7B31-03 / outer-failed-before-header | `outer-catch-null-not-provider-failure-observed` | BindingInvoice try/outer-catch → Open/ExecuteReader أوتحويل خارجي إذا فشل إلى outer-catch يضع ref=null؛الأب يعيد CLR؛ توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا. |
| LO7B31-04 / outer-failed-after-header | `partial-working-header-can-be-discarded-not-original-restored` | قارئ mutates ref ثم outer-catch → رأس يكتب على working editor ثم fill/مساعد خارجي قد يرمي؛outer-catch يضع null→fallback؛ توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا. |
| LO7B31-05 / found-nonnull | `one-preclear-then-binding-attempted-not-completeness-proof` | فرع Invoic!=null بعد القارئ → الأب يحاول BindingDGV ثم BindingControls؛القارئ يكتب ISNew=false/IsPrinted=true عند رأس found؛ تعيين ملكية editor/working-copy/line identity ونتيجة اكتمال مصدرية قبل النقل إلى UI،دون تشغيل SDK أوتحميل DLL. |
| LO7B31-06 / row-caught-nonnull | `inner-row-catch-may-retain-nonnull-not-all-errors-null` | catch projectError4 داخل حلقة البنود → قد يتخطى الصف ويستمر؛بعض catch محلية؛لا تعميم كل استثناء إلى ref=null؛ تعيين ملكية editor/working-copy/line identity ونتيجة اكتمال مصدرية قبل النقل إلى UI،دون تشغيل SDK أوتحميل DLL. |
| LO7B31-07 / first-reset-number-failure | `purchase-may-continue-sale-stops-before-reader-under-supplied-failure` | ResetInvoice خارج catch المحلي → قد يخرج فشل الرقم بعد unbind/new وقبل BindingInvoice؛لا يصح ادعاء fallback أوقراءة لكل طريق؛ فصل تحضير رقم وحالة جديدة عن نشرها؛توثيق أخطاء CLR والربط حسب عقد الأحداث دون إصلاح أوتجربة WPF هنا. |
| LO7B31-08 / fallback-number-failure | `no-explicit-new-flags-after-supplied-number-failure-no-default-claim` | null branch→new→CLR ثانية → إحلال إضافي بعد empty/outer-failure؛شراء يبتلع الرقم وبيع قد يرمي قبل أعلام ISNew التالية؛ توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا. |

## 4. القدرات الست عشرة وثوابتها وخططها — لا ست عشرة موافقة

كل قدرة أدناه محفوظة أيضاً فيFE16/INV16،ولكل منها خطتان متكاملتان مختلفتان في[سجل32](evidence/acceptance-tests-07B31.csv). **كلها not-executed**. السجل يتضمن prerequisites/procedure/criterion/safety/owner/source؛اقترانها بشاهدPython لا ينفذها.

### FE7B31-01 — غياب هدف المشتريات

- **الدخول والمصدر والمخرج:** toolbar next/previous/first/last بعد حارس يسمح → CLR يستبدل الرأس ويمسح _invoiceItems قبل القارئ؛HasRows=false→null→new+CLR ثانية.
- **الحالة والعمق:** `confirmed-source-local`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `P7-161`.
- **المالك والمدخل المنقح:** مالك المنتج وسياسة التنقل ونتيجة التحميل؛ محرر قائم clean وهدف empty مورّد ورجوع عادي للتصفير والترقيم مرتين؛لا SQL فعلي.
- **أثر غياب المدخل:** حد null يخلط غياب الهدف بفشل القراءة؛لا نمنح الأمر إذناً ضمنياً بإنشاء فاتورة جديدة عند الطرف أوالخطأ.
- **الخطوة التالية:** تحديد Found/Empty/Failed/Partial وBoundary بلا تغيير للأصل حتى نجاح التحضير،وفصل قرار ترك المسودة عن صلاحية الهدف.
- **حد الخروج المقترح:** لا يُستبدل المحرر الحالي عند Empty؛نتيجة الطرف ليست أمراً جديداً ضمنياً.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-548;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1531-1587;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-407;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:281-298;SmartAuditERP/Form_WPF/frmInvPurch.xaml:1337-1352;SmartAuditERP/Class/InvoiceOper.cs:3496-3508`؛ `P7B31T-01;P7B31T-02` — **not-executed**.

### FE7B31-02 — غياب هدف البيع

- **الدخول والمصدر والمخرج:** toolbar والتحقق ثم Navigate → CLR يفصل مصدر Grid ويستبدل Invoic؛نتيجة null تعيد new+CLR،ولا rollback للأصل.
- **الحالة والعمق:** `confirmed-source-local`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `P7-161`.
- **المالك والمدخل المنقح:** مالك المنتج وسياسة التنقل ونتيجة التحميل؛ محرر بيع غيرnull وعقد setters/collections سليم ونتيجة header-absent وترقيم طبيعي مورّدان.
- **أثر غياب المدخل:** حد null يخلط غياب الهدف بفشل القراءة؛لا نمنح الأمر إذناً ضمنياً بإنشاء فاتورة جديدة عند الطرف أوالخطأ.
- **الخطوة التالية:** تحديد Found/Empty/Failed/Partial وBoundary بلا تغيير للأصل حتى نجاح التحضير،وفصل قرار ترك المسودة عن صلاحية الهدف.
- **حد الخروج المقترح:** لا يتحول مستند البيع الحالي إلى فاتورة جديدة لمجرد أن مصدر الهدف فارغ.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1679;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2597-2639;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1607-1641;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1605;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:558-570;SmartAuditERP/Form_WPF/frmInvSale.xaml:1220-1234;SmartAuditERP/Class/InvoiceOper.cs:3496-3508`؛ `P7B31T-03;P7B31T-04` — **not-executed**.

### FE7B31-03 — فشل خارجي قبل رأس الهدف

- **الدخول والمصدر والمخرج:** BindingInvoice try/outer-catch → Open/ExecuteReader أوتحويل خارجي إذا فشل إلى outer-catch يضع ref=null؛الأب يعيد CLR.
- **الحالة والعمق:** `confirmed-source-local`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `P7-161`.
- **المالك والمدخل المنقح:** DBA ومالك قارئ المستندات والمزود؛ Failed-before-header نتيجة مورّدة؛لا فشل provider أحدث هنا؛تصفير سابق ولاحِق يرجعان طبيعياً.
- **أثر غياب المدخل:** الاستثناء الخارجي والغياب يلتقيان عند null؛استثناء صف داخلي قد يبقي nonnull،فلا null يقيس الصحة الكاملة ولا المورد جُرب.
- **الخطوة التالية:** توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا.
- **حد الخروج المقترح:** Failed قبل رأس الهدف يحافظ على الأصل ويخرج نتيجة مميزة لا blank-new.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1660;SmartAuditERP/Class/InvoiceOper.cs:3219-3243;SmartAuditERP/Class/InvoiceOper.cs:3496-3508`؛ `P7B31T-05;P7B31T-06` — **not-executed**.

### FE7B31-04 — فشل خارجي بعد بعض الرأس

- **الدخول والمصدر والمخرج:** قارئ mutates ref ثم outer-catch → رأس يكتب على working editor ثم fill/مساعد خارجي قد يرمي؛outer-catch يضع null→fallback.
- **الحالة والعمق:** `confirmed-source-local`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `P7-161`.
- **المالك والمدخل المنقح:** DBA ومالك قارئ المستندات والمزود؛ جزء رأس وouter-failed-after-header مورّدان؛لا نفترض فشل كل helper أوكل تحويل أوصف.
- **أثر غياب المدخل:** الاستثناء الخارجي والغياب يلتقيان عند null؛استثناء صف داخلي قد يبقي nonnull،فلا null يقيس الصحة الكاملة ولا المورد جُرب.
- **الخطوة التالية:** توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا.
- **حد الخروج المقترح:** لا تنشر حقولاً أوتمحُ الأصل عند فشل خارجي متأخر؛التحضير مستقل عن Apply.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1660;SmartAuditERP/Class/InvoiceOper.cs:3237-3277;SmartAuditERP/Class/InvoiceOper.cs:3366-3378;SmartAuditERP/Class/InvoiceOper.cs:3487-3508`؛ `P7B31T-07;P7B31T-08` — **not-executed**.

### FE7B31-05 — ضابط Found غيرnull

- **الدخول والمصدر والمخرج:** فرع Invoic!=null بعد القارئ → الأب يحاول BindingDGV ثم BindingControls؛القارئ يكتب ISNew=false/IsPrinted=true عند رأس found.
- **الحالة والعمق:** `bounded-positive-control-not-hydration-certification`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-02`.
- **المالك والمدخل المنقح:** مالك SDK/DTO وهوية المحرر واكتمال البنود؛ Found على working editor غيرnull مع تفاصيل وSDK/setters مكتملة وفق عقد يورده المالك لاحقاً.
- **أثر غياب المدخل:** إحلال المرجع ثابت محلياً؛اكتمال التحميل ومعاني defaults وملكية النسخ وكل مرجع خارجي لا تثبت من fixture.
- **الخطوة التالية:** تعيين ملكية editor/working-copy/line identity ونتيجة اكتمال مصدرية قبل النقل إلى UI،دون تشغيل SDK أوتحميل DLL.
- **حد الخروج المقترح:** يجب أن يسبق تحقق اكتمال Found النشر؛nonnull وحده ليس فحص صحة.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1660;SmartAuditERP/Class/InvoiceOper.cs:3237-3243`؛ `P7B31T-09;P7B31T-10` — **not-executed**.

### FE7B31-06 — استثناء الصف الداخلي ليس outer-null

- **الدخول والمصدر والمخرج:** catch projectError4 داخل حلقة البنود → قد يتخطى الصف ويستمر؛بعض catch محلية؛لا تعميم كل استثناء إلى ref=null.
- **الحالة والعمق:** `unresolved-completeness-contract-not-new-root`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-02`.
- **المالك والمدخل المنقح:** مالك SDK/DTO وهوية المحرر واكتمال البنود؛ عقد row-level health وpartial/failure مع هوية كل سطر وقرار الرفض/القبول المنقح.
- **أثر غياب المدخل:** إحلال المرجع ثابت محلياً؛اكتمال التحميل ومعاني defaults وملكية النسخ وكل مرجع خارجي لا تثبت من fixture.
- **الخطوة التالية:** تعيين ملكية editor/working-copy/line identity ونتيجة اكتمال مصدرية قبل النقل إلى UI،دون تشغيل SDK أوتحميل DLL.
- **حد الخروج المقترح:** النتيجة الجزئية قابلة للتمييز ولا تقبل لمجرد nonnull؛ليس كل catch واحداً.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Class/InvoiceOper.cs:3374-3385;SmartAuditERP/Class/InvoiceOper.cs:3454-3487`؛ `P7B31T-11;P7B31T-12` — **not-executed**.

### FE7B31-07 — رفض الترك يمنع أول كتابة

- **الدخول والمصدر والمخرج:** CheckBeforeClear وMessageBoxResult.No → أوامر toolbar الثمانية تحترم No؛لا CLR أوBindingInvoice عند الرفض.
- **الحالة والعمق:** `bounded-negative-control-existing-guard`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-03`.
- **المالك والمدخل المنقح:** مالك WPF والأوامر وحارس ترك المستند؛ أعلام updated أوnew مع count يحقق الشرط،وقرار No صريح مورّد؛لا تعامل GUI أوplaceholder كتجربة.
- **أثر غياب المدخل:** No ضابط يمنع أول كتابة؛وجود الحارس لا يجعل قراءة الهدف ناجحة ولا يغطي بقية الأوامر أوdirty propagation.
- **الخطوة التالية:** تتبع أول كتابة لكل أمر مختار وبقية caller في شريحة7B صريحة،ووضع No قبل reset وحفظ الأصل حتى اعتماد الهدف.
- **حد الخروج المقترح:** No يوقف الأمر قبل أول تخصيص أوclear أوطلب قراءة،ولا تُورّد نتائج لمسار غير واصل.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:504-546;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1571-1587;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1662-1679;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2597-2639`؛ `P7B31T-13;P7B31T-14` — **not-executed**.

### FE7B31-08 — Yes وclean منفصلان عن صحة التحميل

- **الدخول والمصدر والمخرج:** حارس يسمح ثم ReaderOutcome → الحارس قرار ترك لا دليل target؛clean لا يسأل أصلاً ولا يحمي من Empty/Failed.
- **الحالة والعمق:** `policy-and-load-health-boundary`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-01`.
- **المالك والمدخل المنقح:** مالك المنتج وسياسة التنقل ونتيجة التحميل؛ مصفوفة clean/new/updated وYes/No وحدود dirty مع Found/Empty/Failed/Partial منقحة.
- **أثر غياب المدخل:** حد null يخلط غياب الهدف بفشل القراءة؛لا نمنح الأمر إذناً ضمنياً بإنشاء فاتورة جديدة عند الطرف أوالخطأ.
- **الخطوة التالية:** تحديد Found/Empty/Failed/Partial وBoundary بلا تغيير للأصل حتى نجاح التحضير،وفصل قرار ترك المسودة عن صلاحية الهدف.
- **حد الخروج المقترح:** سماح الحارس لا يحوّل Empty/Failed إلى Found،ولا يخلط AbandonDecision بنتيجة التحميل.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1571-1587;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1679`؛ `P7B31T-15;P7B31T-16` — **not-executed**.

### FE7B31-09 — فشل أول ترقيم في CLR المشتريات

- **الدخول والمصدر والمخرج:** CLR try يحتوي allocation/clear/ResetInvoice → قد يبتلع فشل LoadInvNo بعد إحلال المرجع ثم يستمر إلى القارئ؛ليس rollback.
- **الحالة والعمق:** `supplied-dependency-failure-boundary`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-05`.
- **المالك والمدخل المنقح:** مالك WPF والتصفير والربط والأحداث؛ فشل مورّد AT number بعد تمام التعيينات السابقة؛لا فشل provider أوsetter مرصود.
- **أثر غياب المدخل:** LoadInvNo يسبق أعلام reset؛شراء يبتلع فشله داخل CLR وبيع قد يخرجه؛لا اعتمادية أحداث أوإعادة دخول مفترضة.
- **الخطوة التالية:** فصل تحضير رقم وحالة جديدة عن نشرها؛توثيق أخطاء CLR والربط حسب عقد الأحداث دون إصلاح أوتجربة WPF هنا.
- **حد الخروج المقترح:** فشل تحضير الرقم لا يترك مرجعاً منشوراً بغير health ولا يمحو الأصل.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1531-1568;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-389;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:281-298;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502`؛ `P7B31T-17;P7B31T-18` — **not-executed**.

### FE7B31-10 — فشل أول ترقيم في CLR البيع

- **الدخول والمصدر والمخرج:** ResetInvoice خارج catch المحلي → قد يخرج فشل الرقم بعد unbind/new وقبل BindingInvoice؛لا يصح ادعاء fallback أوقراءة لكل طريق.
- **الحالة والعمق:** `supplied-early-stop-counter-control`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-05`.
- **المالك والمدخل المنقح:** مالك WPF والتصفير والربط والأحداث؛ فشل أول رقم مورّد مع عودة setters السابقة طبيعياً؛لا مدخل reader لمسار لا يصله التنفيذ.
- **أثر غياب المدخل:** LoadInvNo يسبق أعلام reset؛شراء يبتلع فشله داخل CLR وبيع قد يخرجه؛لا اعتمادية أحداث أوإعادة دخول مفترضة.
- **الخطوة التالية:** فصل تحضير رقم وحالة جديدة عن نشرها؛توثيق أخطاء CLR والربط حسب عقد الأحداث دون إصلاح أوتجربة WPF هنا.
- **حد الخروج المقترح:** موضع الفشل قبل القارئ وبعد أول كتابة معلن،ويحفظ التصميم المقترح الأصل دون نشر جزئي.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1607-1660;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1595;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:558-570`؛ `P7B31T-19;P7B31T-20` — **not-executed**.

### FE7B31-11 — فشل رقم fallback

- **الدخول والمصدر والمخرج:** null branch→new→CLR ثانية → إحلال إضافي بعد empty/outer-failure؛شراء يبتلع الرقم وبيع قد يرمي قبل أعلام ISNew التالية.
- **الحالة والعمق:** `supplied-fallback-failure-boundary`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-04`.
- **المالك والمدخل المنقح:** DBA ومالك قارئ المستندات والمزود؛ الرقم الأول طبيعي والثاني يفشل AT الحد؛لا defaults لأعلام الكائن بعد الإنشاء ولا UI نهائية.
- **أثر غياب المدخل:** الاستثناء الخارجي والغياب يلتقيان عند null؛استثناء صف داخلي قد يبقي nonnull،فلا null يقيس الصحة الكاملة ولا المورد جُرب.
- **الخطوة التالية:** توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا.
- **حد الخروج المقترح:** لا يعتمد المستهلك أن أعلام الجديد وصلت عند فشل الرقم؛الأصل محفوظ حتى نتيجة نجاح صريحة.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1531-1568;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1607-1660`؛ `P7B31T-21;P7B31T-22` — **not-executed**.

### FE7B31-12 — مرشح الرقم ليس حجزاً

- **الدخول والمصدر والمخرج:** LoadInvNo→InvoiceNo MAX+1 → النداءان ممكنان عند Empty مع reset طبيعي؛لا transaction أوreservation في المساعد المحدود.
- **الحالة والعمق:** `source-number-boundary-not-new-concurrency-root`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-04`.
- **المالك والمدخل المنقح:** DBA ومالك قارئ المستندات والمزود؛ قاموس candidate/reservation/GlobalID وسياسة الرقم عند new فقط،مع أمثلة اصطناعية؛P3-005 يبقىpotential.
- **أثر غياب المدخل:** الاستثناء الخارجي والغياب يلتقيان عند null؛استثناء صف داخلي قد يبقي nonnull،فلا null يقيس الصحة الكاملة ولا المورد جُرب.
- **الخطوة التالية:** توثيق نتيجة header/detail والفشل بعقد مصدر منقح وتجهيز مصدر اصطناعي معزول للقبول المأذون لاحقاً؛لا اتصال هنا.
- **حد الخروج المقترح:** عدد قراءات المرشح ليس إنشاء مستند أوحجزاً أوتصادماً مثبتاً أوGlobalID جديداً.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:281-298;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:558-570;SmartAuditERP/Class/InvoiceOper.cs:2789-2808`؛ `P7B31T-23;P7B31T-24` — **not-executed**.

### FE7B31-13 — هوية cursor لها مصدر id فعلاً

- **الدخول والمصدر والمخرج:** BindingControls txtNo←InvoiceNo وreader InvoiceNo←id → مقارنة next/previous بـid لا تثبت خلط مجالين لمجرد اسم InvoiceNo؛رفض lead غير مسند.
- **الحالة والعمق:** `counter-hypothesis-rejected-not-new-root`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-02`.
- **المالك والمدخل المنقح:** مالك SDK/DTO وهوية المحرر واكتمال البنود؛ DocumentRef منقح يشمل branch/type/proc/id/global-id ولقطة cursor؛لا افتراض تعارض id وInvoiceNo بالاسم.
- **أثر غياب المدخل:** إحلال المرجع ثابت محلياً؛اكتمال التحميل ومعاني defaults وملكية النسخ وكل مرجع خارجي لا تثبت من fixture.
- **الخطوة التالية:** تعيين ملكية editor/working-copy/line identity ونتيجة اكتمال مصدرية قبل النقل إلى UI،دون تشغيل SDK أوتحميل DLL.
- **حد الخروج المقترح:** الهوية تُتبع من الحقل المصدر لا اسم الخاصية؛ترتيب id وحده ليس نتيجة جديدة هنا.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:445-475;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:513-537;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1447-1467;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2615-2639;SmartAuditERP/Class/InvoiceOper.cs:3271-3285`؛ `P7B31T-25;P7B31T-26` — **not-executed**.

### FE7B31-14 — LoadOutcome والنسخة المستقلة

- **الدخول والمصدر والمخرج:** عقد المصدر/النتيجة/النشر المقترح غير المنفذ → void+ref وnull يخلطان Empty/Failed،وnonnull لا يثبت completeness؛لا Apply قبل resolve.
- **الحالة والعمق:** `proposed-contract-not-implemented`؛ bounded-toolbar-reset-and-whole-local-reader-method-not-whole-files-or-runtime؛ root/handoff: `H7B31-01`.
- **المالك والمدخل المنقح:** مالك المنتج وسياسة التنقل ونتيجة التحميل؛ NavigationRequest/DocumentRef وFound/Empty/Failed/Partial ونسخة مستقلة وعقد retry قبل أي إصلاح مأذون.
- **أثر غياب المدخل:** حد null يخلط غياب الهدف بفشل القراءة؛لا نمنح الأمر إذناً ضمنياً بإنشاء فاتورة جديدة عند الطرف أوالخطأ.
- **الخطوة التالية:** تحديد Found/Empty/Failed/Partial وBoundary بلا تغيير للأصل حتى نجاح التحضير،وفصل قرار ترك المسودة عن صلاحية الهدف.
- **حد الخروج المقترح:** resolve/validate في نسخة مستقلة،ثم قرار ترك وApply واحد عند Found المكتمل فقط.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `SmartAuditERP/Class/InvoiceOper.cs:3219-3243;SmartAuditERP/Class/InvoiceOper.cs:3476-3508;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-502;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1660`؛ `P7B31T-27;P7B31T-28` — **not-executed**.

### FE7B31-15 — حفظ الحالة التاريخية للمدقق

- **الدخول والمصدر والمخرج:** OWN332/raw333CRLF/indexes/presetB30/ALL52 → 111 مدخل source assertions تاريخية وdispatcher TEXT؛115 أداة تنفيذ حالية تفحص مستقلاً.
- **الحالة والعمق:** `documentary-historical-input-contract`؛ documentary-contract-not-application-body؛ root/handoff: `H7B31-06`.
- **المالك والمدخل المنقح:** مالك نطاق التدقيق والتوثيق والتسليم؛ 900 مادة محمية و3تجميدات ولقطةdispatcher إضافية؛ALL986 السابقة دون skip أوتعديل أوoverlay.
- **أثر غياب المدخل:** خمسة مسارات متقاطعة واتحاد427 لا حصر قدرات أو400 مهمةC؛نجاح مدقق الوثائق والدفع لا يثبت بدء الإصلاح أوتزامنه.
- **الخطوة التالية:** اختيار R4p/7B32 أوsplit مسبب منSP01–03 مع مالك ومدخل ومخرج وخروج وتسليم SHA تدقيق محدد للإصلاح المستقل.
- **حد الخروج المقترح:** كل332 قاموساً وبادئةraw333/G240 والمدخلات المحمية exact،وكل52B30 تعمل دون تعديل.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `none-documentary-metadata`؛ `P7B31T-29;P7B31T-30` — **not-executed**.

### FE7B31-16 — حد النطاق والتسليم والإصلاح المستقل

- **الدخول والمصدر والمخرج:** SP01 وSP02 وSP03 وRS14 → 5مسارات كلها تقاطع→427؛14شريحة/0ملف كامل،method290لاكلSDK أوcaller/feature؛7Cلمتبدأ.
- **الحالة والعمق:** `documentary-boundary-not-coverage-or-approval`؛ documentary-contract-not-application-body؛ root/handoff: `H7B31-06`.
- **المالك والمدخل المنقح:** مالك نطاق التدقيق والتوثيق والتسليم؛ حصر entry/source/output وcrosswalk455FE والدفاتر القديمة NL8/LO8 وحدود الاستثناءوالخطوةوالمالك والمدخل.
- **أثر غياب المدخل:** خمسة مسارات متقاطعة واتحاد427 لا حصر قدرات أو400 مهمةC؛نجاح مدقق الوثائق والدفع لا يثبت بدء الإصلاح أوتزامنه.
- **الخطوة التالية:** اختيار R4p/7B32 أوsplit مسبب منSP01–03 مع مالك ومدخل ومخرج وخروج وتسليم SHA تدقيق محدد للإصلاح المستقل.
- **حد الخروج المقترح:** لا تحول اتحاد المسارات أوحالات الوثائق إلى نسبة قدرات أوإتمام7B أوإذن8 أوتزامن الإصلاح.
- **حد الإثبات:** عينة ساكنة؛الاعتماديات ونتيجة القارئ/الرقم مورّدة،لا defaults أوhydration أوأحداث مستقرة أوفشل provider أوحفظ/خسارة مرصودة.
- **الدليل والخطط:** `none-documentary-metadata`؛ `P7B31T-31;P7B31T-32` — **not-executed**.

## 5. مصالحة المصدر والنتيجة RC6

- **RC7B31-01 — الرجوع الفارغ والفشل:** `FE7B31-01;FE7B31-02;FE7B31-03;FE7B31-04`؛ لا يُستبدل المحرر الحالي عند Empty؛نتيجة الطرف ليست أمراً جديداً ضمنياً. ؛ لا يتحول مستند البيع الحالي إلى فاتورة جديدة لمجرد أن مصدر الهدف فارغ. ؛ Failed قبل رأس الهدف يحافظ على الأصل ويخرج نتيجة مميزة لا blank-new. ؛ لا تنشر حقولاً أوتمحُ الأصل عند فشل خارجي متأخر؛التحضير مستقل عن Apply. حد:مصدر ونتيجة ونشر محدودة لا قبول ERP أوكلcaller أوSDK؛32 خطة تبقى not-executed.

- **RC7B31-02 — nonnull والاكتمال:** `FE7B31-05;FE7B31-06;FE7B31-13`؛ يجب أن يسبق تحقق اكتمال Found النشر؛nonnull وحده ليس فحص صحة. ؛ النتيجة الجزئية قابلة للتمييز ولا تقبل لمجرد nonnull؛ليس كل catch واحداً. ؛ الهوية تُتبع من الحقل المصدر لا اسم الخاصية؛ترتيب id وحده ليس نتيجة جديدة هنا. حد:مصدر ونتيجة ونشر محدودة لا قبول ERP أوكلcaller أوSDK؛32 خطة تبقى not-executed.

- **RC7B31-03 — حارس الترك وصحة الهدف:** `FE7B31-07;FE7B31-08`؛ No يوقف الأمر قبل أول تخصيص أوclear أوطلب قراءة،ولا تُورّد نتائج لمسار غير واصل. ؛ سماح الحارس لا يحوّل Empty/Failed إلى Found،ولا يخلط AbandonDecision بنتيجة التحميل. حد:مصدر ونتيجة ونشر محدودة لا قبول ERP أوكلcaller أوSDK؛32 خطة تبقى not-executed.

- **RC7B31-04 — تبعيات التصفير والترقيم:** `FE7B31-09;FE7B31-10;FE7B31-11;FE7B31-12;FE7B31-14`؛ فشل تحضير الرقم لا يترك مرجعاً منشوراً بغير health ولا يمحو الأصل. ؛ موضع الفشل قبل القارئ وبعد أول كتابة معلن،ويحفظ التصميم المقترح الأصل دون نشر جزئي. ؛ لا يعتمد المستهلك أن أعلام الجديد وصلت عند فشل الرقم؛الأصل محفوظ حتى نتيجة نجاح صريحة. ؛ عدد قراءات المرشح ليس إنشاء مستند أوحجزاً أوتصادماً مثبتاً أوGlobalID جديداً. ؛ resolve/validate في نسخة مستقلة،ثم قرار ترك وApply واحد عند Found المكتمل فقط. حد:مصدر ونتيجة ونشر محدودة لا قبول ERP أوكلcaller أوSDK؛32 خطة تبقى not-executed.

- **RC7B31-05 — المدخل التاريخي:** `FE7B31-15`؛ كل332 قاموساً وبادئةraw333/G240 والمدخلات المحمية exact،وكل52B30 تعمل دون تعديل. حد:مصدر ونتيجة ونشر محدودة لا قبول ERP أوكلcaller أوSDK؛32 خطة تبقى not-executed.

- **RC7B31-06 — حد النطاق والإذن:** `FE7B31-16`؛ لا تحول اتحاد المسارات أوحالات الوثائق إلى نسبة قدرات أوإتمام7B أوإذن8 أوتزامن الإصلاح. حد:مصدر ونتيجة ونشر محدودة لا قبول ERP أوكلcaller أوSDK؛32 خطة تبقى not-executed.

## 6. ما لا يحسمه العقد المحلي

تبقى بقية callers/dialogs/editors/fields/writers/output وDocumentRef/allowed-set/branch/reset/dirty/cancel/failure وProduct/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome ضمن **SP01 و7B**. يبقى **SP02** حصر entry/source/output وcrosswalk455FE والدفاتر اللاحقة،و**SP03** SDK/DTO/constructors/collections/currency/precision/words/legacy/templates والسياسات ضمن7B صراحة؛لا نقل غير المراجع إلى7C.

اختر R4p/7B32 أوsplit مسبباً بقدرة ومدخل ومصدر ومخرج واستبعاد ودليل وحد ومالك ومدخل منقح وأثر وخطوة وخروج. لا وعد مدة أوجلسات أوآخر جزء أوإتمام النظام. يسلم SHA تدقيق مدفوع محدد للإصلاح المستقل،دون افتراض بدئه أوتزامنه أودمج تعديلاته هنا.

تبقى **P4-014 وP7-132 وP7-145 potential**،و020/021 وحواجز المال وACL والمخزون والحفظ والإنتاج دون تغيير. تصحيح B10 الإضافي:10 محلياً مقابل120 مرجعياً وضابط equality1=10،دون إعادة تحريرG138. لا ERP/build/C#/VB/.NET/WPF/SQL/DataView/provider/SDK/REPX/ToDataTable أوطابعة وماسح أوبيانات أعمال وأسرار أوإصلاح وقياس وقبول تشغيلي نُفذ هنا.

[NL8](evidence/navigation-load-lineage-07B31.csv) · [LO8](evidence/reader-outcome-lineage-07B31.csv) · [FE16](evidence/feature-implementation-matrix-07B31.csv) · [INV16](evidence/report-invariants-07B31.csv) · [32 خطة](evidence/acceptance-tests-07B31.csv) · [RC6](evidence/report-reconciliation-07B31.csv) · [AD8](evidence/root-adjudication-07B31.csv) · [امتدادات0](evidence/historical-extensions-07B31.csv) · [شاهد20+20](evidence/navigation-load-witnesses-07B31.json) · [RS14](evidence/residual-disposition-07B31.csv) · [SP3](evidence/split-register-07B31.csv) · [H6](evidence/handoffs-07B31.csv) · [Q6](evidence/questions-07B31.csv) · [workplan10](evidence/remaining-workplan-07B31.csv) · [backlog10](evidence/continuation-backlog-07B31.csv)
