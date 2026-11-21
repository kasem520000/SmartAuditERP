# حصر 7B: القدرة والمدخل والمصدر والمخرج

هذا **مقترح مقام عمل** يتيح الوصول إلى قرار نهاية قابل للدفاع عنه؛ ليس إعلان اكتمال أو موافقة مستخدم مفترضة. يفسر [تقرير الحالة](PHASE-07B38.md) الفرق بين التسليم الحالي والمهمة الكاملة. المرجع الحاكم2026-11-16 UTC، ومصدر التطبيق10ba215، ودخول المتابعة0423c61.

## 1. المقامات المختلفة

| المادة | معناها الصحيح |
|---|---|
| 797 FE عبرB1–B37 | صفوف تقييم/بوابات/إحالات متداخلة ذات أنساب، لا ميزات فريدة |
| 26 قدرة مقترحة | تقسيم دلالي للعمل بحدود واضحة، **غير معتمد بعد** |
| 52 شاشة+3 توضيحات | بذور تاريخية معلنة، لا كل التقارير المستنتجة من regex |
| 477 C# و277 XAML | ملفات source-kind في الحصر الأصلي؛ لا14 ملفC# مولداً ضمن مقام parse |
| 8997 تصريحاً | method/constructor/local function/operator-like syntax؛ لا8997 واجباً وظيفياً |
| 4409 مواضع اكتشاف | مرشحات بالاسم/النوع المكتوب؛ ليست call graph أو4409 إخفاقات/قدرات |
| 49 إنشاء حوار | حالات مباشرة محددة داخل47 owner، لا كل آليات الإنشاء الديناميكي |

المرشحات4409 تشمل **3419 `Show` و552 `ShowDialog` و200 نداء آخر و238 إنشاءً**. تتضمن `Show` أسماء متشابهة مثل صناديق الرسائل، ويشمل استخراج الأنواع صفوف DTO محلية في ملفات البذور. **لا نطلب تدقيق كل4409 كميزات7B مستقلة**؛ يلزم فرز قائم على المدخل/المصدر/المخرج تحت مقام معتمد، دون إسقاط المجهول بالاسم وحده. وجود مصنع أو alias أو reflection أو XAML activation أو نداء غير مختار بالاسم يظل قيداً على الشمول.

## 2. سجل القدرات المقترح

[CSV الكاملة](evidence/capability-register-07B38.csv) تحمل لكل صف: capability،entry،source،output،exclusions،owner،required input،absence impact،next action،static exit،وإحالات. الروابط إلى FE على مستوى الجزء **many-to-many للتنقل**، لا تصديق دلالي مستقل لكل صف.

| القدرة | عائلة العمل | الحد الحاسم |
|---|---|---|
| D01 | محركات التقرير والطباعة والتصدير | overload/channel/copies/outcome وconsumer |
| D02 | إسقاط الفاتورة للطباعة | source→row→DTO→table→template؛ نقاء المعاينة ونسخة المصدر |
| D03 | الباركود والوحدة والملصق | هوية الوحدة وpayload/health وسعر وكمية الملصق |
| D04 | التفقيط والعملة والدقة والقديم | culture/precision/sign/fraction والتحويل المستخدم فعلاً |
| D05 | أرصدة وكشوف الحساب والسنة | قاعدة السنة وهوية الحساب/المستند والمعيار |
| D06 | ميزان المراجعة والصندوق والمركز | السابق/الفترة/الختامي وعضوية الشجرة/المركز والقطع الزمني |
| D07 | الدخل والميزانية والتقييم | current/period/as-of ومصدر المخزون الآلي/اليدوي |
| D08 | المخزون والحركة والصلاحية | unit/grain/cost/expiry/branch والطفل والمخرج |
| D09 | التحليل والربح والفئات واليومية | source-set/sign/discount/grain/denominator والملخص |
| D10 | تفاصيل البيع وPOS وأندرويد | saved/current VAT وsnapshot وأوامر الدفع/الطرف |
| D11 | المشتريات والإشعارات | amount-vs-percent ومخزن/خزينة/فرع وصيغة التصدير |
| D12 | القرار والملخصات وسجل المستخدم | NULL/zero واللغة وrequest generation وقصد الأوامر |
| D13 | المندوب والمبيعات والتحصيل | القيمة/الصافي/العمولة/الربح/التحصيل مقاييس مستقلة |
| D14 | الإنتاج والتأجير والسيريال والبحري | حبيبة مصدر كل تقرير وDTO والقالب والـlauncher |
| D15 | السندات والراتب والاستحقاق | period/eligibility/child/save-set وهوية الموظف |
| D16 | الضرائب والإقرار وتفاصيل الطفل | source/category/rate/discount/branch وعدم فرض مساواة الأب والطفل |
| D17 | هوية المستند والتنقل والأطفال | DocumentRef وallowed-set وFound/Empty/Failed/Partial |
| D18 | منتقي الأصناف والسلة | single/multi/cancel/invalid وملكية القائمة لكلcaller |
| D19 | استيراد البنود والتحضير والدمج | LineRef/OwnedSeed/CopyIntent/AcceptedLines وحد النشر |
| D20 | الخصائص والتعديل العام والتسعير | وحدات FillRatio/FillValue والأبعاد وPropertiesResult/BulkPatch |
| D21 | منتقي الفاتورة والرجوع والأهلية | request/result/Return وحقول الهوية والقارئ لكلcaller |
| D22 | ترك المسودة والجديد والإغلاق | Save/Discard/Stay منفصل عن قبول هدف ونجاح تحميله |
| D23 | قصد الإخراج والإعدادات والمشاركة | OutputIntent/bytes/ownership/partial/retry لاDelivered |
| D24 | SDK وDTO والمحولات والقوالب | known-local/supplied/unresolved وmanifest/version/hash |
| D25 | المخطط والمنح وهوية الفرع | schema/keys/constraints/grants وأدوار×أوامر×موارد |
| D26 | الحصر والنسب والاستبعاد وقرار النهاية | مقام متفق عليه وتقييم كل التزام وقرار أسرة مستقل |

كل حقل `whole_capability_certified` و`local_semantic_obligations_complete` في **هذا الإصدار** false: يعني عدم إثبات إتمام القدرة كلها، لا أن كل مصادرها غير مقروءة أو أن كل عملها لم يبدأ. لا تُمحى التقييمات التاريخية الناجزة.

## 3. نسب797: ما الذي حفظناه بالضبط؟

[feature-lineage](evidence/feature-lineage-07B38.csv) تربط كل صف من الملفات37 بالترتيب نفسه، مع:

- path وSHA-256 لملف الأصل، وordinal وid وSHA لقاموس الصف.
- القاموس الأصلي كاملاً في `canonical_row_json` دون إسقاط status/depth/limit/evidence/acceptance أو تحويل deferred إلى implemented.
- الأدلة وخطط القبول الأصلية منفصلة، مع وصف صريح أن الفهرسة ليست source rereview.
- ربط أول455 بهويات [دفترB17](evidence/capability-ledger-07B17.csv) المستهلك دون إعادة كتابته.

خوارزمية rowSHA: JSON بمفاتيح مرتبة وUTF-8 و`ensure_ascii=False` وseparators المضغوطة، ثمSHA-256. تطابق hash القاموس ليس قبولاً لصحة الأعمال.

## 4. المصدر وXAML وحدود القراءة

[لقطة الاكتشاف](evidence/capability-census-07B38.json) تسجل المصدر/الترميز/البصمة وعدد الأسطر والتصريحات ومواضع النداء المحتملة وسِمات XAML. محللC# هوTree-sitter0.25.2 معgrammar0.23.1؛ XAML قراءةXML بمكتبةPython. صفر parse errors ليس بناء .NET/WPF أو حسم overload أو references أو BAML/SDK.

حُسب اتحاد النطاقات التاريخية مع **قبول singleton** مثل `332`، لا المديات `a-b` فقط. بالنسبة إلى55seed، يغطي اتحاد **المديات المعلنة تاريخياً** كل أسطر أجسام C# المحلية؛ وتبقى فجوات مدياتXAML في19ملفاً. هذا وصف لدفاتر القراءة، لا برهان أن كل سطر/قدرة راجعه هذا الإصدار أو أن كل XAML-gap خلل واجهة. [ربط55](evidence/screen-crosswalk-07B38.csv) يحفظ المديات نفسها دون إسقاط.

تتضمن818سمّة مدخل محتملة في55seed أسماء تطابق method declarations في codebehind المحلي. لا اسم handler مفقود في **هذا الاستخراج المحدد**؛ لكن الربط البرمجي والإرث وtemplates/commands وdispatch والإذن لا تُحسم من ذلك، ولا نحول المعالج الفارغ إلى قدرة واجبة بلا قصد منتج.

[نطاق القراءة الحالية43](review-scope-07B38.csv) مستقل تماماً عن الاكتشاف. يضم47owner محلياً للحوارات49، ومقاطع دخول ومساعدات معلنة. قُرئت أجسام `Number2Arabic`328 و`RptRentInvData`125 و`listItemBarcode`10 و`InvPrinter`12 محلياً كاملة، و`frmItemsSrch`617. **لا ننقل هذه الصفة إلىSDK أو كل caller أو whole family**.

في `RptRentInvData` يشترك `Marine` و`Marine1` صراحة في `_marine` مع null→empty محلي؛ أما بقية auto-properties المهيأة فليست مخططREPХ خارجياً. `InvPrinter.cs` يعرف محلياً `InvPrinter1`؛ التشابه بالاسم ليس حسم resolution لنداء `InvPrinter` آخر. `Number2Arabic.ameral` مسار محلي مستقل له parsing/catch؛ وجوده لا يساوي استعماله ولا يغير نتائج034/035 أو سياسة العملة.

## 5. إعادة الإنتاج والأثر التاريخي

الأدوات الجديدة تحت `tools/census07b/` ولا تغيّر الـ139 أداة العليا المحمية أو dispatcherB37. سجل [فصل namespace](evidence/census-tool-namespace-note-07B38.json) انتقال builder الجديد قبل الإنهاء وتغير عمق مساره فقط؛ **أعيد بناء اللقطة كاملة في الذاكرة وقورنت**، لا تعديل snapshot مستهلك أو إعادة ترتيب hashes لتبدو سابقة.

```sh
python -m pip install --target /tmp/audit-parser -r docs/audit/tools/census07b/requirements-census-07B38.txt
PYTHONPATH=/tmp/audit-parser python -B docs/audit/tools/census07b/validate_7b_completion.py --reparse
python -B docs/audit/tools/census07b/test_7b_completion.py
python -B docs/audit/tools/census07b/validate_7b_completion.py --require-complete
```

الأخير يرجع2 ما دامت بوابة النهاية محجوبة؛ لا تتعامل معه كنجاح كامل7B. الـbuilder يكتب إلى **مسار جديد حصري فقط** ويرفض الكتابة فوق لقطة موجودة. عند تحديث نطاق/مصدر/قرار لاحق يجب إنشاء إصدار جديد ومحاسبة مصدره، لا تعديل الأدلة المستهلكة أو الادعاء أن الموافقة أو التصحيح كانا قائمين عند التقاط سابق.
