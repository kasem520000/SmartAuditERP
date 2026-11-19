# تحقق 7B21 — وثائق منفذة وخطط أعمال غير منفذة

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711` والفرع `arena/94ae8414-smartauditerp`. دخول B21 بعد دفع B20 المكتمل `c2c895d0df0e4f106c4e5c2853219aa04303e002` بجميع **588 مسار تدقيق**. ساعة التجميد المرصودة `2026-11-19T19:30:15.393695+00:00` مستقلة عن المرجع المعلن؛ ليست تاريخ تشغيل أو قبول.

**R4e سُلّم بحدود الشريحة فقط؛ 7B/7 جزئيتان؛ R4f/7B22 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا بناء أو تشغيل ERP/C#/VB/.NET/WPF/SQL أو SDK/provider/UtilitiesProj/ToDataTable/REPX أو قالب/طابعة/ماسح أو بيانات أعمال أو أسرار أو إصلاح أو قياس أو قبول. Python و Git لأدوات الوثائق فقط؛ `next_phase=8` تخطيط لا إذن.

[النتيجة](PHASE-07B21.md) · [عقود التفقيط والعملة](AMOUNTWORD-CONTRACTS-07B21.md) · [التحقق والخطط](VALIDATION-07B21.md) · [المتبقي](PHASE-07-REMAINING-07B21.md) · [scope24](review-scope-07B21.csv) · [السجل](findings.csv) · [provenance583](evidence/provenance-07B21.json) · [stdoutB21](evidence/checks-07B21.json)

## 1. ما نُفذ فعلاً وما لم ينفذ

- نُفذت 36 حالة جديدة لمدقق الوثائق وحده، بعد إضافة سياق B20 التاريخي الضيق. الحالات السابقة 530 محفوظة دون تعديل؛ B20/32 في طفل تاريخي صريح، و B19/36 و B18/28 محفوظة.
- نُفذت 26 وضعية OWN فعلية من 2–6 و A/B1…B20؛ كلها exit0/errors[]/827. الأرشيف التالي ملخص stdout حقيقي ببصمة وطول و exitcode، لا نسخة من checks قديمة أو إعادة مزعومة لمقاييس أصلية.
- الشاهد 12manual+12lexical يعاد حسابه قراءة فقط ويطابق capture الأول:33 قراءة من 20 مساراً؛ 477 lexical scans لا تساوي 477 body reviews. النماذج ASCII/Decimal وبوليان parse مفترض، لا.NET/VB/SQL/كلمات/قالب أو طابعة.
- **كل 36 خطة قبول أدناه not-executed**، بما فيها البوابات الوثائقية المخططة. لا build/ERP/WPF/SDK/provider/ToDataTable/REPX/print أو بيانات أعمال أو إصلاح أو قبول أو قياس. نجاح المدقق لا يغير certainty المحتمل لـ 014/132 أو حالة أي finding.

نجح CLI الحالي الافتراضي وبـB21 الصريح في الفحص الفعلي: **566 حالة مدقق وثائق عبر 22 مجموعة، errors=[]**، مع 313 نتيجة و 827 بصمة؛ 530 حالة سابقة و 36 جديدة. هذه فحوص وثائق لا قبول أعمال. الأرشفة الرسمية تلتقط stdout الحقيقي مباشرة دون تحويل JSON أو تعديل flags.

الفحص التحضيري أبلغ `pending=true` لأن ملف checksB21 لم يوجد بعد. لا يحول هذا الخرج إلى أرشيف نهائي بتغيير flag؛ الأرشفة اللاحقة توجه stdout الخام إلى sink حصري، ويبلغ المدقق حالة وجوده الفعلية وقت capture.

أعيد فحص B20 منفصلاً على الشيفرة النهائية أثناء التحضير: **OWN310/530 حالة/21 مجموعة، errors=[]** وكل32 أصلية في الطفل التاريخي. هذا ليس ادعاء إعادة جميع26 وضعية بعد تعديلات الختام. كما نجح `collect_baseline.py --verify`: **827 بصمة/29,128,444 بايت، XML errors=0 وXAML name mismatches=0**؛ `dotnet_available=false`، ولا يعد تحليل XML بناء WPF أو قبولاً تشغيلياً. حارس الحفظ المستقل طابق أيضاً827 ملفاً مع كائنات Git للمصدر10ba، وكل583 مادة و310 صفوف وبادئةCRLF وG195 والتجميدات الثلاثة؛ لم تتغير إلا المسارات الخمسة المشتركة المسموح بها.

## 2. الحالة الحالية مقابل التاريخي

`build_cli_parser` والـ entrypoint الحقيقيان افتراضهما B21؛ `main` البرمجي يبقى B15 للتوافق. PHASE7_B20_CLI و B19/B18/B17/B16 قواعد خيارات تاريخية فعالة، لا أن default اليوم B20.

[Historical childB20](tools/run_historical_barcode_tests_07B21.py) يحمل كل 32 حالة أصلية بـ loadTestsFromModule، ويتحقق من count32 ولا skip، ويختار presetB20 محلياً للطفل ثم يرده في finally. لا يحرر الاختبارات أو يخفي تعارض default؛ الحالي B21 يفحص default و routing باستقلال. سياق B20 يأخذ OWN310/raw311CRLF والفهارس المجمدة في الذاكرة، لا live313؛ facade يلتقط argv واحداً فقط ويحفظ kwargs. Path subclass على AUDIT instance المحدد، لا global pathlib patch أو filesystem overlay. B19/36 و B18/28 يحتفظان بطفليهما دون إعادة تسمية التاريخ.

أوامر قراءة آمنة؛ توجه النواتج إلى scratch لا إلى الأرشيف الرسمي مرة أخرى:

```bash
python3 -B docs/audit/tools/validate_audit.py
python3 -B docs/audit/tools/validate_audit.py --phase7-part B21
python3 -B docs/audit/tools/validate_audit.py --phase7-part B20
python3 -B docs/audit/tools/run_historical_barcode_tests_07B21.py --through-part B20
python3 -B docs/audit/tools/run_historical_navigation_tests_07B20.py --through-part B19
python3 -B docs/audit/tools/run_historical_caller_request_tests_07B19.py --through-part B18
python3 -B docs/audit/tools/test_amountword_contract_audit_validator.py
python3 -B docs/audit/tools/check_amountword_contract_witnesses.py
python3 -B docs/audit/tools/collect_baseline.py --verify
git -c core.whitespace=cr-at-eol diff --check
```

لا تشغّل ملف B20 المحمي standalone ضد defaultB21 لإثبات default قديم؛ استخدم طفله التاريخي. لا--write أو حزم SDK أو SQL/provider أو أجهزة.

## 3. حالات المدقق 36 ومحدوديتها

| الحالات | الموضوع والحد |
| --- | --- |
|01–07|OWN310/311CRLF و copy/isolation/restore/nested307، وحفظ كل حقل و 314CRLF و G195→200؛ تحويرات اصطناعية بالذاكرة.|
|08–12|تقنيع التعليقات/النصوص والنداءات المتوازنة والـ hash و WC12/CM10؛ لا تحليل types أو SDK enum.|
|13–18|sentinel صريح ودليل scope و FE/INV/T36 بالجهتين ومسؤوليات RS14 وبقاء 6C، و strict bool/int-zero وتصويب B10.|
|19–20|بصمة الشاهد وتطابق إعادة حسابه قراءة فقط، وبصمة أرشيف 26 الحقيقي وبنيته. نموذج 26 آخر اصطناعي لتحوير schema، وليس دليلاً على تنفيذ الأوضاع؛ null التاريخي ليس 0.|
|21–29|نماذج مواضع 12/13 وعملة DTO و parse outcome مُعطى وفروع محلية وقوائم ordinal افتراضية وحدود zero/sign/side؛ ليست.NET conformance.|
|30–36|كل 310 و 034/035 و potential014/132 وصفر extensions، و actualB21/APIB15 و routing/argv/facade/ALL32/history hashes/scope24.|

## 4. سجل 26 التاريخي الحقيقي — null ليس صفر اختبارات

[saved26](evidence/historical-mode-verification-07B21.json)؛ 43585 بايت/SHA256=`5ea5719515ba74f4ac7e3a2f7301cf66ed3a399dc9f5748344393d0797888279`. genuine capture checkout=`c2c895d0df0e4f106c4e5c2853219aa04303e002`؛ بصمات أدوات capture-time فيه حقيقية. صدر قبل تثبيت SHA والنثر النهائي وتقوية الحالة 20 بقراءة الأرشيف الحقيقي؛ لا تدعى إعادة كل 26 بعد هذه التغييرات أو بعد push. فحوص current والـ historical child اللاحقة توثق في stdout الحالي باستقلال.

| الوضع | OWN findings / registry | حالات/مجموعات مدقق معلنة | النتيجة |
| --- | --- | --- | --- |
| phase2 | 49 / evidence/findings-through-02.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| phase3 | 74 / evidence/findings-through-03.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| phase4 | 106 / evidence/findings-through-04.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| phase5 | 137 / evidence/findings-through-05.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| phase6 | 172 / evidence/findings-through-06.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| A | 200 / evidence/findings-through-07A.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| B1 | 223 / evidence/findings-through-07B1.csv | null / null — لم يبلغ تاريخياً | exit0؛ errors[]؛ 827 بصمة |
| B2 | 237 / evidence/findings-through-07B2.csv | 44 / 3 | exit0؛ errors[]؛ 827 بصمة |
| B3 | 248 / evidence/findings-through-07B3.csv | 62 / 4 | exit0؛ errors[]؛ 827 بصمة |
| B4 | 261 / evidence/findings-through-07B4.csv | 82 / 5 | exit0؛ errors[]؛ 827 بصمة |
| B5 | 266 / evidence/findings-through-07B5.csv | 104 / 6 | exit0؛ errors[]؛ 827 بصمة |
| B6 | 270 / evidence/findings-through-07B6.csv | 132 / 7 | exit0؛ errors[]؛ 827 بصمة |
| B7 | 276 / evidence/findings-through-07B7.csv | 156 / 8 | exit0؛ errors[]؛ 827 بصمة |
| B8 | 280 / evidence/findings-through-07B8.csv | 184 / 9 | exit0؛ errors[]؛ 827 بصمة |
| B9 | 282 / evidence/findings-through-07B9.csv | 208 / 10 | exit0؛ errors[]؛ 827 بصمة |
| B10 | 285 / evidence/findings-through-07B10.csv | 236 / 11 | exit0؛ errors[]؛ 827 بصمة |
| B11 | 287 / evidence/findings-through-07B11.csv | 266 / 12 | exit0؛ errors[]؛ 827 بصمة |
| B12 | 289 / evidence/findings-through-07B12.csv | 298 / 13 | exit0؛ errors[]؛ 827 بصمة |
| B13 | 291 / evidence/findings-through-07B13.csv | 322 / 14 | exit0؛ errors[]؛ 827 بصمة |
| B14 | 294 / evidence/findings-through-07B14.csv | 350 / 15 | exit0؛ errors[]؛ 827 بصمة |
| B15 | 298 / evidence/findings-through-07B15.csv | 382 / 16 | exit0؛ errors[]؛ 827 بصمة |
| B16 | 299 / evidence/findings-through-07B16.csv | 410 / 17 | exit0؛ errors[]؛ 827 بصمة |
| B17 | 300 / evidence/findings-through-07B17.csv | 434 / 18 | exit0؛ errors[]؛ 827 بصمة |
| B18 | 302 / evidence/findings-through-07B18.csv | 462 / 19 | exit0؛ errors[]؛ 827 بصمة |
| B19 | 307 / evidence/findings-through-07B19.csv | 498 / 20 | exit0؛ errors[]؛ 827 بصمة |
| B20 | 310 / evidence/findings-through-07B20.csv | 530 / 21 | exit0؛ errors[]؛ 827 بصمة |

## 5. كل خطط القبول 36 — غير منفذة

الخطة تحدد prerequisites/procedure/criterion وسلامة ومصدراً وروابط FE/INV بالجهتين؛ ليست اسماً لنتيجة ناجحة. أول 6 finding-specific، والباقي عقود أو أصول قديمة أو بوابات وثائقية. لكل source شرائح scope، وللبوابات metadata sentinel لا citation مصطنع. البيئة والعقود والصلاحيات والبناء حواجز؛ الحجب ليس نجاحاً.

| الخطة/النوع/الإحالة | المقدمات والإجراء اللاحق | معيار القبول المطلوب لا النتيجة |
| --- | --- | --- |
| P7B21T-01 / finding-specific<br>FE7B21-01 / INV7B21-01<br>P7-139 | نصا ASCII افتراضيان 999999999999 و 1000000000000؛ تحديد ثقافة و SDK لاحقاً.<br>**الإجراء:** قارن حد 12/13 بعد توثيق Format الفعلي، واقرأ الرتب مقابل المقدار دون طباعة الآن. | المجال المعلن يفسر بالرتبة الصحيحة، وخارجه رفض قبل الكلمات لا 100 مليار لمقدار تريليون.<br>**not-executed** |
| P7B21T-02 / finding-specific<br>FE7B21-01 / INV7B21-01<br>P7-139 | القيمتان 1000000000000 و 1000000000001 وشاهد صغير 123.<br>**الإجراء:** قارن تمييز القيمتين وشاهد 123، وافصل إسقاط الخانة عن grammar والكسر. | لا تتصادم قيمتان مدعومتان بسبب الخانة 13؛ خارج المجال رفض صريح، ويبقى الشاهد الأصغر بدلالته.<br>**not-executed** |
| P7B21T-03 / finding-specific<br>FE7B21-02 / INV7B21-02<br>P7-140 | فاتورتان اصطناعيتان بنفس Currency و Net؛ InvoiceItems مقابل Items فقط.<br>**الإجراء:** قارن currency والتفقيطين قبل ToDataTable، وراجع aliases إذا ورد manifest دون تشغيل. | يحمل الفرعان الهوية نفسها وفق العقد، أو يرفض البديل قبل إخراج DTO ناقص.<br>**not-executed** |
| P7B21T-04 / finding-specific<br>FE7B21-02 / INV7B21-02<br>P7-140 | عملة opaque بلا اسم مفترض؛ Items فارغة أو كل ProductId موجب كشواهد.<br>**الإجراء:** افصل غياب row عن row بديل بلا currency، وقارن default string.Empty بإسناد primary. | لا تنسب فراغ حقل لصف غير موجود، ولا يعد إصلاح تسميات 035 علاجاً لإسناد currency.<br>**not-executed** |
| P7B21T-05 / finding-specific<br>FE7B21-03 / INV7B21-03<br>P7-141 | txtVal="bad" مفترض فشله، مع تقرير و Foundation متاحين لاحقاً في بيئة مأذونة.<br>**الإجراء:** قارن preview/print في D و QAndroid بالصفر الحقيقي، وارصد BondVal ومدخل الكلمات قبل الإرسال. | فشل القراءة يوقف التقرير برسالة مستقلة؛ لا word-input0 مع raw BondVal غير صالح.<br>**not-executed** |
| P7B21T-06 / finding-specific<br>FE7B21-03 / INV7B21-03<br>P7-141 | قيمة 12.5 ناجحة بثقافة معتمدة، وصفر إن أجازه المالك، و whitespace.<br>**الإجراء:** قارن valid و zero و empty منفصلة، ولا تجعل نجاح حفظ سابق شرط تحقق يغطي Print المستقل. | نفس المبلغ الناجح يصل للرقم والكلمات؛ empty يرفض، والصفر الحقيقي لا يمثل فشل parse.<br>**not-executed** |
| P7B21T-07 / contract-or-retained-root<br>FE7B21-04 / INV7B21-04<br>P7-034 | قيم 19.999 و 19.99 و 20.00 ودقتان مفترضتان 2 و 3 دون اعتماد سياسة.<br>**الإجراء:** تتبع formatted primary و raw fallback و HR قبل فصل الكسر؛ Python ليس دليلاً لتنفيذ VB. | تمثل الكلمات المبلغ النهائي المقرر بدقته، لا بادئة كسر خام؛ يسجل مصدر كل caller.<br>**not-executed** |
| P7B21T-08 / contract-or-retained-root<br>FE7B21-04 / INV7B21-04<br>P7-034 | ثقافات dot/comma وفاصل آلاف وشاهد primary N2 لنفس المقدار.<br>**الإجراء:** راجع format→parse→split والرفض عند اختلاف الثقافة دون إعادة عد 034. | لا يدعى اختبار ثقافة من toy؛ يميز formatted عن raw وتبقى 034 مفتوحة حتى قبول مستقل.<br>**not-executed** |
| P7B21T-09 / contract-or-retained-root<br>FE7B21-05 / INV7B21-05<br>P7-035 | codes4/12/13 و 2 أرقام فروع محلية، وتعريف SDK مطلوب لاحقاً.<br>**الإجراء:** قارن عائلتي major/minor للغتين ثم اربطهما بالعقد دون تخمين enum. | تطابق الهوية للمدعوم ورفض unknown واضح، لا fallback إلى عملة أخرى.<br>**not-executed** |
| P7B21T-10 / contract-or-retained-root<br>FE7B21-05 / INV7B21-05<br>P7-035 | code2 شاهد، مع unknown و 15 و zero دون دقة مفترضة.<br>**الإجراء:** افصل الاتساق الجزئي عن grammar ودعم JPY وثلاث خانات أو صياغة الصفر. | لا يعمم case2 على العملات؛ غير المحسوم له مالك وحد ولا يصبح قاموساً معتمداً.<br>**not-executed** |
| P7B21T-11 / contract-or-retained-root<br>FE7B21-06 / INV7B21-06<br>P7-034;P7-035 | Net خام بدقة زائدة و N2/N3 وفرعا InvoiceItems/Items.<br>**الإجراء:** قارن مصدر Arabic/English في كل branch ودقة الرقم المعروض دون SDK execution. | يستعمل الفرع المبلغ نفسه المقرر للعرض والتفقيطين مع هوية عملة واحدة.<br>**not-executed** |
| P7B21T-12 / contract-or-retained-root<br>FE7B21-06 / INV7B21-06<br>P7-034;P7-035 | InvoiceItems فارغة و Items فارغة أو مستبعدة بـ ProductId موجب.<br>**الإجراء:** ميز عدم بناء row من بلوغ converter؛ عد مواقع النداء لا الصفحات أو الميزات. | لا ينسب تحويل أو طباعة لفرع لم يبن صفاً، وتبقى عقود SDK والقالب خارج المراجعة المحلية.<br>**not-executed** |
| P7B21T-13 / contract-or-retained-root<br>FE7B21-07 / INV7B21-07<br>H7B21-03 | خريطة Doctype→setting منقحة و key13 مشترك مع ReceiptTypes مختلفة.<br>**الإجراء:** راجع الكاتب والقارئ والمستدعين الخمسة قبل أي ادعاء خلط نوع. | يثبت المفتاح المقصود بعقد؛ اختلاف ReceiptType و Inv_Id وحده لا ينشئ نتيجة جديدة.<br>**not-executed** |
| P7B21T-14 / contract-or-retained-root<br>FE7B21-07 / INV7B21-07<br>H7B21-03 | غياب setting وفشل DB و Currency NULL كحالات مميزة.<br>**الإجراء:** افصل default مقصوداً من failed lookup في مراجعة لاحقة دون SQL الآن. | لا يعتمد فشل المصدر كعملة 1 صامتة إلا بعقد يبين السلوك؛ لا اعتماد مالي من fallback.<br>**not-executed** |
| P7B21T-15 / contract-or-retained-root<br>FE7B21-08 / INV7B21-08<br>H7B21-01 | عملة HR مقررة و SalaryPay readonly وإضافة/خصم بقيمة txtVal.<br>**الإجراء:** قارن القيمة الممررة ومصدرها بعقد HR قبل اقتراح تغيير العملة الافتراضية. | تتبع عملة الصرف المقررة ولا يفرض تعدد عملات من SDK أو البلد؛ يبقى 004/006 مستقلين.<br>**not-executed** |
| P7B21T-16 / contract-or-retained-root<br>FE7B21-08 / INV7B21-08<br>H7B21-01 | صافي 0 أو سالب حسب سياسة HR لاحقة وشاهد موجب بسيط.<br>**الإجراء:** قارن domain والرفض ومصدر readonly دون حكم على صحة الرواتب أو WPF timing. | قرار السالب والصفر والعملة صريح؛ لا يعمم failed manual entry من D/QAndroid على كل SalaryPay.<br>**not-executed** |
| P7B21T-17 / contract-or-retained-root<br>FE7B21-09 / INV7B21-09<br>H7B21-01 | مدين 120/دائن 20 وعكسهما، وتعادل 20/20.<br>**الإجراء:** قارن مقدار 100 والتفقيط و BalanceType، مع توثيق أن المصدر مجموعا الشاشة. | يحفظ المقدار والجانب حسب العقد؛ لا يشترط minus إذا كان العرض magnitude+side مقصوداً.<br>**not-executed** |
| P7B21T-18 / contract-or-retained-root<br>FE7B21-09 / INV7B21-09<br>H7B21-01 | رصيد نصي بمسافات و N2/N3 و failed parse مصطنع.<br>**الإجراء:** افصل فشل التنسيق عن صفر حقيقي وحدود SafeParse بالمركز دون حكم GL. | لا يعتمد صفر SafeParse مبلغاً صحيحاً بلا health؛ الهوية المحاسبية خارج شريحة التفقيط.<br>**not-executed** |
| P7B21T-19 / contract-or-retained-root<br>FE7B21-10 / INV7B21-10<br>H7B21-05 | عقد منتج 0.00 وحقل دائن غير صفري مطلوب من المالك.<br>**الإجراء:** تتبع إنتاج Balance1/2 في جزء لاحق مسمى قبل قبول selector. | يثبت معنى الانتقاء بعقد المبلغ والتنسيق، ويسجل نطاق كل منتج قبل الحكم على الرصيد.<br>**not-executed** |
| P7B21T-20 / contract-or-retained-root<br>FE7B21-10 / INV7B21-10<br>H7B21-05 | أمثلة 0 و 0.000 و 0,00 ومسافات، لا نتائج WPF مثبتة.<br>**الإجراء:** تحقق أي منتج يمكنه إخراج كل صيغة واستبعد غير المسند بدلاً من تعميم العيب. | لا finding أو قبول من تغيير النص في toy؛ كل حالة معلقة لها مالك وحد ومتابعة.<br>**not-executed** |
| P7B21T-21 / contract-or-retained-root<br>FE7B21-11 / INV7B21-11<br>H7B21-01 | قائمة مجال معتمدة:0 و-0 والسالب وغير المنتهي وموجب حدي.<br>**الإجراء:** راجع typed precondition ثم قارنه بالكلمات أو الرفض في قبول لاحق مأذون. | لا كلمات مالية صحيحة ظاهرياً خارج المجال؛ zero و negative لهما دلالة أو رفض معلنان.<br>**not-executed** |
| P7B21T-22 / contract-or-retained-root<br>FE7B21-11 / INV7B21-11<br>H7B21-01 | نص signed مفترض-000000000001 وشاهد unsigned12 دون ادعاء Format.<br>**الإجراء:** اعزل البرهان ASCII عن Format/Val الفعليين وعن دلالة BalanceType. | تذكر فروض المثال؛ لا نتيجة سالب مطبوعة أو finding سياسة غير مسندة.<br>**not-executed** |
| P7B21T-23 / contract-or-retained-root<br>FE7B21-12 / INV7B21-12<br>H7B21-04 | تعريف enum أصلي منقح و DB codes اصطناعية معروفة.<br>**الإجراء:** قارن display/save/read والـ numeric cast بعقد القيمة والترتيب والإصدار. | تثبت الهوية أو عدمها بدليل SDK؛ fixture المخترع لا يحكم على التطبيق.<br>**not-executed** |
| P7B21T-24 / contract-or-retained-root<br>FE7B21-12 / INV7B21-12<br>H7B21-04 | قائمتان افتراضيتان[1,2,8] و[0,1,2] ليستا تعريف AuditorAPI.<br>**الإجراء:** اعرض الحالتين كشاهدين واطلب mapping دون تحميل أو تنفيذ DLL. | يبقى الاستنتاج مشروطاً؛ لا finding أو ترحيل بافتراض أن كل enum يبدأ 0 أو 1.<br>**not-executed** |
| P7B21T-25 / contract-or-retained-root<br>FE7B21-13 / INV7B21-13<br>H7B21-03 | قائمة callers تشمل qualified والغير مؤهل والمكون الخارجي حسب المالك.<br>**الإجراء:** قارن توكنات الاسم بالربط الدلالي في جزء لاحق دون تشغيل DLL. | كل قدرة مزعومة لها input/source/output أو سبب استبعاد؛ لا غياب من grep وحده.<br>**not-executed** |
| P7B21T-26 / contract-or-retained-root<br>FE7B21-13 / INV7B21-13<br>H7B21-03 | ameral كمرشح بديل بعقد domain/culture/grammar غير معتمد.<br>**الإجراء:** اكتب معايير مقارنة وقاعدة فشل دون استيراد التطبيق أو تبديل المحول. | لا يعد وجود helper أو عدم متصل مكتشف إصلاحاً أو غياب ميزة؛ تبقى 034/035/139.<br>**not-executed** |
| P7B21T-27 / contract-or-retained-root<br>FE7B21-14 / INV7B21-14<br>H7B21-05 | مقادير اصطناعية 100/15/115 وعقد يحدد الأساس والضريبة والإجمالي ومعنى txtVal/txtNetVal/BondVal؛ لا نفترض تسميات gross/net من أسماء الحقول.<br>**الإجراء:** قارن BondVal و netVal و ArabicLetter ومصادرها بلا قالب أو SQL منفذ. | يمثل التفقيط بند المبلغ المعلن؛ لا يفترض أنه BondVal من الاسم ولا تعتمد الضريبة.<br>**not-executed** |
| P7B21T-28 / contract-or-retained-root<br>FE7B21-14 / INV7B21-14<br>H7B21-05 | فشل currency lookup واستثناء converter ونجاحه حالات منفصلة.<br>**الإجراء:** راجع catch N2 ومعنى health و outcome المطلوب لحقل ArabicLetter. | لا يختفي فشل الكلمات كأرقام بلا علامة حسب العقد؛ catch وحده ليس نجاح تفقيط.<br>**not-executed** |
| P7B21T-29 / contract-or-retained-root<br>FE7B21-15 / INV7B21-15<br>H7B21-02 | manifest منقح يوضح aliases/types/currency/words/side لكل قناة.<br>**الإجراء:** قارن عقد المستهلك بالخواص والإسنادات دون تحميل REPX أو UtilitiesProj. | كل حقل له أصل ومعنى ونوع و fallback؛ اختلاف الاسم وحده لا يثبت غياب ميزة.<br>**not-executed** |
| P7B21T-30 / contract-or-retained-root<br>FE7B21-15 / INV7B21-15<br>H7B21-02 | قالب لا يستعمل currency وآخر يربطه بـ alias أو نص ثابت خارجي.<br>**الإجراء:** افصل 140 المحلي عن الأثر المشروط بالقالب، واحفظ حدود preview/dispatch. | لا يدعى تعويض القالب أو فراغ مطبوع دون دليل؛ لا صور أعمال أو طابعة.<br>**not-executed** |
| P7B21T-31 / documentary<br>FE7B21-16 / INV7B21-16<br>H7B21-06 | OWN310/raw311CRLF و 583hash و G195 ومخزون 827.<br>**الإجراء:** قارن كل الحقول والبايتات و hashes مع تحويرات ذاكرة اصطناعية لا تكتب القديم. | كل القديم و ALLnext_phase/evidence و G01–195 وأصل التطبيق ثابت؛ 139–141 و G196–200 فقط جديدة.<br>**not-executed** |
| P7B21T-32 / documentary<br>FE7B21-16 / INV7B21-16<br>H7B21-06 | تغيير hash أو BOM/CRLF/evidence/order في نسخ ذاكرة مصطنعة.<br>**الإجراء:** تأكد أن المدقق يرفض كل تحوير ويبقي هوية capture الأصلية. | تعديل flags أو إعادة checks عند HEAD التسليم لا يسمى حفظاً؛ الفحص يفشل قبل success.<br>**not-executed** |
| P7B21T-33 / documentary<br>FE7B21-17 / INV7B21-17<br>H7B21-06 | RS14 من B20 و SP3 و HQ6 والقدرة التالية المقترحة.<br>**الإجراء:** راجع الهوية و rowSHA والعقود والأثر عند غياب input وحدود تقدم barcode/words. | لكل بقية تصرف مملوك؛ 14 صفاً ليست 14 موافقة و 12 نداء مؤهلاً ليست كل callgraph.<br>**not-executed** |
| P7B21T-34 / documentary<br>FE7B21-17 / INV7B21-17<br>H7B21-06 | ادعاء إغلاق 7B من 24path أو 477scan أو ثلاثة splits.<br>**الإجراء:** راجع أسباب رفض overclaim وسم القدرة التالية بمدخل ومخرج وسبب وحد خروج. | لا نسبة أو تقدير جلسات أو نقل إلى C؛ لا تفقد البقية هويتها أو عقد مالكها.<br>**not-executed** |
| P7B21T-35 / documentary<br>FE7B21-18 / INV7B21-18<br>H7B21-06 | parser فعلي B21 وقواعد B20/B19/B18 و API defaultB15.<br>**الإجراء:** اختبر الحالي بمجموعته الجديدة و ALL32 B20 بطفله دون تعديل أو skip. | defaultB21 والقديم OWN310 بحد B20؛ تعاد objects بعد نجاح/استثناء بلا global patch أو overlay.<br>**not-executed** |
| P7B21T-36 / documentary<br>FE7B21-18 / INV7B21-18<br>H7B21-06 | 36 خطة أعمال not-executed و stdout وتواريخ/commits مميزة.<br>**الإجراء:** راجع strict false/int-zero وعدم بدء C/8 أو توليد إذن ERP من next_phase8. | stdout خام في sink حصري وبـ captureHEAD الحقيقي و pendingfalse حقيقياً؛ لا flag edits أو selfhash أو قبول متنكر.<br>**not-executed** |

## 6. هوية المصدر والحفظ والأرشفة

تحمى **583 مادة** سابقة، وكل **310 صفوف** بكل حقل وتصنيف و`ALLnext_phase/evidence` وبادئة raw ذات **311CRLF** وبدون BOM، و**G01–195** و**827 أصل تطبيق/29,128,444 بايت**. لا extensions أو تحرير تقارير أو أدوات أو اختبارات أو checks تاريخية؛ خمسة مسارات مشتركة فقط تتقدم، والباقي أسماء B21 جديدة. التراكمي **313 مفتوحة بلا معالجة**:2Critical/181High/129Medium/1Low؛ 275confirmed/31potential/7repository-gap؛ المرحلة 7=141 نتيجة لا مقام ميزات. تضاف G196–200 توصيات لا خمس نتائج أخرى.

- [frozen310](evidence/findings-through-07B20.csv) SHA256=`18b353c138536a98b3aa426bf2e03662df6133d3acccb034232918ed4dcb24d0`؛ [exactB20indexes](evidence/shared-indexes-through-07B20.json) SHA256=`2e5fdc450260f88b69b3172161237681fd7be0d58f45ae7bd7cc7ae76c4f3565`؛ [provenance583](evidence/provenance-07B21.json) SHA256=`4ca4356932a6c1689e3af6558b545697d6e35f4a7d491baf736f88ca2324a175`.
- [witnessB21](evidence/amountword-contract-witnesses-07B21.json)34538 بايت/SHA256=`2129f522533abbbea9e455ebdd3a61d047f02f24bffe7448d1e800d140e99b42`، capture stdout مباشر دون تعديل أو إعادة كتابة.
- [checksB20 الأصلي](evidence/checks-07B20.json)170759 بايت/SHA256=`93667de46adad6443573ac1822db56440678a86d28ee6fe26793e880bd57f766`؛ genuinecheckout=`ac20e3104f84fefbc62779e22d2c9b9621802340`/310/530/21/errors[]/pendingfalse، لا deliveryc2c895d. B19 السابق=`ee393a7`وقت capture لا ac20e31. لا تعاد checks قديمة عند HEAD التسليم.
- [stdoutB21](evidence/checks-07B21.json) يلتقط stdout CLI الحقيقي حصرياً في `xb` دون تحويل JSON أو placeholder أو تعديل flags أو selfhash. فتح sink قبل العملية يجعل حالة وجود الملف حقيقية وقت capture؛ لا نسخ لخرج سابق أو تغيير لعلم pending.

source10ba/entry-completedB20push-c2c895d/genuineB20stdout-ac20e31 هويات مستقلة. فرق ساعة البيئة عن مرجع 16 نوفمبر مسجل لا runtime؛ لم تتغير بصمة تطبيق. تصويب B10 الإضافي 10vs120 محفوظ دون إعادة كتابة الأرشيف. **7B/7 جزئيتان؛ R4f/7B22 مقترح؛ 7C لم تبدأ؛ 8 غير مأذونة.**
