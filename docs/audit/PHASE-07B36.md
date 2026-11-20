# المرحلة 7B36/R4t — طلب منتقي الفاتورة ونتيجته عند أول حوار

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**دخول B36:** تسليم B35 المدفوع `9769e29b8ce34f720fd660a475800f5c3bf9b7fa`؛ **1126 مادة تدقيق و 335 نتيجة مفتوحة** قبل الإضافات الحالية.
المرجع المورّد للمتابعة **2026-11-16 UTC** مستقل عن ساعة البيئة الخام `2026-11-20T22:21:00.166580+00:00`. لا معايرة للتقويم من نجاح assertions ولا إعادة وسم لأثر مستهلك. [التاريخ وهويات الآثار](DATE-IDENTITY-NOTE-07B36.md).

**تدقيق ساكن فقط؛ لا تعديل للتطبيق أو إصلاح أو تشغيل ERP. R4t/7B36 شريحة محدودة؛ 7B والمرحلة 7 جزئيتان؛ 7C لم تبدأ؛ 8 غير مأذونة هنا.** الإصلاح مستقل، وبدؤه وتزامنه غير معلومين؛ لا دمج repair→audit أو كتابة ملفاته أو إغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[الخلاصة](PHASE-07B36.md) · [عقود طلب البحث ونتيجته](INVOICE-PICKER-CONTRACTS-07B36.md) · [التحقق](VALIDATION-07B36.md) · [المتبقي وسلطة المتابعة](PHASE-07-REMAINING-07B36.md) · [الهوية](DATE-IDENTITY-NOTE-07B36.md) · [النطاق](review-scope-07B36.csv) · [قرار الاختيار](evidence/scope-decision-07B36.json) · [السجل دون تعديل](findings.csv) · [stdout الرسمي](evidence/checks-07B36.json)

## 1. النتيجة وحدّ الجديد

**الأحدث: 7B36/R4t — طلب منتقي الفاتورة ونتيجته عند أول حوار في InsertFromInv. صفر جذور جديدة وصفر امتدادات evidence للسجل.** تعميق توثيقي مرتبط بـ **P7-157 و P7-160** دون تعديل أدلتهما أو يقينهما في السجل، ودون P7-164 أو نتيجة مستقلة لكل إيماءة.

التراكمي ثابت: **335 نتيجة مفتوحة بلا معالجة: 2Critical /181High /151Medium /1Low؛ 296confirmed /32potential /7repository-gap**.

- المنشئ يلتقط نتيجة `ConnObj` ويضع حالة محلية جديدة قبل تعيينات المستدعي؛ حقول عامة وليست كائن SearchRequest ثابتاً. آثار permission/settings وملكية الاتصال وخرائط enum غير معتمدة هنا.
- **Enter** يقرأ الصف بالفهرس ثم يكتب `ISDone` والحمولة ويطلب Close؛ أما الفهرس غير الصالح مع صفوف موجودة فيطلب اختيار الصف الأول فقط. **النقر المزدوج** يقرأ SelectedItem ويطلب Hide؛ null لا يقبل. لا trace إطار ولا ادعاء desync فعلي بين الاختيارين.
- حارس المستدعي بعد رجوع الحوار المورّد هو `ISDone & GID!=-1`؛ يطلب BindingInvoice قبل حوار البنود، ولا يثبت LoadComplete أو AcceptedLines أو أهلية النوع والفرع والسنة. **الحارس لا يساوي قبولاً تشغيلياً أو حفظاً.**
- predicate غير التعاقدية تسمح 20 أو النوع المطلوب؛ هذه آلية **157 القائمة**. اختلاف مرشح ProcType المحلي عن المصدر **155 القائمة**، وصحة اللقطة/بقاء القديم تحفظ **046 بامتداد B28**؛ لا إعادة عد.
- **تصحيح حد القراءة:** أُعيدت قراءة C# المحلية كاملةً، 698 سطراً، وقد راجعتها B27/B28 كاملة سابقاً؛ **صفر ملفات جديدة مكتملة**. XAML والمساعد مقاطع فقط؛ 20 شريحة تعاقدية+6 سياق في 3 مسارات قديمة، وليس كل caller أو كل SQL/DataView. 3 تقاطع+0 جديد→اتحاد 428/متمم 399، دفتر مسارات لا نسبة قدرات.

اختير هذا العقد من[المتبقي B35](PHASE-07-REMAINING-07B35.md) و SP7B35-01 و RS14/workplan/backlog. **لا يوسّع ذلك B35 رجعياً إلى داخل أول منتقٍ**؛ الجديد هنا تتبع constructor→caller request→source/display row→Enter/double-click→caller gate. سياق الاستعمال هو المساعد المشترك للمرتجع المرتبط في السنة الحالية الذي وثقته B35، لا اعتماد كل متصل أوكل فعل في النافذة.

[PQ8](evidence/picker-request-lineage-07B36.csv) · [PR8](evidence/picker-result-lineage-07B36.csv) · [FE16](evidence/feature-implementation-matrix-07B36.csv) · [INV16](evidence/report-invariants-07B36.csv) · [32 خطة غير منفذة](evidence/acceptance-tests-07B36.csv) · [RC6](evidence/report-reconciliation-07B36.csv) · [AD8](evidence/root-adjudication-07B36.csv) · [امتدادات 0](evidence/historical-extensions-07B36.csv) · [الشاهد 20+20](evidence/invoice-picker-witnesses-07B36.json) · [مقارنة التاريخ](evidence/dedup-screen-07B36.json) · [RS14](evidence/residual-disposition-07B36.csv) · [SP3](evidence/split-register-07B36.csv) · [H6](evidence/handoffs-07B36.csv) · [Q6](evidence/questions-07B36.csv) · [workplan10](evidence/remaining-workplan-07B36.csv) · [backlog10](evidence/continuation-backlog-07B36.csv)

## 2. السلسلة المصدرية وضوابطها

### أ. المنشئ قبل طلب المستدعي

الدليل: `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:22-66`؛ `SmartAuditERP/Class/InvoiceOper.cs:3941-3976`.

ينشئ InsertFromInv نافذة جديدة. يبدأ المنشئ بـ InitializeComponent، ثم يستدعي MainClass.ConnObj ويضع proc1/pay1/type6 و GID=-1 و ISDone=false والفهرس-1 ومجموعة عرض جديدة. بعد ذلك يعطّل المستدعي اختيار العملية، ويمر على permission/settings، ثم يعيّن Ptype ويختار InvType من فروعه العامة ويطلب ShowDialog. الفرع المسمى ReturnSales يعيّن InvType=1 و hint22؛ لا نعتمد من ذلك خريطة enum الرقمية المفقودة أو سياسة 20 أو المسارات الأخرى.

الترتيب المحلي معلوم، لكن **رمز الاتصال conn-A لا يثبت قاعدة الاتصال أو حياته أو ملكيته**، ولا يثبت أن تغيير متغير global لاحقاً أعاد توصيل _conn. آثار InitializeComponent/permission/settings غير محسومة. هذه ليست شهادة أن كل تحميل استعمل الطلب نفسه؛ والافتراضات المحلية ليست افتراضات InvoiceDGV الخارجية.

### ب. المصدر ومرشح العرض ليسا طلباً واحداً ثابتاً

الدليل: `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:73-86`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:138-143`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:310-408`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:492-519`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml:229-238`.

ينادي Loaded تحميل القوائم ثم LoadInvoices ثم ApplyColumnVisibility بهذا الترتيب النصي؛ لا نحوله إلى عدد events مرصود. يضيف BuildLoadQuery شرط proc الأصلي والفرع لغير 14 والحذف، وفي غير 23 يسمح بالنوع 20 أو النوع المطلوب. النوع 23 ضابط exact-kind خارج اعتماد هذا الأمر، و OR20 ليست UNION تولّد نسخة مضاعفة للصف نفسه.

مرشح SelectedIndex المحلي بعد التحميل لا يستعيد صفوفاً منعها مصدر الطلب؛ هذه **155 الموثقة**، ومجموعة 20/requested هي **157 الموثقة**. تعطيل control أو hint22 لا يصيران عقد أهلية نافذاً بمجرد اسم حقل. السياسة ومصفوفة الدعم مطلوبتان من المالك؛ لم تنفذ query ولم يختبر اتساق DB.

### ج. صف محلي معلوم، لا DocumentRef كامل

الدليل: `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:567-596`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:674-698`.

تعريف InvoiceSrchRow المحلي معلوم ويستعمل auto-properties. مسارات القبول تنقل GID/proc/pay فقط؛ ولا يحمل الصف source type/branch/InvoiceStatus كعقد DocumentRef موحّد. هذا لا يعني أن GlobalID خاطئ أو أن كل حماية غائبة؛ إنه حد معلومات بين الطلب والاختيار والاستهلاك. لا تستنتج عقود SDK/InvoiceDGV أو enum/clone/collections من هذا التعريف المحلي.

### د. Enter و double-click عند نشر النتيجة

الدليل: `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:88-116`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:261-284`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml:1-14`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml:397-414`.

مع فهرس صالح مورّد، يقرأ Enter من _displayRows ثم يكتب ISDone=true قبل GID/proc/pay ويطلب Close داخل try. مع فهرس غير صالح ومجموعة غير فارغة يطلب SelectedIndex=0 و Scroll فقط؛ لا يكتب قبولاً في ذلك الفرع. لا يستنتج النموذج حدوث SelectionChanged أو إعادة تنفيذ Enter بسبب هذا الطلب. المجموعة الفارغة ضابط سلبي آخر.

النقر المزدوج يقرأ SelectedItem ويعود مع null؛ ومع صف مورّد يكتب done والحمولة ثم يطلب Hide. تزويد النموذج بـ index0 و SelectedItem للصف B يوضح اختلاف مصدر القراءتين، لكنه **ليس دليلاً على desync فعلي في WPF**. Close/Hide طلبان محليان؛ رجوع ShowDialog معطى مستقل، ولا يستنتج من مجرد بلوغ التعليمة. لا نفترض استثناء getter مجهولاً لخاصية محلية معلومة، ولا حالة UI نهائية بعد أحداث الإطار.

### هـ. إغلاق جسم جديد دون قبول، ثم حارس الاستهلاك

الدليل: `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:88-132`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml:172-187`؛ `SmartAuditERP/Class/InvoiceOper.cs:3976-3985`؛ `SmartAuditERP/Class/InvoiceOper.cs:4002-4013`.

Escape وزر الإغلاق لا يكتبان done/GID. مع جسم جديد وسنة حالية مورّدة يبقى false/-1 عند الحد المحلي. زر الإغلاق له فرع استعادة global للسنة السابقة؛ Escape لا يمر به في جسمه. هذا سياق غير معتمد كأمر سنة سابقة، ولا يفترض سلوك chromeX أو إعادة الاستعمال أو فئة موروثة.

بعد **رجوع الحوار المورّد** يحرس المساعد القراءة بـ ISDone و GID!=-1. false أو-1 ضابطان يرفضان الحد؛ قيمة فارغة مورّدة قد تجتاز شرط sentinel، لكن لا دليل أنها ظهرت فعلياً أو أصبحت عيباً مستقلاً. عند الاجتياز يطلب BindingInvoice بمعيار IS_Deleted/GID قبل عرض البنود. لا يثبت هذا الحارس إعادة فحص نوع الطلب أو العملية أو الفرع أو صحة لقطة العرض، ولا LoadComplete أو AcceptedLines. أحكام إلغاء الطفل وتحميل ref السابقة محفوظة في[B35](LINKED-RETURN-CONTRACTS-07B35.md)؛ لا يستخلص SaveResult أو rollback جديد هنا.

### و. الفشل وزر Return — سياق لا توسيع لشهادة الأمر

الدليل: `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:286-303`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:310-334`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:492-508`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs:567-636`؛ `SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml:524-546`.

- Fill يسبق ApplyFilter، والعرض يُمسح قبل إضافة الصفوف المحوّلة. حدود الفشل before-clear/after-clear/during-row **مورّدة**؛ توضح القديم/الفارغ/prefix عند حد محدد، لا استثناء Convert أو DataAdapter منفذاً أو صلاحية كل DataView. امتداد 046 في B28 يغطي عقد القديم المعروف؛ وسياسة Partial والنشر باقية للمالك، لا finding جديدة.
- زر Return يقرأ Button.Tag وينادي IsPreviousReturned ثم ينشر الحقول ويضع done ويطلب Hide. Enter/double-click لا يناديان ذلك lookup في جسميهما. found يرفض، و catch-false في lookup لا يعيد Failed typed؛ لكن **مقصد الزر ومصفوفة دعمه ومعنى هذا الفشل باقية 7B**. لا يعتمد ذلك زر Return في المسار المحدد، ولا ينشئ نتيجة مرتجع دون سياسة المالك.
- ApplyColumnVisibility تستعمل ProcType==2 عند استدعائها. لا يثبت هذا أن كل عرض أو gesture داخلها صدر عن caller الحالي أو ينتمي إلى المتطلب نفسه.

## 3. منع العدّ ونقل اليقين

حفظ[dedup](evidence/dedup-screen-07B36.json) **335 صف metadata و 69 صفاً يطابق أحد المسارات الثلاثة حرفياً في evidence و 11 قسماً تاريخياً منتقى**، ومقطعين إضافيين لامتداد 046 في B28 والعقد المحدود B35. ليست قراءة 335 أو 69 متناً تاريخياً، ولا حصر جميع callers. توثق بصمات الآثار والأقسام ما قورن فعلاً.

تستمر 157 و 160 دون registrytail أو ترقية يقين عند متصل جديد. تبقى 155/156/158 و 046 بحدودها مستقلة، وكذلك 159/161 و 012/013 والضوابط 014/145. **استكشاف الضوابط لا ينشئ جذوراً جديدة**، ولا يمحو ما كان unresolved بمجرد مرور حارس-1. المقترح غير المنفذ هو SearchRequest/ResultSnapshot/DocumentRef و PickerOutcome صريحة بـ request-id وصحة لقطة وقبول ذري، دون فرض SDK أو سياسة أعمال غير متاحة.

## 4. الحفظ والتحقق والمتابعة

حُفظت **1122 مادة دخول محمية من 1126 بايتياً**، وتشمل `findings.csv` نفسها: **كل 335 قاموساً بكل حقل وكامل raw336CRLF/222939 بايت، دون BOM**. لا تعديل evidence أو status أو severity أو certainty أو type أو next_phase أوالترميز ونهايات الأسطر. المسارات الأربعة المعلنة القابلة للتحديث وحدها: README/PLAN/IMPROVEMENTS و tools/validate_audit.py؛ بقية العمل ملفات B36 جديدة.

**G01–260 وصفوفها exact؛ G261–264 توصيات غير منفذة وليست أربع نتائج أخرى.** بقيت 827 أصل تطبيق/29,128,444 بايت كما هي. تشمل الحماية كل مواد B35: LN8/NR8/FE16/INV16/RC6/AD8/T32/RS14/SP3/HQ6/RW10/BK10/ext0 وشاهده وأخطاء بنائه وأرشيف 40 وبرهانه و stdout الرسمي وإيصاله وفحوصه؛ و B34 RQ8/AW8 و B33 OS8/OV8 و B32 EO8/DG8 وجميع الدفاتر الأقدم. أعداد B35 التاريخية 1071/1075 و B34 التاريخية 1018/1022 لا يستبدلها عدّ الحالي.

**P4-014 و P7-108 و P7-132 و P7-145 potential كما هي**؛ 020/021 وحواجز المال و ACL والمخزون والحفظ والإنتاج باقية. ذيل 159 في B30 وامتداد 046 في B28 محفوظان؛ 013 و 155/156/158/159/161 أسباب مستقلة بشروطها. تصحيح B10 الإضافي 10 محلياً/120 مرجعياً/equality1=10 باقٍ دون تحرير G138.

اجتازت **كل 52 حالة B35 الأصلية دون تعديل أو تخطٍّ** [تشغيلاً مستقلاً](evidence/historical-B35-direct-07B36.json):exit0 و stdout0 و stderr354 بايت من unittest/provenance. واجتاز [CLI تاريخي مستقل B35](evidence/historical-B35-CLI-preflight-07B36.json) **1242/36 و 335/827 و errors[]/exit0 و outerstderr0** قبل أرشيف 41؛ هذا OWN335 وليس defaultB36. [إيصال CLI](evidence/historical-B35-CLI-preflight-07B36-receipt.json) يسجل 353181 بايت وبقاء 135 أداة و 1122 مادة محمية دون تغيير أثناءه. هذه نتيجة فعلية مستقلة، لا إعادة وسم لخرج الدخول أوالرسمي B35.

المحولة تورّد **OWN335/raw336CRLF/indexes/presetB35 و 131 هوية source assertion و dispatcher TEXT canonical** عبر A/Path محليين في module الطفل فقط، مع restore حتى عند الخطأ. النص بيانات assertion لا code قديم منفذ. لا تغيير v.__file__/main.__code__ أو globalPath/shared-subprocess أو disk overlay أو protected-test edits أو skip/filter/rebaseline. يفحص الجزء الجديد **LIVE36/versioned35/API15/19gates و 135 أداة تنفيذ فعلية** مستقلة؛ B34=127 و B33=123 و B32=119 و B31=115 و B30=111 و B29=107 مدخلات تاريخية منفصلة. الجزء المبلغ عنه في B35=121 ليس كامل 131؛ والجزء المتوقع B36=125=121+4 وليس كامل 135 أو 131 مدخل assertion.

<!-- B36_HISTORICAL_START -->
اكتملت **41 عملية OWN تاريخية فعلية:2–6 و A و B1–35**، وكلها exit0 و errors[] و stderr خارجية فارغة و 827 أصلاً مطابقاً. ليست fixtures أو نسخ prefix؛ كل عملية تستعمل سجلها وفهارسها وإعدادها التاريخي. [الأرشيف](evidence/historical-mode-verification-07B36.json) **229980 بايت**، SHA-256:`de4d9f7b4b8f689ba69735dfe8fe6c9d67a408225300f6e2fd2b35d7f0fdaa48`؛ خلاصات وهويات stdout لا كامل التيارات. القيم null للتجميعات غير المبلغ عنها لا تساوي 0. آخر عملية B35 مرّت بـ 335/1242/36 و OWN `evidence/findings-through-07B35.csv`، لا defaultB36.

[برهان هوية الالتقاط](evidence/capture-time-identity-07B36.json) **10137 بايت**، SHA-256:`1eed40ea4f3c487b2abe96a4a349ebceab151d03eecc19a62764b2ec8d52b0b5`، يثبت إعادة فحص التيارات الإحدى والأربعين المؤقتة وبقاء **134 من 135 أداة مطابقة**. التغيير اللاحق الوحيد هو pin بصمة الأرشيف في `tools/validate_invoice_picker_part.py`؛ استبدال exact واحد في الذاكرة يعيد بايتاته وقت الالتقاط وبصمتها. لم يعدل dispatcher أوالاختبار الجديد بعد الالتقاط، ولم يغيّر أي سجل بصمات مستهلك. **لا ادعاء إعادة 41 كاملة بعد pin أوإنهاء النصوص والفهارس أوالدفع.** تبقى 131 هوية assertion تاريخية B35 منفصلة عن 135 أداة التنفيذ الفعلية، ويبقى برهان B35 التاريخي وصفاً لالتقاطه لا لالتقاط B36.
<!-- B36_HISTORICAL_END -->

<!-- B36_CURRENT_VALIDATION_START -->
اجتاز **CLI الافتراضي الفعلي B36 في فحص تمهيدي مستقل:1294 حالة وثائقية في 37 مجموعة** =1242 حالة سابقة محفوظة دون تعديل أو تخطٍّ+52 جديدة؛ **335 نتيجة مفتوحة و 827 أصلاً مطابقاً، errors[] و exit0 و stderr الخارجية فارغة**. [الفحص التمهيدي 01](evidence/checks-07B36-preflight01.json) خرج فعلي عند دخول B36 `9769e29b8ce34f720fd660a475800f5c3bf9b7fa`؛ **364068 بايت**، SHA-256:`3cdcd381b81a6be28804df3b5ac3e0173344b04db7167f0c8e85965a0738ed55`. يثبت[إيصاله](evidence/preflight01-receipt-07B36.json) بقاء كل 1171 مدخل تدقيق دون تغيير أثناءه؛ مرّ الغلاف نفسه دون أخطاء. لم يكن الملف الرسمي قد كتب آنذاك، ولا يعاد وسم هذا الخرج بأنه رسمي.

جاء ذلك بعد اجتياز [52 الجديدة مستقلة](evidence/current-B36-direct-07B36.json) بـ exit0 و stdout0 و stderr151 بايت من unittest. لا يستنتج من هذا التيار أو فراغ outerstderr خلو كل طفل تاريخي من التحذيرات. يحصر الحقل الكامل **135 أداة تنفيذ** ويطابق glob مستقلاً؛ والحقل الجزئي **125 بصمة مطابقة** =مفاتيح 121 المبلغ عنها في B35+أربع أدوات B36. ليست 125 كامل 135، وليست 131 مدخل assertion تاريخياً لـ B35.

[stdout الرسمي](evidence/checks-07B36.json) مخصص لعملية افتراضية مستقلة جديدة مباشرة إلى ملف حصري **بعد إنهاء التقارير والفهارس**؛ لا placeholder أو JSON مركب أو نسخة preflight/postpush. هويته checkout الدخول 9769e29 مع بصمات أدوات ومحتوى worktree الفعلي، قبل commit التسليم اللاحق. إيصال `evidence/official-capture-receipt-07B36.json` يكتب بعد خروج العملية، وليس مدخلاً لذاته أو stdout. [مذكرة إنهاء النصوص](evidence/finalization-note-07B36.json) تسجل تغيرات التقارير الثمانية وحدها بعد preflight؛ تحقق الإصدار والإيصال هما ما يثبت نجاح الالتقاط النهائي وبقاء مدخلاته، لا هذه الفقرة وحدها.

تبقى **كل 32 خطة B36 وجميع الخطط التشغيلية السابقة not-executed**. ليست 1294 اختبارات ERP أو WPF أو SQL/provider/SDK أوحفظ أوحجز رقم أوإصلاح أوقياس أوقبول تشغيلي.
<!-- B36_CURRENT_VALIDATION_END -->

لم ينفذ ERP/build/C#/VB/.NET/WPF/ShowDialog/SQL/DataView/provider/SDK/REPX/ToDataTable أو طابعة/ماسح أو بيانات أعمال/أسرار أو حفظ أو حجز رقم أو إصلاح أو قياس أو قبول تشغيلي. الصفوف والفهارس و SelectedItem ورموز الاتصال ورجوع الحوار وحدود الفشل **مدخلات رمزية مورّدة لا آثار تشغيل مرصودة**. نعرف auto-properties لـ InvoiceSrchRow المحلية، ولا نعممها على InvoiceDGV أو SDK/constructors/collections/setters/alias/clone/enum أو اكتمال hydration.

**كل 32 خطة B36 وجميع الخطط التشغيلية السابقة، ومنها 32B35/B34/B33/B32/B31/B30/B29/B28 و 36B27، not-executed.** اختبارات Python التوثيقية ليست تنفيذ تلك الخطط أو نجاحاً للواجهة أو قاعدة البيانات أو إصلاحاً.

يبقى زر **Return** المنفصل وفحصه الخاص والسنة السابقة و chrome/إعادة فتح الحوار وكل caller آخر وأعمال editors/fields/writers/outputs ضمن **SP01 و 7B**. قراءة سياقها لا تعتمدها. تبقى DocumentRef/allowed-set/branch/reset/dirty/cancel/failure و Product/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome بعقودها المستقلة، ولا تُختزل إلى ISDone.

**SP02** لحصر القدرات entry/source/output و crosswalk455FE والدفاتر اللاحقة، و**SP03** لعقود SDK/DTO/constructors/collections/currency/precision/words/legacy/templates والسياسات، ضمن 7B صراحة. لا تنقل القدرات غير المقروءة إلى 7C ولا يفتتح هذا التتبع محور C3 العام.

التالي **R4u/7B37 أو split مسبب من SP7B36-01–03**: قدرة ومدخل ومصدر وحد مخرج واستبعاد ودليل ومالك ومدخل منقح وأثر غيابه وخطوة وخروج ساكن. لا وعد بمدة أو جلسات أو آخر جزء أو نسبة قدرات أو إتمام المنظومة. يسلم SHA تدقيق محدد إلى الإصلاح المستقل دون افتراض بدئه أو تزامنه أو دمج تعديلاته هنا.
