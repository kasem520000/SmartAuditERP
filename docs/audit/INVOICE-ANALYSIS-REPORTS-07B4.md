# نموذج مصادر ومصالحة التقارير الأربعة —7B4 الجزئية

**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`، الفرع `arena/94ae8414-smartauditerp`.  
**مرجع التدقيق المعلن:** 2026-11-16 UTC. ملاحظة ساعة البيئة عند دخول هذا الجزء `2026-11-18T00:17:24+00:00` محفوظة منفصلة في provenance؛ ليست تاريخ تشغيل ERP أو إعادة تأريخ للتاريخ المحمي.  
**الحالة:** استمرار ساكن ضمن إذن المرحلة 7؛ لا معالجة للشيفرة أو تشغيل النظام أو إذن المرحلة 8.

هذا **نموذج مصدر وهوية ووحدة ومعايير وحالة ومجاميع وإخراج**، لا مصالحة مالية منفذة أو تصديق للقوالب/الخادم. [تقرير النتائج](PHASE-07B4.md) يحدد 13 نتيجة جديدة و 17 توسعة. لا تغطي الأجسام الأربعة كل callers أو 7B5 أو 7C، و 8 غير مأذونة.

## 1. قواعد مرجع المصالحة

1. عرّف المقياس: gross أو net، مبلغ رأس أوحصة بند، كمية أساس أوكمية وحدة بيع، تكلفة وحدة أوإجمالي، حركة موجبة أوأثر signed. الاسم ليس هوية أو سياسة.
2. ثبت GlobalID/LineId/InvoiceType/ProcType/Branch/Store/Treasury والإصدار والحالة؛ احسم cardinality قبل الانضمامات. المخطط المرفق ليس مخطط النشر.
3. اعتمد مرجع تكلفة/ضريبة/خصم/تقريب مستقل، لا آخر قيمة أوفرق لإجبار التوازن. val الأساسية لا تضرب سعر وحدةبيع بلا تحويل متجانس.
4. طبق كل معيار متاح على مصدر مؤهل موحد قبل التجميع مع تقاطع التفويض، وحدود زمن نصف مفتوحة؛ احفظ المعايير والنتيجة snapshot واحدة.
5. سجل حواجز الخيط والإتاحة والبناء قبل الحساب downstream؛ Empty و Error و Partial و 0 حالات مختلفة. لا تعتبر منع التشغيل نجاح أرقام.
6. صالِح المصدر مع المستند ثم GL بحسب السياسة، ثم count/identity/amounts قبل renderer. القالب والخلايا والملف وحدود الثقة اختبارات أخرى بإذن 8، لا حفظ/ترحيل لتصحيح ورقة.

## 2. مصفوفة ميزة×شاشة×تنفيذ×خطة

[CSV36](evidence/feature-implementation-matrix-07B4.csv) يحفظ الأدلة والحدود والخطط في الاتجاهين:1–13 للجديد، 14–30 لتوسعات الأصول، 31–32 شواهد مقابلة، 33 عقد إشعار 22 غير محسوم، 34 مؤشر موارد/أداء لا قياس، 35–36 حصر مؤجل لا تنفيذ مراجع. **36 صفاً ليست 36 ميزة مكتملة**؛ كلها not-executed.

| الصف — القدرة | الشاشة والمدخل | المشاهدة المحلية | مستوى التغطية والحالة | خطط غير منفذة |
|---|---|---|---|---|
| FE7B4-01 — حاسبتا تكلفة تحليل الفواتير تقربان كمية المقام إلى عدد صحيح قبل القسمة | frmRptInvAnalysis؛ CalcUnitCost / CalcUnitCostStock → int totalQty → netCost/netProfit | كل حاسبة تجمع تكلفة double لكنها تعرف totalQty من int، ثم تضيف (int)Math.Round(q) لكل مجموع كميات. إذا صار المقام 0 تنتقل إلى Items.purch_price. val في الكاتب و DDL كمية float/أساس تقبل الكسور، لا عد قطع صحيحاً مضموناً. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-01;P7B4T-02;P7B4T-44 |
| FE7B4-02 — تجميع الصنف في تحليل الفواتير يطبق آخر تكلفة مقروءة على كامل كمية الفترة | frmRptInvAnalysis؛ ShowResultItem → GROUP BY ItemId/date → lastUnitCost → totalQtyForCost × lastUnitCost | داخل حلقة تواريخ الصنف تجمع totalQtyForCost وتستبدل lastUnitCost كل مرة، وبعدها تحسب netCost=totalQtyForCost*lastUnitCost. الاستعلام GROUP BY ItemId,date بلا ORDER BY. تجميع المجموعة والعميل، بالمقابل، يجمع rowQty*unitCost لكل تاريخ. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-03;P7B4T-04;P7B4T-44 |
| FE7B4-03 — التجميع الشهري لتحليل الفواتير يوسع الفترة المطلوبة إلى حدود الشهر دون تقاطع | frmRptInvAnalysis؛ ShowResultMonth → شهر مرشح → monthStart/monthEnd → استعلامات التفاصيل | الاستعلام الأول يحدد الأشهر التي لها حركة ضمن الفترة، ثم كل استعلام عدد/رأس/تكلفة يستبدل البداية بأول الشهر والنهاية بآخر يوم منه، دون Max مع dateFrom أو Min مع dateTo. لهذا يمكن أن تدخل حركات قبل البداية وبعد النهاية المطلوبة. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-05;P7B4T-06 |
| FE7B4-04 — مرشح المستخدم ومعيار المجموعة لا يطبقان في تجميعات من تحليل الفواتير | frmRptInvAnalysis؛ اختيار Emp/Group → ShowResult validations → فلاتر ShowResult* اليدوية | ShowResult يفرض اختيار المستخدم عند إلغاء الكل، لكن sales_emp لا يدخل إلا في ShowResultEmp؛ بقية التجميعات السبعة لا تطبق الاختيار. وفي ShowResultGroup يعدد كل ItemsCategory دون قراءة chkAllGroups/cmbGroups، خلاف تطبيق معيار المجموعة في بقية الأبعاد. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-07;P7B4T-08 |
| FE7B4-05 — تجميع المخزن في تحليل الفواتير يبني مرشح الخزينة من قيمة المستودع | frmRptInvAnalysis؛ ShowResultStock → safeVal / stockSelVal → [stock]=stockSelVal | ShowResultStock يقرأ safeVal من cmbSafe لكنه لا يستعمله؛ عند !allSafe يضع [stock]={stockSelVal} المأخوذ من cmbStock. الحقل Inv.stock هو Treasury و Inv.safe هو Store في الكاتب؛ بقية الأبعاد تستعمل safeVal للخزينة. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-09;P7B4T-10 |
| FE7B4-06 — مرشح الفئة في تحليل الفواتير يبقي صافي الرأس كاملاً مقابل تكلفة البنود المصفاة | frmRptInvAnalysis؛ ShowResultCust/Salesman/Emp/Month/Day/Stock → MIN(header) per GlobalID مقابل تفاصيل الفئة | بعد ترشيح ItemsCategory.id تجلب مصادر المبلغ MIN(tot_net)/MIN(InvTotal) لكل InvGlobalID ثم تجمع الرأس كاملاً، بينما مصدر الكمية/التكلفة تحت الفلتر يحوي بنود الفئة فقط. MIN يزيل ضرب join لكنه لا يخصص مبلغ الرأس للبنود المختارة. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-11;P7B4T-12;P7B4T-44 |
| FE7B4-07 — تجميعا الصنف والمجموعة في تحليل الفواتير يعرضان المجموع قبل الخصم والخصم صفراً | frmRptInvAnalysis؛ ShowResultGroup / ShowResultItem → sum(val1*exchange_price) → netDiscount=0 → netProfit | مصدر الإجمالي في البعدين SUM(val1*exchange_price) دون discount أو minus، ويثبت netDiscount=0. ثم يطرح التكلفة من هذا المجموع ويسند الناتج لأعمدة صافي الإجمالي وصافي الخصم وصافي الربح. الخصم محفوظ حقلاً مستقلاً في المصدر. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-13;P7B4T-14;P7B4T-44 |
| FE7B4-08 — شروط نوع واتجاه تحليل الفواتير تسقط المرتجع وبيع POS العادي من صافي المخزن | frmRptInvAnalysis؛ ShowResult* eligibility predicates → quantities/amounts/costs | تجميعات غير المخزن تشترط رأس proc_type=1 وسطر proc_type=2 فقط ولا تنشئ طرحاً لرأس المرتجع 2. مسار المخزن يقرأ البيع 2/رأس 1/سطر 2، لكنه يسمي فرع inv_type=3 ورأس 1 وسطر 3 مرتجعات ويضيف مبلغه؛ POS العادي له سطر 2 والمرتجع رأس 2 وفق العقود المرفقة. مصدر تكلفة المخزن أوسع من مصدر مبلغه ولا يقيد inv_type=2. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-15;P7B4T-16;P7B4T-44;P7B4T-45 |
| FE7B4-09 — تعديل نص الصنف في الأرباح التفصيلية يبقي SelectedId السابق عند عرض التقرير | frmRptItemsProfitDetails؛ تعديل txtItemName/Code دون Enter → bntShow → WHERE ItemId=SelectedId → عنوان الإخراج | حل الاسم/الرمز يحدث عند Enter أو حوار البحث؛ حقلا النص قابلان للتحرير بعد إلغاء الكل ولا TextChanged يبطل SelectedId. زر العرض يتحقق من اسم غير فارغ فقط، ثم يبني الشرط من SelectedId. الطباعة تنقل اسم/رمز controls الحاليين. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-17;P7B4T-18;P7B4T-44 |
| FE7B4-10 — قارئ إشعارات الفواتير يطرح الضريبة الإضافية من VAT المحفوظة كحقل مستقل | frmRptInvNotfic؛ Inv.tax / ExtraVAT → BindingListOfInvoices1 → VAT/TotalTax → grid/summaries/CSV | يسمي القارئ row[tax] taxTotal ويضع TotalTax=taxTotal، ثم VAT=taxTotal-extraVAT إذا كان الفرق موجباً. الكاتب يضع inv.VAT في tax و inv.ExtraVAT في ExtraVAT، والحاسبة تجمع vat و extraVat منفصلين ثم Net=Total+VAT+ExtraVAT؛ ليست tax في هذا العقد مجموع الضريبتين. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-19;P7B4T-20;P7B4T-45 |
| FE7B4-11 — تفاصيل المشتريات تربط معرف المستودع بجدول الخزائن عند جلب الاسم | frmRptInvPurchaseDetails؛ LoadData.Invertories → Inv.safe → BuildOptimizedSql JOIN Stocks → InvertoryName | المرشح يقرأ المستودعات من Safes و Inv.safe يكتب من Store، لكن الاستعلام المحسن يربط Stocks.id=inv.safe ويسمي الناتج StoreName ثم InvertoryName. Stocks للخزائن في العقد المحلي لا المستودعات. overrideSql يستعمل Common.GetStoreName الذي يقرأ Safes، وهو شاهد مقابل. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-21;P7B4T-22 |
| FE7B4-12 — خيار كل الفروع في تفاصيل المشتريات يبقي قيد الفرع المختار سابقاً | frmRptInvPurchaseDetails؛ chkAllBranches_Changed → cmbBranches enabled only → CollectQueryParams SelectedIndex | معالج كل الفروع يغير IsEnabled فقط ولا يمسح الاختيار. CollectQueryParams يضيف inv.branch عند SelectedIndex>-1 دون فحص chkAllBranches، لذلك يبقى الفرع السابق فعالاً بعد تحديد الكل. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-23;P7B4T-24 |
| FE7B4-13 — منتقيا تاريخ تحليل الفواتير موضوعان في خلية Grid نفسها | frmRptInvAnalysis؛ XAML Grid.Row1 → txtDateFrom / txtDateTo default Grid.Column0 | Grid التواريخ يعرّف أعمدة متعددة لكن DatePicker للبداية و DatePicker للنهاية ابنان مباشران بلا Grid.Column أو Margin مختلف أو صف منفصل. فيقعان معاً في الخلية الافتراضية 0؛ المستخدم والعميل فقط لهما 4 و 6. يقرأ C# تاريخين مستقلين رغم عدم فصلهما تخطيطياً. | selected-source-slices-not-whole-feature-certification؛ implemented-with-observed-defects | P7B4T-25;P7B4T-26 |
| FE7B4-14 — انحدار أصل P1-004 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | متصلون إضافيون وقوالب REPX مسماة؛ توريدها وإصدارها وعقد بياناتها غير مثبتة من وجود FromFile أو مسار. لا نقص مستقل لكل اسم. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-27 |
| FE7B4-15 — انحدار أصل P1-011 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | يدخل اسم/رمز TextBox في SELECT Items داخل literal SQL دون معاملات. هذه توسعة مصدر→مصَب للجذر السابق؛ لا payload أو اتصال SQL نفذ، ولا يخلط بـ DataView. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-28 |
| FE7B4-16 — انحدار أصل P1-013 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | تحليل الفواتير يستدعي ApplyPermissionToForm قبل Show، ومدخله معطل أولياً؛ مداخل الأرباح/الإشعارات/المشتريات المختارة لا تستدعي الحارس هنا. لا يثبت أي منهما صلاحية أو منعاً مركزياً. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-29 |
| FE7B4-17 — انحدار أصل P1-033 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | زر حفظ المظهر يكتب XML ويعلن الحفظ، لكن LoadDGvSetting يفحص وجود الملف فقط دون استعادة الأعمدة. هذا امتداد أصل الاكتمال، لا عيب لكل معالج RadioButton فارغ؛ زر العرض ينفذ الأبعاد فعلياً. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-30 |
| FE7B4-18 — انحدار أصل P2-001 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | الفتح من الأرباح ينفذ configure/Navigate قبل Show بلا إعادة تفويض محلية؛ فتح المشتريات بلا ApplyPermission هنا. بعض مداخل الإشعار تستدعي الحارس قبل تغيير الاسم ثم Show، وتفاصيله تظهر زر إعادة التكلفة بعده. لا دليل على تنفيذ إعادة التكلفة أو تخطي خادم فعلي. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-31 |
| FE7B4-19 — انحدار أصل P2-010 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | تحليل الفواتير والإشعارات لا يضيفان branch في المصادر المحددة، مقابل حارس BranchNo في الأرباح ومنطق خيارات في المشتريات. غياب/اختلاف scope محلي لا يثبت ACL منشوراً أو إذن الكل. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-32 |
| FE7B4-20 — انحدار أصل P2-011 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | تحميل مواقع عام في التحليل والأرباح مقابل LoadData.Invertories(EmpNo) في المشتريات؛ خيار كل المستودعات يزيل فلتر SQL المحلي ولا يثبت تقاطع تعيينات المورد. لا تعد حصر الأسماء سياسة authorization. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-33 |
| FE7B4-21 — انحدار أصل P3-023 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | نهاية الشهر عند 00:00 تسقط بقية آخر يوم، واليوم المنتهي <=غد 00:00 قد يكرر حد منتصف الليل؛ نهاية 23:59 الصريحة في الأرباح والإشعارات والمشتريات تستبعد ثواني الدقيقة الأخيرة. توسيع الشهر P7-079 مستقل عن هذا cutoff. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-34 |
| FE7B4-22 — انحدار أصل P4-007 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | CalcUnitCost يجمع رأس 1/سطر 1 بلا inv_type=1 فيخلط مصادر دخول منها غير الشراء؛ مسار المرتجع يطلب رأس proc_type3 لا 2 ويضيفه. يقيد CalcUnitCostStock النوع 1 لكنه يكرر proc3. أثر سياسة التكلفة يبقى potential كما كان؛ لا يثبت هذا متوسطاً تاريخياً معتمداً. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-35 |
| FE7B4-23 — انحدار أصل P7-041 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | بسط التكلفة SUM(val*exchange_price) يضرب كمية الأساس بسعر وحدة البيع لا val1؛ عبوة 10 بسعر 50 تعطي تكلفة أساس 50 بدلاً من 5، أي عشرة أضعاف. امتداد الجذر الوحداتي لا نتيجة جديدة، مع بقاء أخطاء المصدر والدقة منفصلة. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-36 |
| FE7B4-24 — انحدار أصل P7-045 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | مصادر الطباعة تقرأ معايير controls الحالية مع صفوف وملخصات التحميل السابق؛ المشتريات تلتقط DTO على UI للعامل وهو شاهد مقابل للخيط، لكنها لا تجمد عنوان الإخراج مع النتيجة. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-37 |
| FE7B4-25 — انحدار أصل P7-046 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | قد تسقط صفوف الإشعارات والمشتريات في catch{} ثم تعاد قائمة دون عد الرفض؛ الأرباح تمسح القائمة داخل try وقبل الاستعلام، وقد تبقي ملخصاً قديماً عند الفشل. لا يعني كل empty خطأ، ولا Progress100 اكتمال المال. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-38;P7B4T-46 |
| FE7B4-26 — انحدار أصل P7-048 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | CSV الأرباح والإشعارات يدمج نصوصاً و N2 مفصولة بفواصل دون quoting أو escaping؛ فاصل أو سطر داخل اسم أو فاصلة ألوف تغير الأعمدة. TSV المشتريات مسجل سلفاً ولا يعاد عده. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-39;P7B4T-46 |
| FE7B4-27 — انحدار أصل P7-049 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | نصوص غير موثوقة تكتب CSV أو تسند إلى خلايا COM بلا سياسة نص/صيغة صريحة؛ الأثر مشروط بقارئ Excel وإعداداته. تبقى potential؛ لم يفتح ملف أو تفسر صيغة أو يشغل COM. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-40;P7B4T-46 |
| FE7B4-28 — انحدار أصل P7-054 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | زر التحليل يبدأ new Thread ثم يقرأ ShowResult قيم IsChecked/SelectedValue قبل Dispatcher وقبل try. مساعدات Dispatcher اللاحقة لا تصلح الحارس الأول. التقاط QueryParams في المشتريات على UI قبل Task.Run شاهد مقابل، لا عيب جديد ثانٍ. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-41 |
| FE7B4-29 — انحدار أصل P7-055 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | طباعة الإشعارات تمرر null إلى BindToData مع تواريخ فقط لا_invoicesList؛ تجعل overloads لـ GridView/DataTable عقد البناء والحسم حاجزاً أسبق، ثم null لا يمثل الصفوف. لا ادعاء صفحة فارغة مرصودة أو DTO مفقود. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-42 |
| FE7B4-30 — انحدار أصل P7-061 | مقاطع B4 المحددة في الدليل؛ متصل محلي → مصدر/معيار/مخرج؛ لا تغطية انتقالية للأبناء | الأرباح التفصيلية توجه فتح الفاتورة بمقارنة أسماء عربية، فيبقى النص المترجم دون فرع مطابق. GlobalID محفوظ ومستعمل هنا، فيقاوم جزء فقد الفرع/الرقم المحلي من الأصل ولا ينسب ذلك الجزء لهذا المتصل. لا نوع رقمي في DTO لتوجيه مستقل عن اللغة. | selected-source-slices-not-whole-feature-certification؛ rechecked-prior-root-not-new-finding | P7B4T-43 |
| FE7B4-31 — الأرباح التفصيلية: فصل تكلفة الوحدة والإجمالي وخصم مرة وطرح المرتجع | frmRptItemsProfitDetails؛ ShowResult → DgvAvgCost / DgvTotAvg → UpdateSummaryCards | DgvAvgCost من AvrgCost و DgvTotAvg من val*AvrgCost، و discount يضاف مرة واحدة قبل netSum في المسار الموحد؛ الملخص sales.Sum-returns.Sum بهوية DgvIsPlus. لا تمتد آلياً P7-038/039 من تقرير الأرباح الآخر؛ وحدة عرض متوسط التكلفة بالنسبة لوحدة البيع وعقد التقريب ما زالا مطلوبين. | selected-source-slices-not-whole-feature-certification؛ counterevidence-not-global-closure | P7B4T-44 |
| FE7B4-32 — المشتريات: التقاط UI للعامل واتصال محلي وطرح المرتجع | frmRptInvPurchaseDetails؛ CollectQueryParams على UI → Task.Run → bgConn باستخدام using → Dispatcher publication | المعايير تجمع على UI قبل Task.Run، والاتصال المحلي using، والملخص يطرح proc2 من proc1. هذا يقاوم تعميم P7-054 أو جمع المرتجع موجباً هنا، لكنه لا يثبت snapshot عنوان ثابتة أو كشف صفوف catch المرفوضة. | selected-source-slices-not-whole-feature-certification؛ counterevidence-not-global-closure | P7B4T-44 |
| FE7B4-33 — إشعارات 22: فصل الأسماء بين seed وقارئ التسمية وفلتر التقرير | frmRptInvNotfic / InvoiceOper / InvTypes؛ نوع 22 → قائمة مدين/دائن → proc2/proc1 → GetInvoiceType و InvTypes seed | GetInvoiceType يسمي 22/1 دائناً و 22/2 مديناً، فيوافق قائمة التقرير وفتحها؛ seed InvTypes المرفق يسمي 22/1 مديناً و 22/2 دائناً. لا نختار الاتجاه المحاسبي الصحيح من الاسم أو نقلب الفلتر عشوائياً. ملخص الإشعارات يجمع المقادير موجباً عند عرض النوعين؛ هل المطلوب حركة إجمالية أم أثر صافٍ قرار سياسة، لا عيب إشارة محسوم. | selected-source-slices-not-whole-feature-certification؛ reviewed-contract-unresolved-not-global-absence | P7B4T-45 |
| FE7B4-34 — الإخراج و COM ومصادر الأداء: مؤشرات فقط لا قياس أو تسرب مرصود | frmRptInvAnalysis / frmRptItemsProfitDetails؛ Fill داخل أبعاد/تواريخ → lookups، و Export → COM dynamic cells/SaveAs | التحليل ينفذ عدة Fill لكل عضو ثم حاسبة تكلفة لكل صنف/تاريخ، والأرباح تجلب InvTypes و lookups داخل الحلقة. COM ينشئ application/workbook قبل try الداخلي، و return عند فشل الخلايا يسبق Close/Quit، ولا finally شامل. هذه إحالة 7C لتحديد عمر الموارد/الإلغاء والعدادات؛ لا Excel شغل أو تسرب/زمن/فهرس ناقص أثبت. | selected-source-slices-not-whole-feature-certification؛ source-only-resource-performance-lead-not-runtime-measured | P7B4T-46 |
| FE7B4-35 — حد حصر مؤجل 7B5 | مرشحون من inventory لا implementation جديدة؛ غير منتقى؛ لا متصل مفترض أو تغطية أبناء من launcher | بقية أجسام البيع و POS و Android وبيع الأصناف والمقاطع المالية/الإخراج ومرشحو غير regex وأبناء frmNkdFoundRpt لم يراجعوا في B4؛ أعلن B5 ولا تدع اكتمال التقارير. | inventory-only-not-implementation-reviewed؛ deferred-not-implementation-reviewed | P7B4T-47 |
| FE7B4-36 — حد حصر مؤجل 7C/8 | مرشحون من inventory لا implementation جديدة؛ غير منتقى؛ لا متصل مفترض أو تغطية أبناء من launcher | بقية HR/PM/البحري و UI/events/resources/RTL/accessibility/cultures والأداء لم تبدأ 7C، و 8 غير مأذونة. وجود مؤشرات B4 لا يرقّي الحصر إلى مراجعة أو يجيز تشغيلها. | inventory-only-not-implementation-reviewed؛ deferred-not-implementation-reviewed | P7B4T-48 |

## 3. الثوابت المطلوبة — ليست خصائص اجتازت اختباراً

[CSV22](evidence/report-invariants-07B4.csv) يحفظ الأدلة. هذه شروط قبول مستقبلية لا ضمانات منفذة:

| المعرف | الثابت المطلوب | النتائج/الإحالة | قبول غير منفذ |
|---|---|---|---|
| INV7B4-01 | حاسبتا تكلفة تحليل الفواتير تقربان كمية المقام إلى عدد صحيح قبل القسمة — الثابت المعاكس المطلوب؛ احتفظ بكمية دقيقة وواحدة الوحدات حتى القسمة مع سياسة حد الصفر والدقة؛ سجل سبب fallback ولا تستبدل كمية موجبة بصفر. ثم اعتمد سياسة مصدر التكلفة مستقلة عن هذا الخلل. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-077 | P7B4T-01;P7B4T-02 |
| INV7B4-02 | تجميع الصنف في تحليل الفواتير يطبق آخر تكلفة مقروءة على كامل كمية الفترة — الثابت المعاكس المطلوب؛ اجمع تكلفة كل كمية مع مرجعها الزمني/سطرها وفق السياسة، أو اقرأ تكلفة محفوظة صحيحة بإصدار؛ لا تعالج بتغيير ORDER BY فقط. اختبر invariance لإعادة الترتيب وتغيير بعد التجميع. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-078 | P7B4T-03;P7B4T-04 |
| INV7B4-03 | التجميع الشهري لتحليل الفواتير يوسع الفترة المطلوبة إلى حدود الشهر دون تقاطع — الثابت المعاكس المطلوب؛ احسب كل bucket كتقاطع [max(requestFrom,monthStart),min(requestToExclusive,nextMonthStart)) مع الفترة المعتمدة، وطبق التقاطع نفسه على العدد والمبلغ والتكلفة والعنوان. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-079 | P7B4T-05;P7B4T-06 |
| INV7B4-04 | مرشح المستخدم ومعيار المجموعة لا يطبقان في تجميعات من تحليل الفواتير — الثابت المعاكس المطلوب؛ ReportCriteria immutable واحد يطبق بالكامل على مصدر مؤهل قبل كل group-by، أو عطّل معياراً غير ذي معنى مع تفسير صريح. اختبر تقاطع كل criterion مع كل بعد، لا بعداً واحداً فقط. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-080 | P7B4T-07;P7B4T-08 |
| INV7B4-05 | تجميع المخزن في تحليل الفواتير يبني مرشح الخزينة من قيمة المستودع — الثابت المعاكس المطلوب؛ أنواع معرف WarehouseId/TreasuryId مختلفة، وربط criteria بالعمود الصحيح دون متغيرات متشابهة؛ افحص المعاملات بهويات غير متساوية ونطاق دور معلوم. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-081 | P7B4T-09;P7B4T-10 |
| INV7B4-06 | مرشح الفئة في تحليل الفواتير يبقي صافي الرأس كاملاً مقابل تكلفة البنود المصفاة — الثابت المعاكس المطلوب؛ اعتمد عقداً صريحاً: measure بنود الفئة بحصص خصم/ضريبة وتكلفة مقابلة، أو فواتير مؤهلة كاملة بكل تفاصيلها مع عنوان مختلف؛ لا تجمع رأساً كاملاً وتكلفة subset تحت صافي واحد. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-082 | P7B4T-11;P7B4T-12 |
| INV7B4-07 | تجميعا الصنف والمجموعة في تحليل الفواتير يعرضان المجموع قبل الخصم والخصم صفراً — الثابت المعاكس المطلوب؛ نموذج مبالغ معرف يحفظ Gross/LineDiscount/HeaderDiscountAllocation/Tax/Net/Cost؛ اجمع كل مكون وفق وحدة واحدة وإشارة معتمدة، وطابق بنود الصنف/المجموعة مع مرجع مستقل. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-083 | P7B4T-13;P7B4T-14 |
| INV7B4-08 | شروط نوع واتجاه تحليل الفواتير تسقط المرتجع وبيع POS العادي من صافي المخزن — الثابت المعاكس المطلوب؛ كتالوج موثق لـ InvoiceType/ProcType/InventoryImpact وحالة الأهلية وإشارة المبيعات والمرتجع؛ مصدر واحد لكل measures بالفلتر نفسه، ثم group-by دون أرقام magic أو فرع POS باسم مرتجع. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-084 | P7B4T-15;P7B4T-16 |
| INV7B4-09 | تعديل نص الصنف في الأرباح التفصيلية يبقي SelectedId السابق عند عرض التقرير — الثابت المعاكس المطلوب؛ SelectedItem typed غير قابل للتحرير الحر أو أبطل الهوية فور تعديل النص ثم أعد الحل النهائي مع تحقق موجود/مفوض؛ snapshot يحتفظ بهوية واسم المصدر لا مدخل غير محلول. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-085 | P7B4T-17;P7B4T-18 |
| INV7B4-10 | قارئ إشعارات الفواتير يطرح الضريبة الإضافية من VAT المحفوظة كحقل مستقل — الثابت المعاكس المطلوب؛ حسم schema/DTO بإصدار: OrdinaryVATAmount و AdditionalTaxAmount و TotalTaxAmount؛ اقرأ الأولين كما كتبا واشتق المجموع مرة أو اقرأ breakdown إصدار موثوقاً. لا تستنتج دلالة الحقل من اسمه وحده. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-086 | P7B4T-19;P7B4T-20 |
| INV7B4-11 | تفاصيل المشتريات تربط معرف المستودع بجدول الخزائن عند جلب الاسم — الثابت المعاكس المطلوب؛ JOIN Safes بهوية مستودع typed/alias ثابت؛ اختبر تطابقه مع lookup العقد القديم ومعرفات متباعدة، مع نطاق وصول محكم لا تصحيح الاسم وحده. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-087 | P7B4T-21;P7B4T-22 |
| INV7B4-12 | خيار كل الفروع في تفاصيل المشتريات يبقي قيد الفرع المختار سابقاً — الثابت المعاكس المطلوب؛ BranchScope صريح intersect مع الدور؛ الكل يزيل اختيار الفلتر داخل نطاق مصرح، أو تجاهل الاختيار عندما all=true، مع تحديث snapshot وإظهار النطاق الفعلي. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-088 | P7B4T-23;P7B4T-24 |
| INV7B4-13 | منتقيا تاريخ تحليل الفواتير موضوعان في خلية Grid نفسها — الثابت المعاكس المطلوب؛ Grid.Column0 و 2 منفصلان مع labels وربط وصول وترتيب تنقل مناسبين، ثم اختبار actual bounds/hit-test و RTL/DPI ولوحة المفاتيح. لا تكتف بوجود x:Name. لا يعد هذا الثابت مجتازاً من توضيح Python أو بحث نصي. | P7-089 | P7B4T-25;P7B4T-26 |
| INV7B4-14 | تفويض قبل القراءة والفتح والمخرج؛ تقاطع دور/فرع/مستودع/خزينة في حد موثوق، وإعادة تفويض هوية المستند قبل Navigate/Show؛ كل/لااختيار ليسا إذناً. | P1-013;P2-001;P2-010;P2-011 | P7B4T-29;P7B4T-31;P7B4T-32;P7B4T-33 |
| INV7B4-15 | حل هوية ومعاملات SQL للنصوص؛ اسم/رمز البحث نصوص معلّمة لا SQL، والحل يثبت الهوية الموجودة والمصرحة ويرفض stale/negative. | P1-011;P7-085 | P7B4T-28 |
| INV7B4-16 | لقطة immutable وحالة كاملة وخيط صحيح؛ التقط المعايير على UI مرة، ثم نتيجة كاملة/فارغة/جزئية/فشل منشورة ذرياً؛ الإخراج يستخدم معايير النتيجة لا controls الجديدة ولا يخفي صفوفاً مرفوضة. | P7-045;P7-046;P7-054 | P7B4T-34;P7B4T-37;P7B4T-38;P7B4T-41;P7B4T-44;P7B4T-46 |
| INV7B4-17 | مصدر تكلفة بوحدة ونوع/اتجاه وتاريخ معلوم؛ وحدة المقام والبسط متجانستان، وأهلية purchase/return/direction موثقة، وسياسة as-of/نطاق الموقع معلنة؛ لا إعادة تسعير صامتة من sale/return أو fallback. | P4-007;P7-041;P7-077;P7-078 | P7B4T-35;P7B4T-36;P7B4T-44 |
| INV7B4-18 | مخرج typed يساوي اللقطة ولا يعيد الأعمال؛ قالب موثوق بإصدار وصفوف/هوية/مجاميع متماثلة قبل renderer؛ لا BindToData(null) أو CSV خام أو نسبة مكان مبلغ أو فتح صيغة غير مقصودة. | P1-004;P7-048;P7-049;P7-055 | P7B4T-27;P7B4T-39;P7B4T-40;P7B4T-42;P7B4T-46 |
| INV7B4-19 | هوية مستند واتجاه مستقلان عن أسماء اللغة؛ GlobalID مع InvoiceType/ProcType/Branch بهوية typed؛ تسميات InvTypes/القارئ/المحرر متفقة بإصدار، والإشارة تعلن gross/net ولا تستنتج من label. | P7-061;P7-084;P7-086 | P7B4T-43;P7B4T-45 |
| INV7B4-20 | حفظ تفضيل له استعادة أو منع واضح؛ حفظ المظهر يليه round-trip إلى نافذة جديدة أو رسالة unsupported؛ handlers RadioButton الفارغة ليست نقصاً بذاتها إذا زر العرض ينفذ البعد. | P1-033 | P7B4T-30 |
| INV7B4-21 | نطاق جزئي لا يغطي الطفل أو الميزة انتقالياً؛ استكمل 7B5 أو استبعاداً مسنداً؛ 52 مرشح شاشة و 98 مرشح ملف و union المسارات ليست نسب اكتمال، ولا تنسب تنفيذ غير مقروء. | H7B4-05 | P7B4T-47 |
| INV7B4-22 | إذن تنفيذ مستقل عن أدوات الوثائق؛ 7C لم تبدأ و 8 غير مأذونة؛ نجاح فحص hash/روابط/نماذج/أجنحة المدقق لا يجيز ERP/SQL/COM/Office/مزود أو معالجة. | H7B4-06 | P7B4T-48 |

## 4. ثمانية عقود مصدر ومصالحة — ليست ثمانية اختبارات

[CSV العقود](evidence/report-reconciliation-07B4.csv) يربط كل عقد بالميزات والخطط وحدود الدليل. لم يقيّم SQL أو محرك التقارير؛ القيم الواردة fixtures مستقلة أو أوصاف محلية:

### RC7B4-01 — تكلفة تحليل الفواتير ومصالحة التجميع

**صلة المصفوفة:** FE7B4-01;FE7B4-02;FE7B4-22;FE7B4-23;FE7B4-31. **الأصول/الإحالات:** P7-077;P7-078;P4-007;P7-041;P7-085.

**المصدر والهوية:** يربط Inv و Inv_Sub عبر InvGlobalID؛ تعيد الحاسبة التكلفة من حركات ItemId حتى تاريخ حركة البيع. تقرأ الأرباح التفصيلية AvrgCost المحفوظة، فلا تفترض تطابق المنهجين أو صحة أحدهما مرجعاً للآخر.

**الوحدة والمقياس:** val كمية أساس، و val1 كمية وحدة البيع، و exchange_price سعر تلك الوحدة. تستعمل الحاسبة val×exchange_price وتقرب المقام إلى int؛ ثم يطبق تجميع Item آخر تكلفة على كامل الكمية.

**الفرع والفترة والمرشحات:** مصادر الحاسبة لا تحمل BranchScope أو لقطة مستودع موحدة؛ CalcUnitCost بلا inv_type=1 وفرع مرتجعه proc3. يقيد CalcUnitCostStock نوع الشراء 1 لكنه يبقي proc3. سقف date فقط ليس اعتماداً لسياسة as-of.

**صلة المستند و GL وحد الجهل:** لا مصالحة GL أو مخزون تاريخية منفذة؛ تبقى سياسة P4-007 محتملة كما كانت. لا تجعل تقريراً آخر مرجع حقيقة لنفسه أو تكتب قيد فرق لتوحيد النتائج.

**المجموع والمثال والشاهد المقابل:** قد تحول كمية 0.4 وقيمة 4 القرار إلى احتياطي 99؛ و 1×10+3×20 مرجعه 70 مقابل 80 أو 40 بحسب آخر تكلفة. عبوة 10 سعر 50 يجب أن تبقى قيمتها 50 لا 500. ثبات التكلفة ووحدة 1 قد يخفيان بعض العيوب.

**مسار الإخراج:** ينقل InvAnalysisRow و InventoryData القيم المنسقة للعرض والطباعة؛ تفصل الأرباح التفصيلية DgvAvgCost و DgvTotAvg محلياً. توافق القالب والمكتبة ودقة العملة غير محسوم.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:493-610`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:826-880`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:285-343`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1597`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1404`.

**خطط غير منفذة:** P7B4T-01;P7B4T-02;P7B4T-03;P7B4T-04;P7B4T-35;P7B4T-36;P7B4T-44. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-02 — فترة ومعايير وتحكم تحليل الفواتير

**صلة المصفوفة:** FE7B4-03;FE7B4-04;FE7B4-05;FE7B4-13;FE7B4-21;FE7B4-28. **الأصول/الإحالات:** P7-079;P7-080;P7-081;P7-089;P3-023;P7-054.

**المصدر والهوية:** ثمانية مسارات ShowResult* لكل بعد؛ تشترك في controls عامة لكن بناء WHERE مكرر يدوياً. يقرأ ShowResult الأول controls من new Thread خارج Dispatcher وقبل try.

**الوحدة والمقياس:** يجب أن تميز المعايير typed بين هوية المستخدم والمجموعة والخزينة والمستودع وحدود الزمن. Column1 تسمية بعد وليست مفتاح المصدر.

**الفرع والفترة والمرشحات:** يوسع Month كل bucket إلى بداية الشهر وآخره بلا تقاطع مع الطلب. اليوم المنتهي <=غد 00:00 قد يكرر الحد. يهمل المستخدم في سبعة أبعاد والمجموعة في بعدها، ويستعمل Stock قيمة المستودع للخزينة. منتقيا التاريخ في خلية واحدة.

**صلة المستند و GL وحد الجهل:** قبول المبلغ محجوب أولاً بحارس الخيط ومدخل Home المعطل أولياً، فضلاً عن حواجز البناء/النشر. هذا قارئ تقرير لا ترحيل محاسبي، وليس إثبات تجاوز ACL.

**المجموع والمثال والشاهد المقابل:** طلب 10–20 يناير مع حركات 5/15/25 بقيم 100/200/300 يجعل معيار الشهر يعطي 600 بدل 200. خزينة 7 ومستودع 3 يفصلان operand الخطأ؛ معرفان متساويان شاهد خادع.

**مسار الإخراج:** يقرأ BindToData المعايير الحالية مع صفوف سابقة التحميل؛ لا يثبت XAML رسماً أو hit-testing فعلياً أو تغطية الواجهة كلها.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:258-320`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:637-679`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1154-1198`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1285-1373`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1583-1600`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:299-354`؛ `SmartAuditERP/Home.xaml:378-384`.

**خطط غير منفذة:** P7B4T-05;P7B4T-06;P7B4T-07;P7B4T-08;P7B4T-09;P7B4T-10;P7B4T-25;P7B4T-26;P7B4T-34;P7B4T-41. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-03 — مبلغ وخصم وجزئية فئة في التحليل

**صلة المصفوفة:** FE7B4-06;FE7B4-07. **الأصول/الإحالات:** P7-082;P7-083.

**المصدر والهوية:** يجمع Customer/Salesman/Emp/Month/Day/Stock رأساً واحداً عبر MIN لكل GlobalID، مقابل تجميع ItemId/date في تفاصيل التكلفة. يستعمل Group/Item قيمة السطر قبل الخصم.

**الوحدة والمقياس:** grain الرأس لا يصبح grain بند الفئة بسبب join؛ حصة الخصم ومعنى net/gross يجب أن يعلنا صراحة وبأساس موحد مع التكلفة.

**الفرع والفترة والمرشحات:** يرشح ItemsCategory البنود المؤهلة لوجود الرأس لكنه لا يخصص قيمة الرأس. الفترة والفرع نفسيهما لا يصلحان خلط مستوى التجميع.

**صلة المستند و GL وحد الجهل:** قارئ الربح لا يؤكد صحة InvTotal أو tot_net المحفوظين أو مطابقتهما GL. استعمل مرجعاً مستقلاً غير متأثر بحواجز P4-003.

**المجموع والمثال والشاهد المقابل:** A100/تكلفة 60 و B300/تكلفة 180 مع فلتر A يتركان رأس 400 وكلفة 60 وربح 340؛ MIN يمنع ضرب الرأس لا خلط معناه. خصم 10 على 100/تكلفة 60 يصبح خصماً0 وربح 40 في Group/Item بدلاً من 10 وربح 30.

**مسار الإخراج:** تنقل Column5/10/2/3 تلك المقاييس إلى الشبكة والبطاقات والملف؛ التنسيق N2 ليس تصحيحاً للقيمة أو دليلاً على صافي معتمد.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:691-755`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:817-880`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:923-995`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1323-1392`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1462-1530`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1596-1690`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:652-687`.

**خطط غير منفذة:** P7B4T-11;P7B4T-12;P7B4T-13;P7B4T-14;P7B4T-44. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-04 — أهلية النوع وإشارة صافي التحليل

**صلة المصفوفة:** FE7B4-08. **الأصول/الإحالات:** P7-084.

**المصدر والهوية:** Inv.inv_type ونوع إجراء الرأس proc_type واتجاه Inv_Sub.proc_type هويات مختلفة؛ كتالوج InvTypes والكاتب يقدمان العقد المحلي المقارن، لا نسخة نشر مثبتة.

**الوحدة والمقياس:** صافي البيع يطرح المرتجع وفق سياسة؛ ليس مجموع حركة مخزنية incoming/outgoing أو كل رأس proc1 دون كتالوج نوع.

**الفرع والفترة والمرشحات:** غير المخزن يشترط رأس 1/سطر 2 فقط؛ المخزن يقرأ بيع 2/رأس 1/سطر 2 مع POS3/رأس 1/سطر 3 تحت اسم مرتجعات ويضيفه. مصدر التكلفة أوسع لأنه لا يقيد نوع البيع 2.

**صلة المستند و GL وحد الجهل:** لا صحة posting أو امتثال ضريبي من مطابقة النوع وحدها؛ P4-001 حاجز مرتجع مرتبط مستقل. لا تشغل كاتب الإنتاج لاختبار قارئ تقرير.

**المجموع والمثال والشاهد المقابل:** بيع 100+POS200−مرتجع 20 مرجعه الصافي 280. يعطي predicate المخزن 100 وغير المخزن 300 في المثال المختار، وقد تختلف الكمية والتكلفة عن أهلية المبلغ. بيع فقط قد يخفي الخلل.

**مسار الإخراج:** التوجيه والعناوين والمخرجات تحتاج mapping typed موثقاً؛ لا تعوض التعليقات أو الأرقام الثابتة مصفوفة الأهلية والإشارة.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:683-717`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:807-837`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1599-1683`؛ `SmartAuditERP/Properties/Resources.resx:3028-3064`؛ `SmartAuditERP/Class/InvoiceOper.cs:1528-1531`؛ `SmartAuditERP/Class/InvoiceOper.cs:1585-1585`؛ `SmartAuditERP/Class/InvoiceOper.cs:1613-1621`.

**خطط غير منفذة:** P7B4T-15;P7B4T-16;P7B4T-44;P7B4T-45. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-05 — أرباح المواد التفصيلية

**صلة المصفوفة:** FE7B4-09;FE7B4-15;FE7B4-18;FE7B4-24;FE7B4-30;FE7B4-31. **الأصول/الإحالات:** P7-085;P1-011;P2-001;P7-045;P7-061;P4-007;P7-041.

**المصدر والهوية:** يربط Inv و Inv_Sub بالـ GlobalID ويرشح النوع 2/3 والرأس 1/2 و ProductId0؛ يحفظ DTO الـ GlobalID و DgvIsPlus لا InvoiceType رقمياً. تأتي SelectedId من البحث أو Enter.

**الوحدة والمقياس:** DgvQty=val1 وسعره exchange_price؛ التكلفة الإجمالية val×AvrgCost. يفصل تكلفة الوحدة عن الإجمالي، ويحسب حصة خصم بكمية السطر وشمول VAT. يخصم مرة في المسار الموحد لا فرع POS ثانياً.

**الفرع والفترة والمرشحات:** يرشح BranchNo الفرع إذا!=-1؛ معايير المستودع والفترة والصنف اختيارية. تحرير النص دون حل لا يبطل الهوية. نهاية 23:59 الصريحة تقطع ثواني الدقيقة الأخيرة.

**صلة المستند و GL وحد الجهل:** AvrgCost محفوظة لكنها لا تثبت سياسة تكلفة تاريخية؛ تبقى P4-006/007. الملخص sales−returns صحيح الإشارة محلياً ولا يثبت GL.

**المجموع والمثال والشاهد المقابل:** تبقى هوية A11 في WHERE بعد تعديل caption إلى B. على مصدر متسق يعطي 100−10−60 ربح 30؛ لا يعمم خصم POS المكرر P7-038 أو خلط تكلفة الوحدة والإجمالي P7-039 هنا.

**مسار الإخراج:** CSV خام مع N2 وصيغ محتملة. يقرأ BuildReportDataSet نص controls الحالي مع قائمة سابقة. التوجيه بأسماء عربية لكن GlobalID محفوظ، فيقاوم جزء فقد الهوية المحلية من الجذر P7-061.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:177-353`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:371-397`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:422-477`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:575-628`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:697-733`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:821-856`؛ `SmartAuditERP/Class_WPF/ItemProfitRow_ProfitDetails.cs:1-25`.

**خطط غير منفذة:** P7B4T-17;P7B4T-18;P7B4T-28;P7B4T-31;P7B4T-37;P7B4T-43;P7B4T-44. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-06 — إشعارات الفواتير

**صلة المصفوفة:** FE7B4-10;FE7B4-19;FE7B4-25;FE7B4-26;FE7B4-27;FE7B4-29;FE7B4-33. **الأصول/الإحالات:** P7-086;P2-010;P7-046;P7-048;P7-049;P7-055;P4-007.

**المصدر والهوية:** Inv21/22 ومعايير عميل/مستخدم/مندوب وتاريخ؛ joins عبر Users.emp و Branches.BranchId. cardinality و schema النشر غير مثبتتين؛ لا تفترض exactly-one من LEFT JOIN.

**الوحدة والمقياس:** tax و ExtraVAT منفصلان في الكاتب؛ يعامل القارئ tax كمجموع فينقص VAT و TotalTax. SumPrice من مجموع val1×price والخصم من الرأس والبنود؛ حقول InvoiceObj الحالية ليست أرشيفاً تاريخياً.

**الفرع والفترة والمرشحات:** لا فرع محلي في المصدر؛ عند كل الفترة لا يدخل BETWEEN، ومع ذلك تقرأ النصوص الزمنية قبل الشرط. UserId/EmployeeId وسياسة القطع يحتاجان عقداً.

**صلة المستند و GL وحد الجهل:** هل جمع النوعين موجباً حركة إجمالية أم أثر صافٍ؟ لم يحسم المتطلب. seed InvTypes22 يعكس أسماء GetInvoiceType والتقرير؛ لا تقلب فلتر مدين/دائن من seed وحده.

**المجموع والمثال والشاهد المقابل:** VAT20+Extra5 يجب أن تجمع 25 وفق عقد الكاتب المنفصل؛ يعطي القارئ 15+5/TotalTax20. تعطي 5/5 مجموع مكونين 10 لكن TotalTax5. extra0 قد يخفي الخلل؛ صف غير قابل للتحويل قد يسقط في catch{}.

**مسار الإخراج:** Grid والملخص و CSV من الإسقاط نفسه. تمرر الطباعة null لا_invoicesList إلى جسر له overloads؛ حسم البناء والعقد يسبق قبول القالب. drill بالـ GlobalID لا يعفي إعادة التفويض.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:224-318`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:340-513`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:522-555`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:572-663`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:685-809`؛ `SmartAuditERP/Class/InvoiceOper.cs:1545-1561`؛ `SmartAuditERP/Class/InvoiceOper.cs:160-192`؛ `SmartAuditERP/Properties/Resources.resx:3072-3078`.

**خطط غير منفذة:** P7B4T-19;P7B4T-20;P7B4T-32;P7B4T-38;P7B4T-39;P7B4T-40;P7B4T-42;P7B4T-45;P7B4T-46. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-07 — تفاصيل المشتريات

**صلة المصفوفة:** FE7B4-11;FE7B4-12;FE7B4-17;FE7B4-20;FE7B4-24;FE7B4-25;FE7B4-32. **الأصول/الإحالات:** P7-087;P7-088;P1-033;P2-011;P7-045;P7-046;P7-054.

**المصدر والهوية:** Inv.* مع جداول أسماء و subqueries لـ SumPrice/ItemDiscount، وصفوف GlobalID. Store من Safes لكن JOIN المحسن Stocks.id=inv.safe؛ overrideSql يقرأ الاسم من Safes.

**الوحدة والمقياس:** المبالغ المحفوظة تقرأ كـ double وتلخص purchase−return. حقل نسبة ExtraVAT والأصفار المالية في BuildDataTable مسجلان سابقاً P7-047، لا نتيجة مكررة.

**الفرع والفترة والمرشحات:** يلتقط QueryParams على UI قبل العامل، واتصال bgConn محلي using وحماية زر العرض single-flight. كل الفروع بعد فرع مختار لا يمسح الفلتر؛ الكل المصرح ليس إذناً خارجياً عاماً.

**صلة المستند و GL وحد الجهل:** طرح proc2 من proc1 شاهد مقابل لجمع المرتجع موجباً هنا، لا إثبات صحة كاتب GL. المصدر المستقل يلزم أن يوافق الحالة ونطاق الفرع.

**المجموع والمثال والشاهد المقابل:** Safes3 مستودع A و Stocks3 خزينة B تعرضان B؛ LEFT JOIN لا يسقط الفاتورة. A100/B200 ثم الكل قد يبقي 100. يمكن أن يستبعد catch صفاً دون إحصاء الرفض.

**مسار الإخراج:** يمرر مصدر الطباعة DataTable حقيقياً لا null، لكن حقول نسبة/صفر ومعايير حالية وحفظ مظهر بلا استعادة تبقى عيوبها. حوار XLSX/CSV يكتب TSV: الجذر P7-050 المحفوظ.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:274-284`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:342-483`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:599-723`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:744-939`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:961-1002`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:1125-1129`؛ `SmartAuditERP/Class/LoadData.cs:12-25`؛ `SmartAuditERP/Class/Common.cs:133-153`.

**خطط غير منفذة:** P7B4T-21;P7B4T-22;P7B4T-23;P7B4T-24;P7B4T-30;P7B4T-33;P7B4T-37;P7B4T-38;P7B4T-44;P7B4T-46. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

### RC7B4-08 — حد الإخراج والموارد وبقية النطاق

**صلة المصفوفة:** FE7B4-14;FE7B4-16;FE7B4-25;FE7B4-26;FE7B4-27;FE7B4-28;FE7B4-29;FE7B4-34;FE7B4-35;FE7B4-36. **الأصول/الإحالات:** P1-004;P1-013;P7-046;P7-048;P7-049;P7-054;P7-055;H7B4-05;H7B4-06.

**المصدر والهوية:** أربعة أجسام محلية ومقاطع صريحة فقط؛ schema/DTO و UtilitiesProj و REPX وقوالب وأبناء خارجيون لا تغطى انتقالياً.

**الوحدة والمقياس:** قيمة مقربة أو نص CSV أو نجاح WriteAllText لا يثبت نوع الخلية أو المبلغ أو الإشارة أو اكتمال الصفوف.

**الفرع والفترة والمرشحات:** التقط معايير النتيجة والنطاق المصرح قبل الإخراج، وسجل حاجز الخيط والإتاحة قبل قبول القيمة. عمر موارد COM والاتصالات والمهام متابعة 7C لا قبول منفذ.

**صلة المستند و GL وحد الجهل:** لم يشغل SQL أو GL أو Office؛ لا benchmark أو فهرس مفقود أو تسرب مرصود. لم تكتب فواتير أو ترسل ضريبة/دفع/مزامنة.

**المجموع والمثال والشاهد المقابل:** وجود Close/Quit في مسار النجاح لا يغطي return الفشل؛ ووجود 17 مرشح شاشة غير regex لا يجعله مراجعة تنفيذ. لا ادعاء العثور على كل العيوب من hash أو self-tests.

**مسار الإخراج:** 7B5 معلنة لبقية البيع/POS/Android والمقاطع المالية والإخراج وأبناء مؤسسة النقد.7C لم تبدأ و 8 غير مأذونة؛ الخطط بوابات مستقبلية لا إذن تشغيل.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1920-2000`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:790-809`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:961-1002`؛ `SmartAuditERP/Home.xaml:378-384`.

**خطط غير منفذة:** P7B4T-27;P7B4T-29;P7B4T-38;P7B4T-39;P7B4T-40;P7B4T-41;P7B4T-42;P7B4T-46;P7B4T-47;P7B4T-48. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/قالب/Office أو اعتماد مالي أو نشر مثبت. سجل حواجز البناء والاعتماديات والمخطط والإتاحة والخيط قبل أي اختبار أثر لاحق، ولا تعتبر الحجب نجاحاً.

## 5. عقود وأسئلة غير محسومة

لا طلب أسرار أو قواعد إنتاج. المجهول لا يصبح gap عالمية أوعيباً مؤكداً من غياب ملف/إجابة. المتطلبات تعالج بعد المراجعة والسياسة والإذن المناسبين؛ لا تعطل متابعة B5 الساكنة:

| الإحالة — العنوان | العقد المطلوب | النتائج/الإحالة | الدليل |
|---|---|---|---|
| H7B4-01 — سياسة تكلفة ووحدة ودقة و as-of | مرجع مستقل يحدد طريقة التكلفة ونطاق الفرع/الموقع وحالات الشراء/مرتجعه والعبوات والكسور و fallback. لا نختار سياسة من CalcUnitCost ولا نصلح دفاتر قديمة آلياً. | P7-077;P7-078;P7-041;P4-007 | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:493-610`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1597` |
| H7B4-02 — معنى مقاييس وصافي وضريبة الإشعارات | عقد Gross/Net/Discount/Cost/Tax/AdditionalTax و grain رأس/سطر مع mapping InvTypes/ProcType بإصدار و schema منشور. التناقض المرفق لا يصادق على اتجاه ضريبي/محاسبي. | P7-082;P7-083;P7-084;P7-086 | `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:438-455`؛ `SmartAuditERP/Class/InvoiceOper.cs:1545-1561`؛ `SmartAuditERP/Class/InvoiceOper.cs:160-192`؛ `SmartAuditERP/Properties/Resources.resx:3028-3078` |
| H7B4-03 — بيئة وقوالب و DTO موثوقة وحواجز الإتاحة | Windows و WPF و DevExpress ومصادر DLL/REPX وبصماتها و overloads قبل قبول المصدر/الطابعة. سجل disabled Home وحارسالخيط و ambiguity null، ولا تعتبر الحجب نجاحاً. | P1-004;P7-054;P7-055;P7-089 | `SmartAuditERP/Home.xaml:378-384`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:258-320`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:790-809`؛ `SmartAuditERP/Class/Report.cs:380-406`؛ `SmartAuditERP/Class/Report.cs:531-553` |
| H7B4-04 — مصفوفة دور×فرع×مورد×أمر | حسم EmployeeId/UserId ونطاق كل/لااختيار وقراءة الكلفة والفتح والتصدير في حد موثوق؛ كل المواقع في القائمة لا يساوي منحاً. | P1-013;P2-001;P2-010;P2-011;P7-088 | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:213-216`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:422-477`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:183-218`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:239-242`؛ `SmartAuditERP/Class/LoadData.cs:12-25` |
| H7B4-05 — استكمال 7B5 ومقاطع التقارير المتبقية | الأجسام الخمسة للبيع/POS/Android/بيع الأصناف والطفلان الماليان وغير regex والباقي من callers/output تحتاج قراءة أو استبعاداً مسنداً؛ قد تعلن أجزاء أخرى. | H7B4-05 | حصر مؤجل فقط؛ لا دليل تنفيذ منتقى |
| H7B4-06 — 7C وموارد/إتاحة/أداء ثم بوابة 8 | 7C لم تبدأ: بقية HR/PM/بحري و UI/resources/events/async/RTL/cultures. schema وخطط وقياسات منقحة قبل حكم فهارس/تسرب/latency؛ 8 تحتاج إذناً وبيئة مستقلين. | H7B4-06 | حصر مؤجل فقط؛ لا دليل تنفيذ منتقى |

| السؤال | المطلوب دون أسرار | الإحالة |
|---|---|---|
| Q7B4-01 | ما مرجع التكلفة المعتمد ووحدة السعر/الكمية ونطاقه الزمني والمكاني وسياسة الكسور والمرتجع؟ | H7B4-01 |
| Q7B4-02 | هل tax في النشر VAT عادية أم شاملة، وما مرجع اختلاف تسميات 22 ومطلب gross/net لملخص النوعين وحصة الفئة؟ | H7B4-02 |
| Q7B4-03 | ما manifest البناء والقوالب وعقود المكتبة والإتاحة المقصودة للتحليل، ومن يقر حواجز التجربة قبل 8؟ | H7B4-03 |
| Q7B4-04 | ما تقاطع الدور/الفرع/المخزن/الخزينة وما صلاحية قراءة التكلفة والإخراج وفتح GlobalID، دون إرسال أسرار أو بيانات أشخاص؟ | H7B4-04 |
| Q7B4-05 | أي أجسام/قنوات معتمدة في النشر ينبغي استكمالها أولاً من قائمة B5، وما سبب الاستبعاد إن لم تكن مطلوبة؟ | H7B4-05 |
| Q7B4-06 | ما سياسات UI/الأداء والعقود الخارجية المطلوبة، ومتى تتوفر بيئة 8 المعزولة وإذنها؟ لا مفاتيح أو كلمات مرور في المحادثة. | H7B4-06 |

## 6. الباقي المعلن — لا إغلاق اسمي

[CSV10](evidence/continuation-backlog-07B4.csv) يحفظ ربط BK7B4 بـ BK7B3 وبـ BK7 الأصلي. **7B5 معلنة ولم تبدأ؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ**. الأعداد 827/98/52 و union334 محاسبة نطاق لا اكتمال قدرات:

| المعرف | الأصل | الجزء والحالة | العمل المطلوب |
|---|---|---|---|
| BK7B4-01 | BK7B3-01 ← BK7-01 | 7B5؛ partially-reviewed-not-complete | B4 قرأت أربعة أجسام فقط:InvAnalysis/ItemsProfitDetails/InvNotfic/PurchaseDetails. استكمل SalesDetails/POS/Android/ItemsSalesDetails/POS والأبناء frmActsInvTotal/frmNkdTotSalePurch وبقية المقاطع المالية وغير regex؛ أعلن مزيداً من 7B إن لزم. |
| BK7B4-02 | BK7B3-02 ← BK7-02 | 7B5/7C؛ partially-reviewed-not-complete | قارئ إشعار VAT ومصدر طباعة null ومخرجات الأرباح والمشتريات روجعت ساكناً؛ بقية callers/PDF/design/REPX/نشر/خطوط/DTO لم تغلق، وقالب مركزي لايغطي متصليه. |
| BK7B4-03 | BK7B3-03 ← BK7-03 | 7C؛ not-started | دورة WPF/events/timers/async/cancel/connections/dispose ما زالت 7C؛ COM التحليل يحوي early return قبل Quit كمؤشر متابعة لا تسرب مرصود؛ لا تشغيل Office. |
| BK7B4-04 | BK7B3-04 ← BK7-04 | 7C؛ not-started | منتقيا التاريخ المتراكبان P7-089 ملاحظة وظيفية محددة، لا بدء/اكتمال keyboard/Tab/Automation/RTL/scaling/cultures/messages/error عبر النظام. |
| BK7B4-05 | BK7B3-05 ← BK7-05 | 7C؛ not-started | بقية PM/دفعات/مقاولين/اعتماد/مستخلص/حالات/GL وصلاحيات أو استبعادات مسندة؛ لا ترقية أجسام التقارير إلى دورة أعمال كاملة. |
| BK7B4-06 | BK7B3-06 ← BK7-06 | 7C؛ not-started | بقية HR/بحري/حضور/حجز/تأمين/نهاية خدمة وفق السياسة ومصادر الحقيقة؛ B4 لا يراجع كتّابها. |
| BK7B4-07 | BK7B3-07 ← BK7-07 | 7B5/7C؛ partially-reviewed-not-complete | حفظ المظهر بلا استعادة امتداد P1-033؛ RadioButton فارغ لكن ShowResult ينفذ البعد ليس stub جديداً. بقية الأوامر والأطفال تحتاج تتبعاً بإتاحة/ضرورة/أثر. |
| BK7B4-08 | BK7B3-08 ← BK7-08 | 7B5/7C؛ partially-reviewed-not-complete | دفتر 827 و 98 مرشح ملف و 52 مرشح شاشة لا حصر ميزات مكتمل؛ النطاقات ومكملاتها محفوظة. استكمل أو استبعد بسبب أو أعلن أجزاء أخرى، لا إغلاق اسمي. |
| BK7B4-09 | BK7B3-09 ← BK7-09 | 7B5/7C؛ partially-reviewed-not-complete | الأداء مؤشرات مصدر فقط:عدة Fill لكل عضو/تاريخ في 8 أبعاد وحاسبة تكلفةداخلية، و InvTypes/lookups لكل صف أرباح. لا قياس latency/خطة/index مفقود أو تسرب مثبت. يلزم scope وحجم وبيئة وخطط. |
| BK7B4-10 | BK7B3-10 ← BK7-10 | 7B5/7C؛ partially-reviewed-not-complete | H3/H4/H5/H6/H7/H7B/H7B2/H7B3 باقية وتضاف H7B4/Q7B4. كل next_phase لأول 248 محفوظة، ولا معالجة أو إذن 8 من مدقق الوثائق. |

لا ترقية طفل بسبب launcher أو جسم مالي بسبب اسم ملف أوكل قالب بسبب Report المركزي. قد يلزم إعلان جزء 7B آخر؛ لا إذن 8 أو إصلاحات من نجاح المدقق. يرجع القارئ إلى [دفتر 827](evidence/coverage-ledger-07B4.csv) و[فرز 98](evidence/report-candidate-disposition-07B4.csv) و[شاشات 52](evidence/report-screen-disposition-07B4.csv) و[scope18](review-scope-07B4.csv) لمعرفة النص المختار ومكمله، لا نسبة اجتياز.
