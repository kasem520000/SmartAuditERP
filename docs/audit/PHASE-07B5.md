# المرحلة 7 — الجزء 7B5: تفاصيل المبيعات و POS وأندرويد وتجميع الأصناف

**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`، الفرع `arena/94ae8414-smartauditerp`.  
**مرجع التدقيق المعلن:** 2026-11-16 UTC. ملاحظة ساعة البيئة عند دخول الجزء `2026-11-18T01:42:35+00:00` محفوظة منفصلة في provenance؛ ليست تاريخ تشغيل تطبيق ولا إعادة تأريخ للتقارير المحمية.  
**الحالة:** مراجعة ساكنة ضمن إذن متابعة المرحلة 7، لا معالجة للشيفرة أو تشغيل ERP أو إذن المرحلة 8.

## 1. الخلاصة وحدود التسليم

قرأ هذا الجزء **خمسة أجسام تقارير C# محلية كاملة، مجموعها 4,624 سطراً**، ومقاطع XAML/كاتب/دفع/قيد/موارد ومداخل محددة. قراءة الجسم المحلي كله لا تعني كل callers أو الأطفال أو القوالب أو مخطط النشر أو السياسة المالية أو قبول التشغيل.

**لم تكتمل 7B أو 7. أُعلنت 7B6 لبقية المالية/الإخراج والمتصلين ومرشحي غير regex والأبناء، ومنها `frmItemsalesdetailsPos` المختلف و`frmActsInvTotal` و`frmNkdTotSalePurch`؛ لم تبدأ. 7C لم تبدأ. المرحلة 8 غير مأذونة ولم تبدأ.** استمرار «طيب واصل العمل» إذن متابعة التدقيق فقط؛ `next_phase=8` تخطيط لا تصريح تشغيل أو إصلاح.

- **5 نتائج جديدة P7-090–094:** 3 عالية و 2 متوسطة، كلها `confirmed / implementation-defect / open-not-remediated` للسلوك أو التعارض المحلي بشروطه؛ ليست حوادث إنتاج مرصودة.
- التراكمي **266 مفتوحة**: 2 حرجة، 173 عالية، 90 متوسطة، 1 منخفضة؛ **231 مؤكدة، 28 محتملة، 7 فجوات مستودع**.
- **24 ذيلاً للأدلة فقط** لأصول سابقة، مع حفظ الخطورة واليقين والنوع والعنوان والحالة **وكل next_phase لأول 261**، ومنها 43 تحمل متابعة7 تاريخياً. لا إعادة عد للأصل أو معالجة أو ترقية P1-013/P7-049 من potential.
- **26 مساراً**: 13 متداخلة مع الاتحاد السابق334 و13 جديدة؛ الاتحاد **347 من827**، وبقي **480 inventory-only** بلا نطاق منتقى ومقاطع غير مختارة داخل الاتحاد. هذه محاسبة مسارات لا نسبة اكتمال أو تغطية ميزات/تنفيذ.
- **35 صف ميزة×شاشة×تنفيذ×خطة، 22 ثابتاً مطلوباً، 8 عقود مصدر/مصالحة، 39 خطة غير منفذة**: 10 مباشرة للجديد، 24 انحدار أصل، 3 عقود عابرة، 2 بوابة نطاق/إذن. الصفان المؤجلان لا يمثلان تنفيذ ميزات تمت مراجعته.
- **20 توضيحاً يدوياً مستقلاً و20 ملاحظة نصية محدودة**، و22 حالة اصطناعية جديدة لمدقق الوثائق؛ ليست اختبارات C#/SQL/WPF أو قبولاً مالياً. الأجنحة التاريخية82 محفوظة، فيكون مجموع حالات المدقق104 فقط.

لم ينفذ build أو C#/Windows/WPF أو SQL/ترحيل أو DevExpress/DTO/SDK/REPX أو Office/COM/صيغة spreadsheet أو مزود/جهاز/طابعة. لا أسرار أو بيانات أشخاص/إنتاج أو ثنائيات وقوالب مجهولة. ملفات التطبيق الأصلية لم تعدل؛ لا إصلاحات أو commit/push. لا شهادة صحة مالية/أمنية أو امتثال أو ادعاء العثور على كل العيوب.

### الأولويات التي كشفها الجزء

1. **أوامر مالية من تقرير:** النقدي/الشبكة يستعملان `InvTotal` دون توفيق حالة السداد وتفاصيل الدفعات؛ والمحمل اللاحق يعيد مقدار النقد/المدفوع من `Net`. لا يعني ذلك تلقائياً قيداً غير متوازن أو تحصيلاً بنكياً وقع. إلغاء اختيار العميل لا يمنع إرسال الهوية0.
2. **القراءة والتحصيل:** قارئا POS/Android يستبدلان النقد الفعلي بـ `tot_net` لكل pay_type1، ولو الحالة جزئية. تعديل الكاتب وعيب القارئ مستقلان، ولا يعالجان بتعديل مستند لإجبار تقرير على المطابقة.
3. **مصدر الطباعة ومعيار الضريبة:** الجسور الثلاثة تمرر GridView حقيقية وصفوفاً، لكنها لا تنقل signed summaries. وAndroid يرشح عمود `Inv.FreeVATSales` الفعلي ثم يعرض قيمة مشتقة بالاسم نفسه؛ ليست دعوى استعمال SELECT alias غير صالح.
4. **أصول ممتدة لا نتائج مكررة:** شراء فقط يسقط من gate بيعي؛ تجميع POS لا يستبعد حذف الرأس؛ gross يسمى net؛ معايير واجهة مهملة؛ ضريبة عادية/إضافية غير متفقة في القارئ العام؛ فرع قديم بعد «الكل»؛ CSV وpartial/snapshot والتفويض والفترة والذرية والإصدار. تبقى كل هذه تحت معرفاتها الأصلية.

## 2. نطاق القراءة الفعلي

[review-scope-07B5.csv](review-scope-07B5.csv) يحكم حدود القراءة. الأجسام الخمسة ليست اسمياً كل تقارير المبيعات، والتجميعي `frmRptItemsSalesDetailsPOS` ليس الجسم التفصيلي المختلف `frmItemsalesdetailsPos` المؤجل7B6.

| الجسم المحلي | C# المقروء | XAML المختار فقط | حد المراجعة |
|---|---|---|---|
| frmRptInvSalesDetails | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1-1514` | 1-13;276-566;605-1093;1105-1140 | جسم التقرير العام:معايير/قارئ/ضريبة/ملخص/أوامر تعديل/تصدير/فتح/جسر طباعة؛ لا كل الكاتب أو callers أو نشر. |
| frmRptInvSalesDetailsPos | `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:1-896` | 1-13;254-411;476-774;796-894;909-939 | جسم قائمة POS:معايير/أهلية/دفع/ملخص/فتح/CSV/GridView مؤقت؛ لا اعتماد قالب أو مزود. |
| frmRptInvSalesDetailsPosAndroid | `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:1-986` | 1-13;270-551;613-901;925-1019;1035-1065 | جسم قائمة Android:مصدر الفترة/ضريبة/فرع/دفع/صفوف/فتح ومخرج؛ لا اعتماد sync/نشر أو DTO. |
| frmRptItemsSalesDetails | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:1-731` | 1-14;249-431;465-633;661-686 | جسم تجميعي البيع/الشراء:أهلية الحركة/وحدة/خصم/هوية/ملخص/مصدر طباعة/CSV. |
| frmRptItemsSalesDetailsPOS | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:1-497` | 1-14;237-341;373-484;495-534;560-585 | جسم تجميعي POS:أهلية المستند/الحذف/فرع/قيمة/ملخص/ضريبة إضافية حالية/مخرج. |

المسارات21 الأخرى هي خمس XAML للتقارير، وحوار `frmSrchClient`335 سطراً مع ربط الإغلاق المختار في XAML، و`InventoryData`303 أسطر و`ItemSalesRow`14 و`ItemSalesPosRow`15 محلية كاملة، ومقاطع `InvoiceOper` و`EntryOper` و`ItemOper` و`Report` و`Resources.resx` و`Home` و`FrmRptSalesChart` و`Common` و`LoadData` و`frmPOSPay` و`frmPOSBill`. لا مراجعة كاملة لعائلة الدفع أو العملاء أو الموارد أو كل مداخل Home من هذه المقاطع.

- [دفتر827](evidence/coverage-ledger-07B5.csv) يحفظ نطاق كل جزء واتحاد النطاقات ومكمله النصي؛ حتى all-lines لا يثبت اكتمال ميزة أو قبولاً.
- [98 مرشح ملف](evidence/report-candidate-disposition-07B5.csv) فرز لفظي، و[52 مرشح شاشة](evidence/report-screen-disposition-07B5.csv) =35 لفظياً+17 غير regex. ليست أعداد ميزات مكتملة أو أجسام مقروءة؛ FingerPrintDevice مطابقة لفظية للبصمة.
- قراءة launcher مؤسسة النقد في B3، أو اسم طفل في Home/B5، لا تغطي أجسام `frmActsInvTotal` و`frmNkdTotSalePurch` أو `frmItemsalesdetailsPos`. الباقي7B6/7C يحتاج قراءة تنفيذ أو استبعاداً مسنداً أو أجزاء إضافية معلنة.

## 3. النتائج الجديدة

التصنيف والحالة مشتركان كما في الخلاصة. «مؤكد» يعني قراراً/إغفالاً محلياً محدداً، لا صحة schema/DTO/ترخيص أو واقعة خسارة في نشر فعلي. الأمثلة fixtures يدوية مستقلة لا نواتج البرنامج.

### P7-090 — أوامر تغيير الدفع في تقرير المبيعات تكتب InvTotal ولا تصالح حالة السداد وتفاصيله

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvSalesDetails` — ToolMenuCash/Credit/Visa → UPDATE Inv → RegenerateEntry → BindInvoByID/SaveEnty.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1098-1205`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1290-1320`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1434-1458`؛ `SmartAuditERP/Class/InvoiceOper.cs:1539-1564`؛ `SmartAuditERP/Class/InvoiceOper.cs:1697-1766`؛ `SmartAuditERP/Class/InvoiceOper.cs:3075-3102`؛ `SmartAuditERP/Class/EntryOper.cs:96-180`؛ `SmartAuditERP/Class/EntryOper.cs:220-276`؛ `SmartAuditERP/Properties/Resources.resx:3859-3880`.

**المشاهدة المحلية:** النقدي يكتب cash=InvTotal و paid=InvTotal، والشبكة تكتب visa=InvTotal و paid=InvTotal؛ الآجل يصفر هذه الحقول. لا تسند الأوامر الثلاثة PaymentStatus أو تعيد تصنيف InvoicePayments. الكاتب المحلي يفصل InvTotal عن tot_net وحالة السداد وتفاصيل الدفعات. ثم BindInvoByID يعيد بناء Paycash/PayATM و Paid من Net عند نوع دفع 1/2 قبل ربط القيد، فيمكن أن يختلف الرأس المحفوظ عن كائن القيد.

**السبب الجذري:** تعديل يدوي لجزء من نموذج الدفع متعدد التمثيلات خارج عقد إعادة تصنيف أو تسوية موحد، مع استعمال أساس قبل الضريبة مكان صافي المستحق. وجود transaction للقيود وحده لا يصالح هذه الدلالات.

**الشروط والحواجز:** فاتورة نوع2 ومتاح أمر العمليات ودور مخول في بيئة لاحقة، InvTotal=100 و tax=15 و tot_net=115 بلا خصم/إضافات، وحالة سداد سابقة معلومة ودفعات موثقة. يكفي اختلاف InvTotal عن tot_net؛ لا نفترض عملية تحصيل حدثت فعلاً. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**مثال الأثر المشروط:** تحويلها نقدياً يكتب paid/cash=100، بينما محمل القيد لنوع1 يبني Paycash=115 و Paid=115. حالة سابقة غير مدفوعة أو دفعة شبكة سابقة لا تتغير تلقائياً؛ يمكن أن يظل مرشح PaymentStatus أو تفصيل الدفعات مخالفاً للرأس الجديد.

**حد الدليل والشاهد المقابل:** إذا تساوى InvTotal و tot_net قد تختفي فجوة المبلغ وحدها، لا فجوة الحالة/التفاصيل. لا نثبت trigger خارج المستودع أو تحصيلاً بنكياً أو صحة القيد النهائي. انفصال المعاملة وابتلاع فشل SaveEnty امتداد P3-003، واستبدال القيد بلا إصدار امتداد P3-006، لا نتيجتان جديدتان هنا.

**معالجة مقترحة — لم تنفذ:** انقل الأمر لاحقاً إلى خدمة إعادة تصنيف مالية مصرح بها: تحدد هل المراد تغيير وسيلة دفعة قائمة أم تسوية مستحق، وتبني المبلغ من العقد الصحيح وتوفق الرأس والحالة والتفاصيل والقيد في اعتماد واحد بإصدار ونتيجة. لا تنشئ دفعة أو تتصل بمزود لمجرد إصلاح عرض.

**التحقق المخطط غير المنفذ:** P7B5T-01؛ P7B5T-02 في [خطة39](VALIDATION-07B5.md). 1) إذا كان المقصود سداداً كاملاً فالمبلغ115 في التمثيلات المصرح بها كلها؛ إن كان مجرد إعادة تصنيف فلا يختلق سداداً جديداً. لا gap100/115 ولا نجاح جزئي. 2) انتقال حالة وتفاصيل متسق وقابل للتتبع؛ لا يحتفظ بحالة paid قديمة مع paid0 أو بدفعة وسيلة سابقة كأنها الجديدة. لا تحصيل أو رد فعلي في الاختبار.

### P7-091 — إغلاق حوار تغيير العميل بلا اختيار يمرر ClientId الصفري إلى تحديث الفواتير

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvSalesDetails + frmSrchClient` — toolCustomers_Click → addNewItem → ShowDialog/Close → Client_id → Chang_Customer.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:43-53`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1334-1430`؛ `SmartAuditERP/Form_WPF/frmSrchClient.xaml.cs:19-43`؛ `SmartAuditERP/Form_WPF/frmSrchClient.xaml.cs:85-90`؛ `SmartAuditERP/Form_WPF/frmSrchClient.xaml.cs:266-293`؛ `SmartAuditERP/Form_WPF/frmSrchClient.xaml:14-15`؛ `SmartAuditERP/Form_WPF/frmSrchClient.xaml:160-166`.

**المشاهدة المحلية:** معالج تغيير الحساب يستدعي Chang_Customer بعد addNewItem بلا نتيجة نجاح. addNewItem ينشئ حواراً جديداً ويأخذ ClientId بعد ShowDialog دون تمييز إلغاء/اختيار. ClientId خاصية int بلا تهيئة؛ لا يغيرها الحوار إلا SelectCurrentItem. Escape وزر الإغلاق يغلقان بلا تعيين. يصبح _Client_id=0، والحارس اللاحق يرفض العميل1 للآجل فقط ولا يرفض0 قبل UPDATE.

**السبب الجذري:** عدم وجود عقد نتيجة حوار مختارة/ملغاة، وتحويل القيمة الافتراضية إلى هوية أمر تعديل قبل التحقق من الطرف وصلاحيته.

**الشروط والحواجز:** صف نوع2 محدد وله GlobalID وعميل فعلي؛ افتح تغيير الحساب ثم أغلق بـ Escape أو زر الإغلاق أو X بلا اختيار. يلزم أن تسمح قاعدة الاختبار بالتحديث لإظهار الكتابة؛ إذا منعه قيد خارجي فهو حاجز يسجل لا دليل أن التطبيق عالج الإلغاء. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**مثال الأثر المشروط:** فاتورة عميلها7 يمكن أن يرسل لها الأمر Cust_id=0 بعد الإلغاء، ثم يحاول إعادة توليد القيد. لا يلزم أن يكون id0 عميلاً صالحاً أو أن ينجح القيد حتى يثبت تمرير أمر تغيير غير مطلوب.

**حد الدليل والشاهد المقابل:** اختيار صف فعلي يضبط ClientId. POS نوع3 يستثنيه Chang_Customer؛ السيناريو يعزل نوع2. لا نستنتج من DDL وحده حالة FK في نشر فعلي أو خسارة طرف مرصودة. هذا ليس P4-015 لتعديل نموذج الدفع قبل التأكيد؛ هنا يترجم caller إغلاق حوار جديد إلى أمر SQL بهوية افتراضية.

**معالجة مقترحة — لم تنفذ:** نتيجة typed من الحوار تحمل SelectedCustomerId أو Cancelled، ولا يستدعى أمر التغيير عند الإلغاء أو الفشل. تحقق داخل خدمة الأمر من وجود العميل وتفعيله ونطاقه وتوافق نوع الدفع، مع تأكيد يذكر المستند والطرف القديم والجديد.

**التحقق المخطط غير المنفذ:** P7B5T-03؛ P7B5T-04 في [خطة39](VALIDATION-07B5.md). 1) لا UPDATE ولا SaveEnty ولا تغيير ذاكرة العميل/الرأس عند كل إلغاء؛ لا إرسال0 أو إعادة استخدام اختيار قديم. 2) يقبل الصالح بعد التفويض والتأكيد فقط، ويرفض غير المحلول بلا كتابة؛ رسالة النتيجة تطابق الاعتماد.

### P7-092 — قارئا POS وأندرويد يستبدلان النقد المحفوظ بصافي الفاتورة دون مراعاة السداد الجزئي

**الخطورة:** عالية. **الشاشة والمسار:** `frmRptInvSalesDetailsPos / frmRptInvSalesDetailsPosAndroid` — BindingListOfInvoices1 → cash / paid / tot_net → Paycash → SummaryCards/CSV/print bridge.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:424-448`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:523-554`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:490-513`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:591-622`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:586-601`؛ `SmartAuditERP/Class/InvoiceOper.cs:4498-4549`؛ `SmartAuditERP/Class/InvoiceOper.cs:4592-4616`؛ `SmartAuditERP/Class/InvoiceOper.cs:4725-4740`؛ `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:494-560`؛ `SmartAuditERP/Form_WPF/frmPOSPay.xaml.cs:445-506`؛ `SmartAuditERP/Class/InvoiceOper.cs:1542-1564`.

**المشاهدة المحلية:** كل قارئ يأخذ paid من الرأس، ويقرأ cash ثم يستبدله بـ tot_net لكل pay_type=1 بلا فحص PaymentStatus أو مبلغ الدفع. المسار العام بالمقابل يقيد هذا الاستبدال بحالة1. مسارات الدفع المرفقة تسمح بحالة PaidPartially وتحتفظ بمبلغ نقدي مستقل عن Net، والكاتب يحفظ cash و paid و PaymentStatus منفصلة.

**السبب الجذري:** اشتقاق مقدار التحصيل من وسيلة الدفع وحدها، وكأن Cash تعني دائماً PaidInFull، رغم وجود حالة ومبالغ فعلية مستقلة.

**الشروط والحواجز:** رأس اختباري نقدي pay_type1 وصافي115 و paid/cash40 وحالة جزئية، ولا شبكة أو دفع زائد؛ عميل مؤهل وخيار الدفع الجزئي متاح وفق إعدادات وعقد بيئة لاحقة. هذه حالة يدعمها النموذج والكاتب، لا ادعاء سجل إنتاج موجود. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**مثال الأثر المشروط:** يعرض/يجمع القارئ Paycash=115 بدلاً من40 بينما Paid يبقى40؛ الفرق75. فاتورتان جزئيتان 115/40 و85/20 يمكن أن تظهر نقديتهما200 بدلاً من60 قبل أثر المرتجعات.

**حد الدليل والشاهد المقابل:** سداد كامل cash=Net يخفي الفرق؛ لا تعمم السلوك على قارئ التقرير العام الذي يضيف شرط حالة1، ولا تزعم أن جميع إعدادات POS تتيح الجزئي أو أن الحفظ/المزود نجح فعلاً. P7-090 تعديل كاتب مختلف؛ هذه إسقاط قراءة غير محفوظ مستقل حتى لرأس صحيح.

**معالجة مقترحة — لم تنفذ:** اعرض التحصيل التاريخي من مبلغ/تفصيل موثق، ولا تستنتجه من pay_type. افصل Paid/Outstanding/Change/CashTendered/SettledCash إذا كانت السياسة تميزها، وطبق الإشارة نفسها في الصف والمجموع والمخرج دون تعديل بيانات المستند لإصلاح التقرير.

**التحقق المخطط غير المنفذ:** P7B5T-05؛ P7B5T-06 في [خطة39](VALIDATION-07B5.md). 1) النقد التاريخي40 لا115، والمدفوع40؛ بقية75 معرّفة الإشارة وفق العقد ولا تغطى بإعادة بناء cash من Net. 2) الكامل115 شاهد مقابل فقط؛ الجزئي يظل بمبلغه الفعلي ومجاميع البيع ناقص المرتجع تطابق المرجع المستقل.

### P7-093 — جسور الطباعة المؤقتة لا تنقل المجاميع الموقعة إلى مصدر التقرير

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvSalesDetails / Pos / PosAndroid` — PrintReport → tempGrid.DataSource/PopulateColumns → Report.BindToData(GridView) → InventoryData summary fields.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:680-715`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1465-1503`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:523-554`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:853-885`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:591-622`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:941-974`؛ `SmartAuditERP/Class/Report.cs:400-432`؛ `SmartAuditERP/Class/InventoryData.cs:7-14`؛ `SmartAuditERP/Class/InventoryData.cs:145-169`؛ `SmartAuditERP/Class/InventoryData.cs:186-199`.

**المشاهدة المحلية:** المجاميع على WPF تحسب محلياً كبيع ناقص مرتجع. عند الطباعة تنشأ GridView جديدة مرتبطة بالقائمة وتولد أعمدتها فقط؛ لا تنقل بطاقات المجاميع ولا تعرف Summary أو CustomSummary موقعة. Report.BindToData لا يعيد الحساب من ProcType، بل يقرأ SummaryText لأعمدة هذه الشبكة الجديدة ويضعه في Sum/Total1/SumTax/NetTotal وغيرها.

**السبب الجذري:** جسر بيانات يعتمد حالة summaries في widget آخر لم يتم بناؤها أو نقلها، بدلاً من نموذج نتيجة مالي مستقل له مجاميع موحدة.

**الشروط والحواجز:** صف بيع100 وصف مرتجع20 بمقادير موجبة على الصف وProcType1/2، والمجموع المعتمد80. قالب موثوق أو فاحص DataSet يقرأ حقول summary، مع إصدار DevExpress و DTO معلنين في قبول لاحق؛ لا قالب مجهول هنا. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**مثال الأثر المشروط:** البطاقة المحلية تحسب80، لكن الجسر لا يورّد80 إلى SummaryText الذي يستهلكه Report. قيمة default/فارغة أو سلوك القالب يحتاج فحصاً مأذوناً؛ وحتى Sum عادي موجب إن أضيف لاحقاً قد يعطي120 لا80.

**حد الدليل والشاهد المقابل:** تمرر الجسور الثلاثة GridView حقيقية غير null وصفوفاً فعلية؛ ليست توسعة P7-055. وليست P7-047 لإسناد نسبة مكان مبلغ أو أصفار صريحة في DataTable. المؤكد غياب نقل/تعريف المجاميع الموقعة؛ لا نزعم صفحة فارغة أو قيمة SummaryText افتراضية بعينها أو عيباً في DevExpress/REPX.

**معالجة مقترحة — لم تنفذ:** مصدر typed immutable واحد يحمل الصفوف والمجاميع الموقعة ومعايير الطلب، ويغذي WPF والطباعة والتصدير؛ أو عقد summaries صريح مختبر بإصدار معلوم. لا تنسخ نصوصاً منسقة كمرجع مالي ولا تصلح المشكلة بتمرير null أو Sum موجب لكل الصفوف.

**التحقق المخطط غير المنفذ:** P7B5T-07؛ P7B5T-08 في [خطة39](VALIDATION-07B5.md). 1) القيمة المطلوبة80 للمقياس غير الضريبي نفسه، ونقل صريح موثق لا الاعتماد على default SummaryText؛ لا120 ولا قيمة غير متاحة معروضة كحقيقة. 2) summary المرتجع-20 حسب العقد، والفراغ معلن ولا تقرير نهائي مضلل؛ بيانات الصفوف محفوظة ولا يزعم فشل null.

### P7-094 — مرشح ضريبة أندرويد يستعمل FreeVATSales المحفوظة بينما يعرض قيمة معاد حسابها

**الخطورة:** متوسطة. **الشاشة والمسار:** `frmRptInvSalesDetailsPosAndroid` — showInvoice VAT predicate → WHERE FreeVATSales → Inv.FreeVATSales / correlated AS FreeVATSales → row.FreeVATSales.

**الدليل:** `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:349-410`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:518-533`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml:465-486`؛ `SmartAuditERP/Properties/Resources.resx:954-1016`؛ `SmartAuditERP/Properties/Resources.resx:48842-48844`؛ `SmartAuditERP/Class/InvoiceOper.cs:1567-1570`.

**المشاهدة المحلية:** rbWithVat/rbNoVAT يضيفان FreeVATSales=0 أو >0 إلى WHERE. في DDL يوجد Inv.FreeVATSales فعلي؛ فلا نحكم أن SELECT alias غير صالح. الإسقاط نفسه يحسب SUM لبنود taxval=0 ويسميها FreeVATSales، ثم يقرأها الصف. سكربت الترقية المرفق يسند0 للرأس inv_type>3 عند null، ومنها20، بينما قد تكون البنود المعفاة موجبة؛ والكاتب يقبل قيمة الرأس مستقلة.

**السبب الجذري:** معيار الصف وقيمته المعروضة لا يصدران عن تعبير أو نسخة مصدر واحدة، مع إخفاء الفرق باستعمال الاسم نفسه لحقل رأس و alias مشتق.

**الشروط والحواجز:** نسخة مخطط تحتوي العمود المرفق، وفاتورة Android20 لها قيمة رأس FreeVATSales=0 وبند خال من الضريبة بقيمة100؛ تنشأ هذه الحالة أيضاً تحت دفعة الترقية المرفقة إذا كان الرأس null. لا نفترض أن دفعة الترقية نفذت في نشر فعلي أو أن كل فواتير Android بهذه الحالة. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**مثال الأثر المشروط:** خيار بدون VAT (>0) يسقط الفاتورة لأن الرأس0، مع أن وضع الكل يعرض FreeVATSales=100؛ وخيار VAT (=0) يمكن أن يضمها. التطابق عندما الرأس والمشتق متساويان شاهد مقابل لا علاج.

**حد الدليل والشاهد المقابل:** لا SQL منفذ، ولا خطأ alias أو عمود مفقود مثبت؛ وجود العمود هو سبب أهمية التفريق. تعريف مختلط/معفى/صفر/خصم المبلغ يحتاج سياسة، وتصحيح التعبير وحده لا يحددها. غياب استعمال VAT radios في التقرير العام توسعة P7-080 منفصلة.

**معالجة مقترحة — لم تنفذ:** حدد معنى VATFilter ومصدره بإصدار واضح؛ ابن التعبير مرة في CTE/derived projection ثم رشح واقرأ القيمة نفسها، أو اعتمد العمود التاريخي بعد ضمان تحديثه ومصالحته. لا تعالج بتغيير اسم alias فقط أو UPDATE واسع لرؤوس الإنتاج.

**التحقق المخطط غير المنفذ:** P7B5T-09؛ P7B5T-10 في [خطة39](VALIDATION-07B5.md). 1) تتطابق عضوية الفاتورة مع القيمة والمفهوم المعتمدين؛ لا يستخدم الرأس0 للتصفية ثم يعرض100 دون بيان اختلاف. 2) التساوي لا يخفي اختبار الاختلاف؛ all/with/no ذات دلالات معلنة ويصدر criterion والعرض من المصدر نفسه.

## 4. توسعات أصول سابقة — ليست 24 نتيجة أخرى

[CSV التوسعات](evidence/historical-extensions-07B5.csv) يحدد ذيول evidence بالترتيب الدقيق؛ النواة والتصنيف والعنوان والحالة **وكل next_phase لأول261** باقية. الأمثلة الجديدة لا تغير يقين الأصل التاريخي أو تثبت trigger/server-side guards أو تقفل نتيجته. خطط11–34 في [القبول](VALIDATION-07B5.md) هي انحدار لهذه الأصول لا قبول منفذ.

| التوسعة | الأصل المحفوظ | الملاحظة المحلية المحددة | الدليل |
|---|---|---|---|
| EX7B5-01 | P1-004 | خمسة callers إضافية تسمي REPX، وبعضها يستعمل GridView/UtilitiesProj. وجود FromFile أو اسم ملف لا يثبت توريداً أو عقد بيانات أو إصداراً موثوقاً. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1465-1503`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:853-885`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:941-974`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:482-554`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:339-393` |
| EX7B5-02 | P1-011 | بحث الصنف يدرج name/code المدخلين داخل SQL؛ فتح المصدر يدرج GlobalID من الصف داخل literal. بحث النص مسار مباشر؛ GlobalID المحمل ليس مدخلاً بشرياً مثبتاً بنفس الثقة. | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:353-406`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1052-1080`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:812-845`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:917-934` |
| EX7B5-03 | P1-013 | المداخل والفتح ليست متطابقة في ApplyPermission: التفاصيل تستدعيه قبل العرض، فتح محرر المصدر لا يستدعيه محلياً، وبعض Home لا يستدعيه. لا يثبت ذلك وحده سلوك الشجرة أو تفويض خادم. | `SmartAuditERP/Home.xaml.cs:3496-3520`؛ `SmartAuditERP/Home.xaml.cs:3529-3537`؛ `SmartAuditERP/Home.xaml.cs:3627-3633`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1010-1080`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:777-845`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:882-934` |
| EX7B5-04 | P1-030 | Home يحتفظ بمرجع Android static ويعيد Show؛ زر الإغلاق في الجسم يستدعي Close. مسار إضافي لنفس أصل إعادة عرض نافذة مغلقة، لا نتيجة lifecycle لكل نافذة. | `SmartAuditERP/Home.xaml.cs:236-237`؛ `SmartAuditERP/Home.xaml.cs:3633-3633`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:728-729` |
| EX7B5-05 | P1-033 | AddClient يعرض رسالة placeholder لا إضافة؛ DgvSaleRatio يثبت0 في التجميعيين ثم ينقل إلى Ratio للطباعة. عمود النسبة مخفي في XAML، فلا ندعي أن المستخدم يراه على الشبكة حالياً؛ تبقى دلالة القالب غير محسومة. | `SmartAuditERP/Form_WPF/frmSrchClient.xaml.cs:295-303`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:304-309`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:464-464`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml:534-542`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:238-240`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:311-311`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml:436-444` |
| EX7B5-06 | P2-001 | إخفاء زر العمليات عند DBNull إعداد فقط لا guard مالي في الأوامر؛ شرط منع POS3 موجود في النقدي/الشبكة/العميل وغائب عن الآجل. تدقيق الخدمة/الدور لا يستبدله visibility أو التزام handler آخر. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:118-133`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:973-1000`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1098-1205`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1290-1320`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1362-1430`؛ `SmartAuditERP/Home.xaml.cs:3496-3520`؛ `SmartAuditERP/Home.xaml.cs:3627-3633` |
| EX7B5-07 | P2-010 | قارئ POS وتجميعه بلا BranchScope محلي في SQL، والكل في التجميعي العام يمكن أن يترك branchFilter فارغاً. نقدي التقرير العام يقيد MainClass.BranchNo بينما القراءة قد تختار فرعاً آخر، بخلاف بقية أوامره؛ لا يفحص عدد الصفوف ثم يعيد القيد ويعلن النجاح. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:169-202`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:342-345`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1125-1134`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1183-1192`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1300-1311`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:253-338`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:157-211`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:195-218`؛ `SmartAuditERP/Home.xaml.cs:3158-3172` |
| EX7B5-08 | P2-011 | قوائم المخازن تختلف بين LoadData حسب الموظف و Safes بحسب فرع الجلسة، ومع كل المخازن لا تقاطع SQL تلقائي بموارد الدور. تحميل combobox ليس سياسة server-side. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:268-276`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:119-126`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:133-140`؛ `SmartAuditERP/Class/LoadData.cs:12-26`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:104-120`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:100-116` |
| EX7B5-09 | P3-001 | تعديل الدفع/العميل وإعادة توليد القيد يدخلان الحفظ المشترك دون حارس إقفال فترة محلي في هذه السلسلة. لا نعالجها بإضافة حارس زر فقط. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1098-1205`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1290-1320`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1362-1458`؛ `SmartAuditERP/Class/EntryOper.cs:850-937` |
| EX7B5-10 | P3-002 | caller جديد يستدعي BindInvoiceToEntry ثم SaveEnty؛ التحقق من بنود/توازن/هوية القيد ليس في الحفظ المشترك، وفشل الربط قد يعيد null. لا عد جديد لكل caller. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1434-1458`؛ `SmartAuditERP/Class/EntryOper.cs:62-87`؛ `SmartAuditERP/Class/EntryOper.cs:284-302`؛ `SmartAuditERP/Class/EntryOper.cs:850-937` |
| EX7B5-11 | P3-003 | UPDATE الرأس يسبق SaveEnty على اتصال/معاملة منفصلين. RegenerateEntry يرجع void ويعرض فشل false أو الاستثناء داخلياً، ثم caller قد يعلن النجاح. الحفظ الذري/نتيجة الفشل أصل سابق لا نتيجة جديدة هنا. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1125-1145`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1183-1201`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1300-1322`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1406-1458`؛ `SmartAuditERP/Class/EntryOper.cs:850-937` |
| EX7B5-12 | P3-006 | تعديل تقرير قديم يعيد توليد تفاصيل القيد بطريقة حذف/إدراج من دون إصدار المستند/القيد في predicate؛ لا يتغير هذا الأصل من كون GlobalID مستعملاً. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1098-1205`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1290-1320`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1362-1458`؛ `SmartAuditERP/Class/EntryOper.cs:861-914` |
| EX7B5-13 | P3-023 | نهاية صحيحة 23:59 تفسر بثواني00، وتقارن BETWEEN شاملاً إلى تلك اللحظة؛ فلا تصل ثانية23:59:30. fallback23:59:59 في الثلاثة الأولى لا يستعمل للنص الصحيح. التجميعيان يرجعان date عند خطأ parse دون إعلان. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:422-438`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:665-672`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml:458-475`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:297-314`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:508-515`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:367-384`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:576-583`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:185-188`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:213-218`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:323-334`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:163-172`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:257-266` |
| EX7B5-14 | P7-040 | نفس أصل حارس الوجود الجزئي للحركة: التجميعي العام يجلب شراءه ومرتجعه لكنه يفحص sale/returnSale/POS فقط قبل فرع OperType2. صنف شراء فقط يسقط؛ بيع فقط يمكن أن يظهر بكمية/شراء0. لم تسجل نتيجة أخرى لأن أصل gate غير الممثل للمقياس قائم تاريخياً. | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:222-239`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:267-296`؛ `SmartAuditERP/Home.xaml.cs:3165-3171` |
| EX7B5-15 | P7-045 | مخرجات تحمل معايير controls الحالية مع مجموعات محملة سابقاً، وأوامر التعديل لا تعيد تحميل القائمة/البطاقات. caller الرسم ينفذ showInvoice قبل Show؛ Loaded يعيد التواريخ/lookups، فتتغير المعايير الظاهرة بعد التحميل. لا نثبت أن كل request drilldown محفوظ الفرع. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1136-1145`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:1465-1503`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:853-885`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:941-974`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:452-479`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:285-336`؛ `SmartAuditERP/Form_WPF/FrmRptSalesChart.xaml.cs:420-443`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:137-161`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:169-189` |
| EX7B5-16 | P7-046 | الثلاثة الأولى تمسك أخطاء صفوف مفردة وتتابع ثم تعيد قائمة بلا حالة partial؛ والخمسة تمسح القائمة قبل اكتمال التحميل وتحدث البطاقات عند النهاية فقط. عند فشل لاحق قد تتخالف الصفوف والبطاقات أو تسقط صفوف بلا تحذير شامل. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:337-338`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:502-647`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:257-258`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:375-492`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:284-285`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:446-560`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:182-182`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:313-320`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:161-161`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:247-254` |
| EX7B5-17 | P7-048 | الثلاثة الأولى تكتب CSV بفواصل ونصوص وأعداد N2 دون cell encoding؛ التجميعيان يحيطان الخلايا باقتباس لكن لا يضاعفان الاقتباس داخل النص. quoting لبعض الحالات شاهد مقابل لا حل كامل. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:841-897`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:643-697`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:749-801`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:556-592`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:395-431` |
| EX7B5-18 | P7-049 | أسماء العميل/الصنف والرموز تنسخ إلى ملف ثم يفتح ShellExecute، بلا سياسة نص آمن لبادئات الصيغ. لم يفتح جدول أو يفسر صيغة؛ أصل potential محفوظ ويتوقف الأثر على برنامج المستخدم. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:872-897`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:674-697`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:779-801`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:573-592`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:412-431` |
| EX7B5-19 | P7-067 | تجميع أصناف POS يقيد Items.IS_Deleted فقط ولا يقيد Inv.IS_Deleted؛ قد تدخل فاتورة POS محذوفة. العام وقائمة فواتير POS يستبعدان الرأس المحذوف محلياً كشاهد مقابل لا اعتماد كامل. | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:157-211`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:222-258`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:315-338` |
| EX7B5-20 | P7-080 | امتداد معيار واجهة مهمل: VAT radios في العام لا يقرأها showInvoice، وProcGroup في Android لا يقرأه showInvoice بل يبني الإجراء من ckAllInvs/cmbInvType. توجد معايير بديلة في Android وليست كل مصادره بلا filter. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:333-474`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml:480-500`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:280-418`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml:519-536` |
| EX7B5-21 | P7-083 | التجميعيان يسميان val1×exchange_price صافي البيع دون خصم بند أو حصة رأس، ويطرحان المرتجع بالقيمة gross نفسها. لا نكرر نتيجة net/gross القائمة في B4. استعمال val1 للقيمة صحيح وحدةً خلاف P7-041 ولا يعالج الخصم. | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:222-239`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:285-309`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:180-199`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml.cs:227-240`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml:525-532`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetailsPOS.xaml:427-434`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1598`؛ `SmartAuditERP/Class/ItemOper.cs:1403-1413` |
| EX7B5-22 | P7-085 | الجسم العام للأصناف يستعمل SelectedId ويبطل هويته عند الكل، لكنه يحل النص عند Enter/بحث فقط، وزر العرض يكتفي باسم غير فارغ. تعديل اسم/رمز بعد اختيارA دون Enter قد يبقي idA. امتداد أصل الهوية/الوصف لا SQL injection جديد. | `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:193-204`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:353-425`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:599-618`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:679-691`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:717-728`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml:311-352` |
| EX7B5-23 | P7-086 | العام يحسب VAT=tax-ExtraVAT إذا كان الفرق موجباً؛ وإلا يرجع tax ثم TotalTax=VAT+ExtraVAT. الكاتب يحفظهما مستقلين. tax20/extra5 يعرض15/5/20 لا20/5/25. حالة5/5 في العام ترجع5/5/10 بخلاف قارئ الإشعارات السابق؛ لا يعاد استعمال شاهده بلا فحص. POS و Android يفصلان المكونين صحيحاً محلياً. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:566-584`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:699-711`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPos.xaml.cs:416-424`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:487-495`؛ `SmartAuditERP/Class/InvoiceOper.cs:1546-1546`؛ `SmartAuditERP/Class/InvoiceOper.cs:1560-1560`؛ `SmartAuditERP/Class/ItemOper.cs:1634-1641` |
| EX7B5-24 | P7-088 | العام و Android يطبقان branch من SelectedIndex دون فحص all؛ handler all يغير IsEnabled فقط. التجميعي العام بالمقابل يقرأ !chkAllBranches في builder، فلا يعمم العيب على الخمسة. | `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:342-345`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml.cs:781-785`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetails.xaml:423-434`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:289-292`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml.cs:680-684`؛ `SmartAuditERP/Form_WPF/frmRptInvSalesDetailsPosAndroid.xaml:411-423`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:195-196`؛ `SmartAuditERP/Form_WPF/frmRptItemsSalesDetails.xaml.cs:693-696` |

### ما لا يصح دمجه أو استنتاجه

- P7-090 فرق دلالة المبلغ/الحالة/تفصيل الدفع؛ ذرية الحفظ وابتلاع الفشل P3-003، والاستبدال بلا إصدار P3-006، والفترة P3-001، وصحة القيد P3-002، والتفويض/الفرع P2. لا نتيجتان جديدتان لكل UPDATE.
- P7-091 أمر جديد بعد إلغاء حوار بلا نتيجة؛ لا نحوله إلى عميل0 صالح أو ندعي نجاح FK/القيد. P7-092 قارئ قد يضلل النقد حتى لرأس وتفاصيل صحيحين.
- P7-093 ليست `BindToData(null)` في P7-055؛ الصفوف تصل هنا. ليست صفراً صريحاً أو نسبة مكان مبلغ في P7-047؛ المؤكد غياب نقل/تعريف summary الموقعة. لا نقرر قيمة default DevExpress أو صفحة مطبوعة مرصودة.
- P7-094 ليست عموداً مفقوداً أو WHERE alias خطأ؛ عمود الرأس موجود في DDL المرفق. إهمال radios في تقرير آخر يبقى P7-080، ولا يخترع تعريف إعفاء/تصفير أو يثبت نشر migration.
- أرقام الأداء والموارد غير مقاسة. العرض هنا متزامن على UI؛ ليس عيب direct UI من worker في P7-054. تتبع connection/early return/per-row lookup أولوية7C، لا leak أو index مفقوداً مثبتاً.

## 5. شواهد مقابلة وحدود عقود غير محسومة

1. **هوية المصدر:** فتح الفواتير الثلاث يحفظ `GlobalID` ويقيد النوع/الإجراء؛ لا نمدد فقد هوية P7-061. هذا لا يثبت التفويض أو قفل الفترة أو صحة Show/Loaded/config.
2. **الوحدة والإشارة:** تجميعا الأصناف يستعملان `val1 × exchange_price` للقيمة و`val` لكمية الأساس؛ لا نكرر خلل وحدة P7-041 هنا. يبقى الخصم مهملاً تحت P7-083. البطاقات الثلاث تخصم المرتجع محلياً، بخلاف عقد summary غير المنقول.
3. **الضريبة والدفع:** POS/Android يجمعان VAT العادية مع ExtraVAT مستقلتين في الصف محلياً، فلا تعميم P7-086 عليهما. القارئ العام يضيف شرط PaymentStatus1 لاستبدال cash، فلا تعميم P7-092 عليه. وللمثال5/5 في العام fallback مختلف عن قارئ الإشعارات السابق.
4. **أهلية وفرع:** قائمة فواتير POS والعام يستبعدان حذف الرأس محلياً، بخلاف تجميع POS. التجميعي العام يقرأ خيار كل الفروع، بخلاف العام/Android. هذه شواهد ضيقة لا شهادة source completeness أو ACL.
5. **عقود بناء/نشر:** InventoryData ونموذجا الأصناف موجودون محلياً؛ المجهول عقد `InvoiceTxt` الخارجي و`UtilitiesProj.Common.ToDataTable` وREPX/الإصدار. من أسئلة العقد `InvertoryTxt/InvertoryName` و`SELECT Inv.*` مع alias FreeVATSales في POS تحت DDL الذي يحتوي العمود؛ لا ندعي SQL failure أو سلوك إعادة تسمية DataTable بعينه. H7B5-05 يبقي هذه الأسئلة بلا اختراع حقول.

تفصيل الربط في [نموذج المصادر](SALES-DETAIL-REPORTS-07B5.md) و[مصفوفة35](evidence/feature-implementation-matrix-07B5.csv)، و[الثوابت22](evidence/report-invariants-07B5.csv)، و[العقود8](evidence/report-reconciliation-07B5.csv).

## 6. التحقق وحفظ التاريخ

[لقطة261](evidence/findings-through-07B4.csv) SHA256=`a951b1a4b2e3df5342f82e9a69736a3cf37e7507cb55809d5e5b628e9ca6b258`، و[فهارسB4 الدقيقة](evidence/shared-indexes-through-07B4.json)، و[provenance178](evidence/provenance-07B5.json) تحفظ178 artifact تاريخية، منها155 المحمية سابقاً وchecksB4 الفعلي. لا إنشاء ثانٍ لهذه اللقطات، ولا إعادة توليد تقرير أو helper أو checks محمي. G-01–104 محفوظة حرفياً؛ تضاف ست مجموعات G-105–110 في [التحسينات](IMPROVEMENTS.md)، لا ست نتائج أخرى.

المدقق يعزل B4 بمدخلاته261 وفهارسه عند المسارات المنطقية نفسها **في الذاكرة**، ثم يتحقق من B5/266؛ A/B1/B2/B3 كذلك بمدخلاتها الخاصة. مقاييس مدقق أحدث ليست ادعاء استنساخ bytes للـchecks التاريخية. نتيجة الاتساق الجديدة فقط في [checks7B5](evidence/checks-07B5.json)، ومنهجها في [VALIDATION](VALIDATION-07B5.md). نجاح المستقلات/الفحوص النصية/حالات المدقق لا يصدق تشغيل ERP أو المبالغ أو السياسة.

## 7. الباقي والقرار التالي

**لم تكتمل 7B أو 7. أُعلنت 7B6 لبقية المالية/الإخراج والمتصلين ومرشحي غير regex والأبناء، ومنها `frmItemsalesdetailsPos` المختلف و`frmActsInvTotal` و`frmNkdTotSalePurch`؛ لم تبدأ. 7C لم تبدأ. المرحلة 8 غير مأذونة ولم تبدأ.** استمرار «طيب واصل العمل» إذن متابعة التدقيق فقط؛ `next_phase=8` تخطيط لا تصريح تشغيل أو إصلاح.

[backlog10](evidence/continuation-backlog-07B5.csv) يربط BK7B5 بأصول BK7B4 ثم BK7، و[handoffs6](evidence/handoffs-07B5.csv)/[questions6](evidence/questions-07B5.csv) تضيف عقود إعادة تصنيف الدفع ونتيجة الحوار والتحصيل/الصافي ومعيارVAT والبناء/الموارد وباقي النطاق إلى الإحالات السابقة؛ لا طلب أسرار أو بيانات إنتاج. يجب إتمام القدرات والمقاطع أو استبعادها بسبب موثق أو إعلان أجزاء أخرى، لا إغلاق7 باسم98/52 أو اتحاد347.
