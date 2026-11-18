# المرحلة 7 — الجزء 7B3: الرسوم واليومية والفئات والإنتاج والتأجير والسيريال

**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`، الفرع `arena/94ae8414-smartauditerp`.  
**مرجع التدقيق المعلن:** 2026-11-16 UTC؛ ملاحظة ساعة البيئة عند الدخول 2026-11-17 محفوظة منفصلة في provenance، لا تاريخ اختبار تطبيق أو إعادة تأريخ للتسليمات.  
**الحالة:** تدقيق ساكن جزئي ضمن إذن المرحلة 7 واستمرار المستخدم «طيب واصل العمل». لا إصلاحات أو تشغيل ERP أو إذن 8.

## 1. الخلاصة وحدود التسليم

استكمل هذا الجزء **تسعة أجسام تقارير محلية و launcher واحداً**، ومقاطع وظيفية محددة من XAML و SQL وكتّاب/مداخل ذات صلة. لم تكتمل 7B أو 7؛ **7B4 معلنة ولم تبدأ** لبقية الأجسام التجارية الكبيرة والمقاطع المالية والإخراج، ثم **7C لم تبدأ** لبقية الميزات والواجهات والموارد والأداء. **المرحلة 8 غير مأذونة ولم تبدأ**. `next_phase=8` متابعة مقترحة، لا تصريح تنفيذ.

- **11 نتيجة جديدة P7-066–076:** ست عالية وخمس متوسطة، كلها `confirmed` للسلوك أو التعارض المحلي بشروطه، لا حادث إنتاج مرصود. التراكمي **248 مفتوحة**: 2 حرجة، 163 عالية، 82 متوسطة، 1 منخفضة؛ 213 مؤكدة، 28 محتملة، 7 فجوات مستودع.
- **13 توسع evidence فقط** لأصول سابقة، لا 13 نتيجة أخرى. حُفظت نواة التصنيف والخطورة واليقين والنوع والعنوان والحالة **وكل next_phase لأول 237**. لا علاج أو إغلاق نتيجة.
- **27 مساراً**:7 متداخلة مع الاتحاد السابق 306 و 20 جديدة؛ الاتحاد 326 من 827، وبقي 501 بلا نطاق منتقى، فضلاً عن مقاطع غير منتقاة داخل 326. هذا اتحاد مسارات **لا نسبة اكتمال أسطر/ميزات أو تغطية تشغيلية**.
- **29 صف ميزة×شاشة×تنفيذ×خطة**، و 17 ثابتاً مطلوباً، و 10 عقود مصدر/مصالحة، و 39 خطة قبول/بوابة **غير منفذة**:22 خاصة بالجديد، 13 انحدار أصل، 2 عقد عابر، 2 بوابة نطاق/إذن.
- **20 توضيح Python مستقلاً و 16 ملاحظة نصية محدودة** واختبارات لمدقق الوثائق نفسه؛ لا استدعاء C# أو SQL أو WPF أو مكتبة أو قالب أو Office، ولا تصديق لصحة المال أو التفويض أو النشر.

لم يُنفذ build أو Windows/WPF/DevExpress/SQL/COM/SDK أو دفع/ضريبة/مزامنة/جهاز/طابعة/Excel أو مزود. لا بيانات إنتاج أو أسرار أو قوالب/ثنائيات مجهولة، ولا commit/push أو تعديل لملفات التطبيق الأصلية.

### أبرز المخاطر المحلية

1. **نطاق الرسوم:** إجراءا الدفع والطلب يتجاهلان نوع الفاتورة، وأربعة إجراءات لا تستبعد المحذوف. المقاييس مختلفة: الطلب cash+visa، والدفع CASE، والشهر InvTotal، والصنف/الفئة كميات×أسعار؛ لا مصالحة من تشابه عناوين البطاقات.
2. **حساب الفئات:** معدل 15 ثابت، وحصة خصم بلا كمية، وأول اختيار فعلي لا يطبق الفلتر. اختيار مستخدم لاحق يطلب عمود Safe_Emps خلاف عقد المصادر والكاتب المرفق؛ إصلاح index0 وحده لا يحل العقد.
3. **المخرجات والمعايير:** مصدر طباعة الفئات يرسل رأساً واحداً لا النتائج المحملة، وتاريخ التأجير غير مرتبط بمعيار SQL في المسار المحلي. بحث DataView لا يرمز الاقتباس؛ ليس حقن SQL.
4. **الإنتاج والسيريال:** طلب ComponentId لا يوافق DDL Inv_Sub والكاتب، مع حواجز إتاحة/حفظ أسبق. زرا بحث الصنف بالسيريال معطلان محلياً؛ اختلاف فرع الرصيد التجميعي امتداد P4-029 لا نتيجة جديدة.

## 2. نطاق القراءة الفعلي

[scope27](review-scope-07B3.csv) هو الحد. الجسم C# الكامل لا يعني كل XAML أو Style أو template أو caller أو DTO أوتعريف SQL منشور. مقاطع XAML تشمل المعايير والأعمدة والملخصات وأزرار الإخراج المحددة فقط:

| الجسم المحلي | C# المقروء | مقاطع XAML فقط | المراجعة وحدها |
|---|---|---|---|
| FrmRptSalesChart | `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:1-493` | 164-281;286-448;455-606 | جسم الرسوم المحلي كاملاً: تهيئة الفرع والفترة والنوع، كل loaders و ExecSP/metadata وخيارات المدة وفتح التفاصيل؛ XAML بطاقات وقيم ومعايير فقط. لا مخطط منشور أو تعريف رسم/قالب خارجي أو قبول UI. |
| frmRptDailySales | `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:1-378` | 168-241;270-405 | جسم المبيعات اليومية كاملاً: TVF ومعايير typed ونقل اليوم/الضريبة/المجاميع وحالة الفارغ و CSV و BindToData/الطباعة؛ XAML المعايير والأعمدة والبطاقات. لا مصالحة مالية منفذة أو كل مصدر Inv. |
| frmRptCategorySaleByDay | `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:1-394` | 172-262;294-445 | جسم المجموعة باليوم كاملاً: SP ونطاق المجموعة/الفرع/الفترة، الأعمدة والمجاميع و CSV والطباعة؛ XAML المعايير/الأعمدة. لا إثبات نسخة SP منشورة أو دلالة سعر/خصم معتمدة. |
| frmRptSalesByCategory | `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:1-529` | 182-332;335-678 | جسم الفئات كاملاً: مصادر الاختيارات، شروط index، SQL الكمية/القيمة/الخصم/ضريبة 15%، الشجرة والبطاقات، CSV ومصدر طباعة الرأس؛ XAML معايير وشجرة/مجاميع/أزرار دون إقرار بصحة كل style. |
| frmRptDailyProcess | `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:1-546` | 151-289;312-419 | جسم الحركة اليومية كاملاً: Task.Run و Dispatcher وقراءة controls، استعلامات الفواتير والسندات وتباين الفرع/المستخدم/الوقت و catch والمصدر الطباعي؛ XAML معايير/أعمدة فقط. لا تنفيذ عامل WPF أو قبول معنى نقدي/آجل. |
| frmRptProducedItems | `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:1-377` | 168-249;257-482 | جسم تقرير الإنتاج كاملاً: ربط الرأس/السطر والكمية/الوحدة/السعر والمكونات و ComponentId، الملخص/البيع الصفري وأوامر المعاينة/الطباعة؛ XAML منتج/مكونات/بطاقات. مدخل Home معطل افتراضياً، والحفظ P4-020 ليس مثبت النجاح. |
| frmRptRentInvoices | `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:1-717` | 223-346;350-563 | جسم تقرير التأجير كاملاً: تحميل/Cond، غياب wiring التاريخ، RowFilter/إعادة التحميل والمجاميع و CSV و REPX ومفاتيح الاختيار؛ XAML معايير/أعمدة/مخرجات. ليس جسم كاتب التأجير أو اعترافاً محاسبياً بالإيراد. |
| frmRptSerialNo | `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:1-492` | 205-316;345-517 | جسم السيريال التفصيلي كاملاً: TVF ومدخلات/ItemId، بحث الصنف المعطل، GlobalID وتوجيه typed/ACL و CSV والطباعة؛ XAML المعايير والأعمدة/أمر الفتح. DTO SerialNoRow خارجي لا يفترض مفقوداً. |
| frmRptSerialNoSummary | `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:1-325` | 204-299;327-433 | جسم السيريال التجميعي كاملاً: TVF والرصيد الموجب والفرع/ItemId و lookups و CSV/طباعة؛ XAML المعايير/الأعمدة. دلالة السيريال/وحدته/موقعه وعقد المخطط المنشور معلقة. |
| frmNkdFoundRpt | `SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml.cs:1-51` | 52-80 | جسم launcher مؤسسة النقد 51 سطراً وموضع الزرين فقط: فتح frmActsInvTotal و frmNkdTotSalePurch فعلي لا stub، لكن الأجسام التابعة لم تقرأ في 7B3 ولا تغطى انتقالياً. |


المسارات السبعة الداعمة هي مقاطع Resources.resx و Home.xaml و Home.xaml.cs و frmProductionOrder و InvoiceOper و ItemOper و StoredQueries؛ حدودها في scope. قارنت val الأساسية بكمية وحدة البيع val1 وسعرها، و InvSum من SumPrice، وعقد ItemId/ProductId. لم أفترض أن Branches.id=BranchId أو ItemsCategory.Id=CategoryId؛ كلا الاسمين موجودان محلياً ودلالة هويتهما المنشورة تحتاج عقداً.

- [دفتر 827](evidence/coverage-ledger-07B3.csv) يحفظ النطاقات ومكملها النصي. حتى اجتماع كل الأسطر في نطاقات تاريخية لا يثبت عمق قراءة أو اكتمال ميزة.
- [فرز 98 مرشح ملف](evidence/report-candidate-disposition-07B3.csv) لفظي، وليس 98 تقريراً/ميزة؛ FingerPrintDevice مطابقة لفظية للبصمة.
- [52 مرشح شاشة](evidence/report-screen-disposition-07B3.csv):35 اسماً يحوي rpt/report و 17 اسماً إضافياً محدداً من الحصر. توسع الفرز، ولا تثبت اكتمال حصر القدرات أو مراجعة تنفيذ غير المنتقى.
- قراءة frmNkdFoundRpt تثبت routing إلى frmActsInvTotal و frmNkdTotSalePurch، **لا قراءة الجسمين**. ربط طفل عبر launcher أو helper لا يرقّيه إلى نطاق مراجع.

## 3. النتائج الجديدة

كل نتيجة أدناه `implementation-defect / confirmed / open-not-remediated` ومتابعتها 8 غير المأذونة. «مؤكدة» للقرار أو التناقض المحلي، لا لخسارة أو تسريب أو استثناء مرصود. الأرقام fixtures مستقلة لا نواتج SQL. لا تختبر أثراً لاحقاً قبل توثيق/حل حواجز البناء و DTO والمخطط والإتاحة والخيط في بيئة مأذونة.


### P7-066 — إجراءا رسوم الدفع والطلب يتجاهلان نوع الفاتورة المرسل ويجمعان البيع و POS

**الخطورة:** عالية. **الشاشة/المسار:** `FrmRptSalesChart` — cmbInvType → LoadSalesByPayment/OrderType → ExecSP → SP المرفق.

**الدليل:** `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:124-194`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:261-307`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml:455-474`؛ `SmartAuditERP/Properties/Resources.resx:4030-4079`؛ `SmartAuditERP/Properties/Resources.resx:49049-49096`.

**المشاهدة المحلية:** كل loader يحول اختيار POS إلى 3 والبيع إلى 2، و ExecSP يرسل @inv_type عند وجوده. لكن جسمي GetSalesByPaymentMethods و GetSalesByOrderType المرفقين، في create و upgrade، يرشحان inv_type=2 OR inv_type=3 ولا يستعملان قيمة @inv_type في WHERE.

**السبب الجذري:** عقد SQL يقبل معاملاً للنوع لكنه لا يطبقه؛ التبديل الظاهر لا يغير نطاق هذين المصدرين.

**الشروط والحواجز:** بيانات بيع 2 و POS3 ضمن الفرع والفترة و OrderType نفسه، و pay_type=1 و visa=0 و tot_net=cash بقيم 100 و 200 على الترتيب، وتعريف منشور يوافق المرفق. اختبر كل مصدر مستقلاً مع حذف=false وضريبة وخصم 0 لعزل النوع؛ ليس كل مقياس رسم هو صافي الفاتورة.

**مثال الأثر المشروط:** طلب النوع 2 يبقي 300 بدلاً من 100، وطلب 3 يبقي 300 بدلاً من 200 في المصدرين؛ لا يعني هذا أن كل بطاقات الرسم تتجاهل النوع.

**حد الدليل والشاهد المقابل:** GetSalesByItems و GetSalesByCategory و MonthlySales تستعمل النوع في نصوصها، وهي شاهد مقابل. النص المرفق مثبت، لا أن كل قاعدة منشورة تطابقه؛ لا SQL أو رسم شغّل.

**معالجة مقترحة — لم تنفذ:** عقد metric/criteria بإصدار، و WHERE يعتمد @inv_type أو enum صريح للكل، مع اختبار معاملات لكل إجراء وبيان هل القياس بيع أم تحصيل. لا تبديل التسمية وحده.

**التحقق المخطط غير المنفذ:** P7B3T-01؛ P7B3T-02 في [خطة 39](VALIDATION-07B3.md). الحالة 1: النوع 2=100 والنوع 3=200 في كل مصدر معني، ولا تدخل الحركة الأخرى. الحالة 2: صافي 2=80 وصافي 3=160؛ الكل 240 فقط إذا كان خياراً مصرحاً ومعلناً. لا يعمم نجاح مصدر على الأربعة.


### P7-067 — استعلامات رسوم المبيعات المرفقة لا تستبعد الفواتير المحذوفة

**الخطورة:** عالية. **الشاشة/المسار:** `FrmRptSalesChart` — أربع loaders → GetSalesBy* → SQL resources.

**الدليل:** `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:124-214`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:261-325`؛ `SmartAuditERP/Properties/Resources.resx:3974-4079`؛ `SmartAuditERP/Properties/Resources.resx:48999-49096`؛ `SmartAuditERP/Properties/Resources.resx:4085-4103`.

**المشاهدة المحلية:** أجسام إجراءات الدفع والطلب والصنف والفئة لا تضيف Inv.IS_Deleted=0 في البيع أو المرتجع. الاستدعاء لا يمرر قائمة رؤوس صالحة بديلة؛ MonthlySales المجاور يضيف شرط الحذف في الجانبين.

**السبب الجذري:** أهلية رؤوس الحركات في إسقاط الرسوم مختلفة عن حالة الحذف المعتمدة في مصادر تقارير أخرى.

**الشروط والحواجز:** رأسان نشط ومحذوف في النوع والفرع والفترة نفسها، مع qty=val=val1=1، وضريبة وخصم 0 و pay_type=1 و visa=0 و cash=tot_net=InvTotal ومبلغ كل بند مطابق لسعره. طبق تعريف الإجراء المرفق وثبّت النوع وتجنب المكونات والوحدات المركبة لعزل الحذف.

**مثال الأثر المشروط:** بيع نشط 100 وبيع محذوف 50 ينتجان 150؛ مرتجع محذوف 20 قد ينقص الصافي أيضاً. قد يتغير ترتيب أعلى 5 ولو لم يظهر كل المحذوف كصف منفرد.

**حد الدليل والشاهد المقابل:** لا نزعم أن الحذف فعلياً بقي في قاعدة منشورة أو أن سياسة كل تقرير استبعاده مطلقاً؛ UI لا يعلن وضع تدقيق للمحذوف. MonthlySales و SalesByDay فيهما حارس حذف واضح فلا تنسب المشكلة لكل النظام.

**معالجة مقترحة — لم تنفذ:** عرّف eligible posted/nondeleted/holding states مركزياً لكل metric، طبّقها قبل التجميع والترتيب، وأظهر وضع تدقيق المحذوف إن كان مطلوباً كخيار مفوض منفصل.

**التحقق المخطط غير المنفذ:** P7B3T-03؛ P7B3T-04 في [خطة 39](VALIDATION-07B3.md). الحالة 1: كل مصدر معني يعيد 100 لا 150، وأعلى 5 يحسب بعد استبعاد المحذوف. الحالة 2: الصافي 90 في القياس المعتمد؛ لا يخصم المحذوف، ولا يدعي نجاح MonthlySales تصحيح بقية الإجراءات.


### P7-068 — أول اختيار فعلي للمجموعة والمستخدم والفرع لا يدخل مرشحات تقرير الفئات

**الخطورة:** متوسطة. **الشاشة/المسار:** `frmRptSalesByCategory` — LoadGroup/Branches/Users → ComboBox index0 → LoadDgv.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:95-142`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:149-195`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml:208-291`.

**المشاهدة المحلية:** تعبأ القوائم من DataView دون عنصر sentinel للكل. LoadDgv يضيف شرط المجموعة والمستخدم والفرع عند SelectedIndex>0 فقط رغم أن الكل CheckBox مستقل. لذلك أول صف فعلي index0 لا يرشح، بينما المندوب يفحص SelectedValue بلا هذا الشرط.

**السبب الجذري:** استعمال ترتيب العنصر كهوية لمعنى الكل بدلاً من وجود اختيار فعلي وهوية typed.

**الشروط والحواجز:** الكل غير مفعل، أول عنصر بيانات مختار، وبيانات لأكثر من مجموعة/مستخدم/فرع؛ لا نفترض أي ترتيب SQL ثابت أو أن أول عنصر له id1.

**مثال الأثر المشروط:** مجموعة أولى بمبلغ 30 وأخرى 70: اختيار الأولى يبقي 100 بدلاً من 30. أي ترتيب يعيد أول صف مختلف يغير المجموعة المتأثرة لا صحة الشرط.

**حد الدليل والشاهد المقابل:** لا نزعم أن تحميل القوائم يختار 0 تلقائياً؛ السيناريو اختيار المستخدم لأول صف. index1 يعمل في هذا الشرط. سياسة عزل الدور التاريخية P2-010 مستقلة عن off-by-one المحلي ولا تعد مرة ثانية.

**معالجة مقترحة — لم تنفذ:** الكل حقل نطاق صريح، و SelectedValue صالح يكفي لعنصر أول أو لاحق؛ رفض no-selection بدلاً من توسيع النطاق. اختبر تغيّر ترتيب القائمة وهوية الفرع/المستخدم المنشورة.

**التحقق المخطط غير المنفذ:** P7B3T-05؛ P7B3T-06 في [خطة 39](VALIDATION-07B3.md). الحالة 1: كل هوية مختارة تحد صفوفها ومجموعها، بما فيها index0، ولا يصبح عدم الاختيار إذناً للكل. الحالة 2: الهوية نفسها تعطي النطاق نفسه بصرف النظر عن index؛ المندوب والكل يبقيان وفق العقد.


### P7-069 — تقرير الفئات يحسب الضريبة والصافي بنسبة 15 بالمئة ثابتة بدلاً من بيانات البنود

**الخطورة:** عالية. **الشاشة/المسار:** `frmRptSalesByCategory` — LoadDgv SQL → itemvat/itemNet → الشجرة/الملخص/CSV.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:205-230`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:266-307`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:407-429`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml:374-398`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml:581-633`؛ `SmartAuditERP/Class/InvoiceOper.cs:1590-1601`؛ `SmartAuditERP/Properties/Resources.resx:1023-1055`.

**المشاهدة المحلية:** SQL يشتق itemvat من مجموع الأساس×0.15 و itemNet×1.15. لا يقرأ taxperc/taxval للبند أو مبلغ ضريبته التاريخي؛ الشجرة والبطاقات و CSV تستهلك النتيجة مباشرة.

**السبب الجذري:** إعادة احتساب الضريبة بمعدل ثابت على تجميع غير متجانس بدلاً من إسقاط مبالغ/فئات محفوظة بعقد واضح.

**الشروط والحواجز:** بند أساس 100 ضريبته 0، أو معدلات 0/5/15 مختلطة، مع خصم رأس 0 لتجنب P7-070، وبيانات محفوظة صحيحة مستقلة عن حواجز الكاتب.

**مثال الأثر المشروط:** المعفى 100 يصبح ضريبة 15 وصافي 115 بدلاً من 0 و 100؛ أساس 100 بمعدل 5 يصبح 15 بدلاً من 5.

**حد الدليل والشاهد المقابل:** إذا كانت كل البنود مؤهلة فعلاً لمعدل 15 وبقية المكونات متجانسة فقد تتطابق الأرقام. لم تحسم سياسة الضريبة/الإضافات/الاستقطاع أو الامتثال القانوني، ولا نفترض أن كل تغيير مطلوب إعادة احتسابه على التاريخ.

**معالجة مقترحة — لم تنفذ:** اعتمد قيمة ضريبة تاريخية مفصلة لكل بند/حصة خصم أو breakdown مالي موثق يميز النسب والفئات. اجمع مبالغ لا معدل افتراضي؛ طابق الرأس والدفتر بعقد وتقريب معتمدين.

**التحقق المخطط غير المنفذ:** P7B3T-07؛ P7B3T-08 في [خطة 39](VALIDATION-07B3.md). الحالة 1: ضريبة المعفى 0 وصافيه 100، وضريبة 5 تساوي 5 لا 15؛ لا يتغير الأصل المحفوظ. الحالة 2: مجموع الضريبة والصافي يطابق breakdown الموقع بعد إشارة المرتجع وتقريب العملة؛ الشجرة والبطاقات والملف متساوية.


### P7-070 — توزيع الخصم في تقريري الفئات يستعمل سعر الوحدة دون كمية السطر

**الخطورة:** عالية. **الشاشة/المسار:** `frmRptSalesByCategory / frmRptCategorySaleByDay` — SQL local و proGetCategorySaleByDay → حصة discount → totals.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:205-248`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:143-184`؛ `SmartAuditERP/Properties/Resources.resx:4393-4468`؛ `SmartAuditERP/Properties/Resources.resx:49644-49776`؛ `SmartAuditERP/Class/InvoiceOper.cs:1545-1571`؛ `SmartAuditERP/Class/InvoiceOper.cs:1590-1601`؛ `SmartAuditERP/Class/InvoiceOper.cs:1624-1624`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1407`؛ `SmartAuditERP/Class/ItemOper.cs:1494-1498`؛ `SmartAuditERP/Class/ItemOper.cs:1556-1564`.

**المشاهدة المحلية:** حصة الخصم المحلي SUM(ROUND(ItemPriceWithoutVAT*minus/NULLIF(InvSum,0),2)) وحصة SP من exchange_price*minus/InvSum. البسط سعر الوحدة بلا val1/مبلغ السطر، بينما مبلغ البيع val1*price؛ InvSum يكتب من SumPrice الذي يجمع ItemQuantity*ItemPrice. البيع والمرتجع يكرران القاعدة.

**السبب الجذري:** وحدات بسط التوزيع لا تمثل مساهمة السطر في مقام مجموع الفاتورة؛ لا يتحقق مجموع الحصص=خصم الرأس عند كمية غير 1.

**الشروط والحواجز:** فاتورة غير شاملة الضريبة وبخصم بنود 0: سطر واحد qty10×price10، InvSum100 و minus10. لا تعتمد دلالة alias DTO المفقود؛ هذه fixture مخزنة متسقة مع حقول الكاتب المعلنة.

**مثال الأثر المشروط:** الحصة المحسوبة 1 لا 10، فيصبح الأساس 99 بدلاً من 90 في التقريرين. تقسيم نفس الكمية إلى عشرة أسطر qty1 يبدل الحصص رغم ثبات البيع الاقتصادي.

**حد الدليل والشاهد المقابل:** qty1 في كل السطور وبقية الأسس المتجانسة شاهد مقابل قد يخفي العيب. المصدر المحلي يستعمل NULLIF أما SP لا؛ لا نساوي حراسي الصفر، ولا نزعم أثر SQL منشور دون حسم التعريف. P4-003 عن كتابة الضريبة/الرأس وليس هذا توزيع التقرير المستقل.

**معالجة مقترحة — لم تنفذ:** وزع الخصم على أساس مبلغ سطر متفق مع المقام وحالة السعر/الضريبة، مع حفظ residual rounding وإشارة المرتجع ومقام 0 صريح، أو اقرأ حصص الإصدار الموثوقة. لا تضف كمية الأساس لسعر وحدة بيع.

**التحقق المخطط غير المنفذ:** P7B3T-09؛ P7B3T-10 في [خطة 39](VALIDATION-07B3.md). الحالة 1: مجموع الحصص 10 والأساس 90، لا 1 و 99؛ لا يستعاض عن المعايير بكون الإجمالي قابلاً للتنسيق. الحالة 2: لا تتغير الحصة الاقتصادية بتقسيم السطر إلا حدود تقريب معلنة مسواة؛ المرتجع يعكس حصته، ومقام 0 يعيد نتيجة صريحة لا تعطل/صفر كاذب.


### P7-071 — مصدر طباعة تقرير الفئات ينقل رأساً واحداً ولا ينقل مجموعاته أو بنوده

**الخطورة:** عالية. **الشاشة/المسار:** `frmRptSalesByCategory` — PrintReport → BuildReportDataSet → ToDataTable(list).

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:255-307`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:446-524`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml:403-566`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml:657-671`.

**المشاهدة المحلية:** CategoryList يحتوي مجموعات وبنوداً وكميات/مبالغ، لكن BuildReportDataSet ينشئ InventoryData واحداً لبيانات الرأس فقط ثم list.Add(item) مرة واحدة. لا يعدّد CategoryList/ItemDetails أو يرسلها أو ملخصاتها إلى DataSet. PrintReport يمرر ذلك المصدر للقالب.

**السبب الجذري:** جسر طباعة رأس فقط منفصل عن نموذج الصفوف الفعلي؛ لا يحافظ على cardinality أو هوية/مبالغ التفاصيل.

**الشروط والحواجز:** قائمتان بمجموعتين وثلاثة بنود أو قائمة أخرى مختلفة، وقالب ومكتبة موثوقان بعد حل حواجز البناء والنشر. افحص مصدر البيانات قبل renderer.

**مثال الأثر المشروط:** ثلاثة بنود ومجاميع معلومة لا تصل عبر DataSource؛ عدد كائنات المصدر المحلي يبقى 1 رأساً حتى عند تغيير البنود.

**حد الدليل والشاهد المقابل:** لا ندعي صفحة فارغة مرصودة، أو حقول InventoryData خارجية غير موجودة، أو أن قالب REPX لا يقرأ مصدراً مستقلاً. الخلل المؤكد في هذا العقد هو عدم نقل النتائج المحملة؛ أي query مستقل بالقالب يحتاج ربطاً مفوضاً موثقاً لا تخميناً.

**معالجة مقترحة — لم تنفذ:** ReportSnapshot typed يضم header/groups/details/totals وهوية المعايير؛ dataset بعلاقات أو flatten موثق ومجاميع غير مضاعفة. طابق الصفوف والقيم قبل المعاينة، وافصل فشل القالب عن حفظ المستند.

**التحقق المخطط غير المنفذ:** P7B3T-11؛ P7B3T-12 في [خطة 39](VALIDATION-07B3.md). الحالة 1: كل بند/هوية/مجموعة ومبلغ مطلوب يصل بعقد معلن؛ لا يكتفى برأس واحد أو نجاح فتح المعاينة. الحالة 2: تتغير التفاصيل والمجاميع مع اللقطة الصحيحة فقط، ولا كتابة أعمال؛ قبول الرسم يتطلب القالب والمكتبة ثم اختباراً مستقلاً بإذن 8.


### P7-072 — قارئ مكونات تقرير الإنتاج يطلب ComponentId خلاف عقد Inv_Sub والكاتب المرفق

**الخطورة:** متوسطة. **الشاشة/المسار:** `frmRptProducedItems` — dgvItems_SelectionChanged → LoadComponents → SQL/row mapping.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:168-228`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:366-374`؛ `SmartAuditERP/Properties/Resources.resx:487-504`؛ `SmartAuditERP/Properties/Resources.resx:1023-1060`؛ `SmartAuditERP/Class/StoredQueries.cs:10-10`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1461-1499`؛ `SmartAuditERP/Home.xaml:378-391`.

**المشاهدة المحلية:** LoadComponents يختار GROUP BY ComponentId من inv و inv_sub ثم يقرأه. تعريف Inv_Sub المرفق و InsertInvSub يستعملان ItemId للمكون و ProductId لأبيه، والكاتب يضع row.ItemId/المنتج فيهما. ComponentId الموجود في ItemComponents ليس جدول FROM لهذا التقرير.

**السبب الجذري:** عقد قراءة للتقرير مأخوذ من كتالوج مكونات مختلف لا من مخطط سطور حركات الإنتاج.

**الشروط والحواجز:** الوصول لنافذة التقرير ثم تفعيل التفصيلي واختيار منتج له صفوف إنتاج صالحة، على مخطط مطابق للمرفق. مدخل Home معطل أولياً وحفظ الإنتاج له مانع P4-020؛ لا نفترض تجاوزهما.

**مثال الأثر المشروط:** المخطط المرفق لا يوفر عمود ComponentId في Inv_Sub، فيتعذر عقد الاستعلام بدلاً من إعادة مكونات المنتج المسجلة بـ ItemId.

**حد الدليل والشاهد المقابل:** هذه مقارنة مصدر/DDL/كاتب محلية، لا استثناء SQL مرصود أو نفي عمود توافق في نشر خارجي. لا نستنتج أن كل قاعدة تفتقده أو أن حفظ الإنتاج نجح؛ يجب توثيق النشر وتجاوز/تسجيل الحواجز لا اعتبارها نجاحاً.

**معالجة مقترحة — لم تنفذ:** قارئ إنتاج مطابق لترحيل بإصدار: ItemId مع alias واضح للمكون و ProductId/هوية أمر/سطر للأب، ومصالحة كمية ووحدة وتكلفة. أخفق typed عند تعذر العقد بدل تقرير ناقص.

**التحقق المخطط غير المنفذ:** P7B3T-13؛ P7B3T-14 في [خطة 39](VALIDATION-07B3.md). الحالة 1: يتوافق reader مع schema ويعيد المكونين الصحيحين؛ حاجز المدخل/الكاتب/المخطط يحجب الاختبار ولا يمرره. الحالة 2: يفصل المنتجين بمعرف الأب والأمر حسب العقد؛ فشل schema ظاهر مستقل عن عدم وجود مكونات؛ لا تغيير مخطط إنتاج حقيقي.


### P7-073 — تواريخ تقرير التأجير لا ترتبط بمعيار الاستعلام في مسار العرض المحلي

**الخطورة:** عالية. **الشاشة/المسار:** `frmRptRentInvoices` — Home → Window_Loaded/btnShow → LoadDgvItems(Cond).

**الدليل:** `SmartAuditERP/Home.xaml.cs:3725-3725`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:62-105`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:161-209`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:584-594`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:670-682`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml:274-294`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml:494-500`.

**المشاهدة المحلية:** Cond يبدأ فارغاً، و LoadDgvItems لا يبني معيار التاريخ من controls؛ يضم Cond فقط ويضيف المعلمات إذا لم يكن فارغاً. دالتا txtFromDate_ValueChanged/txtToDate_ValueChanged وحدهما تضيفان شرط التاريخ لكن لا ربط لهما في DateEdit XAML أو اشتراك برمجي في الجسم المقروء. زر العرض يستدعي التحميل دون توليد Cond. Home لا يضبطه.

**السبب الجذري:** اعتماد المعايير على أحداث قديمة غير موصولة بدلاً من بناء طلب التقرير عند العرض.

**الشروط والحواجز:** الفتح المباشر المحلي من Home وتعديل DateEdit ثم عرض؛ لا متصل خارجي يضع public Cond أو wiring إضافي غير متاح. صفان في فترتين مختلفتين بعد استبعاد بقية الفروق.

**مثال الأثر المشروط:** اختيار فترة ذات مبلغ 100 مع فترة أخرى 200 يبقي مجموعات 300 من ناحية تاريخ SQL، ثم يضع BuildReportDataSet تاريخ الشاشة على الصفوف. دخول/خروج الفلاتر النصية مستقل ولا يصلح تاريخ المصدر.

**حد الدليل والشاهد المقابل:** وجود دالتين مسماتين لا يربطهما تلقائياً في WPF. لا ننفي wiring من مكتبة/تهيئة خارجية غير مفحوصة؛ لا نجاح WPF/SQL مرصود. هذا غياب تطبيق تاريخ المصدر، لا مشكلة حد نهاية اليوم P3-023 ولا انجراف معايير بعد تحميل صحيح P7-045.

**معالجة مقترحة — لم تنفذ:** التقط DateRange typed عند كل عرض/تحديث، ولّد SQL معلماً مباشرة منه مع حارس حدود وترتيب، ثم احفظه في snapshot؛ أحداث UI لتحسين التجربة لا مصدر الحقيقة الوحيد.

**التحقق المخطط غير المنفذ:** P7B3T-15؛ P7B3T-16 في [خطة 39](VALIDATION-07B3.md). الحالة 1: يحمل المصدر حدّي A ويعيد 100 لا 300 قبل الطباعة؛ غياب event لا يلغي قيد تاريخ DTO. الحالة 2: لا يعود Cond فارغاً سراً بسبب الرقم، ولا تخرج نتائج خارج الفترة تحت عنوانها؛ no-selection/حدود غير صالحة تمنع الطلب بوضوح.


### P7-074 — مرشح DataView للتأجير يدرج النصوص دون ترميز علامات الاقتباس

**الخطورة:** متوسطة. **الشاشة/المسار:** `frmRptRentInvoices` — TextChanged/selection → GenerateFilter → DataView.RowFilter.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:285-335`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:616-668`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml:233-270`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml:300-314`.

**المشاهدة المحلية:** اسم العميل والجوال ونص المستخدم/الفئة تُدمج داخل تعبير LIKE حرفي محاط بعلامتي اقتباس مفردتين ثم تسند إلى RowFilter. لا ترميز للعلامة المفردة أو wildcard/literal contract. catch يعرض خطأ بعد الإدخال ويبقي المرشح السابق إن رفض parser التعبير.

**السبب الجذري:** خلط النص المدخل بلغة تعبير DataView بدلاً من تمثيل literal أو predicate typed.

**الشروط والحواجز:** اسم عميل مثل O'Neil باقتباس مفرد ASCII في البيانات أو البحث، أو فئة تحتوي هذا الاقتباس. هذا تعبير داخل الذاكرة وليس أمراً إلى SQL Server.

**مثال الأثر المشروط:** O'Neil ينتج مقطع cust LIKE '%O'Neil%' الذي لا يمثل literal الاسم الصحيح؛ قد يرفضه parser وتبقى نتائج الفلتر السابق. لا payload هجومي أو قارئ DataView شُغّل.

**حد الدليل والشاهد المقابل:** لا نصنف هذا حقن SQL أو استغلال صلاحيات مثبتاً؛ فئات wildcard تحتاج سياسة contains/literal منفصلة. نجاح البحث في اسم بلا اقتباس شاهد مقابل لا يحسم كل المحارف أو Unicode.

**معالجة مقترحة — لم تنفذ:** مرشح typed على الهوية/قيم النص، أو encoder خاص بلغة DataView يضاعف apostrophe ويعالج LIKE metacharacters حسب سياسة بحث معلنة؛ خطأ الفلتر يبطل حالة الإخراج ولا يترك عنواناً كاذباً.

**التحقق المخطط غير المنفذ:** P7B3T-17؛ P7B3T-18 في [خطة 39](VALIDATION-07B3.md). الحالة 1: لا خطأ parser، ويطابق literal الصحيح وحده وفق سياسة contains؛ تظهر حالة نتيجة مرتبطة بالنص الفعلي. الحالة 2: كل محرف له معنى معلن ومختبر، والفلتر الفاشل لا يتيح إخراج نتائج سابقة بوصفها جديدة؛ لا SQL أو أوامر ملفات من النص.


### P7-075 — زر بحث الصنف يبقى معطلاً في تقريري السيريال فلا يحدد ItemId من الواجهة

**الخطورة:** متوسطة. **الشاشة/المسار:** `frmRptSerialNo / frmRptSerialNoSummary` — ckAllItems → code/name editable; unnamed search Button remains disabled → SelectedId.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml:228-261`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml:227-259`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:21-32`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:93-95`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:146-174`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:291-304`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:324-328`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:20-30`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:82-83`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:119-148`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:157-169`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:184-188`؛ `SmartAuditERP/Home.xaml.cs:2963-2979`.

**المشاهدة المحلية:** زر البحث غير المسمى في كل XAML له IsEnabled=False محلياً. ckAllItems_CheckedChanged يمكّن مربعي الاسم/الرمز فقط ولا الزر؛ SelectedId لا يعيّن إلى معرف موجب إلا في addNewItem الذي يستدعيه الزر المعطل، ولا حدث بحث بالرمز/الاسم في هذين المربعين. يرسل ShowResults DBNull عند -1.

**السبب الجذري:** آلة حالة اختيار الصنف لا تشمل أمر البحث ولا تربط التحرير النصي بهوية الصنف.

**الشروط والحواجز:** المسار المحلي المعلن من Home بلا أداة خارجية تعيد تمكين الزر؛ ألغ الكل وحاول اختيار صنف بإدخال اسمه/كوده أو زر البحث.

**مثال الأثر المشروط:** الحقول تبدو قابلة للتحديد لكن ItemId يبقى غير محدد، فيمرر NULL إلى TVF؛ ليست هذه استجابة بحث عن صنف مختار صالح أو إثبات تسريب خادمي.

**حد الدليل والشاهد المقابل:** المعالج الحقيقي موجود وليس stub، لذلك لا تعاد نتيجته تحت P1-033. لا ننفي تغيير IsEnabled عبر كود خارجي غير متاح، ولا نفترض خطأ SerialNoRow/SerialSummaryRow الخارجيين أو أن SQL/الواجهة نفذا.

**معالجة مقترحة — لم تنفذ:** Command/CanExecute وربط موحد للحالة: تفعيل البحث عند تحديد صنف، أو بحث رمز يحل ItemId مع تحقق، ورفض all=false مع هوية غائبة. النص للعرض لا بديل للمفتاح.

**التحقق المخطط غير المنفذ:** P7B3T-19؛ P7B3T-20 في [خطة 39](VALIDATION-07B3.md). الحالة 1: أمر البحث متاح ويعين ItemId=A، والاستعلام لا يرسل NULL؛ كل الأصناف يزيل الهوية صراحة. الحالة 2: لا تفسر الكتابة بلا هوية على أنها اختيار صحيح أو الكل؛ الحالة والطلب والناتج متفقون، ويظل البحث محكوماً بالصلاحية.


### P7-076 — مرشح مستخدم تقرير الفئات يطلب عمود Safe_Emps غير الوارد في عقد مصدريه

**الخطورة:** متوسطة. **الشاشة/المسار:** `frmRptSalesByCategory` — cmbUser → condWhere Safe_Emps → FROM Items/inv_sub/inv.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:132-142`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:173-177`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:221-247`؛ `SmartAuditERP/Properties/Resources.resx:439-479`؛ `SmartAuditERP/Properties/Resources.resx:954-1060`؛ `SmartAuditERP/Properties/Resources.resx:1614-1623`؛ `SmartAuditERP/Class/InvoiceOper.cs:1538-1538`.

**المشاهدة المحلية:** بعد اختيار مستخدم ذي index>0 يضاف AND Safe_Emps=<SelectedValue> إلى SQL الذي يضم Items و inv_sub و inv فقط. DDL المرفق لا يعرف هذا العمود في مصدري الحركة؛ Safe_Emps اسم جدول ربط مستقل بين safe_id و emp_id لا يدخل FROM. الكاتب يضع المستخدم في Inv.sales_emp.

**السبب الجذري:** اسم جدول ربط استعمل كعمود مرشح لا يطابق عقد قارئ/كاتب المستخدم في الحركة.

**الشروط والحواجز:** الكل غير مفعل واختيار مستخدم في index1 أو لاحق على مخطط مطابق للمرفق، بعد تجاوز البناء. index0 يتجاوز الشرط بسبب P7-068 فيخفي حاجز العمود ولا يصلحه.

**مثال الأثر المشروط:** تفعيل المرشح الصحيح ظاهرياً لا يملك عقد عمود صالحاً في SQL المرفق؛ catch يعرض فشل تحميل بدلاً من نتيجة المستخدم المختار. لم ينفذ SQL أو يرصد استثناء فعلي.

**حد الدليل والشاهد المقابل:** تعارض المصدر و DDL المحلي مؤكد لا نفي عمود توافق في نشر خارجي. لا نجزم أن SelectedValue من Employees.id يساوي كل هويات Users.emp في جميع النشر؛ هذه سياسة/هوية H7B3-04. ليس عيب ترميز النص P1-011 أو التفاف index0 P7-068.

**معالجة مقترحة — لم تنفذ:** عرّف ReportUserScope بهوية موثقة ثم عمود المصدر المناسب بمعامل typed أو join صحيح عند الحاجة، لا اسم جدول كعمود. اختبر التوافق مع schema قبل تفعيل المرشح؛ لا تستبدل الاسم بالتخمين فقط.

**التحقق المخطط غير المنفذ:** P7B3T-21؛ P7B3T-22 في [خطة 39](VALIDATION-07B3.md). الحالة 1: الاستعلام مطابق لعقد نشر موثق ويعيد صفوف المختار ومجموعها فقط دون تعذر عمود؛ فشل البناء/schema حجب لا نجاح. الحالة 2: لا يحجب إصلاح index0 خلل العمود أو يربط بالمستخدم الخطأ؛ تتبع الهوية إلى كاتب Inv.sales_emp وفق العقد المعتمد.


## 4. منع التكرار وحفظ التاريخ

الجديد 66/67 عن عقدي SQL محددين؛ و 68 عن ترتيب العنصر لا مجرد غياب ACL؛ و 69 عن معدل ثابت لا خطأ كاتب P4-003 أو تطبيق معدل رأس P7-043. الجديد 70 حصة خصم في قارئين مستقلين، لا إعادة عد حفظ الضريبة. الجديد 71 ينشئ رأس InventoryData ثم لا يعدّد النتائج المحملة؛ بخلاف P7-055 الذي يمرر null إلى جسر خارجي وقد يسبقه حاجز build/overload. ليس الجديد افتراض DTO أوقالب مفقود، ولا إعادة عد اختزال تفاصيل سطر P7-033. الجديد 73 غياب تاريخ المصدر من الأصل، لا حد اليوم P3-023 أو dirty بعد تحميل صحيح P7-045. الجديد 74 لغة DataView في الذاكرة لا حقن SQL. الجديد 75 معالج موجود وزر معطل، لا stub. الجديد 76 عمود لا يوافق عقد المصدر، لا أثر حقن أو دلالة هوية مستخدم محسومة.

لم أعد عد CSV والصلاحيات وحدود الزمن لكل شاشة. ذيول [manifest13](evidence/historical-extensions-07B3.csv) والسجل أدناه تحفظ الأصل، **وكل الحقول التاريخية الأخرى والمتابعات كما كانت**:

| التوسع | الأصل لا نتيجة جديدة | المشاهدة والحد | الأدلة |
|---|---|---|---|
| EX7B3-01 | P1-004 | عقود ملفات REPX إضافية مسماة في المتصلين المحليين؛ لا نثبت وجودها أو مخططها أو استحالة مصدر بيانات مستقل داخلها. يمتد عقد حزمة/نسخة القوالب نفسه، لا نقص مستقل لكل اسم. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. ورّد قوالب موثوقة بإصدارات/bindings وبصمات إلى بيئة الاختبار فقط؛ لا تستعمل ملفاً مجهولاً أو اتصال قالب إنتاجي. | `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:277-339`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:270-325`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:446-482`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:403-449` |
| EX7B3-02 | P1-033 | معاينة/طباعة تقرير الإنتاج موصولتان لكن تعرضان غير معدة فقط؛ بطاقة إجمالي البيع تقرأ grandTotalSale الذي يبقى 0 في الجسم. مدخل Home معطل أولياً، فلا نفترض إتاحة عامة أو وجوب كل قدرة تجريبية. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. حسم اعتماد طباعة/بيع التقرير وإتاحته؛ نفذ عقداً حقيقياً أو عطّل/سم الميزة غير المدعومة دون طباعة أو مجموع صفري مضلل. | `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:27-30`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:303-312`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:332-346`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml:222-235`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml:459-468`؛ `SmartAuditERP/Home.xaml:378-391` |
| EX7B3-03 | P1-013 | مداخل Home للفئات والرسوم والمجموعة باليوم والتأجير والسيريال تفتح بلا ApplyPermission المستعمل في اليومية/الإنتاج؛ ليست دليلاً على نفي كل ضوابط خادم أو صلاحية شاشة. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. اختبر رفض دور بلا عرض/تكلفة/تصدير عند المدخل والأمر ومصدر البيانات، لا VisibleTree قبل Show فقط. | `SmartAuditERP/Home.xaml.cs:2963-2979`؛ `SmartAuditERP/Home.xaml.cs:3540-3540`؛ `SmartAuditERP/Home.xaml.cs:3613-3613`؛ `SmartAuditERP/Home.xaml.cs:3631-3632`؛ `SmartAuditERP/Home.xaml.cs:3725-3725` |
| EX7B3-04 | P2-001 | OpenWindow للتوجيه من السيريال يستدعي configure/Navigate قبل Show دون إعادة تفويض في helper؛ بحث الصنف نفسه يطبق ApplyPermission كشاهد مقابل. الهوية العالمية لا تعوض التفويض. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. نفذ أمر فتح المصدر على GlobalID غير مسموح لمستخدم مختبري؛ ارفض القراءة/الأمر قبل Navigate بصرف النظر عن الزر. | `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:148-162`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:177-209`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:333-345` |
| EX7B3-05 | P2-010 | الرسوم تبدأ loaders بفرع 0 الذي يصير DBNull رغم BranchPermissions. اليومية والمجموعة اليومية تقرآن كل الفروع و no-selection يصير NULL؛ التأجير لا يضيف branch، و BuildSafeCondition في اليومية التشغيلية لا يحمل branch/user. لا حارس خادم منفي، وحاجز العامل P7-054 أسبق في DailyProcess. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. قارن مستخدم فرع 1 ببيانات فرع 2 في التهيئة والعرض والتصدير؛ no-selection/الكل يتقاطعان دائماً مع النطاق المصرح. تحقق UI-thread أولاً حيث يمنع الوصول. | `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:38-53`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:64-95`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:279-283`؛ `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:69-85`؛ `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:141-145`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:62-78`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:143-151`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:169-190`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:382-412` |
| EX7B3-06 | P3-023 | DailySales ينتهي 23:59:59 لا نهاية حصرية؛ category/serial يستعملان غد 00:00 مع<= أو BETWEEN في SQL، فيدخل حد الغد. شهر الرسوم ينتهي آخر يوم 00:00؛ الإنتاج يضيف 24 إلى وقت DateEdit الحالي فيتجاوز منتصف اليوم التالي. سندات DailyProcess تتجاهل وقتي الشاشة، بخلاف فواتيره؛ لا تنفيذ قبل حسم P7-054. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. اختبر from/to مع ساعة ودقة ms، وحد الغد، وأواخر الشهر؛ مرجع[start,end) واحد للفواتير والسندات والإنتاج بلا قطع أو زيادة 24 على وقت خفي. | `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:126-137`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:157-169`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:97-108`؛ `SmartAuditERP/Properties/Resources.resx:4374-4382`؛ `SmartAuditERP/Properties/Resources.resx:4425-4426`؛ `SmartAuditERP/Properties/Resources.resx:4443-4444`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:375-411`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:86-93`؛ `SmartAuditERP/Form_WPF/frmRptProducedItems.xaml.cs:193-201`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:248-257`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:339-358`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:401-412` |
| EX7B3-07 | P4-029 | رصيد السيريال التجميعي في TVF المرفق يقيد الصادر بفرع@Branch فقط، ولا يقيد الوارد به؛ create و upgrade يكرران ذلك. الطلب UI يرسل الفرع، فيحسب كل الوارد ناقص صادر الفرع المختار. لا نعيد عده كـ P7 جديد أو نخلطه بإلغاء حوار الاختيار التاريخي. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. رصيد فرع A: وارد 1 وصادر 0، وفرع B وارد 9؛ المطلوب 1 لا 10. كرر التحويل والصادر والكل وفق عقد السيريال/الوحدة/الموقع؛ عزل المنشور غير مثبت. | `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:61-91`؛ `SmartAuditERP/Properties/Resources.resx:4277-4335`؛ `SmartAuditERP/Properties/Resources.resx:49583-49639` |
| EX7B3-08 | P7-041 | GetSalesByItems للرسوم يضرب val الأساسية في exchange_price للوحدة، مقابل val1 في GetSalesByCategory؛ الكاتب يميز val و val1. امتداد أصل عدم تجانس كمية×سعر، لا نتيجة جديدة باسم رسم مختلف. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. عبوة 10 وحدات بسعر 50 وكمية بيع 1: قيمة المال 50 لا 500، وكمية الأساس 10 منفصلة. قارن الصنف/الفئة بعد توحيد الخصم/الضريبة/النطاق. | `SmartAuditERP/Properties/Resources.resx:3988-3994`؛ `SmartAuditERP/Properties/Resources.resx:4015-4020`؛ `SmartAuditERP/Properties/Resources.resx:49022-49047`؛ `SmartAuditERP/Class/InvoiceOper.cs:1594-1597`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1407` |
| EX7B3-09 | P7-045 | طباعة اليومية/المجموعة/السيريال تقرأ تاريخ controls فوق collections سابقة. الاختصارات في الرسوم لا تحدث controls ولا MonthlySales، وفتح التفاصيل يفرض Sales لا نوع الرسم. التأجير يعيد DataView جديدة بلا إعادة GenerateFilter مع بقاء الخيارات؛ ليس ذلك غياب قيد التاريخ الأصلي الجديد P7-073. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. حمّل A ثم غيّر المعايير/الاختصار أو أعد التحميل؛ snapshot يظهر/يطبع نطاقه الفعلي أو يمنع dirty، وتبقى filters/نوع التفاصيل متوافقة مع المصدر. | `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:239-272`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:344-380`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:467-487`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:356-440`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:197-207`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:285-335`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:584-594` |
| EX7B3-10 | P7-046 | DailySales يمسح المجموعة/حقول المجموع ثم يرجع عند الفارغ قبل تحديث البطاقات المرئية. الفئات قد تبقي summary قديمة بعد exception؛ DailyProcess يبتلع فشل كل DoProcess/2 ثم يعلن progress100. هذه نتائج جزئية/حالة فشل لا عدم وجود اقتصادي، والعامل له حاجز P7-054. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. ابدأ بنتيجة 100 ثم فارغ/مصدر ثان فاشل؛ البطاقات/المجموعة تنشر معاً، Error≠Empty≠0 و progress100 ليس نجاح مصادر. | `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:112-118`؛ `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:153-159`؛ `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:193-200`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:149-156`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:304-316`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:219-245`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:326-335`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:375-379` |
| EX7B3-11 | P7-048 | CSV اليومية والمجموعة والفئات والسيريال يكتب فواصل/N2 ونصاً بلا encoding خلايا. التأجير يغلف الحقول فيعالج comma/newline غالباً لكنه لا يضاعف الاقتباس الداخلي. لا تنسب كل عيب لكل writer. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. round-trip comma/quote/newline وألوف وثقافتين بمعيار CSV معتمد؛ طابق count/types/totals؛ غلاف التأجير وحده لا يصلح quote داخلية. | `SmartAuditERP/Form_WPF/frmRptDailySales.xaml.cs:208-230`؛ `SmartAuditERP/Form_WPF/frmRptCategorySaleByDay.xaml.cs:238-262`؛ `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:396-430`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:494-520`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:358-389`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:199-228` |
| EX7B3-12 | P7-049 | نصوص عميل/فئة/صنف/سيريال غير موثوقة تعبر CSV إلى UseShellExecute أو مستهلك جدول محتمل بلا سياسة خلية نصية. الصيغة لا تزال potential؛ لم ينفذ Office أو formula interpreter ولم يثبت تفسير القارئ الفعلي. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. حسم القارئ/سياسة النص خارج الدردشة؛ راجع encoding typed واستخدم strings خاملة في fixture؛ لا تشغل صيغة أو رابطاً أو ملف عمل غير موثوق. | `SmartAuditERP/Form_WPF/frmRptSalesByCategory.xaml.cs:404-429`؛ `SmartAuditERP/Form_WPF/frmRptRentInvoices.xaml.cs:504-529`؛ `SmartAuditERP/Form_WPF/frmRptSerialNo.xaml.cs:369-391`؛ `SmartAuditERP/Form_WPF/frmRptSerialNoSummary.xaml.cs:210-230` |
| EX7B3-13 | P7-054 | DailyProcess يشغّل ShowResult في Task.Run ثم DoProcess/DoProcess2 و BuildCondition تقرأ IsChecked/SelectedValue/DateTime/Text خارج Dispatcher؛ حمايات المسح/Add/Progress جزئية، و catch{} يخفي الفشل. امتداد أصل thread-affinity نفسه لا عطل جديد لكل شاشة. توسعة هذا الأصل فقط لا إعادة عد أو تغيير خطورة/يقين/نوع/عنوان/حالة أو أي next_phase؛ لا معالجة. التقط المعايير على UI قبل العامل ولا تقرأ controls داخله؛ أي حاجز thread يجب تسجيله كحجب لا نجاح قبل قبول branch/user/time/المجاميع. | `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:196-245`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:248-257`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:338-358`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml.cs:382-412`؛ `SmartAuditERP/Form_WPF/frmRptDailyProcess.xaml:273-277` |


## 5. الشواهد المقابلة وما لم يتحول إلى عيوب

- SalesByDay يقرأ الضريبة والصافي المخزنين ويرشح النوع والفرع والحذف و pay_type<>5. MonthlySales يرشح النوع والحذف. لا تنسب P7-066/067/069 إلى كل النظام؛ ولا يحسم ذلك صحة الحقول عند الكاتب أو مطابقتها إلى GL.
- ثابتَا payType/seller في استدعاء MonthlySales لا يثبتان مرشحاً نشطاً خاطئاً؛ الجسم المرفق لا يستخدم المعاملين. النسخة المنشورة تحتاج دليلاً مستقلاً.
- لا افتراض أن index0 مختار تلقائياً؛ P7-068 عن اختيار المستخدم لأول صف بيانات فعلي. المندوب يفحص SelectedValue دون الحارس نفسه.
- نسخ CategorySaleByDay تختلف ومنها ProductId. المحلي يستعمل NULLIF بينما SP لا؛ لا نساوي مساري الصفر أو نستنتج فقد عمود من اختلاف alias.
- DailyProcess يستعمل DISTINCT GlobalID و MIN(tot_net) لكل رأس قبل SUM؛ لا تضاعف بسيط مؤكد من join. P7-054 قد يحجب الوصول أصلاً و catch{} تخفي الفشل؛ لا قبول لحدود الفرع والمستخدم والساعة خلف الحاجز.
- السيريال التفصيلي يستعمل GlobalID وتوجيهاً رقمياً، شاهد مقابل لتعميم P7-061، لكنه لا يعوض تفويض helper قبل Navigate. التجميعي يقيد الصادر بالفرع لا الوارد: امتداد P4-029.
- مدخل الإنتاج في Home معطل أولياً وحاجز الكاتب P4-020 قائم. ComponentId موجود في ItemComponents لكنه ليس ضمن FROM لقارئ التقرير. لا استثناء SQL مرصود أو نجاح حفظ إنتاج مفترض.
- معنى proc3/4 بالتأجير والإيراد والتحصيل غير محسوم. RowFilter ليس SQL injection. إعادة DataView وفقد الفلاتر سبب dirty منفصل عن غياب تاريخ SQL.
- launcher مؤسسة النقد ليس stub، ولا يغطي الطفلين. CalcStockInOut من 7B2 ما زال بلا متصل نشط مثبت في المسح المحلي، فلا نتيجة جديدة منه.
- InventoryData/SerialNoRow/SerialSummaryRow و REPX/ToDataTable عقود خارجية؛ لا تخمين حقول أو overloads أو صفحة فارغة شوهدت. P7-049 ما زالت potential ولم ينفذ Office أو قارئ صيغ.

## 6. الأدلة والتحقق والتسليم التالي

[لقطة 237](evidence/findings-through-07B2.csv) SHA256=`a666334204d3a79b6b0b1bb324669d5dc0b387c62dba03f80d2c0447248461cb`، و[فهارس 7B2 المجمدة](evidence/shared-indexes-through-07B2.json)، و[provenance7B3](evidence/provenance-07B3.json) تحمي 132 artifact تاريخية، منها 110 المحمية سابقاً. لا إعادة توليد تقرير أو checks أو helper محمي أو baseline. المدقق المشترك يتطور، لكن helper7B2 يقرأ 237 وفهارسه الأصلية **في الذاكرة عند مساراتها المنطقية**، لا 248 أو الفهارس الحالية. مقاييس إعادة الفحص ليست ادعاء تطابق bytes تاريخية.

نجح فحص اتساق الحزمة الوثائقية وسجل أخطائه فارغ في النتيجة الفعلية المرتبطة أدناه؛ ليس قبول ERP.

[checks الفعلي](evidence/checks-07B3.json)، [تفصيل التحقق](VALIDATION-07B3.md)، [التوضيحات 20+16](evidence/report-witnesses-07B3.json). لا تستخدم نجاحها لشهادة مالية/أمنية أو إغلاق نتيجة أو إذن 8.


- [نموذج المصادر](COMMERCIAL-MARINE-REPORTS-07B3.md): مصفوفة 29 وثوابت 17 وعقود 10 و H7B3/Q7B3 و backlog10.
- [خطة التحقق](VALIDATION-07B3.md):39 خطة غير منفذة، وفصل توضيحات Python وفحوص النص ومدقق الوثائق عن قبول ERP.
- [findings](findings.csv)، [scope](review-scope-07B3.csv)، [README](README.md)، [PLAN](PLAN.md)، [IMPROVEMENTS](IMPROVEMENTS.md): الحالة الحالية والتاريخ المحفوظ ومجموعات G-01–96؛ **ليست 96 نتيجة إضافية**.

**التوقف عند هذا التسليم الجزئي. التالي 7B4 ضمن تدقيق 7 القائم** لبقية الأجسام التجارية/المالية والإخراج أو استبعادات مسندة، ثم 7C. لا اكتمال 7B/7 أو إصلاح وتشغيل تلقائي؛ 8 تحتاج إذناً وبيئة موثوقين منفصلين. تبقى H3/H4/H5/H6/H7/H7B/H7B2 وتضاف H7B3، ولا يطلب سر أو بيانات إنتاج هنا.
