# المرحلة الخامسة — المزامنة والأوفلاين والفروع وAndroid وMQTT

**تاريخ مرجع التدقيق:** 2026-11-16 (UTC)  
**الفرع:** `arena/94ae8414-smartauditerp`  
**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`  
**الحالة:** مكتملة **كمراجعة ساكنة ضمن النطاق المعلن** بإذن المستخدم «ابدأ المرحلة 5». لا تعني قبولاً تشغيلياً، أو إصلاحاً، أو إذناً بالمرحلة6. تواريخ تقارير1–4 وchecks التاريخية محفوظة كما صدرت؛ ليست تواريخ إعادة تنفيذ للتطبيق.

## 1. الخلاصة التنفيذية

**نجاح الاتصال أو Publish أو انتهاء Task/ظهور اللون الأخضر ليس إثباتاً لاعتماد بيانات الطرف الآخر.** مصدر الخلل المتكرر هنا هو عدم ثبات عقد الهوية والرسالة والنتيجة بين الكاتب والطابور والمستقبل: صنف يكتب `itemid` ويقرأ `id`، إعادة إرسال تغير موضوع المستند، ACK بعيد بعد كاتب محلي لا يعيد commit outcome، ولقطة/منح/حذف لا تتقارب دائماً عند الإعادة أو الغياب. لا تثبت هذه القراءة وقوع فقد أو تلف أو استغلال فعلي في منشأة.

| النطاق | النتائج | حرجة | عالية | متوسطة | منخفضة |
|---|---:|---:|---:|---:|---:|
| المراحل1–4 تاريخياً |106|2|69|34|1|
| المرحلة5 — جديدة فقط |31|0|22|9|0|
| **التراكمي المفتوح** |**137**|**2**|**91**|**43**|**1**|

- الجديدة **27 مؤكدة من المصدر و4 محتملة**: `P5-004/005` لانقطاع/تزامن ملفات أو تبديل سياق الطابور، و`P5-026` لأن تنظيف SDK خارجي التنفيذ، و`P5-028` لتداخل المهام المشروط بالتوقيت. التراكمي **114 confirmed /18 potential /5 repository-gap**؛ كل نتيجة `open-not-remediated`.
- النطاق5 **54 مساراً**:24 سبق دخولها الاتحاد160 و30 جديدة؛ الاتحاد حتى5 **190 مساراً فريداً** من827 محصورة. هذه **مقاطع قراءة/metadata محددة، لا قراءة كاملة لهذه الملفات أو تغطية تشغيلية أو نسبة اكتمال للنظام**.
- المخرجات: **18 تدفقاً فعلياً/حدياً، 12 مجموعة ملكية بيانات، 25 صف عقد مواضيع MQTT، 36 صف فشل/تكرار/تأخر/تعارض، 24 ثابتاً، 64 خطة قبول غير منفذة**. الصفوف ليست نتائج إضافية أو tests ناجحة.
- أعيد حساب **12 توضيحاً مستقلاً منقولاً يدوياً و5 فحوص معجمية مصدرية منفصلة** بأداة تدقيق Python فقط؛ **صفر build/ERP/C#/WPF/SQL/broker/API/provider tests**، ولا تحميل DLL أو تشغيل سيرفر/مزود أو اتصال إنتاج أو معالجة بيانات.
- **106 نتيجة سابقة لم تغلق أو يعاد تصنيف نواتها**. وسعت أدلة8 فقط وحفظت لقطة106 و38 بصمة artifact تاريخياً؛ إزالة5 من `next_phase` بعد المراجعة لا تعني العلاج.

### أولوية القرارات المقترحة

1. **حد الاعتماد والإقرار:** `P5-006/012/015/016/026/027` مع `P3-003/006`؛ لا تمسح مصدر replay أو ترفع Sync أو تحذف بيانات Android المساعدة قبل إثبات commit/نسخة. `P5-026` مشروطة بعقد SDK ولا تسوغ ادعاء فقد دائم أو تشغيل clear للتجربة.
2. **عقد الطابور والهوية/الموضوع:** `P5-003/004/005/007/010/011`؛ سجل durable بالهوية/السياق/الإصدار وclaim/ACK، لا إعادة نسب سجل إلى جلسة حالية أو الاعتماد على رقم العرض/StartsWith.
3. **التقارب بعد غياب/سحب/حذف:** `P5-009/013/018/019/020/021/023/024/025`؛ snapshot وdelta وempty وtombstone وcursor والوحدة/الموقع عقود مستقلة، لا upsert واحداً لكل معنى.
4. **ملكية الاتصال والمهام والحالة:** `P5-001/002/008/017/028/029/030/031`؛ اتصال واحد وسياق جيل ثابت وTask منتظرة وجدولة صحيحة ومؤشر قبول منفصل عن الاتصال.

هذه توصيات تحتاج قرار معالجة واختبار معزول لاحقاً؛ **لا تعطيل إنتاج أو حذف queue أو إعادة إرسال مالي/ضريبي أو تعديل أرصدة نفذ هنا**. ضوابط TLS/auth/الأسرار وSQL interpolation الأصلية باقية تحت معرفاتها القديمة، لا يعاد احتسابها في5.

## 2. ما راجعته وحدود ما يمكن إثباته

### 2.1 القنوات والوصول

- تتبع `Home` عند التشغيل والمؤقت والنقر والخلفية، وlogin/settings، إلى HTTP غير cloud وcloud ثم الكتاب المحلي ومواضع ACK/cleanup/status. فُصل API النشط عن بوابات MQTT المبنية على `new Home()`؛ الأصل لتلك البوابات `P1-017`.
- قرئت ملفات MQTT writer/replay/subscribe/parser وبعض كتاب الصنف والعضوية والصلاحية والمستند/الأطفال/السيريال. الملف قد يضم آلاف الأسطر؛ النطاق [review-scope-05.csv](review-scope-05.csv) يحدد المقاطع فقط، لا اعتماد كل serializer أو receiver.
- قورنت النماذج المحلية `ItemIdOff/ListItems` وهويات invoice/entry/child مع الكاتب/القارئ، ومواضيع immediate/bulk/offline وcase وretain. **MQTT `x/#` قد يطابق `x` العاري**؛ فشل bare Inv هنا من `Split('/')[1]`، أما Entry/entry فاختلاف حروف/أسماء فعلي.
- تتبعت شاشات المتابعة والرفع/التنزيل العامة والمخزون من Home وربط XAML. `FrmSyncMQtt` قابل للفتح لكن ناشريه خلف بوابة Home المنفصلة. لم يثبت caller لـ`FrmSyncInv` أو`FrmSyncSettings` أو`GetCustFromAndroid.StartConnection` أو`frmInvSale.AddInvLocally` بالبحث المقروء؛ لا تعد مسارات حية لمجرد وجود جسم دالة.
- تتبعت Android من **ReadDataPeriodically** الفعلي (نوع20/10 وفق شروط المصدر)، لا من SignalR helper غير المثبت. راجعت توليد وربط GL وتأكيد received وحذف العميل المساعد، لا بروتوكول جهاز Android أو مزود الفوترة قانونياً.
- راجعت تنزيل التعريفات والموظفين والعضويات والـcursor، وProductStocks/الإجراء المرفق/الناشر ووحدة اللقطة. cache/تكلفة snapshot وحقول DTO غير المتاحة بقيت أسئلة محددة H5/Q5، لا أحكام غياب شاملة.

### 2.2 ضوابط إيجابية وحدود لازمة

1. توجد معاملات محلية فعلاً في `ReadInvoiceOnline/ReadEntyOnline/ReadReceiptOnline`؛ علة ACK هي عدم نقل نتيجتها إلى caller أو return مبكر/فشل مبتلع، **ليست «كل الاستيراد بلا transaction»**. بعض rollback/post-commit errors قد يهرب ويمنع ACK، فلا نعمم أن كل فشل يؤكد.
2. `ReadDataPeriodically` يفحص ClientCode وDistBranch في الفروع المقروءة؛ ضعف StartsWith يخص MQTT. لا يثبت هذا عزل الخادم كله ولا ينفي الضابط الموجود.
3. `ClosingReport` يجمع استبدال الرأس والأطفال في transaction مع rollback/rethrow؛ مثال إيجابي مقابل MQTT المنفصل، **لا إصلاحاً تلقائياً لـP3-014** أو workaround تشغيلياً معتمداً.
4. يوجد guard بعد فشل SaveInvoice في POS قبل تحديث الكمية؛ **لا نزعم خصم cache بعد save=false**. إن وصل DTO المتوقع فدلالة كامل الكمية/فرق التعديل/نسخة snapshot سؤال H5-03، لا أثر محسوم من alias خارجي.
5. مقارنة أسماء معاملات SQL للاستيراد online لا تظهر نقص أسماء InsertInv/UpdateInv/InsertInvSub في المقاطع المقروءة؛ `P4-020` خاص بحفظ الإنتاج. وجود كل الأسماء لا يثبت الأنواع/القيم أو نجاح SQL.
6. `SaveInvoice(null)` يعتمد صراحة خلاف `SaveReceipt(null Entry)` في `P3-004`؛ لا تنقل النتيجة بينهما. معاملات/Pks لا تضمن منع downgrade أو تكرار side effect، والعكس لا يسمح بنفي كل ضابط خادم.
7. `AuditorAPI.Models` و`Ws_Auditor` و`AESencDEC` وتهيئة broker والخادم ومخطط SQL المنشور غير متاحة للفحص هنا. **لا تخمين Equals/setters/enums/Items↔InvoiceItems أو cipher/MAC أو CLearfiles durability/idempotency**. النص المورد ليس schema نشر.
8. لا أرقام خسائر فعلية أو exploits أو قياس مرور/تزامن/استعادة؛ ثبات السلوك المصدر لا يجعل كل أثر شرطي قد حدث. تفاصيل مزودي ZATCA/ETA/الدفع/المتاجر في6، وشمول الميزات/الواجهة7، والتشغيل8 بإذن مستقل.

### 2.3 ملفات التسليم

| المخرج | المحتوى |
|---|---|
| [SYNC-OFFLINE-05.md](SYNC-OFFLINE-05.md) | نموذج القنوات/ACK والتقارب، ملخص التدفقات والملكية والمواضيع والثوابت والفشل وأسئلة Q5/متابعات H5. |
| [sync-flows-05.csv](evidence/sync-flows-05.csv) | 18 تدفقاً مع entrypoint/caller والوصول والهوية وموضع commit/ACK وحدود replay. |
| [sync-data-ownership-05.csv](evidence/sync-data-ownership-05.csv) | 12 مجموعة كيان: الكتاب الظاهرون، السلطة المجهولة، الهوية والتعارض/الحذف/السحب. |
| [mqtt-topic-contracts-05.csv](evidence/mqtt-topic-contracts-05.csv) | 25 صف عقد publisher/subscriber/flag/dispatch/payload/QoS/retain، لا25 ثغرة. |
| [sync-failure-conflict-05.csv](evidence/sync-failure-conflict-05.csv) | 36 صفاً لفشل/تكرار/تأخر/تبديل/حذف، مع ضوابط وحدود ونتيجة مطلوبة. |
| [sync-invariants-05.csv](evidence/sync-invariants-05.csv) | 24 ثابتاً مرتبطاً بالنتائج والخطط؛ ليس اجتيازاً. |
| [VALIDATION-05.md](VALIDATION-05.md) و[acceptance-tests-05.csv](evidence/acceptance-tests-05.csv) | 64 خطة بمتطلبات وإجراء وقبول وأمان ومراجع؛ كلها not-executed. |
| [sync-witnesses-05.json](evidence/sync-witnesses-05.json) | 12 توضيح حالة/نص/ساعة يدوياً و5 فحوص معجمية منفصلة؛ لا تشغيل ERP أو مكتباته. |
| [checks-05.json](evidence/checks-05.json) | فحص اتساق الوثائق/البصمات/الروابط/النطاقات/المعرفات؛ لا شهادة تسليم أو صحة مالية. |
| [provenance-05.json](evidence/provenance-05.json) و[findings-through-04.csv](evidence/findings-through-04.csv) | 38 artifact تاريخياً ولقطة106 قبل5 دون استبدال checks-02/03/04 أو baseline. |
| [findings.csv](findings.csv) و[IMPROVEMENTS.md](IMPROVEMENTS.md) | 137 نتيجة مفتوحة؛ G-01 إلىG-50 تجميعات مقترحة لا50 finding إضافياً. |

## 3. النتائج الجديدة بالتفصيل

الخطورة ترتيب نوعي مشروط بالأثر، لا قياس خسارة أو CVSS. `confirmed` يثبت التعبير/الإغفال المصدر المحدد؛ حدود الأثر بكل نتيجة لازمة. `potential` يبقي شرط التزامن/النشر/المكتبة واضحاً. كل P5T **خطة غير منفذة**؛ ALG5/ST5 توضيح/اتساق مستقلان عن التطبيق. لا إصلاح أو إغلاق من كتابة التقرير.

### P5-001 — فحص اتصال MQTT يستبدل العميل والهوية بدلاً من إعادة استعمال جلسة الاستقبال — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ConnectBroker.cs:41-68`؛ `SmartAuditERP/Class/ConnectBroker.cs:90-119`؛ `SmartAuditERP/Class/ReceivedData.cs:29-113`؛ `SmartAuditERP/Home.xaml.cs:737-744`؛ `SmartAuditERP/Class/SendData.cs:738-779`.
- **الملاحظة ومسار السبب:** IsConnectedToBroker ينشئ MqttClient جديداً ويولّد GUID في كل فحص؛ CheckConnectionAndBroker يستدعيه دائماً عند نجاح Ping. LoadReceived يفحص مرة أخرى ثم يربط subscriptions/handlers بالعميل الحالي؛ نشر الطابور يعيد الفحص لكل جزء ويستبدل المرجع static من جديد.
- **الأثر والشروط:** عميل الإرسال اللاحق ليس بالضرورة العميل الذي رُبط به الاستقبال. العميل السابق لا يفصل/يتخلص منه هذا المسار، وإزالة handler من الكائن الجديد لا تزيله من القديم؛ تصبح ملكية الاشتراكات والاتصالات وإعادة retained غير منضبطة، وقد تتراكم جلسات أو تستمر معالجة قديمة.
- **حد الإثبات والضوابط المقابلة:** المثبت هو إنشاء واستبدال المرجع وعدم نقل/إيقاف الاشتراكات في المسار؛ مدة بقاء اتصال قديم وعدد sockets الفعلي وضمان clean-session في نسخة M2Mqtt الخارجية غير مقاسة. ليس هذا إعادة عد TLS/auth في P1-014 ولا ادعاء تسرب ذاكرة قيس تشغيلياً.
- **المقترح:** خدمة MQTT واحدة لكل سياق ثابت، بهوية عميل مستقرة وسياسة جلسة معلنة؛ connect/reconnect/rebind/dispose تحت قفل واحد، مع إبطال callbacks القديمة عند تغير السياق وتسجيل جيل الاتصال.
- **القبول غير المنفذ:** `P5T-01`، `P5T-02`، `P5T-03`؛ **الثوابت المطلوبة:** `INV5-01`، `INV5-02`.

### P5-002 — الوصول إلى وسيط MQTT مشروط بنجاح ICMP إلى عنوان إنترنت خارجي — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ConnectBroker.cs:70-119`؛ `SmartAuditERP/Class/SendData.cs:694-704`.
- **الملاحظة ومسار السبب:** IsConnectedToInternet يستخدم Ping إلى 8.8.8.8؛ CheckConnectionAndBroker لا يحاول الاتصال بالوسيط إذا فشل Ping، وSendStoredItems يرجع قبل محاولة إرسال الطابور.
- **الأثر والشروط:** فرع بشبكة داخلية سليمة أو وسيط محلي مع حجب ICMP/الإنترنت يمكن أن يُعامل كمنقطع، رغم أن TCP إلى الوسيط متاح. هذا يناقض تشغيل LAN دون إنترنت ولا يميز DNS/مسار broker عن صحة عنوان خارجي.
- **حد الإثبات والضوابط المقابلة:** لم يرسل Ping أو يفتح broker هنا. النتيجة تخص gate ظاهر في العميل؛ لا نقرر سياسة الشبكة الفعلية أو ضرورة الإنترنت في كل تثبيت.
- **المقترح:** فحص endpoint الفعلي ومحاولة اتصال محدودة المهلة؛ فصل حالة WAN عن LAN وعن broker وعن اعتماد الرسائل، وعدم جعل ICMP الخارجي شرطاً لبروتوكول محلي.
- **القبول غير المنفذ:** `P5T-04`؛ **الثوابت المطلوبة:** `INV5-02`.

### P5-003 — طابور الأصناف يكتب itemid ثم يقرأ id من نموذج مختلف — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ItemIdOff.cs:1-8`؛ `SmartAuditERP/Class/ListItems.cs:6-10`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:2134-2155`؛ `SmartAuditERP/Class/SendData.cs:706-725`؛ `SmartAuditERP/Class/SendData.cs:676-691`.
- **الملاحظة ومسار السبب:** كاتب Itemid.json يسلسل ItemIdOff.itemid؛ القارئ يفك الملف إلى List<ListItems> ويأخذ item.id، وهو اسم آخر لا اختلاف حالة أحرف فقط. يرسل بعده استعلامات where id/Itemid بهذه القيمة ثم يفرغ الملف.
- **الأثر والشروط:** مع العقد الافتراضي الظاهر لا تنتقل قيمة itemid إلى id؛ يبقى int عند القيمة الافتراضية صفر بدلاً من هوية الصنف المطلوب. يمكن إرسال مجموعة فارغة أو بيانات id=0، ثم تختفي إشارة الصنف الأصلية من الطابور.
- **حد الإثبات والضوابط المقابلة:** لم يشغّل Newtonsoft أو الصنف/الطابور. لا تحويل أو JsonProperty مخصص لهذين النموذجين في المصدر المقروء أو نتيجة البحث؛ نسخة serializer خارجية. وصول بعض كتاب MQTT محكوم أيضاً بحالة Home الجديدة P1-017؛ هذا لا يصحح عقد الملف إذا وصل إليه سجل.
- **المقترح:** DTO طابور واحد بإصدار schema والتحقق من id موجب ومطابقة الكاتب والقارئ، وترحيل/عزل الملفات القديمة غير المطابقة دون تصفيرها؛ حذف سجل بعينه فقط بعد اعتماد.
- **القبول غير المنفذ:** `P5T-05`، `P5T-06`؛ **الثوابت المطلوبة:** `INV5-03`، `INV5-04`.

### P5-004 — طابور MQTT يكتب بإعادة كتابة ملف كامل خارج معاملة المستند ودون تنسيق ظاهر — عالية / محتملة مشروطة

- **الدليل:** `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1123-1143`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:2142-2155`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1355-1399`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:2713-2732`؛ `SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:1064-1088`؛ `SmartAuditERP/Class/SendData.cs:706-778`.
- **الملاحظة ومسار السبب:** الكتّاب يقرأون JSON كاملاً ثم list.Add ثم File.WriteAllText؛ المرسل يقرأه ثم يصفّره. لا outbox SQL في معاملة الحفظ أو lock/استبدال ذري/claim لسجل في هذه المسارات؛ enqueue يأتي بعد حفظ المستند وفي فروع اتصال محددة.
- **الأثر والشروط:** إذا انقطع التشغيل بين commit وenqueue أو تقاطعت عمليتان/نسختان في المجلد نفسه، قد لا تبقى نية إرسال أو تضيع إضافة عند آخر كتابة/clear؛ ملف مبتور يمنع replay. نجاح SQL لا يثبت بقاء الرسالة والعكس.
- **حد الإثبات والضوابط المقابلة:** خطر مشروط بانقطاع/تزامن أو فشل قرص، لا ضياع شوهد. لا نعمم على طوابير AuditorAPI الخارجية غير المتاحة. بوابات Home في P1-017 قد تمنع الوصول لبعض كتاب الفواتير أصلاً؛ خطة القبول يجب أن تثبت الفرع أولاً.
- **المقترح:** Transactional outbox مع المستند بمفتاح operation/version وسجلات lease/retry؛ إن بقي ملف فليكن journal/replace ذرياً مع قفل بين العمليات وfsync/استعادة موثقة، لا read-modify-clear جماعياً.
- **القبول غير المنفذ:** `P5T-07`، `P5T-08`، `P5T-09`؛ **الثوابت المطلوبة:** `INV5-04`، `INV5-05`.

### P5-005 — ملفا طابور MQTT لا يحملان سياق قاعدة البيانات أو العميل أو الوجهة — عالية / محتملة مشروطة

- **الدليل:** `SmartAuditERP/Form_WPF/frmItems.xaml.cs:2142-2155`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:2713-2732`؛ `SmartAuditERP/Class/InvGLobalIDOff.cs:1-12`؛ `SmartAuditERP/Class/SendData.cs:704-779`؛ `SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs:1027-1038`.
- **الملاحظة ومسار السبب:** Itemid.json وInvGlobalID.json ثابتان تحت Data في مجلد التطبيق؛ نموذج الصنف هو رقم فقط، ونموذج الفاتورة هويات فقط. replay يعيد جلب البيانات باستعمال connString وClientCode الحاليين دون ربط سجل الطابور بسياق إنشائه أو بصمة الوجهة.
- **الأثر والشروط:** عند استخدام تثبيت واحد لأكثر من قاعدة/عميل، أو نقل Data أو تغيير الإعداد قبل تفريغ backlog، قد يقرأ رقم الصنف من القاعدة الجديدة وينشره باسمها ثم يمحو backlog الأصلي. هو خطر namespace مستديم، لا مجرد DTO سحابي عالق في الجلسة.
- **حد الإثبات والضوابط المقابلة:** احتمال مشروط بهذا النشر/التبديل وبوجود سجل قابل للقراءة؛ لا إثبات تسرب بين مستأجرين فعليين أو غياب عزل broker/server. ترقيم الفاتورة قد يخفف بعض التصادمات لكنه لا يضيف سياقاً للصنف أو يمنع clear الخاطئ. P2-003 يبقى الأصل لتبديل الجلسة.
- **المقترح:** تثبيت TenantId/DatabaseInstanceId/OriginBranch/Destination/ProtocolVersion في partition ورسالة موقعة السياق، ورفض replay عند عدم المطابقة مع quarantine ومراجعة لا إعادة نسبه تلقائياً.
- **القبول غير المنفذ:** `P5T-10`، `P5T-11`؛ **الثوابت المطلوبة:** `INV5-06`.

### P5-006 — تفريغ طابور MQTT لا ينتظر اعتماد المستقبل وقد يحدث بعد تخطي النشر — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/SendData.cs:706-779`؛ `SmartAuditERP/Class/SendData.cs:1803-1838`؛ `SmartAuditERP/Class/ReceivedData.cs:1250-1311`؛ `SmartAuditERP/Home.xaml.cs:614-622`.
- **الملاحظة ومسار السبب:** بعد القراءة يدعو SendStoredItems Publish ثم File.WriteAllText(empty) دون ACK تطبيقي. في حلقات المستندات يمكن أن تعيد CheckConnectionAndBroker=false فيتخطى النشر ويصل إلى clear. SendItemDataByid وSendDataa لا يعيدان نتيجة اعتماد، وSendDataa يبتلع فشل الاتصال/النشر.
- **الأثر والشروط:** فشل SQL عند المستقبل أو انقطاعه أو تخطي الفحص لا يمنع إسقاط نية replay المحلية. QoS0 في replay، وحتى QoS1 في SendDataa، لا يثبتان commit قاعدة المستقبل؛ يصبح البيان المحلي غير كافٍ لإعادة محددة أو لمطابقة ما اعتمد.
- **حد الإثبات والضوابط المقابلة:** التحكم/الترتيب في العميل مؤكد؛ لم يثبت فقد منشور أو تنفيذ ACK خارجي غير مرئي. Get* قد يرمي/يعيد null فيوقف بعض الفروع قبل clear؛ لا نقول إن كل استثناء يفرغ الملف. المخاطر التي تعبر دون استثناء أو بفحص false هي المحددة هنا.
- **المقترح:** فصل Pending/TransportAccepted/Applied/Rejected/Unknown؛ إثبات تطبيق بمفتاح الرسالة/الإصدار وبصمة aggregate، وعدم حذف إلا سجل ACK مطابق؛ إعادة المحاولة مع inbox idempotency ومطابقة حالة unknown.
- **القبول غير المنفذ:** `P5T-12`، `P5T-13`، `P5T-14`؛ **الثوابت المطلوبة:** `INV5-04`، `INV5-07`.

### P5-007 — إعادة إرسال المستندات لا تطابق شكل المواضيع وحالة أحرف مستقبلها — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/SendData.cs:738-776`؛ `SmartAuditERP/Class/SendData.cs:1823-1826`؛ `SmartAuditERP/Class/ReceivedData.cs:79-90`؛ `SmartAuditERP/Class/ReceivedData.cs:147-169`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatus.xaml.cs:988-1004`؛ `SmartAuditERP/Form_WPF/frmReceiptsSyncStatus.xaml.cs:645-655`.
- **الملاحظة ومسار السبب:** الإرسال الموحد ينتج Inv/id وentry/id وentryDetails/id. replay والإرسال الجماعي الآخر ينشر Inv/InvSub بلا slash، وEntry وEntryGlobalID أو EntrySub بحروف/أسماء مختلفة. مستقبل العمليات يقرأ Split(/)[1] دون فحص العدد، ويتفرع إلى entry وentryDetails بحروف صغيرة.
- **الأثر والشروط:** قد تصل رسالة Inv العارية عبر Inv/# ثم تفشل قبل dispatch عند قراءة المقطع الثاني؛ Entry الكبير لا يطابق entry/# أصلاً. لذلك الإرسال الفوري وإعادة الإرسال ليسا عقداً واحداً، وقد لا يطبق backlog رغم نجاح Publish.
- **حد الإثبات والضوابط المقابلة:** قاعدة MQTT مهمة: x/# يمكن أن يطابق x العاري؛ العلة في bare Inv هي parser، لا ادعاء عدم اشتراكه. غياب النقل الآمن P1-014 مستقل. بعض manual publishers خلف P1-017؛ SendStoredItems له caller مؤقت مثبت.
- **المقترح:** سجل مواضيع typed واحد للناشر والمشترك والمحلل مع version/tenant/entity/id؛ تحقق shape/case قبل decrypt/dispatch، واختبارات عقد لكل قناة فورية وجماعية وأوفلاين.
- **القبول غير المنفذ:** `P5T-15`، `P5T-16`، `P5T-17`؛ **الثوابت المطلوبة:** `INV5-03`، `INV5-08`.

### P5-008 — أعلام الاشتراك لا تتوافق مع معالجات العملاء والحسابات والمخازن والعروض — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ReceivedData.cs:51-113`؛ `SmartAuditERP/Class/ReceivedData.cs:158-259`؛ `SmartAuditERP/Class/ReceivedData.cs:263-341`؛ `SmartAuditERP/Class/ReceivedData.cs:350-395`؛ `SmartAuditERP/Form_WPF/FrmSyncMQtt.xaml.cs:70-138`.
- **الملاحظة ومسار السبب:** _syncOper يشترك Customers/AccountCust/AccountIndex لكن معالجه لا يحوي هذه الحالات ويفرض slash. Customers تعالجه Items فقط، والحسابات يعالجها definitions فقط، بشرط تحميل معالجاتهما بأعلام أخرى. تعريفات الاشتراك لا تحتوي Safe/Offer/OfferClient/OfferItem رغم وجود handlers وناشرين.
- **الأثر والشروط:** اختيار مزامنة العمليات وحدها لا يكفي لتطبيق بعض بياناتها، وتفعيل definitions لا يشترك في المخازن/العروض المذكورة. جمع الأعلام قد يخفي جزءاً من الخلل لأن الحدث يستدعي أكثر من handler؛ واجهة الاختيار لا تصف هذا الاعتماد المتبادل.
- **حد الإثبات والضوابط المقابلة:** لا ننفي أن اشتراكاً خارجياً أو عميلاً آخر يعالجها؛ الحكم على LoadReceived الظاهر. ناشر FrmSyncMQtt محكوم بـHome جديدة، فلا نستنتج أن العروض نقلت فعلاً. الباقي تعارض بنيوي بين قوائم العميل ومعالجاته.
- **المقترح:** اشتقاق subscribe/dispatch/publish من وصف عقد واحد، وتقسيم الأعلام بحسب كيانات صريحة لا أثر عرضي لمعالج آخر؛ حصر unsubscribe وتحديث الأعلام في دورة حياة واحدة.
- **القبول غير المنفذ:** `P5T-18`، `P5T-19`؛ **الثوابت المطلوبة:** `INV5-08`.

### P5-009 — تحديثات أصناف منفردة تتشارك موضوعاً retained واحداً بدلاً من سجل تغييرات — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/SendData.cs:676-691`؛ `SmartAuditERP/Form_WPF/frmItems.xaml.cs:1138-1165`؛ `SmartAuditERP/Class/ReceivedData.cs:67-77`؛ `SmartAuditERP/Class/ReceivedData.cs:405-450`.
- **الملاحظة ومسار السبب:** النشر لصنف واحد يستخدم ClientCode+Items والمواضيع النوعية المقابلة مع retain=true، مثل النشر الشامل نفسه؛ لا ItemId في اسم الموضوع ولا sequence/cursor في الحمولة المحلية المعروضة.
- **الأثر والشروط:** وفق دلالة retained، آخر دلتا للصنف B تستبدل دلتا A المخزنة في الموضوع نفسه. مستقبل غائب أثناء التحديثين يتلقى آخر payload لا backlog كامل أو snapshot متسق؛ إعادة الاشتراك ليست catch-up لكل الأصناف.
- **حد الإثبات والضوابط المقابلة:** ليس retain خطأ بحد ذاته ولا نزعم أن broker فقد رسالة نشطة؛ الأثر يخص غياب المستقبل وعدم وجود resnapshot خارجي موثق. امتلاء القائمة الشامل من قناة أخرى قد يعوضه، لكنه ليس ضمان هذا البروتوكول. QoS لا يحول retained إلى event log. بوابات بعض ناشري الأصناف تنشئ Home منفصلة (P1-017)؛ هنا علة عقد retain حال الوصول إلى النشر، لا ادعاء أن دلتا A وB نشرتا فعلاً في النسخة.
- **المقترح:** إما snapshot كاملة مؤطرة بنسخة وحد اكتمال، أو موضوع حالة لكل كيان بمفتاحه مع tombstone/صلاحية، أو سجل تغييرات دائم وcursor؛ reconciliation يثبت عدد/بصمات الكيانات بعد الغياب.
- **القبول غير المنفذ:** `P5T-20`، `P5T-21`؛ **الثوابت المطلوبة:** `INV5-09`.

### P5-010 — إزالة passcode من كل النص المفكوك تغير قيم JSON لا بادئة الغلاف فقط — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ReceivedData.cs:147-164`؛ `SmartAuditERP/Class/ReceivedData.cs:263-273`؛ `SmartAuditERP/Class/ReceivedData.cs:350-357`؛ `SmartAuditERP/Class/SendData.cs:559-561`.
- **الملاحظة ومسار السبب:** الناشر يلصق passcode قبل JSON ثم يشفره؛ المعالجات الثلاثة تستدعي DecryptString(...).Replace(passcode, empty) على كل النص، دون حصر البادئة أو التحقق من طولها/مطابقتها.
- **الأثر والشروط:** إذا احتوى اسم أو ملاحظة أو باركود أو معرف على تسلسل passcode يحذف من القيمة أيضاً؛ قد يتغير الاسم/المفتاح مع بقاء JSON صالحاً أو يفسد JSON. passcode الفارغ يثير عقداً آخر ينبغي رفضه قبل المعالجة، لا اعتباره غلافاً صالحاً.
- **حد الإثبات والضوابط المقابلة:** المثال في التحقق يستخدم قيمة اصطناعية ولا يكشف أي سر. لم يفحص تنفيذ AESencDEC الخارجي؛ لا حكم على نمط التشفير أو سلامة MAC من اسم الصنف، ولا تشغيل decrypt فعلي.
- **المقترح:** غلاف typed بإصدار وحقول مستقلة وpayload length/hash وسياق موثّق؛ إذا بقي prefix قديم فإزالة بادئة واحدة بعد مطابقة صريحة ثم ترحيل، لا Replace عالمي.
- **القبول غير المنفذ:** `P5T-22`، `P5T-23`؛ **الثوابت المطلوبة:** `INV5-10`.

### P5-011 — تمييز الفرع المرسل بواسطة StartsWith لا يطابق صيغة المعرف العالمي — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ReceivedData.cs:1169-1176`؛ `SmartAuditERP/Class/ReceivedData.cs:1257-1270`؛ `SmartAuditERP/Class/ReceivedData.cs:1313-1328`؛ `SmartAuditERP/Class/ReceivedData.cs:1351-1368`؛ `SmartAuditERP/Class/ReceivedData.cs:1549-1558`؛ `SmartAuditERP/Class/InvoiceOper.cs:2872-2901`؛ `SmartAuditERP/Class/EntryOper.cs:1271-1301`.
- **الملاحظة ومسار السبب:** المستقبل يتجاهل GlobalID إذا بدأ برقم الفرع المحلي نصياً. التوليد عند ActiveSync هو ClientCode-Branch-No، ودونه Branch-No؛ لا delimiter أو parsing أو مقارنة بحقل Branch المرسل في هذا الحارس.
- **الأثر والشروط:** الفرع1 قد يهمل معرف10-8 أو tenant يبدأ1 رغم أن مصدره فرع آخر، بينما معرف tenant-1-8 لا يبدأ1 فيُعاد تطبيق بيانات الفرع نفسه. هذا ليس حارس عزل/echo موثوقاً ويجعل النتيجة تعتمد أرقام المستأجرين والفروع.
- **حد الإثبات والضوابط المقابلة:** المثبت اختلاف العقد والتصادم النصي، لا تسرب أو كتابة غير مخولة وقع فعلاً. APIs الدورية تحتوي فحص ClientCode وDistBranch صحيحاً في المصدر؛ لا نعمم علة MQTT عليها. MAX+1 يبقى P3-005 دون عد جديد.
- **المقترح:** غلاف OriginTenant/OriginBranch/Device/OperationId موثوق مع parser صارم لهوية معلومة الإصدار؛ مقارنة هويات typed، لا بادئة حرة، مع مسار صريح للهويات السابقة والهجرة.
- **القبول غير المنفذ:** `P5T-24`، `P5T-25`؛ **الثوابت المطلوبة:** `INV5-06`، `INV5-11`.

### P5-012 — استقبال تفاصيل MQTT يستبدلها بكتابات مستقلة ولا يعرّف تفريغ مجموعة فارغة — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/SendData.cs:738-776`؛ `SmartAuditERP/Class/ReceivedData.cs:169-221`؛ `SmartAuditERP/Class/ReceivedData.cs:1250-1311`؛ `SmartAuditERP/Class/ReceivedData.cs:1313-1350`؛ `SmartAuditERP/Class/ReceivedData.cs:1542-1608`.
- **الملاحظة ومسار السبب:** الرأس والبنود وGL مواضيع منفصلة. InsertInvSub وInsertEntrySub يحذفان أولاً في loop ثم يدرجان في loop آخر دون transaction؛ المفتاح يستنتج من كل طفل، لا envelope للأب. قائمة فارغة لا تنفذ أي حذف. السند الموجود يحذف ثم يعاد إدراجه خارج معاملة مشتركة.
- **الأثر والشروط:** بين الرأس/السطور/GL أو بعد فشل إدراج لاحق يمكن بقاء aggregate هجين/جزئي أو سند محذوف، مع catch صامتة. رسالة تفاصيل empty لا تستطيع إزالة آخر سطر للأب؛ وصول تفاصيل قديمة بعد الرأس الأحدث لا يرتبط بإصدار aggregate.
- **حد الإثبات والضوابط المقابلة:** هذا حد استقبال MQTT محلي مستقل عن معاملات ReadInvoiceOnline/ReadEntyOnline الموجودة وعن استقلال مستند/GL في P3-003. لا دليل أن كل رسالة مكررة تضاعف السطور: الحذف الكامل قد يجعل إعادة كاملة متسلسلة تبدو idempotent؛ فشل/ترتيب/empty هي الفجوات. version/history يمتد تحت P3-006.
- **المقترح:** Inbox ورسالة aggregate أو staging برقم إصدار وmanifest/count/hash، واعتماد الرأس/الطفل/روابطه دفعة واحدة بعد اكتمالها؛ parent id حتى مع empty، وقرار رفض قديم/تعارض/عكس محفوظ.
- **القبول غير المنفذ:** `P5T-26`، `P5T-27`، `P5T-28`، `P5T-29`؛ **الثوابت المطلوبة:** `INV5-07`، `INV5-12`، `INV5-13`.

### P5-013 — كل صف صلاحية تشغيل وارد يلغي الصفوف السابقة للموظف نفسه — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ReceivedData.cs:301-304`؛ `SmartAuditERP/Class/ReceivedData.cs:1045-1085`؛ `SmartAuditERP/Class/ListOperationPermission.cs:6-24`؛ `SmartAuditERP/Properties/Resources.resx:1178-1191`.
- **الملاحظة ومسار السبب:** داخل foreach permissions يُحذف كل OperNo>7 للموظف، ثم Activated=0 لكل صفوفه، ثم يدرج الصف الحالي فقط. لا تجميع لكل موظف أو transaction للسياسة كاملة؛ PK المرفق هو id لا (emp,OperNo).
- **الأثر والشروط:** مع صفين للموظف نفسه تختفي/تتعطل الصلاحية الأولى عند معالجة الثانية؛ الترتيب يغير النتيجة، وإعادة الرسالة قد تراكم صفوف العمليات1–7 مع تعطيل سابقتها. يمكن نشر سياسة ناقصة أو متذبذبة رغم حمولة صحيحة متعددة المنح.
- **حد الإثبات والضوابط المقابلة:** لا ندعي منحاً إدارياً معيناً أو استغلالاً حياً؛ نتيجة التقييم النهائي تتقاطع مع حارس الصلاحيات P1-012 ومع schema النشر. هذه علة replay للسياسة، لا علة محرر صلاحيات الموظفين P2-004.
- **المقترح:** لقطة سياسة كاملة لكل principal/version، replace واحد ذري بعد validation وexact key، مع rollback وتاريخ ومنع downgrade وإبطال جلسة وفق SLA؛ لا reset لكل صف.
- **القبول غير المنفذ:** `P5T-30`، `P5T-31`؛ **الثوابت المطلوبة:** `INV5-14`.

### P5-014 — فحص وجود السيريال يربط ItemId بمعرف صف السيريال لا معرف الصنف — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/ReceivedData.cs:610-637`؛ `SmartAuditERP/Class/ItemSerialNo.cs:1-14`؛ `SmartAuditERP/Class/ReceivedData.cs:372-379`.
- **الملاحظة ومسار السبب:** وجود السيريال يفحص ItemId=@ItemId وSerialNo، لكن @ItemId يأخذ itemSerialNo.Id؛ الإدراج يكتب itemSerialNo.ItemId والتعديل يستهدف Id. بذلك predicate الفحص ليس المفتاح نفسه الذي يكتب/يعدل.
- **الأثر والشروط:** عندما Id≠ItemId يمكن إعادة رسالة موجودة أن تُصنّف إدراجاً وتكرر/تتصادم، أو مطابقة سجل صنف آخر ثم تحديث صف مختلف بالـId. قد يتوقف باقي batch عند الخطأ الصامت بدلاً من idempotent upsert.
- **حد الإثبات والضوابط المقابلة:** النتيجة على مقارنة الحقول مؤكدة، أما تكرار فعلي أو رفض identity/PK فيتوقف على المخطط المنشور. P4-029 خاص بنطاق الاختيار وإلغاء الحوار، وليس هذه المقارنة؛ نوع SerialNo/InvGlobalID في DTO المحلي سؤال عقد آخر لا يخمّن تحويله.
- **المقترح:** هوية سيريال ثابتة ومفتاح طبيعي معلن بنطاق الصنف/الموقع، وتطابق check/update/insert مع affected_rows وقيود مناسبة، واختبار تكرار Id مختلف عن ItemId.
- **القبول غير المنفذ:** `P5T-32`؛ **الثوابت المطلوبة:** `INV5-03`، `INV5-15`.

### P5-015 — دورة API تؤكد الاستلام وتحذف عميل Android دون نتيجة اعتماد محلية — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/Sync.cs:315-368`؛ `SmartAuditERP/Class/Sync.cs:386-460`؛ `SmartAuditERP/Class/InvoiceOper.cs:1945-1959`؛ `SmartAuditERP/Class/InvoiceOper.cs:2185-2206`؛ `SmartAuditERP/Class/EntryOper.cs:1004-1017`؛ `SmartAuditERP/Class/ReceiptOper.cs:668-691`.
- **الملاحظة ومسار السبب:** ReadDataPeriodically يستدعي كتاباً void ثم يضبط Received أو يدعو received-by-ID ويكمل cleanup. ReadInvoiceOnline يرجع مبكراً عند رفض ZATCA قبل SQL؛ ReadEntyOnline/ReadReceiptOnline يستطيعان rollback وابتلاع خطأ داخلياً. فاتورة النوع20 تتبع ذلك بـUpdateInvoiceAsyncreceived ثم DeleteCustomerByid.
- **الأثر والشروط:** يمكن لمسار محلي لم يعتمد المستند أن يصل إلى تأكيد بعيد/حذف بيانات مساعدة، فلا يضمن fetched→locally committed→ack. عجز المستدعي عن معرفة failure/unknown يهدد replay ومطابقة الفاتورة/السند/GL؛ النوع20 له counterexample صريح دون افتعال SQL.
- **حد الإثبات والضوابط المقابلة:** توجد transactions وفحوص ClientCode/DistBranch، وقد تهرب بعض أخطاء rollback إلى catch الخارجي فتمنع ACK؛ لا نزعم أن كل فشل يبتلع. أثر API البعيد النهائي/الحذف/سياسة retry خارجي غير متاح، وإرسال/امتثال ZATCA ذاته مؤجل6؛ المؤكد أن الحارس المحلي لا يشترط commit.
- **المقترح:** نتيجة typed من الكتابة تتضمن CommitId/version/applied-already/rejected/unknown؛ ACK فقط لاعتماد مثبت ومطابق، وإبقاء customer/source حتى اكتمال كل التبعيات مع soft-delete/retention لا حذف مساعدة مبكر.
- **القبول غير المنفذ:** `P5T-33`، `P5T-34`، `P5T-35`؛ **الثوابت المطلوبة:** `INV5-07`، `INV5-12`، `INV5-16`.

### P5-016 — القيد المولد عند الاستيراد يبحث بالرقم المحلي بعد حفظ رابط رأس فارغ — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/InvoiceOper.cs:1995-2001`؛ `SmartAuditERP/Class/InvoiceOper.cs:2020-2023`؛ `SmartAuditERP/Class/InvoiceOper.cs:2058-2059`؛ `SmartAuditERP/Class/InvoiceOper.cs:2105-2152`؛ `SmartAuditERP/Class/ReceiptOper.cs:611-619`؛ `SmartAuditERP/Class/ReceiptOper.cs:620-668`؛ `SmartAuditERP/Class/StoredQueries.cs:6-8`؛ `SmartAuditERP/Class/EntryOper.cs:861-875`.
- **الملاحظة ومسار السبب:** في فاتورة20 دون EntryGlobalID يحفظ الرأس EntryID=0 ثم يبحث Entry.type=20+doc_no فقط؛ يولد/يعيد استخدام GlobalID ثم يسنده للكائن ويستدعي SaveEnty دون UPDATE لاحق لرابط الرأس في هذا الفرع. السند10 يخزن EntryGlobalID الفارغ قبل توليده، ويبحث type=5+doc_no دون فرع/هوية الأصل، ولا يعود لتحديثه.
- **الأثر والشروط:** عند نجاح هذا الفرع يمكن بقاء رابط رأس ناقص رغم وجود GL؛ رقم فاتورة/سند متكرر بفرع/جهاز أو نوع عودة قد يعيد استخدام قيد غير المقصود، وSaveEnty يعامله تحديثاً. الإعادة والربط العكسي لا يثبتان مصدر القيد من GlobalID المستند.
- **حد الإثبات والضوابط المقابلة:** لا نفترض قيم enum غير المثبتة أو أن كل Android يستوفي شروط التوليد؛ شروط النوع/الرابط الفارغ معلنة. استقلال المعاملة يعاد ربطه بـP3-003 ولا يعد هنا مرة أخرى؛ MAX+1 تحتP3-005. لم ينفذ توليد/استيراد أو يشهد استبدال قيد فعلي.
- **المقترح:** اشتقاق/حجز GLGlobalID من هوية الأصل قبل الرأس، وunique mapping للنوع+tenant+origin+documentGlobalID؛ حفظ الرابط والقيد في وحدة واحدة ثم ACK؛ لا lookup بالرقم المعروض كهوية موزعة.
- **القبول غير المنفذ:** `P5T-36`، `P5T-37`؛ **الثوابت المطلوبة:** `INV5-11`، `INV5-12`، `INV5-16`.

### P5-017 — شرط تحديث التعاريف الدوري يفضل التاريخ الحديث ويتوقف عند تأخره — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/Sync.cs:479-487`؛ `SmartAuditERP/Class/Sync.cs:120-122`؛ `SmartAuditERP/Class/SyncOperation.cs:232-248`.
- **الملاحظة ومسار السبب:** يشغّل ReadCardsDataOnline عندما CardsLastSync.AddHours(2) >= DateTime.Now؛ لا عندما يحين/يتجاوز الموعد. CardsLastSync يحمل من القاعدة أو Now ثم يحدّث بعد القراءة.
- **الأثر والشروط:** تاريخ أقدم من ساعتين لا يدخل التحديث من هذا المسار، بينما تحديث حديث يكرر الجلب. قد يتوقف catch-up بعد انقطاع طويل بالضبط عند الحاجة إليه؛ القناة اليدوية يمكن أن تخفي المشكلة ولا تصلح predicate.
- **حد الإثبات والضوابط المقابلة:** لا نزعم أن كل التعاريف لا تتحدث مطلقاً؛ توجد شاشات تحميل ومزامنة Cloud أخرى. التاريخ/المنطقة الزمنية وعلامة الصفر الابتدائية أسئلة إضافية؛ المثال يعزل المقارنة الظاهرة.
- **المقترح:** تعريف due بمعنى Now >= lastSuccessful+interval، مع bootstrap/full-sync وحالة فشل/retry ووقت monotonic للجدولة؛ فصل وقت cursor الخادم عن ساعة الجدولة المحلية.
- **القبول غير المنفذ:** `P5T-38`؛ **الثوابت المطلوبة:** `INV5-17`.

### P5-018 — علامة التعاريف تتقدم بوقت الجهاز دون اشتراط نجاح كل الحفظ المحلي — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/SyncOperation.cs:161-248`؛ `SmartAuditERP/Class/SyncOperation.cs:58-114`؛ `SmartAuditERP/Class/EntityOperations.cs:772-793`؛ `SmartAuditERP/Class/EntityOperations.cs:1807-1827`.
- **الملاحظة ومسار السبب:** ReadCardsDataOnline يمرر CardsLastSync للطلبات ثم يهمل bool نتائج SaveBranch/Invertory/Employee/Customer/Accounts/Treasuries/Banks/Products، ويكتب Now في SettingSync والذاكرة. النسخة Cloud كذلك تهمل بعض النتائج وتعلن التحميل. لا cursor ثابت من response ولا ربط ذري بتطبيق كل الأنواع.
- **الأثر والشروط:** فشل كاتب أعاد false قد لا يمنع القفز بعلامة النجاح؛ إعادة delta لاحقة قد لا تطلب التغيير الفاشل. مع API يعتمد updated-since، تغييرات بين طلب نوع مبكر وختم Now أو ساعة جهاز متقدمة قد تقع خلف cursor دون أن تقرأ.
- **حد الإثبات والضوابط المقابلة:** تقدم العلامة رغم bool الفشل ثابت من المصدر؛ فقد delta/الساعة مشروط بعقد server inclusivity/retention والزمن، لا تنفيذ. بعض exceptions غير الملتقطة توقف الدالة قبل الختم؛ لا ادعاء أن أي exception يختم دائماً. P5-017 شرط تشغيل مستقل.
- **المقترح:** cursor/sequence من الخادم مع snapshot bound وصفحات وtransaction apply+cursor لكل stream؛ عدم التقدم إلا بعد كل نتائج المجموعة، وإعادة آمنة مع overlap/dedup إذا لزم، وfull repair موثق.
- **القبول غير المنفذ:** `P5T-39`، `P5T-40`، `P5T-41`؛ **الثوابت المطلوبة:** `INV5-17`، `INV5-18`.

### P5-019 — تنزيل الموظف الموجود ينفذ SELECT بدلاً من تحديث بياناته وتعييناته — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/EntityOperations.cs:1737-1827`؛ `SmartAuditERP/Class/SyncOperation.cs:187-201`؛ `SmartAuditERP/Form_WPF/frmmanagementSync.xaml.cs:321-333`.
- **الملاحظة ومسار السبب:** SaveEmployee يبدأ COUNT command؛ للموجود يختار UPDATE وتجديد EmpBranches فقط إذا AddedLocally=true. المستدعيان التنزيليان يمران false؛ فيبقى الأمر SELECT COUNT ويستدعي ExecuteNonQuery عليه بعد إضافة معاملات ثم يرجع true. حتى الموظف الجديد لا يمر بفرع إدراج EmpBranches المذكور.
- **الأثر والشروط:** تعديل اسم/حالة/حذف/حساب الموظف الموجود من المصدر لا يطبق بهذا التنزيل رغم نجاح الدالة؛ تعيينات الفروع لا تتبع الحزمة الواردة كما يتوقع المستدعي، وقد يبقى نطاق قديم أو عضوية مفقودة.
- **حد الإثبات والضوابط المقابلة:** لا ننفي مسار MQTT آخر يحدث Employees أو جدولاً/إجراء خارجياً؛ الحكم على SaveEmployee(false) الفعلي. لا ندعي أثر منع دخول نهائياً من حقل الموظف وحده؛ الحساب والصلاحيات لها مسارات منفصلة.
- **المقترح:** فصل DownloadUpsert عن CreateLocal مع UPDATE غير مشروط بالمصدر عند وجود row، واستبدال عضويات الموظف المقصود من snapshot مصدّرة بإصدار داخل transaction مع نتيجة affected_rows.
- **القبول غير المنفذ:** `P5T-42`، `P5T-43`؛ **الثوابت المطلوبة:** `INV5-14`، `INV5-19`.

### P5-020 — تنزيل تعيينات المخازن والخزائن لا يزيل عضوية سحبت من المصدر — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/EntityOperations.cs:304-356`؛ `SmartAuditERP/Class/EntityOperations.cs:1272-1316`؛ `SmartAuditERP/Class/SyncOperation.cs:177-186`؛ `SmartAuditERP/Class/SyncOperation.cs:221-232`؛ `SmartAuditERP/Class/ReceivedData.cs:1126-1161`؛ `SmartAuditERP/Class/ReceivedData.cs:1653-1691`.
- **الملاحظة ومسار السبب:** SaveInvertory/SaveTreasuries لا يحذفان التعيينات السابقة إلا في Addlocally/AddedLocally=true، بينما التنزيل false؛ يدرجان كل Employees الواردين فقط. handlers MQTT لعضوية الفرع/المخزن يعيدون وجود الأزواج الحالية ولا يمثلون زوجاً غاب/قائمة فارغة.
- **الأثر والشروط:** إزالة موظف من قائمة المركز لا تسحب صف عضويته المحلي؛ إعادة snapshot قد تكرر الأزواج أو تصطدم بقيد. empty-list لا تعني revoke، فيبقى نطاق وصول/اختيار مورد أوسع من المرجع حتى لو بقية تحديث الاسم نجحت.
- **حد الإثبات والضوابط المقابلة:** النتيجة على lifecycle العضوية، لا إثبات منح عملية لأن التطبيق نفسه يقيم بعض الموارد بصورة غير متسقة P2-011. schema نشر قد يمنع duplicates لكنه لا يزيل عضوية غائبة. مصدر snapshot مقابل delta يجب أن يوثق قبل اختيار replace الشامل.
- **المقترح:** عقد عضويات بإصدار وأصل واضح: replace محدد principal/resource أو grant/revoke events مع tombstone، وتطبيق ذري وفريد وإبطال cache والجلسات، لا insert-only ضمن تنزيل.
- **القبول غير المنفذ:** `P5T-44`، `P5T-45`؛ **الثوابت المطلوبة:** `INV5-14`، `INV5-19`.

### P5-021 — بعض تنزيلات التعاريف تصفر الحذف أو لا تنقل حذف العناصر التابعة — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/EntityOperations.cs:654-677`؛ `SmartAuditERP/Class/EntityOperations.cs:948-977`؛ `SmartAuditERP/Class/EntityOperations.cs:1025-1036`؛ `SmartAuditERP/Class/EntityOperations.cs:15-78`؛ `SmartAuditERP/Class/ItemOper.cs:2290-2312`؛ `SmartAuditERP/Class/ReceivedData.cs:459-504`؛ `SmartAuditERP/Class/ReceivedData.cs:573-608`.
- **الملاحظة ومسار السبب:** SaveProducts يربط IS_Deleted=0 بغض النظر عن حالة المصدر، وتحديث Customers لا يورد IS_Deleted رغم إضافته كمعامل، وتحديث Branches لا يورد is_deleted؛ ReadUnitsOnline يدرج صفاً غير محذوف ولا يحدّث الحذف. MQTT لوحدات/مكونات الصنف يحدث/يدرج الواردين دون إزالة ما غاب من القائمة.
- **الأثر والشروط:** إن أرسل المصدر tombstone يمكن أن يبقى تعريف قابل للاستخدام أو يعود حيّاً؛ إذا حذف تابع من snapshot أو أصبحت قائمته فارغة لا يتقارب MQTT إليه. الصنف/المجموعة/المستخدم ليست كلها خاضعة للنمط نفسه، لذلك يمنع اعتبار أي تنزيل ناجح دليلاً على نشر السحب.
- **حد الإثبات والضوابط المقابلة:** لا نفترض أن API يعيد deleted أو أن كل payload snapshot؛ هذا شرط الأثر. كود المستهلك لا يمثل ذلك لبعض الحقول، بينما MQTT Items نفسه يكتب IS_Deleted فعلاً. version/replay الذي قد يعكس حذف مستند مالي موسّع تحت P3-006، لا نتيجة جديدة مكررة.
- **المقترح:** سياسة tombstone/revive/expiry لكل كيان وتبعياته مع retention/cursor، ومالك واحد لقرار الحذف؛ ترجمة صريحة لكل حقل، وتمييز snapshot empty عن no-change، واختبار سحب ثم إعادة رسالة أقدم.
- **القبول غير المنفذ:** `P5T-46`، `P5T-47`؛ **الثوابت المطلوبة:** `INV5-13`، `INV5-20`.

### P5-022 — حفظ العملاء أثناء التنزيل يعيد رفع الدفعة كلها مرة لكل عميل — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/EntityOperations.cs:948-966`؛ `SmartAuditERP/Class/EntityOperations.cs:1128-1182`؛ `SmartAuditERP/Class/SyncOperation.cs:203-212`؛ `SmartAuditERP/Class/Sync.cs:332-342`.
- **الملاحظة ومسار السبب:** في SaveCustomer يصل مسار AddedLocally=false العادي إلى IL_0b02 داخل foreach، فيستدعي AddCustomer(customers) للدفعة كاملة عند ActiveSync وSyncType>0، دون await. هذا يحدث أيضاً لتنزيلات المركز/Android التي قصدت الحفظ المحلي.
- **الأثر والشروط:** دفعة N عملاء ناجحة المسار يمكن أن تنتج N استدعاءات تحمل N عنصراً لكل منها، مع وقت شبكة وتحديثات عكسية غير منتظرة وإخفاق غير معروف. إذا غير الخادم updated timestamp عند كل upsert قد ينشأ echo مستمر، لكن ذلك ليس ثابتاً هنا.
- **حد الإثبات والضوابط المقابلة:** ليس تكرار سجلات بعيداً مؤكداً؛ idempotency الخادم وطريقة AddCustomer خارج المصدر، وبعض الفروع ترجع مبكراً. المثبت إعادة نشر الدفعة من داخل حلقة التنزيل وعدم انتظارها، لا حلقة شبكة شوهدت.
- **المقترح:** فصل ApplyRemote عن PublishLocal بوضوح، مع origin/operation/version منعاً للارتداد؛ رفع محلي مرة بعد commit عبر outbox، ونتائج مفصلة وانتظار المهام المطلوبة لا fire-and-forget.
- **القبول غير المنفذ:** `P5T-48`؛ **الثوابت المطلوبة:** `INV5-18`، `INV5-21`.

### P5-023 — استيراد لقطة المخزون يراكمها في الوضع النشط غير السحابي ويتجاهل اللقطة الفارغة — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/EntityOperations.cs:897-946`؛ `SmartAuditERP/Class/SyncOperation.cs:123-155`؛ `SmartAuditERP/Class/Inventory.cs:658-662`؛ `SmartAuditERP/Properties/Resources.resx:3932-3940`؛ `SmartAuditERP/Properties/Resources.resx:48668-48679`.
- **الملاحظة ومسار السبب:** SaveCurrentStocks يحذف الكل فقط لـActiveSync+BranchType4، ويحذف المفتاح فقط عند !ActiveSync & BranchType!=4؛ الوضع ActiveSync وغير4 لا يحذف قبل INSERT. ReadStockOnline لا يستدعي الحفظ إن كانت القائمة فارغة. الكاتب void ويبتلع الاستثناء بلا rollback/Close صريحين في الدالة.
- **الأثر والشروط:** إعادة snapshot ناجحة لنفس المفتاح في وضع الفرع النشط تضيف صفاً جديداً في DDL المرفق الذي لا يعرّف unique key، أو تفشل عند وجود قيد نشر. لقطة cloud الفارغة لا تمحو أرصدة قديمة، واللقطة غير الفارغة تمحو الكل دون نطاق معلن. القراءة/العرض/الصلاحية قد تعتمد أرصدة قديمة أو ملتبسة.
- **حد الإثبات والضوابط المقابلة:** لا بيانات أو schema نشر اختبرت؛ fresh snapshot مقابل delta ونطاق الاستجابة الخارجيان مطلوبان. توجد transaction في الكاتب؛ العلة شروط replacement ونتيجة الفشل والتخلص، لا ادعاء غيابها. CalcProductStocks مشكلة موقع منفصلةP5-024.
- **المقترح:** snapshotId/scope/version/complete/empty مصرح بها، staging ثم replace محدود بالنطاق ذرّي مع unique key (tenant,branch,warehouse,item,unit) ونتيجة اعتماد؛ delta upsert مختلف ومعلن، وfinally/dispose.
- **القبول غير المنفذ:** `P5T-49`، `P5T-50`، `P5T-51`؛ **الثوابت المطلوبة:** `INV5-22`.

### P5-024 — إجراء رصيد مخزون السحابة يستقبل المخزن ثم لا يرشح به — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/Inventory.cs:150-186`؛ `SmartAuditERP/Properties/Resources.resx:4214-4224`؛ `SmartAuditERP/Properties/Resources.resx:49309-49321`.
- **الملاحظة ومسار السبب:** CalcItemStock يختار CalcProductStocks عند cloud ويورد @Inventory؛ تعريفا الإجراء المرفقان يقرآن Quantity بحسب ProductId وBranchId والوحدة الأساسية فقط، دون InventoryId. scalar subquery لا يجمع ولا يرفض نطاقاً ملتبساً صراحة.
- **الأثر والشروط:** رصيد المخزن الوحيد الآخر قد يعاد للمخزن المطلوب، ووجود صفين لوحدته/فرعه يمكن أن يسبب subquery متعدد القيم بدلاً من رصيد محدد. الاختيار الظاهر للمخزن لا يضمن عزل رصيد snapshot الذي يستعمله guard.
- **حد الإثبات والضوابط المقابلة:** هذه ملاحظة عن نص الإجراء المرفق ومسار اختياره؛ لم يثبت أنه المخطط المنشور أو أن استجابة الخدمة تشمل أكثر من مخزن. تختلف عن UNION فيP4-009 وعن سباق حجزP4-014 وعن تراكمP5-023.
- **المقترح:** مفتاح/مرشح موقع ووحدة صريحان مطابقان للناشر والمستهلك، وexactly-one أو جمع معلوم المعنى؛ رفض ambiguous/unavailable بدلاً من0، وفحص النسخة المنشورة واختبار مخزنين.
- **القبول غير المنفذ:** `P5T-52`؛ **الثوابت المطلوبة:** `INV5-11`، `INV5-22`.

### P5-025 — رفع مخزون الفرع يوسم كل الكميات بوحدة رقم1 دون اشتقاق وحدة الصنف — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/Inventory.cs:606-655`؛ `SmartAuditERP/Properties/Resources.resx:3942-3948`؛ `SmartAuditERP/Class/Inventory.cs:275-304`؛ `SmartAuditERP/Properties/Resources.resx:4221-4223`.
- **الملاحظة ومسار السبب:** PostStocks يقرأ ItemsStockByBranch الذي يعيد كميات مجمعة للصنف/الفرع/المخزن، ثم يثبت UnitId=1 لكل ProductStock؛ GroupBy لا يتضمن وحدة. المستهلك المحلي للسحابة يطابق Items.unit أو item.Unit، لا ثابتاً عالمياً موثقاً في العقد.
- **الأثر والشروط:** إذا لم تكن وحدة الصنف الأساسية رقم1، تصبح الكمية موسومة بهوية وحدة لا تطابقه؛ lookup قد يرجع0/لا صف أو يعامل الكمية بوحدة أخرى. لا يوجد في هذا المسار تحويل يثبت أن UnitId1 بروتوكول عالمي مستقل عن معرف units المحلي.
- **حد الإثبات والضوابط المقابلة:** المثبت التثبيت وعدم الاشتقاق؛ أثر رصيد خاطئ مشروط بوحدات/عقد نشر. لا نختار معنى DTO.quantity أو نفترض تطابق Items وInvoiceItems. متوسط تكلفة snapshot نفسه يحتاج تعريف Q5-08 ولا يصنف خطأ جديداً دون سياسة.
- **المقترح:** نقل BaseUnitId المستقر مع QuantityBase وmapping للهوية البعيدة، وتحويل دقيق معلن عند الاستقبال؛ لا رقم سحري، ومطابقة الكمية+الوحدة+الموقع قبل اعتماد snapshot.
- **القبول غير المنفذ:** `P5T-53`؛ **الثوابت المطلوبة:** `INV5-03`، `INV5-22`.

### P5-026 — دورة السحابة تستدعي تنظيف الطابور حتى بعد رفض الدفعة وتعيد الباقي فقط — عالية / محتملة مشروطة

- **الدليل:** `SmartAuditERP/Class/Sync.cs:600-685`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatus.xaml.cs:529-575`؛ `SmartAuditERP/Class/Sync.cs:124-130`.
- **الملاحظة ومسار السبب:** PostDataPeriodicallyCloud يقسم allInvoices إلى toSend وremaining. بعد Save، حتى إذا IsValid=false/null، يحدّث InvoicesLastSync في الذاكرة ويدعو CLearfiles ثم يعيد remaining فقط. الشاشة اليدوية تدعو CLearfiles بلا معرف بعد نجاح فاتورة واحدة من القائمة، وتختم وقتاً بعد الحلقة حتى مع رفض بعض الفواتير.
- **الأثر والشروط:** إذا كان CLearfiles يمسح طابور الملفات كما يوحي عقد استعماله، تختفي عناصر toSend المرفوضة أو عناصر غير مختارة يدوياً. الفاصل بين clear وإعادة remaining معرض لانقطاع/تزامن، وInvCounttoSync=0 من الإعداد قد ينتج دفعة فارغة وختم زمن دون عمل.
- **حد الإثبات والضوابط المقابلة:** صنفت potential لأن تنفيذ InvoiceCRUD.CLearfiles/AddinvoicesLocally/مصدر PostInvoicesPeriodicallyCloud غير متاح؛ استدعاء التنظيف خارج شرط النجاح مثبت، لكن خسارة queue/عدم قابلية SQL-rebuild أو معنى وقت البحث لا تثبت من الاسم. لا ننفذ هذه الدوال أو نصلحها هنا.
- **المقترح:** عقد SDK موثق وper-operation ACK/remove فقط للعناصر المقبولة مع lease وatomic checkpoint، إبقاء failed/unknown، رفض batch size غير موجب، وحظر clear شامل من مزامنة انتقائية؛ repair من SQL مفصول ومطابق بالإصدار.
- **القبول غير المنفذ:** `P5T-54`، `P5T-55`، `P5T-56`؛ **الثوابت المطلوبة:** `INV5-04`، `INV5-07`، `INV5-18`.

### P5-027 — شاشتا مزامنة القيود والسندات تثبتان Sync=1 قبل نتيجة الإرسال — عالية / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Form_WPF/frmEntriesSyncStatus.xaml.cs:909-1025`؛ `SmartAuditERP/Form_WPF/frmEntriesSyncStatus.xaml.cs:1130-1149`؛ `SmartAuditERP/Form_WPF/frmReceiptsSyncStatus.xaml.cs:430-472`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatus.xaml.cs:578-599`.
- **الملاحظة ومسار السبب:** القيود تستدعي UpdateEntrySyncStatus(true) داخل تجهيز الصفوف قبل PostEntries، وحتى عند فشل فحص broker الداخلي. السندات تضبط كل list إلى Sync=1 قبل فحص ValidAPIUrl/await PostReceipts، ثم تعلن النجاح. الفواتير خارج شرط API يمكن أن تبقى قائمتها الأصلية وتصل إلى Sync=1 كذلك.
- **الأثر والشروط:** رفض API أو انقطاعه أو عدم تفعيله لا يعيد العلامة إلى Pending؛ تقارير المتابعة وعمليات اختيار غير المتزامن قد تخفي عناصر لم تعتمد. في وضع API صالح وحده لا يتطلب أثر القيود وصول MQTT، لذا لا يحجب P1-017 هذه العلة.
- **حد الإثبات والضوابط المقابلة:** لا ندعي معنى Sync العالمي من الخادم أو اعتماد مستقبل نهائي؛ المشكلة حتى على معنى قبول النقل المحلي. يوجد زر صريح لتغيير حالة الفاتورة دون إرسال؛ يحتاج صلاحية/سبب وسجل override ولا يساوي دليلاً على التسليم. لم تنفذ أي كتابة.
- **المقترح:** نتائج per-document accepted/applied/failed/unknown، وتحديث لاحق لهوية وإصدار مطابقين داخل transaction مع سجل محاولة؛ override حالة إدارية مستقلة عن إثبات التسليم، ولا نجاح شامل عند غياب القناة.
- **القبول غير المنفذ:** `P5T-57`، `P5T-58`؛ **الثوابت المطلوبة:** `INV5-07`، `INV5-23`.

### P5-028 — المؤقت والنقر والمهام الخلفية لا يضمنون دورة مزامنة واحدة لكل سياق — عالية / محتملة مشروطة

- **الدليل:** `SmartAuditERP/Home.xaml.cs:1672-1791`؛ `SmartAuditERP/Home.xaml.cs:2415-2433`؛ `SmartAuditERP/Class/Sync.cs:265-280`؛ `SmartAuditERP/Class/Sync.cs:479-487`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2336-2349`.
- **الملاحظة ومسار السبب:** PerformSync وCheckSyncAsync وBackgroundWorker1_DoWork هي async void؛ timer/click يستدعيان PerformSync بلا task قابلة للانتظار أو قفل noncloud. DoWork يرجع إلى BackgroundWorker عند أول await غير مكتمل بينما تتمة العمل مستمرة؛ Thread الذي يطلق async Task دون انتظار لا يملك عمر تلك العملية. السياق Sync/User static متغير.
- **الأثر والشروط:** إذا طال الطلب فوق الفترة أو تكرر النقر/تبدلت الجلسة، يمكن تداخل download/post/clear/apply ونتائج قديمة مع سياق جديد. IsBusy لا يغطي lifetime الدالة async void، ولا يضمن منع إعادة دفعة السحابة نفسها أو racing checkpoint.
- **حد الإثبات والضوابط المقابلة:** هذا خطر جدولة مشروط بطلب asynchronous فعلاً والتوقيت والنشر؛ لا تجربة سباق أو تكرار مالي. لا نستنتج semantics Equals/setter من DTO خارجي. الجلسة العالقة توسعةP2-003، واستبدال ملفات الطابورP5-004/026؛ لا يعاد عدها كتلف وقع.
- **المقترح:** خدمة Task-based واحدة بSemaphore/lease لكل tenant/database/channel، cancellation+session-generation fence، انتظار واعٍ لكل child task، وسياسة skip/coalesce/backoff؛ لا BackgroundWorker async void كحارس اعتماد.
- **القبول غير المنفذ:** `P5T-59`، `P5T-60`؛ **الثوابت المطلوبة:** `INV5-01`، `INV5-05`، `INV5-24`.

### P5-029 — عقد نتيجة المزامنة يعيد false بعد الإرسال وtrue لرد HTTP غير مفحوص — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Class/InvoiceOper.cs:2647-2661`؛ `SmartAuditERP/Class/InvoiceOper.cs:2717-2740`؛ `SmartAuditERP/Class/EntryOper.cs:1364-1395`؛ `SmartAuditERP/Class/Sync.cs:788-815`.
- **الملاحظة ومسار السبب:** SyncInvoice يهيئ result=false؛ فرع غير cloud قد يعلّم الفواتير Sync=1 ثم يدعو SyncEntry دون await ويرجع result الذي لم يتغير. SendLastCodeToApiAsync ينتظر PostAsync دون قراءة StatusCode/response ثم يرجع true لأي رد لم يرم استثناء.
- **الأثر والشروط:** لا يستطيع المستدعي الاعتماد على bool لمعرفة ما اعتمد: نجاح نقل الفاتورة يظهر false، وإخفاق HTTP4xx/5xx العادي قد يظهر true، والقيد لم يدخل نتيجة الفاتورة المنتظرة. تحسين الواجهة وحده لا يصلح هذا العقد.
- **حد الإثبات والضوابط المقابلة:** لم ترسل طلبات ولا نقرر استجابة خادم حقيقية أو أن كل caller يعمل retry عند false. فرع cloud ناجح يعيد true فعلاً؛ لا تعميم false عليه. نقص ACK بعيد/ذرية GL تحتP5-015/P3-003 منفصل.
- **المقترح:** Outcome typed بمرحلة/operation/version وaffected IDs وremote response/status، مع Await للقيد إذا كان ضمن العقد أو حالة انتظار مستقلة؛ unknown لا false/true مضللان، والتحقق من HTTP ومعنى body قبل النجاح.
- **القبول غير المنفذ:** `P5T-61`؛ **الثوابت المطلوبة:** `INV5-07`، `INV5-23`.

### P5-030 — مؤشرات النجاح تعرض المزامنة نشطة دون جمع نتائج الحفظ والإرسال — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Home.xaml.cs:1705-1791`؛ `SmartAuditERP/Class/Sync.cs:265-280`؛ `SmartAuditERP/Form_WPF/frmmanagementSync.xaml.cs:314-366`؛ `SmartAuditERP/Class/SyncOperation.cs:123-155`.
- **الملاحظة ومسار السبب:** Home يتجاهل bool ReadDataPeriodically/PostDataPeriodically/PostDataPeriodicallyCloud/ReadStockOnline ثم يعيد اللون الأخضر؛ ReadCloudDataManully يعيد true بعد بدء Thread لا بعد نجاح التنزيل. شاشة إدارة التعاريف تهمل نتائج save وبعض async operations ثم تعلن النجاح، وReadStockOnline يرجع true حتى إذا لم يعمل النوع المطلوب.
- **الأثر والشروط:** حالة متصلة/بدأت/اكتملت/اعتمدت تختلط، ويمكن أن يفهم المستخدم اللون الأخضر على أنه لا backlog أو فشل. لا last-success لكل stream أو partial/unknown من هذه المؤشرات؛ يصعب اكتشاف فاتورة/تعريف لم يطبق حتى إن رُصد exception في موضع آخر.
- **حد الإثبات والضوابط المقابلة:** المثبت معنى المؤشر في الفروع المقروءة، لا غياب كل سجل أو تقرير متابعة؛ توجد شاشات حالات وlog4net. لا يعد إعلان UI وحده وقوع فقد أو دليلاً على جودة النتائج المالية.
- **المقترح:** لوحة صحة ذات connection/progress/last accepted/last applied/pending/failed/unknown/oldest age لكل قناة، مع correlation ومحاولات/فروقات قابلة للتتبع؛ لا تغيير إلى completed إلا من outcomes مثبتة.
- **القبول غير المنفذ:** `P5T-62`؛ **الثوابت المطلوبة:** `INV5-23`.

### P5-031 — نمطا نهاية اليوم والوردية يدخلان المزامنة الفورية والمؤقت مثل النمط الدوري — متوسطة / مؤكدة من المصدر

- **الدليل:** `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:2319-2358`؛ `SmartAuditERP/Home.xaml.cs:1672-1756`؛ `SmartAuditERP/Class/Sync.cs:111-138`؛ `SmartAuditERP/Class/Sync.cs:540-585`.
- **الملاحظة ومسار السبب:** الإعداد يحفظ SyncType3 لنهاية اليوم و4 لنهاية الوردية وReadingInterval مستقلاً. CheckSyncAsync وPerformSync يكتفيان >0 ثم يشغلان أول دورة وMoveWaitTimer باستخدام PostInterval؛ الدورة غير cloud تنفذ read ثم post دون تفريع للنوع3/4 أو استعمال ReadInterval هنا.
- **الأثر والشروط:** اختيار نهاية اليوم/الوردية لا يحصر الإرسال في حدثها وفق هذه الأسماء؛ يبدأ عند التشغيل/المؤقت أيضاً. فترة القراءة المنفصلة لا تقود جدولة هذا المسار، فيصعب الالتزام بسياسة off-hours/دفعات أو توقع زمن تطبيق البيانات.
- **حد الإثبات والضوابط المقابلة:** لم نفترض عدم وجود trigger إغلاق آخر؛ وجوده لا يلغي استدعاء المؤقت المثبت. إن كان قصد المنتج أن3/4 أسماء لا حصر زمني فيلزم توثيق/تغيير UI بدلاً من ادعاء صحة الخيار؛ تصنيف الملاحظة عقد إعداد/تنفيذ، لا مخالفة تنظيمية. SDK الخارجي قد يفرض مرشحاً إضافياً لا يراه هذا المصدر؛ المؤكد دخول الدورة/استدعاء الطلبات، لا نجاح رفع بعيد خلاف السياسة فعلياً.
- **المقترح:** جدولة typed بمصفوفة mode×trigger×direction، timer مستقل/معلن لكل reading/post أو سبب توحيدهما، وعدم بدء إرسال3/4 إلا الحد المقرر مع catch-up واعٍ بعد restart واختبار إعداد0 والسالب.
- **القبول غير المنفذ:** `P5T-63`، `P5T-64`؛ **الثوابت المطلوبة:** `INV5-17`، `INV5-24`.

## 4. منع إعادة العد وتقدم المتابعات السابقة

لقطة106 تحفظ النواة السابقة كما صدرت. التوسعة التالية evidence append فقط، بلا تغيير خطورة/يقين/حالة/عنوان؛ أزيل رقم5 من `next_phase` حيث وجد سابقاً (`P1-010/P1-014/P2-003`) لأن المراجعة تمت لا لأن العلاج تم. **P1-014 رحلت صراحةً من5 إلى8** للتحقق المعزول من TLS/auth/ACL المنشور؛ لا تترك متابعة فارغة كأن المشكلة عولجت. لبقية النتائج الجديدة حددت6 لعقود SDK/المزود المناسبة و7 لاستكمال الميزات/الواجهة/العمر و8 للقبول، لا6/7 لكل خلل محلي بلا صلة.

| النتيجة القديمة | ما توسع دون إعادة عد | المراجع المضافة في5 |
|---|---|---|
| P1-010 | تسلسل ونقل كلمة المستخدم/الحقول الحساسة عبر MQTT؛ لا تنسخ قيمها أو تعاد كعيب أمني جديد. | `SmartAuditERP/Class/SendData.cs:889-919`؛ `SmartAuditERP/Class/ReceivedData.cs:1086-1109` |
| P1-011 | نصوص هوية الطفل وIDs الراجعة تدخل SQL string في مسارات تزامن؛ التلوث/الاستغلال مشروط بحد الثقة، لا exploit منفذ. | `SmartAuditERP/Class/ReceivedData.cs:1257-1264`؛ `SmartAuditERP/Class/ReceivedData.cs:1321-1325`؛ `SmartAuditERP/Class/Sync.cs:562-577` |
| P1-014 | login وsubscribe يؤكدان مسار broker/tenant topic الحالي؛ TLS/auth/ACL الأصليان لا يحسبان ضمن31. | `SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs:1027-1038`؛ `SmartAuditERP/Class/ReceivedData.cs:51-113` |
| P1-017 | بوابات FrmSyncMQtt وبعض ناشري الشراء/الحذف تنشئ Home منفصلة؛ تمنع ادعاء وصول غير مثبت وتحتاج الخدمة المشتركة. | `SmartAuditERP/Form_WPF/FrmSyncMQtt.xaml.cs:40-48`؛ `SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs:1362-1399`؛ `SmartAuditERP/Form_WPF/frmEntriesSyncStatus.xaml.cs:909-916`؛ `SmartAuditERP/Class/InvoiceOper.cs:4433-4455` |
| P2-003 | مهام التزامن والسياق السحابي static قد يكملان بعد تبديل؛ سياج الجلسة أصل واحد، ومخاطر التداخل P5-028 مشروطة. | `SmartAuditERP/Home.xaml.cs:1672-1791`؛ `SmartAuditERP/Class/SyncOperation.cs:78-114` |
| P3-003 | توليد GL عند Android عبر SaveEnty بمعاملة مستقلة؛ أصل ذرية المستند/GL لا يعاد عده كـtransaction مفقودة عامة. | `SmartAuditERP/Class/InvoiceOper.cs:1968-1975`؛ `SmartAuditERP/Class/InvoiceOper.cs:2137-2152`؛ `SmartAuditERP/Class/ReceiptOper.cs:652-668` |
| P3-006 | upsert/replay لا يقارن إصداراً ويستبدل الحالة الحالية؛ منع downgrade/إحياء الحذف امتداد لتاريخ/نسخة الأصل. | `SmartAuditERP/Class/EntryOper.cs:941-1017`؛ `SmartAuditERP/Class/ReceivedData.cs:1313-1388`؛ `SmartAuditERP/Class/ReceivedData.cs:1171-1176` |
| P4-029 | سيريال MQTT طريق آخر لتفرد/نطاق السيريال؛ اختلاف predicate المحدد P5-014 منفصل عن اختيار/إلغاء الحوار. | `SmartAuditERP/Class/ReceivedData.cs:610-637` |

- `P3-005` يبقى أصل MAX+1 والترقيم/upsert collision؛ لا نتيجة جديدة بعنوان «كل GlobalID غير فريد» من MQTT.
- `P4-019` يبقى أصل فشل جانبي المناقلة؛5 تتبع إرسالها/طابورها لا يعيد احتساب اعتمادها. `P3-014` للإغلاق العادي باقية رغم وجود ClosingReport أفضل معاملةً.
- H3-02/البديل Android غير مثبت المدخل لا يحول إلى قناة حية من helper؛ H5-02 يحفظ حد الوصول. أسئلة H4/Q4 عن الائتمان/expiry/waste/retention لا تحسم أو تنفى بهذا التتبع المحدد.
- غياب ضمان ظاهر بالعميل لا يثبت غيابه عالمياً؛ H5-01/03/04 وQ5 تسمي العقد/المخطط/البيئة المطلوبة بدلاً من زيادة findings لجهل المكون الخارجي.

## 5. ما ينقص عقد المزامنة المقترح

هذه متطلبات تصميم/قبول مبنية على النتائج، لا كود نفذ ولا رفض لكل التقنيات الحالية:

1. **هوية سياق ثابتة:** Tenant/DatabaseInstance/OriginBranch/Device/Destination وschema version، مع operationId وaggregateId وexpected/new version؛ map للهويات القديمة دون إعادة استعمال رقم العرض كهوية موزعة.
2. **Outbox/Inbox:** نية إرسال في اعتماد الأصل، claim/lease مع retry/backoff/attempt، ومفتاح تكرار/بصمة يحتفظ به المستقبل بما يلائم أقصى offline؛ ACK تطبيق محدد الإصدار بعد commit، لا إزالة شاملة أو QoS كتأكيد SQL.
3. **حالات ذات معنى:** LocalCommitted→Pending→TransportAccepted→Applied/Rejected/Unknown. فقد الرد بعد commit حالة Unknown تستعلم/تعاد idempotently، لا rollback مفترضاً أو نجاحاً أخضر.
4. **عقد تقارب لكل كيان:** snapshot مقابل delta، parent/scope حتى مع empty، tombstone ومن يملك revive، منع downgrade، authority/conflict resolution بالسياسة والتاريخ؛ الأمور المالية تعدل/تعكس وفق سياسة لا last-arrival الصامت.
5. **معاملة أو staging aggregate:** الرأس والبنود والروابط اللازمة وGL بحسب السياسة يطابقون نسخة وmanifest؛ استيراد Android يولد/يحجز الرابط أولاً ويثبت mapping قبل إنهاء المصدر.
6. **Cursor:** server snapshot bound/sequence مع صفحات وتطبيق واعتماد cursor، أو overlap معلوم مع dedup؛ ساعة الجهاز تصلح للجدولة لا للبرهنة على استيعاب تغييرات لم تقرأ.
7. **Stock/security:** snapshot محددة الموقع والوحدة والإصدار وcomplete/empty؛ cache قابلة لإعادة البناء لا دفتر حقيقة ثانياً بلا تصالح. grants/revokes تطبق سياسة كاملة لكل principal/version وتبطل جلسة/cache ضمن SLA.
8. **خدمة تزامن واحدة قابلة للرصد:** connection owner وsingle-flight/session fence/cancellation وعمر Task كامل؛ مصفوفة mode×trigger×direction، pending/failed/unknown/oldest-age وعمليات repair ذات تفويض وسجل لا clear يدوي مخفي.

تفصيل النواقص والإضافات في G-42 إلىG-50 من [IMPROVEMENTS.md](IMPROVEMENTS.md)، مع ارتباط المعايير بـ[الثوابت24](evidence/sync-invariants-05.csv) و[الخطط64](evidence/acceptance-tests-05.csv).

## 6. التحقق وحالة الخروج

- [VALIDATION-05.md](VALIDATION-05.md) يفرق فحوص الوثائق/الأمثلة التي نفذت عن **64 خطة تطبيق غير منفذة**. نتيجة الفحص الآلي التفصيلية في [checks-05.json](evidence/checks-05.json)؛ نجاح hash/range/link لا يثبت الدلالة أو صحة schema أو التسليم.
- الحصر827 والبصمات38 التاريخية ولقطة106 تحفظ المصدر والأثر السابق؛ لا baseline جديد لإخفاء اختلاف. `--through-phase 2/3/4` يعيد فحص frozen49/74/106 لا سجل137 كأنه تاريخ قديم، ولا يستبدل checks التاريخية.
- لا build أو WPF أو SQL/ترحيل أو broker/API/cloud أو fault injection/restart فعلي، لا تحميل assemblies أو بيانات/مفاتيح إنتاج، لا تعديل تطبيق أو commit/push؛ كل137 مفتوحة.
- معيار الخروج الساكن5 تحقق بتوثيق التدفقات والملكية والمواضيع وحالات الفشل وحدود المكونات الخارجية؛ **ليس انتهاء تدقيق النظام كله أو إثبات offline موثوق تشغيلياً**.

**التوقف هنا. المرحلة6 — التكاملات الخارجية والفوترة الإلكترونية والمدفوعات — تحتاج إذناً جديداً.** لا تعد قراءة caller في5 تدقيقاً قانونياً/تقنياً لمزود6، ولا تنفذ أي خطة قبول أو إصلاح تلقائياً.
