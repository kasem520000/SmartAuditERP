# التحقق والأمثلة وخطط القبول — المرحلة6

**مرجع التدقيق:** 2026-11-16 (UTC) — **الفرع:** `arena/94ae8414-smartauditerp`  
**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`.

**انتهت المرحلة6 كمراجعة ساكنة للنطاق المعلن، لا كتصديق تشغيل أوامتثال. سُلّمت المراحل1–6 توثيقياً؛ المرحلة7 لم تبدأ وتحتاج إذناً جديداً. لم تنفذ إصلاحات أوbuild/Windows/WPF/SQL أوتحميل وتشغيلDLL أواتصالات تشغيلية بمزود/جهاز/ضريبة/دفع/WhatsApp/SMTP/دعم/ترخيص. كل قبول تطبيقي مقترح هنا غير منفذ.**

تاريخ مرجع الجلسة المعلن هو2026-11-16. أظهرت ساعة بيئة التوثيق2026-11-17؛ سجل هذا الاختلاف وتاريخ جلب المراجع العامة منفصلين في provenance06 وسجل المراجع. لا يمثل أي منهما اختبار تطبيق/مزود أوتغيير ساعة/رخصة. تواريخ وحزم1–5 التاريخية محفوظة.

[التقرير والنتائج](PHASE-06.md) · [عقود التكامل والثوابت وحالات الفشل](INTEGRATIONS-06.md) · [التحقق وخطط القبول](VALIDATION-06.md) · [السجل التراكمي](findings.csv) · [الفهرس](README.md) · [النواقص والتوصيات](IMPROVEMENTS.md).

## 1. ما نفذ فعلاً وما لم ينفذ

نفذ حصر وبصمات ومراجعة مصدرية وقراءة مراجع عامة وبناء حزمة تدقيق وفحوص اتساقها بواسطة Python/Git. **لاbuild أوERP/C#/VB/Newtonsoft/SQL/SDK/native/browser/SMTP/provider acceptance**. لا استغلال أوتغيير ترخيص/ساعة أواستعمالPAN أوإرسال ضريبة/دفع/رسالة أوتشغيل بطاقة/طابعة. HTTP في المراجع وصف لوثيقة عامة لا طلب تشغيلي إلى خادم العمل.

| الفحص المحلي الآمن | المعنى والحد |
|---|---|
| collect_baseline.py --verify | يقارن827 ملفاً أصلياً وبصماتها؛ لا يستبدلbaseline ولا يقيس التغطية الدلالية. |
| validate_audit.py --through-phase 5 عند الدخول | 137 نتيجة و827 بصمة وerrors[] قبل إنشاء6. checks05 التاريخية لم تستبدل. |
| لقطة الدخول وprovenance06 | 137 صفاً؛ SHA256:6dc63d157f05a25f1f7b580bbe8ee843b2c61267e18c13219905d4ce0073006c. حميت53 artifact من1–5 ببصماتها. |
| check_integration_witnesses.py | 14 توضيحاً رياضياً/حالة مفترضة منقولة يدوياً، و7 فحوص نصية منفصلة. لا استدعاءC#/SQL/مزود. |
| validate_audit.py الافتراضي حتى6 | 172 نتيجة ومعرفات وروابط وحدود أسطر واحتواءscopes؛ عقود14 وثوابت32 وحالات48 وخطط80 ومراجع15 وروابط عكسية وإعادة التوضيحات. لا خروج شبكة. |
| --through-phase 2 / 3 / 4 / 5 | يقرأ لقطات49/74/106/137 المجمدة والتقارير التاريخية؛ الفهرس المشترك الحالي ليس بديلاً لسجل تاريخي. لا يستبدلchecks القديمة. |

المخرجات الفعلية للفحص الأخير في [checks-06.json](evidence/checks-06.json). تكرار الإحالات والروابط يقيس اتساق التوثيق، لا قراءات فريدة أوصحة مالية أوتغطيةWPF. لا تكتب الأداة أدلة، ولا تفحص كل قواعد اللغة/المنطق، وملفchecks لا يبصم نفسه. الفحص التاريخي بهذه الأداة المحدثة لا يعني تطابقJSON الجديد حرفياً معchecks القديمة أوإعادة تشغيل التطبيق.

## 2. أمثلة مستقلة وملاحظات مصدرية منفصلة

المدخلات الاصطناعية والأرقام والمخرجات والافتراضات والحدود والدليل محفوظة في [integration-witnesses-06.json](evidence/integration-witnesses-06.json). لا تتضمن تزوير رخصة أوtax/payment simulation للمورد؛ هي أمثلةPython منطقية لا تعيد تقييمSDK/setters/Math.Round بالكامل.

| المعرف | التوضيح المستقل | النتائج | الحد |
|---|---|---|---|
| ALG6-01 | Different VAT predicates | P6-001 | ASCII predicate transcription only. Not Customer DTO, SQL, taxpayer validation or a real invoice-type decision. |
| ALG6-02 | Two positive rates share one allowance object | P6-003 | Two stipulated positive-rate groups; not proof the business uses mixed rates or that an SDK serializes the object unchanged. |
| ALG6-03 | Early quantity/price rounding and midpoint distinction | P6-004 | Exact Python Decimal illustration, NOT .NET double-to-decimal, Math.Round binary midpoint behavior, SDK arithmetic or tax approval. |
| ALG6-04 | Per-type previous number under a shared issuing unit assumption | P6-005 | Conditional list model only; EGS/POS boundaries, numbering policy, actual hashes and external UUID generation are unresolved. |
| ALG6-05 | No-error predicate is not an explicit accepted-state predicate | P6-006 | A synthetic response shape, not a claim the SDK can emit it or that its defaults have been executed. |
| ALG6-06 | ETA invoice quantity can become zero while value is nonzero | P6-013 | Arithmetic transcription for an unambiguous non-midpoint input; not execution of the external InvoiceLine setter or wire serializer. |
| ALG6-07 | Reference comparison becomes Boolean text | P6-014 | Python Boolean spelling illustrates the comparison, not a call to Microsoft.VisualBasic Conversions or SDK reference normalization. |
| ALG6-08 | Date truncation and a literal Z are not UTC conversion | P6-015 | Stipulated offset and exact datetime illustration only; no machine clock, C# culture/Kind, timezone database or receipt serializer tested. |
| ALG6-09 | Opposite local Boolean outcome contracts | P6-016، P6-017 | Manual control-flow summary only; the SDK status string is NOT assumed to be raw HTTP. No API call, tables or persistence executed. |
| ALG6-10 | Receipt pre-tax line total versus final ERP Net | P6-018 | A minimal stipulated financial fixture; not evidence of actual DTO recalculation, serialized payload, ETA rejection or accounting certification. |
| ALG6-11 | Conditional remote side effect before a local rejection | P6-020، P6-021 | Hypothetical schedule, NOT a double-charge proof, actual terminal invocation, vendor idempotency result or concurrency test. |
| ALG6-12 | Empty mapping selection skips the replacement block | P6-023 | Sequential list effect only, not SQL constraints/transactions/triggers, cloud routing or an actual account mapping change. |
| ALG6-13 | Fixed last-verified fallback does not advance | P6-027 | Stipulated cache and failed-NTP branch only; no real license, AES/hash generation, file modification, clock/NTP operation or entitlement bypass executed. |
| ALG6-14 | Prefix-only phone transformation | P6-032 | Text markers deliberately not dialable; not E.164 validation, WhatsApp URL handling, contact existence or actual misdelivery. |

| المعرف | فحص نصي لا اختبار تطبيق | النتائج | الحد |
|---|---|---|---|
| ST6-01 | Ticket details object is discarded at the local boundary | P6-024 | Literal source observation, not JSON deserialization or UI/NRE execution; remote response schema is unknown. |
| ST6-02 | Fresh ZATCA credential INSERT text shapes | P6-011 | Bounded string/parameter-name extraction only, not SQL parsing/execution, schema/ABI checking, reachability of count==0 or a migration test. No credential values emitted. |
| ST6-03 | Different ETA local return contracts | P6-016، P6-017 | Literal selected-method observation only; external SDK control flow, enums, HTTP semantics and actual tables not executed. |
| ST6-04 | Terminal call and selected validation textual order | P6-020، P6-021 | Text order in selected methods, not WPF event/interleaving analysis, vendor approval or proof every input reaches these branches. Prior rem guard explicitly retained. |
| ST6-05 | Manual flag has a real contract consumer | P6-002 | Bounded lexical presence/absence, not proof of global non-use, runtime cache behavior or all external/reflection-based readers. |
| ST6-06 | Direct-call search separates sample/unused helpers from active test caller | P6-021، P6-022، P6-029، P6-030 | Regex over tracked C# only (including comments), NOT semantic call graph, complete-file manual review, external/reflective/generated caller exclusion or runtime reachability certification. |
| ST6-07 | Conditional Android double dispatch with ordinary-path counterexample | P6-035 | Branch text only; Type==3, printer/report/ActiveAuto/internet and earlier lifecycle guards are required. Not SMTP or report execution, nor a claim every close sends twice. |

**تنبيهات تفسير:**

- مثالrounding يستعملDecimal دقيقاً لا.NET double binary؛ ومثال التصنيف قواعد نصية لاCustomer/runtime. مرجعBoolean منقول من شرط المقارنة لا باستدعاءVB.
- نموذج تكرار الدفع مشروط بجدول افتراضي ولا يبرهن وقوع خصمين أوغيابidempotency عند المورد.
- direct-call regex تبحث tracked C# بما فيه التعليقات؛ لا تستبعدreflection أوgenerated/external callers ولا تحول كل الملفات إلىmanual scope.
- فحصSQL أعداد وأسماء معاملات فقط، لاparser أوتنفيذ أومخطط تطبيق. كل مثال له حد مستقل ولا يغلق نتيجة.

## 3. بوابات قبول مقترحة — كل الخطط80 غير منفذة

1. **تحضير:** عقد/version ودليلDTO/SDK/ABI/endpoint وسياسة ضرائب ومال وأدوار وخصوصية. إن غاب العقد يبقى قبولvendor محجوباً. يلزم مصدر بناء موثوق؛ binary المستودع ليس دليلاً على بناء نسخته الحالية.
2. **Mock/contract:** بيئةWindows/WPF/SQL اختبارية بإذن مستقل عند الحاجة؛fake بالعقد الموثق، وحظرoutbound للإنتاج، وclock/FS/WebDriver وSMTP sink وbarriers/faults اصطناعية. مقارنة بمرجع يقره المحاسب/المالك؛ نجاحmock ليس ضمانvendor.
3. **Sandbox:** إذن منفصل للمزود والتاجر/المكلف والجهاز المحددين؛ اعتمادات اختبار مدارة خارج الدردشة وsnapshots وآثار منقحة. لا حسابات أورسائل أوضريبة أودفعات إنتاج. لا يبدأ الاختبار لمجرد اسمtest في الواجهة.
4. **تشغيل8:** مرشح معالجة مأذون ومصفوفة بناء/نشر/SQL وتعافٍ وrollback وصلاحيات ومطابقة مالية قبل ادعاء النجاح أوالإغلاق. logs تثبتoperation/tenant/version والأصل والنتيجة النهائية دونsecret/PAN.

[acceptance-tests-06.csv](evidence/acceptance-tests-06.csv) المرجع التفصيلي: لكل صفscenario وprerequisites وprocedure وacceptance_criterion وsafety_controls ودليل وربطINV/INT. هذا فهرس مراجعة لا قائمة اختبارات ناجحة.70 خطة بواقع اثنتين لكل نتيجة جديدة و10 للحدود المشتركة؛ يمكن تفصيل الخطة الطرفية عند إعداد البيئة دون تحويلها بأثر رجعي إلى اختبارات منفذة هنا.

| المعرف | الحالة أوالموضوع | العقود والثوابت | معيار قبول مختصر | الحالة |
|---|---|---|---|---|
| P6T-01 | رقم ضريبي غير فارغ لا يستوفي قاعدة الحارس | INT6-01 / INV6-01، INV6-02 | قرار نوع وتوقيت واحد أو رفض صريح قبل الإصدار، لا standard بعد حفظ مسار simple. | not-executed |
| P6T-02 | فشل قراءة العميل لا يخفض نوع المستند | INT6-01 / INV6-01، INV6-02 | فشل قابل للتشخيص بلا fallback إلى simplified وبلا طلب مزود. | not-executed |
| P6T-03 | مصفوفة Auto/Manual للفاتورة والعقد وAndroid | INT6-01، INT6-02، INT6-13 / INV6-02، INV6-03 | سلوك معلن متوافق واستثناءات clearance موثقة، لا إرسال غير مقصود. | not-executed |
| P6T-04 | إيقاف وتشغيل بنفس الجلسة | INT6-01، INT6-02، INT6-13 / INV6-02، INV6-03 | لا انفصال بين رسالة الحالة والبوابة؛ يؤثر التغيير في الجيل الصحيح فقط. | not-executed |
| P6T-05 | فئات الضريبة وصفرها والعملة والبلد | INT6-01 / INV6-04، INV6-06 | category/reason/country/currency صحيحة أو unsupported صريح؛ ليس الصفر أدوية عموماً. | not-executed |
| P6T-06 | خصم مستند بمعدلين مختلفين | INT6-01 / INV6-04، INV6-06 | breakdown لكل category/rate والنتيجة لا تتبدل بترتيب السطور. | not-executed |
| P6T-07 | كمية وسعر بدقة أعلى ومنتصف التقريب | INT6-01 / INV6-05، INV6-06 | الكمية والسعر محفوظان؛ amounts فقط تقرب وفق القاعدة المعتمدة وتتطابق مع الأصل. | not-executed |
| P6T-08 | مقام صفري وقيم غير منتهية | INT6-01 / INV6-05، INV6-06 | رفض مبكر مسبب أو معالجة بسياسة معتمدة بلا division/nonfinite. | not-executed |
| P6T-09 | فاتورة ومرتجع وعقد على وحدة إصدار واحدة | INT6-01، INT6-04 / INV6-07، INV6-08 | ICV/PIH/previousUUID تخص آخر مستند بالوحدة، لا النوع ناقص1 فقط. | not-executed |
| P6T-10 | إعادة بعد ضياع الرد ومحمل المتابعة | INT6-01، INT6-04 / INV6-07، INV6-08 | هوية/hash/payload ثابتة، previousUUID لا يفقد، وQuery يحسم Unknown قبل إصدار جديد. | not-executed |
| P6T-11 | رد بلا أخطاء وبلا حالة قبول نهائية | INT6-01، INT6-02 / INV6-09، INV6-10 | لا Sent إلا لحالة مقبولة مرتبطة بالمستند؛ pending/unknown ليسا قبولاً نهائياً. | not-executed |
| P6T-12 | فشل استخراج QR وغلاف الاستجابة | INT6-01، INT6-02 / INV6-09، INV6-10 | الأصل يبقى، وينقل الخطأ من الرد الحقيقي دون null dereference أو نجاح كاذب. | not-executed |
| P6T-13 | clearance ناجح ثم فشل حفظ محلي | INT6-01 / INV6-11، INV6-12 | محاولة معلومة قابلة للمطابقة، لا إجازة أو دفعة جديدة ولا ادعاء rollback بعيد. | not-executed |
| P6T-14 | simplified بعد commit وتثبيت النتيجة | INT6-01 / INV6-11، INV6-12 | معاملة جديدة صحيحة للنتيجة، لا completed transaction أو محو الأصل السابق. | not-executed |
| P6T-15 | إرسال يدوي ثم تحميل وطباعة | INT6-01، INT6-14 / INV6-12، INV6-13 | metadata والأرشيف والعرض لنفس النسخة المقبولة، لا علامة Sent مع hash فقط. | not-executed |
| P6T-16 | فشل إعلام Android بعد تثبيت القبول | INT6-01، INT6-14 / INV6-12، INV6-13 | نية إعلام دائمة قابلة للإعادة دون إعادة إصدار المستند الضريبي. | not-executed |
| P6T-17 | اختيار عقد بلا صف Inv | INT6-01 / INV6-10، INV6-13 | المحمل والكاتب مصدرهما العقد أو unsupported واضح، لا تجاهل صامت. | not-executed |
| P6T-18 | GlobalID متساوٍ نصياً بين مصدرين | INT6-01 / INV6-10، INV6-13 | لا cross-target، وتقرير كل صف يذكر المصدر والنتيجة. | not-executed |
| P6T-19 | فشل Generate أو OTP مرحلياً | INT6-02 / INV6-14، INV6-15 | يتوقف التدفق ويحفظ last-known-good ولا Saved/Active بعد الفشل. | not-executed |
| P6T-20 | تغيير إعداد لا يمحو اعتماد إنتاج | INT6-02 / INV6-14، INV6-15 | لا CSR جديد دون قصد، ويرفض عدم تطابق المفتاح/EGS دون استبدال الصالح. | not-executed |
| P6T-21 | قاعدة فارغة وفرع PCSID | INT6-02 / INV6-15 | عدد الأعمدة والقيم والمعاملات متوافق وصف واحد صحيح أو رفض قبل أي طلب بعيد. | not-executed |
| P6T-22 | استيراد fresh وexisting | INT6-02 / INV6-15 | لا INSERT مشوه أو تجاهل تحذير مانع، ولا مفتاح صالح يستبدل بملف غير متحقق. | not-executed |
| P6T-23 | مصفوفة البيئة وغرض الشهادة | INT6-01، INT6-02 / INV6-01، INV6-14 | لا خلط إنتاج وcompliance، والجمع غير المعروف مرفوض. | not-executed |
| P6T-24 | EGS وشركة أخرى وشهادة منتهية | INT6-01، INT6-02 / INV6-01، INV6-14 | رفض scope mismatch والانتهاء قبل الشبكة؛ لا select-first أو credential fallback. | not-executed |
| P6T-25 | فاتورة بكمية0.4 و2.75 | INT6-03 / INV6-05، INV6-06 | كمية دقيقة وموجبة، وsalesTotal/netTotal من نفس القيم دون صفر مصطنع. | not-executed |
| P6T-26 | عقد DTO لا يدعم دقة النشاط | INT6-03 / INV6-05، INV6-06 | unsupported صريح أو ترقية عقد معتمدة، لا cast فاقد للبيانات بصمت. | not-executed |
| P6T-27 | مرجع مرتجع فارغ وغير فارغ | INT6-03، INT6-04 / INV6-16 | يمر مرجع الأصل المتحقق لا True/False؛ الحقل المعلوماتي ليس بديلاً عن references. | not-executed |
| P6T-28 | مرتجع إيصال من Sale أوPOS | INT6-03، INT6-04 / INV6-16 | lookup typed يختار الأصل وUUID والحد المتبقي الصحيحين. | not-executed |
| P6T-29 | وقت قرب منتصف الليل وoffset مختلف | INT6-03، INT6-04 / INV6-17 | لا فقد عبر ToShortDateString؛ الوقت والتاريخ UTC يعودان إلى Instant نفسه. | not-executed |
| P6T-30 | ثقافة وتوقيت صيفي | INT6-03، INT6-04 / INV6-17 | serialization UTC موحدة ورفض/تفسير الوقت المبهم؛ لا Z شكلية. | not-executed |
| P6T-31 | قبول أولي وجزئي وجداول ناقصة | INT6-03 / INV6-09، INV6-10، INV6-12 | هوية وsubmission محفوظان، Pending ليست Final، ولا قراءة Rows[0] دون تحقق. | not-executed |
| P6T-32 | نتيجة دفعة فواتير بعد قبول صف | INT6-03 / INV6-09، INV6-10، INV6-12 | لا false دائمة توقف المقبول ولا نجاح عام؛ أعداد كل حالة والمتبقي واضحة. | not-executed |
| P6T-33 | حالات SDK للإيصال دون افتراض HTTP | INT6-04 / INV6-09، INV6-10 | الرفض لا يصبح true، ولا Sent بلا قبول وهوية صحيحة، مع متابعة نهائية. | not-executed |
| P6T-34 | زر Sale ينتظر ومتابعة تفصل الفشل | INT6-04 / INV6-09، INV6-10 | single-flight وانتظار/نتيجة UI دقيقة، لا نجاح عام بعد break فاشل. | not-executed |
| P6T-35 | إيصال أساس100 وضريبة15 | INT6-04 / INV6-06 | netAmount100 وtotal115 ومجموع صافي البنود مطابقون للمعنى الرسمي. | not-executed |
| P6T-36 | خصم بند ورأس واستقطاع | INT6-04 / INV6-06 | taxTotals تساوي ضريبتها بالبند وcommercial discount يطابق التفاصيل دون عد مزدوج. | not-executed |
| P6T-37 | التقاط وجهة preprod دون شبكة | INT6-04 / INV6-14 | وجهة معتمدة لكل بيئة/وظيفة أو دليل SDK موثق عن override محدد. | not-executed |
| P6T-38 | TLS واسم شهادة اختبار | INT6-04 / INV6-14 | نجاح فقط للـhost/chain المعتمدين، ولا نقل preprod root إلى إنتاج. | not-executed |
| P6T-39 | مبلغ غير صالح لا يستدعي الجهاز | INT6-05 / INV6-11، INV6-18 | call count0 لكل مدخل غير صالح؛ حارس rem لا يغني عن بقية الفحوص. | not-executed |
| P6T-40 | المبلغ يتغير بين التحضير والتثبيت | INT6-05 / INV6-11، INV6-18 | لا اعتماد بمبلغ آخر أو إعادة بيع؛ تعارض إصدار يحال للمطابقة أو تعويض مخول. | not-executed |
| P6T-41 | نقر وEnter متزامنان | INT6-05، INT6-06 / INV6-19، INV6-20، INV6-21 | محاولة دائمة واحدة والثانية ترتبط بها؛ لا SALE جديدة لنفس النية. | not-executed |
| P6T-42 | قبول الجهاز وضياع الرد وفشلDB | INT6-05، INT6-06 / INV6-19، INV6-20، INV6-21 | Unknown تبقى حتى المطابقة قبل retry؛ مقبوض واحد ولا PAN/raw غير ضروريين. | not-executed |
| P6T-43 | اختبار الإعداد محايد مالياً | INT6-05، INT6-06 / INV6-14، INV6-18، INV6-20 | health ليس SALE؛ الاختبار المالي المعلن يحتاج تأكيداً وsandbox وIntent بالمبلغ الصحيح. | not-executed |
| P6T-44 | رد Neo مؤجل ثم رفض | INT6-05، INT6-06 / INV6-14، INV6-18، INV6-20 | await وOutcome دقيقة ومنع نقر ثانٍ، ولا استعمال سر مضمن. | not-executed |
| P6T-45 | حذف آخر ربط بنك | INT6-14، INT6-08 / INV6-22 | Empty محفوظة ولا صف قديم يرسل؛ Saved تطابق القاعدة. | not-executed |
| P6T-46 | فشل وسط استبدال mapping | INT6-14، INT6-08 / INV6-22 | rollback للنسخة كاملة أو منع الفعل السحابي؛ لا مزيج نسخ أو تصادم هوية. | not-executed |
| P6T-47 | تفاصيل تذكرة صحيحة | INT6-11 / INV6-10، INV6-29 | DTO كامل وحقول معروضة بلا NRE وهوية تذكرة مطابقة. | not-executed |
| P6T-48 | تفاصيل ناقصة أو ممنوعة | INT6-11 / INV6-10، INV6-29 | لا Success بلا Ticket، وأسباب مميزة دون كشف تذكرة تخص غير المستخدم. | not-executed |
| P6T-49 | HTTP200 مع رفض أعمال | INT6-11 / INV6-10، INV6-29 | لا نجاح أوClearForm؛ الرفض ظاهر والمسودة ومرفقاتها الحالية محفوظة. | not-executed |
| P6T-50 | اسم يحوي &/# وقائمة فاشلة | INT6-11 / INV6-10، INV6-29 | اسم واحد صحيح مرمز، وEmpty مميزة عن Failed/Unauthorized، لا retry غير محدود. | not-executed |
| P6T-51 | توقيع جهة اختبار غير موثوقة | INT6-12 / INV6-01، INV6-30 | رفض قبل Features؛ لا SHA عام كإثبات مصدر الاستحقاق. | not-executed |
| P6T-52 | رخصة لجهاز أوشركة أخرى | INT6-12 / INV6-01، INV6-30 | ممنوعة على السياق الآخر، ونقل الرخصة المخول إجراء مستقل مؤرخ. | not-executed |
| P6T-53 | NTP فاشل وanchor قديم | INT6-12، INT6-13 / INV6-31 | الوقت/grace يتقدمان ولا يتجمد remainingDays، وسلوك الحد معلن. | not-executed |
| P6T-54 | تراجع الساعة وrestart وغياب طويل | INT6-12، INT6-13 / INV6-31 | لا مدة غير منتهية أو إبطال مدمر عابر؛ حالة الشك وgrace قابلة للتفسير. | not-executed |
| P6T-55 | فشل تجديد عابر | INT6-12 / INV6-15، INV6-32 | آخر اعتماد صالح يبقى؛ transient لا يحذف أو يبطل ولا true مضللة. | not-executed |
| P6T-56 | فشل حفظ بديل على القرص | INT6-12 / INV6-15، INV6-32 | لا true دون حفظ فعلي، والقديم يبقى صالحاً؛ تعافٍ ذري وسجل منقح. | not-executed |
| P6T-57 | OAuth state وredirect وmerchant | INT6-07 / INV6-01، INV6-23 | رفض ربط غير مطابق قبل التجارة، وscopes وموافقة موثقتان. | not-executed |
| P6T-58 | refresh أحادي الاستعمال بالتوازي | INT6-07 / INV6-01، INV6-23 | refresh واحدة وتبديل ذري، لا reuse أوaccess مسحوب. | not-executed |
| P6T-59 | صفحات طلبات مع429 في الوسط | INT6-08 / INV6-24، INV6-25 | كل المؤهلين مرة، وcheckpoint بعد apply، وإعادة محدودة دون قفز صفحات. | not-executed |
| P6T-60 | طلب مدفوع مكرر وتصحيح أوإلغاء | INT6-08 / INV6-24، INV6-25 | لا تكرار GL/سداد/مخزون، ولا طغيان قديم؛ التصحيح وفق السياسة. | not-executed |
| P6T-61 | تبديلERP وهوية مرسلWhatsApp | INT6-09 / INV6-01، INV6-26 | لا reuse بلا تفويض؛ حساب المرسل مرتبط بالمستخدم لا بوجود نافذة. | not-executed |
| P6T-62 | ملكية المتصفح ومحاولتان متداخلتان | INT6-09 / INV6-01، INV6-26 | لا kill لبقية العمليات ولا تعطيل sandbox بلا سياسة؛ عزل وقفل صحيحان. | not-executed |
| P6T-63 | صيغ رقم دولي متعددة | INT6-09 / INV6-26 | E.164 صحيحة حسب البلد أو رفض ambiguity، لا بادئة مكررة أوتغيير query. | not-executed |
| P6T-64 | رقم غير صالح وبلد مجهول | INT6-09 / INV6-26 | صفر Navigate/Send قبل تحقق الرقم والمستلم، لا جهة بديلة صامتة. | not-executed |
| P6T-65 | ملف مفقود قبل النص | INT6-09 / INV6-27، INV6-28 | لا جزء يرسل عند فشل التحضير، أوPartial صريحة وفق سياسة معتمدة. | not-executed |
| P6T-66 | نقرة إرسال ثم نتيجة مجهولة وتداخلchat | INT6-09 / INV6-27، INV6-28 | لا Delivered كاذبة أوretry عمياء أوملف فيchat أخرى؛ حالة كل جزء ثابتة. | not-executed |
| P6T-67 | ملف وردية قديم لسياق آخر | INT6-10 / INV6-28 | لا يرفقA لمجرد وجوده؛ preview وملكيةB واختيار صريح. | not-executed |
| P6T-68 | تقريران يولدان بالتوازي | INT6-10 / INV6-28 | كل رسالة تحمل hash تقريرها، لا اسم مشترك، وretention/cleanup معلنان. | not-executed |
| P6T-69 | Type3 Android مع طابعة محددة | INT6-10 / INV6-27 | send count1 لا2 وفق السياسة؛ فشل البريد لا يعيد اعتماد الإغلاق. | not-executed |
| P6T-70 | مصفوفة الطباعة والبريد غير المفعل | INT6-10 / INV6-27 | عدد يطابق السياسة؛ غير مفعل0، وحارس return العادي لا ينكسر. | not-executed |
| P6T-71 | قبول ZATCA طرفي لست حالات محددة | INT6-01، INT6-02 / INV6-01، INV6-02، INV6-04، INV6-05، INV6-06، INV6-07، INV6-08، INV6-09، INV6-10، INV6-11، INV6-12، INV6-13، INV6-14 | كل حالة مرتبطة بإصدار SDK/schema وشهادة/بيئة معلومة، وwarnings/clear/report والأرشيف متسقة؛ ستة اختبارات compliance ليست إثبات إنتاج شامل. | not-executed |
| P6T-72 | ETA: حالة نهائية وإلغاء ورفض | INT6-03، INT6-04 / INV6-09، INV6-10، INV6-12، INV6-16 | حالة/إصدار تطبق مرة ويحفظ الأصل؛ لا نجاح إلغاء من عدم exception فقط ولا false بعد قبول صحيح. | not-executed |
| P6T-73 | جدول نتائج جهاز الدفع وحدود الرد | INT6-05، INT6-06 / INV6-10، INV6-18، INV6-19، INV6-20 | فقط الرفض الموثق Declined، والباقي Unknown للمطابقة؛ لا indexing غير محروس أوبيع جديد من exception. | not-executed |
| P6T-74 | عكس واسترداد وتسوية عملية جهاز | INT6-05، INT6-06، INT6-14 / INV6-19، INV6-20، INV6-21، INV6-22 | تعويض بهوية مرة واحدة مرتبط بالأصل وصلاحية/سقف، والفروق معلقة لا overwrite أوتصحيح أرصدة مباشر. | not-executed |
| P6T-75 | سحب تفويض سلة ونطاق جزئي | INT6-07، INT6-08 / INV6-01، INV6-23، INV6-24، INV6-25 | توقف المتجر الصحيح بلا token متجر آخر؛ checkpoint لا يقفز غير المطبق ولا secrets في الآثار. | not-executed |
| P6T-76 | عقد relay وcloud وCLearfiles | INT6-08، INT6-14 / INV6-01، INV6-08، INV6-10، INV6-11، INV6-12، INV6-22، INV6-25 | لا حكم نجاح أوفقد queue قبل الدليل؛ يزال المثبت فقط وتبقى rejected/unknown، وGL/cursor لا يسبقان اعتماد الأصل. | not-executed |
| P6T-77 | خصوصية المرفقات والبيانات والصلاحيات | INT6-09، INT6-10، INT6-11، INT6-12، INT6-13 / INV6-01، INV6-26، INV6-27، INV6-28، INV6-29، INV6-30 | لا ملف سابق/خارج النطاق يرسل؛ موافقة ورفض موحد وسجل منقح وإثبات ownership بالخادم، لا IDOR مفترض. | not-executed |
| P6T-78 | HTTP وTLS والمهل والإلغاء لكل محول | INT6-01، INT6-02، INT6-03، INT6-04، INT6-07، INT6-08، INT6-11، INT6-12، INT6-13، INT6-14 / INV6-01، INV6-09، INV6-10، INV6-14، INV6-23، INV6-29، INV6-32 | تصنيف ومهلة وإلغاء وretry budget/refresh محددة حسب المزود؛ لا true/empty عامة ولا retry لمتحول مجهول أوتعطيل TLS. | not-executed |
| P6T-79 | تعافٍ بعد انهيار أوامتلاء قرص وقبول بعيد | INT6-01، INT6-03، INT6-04، INT6-05، INT6-06، INT6-08، INT6-09، INT6-10، INT6-11، INT6-12، INT6-14 / INV6-01، INV6-07، INV6-08، INV6-11، INV6-12، INV6-13، INV6-19، INV6-20، INV6-25، INV6-27، INV6-32 | نفس operation/payload والسياق؛ لا خصم/إصدار/رسالة/مخزون مكرر أوACK/clear مبكر، ولا محو الدليل الوحيد. | not-executed |
| P6T-80 | طرفي: طلب وسداد وفاتورة وضريبة وGL وإشعار | INT6-01، INT6-03، INT6-04، INT6-05، INT6-08، INT6-09، INT6-10، INT6-14 / INV6-01، INV6-06، INV6-08، INV6-09، INV6-10، INV6-11، INV6-12، INV6-13، INV6-19، INV6-21، INV6-22، INV6-25، INV6-27، INV6-28 | مبلغ بإشارة وعملة صحيحتين، GL/مخزون مترابطان، tax status/أرشيف صحيحان؛ إعادة طباعة/بريد لا تعيد دفعاً أوحفظاً أوضريبة، والعقد الغائب blocked. | not-executed |

## 4. إعادة التحقق المحلي دون أثر تشغيلي

```bash
python3 docs/audit/tools/collect_baseline.py --verify
python3 docs/audit/tools/check_integration_witnesses.py
python3 docs/audit/tools/validate_audit.py
python3 docs/audit/tools/validate_audit.py --through-phase 5
python3 docs/audit/tools/validate_audit.py --through-phase 4
python3 docs/audit/tools/validate_audit.py --through-phase 3
python3 docs/audit/tools/validate_audit.py --through-phase 2
```

Git وPython stdlib فقط. لا تستورد الأدوات التطبيق أوتكتبbaseline/evidence أوتطلب شبكة. إعادة حساب الأمثلة التاريخية تحقق من التوضيحات نفسها لا تشغيل للتطبيق. **لا تستعملcollect_baseline.py --write لإخفاء تغير المصدر، ولا تستبدلchecks02–05 أواللقطات والتقارير التاريخية.**

## 5. حدود التسليم والقرار التالي

لا تتوفر في هذه البيئة سلسلةWindows/.NET/WPF/SQL وبناء موثوق ومصادرSDK وسياسات واعتمادات مزود متحققة لهذا القبول. المراجع العامة جزئية ومؤرخة وفصلت قواعدها عن شكلSDK. تحفظ H6/Q6 وH4/H5 وQ4/Q5 ما يلزم7/8؛ نقص العقد ليس فشل اختبار أودليل غياب خدمة. اكتمال هذه المراجعة الساكنة لا يحكم الامتثال القانوني/الضريبي أوصحة الأرصدة أوجاهزية الإنتاج. **توقف بعد6؛7 تنتظر إذن المستخدم.**
