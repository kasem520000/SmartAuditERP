#!/usr/bin/env python3
"""Prospective R9 semantic root-comparison correction after run01 publication.

Do not rewrite the consumed packet or its 519 results. Five original-root
comparison reasons were too generic or mischaracterized adjacent mechanics.
Publish explicit replacements with original dictionary/source pins. Preserve
initial publication byte versions and prefix them, then check B38 separately.
This checker is not an additional source/ERP unittest suite or exit decision.
"""
from __future__ import annotations

import argparse
from collections import Counter
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import publish_save_edit as prior

v = prior.v
E = prior.E
SUPPLEMENT = 'save-edit-root-comparison-supplement-' + v.TAG + '.json'
LEDGER = 'capability-reconciliation-rev02-' + v.TAG + '.json'
PREFIX = 'index-prefix-supplement-rev02-' + v.TAG + '.json'
FINAL = 'finalization-before-commit-rev02-' + v.TAG + '.json'
POST = 'postcapture-root-supplement-B38-check-' + v.TAG + '.json'
OUT, ERR = ('B38-postcapture-root-supplement-' + v.TAG + e for e in ('.stdout.txt', '.stderr.txt'))
PHASE, VALIDATION = ('docs/audit/' + n + '-07B39R9-rev02.md' for n in ('PHASE', 'VALIDATION'))
SELF = 'docs/audit/tools/disposition07b/publish_save_edit_rev02.py'
IDS = ('P1-013', 'P2-006', 'P3-025', 'P4-014', 'P6-001')


def replacement_rows():
    facts = v.load(v.FACTS); initial = v.load(v.ROOTS)
    def basis(rel, *sels):
        return [dict(path=rel, selector=s, **{k: v.method(facts, rel, s)[k] for k in ('start', 'end', 'syntax_utf8_sha256')}) for s in sels]
    rows = [
        ('P1-013', 'potential-visual-tree-before-show-not-document-key-root',
         'The original potential root is WPF visual-tree permission application before a window is shown. It is NOT primarily the new Name/Tag/document-key question. GetTargetButtons traverses visual children, and selected Home handlers apply UI permission before Show. This supports keeping the lifecycle concern open, not certifying an absent rendered tree or a runtime bypass.',
         'Written Show order does not establish Loaded/template/event timing; preserve potential. Remaining visual-tree helper owners and all opener lifecycle routes are still local. Name/Tag policy identities remain a separate unnumbered question.',
         basis(v.FP, 'GetTargetButtons', 'ApplyFrmPermissionInternal') + basis(v.HOME, 'stripInputInv_Click', 'stripTransfer_Click') + basis(v.MC, 'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions')),
        ('P2-006', 'create-edit-permission-contract-not-SQL-grant-root',
         'The original confirmed root is inconsistency in the create/edit permission contract between permission editor and enforcing consumer, NOT a SQL-grant/trust root. R9 FormPermission reads IS_New/IS_Save, derives Addable/Editable by visited buttons, and Common.ApplyEditAddPermissionInternal consumes those flags against IsNew; Common.AllowEdit separately reads IS_Edit. These are relevant consumer-side distinctions, not proof of a deployed grant defect.',
         'The original frmUsersPermissions and frmTreasury bodies are cited by their unchanged dictionary, not newly wholly reread in this supplement. Complete the permission-editor-to-consumer mapping and lookup variants locally before deciding exact extension/equivalence of the command question; no new root or remediation.',
         basis(v.FP, 'ApplyFrmPermissionInternal', 'ctor:FormPermission') + basis(v.COMMON, 'AllowEdit', 'ApplyEditAddPermissionInternal') + basis(v.MC, 'ApplyWpfPermissions')),
        ('P3-025', 'notice-header-versus-entry-date-not-rounding-root',
         'The original confirmed root is editing a credit/debt note date while keeping the old note-header date and changing its journal-entry date. It is NOT an invoice rounding root or generic independent-transaction/null-entry problem. The six-editor R9 mapping/SaveEnty review does not by itself extend that notice-date defect.',
         'The prior R7 local note-writer followthrough and original frmCreditNote/frmDebtNote references remain carried evidence, not a fresh complete R9 note-writer review. Keep P3-003 transaction separation, P3-002 entry invariants and unnumbered null-entry/cache questions separate from P3-025; no date/fiscal execution or root-status change.',
         basis(v.EO, 'SaveEnty') + basis(v.IP, 'MappingInvoice', 'BindToEntry', 'SaveInvoice')),
        ('P4-014', 'potential-loaded-stock-versus-atomic-save-not-entry-invariant-root',
         'The original potential root is a stock-availability guard relying on previously loaded stock without atomic revalidation at save. It is NOT the independent EntryOper transaction or entry-balance question. Full R9 central SaveInvoice/cache bodies provide bounded writer/cache context, but DataTable cache mutation order does not prove a concurrency race or persistent stock loss.',
         'Keep potential. Complete remaining ItemOper.ISvalidQuantity and stock/reload/line/transaction owners before assessing the race claim. No deployed locks/isolation/stock provider result or interleaving is executed or certified.',
         basis(v.STOCK, 'UpdateItemStock') + basis(v.IP, 'SaveInvoice') + basis(v.IPC, 'SaveInvoice') + basis(v.POS, 'SaveAndPrint') + basis(v.PURCH, 'SaveAndPrint')),
        ('P6-001', 'invoice-tax-classification-not-remote-commit-order-root',
         'The original confirmed root is inconsistent invoice-tax classification between save guard and ZATCA conversion. It is NOT simply tax integration or remote/local commit ordering. R9 read the save-side type/customer guards and IsTaxCustomer; ordering evidence belongs primarily to P6-007 and cannot alone recertify the P6-001 converter comparison.',
         'Original ZatcaService and sync-status references are retained, not claimed as complete newly read converter bodies in this supplement. Finish exact type/customer/code classification mapping locally; no remote classification/acceptance run or forced root merge.',
         basis(v.IP, 'SaveInvoice', 'IsTaxCustomer') + basis(v.IPC, 'SaveInvoice')),
    ]
    return [dict(root_id=rid, canonical_prior_row=initial['focused_root_reviews'][rid]['canonical_prior_row'],
        initial_consumed_R9_reason_verbatim=initial['focused_root_reviews'][rid]['reason'],
        replacement_classification=classification, replacement_reason=reason, counterevidence_and_local_remainder=limit,
        source_basis=src, original_severity_certainty_status_changed=False, novelty_certified=False,
        accepted_external_handoff=False, fresh_whole_original_root_source_audit_claimed=False)
        for rid, classification, reason, limit, src in rows]


def supplement():
    result = prior.envelope('R9-postcapture-five-root-reason-semantic-correction-not-consumed519-input')
    result.update(initial_consumed_root_packet=prior.pin(v.ROOTS), initial_consumed_source_review=prior.pin('docs/audit/SOURCE-REVIEW-07B39R9.md'),
        initial_publication_ledger=prior.pin(prior.LEDGER), initial_publication_finalization=prior.pin(prior.FINAL),
        corrections=replacement_rows(), reason_for_prospective_correction='Initial reasons were partly generic/mischaracterized (notably P2-006 SQL grant and P3-025 rounding). Preserve the inaccurate authored bytes and replace their interpretation explicitly, not by silently rewriting consumed evidence.',
        initial_consumed_reason_strings_remain_historical_not_current_interpretation=True,
        initial_run01_recaptured_or_relabelled=False, this_semantic_supplement_was_run01_input=False,
        new_unittest_case_count=0, new_source_body_count_claimed=0,
        no_all339_or_missing345_semantic_recertification=True,
        preserved_R7_notice_followthrough=prior.pin('entry-source-local-followthrough-decisions-07B39R7.json'))
    return result


def b38_check():
    command = [sys.executable, '-B', '-W', 'error::ResourceWarning', '-m', 'unittest', 'discover',
        '-s', 'docs/audit/tools/census07b', '-p', 'test_7b_completion.py', '-v']
    started, tick = prior.clock(), time.monotonic()
    with (v.EV / OUT).open('xb') as stdout, (v.EV / ERR).open('xb') as stderr:
        process = subprocess.run(command, cwd=v.ROOT, stdout=stdout, stderr=stderr, check=False)
    text = (v.EV / ERR).read_text(); match = re.search(r'^Ran (\d+) tests in ([\d.]+)s$', text, re.M)
    cases = re.findall(r'^(test_\w+) \(([^)]+)\) \.\.\. (ok|FAIL|ERROR)$', text, re.M)
    result = prior.envelope('R9-second-postcapture-B38-only-check-after-one-prospective-correction-publisher-not519')
    result.update(command=command, exit_code=process.returncode, raw_started_clock_verbatim=started,
        raw_finished_clock_verbatim=prior.clock(), wall_seconds=round(time.monotonic() - tick, 6),
        reported_tests=int(match[1]) if match else None, reported_unittest_seconds=float(match[2]) if match else None,
        actual_verbose_case_lines=len(cases), actual_case_status_counts=dict(Counter(r[2] for r in cases)),
        assertion_lines_verbatim=re.findall(r'^AssertionError:.*$', text, re.M),
        stdout=prior.pin(OUT), stderr=prior.pin(ERR), publication_tool=prior.pin(SELF),
        original_expected142_unchanged=True, no_new_tests_added_to519=True, all_suites_green=False)
    prior.exclusive_json(POST, result); return result


def texts(post):
    phase = f'''# 07B39R9 rev02 — التسليم الحالي مع تصحيح صريح لمقارنة خمسة جذور

**7B مفتوحة؛ صفر خروج قدرة/أسرة وصفر إحالة إكمال جديدة مقبولة؛7C لم تبدأ و8 غير مأذونة.** لا تعديل/بناء/تشغيل ERP أو SQL/WPF/provider/SDK أو قبول مالي/تشغيلي.

[العمل المصدري التفصيلي المحفوظ](PHASE-07B39R9.md) · [مراجعة المصدر المستهلكة](SOURCE-REVIEW-07B39R9.md) · [ملحق التصحيح الحالي](evidence/{SUPPLEMENT}) · [تسوية26 المصححة](evidence/{LEDGER}) · [التحقق والفصل الزمني](VALIDATION-07B39R9-rev02.md) · [المتبقي المحلي](evidence/{v.WORK})

## الإنجاز المصدري الفعلي باقٍ

تُتبعت أوامر الحفظ/الطباعة/Pay/Hold/quotation/repayment والمفاتيح في المحررات الستة حتى كاتبي SaveInvoice كاملين والقيد/الذاكرة/المعاملة والنشر، مع23 حكم دخول وست سلاسل مستقلة. وقُرئت المداخل البديلة المختارة وأجسام الاستيراد الأربعة. فروق الحفظ والطباعة، المعاملات المستقلة، cache قبل النجاح/خارجه، ونتائج void موثقة مع الشواهد المضادة: **POS cache بعد النجاح فقط، والمشتريات ترفض null entry في فرعها المالي المحدد**.

**رُفض ادعاء نقص معاملات رأس العقد الأربعة:** موجودة عند1121–1124 قبل Execute عند1138. لم تُنشأ نتيجة جديدة ولم تُلصق بـP4-020 الإنتاجية. لا cache DataTable = فقد مخزون SQL مرصود، ولا source order = جدولة WPF أو حفظ مزدوج مرصود.

## تصحيح دقة المقارنة بعد519، لا تغيير للقواميس الأصلية

كانت بعض تعليلات R9 الأولى عامة أو وصفت سياقًا غير مطابق للجذر. تحفظ النسخ الأولى كاملة في ملفاتها وأرشيف المدخلات؛ **يحل هذا الملحق محل تعليل المقارنة لتلك الخمسة فقط**:

| الجذر | التعريف/الحكم المصحح |
| --- | --- |
| **P1-013 — potential** | تطبيق صلاحيات على الشجرة المرئية قبل Show؛ ليس أساسًا سؤال Name/Tag الجديد. GetTargetButtons يستعرض visual children، لكن توقيت بناء الشجرة/Loaded غير منفذ ولا يصحح اليقين. |
| **P2-006 — confirmed** | عدم اتساق عقد الإنشاء/التعديل بين محرر الصلاحية ومنفذها، **لا جذر منح SQL**. IS_New/IS_Save→Addable/Editable وIS_Edit المستقل سياق مستهلك ذي صلة؛ محرر الصلاحيات/كل المستهلكين ما زالوا عملًا محليًا، لا مراجعة جديدة مكتملة لهم. |
| **P3-025 — confirmed** | اختلاف تاريخ رأس الإشعار وقيده بعد التعديل، **لا التقريب الحسابي أو generic null/transaction**. أدلة R7/قاموس الإشعار محفوظة، لكن قراءة المحررات الستة لا تثبت امتداد علة الإشعار تلقائيًا. |
| **P4-014 — potential** | حارس توفر مخزون محمّل بلا إعادة تحقق ذرية عند الحفظ، **لا حارس توازن القيد أو معاملة EntryOper**. بقيت ItemOper/ملاك reload والتداخلات/العزل غير محسومة؛ لا race/فقد مرصود. |
| **P6-001 — confirmed** | اختلاف تصنيف الفاتورة الضريبية بين حارس الحفظ ومحول ZATCA، **لا مجرد ترتيب remote/local commit**. ترتيب الإرسال يدعم P6-007؛ يلزم استكمال مقارنة محول التصنيف محليًا، ولا تصديق جديد للجذر من الترتيب وحده. |

شدة/يقين/حالة/نوع/أدلة كل قاموس أصلي دون تعديل؛ P1-013/P4-014/P7-132 تبقى potential. لا استحداث نتيجة أو حسم novelty عبر الست المفقودة. التصحيح مراجعة دقة بشرط المصدر لا نجاح آلي في فهمه؛ لا تضخم لعدد الأجسام أو الحالات.

## التحقق وحدوده

**run01 المحفوظ:519/519 في135.081ثانية**؛129 جديدة ضمن519. B38 أثناءه42نجاحًا/فشل1من43، `162 != 142`، والغلاف1. فحص النشر الأول اللاحق أبقى43/فشل1، `163 != 142`.

بعد إضافة ناشر هذا التصحيح شُغلت **B38 وحدها مجددًا**: {post['actual_case_status_counts'].get('ok', 0)}نجاحًا/فشل{post['actual_case_status_counts'].get('FAIL', 0)}من{post['reported_tests']} في{post['reported_unittest_seconds']}ثانية، `{'; '.join(post['assertion_lines_verbatim'])}`، exit{post['exit_code']}. ليست هذه الحالات إضافة إلى519 أو بديلًا عن أي فشل سابق؛162/163/164 تعداد أدوات Python في ثلاثة نطاقات، لا تعداد حالات/أجسام. توقع142 لم يُعدّل ولم تُخفَ أدوات.

**ملحق التصحيح، هذه الوثيقة، التسوية rev02 وبوادئ الفهارس وفحوصها ليست مدخلات519**. لا suite جديدة لهذا الملحق؛ الفحوص اللاحقة تقارن هوية5قواميس/مصادر، وحفظ26/37/الأسر الأربع والنسخ/الروابط، لا تثبت صحة المعنى أو قراءةً أو تقويمًا. كل الإخفاقات والنسخ المستهلكة الأولى محفوظة.

## المتبقي دون إخفاء أو إحالة مبكرة

D08/D17/D19/D22/D25 تقدم محدود، وبقية21 قدرة محمولة لا مراجعة جديدة لها؛ لا إكمال ستة محررات أو كل R8LOCAL-SAVE-EDIT. التالي بقية الفتّاحات ومنتجي مفاتيحها/allowed-document/branch/year، SearchByID/ItemOper/merge/unit/serial/VAT، transfer/broker/offline/POS tables، type/fallback العقد، السنة/الإغلاق، ومتبقي26قدرة وأسئلة R7D05/D06 و@Recipient. أضيف إكمال المقارنات الخمس الدقيقة للمحلي، ولا يُحال إلى عقد خارجي غائب.

827مصدر تطبيق/29,128,444بايت وسجل335/raw336CRLF وملحقR1 دون تعديل.339 قاموسًا محفوظًا لا339مراجعة جديدة أو345/196/49recertification. مرجع R9 الجديد16نوفمبر2026UTC حسب الجلسة استشرافي؛ لا تصديق21NovR8/نسبة التاريخ للمستخدم أو22Nov من تلخيص/ساعات، ولا chronology R6. **7B مفتوحة؛7C لم تبدأ و8 غير مأذونة.**
'''
    validation = f'''# 07B39R9 rev02 — فصل تصحيح المعنى اللاحق عن نتائج run01

[التحقق الأول المحفوظ](VALIDATION-07B39R9.md) و[إيصال519](evidence/{prior.RECEIPT}) وأرشيف18عضوًا/582385بايت/SHA`3b7f88aa9b67509ccd81c492ba531df3b0a098e7c952ec3a9d184143bb0b4374` لم تتغير.519/519في135.081ثانية، وB38فشل `162 != 142` والغلاف1؛ فحص النشر الأول فشل `163 != 142` محفوظ أيضًا.

**لم يصحح نجاح assertions التعليل الدلالي تلقائيًا.** مراجعة القواميس الفعلية كشفت عمومية/سوء نسبة في خمسة تعليلات. [ملحق المقارنة](evidence/{SUPPLEMENT}) يحفظ كل تعليل أول بالنص ويحدد بديله، قاموسه الأصلي ومصدره وحدوده ومتبقيه المحلي. لا تغيير للنتائج المرقمة أو أدوات/أدلة run01 أو نسبه/فشله؛ لا اختبار ERP/حساب/صلاحية منشورة.

بعد إضافة أداة النشر rev02 شُغلت B38 وحدها فعلًا: **{post['actual_case_status_counts'].get('ok', 0)}نجاحًا وفشل{post['actual_case_status_counts'].get('FAIL', 0)}من{post['reported_tests']} في{post['reported_unittest_seconds']}ثانية**، `{'; '.join(post['assertion_lines_verbatim'])}`، exit{post['exit_code']}. [الإيصال](evidence/{POST}) · [stderr](evidence/{ERR}). **ليست كل المجموعات خضراء**؛ لم يتغير توقع142 ولم تُنقل الأدوات/تخفَ. لم تضف أي حالة إلى519.

فحص نشر التصحيح يتحقق من حفظ كل ملف نهائي أول ببايتاته، والفهارس الثلاثة بلاحقتها الأولى كاملة؛ ومن عدم تغيير القواميس26/النسب37/الأسر الأربع، ومن مصدر/هوية كل تصحيح. هذا تحقق اتساق وحفظ منفصل، **ليس suite جديدة أو شهادة صحة دلالية/قراءة/تقويم/قدرة**. تسوية rev02 والوثائق والبوادئ الجديدة ليست مدخلات519.

مرجع16نوفمبر2026UTC استشرافي حسب الجلسة؛ raw clocks/21NovR8/22Novالتلخيص ليست سلطة تاريخ أو توثيقًا رجعيًا.827مصدر تطبيق لم تعدل/تبن/تشغل. لا345/196/49reconstruction أو قبول إحالة إكمال؛7Bمفتوحة و7Cلمتبدأ و8غيرمأذونة.
'''
    return phase, validation


def verify():
    errors = prior.capture_errors() + v.verify(True)['errors']
    def need(ok, label):
        if not ok: errors.append(label)
    initial_final = v.load(prior.FINAL)
    for pin in initial_final['pinned_final_files']:
        raw = (v.ROOT / pin['path']).read_bytes(); same = prior.file_id(raw) == {k: pin[k] for k in ('bytes', 'sha256')}
        if not same and pin['path'] in prior.INDEXES:
            same = len(raw) > pin['bytes'] and prior.sha(raw[-pin['bytes']:]) == pin['sha256']
        need(same, 'initial-final-file-version-not-preserved:' + pin['path'])
    doc, initial, facts = v.load(SUPPLEMENT), v.load(v.ROOTS), v.load(v.FACTS)
    need([r['root_id'] for r in doc['corrections']] == list(IDS), 'five-exact-original-root-ids')
    need(doc['new_unittest_case_count'] == 0 and doc['this_semantic_supplement_was_run01_input'] is False
         and doc['initial_run01_recaptured_or_relabelled'] is False, 'no-retroactive519-input-or-results-claim')
    for row in doc['corrections']:
        old = initial['focused_root_reviews'][row['root_id']]
        need(row['canonical_prior_row'] == old['canonical_prior_row']
             and row['initial_consumed_R9_reason_verbatim'] == old['reason'], 'exact-initial-root-dictionary-and-reason:' + row['root_id'])
        need(row['replacement_reason'] != old['reason'] and bool(row['counterevidence_and_local_remainder'])
             and not any(row[k] for k in ('original_severity_certainty_status_changed', 'novelty_certified', 'accepted_external_handoff', 'fresh_whole_original_root_source_audit_claimed')), 'qualified-semantic-correction:' + row['root_id'])
        errors += v.previous.source_basis_errors(row['source_basis'], facts)
    ledger, old_ledger = v.load(LEDGER), v.load(prior.LEDGER)
    expected = copy.deepcopy(old_ledger)
    for row in doc['corrections']:
        expected['R9_findings_delta']['focused_root_reviews'][row['root_id']]['reason'] = row['replacement_reason'] + ' ' + row['counterevidence_and_local_remainder']
    for key in old_ledger: need(ledger[key] == expected[key], 'only-five-reasons-superseded-in-new-ledger:' + key)
    need(ledger['initial_consumed_root_packet_preserved'] is True and ledger['new_unittest_case_count_for_semantic_supplement'] == 0, 'corrected-ledger-no-recertification')
    for row in v.load(PREFIX)['indexes']:
        raw = (v.ROOT / row['path']).read_bytes(); n = row['prefix']['bytes']
        need(prior.file_id(raw[:n]) == row['prefix'] and prior.file_id(raw[n:]) == row['preserved_initial_R9_full_file']
             and prior.file_id(raw) == row['after'], 'rev02-prefix-and-initial-R9-suffix:' + row['path'])
    post = v.load(POST)
    need(post['reported_tests'] == post['actual_verbose_case_lines'] == 43 and post['exit_code'] == 1
         and post['actual_case_status_counts'] == {'ok': 42, 'FAIL': 1}
         and post['assertion_lines_verbatim'] == ['AssertionError: 164 != 142'], 'latest-real-B38-failure-not-green')
    for key in ('stdout', 'stderr', 'publication_tool'): need(prior.pin(post[key]['path']) == post[key], 'latest-post-check-pin:' + key)
    for rel in (PHASE, VALIDATION):
        for target in re.findall(r'\]\(([^)]+)\)', (v.ROOT / rel).read_text()):
            if '://' not in target and not target.startswith('#'):
                need(((v.ROOT / rel).parent / target.split('#')[0]).is_file(), 'rev02-doc-link:' + rel + ':' + target)
    if (v.EV / FINAL).exists():
        for pin in v.load(FINAL)['pinned_final_files']: need(prior.pin(pin['path']) == pin, 'latest-final-file-pin:' + pin['path'])
    return dict(errors=errors, original_capabilities_preserved=26, ancestry_records_preserved=37,
        family_nonexit_decisions_preserved=4, corrected_root_comparison_reasons=5,
        initial_run01_passed_tests_not_changed=519, new_unittest_cases_in_semantic_supplement=0,
        application_execution_count=0, all_suites_green=False, whole_7B_static_assessment_complete=False)


def publish():
    names = (SUPPLEMENT, LEDGER, PREFIX, FINAL, POST, OUT, ERR)
    if any((v.EV / n).exists() for n in names) or any((v.ROOT / p).exists() for p in (PHASE, VALIDATION)):
        raise FileExistsError('Preserve correction publication; no overwrite')
    # Confirm the initial publication is intact BEFORE prefixing it prospectively.
    check = prior.verify()
    if check['errors']: raise ValueError(json.dumps(check, ensure_ascii=False))
    prior.exclusive_json(SUPPLEMENT, supplement())
    post = b38_check(); phase, validation = texts(post)
    prior.exclusive_md(PHASE, phase); prior.exclusive_md(VALIDATION, validation)
    ledger = copy.deepcopy(v.load(prior.LEDGER))
    for row in v.load(SUPPLEMENT)['corrections']:
        ledger['R9_findings_delta']['focused_root_reviews'][row['root_id']]['reason'] = row['replacement_reason'] + ' ' + row['counterevidence_and_local_remainder']
    ledger.update(prospective_root_comparison_supplement=prior.pin(SUPPLEMENT), initial_R9_ledger_preserved=prior.pin(prior.LEDGER),
        initial_consumed_root_packet_preserved=True, new_unittest_case_count_for_semantic_supplement=0,
        rev02_ledger_was_run01_input=False, latest_postcapture_B38_check=prior.pin(POST))
    prior.exclusive_json(LEDGER, ledger)
    record = prior.envelope('R9-rev02-prospective-semantic-correction-prefixes-preserve-initial-publication'); record['indexes'] = []
    for rel in prior.INDEXES:
        before = (v.ROOT / rel).read_bytes()
        text = f'''# تحديث دقة المقارنة — 07B39R9 rev02 (الحالة الحالية)

**7B مفتوحة؛ صفر خروج قدرة/أسرة أو إحالة إكمال جديدة مقبولة؛7C لم تبدأ و8 غير مأذونة.** [التسليم المصحح](PHASE-07B39R9-rev02.md) · [تصحيح خمسة تعليلات](evidence/{SUPPLEMENT}) · [تسوية26 المصححة](evidence/{LEDGER}) · [فصل التحقق](VALIDATION-07B39R9-rev02.md).

الإنجاز المصدري للحفظ/الصلاحيات/القيد/الذاكرة والنشر باقٍ، وكذلك شاهد نفي نقص معاملات العقد. صُححت دقة مقارنة خمسة جذور **بعد519**: P1-013 الشجرة المرئية قبلShow؛P2-006 عقد الإنشاء/التعديل لا منحSQL؛P3-025 تاريخ الإشعار/القيد لا rounding؛P4-014 توفر المخزون/التحقق الذري لا توازن القيد؛P6-001 تصنيف الضريبة لا ترتيب remote commit. القواميس واليقين/الشدة/الحالة الأصلية لم تتغير، ولا نتيجة مرقمة جديدة أو اكتمال المحلي.

519/519في135.081ثانية محفوظة مع فشلB38 `162 != 142`؛ فحص النشر الأول `163 != 142`، وآخر فحص مستقل43حالة/42نجاحًا/فشل1 `164 != 142` بعد إضافة ناشر التصحيح. **ليست كل المجموعات خضراء**. التصحيح/هذه البادئة/تسويته ليست مدخلات519 ولا suite إضافية؛ لم يعدّل توقع142 أو يمح أي فشل. 827مصدر تطبيق دون تغيير/تشغيل، و345/196/49المفقودة لم تعاد. مرجع16NovR9 استشرافي لا raw-clock/chronology attestation.

النص التالي هو تسليم R9 الأول المحفوظ كاملًا ببايتاته؛ تعليلات الجذور الخمسة فيه تُقرأ مع التصحيح الصريح أعلاه، لا بوصفها التفسير الحالي.

## أرشيف R9 الأول وما قبله — bytes محفوظة

'''
        prefix = text.encode('utf8'); after = prefix + before; (v.ROOT / rel).write_bytes(after)
        record['indexes'].append(dict(path=rel, prefix=prior.file_id(prefix), preserved_initial_R9_full_file=prior.file_id(before), after=prior.file_id(after)))
    prior.exclusive_json(PREFIX, record)
    result = verify()
    if result['errors']: raise ValueError(json.dumps(result, ensure_ascii=False))
    changed = subprocess.run(['git', 'diff', '--name-only', '-z'], cwd=v.ROOT, capture_output=True, check=True).stdout
    untracked = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '-z'], cwd=v.ROOT, capture_output=True, check=True).stdout
    paths = sorted({r.decode('utf8') for r in (changed + untracked).split(b'\0') if r})
    if any(not p.startswith('docs/audit/') for p in paths): raise ValueError('Unexpected nonaudit change')
    final = dict(prior.envelope('R9-rev02-final-pins-preserve-initial519-and-publication-versions'), **result)
    final.update(pinned_final_files=[prior.pin(p) for p in paths if p != E + FINAL],
        preserved_initial_R9_finalization=prior.pin(prior.FINAL), semantic_correction_is_not_new_unittest_or_runtime_acceptance=True)
    prior.exclusive_json(FINAL, final)
    print(json.dumps(result, ensure_ascii=False, indent=2)); return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__); group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--publish', action='store_true'); group.add_argument('--verify', action='store_true'); args = parser.parse_args(argv)
    if args.publish: return publish()
    result = verify(); print(json.dumps(result, ensure_ascii=False, indent=2)); return 1 if result['errors'] else 0


if __name__ == '__main__': sys.exit(main())
