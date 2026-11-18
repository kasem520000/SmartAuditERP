# الجزء7B10 — تقرير المندوبين وعقود أرباح الأصناف وحركة المبيعات

**مرجع التدقيق المعلن:** 2026-11-16 UTC. مصدر التطبيق الأصلي `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. **7B10 تسليم ساكن جزئي؛ 7B و7 غير مكتملتين. 7B11 معلنة للباقي، و7C لم تبدأ، والمرحلة8 غير مأذونة ولم تبدأ.** استمرار التدقيق ودفع توثيقه ليسا إذن إصلاح أو بناء أو تشغيل أو قياس أو قبول ERP.

**دفع7B9 مكتمل سابقاً، وليس معلقاً:** جميع ملفات التدقيق الـ297 دُفعت إلى `a2541ed204e62493f93cfb811ba5f81ad3206942` قبل هذا الجزء. عند استئناف البيئة كانت الوثائق نفسها غير متتبعة فوق checkout10ba؛ طوبقت كامل297 بايتياً مع الدفع الموجود ثم قُدّم الفرع الحالي fast-forward إلى a254، دون التزام/دفع جديد أو reset/rebase أو إعادة بناء للأرشيف. مصدر التطبيق827 مساراً وبصماتها لم يتغير. [provenanceB10](evidence/provenance-07B10.json) تفصل هذه المشاهدة عن المصدر10ba وعن checksB9 عند checkout3612700 وchecksB8 عند checkout10ba؛ لا إعادة كتابة stdout قديم لتوحيد metadata مع اليوم.

## 1. الحصيلة وحدود التفسير

قُرئت الأجسام وواجهات XAML المحلية كاملة لـ`frmInvBySalesMen` و`frmRptItemsProfit` و`frmRptSalesInPeriod`، وDTOs الثلاثة، مع دعم منتقى من المداخل والطفل والكاتب والمخطط والتفويض. **الأرباح وحركة الفترة سبق تدقيقهما في7B1**؛ الجديد استكمال عقد المندوبين ومصالحة الوحدة/الهوية/المصدر، لا العثور مجدداً على العيب نفسه أو إعادة تسمية نتائجه.

| المقياس | الحصيلة المحدودة |
| --- | --- |
| الجديد | P7-111 وP7-112 وP7-113:ثلاث متوسطة، confirmed كتعارضات تنفيذ محلية بشروطها؛ مفتوحة دون معالجة. |
| السابق | 13 امتداداً لأصولها مع حفظ282 core وكل next_phase؛ إعادة قراءة أرباح/حركة الفترة لا تعيد عد نتائج7B1. |
| التراكمي | 285 مفتوحة:2 حرجة/175 عالية/107 متوسطة/1 منخفضة؛248 confirmed/30 potential/7 repository-gap. |
| النطاق | 23 مساراً:17 متداخلة مع375 و6 جديدة؛ اتحاد381 ومكمل446 inventory-only، فضلاً عن مقاطع غير مختارة داخل381. |
| الأجسام المحلية | 2162 سطراً C# و1864 XAML=4026 للثلاثة، و96 سطر DTO إضافية؛ لا كل caller/child/template/schema/ACL/نشر. |
| المصفوفة | 23 صف FE و23 ثابت INV و6 عقود RC و6 H و6 Q و10 مجموعات استمرار؛ ليست أعداد ميزات مغلقة. |
| القبول | 26 خطة not-executed:6 مباشرة للجديد+13 انحدار أصل+5 عقود+2 بوابة. |
| فحوص الوثائق | 20 نموذجاً يدوياً و20 ملاحظة مصدر نصية محدودة و28 حالة مدقق اصطناعية جديدة؛ لا ERP أو SQL/WPF/Office. |

**السبب قبل النتيجة:** btnShow للمندوبين يستدعي قارئي الفواتير والسندات داخل Task.Run، ثم يقرؤون عناصر WPF مباشرة. بوابةP7-054 سابقة لأي ادعاء تحميل وحساب ناجحين. الأمثلة العددية أدناه تعزل بوابة الخيط بصفوف/معايير صالحة يدوياً، ولا تفترض أنها عولجت أو أن المسار العادي وصل إليها. كذلك اختلاف Notes/CreditDeptNotes محلي مؤكد، أما وجود view/synonym متوافقة في النشر فلم يفحص؛ يلزم حسمه قبل ادعاء فشل نشر أو تلوث بيانات الإشعارات.

## حفظ المصدر والتاريخ

- لقطة الدخول أنشئت **مرة واحدة**: [frozen282](evidence/findings-through-07B9.csv)، SHA256=`7b85f5eeb359220a53d93085dcf0d18d700ba4a965b9b3156171e819e7979d19`؛ [فهارسB9 الدقيقة](evidence/shared-indexes-through-07B9.json)، SHA256=`8d3ae3f18066925b56af0747d9475f9ac2883c0ad072805f833ea613e3e65475`. لا تهيئة ثانية أو rebaseline.
- تحمي [provenance292](evidence/provenance-07B10.json) **292 وثيقة/أداة/جدولاً/خرجاً تاريخياً**. الملفات القديمة الحية الخمسة المسموح بتطورها فقط:README وPLAN وIMPROVEMENTS وfindings وvalidate_audit. باقي التقارير والأدوات وchecks محفوظة حرفياً.
- **أول282 نتيجة:كل الحقول غير الدليل، وكل next_phase دون استثناء، وبادئات الدليل الأصلية محفوظة**؛ تضاف13 ذيلاً معلناً فقط. لا إعادة تصنيف أو إغلاق أو إعادة جدولة خفية. السجل الحي CRLF، وG01–134 صفوف توصية محفوظة حرفياً؛ تضافG135–140 لا ست نتائج أخرى.
- [checksB9 الحقيقي](evidence/checks-07B9.json) يبقى SHA256=`fbd73a272131261240ab7fb29270b45642c314538c55e04301db0e6905996e91`. يعطى helperB9 **frozen282 وفهارسه الدقيقة عند مساراتها المنطقية الأصلية في الذاكرة** لا285 أو الفهارس الحية، دون تعديل helper محمي. الأجزاء الأسبق بمدخلاتها الخاصة أيضاً. مقاييس الإعادة الحالية ليست byte-replay للأرشيف.
- هوية827 path/hash مستقلة عن ancestry وصافي دلتا Git المحصور في docs/audit؛ هذه ليست شهادة كل تاريخ وسيط أو توقيعاً أو إذن تشغيل. ساعة البيئة المشاهدة عند الدخول `2026-11-18T08:06:51.954013+00:00` سجل منفصل عن مرجع التدقيق16نوفمبر وعن تاريخ الأرشيف، وليست تاريخ قبول تطبيق.

## النطاق المقروء وحدوده

| المسار | الأسطر المختارة | حد القراءة |
| --- | --- | --- |
| `SmartAuditERP/Class/InvoiceOper.cs` | `1548-1564;1582-1620;4289-4316` | كاتب علم VAT وكميات/تكلفة البند و binder تكلفة فقط؛ لا كل حفظ/GL. |
| `SmartAuditERP/Class/ItemOper.cs` | `154-183;196-211;1390-1407` | عقد تكلفة الأساس وكمية الإدخال ووحدة العبوة؛ لا كل تسعير/تقريب. |
| `SmartAuditERP/Class/MainClass.cs` | `45-49;418-455` | مصنع اتصال وحارس visual-tree بالاسم فقط؛ لا كل جلسة/موارد/تفويض. |
| `SmartAuditERP/Class_WPF/ItemProfitRow.cs` | `1-35` | DTO الأرباح؛ إعادة قراءة عقد معروف لا ميزة جديدة. |
| `SmartAuditERP/Class_WPF/SaleItemRow.cs` | `1-33` | DTO تبويبي الفترة؛ IsPostpone مطابق للـ XAML. |
| `SmartAuditERP/Class_WPF/SalesManRowItem.cs` | `1-28` | DTO المندوب والاتجاه/فقد GlobalID فقط؛ ليس snapshot عمولة. |
| `SmartAuditERP/Form_WPF/frmDebtNote.xaml.cs` | `210-268;670-709` | قراءة أول إشعار وكاتب CreditDeptNotes فقط؛ لا كل الترحيل أو الحذف/ACL. |
| `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml` | `1-654` | جسم/XAML محلي كامل فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول. أرباح/حركة الفترة لهما 7B1 سابقة فلا يعاد عدها. |
| `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs` | `1-859` | جسم/XAML محلي كامل فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول. أرباح/حركة الفترة لهما 7B1 سابقة فلا يعاد عدها. |
| `SmartAuditERP/Form_WPF/frmItemsDetails.xaml` | `1-16` | وصل Loaded فقط؛ لا كل XAML/إتاحة. |
| `SmartAuditERP/Form_WPF/frmItemsDetails.xaml.cs` | `25-101` | هوية SelectedId وLoaded واستعلام التفاصيل فقط؛ لا طفل كامل أو أداء. |
| `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml` | `1-644` | جسم/XAML محلي كامل فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول. أرباح/حركة الفترة لهما 7B1 سابقة فلا يعاد عدها. |
| `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs` | `1-715` | جسم/XAML محلي كامل فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول. أرباح/حركة الفترة لهما 7B1 سابقة فلا يعاد عدها. |
| `SmartAuditERP/Form_WPF/frmRptSalesInPeriod.xaml` | `1-566` | جسم/XAML محلي كامل فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول. أرباح/حركة الفترة لهما 7B1 سابقة فلا يعاد عدها. |
| `SmartAuditERP/Form_WPF/frmRptSalesInPeriod.xaml.cs` | `1-588` | جسم/XAML محلي كامل فقط؛ لا كل caller/child/template/schema/ACL/نشر/قبول. أرباح/حركة الفترة لهما 7B1 سابقة فلا يعاد عدها. |
| `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs` | `473-534` | Navigate وأول صف وهوية الفاتورة فقط؛ لا كل المحرر/الحفظ. |
| `SmartAuditERP/Form_WPF/frmSalesMen.xaml` | `212-225;272-277` | حقول العمولة وزر المدخل فقط؛ لا UI/صلاحيات كاملة. |
| `SmartAuditERP/Form_WPF/frmSalesMen.xaml.cs` | `157-180;269-280` | كاتب نسب العمولات ومدخل تقرير المندوبين فقط، لا البحث/الحذف/كل الشاشة. |
| `SmartAuditERP/Form_WPF/frmSandQ.xaml.cs` | `624-698;891-939` | Navigate/ReadData وعقد Payment/VAT/NetVal/branch فقط؛ لا كل سند5 أوGL. |
| `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs` | `618-680;928-965` | Navigate/ReadData وعقد Receipt7/branch/NetVal فقط؛ لا كل سند7 أوGL. |
| `SmartAuditERP/Home.xaml` | `482-490` | القوائم وحالة تعطيل حركة الفترة؛ لا صلاحية نشر. |
| `SmartAuditERP/Home.xaml.cs` | `3542-3544;3604-3611` | مداخل new reports وApply قبل Show لحركة الفترة فقط؛ لا كل Home/ACL. |
| `SmartAuditERP/Properties/Resources.resx` | `954-1017;1023-1058;1366-1387;1496-1532;1807-1818` | DDL محلي Inv/Inv_Sub/الإشعار/Receipts/salesmen فقط؛ لا كل 144533 سطر أو schema نشر/alias. |

[scope23](review-scope-07B10.csv)، [ledger827](evidence/coverage-ledger-07B10.csv)، [filename98](evidence/report-candidate-disposition-07B10.csv) و[screens52](evidence/report-screen-disposition-07B10.csv) حصر وتتبع لا نسب اكتمال. المسارات الستة الجديدة:DTO المندوب وXAML المندوب وبدن/XAML تفاصيل الصنف وبدن/XAML المندوبين التعريفيين؛ نطاق الأخيرة مقاطع فقط ولو قرئ جسمها استكشافياً. ظهور الطفل أو ذكر helper لا يمنحه تغطية أبيه.98/52 مرشحان اسميان وليسا عدد ميزات مكتملة.

## 2. النتائج الجديدة

### P7-111 — إجمالي قيمة تقرير المندوبين يجمع المرتجع والإشعار كقيم موجبة خلاف إشارة العمولة

**الخطورة:** متوسطة؛ **الإثبات:** `confirmed` محلياً؛ `open-not-remediated`؛ `next_phase=8` تخطيط لا إذن.

يعين التقرير IsPlus=-1 للمرتجع والإشعار، لكنه يحتفظ بمقدار Value موجباً. RecalculateSummary يجمع `sumVal += row.Value` بلا اتجاه، بينما يطرح العمولات للصف السالب. صف إجمالي XLSX يكرر `items.Sum(x => x.Value)`؛ ليست الملاحظة مجرد فقد خاصية في جسر طباعة خارجي.

بيع100 ومرتجع40 وإشعار10 يعطي150 لقيمة الحركة المطلقة، مقابل50 عند تطبيق الإشارة. عمولات10/4/1 تجمع إلى5 فعلاً. **gross movement قد يكون مقياساً مشروعاً إن سمي صراحة**؛ التعارض المؤكد هنا عدم اتساق اتجاه Value مع اتجاه الصف/العمولة في إجمالي غير مفصول، وليس إثبات خسارة أو صافي نقد أو تسويةGL.

**الأثر وحده:** قد يقرأ المستهلك إجمالي الحركة الموجب كصافي مبيعات/قيمة، بخلاف مجاميع العمولات الموقعة. لا نثبت ملفاً صدر أو مبلغاً مرحلاً؛ بوابةworker السابقة قائمة.

**المقترح غير المنفذ:** عقد مقياس صريح يفصل gross عن net ويطبق الإشارة مرة واحدة في نموذج مشترك للعرض وDTO والملف، مع تسميات تمنع اعتبار جمع البيع والقبض صافي نقد أوGL.

**التحقق اللاحق:** P7B10T-01 وP7B10T-02؛ بيع فقط شاهد مقابل، ومرتجع فقط واختلاط الإشعار وسياسة gross/net. كلاهما not-executed.

**الدليل:** `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:279-290`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:309-343`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:375-398`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:482-510`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:781-796`؛ `SmartAuditERP/Class_WPF/SalesManRowItem.cs:10-24`.

### P7-112 — خيار كل الفترة في تقرير المندوبين يوسع الفواتير وحدها ويبقي السندات مقيدة بالتاريخ

**الخطورة:** متوسطة؛ **الإثبات:** `confirmed` محلياً؛ `open-not-remediated`؛ `next_phase=8` تخطيط لا إذن.

عند `chkAllPeriod=true` يحذف ShowInvoiceResults شرط التاريخ عن Inv وحده. الطلب نفسه يستدعي LoadClientReceiptVouchers وLoadGeneralReceiptVouchers؛ LoadReceiptsByType يضيف دائماً `ReceiptDate >= @date1` و`<= @date2` ولا يقرأ خيار كل الفترة. تواريخ التحكم تهيأ إلى اليوم، وXAML يبدأ كل الفترة مفعلاً والتواريخ معطلة؛ كما يمكن أن تبقى فترة اختيرت سابقاً.

**هذا اختلاف عضوية بين مصدرين في الطلب نفسه**:فواتير كل الزمن مع سندات5/7 من اليوم/الفترة الباقية. لا يتطلب تغيير المعايير بعد العرض ولا فشل parse، ولا يحل بتصحيح شمول منتصف اليوم التالي وحده.

**الأثر وحده:** تقرير واحد ومجموع عمولات مصدره فترات غير متجانسة إذا وصلت إليه صفوف سليمة بعد بوابةworker. لا ادعاء واقعة عرض/ERP ناجحة أو فرع مفوض من المثال.

**المقترح غير المنفذ:** DTO طلب immutable واحدة تحمل all-period أو[from,toExclusive) مع تحقق المجال؛ يطبقها كل مصدر مع BranchScope مفوض وتصل دلالتها إلى المخرج.

**التحقق اللاحق:** P7B10T-03 وP7B10T-04؛ بيانات قديمة وحديثة للفواتير ولكل نوع سند، وفترة محددة كشاهد، ثم تبديل الخيار. كلاهما not-executed.

**الدليل:** `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:56-64`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:158-166`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:181-218`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:401-439`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:824-830`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml:282-309`.

### P7-113 — قارئ إشعارات المندوبين يطلب Notes خلاف كاتب ومخطط CreditDeptNotes المرفقين

**الخطورة:** متوسطة؛ **الإثبات:** `confirmed` محلياً؛ `open-not-remediated`؛ `next_phase=8` تخطيط لا إذن.

LoadCreditNotes وتنقل صف الإشعار يطلبان `FROM Notes`، بينما محرر الإشعار المحدد يكتب `INSERT/UPDATE CreditDeptNotes` وDDL المرفق المقروء يعرف CreditDeptNotes. catch التحميل يتجاهل الخطأ.

**المؤكد هو عدم تطابق عقدي القارئ والكاتب/DDL المحليين**. إذا لم توجد مطابقة خارجية متوافقة فقد يفشل التحميل صامتاً ويفشل التنقل إلى كيان الكاتب. لم تفحص قاعدة نشر أو view/synonym؛ لا ننفي وجودها من بحث مستودع ولا نسجل خطأSQL منفذاً. بوابةworker سابقة، ثم توافق الاسم، ثم حبيبة الإشعار وهويته وحذفه وفرعه وتاريخه.

**الأثر وحده:** إتاحة الإشعارات والتنقل إليها غير موثوقين على العقد المرفق بلا توافق معتمد. الفشل الصامت يمتد تحتP7-046؛ لا نتيجة جديدة لكلcatch أو ادعاء صفوف محذوفة/عابرة للفروع قبل حسم البوابات.

**المقترح غير المنفذ:** عقد اسم/إصدار وهوية واحد أو compatibility mapping موثقة ومختبرة ببدائل؛ blocked/error معلن عند عدم التوافق. لا تصنيع جدولNotes فارغ أوview تخمينية لإخفاء السبب.

**التحقق اللاحق:** P7B10T-05 وP7B10T-06؛ عدم مطابقة مخطط اختباري ومطابقة خارجية افتراضية مشروطة ثم بوابات الهوية/الحذف/التاريخ. كلاهما not-executed.

**الدليل:** `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:351-359`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:375-398`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:558-566`؛ `SmartAuditERP/Form_WPF/frmDebtNote.xaml.cs:670-709`؛ `SmartAuditERP/Properties/Resources.resx:1366-1387`.

## 3. الامتدادات المعلنة — لا إعادة ترقيم

| الامتداد | الأصل | الملاحظة وحدودها | العقد/المقترح غير المنفذ | الدليل |
| --- | --- | --- | --- | --- |
| EX7B10-01 | P1-004 | المندوبون يحمل rptInvBySalesMen.repx، الأرباح rptItemsProfit.repx، والفترة RptSalesInPeriod1/2.repx. هذه مسارات تحميل حقيقية بخلاف stub SummaryQ؛ غياب القوالب من المستودع لا يثبت غيابها من النشر. الإعدادات تقرأ ثم تتجاوزها ReportsPath/ReportsPrinter وأسماء ثابتة؛ بعض flags غير مستهلكة، و LoadPrintSettings في الأرباح معرف دون استدعاء محلي. | manifest موثوق و schema للـ DTO و setting→effective-output/نسخ/header/footer/وجهة، مع حالات غياب/فشل وتعطيل معلن؛ لا قالب فارغ كعلاج. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:90-134`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:581-655`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:407-439`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:470-539`؛ `SmartAuditERP/Form_WPF/frmRptSalesInPeriod.xaml.cs:359-435` |
| EX7B10-02 | P1-013 | مداخلا Home للأرباح والمندوبين ينشئان نافذة ويعرضانها بلا Apply محلي، ومدخل حركة المبيعات يطبق Apply قبل Show وقائمته disabled. frmSalesMen يفتح المندوبين مباشرة؛ طفل تفاصيل الأرباح يطبق Apply. غياب apply في slice لا يثبت تجاوز حارس command/server أو إتاحة مستخدم نشر؛ potential التاريخية محفوظة. | مصفوفة دور×مدخل×طفل×قراءة/طباعة/تصدير/تكلفة×فرع وحارس حد موثوق؛ لا شهادة من visual-tree أو اسم زر. | `SmartAuditERP/Home.xaml.cs:3542-3544`؛ `SmartAuditERP/Home.xaml.cs:3604-3611`؛ `SmartAuditERP/Home.xaml:482-490`؛ `SmartAuditERP/Form_WPF/frmSalesMen.xaml.cs:269-280`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:652-665`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:517-570`؛ `SmartAuditERP/Class/MainClass.cs:418-455` |
| EX7B10-03 | P1-033 | ينشئ ProcessInvoiceRow تسميتي فاتورة نقطة بيع ومرتجعها، لكن switch الصف يدعم بيع/مرتجع عاديين وسند 5/7 وإشعاراً فقط؛ لا case لتسميتي POS ولا default يعلن عدم الدعم. زر الصف ظاهر لكل الحركات. الطباعة هنا منفذة ولا توصف stub؛ الملاحظة أمر POS فقط تحت أصل الاكتمال السابق. | توجيه typed لكل نوع مدعوم أو تعطيل/رسالة عدم دعم صريحة؛ لا اعتبار غياب case ترخيصاً أو فتح مستند من نوع آخر. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:279-290`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:517-570`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml:495-510` |
| EX7B10-04 | P2-010 | استعلام Inv يقيد MainClass.BranchNo عند !=-1، بينما استعلام Receipts للنوعين 5/7 لا يقيد BranchID؛ DDL وكاتبا السند يحملان هوية الفرع. وجود ترشيح مندوب أو اسم لا يثبت عزلاً، وغياب predicate محلي لا يثبت انتفاء حارس قاعدة/جلسة خارجي. | BranchScope مفوض واحد وهوية canonical لكل مصدر، بما فيها كل الفروع و NULL؛ ثم قبول مستقل على نشر مصرح لا اختراق مفترض. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:189-208`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:411-439`؛ `SmartAuditERP/Form_WPF/frmSandQ.xaml.cs:891-916`؛ `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:928-944`؛ `SmartAuditERP/Properties/Resources.resx:1496-1532` |
| EX7B10-05 | P3-023 | عند الفترة المحددة يمرر المندوبون DateTo+24h ويقارن <= في Inv و Receipts؛ منتصف اليوم التالي يدخل. DateTime parameters صحيحة النوع لكنها لا تصلح cutoff الشامل. لا نعيد عد حدود الأرباح/الفترة المشمولة في 7B1، ولا نخلطها باختلاف all-period الجديد. | مدى نصف مفتوح typed مع تحقق from<=to وتوقيت/دقة معلنين، مطبق في المصادر المصرح بها؛ لا إصلاح شكل string فقط. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:189-218`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:420-436` |
| EX7B10-06 | P7-041 | GetSaleData للأرباح يحسب TotalCost=SUM(val1*AvrgCost). الكاتب يضع val=ItemPrimaryQnty و val1=ItemQuantity و AvrgCost=ItemCost؛ تكلفة شراء البند في binder محسوبة لكل PrimaryQnty، و RecentPurchPrice يطبع السعر لكل val. عند تكلفة أساس 5 وعبوة 12 وكمية إدخال 2، تكلفة المصدر الأساس 120 مقابل 20 في تعبير التقرير. هذا امتداد لخلط البعد/الوحدة P7-041، لا نتيجة مستقلة لكل تقرير؛ P4-006 عن اختيار مصدر التكلفة و P7-039 عن تسمية العمود مختلفان وباقيان. | وحدة تكلفة موثقة وكمية مطابقة لها، مع UnitEquality=1/12 والبيع/المرتجع؛ لا تغيير AvgCost أو بيانات نشر آلياً من التقرير. | `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:270-287`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1612`؛ `SmartAuditERP/Class/InvoiceOper.cs:4301-4316`؛ `SmartAuditERP/Class/ItemOper.cs:196-211`؛ `SmartAuditERP/Class/ItemOper.cs:1390-1404` |
| EX7B10-07 | P7-045 | تاريخا From/To في DTO يقرآن من عناصر التحكم وقت الطباعة، والصفوف من _itemsList السابقة. تغيير التاريخ أو all-period بعد عرض لا يبطل القائمة؛ all-period لا ينقل كعلم مستقل للقالب. تغيير معايير بعد الطلب يختلف عن P7-112 داخل طلب واحد. | result snapshot تحمل criteria/rows/totals/time/branch وتبطل أو توسِم اختلاف المعايير؛ المخرج من لقطة واحدة لا TextBox حي. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:149-174`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:649-681`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:824-830` |
| EX7B10-08 | P7-046 | المندوبون يمسحون الصفوف ثم ينشرونها تدريجياً، ويتجاهلون فشل الإشعارات/السندات ويعيدون الإجماليات دون health لكل مصدر. الأرباح ومواد الفترة تعيدان أصفاراً عند فشل helper وقد تنشران لقطة ناقصة كأنها ناجحة؛ لا اختبار فشل SQL فعلي. خطأ اسم Notes مستقل، و worker gate سابق، ولا reentry ناجح مثبت كـ P7-107. | نتيجة ذرية rows+totals+criteria و status/error لكل مصدر، أو جزئي معلن يمنع قراراً/تصديراً مضللاً؛ صفر أعمال لا يساوي فشل استعلام. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:158-174`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:339-398`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:411-475`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:124-132`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:294-312`؛ `SmartAuditERP/Form_WPF/frmRptSalesInPeriod.xaml.cs:163-199` |
| EX7B10-09 | P7-054 | btnShow يشغل ShowInvoiceResults ثم قارئي السندات داخل Task.Run. أول كل قارئ يقرأ chkAll.IsChecked أو cmbEmps مباشرة، و ShowInvoiceResults يقرأ chkAllPeriod أيضاً؛ Dispatcher على التاريخ والإضافة لا يغطي هذه القراءات. هذه بوابة قبل النتائج الحسابية؛ catches لا تجعل المهمة ناجحة مالياً. | التقط كل قيم UI في DTO على dispatcher قبل العمل الخلفي، مررها بلا عناصر WPF، وأعد نشر لقطة وصحة الطلب على الخيط الصحيح؛ اختبر البوابة أولاً ولا تفترض زوالها. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:141-201`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:228-243`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:411-436`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml:282-333` |
| EX7B10-10 | P7-061 | DTO المندوب يحتفظ InvoiceNo/RefNo واسم النوع فقط. استعلامات الصف تقيد id مع النوع أو ReceiptNo مع النوع، لا InvGlobalID/GlobalID ولا الفرع؛ كيان Inv و Receipts مفاتيحهما global في DDL، والأطفال يقرؤون أول صف. الجهة المختارة قد تتطابق محلياً في فرعين. لا ننسب ذلك إلى حركة الفترة التي تحتفظ InvGlobalID ولا توفر زر فتح صف في هذا الجسم. | مفتاح immutable typed يشمل النوع و GlobalID والفرع المفوض عند العرض والفتح؛ لا الاعتماد على الاسم أو أول صف أو رقم محلي فقط. | `SmartAuditERP/Class_WPF/SalesManRowItem.cs:10-24`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:325-343`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:458-469`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:517-570`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:473-520`؛ `SmartAuditERP/Form_WPF/frmSandQ.xaml.cs:624-660`؛ `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:618-651`؛ `SmartAuditERP/Properties/Resources.resx:954-977`؛ `SmartAuditERP/Properties/Resources.resx:1012-1017`؛ `SmartAuditERP/Properties/Resources.resx:1496-1532` |
| EX7B10-11 | P7-069 | القارئ يحول NetVal إلى baseVal=NetVal*100/115 دون قراءة VAT/Payment. كاتب 5 يدخل VAT0 و NetVal=Payment، وكاتب 7 يضع VAT0 و NetVal=Payment. سند 115 بلا ضريبة يصبح 100 في عمود القيمة. العمولات على NetVal نفسه، فتحديد base التحصيل سياسة مستقلة. هذا امتداد نسبة 15 الثابتة لا finding آخر لكل reader. | استهلك حقول السند المحفوظة بعقد Payment/VAT/NetVal ومقياس القيمة المعتمد؛ لا استنتاج VAT من قاسم ثابت أو دمج فاتورة وقبض كصافي نقدي. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:450-469`؛ `SmartAuditERP/Form_WPF/frmSandQ.xaml.cs:891-916`؛ `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:928-944`؛ `SmartAuditERP/Properties/Resources.resx:1505-1508` |
| EX7B10-12 | P7-085 | بعد اختيار صنف A، يمكن تعديل الاسم أو الكود دون Enter؛ Show يتحقق من name غير فارغ فقط ثم يستخدم SelectedId القديم. XAML يربط KeyDown ولا يربط تغيير النص بمسح الهوية. الأصل نفسه في الأرباح التفصيلية P7-085؛ ليست نتيجة جديدة لمجرد اسم شاشة آخر. | هوية اختيار typed وتزامنها مع النص؛ التعديل يبطل/يعيد الاختيار قبل أي طلب، مع شاهد اختيار صالح دون تغيير. | `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:132-148`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:321-377`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:604-623`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml.cs:674-710`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfit.xaml:321-341` |
| EX7B10-13 | P7-095 | LoadPrintSettings يقرأ PriceIncVAT من SettingGeneral للنوع2؛ ثم ProcessInvoiceRow يطرح مبلغVAT من قاعدة القيمة وفق هذا الإعداد لكل الفواتير2/3، لا وفق row.PriceIncVAT المحفوظ. الكاتب يخزن العلم فيInv. تغيير الإعداد أو اختلافPOS قد يغير الأساس دون تغيير المستند. نفس أصل إعادة تفسير الشمولP7-095، مستقل عن115 الثابتة للسند. | استعمل علم/نسب VAT المحفوظة لكل مستند وخطوطه وعقد التاريخ/الخصم؛ لا تجعل إعادة طباعة/تقرير مستند قديم تتأثر بإعداد جديد. | `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:120-131`؛ `SmartAuditERP/Form_WPF/frmInvBySalesMen.xaml.cs:249-273`؛ `SmartAuditERP/Class/InvoiceOper.cs:1557-1564`؛ `SmartAuditERP/Properties/Resources.resx:986-994` |

### منع التضخيم وشواهد مقابلة

- **P7-111 تجميع داخل التقرير**:Value وإجماليXLSX لا يتبعان IsPlus. يختلف عنP7-093، الذي يفقد المجاميع الموقعة في جسور طباعة مؤقتة. لا نعده مرتين للعرض والملف. P7-084 يتعلق بأهلية النوع/الاتجاه وإسقاط حركات من مصادر أخرى، لا تجاهل إشارة صفوف موجودة هنا.
- **P7-112 عضوية مصادر في الطلب نفسه**. P3-023 حد نهاية شامل؛ P7-109 فشلparse يوسع الفترة؛ P7-045 تغييرcriteria بعد العرض. أسباب مستقلة، لا نتائج لكلquery.
- **P7-113 عدم تطابق محلي للاسم**، لا حكم بأن كل نشر يفتقر إلىNotes. إذا حسم التوافق لاحقاً تبقى سياسةInv_No/DocType/الحذف/الفرع/التاريخ تحتH7B10-02؛ لا بيانات ملوثة مثبتة الآن.
- `SUM(val1*AvrgCost)` في الأرباح يخالف بُعد تكلفة الأساس في عقد الكاتب:val=PrimaryQuantity وval1=EnteredQuantity وAvrgCost=ItemCost؛ وbinder الشراء يحسب الكلفة لكلPrimaryQuantity. qty2/pack12/cost5 تقابل120 لا20؛ equality1 شاهد مطابق. يمتد **P7-041**؛ لا نتيجة جديدة لاختيار مصدر تكلفةP4-006 أو تسمية متوسطP7-039.
- **P7-095** أصل إعادة تفسير شمولVAT بإعداد النوع الحالي بدلاً من علمInv المحفوظ؛ قاسم115 للسندVAT0 أصلP7-069 مستقل. سياسة العمولة والنسب الحالية والقبض الجزئي واحتمال عد الحدث مرتين تحتاجH7B10-01؛ ليست استحقاقاً أو تسوية مالية مثبتة.
- **P7-038/039/040/042 باقية من7B1**:خصمPOS مرتين، إجمالي تكلفة باسم متوسط، إسقاطreturn-only، ومجموع تبويب آخر. Binding `IsPostpone` يطابقDTO وتعيين الجسم فعلاً؛ لا عيبbinding مختلق. تبويبا المواد والرؤوس ليسا مقياساً واحداً دون تطبيع الضريبة والخصم والوحدة.
- المندوبون يكتبون **XLSX حقيقياً بخلاياClosedXML typed**؛ لا ننسخ إليه عيب نحوCSV أو نفترض تفسير صيغة من`.Value`. SaveAs داخلhelper؛ ينتهيusing عندreturn **قبلlaunch فيcaller**، فلا امتدادP7-108. إصدار المكتبة وسياسة المستهلك لم يختبرا. أرباح/فترةCSV معلنان بامتدادهما الصحيح وتبقىP7-048/049 السابقة، لاP7-050 جديدة.
- **استدعاءاتREPX/preview/print فعلية في الثلاثة**، خلافstub SummaryQ السابق. القوالب والنسخ والوجهة والـflags والإعداد المستهلك عقود غير محسومة، لا غياب عالمي. حلقة مباشرة لا تطبع عندcopies0 ليستP7-030 بلا شرط يفرض نسخة واحدة.
- Home ينشئ **نسخاً جديدة** للتقارير الثلاثة؛ لا امتدادP1-030 static/Close آلياً. Apply-before-Show وتعطيلmenu حركة الفترة، وApply لطفل تفاصيل الأرباح، شواهد صحيحة؛ غيابApply في مدخل آخر لا يثبت انتفاء حارسcommand/server. potentialP1-013 لا يرتقي.
- طفل الأرباح يتلقىSelectedId فقط، ويقرأ حركة الصنف بلاcriteria الأب في المقاطع؛ قد تكونall-history مقصودة. هذا عقدdrilldown لا خلل مؤكد من اختلاف فترتين. N+1 وFill المتتابع ومصنع الاتصال مؤشرات مصدر، لاlatency/index/leak مقاسة ولا اكتمال7C.

## 4. المعالجات والباقي

الترتيب المنطقي: **بوابةworker/criteria، ثم توافق المصدر والهوية والنطاق، ثم المقياس والوحدة والإشارة والمجاميع، ثم صحة النتيجة والمخرج**. لا ترقيع حسابياً يفترض نجاح بوابة سابقة، أوUPDATE تكلفة/ضريبة/GL من تقرير. المقترحات في[مصفوفة23/23 وعقود6](SALESMAN-REPORT-CONTRACTS-07B10.md)، و[26 خطة غير منفذة وحدود التحقق](VALIDATION-07B10.md)، و[IMPROVEMENTS](IMPROVEMENTS.md) G135–140. [checksB10](evidence/checks-07B10.json) سجل مدقق وثائق لا قبول مالي/أمني.

**التالي7B11** لبقية العقود/callers/children/output/template/schema/ACL والإتاحة، أو استبعادات مسندة وأجزاء إضافية. **7C لم تبدأ** لبقيةHR/PM/بحري/UI ودورةWPF/events/resources/timers/async/connections والاختصارات/RTL/accessibility/cultures/messages وأداء المصدر. لا إغلاق7B/7 إلا بمصفوفة قدرة×شاشة×implementation×test أو استبعاد مسبب؛98/52 أسماء فرز فقط. **8 غير مأذونة**؛ دفع التوثيق أوnext_phase8 لا يجيز بناء/تشغيل/قياس/معالجة.
