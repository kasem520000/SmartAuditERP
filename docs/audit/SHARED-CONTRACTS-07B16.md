# عقود المتصل والطفل والمخرجات — 7B16

مرجع التدقيق المعلن **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`، والفرع `arena/94ae8414-smartauditerp`. دخول B16 هو **دفع B15 المكتمل** `16f3fd42f24183db5906bd06517b8dc10a7b9b36` بجميع **445 ملف تدقيق**، لا دفع معلق. ساعة التجميد المرصودة `2026-11-19T01:31:00.779799+00:00` منفصلة عن مرجع 16 نوفمبر وليست تاريخ تشغيل ERP. سجل stdoutB15 الحقيقي يحتفظ بـ checkout `789b04cb485948aa89e153f4b501efa27164c109` وبصمة `b8e937f80ccec245fd280cbab02f15f5652aec02a4b29a75ab669861568b4039`؛ **لا يعاد بعد الدفع**.

**7B/7 جزئيتان؛ R1/R2/R3 محليات محدودة مع بقايا خارجية وتقسيمات معلنة؛ R4/B17 مقترحة ولم تبدأ؛ 7C لم تبدأ؛ 8 غير مأذونة ولم تبدأ.** لا معالجة أو بناء/تشغيل تطبيق أو C#/SQL/WPF/SDK/REPX/Office/COM أو مزود/جهاز/طابعة أو تصدير أعمال أو مفسر HTML/صيغة أو Process.Start فعلي أو قياس. Python/Git للوثائق فقط، و`next_phase=8` جدولة لا إذن.

[النتيجة والحدود](PHASE-07B16.md) · [العقود](SHARED-CONTRACTS-07B16.md) · [خطط القبول والتحقق](VALIDATION-07B16.md) · [المتبقي](PHASE-07-REMAINING-07B16.md) · [scope30](review-scope-07B16.csv) · [السجل الحالي 299](findings.csv) · [provenance440](evidence/provenance-07B16.json) · [stdoutB16 الجديد](evidence/checks-07B16.json)

## 1. العقد المقترح ليس تنفيذاً قائماً

هذه حقول **تصميم/قبول لاحق**، لا DTO جديداً أُضيف للتطبيق ولا فرضسياسةعملبلا مالك:

| العقد | الحد الأدنى المقترح | ما شوهد محلياً وحدّه |
| --- | --- | --- |
| RequestSnapshot | requestId/version، source-reference، metric/grain/sign، fromInclusive/toExclusive، canonical allowedBranchSet و store/resource-set، eligibility/type/proc/history-mode، culture/currency-policy | الوالدان ينقلاننوعاً وتواريخحية فقط؛ الطفللهمعاييرمستقلة و BranchIndex−1/alltrue؛ بعضالمصادر allperiod وبعضها dated. |
| ResultSnapshot | computedRequestVersion، source-set/version، rows ومكوّناتموقعة typed، totals/currency/precision، valid/empty/partial/failed وتفصيلالمصدرالفاشل | child يضيف per-row بعد Clear و catch قدتخفيالفشل؛ VAT يستعمل numericlocals قبلالنشر، لكنلا request fingerprint مشتركةلكلقناة. |
| DocumentRef | source-family/type/proc/globalId/branch + localNo للعرضفقط؛ unsupported/ambiguous صريحة | invoice1/2/3 يحمل GlobalID؛ expense يفرّغهويفتح ReceiptNo، و income/Android لا dispatch لهمافيالمقروء. لا equateid/BranchId من alias. |
| OutputRequest | resultVersion، channel/format/schema-version، effective-settingId/version/precedence، template manifest/hash، mode/copies/printer/flags/cancel/consumer-culture | Print/Report/directREPX تختلففي zero-copies و flags/picker؛ settings0/6/10/12/14 لا تثبتأولويةنشرواحدة. |
| OutputResult | prepared/written/finalized/open-requested/previewed/printed/canceled/failed مع diagnostic منقح؛ مستقلعن save business-result | Print catch لايرجعنتيجةتفصيلية؛ shell launch لايعنيصحةالصيغة، و XML لايصير XLSX بالامتداد. لا output فعليانُفذ. |

فروعالثقة مترابطةلكنلا forcedequality:رأس/حركة/رصيد/دفعة/GL و taxable/exempt/accrual/payment مقاييس مختلفة. لااستحقاق HR أوقانونضريبةمنبلدالمستخدمأواسمالخلية. External-unavailable قيدمعلن لاقبولمنقوصيسمى passed.

## 2. topology ومستهلكو R1/R2 المسَمّون

| المسار المحلي | المصدر/صفوف/DTO | المخرج والإعداد الملحوظ | حدود القراءة |
| --- | --- | --- | --- |
| Home→VATReturn→TaxInvDetails | Inv/Inv_Sub/Receipts/Entry→خلايا VAT أو InvDetailsModel→RptTaxData/InventoryData | TaxRptPeriodNew للبديل؛rptTaxInvDetailsPurchase/Sales للطفل،header/footer؛child reader12 ثم globals للإخراج | VAT/child/own-XAML محليةكاملة؛Home/canonical DDL مقاطع؛ لا كل callgraph. |
| frmTaxRptPeriod→الطفل نفسه | خلاياالوالد→RptTaxData؛ child يقرأمنجديدولايرث source-set/branch/resultVersion | reader14؛ مسارالإخراج يختار TaxRptPeriod.repx و MainClass.ReportsPath/Printer | والد B15 محمي؛في B16 فقط settings/output/callers المعلنة، لا wholeparent reread أووصول production. |
| frmRptInventory→Report | null عندموضعالجسر→GridView/DataTable BindToData الحدودمحفوظة 055 | shared Report.Printing مع selectedsettings/copies؛لا cast/build نتيجةمفترضة |650–755 فقط، لا كلعملالمخزونأو worker. |
| حركةالمواد الإجمالية/التفصيلية | collections→InventoryData→UtilitiesProj.Common.ToDataTable | directrptItemsTotalGrd/rptItemDetails،header/footer،MainClass defaults بعد reader12 | output/DTOslices منآباء B14؛ لا كل opener/LastProcess أعيد. |
| الصلاحية | expired/batchrows→InventoryData→DataSet | RptItemsExpiration.repx→newReport.Printing(copies1) |265–320، لا wholefeature أو expiry policy أو wholeReportrender. |
| FrmReseved | _source→resvdPrint26strings، لا selected/saved-set تلقائياً | _print=newPrint(10) ثم RptResevedSalary/Print.Printing |547–655؛Binder الفاتورةفي Print لميراجعكله، وأهلية HR والحفظ B15 ليساعُدّلامفروضين. |

أدلةهذهالخريطة: `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:676-715`؛ `SmartAuditERP/Form_WPF/frmVATReturn.xaml.cs:734-846`؛ `SmartAuditERP/Form_WPF/frmTaxInvDetails.xaml.cs:948-1059`؛ `SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml.cs:180-211`؛ `SmartAuditERP/Form_WPF/frmTaxRptPeriod.xaml.cs:700-817`؛ `SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:650-755`؛ `SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:515-710`؛ `SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:525-660`؛ `SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs:265-320`؛ `SmartAuditERP/Form_WPF/FrmReseved.xaml.cs:547-655`.

## 3. الإعداد الفعّال والـ picker والـ DTO والـ overloads

- constructor الخاصبـ Print يقرأ SettingPrint و PrinterSettings بحسب Inv_Id؛ Printing يطبق PrintHeader/Footer ويتيح picker، و kitchen يعيدالاختيار. إغلاقالـ picker دون SelectedPrinter يبقيالافتراضي؛ **لا نسميه cancel bug بلا policy**. type1 مع PrintNo≤0 يسقطلـ Print واحدةتحت 030 التاريخية، بينما Report/directchild حلقةنسخ 0؛ ليسكل printmode لهسياسةواحدة. `SmartAuditERP/Class/Print.cs:54-221`؛ `SmartAuditERP/Form_WPF/frmPrinter.xaml.cs:1-127`؛ `SmartAuditERP/Form_WPF/frmPrinter.xaml:1-109`.
- Report محلي 1–611؛ GridView overload4 إلزامية، DataTable overload4 إلزامية+5 اختياريةللملخصات. الأوليقرأ displaytext، والثاني DataRow alias؛ defaults/catch/emptyDataSet لا health version. لا compiler شُغّللحسم null overload، ولا 055 أو 054 حُلّا. `SmartAuditERP/Class/Report.cs:380-611`.
- الإعدادات موصولة **برمجياً**:RegisterEvents يربطزرالحفظ وخياراتالنوع؛ XAML بلا Click ليس absence-wiring. default0/report6 فيالكاتبوالاختيار،12 للطفل/بعضالتقارير و 14 للأب، و Print10 للاستحقاق. Common يقرأ 0 إلى globals مع fallback؛ بعض outputmethods تعيدالمسار/الاسم/الطابعةمن globals بعدتحميلإعدادنوع. هذايرسم consumption لا يثبت setting مفقوداًبالنشرأوأولويةواحدة. `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:97-159`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:1233-1312`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:2087-2205`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:2898-2960`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml:1060-1118`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml:1135-1175`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml:1296-1312`؛ `SmartAuditERP/Class/Common.cs:901-942`.
- InventoryData،resvdPrint،RptTaxData موجودةمحلياًوحقولها strings/defaultempty؛26 و 35 خاصيةللأخيرين عدنصيلاقبول. لاهوية/عملة/صحة typed من string، ولاحكمأنالخارج ToDataTable ينقلالحقوللـ REPX بنفسال schema دوننسخة/manifest. لا build أوتوافققالبحُسممنعدالأسماء؛ تبقىحواجزالبناءوالنشرالتاريخية. `SmartAuditERP/Class/InventoryData.cs:1-303`؛ `SmartAuditERP/Class/resvdPrint.cs:1-32`؛ `SmartAuditERP/Class/RptTaxData.cs:1-46`.

## 4. مصفوفة 24 عقداً لا 24 ميزة مكتملة

[CSV FE24](evidence/feature-implementation-matrix-07B16.csv) يحفظالحدودوالأدلةوالـ trace و implementation_status. الحالتان 23/24 بوابتاتوثيق فقط no-source، وليستاقدرتينتنفيذيتينادّعيتاقراءتهما. كل runtime_status=not-executed. الشاهدالمقابلجزءمنالملاحظةلابرهنإغلاقعام.

| العقد/العنوان | المسار والملحوظ | الحالة | الجذور/الإحالة | خطةغير منفذة |
| --- | --- | --- | --- | --- |
| FE7B16-01 — اتجاه مبلغ بلا ضريبة في المرتجع | RefreshData→SQL grouped proc_type→switch1/2→labels→RptTaxData.A5/B5/C5؛ يقرأ TotalNonTaxable لكل اتجاه؛ case1 يضيف المكوّن و case2 يطرح الأساس و VAT لكنه لا يطرح المكوّن بلا ضريبة. بيع 100 ومرتجع 40 يعطيان محلياً100 بدلاً من صافي 60؛ المرتجع وحده 40 يعطي 0 بدلاً من−40. المبيعات والمشتريات مستهلكان لعلة reducer واحدة. قد تبقى VAT صفراً؛ لا حكم فئة قانونية أو خسارة منشورة. | implemented-with-observed-defects | P7-127 | P7B16T-01;P7B16T-02 |
| FE7B16-02 — أصول إخراج الطفل والمستدعي الفعلي | named REPX/header/footer→file load→DataSource→preview/print؛ التنفيذ يستهلك أسماء REPX والترويسة والتذييل؛ الحصر الأصلي لا يحمل القوالب. Print و Report و DTOs محلية موجودة، أما manifest/hash/version/schema والـ REPX الفعلي فغير متاحة للفحص. غياب Git ليس غياب حزمة نشر. | rechecked-prior-root-not-new-finding | P1-004 | P7B16T-03 |
| FE7B16-03 — Apply قبل Show وحدود الاسم في المستدعي والطفل | caller.ApplyPermissionToForm→Show→visual-tree/name matching→child opener؛ Apply قبل Show في المستدعي؛ BtnPrint/Button3 ليسا btnPrint/btnPreview اللذين تفحصهما الدالة. لا إعادة Apply محلية في openers الطفل المقروءة. يبقى P1-013 potential؛ لا rendering أو bypass أو وصول نشر مثبت من أسماء عناصر. | rechecked-prior-root-not-new-finding | P1-013 | P7B16T-04 |
| FE7B16-04 — الأوامر البديلة لا تصبح تفويضاً من تعطيل زر | details/export/preview/print handlers→sink؛ لا command authorization موثوق هنا؛ أوامر مستقلة للوصول والتصدير والمعاينة والطباعة؛ IsReadOnly يحمي تحرير الخلايا فقط ولا يمنح صلاحية أمر. تبقى ضوابط الخادم والمنح خارج هذه المقاطع، فلا ندعي تجاوزاً تشغيلياً. | rechecked-prior-root-not-new-finding | P2-001 | P7B16T-05 |
| FE7B16-05 — الفروع والطفل و canonical id ليست allowed-set | LoadBranches→canonical branch lookup→query predicates→new child؛ VAT يقرأ BranchId AS Id والطفل id؛ كلا العمودين و Code موجودة في DDL المرفق. الطفل يبدأ SelectedIndex=−1 و all=true، والمستدعيان لا ينقلان branch/allowed-set. alias ليس عموداً مفقوداً، و combobox ليس تفويضاً. | rechecked-prior-root-not-new-finding | P2-010 | P7B16T-06 |
| FE7B16-06 — double→string لا يطبع دقة مالية موحدة | double/Math.Round→N2/string→DTO؛ TryParse failure→0؛ دقة double و Math.Round ثم N2/DTO strings لا تثبت سياسة العملة أو midpoint أو الثقافة. ToDouble/ToInt يختزلان الفشل إلى 0. لم تنفذ دقة SQL/.NET أو بيانات مالية. | rechecked-prior-root-not-new-finding | P3-007 | P7B16T-07 |
| FE7B16-07 — نهاية اليوم في VAT والطفل ليست حداً واحداً | dateFrom.Date/dateTo23:59:59→main parameters؛POS+24h؛receipts shortdate؛ VAT والفواتير الرئيسية للطفل يستعملان حدّاً حصرياً23:59:59، و POS يضيف 24 ساعة إلى هذا الحد. no-sub والسندات تحوّل next-day إلى shortdate. لا نافذة نصف مفتوحة موحدة لكل المصادر، ولا حسم culture/calendar/SQL فعلي. | rechecked-prior-root-not-new-finding | P3-023 | P7B16T-08 |
| FE7B16-08 — أسماء الطرف والرقم الضريبي والترويسة حيّة | GetCustomerInfo/Suppliers/VATClients/FoundationInfoDT→row/header/DTO؛ اسم الطرف ورقمه الضريبي والترويسة تؤخذ من masters وقت العرض/الإخراج لا من issued snapshot في المسار المقروء. P7-032 يبقى potential؛ لا نفي أرشيف خارجي أو واقعة تغير تاريخ مالي. | rechecked-prior-root-not-new-finding | P7-032 | P7B16T-09 |
| FE7B16-09 — تقسيم 0tax بمعدل رأس في VAT البديل | line taxval0+header PriceIncVAT/VATPercent→NonTaxableBase/discount allocation؛ فرع المبيعات بلا ضريبة يقسم المبلغ بمعدل الرأس إذا PriceIncVAT؛ الخصومات تذهب إلى TaxableBase رغم الفئات المختلطة. مشتريات بلا ضريبة لا يقسمها هذا الفرع، شاهد تفريق. يبقى الجذر 043 وسياسة توزيع الخصم والتصنيف غير محسومة. | rechecked-prior-root-not-new-finding | P7-043 | P7B16T-10 |
| FE7B16-10 — طلب ونتيجة ومخرج و child من أجيال مختلفة | live dates/type→new child؛live criteria+prior rows/cells→DTO؛ المستدعيان يمرران التواريخ الحية والنوع دون branch/requestVersion. DTO يقرأ المعايير الحالية مع الصفوف/الخلايا السابقة. hasLoadedData يكتب ولا يحرس print/details؛ عدد الصفوف ليس snapshot موحداً. | rechecked-prior-root-not-new-finding | P7-045 | P7B16T-11 |
| FE7B16-11 — child يعرض صفوفاً جزئية أوصفر parse بلا health | Clear→per-row additions/catch→cards/DTO؛VAT staged numeric locals→publish؛ الطفل يمسح ويضيف صفاً صفاً مع catch فارغة و return/parse→0 دون health typed. VAT يحسب الأرقام في متغيرات محلية حتى النشر، شاهد أفضل من خلايا SQL مرحلية؛ لكنه لا يربط النتيجة والمعايير بنسخة صحة. لا fault injection منفذ. | rechecked-prior-root-not-new-finding | P7-046 | P7B16T-12 |
| FE7B16-12 — XML باسم XLSX ليس OOXML | SaveFileDialog.xlsx→DataTable.WriteXml→Process.Start after return؛ حوار الحفظ يعلن XLSX، والكاتب DataTable.WriteXml ينتج XML ثم يعود قبل الفتح. هذا امتداد 050 لا CSV escaping048 أو formula049 أو سباق كاتب 108. لم ينشأ أو يفتح ملف أعمال. | rechecked-prior-root-not-new-finding | P7-050 | P7B16T-13 |
| FE7B16-13 — مرجع سند المصروف يختزل الهوية | Receipts9.GlobalID→empty row identity→ReceiptNo SQL→Navigate→first Read؛ SELECT* يشمل GlobalID/BranchID، لكن صف المصروف يضع GlobalID/type فارغين ويطابق opener الاسم العربي ثم ReceiptNo بلا فرع. Navigate ينفذ SQL المرسل ويقرأ أول صف؛ التنقل الداخلي فيه حارس فرع. فواتير 1/2/3 تحمل GlobalID فعلاً؛ لا تعميم الفقد عليها. | rechecked-prior-root-not-new-finding | P7-061 | P7B16T-14 |
| FE7B16-14 — all-branches يخفي قيمة محددة ولا يمحوها | select B→all checked→disabled combo→SelectedIndex predicate؛ اختيار B ثم all يعطل القائمة ولا يمحو الاختيار؛ query يفحص SelectedIndex بدلاً من all، فيبقى B. الفتح الأول SelectedIndex=−1 شاهد أن كل طلب all ليس خاطئاً. | rechecked-prior-root-not-new-finding | P7-088 | P7B16T-15 |
| FE7B16-15 — الطفل يعيد تفسير مبالغ محفوظة بإعداد النوع الحالي | SELECT lacks stored flag→new InvoiceObj(type,current setting)→base/VAT reconstruction؛ الفواتير الرئيسية لا تنقل PriceIncVAT المحفوظ، وتستعمل InvoiceObj الحالي؛ no-sub يستعمل PricIncVAT من SettingGeneral2 و VAT الحالي. هذا 095 لإعادة تفسير التاريخ لا 032 لهوية master أو 043 لقسمة بند 0tax. VAT والوالد السابق يقرآن علم الرأس، شاهد مقابل. | rechecked-prior-root-not-new-finding | P7-095 | P7B16T-16 |
| FE7B16-16 — فهرس مرتجع التأجير 5 لا يصل idx>5 | Marine-visible list rent/return at4/5→handler idx4 or idx>5؛ القائمة تضيف rent/return في 4/5 بشرط Marine، لكن handler يعالج 4 ثم>5؛ فهرس 5 يبقي Proc_Type السابق بعد Inv_Type=Invtype. الخيارات موجودة فلا 120. وصول Marine فعلياً غير مرصود، والتعريب لا يصحح المقارنة. | rechecked-prior-root-not-new-finding | P7-099 | P7B16T-17 |
| FE7B16-17 — كل الفترة يوسع فواتير الطفل ويبقي السندات مؤرخة | ckTotalPeriod→empty invoice dateFilter؛receipts always dated؛ كل الفترة يوسع query الفواتير؛ ProcessExpense/Income يضيفان حدّي التاريخ دائماً. الفرق عضوية all-vs-dated، مستقل عن آخر ثانية P3-023 أو أهلية مصدر ضريبي. | rechecked-prior-root-not-new-finding | P7-112 | P7B16T-18 |
| FE7B16-18 — مصادر سندات الطفل تثبت فرع الجلسة | invoice selected/all→Receipts9/10 MainClass.BranchNo؛ Expense9 و Income10 يثبتان فرع الجلسة خلاف معيار الفواتير. اختيار B مع جلسة A يمزج المكونات؛ وقد يتراكب بعد all مع 088. VATReturn Receipt9 يستخدم branchId المختار، فلا إلحاق 125 به تلقائياً. | rechecked-prior-root-not-new-finding | P7-125 | P7B16T-19 |
| FE7B16-19 — مصالحة الأب والطفل متعددة المقاييس | SourceSet+metric/grain/sign/date/branch/health→declared reconciliation؛ VAT يضم types2/3/20/21/22 و Entry10؛ الطفل 2/3/20 و Receipts10 ولا يستعلم RentInvoice هنا. فرق المجموع قد يكون subset مقصوداً إذا أعلن. لا forced equality قبل عقد metric/source/sign/branch/date/health. لا تتبع لكل writer/GL. | reviewed-contract-unresolved-not-global-absence | H7B16-01;H7B16-03 | P7B16T-20 |
| FE7B16-20 — عقد إعدادات و mode/copies/picker | settings0/6/10/12/14→globals→mode/copies/flags/picker→sink؛ Print يستهلك flags ويقبل اختيار picker غير فارغ؛ الإغلاق الفارغ يبقي الافتراضي والمطبخ يعيد picker. Report/direct-child يقرآن flags بلا تحكيمها عند تحميل header/footer. copies0:Print يسقط لنسخة واحدة 030؛ Report/child حلقة 0. لا policy موحدة من الأسماء؛ الأولوية و cancel عقد مالك لا UX finding جديد. | reviewed-contract-unresolved-not-global-absence | H7B16-02;H7B16-03 | P7B16T-21 |
| FE7B16-21 — صفوف R1/R2 إلى DTO ليس wire schema مثبتاً | collections→InventoryData/resvdPrint/RptTaxData→external ToDataTable→DataSet→REPX؛ DTOs محلية string-default:resvdPrint26 و RptTaxData35، والعدد لا يصادق wire schema أو كل feature. grid filter لا يثبت دائماً أن collection المصدرة تغيرت. null-bridge055 و worker054 والحواجز السابقة باقية، ولا build/overload resolution أو كل Print binder مفترض. | reviewed-contract-unresolved-not-global-absence | H7B16-02 | P7B16T-22 |
| FE7B16-22 — schema/ACL والثقافة والملكية والقياس | supplied DDL+UI predicates+query lifecycle→external deployment contract؛ وجود id/BranchId/Code و Receipt.GlobalID PK في DDL لا يثبت schema/grants أو ACL نشر. الطفل يستعلم تزامنياً وفي loop مع catch، و VAT يغلق الاتصال في finally؛ لا leak/latency/index مقاس. culture/calendar/provider والملكية مدخلات منقحة لتخطيط لاحق. | reviewed-contract-unresolved-not-global-absence | H7B16-04;H7B16-05 | P7B16T-23 |
| FE7B16-23 — disposition لكل بقية دون تحويل عدد files إلى features | R1/R2 H/Q→RS14→owner/input/impact/next step؛ R1/R2/R3 محليات موثقة مع بقايا external/split؛ R4 لم تبدأ وستة محاور C لم تبدأ. لكل بقية مهمة نسبة صريحة لا unknown صامت؛14dispositions ليست موافقات خارجية أو كل caller. | deferred-not-implementation-reviewed | H7B16-06 | P7B16T-24 |
| FE7B16-24 — حفظ التاريخ وفصل التخطيط عن إذن 8 | 440 artifacts+298 cores+ALLnext_phase+G170+827 originals+3 freezes→read-only validation؛ المحفوظات لا تعاد بعد push؛ source10ba و entry/completedB15push16f3fd4 و genuineB15stdoutcheckout789b04c منفصلة. 30 مساراً و 399union و 52/98 فرز ليست اكتمالاً أوجلسات.8 غير مأذونة؛ لا معالجة/تشغيل/قبول/قياس. | deferred-not-implementation-reviewed | H7B16-06 | P7B16T-25 |

## 5. ثوابت 24 مقترحة، لا 24 اختباراً ناجحاً

المطلوب فيالعمودالتالي **قبول لاحق** لاوصفكلالتنفيذالحالي. الأدلةتتطابقمععقد FE المقابل، وروابط acceptance ثنائية. التفاصيلالمصدرية في[INV24](evidence/report-invariants-07B16.csv).

| المعرف | الثابت المطلوب | الجذر/الإحالة | خطط not-executed |
| --- | --- | --- | --- |
| INV7B16-01 | لكل مكوّن يشملبيعاً ومرتجعاً مرجع signed واحد؛ تطرح مكوّنات proc2 مرة واحدة وتحملها labels/DTO نفسها. taxval0 لا يصادق تصنيفاً قانونياً. | P7-127 | P7B16T-01;P7B16T-02 |
| INV7B16-02 | لكل قالب مطلوب manifest/hash/version و table/field types وعقد فقد/فساد الأصل؛ المحلي والخارجي مصرحان، ولا نجاح طباعة من مجرد وجود اسم. | P1-004 | P7B16T-03 |
| INV7B16-03 | التفويض يفحص الأمر والهوية بعد إنشاء العناصر وعلى كل مدخل، مع deny-by-default؛ شكل الاسم أو Apply قبل Show ليس دليل صلاحية فعلية. | P1-013 | P7B16T-04 |
| INV7B16-04 | الأمر نفسه محمي عند التفاصيل والتصدير والمعاينة والطباعة والمسار البديل؛ read-only/disabled ليسا حاجز تفويض موثوقاً. | P2-001 | P7B16T-05 |
| INV7B16-05 | BranchSet canonical المصرح به ينتقل لكل query/child/output؛ all لا يتجاوزالمنح، وفشل lookup لا يوسع النطاق. | P2-010 | P7B16T-06 |
| INV7B16-06 | قواعد precision/currency/midpoint/culture معلنة وثابتة من المصدر إلى DTO؛ فشل التحويل health صريحة لا صفر مالي صالح. | P3-007 | P7B16T-07 |
| INV7B16-07 | نافذة واحدة معلنة [from.Date,to.Date+1) لكل مصدر ومخرج؛ لا 23:59:59 حصري أو+24 مكرر أوتحويل نصي تابع للثقافة. | P3-023 | P7B16T-08 |
| INV7B16-08 | issued identity/master/version أوسياسة إعادة طباعة حية موسومة؛ لا إعادة كتابة التاريخ المالي من master متغير دون تصريح. | P7-032 | P7B16T-09 |
| INV7B16-09 | أساس كل بند يستند لفئته وعلم السعر ومعدله التاريخي؛ الخصم العام يوزع بسياسة صريحة، ولا يقسم 0tax بمعدل رأس مختلف. | P7-043 | P7B16T-10 |
| INV7B16-10 | ComputedRequestVersion واحدة للصفوف/cards/DTO/child؛ التعديل يوسم dirty أو يعيد الحساب، ولا يجمع معايير B ونتيجة A. | P7-045 | P7B16T-11 |
| INV7B16-11 | فشل query/row/parse يبطل اعتماد النتيجة أو يعلن partial بمصدره؛ valid-zero مميزة عن failed/empty ولا نجاح صامت. | P7-046 | P7B16T-12 |
| INV7B16-12 | امتداد الملف و MIME والكاتب الفعلي متوافقون؛ artifact مكتمل قبل launch و OutputResult يحمل written/opened/failed منفصلة. | P7-050 | P7B16T-13 |
| INV7B16-13 | DocumentRef يحتفظ بـ source/type/globalId/branch؛ العرض والرقم المحلي ليسا مفتاحاً. كل opener يرفض unsupported/ambiguous ويحترم المنح. | P7-061 | P7B16T-14 |
| INV7B16-14 | all المختار يحسب BranchSet النهائي ولا يخضع لقيمة اختيار معطلة خفية؛ العودة إلى single لا تفقد أوتوسع معياراً سراً. | P7-088 | P7B16T-15 |
| INV7B16-15 | تفسير فاتورة تاريخية من PriceIncVAT/VATPercent المحفوظين أو snapshot موثق، مستقل عنتغيير إعداد النوع الحالي. | P7-095 | P7B16T-16 |
| INV7B16-16 | TypeId و ProcType canonical لا index أو label؛ كل خيار ظاهر له تحويل محدد أو unsupported صريح دون توريث حالة سابقة. | P7-099 | P7B16T-17 |
| INV7B16-17 | all-period مؤهل ومعلن لكل مصدر داخل metric؛ لا يجمع invoices-all مع receipts-dated دون تسمية subset وسبب معتمد. | P7-112 | P7B16T-18 |
| INV7B16-18 | كل مصدر سندات وفواتير يستهلك BranchSet الطلب نفسه بعد mapping والمنح، لا هوية الجلسة بدلاً من الاختيار. | P7-125 | P7B16T-19 |
| INV7B16-19 | عقد reconciliation يحدد metric/grain/source-set/sign/period/branch/health وسبب فرق الأب/الطفل؛ تطابق التواريخ لا يلزم تطابق المجموع. | H7B16-01;H7B16-03 | P7B16T-20 |
| INV7B16-20 | OutputRequest يثبت effective settingId/version/precedence و mode/copies/flags/cancel؛ OutputResult مستقل عنحفظ العمل ولا يفترض إعداد نشر. | H7B16-02;H7B16-03 | P7B16T-21 |
| INV7B16-21 | جدول mapping لكل row→DTO/table/field/type/precision/currency/lineage؛ external ToDataTable/REPX بعقد متاح أو blocked صريح، لا عدد خصائص كشهادة. | H7B16-02 | P7B16T-22 |
| INV7B16-22 | نسخة schema/grants و canonical allowed-set وثقافة/تقويم وملكية موارد معلنة؛ using/finally/loop ليست نتائج قياس أوضمان نشر. | H7B16-04;H7B16-05 | P7B16T-23 |
| INV7B16-23 | كل بقية مهمة لها upstream و owner/input/impact/next-step ودليل محدود أوسبب documentary؛ لا closure منعدد files أوانتهاءفئةعمق. | H7B16-06 | P7B16T-24 |
| INV7B16-24 | 440 مادة و 298 نواة وبادئات evidence و ALLnext_phase و G01–170 و 827 أصلاً وثلاث freezes محفوظة؛ الأوضاع التاريخية OWNinputs، و next_phase8 ليس إذناً. | H7B16-06 | P7B16T-25 |

## 6. ستة عقود مصالحة لا قبول مالي

### RC7B16-01 — مقياس بلا ضريبة واتجاه 1/2

**العقد:**NonTaxable بكل proc_type→signedcomponent→labels→A5/B5/C5؛بالخصم/floating/policy مفصولة.

**يتبع:**FE7B16-01;FE7B16-09;FE7B16-15؛ **الجذور/الإحالات:**P7-127;P7-043;P7-095؛ **الخطط غير المنفذة:**P7B16T-01;P7B16T-02;P7B16T-10;P7B16T-16

**الحكم:**source-bound ومقيدبالـ scope؛ كل فرق SourceSet أو setting مسمى، ولاصحةماليةمنمطابقةجدولروابط. [سجل RC6 والأدلةالمجمّعةمن FE نفسها](evidence/report-reconciliation-07B16.csv).

### RC7B16-02 — caller/child و DocumentRef

**العقد:**طلب immutable لفترة/BranchSet/SourceSet/Type/Health؛كل opener يستعمل DocumentRef لااسمظهور،وبعضفواتيرالطفليحمل GlobalID فعلاً.

**يتبع:**FE7B16-05;FE7B16-10;FE7B16-13;FE7B16-14;FE7B16-16;FE7B16-17;FE7B16-18;FE7B16-19؛ **الجذور/الإحالات:**P2-010;P7-045;P7-061;P7-088;P7-099;P7-112;P7-125;H7B16-01;H7B16-03؛ **الخطط غير المنفذة:**P7B16T-06;P7B16T-11;P7B16T-14;P7B16T-15;P7B16T-17;P7B16T-18;P7B16T-19;P7B16T-20

**الحكم:**source-bound ومقيدبالـ scope؛ كل فرق SourceSet أو setting مسمى، ولاصحةماليةمنمطابقةجدولروابط. [سجل RC6 والأدلةالمجمّعةمن FE نفسها](evidence/report-reconciliation-07B16.csv).

### RC7B16-03 — صفوف وصحة و DTO

**العقد:**computedrequestversion ونوع/عملة/دقةومصدرسليم؛partial/zero-parse ليس validzero؛055barrier باقٍ.

**يتبع:**FE7B16-06;FE7B16-11;FE7B16-21؛ **الجذور/الإحالات:**P3-007;P7-046;H7B16-02؛ **الخطط غير المنفذة:**P7B16T-07;P7B16T-12;P7B16T-22

**الحكم:**source-bound ومقيدبالـ scope؛ كل فرق SourceSet أو setting مسمى، ولاصحةماليةمنمطابقةجدولروابط. [سجل RC6 والأدلةالمجمّعةمن FE نفسها](evidence/report-reconciliation-07B16.csv).

### RC7B16-04 — قنوات الإخراج والإعدادات

**العقد:**snapshot ثم manifest ثم OutputResult لكلقناةومعنى copies0/preview/cancel؛XMLxlsx خطأ format لا formulaexploit.

**يتبع:**FE7B16-02;FE7B16-04;FE7B16-08;FE7B16-12;FE7B16-20؛ **الجذور/الإحالات:**P1-004;P2-001;P7-032;P7-050;H7B16-02;H7B16-03؛ **الخطط غير المنفذة:**P7B16T-03;P7B16T-05;P7B16T-09;P7B16T-13;P7B16T-21

**الحكم:**source-bound ومقيدبالـ scope؛ كل فرق SourceSet أو setting مسمى، ولاصحةماليةمنمطابقةجدولروابط. [سجل RC6 والأدلةالمجمّعةمن FE نفسها](evidence/report-reconciliation-07B16.csv).

### RC7B16-05 — مخطط وصلاحيات وثقافة

**العقد:**canonicalid/grants و culture/calendar والأهليةوتصنيفالضريبة؛UIpredicates و DDL ليستحكمنشر.

**يتبع:**FE7B16-03;FE7B16-07;FE7B16-22؛ **الجذور/الإحالات:**P1-013;P3-023;H7B16-04;H7B16-05؛ **الخطط غير المنفذة:**P7B16T-04;P7B16T-08;P7B16T-23

**الحكم:**source-bound ومقيدبالـ scope؛ كل فرق SourceSet أو setting مسمى، ولاصحةماليةمنمطابقةجدولروابط. [سجل RC6 والأدلةالمجمّعةمن FE نفسها](evidence/report-reconciliation-07B16.csv).

### RC7B16-06 — أربع حزم وستة محاور بلا إغلاق ضمني

**العقد:**R1/R2/R3 محلياتمع handoffs/splits،R4notstarted،7Cnotstarted و 8unauthorized؛متابعة B17static مقترحة.

**يتبع:**FE7B16-23;FE7B16-24؛ **الجذور/الإحالات:**H7B16-06؛ **الخطط غير المنفذة:**P7B16T-24;P7B16T-25

**الحكم:**source-bound ومقيدبالـ scope؛ كل فرق SourceSet أو setting مسمى، ولاصحةماليةمنمطابقةجدولروابط. [سجل RC6 والأدلةالمجمّعةمن FE نفسها](evidence/report-reconciliation-07B16.csv).

## 7. عقود خارجية وأسئلة لم تُجب

لايطلبهذاالتسليمرواتبأوبنوكاًأوبياناتعملأو كلماتمرور. النماذجوالأوصافالمنقحةتكفيلاستكمالالتخطيط؛ عدمتوفّرها external-unavailable لا absence-proof ولاحاجزللمراجعةالساكنةالممكنة.

| الإحالة/السؤال | المالك | المطلوب والأثر | السؤال غيرالمجاب |
| --- | --- | --- | --- |
| H7B16-01 / Q7B16-01 | المحاسب/HR/المخزون | وثيقة منقحة تحدد metric/grain/sign/unit/currency و current/period/as-of و opening/closing والكلفة و fallback و expiry/Today/null وأهليةالاستحقاقوالبدلاتوصافي 0 والحسابات، وفئاتالضريبةوالخصم/GL-source. لاتستنتجمنبلدالمستخدمأواسمالحقل. | ماالمقاييسوالفئاتوالسياساتالمعتمدةوهل childsubset مقصودولماذا؟ |
| H7B16-02 / Q7B16-02 | مالك التقارير والنشر | manifest منقحلكلالأصولالمسماة مع hash/version/SDK/table/fields/types/subreports/InvoiceTxt aliases و format/dialect/culture/text-cell/finalize، و flags/copies/mode/outcome و precedence0/6/10/12/14. UtilitiesProj.ToDataTable خارجي، DTO/Print/Report محلية؛ لاقوالبببيانات عمل حقيقية. | ما manifest/precedence الإعداداتوتعريفالنجاحوالنسخو cancel دونقوالبببياناتحقيقية؟ |
| H7B16-03 / Q7B16-03 | مالك WPF وعقد التقرير | طلب immutable بـ requestId/source-set/allowedBranchSet/dateExclusive/metric/sign/health و DocumentRef source/type/globalId/branch. سياسة subset/reset/dirty/generation/cancel/unsupported وملكيةالنافذة؛ LastProcess وبقيةمحررات R1 لا يعادتصديقهابهذهالمقاطع. leads sharedIsVAT-no-sub و income/Android dispatch تبقىإلى split ساكنبحدودوأهليةمدخلاتمعتمدة. | ماعقد request/DocumentRef/unsupported/health والملكيةوتطابقالإقراروالتفصيل؟ |
| H7B16-04 / Q7B16-04 | DBA ومالك الأمان | نسخة منقحةللـ schema/constraints/grants و mapping Branches.id/BranchId/Code و Receipts.GlobalID/branch/type و Inv/Inv_Sub/InvTypes/UDF/stores/HR/Entry؛ أدوار×أوامر×مواردوتوقيت Apply/child/output. لا equateid من alias أوتفويضمن combo، ولا كلماتمرورأوقاعدةإنتاج. | مامعرفالفرع canonical والـ allowlist/grants والقيودالفعليةبالنسخةالمنقحة؟ |
| H7B16-05 / Q7B16-05 | مالك التشغيل و WPF | ثقافة/تقويم/zone و Windows/SDK/provider ودقةالعرضوحالات failed/empty/partial وملكيةالطلب/الاتصال وأحجام/schema/plans منقحةلتصميماختبارلاحق. loop/finally شواهدلاتسربأو latency/index مقاس. لاتنفيذ 7C/8 بهذاالتسليم. | ماالثقافةوالتقويموإصدارات provider ومدخلاتالقياسوالعمرالمطلوبةلتخطيطلاحقبإذن؟ |
| H7B16-06 / Q7B16-06 | مالك نطاق التدقيق | اعتماد نطاقو disposition للبقايا 14، لااكتمال 7B أو externalapproval. R1/R2/R3 محلياتمعبقايا؛R4 مقترحة أو split معلن بسبب ونطاق. أربع حزم B وستة C ليستجلساتأومدة؛ حفظ 440/298/ALLnext_phase/G170/827 وثلاث freezes وال archives، و 8 غير مأذونة. | هلنطاق R4 والـ splits وال handoffs مقبولكتسليمساكنمحدودمع 7C غير مبدوءةو 8 غير مأذونة؟ |

[دفتر RS14](evidence/residual-disposition-07B16.csv) ينسب مدخلات H/Q14/15 كلها ويحفظ splits الباركود/التفقيط والمتصلينالأوسع. **H/Q ليستنتائججديدةولاموافقاتخارجية، و fullbody/own-XAML ليستكل feature.** R4/B17 مقترحة أوجزءساكنإضافيبسبب ونطاق،و 7C/8 لم تبدأا.
