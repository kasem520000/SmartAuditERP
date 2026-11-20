#!/usr/bin/env python3
"""B33 inert printer-state/argument illustrations, NEVER a printer/PDF test.

Only strings, supplied gate/return flags and lexical source checks are used.
Print.defPrinter is a local auto-property; external InvoiceDGV dirty/mapping
contracts, DevExpress, SQL, templates, installed devices and output outcomes
are not inferred. A normal return is not proof of PDF creation or paper output.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ENTRY = '3f747085b8f91762f7626dd45331ca1f5ba9e9c1'
SC = 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
PC = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs'
SX = 'SmartAuditERP/Form_WPF/frmInvSale.xaml'
PX = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml'
PT = 'SmartAuditERP/Class/Print.cs'
IO = 'SmartAuditERP/Class/InvoiceOper.cs'
PDF = 'Microsoft Print to PDF'
SOURCE_SLICES = (
    (SC, 34, 34), (SC, 65, 78), (SX, 1187, 1191), (SX, 1251, 1259),
    (SC, 3201, 3208), (SC, 2581, 2595), (SC, 2041, 2058),
    (SC, 2059, 2083), (SC, 2084, 2092), (SC, 2093, 2111),
    (SC, 2112, 2124), (PT, 38, 38), (PT, 54, 95),
    (PT, 148, 163), (PT, 164, 189), (PT, 190, 194),
    (PT, 195, 209), (PT, 210, 221), (PC, 1438, 1471), (PC, 1610, 1624),
)
EXPLORATORY_SLICES = (
    (SX, 1206, 1216), (PX, 1411, 1428), (SC, 2888, 2899),
    (SC, 1858, 1935), (SC, 2986, 3035), (SC, 3124, 3199),
    (PT, 110, 146), (IO, 4040, 4131), (SC, 1546, 1606),
)
EVIDENCE = f'{SC}:2041-2124;{SC}:2581-2595;{SC}:3201-3208;{PT}:148-221'
LIMIT = ('سلاسل وأعلام ورجوع حدود موردة صراحة؛لا C#/WPF/SQL/SDK أو قالب أو '
         'طابعة أو PDF أو حفظ أو نتيجة إرسال/خسارة مالية مرصودة.')


def flag(value):
    if type(value) is not bool:
        raise ValueError('Explicit supplied bool required, not a DTO/SDK inference')
    return value


def token(value):
    if type(value) is not str or len(value) > 80 or any(ord(c) < 32 for c in value):
        raise ValueError('Bounded redacted string token required')
    return value


def caller_allows(is_printed, is_updated):
    flag(is_printed)
    flag(is_updated)
    return is_printed and not is_updated


def wrapper(printer, mode, *, rows=1, url=True, report=True, bind_returns=True,
            default_printer='fixture-default'):
    """Boundary only: MappingInvoice has already returned, type fixed by caller.

    report is a supplied combined directory/main-file gate, NOT an REPX load.
    A supplied binding nonreturn occurs after the local property assignment.
    No engine is called by this illustration. The returned argument is a string.
    """
    token(printer)
    token(default_printer)
    if type(mode) is not str or mode not in ('normal', 'pdf'):
        raise ValueError('Only the two selected wrappers')
    if type(rows) is not int or not 0 <= rows <= 1000:
        raise ValueError('Supplied bounded grid count, not invoice-item count')
    for value in (url, report, bind_returns):
        flag(value)
    before = printer
    gate = 'empty-grid' if rows == 0 else ('missing-url' if not url else (
        'missing-main-report' if not report else None))
    reached_assignment = gate is None
    if reached_assignment:
        if mode == 'pdf':
            printer = PDF
        elif not printer:
            printer = default_printer
    engine_entered = reached_assignment and bind_returns
    return dict(mode=mode, shared_before=before, shared_after=printer,
                stopped_before_assignment=gate, assignment_boundary_reached=reached_assignment,
                engine_entered=engine_entered,
                engine_printer_argument=printer if engine_entered else None,
                binding_nonreturn_after_assignment=reached_assignment and not bind_returns,
                engine_or_application_executed=False, actual_output_proved=False)


def engine(printer, *, output_type=1, picker='', template_printer='', copies=1,
           kitchen='', failure='none'):
    """Illustrate local parameter overrides; no mutation of caller's property.

    failure is a supplied point (template or output), not an induced exception.
    Counts are requests in selected branches, never spool jobs or successful
    sheets. Kitchen recursion is a separate boundary, not included in the count.
    """
    for value in (printer, picker, template_printer, kitchen):
        token(value)
    if type(output_type) is not int or output_type not in (1, 2, 3):
        raise ValueError('Selected type1/type2/type3 only')
    if type(copies) is not int or not -2 <= copies <= 20:
        raise ValueError('Bounded supplied copies, not an accepted policy')
    if type(failure) is not str or failure not in ('none', 'template', 'output'):
        raise ValueError('Explicit selected failure boundary')
    local = picker if picker else printer
    assigned = failure != 'template'
    if assigned and output_type == 3 and template_printer:
        local = template_printer
    requests = 0 if not assigned else (copies if output_type == 1 and copies > 0 else (
        0 if output_type == 2 else 1))
    if failure == 'output' and requests:
        requests = 1  # First supplied Print failure prevents the rest of the loop.
    return dict(incoming_argument=printer, local_after_overrides=local,
                report_printer_assignment=local if assigned else None,
                output_type=output_type, selected_branch_print_requests=requests,
                selected_branch_preview_requests=int(assigned and output_type == 2),
                requests_not_successful_or_spooled_copies=True,
                kitchen_recursion_boundary=bool(assigned and failure == 'none' and output_type == 1 and copies > 0 and kitchen),
                failure_point_supplied=failure,
                normal_void_return_proves_output_success=False,
                shared_property_written_by_this_engine=False,
                engine_or_application_executed=False)


def read_slice(path, start, end):
    raw = (ROOT / path).read_bytes()
    lines = raw.decode('utf8').splitlines()
    if not (1 <= start <= end <= len(lines)):
        raise ValueError('Out-of-source slice')
    return '\n'.join(lines[start - 1:end])


def build():
    pdf = read_slice(SC, 2093, 2124)
    normal = read_slice(SC, 2041, 2091)
    call = read_slice(SC, 3201, 3208)
    core = read_slice(PT, 148, 221)
    constructor = read_slice(PT, 54, 95)
    first = wrapper('fixture-paper-A', 'pdf')
    second = wrapper(first['shared_after'], 'normal')
    cases = [
        ('pdf-mutates-shared-local-property', first,
         dict(shared_after=PDF, engine_printer_argument=PDF)),
        ('same-instance-next-normal-reuses-PDF', second,
         dict(shared_after=PDF, engine_printer_argument=PDF)),
        ('normal-without-prior-PDF-control', wrapper('fixture-paper-A', 'normal'),
         dict(shared_after='fixture-paper-A', engine_printer_argument='fixture-paper-A')),
        ('new-independent-instance-control', wrapper('fixture-paper-B', 'normal'),
         dict(shared_after='fixture-paper-B')),
        ('empty-grid-stops-before-PDF-write', wrapper('fixture-paper-A', 'pdf', rows=0),
         dict(shared_after='fixture-paper-A', stopped_before_assignment='empty-grid', engine_entered=False)),
        ('empty-report-url-stops-before-write', wrapper('fixture-paper-A', 'pdf', url=False),
         dict(shared_after='fixture-paper-A', stopped_before_assignment='missing-url')),
        ('missing-main-report-stops-before-write', wrapper('fixture-paper-A', 'pdf', report=False),
         dict(shared_after='fixture-paper-A', stopped_before_assignment='missing-main-report')),
        ('binding-nonreturn-after-PDF-write', wrapper('fixture-paper-A', 'pdf', bind_returns=False),
         dict(shared_after=PDF, engine_entered=False, binding_nonreturn_after_assignment=True)),
        ('empty-normal-printer-fallback', wrapper('', 'normal'),
         dict(shared_after='fixture-default', engine_printer_argument='fixture-default')),
        ('nonempty-normal-printer-is-not-reset', wrapper(PDF, 'normal', default_printer='fixture-paper-A'),
         dict(shared_after=PDF)),
        ('type1-without-picker-or-template-override', engine(PDF, template_printer='fixture-template'),
         dict(report_printer_assignment=PDF, selected_branch_print_requests=1)),
        ('picker-overrides-local-not-property', engine(PDF, picker='fixture-picker'),
         dict(report_printer_assignment='fixture-picker', shared_property_written_by_this_engine=False)),
        ('empty-picker-value-does-not-override', engine(PDF, picker=''),
         dict(report_printer_assignment=PDF)),
        ('type3-template-overrides-picker-locally', engine(PDF, output_type=3, picker='fixture-picker', template_printer='fixture-template'),
         dict(report_printer_assignment='fixture-template')),
        ('type2-preview-is-not-print', engine(PDF, output_type=2),
         dict(selected_branch_print_requests=0, selected_branch_preview_requests=1)),
        ('type3-empty-template-keeps-argument', engine(PDF, output_type=3),
         dict(report_printer_assignment=PDF)),
        ('template-failure-does-not-restore-shared-state', engine(PDF, failure='template'),
         dict(report_printer_assignment=None, shared_property_written_by_this_engine=False)),
        ('output-failure-void-does-not-prove-success', engine(PDF, failure='output'),
         dict(normal_void_return_proves_output_success=False, shared_property_written_by_this_engine=False)),
        ('count-zero-is-old030-not-a-new-root', engine(PDF, copies=0),
         dict(selected_branch_print_requests=1)),
        ('kitchen-is-separate-recursive-boundary', engine(PDF, kitchen='fixture-kitchen'),
         dict(kitchen_recursion_boundary=True, selected_branch_print_requests=1)),
    ]
    illustrations = [dict(
        id=f'ALG7B33-{i:02d}', boundary=name, trace=trace, expected=expected,
        illustration_assertions_passed=all(trace[k] == val and type(trace[k]) is type(val)
                                          for k, val in expected.items()),
        finding_ids='P7-030' if i == 19 else 'P7-163', evidence=EVIDENCE,
        source_application_executed=False, limit=LIMIT,
    ) for i, (name, trace, expected) in enumerate(cases, 1)]
    selected_caller = read_slice(SC, 2581, 2595)
    checks = [
        ('one-instance-field-and-construction', 'private Print print;' in read_slice(SC, 34, 34)
         and 'print = new Print(InvType);' in read_slice(SC, 65, 78), f'{SC}:34-34;{SC}:65-78'),
        ('PDF-menu-wired', 'Click="ExportPDF_Click"' in read_slice(SX, 1187, 1191), f'{SX}:1187-1191'),
        ('normal-and-preview-wired', all(x in read_slice(SX, 1251, 1259) for x in (
            'Click="btnPrint_Click"', 'Click="btnView_Click"')), f'{SX}:1251-1259'),
        ('PDF-caller-flags-and-type1', 'Invoic.IsPrinted && !Invoic.IsUpdated' in call
         and 'MappingInvoice(ref Invoic), 1)' in call, f'{SC}:3201-3208'),
        ('normal-preview-caller-flags-types', selected_caller.count('Invoic.IsPrinted && !Invoic.IsUpdated') == 2
         and 'MappingInvoice(ref Invoic), 1)' in selected_caller and 'MappingInvoice(ref Invoic), 2)' in selected_caller,
         f'{SC}:2581-2595'),
        ('local-auto-property-not-unknown-DTO-setter', 'public string defPrinter { get; set; }' in read_slice(PT, 38, 38), f'{PT}:38-38'),
        ('constructor-default-and-casher-setting', all(x in constructor for x in (
            'this.defPrinter = MainClass.ReportsPrinter;', 'this.defPrinter = Conversions.ToString(dataTable.Rows[0]["CasherPrinter"]);')),
         f'{PT}:54-95'),
        ('PDF-writes-before-binding-call', pdf.index('print.defPrinter = "Microsoft Print to PDF";')
         < pdf.index('print.Printing(type, print.BindToData(inv),'), f'{SC}:2093-2124'),
        ('complete-selected-PDF-wrapper-no-restoration', pdf.count('print.defPrinter =') == 1
         and 'finally' not in pdf and 'try' not in pdf, f'{SC}:2093-2124'),
        ('normal-fallback-only-for-empty-property', 'if (string.IsNullOrEmpty(print.defPrinter))\n                print.defPrinter = MainClass.ReportsPrinter;' in normal,
         f'{SC}:2085-2091'),
        ('PDF-row-url-file-gates-precede-write', all(pdf.index(x) < pdf.index('print.defPrinter =') for x in (
            'GridControl1.Items.Count == 0', 'string.IsNullOrEmpty(print.RptUrl)', '!File.Exists(path)')),
         f'{SC}:2093-2124'),
        ('normal-file-gate-before-engine', normal.index('!File.Exists(path)') < normal.index('print.Printing('), f'{SC}:2041-2091'),
        ('engine-string-parameter-by-value', 'string defPrinter, string kitchenprinter' in core
         and 'ref string defPrinter' not in core and 'out string defPrinter' not in core, f'{PT}:148-162'),
        ('picker-local-override-only-if-nonempty', 'frmPrinter2.SelectedPrinter, "", TextCompare: false) != 0' in core
         and 'defPrinter = frmPrinter2.SelectedPrinter;' in core, f'{PT}:148-162'),
        ('type3-template-local-override', 'if (type == 3 && Operators.CompareString(xtraReport.PrinterName, "", TextCompare: false) != 0)' in core
         and 'defPrinter = xtraReport.PrinterName;' in core, f'{PT}:190-194'),
        ('preview-and-count-controls', all(x in core for x in (
            'if (type == 1 && PrintNo > 0)', 'else if (type == 2)', 'xtraReport.ShowPreviewDialog();')),
         f'{PT}:195-221'),
        ('engine-has-no-write-to-instance-defPrinter', 'this.defPrinter' not in core
         and 'xtraReport.PrinterName = defPrinter;' in core, f'{PT}:148-221'),
        ('void-catch-is-old031-not-success', 'public void Printing(' in core
         and 'catch (Exception projectError)' in core and 'ProjectData.ClearProjectError();' in core,
         f'{PT}:148-221'),
        ('purchase-control-does-not-use-sale-field', 'this.print.defPrinter = MainClass.ReportsPrinter;' in read_slice(PC, 1438, 1471)
         and PDF not in read_slice(PC, 1438, 1471), f'{PC}:1438-1471'),
        ('kitchen-recursive-argument-is-separate', 'this.Printing(type, ds, RptUrl, "rptPOS2.repx", kitchenprinter, "", 1);' in core,
         f'{PT}:195-209'),
    ]
    lexical = [dict(id=f'ST7B33-{i:02d}', boundary=name,
                    documented_text_observation_matches=bool(ok), finding_ids='P7-163',
                    evidence=evidence, source_application_executed=False, limit=LIMIT)
               for i, (name, ok, evidence) in enumerate(checks, 1)]

    def reads(pool, purpose):
        return [dict(path=p, start=a, end=z,
                     sha256=hashlib.sha256((ROOT / p).read_bytes()).hexdigest(),
                     purpose=purpose, whole_local_file_selected=False,
                     whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True)
                for p, a, z in pool]

    errors = [r['id'] for r in illustrations if not r['illustration_assertions_passed']]
    errors += [r['id'] for r in lexical if not r['documented_text_observation_matches']]
    return dict(
        audit_reference_date_utc='2026-11-16', entry_checkout=ENTRY,
        new_root_ids=['P7-163'], extended_existing_root_ids=[],
        illustration_count=20, lexical_check_count=20, selected_source_paths=6,
        selected_contract_slices=20, context_slices_not_certified=9,
        whole_local_files_selected=0,
        gates_and_return_flags_and_printer_tokens_are_supplied=True,
        parameter_overrides_do_not_write_back_local_auto_property=True,
        source_assignment_and_next_request_not_output_success=True,
        unknown_DTO_dirty_mapping_and_SDK_contracts_remain_unknown=True,
        application_code_imported_or_executed=False, dotnet_wpf_sql_or_SDK_executed=False,
        installed_printer_or_PDF_file_or_paper_output_proved=False,
        persisted_setting_write_or_financial_loss_claimed=False,
        all_callers_or_engine_types_certified=False, application_remediation_performed=False,
        phase7C_started=False, phase8_authorized_or_started=False,
        erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0,
        retained_additive_B10_arithmetic_erratum=dict(local_cost=10, reference_cost=120,
            equality1_control=10, protected_G138_not_rewritten=True),
        illustrations=illustrations, static_lexical_contract_checks=lexical,
        bounded_source_reads_not_semantic_coverage=reads(SOURCE_SLICES, 'selected-contract'),
        exploratory_source_reads_not_capability_certification=reads(EXPLORATORY_SLICES, 'context-not-certified'),
        errors=errors,
    )


if __name__ == '__main__':
    output = build()
    print(json.dumps(output, ensure_ascii=False, indent=2))
    raise SystemExit(bool(output['errors']))
