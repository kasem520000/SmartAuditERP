# التحقق التوثيقي وخطط القبول — 7B18

مرجع التدقيق المعلن **2026-11-16 UTC**، ومصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B18 يلي دفع B17 المكتمل `12d2e4b1bc566a860643b8459b16cbc85a6d2c3d` بجميع **500 ملف تدقيق**. ساعة التجميد المرصودة `2026-11-19T02:53:08.853620+00:00` منفصلة عن المرجع وليست تشغيل تطبيق.

**7B/7 جزئيتان؛ R4b سُلّم بحدوده، و R4c/7B19 مقترح؛7C لم تبدأ؛8 غير مأذونة ولم تبدأ.** لا بناء أو تشغيل ERP أو C#/SQL/VB/WPF/SDK/REPX/Office/COM، ولا مفسر أو مزود أو جهاز أو طابعة أو تصدير أعمال أو shell للتطبيق. لا بيانات أعمال حقيقية أو أسرار أو إصلاح أو قبول أو قياس تشغيلي. Python/Git لأدوات الوثائق فقط؛ `next_phase=8` ليس إذناً.

[النتيجة](PHASE-07B18.md) · [عقود المتصلين](CALLER-REQUEST-CONTRACTS-07B18.md) · [التحقق والخطط](VALIDATION-07B18.md) · [المتبقي](PHASE-07-REMAINING-07B18.md) · [scope29](review-scope-07B18.csv) · [السجل](findings.csv) · [provenance495](evidence/provenance-07B18.json) · [stdoutB18](evidence/checks-07B18.json)

## 1. فصل التنفيذ التوثيقي عن القبول

نجاح مدقق الوثائق يعني مقارنة البصمات والصفوف والروابط وحدود الأسطر وإعادة أمثلة مستقلة وملاحظات نصية، لا تنفيذ ERP. [الشاهد](evidence/caller-request-witnesses-07B18.json) يحوي 12 نموذجاً مستقلاً و 12 فحصاً نصياً و 43 شريحة قراءة. بصمته `86eb7a2aa3b66a9f5fa2726a81d45c36a667099366c04d8ed1a9f517c03b6060` وحجمه 41,190 بايت. بُحث 477 C# لاكتشاف 19 نداءً في 10 ملفات؛ هذا بحث lexical لا 477 body review أو كل callgraph.

نجح الـ CLI الحالي فعلياً: **462 حالة مدقق عبر 19 مجموعة، errors=[]**، منها 28 حالة جديدة و 434 سابقة محفوظة. نجحت **23 وضعية تاريخية** بمدخلاتها OWN:through2–6 ثم A و B1…B17؛ أعاد B17 سجل 300 و 434 حالة/18 مجموعة، لا 302 الحالي. وأثبتت أداة baseline بقاء **827 ملفاً أصلياً/29,128,444 بايت** دون تغيير، مع XML0 و XAML mismatch0؛ لم يتوفر dotnet ولم يُبنَ التطبيق. حُفظت 495 مادة و 3 تجميدات و 300 صف و G01–180 حرفياً؛ كلها فحوص وثائق لا قبول ERP أو إصلاح أو قياس.

stdout الحالي يُلتقط مباشرة إلى ملف جديد مرة واحدة، ولا يعاد بعد commit/push. لا flags مصطنعة أو self-hash للـ stdout نفسه؛ فتح ملفه الحصري وتحويل stdout إليه هو أول كتابة فعلية، لا نسخ من تشخيص معدل أو تغيير pending يدوياً.

## 2. الأوامر الآمنة وحدودها

```bash
python3 -B docs/audit/tools/validate_audit.py
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B18
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B17
python3 -B docs/audit/tools/check_caller_request_witnesses.py
python3 -B docs/audit/tools/test_caller_request_audit_validator.py
python3 -B docs/audit/tools/collect_baseline.py --verify
git -c core.whitespace=cr-at-eol diff --check
```

الـ CLI الفعلي `build_cli_parser` يختار B18/current302، و main البرمجي B15 باقٍ للتوافق. PHASE7_CURRENT_CLI اسم API تاريخي B17 فعال كقاعدة لـ PHASE7_LIVE_CLI، لا parser اليوم. اختبار 28 يثبت أن entrypoint يستعمل parser الفعلي، واختبار 27 يقرأ defaultB18 وخيارات B17/B16. لم تُعدّل الاختبارات المحمية لإجبارها على المرور، ولا أضيف dead code لإرضائها.

23 وضعية تاريخية هي through2–6 ثم A و B1…B17، كل منها OWN rows/indexes. B10…B17 تحصل أيضاً على rawCRLF الدقيقة عند المسار المنطقي في الذاكرة؛ B17=300 صف/301CRLF، لا live302 أو 299 الخاصة بـ B16. تعاد كل الهويات عند النجاح والاستثناء والتداخل، بلا global Path patch أو disk overlay أو protected edit أو rebaseline أو إعادة كتابة الأرشيف.

## 3. ما يُتحقق منه توثيقياً

- 495 مادة تاريخية وثلاثة freezes ببصماتها، و 827 مساراً/بصمة أصلية. كل 300 صف وكل ALLnext_phase/evidence/rawprefix و G01–180 حرفية؛ الجديد 129/130 فقط، وصفر extensions، و G181–184 توصيات.
- CL19 يطابق path/start/end/args/hash بالترتيب في 10 ملفات، ويفصل 10 أوامر عامة و 7 حالات نوع و 1 مطابق و 1 حذف ID. GE10=8 تفصيلية pre-dialog و 2 تجميعية؛ لا يفرض توقيت WPF.
- FE14↔INV14↔T24 ربط عكسي ودليل وجذر متطابق، و RC4 يشير لاتحادات FE الدقيقة. المعايير والخطط متمايزة، لا عبارات قبول مكررة.
- RS14 ترتبط بـ upstreamId/rowSHA/contractIds من B17. لكل بقية مالك ومدخل منقح وأثر وخطوة ومعيار، لا 14 موافقة. H/Q6 لم تُجب، و SP3 مفصلة بسبب ونطاق، وستة محاور 7C لم تبدأ.
- فحوص source-reference/index/link/syntax/self-tests تخص الوثائق فقط. أثر SelectedIndex و party_filter نموذج يدوي مشروط، لا.NET selection منفذة. التصويب الإضافي B10،10 مقابل 120، محفوظ؛ لا تصديق لكل نثر قديم.

## 4. خطط القبول — كلها غير منفذة

خمس خطط خاصة بعلة النوع 129 وخطتان خاصتان بحذف المعرف 130؛ والبقية انحدار أصل أو عقد عابر أو بوابة توثيق وإذن. وجود خطة بوابة لا يعني تنفيذها؛ فحص التناسق المنفذ له سجل stdout مستقل. المتطلبات والإجراءات وضوابط السلامة الكاملة في[CSV24](evidence/acceptance-tests-07B18.csv).

| المعرف | السيناريو / الشروط | الإجراء اللاحق | معيار القبول المحدد | FE / الجذر / الحالة |
| --- | --- | --- | --- | --- |
| P7B18T-01 | مورد خالص 2 عند caller يرسل 1 — طرف S id22/type2 وطرف C id11/type1 وحركتان لنفس المخزن والصنف؛ lookup جاهز ومصدر ناجح. | لاحقاً وبإذن قارن طلب الطرف من SalePurch/PurchInv بقائمة الطفل وشرط cust_id؛ لا SQL الآن. | لا يسقط معرف المورد ولا يختفي predicate عند خطأ النوع: نقل مطابق أو رفض واضح، لا all-party صامت. | FE7B18-01 / P7-129 / not-executed |
| P7B18T-02 | عميل POS خالص 1 يرسل 2 — اختيار id11/type1 من frmSrchClient.Type1 قبل أمر الحركة، دون تنفيذ دفع. | لاحقاً تتبع Invoic.Customer ونوعه وقائمة الطفل وقارن بحركة المورد الأسبق وحركة العميل المطلوبة. | يحافظ الطلب على نطاق العميل المختار؛ لا يستبدله بقائمة موردين 2 أو يوسع النطاق دون إعلان. | FE7B18-01 / P7-129 / not-executed |
| P7B18T-03 | الطرف المشترك 3 شاهد إخفاء — طرف id33/type3 مع شاهدين من 1/2 الخالصين في بيئة اصطناعية مأذونة لاحقاً. | قارن kind1 و kind2 للمعرف المشترك ثم استبدله بطرف خالص؛ لا تعتمد 3 كحالة قبول وحيدة. | تتطابق حالة 3 المعلنة دون طمس عيب 1/2؛ تبقى الشواهد وحدودها في التقرير. | FE7B18-01 / P7-129 / not-executed |
| P7B18T-04 | InputOutput5 مقابل 4/14 — قاموس 4/5/14 من الأب ومعرفات مؤهلة من 1/2؛ المخزن والترتيب ثابتان. | قارن مصدر الطرف مع arg4 عبر 4/5/14، واعزل كل component لئلا تختلط الأسباب. | يصل 1 في 5 و 2 في 4/14 أو يرفض النمط وفق مواصفة؛ لا const2 لكل الأنماط. | FE7B18-01 / P7-129 / not-executed |
| P7B18T-05 | عدم تطابق lookup لا يوسع طلباً موجباً — معرف موجب غير موجود في القائمة المطلوبة؛ حالات نجاح فارغ وفشل تحميل منفصلة. | خطط لحالات النوع الخاطئ والمعرف غير الموجود وفشل المصدر، ولا تفسر أياً منها بأنه اختيار الكل. | الطلب المحدد لا ينفذ all-party عند SelectedIndex=-1؛ invalid/failed منفصلتان عن empty. | FE7B18-01 / P7-129 / not-executed |
| P7B18T-06 | أمر العميل المربوط فعلاً يحتفظ بالمعرف — frmInvInOutput فيه طرف موجب وصنف ومخزن صالحان؛ label العميل مربوط بـ StripLastItem. | لاحقاً انقر label العميل لا المعالج المستنتج من اسمه وسجل الوسائط الأربع. | لا يرسل أمر الطرف clientId=-1 مع اختيار موجب؛ يطابق الطلب هوية الطرف أو يرفض بوضوح. | FE7B18-02 / P7-130 / not-executed |
| P7B18T-07 | إصلاح النوع لا يستعيد المعرف المحذوف — عينة 130 نفسها؛ النوع صحيح، والمتغير الوحيد clientId بين-1 ومعرف الأب. | اعزل أمر المادة العام عن أمر الطرف ثم قارن المعرف الموجب؛ لا تنفيذ SQL أو واجهة الآن. | يبقى sentinel مشروعاً لأمر المادة العام، ولا يتحول أمر الطرف إليه ضمنياً؛ إصلاح 129 لا يعلن إصلاح 130. | FE7B18-02 / P7-130 / not-executed |
| P7B18T-08 | storeId تحت علم الكل 122 — ثلاث حركات لنفس الطرف في مخازن 9/5/8 بأزمنة مختلفة؛ المطلوب مخزن 5. | بعد عزل PartyRef قارن chkAll و predicate المخزن في بيئة لاحقة؛ لا تصحيح فعلي الآن. | قيد المخزن 5 لا يتحول إلى كل المخازن؛ تغيير النوع أو ASC/DESC ليس بديلاً عنه. | FE7B18-03 / P7-122 / not-executed |
| P7B18T-09 | latest059 بعد تثبيت النطاق — حركتان للصنف والطرف والمخزن نفسيها بزمنين مختلفين، ثم عينة تعادل زمني. | قارن TOP1 ASC بالـ latest المعتمد وسجل مفتاح تعادل حتمي بدل ترتيب DB عرضي. | يُختار الأحدث داخل النطاق بقاعدة تعادل معلنة؛ لا خلط بينه وبين الرصيد الكامل. | FE7B18-04 / P7-059 / not-executed |
| P7B18T-10 | ShowResult قبل ShowDialog وحد Ready — ثمانية مداخل GE تفصيلية و Window_Loaded مع أصول DateTimeBox/SDK وسلوك Loaded موثق من المالك. | لاحقاً وبإذن تتبع الإنشاء والتهيئة والقراءة والعرض و Loaded؛ راقب الفرع والتاريخ و health دون أعمال حقيقية. | لا قراءة قبل ReadyRequest معتمد، ولا تعرض UI معايير مختلفة عن نسخة النتيجة؛ لا توقيت WPF مفترض من النص. | FE7B18-05 / P7-045;H7B18-03 / not-executed |
| P7B18T-11 | InvPurch المطابق والنوع 3 — مورد 2 موجب وبقية العقد معزولة؛ InvPurch يرسل 2. | احتفظ به كشاهد مقابل وقارنه بالنوع 3 دون افتراض إصلاح المخزن أو الترتيب. | يمر المعرف والنوع مطابقين؛ تبقى 059/122 معلنتين ولا اعتماد عام من شاهد واحد. | FE7B18-06 / P7-129 / not-executed |
| P7B18T-12 | تبديل InvType في الواجهات العامة — InvType1 مقابل 2 في المحررات المسماة، مع مصفوفة دعم الأنماط من المالك. | قارن مصدر lookup و arg4 لكل نمط معتمد وقيد الحكم بالأنماط المتاحة فعلاً. | نفس سياسة النوع تنتج قائمة الأب وطلب الطفل؛ unsupported صريحة لا استدلال من اسم الشاشة. | FE7B18-07 / P7-129 / not-executed |
| P7B18T-13 | اختيار POS لا يثبت كل الدفع — اختيار Type1 من مسار آجل أو SearchforClient، دون جهاز أو دفع أو حفظ. | راجع معرف Invoic.Customer وصلاحيته عند طلب الحركة في بيئة لاحقة فقط. | معرف ونوع POS من مصدر واحد؛ لا معرف افتراضي أو صفري أو مجهول يُعامل كطرف محدد. | FE7B18-08 / P7-129 / not-executed |
| P7B18T-14 | أهلية الطرف في InputOutput — النمطان 4/14 موردون و 5 عميل؛ مفاتيح المعرفات وسياسة support معلومة. | ابن جدول source→kind→command→sink للأنماط المختارة دون التوسع إلى أنواع غير محددة. | تنقل كل حالة دورها الصحيح أو تعلن عدم الدعم؛ label المورد ليس بديلاً عن مصدر النوع. | FE7B18-09 / P7-129 / not-executed |
| P7B18T-15 | نسب 19 موضعاً لا مقام ميزات — inventory827 و CL19 و GE10 ونمط البحث المعلن؛ المصدر الأصلي ثابت. | أعد البحث في 477 C# خارج bin/obj وطابق path/start/end/args/hash وبالترتيب؛ فك cp1256 دون إعادة كتابة. | كل موضع من 19 مرة واحدة في 10 ملفات؛ لا AST/callgraph كامل أو 477 مراجعة body أو ترقية 455 metadata. | FE7B18-10 / H7B18-06 / not-executed |
| P7B18T-16 | التجميعي مقابل التفصيلي وأصل 058 — المدخلان العامان لـ PurchInv/InvInOutput وعقد التجميعي السابق. | افصل اختيار ItemId عن طلب الطرف وتتبع الفرع الفارغ 058 دون تشغيل. | لا يستورد حكم pre-load للمدخلين؛ إصلاح التجميعي لا يعيد النوع أو المعرف المفقودين في LP. | FE7B18-11 / P7-058 / not-executed |
| P7B18T-17 | DocumentRef ليس PartyRef — مستندات اصطناعية بأرقام محلية مكررة وفرع و GlobalID و source/type مع مواصفة الفتح المدعوم. | قارن الفتح التفصيلي بالاسم والرقم المحلي مع GlobalID في inventory؛ أبق بقية Navigate والحفظ split صريحاً. | الفتح مرتبط بمرجع عالمي ونوع وفرع وصلاحية معتمدة؛ لا قبول لكل navigator من نداء عالي المستوى. | FE7B18-12 / P7-061;H7B18-03 / not-executed |
| P7B18T-18 | نسب 14 بقية دون قبول خارجي — RS14 المجمدة من B17 مع rowSHA و H/Q وملاكها، بلا موافقة مفترضة. | طابق كل RS و upstream و hash؛ وثق التقدم المحلي في SP01 واستبقاء العقود و SP02/SP03. | لا عنصر مفقود ولا 14 موافقة؛ لكل بقية مالك ومدخل منقح وأثر وخطوة ومعيار خروج. | FE7B18-13 / H7B18-06 / not-executed |
| P7B18T-19 | R4b محدود و R4c مقترح — SP01–03 وخطة B19 وستة محاور C والحصر المعلن، لا نسبة من عدد الملفات. | تحقق من أسباب الخارج: بقية Navigate/Print والقدرات والتفقيط والباركود؛ لا بدء C ضمني. | لا اكتمال R4/7B من 19/10 أو 29 مساراً؛ كل split إضافي مسبب بنطاق لا وعد جلسة أو مدة. | FE7B18-13 / H7B18-06 / not-executed |
| P7B18T-20 | ALL300 والبادئة الخام ونتيجتان فقط — frozen300 و 301CRLF ومخطط السجل؛ الجديد 129/130 بلا امتدادات. | قارن كل حقول 300 و ALLnext_phase/evidence والبادئة الخام ثم الصفين الجديدين. | كل التاريخ حرفي والجديد 302 بلا BOM وبـ 303CRLF؛ لا تغيير تصنيف أو متابعة أو دليل قديم. | FE7B18-14 / H7B18-06 / not-executed |
| P7B18T-21 | حفظ 495 و G180 و 827 وثلاثة freezes — لقطات الدخول وبصمات 495 و G01–180 و 827 مساراً/بصمة وثلاثة تجميدات. | قارن الأرشيف وصفوف G حرفياً؛ لا تكتف بوجود substring ولا تعيد baseline. | تتطابق بصمات 495/827/3 وصفوف G180؛ تضاف G181–184 كتوصيات فقط. | FE7B18-14 / H7B18-06 / not-executed |
| P7B18T-22 | B17 OWN300 وهوية stdout — source10ba و entry12d2e4b و genuineB17stdoutde0e7cf، مع 300 صف وفهارسها الحرفية. | شغّل B17 الصريح في ذاكرة معزولة بـ 300 و raw301CRLF وفهارسه؛ استعد الهويات في النجاح والخطأ والتداخل. | لا live302 أو OWN299 من B16؛ لا global Path patch أو disk overlay أو تعديل محمي أو rebaseline أو كتابة أرشيف. | FE7B18-14 / H7B18-06 / not-executed |
| P7B18T-23 | CLI الفعلي B18 وتوافق B17/B16 و API B15 — preset B16 قاعدة، و PHASE7_CURRENT_CLI واجهة توافق B17؛ build_cli_parser الحالي يختار B18. | اختبر parser المستخدم فعلاً في entrypoint، وتشغيل defaultB18 وخيار B17 الصريح؛ لا اختبار preset قديم دليلاً على default اليوم. | default الفعلي B18 و historical B17 متاح و main API يبقى B15؛ لا dead code أو تعليق مصطنع لإنجاح اختبار محمي. | FE7B18-14 / H7B18-06 / not-executed |
| P7B18T-24 | stdout حقيقي لا قبول ERP — أدوات الوثائق والشاهد وأوامر التحقق الحالية والتاريخية، بلا placeholder ناجح. | احفظ stdout الجديد مباشرة مرة بعد فحصه وقبل commit/push؛ التشخيص بعد الدفع خارج الأرشيف. | كل 24 خطة not-executed؛ لا ERP/SQL/WPF أو إصلاح أو قياس أو بدء 7C/8 من نجاح المدقق أو الدفع. | FE7B18-14 / H7B18-06 / not-executed |

## 5. حدود الإذن وصحة النتائج

لا app import/build أو SQL/WPF أو إعداد مزود أو جهاز أو طباعة أو Office أو business export. لا اختبارات ضريبية أو مالية أو جلسات إنتاج أو إصلاح أو قياس. فروق نموذج أهلية الطرف لا تعتمد كل المجاميع أو الرصيد أو نجاح المصادر. أي قبول لاحق يحتاج مواصفة وبيئة اصطناعية وإذناً صريحاً، لا مفاتيح أو بيانات أعمال في الدردشة. **7B/7 جزئيتان؛7C لم تبدأ؛8 غير مأذونة.**

## 6. نتائج الأوضاع التاريخية المنفذة

[السجل الموجز](evidence/historical-mode-verification-07B18.json) نتاج 23 عملية CLI فعلية ذات exit0 و errors=[] و 827 بصمة و ERP/SQL0. يحفظ الأوامر وبصمات stdout التي لوحظت؛ التشخيص الكامل خارج Git، وليس إعادة إنتاج byte-for-byte للأرشيفات القديمة. null في تجميع الحالات يعني أن التقرير القديم لم ينشر ذلك التجميع، **لا أنه لم ينفذ فحوصاً**.

| الوضع | السجل OWN | النتائج المفتوحة | الحالات/المجموعات المجمعة إن نشرت | النتيجة الوثائقية |
|---|---|---|---|---|
| phase2 | [evidence/findings-through-02.csv](evidence/findings-through-02.csv) | 49 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| phase3 | [evidence/findings-through-03.csv](evidence/findings-through-03.csv) | 74 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| phase4 | [evidence/findings-through-04.csv](evidence/findings-through-04.csv) | 106 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| phase5 | [evidence/findings-through-05.csv](evidence/findings-through-05.csv) | 137 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| phase6 | [evidence/findings-through-06.csv](evidence/findings-through-06.csv) | 172 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| A | [evidence/findings-through-07A.csv](evidence/findings-through-07A.csv) | 200 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| B1 | [evidence/findings-through-07B1.csv](evidence/findings-through-07B1.csv) | 223 | غير مجمعة في مخرجه القديم | exit0 / errors=[] /827hash /ERP0 |
| B2 | [evidence/findings-through-07B2.csv](evidence/findings-through-07B2.csv) | 237 | 44/3 | exit0 / errors=[] /827hash /ERP0 |
| B3 | [evidence/findings-through-07B3.csv](evidence/findings-through-07B3.csv) | 248 | 62/4 | exit0 / errors=[] /827hash /ERP0 |
| B4 | [evidence/findings-through-07B4.csv](evidence/findings-through-07B4.csv) | 261 | 82/5 | exit0 / errors=[] /827hash /ERP0 |
| B5 | [evidence/findings-through-07B5.csv](evidence/findings-through-07B5.csv) | 266 | 104/6 | exit0 / errors=[] /827hash /ERP0 |
| B6 | [evidence/findings-through-07B6.csv](evidence/findings-through-07B6.csv) | 270 | 132/7 | exit0 / errors=[] /827hash /ERP0 |
| B7 | [evidence/findings-through-07B7.csv](evidence/findings-through-07B7.csv) | 276 | 156/8 | exit0 / errors=[] /827hash /ERP0 |
| B8 | [evidence/findings-through-07B8.csv](evidence/findings-through-07B8.csv) | 280 | 184/9 | exit0 / errors=[] /827hash /ERP0 |
| B9 | [evidence/findings-through-07B9.csv](evidence/findings-through-07B9.csv) | 282 | 208/10 | exit0 / errors=[] /827hash /ERP0 |
| B10 | [evidence/findings-through-07B10.csv](evidence/findings-through-07B10.csv) | 285 | 236/11 | exit0 / errors=[] /827hash /ERP0 |
| B11 | [evidence/findings-through-07B11.csv](evidence/findings-through-07B11.csv) | 287 | 266/12 | exit0 / errors=[] /827hash /ERP0 |
| B12 | [evidence/findings-through-07B12.csv](evidence/findings-through-07B12.csv) | 289 | 298/13 | exit0 / errors=[] /827hash /ERP0 |
| B13 | [evidence/findings-through-07B13.csv](evidence/findings-through-07B13.csv) | 291 | 322/14 | exit0 / errors=[] /827hash /ERP0 |
| B14 | [evidence/findings-through-07B14.csv](evidence/findings-through-07B14.csv) | 294 | 350/15 | exit0 / errors=[] /827hash /ERP0 |
| B15 | [evidence/findings-through-07B15.csv](evidence/findings-through-07B15.csv) | 298 | 382/16 | exit0 / errors=[] /827hash /ERP0 |
| B16 | [evidence/findings-through-07B16.csv](evidence/findings-through-07B16.csv) | 299 | 410/17 | exit0 / errors=[] /827hash /ERP0 |
| B17 | [evidence/findings-through-07B17.csv](evidence/findings-through-07B17.csv) | 300 | 434/18 | exit0 / errors=[] /827hash /ERP0 |

أداة baseline --verify قارنت 827 ملفاً/29,128,444 بايت،XML0 و XAML mismatch0 و dotnet_available=false. لم تستعمل--write ولم تُعد baseline. نجح فحص Whitespace مع core.whitespace=cr-at-eol لأن CSV السجل مقصود CRLF. هذه أدلة حفظ واتساق لا صحة كل نثر أو معادلة أو قالب أو صلاحية في التطبيق.
