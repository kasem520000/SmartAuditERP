# الجزء7B7 — كشف مركز التكلفة وأرباح الفواتير وأرصدة المواد وإعداد الطباعة وإجمالي عميل

**7B7 تسليم ساكن جزئي ضمن إذن تدقيق7 القائم؛ لم تكتمل7B أو7. أُعلنت7B8 للباقي ولم تبدأ، و7C لم تبدأ، والمرحلة8 غير مأذونة ولم تبدأ. لا إصلاح تطبيق أو تشغيل قبول.**

**مرجع التدقيق المعلن:**2026-11-16 UTC؛ ليس وقت ساعة البيئة. مرجع التطبيق الأصلي `10ba215152f722c8808aea0bb672c1d1d4d9d711` ثابت، والفرع `arena/94ae8414-smartauditerp`. آخر التزام مدفوع `d0ae6b318c47451dd7e10a416f07566a7b3f1dc7` يضم توثيق1–6 و7A/B1–B5 فقط؛ B6 وB7 عمل لاحق محفوظ في مساحة العمل، لا جزءاً من ذلك الدفع. لا commit/push أوPR جديد في هذا الجزء.

## 1. الحصيلة وحدود التسليم

قُرئت الأجسام المحلية الخمسة وواجهات XAML المرتبطة بها فعلياً: `frmCostCenterBalance`، `frmInvsProfit`، `frmItemsBalances`، `frmInvRptType`، `frmNkdTotSalePurchActCust`. قراءة مدخل أو مساعد سابق، أو حصر اسم مرشح، لم تكن تغطي هذه الأجسام. وهذه القراءة المحلية لا تصدّق جميع المتصلين أو الشاشات الفرعية أو القوالب والسياسات وبيئة النشر.

| المقياس | النتيجة المحدودة |
|---|---|
| جديد هذا الجزء | **6 نتائج P7-099–104:1 عالية و5 متوسطة، confirmed محلياً بشروطها، كلها مفتوحة ولم تعالج** |
| امتدادات التاريخ | **18 ذيلاً** إلى أصول سابقة؛ لا إعادة عد أو تغيير نواة/عنوان/تصنيف/حالة/أي next_phase لأول270 |
| التراكمي المفتوح | **276**:2 حرجة،175 عالية،98 متوسطة،1 منخفضة؛ **241 confirmed و28 potential و7 repository-gap** |
| النطاق | **19 مساراً**:9 تتقاطع مع353 السابقة و10 جديدة؛ الاتحاد**363**، والمكمل**464 inventory-only** ومقاطع باقية داخل الاتحاد |
| القراءة المحلية | **2894 سطراً C# و2100 XAML=4994 سطراً** للأجسام/واجهاتها فقط؛ لا كل dependency أو مسار متصل |
| النموذج والخطط | **31 صف FE و31 ثابت INV و8 عقود RC و37 خطة قبول/بوابة غير منفذة**؛ H6/Q6/backlog10 |
| شواهد المدقق | 22 نموذجاً يدوياً مستقلاً و22 ملاحظة نصية محدودة، و24 حالة جديدة لمدقق الوثائق؛ لا ERP/SQL/SDK/Office |

37 خطة=12 مباشرة للجديد+18 انحدار أصل+5 عقود عابرة+2 بوابة. confirmed يعني تعارضاً/إغفالاً محلياً مشروطاً، لا حادث إنتاج أو قبولاً مالياً. لم ترفع P1-013 أوP7-049 من potential؛ no caller في البحث لا يثبت غياب قدرة مؤسسية. **كل ERP/build/SQL/COM/Office/مزود/جهاز ومعالجة=0.**

## 2. فصل المصدر عن التوثيق وحماية التاريخ

- [provenance7B7](evidence/provenance-07B7.json) أُنشئ مرة عند الدخول، ويحمي **223 artifact تاريخية**، ومنها تقارير/أدوات B6 وchecksها الفعلية. لا يعاد توليد تاريخ أو baseline للحصول على نجاح.
- [لقطة270](evidence/findings-through-07B6.csv) SHA256=`781c9d4bac775f55456f6b54ba66c4190de0ec93f14b50886790121e8d0e1a98`، و[نصوص فهارس B6 الثلاثة](evidence/shared-indexes-through-07B6.json) SHA256=`99af3af80436557ad21e54784602fd7fd913ea3edd5458813bde49e4f24cb058` ثابتتان.
- checksB6 الفعلي SHA256=`b171d38d2f1d12894be879346c689c67900efed10105c5f2fae5ace110e413a0` محمي؛ B6 يعاد فحصه بمدخل270 وفهارسه الدقيقة في الذاكرة، لا276 أو فهارس اليوم. كذلك A/B1–B5 بمدخلاتها الخاصة. مقاييس checker الأحدث ليست إعادة إنتاج bytes لتاريخ checks.
- مرجع source10ba لا يستبدل بـcheckoutd0ae: إثبات ancestry وصافي دلتا الشجرة الملتزمة داخل docs/audit فقط، ثم **مجموعة مسارات827 وبصماتها الأصلية مستقلة**. هذا فحص net delta لا توقيعاً/تفويضاً تشفيرياً أو إثبات كل تاريخ وسيط.
- **كل270 نواة وnext_phase محفوظة**، ومنها43 نتيجة تاريخية تحمل7. **G01–116 محفوظة حرفياً**، وتضاف G117–122 كمجموعات توصية لا نتائج أخرى؛ next_phase8 للجديد خطة لا إذن تشغيل8.
- وقت البيئة المشاهد للدخول `2026-11-18T03:23:01+00:00` مسجل منفصلاً، ولا يعيد تأريخ المرجع المعلن16نوفمبر أو أرشيف سابق.

| المسار | النطاق المختار | حد القراءة وحده |
|---|---|---|
| `SmartAuditERP/Class/Common.cs` | `429-446` | ResrirectionType يقرأ كتالوج EntryTypes؛ لا مراجعة كل Common أو ترجمة UI. |
| `SmartAuditERP/Class/InvoiceOper.cs` | `1526-1624;3007-3218` | عقود رأس/بنود/وحدات/InvProfit=0، وتحميل GID وItems لتصحيح التكلفة؛ لا كل حفظ/ربط/ضريبة/ترحيل. |
| `SmartAuditERP/Class/ItemOper.cs` | `162-228;288-385;1394-1407` | AvgCost/RecentPurchPrice وعقد سعر الأساس وتصحيح السالب ومفتاح السطر وحساب كمية الأساس؛ لا تقييم تاريخي كامل. |
| `SmartAuditERP/Class/MainClass.cs` | `418-455` | مصنف أسماء أزرار WPF العام وحدوده المرئية؛ لا نتيجة تفويض خادم أو runtime tree مثبتة. |
| `SmartAuditERP/Class/StoredQueries.cs` | `26-28` | نصا UpdateItemCost وUpdateInvProfit فقط؛ لا تشغيل أو كل المستودعات. |
| `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml` | `1-806` | XAML محلي كامل لربط controls/handlers/columns فقط؛ لا render/RTL/وصول مقبول. كشف مركز التكلفة:معايير/سابق/فترة/نوع/طباعة/CSV وبحث وحالة؛ لا كل كاتب/قالب/نشر. |
| `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs` | `1-1176` | جسم محلي كامل. كشف مركز التكلفة:معايير/سابق/فترة/نوع/طباعة/CSV وبحث وحالة؛ لا كل كاتب/قالب/نشر. |
| `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs` | `276-296` | إغلاق POS ينشئ نافذة أرصدة جديدة ليغلقها؛ لا بقية محرر POS أو كل مداخل أرصدة. |
| `SmartAuditERP/Form_WPF/frmInvRptType.xaml` | `1-123` | XAML محلي كامل لربط controls/handlers/columns فقط؛ لا render/RTL/وصول مقبول. إعداد افتراضي الطباعة:قراءة غائبة وحفظ/رسائل/تنظيف؛ لا مستهلك طابعة مثبت. |
| `SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs` | `1-73` | جسم محلي كامل. إعداد افتراضي الطباعة:قراءة غائبة وحفظ/رسائل/تنظيف؛ لا مستهلك طابعة مثبت. |
| `SmartAuditERP/Form_WPF/frmInvsProfit.xaml` | `1-778` | XAML محلي كامل لربط controls/handlers/columns فقط؛ لا render/RTL/وصول مقبول. أرباح الفواتير:مصدر/تكلفة/أهلية/ملخص/كتابة تصحيح/تفاصيل/REPX/CSV؛ لا سياسة تقييم أو DTO/SDK خارجية محسومة. |
| `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs` | `1-1120` | جسم محلي كامل. أرباح الفواتير:مصدر/تكلفة/أهلية/ملخص/كتابة تصحيح/تفاصيل/REPX/CSV؛ لا سياسة تقييم أو DTO/SDK خارجية محسومة. |
| `SmartAuditERP/Form_WPF/frmItemsBalances.xaml` | `1-130` | XAML محلي كامل لربط controls/handlers/columns فقط؛ لا render/RTL/وصول مقبول. قارئ أرصدة المواد واتجاهاته وتحويلاته ودمجه وفشله؛ CalcStock callable لا caller عرض مثبت. |
| `SmartAuditERP/Form_WPF/frmItemsBalances.xaml.cs` | `1-230` | جسم محلي كامل. قارئ أرصدة المواد واتجاهاته وتحويلاته ودمجه وفشله؛ CalcStock callable لا caller عرض مثبت. |
| `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml` | `1-263` | XAML محلي كامل لربط controls/handlers/columns فقط؛ لا render/RTL/وصول مقبول. مصادر إجماليات عميل وجهة/اتجاه/كمية/قيمة وفشل وخيط وstub؛ لا كل caller أو عضوية تاريخية محسومة. |
| `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs` | `1-295` | جسم محلي كامل. مصادر إجماليات عميل وجهة/اتجاه/كمية/قيمة وفشل وخيط وstub؛ لا كل caller أو عضوية تاريخية محسومة. |
| `SmartAuditERP/Form_WPF/frmPOS.xaml.cs` | `282-299` | نظير إغلاق POS الآخر ينشئ نسخة أرصدة جديدة؛ لا caller عرض أو حساب مثبت. |
| `SmartAuditERP/Home.xaml.cs` | `194-195;2642-2647;3541-3541;3766-3766` | مرجع static لإعداد الطباعة وثلاثة مداخل Home المباشرة؛ لا كل قائمة/دور أو callback خارجي. |
| `SmartAuditERP/Properties/Resources.resx` | `242-270;954-1074;1538-1577;1650-1688;1958-1963;3026-3081;3371-3401` | DDL وكتالوج محليان للفروع/رأس وبند/قيد وتحويل/sett وأنواع؛ لا برهان مخطط منشور أو خلو جدول إنتاج أو تنفيذ ترقية. |

[نطاق19](review-scope-07B7.csv)، [دفتر827](evidence/coverage-ledger-07B7.csv)، [فرز98 ملفاً](evidence/report-candidate-disposition-07B7.csv)، [52 مرشح شاشة](evidence/report-screen-disposition-07B7.csv)=35 لفظياً+17 curated لا أعداد ميزات. FingerPrintDevice مطابقة لفظية للبصمة. all-lines داخل جسم لا يغطي كل caller/child/template أو عقد سياسة/نشر/قبول.

## 3. النتائج الجديدة — الشروط والأثر والحدود والمعالجة المقترحة

### P7-099 — مرشح مرتجعات كشف مركز التكلفة يحتفظ بالنوع السابق لأن فهارس الخيارات لا تصل إلى فرع التحويل

**الخطورة:**متوسطة؛ **confirmed من المصدر، open-not-remediated.**<br>
**الشاشة/المسار:**`frmCostCenterBalance` — LoadResType → cmbEntryType_SelectionChanged → Restype → BuildTypeFilter.

**الدليل:**`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:43-71`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:194-219`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:362-367`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:1002-1017`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml:338-355`؛ `SmartAuditERP/Properties/Resources.resx:3371-3386`.

**المشاهدة المحلية:**تحتوي القائمة17 خياراً بفهرس0–16؛ يعيّن handler قيمة Restype للفهرس0–13 فقط أو21–23 مع +7. خيارات المرتجع المعروضة تقع14–16، فلا تصل إلى أي تعيين. يبقى Restype=-1 عند أول اختيار أو يحتفظ بنوع اختير قبله، ثم BuildTypeFilter يقرأه مع تعطيل خيار الكل.

**السبب الجذري:**الخلط بين index واجهة وقيمة Entry.type وشرط غير قابل للوصول لخيارات المرتجع؛ حالة وسيطة باقية بدلاً من هوية typed لكل خيار.

**شرط الوصول والحواجز:**افتح الجسم، اختر مركزاً صالحاً وألغِ كل أنواع القيد. اختر مشتريات index1 ثم مرتجع مشتريات index14؛ أو ابدأ بمرتجع مباشرة. اعزل فلتر السابق/الفترة واجعل مخطط/فرع/صفوف الاختبار صالحة. مراجعة ساكنة محلية ضمن النطاق فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM/مزود/جهاز، ولا إثبات نشر أو حادث إنتاج أو قبول مالي/أمني. حواجز البناء وDTO والمخطط والتفويض والإتاحة والسياسة تسبق أي قبول لاحق مأذون؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط:**1 ثم14 يترك Restype=1 فيرشّح القيد العادي لا21. أول اختيار14 يبقي-1 فيحذف شرط النوع كله.15/16 لهما السلوك نفسه بدلاً من22/23.

**الشاهد المقابل ومنع التكرار وحد الدليل:**اختيار0–13 يصل إلى تعيين محلي فعلي؛ لا نزعم أن كل الفلاتر مهملة. تسميات3 و9 محلية وتحتاج كتالوجاً معتمداً، لكن إثبات الفهارس14–16 مستقل عنها. ليس P7-084 الخاص بنطاقات نوع الفاتورة/إجراء الرأس/أثر السطر، ولا مجرد P7-080 لمرشح غير مقروء: هنا state قديم يعاد استعماله.

**المعالجة المقترحة — لم تنفذ:**اربط كل عنصر بكود EntryType مخزن، لا SelectedIndex أو +7؛ ارفض اختياراً بلا كود وامسح الحالة السابقة. وحّد أسماء القائمة مع الكتالوج ذي الإصدار واختبر كل انتقال لا الاختيار الأول وحده.

**قبول غير منفذ:**P7B7T-01 وP7B7T-02 في[خطة37](VALIDATION-07B7.md)، مع الربط الكامل في FE7B7-01 وINV7B7-01. النموذج اليدوي وفحص النص ليسا قبول النتيجة.

### P7-100 — تصفية أرباح الفواتير تقارن InvProfit المحفوظ بدلاً من الربح المعروض وفق التكلفة المختارة

**الخطورة:**عالية؛ **confirmed من المصدر، open-not-remediated.**<br>
**الشاشة/المسار:**`frmInvsProfit` — BuildWhereClause → SELECT Inv.Invprofit → ShowInvs cost mode → DgvProfit.

**الدليل:**`SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:294-311`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:327-373`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:395-411`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:759-771`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml:716-763`؛ `SmartAuditERP/Class/InvoiceOper.cs:1539-1545`؛ `SmartAuditERP/Class/ItemOper.cs:354-379`.

**المشاهدة المحلية:**الفلاتر موجب/سالب/صفر تطبق في SQL على inv.Invprofit قبل قراءة التفاصيل. صف الشاشة يحسب profit=InvTotal−_invAvrgCost، وتتغير التكلفة بين متوسط محفوظ وسعر شراء حالي وآخر شراء. الكاتب المشترك يمرر InvProfit=0 عند الإدراج، وتصحيح السالب له كاتب منفصل؛ لا مساواة مضمونة بين الحقل والمقياس المختار.

**السبب الجذري:**مصدر قرار الأهلية ليس مصدر المقياس الذي يراه المستخدم؛ الحقل المخزن بلا هوية cost basis/version لا يمثل بالضرورة الربح المحسوب لاحقاً.

**شرط الوصول والحواجز:**فاتورة مخولة غير محذوفة نوع2/3 وإجراء صالح، تفاصيلها موجودة وصالحة وCurrentQnty>=0، ومعيار غير المعالج غير محدد؛ InvTotal=100 وتكلفة العرض60 وInvProfit المخزن0. اعزل دقة الوحدة والضريبة والمرتجع أولاً. مراجعة ساكنة محلية ضمن النطاق فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM/مزود/جهاز، ولا إثبات نشر أو حادث إنتاج أو قبول مالي/أمني. حواجز البناء وDTO والمخطط والتفويض والإتاحة والسياسة تسبق أي قبول لاحق مأذون؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط:**قيمة العرض40، لكن اختيار موجب يستبعد الفاتورة و«صفر» يقبلها ويعرض40. مخزن10 مقابل تكلفة120 يعرض خسارة-20 داخل مجموعة «موجب». لا يلزم افتراض خطأ متوسط أو بيانات إنتاج.

**الشاهد المقابل ومنع التكرار وحد الدليل:**توافق المخزن مع الأساس المحسوب يخفي العيب؛ «الكل» لا يطبق معيار الإشارة لكنه لا يصلح معايير الموجب/السالب. P4-005 عيب تراكم ربح الكاتب لا يعاد عده؛ حتى حقل محفوظ صحيح وفق أساس مختلف لا يصلح كفلتر لمقياس جديد. لا نزعم أن كل الفواتير مخزنها0 أو أن InvTotal يساوي شامل الضريبة.

**المعالجة المقترحة — لم تنفذ:**عرّف ProfitBasis/CostBasis صريحين واشتق التصفية والعرض والبطاقة والإخراج من المقياس نفسه بإشارة المرتجع وسياسة تاريخ معلنة؛ أو سمِّ معيار الربح المخزن مستقلاً واعرضه كذلك. لا تعالج بتحديث جميع الحقول القديمة إلى قيمة عشوائية.

**قبول غير منفذ:**P7B7T-03 وP7B7T-04 في[خطة37](VALIDATION-07B7.md)، مع الربط الكامل في FE7B7-02 وINV7B7-02. النموذج اليدوي وفحص النص ليسا قبول النتيجة.

### P7-101 — ملخصات أرباح الفواتير معرفة كـCustom بلا ربط الحاسبة اليدوية بخلايا الملخص

**الخطورة:**متوسطة؛ **confirmed من المصدر، open-not-remediated.**<br>
**الشاشة/المسار:**`frmInvsProfit` — ShowInvs → RecalculateCustomSummaries → private accumulators; XAML TotalSummary Custom.

**الدليل:**`SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:463-470`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:493-544`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml:225-241`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml:413-439`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:969-1019`.

**المشاهدة المحلية:**تحسب RecalculateCustomSummaries المجاميع العادية والمرتجعة في حقول private ثم تنتهي بتعليق عن عرضها تلقائياً. الخمسة TotalSummary في XAML من نوع Custom؛ لا CustomSummaryCalculate أو Binding/assignment يصل الحقول بهذه الخلايا في الجسم وXAML المقروءين. بالمقابل BuildReportDataSet يسند فروق الحقول إلى DTO صراحة.

**السبب الجذري:**مسار إنتاج الملخص اليدوي منفصل عن عقد استهلاكه في Grid؛ التعليق لا يربط handler أو قيمة Custom بالواجهة.

**شرط الوصول والحواجز:**اكتمل ShowInvs لصف بيع100 ومرتجع20 بالقيم الصحيحة ومخطط/SDK صالحين. المقصود فحص wiring محلي ثم قبول واجهة مأذون لاحقاً، لا التنبؤ بنص default لإصدار DevExpress غير منفذ. مراجعة ساكنة محلية ضمن النطاق فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM/مزود/جهاز، ولا إثبات نشر أو حادث إنتاج أو قبول مالي/أمني. حواجز البناء وDTO والمخطط والتفويض والإتاحة والسياسة تسبق أي قبول لاحق مأذون؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط:**المجموع signed اليدوي80 محسوب، لكن لا مسار محلي يسلّمه لخمس خلايا الملخص. لا نقرر هل يعرض SDK فراغاً أو0 أو تنسيقاً آخر؛ المؤكد غياب نقل80 إلى Custom من هذا التنفيذ.

**الشاهد المقابل ومنع التكرار وحد الدليل:**Print DTO ينقل sum−sum1/Profit−Profit1/Cost−Cost1 صراحة، لذا لا نمدد P7-093 لنفس الشاشة ولا نزعم فقد تلك القيم في طباعة REPX. هذا ليس handler فارغاً جديداً لكل خلية؛ نتيجة واحدة لربط الملخصات، والقبول المرئي محجوب دون SDK/بناء.

**المعالجة المقترحة — لم تنفذ:**انقل التجميع إلى نموذج نتيجة واحد واربط CustomSummaryCalculate أو آلية WPF موثقة بالقيم signed، مع تحديثها عند إعادة التحميل/تصفية العرض حسب عقد واضح. استعمل المصدر نفسه للطباعة والتصدير ولا تجمع المرتجعات موجبة افتراضياً.

**قبول غير منفذ:**P7B7T-05 وP7B7T-06 في[خطة37](VALIDATION-07B7.md)، مع الربط الكامل في FE7B7-03 وINV7B7-03. النموذج اليدوي وفحص النص ليسا قبول النتيجة.

### P7-102 — تحويلات أرصدة الأصناف تستعمل مرجع inv غير المعرّف وعمود currency بدل ItemId

**الخطورة:**متوسطة؛ **confirmed من المصدر، open-not-remediated.**<br>
**الشاشة/المسار:**`frmItemsBalances` — CalcStock(safeId) → branchFilter → FillTransferData → MergeRows.

**الدليل:**`SmartAuditERP/Form_WPF/frmItemsBalances.xaml.cs:41-91`؛ `SmartAuditERP/Form_WPF/frmItemsBalances.xaml.cs:141-160`؛ `SmartAuditERP/Properties/Resources.resx:1650-1688`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:289-295`؛ `SmartAuditERP/Form_WPF/frmPOS.xaml.cs:293-298`.

**المشاهدة المحلية:**يعاد استعمال branchFilter=inv.branch=... في استعلامين FROM SafesTransfer,SafesTransfer_Sub لا يعرّفان inv؛ كلاهما SELECT currency ... GROUP BY currency مع أن DDL المرفق للتفاصيل يعرف ItemId ولا currency. FillTransferData يبتلع الاستثناء دون حالة خطأ ويستكمل بقية الحركات.

**السبب الجذري:**نسخ عقد استعلام من مصدر/مجال آخر دون مواءمة alias ومفتاح الصنف لمصدر التحويلات؛ الإغفال موجود قبل صحة أي قيمة مالية.

**شرط الوصول والحواجز:**إذا استدعي CalcStock بمخزن صالح وBranchNo!=-1، يصبح inv.branch مرجعاً غير مربوط في SQL المختار حتى لو أضيف currency في مخطط آخر. عند=-1 يختفي alias لكن تعارض currency مع DDL المرفق يبقى مشروطاً بالمخطط. لا caller عرض مثبت هنا. مراجعة ساكنة محلية ضمن النطاق فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM/مزود/جهاز، ولا إثبات نشر أو حادث إنتاج أو قبول مالي/أمني. حواجز البناء وDTO والمخطط والتفويض والإتاحة والسياسة تسبق أي قبول لاحق مأذون؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط:**وارد مخزن5 وخروج2 ينبغي أن يساهما+3؛ مسارا التحويلات يمكن أن يفشلا ويتركا مساهمتهما0 فيما يستمر تقرير الأرصدة، مع عزل أخطاء اتجاه الفاتورة P7-084. هذا توقع فرع مصدر لا تشغيل SQL.

**الشاهد المقابل ومنع التكرار وحد الدليل:**الموضعان المكتشفان في POS ينشئان instance جديدة لإغلاقها، لا يعرضانها ولا يستدعيان CalcStock. غياب caller في البحث ليس إثبات استحالة reflection/XAML/نسخة خارجية؛ النتيجة تعارض التنفيذ عند الاستدعاء، لا بلاغ شاشة إنتاجية مفتوحة. ابتلاع الفشل توسعة P7-046 منفصلة؛ لا نكرر finding لكل alias/column.

**المعالجة المقترحة — لم تنفذ:**حدد DTO حركة صنف ومصدر تحويل بإصدار، واستعمل SafesTransfer.branch وSafesTransfer_Sub.ItemId والاتجاه/الوحدة الصحيحين بعقد موحد؛ لا تعدّل المخطط بإضافة currency لتغطية نسخ خاطئ. أعد خطأ typed وامنع إعلان رصيد مكتمل عند فشل مصدر، واحسم إتاحة الميزة أو استبعادها.

**قبول غير منفذ:**P7B7T-07 وP7B7T-08 في[خطة37](VALIDATION-07B7.md)، مع الربط الكامل في FE7B7-04 وINV7B7-04. النموذج اليدوي وفحص النص ليسا قبول النتيجة.

### P7-103 — افتراضي طباعة الفواتير يبدأ دائماً بـA4 دون استرجاع القيمة المحفوظة

**الخطورة:**متوسطة؛ **confirmed من المصدر، open-not-remediated.**<br>
**الشاشة/المسار:**`frmInvRptType` — Home stripDefaultPrint → constructor → XAML RadioButton1=true → UPDATE sett.

**الدليل:**`SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs:19-26`؛ `SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs:38-54`؛ `SmartAuditERP/Form_WPF/frmInvRptType.xaml:83-100`؛ `SmartAuditERP/Home.xaml.cs:194-195`؛ `SmartAuditERP/Home.xaml.cs:3766-3766`.

**المشاهدة المحلية:**الـconstructor يهيئ XAML والاتصال فقط، ولا Loaded/read لصف sett. XAML يحدد RadioButton1(A4)=true، والحفظ يحوّل RadioButton2 إلى2 وإلا1. مدخل Home لا يمرر القيمة الحالية أو يعيد ربطها قبل ShowDialog.

**السبب الجذري:**دورة إعداد write-only بلا تحميل الحالة المعتمدة؛ default عرض أولي يصير قيمة كتابة بدلاً من تمثيل المخزن.

**شرط الوصول والحواجز:**عند فتح instance جديدة ووجود صف واحد sett.id=1,val=2 محفوظ سابقاً، لا تعديل للخيارات ولا خطأ SQL. أعد تشغيل fixture/new instance لتجاوز إعادة Show لنافذة Closed المشمولة أصلاً بـP1-030. مراجعة ساكنة محلية ضمن النطاق فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM/مزود/جهاز، ولا إثبات نشر أو حادث إنتاج أو قبول مالي/أمني. حواجز البناء وDTO والمخطط والتفويض والإتاحة والسياسة تسبق أي قبول لاحق مأذون؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط:**تظهر A4 أول مرة رغم2 المحفوظة؛ الضغط على حفظ دون تغيير يكتب1. لا نزعم أن طابعة فعلية استهلكت sett أو أن كل محركات الطباعة تقرؤه؛ العيب round-trip للإعداد نفسه.

**الشاهد المقابل ومنع التكرار وحد الدليل:**اختيار الورق الصغير يكتب2 فعلاً عند وجود الصف؛ الكتابة ليست stub. احتمال نافذة Closed يمنع إعادة فتحها في الجلسة نفسها ولا يصلح الفتح الأول. P7-104 مستقل عن غياب القراءة: حتى affectedRows=1 لا يمنع استبدال2 بـ1.

**المعالجة المقترحة — لم تنفذ:**حمّل صف إعداد واحداً موثوقاً عند فتح instance وربط النموذج، واعرض unknown/missing عند الغياب أو قيمة غير صالحة؛ احفظ intent صريحاً لا default غير محمل، مع إثبات أن المستهلك المعتمد يقرأ الإصدار نفسه.

**قبول غير منفذ:**P7B7T-09 وP7B7T-10 في[خطة37](VALIDATION-07B7.md)، مع الربط الكامل في FE7B7-05 وINV7B7-05. النموذج اليدوي وفحص النص ليسا قبول النتيجة.

### P7-104 — حفظ افتراضي الطباعة يعلن النجاح دون التحقق من تحديث صف الإعداد

**الخطورة:**متوسطة؛ **confirmed من المصدر، open-not-remediated.**<br>
**الشاشة/المسار:**`frmInvRptType` — Button1_Click → UPDATE sett WHERE id=1 → ExecuteNonQuery ignored → success.

**الدليل:**`SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs:38-68`؛ `SmartAuditERP/Properties/Resources.resx:1958-1963`؛ `SmartAuditERP/Form_WPF/frmInvRptType.xaml:107-116`.

**المشاهدة المحلية:**ينفذ UPDATE فقط ولا يحتفظ بنتيجة ExecuteNonQuery، ثم يظهر «تم الحفظ بنجاح» إن لم يقع استثناء. لا insert عند غياب الصف ولا تحقق من عدد أو قراءة لاحقة. DDL المرفق لـsett(id,val) لا يبين قيد تفرد علىid.

**السبب الجذري:**عدم ربط نجاح واجهة الحفظ بوجود/كاردينالية هدف التعديل؛ no exception ليس دليلاً على حفظ صف الإعداد المطلوب.

**شرط الوصول والحواجز:**جدول sett صالح في اختبار معزول لكنه بلاid1، وUPDATE يعيد0 دون exception، مع صلاحية تنفيذ معتمدة. حالة تكرارid1 مسموحة في DDL المحلي تحتاج تحقق مستقل لا افتراض حدوثها. مراجعة ساكنة محلية ضمن النطاق فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM/مزود/جهاز، ولا إثبات نشر أو حادث إنتاج أو قبول مالي/أمني. حواجز البناء وDTO والمخطط والتفويض والإتاحة والسياسة تسبق أي قبول لاحق مأذون؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط:**الحفظ يعلن النجاح مع بقاء الجدول بلا الصف المطلوب. صفانid1 يمكن أن يعدلا معاً بلا اعتراض محلي؛ المؤكد غياب حارس cardinality لا حصول تكرار منشور.

**الشاهد المقابل ومنع التكرار وحد الدليل:**وجود صف وحيد يعالج فعلاً وتغلق الدالة الاتصال في finally؛ لا نزعم أن الحفظ يفشل دائماً أو أن الاتصال يبقى مفتوحاً هنا. P7-103 يعالج القراءة ولا يصلح نجاح0-row؛ يلزم حارس كتابة مستقل.

**المعالجة المقترحة — لم تنفذ:**عرّف إعداداً وحيد الهوية مع قيد فريد وترحيل مدروس بعد كشف القديم؛ تحقق من affectedRows=1 أو نفذ تهيئة/UPSERT ذرياً مصرحاً بعقد حالة، وأظهر missing/conflict/failed بدلاً من نجاح غير مثبت.

**قبول غير منفذ:**P7B7T-11 وP7B7T-12 في[خطة37](VALIDATION-07B7.md)، مع الربط الكامل في FE7B7-06 وINV7B7-06. النموذج اليدوي وفحص النص ليسا قبول النتيجة.

## 4. إضافات أدلة الأصول —18 لا18 نتيجة جديدة

خلط الأنواع/الاتجاه في أرصدة المواد وعميل **توسعة P7-084**، وعدم تجانس السعر/الكمية **P7-041**، والسابق غير المقيد بمفتاح الحساب/النوع **P7-053**، وسقوط المبلغ عندQ0 **P7-040**. للمعالجات الفارغة أصل واحد P1-033. عناوين الأصول التاريخية محفوظة ولو كانت أضيق من الجسم الجديد؛ لا تعمم آلية الجسم القديم حرفياً على كل امتداد.

| التوسعة | الأصل | المشاهدة الإضافية ودليلها | الاستكمال المقترح |
|---|---|---|---|
| EX7B7-01 | P1-004 | CostCenter يحمل REPX فعلاً عبر FromFile، وكذلك InvsProfit؛ كلاهما يحتاج أصولاً خارج اللقطة. هذا ليس فحص REPX غير مستعمل مثل P7-097.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:692-766`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:895-950` | manifest موثوق بإصدارات schema/DTO/قالب ومستهلك؛ لا تشغيل قالب مجهول أو استنساخ تبعية مفقودة بملف وهمي. |
| EX7B7-02 | P1-011 | cmbAccounts editable؛ Enter ينقل Text إلى SrchName ثم AName=N'...' في SQL دون parameter. اسم عادي يحوي apostrophe يكسر الحد النصي، والتحكم بالمدخل مثبت محلياً؛ لا payload استغلال أو تنفيذ SQL.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:845-862`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml:302-309` | مرّر الاسم بمعامل NVarChar، وثبت نطاق الحساب/الفرع مستقلاً؛ apostrophe مشروع لا يحذف من اسم الأعمال. |
| EX7B7-03 | P1-013 | مداخل Home للكلفة/الأرباح/افتراضي الطباعة تعرض دون Apply محلي؛ فتح تفاصيل الأرباح يطبق ApplyPermission/DoApply قبل Show كشاهد مقابل. لا استنتاج لنتيجة visual-tree الفعلية أو ضابط خادم من هذا وحده؛ potential محفوظة.<br>`SmartAuditERP/Home.xaml.cs:2642-2647`؛ `SmartAuditERP/Home.xaml.cs:3541-3541`؛ `SmartAuditERP/Home.xaml.cs:3766-3766`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:605-627` | تفويض أوامر وقراءة/تصدير/تكلفة مركزي قابل للاختبار، لا مجرد توقيت تطبيق UI؛ لا ترقية potential ببحث أسماء. |
| EX7B7-04 | P1-030 | Home يحتفظ بنسخة frmInvRptType static ثم ShowDialog، وزر الخروج Close؛ الاستدعاء التالي يعيد نفس النسخة المغلقة. النوافذ الجديدة للكلفة/الأرباح شواهد مضادة لا تعميم عليها.<br>`SmartAuditERP/Home.xaml.cs:194-195`؛ `SmartAuditERP/Home.xaml.cs:3766-3766`؛ `SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs:33-36` | إنشاء instance بعد Closed أو سياسة Hide ودورة جلسة صريحة؛ لا تبديل reference التطبيق أو إخفاء الخطأ. |
| EX7B7-05 | P1-033 | زرا معاينة/طباعة تقرير إجمالي عميل موصولان لمعالجين فارغين فعلاً، لا تقرير مكتمل من اسم الشاشة ولا finding لكل handler.<br>`SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:265-270`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml:257-259` | نفذ القدرة المطلوبة أو عطلها بوضوح وفق قرار متطلب؛ لا مخرج وهمي ولا عد نتائج بحسب عدد الأزرار. |
| EX7B7-06 | P2-001 | إعادة احتساب التكلفة تكتب عبر UpdateItemCost من زر خاص يظهر عند غير المعالج؛ لا حارس صلاحية أمر داخل الدالة. مصنف UI العام لا يطابق اسم btnRecalculateCost؛ لا نثبت أن دوراً إنتاجياً معيناً يستطيع الوصول أو أن خادماً خارجياً بلا ضابط.<br>`SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:775-888`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml:490-497`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml:733-739`؛ `SmartAuditERP/Class/MainClass.cs:433-444`؛ `SmartAuditERP/Home.xaml.cs:3541-3541` | CanRevalueCost في حد موثوق مع نطاق فرع/مستند/سطر وإصدار وسجل/فترة؛ اختبار الرفض عبر كل مدخل لا إخفاء زر فقط. |
| EX7B7-07 | P2-010 | BuildBranchFilter في الكلفة يرجع فارغاً عند عدم اختيار فرع ولو الكل غير محدد؛ بحث الحساب لا يعيد BranchCondition رغم loader المقيد. مصادر الأرباح/عميل تعتمد selection أوBranchNo ولا تثبت نطاق موارد مخول موحداً. BranchId موجود في DDL، فلا نسجل غيابه زوراً.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:136-189`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:369-379`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:845-891`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:161-198`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:706-714`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:155-190` | BranchScope مفوض لا fail-open مع null/كل؛ إعادة تحقق الحساب والفرع في القراءة والكتابة والفتح، مع توثيق id مقابل BranchId. |
| EX7B7-08 | P2-011 | LoadStores يجلب Safes النشطة دون تقاطع branch/تعيين المستخدم، ثم معيار الشاشة يرسل safe المختار. شرط status<>2 شاهد قائم لا يساوي العضوية المخولة.<br>`SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:148-158`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:730-736` | قائمة واختيار وقراءة نهائية تتقاطع مع الفرع والعضوية الفعلية؛ لا تعد صلاحية حقل id بحد ذاتها إذناً. |
| EX7B7-09 | P3-023 | الكلفة تبني نهاية23:59:59 وتستخدم<، فتسقط هذا الوقت وما بعده بدقةdatetime؛ الأرباح وعميل تضيفان يوماً وتستعملان<= فتضمان منتصف ليل اليوم التالي. معاملات عميل DateTime تسند نصوصاً. ليست الحدود الثلاثة نفس اتجاه الخطأ.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:347-351`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:479-486`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:298-311`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:768-771`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:173-188`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:242-253` | [from,toExclusive) بمعاملات DateTime فعلية ومنطقة/دقة معلنتين؛ اختبر اللحظة الأخيرة ومنتصف الليل كلتيهما ولا تكتف بآخر دقيقة. |
| EX7B7-10 | P4-010 | مسار إعادة احتساب تقرير الأرباح يرسل UpdateItemCost بمفتاح InvGlobalID+ItemId فقط؛ تكرار الصنف بوحدتين/مخزنين يستهدف السطرين معاً. caller يمرر gid إلى تصحيح السالب: يحد الفواتير خلاف المسار التاريخي الواسع، فلا ننسب إليه تلقائياً كل امتداد خارج الفرع/الفاتورة.<br>`SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:809-880`؛ `SmartAuditERP/Class/StoredQueries.cs:26-28`؛ `SmartAuditERP/Class/InvoiceOper.cs:3131-3169`؛ `SmartAuditERP/Class/ItemOper.cs:288-379` | LineId/مخزن/وحدة/إصدار وعملية ذرية بسجل واعتماد، وسياسة تاريخ/تكلفة معتمدة؛ لا نعيد عد أصل هوية السطر أو نزعم عدم وجود قيد حارس بالمطلق. |
| EX7B7-11 | P7-040 | تقرير إجمالي عميل يجمع المبالغ داخل شرط netPQty!=0 أوnetSQty!=0؛ تساوي الشراء/مرتجعه كميةً مع اختلاف السعر يسقط الباقي النقدي، بعد عزل خطأ التصنيف P7-084.<br>`SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:201-225` | أهلية مبنية على حركات/مقاييس فعلية أو استبعاد معلن مع مصالحة؛ Q0 لا يعني M0. |
| EX7B7-12 | P7-041 | عميل يجمع val×exchange_price كالسوابق. وبالاتجاه المعاكس في آخر شراء للأرباح: RecentPurchPrice يعيد val1×exchange_price/val، أي سعر أساس، ثم يضربه التقرير في Qty=val1 لاval. عبوة10 وتكلفة أساس5 تعطي تكلفة5 لا50.<br>`SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:187-199`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:327-373`؛ `SmartAuditERP/Class/ItemOper.cs:196-211`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1598`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1407` | كمية/سعر متجانسان مع UnitEquality قبل التجميع؛ سعر الشراء الحالي يحتاج عقد وحدته منفصلاً. لا تغيّر gross/net أو سياسة تاريخ ضمن تصحيح وحدة. |
| EX7B7-13 | P7-045 | BindToData بالكلفة يقرأ المركز والتواريخ الحالية فوق grid سابق؛ BuildReportDataSet للأرباح يقرأ dates ونوع الدفع الحالي فوق _currentDataTable. إعادة احتساب التكلفة تنتهي برسالة دون إعادة ShowInvs/summary؛ لا لقطة طلب/نتيجة محكمة.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:591-625`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:969-984`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:1001-1017`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:875-888` | Criteria/result/version immutable أو dirty gate، وإبطال/إعادة تحميل بعد كتابة؛ لا وصف فترة أو مركز جديد فوق بيانات قديمة. |
| EX7B7-14 | P7-046 | فشل السابق في الكلفة يعودnull ثم يكمل الفترة؛ الأرباح تمسح Grid source لكن _currentDataTable لا يستبدل إلا عند النهاية، وفشل Fill/تحويل يترك جدول تحميل سابق قابلاً لمسار المخرج؛ أرصدة وعميل يبتلعان خطأ مصدر ويحتفظان بالصفر.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:383-459`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:280-285`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:460-467`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:564-571`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:895-906`؛ `SmartAuditERP/Form_WPF/frmItemsBalances.xaml.cs:123-160`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:242-263` | حالة result/error/partial واحدة ونشر ذرّي؛ فشل الاستعلام ليس صفراً ولا آخر نتيجة حالية؛ امنع المخرج النهائي أو علّم الجزئية صراحة. |
| EX7B7-15 | P7-048 | EscapeCsv بالكلفة يضاعف quote لكنه لا يحيط الخلية إذا كان quote وحده بلاcomma/CR/LF؛ a"b يصيرa""b غير مقتبس ولا round-trip حرفياً. InvsProfit يحيط كل خلية ويضاعف quote فعلاً، وهو شاهد مقابل لا تعميم فساد نحوي عليه.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:1101-1113`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:1130-1157`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:1026-1094` | encoder CSV مجرب بحالات quote-only/فواصل/أسطر وثقافات؛ احتفظ بترميز الأرباح الصحيح ولا تستبدله بحل أخطر. |
| EX7B7-16 | P7-049 | المصدران يكتبان نصوص أعمال إلى CSV ثم ShellExecute؛ حتى Csv الصحيح نحوياً في الأرباح لا يحسم تفسير بادئة صيغة عند مستهلك جداول. لا formula/Office أو script نفذ، وpotential محفوظة.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:926-943`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:1094-1157`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:565-587`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:1026-1094` | نص typed/سياسة مستهلك آمنة وعدم فتح تلقائي غير لازم؛ معيار ترميز CSV منفصل عن تحييد المحتوى النشط. |
| EX7B7-17 | P7-053 | افتتاحي كشف مركز التكلفة يرشح CCcode والفرع/التاريخ والحالة فقط؛ period يطبق acc_no وEntry.type المختارين. السابق لكل حسابات/أنواع المركز يختلط مع حركة حساب/نوع محدد؛ لا ندعي أنه يكرر أول حساب مثل الجسم التاريخي، بل امتداد فقد هوية/نطاق الافتتاحي نفسه.<br>`SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:258-276`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:354-366`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:383-411`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:466-476` | سابق وحركة على نفس المفاتيح والمعايير أو سابق كلي مسمى منفصلاً ومصالَح؛ لا تعديل النواة التاريخية لإخفاء اختلاف الآلية. |
| EX7B7-18 | P7-084 | أرصدة يقرر اتجاه الإضافة/الخصم بمزيج proc_type الرأس/السطر دونinv_type؛ مثال كميات شراء100/مرتجع20/بيع60/مرتجع10 يعطي50 لا30. عميل يضع normal+sub1 للشراء وreturn+sub1 لمرتجعه بلاinv_type؛ يعطي90/40 بدلاً من80/50 بقيم وحدة1.<br>`SmartAuditERP/Form_WPF/frmItemsBalances.xaml.cs:58-81`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:187-206`؛ `SmartAuditERP/Class/InvoiceOper.cs:1526-1534`؛ `SmartAuditERP/Class/InvoiceOper.cs:1583-1585`؛ `SmartAuditERP/Properties/Resources.resx:3028-3064` | كتالوج نوع/رأس/أثر وإشارة واحد، ونطاق مستندات معلن؛ لا تصحيح الأرقام بقلب اتجاه واحد دون جدول حالات. P4-001 حاجز الكاتب المرتبط لا يفترض حدوثه. |

## 5. شواهد مقابلة وحدود تمنع نتائج مضخمة

1. **كل الفروع في InvsProfit يمسح SelectedIndex فعلاً**؛ لا تمديد P7-088 لهذا الجسم. BranchId موجود في DDL المحلي؛ عدم وحدة semantics معid سؤال عقد لا غياب عمود مزعوم. الدليل: `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:676-682`؛ `SmartAuditERP/Properties/Resources.resx:242-248`.
2. **DTO الطباعة في الأرباح يحمل الفروق signed صراحة**؛ لا P7-093 هنا. P7-101 خاص بانقطاع ربط UI Custom، لا فراغ هذه الحقول في REPX أو تنبؤ default SDK. الدليل: `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:1001-1017`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml:413-439`.
3. **الكلفة تعيد subNotes في التجميعي وتقيد Entry.state=1 وIS_Deleted=0**؛ لا تكرار P3-022 أو ادعاء كل الحراس مفقودة. تعارض السابق/الفترة P7-053 مستقل. الدليل: `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:466-476`.
4. **CSV الأرباح يحيط كل حقل ويضاعفquote**؛ لا نضيفه إلى فساد النحو P7-048. يبقى المحتوى النشط P7-049 محتملاً بحسب المستهلك. الدليل: `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:1076-1080`.
5. **الطباعة بالكلفة/الأرباح تحمل REPX فعلاً وتطبق PrintNo بحلقة**؛ ليست بوابة قالب غير مستخدم P7-097. لا يحسم ذلك مورد القالب/DTO/الترويسة/الوجهة أو خروج ورق. الدليل: `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:743-795`؛ `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:921-962`.
6. **عميل يقرأ ويحدّث controls عبر Dispatcher**؛ لا تعميم P7-054 لمجرد Thread. بقاء الزر فعالاً/اتصال مشترك وتكرار المصادر leads إلى7C لا قياس تداخل أو تسرب مثبت. الدليل: `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:133-180`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurchActCust.xaml.cs:211-237`.
7. **finally لإعداد الطباعة يغلق الاتصال**. الكتابة قيمة1/2 فعلياً ليست stub. غياب read ونجاح0-row نتيجتان مستقلتان، وإعادة إظهار Closed أصلP1-030 ولا يلغي مشكلة الفتح الأول. الدليل: `SmartAuditERP/Form_WPF/frmInvRptType.xaml.cs:38-68`.
8. **إتاحة أرصدة المواد وعميل غير محسومة هنا**. موضعا أرصدة المكتشفان ينشئان نافذة جديدة لإغلاقها، لا CalcStock/Show. لا نعتبر البحث النصي call graph كاملاً أو نضيف caller بهدف الوصول إلى اختبار. الدليل: `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:289-295`؛ `SmartAuditERP/Form_WPF/frmPOS.xaml.cs:293-298`.
9. **caller إعادة تقييم الأرباح يمرر GID لتصحيح السالب**؛ يقيد الفواتير، فلا ننسب له آلياً كل توسع P4-010 خارج الفاتورة. يبقى استهداف ItemId بدلLineId مثبتاً محلياً، والأساس التاريخي/المخزن/الذرية/الصلاحية بحاجة عقد. الدليل: `SmartAuditERP/Form_WPF/frmInvsProfit.xaml.cs:809-880`؛ `SmartAuditERP/Class/StoredQueries.cs:26-28`.

## 6. التحقق والباقي

<!-- B7-VERIFICATION-RESULTS -->
**اجتاز التحقق الوثائقي الحالي فعلياً:**827 مسار تطبيق وبصماتها الأصلية، و223 ملفاً تاريخياً محمياً، وحفظ270 نواة وكل `next_phase` وG01–116. فُحص 18,193 مرجع نطاق و2,554 رابط محلي، بما في ذلك التكرارات، وفُحصت الصياغة النحوية لـ30 أداة تدقيق مكتوبة بلغة Python. **اجتازت156 حالة اصطناعية للمدقق**:132 تاريخية محمية+24 جديدة؛ ليست اختباراتERP أو37 قبولاً ناجحاً.

أُعيد توليد22 نموذجاً يدوياً و22 ملاحظة نصية محدودة ومطابقتها بسجلها الفعلي. نجحت12 واجهةCLI تاريخية منفصلة للمراحل2–6 وA/B1–B6 بمدخلاتها الخاصة. **كل قبول/تشغيلERP أوSQL أوOffice أوصيغة أوSDK/جهاز/مزود ومعالجة=0**؛7C لم تبدأ و8 غير مأذونة.

[checksB7 الفعلي](evidence/checks-07B7.json) محفوظ منstdout بعدexit0 و`errors=[]` و`pending=false`، لا حقول نجاح مدخلة يدوياً. SHA256=`25043dbf69013f010a3f063938ea5377862bb9c11d02ea01447a5d51a7ded5c3`. أُعيدت مقارنة stdout بهذا السجل حرفياً فطابقه؛ ذلك اتساق أداة الوثائق، لا شهادة مالية أو اكتمال للجزء7B أو المرحلة7.

<!-- END-B7-VERIFICATION-RESULTS -->

- [نموذج المصادر/FE31/INV31/RC8 وH/Q/backlog](FINANCIAL-CONTROLS-07B7.md)، [قبول37 وحدود المدقق](VALIDATION-07B7.md).
- [witness22+22 الفعلي](evidence/report-witnesses-07B7.json)، [checksB7 الفعلي](evidence/checks-07B7.json)، [لقطة270](evidence/findings-through-07B6.csv) و[توسعات18 الدقيقة](evidence/historical-extensions-07B7.csv).
- **التالي7B8 ضمن إذن تدقيق7**:DecisionHelp/SummaryD/UsersRecords وبقية المالية/الإخراج/nonregex/الأطفال والمتصلين، أو استبعاد مسند/جزء معلن؛ ثم7C التي لم تبدأ. لا اكتمال7B/7 من union363 أو خطة/فحصPython أو pushتوثيق.
- لا طلب أسرار أو قواعد/أشخاص إنتاج. H/Q السابقة باقية وتضاف H7B7/Q7B7، وأي قياس/SQL plans/latency/leak يحتاج متطلبات وإذناً مناسبين، لا حكم نصي.

[الفهرس](README.md) · [الخطة](PLAN.md) · [التحسينات](IMPROVEMENTS.md) · [سجل النتائج](findings.csv)
