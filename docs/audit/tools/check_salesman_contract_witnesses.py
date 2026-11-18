#!/usr/bin/env python3
"""Deterministic manual B10 contrasts and bounded source text observations.

Stdlib only, no ERP imports/translations/build/runtime or actual export/shell.
An upstream worker/WPF gate remains. A Notes view/synonym in deployment is NOT
assumed present or absent. These are documentary fixtures, not SQL/WPF/Office,
financial/policy/commission/authorization acceptance or a remediation claim.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
F = 'SmartAuditERP/Form_WPF/'
C = 'SmartAuditERP/Class/'
M = 'SmartAuditERP/Class_WPF/'
S = F + 'frmInvBySalesMen.xaml.cs'; SX = F + 'frmInvBySalesMen.xaml'
P = F + 'frmRptItemsProfit.xaml.cs'; PX = F + 'frmRptItemsProfit.xaml'
T = F + 'frmRptSalesInPeriod.xaml.cs'; TX = F + 'frmRptSalesInPeriod.xaml'
D = F + 'frmDebtNote.xaml.cs'; SM = F + 'frmSalesMen.xaml.cs'
SQ = F + 'frmSandQ.xaml.cs'; QD = F + 'frmSandQD.xaml.cs'
SI = F + 'frmSalesInvoice.xaml.cs'; ID = F + 'frmItemsDetails.xaml.cs'
IDX = F + 'frmItemsDetails.xaml'; IO = C + 'InvoiceOper.cs'; IT = C + 'ItemOper.cs'
MC = C + 'MainClass.cs'; RS = 'SmartAuditERP/Properties/Resources.resx'
HM = 'SmartAuditERP/Home.xaml.cs'; HX = 'SmartAuditERP/Home.xaml'
SR = M + 'SalesManRowItem.cs'; TR = M + 'SaleItemRow.cs'
ILL = []; ST = []; READS = {}
LIMIT = (
    'Independent hand-selected documentary contrast ONLY. No C#/SQL/WPF/Office execution/translation, '
    'deployment schema/alias/data/ACL/policy/commission/GL acceptance or certification. '
    'The upstream worker/WPF gate P7-054 is NOT assumed resolved: downstream fixtures isolate '
    'well-formed rows/criteria without claiming the normal UI reached them. Notes compatibility '
    'is not assumed in deployment. No real data, secrets, exports, consumer/formula interpreter or shell.'
)
TEXT_LIMIT = (
    'Bounded literal/structural observation of inert source text only. Not a semantic callgraph, '
    'deployed schema/view/synonym/permission/availability proof, SQL/WPF rendering, complete child '
    'review, financial acceptance or measured latency/leak/index judgment. No application execution.'
)


def ev(*pairs):
    return ';'.join(f'{path}:{start}-{end}' for path, start, end in pairs)


def illustration(title, roots, inputs, observed, reference, difference, refs):
    assert (observed != reference) is difference, title
    ILL.append(dict(id=f'ALG7B10-{len(ILL)+1:02d}', title=title, finding_ids=roots,
                    hand_selected_inputs=inputs, manual_observation_model=observed,
                    independent_reference=reference, difference_expected=difference,
                    illustration_assertions_passed=True, evidence=refs,
                    source_application_executed=False, limit=LIMIT))


def span(path, start, end):
    lines = (ROOT / path).read_text(encoding='utf-8-sig').splitlines()
    assert 1 <= start <= end <= len(lines)
    text = '\n'.join(lines[start - 1:end])
    READS[(path, start, end)] = dict(path=path, start=start, end=end,
                                    selected_text_sha256=hashlib.sha256(text.encode()).hexdigest())
    return text


def literal(title, roots, pairs, predicate, description):
    values = [span(*p) for p in pairs]
    ok = bool(predicate(values))
    assert ok, title
    ST.append(dict(id=f'ST7B10-{len(ST)+1:02d}', title=title, finding_ids=roots,
                   documented_observation=description, documented_text_observation_matches=ok,
                   evidence=ev(*pairs), source_application_executed=False, limit=TEXT_LIMIT))


def main():
    movements = [dict(value=100, commission=10, sign=1), dict(value=40, commission=4, sign=-1),
                 dict(value=10, commission=1, sign=-1)]
    illustration('Unsigned value sum disagrees with the signed movement contract', 'P7-111',
                 dict(rows=movements, upstream_gate_isolated_not_fixed=True),
                 dict(value=sum(x['value'] for x in movements), commission=sum(x['sign']*x['commission'] for x in movements)),
                 dict(value=sum(x['sign']*x['value'] for x in movements), commission=5), True,
                 ev((S,279,290),(S,309,343),(S,375,398),(S,482,510),(S,781,796),(SR,10,24)))
    illustration('A sale-only population is counterevidence to an unconditional total difference', 'P7-111',
                 dict(value=100, sign=1, gross_vs_net_policy_requires_label=True),
                 dict(unsigned_total=100, signed_total=100), dict(unsigned_total=100, signed_total=100), False,
                 ev((S,482,510),(S,781,796)))
    illustration('All-period has different invoice and receipt membership in the same request', 'P7-112',
                 dict(all_period=True, invoice_periods=['old','today'], receipt_periods=['old','today'], control_dates='today'),
                 dict(invoice_periods=['old','today'], receipt_periods=['today']),
                 dict(invoice_periods=['old','today'], receipt_periods=['old','today']), True,
                 ev((S,189,218),(S,401,439)))
    illustration('A deliberately restricted period is not the all-period split', 'P7-112',
                 dict(all_period=False, selected_period='today', endpoint_effect_isolated=True),
                 dict(invoice_periods=['today'], receipt_periods=['today']),
                 dict(invoice_periods=['today'], receipt_periods=['today']), False,
                 ev((S,189,218),(S,411,439)))
    illustration('Local reader and writer request different relation names', 'P7-113',
                 dict(reader='Notes', writer='CreditDeptNotes', supplied_DDL='CreditDeptNotes', deployed_alias='unknown'),
                 dict(local_relation_names_match=False), dict(local_relation_names_match=True), True,
                 ev((S,351,359),(S,558,566),(D,670,709),(RS,1366,1387)))
    illustration('An externally verified compatible alias would be a separate conditional contract', 'P7-113;H7B10-02',
                 dict(hypothetical_alias_maps_to_writer=True, actually_observed_in_deployment=False, SQL_not_executed=True),
                 dict(local_name_difference=True, runtime_failure_necessarily_proven=False),
                 dict(local_name_difference=True, runtime_failure_necessarily_proven=False), False,
                 ev((S,351,398),(D,670,709)))
    illustration('Invoice branch filtering does not filter receipt rows', 'P2-010',
                 dict(current_branch=1, invoice_branches=[1,2], receipt_branches=[1,2], same_salesman=7),
                 dict(invoice_branches=[1], receipt_branches=[1,2]),
                 dict(invoice_branches=[1], receipt_branches=[1]), True,
                 ev((S,189,208),(S,411,439),(RS,1512,1532)))
    end = datetime(2026,1,2)
    illustration('An inclusive next-midnight endpoint includes a following-day row', 'P3-023',
                 dict(selected_end='2026-01-01', row=end.isoformat(), typed_parameters=True),
                 dict(included=end<=end), dict(included=end<end), True,
                 ev((S,189,218),(S,420,436)))
    illustration('Base-unit cost times entered pack quantity understates the dimensional reference', 'P7-041',
                 dict(entered_quantity=2, equality=12, base_unit_cost=5, cost_contract_assumed_for_fixture=True),
                 dict(total_cost=2*5), dict(total_cost=2*12*5), True,
                 ev((P,270,287),(IO,1593,1612),(IO,4301,4316),(IT,196,211),(IT,1390,1404)))
    illustration('Unit equality one is counterevidence to always-different unit cost totals', 'P7-041',
                 dict(entered_quantity=2, equality=1, base_unit_cost=5),
                 dict(total_cost=10), dict(total_cost=10), False,
                 ev((P,270,287),(IO,1593,1612)))
    illustration('Live print dates can label previously captured rows', 'P7-045',
                 dict(result_period='A', controls_now='B', reload_performed=False),
                 dict(rows_period='A', print_header_period='B'),
                 dict(rows_period='A', print_header_period='A'), True,
                 ev((S,149,174),(S,649,681),(S,824,830)))
    illustration('A swallowed late-source error is not an empty successful source', 'P7-046',
                 dict(invoice_rows=[100], receipt5_rows=[50], receipt7_failed=True, not_a_SQL_failure_injection=True),
                 dict(published_total=150, source_health='unlabelled'),
                 dict(published_total=150, source_health='explicit-partial-or-blocked'), True,
                 ev((S,158,174),(S,411,475)))
    illustration('The upstream worker control-read gate must remain visible', 'P7-054',
                 dict(hand_selected_event_sequence=['Task.Run','read-chkAll','catch'], WPF_not_run=True),
                 dict(request_from_ui_snapshot=False, downstream_population_established=False),
                 dict(request_from_ui_snapshot=True, downstream_population_established=False), True,
                 ev((S,141,201),(S,411,436)))
    rows = [dict(gid='A-7', local=7, branch=1), dict(gid='B-7', local=7, branch=2)]
    selected = rows[1]
    illustration('A local-number route can select the wrong first global identity', 'P7-061',
                 dict(rows=rows, selected=selected, first_row_order_is_only_fixture=True),
                 dict(open_gid=rows[0]['gid']), dict(open_gid=selected['gid']), True,
                 ev((SR,10,24),(S,517,570),(SI,473,520),(SQ,624,660),(QD,618,651),(RS,1012,1017)))
    illustration('A VAT-free receipt115 is not a tax-inclusive115 invoice', 'P7-069',
                 dict(Payment=115, VAT=0, NetVal=115),
                 dict(display_value=round(115*100/115,2)), dict(display_value=115), True,
                 ev((S,450,469),(SQ,891,916),(QD,928,944)))
    illustration('Editing text without resolving a new item keeps a prior selected id', 'P7-085',
                 dict(prior_selected_id=1, text_now='B', Enter_pressed=False, item_B_id=2),
                 dict(queried_id=1, visible_text='B'), dict(queried_id=2, visible_text='B'), True,
                 ev((P,132,148),(P,604,623),(P,674,710),(PX,321,341)))
    illustration('A current VAT-inclusion setting can reinterpret a saved excluded-price invoice', 'P7-095',
                 dict(saved_price_includes_vat=False, current_setting_includes_vat=True, line_total=100, tax=15),
                 dict(base=100-15), dict(base=100), True,
                 ev((S,120,131),(S,249,273),(IO,1557,1564),(RS,986,994)))
    illustration('A visible POS row has no matching route in the current string switch', 'P1-033',
                 dict(process_label='فاتورة نقطة بيع', row_action_visible=True),
                 dict(route='no-matching-case'), dict(route='typed-POS-route-or-explicit-unavailable'), True,
                 ev((S,279,290),(S,517,570),(SX,495,510)))
    raw = '"1","CODE","A"Q", "1.00","5.00","10.00","5.00","100%"'
    parsed = next(csv.reader(io.StringIO(raw)))
    illustration('Quoted CSV needs quote escaping even when an embedded comma is quoted', 'P7-048;H7B10-04',
                 dict(manually_constructed_line=raw, original_label='A"Q', formula_interpreter_used=False),
                 dict(label_round_trips=parsed[2]=='A"Q'), dict(label_round_trips=True), True,
                 ev((P,561,584)))
    illustration('Typed XLSX and helper finalization are counterevidence to copying CSV/finalization claims', 'H7B10-04',
                 dict(hand_selected_events=['typed-cell-assignment','SaveAs','helper-using-dispose','return','launch'],
                      actual_export_or_shell_executed=False, library_formula_policy_not_certified=True),
                 dict(format='XLSX', amount_kind='numeric', finalization_before_launch=True),
                 dict(format='XLSX', amount_kind='numeric', finalization_before_launch=True), False,
                 ev((S,694,714),(S,720,739),(S,751,770),(S,807,811)))

    literal('Return/note signs exist, value total ignores them while commissions honor them', 'P7-111',
            [(S,279,290),(S,325,343),(S,381,398),(S,482,510),(S,781,796),(SR,10,24)],
            lambda t: 'isPlus = -1' in t[0] and 'IsPlus = isPlus' in t[1] and 'IsPlus = -1' in t[2]
            and 'sumVal += row.Value;' in t[3] and 'sumComm -= row.SalesComm;' in t[3]
            and 'items.Sum(x => x.Value)' in t[4] and 'IsPlus' in t[5],
            'The local amount total is unsigned, not proof of financial settlement or an actual exported workbook; upstream WPF gate remains.')
    literal('All-period only suppresses the invoice date predicate; receipt calls always bind dates', 'P7-112',
            [(S,56,64),(S,158,166),(S,181,218),(S,401,439),(S,824,830),(SX,282,309)],
            lambda t: 'DateTime.Today' in t[0] and 'LoadClientReceiptVouchers();' in t[1]
            and 'chkAllPeriod.IsChecked != true' in t[2] and 'periodFilter' in t[2]
            and 'ReceiptDate >= @date1' in t[3] and 'ReceiptDate <= @date2' in t[3]
            and 'chkAllPeriod' not in t[3] and 'IsEnabled = !isChecked' in t[4]
            and 'x:Name="chkAllPeriod"' in t[5],
            'This is a within-request source population split, distinct from the inclusive endpoint and post-display criteria drift.')
    literal('Notes reader/route differ from CreditDeptNotes writer and selected supplied DDL', 'P7-113',
            [(S,351,359),(S,391,398),(S,558,566),(D,670,709),(RS,1366,1387)],
            lambda t: 'FROM Notes WHERE' in t[0] and 'catch { /* تجاهل */ }' in t[1]
            and 'FROM Notes WHERE' in t[2] and 'INSERT INTO CreditDeptNotes' in t[3]
            and 'UPDATE CreditDeptNotes' in t[3] and 'CREATE TABLE [dbo].[CreditDeptNotes]' in t[4],
            'Confirmed LOCAL name mismatch only: no assertion that a deployed compatibility view/synonym is absent, and no SQL executed.')
    literal('Task.Run encloses readers with direct WPF dependency-property access', 'P7-054',
            [(S,141,201),(S,228,243),(S,411,436)],
            lambda t: 'await Task.Run(() =>' in t[0] and 'ShowInvoiceResults();' in t[0]
            and 'if (chkAll.IsChecked != true && cmbEmps.SelectedValue != null)' in t[0]
            and '_empName = chkAll.IsChecked == true' in t[1]
            and 'if (chkAll.IsChecked != true && cmbEmps.SelectedValue != null)' in t[2],
            'Dispatcher-wrapped date reads/row additions do not wrap these reads. This upstream gate must not be assumed fixed to claim downstream runtime occurrence.')
    literal('Typed dates still have an inclusive next-day endpoint', 'P3-023',
            [(S,189,218),(S,420,436)],
            lambda t: 'date<=@date2' in t[0] and 'AddHours(24)' in t[0]
            and 'ReceiptDate <= @date2' in t[1] and 'AddHours(24)' in t[1]
            and 'SqlDbType.DateTime' in t[1],
            'Typing and interval closure are independent; no SQL culture/date/timezone acceptance executed.')
    literal('Invoice BranchNo predicate has no corresponding receipt branch predicate', 'P2-010',
            [(S,189,208),(S,411,439),(RS,1512,1532)],
            lambda t: 'inv.branch={MainClass.BranchNo}' in t[0]
            and 'Branch' not in t[1] and '[BranchID] [int]' in t[2] and '[GlobalID] ASC' in t[2],
            'Local predicate gap does not prove global absence of external row-level/session authorization.')
    literal('Receipt115 conversion conflicts with the selected VAT0 writer contracts', 'P7-069',
            [(S,450,469),(SQ,891,916),(QD,928,944)],
            lambda t: 'netVal * 100.0 / 115.0' in t[0] and '@Payment,0,@Payment' in t[1]
            and 'VAT = 0.0' in t[2] and 'NetVal = Convert.ToDouble(txtVal.Text)' in t[2],
            'The report base uses a fixed divisor; commission base and possible invoice/receipt double counting require policy, not a new defect per percentage expression.')
    literal('Salesman report reads current type2 VAT inclusion, ignoring the saved invoice flag', 'P7-095',
            [(S,120,131),(S,249,273),(IO,1557,1564),(RS,986,994)],
            lambda t: 'SettingGeneral WHERE Inv_Id=2' in t[0] and 'table2.Rows[0]["PriceIncVAT"]' in t[0]
            and 'if (_priceIncVAT) netVal -= taxVal;' in t[1] and 'row["PriceIncVAT"]' not in t[1]
            and '"@PriceIncVAT"' in t[2] and 'PriceIncVAT [bit]' in t[3],
            'The saved header flag exists in the local writer/schema. A current setting is not a historical tax-policy certificate.')
    literal('Profit cost expression uses val1 while writer/binder retain base quantity and per-base cost', 'P7-041',
            [(P,270,287),(IO,1593,1612),(IO,4301,4316),(IT,196,211),(IT,1390,1404)],
            lambda t: 'SUM(val1 * AvrgCost) AS TotalCost' in t[0]
            and '"@val", SqlDbType.Float).Value = invoiceItem.ItemPrimaryQnty' in t[1]
            and '"@val1", SqlDbType.Float).Value = invoiceItem.ItemQuantity' in t[1]
            and '"@AvrgCost", SqlDbType.Float).Value = invoiceItem.ItemCost' in t[1]
            and 'new decimal(invoiceItem.ItemPrimaryQnty)' in t[2] and '/ val, 2)' in t[3]
            and 'item.ItemQuantity * item.UnitEquality' in t[4],
            'Dimensional root P7-041 is extended, not renumbered. Cost policy/source P4-006 and misleading cost label P7-039 are separate existing roots.')
    literal('Editable item text has KeyDown resolution but Show uses the retained SelectedId', 'P7-085',
            [(P,132,148),(P,604,623),(P,674,710),(PX,321,341)],
            lambda t: 'Items.id={SelectedId}' in t[0] and 'string.IsNullOrWhiteSpace(txtItemName.Text)' in t[1]
            and 'KeyDown' in t[3] and 'TextChanged' not in t[3] and 'SearchByName();' in t[2]
            and 'SearchByCode();' in t[2],
            'Editing without Enter can leave a stale identity; same prior root as profit-details, no new finding for a copied handler.')
    literal('Report dates are read live while rows remain the stored collection', 'P7-045',
            [(S,149,174),(S,649,681),(S,824,830)],
            lambda t: '_itemsList.Clear();' in t[0] and 'foreach (var row in _itemsList)' in t[1]
            and 'FromDate = txtDateFrom.SelectedDate?' in t[1] and 'ToDate = txtDateTo.SelectedDate?' in t[1]
            and '_itemsList.Clear' not in t[2] and 'txtDateFrom.IsEnabled' in t[2],
            'Source-query criteria and printed criteria are not a frozen snapshot; the external template is not available to certify the final paper.')
    literal('Late-source catches/zero helpers do not produce explicit source health', 'P7-046',
            [(S,158,174),(S,391,398),(S,470,475),(P,294,312),(T,185,199)],
            lambda t: 'RecalculateSummary();' in t[0] and 'catch { /* تجاهل */ }' in t[1]
            and 'catch { /* تجاهل */ }' in t[2] and 'return (0, 0, 0, 0, 0, 0);' in t[3]
            and 'return (0.0, 0.0);' in t[4],
            'Failure-as-zero/partial publication extends the historical failure-state root; no live database fault injection and no automatic P7-107 claim.')
    literal('Salesman DTO drops global keys; selected child readers take the first result row', 'P7-061',
            [(SR,10,24),(S,517,570),(SI,496,520),(SQ,644,660),(QD,635,651)],
            lambda t: 'InvoiceNo' in t[0] and 'GlobalID' not in t[0]
            and 'ReceiptNo={row.InvoiceNo}' in t[1] and 'id={row.InvoiceNo}' in t[1]
            and 'GlobalID=' not in t[1] and 'dr.Read();' in t[2]
            and 'reader.Read();' in t[3] and 'reader.Read();' in t[4],
            'Global identity acquisition inside a child does not repair selection of the wrong first row. The fixture is conditional on matching local numbers, not a deployed collision observation.')
    literal('Two POS labels are produced but neither is a case in the visible row action', 'P1-033',
            [(S,279,290),(S,517,570),(SX,495,510)],
            lambda t: 'processType = "فاتورة نقطة بيع"' in t[0]
            and 'processType = "فاتورة مرتجع نقطة بيع"' in t[0]
            and 'case "فاتورة نقطة بيع"' not in t[1] and 'case "فاتورة مرتجع نقطة بيع"' not in t[1]
            and 'Click="ViewInvoiceBtn_Click"' in t[2],
            'The missing POS route is an extension under functional incompleteness, not proof that the report print renderer or all row actions are empty.')
    literal('These report print paths really load REPX and call print/preview', 'P1-004;H7B10-04',
            [(S,581,655),(P,470,539),(T,359,435)],
            lambda t: all('XtraReport.FromFile' in x and 'ShowPreviewDialog' in x and '.Print()' in x for x in t)
            and all('MainClass.ReportsPath' in x and 'MainClass.ReportsPrinter' in x for x in t),
            'Unlike the prior SummaryQ stub, all three have renderer calls. Deployed templates, effective settings/copies/flags and output consumers remain unresolved, not globally absent.')
    literal('New-window entries differ in local Apply; one disabled menu is counterevidence', 'P1-013;H7B10-05',
            [(HM,3542,3544),(HM,3604,3611),(HX,482,490),(SM,269,280),(P,652,665),(MC,418,455)],
            lambda t: 'ApplyPermissionToForm' not in t[0] and 'ApplyPermissionToForm' in t[1]
            and 'StripSalesInPeriod' in t[2] and 'IsEnabled="False"' in t[2]
            and 'ApplyPermissionToForm' not in t[3] and 'ApplyPermissionToForm(dlg)' in t[4]
            and 'name == "btnPrint"' in t[5],
            'Potential remains potential: no deployed role/server bypass or blanket absence of permission from an isolated caller slice. New instances do not extend static/Close by themselves.')
    literal('B1 roots remain and the deferred-payment binding actually matches its DTO', 'H7B10-03;P7-038;P7-039;P7-040;P7-042',
            [(P,203,250),(T,119,150),(T,238,268),(T,325,355),(TX,441,443),(TR,17,32)],
            lambda t: 'r3.discount * 2' in t[0] and 'DgvAvgCost     = salesTotalCost' in t[0]
            and 'if (qty == 0.0) continue;' in t[1] and 'IsPostpone  = isPostpone' in t[2]
            and 'SumSell      = txtSumSale.Text' in t[3] and 'Binding IsPostpone' in t[4]
            and 'IsPostpone' in t[5],
            'Rechecks are not new findings, and IsPostpone is not a fabricated spelling mismatch. Different tab grains/taxes/discounts require reconciliation, not forced equal totals.')
    literal('Profit detail handoff carries an item id, not the parent date/safe criteria', 'H7B10-03',
            [(P,652,665),(ID,25,55),(ID,74,101),(IDX,1,16)],
            lambda t: 'dlg.SelectedId = itemId;' in t[0] and 'dlg.ShowDialog();' in t[0]
            and 'Date' not in t[0] and 'public int SelectedId' in t[1]
            and 'ShowResults();' in t[1] and 'Inv_Sub.ItemId={SelectedId}' in t[2]
            and '@date' not in t[2] and 'Loaded="frmInvoiceDetails_Load"' in t[3],
            'A deliberate all-history drilldown may be valid; its scope must be stated. Selected child ranges are not whole-child, authorization or financial certification.')
    literal('ClosedXML writes typed XLSX cells and helper using finalizes before caller launch', 'H7B10-04',
            [(S,694,714),(S,720,739),(S,751,770),(S,807,811)],
            lambda t: 'Excel Files (*.xlsx)|*.xlsx' in t[0] and 'ExportToExcelClosedXml(' in t[0]
            and t[0].index('ExportToExcelClosedXml(') < t[0].index('Process.Start(')
            and 'using var workbook = new ClosedXML.Excel.XLWorkbook();' in t[1]
            and '.Value = row.SalesManName;' in t[2] and '.Value = row.Value;' in t[2]
            and 'workbook.SaveAs(filePath);' in t[3],
            'The caller invokes shell only after the helper returns/disposes; no P7-108 extension. Typed .Value assignments are not CSV syntax, nor a certification of every library/consumer formula policy.')
    literal('Known CSV paths use csv extensions and unescaped quoted text, not fake XLSX', 'P7-048;P7-049;H7B10-04',
            [(P,546,591),(T,437,491)],
            lambda t: '.csv' in t[0] and 'StreamWriter' in t[0] and '{r.DgvItem}' in t[0]
            and 'Replace(' not in t[0] and 'CSV Files (*.csv)|*.csv' in t[1]
            and '{r.ItemName}' in t[1] and 'UseShellExecute = true' in t[1],
            'Historical CSV escaping/consumer roots remain, not new extensions from rereading identical B1 ranges. No Office/formula/shell/actual export run; no P7-050 extension for matching CSV extension/content.')
    assert len(ILL) == len(ST) == 20
    print(json.dumps(dict(
        phase='7B10-partial-static-audit',
        method='independent manual contrasts plus bounded inert-source observations, not ERP tests',
        illustration_count=len(ILL), static_lexical_contract_check_count=len(ST),
        illustrations=ILL, static_lexical_contract_checks=ST,
        bounded_source_reads_not_semantic_coverage=[READS[k] for k in sorted(READS)],
        application_code_imported_or_executed=False, application_remediation_performed=False,
        real_business_or_secret_data_used=False, spreadsheet_or_formula_interpreter_executed=False,
        upstream_thread_gate_not_assumed_resolved=True, notes_compatibility_not_assumed_in_deployment=True,
        erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0, errors=[],
    ), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
