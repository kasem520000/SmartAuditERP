# عقود التوجيه والاستقبال والحفظ — 7B19/R4c

مرجع التدقيق المعلن **2026-11-16 UTC**. مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B19 يلي دفع B18 المكتمل `ee393a741a862a605c6c2f688d3f634bd91856ae` بجميع **528 ملف تدقيق**. ساعة التجميد المرصودة `2026-11-19T03:37:39.154596+00:00` مستقلة عن المرجع، لا تشغيل تطبيق في أي منهما.

**7B/7 جزئيتان؛ R4c سُلّم بحدوده لا كل R4، وR4d/7B20 مقترح؛7C لم تبدأ؛8 غير مأذونة ولم تبدأ.** لا تشغيل أو بناء ERP/C#/SQL/VB/WPF/SDK/DTO/REPX/Office/COM أو مفسر أو مزود أو جهاز أو طابعة أو تصدير أعمال أو shell للتطبيق. لا بيانات أعمال حقيقية أو أسرار أو إصلاح أو قبول أو قياس تشغيلي. Python/Git لأدوات الوثائق فقط؛ `next_phase=8` ليس إذناً.

[النتيجة](PHASE-07B19.md) · [عقود التوجيه والاستقبال](NAVIGATION-CONTRACTS-07B19.md) · [التحقق والخطط](VALIDATION-07B19.md) · [المتبقي](PHASE-07-REMAINING-07B19.md) · [scope23](review-scope-07B19.csv) · [السجل](findings.csv) · [provenance523](evidence/provenance-07B19.json) · [stdoutB19](evidence/checks-07B19.json)

## 1. نموذج الطلب وحد الحصر

```
صف التقرير + discriminator
  → طلب مصدر وهوية (لا SQL حر ولا label كهوية مقترحة)
  → حالة new/existing + التهيئة والتحميل وصحة النتيجة
  → محرر بمرجع/جيل وحارس dirty/cancel عند إعادة الاستعمال
  → حافة حفظ مفوضة ومفحوصة + تاريخ/وحدات/دقة محفوظة
  → نتيجة حفظ صريحة، ثم إخراج مستقل بعقده
```

هذا نموذج مطلوب لا إصلاح مطبق. الشيفرة الحالية تنقل نصSQL إلىNavigate. الحصر للمواضع النصية المسماة فقط؛ لا يحلreflection/keyboard/delegates/conditional compilation أو كلcallgraph. الشاهدlexical وليسC#AST؛ لا يفهم التعليقات عموماً. روجعت المواضع المسجلة في الشرائح بوصفها نداءات نصية فعالة، لاcompiler منفذاً.

في التفصيلي14 موضعاً تستعملlabel/localNo، معaliases لمرتجع المبيعات والتسوية. في المخزون8 حالاتSelectedIndex0…7 تتقاسم5helpers وتأخذGlobalID/ProcType منrow. ترتيبconfigure→Navigate→Show مختلف نصياً عنShow→Navigate، لكنه لا يشهد بإتمامLoaded. Production وSafe قارئان خاصان لاInvoiceDGV موحداً.

## 2. دفتر NV22 — حالات توجيه، لا22موضعاً مستقلاً

[CSV](evidence/navigation-ledger-07B19.csv) يحفظ الملف والسطرين وبصمة النص المفكوك ووسيطquery كاملاً وخريطةLC والمالك والمدخل والأثر والخطوة والحد. البصمة ليستcompilerhash أوquery منفذة؛ نوعاInv/Proc أدناه من الطلب لا سياسة منتج معتمدة.

| المعرف / الأب | التمييز | المستقبل / LC | Inv / Proc في الطلب | حافة النص | الجذور والحد |
| --- | --- | --- | --- | --- | --- |
| NV7B19-01 / detailed | فاتورة مبيعات | frmInvSale / LC7B19-01 | 2 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1042-1043 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-02 / detailed | مرتجع مبيعات / مرتجع مبيعات بمسافة | frmInvSale / LC7B19-01 | 2 / 2 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1053-1054 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-03 / detailed | فاتورة مشتريات | frmInvPurch / LC7B19-02 | 1 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1062-1063 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-04 / detailed | مرتجع مشتريات | frmInvPurch / LC7B19-02 | 1 / 2 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1072-1073 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-05 / detailed | نقطة بيع | frmInvPOS / LC7B19-03 | 3 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1081-1082 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-06 / detailed | مرتجع نقطة بيع | frmInvPOS / LC7B19-03 | 3 / 2 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1090-1091 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-07 / detailed | بضاعة أول مدة | frmInvPurch / LC7B19-02 | 9 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1100-1101 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-08 / detailed | فاتورة الإدخال | frmInvInputOutput / LC7B19-04 | 4 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1109-1110 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-09 / detailed | فاتورة الإخراج | frmInvInputOutput / LC7B19-04 | 5 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1119-1120 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-10 / detailed | إنتاج | frmProductionOrder / LC7B19-05 | 6 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1127-1128 | P7-061;P7-133;P7-134;P4-020;P4-021 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-11 / detailed | مستهلك في الإنتاج | frmProductionOrder / LC7B19-05 | 6 / 2 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1135-1136 | P7-061;P7-133;P7-134;P4-020;P4-021 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-12 / detailed | مناقلة إلى | frmInventoryTransfer / LC7B19-06 | 8 / 1 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1143-1144 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-13 / detailed | مناقلة من | frmInventoryTransfer / LC7B19-06 | 8 / 2 | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1151-1152 | P7-061;P7-132 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-14 / detailed | تسوية جردية مدخلة / مخرجة | frmSafeAdjust / LC7B19-07 | SafesAdjust / not-in-query | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1160-1160 | P7-061;H7B19-03 — اسم عربي/رقم محلي؛ alias لا route جديد. قارئ5 أوراق يعيد reset في Loaded مشروطاً بنجاح الوصول؛ production/safe لهما قارئ خاص، لا تعميم ISNew عليهما. |
| NV7B19-15 / inventory | cmbType.SelectedIndex=0 | frmInventoryTransfer / LC7B19-06 | 8 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:563-565 | P4-019 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-16 / inventory | cmbType.SelectedIndex=1 | frmInventoryTransfer / LC7B19-06 | 8 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:563-565 | P4-019 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-17 / inventory | cmbType.SelectedIndex=2 | frmInvPurch / LC7B19-02 | 9 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:585-587 | H7B19-03 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-18 / inventory | cmbType.SelectedIndex=3 | frmInvInputOutput / LC7B19-04 | 4 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:606-608 | H7B19-03 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-19 / inventory | cmbType.SelectedIndex=4 | frmInvInputOutput / LC7B19-04 | 5 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:606-608 | H7B19-03 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-20 / inventory | cmbType.SelectedIndex=5 | frmProductionOrder / LC7B19-05 | 6 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:620-622 | P7-133;P7-134;P4-020;P4-021 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-21 / inventory | cmbType.SelectedIndex=6 | frmInvInputOutput / LC7B19-04 | 14 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:606-608 | H7B19-03 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |
| NV7B19-22 / inventory | cmbType.SelectedIndex=7 | frmSafeAdjust / LC7B19-07 | 7 / row.ProcType | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:630-632 | P7-131 — يفرق GlobalID عن رقم العرض؛ discriminator من قائمة النوع الحالية لا row type. Show قبل Navigate ليس إثبات اكتمال Loaded أو ACL. request/table خطأ في safe مستقل عن ترتيب العرض. |

لكلNV فيCSV مالك ومدخل وأثر وخطوة وnot-executed. المشترك بينها: مالكWPF وعقد المستند؛ مدخلDocumentRef/source/type/globalId/branch وsupport/allowed-set وسياسةinit/load منقحة؛ غيابه يحجب اعتماد المحرر والعزل والحفظ. ثم إثبات الطلب والحالة والرفض لاحقاً بإذن. لا يختزل ذلك العقود الخارجية إلى موافقات.

## 3. أوراق الاستقبال السبعة — حدود مسماة لا محررات كاملة

### LC7B19-01 — frmInvSale

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→CLR→BindingInvoice→BindingDGV/Controls |
| غياب الصف أو الفشل | غياب/استثناء المحمل يعيد null ثم نموذجاً جديداً و CLR؛ لا health مستقل. |
| التهيئة ودورة النشر | Loaded→ResetInvoice يعيد ISNew=true والفرع/التاريخ/الطرف؛ التوقيت لم ينفذ. |
| حارس المسودة | CheckBeforeClear موجود في helper المسمى؛ Navigate العام لا يستدعيه. لم تتوسع المراجعة إلى كل Closing أو كل أوامر النافذة. |
| حافة الحفظ | ValidateInvoice و period في زري الحفظ؛ SaveAndPrint يتحقق إلكتروني/allowEdit بشروط PaymentStatus/IsUpdated، ثم Mapping/SaveInvoice. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-132;P3-001;P1-013؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1663-1682`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:123-235`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1610`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2537-2570`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1860-1912`.

### LC7B19-02 — frmInvPurch

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→CLR→BindingInvoice→BindingDGV/Controls |
| غياب الصف أو الفشل | غياب/استثناء المحمل null ثم CLR؛ لا تمييز loading-failed من no-row. |
| التهيئة ودورة النشر | Loaded→ResetInvoice يعيد ISNew=true والفرع؛ inventory Show-before-Navigate شاهد ترتيب مصدري لا إثبات WPF. |
| حارس المسودة | toolbar يفحص CheckBeforeClear؛ النافذة من التقرير new لا مسودة receiver قديمة مثبتة. |
| حافة الحفظ | btnSave يفحص period/net/confirmation و btnSavePrint يفحص items/qty؛ SaveAndPrint يستدعي الكاتب؛ تفاوت P4-031 باقٍ، لا ACL جديد من الواجهة. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-132;P4-031;P3-001؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-504`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:506-546`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:97-160`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-407`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1196-1335`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1571-1589`.

### LC7B19-03 — frmInvPOS

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→CLR→BindingInvoice→BindingDGV/Controls |
| غياب الصف أو الفشل | المحمل null ينشئ نموذجاً جديداً؛ CLR نفسه يعيد InvType3/ProcType1 قبل الربط؛ لا تنسب ProcType2 للواجهة كلها. |
| التهيئة ودورة النشر | Loaded يثبت InvType3/ProcType1 وينادي ResetInvoice؛ ISNew=true قد يغطي المحمل إذا جاء لاحقاً. |
| حارس المسودة | CheckBeforeClear موجود بشرائطه في helper المسمى؛ لا فقد مسودة من fresh-window مفترض، ولا مراجعة لكل Closing أوcaller. |
| حافة الحفظ | btnPay يقرأ الفترة/EmpNo/تعديل المدفوع؛ PayBill إلكتروني ومندوب/طرف؛ SaveAndPrint يستبدل التاريخ في غير الإلكتروني الموجود ويستدعي SaveInvoice. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-132;P7-135;P3-001؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1861-1881`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:621-641`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:210-270`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:512-553`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2012-2056`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2170-2211`.

### LC7B19-04 — frmInvInputOutput

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→CLR→BindingInvoice→RefreshGrid/BindingControls |
| غياب الصف أو الفشل | غياب/استثناء المحمل null ثم نموذج جديد؛ ضبط القوائم مشروط بوجود ItemsSource. |
| التهيئة ودورة النشر | Loaded→ResetInvoice يعيد ISNew=true و branch الجلسة؛ الحارس UI يطبق IsNew=true قبل الربط. |
| حارس المسودة | toolbar يفحص CheckBeforeClear؛ publicNavigate بلا حارس داخلي؛ لا تحرير قائم لنفس النافذة في caller المختار. |
| حافة الحفظ | Save يفحص period/net إلانوع9؛ SavePrint مسار مختلف ثم SaveAndPrint/Mapping/SaveInvoice؛ ليس وصولاً مأذوناً مثبتاً. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-132;P3-001;P2-006؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:483-500`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:502-618`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:690-710`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:94-130`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:162-201`.

### LC7B19-05 — frmProductionOrder

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→SqlCommand→ReadData رأس Inv ثم Inv_Sub(productId0/>0) |
| غياب الصف أو الفشل | لا صف→CLR؛ قراءات حقول فرعية catch؛ _isLoaded يحجب unit/selection أثناء القراءة. |
| التهيئة ودورة النشر | Loaded يحمل القوائم/رقماً/تواريخ؛ ليس InvoiceDGV ResetInvoice، فلا تعميم ISNew الخاص بالخمس. |
| حارس المسودة | Navigate العام لا CheckBeforeClear و new/toolbar مباشر؛ fresh caller لا يثبت فقد مسودة مستخدم. |
| حافة الحفظ | زرSave/SavePrint→Save؛ كميات قد تقارن StockQty؛ P4-020 يحجب عقد المعاملات و P4-021 يبقي هوية التعديل محتملة؛ لا حفظ ناجح معتمد. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-133;P7-134;P4-020;P4-021;P4-022؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:854-884`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:100-124`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1026-1070`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1274-1335`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1352-1423`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497`.

### LC7B19-06 — frmInventoryTransfer

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→CLR (شرط _isLoading)→BindingInvoice→BindingDGV/Controls ثم قرين Inv |
| غياب الصف أو الفشل | null→نموذج جديد والعودة؛ قرين النصف الآخر يطلب Inv/Reff_No، لا pairing مفروض في schema مثبت. |
| التهيئة ودورة النشر | Loaded→ResetInvoice يعيد ISNew=true؛ _isLoading ليس حارس loaded-document في reset. |
| حارس المسودة | CheckBeforeClear في toolbar/new؛ Navigate العام لا؛ fresh windows المختارة ليست نافذة تحرير مشتركة. |
| حافة الحفظ | SaveReceive/SaveSend ثم async void SaveAndPrint؛ لا نتيجة نجاح مشتركة للجانبين، P4-019 باقٍ ولا ينشأ root جديد. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-132;P4-019;P3-001؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml:1-18`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:126-160`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:286-328`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:523-544`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:797-1029`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:1520-1563`.

### LC7B19-07 — frmSafeAdjust

| الحافة | الملاحظة والحد |
| --- | --- |
| الدخول والقارئ | Navigate→SqlCommand→ReadData صف SafesAdjust ثم SafesAdjust_Sub |
| غياب الصف أو الفشل | لا صف يعود دون CLR؛ استثناء قارئ يعرض رسالة بعد تعيين Code/date وربما قبل البنود. |
| التهيئة ودورة النشر | Loaded يعبئ status/safe ويغير التاريخ/الرقم، لا ResetInvoice ولا type2 تلقائي من report. |
| حارس المسودة | لا حارس dirty داخل Navigate؛ النوافذ جديدة. أوامر الاعتماد تمنع حالة معتمدة أو غير محفوظة بشروطها. |
| حافة الحفظ | btnSave→AdjustStock و btnExecute→SaveAndPrint→BindToInvoice→SaveInvoice(true). ExecuteAdjustment ليس المسار النشط المثبت. P4-017/018 باقيا الحدود. |
| المالك | مالك WPF والمحرر والمحاسب/المخزون بحسب المستند |
| المدخل المنقح | عقد typed DocumentRef والتهيئة/الحفظ/الإلغاء ودقة وسياسة الفرع، ونسخ schema/SDK منقحة. |
| الأثر إن غاب | لا تصديق للهوية أو صلاحية أو مصالحة مالية أو حفظ ناجح من هذه المقاطع. |
| الخطوة | إثبات الطلب/الحالة/الفشل والرفض في بيئة مأذونة لاحقاً؛ لا تعدل المصدر الآن. |
| الحد | سبع أوراق بشرائح named Navigate/reader/lifecycle/save-boundary فقط، ليست سبعة محررات كاملة أو كلcallers/الكتّاب أو محور7C. |

**الجذور:**P7-131;P4-017;P4-018؛ **الحالة:**not-executed.

**الأدلة:** `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1096-1103`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:113-151`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:908-979`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1368-1418`.

## 4. مصفوفة18قدرة/عقد وثوابتها وخططها

FE01–15 تتبعات مصدرية منتقاة؛FE16–18 بوابات وثائقية لقالب أو نطاق أو حفظ، بـ`none-documentary-metadata` صريح لا سطرمصدر مصطنع. لا يكفيimplemented لتسمية الميزة صحيحة؛status يصرح بعيب أو احتمال أو عقد خارجي غير محسوم.

| FE والعنوان والمسار | التنفيذ الملاحظ | الثابت المطلوب | الدليل والحد | القبول غير المنفذ |
| --- | --- | --- | --- | --- |
| FE7B19-01 — عقد رأس التسوية<br>OpenSafeAdjust→Navigate→Is_Approved→Adjust_id | implemented-with-observed-defects — طلب قائمة المخزون يقرأ Inv بينما ReadData يطلب Is_Approved ثم SafesAdjust_Sub. المسار التفصيلي يرسل SafesAdjust كشاهد توافق اسم المصدر، لا كقبول كامل. | INV7B19-01 — طلب التسوية يحمل هوية مصدرها وحقولها المتوافقة، أو يرفض قبل ملء محرر آخر جزئياً. | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206;SmartAuditERP/Properties/Resources.resx:954-1017;SmartAuditERP/Properties/Resources.resx:1692-1726<br>المؤكد اختلاف عقد المصدر المرفق؛ لا جزم بوقوع خطأ منشور أو خلو قاعدة نشر بعينها من عمود إضافي. | P7B19T-01;P7B19T-02 |
| FE7B19-02 — التهيئة لا تستبدل المستند المحمل<br>configure/Navigate→Show→Loaded/reset | implemented-with-conditional-risk — ينفذ التفصيلي configure/Navigate قبل Show. خمسة Loaded مربوطة بـ ResetInvoice يعيد ISNew=true وفرع الجلسة. خطر تبدل حالة الموجود مشروط بالتحميل وترتيب الأحداث، وليس نسخة محفوظة مثبتة. | INV7B19-02 — تهيئة المستند الجديد لا تعمل بعد تحميل مستند موجود؛ تنشر الواجهة مرجع الطلب وحالة التحرير نفسها بعد Loaded. | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmInvSale.xaml:1-16;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:123-235;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1610;SmartAuditERP/Form_WPF/frmInvPurch.xaml:1-16;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:97-160;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-407;SmartAuditERP/Form_WPF/frmInvPOS.xaml:1-16;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:210-270;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:512-553;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml:1-16;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:94-130;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:162-201;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml:1-18;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:126-160;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:286-328;SmartAuditERP/Class/InvoiceOper.cs:3219-3281<br>P7-132 محتملة: لم ينفذ WPF/DevExpress/DTO أو ترتيب الأحداث؛ قد يفشل الإعداد قبل بلوغ reset. لا ادعاء فقد بنود أو تجاوز ACL فعلي. | P7B19T-03;P7B19T-04 |
| FE7B19-03 — معامل الوصفة بعد إعادة الفتح<br>ReadData→initializer ناقص BaseQty→أحداث qty/unit | implemented-with-observed-defects — يعيد القارئ Qty/Price ولا BaseQty أو UnitEquality. النوع المحلي يبدأ BaseQty=0 وUnitEquality=1؛ حدث الكمية يتجاوز المكون بحارس BaseQty>0، وحدث الوحدة قد يضرب الصفر. | INV7B19-03 — تعاد معاملات الوصفة والوحدة اللازمة من مصدر موثوق أو يمنع التحرير المشتق؛ لا تجاوز صامت لإعادة التحجيم ولا تصفير للمكونات. | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511<br>حدث الكمية لا يصفر عند BaseQty=0 بسبب الحارس. تصفير حدث الوحدة مشروط باختيار وحدة ووجود perc وبعد التحميل؛ لا حفظ ناجح مفترض مع P4-020. | P7B19T-05;P7B19T-06 |
| FE7B19-04 — دقة تحميل مكونات الإنتاج<br>Inv_Sub.val1/exchange_price→Math.Round→Qty/Price/Total | implemented-with-observed-defects — تقريب val1 وexchange_price إلى منزلتين يسبق إنشاء ProductionItemRow ومجموعه. كمية 0.004 تصير صفراً في النموذج قبل أي StringFormat أو حفظ. | INV7B19-04 — التحميل يعيد دقة المصدر إلى نموذج التحرير؛ تنسيق العرض لا يبدل كمية أو سعراً أو مجموعاً محفوظاً. | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497<br>المؤكد تحويل مبكر في المصدر، لا خطأ بيانات نشر شوهد. سياسة الدقة خارجية، وحاجزا P4-020/021 للحفظ والهوية لم يعالجا. | P7B19T-07;P7B19T-08 |
| FE7B19-05 — تاريخ إعادة حفظ POS<br>BindingControls→period(old)→Mapping→Now→SaveInvoice | implemented-with-observed-defects — يستبدل SaveAndPrint تاريخ الموجود بـ DateTime.Now حين !EnableE_Invoice، بعد فحص txtDate_Value المحمل. SaveInvoice يمرر القيمة إلى @date ويستعملها UpdateInv. | INV7B19-05 — تاريخ الإصدار لا يصير وقت التعديل تلقائياً؛ يفصل modified-at عنه، وأي تصحيح تاريخ مقصود له عقد وفترة وهوية واضحان. | SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1009-1028;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2170-2211;SmartAuditERP/Class/InvoiceOper.cs:1497-1535;SmartAuditERP/Class/StoredQueries.cs:6-10;SmartAuditERP/Class/InvoiceOper.cs:4186-4248<br>مشروط بالنمط غير الإلكتروني والسماح بالوصول للحفظ ونجاحه. الموجود الإلكتروني شاهد خارج الفرع. حارس الفترة P3-001 المعروف مستقل، ولا خسارة منشورة أو حكم قانوني مثبت. | P7B19T-09;P7B19T-10 |
| FE7B19-06 — هوية المستند لا label/رقم<br>row→dispatcher→DocumentRef | retained-prior-defect-not-recounted — P7-061 معادة بحدودها: التفصيلي يوجه باسم العرض والرقم المحلي دون فرع، والمخزون يحمل GlobalID وProcType. لا يصحح GlobalID مصدر safe ولا يثبت الإذن. | INV7B19-06 — مرجع المستند typed يحمل source/type/globalId/branch وإصدار الطلب، مستقلاً عن label وبداخل allowed-set. | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:285-309;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmRptInventory.xaml:454-486;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml:708-720<br>لا ترتيب أول صف SQL منفذ ولا حالة لغة منشورة مثبتة. سياسة الأنماط والأسماء المدعومة عند مالك المنتج. | P7B19T-11;P7B19T-12 |
| FE7B19-07 — حراس UI لا تثبت تفويض الحفظ<br>Apply UI→selected command→writer boundary | external-authorization-contract-unresolved — ضبط Add/Edit جزئي على أزرار WPF، وأصول التوقيت والأوامر البديلة والصلاحيات معروفة سابقاً. غياب Apply في safe أو التفصيلي ليس برهان تجاوز ACL جديداً. | INV7B19-07 — هوية المستخدم والأمر والكيان والفرع تتحقق في حد موثوق؛ لا يحول flag واجهة عملية update إلى create لتغيير قرار الإذن. | SmartAuditERP/Class/Common.cs:1435-1490;SmartAuditERP/Class/FormPermission.cs:38-178<br>لا منح أو أدوار نشر أو اختبار رفض فعلي. الواجهة قرينة محدودة، ولا إعادة عد لأصول 1/2. | P7B19T-13;P7B19T-14 |
| FE7B19-08 — حارس المسودة وحد نشر جديد<br>fresh-window مقابل إعادةاستخدامreceiver | bounded-counterevidence-not-absence-proof — لا تستدعي مقاطع Navigate المختارة CheckBeforeClear داخلياً، لكن الآباء ينشئون نافذة جديدة وبعض toolbar يحرس. لذلك لا نتيجة جديدة لفقد مسودة من هذه الحقيقة وحدها. | INV7B19-08 — عند إعادة استعمال محرر تحدد سياسة dirty/cancel قبل CLR؛ فتح نافذة جديدة لا يثبت فقد مسودة مستقبل قديمة. | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1663-1682;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:506-546;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:523-544;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661<br>ليست كل المداخل أو سيناريو إعادة استعمال محرر. لم يثبت نقل مسودة من الأب إلى الطفل في المسار المختار. | P7B19T-15;P7B19T-16 |
| FE7B19-09 — صحة المحمل: لا صف أم فشل<br>reader→null→CLR/new | bounded-source-health-contract-unresolved — يضع BindingInvoice الحالة ISNew=false عند صف موجود، وnull عند غياب الصف أو الاستثناء. بعض الأوراق تفرغ إلى جديد؛ no-row وloading-failed ليسا صحة واحدة. | INV7B19-09 — نتيجة التحميل تميز found/not-found/failed وتحمل مرجع الطلب؛ الفشل لا يخلط حالة جديد مع هوية مستند مطلوب. | SmartAuditERP/Class/InvoiceOper.cs:3219-3281;SmartAuditERP/Class/InvoiceOper.cs:3496-3509;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-504;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:483-500;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1861-1881<br>هذه قراءة لعقد null الحالي لا finding عددية أخرى. provider والحقول الخارجية وسلوك DTO غير معتمدة. | P7B19T-17;P7B19T-18 |
| FE7B19-10 — النمط المدعوم والمرجع المصدرّي<br>language/index/proc/source→leaf | support-matrix-external-unresolved — التفصيلي switch لأسماء عربية بلا رسالة default، والمخزون switch لـSelectedIndex الحالي. لا يعني هذا أن كل نوع غير ظاهر قدرة واجبة أو أن كل route معتمد. | INV7B19-10 — كل نوع ومصدر وعملية مطلوب إما مدعوم بعقد صريح أو مرفوض بسبب؛ لا اشتقاق سياسة المنتج من label أو رقم نوع وحده. | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:100-124;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:113-151<br>لم ترد support matrix. production وsafe قارئان خاصان، فلا تعمم عليهما حالة ISNew للأوراق الخمس. | P7B19T-19;P7B19T-20 |
| FE7B19-11 — حراس حفظ محددة لا كامل السياسة<br>buttons→validation/pay→SaveAndPrint | retained-prior-guards-with-open-boundaries — توجد حراس حقيقية للطرف والمندوب وبعض حالات التعديل والدفع. تفاوت زري المشتريات P4-031 وحارس الفترة P3-001 باقيان؛ لا صحة مالية من قراءة حافة الحفظ. | INV7B19-11 — تتكافأ قواعد Save/SavePrint/Pay والمسارات البديلة في الحد الموثوق، ولا تساوي حراس UI قبولاً مالياً أو تفويضاً كاملاً. | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2537-2570;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1860-1912;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1196-1335;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2012-2056;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:502-618;SmartAuditERP/Class/Common.cs:1271-1301<br>لا تشغيل .NET ولا سياسة حسابات مفترضة ولا إثبات كل الأذونات داخل DLL. أصول الإذن والفترة ليست جديدة. | P7B19T-21;P7B19T-22 |
| FE7B19-12 — نتيجة حفظ المناقلة<br>SaveAndPrint calls→state/second-side | retained-prior-defect-not-recounted — استدعاءات SaveAndPrint متعددة وبوابتان مختلفتان للحفظ والطباعة؛ P4-019 باقية. عقد Navigate أو ربط القرين لا يصلح ذرية جانبي المناقلة. | INV7B19-12 — اعتماد طرفي المناقلة له نتيجة واحدة محددة وفشل وإلغاء ذريان؛ المرجع بين طرفين ليس دليل اعتماد كليهما. | SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:797-1029;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:1520-1563;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451<br>لا معاملات SQL أو مخزون أو مزود منفذ. النتائج البعيدة للمزامنة خارج حدود هذا التتبع. | P7B19T-23;P7B19T-24 |
| FE7B19-13 — اعتماد التسوية الفعلي<br>btnExecute→SaveAndPrint→BindToInvoice | retained-prior-defect-not-recounted — btnSave يفحص الحالة المعتمدة؛ btnExecute يفحص مسودة وحيدة ثم SaveAndPrint/BindToInvoice. أصول P4-017/018 باقية، وخطأ مصدر الطلب 131 مستقل. | INV7B19-13 — اعتماد التسوية وحركتها نتيجة موحدة لا تتقدم قبل نجاح الحفظ؛ مصدر القراءة وحالتها لا يختلطان برأس Inv آخر. | SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1368-1418;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:908-979;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635<br>لم يعاد تدقيق كل AdjustStock/Delete في B19. ExecuteAdjustment ليس المدخل النشط المثبت، فلا يستبدل به مسار الزر. | P7B19T-25;P7B19T-26 |
| FE7B19-14 — حاجز الإنتاج والهوية والتحويل القديم<br>Read→Save inputs→parameter/identity boundaries | retained-prior-defects-not-recounted — P4-020 نقص معاملات قبل commit، وP4-021 تخصيص هوية جديدة عند update محتمل بعد الحاجز، وP4-022 تقارن معاملي تحويل مع BaseQty موجب. 133/134 سببا reader مستقلان. | INV7B19-14 — لا يرقى binding إلى حفظ ناجح؛ يفحص كل حاجز مستقلاً مع الهوية وعدد الصفوف وتكافؤ وحدات السطر. | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1274-1335;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1352-1423;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Class/StoredQueries.cs:6-10<br>لم ينفذ إصلاح لتجاوز الحاجز أو اختبار بنود يتيمة. قيود النشر وDTO وسياسة الوصفة خارجية. | P7B19T-27;P7B19T-28 |
| FE7B19-15 — سياسة الدقة ووحدة الوصفة<br>raw quantity/price/unit→edit/display/persist | external-policy-unresolved — 133 فقد معامل إعادة البناء و134 تقريب في reader. الدقة ووحدة الوصفة المقصودتان تحتاجان قاموساً، ولا تستنتجان من N2 أو بلد المستخدم. | INV7B19-15 — قاموس quantity/price/currency/unit/base/equality/rounding ومصدر BOM/as-of صريح؛ العرض لا يمحو raw ولا يستبدل الوصفة التاريخية بالحالية بصمت. | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511<br>لا طلب لقاعدة إنتاج أو وصفة أعمال حقيقية؛ float في المخطط المرفق ليس سياسة دقة معتمدة. | P7B19T-29;P7B19T-30 |
| FE7B19-16 — مخرجات الطباعة الخارجية<br>editor load/save→Print الخارجي غيرموسع | external-template-contract-unresolved — لم يراجع B19 كل BindToData/Report/REPX. تبقى manifest والأنواع وoutcome في H02 وSP01؛ فتح المصدر ليس موافقة على ورقة مطبوعة. | INV7B19-16 — لكل مخرج manifest/version/hash/DTO/table/fieldtypes وسياسة snapshot/copies/printer/outcome قابلة للتحقق. | none-documentary-metadata<br>لا SDK أو مزود أو طابعة أو PDF أو wire-schema مستورد هنا؛ لا نتيجة جديدة لكل قالب غير مرفق. | P7B19T-31;P7B19T-32 |
| FE7B19-17 — حصر قدرات صادق من NV22/LC7<br>scope/reason/exclusions→historicalFE455 cross-reference | documentary-scope-gate — NV22 حالات توجيه من 19 موضعاً نصياً في والدين إلى 7 أوراق. ليست مجموع الميزات أو callgraph؛455 صف FE تاريخياً محفوظة ولم تعد مراجعة أجسامها. | INV7B19-17 — كل قدرة داخل عينة B19 لها مدخل ومصدر ومخرج ودليل وحد ومالك وخطوة وخطة؛ الخارج مسمى في split بسبب ومعيار خروج. | none-documentary-metadata<br>23 مساراً بشرائح ليست مقام اكتمال أو 23 body review. سُلّم R4c محدوداً لا كل R4 أو7B. | P7B19T-33;P7B19T-34 |
| FE7B19-18 — حفظ التاريخ والأرشيف والإذن<br>OWN302/raw303CRLF/indexes→protectedB18 | documentary-preservation-authorization-gate — حفظ 523 مادة و302 صف وALLnext_phase/evidence/rawprefix/G184/827. يتلقى B18 OWN302؛ الحالي B19=307. تعمل كل28 حالة B18 الأصلية بطفل تاريخي صريح دون تعديلها. | INV7B19-18 — هويات المصدر والدخول والأرشيف مستقلة؛ لا rewrite بعد push أو global patch أو test skip، ولا بدء7C/8 من نجاح بوابة الوثائق. | none-documentary-metadata<br>Python/Git للوثائق فقط. stdout الحالي يلتقط مباشرة مرة واحدة ولا self-hash له؛ لا إعادة كتابة أرشيف أو شهادة لكل نثر تاريخي. | P7B19T-35;P7B19T-36 |

ولكل قدرة مسؤولية لا يغني عنها نجاحregex:

| FE | المالك | المدخل المنقح | الأثر إن غاب | الخطوة التالية |
| --- | --- | --- | --- | --- |
| FE7B19-01 | مالك WPF وDBA | عقد حقول رأسي Inv/SafesAdjust ومفتاح ربط المصدر وإصدار schema منقح. | يبقى فتح التسوية غير معتمد عند خلط المصدر أو غياب عقد الربط. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-02 | مالك WPF والمنتج | نسخ SDK وcontract init/load/Loaded/reset وDocumentRef وغرض فتح read/edit منقحة. | يبقى خطر132 محتملاً ولا تثبت حالة الواجهة أو حفظ نسخة جديدة. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-03 | مالك الإنتاج والمخزون | قاموس BaseQty/UnitEquality ومصدر الوصفة التاريخي وسياسة إعادة التحجيم. | لا اعتماد لتحجيم الكميات أو إلغاء التعديل دون هذا العقد. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-04 | مالك الإنتاج والدقة والمحاسب | دقة كمية وسعر ووحدة ومجموع وrounding، مع أمثلة اصطناعية غير midpoint. | لا اعتماد لذهاب وعودة دقة المصدر أو قيمة إنتاج محفوظة. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-05 | المحاسب ومالك POS | سياسة issue-date/modified-at وtimezone والتعديل المسموح، وبيئة اصطناعية. | يبقى أثر نقل تاريخ المستند على الفترات والتقارير غير مقاس وغير معتمد. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-06 | مالك عقد المستند | DocumentRef/source/type/globalId/branch وsupport/allowed-set وrequest generation. | لا اعتماد لهوية صف من الاسم أو الرقم المحلي أو GlobalID وحده. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-07 | مالك الأمان وDBA | منح وأدوار×أوامر×موارد وحد تنفيذ وschema منقحة بلا أسرار. | لا إثبات لعزل الفروع أو رفض الحفظ من الشيفرة المرئية وحدها. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-08 | مالك WPF والمنتج | عقد ملكية نافذة وfresh/reused وdirty/cancel ومصفوفة supported calls. | لا يفصل فقد مسودة فعلي من أمر جديد مشروع دون تحديد المالك والحالة. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-09 | مالك المحمل وWPF | عقد found/not-found/failed/partial ومرجع الطلب ومصدره، منقح. | قد يفسر فشل قراءة كحالة فارغة؛ لا قبول مالي من null. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-10 | مالك المنتج وعقد المستند | مصفوفة supported/unsupported/optional بحسب المصدر والنوع والعملية واللغة. | لا حكم missing-feature أو دعم كامل من switch وحده. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-11 | المحاسب ومالك الأمان | سياسة حراس Save/SavePrint/Pay وإعادة السداد والتعديل والفترة، منقحة. | لا اعتماد لحفظ من مسار بديل أو حارس جزئي. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-12 | مالك المخزون والمناقلة | عقد نتيجة الطرفين/approval/retry/idempotency وحد المعاملة، منقح. | تبقى سلامة طرفي النقل والنجاح الحقيقي غير معتمدة. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-13 | مالك الجرد وDBA | عقد مسودة/اعتماد/إلغاء التسوية ونتيجة الحركة وحد المعاملة، منقح. | لا اعتماد لحالة Is_Approved أو لصحة مصدر القراءة من وجود رسالة. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-14 | مالك الإنتاج وDBA | عقد Parameters/types وDocumentID/LineID/version وBOM/writer منقح. | لا حفظ إنتاج ناجح مفترض قبل حسم020/021 وبقية الوحدات. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-15 | المحاسب ومالك الإنتاج والعملة | قاموس precision/BOM/yield/as-of والعملات والوزن مع مراجع اصطناعية. | لا سياسة أعمال مستنتجة من N2 أوحقل عام أو الموقع. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-16 | مالك التقارير والنشر | manifest/hash/version/SDK/DTO/ToDataTable/REPX ومخرجات وoutcome منقحة. | لا ورقة أو PDF أو wire-schema معتمدة من فتح المحرر. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-17 | مالك نطاق التدقيق | قائمة قدرات ومداخل ومصادر ومخارج متفق عليها مع أسباب الاستبعاد. | لا إغلاق7B من عينة NV22 أو455 صفاً تاريخياً. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |
| FE7B19-18 | مالك أدلة التدقيق | لقطات OWN وثلاثة freezes وبصمات523/827 وstdout حقيقي وهوية الفرع. | لا تحفظ الثقة إن أعيد الأرشيف أو خلط historical parser بالحالي. | تابع خطتي القبول المرتبطتين بإذن لاحق، واحتفظ بالعقد الخارجي أو البقية في H/Q وSP01–03. لا إصلاح أو تشغيل الآن. |

## 5. عقود المقارنة الستة — ليست مصالحة مالية منفذة

| RC والعنوان | FE والجذور | قاعدة المقارنة والحد | الخطط غير المنفذة |
| --- | --- | --- | --- |
| RC7B19-01 — المرجع ومصدر التسوية والعزل | FE7B19-01;FE7B19-06;FE7B19-07;FE7B19-10<br>P7-131;P7-061;P1-013;P2-001;P2-006;H7B19-04;H7B19-03 | قارن عقد المصدر والهوية والحالة والدقة قبل المصب، لا مساواة قسرية بين مصادر مختلفة ولا صحة تقرير أو رصيد من اسمه.<br>عقود ساكنة منتقاة، ليست مصالحة مالية منفذة أو اختبار ERP أو موافقة خارجية. | P7B19T-01;P7B19T-02;P7B19T-11;P7B19T-12;P7B19T-13;P7B19T-14;P7B19T-19;P7B19T-20 |
| RC7B19-02 — التهيئة والصحة والمسودة | FE7B19-02;FE7B19-08;FE7B19-09<br>P7-132;H7B19-03 | قارن عقد المصدر والهوية والحالة والدقة قبل المصب، لا مساواة قسرية بين مصادر مختلفة ولا صحة تقرير أو رصيد من اسمه.<br>عقود ساكنة منتقاة، ليست مصالحة مالية منفذة أو اختبار ERP أو موافقة خارجية. | P7B19T-03;P7B19T-04;P7B19T-15;P7B19T-16;P7B19T-17;P7B19T-18 |
| RC7B19-03 — إعادة تحميل الإنتاج ودقته | FE7B19-03;FE7B19-04;FE7B19-14;FE7B19-15<br>P7-133;P7-134;P4-020;P4-021;P4-022;H7B19-01 | قارن عقد المصدر والهوية والحالة والدقة قبل المصب، لا مساواة قسرية بين مصادر مختلفة ولا صحة تقرير أو رصيد من اسمه.<br>عقود ساكنة منتقاة، ليست مصالحة مالية منفذة أو اختبار ERP أو موافقة خارجية. | P7B19T-05;P7B19T-06;P7B19T-07;P7B19T-08;P7B19T-27;P7B19T-28;P7B19T-29;P7B19T-30 |
| RC7B19-04 — زمن POS وحراس الحفظ | FE7B19-05;FE7B19-11<br>P7-135;P3-001;P4-031;H7B19-04 | قارن عقد المصدر والهوية والحالة والدقة قبل المصب، لا مساواة قسرية بين مصادر مختلفة ولا صحة تقرير أو رصيد من اسمه.<br>عقود ساكنة منتقاة، ليست مصالحة مالية منفذة أو اختبار ERP أو موافقة خارجية. | P7B19T-09;P7B19T-10;P7B19T-21;P7B19T-22 |
| RC7B19-05 — اعتماد النقل والجرد | FE7B19-12;FE7B19-13<br>P4-019;P4-017;P4-018;P7-131 | قارن عقد المصدر والهوية والحالة والدقة قبل المصب، لا مساواة قسرية بين مصادر مختلفة ولا صحة تقرير أو رصيد من اسمه.<br>عقود ساكنة منتقاة، ليست مصالحة مالية منفذة أو اختبار ERP أو موافقة خارجية. | P7B19T-23;P7B19T-24;P7B19T-25;P7B19T-26 |
| RC7B19-06 — الإخراج والحصر والحفظ والإذن | FE7B19-16;FE7B19-17;FE7B19-18<br>H7B19-02;H7B19-06 | قارن عقد المصدر والهوية والحالة والدقة قبل المصب، لا مساواة قسرية بين مصادر مختلفة ولا صحة تقرير أو رصيد من اسمه.<br>عقود ساكنة منتقاة، ليست مصالحة مالية منفذة أو اختبار ERP أو موافقة خارجية. | P7B19T-31;P7B19T-32;P7B19T-33;P7B19T-34;P7B19T-35;P7B19T-36 |

[RC6](evidence/report-reconciliation-07B19.csv) يطابق مجموعة روابطFE فيالأدلة والجذور والخطط، لا يفرض مساواة كل مجموعمالي بمجموع ذيgrain/source/as-of مختلف. sharedguards/null وpublicNavigate وGlobalID شواهد جزئية لا حد صلاحيات أو استعادة منشوراً.

## 6. الحدود التي بقيت عند ملاكها

- [H/Q01](evidence/questions-07B19.csv):BOM والدقة والتاريخ والقاموس المالي والمخزني، مع بقاياHR/ضريبة السابقة؛ لا سياسة قانونية من الموقع.
- H/Q02:manifest/DTO/tabletypes/SDK/REPX وسياسةcopies/printer/snapshot/outcome؛ لا اختبار قالب أو إخراج، وPrint الأوسعSP01.
- H/Q03:DocumentRef/support/health/init/Loaded/reset/dirty/generation، لا كلcaller أو كل7C.
- H/Q04:schema/migrations/grants/constraints/allowed-set؛ لا إثبات نشر منCREATE أو زر مرئي.
- H/Q05:SDK/provider/culture/zone/ownership والأحداث والأحجام؛ لا قياسleak/index/latency أو محاكاة.NET.
- H/Q06:حصر قدرات متفق عليه بعد العينة؛455FE التاريخية وNV22/LC7 ليست مقام اكتمال. [SP01–03](evidence/split-register-07B19.csv) و[المتبقي](PHASE-07-REMAINING-07B19.md) تبقى صريحة.

يربط[الشاهدJSON](evidence/navigation-contract-witnesses-07B19.json) النماذج14 والملاحظات النصية14 بالأدلة والحدود. إعادة حسابه وثائقية فقط. **7B/7 جزئيتان؛R4d/B20 مقترح؛7C لم تبدأ؛8 غير مأذونة.**
