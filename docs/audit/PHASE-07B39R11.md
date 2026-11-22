# 07B39R11 — إكمال البند 3 من 7C: عائلة بحث الصنف ووحدته وكميته وسعره وخصمه وضريبته

**7C جارية؛ المرحلة 8 كإصلاح جارٍ على فرع منفصل بتوجيه المالك (fix/stage1-p1-security وfix/stage2-p2-authz)؛ صفر شهادة خروج قدرة/أسرة جديدة.** تقييم ساكن على `arena/94ae8414-smartauditerp` من R10 المنشور `0f6559cf6853cc580b6fe3a2c63100e40f673453`.

[مراجعة المصدر](SOURCE-REVIEW-07B39R11.md) · [عقد عائلة البحث](evidence/search-item-family-contract-07B39R11.json) · [التحقق](VALIDATION-07B39R11.md)

## سياق الشريحة

بوابة بدء 7C (R10) حمّلت البند 3 «بقية الكتّاب والمساعدات غير المقروءين» وتحديدًا التزام R9 المحلي: **SearchByID/ItemOper ومنطق الدمج/الاستبدال/الوحدة/الكمية/السعر/الخصم/VAT**. هذه الشريحة تسدد ذلك الالتزام كاملًا: قُرئت الأداة المركزية `ItemOper` بمناهجها الستة عشر، وكل متغيرات `SearchByID` الثلاثة عشر في المحررات، ومسارات باركود POS الكاملة، وتغيّر الوحدة، وكتل الحساب والتحقق.

## ما قُرئ فعليًا

- **`Class/ItemOper.cs` (2,950 سطرًا):** SearchForBarcode، GetItemByID (بمنطق التكرار كاملًا 1082–1136)، LoadItemInf، LoadItemDetails، ItemExpire، LoadUnitInf، LoadCustomerPrice، CheckForCategoryOffer، CheckForItemOffer، AddItemOffer، CalcRows، CalcTotal، IsValidDiscount، IsValidPrice، checkQtyLimi، ISvalidQuantity.
- **متغيرات `SearchByID` الثلاثة عشر:** frmInvPurch، frmInvSale، frmSalesInvoice، frmPOS، frmInvPOS، frmcontract، frmSalePurch، frmPurchInv، frmInvInOutput، frmProductionOrder، frmOffers، frmInventoryTransfer، frmInvInputOutput — مع SearchByName/SearchByCode المرافقة في مواضعها.
- **مسارات frmPOS للباركود كاملة:** ReadBarcode (2675–2782) بفروعه الثلاثة، وLoadItemInf المحلي، وCalcVAT.
- **تغيير الوحدة:** ShowItemUnit في frmInvPurch (974–1008) وfrmInvSale (795–825).

التجزئات والأسطر محفوظة في [ملف العقد](evidence/search-item-family-contract-07B39R11.json). القراءة ساكنة: لا تنفيذ، لا تصديق SqlClient، لا مخطط منشور.

## الجذور السبعة الجديدة (P7-166 → P7-172)

| الجذر | الخطأ | الدليل الأبرز |
|---|---|---|
| **P7-166** High/confirmed | عائلة بحث الصنف/الباركود/الكود/الاسم/السيريال تبني SQL بدمج نصي مباشر بلا معاملات ولا تهريب — 22 موقعًا موثقًا عبر ItemOper وfrmPOS وfrmSalesInvoice وfrmInvSale وfrmInvPurch وfrmcontract وfrmInvPOS وfrmSalePurch | ملف العقد: string_interpolation_sites |
| **P7-167** High/confirmed | باركود الميزان في POS: `SearchByID` مع `IsBarcode=true` يضيف سطرًا جديدًا ثم يكتب الكود الوزن/السعر في `_gridSource[0]` (2745/2761) بدل السطر المضاف — يعمل صدفة عند فراغ الشبكة ويفسد البند الأول عند وجود بنود | frmPOS.xaml.cs:2737-2768 |
| **P7-168** Medium/confirmed | فرع Wscale ليس 1 أو 2 في POS: لا else — الصنف موجود ولا إضافة ولا رسالة؛ بينما SearchForBarcode يدعم wscale=3 (سعر+كمية) | frmPOS.xaml.cs:2730-2769 مقابل ItemOper.cs:2023-2051 |
| **P7-169** Medium/confirmed | مطابقة المكرر تختلف بين المحررات: خمسة يقارنون ItemId فقط (يتجاهلون الوحدة)، وfrmOffers لا تفحص أصلًا، وPOS يقارن الصنف+الوحدة بلا حوار وبلا إعداد RepeatItem، وItemOper يقارن الصنف+الوحدة+الباركود بحوار وإعداد | جدول التباين في ملف العقد |
| **P7-170** Medium/confirmed | تغيير وحدة بند قائم يستدعي LoadUnitInf التي تضبط `ItemQuantity=1` قسرًا في فرعيها (761/796) فتفقد الكمية المدخلة بصمت بلا تأكيد | frmInvPurch:974-1008؛ frmInvSale:795-825 |
| **P7-171** Medium/potential | POS يعرض `VatPerDgv` من قيمة `Items.tax` الخام (971) بينما CalcVAT يحسب بضريبة الفاتورة الافتراضية لأي ضريبة صنف غير صفرية — العرض والحساب يفترقان حين تختلف القيمتان | frmPOS:971 مقابل 753-780؛ ItemOper:532-535؛ ItemOpercontract:1220-1223 |
| **P7-172** Low/confirmed | `invo.InvoiceItems.OrderByDescending(x => x.ItemRowIndex);` بلا استقبال نتيجة (1184–1185): لا ترتيب يحدث إطلاقًا — نية «الأحدث أولًا» غير منفذة | ItemOper.cs:1184-1185 |

## ما لم يُسجَّل جذورًا (مغطى أو خارج حد التأكيد)

- **مغطى بجذور قائمة:** سياسة سعر الوحدة الموجودة (P4-026)، حالة IsPriceFromBarcode الستاتيكية (P4-028)، حارس المخزون غير الذري (P4-014)، إهمال كمية/سعر الميزان في محررات البيع/الشراء/الإدخال-الإخراج (P7-136)، اختيار أول وحدة للبادئة (P7-137)، السقوط للصفر (P7-138)، تسعير العميل (P7-142)، عكس حوار المكرر (P7-143)، آثار حوار الخصائص (P7-151/152)، ركود سعر الوحدة عند تعديل الصنف (P7-154)، ودلالات تراكم CalcTotal/CalcRows (P4-003/004/005).
- **داخل P1-011 عائلةً لا موقعًا:** حقن `InvGlobalID` (ItemOper:1859) قيمة نظامية GUID-like منخفضة الخطورة — يُدرج مع جدولة المراحل اللاحقة لمواقع P1-011 منخفضة الخطورة، ولا يكرر كجذر مستقل.
- **حد التأكيد:** ثبات `TotDiscount += InvDiscount` في CalcTotal عند الاستدعاء المتكرر خارج CalcRows يُحتمل أن يعتمّ التراكم، لكن مسارات الاستدعاء الفعلية تمر عبر CalcRows التي تعيد الضبط (1509) — **لا يرقى لجذر مؤكد بلا تتبع كل مستدعٍ**؛ يُحمل كملاحظة في مراجعة المصدر.
- **تصفير vat بعد خصمه من lineTotal** في فرع PriceIncVAT عند `VATperc==0` مع `ItemVatPerc>0` حالة بيانات غير متسقة؛ الأثر يتطلب حالة مخطط/بيانات غير مثبتة — ملاحظة لا جذر.

## حدود صارمة

- لا تنفيذ تطبيق؛ لا تصديق ربط SqlClient أو مخطط منشور أو حالات بيانات فعلية (قيم tax وWscale وRepeatItem وقت التشغيل).
- مقارنات أسماء الأعمدة معجمية من نص المصدر؛ `VatPerDgv = tax` عرضٌ، وحسم أثره على القيم المعروضة يتطلب بيانات.
- حقن الباركود/الكود/الاسم مؤكد ساكنًا كبِنية SQL، وخطورته العملية تتوقف على نقاط الدخول (ماسح/لوحة مفاتيح/استيراد نص متعدد) — كلها مسارات إدخال مستخدم مباشرة.
- `162 != 142` فشل B38 المحفوظ لم يُلمس. لا إعادة ترقيم ولا تعديل للأصل الرقمي؛ الجذور السبعة رقمت استمرارًا لآخر جذر (P7-165) والسجل الآن **344 صفًا** بتنسيق CRLF بلا BOM.
- المهاجرة أو تنفيذ ERP/SQL/WPF لم تحدث؛ صفر تشغيل تطبيق.

## التالي في 7C

أسئلة R7/R9 المحلية المفتوحة (القارئ Q/منشأ السنة/إعادة ترطيب الفرع)، ثم allowed-set لكل مستند/فرع/سنة (بوابة خروج D05/D06 وبقية القدرات الست والعشرين)، ثم توحيد دفتر المسارات التراكمي، ثم بوابة `--require-complete` للمرحلة 7 كاملة قبل أي ترخيص تدقيقي للمرحلة 8.
