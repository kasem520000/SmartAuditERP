# تحقق 7B22 وخطط قبول غير منفذة

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711` والفرع `arena/94ae8414-smartauditerp`. دخول B22 بعد دفع B21 المكتمل `b1f9524e552c36a05e1b351e2e12fd450ba051aa` بجميع **618 مسار تدقيق**. ساعة التجميد المرصودة `2026-11-19T20:54:51.849393+00:00` مستقلة عن المرجع المعلن، وليست تاريخ تشغيل أو قبول.

**R4f محدود بهذه الشريحة، لا كل R4 أو SP03؛ 7B/7 جزئيتان؛ R4g/7B23 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا بناء أو تشغيل ERP/C#/VB/.NET/WPF/SQL/Excel/provider/SDK/UtilitiesProj/ToDataTable/REPX أو قالب/طابعة/ماسح أو بيانات أعمال أو أسرار أو إصلاح أو قياس أو قبول. Python و Git لأدوات الوثائق فقط؛ `next_phase=8` تخطيط لا إذن.

[النتائج](PHASE-07B22.md) · [العقود والتتبع](CONTRACT-ITEM-CONTRACTS-07B22.md) · [التحقق والخطط](VALIDATION-07B22.md) · [المتبقي](PHASE-07-REMAINING-07B22.md) · [scope12](review-scope-07B22.csv) · [السجل](findings.csv) · [provenance613](evidence/provenance-07B22.json) · [stdoutB22](evidence/checks-07B22.json)

## 1. ما نفذ بالفعل وما لم ينفذ

اجتاز التحقق المجمّع الحالي **606 حالات لمدققات الوثائق في 23 مجموعة**، منها **40 حالة جديدة**، مع **827 بصمة تطبيق مطابقة و`errors=[]`**. نُفذت أيضاً **27 وضعية تاريخية OWN** بمدخلاتها الخاصة وبأدوات الالتقاط المعلنة، لا ادعاء إعادة كل27 بعد التحرير أو الدفع. [stdout B22 الرسمي](evidence/checks-07B22.json) خرج مباشر للمدقق، لا JSON معاد تشكيله؛ هوية التقاطه checkout الدخول b1f9524 قبل commit التسليم، ولا يعاد بعد push. **كل خطط القبول الـ36 غير منفذة**؛ النجاح هنا وثائقي لا ERP أو إصلاحاً أو قبولاً أو قياساً.

نُفذت أدوات Python/stdlib و Git الوثائقية فقط، لا محمل C# أو WPF أو DB/provider/Excel/SDK أوماسح/طابعة أو بيانات أعمال. **كل 36 خطة في هذا التقرير not-executed**، مهما نجح checker.40 حالة جديدة تفحص حراسة الوثائق والنماذج الموردة لا صحة ERP أو سياسة تسعير أو أثر import محفوظ.

[الشاهد](evidence/contract-item-witnesses-07B22.json) stdout فعلي مباشر حتمي:30159 بايت، SHA256=`a911a378abc7da84b865bd939c66b27bcac1fd095b9227e7f5c1f4ad61f2455a`. يحوي 12 نموذجاً بمدخلات موردة و 12 ملاحظة نصية، و 31 قراءة محدودة من 11 مساراً، وبحثين بأشكال receiver محددة عبر 477 ملف C# مع أربع replacement paths. هذه ليست 31 body review أو 477 مراجعة، ولا دليل وصول ماسح أو قاعدة تسعير أو مخطط نشر. لا يعتمد 96 تحويلاً أو Action نوعاً في SDK؛ المدخلات مصطنعة لا بيانات أعمال.

### نتيجة الفحوص الوثائقية الحالية

| الفحص المنفذ | النتيجة وحد الحكم |
| --- | --- |
| CLI الافتراضي و`--through-phase 7 --phase7-part B22` الصريح | 316 نتيجة مفتوحة، و606 حالات مدقق/23 مجموعة، و827 بصمة مطابقة، و`errors=[]`؛ ليس تشغيل ERP. |
| الأوضاع التاريخية الـ27 | لكل وضع مدخله OWN وstdoutSHA/length/exit؛ كلها exit0/827/errors[] وstderr فارغ. سجل الالتقاط سابق لتثبيت SHA وتحسين النثر، لا ادعاء إعادة الجميع بعدها. |
| `collect_baseline.py --verify` | 827 ملفاً/29,128,444 بايت مطابقة؛ XML parse errors=0 وXAML name mismatches=0. .NET غير متاح ولم يجر build؛ فحص النص ليس قبول تطبيق. |
| حفظ السجل والأدلة | 613 مادة تاريخية وثلاثة freezes ثابتة؛313 قاموس صف قديم وكل حقوله وبادئة raw314CRLF/noBOM وG01–200 حرفية. |
| `git -c core.whitespace=cr-at-eol diff --check` | لا أخطاء مسافات في التغيير؛ لا حكم جودة أعمال أو معالجة للنتائج. |

## 2. حماية الدخول والهوية

| العنصر | الهوية وحد الحكم |
| --- | --- |
| مصدر التطبيق | 10ba215152f722c8808aea0bb672c1d1d4d9d711؛ 827path/SHA256 و 29,128,444 بايت، لا checkout للتطبيق بدلاً من التسليم. |
| دخول B22 | b1f9524e552c36a05e1b351e2e12fd450ba051aa بعد دفع B21 المكتمل؛ 618 مادة منها 613 محمية، وخمسة مسارات مشتركة فقط يسمح بتقدمها. |
| تجميد 313 صفاً | evidence/findings-through-07B21.csv؛ SHA256=f1616cae0ea2363f5b459716b56298067b9d47f16b94c85e62ab7249459032f0؛ raw314CRLF/noBOM. |
| تجميد الفهارس | evidence/shared-indexes-through-07B21.json؛ SHA256=51984aa3813743612a03c925b0bbd1b40abbda2943ec1e2d745266a3bb12c272؛ نصوص README/PLAN/IMPROVEMENTS الأصلية حرفياً. |
| provenance613 | evidence/provenance-07B22.json؛ SHA256=b76437da81084deb5cb9622c24aef8c4d6d8992108ee7b8ac86667c3e87b6228؛ 613 بصمة محمية وتجميد واحد، لا rebaseline. |
| stdoutB21 المحمي | 180181 بايت/SHA256=02ed265704efe56144f104e2b991debe488aa410d7ee586536fe78e3fdba3177؛ capturecheckout=c2c895d0df0e4f106c4e5c2853219aa04303e002، لا entryb1f. |
| السجل الحالي | 316 صفاً/raw317CRLF/noBOM؛ كل313 قاموس صف وALLnext_phase/evidence وبادئة raw314CRLF محفوظة حرفياً. ثلاث Medium confirmed فقط، صفر extensions. |
| التوصيات | G01–200 صفوف حرفية؛ G201–205 إضافات لا تمثل خمس نتائج أخرى. |
| حالة Git المستعادة | أعيدت محاذاة metadata على نفس الفرع بـ mixed reset فقط بعد مطابقة 1445 blob مع التسليم ومساواة SHA256 قبل وبعد؛ لم تعد كتابة ملف تطبيق أو تدقيق. |
| مرجع التاريخ والساعة | 2026-11-16 مرجع التدقيق؛ ساعة التجميد 2026-11-19T20:54:51.849393+00:00 رصد بيئة مستقل، لا عمل تطبيق أو قبول على أي من التاريخين. |


المسارات المشتركة الخمسة فقط هي findings.csv و README.md و PLAN.md و IMPROVEMENTS.md و tools/validate_audit.py. تبقى كل التقارير والأدوات والاختبارات و freezes و witnesses و stdout التاريخية ببصماتها. لا protected edit أو skip أو تغيير ALLnext_phase أو overlay أو rebaseline أو إعادة أرشيف بعد push. تصويب B10 الإضافي 10 مقابل 120 و equality1=10 مع G138 المحمي باقٍ.

## 3. أوضاع OWN التاريخية و CLI الحالي

[سجل 27](evidence/historical-mode-verification-07B22.json) التقاط stdout فعلي لكل وضع، 51222 بايت، SHA256=`9451c55565541fa72d7304ee81f8f039f1cb1d8bde535b2c91082a7bdc0197f2`. ليس نسخ 26 قديماً أو تحديث أرقامها. خرج كل process بالرمز 0 مع stderr فارغ و errors=[] و 827 بصمة. قيم null في التجميع القديم تعني أن الوضع لم يبلغ aggregate، لا 0 أو فقد ملف. كل stdoutSHA/length/command/checkout/toolhash موثق وقت الالتقاط؛ قد يختلف مدقق جديد أو نثر لاحق، ولا يدعى إعادة كل 27 بعد تثبيت SHA أو الدفع.

| الوضع OWN المنفذ | صفوفه لا live316 | حالات مدقق الوثائق/المجموعات | exit/بصمات |
| --- | --- | --- | --- |
| phase2 | 49 | null / null — غير مبلغ عنه | 0 / 827 |
| phase3 | 74 | null / null — غير مبلغ عنه | 0 / 827 |
| phase4 | 106 | null / null — غير مبلغ عنه | 0 / 827 |
| phase5 | 137 | null / null — غير مبلغ عنه | 0 / 827 |
| phase6 | 172 | null / null — غير مبلغ عنه | 0 / 827 |
| A | 200 | null / null — غير مبلغ عنه | 0 / 827 |
| B1 | 223 | null / null — غير مبلغ عنه | 0 / 827 |
| B2 | 237 | 44 / 3 | 0 / 827 |
| B3 | 248 | 62 / 4 | 0 / 827 |
| B4 | 261 | 82 / 5 | 0 / 827 |
| B5 | 266 | 104 / 6 | 0 / 827 |
| B6 | 270 | 132 / 7 | 0 / 827 |
| B7 | 276 | 156 / 8 | 0 / 827 |
| B8 | 280 | 184 / 9 | 0 / 827 |
| B9 | 282 | 208 / 10 | 0 / 827 |
| B10 | 285 | 236 / 11 | 0 / 827 |
| B11 | 287 | 266 / 12 | 0 / 827 |
| B12 | 289 | 298 / 13 | 0 / 827 |
| B13 | 291 | 322 / 14 | 0 / 827 |
| B14 | 294 | 350 / 15 | 0 / 827 |
| B15 | 298 | 382 / 16 | 0 / 827 |
| B16 | 299 | 410 / 17 | 0 / 827 |
| B17 | 300 | 434 / 18 | 0 / 827 |
| B18 | 302 | 462 / 19 | 0 / 827 |
| B19 | 307 | 498 / 20 | 0 / 827 |
| B20 | 310 | 530 / 21 | 0 / 827 |
| B21 | 313 | 566 / 22 | 0 / 827 |


**B21 OWN313/raw314CRLF/indexes في الذاكرة** مع كل 36 حالة أصلية غير معدلة في [طفل presetB21 صريح](tools/run_historical_amountword_tests_07B22.py). يستعمل context-local AUDIT Path وصفوفه وثلاثة نصوص، لا كتابة أو تعديل Path/subprocess المشترك. توجه الواجهة الضيقة argv الدقيق لجناح B21 فقط وتحفظ kwargs؛ لا filter أو skip أو تغيير اختبار محمي. تبقى B20/32 و B19/36 و B18/28 في أطفالها بإعداداتها التاريخية.

**الحالي build_cli_parser/defaultB22 والـ entrypoint يختبران باستقلال؛ main API defaultB15 محفوظ عمداً.** PHASE7_B21_CLI وقبله B20/B19/B18/B17/B16 قواعد توافق فعالة لا افتراض اليوم. جناح B21 المنفرد يفحص parser وقته؛ يستعمل launcher التاريخي، ولا يعدل الاختبار أو يسمى assertion الحالي تاريخياً. في B22 تطبق extend_contract_items بعد الخروج من سياق OWN B21، فتفحص السجل والفهارس الحالية فعلاً.

## 4. الأربعون حالة مدقق جديدة

- **1–8:** OWN313/raw314CRLF/exact indexes؛ رفض BOM/LF أو صفوف غير مطابقة، وعزل النسخ وتداخل 310 واستعادة الاستثناء، وكل حقل في السجل و G200→205.
- **9–18:** sentinel مصدري صادق وتوسيع same-file ranges؛ EN8/UP8 وقيد Code ودعم 3؛ FE18/INV18 وخطتان لكل قدرة؛ نسب RS14 و hash والعقود والمدخل وكل مسارات الإحالة؛ SP3 و 4B/6C وحراسة الأنواع والصفر و B10.
- **19–20:** إعادة حتمية للشاهد ومطابقة بصمته؛ سجل 27 الحقيقي منفصل عن fixture مصطنعة لفحص schema، و OWN313/ALL36 و null لا 0.
- **21–33:** نماذج موردة لسعر وحدة أخرى وشواهده، و Action1/2/0/3، واستيراد غير الأخير/الأخير/الإلغاء ونسخ inputs؛ قيد Code وجدول نتائج query المفترضة والبحث المؤهل مع حجب comments/strings؛ لا .NET أو WPF.
- **34–40:** parser/defaultB22 الحقيقي و API B15 والـ entrypoint؛ ضيق argv facade والاستعادة بلا global patch؛ launcher لكل 36 حالة مع protected hashes؛ فحص جيران 313 وحواجز potential وصفر extensions؛ ونطاق 12/8/4/416/411 وعدم فرض دعم 3.

النجاح لا يعتمد كل نثر أو مجال تاريخي أو كل callgraph، ولا يشهد بجدوى إصلاح مقترح. خطأ المدقق يستلزم تحقيقاً في التوثيق، ولا يتحول إلى فشل ERP أو علاج صامت له.

## 5. خطط القبول الست والثلاثون — جميعها NOT EXECUTED

### P7B22T-01 — سعر عبوة مع صف عميل لوحدة الأساس

- **الربط:** FE7B22-01 / INV7B22-01 / P7-142؛ finding-specific.
- **المتطلبات:** fixture مجهلة U1/U2 بنسبة معلنة 12؛ quote محملة لـ U2=120 وصف عميل لـ U1=8 وخيار scalar محلي 6؛ عقد وحدة السعر ودعمه قبل القبول.
- **الإجراء المقترح:** بعد إذن مستقل فقط، مرر السيناريو إلى المسارين المختارين وتتبع UnitID/UnitEquality/ItemPrice ومصدر السعر قبل override وبعده، دون إنتاج.
- **معيار القبول اللاحق:** تبقى sourceUnit/lineUnit صريحتين؛ تحويل معتمد أو رفض مسبب، لا 8 موسومة كسعر U2 بلا وحدة.96 مرجع خطي افتراضي لا معيار سياسة ملزم.
- **المالك:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1195-1211`؛ `1331-1366`؛ `1481-1527`؛ `SmartAuditERP/Class/ItemOper.cs:495-521`؛ `983-1041`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1022-1083`؛ `SmartAuditERP/Properties/Resources.resx:1086-1103`

### P7B22T-02 — أولوية العميل والوحدة مع الخصم والضريبة

- **الربط:** FE7B22-01 / INV7B22-01 / P7-142؛ finding-specific.
- **المتطلبات:** عقد مالك لوحدة السعر وأولوية العميل والخصم والضريبة والدقة؛ fixtures مصطنعة للوحدة غير الأساسية ولا override كتحكم.
- **الإجراء المقترح:** بعد إذن مستقل قارن الفرعين ومصدر السعر قبل العروض والحساب والحفظ، وافصل تنفيذ أولوية العقد عن حفظ priceUnit.
- **معيار القبول اللاحق:** كل قيمة يمكن ردها إلى وحدة ومصدر وقاعدة معتمدة؛ إصلاح P4-026 وحده لا يختم 142 ولا يكفي لتسوية مصدر سعر العميل.
- **المالك:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1195-1211`؛ `1331-1366`؛ `1481-1527`؛ `SmartAuditERP/Class/ItemOper.cs:495-521`؛ `983-1041`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1022-1083`؛ `SmartAuditERP/Properties/Resources.resx:1086-1103`

### P7B22T-03 — إضافة الكمية من الحوار المرئي

- **الربط:** FE7B22-02 / INV7B22-02 / P7-143؛ finding-specific.
- **المتطلبات:** بند A بكمية 4 ووحدة ثابتة، بلا scale/serial/عروض؛ مصدر تحميل متاح ودعم الحوار موثق.
- **الإجراء المقترح:** في قبول لاحق مأذون فقط، اختر إضافة الكمية من الزر الفعلي وقارن البنود قبل وبعد في loaders الثلاثة المختارة، مع التحقق من عودة الحوار.
- **معيار القبول اللاحق:** يزداد البند المقصود إلى 5 ولا ينشأ بند جديد بسبب كود معكوس، أو يرفض بوضوح وفق عقد مسمى متسق مع النص.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/MsgExistItem.xaml:59-134`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:1-57`؛ `SmartAuditERP/Class/ItemOpercontract.cs:1000-1084`؛ `1109-1193`؛ `SmartAuditERP/Class/ItemOper.cs:1091-1154`

### P7B22T-04 — إدراج بند جديد من الحوار المرئي

- **الربط:** FE7B22-02 / INV7B22-02 / P7-143؛ finding-specific.
- **المتطلبات:** نفس fixture وبند A قائم، مع مصدر سعر معلوم للبند الجديد وقاعدة تكرار مقررة.
- **الإجراء المقترح:** بعد إذن مستقل اختر إدراج بند جديد وتتبع Action والانتقال وهوية السطر ومصدر سعره دون حفظ.
- **معيار القبول اللاحق:** يبقى القديم 4 ويضاف بند 1 بهوية مستقلة وفق الاختيار؛ لا تستبدل زيادة القديم بهذا الطلب ولو تساوى مجموع الكمية.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/MsgExistItem.xaml:59-134`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:1-57`؛ `SmartAuditERP/Class/ItemOpercontract.cs:1000-1084`؛ `1109-1193`؛ `SmartAuditERP/Class/ItemOper.cs:1091-1154`

### P7B22T-05 — دمج بند سابق غير أخير أثناء الاستيراد

- **الربط:** FE7B22-03 / INV7B22-03 / P7-144؛ finding-specific.
- **المتطلبات:** A في index1 و B في 2؛ صف A مستورد بكمية 7 وسعر 50؛ عقد دمج معتمد ومصدر متاح وحالة fixture فقط.
- **الإجراء المقترح:** بعد إذن مستقل نفذ قرار دمج مسمى وافحص السطر الذي تعيده عملية التحميل ثم projection، دون استخدام Count لتعويض هوية النتيجة.
- **معيار القبول اللاحق:** تطبق القيم على هوية A المعلنة وفق سياسة الدمج، أو تسجل نتيجة رفض/فشل قابلة للمعالجة؛ لا success مع فقد قيم الصف بسبب موضعه.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmcontract.xaml:1001-1022`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:185-206`؛ `1747-1762`؛ `2500-2550`؛ `SmartAuditERP/Class/ItemOpercontract.cs:1025-1035`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml:127-134`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:48-53`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:996-1057`

### P7B22T-06 — عدم إدراج آخر بند مطابق

- **الربط:** FE7B22-03 / INV7B22-03 / P7-144؛ finding-specific.
- **المتطلبات:** B في index1 و A في 2؛ A=4/10 وصف import A=7/50 ووصف مختلف؛ اختيار عدم الإدراج Action3.
- **الإجراء المقترح:** بعد إذن لاحق فقط اختر عدم الإدراج، وقارن نسخة البنود عند caller بعد رجوع loader، لا عند إغلاق الحوار فقط.
- **معيار القبول اللاحق:** لا يتغير وصف أو كمية أو سعر A؛ الصف cancelled صراحة، ولا يحول شرط code+Count عدم الإدراج إلى overwrite للبند القديم.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmcontract.xaml:1001-1022`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:185-206`؛ `1747-1762`؛ `2500-2550`؛ `SmartAuditERP/Class/ItemOpercontract.cs:1025-1035`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml:127-134`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:48-53`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:996-1057`

### P7B22T-07 — عقد منتج الأسعار لوحدتين

- **الربط:** FE7B22-04 / INV7B22-04 / P7-142؛ counterevidence-or-shared-contract.
- **المتطلبات:** schema/version منقحان ومثال لوحدتين من مالك التعاريف، بلا DB إنتاج أو أسرار.
- **الإجراء المقترح:** في بيئة مأذونة لاحقاً افحص ناتج الكاتب، ثم تعيين سعر الأساس والإضافية وقراءة المستهلك، دون افتراض تاريخ الأسعار أو ترتيب الصفوف.
- **معيار القبول اللاحق:** تعيين سعر كل وحدة صريح، ولا تخمن وحدة صف ItemPrices من ItemId أو موضعه أو اسم عمود السعر وحده.
- **المالك:** DBA ومالك الأمان و AuditorAPI؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1022-1083`؛ `SmartAuditERP/Properties/Resources.resx:1086-1103`؛ `47443-47447`

### P7B22T-08 — بيانات تاريخية بوحدة غائبة أو متعددة

- **الربط:** FE7B22-04 / INV7B22-04 / P7-142؛ counterevidence-or-shared-contract.
- **المتطلبات:** قاموس مالك لحالات NULL/history/duplicate price rows وما إذا كانت مسموحة؛ fixtures صناعية فقط.
- **الإجراء المقترح:** بعد إذن مستقل أدخل حالات الاختبار المتفق عليها وقارن projection قبل العروض والحفظ، مع حفظ نسخة المصدر.
- **معيار القبول اللاحق:** unknown/ambiguous يرفض أو يمثل بوضوح؛ لا Rows[0] كسعر مضمون لكل وحدة أو تاريخ. لا يثبت الاختبار أن التاريخ الفعلي يحوي تلك الحالات.
- **المالك:** DBA ومالك الأمان و AuditorAPI؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1022-1083`؛ `SmartAuditERP/Properties/Resources.resx:1086-1103`؛ `47443-47447`

### P7B22T-09 — نفس وحدة السطر والسعر كتحكم

- **الربط:** FE7B22-05 / INV7B22-05 / P7-142؛ counterevidence-or-shared-contract.
- **المتطلبات:** U1/equality1 و customer quote U1=8، وعقد أولوية معتمد لا قيمة تجارية حقيقية.
- **الإجراء المقترح:** بعد إذن مستقل قارن load في المسارين المختارين بنفس الوحدة، وافصل قيمة السعر عن هويتها.
- **معيار القبول اللاحق:** لا يوسم هذا cross-unit، ويطابق الإسقاط العقد المعلن؛ لا إيجابية زائفة لمجرد تغير scalar داخل الوحدة نفسها.
- **المالك:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1331-1366`؛ `1481-1527`؛ `SmartAuditERP/Class/ItemOper.cs:983-1041`

### P7B22T-10 — غياب override العميل كتحكم

- **الربط:** FE7B22-05 / INV7B22-05 / P7-142؛ counterevidence-or-shared-contract.
- **المتطلبات:** U2=120 وعميل بلا override أو بلا صف سعر؛ تعريف الفرق بين missing customer و missing price والحالة غير المطابقة.
- **الإجراء المقترح:** في قبول لاحق مأذون افصل الفروع الثلاثة وتتبع السعر ومصدره قبل تحميل العميل وبعده.
- **معيار القبول اللاحق:** يحافظ الفرع على quote الوحدة أو يعلن رفضاً/تعذراً وفق العقد؛ لا يحول غياب البيانات إلى سعر صفر ناجح ولا يغلق 026.
- **المالك:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1331-1366`؛ `1481-1527`؛ `SmartAuditERP/Class/ItemOper.cs:983-1041`

### P7B22T-11 — رمز صالح بكتالوج ثابت

- **الربط:** FE7B22-06 / INV7B22-06 / H7B22-03؛ counterevidence-or-shared-contract.
- **المتطلبات:** Code A موجود، ونتيجتا التحقق والبحث مضبوطة بالثبات في fixture؛ لا ملف أو استيراد حقيقي الآن.
- **الإجراء المقترح:** في قبول لاحق مأذون تحكم في query outcomes وسجل الفرع المستعمل بين IsItemExist و SearchByCode.
- **معيار القبول اللاحق:** يدخل فرع ID كما يشترط الثبات، ولا يسجل ذلك كمسح barcode. تظل المطابقة بين query ين افتراضاً لا معاملة ذرية.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1764-1810`؛ `2500-2550`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:996-1057`؛ `1188-1199`

### P7B22T-12 — اختلاف الحالة بين حارسي الرمز

- **الربط:** FE7B22-06 / INV7B22-06 / H7B22-03؛ counterevidence-or-shared-contract.
- **المتطلبات:** خطة مصطنعة لتغير master بين التحقق والبحث، بمتحكم مصدر في بيئة معزولة فقط، بلا إنتاج.
- **الإجراء المقترح:** بعد إذن مستقل اختبر mismatch وسلوك fallback أو رفضه وفق support matrix منقحة.
- **معيار القبول اللاحق:** تغير المرجع أو إخفاقه له نتيجة صريحة؛ لا قبول ضمني لاختيار عادي باسم نجاح barcode ولا ادعاء dead code من حالة الثبات.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1764-1810`؛ `2500-2550`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:996-1057`؛ `1188-1199`

### P7B22T-13 — وزن عبر مدخل legacy إذا اعتمد

- **الربط:** FE7B22-07 / INV7B22-07 / P7-136؛ counterevidence-or-shared-contract.
- **المتطلبات:** إثبات مدخل ودعم من المالك ورمز 13ASCII اصطناعي ووحدة وقصد قيمة وصحة معلومة.
- **الإجراء المقترح:** بعد إذن لاحق راقب DecodeResult ثم request ثم line، لا ItemID وحده، ودون DB أو scanner إنتاج.
- **معيار القبول اللاحق:** تحفظ payload مثل 2.5 إذا كانت مقررة أو يرفض unsupported؛ لا رجوع صامت إلى 1. يظل 136 مفتوحاً حتى قبول سببه لا هذه الخطة.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1808-1916`؛ `977-1084`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1747-1810`

### P7B22T-14 — مطابقة exact قبل scale

- **الربط:** FE7B22-07 / INV7B22-07 / P7-136؛ counterevidence-or-shared-contract.
- **المتطلبات:** رمز exact ورمز scale يشتركان ببداية افتراضية، مع عقد precedence صريح ووحدة معتمدة.
- **الإجراء المقترح:** في قبول لاحق مأذون قارن الفرع والنتيجة الموسومة في القارئين دون فرض symbology أو checksum من الطول.
- **معيار القبول اللاحق:** تبقى نتيجة exact اختياراً واضحاً، ولا تفترض payload لأن الطول 13 وحده؛ لا اعتماد ماسح أو دعم legacy من اسم الدالة.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1808-1916`؛ `977-1084`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1747-1810`

### P7B22T-15 — بادئة الأساس بوحدتين ورموز فريدة

- **الربط:** FE7B22-08 / INV7B22-08 / P7-137؛ counterevidence-or-shared-contract.
- **المتطلبات:** ItemId واحد ووحدتان بهويتين ومعامل 12؛ رموز الوحدات فريدة والبادئة ترتبط برمز الأساس وفق fixture.
- **الإجراء المقترح:** بعد إذن مستقل بدل ترتيب المرشحين في fixture متحكم به وافحص UnitID/priceBasis الناتجين.
- **معيار القبول اللاحق:** تكون الوحدة المرجعية نفسها أو يرفض ambiguity بوضوح؛ لا يتغير عقد الوحدة مع ترتيب Rows[0] ولا يعاد عد 137.
- **المالك:** DBA ومالك الأمان و AuditorAPI؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1849-1885`؛ `SmartAuditERP/Class/ItemOper.cs:1962-2051`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1022-1054`

### P7B22T-16 — بادئة وحدة بعقد حاسم

- **الربط:** FE7B22-08 / INV7B22-08 / P7-137؛ counterevidence-or-shared-contract.
- **المتطلبات:** خريطة prefix→UnitId معتمدة ورمز واحد صالح ووحدة مقدار وسعر مقررتان.
- **الإجراء المقترح:** في قبول لاحق مأذون قارن الوحدة والكمية والسعر والصحة بين decode وكل مستهلك معتمد.
- **معيار القبول اللاحق:** حبيبة القيمة ووحدتها واضحتان؛ حل غموض 137 لا يختم 036 أو 142 أو إسقاط 136 اللاحق.
- **المالك:** DBA ومالك الأمان و AuditorAPI؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1849-1885`؛ `SmartAuditERP/Class/ItemOper.cs:1962-2051`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1022-1054`

### P7B22T-17 — فشل جزء أو كل payload

- **الربط:** FE7B22-09 / INV7B22-09 / P7-138؛ counterevidence-or-shared-contract.
- **المتطلبات:** صيغة scanner وثقافة مصرح بهما وأجزاء ASCII مقصودة بنتائج تحويل مضبوطة بالفشل، لا جهاز فعلي الآن.
- **الإجراء المقترح:** بعد إذن مستقل افصل صحة كل جزء عن قيمته 0، وتتبع mutation في مستهلك معتمد فقط.
- **معيار القبول اللاحق:** لا قيمة مثل 0.25 مستنتجة من نصف صالح بلا فشل معلن، ولا qty1 افتراضية لحمولة فاشلة؛ لا إغلاق 138 من نموذج Python.
- **المالك:** مالك الثقافة و Excel/provider والتشغيل و WPF؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:43-58`؛ `1849-1885`؛ `SmartAuditERP/Class/ItemOper.cs:1908-2091`

### P7B22T-18 — تمييز صفر صالح من unknown

- **الربط:** FE7B22-09 / INV7B22-09 / P7-138؛ counterevidence-or-shared-contract.
- **المتطلبات:** قاموس health وقاعدة صفر يقررهما المالك، دون افتراض قبول أو رفض الصفر؛ fixtures منقحة بلا أعمال.
- **الإجراء المقترح:** بعد إذن لاحق قارن valid zero و unknown barcode وفشل provider دون خلط أو تحويل صامت.
- **معيار القبول اللاحق:** كل حالة تعاد بصحة واضحة وحارس ذي دلالة؛ نجاح هوية الصنف ليس برهان نجاح الحمولة الرقمية.
- **المالك:** مالك الثقافة و Excel/provider والتشغيل و WPF؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:43-58`؛ `1849-1885`؛ `SmartAuditERP/Class/ItemOper.cs:1908-2091`

### P7B22T-19 — نمط 3 إذا كان معتمداً في هذا المدخل

- **الربط:** FE7B22-10 / INV7B22-10 / H7B22-03؛ counterevidence-or-shared-contract.
- **المتطلبات:** مصفوفة دعم منقحة و fixture رمز سعر أو كمية بنمط 3 في المدخل المقصود؛ لا حكم بوجوب الدعم الآن.
- **الإجراء المقترح:** بعد إذن مستقل قارن القارئين وفق capability المطلوبة فعلاً، مع exact lookup كتحكم.
- **معيار القبول اللاحق:** supported يحفظ القصد و unsupported يرفض صراحة؛ لا تصبح branch غائبة finding جديدة دون عقد الدعم والمدخل.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1849-1916`؛ `SmartAuditERP/Class/ItemOper.cs:1962-2051`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:905-925`

### P7B22T-20 — نمط 3 غير معتمد أو اختيار فقط

- **الربط:** FE7B22-10 / INV7B22-10 / H7B22-03؛ counterevidence-or-shared-contract.
- **المتطلبات:** قرار مالك منقح يحدد selection-only أو unsupported، والرسائل والنتائج المتوقعة.
- **الإجراء المقترح:** عند قبول لاحق مأذون افحص الرسالة والنتيجة وعدم mutation المضللة، دون scanner/SDK فعلي في هذه المرحلة.
- **معيار القبول اللاحق:** الدعم متسق ومعلن؛ لا ادعاء وجوب نمط 3 للعقود أو إغلاق 136–138 بمجرد تصنيف unsupported.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1849-1916`؛ `SmartAuditERP/Class/ItemOper.cs:1962-2051`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:905-925`

### P7B22T-21 — خريطة الأعمدة وعقد dtInvSel

- **الربط:** FE7B22-11 / INV7B22-11 / P7-144؛ counterevidence-or-shared-contract.
- **المتطلبات:** مخطط ملف اصطناعي منقح وموافقة mapping للحقول الخمسة، بلا ملف أعمال أو Excel حي الآن.
- **الإجراء المقترح:** بعد إذن مستقل اختبر رأساً مبدلاً ودقة كسور والوحدة والحقول وربط صف المصدر، قبل استهلاك البنود.
- **معيار القبول اللاحق:** كل صف له source-row-id وصحة وخريطة قابلة للمراجعة؛ اسم quntity المحلي لا يفترض alias خارجياً أو قبول صيغة ملف.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmcontract.xaml:1001-1022`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:185-206`؛ `2500-2550`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:370-382`؛ `429-442`؛ `996-1057`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml:439-452`؛ `601-609`

### P7B22T-22 — إلغاء wizard أو قائمة فارغة

- **الربط:** FE7B22-11 / INV7B22-11 / P7-144؛ counterevidence-or-shared-contract.
- **المتطلبات:** fixture لـ ISDone=false أو صفوف خالية، بلا كتابة master أو invoice؛ الحارس معروف من المصدر.
- **الإجراء المقترح:** في قبول لاحق مأذون قارن بنود العقد قبل الأمر وبعده، وافصل هذه الحالة عن إلغاء duplicate بعد ISDone=true.
- **معيار القبول اللاحق:** لا يضيف الحارس ولا يعدل في الحالتين؛ نجاحه لا يثبت أن 144 عولج عند إلغاء تكرار بند قائم لاحقاً.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/frmcontract.xaml:1001-1022`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:185-206`؛ `2500-2550`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:370-382`؛ `429-442`؛ `996-1057`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml:439-452`؛ `601-609`

### P7B22T-23 — إغلاق حوار التكرار دون قرار

- **الربط:** FE7B22-12 / INV7B22-12 / P7-144؛ counterevidence-or-shared-contract.
- **المتطلبات:** fixture آمنة لـ Action0 مع وجود A أخيراً؛ لا افتراض توقيت modal أو Hide من النموذج.
- **الإجراء المقترح:** بعد إذن لاحق تتبع no-selection عند الحوار و loader و import projection، مع مقارنة النسخة الأصلية.
- **معيار القبول اللاحق:** لا تتغير البنود ولا ينشر الصف applied عند عدم الاختيار؛ لا يكفي return محلي إذا استمر caller في تعديل آخر بند.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/MsgExistItem.xaml:127-134`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:9-18`؛ `48-53`؛ `SmartAuditERP/Class/ItemOpercontract.cs:1025-1035`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1747-1762`؛ `2524-2543`

### P7B22T-24 — رفض الإدراج مع بند مطابق في موضعين

- **الربط:** FE7B22-12 / INV7B22-12 / P7-144؛ counterevidence-or-shared-contract.
- **المتطلبات:** قائمتا A/B و B/A ونفس قرار Action3 ونفس صف import؛ مصدر متاح، مع حالة فشل منفصلة في fixture.
- **الإجراء المقترح:** بعد إذن مستقل قارن قبل/بعد وحالة النتيجة في الموضعين، ثم افصل failed عن cancelled.
- **معيار القبول اللاحق:** الرفض لا يعتمد ترتيب القائمة ولا يتحول إلى overwrite حين A آخر؛ الفشل له نتيجة متميزة ولا نجاح مجمل يخفيه.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Form_WPF/MsgExistItem.xaml:127-134`؛ `SmartAuditERP/Form_WPF/MsgExistItem.xaml.cs:9-18`؛ `48-53`؛ `SmartAuditERP/Class/ItemOpercontract.cs:1025-1035`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1747-1762`؛ `2524-2543`

### P7B22T-25 — عزل تجاوز resolver عن إسقاط العميل

- **الربط:** FE7B22-13 / INV7B22-13 / P4-026;P7-142؛ counterevidence-or-shared-contract.
- **المتطلبات:** resolver اختباري يعيد quote صحيحة لوحدة U2، وصف عميل U1 مختلف؛ عقد وحدات وأولوية مقرر.
- **الإجراء المقترح:** بعد إذن مستقل ثبت صحة خرج resolver أولاً ثم طبق customer projection وقارن الوحدة والمصدر.
- **معيار القبول اللاحق:** لا يختم 142 بأن 026 أصلح؛ كل سبب له invariant وقبول مستقل دون مضاعفة عد النتائج أو فرض أولوية من Python.
- **المالك:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1481-1579`؛ `1331-1366`؛ `SmartAuditERP/Class/ItemOper.cs:733-811`؛ `983-1041`

### P7B22T-26 — الفروع 2/3/23 والعميل

- **الربط:** FE7B22-13 / INV7B22-13 / P4-026;P7-142؛ counterevidence-or-shared-contract.
- **المتطلبات:** تعريف enum خارجي منقح ومصفوفة نوع×تسعير×وحدة من المالك، دون استخراج DLL تنفيذي.
- **الإجراء المقترح:** بعد إذن لاحق افحص existing ItemUnits وفشل lookup و fallback و customer override في fixtures معزولة.
- **معيار القبول اللاحق:** سلوك كل نوع ومصدر سعره موثق؛ لا استنتاج لقيم Pricing من ترتيب UI ولا قول إن type23 يشتري في كل الفروع.
- **المالك:** المحاسب ومالك الوحدة والتسعير والمخزون و HR؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1481-1579`؛ `1331-1366`؛ `SmartAuditERP/Class/ItemOper.cs:733-811`؛ `983-1041`

### P7B22T-27 — صلاحية أمر وبيانات مفوضة

- **الربط:** FE7B22-14 / INV7B22-14 / P1-011;P4-014;P7-132؛ counterevidence-or-shared-contract.
- **المتطلبات:** مصفوفة دور×أمر×فرع×مورد منقحة وبيئة اختبار لا تتصل بإنتاج، قبل أي قبول تشغيلي.
- **الإجراء المقترح:** بعد إذن مستقل افحص رفض الاستيراد والبحث قبل mutation عند غياب الصلاحية، ولا تعتمد إخفاء MenuItem وحده.
- **معيار القبول اللاحق:** الرفض عند حد موثوق وبهوية سياق معلومة؛ لا تقاس صلاحية الخادم من UI أو Apply، ولا تستنتج تجربة تجاوز من القراءة الساكنة.
- **المالك:** DBA ومالك الأمان و AuditorAPI؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1808-1916`؛ `1331-1366`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1764-1810`؛ `2500-2550`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:1188-1199`

### P7B22T-28 — بوابة الحفظ المالية والمخزنية النهائية

- **الربط:** FE7B22-14 / INV7B22-14 / P1-011;P4-014;P7-132؛ counterevidence-or-shared-contract.
- **المتطلبات:** schema وعقد stock/GL/save وإذن مستقل قبل أي عمل تشغيلي؛ 014/132potential و 020/021 محفوظة.
- **الإجراء المقترح:** في قبول لاحق مأذون فقط قارن validation لكل البنود بنتيجة writer النهائية؛ لا يجرب حفظ أو SQL في هذه المرحلة.
- **معيار القبول اللاحق:** لا نجاح مالي من Python أو صحة سعر واحد؛ potential لا تصبح confirmed دون دليلها، ولا تزول حواجز الإنتاج بتقدم import.
- **المالك:** DBA ومالك الأمان و AuditorAPI؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:1808-1916`؛ `1331-1366`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1764-1810`؛ `2500-2550`؛ `SmartAuditERP/Form_WPF/frmImportDataGeneral.xaml.cs:1188-1199`

### P7B22T-29 — تكرار الصنف بوحدتين

- **الربط:** FE7B22-15 / INV7B22-15 / P7-143;P7-144؛ counterevidence-or-shared-contract.
- **المتطلبات:** عقد قرار دمج لمفتاح ItemId/UnitId/price/serial معلن، مع هوية طلب وصف مصدر ثابتتين.
- **الإجراء المقترح:** بعد إذن مستقل حدد المفتاح والنتيجة لكل صف مستورد دون الاعتماد على موضعه، وافصل الطلب عن تسعير الوحدة.
- **معيار القبول اللاحق:** الدمج فقط وفق العقد؛ غيره رفض أو بند جديد بقرار مصادق. Count ليس بديلاً عن LineRef ولا سياسة دمج بذاته.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:977-1084`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1747-1762`؛ `2500-2550`

### P7B22T-30 — إعادة طلب وفشل جزئي

- **الربط:** FE7B22-15 / INV7B22-15 / P7-143;P7-144؛ counterevidence-or-shared-contract.
- **المتطلبات:** request-row-id وحالات cancelled/failed/retry وقواعد دقة كمية وسعر منقحة؛ fixtures لا أعمال.
- **الإجراء المقترح:** بعد إذن لاحق كرر طلباً وافشل منتصف دفعة متحكم بها مع مراقبة نسخة البنود والنتائج، دون إنتاج.
- **معيار القبول اللاحق:** نتيجة كل صف منسوبة ولا تضيع في success مجمل؛ لا idempotency مفترضة ولا اعتماد إعادة محاولة من غياب exception فقط.
- **المالك:** مالك WPF والعقود و ItemOper والاستيراد والمنتج؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `SmartAuditERP/Class/ItemOpercontract.cs:977-1084`؛ `SmartAuditERP/Form_WPF/frmcontract.xaml.cs:1747-1762`؛ `2500-2550`

### P7B22T-31 — حزمة عقود منقحة بإصدارات

- **الربط:** FE7B22-16 / INV7B22-16 / H7B22-01;H7B22-02;H7B22-04;H7B22-05؛ documentary-boundary.
- **المتطلبات:** وثائق وحدات وتسعير و SDK/schema/manifest وموافقات ملاكها فقط، لا connection أو credentials.
- **الإجراء المقترح:** خطة مراجعة لاحقة لـ crosswalk والحدود والاختلافات قبل قبول تطبيقي؛ لا تحميل مكونات تنفيذية في هذه المرحلة.
- **معيار القبول اللاحق:** كل حقل priceUnit/LineRef/health له عقد منسوب أو تعذر معلن؛ لا تخمين سعر مطبوع أو تعريف enum من اسم خاصية.
- **المالك:** مالك التقارير والنشر و SDK/UtilitiesProj؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `none-documentary-metadata`

### P7B22T-32 — عقد مفقود أو متعارض

- **الربط:** FE7B22-16 / INV7B22-16 / H7B22-01;H7B22-02;H7B22-04;H7B22-05؛ documentary-boundary.
- **المتطلبات:** fixture وثائقية تمثل عقداً مفقوداً وآخر متعارضاً، وليست بديلاً عن موافقة مالك أو capture حقيقي.
- **الإجراء المقترح:** في مراجعة وثائقية لاحقة تحقق من blocked/owner/input/impact/next-step لكل بقية دون تعديل الأصل المجمد.
- **معيار القبول اللاحق:** لا تتحول external-handoff إلى approved، ولا يحل fixture مصطنع محل سياسة حقيقية أو تعريف نشر أو سجل stdout.
- **المالك:** مالك التقارير والنشر و SDK/UtilitiesProj؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `none-documentary-metadata`

### P7B22T-33 — نسب الأدلة والتقاط الوضع التاريخي

- **الربط:** FE7B22-17 / INV7B22-17 / H7B22-06؛ documentary-boundary.
- **المتطلبات:** 313 صفاً/raw314CRLF و G200 و 613 مادة و 827 بصمة وثلاثة freezes، وهويات source10ba/entryb1f/capturec2c.
- **الإجراء المقترح:** خطة قراءة فروق الهويات ومدخل OWN B21 وكل 36 أصلية، دون توليد أرشيف بديل أو تغيير ALLnext_phase.
- **معيار القبول اللاحق:** لا overwrite للأرشيف أو rebaseline؛ المنقول له hash و lineage، وحالة التاريخ لا تستبدل بإحصاءات live316.
- **المالك:** مالك نطاق التدقيق والمنتج والتوثيق؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `none-documentary-metadata`

### P7B22T-34 — خارج العينة وقرار النطاق التالي

- **الربط:** FE7B22-17 / INV7B22-17 / H7B22-06؛ documentary-boundary.
- **المتطلبات:** SP01/02/03 وقائمة ملاك ومدخلات منقحة وحدود خروج وقبول لاحق مشروط؛ لا قائمة 411 مهمة C.
- **الإجراء المقترح:** خطة اختيار قدرة R4g/7B23 أو split مسبب؛ كل خارج ينسب إلى سبب ومالك وخطوة، لا عدد مسارات كدليل إتمام.
- **معيار القبول اللاحق:** غير المراجع معلن؛ لا نقل صامت إلى 7C أو وعد مدة أو اكتمال نظام من 12 مساراً أو 455FE أو 477scan.
- **المالك:** مالك نطاق التدقيق والمنتج والتوثيق؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `none-documentary-metadata`

### P7B22T-35 — الأجنحة التاريخية والافتراضي الحالي

- **الربط:** FE7B22-18 / INV7B22-18 / H7B22-06؛ documentary-boundary.
- **المتطلبات:** B21 كل 36 بطفل presetB21 و B20/32 و B19/36 و B18/28؛ APIdefaultB15 مستقل عن actualCLI B22.
- **الإجراء المقترح:** خطة قراءة النتائج وقائمة الحالات دون protected edits أو skip أو globalpatch أو overlay؛ فصل fixture schema عن تشغيل 27 الفعلي.
- **معيار القبول اللاحق:** وضع ومدخل كل run واضحان؛ null هو aggregate غير مبلغ عنه لا 0. حالات checker لا تصبح قبولاً تجارياً للخطط 36.
- **المالك:** مالك نطاق التدقيق والمنتج والتوثيق؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `none-documentary-metadata`

### P7B22T-36 — الإذن وبقاء القبول غير منفذ

- **الربط:** FE7B22-18 / INV7B22-18 / H7B22-06؛ documentary-boundary.
- **المتطلبات:** موافقة مستقلة لـ Windows/SQL/SDK/طابعة/ماسح أو إصلاح أوقياس قبل أي نشاط منها، دون أسرار الآن.
- **الإجراء المقترح:** خطة متابعة وثائقية للتأكد من بقاء 7C/8 والحواجز والملاك والخطوات، لا تشغيل ERP أو أعمال في هذه المرحلة.
- **معيار القبول اللاحق:** كل 36 خطة not-executed؛ 7C لم تبدأ و 8 غير مأذونة. لا إصلاح أو قياس أو قبول من نجاح 606 حالة مدقق أو من commit/push.
- **المالك:** مالك نطاق التدقيق والمنتج والتوثيق؛ **الحالة:** not-executed.
- **الأمان:** خطة فقط not-executed. أي Windows/C#/WPF/SQL/Excel/SDK/طباعة/ماسح/تعديل/قياس يحتاج إذناً مستقلاً وبيئة معزولة ومصادر و fixtures موثوقة؛ لا إنتاج أو أسرار. أمثلة Python ليست تنفيذ هذه الخطة.
- **الدليل:** `none-documentary-metadata`

## 6. إعادة فحص وثائق آمنة بلا إعادة الأرشيف

```bash
python3 -B docs/audit/tools/validate_audit.py
python3 -B docs/audit/tools/validate_audit.py --phase7-part B22
python3 -B docs/audit/tools/validate_audit.py --phase7-part B21
python3 -B docs/audit/tools/run_historical_amountword_tests_07B22.py --through-part B21
python3 -B docs/audit/tools/run_historical_barcode_tests_07B21.py --through-part B20
python3 -B docs/audit/tools/run_historical_navigation_tests_07B20.py --through-part B19
python3 -B docs/audit/tools/run_historical_caller_request_tests_07B19.py --through-part B18
python3 -B docs/audit/tools/check_contract_item_witnesses.py
python3 -B docs/audit/tools/test_contract_item_audit_validator.py
python3 -B docs/audit/tools/collect_baseline.py --verify
git -c core.whitespace=cr-at-eol diff --check
```

إذا حفظت إعادة الفحص فإلى `/tmp`، لا فوق checks أو freezes أو witness أو history رسمية بعد push. يلتقط أرشيف B22 الرسمي stdout الحقيقي مباشرة عند إنشائه، دون تحويل JSON أو تعديل flags أو self-hash. فتح stream الوجهة حصرياً لـ stdout ليس تعبئة ملف placeholder يدوياً. **7B/7 جزئيتان؛ R4f محدود بهذه الشريحة لا كل R4/SP03؛ R4g/7B23 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.**
