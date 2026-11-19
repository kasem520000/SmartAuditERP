#!/usr/bin/env python3
"""Read-only 7B22/R4f documentary witnesses; NEVER ERP or business tests.

Only bounded UTF-8 source text and explicitly supplied Python/Decimal models.
No C#/VB/.NET/WPF/SQL/SDK/Excel/scanner/printer/provider execution, imports,
remediation, operational measurement or acceptance. Token discovery is not a
semantic callgraph/capability census. Stable query outcomes are assumptions,
not observed DB transactions; a method named legacy is not unsupported proof.
"""
from __future__ import annotations

import copy
import csv
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

from check_amountword_contract_witnesses import mask_noncode, qualified_calls

ROOT = Path(__file__).resolve().parents[3]
C = 'SmartAuditERP/Class/'
F = 'SmartAuditERP/Form_WPF/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def supplied_price_projection(unit, equality, loaded_price, price_row_unit,
                              customer_scalar, override):
    """No pricing enum or policy: scalar and override outcome are supplied.

    The conditional reference assumes a DECLARED linear ratio, not ERP policy.
    The identity mismatch itself does not require approving that reference.
    """
    if type(override) is not bool or not all(isinstance(x, str) for x in
            (unit, equality, loaded_price, price_row_unit, customer_scalar)):
        raise ValueError('Supplied strings and exact boolean required')
    eq, before, scalar = map(Decimal, (equality, loaded_price, customer_scalar))
    if not all(x.is_finite() for x in (eq, before, scalar)) or eq <= 0:
        raise ValueError('Finite supplied amounts and positive illustrative ratio required')
    after = scalar if override else before
    return dict(line_unit_before=unit, line_unit_after=unit,
                supplied_price_row_unit=price_row_unit,
                unit_equality_after=str(eq), loaded_unit_price=str(before),
                projected_line_price=str(after), override_supplied=override,
                crossed_unit_without_conversion=override and unit != price_row_unit,
                hypothetical_linear_reference_only=str(scalar * eq),
                actual_pricing_policy_not_supplied=True)


def supplied_dialog_transition(action, quantity='4'):
    """Model the visible consumer switch only, not a WPF dialog invocation."""
    if type(action) is not int or action not in (0, 1, 2, 3):
        raise ValueError('Supplied source-local action 0/1/2/3 required')
    q = Decimal(quantity)
    if not q.is_finite():
        raise ValueError('Finite illustrative quantity required')
    return dict(source_local_action=action,
                existing_quantity_after=str(q + 1 if action == 1 else q),
                rows_after=2 if action == 2 else 1,
                consumer_effect={0: 'return-no-insertion', 1: 'increment-existing-and-return',
                                 2: 'break-then-build-new-row', 3: 'return-no-insertion'}[action],
                wpf_or_new_row_loading_executed=False)


def supplied_import_projection(lines, imported, loader_action):
    """Inert model of repeat action then code+LAST-index update.

    The action/result is supplied. No file/Excel/SQL/importer/DTO is executed;
    labels/policy do not decide the synthetic result. Imported strings are inert.
    """
    if type(loader_action) is not int or loader_action not in (0, 1, 2, 3):
        raise ValueError('Supplied local repeat action required')
    if not isinstance(lines, list) or not lines or not isinstance(imported, dict):
        raise ValueError('Nonempty supplied rows and inert imported row required')
    result = copy.deepcopy(lines)
    required = {'code', 'index', 'quantity', 'price', 'description'}
    if any(set(r) != required or type(r['index']) is not int for r in result):
        raise ValueError('Exact illustrative line shape required')
    if set(imported) != {'code', 'quantity', 'price', 'description'}:
        raise ValueError('Exact imported shape required')
    for r in result:
        if r['code'] == imported['code']:
            if loader_action == 1:
                r['quantity'] = str(Decimal(r['quantity']) + 1)
            elif loader_action == 2:
                result.append(dict(code=imported['code'], index=len(result)+1,
                                   quantity='1', price='10', description=''))
            break
    touched = []
    for r in result:
        if r['code'] != imported['code'] or r['index'] != len(result):
            continue
        r['description'] = imported['description']
        r['quantity'] = str(Decimal(imported['quantity']))
        if Decimal(imported['price']) > 0:
            r['price'] = str(Decimal(imported['price']))
        touched.append(r['index'])
    return dict(lines=result, import_projection_touched_indices=touched,
                imported_values_supplied_not_business_policy=True,
                success_message_after_loop_unconditional_in_model=True,
                real_result_or_cancellation_contract_not_executed=True)


def supplied_stable_entry_guard(validated_existing_code, later_code_query_matches):
    if type(validated_existing_code) is not bool or type(later_code_query_matches) is not bool:
        raise ValueError('Exact supplied outcome booleans required')
    return dict(import_row_emitted=validated_existing_code,
                direct_id_branch=validated_existing_code and later_code_query_matches,
                barcode_fallback=validated_existing_code and not later_code_query_matches,
                database_stability_not_observed=True,
                raw_method_fallback_is_not_a_scanner_entry_contract=True)


def main():
    reads, models, checks, errors = [], [], [], []

    def read(path, start, end):
        # Selected files are strict UTF-8 here. Do not silently certify other encodings.
        lines = (ROOT/path).read_bytes().decode('utf-8-sig').splitlines(keepends=True)
        if not 1 <= start <= end <= len(lines):
            raise ValueError('Out-of-bounds documentary read: '+path)
        text = ''.join(lines[start-1:end])
        reads.append(dict(path=path, start=start, end=end,
                          sha256=digest(text.encode()),
                          purpose='bounded-inert-text-not-body-coverage-or-runtime'))
        return text

    # Whole METHODS below only as bounded slices, never whole-file/whole-feature claims.
    legacy_decode = read(C+'ItemOpercontract.cs', 1808, 1916)
    contract_entry = read(F+'frmcontract.xaml.cs', 1747, 1810)
    importer = read(F+'frmImportDataGeneral.xaml.cs', 996, 1057)
    existence = read(F+'frmImportDataGeneral.xaml.cs', 1188, 1199)
    import_consumer = read(F+'frmcontract.xaml.cs', 2500, 2550)
    import_wiring = read(F+'frmcontract.xaml.cs', 163, 206)
    menu = read(F+'frmcontract.xaml', 1001, 1022)
    dialog = read(F+'MsgExistItem.xaml.cs', 1, 57)
    dialog_xaml = read(F+'MsgExistItem.xaml', 59, 134)
    legacy_load = read(C+'ItemOpercontract.cs', 977, 1084)
    duplicate_load = read(C+'ItemOpercontract.cs', 1086, 1193)
    main_load = read(C+'ItemOper.cs', 1035, 1185)
    legacy_customer = read(C+'ItemOpercontract.cs', 1331, 1366)
    main_customer = read(C+'ItemOper.cs', 983, 1030)
    legacy_unit = read(C+'ItemOpercontract.cs', 1481, 1579)
    main_unit = read(C+'ItemOper.cs', 733, 811)
    writer = read(F+'frmItems.xaml.cs', 1022, 1083)
    schema = read('SmartAuditERP/Properties/Resources.resx', 1086, 1103)
    legacy_order = read(C+'ItemOpercontract.cs', 1195, 1211)
    main_order = read(C+'ItemOper.cs', 495, 521)
    main_decode = read(C+'ItemOper.cs', 1908, 2091)
    read(F+'frmItems.xaml.cs', 905, 925)
    read(F+'frmItems.xaml.cs', 972, 990)
    read(F+'frmItems.xaml', 497, 505)
    read(F+'frmImportDataGeneral.xaml.cs', 370, 382)
    read(F+'frmImportDataGeneral.xaml.cs', 429, 442)
    read(F+'frmImportDataGeneral.xaml', 439, 452)
    read(F+'frmImportDataGeneral.xaml', 601, 609)
    read(F+'frmcontract.xaml.cs', 76, 95)
    read(F+'frmcontract.xaml.cs', 555, 619)
    read(F+'frmcontract.xaml', 636, 680)

    def model(title, ids, evidence, value, assertion, limit):
        row = dict(id=f'ALG7B22-{len(models)+1:02d}', title=title,
                   finding_ids=ids, evidence=evidence, supplied_result=value,
                   illustration_assertions_passed=bool(assertion),
                   source_application_executed=False, limit=limit)
        models.append(row)
        if not assertion:
            errors.append('Documentary model assertion: '+row['id'])

    p = supplied_price_projection('PACK', '12', '120', 'EACH', '8', True)
    model('Foreign-unit customer scalar replaces selected unit quote', 'P7-142',
          C+'ItemOpercontract.cs:1195-1211;1331-1366;1481-1527;'+F+'frmItems.xaml.cs:1022-1083',
          p, p['projected_line_price']=='8' and p['line_unit_after']=='PACK' and p['crossed_unit_without_conversion'],
          'Supplied pack/base quote and ratio;96 is a hypothetical declared linear reference, not an approved discount, conversion or tax policy. No actual DB/.NET/SDK pricing.')
    modes = {str(n): supplied_price_projection('PACK','12','120','EACH','8',True)
             for n in (1,2,5,6,7)}
    model('Five explicit source-local scalar branches share the unitless projection', 'P7-142',
          C+'ItemOper.cs:983-1030;'+C+'ItemOpercontract.cs:1331-1366',
          modes, all(x['projected_line_price']=='8' for x in modes.values()),
          'Numbers are visible switch cases only, not an AuditorAPI Pricing enum or a requirement that all customers use these modes. Recent-cost cases3/4 are outside this scalar proof.')
    p = supplied_price_projection('EACH','1','10','EACH','8',True)
    model('Same-unit control does not cross unit identity', 'P7-142', C+'ItemOpercontract.cs:1331-1366',
          p, not p['crossed_unit_without_conversion'] and p['projected_line_price']=='8',
          'Same-unit counterexample limits the cause; no business price approval or real customer observed.')
    p = supplied_price_projection('PACK','12','120','EACH','8',False)
    model('No-customer-override supplied outcome preserves unit quote', 'P7-142', C+'ItemOper.cs:983-1030',
          p, p['projected_line_price']=='120' and not p['crossed_unit_without_conversion'],
          'Supplied early-return/nonmatching pricing outcome only. Does not fix P4-026 or accept its pricing resolver.')
    p = supplied_dialog_transition(2)
    model('Visible add-quantity button emits2 but consumer starts a new row', 'P7-143',
          F+'MsgExistItem.xaml:59-134;'+F+'MsgExistItem.xaml.cs:34-53;'+C+'ItemOpercontract.cs:1000-1084',
          p, p['rows_after']==2 and p['existing_quantity_after']=='4',
          'Conditional on reaching repeat dialog and normal completion of new-row load. Total quantity may still be5; mismatch is chosen row action, not a claim of doubled financial quantity or WPF execution.')
    p = supplied_dialog_transition(1)
    model('Visible new-line button emits1 but consumer increments old row', 'P7-143',
          F+'MsgExistItem.xaml:59-134;'+F+'MsgExistItem.xaml.cs:34-53;'+C+'ItemOper.cs:1091-1154',
          p, p['rows_after']==1 and p['existing_quantity_after']=='5',
          'No presumed policy about merging different units/discounts/serials, no persisted item or render observed; label, emitted code and selected consumer disagree locally.')
    p = {str(n): supplied_dialog_transition(n) for n in (0,3)}
    model('Do-not-insert and initial-close controls do not mutate the loader row', 'P7-143',
          F+'MsgExistItem.xaml.cs:9-18;34-53;'+C+'ItemOpercontract.cs:1025-1035',
          p, all(x['existing_quantity_after']=='4' and x['rows_after']==1 for x in p.values()),
          'Loader-level control only; importer can still mutate last matching row afterward, a separate P7-144 boundary. No modal close/Hide lifecycle behavior is executed or accepted.')
    a = dict(code='A',index=1,quantity='1',price='10',description='old-A')
    b = dict(code='B',index=2,quantity='2',price='20',description='old-B')
    incoming = dict(code='A',quantity='7',price='50',description='import-A')
    p = supplied_import_projection([a,b], incoming, 1)
    model('Merged nonlast line is not targeted by import code+Count predicate', 'P7-144',
          F+'frmcontract.xaml.cs:1747-1762;2500-2550;'+C+'ItemOpercontract.cs:1025-1035',
          p, p['import_projection_touched_indices']==[] and p['lines'][0]['quantity']=='2' and p['lines'][0]['price']=='10',
          'Supplied Action1 outcome models increment1 then failed last-index match. Even with dialog labels corrected the importer still lacks a resolved line/result. Duplicate merge quantity policy is not invented; success text is source-local, not a saved import.')
    last_a = dict(a,index=2)
    first_b = dict(b,index=1)
    p = supplied_import_projection([first_b,last_a], incoming, 1)
    model('Same-code last row is a control where import values do get assigned', 'P7-144',
          F+'frmcontract.xaml.cs:2524-2543', p,
          p['import_projection_touched_indices']==[2] and p['lines'][-1]['quantity']=='7' and p['lines'][-1]['price']=='50',
          'Control limits the nonlast-row cause. Replacement versus addition is an owner decision; this is not acceptance of the importer or a prescribed duplicate policy.')
    p = supplied_import_projection([first_b,last_a], incoming, 3)
    model('Do-not-insert result still reaches blind update of matching last row', 'P7-144',
          F+'MsgExistItem.xaml:127-134;'+F+'MsgExistItem.xaml.cs:48-53;'+C+'ItemOpercontract.cs:1025-1035;'+F+'frmcontract.xaml.cs:1747-1762;2524-2543',
          p, p['lines'][-1]['quantity']=='7' and p['lines'][-1]['description']=='import-A' and p['import_projection_touched_indices']==[2],
          'Independent of the reversed1/2 label mapping: source-local Action3 means no insertion in loader. Caller has no typed cancellation result and mutates existing line; no actual click/import/save/DB rollback observed.')
    p = supplied_stable_entry_guard(True,True)
    model('Stable accepted import-code guard shadows the barcode fallback', 'H7B22-03',
          F+'frmImportDataGeneral.xaml.cs:1026-1048;1188-1199;'+F+'frmcontract.xaml.cs:1764-1810;2520-2522',
          p, p['direct_id_branch'] and not p['barcode_fallback'],
          'Two matching query outcomes supplied; no snapshot/atomicity or actual scanner reachability proof. Concurrent master edits/other callers/external/reflection/alias entry remain unresolved; not dead code or unsupported status.')
    p = dict(legacy_explicit_weight_modes=[1,2],main_explicit_weight_modes=[1,2,3],
             legacy_assigns_identity_for_mode3=False,mode3_support_policy_not_supplied=True)
    model('Legacy mode3 omission is a compatibility question, not a new defect', 'H7B22-03',
          C+'ItemOpercontract.cs:1849-1916;'+C+'ItemOper.cs:1962-2051;'+F+'frmItems.xaml.cs:905-925',
          p, 'wscale == 3' not in legacy_decode and 'wscale == 3' in main_decode,
          'Exact lookup precedes scale in both readers. No enum, checksum, scanner format or required mode3 support inferred. Same136/137/138 causes are compared, not extended or re-counted.')

    def observe(title, ids, evidence, observed, limit):
        row = dict(id=f'ST7B22-{len(checks)+1:02d}', title=title, finding_ids=ids,
                   evidence=evidence, documented_text_observation_matches=bool(observed),
                   source_application_executed=False, limit=limit)
        checks.append(row)
        if not observed:
            errors.append('Documentary text observation: '+row['id'])

    observe('Writer records base UnitId and separate ItemUnits prices', 'P7-142',
            F+'frmItems.xaml.cs:1022-1083',
            'u.DgvUnitSalePrice' in writer and 'priceCmd.Parameters.Add("@UnitId"' in writer and 'GetSelectedIntValue(cmbUnit)' in writer,
            'Selected writer only; not every import/cloud/history writer or deployed unique/foreign-key contract.')
    observe('Supplied DDL explicitly contains ItemPrices.UnitID', 'P7-142',
            'SmartAuditERP/Properties/Resources.resx:1086-1103', '[UnitID] [int]' in schema,
            'Embedded text, not executed migration or proof of deployed schema.')
    observe('Legacy customer price projection has item-only query and no unit normalization', 'P7-142',
            C+'ItemOpercontract.cs:1331-1366',
            'FROM ItemPrices WHERE ItemID={NewItem.ItemId}' in legacy_customer and 'UnitID' not in legacy_customer and 'UnitEquality' not in legacy_customer,
            'Whole selected method text checked. Query order/history and pricing cases3/4 are not separate findings here.')
    observe('Main customer price projection repeats item-only unitless scalar assignment', 'P7-142',
            C+'ItemOper.cs:983-1030',
            'FROM ItemPrices WHERE ItemID={newItem.ItemId}' in main_customer and 'UnitID' not in main_customer and 'UnitEquality' not in main_customer,
            'Five shown scalar cases only. Not all pricing functions or an external enum definition.')
    observe('Both load paths place customer override after selected unit loading', 'P7-142',
            C+'ItemOpercontract.cs:1195-1211;'+C+'ItemOper.cs:495-521',
            legacy_order.index('LoadUnitInf(')<legacy_order.index('LoadCustomerPrice(') and main_order.index('LoadUnitInf(')<main_order.index('LoadCustomerPrice('),
            'Conditional on successful lookup and normal method flow; no actual customer rows or load execution.')
    observe('Add quantity/new line XAML labels are wired to explicit handlers', 'P7-143',
            F+'MsgExistItem.xaml:59-134',
            all(t in dialog_xaml for t in ('إضافة الكمية','إدراج في بند جديد','Click="btnAddquantity_Click"','Click="btnNewTirm_Click"')),
            'Not just an inference from method names; still no WPF render or click.')
    observe('Dialog handlers emit2/1/3 and defaults0', 'P7-143',
            F+'MsgExistItem.xaml.cs:1-57',
            all(re.search(p,dialog,re.S) for p in (r'btnAddquantity_Click.*?Action = 2;',r'btnNewTirm_Click.*?Action = 1;',r'btnNon_Click.*?Action = 3;')) and 'public int Action = 0;' in dialog,
            'Integer source protocol only, not a guessed SDK enum or Hide/ShowDialog lifecycle contract.')
    observe('Three selected loaders consume1 as increment and2 as break-to-new', 'P7-143',
            C+'ItemOpercontract.cs:1000-1084;1109-1193;'+C+'ItemOper.cs:1091-1154',
            all(re.search(r'Action == 1.*?ItemQuantity \+= 1(?:\.0)?.*?Action == 2.*?break;',x,re.S) for x in (legacy_load,duplicate_load,main_load)),
            'Selected bodies only; other discovered MsgExistItem consumers are not body-reviewed or silently certified.')
    observe('Contract import command has literal menu and event wiring', 'P7-144',
            F+'frmcontract.xaml:1001-1022;'+F+'frmcontract.xaml.cs:163-206',
            'x:Name="stripImport"' in menu and 'stripImport.Click += stripImport_Click;' in import_wiring,
            'Static wiring conditional on window setup and authorization; not proof of deployed availability or permission.')
    observe('Importer success requires an existing item Code and emits typed column names', 'H7B22-03',
            F+'frmImportDataGeneral.xaml.cs:996-1057;1188-1199',
            'if (!IsItemExist(itemCode))' in importer and 'Code = N\'{code}\'' in existence and 'dtInvSel.Rows.Add(itemCode' in importer,
            'Same SQL intent, no stability or parameterization approval. SQL interpolation remains under P1-011, not a new root.')
    observe('Caller discards loader outcome and updates code plus final index', 'P7-144',
            F+'frmcontract.xaml.cs:1747-1810;2500-2550',
            'private void SearchByID' in contract_entry and 'GetItemByIDcontract(' in contract_entry and 'invItem.ItemRowIndex !=' in import_consumer and 'Invoic.InvoiceItems.Count)' in import_consumer and 'تم الاستيراد بنجاح' in import_consumer,
            'Positive/nonempty import guards exist, but do not bind a resolved line or cancel. No persisted success/commit claim.')
    observe('Legacy barcode outputs are omitted and shared nearest causes remain', 'P7-136;P7-137;P7-138;P4-026',
            C+'ItemOpercontract.cs:1808-1916;1481-1527;'+F+'frmcontract.xaml.cs:1747-1810',
            'ref price, ref qty' in contract_entry and 'ref Invoic, false, barcode, serialNo' in contract_entry and 'ItemQuantity = default;' in legacy_decode and 'Rows[0]' in legacy_decode and 'return;' in legacy_unit,
            'Source-local homologues only, zero old registry extensions/new barcode causes. Stable import guard limits practical reachability; no scan, decode, stock/save or approved support observed.')

    discovered = {'legacy_SearchForBarcode': [], 'legacy_GetItemByIDcontract': []}
    scanned, replacements = 0, []
    with (ROOT/'docs/audit/evidence/inventory.csv').open(encoding='utf-8', newline='') as stream:
        source_paths = sorted(r['path'] for r in csv.DictReader(stream)
                              if r['kind']=='source' and r['path'].endswith('.cs'))
    for relative in source_paths:
        raw = (ROOT/relative).read_bytes()
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            text = raw.decode('utf-8-sig', errors='replace')
            replacements.append(relative)
        scanned += 1
        for key, method, receiver in (
                ('legacy_SearchForBarcode','SearchForBarcode','ItemOpercontract'),
                ('legacy_GetItemByIDcontract','GetItemByIDcontract',
                 r'new\s+ItemOpercontract\s*\(\s*\)')):
            discovered[key] += qualified_calls(text, relative, method=method,
                                                receiver=receiver)
    result = dict(
        source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',
        branch='arena/94ae8414-smartauditerp',
        application_code_imported_or_executed=False,
        dotnet_wpf_sql_or_excel_executed=False,
        erp_runtime_tests_executed=0, sql_or_external_service_tests_executed=0,
        scanner_or_printer_tests_executed=0,
        phase7C_started=False, phase8_authorized_or_started=False,
        B_R4f_bounded_not_whole7B_closure=True,
        unresolved_external_contracts_and_explicit_splits_retained=True,
        retained_additive_B10_arithmetic_erratum=dict(local_cost=10, reference_cost=120,
                                                     equality1_control=10,
                                                     protected_G138_not_rewritten=True),
        illustration_count=len(models), illustrations=models,
        lexical_check_count=len(checks), static_lexical_contract_checks=checks,
        bounded_source_reads_not_semantic_coverage=reads,
        qualified_literal_discovery=dict(
            source_csharp_paths_lexically_scanned=scanned,
            scanned_bodies_not_reviewed=True,
            not_complete_callgraph_or_capability_census=True,
            lexical_utf8_replacement_paths_not_encoding_acceptance=replacements,
            **discovered,
            limit='Only two receiver-qualified names, comments/strings masked; unqualified/alias/reflection/external/delegate and interpolated-expression calls excluded. No semantic source binding, scanner support, dead-code proof or whole-body review.'),
        errors=errors)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
