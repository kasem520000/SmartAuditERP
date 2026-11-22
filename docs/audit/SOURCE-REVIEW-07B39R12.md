# SOURCE-REVIEW-07B39R12 — قراءة موجهة: مستقبلات السندات والقيود وسلاسل السنوات والفروع

مرجع التقييم: 2026-11-22 UTC (غير مصادق تقويميًا). القاعدة المنشورة: `9a552b7` (تسليم R11). قراءة ساكنة فقط.

## 1. مستقبلات السندات: نمط الإغلاق-ثم-القراءة (P7-173)

قرئت أجسام ReadData/Navigate الخمسة لمستقبلات Receipts:

- **frmSandQ (سند قبض، حالة 5):** ReadData (644–724) يقرأ الأعمدة كلها والقارئ مفتوح، ثم `reader.Close()` في **716**، ثم `LoadEditorName(reader["EmpId"] != DBNull.Value ? ...)` في **719** — وسيطة النداء تُقيَّم بعد الإغلاق. وصول مفهرس لقارئ مغلق يرمي حسب عقد SqlDataReader؛ الالتقاط في Navigate (633–637) يعرض «خطأ في التنقل» وتسقط السطور 722–723 (SetStatus وTabControl1).
- **frmSandQD (حالة 7):** `object empIdObj = reader["EmpId"]...` في 666 قبل الإغلاق في 688 بتعليق «← الآن آمن».
- **frmSandSD (حالة 8):** empId محلي 1073–1077 قبل الإغلاق بتعليق «الآن آمن للإغلاق».
- **frmSandVAT (حالة 9):** يقرأ EmpId في 615 قبل الإغلاق في 616.
- **frmSandD (حالة 6):** Navigate (408–416) يغلق بعد عودة ReadData (421–480) التي تقرأ كل الأعمدة والقارئ مفتوح.

التعليقات الصريحة «الآن آمن» في الشقيقين تثبت أن النمط أصلح عمدًا وفات frmSandQ.

## 2. مستقبلات القيود: رأس عالمي مقابل بنود بفرع الجلسة (P7-174)

- **FrmIntialRestraiction (حالة 0):** الموزّع يرسل `SELECT * FROM Entry WHERE IS_Deleted=0 AND type=0 AND GlobalId=N'{glid}'` (EntryOper:1160) — بلا مرشح فرع. ReadDataFromReader (234–309) يحمل الرأس ثم يستعلم البنود: `SELECT * FROM Entry_sub WHERE branch={MainClass.BranchNo} AND EntryGlobalId=N'{txtEntryGID.Text}'` (278–281) — **فرع الجلسة**. قيد فرع آخر: رأسه يُعرض وبنوده (المخزنة بفرعه) لا تطابق → شبكة فارغة.
- **FrmNewEntry (حالة 10):** ReadData (168–240) يقرأ EmpId والقارئ مفتوح (نمط سليم) ثم البنود `where EntryGlobalId=N'{...}' order by id asc` (221–223) — **بلا فرع**.
- **مستقبلات الفواتير:** BindingInvoice (InvoiceOper:3219+) يحمل Inv_Sub بـ`WHERE Inv.InvGlobalID = N'{Invo.InvGlobalID}'` (3366–3368) — بلا فرع.

الانحراف بين الشقيقين يحصر العيب في المستقبل الافتتاحي وحده.

## 3. سلاسل السنوات (P7-175، P7-176)

- **آلية السنة:** علم `MainClass.ReturnYearPreviews` (MainClass:122)؛ اختيار سنة في CmbYearPreviews يرفعه (frmAccountsStatement:870–873)؛ btnShow يستبدل connstr إلى قاعدة السنة ثم **يعيد فورًا** ويصفّر العلم بعد التحميل (frmAccountBalance:673–687، frmAccountsStatement:844–858)؛ شاشات البحث الأخرى تعيد عند الإغلاق (frmInvoiceSrch:125–129).
- **أثر الاسترجاع الفوري على مصدر القيد:** BtnShowDetail_Click (frmAccountsStatement:874–891، وقرينه في frmAccountBalance) يستدعي `EntryOper.ShowEntrySource(genralNo)` بلا تبديل — ConnObj() على القاعدة الحالية؛ `SELECT doc_no,type,id,branch FROM Entry WHERE GlobalId=N'{glid}'` (EntryOper:1027–1028) لا يجد مفتاح السنة السابقة → `return` صامت (1032–1033).
- **فقد اعتماد SQL:** كل مواقع التبديل الأربعة تبني `trusted_connection=true` حرفيًا: frmAccountBalance:676، frmAccountsStatement:846، frmInvSale:2739–2742 (InsertLinkedReturn)، frmcontract:2079–2081 (btnInsertLinkedInv) — بينما الدخول يدعم مصادقة SQL (frmUserLogin:708–718، 921–931). نشرات SQL-auth تفقد الاعتماد عند المعاينة السابقة.
- **ConnObj:** ثابت ساكن `connstr` (MainClass:36–49) — كل استعلامات ConnObj تتبع آخر تبديل.

## 4. تنقل الفواتير وفرع الجلسة (P7-177)

frmInvPurch.Navigate (481–502) يحمل بلا مرشح فرع خاص به (يتبع استعلام الموزّع)، لكن أزرار btnFirst/btnPrevious/btnNext/btnLast (504–546) تبني `and branch={MainClass.BranchNo}` — بعد فتح فاتورة بفرع آخر عبر الموزّع، أي تنقل لاحق يقفز لفواتير فرع الجلسة بصمت.

## 5. مبدّل قواعد الدخول (ملاحظة محمولة)

`cmbDatabases_SelectionChangeCommitted` (frmUserLogin:911–955): يبني اتصالًا جديدًا لقاعدة mbDatabases ويضبط `MainClass.Database` لكنه لا يلمس `MainClass.connstr` — استعلامات ConnObj اللاحقة تبقى على قاعدة الدخول. لم يُرقَّم: تعبئة الصندوق ومسارات ما بعد التبديل تحتاج تتبعًا إضافيًا قبل حسم الأثر.

## 6. نطاق القراءة

قُرئت الأجسام الموثقة أعلاه بأسطرها وتجزئاتها في ملف العقد. لم تُقرأ مستقبلات الإيجار (frminvoice) وCreditNote/DebtNote وfrmRptEntries في هذه الشريحة (محفولة ضمن بقية الفتّاحات). لا تساوي هذه القراءة شهادة خروج؛ الأحكام ساكنة.
