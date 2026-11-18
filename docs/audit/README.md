# تدقيق SmartAuditERP — فهرس العمل

**مرجع التدقيق المعلن:** 2026-11-16 UTC.  
**الفرع:** `arena/94ae8414-smartauditerp`  
**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`

## الحالة الحالية

سُلّمت 1–6 كمراجعات ساكنة بنطاقاتها، ثم 7A/B1/B2/B3/B4؛ أحدث تسليم **[7B5](PHASE-07B5.md)** لخمسة أجسام تقارير تفاصيل البيع/POS/Android وتجميع الأصناف ومقاطع دعم محددة. **لم تكتمل 7B أو 7. أُعلنت 7B6 لبقية المالية والإخراج والمتصلين ومرشحي غير regex والأبناء؛ لم تبدأ. 7C لم تبدأ. المرحلة 8 غير مأذونة ولم تبدأ.** استمرار «طيب واصل العمل» إذن تدقيق 7 فقط، لا معالجة أو تشغيل.

لا تعديل لملفات التطبيق أو build أو ERP/Windows/WPF/SQL/COM/DevExpress/SDK/Office أو مزود أو طابعة/جهاز. قبول التطبيق والإصلاحات و commit/push: **صفر**. فحوص الوثائق والنماذج اليدوية ليست شهادة صحة مالية/أمنية أو امتثال أو العثور على كل العيوب.

الأعداد والحالات والباقي في التقارير و checks المجمدة **تاريخية عند التسليم**. لم تُعد كتابة تقاريرها أو checks أو helpers. يتطور هذا الفهرس والسجل والمدقق بإضافة محددة، مع عزل مدخلات كل تاريخ عن الحالة الحالية في الذاكرة.

### النطاق — اتحاد مسارات لا نسبة اكتمال

الحصر الأصلي **827 ملف مشروع و 29,128,444 بايت**؛ 754 ملف C#/XAML و 394,029 سطراً خارج bin/obj. أعداد المسارات لها نطاقات منتقاة، لا كل أسطرها أو callers/templates ولا تغطية تنفيذية:

| المرحلة/الجزء | مسارات نطاقها | تقاطعها مع الاتحاد السابق | جديدة على الاتحاد | الاتحاد التراكمي |
|---|---:|---:|---:|---:|
|1|52|—|52|52|
|2|60|20|40|92|
|3|50|15|35|127|
|4|48|15|33|160|
|5|54|24|30|190|
|6|53|17|36|226|
|7A — تاريخياً|47|7|40|266|
|7B1 — تاريخياً|42|20|22|288|
|7B2 — تاريخياً|33|15|18|306|
|7B3 — تاريخياً|27|7|20|326|
|7B4 — تاريخياً|18|10|8|334|
|**7B5 — إضافة محدودة**|**26**|**13**|**13**|**347**|

بقي **480 مساراً inventory-only** بلا نطاق منتقى، فضلاً عن مقاطع داخل 347. [دفتر 827](evidence/coverage-ledger-07B5.csv) يحفظ كل نطاق ومكمله؛ حتى all-lines لا يشهد اكتمال ميزة. [backlog10](evidence/continuation-backlog-07B5.csv) يربط BK7B5 بـ BK7B4 و BK7 الأصلي والباقي 7B6/7C. لا إغلاق 7 دون استكمال أو استبعاد مسند أو أجزاء إضافية معلنة.

- **7B1:** محرك الطباعة والإخراج والباركود والتفقيط ومقاطع callers وثلاثة أجسام؛ ليس كل caller أو REPX.
- **7B2:** ستة أجسام مالية/مخزنية ودعم محدد؛ [scope33](review-scope-07B2.csv) حده التاريخي.
- **7B3:** تسعة أجسام أعمال و launcher ودعم محدد؛ [scope27](review-scope-07B3.csv). قراءة launcher لا تغطي أبناءه.
- **7B4:** أربعة أجسام تحليل/أرباح/إشعارات/مشتريات؛ [scope18](review-scope-07B4.csv). حواجز الخيط والإتاحة والبناء تسبق قبول الأثر اللاحق.
- **7B5:** خمسة أجسام، وحوار عميل ونماذج محلية ومقاطع XAML/دفع/كاتب/قيد/مصدر/مداخل؛ [scope26](review-scope-07B5.csv). لا كل عائلة الدفع أو العملاء أو القوالب والنشر. `frmRptItemsSalesDetailsPOS` لا يساوي `frmItemsalesdetailsPos` المختلف المؤجل 7B6.
- [98 مرشح ملف](evidence/report-candidate-disposition-07B5.csv) و[52 مرشح شاشة](evidence/report-screen-disposition-07B5.csv) =35 لفظياً+17 غير regex، **ليست أعداد ميزات أو أجسام مقروءة**؛ FingerPrintDevice مطابقة للبصمة. الأبناء `frmActsInvTotal` و`frmNkdTotSalePurch` لا تغطى بقراءة launcher.

### سجل النتائج المفتوحة

| النطاق | العدد | حرجة | عالية | متوسطة | منخفضة |
|---|---:|---:|---:|---:|---:|
|المرحلة 1 تاريخياً|33|2|17|13|1|
|المرحلة 2 — جديدة|16|0|10|6|0|
|المرحلة 3 — جديدة|25|0|18|7|0|
|المرحلة 4 — جديدة|32|0|24|8|0|
|المرحلة 5 — جديدة|31|0|22|9|0|
|المرحلة 6 — جديدة|35|0|26|9|0|
|7A — جديدة تاريخياً|28|0|20|8|0|
|7B1 — جديدة تاريخياً|23|0|11|12|0|
|7B2 — جديدة تاريخياً|14|0|9|5|0|
|7B3 — جديدة تاريخياً|11|0|6|5|0|
|7B4 — جديدة تاريخياً|13|0|7|6|0|
|**7B5 — جديدة**|**5**|**0**|**3**|**2**|**0**|
|**التراكمي المفتوح**|**266**|**2**|**173**|**90**|**1**|

بحسب الإثبات: **231 مؤكدة، 28 محتملة، 7 فجوات مستودع**. المؤكد محلياً بشروطه ليس حادث إنتاج؛ الجميع open-not-remediated. P1-013 و P4-007 و P7-032 و P7-049 وغيرها من potential لم تُرقّ بسبب توسيع دليل أو fixture يدوي.

أضافت 7B5 **24 ذيلاً للأدلة فقط** مع حفظ نواة وتصنيف وعنوان وحالة **وكل next_phase لأول 261**. ليست 24 نتيجة أخرى أو علاجاً. 43 نتيجة تاريخية تحمل متابعة 7؛ الجديد next_phase=8 خطة لا إذن.

[لقطة 261](evidence/findings-through-07B4.csv) SHA256=`a951b1a4b2e3df5342f82e9a69736a3cf37e7507cb55809d5e5b628e9ca6b258` و[فهارس B4 الدقيقة](evidence/shared-indexes-through-07B4.json) و[provenance178](evidence/provenance-07B5.json) تحمي 178 artifact تاريخية، منها 155 السابقة و checksB4 الفعلي. يقرأ المدقق B4 بمدخلاته 261 وفهارسه في الذاكرة، لا 266 أو فهارسها الحالية، وكذلك A/B1/B2/B3 بمدخلاتها الخاصة؛ لا baseline أو helper/checks محمي يعاد توليده.

مرجع 16 نوفمبر تاريخ معلن للجلسة لا ادعاء ساعة البيئة؛ ملاحظة الدخول 18 نوفمبر محفوظة منفصلة في provenance7B5. ليست تاريخ تشغيل ERP أو إعادة تأريخ للأرشيف. لا مصادر ويب جديدة أو اتصالات تشغيلية في 7B5.

## ابدأ من هنا — أحدث تسليم 7B5 لا كامل 7B أو 7

| الملف | المحتوى |
|---|---|
|[PHASE-07B5.md](PHASE-07B5.md)|5 نتائج P7-090–094 وشروطها وحدودها ومعالجتها المقترحة؛ 24 توسعة وشواهد مقابلة|
|[SALES-DETAIL-REPORTS-07B5.md](SALES-DETAIL-REPORTS-07B5.md)|مصدر/هوية/وحدة/فلاتر/تحصيل/مجاميع/GL/مخرج؛ 35 صفاً و 22 ثابتاً و 8 عقود|
|[VALIDATION-07B5.md](VALIDATION-07B5.md)|حدود فحص الوثائق و 39 خطة غير منفذة؛ لا قبول ERP|
|[findings.csv](findings.csv)|266 نتيجة مفتوحة قابلة للفرز؛ لا علاج أو إغلاق|
|[review-scope-07B5.csv](review-scope-07B5.csv)|26 مساراً بنطاقات صريحة؛ لا كل caller/template/نشر|
|[مصفوفة 35](evidence/feature-implementation-matrix-07B5.csv) و[ثوابت 22](evidence/report-invariants-07B5.csv)|ربط ثنائي إلى الخطط؛ FE7B5-34/35 حصر مؤجل لا تنفيذ مراجع|
|[عقود 8](evidence/report-reconciliation-07B5.csv)|مصدر/هوية/وحدة/معيار/مجاميع/GL/مخرج وحدود جهل؛ لا مصالحة مالية منفذة|
|[خطط 39](evidence/acceptance-tests-07B5.csv)|10 مباشرة، 24 انحدار أصل، 3 عقود عابرة، 2 بوابة نطاق/إذن؛ not-executed|
|[دفتر 827](evidence/coverage-ledger-07B5.csv) و[فرز 98](evidence/report-candidate-disposition-07B5.csv) و[شاشات 52](evidence/report-screen-disposition-07B5.csv)|محاسبة نطاق ومكملات وفرز مرشحين، لا اكتمال ميزات|
|[توسعات 24](evidence/historical-extensions-07B5.csv)|ذيول evidence دقيقة مع حفظ كل نواة و next_phase لأول 261|
|[handoffs6](evidence/handoffs-07B5.csv) و[questions6](evidence/questions-07B5.csv)|إعادة تصنيف الدفع ونتيجة الحوار والصافي/التحصيل و VATFilter والبناء والموارد وبقية النطاق؛ لا أسرار|
|[backlog10](evidence/continuation-backlog-07B5.csv)|ربط تاريخي بالباقي 7B6/7C؛ لا إغلاق شكلي|
|[witnesses20+20](evidence/report-witnesses-07B5.json)|نماذج يدوية وملاحظات نصية محدودة؛ لا ERP/SQL/WPF/Office|
|[checks7B5](evidence/checks-07B5.json)|ناتج فحص اتساق فعلي للوثائق والبصمات، ليس شهادة مالية أو ERP|
|[provenance178](evidence/provenance-07B5.json) و[لقطة 261](evidence/findings-through-07B4.csv)|حفظ التاريخ وعزل مدخلات B4 دون تعديل ملفاته|
|[PLAN.md](PLAN.md)|المراحل الثماني وتقسيم 7A/B1/B2/B3/B4/B5/B6/C وبوابة 8 غير المأذونة|
|[IMPROVEMENTS.md](IMPROVEMENTS.md)|110 مجموعات تحسين لا نتائج إضافية؛ G-105–110 توصيات 7B5|

### التسليمات التاريخية — محفوظة بأعدادها وحدودها

| المرحلة | التقرير والنموذج والتحقق | أهم الأدلة وقت التسليم |
|---|---|---|
|7B4|[PHASE-07B4](PHASE-07B4.md)، [INVOICE-ANALYSIS-REPORTS-07B4](INVOICE-ANALYSIS-REPORTS-07B4.md)، [VALIDATION-07B4](VALIDATION-07B4.md)|[scope18](review-scope-07B4.csv)، [مصفوفة36](evidence/feature-implementation-matrix-07B4.csv)، [ثوابت22](evidence/report-invariants-07B4.csv)، [عقود8](evidence/report-reconciliation-07B4.csv)، [خطط48](evidence/acceptance-tests-07B4.csv)، [توسعات17](evidence/historical-extensions-07B4.csv)، [backlog10](evidence/continuation-backlog-07B4.csv)، [H7B4](evidence/handoffs-07B4.csv)/[Q7B4](evidence/questions-07B4.csv)، [witnesses23+18](evidence/report-witnesses-07B4.json)، [checks الفعلي](evidence/checks-07B4.json)؛13 جديدة/261 تراكمياً، union334 و493 inventory-only وقت التسليم، لاERP|
|7B3|[PHASE-07B3](PHASE-07B3.md)، [COMMERCIAL-MARINE-REPORTS-07B3](COMMERCIAL-MARINE-REPORTS-07B3.md)، [VALIDATION-07B3](VALIDATION-07B3.md)|[scope27](review-scope-07B3.csv)، [مصفوفة 29](evidence/feature-implementation-matrix-07B3.csv)، [ثوابت 17](evidence/report-invariants-07B3.csv)، [عقود 10](evidence/report-reconciliation-07B3.csv)، [خطط 39](evidence/acceptance-tests-07B3.csv)، [checks الفعلي](evidence/checks-07B3.json)؛ 11 جديدة/248 تراكمياً، 13 توسعة، union326 و 501 inventory-only وقت التسليم؛ 20 نموذجاً و 16 ملاحظة نصية، لا ERP|
|7B2|[PHASE-07B2](PHASE-07B2.md)، [FINANCIAL-INVENTORY-REPORTS-07B2](FINANCIAL-INVENTORY-REPORTS-07B2.md)، [VALIDATION-07B2](VALIDATION-07B2.md)|[scope33](review-scope-07B2.csv)، [مصفوفة 32](evidence/feature-implementation-matrix-07B2.csv)، [ثوابت 18](evidence/report-invariants-07B2.csv)، [عقود 14](evidence/report-reconciliation-07B2.csv)، [قبول 46](evidence/acceptance-tests-07B2.csv)، [دفتر 827](evidence/coverage-ledger-07B2.csv)، [فرز 98](evidence/report-candidate-disposition-07B2.csv)، [توسعات 15](evidence/historical-extensions-07B2.csv)، [backlog10](evidence/continuation-backlog-07B2.csv)، [H7B2](evidence/handoffs-07B2.csv)/[Q7B2](evidence/questions-07B2.csv)، [witnesses22+14](evidence/report-witnesses-07B2.json)، [checks](evidence/checks-07B2.json)؛ 14 جديدة/237 تراكمياً و union306/521 inventory-only وقت التسليم|
|7B1|[PHASE-07B1](PHASE-07B1.md)، [REPORTS-PRINTING-07B1](REPORTS-PRINTING-07B1.md)، [VALIDATION-07B1](VALIDATION-07B1.md)|[scope 42](review-scope-07B1.csv)، [ميزات 33](evidence/feature-implementation-matrix-07B1.csv)، [ثوابت 20](evidence/report-invariants-07B1.csv)، [مصالحة 6](evidence/report-reconciliation-07B1.csv)، [قنوات 11](evidence/output-contracts-07B1.csv)، [قبول 54](evidence/acceptance-tests-07B1.csv)، [دفتر 827](evidence/coverage-ledger-07B1.csv)، [backlog 10](evidence/continuation-backlog-07B1.csv)، [توسعات 7](evidence/historical-extensions-07B1.csv)، [H7B](evidence/handoffs-07B1.csv)/[Q7B](evidence/questions-07B1.csv)، [witnesses 19+11](evidence/report-witnesses-07B1.json)، [checks 7B1](evidence/checks-07B1.json)؛ 23 جديدة/223 تراكمياً، union288 و 539 inventory-only **حينئذ**|
|7A|[PHASE-07](PHASE-07.md)، [FEATURES-HR-PROJECTS-07](FEATURES-HR-PROJECTS-07.md)، [VALIDATION-07](VALIDATION-07.md)|[scope 47](review-scope-07.csv)، [ميزات 36](evidence/feature-implementation-matrix-07.csv)، [أوامر 16](evidence/command-completeness-07.csv)، [ثوابت 25](evidence/feature-invariants-07.csv)، [قبول 64](evidence/acceptance-tests-07.csv)، [دفتر 827](evidence/coverage-ledger-07.csv)، [backlog 10](evidence/continuation-backlog-07.csv)، [توسعات 15](evidence/historical-extensions-07.csv)، [H7](evidence/handoffs-07.csv)/[Q7](evidence/questions-07.csv)، [witnesses 12+8](evidence/feature-witnesses-07.json)، [checks 07](evidence/checks-07.json)؛ 28 جديدة/200 تراكمياً، union266 و 561 inventory-only **حينئذ**|
|6|[PHASE-06](PHASE-06.md)، [INTEGRATIONS-06](INTEGRATIONS-06.md)، [VALIDATION-06](VALIDATION-06.md)|[scope 53](review-scope-06.csv)، [عقود 14](evidence/provider-contracts-06.csv)، [ثوابت 32](evidence/integration-invariants-06.csv)، [حالات 48](evidence/integration-failure-matrix-06.csv)، [قبول 80](evidence/acceptance-tests-06.csv)، [مراجع 15](evidence/official-references-06.csv)، [checks 06](evidence/checks-06.json)؛ 35 جديدة/172 تراكمياً|
|5|[PHASE-05](PHASE-05.md)، [SYNC-OFFLINE-05](SYNC-OFFLINE-05.md)، [VALIDATION-05](VALIDATION-05.md)|[scope 54](review-scope-05.csv)، [تدفقات 18](evidence/sync-flows-05.csv)، [ملكية 12](evidence/sync-data-ownership-05.csv)، [topics 25](evidence/mqtt-topic-contracts-05.csv)، [ثوابت 24](evidence/sync-invariants-05.csv)، [حالات 36](evidence/sync-failure-conflict-05.csv)، [قبول 64](evidence/acceptance-tests-05.csv)، [checks 05](evidence/checks-05.json)؛ 31 جديدة/137 تراكمياً|
|4|[PHASE-04](PHASE-04.md)، [SALES-INVENTORY-04](SALES-INVENTORY-04.md)، [VALIDATION-04](VALIDATION-04.md)|[scope 48](review-scope-04.csv)، [ثوابت 25](evidence/inventory-invariants-04.csv)، [حالات 40](evidence/document-state-effects-04.csv)، [قبول 60](evidence/acceptance-tests-04.csv)، [checks 04](evidence/checks-04.json)؛ 32 جديدة/106 تراكمياً|
|3|[PHASE-03](PHASE-03.md)، [ACCOUNTING-INTEGRITY-03](ACCOUNTING-INTEGRITY-03.md)، [VALIDATION-03](VALIDATION-03.md)|[scope 50](review-scope-03.csv)، [ثوابت 20](evidence/accounting-invariants-03.csv)، [دورات 16](evidence/document-lifecycle-03.csv)، [قبول 35](evidence/acceptance-tests-03.csv)، [checks 03](evidence/checks-03.json)؛ 25 جديدة/74 تراكمياً|
|2|[PHASE-02](PHASE-02.md)، [IDENTITY-AUTHORIZATION-02](IDENTITY-AUTHORIZATION-02.md)، [VALIDATION-02](VALIDATION-02.md)|[scope 60](review-scope-02.csv)، [هوية 12](evidence/identity-flows-02.csv)، [تفويض 21](evidence/authorization-matrix-02.csv)، [SQL 26](evidence/sql-source-sink-02.csv)، [قبول 24](evidence/acceptance-tests-02.csv)، [checks 02](evidence/checks-02.json)؛ 16 جديدة/49 تراكمياً|
|1|[PHASE-01](PHASE-01.md)، [VALIDATION](VALIDATION.md)|[scope 52](review-scope.csv)، [baseline](evidence/baseline.json)، [inventory 827](evidence/inventory.csv)؛ 33 نتيجة وخطط T01–T28 غير المنفذة|

لقطات 49/74/106/137/172/200/223/237/248/261 وبصمات 14/26/38/53/67/86/110/132/155/178 artifacts تحفظ التاريخ. لا مرجع جزئي أو helper بلا caller يثبت امتثالاً أو ينفي خدمة خارجية.
## أولويات معالجة مقترحة — لم تنفذ

1. الهوية والأسرار والتفويض المركزي ودور×فرع×مورد من P1/P2؛ لا تدوير أو حذف عشوائي أو التفاف على حواجز البناء.
2. **P7-090/091:** خدمة إعادة تصنيف دفع/طرف، ونتيجة حوار Selected/Cancelled، وتوفيق InvTotal/Net/PaymentStatus/InvoicePayments/GL، وفترة وإصدار وذرية ونتيجة أمر؛ لا تحديث0 بعد إلغاء أو تحصيل مكرر.
3. **P7-092/083/086/094:** تحصيل جزئي من مبلغ فعلي لا من نوع الدفع، و gross/net وخصم واحد، وضريبة عادية/إضافية مستقلة ومعيار VAT من المصدر نفسه؛ مرجع مالي مستقل لا التقرير نفسه.
4. **P7-093:** صفوف ومجاميع signed ومعايير من snapshot واحدة قبل renderer؛ الجسور ليست null، ولا إصلاح بـ unsigned SUM. تبقى عقود InvoiceTxt/aliases/FreeVATSales/ToDataTable/REPX صريحة.
5. نتائج B1–B4 للتكلفة والوحدة والربح والفترة والإلغاء والفرع والهوية والخيط و partial/CSV تبقى مفتوحة؛ شاهد ضريبي أو GlobalID أو using لا يغلق غيره.
6. بقية HR/PM/البحري والمزامنة والمزودين وعقود Unknown/ACK من P4/P5/P6/P7A؛ لا replay عمياء أو تسوية أرصدة لإرضاء المخرج.
7. استكمل 7B6/7C أو استبعد بسبب وأعلن أجزاء إضافية؛ لا قياس latency/index/leak من قراءة مصدر، ولا 8 أو إصلاحات دون إذن وبيئة مستقلين.

## منهج قراءة السجل

- confirmed قرار/إغفال/تعارض محلي محدد؛ أثره مشروط لا حادث إنتاج. potential سياسة/نشر/تزامن/SDK/قالب/قارئ غير محسوم. repository-gap نقص في اللقطة لا نفي مكون خارجي.
- كل next_phase لأول 261 محفوظة في B5 الجزئية؛ إعادة جدولة P1-014 و P1-032 في 5/6 تاريخ محفوظ لا علاج.
- transaction/PK/GlobalID أو Saved أو SDK200 أو ملف مكتوب لا تثبت المبلغ أو التفويض أو القبول البعيد. فرق header/reloaded amount لا يثبت قيداً غير متوازن.
- **FreeVATSales عمود رأس فعلي** في DDL؛ P7-094 فرق criterion/projection لا خطأ SELECT alias. **GridView حقيقية وصفوف** في P7-093؛ لا default SummaryText أو صفحة مرصودة. ratio0 مخفية في الشبكة لا عمود ظاهر.
- InventoryData و ItemSalesRow و ItemSalesPosRow محلية موجودة؛ لا تخمين InvoiceTxt/DTO/SDK/aliases/نشر/سياسة. مؤشرات الأداء والموارد leads لـ 7C، لا latency أو تسرب مثبتين.
- **كل قبول ERP حتى 7B5 غير منفذ**. النجاح الوثائقي لا يمثل إكمال كل caller/template أو شهادة مالية/أمنية/امتثال.

## إعادة التحقق المحلي الآمن

من جذر المستودع، Python3 stdlib و Git فقط:

```bash
python3 -B docs/audit/tools/collect_baseline.py --verify
python3 -B docs/audit/tools/check_sales_report_witnesses.py
python3 -B docs/audit/tools/test_audit_validator.py
python3 -B docs/audit/tools/test_report_audit_validator.py
python3 -B docs/audit/tools/test_financial_report_audit_validator.py
python3 -B docs/audit/tools/test_commercial_report_audit_validator.py
python3 -B docs/audit/tools/test_invoice_analysis_audit_validator.py
python3 -B docs/audit/tools/test_sales_report_audit_validator.py
python3 -B docs/audit/tools/validate_audit.py
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B4
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B3
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B2
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B1
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part A
```

أجنحة المدقق 10+14+20+18+20 محفوظة و 22 جديدة؛ مجموع 104 حالات اصطناعية فقط. الافتراضي B5 يعزل A/200 و B1/223 و B2/237 و B3/248 و B4/261 بمدخلاتها وفهارسها ثم يفحص 266 الحالية. through-phase2–6 تاريخية. المقاييس الأحدث ليست استنساخ bytes للـ checks المحمية ولا يعاد توليدها. [تفصيل التحقق](VALIDATION-07B5.md).

**لا تستخدم collect_baseline.py --write لإخفاء اختلاف.** تغير HEAD أو الشيفرة لاحقاً يحتاج مرجعاً جديداً وإعادة ربط الأدلة.

## الخطوة التالية

**7B6 ثم 7C ضمن إذن تدقيق 7 القائم** أو أجزاء إضافية معلنة/استبعاد مسند؛ لا اكتمال 7B/7 ولا إذن 8 أو إصلاحات/تشغيل تلقائي. تضاف H7B5/Q7B5 إلى H3/H4/H5/H6/H7/H7B/H7B2/H7B3/H7B4؛ لا طلب أسرار أو بيانات إنتاج.
