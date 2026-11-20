#!/usr/bin/env python3
"""P7-162: source witnesses and a small event-dispatch model, not a WPF test.

The model assumes the ordinary XAML/WPF event wiring and synchronous normal return.
It does not instantiate a window, exercise generated BAML, or prove a save occurred.
"""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
base = ROOT / "SmartAuditERP" / "Form_WPF"
xaml = (base / "frmInvSale.xaml").read_text(encoding="utf-8-sig")
code = (base / "frmInvSale.xaml.cs").read_text(encoding="utf-8-sig")
checks = 0


def check(name, condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(name)
    print("PASS", name)


def strip_comments(s):
    # Mask strings as well as comments, so a logger message naming a handler
    # is not mistaken for a registration.
    tokens = r'@"(?:""|[^"])*"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*.*?\*/'
    return re.sub(tokens, " ", s, flags=re.S)


def body(text, signature):
    start = text.index(signature)
    opening = text.index("{", start)
    depth = 0
    for i in range(opening, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[opening + 1:i]
    raise AssertionError("unclosed " + signature)


def source_contract(x, c):
    root = ET.fromstring(x)
    expected = {"Loaded": "Window_Loaded", "Closing": "Window_Closing", "KeyDown": "Window_KeyDown"}
    if any(root.attrib.get(event) != handler for event, handler in expected.items()):
        return False
    plain = strip_comments(c)
    # All direct references, not merely those inside the constructor: each handler
    # should occur once, at its declaration. This also catches += and AddHandler.
    for event, handler in expected.items():
        if len(re.findall(r"\b" + handler + r"\b", plain)) != 1:
            return False
        if not re.search(r"\bvoid\s+" + handler + r"\s*\(", plain):
            return False
        if re.search(r"\b(?:this\s*\.\s*)?" + event + r"\s*\+=", plain):
            return False
    return True


check("XAML owns each handler once, with no code-behind duplicate", source_contract(xaml, code))
constructor = body(code, "public frmInvSale()")
check("InitializeComponent and the timer subscription remain", "InitializeComponent();" in constructor and
      "Timer1.Tick += Timer1_Tick;" in constructor)
closing = body(code, "private void Window_Closing(")
key = body(code, "private void Window_KeyDown(")
loaded = body(code, "private void Window_Loaded(")
check("close guard and No veto remain", "(hasRows && Invoic.ISNew) || Invoic.IsUpdated" in closing and
      "result == MessageBoxResult.No" in closing and "e.Cancel = true;" in closing and
      not re.search(r"e\.Cancel\s*=\s*false", closing))
check("F6 still requests validation without setting Handled", bool(re.search(
    r"if\s*\(e\.Key\s*==\s*Key\.F6\)\s*ValidateInvoice\(\);", key)))
check("F5 marks the event handled after new returns", bool(re.search(
    r"if\s*\(e\.Key\s*==\s*Key\.F5\)\s*\{\s*btnNew_Click\(null, null\);\s*e\.Handled\s*=\s*true;", key)))
check("loaded retains reset and timer", "ResetInvoice();" in loaded and "Timer1.Start();" in loaded)

# Models an invocation list; supplied booleans describe the guard, response and
# incoming veto, not externally observed WPF state.
def close(subscriptions, dirty, responses, incoming_cancel=False):
    cancel = incoming_cancel
    calls = 0
    for _ in range(subscriptions):
        if dirty:
            answer = responses[calls]
            calls += 1
            if answer == "No":
                cancel = True
    return calls, cancel


def keydown(subscriptions, key_name, handled=False, returns=True):
    calls = 0
    for _ in range(subscriptions):
        if handled:  # ordinary routed-event subscriptions, not handledEventsToo
            break
        calls += 1
        if not returns:
            break
        if key_name == "F5":
            handled = True
    return calls, handled


check("legacy close may ask twice", close(2, True, ["Yes", "Yes"]) == (2, False))
check("one subscription asks once on Yes", close(1, True, ["Yes"]) == (1, False))
check("No vetoes close", close(1, True, ["No"]) == (1, True))
check("incoming veto survives Yes", close(1, True, ["Yes"], True) == (1, True))
check("clean close asks nothing and preserves veto", close(1, False, [], True) == (0, True))
check("legacy F6 can request validation twice", keydown(2, "F6") == (2, False))
check("fixed F6 requests validation once", keydown(1, "F6") == (1, False))
check("F5 marks handled after return even with legacy duplicate", keydown(2, "F5") == (1, True))
check("previously handled key invokes no ordinary handler", keydown(1, "F6", True) == (0, True))
check("non-returning callback does not reach a later handler", keydown(2, "F6", returns=False) == (1, False))
check("independent windows each have one subscription", [close(1, True, ["Yes"]),
      close(1, True, ["No"])] == [(1, False), (1, True)])

# Exercise the source witness itself against representative regressions in memory.
mutants = [
    (xaml.replace('Loaded="Window_Loaded"', ''), code),
    (xaml.replace('Closing="Window_Closing"', 'Closing="Other"'), code),
    (xaml.replace('KeyDown="Window_KeyDown"', ''), code),
    (xaml, code.replace('InitializeComponent();', 'InitializeComponent();\n            Loaded += Window_Loaded;', 1)),
    (xaml, code.replace('InitializeComponent();', 'InitializeComponent();\n            this.Closing += Window_Closing;', 1)),
    (xaml, code.replace('InitializeComponent();', 'InitializeComponent();\n            KeyDown += Window_KeyDown;', 1)),
    (xaml, code.replace('InitializeComponent();', 'InitializeComponent();\n            AddHandler(KeyDownEvent, Window_KeyDown);', 1)),
]
for i, (mx, mc) in enumerate(mutants, 1):
    check("source witness rejects mutant %d" % i, not source_contract(mx, mc))
print("RESULT: PASS - %d checks; source and supplied models only, no WPF execution." % checks)
