#!/usr/bin/env python3
"""R9 post-capture publication/preservation checks, not the 519-case run inputs.

Exclusively publish new documents; prepend to three historical indexes without
rewriting their suffix. Preserve capture and initial fixture versions. Adding
this post-capture Python tool naturally changes B38's recursive tool census;
its unchanged142 expectation is exercised again and its failure is retained.
No application/SQL/WPF/provider/SDK execution, remediation or exit certificate.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import time

import verify_save_edit as v

E, D = 'docs/audit/evidence/', 'docs/audit/tools/disposition07b/'
LEDGER = 'capability-reconciliation-' + v.TAG + '.json'
STATUS = 'validation-status-supplement-' + v.TAG + '.json'
PREFIX = 'index-prefix-supplement-' + v.TAG + '.json'
CHECK = 'publication-check-receipt-' + v.TAG + '.json'
FINAL = 'finalization-before-commit-' + v.TAG + '.json'
POST = 'postcapture-B38-check-' + v.TAG + '.json'
RECEIPT = 'validation-current-run01-receipt-' + v.TAG + '.json'
JOURNAL = 'validation-current-run01-journal-' + v.TAG + '.jsonl'
POSTOUT, POSTERR = ('B38-postcapture-publication-' + v.TAG + ext for ext in ('.stdout.txt', '.stderr.txt'))
INDEXES = ('docs/audit/README.md', 'docs/audit/PLAN.md', 'docs/audit/IMPROVEMENTS.md')
PHASE, VALIDATION = 'docs/audit/PHASE-' + v.TAG + '.md', 'docs/audit/VALIDATION-' + v.TAG + '.md'
SELF = D + 'publish_save_edit.py'


def sha(raw): return hashlib.sha256(raw).hexdigest()
def canonical(obj): return sha(json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf8'))
def file_id(raw): return dict(bytes=len(raw), sha256=sha(raw))
def pin(name): return v.identity(name if '/' in name else E + name)
def clock(): return datetime.now(timezone.utc).isoformat()


def envelope(kind):
    return dict(schema_version=1, kind=kind, assessment_reference_date_utc=v.DATE,
        session_reference_date_utc=v.SESSION_DATE, raw_clocks_are_calendar_authority=False,
        application_execution_count=0, whole_7B_static_assessment_complete=False,
        capability_exit_certificates_issued=0, four_family_exit_certificates_issued=0,
        new_accepted_external_handoffs=0, phase7C_started=False, phase8_authorized=False,
        R2_R3_files_recovered=False, prior196_tests_recertified=False,
        this_postcapture_publication_was_run01_input=False)


def exclusive_json(name, obj):
    with (v.EV / name).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2); stream.write('\n')


def exclusive_md(rel, text):
    with (v.ROOT / rel).open('x', encoding='utf8', newline='\n') as stream: stream.write(text)


def post_B38_check():
    paths = [v.EV / n for n in (POSTOUT, POSTERR, POST)]
    if any(p.exists() for p in paths): raise FileExistsError('Preserve post-capture check; no overwrite')
    command = [sys.executable, '-B', '-W', 'error::ResourceWarning', '-m', 'unittest', 'discover',
        '-s', 'docs/audit/tools/census07b', '-p', 'test_7b_completion.py', '-v']
    started, tick = clock(), time.monotonic()
    with paths[0].open('xb') as out, paths[1].open('xb') as err:
        process = subprocess.run(command, cwd=v.ROOT, stdout=out, stderr=err, check=False)
    text = paths[1].read_text(encoding='utf8')
    match = re.search(r'^Ran (\d+) tests in ([\d.]+)s$', text, re.M)
    cases = re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. (ok|FAIL|ERROR)$', text, re.M)
    result = envelope('R9-postcapture-B38-only-run-after-adding-versioned-publication-tool-not-part-of519')
    result.update(command=command, exit_code=process.returncode,
        raw_started_clock_verbatim=started, raw_finished_clock_verbatim=clock(),
        wall_seconds=round(time.monotonic() - tick, 6),
        reported_tests=int(match[1]) if match else None,
        reported_unittest_seconds=float(match[2]) if match else None,
        actual_verbose_case_lines=len(cases), actual_case_status_counts=dict(Counter(c[2] for c in cases)),
        assertion_lines_verbatim=re.findall(r'^AssertionError:.*$', text, re.M),
        stdout=pin(POSTOUT), stderr=pin(POSTERR),
        unchanged_legacy_expected142_not_rewritten=True,
        new_publication_tool=pin(SELF), all_suites_green=process.returncode == 0)
    exclusive_json(POST, result)
    return result


def summary():
    receipt = v.load(RECEIPT); tests = next(r for r in receipt['records'] if r['id'].endswith('combined-tests'))
    b38 = next(r for r in receipt['records'] if r['id'] == 'B38-preserved-tests')
    return receipt, tests, b38


def validation_text(post):
    r, t, b = summary(); archive = r['exact_authored_consumed_versions_archive']
    return f'''# 07B39R9 — تحقق فعلي محفوظ، لا تشغيل ERP أو شهادة اكتمال

**7B مفتوحة؛ لا خروج قدرة/أسرة أو إحالة إكمال جديدة مقبولة؛7C لم تبدأ و8 غير مأذونة.** مرجع R9 الجديد2026-11-16UTC استشرافي حسب الجلسة، لا حسب ساعة العملية. لا تصديق21Nov/نسبة مرجع R8 للمستخدم أو22Nov من تلخيص/ساعات خام.

## run01 المستهلك فعليًا

| النطاق | النتيجة الفعلية |
| --- | --- |
| R1+R4+R5+R6+R7+R8+R9 | **{t['actual_case_status_counts']['ok']}/{t['reported_tests']} نجاحًا في{t['reported_unittest_seconds']} ثانية**، exit{t['exit_code']}. |
| تفصيل الحالات |42+50+57+62+86+93+129؛ الجديدة129 ضمن519 وليست فوقها. |
| B38 المحفوظة أثناء run01 | **{b['actual_case_status_counts']['ok']} نجاحًا/فشل{b['actual_case_status_counts']['FAIL']} من{b['reported_tests']} في{b['reported_unittest_seconds']} ثانية**، `{b['assertion_lines_verbatim'][0]}`، exit{b['exit_code']}. |
| فحوص السلامة |8 أوامر exit0 وerrors[]، بما فيها R9 وإعادة اشتقاق R8/R7/R6/R5/R4/R1/B38؛ ليست شهادة دلالية للقدرات. |
| بوابات الإكمال |7 أوامر exit2/open، لا نجاح إكمال. |
| الالتقاط |17 أمرًا/34 تيارًا،{len(r['inputs_before'])} مدخلًا ثابتًا، تغيّر أثناء الالتقاط: `{r['inputs_changed_during_capture']}`؛ **الغلاف exit{r['wrapper_exit_code']} وليست كل المجموعات خضراء**. |

[إيصال run01](evidence/{RECEIPT}) · [journal الفعلي](evidence/{JOURNAL}) · [stdout المجموعة](evidence/{Path(t['stdout']['path']).name}) · [stderr و519 حالة](evidence/{Path(t['stderr']['path']).name}) · [فشل B38 الأصلي](evidence/{Path(b['stderr']['path']).name})

أرشيف النسخ المؤلفة المستهلكة [validation-consumed-inputs-run01](evidence/{Path(archive['path']).name}): **{archive['members']} عضوًا/{archive['bytes']} بايت**، SHA-256 `{archive['sha256']}`. تقارن مراجعة النشر كل عضو بهوية المدخل قبل التشغيل وبايتاته الحالية؛ لا إعادة بناء من ملخص اختبارات.

إحداثيات/بصمات142 جسمًا و158 نطاق عرض ليست حالات اختبار ولا شهادة قراءة بشرية أو تقويم. أدوات Python تقرأ/تحور الصياغة المقدمة والـJSON في الذاكرة/مجلدات مؤقتة فقط؛ لا C# أو SQL أو WPF أو provider أو حسابات أعمال أو SDK أو REPX منفذ.

## فحص نشر لاحق منفصل، لا يضاف إلى519

أضيفت أداة النشر المصدّرة **publish_save_edit.py بعد الالتقاط**، لذلك أعيدت B38 وحدها بمخرجات مستقلة: **{post['actual_case_status_counts'].get('ok', 0)} نجاحًا/فشل{post['actual_case_status_counts'].get('FAIL', 0)} من{post['reported_tests']} في{post['reported_unittest_seconds']} ثانية**، `{'; '.join(post['assertion_lines_verbatim'])}`، exit{post['exit_code']}. [الإيصال](evidence/{POST}) · [stderr](evidence/{POSTERR}).

162 في run01 ثم163 بعد إضافة ناشر Python هي أعداد أدوات Python التكرارية، **لا أعداد حالات519 أو الأجسام142**. توقع الاختبار التاريخي142 لم يُغيّر، ولم تُنقل/تُخف/تُستبعد الأدوات لصنع نجاح. النتيجتان محفوظتان؛ ليست هذه معالجة ERP أو suite كلها خضراء.

## التأليف والحفظ والحدود

فحص تأليف أولي لعدد التطابقات النصية وجد5 توقعات fixture غير مطابقة قبل أول unittest؛ صُححت إلى التكرار الفعلي. [الملاحظة](evidence/fixture-authorship-check-07B39R9.json) وأرشيف نسخة الاختبار الأولية محفوظان. **ليس فشل خمس حالات unittest ولا تحويل فشل فعلي إلى نجاح.** R5run01 وفشل preflight R8 وناشره وإيصالاتهما لم تُعدّل أو تُمح.

هذه الوثيقة وPHASE وتسوية26 والملحقات وبوادئ README/PLAN/IMPROVEMENTS وأداة النشر والفحص اللاحق **ليست مدخلات519 أو أعضاء الأرشيف18**؛ فحوص نشرها اللاحقة مسماة مستقلة وليست اختبارات ERP إضافية. إيصال run01/journal/الأرشيف ومخرجاته ليست مدخلات لنفسها.

827 مصدر تطبيق/29,128,444 بايت و1604 مدخل تدقيق منشور عند الدخول محفوظة؛ الفهارس الثلاثة بإضافة بادئة وحفظ اللاحقة الأصلية حرفيًا فقط. سجل335/raw336CRLF وملحقR1 محفوظان؛339 قاموسًا متاحًا لا تصديق345 التاريخية أو196 اختبارًا أو49 حدًا مفقودة. لا استرداد R2/R3 أو توثيق chronology R6. **لا إصلاح/بناء/تشغيل/قبول مالي أو تشغيلي، ولا بدء7C/تفويض8.**
'''


def phase_text(post):
    r, t, b = summary()
    return f'''# 07B39R9 — الحفظ والتعديل ومآل الأوامر: تقدم مسند لا خروج من العدّ

**7B مفتوحة؛ صفر شهادة قدرة/أسرة وصفر إحالة إكمال جديدة مقبولة.7C لم تبدأ و8 غير مأذونة.** تقييم ساكن على `arena/94ae8414-smartauditerp` من R8 المنشور `{v.BASE_HEAD}`.

[مراجعة المصدر](SOURCE-REVIEW-07B39R9.md) · [الأوامر/المحررات/الفتّاحات](evidence/{v.MATRIX}) · [الأحكام15](evidence/{v.REVIEW}) · [مقارنة الجذور](evidence/{v.ROOTS}) · [التحقق](VALIDATION-07B39R9.md) · [تسوية26](evidence/{LEDGER}) · [المتبقي المحلي](evidence/{v.WORK})

## ما أُنجز فعليًا

قُرئت142 أجسام method/constructor مختارة في25 هوية مصدر، تشمل كاتبي SaveInvoice كاملين، الستة SaveAndPrint ومداخل Save/Print/Pay/Hold/quotation/repayment والمفاتيح، الصلاحيات والمحولين والقيد والذاكرة والمزامنة والمرفقات المحددة. لكل23 مالك أمر حكم مستقل وللمحررات الستة trace من المدخل إلى النشر. ثم قُرئ21فتّاح Home وGenerateInvoice ومساعداه وثلاثة فتّاحات مخزون وتفاصيل العقد وأجسام ImportInventoryItems الأربعة؛ **26 مالك فتّاح/31 إنشاء ليست26 مراجعة قدرة أو كل مداخل المستند**.

المصدر لا يساوي إكمالًا آليًا: manifest158 نطاقًا متداخلًا من عروض المساعد، ليس raw telemetry أو158 مراجعة مستقلة/طوابع فردية. لا compiler binding أو WPF lifecycle أو SQL/provider أو تشغيل أعمال.

## أهم الأحكام والشواهد المضادة

- **الفترة والصلاحية:** CheckProiedAcc ينتهي بـ`|| true` وAllowEdit يسمح عند غياب الصف/الخطأ؛ دعم P3-001/P1-012. تعطيل UI ووجود موظف/مخزن أو Branch في payload ليس allowed-set للمستند/الفرع/السنة. العقد يهيئ allowEdit=true بلا كتابة محلية لاحقة، **لكن الحارس الإلكتروني المستقل قد يمنع التعديل**.
- **الحفظ ليس مسارًا موحدًا:** شراء Save وSavePrint يختلفان فعليًا (P4-031)، وF6 البيع يصل ValidateInvoice متجاوزًا wrapper الفترة؛ اشتراكه في XAML والمنشئ يدعم P7-162 دون حفظ مزدوج مرصود. POS F6/Pay وF7/Hold مساران مختلفان، وتغيير التاريخ يدعم P7-135.
- **النتيجة والنشر:** نقل المخزون ينادي async-void مرتين ثم يواصل الكلفة/رسالة النجاح دون bool مجمع (P4-019). quotation يعيد النوع وCLR بعد void validator؛ Hold ينشر HoldList بعد void save. Contract saved-print branch **لا ينادي RptPrint**. لا تعميم زمني: آثار ما قبل await قد تنفذ تزامنيًا.
- **المعاملة والذاكرة:** EntryOper يلتزم بمعاملته قبل التزام الفاتورة (P3-003)؛ لا empty/balance/period guard محلي في SaveEnty (مقارنة P3-002 مؤهلة). cache قبل Save في IO/شراء/مناقلة وخارج saved في بيع/عقد؛ **POS يغيره بعد النجاح فقط، والشراء يرفض null entry للأنواع المالية المحددة**. cache DataTable، لا فقد SQL stock مستديم مُشاهد.
- **شاهد نفي مهم:** معاملات رأس العقد الأربعة **QRCode/InvoiceHash/UUID/ZatcaSent موجودة عند1121–1124 قبل Execute عند1138**. مقارنة placeholders لا تفقد اسمًا بعد trim، مع حفظ62 اسمًا خامًا ومسافاتها. رُفض ادعاء الغياب؛ لا رقم نتيجة ولا إلصاق بـP4-020 الإنتاجية ولا تصديق SqlClient/deployed schema.
- **المداخل والاستيراد:** بعض فتّاحات Home تفحص IsEnabled وأخرى تختلف Name/Tag/موعد lookup؛ GenerateInvoice قد يستورد في أول POS مفتوح. فتّاحات RptInventory تحتفظ global key، خلاف التعميم. تفصيل العقد يطلب type23 لكنه يضبط editor.InvType2. أربعة imports تكتب FirstOrDefault ItemId بعد void SearchByID؛ لا دمج تلقائي مع P7-144 ذات آخر مطابق، وبقية SearchByID/ItemOper باقية محليًا.
- **الإرسال والملفات:** print/sync/broker/table/cache لها حراس saved مختلفة؛ broker المناقلة غير محروس بنتيجة save. فروع SyncInvoice لا تعيد النتيجة نفسها، وnoncloud العقد يعلّم Inv. لا cloud/SDK/طابعة/ملفات أو SQL منفذة؛ الأدلة المحلية الإضافية لا تساوي نجاحًا طرفيًا أو معالجة P6-007.

الحزمة تحفظ339 قاموس نتيجة وتقارن23 منها دلاليًا بصورة محددة، وتعزل22 سؤال مصدر بينها نفي المعاملات ودعم جذور وأسئلة غير مرقمة. لا339 مراجعة جديدة أو345 recertification؛ P4-014/P7-132 تبقيان potential؛ صفر نتائج مرقمة جديدة وصفر إغلاق معالجة.

## التحقق الفعلي لا يساوي الخروج

**run01:519/519 نجاحًا في{t['reported_unittest_seconds']} ثانية** =42+50+57+62+86+93+129، والجديدة129 ضمن519. **B38:42 نجاحًا/فشل1 من43 في{b['reported_unittest_seconds']} ثانية، `162 != 142`**. ثمانية فحوص سلامة exit0 وسبع بوابات إكمال exit2/open؛ **الغلاف1، ليست كل المجموعات خضراء**.

17أمرًا/34تيارًا،2449مدخلًا ثابتًا/18نسخة مؤلفة مستهلكة مؤرشفة. بعد إضافة أداة النشر المصدّرة أُعيدت B38 وحدها: **42 نجاحًا/فشل1 من43، `163 != 142`**؛ فحص نشر لاحق منفصل لا يضاف إلى519 أو الأرشيف. لم يُغيّر توقع142 أو يُخفَ فشل قديم. ملاحظة تصحيح توقعات5fixtures قبل أول unittest محفوظة وليست خمس حالات اختبار فاشلة/ناجحة.

هذه الوثيقة وVALIDATION وتسوية26/الملحقات/الفهارس/الناشر بعد الالتقاط، فلا تُنسب رجعيًا لمدخلات519. [إيصال التحقق](evidence/{RECEIPT}) و[فحص النشر اللاحق](evidence/{POST}) يفصلان النطاقين.

## الباقي محليًا والخروج المستقل

تقدم محدود في **D08/D17/D19/D22/D25**؛ القدرات21 الأخرى محمولة بقواميسها الأصلية/سجلR8، لا مراجعة جديدة لها. كل26 قدرة والأسر الأربع بلا شهادة خروج، وتسوية37 سجل نسب محفوظة حرفيًا. لا إكمال `R8LOCAL-SAVE-EDIT` من الشريحة المحددة.

**التالي:** بقية الفتّاحات ومنتجي مفاتيحها والنطاق المسموح لكل مستند/فرع/سنة؛ ثم SearchByID/ItemOper ودمج/استبدال/وحدة/كمية/سعر/خصم/VAT؛ transfer/offline/broker/POS table dependencies؛ type/fallback العقد؛ السنة والإغلاق؛ وبقية القدرات وأسئلة R7 D05/D06 و@Recipient. القائمة تميز الأجسام المنجزة فلا تُطلب مجددًا لمجرد زيادة العدّ. عقود model/policy/remote تبقى بمالك ومدخل منقح وأثر وخطوة وتصرف ساكن **غير مقبول كإحالة إكمال** قبل استيفاء المحلي.

## الحفظ والمرجع

الاستعادة الموثقة ff-only أعادت R8 المنشور بعد التحقق من أرشيف R4 الأصلي؛ ليست استرداد R2/R3. 827مصدر تطبيق/29,128,444بايت وسجل335/raw336CRLF وملحقR1 وكل الالتقاطات/الإخفاقات محفوظة. 196/345/49 المفقودة لا تعاد من السرد.

مرجع R9 الحالي **2026-11-16UTC استشرافيًا**؛21Nov R8 ونسبة التاريخ للمستخدم غير مصدقتين؛22Nov في تلخيص أو raw clocks ليست سلطة تقويمية. لا تعديل تاريخ قديم أو تصديق chronology R6. لا إصلاح/بناء/تشغيل ERP/SQL/WPF/provider/device/SDK/REPX أو قبول مالي/تشغيلي. **7B مفتوحة؛7C لم تبدأ؛8 غير مأذونة.**
'''


def reconciliation(post):
    old = v.load('capability-reconciliation-07B39R8.json'); review = v.load(v.REVIEW); roots = v.load(v.ROOTS)
    r, tests, b38 = summary(); result = envelope('R9-canonical26-and-original37-ancestry-reconciliation-with-independent-open-decisions')
    prior_pin = pin('capability-reconciliation-07B39R8.json')
    result.update(base_HEAD=v.BASE_HEAD, canonical_capability_input=pin('capability-register-07B38.csv'),
        prior_R8_ledger_input=prior_pin, canonical_capabilities_count=26, capabilities=[])
    for previous in old['capabilities']:
        cid = previous['capability_id']; row = previous['canonical_upstream_row']; fresh = review['capabilities'].get(cid)
        result['capabilities'].append(dict(capability_id=cid, canonical_upstream_row=row,
            canonical_upstream_row_canonical_json_sha256=canonical(row),
            preserved_R8_record_reference=dict(ledger=prior_pin, capability_id=cid, canonical_json_sha256=canonical(previous),
                record_not_relabelled_as_fresh_R9_review=True),
            new_R9_bounded_review=dict(review=pin(v.REVIEW), capability_id=cid, canonical_json_sha256=canonical(fresh)) if fresh else None,
            fresh_R9_whole_capability_assessment=False, independent_whole_capability_exit=False,
            whole_capability_certified=False, local_semantic_obligations_complete=False, readable_local_externalized=False,
            next_action_source=dict(current_R9_local_remainder=fresh['remaining_readable_local'], local_worklist=pin(v.WORK)) if fresh else previous['next_action_source'],
            next_action_precedence='Use current R9 source decisions and successor worklist for the five touched capabilities; prior original rows/other21 obligations remain carried, not newly reviewed or completed.'))
    ancestry = old['preserved_R7_ancestry_object']
    family_blockers = {
        'R1': ('Parent/child result and publication remains unclosed across original B14 obligations; quotation/Hold/transfer show void-result limits, while unrelated parents/output channels are still original local work.', ['CAP7B38-D17', 'CAP7B38-D19', 'CAP7B38-D22'], [v.MATRIX, v.WORK]),
        'R2': ('B15 accrual/tax local contracts are not independently exhausted. New independent-entry/tax-send evidence does not close accrual/receipt/notice/tax-report and original account/period consumers, including R7 @Recipient.', ['CAP7B38-D05', 'CAP7B38-D06', 'CAP7B38-D15', 'CAP7B38-D16'], [v.REVIEW, 'entry-source-local-followthrough-decisions-07B39R7.json']),
        'R3': ('B16 shared DTO/policy/provider/output contracts lack individual exit after completing all readable consumers. Current model/policy/remote boundaries explicitly unaccepted; local SearchByID, grants/lookup and service/helper work remains.', ['CAP7B38-D24', 'CAP7B38-D25'], [v.REVIEW, v.WORK]),
        'R4': ('B17-B37 continuation ancestry37 is preserved, but selected Save/commands/openers do not assess all26 capabilities or all alias/reflection/document ingress; inventory/printing/year/merge and other canonical local obligations remain.', ['CAP7B38-D08', 'CAP7B38-D17', 'CAP7B38-D19', 'CAP7B38-D22', 'CAP7B38-D26'], [v.MATRIX, v.WORK]),
    }
    result.update(preserved_R8_ancestry_object_verbatim=ancestry, B37_canonical_ancestry_rows=sum(len(b['records']) for b in ancestry['bundles']),
        independently_authored_R9_family_nonexit_decisions=[])
    for original in ancestry['family_exits']:
        reason, caps, evidence = family_blockers[original['family']]
        result['independently_authored_R9_family_nonexit_decisions'].append(dict(family=original['family'], original_family_record_verbatim=original,
            current_static_disposition='No independent exit certificate: readable-local obligations remain', source_backed_blocker=reason,
            named_capability_obligations=caps, evidence=[pin(n) for n in evidence], owner_role='Static audit agent and separately named contract owners',
            whole_family_sources_freshly_reread=False, local_semantic_obligations_complete=False, static_assessment_complete=False,
            accepted_completion_handoff=False, certificate_issued=False))
    result.update(findings=old['findings'], external_boundaries=old['external_boundaries'],
        preserved_prior_R8_findings_delta=old['R8_findings_delta'], preserved_prior_R8_external_delta=old['R8_external_delta'],
        R9_findings_delta=dict(new_numbered_ids=[], prior339_available_dictionaries_preserved=True, all339_semantically_reread=False,
            historical345_recertified=False, focused_root_reviews=roots['focused_root_reviews'], source_question_dispositions=roots['candidate_dispositions'],
            rejected_missing_four_header_parameters='Counterevidence at contract1121-1124/1138; no missing names after trim, raw whitespace retained, not provider certification.', root_remediated=False),
        R9_external_delta=dict(new_accepted_external_handoffs=0, boundaries_with_owner_redacted_input_impact_action_and_static_disposition=review['unavailable_contracts_not_accepted_as_handoffs'],
            local_work_externalized=False, lost49_reconstructed=False),
        actual_validation=dict(receipt=pin(RECEIPT), journal=pin(JOURNAL), archive=r['exact_authored_consumed_versions_archive'],
            combined_case_count=tests['reported_tests'], combined_seconds=tests['reported_unittest_seconds'], combined_status_counts=tests['actual_case_status_counts'],
            combined_partition=r['combined_actual_partition'], input_count=len(r['inputs_before']), command_count=len(r['records']),
            capture_B38_assertions=b38['assertion_lines_verbatim'], capture_B38_status_counts=b38['actual_case_status_counts'],
            capture_wrapper_exit_code=r['wrapper_exit_code'], all_suites_green=False, postcapture_B38_only_check=pin(POST),
            postcapture_B38_assertions=post['assertion_lines_verbatim'], ledger_phase_validation_and_prefixes_were_run01_inputs=False),
        new_source_work=dict(review_input=pin(v.REVIEW), matrix_input=pin(v.MATRIX), source_facts_input=pin(v.FACTS), reads_input=pin(v.READS),
            whole_selected_method_contexts=142, source_identities=25, command_owner_reviews=23, editor_pipelines=6, selected_opener_owners=26,
            selected_editor_creations=31, literal_command_calls=35, source_decisions=15, all_routes_or_whole_six_editors_complete=False),
        reference_date_note=pin(v.DATE_NOTE), ledger_validation_phase_and_index_prefixes_were_run01_inputs=False)
    return result


def prefixes():
    common = '''**7B مفتوحة؛ صفر شهادة قدرة/أسرة وصفر إحالة إكمال جديدة مقبولة؛7C لم تبدأ و8 غير مأذونة.**

'''
    links = f'''[التسليم الحالي](PHASE-07B39R9.md) · [المصدر المستهلك](SOURCE-REVIEW-07B39R9.md) · [الأوامر والمداخل](evidence/{v.MATRIX}) · [التحقق الفعلي](VALIDATION-07B39R9.md) · [القدرات26/النسب37/الأسر الأربع](evidence/{LEDGER}) · [المتبقي المحلي](evidence/{v.WORK}) · [مرجع R9](evidence/{v.DATE_NOTE})

'''
    validation = '''**run01:519/519 في135.081ثانية** =42+50+57+62+86+93+129؛ الجديدة129 ضمن519. **B38:42نجاحًا/فشل1من43، `162 != 142`**؛8فحوص سلامة0 و7بوابات2/open والغلاف1. بعد إضافة أداة النشر المصدّرة فحصB38 منفصل43حالة/فشل1 `163 != 142` لا يضاف إلى519؛ توقع142 والأصول والإخفاقات لم تعدّل. ليست كل المجموعات خضراء.

'''
    preserved = '''827مصدر تطبيق دون تغيير أو تشغيل؛339قاموسًا محفوظًا لا339مراجعة جديدة أو تصديق345/196/49المفقودة. مرجعR9 الجديد16نوفمبر2026UTC استشرافي حسب الجلسة؛21NovR8 ونسبة التاريخ للمستخدم و22Nov من تلخيص/ساعات لا تصدق، والأصول مجمدة. النص التالي محفوظ كاملًا ببايتاته كتسليمR8 وما قبله، لا الحالة الحالية.

## أرشيف R8 وما قبله — النص التالي محفوظ كاملًا

'''
    return {
        INDEXES[0]: '# الحالة الحالية — 07B39R9: الحفظ والتعديل والنشر بأحكام مصدرية\n\n' + common +
            'أُنجزت أجسام الحفظ/التحقق/الصلاحية والكاتبين المركزيين و23مالك أمر وست سلاسل مستقلة؛26مالك فتّاح مختار لا26قدرة مكتملة. فروق Save/Print/keyboard/Pay/Hold/quotation والـcache/القيد والمعاملة موثقة بشواهد مضادة: POS cache بعد النجاح والشراء يرفض null entry ماليًا. **رُفض ادعاء نقص معاملات العقد الأربعة لأنها موجودة قبل Execute**؛ لا نتيجة جديدة أو إصلاح.\n\n' + validation + links + preserved,
        INDEXES[1]: '# خطة المتابعة — 07B39R9 ضمن القدرات26 المعتمدة\n\n' + common +
            'قُرئت/قُيّمت142أجسام مختارة، لا اكتمال كل Save/المحررات/ingress. لا تُطلب الأجسام المنجزة ثانية لزيادة العدّ؛ تبقى37هويةR6 وراياتها ومهامR8 محفوظة مع فصل المنجز والموروث.\n\n**التالي محليًا:** بقية فتّاحات المستند ومصادر الصفوف وallowed-document/branch/year؛ SearchByID/ItemOper وmerge/copy/unit/serial/VAT؛ transfer/offline/broker/POS tables؛ type/fallback العقد؛ السنة والإغلاق؛ وبقية26قدرة وأسئلةR7D05/D06 و@Recipient. عقود model/policy/remote ليست إحالات إكمال مقبولة قبل استيفاء المحلي.\n\n' + links + validation + preserved,
        INDEXES[2]: '# متابعة 07B39R9 — أحكام الحفظ والشواهد المضادة، لا معالجة\n\n' + common +
            'دعم إضافي للجذور P3-001/P1-012/P4-031/P7-135/P7-162/P4-019/P3-003 وP3-002/P6-007 بحدودها. cache ذاكرة لا فقد SQL stock، وnull entry ليس حكمًا واحدًا لكل محرر. **معاملات QRCode/InvoiceHash/UUID/ZatcaSent موجودة في العقد1121–1124 قبل1138**؛ لا إلصاق بـP4-020 الإنتاجية. type2/UI مقابل صف23، وFirstOrDefault import بعدvoid، وquotation/Hold/print/sync أسئلة منفصلة غير مرقمة؛P4-014/P7-132 تبقيانpotential.\n\n' + links + validation + preserved,
    }


def capture_errors():
    r, tests, b38 = summary(); errors = []
    def need(ok, label):
        if not ok: errors.append(label)
    need(not r['inputs_changed_during_capture'] and len(r['inputs_before']) == 2449, 'run01-stable-inputs')
    need(tests['reported_tests'] == tests['actual_verbose_case_lines'] == 519 and tests['actual_case_status_counts'] == {'ok': 519, 'FAIL': 0, 'ERROR': 0}, 'actual519-case-lines')
    need(r['combined_actual_partition'] == dict(test_recovery_exit=42, test_document_receiver=50, test_production_adjustment=57, test_session_year=62, test_entry_source=86, test_linked_activity=93, test_save_edit=129), 'actual-seven-module-partition')
    need(b38['reported_tests'] == 43 and b38['actual_case_status_counts'] == {'ok': 42, 'FAIL': 1, 'ERROR': 0}
        and b38['assertion_lines_verbatim'] == ['AssertionError: 162 != 142'] and b38['exit_code'] == r['wrapper_exit_code'] == 1, 'preserved-real-B38-failure')
    for rel, expected in r['inputs_before'].items():
        raw = (v.ROOT / rel).read_bytes(); same = file_id(raw) == expected
        if not same and rel in INDEXES: same = len(raw) > expected['bytes'] and sha(raw[-expected['bytes']:]) == expected['sha256']
        need(same, 'consumed-input-not-preserved:' + rel)
    for row in r['records']:
        for stream in ('stdout', 'stderr'): need(pin(row[stream]['path']) == row[stream], 'stream:' + row['id'] + ':' + stream)
    journal = [json.loads(line) for line in (v.EV / JOURNAL).read_text().splitlines()]
    need(journal == r['records'], 'actual-journal-records')
    archive = r['exact_authored_consumed_versions_archive']; need(pin(archive['path']) == {k: archive[k] for k in ('path', 'bytes', 'sha256')}, 'consumed-archive-identity')
    with tarfile.open(v.ROOT / archive['path'], 'r:gz') as tar:
        members = tar.getmembers(); need(sorted(m.name for m in members) == archive['member_paths'] and len(members) == 18, 'exact18-consumed-versions')
        for m in members:
            stream = tar.extractfile(m)
            if stream is None: errors.append('nonfile-archive-member:' + m.name); continue
            with stream: raw = stream.read()
            need(file_id(raw) == r['inputs_before'][m.name], 'archive-version-not-before:' + m.name)
            need(raw == (v.ROOT / m.name).read_bytes(), 'archive-version-changed:' + m.name)
    return errors


def verify(require_final=True):
    errors = capture_errors() + v.verify(True)['errors']
    ledger, post = v.load(LEDGER), v.load(POST)
    def need(ok, label):
        if not ok: errors.append(label)
    old = v.load('capability-reconciliation-07B39R8.json')
    canonical_rows = v.base.rows('capability-register-07B38.csv')
    need([r['canonical_upstream_row'] for r in ledger['capabilities']] == canonical_rows and len(canonical_rows) == 26, 'exact-original26-canonical-rows')
    for i, row in enumerate(ledger['capabilities']):
        need(row['canonical_upstream_row_canonical_json_sha256'] == canonical(row['canonical_upstream_row'])
            and row['preserved_R8_record_reference']['canonical_json_sha256'] == canonical(old['capabilities'][i]), 'prior-capability-pin:' + row['capability_id'])
        need(all(row[k] is False for k in ('fresh_R9_whole_capability_assessment', 'independent_whole_capability_exit', 'whole_capability_certified', 'local_semantic_obligations_complete', 'readable_local_externalized')), 'no-capability-exit:' + row['capability_id'])
    ancestry = ledger['preserved_R8_ancestry_object_verbatim']
    need(ancestry == old['preserved_R7_ancestry_object'] and sum(len(b['records']) for b in ancestry['bundles']) == 37, 'exact37-ancestry-and-original-four-families')
    families = ledger['independently_authored_R9_family_nonexit_decisions']
    need([r['family'] for r in families] == ['R1', 'R2', 'R3', 'R4'] and len({r['source_backed_blocker'] for r in families}) == 4, 'four-individual-source-backed-family-nonexits')
    for row, original in zip(families, ancestry['family_exits']):
        need(row['original_family_record_verbatim'] == original and all(row[k] is False for k in ('whole_family_sources_freshly_reread', 'local_semantic_obligations_complete', 'static_assessment_complete', 'accepted_completion_handoff', 'certificate_issued'))
             and bool(row['evidence']) and bool(row['named_capability_obligations']), 'qualified-family-nonexit:' + row['family'])
        for p in row['evidence']: need(pin(p['path']) == p, 'family-input-pin:' + p['path'])
    need(ledger['findings'] == old['findings'] and ledger['external_boundaries'] == old['external_boundaries'], 'original-findings-and-boundary-limits')
    need(post['reported_tests'] == post['actual_verbose_case_lines'] == 43 and post['actual_case_status_counts'] == {'ok': 42, 'FAIL': 1}
         and post['assertion_lines_verbatim'] == ['AssertionError: 163 != 142'] and post['exit_code'] == 1, 'postcapture-B38-failure-still-retained')
    for name in ('stdout', 'stderr'): need(pin(post[name]['path']) == post[name], 'postcapture-stream-pin:' + name)
    need(pin(SELF) == post['new_publication_tool'], 'postcapture-publisher-version')
    prefix = v.load(PREFIX)
    link_count = 0
    for row in prefix['indexes']:
        raw = (v.ROOT / row['path']).read_bytes(); before = row['preserved_suffix']; n = row['prefix']['bytes']
        need(file_id(raw[:n]) == row['prefix'] and file_id(raw[n:]) == before and file_id(raw) == row['after'], 'prefix-only:' + row['path'])
    new_text = [(p, (v.ROOT / p).read_text()) for p in (PHASE, VALIDATION, 'docs/audit/SOURCE-REVIEW-07B39R9.md')]
    new_text += [(r['path'], (v.ROOT / r['path']).read_bytes()[:r['prefix']['bytes']].decode('utf8')) for r in prefix['indexes']]
    for rel, text in new_text:
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in target or target.startswith('#'): continue
            path = (v.ROOT / rel).parent / target.split('#', 1)[0]
            need(path.is_file(), 'new-doc-link:' + rel + ':' + target); link_count += 1
    for name in (LEDGER, STATUS, PREFIX, POST):
        obj = v.load(name)
        need(obj['assessment_reference_date_utc'] == v.DATE and obj['application_execution_count'] == 0
            and obj['whole_7B_static_assessment_complete'] is False and obj['capability_exit_certificates_issued'] == obj['four_family_exit_certificates_issued'] == obj['new_accepted_external_handoffs'] == 0
            and obj['phase7C_started'] is False and obj['phase8_authorized'] is False, 'static-open-publication:' + name)
    if require_final:
        final = v.load(FINAL)
        for p in final['pinned_final_files']: need(pin(p['path']) == p, 'final-pin:' + p['path'])
        need(final['errors'] == [] and final['finalization_is_not_an_extra_unittest_suite'] is True, 'finalization-not-suite')
    return dict(errors=errors, canonical_capabilities=26, ancestry_rows=37, independent_family_nonexit_decisions=4,
        new_document_links_checked=link_count, run01_tests=519, all_suites_green=False,
        capability_exit_certificates_issued=0, four_family_exit_certificates_issued=0,
        application_execution_count=0, whole_7B_static_assessment_complete=False)


def finalize():
    result = verify(False)
    if result['errors']: raise ValueError(json.dumps(result, ensure_ascii=False))
    if not (v.EV / CHECK).exists():
        exclusive_json(CHECK, dict(envelope('R9-postcapture-publication-integrity-not-unittest-or-exit'), **result,
            run01_receipt=pin(RECEIPT), postcapture_B38_check=pin(POST), publication_tool=pin(SELF)))
    changed = subprocess.run(['git', 'diff', '--name-only', '-z'], cwd=v.ROOT, capture_output=True, check=True).stdout
    untracked = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=v.ROOT, capture_output=True, check=True).stdout
    paths = sorted({p.decode('utf8') for p in (changed + untracked).split(b'\0') if p})
    if any(not p.startswith('docs/audit/') for p in paths): raise ValueError('Unexpected nonaudit change; do not stage user files')
    obj = dict(envelope('R9-final-file-pins-before-commit-not-recertification-or-own-commit-id'), **result)
    obj.update(base_HEAD=v.BASE_HEAD, branch='arena/94ae8414-smartauditerp',
        pinned_final_files=[pin(p) for p in paths if p != E + FINAL],
        pinning_itself_or_its_future_commit_hash=False, finalization_is_not_an_extra_unittest_suite=True,
        preserved_published_R8_audit_inputs=1604, unchanged_application_sources=827,
        source_review_was_run01_input=True, later_phase_validation_ledger_prefixes_publisher_and_check_were_run01_inputs=False)
    exclusive_json(FINAL, obj)
    return obj


def publish():
    branch = subprocess.run(['git', 'branch', '--show-current'], cwd=v.ROOT, capture_output=True, check=True, text=True).stdout.strip()
    head = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=v.ROOT, capture_output=True, check=True, text=True).stdout.strip()
    if branch != 'arena/94ae8414-smartauditerp' or head != v.BASE_HEAD: raise ValueError('Wrong current branch/base for new publication')
    outputs = [v.EV / n for n in (LEDGER, STATUS, PREFIX, CHECK, FINAL, POST, POSTOUT, POSTERR)] + [v.ROOT / p for p in (PHASE, VALIDATION)]
    if any(p.exists() for p in outputs): raise FileExistsError('Preserve existing publication; --finalize only resumes missing finalization')
    captured = v.load(RECEIPT)
    for rel in INDEXES:
        if file_id((v.ROOT / rel).read_bytes()) != captured['inputs_before'][rel]: raise ValueError('Unexpected modified index before prefix: ' + rel)
    post = post_B38_check()
    exclusive_md(PHASE, phase_text(post)); exclusive_md(VALIDATION, validation_text(post))
    exclusive_json(LEDGER, reconciliation(post))
    status = envelope('R9-actual-run01-and-separate-postcapture-B38-status-supplement-not-prior-history-rewrite')
    status.update(preserved_prior_status_input=pin('validation-status-supplement-07B39R8.json'), run01_receipt=pin(RECEIPT),
        run01_journal=pin(JOURNAL), run01_combined_tests=519, new_R9_tests_within519=129,
        run01_B38_assertions=['AssertionError: 162 != 142'], postcapture_B38_check=pin(POST),
        postcapture_B38_assertions=post['assertion_lines_verbatim'], all_suites_green=False, run01_wrapper_exit=1,
        completion_gates_open_exit2=7, integrity_commands_exit0=8,
        phase_validation_ledger_and_index_prefixes_were_run01_inputs=False)
    exclusive_json(STATUS, status)
    record = envelope('R9-three-prefixes-preserve-original-R8-index-bytes-not-history-or-date-rewrite'); record['indexes'] = []
    for rel, text in prefixes().items():
        before = (v.ROOT / rel).read_bytes(); prefix = text.encode('utf8'); after = prefix + before
        (v.ROOT / rel).write_bytes(after)
        record['indexes'].append(dict(path=rel, prefix=file_id(prefix), preserved_suffix=file_id(before), after=file_id(after)))
    exclusive_json(PREFIX, record)
    final = finalize()
    print(json.dumps({'publication_integrity_errors': final['errors'], 'pinned_final_files': len(final['pinned_final_files']),
        'run01_combined_passed': 519, 'capture_B38_failure': '162 != 142', 'postcapture_B38_failure': '163 != 142',
        'all_suites_green': False, 'whole_7B_static_assessment_complete': False}, ensure_ascii=False, indent=2))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__); modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--publish', action='store_true'); modes.add_argument('--verify', action='store_true'); modes.add_argument('--finalize', action='store_true')
    args = parser.parse_args(argv)
    if args.publish: return publish()
    if args.finalize:
        result = finalize(); print(json.dumps({'errors': result['errors'], 'pinned_final_files': len(result['pinned_final_files'])}, ensure_ascii=False)); return 0
    result = verify(); print(json.dumps(result, ensure_ascii=False, indent=2)); return 1 if result['errors'] else 0


if __name__ == '__main__': sys.exit(main())
