# عقود طلب منتقي الفاتورة ونتيجته — 7B36/R4t

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**دخول B36:** تسليم B35 المدفوع `9769e29b8ce34f720fd660a475800f5c3bf9b7fa`؛ **1126 مادة تدقيق و 335 نتيجة مفتوحة** قبل الإضافات الحالية.
المرجع المورّد للمتابعة **2026-11-16 UTC** مستقل عن ساعة البيئة الخام `2026-11-20T22:21:00.166580+00:00`. لا معايرة للتقويم من نجاح assertions ولا إعادة وسم لأثر مستهلك. [التاريخ وهويات الآثار](DATE-IDENTITY-NOTE-07B36.md).

**تدقيق ساكن فقط؛ لا تعديل للتطبيق أو إصلاح أو تشغيل ERP. R4t/7B36 شريحة محدودة؛ 7B والمرحلة 7 جزئيتان؛ 7C لم تبدأ؛ 8 غير مأذونة هنا.** الإصلاح مستقل، وبدؤه وتزامنه غير معلومين؛ لا دمج repair→audit أو كتابة ملفاته أو إغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[الخلاصة](PHASE-07B36.md) · [عقود طلب البحث ونتيجته](INVOICE-PICKER-CONTRACTS-07B36.md) · [التحقق](VALIDATION-07B36.md) · [المتبقي وسلطة المتابعة](PHASE-07-REMAINING-07B36.md) · [الهوية](DATE-IDENTITY-NOTE-07B36.md) · [النطاق](review-scope-07B36.csv) · [قرار الاختيار](evidence/scope-decision-07B36.json) · [السجل دون تعديل](findings.csv) · [stdout الرسمي](evidence/checks-07B36.json)

## 1. الحدود التي لا تُستبدل ببعضها

1. **SearchRequest** مستقل عن حقل ProcType القابل للتغيير ومرشح العرض اللاحق.
2. **ResultSnapshot** مستقل عن مدى نجاح نشر الصفوف؛ Found/Empty/Failed/Partial ليست حالة واحدة.
3. **AcceptedDocument** مستقل عن AbandonDecision و AcceptedLines و LoadComplete؛ ليس ISDone عقد حفظ.
4. **تعريف InvoiceSrchRow المحلي** لا يثبت SDK/InvoiceDGV أو enum أو connection/clone/alias.
5. **طلب Close/Hide** مستقل عن رجوع modal مورّد؛ زر Return والسنة السابقة سياق لا شهادة أمر.

النطاق أول حوار فقط بالمساعد المشترك في السنة الحالية. [الخلاصة](PHASE-07B36.md) تضبط المصدر وموضع الاستنتاج والضوابط؛ [FE16](evidence/feature-implementation-matrix-07B36.csv) تحفظ المسؤولية والمدخلات والاستبعادات والأثر والخروج لكل قدرة.

## 2. crosswalk محدود — 16 قدرة و 32 خطة غير منفذة

| FE/INV | القدرة المحددة | النتيجة القائمة/العقد | خطتا القبول — not-executed | المالك |
|---|---|---|---|---|
| FE7B36-01 / INV7B36-01 | الإنشاء قبل طلب المستدعي | P7-160 | P7B36T-01;P7B36T-02 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-02 / INV7B36-02 | الافتراضات المحلية وحد الاتصال الخارجي | H7B36-02 | P7B36T-03;P7B36T-04 | مالك العقد المحلي و SDK/DTO والاتصال والتحميل |
| FE7B36-03 / INV7B36-03 | طلب المصدر ومرشح العملية المحلي | P7-155 | P7B36T-05;P7B36T-06 | مالك المنتج وسياسة أهلية طلب البحث والاختيار |
| FE7B36-04 / INV7B36-04 | allowed-set القديمة 20/requested | P7-157 | P7B36T-07;P7B36T-08 | مالك المنتج وسياسة أهلية طلب البحث والاختيار |
| FE7B36-05 / INV7B36-05 | هوية الصف وحد حمولة DocumentRef | P7-157 | P7B36T-09;P7B36T-10 | DBA ومالك هوية المستند والفرع والسنة |
| FE7B36-06 / INV7B36-06 | Enter بفهرس مورّد صالح | P7-160 | P7B36T-11;P7B36T-12 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-07 / INV7B36-07 | Enter دون فهرس صالح | P7-160 | P7B36T-13;P7B36T-14 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-08 / INV7B36-08 | double-click مع SelectedItem/null | P7-160 | P7B36T-15;P7B36T-16 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-09 / INV7B36-09 | زر Return كسياق غير معتمد | H7B36-03 | P7B36T-17;P7B36T-18 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-10 / INV7B36-10 | الإغلاق الجديد دون قبول | P7-160 | P7B36T-19;P7B36T-20 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-11 / INV7B36-11 | صحة لقطة العرض وفشل مورّد | H7B36-05 | P7B36T-21;P7B36T-22 | مالك لقطة البحث وصحتها وسياسة الفشل |
| FE7B36-12 / INV7B36-12 | حارس المساعد ليس LoadComplete | P7-160;P7-157 | P7B36T-23;P7B36T-24 | مالك أوامر WPF ونشر نتيجة البحث |
| FE7B36-13 / INV7B36-13 | المعلوم محلياً مقابل SDK | H7B36-02 | P7B36T-25;P7B36T-26 | مالك العقد المحلي و SDK/DTO والاتصال والتحميل |
| FE7B36-14 / INV7B36-14 | حد السنة والفرع والحفظ | H7B36-04 | P7B36T-27;P7B36T-28 | DBA ومالك هوية المستند والفرع والسنة |
| FE7B36-15 / INV7B36-15 | منع العد وحفظ السجل | H7B36-06 | P7B36T-29;P7B36T-30 | مالك نطاق التدقيق والأنساب والتسليم المستقل |
| FE7B36-16 / INV7B36-16 | الأنساب والمتبقي وسلطة التسليم | H7B36-06 | P7B36T-31;P7B36T-32 | مالك نطاق التدقيق والأنساب والتسليم المستقل |

لكل صف CSV مدخل entry_point ومصدر source_contract وحد output_boundary واستبعاد excluded_from_claim ومالك ومدخل منقح وأثر غيابه وخطوة وخروج. لكل خطة prerequisites/procedure/acceptance_criterion وسلامة وحالة not-executed. ليست 16 حصراً عاماً للقدرات أو 455FE.

## 3. PQ8 و PR8 — unions أدلة وحدودمرتبة

### PQ8 — منالإنشاءإلىطلبالبحث

| المعرف | FE المرتبطة | الجذور/العقود | الحد الموثق | الحالة |
|---|---|---|---|---|
| PQ7B36-01 | FE7B36-01;FE7B36-02 | P7-160;H7B36-02 | InsertFromInv→new frmInvoiceSrch→permission/settings→ProcType → طلب ShowDialog لحقول عامة وليس SearchRequest immutable ∣ constructor→ConnObj→defaults→ItemsSource → local result baseline معلومة لا defaults InvoiceDGV | not-executed |
| PQ7B36-02 | FE7B36-03;FE7B36-04 | P7-155;P7-157 | Window_Loaded→LoadInvoices ثم cmbProcType event → All0 محلي لايعيدصفوفاً استبعدهاالمصدر ∣ BuildLoadQuery للنوع غير 23 → مرشح 1 قد يعرض 20؛ لا حسمقصدالمالك منالاسم | not-executed |
| PQ7B36-03 | FE7B36-05;FE7B36-06 | P7-157;P7-160 | RefreshDisplayRows→InvoiceSrchRow→result fields → GlobalID محفوظ لكن ليس DocumentRef كامل الأهلية ∣ Window_KeyDown مع Return و _rowIndex صحيح → قبول محلي مشروطبصفوفوفهرسمورّدين | not-executed |
| PQ7B36-04 | FE7B36-07;FE7B36-08 | P7-160 | Return مع _rowIndex=-1 ومجموعةموجودةأوفارغة → طلب اختيار أول صف وليس SelectedResult تلقائياً ∣ dgvItems_MouseDoubleClick و SelectedItem موردة → مسار SelectedItem لا شهادة تطابقه مع _rowIndex فيالواجهة | not-executed |
| PQ7B36-05 | FE7B36-09 | H7B36-03 | Button.Tag→IsPreviousReturned→Hide؛ ColReturnInv محلياًproc2 → قراءةسياقلااعتماد Return أوحكمجذرجديدبالتشابه | not-executed |
| PQ7B36-06 | FE7B36-10;FE7B36-11 | P7-160;H7B36-05 | Escape أو btnClose_Click على freshpicker → freshcancel عندالحدالمحلي، لا قاعدةلكلإغلاقموروث ∣ ApplyFilter→RefreshDisplayRows → لا نتيجة health typed؛ عقد Partial مفتوح و 046B28 محفوظة | not-executed |
| PQ7B36-07 | FE7B36-12;FE7B36-13 | P7-160;P7-157;H7B36-02 | ShowDialog(return supplied)→ISDone & GID!=-1 → حارسنتيجةبحث لا LoadComplete أو AcceptedLines ∣ InvoiceSrchRow auto-properties مقابل ref InvoiceDGV → لا تعميم default/alias/clone/notifications أو hydration | not-executed |
| PQ7B36-08 | FE7B36-14;FE7B36-15;FE7B36-16 | H7B36-04;H7B36-06 | current-year input→local branch predicate→gid boundary → لا مصدرحقيقةأورصيدمرتجعأو ACL أو save/stock/financialloss ∣ dedup metadata335 و 69literalpaths و 11sections → 335 قاموساً وكامل raw336 ثابتة؛ لا P7-164 ∣ RS14/SP3/HQ6/RW10/BK10 من B35 → 7B/7 جزئيتان؛ 7C لمتبدأو 8 غيرمأذونة، repair بدؤهوتزامنهمجهولان | not-executed |

### PR8 — منالصفإلىحارسالمستهلك

| المعرف | FE المرتبطة | الجذور/العقود | الحد الموثق | الحالة |
|---|---|---|---|---|
| PR7B36-01 | FE7B36-01;FE7B36-02 | P7-160;H7B36-02 | InsertFromInv→new frmInvoiceSrch→permission/settings→ProcType → طلب ShowDialog لحقول عامة وليس SearchRequest immutable ∣ constructor→ConnObj→defaults→ItemsSource → local result baseline معلومة لا defaults InvoiceDGV | not-executed |
| PR7B36-02 | FE7B36-03;FE7B36-04;FE7B36-05 | P7-155;P7-157 | Window_Loaded→LoadInvoices ثم cmbProcType event → All0 محلي لايعيدصفوفاً استبعدهاالمصدر ∣ BuildLoadQuery للنوع غير 23 → مرشح 1 قد يعرض 20؛ لا حسمقصدالمالك منالاسم ∣ RefreshDisplayRows→InvoiceSrchRow→result fields → GlobalID محفوظ لكن ليس DocumentRef كامل الأهلية | not-executed |
| PR7B36-03 | FE7B36-06 | P7-160 | Window_KeyDown مع Return و _rowIndex صحيح → قبول محلي مشروطبصفوفوفهرسمورّدين | not-executed |
| PR7B36-04 | FE7B36-07 | P7-160 | Return مع _rowIndex=-1 ومجموعةموجودةأوفارغة → طلب اختيار أول صف وليس SelectedResult تلقائياً | not-executed |
| PR7B36-05 | FE7B36-08 | P7-160 | dgvItems_MouseDoubleClick و SelectedItem موردة → مسار SelectedItem لا شهادة تطابقه مع _rowIndex فيالواجهة | not-executed |
| PR7B36-06 | FE7B36-09;FE7B36-10 | H7B36-03;P7-160 | Button.Tag→IsPreviousReturned→Hide؛ ColReturnInv محلياًproc2 → قراءةسياقلااعتماد Return أوحكمجذرجديدبالتشابه ∣ Escape أو btnClose_Click على freshpicker → freshcancel عندالحدالمحلي، لا قاعدةلكلإغلاقموروث | not-executed |
| PR7B36-07 | FE7B36-11;FE7B36-12;FE7B36-13 | H7B36-05;P7-160;P7-157;H7B36-02 | ApplyFilter→RefreshDisplayRows → لا نتيجة health typed؛ عقد Partial مفتوح و 046B28 محفوظة ∣ ShowDialog(return supplied)→ISDone & GID!=-1 → حارسنتيجةبحث لا LoadComplete أو AcceptedLines ∣ InvoiceSrchRow auto-properties مقابل ref InvoiceDGV → لا تعميم default/alias/clone/notifications أو hydration | not-executed |
| PR7B36-08 | FE7B36-14;FE7B36-15;FE7B36-16 | H7B36-04;H7B36-06 | current-year input→local branch predicate→gid boundary → لا مصدرحقيقةأورصيدمرتجعأو ACL أو save/stock/financialloss ∣ dedup metadata335 و 69literalpaths و 11sections → 335 قاموساً وكامل raw336 ثابتة؛ لا P7-164 ∣ RS14/SP3/HQ6/RW10/BK10 من B35 → 7B/7 جزئيتان؛ 7C لمتبدأو 8 غيرمأذونة، repair بدؤهوتزامنهمجهولان | not-executed |

## 4. ضوابط موجبة وسالبة وخطط قبول لم تنفذ

- T01–04 لترتيب الطلب والافتراضات والاتصال؛ T05–10 للمصدر ومرشح العملية ومجموعة الأنواع والحمولة.
- T11–16 لقبول Enter والفهرس غير الصالح و double-click/null؛ T17–20 لفصل Return والإغلاق الجديد.
- T21–28 لصحة اللقطة والحارس والعقد المحلي/SDK والسنة والفرع؛ T29–32 للسجل والأنساب والتسليم المستقل.

كلها **not-executed**، ومشروطة بإذن قبول منفصل ومدخلات اصطناعية منقحة. لا WPF/SQL/provider/SDK أو أعمال حقيقية هنا. نتائج النماذج ليست قبولاً تشغيلياً لهذه الخطط.

## 5. المصالحة والتوصيات

[RC6](evidence/report-reconciliation-07B36.csv) يحفظ unions الأدلة والـ FE والجذور وخطط القبول بدقة؛ [AD8](evidence/root-adjudication-07B36.csv) يحفظ سبب عدم إنشاء 164 وعدم إلحاق evidence؛ [السجل](findings.csv) دون تغيير. G261–264 توصيات لـ SearchRequest/DocumentRef ونشر نتيجة موحد وصحة لقطة وحصر عقود، لا إصلاحات منفذة.

حُفظت **1122 مادة دخول محمية من 1126 بايتياً**، وتشمل `findings.csv` نفسها: **كل 335 قاموساً بكل حقل وكامل raw336CRLF/222939 بايت، دون BOM**. لا تعديل evidence أو status أو severity أو certainty أو type أو next_phase أوالترميز ونهايات الأسطر. المسارات الأربعة المعلنة القابلة للتحديث وحدها: README/PLAN/IMPROVEMENTS و tools/validate_audit.py؛ بقية العمل ملفات B36 جديدة.

**G01–260 وصفوفها exact؛ G261–264 توصيات غير منفذة وليست أربع نتائج أخرى.** بقيت 827 أصل تطبيق/29,128,444 بايت كما هي. تشمل الحماية كل مواد B35: LN8/NR8/FE16/INV16/RC6/AD8/T32/RS14/SP3/HQ6/RW10/BK10/ext0 وشاهده وأخطاء بنائه وأرشيف 40 وبرهانه و stdout الرسمي وإيصاله وفحوصه؛ و B34 RQ8/AW8 و B33 OS8/OV8 و B32 EO8/DG8 وجميع الدفاتر الأقدم. أعداد B35 التاريخية 1071/1075 و B34 التاريخية 1018/1022 لا يستبدلها عدّ الحالي.

**P4-014 و P7-108 و P7-132 و P7-145 potential كما هي**؛ 020/021 وحواجز المال و ACL والمخزون والحفظ والإنتاج باقية. ذيل 159 في B30 وامتداد 046 في B28 محفوظان؛ 013 و 155/156/158/159/161 أسباب مستقلة بشروطها. تصحيح B10 الإضافي 10 محلياً/120 مرجعياً/equality1=10 باقٍ دون تحرير G138.

لم ينفذ ERP/build/C#/VB/.NET/WPF/ShowDialog/SQL/DataView/provider/SDK/REPX/ToDataTable أو طابعة/ماسح أو بيانات أعمال/أسرار أو حفظ أو حجز رقم أو إصلاح أو قياس أو قبول تشغيلي. الصفوف والفهارس و SelectedItem ورموز الاتصال ورجوع الحوار وحدود الفشل **مدخلات رمزية مورّدة لا آثار تشغيل مرصودة**. نعرف auto-properties لـ InvoiceSrchRow المحلية، ولا نعممها على InvoiceDGV أو SDK/constructors/collections/setters/alias/clone/enum أو اكتمال hydration.

**كل 32 خطة B36 وجميع الخطط التشغيلية السابقة، ومنها 32B35/B34/B33/B32/B31/B30/B29/B28 و 36B27، not-executed.** اختبارات Python التوثيقية ليست تنفيذ تلك الخطط أو نجاحاً للواجهة أو قاعدة البيانات أو إصلاحاً.

يبقى زر **Return** المنفصل وفحصه الخاص والسنة السابقة و chrome/إعادة فتح الحوار وكل caller آخر وأعمال editors/fields/writers/outputs ضمن **SP01 و 7B**. قراءة سياقها لا تعتمدها. تبقى DocumentRef/allowed-set/branch/reset/dirty/cancel/failure و Product/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome بعقودها المستقلة، ولا تُختزل إلى ISDone.

**SP02** لحصر القدرات entry/source/output و crosswalk455FE والدفاتر اللاحقة، و**SP03** لعقود SDK/DTO/constructors/collections/currency/precision/words/legacy/templates والسياسات، ضمن 7B صراحة. لا تنقل القدرات غير المقروءة إلى 7C ولا يفتتح هذا التتبع محور C3 العام.

التالي **R4u/7B37 أو split مسبب من SP7B36-01–03**: قدرة ومدخل ومصدر وحد مخرج واستبعاد ودليل ومالك ومدخل منقح وأثر غيابه وخطوة وخروج ساكن. لا وعد بمدة أو جلسات أو آخر جزء أو نسبة قدرات أو إتمام المنظومة. يسلم SHA تدقيق محدد إلى الإصلاح المستقل دون افتراض بدئه أو تزامنه أو دمج تعديلاته هنا.

## 6. تحقق وثائقي لا تنفيذ خطط القبول

اجتاز الفحص التمهيدي المستقل 1294/37، بما فيه 1242 حالة سابقة و 52 جديدة. أرشيف 41 ناتج عمليات OWN فعلية، لا fixtures. تبقى خطط القبول التشغيلية كلها not-executed؛ الهويات الدقيقة وحدود الالتقاط الرسمي اللاحق في[التحقق](VALIDATION-07B36.md).
