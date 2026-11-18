# نموذج التكاملات والحدود وحالات الفشل — المرحلة6

**مرجع التدقيق:** 2026-11-16 (UTC) — **الفرع:** `arena/94ae8414-smartauditerp`  
**مرجع الشيفرة:** `10ba215152f722c8808aea0bb672c1d1d4d9d711`.

**انتهت المرحلة6 كمراجعة ساكنة للنطاق المعلن، لا كتصديق تشغيل أوامتثال. سُلّمت المراحل1–6 توثيقياً؛ المرحلة7 لم تبدأ وتحتاج إذناً جديداً. لم تنفذ إصلاحات أوbuild/Windows/WPF/SQL أوتحميل وتشغيلDLL أواتصالات تشغيلية بمزود/جهاز/ضريبة/دفع/WhatsApp/SMTP/دعم/ترخيص. كل قبول تطبيقي مقترح هنا غير منفذ.**

نطاق6 هو **53 مساراً بمقاطع محددة**: يتداخل17 مع الاتحاد السابق190 ويضيف36، فيصبح الاتحاد حتى6 **226 مساراً**. هذه ليست قراءة كاملة لكل ملف أوتغطية تنفيذية. البحث الآلي عن المراجع لا يحول بقية أسطر الملفات إلى مراجعة يدوية. التفاصيل في [review-scope-06.csv](review-scope-06.csv).

[التقرير والنتائج](PHASE-06.md) · [عقود التكامل والثوابت وحالات الفشل](INTEGRATIONS-06.md) · [التحقق وخطط القبول](VALIDATION-06.md) · [السجل التراكمي](findings.csv) · [الفهرس](README.md) · [النواقص والتوصيات](IMPROVEMENTS.md).

## 1. كيف يقرأ العقد

العقودINT6 تصف **السلوك المحلي وشروط العقد المطلوب قبوله**؛ لا تدعي أن كل ضابط موصى به منفذ، أوأن المزود يفتقد ضابطاً داخلSDK أوخادم غير متاح. `runtime_status=not-executed` لكل صف. الفصل بين النقل والقبول والتطبيق والنتيجة النهائية ضروري.

```text
ERP Context + PolicyVersion + DocumentVersion
  -> Validate + Authorize + immutable Payload + durable Intent
  -> Provider (HTTP / native SDK / browser / SMTP)
      -> Accepted / Rejected / Pending / Unknown + correlation
  -> correlate + persist Result/Archive in a valid local commit
  -> reconcile final state / compensate only by authorized original-linked operation
  -> notification / acknowledge scoped applied result
```

هذا **نموذج مقترح** لا مخطط معمارية منفذ أوضمان exactly-once. لا يجعلHTTP جزءاً منSQL transaction، ولا يتجاوز توقيتclearance المطلوب للنوع القياسي. **Unknown ليستDeclined، وSubmitted ليستValid، ونقرة إرسال أوقبولSMTP لا يثبتانDelivered.**

## 2. فهرس العقود14

| المعرف | المزود/القناة | حد الوصول | نتائج مرتبطة |
|---|---|---|---|
| INT6-01 — | ZATCA — الإصدار والإجازة والإبلاغ والأرشفة | InvoiceOper وInvoiceOperContract عند الحفظ، والمتابعة الموصولة من Home، ومسار Android المحدد بعد commit؛ اختبار compliance مسار مختلف. | P6-001، P6-002، P6-003، P6-004، P6-005، P6-006، P6-007، P6-008، P6-009، P6-012 |
| INT6-02 — | ZATCA — دورة الاعتماد والتجديد والاستيراد | أزرار إعداد مع حراس EmpNo/password/trial جزئية. زر التجديد يعرض رسالة فقط، وهو امتداد P1-033 لا نتيجة جديدة. | P6-010، P6-011، P6-012، P1-033 |
| INT6-03 — | ETA — الفاتورة والإشعار الدائن | زر إرسال فاتورة Sale والمتابعة؛ CancelInvoice helper خاص، وfrmSentEinvoice موجودة لكن مدخل Home فارغ، فلا يوصف الإلغاء كمسار حي مثبت. | P6-013، P6-014، P6-015، P6-016، P1-033 |
| INT6-04 — | ETA — الإيصال والمرتجع | sendERecitp من Sale كـTask غير منتظرة ومن المتابعة المنتظرة؛ Receipt=true يختار المسار. لم يشغل أي منهما. | P6-005، P6-014، P6-015، P6-017، P6-018، P6-019 |
| INT6-05 — | Geidea وUtilitiesProj — الدفع الطرفي | Bill يستعمل UtilitiesProj.Geidea.Pay أو GeideaPament.Pay حسب IsGediaActive؛ Pay يستعمل الأول. ConnectGeidea المحلي بلا caller مباشر مكتشف. | P6-020، P6-021، P6-022 |
| INT6-06 — | NeoLeap connector — SALE واختبار الإعداد | TestConnection له caller إعداد، وProcessSale موجود بلا caller بيع POS مباشر مكتشف؛ لا يعمم مسار الاختبار على سداد العملاء. | P6-021، P6-022 |
| INT6-07 — | Salla — OAuth والتثبيت والتدوير | SallaAuth وعينة FrmSallah بلا caller تنقل مباشر مكتشف؛ قد تملك خدمة auditor-salla الخارجية دورة أخرى. | P6-029 |
| INT6-08 — | Salla — الطلبات والمنتجات والعملاء وتطبيق ERP | managers CRUD وعينة تعرض count وتضيف منتجاً ثابتاً؛ Home فارغ تحت P1-033 وpending helper بلا caller مباشر مكتشف. | P6-030، P6-029، P6-023، P5-026 |
| INT6-09 — | WhatsApp Web — الجلسة والنص والملف | Sale→printwhatsapp→Session→WhatsAppSender مسار فعلي؛ يولد PDF أولاً ثم يهمل bool العائد من المساعد. | P6-031، P6-032، P6-033، P1-024 |
| INT6-10 — | SMTP — يدوي وفاتورة وإغلاق | EmailMang/SendEmail وPrint ومولدا الإغلاق؛ AndroidType3 قد يرسل مرتين، أما العادي ففيه return بعد الفرع3. | P6-034، P6-035، P2-015 |
| INT6-11 — | Support API — التذكرة والرد والمرفقات | FormCreateTicket وعميل HttpClient بمهلة30ث؛ مسار التفاصيل يهمل DTO، والإنشاء لديه تعطيل زر أثناء انتظار المهمة. | P6-024، P6-025، P2-015 |
| INT6-12 — | DeviceLicense — authorize وcache والأوفلاين | Home.CheckLicense وStartDailyCheck/ShowtrialOfflin وActivateOnlineLicense؛ لا تفعيل أو تعديل ملف رخصة جرى. | P6-026، P6-027، P6-028، P1-032 |
| INT6-13 — | ManagerOnline — الاستحقاق والتواصل | CheckLicenseStatus يستدعي بيانات المؤسسة وتفعيل ZATCA وفحص الجهاز وتاريخ الاشتراك؛ StartDailyCheck بعد30يوماً، وOnOff محلي منفصل. | P6-002، P6-027، P6-028، P1-032 |
| INT6-14 — | AuditorAPI وWs_Auditor — متابعة عقود السحابة | Save يستقبل GetInvoiceCloudPaymentType وSendQrCode من المتابعة؛ متابعة محدودة لـP5، لا إعادة تدقيق المزامنة كلها. | P6-023، P5-026، P5-029 |

### INT6-01 — ZATCA — الإصدار والإجازة والإبلاغ والأرشفة

**المدخل وإمكان الوصول:** InvoiceOper وInvoiceOperContract عند الحفظ، والمتابعة الموصولة من Home، ومسار Android المحدد بعد commit؛ اختبار compliance مسار مختلف.

**البيئة والعنوان والإصدار:** IsProduction/IsSimulation إلى SDK؛ المضيف ونسخة HTTP داخله غير متاحين. البوابة الرسمية ما زالت تربط XML v1.2 المؤرخة19 مايو2023؛ لا مواصفة جديدة مفترضة لمجرد تحديث الصفحة في2026.

**الهوية والتوثيق والنطاق:** CSID/Secret ومفتاح خاص؛ يثبت issuer وEGS وtenant والبيئة وغرض الشهادة وإصدارها. HTTP auth/TLS داخل SDK يحتاجان دليلاً منفصلاً.

**الطلب والثوابت قبل الإرسال:** قرار نوع واحد؛ كمية وسعر وضريبة وخصومات وعملة وICV/PIH ومرجع تصحيح متحققون، ولقطة ثابتة قبل التوقيع.

**النتيجة والربط:** Clearance أو Reporting مقبول حسب النوع، لا غياب أخطاء فقط؛ يفصل النقل والقبول والرفض وUnknown والتحذيرات، ويحفظ UUID/hash والرد الفعلي.

**الاستدامة والإعادة والمطابقة/العكس:** نية دائمة وهوية/حمولة ثابتتان؛ قبول بعيد ثم فشل محلي يستكمل بالمطابقة لا إعادة الإصدار. أرشيف أصل ومجاز ومحاولات. طابور الأوفلاين وSLA حيث ينطبقان؛ standard لا يشارك قبل clearance.

**النقل والمهل والإلغاء والحدود:** المهل والإلغاء و401/403/429/5xx وRetry-After غير مكشوفة في helper؛ لا نفترض أن SDK لا يوفرها، ولا نوصي بإعادة عمياء.

**الخصوصية والتفويض:** حقوق إصدار وإعادة واستيراد مفتاح وتنزيل XML وتجاوز إداري مستقلة؛ مخزن مفاتيح محمي وretention ومنع secrets/فواتير عملاء في logs.

**المحجوب وحدود المعرفة:** مصدر SDK وبيئة النشر وحدود EGS وموجة إلزام المنشأة غير متاحة؛ لا حكم امتثال أو إرسال تشغيلي.

**الدليل المحلي:** `SmartAuditERP/Class/ZatcaService.cs:78-124`؛ `SmartAuditERP/Class/InvoiceOper.cs:1473-1495`؛ `SmartAuditERP/Class/InvoiceOper.cs:1854-1884`؛ `SmartAuditERP/Class/InvoiceOper.cs:5211-5243`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:285-307`؛ `SmartAuditERP/Class/MainSetting.cs:12-18`؛ `SmartAuditERP/Class/Common.cs:1066-1088`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:911-926`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:274-278`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1115-1149`؛ `SmartAuditERP/Class/ZatcaService.cs:122-124`؛ `SmartAuditERP/Class/ZatcaService.cs:154-176`؛ `SmartAuditERP/Class/ZatcaService.cs:204-263`؛ `SmartAuditERP/Class/ZatcaService.cs:278-324`؛ `SmartAuditERP/Class/ZatcaService.cs:235-263`؛ `SmartAuditERP/Class/ZatcaService.cs:277-342`؛ `SmartAuditERP/Class/ZatcaService.cs:116-124`؛ `SmartAuditERP/Class/ZatcaService.cs:343-366`؛ `SmartAuditERP/Class/InvoiceOper.cs:5276-5323`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:105-116`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:287-333`؛ `SmartAuditERP/Class/EtaReciptService.cs:100-106`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:624-708`؛ `SmartAuditERP/Class/ZatcaService.cs:369-427`؛ `SmartAuditERP/Class/InvoiceOper.cs:2209-2249`؛ `SmartAuditERP/Class/InvoiceOper.cs:1488-1494`؛ `SmartAuditERP/Class/InvoiceOper.cs:1878-1883`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:892-915`؛ `SmartAuditERP/Class/InvoiceOper.cs:1473-1511`؛ `SmartAuditERP/Class/InvoiceOper.cs:1833-1902`؛ `SmartAuditERP/Class/InvoiceOper.cs:2132-2184`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:915-994`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:1043-1051`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:1372-1405`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:480-519`؛ `SmartAuditERP/Class/ZatcaService.cs:343-357`؛ `SmartAuditERP/Class/ZatcaService.cs:369-377`؛ `SmartAuditERP/Class/InvoiceOper.cs:1914-1943`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:159-208`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:624-647`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:815-837`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:920-943`؛ `SmartAuditERP/Class/ZatcaCredential.cs:4-20`؛ `SmartAuditERP/Class/ZatcaService.cs:343-377`؛ `SmartAuditERP/Class/ZatcaService.cs:430-456`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:259-278`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:892-909`؛ `SmartAuditERP/Home.xaml.cs:3796-3798`

**التتبع:** INV6-01، INV6-02، INV6-03، INV6-04، INV6-05، INV6-06، INV6-07، INV6-08، INV6-09، INV6-10، INV6-11، INV6-12، INV6-13، INV6-14؛ خطط P6T-01، P6T-02، P6T-03، P6T-04، P6T-05، P6T-06، P6T-07، P6T-08، P6T-09، P6T-10، P6T-11، P6T-12، P6T-13، P6T-14، P6T-15، P6T-16، P6T-17، P6T-18، P6T-23، P6T-24، P6T-71، P6T-78، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: REF6-01، REF6-02، REF6-03؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-02 — ZATCA — دورة الاعتماد والتجديد والاستيراد

**المدخل وإمكان الوصول:** أزرار إعداد مع حراس EmpNo/password/trial جزئية. زر التجديد يعرض رسالة فقط، وهو امتداد P1-033 لا نتيجة جديدة.

**البيئة والعنوان والإصدار:** فصل compliance وsimulation وproduction وغرض كل شهادة؛ لا اختيار P_* لكل البيئات أو اعتماد مدة الشهادة من نص الزر.

**الهوية والتوثيق والنطاق:** OTP وCSR وkeypair وCSID/Secret وrequestId؛ هوية المنشأة والوحدة وصلاحية/سلسلة الشهادة وتفويض المسؤول.

**الطلب والثوابت قبل الإرسال:** Generate ثم تحقق ثم compliance ثم اختبارات ثم تفعيل إنتاج بنتائج typed؛ fresh/existing/import تستعمل كاتباً مكتمل الأعمدة والقيم والمعاملات.

**النتيجة والربط:** كل خطوة لها نتيجة وهوية طلب؛ فشل داخلي يوقف المتصل ولا Saved/Active بعده، ولا نجاح اعتماد جديد قبل تحقق هويته.

**الاستدامة والإعادة والمطابقة/العكس:** نسخة staging وتبديل ذري مع آخر اعتماد صالح محمي وخطة rollback؛ rotation/expiry/revocation وحوادث المفتاح مطلوبة.

**النقل والمهل والإلغاء والحدود:** OTP/CSR ليسا طلبين قابلين للتكرار عميانياً؛ timeout أو نتيجة مجهولة يطابقان request قبل إنشاء محاولة جديدة.

**الخصوصية والتفويض:** صلاحيات إنشاء واستيراد وتفعيل منفصلة، وحماية/منع تصدير المفتاح وفق السياسة؛ لا OTP أو شهادة إنتاج في الاختبار أو الدردشة.

**المحجوب وحدود المعرفة:** تجديد فعلي والتحقق من chain وAPI الداخلية غير متاحين؛ لم يستعمل أي مفتاح أو رمز.

**الدليل المحلي:** `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:160-293`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:454-495`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:506-527`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:534-605`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1019-1054`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:350-370`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1056-1081`؛ `SmartAuditERP/Properties/Resources.resx:4164-4174`؛ `SmartAuditERP/Class/ZatcaCredential.cs:4-20`؛ `SmartAuditERP/Class/ZatcaService.cs:343-377`؛ `SmartAuditERP/Class/ZatcaService.cs:430-456`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:259-278`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:892-909`؛ `SmartAuditERP/Home.xaml.cs:2367-2372`؛ `SmartAuditERP/Home.xaml.cs:3805-3808`؛ `SmartAuditERP/Home.xaml.cs:3877-3886`؛ `SmartAuditERP/Home.xaml:394-397`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1152-1157`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml:429-434`

**التتبع:** INV6-01، INV6-13، INV6-14، INV6-15؛ خطط P6T-03، P6T-04، P6T-11، P6T-12، P6T-19، P6T-20، P6T-21، P6T-22، P6T-23، P6T-24، P6T-71، P6T-78؛ جميعها غير منفذة. المراجع: REF6-01، REF6-02؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-03 — ETA — الفاتورة والإشعار الدائن

**المدخل وإمكان الوصول:** زر إرسال فاتورة Sale والمتابعة؛ CancelInvoice helper خاص، وfrmSentEinvoice موجودة لكن مدخل Home فارغ، فلا يوصف الإلغاء كمسار حي مثبت.

**البيئة والعنوان والإصدار:** EtaSetting.EinvoieType/DocumentTypeVersion إلى ETA_Invoice؛ قرئت Invoice/Credit v1.0، أما الإصدارات الأخرى فتحتاج مراجعة عقدها.

**الهوية والتوثيق والنطاق:** client_id وsecret1/2 وtoken certificate/PIN؛ تثبت هوية الممول/الوسيط وصلاحياته ومصدر التوقيع خارجياً.

**الطلب والثوابت قبل الإرسال:** كمية عشرية ووحدة وسعر وخصومات وTaxType وعملة؛ UTC حقيقي، references للـcredit وinternalId مرتبطان بالأصل لا بالصف الأول افتراضاً.

**النتيجة والربط:** returnds عقد خارجي؛ accepted/rejected/submissionUUID وربط internalId مطلوبان. HTTP202 قبول أولي لا Valid نهائية، وعدم exception لا يثبت إلغاء أو رفضاً.

**الاستدامة والإعادة والمطابقة/العكس:** SubmittedPending ثم callback أو polling للـsubmission إلى الحالة النهائية؛ لا resubmit بعد20x دون سبب عقدي. حفظ التصحيح والعكس والأصل.

**النقل والمهل والإلغاء والحدود:** التوقيع والتوكين وHTTP والمهل داخل SDK؛ caching للتوكين وإعادة محدودة. recent/print ليست آلية polling بديلة للـsubmission.

**الخصوصية والتفويض:** حق إرسال/إلغاء/رفض/عرض printout مع actor/subject/UUID؛ لا PIN أو مفاتيح أو بيانات عملاء في آثار الاختبار.

**المحجوب وحدود المعرفة:** تعريف SendEinvoice/returnds/التوقيع غير متاح؛ لا نحول أسماء الحقول إلى ضمانات raw HTTP أو final validation.

**الدليل المحلي:** `SmartAuditERP/Class/EtaService.cs:34-81`؛ `SmartAuditERP/Class/EtaReciptService.cs:28-44`؛ `SmartAuditERP/Class/EtaService.cs:171-186`؛ `SmartAuditERP/Class/EtaReciptService.cs:100-107`؛ `SmartAuditERP/Class/EtaService.cs:179-182`؛ `SmartAuditERP/Class/EtaReciptService.cs:100-105`؛ `SmartAuditERP/Class/EtaService.cs:87-90`؛ `SmartAuditERP/Class/EtaService.cs:248-299`؛ `SmartAuditERP/Class/InvoiceOper.cs:5348-5373`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:592-615`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2941-2959`؛ `SmartAuditERP/Home.xaml.cs:2367-2372`؛ `SmartAuditERP/Home.xaml.cs:3805-3808`؛ `SmartAuditERP/Home.xaml.cs:3877-3886`؛ `SmartAuditERP/Home.xaml:394-397`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1152-1157`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml:429-434`؛ `SmartAuditERP/Form_WPF/frmSentEinvoice.xaml.cs:188-280`؛ `SmartAuditERP/Home.xaml.cs:3805-3808`

**التتبع:** INV6-01، INV6-05، INV6-06، INV6-08، INV6-09، INV6-10، INV6-12، INV6-16، INV6-17؛ خطط P6T-25، P6T-26، P6T-27، P6T-28، P6T-29، P6T-30، P6T-31، P6T-32، P6T-72، P6T-78، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: REF6-04، REF6-06، REF6-07، REF6-09، REF6-11؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-04 — ETA — الإيصال والمرتجع

**المدخل وإمكان الوصول:** sendERecitp من Sale كـTask غير منتظرة ومن المتابعة المنتظرة؛ Receipt=true يختار المسار. لم يشغل أي منهما.

**البيئة والعنوان والإصدار:** Valley/config_class؛ production API/token منفصلان في الإعداد، وBaseUrl الاختباري يشير للهوية. typeVersion1.2 مدخل محلي وليس إثبات شكل JSON.

**الهوية والتوثيق والنطاق:** client_id/secret وPosEtaSerial وbranch وseller.RIN؛ تثبت هوية POS والممول والفرع وغرض الاعتماد.

**الطلب والثوابت قبل الإرسال:** كمية عشرية وnetSale/totalSale ومجاميع خصم/ضريبة/T4؛ previousUUID على POS، referenceUUID لأصل المرتجع، وقت وعملة صحيحان.

**النتيجة والربط:** status في send_respons_model ليس HTTP مفترضاً؛ يثبت معنى النجاح وUUID وsubmissionUUID والقبول الأولي/النهائي. غير المقبول لا يصبح true/Sent.

**الاستدامة والإعادة والمطابقة/العكس:** UUID مشتق من المحتوى وفق العقد، وسلسلة POS ومحاولة دائمة؛ correction وreferenceOldUUID حيث ينطبقان، مع مطابقة duplicate قبل الإعادة.

**النقل والمهل والإلغاء والحدود:** 202 أولي وduplicate422/throttle وRetry-After في الوثائق لا تثبت ترجمتها إلى status بالمكتبة؛ يلزم backoff/budget/cancellation حسب العقد.

**الخصوصية والتفويض:** POS مفوض وأرشيف محدود الوصول ومفاتيح اختبار فقط، وفصل حق الإرسال والعكس عن العرض.

**المحجوب وحدود المعرفة:** المكتبة وserializer وconfig/status/signing/polling غير متاحة؛ لا نتهم SDK بعيب لم يثبت.

**الدليل المحلي:** `SmartAuditERP/Class/ZatcaService.cs:116-124`؛ `SmartAuditERP/Class/ZatcaService.cs:343-366`؛ `SmartAuditERP/Class/InvoiceOper.cs:5276-5323`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:105-116`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:287-333`؛ `SmartAuditERP/Class/EtaReciptService.cs:100-106`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:624-708`؛ `SmartAuditERP/Class/EtaService.cs:171-186`؛ `SmartAuditERP/Class/EtaReciptService.cs:100-107`؛ `SmartAuditERP/Class/EtaService.cs:179-182`؛ `SmartAuditERP/Class/EtaReciptService.cs:100-105`؛ `SmartAuditERP/Class/EtaReciptService.cs:217-244`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:592-615`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:2951-2958`؛ `SmartAuditERP/Class/InvoiceOper.cs:5348-5373`؛ `SmartAuditERP/Class/EtaReciptService.cs:28-61`؛ `SmartAuditERP/Class/EtaReciptService.cs:108-149`؛ `SmartAuditERP/Class/InvoiceOper.cs:5074-5105`؛ `SmartAuditERP/Class/InvoiceOper.cs:4189-4221`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:780-809`؛ `SmartAuditERP/Class/EtaReciptService.cs:66-81`؛ `SmartAuditERP/Form_WPF/frmSentEinvoice.xaml.cs:58-89`

**التتبع:** INV6-01، INV6-05، INV6-06، INV6-07، INV6-08، INV6-09، INV6-10، INV6-12، INV6-16، INV6-17؛ خطط P6T-09، P6T-10، P6T-27، P6T-28، P6T-29، P6T-30، P6T-33، P6T-34، P6T-35، P6T-36، P6T-37، P6T-38، P6T-72، P6T-78، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: REF6-05، REF6-06، REF6-08، REF6-10، REF6-12؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-05 — Geidea وUtilitiesProj — الدفع الطرفي

**المدخل وإمكان الوصول:** Bill يستعمل UtilitiesProj.Geidea.Pay أو GeideaPament.Pay حسب IsGediaActive؛ Pay يستعمل الأول. ConnectGeidea المحلي بلا caller مباشر مكتشف.

**البيئة والعنوان والإصدار:** COMPort وreceipt flag للفرع الجديد؛ PInvoke المحلي يذكر madaapi ونسخة1_7 وStdCall. ABI والمعمارية وfirmware وبيئة التاجر مجهولة.

**الهوية والتوثيق والنطاق:** terminal/merchant/store/operator/role وعملة ووحدة مبلغ موثقة؛ لا تعد إعدادات الواجهة تفويضاً من البنك.

**الطلب والثوابت قبل الإرسال:** PaymentIntent متحقق وثابت amount/currency/remainder/invoiceVersion/operationId قبل Pay؛ فحص المدخلات وطول الرد جزء من الحد.

**النتيجة والربط:** ثلاثة bytes أو IsSucess في العميل؛ لا نوثق دلالة أكواد المورد بغير مرجع. Approved/Declined/Cancelled/Unknown وamount/reference مستقلة.

**الاستدامة والإعادة والمطابقة/العكس:** محاولة قبل الطلب؛ Query قبل retry عند فقد الرد أو فشل SQL؛ reversal/refund/void ومطابقة settlement مرتبطان بالأصل ومخولان.

**النقل والمهل والإلغاء والحدود:** sync للفرع القديم وasync للجديد؛ timeout/cancel/port busy لا يلغون خصماً بأثر رجعي. يلزم عقد المورد للمهل وquery والإعادة.

**الخصوصية والتفويض:** حق اختبار مالي وعكس وتسوية unknown مستقل؛ لا PAN أو raw card data في السجلات والوثائق أو fakes.

**المحجوب وحدود المعرفة:** UtilitiesProj وGeideaPament وnative ABI غير متاحة؛ لا أكواد نجاح أو idempotency أو ضمان عكس مخترع، ولا تحميل DLL أو دفع نفذ.

**الدليل المحلي:** `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:437-519`؛ `SmartAuditERP/Form_WPF/frmPOSPay.xaml.cs:402-464`؛ `SmartAuditERP/Class/InvoiceOper.cs:4498-4535`؛ `SmartAuditERP/Class/InvoiceOper.cs:4680-4718`؛ `SmartAuditERP/Class/InvoiceOper.cs:4592-4625`؛ `SmartAuditERP/Class/InvoiceOper.cs:4781-4802`؛ `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:102-107`؛ `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:434-564`؛ `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:1093-1115`؛ `SmartAuditERP/Form_WPF/frmPOSPay.xaml.cs:428-485`؛ `SmartAuditERP/Class/InvoiceOper.cs:1750-1765`؛ `SmartAuditERP/Properties/Resources.resx:3852-3875`؛ `SmartAuditERP/Class/NeoleapService.cs:23-50`؛ `SmartAuditERP/Class/TransactionResponse.cs:1-32`؛ `SmartAuditERP/Class/NeoleapService.cs:54-83`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:2505-2536`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:4047-4066`؛ `SmartAuditERP/Class/Geidea.cs:1-58`؛ `SmartAuditERP/Class/PassPayment.cs:1-16`

**التتبع:** INV6-01، INV6-10، INV6-11، INV6-12، INV6-18، INV6-19، INV6-20، INV6-21؛ خطط P6T-39، P6T-40، P6T-41، P6T-42، P6T-43، P6T-44، P6T-73، P6T-74، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-06 — NeoLeap connector — SALE واختبار الإعداد

**المدخل وإمكان الوصول:** TestConnection له caller إعداد، وProcessSale موجود بلا caller بيع POS مباشر مكتشف؛ لا يعمم مسار الاختبار على سداد العملاء.

**البيئة والعنوان والإصدار:** ConnectionManagerFactory/RequestBuilder خارجيان؛ host والجهاز والتاجر وsandbox ونسخة ABI غير متاحة. Test يبني SALE0.5.

**الهوية والتوثيق والنطاق:** merchantToken/ecrToken/ecrRef؛ الاعتماد المضمن في Test لم ينسخ أو يستعمل، ويلزم مخزن وتدوير واختيار تاجر صريح.

**الطلب والثوابت قبل الإرسال:** amount وecrRef ثابتان لنفس النية؛ Guid جديد ليس تعويضاً عن correlation مفقودة. فحص اتصال محايد منفصل عن SALE.

**النتيجة والربط:** parser محلي يفسر ErrorMsg و00/01/02 ويجمع RRN/STAN/approval/amount/PAN/raw. دلالات المورد نفسها غير مثبتة.

**الاستدامة والإعادة والمطابقة/العكس:** catch وSuccess=false لا يثبتان Declined؛ Query/Reversal/Reconcile قبل إنشاء SALE بمرجع جديد، وإعادة تشغيل لا تنسى المحاولة.

**النقل والمهل والإلغاء والحدود:** SendRequest Task بلا مهلة/إلغاء ظاهرين هنا وقد يوفرهما connector؛ Test caller لا ينتظر النتيجة حالياً.

**الخصوصية والتفويض:** تنقيح PAN/raw/token، جهاز اختبار وتفويض تأكيد مالي، ومنع استخدام زر الاختبار كـping على الإنتاج.

**المحجوب وحدود المعرفة:** العقد والـfirmware والإعداد الفعلي غائبة؛ لا نجاح parser أو SALE حقيقي ثبت.

**الدليل المحلي:** `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:102-107`؛ `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:434-564`؛ `SmartAuditERP/Form_WPF/frmPOSBill.xaml.cs:1093-1115`؛ `SmartAuditERP/Form_WPF/frmPOSPay.xaml.cs:428-485`؛ `SmartAuditERP/Class/InvoiceOper.cs:1750-1765`؛ `SmartAuditERP/Properties/Resources.resx:3852-3875`؛ `SmartAuditERP/Class/NeoleapService.cs:23-50`؛ `SmartAuditERP/Class/TransactionResponse.cs:1-32`؛ `SmartAuditERP/Class/NeoleapService.cs:54-83`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:2505-2536`؛ `SmartAuditERP/Form_WPF/frmSettings.xaml.cs:4047-4066`؛ `SmartAuditERP/Class/NeoleapService.cs:1-166`؛ `SmartAuditERP/Class/TransactionResponse.cs:1-32`

**التتبع:** INV6-01، INV6-10، INV6-14، INV6-18، INV6-19، INV6-20، INV6-21؛ خطط P6T-41، P6T-42، P6T-43، P6T-44، P6T-73، P6T-74، P6T-79؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-07 — Salla — OAuth والتثبيت والتدوير

**المدخل وإمكان الوصول:** SallaAuth وعينة FrmSallah بلا caller تنقل مباشر مكتشف؛ قد تملك خدمة auditor-salla الخارجية دورة أخرى.

**البيئة والعنوان والإصدار:** accounts.salla.sa/token وAdmin v2 في helper؛ نوع التطبيق/Easy أوCustom mode غير معلوم. المرجع المقروء يذكر Easy Mode للتطبيقات المنشورة.

**الهوية والتوثيق والنطاق:** registered redirect وstate وcode وmerchant user-info وscopes وexpiry وaccess/refresh، مع ربط tenant لا اسم بشري فقط.

**الطلب والثوابت قبل الإرسال:** تفويض متجر بموافقته وredirect مطابق؛ لا placeholder أو token ثابت لكل المتاجر، والأسرار تحفظ وفق معمارية موثوقة.

**النتيجة والربط:** 2xx وschema وmerchant/scopes/expiry متطابقة؛ denied/invalid_grant/expired/uninstalled نتائج مميزة.

**الاستدامة والإعادة والمطابقة/العكس:** refresh أحادي الاستعمال وفق الوثيقة؛ single-flight وتبديل ذري ومنع إعادة استعمال متوازية، وإبطال uninstall لا fallback لرمز سابق.

**النقل والمهل والإلغاء والحدود:** cache وفق lifetime، و401 بميزانية refresh محدودة؛ تبادل code وrefresh ليسا طلبَي GET قابلين للإعادة بلا ضوابط.

**الخصوصية والتفويض:** لا tokens في source أو logs أو الرسائل، وحق تثبيت وفصل المتجر وscopes وretention معلن.

**المحجوب وحدود المعرفة:** إعداد التطبيق وcallback/backend لم يفحصا؛ فجوة مستودع لا دليل على فشل تفويض متجر حي.

**الدليل المحلي:** `SmartAuditERP/Class/SallaAuth.cs:10-33`؛ `SmartAuditERP/Class/SallaAPI.cs:20-39`؛ `SmartAuditERP/Form_WPF/FrmSallah.xaml.cs:30-35`

**التتبع:** INV6-01، INV6-14، INV6-23، INV6-24؛ خطط P6T-57، P6T-58، P6T-75، P6T-78؛ جميعها غير منفذة. المراجع: REF6-13؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-08 — Salla — الطلبات والمنتجات والعملاء وتطبيق ERP

**المدخل وإمكان الوصول:** managers CRUD وعينة تعرض count وتضيف منتجاً ثابتاً؛ Home فارغ تحت P1-033 وpending helper بلا caller مباشر مكتشف.

**البيئة والعنوان والإصدار:** api.salla.dev/admin/v2؛ Orders المرجعية تذكر صفحات متسلسلة وcache، والحدود مرتبطة بالخطة/headers لا quota ثابتة لكل متجر.

**الهوية والتوثيق والنطاق:** Bearer وscopes لكل نشاط وربط merchant؛ تفويض relay وwebhook signature يجب إثباتهما من المكون الخارجي.

**الطلب والثوابت قبل الإرسال:** merchant/entity/version وmapping للطلب/العميل/الصنف/الوحدة/الدفعة/الضريبة/الفرع/المخزن، وسياسة paid/cancel/refund ومصدر stock truth.

**النتيجة والربط:** HTTP/schema/business result وremote order id/version؛ count أول data ليس اكتمالاً، وUpdateStatus ليس إثبات اعتماد ERP.

**الاستدامة والإعادة والمطابقة/العكس:** صفحات وcheckpoint/snapshot وinbox/outbox وdedup/version؛ الرسالة المكررة أو القديمة لا تكرر قيداً/سداداً/مخزوناً.

**النقل والمهل والإلغاء والحدود:** 429 وRetry-After/cache/backoff/jitter وميزانية توازٍ. الاستثناء العام الحالي لا يقوم مقام إدارة دورة مزامنة كاملة.

**الخصوصية والتفويض:** تقليل بيانات العميل وretention وحقوق create/delete/status ومراجعة روابط المواقع؛ لا تجارب CRUD على متجر حي.

**المحجوب وحدود المعرفة:** relay وERP mapping خارج النسخة؛ إلغاء expanded لا يثبت فشل عينة لا تقرؤه أصلاً، ولا ننفي وجود خدمة خارجية.

**الدليل المحلي:** `SmartAuditERP/Class/OrdersManager.cs:25-38`؛ `SmartAuditERP/Class/ProductsManager.cs:16-38`؛ `SmartAuditERP/Class/CustomersManager.cs:15-23`؛ `SmartAuditERP/Class/SallaAPI.cs:29-74`؛ `SmartAuditERP/Form_WPF/FrmSallah.xaml.cs:41-101`؛ `SmartAuditERP/Home.xaml.cs:2367-2393`؛ `SmartAuditERP/Home.xaml.cs:3877-3886`؛ `SmartAuditERP/Home.xaml:394-397`؛ `SmartAuditERP/Class/SallaAuth.cs:10-33`؛ `SmartAuditERP/Class/SallaAPI.cs:20-39`؛ `SmartAuditERP/Form_WPF/FrmSallah.xaml.cs:30-35`؛ `SmartAuditERP/Form_WPF/frmCloudPaymentSetting.xaml.cs:249-260`؛ `SmartAuditERP/Form_WPF/frmCloudPaymentSetting.xaml.cs:268-355`؛ `SmartAuditERP/Class/InvoiceOper.cs:5246-5274`؛ `SmartAuditERP/Class/InvoiceOper.cs:2666-2694`

**التتبع:** INV6-01، INV6-22، INV6-23، INV6-24، INV6-25؛ خطط P6T-45، P6T-46، P6T-59، P6T-60، P6T-75، P6T-76، P6T-78، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: REF6-13، REF6-14، REF6-15؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-09 — WhatsApp Web — الجلسة والنص والملف

**المدخل وإمكان الوصول:** Sale→printwhatsapp→Session→WhatsAppSender مسار فعلي؛ يولد PDF أولاً ثم يهمل bool العائد من المساعد.

**البيئة والعنوان والإصدار:** Selenium/ChromeDriver وDOM selectors، وليس Meta Cloud API. profile ثابت تحت حساب OS؛ نسخ المتصفح/driver/DOM غير مثبتة.

**الهوية والتوثيق والنطاق:** حساب المرسل عبر QR؛ WindowHandles لا يثبت الحساب أو التفويض. principal/tenant وE.164 والبلد وجهة الاتصال مطلوبة.

**الطلب والثوابت قبل الإرسال:** ملف immutable مملوك للمستند وبصمة وpreview وحق مشاركة، والتحقق قبل إرسال النص؛ لا prefix966 عشوائي.

**النتيجة والربط:** TextSubmitted/FileSubmitted/Partial/Unknown، لا Delivered من click+Delay. أي API مستقبلي يوثق بعقده ولا يفترض حاضراً.

**الاستدامة والإعادة والمطابقة/العكس:** serial queue وهوية محاولة وحالة كل جزء، لا إعادة من الصفر عند unknown؛ cleanup/retention محددان ولا kill شامل.

**النقل والمهل والإلغاء والحدود:** انتظارات DOM متفرقة لا cancellation أعمال شاملة؛ reconnect/login والمهلة الكلية والتزامن تحتاج عقد دورة حياة.

**الخصوصية والتفويض:** QR/profile ومحادثات وفاتورة حساسة؛ عزل OS/ERP ومراجعة --no-sandbox وتفويض حساب المرسل، لا أتمتة حساب حقيقي.

**المحجوب وحدود المعرفة:** الحساب وسياسة المزود وDOM ودليل التسليم الفعلي غائبة؛ لا رسالة أو وصول أو قراءة مثبتة.

**الدليل المحلي:** `SmartAuditERP/Class/WhatsAppSender.cs:22-63`؛ `SmartAuditERP/Class/WhatsAppSender.cs:230-260`؛ `SmartAuditERP/Class/Session.cs:9-29`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3185-3187`؛ `SmartAuditERP/Class/WhatsAppSender.cs:107-118`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3150-3187`؛ `SmartAuditERP/Class/WhatsAppSender.cs:140-217`؛ `SmartAuditERP/Class/Session.cs:14-29`؛ `SmartAuditERP/Form_WPF/frmInvSale.xaml.cs:3166-3199`؛ `SmartAuditERP/Class/WhatsAppSender.cs:22-39`

**التتبع:** INV6-01، INV6-26، INV6-27، INV6-28؛ خطط P6T-61، P6T-62، P6T-63، P6T-64، P6T-65، P6T-66، P6T-77، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-10 — SMTP — يدوي وفاتورة وإغلاق

**المدخل وإمكان الوصول:** EmailMang/SendEmail وPrint ومولدا الإغلاق؛ AndroidType3 قد يرسل مرتين، أما العادي ففيه return بعد الفرع3.

**البيئة والعنوان والإصدار:** host/port/SSL من SettingEmail؛ EmailMang يفرض EnableSsl=true، ومسارات أخرى تقرأ SSL. لا مزود أو TLS مفترض لكل الإعدادات.

**الهوية والتوثيق والنطاق:** اسم وكلمة مرور من UI/DB؛ هوية مرسل وصلاحية send-as ونطاق فرع ومستلم؛ المصادقة والشهادة تختبران ببيئة منفصلة.

**الطلب والثوابت قبل الإرسال:** مرفقات صريحة مرتبطة بتقرير/وردية/فرع/hash مع subject/body مطابقين؛ لا آخر PDF ضمنياً أو اسم ثابت يتبادل بين عمليتين.

**النتيجة والربط:** SmtpClient.Send ليس إثبات وصول صندوق أو قراءة؛ Accepted/Failed/Unknown/Bounce ونتيجة كل مستلم تميز.

**الاستدامة والإعادة والمطابقة/العكس:** NotificationId/MessageId حيث يتاح ودفتر محاولات؛ فقد الرد بعد القبول لا يولد رسالة جديدة آلياً. فشل البريد لا يعيد commit المالي.

**النقل والمهل والإلغاء والحدود:** Send متزامن في المقروء؛ حدود الحجم/الحساب والمهل والإلغاء وSPF/DKIM/DMARC/bounce policy غير متاحة. يلزم SMTP sink أولاً.

**الخصوصية والتفويض:** حماية secret وتقليل المرفقات وretention وحق مشاركة التقرير؛ TLS لا يصحح إرفاق ملف سابق.

**المحجوب وحدود المعرفة:** خادم SMTP والتسليم والتفويض غير متاحة. Print يعيد توليد PDF المبيعات، فلا يعمم عليه عيب الملف القديم اليدوي.

**الدليل المحلي:** `SmartAuditERP/Form_WPF/frmEmailMang.xaml.cs:57-108`؛ `SmartAuditERP/Form_WPF/frmEmailMang.xaml.cs:137-191`؛ `SmartAuditERP/Form_WPF/frmCloseShift.xaml.cs:2389-2401`؛ `SmartAuditERP/Form_WPF/ClosShiftAndroid.xaml.cs:1820-1839`؛ `SmartAuditERP/Class/Print.cs:1194-1209`؛ `SmartAuditERP/Form_WPF/ClosShiftAndroid.xaml.cs:1732-1764`؛ `SmartAuditERP/Form_WPF/ClosShiftAndroid.xaml.cs:1820-1888`؛ `SmartAuditERP/Form_WPF/frmCloseShift.xaml.cs:1579-1586`؛ `SmartAuditERP/Form_WPF/FormCreateTicket.xaml.cs:74-110`؛ `SmartAuditERP/Class/SupportTicketApiClient.cs:49-79`؛ `SmartAuditERP/Class/Print.cs:1158-1238`؛ `SmartAuditERP/Form_WPF/frmSendEmail.xaml.cs:1-165`

**التتبع:** INV6-01، INV6-27، INV6-28؛ خطط P6T-67، P6T-68، P6T-69، P6T-70، P6T-77، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-11 — Support API — التذكرة والرد والمرفقات

**المدخل وإمكان الوصول:** FormCreateTicket وعميل HttpClient بمهلة30ث؛ مسار التفاصيل يهمل DTO، والإنشاء لديه تعطيل زر أثناء انتظار المهمة.

**البيئة والعنوان والإصدار:** apiBaseUrl إلى Create/Number/GetTicketsBycustomer/AddReply؛ schema وإصدار backend غير مرفقين.

**الهوية والتوثيق والنطاق:** الواجهة ترسل اسم/بريد/هاتف وbranch1؛ لا تثبت هذه القيم المصادقة. auth/ownership يفحصان في test backend بعقد معلوم.

**الطلب والثوابت قبل الإرسال:** subject/body/category/priority وbranch/context صحيحان، مرفقات بملكية وحدود حجم/عدد/نوع؛ path/query مرمزان وDTO متفق.

**النتيجة والربط:** HTTP وbody.Success وTicket/Number/schema؛ Empty ليست Failed، وnotfound/forbidden/unauthenticated نتائج مختلفة.

**الاستدامة والإعادة والمطابقة/العكس:** operationId لإنشاء/رد بعد timeout، ومسودة لا تمسح قبل قبول موثق، ومرفقات لا تبقى مختارة من تذكرة سابقة؛ pagination إن وفرها الخادم توثق.

**النقل والمهل والإلغاء والحدود:** 30ث حارس موجود لا ينفى؛ cancellation/lifecycle/retry/401/429/5xx وتفاصيل النتيجة تحتاج عقداً.

**الخصوصية والتفويض:** ملكية التذكرة/المرفق وretention والتحقق من محتوى base64 على الخادم، لا IDOR مفترض؛ بقاء مرفقات الواجهة P2-015 لا يعاد عده.

**المحجوب وحدود المعرفة:** backend وauth والاحتفاظ وحذف المرفق غير متاحة؛ لم يستعمل رقم تذكرة أو بيانات عميل حقيقي.

**الدليل المحلي:** `SmartAuditERP/Class/SupportTicketApiClient.cs:120-149`؛ `SmartAuditERP/Class/TicketDetailsResponse.cs:1-8`؛ `SmartAuditERP/Class/TicketDetailsApiResponse.cs:1-10`؛ `SmartAuditERP/Form_WPF/FormCreateTicket.xaml.cs:148-163`؛ `SmartAuditERP/Class/SupportTicketApiClient.cs:86-117`؛ `SmartAuditERP/Class/SupportTicketApiClient.cs:151-221`؛ `SmartAuditERP/Class/ApiResponse.cs:1-12`؛ `SmartAuditERP/Class/ApiResponseBase.cs:1-10`؛ `SmartAuditERP/Form_WPF/FormCreateTicket.xaml.cs:94-110`؛ `SmartAuditERP/Form_WPF/FormCreateTicket.xaml.cs:74-110`؛ `SmartAuditERP/Class/SupportTicketApiClient.cs:49-79`؛ `SmartAuditERP/Class/TicketAttachmentDto.cs:1-12`؛ `SmartAuditERP/Class/CreateTicketDto.cs:1-28`؛ `SmartAuditERP/Class/TicketDetails.cs:1-24`

**التتبع:** INV6-01، INV6-10، INV6-28، INV6-29؛ خطط P6T-47، P6T-48، P6T-49، P6T-50، P6T-77، P6T-78، P6T-79؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-12 — DeviceLicense — authorize وcache والأوفلاين

**المدخل وإمكان الوصول:** Home.CheckLicense وStartDailyCheck/ShowtrialOfflin وActivateOnlineLicense؛ لا تفعيل أو تعديل ملف رخصة جرى.

**البيئة والعنوان والإصدار:** baseUrl + /api/DeviceLicense/authorize وcache تحت StartupPath؛ issuer/signed schema/policy version خارج النسخة.

**الهوية والتوثيق والنطاق:** Company/DeviceId/Email/DeviceName قيم عميل وليست مصدراً موثوقاً للاستحقاق؛ توقيع جهة إصدار وربط tenant/audience/device لازمان.

**الطلب والثوابت قبل الإرسال:** payload typed متفق؛ لا يفترض عقد أسماء ValueTuple من دون serializer/server. تواريخ وميزات وسياسة grace واضحة.

**النتيجة والربط:** HTTP2xx لا يعني license valid؛ تحقق schema/signature/device/expiry ثم نتيجة حفظ فعلية قبل true/Features.

**الاستدامة والإعادة والمطابقة/العكس:** last-known-good وtemp/atomic replace، transient لا revoke، زمن أوفلاين يتقدم وgrace محدود؛ لا تمديد إداري عشوائي.

**النقل والمهل والإلغاء والحدود:** HttpClient افتراضي وICMP probe وNTP/UDP؛ المهل/الإلغاء وسياسة الوقت الموثوق غير متاحة. fallback لا يتجمد عند anchor.

**الخصوصية والتفويض:** Hardware ID والبريد والشركة تحتاج تقليل ومسوغ إرسال وretention؛ لا مفاتيح AES أو تراخيص حقيقية في الأدلة.

**المحجوب وحدود المعرفة:** خادم الإصدار وUID ومعيار توقيعه وسياسة الإبطال غائبة؛ لا تزوير أو تغيير ساعة أو تفعيل نفذ.

**الدليل المحلي:** `SmartAuditERP/Class/DeviceLicenseManager.cs:22-28`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:53-107`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:300-325`؛ `SmartAuditERP/Class/DeviceLicenseDto.cs:5-16`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:226-246`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:186-246`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:327-364`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:372-419`؛ `SmartAuditERP/Class/ManagerOnline.cs:337-375`؛ `SmartAuditERP/Home.xaml.cs:696-704`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:30-51`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:109-146`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:169-177`؛ `SmartAuditERP/Class/ManagerOnline.cs:574-649`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1115-1149`؛ `SmartAuditERP/Class/DeviceInfoDto.cs:1-16`

**التتبع:** INV6-01، INV6-14، INV6-15، INV6-30، INV6-31، INV6-32؛ خطط P6T-51، P6T-52، P6T-53، P6T-54، P6T-55، P6T-56، P6T-77، P6T-78، P6T-79؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-13 — ManagerOnline — الاستحقاق والتواصل

**المدخل وإمكان الوصول:** CheckLicenseStatus يستدعي بيانات المؤسسة وتفعيل ZATCA وفحص الجهاز وتاريخ الاشتراك؛ StartDailyCheck بعد30يوماً، وOnOff محلي منفصل.

**البيئة والعنوان والإصدار:** ManagerOnline.url ومسار getzatca-EndDate مع company/database؛ إصدار API والجهة المصدرة وسياسة الاشتراك غير مرفقة.

**الهوية والتوثيق والنطاق:** هوية الشركة/القاعدة/المستخدم تثبت في حد موثوق؛ parameters البشرية ليست تفويضاً وحيداً، وauth/TLS الخادم غير معلومين.

**الطلب والثوابت قبل الإرسال:** Active/ExpiringSoon/Expired/Inactive وendDate وتفعيل خدمة منفصلة عن الالتزام الضريبي؛ telemetry scope ومسوغ الإرسال واضحان.

**النتيجة والربط:** HTTP/body/status/issuer؛ Inactive رسالة فقط في المقطع وExpired يحدث DB لا cache. لا ادعاء إبطال فعلي لكل القنوات.

**الاستدامة والإعادة والمطابقة/العكس:** حالة استحقاق بإصدار ومدة وسياسة grace؛ تحديث ذري وإبطال cache. P1-032 باقية potential ومعاد جدولتها إلى8، لا علاج.

**النقل والمهل والإلغاء والحدود:** HttpClient وcatch لا يثبتان كل سياسة مهلة/retry/rate؛ موعد الفحص ونجاحه يفصلان، وفشل الفحص لا يختزل كنجاح.

**الخصوصية والتفويض:** حصر بيانات الاسم/البريد/الهاتف/المدينة/الجهاز/الميزات ومبررها وretention وحقوق الإدارة؛ لا إرسال telemetry فعلي هنا.

**المحجوب وحدود المعرفة:** backend entitlement وعدد الأجهزة وخصائص الاستحقاق غير متاحة؛ لا نفي auth أو إثبات أهلية من العميل وحده.

**الدليل المحلي:** `SmartAuditERP/Class/MainSetting.cs:12-18`؛ `SmartAuditERP/Class/Common.cs:1066-1088`؛ `SmartAuditERP/Class/InvoiceOper.cs:1473-1495`؛ `SmartAuditERP/Class/InvoiceOper.cs:1854-1884`؛ `SmartAuditERP/Class/InvoiceOperContract.cs:911-926`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:274-278`؛ `SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs:1115-1149`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:186-246`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:327-364`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:372-419`؛ `SmartAuditERP/Class/ManagerOnline.cs:337-375`؛ `SmartAuditERP/Home.xaml.cs:696-704`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:30-51`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:109-146`؛ `SmartAuditERP/Class/DeviceLicenseManager.cs:169-177`؛ `SmartAuditERP/Class/ManagerOnline.cs:574-649`؛ `SmartAuditERP/Class/ClListManagerOnline.cs:1-30`؛ `SmartAuditERP/Class/CustZatcaEndDate.cs:1-12`

**التتبع:** INV6-01، INV6-03، INV6-14، INV6-31، INV6-32؛ خطط P6T-03، P6T-04، P6T-53، P6T-54، P6T-77، P6T-78؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

### INT6-14 — AuditorAPI وWs_Auditor — متابعة عقود السحابة

**المدخل وإمكان الوصول:** Save يستقبل GetInvoiceCloudPaymentType وSendQrCode من المتابعة؛ متابعة محدودة لـP5، لا إعادة تدقيق المزامنة كلها.

**البيئة والعنوان والإصدار:** Sync.APIUrl وSDK خارجيان؛ hosts/schema/versions وserver tenant ACL غير متاحة.

**الهوية والتوثيق والنطاق:** User.CurrentCloudUser وClientCode وbranch/DistBranch ثابتة بالسياق؛ تحقق الخادم ومصدر التفويض مطلوبان.

**الطلب والثوابت قبل الإرسال:** نسخة payment mapping وinvoiceGlobalID/QR/hash/version ومالك الحقيقة؛ شكل envelope/التشفير وper-item acceptance يجب إثباته.

**النتيجة والربط:** IsValid وSendQrCode لا يفترضان Applied؛ accepted/rejected/unknown وACK مرتبطون بالعملية/الإصدار وفق عقد5.

**الاستدامة والإعادة والمطابقة/العكس:** intent/claim/cleanup محدد ومطابقة per item قبل إزالة queue؛ GL/cursor لا يسبقان الاعتماد، والقائمة الفارغة للربط تطبق.

**النقل والمهل والإلغاء والحدود:** HTTP/body/timeout/cancel/refresh/rate وCLearfiles/durability متطلبات دليل، لا عقد fake مخترع كضمان SDK.

**الخصوصية والتفويض:** عزل tenant/branch/resource/role وتنقيح الأسرار والمرفقات، وعدم اختبار cleanup على backlog عمل.

**المحجوب وحدود المعرفة:** H5-01/H5-03 لم يحسما؛ مصادر AuditorAPI/Ws_Auditor غائبة ولا اختبار partial/cleanup نفذ. ليست نتيجة إضافية عن5.

**الدليل المحلي:** `SmartAuditERP/Form_WPF/frmCloudPaymentSetting.xaml.cs:249-260`؛ `SmartAuditERP/Form_WPF/frmCloudPaymentSetting.xaml.cs:268-355`؛ `SmartAuditERP/Class/InvoiceOper.cs:5246-5274`؛ `SmartAuditERP/Class/InvoiceOper.cs:2666-2694`؛ `SmartAuditERP/Class/InvoiceOper.cs:2666-2694`؛ `SmartAuditERP/Form_WPF/frmInvsSyncStatusZatca.xaml.cs:511-519`

**التتبع:** INV6-01، INV6-08، INV6-10، INV6-11، INV6-12، INV6-21، INV6-22، INV6-25؛ خطط P6T-15، P6T-16، P6T-45، P6T-46، P6T-74، P6T-76، P6T-78، P6T-79، P6T-80؛ جميعها غير منفذة. المراجع: none؛ none تعني أنه لم تقرأ وثيقة مزود مباشرة لهذا العقد، لا غياب عقد حقيقي.

## 3. ثوابت القبول32 — ليست نتائج إضافية أواختبارات ناجحة

| المعرف | الثابت | المطلوب عند القبول | النتائج والقبول غير المنفذ |
|---|---|---|---|
| INV6-01 | سياق العملية ثابت وهوية الطرف والبيئة محددة | Tenant/branch/user/device/environment/operation/version ثابتة عبر await/restart ولا تستخدم credentials من سياق آخر. | P6-002، P6-012، P6-021، P6-026، P6-029، P6-031 / P6T-01، P6T-02، P6T-23، P6T-24، P6T-51، P6T-52، P6T-57، P6T-58، P6T-61، P6T-62، P6T-71، P6T-75، P6T-76، P6T-77، P6T-78، P6T-79، P6T-80 |
| INV6-02 | نوع الفاتورة قرار واحد قبل side effects | نوع standard/simplified/note والبوابة والتوقيت يخرجان من قرار متحقق واحد لا من قواعد VATno مختلفة. | P6-001، P6-002 / P6T-01، P6T-02، P6T-03، P6T-04، P6T-71 |
| INV6-03 | تغيير سياسة التكامل يسري بوضوح بعد اعتماده | الحالة DB/cache/UI والعقد متفقة؛ لا إعلان إيقاف بينما بوابة التنفيذ تحتفظ بقيمة قديمة. | P6-002 / P6T-03، P6T-04 |
| INV6-04 | معنى فئة الضريبة وسببها وعملتها محفوظ | لكل سطر وفئة/معدل وحصة خصم هوية صحيحة؛ لا تحويل الصفر تلقائياً إلى أدوية ولا وسم عملة/بلد غير مدعومين بصمت. | P6-003 / P6T-05، P6T-06، P6T-71 |
| INV6-05 | دقة الكمية والسعر مستقلة عن تقريب المبالغ | لا تضيع كمية كسرية أو دقة سعر مطلوبة؛ rounding mode وscale معتمدان ولا تقسيم على صفر أو nonfinite. | P6-004، P6-013 / P6T-07، P6T-08، P6T-25، P6T-26، P6T-71 |
| INV6-06 | مجاميع payload تطابق بنوده والأصل المالي | صافي/ضريبة/خصم/استقطاع/إجمالي الرأس مشتقة من نفس اللقطة؛ تطابق breakdown لكل taxType/category/rate. | P6-003، P6-004، P6-013، P6-018 / P6T-05، P6T-06، P6T-07، P6T-08، P6T-25، P6T-26، P6T-35، P6T-36، P6T-71، P6T-80 |
| INV6-07 | السلسلة تخص EGS/POS المقرر لا نوعاً محلياً عرضياً | ICV/PIH/previousUUID تُدار ضمن scope موثق وبالتسلسل مع حالات first/gap/parallel/restart وأصل فاتورة/إشعار. | P6-005 / P6T-09، P6T-10، P6T-71، P6T-79 |
| INV6-08 | إعادة النقل لا تولد هوية/حمولة جديدة بلا سبب مصرح | للإعادة ذاتها UUID/operation/payload hash ثابتة؛ corrected rejected وثيقة جديدة مرتبطة بالأصل وفق العقد. | P6-005، P6-007، P6-008، P6-016، P6-017، P6-021 / P6T-09، P6T-10، P6T-71، P6T-76، P6T-79، P6T-80 |
| INV6-09 | القبول الأولي ليس validation نهائية أو تسليماً | TransportAccepted/SubmittedPending وCleared/Reported/Valid وRejected وUnknown حالات منفصلة لا bool عام. | P6-006، P6-016، P6-017، P6-033 / P6T-11، P6T-12، P6T-31، P6T-32، P6T-33، P6T-34، P6T-71، P6T-72، P6T-78، P6T-80 |
| INV6-10 | كل طلب واستجابة مرتبطان بهوية المستند ومصدره الصحيح | schema/sourceType/identity/internalId/UUID/submission/device/amount تفحص قبل التحميل أو الكتابة أو ختم نجاح؛ العقد لا يحمل من Inv فقط، والرد الحقيقي محفوظ لا كائن فارغ أو Rows[0] بلا تطابق. | P6-006، P6-009، P6-016، P6-017، P6-021، P6-024، P6-025 / P6T-11، P6T-12، P6T-17، P6T-18، P6T-31، P6T-32، P6T-33، P6T-34، P6T-47، P6T-48، P6T-49، P6T-50، P6T-71، P6T-72، P6T-73، P6T-76، P6T-78، P6T-80 |
| INV6-11 | نية المحاولة دائمة قبل الطلب غير القابل للعكس | operation/amount/context/payload محفوظة قبل الشبكة والجهاز؛ الحفظ المالي وoutbox لهما عقد اعتماد واضح. | P6-007، P6-008، P6-020، P6-021 / P6T-13، P6T-14، P6T-39، P6T-40، P6T-71، P6T-76، P6T-79، P6T-80 |
| INV6-12 | فشل التثبيت المحلي بعد قبول بعيد قابل للمطابقة | لا rollback وهمي لعملية خارجية ولا reissue عمياء؛ نتيجة remote تقارن بسجل محلي لاستكماله بمعاملة جديدة. | P6-007، P6-008، P6-016، P6-017، P6-021، P6-028 / P6T-13، P6T-14، P6T-15، P6T-16، P6T-31، P6T-32، P6T-71، P6T-72، P6T-76، P6T-79، P6T-80 |
| INV6-13 | الأرشيف يربط الأصل والمجاز ومحاولات النتيجة دون محو | كل UUID/hash/QR/XML/environment/response version وسبب تعديل محفوظة مع حقوق وretention؛ لا مجرد Sent=1. | P6-008، P6-010، P3-006 / P6T-15، P6T-16، P6T-17، P6T-18، P6T-71، P6T-79، P6T-80 |
| INV6-14 | غرض الاعتماد وبيئته وهويته لا يختلطان | key/cert/issuer/EGS/purpose/environment/validity ورابط النسخة متحققة، ولا fallback لإنتاج عند غياب sandbox أو العكس. | P6-010، P6-012، P6-019، P6-022 / P6T-19، P6T-20، P6T-23، P6T-24، P6T-37، P6T-38، P6T-43، P6T-44، P6T-71، P6T-78 |
| INV6-15 | تبديل اعتماد التشغيل معاملة حالة لا أوامر void متسلسلة | فشلGenerate/OTP/import/DB لا يمحو last-known-good ولا يسمح Saved/active؛ أعمدة وقيم ومعاملات الإدراج مكتملة. | P6-010، P6-011، P6-028 / P6T-19، P6T-20، P6T-21، P6T-22، P6T-55، P6T-56 |
| INV6-16 | مرجع التصحيح/المرتجع هو مستند الأصل المقصود | UUID/GlobalID/type/branch/issuer/line والحد المتبقي متحققون؛ ليس True/False ولا رقم من نوع ثابت غير مناسب. | P6-014 / P6T-27، P6T-28، P6T-72 |
| INV6-17 | وقت الإصدار Instant صحيح لا تاريخ عند منتصف الليل | يحفظ وقت الأصل وoffset؛ UTC حقيقي عند الحد الخارجي مع اختبارات انتقال اليوم والثقافة. | P6-015 / P6T-29، P6T-30 |
| INV6-18 | المبلغ النهائي يتحقق قبل أي طلب جهاز | amount/currency/remainder/version/net/paytype كلها صحيحة وثابتة قبل أول Pay/SALE؛ الحارس المتأخر لا يترك خصماً بلا سداد. | P6-020، P6-022 / P6T-39، P6T-40، P6T-43، P6T-44، P6T-73 |
| INV6-19 | محاولة جهاز واحدة لكل نية وهوية قابلة للتسوية | single-flight وidempotency مع correlation وRRN/STAN/approval اللازمة وفق عقد المورد؛ restart لا يخلق بيعاً جديداً. | P6-021 / P6T-41، P6T-42، P6T-73، P6T-74، P6T-79، P6T-80 |
| INV6-20 | نتيجة الدفع المجهولة لا تتحول إلى رفض مع دعوة إعادة البيع | timeout/short-response/disconnect يلزمها Query/Reconcile قبل retry؛ الرفض الصريح وحده Declined. | P6-020، P6-021، P6-022 / P6T-41، P6T-42، P6T-43، P6T-44، P6T-73، P6T-74، P6T-79 |
| INV6-21 | العكس والتسوية عمليات مستقلة مرتبطة بالأصل | reversal/refund/void/settlement لكل منها صلاحية وهوية وحالة وإعادة آمنة ومطابقة مبلغ/عملة/fees/GL قبل إغلاق العملية. | P6-021، P6-023، P4-016 / P6T-41، P6T-42، P6T-74، P6T-80 |
| INV6-22 | snapshot إعدادات الربط يقبل empty ويعتمد ذرياً | حذف آخر mapping يثبت ويعاد تحميله؛ فشل وسط الكتابة يرجع النسخة السابقة لا مزيجاً من النسختين. | P6-023 / P6T-45، P6T-46، P6T-74، P6T-76، P6T-80 |
| INV6-23 | OAuth مقيد بالمتجر والنطاق والتدوير الذري | state/redirect/merchant/scopes/expiry/refresh-token rotation/uninstall محكومة؛ لا reuse متوازي لrefresh أحادي الاستعمال. | P6-029 / P6T-57، P6T-58، P6T-75، P6T-78 |
| INV6-24 | كل الصفحات وحدود المزود جزء من عقد الجلب | صفحات متسلسلة وcursor/snapshot/version، و429/Retry-After/cache/401 معالجة محدودة؛ لا أول صفحة كاكتمال. | P6-030، P6-029 / P6T-59، P6T-60، P6T-75 |
| INV6-25 | طلب التجارة يطبق في ERP مرة بإصدار وأثر مالي/مخزني واضح | mapping merchant/customer/item/unit/payment وقرار cancel/refund/stock/GL متفق؛ replay لا يكرر السداد/الحركة. | P6-030، P6-023، P5-026 / P6T-59، P6T-60، P6T-75، P6T-76، P6T-79، P6T-80 |
| INV6-26 | الجلسة والمستلم يتبعان التفويض الحالي | حساب المرسل وprofile والرقم الدولي النهائي متحققون ومعزولون عن سياقERP آخر؛ لا kill شامل أو إعادة استعمال صامت. | P6-031، P6-032، P1-024 / P6T-61، P6T-62، P6T-63، P6T-64، P6T-77 |
| INV6-27 | الإشعار الجزئي والمجهول لا يعلن تسليماً كاملاً | تحضير ملف قبل النص، serialization لكل session، هوية محاولة ونتيجة لكل جزء، وإعادة محافظة على عدم التكرار. | P6-033، P6-035 / P6T-65، P6T-66، P6T-69، P6T-70، P6T-77، P6T-79، P6T-80 |
| INV6-28 | كل مرفق محدد الملكية والموافقة والنسخة | لا File.Exists كاختيار ضمني؛ preview/owner/context/hash/size/type/retention وصلاحية القراءة/الإرسال مستقلة. | P6-034، P6-033، P2-015 / P6T-65، P6T-66، P6T-67، P6T-68، P6T-77، P6T-80 |
| INV6-29 | عقد الدعم يميز empty/failed وHTTP/body/DTO | Ticket صالح عندSuccess، body success معتبر، URI مرمز، وفشل القائمة ليس صفراً ناجحاً أو إذناً للوصول. | P6-024، P6-025، P2-015 / P6T-47، P6T-48، P6T-49، P6T-50، P6T-77، P6T-78 |
| INV6-30 | cache الاستحقاق موثق من الجهة ومقيد بالجهاز/الشركة | توقيع جهة الإصدار الموثوق يتحقق قبل Features/expiry، DeviceId/tenant/audience مطابقون ولا digest عام كإثبات مصدر. | P6-026 / P6T-51، P6T-52، P6T-77 |
| INV6-31 | زمن/grace الأوفلاين يتقدم ولا يتراجع | آخر وقت موثوق ليس بديلاً ثابتاً لكل الأيام اللاحقة؛ تقدم monotonic وحدود grace وإعادة تشغيل وrollback موثقة. | P6-027 / P6T-53، P6T-54 |
| INV6-32 | فشل تجديد/حفظ عابر لا يمحو رخصة صحيحة | بديل متحقق يكتب ذرّياً بنتيجة واضحة؛ revoke الموثق منفصل عن network/disk/body errors. | P6-028، P1-032 / P6T-55، P6T-56، P6T-78، P6T-79 |

## 4. مصفوفة الفشل48 — لكل عقد حالة وربط قبول

[الـCSV الكامل](evidence/integration-failure-matrix-06.csv) يفصل الملاحظة المصدرية عن fault/precondition والأثر المشروط والضابط والحد والدليل.35 صفاً تربط النتائج الجديدة و13 للحدود المشتركة؛ ليست عدد حوادث أوعيوب إضافية، وكل `runtime_status=not-executed`.

| المعرف | الحالة أومجموعة الفشل | العقد | النتائج | خطة القبول |
|---|---|---|---|---|
| FM6-01 — | تصنيف الفاتورة الضريبية يختلف بين حارس الحفظ ومحول ZATCA | INT6-01 | P6-001 | P6T-01، P6T-02 |
| FM6-02 — | سياسة الإرسال اليدوي وإيقاف ZATCA لا تتطابق مع بوابات التنفيذ المخزنة بالذاكرة | INT6-01، INT6-02، INT6-13 | P6-002 | P6T-03، P6T-04 |
| FM6-03 — | محول ZATCA يختزل الفئات الضريبية وخصومات المعدلات المتعددة إلى قيم ثابتة | INT6-01 | P6-003 | P6T-05، P6T-06 |
| FM6-04 — | توليد ZATCA يقرب الكمية وسعر الوحدة مبكراً ويمر بمقامات غير محروسة | INT6-01 | P6-004 | P6T-07، P6T-08 |
| FM6-05 — | مراجع السلسلة الضريبية مشتقة من رقم ناقص1 داخل النوع لا من تسلسل وحدة إصدار صريح | INT6-01، INT6-04 | P6-005 | P6T-09، P6T-10 |
| FM6-06 — | نجاح ZATCA يستنتج من غياب الأخطاء وتضيع الاستجابة الفعلية في الغلاف المحلي | INT6-01، INT6-02 | P6-006 | P6T-11، P6T-12 |
| FM6-07 — | إرسال الضريبة وحفظ المستند المحلي يتركان فجوات قبول بعيد وحالة محلية غير معتمدة | INT6-01 | P6-007 | P6T-13، P6T-14 |
| FM6-08 — | الإرسال اليدوي الناجح لا يحفظ UUID وQR وXML المعادين من ZATCA | INT6-01، INT6-14 | P6-008 | P6T-15، P6T-16 |
| FM6-09 — | متابعة الفواتير تعرض العقود لكن محمل الصف المختار يبحث في Inv وحده | INT6-01 | P6-009 | P6T-17، P6T-18 |
| FM6-10 — | حفظ إعداد ZATCA يستمر بعد فشل إنشاء الاعتماد ويستبدل شهادة قائمة دون وحدة اعتماد | INT6-02 | P6-010 | P6T-19، P6T-20 |
| FM6-11 — | فرعا إنشاء صف اعتماد ZATCA الجديد لا يطابقان أعمدة INSERT وقيمه ومعاملاته | INT6-02 | P6-011 | P6T-21، P6T-22 |
| FM6-12 — | قارئ اعتماد ZATCA يختار حقول الإنتاج مهما كانت بيئة الطلب | INT6-01، INT6-02 | P6-012 | P6T-23، P6T-24 |
| FM6-13 — | محول فاتورة ETA يقرب الكمية إلى عدد صحيح بينما يحسب القيمة من الكمية الأصلية | INT6-03 | P6-013 | P6T-25، P6T-26 |
| FM6-14 — | محول إشعار ETA الدائن يكتب نص Boolean بدلاً من المرجع المدخل | INT6-03، INT6-04 | P6-014 | P6T-27، P6T-28 |
| FM6-15 — | محولا ETA يسقطان وقت الإصدار والفاتورة تلحق Z دون تحويل UTC | INT6-03، INT6-04 | P6-015 | P6T-29، P6T-30 |
| FM6-16 — | إرسال فاتورة ETA يعيد false حتى بعد تحديث UUID ويخلط القبول الأولي بحالة المستند | INT6-03 | P6-016 | P6T-31، P6T-32 |
| FM6-17 — | إرسال إيصال ETA يعيد true لكل رد غير استثنائي ثم تختم المتابعة الفاتورة مرسلة | INT6-04 | P6-017 | P6T-33، P6T-34 |
| FM6-18 — | مدخل إيصال ETA لا يوفق صافي الرأس وتفصيل الخصومات والاستقطاع مع بنوده | INT6-04 | P6-018 | P6T-35، P6T-36 |
| FM6-19 — | BaseUrl إيصال ETA غير الإنتاجي يشير إلى مضيف الهوية بدلاً من API الموثق | INT6-04 | P6-019 | P6T-37، P6T-38 |
| FM6-20 — | استدعاء جهاز الدفع يسبق استكمال التحقق من المبلغ والباقي في حواري POS | INT6-05 | P6-020 | P6T-39، P6T-40 |
| FM6-21 — | لا يظهر ربط دائم لمحاولة الجهاز بالدفعة المحلية أو مسار unknown قبل إعادة الدفع | INT6-05، INT6-06 | P6-021 | P6T-41، P6T-42 |
| FM6-22 — | أزرار اختبار الدفع تبني طلبات بيع لا فحص اتصال محايداً وNeo لا ينتظر النتيجة | INT6-05، INT6-06 | P6-022 | P6T-43، P6T-44 |
| FM6-23 — | حذف آخر ربط دفع سحابي من الواجهة لا يحذف صفه المحفوظ | INT6-14، INT6-08 | P6-023 | P6T-45، P6T-46 |
| FM6-24 — | عميل تفاصيل تذكرة الدعم يهمل الجسم المحلل ويعيد نجاحاً مع Ticket غير مهيأ | INT6-11 | P6-024 | P6T-47، P6T-48 |
| FM6-25 — | طلبات الدعم تخلط HTTP2xx بنجاح الأعمال وتعيد القائمة الفاشلة كأنها خالية | INT6-11 | P6-025 | P6T-49، P6T-50 |
| FM6-26 — | توقيع ملف الترخيص المحلي SHA256 غير سري ولا يربط الحمولة بالجهاز الحالي | INT6-12 | P6-026 | P6T-51، P6T-52 |
| FM6-27 — | زمن التحقق الأوفلاين يتجمد عند آخر تاريخ شبكة بدلاً من تقدم الوقت | INT6-12، INT6-13 | P6-027 | P6T-53، P6T-54 |
| FM6-28 — | فشل تجديد الترخيص قد يمحو cache صالحاً والحفظ الفاشل لا يمنع true | INT6-12 | P6-028 | P6T-55، P6T-56 |
| FM6-29 — | دورة OAuth لسلة في المستودع لا تتجاوز تبادل code بعائد access token فقط | INT6-07 | P6-029 | P6T-57، P6T-58 |
| FM6-30 — | عينة سلة تعد أول صفحة وتضيف منتجاً ثابتاً ولا تثبت دورة ربط الطلب بالمحاسبة والمخزون | INT6-08 | P6-030 | P6T-59، P6T-60 |
| FM6-31 — | جلسة WhatsApp تحتفظ بملف Chrome ثابت لا يرتبط بسياق ERP وتطلب تعطيل sandbox | INT6-09 | P6-031 | P6T-61، P6T-62 |
| FM6-32 — | تهيئة رقم WhatsApp تضيف966 حتى للأرقام الدولية التي تبدأ بعلامة زائد | INT6-09 | P6-032 | P6T-63، P6T-64 |
| FM6-33 — | نتيجة WhatsApp تخلط نقرة الإرسال بالتسليم وقد ترسل النص قبل فشل الملف | INT6-09 | P6-033 | P6T-65، P6T-66 |
| FM6-34 — | نافذة البريد ترفق آخر ملف إغلاق ثابت تلقائياً دون ربطه بالوردية الحالية | INT6-10 | P6-034 | P6T-67، P6T-68 |
| FM6-35 — | فرع بريد إغلاق Android يستدعي الإرسال مرتين عندما يكون Type=3 والطابعة محددة | INT6-10 | P6-035 | P6T-69، P6T-70 |
| FM6-36 — | ZATCA: رفض أو تحذير أو قبول مجهول ثم انهيار | INT6-01 | P6-005، P6-006، P6-007، P6-008 | P6T-71، P6T-78، P6T-79 |
| FM6-37 — | ZATCA: فشل OTP أو الشهادة أو القرص أثناء تبديل الاعتماد | INT6-02 | P6-010، P6-011، P6-012، P1-033 | P6T-19، P6T-20، P6T-21، P6T-22، P6T-23، P6T-24، P6T-78 |
| FM6-38 — | ETA: قبول أولي أو جزئي ثم حالة نهائية أو إلغاء/رفض متأخر | INT6-03، INT6-04 | P6-014، P6-016، P6-017 | P6T-31، P6T-32، P6T-33، P6T-34، P6T-72، P6T-78 |
| FM6-39 — | الدفع: رفض أو إلغاء أو رد قصير أو انقطاع ونتيجة مجهولة | INT6-05، INT6-06 | P6-020، P6-021، P6-022 | P6T-39، P6T-40، P6T-41، P6T-42، P6T-43، P6T-44، P6T-73، P6T-79 |
| FM6-40 — | الدفع: العكس والاسترداد الجزئي والتسوية | INT6-05، INT6-06، INT6-14 | P6-021، P6-023، P4-016 | P6T-41، P6T-42، P6T-45، P6T-46، P6T-74، P6T-80 |
| FM6-41 — | سلة: state أو متجر مختلف أو refresh متوازٍ أو uninstall | INT6-07 | P6-029 | P6T-57، P6T-58، P6T-75، P6T-78 |
| FM6-42 — | سلة والrelay: صفحات و429 وcache وطلب مدفوع مكرر | INT6-08، INT6-14 | P6-029، P6-030، P6-023، P5-026 | P6T-45، P6T-46، P6T-57، P6T-58، P6T-59، P6T-60، P6T-75، P6T-76، P6T-79، P6T-80 |
| FM6-43 — | WhatsApp: تبديل حساب وتداخل جلسة أو قبول إرسال مجهول | INT6-09 | P6-031، P6-032، P6-033، P1-024 | P6T-61، P6T-62، P6T-63، P6T-64، P6T-65، P6T-66، P6T-77، P6T-79، P6T-80 |
| FM6-44 — | SMTP: ملف قديم أو إرسال مكرر أو قبول مجهول | INT6-10 | P6-034، P6-035 | P6T-67، P6T-68، P6T-69، P6T-70، P6T-77، P6T-79، P6T-80 |
| FM6-45 — | الدعم: HTTP وbody وDTO وهوية التذكرة والمرفق | INT6-11 | P6-024، P6-025، P2-015 | P6T-47، P6T-48، P6T-49، P6T-50، P6T-77، P6T-78، P6T-79 |
| FM6-46 — | الترخيص: أصالة وزمن وتجديد وفشل قرص | INT6-12 | P6-026، P6-027، P6-028، P1-032 | P6T-51، P6T-52، P6T-53، P6T-54، P6T-55، P6T-56، P6T-77، P6T-78، P6T-79 |
| FM6-47 — | ManagerOnline: Inactive وExpired وcache وخصوصية الاستحقاق | INT6-13 | P6-002، P6-027، P6-028، P1-032 | P6T-03، P6T-04، P6T-53، P6T-54، P6T-77، P6T-78 |
| FM6-48 — | AuditorAPI وWs_Auditor: عقد قبول جزئي وتشفير/هوية وcleanup محجوب | INT6-14 | P6-023، P5-010، P5-015، P5-016، P5-018، P5-021، P5-022، P5-023، P5-025، P5-026، P5-029 | P6T-45، P6T-46، P6T-74، P6T-76، P6T-78، P6T-79، P6T-80 |

### تصنيف الأخطاء المطلوب دون تخمين سلوك المورد

- **قبل الطلب:** validation أوauthorization أوconfig/schema أوcredential mismatch. فشل محلي مؤكد لا يرسل طلباً؛ لا fallback لبيئة أومستأجر آخر.
- **HTTP:** افحص status ثمbody/schema/business/identity. قد تعني2xx انتظاراً أورفض أعمال بحسب العقد.401 لها refresh بميزانية وسياق مقيدين؛403 ليست سبباً لتبديل الهوية.429 وRetry-After/backoff حسب المرجع، و5xx قد تترك أمراً mutating فيUnknown.409/422 يفسران بحسب كلendpoint لا بتعريف موحد.
- **SDK/native:** null أوshort reply أوexception أوtimeout ليست رفضاً مفترضاً. وثق ABI وencoding وamount units وstatus وquery/refund بالعقد الحقيقي قبل fake القبول. لا تستنتجHTTP من حقلstatus200 في الإيصال.
- **بعد القبول:** فشل local commit أوdisk/archive/notification لا يلغي عملية المزود. Match/Resume بالهوية نفسها؛ التعويض عملية مخولة جديدة مرتبطة بالأصل.
- **الإلغاء:** إلغاء انتظارUI أوTask لا يعني سحب طلب وصل إلى المزود. منع النقر الثاني مفيد، لكنه ليس دفتر محاولة دائماً.
- **الجلب:** failed ليستempty؛page/cursor يتقدم بعدapply للمدى المثبت. version/snapshot يمنعان إسقاط المتأخر أوتكرار الدفعة/GL/المخزون.
- **المرفقات والإشعارات:** لا جهة أوملف من سياق سابق؛ تقليل وإذن ومعاينة وحالة لكل جزء ومحاولة. التسليم لا يستنتج منDOM click أوSMTP.Send.

## 5. سجل المراجع الرسمية وحدود المقارنة

تاريخ مرجع الجلسة المعلن هو2026-11-16. أظهرت ساعة بيئة التوثيق2026-11-17؛ سجل هذا الاختلاف وتاريخ جلب المراجع العامة منفصلين في provenance06 وسجل المراجع. لا يمثل أي منهما اختبار تطبيق/مزود أوتغيير ساعة/رخصة. تواريخ وحزم1–5 التاريخية محفوظة.

كل الروابط عامة ورسمية وقرئت read-only. **لم تحفظbodies ولا بصمات محتواها، ولا يتحقق validator من توافرها الحالي عبر الشبكة.** الوصول إلى صفحة أوتاريخ تحديثها ليس مصادقةSDK أوشهادة امتثال. يحفظ السجل URL والإصدار والأجزاء المقروءة والفاشلة والقاعدة المستخدمة وحد المقارنة. لم يحصل التدقيق على مرجعvendor رسمي لدلالات Geidea/NeoLeap أوABI؛ بقيت مجهولة صراحة.

| المعرف والجهة | المصدر | ما قرئ | المستخدم وحده وحد المقارنة |
|---|---|---|---|
| REF6-01 — ZATCA | [E-Invoice specifications — official developer hub](https://zatca.gov.sa/en/E-Invoicing/SystemsDevelopers/Pages/E-Invoice-specifications.aspx)<br>الصفحة تعرض تحديث12 يناير2026 وتربط وثائق19 مايو2023؛ ليس إصدار XML جديداً مؤرخاً2026. | chunk0 وchunk2؛ قراءة الروابط/السياق وليست مراجعة كل المواد المرتبطة. | تحديد أصل المواصفات والقرار وXML؛ وجود SDK لا يثبت امتثالاً أو حداثة الإصدار. المراجع التي لم تفتح أو أجزاء navigation لا تعد مقروءة؛ يلزم التحقق من الإصدار المنطبق عند إعداد مرشح التشغيل. |
| REF6-02 — ZATCA | [Implementation Resolution — English PDF](https://zatca.gov.sa/en/E-Invoicing/Introduction/LawsAndRegulations/Documents/20230519_E-Invoicing%20Implementation%20Resolution%20English.pdf)<br>19 مايو2023؛ الترجمة الإنجليزية غير رسمية والنص العربي مرجع التعارض. | chunks0 و2 و3 و4 من8؛ chunk1 فشل، وإعادة chunk3 فشلت502 بعد قراءة سابقة؛ chunk4 أعيدت بنجاح. ليست قراءة PDF كاملة. | clearance للنوع القياسي قبل المشاركة وreporting للمبسط خلال24ساعة حيث ينطبق؛ حماية المفاتيح والأرشيف والسلسلة/العداد وعدم التعديل غير المنضبط، والتعامل مع تعطل/أوفلاين. ليس رأياً قانونياً أو تحديد موجة إلزام المنشأة أو مراجعة Security Standard/XSD كاملة؛ تنطبق التفاصيل على نطاق المكلف/النوع/المرحلة المحدد. |
| REF6-03 — ZATCA | [Electronic Invoice XML Implementation Standard](https://zatca.gov.sa/ar/E-Invoicing/SystemsDevelopers/Documents/20230519_ZATCA_Electronic_Invoice_XML_Implementation_Standard_%20vF.pdf)<br>v1.2 —19 مايو2023، كما ربطته البوابة عند القراءة. | chunks0–5 من7؛ chunk6 فشل؛ chunk3 أعيدت بنجاح. ليست مراجعة schema أو cryptographic profile كاملة. | كمية/سعر بدقة مستقلة عن amounts، تقريب المبالغ وقواعد half-up حيث تحدد؛ breakdown للفئة/المعدل/الخصومات، وفصل عملة المستند عن عملة الضريبة SAR عند اللزوم. القواعد التي لم تقرأ لا تنسب لهذه المراجعة؛ النشاط/العملة/الفئات القانونية تحدد قبل اختبار أو حكم امتثال. |
| REF6-04 — ETA | [Submit Documents — eInvoice API](https://sdk.invoicing.eta.gov.eg/einvoicingapi/01-submit-documents/)<br>صفحة API الرسمية المقروءة؛ لا تعني نسخة ETA_Invoice المحلية. | chunks0 و2؛ ليست كل chunks. | HTTP202 قبول للمعالجة لا validation نهائية؛ submissionUUID وaccepted/rejected documents وربط internalId. schema/تعريف returnds وترجمة HTTP داخل المكتبة غير متاحة؛ لا تفسير raw HTTP من أسماء DataTables وحدها. |
| REF6-05 — ETA | [Submit Receipts — eReceipt API](https://sdk.invoicing.eta.gov.eg/ereceiptapi/02-submit-receipt/)<br>صفحة API الرسمية؛ نسخة Valley وserializer غير معلومتين. | كلا الجزأين المقروءين من الصفحة. | 202 أولي وربط submission/UUID؛ duplicate422 وthrottle وRetry-After حيث ينطبقان، لا إعادة عمياء. الرمز200 في send_respons_model حقل SDK لا raw HTTP مثبت؛ الترجمة والانتظار الداخلي يحتاجان عقداً. |
| REF6-06 — ETA | [Integration Practices](https://sdk.invoicing.eta.gov.eg/integrationpractices/)<br>ممارسات تكامل رسمية، ليست كود SDK المحلي. | الجزآن المقروءان؛ استعمال الممارسات ذات الصلة فقط. | callback أوsubmission polling وحفظ التوكين وفق عمره وتحديث ERP بعد المعالجة؛ تجنب تكرار submit بعد20x أو استعمال printout كبديل للمتابعة. لا نجزم أن SDK لا يوفر polling/cache؛ المطلوب إثبات ذلك عند حد النتيجة الذي يعتمد عليه العميل. |
| REF6-07 — ETA | [Get Submission — eInvoice API](https://sdk.invoicing.eta.gov.eg/einvoicingapi/09-get-submission/)<br>عقد متابعة submission للفواتير. | الصفحة المقروءة كاملة في نتيجة الجلب. | overall in-progress/valid/partially-valid/invalid وحالات المستند submitted/valid/invalid/rejected/cancelled، مع الهوية والصفحات. لا اختبار callback/polling أوتأكيد وصول نسخة بيانات فعلية؛ صلاحيات إلغاء/رفض وسياساتها تحتاج سياقاً مستقلاً. |
| REF6-08 — ETA | [Get Receipt Submission — eReceipt API](https://sdk.invoicing.eta.gov.eg/ereceiptapi/06-get-receipt-submission/)<br>عقد متابعة submission للإيصالات. | chunk0 من2 فقط؛ بقية الصفحة غير معدودة ضمن القراءة. | overall InProgress/Valid/Invalid وحالات receipt Valid/Invalid/Cancelled وربطUUID/receiptNumber/POS والصفحات. لا استنتاج لدعمكل callback/cancel من chunk واحد أو لعقد return receipt الذي لم يجلب مباشرة. |
| REF6-09 — ETA | [Invoice v1.0 — document schema](https://sdk.invoicing.eta.gov.eg/documents/invoice-v1-0/)<br>Invoice v1.0؛ أي typeVersion أخرى تحتاج مرجعاً موافقاً. | chunks0 و1 من3؛ chunk1 يتضمن تعريفات quantity/amountEGP/discount/tax/line totals. | وقت إصدار UTC؛ quantity كمية decimal موجبة، amountEGP حتى5 منازل بحسب التعريف، وnetTotal/taxTotals وline totals متسقة. حد5 منازل المذكور amountEGP لا تعميم تلقائي على كل حقل؛ لا مراجعة SDK setter/serializer أو كل schema. |
| REF6-10 — ETA | [Retail Receipt v1.2 — document schema](https://sdk.invoicing.eta.gov.eg/documents/retail-receipt-v1-2/)<br>Retail Receipt v1.2 كما يطلبه المحول محلياً؛ تحقق wire/version مطلوب. | الجزآن المقروءان مع إعادة قراءة أجزاء. | UTC وpreviousUUID على POS، فارغ لأول إيصال وفق شروطه؛ quantity عشرية؛ netAmount مجموع line net لا totalAmount، ومجاميع الخصم/الضريبة لها معانٍ منفصلة. مخطط Return Receipt لم يجلب مباشرة؛ لا نفترض wire لسلاسل s/r أوإعادة حساب Valley من أسماء حقولها. |
| REF6-11 — ETA | [Credit Note v1.0 — document schema](https://sdk.invoicing.eta.gov.eg/documents/credit-note-v1-0/)<br>Credit Note v1.0، type c. | chunk0 من3 فقط. | UTC وreferences لUUID الأصل حيث تنطبق؛ salesOrderReference حقل مختلف لا يحول Boolean إلى مرجع صحيح. references اختيارية في schema مع قيود الحالة؛ لا ادعاء رفض كل إشعار لا يحتويها أو مراجعة كل شروط الإشعار. |
| REF6-12 — ETA | [Frequently Asked Questions — environment separation](https://sdk.invoicing.eta.gov.eg/faq/)<br>FAQ رسمية؛ استخدم جزء مضيفاتAPI/identity فقط. | الصفحة المقروءة كاملة؛ لم تتبع تعليمات تشغيل/تثبيت أوPostman. | فصل API عن مضيف الهوية بين preproduction/production ومراجعةURI النهائي. لا اعتماد لنصيحة قديمة بتعطيل TLS أوإضافة root اختباري للإنتاج؛ config_class قد يعيد تحديد العنوان داخلياً. |
| REF6-13 — Salla | [OAuth2 Authorization](https://docs.salla.dev/421118m0)<br>تعرض الصفحة تعديل18 أغسطس2026؛ نموذج التطبيق/طريقة النشر الفعلية غير معلومين. | body chunks3–6؛ chunks0–2 كانت navigation، ليست قراءة مضمون OAuth إضافية. | state وregistered redirect وmerchant user-info وscopes/expiry؛ refresh أحادي الاستعمال مع تدوير ذري وتجنب إعادة استعمال متوازية، وEasy Mode للتطبيقات المنشورة حسب الصفحة. لا Authorization/Refresh/Uninstall جرى؛ لا تحفظ أعماراً ثابتة بلا مراجعة عقد التطبيق وقت التنفيذ، ولا تنف إعداد backend خارج المستودع. |
| REF6-14 — Salla | [List Orders](https://docs.salla.dev/orders/list)<br>تعرض تعديل8 أكتوبر2026؛ Admin API orders. | body chunk3 وأمثلة chunk4 من6، لا كل الصفحة. | تتابع الصفحات دون قفز وper_page/cache/date filters وفق endpoint؛ expanded مهمل من1 سبتمبر2026 وفق الصفحة. العينة لا تقرأ expanded أصلاً فلا ينسب له فشلها؛ شروط endpoints المنتجات/العملاء/الwebhooks لا تستنتج من orders وحدها. |
| REF6-15 — Salla | [Rate Limiting](https://docs.salla.dev/rate-limiting)<br>حدود ديناميكية مرتبطة بالخطة/endpoint وليست quota واحدة. | body chunks3–4 من5؛ navigation ليست مضموناً مقروءاً. | headers وحدود الخطة/المورد وRetry-After/backoff؛ لا عدد موحد hardcoded لكل المتاجر. لا rate-load test أوحساب مزود استعمل؛ الرقم المنشور لمورد معين لا يعمم على كل الموارد/التطبيقات. |

## 6. متابعات محجوبة مسماة — لا نتائج إضافية

| المعرف والمتابعة | المجهول أوالاعتماد | شرط القبول المتبقي | مرحلة مرشحة |
|---|---|---|---|
| H6-01 — عقد ZATCA SDK وXSD/security والبيئة | مصدر/DTO وGenerateInvoiceXML وUUID/hash/PIH وIsProduction/Simulation وraw response/timeout/auth؛ هوية EGS ونسخة الشهادة ووثيقة اختبار معتمدة. لم تفحص كل مواصفات security أوXML. | حسم P6-005 وشروط001/003/004/006–012 وP6T-71/78/79 قبل حكم امتثال أوsandbox. لا مفاتيح في الدردشة. | 8 |
| H6-02 — عقد ETA_Invoice وValley والتوقيع والحالة النهائية | أنواع InvoiceLine/returnds/send_respons_model وconfig/serializer/status/polling وreturn schema الفعلية؛ token/cert/PIN/timezone. لا تفسير200 على أنه raw HTTP. | توثيق handoff ثم التقاط payload وaccepted/rejected/internalId/submission والحالة النهائية والعكس بخطط25–38 و72/78. مدخل frmSentEinvoice نفسه يحتاج7. | 7;8 |
| H6-03 — عقد أجهزة الدفع وABI والمطابقة | UtilitiesProj وGeideaPament وmadaapi وneoleapconnector بإصدار/معمارية/firmware موثوقين؛ statuses وunits وencoding وQuery/Reversal/settlement/receipt. لا caller POS مباشر لـNeo ProcessSale مثبت. | حسم potential P6-021 دون دفع حي، وإثبات39–44 و73/74/79؛ لا double-charge مفترض أو اختبار اتصال مالي على إنتاج. | 8 |
| H6-04 — سلة: النشر وOAuth والrelay وربط ERP | Easy/Custom mode والتطبيق المسجل وscopes/state/merchant وbackend/webhooks/refresh store؛ orders/payment/stock truth وmapping. العينة ليست ميزة منشورة مثبتة. | حسم فجوتي029/030 ومداخل P1-033 في7، ثم57–60/75/76/80 بإذن8. لا CRUD أوtoken حقيقي هنا. | 7;8 |
| H6-05 — قنوات الرسائل والدعم والمرفقات والخصوصية | هوية مرسل WhatsApp وprofile وسياسة المزود وSMTP/send-as/TLS/bounce وAPI schema/ownership/size/retention/consent وقوالب التقرير الخارجية. لا IDOR أوتسليم مثبت. | خطط47–50 و61–70 و77/79/80 معWebDriver وSMTP sink وخادم دعم وهمية قبل أيsandbox؛ ملف قديم وسياق جديد اختبار أساسي. | 7;8 |
| H6-06 — مصدر الاستحقاق والزمن وسياسة الأوفلاين | خادم DeviceLicense وManagerOnline وissuer/schema/signature/device binding وUID وgrace/revoke/telemetry وسياسة إضافة السنة. P1-032 ليست معالَجة. | إعادة جدولة P1-032 التي كان next_phase لها6 فقط إلى8؛ حسم51–56 و77–79 بساعة وFS وهميتين لا تزوير رخصة أوتغييرOS. | 8 |
| H6-07 — عقود سحابة المرحلة5 التي بقيت محجوبة | AuditorAPI وWs_Auditor وrelay وCLearfiles وDTOs/Equals/setters وaliases والتشفير وper-item ACK وtenant/branch ACL وcache/stock units. H5-01/H5-03 وQ5 باقية. | INT6-14 وFM6-48 وخطط76/78/79 تحفظ المتابعة إلى8؛ لم يعد فحص كل مساراتP5 أوتغيير تصنيفها أوحسم cleanup من اسم الدالة. | 8 |
| H6-08 — القبول الطرفي والتعافي والمطابقة المالية | Windows/.NET/WPF/SQL وقوالب وSDKs موثوقة وبيانات اصطناعية وسياسات يقرها محاسب، مع مرشح معالجة منفصل بإذن؛ لا بناء متاح هنا. | في8 بعد إذن مستقل: remote/local crash وUnknown/restart ومطابقة GL/stock/tax/payment/notification. H4/H5 لا تغلق بأمثلةPython. | 8 |

## 7. أسئلة سياسة وعقود لا أسرار

| المعرف | المجال | السؤال |
|---|---|---|
| Q6-01 | الانطباق الضريبي | ما الدولة والكيان/التسجيل والفرع ونوع التوريد/الفاتورة/الإشعار والعملة وموجةZATCA؟ ما قاعدة standard/simplified/auto/manual وحدودSLA؟ لا يختار نص VAT وحده السياسة. |
| Q6-02 | وحدة الإصدار والتسلسل | كم EGS/POS وdevice/branch/environment؟ هل تشترك الأنواع والعقود/المرتجعات بوحدة؟ ما سياسة الفجوات والتعديل وإعادة المرفوض أوالمجهول وربط ICV/PIH/previousUUID؟ |
| Q6-03 | مصادر المكتبات والعقود | أين المصدر/المواصفات الموثوقة وإصدارات SDK/DTO/serializer وXSD/security/native ABI والمعمارية؟ لا حاجة لرفع binary غير موثوق أوأسرار هنا. |
| Q6-04 | الاعتماد والشهادات | من يفوض CSR/OTP/import/renew/revoke؟ أين تحفظ المفاتيح وكيف يثبت تطابق keypair/issuer/EGS/environment/validity؟ ما خطة آخر اعتماد صالح والحوادث؟ |
| Q6-05 | ETA والمعنى المالي والحالة النهائية | ما document version والعملة/الوحدة/خصم البند والرأس/T4 والمرجع والسياسة الزمنية؟ من يتابع submission/callback/cancel/reject وكيف يرتبط UUID بالأصل؟ |
| Q6-06 | الدفع الطرفي | ما الجهاز/التاجر/العملة ووحدةamount ومعنى كلstatus والمهل وquery/idempotency/refund/reversal/settlement والحدود/الصلاحيات؟ ما البيانات المسموح حفظها من RRN/STAN/PAN/raw؟ |
| Q6-07 | سلة وتثبيت المتجر | هل العينة معتمدة أم خدمة relay هي الميزة؟ ماMode/scopes وregistered redirect/state وmerchant identity ومخزن/تدويرtokens وuninstall والمالك المخول؟ |
| Q6-08 | دورة التجارة ومصدر الحقيقة | ما سياسة paid/pending/partial/cancel/refund وحركة المخزون/GL والفرع/الوحدة/العميل، وmapping version/checkpoint/webhook dedup/stock truth والصفحات/cache/rate؟ |
| Q6-09 | المراسلة والمستلم والاحتفاظ | أي حساب WhatsApp أوSMTP/send-as يجوز لكل ERP principal؟ ما سياسة مشاركة/موافقة/إقامة/retention وحمايةprofile وتطبيع الهواتف وpreview وحالات partial/unknown/bounce؟ |
| Q6-10 | الدعم والمرفقات | ما schema/ownership/auth وbranch/context الصحيح وحدود حجم/عدد/نوع وفحص محتوى المرفق وحذفه/احتفاظه؟ هل الرقم/اسم العميل identifier فقط أم حد تفويض؟ يلزم دليل خادم لا افتراضIDOR. |
| Q6-11 | الاستحقاق والزمن والبيانات | هل تمديد السنة مقصود ومخول؟ ما issuer/signature/device/tenant/grace/revocation/rollback-clock policy وسبب إرسال company/email/mobile/city/device/features وretention؟ |
| Q6-12 | النقل والرصد والتعافي | ما timeouts/cancel/retry budget/401 refresh/429 وHTTP/body contract لكلprovider، وoperation/version والlogs المنقحة والتنبيهات وdead-letter/repair/RPO/RTO ومالك التدخل؟ |

لا تغلق H4/Q4 وH5/Q5 بأسماءmethods أوبنجاح mock مفترض. قد تحسم أسئلة7 نقص الميزة أومدخلها؛ ويتطلب اختبار8 إذناً وبيئة ومرشح معالجة موثوق المصدر. لا أرقام عملاء أومفاتيح أوOTP أوPAN أوقواعد إنتاج مطلوبة في المحادثة.
