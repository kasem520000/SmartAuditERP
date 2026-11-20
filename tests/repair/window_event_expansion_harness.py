#!/usr/bin/env python3
"""R-099/R-100 source witnesses and supplied dispatch models, not WPF tests.

Models assume normal XAML event hookup and callback return; they do not run login,
query data, construct a window, or prove what a deployed BAML contains.
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parents[2] / 'SmartAuditERP' / 'Form_WPF'


def read(name):
    return (BASE / name).read_text(encoding='utf-8-sig')


def mask_comments_and_strings(source):
    tokens = r'@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/'
    return re.sub(tokens, ' ', source, flags=re.S)


def method(source, signature):
    start = source.index(signature)
    opening = source.index('{', start)
    depth = 0
    # Code in these selected methods has no braces inside literals or comments.
    for pos in range(opening, len(source)):
        if source[pos] == '{':
            depth += 1
        elif source[pos] == '}':
            depth -= 1
            if depth == 0:
                return source[opening + 1:pos]
    raise AssertionError('unclosed method: ' + signature)


def direct_refs(source, handler):
    return len(re.findall(r'\b' + re.escape(handler) + r'\b', mask_comments_and_strings(source)))


def login_contract(xaml, code):
    root = ET.fromstring(xaml)
    expected = {'Loaded': 'Window_Loaded', 'Closing': 'Window_Closing', 'KeyDown': 'Window_KeyDown'}
    clean = mask_comments_and_strings(code)
    return all(root.attrib.get(event) == handler and direct_refs(code, handler) == 1 and
               re.search(r'\bvoid\s+' + handler + r'\s*\(', clean)
               for event, handler in expected.items())


def contract_search_contract(xaml, code):
    root = ET.fromstring(xaml)
    clean = mask_comments_and_strings(code)
    constructor = method(clean, 'public frmContractSrchPM()')
    loaded_registrations = re.findall(r'\b(?:this\s*\.\s*)?Loaded\s*\+=\s*Window_Loaded\s*;', clean)
    return (root.attrib.get('Deactivated') == 'Window_Deactivated' and
            'Loaded' not in root.attrib and direct_refs(code, 'Window_Deactivated') == 1 and
            re.search(r'\bvoid\s+Window_Deactivated\s*\(', clean) is not None and
            direct_refs(code, 'Window_Loaded') == 2 and len(loaded_registrations) == 1 and
            re.search(r'\b(?:this\s*\.\s*)?Loaded\s*\+=\s*Window_Loaded\s*;', constructor) is not None)


checks = 0

def check(label, value):
    global checks
    checks += 1
    if not value:
        raise AssertionError(label)
    print('PASS', label)


lx, lc = read('frmUserLogin.xaml'), read('frmUserLogin.xaml.cs')
cx, cc = read('frmContractSrchPM.xaml'), read('frmContractSrchPM.xaml.cs')
check('login uses XAML once for its three window handlers', login_contract(lx, lc))
check('contract search keeps Loaded in code and Deactivated in XAML', contract_search_contract(cx, cc))
login_ctor = method(lc, 'public frmUserLogin()')
search_ctor = method(cc, 'public frmContractSrchPM()')
check('login constructor retains initialization and direction', 'InitializeComponent();' in login_ctor and
      'this.FlowDirection = FlowDirection.LeftToRight;' in login_ctor)
check('search initialization precedes its Loaded registration',
      search_ctor.index('InitializeComponent();') < search_ctor.index('this.Loaded += Window_Loaded;'))
login_loaded = method(lc, 'private void Window_Loaded(')
login_closing = mask_comments_and_strings(method(lc, 'private void Window_Closing('))
login_key = method(lc, 'private void Window_KeyDown(')
search_loaded = method(cc, 'private void Window_Loaded(')
search_deactivated = method(cc, 'private void Window_Deactivated(')
check('login Loaded keeps language, data and version setup', all(x in login_loaded for x in
      ('cmblanguages.SelectedIndex = 0;', 'LoadData();', 'Common.CurrentVersion();', 'Common.SalesmanSetting();')))
check('login Closing remains empty', not login_closing.strip())
check('login F4 is still marked handled', re.search(r'if\s*\(e\.Key\s*==\s*Key\.F4\)\s*e\.Handled\s*=\s*true;', login_key) is not None)
check('search Loaded keeps all three data loads', all(x in search_loaded for x in
      ('LoadDgvItems();', 'LoadClient();', 'LoadStatus();')))
check('search Deactivated still closes the window', 'this.Close();' in search_deactivated)

# A simple invocation-list model, not a WPF implementation. F4 sets Handled
# after a normal callback return; a close callback may instead fail or reenter.
def dispatch(count, event, handled=False, returns=True):
    calls = 0
    for _ in range(count):
        if event == 'F4' and handled:
            break
        calls += 1
        if not returns:
            break
        if event == 'F4':
            handled = True
    return calls, handled


check('legacy login Loaded can invoke twice under the model', dispatch(2, 'Loaded') == (2, False))
check('login Loaded now has one modeled invocation', dispatch(1, 'Loaded') == (1, False))
check('F4 with legacy duplicate is handled after first normal callback', dispatch(2, 'F4') == (1, True))
check('already handled F4 does not invoke ordinary subscription', dispatch(1, 'F4', True) == (0, True))
check('search deactivation has one modeled close request', dispatch(1, 'Deactivated') == (1, False))
check('search Loaded remains once', dispatch(1, 'Loaded') == (1, False))
check('a non-returning callback is not modeled as reaching the next', dispatch(2, 'Deactivated', returns=False) == (1, False))
check('independent instances each get their own event', [dispatch(1, 'Loaded'), dispatch(1, 'Loaded')] == [(1, False), (1, False)])

# Verify witness catches removal and reintroduction of the relevant registrations.
login_mutants = [
    (lx.replace('Loaded="Window_Loaded"', ''), lc),
    (lx.replace('Closing="Window_Closing"', ''), lc),
    (lx.replace('KeyDown="Window_KeyDown"', ''), lc),
    (lx, lc.replace('InitializeComponent();', 'InitializeComponent();\n this.Loaded += Window_Loaded;', 1)),
    (lx, lc.replace('InitializeComponent();', 'InitializeComponent();\n this.Closing += Window_Closing;', 1)),
    (lx, lc.replace('InitializeComponent();', 'InitializeComponent();\n this.KeyDown += Window_KeyDown;', 1)),
]
for n, (x, c) in enumerate(login_mutants, 1):
    check('login witness rejects mutant %d' % n, not login_contract(x, c))
search_mutants = [
    (cx.replace('Deactivated="Window_Deactivated"', ''), cc),
    (cx, cc.replace('InitializeComponent();', 'InitializeComponent();\n this.Deactivated += Window_Deactivated;', 1)),
    (cx, cc.replace('this.Loaded += Window_Loaded;', '', 1)),
    (cx.replace('Deactivated="Window_Deactivated"', 'Loaded="Window_Loaded" Deactivated="Window_Deactivated"'), cc),
    (cx, cc.replace('this.Loaded += Window_Loaded;', 'this.Loaded += Window_Loaded;\n this.Loaded += Window_Loaded;', 1)),
]
for n, (x, c) in enumerate(search_mutants, 1):
    check('search witness rejects mutant %d' % n, not contract_search_contract(x, c))
print('RESULT: PASS - %d checks; static witnesses and supplied models only.' % checks)
