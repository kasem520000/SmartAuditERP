# عقود طلبات المتصلين — 7B18/R4b

مرجع التدقيق المعلن **2026-11-16 UTC**، ومصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B18 يلي دفع B17 المكتمل `12d2e4b1bc566a860643b8459b16cbc85a6d2c3d` بجميع **500 ملف تدقيق**. ساعة التجميد المرصودة `2026-11-19T02:53:08.853620+00:00` منفصلة عن المرجع وليست تشغيل تطبيق.

**7B/7 جزئيتان؛ R4b سُلّم بحدوده، و R4c/7B19 مقترح؛7C لم تبدأ؛8 غير مأذونة ولم تبدأ.** لا بناء أو تشغيل ERP أو C#/SQL/VB/WPF/SDK/REPX/Office/COM، ولا مفسر أو مزود أو جهاز أو طابعة أو تصدير أعمال أو shell للتطبيق. لا بيانات أعمال حقيقية أو أسرار أو إصلاح أو قبول أو قياس تشغيلي. Python/Git لأدوات الوثائق فقط؛ `next_phase=8` ليس إذناً.

[النتيجة](PHASE-07B18.md) · [عقود المتصلين](CALLER-REQUEST-CONTRACTS-07B18.md) · [التحقق والخطط](VALIDATION-07B18.md) · [المتبقي](PHASE-07-REMAINING-07B18.md) · [scope29](review-scope-07B18.csv) · [السجل](findings.csv) · [provenance495](evidence/provenance-07B18.json) · [stdoutB18](evidence/checks-07B18.json)

## 1. عقد الطلب الذي جرى تتبعه

`الصنف + المخزن + PartyRef(id,kind) + الفترة/الفرع/عملية الحركة + health/نسخة الطلب` ليست مجرد قيم UI. تتبع هذا الجزء اختيار الطرف في الأب ثم النقل إلى LastProcess ثم radio/lookup ثم شرط SQL، دون تشغيل. الفلاتر المفقودة للمخزن 122 والترتيب 059 مستقلة عن نوع الطرف 129 ومعرفه 130. مرجع الطرف ليس مرجع المستند DocumentRef عند فتح صف 061، ولا متطلب ACL يثبت من Apply.

مالك العقد المحلي WPF/المنتج، ومدخله المنقح جدول الأنماط 1/2/3 و 4/5/14 وحالتا lookup/health وعينات هوية اصطناعية؛ غيابه يمنع اعتماد كل حالات الدعم أو التوسيع الصامت. الخطوة اللاحقة توحيد المواصفة ثم خطة قبول مأذونة، لا تعديل تطبيق الآن. تفاصيل العقود الخارجية في[H6](evidence/handoffs-07B18.csv).

## 2. دفتر المداخل المباشرة CL19

النمط `object.LastProcess(...)` فقط في 477 ملف C# أصلي خارج bin/obj. يسجل [CSV](evidence/caller-request-ledger-07B18.csv) الملف/المعالج/السطر/الوسائط الأربع/بصمة النص. اكتملت نسبة هذه **19 موضعاً نصياً** إلى السياقات التالية، لا الحصر الدلالي لكل callgraph أو كل ميزة أو وصول نشر.10 أوامر مادة عامة،7 أنماط طرف مخالفة أو مشروطة،1 شاهد مطابق،1 أمر طرف يحذف ID. قد يختار طرف 3 فيخفي مخالفة النوع.

| المعرف | الملف والمعالج / السطر | الوسيط الثالث | الرابع | السياق والحكم المحدود | الجذر |
| --- | --- | --- | --- | --- | --- |
| CL7B18-01 | frmInvInOutput.xaml.cs / StripClientLastItem_Click / 2600–2600 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | H7B18-03 |
| CL7B18-02 | frmInvInOutput.xaml.cs / StripLastItem_Click / 2618–2618 | -1 | 1 | selected-party-id-omitted — label العميل يرسل-1 رغم وجود قائمة طرف في الأب؛130 مستقل عن نوع lookup. | P7-130 |
| CL7B18-03 | frmInvInputOutput.xaml.cs / CtxItemLastActivity_Click / 1287–1288 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-04 | frmInvInputOutput.xaml.cs / CtxClientActivity_Click / 1304–1305 | custId | 2 | conditional-kind-mismatch — تتوقف المطابقة على InvType: النوع الثابت يخالف الفرع الذي يستخدم النوع الآخر؛ ليست كل الأنماط خاطئة. | P7-129 |
| CL7B18-05 | frmInvPOS.xaml.cs / CtxItemLastActivity_Click / 1224–1224 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-06 | frmInvPOS.xaml.cs / CtxClientActivity_Click / 1238–1239 | Invoic.Customer | 2 | kind-mismatch — نوع الطرف المنقول يخالف مصدر اختياره في الأب؛ يسقط قيده إذا لم يجد ID في lookup الطفل المؤهلة. | P7-129 |
| CL7B18-07 | frmInvPurch.xaml.cs / ItemLastActivity / 1149–1149 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-08 | frmInvPurch.xaml.cs / ItemClientActivity / 1165–1166 | GetSelectedId(this.cmbClient) | 2 | matching-kind-counterevidence — معرف المورد ونوع 2 منقولان مطابقين؛ لا اعتماد بقية المخزن أو الترتيب. | P7-129 |
| CL7B18-09 | frmInvSale.xaml.cs / ItemLastActivity / 1210–1210 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-10 | frmInvSale.xaml.cs / ItemClientActivity / 1226–1226 | custId | 1 | conditional-kind-mismatch — تتوقف المطابقة على InvType: النوع الثابت يخالف الفرع الذي يستخدم النوع الآخر؛ ليست كل الأنماط خاطئة. | P7-129 |
| CL7B18-11 | frmInventoryTransfer.xaml.cs / ItemLastActivity / 1473–1474 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-12 | frmPurchInv.xaml.cs / StripItemLastActivity_Click / 2431–2431 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-13 | frmPurchInv.xaml.cs / StripClientLastActivity_Click / 2444–2444 | custId | 1 | kind-mismatch — نوع الطرف المنقول يخالف مصدر اختياره في الأب؛ يسقط قيده إذا لم يجد ID في lookup الطفل المؤهلة. | P7-129 |
| CL7B18-14 | frmSalePurch.xaml.cs / StripClientLastItem_Click / 2252–2253 | Convert.ToInt32(cmbClient.SelectedValue) | 1 | kind-mismatch — نوع الطرف المنقول يخالف مصدر اختياره في الأب؛ يسقط قيده إذا لم يجد ID في lookup الطفل المؤهلة. | P7-129 |
| CL7B18-15 | frmSalePurch.xaml.cs / StripLastItem_Click / 2265–2265 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-16 | frmSalesInvoice.xaml.cs / StripClientLastItem_Click / 2550–2553 | Convert.ToInt32(cmbClient.SelectedValue) | 1 | conditional-kind-mismatch — تتوقف المطابقة على InvType: النوع الثابت يخالف الفرع الذي يستخدم النوع الآخر؛ ليست كل الأنماط خاطئة. | P7-129 |
| CL7B18-17 | frmSalesInvoice.xaml.cs / StripLastItem_Click / 2565–2567 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-18 | frmcontract.xaml.cs / ItemLastActivity / 1567–1570 | -1 | 1 | all-party-item-command — أمر مادة عام، لا طرف محدد مطلوب؛-1 مشروع في هذا السياق. يبقى 122/059 دون إعادة عد. | P7-122;P7-059 |
| CL7B18-19 | frmcontract.xaml.cs / ItemClientActivity / 1590–1593 | SafeGetSelectedValue<int>(cmbClient) | 1 | conditional-kind-mismatch — تتوقف المطابقة على InvType: النوع الثابت يخالف الفرع الذي يستخدم النوع الآخر؛ ليست كل الأنماط خاطئة. | P7-129 |

الأدلة تشير إلى المعالجات المقروءة لا كل أجسام المحررات. قائمة contract و InventoryTransfer تُنشأ runtime في الشرائح المعلنة، وبقية القوائم XAML محلي. على سبيل المثال `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1338-1374` و`SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:1358-1381`. ربط InvInOutput المضلل اسماً موثق بـ`SmartAuditERP/Form_WPF/frmInvInOutput.xaml:551-559`؛ لذا لا يُستنتج قصد الأمر من اسم function وحده.

## 3. المداخل العامة GE10 وملاحظة التهيئة

| المعرف | الملف / المعالج | عائلة التقرير | الترتيب النصي | الحد |
| --- | --- | --- | --- | --- |
| GE7B18-01 | frmcontract.xaml.cs / ItemProcess | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-02 | frmSalesInvoice.xaml.cs / StripItemProcess_Click | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-03 | frmSalePurch.xaml.cs / StripItemProcess_Click | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-04 | frmPurchInv.xaml.cs / StripItemProcess_Click | aggregate | ShowDialog-with-ItemId-no-explicit-query | هذا الأمر يستدعي التجميعي لا التفصيلي؛ لا استيراد لحكم ثمانية ShowResult إليه. |
| GE7B18-05 | frmInventoryTransfer.xaml.cs / ItemProcess | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-06 | frmInvSale.xaml.cs / ItemProcess | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-07 | frmInvPurch.xaml.cs / ItemProcess | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-08 | frmInvPOS.xaml.cs / CtxItemProcess_Click | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-09 | frmInvInputOutput.xaml.cs / CtxItemProcess_Click | detailed | query-before-ShowDialog | ShowResult يسبق ShowDialog، و Loaded يحمل التاريخ والمخزن والفرع؛ ترتيب نصي لا قضاء WPF أو سلوك DateTimeBox. |
| GE7B18-10 | frmInvInOutput.xaml.cs / StripItemProcess_Click | aggregate | ShowDialog-with-ItemId-no-explicit-query | هذا الأمر يستدعي التجميعي لا التفصيلي؛ لا استيراد لحكم ثمانية ShowResult إليه. |

المستقبل `SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:55-95` يهيئ SelectedId ثم يحمّل التاريخ والمخزن والفرع في Loaded؛ والفلاتر في`SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:253-283` مشروطة بقيم UI. الـ ShowResult قبل ShowDialog ثابت في المداخل الثمانية، لكن لا .NET منفذ أو DateTimeBox/SDK أو سياسة Ready معتمدة، لذلك تبقى 045/H03 ملاحظة عقد لا نتيجة lifecycle جديدة. هذه ليست مساواة بين ترتيب القراءة العامة وترتيب كل LastProcess الذي قد يسبقُه Show في المعالج المحلي.

توجد شواهد route إلى SalePurch في`SmartAuditERP/Form_WPF/frmInvSumByType.xaml.cs:275-307` و`SmartAuditERP/Form_WPF/frmEmpInvs.xaml.cs:435-475`، ومداخل R1 في`SmartAuditERP/Home.xaml.cs:2872-2889` و`SmartAuditERP/Home.xaml.cs:2948-2962`. لا يُستنتج منها وصول كل نافذة أو كل نمط. المداخل الخارجية إلى PurchInv/InvInOutput لم تُحسم من الشرائح.

## 4. مصفوفة القدرة/التنفيذ/الخطة وحدودها

كل صف source-trace أو بوابة وثائق محددة، لا ميزة مكتملة. FE10/13/14 وثائق نطاق؛ البقية شرائح مصدر. لا تعني حالة implemented-with-observed-defects اختباراً منفذاً. سجل 455 السابق يبقى metadata تاريخية، لا يُدمج في عد ميزات حالية.

| المعرف — العقد | المكون والمدخل | الملاحظة | الحالة / العمق | الحد | الخطط |
| --- | --- | --- | --- | --- | --- |
| FE7B18-01 — نوع الطرف بين الأب والطفل | سبعة أنماط caller، لا سبع نتائج؛ قائمة الطرف في الأب → LastProcess(id,kind) → lookup الطفل → predicate | المعرف الموجب لا يكفي مع النوع المخالف: SalePurch/PurchInv يرسلان 1 لمورد 2، و POS يرسل 2 لعميل 1. وثلاث واجهات عامة تتبدل بحسب InvType، و InputOutput يثبت 2. إذا لم يطابق المعرف قائمة الطفل، لا يُبنى شرط cust_id؛ النوع 3 قد يخفي العلة. | implemented-with-observed-defects / bounded-selected-source-request-trace-not-whole-feature | النوع المخالف مثبت نصياً؛ سقوط الفلتر مشروط بمعرف موجب من النوع 1/2 الخالص وبنجاح المصدر وتهيئة lookup. لا إثبات حادث إنتاج أو تجاوز ACL. | P7B18T-01;P7B18T-02;P7B18T-03;P7B18T-04;P7B18T-05 |
| FE7B18-02 — أمر الطرف مختلف عن أمر المادة العام | frmInvInOutput / الربط الفعلي في XAML؛ آخر حركة للعميل → StripLastItem_Click → LastProcess(...,-1,1) | يربط XAML أمر العميل بـ StripLastItem، لا بالاسم الذي يوحي به StripClientLastItem. كلا المعالجين يرسل-1؛ لا يدخل المستقبل فرع clientId>0، فيُطلب كل الأطراف حتى مع اختيار موجب في الأب. | implemented-with-observed-defects / bounded-selected-source-request-trace-not-whole-feature | الربط المحلي ثابت. مسار الوصول إلى النافذة من خارجها ونشرها غير محسومين؛ ليس كل استعمال للمعرف-1 عيباً. | P7B18T-06;P7B18T-07 |
| FE7B18-03 — المخزن الموجب لا يعطل خيار الكل | المستقبل التفصيلي؛ storeId → SelectedValue تحت chkAll → condItems | يبقى 122: chkAll يبدأ true ولا يغيره LastProcess. توثيق المتصلين لا يُنشئ نتيجة لكل نداء، وتصحيح الطرف لا يغير علم المخزن. | rechecked-prior-root-not-new-finding / bounded-selected-source-request-trace-not-whole-feature | لا افتراض سلامة نطاق المخزن من صحة PartyRef، ولا إثبات كل callers أو مخطط النشر أو الأداء. | P7B18T-08 |
| FE7B18-04 — الأحدث بعد تثبيت نطاق الطلب | المستقبل التفصيلي؛ TOP1 → ORDER BY inv.date ASC | يبقى 059: ASC يختار الأقدم لا latest. تصحيح النوع والمعرف والمخزن لا يغير الترتيب؛ تعادل التواريخ يحتاج قاعدة إضافية. | rechecked-prior-root-not-new-finding / bounded-selected-source-request-trace-not-whole-feature | مقارنة ترتيب وعضوية في نموذج مستقل، لا SQL منفذ أو تقدير رصيد كامل. | P7B18T-09 |
| FE7B18-05 — قراءة قبل Loaded ليست لقطة UI بعدها | ثمانية مداخل عامة تفصيلية؛ إنشاء/SelectedId → ShowResult → ShowDialog → Loaded | ثمانية مداخل عامة تستدعي ShowResult قبل ShowDialog؛ Window_Loaded يضبط التاريخ ويحمل المخزن والفرع. ثبت الترتيب النصي، ولم يُختبر توقيت WPF أو DateTimeBox أو تأثير الإعدادات. | reviewed-contract-unresolved-not-global-absence / bounded-selected-source-request-trace-not-whole-feature | لا حكم بأن ID أو تاريخاً مُرر فعلاً قد مُسح، ولا إثبات SQL خاطئ أو تسريب. يقارن 045/H03 دون نتيجة جديدة. | P7B18T-10 |
| FE7B18-06 — النقل المطابق والطرف المشترك شاهدان مقابلان | InvPurch / النوع 3؛ مورد 2 → LP(kind2)، ونوع 3 → قائمتي الطرف | InvPurch ينقل معرف مورد 2 ونوع 2. والطرف 3 مؤهل في قائمتي الطفل وقد يخفي مخالفة caller. لا يثبت الشاهدان سلامة بقية المخزن أو الترتيب. | counterevidence-not-global-closure / bounded-selected-source-request-trace-not-whole-feature | ضبط سببي لا اعتماد كل المشتريات أو كل قيمة في تقرير. | P7B18T-11 |
| FE7B18-07 — الواجهة العامة لا تشتق الدور من اسمها | contract / SalesInvoice / InvSale؛ InvType1 → مصدر 2، مقابل LP(kind1) ثابت | تختار الواجهات الثلاث مورد 2 عند InvType1، بينما arg4 ثابت 1. قد تتطابق الحالات البيعية؛ لا يُفترض أن كل نمط متاح من وجود الحقل. | implemented-with-observed-defects / bounded-selected-source-request-trace-not-whole-feature | مخالفة حالة InvType1 مشروطة بإتاحتها؛ لا كل واجهة اسمها Sale تحمل عميلاً دائماً. | P7B18T-12 |
| FE7B18-08 — عميل POS ليس مورداً | InvPOS؛ frmSrchClient.Type1 → Invoic.Customer → LP(kind2) | مسار الآجل يختار Type1 ويحفظ ClientId في Invoic.Customer، لكن أمر الحركة يمرر 2. نوع الطرف مستمد من مسار الاختيار لا caption المورد أو default ID. | implemented-with-observed-defects / bounded-selected-source-request-trace-not-whole-feature | لا اختبار دفع أو آجل أو حوار؛ المعرفات غير الموجبة والافتراضية لا تثبت خسارة حالية. | P7B18T-13 |
| FE7B18-09 — InputOutput: النمطان 4/14 مقابل 5 | InputOutput caller؛ مصدر 4/14→2، وإلا 1 → const2 | النوع 2 يطابق مصدر المورد في 4/14، ولا يطابق مصدر العميل في 5. الفروع المتعددة مظاهر لنفس علة النوع لا نتائج مستقلة. | implemented-with-observed-defects / bounded-selected-source-request-trace-not-whole-feature | سياسة أنواع أخرى غير 4/5/14 تحتاج support matrix؛ لا إلزام من else وحده. | P7B18T-14 |
| FE7B18-10 — نسب 19 موضعاً نصياً في 10 ملفات | caller-request-ledger19؛ بحث نصي في 477 C# أصلية → مواقع ووسائط وبصمات → شرائح مسماة | الحصر مغلق على النمط النصي object.LastProcess فقط، بالملف والسطر والأربع وسائط و SHA. ليس AST أو كل callgraph أو حصر كل قدرات التقارير، ولا يرقّي 455 metadata قديمة. | reviewed-contract-unresolved-not-global-absence / frozen-documentary-scope-contract-not-source-rereview | 477 ملف بحث لا 477 مراجعة body. المداخل عبر delegate/reflection أو غير النمط خارج هذا المقام. | P7B18T-15 |
| FE7B18-11 — الأمر التجميعي ليس التفصيلي | PurchInv / InvInOutput → aggregate؛ ItemId → frmRptItemsActivity → SQL تجميعي | المدخلان العامان يستخدمان التجميعي لا التفصيلي؛ فرع العميل في التجميعي فارغ 058. إصلاحه لا يستعيد نوعاً أو معرفاً فُقد في LP. | rechecked-prior-root-not-new-finding / bounded-selected-source-request-trace-not-whole-feature | لا يُستورد حكم ثمانية pre-load إلى هذين المدخلين؛058 يعاد فحصه ولا يعاد عده. | P7B18T-16 |
| FE7B18-12 — مرجع المستند ليس مرجع الطرف | الفتح التفصيلي مقابل inventory؛ label/localNo → فتح، مقابل GlobalID/ProcType في inventory | يبقى 061: التفصيلي يفتح بالاسم والرقم المحلي. Inventory يحمل GlobalID و ProcType كشاهد ينفي الفقد العام. هذا لا يثبت كل Navigate أو حارس حفظ أو ACL. | reviewed-contract-unresolved-not-global-absence / bounded-selected-source-request-trace-not-whole-feature | بقية Navigate والحفظ والقوالب خارج الشرائح؛ فتح مستند لا يثبت أنه read-only أو معزول الفروع. | P7B18T-17 |
| FE7B18-13 — تصرف البقايا والتقسيم بعد R4b | RS14 / SP3؛ RS/H/Q السابقة → تقدم محلي أو handoff أو split | تقدم SP01 في المداخل المباشرة المسماة فقط. SP02 للحصر الأوسع و SP03 للتفقيط والباركود باقيان.14 تصرفاً ليست 14 موافقة؛ R4b ليس كل R4. | reviewed-contract-unresolved-not-global-absence / frozen-documentary-scope-contract-not-source-rereview | R4c/B19 مقترح أو split إضافي مسبب. ستة محاور 7C لم تبدأ و 8 غير مأذونة. | P7B18T-18;P7B18T-19 |
| FE7B18-14 — حفظ 300 والأرشيف وصدق CLI | 495 مادة /300 صف /G180 /827 أصلاً؛ B17 OWN300 و 301CRLF وفهارسه الدقيقة → B18 الحالي | مصدر 10ba ودخول 12d2e4b و checkout سجل B17 الحقيقي de0e7cf هويات مختلفة. كل 300 صف و ALLnext_phase و rawprefix ثابتة، بلا extensions. ثابت PHASE7_CURRENT_CLI واجهة توافق B17؛ parser الفعلي يختار B18 ويُختبر مباشرة. | reviewed-contract-unresolved-not-global-absence / frozen-documentary-scope-contract-not-source-rereview | لا ERP أو إصلاح أو قياس أو 7C/8 من المدقق. main البرمجي B15 باقٍ للتوافق؛ لا إعادة كتابة stdout بعد الدفع. | P7B18T-20;P7B18T-21;P7B18T-22;P7B18T-23;P7B18T-24 |

الدليل المفصل لكل صف والجذور في[FE14](evidence/feature-implementation-matrix-07B18.csv)، ولا توضع إحالات source مصطنعة لبوابات النطاق. [INV14](evidence/report-invariants-07B18.csv) يقابل كل FE واحداً لواحد، و[plans24](evidence/acceptance-tests-07B18.csv) يحتفظ بالربط العكسي والجذور والأدلة وحالة not-executed.

## 5. الثوابت المطلوبة لا الاختبارات الناجحة

| المعرف | الثابت المطلوب | FE / الجذور | الخطط |
| --- | --- | --- | --- |
| INV7B18-01 | ينتقل PartyRef بمعرفه ونوعه من نفس مصدر اختيار الأب؛ لا يوسع الطفل طلباً محدداً بصمت عند عدم أهلية lookup. | FE7B18-01 / P7-129 | P7B18T-01;P7B18T-02;P7B18T-03;P7B18T-04;P7B18T-05 |
| INV7B18-02 | أمر الطرف ينقل معرفه الموجب أو يرفضه بوضوح؛ sentinel الكل خاص بطلب عام معلن. | FE7B18-02 / P7-130 | P7B18T-06;P7B18T-07 |
| INV7B18-03 | يدخل كل قيد مخزن موجب في الطلب والاستعلام أو يرفض؛ لا SelectedValue مضللة تحت خيار الكل. | FE7B18-03 / P7-122 | P7B18T-08 |
| INV7B18-04 | يطبق النطاق قبل TOP، ثم ترتيب latest وقاعدة تعادل معتمدة. | FE7B18-04 / P7-059 | P7B18T-09 |
| INV7B18-05 | يسبق ReadyRequest الصريح القراءة؛ معايير UI والنتيجة و health مرتبطة بنسخة طلب واحدة. | FE7B18-05 / P7-045;H7B18-03 | P7B18T-10 |
| INV7B18-06 | تُحفظ حالتا المورد 2 المطابق والنوع 3 كشاهدين مقابلين، دون أن تمحوا مخالفة النوعين الخالصين 1/2. | FE7B18-06 / P7-129 | P7B18T-11 |
| INV7B18-07 | قرار InvType نفسه يقود قائمة الأب ونوع الطرف المحمول، أو تُعلن الحالة unsupported. | FE7B18-07 / P7-129 | P7B18T-12 |
| INV7B18-08 | هوية عميل POS ونوعه من نفس الاختيار؛ لا يرقّى المعرف غير الصالح إلى طلب محدد. | FE7B18-08 / P7-129 | P7B18T-13 |
| INV7B18-09 | جدول الأنماط المعتمد يوحد النوع بين lookup والنقل، مع شاهد 4/14 المطابق. | FE7B18-09 / P7-129 | P7B18T-14 |
| INV7B18-10 | لا يفقد الحصر أي موضع معلن أو يكرره أو يغيره؛ تبقى حدود النمط النصي صريحة وقابلة للتوسعة. | FE7B18-10 / H7B18-06 | P7B18T-15 |
| INV7B18-11 | يفصل عقد التجميعي عن التفصيلي؛ لا مساواة نتائج بلا grain و source-set متفقين. | FE7B18-11 / P7-058 | P7B18T-16 |
| INV7B18-12 | DocumentRef يحمل source/type/GlobalID/branch/allowed-set، مستقلاً عن PartyRef و label العرض. | FE7B18-12 / P7-061;H7B18-03 | P7B18T-17 |
| INV7B18-13 | كل عنصر مختار له دليل وحد ومالك ومدخل منقح وأثر وخطوة وخطة؛ الخارج handoff أو split صريح، لا بدء 7C ضمني. | FE7B18-13 / H7B18-06 | P7B18T-18;P7B18T-19 |
| INV7B18-14 | تُحفظ الأرشيفات والهويات والمدخلات OWN؛ current/default الفعلي B18 و historical B17 معزولان مع بقاء API B15. | FE7B18-14 / H7B18-06 | P7B18T-20;P7B18T-21;P7B18T-22;P7B18T-23;P7B18T-24 |

## 6. عقود المصالحة الأربعة

لا مساواة مفروضة بين التجميعي والتفصيلي أو دفتر المخزون وبين GL دون قاموس grain/source-set/unit/sign/currency/period/health. لا قبول أرقام أو دقة أو ACL من نجاح فحص CSV.

### RC7B18-01 — PartyRef(id,kind) قبل الفلتر

قائمة الأب والمعرف والنوع و lookup و query عقد واحد. نوع مخالف 129 ومعرف محذوف 130 علتان تعزلان بتغيير component مستقل؛ النوع 3 شاهد إخفاء. لا all-party صامت لطلب محدد.

**الربط:** FE7B18-01;FE7B18-02;FE7B18-06;FE7B18-07;FE7B18-08;FE7B18-09؛ الجذور P7-129;P7-130؛ الخطط P7B18T-01;P7B18T-02;P7B18T-03;P7B18T-04;P7B18T-05;P7B18T-06;P7B18T-07;P7B18T-11;P7B18T-12;P7B18T-13;P7B18T-14. **التشغيل:**not-executed.

### RC7B18-02 — النطاق و Ready والترتيب

تصحيح PartyRef لا يصلح 122/059. يُثبت المخزن والفرع والفترة و health قبل TOP واللقطة؛ pre-Loaded ترتيب نصي محدود لا ACL أو توقيت WPF مقاس.

**الربط:** FE7B18-03;FE7B18-04;FE7B18-05؛ الجذور P7-122;P7-059;P7-045;H7B18-03؛ الخطط P7B18T-08;P7B18T-09;P7B18T-10. **التشغيل:**not-executed.

### RC7B18-03 — مرجع المستند وعائلة التقرير

التجميعي والتفصيلي عقدان مختلفان؛ PartyRef ليس DocumentRef. GlobalID شاهد جزئي لا كل navigator أو saveguard أو صلاحية؛ لا forced-equality بين grain مختلف.

**الربط:** FE7B18-11;FE7B18-12؛ الجذور P7-058;P7-061;H7B18-03؛ الخطط P7B18T-16;P7B18T-17. **التشغيل:**not-executed.

### RC7B18-04 — الحصر والبقايا والحفظ والإذن

CL19/10 و GE10 ليست كل callgraph؛455 metadata محفوظة لا مراجعة حالية. البقايا والملاك و splits والأرشيف و OWN وحد الإذن مطالب مستقلة، لا اكتمال 7B بالعد.

**الربط:** FE7B18-10;FE7B18-13;FE7B18-14؛ الجذور H7B18-06؛ الخطط P7B18T-15;P7B18T-18;P7B18T-19;P7B18T-20;P7B18T-21;P7B18T-22;P7B18T-23;P7B18T-24. **التشغيل:**not-executed.

## 7. الشواهد المقابلة والبوابات

InvPurch ينقل مورد 2 مع kind2، والنوع 3 مؤهل في القائمتين، وأمر المادة العام قد يطلب-1 بحق. هذه الشواهد تمنع تعميم 129/130 على كل نداء. يبقى علم المخزن 122 و ASC059 حتى مع الطرف الصحيح. يحمل inventory GlobalID و ProcType في`SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-508` و`SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:545-639` و`SmartAuditERP/Form_WPF/frmRptInventory.xaml:453-489`، خلاف فتح التفصيلي في`SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1045`؛ ليس ذلك اعتماداً لكل Navigate أو saveguard.

الملاك والمدخلات والأثر والخطوة في[RS14](evidence/residual-disposition-07B18.csv) و[المتبقي](PHASE-07-REMAINING-07B18.md). externalmanifest/DTO/schema/grants/support/culture والعقود المالية غير معتمدة. لا يفسر SelectedIndex=-1 بأنه empty ناجح أوأن الطلب المحدد يسمح بالكل.24 خطة لاحقة غير منفذة، ولا 7C/8 ضمنياً.
