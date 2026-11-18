# المرحلة 7 — الجزء 7B4: تحليل الفواتير والأرباح التفصيلية والإشعارات والمشتريات

**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`، الفرع `arena/94ae8414-smartauditerp`.  
**مرجع التدقيق المعلن:** 2026-11-16 UTC. ملاحظة ساعة البيئة عند دخول هذا الجزء `2026-11-18T00:17:24+00:00` محفوظة منفصلة في provenance؛ ليست تاريخ تشغيل ERP أو إعادة تأريخ للتاريخ المحمي.  
**الحالة:** استمرار ساكن ضمن إذن المرحلة 7؛ لا معالجة للشيفرة أو تشغيل النظام أو إذن المرحلة 8.

## 1. الخلاصة وحدود التسليم

اقتصر هذا الجزء على **أربعة أجسام C# محلية كاملة**: `frmRptInvAnalysis` و`frmRptItemsProfitDetails` و`frmRptInvNotfic` و`frmRptInvPurchaseDetails`، ومقاطع وظيفية محددة من XAML والكاتب والحاسبة والموارد والمداخل. الجسم الكامل لا يعني كل caller أو قالب أو SDK أو عقد نشر أو قبول تشغيل.

**لم تكتمل 7B أو 7. أُعلنت 7B5 لبقية أجسام البيع/POS/Android وبيع الأصناف والمقاطع المالية والإخراج ومرشحي غير regex وأبناء مؤسسة النقد؛ لم تبدأ. 7C لم تبدأ. المرحلة 8 غير مأذونة ولم تبدأ.** استمرار «طيب واصل العمل» إذن متابعة تدقيق 7 لا إذن معالجة أو تشغيل، و`next_phase=8` خطة لا تصريح.

- **13 نتيجة جديدة P7-077–089**:7 عالية و 6 متوسطة؛ كلها `confirmed` للسلوك/التعارض المحلي بشروطه، وليست حوادث إنتاج مرصودة. التراكمي **261 مفتوحة**:2 حرجة، 170 عالية، 88 متوسطة، 1 منخفضة؛ 226 مؤكدة، 28 محتملة، 7 فجوات مستودع.
- **17 ذيلاً للأدلة فقط** لأصول سابقة، مع حفظ الخطورة واليقين والنوع والعنوان والحالة **وكل next_phase لأول 248**، ومنها 43 تحمل متابعة 7 تاريخياً. لا تغيير P4-007 أو P7-049 من potential إلى confirmed، ولا إغلاق نتيجة.
- **18 مساراً**:10 متداخلة مع الاتحاد السابق 326، و 8 جديدة؛ الاتحاد 334 من 827 وبقي 493 بلا نطاق منتقى، فضلاً عن المقاطع غير المختارة داخل 334. هذا اتحاد مسارات **لا نسبة اكتمال أو قراءة كل أسطر الملفات أو تغطية ميزات/تنفيذ**.
- **36 صف ميزة×شاشة×تنفيذ×خطة، و 22 ثابتاً مطلوباً، و 8 عقود مصدر/مصالحة، و 48 خطة غير منفذة**:26 خاصة بالجديد، 17 انحدار أصل، 3 عقود عابرة، 2 بوابة نطاق/إذن. الصفوف المؤجلة ليست ميزات راجعت تنفيذها.
- **23 توضيح Python يدوياً مستقلاً و 18 ملاحظة نصية محدودة**، و 20 حالة جديدة لمدقق الوثائق الاصطناعي. هذه ليست اختبارات C#/SQL/WPF أو مطابقة مالية/أمنية.

لم ينفذ build أو SQL أو WPF/DevExpress/SDK أو COM/Office أو مزود دفع/ضريبة/مزامنة أو جهاز/طابعة. لا بيانات إنتاج أو أسرار أو ثنائيات/قوالب مجهولة، ولا تعديل لملفات التطبيق الأصلية أو commit/push. لا شهادة صحة مالية أو امتثال أو «كل العيوب عُثر عليها».

### أهم ما يستحق المعالجة لاحقاً

1. **التكلفة والربح في التحليل:** تقريب كمية المقام إلى int؛ استعمال آخر تكلفة لكل كمية الفترة؛ خلط مبلغ رأس كامل بتكلفة فئة محددة؛ وإهمال الخصم في تجميعي الصنف والمجموعة. الوحدة ومصدر متوسط التكلفة امتدادان لأصول سابقة، لا نتائج مكررة.
2. **الفترة والأهلية والمعايير:** التوسيع الشهري خارج الطلب؛ اختلاف نوع/إجراء/اتجاه البيع والمرتجع و POS؛ معيار مستخدم مهمل ومعيار خزينة من قيمة مستودع. منتقيا التاريخ في خلية XAML واحدة، بلا ادعاء render مرصود.
3. **الإشعارات والمشتريات:** قارئ الإشعارات يفترض أن tax تشمل ExtraVAT خلاف الكاتب المحلي؛ JOIN المشتريات يقرأ اسم خزينة مكان المستودع؛ وخيار كل الفروع يبقي الفرع السابق.
4. **حدود أسبق من الحساب:** عامل تحليل الفواتير يقرأ WPF قبل Dispatcher و try؛ ومدخله في Home معطل أولياً. طباعة الإشعارات تمرر null مع حاجز حسم overload/build. لا تُسمَّ نتيجة downstream ناجحة أو مرصودة خلف هذه الحواجز.

## 2. نطاق القراءة الفعلي

[scope18](review-scope-07B4.csv) هو الحد. تمت قراءة الأجسام الأربعة، لا كل XAML أو Style أو Resources/AlterDb أو كاتب أو Caller:

| الجسم | C# المقروء | XAML المختار فقط | حد المراجعة |
|---|---|---|---|
| frmRptInvAnalysis | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1-2147` | 1-13;245-562;597-812 | ثمانية أبعاد، مصدرا تكلفة، معايير وأهلية ومجاميع وبطاقات ومخرجات ونموذج صف؛ حواجز الإتاحة والخيط مستقلة. |
| frmRptItemsProfitDetails | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:1-862` | 1-13;246-375;408-643;653-763 | هوية/بحث، بنود ووحدات وتكلفة وضريبة وخصم وإشارة، ملخص وفتح مصدر وطباعة و CSV؛ لا اعتماد لسياسة التكلفة. |
| frmRptInvNotfic | `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:1-813` | 1-15;190-519;543-695 | أنواع ومعايير و joins وإسقاط الضريبة والملخص والتنقل و CSV وجسر الطباعة؛ لا عقد نشر أو قالب موثوق مثبت. |
| frmRptInvPurchaseDetails | `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:1-1171` | 1-14;177-447;485-837;858-916 | التقاط UI والعامل، JOIN والأسماء وحالة الصفوف والمجاميع، المظهر والفتح ومصدر الطباعة والملف؛ يكمل مقاطع B1 دون إعادة تصنيفها. |

المسارات العشرة الأخرى: مقاطع `InvoiceOper` و`ItemOper` و`Common` و`LoadData` و`Report` و`Home.xaml.cs` و`Home.xaml` و`Resources.resx`، و`InventoryData`303 أسطر و`ItemProfitRow_ProfitDetails`25 سطراً محليان. النموذج المحلي ليس مفقوداً أو خارجياً؛ المجهول هو عقد `UtilitiesProj.Common.ToDataTable` و REPX والمكتبات/النشر. لا نفترض aliases أو cardinality أو مفاتيح دلالية من تشابه أسماء الحقول.

- [دفتر 827](evidence/coverage-ledger-07B4.csv) يحفظ نطاق كل جزء واتحاد النطاقات ومكمله النصي؛ حتى all-lines لا يمنح تصديق ميزة.
- [98 مرشح ملف](evidence/report-candidate-disposition-07B4.csv) فرز لفظي لا 98 تقريراً؛ FingerPrintDevice مطابقة لفظية للبصمة.
- [52 مرشح شاشة](evidence/report-screen-disposition-07B4.csv):35 اسماً لفظياً و 17 مرشحاً غير regex محدداً. ليست قائمة كل قدرات النظام أو 52 جسماً مقروءاً.
- قراءة launcher مؤسسة النقد في B3 لا تغطي جسمي `frmActsInvTotal` و`frmNkdTotSalePurch`؛ كلاهما متابعة B5. لا ترقية طفل بسبب caller أو Helper.

## 3. النتائج الجديدة

كل نتيجة أدناه `implementation-defect / confirmed / open-not-remediated`، ومتابعتها 8 غير المأذونة. «مؤكدة» للقرار أو التعارض المحلي لا خسارة أو استثناء إنتاجي شوهد. الأمثلة fixtures يدوية مستقلة، لا مخرجات SQL أو C#؛ صحة النشر والسياسة وقبول العرض منفصلة.

### P7-077 — حاسبتا تكلفة تحليل الفواتير تقربان كمية المقام إلى عدد صحيح قبل القسمة

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvAnalysis` — CalcUnitCost / CalcUnitCostStock → int totalQty → netCost/netProfit.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:493-610`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:717-730`؛ `SmartAuditERP/Properties/Resources.resx:1023-1053`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1597`.

**المشاهدة المحلية:** كل حاسبة تجمع تكلفة double لكنها تعرف totalQty من int، ثم تضيف (int)Math.Round(q) لكل مجموع كميات. إذا صار المقام 0 تنتقل إلى Items.purch_price. val في الكاتب و DDL كمية float/أساس تقبل الكسور، لا عد قطع صحيحاً مضموناً.

**السبب الجذري:** اختزال دقة كمية الأساس قبل حساب متوسط القيمة/الكمية؛ التقريب المالي النهائي لا يصلح مقاماً تغير بالفعل.

**الشروط والحواجز:** صنف بوحدة أساس كسرية، وتحويل وحدة 1 ونوع شراء صحيح بلا خصم أو ضريبة أو مرتجع، وسعر احتياطي معروف مختلف لعزل باقي عيوب التكلفة. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** شراء 0.4 بقيمة 4 يحول المقام إلى 0 فيختار الاحتياطي 99 بدلاً من متوسط 10؛ وشراء 0.6 بقيمة 6 يحول المقام إلى 1 فيعطي 6 بدلاً من 10.

**حد الدليل والشاهد المقابل:** الكميات الصحيحة قد تخفي العيب. هذا ليس P3-007 لتوازن مبلغ مقرب مع حفظ raw؛ هنا فقد دقة كمية داخل قارئ مستقل. لا نختار FIFO/متوسطاً متحركاً أو نؤكد نشر قاعدة.

**معالجة مقترحة — لم تنفذ:** احتفظ بكمية دقيقة وواحدة الوحدات حتى القسمة مع سياسة حد الصفر والدقة؛ سجل سبب fallback ولا تستبدل كمية موجبة بصفر. ثم اعتمد سياسة مصدر التكلفة مستقلة عن هذا الخلل.

**التحقق المخطط غير المنفذ:** P7B4T-01؛ P7B4T-02 في [خطة 48](VALIDATION-07B4.md). الحالة 1: يبقى المقام 0.4 والمتوسط 10؛ لا fallback سببه Math.Round فقط. الحالة 2: المتوسط 10 في الحالتين؛ الصفر الحقيقي له نتيجة موثقة لا نجاح مصطنع.

### P7-078 — تجميع الصنف في تحليل الفواتير يطبق آخر تكلفة مقروءة على كامل كمية الفترة

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvAnalysis` — ShowResultItem → GROUP BY ItemId/date → lastUnitCost → totalQtyForCost × lastUnitCost.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:826-860`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:717-730`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:991-1000`.

**المشاهدة المحلية:** داخل حلقة تواريخ الصنف تجمع totalQtyForCost وتستبدل lastUnitCost كل مرة، وبعدها تحسب netCost=totalQtyForCost*lastUnitCost. الاستعلام GROUP BY ItemId,date بلا ORDER BY. تجميع المجموعة والعميل، بالمقابل، يجمع rowQty*unitCost لكل تاريخ.

**السبب الجذري:** فقد ربط كل كمية بتاريخ تكلفتها، واستبدال fold جمع موزون بآخر عنصر لا يضمن ترتيباً زمنياً أصلاً.

**الشروط والحواجز:** للصنف حركتان مؤهلتان بكميتين 1 و 3 وتكلفتين موثقتين وقتيهما 10 و 20؛ لا تفترض صحة CalcUnitCost، بل استعمل مرجعاً مستقلاً لعزل هذا التراكم. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** مرجع مجموع التكلفة 1×10+3×20=70؛ الحلقة تعطي 80 إذا قرئ 20 أخيراً أو 40 إذا عكس الترتيب. حتى ترتيب زمني صريح وحده لا يجعل الكمية السابقة بسعرها.

**حد الدليل والشاهد المقابل:** تكلفة ثابتة لكل التواريخ قد تخفي العيب. لا ندعي أن SQL أعاد ترتيباً معيناً فعلاً أو أن آخر صف هو أحدث تاريخ؛ المقارنة بمسار المجموعة شاهد مقابل محلي لا تصديق لتكلفته.

**معالجة مقترحة — لم تنفذ:** اجمع تكلفة كل كمية مع مرجعها الزمني/سطرها وفق السياسة، أو اقرأ تكلفة محفوظة صحيحة بإصدار؛ لا تعالج بتغيير ORDER BY فقط. اختبر invariance لإعادة الترتيب وتغيير بعد التجميع.

**التحقق المخطط غير المنفذ:** P7B4T-03؛ P7B4T-04 في [خطة 48](VALIDATION-07B4.md). الحالة 1: إجمالي التكلفة 70 والربح من نفس الأساس؛ لا 80 الناتجة من آخر تكلفة. الحالة 2: يبقى الأول 70 في الترتيبين والثاني 40؛ لا أثر لترتيب القراءة.

### P7-079 — التجميع الشهري لتحليل الفواتير يوسع الفترة المطلوبة إلى حدود الشهر دون تقاطع

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvAnalysis` — ShowResultMonth → شهر مرشح → monthStart/monthEnd → استعلامات التفاصيل.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1285-1373`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:280-294`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1841-1842`.

**المشاهدة المحلية:** الاستعلام الأول يحدد الأشهر التي لها حركة ضمن الفترة، ثم كل استعلام عدد/رأس/تكلفة يستبدل البداية بأول الشهر والنهاية بآخر يوم منه، دون Max مع dateFrom أو Min مع dateTo. لهذا يمكن أن تدخل حركات قبل البداية وبعد النهاية المطلوبة.

**السبب الجذري:** استعمال الشهر كمجال كامل بدلاً من bucket داخل النطاق المطلوب؛ اختيار bucket لا يكفي لتقييد تفاصيله.

**الشروط والحواجز:** طلب 10–20 يناير، وحركات مؤهلة في 5 و 15 و 25 منه بقيم 100 و 200 و 300، مع واحدة داخل الفترة لضمان ظهور الشهر. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** تعيد استعلامات الشهر 600 بدلاً من 200 تحت تاريخي 10–20. استبعاد معظم آخر يوم الشهر عند<=monthEnd00:00 خلل حد مستقل تحت امتداد P3-023، وليس علاجاً للتوسيع.

**حد الدليل والشاهد المقابل:** اختيار شهر كامل قد يخفي التوسيع، لكنه لا يصلح cutoff لآخر يوم. لا تعد النتيجة صفراً إن منع الخيط/الإتاحة التنفيذ. هذه ليست مجرد نصف يوم مفقود في P3-023 بل استبدال نطاق بأكمله.

**معالجة مقترحة — لم تنفذ:** احسب كل bucket كتقاطع [max(requestFrom,monthStart),min(requestToExclusive,nextMonthStart)) مع الفترة المعتمدة، وطبق التقاطع نفسه على العدد والمبلغ والتكلفة والعنوان.

**التحقق المخطط غير المنفذ:** P7B4T-05؛ P7B4T-06 في [خطة 48](VALIDATION-07B4.md). الحالة 1: المصدر يعطي 200 فقط والعدد والتكلفة من الفترة نفسها. الحالة 2: لا بيانات خارج الطلب، ومجموع bucket ين يساوي مرجع الفترة؛ حدود النهاية وفق [from,toExclusive).

### P7-080 — مرشح المستخدم ومعيار المجموعة لا يطبقان في تجميعات من تحليل الفواتير

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvAnalysis` — اختيار Emp/Group → ShowResult validations → فلاتر ShowResult* اليدوية.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:281-297`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:637-679`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:765-808`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:898-938`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1026-1068`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1154-1198`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1285-1327`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1424-1466`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1559-1600`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:342-354`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:407-419`.

**المشاهدة المحلية:** ShowResult يفرض اختيار المستخدم عند إلغاء الكل، لكن sales_emp لا يدخل إلا في ShowResultEmp؛ بقية التجميعات السبعة لا تطبق الاختيار. وفي ShowResultGroup يعدد كل ItemsCategory دون قراءة chkAllGroups/cmbGroups، خلاف تطبيق معيار المجموعة في بقية الأبعاد.

**السبب الجذري:** تكرار بناء المعايير داخل كل بعد دون عقد مشترك كامل؛ المتحقق منه في الواجهة ليس بالضرورة مستعملاً في SQL.

**الشروط والحواجز:** مستخدمان أو مجموعتان بحركتين 100 و 200، وإلغاء الكل واختيار واحدة، مع سياسة أن controls العامة ترشح جميع الأبعاد كما يظهر النموذج. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** اختيار المستخدم صاحب 100 في بعد الصنف قد يبقي 300؛ واختيار مجموعة واحدة في بعد المجموعة يبقي صفوف المجموعات الأخرى. هذا خطأ تطبيق معيار، وليس إثبات خرق ACL خادم.

**حد الدليل والشاهد المقابل:** بعد المستخدم يطبق اختياره؛ أغلب الأبعاد الأخرى تطبق المجموعة. ليست مشكلة index0 P7-068 ولا حقل Safe_Emps P7-076 أو مرشح العميل P7-058، ولا يعاد عد عزل الفروع P2-010.

**معالجة مقترحة — لم تنفذ:** ReportCriteria immutable واحد يطبق بالكامل على مصدر مؤهل قبل كل group-by، أو عطّل معياراً غير ذي معنى مع تفسير صريح. اختبر تقاطع كل criterion مع كل بعد، لا بعداً واحداً فقط.

**التحقق المخطط غير المنفذ:** P7B4T-07؛ P7B4T-08 في [خطة 48](VALIDATION-07B4.md). الحالة 1: كل بعد مدعوم يساوي 100؛ لا 300 أو قبول اختيار مطلوب ثم مهمل. الحالة 2: المحددة صفها ومجموع 100 والكل 300 حسب الدور؛ لا صفوف خارج المجموعة المحددة.

### P7-081 — تجميع المخزن في تحليل الفواتير يبني مرشح الخزينة من قيمة المستودع

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvAnalysis` — ShowResultStock → safeVal / stockSelVal → [stock]=stockSelVal.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1583-1600`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:785-803`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:452-497`؛ `SmartAuditERP/Class/InvoiceOper.cs:1533-1534`؛ `SmartAuditERP/Class/Common.cs:133-152`.

**المشاهدة المحلية:** ShowResultStock يقرأ safeVal من cmbSafe لكنه لا يستعمله؛ عند !allSafe يضع [stock]={stockSelVal} المأخوذ من cmbStock. الحقل Inv.stock هو Treasury و Inv.safe هو Store في الكاتب؛ بقية الأبعاد تستعمل safeVal للخزينة.

**السبب الجذري:** متغير صحيح محمل لكن operand من ComboBox آخر استعمل في شرط حقل مختلف الهوية.

**الشروط والحواجز:** خزينة id7 ومستودع id3، وصفوف بمستودع 3 وخزينتين 7 و 3، مع إلغاء كل الخزائن وتحديد 7 والمستودع 3. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** يصبح الشرط stock=3 بدلاً من 7؛ قد يسقط صف 7 ويعرض صف خزينة 3. وإذا بقي المستودع بلا اختيار مع كل المستودعات، GetSelectedValue يعيد 0 فيقيد خزينة 0.

**حد الدليل والشاهد المقابل:** تساوي المعرفين صدفة قد يخفي العيب، وقراءة safeVal لا تثبت استعمالها. لا نساوي مجموعتي Safes/Stocks ولا نستنتج تفويضاً من تصحيح المتغير.

**معالجة مقترحة — لم تنفذ:** أنواع معرف WarehouseId/TreasuryId مختلفة، وربط criteria بالعمود الصحيح دون متغيرات متشابهة؛ افحص المعاملات بهويات غير متساوية ونطاق دور معلوم.

**التحقق المخطط غير المنفذ:** P7B4T-09؛ P7B4T-10 في [خطة 48](VALIDATION-07B4.md). الحالة 1: stock=7 و safe=3؛ لا استبدال 7 بقيمة 3. الحالة 2: الخزينة تظل 7 لا 0؛ تساوي المعرفين لا معيار نجاح وحيد.

### P7-082 — مرشح الفئة في تحليل الفواتير يبقي صافي الرأس كاملاً مقابل تكلفة البنود المصفاة

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvAnalysis` — ShowResultCust/Salesman/Emp/Month/Day/Stock → MIN(header) per GlobalID مقابل تفاصيل الفئة.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:923-995`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1061-1125`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1190-1255`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1323-1392`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1462-1530`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1596-1690`.

**المشاهدة المحلية:** بعد ترشيح ItemsCategory.id تجلب مصادر المبلغ MIN(tot_net)/MIN(InvTotal) لكل InvGlobalID ثم تجمع الرأس كاملاً، بينما مصدر الكمية/التكلفة تحت الفلتر يحوي بنود الفئة فقط. MIN يزيل ضرب join لكنه لا يخصص مبلغ الرأس للبنود المختارة.

**السبب الجذري:** خلط grain رأس مستند مع grain بنود مفلترة في مقياس صافي/ربح واحد.

**الشروط والحواجز:** فاتورة واحدة بفئتين: A بيع 100 وتكلفة 60، B بيع 300 وتكلفة 180، بلا ضريبة/خصم/إضافات أو مكونات، وحدد A. ثبّت تكاليف مرجعية مستقلة لعزل عيوب الحاسبة. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** المبلغ 400 وتكلفة 60 يعطيان ربح 340 بدلاً من مبلغ A100 وربح 40. في وضع الكل لا يحدث هذا الفرق من فلتر الفئة، فلا يصح وصفه دائماً بضعف join.

**حد الدليل والشاهد المقابل:** DISTINCT GlobalID و MIN لكل رأس شاهدان ضد الضرب البسيط لعدد البنود. إذا كانت السياسة عرض كامل الفواتير التي تحتوي الفئة، يجب التصريح بذلك وتوحيد تكلفة الرأس؛ النموذج الحالي يخلط المعنيين.

**معالجة مقترحة — لم تنفذ:** اعتمد عقداً صريحاً: measure بنود الفئة بحصص خصم/ضريبة وتكلفة مقابلة، أو فواتير مؤهلة كاملة بكل تفاصيلها مع عنوان مختلف؛ لا تجمع رأساً كاملاً وتكلفة subset تحت صافي واحد.

**التحقق المخطط غير المنفذ:** P7B4T-11؛ P7B4T-12 في [خطة 48](VALIDATION-07B4.md). الحالة 1: في عقد بنود الفئة المعلن: المبلغ 100 والتكلفة 60 والربح 40، أو عقد فاتورة كاملة صريح ومتماثل لا خليط. الحالة 2: التقسيم لا يضاعف الرأس؛ المحددة والكل كل منهما يصالح مرجعه grain واحداً دون افتراض علاج MIN للتخصيص.

### P7-083 — تجميعا الصنف والمجموعة في تحليل الفواتير يعرضان المجموع قبل الخصم والخصم صفراً

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvAnalysis` — ShowResultGroup / ShowResultItem → sum(val1*exchange_price) → netDiscount=0 → netProfit.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:691-755`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:817-880`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:652-687`؛ `SmartAuditERP/Class/InvoiceOper.cs:1545-1546`؛ `SmartAuditERP/Class/InvoiceOper.cs:1594-1598`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1413`.

**المشاهدة المحلية:** مصدر الإجمالي في البعدين SUM(val1*exchange_price) دون discount أو minus، ويثبت netDiscount=0. ثم يطرح التكلفة من هذا المجموع ويسند الناتج لأعمدة صافي الإجمالي وصافي الخصم وصافي الربح. الخصم محفوظ حقلاً مستقلاً في المصدر.

**السبب الجذري:** إسقاط إجمالي gross إلى أسماء net و discount دون إدخال الخصم، لا مجرد تسمية خانة تكلفة.

**الشروط والحواجز:** بند واحد qty1×100، خصم بند 10 وخصم رأس 0 وضريبة 0 وتكلفة مرجعية 60، أو خصم رأس 10 وبند 0 لعزل حالتي الخصم. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** تظهر 100 وخصم 0 وربح 40 بدلاً من صافي 90 وخصم 10 وربح 30. العيب قائم بكمية 1، فلا هو توزيع بلا كمية P7-070 ولا خصم POS المكرر P7-038.

**حد الدليل والشاهد المقابل:** انعدام الخصم يخفي هذا الفرق؛ الأساس الضريبي والعملة والإضافات تحتاج سياسة مستقلة. لا نعتمد رأساً خاطئاً بسبب P4-003 كمرجع؛ fixture هنا غير ضريبية متسقة.

**معالجة مقترحة — لم تنفذ:** نموذج مبالغ معرف يحفظ Gross/LineDiscount/HeaderDiscountAllocation/Tax/Net/Cost؛ اجمع كل مكون وفق وحدة واحدة وإشارة معتمدة، وطابق بنود الصنف/المجموعة مع مرجع مستقل.

**التحقق المخطط غير المنفذ:** P7B4T-13؛ P7B4T-14 في [خطة 48](VALIDATION-07B4.md). الحالة 1: صافي 90 وخصم 10 وربح 30 في المصدر والبطاقات والإخراج وفق العقد. الحالة 2: حصة 10 كاملة مرة واحدة في مثال السطر الواحد، وصافي 90؛ بلا خصم صافي 100.

### P7-084 — شروط نوع واتجاه تحليل الفواتير تسقط المرتجع وبيع POS العادي من صافي المخزن

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvAnalysis` — ShowResult* eligibility predicates → quantities/amounts/costs.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:683-717`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:807-837`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:939-980`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1293-1297`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1599-1683`؛ `SmartAuditERP/Properties/Resources.resx:3028-3064`؛ `SmartAuditERP/Class/InvoiceOper.cs:1528-1531`؛ `SmartAuditERP/Class/InvoiceOper.cs:1585-1585`؛ `SmartAuditERP/Class/InvoiceOper.cs:1613-1621`.

**المشاهدة المحلية:** تجميعات غير المخزن تشترط رأس proc_type=1 وسطر proc_type=2 فقط ولا تنشئ طرحاً لرأس المرتجع 2. مسار المخزن يقرأ البيع 2/رأس 1/سطر 2، لكنه يسمي فرع inv_type=3 ورأس 1 وسطر 3 مرتجعات ويضيف مبلغه؛ POS العادي له سطر 2 والمرتجع رأس 2 وفق العقود المرفقة. مصدر تكلفة المخزن أوسع من مصدر مبلغه ولا يقيد inv_type=2.

**السبب الجذري:** خلط أرقام نوع المستند مع إجراء الرأس واتجاه السطر وغياب مصفوفة أهلية signed واحدة للمقاييس المسماة صافية.

**الشروط والحواجز:** بيع 2 بقيمة 100، POS3 بقيمة 200 كلاهما رأس 1/سطر 2، ومرتجع عادي رأس 2/سطر 1 بقيمة 20؛ بلا ضريبة/خصم أو تعارض P4-001 للمرتجع المرتبط، ونوعان موثقان. في مسار btnShow لتحليل الفواتير توجد قراءة WPF من خيط خلفي قبل try؛ ومدخل Home معطل أولياً. الأمثلة تعزل الحساب/الاستعلام بعد تسجيل هذين الحاجزين، ولا تزعم أن الواجهة وصلت إليه فعلاً.

**مثال الأثر المشروط:** مسار المخزن يعطي مبلغ 100 لا صافي 280 في fixture، لكنه قد يضم كمية/تكلفة POS في كلفته. الأبعاد الأخرى تجمع البيع و POS300 دون طرح 20. إدخال أنواع أخرى ذات رأس 1/سطر 2 خطر أهلية إضافي، لا إيراد صالح تلقائياً.

**حد الدليل والشاهد المقابل:** لا نخلط مع تعيين 7/8 أو غياب 6 في P7-056/057 أو اتجاه إنتاج P7-060؛ هذا عقد تقرير مستقل. إن أريد gross sales لا net يجب تغيير الاسم ومقياس المقارنة، ولا يصبح فرع POS سطر 3 صحيحاً. الكاتب/النشر والمرتجع المرتبط P4-001 حواجز منفصلة.

**معالجة مقترحة — لم تنفذ:** كتالوج موثق لـ InvoiceType/ProcType/InventoryImpact وحالة الأهلية وإشارة المبيعات والمرتجع؛ مصدر واحد لكل measures بالفلتر نفسه، ثم group-by دون أرقام magic أو فرع POS باسم مرتجع.

**التحقق المخطط غير المنفذ:** P7B4T-15؛ P7B4T-16 في [خطة 48](VALIDATION-07B4.md). الحالة 1: عقد صافي معتمد يعطي 280 بإشارات متطابقة؛ POS سطر 2 لا يسقط والمرتجع لا يهمل. الحالة 2: لا يدخل غير البيع في ربح المبيعات؛ شاهد البيع فقط يبقى 100 ولا يبرر قبول المصفوفة كاملة.

### P7-085 — تعديل نص الصنف في الأرباح التفصيلية يبقي SelectedId السابق عند عرض التقرير

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptItemsProfitDetails` — تعديل txtItemName/Code دون Enter → bntShow → WHERE ItemId=SelectedId → عنوان الإخراج.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:193-210`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:502-518`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:546-558`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:575-628`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:631-684`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:837-852`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml:277-313`.

**المشاهدة المحلية:** حل الاسم/الرمز يحدث عند Enter أو حوار البحث؛ حقلا النص قابلان للتحرير بعد إلغاء الكل ولا TextChanged يبطل SelectedId. زر العرض يتحقق من اسم غير فارغ فقط، ثم يبني الشرط من SelectedId. الطباعة تنقل اسم/رمز controls الحاليين.

**السبب الجذري:** فصل غير محكوم بين هوية الصنف المحلولة و caption قابل للتغيير؛ لا حالة dirty/resolved أو تحقق نهائي تطابق النص والهوية.

**الشروط والحواجز:** اختر A بهوية 11 ثم غيّر النص إلى B دون Enter واضغط عرض؛ أو اكتب اسماً عند SelectedId=-1. لا SQL خبيث مطلوب للسيناريو.

**مثال الأثر المشروط:** قد تستعلم بنود A بينما يظهر B في رأس الطباعة، أو تستعلم ItemId=-1 دون رسالة حل هوية. هذا ليس مجرد انجراف تاريخ بعد عرض قديم، بل طلب جديد بهوية لا توافق مدخله.

**حد الدليل والشاهد المقابل:** Enter ناجح أو اختيار الحوار يضبط الهوية؛ إلغاء الكل يمسحها عند التحويل إلى الكل. حقن SQL في SearchByName/Code توسعة P1-011 مستقلة، و P7-045 يحفظ انجراف اللقطة بعد التحميل.

**معالجة مقترحة — لم تنفذ:** SelectedItem typed غير قابل للتحرير الحر أو أبطل الهوية فور تعديل النص ثم أعد الحل النهائي مع تحقق موجود/مفوض؛ snapshot يحتفظ بهوية واسم المصدر لا مدخل غير محلول.

**التحقق المخطط غير المنفذ:** P7B4T-17؛ P7B4T-18 في [خطة 48](VALIDATION-07B4.md). الحالة 1: يرفض حتى حل B أو يحل B موثوقاً؛ لا استعلام A مع captionB. الحالة 2: لا استعلام بهوية سالبة أو قديمة؛ بعد الحل تتطابق الهوية والاسم والمخرج.

### P7-086 — قارئ إشعارات الفواتير يطرح الضريبة الإضافية من VAT المحفوظة كحقل مستقل

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvNotfic` — Inv.tax / ExtraVAT → BindingListOfInvoices1 → VAT/TotalTax → grid/summaries/CSV.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:295-300`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:438-455`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:534-555`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:706-727`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml:312-337`؛ `SmartAuditERP/Class/InvoiceOper.cs:1546-1546`؛ `SmartAuditERP/Class/InvoiceOper.cs:1560-1560`؛ `SmartAuditERP/Class/InvoiceOper.cs:4209-4212`؛ `SmartAuditERP/Class/ItemOper.cs:1494-1498`؛ `SmartAuditERP/Class/ItemOper.cs:1635-1641`.

**المشاهدة المحلية:** يسمي القارئ row[tax] taxTotal ويضع TotalTax=taxTotal، ثم VAT=taxTotal-extraVAT إذا كان الفرق موجباً. الكاتب يضع inv.VAT في tax و inv.ExtraVAT في ExtraVAT، والحاسبة تجمع vat و extraVat منفصلين ثم Net=Total+VAT+ExtraVAT؛ ليست tax في هذا العقد مجموع الضريبتين.

**السبب الجذري:** قارئ يفترض أن الضريبة العادية aggregate شامل للإضافية خلاف عقد الكاتب المحلي، مع fallback آخر غير متجانس عند الفرق غير الموجب.

**الشروط والحواجز:** إشعار مخزن وفق الكاتب المرفق بضريبة عادية 20 وإضافية 5، وصافي متفق مع المكونين؛ لا تفترض أن كل نشر يتبع هذا العقد قبل توثيقه. اعزل فشل الصفوف و joins والصلاحية أولاً.

**مثال الأثر المشروط:** يظهر VAT15 و Extra5 و TotalTax20 بدلاً من 20 و 5 و 25. وإذا كانت tax=extra=5 يعطي VAT5 و Extra5 و TotalTax5؛ لا يتحقق جمع العمودين أيضاً. Grid وملخص و CSV يستهلكون الإسقاط نفسه.

**حد الدليل والشاهد المقابل:** عند extra=0 قد تتطابق الأرقام. تغيير معنى tax في ترحيل خارجي يحتاج عقد إصدار، لا نفترضه. ليست P7-047 لتصدير نسبة مكان مبلغ، ولا شهادة امتثال أو ضريبة منشورة؛ التناقض مع الكاتب محلي مثبت.

**معالجة مقترحة — لم تنفذ:** حسم schema/DTO بإصدار: OrdinaryVATAmount و AdditionalTaxAmount و TotalTaxAmount؛ اقرأ الأولين كما كتبا واشتق المجموع مرة أو اقرأ breakdown إصدار موثوقاً. لا تستنتج دلالة الحقل من اسمه وحده.

**التحقق المخطط غير المنفذ:** P7B4T-19؛ P7B4T-20 في [خطة 48](VALIDATION-07B4.md). الحالة 1: VAT20 و Extra5 و TotalTax25 وتتسق مع صافي الأصل؛ لا 15/5/20. الحالة 2: 20/0/20 ثم 5/5/10؛ لا يمر شاهد extra0 وحده كقبول كامل.

### P7-087 — تفاصيل المشتريات تربط معرف المستودع بجدول الخزائن عند جلب الاسم

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvPurchaseDetails` — LoadData.Invertories → Inv.safe → BuildOptimizedSql JOIN Stocks → InvertoryName.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:274-284`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:601-607`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:648-650`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:705-723`؛ `SmartAuditERP/Class/LoadData.cs:12-25`؛ `SmartAuditERP/Class/Common.cs:133-151`؛ `SmartAuditERP/Class/InvoiceOper.cs:1533-1534`؛ `SmartAuditERP/Properties/Resources.resx:1629-1641`؛ `SmartAuditERP/Properties/Resources.resx:1992-2005`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml:644-646`.

**المشاهدة المحلية:** المرشح يقرأ المستودعات من Safes و Inv.safe يكتب من Store، لكن الاستعلام المحسن يربط Stocks.id=inv.safe ويسمي الناتج StoreName ثم InvertoryName. Stocks للخزائن في العقد المحلي لا المستودعات. overrideSql يستعمل Common.GetStoreName الذي يقرأ Safes، وهو شاهد مقابل.

**السبب الجذري:** تحسين N+1 غيّر جدول lookup إلى كيان آخر ذي id رقمي مستقل، مع إبقاء تسمية المستودع.

**الشروط والحواجز:** Safes.id3 اسمه مستودع A و Stocks.id3 اسمه خزينة B، أو لا يوجد Stocks.id3، وفاتورة store3؛ شغّل لاحقاً المسار المحلي المحسن لا override بفرضه.

**مثال الأثر المشروط:** يعرض اسم خزينة B أو فارغاً تحت المستودع، وينقله إلى الطباعة/التصدير؛ لا يثبت هذا تغيير هوية Store أو رصيد المخزون المحفوظ.

**حد الدليل والشاهد المقابل:** تطابق الأسماء/الأرقام عرضاً قد يخفي العيب، و LEFT JOIN يحفظ الفاتورة عند غياب الاسم فلا نزعم إسقاطها. الحقول المالية الأخرى و P7-047 تبقى نتائجها السابقة.

**معالجة مقترحة — لم تنفذ:** JOIN Safes بهوية مستودع typed/alias ثابت؛ اختبر تطابقه مع lookup العقد القديم ومعرفات متباعدة، مع نطاق وصول محكم لا تصحيح الاسم وحده.

**التحقق المخطط غير المنفذ:** P7B4T-21؛ P7B4T-22 في [خطة 48](VALIDATION-07B4.md). الحالة 1: InvertoryName=مستودع A والهوية Store3؛ لا خزينة B. الحالة 2: يبقى اسم المستودع A دون إسقاط الفاتورة أو اختراع اسم؛ يطابق القراء بالعقد نفسه.

### P7-088 — خيار كل الفروع في تفاصيل المشتريات يبقي قيد الفرع المختار سابقاً

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvPurchaseDetails` — chkAllBranches_Changed → cmbBranches enabled only → CollectQueryParams SelectedIndex.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:183-218`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:342-350`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:1125-1129`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml:303-324`.

**المشاهدة المحلية:** معالج كل الفروع يغير IsEnabled فقط ولا يمسح الاختيار. CollectQueryParams يضيف inv.branch عند SelectedIndex>-1 دون فحص chkAllBranches، لذلك يبقى الفرع السابق فعالاً بعد تحديد الكل.

**السبب الجذري:** حالة all في العرض منفصلة عن معيار المصدر؛ بقاء قيمة تحكم معطل يستعمل كفلتر خفي.

**الشروط والحواجز:** مستخدم مصرح له بكل الفروع و checkbox ظاهرة، اختارفرع A ثم فعّل الكل؛ بيانات A100 و B200. إذا كانت BranchPermissionsi تخفي الكل لا تفترض الوصول لهذا السيناريو.

**مثال الأثر المشروط:** قد يبقى مصدر A100 بدلاً من مجموع النطاق المصرح 300 مع ظهور الكل. هذا تضييق خفي لا توسعة صلاحية مثبتة ولا P7-065 لاختلاف نطاق مصدرين ماليين.

**حد الدليل والشاهد المقابل:** بداية SelectedIndex=-1 قد تعطي الكل؛ مسار الفرع المقيد يخفي checkbox وهو حاجز مستقل. لا تحل القضية بإزالة عزل خادم أو جعل-1 إذناً عاماً.

**معالجة مقترحة — لم تنفذ:** BranchScope صريح intersect مع الدور؛ الكل يزيل اختيار الفلتر داخل نطاق مصرح، أو تجاهل الاختيار عندما all=true، مع تحديث snapshot وإظهار النطاق الفعلي.

**التحقق المخطط غير المنفذ:** P7B4T-23؛ P7B4T-24 في [خطة 48](VALIDATION-07B4.md). الحالة 1: الكل المصرح 300 لا 100 المتبقية؛ لا قيد فرع خفي. الحالة 2: المحدد 200 للمخول؛ المقيد لا يرى B ولا يتحول فشل الاختيار إلى كل الفروع.

### P7-089 — منتقيا تاريخ تحليل الفواتير موضوعان في خلية Grid نفسها

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvAnalysis` — XAML Grid.Row1 → txtDateFrom / txtDateTo default Grid.Column0.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:299-335`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:64-68`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:454-472`.

**المشاهدة المحلية:** Grid التواريخ يعرّف أعمدة متعددة لكن DatePicker للبداية و DatePicker للنهاية ابنان مباشران بلا Grid.Column أو Margin مختلف أو صف منفصل. فيقعان معاً في الخلية الافتراضية 0؛ المستخدم والعميل فقط لهما 4 و 6. يقرأ C# تاريخين مستقلين رغم عدم فصلهما تخطيطياً.

**السبب الجذري:** فقد تعيين attached layout property عند تحويل النموذج؛ وجود تحكمين مسميين لا يضمن قابلية رؤية/تعديل كليهما.

**الشروط والحواجز:** XAML المرفق وقيم Grid.Column الافتراضية، ولا style/template خارجي يغير التعيين؛ قبول hit-testing والـ Tab/RTL الحقيقي يحتاج WPF مأذوناً. Home معطل أولياً فلا تفترض مدخلاً حياً متاحاً.

**مثال الأثر المشروط:** يتراكب نطاقا عرض المنتقيين، وقد يغطي الثاني الأول فيصعب تعديل بداية الفترة بالفأرة. لا نزعم لقطة render أو منع لوحة المفاتيح كلياً؛ الإحداثيات المتطابقة المحلية هي المؤكدة.

**حد الدليل والشاهد المقابل:** التعبئة البرمجية تستطيع وضع تاريخين و GetDateFrom/To يقرآن حقليهما؛ لا غياب تحكم أو دالة تاريخ. هذه ملاحظة وظيفية محددة من B4 وليست بدءاً أو اكتمالاً لمراجعة UI/RTL/accessibility في 7C.

**معالجة مقترحة — لم تنفذ:** Grid.Column0 و 2 منفصلان مع labels وربط وصول وترتيب تنقل مناسبين، ثم اختبار actual bounds/hit-test و RTL/DPI ولوحة المفاتيح. لا تكتف بوجود x:Name.

**التحقق المخطط غير المنفذ:** P7B4T-25؛ P7B4T-26 في [خطة 48](VALIDATION-07B4.md). الحالة 1: منطقتان غير متراكبتين، وتغييرالبداية لا يحجب النهاية أو يبدل معياراً آخر. الحالة 2: كلا التاريخين قابلان للتحرير ومعياراهما محفوظان؛ لا تعميم أن 7C/UI كله اجتاز.

## 4. توسعات أصول سابقة — ليست 17 نتيجة أخرى

[CSV التوسعات](evidence/historical-extensions-07B4.csv) يسجل الذيل الدقيق. نواة أول 248 وجدولتها محفوظتان؛ التوسعة لا تغلق الأصل ولا تعيد حسم policy أو deployment:

| الامتداد | الأصل وحالته التاريخية | الملاحظة المضافة فقط | الدليل |
|---|---|---|---|
| EX7B4-01 | P1-004 — High/repository-gap؛ next_phase=8 | متصلون إضافيون وقوالب REPX مسماة؛ توريدها وإصدارها وعقد بياناتها غير مثبتة من وجود FromFile أو مسار. لا نقص مستقل لكل اسم. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1736-1796`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:758-798`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:754-785`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:782-816` |
| EX7B4-02 | P1-011 — High/confirmed؛ next_phase=7;8 | يدخل اسم/رمز TextBox في SELECT Items داخل literal SQL دون معاملات. هذه توسعة مصدر→مصَب للجذر السابق؛ لا payload أو اتصال SQL نفذ، ولا يخلط بـ DataView. | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:546-558`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:575-628`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml:292-313` |
| EX7B4-03 | P1-013 — High/potential؛ next_phase=7;8 | تحليل الفواتير يستدعي ApplyPermissionToForm قبل Show، ومدخله معطل أولياً؛ مداخل الأرباح/الإشعارات/المشتريات المختارة لا تستدعي الحارس هنا. لا يثبت أي منهما صلاحية أو منعاً مركزياً. | `SmartAuditERP/Home.xaml.cs:2898-2903`؛ `SmartAuditERP/Home.xaml.cs:3104-3111`؛ `SmartAuditERP/Home.xaml.cs:3126-3152`؛ `SmartAuditERP/Home.xaml.cs:3543-3543`؛ `SmartAuditERP/Home.xaml:382-382` |
| EX7B4-04 | P1-033 — Medium/confirmed؛ next_phase=7 | زر حفظ المظهر يكتب XML ويعلن الحفظ، لكن LoadDGvSetting يفحص وجود الملف فقط دون استعادة الأعمدة. هذا امتداد أصل الاكتمال، لا عيب لكل معالج RadioButton فارغ؛ زر العرض ينفذ الأبعاد فعلياً. | `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:171-180`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:961-987`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:990-1002`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml:866-878` |
| EX7B4-05 | P2-001 — High/confirmed؛ next_phase=8 | الفتح من الأرباح ينفذ configure/Navigate قبل Show بلا إعادة تفويض محلية؛ فتح المشتريات بلا ApplyPermission هنا. بعض مداخل الإشعار تستدعي الحارس قبل تغيير الاسم ثم Show، وتفاصيله تظهر زر إعادة التكلفة بعده. لا دليل على تنفيذ إعادة التكلفة أو تخطي خادم فعلي. | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:422-477`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:1051-1070`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:572-586`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:606-663`؛ `SmartAuditERP/Home.xaml.cs:3543-3543` |
| EX7B4-06 | P2-010 — High/confirmed؛ next_phase=7;8 | تحليل الفواتير والإشعارات لا يضيفان branch في المصادر المحددة، مقابل حارس BranchNo في الأرباح ومنطق خيارات في المشتريات. غياب/اختلاف scope محلي لا يثبت ACL منشوراً أو إذن الكل. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:637-717`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:493-599`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:239-242`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:295-318`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:213-216`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:183-218`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:342-350` |
| EX7B4-07 | P2-011 — High/confirmed؛ next_phase=8 | تحميل مواقع عام في التحليل والأرباح مقابل LoadData.Invertories(EmpNo) في المشتريات؛ خيار كل المستودعات يزيل فلتر SQL المحلي ولا يثبت تقاطع تعيينات المورد. لا تعد حصر الأسماء سياسة authorization. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:81-119`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:110-121`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:185-191`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:274-284`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:369-373`؛ `SmartAuditERP/Class/LoadData.cs:12-25` |
| EX7B4-08 | P3-023 — Medium/confirmed؛ next_phase=7;8 | نهاية الشهر عند 00:00 تسقط بقية آخر يوم، واليوم المنتهي <=غد 00:00 قد يكرر حد منتصف الليل؛ نهاية 23:59 الصريحة في الأرباح والإشعارات والمشتريات تستبعد ثواني الدقيقة الأخيرة. توسيع الشهر P7-079 مستقل عن هذا cutoff. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:653-677`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1331-1358`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1470-1497`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:218-247`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:356-363`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml:358-362`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:278-288`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml:680-684`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:400-414` |
| EX7B4-09 | P4-007 — High/potential؛ next_phase=8 | CalcUnitCost يجمع رأس 1/سطر 1 بلا inv_type=1 فيخلط مصادر دخول منها غير الشراء؛ مسار المرتجع يطلب رأس proc_type3 لا 2 ويضيفه. يقيد CalcUnitCostStock النوع 1 لكنه يكرر proc3. أثر سياسة التكلفة يبقى potential كما كان؛ لا يثبت هذا متوسطاً تاريخياً معتمداً. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:493-610`؛ `SmartAuditERP/Properties/Resources.resx:3028-3064`؛ `SmartAuditERP/Class/InvoiceOper.cs:1528-1531`؛ `SmartAuditERP/Class/InvoiceOper.cs:1585-1585` |
| EX7B4-10 | P7-041 — High/confirmed؛ next_phase=8 | بسط التكلفة SUM(val*exchange_price) يضرب كمية الأساس بسعر وحدة البيع لا val1؛ عبوة 10 بسعر 50 تعطي تكلفة أساس 50 بدلاً من 5، أي عشرة أضعاف. امتداد الجذر الوحداتي لا نتيجة جديدة، مع بقاء أخطاء المصدر والدقة منفصلة. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:500-509`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:562-570`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1597`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1404` |
| EX7B4-11 | P7-045 — High/confirmed؛ next_phase=8 | مصادر الطباعة تقرأ معايير controls الحالية مع صفوف وملخصات التحميل السابق؛ المشتريات تلتقط DTO على UI للعامل وهو شاهد مقابل للخيط، لكنها لا تجمد عنوان الإخراج مع النتيجة. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1812-1857`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:837-856`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:795-815`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:430-483` |
| EX7B4-12 | P7-046 — Medium/confirmed؛ next_phase=8 | قد تسقط صفوف الإشعارات والمشتريات في catch{} ثم تعاد قائمة دون عد الرفض؛ الأرباح تمسح القائمة داخل try وقبل الاستعلام، وقد تبقي ملخصاً قديماً عند الفشل. لا يعني كل empty خطأ، ولا Progress100 اكتمال المال. | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:177-183`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:342-353`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:450-479`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:688-696`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:476-513`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:739-757` |
| EX7B4-13 | P7-048 — Medium/confirmed؛ next_phase=8 | CSV الأرباح والإشعارات يدمج نصوصاً و N2 مفصولة بفواصل دون quoting أو escaping؛ فاصل أو سطر داخل اسم أو فاصلة ألوف تغير الأعمدة. TSV المشتريات مسجل سلفاً ولا يعاد عده. | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:697-733`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:685-738` |
| EX7B4-14 | P7-049 — High/potential؛ next_phase=8 | نصوص غير موثوقة تكتب CSV أو تسند إلى خلايا COM بلا سياسة نص/صيغة صريحة؛ الأثر مشروط بقارئ Excel وإعداداته. تبقى potential؛ لم يفتح ملف أو تفسر صيغة أو يشغل COM. | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:720-733`؛ `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:706-737`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:1955-1983` |
| EX7B4-15 | P7-054 — High/confirmed؛ next_phase=8 | زر التحليل يبدأ new Thread ثم يقرأ ShowResult قيم IsChecked/SelectedValue قبل Dispatcher وقبل try. مساعدات Dispatcher اللاحقة لا تصلح الحارس الأول. التقاط QueryParams في المشتريات على UI قبل Task.Run شاهد مقابل، لا عيب جديد ثانٍ. | `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:258-320`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml.cs:332-341`؛ `SmartAuditERP/Form_WPF/frmRptInvAnalysis.xaml:545-549`؛ `SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs:430-482` |
| EX7B4-16 | P7-055 — High/confirmed؛ next_phase=8 | طباعة الإشعارات تمرر null إلى BindToData مع تواريخ فقط لا_invoicesList؛ تجعل overloads لـ GridView/DataTable عقد البناء والحسم حاجزاً أسبق، ثم null لا يمثل الصفوف. لا ادعاء صفحة فارغة مرصودة أو DTO مفقود. | `SmartAuditERP/Form_WPF/frmRptInvNotfic.xaml.cs:754-809`؛ `SmartAuditERP/Class/Report.cs:380-406`؛ `SmartAuditERP/Class/Report.cs:451-462`؛ `SmartAuditERP/Class/Report.cs:531-553`؛ `SmartAuditERP/Class/Report.cs:597-608` |
| EX7B4-17 | P7-061 — High/confirmed؛ next_phase=8 | الأرباح التفصيلية توجه فتح الفاتورة بمقارنة أسماء عربية، فيبقى النص المترجم دون فرع مطابق. GlobalID محفوظ ومستعمل هنا، فيقاوم جزء فقد الفرع/الرقم المحلي من الأصل ولا ينسب ذلك الجزء لهذا المتصل. لا نوع رقمي في DTO لتوجيه مستقل عن اللغة. | `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:281-285`؛ `SmartAuditERP/Form_WPF/frmRptItemsProfitDetails.xaml.cs:422-477`؛ `SmartAuditERP/Class_WPF/ItemProfitRow_ProfitDetails.cs:6-8`؛ `SmartAuditERP/Class_WPF/ItemProfitRow_ProfitDetails.cs:21-23`؛ `SmartAuditERP/Properties/Resources.resx:3028-3038` |

## 5. الشواهد المقابلة والعقود غير المحسومة

- **الأرباح التفصيلية ليست نسخة العيب في تقرير الأرباح السابق:** تفصل DgvAvgCost/DgvTotAvg، وتحسب خصم السطر/حصة الرأس مرة في مسار موحد، وتطرح ملخص المرتجع من البيع. لا نعمم P7-038/039/070 عليها. أما وحدة تكلفة الوحدة قياساً إلى وحدة البيع والتقريب ومصدر AvrgCost فتحتاج عقداً مستقلاً.
- **GlobalID محفوظ في تفاصيل الأرباح** وينقل إلى فتح المصدر؛ العيب المضاف إلى P7-061 هنا توجيه بأسماء عربية، لا فقد هوية الفرع/الرقم المحلي. الهوية لا تعوض إعادة التفويض.
- **المشتريات تلتقط QueryParams على UI قبل Task.Run**، وتستعمل اتصالاً محلياً using وملخصاً signed. لا نعمم عليها حاجز P7-054 أو جمع المرتجع موجباً. بقاء معايير عنوان الطباعة controls حيّة توسعة P7-045 مستقلة.
- **MIN لكل GlobalID يمنع الضرب البسيط للرأس** لكنه لا يخصص رأس الفاتورة للفئة المصفاة. لا نوصي بمجرد DISTINCT لعلاج P7-082.
- **تقرير إشعار 22 يوافق GetInvoiceType و Home في مدين/دائن**، بينما seed InvTypes المرفق يعكس أسماءهما. لا نتيجة «فلتر معكوس» من seed وحده؛ هل الملخص gross movements أم أثر صافٍ سؤال سياسة لم يحسم.
- الإشعارات تمرر `@DateFrom/@DateTo` عند استعمالهما؛ المعاملان الإضافيان `@date1/@date2` غير المستعملين ليسا missing parameters. `InventoryData` المحلي موجود ومقروء. overloads Report والمكتبة والقالب حواجز حقيقية لا DTO مخمن غائب.
- COM فيه مسار return قبل Close/Quit، والاستعلامات متكررة لكل عضو/تاريخ/صف. **هذه مؤشرات 7C فقط**، لا تشغيل Excel أو تسرب/latency أو فهرس مفقود مثبت من النص.
- handlers الأبعاد الفارغة لا تعني أن التحليل غير منفذ؛ زر العرض يختار ShowResult* فعلياً. نقص استعادة المظهر يبقى تحت P1-033، لا نتيجة لكل RadioButton.

## 6. الحفظ والتحقق وحدوده

تحمي [لقطة 248](evidence/findings-through-07B3.csv) ذات SHA256=`993dbf53411cc2f495136bc699f3960ab2a10d6e9eb699d44d643195bac4f13f`، و[نصوص فهارس B3 الأصلية](evidence/shared-indexes-through-07B3.json)، و[provenance155](evidence/provenance-07B4.json) التاريخ، بما فيه checks-07B3 الفعلي وكل تقاريره وأدواته. لم يستبدل baseline أو تقرير أو helper أو checks محمي.

أضيف adapter جديد يقرأ B3 بمدخلاته 248 وفهارسه الدقيقة **في الذاكرة عند المسارات المنطقية نفسها**؛ لا تمرير 261 والفهارس الحالية إلى helper المحمي أو تبديلها على القرص. عزل A/200 و B1/223 و B2/237 محفوظ. مقاييس الفحص بمدقق أحدث ليست إعادة إنتاج bytes للـ checks التاريخية.

[VALIDATION-07B4](VALIDATION-07B4.md) و[checks الفعلي](evidence/checks-07B4.json) يفصلان تحقق الوثائق عن قبول ERP. [witnesses23+18](evidence/report-witnesses-07B4.json) نماذج وملاحظات نصية فقط. **صفر اختبار نظام أو SQL أومزود وصفر معالجة**؛ نجاح الأرقام والروابط والبصمات لا يشهد صحة المال أو كل المزايا.

## 7. المتابعة المعلنة ضمن 7 — لا إذن 8

**7B5 التالية**: `frmRptInvSalesDetails` و`frmRptInvSalesDetailsPos` و`frmRptInvSalesDetailsPosAndroid` و`frmRptItemsSalesDetails` و`frmRptItemsSalesDetailsPOS` كأسماء فرز عمل؛ ثم بقية المقاطع المالية/الإخراج والمتصلين ومرشحي غير regex، و`frmActsInvTotal` و`frmNkdTotSalePurch`. يلزم تثبيت الاسم الفعلي من الحصر وقراءة الجسم قبل ادعاء تغطيته، أو استبعاد مسند أو إعلان جزء 7B إضافي إن لزم.

**7C لم تبدأ**: بقية HR/PM/البحري و UI/events/resources/timers/async/cancel/connections، والاختصارات و RTL/accessibility/cultures/messages وأداء المصدر. لا أحكام فهارس دون مخطط وخطط تنفيذ أو قياسات منقحة مأذونة.

[backlog10](evidence/continuation-backlog-07B4.csv) يربط الأصل BK7 بالأجزاء المتتابعة. [H7B4/Q7B4](INVOICE-ANALYSIS-REPORTS-07B4.md) تضاف إلى H3/H4/H5/H6/H7/H7B/H7B2/H7B3، ولا تجيب عنها أداة النص. المرحلة 7 لا تغلق حتى تغطية المعايير/المصادر/الهوية/الحساب/الحالة/المجاميع/GL/الإخراج/ACL أو الاستبعاد المسند، لا من 98/52 اسماً أو 334 مساراً. **8 والإصلاحات تحتاج إذناً منفصلاً ومتطلبات مستقلة؛ لا انتقال تلقائي.**
