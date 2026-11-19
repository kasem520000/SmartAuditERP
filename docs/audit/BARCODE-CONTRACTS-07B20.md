# عقود الباركود والميزان والمستهلك والملصق — 7B20

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B20 بعد دفع B19 المكتمل `ac20e3104f84fefbc62779e22d2c9b9621802340` بجميع **558 مسار تدقيق**. ساعة التجميد المرصودة `2026-11-19T18:40:15.182879+00:00` مستقلة عن المرجع المعلن؛ ليست تاريخ تشغيل تطبيق أو قبول.

**R4d سُلّم بحدوده فقط؛ 7B/7 جزئيتان؛ R4e/7B21 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا تشغيل أو بناء ERP/C#/VB/WPF/SQL أو SDK/provider/UtilitiesProj/ToDataTable/REPX أو ماسح أو طابعة أو بيانات أعمال أو أسرار أو إصلاح أو قبول أو قياس تشغيلي. Python وGit لأدوات الوثائق فقط؛ `next_phase=8` تخطيط لا إذن.

[النتيجة](PHASE-07B20.md) · [عقود الباركود والملصق](BARCODE-CONTRACTS-07B20.md) · [التحقق والخطط](VALIDATION-07B20.md) · [المتبقي](PHASE-07-REMAINING-07B20.md) · [scope20](review-scope-07B20.csv) · [السجل](findings.csv) · [provenance553](evidence/provenance-07B20.json) · [stdoutB20](evidence/checks-07B20.json)

## 1. نموذج مرجعي مقترح، لا إصلاح مطبق

المدخل المنقح هو نص الرمز ومصدر التعريف وصف الوحدة ونوع المسار المطلوب. لا تستخدم عينات مستخدم حقيقية. «حمولة صحيحة» هنا تعني أن الأجزاء الرقمية أنتجت قيمة موجبة في فرع المصدر المختار؛ لا إثبات checksum أو معيار أو ثقة في الماسح.

```text
InputText + SupportedConsumerPolicy + UnitIdentityContract
  -> ExactUnit | Alias | ScaleCandidate | Unsupported | NotFound | Failed
  -> DecodeResult {health, sourceKind, ItemId, UnitId, ValueKind,
                   quantity?, price?, priceBasis, precision, sourceVersion}
  -> explicit invoice-row request OR declared selection-only/label request
  -> final quantity/unit/price checks + isolated row identity
  -> local projection -> manifest-defined table/template/output outcome
```

هذا فصل مقترح لمسؤوليات غير مكتملة، لا DTO خارجي اكتشف أو API جديد نُفذ. لا يفرض دعم الميزان على كل شاشة، لكنه لا يسوي invalid مع صفر أو نجاح هوية. وسياسة Wscale2/3 هل القيمة unit-price أم extended-price/weight يجب أن يثبتها المالك لا اسم الحقل.

## 2. مصادر القارئ وأنماط القيمة DC5

| العقد والنوع | الكمية / السعر | هوية الوحدة والصحة | الدليل والحد |
| --- | --- | --- | --- |
| DC7B20-01 / unit-exact | 0 افتراضية / 0 افتراضي | ItemUnits.unit من أول صف exact؛ يعيد هوية ووحدة وقيمتين 0 قبل scale، دون نتيجة health مستقلة. | SmartAuditERP/Class/ItemOper.cs:1908-2091؛ تعليمات مصدر محدودة لا صيغة GS1 معتمدة أو فك ماسح فعلي أو كل barcode engines. |
| DC7B20-02 / alias-exact | 0 افتراضية / 0 افتراضي | unitId0 ثم حسم إضافي لدى المستهلك؛ Itembarcodes exact يرجع قبل scale؛ ليس unit0 عقد وحدة مكتملًا وحده. | SmartAuditERP/Class/ItemOper.cs:1908-2091؛ تعليمات مصدر محدودة لا صيغة GS1 معتمدة أو فك ماسح فعلي أو كل barcode engines. |
| DC7B20-03 / Wscale1 | chars7..8 + chars9..11 /1000 / 0 افتراضي | أول وحدة في صفوف prefix-query الموصولة؛ فشل جزء رقمي يصير 0 والهوية تبقى ناجحة. | SmartAuditERP/Class/ItemOper.cs:1908-2091؛ تعليمات مصدر محدودة لا صيغة GS1 معتمدة أو فك ماسح فعلي أو كل barcode engines. |
| DC7B20-04 / Wscale2 | 0 افتراضية / chars7..9 + chars10..11 /100 | أول وحدة في صفوف prefix-query الموصولة؛ الجزء الفاشل يصير 0 بلا health مستقل. | SmartAuditERP/Class/ItemOper.cs:1908-2091؛ تعليمات مصدر محدودة لا صيغة GS1 معتمدة أو فك ماسح فعلي أو كل barcode engines. |
| DC7B20-05 / Wscale3 | Round(price/SalePrice,3) إن SalePrice>0 وإلا0 / Round(decodedPrice,2) | نفس وحدة ومصدر SalePrice لأول صف prefix؛ يضبط static flag true؛ لا سياسة دقة/صفر أو health أو checksum معتمدة. | SmartAuditERP/Class/ItemOper.cs:1908-2091؛ تعليمات مصدر محدودة لا صيغة GS1 معتمدة أو فك ماسح فعلي أو كل barcode engines. |

يعود exact قبل scale؛ ليس كل رمز من13 حرفاً ميزاناً. لا يثبت length صحة الأجزاء أو معيار الحرف الأخير. فرعWscale3 يقسم على SalePrice الموجب ويقرب3 ويضبط علماًstatic معروفاً؛ لا سياسة ضريبة/عملة أو سعر مجاني مستنتجة من ذلك.

## 3. المستهلكون السبعة BC7 وحدود القصد

| الموضع والمستهلك | المدخل والأثر | نقل الكمية / السعر / علم الميزان | الروابط والحد |
| --- | --- | --- | --- |
| BC7B20-01 — frmInvInputOutput<br>SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:448-450 | IO Enter/KeyDown أو Code fallback<br>identity+unit-only | discarded / discarded / false | FE7B20-01; P7-136<br>عقد نقل وزن IO أو إعلان النمط unsupported قبل الإضافة. |
| BC7B20-02 — frmInvPOS<br>SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:881-885 | txtBarcode Enter<br>positive-values-only-after-new-line | positive-only / positive-only / positive-qty-or-price | FE7B20-03;FE7B20-05;FE7B20-06; P7-138;P4-014;P4-028<br>نجاح إضافة سطر ومطابقة item/unit/index شرطان؛ ليس هذا اعتماد POS كاملاً. |
| BC7B20-03 — frmInvPurch<br>SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:652-655 | Window Enter مع التركيز أو Code fallback<br>identity+unit-only | discarded / discarded / false | FE7B20-01; P7-136<br>عقد كمية/قيمة الميزان في الشراء لا يستنتج من itemId ناجح وحده. |
| BC7B20-04 — frmInvSale<br>SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:708-710 | txtBarcode Enter<br>identity+unit-only | discarded / discarded / false | FE7B20-01; P7-136<br>سطر جديد ناجح؛ المثال لا يخلط عروضاً أو سعر عميل بديل أو كتابة محفوظة. |
| BC7B20-05 — frmInventoryTransfer<br>SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:654-655 | SearchByCode fallback مثبت؛ لا Enter ماسح مباشر من الشرائح<br>identity+unit-selection-only | discarded-support-unresolved / discarded-support-unresolved / false | FE7B20-08; H7B20-03;P4-019<br>ليس ضمن P7-136 كوجوب وزن للمناقلة بلا مصفوفة دعم. |
| BC7B20-06 — frmPrintBarcode<br>SmartAuditERP/Form_WPF/frmPrintBarcode.xaml.cs:224-225 | Window Enter مع تركيز txtItemBarcode<br>label-raw-barcode+base-item-price | not-label-copy-count / discarded-use-base-price / not-invoice-line | FE7B20-10;FE7B20-12; P7-037;H7B20-02<br>ItemQty1 عدد ملصقات لا وزن؛ wire/template والطابعة غير معتمدة. |
| BC7B20-07 — frmSafeAdjust<br>SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:624-625 | Window Enter مع تركيز txtBarcode وحارس المخزن<br>item-selection-for-stock-not-counted-weight | not-realstock-count / not-selected-price / not-invoice-line | FE7B20-09; H7B20-03;P4-017;P4-018<br>يعين SelectedId ويحسِب الرصيد وRealStock0؛ لا عيب وزن جديد بلا قصد مدعوم. |

دفتر BC يحتفظ كذلك بالنص الخام للوسائط وبصمة النداء وحدوده والمالك والمدخل والأثر والخطوة. الاستخراج pattern حرفي مؤهل مع موازنة أقواس/تعليقات/اقتباسات داخل الوسائط، لا parser C# أو type-resolution. قُرئت المواضع السبعة بعد الاكتشاف؛ aliases/delegates/reflection والقارئات الأخرى خارج الحصر. لا يستنتج توجيه لوحة مفاتيح مباشر للمناقلة من نداء fallback وحده.

## 4. مقابلة مصدري الملصق دون طباعة

- **ملصق المسح:** ItemId/UnitId/قيمة مفكوكة تصل إلى ReadBarcode، ثم يبقى النص الممسوح ويؤخذ Common.GetItemPrice من سعر الصنف الأساسي. ItemQty=1 هنا عدد ملصقات، لا وزن ميزان. يسقط DTO الاسم والرقم والسعر كنص والرمز والتاريخ والجهة، ثم يستدعي ToDataTable الخارجي وBarcode.repx؛ لا wire-schema معتمد. P7-037 محفوظة.
- **اليدوي:** اختيار الصنف والرمز يقيد lookup بـItemID+barcode ويقرأ IU.sale. يكتب F2 للسعر الأساس وللشامل المشتق من defVAT عندtax!=0، ثم ينتقي خياراً في BindToData. كلا الخيارين معاً رفض صريح؛ دونهما Price فارغ. تحويل النص الفاشل يسقط0 محلياً؛ لم يجر اختبار ثقافة أو ضريبة. الحقول القابلة للتحرير والجهة والتواريخ إلى strings ليست عقد اعتماد منشور.
- **النسخ والمخرج:** المتعدد لا يستدعي PrintBarcode إلا لكمية موجبة، ثم loop مباشر. اليدوي يرفض txtQuat الفارغ ثم TryParse، فيصير النص غير الرقمي0 وتكون loop بلا تكرار؛ ShowPreviewDialog مسار منفصل. لا إعادة عد لـP7-030 من محرك فاتورة آخر، ولا نجاح ورق من void أو غياب exception.
- يوجد في نص مسار Barcode2 علامتا اتجاه RTL؛ سجلت كحد manifest/path لا finding جديدة بلا حزمة فعلية. `frmBarcodeSetting.cs` القديم واجهة رسم/تدوير لا إثبات أنه عقد بروتوكول الميزان المشترك، وهو خارج scope20. لا أعيدت ترميز ملفات قديمة أو تحميل قالب/طابعة.

دعم محدد: `SmartAuditERP/Form_WPF/frmPrintBarcode.xaml.cs:215-253`؛ `SmartAuditERP/Form_WPF/frmPrintBarcode.xaml.cs:307-325`؛ `SmartAuditERP/Form_WPF/frmPrintBarcode.xaml.cs:337-381`؛ `SmartAuditERP/Class/Common.cs:560-578`؛ `SmartAuditERP/Form_WPF/frmItemsBarcode.xaml.cs:142-174`؛ `SmartAuditERP/Form_WPF/frmItemsBarcode.xaml.cs:206-237`؛ `SmartAuditERP/Form_WPF/frmItemsBarcode.xaml.cs:274-328`؛ `SmartAuditERP/Form_WPF/frmItemsBarcode.xaml.cs:334-488`؛ `SmartAuditERP/Class/InvoiceData.cs:274-283`؛ `SmartAuditERP/Class/InvoiceData.cs:374-380`؛ `SmartAuditERP/Class/InvoiceData.cs:415-423`.

## 5. العقود والثوابت والمسؤوليات — 16 عقداً لا16 ميزة جديدة

الأول13 source-bound بشرائح؛ آخر3 بوابات وثائقية تستخدم `none-documentary-metadata` بوضوح، لا سطر مصدر مصطنع. لكل عقد خطتان في [القبول32](evidence/acceptance-tests-07B20.csv) و[الشرح](VALIDATION-07B20.md)، كلتاهما not-executed. الربط لا يعد اختباراً مشغلاً أو تبنياً تلقائياً لمعيار قبول مقترح.

### FE7B20-01 / INV7B20-01 — نقل قيم الميزان إلى محررات الفاتورة

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | Sale/Purch/InputOutput — Enter/ReadBarcode → SearchForBarcode → SearchByID(false) → GetItemByID/LoadUnitInf |
| الملاحظة الساكنة | الكمية والسعر المفكوكان ينقطعان عند Sale/Purch/InputOutput؛ على مسار سطر جديد ناجح تضبط LoadUnitInf الكمية إلى 1 ومصدر سعر الوحدة. POS ينقل القيم الموجبة كشاهد مقابل. |
| الثابت المطلوب | يحفظ طلب السطر نوع قيمة الميزان ووحدتها وكمّيتها/سعرها، أو يرفض المستهلك نمطاً غير مدعوم قبل الإضافة؛ لا قبول لهوية نجاح مع إسقاط payload صامت. |
| الدليل | SmartAuditERP/Class/ItemOper.cs:729-811;1035-1185;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:667-725;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:613-663;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:427-458;SmartAuditERP/Class/ItemOper.cs:1908-2091 |
| الحد | سطر جديد ناجح بلا مزج أو عروض أو ضريبة أو سعر عميل بديل؛ لا كتابة محفوظة مثبتة. قصد الدعم يحدده المالك، ولا تُلزم كل شاشة بنقل الوزن. |
| المالك | مالك ItemOper ومحررات الفاتورة والمحاسب |
| المدخل المنقح | support-matrix لكل مستهلك: إدخال بيع/شراء/IO أو selection-only للمناقلة والتسوية والملصق، مع نتيجة decode typed/health/unit/valueKind. تبقى DocumentRef/sourceKind/globalId/branch/allowed-set وinit/Loaded/reset/dirty/cancel/generation على SDK معلوم مطلوبة. |
| الأثر إن غاب | لا تعميم P7-136 على قصد التسوية والمناقلة، ولا افتراض أن كل 13 حرفاً معيار بعينه؛ P7-132 محتملة وعقود الفتح السابقة لا تعتمد من مسار المسح. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-136; P7B20T-01;P7B20T-02; not-executed |

### FE7B20-02 / INV7B20-02 — وحدة بادئة الميزان ليست أول صف اعتباطي

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | ItemOper.SearchForBarcode — Items+ItemUnits وOR رمز الأساس → Rows[0].unit/SalePrice → POS → UnitEquality |
| الملاحظة الساكنة | شرط Items.barcode=prefix يطابق كل وحدات الصنف الموصولة حتى مع رموز وحدة مختلفة؛ يأخذ Rows[0] بلا مفتاح وحدة للرمز أو ترتيب حاسم. كاتب التعريف يسمح بوحدة أساس وإضافية. |
| الثابت المطلوب | تحسم البادئة وحدة واحدة وفق عقد الرمز أو ترد ambiguous؛ لا يتغير معنى كمية الأساس بتبديل ترتيب مرشحي الوحدات. |
| الدليل | SmartAuditERP/Class/ItemOper.cs:1908-2091;729-811;SmartAuditERP/Form_WPF/frmItems.xaml.cs:905-925;1022-1054;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:871-955 |
| الحد | المؤكد تعدد مرشحي الشرط وعدم حسم هويتهم؛ لا نحدد أول صف SQL فعلي أو نفترض قيود نشر أو نرصد وحدة خاطئة زمن التشغيل. |
| المالك | مالك هوية الصنف والوحدة وDBA وItemOper |
| المدخل المنقح | schema/migrations/grants/constraints/FK/unique/row-version وأدوار×أوامر×فروع×موارد، بلا أسرار. يشمل عقد ItemId/UnitId/base-code/barcode والتفرد، وعقد Inv/SafesAdjust السابق ومفاتيح الربط. |
| الأثر إن غاب | شرط SQL أو UI ليس تفويضاً؛ لم يفحص ترتيب صفوف منشور أو قيود نشر، وP7-036 وأصول ACL باقية. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-137; P7B20T-03;P7B20T-04; not-executed |

### FE7B20-03 / INV7B20-03 — صحة حمولة الميزان مستقلة عن العثور على الصنف

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | ItemOper→POS — ToDouble(failure→0) → itemId>0 → تحديثات POS للقيم الموجبة فقط |
| الملاحظة الساكنة | فشل ToDouble يصير صفراً بلا health؛ بادئة موجودة مع AABBB تعيد هوية وqty0، فيضيف POS افتراضياً 1 كنمط عادي عند نجاح بقية المسار. AA250 قد تنتج 0.25 رغم فساد الجزء الصحيح. |
| الثابت المطلوب | invalid-payload ليست success أو zero أو regular؛ لا يضاف سطر افتراضي أو وزن جزئي بعد فشل جزء من حمولة الميزان. |
| الدليل | SmartAuditERP/Class/ItemOper.cs:93-103;1908-2091;729-811;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:871-955 |
| الحد | بشرط غياب exact match ونجاح prefix وصنف/وحدة صالحين؛ ASCII توضيحي لا اختبار TryParse أو قواعد checksum/ماسح معيارية. |
| المالك | مالك قارئ الباركود وPOS وعقد الإدخال |
| المدخل المنقح | culture/zone/SDK/provider وDTO/DateTimeBox وترتيب Loaded وملكية الأحداث منقحة. أضف صيغة الماسح والرمز والطابعة وسياسة empty/invalid/unknown/zero/missing-price وحالات الفشل، دون بيانات حقيقية. |
| الأثر إن غاب | نماذج ASCII/Decimal لا تنفذ TryParse/.NET أو الماسح أو القالب أو جدولة WPF؛ لا قياس أو ثقافة أو منطقة مفترضة. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-138; P7B20T-05;P7B20T-06; not-executed |

### FE7B20-04 / INV7B20-04 — أسبقية المصادر الدقيقة والبدائل

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | ItemOper.SearchForBarcode — ItemUnits exact → Itembarcodes exact → length13 scale |
| الملاحظة الساكنة | المطابقة الدقيقة في ItemUnits ثم Itembarcodes تسبق scale؛ يعيد alias الوحدة 0 والقيمتين 0، وقد يحسم LoadUnitInf وحدة افتراضية. طول 13 وحده لا يثبت صيغة معيارية. |
| الثابت المطلوب | تعلن أسبقية المصادر وهوية الرمز ومعنى unit0 ضمن support-matrix؛ لا يفسر رمز دقيق معتبر كوزن دون قرار صريح. |
| الدليل | SmartAuditERP/Class/ItemOper.cs:1908-2091 |
| الحد | لا ادعاء بمراجعة كل محركات الباركود أو منع التصادم أو خطأ معياري من أسبقية المصدر وحدها. |
| المالك | مالك المنتج والباركود وهوية الوحدة |
| المدخل المنقح | support-matrix لكل مستهلك: إدخال بيع/شراء/IO أو selection-only للمناقلة والتسوية والملصق، مع نتيجة decode typed/health/unit/valueKind. تبقى DocumentRef/sourceKind/globalId/branch/allowed-set وinit/Loaded/reset/dirty/cancel/generation على SDK معلوم مطلوبة. |
| الأثر إن غاب | لا تعميم P7-136 على قصد التسوية والمناقلة، ولا افتراض أن كل 13 حرفاً معيار بعينه؛ P7-132 محتملة وعقود الفتح السابقة لا تعتمد من مسار المسح. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-03;P7-036; P7B20T-07;P7B20T-08; not-executed |

### FE7B20-05 / INV7B20-05 — نقل POS للقيم الموجبة وحدوده

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | frmInvPOS.ReadBarcode — Enter → decode → isScale → SearchByID → مطابقة item/unit/index → override |
| الملاحظة الساكنة | POS لا يهمل القيم الموجبة مثل الثلاثة؛ بعد SearchByID يطابق item/unit وItemRowIndex==Count. نجاح الإضافة/المزج والـDTO وحالات الصفر حدود لا اعتماد كلي. |
| الثابت المطلوب | تطبق نتيجة decode المتماسكة على السطر المقصود بهوية صريحة؛ لا يعتمد الربط على Count وحده عند فشل إضافة أو مزج أو ترقيم مختلف. |
| الدليل | SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:834-850;871-955;SmartAuditERP/Form_WPF/frmInvPOS.xaml:832-848 |
| الحد | مراجعة الشرائح فقط؛ لا finding تكرار جديدة ولا حكم بأن شرط الفهرس يفشل في كل مسح. |
| المالك | مالك POS وعقد السطر |
| المدخل المنقح | support-matrix لكل مستهلك: إدخال بيع/شراء/IO أو selection-only للمناقلة والتسوية والملصق، مع نتيجة decode typed/health/unit/valueKind. تبقى DocumentRef/sourceKind/globalId/branch/allowed-set وinit/Loaded/reset/dirty/cancel/generation على SDK معلوم مطلوبة. |
| الأثر إن غاب | لا تعميم P7-136 على قصد التسوية والمناقلة، ولا افتراض أن كل 13 حرفاً معيار بعينه؛ P7-132 محتملة وعقود الفتح السابقة لا تعتمد من مسار المسح. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-138;H7B20-03; P7B20T-09;P7B20T-10; not-executed |

### FE7B20-06 / INV7B20-06 — الكمية النهائية لا الكمية الافتراضية تدخل الحارس

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | POS/ItemOper — SearchByID → ISvalidQuantity(default) → ReadBarcode يستبدل الكمية → CalcRows |
| الملاحظة الساكنة | حارس الكمية الظاهر يسبق استبدال ReadBarcode لكمية السطر بالمفكوكة. CalcRows حساب لا حجز ذري؛ هذه حافة للأصل P4-014 لا نتيجة أخرى. |
| الثابت المطلوب | تراجع كمية الأساس النهائية ونطاق المخزن، مع عقد حجز/رفض ذري معتمد عند الكتابة؛ اجتياز الكمية الافتراضية 1 لا يثبت اجتياز حمولة 4. |
| الدليل | SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:871-955;1901-1978;SmartAuditERP/Class/ItemOper.cs:1829-1902;1367-1430 |
| الحد | P4-014 تبقى potential؛ لا تنفيذ حفظ أو تزامن أو دعوى تجاوز حماية خادم منشور أو بيع زائد محفوظ. |
| المالك | مالك المخزون وPOS وDBA |
| المدخل المنقح | schema/migrations/grants/constraints/FK/unique/row-version وأدوار×أوامر×فروع×موارد، بلا أسرار. يشمل عقد ItemId/UnitId/base-code/barcode والتفرد، وعقد Inv/SafesAdjust السابق ومفاتيح الربط. |
| الأثر إن غاب | شرط SQL أو UI ليس تفويضاً؛ لم يفحص ترتيب صفوف منشور أو قيود نشر، وP7-036 وأصول ACL باقية. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P4-014; P7B20T-11;P7B20T-12; not-executed |

### FE7B20-07 / INV7B20-07 — دلالة سطر الميزان والسعر الممتد

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | ItemOper.GetItemByID/CalcRows — isScale → قواعد المزج → LoadUnitInf → ItemPrimaryQnty وstatic flag |
| الملاحظة الساكنة | يحمل الإنشاء isScale ويضبط LoadUnitInf الكمية 1؛ يحسب CalcRows quantity×equality ويستعمل static price flag للسعر الممتد. سياسة resolver في 026 والعلم 028 باقيان. |
| الثابت المطلوب | نوع القيمة ومصدر السعر والوحدة والكمية خاص بكل سطر؛ لا تسرب static ولا تجاوز لسياسة resolver عند وجود وحدة. |
| الدليل | SmartAuditERP/Class/ItemOper.cs:491-576;729-811;1035-1185;1367-1430;30-34 |
| الحد | ليس كل GetItemByID أو أسعار العملاء والعروض أو الضرائب مراجعاً؛ نقل payload لا يعالج 026/028 ولا يعتمد الحساب المالي. |
| المالك | مالك ItemOper والتسعير والمحاسب |
| المدخل المنقح | قاموس وحدة/أساس/perc، ونوع قيمة الميزان Weight/UnitPrice/ExtendedPrice، والدقة ومصدر السعر والضريبة. تبقى عقود BOM التاريخية وas-of وmetric/period/الاستحقاق من الأجزاء السابقة منقحة ومطلوبة. |
| الأثر إن غاب | لا اعتماد لتحويل كمية أو قيمة أو ضريبة أو تسوية من prefix أو N2؛ تقدم الباركود لا يعتمد أي عقد BOM/HR/VAT سابق. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P4-026;P4-028; P7B20T-13;P7B20T-14; not-executed |

### FE7B20-08 / INV7B20-08 — المناقلة: نقل هوية ووحدة وحدود دعم الوزن

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | frmInventoryTransfer — SearchByCode fallback → ReadBarcode → SearchByID(itemId,unitId) |
| الملاحظة الساكنة | SearchByCode fallback يصل إلى ReadBarcode ثم SearchByID بالهوية والوحدة دون القيم. وجوب نقل الوزن في المناقلة عقد دعم؛ اختصارات النافذة المقروءة لا تثبت Enter ماسح مباشراً. |
| الثابت المطلوب | إما وزن مدعوم بعقد نقل قيمة واضح، أو selection-only/unsupported معلن؛ لا تسمى كمية افتراضية وزناً ممسوحاً معتمداً. |
| الدليل | SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:167-218;575-614;648-666;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml:1-18 |
| الحد | المناقلة ليست ضمن P7-136 بلا شرط دعم؛ P4-019 باقية، ولا حفظ جانبي المناقلة أو كل callgraph مراجع. |
| المالك | مالك المناقلة وWPF والمنتج |
| المدخل المنقح | support-matrix لكل مستهلك: إدخال بيع/شراء/IO أو selection-only للمناقلة والتسوية والملصق، مع نتيجة decode typed/health/unit/valueKind. تبقى DocumentRef/sourceKind/globalId/branch/allowed-set وinit/Loaded/reset/dirty/cancel/generation على SDK معلوم مطلوبة. |
| الأثر إن غاب | لا تعميم P7-136 على قصد التسوية والمناقلة، ولا افتراض أن كل 13 حرفاً معيار بعينه؛ P7-132 محتملة وعقود الفتح السابقة لا تعتمد من مسار المسح. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-03;P4-019; P7B20T-15;P7B20T-16; not-executed |

### FE7B20-09 / INV7B20-09 — التسوية: المسح يختار الصنف لحساب الرصيد

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | frmSafeAdjust — store/Enter → decode → SelectedId → CalcStock → RealStock0 |
| الملاحظة الساكنة | يستخدم قارئ التسوية SelectedId لحساب المخزون ثم RealStock0؛ ليس وزن الباركود بالضرورة العد الفعلي المقصود. تجاهل payload هنا لا يكفي لعيب وزن. |
| الثابت المطلوب | يعلن اختيار الصنف فقط إذا كان قصد المسار؛ لا يختلط الرصيد أو العد الفعلي أو وحدته بوزن رمز دون سياسة. |
| الدليل | SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:291-336;410-436;618-643;1708-1725;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml:1-16 |
| الحد | لا إعادة عد لاعتماد/اتصال P4-017/018 أو قارئ P7-131، ولا حكم بوجوب نقل كمية الميزان إلى التسوية. |
| المالك | مالك التسوية والمخزون والمنتج |
| المدخل المنقح | support-matrix لكل مستهلك: إدخال بيع/شراء/IO أو selection-only للمناقلة والتسوية والملصق، مع نتيجة decode typed/health/unit/valueKind. تبقى DocumentRef/sourceKind/globalId/branch/allowed-set وinit/Loaded/reset/dirty/cancel/generation على SDK معلوم مطلوبة. |
| الأثر إن غاب | لا تعميم P7-136 على قصد التسوية والمناقلة، ولا افتراض أن كل 13 حرفاً معيار بعينه؛ P7-132 محتملة وعقود الفتح السابقة لا تعتمد من مسار المسح. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-03;P4-017;P4-018; P7B20T-17;P7B20T-18; not-executed |

### FE7B20-10 / INV7B20-10 — ملصق المسح يحتفظ بالرمز لا سعر وحدته

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | frmPrintBarcode — decode → GetItemPrice الأساس → InvoiceData → ToDataTable → Barcode.repx |
| الملاحظة الساكنة | ملصق المسح يحتفظ بالرمز الممسوح لكنه يأخذ Items.sale_price دون unitId؛ P7-037 باقية. السعر في DTO نص ثقافي، لا نوع wire مثبت. |
| الثابت المطلوب | يربط عقد الملصق رمز الوحدة بمصدر السعر وpriceBasis والعملة/الضريبة حتى المستهلك؛ لا رمز عبوة بسعر أساس بعد محو هوية وحدته. |
| الدليل | SmartAuditERP/Form_WPF/frmPrintBarcode.xaml.cs:50-90;215-253;337-381;SmartAuditERP/Class/Common.cs:560-578;SmartAuditERP/Class/InvoiceData.cs:274-283;374-380;415-423;SmartAuditERP/Form_WPF/frmPrintBarcode.xaml:1-16;199-206 |
| الحد | P7-037 قديمة لا تسجل ثانية؛ لا UtilitiesProj.ToDataTable أو REPX أو طباعة أو سعر مطبوع نُفذ. |
| المالك | مالك الملصقات والتقارير والنشر |
| المدخل المنقح | manifest/hash/version/SDK وwire-tabletypes/aliases وUtilitiesProj.ToDataTable/REPX لكل مخرج متبقٍّ. للملصقين: Barcode.repx وBarcode2.repx، وثقافة السعر والتاريخ، وصيغة الرمز والنسخ والوجهة وoutcome، بلا أسرار. |
| الأثر إن غاب | DTO محلي لا يثبت نوع الجدول أو صحة القالب أو طباعة السعر والرمز؛ بقية مصبات R1/R2/R3 لا تعتمد من فرعين محليين. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-037;H7B20-02; P7B20T-19;P7B20T-20; not-executed |

### FE7B20-11 / INV7B20-11 — ملصق الوحدة المختارة شاهد مقابل لا قبول ضريبي

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | frmItemsBarcode — item+barcode → IU.sale → defVAT/خيار السعر → DTO |
| الملاحظة الساكنة | المسار اليدوي يقيد ItemID والرمز ويقرأ IU.sale، كشاهد يمنع تعميم P7-037. يشتق سعر الشمول من defVAT عندما tax غير 0؛ اعتماد الضريبة والدقة للمالك. |
| الثابت المطلوب | هوية رمز/وحدة/سعر/ضريبة صريحة؛ حالات كلا الخيارين أو لا خيار أو تعذر مصدر السعر لا تنتج قيمة قديمة/فارغة معتبرة دون قرار. |
| الدليل | SmartAuditERP/Form_WPF/frmItemsBarcode.xaml.cs:142-174;206-237;274-328;334-488;SmartAuditERP/Form_WPF/frmItemsBarcode.xaml:211-294 |
| الحد | لا finding ضريبة جديدة بافتراض أن defVAT خطأ لكل منتج، ولا اعتماد تفرد أو تنفيذ UI من checkbox في المصدر. |
| المالك | مالك الملصقات والمحاسب |
| المدخل المنقح | قاموس وحدة/أساس/perc، ونوع قيمة الميزان Weight/UnitPrice/ExtendedPrice، والدقة ومصدر السعر والضريبة. تبقى عقود BOM التاريخية وas-of وmetric/period/الاستحقاق من الأجزاء السابقة منقحة ومطلوبة. |
| الأثر إن غاب | لا اعتماد لتحويل كمية أو قيمة أو ضريبة أو تسوية من prefix أو N2؛ تقدم الباركود لا يعتمد أي عقد BOM/HR/VAT سابق. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-037;H7B20-01;H7B20-02; P7B20T-21;P7B20T-22; not-executed |

### FE7B20-12 / INV7B20-12 — نسخ الملصق والمعاينة ليست محرك الفاتورة

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | frmPrintBarcode/frmItemsBarcode — positive ItemQty أو TryParse qty loop أو preview مرة → template sink |
| الملاحظة الساكنة | المتعدد يحرس ItemQty>0 ويدور مباشرة؛ اليدوي يفحص فراغ النص ثم TryParse للنسخ، والمعاينة منفصلة لا تكرر بعدد qty. الجسر والقالب والوجهة والنتيجة خارجية. |
| الثابت المطلوب | عدد الملصقات المرسلة والمعاينة والوجهة والفشل/النجاح بعقد صريح؛ ترفض الكمية غير الصالحة قبل الإرسال ولا يستنتج تسليم الورق من رجوع void. |
| الدليل | SmartAuditERP/Form_WPF/frmPrintBarcode.xaml.cs:307-325;337-381;SmartAuditERP/Form_WPF/frmPrintBarcode.xaml:317-336;408-421;SmartAuditERP/Form_WPF/frmItemsBarcode.xaml.cs:334-488;SmartAuditERP/Form_WPF/frmItemsBarcode.xaml:358-405 |
| الحد | لا طباعة أو قياس نسخ أو إعادة عد 030/031؛ حلقة هذين المسارين مختلفة عن محرك الفاتورة ذي علة الصفر القديمة. |
| المالك | مالك الملصقات والنشر والتشغيل |
| المدخل المنقح | manifest/hash/version/SDK وwire-tabletypes/aliases وUtilitiesProj.ToDataTable/REPX لكل مخرج متبقٍّ. للملصقين: Barcode.repx وBarcode2.repx، وثقافة السعر والتاريخ، وصيغة الرمز والنسخ والوجهة وoutcome، بلا أسرار. |
| الأثر إن غاب | DTO محلي لا يثبت نوع الجدول أو صحة القالب أو طباعة السعر والرمز؛ بقية مصبات R1/R2/R3 لا تعتمد من فرعين محليين. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-02;P7-030;P7-031; P7B20T-23;P7B20T-24; not-executed |

### FE7B20-13 / INV7B20-13 — صيغة الميزان والدقة والصفر عقود غير معتمدة

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | SearchForBarcode/Wscale writer — Wscale1/2/3 → substring → mode3 divide/Round3 → consumer |
| الملاحظة الساكنة | أجزاء القيمة لا تقرأ الحرف الأخير ولا تتحقق من كل المحارف؛ Wscale3 يقسم السعر على IU.sale ويقرب الكمية إلى 3 منازل إذا كان المقام موجباً وإلا 0. لا افتراض GS1. |
| الثابت المطلوب | تحدد صيغة الرمز ونوع القيمة ودقة الوحدة وسياسة zero/missing-price وchecksum إن كان مدعوماً؛ تعذر العقد لا يعامل كنجاح عادي. |
| الدليل | SmartAuditERP/Class/ItemOper.cs:1908-2091;SmartAuditERP/Form_WPF/frmItems.xaml.cs:905-925 |
| الحد | لا تستنتج قاعدة معيار أو دقة أو صنف مجاني من الأمثلة؛ ASCII ليس مطابقة ثقافات، والتفقيط والعملة الأوسع خارج العينة. |
| المالك | مالك صيغة الميزان والمحاسب وعقد الإدخال |
| المدخل المنقح | culture/zone/SDK/provider وDTO/DateTimeBox وترتيب Loaded وملكية الأحداث منقحة. أضف صيغة الماسح والرمز والطابعة وسياسة empty/invalid/unknown/zero/missing-price وحالات الفشل، دون بيانات حقيقية. |
| الأثر إن غاب | نماذج ASCII/Decimal لا تنفذ TryParse/.NET أو الماسح أو القالب أو جدولة WPF؛ لا قياس أو ثقافة أو منطقة مفترضة. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | P7-138;P4-028;H7B20-01;H7B20-05; P7B20T-25;P7B20T-26; not-executed |

### FE7B20-14 / INV7B20-14 — نسب كل بقية قديمة دون موافقة خارجية

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | RS14/HQ6 — صف B19 وhash/contracts → تصرف B20 المحدود |
| الملاحظة الساكنة | كل بقية من B19 محتفظة بهويتها وبصمة صفها وعقودها. تقدم الباركود في RS13 جزئي؛ العملة والتفقيط وبقية القوالب وACL والسياسات مفتوحة. |
| الثابت المطلوب | لكل RS19 صف RS20 واحد مع upstreamArtifact/rowSHA/contracts ومالك ومدخل وأثر وخطوة ومعيار؛ ليست 14 موافقة. |
| الدليل | none-documentary-metadata |
| الحد | هذا نسب مسؤولية للعقود الخارجية، لا إعادة مراجعة كل جسم أو اعتماد نشر. |
| المالك | مالك التدقيق وملاك العقود الخارجية |
| المدخل المنقح | قائمة قدرات ومداخل ومصادر ومخارج متفق عليها خارج BC7 وحدّي الملصق، مع crosswalk إلى 455FE التاريخية وNV22/LC7 وسبب supported/unsupported/optional وكل split أو استبعاد. |
| الأثر إن غاب | 7B/7 جزئيتان؛ لا ختم من 477 بحثاً أو 410 مسارات أو 3 splits، ولا نقل صامت لمتطلب 7B إلى 7C. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-06; P7B20T-27;P7B20T-28; not-executed |

### FE7B20-15 / INV7B20-15 — حد الحصر والتقسيم الصريح بعد BC7

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | SP01–03/20 scope — قرار SP03 → decoder/BC7 وحدا label → R4e/7B21 المتبقي |
| الملاحظة الساكنة | 477 بحثاً نصياً و7 qualified tokens ليست كل callgraph أو مراجعة 477 جسماً. المسارات الـ20 قديمة في الاتحاد 410؛ المكمل 417 ومقاطع غير مستكملة داخل 410 باقيان. |
| الثابت المطلوب | لكل بقية مهمة دليل أو استبعاد مسند أو handoff/split مسمى؛ لا ينقل متطلب 7B غير المراجع إلى 7C ولا تحسب نسبة إتمام من الملفات. |
| الدليل | none-documentary-metadata |
| الحد | R4d محدود وليس كل SP03/7B؛ R4e/7B21 مقترح لا جلسة أخيرة أو مدة مضمونة. |
| المالك | مالك نطاق التدقيق والمنتج |
| المدخل المنقح | قائمة قدرات ومداخل ومصادر ومخارج متفق عليها خارج BC7 وحدّي الملصق، مع crosswalk إلى 455FE التاريخية وNV22/LC7 وسبب supported/unsupported/optional وكل split أو استبعاد. |
| الأثر إن غاب | 7B/7 جزئيتان؛ لا ختم من 477 بحثاً أو 410 مسارات أو 3 splits، ولا نقل صامت لمتطلب 7B إلى 7C. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-06; P7B20T-29;P7B20T-30; not-executed |

### FE7B20-16 / INV7B20-16 — حفظ التاريخ وصدق CLI والنتيجة

| الحقل | العقد والحد |
| --- | --- |
| المكون والتتبع | preservation/OWN modes/current CLI — freezes → OWN307/raw308CRLF/indexes → historical36 child → current32 cases |
| الملاحظة الساكنة | 553 مادة و307 صفوف وكل ALLnext_phase/evidence/rawprefix وG190 و827 أصلاً وثلاثة freezes محمية. B19 يقرأ OWN307 لا310 live؛ assertions B19 تاريخية والحالي B20 مستقل. |
| الثابت المطلوب | لا تعديل محميات أو تخطي أو disk overlay أو global patch أو rebaseline أو archive rewrite؛ stdout حقيقي لا placeholder، ولا ERP/7C/8 ضمنياً. |
| الدليل | none-documentary-metadata |
| الحد | كل32 خطة قبول not-executed؛ Python مدقق وثائق وليس ERP/C#/SQL أو ماسحاً أو طابعة أو قبول أعمال. |
| المالك | مالك التدقيق وحفظ الأدلة |
| المدخل المنقح | قائمة قدرات ومداخل ومصادر ومخارج متفق عليها خارج BC7 وحدّي الملصق، مع crosswalk إلى 455FE التاريخية وNV22/LC7 وسبب supported/unsupported/optional وكل split أو استبعاد. |
| الأثر إن غاب | 7B/7 جزئيتان؛ لا ختم من 477 بحثاً أو 410 مسارات أو 3 splits، ولا نقل صامت لمتطلب 7B إلى 7C. |
| الخطوة التالية | تثبيت العقد ثم اتباع الخطتين المرتبطتين بعد إذن مستقل؛ الباقي H/Q وSP01–03 صريح، لا إصلاح أو تشغيل ضمني. |
| الروابط والحالة | H7B20-06; P7B20T-31;P7B20T-32; not-executed |

## 6. المصالحات عبر الحدود

| العقد | القدرات | القاعدة وحدها | الخطط غير المنفذة |
| --- | --- | --- | --- |
| RC7B20-01 — نتيجة decode وهوية الوحدة | FE7B20-01;FE7B20-02;FE7B20-03;FE7B20-04;FE7B20-13 | الكمية والسعر ونوع القيمة والوحدة وhealth عقد متكامل؛ تساوي ItemId لا يصالح unit/amount/failed. لا تنفيذ أو موافقة schema/SDK/template/policy؛ الفروق معلنة لا forced equality. | P7B20T-01;P7B20T-02;P7B20T-03;P7B20T-04;P7B20T-05;P7B20T-06;P7B20T-07;P7B20T-08;P7B20T-25;P7B20T-26 |
| RC7B20-02 — المستهلك وحد الحارس | FE7B20-05;FE7B20-06;FE7B20-07;FE7B20-08;FE7B20-09 | POS ومحرر الفاتورة والبحث عن صنف التسوية ليست وظيفة واحدة؛ يعلن القصد وتفحص الكمية النهائية قبل الحارس. لا تنفيذ أو موافقة schema/SDK/template/policy؛ الفروق معلنة لا forced equality. | P7B20T-09;P7B20T-10;P7B20T-11;P7B20T-12;P7B20T-13;P7B20T-14;P7B20T-15;P7B20T-16;P7B20T-17;P7B20T-18 |
| RC7B20-03 — هوية الملصق والسعر والنسخ | FE7B20-10;FE7B20-11;FE7B20-12 | رمز الوحدة وسعره وpriceBasis/عملة/ضريبة وعدد الملصقات والوجهة وoutcome عقد إلى المصب لا DTO فقط. لا تنفيذ أو موافقة schema/SDK/template/policy؛ الفروق معلنة لا forced equality. | P7B20T-19;P7B20T-20;P7B20T-21;P7B20T-22;P7B20T-23;P7B20T-24 |
| RC7B20-04 — البقايا والحصر والتقسيم | FE7B20-14;FE7B20-15 | RS14/477 lexical/BC7/scope20 بيانات نسب ومسؤولية لا14 موافقة أو اكتمال SP03/7B. لا تنفيذ أو موافقة schema/SDK/template/policy؛ الفروق معلنة لا forced equality. | P7B20T-27;P7B20T-28;P7B20T-29;P7B20T-30 |
| RC7B20-05 — الحفظ والتاريخ والإذن | FE7B20-16 | source10ba/entryac20e31/genuineB19stdoutee393a7 هويات مستقلة؛ يحفظ التاريخ والإذن دون ERP acceptance. لا تنفيذ أو موافقة schema/SDK/template/policy؛ الفروق معلنة لا forced equality. | P7B20T-31;P7B20T-32 |

لا تقارن سعر ملصق شامل/غير شامل أو سعر عبوة أو مبلغ ميزان ممتد دون priceBasis/عملة/ضريبة/وحدة معتمدة. لا forced-equality مصطنعة بين مسارين مختلفين، ولا موافقة ACL من نتيجة lookup. تبقى P4-014/026/028 وP7-036/037 والأصول المالية والأمنية و061/131–135 كما هي، و132 potential. [كل البقايا والتقسيمات](PHASE-07-REMAINING-07B20.md) مفتوحة؛ **7B/7 جزئيتان و7C لم تبدأ و8 غير مأذونة.**
