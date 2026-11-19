# المرحلة 7B19 — فتح المستند من التقرير إلى المحرر، R4c محدود

مرجع التدقيق المعلن **2026-11-16 UTC**. مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B19 يلي دفع B18 المكتمل `ee393a741a862a605c6c2f688d3f634bd91856ae` بجميع **528 ملف تدقيق**. ساعة التجميد المرصودة `2026-11-19T03:37:39.154596+00:00` مستقلة عن المرجع، لا تشغيل تطبيق في أي منهما.

**7B/7 جزئيتان؛ R4c سُلّم بحدوده لا كل R4، وR4d/7B20 مقترح؛7C لم تبدأ؛8 غير مأذونة ولم تبدأ.** لا تشغيل أو بناء ERP/C#/SQL/VB/WPF/SDK/DTO/REPX/Office/COM أو مفسر أو مزود أو جهاز أو طابعة أو تصدير أعمال أو shell للتطبيق. لا بيانات أعمال حقيقية أو أسرار أو إصلاح أو قبول أو قياس تشغيلي. Python/Git لأدوات الوثائق فقط؛ `next_phase=8` ليس إذناً.

[النتيجة](PHASE-07B19.md) · [عقود التوجيه والاستقبال](NAVIGATION-CONTRACTS-07B19.md) · [التحقق والخطط](VALIDATION-07B19.md) · [المتبقي](PHASE-07-REMAINING-07B19.md) · [scope23](review-scope-07B19.csv) · [السجل](findings.csv) · [provenance523](evidence/provenance-07B19.json) · [stdoutB19](evidence/checks-07B19.json)

## 1. قرار النطاق والحصيلة

اختيرت من [متبقي B18](PHASE-07-REMAINING-07B18.md) و[SP7B18-01](evidence/split-register-07B18.csv) حواف **التوجيه والهوية والتهيئة والقراءة والمسودة وحد الحفظ** في والدين مسميين: تقرير حركة المادة التفصيلي وقائمة الفواتير المخزنية، إلى سبعة مستقبلين. [قرار النطاق](evidence/scope-decision-07B19.json) يثبت السبب والمدخل والمخرج والاستبعاد. هذه متابعة لعقد مصدر التقرير وفتح صفه، لا بدء محور WPF العام في7C ولا تدقيق كامل لسبعة محررات أو محركات كتابة.

- **خمس علل محلية جديدة P7-131…135**: اثنتان High وثلاث Medium؛ أربع confirmed من المصدر بشروطها وواحدة potential تتعلق بترتيب التهيئة. لا حادث إنتاج أو خسارة مقاسة أو معالجة.
- التراكمي **307 مفتوحة بلا معالجة**:2Critical/180High/124Medium/1Low، و269confirmed/31potential/7repository-gap. المرحلة7=135 نتيجة، لا135 ميزة.
- **صفر امتدادات تاريخية.** كل302 صف سابق، كل حقل وALLnext_phase والأدلة والتصنيفات والبادئة الخام، وG01–184 و523 مادة محمية و827 مساراً أصلياً/بصمة محفوظة. لا إصلاح مفترض للأصول المالية أو المخزون أو الهوية.
- [NV22](evidence/navigation-ledger-07B19.csv) **22 حالة توجيه من19 موضع Navigate نصياً في والدين** إلى [LC7](evidence/leaf-contract-ledger-07B19.csv) **سبعة حدود استقبال منتقاة**. تتشارك8 حالات نوع بالمخزون5 helpers؛ والتفصيلي14 موضعاً، وaliases الأسماء لا تضيف مواضع نداء. ليست هذه كلcallgraph أو حصر قدرات أو إثبات وصول منشور.
- **18 عقداً/18 ثابتاً/6 عقود مقارنة و36 خطة قبول كلها غير منفذة**. تبقى14 بقية منB18 منسوبة بـupstream rowSHA، و3 splits صريحة و6H/6Q غير معتمدة خارجياً.

## 2. عمق القراءة وحساب المسارات

[النطاق](review-scope-07B19.csv) **23 مساراً بشرائح مسماة**:21 تتداخل مع الاتحاد السابق408 ومساران جديدان؛ الاتحاد410 والمكمل417=352source/61generated/4project-resource. الجديد مسارا XAML للمناقلة والتسوية، لا جسمان كاملان أو ميزتان جديدتان. توجد مقاطع غير مستكملة داخل410 أيضاً؛417 ليست417 مهمة7C أو مقام نسبة إتمام.

قُرئت عناوين وتصنيفات302 سابقة لتحديد أقرب الجذور، ثم سلاسل مصدر مختارة منها، لا كل التاريخ أو كل عقد نشر. فُك `FormPermission.cs` بـcp1256 للقراءة فقط دون إعادة ترميز. يسجل شاهد Python68 قراءة نصية محدودة في22 مساراً؛ النطاق23 يضم دعم الصلاحيات ومقاطع دعم إضافية مثلmigration. لا تمثل68 كل قراءة أو مراجعة دلالية.

| المسار | الشرائح | عمق القراءة وحده |
| --- | --- | --- |
| SmartAuditERP/Class/Common.cs | 1247-1301;1435-1490 | حارس الفترة المعروف وحارس تعديل UI؛ دعم لحافة الحفظ لا تفويض مصدر موثوق أو مراجعة كامل Common. |
| SmartAuditERP/Class/FormPermission.cs | 38-178 | تطبيق منح الواجهة في شرائح مسماة؛ قراءة cp1256 فقط بلا إعادة ترميز؛ لا grants أو صلاحيات نشر مثبتة. |
| SmartAuditERP/Class/InvoiceOper.cs | 1497-1535;3219-3281;3496-3509;4186-4248 | BindingInvoice false/null وخريطة تاريخ الموجود ومعامل @date؛ لا كل materializer أو SaveInvoice أو المعاملات/SQL. |
| SmartAuditERP/Class/StoredQueries.cs | 6-10 | النصوص المرفقة لرأس Inv، وإسناد @date وحاجز معاملات إنتاج سابق؛ ليست SQL منفذة أو schema نشر. |
| SmartAuditERP/Form_WPF/frmInvInputOutput.xaml | 1-16 | ربط Loaded فقط. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs | 94-130;162-201;483-500;502-618;690-710 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmInvInputOutput؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Form_WPF/frmInvPOS.xaml | 1-16 | ربط Loaded فقط. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs | 210-270;512-553;621-641;1009-1028;1861-1881;1901-1974;2012-2056;2170-2211 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmInvPOS؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Form_WPF/frmInvPurch.xaml | 1-16 | ربط Loaded فقط. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs | 97-160;350-407;481-504;506-546;1196-1335;1571-1589 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmInvPurch؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Form_WPF/frmInvSale.xaml | 1-16 | ربط Loaded فقط. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmInvSale.xaml.cs | 67-94;123-235;1546-1610;1643-1661;1663-1682;1860-1912;2537-2570 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmInvSale؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml | 1-18 | ربط Loaded فقط. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs | 126-160;286-328;402-451;523-544;797-1029;1520-1563 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmInventoryTransfer؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Form_WPF/frmProductionOrder.xaml | 1-16;487-511 | ربط Loaded فقط وتنسيق حقول كمية/سعر مكونات الإنتاج. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs | 100-124;510-578;854-1022;1026-1070;1274-1335;1352-1423;1425-1497;1907-2022 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmProductionOrder؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Form_WPF/frmRptInventory.xaml | 454-486 | Tag الصف وزر مصدر المستند؛ ربط محلي فقط لا كامل XAML أو قالب طباعة. |
| SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs | 490-635 | dispatcher SelectedIndex0..7 وخمسة helpers إلى أوراق التحرير؛ InvGlobalID/ProcType وترتيب Show ثم Navigate؛ لا كل التقرير. |
| SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml | 708-720 | زر فتح المستند وربط الصف؛ لا rendering أو كامل XAML. |
| SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs | 285-309;1011-1191 | حقول الصف label/localNo و14 موضع Navigate في switch وconfigure قبل Show؛ لا body كامل جديد أو كل المتصلين. |
| SmartAuditERP/Form_WPF/frmSafeAdjust.xaml | 1-16 | ربط Loaded فقط. لا كامل XAML أو rendering أو قبول واجهة. |
| SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs | 113-151;908-979;1096-1103;1105-1206;1368-1418 | شرائح مسماة لـ Navigate/reader وLoaded/reset وdirty وحافة حراس الحفظ في frmSafeAdjust؛ لا كامل المحرر أو كتّابه أو كل مداخل الوصول أو محور7C. |
| SmartAuditERP/Properties/Resources.resx | 954-1017;1692-1726;47207-47209;47828-47842 | CREATE Inv وSafesAdjust/Sub كشاهد عقد حقول مرفق، ودعم migrations Reff_No ومخزون التسوية؛ لا مخطط نشر أو كل AlterDb. |

دفتر455FE التاريخي فيB17 محفوظ بمقامه القديم، ولم تعد مراجعة كل أجسامه. لا تُضاف NV22 أوLC7 أوFE18 إليه على أنها ميزات مستقلة. lookup أوTag أووجود شرط أوUI ليس عقد ACL أوschema منشوراً.

## 3. العلل الجديدة

### P7-131 — فتح التسوية من قائمة المخزون يمرر رأس Inv إلى قارئ SafesAdjust

**Medium / confirmed / implementation-defect / open-not-remediated / next_phase=8.** المؤكد اختلاف المصدر وحقول القارئ في الشيفرة والمخطط المرفق؛ لا يثبت ذلك غياب تعديل في قاعدة نشر بعينها.

عند اختيار المخزون7، ينشئ `OpenSafeAdjust` نافذة جديدة ويرسل `SELECT * FROM Inv … inv_type=7 … InvGlobalID=…`. يقبل `frmSafeAdjust.Navigate` النص ثم يمرر reader إلى `ReadData`. ينسخ القارئ `id` إلىCode والتاريخ، ثم يقرأ `Is_Approved` الذي يخصSafesAdjust فيCREATE المرفق لاInv، وبعده يطلب `SafesAdjust_Sub WHERE Adjust_id=Code`. ليست هويةInv المحلية عقد ربط مثبتاً بهوية التسوية الأصلية.

**الشاهد المقابل:** يرسل التفصيلي إلى الورقة نفسها استعلامSafesAdjust. هذا يطابق اسم مصدر القارئ فقط، ولا يصادق على061 أو كل مرجع/فرع/إذن. عند غياب الحقل في مخطط يوافق المرفق يعرض catch خطأ بعد تعديل بعض الحقول؛ لا ندعي حفظاً خاطئاً أو فشلاً في كل نشر. حتى إضافة الحقل إلىInv لا تثبت صحة اختيار بنودSafesAdjust_Sub.

**الفصل:**061 هويةlabel/localNo/branch في التفصيلي؛017 اعتماد قبل نجاح الحركة؛030/113 أعمدة جرد/إشعار آخر. هذه علة عقد مصدر عند الفتح، لا إعادة عد لها ولا نتيجة أخرى لغيابApply. **اقتراح فقط:**SourceRef ونوع مصدر صريح، والتحقق من عقد القارئ قبل تعديل النموذج؛ لا إصلاح مطبق. **المالك:**WPF وDBA. **المدخل المنقح:**schema/migrations ومفتاح الربط ووصف المصدر؛ غيابه يحجب اعتماد هذا الفتح. **القبول اللاحق:**P7B19T-01–02 غير منفذتين.

**الدليل المحدد:** `SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206`؛ `SmartAuditERP/Properties/Resources.resx:954-1017`؛ `SmartAuditERP/Properties/Resources.resx:1692-1726`.

### P7-132 — فتح محرر الفاتورة من حركة المادة يحمّل المستند قبل Loaded الذي يعيد حالة الجديد

**High / potential / implementation-defect / open-not-remediated / next_phase=8.** الترتيب وتعليماتreset مثبتة نصياً، لكن أثرها علىWPF/DevExpress/DTO والإعدادات والمرور إلى الحفظ لم ينفذ؛ لذلك لا تُرفع إلىconfirmed ولا تدعى نسخة مستند محفوظة.

فيhelperي التفصيلي يسبق `configure(form/window)` نداءShow؛ وتنفذlambda بدورهاNavigate. يضعBindingInvoice عند العثور على صف `ISNew=false` ويستعيد الفرع والتاريخ. تربطXAML فيSale/Purch/POS/InputOutput/Transfer حدثLoaded بمعالجات تناديResetInvoice. تعيد تعليماتreset `ISNew=true` وفرع الجلسة وحقول تهيئة أخرى. إذا نجحload قبلLoaded ثم وصلreset، لا يحمي نجاح الهوية وحده حالة الموجود من التهيئة المتأخرة.

**حدود وشواهد:** قد يفشل الإعداد أو التحميل قبل هذه النقطة، وقد تختلف جدولة الأحداث أو تهيئةcontrols والـDTO الخارجي. تكتب5helpers بالمخزونShow قبلNavigate، وهو شاهد ترتيب مصدري معاكس **لا إثبات أنLoaded اكتمل**. Production وSafe لهما قارئان مختلفان، فلا تعمم عليهما علةISNew للخمس. لا نجزم بمسح كل البنود أو تجاوزACL أو حفظ نسخة مكررة.

**الفصل:** حتى معDocumentRef وallowed-set صحيحين قد يفسدlate-reset الحالة؛ ليست061 أو فحصUI فيP1-013 أو خليطrequest/results في045. **اقتراح فقط:** فصلInitializeNew عنLoadExisting معحالة/generation مثبتة قبل النشر. **المالك:**WPF والمنتج. **المدخل المنقح:**نسخSDK وعقدDTO وسياسةinit/load/Loaded. غيابه يبقي132 محتملاً واعتماد التحرير محجوباً. **القبول:**P7B19T-03–04 غير منفذتين، معfresh/reopen وحالات فشل ومقارنة الترتيبين.

**الدليل المحدد:** `SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:123-235`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1610`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:97-160`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-407`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:210-270`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:512-553`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml:1-16`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:94-130`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:162-201`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml:1-18`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:126-160`؛ `SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:286-328`؛ `SmartAuditERP/Class/InvoiceOper.cs:3219-3281`.

### P7-133 — إعادة فتح الإنتاج لا تستعيد BaseQty فتتوقف إعادة تحجيم المكونات أو تصفرها عند تغيير الوحدة

**Medium / confirmed / implementation-defect / open-not-remediated / next_phase=8.** العيب في إعادة بناء الكائن المحلي، لا حكم بوصفة النشر أو حفظ فاسد شوهد.

يعيدProduction.ReadData رأسInv ثم المنتج `productId=0` ومكونات `productId>0` منInv_Sub. ينشئProductionItemRow لكل مكون بكمية وسعر ووحدة ومخزن، لكن لا يسندBaseQty أوUnitEquality. النوع محلي ظاهر: الحقل`_baseQty` بلاinitializer أي0، و`_unitEquality=1`، والـsetters لا تستنتج معامل الوصفة منQty.

عند تغيير مقدار المنتج، يحرس حدث الكمية `row.BaseQty>0` فيتجاوز المكون المعاد تحميله بمعامل أساس0 بدلاً من إعادة تحجيمه. **لا يصفر حدث الكمية هذا السطر.** أما حدث وحدة المنتج، بعد خروج`_isLoaded` ووجود الصنف والوحدة وperc، فيضرب `perc * row.BaseQty * qty` بلا الحارس نفسه؛ قد يصير المكون صفراً. مثال يدوي: مكون8 يبقى8 مع تغيير مقدار المنتج إلى3؛ وفرع الوحدة بـBaseQty0 يعطي0. لا نعتمد ما يفترض أن يكون المعامل الصحيح بلاBOMpolicy.

**الفصل:**P4-022 يقارن معادلتين عندBaseQty موجب وعاملي وحدة مختلفين. هنا يفقدreader المعامل بصرف النظر عن صحة تلك المعادلة؛ توحيد المعادلتين لا يعيده. حاجزParameters فيP4-020 باقٍ، وP4-021 احتمال هوية تعديل بعده؛ لا نقفز منbinding إلى حفظ يتيم أو ناجح.

**اقتراح فقط:** إعادة معاملات الوصفة والوحدات من مصدرhistorical موثوق أو منع التحجيم معسبب، لا قسمة تخمينية على كمية المنتج. **المالك:**الإنتاج والمخزون. **المدخل:**قاموسBOM/as-of/base/equality ووحدات منقح؛ غيابه يحجب اعتماد حسابات التحرير المشتقة. **القبول:**P7B19T-05–06 غير منفذتين، مع كمية ثم وحدة وإلغاء وشواهد غير صفرية.

**الدليل المحدد:** `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511`.

### P7-134 — قارئ مكونات الإنتاج يقرب الكمية والسعر قبل بناء نموذج التحرير

**Medium / confirmed / implementation-defect / open-not-remediated / next_phase=8.** التقريب المبكر تعليمة قراءة مثبتة، لا سياسة دقة مستنتجة من الموقع أوN2، ولا واقعة خسارة بيانات منشورة.

داخل حلقة مكوناتReadData تطبقMath.Round إلى منزلتين على `val1` و`exchange_price` قبل إسنادهما إلىQty/Price فيProductionItemRow، ثم تحسبTotal من الناتج المقرب. ليست الحالةStringFormat=N2 فيXAML فقط؛ كائن التحرير نفسه يفقد جزءاً من قيمة المصدر.

**مثال استقلالي بعيد عنmidpoint:**كمية0.004 وسعر1000.004 يتحولان في النموذج اليدوي إلى0.00 و1000.00 ومجموع0.00؛ وكمية2 بسعر1.234 تعطي2.46 محلياً بدلاً منraw2.468. في المقابلqty2/price1.25 تبقى2.50. هذهDecimal توضيحية، لا اختبارbinarydouble أوSQL. دقة السعر/الكمية المطلوبة عند المالك؛ ليست دعوة لحفظraw بلا حدود أو سياسة.

**الفصل:** ليستP3-007 فحص توازن قيد، ولاP4-022 عامل تحويل، ولاP6-004 محول ضريبة، ولا096 تفاصيل تقرير. سبب القارئ مختلف وإصلاحه وحده لا يتجاوز020/021. الحفظ المحلي مكتوب ليستهلكrow.Qty/Price، لكن لا حفظ ناجح مفترض معحاجز المعاملات الحالي.

**اقتراح فقط:** احتفاظ النموذج بالدقة المقررة وفصل العرض عنها، ومقارنة قبل/بعد إعادة الفتح؛ لا تغيير تطبيق أو مخطط. **المالك:**الإنتاج والمحاسب ومالك الدقة. **المدخل:**قاموسquantity/price/currency/rounding ووصفة اصطناعية منقحة؛ غيابه يحجب اعتماد ذهاب وإياب الدقة. **القبول:**P7B19T-07–08 غير منفذتين، دون تجربةsave قبل إذن مستقل وحسم الحواجز.

**الدليل المحدد:** `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511`؛ `SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497`.

### P7-135 — إعادة حفظ POS غير الإلكتروني تستبدل تاريخ الفاتورة المحملة بوقت الحفظ

**High / confirmed / implementation-defect / open-not-remediated / next_phase=8.** الثابت إسناد تاريخ مختلف إلى طلب الكتابة للموجود غير الإلكتروني؛ الأثر المنشور مشروط بالسماح ونجاح الحفظ، لا خسارة أو حكم امتثال قانوني.

يسندBindingControls تاريخInvoic.InvDate إلىtxtDate_Value ويعرضه. يفحصbtnPay الفترة على هذه القيمة، ويحوي حراساً حقيقية للموظف والبنود والدفع بحسب الحالة. تنقلMappingInvoice تاريخDGV إلىInvoice؛ ثمSaveAndPrint، إضافة إلى فرع الجديد، ينفذ للموجود حين`!EnableE_Invoice && !Invoic.ISNew` إسناد`invoice.InvDate=DateTime.Now`. يمرSaveInvoice عبر@date إلىUpdateInv في العقد المرفق بدلاً من تاريخ المستند المحمل والمعروض.

**مثال شرطي:** فاتورة31ديسمبر يعاد تحريرها في2يناير دون طلب تغيير تاريخ؛ قد تصير كتابة التاريخ2يناير، فيتغير انتماؤها للفترة وتقارير الحركة إذا اكتمل الحفظ. الموجود الإلكتروني لا يأخذ هذا الفرع نفسه، وقد يمنعه من التعديل حارس آخر؛ الجديد حالة مختلفة. ليست كلPOS تفقد تاريخها، ولا يثبت أن العرض يعكس التاريخ الجديد بعد الحفظ.

**الفصل:**P3-001 يحسم حارس الفترة المعروف دائماًtrue، ولا يفسر استبدال تاريخ الموجود.025 اختلاف إشعار/قيد، وP6-015 توصيفzone/ETA، و045 طلب/نتيجة؛ إصلاحها لا يحذف إسنادNow. لا يعتمد التحليل على حاجز132: يمكن فحص موجود بعد تهيئة مكتملة؛ ولا تفترض حراس الصلاحية والدفع متجاوزة.

**اقتراح فقط:** فصلissue-date عنmodified-at، وتمرير تاريخ المستند المقصود إلى حواف الحفظ والقيد والنشر بسياسة تصحيح صريحة. **المالك:**POS والمحاسب. **المدخل:**سياسة تاريخ/فترة/zone وتعديل مأذون بأمثلة اصطناعية؛ غيابه يحجب اعتماد مقارنة الفترات ورواية أن التاريخ هو تاريخ الإصدار. **القبول:**P7B19T-09–10 غير منفذتين، معالموجود الإلكتروني والجديد والرفض كشواهد.

**الدليل المحدد:** `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1009-1028`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2170-2211`؛ `SmartAuditERP/Class/InvoiceOper.cs:1497-1535`؛ `SmartAuditERP/Class/StoredQueries.cs:6-10`؛ `SmartAuditERP/Class/InvoiceOper.cs:4186-4248`.

## 4. الحدود والشواهد التي تمنع التعميم

- يبقى061 لهوية المستند بالاسم/الرقم المحلي في التفصيلي. المخزون يحملGlobalID/ProcType كشاهد، لكنه لا يثبت مصدرsafe أوACL أوfreshness عند تغيرSelectedIndex.
- عدمCheckBeforeClear داخلNavigate لا يكفي لنتيجة فقد مسودة: الآباء المختارون ينشئون نوافذnew، وبعضtoolbar يفحص الحارس. إعادة استعمال محرر قديم خارج الشرائح تحتاج تتبعاً صريحاً.
- يعيدBindingInvoice قيمةnull لغياب الصف أو الاستثناء؛ لا يفصلhealth. هذا حد متتبع لاfinding عددية أخرى، ولا يسمى النموذج الجديد اللاحق صحيحاً للترحيل.
- الحراس الفعلية للطرف والمندوب والدفع والتعديل باقية. تفاوتSave/SavePrint فيP4-031، وP4-017/018/019 و020/021/022 وP1/P2ACL لم تعالج ولا تُعد ثانية.
- CREATE المرفق ليسschema نشر. مثال ضرورة التحفظ: يغيرmigration نوعReff_No إلىvarchar20؛ لا نستنتج تعارضاً دائماً منint فيCREATE. دعم `SmartAuditERP/Properties/Resources.resx:47207-47209` و`SmartAuditERP/Properties/Resources.resx:47828-47842` لحدود المخطط فقط، لا قبول ترحيل أو نفي تحديثات أخرى.
- لا وصول خادم أو تراخيصSDK أو عقدBOM أوmanifest أوgrants أوثقافة مفترضة. DBNull أوcatch أو اسم نافذة لا يعتمد كلقارئ أو جدولة حدث.

## 5. الفصل السببي والحفظ والمتابعة

| المعرف | الجذر الحالي / الأقرب | التصرف والسبب المحدود |
| --- | --- | --- |
| AD7B19-01 | P7-131 / P7-061;P4-017;P4-030;P7-113 | new-local-root — عقد جدول وحقول عند فتح التسوية، لا هويةlabel/branch في061 ولا اعتماد017 أو أعمدة تقييم030/Notes113. يطلب القارئ حقلاً من مصدر آخر. |
| AD7B19-02 | P7-132 / P7-061;P1-013;P7-045 | new-local-root — حتى مع DocumentRef وACL صحيحين قد يأتي reset بعدload. سبب init/order مستقل عنlabel061 أوvisual-permissions013 أوfreshness045؛ مصنفpotential لا.NET منفذ. |
| AD7B19-03 | P7-133 / P4-022;P4-020;P4-021 | new-local-root — يفترض P4-022 BaseQty موجباً ويقارن عاملَي وحدة. هناreader لا يعيدBaseQty أصلاً؛ إصلاح تطابق المعادلتين لا يعيد المعامل المفقود. حواجز020/021 محفوظة. |
| AD7B19-04 | P7-134 / P3-007;P4-022;P6-004;P7-096 | new-local-root — تقريب ReadData قبلmodel يبدل قيمة المصدر، مستقل عن فحص توازنdouble في007 أوتحويل022 أو محولضريبة004 أوتفاصيل تقرير096. ليست كلMath.Round جذراً واحداً. |
| AD7B19-05 | P7-135 / P3-001;P3-025;P6-015;P7-045 | new-local-root — حارس الفترة001 معروف دائماًtrue؛ هنا يستبدلPOS issue-date بـNow دون تغيير تاريخ مقصود.025 اختلاف إشعار/قيد و015 توصيفtimezoneETA، لا التعليمة نفسها. |
| AD7B19-06 | P7-061 / P7-061 | retained-prior-roots-no-recount-no-registry-extension — أعيدت ملاحظةlabel/localNo بحدود061؛GlobalID بالمخزون شاهد، لا أصل جديد أوإذن مثبت. |
| AD7B19-07 | P4-020;P4-021;P4-022 / P4-020;P4-021;P4-022 | retained-prior-roots-no-recount-no-registry-extension — نقصParameters والهوية والتحويل لم تعالج؛ لا يرقىbinding إلىحفظ ناجح ولا يرفعpotential021. |
| AD7B19-08 | P3-001;P4-031;P1-013;P2-001;P2-006 / P3-001;P4-031;P1-013;P2-001;P2-006 | retained-prior-roots-no-recount-no-registry-extension — الحراس وUI موجودة ومتفاوتة؛غيابApply أوprompt ليسfinding أخرى. ACL والنشر غير محسومين. |
| AD7B19-09 | P4-017;P4-018;P4-019 / P4-017;P4-018;P4-019 | retained-prior-roots-no-recount-no-registry-extension — اعتماد التسوية والاتصال ونتيجةالنقل أصولقديمة محفوظة؛ لا يشغلExecuteAdjustment ولا يدعي نجاح الطرفين. |

[AD9](evidence/root-adjudication-07B19.csv) يحتفظ بعمق المقارنة والدليل. لا يدعي المدقق الحكم آلياً على كلسبب بشري أو نثر تاريخي. تصويبB10 الإضافي **10 محلياً مقابل120 مرجعياً** باقٍ دون إعادة تحرير الأرشيف أوG138.

يحميB19 **523 مادة** خارج الخمسة المشتركة المتقدمة، وثلاثة تجميدات جديدة. يتلقىB18 التاريخيOWN302/exact303CRLF وفهارسه في الذاكرة، لا307 الحية. تعمل **كل28 حالةB18 الأصلية غير المعدلة** في طفل صريحpresetB18؛ لا توصف مطالبتها بـdefaultB18 بأنها اختبارdefault اليوم. الحاليbuild_cli_parser/entrypointB19 يختبر باستقلال، والتوافقB16/B17/B18 وmainAPI B15 باقٍ. لا تعديل مساعد أو اختبار محمي، ولاskip أوglobalPath/subprocesspatch أوdiskoverlay أوrebaseline أوarchiverewrite.

source10ba وentry/completedB18pushee393a7 وgenuineB18stdoutcheckout12d2e4b هويات مختلفة. [checksB18](evidence/checks-07B18.json) ببصمة`abe579df675cf7e0858eb209d8524d6c97cf663205f04b9515d2e76aade87c03` لا يعاد بعد الدفع. [المتبقي الحالي](PHASE-07-REMAINING-07B19.md) يبقيSP01 خارجNV22/LC7 وSP02 لحصر القدرات وSP03 للتفقيط/الباركود والعقود الخارجية مفتوحة. R4d/7B20 مقترح أوsplit مسبب، لا جلسة أخيرة مضمونة أو نقل بقية7B إلى7C بصمت.

## 6. حالة التحقق التوثيقي

نُفذت36 حالة مدقق جديدة بنجاح، و24 وضعية تاريخيةOWN بـerrors=[] وبصمات827، منهاB18 بـ302 و462 حالة/19 مجموعة وكل28 حالةB18 الأصلية. [السجل](evidence/historical-mode-verification-07B19.json) يحفظSHAstdout وexitcode؛ الحقول الغائبة قديماً تبقىnull لا0 تخميناً. شاهدB19 يحوي14 نموذجاً يدوياً و14 فحصاً نصياً و68 شريحة،errors=[]؛ ليستERP أو.NET.

نجح أيضاًCLI الحالي فعلياً، الافتراضي وB19 الصريح: **498 حالة مدقق عبر20 مجموعة،errors=[]**؛462 حالة سابقة و36 جديدة، لا اختباراتERP. وأعادت أداةbaseline المطابقة **827 ملفاً/29,128,444 بايت**، معXML parse errors0 وXAML name mismatches0 وdotnet_available=false؛لا بناء أو قبولbindings. يلتقط[checksB19](evidence/checks-07B19.json) stdout الأصلي مباشرة فيملف جديد حصري كمصب العملية، بلاplaceholder أو تعديلpendingflag أوself-hash. يبقىcheckout السجلee393a7 وقت الالتقاط مختلفاً عنcommit التسليم اللاحق، ولا يعاد الأرشيف بعدالدفع. **كل36 خطة قبول غير منفذة؛7B/7 جزئيتان؛7C لم تبدأ؛8 غير مأذونة.**
