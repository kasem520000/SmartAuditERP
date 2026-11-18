# التحقق وخطط القبول — المرحلة7، الجزء7A

**مرجع التدقيق:** 2026-11-16 (UTC) — **الفرع:** `arena/94ae8414-smartauditerp`  
**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`.

**هذا تسليم الجزء7A فقط، ضمن إذن المستخدم «ابدأ المرحلة 7». المرحلة7 غير مكتملة:7B للتقارير والطباعة و7C لبقية الواجهات/المسارات والأداء لم يبدآ. لا إذن أو بدء للمرحلة8، ولا إصلاحات أوbuild أوتشغيل التطبيق/WPF/SQL/COM/SDK أو جهاز/مزود. كل قبول تطبيقي هنا غير منفذ.**

حُفظ تاريخ المرجع المعلن16 نوفمبر؛ ملاحظة ساعة بيئة التوثيق17 نوفمبر منفصلة في provenance07، لا كتاريخ اختبار ERP أو تصحيح لتواريخ المراحل التاريخية. لا مصادر ويب جديدة في7A ولا طلبات تشغيلية أو أسرار/بيانات موظفين حقيقية.

[نتائج7A](PHASE-07.md) · [مصفوفة الميزات والنموذج](FEATURES-HR-PROJECTS-07.md) · [التحقق وخطط القبول](VALIDATION-07.md) · [السجل](findings.csv) · [الفهرس](README.md) · [الخطة](PLAN.md) · [التحسينات](IMPROVEMENTS.md).

## 1. المنفذ فعلاً مقابل المخطط فقط

نفذت قراءة مصادر/نصوص ومقارنة عقود وDDL مرفق، وحصر/بصمات وتوليد توثيق وفحوص Python/Git محلية. **لم يشغل ERP أو C# أوWPF أوSQL أوCOM/SDK/native binaries أوطابعة/جهاز/مزود، ولم تنفذ معالجة أو اختبارات قبول التطبيق.** أمثلة Python مستقلة منقولة يدوياً لا تحمل DTO أوتشغل methods المشروع ولا تعيد تنفيذ كل دلالات.NET/الثقافات.

| الفحص/الأثر | العدد والمعنى والحد |
|---|---|
| تحقق الدخول حتى6 |172 نتيجة و827 بصمة أصلية وerrors[] قبل تأليف7A؛ checks06 التاريخية لم تستبدل. |
| لقطة الدخول/provenance07 |SHA256 للـ172صفاً: `1916bebebcb9d6af3e6bff94719c0269f44fb0e120c07c2bd3c316fd9ac07597`؛67 artifact تاريخياً محفوظة ببصماتها. |
| collect_baseline.py --verify |827 ملف تطبيق أصلياً لم تتغير؛ لا baseline جديد ولا إصدار تطبيق جديد. |
| check_feature_witnesses.py |12 توضيحاً مستقلاً و8 فحوص معجمية بأرقام/هويات وهمية؛ لا device/SQL أوtypes/CLR فعلي. |
| test_audit_validator.py |10 اختبارات لوظائف **مدقق الوثائق نفسه** نجحت على قواميس/نطاقات اصطناعية: حفظ متابعات7 الجزئية ورفض تغيير النواة/الدليل أوادعاء قبول منفذ أوعلاقة/نطاق غير صالح؛ ليست اختبارات SmartAuditERP ولا تغلق نتيجة. |
| validate_audit.py الافتراضي7 |يرجع `phase_7_delivery=7A-partial` صراحة؛200 نتيجة مفتوحة، scope47/union266 وledger827، matrix36/commands16/invariants25/tests64/backlog10؛ ليس اكتمال7. |
| --through-phase 6 |يقرأ **لقطة172 المجمدة** وتقارير6، لا السجل200 الحالي أو shared docs كبديل تاريخي؛ الآثار53 قبل6 و67 عند دخول7 تتحقق دون إعادة كتابة. |
| --through-phase 2 / 3 / 4 / 5 |لقطات49/74/106/137 وتقارير/نطاقات التاريخ منفصلة؛ نجاح هذه الأداة لا يساوي تطابق JSON القديم حرفياً أو إعادة تنفيذ التطبيق. |

المخرج التفصيلي [checks-07.json](evidence/checks-07.json) يقيس اتساق هوية/روابط/مقاطع/بصمات وربطاً عكسياً فقط، بما في ذلك حصر كل827 وحفظ نواة172 وnext_phase لها. تكرار الإحالات ليس قراءات فريدة، وملفchecks لا يبصم نفسه. لا يثبت هذا الفحص المعنى المحاسبي أوschema مثبتاً أوسلوكCOM/WPF/ضابطاً خارجياً.

## 2. توضيحات مستقلة وفحوص نصية منفصلة

[feature-witnesses-07.json](evidence/feature-witnesses-07.json) يحفظ المدخلات/المخرجات والافتراض والحد والدليل؛ السجل ليس سجل اختبارات ناجحة للمنتج. لا قيمة حقيقية لموظف أو راتب أو بصمة أو ملف، ولا packet/device أوحقن SQL أو تعديل قاعدة أو ساعة.

| المعرف | التوضيح المستقل | النتائج | الحد |
|---|---|---|---|
| ALG7-01 | Typed row mismatch can take the null-entry success branch | P7-001 | Symbolic type/branch model only, not .NET casting, exception, WPF or SQL execution; persistence is conditional on schema and preceding writes. |
| ALG7-02 | Reload omission preserves the default employee identifier | P7-003 | Dictionary/default illustration, not DTO setters, a deployed employee0/FK, a selected WPF row, payroll SQL or production corruption. |
| ALG7-03 | Editable components disagree with a stale saved net | P7-006 | Exact Decimal fixtures, not C# culture/binary arithmetic, WPF events, SQL writes or an actual financial payment. |
| ALG7-04 | Clearing fields is not resetting edit identity | P7-007، P7-023 | Sequential editor-state transcription only; no concurrent SQL, actual MAX allocation, WPF button presses or overwrite performed. Explicit Booking New is a counterexample that resets Code. |
| ALG7-05 | Business number used as primary key targets a different head | P7-010 | Two stipulated distinct keys, not deployed numbering/constraints/triggers or a SQL update. Equality in a small database can mask this mismatch. |
| ALG7-06 | Re-saving two terms can append two more projects | P7-011 | List model conditional on reaching Commit and a compatible schema; P7-014 can block actual inserts. Not evidence of duplicated projects in a deployment. |
| ALG7-07 | Reloaded term net and saved header tax do not match components | P7-012، P7-013 | Exact Decimal counterexample with a VAT amount, not a legal tax-rate decision, .NET calculation/property setters, SQL, a report or compliance certification. |
| ALG7-08 | One status code has conflicting semantic consumers | P7-015 | Seed/consumer symbol model, not the deployed PM_Status lookup, a project transition, closed-state UI rendering or a migration test. |
| ALG7-09 | Empty loops pass while a seventh configured stage is not displayed | P7-016، P7-017 | Python loop/list illustration, not WPF layout or actual stage approval. Sequential versus parallel business policy and valid empty project types require an explicit contract. |
| ALG7-10 | Commit followed by failed clear requires ingestion idempotency | P7-009 | Conditional list schedule only; no device/COM or SQL. SDK replay semantics, external triggers and a reliable event identity remain unresolved. Commit precedes clear; no pre-commit erasure claim. |
| ALG7-11 | An active-row display count is not the inserted booking identity | P7-022 | Stipulated identity-gap example only, not SQL identity allocation or proof of orphan/foreign booking rows; no missing stored-procedure return contract assumed. |
| ALG7-12 | Day-wide exit update rewrites previously recorded entry modes | P7-026 | List/predicate illustration, not Attendance SQL or payroll attendance. The inspected consumer is marine; no employee identity relationship is inferred. |

| المعرف | فحص نصي لا اختبار تطبيق | النتائج | الحد |
|---|---|---|---|
| ST7-01 | Accrual row tags, cast and nullable entry guard in selected text | P7-001 | Bounded literal presence, not type checking, .NET exception or transaction execution. Semantic trace and limitations are in the report. |
| ST7-02 | Both selected reload initializers omit Emp | P7-003 | Absence only in the two declared initializer slices, not a global data-flow proof or evaluation of external DTO/default/FK behavior. |
| ST7-03 | SalaryPay writer uses the field without a local financial writer call | P7-004 | Local selected-method text only. Does not rule out database triggers or services outside the repository, and makes no collateral-deletion claim about ReceiptOper. |
| ST7-04 | Salary component event declarations have different recalc wiring | P7-006 | Selected XAML declaration check only, not a WPF event/style/rendering test or a global binding analysis; the full local code-behind was separately reviewed. |
| ST7-05 | Contract primary-id parameter and forced zero tax in selected text | P7-010، P7-012 | Literal selected C#/SQL strings, not a SQL parser, data update, deployed schema or tax certification. |
| ST7-06 | Supplied requirement-detail DDL differs from selected readers | P7-021 | Bounded embedded-DDL/text-name extraction only, not SQL parsing or proof that a deployed schema lacks a later external migration/trigger. |
| ST7-07 | Hold entry-detail caller omits a required shared SQL parameter | P4-020، P4-025 | Parameter-name set difference only. Not SQL execution or an assessment of every type/length/path. False success is the existing P4-025 root, not a new phase7 finding. |
| ST7-08 | Biometric text keeps commit before clear but re-enable before finally | P7-008، P7-009 | Textual order/absence only; SDK Boolean semantics, actual disabling/replay/normal exhaustion, exceptions and device recovery are untested. Closing SQL ordinarily rolls back uncommitted work. |

تفصيل الحدود: DataRow مجرد فحص عقد رمزي لا InvalidCastException منفذ؛ فقدEmp نموذج default لا FK إنتاج؛ الحساب Decimal دقيق لا C#binary/الثقافة؛ تعداد المجموعة لا يجرب Enumerator في.NET؛ replay مفترض لا عقد جهاز؛ matched keys نموذج لهويتين مختلفتين لا SQLUPDATE. فحص required/supplied أسماء فقط لا parsing/types/SP runtime. **Commit قبل ClearGLog باقٍ كدليل مقابل** وليس فحصاً فاشلاً.

## 3. حواجز القبول —64 خطة غير منفذة

1. **مصدر/عقد:** Windows/.NET واعتماديات مرخصة معلومة الأصل وتعريف DTO/schema/SP/SDK/COM/firmware/سياسة، ومرجع محاسب/HR/PM للحساب والهوية والانتقال؛ نقصه يحجب القبول المعتمد عليه لا يعدpass.
2. **اختبار معزول لاحق:** إذن تشغيل واضح ونسخة schema/fixtures اصطناعية وfakes معلنة وحجب sync/رسائل/دفع/شبكة إنتاج وsnapshot/restore وعمليات faults/حجم/تزامن مضبوطة. وجود خطة أوfake ناجح لا يضمن مزوداً أوجهازاً حقيقياً.
3. **الحواجز السابقة:** لا تصل سيناريوهات PM اللاحقة إلى Commit على مخطط غير متوافق. يستعمل double موثق أو مرشح إصلاح مأذون فقط؛ لا تعديل إنتاج/تمكينBULK أوتجاوز حماية جهاز لتجربة النتيجة.
4. **الجهاز والمال والخصوصية:** لا ClearGLog/EnableDevice(false) أوحذف بصمات حي، لا تحويل مصرفي ولاPAN/بيانات شخصية/ملفات مستخدمين. الاختبار الفعلي يحتاج جهازاً مخصصاً وعقد الحد وهوية الحدث وإذن8 مستقلاً عند بلوغه.
5. **الإغلاق:** لا نتيجة `pass` أوتغيير `open-not-remediated` دون معالجة مأذونة ودليل قبول وفشل وتعافٍ ومصالحة مرجعية مناسبة. الجزء7A لم ينفذ ذلك ولا ينفذ8 ضمن إذن7.

[acceptance-tests-07.csv](evidence/acceptance-tests-07.csv) هو المرجع الكامل لكلscenario/prerequisites/procedure/acceptance_criterion/safety_controls/evidence وروابطFE/INV/finding.56 خطة مرتبطة مباشرة بالنتائج28 و8 للأصول/العقود المشتركة؛ ليست64 اختباراً نفذ أو64 نتيجة جديدة. القبول المستقبلي يمكن تفصيله أكثر دون محو ما كانnot-executed هنا.

| المعرف | السيناريو | الميزات / الثوابت | معيار القبول | الحالة |
|---|---|---|---|---|
| P7T-01 | حفظ استحقاق موظفين من المصدر Typed الفعلي | FE7-04 / INV7-02، INV7-04 | لا تحويل خاطئ ولا null مقبول؛ استحقاق واحد بتفصيلين وقيد واحد متوازن مطابق لهما، ولا يظهر نجاح إلا بعد اعتماد الجميع. | not-executed |
| P7T-02 | إخفاق الرابط أو الصف الثاني لا يترك استحقاقاً جزئياً | FE7-04 / INV7-02، INV7-04 | يرفض الاعتماد كله قبل أي أثر دائم أو يرجع الجميع في المعاملة؛ لا حوار Saved ولا سجل نصف مكتمل؛ سبب الفشل محدد. | not-executed |
| P7T-03 | فتح الاستحقاق من التقرير في دورة Loaded الحقيقية | FE7-05 / INV7-03 | الهويات والفترة محفوظة، ItemsSource من النموذج نفسه الذي يستهلكه الحفظ، وعدد الصفوف المحددة/المحفوظة مطابق بلا مسح صامت. | not-executed |
| P7T-04 | تحديد الكل وطباعة/عرض القيد بعد فتح التقرير | FE7-05 / INV7-03 | يعمل IsSelected على كل صف، لا إنشاء جديد ولا فقدان EntryGlobalID ولا تفاصيل خارج المعروض؛ لا يشترط نجاح طابعة حقيقية في هذا السيناريو. | not-executed |
| P7T-05 | فتح استحقاق من عارض القيود وإعادة الحفظ | FE7-06 / INV7-01، INV7-03، INV7-05 | تحفظ كل هوية موظف كما كانت، ولا تنشأ تفاصيل للموظف0؛ بيانات الطباعة البنكية تخص الموظف نفسه. | not-executed |
| P7T-06 | ممانعة موظف غير موجود أو فشل استعلام تاريخ التعيين | FE7-06 / INV7-01، INV7-03، INV7-05 | فشل آمن مع رسالة قابلة للتشخيص، لا موافقة افتراضية ولا كتابة راتب/قيد لهوية غير صالحة. | not-executed |
| P7T-07 | صرف راتب نقدي ثم بنكي مع أثر مالي قابل للمصالحة | FE7-07 / INV7-04، INV7-07، INV7-13 | كل صرف معتمد له هوية سند وقيد غير-1 فريدان ومتوازنان وتسوية بالمبلغ نفسه، ويطابق البنك/الصندوق المختار بلا تنفيذ تحويل مصرفي حي. | not-executed |
| P7T-08 | فتح صرف سابق ثم جديد وفشل الترحيل | FE7-07 / INV7-04، INV7-07، INV7-13 | لا يرث الجديد هوية السابق، ولا يصبح Paid عند فشل القيد، والحذف لا يفترض سنداً غير منشأ ولا يؤثر في سجل آخر. | not-executed |
| P7T-09 | استحقاق محذوف لا يصلح أصلاً للصرف | FE7-08 / INV7-05، INV7-25 | يرفض المحذوف؛ عند وجود النشط يختاره بهوية واضحة ولا يقرأ تفاصيل الملغى أو يقبلها كرصيد. | not-executed |
| P7T-10 | استحقاقات متعددة وفروع مختلفة للفترة نفسها | FE7-08 / INV7-05، INV7-25 | لا Rows[0] صامت ولا صرف فوق الرصيد؛ يطلب اختياراً/يفرض uniqueness أو سياسة الأقساط، ويقيد الفرع المأذون. | not-executed |
| P7T-11 | تعديل الحافز وحده ثم الحفظ | FE7-09 / INV7-06 | الجميع120 بالمقياس والعملة المعتمدين، ولا يحفظ salary_net=100 مع salary_add=20. | not-executed |
| P7T-12 | تعديل الخصم وحده وتطبيع الثقافات | FE7-09 / INV7-06 | الصافي85 في الحالة الصحيحة، والقيم غير الصالحة ترفض صراحة، وتظل المكونات/الصافي متطابقة دون اعتماد تنسيق N2 كمصدر SQL. | not-executed |
| P7T-13 | إدخال إضافة ثم أخرى في النموذج المفرغ بعد النجاح | FE7-10 / INV7-07، INV7-10 | ينشأ سجلB بهوية جديدة ولا يعدل سجلA؛ الحالة بعد ClearForm لا تصبح آخرMAX. | not-executed |
| P7T-14 | نافذتان تضيفان إجراء موظف بين الحفظين | FE7-10 / INV7-07، INV7-10 | لا تستهدف A سجلB بسبب SELECT MAX(id)، والهوية الناتجة من كل INSERT تخص طلبه فقط. | not-executed |
| P7T-15 | فشل SQL بعد تعطيل جهاز البصمة | FE7-12 / INV7-08 | محاولة تمكين واحدة على الأقل في finally حتى عند الفشل، وتمييز نجاح الاستعادة/فشلها للمشغل دون بلع صامت. | not-executed |
| P7T-16 | فشل إعادة التمكين أو تهيئة الاتصال | FE7-12 / INV7-08 | خطأ مضبوط لا يقتل UI أو يخفي حالة الجهاز، ولا نجاح كاذب؛ تقفل الموارد ولا يجرب تعطيلاً جديداً غير محمي. | not-executed |
| P7T-17 | اعتماد SQL ثم ClearGLog=false وإعادة الدفعة | FE7-12 / INV7-09، INV7-24 | عدد أحداث الأصل لا يزيد في الإعادة ويظل الإقرار قابلاً للتعافي؛ نفس المفتاح لا يكرر حضوراً/رحلة. | not-executed |
| P7T-18 | نافذة توقف بعد Commit وقبل المسح | FE7-12 / INV7-09، INV7-24 | لا تكرار للقديم ولا إسقاط لحدث مختلف يشترك في الدقيقة؛ لا تعتمد dedup بدقة زمن غير كافية دون عقد جهاز. | not-executed |
| P7T-19 | اختلاف رقم العقد التجاري عن المفتاح الأساسي | FE7-16 / INV7-10، INV7-11 | يتغير رأس10 وتفاصيل عقد77 وحدهما بعد توحيد الهوية؛ لا نجاح عند rowcount=0 ولا لمس رأس77 الآخر. | not-executed |
| P7T-20 | أرقام عقود متشابهة بين الفروع وأنواع المستندات | FE7-16 / INV7-10، INV7-11 | هوية المستهدف واحدة وثابتة، واكتشاف الغموض/الصلاحية يسبق التعديل ولا يعتمد الرقم التجاري وحده. | not-executed |
| P7T-21 | إعادة حفظ عقد دون تغيير لا تولد مشروعات | FE7-17 / INV7-11 | يبقى عدد المشروعات وهوياتها وعلاقاتها ثابتاً، بلا نسخ جديدة أو انفصال عن المراحل. | not-executed |
| P7T-22 | إضافة وحذف بند عقد بعد بدء التنفيذ | FE7-17 / INV7-11 | إضافة مقصودة واحدة، تعديل يحفظ ProjectId، ورفض/إجراء إلغاء واضح للبند المستخدم مع سجل تدقيق وعدم حذف تاريخه. | not-executed |
| P7T-23 | مطابقة ضريبة الرأس والبنود والقيد | FE7-18 / INV7-06، INV7-12 | ضريبة الرأس30 ومجموع البنود30 وسطر الضريبة30 والصافي330 وفق السياسة المختارة؛ لا VATval=0 مع ضريبة موجبة. | not-executed |
| P7T-24 | ضريبة صفرية وحواف تقريب في عقد متعدد البنود | FE7-18 / INV7-06، INV7-12 | الصفر مشروع فقط وفق الحالة الضريبية، وفروق التقريب ضمن سياسة معلنة واحدة؛ لا اختراع نسبة أو اعتماد امتثال من هذا الاختبار. | not-executed |
| P7T-25 | دورة فتح بند بكميته الأصلية | FE7-19 / INV7-06، INV7-11، INV7-12 | Total=1000 وNetValue=1150، ولا يتغير صافي البند إلى250 بمجرد الفتح. | not-executed |
| P7T-26 | حفظ عقد مفتوح دون تصفير التكلفة | FE7-19 / INV7-06، INV7-11، INV7-12 | التكلفة لا تصبح0 افتراضياً ولا يعاد تسعيرها من حالة غير موثقة؛ إما round-trip محفوظ أو فشل صريح لنقص المصدر. | not-executed |
| P7T-27 | توافق قيد العقد/الإسناد/قبض PM مع مخطط الإنشاء | FE7-20، FE7-29 / INV7-13 | كل INSERT يزود GlobalID/EntryGlobalID، ولا يستعمل جدولاً أزيل اسمه؛ لا مستند يعتمد منفصلاً عن القيد المتوافق. | not-executed |
| P7T-28 | ترحيل مخطط قديم وإعادة مطابقة القيد | FE7-20، FE7-29 / INV7-13 | عقد مخطط واحد موثق بالإصدار، لا synonym/default غير مسجل يعتمد عليه القبول، والروابط والتوازن والتاريخ محفوظة. | not-executed |
| P7T-29 | تعميد مشروع ثم إرفاق ملف وهو تحت التنفيذ | FE7-21 / INV7-14، INV7-19 | تسمح الحالة تحت التنفيذ بالعمل المأذون ولا تفسر3 على أنه مغلق؛ الألوان والحراسة والتسمية تتفق مع الرمز. | not-executed |
| P7T-30 | إغلاق مشروع وعقد لا يزال أحد مشروعاته تحت التنفيذ | FE7-21 / INV7-14، INV7-19 | يحفظ إغلاقاً دلالياً مميزاً عن التنفيذ، ويرفض إغلاق العقد مع مشروع غير مغلق، ولا يستعمل status<3 كبديل غير صالح. | not-executed |
| P7T-31 | اعتماد مرحلة لاحقة مع السابقة غير مستوفاة | FE7-22 / INV7-15، INV7-19 | حارس السير يراجع المراحل السابقة المطلوبة فعلاً ويرفض تخطيها إن كانت السياسة تسلسلية؛ إن كانت متوازية يعكس القرار/الرسالة تلك السياسة صراحة. | not-executed |
| P7T-32 | إغلاق مشروع بلا مراحل أو بعد خطأ تحميلها | FE7-22 / INV7-15، INV7-19 | لا يعتبر غياب البيانات نجاحاً؛ لا يغلق إلا بعد تطابق الخطة المطلوبة وكل الاعتمادات، مع تشخيص فشل التحميل. | not-executed |
| P7T-33 | مجموعة ذات سبع مراحل | FE7-23 / INV7-15، INV7-16 | كل مرحلة محفوظة قابلة للوصول والعمل، أو يمنع الإدخال بحد أعمال صريح قبل حفظ خطة غير قابلة للعرض. | not-executed |
| P7T-34 | تغير عدد وترتيب المراحل بعد التحميل | FE7-23 / INV7-15، INV7-16 | لا اقتطاع صامت ولا اعتماد مرحلة بهوية زر آخر، وسياسة الخطة/الإغلاق متسقة مع العدد المحفوظ. | not-executed |
| P7T-35 | فشل في منتصف استبدال قالب المراحل | FE7-24 / INV7-17 | يبقى القالب القديم كله أو يعتمد الجديد كله، ولا DELETE مع نصف قائمة بعد الخطأ. | not-executed |
| P7T-36 | تعديلان متزامنان لقالب واحد | FE7-24 / INV7-17 | تعارض إصدار صريح أو ترتيب متسق كامل؛ لا lost update صامت، وخطة المشروع المأخوذة لها إصدار معروف. | not-executed |
| P7T-37 | رفع ملف مع SQL على جهاز آخر | FE7-25 / INV7-18، INV7-25 | تنتقل bytes المختارة نفسها عبر عقد رفع محدود، لا يحتاج OPENROWSET إلى وجود المسار المحلي على الخادم. | not-executed |
| P7T-38 | ملف كبير أو نوع غير مطابق ومسار ذو اقتباس | FE7-25 / INV7-18، INV7-25 | رفض النوع/الحجم غير المسموح، ولا يدمج المسار في SQL أو ينفذ وصول ملفات خادم؛ أسماء الملفات لا تحدد صلاحية الوصول. | not-executed |
| P7T-39 | ضغط تعميد مرتين مع إبقاء المحرر | FE7-27 / INV7-19، INV7-13 | اعتماد واحد وقيد واحد؛ الطلب الثاني يعيد النتيجة نفسها أو تعارض حالة واضح، ولا يعتمد على تحديث بصري للزر فقط. | not-executed |
| P7T-40 | نافذتان بحالة قديمة تعمدان المشروع نفسه | FE7-27 / INV7-19، INV7-13 | فائز واحد بانتقال CAS ومفتاح حدث فريد؛ إعادة الطلب بعد غموض الرد لا تولد قيداً جديداً. | not-executed |
| P7T-41 | طلب احتياج متعدد البنود على DDL المستودع | FE7-15 / INV7-20 | بعد الترحيل المعتمد يوجد مفتاح بند مستقل وعمود/سياسة حذف مطابقة لكل الاستعلامات، ويحفظ البندان ويقرآن بلا فقد. | not-executed |
| P7T-42 | تحويل طلب الاحتياج إلى عقد وإعادة الفتح | FE7-15 / INV7-20 | يسترجع كل بند مرة واحدة، ولا يفشل IsDeleted ولا يختفي التعديل خلف Saved بلا UPDATE؛ يميز نقص تنفيذ P1-033 عن مشكلة DDL. | not-executed |
| P7T-43 | فجوة Bid لا تغير ملكية إضافات الحجز | FE7-30 / INV7-21، INV7-07 | تفصيل الإضافة يحمل Bid الفعلي من OUTPUT، لا عدد الصفوف+1، ويظهر مع الحجز الصحيح فقط. | not-executed |
| P7T-44 | إنشاء حجزين بالتوازي وتحقق علاقة الإضافات | FE7-30 / INV7-21، INV7-07 | لا مشاركة/يتيمة/انتقال إضافات بين الحجزين؛ الأرقام المرئية مستقلة عن مفتاح القاعدة وهوية فاتورة التأجير. | not-executed |
| P7T-45 | إدخال حجز بعد تعديل سابق في الشاشة المفرغة | FE7-31 / INV7-07، INV7-21 | إما يبقى سجل7 واضحاً بوضع Edit أو تنتقل الشاشة إلى New بهوية فارغة؛ لا UPDATE7 مفاجئ لبيانات الحجز الجديد. | not-executed |
| P7T-46 | الزر جديد مقابل التفريغ التلقائي بعد إنشاء | FE7-31 / INV7-07، INV7-21 | كلا المسارين متسقان بلا أرقام سابقة أو تحديث عرضي؛ يسجل أن زر جديد الحالي Counterexample يعيد Code ولا يعمم فشله. | not-executed |
| P7T-47 | حجزان متداخلان للمركب نفسه | FE7-32 / INV7-22، INV7-25 | يرفض واحد من المتداخلين بنتيجة تعارض، ويسمح المتجاورين وفق حد الفترة [start,end)، ولا ينفي حارساً خارجياً قبل فحصه. | not-executed |
| P7T-48 | إلغاء الحجز وتغيير مدته وسياق الفرع | FE7-32 / INV7-22، INV7-25 | تطبق سياسة المدة والحالات والإتاحة الذرية نفسها في create/update/cancel، ولا ترخص الدقائق إلى ساعات صحيحة أو تتجاوز الفرع. | not-executed |
| P7T-49 | بحث اسم يطابق صفاً مع إعادة تعبئة النتائج | FE7-33 / INV7-23 | لا تعديل للمجموعة داخل Enumerator ولا InvalidOperationException، وينفذ البحث النهائي مرة واحدة بالمرشحات المتفق عليها. | not-executed |
| P7T-50 | بحث هاتف مع أكثر من صف مطابق وبدون مطابقة | FE7-33 / INV7-23 | نتيجة حتمية بلا exception أو تجاهل صامت للفترة/المرشح، ولا إعادة بحث لكل صف يؤدي إلى مسح التعداد. | not-executed |
| P7T-51 | خروج مركب له أكثر من حدث دخول/خروج في اليوم | FE7-13 / INV7-24، INV7-09 | لا تتغير أحداث الأصل؛ يسجل حدث خروج/تصحيح مستقل بمستخدم وسبب، وحالة المركب مشتقة دون مسح تسلسله. | not-executed |
| P7T-52 | ربط فاتورة برحلة واحدة دون تعديل كل اليوم | FE7-13 / INV7-24، INV7-09 | ارتباط محدد بالرحلة/الحدث لا تحديث كل اليوم، ولا تكرار قيد أو تغيير حدث قديم عند إعادة الطلب. | not-executed |
| P7T-53 | جديد/فتح موظف بعد LoadBranches | FE7-01 / INV7-01، INV7-03، INV7-23 | تعدل القائمة المرتبطة وحدها دون Items.Clear/Add غير قانونيين، وتحمل الحقول والفروع بالكامل في كل دورة. | not-executed |
| P7T-54 | إعادة تهيئة واجهة الموظف بعد حفظ ناجح | FE7-01 / INV7-01، INV7-03، INV7-23 | لا فشل تهيئة بعد كتابة ناجحة ولا رسالة نجاح/فشل مضللة، ومصدر فروع واحد يتفق مع القائمة المعروضة. | not-executed |
| P7T-55 | حفظ ملف موظف ببدلات وحقول غير صفرية | FE7-01 / INV7-01، INV7-06 | تحفظ القيم غير المعدلة كما هي ولا تستبدل بثوابت0/-1/NULL، ويطابق إجمالي الشاشة المخزن. | not-executed |
| P7T-56 | تعديل مقصود مقابل حقول غير متاحة في DTO | FE7-01 / INV7-01، INV7-06 | لا فقد صامت لقيمة لم يدعمها النقل؛ رفض واضح أو خريطة كاملة، ولا حذف صورة/ملاحظة ضمن حفظ غير متعلق بها. | not-executed |
| P7T-57 | عقود SQL ذات النصوص الحرة وحدود المبلغ المالي | FE7-10 / INV7-06، INV7-13، INV7-25 | كل مدخل بيانات يمر بمعامل Typed؛ لا حفظ لقيد فارغ أو مبلغ غير صالح، ولا أخطاء syntax بسبب بيانات المستخدم؛ ليس اختبار استغلال. | not-executed |
| P7T-58 | تفويض حفظ/طباعة الرواتب وPM وعزل الفروع عبر كل المدخلات | FE7-08، FE7-14، FE7-16 / INV7-25، INV7-10 | تحقق تفويض فعلي في حد الخدمة/المستودع والفرع لا الظهور البصري وحده؛ لا كشف راتب أو تعديل عبر مسار مباشر، وتوثق كل حالة محجوبة لا تعد ناجحة. | not-executed |
| P7T-59 | حالة جهاز واحدة وإعادة فتح نوافذ الرواتب المغلقة | FE7-11، FE7-36 / INV7-03، INV7-08، INV7-25 | لا قراءة Home وهمية ولا Show لنسخة مغلقة ولا حالة جلسة قديمة؛ فصل خدمة الاتصال عن عمر النافذة؛ اختبار timers الشامل يبقى جزء7C. | not-executed |
| P7T-60 | اكتمال الأوامر الظاهرة مقابل المخفية/الاختيارية | FE7-11، FE7-15، FE7-26، FE7-28، FE7-35، FE7-36 / INV7-03، INV7-25 | كل أمر ظاهر ومطلوب ينفذ عقده أو يعطل برسالة دقيقة؛ المخفي والحدث الاختياري لا يسجلان عيباً تلقائياً؛ القائمة ليست شهادة اكتمال بقية UI أو محرك الطباعة. | not-executed |
| P7T-61 | فشل الحفظ المركب وعقد معاملات ربط المركب | FE7-03، FE7-04، FE7-34 / INV7-04، INV7-13، INV7-24 | يوفر @salesman وباقي العقد، وتوحد نتيجة العملية؛ لا نجاح بعد ابتلاع فشل ولا نصف ربط/قيد/حضور غير معلن؛ لا يحاول Rollback لمعاملة اعتمدت كتعويض وهمي. | not-executed |
| P7T-62 | هوية المستندات وتعديلها وإلغاؤها وربط الحساب بالكود | FE7-04، FE7-10، FE7-29 / INV7-07، INV7-10، INV7-13، INV7-25 | لا MAX+1 غير محجوز ولا حذف واسع برقم محلي أو اختيار حساب بالاسم؛ الإلغاء يعكس/يلغي القيد وفق السياسة ويحافظ على تاريخ المعاملة ولا يترك lost update. | not-executed |
| P7T-63 | حدود الفترة وسياسة مكونات الرواتب ومصدر الحضور | FE7-02، FE7-14 / INV7-01، INV7-05، INV7-06، INV7-25 | الفترات نصف مفتوحة ولا تفقد وقت آخر يوم؛ سياسة البدلات/التناسب/الحضور مكتوبة ومصدقة ولا يستنتج خصم راتب من Marine. أي سياسة/DTO غير محسوم يبقى blocked لا pass. | not-executed |
| P7T-64 | بوابة عقود SQL/COM واستكمال7B/7C قبل قبول8 | FE7-02، FE7-11، FE7-12، FE7-26، FE7-32، FE7-35، FE7-36 / INV7-08، INV7-13، INV7-18، INV7-20، INV7-25 | كل اعتماد/سياسة له مالك وإصدار وعينة أو يبقى blocked؛ لا تتغير حالة not-executed إلى pass بسبب اكتمال مستندات أو أمثلة Python؛ لا بدء8 ضمن إذن7. | not-executed |

## 4. إعادة الفحص المحلي الآمن

من جذر المستودع، Python3 stdlib وGit فقط. الأدوات تطبع stdout ولا تكتب evidence/baseline ولا تتصل بشبكة أوتستورد التطبيق:

```bash
python3 docs/audit/tools/collect_baseline.py --verify
python3 docs/audit/tools/check_feature_witnesses.py
python3 docs/audit/tools/test_audit_validator.py
python3 docs/audit/tools/validate_audit.py
python3 docs/audit/tools/validate_audit.py --through-phase 7
python3 docs/audit/tools/validate_audit.py --through-phase 6
python3 docs/audit/tools/validate_audit.py --through-phase 5
python3 docs/audit/tools/validate_audit.py --through-phase 4
python3 docs/audit/tools/validate_audit.py --through-phase 3
python3 docs/audit/tools/validate_audit.py --through-phase 2
```

تعيد الأداة توضيحات3–7A المستقلة فقط. إعادة الفحص التاريخي لا تعني أنchecks02–06 استبدلت أوأن العدد200 كان موجوداً في6. **لا تستعملcollect_baseline.py --write لإخفاء اختلاف المصدر**؛ أي تعديل تطبيق لاحق يتطلب مرجعاً/أدلة جديدة، لا أرقام أسطر قديمة وbaseline مستبدلاً.

## 5. حالة التسليم والحد التالي

7A منجزة **ساكناً ضمن47 نطاقاً منتقى**؛ ليست مراجعة كل أسطر266 مساراً أوكل ملفinventory. تحفظ [backlog10](evidence/continuation-backlog-07.csv) أن7B/7C لم يبدآ، و[H7/Q7](FEATURES-HR-PROJECTS-07.md) ما يعتمد على schema/DTO/سياسة/بيئة خارجية. لا اكتمال7 أوحكم سلامة/أداء/امتثال شامل؛ **التالي7B ضمن تدقيق7، ولا8 أوإصلاحات/تشغيل دون تفويض مستقل**.
