# عقود أوامر منتقي المناقلة —7B37/R4u

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**دخول B37:** تسليم B36 المدفوع `a83cb66108241ad51ab4f08fbff3fe5f361d58a0`؛ **1177 مادة تدقيق و 335 نتيجة مفتوحة** قبل إضافات الشريحة.
التاريخ المرجعي الحاكم لهذه المتابعة **2026-11-16 UTC**؛ ساعة البيئة الخام وقت التجميد `2026-11-20T23:13:01.594594+00:00` مسجلة حرفياً بتاريخها المختلف، وليست معايرة تقويم. لا يعاد تأريخ أثر مستهلك ولا يصادق نجاح assertions على التقويم. [فصل التاريخ والهويات](DATE-IDENTITY-NOTE-07B37.md).

**تدقيق ساكن فقط؛ لا تعديل للتطبيق أو إصلاح أو تشغيل ERP. R4u/7B37 شريحة محدودة؛ 7B والمرحلة 7 جزئيتان؛ 7C لم تبدأ؛ 8 غير مأذونة هنا.** الإصلاح مستقل وبدؤه وتزامنه غير معلومين؛ لا دمج repair→audit أو كتابة ملفاته أو إغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[الخلاصة](PHASE-07B37.md) · [عقود أوامر المناقلة](TRANSFER-PICKER-CONTRACTS-07B37.md) · [التحقق](VALIDATION-07B37.md) · [المتبقي وسلطة المتابعة](PHASE-07-REMAINING-07B37.md) · [الهوية](DATE-IDENTITY-NOTE-07B37.md) · [النطاق](review-scope-07B37.csv) · [قرار الاختيار](evidence/scope-decision-07B37.json) · [السجل دون تعديل](findings.csv) · [stdout الرسمي](evidence/checks-07B37.json)

## 1. عقود مستقلة لا تستبدل ببعضها

**هذه عقود مقترحة غير منفذة، وليست وصفاً لسلامة السلوك الحالي.** يبين المصدر الحالي أن شرط القبول يحكم Navigate وحده ولا يشمل أذيال التحويل الثلاثة.

1. **SearchRequest** يحدد الهدف المسموح لكل أمر؛ لا يضمن إسناد ProcType وحده جميع آثار permission/settings.
2. **AcceptedDocument** مستقل عن AbandonDecision وعن Copy/ReceiveIntent. المطلوب أن يمنع nonaccept كامل التحويل غير المصرح به، لا Navigate وحده.
3. **LoadOutcome** لا يستنتج من void أو null fallback/new؛ اللقطة المورّدة ليست عقد DTO أو دليلاً على اكتمال hydration.
4. **NumberOutcome** لا يستنتج من عودة helper ذي catch؛ يظل catch-return مختلفاً عن nonreturn.
5. **NumberScope** يعلن مصادر field/header/branch/type/year. اختلاف field1/header2 سؤال سياسة، لا عيب محسوم بمجرد مقارنة tokens.
6. **UI Publish** مستقل عن الوصول إلى تعليمة label/ISNew؛ لا نستنتج حالة نهائية بعد framework/SDK events دون عقد.

تسند [الخلاصة](PHASE-07B37.md) السلسلة والضوابط إلى المقاطع المحددة. تحمل [المصفوفة](evidence/feature-implementation-matrix-07B37.csv) لكل قدرة: المدخل والمصدر وحد المخرج والاستبعاد والمالك والمدخل المنقح وأثر غيابه والخطوة ومعيار الخروج.

## 2. crosswalk محدود— 16 قدرة و 32 خطة غير منفذة

| FE/INV | القدرة | نتيجة قائمة/عقد | خطتا القبول—not-executed | المالك |
|---|---|---|---|---|
| FE7B37-01 / INV7B37-01 | طلبات الأوامر الثلاثة والضابط ليست عقداً واحداً | H7B37-01 | P7B37T-01;P7B37T-02 | مالك المنتج وقصد أمر المناقلة |
| FE7B37-02 / INV7B37-02 | wiring والاستعمال المشترك لمعالج الطلب | P7-160 | P7B37T-03;P7B37T-04 | مالك أوامر WPF وحارس ترك المسودة |
| FE7B37-03 / INV7B37-03 | البحث العادي ضابط nonaccept دون ذيل تحويل | P7-160 | P7B37T-05;P7B37T-06 | مالك المنتج وقصد أمر المناقلة |
| FE7B37-04 / INV7B37-04 | استلام المناقلة بعد nonaccept | P7-160 | P7B37T-07;P7B37T-08 | مالك المنتج وقصد أمر المناقلة |
| FE7B37-05 / INV7B37-05 | إدراج طلب بضاعة بعد nonaccept | P7-160 | P7B37T-09;P7B37T-10 | مالك المنتج وقصد أمر المناقلة |
| FE7B37-06 / INV7B37-06 | إدراج مشتريات بعد nonaccept | P7-160 | P7B37T-11;P7B37T-12 | مالك المنتج وقصد أمر المناقلة |
| FE7B37-07 / INV7B37-07 | هوية الرأس والرقم حد ذاكرة لا حفظ | P7-160 | P7B37T-13;P7B37T-14 | مالك SDK/DTO والقارئ وحدود المراجع |
| FE7B37-08 / INV7B37-08 | Accepted لا يساوي AbandonDecision | P7-159 | P7B37T-15;P7B37T-16 | مالك أوامر WPF وحارس ترك المسودة |
| FE7B37-09 / INV7B37-09 | void Navigate وحد null/fallback | H7B37-02 | P7B37T-17;P7B37T-18 | مالك SDK/DTO والقارئ وحدود المراجع |
| FE7B37-10 / INV7B37-10 | مصادر طلب الترقيم وترتيب النشر | H7B37-04 | P7B37T-19;P7B37T-20 | DBA ومالك الهوية والترقيم والعملية |
| FE7B37-11 / INV7B37-11 | catch-return غير nonreturn في helper الترقيم | H7B37-05 | P7B37T-21;P7B37T-22 | مالك سياسة فشل الترقيم والنشر |
| FE7B37-12 / INV7B37-12 | field ProcType مقابل header ProcType بعد التسلسل | H7B37-04 | P7B37T-23;P7B37T-24 | DBA ومالك الهوية والترقيم والعملية |
| FE7B37-13 / INV7B37-13 | حد الأهلية والفرع عند الاستهلاك | P7-156;P7-157 | P7B37T-25;P7B37T-26 | DBA ومالك الهوية والترقيم والعملية |
| FE7B37-14 / INV7B37-14 | المدخلات الموردة لا تحل SDK أو ترتيب الإطار | H7B37-02 | P7B37T-27;P7B37T-28 | مالك SDK/DTO والقارئ وحدود المراجع |
| FE7B37-15 / INV7B37-15 | منع العد وحفظ السجل والأصول | H7B37-06 | P7B37T-29;P7B37T-30 | مالك نطاق التدقيق والأنساب والتسليم المستقل |
| FE7B37-16 / INV7B37-16 | الأنساب والمتبقي وتسليم SHA مستقل | H7B37-06 | P7B37T-31;P7B37T-32 | مالك نطاق التدقيق والأنساب والتسليم المستقل |

## 3. TR8/TT8—اتحاد أدلة وحدود مرتبة

### TR8 — من الأمر إلى الطلب

| المعرف | FE | الجذور/العقود | الحد الموثق | الحالة |
|---|---|---|---|---|
| TR7B37-01 | FE7B37-01;FE7B37-02 | H7B37-01;P7-160 | أزرار search/receive/order/purchase→new picker → حقول طلب ثم ShowDialog مطلوب لا رجوع مشاهد ∣ XAML→Receive/Order/Purchase والبحث العادي → لا root لكل زر أو event أو موضع XAML | not-executed |
| TR7B37-02 | FE7B37-03;FE7B37-04 | P7-160 | search ShowDialog→done/GID gate → رفض النتيجة لا يبلغ تحويل الأوامر الأخرى ∣ receive ShowDialog(return supplied)→if single Navigate → الذيل مستقل عن قبول الهدف عند الحد المحلي | not-executed |
| TR7B37-03 | FE7B37-05;FE7B37-06 | P7-160 | order ShowDialog(return supplied)→if Navigate → تحويل رأس قائم دون اعتماد نتيجة الاختيار ∣ purchase ShowDialog(return supplied)→if Navigate → نفس آلية 160 لا finding ثالثة للزر | not-executed |
| TR7B37-04 | FE7B37-07;FE7B37-08 | P7-160;P7-159 | nonaccept→conversion/number helper → نفس slot رمزي بلا Navigate لا يعني ثبات UI أو SDK aliases ∣ done/non-1→Navigate دون CheckBeforeClear → مقارنة 159 دون توسعة registry أو تعميم dirty | not-executed |
| TR7B37-05 | FE7B37-09 | H7B37-02 | Navigate→BindingInvoice(ref)→null check/new/return → الرجوع void لا يثبت Found أو Complete قبل ذيل التحويل | not-executed |
| TR7B37-06 | FE7B37-10;FE7B37-11 | H7B37-04;H7B37-05 | LoadInvoiceNumber→InvoiceNo(InvType,ProcType,Prefixe) → MAX+1/prefix قراءة لا حجز أو مصدر GlobalID ∣ number helper catch→ShowError ثم عودة void → لا تستعار حالة فشل LoadInvNo في B30 على helper مختلف | not-executed |
| TR7B37-07 | FE7B37-12;FE7B37-13 | H7B37-04;P7-156;P7-157 | receive nonaccept→field1 ثم order/purchase → اختلاف مصدر مثبت وسياسة غير محسومة لا finding جديدة ∣ receive ينقل InvoiceStatus1 في الطلب→gid/branch؛ order/purchase→gid فقط → لا اعتماد ACL أو allowed-set لكل متصل من شرط هوية | not-executed |
| TR7B37-08 | FE7B37-14;FE7B37-15;FE7B37-16 | H7B37-02;H7B37-06 | fresh picker false/-1 و modal return(header supplied) → 0 ملفات كاملة و 0 اكتمال قدرات؛ DTO المجهول ليس دليلاً على غياب الحماية ∣ metadata335/71literalpaths/8sections+2contracts → 335 قاموساً وكامل raw336 و 1173protected/G264/827 exact ∣ RS14/SP3/HQ6/RW10/BK10 من B36 → 7B/7 جزئيتان؛ R4v/B38 أو split مسبب؛ 7C لم تبدأ و 8 غير مأذونة | not-executed |

### TT8 — من الرجوع إلى الذيل وحد الفشل

| المعرف | FE | الجذور/العقود | الحد الموثق | الحالة |
|---|---|---|---|---|
| TT7B37-01 | FE7B37-01;FE7B37-02 | H7B37-01;P7-160 | أزرار search/receive/order/purchase→new picker → حقول طلب ثم ShowDialog مطلوب لا رجوع مشاهد ∣ XAML→Receive/Order/Purchase والبحث العادي → لا root لكل زر أو event أو موضع XAML | not-executed |
| TT7B37-02 | FE7B37-03;FE7B37-04;FE7B37-05 | P7-160 | search ShowDialog→done/GID gate → رفض النتيجة لا يبلغ تحويل الأوامر الأخرى ∣ receive ShowDialog(return supplied)→if single Navigate → الذيل مستقل عن قبول الهدف عند الحد المحلي ∣ order ShowDialog(return supplied)→if Navigate → تحويل رأس قائم دون اعتماد نتيجة الاختيار | not-executed |
| TT7B37-03 | FE7B37-06 | P7-160 | purchase ShowDialog(return supplied)→if Navigate → نفس آلية 160 لا finding ثالثة للزر | not-executed |
| TT7B37-04 | FE7B37-07 | P7-160 | nonaccept→conversion/number helper → نفس slot رمزي بلا Navigate لا يعني ثبات UI أو SDK aliases | not-executed |
| TT7B37-05 | FE7B37-08 | P7-159 | done/non-1→Navigate دون CheckBeforeClear → مقارنة 159 دون توسعة registry أو تعميم dirty | not-executed |
| TT7B37-06 | FE7B37-09;FE7B37-10 | H7B37-02;H7B37-04 | Navigate→BindingInvoice(ref)→null check/new/return → الرجوع void لا يثبت Found أو Complete قبل ذيل التحويل ∣ LoadInvoiceNumber→InvoiceNo(InvType,ProcType,Prefixe) → MAX+1/prefix قراءة لا حجز أو مصدر GlobalID | not-executed |
| TT7B37-07 | FE7B37-11;FE7B37-12;FE7B37-13 | H7B37-05;H7B37-04;P7-156;P7-157 | number helper catch→ShowError ثم عودة void → لا تستعار حالة فشل LoadInvNo في B30 على helper مختلف ∣ receive nonaccept→field1 ثم order/purchase → اختلاف مصدر مثبت وسياسة غير محسومة لا finding جديدة ∣ receive ينقل InvoiceStatus1 في الطلب→gid/branch؛ order/purchase→gid فقط → لا اعتماد ACL أو allowed-set لكل متصل من شرط هوية | not-executed |
| TT7B37-08 | FE7B37-14;FE7B37-15;FE7B37-16 | H7B37-02;H7B37-06 | fresh picker false/-1 و modal return(header supplied) → 0 ملفات كاملة و 0 اكتمال قدرات؛ DTO المجهول ليس دليلاً على غياب الحماية ∣ metadata335/71literalpaths/8sections+2contracts → 335 قاموساً وكامل raw336 و 1173protected/G264/827 exact ∣ RS14/SP3/HQ6/RW10/BK10 من B36 → 7B/7 جزئيتان؛ R4v/B38 أو split مسبب؛ 7C لم تبدأ و 8 غير مأذونة | not-executed |

## 4. خطط قبول لم تنفذ

T01–04 للطلب وwiring؛ T05–12 للبحث الضابط وأذيال nonaccept الثلاثة؛ T13–18 للهوية وقرار الترك وحد null/void؛ T19–24 لطلب الرقم وcatch-return وسياسة field/header؛ T25–28 للأهلية وSDK/الإطار؛ T29–32 للسجل والأنساب والتسليم المستقل. لكل خطة شروط وprocedure وacceptance_criterion وضوابط سلامة وحالة not-executed. ليست هذه 32 نموذج Python أو حصراً لقدرات 455FE، ولا ينفذها اجتياز 52 حالة وثائقية.

يصالح [RC6](evidence/report-reconciliation-07B37.csv) الأدلة والقدرات والجذور والخطط؛ ويوثق [AD8](evidence/root-adjudication-07B37.csv) عدم إنشاء 164 والتمييز بين 159 و160 والسياسة غير المحسومة. G265–268 توصيات بعقود typed وNumberOutcome/Scope وحصر الأنساب، وليست إصلاحات منفذة.

حُفظت **1173 مادة دخول محمية من 1177 بايتياً**، ومنها `findings.csv`: **كل 335 قاموساً بكل حقل وكامل raw336CRLF/222939 بايت، دون BOM**. لا تغيير evidence أو status أو severity أو certainty أو type أو next_phase أوالترميز ونهايات الأسطر. أربعة مسارات دخول معلنة قابلة للتحديث فقط: README/PLAN/IMPROVEMENTS و tools/validate_audit.py؛ بقية العمل ملفات B37 جديدة.

**G01–264 وصفوفها exact؛ G265–268 توصيات غير منفذة وليست أربع نتائج أخرى.** بقيت 827 أصل تطبيق/29,128,444 بايت كما هي. تشمل الحماية كل B36: PQ8/PR8/FE16/INV16/T32/RC6/AD8/RS14/SP3/HQ6/RW10/BK10/ext0 وشاهده وفشل codec التاريخي وأرشيف 41 وبرهانه و stdout الرسمي وإيصاله، وكل LN8/NR8B35 و RQ8/AW8B34 و OS8/OV8B33 و EO8/DG8B32 والدفاتر الأقدم. الأعداد التاريخية 1122/1126 في B36 و 1071/1075 في B35 لا يعاد وسمها بأنها أعداد B37.

تبقى **P4-014 و P7-108 و P7-132 و P7-145 potential**؛ 020/021 وحواجز المال و ACL والمخزون والحفظ والإنتاج باقية. امتداد 046B28 وذيل 159B30 محميان. 155/156/157 و P4-019 و P3-005 أسباب مستقلة لا يعاد عدها. تصحيح B10 الإضافي 10 محلياً/120 مرجعياً/equality1=10 باقٍ دون تحرير G138.

لم ينفذ ERP/build/C#/VB/.NET/WPF/ShowDialog/SQL/DataView/provider/SDK/REPX/ToDataTable أو طابعة/ماسح أو بيانات أعمال/أسرار أو حفظ أو حجز رقم أو إصلاح أو قياس أو قبول تشغيلي. الرجوع الطبيعي ولقطات الرأس/الحقول والأعلام ونتيجة Navigate والرقم ونجاح setters وحدود الفشل **مدخلات مورّدة لا آثار تشغيل مرصودة**. رموز slot ليست برهان CLR alias أو clone؛ لا نعتمد DTO defaults أو enum mapping أو اكتمال hydration أو ثبات UI/الأعلام بعد notifications.

**كل 32 خطة B37 وجميع الخطط التشغيلية السابقة، ومنها 32B36/B35/B34/B33/B32/B31/B30/B29/B28 و 36B27، not-executed.** اختبارات Python الوثائقية ليست تنفيذ تلك الخطط أو نجاحاً للواجهة أو SQL أو إصلاحاً.

تبقى بقية أوامر المحرر والمتصلين والحقول والكتّاب والمخارج و DocumentRef/allowed-set/branch/reset/dirty/cancel/failure و Product/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome داخل **SP01 و 7B**. لا يعتمد هذا التتبع زر Return المنفصل أو السنة السابقة أو chrome/إعادةفتح/Loaded أو كل lookup/query أو كود save/stock. مقارنة طلب field1 برأس 2 سؤال سياسة لا ترقية يقين أو نتيجة مالية تلقائية.

**SP02** للحصر entry/source/output و crosswalk455FE والدفاتر اللاحقة؛ **SP03** لـ SDK/DTO/constructors/setters/collections/currency/precision/words/legacy/templates والسياسات. لا تنقل القدرات غير المقروءة إلى 7C ولا يبدأ محور C3 العام من شريحة WPF محلية.

التالي **R4v/7B38 أو split مسبب من SP7B37-01–03** بقدرة ومدخل ومصدر وحد مخرج واستبعاد ودليل ومالك ومدخل منقح وأثر غيابه وخطوة وخروج ساكن. لا وعد بمدة أو جلسات أو آخر جزء أو نسبة قدرات أو إتمام المنظومة. يسلم SHA تدقيق مدفوع محدد إلى الإصلاح المستقل دون افتراض بدئه أو تزامنه أو دمج تعديلاته هنا.

## 5. تحقق وثائقي لا تنفيذ خطط القبول

اجتاز الفحص التمهيدي المستقل 1346/38، بما فيه 1294 حالة سابقة و 52 جديدة؛ أرشيف 42 ناتج عمليات OWN فعلية لا fixtures. تبقى الخطط التشغيلية كلها not-executed؛ الهويات وحدود الالتقاط الرسمي اللاحق في[التحقق](VALIDATION-07B37.md).
