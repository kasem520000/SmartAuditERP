# التحقق وخطط القبول غير المنفذة — 7B15

مرجع التدقيق المعلن **2026-11-16 UTC**، ومصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول 7B15 هو دفع 7B14 المكتمل `789b04cb485948aa89e153f4b501efa27164c109` بجميع **418 ملف تدقيق**. سجل stdoutB14 الحقيقي يبقى checkout`461ceaf3e14e67e1c5b3f97a202d874746f6523f` وبصمته `e9d795dd…655a`؛ لا يعاد بعد الدفع. ساعة إنشاء التجميدات المرصودة **2026-11-19T00:42:30.011125+00:00** مستقلة عن مرجع 16 نوفمبر وعن ساعة B14 في 18 نوفمبر، وليست تاريخ تنفيذ ERP.

**7B/7 جزئيتان؛ R1/R2 سُلّمت محلياتهما وبقايا العقود مفتوحة؛ التالي المقترح 7B16/R3 ؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا معالجة أو بناء/تشغيل تطبيق أو C#/SQL/WPF/REPX/Office/COM أو مزود/جهاز/طابعة أو تصدير أعمال أو مفسر HTML/صيغة أو Process.Start فعلي أو قياس. فحوص Python/Git وثائقية، لا قبول مالي أو تشغيلي. `next_phase=8` جدولة لا إذن.

[النتائج 298](findings.csv) · [نطاق 20](review-scope-07B15.csv) · [العقود](ACCRUAL-TAX-CONTRACTS-07B15.md) · [التحقق](VALIDATION-07B15.md) · [المتبقي](PHASE-07-REMAINING-07B15.md) · [provenance413](evidence/provenance-07B15.json) · [stdout الجديد](evidence/checks-07B15.json)

## 1. ما الذي تثبته فحوص هذا الجزء؟

ثبات المصدر 827 و 413 بصمة تاريخية و 294core/ALLnext_phase وتتابع IDs وروابط الملفات والنطاقات وعلاقات FE/INV/T/RC وذيول 22 بالضبط و exactG01–164. ثلاث لقطات دخول ثابتة، ومصدر 10ba منفصل عن checkout789b04c. helpers التاريخية لم تحرر؛ B14 يتلقى OWN294row/rawCRLFbytes(295CRLF/noBOM)/exactindexes فيالذاكرة عند المسارات المنطقية الدقيقة؛ لا تبديل قرصي أو patch عام أو rebaseline.

هذا يثبت الاتساق الوثائقي وبصمات المصدر، **لا**دلالة كل جملة أوصحة حساب أو compiledcallgraph/overload أو schema نشر أوصلاحية فعلية أوقدرة قالب خارجي. نطاق الوالدين محلي كامل لاكل feature ، و C# كامل سابقاً 7A/B1. الطفل مقاطع و Home الضريبي يفتح البديل؛ صفر الفئة القديمة لا يغلق R1/R2.

## 2. أدوات تدقيق فقط

من جذر المستودع، بـ Python3stdlib و Git. اكتب أي خرج تشخيصي جديد إلى stdout أو`/tmp`، **لا**تعد كتابة سجل checks تاريخي أوتعدله بعد الدفع:

```bash
python3 -B docs/audit/tools/collect_baseline.py --verify
python3 -B docs/audit/tools/check_accrual_tax_witnesses.py
python3 -B docs/audit/tools/test_accrual_tax_audit_validator.py
python3 -B docs/audit/tools/validate_audit.py
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B14
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B13
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B12
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part A
```

الأوضاع التاريخية 20:2–6 و A/B1…B14 ، لكلٍ OWNcutoff لا 298 الحالي. B14=294 و B13=291 و B12=289 ؛ B10…B14 تتلقى البايتات الأصلية CRLF بالذاكرة أيضاً. العدادات المعاد احتسابها بالمدقق الحالي ليست استنساخاً حرفياً للـ stdout القديم ولا تستبدله. B14 الأصلي checkout461 ثم push789 ؛ هذا الجزء سجل جديد checkout789 عند الالتقاط، لا بصمة ذاتية له.

[check_accrual_tax_witnesses](tools/check_accrual_tax_witnesses.py) لا يفسر الشيفرة أو SQL.24 مثالاً يدوياً مستقلاً بقيم وتواريخ وموظفين خياليين، منها 31 فبراير لا يوم التدقيق؛ و 24 ملاحظة tokens/text في 93 قراءة نطاق محددة لا semantic coverage. طباعته تعني JSON لاطباعة أعمال. [الشاهد المحفوظ الجديد](evidence/report-witnesses-07B15.json) stdout حقيقي قابل للمقارنة مع إعادة توليد قرائية فقط.

[test_accrual_tax_audit_validator](tools/test_accrual_tax_audit_validator.py) يضيف 32 حالة اصطناعية لـ adapters/CRLF/restore-on-exception/nesting/core/tails/Grows/links/scopes/gates/adjudication وعدم بدء C. مع 350 حالة سابقة محفوظة=382 عبر 16 مجموعة. **ليست 36 قبول ERP مجتازاً.** رفضت أثناء التأليف نطاقات tokens غير دقيقة وخطأ في بناء رسالة None بالمدقق؛ صححت الأدلة والمدقق الجديد، لا إضعاف البوابات أو تحرير المحمي. لا يرفع نجاحها حالة potential.

## 3. مصفوفة خطط 36 — كلها not-executed

8 مباشرة للجديد، 22 لأصول تاريخية، 4 عقود مشتركة، 2 بوابة حصر/إذن. [CSV الكامل](evidence/acceptance-tests-07B15.csv) يحفظ prerequisites/procedure/criterion/safety/evidence والعلاقات الثنائية. أي ERP أو Windows/SDK/SQL/WPF/قالب/طابعة يتطلب إذناً مستقلاً للمرحلة 8 وبيئة معزولة وعقداً مصادقاً وبيانات synthetic. الحاجز أوالعقد غير المتاح blocked لا passed ؛ لا يفترض إصلاح 001/002/003 أوالكاتب أو FK للوصول إلى sink.

| المعرف | الأصل/الإحالة | النوع | السيناريو المقترح | FE/INV | المعيار | الحالة |
| --- | --- | --- | --- | --- | --- | --- |
| P7B15T-01 | P7-123 | finding-specific | فترة ماضية قبل أول عرض ثم إعادة العرض | FE7B15-01 / INV7B15-01 | اختيار سنة/شهر صالحين غير الحاليين ثم عرض مرتين يحافظ عليهما وعلى حدود مصدر الإضافات؛ defaults للحالة الجديدة فقط. لا تعاد الهوية أو الفترة سراً. | not-executed |
| P7B15T-02 | P7-123 | finding-specific | سنة وشهر مختلفان عن الحاليين مقابل أمر جديد صريح | FE7B15-01 / INV7B15-01 | اختيار سنة/شهر صالحين غير الحاليين ثم عرض مرتين يحافظ عليهما وعلى حدود مصدر الإضافات؛ defaults للحالة الجديدة فقط. لا تعاد الهوية أو الفترة سراً. | not-executed |
| P7B15T-03 | P7-124 | finding-specific | يوم 31 إلى فبراير مع إضافات شهرية مختلفة | FE7B15-02 / INV7B15-02 | انتقال 31 يناير→فبراير أو 31 مايو→أبريل لا يحتفظ بمبالغ/اختيار A قابلة للحفظ باسم B. إما إعادة حساب ناجحة واحدة تحت B أوحالة فشل معلنة تمنع الحفظ والطباعة النهائية. | not-executed |
| P7B15T-04 | P7-124 | finding-specific | يوم صالح مقابل انتقال 31 إلى شهر 30 يوماً مع رفض الحفظ القديم | FE7B15-02 / INV7B15-02 | انتقال 31 يناير→فبراير أو 31 مايو→أبريل لا يحتفظ بمبالغ/اختيار A قابلة للحفظ باسم B. إما إعادة حساب ناجحة واحدة تحت B أوحالة فشل معلنة تمنع الحفظ والطباعة النهائية. | not-executed |
| P7B15T-05 | P7-125 | finding-specific | جلسة A واختيار B المفوض مع قبض وفواتير مختلفة | FE7B15-03 / INV7B15-03 | بيانات A/B متميزة:اختيار B لا يضم قبض A ؛ all المصرح يجمع قبض A+B كما الفواتير؛ كل DTO/card من criteria واحدة دون افتراض منح أو schema. | not-executed |
| P7B15T-06 | P7-125 | finding-specific | كل الفروع المفوضة وسياق BranchNo=-1 مع ضبط معنى all | FE7B15-03 / INV7B15-03 | بيانات A/B متميزة:اختيار B لا يضم قبض A ؛ all المصرح يجمع قبض A+B كما الفواتير؛ كل DTO/card من criteria واحدة دون افتراض منح أو schema. | not-executed |
| P7B15T-07 | P7-126 | finding-specific | ربع محدد ثم تفعيل شهري دون off يدوي | FE7B15-04 / INV7B15-04 | ربع→شهر وشهر→ربع يتركان القائمة النشطة وحدها enabled وتواريخ صالحة للنمط النهائي؛ العكس/التكرار/إلغاءكليهما لا يحبس controls أو يستبقي معياراً غير معلن. | not-executed |
| P7B15T-08 | P7-126 | finding-specific | شهر محدد ثم تفعيل ربعي ومقارنة أول تفعيل بلا نمط سابق | FE7B15-04 / INV7B15-04 | ربع→شهر وشهر→ربع يتركان القائمة النشطة وحدها enabled وتواريخ صالحة للنمط النهائي؛ العكس/التكرار/إلغاءكليهما لا يحبس controls أو يستبقي معياراً غير معلن. | not-executed |
| P7B15T-09 | P1-004 | historical-root-regression | انحدار أصل P1-004 — قالب ونشر وإعداد فعّال لكل قناة | FE7B15-05 / INV7B15-05 | manifest/schema ونسخة DTO/REPX وإعداد فعّال لكل قناة. وثّق أثر flags/copies ومصادر subreports ، ولا تصادق شكل الورقة من DTO. | not-executed |
| P7B15T-10 | P1-011 | historical-root-regression | انحدار أصل P1-011 — SQL بهويات محمولة من controls والمتصل | FE7B15-06 / INV7B15-06 | مرّر identifiers وطلباً typed إلى repository بمعلمات، وصنّف مصدر كل قيمة قبل اعتبارها مدخل مهاجم. SQL ذو المعلمات شاهد مقابل لا إغلاق عام. | not-executed |
| P7B15T-11 | P1-013 | historical-root-regression | انحدار أصل P1-013 — توقيت وحدود صلاحيات مداخل الوالد والطفل | FE7B15-07 / INV7B15-07 | تفويض كل command عند حد موثوق بمعرف أمر مستقل عن Name. حالة visual-tree وتوقيت Show ليسا قبول ACL ؛ تحقق الأدوار لاحقاً بعد إذن مستقل للمرحلة 8. | not-executed |
| P7B15T-12 | P1-030 | historical-root-regression | انحدار أصل P1-030 — مرجع محرر static مقابل إغلاقه الحقيقي | FE7B15-08 / INV7B15-08 | Factory/ownership يعيد إنشاء النافذة بعد Closed أو يختار Hide بسياسة صريحة. تحقق الجلسة والاشتراكات لاحقاً، ولا تستنتج leak من النص. | not-executed |
| P7B15T-13 | P2-001 | historical-root-regression | انحدار أصل P2-001 — حارس أمر الحفظ والحذف مستقل عن تمكين الزر | FE7B15-09 / INV7B15-09 | Authorization لأوامر read/save/delete/print في طبقة موثوقة بعد اشتقاق allowedBranchSet ، لا الاكتفاء بتعطيل زر أو تغيير اسمه. | not-executed |
| P7B15T-14 | P2-010 | historical-root-regression | انحدار أصل P2-010 — الفرع المسموح منفصل عن معيار التقرير | FE7B15-10 / INV7B15-10 | مفتاح canonical ومجموعة فروع مسموحة يتقاطعان مع كل read/write/output عند حد موثوق؛ all لا يلغي allowed set. DDL المرفق ليس شهادة نشر. | not-executed |
| P7B15T-15 | P3-002 | historical-root-regression | انحدار أصل P3-002 — شروط القيد والدفعة كاملة قبل اعتماد مالي | FE7B15-11 / INV7B15-11 | نموذج قيد typed يتحقق من الحسابات والتوازن والعملة والدقة وعلاقات المستند قبل الكتابة؛ null/empty/invalid رفض لا success. | not-executed |
| P7B15T-16 | P3-003 | historical-root-regression | انحدار أصل P3-003 — ذرية اختيار الرواتب والتحقق قبل أول كتابة والحذف | FE7B15-12 / INV7B15-12 | تحقق من المجموعة كلها قبل الكتابة، واعتمد الرأس والتفاصيل والقيد والنتيجة بحد واحد. فشل الموظف الثاني أو حذف القيد لا يبقي رأساً أو دفعة جزئية. | not-executed |
| P7B15T-17 | P3-005 | historical-root-regression | انحدار أصل P3-005 — رقم العرض ورقم الحفظ والهوية ليسوا حجزاً واحداً | FE7B15-13 / INV7B15-13 | هوية ومفتاح مستند بقاعدة فردية وذرية معتمدة؛ رقم العرض لا يعد حجزاً، ولا يتغير id دون مواءمة GlobalID. قبول سباق اصطناعي يحتاج إذناً لاحقاً. | not-executed |
| P7B15T-18 | P3-006 | historical-root-regression | انحدار أصل P3-006 — تعديل السجل المالي وحفظ نسخة المصدر | FE7B15-14 / INV7B15-14 | سياسة تعديل ومراجعة و optimistic-concurrency مع نسخة المستند وقيده الذري. سجل قبل/بعد ومنفذ وسبب؛ transaction ليست بذاتها سجل تاريخ. | not-executed |
| P7B15T-19 | P3-007 | historical-root-regression | انحدار أصل P3-007 — Decimal الواجهة و Float القاعدة والنص ليست دقة واحدة | FE7B15-15 / INV7B15-15 | ثبّت مقياس العملة والتقريب قبل الحفظ والجمع و DTO وتسامح المصالحة. اختبر الكسور والحدود وفق عقد decimal معتمد، بعد إذن 8 فقط. | not-executed |
| P7B15T-20 | P3-023 | historical-root-regression | انحدار أصل P3-023 — مدى يوم نصف مفتوح في الوالد مقابل حدود الطفل | FE7B15-16 / INV7B15-16 | DateRange صريح [from,toExclusive) مشترك لكل المصادر والطفل. اختبر آخر ثانية وكسورها وبداية الغد و culture/zone ، واحفظ الشاهد الإيجابي للوالد. | not-executed |
| P7B15T-21 | P7-001 | historical-root-regression | انحدار أصل P7-001 — Typed-row/null ونتيجة حفظ الاستحقاق السابقة | FE7B15-17 / INV7B15-17 | List<SalaryAccrualLine> واحدة بعقد نتيجة مركب، ورفض null وفشل أي كاتب. إشارة النجاح بعد اعتماد الجميع فقط، دون إعادة عد الجذر. | not-executed |
| P7B15T-22 | P7-002 | historical-root-regression | انحدار أصل P7-002 — مصدر العرض والهوية والفترة عند إعادة الفتح | FE7B15-18 / INV7B15-18 | LoadAccrualTyped بعد التهيئة مع هوية وفترة ومجموعة واحدة للعرض والتحديد والحفظ والطباعة. controls الخفية ليست مالك هوية النموذج. | not-executed |
| P7B15T-23 | P7-003 | historical-root-regression | انحدار أصل P7-003 — EmployeeId عند reload والطباعة البنكية | FE7B15-19 / INV7B15-19 | EmployeeId موجب وموجود ومرتبط بنفس detail عبر save/reload/print. unknown/failed في فحص الهوية يمنع الاعتماد، لا يتحول إلى 0 مقبول. | not-executed |
| P7B15T-24 | P7-031 | historical-root-regression | انحدار أصل P7-031 — نتيجة الإخراج القابلة للرصد في استحقاق الرواتب | FE7B15-20 / INV7B15-20 | PrintResult يفصل cancel/template-missing/build-failed/spool-accepted/unknown. نجاح preview ليس طباعة مؤكدة؛ لا طباعة أو Office نُفّذ. | not-executed |
| P7B15T-25 | P7-032 | historical-root-regression | انحدار أصل P7-032 — بيانات تعريف حالية داخل إعادة طباعة الاستحقاق | FE7B15-21 / INV7B15-21 | احفظ لقطة الإصدار أو وسم إعادة الطباعة بأنها بيانات حالية بسياسة مصادق عليها. Version/master-lineage معلوم، والخصوصية وحق إظهار البنك مستقلان. | not-executed |
| P7B15T-26 | P7-043 | historical-root-regression | انحدار أصل P7-043 — معادلة TAXED/NOTAX بقيت الجذر السابق | FE7B15-22 / INV7B15-22 | breakdown لكل سطر وفئة ومعدل وتوزيع خصم صريح؛ لا header-rate لبند 0%. taxval0 ليست فئة exempt قانونية بذاتها، و P4-003 ليس مفترض الإصلاح. | not-executed |
| P7B15T-27 | P7-044 | historical-root-regression | انحدار أصل P7-044 — معفى ظاهر وإجمالي لا يجمعه إلى DTO | FE7B15-23 / INV7B15-23 | total=sum المكونات الدلالية الأصلية بعد اعتماد الأنواع والإشارات. اختبر معفى فقط ومختلطاً ومرتجعاً وصفراً؛ لا تعد المجموع الفرعي مكوناً ثانياً. | not-executed |
| P7B15T-28 | P7-045 | historical-root-regression | انحدار أصل P7-045 — الصفوف والفترة والاختيار وطلب الطفل snapshot واحدة | FE7B15-24 / INV7B15-24 | snapshot يجمع criteria والصفوف المختارة المحفوظة والهوية والصحة. طلب child typed يعلن subset ومصادر الفرق؛ dirty يبطل الاعتماد وفق سياسة الحفظ والطباعة. | not-executed |
| P7B15T-29 | P7-046 | historical-root-regression | انحدار أصل P7-046 — النشر الجزئي وفشل parsing ليسا valid-zero | FE7B15-25 / INV7B15-25 | Result(valid/empty/failed/partial) لكل مصدر و snapshot واحدة للعرض والمجاميع و DTO. الفشل لا يسمح بنسخة نهائية تجمع قديماً وجديداً بلا وسم. | not-executed |
| P7B15T-30 | P7-051 | historical-root-regression | انحدار أصل P7-051 — مواءمة أساس التأجير مع عمود الصافي | FE7B15-26 / INV7B15-26 | حدد أساس المصدر والضريبة والإضافات والتأمين بسياسة قانونية ومحاسبية. شامل 115 وضريبة 15 لا يسمى أساس 115 بلا تعريف معتمد للمقياس؛ لا طرح أو عكس عشوائي. | not-executed |
| P7B15T-31 | H7B15-01 | cross-cutting-contract | عقد مشترك — سياسة أهلية ومكونات الاستحقاق | FE7B15-27 / INV7B15-27 | عقد أهلية وفترة وحسابات ودقة مصادق عليه قبل المقارنة؛ لا افتراض أن كل بدل حق مستحق أو أن صافي 0 ممنوع قانونياً. | not-executed |
| P7B15T-32 | H7B15-02 | cross-cutting-contract | عقد مشترك — تصنيف المصادر ومرحّل الفترات والضريبة الإضافية | FE7B15-28 / INV7B15-28 | كل خلية لها source/category/rate/unit/sign/period/branch وأهلية. الثوابت 0 والفراغات لا تعلن عدم وجود عمل أو اكتمال إقرار. | not-executed |
| P7B15T-33 | H7B15-03 | cross-cutting-contract | عقد مشترك — مخرج DTO والقالب والإعداد الفعّال | FE7B15-29 / INV7B15-29 | manifest/schema معتمدان ومصدر إخراج snapshot. أثر flags والحقل و subreport يتحقق لاحقاً بإذن لا بالتخمين. | not-executed |
| P7B15T-34 | H7B15-05 | cross-cutting-contract | عقد مشترك — عمر وملكية وثقافة وأداء مصدر لا تقاسه الأسطر | FE7B15-30 / INV7B15-30 | مؤشرات مصدر بحدود ومدخلات قياس مستقلة؛ لا حكم ذاكرة أو فهرس أو زمن من حلقة أو using ، و 7C غير مبدوءة. | not-executed |
| P7B15T-35 | H7B15-06 | documentary-scope-or-authorization-gate | بوابة توثيق — حصر العمق وبقايا R1/R2 لا كل التقارير | FE7B15-31 / INV7B15-31 | قدرة×شاشة×تنفيذ×خطة أو استبعاد مسند/handoff/split لبقايا R1/R2 ثم R3/R4. تصنيف 33local+19selected+0old في 52 ليس نسبة whole-feature.7B16/R3 مقترحة، و 7C لم تبدأ. | not-executed |
| P7B15T-36 | H7B15-06 | documentary-scope-or-authorization-gate | بوابة توثيق — حفظ التاريخ والإذن وسجل الفحوص | FE7B15-32 / INV7B15-32 | 827path/hash ثابتة وسجل فحوص جديد حقيقي مرة واحدة.7B/7 جزئيتان، 7C لم تبدأ، 8 غير مأذونة. ERP/SQL/قبول/قياس/معالجة 0 ، و next_phase8 تخطيط لا authorization. | not-executed |

## 4. هوية التجميدات وحماية الأرشيف

| السجل | SHA256 الثابت |
| --- | --- |
|[frozen294](evidence/findings-through-07B14.csv)|`8cd8fdbcee2d522dae32a561f9b41460b1c4b0ddf9ca2d38763015677ffadf16`|
|[exactB14indexes](evidence/shared-indexes-through-07B14.json)|`ae628ed72893c00310314fe239c0c6934324321ec94c5265e43dde964f744a5e`|
|[provenance413](evidence/provenance-07B15.json)|`ac4977145152f1c787dd2e4fd9f414b49789c204dabfc21c99222349354323cf`|
|[genuinechecksB14](evidence/checks-07B14.json)|`e9d795dde67e358e9b03e46b449a6314e9cff3613a254e832cb433ed789c655a`|

الملفات الخمسة القديمة التي يجوز أن تتقدم هنا:findings/README/PLAN/IMPROVEMENTS/tools/validate_audit فقط. باقي 413 حرفياً وثلاث تجميدات ثابتة؛ لا overlay على helpers/witnesses/tests/reports/checks القديمة. كل next_phase محفوظ حتى 8 ، وبادئة evidence+manifest-tail واحد فقط للجذور 22. G01–164 بنفس نص صفوفها، و G165–170 إضافة. source10ba/original827 والفرع الفعال نفسهما؛ لا صنع تاريخ أوتغيير base.

تصويب B10 إضافي فقط:2×5=10 محلياً، و 2×12×5=120 مرجعياً، وعند equality1 كلاهما 10. لا archive rewrite أوتغيير G138/EX7B10-06 ؛ ولا checker بنيوي يصادق كل النثر التاريخي.

## 5. سجل الفحوص الوثائقية المنفذة فعلاً

| الفحص المنفذ | النتيجة الفعلية وحدودها |
| --- | --- |
| `collect_baseline.py --verify` | exit0؛ تطابق827/827 مساراً وبصمة أصلية. لا إعادة إنشاءbaseline. |
| `validate_audit.py` للوضع الحالي | exit0 و`errors=[]`؛298 نتيجة، و827 بصمة أصلية مطابقة. فحص الروابط ونطاقات المصدر وعلاقات الجداول، لا صحة حسابERP. عدادات المراجع والروابط تشمل التكرار وتوجد فيstdout الجديد. |
| مجموعات المدقق الاصطناعية16 | **382/382 ناجحة**:10+14+20+18+20+22+28+24+28+24+28+30+32+24+28+32. كل مجموعة exit0 وبعددها المتوقع؛350 سابقة محفوظة و32 جديدة، مع فحصNone متزامن مع حالة غير صالحة أيضاً. لا استيراد أوتشغيل تطبيق. |
| الأوضاع التاريخية20 | كلهاexit0 و`errors=[]` و827 بصمة مطابقة؛2→49،3→74،4→106،5→137،6→172،A→200،B1→223،B2→237،B3→248،B4→261،B5→266،B6→270،B7→276،B8→280،B9→282،B10→285،B11→287،B12→289،B13→291،B14→294. استُخدمتOWNsnapshots دون إعادة كتابة أيchecks قديم. |
| الشاهد المستقل الجديد وإعادة توليده القرائية |24 مثالاً يدوياً و24 ملاحظة نصية و93 قراءة نطاق؛`errors=[]`، وstdout المعاد مطابق بايتياً للشاهد المحفوظ. SHA256=`bf2c5f960b0626881f4cdd9567086e81ed6a8da75c9126680b04f8fbcdd6f653`. ليسsemantic coverage. |
| حارس الحفظ المستقل |413 بصمة تاريخية وثلاث تجميدات الدخول ثابتة؛294core وكلnext_phase وبادئةevidence محفوظة، و22 ذيلاً يساويmanifest بالضبط. صفوفG01–164 حرفياً وبالترتيب، وتضافG165–170 فقط. findings الحالي299CRLF بلاBOM، واللقطة295CRLF بلاBOM. |
| حدود التغيير | خمسة ملفات قديمة حية فقط تقدمت، والباقي إضافات تدقيق تحت`docs/audit/`. source10ba ثابت والفرع نفسه؛ لا تغيير تطبيق أوhelper تاريخي أوأرشيف. فحصGit مع`core.whitespace=cr-at-eol` يحافظ علىCRLF المقصودة. |

مسار الالتقاط الرسمي هو[evidence/checks-07B15.json](evidence/checks-07B15.json):stdout حقيقي للمدقق عندcheckout789b04c، يُنشأ مرة واحدة بـexclusive-create إلى مقبض الإخراج نفسه، لاJSON يدوي أوplaceholder ولا تعديل لاحق لساعةcheckout بعدcommit/push. وجود المسار أثناء توجيه stdout ليس قبولاً لمحتوى غير متحقق؛ يعاد فحصJSON بعد اكتمال العملية، وتذهب فحوص ما بعد الحفظ والدفع إلى`/tmp` فقط. المقارنة اللاحقة تحفظ بصمته ولا تستبدله بسجلcheckout أحدث.

## 6. ما لم ينفذ

ERP/build/C#/SQL/WPF/SDK/REPX/Office/COM/provider/device/printer/formula/HTMLinterpreter/actual-business-export/Process.Start/معالجة/قياس/بيانات أعمال أوأسرار=**0**. لا قبول مالي أوتشغيلي أوشهادة ضريبة أوسياسة رواتب أو ACL نشر أو FK/فهرس/خطة تنفيذ/ذاكرة/زمن. النماذج المستقلة لا تثبت سلوك وقت تشغيل، و DDL المرفق ليس نشراً معتمداً.

**7B/7 جزئيتان؛ R1/R2 ببقايا عقود صريحة؛ 7B16/R3 مقترحة؛ 7C لم تبدأ؛ 8 غير مأذونة.** كل 36 خطة not-executed وكل 298 نتيجة مفتوحة بلا تعديل تطبيق أوإغلاق أوإعادة تصنيف قديم.
