# عقود 7B21 — المبلغ والمحول والمتصل والعملات وحقول التقرير

مرجع التدقيق **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711` والفرع `arena/94ae8414-smartauditerp`. دخول B21 بعد دفع B20 المكتمل `c2c895d0df0e4f106c4e5c2853219aa04303e002` بجميع **588 مسار تدقيق**. ساعة التجميد المرصودة `2026-11-19T19:30:15.393695+00:00` مستقلة عن المرجع المعلن؛ ليست تاريخ تشغيل أو قبول.

**R4e سُلّم بحدود الشريحة فقط؛ 7B/7 جزئيتان؛ R4f/7B22 مقترح أو split مسبب؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا بناء أو تشغيل ERP/C#/VB/.NET/WPF/SQL أو SDK/provider/UtilitiesProj/ToDataTable/REPX أو قالب/طابعة/ماسح أو بيانات أعمال أو أسرار أو إصلاح أو قياس أو قبول. Python و Git لأدوات الوثائق فقط؛ `next_phase=8` تخطيط لا إذن.

[النتيجة](PHASE-07B21.md) · [عقود التفقيط والعملة](AMOUNTWORD-CONTRACTS-07B21.md) · [التحقق والخطط](VALIDATION-07B21.md) · [المتبقي](PHASE-07-REMAINING-07B21.md) · [scope24](review-scope-07B21.csv) · [السجل](findings.csv) · [provenance583](evidence/provenance-07B21.json) · [stdoutB21](evidence/checks-07B21.json)

## 1. من مصدر المبلغ إلى حقل التقرير، لا مجرد helper

[قرار النطاق](evidence/scope-decision-07B21.json) يختار بقية words/currency من SP7B20-03، لا حصر قدرات أو كل callgraph. للعملة ثلاث فئات مصدر في العينة: Inv.Currency في فرعي Print، وإعداد key13 في خمسة سندات، و Currency.SAR الافتراضية في خمسة متصلين WPF. هذه مصادر الشيفرة، لا لائحة العملات التي يدعمها المنتج أو تعريف enum.

| WC / المتصل / الموضع | مصدر المقدار وحقل الرقم | مصدر العملة وحد القراءة/الإسقاط | FE / الحد |
| --- | --- | --- | --- |
| WC7B21-01 — Print.InvoiceItems<br>SmartAuditERP/Class/Print.cs:748 | formatted-Net → InvoiceData.Net | explicit-Inv.Currency<br>formatted string → Conversions.ToDouble | FE7B21-01;FE7B21-02;FE7B21-04;FE7B21-05;FE7B21-06<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-02 — Print.Items-when-InvoiceItems-empty<br>SmartAuditERP/Class/Print.cs:1064 | raw-Inv.Net → InvoiceData.Net formatted | explicit-Inv.Currency<br>raw double; currency DTO omitted | FE7B21-01;FE7B21-02;FE7B21-06<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-03 — frmAccountBalance<br>SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:460 | literal-zero-selector-text → BalanceInperiod | default-Currency.SAR<br>Convert.ToDouble; whole producer contract unresolved | FE7B21-10<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-04 — frmAccountsStatement<br>SmartAuditERP/Form_WPF/frmAccountsStatement.xaml.cs:732 | absolute-debit-credit-difference → BalanceInperiod+BalanceType | default-Currency.SAR<br>TryParse with conditional assignment | FE7B21-09;FE7B21-11<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-05 — frmCostCenterBalance<br>SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:648 | selected-positive-balance-text → BalanceInperiod+BalanceType | default-Currency.SAR<br>SafeParseDouble removes comma and failure→0 | FE7B21-09<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-06 — frmEmpSalaryAddSub<br>SmartAuditERP/Form_WPF/frmEmpSalaryAddSub.xaml.cs:980-981 | txtVal.Text → Bond.BondVal | default-Currency.SAR<br>Convert.ToDouble; no runtime exception claim | FE7B21-04;FE7B21-08<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-07 — frmSalaryPay<br>SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs:863 | read-only-local-txtNet.Text → Bond.BondVal | default-Currency.SAR<br>TryParse failure→0; read-only counterexample to manual-entry generalization | FE7B21-08<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-08 — frmSandD<br>SmartAuditERP/Form_WPF/frmSandD.xaml.cs:1311 | editable-local-txtVal.Text → Bond.BondVal | explicit-SettingGeneral-key13<br>TryParse failure→0; raw BondVal retained | FE7B21-03;FE7B21-07<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-09 — frmSandQAndroid<br>SmartAuditERP/Form_WPF/frmSandQAndroid.xaml.cs:1108 | editable-local-txtVal.Text → Bond.BondVal | explicit-SettingGeneral-key13<br>TryParse failure→0; raw BondVal retained | FE7B21-03;FE7B21-07<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-10 — frmSandQD<br>SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:1407-1410 | txtVal.Text-whitespace-to0 → Bond.BondVal | explicit-SettingGeneral-key13<br>Convert.ToDouble; catch returns null dataset | FE7B21-07<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-11 — frmSandSD<br>SmartAuditERP/Form_WPF/frmSandSD.xaml.cs:1363-1365 | txtVal.Text-empty-to0 → Bond.BondVal | explicit-SettingGeneral-key13<br>Convert.ToDouble; catch returns null dataset | FE7B21-07<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |
| WC7B21-12 — frmSandVAT<br>SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs:1207-1208 | txtNetVal.Text-not-gross-BondVal → Bond.netVal | explicit-SettingGeneral-key13<br>TryParse outcome ignored; catch numeric-N2 in word field | FE7B21-07;FE7B21-14<br>qualified token و body slice منتقاة فقط؛ لا كل callgraph أو كامل نافذة أو قالب أو حفظ. |

نداءا SpellNumberEDP في Print هما `SmartAuditERP/Class/Print.cs:748-749` و`SmartAuditERP/Class/Print.cs:1064-1065` للمقارنة مع العربية، لا ندائين عربيين إضافيين. يحفظ CSV/Witness نص الحجة الخامل و line start/end و SHA للنداء؛ لا يقيّم الحجة أو يستورد التطبيق. البحث يقنّع التعليقات والنصوص بما فيها تعبيرات interpolation؛ لا يحل aliases/delegates/reflection أو calls داخل النصوص المقنّعة أو DLL. لم يكتشف Number2Arabic.ameral مؤهلاً خارج ملفه، وليس هذا برهان غياب أو عدم استعمال خارجي.

**شواهد مهمة:** primary يسبق التحويل بتنسيق Net؛ وعملة code2 متسقة جزئياً في العائلتين؛ و key13 له مقابل محلي في GetInvId؛ و SalaryPay/VAT net مقروءان فقط محلياً؛ والبيان/المركز يحملان مقداراً موجباً مع جانب دائن أو مدين. لا يعمم مدخل يدوي غير صالح على كل HR، أو فقد السالب على كل بيان، أو خطأ إعداد من رقمين غير متكافئين.

## 2. قاموس الفروع الرقمية المحلية CM10 — ليس تعريف SDK

| CM / رقم الفرع المحلي | عربي major / minor | إنجليزي major / minor | الحكم |
| --- | --- | --- | --- |
| CM7B21-01 / 2 | دولار / سنت | Dollar / Cent | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-02 / 4 | ريال-default / هللة-default | Dirham / Fil | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-03 / 8 | ريال-default / هللة-default | Riyal / Halala | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-04 / 9 | ريال-default / هللة-default | Pound / Penny | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-05 / 10 | ريال-default / هللة-default | Euro / Cent | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-06 / 11 | ريال-default / هللة-default | Yen / Sen | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-07 / 12 | جنيه مصري / قرش | Riyal-default / Halala-default | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-08 / 13 | جنيه سوداني / قرش | Riyal-default / Halala-default | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-09 / 15 | ليرة سورية / هللة-default | Riyal-default / Halala-default | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |
| CM7B21-10 / other | ريال-default / هللة-default | Riyal-default / Halala-default | P7-035 محفوظة؛ لا finding جديدة ولا policy precision/zero/grammar. |

**الدليل المشترك:** `SmartAuditERP/Class/InvoiceOper.cs:972-1170`. العائلات تلخص فروع النصوص، لا كل grammar أو حالات العدد/المثنى/الجمع. للفرع 15 لفظ major عند الصفر، بينما يسقط فرعه minor إلى هللة؛ هذه وقائع نصية لا اعتماد للعلاقة أو الدقة أو عدد الخانات أو الصياغة القانونية. لا يستنتج المعنى العددي لـ Currency.SAR من fallback1 أو من بلد المستخدم.

**إعداد value/index:** `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:333-352` يعرض كائنات Enum؛ و`SmartAuditERP/Form_WPF/frmSettings.xaml.cs:1028-1032` يستعيد SelectedIndex؛ و`SmartAuditERP/Form_WPF/frmSettings.xaml.cs:1655-1661` يحفظ index؛ و`SmartAuditERP/Class/InvoiceObj.cs:262-270` يلقي العدد مباشرة إلى Currency. المثال الافتراضي [1,2,8] يبين شرط الخطر، ومثال [0,1,2] شاهد يمنع التعميم؛ لا يدعى أن أياً منهما التعريف الفعلي. تبقى H7B21-04 مفتوحة دون نتيجة جديدة من enum مخترع.

## 3. كل قدرة مختارة بعقد ومسؤولية وخطط

### FE7B21-01 — حد مجال العدد قبل التفقيط

**المسار:** InvoiceOper / Print — ToArabicLetter → SFormatNumber fixed positions → words

**المشاهدة:** قناع 000000000000 يحدد أدنى عرض، ثم تقرأ Mid المواقع 1–12 فقط دون فحص طول أو رفض للمجال الأوسع. مع نص موجب مفترض 1000000000000 تختار المقاطع مقدار 100000000000، و 1000000000001 يتصادم معه. هذا خلل رتبة صحيحة لا كسر P7-034.

**الثابت INV7B21-01:** يمثل المحول المقدار الصحيح في مجاله المعلن كاملاً، أو يرفض خارج المجال قبل بناء الكلمات؛ لا إسقاط لخانة أو تغيير رتبة.

**المالك والمدخل المنقح:** مالك محرك التفقيط والمحاسب — حدود المبلغ الصحيح المسموح به و fixture منقحة لنتيجة Format والثقافة؛ لا سقف مستنتج من double أو N2.

**الأثر والخطوة:** قد يختلف مقدار الكلمات عن الرقم عند وصول قيمة أوسع من اثنتي عشرة خانة؛ لا مقدار منشور كهذا شوهد. تحديد مجال معلن وفحص طول/رتبة مستقل، ثم قبول مأذون بعد ورود العقد.

**الإحالة:** P7-139؛ P7B21T-01;P7B21T-02، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. برهان الرتبة مشروط بنص موجب غير أُسي أوسع من 12 خانة؛ لا مقدار منشور شوهد أو VB نفذ.

**الدليل:** `SmartAuditERP/Class/InvoiceOper.cs:550-795`؛ `SmartAuditERP/Class/Print.cs:737-750`

### FE7B21-02 — هوية عملة DTO في الفرعين

**المسار:** Print / InvoiceData — InvoiceItems primary vs Items fallback → local currency/word fields

**المشاهدة:** الفرع الأساسي يعين invoiceData.currency من Inv.Currency. البديل، عند InvoiceItems.Count==0، ينشئ InvoiceData جديداً ويمرر Inv.Currency للتفقيطين، لكنه لا يعين currency حتى list.Add/ToDataTable؛ والقيمة الافتراضية للخاصية string.Empty.

**الثابت INV7B21-02:** يمرر كل فرع هوية العملة المتاحة إلى DTO والرقم والتفقيط، أو يصرح بعدم دعم الفرع قبل الإخراج؛ لا حقل فارغ مع هوية متاحة.

**المالك والمدخل المنقح:** مالك إسقاط بيانات الفاتورة والتقارير — عقد currency و aliases و tabletypes و manifest/hash للقالب والفرعين، مع فاتورة اصطناعية منقحة.

**الأثر والخطوة:** يفقد DTO المحلي البديل هوية عملة متاحة؛ ظهور فراغ مطبوع أو تعويضه في محول خارجي غير مثبت. مقارنة الفرعين قبل حد ToDataTable، ثم مطابقة wire/template عند ورود العقد وبإذن مستقل.

**الإحالة:** P7-140؛ P7B21T-03;P7B21T-04، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. إسقاط محلي فقط، لا تعويض خارجي أو أثر مطبوع شوهد.

**الدليل:** `SmartAuditERP/Class/InvoiceData.cs:53-56`؛ `SmartAuditERP/Class/Print.cs:708-750`؛ `SmartAuditERP/Class/Print.cs:970-1156`

### FE7B21-03 — صحة مبلغ سندي الطباعة قبل بناء الكلمات

**المسار:** frmSandD / frmSandQAndroid / Bond — editable txtVal → whitespace guard → TryParse ?:0 → BondVal + ArabicLetter

**المشاهدة:** الحارس يرفض whitespace فقط. عند فشل TryParse يصبح netVal صفراً، ويبقى BondVal هو txtVal.Text ويستدعى ToArabicLetter(0) بلا health. حقل TextBox وستايله المحليان بلا mask، ومحول D لا يمحو النص غير القابل للقراءة.

**الثابت INV7B21-03:** تظل invalid و empty و zero و valid حالات مختلفة؛ لا يبنى أو يرسل تقرير ذو raw amount غير صالح وتفقيط مصدره صفر دون فشل معلن.

**المالك والمدخل المنقح:** مالك سندي الصرف وقبض أندرويد و WPF — عقد مدخل المبلغ وحدوده وثقافته و typed error، ونصوص مصطنعة ومسار تقرير منقح بلا أسرار.

**الأثر والخطوة:** قد يبنى DTO غير متسق من المعاينة أيضاً دون حفظ؛ ليس هذا إثبات صفر محفوظ أو طباعة تمت. تحديد health عند print boundary ومقارنة النجاح والفشل تحت شروط مسار وبيانات اصطناعية.

**الإحالة:** P7-141؛ P7B21T-05;P7B21T-06، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. سندا D/QAndroid فقط؛ شروط المسار و Foundation لازمة، ولا صفر محفوظ شوهد.

**الدليل:** `SmartAuditERP/Form_WPF/frmSandD.xaml:64-93`؛ `SmartAuditERP/Form_WPF/frmSandD.xaml:345-348`؛ `SmartAuditERP/Form_WPF/frmSandD.xaml.cs:984-989`؛ `SmartAuditERP/Form_WPF/frmSandD.xaml.cs:1092-1122`؛ `SmartAuditERP/Form_WPF/frmSandD.xaml.cs:1233-1330`؛ `SmartAuditERP/Form_WPF/frmSandQAndroid.xaml:65-94`؛ `SmartAuditERP/Form_WPF/frmSandQAndroid.xaml:322-325`؛ `SmartAuditERP/Form_WPF/frmSandQAndroid.xaml.cs:791-796`؛ `SmartAuditERP/Form_WPF/frmSandQAndroid.xaml.cs:1030-1127`؛ `SmartAuditERP/Class/Bond.cs:40-44`؛ `SmartAuditERP/Class/Bond.cs:60-64`

### FE7B21-04 — إعادة فحص التطبيع والكسر السابق

**المسار:** InvoiceOper / Print / EmpSalaryAddSub — raw or formatted amount → fixed-dot fraction prefix

**المشاهدة:** يبقى الفصل بالنقطة وقص أول خانتين كما في P7-034. الشاهد المقابل: Print الأساسي يمرر المبلغ بعد تنسيق DigitsNo وقد يمنع مثال البتر عند N2؛ البديل يرسل Inv.Net الخام. لا نتيجة جديدة أو extension.

**الثابت INV7B21-04:** ينشأ الرقم والكلمات من مبلغ normalized واحد وفق دقة وتقريب مقررين، لا من قص أول خانتين من كسر خام.

**المالك والمدخل المنقح:** المحاسب ومالك التفقيط والثقافة — سياسة precision/midpoint/major-minor مع fixtures حدية وثقافات تشغيل منقحة.

**الأثر والخطوة:** لا يمكن تعميم مثال 19.999 على كل Print أو اعتماد N2 كسياسة عملة؛ P7-034 باقية. حفظ الأصل دون extension وتصميم قبول مستقل يميز raw عن formatted عند ورود السياسة.

**الإحالة:** P7-034؛ P7B21T-07;P7B21T-08، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/InvoiceOper.cs:550-591`؛ `SmartAuditERP/Class/Print.cs:737-750`؛ `SmartAuditERP/Class/Print.cs:1051-1075`؛ `SmartAuditERP/Form_WPF/frmEmpSalaryAddSub.xaml.cs:973-984`

### FE7B21-05 — إعادة فحص فروع هوية العملة بين اللغتين

**المسار:** InvoiceOper / Print — same numeric code → Arabic and English currency branches

**المشاهدة:** فروع الأرقام نفسها تختلف: code4 يعطي Dirham إنجليزياً و fallback ريال عربياً؛ 12/13 يعطيان جنيهاً عربياً و fallback Riyal إنجليزياً. code2 مع Dollar/Cent شاهد اتساق جزئي لا تعريف SDK أو اعتماد grammar.

**الثابت INV7B21-05:** ترتبط هوية العملة بقاموس معلن واحد للغتين؛ unsupported لا يتحول صامتاً إلى عملة أخرى.

**المالك والمدخل المنقح:** مالك قاموس العملة والتقارير — تعريف enum و wire code والتسميات major/minor بإصدار SDK وبصمته، منقحاً.

**الأثر والخطوة:** لا يعتمد اسم أو دقة عملة من موقع المستخدم أو رقم case؛ P7-035 لا تعد ثانية. حفظ CM10 بوصفها فروعاً محلية لا enum، وطلب عقد القاموس قبل أي اعتماد.

**الإحالة:** P7-035؛ P7B21T-09;P7B21T-10، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/InvoiceOper.cs:972-1170`؛ `SmartAuditERP/Class/Print.cs:737-750`

### FE7B21-06 — مصدر المبلغ في نداءي فاتورة Print

**المسار:** Print / InvoiceObj — formatted invoiceData.Net vs raw Inv.Net → both word converters

**المشاهدة:** نداءان عربيان ونداءان إنجليزيان في Print: الأساسي يبدأ من Net المنسق، والبديل من Inv.Net الخام، وكلاهما يمرر Inv.Currency. اختلاف المصدر لا يثبت كل الدقة أو معالجة 035 أو 140.

**الثابت INV7B21-06:** يعلن كل caller مصدر المقدار ووقت تسويته وعملته، وتكون فروقه عن القنوات الأخرى مفسرة بعقد.

**المالك والمدخل المنقح:** مالك الفاتورة ومحاسب العملة — عقد Net/DigitsNo وحالة InvoiceItems/Items وحقول كل قالب وفرع.

**الأثر والخطوة:** لا يمكن الجزم بمساواة الكلمات بالرقم المعروض في كل فرع أو قالب من النداءات وحدها. مقارنة سلسلة منتج المبلغ والإسقاط والقالب عند ورود عقوده.

**الإحالة:** P7-034;P7-035؛ P7B21T-11;P7B21T-12، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/Print.cs:516-523`؛ `SmartAuditERP/Class/Print.cs:708-750`؛ `SmartAuditERP/Class/Print.cs:970-1156`؛ `SmartAuditERP/Class/InvoiceObj.cs:242-270`

### FE7B21-07 — عملة إعداد السندات ذات المفتاح 13

**المسار:** Common / settings / five receipt callers — GetCurrencytosand(13) → parameterized settings lookup → Currency cast

**المشاهدة:** خمسة callers تستخدم GetCurrencytosand(13). القارئ يربط Doctype بـ SettingGeneral.inv_id ويعيد 1 عند غياب صف أو استثناء. GetInvId يمثل rbRecieptVAT بـ 13؛ اختلاف ReceiptType ليس وحده دليلاً على إعداد عملة خاطئ.

**الثابت INV7B21-07:** يعلن مصدر عملة السند والـ fallback ونوع الإعداد في نطاق هوية واحد؛ لا تقارن أرقام أنواع مختلفة كأنها المفتاح نفسه.

**المالك والمدخل المنقح:** مالك سياسة السندات والإعدادات و DBA — خريطة أنواع السندات إلى مفاتيح SettingGeneral وقاعدة غياب أو فشل العملة، منقحة.

**الأثر والخطوة:** لا تعتمد صحة أو خطأ key13 المشترك أو fallback1 دون عقد؛ المصدر المحلي شاهد لا موافقة. حفظ شاهد الإعداد 13 وإحالة سياسة shared-setting دون نتيجة مصطنعة.

**الإحالة:** H7B21-03؛ P7B21T-13;P7B21T-14، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/Common.cs:768-788`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:2772-2791`؛ `SmartAuditERP/Form_WPF/frmSandD.xaml.cs:1285-1313`؛ `SmartAuditERP/Form_WPF/frmSandQAndroid.xaml.cs:1082-1110`؛ `SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:1388-1411`؛ `SmartAuditERP/Form_WPF/frmSandSD.xaml.cs:1339-1365`؛ `SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs:1200-1214`

### FE7B21-08 — عملة نداءي HR الافتراضية وحدود readonly

**المسار:** SalaryPay / EmpSalaryAddSub — HR amount → omitted Currency argument → default Currency.SAR

**المشاهدة:** يحذف النداءان وسيط العملة فتطبق Currency.SAR المعلنة. صافي SalaryPay مقروء فقط محلياً، فلا تعمم 141 عليه كإدخال يدوي. تبقى 004 و 006 الخاصتان بالمال وإعادة الاحتساب دون تعديل أو إعادة عد.

**الثابت INV7B21-08:** تعتمد عملة HR ومصدر صافيها بسياسة، وتفصل صحة التفقيط عن صحة الاستحقاق وإعادة الاحتساب والترحيل.

**المالك والمدخل المنقح:** HR والمحاسب ومالك الرواتب — سياسة عملة الصرف والإضافة/الخصم و net والسالب والصفر، بأمثلة مصطنعة بلا هوية موظف.

**الأثر والخطوة:** لا يثبت حذف وسيط العملة أن تعدد العملات واجب أو أن 006 عولجت؛ readonly ليس صحة شاملة. تقرير مصدر المبلغ والـ default وطلب عقد HR دون تشغيل أو استنتاج قانون من بلد المستخدم.

**الإحالة:** H7B21-01؛ P7B21T-15;P7B21T-16، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs:785-879`؛ `SmartAuditERP/Form_WPF/frmSalaryPay.xaml:368-374`؛ `SmartAuditERP/Form_WPF/frmEmpSalaryAddSub.xaml.cs:941-998`؛ `SmartAuditERP/Class/InvoiceOper.cs:550-575`

### FE7B21-09 — مقدار رصيد الفترة وجانبه في البيان والمركز

**المسار:** AccountsStatement / CostCenterBalance / RestrictionData — debit-credit magnitude + side → report field → Arabic words

**المشاهدة:** البيان يحسب فرق المجموعين كمقدار موجب مع BalanceType مدين/دائن، والمركز ينتقي txtBalance1/2 بحسب المقارنة. مقدار موجب مع كلمة دائن ليس فقد إشارة تلقائياً؛ مسار التعادل يضع صفراً.

**الثابت INV7B21-09:** يعبر المقدار وجانب الحساب عن معنى واحد، مع فصل إشارة الرصيد الدلالية عن سياسة لفظ minus.

**المالك والمدخل المنقح:** المحاسب ومالك التقارير المالية — قاموس signed/magnitude/side وقواعد التعادل و alias و format منقحة.

**الأثر والخطوة:** لا يعتمد GL أو توازنه أو P3-021 من ArabicLetter؛ لا يفرض سالب على مقدار يصفه جانب دائن. تثبيت عقد المقدار والجانب والصفر وصحة القراءة باختبارات لاحقة مستقلة.

**الإحالة:** H7B21-01؛ P7B21T-17;P7B21T-18، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Form_WPF/frmAccountsStatement.xaml.cs:606-747`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:561-651`؛ `SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:1042-1057`؛ `SmartAuditERP/Class/RestrictionData.cs:62-70`؛ `SmartAuditERP/Class/RestrictionData.cs:160-169`

### FE7B21-10 — انتقاء الرصيد النصي في AccountBalance

**المسار:** AccountBalance / nested report DTO — literal text != 0.00 → selected balance, side and words

**المشاهدة:** يختار txtBalance1.Text!="0.00" القيمة والجانب والتفقيط من المصدر النصي نفسه. لم تتبع هنا كل منتِجات format؛ لا finding إضافية من مثال 0.000 افتراضي دون إثبات وصوله.

**الثابت INV7B21-10:** يبنى انتقاء الطرف على مبلغ موثوق بعقد format و health، لا صيغة نصية مفترضة دون إثبات منتجها.

**المالك والمدخل المنقح:** مالك بيان الأرصدة والثقافة — عقد إنتاج Balance1/2 وصيغة الصفر والدقة ومتى يعاد تحميل الحقلين.

**الأثر والخطوة:** لا يدعى خطأ رصيد من نص افتراضي أو صيغة مفترضة من موقع المستخدم. إحالة مصدر format/side قبل توسيع النطاق أو عد نتيجة جديدة.

**الإحالة:** H7B21-05؛ P7B21T-19;P7B21T-20، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:425-480`؛ `SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:854-902`

### FE7B21-11 — مجال السالب والصفر والقيم غير المنتهية

**المسار:** InvoiceOper / selected balance callers — sign/zero/nonfinite/domain boundary before word conversion

**المشاهدة:** لا يعلن helper حارس sign/finite/length في المدخل المختار. مقاطع الصفر قد تترك فواصل وخاتمة بلا لفظ صفر؛ البرهان الموضعي هنا للموجب ذي الاثنتي عشرة خانة فقط. لم تنفذ نتيجة VB/null أو صيغة سالب فعلية.

**الثابت INV7B21-11:** يعلن قبول أو رفض negative/zero/nonfinite وحدوده وصياغة الصفر ودلالة الجانب قبل التحويل، وفق سياسة مالك موثقة.

**المالك والمدخل المنقح:** مالك التفقيط والمحاسب والثقافة — fixtures منقحة للصفر و-0 والسالب والحدود و NaN/Infinity وصياغة الكلمات والرفض، بلا سياسة مخترعة.

**الأثر والخطوة:** لا يعتمد نص سالب أو صفر أو دقة مستند من Mask، ولا يرقى toy إلى اختبار VB أو صياغة قانونية. تحليل عقد المجال وحفظ ما لم يحسم كـ handoff بدلاً من finding لكل قيمة.

**الإحالة:** H7B21-01؛ P7B21T-21;P7B21T-22، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/InvoiceOper.cs:550-795`؛ `SmartAuditERP/Class/InvoiceOper.cs:972-1170`؛ `SmartAuditERP/Form_WPF/frmAccountsStatement.xaml.cs:708-747`

### FE7B21-12 — قيمة enum مقابل فهرس اختيار الإعداد

**المسار:** frmSettings / InvoiceObj — Enum.GetValues objects → SelectedIndex storage → numeric Currency cast

**المشاهدة:** تعرض الإعدادات كائنات Enum.GetValues لكن الحفظ والاسترجاع يستعملان SelectedIndex؛ القارئ يلقي الرقم مباشرة إلى Currency. المثال القفزي افتراضي وقائمة 0..n شاهد؛ تعريف AuditorAPI غير مورّد فلا يثبت تعطل فعلي.

**الثابت INV7B21-12:** يحفظ معرف عملة مستقر بعقد enum/wire، ويثبت أو ينفى تطابق index/value قبل عد خلل أو تغيير تاريخي.

**المالك والمدخل المنقح:** مالك SDK والإعدادات و DBA — تعريف Currency بإصدار AuditorAPI وبصمته وقائمة قيمه وترتيبها وأصل رموز DB، منقحاً.

**الأثر والخطوة:** لا يجزم بانحراف العملة أو رقم SAR من مصدر محلي أو قائمة enum مخترعة. طلب عقد value/index ومراجعة الحفظ التاريخي عند وروده؛ لا DLL execution أو ترحيل.

**الإحالة:** H7B21-04؛ P7B21T-23;P7B21T-24، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Form_WPF/frmSettings.xaml:245-253`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:333-352`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:1009-1035`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:1604-1661`؛ `SmartAuditERP/Class/InvoiceObj.cs:122-133`؛ `SmartAuditERP/Class/InvoiceObj.cs:262-270`

### FE7B21-13 — حد helper Number2Arabic القديم

**المسار:** Number2Arabic / qualified-token discovery — Number2Arabic.ameral lexical boundary vs active InvoiceOper callers

**المشاهدة:** لم يكشف البحث المؤهل عن Number2Arabic.ameral خارج ملفه في 477 source C#. النداءات العربية الاثنتا عشرة المكتشفة إلى InvoiceOper؛ هذا حصر توكنات لا reflection أو DLL، ولا حكم dead-code أو بديل يعالج 034/139.

**الثابت INV7B21-13:** لا يعتمد helper بديل أو تنفى قدرة من غياب توكن مكتشف؛ يلزم source→consumer وعقد مجال معلوم.

**المالك والمدخل المنقح:** مالك المحركات القديمة والمنتج — قائمة engines/callers/aliases/external components وسبب اختيار المحول أو استبعاده.

**الأثر والخطوة:** لا يعلن اكتمال words أو استبدال آمن من helper بلا متصل مثبت في هذه العينة. split صريح لبقية المحركات والمتصلين غير المؤهلين؛ أي استبدال يحتاج عملاً وإذناً آخرين.

**الإحالة:** H7B21-03؛ P7B21T-25;P7B21T-26، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/Number2Arabic.cs:261-328`؛ `SmartAuditERP/Class/InvoiceOper.cs:550-575`؛ `SmartAuditERP/Class/Print.cs:737-750`

### FE7B21-14 — تمييز fallback رقمي من كلمات في VAT

**المسار:** frmSandVAT / Bond — txtNetVal → conversion catch → ArabicLetter numeric-N2 fallback

**المشاهدة:** مصدر التفقيط txtNetVal لا BondVal قبل الضريبة. لا يحمل TryParse health؛ وعند استثناء العملة أو الكلمات ينقل N2 إلى ArabicLetter. هذا حد صحة محلي لا إثبات صفر أو ضريبة أو قالب منشور؛ txtNetVal مقروء فقط في XAML المختار.

**الثابت INV7B21-14:** يميز فشل التفقيط أو العملة أو القراءة عن نجاح نص كلمات، ويعلن أي بند مبلغ يقصد قبل أو بعد الضريبة.

**المالك والمدخل المنقح:** مالك VAT والتقارير والثقافة — عقد gross/tax/net وسياسة رفض أو وسم fallback رقمي بدل words، مع manifest منقح.

**الأثر والخطوة:** لا ترقى سلسلة N2 في حقل الكلمات إلى تفقيط صحيح أو إغلاق 034/035؛ لا طباعة شوهدت. تسجيل fallback كحد صحة، وعدم توسيع 141 إلى VAT دون تتبع منتج الحقل المقروء فقط.

**الإحالة:** H7B21-05؛ P7B21T-27;P7B21T-28، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Form_WPF/frmSandVAT.xaml:316-345`؛ `SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs:1074-1125`؛ `SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs:1160-1217`؛ `SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs:1330-1345`

### FE7B21-15 — حدود DTO والقالب ودلالة العملة

**المسار:** InvoiceData / Bond / RestrictionData / nested AccountStatement DTO — local string properties → external ToDataTable → unknown template mapping

**المشاهدة:** حقول المبلغ والكلمات والعملة المحلية strings، والجانب منفصل عن المقدار؛ ToDataTable و REPX خارج المصدر. 140 فقد إسقاط محلي فقط، ولا يفترض وجود currency property أو أسماء aliases متماثلة في كل نوع.

**الثابت INV7B21-15:** يوثق mapping كل قناة من DTO إلى جدول و alias وقالب وبصمة؛ وجود property لا يساوي نجاح الطباعة.

**المالك والمدخل المنقح:** مالك التقارير والنشر و SDK UtilitiesProj — manifest/hash/version/SDK/tabletypes/aliases لقنوات Invoice/Bond/Restriction/AccountStatement ورمز العملة المطلوب.

**الأثر والخطوة:** لا تثبت عملة فارغة مطبوعة أو كلمات صحيحة من DTO وحده، ولا ينفى دعم العملة من شكل Bond. إحالة wire/templates مع crosswalk صريح قبل أي قبول لاحق.

**الإحالة:** H7B21-02؛ P7B21T-29;P7B21T-30، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** `SmartAuditERP/Class/InvoiceData.cs:53-56`؛ `SmartAuditERP/Class/InvoiceData.cs:197-200`؛ `SmartAuditERP/Class/InvoiceData.cs:251-255`؛ `SmartAuditERP/Class/InvoiceData.cs:290-294`؛ `SmartAuditERP/Class/Bond.cs:31-44`؛ `SmartAuditERP/Class/Bond.cs:60-64`؛ `SmartAuditERP/Class/RestrictionData.cs:62-70`؛ `SmartAuditERP/Class/RestrictionData.cs:160-169`؛ `SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:854-902`؛ `SmartAuditERP/Class/Print.cs:1141-1156`

### FE7B21-16 — حفظ 310 صفوف و G195 وكل التاريخ

**المسار:** documentary preservation — entry freezes → exact old registry/G/artifact/source comparison

**المشاهدة:** تحمى 583 مادة من 588 عند c2c895d وثلاثة freezes جديدة. كل حقل قديم و ALLnext_phase/evidence/raw311CRLF prefix و G195 و 827 بصمة محفوظة، وصفر extension.

**الثابت INV7B21-16:** يبقى كل قديم حرفياً بلا rebaseline أو archive overwrite؛ تتقدم خمسة مسارات مشتركة فقط وتضاف مواد B21 بأسماء جديدة.

**المالك والمدخل المنقح:** مالك مدقق الوثائق والتاريخ — لقطة الدخول و hashes و OWN310 والفهارس الثلاثة دون أسرار.

**الأثر والخطوة:** لا تعتمد نتيجة حديثة إذا خالطت التاريخ مدخلات live313 أو تغيرت أدلته. فحص مستقل لكل الحقول والبايتات و G والأرشيف وبصمات التطبيق قبل التسليم.

**الإحالة:** H7B21-06؛ P7B21T-31;P7B21T-32، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** بوابة وثائقية بـ`none-documentary-metadata`، لا source مصطنع.

### FE7B21-17 — بقايا مملوكة وحصر لا توكنات

**المسار:** documentary scope and residuals — RS14 upstream lineage → owned handoffs and explicit SP01–03

**المشاهدة:** تحفظ RS14 أصل B20 وعقوده و rowSHA، وتبقى SP01–03 و H/Q6 مفتوحة. 477 scan و 12AR/2EN و 24path ليست النظام أو كل words؛ 455FE تاريخية لم تعد body review.

**الثابت INV7B21-17:** لكل قدرة منتقاة دليل وحد ومالك ومدخل وأثر وخطوة وخطة وتصرف؛ غير المراجع يبقى في 7B أو handoff خارجي لا موافقة ضمنية.

**المالك والمدخل المنقح:** مالك النطاق والمنتج والتقارير — حصر قدرات ومداخل ومصادر ومخارج supported/unsupported/optional متفق عليه، دون نسبة إتمام.

**الأثر والخطوة:** لا ختم R4/SP03/7B من أعداد الملفات أو splits، ولا نقل صامت إلى 7C. R4f/7B22 مقترح أو split مسبب بقدرة مسماة ومعيار خروج، لا وعد مدة أو جلسات.

**الإحالة:** H7B21-06؛ P7B21T-33;P7B21T-34، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** بوابة وثائقية بـ`none-documentary-metadata`، لا source مصطنع.

### FE7B21-18 — CLI تاريخي صريح وفصل الإذن والقبول

**المسار:** documentary CLI and authorization — OWN310 exact inputs + historical child → separate current B21 tests

**المشاهدة:** يستعمل B20 OWN310/raw311CRLF والفهارس في الذاكرة وكل 32 أصلية بطفل presetB20 صريح؛ B19/36 و B18/28 محفوظان. CLI الحالي B21 مستقل و main API B15 متوافق؛ 7C لم تبدأ و 8 غير مأذونة.

**الثابت INV7B21-18:** نجاح الوثائق لا ينفذ خطط الأعمال أو يصلح التطبيق؛ لا skip أو protected edit أو global patch أو overlay أو rebaseline أو archive rewrite.

**المالك والمدخل المنقح:** مالك أداة التدقيق والإذن والمراجعة — stdout حقيقي بهوية capture HEAD ومدخل تاريخي وطفل شفاف، دون تحويل JSON أو flags مصطنعة.

**الأثر والخطوة:** خلط التاريخ بـ live313 يبطل المقارنة؛ خلط الوثائق بالقبول ينشئ إذناً لم يعطه المستخدم. تشغيل مدقق الوثائق والأطفال التاريخية فقط وأرشفة stdout خام في sink حصري.

**الإحالة:** H7B21-06؛ P7B21T-35;P7B21T-36، كلها not-executed. **الحد:** تتبع ساكن منتقى لا كامل الميزة أو SDK أو ثقافة أو قالب أو نشر؛ لا تشغيل أو إصلاح أو قبول. المدخل والسياسة والمستهلك المطلوبون لم يعتمدوا؛ الشواهد ليست قبولاً كلياً.

**الدليل:** بوابة وثائقية بـ`none-documentary-metadata`، لا source مصطنع.

## 4. النطاق والعدّ لا يساويان العمق أو الإذن

24path/22overlap/2new→union412/complement415. الجديد على الاتحاد SandD.xaml و SandVAT.xaml، والباقي 22 مساراً سبق scope لها؛ هذا لا يكمل أجسامها أو قدراتها. [دفتر scope](review-scope-07B21.csv) يصرح بالشرائح:

| المسار : المقاطع | العمق والحد |
| --- | --- |
| SmartAuditERP/Class/Bond.cs:31-44;60-64 | حقول المبلغ والتفقيط المحلية؛ ليس عقداً لكل Bond أو ToDataTable الخارجي. |
| SmartAuditERP/Class/Common.cs:768-788 | قارئ عملة SettingGeneral بالـ Doctype وفشل أو غياب الصف إلى 1؛ لا SQL منفذ. |
| SmartAuditERP/Class/InvoiceData.cs:53-56;197-200;251-255;290-294 | العملة والتفقيطان والصافي في DTO المحلي؛ لا wire-table أو aliases أو SDK. |
| SmartAuditERP/Class/InvoiceObj.cs:122-133;242-270 | عملة افتراضية وقراءة DigitsNo/عملة الإعداد إلى enum؛ لا كل قراءة/حفظ الفاتورة. |
| SmartAuditERP/Class/InvoiceOper.cs:550-795;972-1308 | عقد التفقيط والمقاطع العددية والعملات والإنجليزية فقط؛ لا SaveInvoice أو تشغيل VB/.NET. |
| SmartAuditERP/Class/Number2Arabic.cs:261-328 | helper القديم كحد منفصل؛ غياب متصل مؤهل مكتشف ليس dead-code أو بديلاً معتمداً. |
| SmartAuditERP/Class/Print.cs:516-523;708-750;970-1156 | إعداد BindToData وفرعا InvoiceItems/Items حتى الإسقاط والعودة؛ لا كامل Print أو كل مستند/قالب. |
| SmartAuditERP/Class/RestrictionData.cs:62-70;160-169 | حقول رصيد/جانب/تفقيط المحلية فقط؛ القراءة cp1256 fallback لا اعتماد encoding أو schema. |
| SmartAuditERP/Form_WPF/frmAccountBalance.xaml.cs:425-480;854-902 | انتقاء قيمة الرصيد بالتنسيق النصي والتفقيط و DTO الداخلي؛ لا إعادة حساب كل GL. |
| SmartAuditERP/Form_WPF/frmAccountsStatement.xaml.cs:606-747 | مصدر مجموعي الشاشة واختيار مقدار الرصيد وجانبه ونداء التفقيط؛ لا دورة التقرير أو المحاسبة كاملة. |
| SmartAuditERP/Form_WPF/frmCostCenterBalance.xaml.cs:561-651;1042-1057 | إسقاط مجاميع/جانب الرصيد و SafeParseDouble إلى تفقيط؛ لا كل المركز أو reader. |
| SmartAuditERP/Form_WPF/frmEmpSalaryAddSub.xaml.cs:941-998 | BondVal والتفقيط بالعملة الافتراضية؛ لا حفظ/استحقاق HR أو تتبع أحداث كامل. |
| SmartAuditERP/Form_WPF/frmSalaryPay.xaml:368-374 | txtNet مقروء فقط محلياً؛ شاهد يمنع تعميم مدخل غير صالح في سندين على كل الرواتب. |
| SmartAuditERP/Form_WPF/frmSalaryPay.xaml.cs:785-879 | حارس الطباعة وربط txtNet إلى Bond والتفقيط الافتراضي؛ لا إصلاح 006 أو ترحيل مالي. |
| SmartAuditERP/Form_WPF/frmSandD.xaml:64-93;345-348;694-700 | حقل مبلغ وستايله وربط زر الطباعة المحلي؛ لا rendering أو styles خارجية. |
| SmartAuditERP/Form_WPF/frmSandD.xaml.cs:984-989;1092-1122;1233-1330 | ربط الطباعة ومحول النص الجزئي وحارسها والإسقاط إلى Bond؛ لا الحفظ أو القيد. |
| SmartAuditERP/Form_WPF/frmSandQAndroid.xaml:65-94;322-325;740-749 | حقل txtVal وستايل TextBox وربط الطباعة؛ لا قيود مصدر أخرى أو WPF منفذ. |
| SmartAuditERP/Form_WPF/frmSandQAndroid.xaml.cs:791-796;1030-1127 | حدث الطباعة وحارس whitespace و TryParse fallback مع raw BondVal؛ لا Android خارجي أو حفظ. |
| SmartAuditERP/Form_WPF/frmSandQD.xaml.cs:1360-1447 | عملة إعداد 13 و Convert.ToDouble و Bond مع catch؛ لا كل مسار الطباعة والحفظ. |
| SmartAuditERP/Form_WPF/frmSandSD.xaml.cs:1312-1390 | عملة إعداد 13 و Convert.ToDouble و Bond مع catch؛ لا كل سند/قالب أو SDK. |
| SmartAuditERP/Form_WPF/frmSandVAT.xaml:316-345 | حقول value/VAT/net المحلية للتمييز بين إجمالي السند وصافيه؛ لا تنفيذ إعادة الاحتساب. |
| SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs:1074-1125;1160-1217;1330-1345 | حارس الطباعة ومصدر netVal و catch N2 وتعيين Bond؛ لا كامل الضريبة أو القالب. |
| SmartAuditERP/Form_WPF/frmSettings.xaml:245-253 | عنصر اختيار العملة المحلي؛ لا كامل إعدادات أو تهيئة WPF. |
| SmartAuditERP/Form_WPF/frmSettings.xaml.cs:333-352;1009-1035;1604-1661;2772-2791 | تحميل enum وعرض index وحفظه ومعرف إعداد 13؛ لا تعريف SDK الفعلي أو سياسة عملة. |

الشاهد يعيد 33 قراءة محدودة من 20 مساراً؛ بعض الدعم ضمن 24 مقروء يدوياً لا instrumented proof. التوكنات المكتشفة في 477 scan ليست body reviews. دفاتر 455/98/52 التاريخية لا يعاد مقامها من 12 نداء. [RS14/SP3](PHASE-07-REMAINING-07B21.md) تحفظ خارج العينة ولا تنقله إلى 7C. **لا تشغيل محول أو.NET/VB/SDK/ToDataTable/REPX/SQL/طابعة أو بيانات أعمال؛ 7C لم تبدأ و 8 غير مأذونة.**
