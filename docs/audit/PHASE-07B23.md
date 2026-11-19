# الجزء 7B23/R4g — عضوية اختيار الأصناف ودفعات البنود وترطيب الاستيراد

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711` والفرع `arena/94ae8414-smartauditerp`. دخول B23 بعد دفع B22 المكتمل `3276579931925bff37bbf45c5b43efb7fbcd0118` بجميع **648 مادة تدقيق**. ساعة البيئة المرصودة `2026-11-19T22:04:00.405782+00:00` منفصلة عن المرجع المعلن؛ ليست تاريخ تشغيل أو قبول.

**R4g محدود بشريحة SP01، لا كل R4 أو 7B؛ 7B/7 جزئيتان؛ R4h/7B24 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا ERP أو بناء أو C#/VB/.NET/WPF/SQL/Excel/provider/SDK/UtilitiesProj/ToDataTable/REPX أو ماسح/طابعة أو بيانات أعمال أو أسرار أو إصلاح أو قياس أو قبول هنا. `next_phase=8` تخطيط لا إذن. المحادثة الموازية للإصلاح مستقلة؛ لا نفترض أنها بدأت أو تزامنت، ولا ندمج إصلاحاتها في هذا الفرع.

[النتائج](PHASE-07B23.md) · [العقود والتتبع](ITEM-INGRESS-CONTRACTS-07B23.md) · [التحقق والخطط](VALIDATION-07B23.md) · [المتبقي](PHASE-07-REMAINING-07B23.md) · [scope12](review-scope-07B23.csv) · [السجل](findings.csv) · [provenance643](evidence/provenance-07B23.json) · [stdoutB23](evidence/checks-07B23.json)

## قرار الشريحة وحد الخروج

السلطة هي [متبقي B22](PHASE-07-REMAINING-07B22.md) و[SP7B22-01](evidence/split-register-07B22.csv) وبقاياه [RS14](evidence/residual-disposition-07B22.csv). اختيرت القدرة **picker SelectedItems→Itemlist→دفعة محلية في المحرر→seed صف الاستيراد→بند مرطّب في الذاكرة**. لم يختر هذا الجزء كل مستهلكي الحوار أو الاستيراد، أو كل بديهيات تسعير الفاتورة ودورة حفظها.

- **المدخل:** event wiring منتقى و F1/menu ومثال report→editor حرفي، ثم ISDone/ItemId>0 أو dtInvSel غير فارغ. نجـاح Code/ID النشط والفريد وعودة التحميل الطبيعية مدخلات مفترضة؛ ليست جلسة WPF أو SQL مرصودة.
- **المصدر:** مجموعة SelectedItems و Itemlist المحلية وخمس خلايا wizard، وهوية seed وكائن البند الجديد وتعليمات defaults. لا ملفات Excel أو تعريف enum أو عقد تحويل مستخرج من DLL.
- **المخرج:** عضوية النتيجة، وبقاء بنود الدفعة، ثم description/unit/quantity/price عند حد hydration في الذاكرة. لا save أو GL أو stock أو مبلغ مطبوع أو خسارة مالية شوهدت.
- **الخروج المحلي:** لكل قدرة مختارة دليل وحد ومالك ومدخل منقح وأثر وخطوة وخطتان غير منفذتين، مع قرار جذور مستقل ونسب كل 14 بقية و SP01–03. هذا خروج الشريحة لا موافقة العقود الخارجية أو إغلاق 7B.
- **النطاق:**12 مساراً بشرائح،10 قديمة و 2 جديدة على اتحاد 416 فيصبح 418؛ المكمل 409=344source/61generated/4project-resource. الجديد `frmItemsSrch.xaml` و`frmInvSumByType.xaml` ربط محلي لا بدء UX/lifecycle7C. داخل 418 أيضاً أجسام ومقاطع وقدرات غير مستكملة.

## النتائج الجديدة — أسباب مستقلة لا إصلاحات

### P7-145 — قائمة نتائج البحث تتراكم دون إزالة ما ألغي تحديده مع عقد اختيار نهائي غير محسوم

**الخطورة:** Medium؛ **الإثبات:** potential؛ **الحالة:** open-not-remediated.

**الدليل:** `SmartAuditERP/Form_WPF/frmItemsSrch.xaml.cs:294-338`؛ `SmartAuditERP/Form_WPF/frmItemsSrch.xaml:596-614`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:1495-1502`؛ `SmartAuditERP/Form_WPF/frmSalePurch.xaml.cs:796-807`.

**السلسلة:** GridControl1 يعلن Extended/full-row ويربط SelectionChanged. المعالج يمر على SelectedItems الحالية ويضيف كل ID موجب غير موجود في Itemlist، ولا يزيل عضواً أُلغي تحديده. عند التأكيد تحذف SelectCurrentItem المعرّف الحالي وحده ثم تعيد إضافته وتضع ISDone/ItemId؛ لا تعيد بناء كل النتيجة من الاختيار الحالي. المستهلكان المختاران يقرآن Itemlist بعد حارس التأكيد.

**الشاهد والشرط:** نموذج اصطناعي حدّد A ثم غيّر التحديد إلى B فقط. تصبح المجموعة الحالية[B] لكن النتيجة المتراكمة[A,B]؛ إزالة عضو من مجموعة[A,B] لا يمحو تاريخه أيضاً. اختيار واحد مستقر لا يظهر الفرق، و ISDone=false يمنع استهلاك الدفعة في الحارسين المحددين. لم ينفذ click أو ترتيب أحداث أو modal أو حفظ.

**لماذا potential؟** تراكم IDs مثبت بالتعليمات، لكن لم يورد عقد يقول هل هذه نافذة اختيار نهائي أم سلة تراكمية مقصودة. في عقد الاختيار النهائي قد يعود صنف ألغى المستخدم تحديده؛ وفي عقد basket يحتاج المنتج تمثيلاً وإزالة متفقاً عليهما. لا نحول غياب مواصفة السلة إلى ميزة واجبة أو عيب مؤكّد. قراءة wiring هنا ليست بداية محور UX العام في 7C.

**الأثر المحدود والتفاعل:** الدليل على اختلاف العضوية عند حد Result، لا على أن كل فاتورة ستحتفظ بـ A. قد يخفي استبدال البند في 146 بعض العضوية السابقة بمحرر المبيعات، بينما ضابط seed في المحرر الآخر يبقي بنود الدفعة الفريدة. لا تجمع الآثار الثلاثة في سيناريو حفظ مفترض واحد.

**المقترح غير المنفذ:** حسم final-selection/basket أولاً، ثم نتيجة SelectedIDs بهوية وعضوية وإزالة صريحة متطابقة مع العقد. H7B23-03 و P7B23T-01/02 غير منفذتين. P2-004 تخص تراكم منح موظف عند تغيير المستخدم، و P4-013 هوية سطر حوار الجزء، و 032 نموذج عقد آخر؛ ليست هذه الحالة إعادة عد لها.

### P7-146 — إضافة دفعة أصناف متميزة تستبدل البند السابق في محرر المبيعات بدلاً من إلحاقها

**الخطورة:** Medium؛ **الإثبات:** confirmed من المصدر المحلي بشروط المدخل المختار؛ **الحالة:** open-not-remediated.

**الدليل:** `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:183-203`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:1393-1510`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:2473-2477`.

**السلسلة:** يضع F1 و StripItemSearch المؤشر RowIndex=Count قبل AddNewItem. تتكرر الدفعة على frm.Itemlist؛ بعد كل SearchByID يترك caller المؤشر Count−1. فرع صنف متميز غير موجود لا يفتح MsgExistItem، لكنه يحذف أي row حالية إذا RowIndex<Count بلا شرط أنها seed فارغة، ثم يضيف row الجديدة. بعد الإضافة الأولى صار المؤشر هو البند الذي أضيف لتوه، فتزيله الدورة التالية الناجحة.

**المثال:** prefix[X] ودفعة فريدة[A,B]، وكل lookup ناجح ويرجع طبيعياً. الأولى تنتج[X,A] وتترك المؤشر على A؛ الثانية تزيل A ثم تلحق B فيبقى[X,B]. ومع prefix فارغ ودفعة A/B/C يبقى الأخير في النموذج. النتيجة محلية عند تعليمات الإضافة، لا كمية أو مبلغ محفوظ.

**الحد والشاهد:** صنف واحد لا يحتاج التكرار التالي، و ISDone=false لا ينفذ الحلقة. في `SmartAuditERP/Form_WPF/frmSalePurch.xaml.cs:780-813` يضيف caller seed فارغة لكل تكرار؛ وفي `SmartAuditERP/Form_WPF/frmSalePurch.xaml.cs:436-501` يحذف loader فقط ذات ItemId<=0. هذا control مختلف، لا إعلان صحة كل المشتريات أو كل مسار فشل أو تكرار. افترضت النماذج نجاح التحميل والرجوع ومؤشراً مستقراً عند الحد الموثق؛ لا WPF reentrancy أو عرض/حفظ شوهد.

**منع التكرار:** السبب لا يحتاج صنفاً مكرراً أو الحوار 143، ولا تعديل مجموعة Itemlist أثناء تعدادها كما P7-025؛ المجموعة المعدلة هنا هي صفوف الفاتورة، وقائمة for-each منفصلة. ليس اختيار جزء من الفاتورة بهوية ItemId في P4-013.

**المقترح غير المنفذ:** AppendContext/LineRef صريح لكل دورة، وفصل append عن replace المقصود؛ لا حذف لمجرد أن المؤشر ضمن Count. يقبل الإصلاح المستقبلي دفعة فريدة تحفظ prefix وكل IDs الناجحة، مع نتيجة لكل failed/cancelled وفق عقد منفصل. H7B23-03 و P7B23T-03/04 غير منفذتين.

### P7-147 — استيراد الفواتير يفقد قيم الصف أثناء استبداله ببند جديد في المحررين المختارين

**الخطورة:** Medium؛ **الإثبات:** confirmed لتدمير seed قبل hydration في المحررين المحددين بشروطه؛ **الحالة:** open-not-remediated.

**الدليل:** `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:2636-2681`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:1364-1385`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:1451-1471`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:1514-1640`؛ `SmartAuditERP/Form_WPF/frmSalePurch.xaml.cs:2347-2384`؛ `SmartAuditERP/Form_WPF/frmSalePurch.xaml.cs:408-619`؛ `SmartAuditERP/Form_WPF/frmSalesInvoice.xaml.cs:3048-3100`؛ `SmartAuditERP/Form_WPF/frmSalePurch.xaml.cs:2800-2845`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:996-1057`.

**السلسلة:** منتج wizard يكوّن ItemCode/description/unit/quntity/price بعد حارس Code ويضع ISDone. كل مستورد يملأ seed بـ Description و UnitName من unit و Quantity، وبالسعر إذا كان موجباً، ثم يلحقها ويستدعي SearchByCode. عند مطابقة Code يستدعي SearchByID(0). المبيعات يحذف row المؤشر، والمشتريات يحذف row ذات ItemId0؛ وهذه هي seed التي أنشأها المستورد. يبني كل منهما row جديدة لا تنسخ حقول seed؛ يبدأ description empty، ثم تختار LoadItemInf/LoadUnitInf الوحدة/السعر الافتراضيين وتضبط Quantity=1 في المسار المحدد. لا يستعيد المستورد الحقول بعد عودة SearchByCode في المقطعين.

**الشاهد المحدود:** seed اصطناعية A/description=import-A/unit=PACK/quantity7/positivePrice50، و quote افتراضية موردة EACH/20، معصنف فريد ناجح و rdAuto off. النموذج عند حد hydration يصبح description فارغاً ووحدة EACH وكمية 1 وسعر quote20.20 و 50 ليستا أسعاراً صحيحة مقررة، و PACK ليست وحدة واجبة؛ النتيجة تثبت عدم نقل القيم المعبأة لا أولوية مالية معتمدة. قد تغير عروض أو تدخلات لاحقة السعر أو الكمية؛ لم يراجع كامل المحرر أو يرصد صافي حفظه. لا يخفي ذلك أن كائن seed المعبأ قد حُذف بلا copy في الحد المختار.

**الشواهد والحدود:** إذا ساوت الحقول defaults قد لا يظهر فرق بالقيم، لكنه لا يثبت سلامة النقل. فشل lookup أو no-match ليسا نموذجاً لتطبيق 147؛ قد يفتح picker أو يحدث خطأ أو يبقى أثر آخر، ولذلك خانة False تعني أن هذا الفرع خارج النموذج، لا إثبات أنه noop صحيح. rdAuto on والحاسبة و settingsQTY عقد منفصل. صحة Common.GetUnitName وثقافة parse والتفرد والمنح و schema لم تعتمد؛ نجاح هذه المدخلات افتراض للشاهد فقط.

**الفصل عن 144 و 143 و 142/026:** لا تكرار هنا ولا قرار merge/cancel ولا شرط آخر index لإسقاط القيم.144 تخص void ثم code+Count في مستورد العقد الذي يطبّق القيم *بعد* loader؛147 تفقد seed *قبل* hydration في محررين آخرين، حتى مع أول صنف فريد.143 عكس زر التكرار مستقل، و 026/142 تسعير/هوية وحدة لا يفسران فقد الوصف والكمية بسبب تبديل الكائن. PM013 إعادة فتح صافي/تكلفة نموذج آخر، لا هذا الحد.

**المقترح غير المنفذ:** مرر ImportSeed/SourceRowRef و UnitId والقيم المقبولة إلى نتيجة HydratedLine بهوية ومصدر لكل حقل؛ إما preserve أو reject/override بسبب ظاهر وفق عقد المالك. لا تعتمد وحدة اسمية أوسعر 50 تلقائياً، ولا تصلح هذا الفرع بتغيير 144 وحده. H7B23-01/03/05 و P7B23T-05/06 غير منفذتين.

## قرار الجذور والعمق والحواجز

قرئت عناوين وتصنيفات ومسارات أدلة كل 316 صفاً تاريخياً في دفعات غير مبتورة؛ هذا ليس قراءة كل 316 متناً. قورنت الأجسام الأقرب P2-004 و P4-013/026/032 و P7-013/025/143/144، مع تتبعات المصدر المختارة. [AD10](evidence/root-adjudication-07B23.csv) يشرح كل قرار، و[extensions0](evidence/historical-extensions-07B23.csv) يؤكد صفر توسعات تاريخية.

| الجذر/القرار | الأقرب | حد الفصل |
| --- | --- | --- |
| P7-145 / new-local-root | P2-004;P4-013;P4-032 | تراكم عضوية picker دون إزالة بين selection changes؛ ليست صلاحيات مستخدمين أو حوار جزء بهوية ItemId أو نموذج خاطئ. قصد basket غير محسوم، لذا potential. |
| P7-146 / new-local-root | P7-143;P7-025;P4-013 | cursor مشترك في foreach لقائمة اختيار منفصلة يحذف row أضيفت سابقاً؛ الأصناف فريدة فلا MsgExistItem، ولا تعديل لمجموعة التعداد كما 025 أو هوية جزء 013. |
| P7-147 / new-local-root | P7-144;P7-143;P7-013;P4-026;P7-142 | تملأ seed ثم تحذف ويعاد بناؤها بلا copy حتى لصنف فريد ناجح؛144 تخص projection آخر index ونتيجة void بالعقد، و 143 تكرار، و 026/142 سعر، و PM013 round-trip تكلفة/صافي. |
| P7-143 / same-cause-homologues-not-extended-or-recounted | P7-143 | القارئان الإضافيان يستهلكان 1 زيادةً و 2 new مع أزرار 2/1 نفسها في 143؛11 literal constructions في 7 paths ليست 11 finding أو كل bodies. |
| P7-147;P7-144 / prior-boundary-preserved-distinct-seed-loss | P7-144 | لا يحتاج 147 شرط آخر index في projection144؛ إصلاح TypedLineResult في العقد لا ينقل seed في هذين المحررين بذاته.144 بكل حقولها بلا extension. |
| P4-026;P7-142 / pricing-policy-not-invented-not-recounted | P4-026;P7-142 | يفقد 147 مصدر القيمة قبل تسعير default؛ لا يعتمد 50 أو 20 أو conversion أو enum.026/142 ليسا سبب فقد الوصف والكمية في seed. |
| H7B23-03 / nearest-bodies-compared-not-new-findings | P2-004;P4-013;P4-032;P7-025 | قورنت الأجسام الأقرب المسماة: تراكم permissions عند تغيير مستخدم، وجزء فاتورة يطابق ItemId، ونموذج عقد آخر، وبحث يعدل مجموعة تعداده؛ لا تعاد أسبابها هنا. |
| P1-011 / same-prior-sql-family-not-recounted | P1-011 | Code interpolation ظاهر من عائلة SQL السابقة؛ لا حقن أو تجربة أو finding جديدة منه، ولا قبول لتفويض أو schema. |
| P4-014;P7-132 / barriers-and-potential-preserved | P4-014;P7-132;P4-020;P4-021 | لا قبول Save/stock/ACL/schema أو load-order من report constructor أو row؛ تبقى 014/132 potential و 020/021 وحواجز المال كما هي. |
| H7B23-06 / documentary-preservation-gate | P4-014;P7-132 | قرئت كل 316 خلاصة metadata مع الأقرب المسمى وتتبعات محدودة؛ ليست كل متون التاريخ أو 455FE/census.643 protected و G205/827 والتوازي بلا repair merge. |

اكتشف البحث المعجمي عن `new MsgExistItem(` عبر 477 ملف C# مصدري **11 موضعاً في 7 مسارات**. راجع هذا الجزء سلوك المستهلكين المختارين، لا كل 11 موضعاً أو body أو callgraph؛ المواضع الباقية split صريح. أربع مسارات احتاجت strictUTF8→cp1256 قراءةً فقط، ومنها frmSalePurch الذي قرئت شرائحه بهذا الترميز؛ لا إعادة ترميز أو اعتماد compiler encoding. [الشاهد](evidence/item-ingress-witnesses-07B23.json) يحفظ 29 قراءة نصية محدودة من المسارات 12 كلها و 12 نموذجاً و 12 ملاحظة نصية؛ ليست 29 اختبار ERP.

القارئان الإضافيان يظهران عكس 1/2 نفسه في P7-143؛ لم تمدد حقول 143 أو تعدّه finding جديدة. تبقى 144 و 142 و 026 و 034/035/136–141 بحدودها؛ لا SQL injection جديدة من نفس عائلة 011 أو افتراض SDK/سلة/تحويل/دمج. تبقى P4-014 و P7-132 **potential** و P4-020/021 حاجزي إنتاج، وكل حواجز المال/ACL/stock/save مفتوحة. تصويب B10 الإضافي 10 محلياً مقابل 120 مرجعياً، وعند equality1 كلاهما 10؛ G138 المحمي لم يحرر.

## الحفظ والتحقق والبقايا

حُفظت **643 مادة تاريخية** وكل 316 قاموس finding بكل حقوله وتصنيفاته و ALLnext_phase/evidence وبادئة raw317CRLF/noBOM و G01–205 و 827 أصل تطبيق/29,128,444 بايت وثلاثة freezes. التراكمي **319 نتيجة مفتوحة بلا معالجة**:2Critical/181High/135Medium/1Low؛280confirmed/32potential/7repository-gap؛ المرحلة 7=147. تضاف G206–210 كتوصيات لا خمس findings أخرى.

مكونات المدقق الحالي **650 حالة وثائقية في 24 مجموعة** =606 سابقة محفوظة +44 جديدة؛ ليست اختبارات أعمال. نُفذت **28 وضعية تاريخية OWN** فعلياً بمدخلاتها الخاصة وأدوات التقاطها المعلنة: exit0/827/errors[]، لا ادعاء إعادة كل 28 بعد تثبيت SHA أو تحرير النثر أو push. [stdout B23 الرسمي](evidence/checks-07B23.json) خرج مباشر للمدقق عند checkout الدخول 3276579 قبل commit التسليم، لا JSON معاد تشكيله؛ لا يعاد توليده بعد push. **كل 36 خطة قبول not-executed**؛ لا إصلاح أو تشغيل أو قياس أو قبول ERP.

[SB8](evidence/selection-batch-lineage-07B23.csv)/[IM8](evidence/import-field-lineage-07B23.csv)/[FE18](evidence/feature-implementation-matrix-07B23.csv)/[INV18](evidence/report-invariants-07B23.csv)/[RC6](evidence/report-reconciliation-07B23.csv) تتبع 15 قدرة مصدرية و 3 بوابات وثائقية. [RS14](evidence/residual-disposition-07B23.csv) تحفظ upstream IDs/artifacts/rowSHA/contracts وكل required-input سابق وكل mappedroute والتصرف؛ ليست 14 موافقة. [SP01–03](evidence/split-register-07B23.csv) تحفظ بقية callers/editors/writers/output والحصر و SDK/words/currency/legacy/precision/templates ضمن 7B؛ لا نقل صامت إلى 7C أو وعد بآخر جزء.

**المتابعة الموازية:** سلّم SHA هذا التدقيق بعد دفعه إلى محادثة الإصلاح كي تراجعه وتدمج تاريخ التدقيق في فرعها دون استبدال ملفاتها أو إعادة كتابة التاريخ. لا merge إصلاح→تدقيق هنا ولا ادعاء أن الفرع الآخر بدأ أو التقط هذا التسليم بالفعل.
