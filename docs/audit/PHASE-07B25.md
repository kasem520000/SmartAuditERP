# المرحلة 7B25 / R4i — نتيجة خصائص المادة واستقرار حساب التعبئة

**تدقيق ساكن فقط — لا إصلاح أو تشغيل ERP.** مرجع الجلسة **2026-11-16 UTC**؛ مصدر التطبيق `10ba215152f722c8808aea0bb672c1d1d4d9d711`؛ الفرع `arena/94ae8414-smartauditerp`؛ دخول هذا الجزء بعد تسليم B24 المدفوع `45a2a504db4f82927a286ce425f21a82bcee7a84` مع 708 مواد و 322 نتيجة. ساعة البيئة المرصودة عند التجميد `2026-11-19T23:46:45.007507+00:00` **حقل مختلف لا يستبدل المرجع**. [إيضاح إضافي للتاريخ والالتقاط](DATE-IDENTITY-NOTE-07B25.md).

**R4i محدود؛7B/7 جزئيتان؛R4j/7B26 مقترح أو split مسبب؛7C لم تبدأ؛8 غير مأذونة هنا.** محادثة الإصلاح مستقلة على فرعها؛ لا نفترض بدءها أو تزامنها، ولا نكتب ملفات إصلاح أو ندمج repair→audit. `next_phase=8` تخطيط لا تفويض تشغيل أو معالجة في هذا الفرع.

[العقود والتتبع](PROPERTY-DIALOG-CONTRACTS-07B25.md) · [التحقق والخطط](VALIDATION-07B25.md) · [المتبقي](PHASE-07-REMAINING-07B25.md) · [scope10](review-scope-07B25.csv) · [قرار النطاق](evidence/scope-decision-07B25.json) · [السجل](findings.csv) · [الشواهد](evidence/property-dialog-witnesses-07B25.json) · [stdoutB25](evidence/checks-07B25.json)

## 1. القرار والنتيجة قبل العدد

اخترنا من SP7B24-01 سلسلة **تفصيل الصنف→حوار خصائص 2..4→نتيجة/نص→كمية البند والتفصيل في الذاكرة**، ومعها **حساب التعبئة 2 عند استدعاء Calc مرة أخرى**. إضافة شرائح محررات البيع والإدخال/الإخراج ونسختي loader كانت لتقييد الادعاء، لا لافتراض أن كل مسار يصل الحوار.

- **نتيجتان جديدتان فقط:** P7-151 و P7-152؛ Medium/confirmed من التعليمات المحلية بشروط الشاهد؛ مفتوحتان بلا معالجة.
- **التراكمي 324:**2Critical/181High/140Medium/1Low؛285confirmed/32potential/7repository-gap؛ المرحلة 7=152. حفظت 322 نتيجة سابقة **بكل حقل، ومنها ALLnext_phase/evidence/status/certainty** دون extension أو إعادة عد.
- قرئ كامل **318 سطراً C# و 313 سطراً XAML للحوار نفسه محلياً**، ومع المحيط 23 شريحة في 10 مسارات؛8 متقاطعة ومساران جديدان على اتحاد 419 فيصير 421. المكمل 406=341source/61generated/4project-resource؛ ليس نسبة أو 406 مهام 7C، ولا قراءة كل ما داخل الاتحاد.
- **DG8/PK8/FE16/INV16/RC4/AD8** تضبط النتيجة والحساب والضوابط. **32 خطة قبول كلها not-executed**؛16 شاهداً خاملاً و 16 ملاحظة نصية ليست اختبارات WPF أو أعمال.
- نُفذت **30 وضعية تاريخية OWN فعلياً** بأدوات وقت التقاطها:2–6،A،B1–24؛ كلها exit0/827/errors[]/stderr فارغ. مدخل B24 هو 322/raw323CRLF/indexes و**كل 44 حالة أصلية غير معدلة** في طفل presetB24 مع A محلي. [أرشيف 30 الحقيقي](evidence/historical-mode-verification-07B25.json) لا fixture schema أو ادعاء إعادة 30 بعد تثبيت SHA/النثر/push.

**التحقق المنفذ:** اجتاز فحص B25 الصريح **738 حالة وثائقية في 26 مجموعة** =694 محفوظة +44 جديدة؛324 نتيجة/827 أصلاً/errors[]/exit0/stderr فارغ. stdoutB25 الرسمي يلتقط مباشرة من CLI الافتراضي قبل commit التسليم، ولا يستبدل بفحص ما بعد الدفع؛ليست 738 اختبار ERP أو قبول 32 خطة. لا بناء أو C#/VB/.NET/WPF/SQL/Excel/provider/SDK/UtilitiesProj/ToDataTable/REPX أو طابعة/ماسح أو بيانات أعمال/أسرار أو قياس أو حفظ أو إصلاح نُفذ.

## 2. النتائج الجديدة

### P7-151 — مساعد خصائص المادة يطبق الكمية الصفرية بعد رجوع الحوار دون تأكيد

**Medium؛confirmed مصدرية محلية؛open-not-remediated.**

**الدليل الأساسي:** `SmartAuditERP/Form_WPF/frmItemProperties.xaml.cs:14-26;303-308`؛ `SmartAuditERP/Class/ItemOper.cs:587-655;549-574;1181-1188`؛ `SmartAuditERP/Form_WPF/frmItemProperties.xaml:263-279`.

**السلسلة:** ينشئ المساعد حواراً جديداً لخاصية 2..4. يبدأ **الحقل العام NetQnty=0**؛ Calc يكتب **txtNetQnty.Text**، وليس ذلك الحقل. المعالج Insert وحده ينقل النص إلى NetQnty ثم يحاول DialogResult=true ويغلق. المستهلك يستدعي ShowDialog دون التقاط bool? أو فحص النتيجة، ثم يبني الوصف ويعين ItemQuantity للبند ولأول تفصيل من الحقل العام. عند خاصية 2 يكتب FillValue من الارتفاع؛ وفي 3/4 يكتب الارتفاع والعرض أيضاً.

**الشاهد:** بند/تفصيل بكمية 6، وحوار جديد نص نتيجته 60، ورجوع طبيعي **دون تنفيذ Insert** مع نتيجة false أو null موردة. يبقى الحقل العام 0، ومع ذلك تصبح كمية الكائن والتفصيل 0 ويتغير الوصف؛ النص 60 لا يحميهما. لا نفترض أن لفتة إغلاق WPF بعينها تعيد null أو false، ولا أن كل إلغاء يسبب خسارة محفوظة.

**حد الإلحاق:** في السلسلة المختارة يحمل LoadItemInf الخاصية و FillRatio ويستدعي الحوار؛ GetItemByID يلحق newItem بعد الرجوع الطبيعي من LoadItemInf دون نتيجة تفاصيل نوعية. مع lookup ناجح وغياب فرع تكرار مبكر يمكن تمثيل وصول المحاولة الصفرية إلى القائمة في الذاكرة. هذا لا يثبت مصيرها بعد الحارس/الحساب/الحفظ أو أن SQL نجح فعلاً في النشر.

**الضوابط:** غياب التفاصيل أو firstDetail=null يرجع قبل هذا الفرع. تأكيد Insert بقيمة صالحة يملأ scalar ويعطي ضابطاً موجباً. property5 فرع serial آخر سبق 029؛ لا يمثل نموذج 2..4 إلغاء serial أو سلامته. النسخة InvoiceDGV في ItemOpercontract تحمل السبب نفسه **ضمن 151 لا finding ثانية**؛ LoadItemInfcontract المختلفة لا تستدعي الحوار في الجسم المقروء.

**الوصول والأثر:** مسار إضافة صنف مستوفٍ مفترض عبر ItemOper مستقل عن إظهار عمود الوصف. أما تعديل بند قائم بالنقر المزدوج في البيع فـDescription **Collapsed افتراضياً** ويحتاج عقد layout/SortMemberPath؛ وفي الإدخال/الإخراج يعيد GetFocusedColumnName نصاً فارغاً. لذلك لا ندعي أن كل مستخدم يستطيع بلوغ فرع التحرير أو أن كل بند قائم يفقد كميته. الإثبات عند تعيينات الكائن، لا كتابة قاعدة بيانات أو خسارة مالية.

**الفصل والمقترح غير المنفذ:** ليست premutation دفع 015 أو clear لقائمة serial029 أو تحديث عميل 091 أو projection import144 أو حذف current في picker148. المطلوب نتيجة PropertiesResult بحالة Accepted/Cancelled/Failed و LineRef وقياسات مستقلة؛ لا تطبيق قبل التأكيد وفق العقد، ولا تفسير عودة loader الطبيعية كتأكيد تفاصيل. المالك H7B25-03/05؛ **P7B25T-01/02** وخطط الضوابط ذات الصلة غير منفذة.

### P7-152 — حساب التعبئة يعيد إدخال ناتجه فيضرب الكمية مجدداً عند الاستدعاء المتتابع

**Medium؛confirmed مصدرية محلية؛open-not-remediated.**

**الدليل:** `SmartAuditERP/Form_WPF/frmItemProperties.xaml.cs:72-79;123-192;214-251;280-297`؛ `SmartAuditERP/Form_WPF/frmItemProperties.xaml:239-245;263-270`؛ `SmartAuditERP/Class/ItemOper.cs:637-654`.

**السلسلة:** في التعبئة 2 يقرأ Calc النص net الحالي، ويستخرج height من net/width عند الارتفاع الصحيح، أو ceil(net/width) عند شرط الارتفاع الكسري الموجود، ثم يحسب net=height×width×qty ويكتبه في **النص نفسه الذي سيقرأه الاستدعاء التالي**. لا يحتفظ هذا الفرع بكمية طلب أصلية منفصلة عن ناتجه.

**شاهد صحيح الأعداد، لا تقريب:** أدخل إلى الحد المحلي width10/height2/count3/netText20. النداء الأول يكتب height2/net60؛ النداء التالي دون تغيير طلب الأعمال أو width/count يقرأ 60 ويكتب height6/net180. تغير الارتفاع هنا ناتج مشتق من النداء السابق، لا طلب جديد من المستخدم. النسبة 3 جاءت من count المورّد، وليست تقدير خسارة أو مرجع كمية تجارية.

**الأحداث والحارس:** هناك استدعاءات فعلية في handlers تغير count وفقد تركيزه و Enter، وفي فقد تركيز/Enter النص net. XAML يوصلها. `_isInternalUpdate` يمنع النداء المتداخل أثناء الكتابة ويعاد false في finally؛ لا يجعل نداءين متتابعين مستقرين. **لم نشغّل WPF أو نثبت عدد/ترتيب الأحداث لنقرة أو دورة Loaded بعينها**؛ الشاهد يثبت ما تفعله التعليمات إذا وصل استدعاءان متتابعان بالحالة المحددة، لا جدول أحداث مرصوداً.

**الضوابط والحد:** count1 يبقي 20 في المثال؛ width0 أو count0 لهما guard يكتب height/net0، فلا نخترع divide-by-zero exception في الفرع المحروس. مساحة 3 تعيد الحساب منالأبعاد فتبقى 60، وصيغة 4 تبقى 72. هذه ضوابط اختلاف المعادلات لا شهادة أن«متر طولي» يجب أن يكون محيطاً تجارياً. شرط ceil عند height2.5/net21/width10/count2 يعطي 3/60 في المثال نفسه؛ يظل ضمن 152 لا finding ثالثة أو سياسة تقريب معتمدة. الشاهد يستخدم rational منتهياً وبسيطاً؛ ليس تنفيذ double/Math.Ceiling/FormatNumber0.### أو NumberStyles/ثقافات .NET.

**الفصل والمقترح غير المنفذ:** يظهر بأعداد صحيحة دون خصم أو VAT أو priceUnit أو RemoveAt؛ فلا يعيد عد float007 أو VAT003 أو unit-price026 أو stale-index150. وحتى عند تأكيد Insert وتطبيق النتيجة الصحيحة من حيث الحالة، يظل feedback الحساب مستقلاً عن 151. يفصل الطلب الأصلي عن الناتج، ويعلن عقد FillRatio/FillValue/height/width/count/net والوحدات وسياسة الكسر؛ بعدها يختبر استقرار الحساب مع تكرار callbacks. المالك H7B25-01/05؛ **P7B25T-03/04** وخطط الضوابط غير منفذة.

## 3. وصول المصدر لا يُستنتج من اسم helper

| الحد | الدليل المختار | القرار والحد |
|---|---|---|
| مصدر الخاصية/قيمة التعبئة | `SmartAuditERP/Class/ItemOper.cs:491-574;604-620`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:905-934;985-991`؛ `SmartAuditERP/Form_WPF/frmItems.xaml:487-512` | code2 تعبئة محلياً؛ FillValue→FillRatio→width. لا SQL أو وحدة أو قيمة نشر معتمدة؛positivewidth مدخل شاهد. |
| إلحاق ItemOper | `SmartAuditERP/Class/ItemOper.cs:1047-1056;1075-1091;1134-1188`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:667-705;1413-1445` | حمل ثم Add ثم caller calculation/binding. نجاح lookup والرجوع الطبيعي مفترضان؛ لا حكم نهائي عن كل stock/save. |
| محرر البيع القائم | `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:1068-1093;3689-3745`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml:650-663;882-888` | handler موصول لكن Description مخفي؛layout و SortMemberPath شرطان، لا وصول غير مشروط أو finding إضافية لغياب إظهار. |
| الإدخال/الإخراج | `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml.cs:1146-1195`؛ `SmartAuditERP/Form_WPF/frmInvInputOutput.xaml:722-739` | helper العمود يعيد الفارغ؛ لا نستدل من شرط Description في body على بلوغه فعلياً من هذا المدخل. |
| overload الفاتورة/العقد | `SmartAuditERP/Class/ItemOpercontract.cs:977-1005;1058-1083;1171-1192;1195-1329;1367-1417` | helper InvoiceDGV مظهر 151؛GetItemByIDcontract→LoadItemInfcontract لا يثبت حوار العقد. لا collection-runtime failure أو missing-feature معتمدة من الاسم. |

تفاصيل كل قدرة ومسؤوليتها ومدخلها وأثر الغياب والخطوة والخطتين في [FE16](evidence/feature-implementation-matrix-07B25.csv) و[INV16](evidence/report-invariants-07B25.csv) و[خطط 32](evidence/acceptance-tests-07B25.csv).14 قدرة مصدرية/ضابطية و 2 بوابة وثائقية ذات sentinel صريح؛ ليست 16 موافقة أعمال أو 16 عيباً.

## 4. منع التكرار والتوسع غير المثبت

| القرار | النتيجة |
|---|---|
|151 مقابل 015/029/091/144/148|فصل producer/result والهدف والتعليمة المسببة؛ لا يكفي التشابه اللفظي«إلغاء» لدمج كل عقود مختلفة، ولا تعاد count أسباب قديمة.|
|152 مقابل 007/003/026/150|حلقة output→input×count صحيحة الأعداد،ليست تقريباً أو VAT أو اختيار سعر أو فهرس بعد إزالة.|
|نسخة helper الثانية|نفس 151 ضمن المعرف نفسه، لا finding ثالثة ولا historicalextension.|
|Invoicecontract|ضابط حدود ولا support/missing-feature استنتج من اسم class. لا يُحسم collection lead بلا DTO/contract؛025 تبقىبحدودها.|
|المحررات القائمة|Hidden/empty-column قيود على الوصول؛ليستا قدرتين مفقودتين ثبت وجوبهما، ولا كل double-click مدقق.|
|serial/LineRef|029/013 محفوظتان؛sameItemId lead لم يتحول إلى finding جديدة أو تغيير أدلة تاريخية.|
|الحواجز|014/132/145 تظل potential؛020/021 والمال/ACL/stock/save/production والسياسات/SDK لم تعتمد.|
|عمق المقارنة|قرئت 322 خلاصة عنوان/يقين وصفيت metadata المسارات ثم قورنت الأجسام الأقرب المسماة؛ليست كل 322 متناًأو 455FE/477body أو كل أدلته يدوياً.|

[AD8](evidence/root-adjudication-07B25.csv) يحفظ القرار والسبب والعمق؛ [historical-extensions](evidence/historical-extensions-07B25.csv) **صفر صفوف**. لم تغيّر يقيناً أو خطورة أو جدولة أو حالة أو دليل أي أصل تاريخي.

## 5. الحفظ والتحقق والتاريخ

- [provenance703](evidence/provenance-07B25.json) يحمي 703 من 708 مواد دخول؛الخمس المشتركة فقط تتقدم:findings/README/PLAN/IMPROVEMENTS/dispatcher. [لقطة 322](evidence/findings-through-07B24.csv) و[فهارس B24](evidence/shared-indexes-through-07B24.json) و provenance ثلاث freezes مستقلة لا يعاد توليدها.
- السجل الحالي 324/raw325CRLF/noBOM يبدأ حرفياً ببايتات سجل 322/raw323CRLF؛G01–215 محفوظة حرفياً،وتضاف G216–219 توصيات لا findings إضافية.827 أصلاً/29,128,444 بايت لم تتغير.
- stdoutB24 المحمي 208993 بايت/SHA`5866e39e46d6075ca186059bdf8d860f2d66c3330ac400859ae334fb3d80c69b` يظل على capturef37c37c، لا دخول 45a2a50. المرجع 16 وساعة 19 والمصدر والتقاط stdout والتسليم هويات مستقلة؛الإيضاح إضافي فقط.
- أرشيف 30 الحقيقي 73506 بايت/SHA`42755c94a5b223159b93bcf38335366646cefd6fab777aaa7222f9e0066442d6` يحفظ مخرجات وأدوات وقت الالتقاط. وقت التقاطه سبق تثبيت SHA في helper وتصحيح دمج إحالات RC وإضافة ضابطها إلى الحالة 09. هذان الملفان الجديدان فقط اختلفا منذ التقاط 30؛ لا تعديل لأدوات B24 المحمية أو لسجل 30 ولا ادعاء final-wholesale replay.
- [الشاهد 16+16](evidence/property-dialog-witnesses-07B25.json)39311 بايت/SHA`1a47740eb84428c6bee3dadc1f34f08134b8996aa93b74254ea40f3cfd9d69a4` أعيد حسابه قراءة فقط. هو صور supplied states ونصوص لااختبارات ERP أوإطار .NET.
- CLI الحالي B25 منفصل عن descriptorsB16…B24 التاريخية وعن API main defaultB15 المحفوظ. لا protected edit/skip/filter/globalPath/sharedsubprocess mutation/diskoverlay/rebaseline/archive rewrite. حالات schema التاريخية الاصطناعية ليست دليل تنفيذ 30؛الأرشيف الحقيقي منفصل.

تصويب B10 الإضافي محفوظ:10 محلياً مقابل 120 مرجعياً؛equality1 كلاهما 10؛G138 المحمي لم يحرر. لا حسم للسياسات المالية/HR/عملة/SDK أوخسارة/ربح محفوظ من شاهدي 0 و 60→180.

## 6. ما بقي والتسليم إلى الإصلاح

[RS14](evidence/residual-disposition-07B25.csv) يحفظ كل upstreamID/artifact/rowSHA/contracts والمدخل السابق **كاملاً كبادئة** وكل route بعد mapping والتصرف دون تحويل إلى approved. [SP3](evidence/split-register-07B25.csv) يحفظ نسب كل split والمدخل السابق؛ليست 3 موافقات أو 3 جلسات. [H6](evidence/handoffs-07B25.csv)/[Q6](evidence/questions-07B25.csv) عقود وأسئلة غير محسومة، لا طلب أسرار أو بيانات أعمال.

تبقى SP01 بقية callers/dialogs/editors/writers/output/DocumentRef/allowed-set/branch/reset/dirty و cancel/failure،و SP02 حصر قدرات متفق عليه،و SP03 العملة/words/legacy/SDK/sign/zero/precision/templates وسياسة التعبئة. تراجع R4j/B26 أو split مسبب بمدخل ومصدر ومخرج واستبعاد وحد خروج؛ لا وعد مدة أو جلسات أو أن التالي الجزء الأخير.7C بمحاوره الستة لم تبدأ؛8 غير مأذونة هنا.

**المحادثة الموازية:** تُزوّد بـSHA تسليم التدقيق المدفوع،فتدمج تاريخ التدقيق في فرعها بحفظ تعديلاتها وتسجل آخر SHA راجعته وتربط finding→task/test. لا نفترض بدءها أو تزامنها، ولا نغلق findings من هنا أو نصنع ملفات إصلاح أو ندمج إصلاحاتها عكسياً.
