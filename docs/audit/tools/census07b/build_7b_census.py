#!/usr/bin/env python3
"""Build a NEW, exclusive static discovery snapshot. Never execute ERP or SQL.

Optional documentary dependency only (not an application dependency):
  python -m pip install --target /tmp/audit-parser -r docs/audit/tools/census07b/requirements-census-07B38.txt
  PYTHONPATH=/tmp/audit-parser python -B docs/audit/tools/census07b/build_7b_census.py --output <new-path.json>

Parsing is syntax discovery, NOT compilation, binding, a semantic call graph,
a source review, a complete capability denominator, or a closure decision.
Only inventory-kind source C#/XAML is parsed. Argument/literal contents are not
copied to the snapshot. XML attributes record possible entry names, not WPF
registration, event ordering, reachability, or authorization. No assemblies,
BAML, SDKs, templates, business data or database providers are loaded.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import re
import xml.parsers.expat

ROOT = Path(__file__).resolve().parents[4]
AUDIT = ROOT / 'docs/audit'
BASELINE = '10ba215152f722c8808aea0bb672c1d1d4d9d711'
PARSER_VERSIONS = {'tree-sitter': '0.25.2', 'tree-sitter-c-sharp': '0.23.1'}
DECLARATIONS = frozenset({'method_declaration', 'constructor_declaration',
    'local_function_statement', 'operator_declaration', 'conversion_operator_declaration'})
TYPE_NODES = frozenset({'class_declaration', 'struct_declaration', 'interface_declaration',
    'record_declaration'})
# These are deliberately syntactic candidates, including unrelated homonyms.
CALL_NAMES = frozenset({'Printing', 'BindToData', 'RptPrint', 'ToArabicLetter',
    'SpellNumberEDP', 'NumberAsCurrency', 'FractionAsCurrency', 'SearchForBarcode',
    'ameral', 'ShowDialog', 'Show', 'PrintDialog', 'ShowPrintPreview',
    'PrintDirect', 'ExportToPdf', 'ExportToXlsx', 'ExportToXls', 'ExportToCsv',
    'ExportToHtml', 'PrintVisual', 'PrintDocument'})
EVENT_NAMES = frozenset({'Click', 'Loaded', 'Unloaded', 'Closing', 'Closed',
    'KeyDown', 'KeyUp', 'PreviewKeyDown', 'PreviewKeyUp', 'MouseDoubleClick',
    'MouseLeftButtonUp', 'MouseLeftButtonDown', 'SelectionChanged',
    'SelectedIndexChanged', 'SelectedValueChanged', 'Checked', 'Unchecked',
    'TextChanged', 'EditValueChanged', 'ValueChanged', 'DateChanged',
    'SelectedDateChanged', 'GotFocus', 'LostFocus', 'CellValueChanged',
    'CustomSummary', 'ShowingEditor', 'HiddenEditor', 'FocusedRowChanged',
    'RowUpdated', 'RowCellClick', 'SelectionModeChanged'})
IDENTIFIER = re.compile(r'^[A-Za-z_][A-Za-z_0-9]*$')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def row_sha(row: dict) -> str:
    return sha(json.dumps(row, ensure_ascii=False, sort_keys=True,
                          separators=(',', ':')).encode('utf8'))


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream))
    if any(None in r or any(v is None for v in r.values()) for r in rows):
        raise ValueError(f'Malformed CSV: {path}')
    return rows


def decode_source(data: bytes) -> tuple[str, str]:
    if data.startswith((b'\xff\xfe', b'\xfe\xff')):
        return data.decode('utf-16'), 'utf-16-bom'
    try:
        return data.decode('utf-8-sig'), 'utf-8-sig'
    except UnicodeDecodeError:
        # Strict read-only fallback, not the compiler's codepage certification.
        return data.decode('cp1256'), 'cp1256-strict-read-only-fallback'


def local_name(value: str) -> str:
    return value.rsplit('|', 1)[-1]


def numeric_spans(value: str) -> list[tuple[int, int]]:
    """Inclusive ranges; singleton citations are significant, not silently lost."""
    result = []
    for part in re.split(r'[;,،]', value):
        match = re.fullmatch(r'\s*(\d+)(?:[-–](\d+))?\s*', part)
        if match:
            first, last = int(match[1]), int(match[2] or match[1])
            if first < 1 or last < first:
                raise ValueError(f'Invalid span: {part}')
            result.append((first, last))
        elif part.strip() and part.strip().lower() not in {'none', 'none-metadata', 'n/a'}:
            raise ValueError(f'Unrecognized span: {part}')
    return result


def compact_spans(values: set[int]) -> str:
    if not values:
        return ''
    values = sorted(values)
    result = []
    first = last = values[0]
    for line in values[1:]:
        if line == last + 1:
            last = line
        else:
            result.append(str(first) if first == last else f'{first}-{last}')
            first = last = line
    result.append(str(first) if first == last else f'{first}-{last}')
    return ';'.join(result)


def xml_entries(text: str, method_names: set[str]) -> tuple[list[dict], str | None, str | None]:
    parser = xml.parsers.expat.ParserCreate(namespace_separator='|')
    entries = []
    xclass = None

    def start(name, attributes):
        nonlocal xclass
        if xclass is None:
            xclass = attributes.get('http://schemas.microsoft.com/winfx/2006/xaml|Class')
        control = attributes.get('http://schemas.microsoft.com/winfx/2006/xaml|Name',
                                 attributes.get('Name', ''))
        for attribute, value in sorted(attributes.items()):
            attr = local_name(attribute)
            event = attr in EVENT_NAMES or (IDENTIFIER.fullmatch(value) and value in method_names)
            command = attr in {'Command', 'CommandParameter'}
            if not (event or command):
                continue
            entries.append({'line': parser.CurrentLineNumber, 'element': local_name(name),
                'control_name': control, 'attribute': attr,
                'handler': value if event and IDENTIFIER.fullmatch(value) else None,
                'kind': 'command-attribute-not-binding-resolved' if command else
                        'possible-event-attribute-not-registration-proof',
                'literal_command_name': value if command and IDENTIFIER.fullmatch(value) else None})
    parser.StartElementHandler = start
    try:
        parser.Parse(text.encode('utf8'), True)
    except xml.parsers.expat.ExpatError as exc:
        # Keep discovery errors explicit. Do not repair XML or reinterpret as BAML.
        return entries, xclass, f'{exc.code}:{exc.lineno}:{exc.offset}'
    return entries, xclass, None


def build(root: Path = ROOT) -> dict:
    for package, expected in PARSER_VERSIONS.items():
        if version(package) != expected:
            raise ValueError(f'{package} must be {expected}')
    from tree_sitter import Language, Parser
    import tree_sitter_c_sharp
    parser = Parser(Language(tree_sitter_c_sharp.language()))
    audit = root / 'docs/audit'
    inventory = read_rows(audit / 'evidence/inventory.csv')
    originals = [r for r in inventory if r['kind'] == 'source']
    csharp = [r for r in originals if r['path'].endswith('.cs')]
    xamls = [r for r in originals if r['path'].endswith('.xaml')]
    source_files, methods, creations, calls, type_index = [], [], [], [], []
    by_path_names = defaultdict(set)
    for item in sorted(csharp, key=lambda x: x['path']):
        path = item['path']
        raw = (root / path).read_bytes()
        if sha(raw) != item['sha256']:
            raise ValueError(f'Source drift: {path}')
        text, encoding = decode_source(raw)
        encoded = text.encode('utf8')
        tree = parser.parse(encoded)
        source_files.append({'path': path, 'sha256': sha(raw), 'encoding': encoding,
                             'lines': len(text.splitlines()), 'parse_has_error': tree.root_node.has_error})

        def token(node):
            return encoded[node.start_byte:node.end_byte].decode('utf8') if node else ''

        def walk(node, owner_type='', owner=None):
            if node.type in TYPE_NODES:
                owner_type = token(node.child_by_field_name('name'))
                type_index.append({'path': path, 'name': owner_type,
                    'start': node.start_point.row + 1, 'end': node.end_point.row + 1})
            if node.type in DECLARATIONS:
                method = token(node.child_by_field_name('name')) or node.type
                owner = {'path': path, 'class_name': owner_type, 'method_name': method,
                         'start': node.start_point.row + 1, 'end': node.end_point.row + 1,
                         'node_type': node.type,
                         'syntax_utf8_sha256': sha(encoded[node.start_byte:node.end_byte])}
                methods.append(owner)
                by_path_names[path].add(method)
            if node.type in {'object_creation_expression', 'implicit_object_creation_expression'}:
                type_node = node.child_by_field_name('type')
                # No type inference for target-typed new; retain it as unresolved.
                name = token(type_node) if type_node else None
                target = re.split(r'[.<]', name)[-1] if name else None
                if name and '<' in name:
                    target = name.split('<', 1)[0].rsplit('.', 1)[-1]
                creations.append({'path': path, 'line': node.start_point.row + 1,
                    'end_line': node.end_point.row + 1, 'kind': 'constructor-syntax-only',
                    'target': target, 'type_text': name,
                    'class_name': owner_type,
                    'owner': owner['method_name'] if owner else None,
                    'owner_start': owner['start'] if owner else None,
                    'owner_end': owner['end'] if owner else None})
            if node.type == 'invocation_expression':
                function = node.child_by_field_name('function')
                name_node = function.child_by_field_name('name') if function else None
                name = token(name_node) if name_node else token(function)
                if name in CALL_NAMES or name.startswith(('ExportTo', 'PrintTo')):
                    calls.append({'path': path, 'line': node.start_point.row + 1,
                        'end_line': node.end_point.row + 1,
                        'kind': 'invocation-name-not-type-resolved', 'target': name,
                        'class_name': owner_type,
                        'owner': owner['method_name'] if owner else None,
                        'owner_start': owner['start'] if owner else None,
                        'owner_end': owner['end'] if owner else None})
            for child in node.named_children:
                walk(child, owner_type, owner)
        walk(tree.root_node)

    seed_rows = read_rows(audit / 'evidence/report-screen-disposition-07B16.csv')
    clarifications = read_rows(audit / 'evidence/report-depth-clarification-07B16.csv')
    seeds = {r['body_path'] for r in seed_rows} | {r['body_path'] for r in clarifications}
    seed_types = {r['name'] for r in type_index if r['path'] in seeds}
    selected_types = seed_types | {'Print', 'Report', 'InvPrinter', 'InvPrinter1',
        'Number2Arabic', 'frmItemsSrch', 'frmInvoiceSrch', 'frmInvoiceItems',
        'frmItemProperties', 'frmEditItems'}
    sites = [dict(r, selection_basis='declared-seed-type-or-helper-spelling') for r in creations
             if r['target'] in selected_types] + [dict(r, selection_basis='configured-call-spelling') for r in calls]
    # Target-typed new cannot be dismissed as not a report constructor.
    unresolved_new = [r for r in creations if r['target'] is None]
    sites.sort(key=lambda r: (r['path'], r['line'], r['kind'], str(r['target'])))

    xml_files, entries = [], []
    for item in sorted(xamls, key=lambda x: x['path']):
        path = item['path']
        raw = (root / path).read_bytes()
        if sha(raw) != item['sha256']:
            raise ValueError(f'Source drift: {path}')
        text, encoding = decode_source(raw)
        found, xclass, error = xml_entries(text, by_path_names[path + '.cs'])
        xml_files.append({'path': path, 'sha256': sha(raw), 'encoding': encoding,
                          'lines': len(text.splitlines()), 'x_class': xclass,
                          'xml_error_code_line_column': error})
        for found_entry in found:
            name = found_entry['handler']
            matches = [dict(start=m['start'], end=m['end'], class_name=m['class_name'])
                       for m in methods if m['path'] == path + '.cs' and m['method_name'] == name]
            entries.append(dict(found_entry, path=path, codebehind_name_matches=matches))

    historic_scope_inputs, historic_lines = [], defaultdict(set)
    for p in sorted(audit.glob('review-scope-*.csv')):
        # Stop at B37. Future source scopes must not silently improve this snapshot.
        match = re.search(r'07B(\d+)\.csv$', p.name)
        if match and int(match[1]) > 37:
            continue
        historic_scope_inputs.append({'path': p.relative_to(audit).as_posix(), 'sha256': sha(p.read_bytes())})
        for row in read_rows(p):
            for first, last in numeric_spans(row.get('ranges', '')):
                historic_lines[row['path']].update(range(first, last + 1))
    files = {r['path']: r for r in source_files + xml_files}
    selected_screens = []
    for row in seed_rows:
        selected_screens.append((row['path'], row['body_path'], 'frozen52-membership-not-denominator'))
    for row in clarifications:
        if (row['xaml_path'], row['body_path']) not in {(a, b) for a, b, _ in selected_screens}:
            selected_screens.append((row['xaml_path'], row['body_path'], 'explicit-B16-depth-clarification'))
    screens = []
    for xaml, body, selection in sorted(selected_screens):
        x, c = files[xaml], files[body]
        missing_x = set(range(1, x['lines'] + 1)) - historic_lines[xaml]
        missing_c = set(range(1, c['lines'] + 1)) - historic_lines[body]
        screens.append({'xaml_path': xaml, 'body_path': body, 'selection_basis': selection,
            'body_line_count': c['lines'], 'xaml_line_count': x['lines'],
            'historically_unselected_body_ranges': compact_spans(missing_c),
            'historically_unselected_xaml_ranges': compact_spans(missing_x),
            'entry_attribute_count': sum(e['path'] == xaml for e in entries),
            'output_or_modal_candidate_count': sum(s['path'] == body for s in sites),
            'interpretation': 'range-membership-and-syntax-discovery-not-semantic-completion'})
    return {'schema_version': 1, 'audit_reference_date_utc': '2026-11-16',
        'application_baseline': BASELINE, 'parser_packages': PARSER_VERSIONS,
        'source_inventory_sha256': sha((audit / 'evidence/inventory.csv').read_bytes()),
        'source_files': source_files, 'xaml_files': xml_files, 'methods': methods,
        'type_declarations': type_index, 'candidate_sites': sites,
        'target_typed_new_unresolved': unresolved_new, 'xaml_entry_attributes': entries,
        'historical_scope_inputs': historic_scope_inputs, 'seed_screens': screens,
        'summary': {'source_csharp_files': len(source_files), 'source_xaml_files': len(xml_files),
            'declarations': len(methods), 'candidate_sites': len(sites),
            'target_typed_new_unresolved': len(unresolved_new), 'xaml_entry_attributes': len(entries),
            'seed_screens': len(screens),
            'csharp_grammar_error_paths': [f['path'] for f in source_files if f['parse_has_error']],
            'xml_error_paths': [f['path'] for f in xml_files if f['xml_error_code_line_column']],
            'direct_item_picker_constructions': sum(s['kind'] == 'constructor-syntax-only' and s['target'] == 'frmItemsSrch' for s in sites),
            'direct_invoice_picker_constructions': sum(s['kind'] == 'constructor-syntax-only' and s['target'] == 'frmInvoiceSrch' for s in sites)},
        'limitations': ['Syntax parsing is not compilation, C# name/type resolution, or a semantic call graph.',
            'Seed52 plus three named B16 clarifications are historical seeds, not all capabilities.',
            'Call selection is name-based; homonyms are not resolved and omitted method names remain possible.',
            'Implicit construction, factories, reflection, aliases, dynamic and XAML activation need separate disposition.',
            'XAML attributes are possible entries, not registration/dispatch/reachability/authorization proof.',
            'Historical range union, including singletons, records declarations of reading, not semantic review.',
            'No source body is deemed reviewed by extraction, parsing, hashing, or citation membership.',
            'No ERP, build, SQL, provider, SDK, REPX, printing, business-data, remediation or operational test executed.'],
        'capability_denominator_agreed': False, 'whole_7B_complete': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True,
                        help='New JSON only; existing evidence is never overwritten.')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an existing snapshot. Choose a new versioned path.')
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x', encoding='utf8', newline='\n') as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'path': str(args.output), 'sha256': sha(args.output.read_bytes()),
                      'summary': result['summary'], 'whole_7B_complete': False}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
