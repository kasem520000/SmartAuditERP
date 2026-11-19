# التحقق التوثيقي وخطط القبول غير المنفذة — 7B19

مرجع التدقيق المعلن **2026-11-16 UTC**. مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B19 يلي دفع B18 المكتمل `ee393a741a862a605c6c2f688d3f634bd91856ae` بجميع **528 ملف تدقيق**. ساعة التجميد المرصودة `2026-11-19T03:37:39.154596+00:00` مستقلة عن المرجع، لا تشغيل تطبيق في أي منهما.

**7B/7 جزئيتان؛ R4c سُلّم بحدوده لا كل R4، وR4d/7B20 مقترح؛7C لم تبدأ؛8 غير مأذونة ولم تبدأ.** لا تشغيل أو بناء ERP/C#/SQL/VB/WPF/SDK/DTO/REPX/Office/COM أو مفسر أو مزود أو جهاز أو طابعة أو تصدير أعمال أو shell للتطبيق. لا بيانات أعمال حقيقية أو أسرار أو إصلاح أو قبول أو قياس تشغيلي. Python/Git لأدوات الوثائق فقط؛ `next_phase=8` ليس إذناً.

[النتيجة](PHASE-07B19.md) · [عقود التوجيه والاستقبال](NAVIGATION-CONTRACTS-07B19.md) · [التحقق والخطط](VALIDATION-07B19.md) · [المتبقي](PHASE-07-REMAINING-07B19.md) · [scope23](review-scope-07B19.csv) · [السجل](findings.csv) · [provenance523](evidence/provenance-07B19.json) · [stdoutB19](evidence/checks-07B19.json)

## 1. ما نُفذ وما لم يُنفذ

| النوع | النتيجة والحد |
| --- | --- |
|36 حالةPython جديدة|نجحت مستقلة؛ مدقق وثائق وصفوف مصطنعة ونماذج يدوية. لا تستورد التطبيق أوWPF/SQL.|
|24 وضعية تاريخيةOWN|نُفذت فعلياًthrough2–6 ثمA/B1…B18،exit0/errors=[] وبصمات827؛B18 بـOWN302/462 حالة/19 مجموعة.|
|شاهدB19|14 نموذجاً مستقلاً و14 فحصاً نصياً و68 شريحة/22مساراً؛errors=[]، لا.NET أوSQL أوcompiler/DTO منفذ.|
|المدقق الحاليB19|نجح الافتراضي وB19 الصريح: **498 حالة/20مجموعة،errors=[]**؛462 سابقة و36جديدة، مع307صف و827بصمة. [stdout الحالي](evidence/checks-07B19.json) يلتقط مباشرة، لاERP.|
|baseline --verify|نجح:827ملفاً/29,128,444بايت،XML parse errors0 وXAML name mismatches0؛dotnet_available=false. ليستbindings أوبناءWPF.|
|ERP/build/WPF/SQL/provider/printer|لم تنفذ؛ صفر. لا اختبار أعمال أو إصلاح أو قياس أو قبول تشغيلي.|
|36 خطة قبول أدناه|كلهاnot-executed؛ نجاحPython لا يغير حالتها. بعض البوابات الوثائقية عادت كحالاتمدقق فقط، لا موافقة للنظام.|

[النموذج والأدلة](NAVIGATION-CONTRACTS-07B19.md) يفصل العقد والسياسة والمخالفات والجذور القديمة. لا يفترض إصلاح054/055 أوP4-020/021 أو031 أوACL أو أصول الذرية والهوية والثقافة.

## 2. أدوات الإعادة الآمنة الآن

```bash
python3 -B docs/audit/tools/validate_audit.py
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B19
python3 -B docs/audit/tools/validate_audit.py --through-phase 7 --phase7-part B18
python3 -B docs/audit/tools/run_historical_caller_request_tests_07B19.py --through-part B18
python3 -B docs/audit/tools/test_navigation_contract_audit_validator.py
python3 -B docs/audit/tools/check_navigation_contract_witnesses.py
python3 -B docs/audit/tools/collect_baseline.py --verify
git -c core.whitespace=cr-at-eol diff --check
```

أدوات وثائق فقط؛ لا--write أو بناء أو مزود أوSQL أوطباعة. لا تعاد كتابةchecks قديمة أو تجميدات الدخول. يفتح ملفchecksB19 جديد حصرياً (`xb`) كمصبstdout للعملية الفعلية الجارية، لاplaceholder أو نسخ/تحويلJSON أو تعديلpendingflag؛لهذا يوجد مسار المخرج أثناء فحص روابطه، ولاself-hash. يبقىcheckout السجلee393a7 وقت الالتقاط لاcommit التسليم اللاحق. إعادات التحقق بعدالالتقاط/commit/push إلى/tmp فقط، ولا يعاد الأرشيف لإلحاقHEAD جديد.

### لماذاlauncher تاريخي واضح لـB18؟

الحالتان27/28 فيB18 المحمي تفحصانbuild_cli_parser والـentrypoint الفعليين معdefaultB18 وقتها. تشغيلهما كماهما فيcontext اليومB19 بلا حد تاريخي يعطي تعارض إصدار. لا يجوز تغييرهما أو إخفاؤهما أو الادعاء أنB18 هوdefault اليوم. يوجهfacade ضيق جداً الـargv المطابق لتلك المجموعة فقط إلىchild مسمى**run_historical_caller_request_tests_07B19.py --through-part B18**. داخلهPHASE7_LIVE_CLI مبني صراحة منpresetB18، وكل28 حالة أصلية تنفذ بلاskip أوfilter أو تعديل مناهج، معfinally لاستعادة الهوية. غير ذلك منsubprocess يمر دون تغيير؛ ليسpatch لـsubprocess.run العام.

يتلقىB18 صفوفOWN302 والبايتات303CRLF وفهارسه الدقيقة في الذاكرة، لا307live. يحوي سجلstdout اسمlauncher والـargv الفعلي وكونassertions تاريخية لاcurrentdefault. **تفحص36 حالةB19 الجديدة الـparser الحاليB19 والـentrypoint باستقلال**، مع عدمglobalPath/subprocesspatch وبقاء ملفB18 الأصلي بطابعه المحمي. main البرمجيةB15 وقواعد خياراتB16/B17/B18 باقية كتوافق؛ لاparser صوري أو إغلاق شكلي للاختبارات القديمة. أمرB18 المباشر أعلاه هو المدقق معOWN، وليس تشغيل ملف الاختبارات المحمي منفرداً فيcontext إصدار جديد.

## 3. مصفوفة الحالات الـ36 الجديدة

| الحالات | المطلب المختبر مصطنعاً |
| --- | --- |
| 01–07 | OWN302/exact303CRLF/indexkeys ونسخ المدخلات واستعادة الهويات عند النجاح والاستثناء وnestedOWN300؛ لاglobalPathpatch أو تراكب خارجfindings. |
| 08–10 | كل302 حقل وALLnext_phase/evidence والبادئة الخام وIDs131–135 والـCRLF وG184+6 الجديدة بلا عبث. |
| 11–15 | النص الحرفيbalanced/line/hash/arg بحدوده،22instance/19tokens/2parents/7leaves، وLC بحدود المالك والمدخل والفشل. |
| 16–19 | FE18/INV18/T36 وخطتان متعاكستان لكلعقد، روابط وعدمexecution أو تكرارcriteria، وكل14residual بـrowSHA/contract/owner/input/impact/exit. |
| 20–22 | R4c محدود و6C غير مبدوءة و3splits بسبب ومعيار وmetadata بأنواعbooleans/int صارمة وتصويبB10:10/120. |
| 23–28 | نماذج يدوية:late-reset، حارس الكمية يتجاوزBaseQty0 لا تصفيره، فرع الوحدة قد يصفر، تقريب مبكر وشاهد سليم، تاريخPOS وشاهده الإلكتروني، واستخراجCREATE خامد لاSQLparser. |
| 29–33 | الـparser الحاليB19 فعلاً وB16/B17/B18bases/mainB15،entrypoint واحد وOWNB18 قبل الحالي،facade ضيق لا عالمي،redirect للـargv المطابق فقط،child ملتزم بكل28 بلاskip وملفB18 الأصلي. |
| 34–36 | sentinels وثائقية صريحة لا سطرمصطنع،historical24 مرتبة بـstdoutSHA/null عند غيابaggregate، وحسابscope23/21/2/410/417 لاwholebody أو نسبة. |

هذه حالات لأداة الوثائق والنماذج المنقولة، لاmutation للتطبيق أو تنفيذ خطة قبول مال أو مخزون. اختبارات التاريخ الأصلية غير معدلة.

## 4. الأوضاع التاريخية المنفذة فعلياً

يحفظ[السجل24](evidence/historical-mode-verification-07B19.json) الأوامر والخروج والسجل وعدد النتائج وvalidation-scope وSHA وبايتاتstdout كما صدر، لا يعيدchecks الأصلية أو يدعي استنساخ كل مقاييسها. **null تعني أن المفتاح غير مذكور فيstdout القديم، لا0 حالة منفذة.** هذه إعادة تحقق توثيقية بمدقق حالي وOWN، لا موافقة تشغيلية للمراحل السابقة.

| الوضع | السجل الذي قرأه | النتائج | حالاتchecker / مجموعات كما وردت | الخروج |
| --- | --- | --- | --- | --- |
| phase2 | evidence/findings-through-02.csv | 49 | null / null | 0; errors=[]; hashes827 |
| phase3 | evidence/findings-through-03.csv | 74 | null / null | 0; errors=[]; hashes827 |
| phase4 | evidence/findings-through-04.csv | 106 | null / null | 0; errors=[]; hashes827 |
| phase5 | evidence/findings-through-05.csv | 137 | null / null | 0; errors=[]; hashes827 |
| phase6 | evidence/findings-through-06.csv | 172 | null / null | 0; errors=[]; hashes827 |
| A | evidence/findings-through-07A.csv | 200 | null / null | 0; errors=[]; hashes827 |
| B1 | evidence/findings-through-07B1.csv | 223 | null / null | 0; errors=[]; hashes827 |
| B2 | evidence/findings-through-07B2.csv | 237 | 44 / 3 | 0; errors=[]; hashes827 |
| B3 | evidence/findings-through-07B3.csv | 248 | 62 / 4 | 0; errors=[]; hashes827 |
| B4 | evidence/findings-through-07B4.csv | 261 | 82 / 5 | 0; errors=[]; hashes827 |
| B5 | evidence/findings-through-07B5.csv | 266 | 104 / 6 | 0; errors=[]; hashes827 |
| B6 | evidence/findings-through-07B6.csv | 270 | 132 / 7 | 0; errors=[]; hashes827 |
| B7 | evidence/findings-through-07B7.csv | 276 | 156 / 8 | 0; errors=[]; hashes827 |
| B8 | evidence/findings-through-07B8.csv | 280 | 184 / 9 | 0; errors=[]; hashes827 |
| B9 | evidence/findings-through-07B9.csv | 282 | 208 / 10 | 0; errors=[]; hashes827 |
| B10 | evidence/findings-through-07B10.csv | 285 | 236 / 11 | 0; errors=[]; hashes827 |
| B11 | evidence/findings-through-07B11.csv | 287 | 266 / 12 | 0; errors=[]; hashes827 |
| B12 | evidence/findings-through-07B12.csv | 289 | 298 / 13 | 0; errors=[]; hashes827 |
| B13 | evidence/findings-through-07B13.csv | 291 | 322 / 14 | 0; errors=[]; hashes827 |
| B14 | evidence/findings-through-07B14.csv | 294 | 350 / 15 | 0; errors=[]; hashes827 |
| B15 | evidence/findings-through-07B15.csv | 298 | 382 / 16 | 0; errors=[]; hashes827 |
| B16 | evidence/findings-through-07B16.csv | 299 | 410 / 17 | 0; errors=[]; hashes827 |
| B17 | evidence/findings-through-07B17.csv | 300 | 434 / 18 | 0; errors=[]; hashes827 |
| B18 | evidence/findings-through-07B18.csv | 302 | 462 / 19 | 0; errors=[]; hashes827 |

## 5. شواهد مستقلة وملاحظات نصية لاERP

يعيد[check_navigation_contract_witnesses.py](tools/check_navigation_contract_witnesses.py) إنشاءJSON من نماذجDecimal/datetime منقولة يدوياً ومقاطع مدرجة معhash. قيم الكسور بعيدة عنmidpoint؛ لا اعتماد لسلوكbinarydouble أوSQL أو ثقافة تاريخ. نموذجafter_lifecycle يطبق ترتيباً مفترضاً لشرح132 ولا يشغلWPF. الشاهدان المضادان مهمان:BaseQty0 يجعل حدث الكمية يتجاوز السطر لا يصفره، والموجود الإلكتروني لا يأخذ فرعNow نفسه.

البصمات المرجعية الخام:

| المادة | SHA256 |
| --- | --- |
| evidence/navigation-contract-witnesses-07B19.json | eab94591ab49ba379728beaa0d65f19e0a3a26d06fb12b4243660c3079cca836 |
| evidence/historical-mode-verification-07B19.json | c9bb8f4f1adff9df8d8ce2cb0822a0bdaf0f891ee7cbd9b2b70cb7185ea0c022 |
| evidence/checks-07B18.json | abe579df675cf7e0858eb209d8524d6c97cf663205f04b9515d2e76aade87c03 |
| evidence/findings-through-07B18.csv | 3ed75512f7f998abf3c49f2bc5d27ab6c6d37dffd6521ce59835783da28208a1 |
| evidence/shared-indexes-through-07B18.json | caef7e54e683a42ae98b80a71b7319dac31fbca3ef92a9b69068cf2569fa6c60 |
| evidence/provenance-07B19.json | 3824fc6427bfbcc8ae45fe25360b8eac6e5356e3161fd3215f558bd236765c00 |

## 6. خطط القبول الـ36 — جميعهاnot-executed

لكلخطةfixture اصطناعي ومسار ومعيار خاص وربطFE/INV/roots. أيWPF/SQL أو حفظ أو مزود أوطابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة؛ لا مدخل إنتاج أو أسرار. تحتاج المعايير المقترحة تثبيت سياسة المالك وخطة إصلاح مستقلة إن لزم، ولا تأذن بالإصلاح هنا. القوائم الوثائقية ضمن31–36 أيضاً ليست موافقاتERP.

### P7B19T-01 — عقد رأس التسوية — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-131; FE7B19-01; INV7B19-01 |
| المتطلبات والمدخل الاصطناعي | صف Inv نوع7 به GlobalID وid17 دون Is_Approved؛ وSafesAdjust17 بحالة مستقلة. |
| الخطوات لاحقاً | لاحقاً اعزل SourceRef لكل مصدر وافحص OpenSafeAdjust حتى القارئ دون حفظ. |
| معيار القبول | قراءة التسوية المقصودة أو رفض نوع المصدر قبل mutation؛ لا تحميل جزئي أو بنود تسوية أخرى. |
| الدليل | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206;SmartAuditERP/Properties/Resources.resx:954-1017;SmartAuditERP/Properties/Resources.resx:1692-1726 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-02 — عقد رأس التسوية — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-131; FE7B19-01; INV7B19-01 |
| المتطلبات والمدخل الاصطناعي | SafesAdjust17 أصلي معتمَد وبنوده، وصف مختلف يحمل رقم العرض نفسه. |
| الخطوات لاحقاً | قارن المسارين المسمّيين من التقريرين مع عقد الحقول والهوية والفشل في بيئة معزولة لاحقاً. |
| معيار القبول | ثبات المصدر والهوية وحالة الصحة؛ مجرد نجاح SELECT لرأس غير مطابق لا يكفي. |
| الدليل | SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206;SmartAuditERP/Properties/Resources.resx:954-1017;SmartAuditERP/Properties/Resources.resx:1692-1726 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-03 — التهيئة لا تستبدل المستند المحمل — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-132; FE7B19-02; INV7B19-02 |
| المتطلبات والمدخل الاصطناعي | مستند موجود ISNew=false وفرع B وتاريخ سابق لكل من Sale/Purch/POS/InputOutput/Transfer. |
| الخطوات لاحقاً | لاحقاً سجل init/load/Loaded/navigation على SDK معلوم، عند أول فتح ثم إعادة فتح من التقرير. |
| معيار القبول | لا تعود الحالة إلى الجديد أو فرع الجلسة بعد تحميل الموجود؛ الفشل لا ينشر خليطاً قابلاً للحفظ. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmInvSale.xaml:1-16;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:123-235;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1610;SmartAuditERP/Form_WPF/frmInvPurch.xaml:1-16;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:97-160;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-407;SmartAuditERP/Form_WPF/frmInvPOS.xaml:1-16;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:210-270;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:512-553;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml:1-16;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:94-130;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:162-201;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml:1-18;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:126-160;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:286-328;SmartAuditERP/Class/InvoiceOper.cs:3219-3281 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-04 — التهيئة لا تستبدل المستند المحمل — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-132; FE7B19-02; INV7B19-02 |
| المتطلبات والمدخل الاصطناعي | حالة معاكسة: تهيئة مكتملة قبل load؛ صف ناجح وآخر غائب أو مرفوض. |
| الخطوات لاحقاً | قارن Show-before-Navigate وconfigure-before-Show بإتمام Loaded الفعلي، لا بالترتيب النصي وحده. |
| معيار القبول | كلا publisher ينتهي بالحالة الصحيحة أو رفض واضح؛ الشاهد المعاكس لا يصير قبولاً لكل WPF. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmInvSale.xaml:1-16;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:123-235;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1546-1610;SmartAuditERP/Form_WPF/frmInvPurch.xaml:1-16;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:97-160;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:350-407;SmartAuditERP/Form_WPF/frmInvPOS.xaml:1-16;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:210-270;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:512-553;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml:1-16;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:94-130;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:162-201;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml:1-18;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:126-160;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:286-328;SmartAuditERP/Class/InvoiceOper.cs:3219-3281 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-05 — معامل الوصفة بعد إعادة الفتح — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-133; FE7B19-03; INV7B19-03 |
| المتطلبات والمدخل الاصطناعي | أمر محفوظ منتجه2 ومكونه8 ومعامل أساسه الاقتصادي4؛ لم يتغير BOM. |
| الخطوات لاحقاً | بعد إعادة الفتح لاحقاً غيّر كمية المنتج إلى3 وافحص BaseQty والمكون قبل أي حفظ. |
| معيار القبول | يتحجم المكون إلى12 وفق العقد أو يرفض التعديل بسبب؛ لا يبقى8 لفقد معامل القارئ. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-06 — معامل الوصفة بعد إعادة الفتح — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-133; FE7B19-03; INV7B19-03 |
| المتطلبات والمدخل الاصطناعي | الأمر نفسه، ووحدة منتج ذات perc12 ومكونات غير صفرية، بعد _isLoaded=false. |
| الخطوات لاحقاً | لاحقاً اختر الوحدة وافحص الكميات والمجاميع وأثر الإلغاء. |
| معيار القبول | لا تصفير للمكونات بمعامل وصفة افتراضي؛ الإلغاء يحفظ الأصل أو يرفض بوضوح. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-07 — دقة تحميل مكونات الإنتاج — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-134; FE7B19-04; INV7B19-04 |
| المتطلبات والمدخل الاصطناعي | مكون qty0.004 وسعر1000.004، ومرجع دقة متفق عليه غير midpoint. |
| الخطوات لاحقاً | قارن لاحقاً raw row وmodel وgrid وtotal عند الفتح دون حفظ؛ افصل القيمة عن نص N2. |
| معيار القبول | يبقى المقدار والسعر في المصدر الداخلي أو رفض دقة معلن قبل التحرير؛ لا صفر صامت من load. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-08 — دقة تحميل مكونات الإنتاج — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-134; FE7B19-04; INV7B19-04 |
| المتطلبات والمدخل الاصطناعي | qty2/price1.234، وشاهد qty2.00/price1.25 مضبوط لمنزلتين. |
| الخطوات لاحقاً | قارن subtotal قبل وبعد load والتعديل والإلغاء؛ خطط save بعد حل الحاجز بإذن إصلاح مستقل، لا الآن. |
| معيار القبول | لا خسارة دقة من التحميل وحده؛ الحالة السليمة مميزة، ولا يدعى نجاح حفظ من binding. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-09 — تاريخ إعادة حفظ POS — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-135; FE7B19-05; INV7B19-05 |
| المتطلبات والمدخل الاصطناعي | POS محفوظة بتاريخ31ديسمبر، إعداد غير إلكتروني، وصلاحية تعديل وعناصر سليمة. |
| الخطوات لاحقاً | لاحقاً عدّل ملاحظة فقط في2يناير وقارن displayed/checked date مع Invoice.InvDate و@date. |
| معيار القبول | ثبات تاريخ الإصدار31ديسمبر وفصل modified-at؛ لا نقل صامت إلى فترة التقرير الجديدة. |
| الدليل | SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1009-1028;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2170-2211;SmartAuditERP/Class/InvoiceOper.cs:1497-1535;SmartAuditERP/Class/StoredQueries.cs:6-10;SmartAuditERP/Class/InvoiceOper.cs:4186-4248 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-10 — تاريخ إعادة حفظ POS — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | finding-specific; P7-135; FE7B19-05; INV7B19-05 |
| المتطلبات والمدخل الاصطناعي | موجود إلكتروني يرفض التعديل حسب العقد، وجديد غير محفوظ، وساعتان اصطناعيتان معلومتان. |
| الخطوات لاحقاً | قارن فروع ISNew/electronic/allowed/denied مع إبقاء حراس الدفع والنشر صريحة. |
| معيار القبول | الجديد يأخذ تاريخ إصداره المقرر والموجود يحفظ أصله أو يرفض؛ لا تعميم لكلPOS أو قبول ضريبي. |
| الدليل | SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1009-1028;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2170-2211;SmartAuditERP/Class/InvoiceOper.cs:1497-1535;SmartAuditERP/Class/StoredQueries.cs:6-10;SmartAuditERP/Class/InvoiceOper.cs:4186-4248 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-11 — هوية المستند لا label/رقم — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P7-061; FE7B19-06; INV7B19-06 |
| المتطلبات والمدخل الاصطناعي | فرعان A/B لهما id7 من النوع نفسه وأسماء عرض بلغتين. |
| الخطوات لاحقاً | لاحقاً افتح صف كل تقرير بعد تغيير اللغة ومرشح الفرع مع تتبع المرجع. |
| معيار القبول | لا استهداف لفرع آخر أو تعطل من ترجمة label؛ source/branch جزء من الهوية. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:285-309;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmRptInventory.xaml:454-486;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml:708-720 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-12 — هوية المستند لا label/رقم — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P7-061; FE7B19-06; INV7B19-06 |
| المتطلبات والمدخل الاصطناعي | GlobalID مختلفان مع local7، وإحداهما خارج allowed-set. |
| الخطوات لاحقاً | قارن مرجع query وrow مع الأدوار والموارد في schema اصطناعي معلوم. |
| معيار القبول | تمييز الهوية لا يستبدل رفض المورد غير المسموح؛ GlobalID ليس بوابة تفويض. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:285-309;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmRptInventory.xaml:454-486;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml:708-720 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-13 — حراس UI لا تثبت تفويض الحفظ — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; P1-013;P2-001;P2-006;H7B19-04; FE7B19-07; INV7B19-07 |
| المتطلبات والمدخل الاصطناعي | CanAdd=true/CanEdit=false والعكس، وفواتير فرعين وprincipal معلوم. |
| الخطوات لاحقاً | لاحقاً اختبر click/shortcut/alternate caller للقراءة والتعديل مع deny خارج النطاق. |
| معيار القبول | رفض موحد لا يحول update إلى create بflag UI؛ تعطيل زر ليس الدليل الوحيد. |
| الدليل | SmartAuditERP/Class/Common.cs:1435-1490;SmartAuditERP/Class/FormPermission.cs:38-178 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-14 — حراس UI لا تثبت تفويض الحفظ — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; P1-013;P2-001;P2-006;H7B19-04; FE7B19-07; INV7B19-07 |
| المتطلبات والمدخل الاصطناعي | منح غائبة أو استثناء مصدر permissions ومورد غير تابع. |
| الخطوات لاحقاً | راجع مع DBA والأمان عقد deny/allowed-set ثم خطط fault injection في بيئة معزولة لاحقاً. |
| معيار القبول | فشل المنح لا يوسع الصلاحية؛ رفض موثق بلا أسرار أو وصول إنتاج مطلوب. |
| الدليل | SmartAuditERP/Class/Common.cs:1435-1490;SmartAuditERP/Class/FormPermission.cs:38-178 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-15 — حارس المسودة وحد نشر جديد — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-03; FE7B19-08; INV7B19-08 |
| المتطلبات والمدخل الاصطناعي | نافذة مستقبل جديدة من التقرير ولا حالة مسودة سابقة لها. |
| الخطوات لاحقاً | تحقق لاحقاً من new-instance والملكية، ولا تستنتج فقد بيانات من عدم prompt. |
| معيار القبول | عدم ظهور prompt في fresh-window ليس فشلاً؛ لا finding من غياب الحارس المحلي فقط. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1663-1682;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:506-546;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:523-544;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-16 — حارس المسودة وحد نشر جديد — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-03; FE7B19-08; INV7B19-08 |
| المتطلبات والمدخل الاصطناعي | محرر معاد الاستعمال بمسودة وإلغاء المستخدم، إن كان هذا مدعوماً. |
| الخطوات لاحقاً | تتبع caller المعاد استعماله قبل CLR ضمن SP01 المعلن لاحقاً. |
| معيار القبول | الإلغاء يبقي الهوية والبنود؛ خارج NV22 يظل split ولا مراجعة مزعومة. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1663-1682;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:506-546;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:523-544;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-17 — صحة المحمل: لا صف أم فشل — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-03; FE7B19-09; INV7B19-09 |
| المتطلبات والمدخل الاصطناعي | مصدر يعيد0صف وآخر يخفق أثناء حقول مطلوبة. |
| الخطوات لاحقاً | قارن لاحقاً health ومرجع الطلب والرسالة وتمكين الحفظ في الحالتين. |
| معيار القبول | تمييز not-found من failed؛ لا تحويل صامت للفشل إلى نموذج جديد صالح للترحيل. |
| الدليل | SmartAuditERP/Class/InvoiceOper.cs:3219-3281;SmartAuditERP/Class/InvoiceOper.cs:3496-3509;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-504;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:483-500;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1861-1881 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-18 — صحة المحمل: لا صف أم فشل — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-03; FE7B19-09; INV7B19-09 |
| المتطلبات والمدخل الاصطناعي | رأس صحيح وبنود بعضها غير صالح مع استثناء مادي أثناء materialization. |
| الخطوات لاحقاً | حدد سياسة partial مع مالك المحمل، ثم اختبر إبطال النتيجة غير الكاملة لاحقاً. |
| معيار القبول | الجزئي لا يعتمد مستنداً كاملاً؛ نتيجة الفشل وحد التوقف واضحان. |
| الدليل | SmartAuditERP/Class/InvoiceOper.cs:3219-3281;SmartAuditERP/Class/InvoiceOper.cs:3496-3509;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1643-1661;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:481-504;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:483-500;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1861-1881 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-19 — النمط المدعوم والمرجع المصدرّي — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-03; FE7B19-10; INV7B19-10 |
| المتطلبات والمدخل الاصطناعي | نوع غير معروف وترجمة غير عربية ومصدر production/safe واضح. |
| الخطوات لاحقاً | راجع supported/unsupported/optional مع المنتج وخطط اختبار الرسالة لاحقاً. |
| معيار القبول | رفض واضح لخارج المصفوفة؛ لا استنتاج ميزة واجبة من absence في switch وحده. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:100-124;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:113-151 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-20 — النمط المدعوم والمرجع المصدرّي — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-03; FE7B19-10; INV7B19-10 |
| المتطلبات والمدخل الاصطناعي | تبدلت قائمة النوع بعد تحميل row وبقي GlobalID وProcType القديمان في الصف. |
| الخطوات لاحقاً | قارن لاحقاً request-generation وrow-type مع SelectedIndex والقارئ المستلم. |
| معيار القبول | لا طلب من جيل أو نوع آخر؛ لا freshness أو ACL مفترضة من حقل واحد. |
| الدليل | SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1191;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:100-124;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:113-151 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-21 — حراس حفظ محددة لا كامل السياسة — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P3-001;P4-031;H7B19-04; FE7B19-11; INV7B19-11 |
| المتطلبات والمدخل الاصطناعي | فاتورة خارج الفترة وقائمة فارغة وكمية0 وطرف خاطئ، مع حالات سليمة مضادة. |
| الخطوات لاحقاً | لاحقاً قارن Save/SavePrint/Pay والمسار البديل لكل نوع مختار. |
| معيار القبول | رفض متسق قبل الأثر الجانبي؛ لا طابعة أو مزود بعد فشل الحارس. |
| الدليل | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2537-2570;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1860-1912;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1196-1335;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2012-2056;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:502-618;SmartAuditERP/Class/Common.cs:1271-1301 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-22 — حراس حفظ محددة لا كامل السياسة — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P3-001;P4-031;H7B19-04; FE7B19-11; INV7B19-11 |
| المتطلبات والمدخل الاصطناعي | موجود إلكتروني وغير إلكتروني وصلاحية تعديل ممنوعة وسداد جزئي. |
| الخطوات لاحقاً | ثبت سياسة PaymentStatus/IsUpdated ثم خطط اختبار الحراس والمصب لاحقاً. |
| معيار القبول | وجود شرط لا يعني تفويض كل الكتابات أو صحة السداد؛ يحتفظ كل رفض وأثر بمرجعه. |
| الدليل | SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2537-2570;SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1860-1912;SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1196-1335;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1901-1974;SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2012-2056;SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:502-618;SmartAuditERP/Class/Common.cs:1271-1301 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-23 — نتيجة حفظ المناقلة — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P4-019; FE7B19-12; INV7B19-12 |
| المتطلبات والمدخل الاصطناعي | فشل حفظ الطرف الأول للمناقلة قبل الثاني أو بين مرحلتي الاعتماد. |
| الخطوات لاحقاً | نفذ لاحقاً fault injection مع استعادة معزولة وافحص state/approval/second-side. |
| معيار القبول | لا false-success أو طرف يتيم؛ لا تفترض إصلاح P4-019 من قراءة Navigate. |
| الدليل | SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:797-1029;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:1520-1563;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-24 — نتيجة حفظ المناقلة — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P4-019; FE7B19-12; INV7B19-12 |
| المتطلبات والمدخل الاصطناعي | المناقلة نفسها في send/receive مع InvoiceStatus3 وغير3. |
| الخطوات لاحقاً | قارن لاحقاً Save وSavePrint والقرين وretry بهوية ثابتة. |
| معيار القبول | منع إعادة الأثر أو اعتماد محدد؛ رسالة نجاح وحدها لا تكفي. |
| الدليل | SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:797-1029;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:1520-1563;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:402-451 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-25 — اعتماد التسوية الفعلي — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P4-017;P4-018;P7-131; FE7B19-13; INV7B19-13 |
| المتطلبات والمدخل الاصطناعي | مسودة17 وحركة ترفض الحفظ، وصف معتمد وصف محذوف. |
| الخطوات لاحقاً | اختبر لاحقاً active entry والحالة قبل وبعد الفشل؛ لا تستبدل مسار الزر بـExecuteAdjustment. |
| معيار القبول | لا اعتماد باقٍ دون حركة، ولا يتحول الفشل إلى عرض مستند آخر. |
| الدليل | SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1368-1418;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:908-979;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-26 — اعتماد التسوية الفعلي — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P4-017;P4-018;P7-131; FE7B19-13; INV7B19-13 |
| المتطلبات والمدخل الاصطناعي | إلغاء تأكيد المسودة وفشل اتصال/معاملة مضبوط. |
| الخطوات لاحقاً | افحص لاحقاً أثر الإلغاء والمصدر الفعلي والاتصالين تحت خطة استعادة. |
| معيار القبول | لا قفل أو اعتماد جزئي من الإلغاء؛ قراءة المصدر ليست اختبار معاملة. |
| الدليل | SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1368-1418;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:908-979;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1105-1206;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:490-635 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-27 — حاجز الإنتاج والهوية والتحويل القديم — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P4-020;P4-021;P4-022;P7-133;P7-134; FE7B19-14; INV7B19-14 |
| المتطلبات والمدخل الاصطناعي | عقد StoredQueries ومعاملات رأس ومنتج ومكونات كاملة وهويات موجودة. |
| الخطوات لاحقاً | لاحقاً بإذن إصلاح منفصل اختبر كل نقص بعقد types/values قبل تجربة حفظ؛ الآن نصوص فقط. |
| معيار القبول | لا افتراض نجاح من transaction.Commit؛ كل أمر يستوفي العقد ويحدد عدد الصفوف. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1274-1335;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1352-1423;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Class/StoredQueries.cs:6-10 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-28 — حاجز الإنتاج والهوية والتحويل القديم — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | prior-root-regression-plan; P4-020;P4-021;P4-022;P7-133;P7-134; FE7B19-14; INV7B19-14 |
| المتطلبات والمدخل الاصطناعي | BaseQty موجب وproduct-equality12/component-equality1 وكمية3 وDocumentID معروف. |
| الخطوات لاحقاً | خطط اختبار الهوية والوحدات وبداية التحرير بمراجع ومخرج موحد بعد توفير السياسة. |
| معيار القبول | حل reader وحده لا يحل P4-022/021؛ لا إعادة عد أو ترقية certainty بلا دليل. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1274-1335;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1352-1423;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1497;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Class/StoredQueries.cs:6-10 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-29 — سياسة الدقة ووحدة الوصفة — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-01;P7-133;P7-134; FE7B19-15; INV7B19-15 |
| المتطلبات والمدخل الاصطناعي | قاموس دقة بكسور أكثر من منزلتين وحالات صفر/سالب وهالك محدد. |
| الخطوات لاحقاً | اطلب السياسة ومصدر الوصفة والتاريخ من المالك، ثم حضّر fixtures اصطناعية منقحة. |
| معيار القبول | لكل case وحدة ودقة وسبب تقريب أو رفض؛ لا سياسة مستنتجة من منزلتين في الشيفرة. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-30 — سياسة الدقة ووحدة الوصفة — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-01;P7-133;P7-134; FE7B19-15; INV7B19-15 |
| المتطلبات والمدخل الاصطناعي | تعريف وصفة تغير بعد إصدار الأمر مع مطلب محتمل للاحتفاظ باللقطة القديمة. |
| الخطوات لاحقاً | راجع هل المحرر يستعمل historic-BOM أم الحالي وشروط تعديل الكمية قبل أي نموذج تنفيذي. |
| معيار القبول | التعريف الحالي ليس لقطة إصدار مفترضة؛ العقد الغائب يبقى handoff لا موافقة. |
| الدليل | SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:884-1022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1907-2022;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:510-578;SmartAuditERP/Form_WPF/frmProductionOrder.xaml:487-511 |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-31 — مخرجات الطباعة الخارجية — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-02; FE7B19-16; INV7B19-16 |
| المتطلبات والمدخل الاصطناعي | manifest منقح لمخرجات الأوراق السبعة وDTO/table-aliases دون أسرار. |
| الخطوات لاحقاً | راجع عقد الطباعة في جزء ساكن مستقل عند توفر المدخل قبل تشغيله. |
| معيار القبول | حقول وأنواع وهوية متوافقة أو اختلاف معلن؛ غياب المدخل handoff لا passed. |
| الدليل | none-documentary-metadata |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-32 — مخرجات الطباعة الخارجية — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-02; FE7B19-16; INV7B19-16 |
| المتطلبات والمدخل الاصطناعي | قالب يفشل وcopies0/2 وإلغاء حوار وsnapshot قديم. |
| الخطوات لاحقاً | خطط قبول الإخراج لاحقاً بإذن ووحدة مستقلة؛ لا طباعة الآن. |
| معيار القبول | تمييز success/cancel/failure؛ عودة void ليست نسخة مطبوعة مثبتة. |
| الدليل | none-documentary-metadata |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-33 — حصر قدرات صادق من NV22/LC7 — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-06; FE7B19-17; INV7B19-17 |
| المتطلبات والمدخل الاصطناعي | فهرس NV22/19/2/7 والشرائح وارتباط النتائج والخطط والبقايا. |
| الخطوات لاحقاً | شغل فحوص الوثائق فقط وقارن الارتباط المتعاكس دون ERP. |
| معيار القبول | لا route يتيم أو خطة قبول ناجحة مزعومة أو نفي قدرة من حصر غير متفق. |
| الدليل | none-documentary-metadata |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-34 — حصر قدرات صادق من NV22/LC7 — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-06; FE7B19-17; INV7B19-17 |
| المتطلبات والمدخل الاصطناعي | توسعة خارج dispatcherين إلى بقية Print/words/barcode. |
| الخطوات لاحقاً | سجل سبب الاختيار والاستبعاد وحدود SP01–03 وR4d/7B20 المقترح. |
| معيار القبول | الخارج split صريح أو handoff بمالك؛ لا اكتمال7B من disposition أو عدد صفوف. |
| الدليل | none-documentary-metadata |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-35 — حفظ التاريخ والأرشيف والإذن — 1

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-06; FE7B19-18; INV7B19-18 |
| المتطلبات والمدخل الاصطناعي | ثلاثة freezes و523hash و302raw-prefix وG184 و827baseline وOWN historical modes. |
| الخطوات لاحقاً | شغل المدقق وحالات mutation الوثائقية والتقط stdout مباشرة دون placeholder أو إعادة بعد push. |
| معيار القبول | ثبات ALLnext_phase والنواة والبصمات؛ تعديلات docs/tools فقط وأرشيف أصيل لا يعاد. |
| الدليل | none-documentary-metadata |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

### P7B19T-36 — حفظ التاريخ والأرشيف والإذن — 2

| الحقل | المحتوى |
| --- | --- |
| النوع والروابط | documentary-or-external-contract-gate; H7B19-06; FE7B19-18; INV7B19-18 |
| المتطلبات والمدخل الاصطناعي | B18 parser في child تاريخي فقط، وB19 default/explicit مع الاستثناءات. |
| الخطوات لاحقاً | اختبر استعادة الهويات وعدم global patch أو redirect لاستدعاء آخر والعدادات الصارمة. |
| معيار القبول | تنفذ28 حالة B18 كاملة بلا تخطي أو تعديل بحد تاريخي ظاهر؛ الحالي B19، ولا ERP/7C/8/إصلاح. |
| الدليل | none-documentary-metadata |
| الحالة والسلامة | not-executed — خطة غير منفذة؛ أي WPF/SQL أو حفظ أو مزود أو طابعة يحتاج لاحقاً إذناً وبيئة اصطناعية معزولة واستعادة. لا app import/build أو بيانات أعمال أو أسرار أو إصلاح أو قياس. Python/Git للوثائق فقط. |

## 7. بوابة الحفظ قبل التسليم

- 523 مادة محمية وثلاثةfreezes لا كتابة عليها، و827 ملفاً أصلياً/بصمات ثابتة.
- 302 صف بكلحقل وnext_phase/evidence/classification والبادئة303CRLF حرفياً، ثم5 صفوف فقط→307/308CRLF/noBOM؛ صفرextensions.
- G01–184 حرفية، وتوصياتG185–190 إضافية لا ست نتائج أخرى.
- CLI الحقيقيdefaultB19/explicitB19 والتاريخB18=OWN302 معchild صريح. لاprotectedhelper/testedit أوskip أوglobalpatch أوdiskoverlay أوrebaseline أوarchiverewrite.
- source10ba/entryee393a7/genuineB18stdout12d2e4b هويات مستقلة؛checkout الجديد بعدcommit لن يبرر كتابة الأرشيف مجدداً.
- الـoutput الحالي يتحقق من الأدلة والروابط والثوابت الوثائقية، لا يشهد على كلنثر تاريخي أو كلسبب بشري. **7B/7 جزئيتان؛7C لم تبدأ؛8 غير مأذونة.**
