# المرحلة7B33 / R4q — انتقال حالة وجهة PDF إلى الطباعة العادية

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**مدخل B33:** تسليم B32 المدفوع `3f747085b8f91762f7626dd45331ca1f5ba9e9c1`؛ **981 مادة تدقيق و334 نتيجة مفتوحة**. مرجع المتابعة **2026-11-16 UTC** منفصل عن رصد ساعة البيئة الخام عند التجميد `2026-11-20T19:47:42.413048+00:00`؛ لا معايرة أو تأريخ رجعي أو تبديل لطوابع الأرشيف. [الهوية والتاريخ](DATE-IDENTITY-NOTE-07B33.md).

**تدقيق ساكن فقط؛ لا تعديل للتطبيق أو إصلاح أو تشغيل ERP. R4q شريحة محدودة؛7B والمرحلة7 جزئيتان؛R4r/7B34 مقترح أوsplit مسبب؛7C لم تبدأ؛8 غير مأذونة هنا.** الإصلاح في فرع ومحادثة مستقلين،وبدؤه وتزامنه غير معلومين؛لا دمج repair→audit أوكتابة ملفاته أوإغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[النتيجة](PHASE-07B33.md) · [عقود المخارج](OUTPUT-ROUTE-CONTRACTS-07B33.md) · [التحقق](VALIDATION-07B33.md) · [المتبقي وسلطة المتابعة](PHASE-07-REMAINING-07B33.md) · [الهوية](DATE-IDENTITY-NOTE-07B33.md) · [النطاق](review-scope-07B33.csv) · [قرار الاختيار](evidence/scope-decision-07B33.json) · [السجل](findings.csv) · [stdout الرسمي](evidence/checks-07B33.json)

## 1. قرار النطاق من SP7B32-01

**الأحدث:7B33/R4q؛P7-163 واحدة Medium/confirmed مصدرية،وصفر امتدادات تاريخية.** التراكمي **335 نتيجة مفتوحة بلا معالجة:2Critical /181High /151Medium /1Low؛296confirmed /32potential /7repository-gap**.

- **جذر واحد:** يكتب تصدير PDF اسم `Microsoft Print to PDF` في `print.defPrinter` المشتركة للـinstance. لا توجد استعادة في جسم wrapper المختار؛الطباعة العادية تستبدل القيمة فقط عندما تكون فارغة،فتمرر PDF غير الفارغة للطلب التالي.
- **الشروط:** نفس instance،مستند وأعلام printed/clean موردة صراحة،رجوع mapping،وصفوف وURL وmain report تمر من بوابات المصدر،ورجوع التحضير عند تتبع دخول المحرك؛لا كاتب آخر بين الطلبين. لا يلزم فشل أوحدث مكرر أوترك مسودة.
- **الخاصية ليست الوسيط:** picker غير الفارغ وtype3/طابعة القالب قد يغيران string parameter المحلي دون ردّ التغيير إلى الخاصية. قد لا يستخدم طلب معين PDF؛type2 معاينة لا طباعة عادية. بوابات grid0/URL/file قبل الكتابة ضوابط مضادة،وفشل BindToData بعد الكتابة لا يعيد الأصل.
- **ليس دليلاً على جهاز:** الأثر المثبت هو قيمة إعداد الذاكرة والطلب التالي المشروط،لا تركيب طابعة أوPDFCreated أوورق أوspool accepted أوتغيير SettingPrint/Windows default أوخسارة مالية.
- **حدود معلنة:**20 شريحة تعاقدية و9 سياق في6 مسارات سابقة؛0 ملف كامل.6تقاطع+0جديد→اتحاد427/متمم400؛لا نسبة قدرات أو400مهمةC. ترشيح334metadata و37صف سجل مطابق لخمسة paths وقراءة24قسم finding منتقاة ليست قراءة كل المتون أوحصر455FE.

**سلطة الاختيار:**[متبقيB32](PHASE-07-REMAINING-07B32.md) وRS14/SP3/workplan/backlog التابعة له،ثم [القرار المحدد](evidence/scope-decision-07B33.json). المالك:WPF والتقارير وملكية طابعة المحرر؛المدخل المنقح:OutputRequest ونسخة إعداد وpolicy للأولوية والفشل،معرجوع mapping/binding صريح؛غيابه يبقي نتيجة الجهاز وSDK غير محسومين. المخرج:خاصية الذاكرة ووسيط الطلب التالي المشروط فقط. الخروج الساكن:حدود الكتابة والبوابات والتجاوزات وأثرها وdedup موثقة؛القبول التشغيلي يحتاج إذناً وعقوداً لاحقة.

[OS8](evidence/output-state-lineage-07B33.csv) · [OV8](evidence/route-override-lineage-07B33.csv) · [FE16](evidence/feature-implementation-matrix-07B33.csv) · [INV16](evidence/report-invariants-07B33.csv) · [32 خطة](evidence/acceptance-tests-07B33.csv) · [RC6](evidence/report-reconciliation-07B33.csv) · [AD8](evidence/root-adjudication-07B33.csv) · [امتدادات0](evidence/historical-extensions-07B33.csv) · [شاهد20+20](evidence/output-route-witnesses-07B33.json) · [حد ترشيح التاريخ](evidence/dedup-screen-07B33.json) · [RS14](evidence/residual-disposition-07B33.csv) · [SP3](evidence/split-register-07B33.csv) · [H6](evidence/handoffs-07B33.csv) · [Q6](evidence/questions-07B33.csv) · [workplan10](evidence/remaining-workplan-07B33.csv) · [backlog10](evidence/continuation-backlog-07B33.csv)

## 2. النتيجة الجديدة الوحيدة

### P7-163 — تصدير PDF يترك طابعة محرر البيع على Microsoft Print to PDF للطلب العادي التالي

**Medium؛confirmed لكتابة الخاصية المحلية وحملها المشروط إلى الطلب التالي؛implementation-defect؛open-not-remediated؛next_phase=8 تخطيط فقط.** ليست نتيجة جهاز أو تجربة واجهة.

**دليل الملكية:** يعلن `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:34-34` حقل `Print` غير ساكن، وينشئه المنشئ في `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:65-78`. وتعرّف `SmartAuditERP/Class/Print.cs:38-38` خاصية محلية تلقائية. لا نحتاج افتراض setter خارجي لإثبات هذه الكتابة.

**مدخل الطلب:** قائمة PDF موصولة في `SmartAuditERP/Form_WPF/frmInvSale.xaml:1187-1191`، وزرا الطباعة والمعاينة في `SmartAuditERP/Form_WPF/frmInvSale.xaml:1251-1259`. يفحص `ExportPDF_Click` و`btnPrint_Click` الشرط `IsPrinted && !IsUpdated`، ثم يقيّمان `MappingInvoice` قبل استدعاء wrapper بالنوع1؛الدليل `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3201-3208` و`SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2581-2595`. الأعلام ورجوع mapping شروط صريحة هنا، لا إثبات لحفظ كل مستند أو لسلوك جميع setters.

**السبب عند الحد المحلي:** ترجع `RptPrintPDF` مبكراً مع grid0 أو URL فارغة أو غياب ملف التقرير الرئيسي. بعد تجاوز هذه البوابات تكتب `print.defPrinter = "Microsoft Print to PDF"`، ثم تقيّم `BindToData` وتطلب الإخراج. لا توجد استعادة للقيمة الأصلية أو `finally` في جسمها المحدد؛`SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2093-2124`. في المقابل لا تستبدل `RptPrint` العادية الخاصية بـ`MainClass.ReportsPrinter` إلا عند الفراغ؛`SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2041-2091`. اسم PDF غير فارغ، ولذلك يمر إلى الطلب العادي التالي في نفس الكائن، ما لم يكتب متدخل آخر بينهما.

| التسلسل المحدود بنفس الـinstance | الخاصية بعد PDF أو بوابته | وسيط الطلب العادي التالي |
|---|---|---|
|fixture-paper-A → PDF مع البوابات الموجبة ورجوع التحضير → normal|Microsoft Print to PDF|Microsoft Print to PDF إذا وصل normal إلى المحرك|
|fixture-paper-A → normal دون PDF سابق|fixture-paper-A|fixture-paper-A|
|رفض PDF عند grid0 أو URL/file قبل الكتابة|fixture-paper-A|fixture-paper-A مع بوابات normal موجبة|
|عدم رجوع BindToData بعد كتابة PDF|Microsoft Print to PDF|يبقى الأثر إن أمكن طلب normal لاحقاً؛لا يلزم دخول المحرك للطلب الأول|
|instance مستقلة ببداية fixture-paper-B|لا مشاركة في النموذج مع الكائنA|fixture-paper-B؛لا تغيير عام في Windows default أو DB مدعى|

**تغيير الخاصية ليس نجاح PDF:** الكتابة سابقة لتقييم `BindToData`؛عدم رجوعه يمنعنا من ادعاء دخول `Printing` أو استقرار حالة الواجهة أو تعافٍ تلقائي. وحتى الرجوع الطبيعي من `Printing` لا يثبت إنشاء ملف أو وصول ورق:توقيعه `void` وcatch المبتلع ضمن P7-031. الاسم الثابت لا يثبت تركيب تلك الطابعة أو ظهور حوار حفظ أو وجود مسار ملف فعلي.

**الخاصية والوسيط كيانان مختلفان:** تقبل `SmartAuditERP/Class/Print.cs:148-221` وسيط string دون `ref/out`. إذا كانت `PrintersList` موجبة و`SelectedPrinter` غير فارغة يغير المحرك وسيطه المحلي واسم القالب المحلي. وبعد تحميل التقرير قد يتجاوز النوع3 بقيمة `report.PrinterName` غير الفارغة اختيار picker أيضاً؛النوع1 المختار لا يسلك شرط3. لا يكتب هذا الجسم `this.defPrinter`. لذلك لا تعد طابعة اختارها المستخدم للطلب الأول استعادةً لخاصية المستدعي. وقد يتجه طلب بعينه إلى picker لا PDF؛ليس كل تصدير أو كل طلب عادي متأثراً بصورة واحدة.

**ضوابط أخرى محفوظة:**

- النوع2 يستدعي `ShowPreviewDialog`،لا `Print` من ذلك الفرع. لم نراجع أزرار واجهة المعاينة اللاحقة أو ننفها.
- تمرر kitchen recursion اسم طابعة منفصلاً لنداء آخر؛لا تخلط خطط القبول عدد طلباتها بعدد النسخ الرئيسية أو أوراق نجحت.
- قيمة copies0 أو السالبة التي تسقط في طباعة واحدة هي P7-030 القائمة،لا نتيجة جديدة. فشل أول `Print` المورّد يمنع بقية الحلقة وحد kitchen في ذلك المثال،ولا يثبت نجاح أي ورقة.
- المشتريات ضابط محرر مستقل،و`Print2` يغير `RptName` لا يعيد `defPrinter`. لا نعمم علة البيع على كائن آخر،ولا نحول غياب شرط dirty نصي في purchase إلى عيب مؤكد دون عقد DTO.

**الأثر والمقترح غير المنفذ:** يبدل أمر تصدير واحد وجهة طلب عادي لاحق في نفس الكائن،بدلاً من اختيار وجهة خاصة بالعملية،بشروط المصدر المذكورة. اقترح `OutputRequest` مستقلاً يحمل الوجهة والقالب والنوع،مع أولوية معلنة لـpicker/template و`OutputOutcome` منفصل عن `SaveResult`. وإذا اختير تصميم استعادة حالة مشتركة،فتحتاج حدود الاستثناء وإعادة الدخول إلى عقد؛إضافة `finally` وحدها ليست اعتماداً لكل الأوامر. لا إصلاح للتطبيق هنا. خطط P7B33T-01–16 وضوابط17–32 كلها غير منفذة.

## 3. منع التكرار وحدود الاستدلال

يحفظ [AD8](evidence/root-adjudication-07B33.csv) و[تسجيل الترشيح](evidence/dedup-screen-07B33.json) فحص334 عنواناً/metadata و37 صف سجل مطابقة لخمسة مسارات،وقراءة24 قسم finding قديم منتقاة. ليس ذلك قراءة كل334 متناً أو جميع مصادرها. أعداد20 شريحة تعاقدية و9 سياق تخص القراءات المختارة للتوثيق،لا كل grep أو اطلاع تمهيدي ولا شهادة لكامل الملفات.

- **P7-030/031/103/104:** عدد النسخ،غياب نتيجة الإخراج،تحميل إعداد sett،ونجاح كتابة صفر صف. إصلاح هذه الآليات وحده لا يستعيد خاصية غير فارغة في محرر البيع.
- **P7-032/033/140 وP6-033:** هوية بيانات حية وتفاصيل سيريال وإسقاط عملة ونتيجة إرسال؛ليست حمل اسم طابعة إلى الطلب التالي.
- **P7-162/126 وP6-035:** تكرار اشتراك أو تداخل أحداث أو إرسال SMTP. هنا طلب PDF ثم normal مقصودان ومتتابعان،لا معالج تكرر.
- **159/160/161/046/115/157/158:** حارس قبول بحث،ذيل إدراج غير مقبول،preclear عند Empty مع clean،لقطة جزئية،مصدر سنة،allowed-set،وإزالة مرشح. يثبت163 دونها على مصدر محفوظ clean ورجوع mapping مورّد.
- لا إعادة عد لـP4-015 الخاصة بالدفع قبل التأكيد،ولا P3-005 لتزامن الترقيم. لا يلزم نمط إعادة فتح نافذة Closed في P1-030 لطلبين على instance مفتوحة. تبقى132/145 وعقود dirty غير المحسومة ضمن حدودها السابقة؛لا absence proof جديدة من purchase أو من غياب مصدر SDK.

## 4. الحفظ والتحقق والمتابعة

حُفظت **976 مادة دخول محمية من981 بايتياً**،و**كل334 قاموس نتيجة بكل حقل** بما فيها جميع `next_phase` والأدلة والتصنيف والشدة واليقين والحالة. **بادئة raw335CRLF كاملة دونBOM مطابقة**؛الحالي335نتيجة وraw336CRLF،و163 وحدها مضافة. لا إلحاق لجذر سابق. **G01–248 محفوظة حرفياً**،وG249–252 توصيات غير منفذة لا أربع نتائج أخرى.

بقيت **827 أصل تطبيق /29,128,444 بايت** والتجميدات الثلاثة ولقطةdispatcher النصية الإضافية مطابقة. تشمل الحماية تقاريرB32 وEO8/DG8/FE16/INV16/RC6/AD8/32خطته وشاهده وأرشيف37 وبرهانه وstdoutه الرسمي وإيصال الالتقاط،وB31 NL8/LO8 وكل محاولاته ومذكراته وB30 IC8/IR8/ext1 وB29 DN8/NO6 وأرشيفيه ومحاولته غير المكتملة وB28/158 وتوسعة046 والكل الأقدم. لا إعادة توليد أوإعادة وسم لأي archive/stdout قديم أوإعادة تشغيل لكاتب حصري مستهلك.

تبقى P7-161 known-empty/preclear و159 guard omission و160 nonaccepted-import→current-editor و162 duplicate subscriptions جذوراً مختلفة. ذيل159 المقبول فيB30 ثابت كما دخل؛لا نتيجة لكلevent/key/editor/failure ولا استنتاج persisted loss. **P4-014 وP7-132 وP7-145 potential**،و020/021 وحواجز المال وACL والمخزون والحفظ والإنتاج ثابتة. تصحيحB10 الإضافي **10 محلياً مقابل120 مرجعياً وضابطequality1=10** باق دون إعادة تحريرG138.

**B32 التاريخي:** تعمل ALL52 الأصلية دون تعديل أوskip/filter/rebaseline في طفل `OWN334/raw335CRLF/indexes/presetB32`. تُورد **119 هوية مصدر تاريخية وdispatcher TEXT canonical** عبر `A` و`Path` محليين داخلmodule الاختبار فقط؛ليس ذلك تعداد أدوات التنفيذ الحالية أوoldcode. يدعم Path المحلي read_bytes/read_text و**open للقراءة فقط** وglob التاريخية،مع استعادة الهويات حتى عند الخطأ؛لا تتغير `v.__file__` أو`v.main.__code__` أوpathlib/shared-subprocess العامان ولاoverlay على القرص. تبقى مدخلات B31=115 وB30=111 وB29=107 منفصلة.

**محاولة مُهايئ محفوظة لا تُخفى:** فشلت المحاولة الأولى ذات52حالة فيtest47 لأن canonical `Path.open` في الاختبار المحمي قرأ السجل الحالي335،بينما غطى المُهايئ الجديد read_bytes/read_text فقط. [مذكرة01](evidence/historical-adapter-note01-07B33.json) تحفظ النتيجة المرصودة exit1/فشل1 ومصدر المساعد قبله؛**ليست raw stderr محفوظة أوSHA تيار مزعوماً**. صُحح المُهايئ الجديد وحده بإضافة open محلي read-only،ثم [عملية02 المباشرة](evidence/historical-adapter-note02-07B33.json) اجتازت ALL52/exit0؛stdout0 وstderr364بايت هيunittest/provenance عادية وليستstderr الخارجية للـCLI. تبقى المحاولتان منفصلتين،ولا تعديل لاختبارB32 أوإسقاط لأي حالة. التحقق التاريخي38 اللاحق مستقل جديد لا نسخ لنجاح02.

نُفذت **38 وضعية تاريخية OWN فعلياً**:2–6 وA وB1–32؛كلها errors[]/exit0/827 وstderr الخارجية فارغة. [الأرشيف](evidence/historical-mode-verification-07B33.json) **174256 بايت**،SHA-256:`be4e7d5aeafa9c70b9681df9e406b6e32efff6ed0e013d373b5c191e2e5f63a1`. يحفظ ملخصات عمليات جديدة حقيقية وهويات stdout وقت التقاطها مع **123 بصمة أداة تنفيذ**،لا streams كاملة أوprefix منB32 أوfixtures كدليل تنفيذ. `null` aggregate غير مبلغ عنه،لا صفراً.

[برهان الهوية](evidence/capture-time-identity-07B33.json) **8901 بايت**،SHA-256:`f1d5f71b2f9a1bb088553eff0a6aa04e10bab239c911efe844b85fcc3d8061b3`؛**122 أداة مطابقة +عكس pin واحد فقط** في helper بالذاكرة يعيدان بايتات123 أداة وقت الالتقاط بالضبط. لم يتغير الاختبار الجديد أوdispatcher بعد التقاط38،ولا رتبت hashes رجعياً. وضعB32 الأخير نفذ ALL52 الأصلية ضمن OWN334/1086/33 و119 مدخل assertion تاريخي؛لا ادعاء لإعادة38 كاملة بعد pin أوالنصوص والفهارس أوالدفع.

<!-- B33_CURRENT_VALIDATION_START -->
اجتاز **CLI الافتراضي الفعلي B33:1138 حالة وثائقية في34 مجموعة** =1086 حالة سابقة محفوظة +52 جديدة؛**335 نتيجة مفتوحة و827 أصلاً مطابقاً،errors[] وexit0 وstderr الخارجية فارغة**. هذا فحص متكامل مستقل بعد أرشيف38 والـpin وبرهان الهوية،لا استنتاج من نجاح52 حالة منفردة. جرى الفحص التمهيدي عند دخولB33 `3f747085b8f91762f7626dd45331ca1f5ba9e9c1`،والخرج المؤقت **321256 بايت**،SHA-256:`293dd3aa3b4317aa91c1caecd6b8122c831f4ce5f14718bea9e2883fbe9ef280`؛كل1020 مدخل تدقيق بقيت دون تغيير أثناء تلك العملية. لم يكن stdout الرسمي قد كُتب آنذاك،ولا يعاد وسم هذا الخرج التمهيدي بأنه رسمي.

[stdout الرسمي](evidence/checks-07B33.json) مخصص لعملية افتراضية جديدة مباشرة إلى ملف حصري **بعد إنهاء التقارير والفهارس**؛لا placeholder أوJSON مركب أونسخة منpreflight أوpostpush. هويته دخولB33 عند`3f747085b8f91762f7626dd45331ca1f5ba9e9c1` قبلcommit التسليم اللاحق؛إيصال `evidence/official-capture-receipt-07B33.json` يُكتب بعد خروجها ويثبت مدخلاتها،ولا يكون مدخلاً لذاته أوللـstdout. تحقق الإصدار المستقل هو ما يثبت نجاح الالتقاط النهائي وبقاء جميع مدخلاته،لا هذه الفقرة وحدها.

خريطةhashes القديمة المبلّغ عنها **113 كجزء**،وكل113 مطابقة؛الحقل المستقل الكامل يحصر **123 أداة تنفيذ فعلية** ويطابقglob مستقلاً. لا تساوى قائمة119 التاريخية لـassertionsB32 بكامل123،ولا يكرر افتراضB31 الخاطئ حول حجم الخريطة الجزئية. تبقى **كل32خطةB33 و32B32/B31/B30/B29/B28 و36B27 not-executed**؛1138 ليست اختبارات ERP أوWPF أوPDF/طابعة أوحفظ أوإصلاح أوقياس أوقبول تشغيلي.
<!-- B33_CURRENT_VALIDATION_END -->

لا ERP/build/C#/VB/.NET/WPF/SQL/DataView/provider/SDK/REPX/ToDataTable أو BAML أوطابعة/ماسح/PDF أوبيانات أعمال وأسرار أوحفظ/دفع/بريد أوإصلاح/قياس/قبول تشغيلي نُفذ هنا. الخاصية المحلية `defPrinter` معروفة من المصدر،لكن InvoiceDGV/setters/collections/Mapping/BindToData والعقود المنشورة لا تُحسم من قيم النموذج؛غياب تعيين `IsUpdated=true` صريح أوتعريف DTO متتبع ليس إثبات غياب حماية أوقدرة. كل32خطةB33 و32B32/B31/B30/B29/B28 و36B27 **not-executed**.

تبقى بقية callers/dialogs/editors/fields/writers/outputs وDocumentRef/allowed-set/branch/reset/dirty/cancel/failure وProduct/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome ضمن **SP01 و7B**. يبقى **SP02** حصر entry/source/output وcrosswalk455FE والدفاتر اللاحقة،و**SP03** SDK/DTO/constructors/collections/currency/precision/words/legacy/templates والسياسات ضمن7B صراحة. قراءة مخارج هذه الشريحة لا تفتتح محورC3 أوC4 العام ولا تنقل غير المراجع إلى7C.

اختر R4r/7B34 أوsplit مسبباً بقدرة وentry/source/output واستبعاد ودليل وحد ومالك ومدخل منقح وأثر وخطوة وخروج. لا وعد مدة أوجلسات أوآخر جزء أوإتمام النظام. يسلم SHA تدقيق مدفوع محدد للإصلاح المستقل دون افتراض بدئه أوتزامنه أودمج تعديلاته هنا.
