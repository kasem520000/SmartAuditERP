# عقود ملكية الصف ونتيجة التكرار — 7B24/R4h

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ الفرع `arena/94ae8414-smartauditerp`؛ دخول B24 بعد دفع B23 المكتمل `f37c37ca6581c4d1546bf0e073326572f4b7af36`، مع678 مادة و319 نتيجة. حقل ساعة البيئة المرصود في freeze هو `2026-11-19T22:54:44.646432+00:00`؛ منفصل عن المرجع المعلن ولا يستبدل تاريخ التقاط محفوظ.

**R4h محدود،7B/7 جزئيتان؛R4i/7B25 مقترح أو split مسبب؛7C لم تبدأ؛8 غير مأذونة هنا.** لا ERP أو إصلاح أو بناء أو C#/VB/.NET/WPF/SQL/Excel/provider/SDK/UtilitiesProj/ToDataTable/REPX أو طابعة/ماسح أو أعمال/أسرار أو قياس أو قبول تشغيلي. `next_phase=8` تخطيط لا إذن. محادثة الإصلاح مستقلة؛ لا يفترض بدءها أو تزامنها ولا يدمج repair→audit هنا.

[النتائج](PHASE-07B24.md) · [العقود والتتبع](ROW-OWNERSHIP-CONTRACTS-07B24.md) · [التحقق والخطط](VALIDATION-07B24.md) · [المتبقي](PHASE-07-REMAINING-07B24.md) · [scope10](review-scope-07B24.csv) · [السجل](findings.csv) · [provenance673](evidence/provenance-07B24.json) · [stdoutB24](evidence/checks-07B24.json)

## 1. القدرة المختارة وحدها

من [SP7B23-01](evidence/split-register-07B23.csv) و[متبقي B23](PHASE-07-REMAINING-07B23.md): ملكية صف PurchInv في picker false/invalid، وهوية هدف wire2، ومرجع حساب wire1 بعد إزالة current أسبق. الافتتاحي والإنتاج مقارنتان محدودتان للحوار، لا مراجعة كاملة للمحرر أو caller/writer أو capability census. [قرار النطاق](evidence/scope-decision-07B24.json) يسجل المدخل والمصدر والمخرج والاستبعادات وحد الخروج؛ الربط في XAML لا يبدأ محاور UX/lifecycle العامة في7C.

الشواهد supplied-input وليست استدعاء للتطبيق: رجوع طبيعي من الحوار ومؤشر مستقر، وlookup موجب نشط وفريد مفترض.149 يثبت هدف الهوية **قبل** hydration، لا أن LoadItemInf بلا أثر.150 يوضح مرجع الحساب بأعداد صحيحة وratio1/noVAT/nodiscount؛40/50 ليس مبلغ حفظ أو قبول ضريبة أو .NET formatting/rounding. GetRowAt يحرس null فلا IndexOutOfRange exception مفترضة. notification ليست حساباً ذاتياً في setter المقروء، لكن لم تراجع كل subscribers أو إعادة حساب لاحقة.

143 عكس labels/wires نفسه في المستهلكين المختارين، و146 مظهر cursor الدفعة نفسه؛ **لا إعادة عد أو historical extensions**. تبقى144/145/147 و142/026 و034/035/136–141 بحدودها، و145/014/132 potential و020/021 وحواجز المال/ACL/stock/save/production مفتوحة. ضابط append في الإنتاج ليس اعتماد BOM أو كاتب أو إعادة فتح. تصويب B10 الإضافي10 مقابل120، وequality1 كلاهما10؛G138 المحمي لم يحرر.

34 شريحة نصية في10 مسارات وثلاثة مستهلكين لا تعني كل11 constructor أو477 body أو callgraph أو حصر455FE. قرئت319 خلاصة عنوان/يقين وصفيت metadata الأدلة آلياً ثم قورنت الأجسام الأقرب المسماة؛ ليست كل319 متناً أو كل مسارات الأدلة يدوياً.10 مسارات/9 تقاطع/1 جديد على418→419؛ المكمل408=343source/61generated/4project-resource، لا نسبة أو408 مهام7C. داخل الاتحاد مقاطع وقدرات باقية أيضاً.

## 2. RO10 — حدود ملكية الصف والحساب

| RO/الحد | المصدر→المخرج | الملاحظة والحد | الجذور/FE |
| --- | --- | --- | --- |
| RO7B24-01 / entry-context | F1/menu→reuse current→picker | existing-current-not-implicit-owned-seed<br>الحكم عند RemoveAt مع رجوع الحوار وفهرس مستقر؛ لا WPF/modal أو حذف محفوظ شوهد. | P7-148 / FE7B24-01 |
| RO7B24-02 / selected-reference | SelectedItem→IndexOf→RowIndex | selected-reference-translated-to-mutable-index<br>wiring محلي لا كل وصول أو ACL أو محور keyboard7C. | P7-148;P7-149 / FE7B24-04 |
| RO7B24-03 / picker-cancel | false result→RemoveAt(current) | in-range-cleanup-without-seed-ownership<br>الحكم عند RemoveAt مع رجوع الحوار وفهرس مستقر؛ لا WPF/modal أو حذف محفوظ شوهد. | P7-148 / FE7B24-01 |
| RO7B24-04 / invalid-confirmation | ISDone/ID<=0→RemoveAt(current) | invalid-result-not-ownership-permission<br>لا تنفيذ ShowDialog/Hide/Close أو قبول كل cancel؛145 potential. | P7-148 / FE7B24-05 |
| RO7B24-05 / last-row-target | wire2→Count−1→FillRowFromDt | unrelated-last-reference-mutated-no-add<br>تكرار واحد كافٍ؛ الإثبات لتعيينات الهوية قبل hydration، لا السياسة السعرية أو السلوك بعد rendering. | P7-149 / FE7B24-02 |
| RO7B24-06 / existing-increment | wire1→quantity++ onfound | existing-reference-mutated-before-removal<br>مثال ratio1/noVAT/nodiscount وأعداد صحيحة؛ old-index قد يرجع null لا exception مفترضاً. | P7-150 / FE7B24-03 |
| RO7B24-07 / index-shift | RemoveAt(current<found)→Calc(oldfound) | old-index-after-removal-not-rebased<br>مثال ratio1/noVAT/nodiscount وأعداد صحيحة؛ old-index قد يرجع null لا exception مفترضاً. | P7-150 / FE7B24-03 |
| RO7B24-08 / out-of-range-control | GetRowAt(oldfound)→null→return | guarded-missed-recalc-not-asserted-exception<br>ضابط محلي للتسلسل لا مصادقة على سياسة merge أو VAT. | P7-150 / FE7B24-06 |
| RO7B24-09 / stored-aggregate | SumPriceDgv→CalcTot | stored-derived-not-line-reconstruction<br>40/50 مثال مسطح لا صحة ضريبية أو قيمة حفظ أو قيد. | P7-150 / FE7B24-10 |
| RO7B24-10 / property-notification | QuantDgv setter→OnPC | notification-not-derived-recalculation<br>ليس حكماً على كل subscriber خارجي؛ لم يرصد rendering أو reentrancy. | P7-150 / FE7B24-11 |

الأدلة والمالك والمدخل المنقح وأثر الغياب والخطوة لكل حد في [RO10 الكامل](evidence/row-ownership-lineage-07B24.csv)، منسوخة بعلاقاتها من القدرة المختارة، لا شهادات تنفيذ مستقلة.

## 3. DO8 — نتائج الحوار والمقارنات

| DO/الحد | المصدر→المخرج | الملاحظة والحد | الجذور/FE |
| --- | --- | --- | --- |
| DO7B24-01 / wire-map | labels→2/1→consumers1/2 | same143-reversal-not-recounted<br>لا تجربة زر مخفي؛ ليست كل11 constructor أو477 body. | P7-143 / FE7B24-13 |
| DO7B24-02 / active-lookup | Code/Name→ID→row-countguard | positive-lookup-assumption-not-SQL-proof<br>لا SQL أو provider أو lookup أو تفرد جرى اختباره. | H7B24-05 / FE7B24-15 |
| DO7B24-03 / purchase-wire2 | duplicate→wire2→lastidentity | target149-independent-of-button-labels143<br>تكرار واحد كافٍ؛ الإثبات لتعيينات الهوية قبل hydration، لا السياسة السعرية أو السلوك بعد rendering. | P7-149 / FE7B24-02 |
| DO7B24-04 / purchase-wire1 | duplicate→wire1→remove→calcoldindex | recalc150-independent-of-last-target149<br>مثال ratio1/noVAT/nodiscount وأعداد صحيحة؛ old-index قد يرجع null لا exception مفترضاً. | P7-150 / FE7B24-03 |
| DO7B24-05 / duplicate-cancel | wire0/3→return | local-no-mutation-not-picker148-or-import144-acceptance<br>لا تجربة زر مخفي؛ ليست كل11 constructor أو477 body. | P7-143 / FE7B24-13 |
| DO7B24-06 / initial-hidden-wire | duplicateaccount→hidequantity2→acceptonly2 | same143-hidden-wire-not-user-click<br>لا تجربة زر مخفي؛ ليست كل11 constructor أو477 body. | P7-143 / FE7B24-13 |
| DO7B24-07 / production-control | wire2→newrowAdd;0/3→CalcTot | new-reference-control-not-production-save-approval<br>020/021/022/133/134 بحدودها؛ لا WPF أو حفظ أو قراءة كامل أمر الإنتاج. | P7-143 / FE7B24-14 |
| DO7B24-08 / batch-and-failure-limits | foreach validcursor/no-match→picker | same146-batch-and-unmodelled-failure-not-new-roots<br>أصناف فريدة ونجاح lookup مفروضان؛ لا كل المحررات أو مجموعة التعداد P7-025. | P7-146 / FE7B24-08 |

[DO8 الكامل](evidence/repeat-outcome-lineage-07B24.csv) لا يفرض معنى تجارياً من الرقم1/2. يميز wire0/3 في الشعبة المحلية عن إلغاء picker148 أو import144؛ وضابط الإنتاج ذو Ref جديدة عن last-row149. نفس143 ونفس146 بلا recount/extension.

## 4. FE18/INV18 — مصدر وحد ومسؤولية وخطتان لكل قدرة

الحالة runtime=not-executed في الجميع؛15 قدرة مصدرية محدودة و3 بوابات وثائقية. الأدلة لكل قدرة أسفلها، و`none-documentary-metadata` للبوابات المعلنة فقط لا مصدر تطبيق مختلق. [FE18](evidence/feature-implementation-matrix-07B24.csv) و[INV18](evidence/report-invariants-07B24.csv) و[36 خطة](evidence/acceptance-tests-07B24.csv) هي الصفوف القابلة للتحقق باتجاهي العلاقات.

### FE7B24-01 — ملكية الصف عند إلغاء بحث الصنف

- **المدخل والتتبع:** F1 أو القائمة→picker false/invalid؛ يمرر المستهلك RowIndex الحالي؛ يحذف فرعا التنظيف أي صف ضمن المدى بلا فحص أنه seed تملكها المحاولة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:133-145;767-808;2293-2299;2378;SmartAuditERP/Form_WPF/frmPurchInv.xaml:1-16;548-581;770-778;SmartAuditERP/Form_WPF/frmItemsSrch.xaml.cs:23-60;442-445;495-499;571-574;SmartAuditERP/Form_WPF/frmItemsSrch.xaml:1-16;206-214`؛ الجذور/الإحالات P7-148.
- **الثابت INV7B24-01:** نتيجة Cancelled/invalid لا تزيل صفاً غير مملوك للمحاولة؛ هوية seed مستقلة عن الفهرس.
- **الحد والحالة:** الحكم عند RemoveAt مع رجوع الحوار وفهرس مستقر؛ لا WPF/modal أو حذف محفوظ شوهد. الحالة confirmed-source-local؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: ملكية الصف عند إلغاء بحث الصنف.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-01;P7B24T-02، غير منفذتين.

### FE7B24-02 — هوية هدف البند المكرر في wire2

- **المدخل والتتبع:** duplicate found→wire2→Count−1→FillRowFromDt؛ لا تنشئ الشعبة صفاً؛ تكتب هوية الصنف في آخر كائن، ولو كان بنداً آخر غير current أو duplicate.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:548-625;628-666;2293-2327;SmartAuditERP/Form_WPF/frmPurchInv.xaml:558-581;591-605;SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:1-57;SmartAuditERP/Form_WPF/MsgExistItem.xaml:59-134;SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:575-594`؛ الجذور/الإحالات P7-149.
- **الثابت INV7B24-02:** تستهدف نتيجة new/replace صفها المعرف صراحة؛ لا Count−1 بديلاً عن LineRef أو OwnedSeed.
- **الحد والحالة:** تكرار واحد كافٍ؛ الإثبات لتعيينات الهوية قبل hydration، لا السياسة السعرية أو السلوك بعد rendering. الحالة confirmed-source-local؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: هوية هدف البند المكرر في wire2.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-03;P7B24T-04، غير منفذتين.

### FE7B24-03 — مرجع الحساب بعد إزالة صف سابق

- **المدخل والتتبع:** wire1→increment found→RemoveAt(current<found)→Calc(oldfound)؛ تزداد كمية كائن existing أولاً ثم يزاح إلى فهرس أقل؛ تستعمل الدالة foundIndex القديم لحساب صف تال أو null.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:300-327;359-457;575-587;2460-2503;SmartAuditERP/Form_WPF/frmPurchInv.xaml:632-734;SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:133-145;767-808;2293-2299;2378;SmartAuditERP/Form_WPF/frmPurchInv.xaml:1-16;548-581;770-778`؛ الجذور/الإحالات P7-150.
- **الثابت INV7B24-03:** يعاد حساب الكائن الذي تغيرت كميته بهويته بعد الإزالة، قبل جمع خلاياه المشتقة.
- **الحد والحالة:** مثال ratio1/noVAT/nodiscount وأعداد صحيحة؛ old-index قد يرجع null لا exception مفترضاً. الحالة confirmed-source-local؛ runtime=not-executed.
- **المالك والمدخل المنقح:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ عقد مصدر كمية وسعر ووحدة البند وأولوية merge/replace والخصم/VAT والتقريب؛ تبقى عقود العملة و HR/BOM/as-of/expiry وpriceUnit السابقة، وأمثلة اصطناعية بلا بيانات أعمال. يخصص لهذه القدرة: مرجع الحساب بعد إزالة صف سابق.
- **أثر الغياب:** لا يقرر مثال 2×10 أو فرق 40/50 سياسة سعر أو ضريبة أو مبلغاً محفوظاً؛ الحقول المشتقة المحلية غير معتمدة مالياً.
- **الخطوة والخطط:** تعيين مصدر الحقول المشتقة وسياسة الحساب بعد تغيير الكمية، مع هوية ثابتة وضوابط مالية مستقلة؛ إبقاء العقود المالية السابقة منسوبة. P7B24T-05;P7B24T-06، غير منفذتين.

### FE7B24-04 — سياق المدخل F1 والقائمة

- **المدخل والتتبع:** KeyDown/contextmenu→addNewItem بلا reset؛ تسمح المداخل بإعادة استعمال current موجود؛ لا يفترض append من اسم addNewItem.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:133-145;767-808;2293-2299;2378;SmartAuditERP/Form_WPF/frmPurchInv.xaml:1-16;548-581;770-778`؛ الجذور/الإحالات P7-148;P7-149.
- **الثابت INV7B24-04:** يعرف كل مدخل AppendContext أو EditContext بمرجع لا يفقد عند فتح البحث.
- **الحد والحالة:** wiring محلي لا كل وصول أو ACL أو محور keyboard7C. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: سياق المدخل F1 والقائمة.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-07;P7B24T-08، غير منفذتين.

### FE7B24-05 — تمييز نتيجة picker عن تنظيف seed

- **المدخل والتتبع:** new picker defaults false/ID−1؛ Close/Escape/Select؛ default false و Close لا يؤكد؛ المستهلك هو الذي يقرر الحذف ولا يختبر ملكية الصف في الفرعين.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:133-145;767-808;2293-2299;2378;SmartAuditERP/Form_WPF/frmPurchInv.xaml:1-16;548-581;770-778;SmartAuditERP/Form_WPF/frmItemsSrch.xaml.cs:23-60;442-445;495-499;571-574;SmartAuditERP/Form_WPF/frmItemsSrch.xaml:1-16;206-214`؛ الجذور/الإحالات P7-148.
- **الثابت INV7B24-05:** نتيجة typed مستقلة للاختيار والإلغاء والفشل، مع مراجعة ملكية أي cleanup.
- **الحد والحالة:** لا تنفيذ ShowDialog/Hide/Close أو قبول كل cancel؛145 potential. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والثقافة والتشغيل و Excel/provider؛ عقد modal return وfailure/no-match/partial/unknown وملكية الإلغاء، وculture/parse/notification/dispatcher؛ تبقى عقود provider/SDK/volumes/موارد السابقة؛ أمثلة اصطناعية فقط. يخصص لهذه القدرة: تمييز نتيجة picker عن تنظيف seed.
- **أثر الغياب:** لا قبول لترتيب أحداث WPF أو إعادة الحساب اللاحقة أو الفشل؛ property notification ليست حساباً مالياً ولا قياس أداء.
- **الخطوة والخطط:** فصل قرار النتيجة عن تنظيف الصف وجدولة الحساب؛ توثيق failure/no-match والجهات المسؤولة دون تشغيل WPF/provider. P7B24T-09;P7B24T-10، غير منفذتين.

### FE7B24-06 — ضابط ترتيب الحذف بالنسبة إلى duplicate

- **المدخل والتتبع:** current>found أو current==found؛ إذا كانت الإزالة بعد existing لا يتغير foundIndex؛ والمساواة تتجاوز RemoveAt.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:300-327;359-457;575-587;2460-2503;SmartAuditERP/Form_WPF/frmPurchInv.xaml:632-734`؛ الجذور/الإحالات P7-150.
- **الثابت INV7B24-06:** اجتياز ترتيب واحد لا يغلق خلل الحساب في ترتيب current<found.
- **الحد والحالة:** ضابط محلي للتسلسل لا مصادقة على سياسة merge أو VAT. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ عقد مصدر كمية وسعر ووحدة البند وأولوية merge/replace والخصم/VAT والتقريب؛ تبقى عقود العملة و HR/BOM/as-of/expiry وpriceUnit السابقة، وأمثلة اصطناعية بلا بيانات أعمال. يخصص لهذه القدرة: ضابط ترتيب الحذف بالنسبة إلى duplicate.
- **أثر الغياب:** لا يقرر مثال 2×10 أو فرق 40/50 سياسة سعر أو ضريبة أو مبلغاً محفوظاً؛ الحقول المشتقة المحلية غير معتمدة مالياً.
- **الخطوة والخطط:** تعيين مصدر الحقول المشتقة وسياسة الحساب بعد تغيير الكمية، مع هوية ثابتة وضوابط مالية مستقلة؛ إبقاء العقود المالية السابقة منسوبة. P7B24T-11;P7B24T-12، غير منفذتين.

### FE7B24-07 — ضابط آخر صف تمهيدي

- **المدخل والتتبع:** btnAddRow→owned trailing seed→wire2؛ إضافة صف فارغ صريحة ثم ملؤه قد تحجب الكتابة فوق lastZ غير المتعلق.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:2089-2095;588-625;SmartAuditERP/Form_WPF/frmPurchInv.xaml:548-581`؛ الجذور/الإحالات P7-149.
- **الثابت INV7B24-07:** يستعمل المستهلك مرجع seed المملوك لا مجرد كونها آخر عناصر القائمة.
- **الحد والحالة:** ضابط هوية قبل hydration لا قبول وحدة أو سعر أو C#/WPF. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: ضابط آخر صف تمهيدي.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-13;P7B24T-14، غير منفذتين.

### FE7B24-08 — دفعة الأصناف مظهر لنفس146

- **المدخل والتتبع:** foreach Itemlist→reuse valid RowIndex→FillRow؛ عند ثبات current صالحاً تملأ الدورات المتعاقبة الصف نفسه؛ ليست finding جديدة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:133-145;767-808;2293-2299;2378;SmartAuditERP/Form_WPF/frmPurchInv.xaml:1-16;548-581;770-778;SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:548-625;628-666;2293-2327;SmartAuditERP/Form_WPF/frmPurchInv.xaml:558-581;591-605`؛ الجذور/الإحالات P7-146.
- **الثابت INV7B24-08:** يظل146 بمعرفه وأدلته القديمة؛ تتبع المظهر لا يعيد عد السبب أو يمدد السجل.
- **الحد والحالة:** أصناف فريدة ونجاح lookup مفروضان؛ لا كل المحررات أو مجموعة التعداد P7-025. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: دفعة الأصناف مظهر لنفس146.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-15;P7B24T-16، غير منفذتين.

### FE7B24-09 — مدخل تحرير الكود أو الاسم

- **المدخل والتتبع:** SelectionChanged→RowIndex؛ CellEditEnding→deferred lookup؛ المعالجان موصولان في XAML؛ يرسل اسم الصف أو رمزه بحثاً عند commit.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:500-625;767-808;2293-2327;SmartAuditERP/Form_WPF/frmPurchInv.xaml:558-581;591-605`؛ الجذور/الإحالات P7-149;P7-150.
- **الثابت INV7B24-09:** تربط نتيجة التحرير بـ LineRef الصف الذي بدأ الطلب لا بتركيز قد يتغير بعد الجدولة.
- **الحد والحالة:** لم يشغل Dispatcher أو يثبت سباق زمني مرصود؛ الثبات مدخل للشواهد. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والثقافة والتشغيل و Excel/provider؛ عقد modal return وfailure/no-match/partial/unknown وملكية الإلغاء، وculture/parse/notification/dispatcher؛ تبقى عقود provider/SDK/volumes/موارد السابقة؛ أمثلة اصطناعية فقط. يخصص لهذه القدرة: مدخل تحرير الكود أو الاسم.
- **أثر الغياب:** لا قبول لترتيب أحداث WPF أو إعادة الحساب اللاحقة أو الفشل؛ property notification ليست حساباً مالياً ولا قياس أداء.
- **الخطوة والخطط:** فصل قرار النتيجة عن تنظيف الصف وجدولة الحساب؛ توثيق failure/no-match والجهات المسؤولة دون تشغيل WPF/provider. P7B24T-17;P7B24T-18، غير منفذتين.

### FE7B24-10 — جمع الخلايا المشتقة بعد الحساب

- **المدخل والتتبع:** QuantDgv→CalcRowValues→SumPriceDgv→CalcTot؛ يجمع CalcTot خلايا SumPriceDgv وغيرها؛ لا يعيد بناء كل بند من qty×price عند الجمع.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:300-327;359-457;575-587;2460-2503;SmartAuditERP/Form_WPF/frmPurchInv.xaml:632-734`؛ الجذور/الإحالات P7-150.
- **الثابت INV7B24-10:** تعتمد المجاميع على قيم مشتقة حديثة لذات LineRef، لا كمية محدثة ومجموع قديم.
- **الحد والحالة:** 40/50 مثال مسطح لا صحة ضريبية أو قيمة حفظ أو قيد. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ عقد مصدر كمية وسعر ووحدة البند وأولوية merge/replace والخصم/VAT والتقريب؛ تبقى عقود العملة و HR/BOM/as-of/expiry وpriceUnit السابقة، وأمثلة اصطناعية بلا بيانات أعمال. يخصص لهذه القدرة: جمع الخلايا المشتقة بعد الحساب.
- **أثر الغياب:** لا يقرر مثال 2×10 أو فرق 40/50 سياسة سعر أو ضريبة أو مبلغاً محفوظاً؛ الحقول المشتقة المحلية غير معتمدة مالياً.
- **الخطوة والخطط:** تعيين مصدر الحقول المشتقة وسياسة الحساب بعد تغيير الكمية، مع هوية ثابتة وضوابط مالية مستقلة؛ إبقاء العقود المالية السابقة منسوبة. P7B24T-19;P7B24T-20، غير منفذتين.

### FE7B24-11 — إشعار الخاصية ليس بديلاً عن الحساب

- **المدخل والتتبع:** PurchInvRow.QuantDgv setter→OnPC فقط؛ يرفع setter إشعار PropertyChanged ولا ينادي CalcRowValues أو يشتق SumPrice بذاته.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:359-457;2460-2503;SmartAuditERP/Form_WPF/frmPurchInv.xaml:632-734`؛ الجذور/الإحالات P7-150.
- **الثابت INV7B24-11:** يفصل العقد notification عن الحساب الصريح ويربط الحساب بتغير كمية ذات الصف.
- **الحد والحالة:** ليس حكماً على كل subscriber خارجي؛ لم يرصد rendering أو reentrancy. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والثقافة والتشغيل و Excel/provider؛ عقد modal return وfailure/no-match/partial/unknown وملكية الإلغاء، وculture/parse/notification/dispatcher؛ تبقى عقود provider/SDK/volumes/موارد السابقة؛ أمثلة اصطناعية فقط. يخصص لهذه القدرة: إشعار الخاصية ليس بديلاً عن الحساب.
- **أثر الغياب:** لا قبول لترتيب أحداث WPF أو إعادة الحساب اللاحقة أو الفشل؛ property notification ليست حساباً مالياً ولا قياس أداء.
- **الخطوة والخطط:** فصل قرار النتيجة عن تنظيف الصف وجدولة الحساب؛ توثيق failure/no-match والجهات المسؤولة دون تشغيل WPF/provider. P7B24T-21;P7B24T-22، غير منفذتين.

### FE7B24-12 — الحذف الصريح له تأكيد ومرجع

- **المدخل والتتبع:** Delete button.Tag→row→prompt→Remove(row)؛ يسأل مسار الحذف الصريح ويمسك row، بخلاف cleanup الإلغاء الذي يستخدم فهرساً فقط.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:791-808;2329-2342;SmartAuditERP/Form_WPF/frmPurchInv.xaml:748-778`؛ الجذور/الإحالات P7-148.
- **الثابت INV7B24-12:** Cancel ليس دليلاً على طلب Delete؛ عقد الأمر وملكية الصف مستقلان.
- **الحد والحالة:** مقارنة مصدرية لا فرض واجهة تأكيد جديدة أو قبول ACL. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: الحذف الصريح له تأكيد ومرجع.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-23;P7B24T-24، غير منفذتين.

### FE7B24-13 — نفس143 في ثلاثة مستهلكين

- **المدخل والتتبع:** quantity button→2/new button→1؛ consumers1/2؛ PurchInv و Production يفسران1 زيادةً و2 جديداً؛ الافتتاحي يخفي زر2 ويقبل2 فقط للتكرار.
- **الدليل:** `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:1-57;SmartAuditERP/Form_WPF/MsgExistItem.xaml:59-134;SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:575-594;SmartAuditERP/Form_WPF/FrmIntialRestraiction.xaml.cs:509-574;609-612;SmartAuditERP/Form_WPF/FrmIntialRestraiction.xaml:1-16;393-420;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:122-126;1130-1265;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:1-16;443-500`؛ الجذور/الإحالات P7-143.
- **الثابت INV7B24-13:** العكس والزر المخفي مظهران لنفس اتفاق143؛ لا finding أو extension جديدة.
- **الحد والحالة:** لا تجربة زر مخفي؛ ليست كل11 constructor أو477 body. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: نفس143 في ثلاثة مستهلكين.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-25;P7B24T-26، غير منفذتين.

### FE7B24-14 — ضابط إضافة صف إنتاج بمرجع جديد

- **المدخل والتتبع:** production duplicate wire2→AppendItemRow→Add(newRow)؛ يعرف الفرع كائناً جديداً ويلحقه؛ wire0/3 لا يعدلان البنود في الشعبة المقروءة قبل CalcTot.
- **الدليل:** `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:122-126;1130-1265;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:1-16;443-500`؛ الجذور/الإحالات P7-143.
- **الثابت INV7B24-14:** ضابط الهوية لا يرفع حواجز كاتب production أو وحدة BOM أو إعادة الفتح.
- **الحد والحالة:** 020/021/022/133/134 بحدودها؛ لا WPF أو حفظ أو قراءة كامل أمر الإنتاج. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والمنتج ومحرر الفاتورة وعقد الصف؛ عقد OwnedSeed/LineRef وCurrentRow مقابل AppendContext، وSelected/Merged/New/Cancelled/Failed وRepeatOutcome؛ متى يجوز حذف صف أو استبداله وكيف تحفظ الهوية بعد RemoveAt. تبقى supportmatrix و DocumentRef/allowed-set/branch/reset/basket/legacy/Wscale3 السابقة. يخصص لهذه القدرة: ضابط إضافة صف إنتاج بمرجع جديد.
- **أثر الغياب:** لا يجوز استنتاج ملكية صف من فهرسه أو أنه آخر عنصر؛ قبول merge/new/cancel وبقية المداخل يبقى محجوباً، و145 potential.
- **الخطوة والخطط:** حسم OwnedSeed وLineRef وOutcome؛ تتبع كل إزالة وكتابة وحساب إلى الصف المقصود، وبقية SP01 بنطاق مستقل. P7B24T-27;P7B24T-28، غير منفذتين.

### FE7B24-15 — حدود النجاح و no-match والصحة

- **المدخل والتتبع:** active query→row-count guard→picker عند غياب النتيجة؛ النتائج الإيجابية والتفرد والرجوع الطبيعي مدخلات؛ no-match قد يعيد picker ولا يمثله نموذج النجاح.
- **الدليل:** `SmartAuditERP/Form_WPF/frmPurchInv.xaml.cs:500-625;767-808;2293-2327`؛ الجذور/الإحالات H7B24-05.
- **الثابت INV7B24-15:** لكل Failed/unknown/no-match نتيجة وهوية؛ لا يفسر غياب الشاهد كـ no-op مقبول.
- **الحد والحالة:** لا SQL أو provider أو lookup أو تفرد جرى اختباره. الحالة bounded-source-contract-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك WPF والثقافة والتشغيل و Excel/provider؛ عقد modal return وfailure/no-match/partial/unknown وملكية الإلغاء، وculture/parse/notification/dispatcher؛ تبقى عقود provider/SDK/volumes/موارد السابقة؛ أمثلة اصطناعية فقط. يخصص لهذه القدرة: حدود النجاح و no-match والصحة.
- **أثر الغياب:** لا قبول لترتيب أحداث WPF أو إعادة الحساب اللاحقة أو الفشل؛ property notification ليست حساباً مالياً ولا قياس أداء.
- **الخطوة والخطط:** فصل قرار النتيجة عن تنظيف الصف وجدولة الحساب؛ توثيق failure/no-match والجهات المسؤولة دون تشغيل WPF/provider. P7B24T-29;P7B24T-30، غير منفذتين.

### FE7B24-16 — حواجز المال والأمان والإذن

- **المدخل والتتبع:** gate before acceptance؛ Python والصف المحلي لا يختبران المخطط والمنح و save/stock؛ next_phase8 تخطيط.
- **الدليل:** `none-documentary-metadata`؛ الجذور/الإحالات P4-014;P7-132;P7-145;P4-020;P4-021.
- **الثابت INV7B24-16:** تبقى014/132/145 potential و020/021 والحواجز والتاريخ دون ترقية أو إذن ضمني.
- **الحد والحالة:** بوابة وثائقية؛ لا مرجع مالي اختبر أو ERP نفذ. الحالة gate-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** DBA ومالك الأمان و AuditorAPI؛ schema/migrations/grants/constraints وتفرد Code/ItemId وbranch وwire/enum بإصداراتها وبصماتها وأدوار×أوامر×موارد؛ لا credentials أو اتصال أو قبول save/stock. يخصص لهذه القدرة: حواجز المال والأمان والإذن.
- **أثر الغياب:** نجاح lookup مفترض لا يثبت مخطط النشر أو المنح أو تفويض حفظ/مخزون؛014/132 potential و 020/021 باقية.
- **الخطوة والخطط:** مقارنة القاموس والمنح وتعريفات wire/enum قبل أي قبول مأذون لاحق، دون اتصال أو تشغيل أو تغيير تصنيف الحواجز. P7B24T-31;P7B24T-32، غير منفذتين.

### FE7B24-17 — نسب البقايا والحصر المتفق

- **المدخل والتتبع:** RS14/SP01–03؛ تقدم RO10/DO8 لا يستبدل أي required-input أو route قديم؛ ثلاثة مستهلكين ليست حصر قدرات.
- **الدليل:** `none-documentary-metadata`؛ الجذور/الإحالات H7B24-06.
- **الثابت INV7B24-17:** كل upstream ID/artifact/rowSHA/contract/input/route/disposition محفوظ؛7B جزئية و7C لم تبدأ.
- **الحد والحالة:** بوابة وثائقية وليست14 موافقة خارجية. الحالة gate-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك نطاق التدقيق والمنتج والتوثيق؛ حصر قدرات ومداخل ومصادر ومخارج متفق عليه و crosswalk455FE/NV22/BC7/WC12/EN8/UP8/SB8/IM8/RO10/DO8، وسبب كل split أو استبعاد وحد الخروج؛ وآخر SHA تدقيق راجعته محادثة الإصلاح المستقلة. يخصص لهذه القدرة: نسب البقايا والحصر المتفق.
- **أثر الغياب:** ثلاثة مستهلكين و 34 شريحة و 10 مسارات ليست كل 11 construction أو 477 body أو حصر 455FE أو نسبة؛ لا يفترض بدء محادثة الإصلاح أو تزامنها.
- **الخطوة والخطط:** اختيار R4i/7B25 المقترح أو split مسبب من SP01–03 بمدخل ومصدر ومخرج وحد خروج؛ تسليم SHA التدقيق إلى المحادثة الموازية بحفظ تاريخها وتعديلات الإصلاح. P7B24T-33;P7B24T-34، غير منفذتين.

### FE7B24-18 — حفظ OWN319 والتوازي

- **المدخل والتتبع:** OWN B23/44 and actual current CLI B24؛ separate repairs؛ التاريخ بمدخل319/raw320CRLF/indexes ومجموعة44 الأصلية؛ CLI B24 الحالي يختبر مستقلاً.
- **الدليل:** `none-documentary-metadata`؛ الجذور/الإحالات H7B24-06.
- **الثابت INV7B24-18:** 673 مادة محمية وكل حقول319 و rawprefix/G210/827 وثلاثة freezes محفوظة؛ لا إصلاح تلقائي أو repair→audit merge.
- **الحد والحالة:** بوابة وثائقية لا تفترض بدء المحادثة الموازية أو تزامنها. الحالة gate-open؛ runtime=not-executed.
- **المالك والمدخل المنقح:** مالك نطاق التدقيق والمنتج والتوثيق؛ حصر قدرات ومداخل ومصادر ومخارج متفق عليه و crosswalk455FE/NV22/BC7/WC12/EN8/UP8/SB8/IM8/RO10/DO8، وسبب كل split أو استبعاد وحد الخروج؛ وآخر SHA تدقيق راجعته محادثة الإصلاح المستقلة. يخصص لهذه القدرة: حفظ OWN319 والتوازي.
- **أثر الغياب:** ثلاثة مستهلكين و 34 شريحة و 10 مسارات ليست كل 11 construction أو 477 body أو حصر 455FE أو نسبة؛ لا يفترض بدء محادثة الإصلاح أو تزامنها.
- **الخطوة والخطط:** اختيار R4i/7B25 المقترح أو split مسبب من SP01–03 بمدخل ومصدر ومخرج وحد خروج؛ تسليم SHA التدقيق إلى المحادثة الموازية بحفظ تاريخها وتعديلات الإصلاح. P7B24T-35;P7B24T-36، غير منفذتين.

## 5. RC6 وAD10 والحواجز

| RC/العقد | FE | قاعدة المصالحة | حد الحكم |
| --- | --- | --- | --- |
| RC7B24-01 / أسباب ملكية الصف والهدف والحساب | FE7B24-01;FE7B24-02;FE7B24-03 | نتيجة Cancelled/invalid لا تزيل صفاً غير مملوك للمحاولة؛ هوية seed مستقلة عن الفهرس.؛ تستهدف نتيجة new/replace صفها المعرف صراحة؛ لا Count−1 بديلاً عن LineRef أو OwnedSeed.؛ يعاد حساب الكائن الذي تغيرت كميته بهويته بعد الإزالة، قبل جمع خلاياه المشتقة. | مصالحة تتبع مصدرية لا ERP أو قبول مالي؛ حدود كل قدرة وأصل وخطة محفوظة كما هي. |
| RC7B24-02 / المداخل والنتيجة وضوابط ترتيب الحذف | FE7B24-04;FE7B24-05;FE7B24-06 | يعرف كل مدخل AppendContext أو EditContext بمرجع لا يفقد عند فتح البحث.؛ نتيجة typed مستقلة للاختيار والإلغاء والفشل، مع مراجعة ملكية أي cleanup.؛ اجتياز ترتيب واحد لا يغلق خلل الحساب في ترتيب current<found. | مصالحة تتبع مصدرية لا ERP أو قبول مالي؛ حدود كل قدرة وأصل وخطة محفوظة كما هي. |
| RC7B24-03 / seed والدفعة والتحرير | FE7B24-07;FE7B24-08;FE7B24-09 | يستعمل المستهلك مرجع seed المملوك لا مجرد كونها آخر عناصر القائمة.؛ يظل146 بمعرفه وأدلته القديمة؛ تتبع المظهر لا يعيد عد السبب أو يمدد السجل.؛ تربط نتيجة التحرير بـ LineRef الصف الذي بدأ الطلب لا بتركيز قد يتغير بعد الجدولة. | مصالحة تتبع مصدرية لا ERP أو قبول مالي؛ حدود كل قدرة وأصل وخطة محفوظة كما هي. |
| RC7B24-04 / المشتقات والإشعار والحذف الصريح | FE7B24-10;FE7B24-11;FE7B24-12 | تعتمد المجاميع على قيم مشتقة حديثة لذات LineRef، لا كمية محدثة ومجموع قديم.؛ يفصل العقد notification عن الحساب الصريح ويربط الحساب بتغير كمية ذات الصف.؛ Cancel ليس دليلاً على طلب Delete؛ عقد الأمر وملكية الصف مستقلان. | مصالحة تتبع مصدرية لا ERP أو قبول مالي؛ حدود كل قدرة وأصل وخطة محفوظة كما هي. |
| RC7B24-05 / التكرار والضابط وحدود الفشل | FE7B24-13;FE7B24-14;FE7B24-15 | العكس والزر المخفي مظهران لنفس اتفاق143؛ لا finding أو extension جديدة.؛ ضابط الهوية لا يرفع حواجز كاتب production أو وحدة BOM أو إعادة الفتح.؛ لكل Failed/unknown/no-match نتيجة وهوية؛ لا يفسر غياب الشاهد كـ no-op مقبول. | مصالحة تتبع مصدرية لا ERP أو قبول مالي؛ حدود كل قدرة وأصل وخطة محفوظة كما هي. |
| RC7B24-06 / الحواجز والبقايا والتاريخ والتوازي | FE7B24-16;FE7B24-17;FE7B24-18 | تبقى014/132/145 potential و020/021 والحواجز والتاريخ دون ترقية أو إذن ضمني.؛ كل upstream ID/artifact/rowSHA/contract/input/route/disposition محفوظ؛7B جزئية و7C لم تبدأ.؛ 673 مادة محمية وكل حقول319 و rawprefix/G210/827 وثلاثة freezes محفوظة؛ لا إصلاح تلقائي أو repair→audit merge. | مصالحة تتبع مصدرية لا ERP أو قبول مالي؛ حدود كل قدرة وأصل وخطة محفوظة كما هي. |

[RC6](evidence/report-reconciliation-07B24.csv) يربط FE/roots/plans والأدلة نفسها بلا مصدر إضافي مفترض. [AD10](evidence/root-adjudication-07B24.csv) يقارن148–150 بالأقرب ويفصل143/146 وبوابة التاريخ؛ [extensions0](evidence/historical-extensions-07B24.csv) صفر. المراجعة على مستوى العقد والحد المحلي لا كل مسار حفظ أو قياس أو صحة المال.

حفظ673 مادة محمية وكل319 قاموساً بكل حقل وALLnext_phase/evidence/raw320CRLFprefix/noBOM وG01–210 و827 أصلاً/29,128,444 بايت وثلاثة freezes.322 مفتوحة بلا معالجة:2Critical/181High/138Medium/1Low؛283confirmed/32potential/7repository-gap؛ المرحلة7=150.148–150 وحدها إضافات هذا الجزء، وG211–215 توصيات لا findings إضافية.

694 حالة مدقق وثائق في25 مجموعة =650 سابقة محفوظة +44 جديدة، وليست ERP.29 وضعية تاريخية OWN نفذت فعلياً بأدوات التقاطها المعلنة، لا ادعاء إعادة29 بعد تثبيت SHA/النثر/push. B23 بمدخل319/raw320CRLF/indexes وALL44 الأصلية في child presetB23 مع A محلي؛B22/40,B21/36,B20/32,B19/36,B18/28 باقية. لا تحرير/skip/rebaseline/global Path أو shared subprocess mutation أو disk overlay أو إعادة stdout. actual CLI B24/API main B15 مختلفان عمداً.

[RS14](evidence/residual-disposition-07B24.csv) و[SP3](evidence/split-register-07B24.csv) و[H6](evidence/handoffs-07B24.csv)/[Q6](evidence/questions-07B24.csv) تحفظ بقايا العقود والمدخلات والهوية. لكل بقية ancestry وcontract وrowSHA ومدخل سابق كامل وكل mapped route وتصرف لا يتبدل إلى approved. R4i/7B25 مقترح أو split مسبب؛7B/7 جزئيتان،7C لم تبدأ و8 غير مأذونة هنا. مسار الإصلاح مستقل، لا مزامنة أو معالجة مفترضة.
