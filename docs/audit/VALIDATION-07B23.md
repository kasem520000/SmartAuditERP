# تحقق 7B23 — أدوات الوثائق وخطط القبول غير المنفذة

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711` والفرع `arena/94ae8414-smartauditerp`. دخول B23 بعد دفع B22 المكتمل `3276579931925bff37bbf45c5b43efb7fbcd0118` بجميع **648 مادة تدقيق**. ساعة البيئة المرصودة `2026-11-19T22:04:00.405782+00:00` منفصلة عن المرجع المعلن؛ ليست تاريخ تشغيل أو قبول.

**R4g محدود بشريحة SP01، لا كل R4 أو 7B؛ 7B/7 جزئيتان؛ R4h/7B24 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا ERP أو بناء أو C#/VB/.NET/WPF/SQL/Excel/provider/SDK/UtilitiesProj/ToDataTable/REPX أو ماسح/طابعة أو بيانات أعمال أو أسرار أو إصلاح أو قياس أو قبول هنا. `next_phase=8` تخطيط لا إذن. المحادثة الموازية للإصلاح مستقلة؛ لا نفترض أنها بدأت أو تزامنت، ولا ندمج إصلاحاتها في هذا الفرع.

[النتائج](PHASE-07B23.md) · [العقود والتتبع](ITEM-INGRESS-CONTRACTS-07B23.md) · [التحقق والخطط](VALIDATION-07B23.md) · [المتبقي](PHASE-07-REMAINING-07B23.md) · [scope12](review-scope-07B23.csv) · [السجل](findings.csv) · [provenance643](evidence/provenance-07B23.json) · [stdoutB23](evidence/checks-07B23.json)

## 1. ما ينفذ وما لا ينفذ

تنفذ أدوات Python/Git قراءة بصمات وحدود أسطر وربط IDs/روابط وقيود preservation وإعادةحساب نماذجمدخلة ونصوص. لا تستورد التطبيق أوتشغل C#/VB/.NET/WPF/SQL/Excel أو SDK/provider/REPX/scanner/printer أوحفظاًأومعالجة أوقياساً أوبياناتأعمال. success/normal-return/uniquelookup و rdAutooff شروطشاهد لا observations تشغيل.

مكونات المدقق الحالي **650 حالة وثائقية في 24 مجموعة** =606 سابقة محفوظة +44 جديدة؛ ليست اختبارات أعمال. نُفذت **28 وضعية تاريخية OWN** فعلياً بمدخلاتها الخاصة وأدوات التقاطها المعلنة: exit0/827/errors[]، لا ادعاء إعادة كل 28 بعد تثبيت SHA أو تحرير النثر أو push. [stdout B23 الرسمي](evidence/checks-07B23.json) خرج مباشر للمدقق عند checkout الدخول 3276579 قبل commit التسليم، لا JSON معاد تشكيله؛ لا يعاد توليده بعد push. **كل 36 خطة قبول not-executed**؛ لا إصلاح أو تشغيل أو قياس أو قبول ERP.

الأوامر وثائقية فقط:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/validate_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B23
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B22
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/run_historical_contract_item_tests_07B23.py --through-part B22
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/test_item_ingress_audit_validator.py
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/check_item_ingress_witnesses.py
PYTHONDONTWRITEBYTECODE=1 python3 -B docs/audit/tools/collect_baseline.py --verify
```

لا تعاد كتابة أي checks تاريخية عند تكرار الأمر؛ وجّه التشغيل الجديد إلى stdout مستقل. الـ API main يبقى B15، بينما parser/entrypoint الحقيقيان B23، واختبارهما الحالي مستقل عن presets التاريخية.

## 2. سلسلة الحفظ والهوية

| البند | القيمة والحد |
| --- | --- |
| دخول B23 | checkout/remote-tip3276579 بعد دفع B22 المكتمل،648 مادة؛ ليست هوية stdoutB22 الأصلية. |
| مصدر التطبيق |10ba215…d711؛827 مساراً/29,128,444 بايت تطابق inventory، لا build/runtime شهادة. |
| مواد محمية |643؛ استثناءاتالتعديلالقديمةفقط findings/README/PLAN/IMPROVEMENTS/validate_audit؛ كل B22 وماقبلهاأدلةوأدواتمحفوظة. |
| سجل الدخول |كل 316 قاموساً بكلحقل و ALLnext_phase/evidence،raw317CRLF/noBOM بادئةحرفية؛الحالي 319/raw320CRLF. |
| G |G01–205 حرفية؛G206–210 خمس توصياتلا findings أخرى. |
| B22 stdout |189940 بايت،SHA07b037…d3ae؛captureb1f9524 لا entry3276579،ولا يعادبعد push. |
| freezes |findings-through-07B22.csv و shared-indexes-through-07B22.json و provenance-07B23.json مستقلة ثابتة. |
| B22 التاريخي |OWN316/raw317CRLF/indexes و ALL40 الأصلية بطفل presetB22؛A الخاصبمجموعةالاختبار path محلي،لا Path عامأوتعديلقرص. |
| الأبناء السابقون |B21/36 و B20/32 و B19/36 و B18/28 unchanged؛لا skip/filter/protectededit/sharedsubprocessmutation. |

**بصمات دقيقة:**

- frozen316: `81671191c1841bca1c7a7e0f3e7725644104b1d654992f5dc44b00dbdd0d5ce3`.
- shared-indexesB22: `c1195fa8e009432b41bdfaba60f7d052c2f3d9c42b10d0782a29883929b880ea`.
- provenanceB23: `1eb22ab37d41094004c9acf8a0888322d51eb38b888334894b9105cfe27e06ed`.
- شاهد B23:33617 بايت/SHA `ebca4a9a8faf1546b62dd91235af469c96b5c9d3322c843861680a6069b2f61e`؛stdout مباشرلاخلاصةمعادة.
- genuine28:57749 بايت/SHA `b67d3ecc7125f6cbfe163ca35a805895846789351800de539ef76469b28283d6`؛[الأرشيف](evidence/historical-mode-verification-07B23.json) يحفظكل stdoutSHA/length/exit والمدخلوالأدواتعندالالتقاط.

قائمة 28 هي 2–6 و A/B1…B22؛كلهاالتقطتفعلياًبـ OWN و exit0/827/errors[]/stderr فارغ. مفاتيح aggregate الغائبةفيالأقدم null لاتبدلإلى 0. B22=316/606 حالة/23 مجموعة،بكل 40 أصلية؛B21=313/566/22 و B20=310/530/21 و B19=307/498/20 و B18=302/462/19. الـ fixture الاصطناعية 28 في tests لفحصال schema فقط،ليستدليلاًعلىالتنفيذ. تثبيت SHA وتحسينالنثرلاحقاًلايعنيإعادةكل 28 بالشيفرةالنهائيةأوبعد push.

## 3.44 حالة جديدة مستقلة للمدقق، لا 36 خطة أعمال

| مجموعة الحالات الجديدة | ما تحرسه |
| --- | --- |
| 01–05 | OWN316/raw317CRLF/ثلاثة نصوص،رفضالمدخلغيرالدقيق،مساراتمحليةلاتغير Path عموماً،nestingOWN313 واسترجاعالهويات/نسخالقواميس. |
| 06–09 | كلحقول 316 و ALLnext_phase/evidence/rawprefix،فقط 145–147،G205→210،sentinel ومدىالمصدرالصريح. |
| 10–17 | ترتيب SB8/IM8 ودلالاتالسببوالحد،المسؤوليات،FE/INV/خطةثنائية،RS14/upstreamrowSHA/contracts/input/routes/SP3 وعدمبدء 7C. |
| 18–21 | أنواع bool/int الصريحةوتصويب B10،stdout الشاهدالمباشر،fixture28schema منفصلةعنسجل 28 الفعليوبصمته. |
| 22–30 | تراكمودحض membership معحكم 145 المشروط،cursor لأصناففريدةوشواهد single/cancel وضابط emptyseed،رفضشكلغيرمسموحونسخمدخلات. |
| 31–36 | فقدحقول seed فيالمحررين،تساوي defaults،إعلانفشل lookup خارجهذاالنموذج،شكل/قيم finite،maskcomments/strings لتوكن constructor. |
| 37–44 | parser/entrypointB23 الحقيقيان/APIB15/قواعد B16–22،ترتيب OWN22 قبلالحالي،argv دقيقلا globalmutation،ALL40 محفوظةبـ A محلي،316/643/827/zeroextensions و 145potential. |

## 4. خطط القبول 36 — جميعها not-executed

هذه **خطط** لا سجل تنفيذ. لكلقدرة خطتانبإجراءاتومعيارمستقل ومدخلاتومالكوضوابطأمان في[CSV الكامل](evidence/acceptance-tests-07B23.csv). قد تحتاج كلخطةبيئةوإذناًمستقلاً؛حتىخططمراجعةالأرشيفأوالتوازيلايستعملجدولهاكدليلإنجازتشغيلي. الإثباتالوثائقياستمدمن stdout/أرشيفالمدققلا status خططالقبول.

| الخطة/القدرة/المالك | السيناريو والإجراء | معيار القبول غير المنفذ |
| --- | --- | --- |
| P7B23T-01 / FE7B23-01<br>مالك WPF والمنتج و ItemOper والاستيراد | تحديد A ثم إلغاؤه وتأكيد B<br>بعد حسم العقد جهز A/B اصطناعيين؛ اختر A ثم B فقط، أكد واقرأ Itemlist والمستهلك دون حفظ. | عقد نهائي: لا A في النتيجة؛ عقد basket: تظهر عضوية A المتراكمة وإزالتها الصريحة وتنتج نتيجة موثقة لا مفاجأة.<br>status=not-executed |
| P7B23T-02 / FE7B23-01<br>مالك WPF والمنتج و ItemOper والاستيراد | تحديد متعدد ثم إزالة عضو مع Ctrl<br>اختر A+B، ألغ A وأكد B؛ قارن الحالة المعلنة و Result دون الاعتماد على نصوص model Python. | فرق العضوية معلوم وقابل للتفسير وفق العقد؛ إن لم يورد العقد يبقى 145 potential ولا يسجل قبول.<br>status=not-executed |
| P7B23T-03 / FE7B23-02<br>مالك WPF ومحرر الفاتورة | دفعة A/B بعد prefixX<br>جهز X وبحثين ناجحين A/B غير موجودين؛ أكد دفعة واحدة من المدخل المحدد وافحص الهويات بعد كل دورة. | تبقى X ويظهر A و B مرة لكل منهما؛ لا يصبح ناتج الدفعة X+B فقط.<br>status=not-executed |
| P7B23T-04 / FE7B23-02<br>مالك WPF ومحرر الفاتورة | دفعة ثلاثة أصناف مع prefix فارغ<br>ابدأ مسودة معزولة فارغة وأعد A/B/C ناجحة متميزة؛ سجل cursor و LineRef دون حفظ أو عروض. | تبقى A/B/C بهويات مستقلة؛ لا تعتمد سلامة الدفعة على كون C آخر اختيار أو على فهرس مشترك.<br>status=not-executed |
| P7B23T-05 / FE7B23-03<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | بذرة مميزة ناجحة في محرر المبيعات<br>استعمل dtInvSel اصطناعياً بوصف import-A ووحدة مختلفة وكمية 7 وسعر 50 موجب، و lookup فريد ناجح و rdAuto off؛ راقب قبل/بعد hydration. | كل حقل يحتفظ به أو يعرض رفض/override معتمد صريح؛ لا يتحول صامتاً إلى empty/default/1/catalog-quote.<br>status=not-executed |
| P7B23T-06 / FE7B23-03<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | البذرة نفسها في محرر المشتريات<br>كرر القيم الاصطناعية في المسار المنفصل بعد التحقق من مدخلات unit ومصدر السعر؛ قارن row الجديد لا رسالة النجاح. | يحقق المحرران عقد الحقول نفسه أو فرق دعم معلناً؛ تبقى description و quantity والوحدة والسعر بقرار معلوم لا بإسقاط الكائن.<br>status=not-executed |
| P7B23T-07 / FE7B23-04<br>مالك WPF والمنتج و ItemOper والاستيراد | إغلاق بلا تأكيد<br>أعد نتيجة ISDone=false للقائمة في عزل مأذون وافحص عدم استهلاك Itemlist؛ لا تفترض تفاصيل Close/Hide. | لا دفعة مطبقة في المستهلكين المختارين؛ أثر cleanup إن وجد يوثق منفصلاً ولا يسمى قبول كل cancel.<br>status=not-executed |
| P7B23T-08 / FE7B23-04<br>مالك WPF والمنتج و ItemOper والاستيراد | تأكيد عضو غير أخير من المجموعة<br>حدد A+B وأكد A؛ قارن ترتيب Result وعقد الترتيب قبل وضع توقع للبند الأخير. | ترتيب Result معلن ومستقر أو مستقل عن اختيار current؛ لا يستعمل Count كهوية قرار المستخدم.<br>status=not-executed |
| P7B23T-09 / FE7B23-05<br>مالك WPF والمنتج و ItemOper والاستيراد | مقارنة Return و doubleclick<br>بعد اعتماد العقد وفي بيئة اختبار كوّن المجموعة نفسها، وأكد بكل طريق على نسخة مسودة مستقلة. | نفس SelectedIDs/Outcome وفق العقد لكل طريق، بلا اعتماد ترتيب أحداث مفترض من static.<br>status=not-executed |
| P7B23T-10 / FE7B23-05<br>مالك WPF والمنتج و ItemOper والاستيراد | اختيار واحد مستقر كشاهد مقابل<br>استخدم B وحده دون تغييرات سابقة وأكد؛ قارن Result وحدود الدعم دون ادعاء اجتياز كل selection. | B مرة واحدة مع تفسير عدم ظهور stale في هذه الحالة؛ نجاح الشاهد لا يغلق 145 أو كل UX.<br>status=not-executed |
| P7B23T-11 / FE7B23-06<br>مالك WPF ومحرر الفاتورة | تساوي مدخلي F1 و menu<br>أعد prefixX ودفعة A/B في نسختين من المسودة بنفس البيانات، مرة من F1 ومرة من menu. | نفس append-context وبقاء كل البنود في المسارين؛ ليست سلامة cursor قبولاً لـ Loaded أو التفويض.<br>status=not-executed |
| P7B23T-12 / FE7B23-06<br>مالك WPF ومحرر الفاتورة | صنف واحد ضابط للمؤشر<br>من مدخل append حمّل A ناجحاً وحده بعد X وقارن LineRef قبل التحميل وبعده. | تبقى X و A دون حذف؛ نجاح الصنف الواحد لا يسجل إغلاق 146 المتعلق بتكرار الدفعة.<br>status=not-executed |
| P7B23T-13 / FE7B23-07<br>مالك WPF ومحرر الفاتورة | مقارنة دفعة المحرر الآخر<br>جهز X و A/B فريدة ناجحة؛ سجل seed ذات ItemId0 التي أضافتها كل دورة ثم LineRef الجديدة. | تبقى X/A/B وتتطابق seed المحذوفة مع seed الدورة؛ لا قبول لمسار تكرار أو فشل غير مختبر.<br>status=not-executed |
| P7B23T-14 / FE7B23-07<br>مالك WPF ومحرر الفاتورة | حماية بند غير فارغ عند cursor<br>وجّه cursor إلى بند ذي ItemId موجب في حالة اختبار مرجعية وفق عقد edit؛ لا تعدل بيانات أعمال. | لا يحذف بنداً غير فارغ دون قرار replace معلن؛ اختلاف الضابط عن سلوك المبيعات يبقى موثقاً.<br>status=not-executed |
| P7B23T-15 / FE7B23-08<br>مالك الثقافة و Excel/provider والتشغيل و WPF | خريطة خمس خلايا صالحة<br>بعد إذن لاحق وبـ fixture فقط، عين الحقول الخمسة مع Code نشط وقارن dtInvSel بالمدخل؛ لا تشغله هنا. | أسماء الخلايا الخمس وأنواعها ومصادرها مثبتة؛ لا يسقط الوصف أو العدد عند الانتقال إلى المحرر.<br>status=not-executed |
| P7B23T-16 / FE7B23-08<br>مالك الثقافة و Excel/provider والتشغيل و WPF | Code مرفوض شاهد على حد المسار<br>استعمل Code غير مطابق في بيئة اختبار بلا SQL حر؛ راقب return و ISDone ونتيجة الصف. | لا hydration ناجح لهذا الصف؛ تظهر النتيجة المرفوضة دون اعتبار غياب 147 قبولاً لكل فشل.<br>status=not-executed |
| P7B23T-17 / FE7B23-09<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | وصف غير فارغ فريد ومميز<br>جهز description بعلامة اصطناعية غير شخصية؛ تتبع كائن seed وهوية الصف الجديد في المحررين. | تبقى العلامة أو يرفض الوصف بقاعدة معلنة؛ لا empty غير مفسر بعد lookup ناجح.<br>status=not-executed |
| P7B23T-18 / FE7B23-09<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | وصف فارغ ضابط لا يثبت النقل<br>كرر description فارغاً مع نفس الهوية والمقادير المميزة؛ افحص بقية الحقول أيضاً. | لا يستنتج نقل description من مصادفة empty=empty؛ تثبت الكمية والوحدة والسعر مستقلة.<br>status=not-executed |
| P7B23T-19 / FE7B23-10<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | وحدة بديلة صحيحة في fixture<br>بعد اعتماد UnitId/ratio، اختر وحدة مستوردة غير default وأكمل lookup فريداً في المحررين. | تبقى هوية الوحدة المستهدفة أو يظهر رفض/override معلن؛ لا اختيار default صامت من unitId0.<br>status=not-executed |
| P7B23T-20 / FE7B23-10<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | نفس الوحدة كشاهد مقابل<br>اجعل الوحدة المستوردة مساوية للافتراضية مع كمية ووصف مختلفين؛ قارن هويات الوحدات لا مجرد أسمائها. | عدم فرق UnitName ليس دليل نقل UnitId؛ يحتفظ الأثر بمصدر الوحدة ويوثق حد التساوي.<br>status=not-executed |
| P7B23T-21 / FE7B23-11<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | كمية 7 مع rdAuto off<br>استعمل quantity7 مع بذرة واحدة فريدة و rdAuto off واضح؛ تتبع النقل ثم إنشاء row والحساب في مختبر مأذون. | تبقى 7 أو رفض/override صريح؛ لا تصير 1 كتبع لإعادة تهيئة الصف.<br>status=not-executed |
| P7B23T-22 / FE7B23-11<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | rdAuto on يحتاج عقداً مستقلاً<br>بعد تعريف العقد اختبر نمط الحاسبة بكميات اصطناعية وملكية حوار محددة؛ قارن مصدر QTY المعلن. | تمييز كمية import عن كمية Calculator/settings مع إلغاء صريح؛ لا شهادة تشغيل أو حكم على كل modal من القبول المخطط.<br>status=not-executed |
| P7B23T-23 / FE7B23-12<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | سعر مستورد 50 و quote20 — مصدران موردان<br>عين مصدر سعر 50 موجب ومصدر default20 كمدخلين موردين فقط؛ تتبعهما على وحدة معتمدة دون افتراض صحة أحدهما. | PriceSource وقرار preserve/override/reject موثقان؛ لا فقد صامت للسعر المستورد بسبب تبديل الكائن.<br>status=not-executed |
| P7B23T-24 / FE7B23-12<br>المحاسب ومالك الوحدة والتسعير والمخزون و HR | سعر 0 أو مساوٍ لل quote كشاهد<br>حدد سياسة السعر 0/unknown أولاً، واختبر 0 وحالة default المساوية في عزل منفصل. | لا ينسب إلى 147 فرق غير موجود عند التساوي، ولا يسوّى 0 بـ unknown أو تستنتج سياسة من Math.Round.<br>status=not-executed |
| P7B23T-25 / FE7B23-13<br>مالك WPF والمنتج و ItemOper والاستيراد | تطابق الأزرار مع قرار التكرار<br>بعد إذن لاحق فقط اختبر كل زر على بند مكرر، واقرأ typedOutcome والأثر؛ حافظ على إحالة 143. | add-quantity يزيد وفق عقد و new-line ينشئ صفاً؛ لا يضاف معرف جديد للعكس نفسه.<br>status=not-executed |
| P7B23T-26 / FE7B23-13<br>مالك WPF والمنتج و ItemOper والاستيراد | إلغاء 0/3 وعزل 147 عن التكرار<br>استخدم cancel مع بند مكرر وتتبع نتيجة caller كمسار منفصل؛ اختبر 147 منعزلاً بأصناف فريدة ناجحة. | لا يخلط عدم إدراج loader بضمان عدم تغيير caller؛ يظل 147 قابلاً للإثبات بلا 143 أو 144.<br>status=not-executed |
| P7B23T-27 / FE7B23-14<br>مالك WPF والمنتج و ItemOper والاستيراد | تعيين type1/2 والهوية<br>بعد عقد DocumentRef/branch استخدم report-row اصطناعياً لكل type من العينة وسجل construct/Show/Navigate. | النوع والهوية والمصدر و allowed-set متطابقة أو مرفوضة؛ trace لا يقبل 132 أو كل navigation تلقائياً.<br>status=not-executed |
| P7B23T-28 / FE7B23-14<br>مالك WPF والمنتج و ItemOper والاستيراد | حد نوع خارج العينة<br>صنف type3 والأنواع الأخرى supported/unsupported/optional بقرار مالك؛ لا يختبر POS هنا من ظهور اسمه. | يبقى خارج body العينة بتصرف مسند؛ لا missing-feature واجبة أو قبول نافذة من مجرد constructor.<br>status=not-executed |
| P7B23T-29 / FE7B23-15<br>مالك الثقافة و Excel/provider والتشغيل و WPF | عقد no-match بعد المنتج<br>جهز fixture يتغير فيه master افتراضياً بعد المنتج، وعرّف Outcome المطلوب؛ افصله عن شاهد 147 الموجب. | نتيجة failed/unknown/selection محددة ولا رسالة success لكل صف بلا result؛ لا يسمى ذلك سباقاً مرصوداً.<br>status=not-executed |
| P7B23T-30 / FE7B23-15<br>مالك الثقافة و Excel/provider والتشغيل و WPF | استثناء hydration مع رجوع caller<br>بمضاعف اختبار وبإذن فقط، أعد failure واضحاً من loader وتتبع تطبيق المستورد و health. | لا تمر قيم صف فاشل كصحيح ولا تحذف prefix؛ خطة الفشل لا تسجل تنفيذاً أو امتداد 144.<br>status=not-executed |
| P7B23T-31 / FE7B23-16<br>DBA ومالك الأمان و AuditorAPI | مراجعة الحواجز قبل أي قبول<br>قبل تخطيط تشغيل اربط المخطط والمنح والبيئة والعزل بإجراءات الحفظ والمخزون التي تعبر الحد. | سجل gate لكل قيد غير محسوم؛ لا يتحول اجتياز Python أو العرض إلى إثبات تشغيلي.<br>status=not-executed |
| P7B23T-32 / FE7B23-16<br>DBA ومالك الأمان و AuditorAPI | مراجعة ثبات certainty والإذن<br>قارن سجل الدخول والحالي حرفياً، وبالأخص 014/132 و 020/021 والحالة و next_phase. | تبقى كل التصنيفات والحالة كما هي؛ next_phase8 ليس إذن تنفيذ أو إصلاح هنا.<br>status=not-executed |
| P7B23T-33 / FE7B23-17<br>مالك نطاق التدقيق والمنتج والتوثيق | تدقيق نسب كل 14 بقية<br>احسب rowSHA لكل صف B22 الأصلي، ثم قارن عقده و required-input وكل mapped-route في RSB23. | تطابق 14 هوية/rowSHA/contract؛ المدخل القديم كامل ولا approved أو ضياع route.<br>status=not-executed |
| P7B23T-34 / FE7B23-17<br>مالك نطاق التدقيق والمنتج والتوثيق | تدقيق split ومعيار الخروج<br>راجع SP01–03 والقدرة التالية المقترحة بمدخل ومصدر ومخرج واستبعاد؛ لا عدد جلسات أو نسبة مسارات. | تبقى 3 splits مسببة مفتوحة و 7C لم تبدأ؛ R4h/B24 اقتراح لا وعد إغلاق R4 أو كل 7B.<br>status=not-executed |
| P7B23T-35 / FE7B23-18<br>مالك نطاق التدقيق والمنتج والتوثيق | مراجعة OWN والأرشيف<br>شغل مدقق الوثائق بوضع B22 بـ OWN316/raw317CRLF/indexes وكل 40 أصلية دون skip؛ قارن بصمات 643/827. | لا live319 أو global Path/subprocess mutation أو disk overlay؛ stdout القديم ثابت والجديد موسوم بـ checkout فعلي.<br>status=not-executed |
| P7B23T-36 / FE7B23-18<br>مالك نطاق التدقيق والمنتج والتوثيق | تسليم SHA إلى المسار الموازي<br>قدم SHA التدقيق المدفوع للمحادثة الأخرى مع قاعدة merge حافظة للتاريخ وبنود finding→task/test؛ لا تدّع بدء المسار من غير دليل. | لا repair→audit merge هنا أو كتابة ملفات repairs؛ تعلن المحادثة الأخرى آخر SHA راجعته، ولا يتغير سجل audit بتقدمها.<br>status=not-executed |

## 5. حدود الحكم

145 لا يصير confirmed من نموذجتراكم حتىيورّدعقد final-selection/basket.146/147 confirmed لتعليماتالمسارالمشروطنفسهالالنتيجةعرضأوحفظمرصودة. لايعتمدسعر 50/20 أو PACK/ratio أو mergepolicy؛الـ False عند lookup لايمثلفشل C#الفعلي. القراءة cp1256 لأربع paths ليست compilerencoding قبولاً،و 477/11/7 ليستكل bodies/callgraph/census أو 455FE معادة.

تبقى 014/132 محتملتين و 020/021 وحواجزالمال/ACL/stock/save والعقودالخارجية،و 034/035/136–144 بلا extension أوإعادةعد. تصويب B10 الإضافي 10 مقابل 120 وعند equality1 كلاهما 10 محفوظبلاكتابة G138.7B/7 جزئيتان؛R4h/B24 مقترحأو split مسبب؛7C لمتبدأ؛8 غيرمأذونة. استقلالمحادثةالإصلاحلايعنيبدءها،ولاتزامناًتلقائياًأودمجإصلاحاتهناأوتغييرحالةنتيجةمنغيردليل.
