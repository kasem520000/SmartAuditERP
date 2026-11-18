# الجزء 7B6 — تفاصيل أصناف POS وجهات العمل وإجمالي البيع/الشراء

**7B6 تسليم ساكن جزئي ضمن إذن تدقيق 7 القائم؛ لا اكتمال 7B أو 7. أُعلنت 7B7 للباقي ولم تبدأ.7C لم تبدأ. المرحلة 8 غير مأذونة ولم تبدأ.**

**مرجع التدقيق المعلن:**2026-11-16 UTC، لا ادعاء أنه وقت ساعة البيئة. مرجع التطبيق الأصلي `10ba215152f722c8808aea0bb672c1d1d4d9d711` ثابت. التزام التوثيق المدفوع قبل B6 هو `d0ae6b318c47451dd7e10a416f07566a7b3f1dc7` على الفرع نفسه `arena/94ae8414-smartauditerp`؛ فصل source عن checkout لا يعيد baseline أو يعيد تأريخ checks التاريخية.

## 1. ماذا سُلّم وما الذي دُفع؟

نُفذ طلب «ادفع كل ماقد انجزته الى الفرع ثم واصل العمل»: حُفظت الأعمال المكتملة 1–6 و 7A/B1–B5 في التزام التوثيق أعلاه، **204 ملفات تدقيق فقط** و 38294 إضافة، ودُفعت إلى الفرع نفسه بنجاح قبل بدء B6. لا PR أو merge أو تغيير فرع أو تعديل تطبيق. تعديلات B6 نفسها عمل لاحق لذلك الدفع، ولا نزعم أنها كانت داخله.

هذا الجزء يقرأ التنفيذ الفعلي المختلف لـ`frmItemsalesdetailsPos`، لا `frmRptItemsSalesDetailsPOS` التجميعي الذي قرئ في B5. ويقرأ طفلي `frmNkdFoundRpt` المسميين `frmActsInvTotal` و`frmNkdTotSalePurch` فعلاً، لا يرقّيهما من قراءة launcher قديم.

| المقياس | النتيجة المحدودة |
|---|---|
| نتائج جديدة | **4**:P7-095–098، **1 عالية و 3 متوسطة، كلها confirmed محلياً بشروطها** |
| إضافات لأدلة أصول سابقة | **16 ذيلاً فقط**؛ لا إعادة عد أو تغيير نواة أو أي next_phase لأول 266 |
| التراكمي المفتوح | **270**:2 حرجة،174 عالية،93 متوسطة،1 منخفضة؛ **235 مؤكدة،28 محتملة،7 فجوات مستودع** |
| نطاق B6 | **13 مساراً**:7 تتقاطع مع 347 السابقة و 6 جديدة؛ الاتحاد **353**، والمكمل **474 inventory-only** فضلاً عن مقاطع داخل الاتحاد |
| التنفيذ المحلي المقروء | ثلاثة أجسام C# كاملة **1794 سطراً** و XAML ها **1274 سطراً**؛ **3068 سطراً** لا اكتمال لكل callers/templates أو قواعد/نشر |
| مصفوفة وحدود | **26 صفاً**، **19 ثابتاً**، **7 عقود مصدر/تسوية مقترحة**، **31 خطة قبول/بوابة غير منفذة**،6 handoffs و 6 أسئلة و 10 backlog |
| شواهد المدقق |20 توضيحاً يدوياً مستقلاً و 20 ملاحظة نصية محدودة؛ ليست نواتج C#/SQL أو اختبارات ERP |

جميع النتائج open-not-remediated. confirmed قرار/إغفال محلي لا حادث إنتاج. لم تُرقَّ P1-013 أو P7-049 من potential، ولا حُسمت سياسات مالية/خادم/قوالب من نموذج اصطناعي.31 خطة =8 مباشرة للجديد +16 انحدار أصل +5 عقود عابرة +2 بوابة نطاق/إذن. **لا اختبارات ERP أو build أو SQL أو Office/COM/جهاز/مزود أو معالجة.**

## 2. ضبط المصدر والتاريخ والنطاق

- [provenance7B6](evidence/provenance-07B6.json) أنشئ مرة عند الدخول ويحمي **199 artifact تاريخية**، بينها 178 السابقة وملفات B5 المسلّمة وأدواتها و checks ها الفعلية. لم يعاد توليد أي helper أو checks أو baseline محمي.
- [لقطة 266](evidence/findings-through-07B5.csv) SHA256=`05204ad5a40eed6a6a276b949c3c679e6f506f139a6470394f1489706a882619`، و[نصوص فهارس B5 الثلاثة](evidence/shared-indexes-through-07B5.json) محفوظة كما سُلّمت.
- التزام docs-only لا يصبح مرجع ERP جديداً. المدقق يثبت ancestry ودلتا الشجرة الملتزمة داخل`docs/audit/` فقط، ثم يطابق **مجموعة مسارات التطبيق 827 وبصماتها** مستقلة. هذا فحص net tree delta لا توقيعاً أو إثبات كل تاريخ وسيط. لا يستبدل تجزئة المصادر ولا يسمح بتغيير تطبيق تحت مسمى توثيق.
- B5 يعاد فحصه بمدخلاته 266 وفهارسه الدقيقة في الذاكرة، لا بسجل 270 أو الفهارس الحالية؛ كذلك A/B1/B2/B3/B4 بمدخلاتها الخاصة. **إعادة الفحص الحالية ليست ادعاء استنساخ bytes أو مقاييس checks التاريخية.**
- أول 110 صفوف G محفوظة حرفياً، وتضاف G-111–116 كست مجموعات توصية لا نتائج إضافية. كل 266 نواة وجدولة محفوظة، ومنها 43 متابعة تاريخية تحمل 7؛ الجديد next_phase=8 خطة لا إذن.
- وقت البيئة المشاهد للدخول`2026-11-18T02:20:48+00:00` مسجل منفصلاً في provenance، لا إعادة تأريخ للمرجع 16 نوفمبر ولا تاريخ تشغيل ERP.

[نطاق 13](review-scope-07B6.csv) هو المصدر التفصيلي للحدود، وليس مجرد قائمة أسماء:

| المسار | النطاق | سبب القراءة وحده |
|---|---|---|
| `SmartAuditERP/Class/InvoiceObj.cs` | `113-178;292-299` | مصدر PriceIncVAT من SettingGeneral الحالي و IsInput من InvTypes؛ لا كل الإعدادات/الكاتب. |
| `SmartAuditERP/Class/InvoiceOper.cs` | `1526-1624;3219-3312` | عقد حقول الرأس والبند ووحداتهما و flag الشمول التاريخي، وبداية BindingInvoice التي تستهلك SQL المستدعي؛ لا كل حفظ/فتح/ترحيل. |
| `SmartAuditERP/Class/ItemOper.cs` | `1365-1508;1630-1643` | حساب كمية الأساس وسعر وحدة البيع و sum/خصم/ضريبة/Net المستقل؛ لا سياسة كاملة للعروض أو الاستقطاع. |
| `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml` | `1-315` | XAML المحلي كاملاً لربط معايير/جدول/مجاميع وأزرار جهات العمل؛ لا render/RTL/وصول مقبول. |
| `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs` | `1-431` | جسم تقرير جهات العمل كاملاً:مصادر/أنواع/اتجاه/أخطاء/Dispatcher و placeholder الإخراج؛ لا كل كاتب/جهة أو تنفيذ. |
| `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs` | `1855-1880` | Navigate المحلي:BindingInvoice يستهلك SQL المرسل ثم يربط النموذج؛ لا بقية محرر POS أو حفظه. |
| `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml` | `1-642` | XAML المحلي كاملاً:معيار مستخدم وفترة/وقت وجدول/مجاميع وفتح ومخرج؛ البحث عن الصنف ليس control ظاهراً هنا. |
| `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs` | `1-866` | جسم تفاصيل أصناف POS المختلف كاملاً:قارئ/معايير/flag/دقة/ملخص/هوية/FlowDocument/CSV/HTML؛ لا كل caller أو محرر مصدر. |
| `SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml.cs` | `1-51` | launcher الطفلين كاملاً؛ لا ترقية أي طفل آخر من قراءة اسمه. |
| `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml` | `1-317` | XAML المحلي كاملاً لمدخل فترة/مبالغ/كميات ومخرج؛ لا كل موارد التطبيق أو قبول لوحة مفاتيح/ثقافة. |
| `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs` | `1-497` | جسم إجمالي البيع/الشراء كاملاً:ستة مجاميع/وحدة/شرط كمية/فشل/HTML و FlowDocument وإعدادات؛ لا تصديق سياسة المقياس. |
| `SmartAuditERP/Home.xaml.cs` | `137-138;2906-2913;3627-3633` | مرجع Nkd static ومدخل Home الذي يطبق صلاحياته مقابل مدخل تفاصيل POS المباشر؛ لا كل Home أو قائمة XAML. |
| `SmartAuditERP/Properties/Resources.resx` | `954-1074;3026-3081` | DDL Inv/Inv_Sub وكتالوج InvTypes المرفق؛ يميز النوع وإجراء الرأس واتجاه السطر. لا دليل مخطط منشور أو تنفيذ ترقية. |

[دفتر 827](evidence/coverage-ledger-07B6.csv) يحفظ نطاق كل مرحلة ومكمل الأسطر، و[فرز 98 ملفاً](evidence/report-candidate-disposition-07B6.csv) و[52 مرشح شاشة](evidence/report-screen-disposition-07B6.csv)=35 لفظياً+17 من غير regex، **ليست أعداد ميزات أو أجسام مكتملة**. FingerPrintDevice مطابقة لفظية للبصمة. قراءة الجسم و XAML هنا لا تغطي أي طفل آخر أو قالب/مخطط منشور/دور/قبول.

## 3. النتائج الجديدة — مصدر وشروط وحدود ومعالجة مقترحة

### P7-095 — تفاصيل أصناف POS تعيد تفسير شمول السعر للضريبة بإعداد النوع الحالي لا بعلم الفاتورة المحفوظ

**الخطورة:**عالية؛ **confirmed من المصدر، مفتوحة ولم تعالج.**<br>
**الشاشة والمسار:**`frmItemsalesdetailsPos` — ShowResult1 → new InvoiceObj(invType,procType) → SettingGeneral.PriceIncVAT → DgvTotalBeforeTax/DgvTotal.

**الدليل:**`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:177-197`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:211-256`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:266-278`؛ `SmartAuditERP/Class/InvoiceObj.cs:113-178`؛ `SmartAuditERP/Class/InvoiceOper.cs:1560-1564`؛ `SmartAuditERP/Class/InvoiceOper.cs:3271-3277`؛ `SmartAuditERP/Class/ItemOper.cs:1388-1411`؛ `SmartAuditERP/Class/ItemOper.cs:1420-1482`؛ `SmartAuditERP/Properties/Resources.resx:986-994`.

**المشاهدة المحلية:**SELECT لا يحمل Inv.PriceIncVAT، وينشئ InvoiceObj لكل صف. هذه الفئة تقرأ flag من SettingGeneral حيث Inv_Id=نوع الفاتورة الآن. يعتمد قبل الضريبة/الإجمالي على flag الحالي، رغم أن الكاتب يحفظ Inv.PriceIncVAT والقارئ العام BindingInvoice يستعيده من الرأس.

**السبب الجذري:**استبدال خاصية مالية تاريخية محفوظة بسياسة إعداد حية عند قراءة مستند قديم؛ يمكن لتغيير الإعداد وحده تغيير مبلغ التقرير بلا تغيير الفاتورة.

**شرط الوصول والحواجز:**رأس POS محفوظ PriceIncVAT=true وبند qty1×115 وخصم 0 و taxval15 وإضافية/خصم رأس 0؛ إعداد النوع الحالي false. اعزل خطأ نوع/DBNull/وحدة واسم/فرع أولاً. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**الأثر بمثال مشروط:**يعرض الأساس 115 والإجمالي 130 بدلاً من 100 و 115. وبالاتجاه العكسي: مستند غير شامل qty1×100 و tax15، مع إعداد حالي true، يعطي 85 و 100 بدلاً من 100 و 115.

**حد الدليل والشاهد المقابل ومنع التكرار:**توافق العلمين يخفي العيب. لا يعد هذا P7-086 لطرح ضريبة إضافية من VAT، ولا P7-032 لهوية الطرف في إعادة الطباعة؛ المثال بضريبة إضافية 0. لا نقرر سياسة ضريبية منشورة أو نثبت حادث إنتاج، و flag الرأس غير المتاح يحتاج حالة unknown لا fallback صامتاً.

**المعالجة المقترحة — لم تنفذ:**اقرأ flag الإصدار المحفوظ مع البند أو breakdown تاريخياً موثوقاً، واحفظ مصدره/إصداره في DTO؛ لا تعتمد SettingGeneral لإعادة تفسير السعر التاريخي. امنع التقرير النهائي إذا تعذر حسم أساس السعر.

**قبول غير منفذ:**P7B6T-01 و P7B6T-02 في[خطة 31](VALIDATION-07B6.md). لا يعد نجاح المثال اليدوي أو ملاحظة النص قبولاً لهذه النتيجة.

### P7-096 — تفاصيل أصناف POS تقرب الكمية قبل ضرب السعر فتخالف قيمة السطر المحسوبة من الكمية الأصلية

**الخطورة:**متوسطة؛ **confirmed من المصدر، مفتوحة ولم تعالج.**<br>
**الشاشة والمسار:**`frmItemsalesdetailsPos` — ShowResult1 SQL raw val1 → Math.Round(val1,2) → DgvItemSum → signed cards / CSV / FlowDocument.

**الدليل:**`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:177-193`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:242-275`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:308-344`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:708-724`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml:453-480`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1597`؛ `SmartAuditERP/Properties/Resources.resx:1033-1035`.

**المشاهدة المحلية:**SQL يحسب sum=(val1*exchange_price)-discount من الكمية الأصلية؛ في loop تقرب val1 إلى منزلتين قبل إسناد DgvQty وحساب DgvItemSum=Math.Round(val1*exchPrice,2). DgvTotalBeforeTax و DgvTotal يستعملان sum الأصلي، فتوجد قاعدتان عدديتان داخل الصف نفسه.

**السبب الجذري:**تحويل تنسيق عرض الكمية إلى فقد دقة داخل الحساب؛ السعر المرتفع يضخم فرقاً صغيراً في الكمية، وقد يغير تقسيم السطر المجموع المعروض.

**شرط الوصول والحواجز:**qty0.004 و price1000، خصم وضريبة 0 وعلم شمول false، ووحدة أساس 1؛ float/val1 المرفقة تقبل كسوراً. لا تعتمد تقريب midpoint أو فرق تمثيل double في المثال. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**الأثر بمثال مشروط:**DgvQty=0 و DgvItemSum=0، لكن SQL sum و DgvTotal=4؛ البطاقات تجمع gross0 و net4 لنفس البند. qty1.2346×100 يعطي 123 بدل 123.46، وتقسيمه إلى 0.6173 مرتين يعطي 124.

**حد الدليل والشاهد المقابل ومنع التكرار:**الكميات ذات منزلتين أو أقل قد تخفي الخلل. ليس P7-077 لعدد صحيح في مقام متوسط تكلفة؛ هنا بسط قيمة بيع مستقل وحقول صف متعارضة حتى بلا تكلفة. الإجمالي المحسوب من sum الخام ليس هو الذي خسر الكمية؛ لا تعمم أن كل المبالغ صفر.

**المعالجة المقترحة — لم تنفذ:**احتفظ بكمية ومبلغ دقيقين في نموذج التقرير، واقصر N2 على العرض؛ احسب Gross/Discount/Base/Tax/Net مرة وفق سياسة الدقة وباقي التقريب، ثم اشتق البطاقات والمخرج من القيم نفسها.

**قبول غير منفذ:**P7B6T-03 و P7B6T-04 في[خطة 31](VALIDATION-07B6.md). لا يعد نجاح المثال اليدوي أو ملاحظة النص قبولاً لهذه النتيجة.

### P7-097 — مخرجا تفاصيل POS وإجمالي البيع والشراء يحجبان FlowDocument بفحص REPX لا يحمّلانه

**الخطورة:**متوسطة؛ **confirmed من المصدر، مفتوحة ولم تعالج.**<br>
**الشاشة والمسار:**`frmItemsalesdetailsPos / frmNkdTotSalePurch` — PrintDevexpress → ReportsPath/File.Exists(REPX) → BuildPrintDocument → WPF DocumentViewer/PrintDialog.

**الدليل:**`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:482-535`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:540-565`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:289-350`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:355-380`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml:625-637`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml:308-310`.

**المشاهدة المحلية:**يشترط كل مسار ReportsPath غير فارغ ومجلداً وملف rptInvDetailsPos.repx أو rptNkdTotSalePurch.repx موجوداً، ثم ينشئ FlowDocument محلياً ويعرضه أو يرسله إلى PrintDialog. لا يقرأ محتوى الملف ولا يحمل XtraReport في جسمي المسارين.

**السبب الجذري:**حارس تبعية لمحرك/قالب غير مستعمل باقٍ أمام محرك WPF مستقل؛ امتلاك بيانات كافية لبناء المستند لا يكفي للوصول إلى المعاينة دون ملف لا يستهلكه البناء.

**شرط الوصول والحواجز:**صف محمل غير فارغ وإتاحة WPF/BuildPrintDocument، لكن ReportsPath فارغ أو ملف REPX المحدد غير موجود. لا يلزم إرسال طباعة أو تشغيل ERP لإثبات فرع return المحلي. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**الأثر بمثال مشروط:**تتوقف المعاينة/الطباعة قبل بناء FlowDocument برسالة مسار. وجود ملف بمحتوى غير مستعمل يغير اجتياز الحارس وحده؛ لا يثبت صدور ورق أو صلاحية ذلك المحتوى كقالب.

**حد الدليل والشاهد المقابل ومنع التكرار:**P1-004 فجوة توريد تاريخية؛ الجديد تعارض اعتماد داخل caller حتى لو كانت REPX موردة. لا نزعم فشل قراءة/تنفيذ REPX أو إصابة DevExpress أو أن المخرج فارغ. Nkd يطبق PrintNo بحلقة، بخلاف POS؛ إعدادات الوجهة/الترويسة عقد منفصل غير محسوم.

**المعالجة المقترحة — لم تنفذ:**حدد renderer وعقده: احذف فقط بوابة REPX غير المستخدمة إذا كان FlowDocument هو المسار المعتمد، أو حمّل القالب الموثوق بعقد بيانات صحيح إذا كان REPX مطلوباً. وثق إعدادات النسخ/الوجهة والترويسة ودلالة النتيجة؛ لا تعالج بإنشاء ملف وهمي.

**قبول غير منفذ:**P7B6T-05 و P7B6T-06 في[خطة 31](VALIDATION-07B6.md). لا يعد نجاح المثال اليدوي أو ملاحظة النص قبولاً لهذه النتيجة.

### P7-098 — تصديرا HTML في تفاصيل POS وإجمالي البيع والشراء يدرجان نصوص البيانات كترميز خام

**الخطورة:**متوسطة؛ **confirmed من المصدر، مفتوحة ولم تعالج.**<br>
**الشاشة والمسار:**`frmItemsalesdetailsPos / frmNkdTotSalePurch` — GetCurrencyName / Items.name → DTO string → ExportToExcelHtml / ExportToHtml → UTF8 HTML cells.

**الدليل:**`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:730-767`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:775-793`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:89-94`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:119-125`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:260-286`.

**المشاهدة المحلية:**تنسخ أسماء الصنف والمخزن/العميل/المستخدم والعنوان إلى &lt;td&gt;/&lt;h2&gt; بواسطة interpolation بلا HTML encoding؛ Nkd يدرج row.Column2 كذلك. لا يعزل النص عن صيغة HTML. الخلايا الرقمية المنسقة لا تثبت سلامة الخلايا النصية.

**السبب الجذري:**غياب encoder ملائم لسياق HTML text، لا مجرد فاصل CSV أو double quote. قيمة أعمال تحوي &lt; أو &amp; يمكن أن تتحول إلى بنية/كيانات بدلاً من نصها الحرفي عند تفسير HTML.

**شرط الوصول والحواجز:**قيمة اسم اصطناعية مثل صنف &lt;b&gt;خاص&lt;/b&gt; &amp; عرض أو نص &lt;/td&gt;&lt;td&gt;زائد في مصدر الاختبار؛ لا نص script أو صيغة أو بيانات شخصية، ولا دعوى أن محرر بعينه يسمح بها في الإنتاج. مراجعة ساكنة للنطاق المختار فقط؛ لا تشغيل C#/WPF/SQL/DevExpress/قالب أو Office/COM أو مزود، ولا اعتماد مالي/أمني أو إثبات نشر. حواجز البناء والاعتماديات والمخطط والإتاحة والتفويض تسبق أي قبول لاحق مأذون، ولا يعد الحجب نجاحاً.

**الأثر بمثال مشروط:**bytes الملف تحتوي الوسوم كجزء خام من البنية لا &amp;lt; و &amp;amp;. قد يغير مستهلك HTML تنسيق الخلية/عددها أو نصها؛ المؤكد حد الترميز المكسور، لا تشغيل JavaScript أو Office أو فقد إنتاجي مرصود.

**حد الدليل والشاهد المقابل ومنع التكرار:**يختلف عن P7-048 لترميز CSV/TSV وعن P7-049 المحتملة لتفسير الصيغ: إصلاح quote CSV أو تحييد = لا يهرب &lt; في HTML. قبول وسم خام لا يثبت تنفيذ script في Excel أو خصائص المستهلك؛ لا اختبار مستهلك أو شبكة.

**المعالجة المقترحة — لم تنفذ:**استعمل HTML encoder لكل نص في text node وعقداً مستقلاً للسمات/الروابط إن أضيفت؛ أو صدّر صيغة typed حقيقية تحفظ النصوص. اختبر بقاء القيم والبنية وعزل سياسة الصيغ/الفتح التلقائي؛ لا تطهر المدخل بحذف أحرف أعمال مشروعة.

**قبول غير منفذ:**P7B6T-07 و P7B6T-08 في[خطة 31](VALIDATION-07B6.md). لا يعد نجاح المثال اليدوي أو ملاحظة النص قبولاً لهذه النتيجة.

## 4. توسيع أصول سابقة —16 لا 16 نتيجة جديدة

خلط النوع/الإجراء/اتجاه السطر في جهات العمل **توسعة P7-084**، ووحدة`val×exchange_price` توسعة P7-041، و gate كمية صفر لقيمة غيرصفر توسعة P7-040. لا نتيجة لكل query أو TODO أو caller. نواة العنوان والتصنيف والحالة والجدولة القديمة محفوظة؛ قد يكون عنوان الأصل أضيق من التوسعة، فتقرأ الملاحظة المحددة أدناه لا تعميم العنوان حرفياً على كل مسار.

| التوسعة | الأصل | المشاهدة الإضافية ودليلها | الاستكمال المقترح |
|---|---|---|---|
| EX7B6-01 | P1-004 | المخرجان يسميان REPX خارج اللقطة ويشترطان وجوده، لكنهما يبنيان FlowDocument لا يستهلك محتواه؛ افصل فجوة التوريد عن تعارض اعتماد caller الجديد P7-097.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:482-512`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:289-316` | manifest/renderer بإصدار ومورد مستهلك فعلياً؛ لا تحميل DLL أو قالب مجهول. |
| EX7B6-02 | P1-013 | مدخل Nkd في Home يطبق ApplyPermission/DoApply قبل Show، بينما launcher الطفلين ومدخل POS وفتح محرره لا يستدعونها محلياً. هذا اختلاف مسار لا حكم فعلي على visual-tree أو تفويض خادم.<br>`SmartAuditERP/Home.xaml.cs:2906-2913`؛ `SmartAuditERP/Home.xaml.cs:3627-3633`؛ `SmartAuditERP/Form_WPF/frmNkdFoundRpt.xaml.cs:19-46`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:373-409` | تفويض مركزي للقراءة/المخرج/فتح المورد، وقبول lifecycle مأذون لاحقاً؛ potential محفوظة. |
| EX7B6-03 | P1-030 | Home يعيد Show لمرجع Nkd static محتفظ به، وزر الخروج المحلي Close؛ launcher الآخر ينشئ instance جديدة كشاهد مقابل لا نفس lifecycle.<br>`SmartAuditERP/Home.xaml.cs:137-138`؛ `SmartAuditERP/Home.xaml.cs:2906-2913`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:469-475` | إنشاء instance بعد Closed أو عقد Hide صريح مع إبطال سياق الجلسة. |
| EX7B6-04 | P1-033 | معاينة/طباعة جهات العمل موصولتان لكن تعرضان قيد التطوير دون مخرج. البحث بالاسم/الرمز في POS مستقبلي و SelectedId لا يدخل القارئ؛ لا control صنف ظاهر في XAML المقروء، فلا نصفه زر بحث مرئياً معطلاً.<br>`SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:360-403`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml:146-158`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:441-466` | نفذ القدرة المعتمدة أو عطلها بوضوح، واحسم حاجة الشيفرة غير الموصولة؛ لا نتيجة لكل TODO. |
| EX7B6-05 | P2-010 | قارئات الأجسام تقيد BranchNo إن لم يكن-1، لكن فتح تفاصيل POS يعيد البحث بالرقم/النوع/الإجراء دون branch أو GlobalID.=-1 لا يثبت نطاقاً مخولاً أو انتهاكاً في نشر فعلي.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:173-193`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:373-409`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:187-194`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:258-270`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:98-108` | BranchScope مفوض واحد في القراءة والفتح/التصدير، دون الاعتماد على caption أو متغير جلسة عام فقط. |
| EX7B6-06 | P3-023 | الأجسام الثلاثة تستعمل تاريخ النهاية+24 ساعة مع &lt;=؛ في fixture أيام عند منتصف الليل يدخل حدث اليوم التالي 00:00. POS/Nkd يحولان تواريخ إلى نصوص قبل معاملات DateTime. هذه زيادة حد مشمول لا تكرار ادعاء استبعاد آخر دقيقة تاريخياً.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:168-199`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:177-178`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:258-269`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:102-108`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:202-209` | [from,toExclusive) بمعاملات DateTime فعلية ودقة/منطقة معلنتين؛ لا تغيير ثقافة/Parse يخفي الفرق. |
| EX7B6-07 | P7-040 | حارس صف Nkd يفحص صافي كميتي الشراء/البيع فقط، ثم يجمع المبالغ داخله. شراء 1×100 ومرتجع 1×80 يعطي كمية 0 وقيمة 20 فيسقط الصف والمبلغ إذا لا بيع.<br>`SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:128-181` | أهلية تمثل الحركات والمقاييس غير الصفرية أو استبعاداً معلناً مصالَحاً؛ ليس netQty وحده دليلاً على انعدام أثر مالي. |
| EX7B6-08 | P7-041 | SUM(val*exchange_price) في جهات العمل والمجاميع الستة لـ Nkd يضرب كمية أساس في سعر وحدة بيع. عبوة 10/سعر 50 تعطي 500 لا 50، مع حسم النوع/الاتجاه والخصومات أولاً.<br>`SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:258-270`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:128-153`؛ `SmartAuditERP/Class/InvoiceOper.cs:1593-1598`؛ `SmartAuditERP/Class/ItemOper.cs:1394-1407`؛ `SmartAuditERP/Properties/Resources.resx:1023-1045` | قيمة من كمية البيع×سعرها أو سعر أساس متجانس، وكمية أساس مستقلة؛ لا تبدل سياسة gross/net ضمن إصلاح وحدة. |
| EX7B6-09 | P7-045 | FlowDocument في POS/Nkd يبني وصف الفترة من controls الحالية، والصفوف والمجاميع من تحميل سابق. لا snapshot للمعايير ولا dirty guard محلي؛ التقاط النص لاحقاً لا يعيد الاستعلام.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:157-199`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:560-570`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:590-618`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:102-108`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:373-380`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:400-420` | لقطة طلب/نتيجة واحدة أو منع إخراج عند تغير المعايير، لا تاريخ جديد فوق صفوف قديمة. |
| EX7B6-10 | P7-046 | Nkd يبتلع ExecuteQuery الفاشل ويبقي qty/total الافتراضيين 0؛ جهات العمل تسجل فشل aggregate ثم ترجع 0 وتواصل. POS قد يحتفظ بصفوف _dataRows قبل فشل لاحق مع summaries لم تحسب؛ المخرج يختبر Count فقط.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:161-164`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:207-294`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:79-84`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:187-222`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:208-235`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:308-316` | خطأ≠صفر؛ نشر result atomically أو partial معلن وتعطيل final output عند عدم اكتمال مصدر. |
| EX7B6-11 | P7-048 | CSV POS يحيط الحقول باقتباس لكنه لا يضاعف quote داخل الاسم؛ quoting يصلح الفاصلة في جزء من الحالات لا round-trip كامل.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:700-727` | CSV encoder مستقل للحدود/الاقتباس/الأسطر والأرقام وثقافة آلة؛ لا يصلح تلقائياً HTML الجديد P7-098. |
| EX7B6-12 | P7-049 | نصوص المصدر تنسخ إلى CSV مقتبس ثم يفتح ShellExecute بلا سياسة نص آمن للمستهلك؛ quoting النحوي لا يحيد تفسير بادئة صيغة.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:683-693`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:700-727` | عقد نص آمن أو ملف typed، وعدم فتح تلقائي؛ potential محفوظة ولا spreadsheet/formula نفذا. |
| EX7B6-13 | P7-050 | Nkd يعرض CSV لكنه يرسل كل امتداد إلى ExportToHtml بلا فرع؛ POS يميز.csv فعلاً، أما.xls فهو HTML متوافق مقصوداً لا workbook ثنائي مثبت.<br>`SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:242-255`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:260-286`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:679-690`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:730-767` | ملف مطابق للخيار أو HTML موسوم بوضوح وفق مستهلك معلوم؛ لا نزعم أن كل Excel يرفض HTML أو أن CSV POS هو HTML. |
| EX7B6-14 | P7-061 | POS لا يحمل GlobalID ويضعه سلسلة فارغة؛ تفاصيله توجه باسم عربي ورقم id محلي بلا branch ثم BindingInvoice يقرأ أول صف من SQL. هذا امتداد أصل الهوية لا نتيجة لكل شاشة.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:177-193`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:277-278`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:373-409`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:1861-1878`؛ `SmartAuditERP/Class/InvoiceOper.cs:3229-3244`؛ `SmartAuditERP/Properties/Resources.resx:954-958`؛ `SmartAuditERP/Properties/Resources.resx:1014-1017` | هوية GlobalID/type/branch مستقرة محفوظة في الصف و exactly-one وإعادة التفويض؛ لا اختيار أول تطابق أو routing بالنص. |
| EX7B6-15 | P7-080 | مرشح المستخدم وأوقات البداية/النهاية مرئية وقابلة للتمكين، لكن ShowResult1 لا يقرأ cmbusers/ckAllUsers ولا نصي الوقت لبناء SQL؛ يستعمل التاريخ فقط. لا ندعي وجود فلتر صنف مرئي غير موجود هنا.<br>`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:166-199`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:351-368`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml:238-250`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml:278-315` | عقد معايير immutable يقرأ كل control معلن أو يرفض unsupported، مع ID موظف ومعنى وقت/كل صحيحين. |
| EX7B6-16 | P7-084 | جهات العمل تعين isPurchase?1:2 إلى inv.proc_type بلا شرط inv_type، وتطرح اتجاه سطر 2 من 1 تحت الإجراء نفسه. proc_type الرأس عادي/مرتجع وليس شراء/بيع؛ والاتجاه المخزني ليس إجراء الرأس. شراء 100/مرتجعه 20 وبيع 60/مرتجعه 10 قد يعطيان 40 و-10 بدل 80 و 50، بوحدة 1.<br>`SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:245-310`؛ `SmartAuditERP/Class/InvoiceOper.cs:1528-1531`؛ `SmartAuditERP/Class/InvoiceOper.cs:1583-1585`؛ `SmartAuditERP/Class/InvoiceOper.cs:1613-1621`؛ `SmartAuditERP/Properties/Resources.resx:3028-3064` | كتالوج InvoiceType/HeadProc/LineImpact وإشارة تقرير واحدة، ومجموعة أنواع معتمدة؛ لا قلب رقم بلا fixture وعقد. تعارض الكاتب المرتبط P4-001 حاجز منفصل لا يفترض حدوث الحفظ. |

## 5. شواهد مقابلة تمنع التعميم

1. **ملخص POS هنا signed صريح وينقل إلى FlowDocument.** ليس جسر B5 المؤقت ولا null ولا summary افتراضية: `100−20=80` وفق قيم الإسقاط المعزولة؛ لا نمدد P7-093. الدليل:`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:308-344`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:615-618`.
2. **جهات العمل تستخدم Dispatcher لقراءة controls وتعطلها أثناء await.** لا ننسب لها P7-054 لمجرد وجود Task.Run. تبقى حسابات الأنواع والموارد/الفشل مستقلة. الدليل:`SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:110-130`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:168-194`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:326-335`.
3. **الثلاثة تقيد Inv.IS_Deleted محلياً**؛ لا نعمم P7-067 لحذف الرؤوس عليها. POS يجلب Safes من safe الصحيح؛ لا نمدد P7-087. الدليل:`SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:173-193`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:805-817`؛ `SmartAuditERP/Form_WPF/frmActsInvTotal.xaml.cs:258-270`؛ `SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:128-153`.
4. **Nkd يطبق PrintNo بحلقة؛ POS يميز CSV فعلياً.** لا ندعي أن كل الإعدادات مهملة أو أن كل CSV هو HTML، ولا أن كل Excel يرفض HTML.xls. اختلاف الوجهة/الترويسة/النسخ يبقى H7B6-03. الدليل:`SmartAuditERP/Form_WPF/frmNkdTotSalePurch.xaml.cs:338-346`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:679-690`.
5. **id من عمود int ليس مدخلاً نصياً بشرياً مثبتاً لحقن SQL.** فقد GlobalID/branch وإعادة أول صف أصل P7-061، لا توسعة آلية لحقن SQL تحت P1-011. الدليل:`SmartAuditERP/Properties/Resources.resx:954-958`؛ `SmartAuditERP/Form_WPF/frmItemsalesdetailsPos.xaml.cs:373-409`؛ `SmartAuditERP/Class/InvoiceOper.cs:3229-3244`.
6. العنوان «إجمالي» في Nkd أوطرح المرتجع في Acts لا يحسم gross/net أوحصة خصم/ضريبة/GL. لم نعد عد P7-083 بلا عقد؛ و Customers.act الحية تطرح سؤال تصنيف تاريخي لا عيباً جديداً مثبتاً من تلقاء الاسم.
7. فشل مصدر يرجع 0 مختلف عن مجموع صحيح 0؛ وجود log أو Dispatcher أو GlobalID join لا يثبت شمول مصدر أو تفويضاً أوشفاء النتيجة بعد الخطأ.
8. HTML raw interpolation ثابت محلياً، لكن **لا script أوصيغة أو Excel أو DOM مستهلك فعلي نُفذ**.20 نموذجاً يدوياً ليست ترجمة قابلة للتنفيذ لبرنامج C# أو SQL ولا استنساخاً لمخرجاته.

## 6. التحقق والتسليم والباقي

<!-- B6-VERIFICATION-RESULTS -->
**خرج فعلي ناجح لمدقق التوثيق، لا قبول ERP:** exit0 و `errors=[]`، بعد إنشاء سجل checks من stdout ثم إعادة فحصه؛ `current_output_record_pending_first_write_not_placeholder=false` من التشغيل نفسه، لا تعديل يدوي للنتيجة.

| الفحص المنفذ | النتيجة وحدها |
|---|---|
| مصدر التطبيق وcheckout | مرجع 10ba215 ثابت وcheckout d0ae6b3 منفصل؛ ancestry وصافي دلتا 204 مسارات توثيق ملتزمة، ثم مطابقة مستقلة لكل 827 مساراً وبصمتها |
| حماية التاريخ | **199 artifact** مطابقة لبصمات الدخول، بينها checksB5 الفعلي؛ لقطة 266 وفهارس B5 الدقيقة لم يعاد توليدها |
| انتقال السجل | **266 نواة وكل next_phase محفوظة**،16 ذيلاً مطابقاً للـ manifest و4 جديدة فقط؛ أول 110 صفوف G محفوظة حرفياً، والحالي 116 مجموعة لا نتائج إضافية |
| النطاق والروابط | **16248 إحالة نطاق و2141 رابطاً محلياً مع التكرار**، و 13/26/19/7/31 وجميع روابط IDs/ثوابت/خطط ودفتر 827/فرز98/شاشات52 متسقة؛ ليست شهادة قراءة دلالية أو feature completion |
| أدوات تدقيق فقط | **27 ملف Python نجح تحليلها نحوياً، و132 حالة مدقق اصطناعية اجتازت**:104 تاريخية +28 جديدة؛ منها 8 حالات هوية source/checkout بأمثلة مصطنعة |
| الشاهد التوثيقي B6 |20 نموذجاً يدوياً مستقلاً +20 ملاحظة نصية محدودة؛ إعادة حسابها مطابقة للملف المحفوظ، لا نتائج C#/SQL/Office أوتفسير صيغة |
| القطع التاريخية المستقلة | **11 أمر CLI نجح**:2–6 ثم7A وB1–B5 بأعداد 49/74/106/137/172/200/223/237/248/261/266؛ كل منها بمدخلاته المجمدة لا270/فهارس اليوم، ودون كتابة أو إعادة تأريخ checks محمي |
| ما لم ينفذ | **ERP0 وSQL/مزود0 ومعالجة0**؛31 خطة قبول/بوابة not-executed، و7B7/7C باقية، و8 غير مأذونة |

الملف `evidence/checks-07B6.json` خرج stdout فعلي محفوظ، **ليس placeholder ولا صياغة يدوية ولا إعادة إنتاج bytes لتاريخ checks المحمية**. نجح `collect_baseline.py --verify` دون `--write`؛ لا تغيير تطبيق أو baseline. التحقق الوثائقي لا يغلق نتيجة أويعوض schema/سياسة/ACL/قوالب أويرخص تشغيل8.
<!-- END-B6-VERIFICATION-RESULTS -->

- [نموذج المصدر والمصفوفة 26 والثوابت 19 والعقود 7 و H/Q/backlog](POS-ACTS-TOTALS-07B6.md).
- [حدود المدقق والخطط 31](VALIDATION-07B6.md)، [witness20+20](evidence/report-witnesses-07B6.json)، [checksB6 الفعلي](evidence/checks-07B6.json).
- **التالي 7B7 ضمن إذن تدقيق 7، ثم 7C أو أجزاء إضافية معلنة/استبعادات مسندة.** تبقى بقية المالية/الإخراج ومرشحو غير regex والأطفال، و HR/PM/بحري/موارد/واجهة/وصول/ثقافات/أداء. لا إغلاق 7B/7 من union353 أو 31 خطة أو push.
- لا طلب أسرار أو بيانات أشخاص/إنتاج. تبقى H/Q السابقة وتضاف H7B6/Q7B6؛ قواعد وفهارس/latency/تسرب تحتاج عقود مخطط/خطط وقياساً مأذوناً، لا بحثاً نصياً.

[الفهرس](README.md) · [الخطة](PLAN.md) · [التحسينات](IMPROVEMENTS.md) · [سجل النتائج](findings.csv)
