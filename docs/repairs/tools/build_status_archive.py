#!/usr/bin/env python3
"""Build a conservative, reproducible repair-status overlay over the audit snapshot.

Usage from any directory: python3 docs/repairs/tools/build_status_archive.py [--check]
Does not alter docs/audit. The input snapshot is pinned; update rules deliberately
when reconciling a new audit delivery. `--check` compares without writing.
"""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
REPAIRS = ROOT / 'docs/repairs'
AUDIT = ROOT / 'docs/audit/findings.csv'
RULES = REPAIRS / 'classification_rules.json'


def load_inputs():
    rules = json.loads(RULES.read_text(encoding='utf-8'))
    raw = AUDIT.read_bytes()
    if hashlib.sha256(raw).hexdigest() != rules['findings_sha256']:
        raise ValueError('Audit snapshot differs from pinned SHA-256; reconcile it before rebuilding.')
    with io.StringIO(raw.decode('utf-8-sig'), newline='') as stream:
        findings = list(csv.DictReader(stream))
    ids = [row['id'] for row in findings]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate finding ID in audit snapshot')
    if any(not re.fullmatch(r'P[1-7]-\d{3}', fid) for fid in ids):
        raise ValueError('Finding IDs invalid')
    documents = []
    for name, key in [('TRACKER.md', 'tracker_sha256'), ('PLAN.md', 'plan_sha256')]:
        raw_doc = (REPAIRS / name).read_bytes()
        if hashlib.sha256(raw_doc).hexdigest() != rules[key]:
            raise ValueError(name + ' changed; review classifications and update its pinned hash.')
        documents.append(raw_doc.decode('utf-8'))
    return rules, findings, documents[0], documents[1]


def index_docs(tracker, plan, rules, finding_ids):
    repairs = collections.defaultdict(list)
    for match in re.finditer(r'^### (R-\d+[^\n]*)', tracker, re.M):
        heading = match.group(1)
        for fid in set(re.findall(r'P[1-7]-\d{3}', heading)):
            if fid not in finding_ids:
                raise ValueError('Tracker refers to a finding absent from snapshot: ' + fid)
            for repair in re.findall(r'R-\d+', heading):
                if repair not in repairs[fid]:
                    repairs[fid].append(repair)
    for fid, ids in rules['repair_mapping_overrides'].items():
        if fid not in repairs or not set(ids).issubset(repairs[fid]):
            raise ValueError('Invalid multi-repair mapping: ' + fid)
        repairs[fid] = ids
    for fid, info in rules['extra_repairs'].items():
        if fid not in finding_ids or fid in repairs or not info['repairs']:
            raise ValueError('Invalid supplemental repair: ' + fid)
        for repair in info['repairs']:
            if repair not in plan:
                raise ValueError('Supplemental repair missing from plan: ' + repair)
        repairs[fid] = info['repairs']
    blockers = {}
    headings = list(re.finditer(r'^### (BLK-(P[1-7]-\d{3}))[^\n]*', plan, re.M))
    for index, match in enumerate(headings):
        blocker, fid = match.group(1), match.group(2)
        if fid not in finding_ids or fid in blockers:
            raise ValueError('Unknown or duplicate blocker: ' + blocker)
        # Pull the documented next input from this card only, bounded by the next heading.
        end = re.search(r'^#{2,3} ', plan[match.end():], re.M)
        card = plan[match.end():match.end() + end.start()] if end else plan[match.end():]
        needed = re.search(r'^- \*\*المدخل المطلوب[^*]*:\*\*\s*(.*)$', card, re.M)
        blockers[fid] = (blocker, needed.group(1).strip() if needed else 'راجع بطاقة العائق في PLAN.md.')
    for fid, reason in rules['partial'].items():
        if fid not in repairs or not reason.strip():
            raise ValueError('Partial override needs a repair and a reason: ' + fid)
    return repairs, blockers


def build_rows(findings, repairs, blockers, rules):
    rows = []
    for finding in findings:
        fid = finding['id']
        r = repairs.get(fid, [])
        blocker, needed = blockers.get(fid, ('', ''))
        partial_reason = rules['partial'].get(fid, '')
        if r and (partial_reason or blocker):
            status = 'partial_open'
            note = partial_reason or ('إصلاح جزئي مع عائق موثق؛ ' + needed)
        elif r:
            status = 'closed_in_scope'
            note = 'مغلق في سجل الإصلاح للنطاق الموثق فقط؛ راجع البطاقة وحدود تحققها.'
        elif blocker:
            status = 'deferred_blocked'
            note = needed
        else:
            status = 'pending_review'
            note = 'لا بطاقة إصلاح أو عائق مطابق في المصادر المفهرسة؛ يحتاج فرزاً وتأريضاً.'
        evidence = []
        if r:
            if fid in rules['extra_repairs']:
                evidence.append(rules['extra_repairs'][fid]['evidence'])
            else:
                evidence.append('TRACKER.md: ' + ', '.join(r))
        if blocker:
            evidence.append('PLAN.md: ' + blocker)
        rows.append({
            'id': fid, 'severity_at_audit': finding['severity'], 'certainty_at_audit': finding['certainty'],
            'title': finding['title'], 'audit_status': finding['status'], 'repair_status': status,
            'repair_ids': '; '.join(r), 'blocker_id': blocker,
            'status_evidence': ' ؛ '.join(evidence), 'remaining_or_scope': note,
            'audit_evidence': finding['evidence'],
        })
    return rows


def render_csv(rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode('utf-8-sig')


def render_summary(rows, rules):
    totals = collections.Counter(r['repair_status'] for r in rows)
    categories = [('closed_in_scope', 'مغلق ضمن نطاق الإصلاح'), ('partial_open', 'مصلح جزئياً وما زال مفتوحاً'),
                  ('deferred_blocked', 'مؤجل بعائق موثق'), ('pending_review', 'بانتظار فرز ومراجعة')]
    out = [
        '# سجل حالة الإصلاح — نسخة مشتقة من أرشيف التدقيق', '',
        'هذا سجل متابعة منفصل؛ لم تُعدّل ملفات التدقيق الأصلية ولم تُغلق الحالات فيها. '
        'مصدره `docs/audit/findings.csv` عند تسليم ' + rules['audit_delivery'] + ' (`' + rules['audit_commit'][:7] + '`) '
        'وبصمة SHA-256 `' + rules['findings_sha256'] + '`؛ ويستند إلى بطاقات `TRACKER.md` '
        'وحواجز `PLAN.md` عند لقطة الإصلاح `' + rules['repair_snapshot_commit'] + '` '
        'وقواعد الاستثناء في `classification_rules.json`. لقطة ثابتة وليست تحديثاً تلقائياً.', '',
        '**مهم:** الإغلاق هنا إداري وللنطاق الموثق فقط، ولا يعني قبول ERP أو إثبات إصلاح كل '
        'المواقع خارج ذلك النطاق. الجزئي والمؤجل ما زالا مفتوحين فنياً؛ التأجيل ليس إصلاحاً. '
        'لم يُبنَ التطبيق أو يُشغّل WPF/SQL ضمن اختبارات الإصلاح الموثقة.', '',
        '[الجدول الكامل لكل نتيجة (CSV)](STATUS_ARCHIVE.csv) · '
        '[بطاقات الإصلاح](TRACKER.md) · [الحواجز ومدخلاتها](PLAN.md) · '
        '[قواعد التصنيف](classification_rules.json)', '',
        '## الإجمالي', '', '| الحالة | العدد |', '| --- | ---: |',
    ]
    for code, label in categories:
        out.append('| ' + label + ' (`' + code + '`) | ' + str(totals[code]) + ' |')
    out += ['| **المجموع** | **' + str(len(rows)) + '** |', '',
            '**يحتاج متابعة فنية:** ' + str(len(rows) - totals['closed_in_scope']) +
            ' نتيجة = الجزئي + المؤجل + بانتظار الفرز. هذا ليس عدد اختبارات قبول فاشلة، '
            'ولا يشمل توسعات غير مرقمة خارج أرشيف التدقيق.', '',
            '## التوزيع حسب المرحلة', '',
            '| المرحلة | مغلق ضمن النطاق | جزئي مفتوح | مؤجل بعائق | بانتظار فرز | المجموع |',
            '| --- | ---: | ---: | ---: | ---: | ---: |']
    for phase in range(1, 8):
        group = [r for r in rows if r['id'].startswith('P%d-' % phase)]
        c = collections.Counter(r['repair_status'] for r in group)
        out.append('| P%d | %s | %s | %s | %s | %s |' %
                   (phase, c['closed_in_scope'], c['partial_open'], c['deferred_blocked'],
                    c['pending_review'], len(group)))
    remaining_severity = collections.Counter(r['severity_at_audit'] for r in rows
                                             if r['repair_status'] != 'closed_in_scope')
    out += ['', '## الشدة الأصلية للنتائج التي تحتاج متابعة', '',
            '| الشدة وقت التدقيق | العدد |', '| --- | ---: |']
    for severity, label in [('Critical', 'حرجة'), ('High', 'عالية'),
                            ('Medium', 'متوسطة'), ('Low', 'منخفضة')]:
        out.append('| ' + label + ' | ' + str(remaining_severity[severity]) + ' |')
    out += ['', 'هذه الشدة كما وردت وقت التدقيق، وليست تقييماً جديداً لشدة الأجزاء المتبقية بعد الإصلاح الجزئي.', '',
            'في لقطة P7 تضم النتائج الجزئية P7-035 بسبب تأكيد هويات العملات المعلّق؛ '
            'هذا تصنيف أكثر تحفظاً من ملخص المتتبع السابق الذي عدّها ضمن المنجز. '
            'لا تُعامل الفئات الثلاث خارج الإغلاق على أنها جميعاً عوائق مالك.', '',
            '## كيف تقرأ السجل', '',
            '- `severity_at_audit` و`certainty_at_audit` و`audit_status` محفوظة من التدقيق، ولا تعني تقييم شدة متجدداً أو قبول الإصلاح.',
            '- `closed_in_scope`: توجد بطاقة إصلاح، ولا يُعرف من القواعد أو بطاقة عائق تخص النتيجة أن جزءاً منها متبقٍ. لا يثبت ذلك سلامة النشر أو كل توسيع لاحق.',
            '- `partial_open`: توجد إصلاحات، مع جزء متبقٍ محدد في `remaining_or_scope`. لا يُغلق العمل المتبقي بمجرد إصلاح جزء منه.',
            '- `deferred_blocked`: لا تُسجَّل بطاقة إصلاح مطابقة ويوجد عائق محدد في الخطة؛ خانة `remaining_or_scope` تحمل المدخل المطلوب إن وُجد.',
            '- `pending_review`: لم تُعثر بطاقة مطابقة في الفهرسة؛ لا يُفترض أنها آمنة أو مؤجلة بقرار مالك أو صالحة للإصلاح دون تأريض.',
            '- المطابقات الآلية تقرأ معرّفات النتائج من عناوين بطاقات الإصلاح، والحواجز من عناوين الخطة. تُصحح البطاقات المشتركة والنتائج الجزئية صراحةً في ملف القواعد؛ لا تحل الفهرسة محل مراجعة كل أثر أو قبول تشغيلي.',
            '- الأدلة الأصلية في عمود `audit_evidence` مراجع تاريخية وقد تتغير أرقام أسطر المصدر بعد الإصلاح؛ استخدم اسم الدالة وبطاقة الإصلاح لتحديد الموضع الحالي.', '',
            '## إعادة البناء والتحقق', '',
            'من جذر المستودع: `python3 docs/repairs/tools/build_status_archive.py`؛ '
            'للتحقق من مطابقة المخرجات دون تعديلها أضف `--check`. '
            'تغيير نتائج التدقيق أو الخطة أو المتتبع يوقف المولد حتى تُراجع اللقطة والتصنيفات وتُحدّث البصمات والقواعد عمداً. '
            'ولا يغني ذلك عن مراجعة ما إذا امتد نطاق النتيجة تاريخياً إلى مواقع أخرى.', '']
    return '\n'.join(out).encode('utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    rules, findings, tracker, plan = load_inputs()
    repairs, blockers = index_docs(tracker, plan, rules, {r['id'] for r in findings})
    rows = build_rows(findings, repairs, blockers, rules)
    outputs = {REPAIRS / 'STATUS_ARCHIVE.csv': render_csv(rows),
               REPAIRS / 'STATUS_ARCHIVE.md': render_summary(rows, rules)}
    for path, data in outputs.items():
        if args.check:
            if not path.exists() or path.read_bytes() != data:
                print('STALE:', path.relative_to(ROOT), file=sys.stderr)
                return 1
        else:
            path.write_bytes(data)
    print('Results:', len(rows), dict(collections.Counter(r['repair_status'] for r in rows)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
