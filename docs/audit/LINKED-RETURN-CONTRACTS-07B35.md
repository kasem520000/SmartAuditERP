# عقود المرتجع المرتبط — 7B35/R4s

**مصدر التطبيق:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ **الفرع:** `arena/94ae8414-smartauditerp`.
**دخول B35:** تسليم B34 المدفوع `e6f022ab5df771aab9631886ad713a8a7e6dfbfa`؛ **1075 مادة تدقيق و335 نتيجة مفتوحة** قبل إضافات هذه الشريحة.
التاريخ المرجعي المورّد حالياً **2026-11-16 UTC**،بينما أبلغت ساعة البيئة الخام عند التجميد عن `2026-11-20T21:36:10.691950+00:00`. هذا تعارض مسجل،لا معايرة للتقويم ولا إعادة وسم لأثر مستهلك. [توضيح التاريخ والهوية](DATE-IDENTITY-NOTE-07B35.md).

**تدقيق ساكن فقط؛لا تعديل للتطبيق أو إصلاح أو تشغيل ERP. R4s/7B35 شريحة محدودة؛7B والمرحلة7 جزئيتان؛7C لم تبدأ؛8 غير مأذونة هنا.** الإصلاح مستقل،وبدؤه وتزامنه غير معلومين؛لا دمج repair→audit أو كتابة ملفاته أو إغلاق نتائج. `next_phase=8` تخطيط لا تفويض.

[الخلاصة](PHASE-07B35.md) · [عقود المرتجع المرتبط](LINKED-RETURN-CONTRACTS-07B35.md) · [التحقق](VALIDATION-07B35.md) · [المتبقي](PHASE-07-REMAINING-07B35.md) · [الهوية](DATE-IDENTITY-NOTE-07B35.md) · [النطاق](review-scope-07B35.csv) · [قرار الاختيار](evidence/scope-decision-07B35.json) · [السجل دون تعديل](findings.csv) · [stdout الرسمي](evidence/checks-07B35.json)

## 1. الثوابت الأربعة غير القابلة للاستبدال

1. **AbandonDecision** مستقل عن قبولDocumentRef. لا تعني موافقة الهدف التخلي عن الأصل.
2. **AcceptedDocument** مستقل عن **AcceptedLines**. لا يعيدfalse للثاني بالضرورة ما كُتب قبل عرضه.
3. **ref/child field boundary** مستقل عن **CLR alias/clone contract**. توثق التعليمات ولا تفترض مصدرDTO المفقود.
4. **Prepared/Applied** مستقلان عن **SaveResult/stock/ACL**. نموذج الرمز ومرشح الرقم لا يثبتان حفظاً أو حجزاً أو خسارة.

النطاق current-year sale(2,2)/purchase(1,2) فقط. تفاصيل الدليل والشروط في[الخلاصة](PHASE-07B35.md)،والمدخلات والاستبعادات والأثر والخروج لكل قدرة في[FE16](evidence/feature-implementation-matrix-07B35.csv). لم تشمل القراءة أجسام إنشاء/قبول/إغلاق حوار البحث الأول؛الاعتماد على بوابة المستدعي وترتيبها،لا على نتيجةchrome أوتسلسلLoaded مفترض.

اجتاز الفحص الوثائقي التمهيدي المستقل1242/36،مع بقاء خطط القبول التشغيلية غير منفذة؛هويته وحدود الالتقاط الرسمي اللاحق موثقة في[التحقق](VALIDATION-07B35.md).

## 2. crosswalk محدود — 16 قدرة و32 خطة غير منفذة

| FE/INV | القدرة المحددة | النتيجة القائمة/العقد | خطتا القبول — not-executed | المالك |
|---|---|---|---|---|
| FE7B35-01 / INV7B35-01 | المدخل والإظهار وحد النوع والسنة | P7-159 | P7B35T-01;P7B35T-02 | مالك WPF وأوامر الإدراج ونتائج الحوارين |
| FE7B35-02 / INV7B35-02 | تمرير Stay من أمر جديد في المشتريات | P7-159 | P7B35T-03;P7B35T-04 | مالك WPF وأوامر الإدراج ونتائج الحوارين |
| FE7B35-03 / INV7B35-03 | أول تصفير في البيع قبل البحث | P7-159 | P7B35T-05;P7B35T-06 | مالك WPF وأوامر الإدراج ونتائج الحوارين |
| FE7B35-04 / INV7B35-04 | حارس البحث وحد رجوعvoid | P7-160 | P7B35T-07;P7B35T-08 | مالك WPF وأوامر الإدراج ونتائج الحوارين |
| FE7B35-05 / INV7B35-05 | تحميلref قبل قبول البنود | P7-160 | P7B35T-09;P7B35T-10 | مالك SDK/DTO وref والنسخ والمجموعات والتحميل |
| FE7B35-06 / INV7B35-06 | Close/Escape وحقل الطفل مقابل الأب | P7-160 | P7B35T-11;P7B35T-12 | مالك WPF وأوامر الإدراج ونتائج الحوارين |
| FE7B35-07 / INV7B35-07 | قبول الكل وNoSelection | P4-013 | P7B35T-13;P7B35T-14 | مالك هوية السطر ونتيجة الجزء والفشل والتحضير |
| FE7B35-08 / INV7B35-08 | هوية السطر وItemId القائمة | P4-013 | P7B35T-15;P7B35T-16 | مالك هوية السطر ونتيجة الجزء والفشل والتحضير |
| FE7B35-09 / INV7B35-09 | إلغاء الجزء ثم ذيل التحويل | P7-160 | P7B35T-17;P7B35T-18 | مالك WPF وأوامر الإدراج ونتائج الحوارين |
| FE7B35-10 / INV7B35-10 | مرجع البيع قبل مرشح الرقم | P7-160 | P7B35T-19;P7B35T-20 | DBA ومالك الفرع والأهلية والصلاحيات والحفظ |
| FE7B35-11 / INV7B35-11 | مرجع الشراء بعد مرشح الرقم | P7-160 | P7B35T-21;P7B35T-22 | DBA ومالك الفرع والأهلية والصلاحيات والحفظ |
| FE7B35-12 / INV7B35-12 | Failed/Partial/null ليست قبولاً | P7-160 | P7B35T-23;P7B35T-24 | مالك SDK/DTO وref والنسخ والمجموعات والتحميل |
| FE7B35-13 / INV7B35-13 | dirty والأعلام ليست SaveResult | P7-159;P7-160 | P7B35T-25;P7B35T-26 | مالك المنتج وسياسة المرتجع وقصد النسخ وترك المسودة |
| FE7B35-14 / INV7B35-14 | عقودDTO/alias والسنة غير المحسومة | H7B35-02 | P7B35T-27;P7B35T-28 | مالك SDK/DTO وref والنسخ والمجموعات والتحميل |
| FE7B35-15 / INV7B35-15 | حفظ السجل ومنع إعادة العد | H7B35-06 | P7B35T-29;P7B35T-30 | مالك نطاق التدقيق والأنساب والتسليم المستقل |
| FE7B35-16 / INV7B35-16 | بقية7B والأنساب والتسليم المستقل | H7B35-06 | P7B35T-31;P7B35T-32 | مالك نطاق التدقيق والأنساب والتسليم المستقل |

لكل صف فيCSV مدخل entry_point ومصدر source_contract وحد output_boundary واستبعاد excluded_from_claim ومالك ومدخل منقح وأثر غيابه وخطوة؛لكل خطة prerequisites/procedure/acceptance_criterion وسلامة وحالةnot-executed. الجدول المختصر لا يستبدلها أو يحول16 إلى حصر لكل القدرات.

## 3. LN8 وNR8

### LN8 — مسار الأمر والتحويل

| المعرف | FE المرتبطة | الجذور/العقود | الحد الموثق | الحالة |
|---|---|---|---|---|
| LN7B35-01 | FE7B35-01;FE7B35-02 | P7-159 | زر الإدراج XAML في البيع(2,2) والشراء(1,2) للسنة الحالية → أمر linked-return فقط،لا إثبات وصول فعلي أو أحداث واجهة أو صلاحيات منشورة ∣ btnInsertLinkedInv_Click → btnNew_Click → CheckBeforeClear → رفض محلي لا يخرج من caller الإدراج وفق ترتيب التعليمات | not-executed |
| LN7B35-02 | FE7B35-03;FE7B35-04 | P7-159;P7-160 | InsertLinkedReturn(2,1) معReturnYearPreviews=false → تعيينInvoiceDGVجديدةفيحالةالأبقبلحسمهدفأوجزء ∣ InsertFromInvبعدرجوعShowDialogالأول → رفضالبحثيوقفbindلكنلايعيدpreclearولاينقلCancelledللأب | not-executed |
| LN7B35-03 | FE7B35-05;FE7B35-06 | P7-160 | قبولالبحث→BindingInvoice(refInvo)→frmInvoiceItems → حالةتحميلعلىالأبقبلAcceptedLines،لافقطالتعيينالنهائي ∣ btnClose/Escape→CloseWithoutResultلـInvTypeغير23 → استبدالحقلchildالمحليليسrollbackصريحاًلـrefالأب | not-executed |
| LN7B35-04 | FE7B35-07;FE7B35-08 | P4-013 | btnAddallمقابلInsertSelectedItemsعندماselectedRows.Count=0 → رجوعمعالجالصفريليسقبولاًولارجوعاًتلقائياًمنShowDialog ∣ InsertSelectedItemsثمRemoveNonSelectedItems → يمكنلسطرينأصليينمختلفينلنفسالصنفأنيبقياويتلقياالقيمذاتها | not-executed |
| LN7B35-05 | FE7B35-09 | P7-160 | BindingInvoiceبقيمموردةثمchild.ISDone=falseثمعودةvoid → يمكنللقيمالمحملةأنتكونمدخلتحويلرغمعدمقبولالبنود | not-executed |
| LN7B35-06 | FE7B35-10;FE7B35-11 | P7-160 | ذيلInsertLinkedReturnثمLoadInvNo → فشلالرقمالمورّدلايعيدالإسناداتالسابقة،ولايثبتأنالمرجعGID ∣ PrepareReturnInvoice(Purchase,2,2) → عندفشلالرقملاتصلتعييناتالمرجعالتاليةلكنالملاحظةوالدفعاتالسابقةقدوصلت | not-executed |
| LN7B35-07 | FE7B35-12;FE7B35-13 | P7-160;P7-159 | catchInsertFromInvومخرجاتالقارئالموردة → عودةطبيعيةللمساعدلاتعنيكتمالالتحميلأوالتحويل ∣ CheckBeforeClearوResetInvoiceوحدISNewقبلCalcRows → إثباتحدمحليمعclean/dirtyمورّدتينفقط | not-executed |
| LN7B35-08 | FE7B35-14;FE7B35-15;FE7B35-16 | H7B35-02;H7B35-06 | H7B35-02/04وعقودSDKوالسنةوالفروعالمستبعدة → handoffبعقدمنقحومالكوأثرعدممدخللاabsenceproof ∣ dedup335metadata/83pathrows/15sectionsثمقرارالنطاق → صفرnew/ext؛335قاموساًوraw336كاملةكماالدخول ∣ RS14/SP3/HQ6/RW10/BK10منB34 → 7B/7جزئيتان؛7Cلمتبدأو8غيرمأذونة؛حالةبدءالإصلاحوتزامنهغيرمعلومة | not-executed |

### NR8 — نتيجتا البحث والبنود

| المعرف | FE المرتبطة | الجذور/العقود | الحد الموثق | الحالة |
|---|---|---|---|---|
| NR7B35-01 | FE7B35-04 | P7-160 | InsertFromInvبعدرجوعShowDialogالأول → رفضالبحثيوقفbindلكنلايعيدpreclearولاينقلCancelledللأب | not-executed |
| NR7B35-02 | FE7B35-05 | P7-160 | قبولالبحث→BindingInvoice(refInvo)→frmInvoiceItems → حالةتحميلعلىالأبقبلAcceptedLines،لافقطالتعيينالنهائي | not-executed |
| NR7B35-03 | FE7B35-06 | P7-160 | btnClose/Escape→CloseWithoutResultلـInvTypeغير23 → استبدالحقلchildالمحليليسrollbackصريحاًلـrefالأب | not-executed |
| NR7B35-04 | FE7B35-07;FE7B35-08 | P4-013 | btnAddallمقابلInsertSelectedItemsعندماselectedRows.Count=0 → رجوعمعالجالصفريليسقبولاًولارجوعاًتلقائياًمنShowDialog ∣ InsertSelectedItemsثمRemoveNonSelectedItems → يمكنلسطرينأصليينمختلفينلنفسالصنفأنيبقياويتلقياالقيمذاتها | not-executed |
| NR7B35-05 | FE7B35-09 | P7-160 | BindingInvoiceبقيمموردةثمchild.ISDone=falseثمعودةvoid → يمكنللقيمالمحملةأنتكونمدخلتحويلرغمعدمقبولالبنود | not-executed |
| NR7B35-06 | FE7B35-10;FE7B35-11 | P7-160 | ذيلInsertLinkedReturnثمLoadInvNo → فشلالرقمالمورّدلايعيدالإسناداتالسابقة،ولايثبتأنالمرجعGID ∣ PrepareReturnInvoice(Purchase,2,2) → عندفشلالرقملاتصلتعييناتالمرجعالتاليةلكنالملاحظةوالدفعاتالسابقةقدوصلت | not-executed |
| NR7B35-07 | FE7B35-12;FE7B35-13 | P7-160;P7-159 | catchInsertFromInvومخرجاتالقارئالموردة → عودةطبيعيةللمساعدلاتعنيكتمالالتحميلأوالتحويل ∣ CheckBeforeClearوResetInvoiceوحدISNewقبلCalcRows → إثباتحدمحليمعclean/dirtyمورّدتينفقط | not-executed |
| NR7B35-08 | FE7B35-14;FE7B35-15;FE7B35-16 | H7B35-02;H7B35-06 | H7B35-02/04وعقودSDKوالسنةوالفروعالمستبعدة → handoffبعقدمنقحومالكوأثرعدممدخللاabsenceproof ∣ dedup335metadata/83pathrows/15sectionsثمقرارالنطاق → صفرnew/ext؛335قاموساًوraw336كاملةكماالدخول ∣ RS14/SP3/HQ6/RW10/BK10منB34 → 7B/7جزئيتان؛7Cلمتبدأو8غيرمأذونة؛حالةبدءالإصلاحوتزامنهغيرمعلومة | not-executed |

## 4. خطط القبول — لا تنفيذ تشغيلي

P7B35T-01–06 للمدخل وStay وpreclear،07–12 لرفض البحث وref وإلغاء الطفل،13–18 للكل والجزء وItemId،19–26 لترتيب المرجع والرقم والفشل والأعلام،27–32 للعقود الخارجية والسجل والأنساب. كلها **not-executed**،بإذن قبول مستقل لاحق ومراقب حدود اصطناعي ومدخلات منقحة؛لا ERP/SQL/WPF/SDK أو أعمال حقيقية هنا.

## 5. مصالحة النتائج والقرارات

[RC6](evidence/report-reconciliation-07B35.csv) يحفظ unions الأدلة والـFE والجذور وخطط القبول بدقة. [AD8](evidence/root-adjudication-07B35.csv) يحفظ سبب عدم إنشاء164 وعدم إلحاقevidence؛[السجل](findings.csv) لا يتغير.

حُفظت **1071 مادة دخول محمية من1075 بايتياً**،وتشمل `findings.csv` نفسها: **كل335 قاموساً بكل حقل وكامل raw336CRLF/222939 بايت،دونBOM**. لا تعديل evidence أو status أو classification أو severity أو certainty أو أي next_phase. أربعة مسارات دخول فقط معلنة قابلة للتحديث:README/PLAN/IMPROVEMENTS وtools/validate_audit.py؛بقية العمل ملفاتB35 جديدة.

**G01–256 وصفوفها exact؛G257–260 توصيات غير منفذة لا أربع نتائج أخرى.** بقيت827 أصل تطبيق/29,128,444 بايت كما هي. تشمل الحماية جميع موادB34: RQ8/AW8/FE16/INV16/RC6/AD8/T32/RS14/SP3/HQ6/RW10/BK10/ext0،الشاهد وأرشيف39 وبرهانه وstdout الرسمي وإيصاله ومحاولاته ومذكرة التحذير؛وB33 OS8/OV8 وB32 EO8/DG8 وجميع الدفاتر الأقدم. التزاماتB34 التاريخية1018/1022 وG252،وB33 التاريخية976/981 و334/raw335prefix/G248،لا يستبدلها العد الحالي.

**P4-014 وP7-108 وP7-132 وP7-145 potential كما هي**؛020/021 وحواجز المال وACL والمخزون والحفظ والإنتاج باقية. ذيل159 فيB30 وتوسعة046 فيB28 محفوظان. تصحيحB10 الإضافي10 محلياً/120 مرجعياً/equality1=10 باقٍ دون تحريرG138.

لم ينفذ ERP/build/C#/VB/.NET/WPF/ShowDialog/SQL/DataView/provider/SDK/REPX/ToDataTable أو طابعة/ماسح أو بيانات أعمال/أسرار أو حفظ أو حجز رقم أو إصلاح أو قياس أو قبول تشغيلي. قيم dirty/count والإجابة والرجوع الطبيعي والـreader snapshot والفشل مدخلات رمزية موردة صراحة. غياب تعريفDTO أو تعيينdirty محلي لا يثبت غياب حماية؛ملكية المجموعات وclone/setters/events والتحميل الجزئي عقود مفتوحة.

**كل32 خطةB35 وجميع الخطط التشغيلية السابقة،ومنها32B34/B33/B32/B31/B30/B29/B28 و36B27،not-executed.** تشغيل نماذج Python التوثيقية أو مدققها لا ينفذ خطة قبول متكاملة ولا يثبت إصلاحاً.

تبقى بقية callers/dialogs/editors/fields/writers/outputs وDocumentRef/allowed-set/branch/reset/dirty/cancel/failure وProduct/BulkPatch/LineRef/OwnedSeed/PropertiesResult/basket/RepeatOutcome ضمن **SP01 و7B**. وتبقى السنة السابقة وفروعQuotation و21/22/23 والعقد وكلcaller آخر خارج حكم هذه العينة. لا تتوسع شهادة الشريحة من مجرد قراءة سياق تلك الفروع.

**SP02** لحصر القدرات entry/source/output وcrosswalk455FE والدفاتر اللاحقة،و**SP03** لعقودSDK/DTO/constructors/collections/currency/precision/words/legacy/templates والسياسات،ضمن7B صراحة. هذا التتبع لا يفتتح محورC3 العام ولا ينقل غير المراجع إلى7C.

التالي **R4t/7B36 أو split مسبب منSP7B35-01–03**: قدرة ومدخل ومصدر وحد مخرج واستبعاد ودليل ومالك ومدخل منقح وأثر غيابه وخطوة وخروج ساكن. لا وعد بمدة أو جلسات أو آخر جزء أو نسبة قدرات أو إتمام المنظومة. يسلم SHA تدقيق محدد إلى الإصلاح المستقل دون افتراض بدئه أو تزامنه أو دمج تعديلاته هنا.
