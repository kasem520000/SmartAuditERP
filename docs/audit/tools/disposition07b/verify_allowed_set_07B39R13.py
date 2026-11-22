#!/usr/bin/env python3
"""R13 source guards: capability allowed-set landscape + D06 trial-balance parent/child double-count.

Read-only C# lexical facts for the 7C allowed-set obligation, not compilation,
ERP, SQL, WPF, provider, migration, SDK, authorization or financial acceptance.
Branch/year scoping detection is literal pattern presence in selected entry
files; it does not certify that every query inside a capability is scoped, nor
deployed schema, nor runtime enforcement. All prior consumed files, failures
and missing-history limits are preserved unchanged.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
C = ROOT / 'SmartAuditERP'
P = C / 'Form_WPF'
EV = ROOT / 'docs' / 'audit' / 'evidence'
TAG = '07B39R13'

BRANCH_PAT = re.compile(r'MainClass\.BranchNo|BranchCondition|branch\s*=|BranchId\s*=|BranchID\s*=')
YEAR_PAT = re.compile(r'YearPreviews|CmbYearPreviews')

# capability entry-file families (register CAP7B38-D01..D26)
CAP_FILES = {
    'D01': ['frm_ReportDesign.cs', 'frmRptUsersRecords.xaml.cs'],
    'D02': ['Print.cs', 'Report.cs'],
    'D03': ['frmPrintBarcode.xaml.cs', 'frmMultiBarcode.xaml.cs', 'frmItemsBarcode.xaml.cs'],
    'D04': ['Number2Arabic.cs', 'Common.cs'],
    'D05': ['frmAccountBalance.xaml.cs', 'frmAccountsStatement.xaml.cs'],
    'D06': ['frmMezanMorg3a.xaml.cs', 'frmRptCostCenter.xaml.cs', 'frmRptKhzna.xaml.cs'],
    'D07': ['frmRptIncomeStatement.xaml.cs', 'frmItemsBalances.xaml.cs'],
    'D08': ['frmRptItemsActivity.xaml.cs', 'frmRptItemsExpiration.xaml.cs'],
    'D09': ['frmInvsProfit.xaml.cs', 'frmRptItemsProfit.xaml.cs'],
    'D10': ['frmRptInvSalesDetails.xaml.cs', 'frmRptInvSalesDetailsPos.xaml.cs'],
    'D11': ['frmRptInvPurchDetails.xaml.cs', 'frmTaxInvDetails.xaml.cs'],
    'D12': ['frmDecisionHelp.xaml.cs', 'frmrptUsersRecords.xaml.cs'],
    'D13': ['frmInvBySalesMen.xaml.cs', 'FrmRptSalesChart.xaml.cs'],
    'D14': ['frmProductionOrder.xaml.cs'],
    'D15': ['frmRptSand.xaml.cs', 'frmSalaryPay.xaml.cs'],
    'D16': ['frmTaxRptPeriod.xaml.cs', 'frmVATReturn.xaml.cs'],
    'D17': ['frmInvoiceSrch.xaml.cs', 'frmRptEntries.xaml.cs'],
    'D18': ['frmItemsSrch.xaml.cs'],
    'D19': ['frmRecyclingData.xaml.cs'],
    'D20': ['frmEditItems.xaml.cs', 'frmUnits.xaml.cs'],
    'D21': ['frmInvoiceSrch.xaml.cs'],
    'D22': ['frmInvPurch.xaml.cs', 'frmInvSale.xaml.cs'],
    'D23': ['frmSettings.xaml.cs'],
    'D24': ['EntityOperations.cs'],
    'D25': ['frmServerSetting.xaml.cs'],
    'D26': [],
}


def sha16(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def find_line(text: str, needle: str, start: int = 0):
    for i, l in enumerate(text.split('\n')):
        if i >= start and needle in l:
            return i + 1
    return None


def main() -> int:
    receipt: dict = {
        'schema_version': 1,
        'kind': 'R13-capability-allowed-set-landscape-and-D06-trial-balance-double-count',
        'tag': TAG,
        'application_execution_count': 0,
        'read_only': True,
    }

    # ── 1. branch allowed-set mechanism (accounts) ──────────────────
    acc = (C / 'Class' / 'Accounting.cs').read_text(encoding='utf-8-sig', errors='replace')
    usr = (C / 'Class' / 'User.cs').read_text(encoding='utf-8-sig', errors='replace')
    receipt['branch_mechanism'] = {
        'Accounting_BranchCondition_default': {
            'line': find_line(acc, 'public static string BranchCondition'),
            'text': ' and (acc_branch={MainClass.BranchNo} or acc_branch is null ) — session branch or shared (null)',
        },
        'User_LoadUserOperPermission_sets_condition': {'line': find_line(usr, 'Accounting.BranchCondition = ')},
        'OperNo_17_disables_branch_condition': {
            'line': find_line(usr, 'Accounting.BranchCondition = " "'),
            'effect': 'permission 17 (ShowBranchsAccounts) empties the account branch filter — all-branches account view',
        },
    }

    # ── 2. capability allowed-set landscape ─────────────────────────
    landscape = {}
    for cap, names in CAP_FILES.items():
        entry = {'files': []}
        any_branch = False
        any_year = False
        for n in names:
            f = (P / n) if n.endswith('.xaml.cs') else (C / 'Class' / n)
            if not f.exists():
                f = (C / n) if (C / n).exists() else None
            if f is None:
                entry['files'].append({'name': n, 'missing': True})
                continue
            src = f.read_text(encoding='utf-8-sig', errors='replace')
            has_b = bool(BRANCH_PAT.search(src))
            has_y = bool(YEAR_PAT.search(src))
            any_branch = any_branch or has_b
            any_year = any_year or has_y
            entry['files'].append({'name': n, 'bytes': len(src.encode('utf-8', 'replace')),
                                   'branch_scope_pattern': has_b, 'year_preview_refs': has_y})
        entry['branch_scope_pattern_present'] = any_branch
        entry['year_preview_refs_present'] = any_year
        landscape[cap] = entry
    receipt['capability_landscape'] = landscape
    receipt['capability_landscape_note'] = (
        'Pattern presence in selected entry files is an allowed-set indicator, not a '
        'certificate that every query in the capability is scoped. D26 is the phase '
        'completion capability itself (no entry files).'
    )

    # ── 3. D06 trial-balance parent/child double-count ──────────────
    mz = (P / 'frmMezanMorg3a.xaml.cs').read_text(encoding='utf-8-sig', errors='replace')
    mz_lines = mz.split('\n')

    def seg(a, b):
        return '\n'.join(mz_lines[a - 1:b])

    loadtree_body = seg(192, 229)
    travarse_body = seg(357, 495)
    calcsum_body = seg(508, 535)

    receipt['trial_balance_D06'] = {
        'file': 'SmartAuditERP/Form_WPF/frmMezanMorg3a.xaml.cs',
        'LoadtTreeList_192_229_sha16': sha16(loadtree_body),
        'TravarseTree_357_495_sha16': sha16(travarse_body),
        'CalcSum_508_535_sha16': sha16(calcsum_body),
        'display_rows_built_from': 'ALL AccountList nodes (parents and leaves) — line ' + str(find_line(mz, 'foreach (AccountNode node in AccountList)')),
        'parent_aggregates_children_at': find_line(travarse_body, 'root.TrDebtorMovement += Math.Round(account.TrDebtorMovement') and find_line(mz, 'root.TrDebtorMovement += Math.Round(account.TrDebtorMovement'),
        'parent_final_from_aggregates_at': find_line(mz, 'root.TrDeptFinal = root.TrDeptIntial + root.TrDeptBlc'),
        'calcsum_sums_all_display_rows_at': find_line(mz, 'foreach (AccountNode row in _displayRows)'),
        'calcsum_sums': ['TrDebtorMovement', 'TrCreditorMovement', 'TrDeptFinal', 'TrCreditFinal'],
        'adjudication': (
            'CalcSum iterates _displayRows which LoadtTreeList fills from ALL AccountList '
            'nodes; parents already aggregate their children (TravarseTree), so each leaf '
            'movement/final is counted once for the leaf row and once more for every '
            'displayed ancestor — totals and the balanced indicator operate on '
            'double-counted sums when the full tree is displayed (btnShow and btnlvl4 '
            'both rebuild the full list).'
        ),
        'chkPrevbalance_label': 'استثناء الرصيد السابق (exclusion) — the conditional previous add is consistent with the label, not an inversion',
        'date_param_note': '@date1 values are passed as dtFrom.ToShortDateString() strings (culture-fragile pattern, same-thread parse) — observation, not a root',
    }

    # ── 4. D05/D06 exit-criterion adjudication ──────────────────────
    receipt['exit_criterion_adjudications'] = {
        'D05': {
            'criterion': 'اتساق مصدر السنة والمعايير وهوية الحساب والمستند بين إعادة العرض والطفل والمخرج',
            'status': 'NOT MET — adjudicated with numbered roots',
            'roots': ['P7-115 (restore-to-current-DB pattern)', 'P7-176 (year-source inconsistency into the entry-source child, R12)', 'P7-174 (session-branch lines under a global-key header breaks document identity at the Initial child, R12)'],
            'allowed_set_landscape': 'frmAccountBalance/frmAccountsStatement both branch-scoped and year-preview aware; the inconsistency is between redisplay and child, not absence of scoping',
        },
        'D06': {
            'criterion': 'عدم عد الأب والطفل مرتين، وقطع الوقت الصحيح وعضوية المركز ووصول أعمدة السابق إلى كل مخرج',
            'status': 'NOT MET — adjudicated with numbered roots',
            'roots': ['P7-178 (parent+child double-count in CalcSum, this slice)', 'P7-118 (level filter shows wrong level)', 'P7-119 (print drops previous columns)', 'P3-019 (previous dropped in aggregation and secondary-only)', 'P7-052/P7-053 (center membership)', 'P7-062 (cash cutoff at midnight)'],
            'allowed_set_landscape': 'frmMezanMorg3a/frmRptCostCenter/frmRptKhzna all branch-scoped; exit failures are aggregation/output semantics, not scoping absence',
        },
    }

    # ── 5. findings.csv integrity ───────────────────────────────────
    raw = (ROOT / 'docs' / 'audit' / 'findings.csv').read_bytes()
    text = raw.decode('utf-8-sig')
    rows = list(csv.DictReader(io.StringIO(text)))
    receipt['findings_csv'] = {
        'bytes': len(raw), 'bom': raw[:3] == b'\xef\xbb\xbf',
        'crlf': raw.count(b'\r\n'), 'lf_only': raw.count(b'\n') - raw.count(b'\r\n'),
        'rows': len(rows), 'last_id': rows[-1]['id'],
        'p7_max': max(int(r['id'].split('-')[1]) for r in rows if r['id'].startswith('P7-')),
    }

    out = EV / 'capability-allowed-set-07B39R13.json'
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'receipt: {out} ({out.stat().st_size} bytes)')
    print(f"findings rows={receipt['findings_csv']['rows']} last={receipt['findings_csv']['last_id']}")
    ok = (receipt['findings_csv']['bom'] is False
          and receipt['findings_csv']['lf_only'] == 0
          and receipt['findings_csv']['rows'] in (349, 350))
    return 0 if ok else 2


if __name__ == '__main__':
    raise SystemExit(main())
