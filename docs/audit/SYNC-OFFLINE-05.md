# نموذج المزامنة والأوفلاين — المرحلة5

**مرجع التدقيق:** 2026-11-16؛ `10ba215152f722c8808aea0bb672c1d1d4d9d711`، الفرع `arena/94ae8414-smartauditerp`.  
**النوع:** تتبع ساكن للقنوات/الهوية/النتائج، لا packet trace أو sequence ثبت تشغيله. [التقرير](PHASE-05.md) يحوي31 نتيجة جديدة؛ [النطاق54](review-scope-05.csv) محدد بالمقاطع. كل جداول التشغيل أدناه `not-executed` وليست findings إضافية.

## 1. حدود الثقة والاعتماد

```text
[جلسة/قاعدة/فرع محلي]                         [قناة خارجية لم تنفذ]
  شاشة → SQL commit
      ├─ JSON IDs بعد الحفظ → replay → Publish ─── MQTT broker ── receiver → SQL
      │   لا version/context ثابتين     │           │             │
      │   clear محلي بعد محاولة         └ نقل ≠ تطبيق ┘      رأس/طفل/GL منفصلون
      ├─ AuditorAPI CRUD / SDK queue ─────────────── HTTP/API → queue/route/ACK مجهول العقد
      └─ Cloud Save أو periodic batch ───────────── Ws_Auditor / Cloud
            cloud-first قد يسبق SQL                 clear semantics خارج المصدر

[تنزيل HTTP فعلي]
  fetch → فحص ClientCode/DistBranch → writer void → received/cleanup
                                        │                  │
                            transaction/return/rollback   لا يشترط outcome اعتماد
                            GL fallback قد يكون مستقلاً

[تنزيل master/stock]
  lastTime → طلبات عدة → Save* bool مهمل → checkpoint=Now
  snapshot/empty/وحدة/موقع/عضوية/حذف ليست مرادفات upsert
```

هذا الرسم **يلخص حدوداً مقروءة** ولا يثبت أن كل حافة قابلة للوصول في كل إعداد. MQTT بعض ناشريه خلف `P1-017`؛ API/status لها فروع مستقلة. `P1-014` حد النقل/التوثيق لا يعاد عده. `P2-003` حد تبديل الجلسة، و`P3-003/006` حد الأصل المالي ونسخته/تاريخه، باقية جميعاً.

### 1.1 قاموس الحالة المطلوب، لا وصف تنفيذ قائم

| الحالة المقترحة | ماذا تثبت | ماذا لا تثبت |
|---|---|---|
| LocalCommitted |المستند/الإصدار ونيته المحلية اعتمدا وفق سياسة الأصل|أن طرفاً آخر استلمه|
| Pending/Claimed |سجل durable ينتظر/تملكه محاولة بlease|أن Publish/HTTP قد نجح|
| TransportAccepted |قُبل النقل/الطلب وفق عقد broker/API محدد|commit SQL أو تطبيق كل سطور aggregate|
| Applied |ACK مطابق operation/version/hash بعد commit مستقبل|صحة الحساب/الضريبة إن كان validator نفسه ناقصاً|
| Rejected |رفض معلوم السبب لا يعد تطبيقاً|أن الحذف أو الإصلاح أو إعادة الإرسال التلقائي مسموح|
| Unknown |انقطع الرد أو لم يعرف حد commit؛ يحتاج query/replay idempotent|rollback أو failure نهائياً؛ لا تحول إلى Sync=1 أو clear تخميناً|

وجود QoS1 أو GlobalID أو transaction/PK مفيد لكنه لا يجمع هذه الحالات تلقائياً. لا يعد Color=Green أو `bool true` بديلاً عن commit id. الفشل بعد commit لا يعالج بإعادة أصل مالي عمياء؛ اختيار exactly-once لا يستنتج من QoS أو اسم SDK.

## 2. تدفقات القنوات18 والوصول الفعلي

السجل الكامل [sync-flows-05.csv](evidence/sync-flows-05.csv) يضم caller/الوصول والهوية وحد commit/ACK وحالات duplicate/order/delete وحدود كل قناة ومراجعها. هذا ملخصه؛ أسماء "live" لا تعني تشغيلها هنا.

| التدفق | القناة ومدخلها | الوصول وحد النتيجة |
|---|---|---|
| SF5-01 — MQTT-configuration | login→ConnectBroker→Home.ConnectMQTList→LoadReceived | المدخل ظاهر عند تفعيل _is_active في Home المعروض؛ حالة الإعداد ليست اختبار تشغيل. كل فحص ناجح ينشئ عميلاً جديداً؛ ربط handlers لاحق وليس وحدة عمل مع الاتصال. |
| SF5-02 — MQTT-item-save | frmItems commit→SyncProduct أو MQTT/SaveItemIDOffLine | كاتب الصنف موجود؛ يجب إثبات بوابة Home الجديدة لا افتراض تجاوز P1-017. اعتماد SQL يسبق كتابة نية الإرسال؛ Publish لا يعيد ACK تطبيق. |
| SF5-03 — MQTT-invoice-save | frmInvPurch/POS/InventoryTransfer→SendDataa أو SaveGlobalIDOffLine | callers موجودون لكن new Home()._is_active قد يحجب فروع MQTT ؛ لا نفترض تفعيلها. اعتماد الأصل وكتابة نية الرسالة مستقلان؛ SendDataa void ولا ACK من المستقبل. |
| SF5-04 — MQTT-replay | Home.TimerCheckInternet_Tick→SendStoredItems | caller مؤقت مثبت بشرط _is_active في Home المعروض. read→publish أو تخطي عند false→clear ؛ LoadReceived في النهاية لا يثبت اعتماد الرسائل السابقة. |
| SF5-05 — MQTT-manual | Home menu→FrmSyncMQtt upload/download | ربط XAML مثبت لكن new Home يحجب المسار؛ لا ترقيع للبوابة أثناء التدقيق. رسالة نجاح بعد publish/subscribe لا بعد apply ؛ لا outcome لكل كيان. |
| SF5-06 — MQTT-receive-document | MqttMsgReceivedOper→InsertInv/Sub/Entry/Sub/Receipt | الاشتراك _syncOper ظاهر؛ رسائل وسيط فعلي لم ترسل. تفاصيل وسند MQTT تحذف/تدرج خارج معاملة aggregate ؛ catches لا تعيد نتيجة للناشر. |
| SF5-07 — MQTT-receive-security | MqttMsgReceiveddefinitions→Users/permissions/EmpBranches/SafeEmp | اشتراك definitions ومعالجاته ظاهرة؛ actor/authority الخارجيان غير موثقين هنا. OperationPermission يعيد reset لكل صف؛ بقية التعريفات/عضوياتها ليست policy transaction موحدة. |
| SF5-08 — HTTP-upload-direct | Save caller→SyncInvoice/SyncEntry/SyncReceipt→AuditorAPI CRUD | callers API ظاهرة مستقلة عن MQTT ؛ SyncInvoice cloud فرع مختلف. قائمة رد SDK تقود Sync=1 ؛ SyncInvoice لا ينتظر child SyncEntry في الفرع غير السحابي. |
| SF5-09 — HTTP-upload-periodic | Home.PerformSync→Sync.PostDataPeriodically | تشغيل أولي ومؤقت ونقرة عند SyncType>0 ؛ noncloud مشروط Conn_type=1. لا outcome اعتماد aggregate موحد؛ remove/update queue وسلوك received خارج العميل المتاح. |
| SF5-10 — HTTP-download-import | Home.PerformSync→ReadDataPeriodically→local writers→UpdateReceived/cleanup | مدخل فعلي؛ فحص ClientCode و DistBranch للمستندات ضابط إيجابي محفوظ. كاتب void يمكن أن يرجع دون commit ؛ caller يكمل ACK أو حذف العميل المساعد. |
| SF5-11 — HTTP-relay-branch3 | ReadDataPeriodically BranchType3→route fields→remote update | فرع موجود في المصدر؛ لم يختبر تتابع وسيط ووجهة. حفظ محلي قبل التوجيه؛ هل SDK ينقل Received=false أو يعرف route من الخادم غير معلوم. |
| SF5-12 — HTTP-master-delta | Sync due→ReadCardsDataOnline→Save*→local-now checkpoint | المؤقت مثبت، لكن predicate due مقلوب؛ توجد بدائل يدوية منفصلة. نتائج Save* bool مهملة؛ العلامة DateTime.Now وليست server snapshot cursor. |
| SF5-13 — Cloud-master | Home refresh→ReadCloudDataManully→ReadCardsDataCloud | زر ظاهر؛ بدء Thread لا يساوي انتظار اكتمال Task. Get* متنوعة ثم saves بنتائج مهملة؛ رسالة تحميل لا تلخص commit فعلياً. |
| SF5-14 — Cloud-invoice-direct | frmInvPOS cloud-first أو SyncInvoice branch4 | حراس BranchType4 و SyncCloudFirst و ValidAPI وغير trial ظاهرة. cloud-first قد يعتمد بعيداً قبل SQL المحلي؛ عقد Save per-item غير متاح. |
| SF5-15 — Cloud-invoice-backlog | Home BackgroundWorker→PostDataPeriodicallyCloud | DoWork async void و InvCounttoSync من الإعداد؛ عمر IsBusy ليس عمر كل await. CLearfiles بعد Save خارج IsValid ثم إعادة remaining فقط؛ التنفيذ داخل SDK غير متاح. |
| SF5-16 — Manual-status-screens | Home menus→invoice/entry/receipt Sync buttons | أحداث وأزرار مثبتة؛ API-ready يكفي لمسار القيود ولو MQTT محجوب. بعض Sync=1 قبل API ؛ clear سحابي انتقائي دون ID ؛ override حالة فاتورة صريح. |
| SF5-17 — Stock-snapshot | frmStocksSync/Home cloud quantity→ReadStockOnline ؛ Inventory.PostStocks | callbacks ظاهرة؛ لقطة ProductStocks تقابل دفتر الحركات في أوضاع أخرى. SaveCurrentStocks له transaction لكن شروط replacement ونتيجة الفشل غير سليمة. |
| SF5-18 — Closing-and-legacy-boundaries | ReadDataPeriodically→ClosingReport ؛ legacy helpers | ClosingReport له caller ؛ SignalR.StartConnection و FrmSyncInv/Settings بلا caller مثبت؛ GetDataAPI مثال PM فقط. ClosingReport يستبدل الرأس/التفاصيل في transaction مع rollback/rethrow ؛ لا ACK لنسخة منشورة ظاهر. |

### 2.1 سيناريوهات تقارب لا يغطيها مجرد نجاح upsert

- **الصنف A ثم B والمستقبل غائب:** retained للموضوع النوعي يحمل آخر payload؛ قد تتسلم B ولا A. النشر الشامل اليدوي قد يعوض لكنه ليس catch-up مضموناً في بروتوكول الدلتا (`P5-009`).
- **فقد الرد بعد اعتماد المستقبل:** clear بعد Publish يمنع مطابقة ما طبق؛ retry دون inbox/version قد يستبدل أحدث حالة. الحفاظ على السجل وحده لا يضمن idempotent side effects (`P5-006` و`P3-006`).
- **رأس2 ثم بنود1 أو حذف آخر بند:** رسائل مستقلة بلا manifest/version؛ القائمة الفارغة لا تعرّف الأب، وdelete-loop ثم insert-loop يترك partial عند فشل وسطها (`P5-012`). HTTP المحلي له transaction مختلفة، فلا تنقل التعميم إليه.
- **Android رفض محلي:** `ReadInvoiceOnline` يمكن أن يرجع قبل SQL، بينما caller void يكمل received/delete المساعد؛ كذلك rollback مبتلع في فروع أخرى. بعض الفشل يهرب فيوقف ACK، لذلك المشكلة غياب عقد outcome لا تأكيد كل فشل (`P5-015`).
- **تغيير قديم للموظف أو عضوية مسحوبة:** نجاح SaveEmployee(false) قد يكون SELECT لا UPDATE، وعضويات resources التنزيلية لا تحذف الغائب. يجب تحديد snapshot/grant-revoke قبل سياسة replace، مع principal/version وإبطال cache (`P5-019/020`).
- **حذف ثم replay أقدم:** upsert الحالي/IS_Deleted من حمولة قديمة لا يحفظ بالضرورة tombstone الأحدث؛ هذا امتداد `P3-006` لا علة تاريخ جديدة. بعض تنزيلات التعريفات لا تنقل الحذف أصلاً (`P5-021`).
- **لقطة مخزون فارغة أو مخزن ثانٍ/وحدة7:** تجاهل empty ليس مسحاً ناجحاً، وتراكم/تصفير scope شامل ليس delta، و@Inventory المهمل/UnitId1 يغيران هوية الرصيد (`P5-023/024/025`). لا يفترض snapshot authoritative لكل الأوضاع.

## 3. ملكية البيانات والهوية12

**الموجود كتاب ظاهرون، لا خريطة سلطة معتمدة من المالك.** لا تختار هذه المراجعة last-writer-wins أو مركزاً مرجعياً بدلاً من المنتج/المحاسبة/الأمن. السجل [sync-data-ownership-05.csv](evidence/sync-data-ownership-05.csv) يحفظ الهوية وحدود الحذف/revoke والتعارض لكل مجموعة.

| المجموعة | الكتاب الظاهرون | العقد/السلطة التي يلزم حسمها |
|---|---|---|
| OWN5-01 — مستندات الفروع ورؤوسها | شاشات SQL المحلية؛ MQTT InsertInv ؛ HTTP ReadInvoiceOnline ؛ Cloud SDK | تعدد جهات الإنشاء والتعديل ظاهر؛ مالك التعديل/الحذف المتزامن غير موثق بهذا المصدر. الحذف المحلي soft لبعض المستندات؛ version و ACK و policy replay ليست موحدة. |
| OWN5-02 — تفاصيل المستند و GL وروابطهما | MQTT writers مستقلة؛ HTTP transactions لكل أصل؛ SaveEnty بمعاملة أخرى | ملكية child يجب أن تتبع parent/version ؛ توقيت GL مطلوب من سياسة المحاسبة. empty و staging وتوازن/عكس/حذف الروابط تحتاج عقداً معتمداً. |
| OWN5-03 — مستخدمون وصلاحيات | MQTT User/UserPermissions/OperationPermission وواجهات محلية | الجهة المخولة لنشر سياسة المنح أو سحبها غير مثبتة من broker ACL. سياسة كاملة ذرية بالإصدار ومنع downgrade ؛ reset لكل صف لا يتقارب. |
| OWN5-04 — موظف وعضوية فرع | SaveEmployee(false/true) و MQTT Employee/EmpBranches | هل المركز مرجع أم توجد تعديلات فرع؟ يحتاج قراراً موثقاً لا تخميناً. تنزيل الموجود لا ينفذ UPDATE في الفرع المحدد؛ العضوية تحتاج سحباً/استبدالاً محدداً. |
| OWN5-05 — صنف ووحدات/مكونات/سيريال/أسعار | واجهات محلية؛ retained نوعي؛ SaveProducts وتوابع API | ملكية تعريف مركزي مقابل override سعر/وحدة فرعي تحتاج Q5-01. snapshot/delta و tombstone لكل تابع؛ بعض MQTT upsert-only. |
| OWN5-06 — عملاء وموردون وحساباتهم | SaveCustomer محلياً/تنزيلاً؛ Customers/AccountCust ؛ Android cleanup | من يملك العميل المؤقت وحذفه؟ سلطة المركز/Android و return-to-API تحتاج عقداً. نقل الحذف ناقص بفروع محددة؛ لا echo من ApplyRemote ولا حذف مصدر قبل commit. |
| OWN5-07 — دليل حسابات وفروع وتعريفات موارد | SaveAccounts/Branch/Invertory/Treasury/Banks و MQTT definitions | سلطة جذر الحسابات والشجرة والموارد وتعارض تعديل الفرع تحتاج Q3/Q5. تحديد سياسة حذف/إصدار وعضوية؛ لا مطابقة اسم أو اختزال grant/revoke في insert. |
| OWN5-08 — لقطات المخزون وتغييرات cache | StockCRUD و ClsItem ؛ Inventory.PostStocks ؛ POS UpdateItemsQty | مصدر حقيقة snapshot مقابل الحركة والحجز/cache قرار أعمال/تقنية مطلوب. replace بنطاق/empty معلنين ومنع تطبيق نسخة مرتين؛ cache يطبق فرقاً موثقاً أو يعاد بناؤه. |
| OWN5-09 — طابور ملفات MQTT | كتّاب أصناف/مستندات متعددون؛ SendStoredItems يفرغ الملفات | مالك queue يجب أن يكون قاعدة/مستأجراً/وجهة ثابتة لا مجلد تثبيت عاماً. append/claim/ACK لكل سجل و quarantine للمعيب؛ لا clear شامل بعد مجرد Publish. |
| OWN5-10 — طابور SDK ودفعات cloud | AuditorAPI Add*/PostPeriodically/CLearfiles ؛ Ws_Auditor.Save | مصدر queue وديمومتها وإعادة بنائها وقبول partial غير متاحين. قبول ذري موثق أو نتائج per-item ؛ unknown يستعلم عنه قبل الإعادة أو الحذف. |
| OWN5-11 — cursor وإعدادات modes | SyncOperation يختم Now ؛ Sync.CheckSync ؛ frmSettings | Server sequence/cursor مصدر تغيرات، وساعة الجهاز للجدولة لا مرجع ملكية البيانات. تقدم بعد تطبيق نطاق جلب معلوم، bootstrap/retry ، ومصفوفة mode×trigger×direction. |
| OWN5-12 — إغلاق/تقارير وحالة متابعة | ClosingReport بمعاملة؛ MQTT closing منفصل؛ Home/status forms | مصدر إغلاق معتمد وتوقيت GL وسلطة override للمتابعة تحتاج سياسة. transaction HTTP موجودة؛ version/inbox/ACK وحل تعارض إغلاق لم تحسم. |

مفتاح SQL موجود لا يثبت هوية عبر قواعد مختلفة. GlobalID بصيغتي Branch-No وClient-Branch-No لا يصلح له StartsWith ولا raw Id من فرع آخر. parent/line/site/unit/version وorigin وdestination مطلوبة مع أذونات ومراجع ثابتة. لا يفترض أن namespace موضوع ClientCode المتصل نصياً يفرض ACL أو توقيعاً على الحمولات؛ ذلك يحتاج عقد broker/server.

## 4. عقد مواضيع MQTT25

`{client}` أدناه هو النص الحالي لـClientCode لا رمز تقسيم معتمد. **أسماء المواضيع حساسة للحروف.** فلاتر `x/#` تشمل x العاري لكن handler العمليات يقرأ المقطع الثاني دون guard. اشتراك LoadReceived QoS1 لا يرفع QoS0 publisher إلى ACK تطبيق. كل payload هنا وصف DTO/metadata محلي؛ ليست schema server معتمدة أو body writer كامل مدقق.

**قيد الوصول:** معظم الناشرين اليدويين في FrmSyncMQtt خلف `new Home()._is_active`؛ الجدول يوثق العقد المصدر لا نجاح النشر. لكل صف publisher/subscription/dispatch evidence مقطعي في [mqtt-topic-contracts-05.csv](evidence/mqtt-topic-contracts-05.csv). لا تعد25 صفاً findings مستقلة.

| العقد | الموضوع الصادر | الاشتراك والمعالج | QoS/retain وحد العقد |
|---|---|---|---|
| MT5-01 — Items | {client}Items (صنف واحد أو كل القائمة) | نفس الاسم؛ _syncItems؛ Items handler EndsWith(Items) | QoS0 retain=true؛ كل دلتا تستبدل آخر retained نوعي؛ السعر/الاسم/الحذف من الحمولة دون expected version ظاهر. |
| MT5-02 — ItemsUnit | {client}ItemsUnit | نفس الاسم؛ _syncItems؛ Items→InsertItemUnits | QoS0 retain=true؛ upsert للوارد فقط؛ لا إزالة وحدة غابت أو empty محددة الأب |
| MT5-03 — ItemPrices | {client}ItemPrices | نفس الاسم؛ _syncItems؛ Items→InsertItemPrice | QoS0 retain=true؛ نفس موضوع snapshot/delta ؛ دلالة السعر/identity migration ليست مثبتة خارج المقاطع |
| MT5-04 — ItemComponents | {client}ItemComponents | نفس الاسم؛ _syncItems؛ Items→InsertItemComponents | QoS0 retain=true؛ upsert بالـ Id دون حذف الغائب؛ full ودلتا غير مميزين |
| MT5-05 — ItemSerialNo | {client}ItemSerialNo | نفس الاسم؛ _syncItems؛ Items→InsertItemSerialNo | QoS0 retain=true؛ فحص وجود السيريال بمفتاح مختلف عن الكتابة؛ FrmSyncMQtt يستعمل GetItemComponents خلف بوابة Home ، كما في H5-02. |
| MT5-06 — ItemBarcode | {client}ItemBarcode | نفس الاسم؛ _syncItems؛ Items→insertItemBarcode | QoS0 retain=true؛ وجود handler لا يثبت حذف/تعارض كل الباركود؛ نوعي retained ليس backlog |
| MT5-07 — Units | {client}Units | نفس الاسم؛ _syncItems؛ Items→InsertUnits | QoS0 retain=true؛ يلزم فصل عقد tombstone لكل قناة؛ نقص ReadUnitsOnline لا يعمم على MQTT |
| MT5-08 — ItemsCategory | {client}ItemsCategory | نفس الاسم؛ _syncItems؛ Items→insertItemCategory | QoS0 retain=true؛ schema/دلالة snapshot/version غير معلنة في الغلاف المحلي |
| MT5-09 — Customers | {client}Customers | _syncOper يشترك بالاسم العاري؛ Oper لا يملك case للعملاء ويفرض slash ؛ Items يعالجها إذا حُمّل أيضاً. | QoS0 retain=true؛ تفعيل العمليات وحده لا يكفي؛ قائمة عملاء كاملة ليست دليلاً على سلطة المصدر أو قبولها. |
| MT5-10 — AccountCust/AccountIndex | {client}AccountCust أو AccountIndex | _syncOper يشترك بالاسمين؛ Oper لا يملك case للحسابين؛ definitions يعالجهما إذا فُعّل. | QoS0 retain=true؛ اعتماد غير معلن بين flags ؛ ClientCode ليس فاصلاً أو ACL معتمداً بمجرد وجوده. |
| MT5-11 — Employee/EmpBranches/AccountEmp | {client}Employee/EmpBranches/AccountEmp | _syncDefinitions يشترك بها؛ definitions handlers حسب EndsWith | QoS0 retain=true؛ عضوية MQTT تطبق upsert لا revoke للغائب؛ SaveEmployee(false) عبر API فرع مختلف لا يحدث الموجود. |
| MT5-12 — Users | {client}Users | _syncDefinitions؛ definitions→InsertUsers | QoS0 retain=true؛ كلمات المستخدم/النقل امتداد P1-010/014 ؛ raw IDs وسلطة المصدر لم يعتمدا خارج العميل. |
| MT5-13 — UserPermissions | {client}UserPermissions | _syncDefinitions؛ definitions→InserUserPermissions | QoS0 retain=true؛ المقطع المقروء upsert لكل صف لا replace لسياسة كاملة؛ إعادة ترتيب/empty/إصدار أقدم تحتاج عقداً ومنع downgrade. لا حكم شامل على محرك الصلاحيات. |
| MT5-14 — OperationPermission | {client}OperationPermission | _syncDefinitions؛ definitions→InsertOperPrimisson | QoS0 retain=true؛ reset داخل كل صف؛ إعادة الإرسال أو تغيير ترتيب الصفوف لا يحافظان على السياسة الكاملة. |
| MT5-15 — Safe | {client}Safe | غير موجود في قائمة definitions؛ handler موجود | QoS0 retain=true؛ ناشر يدوي خلف بوابة Home ؛ وجود handler لا يثبت اشتراك العميل بالموضوع. |
| MT5-16 — SafeEmp | {client}SafeEmp | _syncDefinitions؛ definitions→InsertOrUpdateSafesEmp | QoS0 retain=true؛ إعادة إدراج الموجود ولا حذف زوج غاب من snapshot |
| MT5-17 — Stock/StockEmp | {client}Stock و StockEmp | _syncDefinitions؛ definitions→stock/stock-membership writers | QoS0 retain=true؛ Stock تعني خزينة لا ProductStocks الكمية؛ dispatch مقروء لكن دورة سحب StockEmp كاملة غير مثبتة، فلا تعمم علة SafeEmp عليها دون تتبع. |
| MT5-18 — Banks/Branches | {client}Banks و Branches | _syncDefinitions؛ definitions handlers | QoS0 retain=true؛ Client topics ليست برهان عزل الخادم؛ لكل قناة عقد حذف مستقل لم يفترض تكافؤه. |
| MT5-19 — Offer/OfferClient/OfferItem | {client}Offer/OfferClient/OfferItem | غير موجودة في definitions؛ handlers موجودة | QoS0 retain=true؛ لا subscription لهذه الأسماء في LoadReceived ؛ الناشر اليدوي خلف P1-017. جسم OfferItem writer ليس ضمن النطاق فلا نتيجة SQL جديدة منه. |
| MT5-20 — Inv | {client}Inv/{id} أو {client}Inv العاري في replay/bulk | _syncOper: {client}Inv/#؛ Oper يأخذ Split[0] و[1] ثم InsertInv | SendDataa: QoS1 ؛ replay/bulk: QoS0 ؛ retain=true؛ x/# يطابق x العاري لكن Split[1] يفشل؛ حارس بادئة الأصل والنسخة لا يثبت هوية مصدر صحيحة. |
| MT5-21 — InvSub | {client}InvSub/{id} أو bare | _syncOper: {client}InvSub/#؛ Oper→InsertInvSub | QoS1 أو 0 retain=true؛ empty بلا parent ؛ delete ثم insert دون transaction لهذا الكاتب؛ تأخر الأطفال لا يربطهم بإصدار الرأس. |
| MT5-22 — entry | {client}entry/{id}؛ بدائل Entry/EntrySub لا تتطابق | _syncOper: {client}entry/# بحروف صغيرة؛ Oper case entry | QoS1 أو 0 retain=true؛ حالة الأحرف مختلفة في الناشرين البديلين؛ لا expected version ظاهر. لم يشهد تعديل قيد أو نجاح استيراده بالتشغيل. |
| MT5-23 — entryDetails | {client}entryDetails/{id}؛ EntryGlobalID/EntrySub في bulk | _syncOper: {client}entryDetails/#؛ Oper→InsertEntrySub | QoS1 أو 0 retain=true؛ مواضيع بديلة غير مشتركة؛ replace غير ذري، وقائمة empty مجهولة الأب. |
| MT5-24 — Receipts | {client}Receipts/{id}؛ بعض manual يستعمل /0 أو bare | _syncOper: {client}Receipts/#؛ Oper→InsertOrUpdateReceipts | QoS1 أو 0 retain=true؛ /0 يجمع آخر دفعة retained على موضوع واحد إذا وصل الناشر؛ bare يفشل parser ؛ الرأس يحذف ثم يدرج. |
| MT5-25 — CasherClosed/CasherClosed_Sub | {client}CasherClosed[/id] و CasherClosed_Sub[/id] | _syncOper يشترك بالاسمين bare وبـ/#؛ Oper يفرض Split[1] ثم يستدعي كاتبي رأس/تفاصيل منفصلين. | QoS1 أو 0 retain=true؛ ناشر POS خلف new Home ؛ P3-014 تخص مدخل الإغلاق العادي ولا يعالجه وجود ناشر أو كاتب آخر. |

- أعلام items/oper/definitions غير متطابقة مع مسؤوليات dispatch: قد يعالج handler آخر رسالة وصلته بسبب اشتراك من علم مختلف؛ نجاح جميع الأعلام لا يثبت صحة كل تركيبة منفردة (`P5-008`).
- المستقبل يزيل passcode بـReplace عالمي؛ غلاف الرسالة لا ينبغي أن يغير اسم عميل/باركود/ملاحظة. AESencDEC خارج المصدر، فلا نستنتج mode أو MAC أو مقاومة تلاعب من اسمه (`P5-010`).
- topics/ACK/context أو schema migration يجب أن تكون عقداً واحداً بين immediate/bulk/offline؛ تغيير ناشر واحد لا يصحح استئناف backlog قديم (`P5-003/007/011`).

## 5. الثوابت24 — معايير مطلوبة وليست اختبارات ناجحة

التفصيل وارتباط القبول والمصدر في [sync-invariants-05.csv](evidence/sync-invariants-05.csv). كل `runtime_status=not-executed`.

| الثابت | القاعدة | مرجع القبول المطلوب |
|---|---|---|
| INV5-01 | ملكية اتصال واحد وسياق جيل ثابت | لا callback أو مهمة من سياق سابق تكتب في السياق الجديد؛ الاتصال له مالك وعمر انتظار معلوم. |
| INV5-02 | الوصول يقاس عند الوجهة لا عند ICMP | LAN/WAN و broker و apply حالات مختلفة؛ فشل Ping خارجي لا يمنع وسيطاً داخلياً متاحاً. |
| INV5-03 | عقد نوع/معرف/وحدة قابل للتحقق | نموذج الطابور والمرسل والمستقبل متفق؛ يرفض الافتراضي 0 أو alias غير معروف ولا يتجاهل اختلاف schema. |
| INV5-04 | نية إرسال دائمة مرتبطة باعتماد الأصل | لكل تغيير معتمد سجل outbox/إصدار يمكن إعادته؛ لا clear عام أو إزالة failed/unknown. |
| INV5-05 | تنسيق بين العمليات ونجاة من restart | لكل سجل claim/lease وكتابة ذرية؛ interruption أو نسختان لا يفقدان أو يضاعفان التغيير. |
| INV5-06 | namespace ثابت للمستأجر/القاعدة/الوجهة | لا يتغير أصل/مالك الرسالة عند تغيير جلسة أو إعداد أو نقل مجلد الطابور. |
| INV5-07 | ACK بعد أثر معلوم بإصدار مطابق | فصل transport accepted عن locally committed وعن remotely applied ؛ unknown لا نجاح كاذب. |
| INV5-08 | سجل مواضيع وعقد dispatch واحد | كل ناشر له subscription ومعالج بشروط الأعلام نفسها؛ parser آمن للشكل والحروف. |
| INV5-09 | retained ليس سجل catch-up للدلتات | إثبات اكتمال snapshot أو replay cursor بعد غياب، لا الاكتفاء بآخر payload نوعي. |
| INV5-10 | غلاف لا يغير محتوى الأعمال | إزالة envelope لا تحذف أحرفاً من payload ؛ schema/context/integrity يتحقق منها صراحة. |
| INV5-11 | هوية أصل مستقرة لا رقم عرض/بادئة | هوية tenant+origin+doc/line/version ؛ parse صحيح وربط GL/warehouse بالهوية نفسها. |
| INV5-12 | اعتماد aggregate مكتمل أو حالة staging | رأس+أطفال+روابط/GL المطلوبة تتبع الإصدار نفسه؛ الفشل لا يترك جزءاً معتمداً غير معلن. |
| INV5-13 | منع downgrade وإحياء tombstone | رسالة أقدم/مكررة لا تعكس حذفاً أو إصداراً أحدث، و empty يحدد الأب والنطاق بوضوح. |
| INV5-14 | نشر سياسة صلاحيات/سحب ذري بالإصدار | كامل السياسة لكل principal لا صف يلغي السابق، وإعادة/empty/revoke تتقارب بأمان. |
| INV5-15 | upsert سيريال بالمفتاح نفسه | check/insert/update متطابقة الهوية والنطاق؛ duplicate/PK conflict معلنان لا catch صامتة. |
| INV5-16 | استيراد Android لا ينهي مصدره قبل الربط | local commit وروابطه مثبتة قبل received/delete/QR وتوليد GL من أصل عالمي صحيح. |
| INV5-17 | جدولة due و bootstrap واضحة | تاريخ قديم/انقطاع/نوع مزامنة لا يوقف catch-up أو يرسل خلاف mode معلن. |
| INV5-18 | cursor من نطاق جلب معتمد | لا تقدم عند فشل save أو اعتماد على ساعة جهاز كحد changes غير مقروءة؛ origin يمنع echo. |
| INV5-19 | تحديث تعريف وعضوياته فعلياً | الموجود والجديد والمنقول والمحذوف يطبقون حالة المرجع المختار؛ لا insert-only لسحب المنح. |
| INV5-20 | حذف/حياة التعاريف والعناصر التابعة متسقان | حقل الحذف والقائمة الفارغة و revive أو tombstone ينقلون وفق عقد معلوم لكل نوع. |
| INV5-21 | ApplyRemote لا يصبح PublishLocal عرضياً | لا إعادة دفعة كاملة لكل صف تنزيل؛ origin/version/outbox يمنعون الارتداد غير المقصود. |
| INV5-22 | لقطة مخزون كاملة بهوية موقع/وحدة وزمن | snapshot مقابل delta و empty وسكوب استبدال معلنون؛ لا صفوف مكررة أو وحدة 1 سحرية أو مخزن مهمل. |
| INV5-23 | حالة وتقارير صحة قابلة للمطابقة | علامة Sync واللون الأخضر لا يتجاوزان outcome ؛ partial/failed/unknown/backlog قابلة للرصد. |
| INV5-24 | دورة واحدة لكل قناة ومصفوفة triggers | Task lifetime منتظر و single-flight/cancellation ؛ نمط 3/4 له حد حدث معلن وجدولة اتجاهات معلومة. |

## 6. مصفوفة الفقد/التكرار/التأخر/التعارض36

[السجل الكامل](evidence/sync-failure-conflict-05.csv) يفرق الحد المصدر والأثر المحتمل والضابط/المجهول والنتيجة المطلوبة. الصفوف32–36 توسعات/متابعات مركبة، **لا خمس findings إضافية**. لا تعني كلمة failure أن حادثاً نفذ أو شوهد. كل `runtime_status=not-executed`.

| الحالة | الحد/الحدث | النتيجة المطلوبة والارتباط |
|---|---|---|
| FM5-01 — mqtt-client-lifecycle | فحص متكرر واتصال قديم ما زال يستقبل؛ تبدل client generation أثناء إرسال واستقبال متزامنين | عميل واحد أو انتقال واضح مع إبطال callbacks السابقة؛ P5-001 |
| FM5-02 — mqtt-internet-probe-gate | LAN فقط أو حجب ICMP؛ Ping يفشل والوسيط متاح عبر TCP | محاولة الوجهة الفعلية مع فصل WAN عن broker؛ P5-002 |
| FM5-03 — offline-item-queue-json-contract | استئناف ملف صنف سليم شكلاً خاطئ العقد؛ JSON يحوي itemid42 والقارئ يبحث عن id | قراءة 42 أو quarantine ؛ لا 0 ولا حذف صامت؛ P5-003 |
| FM5-04 — offline-outbox-atomicity-and-file-race | تعطل أو تسابق كتابة طابور؛ انقطاع بين commit و enqueue أو read/write من عمليتين | نية دائمة و claim/كتابة ذرية أو repair موثق دون فجوة؛ P5-004 |
| FM5-05 — offline-queue-context-namespace | تبديل قاعدة/عميل مع backlog؛ نفس Data ومعرف صنف محلي بمعنيين مختلفين | عزل namespace ورفض سياق غير مطابق دون clear؛ P5-005 |
| FM5-06 — mqtt-queue-clear-before-application-ack | انقطاع بعد النقل أو false قبل Publish؛ اعتماد broker لا SQL أو تخطي فحص داخلي | pending/failed/unknown تبقى حتى ACK تطبيق مطابق؛ P5-006 |
| FM5-07 — mqtt-publisher-subscriber-topic-drift | موضوع bare أو مختلف الحروف؛ Inv بلا slash و Entry/EntryGlobalID بدل entry/entryDetails | عقد واحد أو رفض مسبب لا فقد في catch؛ P5-007 |
| FM5-08 — mqtt-subscription-dispatch-flag-contract | تغيير أعلام اشتراك أو كيان غير مشترك؛ عمليات فقط مع Customers ؛ definitions مع Safe/Offer | subscribe و dispatch متطابقان لكل flag/كيان؛ P5-008 |
| FM5-09 — mqtt-retained-delta-not-backlog | مستقبل غائب عن دلتا صنفين؛ A ثم B على topic retained واحد | يلحق الاثنتين من snapshot/cursor لا آخر دلتا فقط؛ P5-009 |
| FM5-10 — mqtt-envelope-global-passcode-replacement | قيمة أعمال تحتوي passcode اصطناعياً؛ الاسم/الباركود يحتوي تسلسل الغلاف | فك الغلاف يحفظ payload حرفياً أو يرفض قبل SQL؛ P5-010 |
| FM5-11 — mqtt-origin-branch-prefix-identity | معرف فرع 10 أمام فرع 1 أو tenant-prefixed؛ StartsWith لا يقارن فرع الأصل الحقيقي | مقارنة origin typed وتوافق legacy بلا echo ذاتي؛ P5-011 |
| FM5-12 — mqtt-aggregate-detail-commit-boundary | رسالة طفل متأخرة وفشل وسط الاستبدال؛ رأس إصدار 2 وبنود 1 أو delete ثم insert جزئي | aggregate2 كامل أو staging/قديم كامل مع recovery ظاهر؛ P5-012 |
| FM5-13 — mqtt-permission-reset-inside-row-loop | إعادة سياسة صلاحيات بترتيب آخر؛ موظف واحد وصفوف 9/10 و 1/7 | سياسة متقاربة ذرية لا آخر صف وتراكم low-oper؛ P5-013 |
| FM5-14 — mqtt-serial-upsert-key-disagreement | رسالة سيريال مكررة؛ Id501 و ItemId42 ثم إعادة/تعديل | نفس predicate والهوية في check/insert/update؛ P5-014 |
| FM5-15 — http-received-ack-without-local-save-result | رفض/rollback محلي ثم تأكيد received؛ كاتب void يرجع مبكراً أو يبتلع failure | ACK وحذف المصدر لا يحدثان دون commit مطابق؛ P5-015 |
| FM5-16 — android-generated-ledger-document-link | رقم Android معاد بفرع آخر؛ lookup type+doc_no وربط رأس سبق حفظه فارغاً | SourceGlobalID→GL mapping فريد وروابط محفوظة قبل ACK؛ P5-016 |
| FM5-17 — master-sync-staleness-predicate | عودة فرع بعد غياب أكثر من ساعتين؛ شرط due مقلوب أمام CardsLastSync قديم | bootstrap/catch-up عند الاستحقاق لا توقفه القِدم؛ P5-017 |
| FM5-18 — master-sync-cursor-after-failed-or-racing-apply | فشل save وسط جلب تعاريف متعدد؛ bool=false لا يمنع ختم Now ؛ تغيرات بين الطلب والختم | apply+cursor معتمد وحد snapshot/sequence من الخادم؛ P5-018 |
| FM5-19 — employee-download-existing-row-no-update | تغيير موظف موجود أو نقل فروعه؛ AddedLocally=false يبقي COUNT ولا يجدّد العضوية | UPDATE فعلي وعضوية scoped أو failure معلن؛ P5-019 |
| FM5-20 — resource-membership-sync-does-not-revoke | سحب موظف من مخزن/خزينة؛ تنزيل false أو snapshot غاب منه زوج سابق | revoke/replace محدد بالإصدار؛ لا union دائم للمنح؛ P5-020 |
| FM5-21 — master-data-tombstone-and-child-removal-contract | حذف تعريف أو آخر تابع؛ IS_Deleted يصفر/يهمل أو empty لا يحمل إزالة | tombstone/empty/إحياء مصرح وفق عقد كيان محدد؛ P5-021 |
| FM5-22 — customer-download-full-batch-echo | تنزيل دفعة عملاء ثم تغير timestamp؛ SaveCustomer يعيد AddCustomer لكل صف دون انتظار | ApplyRemote لا ينشر المحلي ولا يخلق echo عرضياً؛ P5-022 |
| FM5-23 — stock-snapshot-replacement-contract | تكرار أو empty أو فشل snapshot مخزون؛ append في Active غير 4 ؛ cloud empty لا يدخل الكاتب | نسخة واحدة لكل مفتاح واستبدال scope معلن مع rollback/نتيجة؛ P5-023 |
| FM5-24 — cloud-stock-warehouse-filter-ignored | مخزنان للصنف/الوحدة نفسها؛ CalcProductStocks لا يستخدم @Inventory | رصيد مطابق للموقع؛ ambiguous/unavailable ليس 0 مقبولاً؛ P5-024 |
| FM5-25 — stock-snapshot-hardcoded-unit-identity | صنف وحدته الأساسية ليست 1؛ الناشر يثبت UnitId1 والقارئ يطابق وحدة الصنف | QuantityBase ووحدة هوية متفقة عبر القنوات؛ P5-025 |
| FM5-26 — cloud-batch-queue-cleanup-without-success-boundary | رفض دفعة cloud أو نجاح انتقائي؛ CLearfiles بلا شرط نجاح شامل وبلا IDs ؛ restore remaining فقط | إزالة المقبول فقط وبقاء rejected/unknown وغير المختار؛ SDK عقده مطلوب؛ P5-026 |
| FM5-27 — manual-sync-status-before-remote-ack | رفض API بعد تعليم الحالة محلياً؛ Sync1 قبل PostEntries/PostReceipts أو دون قناة | حالة كل إصدار من outcome لاحق لا من اختيار الصف؛ P5-027 |
| FM5-28 — sync-async-void-single-flight-session-fence | مؤقت ونقرة أثناء await/تبديل جلسة؛ async void/IsBusy لا يحجز عمر العمل والسياق static | single-flight و generation fence وإلغاء مع pending محفوظ؛ P5-028 |
| FM5-29 — sync-result-contract-false-and-unchecked-http-status | bool لا يطابق الرد أو GL ما زال جارياً؛ noncloud يرجع false و HTTP4xx قد true ؛ GL غير منتظر | نتيجة typed و HTTP/body مفحوص وعمر child معروف؛ P5-029 |
| FM5-30 — sync-ui-green-not-commit-health | فشل خفي مع لون أخضر؛ false/no-work/Thread start يعرض نشطة/نجاحاً | مؤشرات connection/progress/applied/failed/unknown مستقلة؛ P5-030 |
| FM5-31 — sync-mode-schedule-read-interval-contract | نهاية وردية/يوم مع tick أولي؛ SyncType>0 يرسل مباشرة ويستعمل PostInterval للكل | مصفوفة mode×trigger×direction مطابقة للسياسة المعلنة؛ P5-031 |
| FM5-32 — HTTP/MQTT-replay | رسالة مالية قديمة بعد حذف/إصدار أحدث؛ upsert يكتب حالة IS_Deleted/البنود دون expected version أو inbox ظاهر | رفض الأقدم/المكرر أو تسوية تعارض مصرح بها بسجل؛ tombstone لا ينعكس بسبب ترتيب الوصول؛ P3-006;P5-012;P5-021 |
| FM5-33 — HTTP-branch3-receipt-relay | وصول سند إلى فرع وسيط؛ يضبط DistBranch/BranchType/Received=false في الكائن ثم يدعو UpdateReceiptAsyncreceived بالـ IDs فقط | عقد route/ACK موثق واختبار نهايتين قبل cleanup ؛ المجهول blocked لا passed؛ H5-01;P5-015 |
| FM5-34 — MQTT-empty-children | حذف آخر طفل من aggregate؛ مفتاح الحذف يستنتج من عناصر القائمة؛ foreach لقائمة empty لا يفعل شيئاً | envelope يحوي parent+scope+version مع empty صريحة واعتماد وحدة كاملة؛ P5-012;P5-021 |
| FM5-35 — HTTP-master-clock | ساعة جهاز متقدمة أو تحديث أثناء الجلب؛ ختم DateTime.Now بعد طلبات تستخدم watermark السابق؛ لا snapshot token وارد ظاهر | cursor من server snapshot بعد تطبيق كل الصفحات أو overlap مع dedup ومنع تقدم عند فشل؛ P5-018 |
| FM5-36 — Cloud-POS-cache | تعديل/إعادة حفظ بعد تنزيل snapshot أو فشل DTO cast؛ POS يدعو UpdateItemsQty بعد نجاح SQL ؛ المساعد يطرح/يزيد كامل item.Quantity قراءة ثم كتابة دون operationversion | توثيق DTO/sourceoftruth ثم delta بإصدار/إعادة بناء cache ؛ لا تعويض أرصدة أو افتراض تكلفة/وحدة غير معلومة؛ H5-03;P5-023;P5-025 |

## 7. أسئلة العقد والسياسة المفتوحة Q5

هذه طلبات سياق للمالك/المكونات الخارجية، **لا مطالبة بأسرار أو بيانات إنتاج ولا شروط لبدء6 بلا إذن**. المجهول يبقى معلناً، ولا يصنف فجوة مستودع جديدة لمجرد عدم توفر server/SDK.

| السؤال | المجال | ما يلزم حسمه | المالك/الحد |
|---|---|---|---|
| Q5-01 | ملكية وتعارض الكيانات | أي كيان مركزي وأي كيان يملكه الفرع/الجهاز؟ هل يسمح تعديل أصل مالي من جهتين أو revive بعد الحذف؟ ما expected version والحل المصرح وحفظ التاريخ؟ | مالك المنتج/المحاسبة والأمن؛ OWN5-01 إلى OWN5-07؛ P3-006. |
| Q5-02 | الهوية وعقد الرسالة | ما namespace المستأجر/قاعدة البيانات/الفرع والجهاز؟ كيف تهاجر Branch-No إلى Client-Branch-No والـraw IDs؟ ما schema/topic/envelope الإصدار وmapping السيريال/الوحدات؟ | معمارية وخادم؛ INV5-03/06/08/10/11؛ لا أسرار مطلوبة. |
| Q5-03 | سياسة broker والتوثيق والنقل | ما نسخة M2Mqtt وsession/retained/persistence limits وTLS/auth/ACL الفعلية؟ هل broker LAN مدعوم بلا WAN؟ كيف تتوقف callbacks القديمة وتستعاد الاشتراكات؟ | تشغيل/أمن؛ P1-014 وP5-001/002/008/009؛ لا تفحص إعدادات إنتاج هنا. |
| Q5-04 | عقد SDK/API والـACK | ما Add*/PostPeriodically/UpdateReceived/RemoveReceived/CLearfiles فعلياً؟ per-item أم دفعة ذرية؟ scope queue وديمومتها/SQL rebuild، server idempotency، والـreceipt relay بالـID؟ | مصدر/وثائق SDK أو fakes معتمدة؛ H5-01 وP5T-35/54/55/56؛ غياب العقد يبقي الجزء blocked. |
| Q5-05 | Android وهوية GL/العميل المؤقت | ما enum/types20/10 ووقت/مالك توليد GL وmapping الأصل؟ متى يحذف العميل المؤقت وما retention للمستند/QR؟ كيف يربط الرفض المحلي دون إنهاء source؟ | المنتج/المحاسبة/تكامل6؛ P5-015/016؛ لا إقرار ZATCA أو إرسال ضريبي هنا. |
| Q5-06 | حد التغييرات والساعة | هل lastTime مرشح updated-since؟ inclusive أم exclusive، UTC أم محلي، صفحات وsnapshot token، retention وbootstrap/full repair؟ كيف يحسب clock skew وحد الجلب؟ | API وبيانات؛ P5-017/018 وINV5-17/18؛ لا تفترض دلالة الوقت من اسم الحقل. |
| Q5-07 | الأوضاع والجدولة وإعادة المحاولة | ما matrix mode×trigger×direction المعلنة لـ3/4 وReading/PostIntervals؟ طول الانقطاع المدعوم، backoff/jitter وsingle-flight وإلغاء تبديل الجلسة؟ | منتج/تشغيل؛ P5-028/031 وP2-003؛ عودة الشبكة لا تعني إعادة كل حدث عشوائياً. |
| Q5-08 | رصيد المخزون/الحساب وقيم snapshot | هل ProductStocks snapshot كاملة أم delta وبأي scope وcomplete/empty/version؟ UnitId/QuantityBase/AvgCost وItems↔InvoiceItems وعقد تعديل POS؟ هل SaveAccounts الذي يكتب IValue=0 مقصود لأن افتتاحي الحساب مشتق من GL؟ | محاسب/بيانات/DTO؛ H5-03 وP5-023 إلىP5-025؛ لا تعد IValue=0 خسارة رصيد مثبتة دون تعريف الحقل. |
| Q5-09 | سياسة نشر المستخدمين والسحب | من يملك principal IDs والمنح وعضوية الموارد؟ هل الحمولة snapshot أم grant/revoke، وما SLA لإبطال جلسة/أوفلاين وسجل before/after ومنع downgrade؟ | أمن ومنتج؛ P5-013/019/020 وP2-003/011؛ لا كلمات مرور أو بيانات شخصية في الدردشة. |
| Q5-10 | التشغيل والتسوية والاحتفاظ | ما قواعد Pending/Accepted/Applied/Rejected/Unknown ومطابقة العدد/البصمات وdead-letter/quarantine؟ من يجيز repair وإعادة الإرسال المالي/الحذف، RPO/RTO ومدة inbox/tombstone وحماية سجل المحاولات؟ | تشغيل/أمن/محاسب؛ H5-04 وP5-004/006/026/027/030؛ الاختبار8 بإذن منفصل. |

## 8. المتابعات المحددة H5 — غير معدودة findings جديدة

| المتابعة | الملاحظة المحددة | قرار الحدود والاستكمال | قبول مستقبلي ومصدر |
|---|---|---|---|
| H5-01 — عقد SDK/cloud/relay | موضع CLearfiles خارج النجاح مثبت لكن نطاقه/إعادة البناء مجهولان؛ receipt relay يغير DTO ثم يمرر IDs. provider partial وcloud-first/SQL boundary تحتاج عقداً. | P5-026 potential باقية؛ لا finding إضافي لـrelay/ازدواج بعيد دون العقد. مراجعة الواجهة المحلية5 مكتملة ضمن الحدود؛ العقد في6 والقبول8. | `P5T-35`، `P5T-54`، `P5T-55`، `P5T-56`؛ `SmartAuditERP/Class/Sync.cs:412-460`؛ `SmartAuditERP/Class/Sync.cs:600-685`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2168-2211` |
| H5-02 — الوصول الفعلي والبدائل الخاملة | FrmSyncMQtt خلف new Home؛ يرسل components تحت ItemSerialNo. FrmSyncInv/FrmSyncSettings وGetCustFromAndroid.StartConnection وfrmInvSale.AddInvLocally بلا caller مثبت في بحث المستودع؛ GetDataAPI مثال PM. | لا تعد خمول هذه الأجسام نقلاً حياً أو إصلاحاً لـP3-014؛ P1-017 الأصل للبوابة وH3-02/P1-033 باقية. حسم وظيفة/وصول7 وقبول8. | `P5T-17`، `P5T-19`؛ `SmartAuditERP/Form_WPF/FrmSyncMQtt.xaml.cs:40-65`؛ `SmartAuditERP/Form_WPF/FrmSyncInv.xaml.cs:1-196`؛ `SmartAuditERP/Form_WPF/FrmSyncSettings.xaml.cs:1-163`؛ `SmartAuditERP/Class/GetCustFromAndroid.cs:1-69`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2483-2499`؛ `SmartAuditERP/Form_WPF/frmNewProjectPM.xaml.cs:38-49` |
| H5-03 — دلالة DTO وcache/التكلفة/الافتتاحي | POS quantity يأتي بعد نجاح SaveInvoice؛ إذا وصل DTO المطلوب يطبق كامل quantity لا operation delta، snapshot لاحقة قد تستبدله. Items وInvoiceItems/setters والـAvgCost وIValue ليست عقودها متاحة. | لا ننسب تكرار خصم أو ضياع افتتاحي فعلياً؛ لا يضاعف P4-014 أو P5-023/025. يلزم Q5-08 وDTO/سياسة ثم اختبار8، دون تعويض أرصدة. | `P5T-49`، `P5T-50`، `P5T-53`؛ `SmartAuditERP/Form_WPF/frmInvPOS.xaml.cs:2269-2288`؛ `SmartAuditERP/Class/Inventory.cs:266-315`؛ `SmartAuditERP/Class/Inventory.cs:632-655`؛ `SmartAuditERP/Class/EntityOperations.cs:1588-1628` |
| H5-04 — قبول طرفي واستعادة معزولة | لا مصدر broker/API ولا مخطط نشر وبيئة Windows أو سجلات حقيقية؛ جدول الفشل والخطط ليسا replay تجريبياً. سياسة السلطة/الحذف/السحب/retention لم تحسم من العميل. | كل P5T not-executed؛6 تكاملات و7 اكتمال/واجهة و8 تشغيل بإذن مستقل. H4/Q4 لا تنفى قدراتها من هذا التدقيق. | `P5T-03`، `P5T-14`، `P5T-28`، `P5T-31`، `P5T-59`، `P5T-60`، `P5T-62`؛ `SmartAuditERP/SmartAuditERP.csproj:29-31`؛ `SmartAuditERP/SmartAuditERP.csproj:149-151`؛ `SmartAuditERP/Class/ClosingReport.cs:27-102` |

## 9. معيار انتهاء5 وما يبقى

تتبع القنوات والملكية والمواضيع وحالات التعطل/الإعادة/الحذف وسياق الجلسة ضمن النطاق المعلن اكتمل ساكناً؛ لا اعتماد تشغيلي للأوفلاين. كل137 نتائج الشيفرة مفتوحة، وكل64 خطة قبول5 غير منفذة. لا يلغي ذلك غياب اختبار بناء/SQL فعلي في1–4 أو H4/Q4/H3 الباقية. [VALIDATION-05.md](VALIDATION-05.md) يحدد أمان وبيئة الأدلة اللاحقة.

**6–8 لم تبدأ؛6 تحتاج إذناً جديداً.** لا تعديل تطبيق أو تنفيذ repair/clear/replay أو تشغيل broker/API/مزود أو commit/push ضمن هذا التسليم.
