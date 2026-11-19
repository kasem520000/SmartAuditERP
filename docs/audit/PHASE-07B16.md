# المرحلة 7B16 — عقود المتصل والطفل والمخرجات المشتركة B-R3

مرجع التدقيق المعلن **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B16 هو **دفع B15 المكتمل** `16f3fd42f24183db5906bd06517b8dc10a7b9b36` بجميع **445 ملف تدقيق**، لا دفع معلق. ساعة التجميد المرصودة `2026-11-19T01:31:00.779799+00:00` منفصلة عن مرجع 16 نوفمبر وليست تاريخ تشغيل ERP. سجل stdoutB15 الحقيقي يحتفظ بـ checkout `789b04cb485948aa89e153f4b501efa27164c109` وبصمة `b8e937f80ccec245fd280cbab02f15f5652aec02a4b29a75ab669861568b4039`؛ **لا يعاد بعد الدفع**.

**7B/7 جزئيتان؛ R1/R2/R3 محليات محدودة مع بقايا خارجية وتقسيمات معلنة؛ R4/B17 مقترحة ولم تبدأ؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا معالجة أو بناء/تشغيل تطبيق أو C#/SQL/WPF/SDK/REPX/Office/COM أو مزود/جهاز/طابعة أو تصدير أعمال أو مفسر HTML/صيغة أو Process.Start فعلي أو قياس. Python/Git للوثائق فقط، و`next_phase=8` جدولة لا إذن.

[النتيجة والحدود](PHASE-07B16.md) · [العقود](SHARED-CONTRACTS-07B16.md) · [خطط القبول والتحقق](VALIDATION-07B16.md) · [المتبقي](PHASE-07-REMAINING-07B16.md) · [scope30](review-scope-07B16.csv) · [السجل الحالي 299](findings.csv) · [provenance440](evidence/provenance-07B16.json) · [stdoutB16 الجديد](evidence/checks-07B16.json)

## 1. الحصيلة الفعلية وحدودها

- **نتيجة جديدة واحدة P7-127، Medium/confirmed/implementation-defect**، محلية ومفتوحة بلا معالجة. التراكمي **299**:2Critical/178High/**118Medium**/1Low؛ **262confirmed/30potential/7repository-gap**. نتائج المرحلة 7=127، لا 127 ميزة مكتملة.
- **17 ذيلاً دقيقاً** لأصول موجودة، لا 17 نتيجة أخرى. كل **298 نواة** وعنوان/نوع/خطورة/يقين/حالة و**كل next_phase** وبادئات الأدلة محفوظة. **440 مادة سابقة** وثلاث تجميدات B16 ثابتة و**G01–170 حرفياً** و**827 path/hash أصلياً** لم تتغير. G171–176 اقتراحات لا ست نتائج إضافية.
- **30 مساراً**، منها 26 داخل اتحاد B15 و 4 جديدة عليه:own-XAML للإعدادات و picker، و VAT C#/XAML. الاتحاد 395→**399**، ومكمله**428**:363source/61generated-artifact/4project-or-resource. هذا حساب مسارات ومقاطع معلنة لا نسبة تغطية أو 428 مهمة C.
- الجسم و own-XAML محليان كاملان لـ TaxInvDetails و VATReturn و picker؛ **VAT والطفل جديدا الاكتمال المحلي C#، أما picker C# فكان كاملاً في B1**. الثلاثة خارج حصر 52 شاشة القديم؛ لا توسيع خفي للمقام. حصر 52 يبقى 33body/own-XAML+19 منتقى، وفرز 98 اسم ملف ليس كلقدرات التقارير.
- Report محلي كامل 1–611، و Print **54–221 فقط**:constructor/settings/Printing، **لا كل BindToData للفواتير أو البريد/التفقيط**. DTOs المحلية موجودة؛ بقية R1/R2 والإعدادات و DDL مقاطع محددة. الاطلاع على جسم لا يغلق feature/callgraph أو يصادق قالباً أو سياسة أو نشر.
- FE24/INV24/RC6/AD9/H6/Q6 و**14 residual-dispositions** و backlog10/workplan10. **25 خطة كلها not-executed**:2 مباشرة+17 تراجع أصل+4 عقود+2 بوابة.20 مثالاً يدوياً+20 ملاحظة نصية/74 قراءة محددة و 28 حالة مدقق جديدة ليست ERP acceptance.

## 2. المسارات المقروءة وما لا تورّثه

Home الضريبي الفعلي ينشئ **frmVATReturn** لا frmTaxRptPeriod التاريخي؛ القائمة disabled أولياً، و Apply قبل Show لا يثبت الوصول في نشر فعلي. كل من الوالد القديم والمستدعي البديل يفتح الطفل مع Invtype1/2 والتواريخ و totalPeriod=false، لكنه لا يرسل BranchSet أو allowed-set أو requestVersion. LoadBranches فيالطفل يعيد SelectedIndex=−1، و own-XAML يبدأ all=true. دليل محدود: `SmartAuditERP/Home.xaml.cs:2706-2713`؛ `SmartAuditERP/Home.xaml:345-345`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:676-715`؛ `SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml.cs:847-887`؛ `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs:128-151`؛ `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml:265-275`.

VAT يستعلم Inv/Inv_Sub مع types2/3/20/21/22 و proc1/2، ومشتريات 1، و Receipts9/Entry10. الطفل يشمل 2/3/20 ومشتريات بلا sub وسندات 9/10؛ ليس نفس SourceSet، ولا RentInvoice query فيه هنا. لذلك **لا نفرض مجموع طفل=مجموع إقرار لمجرد تطابق التاريخ**؛ المطلوب metric/grain/source-set/sign/branch/date/health معلنة وسببكل subset. label«صافي الخاضعة»ليس label«إجمالي كل الفئات»، فلا تمديد 044 آلياً.

[النطاق 30](review-scope-07B16.csv) يضم كل الحدود الآتية؛ القراءة ليست ناتجة من عداد المدقق:

| المسار | الحدود المعلنة | التركيز وحد الحكم |
| --- | --- | --- |
| SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs | 1-1086 | جسم محلي و own-XAML مقروءان بالكامل في B16 مع تتبع source/request/DTO/output. ليست تغطية كل feature أو كل caller أوتصديق REPX/schema/ACL/نشر أوتشغيل. الطفل كان مقاطع فقط B15، لا يرث عمق والده. |
| SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml | 1-601 | جسم محلي و own-XAML مقروءان بالكامل في B16 مع تتبع source/request/DTO/output. ليست تغطية كل feature أو كل caller أوتصديق REPX/schema/ACL/نشر أوتشغيل. |
| SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs | 1-858 | جسم محلي و own-XAML مقروءان بالكامل في B16 مع تتبع source/request/DTO/output. ليست تغطية كل feature أو كل caller أوتصديق REPX/schema/ACL/نشر أوتشغيل. مستدع فعلي منفصل عن frmTaxRptPeriod؛ لا مساواة قسرية بين مصدريهما. |
| SmartAuditERP/Form_WPF/frmVATReturn.xaml | 1-764 | جسم محلي و own-XAML مقروءان بالكامل في B16 مع تتبع source/request/DTO/output. ليست تغطية كل feature أو كل caller أوتصديق REPX/schema/ACL/نشر أوتشغيل. |
| SmartAuditERP/Class/Report.cs | 1-611 | Report محلي كامل: GridView/DataTable overloads، defaults/empty-result، نسخ ومعاينة و header/footer. ليس build/resolution أو REPX. |
| SmartAuditERP/Class/Print.cs | 54-221 | constructor/SettingPrint/PrinterSettings و Printing فقط؛ لا إعادة قراءة BindToData للفواتير أوالبريد/التفقيط كله. |
| SmartAuditERP/Form_WPF/frmPrinter.xaml.cs | 1-127 | جسم محلي و own-XAML مقروءان بالكامل في B16 مع تتبع source/request/DTO/output. ليست تغطية كل feature أو كل caller أوتصديق REPX/schema/ACL/نشر أوتشغيل. C# كامل في B1 سابقاً؛ الجديد own-XAML/contract، لا أول قراءة للجسم. |
| SmartAuditERP/Form_WPF/frmPrinter.xaml | 1-109 | جسم محلي و own-XAML مقروءان بالكامل في B16 مع تتبع source/request/DTO/output. ليست تغطية كل feature أو كل caller أوتصديق REPX/schema/ACL/نشر أوتشغيل. |
| SmartAuditERP/Class/InventoryData.cs | 1-303 | DTO محلي string-default fields، لا غياب Dependency من using. لا typed مالي أو versioned snapshot. |
| SmartAuditERP/Class/resvdPrint.cs | 1-32 | DTO محلي 26string؛ بنوك/رواتبحقيقيةلمتستخدم. |
| SmartAuditERP/Class/RptTaxData.cs | 1-46 | DTO محلي 35string؛ A/B/C/E/F/H mappings؛ لاخريطةقالبخارجي. |
| SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs | 650-755 | output→Report و null GridView barrier محفوظ؛ لا إعادة جسم الأب أووهمحل overload. |
| SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs | 515-710 | settings12→live defaults و DTO/movement outputs؛ الأب كامل B14 وليس أول قراءة. |
| SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs | 525-660 | output/DTO المقابل للحركة التفصيلية فقط؛ لا إعادة جسم الأب أو كل opener. |
| SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs | 265-320 | batch/expiry DTO→Report.Printing مع copies1؛ لا مساواة batch بمجموعحركة أوإثباتقالب. |
| SmartAuditERP/Form_WPF/FrmReseved.xaml.cs | 547-655 | resvdPrint→Print طلب 10 تاريخياً، حقول/masters/livecriteria/saved-subset والنتيجة؛ لا إعادةحسابالرواتبأوأهليتها. |
| SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml.cs | 180-211;700-817;847-887 | outputSettings/DTO/REPX/callers للوالدالسابق، شاهدالتفريق عن VATcaller؛ لا إعادةالجسم. |
| SmartAuditERP/Form_WPF/frmSettings.xaml.cs | 97-159;1233-1312;2087-2205;2898-2960 | RegisterEvents يربط حفظ الطباعة وخياراتها برمجياً؛ XAML بلا Click ليس إثبات غياب. مقاطع read/write/settingsId/default0/report6 و global publication، لا كل frmSettings أوأمنه. |
| SmartAuditERP/Form_WPF/frmSettings.xaml | 1060-1118;1135-1175;1296-1312 | عناصرنوعالطباعةوالنسخوالاسم/المسارو flags وزرالحفظ؛ selectedXAML لاالجسم. |
| SmartAuditERP/Class/Common.cs | 901-942 | مصدر defaultsReportsPath/Printer من SettingPrint0 و fallback؛ لاقراءةكل Common. |
| SmartAuditERP/Class/MainClass.cs | 349-455 | WPFpermission helper/earlyreturn/visualtree/exactnames، لا ACL فعلي من النص. |
| SmartAuditERP/Home.xaml.cs | 2706-2713 | HomeTax ينشئ VATReturn و Apply قبل Show؛ لا وصولنشرمنوجود handler. |
| SmartAuditERP/Home.xaml | 345-345 | عنصرالقائمة disabled أولياً شاهد مضادلاعتبار Home إثباتوصولتشغيلي. |
| SmartAuditERP/Properties/Resources.resx | 242-276;954-977;1496-1532;2014-2035;2283-2312;3895-3908 | DDL supplied لفرع id/BranchId/Code ومفاتيح Inv/Receipts/settings والموردين؛ ليس schema/deployment/grants أو كل migrations. |
| SmartAuditERP/Class/InvoiceObj.cs | 113-184 | إعدادالنوعالحالي PriceIncVAT/MainVAT/defaults؛ لا تحميلتاريخيفاتورة. |
| SmartAuditERP/Class/InvoiceOper.cs | 1530-1573;1595-1604 | كاتب parameterized يحفظ PriceIncVAT و VATPercent و val/val1/exchange_price، لافرضإصلاحالكاتبأوحفظمرصود. |
| SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs | 481-503 | مستقبل Navigate المحلي→BindingInvoice/Controls؛ لا كلمحررأو كل binder. |
| SmartAuditERP/Form_WPF/frmInvSale.xaml.cs | 1643-1660 | مستقبل Navigate للمبيعاتمقاطع فقط. |
| SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs | 1861-1880 | مستقبل Navigate لـ POS؛ لا review شاملهأوأندرويد. |
| SmartAuditERP/Form_WPF/frmSandVAT.xaml.cs | 528-622;642-667 | المستقبلينفذ SQL المرسلثم Read مرة ويعيد GlobalID/BranchID؛ navigation داخليهحارسفرعخلافطلبالطفل. |

## 3. النتيجة الجديدة

### P7-127 — الإقرار الضريبي البديل لا يطرح مرتجع المبيعات والمشتريات من مجموع المبالغ بلا ضريبة

**Medium / confirmed / implementation-defect / open-not-remediated / next_phase=8.** تأكيد مصدر محلي بشروطه، لا واقعة إنتاج أو إذن إصلاح/تشغيل.

**سلسلة السبب:** يعيد استعلام المبيعات `TotalNonTaxable` بحسب `proc_type` مع الاتجاهين1 و2. تقرأ الحلقة `nonTaxable` لكل صف؛ يضيفه `case1` إلى `salesNotTax`، لكن `case2` يطرح `netBase` و`vatAmt` و`extraVatAmt` فقط، ولا يطرح `nonTaxable`. يتكرر الإغفال في `purchNotTax` للمشتريات، بينما يطرح فرع المرتجع الأساس وVAT. تنتقل القيم إلى `lblsalesnotax/lblpurchnotax` ثم `RptTaxData.A5/B5/C5`. المستهلكان اثنان، لكن علة الاختزال واحدة لا نتيجتان.

**الشروط:** وصول صفوف مؤهلة غير محذوفة من `proc2`، لها مكوّن بلا ضريبة غير صفري، مع lookup/schema متوافقين. يمكن عزل المكوّن عن الخصم وعلم السعر باستخدام خصم0 و`PriceIncVAT=false` في المثال. لا نفترض إصلاح الكاتب أو كل مصدر أو قالب خارجي.

**مثال يدوي مستقل:** بيع100 ومرتجع40 → المرجع الموقّع60، لكن منطق الحلقة يبقي100. مرتجع وحده40 → المرجع−40، والمحلي0. بيع وحده100 → كلاهما100. تكرر الخطة الحالتين للمشتريات وتتابع المكوّن في DTO. **قد تبقى VAT المستحقة0**، ولا تصنيف قانوني للمعفى استُنتج من `taxval0`. لم يُنفذ SQL أو C# لاستنباط هذه الأعداد.

**الأثر المحدود:** المكوّن المعروض والصادر في DTO لا يصالح اتجاه المرتجع، وقد يبالغ في الإفصاح عن المبالغ بلا ضريبة بحسب تسمية القالب. شكل الورقة الفعلي ووقوع خطأ إقرار منشور غير معلومين؛ الخطورة متوسطة، لا ادعاء خسارة أو غرامة.

**تمييز العلة:** P7-044 يحذف صف المعفى من إجمالي أب آخر حتى دون مرتجع؛ P7-111 يجمع `Value` الموجب لعمولات مصدر آخر؛ P7-084 يتعلق بأهلية الاستعلام قبل الاختزال؛ P7-043 يتعلق بمعدل الرأس والخصم حتى في بيع منفرد. إصلاح أحدها لا يضيف طرح المكوّن المفقود هنا. اختلاف هوية المستدعي لا يكفي وحده لنتيجة جديدة.

**الدليل المحدود:** `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:348-442`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:465-554`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:615-637`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:806-846`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml:503-520`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml:650-666`.

**مقترح فقط:** توحيد تطبيق الإشارة لكل مكوّن من مجموعة typed قبل الإجماليات؛ تمرير المكوّن الموقّع إلى labels/DTO دون إعادة تفسير، مع سياسة فئات وخصم موثقة. لم تُعدّل شيفرة التطبيق.

**معيار لاحق غير منفذ:** بيع100/مرتجع40→60، مرتجع وحده40→−40، بيع وحده100→100، في المبيعات والمشتريات. تطبق الإشارة مرة واحدة وتتفق الخلايا وDTO؛ FE7B16-01 وINV7B16-01 وخطتا P7B16T-01/02. عدم توفر القالب يحجب قبول الورقة ولا يمحو عيب المكوّن المحلي.

## 4. الجذور التاريخية:17 ذيلاً فقط

[manifest17](evidence/historical-extensions-07B16.csv) هو نصذيول evidence المضبوطة، لا استبدال للمقدمة. التقارير التاريخية والأرشيف لا تحرر. التصنيف في العمود التالي من لقطة 298 نفسها؛ لا رفع potential أو إعادةجدولةضمنية.

| الامتداد | الأصل/التصنيف المحفوظ | الملاحظة المحلية/الشاهد المقابل | خطة تراجع غير منفذة |
| --- | --- | --- | --- |
| EX7B16-01 | P1-004 / High/repository-gap | التنفيذ يستهلك أسماء REPX والترويسة والتذييل؛ الحصر الأصلي لا يحمل القوالب. Print و Report و DTOs محلية موجودة، أما manifest/hash/version/schema والـ REPX الفعلي فغير متاحة للفحص. غياب Git ليس غياب حزمة نشر. | P7B16T-03 |
| EX7B16-02 | P1-013 / High/potential | Apply قبل Show في المستدعي؛ BtnPrint/Button3 ليسا btnPrint/btnPreview اللذين تفحصهما الدالة. لا إعادة Apply محلية في openers الطفل المقروءة. يبقى P1-013 potential؛ لا rendering أو bypass أو وصول نشر مثبت من أسماء عناصر. | P7B16T-04 |
| EX7B16-03 | P2-001 / High/confirmed | أوامر مستقلة للوصول والتصدير والمعاينة والطباعة؛ IsReadOnly يحمي تحرير الخلايا فقط ولا يمنح صلاحية أمر. تبقى ضوابط الخادم والمنح خارج هذه المقاطع، فلا ندعي تجاوزاً تشغيلياً. | P7B16T-05 |
| EX7B16-04 | P2-010 / High/confirmed | VAT يقرأ BranchId AS Id والطفل id؛ كلا العمودين و Code موجودة في DDL المرفق. الطفل يبدأ SelectedIndex=−1 و all=true، والمستدعيان لا ينقلان branch/allowed-set. alias ليس عموداً مفقوداً، و combobox ليس تفويضاً. | P7B16T-06 |
| EX7B16-05 | P3-007 / Medium/confirmed | دقة double و Math.Round ثم N2/DTO strings لا تثبت سياسة العملة أو midpoint أو الثقافة. ToDouble/ToInt يختزلان الفشل إلى 0. لم تنفذ دقة SQL/.NET أو بيانات مالية. | P7B16T-07 |
| EX7B16-06 | P3-023 / Medium/confirmed | VAT والفواتير الرئيسية للطفل يستعملان حدّاً حصرياً23:59:59، و POS يضيف 24 ساعة إلى هذا الحد. no-sub والسندات تحوّل next-day إلى shortdate. لا نافذة نصف مفتوحة موحدة لكل المصادر، ولا حسم culture/calendar/SQL فعلي. | P7B16T-08 |
| EX7B16-07 | P7-032 / High/potential | اسم الطرف ورقمه الضريبي والترويسة تؤخذ من masters وقت العرض/الإخراج لا من issued snapshot في المسار المقروء. P7-032 يبقى potential؛ لا نفي أرشيف خارجي أو واقعة تغير تاريخ مالي. | P7B16T-09 |
| EX7B16-08 | P7-043 / High/confirmed | فرع المبيعات بلا ضريبة يقسم المبلغ بمعدل الرأس إذا PriceIncVAT؛ الخصومات تذهب إلى TaxableBase رغم الفئات المختلطة. مشتريات بلا ضريبة لا يقسمها هذا الفرع، شاهد تفريق. يبقى الجذر 043 وسياسة توزيع الخصم والتصنيف غير محسومة. | P7B16T-10 |
| EX7B16-09 | P7-045 / High/confirmed | المستدعيان يمرران التواريخ الحية والنوع دون branch/requestVersion. DTO يقرأ المعايير الحالية مع الصفوف/الخلايا السابقة. hasLoadedData يكتب ولا يحرس print/details؛ عدد الصفوف ليس snapshot موحداً. | P7B16T-11 |
| EX7B16-10 | P7-046 / Medium/confirmed | الطفل يمسح ويضيف صفاً صفاً مع catch فارغة و return/parse→0 دون health typed. VAT يحسب الأرقام في متغيرات محلية حتى النشر، شاهد أفضل من خلايا SQL مرحلية؛ لكنه لا يربط النتيجة والمعايير بنسخة صحة. لا fault injection منفذ. | P7B16T-12 |
| EX7B16-11 | P7-050 / Medium/confirmed | حوار الحفظ يعلن XLSX، والكاتب DataTable.WriteXml ينتج XML ثم يعود قبل الفتح. هذا امتداد 050 لا CSV escaping048 أو formula049 أو سباق كاتب 108. لم ينشأ أو يفتح ملف أعمال. | P7B16T-13 |
| EX7B16-12 | P7-061 / High/confirmed | SELECT* يشمل GlobalID/BranchID، لكن صف المصروف يضع GlobalID/type فارغين ويطابق opener الاسم العربي ثم ReceiptNo بلا فرع. Navigate ينفذ SQL المرسل ويقرأ أول صف؛ التنقل الداخلي فيه حارس فرع. فواتير 1/2/3 تحمل GlobalID فعلاً؛ لا تعميم الفقد عليها. | P7B16T-14 |
| EX7B16-13 | P7-088 / Medium/confirmed | اختيار B ثم all يعطل القائمة ولا يمحو الاختيار؛ query يفحص SelectedIndex بدلاً من all، فيبقى B. الفتح الأول SelectedIndex=−1 شاهد أن كل طلب all ليس خاطئاً. | P7B16T-15 |
| EX7B16-14 | P7-095 / High/confirmed | الفواتير الرئيسية لا تنقل PriceIncVAT المحفوظ، وتستعمل InvoiceObj الحالي؛ no-sub يستعمل PricIncVAT من SettingGeneral2 و VAT الحالي. هذا 095 لإعادة تفسير التاريخ لا 032 لهوية master أو 043 لقسمة بند 0tax. VAT والوالد السابق يقرآن علم الرأس، شاهد مقابل. | P7B16T-16 |
| EX7B16-15 | P7-099 / Medium/confirmed | القائمة تضيف rent/return في 4/5 بشرط Marine، لكن handler يعالج 4 ثم>5؛ فهرس 5 يبقي Proc_Type السابق بعد Inv_Type=Invtype. الخيارات موجودة فلا 120. وصول Marine فعلياً غير مرصود، والتعريب لا يصحح المقارنة. | P7B16T-17 |
| EX7B16-16 | P7-112 / Medium/confirmed | كل الفترة يوسع query الفواتير؛ ProcessExpense/Income يضيفان حدّي التاريخ دائماً. الفرق عضوية all-vs-dated، مستقل عن آخر ثانية P3-023 أو أهلية مصدر ضريبي. | P7B16T-18 |
| EX7B16-17 | P7-125 / High/confirmed | Expense9 و Income10 يثبتان فرع الجلسة خلاف معيار الفواتير. اختيار B مع جلسة A يمزج المكونات؛ وقد يتراكب بعد all مع 088. VATReturn Receipt9 يستخدم branchId المختار، فلا إلحاق 125 به تلقائياً. | P7B16T-19 |

## 5. منع التكرار وحد المقارنة

قُرئت عناوين وتصنيفات ومسارات الأدلةالمتميزة **لكل 298 صفاً** في اللقطة، ثم سلاسل مختارة من أقرب الأصول فيالتقارير/المصدر المنتقى. **ليس كل 298 chain أعيد تدقيقها، ولا كل callgraph**؛ قراءة CSV برمجياً ليست هي التتبع. [AD9](evidence/root-adjudication-07B16.csv) يثبت حدود المقارنة ويصل الأدلة بأصولها، لا مجرد تطابقنص أو اختلافشاشة.

| المعرف | الجذرالحالي | الأقربالسابق | التصرف | سببالفصل/عدمإعادةالعد |
| --- | --- | --- | --- | --- |
| AD7B16-01 | P7-127 | P7-044;P7-111;P7-084;P7-043 | new-local-root | الاستعلام يعيد nonTaxable مع proc2؛ case2 يطرحالمقاييسالأخرىويسقطهذاالمكوّن.044 إجماليأبلايضمصفالمعفىحتىبلا return؛111 يجمع Value الموجبفيتقريرعمولاتآخر؛084 أهليةقبل reducer؛043 rate/discount يظهرحتىبلا return. إصلاحأحدهالايفرضطرحالمكونهنا. sales/purchases مستهلكانلجذرواحد. |
| AD7B16-02 | P7-050 | P7-048;P7-049;P7-108 | extended-existing-root | XMLxlsx عقدنوعملفلاخلل CSVescaping ولاصيغة exploit أوكاتبمفتوح؛WriteXml يعودقبل Process.Start. لاامتداد 049 أو 108 بمجردالفتح. |
| AD7B16-03 | P7-095 | P7-032;P7-043 | extended-existing-root | PriceIncVAT الحاليمناعدادنوعلاعلمفاتورة؛نفس 095 لامجردتغيراسم master032. VATparent البديلوالأبالتاريخييعتمدانعلمالرأسشاهدعدمإلحاق 095 بهما. |
| AD7B16-04 | P7-061 | P2-010;P7-045 | extended-existing-root | مصروفيفقد GlobalID ويفتح ReceiptNo؛نفس DocumentRefloss061. فاتورة 1/2/3GlobalID تحملهفعلاً،ومستهلك Navigate ينفذ SQL المرسل. لافرضهويةمتاجرمنالاسم. صفالمقبوضاتيرجع type فارغاً/GlobalID فارغاًو opener لا dispatch لهولا Android20؛ تبقىسياسة supported/unsupported وامتداد DocumentRef الأوسع في H03/RS14، لاجذرجديدمحسوممنغيابفرع. |
| AD7B16-05 | P7-088;P7-099;P7-112;P7-125 | P7-120;P7-126 | extended-existing-roots-not-new-callers | all بقيمةخفية،idx5 مقابل>5،allperiod مختلفبينمصدرين،فرعجلسةثابت؛أربعةجذورسابقاتلاتعدجديدةلأنهناطفل. القائمةمعبأةفلاتمتد 120،ومعالجات VATChecked فقطبلا Unchecked لاتمتد 126. |
| AD7B16-06 | P7-045;P7-046 | P7-055;P7-054 | retained-boundaries-and-counterevidence | hasLoadedData ليسحارس requestversion؛VAT يجمعالأرقاممحلياًحتىالنشرشاهدضد partialSQLcells. childClear/perrowcatch جزئي؛R1null055/TaskRun054 قائمةوغيرمفترضةالإصلاح،fullReport ليسحل overload. ملاحظةمفتوحة:ProcessInvoiceRow يعيد IsVAT=true،أما no-sub فلايعيدهلكل صف/طلب؛أثر state/filter/eligibility ومقارنةجذورهحاللا جزءساكنصريح H03/RS14،لا ادعاءحسمجميععيوبالجسم. |
| AD7B16-07 | P7-043 | P7-044;P7-051 | extended-existing-root-with-counterexample | VATsalesNOTAX يقسمبمعدلالرأس؛لكنصافي Sales/Purch في XAML مسمىخاضعلاضمكلالفئات،فلا 044 مننفسالعرض. لا RentInvoicequery هنا،فلا 051 من cellotherincome0. سياساتمصادر/0tax غير محسومة. |
| AD7B16-08 | P1-013;P2-001;P2-010;P3-007;P3-023;P7-032;P1-004 | P7-030;P7-031;P7-034;P7-035 | extended-existing-roots-retained-policy-handoffs | أصول/ACL/ثقافة/دقة/تاريخ/master ملحقةبأصولها،لا bypass أو leak/latency من النص. Printcopies0/نتيجة 31 جذورقديمةمعادةالقراءةدون finding جديد؛cancel/kitchen/resources/تفقيط/barcode سياسةأو split ولاجزممنتعليق. |
| AD7B16-09 | H7B16-06 | H7B16-01;H7B16-02;H7B16-03;H7B16-04;H7B16-05 | explicit-residual-handoff-or-split-not-whole-feature-closure | لا كل 298chains أعيدتقراءتها؛كل 298title/classification/uniqueevidencepaths فقطمعأقربسلاسلمنتقاة. أسطر fullbody ولفرز 52/98 لاغرضقبولأو closure. بقايا 14 محالةمعلنةلا 0 المهام. |

## 6. ملاحظات محلية مفتوحة ليست جذوراً معدودة أو شهادة خلو

| الملاحظة | ما قُرئ فعلاً | ما لم يُحسم ولماذا ينتقل صراحةً |
| --- | --- | --- |
| L7B16-01 — IsVAT في no-sub | ProcessInvoiceRow يعيد IsVAT=true لكل صف؛ ProcessPurchasesWithoutSubs يصفّرالمبالغ لكنهلايعيدالعلم فيبدايةكلصف/طلب، ويستعمله في continue. `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs:330-338`؛ `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs:463-491`. | احتمال تسربحالةتصنيفبينالمسارين/الطلبات يحتاج عينةدخل مؤهلة وترتيب استدعاء ومقارنةأقربجذورلمتكتمل. أُحيل إلى H7B16-03 و RS7B16-14/جزءساكنإضافي؛ لا إغلاقمن fullbody ولا ادعاءجذرجديدمحسوم. |
| L7B16-02 — unsupported income/Android | صفمقبوضات type فارغ/GlobalID فارغ؛ dispatcher خاصبمصروفات ثمفواتير 1/2/3 فقط، لا income أو 20 هنا. `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs:589-615`؛ `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs:785-868`. | وثقناحدالـ dispatch لاوجوبمحررأندرويدأوقبضبعينه. سياسة supported/unsupported و DocumentRef وسعالجذرتحتاج حسممتطلب/تتبعكاتبآخر؛ H03 و RS14 split معلن، لا missing-feature منغيابفرعفقط. |
| L7B16-03 — callers/باركود/تفقيط أوسع | لا كل Print.BindToData، ولا كلمحررأو كلتعريب/باركود قُرئفيهذاالجزء. أدلة B1 قائمةمحمية. | RS13/14 تسمّيانالنقلوسببهللحفاظعلىدقةالمراجعة؛ لاشطب 034/035/036/037 أو قبولمن using/comment. |

## 7. الشواهد المقابلة والحفظ والخطوة التالية

- فواتير 1/2/3 تحمل GlobalID وينقله opener؛ الفقد الموثق 061 للمصروفلا يعمها. Local Print/Report/DTOs موجودة؛ UtilitiesProj.ToDataTable/REPX وعقدالنشر خارجيان، لا missingdependency من using.
- VAT يقرأ PriceIncVAT المخزن، وتحديثمجاميعالأرقام staged محلياً؛ Receipt9 عنده يستهلك selectedbranch. لا 095 أو 125 آلياً عليه، ولا 126 من Checked-only handlers. labels الخاضعة تمنعإلحاق 044 بلاسبب، وعدم RentInvoice يمنع 51 منخليةصفر.
- Report له GridView overload بأربعةوسائطإلزامية، و DataTable overload بأربعةإلزامية وخمسةاختيارية؛ لم يحسم build/overload resolution. جسر R1 null055 و worker054 وأصولالهوية/الكاتب/الدقة/المخزون/الإنتاج وسائرالحواجز غيرمفترضةالإصلاح. `SmartAuditERP/Class/Report.cs:380-461`؛ `SmartAuditERP/Class/Report.cs:533-611`؛ `SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:728-750`.
- DDL يضم id و BranchId معاً؛ لا missing-column من alias ولامنح/index/deployment منمخططمرفق. Apply/new/disabled/Closing و finally ضوابطأومؤشراتمصدر، لا ACL أو leak/latency مقاس.
- [RS14](evidence/residual-disposition-07B16.csv) يربط 12 زوج H/Q من R1/R2 و 2splits بمالك ومدخل/أثر ومتابعة؛ ليس تسلم manifest أو policy أو grants خارجية. R1/R2/R3 باقيةبعقودها، والتالي **7B17/B-R4 مقترح ساكن أو split صريح**؛ 7C لم تبدأ و 8 غير مأذونة. تصويب B10 الإضافي 10 مقابل 120 باقٍدونتحريرأرشيف.
