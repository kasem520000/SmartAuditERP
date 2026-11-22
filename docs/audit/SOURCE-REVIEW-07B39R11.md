# SOURCE-REVIEW-07B39R11 — قراءة موجهة: عائلة بحث الصنف وأدوات الوحدة والكمية والسعر والخصم والضريبة

مرجع التقييم: 2026-11-22 UTC (غير مصادق عليه تقويميًا). القاعدة المنشورة: `0f6559cf6853cc580b6fe3a2c63100e40f673453` (تسليم R10). قراءة ساكنة فقط.

## 1. الأداة المركزية `Class/ItemOper.cs`

### SearchForBarcode (1908–2080)
ثلاث مراحل بحث: ItemUnits.barcode ثم Itembarcodes.barcode ثم فرع الميزان ذي الـ13 رقمًا ببادئة 7. **كل مطابقات الباركود دمج نصي `N'{barcode}'` بلا معاملات** (1927، 1947، 1976–1977). فكّ حمولة الميزان يدعم Wscale=1 (وزن)، 2 (سعر مضمّن)، 3 (سعر+كمية بقسمة محروسة على sale). لا تهرّب `Replace("'","''")` في الملف كله (تحقق rg: صفر نتائج).

### GetItemByID (1047–1188)
- قراءة إعداد RepeatItem من `SettingsPOSDisplay where Inv_id=3` (1056–1065) ثم استعلام الصنف (1068–1077، دمج `id={itemId}` رقمي).
- منطق التكرار (1082–1136): POS مع RepeatItem → حوار MsgExistItem (زيادة/فصل)؛ POS بلا RepeatItem → زيادة صامتة عند تطابق الوحدة والباركود وغير الميزان؛ غير POS → حوار دائمًا عند تطابق الوحدة أو unitId=0. `break` يخرج ليضيف صفًا جديدًا (سلوك «بند منفصل»).
- بناء الصف الجديد وتحميله عبر LoadItemInf (1181).
- **1184–1185: `OrderByDescending` نتيجته مهملة — لا أثر (P7-172).**
- `catch { }` يبتلع كل شيء (1187).

### LoadItemInf (497–581)
استعلام رأس الصنف → LoadUnitInf → LoadCustomerPrice → التكلفة (فرع BranchType==4/POS يأخذ purch_price مباشرة) → الرصيد → **ضريبة السطر (532–535): `ItemVatPerc = invo.VATperc` ثم لا تُستبدل إلا إذا كانت ضريبة الصنف صفرًا** — أي ضريبة صنف غير صفرية تُتجاهل قيمتها وتُستبدل بافتراضية الفاتورة؛ ثم الخصم الافتراضي والخصائص (prop 2–5، 8) وLoadItemDetails للخصائص التفاعلية (حواريات داخل مسار التحميل).

### LoadUnitInf (733–917)
فرع ItemUnits الموجودة (743–772): يضبط **`ItemQuantity = 1` قسرًا (761)** وسعر الوحدة purch/sale حسب InvType — هذا الاستدعاء نفسه يستخدمه تغيير الوحدة للبند القائم (P7-170). فرع الاحتياط عبر Items.unit (774–914): `UnitEquality=1` و`ItemQuantity=1` (796) وسياسات ResolvePrice بفروع PriceIncVAT وSettingGeneral.

### CalcRows/CalcTotal (1367–1645)
CalcRows يعيد ضبط المجاميع ويعيد حساب السطر: SumPrice، العروض (CheckForItemOffer ثم CheckForCategoryOffer)، الخصم، ثم VAT بفرعي PriceIncVAT (خصم داخلي) أو الإضافة الخارجية، وضريبة إضافية بشرط `ItemPriceWithoutVAT < 25 → 25.0*Qty`، وتصفير vat لـBeginingInventory أو VATperc==0 (1463–1465)، وWithholding عند EtaSetting.Active. **1509: `TotDiscount = ItemsDiscount` (ضبط لا تراكم)** ثم CalcTotal عند InvDiscount>0 — وCalcTotal **1642: `TotDiscount += InvDiscount`** (تراكم إن استُدعي متكررًا خارج CalcRows؛ المستدعون المعروفون يمرون عبر CalcRows أولًا؛ لا جذر بلا استدعاء متكرر مرصود).

### IsValidDiscount/IsValidPrice/checkQtyLimi/ISvalidQuantity (1651–1902)
- IsValidDiscount: قراءة سقفي الخصم (نسبة/مبلغ) لكل صف مطابق؛ التجاوز (بدون علم تجاوز المستخدم) → تصفير الخصم كليًا لا قطعه عند السقف.
- IsValidPrice: تجاوز الأعلى → تحذير فقط؛ تجاوز الأدنى → تحذير وإرجاع السعر الافتراضي؛ أقل من التكلفة → تحذير فقط.
- checkQtyLimi: تحذيرات حد أدنى/أعلى بلا منع.
- ISvalidQuantity: يجمع استهلاك الصنف في كل الصفوف (بما فيها الحالي)، وغير الجديد يضيف قيمة Inv_Sub المحفوظة، والسالب الجديد (بلا SaleByMinus وغير ItemType 5) يقصّ الكمية إلى الرصيد؛ تعديل الفاتورة القديمة لا يقصّ بل يعرض رسالة فقط. **1859: `InvGlobalID='{...}'` دمج نصي لقيمة نظامية (منخفض الخطورة).**

## 2. متغيرات المحررات

- **مسار ItemOper المشترك:** frmInvPurch (613–623) → GetItemByID+CalcRows؛ frmInvSale (665–682) → يضيف ISvalidQuantity؛ frmInvPOS (936–955) كذلك؛ frmcontract (1747–1762) عبر ItemOpercontract؛ frmInventoryTransfer (602–615)؛ frmInvInputOutput (427–440).
- **مطابقة محلية ItemId-only (P7-169):** frmSalesInvoice (1393–1477: يستقبل unitId ولا يستخدمه في المطابقة 1426؛ حوار MsgExistItem؛ `RemoveAt(RowIndex)` عند 1452–1453 لاستبدال صف الكتابة)؛ frmSalePurch (436–470)؛ frmPurchInv (548–575 يقارن ItemIdDgv نصيًا)؛ frmInvInOutput (912–950 بحوار MessageBox YesNoCancel ثلاثي الخيارات)؛ frmProductionOrder (1159–1210 بحوار MsgExistItem).
- **frmOffers (837–878): لا فحص تكرار إطلاقًا — إضافة غير مشروطة** (ضمن P7-169).
- **frmPOS (867–955):** يقارن ItemId+وحدة (897–898)؛ `found && !IsBarcode` (906) يزيد الكمية؛ من الباركود → صف جديد دائمًا؛ **لا يقرأ إعداد RepeatItem ولا يعرض حوار MsgExistItem** (تباين موثق ضمن P7-169). حارس التعديل `!ISNew && ProcType != 3` يمنع تعديل السابقة.

## 3. مسارات الباركود في frmPOS (2675–2782)

المرحلتان الأولى والثانية دمج نصي (2687، 2704). فرع الـ13 رقمًا: بادئة 7 دمج نصي (2725)؛ بعد العثور:
- **Wscale=1 (2737–2752):** `IsBarcode=true` → SearchByID يضيف صفًا جديدًا → **`_gridSource[0].QuantDgv = qty` (2745)** — الصف المضاف أشار إليه `RowIndex` داخل SearchByID (936) لكن المتصل يكتب في الصف الأول.
- **Wscale=2 (2753–2768):** بالمثل **`_gridSource[0].priceDgv = price` (2761)**.
- **لا else لقيم Wscale الأخرى** (P7-168) — سقوط صامت بينما SearchForBarcode يدعم 3.
- LoadItemInf المحلي (957–989): `VatPerDgv = tax` الخام (971) وCalcVAT (753–780) يحسب بـ`InvObj.VAT` لأي ضريبة غير صفرية (P7-171).

## 4. تغيير الوحدة (P7-170)

frmInvPurch.ShowItemUnit (974–1008) وfrmInvSale.ShowItemUnit (795–825): بعد اختيار الوحدة الجديدة يستدعيان LoadUnitInf للبند القائم — التي تضبط `ItemQuantity=1` في فرعيها (761، 796) — بلا تأكيد ولا حفظ للكمية السابقة، ثم CalcRows وBindingDGV.

## 5. نطاق القراءة مقابل ادعائها

قُرئت الأجسام المذكورة أعلاه بأسطرها وتجزئاتها المحفوظة في ملف العقد. لم تُقرأ في هذه الشريحة: كاتب أعمق من CalcRows داخل كل محرر (مغطى R9 لستة محررات)، وفاتحات Home وأمنتُقي المفاتيح (بند منفصل محمول)، وFormPermission (R7)، والاستعادات (R7). لا تساوي هذه القراءة مراجعة قدرة أو شهادة خروج؛ تصنيفات FoundPath/التحقق ساكنة بحتة.
