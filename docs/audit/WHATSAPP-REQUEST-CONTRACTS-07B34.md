# عقود طلب واتساب والانتظار — 7B34/R4r

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**مدخل B34:** تسليم B33 المدفوع `dea2244267d74dd540af59c6e63b0f4362ab8c1c`؛ **1022 مادة تدقيق و 335 نتيجة مفتوحة**. مرجع المتابعة **2026-11-16 UTC** مستقل عن رصد ساعة البيئة الخام عند التجميد `2026-11-20T20:42:25.020521+00:00`؛ لا معايرة للساعة أوتأريخ رجعي أوإعادة وسم لأثر مستهلك. [الهوية والتاريخ](DATE-IDENTITY-NOTE-07B34.md).

**تدقيق ساكن فقط؛ لا تعديل للتطبيق أو إصلاح أو تشغيل ERP. R4r شريحة محدودة؛ 7B والمرحلة 7 جزئيتان؛ R4s/7B35 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة هنا.** الإصلاح مستقل، وبدؤه وتزامنه غير معلومين؛ لا دمج repair→audit أوكتابة ملفاته أوإغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[الخلاصة](PHASE-07B34.md) · [عقود طلب واتساب](WHATSAPP-REQUEST-CONTRACTS-07B34.md) · [التحقق](VALIDATION-07B34.md) · [المتبقي وسلطة المتابعة](PHASE-07-REMAINING-07B34.md) · [الهوية](DATE-IDENTITY-NOTE-07B34.md) · [النطاق](review-scope-07B34.csv) · [قرار الاختيار](evidence/scope-decision-07B34.json) · [السجل دون تغيير](findings.csv) · [stdout الرسمي](evidence/checks-07B34.json)

**الأحدث:7B34/R4r؛صفر جذور جديدة وصفر امتدادات evidence للسجل.** هذا تعميق توثيقي للنتيجتين **P6-031 وP6-033**،لا P7-164 ولا نتيجة لكل await أوعنصر أومستلم أوملف. يظل التراكمي **335 نتيجة مفتوحة بلا معالجة:2Critical /181High /151Medium /1Low؛296confirmed /32potential /7repository-gap**.

- **السبب موثق سابقاً:** يذكر متنا PHASE-06 الجلسة المشتركة وتداخل chat واسم InvoiceNo والنتيجة الجزئية،ويقترحان تسلسل العمليات ومرفقاً immutable. التفصيل الجديد يحدد شروط الآلية وضوابطها،ولا يخلق سبباً آخر.
- **ما يتتبعه المصدر:** يحضّر `SendWhatsapp_Click→printwhatsapp` قيماً محلية ثم ينتظر Ensure والمرسل المشترك. بعد Navigate/await تبحث محددات عامة في سياق driver الحالي؛قيم mobile/message/pdfPath المحلية لا تثبت بقاء المحادثة المطلوبة.
- **تمييز لازم:** عنصر caption الملتقط قبل await يبقى المرجع نفسه؛لا يعاد توجيهه تلقائياً عند تنقل المتصفح. بقاء ارتباطه أوفشله كعنصر stale عقد خارجي غير محسوم؛المحددات اللاحقة حد آخر.
- **حد النتيجة:** File.Exists ومسار string ورمز version لا تثبت bytes قرأها المتصفح أوupload أوprovider acceptance أوDelivered. العودة true بعد click+delay محلية؛والعودة false بعد طلب النص لا تثبت رفض كل الأجزاء.
- **حد النطاق:**20 شريحة تعاقدية و8 شرائح سياق في5 مسارات سابقة،وصفر ملفات كاملة؛5 تقاطع+0 جديد→اتحاد427/متمم400. ترشيح335 صف metadata و33 صفاً مطابقاً لخمسة paths وقراءة20 قسماً منتقاة ليست قراءة كل المتون أوحصر455FE أوكل caller/SDK.

## 1. مفردات لا يجوز دمجها

| الهوية | نطاقهاالمصدرّي | حدالاستنتاج |
|---|---|---|
| mobile/message/pdfPath/inv المحضرة | قيم محليةقبل الانتظار؛ محتوى inv العميقوعقود mapping غيرمحسومة | لا يعادتقييمهاتلقائياًمنالواجهةولا يمكنعدها bytesimmutable |
| Session.waSender | حقل static يعادحلهعنداستدعاءالمرسلبعد Ensure | لايشهدعلىحسابمزودأوسياق ERP أوتسلسلحصري |
| driver و currentchat | حالةمشتركةداخل sender ؛ Navigate وتعاملاتالمحدداتاللاحقة | جدولة B قدتغيرها، لكنقبول DOM خارجيغيرمفترض |
| captionIWebElement | مرجعيلتقطمرةثم SendKeys و Enter علىنفسه | لا silentretarget ؛ stale وفشلوسلامةالمرجعحالاتموردةمستقلة |
| attach/fileinput/send المحددلاحقاً | قراءةجديدةبمحددعامعلى driver عندذلكالحد | لايرثهوية target من customerPhone المحليتلقائياً |
| pdfPath/latest-symbolic-version | مفتاحملفورمزنسخةداخلنموذجساكن | لا bytes مقروءةأومرفوعةأومقبولةعندمزود |
| true/false/Taskreturn | نتيجةمحليةومراحلمحاولة | ليست SaveResult أو Accepted أو Delivered أوضمان no-partial-effect |

## 2. دفتر ملكية الطلب RQ8

| المعرف | الحد | الملاحظةالمقيدة | السلسلة | الدليل |
|---|---|---|---|---|
| RQ7B34-01 | ملكية الأمر المتداخل عند مدخل واتساب | يفوض async void الخارجي إلى async void داخلي؛ يوجد await لاحق دون handle Task عند المدخل ∣ يلتقط inv و mobile و pdfPath و message محلياً قبل await ؛ Mapping/BindToData/Export عقود رجوع خارج هذا النموذج | قائمة SendWhatsapp → SendWhatsapp_Click → printwhatsapp → إمكان وصول أمر آخر إلى نفس سلسلة الإرسال وفق جدولة موردة صراحة ∣ printwhatsapp بعد items>0 وقراءة الطرف → أسماء هدف ومسار ورسالة مرتبطة بطلب محلي، لا نسخة bytes أو SaveResult مثبتة | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3141;SmartAuditERP/Form_WPF/frmInvSale.xaml:1187-1191;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3132-3187 |
| RQ7B34-02 | معنى إعادة استخدام Session.waSender | يعاد استخدام الحقل static إذا أعادت IsSessionValid true من قراءة WindowHandles ∣ ينفذ Navigate(targetA) ثم Delay10000 ؛ الفحص اللاحق يبحث عن editable عام لا targetA | EnsureWhatsAppSessionAsync مع مرسل موجود → إعادة استخدام كائن المرسل لا إثبات حساب WhatsApp أو ارتباط ERP/recipient ∣ SendInvoiceAsync على sender-S صالح مورّد → يمكن لفحص A أن يرى المحادثة الحالية B في تداخل موجب مورّد | SmartAuditERP/Class/Session.cs:9-21;SmartAuditERP/Class/WhatsAppSender.cs:230-245;SmartAuditERP/Class/WhatsAppSender.cs:107-144 |
| RQ7B34-03 | عنصر caption الملتقط ليس selector قابلاً لإعادة التوجيه | يلتقط IWebElement ثم Click/SendKeys(message) قبل Delay500 ، ويستخدم المرجع نفسه لـ Enter بعدها ∣ تستعمل this.driver.FindElement مع XPath عام، ثم تنقر عبر JavaScript وتنتظر مجدداً | بعد إيجاد chat وقبل Enter المتأخر → قد يبقى مرتبطاً بسياقه أو يفشل كعنصر stale وفق عقد خارجي ∣ حلقة إيجاد زر الإرفاق بعد caption → سياق selector الحالي مستقل عن قيمة customerPhone المحلية | SmartAuditERP/Class/WhatsAppSender.cs:145-155;SmartAuditERP/Class/WhatsAppSender.cs:219-228;SmartAuditERP/Class/WhatsAppSender.cs:156-189 |
| RQ7B34-04 | ملكية مسار PDF المتولد برقم الفاتورة | يبنى المسار من StartupPath و INV+txtNo ثم يحذف الموجود ويصدر إليه، دون request token في الاسم ∣ يفحص وجود الملف ثم يمرر string إلى file input عام، ولا يثبت hash محتوى عند حد المتصفح | تحضير printwhatsapp قبل Ensure await → طلبان بالاسم نفسه يشتركان في مفتاح ملف قابل للاستبدال ∣ بعد Delay2000 وقبل SendKeys(filePath) → طلب handoff لمسار؛ هوية bytes/قبول الرفع unresolved | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3166-3187;SmartAuditERP/Class/WhatsAppSender.cs:181-189 |
| RQ7B34-05 | زر send و true بعد click+delay | يبحث عن send icon عاماً وينقر ثم Delay3000 ويرجع true ، دون receipt أو provider message id ∣ يتقدم طلب النص على فشل الملف أو الإرفاق؛ catch يعرض رسالة ويرجع false | SendInvoiceAsync بعد انتظار file input → نتيجة محلية لطلب النقر لا تأكيد تسليم لمستلم ∣ caption → attach → File.Exists → file input → false قد يلي caption-request بدلاً من إلغاء كل ما سبق | SmartAuditERP/Class/WhatsAppSender.cs:190-228;SmartAuditERP/Class/WhatsAppSender.cs:145-228 |
| RQ7B34-06 | مسؤولية caller عن bool و Task المحاولة | لا يسند bool الناتج إلى حالة محاولة أو result caller ؛ المدخل الخارجي لا ينتظر Task الداخلية ∣ ينشأ WhatsAppSender ثم ينتظر Initialize ؛ كلا المسارين يعرض خطأ دون نتيجة typed تثبت التهيئة | printwhatsapp ينتظر sender ثم يعود async void → غياب نتيجة مركبة عند الحد المختار، مع بقاء رسائل الخطأ الداخلية ∣ Ensure مع sender null أو handles غير مقروءة → قد يعود Task إلى caller دون برهان login/account/ready | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3128;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3185-3199;SmartAuditERP/Class/Session.cs:9-30;SmartAuditERP/Class/WhatsAppSender.cs:66-105 |
| RQ7B34-07 | الرقم والحارس لا يعادان اكتشافهما كجذر جديد | يبقى تحويل 966 في P6-032 ؛ حارس count ليس SaveResult ولا يراجع dirty نصياً هنا ∣ يعيد helper تصدير PDF قبل Attachment ويستدعي SMTP Send متزامناً في المقطع المختار | mobile غير فارغة و items>0 ثم sender normalize → تحويل نص وشرط دخول مصدريان فقط؛ سياسة مشاركة draft unresolved ∣ BtnSendEmail_Click → Print.SendInvoiceToEmail → إعادة توليد قبل الإرفاق ليست تلقائياً ملف وردية قديم ضمني | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3128-3165;SmartAuditERP/Class/WhatsAppSender.cs:107-118;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2986-3033;SmartAuditERP/Class/Print.cs:1193-1229 |
| RQ7B34-08 | حفظ السجل ومنع إعادة عد آلية سابقة | ذكر P6-031/033 التداخل واسم الملف واقترح queue/immutable سابقاً؛ الجديد تفصيل شروط لا سبب جديد ∣ كل upstream input بادئة و rowSHA/contracts/routes/dispositions محفوظ؛ الأدوات التاريخية 123 تختلف عن 127 الحالية | dedup335metadata/33pathrows/20bodies ثم إقرار النطاق → صفر جذور وصفر ذيول للسجل؛ 335 قاموساً و raw336 كاملة مطابقة ∣ SP01–03 و RS14 و H/Q6 و RW/BK10 من B33 → 7B/7 جزئيتان؛ 7C لم تبدأ و 8 غير مأذونة؛ repair start/sync unknown | none-documentary-metadata |

## 3. دفتر حدود الانتظار AW8

| المعرف | الحد | الملاحظة | FE/الجذورالقائمة | الدليل |
|---|---|---|---|---|
| AW7B34-01 | التنقل قبل await ثم selector محادثة عام | ينفذ Navigate(targetA) ثم Delay10000 ؛ الفحص اللاحق يبحث عن editable عام لا targetA | FE7B34-04 / P6-031;P6-033 | SmartAuditERP/Class/WhatsAppSender.cs:107-144 |
| AW7B34-02 | عنصر caption الملتقط ليس selector قابلاً لإعادة التوجيه | يلتقط IWebElement ثم Click/SendKeys(message) قبل Delay500 ، ويستخدم المرجع نفسه لـ Enter بعدها | FE7B34-05 / P6-033 | SmartAuditERP/Class/WhatsAppSender.cs:145-155;SmartAuditERP/Class/WhatsAppSender.cs:219-228 |
| AW7B34-03 | زر الإرفاق يقرأ current driver بعد انتظار caption | تستعمل this.driver.FindElement مع XPath عام، ثم تنقر عبر JavaScript وتنتظر مجدداً | FE7B34-06 / P6-033 | SmartAuditERP/Class/WhatsAppSender.cs:156-189 |
| AW7B34-04 | ملكية مسار PDF المتولد برقم الفاتورة | يبنى المسار من StartupPath و INV+txtNo ثم يحذف الموجود ويصدر إليه، دون request token في الاسم ∣ يفحص وجود الملف ثم يمرر string إلى file input عام، ولا يثبت hash محتوى عند حد المتصفح | FE7B34-07;FE7B34-08 / P6-033 | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3166-3187;SmartAuditERP/Class/WhatsAppSender.cs:181-189 |
| AW7B34-05 | زر send و true بعد click+delay | يبحث عن send icon عاماً وينقر ثم Delay3000 ويرجع true ، دون receipt أو provider message id | FE7B34-09 / P6-033 | SmartAuditERP/Class/WhatsAppSender.cs:190-228 |
| AW7B34-06 | النص قبل فحص الملف وحدود الفشل الجزئي | يتقدم طلب النص على فشل الملف أو الإرفاق؛ catch يعرض رسالة ويرجع false ∣ لا يسند bool الناتج إلى حالة محاولة أو result caller ؛ المدخل الخارجي لا ينتظر Task الداخلية | FE7B34-10;FE7B34-11 / P6-033 | SmartAuditERP/Class/WhatsAppSender.cs:145-228;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3128;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3185-3199 |
| AW7B34-07 | تهيئة الجلسة ليست مصادقة مثبتة | ينشأ WhatsAppSender ثم ينتظر Initialize ؛ كلا المسارين يعرض خطأ دون نتيجة typed تثبت التهيئة | FE7B34-12 / P6-031;P6-033 | SmartAuditERP/Class/Session.cs:9-30;SmartAuditERP/Class/WhatsAppSender.cs:66-105 |
| AW7B34-08 | حفظ السجل ومنع إعادة عد آلية سابقة | ذكر P6-031/033 التداخل واسم الملف واقترح queue/immutable سابقاً؛ الجديد تفصيل شروط لا سبب جديد ∣ كل upstream input بادئة و rowSHA/contracts/routes/dispositions محفوظ؛ الأدوات التاريخية 123 تختلف عن 127 الحالية | FE7B34-15;FE7B34-16 / H7B34-06 | none-documentary-metadata |

كلصفأعلاهيحفظفي CSV المالكوالمدخلالمنقحوأثرغيابهوالخطوةوالحدو not-executed ؛ لا يختزلحسندفترالتتبعبقيةعقدالمنتجأوالمزود.

## 4. ست عشرة قدرة وثوابت وخطط قبول غير منفذة

### FE7B34-01 — ملكية الأمر المتداخل عند مدخل واتساب

- **المدخلوالمصدر:** قائمة SendWhatsapp → SendWhatsapp_Click → printwhatsapp يفوض async void الخارجي إلى async void داخلي؛ يوجد await لاحق دون handle Task عند المدخل
- **التتبّع:** يفوض async void الخارجي إلى async void داخلي؛ يوجد await لاحق دون handle Task عند المدخل → إمكان وصول أمر آخر إلى نفس سلسلة الإرسال وفق جدولة موردة صراحة
- **المخرجومايستبعده:** إمكان وصول أمر آخر إلى نفس سلسلة الإرسال وفق جدولة موردة صراحة **الاستبعاد:** لا إثبات إتاحة فعلية أو نقرات WPF أو حاجز غائب في كل التطبيق.
- **الدليل:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3141;SmartAuditERP/Form_WPF/frmInvSale.xaml:1187-1191`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-01 — الثابتالمطلوبلاالمجتاز:** يملك كل أمر مشاركة محاولة مستقلة قابلة للرصد ولا تتداخل آثارها على جلسة واحدة.
- **المالك:** مالك WPF وتسلسل طلبات واتساب؛ **المدخلالمنقحالمطلوب:** عقد request/session ownership و single-flight/queue وسياسة الإلغاء والتزامن؛ هدفان رمزيان وسجل مراحل منقح ونقاط تعليق اصطناعية بلا متصفح أو رسائل.
- **أثرغيابه:** يمكن للمصدر مواصلة طلب A على سياق محادثة طلب B إذا ورد تداخل جاهز؛ النتيجة الفعلية قد تكون فشلاً أو توقفاً أو طلباً خاطئ السياق.؛ **الخطوة/الخروجالساكن:** تعريف طلب immutable وتسلسل لكل جلسة مع تحقق target/generation قبل كل أثر، وفصل ملكية عنصر ملتقط عن selector لاحق. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا إثبات إتاحة فعلية أو نقرات WPF أو حاجز غائب في كل التطبيق.

**P7B34T-01 — طلبان متداخلان ومتلقيان مختلفان — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:علّق A بعد التنقل وقبل استئناف chat ، ثم اطلب B باستخدام المرسل الرمزي نفسه، وراقب ترتيب admission ومراحل الطلبين. القبولالمستقل:لا ينفذ B تغيير target داخل المرسل المملوك لـ A ؛ تسجل المحاولتان وحدود الانتظار والنتيجة دون خلط سياق. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-02 — طلبان مقصودان للمستلم نفسه — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد معرفَي محاولة مختلفين للهدف نفسه، ثم راقب السياسة المعتمدة للتسلسل أو الرفض دون افتراض أن كل نقرة تكرار غير مقصود. القبولالمستقل:تطبق سياسة المنتج المعلنة بمعرفي محاولة واضحين؛ لا تضيع محاولة مقصودة ولا يستدل من الهدف نفسه على تسليم أو idempotency. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-02 — لقطة الطلب وشروط التحضير قبل الانتظار

- **المدخلوالمصدر:** printwhatsapp بعد items>0 وقراءة الطرف يلتقط inv و mobile و pdfPath و message محلياً قبل await ؛ Mapping/BindToData/Export عقود رجوع خارج هذا النموذج
- **التتبّع:** يلتقط inv و mobile و pdfPath و message محلياً قبل await ؛ Mapping/BindToData/Export عقود رجوع خارج هذا النموذج → أسماء هدف ومسار ورسالة مرتبطة بطلب محلي، لا نسخة bytes أو SaveResult مثبتة
- **المخرجومايستبعده:** أسماء هدف ومسار ورسالة مرتبطة بطلب محلي، لا نسخة bytes أو SaveResult مثبتة **الاستبعاد:** غياب تعيين dirty صريح أو تعريف DTO لا يثبت غياب حماية أو أن كل مسودة ترسل.
- **الدليل:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3132-3187`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-02 — الثابتالمطلوبلاالمجتاز:** تثبت لقطة مستند ومستلم ومرفق خاصة بالطلب مع شروط رجوع موثقة قبل إتاحتها للإرسال.
- **المالك:** مالك SDK/DTO والتقارير وعقد المتصفح؛ **المدخلالمنقحالمطلوب:** هوية مصدر منقح وبصمة لعقود MappingInvoice/BindToData والقالب وقراءة file input وحياة IWebElement/DOM ؛ سياسة waits/errors دون DLL أو جلسة أو رمز QR.
- **أثرغيابه:** تبقى هوية bytes التي قرأها المتصفح ونجاح PDF والتحميل والربط والتهيئة غير معلومة، ولا يستبدلها نموذج الرموز.؛ **الخطوة/الخروجالساكن:** حفظ unknown صراحة وإسناد كل عقد خارجي إلى مصدر منقح ونسخة أو handoff ، دون استنتاج غياب قدرة. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. غياب تعيين dirty صريح أو تعريف DTO لا يثبت غياب حماية أو أن كل مسودة ترسل.

**P7B34T-03 — تغير المحرر بعد التحضير — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:حضّر A بقيم رمزية معلنة ثم غيّر الحالة المعروضة أثناء انتظار اصطناعي، وراقب DocumentRef/target/version الخاصة بـ A. القبولالمستقل:يبقى كل أثر تابعاً للقطة A المعتمدة؛ لا تقرأ متابعة متأخرة هوية جديدة من واجهة متغيرة دون إعادة تفويض. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-04 — عدم رجوع mapping أو export — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد فشلاً قبل نهاية التحضير في كل حد على حدة، وراقب ألا تنشأ محاولة sender أو نتيجة Delivered. القبولالمستقل:لا يدخل المرسل قبل نجاح التحضير المتفق عليه؛ تفصل حالات mapping/export عن timeout/فشل مزود ولا يسجل حفظ أو تحميل فعلي مدعى. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-03 — معنى إعادة استخدام Session.waSender

- **المدخلوالمصدر:** EnsureWhatsAppSessionAsync مع مرسل موجود يعاد استخدام الحقل static إذا أعادت IsSessionValid true من قراءة WindowHandles
- **التتبّع:** يعاد استخدام الحقل static إذا أعادت IsSessionValid true من قراءة WindowHandles → إعادة استخدام كائن المرسل لا إثبات حساب WhatsApp أو ارتباط ERP/recipient
- **المخرجومايستبعده:** إعادة استخدام كائن المرسل لا إثبات حساب WhatsApp أو ارتباط ERP/recipient **الاستبعاد:** إعادة عد P6-031 أو افتراض أن handles readable تعني logged-in ممنوعان.
- **الدليل:** `SmartAuditERP/Class/Session.cs:9-21;SmartAuditERP/Class/WhatsAppSender.cs:230-245`؛ الجذور/الإحالة:P6-031 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-03 — الثابتالمطلوبلاالمجتاز:** تتحقق أهلية الجلسة من هوية حساب وسياق مفوضين، لا قابلية قراءة WindowHandles وحدها.
- **المالك:** مالك WPF وتسلسل طلبات واتساب؛ **المدخلالمنقحالمطلوب:** عقد request/session ownership و single-flight/queue وسياسة الإلغاء والتزامن؛ هدفان رمزيان وسجل مراحل منقح ونقاط تعليق اصطناعية بلا متصفح أو رسائل.
- **أثرغيابه:** يمكن للمصدر مواصلة طلب A على سياق محادثة طلب B إذا ورد تداخل جاهز؛ النتيجة الفعلية قد تكون فشلاً أو توقفاً أو طلباً خاطئ السياق.؛ **الخطوة/الخروجالساكن:** تعريف طلب immutable وتسلسل لكل جلسة مع تحقق target/generation قبل كل أثر، وفصل ملكية عنصر ملتقط عن selector لاحق. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. إعادة عد P6-031 أو افتراض أن handles readable تعني logged-in ممنوعان.

**P7B34T-05 — handles مقروءة وحساب غير مطابق — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد handles readable مع account token لا يطابق سياق الطلب، ثم راقب قرار بوابة الإرسال دون جلسة حقيقية. القبولالمستقل:لا يمنح فحص handles وحده إذن إرسال؛ يسجل account mismatch أو unresolved دون أي طلب رسالة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-06 — الجلسة نفسها وطلبان مختلفان — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:استخدم sender token واحداً صالحاً بين طلبين رمزيين بهويتين مستقلتين وراقب ملكية المرسل عبر الانتظار. القبولالمستقل:تبقى ملكية الجلسة وتسلسلها صريحين لكل محاولة؛ لا ينسخ bool الصلاحية إلى إثبات target أو تسليم. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-04 — التنقل قبل await ثم selector محادثة عام

- **المدخلوالمصدر:** SendInvoiceAsync على sender-S صالح مورّد ينفذ Navigate(targetA) ثم Delay10000 ؛ الفحص اللاحق يبحث عن editable عام لا targetA
- **التتبّع:** ينفذ Navigate(targetA) ثم Delay10000 ؛ الفحص اللاحق يبحث عن editable عام لا targetA → يمكن لفحص A أن يرى المحادثة الحالية B في تداخل موجب مورّد
- **المخرجومايستبعده:** يمكن لفحص A أن يرى المحادثة الحالية B في تداخل موجب مورّد **الاستبعاد:** لا وقت تنفيذ أو وصول شبكة أو صلاحية رقم أو DOM WhatsApp حقيقي ثبت.
- **الدليل:** `SmartAuditERP/Class/WhatsAppSender.cs:107-144`؛ الجذور/الإحالة:P6-031;P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-04 — الثابتالمطلوبلاالمجتاز:** تظل محادثة الاستمرار مرتبطة بهدف الطلب أو يرفض الاستمرار قبل أي أثر إذا تبدل الهدف.
- **المالك:** مالك WPF وتسلسل طلبات واتساب؛ **المدخلالمنقحالمطلوب:** عقد request/session ownership و single-flight/queue وسياسة الإلغاء والتزامن؛ هدفان رمزيان وسجل مراحل منقح ونقاط تعليق اصطناعية بلا متصفح أو رسائل.
- **أثرغيابه:** يمكن للمصدر مواصلة طلب A على سياق محادثة طلب B إذا ورد تداخل جاهز؛ النتيجة الفعلية قد تكون فشلاً أو توقفاً أو طلباً خاطئ السياق.؛ **الخطوة/الخروجالساكن:** تعريف طلب immutable وتسلسل لكل جلسة مع تحقق target/generation قبل كل أثر، وفصل ملكية عنصر ملتقط عن selector لاحق. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا وقت تنفيذ أو وصول شبكة أو صلاحية رقم أو DOM WhatsApp حقيقي ثبت.

**P7B34T-07 — A navigate ثم B navigate ثم A chat — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ثبت ترتيباً اصطناعياً A.Navigate/B.Navigate/A.resume مع editable جاهز في target-B ، وسجل identity لكل مرحلة. القبولالمستقل:لا يقبل A selector عاماً كإثبات لهدفه؛ يؤجل أو يرفض أثره حتى target-A ضمن ملكية مصرح بها. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-08 — تسلسل A كاملاً ثم B كاملاً — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:أكمل A قبل بدء تغيير هدف B مع readiness موجبة موردة، ثم قارن سياق كل طلب بهدفه. القبولالمستقل:ينتج مراقب المراحل تطابق request/target دون اختلاط؛ هذه المقارنة لا تتحول إلى إثبات تسليم أو نجاح مزود. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-05 — عنصر caption الملتقط ليس selector قابلاً لإعادة التوجيه

- **المدخلوالمصدر:** بعد إيجاد chat وقبل Enter المتأخر يلتقط IWebElement ثم Click/SendKeys(message) قبل Delay500 ، ويستخدم المرجع نفسه لـ Enter بعدها
- **التتبّع:** يلتقط IWebElement ثم Click/SendKeys(message) قبل Delay500 ، ويستخدم المرجع نفسه لـ Enter بعدها → قد يبقى مرتبطاً بسياقه أو يفشل كعنصر stale وفق عقد خارجي
- **المخرجومايستبعده:** قد يبقى مرتبطاً بسياقه أو يفشل كعنصر stale وفق عقد خارجي **الاستبعاد:** لا نفترض أن كل عنصر قديم ينتقل تلقائياً إلى المحادثة الجديدة أو ينجح.
- **الدليل:** `SmartAuditERP/Class/WhatsAppSender.cs:145-155;SmartAuditERP/Class/WhatsAppSender.cs:219-228`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-05 — الثابتالمطلوبلاالمجتاز:** تثبت ملكية عنصر caption عند الالتقاط، ويعالج stale/تبدل السياق دون متابعة نجاح أو إعادة عمياء.
- **المالك:** مالك SDK/DTO والتقارير وعقد المتصفح؛ **المدخلالمنقحالمطلوب:** هوية مصدر منقح وبصمة لعقود MappingInvoice/BindToData والقالب وقراءة file input وحياة IWebElement/DOM ؛ سياسة waits/errors دون DLL أو جلسة أو رمز QR.
- **أثرغيابه:** تبقى هوية bytes التي قرأها المتصفح ونجاح PDF والتحميل والربط والتهيئة غير معلومة، ولا يستبدلها نموذج الرموز.؛ **الخطوة/الخروجالساكن:** حفظ unknown صراحة وإسناد كل عقد خارجي إلى مصدر منقح ونسخة أو handoff ، دون استنتاج غياب قدرة. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا نفترض أن كل عنصر قديم ينتقل تلقائياً إلى المحادثة الجديدة أو ينجح.

**P7B34T-09 — التبديل قبل التقاط عنصر caption — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:بدل الهدف إلى B قبل استئناف A وإيجاد العنصر، مع ready موجبة، وراقب context حين التقاطه وحين طلب Enter. القبولالمستقل:يرفض طلب A الأثر على عنصر من target-B ولا يعد العثور على selector عاماً تحققاً من المستلم. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-10 — التبديل بعد التقاط العنصر — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:التقط عنصر A ثم ورد invalid/stale عند Enter بعد التعليق، وراقب false/unknown والسجل الجزئي. القبولالمستقل:لا يعاد توجيه المرجع القديم ضمنياً إلى B في النموذج أو تقرير النتيجة؛ لا نجاح كاذب ولا إخفاء احتمال caption جزئي. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-06 — زر الإرفاق يقرأ current driver بعد انتظار caption

- **المدخلوالمصدر:** حلقة إيجاد زر الإرفاق بعد caption تستعمل this.driver.FindElement مع XPath عام، ثم تنقر عبر JavaScript وتنتظر مجدداً
- **التتبّع:** تستعمل this.driver.FindElement مع XPath عام، ثم تنقر عبر JavaScript وتنتظر مجدداً → سياق selector الحالي مستقل عن قيمة customerPhone المحلية
- **المخرجومايستبعده:** سياق selector الحالي مستقل عن قيمة customerPhone المحلية **الاستبعاد:** لا تثبت JavaScript أو المحددات القديمة صلاحية DOM المنشور أو نجاح نقرة فعلية.
- **الدليل:** `SmartAuditERP/Class/WhatsAppSender.cs:156-189`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-06 — الثابتالمطلوبلاالمجتاز:** يتحقق طلب الإرفاق من request/session/target قبل اختيار زر عام أو طلب أثر مرئي.
- **المالك:** مالك WPF وتسلسل طلبات واتساب؛ **المدخلالمنقحالمطلوب:** عقد request/session ownership و single-flight/queue وسياسة الإلغاء والتزامن؛ هدفان رمزيان وسجل مراحل منقح ونقاط تعليق اصطناعية بلا متصفح أو رسائل.
- **أثرغيابه:** يمكن للمصدر مواصلة طلب A على سياق محادثة طلب B إذا ورد تداخل جاهز؛ النتيجة الفعلية قد تكون فشلاً أو توقفاً أو طلباً خاطئ السياق.؛ **الخطوة/الخروجالساكن:** تعريف طلب immutable وتسلسل لكل جلسة مع تحقق target/generation قبل كل أثر، وفصل ملكية عنصر ملتقط عن selector لاحق. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا تثبت JavaScript أو المحددات القديمة صلاحية DOM المنشور أو نجاح نقرة فعلية.

**P7B34T-11 — تبدل chat قبل زر الإرفاق — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:أبق A معلقاً بعد caption ثم ورد target-B عند lookup زر الإرفاق، بوجود زر رمزي جاهز. القبولالمستقل:لا يستعمل A زر إرفاق من سياق B ؛ يرصد المراقب mismatch قبل أثر JavaScript أو نقل المسار. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-12 — عدم العثور على زر الإرفاق — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد انتهاء مهلة الزر بعد caption-request وسجل كل مرحلة دون إعادة أو إرسال فعلي. القبولالمستقل:تعاد حالة جزئية/unknown محددة، لا Delivered ولا ضمان أن النص لم يطلب؛ قرار الإعادة مفوض وفق السياسة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-07 — ملكية مسار PDF المتولد برقم الفاتورة

- **المدخلوالمصدر:** تحضير printwhatsapp قبل Ensure await يبنى المسار من StartupPath و INV+txtNo ثم يحذف الموجود ويصدر إليه، دون request token في الاسم
- **التتبّع:** يبنى المسار من StartupPath و INV+txtNo ثم يحذف الموجود ويصدر إليه، دون request token في الاسم → طلبان بالاسم نفسه يشتركان في مفتاح ملف قابل للاستبدال
- **المخرجومايستبعده:** طلبان بالاسم نفسه يشتركان في مفتاح ملف قابل للاستبدال **الاستبعاد:** لا نقرأ ملف فاتورة أو نثبت bytes استهلكها Selenium ؛ الآلية مذكورة أصلاً في P6-033.
- **الدليل:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3166-3187`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-07 — الثابتالمطلوبلاالمجتاز:** يملك كل طلب مرفقاً immutable بهوية وبصمة، لا مساراً مشتركاً يعاد توليده قبل الاستهلاك.
- **المالك:** مالك المراسلة والتشغيل ونتيجة المحاولة؛ **المدخلالمنقحالمطلوب:** عقد partial/unknown و correlation ومحاولة الإعادة وإثبات قبول المزود/التسليم منفصلين؛ مرفق immutable ببصمة وملكية و retention دون ملف حقيقي أو حساب.
- **أثرغيابه:** قد يسبق طلب النص فشل المرفق؛ true و delay/click ليست Delivered ، ولا يسمح false بإعادة تلقائية عمياء لجزء مجهول النتيجة.؛ **الخطوة/الخروجالساكن:** وصف مراحل Requested/CaptionSubmitted/FileHandedOff/Unknown/Failed بعقد مراقب مأذون لاحقاً وإعادة واعية للجزئية. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا نقرأ ملف فاتورة أو نثبت bytes استهلكها Selenium ؛ الآلية مذكورة أصلاً في P6-033.

**P7B34T-13 — رقم واحد ونسختان رمزيتان — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:حضّر A(version-A) وعلقه، ثم حضّر B(version-B) بالمفتاح نفسه، وراقب المرجع الذي يسلم لكل محاولة. القبولالمستقل:يحافظ A على مرفقه المعتمد أو يمنع الاستبدال قبل handoff ؛ لا يكفي File.Exists لإثبات version-A. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-14 — مفاتيح مختلفة وسياق chat مشترك — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:استخدم path-A/path-B مختلفين مع تداخل التنقل على sender واحد، ثم قارن هوية الملف وسياق المحادثة منفصلين. القبولالمستقل:لا يعد اختلاف اسمي الملفين إصلاحاً لملكية chat ؛ يجب أن يطابق كل من مرفق الطلب وهدفه هويته الخاصة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-08 — File.Exists والمسار لا يثبتان بايتات الرفع

- **المدخلوالمصدر:** بعد Delay2000 وقبل SendKeys(filePath) يفحص وجود الملف ثم يمرر string إلى file input عام، ولا يثبت hash محتوى عند حد المتصفح
- **التتبّع:** يفحص وجود الملف ثم يمرر string إلى file input عام، ولا يثبت hash محتوى عند حد المتصفح → طلب handoff لمسار؛ هوية bytes/قبول الرفع unresolved
- **المخرجومايستبعده:** طلب handoff لمسار؛ هوية bytes/قبول الرفع unresolved **الاستبعاد:** لا قراءة ملف أو رفع أو PDF فعلي، ولا تعميم أن وجود الاسم يضمن نسخة بعينها.
- **الدليل:** `SmartAuditERP/Class/WhatsAppSender.cs:181-189`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-08 — الثابتالمطلوبلاالمجتاز:** يربط handoff المرفق بهوية محتوى مثبتة عند الاستهلاك وبهدف طلبه دون استنتاجها من وجود المسار.
- **المالك:** مالك SDK/DTO والتقارير وعقد المتصفح؛ **المدخلالمنقحالمطلوب:** هوية مصدر منقح وبصمة لعقود MappingInvoice/BindToData والقالب وقراءة file input وحياة IWebElement/DOM ؛ سياسة waits/errors دون DLL أو جلسة أو رمز QR.
- **أثرغيابه:** تبقى هوية bytes التي قرأها المتصفح ونجاح PDF والتحميل والربط والتهيئة غير معلومة، ولا يستبدلها نموذج الرموز.؛ **الخطوة/الخروجالساكن:** حفظ unknown صراحة وإسناد كل عقد خارجي إلى مصدر منقح ونسخة أو handoff ، دون استنتاج غياب قدرة. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا قراءة ملف أو رفع أو PDF فعلي، ولا تعميم أن وجود الاسم يضمن نسخة بعينها.

**P7B34T-15 — الملف مفقود بعد طلب النص — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد file absent عند الحد المتأخر بعد caption-request ، وراقب false وحدود الجزئية دون أي متصفح. القبولالمستقل:لا يحدث file handoff أو Delivered ؛ لا تصنف المحاولة كأنها لم تبدأ آثاراً محلية أو تطلب إعادة تلقائية للكل. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-16 — الاسم موجود ومحتواه الرمزي تبدل — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:أبق مفتاح الملف موجوداً ثم بدّل version token قبل handoff ، وراقب الإثبات المطلوب للنسخة دون استهلاك bytes. القبولالمستقل:يرفض عقد الملكية قبول Exists بديلاً للبصمة/النسخة، وتبقى نتيجة الرفع unknown حتى دليل مستقل مأذون. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-09 — زر send و true بعد click+delay

- **المدخلوالمصدر:** SendInvoiceAsync بعد انتظار file input يبحث عن send icon عاماً وينقر ثم Delay3000 ويرجع true ، دون receipt أو provider message id
- **التتبّع:** يبحث عن send icon عاماً وينقر ثم Delay3000 ويرجع true ، دون receipt أو provider message id → نتيجة محلية لطلب النقر لا تأكيد تسليم لمستلم
- **المخرجومايستبعده:** نتيجة محلية لطلب النقر لا تأكيد تسليم لمستلم **الاستبعاد:** لا يفهم true على أنه Accepted/Delivered ؛ هذا الأصل P6-033 لا P7 جديدة.
- **الدليل:** `SmartAuditERP/Class/WhatsAppSender.cs:190-228`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-09 — الثابتالمطلوبلاالمجتاز:** تفرق نتيجة المحاولة بين طلب إجراء محلي وقبول المزود والتسليم، مع correlation قابل للتتبع.
- **المالك:** مالك المراسلة والتشغيل ونتيجة المحاولة؛ **المدخلالمنقحالمطلوب:** عقد partial/unknown و correlation ومحاولة الإعادة وإثبات قبول المزود/التسليم منفصلين؛ مرفق immutable ببصمة وملكية و retention دون ملف حقيقي أو حساب.
- **أثرغيابه:** قد يسبق طلب النص فشل المرفق؛ true و delay/click ليست Delivered ، ولا يسمح false بإعادة تلقائية عمياء لجزء مجهول النتيجة.؛ **الخطوة/الخروجالساكن:** وصف مراحل Requested/CaptionSubmitted/FileHandedOff/Unknown/Failed بعقد مراقب مأذون لاحقاً وإعادة واعية للجزئية. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا يفهم true على أنه Accepted/Delivered ؛ هذا الأصل P6-033 لا P7 جديدة.

**P7B34T-17 — زر send جاهز و receipt غائبة — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد click-returned ثم delay-returned مع عدم وجود provider receipt ، وسجل نتيجة طبقية اصطناعية. القبولالمستقل:لا تسجل Delivered أو تزعم وصول فاتورة؛ تعرف الحالة بأنها أثر محلي/unknown وفق عقد القناة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-18 — غياب زر send بعد file handoff — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد file-input handoff ثم send-button absent ، وارصد الحالة الجزئية والتصرف قبل إعادة المحاولة. القبولالمستقل:تحفظ حدود ما طلب وما بقي unknown ؛ لا يعد false إثبات رفض مزود أو أن الملف لم يرفع مطلقاً. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-10 — النص قبل فحص الملف وحدود الفشل الجزئي

- **المدخلوالمصدر:** caption → attach → File.Exists → file input يتقدم طلب النص على فشل الملف أو الإرفاق؛ catch يعرض رسالة ويرجع false
- **التتبّع:** يتقدم طلب النص على فشل الملف أو الإرفاق؛ catch يعرض رسالة ويرجع false → false قد يلي caption-request بدلاً من إلغاء كل ما سبق
- **المخرجومايستبعده:** false قد يلي caption-request بدلاً من إلغاء كل ما سبق **الاستبعاد:** لا إثبات أن نصاً وصل؛ ولا ادعاء أن catch صامت أو أن كل خطأ قابل لإعادة آمنة.
- **الدليل:** `SmartAuditERP/Class/WhatsAppSender.cs:145-228`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-10 — الثابتالمطلوبلاالمجتاز:** تحفظ النتيجة الجزئية ما طلب قبل الفشل ولا تحول false إلى ضمان rollback لمزود خارجي.
- **المالك:** مالك المراسلة والتشغيل ونتيجة المحاولة؛ **المدخلالمنقحالمطلوب:** عقد partial/unknown و correlation ومحاولة الإعادة وإثبات قبول المزود/التسليم منفصلين؛ مرفق immutable ببصمة وملكية و retention دون ملف حقيقي أو حساب.
- **أثرغيابه:** قد يسبق طلب النص فشل المرفق؛ true و delay/click ليست Delivered ، ولا يسمح false بإعادة تلقائية عمياء لجزء مجهول النتيجة.؛ **الخطوة/الخروجالساكن:** وصف مراحل Requested/CaptionSubmitted/FileHandedOff/Unknown/Failed بعقد مراقب مأذون لاحقاً وإعادة واعية للجزئية. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا إثبات أن نصاً وصل؛ ولا ادعاء أن catch صامت أو أن كل خطأ قابل لإعادة آمنة.

**P7B34T-19 — caption ثم attach غير جاهز — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:أثبت في سجل المراقب طلب caption أولاً ثم ورد فشل attach ، واطلب قرار إعادة وفق سياسة معتمدة. القبولالمستقل:لا يعيد النظام كل الأجزاء عميانياً؛ تعرض مرحلة الفشل وما بقي مجهولاً دون ادعاء وصول النص. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-20 — رسالة فارغة ومرفق مفقود — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد caption فارغة ثم file absent على حد لاحق، وقارن سجل العمليات بالمحاولة ذات النص. القبولالمستقل:لا تسجل خطوة نص لم تقع في هذا الفرع؛ يبقى فشل الملف مميزاً ولا يعمم وصف جزئية النص على كل محاولة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-11 — مسؤولية caller عن bool و Task المحاولة

- **المدخلوالمصدر:** printwhatsapp ينتظر sender ثم يعود async void لا يسند bool الناتج إلى حالة محاولة أو result caller ؛ المدخل الخارجي لا ينتظر Task الداخلية
- **التتبّع:** لا يسند bool الناتج إلى حالة محاولة أو result caller ؛ المدخل الخارجي لا ينتظر Task الداخلية → غياب نتيجة مركبة عند الحد المختار، مع بقاء رسائل الخطأ الداخلية
- **المخرجومايستبعده:** غياب نتيجة مركبة عند الحد المختار، مع بقاء رسائل الخطأ الداخلية **الاستبعاد:** لا ننفي كل تنبيه أو سجل خارجي ولا نثبت أن المشغل أعاد إرسالاً فعلياً.
- **الدليل:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3128;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3185-3199`؛ الجذور/الإحالة:P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-11 — الثابتالمطلوبلاالمجتاز:** يعرض caller نتيجة typed ومحاولة قابلة للإلغاء/الانتظار ولا يسقط bool/الجزئية عند حدود void.
- **المالك:** مالك WPF وتسلسل طلبات واتساب؛ **المدخلالمنقحالمطلوب:** عقد request/session ownership و single-flight/queue وسياسة الإلغاء والتزامن؛ هدفان رمزيان وسجل مراحل منقح ونقاط تعليق اصطناعية بلا متصفح أو رسائل.
- **أثرغيابه:** يمكن للمصدر مواصلة طلب A على سياق محادثة طلب B إذا ورد تداخل جاهز؛ النتيجة الفعلية قد تكون فشلاً أو توقفاً أو طلباً خاطئ السياق.؛ **الخطوة/الخروجالساكن:** تعريف طلب immutable وتسلسل لكل جلسة مع تحقق target/generation قبل كل أثر، وفصل ملكية عنصر ملتقط عن selector لاحق. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا ننفي كل تنبيه أو سجل خارجي ولا نثبت أن المشغل أعاد إرسالاً فعلياً.

**P7B34T-21 — رجوع sender=false إلى caller — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد result=false رمزياً إلى continuation المكتمل ثم راقب سجل المحاولة والواجهة في قبول مأذون لاحقاً. القبولالمستقل:لا يسقط سبب الفشل أو الجزء المجهول في void ؛ ترتبط النتيجة بمعرف الطلب ولا يتقرر حفظ أو تسليم تلقائياً. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-22 — رجوع متأخر بعد طلب آخر — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:أكمل B ثم أعد نتيجة A متأخرة إلى مالك الأمر، وراقب generation/طلب العرض دون مشاركة مؤشر نجاح واحد. القبولالمستقل:لا تغير نتيجة A المتأخرة حالة B أو تعرض نجاحها نيابة عنه؛ كل نتيجة لها correlation وحدود مستقلة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-12 — تهيئة الجلسة ليست مصادقة مثبتة

- **المدخلوالمصدر:** Ensure مع sender null أو handles غير مقروءة ينشأ WhatsAppSender ثم ينتظر Initialize ؛ كلا المسارين يعرض خطأ دون نتيجة typed تثبت التهيئة
- **التتبّع:** ينشأ WhatsAppSender ثم ينتظر Initialize ؛ كلا المسارين يعرض خطأ دون نتيجة typed تثبت التهيئة → قد يعود Task إلى caller دون برهان login/account/ready
- **المخرجومايستبعده:** قد يعود Task إلى caller دون برهان login/account/ready **الاستبعاد:** لا تشغيل Chrome أو QR ولا نساوي رجوع Task بمتصفح صالح.
- **الدليل:** `SmartAuditERP/Class/Session.cs:9-30;SmartAuditERP/Class/WhatsAppSender.cs:66-105`؛ الجذور/الإحالة:P6-031;P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-12 — الثابتالمطلوبلاالمجتاز:** تسلم التهيئة نتيجة صريحة بهوية حساب مفوض وصلاحية محددة أو failure/unknown قبل استعمال المرسل.
- **المالك:** مالك SDK/DTO والتقارير وعقد المتصفح؛ **المدخلالمنقحالمطلوب:** هوية مصدر منقح وبصمة لعقود MappingInvoice/BindToData والقالب وقراءة file input وحياة IWebElement/DOM ؛ سياسة waits/errors دون DLL أو جلسة أو رمز QR.
- **أثرغيابه:** تبقى هوية bytes التي قرأها المتصفح ونجاح PDF والتحميل والربط والتهيئة غير معلومة، ولا يستبدلها نموذج الرموز.؛ **الخطوة/الخروجالساكن:** حفظ unknown صراحة وإسناد كل عقد خارجي إلى مصدر منقح ونسخة أو handoff ، دون استنتاج غياب قدرة. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا تشغيل Chrome أو QR ولا نساوي رجوع Task بمتصفح صالح.

**P7B34T-23 — فشل initialize مع رجوع Task — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد initialization error-handled مع Task returned ، ثم راقب بوابة sender دون متصفح أو حساب. القبولالمستقل:لا تمنح عودة Task وحدها إذن متابعة رسالة؛ يرصد failure/unknown بمرحلة وهوية ولا يتقرر جاهزية من catch. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-24 — مرسل صالح سابقاً مقابل null — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:قارن route مرسل موجود handles-readable بحالة null ، مع توثيق استقلال هذين المسارين عن إثبات المصادقة. القبولالمستقل:يظل reused/new قرار ملكية لا شهادة logged-in أو recipient ؛ تبقى عقود الاستبدال والإلغاء والتزامن صريحة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-13 — الرقم والحارس لا يعادان اكتشافهما كجذر جديد

- **المدخلوالمصدر:** mobile غير فارغة و items>0 ثم sender normalize يبقى تحويل 966 في P6-032 ؛ حارس count ليس SaveResult ولا يراجع dirty نصياً هنا
- **التتبّع:** يبقى تحويل 966 في P6-032 ؛ حارس count ليس SaveResult ولا يراجع dirty نصياً هنا → تحويل نص وشرط دخول مصدريان فقط؛ سياسة مشاركة draft unresolved
- **المخرجومايستبعده:** تحويل نص وشرط دخول مصدريان فقط؛ سياسة مشاركة draft unresolved **الاستبعاد:** لا رقم حقيقي ولا افتراض بلد من موقع المستخدم، ولا إثبات غياب حماية SDK.
- **الدليل:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3128-3165;SmartAuditERP/Class/WhatsAppSender.cs:107-118`؛ الجذور/الإحالة:P6-032;P6-033 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-13 — الثابتالمطلوبلاالمجتاز:** يحسم المنتج أهلية المشاركة والرقم typed وفق عقد منقح مستقل دون استنتاج الحفظ أو البلد من count/location.
- **المالك:** مالك المنتج وسياسة مشاركة المستند؛ **المدخلالمنقحالمطلوب:** سياسة إخراج saved/draft و OutputIntent المأذون، ومعنى النقرات المتعددة وطلبين مختلفين وقرار الإلغاء والموافقة؛ أمثلة رمزية بلا بيانات عمل أو أرقام هواتف.
- **أثرغيابه:** لا يثبت عد البنود أن المستند محفوظ؛ تبقى أهلية المشاركة وقصد التكرار والمستلم المصرح وسياسة الإلغاء غير محسومة.؛ **الخطوة/الخروجالساكن:** تحديد أهلية المشاركة لكل نية مستقلة قبل الإرسال، دون اعتماد الحارس النصي أو إصلاح التطبيق في هذا الفرع. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا رقم حقيقي ولا افتراض بلد من موقع المستخدم، ولا إثبات غياب حماية SDK.

**P7B34T-25 — items0 و mobile فارغة كضابطين — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد أولاً count0 ثم count1 مع mobile فارغة، وارصد عدم بلوغ session/export بحسب موضع كل بوابة. القبولالمستقل:تحفظ البوابات الفعلية وحدودها، ولا تحول رسالة قبل الحفظ إلى إثبات أن جميع saved/draft predicates فحصت. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-26 — صيغة دولية وسياسة بلد معلنة — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:استخدم هاتفاً رمزياً بعقد normalization مفوض ومثبت مسبقاً، وقارن قرار السياسة بتتبع string الأصلي دون رابط حقيقي. القبولالمستقل:تبقى P6-032 مفتوحة حتى قبول مستقل؛ لا يستنتج بلد العميل من مكان المستخدم ولا يضاف finding تكراري عن التحويل نفسه. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-14 — البريد ضابط مختلف عن متصفح واتساب

- **المدخلوالمصدر:** BtnSendEmail_Click → Print.SendInvoiceToEmail يعيد helper تصدير PDF قبل Attachment ويستدعي SMTP Send متزامناً في المقطع المختار
- **التتبّع:** يعيد helper تصدير PDF قبل Attachment ويستدعي SMTP Send متزامناً في المقطع المختار → إعادة توليد قبل الإرفاق ليست تلقائياً ملف وردية قديم ضمني
- **المخرجومايستبعده:** إعادة توليد قبل الإرفاق ليست تلقائياً ملف وردية قديم ضمني **الاستبعاد:** لا SMTP أو ملف فعلي ولا تعميم سباق await المتصفح على المسار المتزامن أو إثبات خلو كل مخاطر الاسم.
- **الدليل:** `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2986-3033;SmartAuditERP/Class/Print.cs:1193-1229`؛ الجذور/الإحالة:P6-034 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-14 — الثابتالمطلوبلاالمجتاز:** تميز عقود البريد بين إعادة توليد مرفق واختيار stale implicit ، مع سياسة ملف/نتيجة منفصلة عن واتساب.
- **المالك:** مالك المراسلة والتشغيل ونتيجة المحاولة؛ **المدخلالمنقحالمطلوب:** عقد partial/unknown و correlation ومحاولة الإعادة وإثبات قبول المزود/التسليم منفصلين؛ مرفق immutable ببصمة وملكية و retention دون ملف حقيقي أو حساب.
- **أثرغيابه:** قد يسبق طلب النص فشل المرفق؛ true و delay/click ليست Delivered ، ولا يسمح false بإعادة تلقائية عمياء لجزء مجهول النتيجة.؛ **الخطوة/الخروجالساكن:** وصف مراحل Requested/CaptionSubmitted/FileHandedOff/Unknown/Failed بعقد مراقب مأذون لاحقاً وإعادة واعية للجزئية. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا SMTP أو ملف فعلي ولا تعميم سباق await المتصفح على المسار المتزامن أو إثبات خلو كل مخاطر الاسم.

**P7B34T-27 — إعادة توليد البريد قبل الإرفاق — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد export-returned ثم attachment ثم send-returned بمراقب رمزي، وقارن ترتيبها بقبول تعمق P6-033. القبولالمستقل:لا ينسب stale implicit الخاص بـ P6-034 إلى helper الذي يجدد الملف هنا؛ يبقى receipt/retention والاسم المشترك أسئلة منفصلة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-28 — فشل تصدير البريد قبل الإرفاق — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:ورد export nonreturn قبل new Attachment وراقب ألا يستنتج التقرير إرسال ملف موجود سابقاً من هذا المسار وحده. القبولالمستقل:لا يقفز التتبع إلى attach/send بعد فشل export ؛ لا يعمم ذلك سلامة كل بريد أو إنشاء ملف حقيقي. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-15 — حفظ السجل ومنع إعادة عد آلية سابقة

- **المدخلوالمصدر:** dedup335metadata/33pathrows/20bodies ثم إقرار النطاق ذكر P6-031/033 التداخل واسم الملف واقترح queue/immutable سابقاً؛ الجديد تفصيل شروط لا سبب جديد
- **التتبّع:** ذكر P6-031/033 التداخل واسم الملف واقترح queue/immutable سابقاً؛ الجديد تفصيل شروط لا سبب جديد → صفر جذور وصفر ذيول للسجل؛ 335 قاموساً و raw336 كاملة مطابقة
- **المخرجومايستبعده:** صفر جذور وصفر ذيول للسجل؛ 335 قاموساً و raw336 كاملة مطابقة **الاستبعاد:** ليس ترشيحاً لكل المتون أو إغلاقاً لنتيجة قديمة؛ G ليست findings.
- **الدليل:** `none-documentary-metadata`؛ الجذور/الإحالة:H7B34-06 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-15 — الثابتالمطلوبلاالمجتاز:** يحفظ السجل السابق بكل بايت وحقل، ولا تحول إعادة شرح آلية مذكورة إلى رقم نتيجة جديد.
- **المالك:** مالك نطاق التدقيق والأنساب والتسليم المستقل؛ **المدخلالمنقحالمطلوب:** crosswalk455FE وبقية SP01–03 ، وحصر caller/editor/field/writer/output ؛ آخر SHA راجعه قارئ الإصلاح إن ورد، والفصل بين 123 assertion inputs و 127 أداة تنفيذ.
- **أثرغيابه:** تبقى 7B/7 جزئيتين و 7C لم تبدأ؛ لا يمكن تحويل دفاتر التوكنات إلى حصر قدرات أو افتراض بدء الإصلاح أو تزامنه.؛ **الخطوة/الخروجالساكن:** اختيار R4s/7B35 أو split مسبب بقدرة وحدود ومالك ومدخل وخطوة وخروج مع تسليم SHA تدقيق مستقل. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. ليس ترشيحاً لكل المتون أو إغلاقاً لنتيجة قديمة؛ G ليست findings.

**P7B34T-29 — محاولة إعادة عد التداخل — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:قدم للمدقق وثيقة تجعل P7-164 جديداً لنفس chat/file interleaving ثم شغل تحقق الوثائق فقط. القبولالمستقل:يرفض metadata/report/count أو registry mutation ؛ لا يحول ثراء الشاهد إلى جذر أو severity جديدة. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-30 — تبديل حقل قديم أو نهاية سطر — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:غير نسخة اصطناعية فقط من raw/row/status/next_phase ثم تحقق من مقارنة كل 335 و CRLF دون لمس الأصل. القبولالمستقل:يفشل تحقق الوثائق أمام أي اختلاف، بما فيه evidence أو newline ؛ findings.csv نفسها ضمن 1018 المحمية. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

### FE7B34-16 — حمل بقية 7B والحواجز والإصلاح المستقل

- **المدخلوالمصدر:** SP01–03 و RS14 و H/Q6 و RW/BK10 من B33 كل upstream input بادئة و rowSHA/contracts/routes/dispositions محفوظ؛ الأدوات التاريخية 123 تختلف عن 127 الحالية
- **التتبّع:** كل upstream input بادئة و rowSHA/contracts/routes/dispositions محفوظ؛ الأدوات التاريخية 123 تختلف عن 127 الحالية → 7B/7 جزئيتان؛ 7C لم تبدأ و 8 غير مأذونة؛ repair start/sync unknown
- **المخرجومايستبعده:** 7B/7 جزئيتان؛ 7C لم تبدأ و 8 غير مأذونة؛ repair start/sync unknown **الاستبعاد:** لا مدة أو جلسات أو نسبة إكمال أو إصلاح أو قبول تشغيلي أو كل 455FE من دفتر توكنات.
- **الدليل:** `none-documentary-metadata`؛ الجذور/الإحالة:H7B34-06 ؛ الحالة:bounded-source-contract-not-runtime-acceptance ؛ العمق:selected-slices-with-explicit-external-contract-limits.
- **INV7B34-16 — الثابتالمطلوبلاالمجتاز:** تبقى كل بقية في 7B حتى اختيار مسبب بمالك ومدخل وخروج، ولا تستنتج صلاحية مرحلة 8 أو بدء الإصلاح.
- **المالك:** مالك نطاق التدقيق والأنساب والتسليم المستقل؛ **المدخلالمنقحالمطلوب:** crosswalk455FE وبقية SP01–03 ، وحصر caller/editor/field/writer/output ؛ آخر SHA راجعه قارئ الإصلاح إن ورد، والفصل بين 123 assertion inputs و 127 أداة تنفيذ.
- **أثرغيابه:** تبقى 7B/7 جزئيتين و 7C لم تبدأ؛ لا يمكن تحويل دفاتر التوكنات إلى حصر قدرات أو افتراض بدء الإصلاح أو تزامنه.؛ **الخطوة/الخروجالساكن:** اختيار R4s/7B35 أو split مسبب بقدرة وحدود ومالك ومدخل وخطوة وخروج مع تسليم SHA تدقيق مستقل. يثبتالعقدبدليلمحددأويبقى unresolved بمالك؛ لاانتقالإلىقبولتشغيليمننجاحوثائق.
- **الحد:** 20 شريحة تعاقدية و 8 سياق في 5 مسارات سابقة؛ 0 ملف كامل. لا مدة أو جلسات أو نسبة إكمال أو إصلاح أو قبول تشغيلي أو كل 455FE من دفتر توكنات.

**P7B34T-31 — محاولة إسقاط مدخل أو route قديم — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:احذف في نسخة اصطناعية upstream prefix أو mapped route أو بدّل disposition ، ثم شغل مقارنة الدفاتر الوثائقية. القبولالمستقل:يرفض المدقق الإخلال بالأنساب والمدخلات دون نقل البقية إلى 7C أو اختزالها إلى شرط session واحد. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

**P7B34T-32 — خلط هويات الالتقاط والتسليم والتاريخ — not-executed.** المتطلبات:إذن قبول مستقل لاحقاً وعقود product/DTO/provider منقحة ومراقب طلبات اصطناعي لا يتصل بحساب أو Chrome/SQL/طابعة/WhatsApp أو بيانات أعمال؛ لم ينفذ هذا القبول هنا. الإجراء:قدم في نسخة اصطناعية capture checkout خاطئاً أو مساواة 123 assertion inputs مع 127 execution tools أو timestamp معاد الوسم. القبولالمستقل:يرفض التحقق الخلط ويحفظ القيم الخام ومرجع 2026-11-16 والهوية الأصلية؛ لا يختلق تزامناً مع الإصلاح أو قبولاً. الضوابط:not-executed ؛ لا ERP/build/C#/VB/.NET/WPF/SQL/Selenium/Chrome/SDK/REPX/PDF أو رفع ملف أو هاتف أو QR أو رسالة أو مزود أو إصلاح أو قياس/قبول نُفذ هنا.

## 5. المصالحة بين دفاتر القدرة

| المعرف | القدرات | الجذورالقائمة | الخطط | الدليل |
|---|---|---|---|---|
| RC7B34-01 | FE7B34-01;FE7B34-02;FE7B34-03;FE7B34-04 | P6-033;P6-031 | P7B34T-01;P7B34T-02;P7B34T-03;P7B34T-04;P7B34T-05;P7B34T-06;P7B34T-07;P7B34T-08 | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3141;SmartAuditERP/Form_WPF/frmInvSale.xaml:1187-1191;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3132-3187;SmartAuditERP/Class/Session.cs:9-21;SmartAuditERP/Class/WhatsAppSender.cs:230-245;SmartAuditERP/Class/WhatsAppSender.cs:107-144 |
| RC7B34-02 | FE7B34-05;FE7B34-06;FE7B34-07;FE7B34-08 | P6-033 | P7B34T-09;P7B34T-10;P7B34T-11;P7B34T-12;P7B34T-13;P7B34T-14;P7B34T-15;P7B34T-16 | SmartAuditERP/Class/WhatsAppSender.cs:145-155;SmartAuditERP/Class/WhatsAppSender.cs:219-228;SmartAuditERP/Class/WhatsAppSender.cs:156-189;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3166-3187;SmartAuditERP/Class/WhatsAppSender.cs:181-189 |
| RC7B34-03 | FE7B34-09;FE7B34-10;FE7B34-11;FE7B34-12 | P6-033;P6-031 | P7B34T-17;P7B34T-18;P7B34T-19;P7B34T-20;P7B34T-21;P7B34T-22;P7B34T-23;P7B34T-24 | SmartAuditERP/Class/WhatsAppSender.cs:190-228;SmartAuditERP/Class/WhatsAppSender.cs:145-228;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3124-3128;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3185-3199;SmartAuditERP/Class/Session.cs:9-30;SmartAuditERP/Class/WhatsAppSender.cs:66-105 |
| RC7B34-04 | FE7B34-13;FE7B34-14 | P6-032;P6-033;P6-034 | P7B34T-25;P7B34T-26;P7B34T-27;P7B34T-28 | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3128-3165;SmartAuditERP/Class/WhatsAppSender.cs:107-118;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2986-3033;SmartAuditERP/Class/Print.cs:1193-1229 |
| RC7B34-05 | FE7B34-15 | H7B34-06 | P7B34T-29;P7B34T-30 | none-documentary-metadata |
| RC7B34-06 | FE7B34-16 | H7B34-06 | P7B34T-31;P7B34T-32 | none-documentary-metadata |

[RQ8](evidence/request-ownership-lineage-07B34.csv) · [AW8](evidence/await-boundary-lineage-07B34.csv) · [FE16](evidence/feature-implementation-matrix-07B34.csv) · [INV16](evidence/report-invariants-07B34.csv) · [32 خطة](evidence/acceptance-tests-07B34.csv) · [RC6](evidence/report-reconciliation-07B34.csv) · [AD8](evidence/root-adjudication-07B34.csv) · [امتدادات 0](evidence/historical-extensions-07B34.csv) · [شاهد 20+20](evidence/messaging-request-witnesses-07B34.json) · [حد ترشيح التاريخ](evidence/dedup-screen-07B34.json) · [RS14](evidence/residual-disposition-07B34.csv) · [SP3](evidence/split-register-07B34.csv) · [H6](evidence/handoffs-07B34.csv) · [Q6](evidence/questions-07B34.csv) · [workplan10](evidence/remaining-workplan-07B34.csv) · [backlog10](evidence/continuation-backlog-07B34.csv)

تبقى بقية callers/dialogs/editors/fields/writers/outputs وDocumentRef/allowed-set/branch/reset/dirty/cancel/failure وProduct/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome ضمن **SP01 و7B**. ويبقى **SP02** لحصر entry/source/output وcrosswalk455FE والدفاتر اللاحقة،و**SP03** لعقود SDK/DTO/constructors/collections/currency/precision/words/legacy/templates والسياسات،ضمن7B صراحة. تتبع await في واتساب لا يفتتح محورC3 العام ولا ينقل غير المراجع إلى7C.

التالي **R4s/7B35 أوsplit مسبب** منSP7B34-01–03:قدرة ومدخل ومصدر وحد مخرج واستبعاد ودليل ومالك ومدخل منقح وأثر وخطوة وخروج ساكن. لا وعد بمدة أوجلسات أوآخر جزء أونسبة تغطية أوإتمام النظام. يسلم SHA تدقيق محدد إلى الإصلاح المستقل دون افتراض بدئه أوتزامنه أودمج تعديلاته هنا.

لم ينفذ هنا ERP/build/C#/VB/.NET/WPF/SQL/DataView/provider/SDK/REPX/ToDataTable أوBAML أوSelenium/Chrome/QR/WhatsApp أوSMTP أوطابعة/ماسح/PDF أوملف فاتورة/هاتف حقيقي أوبيانات أعمال/أسرار أوحفظ/دفع/إصلاح/قياس/قبول تشغيلي. الأمثلة رموز؛الجدولة والجاهزية والرجوع وحالات staleness موردة صراحة،وليست thread schedule أوDOM منشوراً اختُبر. غياب setter أوdirty write صريح أومصدر DTO متتبع ليس إثبات غياب حماية أوقدرة. خاصية Print.defPrinter المحلية معروفة من B33،لكن عقود SDK/constructor/collections/events وmapping/export/المتصفح لا تزال غير محسومة. كل32 خطةB34 و32B33/B32/B31/B30/B29/B28 و36B27 **not-executed**.
