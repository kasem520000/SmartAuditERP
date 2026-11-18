# الجزء7B8 — دعم القرار وملخص السندات وسجل المستخدمين

**مرجع التدقيق المعلن:**2026-11-16 UTC. مصدر التطبيق الأصلي `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. **7B8 تسليم ساكن جزئي؛7B و7 غير مكتملتين،7B9 معلنة للباقي،7C لم تبدأ، والمرحلة8 غير مأذونة ولم تبدأ.** لا إصلاح تطبيق أو قبول/قياس/تشغيل ERP.

آخر دفع مأذون ناجح `d0ae6b318c47451dd7e10a416f07566a7b3f1dc7` كان204 ملفات تدقيق حتى7B5. B6/B7/B8 عمل لاحق محفوظ هنا، لا جزءاً من ذلك الدفع. **في دخولB8 كان checkout المحلي10ba وملفات التدقيق السابقة كلها موجودة كـuntracked docs، والفرع البعيد ما زالd0ae؛** لا نغير مصدر التطبيق أو نعيد بناء تاريخ Git لإخفاء اختلاف السياق. لا commit/push/PR أو fetch/reset/reconstruction جديد فيB8. بيانات checkout في أرشيفB7 تظل حقيقة وقت تسليمه ولا يعاد توليد checksه لتطابق الحاضر.

## 1. حصيلة محدودة لا إغلاق للمرحلة

قُرئت الأجسام المحلية وXAML لكل من **frmDecisionHelp وfrmSummaryD وfrmrptUsersRecords** كاملة، مع DTOين محليين ودعم منتقى للكتابة/المخطط/المداخل/الأطفال/منتجي السجل. الاسم المختصر **frmUsersRecords** في بعض أوصاف الباقي التاريخية يقصد **frmrptUsersRecords الفعلي**، وليس شاشة رابعة أو ملفاً مفقوداً؛ نسجل التوضيح في الطبقة الجديدة دون تغيير التاريخ.

| المقياس | النتيجة المحدودة |
| --- | --- |
| الجديد | 4 نتائج P7-105–108: كلها متوسطة؛3 confirmed محلياً بشروطها و1 potential؛ كلها مفتوحة ولم تعالج. |
| التاريخ | 17 ذيلاً محدداً، دون تغيير أول276 core أو أيnext_phase؛ لا finding لكل query/زر/معالج. |
| التراكمي | 280 مفتوحة:2 حرجة و175 عالية و102 متوسطة و1 منخفضة؛244 confirmed و29 potential و7 repository-gap. |
| النطاق | 23 مساراً، تقاطع13 مع363 السابقة و10 جديدة؛ اتحاد373 ومكمل454 inventory-only فضلاً عن مقاطع داخل373. |
| الأجسام المحلية | 1225 سطراً C# +1388 XAML =2613 سطراً للثلاثة فقط؛ DTOان33 سطراً إضافياً، لا كل dependency/feature/caller. |
| النموذج | 28 صف FE و28 ثابت INV و8 عقود RC؛6 handoffs و6 أسئلة غير محسومة و10 مجموعات استمرار. |
| القبول | 32 خطة غير منفذة =8 خاصة بالجديد +17 انحدار أصل +5 عقود +2 بوابة. |
| شواهد الوثائق | 20 مثالاً يدوياً مستقلاً و20 ملاحظة نصية؛28 حالة جديدة لمدقق الوثائق فقط، لا تشغيل تطبيق. |


confirmed يصف تعارضاً محلياً بشروطه لا حادث إنتاج. potential لا تتحول إلى confirmed من نموذج يدوي، ومنها خطر توقيت مستهلك الملف P7-108 وP7-049 التاريخية. **build/ERP/C#/SQL/WPF/SDK/REPX/Office/COM/مزود/جهاز/صيغة/shell وتصدير فعلي ومعالجة=0.**

### قيد سببي سابق للحساب: دعم القرار ليس نتيجة تشغيل ناجحة

`BtnShow_Click` ينشئ `Thread(CalcStock)`، ثم يقرأ `CalcStock` عناصر WPF مثل chkAllItems/txtItemName/chkAllGroups قبل أول marshal مناسب لتلك القراءات. وجود Dispatcher للتقدم والصفوف **لاحقاً** لا يحميها. امتداد **P7-054** يسبق إمكان الوصول إلى استعلامات/حسابات الحركة في المسار المعتاد. لذلك أمثلة إسقاط المرتجع وPOS، وخلط7/8، وغياب6، وstore=null ومعنى المقياس **تحليل لما بعد الحاجز إذا عولج أو عزل بإذن واختبار مستقل**، لا رصيداً أو تقريراً مرصوداً من التطبيق. نموذج Python لا يعالج الحاجز ولا يعده مجتازاً.

الدليل: `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:426-445`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:174-198`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:270-276`. اختلاف أهلية قائمة المجموعات P7-105 ينتج من LoadGroups أثناء Loaded قبل هذا العامل، فلا يحتاج افتراض تشغيل CalcStock لإثباته. وإتاحة المدخل نفسه تبقى عقداً مستقلاً: Home يربطه لكنه disabled افتراضياً في XAML، لا وصول دور منشور مثبت.

## فصل المصدر وحفظ التاريخ

- [provenanceB8](evidence/provenance-07B8.json) ثُبت **مرة واحدة** بعد فحص الدخول، ويحمي **246 artifact سابقة غير قابلة للتعديل** تشمل تقارير وأدوات وشواهد وchecksB7 الفعلية. ملفات الفهارس الحية الثلاثة والسجل والمدقق الرئيسي فقط من القديم قابلة لتحديث معلن؛ لا إعادة تهيئة snapshots.
- [لقطة276](evidence/findings-through-07B7.csv) byte-exact، SHA256=`1b9b7bbd35723035fc69431a46a9b6033306792c5c5ee13d9c15cc6c03c2dc80`؛ [فهارسB7 الدقيقة](evidence/shared-indexes-through-07B7.json) SHA256=`5bee3da15f6342cd7e184b9d485931233acac2d110788d1cd4ddcb8f770a27a9`.
- [checksB7 المحمي](evidence/checks-07B7.json) SHA256=`25043dbf69013f010a3f063938ea5377862bb9c11d02ea01447a5d51a7ded5c3` بقي stdoutه الحقيقي بلا إعادة كتابة. محولB8 جديد يعطي helperB7 سجل276 وفهارسه الأصلية **في الذاكرة وعند المسارات المنطقية نفسها**؛ لا يمرر له280 أو فهارس اليوم، ولا يعدّل helperB7/B6. كل الأجزاء الأسبق معزولة بمدخلاتها الخاصة كذلك.
- أول276 نواة/عنوان/تصنيف/حالة و**كل next_phase** محفوظة، بما فيها43 متابعة تاريخية تحمل7. تضاف17 ذيلاً محدداً فقط. السجل الحي يحافظ علىCRLF. **G01–122 محفوظة حرفياً** وتضافG123–128 كمجموعات توصية، لا نتائج أخرى.
- فحص [هوية المصدر](tools/audit_source_identity.py) ancestry وصافي دلتا شجرة ملتزمة docs-only، مع فحص مستقل لمجموعة827 مسار تطبيق وبصماتها. source==checkout و0 دلتا ملتزمة حالة صحيحة، لا سبب لاختلاقd0ae محلي. ليس الفحص إثبات كل تاريخ وسيط أو توقيعاً أو تفويضاً للمعالجة.
- وقت ساعة البيئة المشاهد فيprovenanceB8 (`2026-11-18T04:05:11+00:00`) منفصل عن المرجع المعلن16نوفمبر وعن أرشيفB7، وليس تاريخ تشغيل/قبول. اختلاف metadata إعادة الفحص عن أرشيفB7 ليس فقد أدلة أو مبرراً لـrebaseline.

## النطاق المقروء وحدوده

| المسار | المقاطع المنتقاة | حد القراءة |
| --- | --- | --- |
| `SmartAuditERP/Class/Common.cs` | `2076-2093` | تهيئة مراقبة log4net وتغيير ConnectionString فقط دون قراءة قيم اتصال/أسرار؛ لا خريطة appender الخارجية أو سلامة السجل/النشر. |
| `SmartAuditERP/Class/InvoiceOper.cs` | `1583-1601` | عقد writer المحلي للوحدة وval/val1 والسعر/الأثر فقط؛ لا تنفيذ الكاتب أو إصلاح المرتجع أو مصالحة مخزون كاملة. |
| `SmartAuditERP/Class/MainClass.cs` | `45-49` | ConnObj ينشئ اتصالاً؛ لا كل ملكية/إغلاق/صلاحيات MainClass. |
| `SmartAuditERP/Class/ReceiptOper.cs` | `206-218` | معاملات Payment/VAT/NetVal/BranchID المكتوبة فقط؛ لا دورة حفظ/ترحيل السند. |
| `SmartAuditERP/Class_WPF/ReceiptSummaryItem.cs` | `1-22` | عقد صف محلي صغير كاملاً، لاكلClass_WPFأوالمستهلكاتالخارجية. |
| `SmartAuditERP/Class_WPF/UserLogRow.cs` | `1-11` | عقد صف محلي صغير كاملاً، لاكلClass_WPFأوالمستهلكاتالخارجية. |
| `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml` | `1-495` | جسم محلي/واجهة كاملة لـfrmDecisionHelp فقط؛ لا كل caller/child/template/schema/ACL/سياسة/نشر أو قبول. يختلف الاسم الفعلي frmrptUsersRecords عن اختصار UsersRecords في الباقي التاريخي. |
| `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs` | `1-606` | جسم محلي/واجهة كاملة لـfrmDecisionHelp فقط؛ لا كل caller/child/template/schema/ACL/سياسة/نشر أو قبول. يختلف الاسم الفعلي frmrptUsersRecords عن اختصار UsersRecords في الباقي التاريخي. |
| `SmartAuditERP/Form_WPF/frmItemCategory.xaml.cs` | `355-365;399-419` | كاتب مجموعة: type2 للصف وتحويل الأب إلىtype1 فقط؛ لا بقية حفظ/تفويض/تزامن المجموعات. |
| `SmartAuditERP/Form_WPF/frmItems.xaml.cs` | `421-441` | loader المجموعات المماثل لتفسير أهلية اللغة؛ لا بقية بطاقة الصنف. |
| `SmartAuditERP/Form_WPF/frmItemsSrch.xaml.cs` | `1-125` | بداية child البحث وموارد loader وأول query group_id والفرع فقط؛ لا كل البحث/الاختيار/SQLpaging/DTO أو إتاحة/تفويض child. |
| `SmartAuditERP/Form_WPF/frmLogOut.xaml.cs` | `16-16;89-90` | اسم logger وكتابة EmpID/رسالة الخروج فقط؛ لا استكمال دورة logout أو كل ThreadContext. |
| `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs` | `281-298;618-693;1002-1006` | lookup بـBranchId ومقاطع Navigate/قراءة هوية السند ورسالة EmpID بعد نجاح محلي؛ لا كل محرر/قيد/ACL أو منتجي السجل. |
| `SmartAuditERP/Form_WPF/frmSandSD.xaml.cs` | `1001-1064` | Navigate/ReadData المختار فقط؛ لا كل حفظ/تعديل/حذف أو حسم عقد Recipient في النشر. |
| `SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs` | `528-589` | Navigate/ReadData المختار فقط؛ لا كل ترحيل/مخطط/إتاحة/ضريبة محرر الصرف الضريبي. |
| `SmartAuditERP/Form_WPF/frmSummaryD.xaml` | `1-579` | جسم محلي/واجهة كاملة لـfrmSummaryD فقط؛ لا كل caller/child/template/schema/ACL/سياسة/نشر أو قبول. يختلف الاسم الفعلي frmrptUsersRecords عن اختصار UsersRecords في الباقي التاريخي. |
| `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs` | `1-450` | جسم محلي/واجهة كاملة لـfrmSummaryD فقط؛ لا كل caller/child/template/schema/ACL/سياسة/نشر أو قبول. يختلف الاسم الفعلي frmrptUsersRecords عن اختصار UsersRecords في الباقي التاريخي. |
| `SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs` | `42-43;239-246;419-425;489-494` | اسم logger وThreadContext.EmpID ومصدر هوية online/offline المختاران فقط؛ لا إعادة مراجعة دخول أو إثبات تماثل هويات مخزن خارجي. |
| `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml` | `1-314` | جسم محلي/واجهة كاملة لـfrmrptUsersRecords فقط؛ لا كل caller/child/template/schema/ACL/سياسة/نشر أو قبول. يختلف الاسم الفعلي frmrptUsersRecords عن اختصار UsersRecords في الباقي التاريخي. |
| `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs` | `1-169` | جسم محلي/واجهة كاملة لـfrmrptUsersRecords فقط؛ لا كل caller/child/template/schema/ACL/سياسة/نشر أو قبول. يختلف الاسم الفعلي frmrptUsersRecords عن اختصار UsersRecords في الباقي التاريخي. |
| `SmartAuditERP/Home.xaml` | `330-333;383-386;530-533` | ربط ثلاث قوائم وحالتي IsEnabled=false؛ لا تشغيل التفعيل أو إثبات الإتاحة. |
| `SmartAuditERP/Home.xaml.cs` | `92-93;122-123;2592-2597;2922-2927;3648-3648` | مرجعان static ومداخل ثلاث شاشات فقط؛ لا كل Home أو تشغيل صلاحيات menu. |
| `SmartAuditERP/Properties/Resources.resx` | `242-275;714-751;877-896;1496-1532;3026-3064;3957-3971` | DDL محلي للفرع/الموظف/الفئات/السند/السجل ونوع الحركة؛ لا بيانات seed/أشخاص أو كل ترحيل/مخطط منشور أو SQL منفذ. |


[scope23](review-scope-07B8.csv) و[دفتر827](evidence/coverage-ledger-07B8.csv) و[مرشحو98 ملفاً](evidence/report-candidate-disposition-07B8.csv) و[52 شاشة](evidence/report-screen-disposition-07B8.csv) تحفظ الفرق بين inventory-only والمقاطع/الجسم المحلي.98/52 فرز أسماء لا أعداد قدرات مكتملة؛ FingerPrintDevice مطابقة لفظية للبصمة. كل child له عقده ولا يرث تغطية أبيه، ولا all-lines تعني whole-feature أوdeployment/ACL/culture/acceptance.

## 2. النتائج الجديدة

### P7-105 — قائمة مجموعات دعم القرار تغير نطاق الأهلية عند تبديل اللغة بدلاً من تغيير الاسم فقط

**الخطورة:**متوسطة؛ **الإثبات:**`confirmed`؛ `open-not-remediated` و`next_phase=8` تخطيط لا إذن.<br>
**الشاشة والمسار:**frmDecisionHelp؛ دعم loader في frmItems — Loaded → LoadGroups → FillComboBox؛ CalcStock يقرأ Grpcode.

**الدليل:**`SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:58-65`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:110-117`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:180-187`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml:277-288`؛ `SmartAuditERP/Form_WPF/frmItemCategory.xaml.cs:355-365`؛ `SmartAuditERP/Form_WPF/frmItemCategory.xaml.cs:399-419`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:421-441`؛ `SmartAuditERP/Properties/Resources.resx:877-896`.

**المشاهدة المحلية:**الفرع العربي يحمّل ItemsCategory WHERE type=2، والفرع غير العربي يحذف هذا القيد ويغير الاسم عبر CASE فقط. كاتب المجموعة يجعل الأب type=1 والصف الجديد type=2. الاختلاف نفسه حاضر في loader بطاقة الصنف المختار للدعم؛ ليست ترجمة لصفوف المجموعة نفسها.

**السبب الجذري:**ربط شرط أهلية البيانات بفرع اللغة ونسخ استعلامين مختلفين بدلاً من استعلام نطاق واحد بإسقاط اسم مترجم.

**شروط الوصول والحواجز:**مجموعة أب id10/type1 وورقة id20/type2 لهما اسمان صالحان، ولغة ar ثم en في instance جديدة. يثبت اختلاف القائمة من Loaded وحده؛ حساب التقرير اللاحق محجوب بمسار الخيط P7-054، فلا يشترط تجاوزه لإثبات هذه القائمة. تدقيق ساكن محلي فقط؛ لا ERP/C#/SQL/WPF/DevExpress/Office/COM/صيغة/قالب/جهاز/مزود أو بيانات عمل نُفذت. حواجز البناء والمخطط وDTO والتفويض والإتاحة وتوقيت الطلب تسبق قبولاً لاحقاً مستقلاً. مثال يدوي أو فحص نص ليس قبولاً أو حادث إنتاج؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط، لا نتيجة تشغيل:**ar تعرض20 فقط وen تعرض10 و20؛ اختيار10 غير المتاح عربياً قد يطلب Grpcode10 مباشرة لا أبناءه، بعد معالجة حواجز العرض بعقد لاحق. لا ندعي أن كل English label فارغ أو أن كل تقرير إنجليزي يفشل.

**الشاهد المقابل وحد الدليل ومنع التكرار:**المعيار الفعلي للمجموعة مقروء في CalcStock، لذلك ليست توسعة معيار غير مستخدم P7-080، ولا عيب فهرس0 في P7-068. غياب IS_Deleted في كلا فرعي loader سؤال نطاق قائم منفصل؛ المثال يعزل الحذف/الفرع والقيم غير الفارغة، ولا يضاعف finding للنسخة في frmItems.

**المعالجة المقترحة — لم تنفذ:**وحّد مجموعة IDs والأهلية/الفرع والحذف والكتالوج قبل إسقاط اسم اللغة؛ إن كان اختيار الأب مطلوباً فليكن عقد توسعة شجرة واحداً في اللغتين، لا إضافة صفوف صامتة في en. حافظ على هوية العنصر عند تبديل اللغة.

**التحقق اللاحق غير المنفذ:**P7B8T-01 وP7B8T-02؛ FE7B8-01 وINV7B8-01 في[نموذج المصدر](DECISION-SUMMARY-LOGS-07B8.md) و[خطة32](VALIDATION-07B8.md). الشاهد اليدوي/النصي ليس قبول ERP أو توقيت ملف أو مستهلك جداول.

### P7-106 — ملخص السندات يصفر الصافي عند NULL في أحد المبلغين رغم عرض المبلغ الآخر بقيمته

**الخطورة:**متوسطة؛ **الإثبات:**`confirmed`؛ `open-not-remediated` و`next_phase=8` تخطيط لا إذن.<br>
**الشاشة والمسار:**frmSummaryD — ShowResult SELECT Payment+VAT → ReceiptSummaryItem.DgvNet → UpdateSummaries/CSV.

**الدليل:**`SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:168-195`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:211-249`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml:366-405`؛ `SmartAuditERP/Class_WPF/ReceiptSummaryItem.cs:8-20`؛ `SmartAuditERP/Properties/Resources.resx:1496-1508`؛ `SmartAuditERP/Class/ReceiptOper.cs:206-218`.

**المشاهدة المحلية:**الاستعلام يشتق DgvNet=(Payment+VAT) بلا تطبيع NULL. عند ربط الصف يحول Payment وVAT كلّاً على حدة من DBNull إلى0، لكنه يحول ناتج الجمع DBNull إلى0 مستقلاً. DgvNet خاصية مخزنة في النموذج لا getter يعيد جمع القيم المعروضة، وتجمعها بطاقة الصافي وينقلها CSV كما هي.

**السبب الجذري:**سياسة NULL غير متجانسة بين مركبَي المبلغ والمقياس المشتق؛ تطبيع متأخر للناتج بدلاً من تطبيع المصدر أو إعلان unknown.

**شروط الوصول والحواجز:**صف وحيد مخول غير محذوف نوع7/8/9 وبفرع لا يضاعف JOIN، Payment100 وVAT=NULL، وDDL المرفق يسمح NULL لكليهما. لا إثبات لوجود صف كهذا في قاعدة منشورة؛ إن كان NULL غير مسموح أعمالياً فيجب رفضه/إعلانه لا عرضه كصفر صافي. تدقيق ساكن محلي فقط؛ لا ERP/C#/SQL/WPF/DevExpress/Office/COM/صيغة/قالب/جهاز/مزود أو بيانات عمل نُفذت. حواجز البناء والمخطط وDTO والتفويض والإتاحة وتوقيت الطلب تسبق قبولاً لاحقاً مستقلاً. مثال يدوي أو فحص نص ليس قبولاً أو حادث إنتاج؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط، لا نتيجة تشغيل:**يظهر Payment100 وVAT0 بينما DgvNet0 والبطاقة0؛ معاملة NULL كصفر وفق العرض تعطي100، أو يجب إظهار unknown صريحاً وفق السياسة. والعكس PaymentNULL/VAT15 يعطي صافي0 رغم عرض15. لا يلزم تغيير الضرائب أو القيد لشرح التناقض.

**الشاهد المقابل وحد الدليل ومنع التكرار:**صف100/15 غيرNULL يعطي115 فعلاً. حقل NetVal مخزن ومكتوب مستقل لكن التقرير يختار Payment+VAT؛ مصدر الحقيقة النهائي H7B8-01 لا يحسم من الاسم. ليس عيب DTO طباعة P7-047/093؛ المقياس المخالف ينتج في query قبل الربط حتى مع عدم تشغيل طباعة SummaryD التي هي stub.

**المعالجة المقترحة — لم تنفذ:**اختر سياسة NULL صريحة ومصدر صافي معتمداً. عند اعتباره صفراً طبّع كل مركب قبل الجمع، أو احمل unknown/error في result بدلاً من0؛ اجعل الصف والبطاقة وCSV من النموذج المطبع نفسه، ولا تعالج بتعديل GL/سندات تاريخية عشوائياً.

**التحقق اللاحق غير المنفذ:**P7B8T-03 وP7B8T-04؛ FE7B8-02 وINV7B8-02 في[نموذج المصدر](DECISION-SUMMARY-LOGS-07B8.md) و[خطة32](VALIDATION-07B8.md). الشاهد اليدوي/النصي ليس قبول ERP أو توقيت ملف أو مستهلك جداول.

### P7-107 — طلبات سجل المستخدمين المتداخلة تضيف نتائجها إلى المجموعة المشتركة بلا تمييز جيل الطلب

**الخطورة:**متوسطة؛ **الإثبات:**`confirmed`؛ `open-not-remediated` و`next_phase=8` تخطيط لا إذن.<br>
**الشاشة والمسار:**frmrptUsersRecords — btnShow_Click → async void ShowResults → Clear → await Fill → LogList.Add.

**الدليل:**`SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs:18-29`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs:62-109`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs:121-126`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml:177-187`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml:68-101`؛ `SmartAuditERP/Class/MainClass.cs:45-49`.

**المشاهدة المحلية:**يمسح كل طلب LogList قبل await، ثم يضيف صفوف جدوله المحلي إلى المجموعة المشتركة بعد اكتماله. زر العرض لا يعطل في الجسم/XAML ولا cancellation/generation أو استبدال لقطة عند commit. لا يمسح الطلب قائمته مرة أخرى عند النشر، ولا يتحقق أن معاييره ما زالت الحالية.

**السبب الجذري:**غياب ملكية الطلب/جيله للنشر الذري؛ clear-before-await مع append-after-await يسمح بدمج نتيجتين ناجحتين في observable collection واحدة.

**شروط الوصول والحواجز:**نقرتان A ثمB قبل عودة استمرارA، ونجاح المصدرين. يمكن تسلسل تعبئة SQL من دون تداخل reader فعلي: clearA،clearB،اكتملFillA،نشرA،اكتملFillB،نشرB. مشاركة اتصال instance قد تسبب فشلاً في تسلسل آخر لكنها لا تمنع هذا الترتيب؛ لا نفترض MARS أو نختبره. تدقيق ساكن محلي فقط؛ لا ERP/C#/SQL/WPF/DevExpress/Office/COM/صيغة/قالب/جهاز/مزود أو بيانات عمل نُفذت. حواجز البناء والمخطط وDTO والتفويض والإتاحة وتوقيت الطلب تسبق قبولاً لاحقاً مستقلاً. مثال يدوي أو فحص نص ليس قبولاً أو حادث إنتاج؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط، لا نتيجة تشغيل:**A تعيد السجل1 للمستخدمA وB تعيد2 للمستخدمB؛ بعد تغيّر معيار الشاشة إلىB يمكن أن تصبح القائمة[1,2] بدلاً من[2]. وعند المعيار نفسه يمكن تكرارIDs. هذا نموذج interleaving يدوي لا تشغيل Tasks/WPF أو SQL.

**الشاهد المقابل وحد الدليل ومنع التكرار:**الطلب الواحد الناجح يعرض صفوفه محلياً، وقراءة controls تتم قبل Task.Run والتحديث داخل Dispatcher؛ لا نمدد P7-054 إلى السجل. P7-046 يغطي فشل/جزئية المصدر؛ النتيجة الحالية لا تفترض فشلاً أصلاً بل نشر طلبين ناجحين. P7-045 لقطة معايير المخرج لا يمنع وحده الدمج.

**المعالجة المقترحة — لم تنفذ:**التقط criteria وScope وrequestId قبل البدء، وابن result غير قابل للتغيير محلياً ثم انشر مرة واحدة للجيل الأحدث فقط؛ إلغاء/تسلسل single-flight وإدارة اتصال لكل طلب بحسب الملكية. لا يكفي clear جديد في موضع عشوائي أو افتراض ترتيب اكتمال الطلبات.

**التحقق اللاحق غير المنفذ:**P7B8T-05 وP7B8T-06؛ FE7B8-03 وINV7B8-03 في[نموذج المصدر](DECISION-SUMMARY-LOGS-07B8.md) و[خطة32](VALIDATION-07B8.md). الشاهد اليدوي/النصي ليس قبول ERP أو توقيت ملف أو مستهلك جداول.

### P7-108 — فتح ملف سجل المستخدمين للتطبيق الخارجي يسبق إغلاق الكاتب وقد يتيح قراءة ملف غير مكتمل

**الخطورة:**متوسطة؛ **الإثبات:**`potential`؛ `open-not-remediated` و`next_phase=8` تخطيط لا إذن.<br>
**الشاشة والمسار:**frmrptUsersRecords — btnExportExcel_Click → using var StreamWriter → WriteLine → Process.Start before scope end.

**الدليل:**`SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs:137-165`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:274-291`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml:303-310`.

**المشاهدة المحلية:**using var يبقي StreamWriter حياً حتى نهاية try. Process.Start(UseShellExecute=true) يقع قبله ولا Flush/Dispose/AutoFlush محلياً قبله؛ ليست using-block مثل SummaryD التي تنتهي قبل الفتح. المؤكد ترتيب المصدر، أما قراءة ملف ناقص/قفل مستهلك فعلي فخطر زمني محتمل لم ينفذ.

**السبب الجذري:**نشر المسار لمستهلك خارجي قبل اكتمال/finalization الكتابة؛ بدء الفتح ليس برهاناً على أن كل البيانات وصلت إلى الملف.

**شروط الوصول والحواجز:**تصدير سجل صغير/كبير في بيئة لاحقة مأذونة، مع مستهلك يمكن أن يحاول القراءة أثناء Process.Start وقبل انتهاء try. سلوك التخزين المؤقت وتوقيت الارتباط بالمستهلك/المنصة غير مقاسين؛ لا نقرر أن كل فتح يفشل أو كل ملف فارغ. تدقيق ساكن محلي فقط؛ لا ERP/C#/SQL/WPF/DevExpress/Office/COM/صيغة/قالب/جهاز/مزود أو بيانات عمل نُفذت. حواجز البناء والمخطط وDTO والتفويض والإتاحة وتوقيت الطلب تسبق قبولاً لاحقاً مستقلاً. مثال يدوي أو فحص نص ليس قبولاً أو حادث إنتاج؛ الحجب ليس نجاحاً.

**الأثر بمثال مشروط، لا نتيجة تشغيل:**قارئ مبكر قد يرى فقط ما نُقل من buffer حتى تلك اللحظة أو يرفض ملفاً مشغولاً؛ قارئ متأخر بعد Dispose قد يقرأ كاملاً. نموذج state يفرق write-buffered عن finalized دون تشغيل FileStream أو shell أو Office.

**الشاهد المقابل وحد الدليل ومنع التكرار:**SummaryD يغلق using-block فعلاً قبل Process.Start كشاهد مقابل؛ لا تعميم عليه. النتيجة potential محفوظة ولا يرقّيها نموذج يدوي إلى عيب مرئي confirmed. فساد CSV النحوي P7-048 وسلامة الصيغة P7-049 مستقلان حتى مع ملف مكتمل.

**المعالجة المقترحة — لم تنفذ:**أكمل وأغلق الكاتب بنجاح قبل أي فتح خارجي؛ انشر ملفاً نهائياً واحداً بعد finalize، وتحقق من فشل الكتابة/الإلغاء قبل إعلان النجاح. لا فتح تلقائي افتراضي غير لازم؛ سياسة المستهلك منفصلة عن escaping وformula safety.

**التحقق اللاحق غير المنفذ:**P7B8T-07 وP7B8T-08؛ FE7B8-04 وINV7B8-04 في[نموذج المصدر](DECISION-SUMMARY-LOGS-07B8.md) و[خطة32](VALIDATION-07B8.md). الشاهد اليدوي/النصي ليس قبول ERP أو توقيت ملف أو مستهلك جداول.

## 3. توسيع الأصول السابقة — لا نتائج مكررة

[manifest الذيول](evidence/historical-extensions-07B8.csv) يحدد tail كل سجل حرفياً. لا إعادة عنوان أو severity/certainty/type/status أوnext_phase في التاريخ. العنوان التاريخي قد يصف مثاله الأول؛ الامتداد هنا يعلن الجذر والاختلاف، لا يزعم أن كل آلياته القديمة تطابقت في كل شاشة.

| المعرف | الأصل | المشاهدة الإضافية وحدها | المتابعة المقترحة | الدليل |
| --- | --- | --- | --- | --- |
| EX7B8-01 | P1-004 | دعم القرار يحمل rptDecisionHelp/header/footer REPX فعلاً. SummaryD يفحص المسار ثم يستدعي SetStatus فارغة بلا renderer؛ نقص قالب خارجي لا يفسر وحده هذا stub ولا يعالَج بقالب وهمي. | manifest موثوق لقالب مستهلك فعلاً وDTO بإصدار؛ افصل حواجز النشر عن القدرة غير المنفذة. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:526-567`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:396-424` |
| EX7B8-02 | P1-013 | Home يستدعي ApplyPermission/DoApply قبل Show لـDecisionHelp/SummaryD، ومدخلاهما disabled في XAML؛ التفعيل الفعلي ونتيجة visual-tree غير محسومين هنا. سجل المستخدمين يفتح new بلا Apply محلي، وأطفال SummaryD تعرض ثم Navigate بلا Apply محلي. potential التاريخية لم ترفع أو تقفل. | تفويض القراءة/التفاصيل/التصدير في حد موثوق مع خريطة مدخل/دور؛ لا استنتاج وصول دور إنتاجي من اسم menu أو ترتيب الاستدعاء وحده. | `SmartAuditERP/Home.xaml.cs:2592-2597`؛ `SmartAuditERP/Home.xaml.cs:2922-2927`؛ `SmartAuditERP/Home.xaml.cs:3648-3648`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:316-340`؛ `SmartAuditERP/Home.xaml:330-333`؛ `SmartAuditERP/Home.xaml:383-386`؛ `SmartAuditERP/Home.xaml:530-533` |
| EX7B8-03 | P1-030 | Home يحتفظ بنسختين static لـSummaryD وDecisionHelp؛ أمر الخروج Close والاستدعاء التالي يعيد Show على instance Closed. سجل المستخدمين new كل مرة شاهد مقابل، لا يعمم عليه العمر نفسه. | دورة instance/session صريحة أو إنشاء بعد Closed، ثم اختبار close/reopen وتغير جلسة؛ لا إخفاء استثناء. | `SmartAuditERP/Home.xaml.cs:92-93`؛ `SmartAuditERP/Home.xaml.cs:122-123`؛ `SmartAuditERP/Home.xaml.cs:2592-2597`؛ `SmartAuditERP/Home.xaml.cs:2922-2927`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:70-72`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:255-258` |
| EX7B8-04 | P1-033 | طباعة/معاينة SummaryD موصولتان لكن PrintReport لا يقرأ قالباً أو ينفذ مخرجاً؛ ينتهي إلى SetStatus فارغة. بحث الحساب يعرض placeholder. لا finding لكل زر فارغ، ولا تعميم P7-097 إذ لا FlowDocument هنا أصلاً. | نفذ القدرة بعقد مصدر/نتيجة أو عطلها وفق المتطلب؛ ملف REPX فارغ أو رسالة جارٍ لا ينفذان الطباعة. | `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:259-261`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:378-389`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:396-424`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:436-436`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml:561-571` |
| EX7B8-05 | P2-010 | اختيار فرع SummaryD يستعمل Branches.id بينما JOIN يقابل Receipts.BranchID بـBranches.BranchId ومحرر القبض يختار BranchId. مع id1/BranchId7 يطلب الاختيار1 لا7. كلا العمودين موجود؛ لا ادعاء غياب BranchId أو اختلاف بيانات منشورة. null/كل يزيل القيد دون تقاطع مفوض مثبت محلياً. | هوية فرع canonical وعقد id/BranchId منشور، وBranchScope مفوض لا fail-open؛ قارن GlobalIDs وعدد JOIN دون افتراض تطابق القيم أو تفرد BranchId غير المرفق. | `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:103-125`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:158-166`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:181-193`؛ `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:281-298`؛ `SmartAuditERP/Properties/Resources.resx:242-275`؛ `SmartAuditERP/Properties/Resources.resx:1518-1522` |
| EX7B8-06 | P3-023 | SummaryD يبني نهاية اليوم التالي.Date ثم يستعمل ReceiptDate<=@date2، فيضم منتصف ليل اليوم التالي. المعاملات تحمل DateTime فعلياً كشاهد صحيح لكنه لا يصلح المقارنة الشاملة. | [from,toExclusive) typed مع اختبار آخر لحظة ومنتصف الليل ودقة SQL وسياسة المنطقة؛ لا تغيير علامة المقارنة وحدها. | `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:168-171`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:195-205` |
| EX7B8-07 | P7-039 | دعم القرار يستعمل SUM(val) للكمية، لكن XAML يسميها المبلغ الوارد/الصادر وينقلها DTO باسم Income/Outcome. امتداد لعقد تسمية/وحدة المقياس، لا زعم استعمال متوسط التكلفة التاريخي نفسه ولا أن val مبلغ. | سمِّ كمية أساس/وحدة واضحة أو احسب مبلغاً بعقد مستقل؛ لا تغير مقياس الحركة أو الربح بصمت تحت label مالي. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:290-313`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:237-256`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml:372-391` |
| EX7B8-08 | P7-040 | hasMovement لا يفحص purchaseReturn/saleReturn/rentOutcome/rentReturn. صف له مرتجع فقط أو POS وحيد مصنف rent قد يسقط بالكامل. المثال مشروط بتجاوز حاجز الخيط P7-054 وعزل أخطاء الكتالوج. | أهلية تمثل كل حركة معتبرة أو كل مقياس/رصيد، مع استبعاد مسند ومصالحة؛ لا finding لكل متغير غائب. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:217-246` |
| EX7B8-09 | P7-045 | BindToReportData يقرأ المخزن/الصنف الحاليين فوق DataView حمّل سابقاً؛ تغيير controls لا يبطل النتيجة. امتداد لقطة المعايير لا فقد كل DTO؛ حساب المسار الأصلي رهن حاجز الخيط. | لقطة criteria/result/version أو dirty-output guard؛ لا ترويسة B فوق بيانات A ولا إصلاح مصدر من renderer. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:492-518`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:426-445`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:403-419` |
| EX7B8-10 | P7-046 | دعم القرار يرد0 عند استثناء كل GetSumVal، فيخلط غياب الحركة بفشلها. SummaryD يمسح _items قبل Fill ولا يحدث بطاقاته إلا بعد النجاح؛ فشل الطلب الجديد قد يبقي بطاقات قديمة وقائمة فارغة/جزئية. | result/error/partial typed ونشر ذري؛ فشل مصدر ليس0 ولا نتيجة أقدم حالية. P7-107 جديد لتداخل طلبين ناجحين، لا جمع كل async تحت فشل المصدر. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:288-320`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:266-276`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:133-134`؛ `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:207-249` |
| EX7B8-11 | P7-048 | SummaryD يكتب N2 بفواصله الثقافية وحقول النص بلا CSV escaping؛ 1000.00 قد تكتب 1,000.00 فتزيد الخلايا. السجل يحيط Message باقتباسين دون مضاعفة الداخليين وبقية النص خام؛ O"K لا يحفظ حرفياً. | مرمز CSV واحد بحالات فاصلة/اقتباس/أسطر وثقافات وround-trip لكل الحقول؛ لا تفترض Office لإثبات خلل النحو. | `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:278-286`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs:146-155` |
| EX7B8-12 | P7-049 | CSV السندات والسجلات يحمل نصوصاً ثم ShellExecute؛ لا سياسة typed-text مثبتة محلياً. سلامة صيغة مستهلك الجداول محتملة ولم تنفذ؛ لا ننسب سلوك formula إلى ExportToXlsx في DecisionHelp دون عقد SDK. | عقد نص خامل ومستهلك معلن، وتجنب الفتح التلقائي غير اللازم؛ escaping وfinalization لا يغلقان potential دون دليل المستهلك. | `SmartAuditERP/Form_WPF/frmSummaryD.xaml.cs:278-290`؛ `SmartAuditERP/Form_WPF/frmrptUsersRecords.xaml.cs:146-159` |
| EX7B8-13 | P7-054 | BtnShow ينشئ Thread(CalcStock)، وأول البناء يقرأ chkAllItems/txtItemName/chkAllGroups ثم المخزن خارج Dispatcher. وجود Dispatcher للتقدم/النشر لاحقاً لا يحمي القراءات الأولى؛ حاجز سابق للحساب في المسار المعتاد. | التقط معايير typed ومفوضة على UI قبل العامل ومرر قيماً ثابتة؛ لا access controls فيه. الحسابات المشروطة ليست نتائج تشغيل بعد تجاوز الحاجز في نموذج يدوي. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:426-445`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:174-198`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:270-276` |
| EX7B8-14 | P7-056 | دعم القرار يسمي invType8 تسوية و7 مناقلة، بينما الكتالوج المرفق يعرف7 تسوية و8 مناقلة. استعلام7/1/sub2 قد لا يمثل التسوية الصادرة7/2؛ توسعة root النوعين لا نتيجة لكل استدعاء. | كتالوج واحد للنوع/إجراء الرأس/أثر السطر؛ اختبر7/1 و7/2 و8/1 و8/2 مع عزل حاجز الخيط. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:224-227`؛ `SmartAuditERP/Properties/Resources.resx:3058-3064` |
| EX7B8-15 | P7-057 | استدعاءات GetSumVal المحددة لا تمرر نوع6 للإنتاج/الاستهلاك. الكتالوج يعرف6/1 و6/2؛ لا يصح ادعاء رصيد كامل بلا نطاق معلن. نوعا4/5 وAndroid20 سؤال نطاق أيضاً لا finding جديد لكل كود. | أعلن مصادر الحركات المدخلة/المستبعدة، واربط نوع6 ومكوناته بعقد أثر السطر، أو استبعده بسبب موثق لا رصيد شامل مزعوم. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:217-227`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:280-305`؛ `SmartAuditERP/Properties/Resources.resx:3054-3056` |
| EX7B8-16 | P7-080 | مرشح inv_sub.store يتكون من المخزن المختار ويمر للأنواع9/1/2/3، لكن أربع قراءات التسوية/المناقلة تمرر safeFilter=null. fixture مخزنA2 ومخزنB8 يضيف10 تحتA عند عزل الأنواع والخيط. المجموعة والصنف مقروءان فعلاً فلا تعميم إهمالهما. | مرر Scope/Store لكل مصدر ذي صلة بعقد الطرفين/التحويل؛ إن قصد إجمالي المخازن فسمّه مستقلاً وصالحه لا تحت اسم المختار. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:195-198`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:217-227`؛ `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:304-305` |
| EX7B8-17 | P7-084 | دعم القرار يسمي POS نوع3 rentOutcome/rentReturn ويفصله عن sale نوع2؛ الموجب العادي من3 لا يدخل بوابة hasMovement إلا مع حركة أخرى. القراءة هنا تستعمل inv_type فعلاً؛ ليست نسخة آلية لكل proc_type في الأصل. | جدول نوع×إجراء×أثر ومصطلحات POS الصحيحة وإشارة المرتجع، مع عزل حاجز الكاتب P4-001؛ لا فرض صفر أو سلوك قالب. | `SmartAuditERP/Form_WPF/frmDecisionHelp.xaml.cs:217-227`؛ `SmartAuditERP/Properties/Resources.resx:3036-3040`؛ `SmartAuditERP/Properties/Resources.resx:3028-3030` |


### قرارات منع التكرار والشواهد المقابلة

- **P7-105** اختلاف IDs/أهلية باللغة؛ ليس شرط index0 التاريخي P7-068 ولا معياراً غير مقروء P7-080. **P7-106** فقد NULL بين جمع SQL وربط مكونات السند؛ ليس فقد حقول طباعة P7-047/093 ولا مجرد اختيار NetVal مختلف.
- **P7-107** نشر طلبين ناجحين بلا ملكية/جيل؛ مستقل عن فشل المصدر/الجزئية P7-046 أو ترويسة live فوق نتيجة P7-045. نقرتا A ثمB لا تستلزمان قارئي SQL متزامنين ناجحين: يكفي clearB قبل استمرارA ولو تعبأ المصدران بالتسلسل. مشاركة الاتصال قد تفشل في ترتيب آخر؛ لا MARS مفترض ولا سباق مقاس.
- **P7-108** حد اكتمال الملف قبل نشره لمستهلك؛ مستقل عن نحـو CSV P7-048 وصيغ المستهلك P7-049. الثابت ترتيب المصدر، أما قراءة ملف ناقص/مشغول فـpotential بسبب التوقيت والمنصة. **SummaryD يغلق كاتبه قبل الفتح فعلاً**؛ لا نعطيه العيب نفسه.
- **P7-039** يجمع خلل تسمية المقياس ووحدته، لا يدعي إعادة معادلة average-cost نفسها. DecisionHelp يجمع val (كمية أساس وفق الكاتب)، **ولا يضربها في السعر**؛ لذلك لا ذيل جديد P7-041 هنا. تفسير الدوران/الركود ومقام0 ونطاق all-time معلق H7B8-01، وليس finding لنسبة لا متطلب معتمداً لها.
- **P7-080** خاص بعدم تمرير المخزن لأربع مصادر؛ الصنف والمجموعة مقروءان فعلاً. **SummaryD يرسل receiptType+GlobalID** للتفاصيل: لا ذيل P7-061 أو زعم رقم محلي فقط. مقاطع Navigate لا تثبت سياسة/حفظ كل طفل أو تجيز فتحه.
- **DecisionHelp يحمل REPX فعلياً**، بخلاف SummaryD stub؛ لا تعميم P7-097 أو فقد DTO طباعة غير موجودة أصلاً. سجل المستخدمين يقرأ المعايير قبل Task.Run وينشر عبر Dispatcher: **لا ذيل P7-054 له**. `MainClass.ConnObj` ينشئ اتصالاً جديداً، وSummaryD يغلق اتصاله فيfinally/OnClosing؛ لا blanket leak.
- يوجد منتجون للسجل فعلاً: login/سند قبض وخروج مختارة تضع EmpID من EmpNo. config/appender الخارجية ومساواة CloudUserID بـEmployees.id والاحتفاظ/الخصوصية/تغطية الأحداث **لم تحسم**. لا claim سلامة سجل تدقيق شامل أو tampering/تسرب أو تجاوز تفويض خادم من غياب حارس محلي.
- SearchByItemName نص SQL محلي، لكن لم يثبت caller له في التتبع المحدود؛ لا تمديد P1-011 من مجرد interpolation أو int IDs. لا يتم تشغيله أو حقن SQL لإكمال هذا التدقيق.

## 4. المعالجات والحدود الباقية

الأولوية المقترحة: معايير typed/immutable ومفوضة قبل عامل دعم القرار، كتالوج نوع/رأس/أثر ونطاق مصادر واضح، أهلية مجموعة واحدة في اللغات، سياسة NULL وصافي سند موحدة، requestId ونشر ذري/إلغاء أوsingle-flight للسجل، ثم CSV encoder وfinalize-before-open وعقد مستهلك نص خامل. هوية الفرع/appender/GL والقالب/الإتاحة متطلبات مستقلة؛ لا معالجة عشوائية لبيانات أو GL أو ترحيل لجعل نموذج يمر.

التفصيل في[نموذج28/28 وعقود8](DECISION-SUMMARY-LOGS-07B8.md)، و[خطط32](VALIDATION-07B8.md)، و[IMPROVEMENTS](IMPROVEMENTS.md) G123–128. التحقق الوثائقي الفعلي يحفظ في[checksB8](evidence/checks-07B8.json) بحدوده، وليس شهادة مالية/أمنية أو نجاح الخطط.

**المتبقي المعلن7B9**: عقود caller/child/output/template/schema/ACL/سياسة وإتاحة بمرشحي التقارير وبقايا الأجسام المقروءة أو استبعادات مسندة/أجزاء أخرى. **7C لم تبدأ** لبقية HR/PM/بحري/UI وموارد/events/timers/async/connections ولوحة المفاتيح/RTL/accessibility/cultures/messages وأداء المصدر. source hot-path ليس latency/leak/index؛ أي قياس/SQLplans وتشغيل/8 يحتاج إذناً ومتطلبات مستقلة. لا تغلق7B/7 إلا بخريطة feature×screen×implementation×test/استبعاد حقيقية؛ استمرار المستخدم في التدقيق ليس إذن إصلاح أو8.
