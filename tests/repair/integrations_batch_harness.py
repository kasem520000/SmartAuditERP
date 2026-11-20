#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-059 (P6-011), R-061 (P6-014), R-062 (P6-016),
R-063 (P6-017), R-064 (P6-032) and R-065 (P6-035). No .NET/ZATCA/ETA/SMTP
toolchain exists here, so each repair is validated as a behavioural model of
its exact contract plus static witnesses (including a real parse-and-parity
check of the repaired SQL statements).

Run: python3 tests/repair/integrations_batch_harness.py
Exit 0 on PASS.
"""
import re
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


ZATCA = open("SmartAuditERP/Form_WPF/frmZatcaSetting.xaml.cs", encoding="utf-8").read()
ETASVC = open("SmartAuditERP/Class/EtaService.cs", encoding="utf-8").read()
RECPT = open("SmartAuditERP/Class/EtaReciptService.cs", encoding="utf-8").read()
WAPP = open("SmartAuditERP/Class/WhatsAppSender.cs", encoding="utf-8").read()
CLOSE = open("SmartAuditERP/Form_WPF/ClosShiftAndroid.xaml.cs", encoding="utf-8").read()

print("Part A: R-059 / P6-011 - credential inserts are executable statements")


def insert_verdict(columns, values, bound_params):
    """models SQL Server's arity/parameter checks for one INSERT."""
    if len(columns) != len(values):
        return "error: column count %d <> value count %d" % (len(columns), len(values))
    unbound = [v for v in values if v.startswith("@") and v.lstrip("@") not in bound_params]
    if unbound:
        return "error: must declare scalar variable(s) %s" % ",".join(unbound)
    return "ok:%d rows" % 1


def parse_insert(src, table_marker):
    i = src.index(table_marker)
    stmt = src[i: src.index(')", conn)', i)] + ')"'
    cols = re.search(r"\((ID[^)]*)\)", stmt).group(1)
    vals = re.search(r"VALUES\(([^)]*)\)", stmt).group(1)
    return [c.strip() for c in cols.split(",")], [v.strip() for v in vals.split(",")]


def bound_after(src, start_marker, end_marker):
    seg = src[src.index(start_marker): src.index(end_marker)]
    return set(re.findall(r'cmd\.Parameters\.Add\("@([A-Za-z_]+)"', seg))


b1_cols, b1_vals = parse_insert(ZATCA, "INSERT INTO ZatcaCredential(ID,P_RequestID")
b1_bound = bound_after(ZATCA, "if (count == 0)\n                    // Repair R-059",
                       "DXMessageBox.Show(\"تم تحديث البيانات بنجاح\"")
def parse_insert_after(src, anchor):
    """locates the INSERT statement that follows a unique R-059 comment anchor."""
    tail = src[src.index(anchor):]
    return parse_insert(tail, '"INSERT INTO ZatcaCredential "')


b2_cols, b2_vals = parse_insert_after(ZATCA, "// unowned by this payload and nullable")
_b2_tail = ZATCA[ZATCA.index("// unowned by this payload and nullable"):]
b2_bound = set(re.findall(r'cmd\.Parameters\.Add\("@([A-Za-z_]+)"',
                          _b2_tail[: _b2_tail.index("cmd.ExecuteNonQuery();")]))

LEGACY_COLS = ["ID", "CSR", "RequestID", "CSID", "Secret", "P_RequestID", "P_CSID", "P_Secret"]
LEGACY_VALS = ["1", "@RequestID", "@CSID", "@Secret", "@P_RequestID", "@P_CSID", "@P_Secret"]
check("A1 both legacy inserts fail arity before any parameter question (bug reproduced)",
      insert_verdict(LEGACY_COLS, LEGACY_VALS, set()) .startswith("error: column count 8 <> value count 7"))
check("A2 onboard branch now matches 4/4 with its three parameters bound (+constant 1)",
      b1_cols == ["ID", "P_RequestID", "P_CSID", "P_Secret"] and
      b1_vals == ["1", "@P_RequestID", "@P_CSID", "@P_Secret"] and
      insert_verdict(b1_cols, b1_vals, b1_bound) == "ok:1 rows")
check("A3 import branch now matches 7/7 with all six parameters bound",
      b2_cols == ["ID", "RequestID", "CSID", "Secret", "P_RequestID", "P_CSID", "P_Secret"] and
      b2_vals == ["1", "@RequestID", "@CSID", "@Secret", "@P_RequestID", "@P_CSID", "@P_Secret"] and
      insert_verdict(b2_cols, b2_vals, b2_bound) == "ok:1 rows")
check("A4 CSR is gone from both statements and every UPDATE arm stayed untouched",
      ZATCA.count("(ID,CSR,RequestID") == 0 and
      ZATCA.count("\"(ID,CSR,RequestID,CSID,Secret,P_RequestID,P_CSID,P_Secret) \" +") == 0 and
      ZATCA.count("UPDATE ZatcaCredential SET P_RequestID=@P_RequestID,") == 1 and
      ZATCA.count("RequestID=@RequestID,CSID=@CSID,Secret=@Secret,") == 1)

print("Part B: R-061/R-062 / P6-014,P6-016 - ETA invoice converter and send outcome")


def sales_order_reference(rules, proc_type, reff_no):
    base = ""
    if proc_type != 2:
        return base
    if rules == "legacy":
        return str("" == reff_no)                             # Conversions.ToString(compare==0)
    return reff_no if reff_no is not None else ""             # (ReffNo ?? "") ?? ""


check("B1 legacy wrote the COMPARISON'S TEXT where the reference belongs (bug reproduced)",
      sales_order_reference("legacy", 2, "INV-7") == "False" and
      sales_order_reference("legacy", 2, "") == "True")
check("B2 repaired credit notes carry the reference verbatim; non-credit stays empty",
      sales_order_reference("fixed", 2, "INV-7") == "INV-7" and
      sales_order_reference("fixed", 2, "") == "" and
      sales_order_reference("fixed", 1, "INV-7") == "")


def eta_send(rules, ds_shape):
    """ds_shape: None | 'no_tables' | 'without_accepted' | 'accepted_empty' | 'uuid_blank' | 'uuid_valid'."""
    returnds = None
    tables = {}
    uuid = None
    if ds_shape == "no_tables":
        returnds = object()
    elif ds_shape == "without_accepted":
        returnds, tables = object(), {"other": [[]]}
    elif ds_shape == "accepted_empty":
        returnds, tables = object(), {"acceptedDocuments": []}
    elif ds_shape == "uuid_blank":
        returnds, tables = object(), {"acceptedDocuments": [["   "]]}
    elif ds_shape == "uuid_valid":
        returnds, tables = object(), {"acceptedDocuments": [["abc-uuid"]]}
        uuid = "abc-uuid"
    stored = False
    outcome = False                                           # default(bool)
    if rules == "legacy":
        try:
            _ = tables[list(tables)[0]][0] if tables else (_ for _ in ()).throw(KeyError())
            if returnds is not None:                          # guard AFTER the read
                stored = True                                 # unconditional Rows[0]['uuid']
        except Exception:
            return ("crash-dialog-or-nre", False, stored)
        return ("shown", outcome, stored)                     # outcome never touched
    # repaired flow
    shown = returnds is not None and len(tables) > 0
    if "acceptedDocuments" in tables:
        rows = tables["acceptedDocuments"]
        if rows and rows[0][0].strip():
            stored = True
            outcome = True
    return ("shown" if shown else "skipped-dialog", outcome, stored)


for shape in ("None", "no_tables", "without_accepted", "accepted_empty", "uuid_blank"):
    leg = eta_send("legacy", None if shape == "None" else shape)
    fix = eta_send("fixed", None if shape == "None" else shape)
    check("B3 degenerate response %-17s legacy %s vs repaired honest false" % (shape, leg[0]),
          fix[1] is False and fix[2] is False and (leg[0] != "shown" or leg[1] is False))
fix_ok = eta_send("fixed", "uuid_valid")
leg_ok = eta_send("legacy", "uuid_valid")
check("B4 a genuinely accepted document: legacy still reports false (bug); repaired true+stored",
      leg_ok[1] is False and fix_ok == ("shown", True, True))
send_seg = ETASVC.split("sendEinvoice.sendinvoice(invoiceBody);")[1][:2500]
check("B5 static: grid shape-guarded, UUID validated, result assigned after the store",
      "sendEinvoice.returnds.Tables.Count > 0" in send_seg and
      'Tables.Contains("acceptedDocuments")' in send_seg and
      "!string.IsNullOrWhiteSpace(uuidValue.ToString())" in send_seg and
      "result = true;" in send_seg and
      '(invoice.ReffNo ?? "") ?? ""' in ETASVC and
      'Conversions.ToString(Operators.CompareString("", invoice.ReffNo' not in ETASVC)

print("Part C: R-063 / P6-017 - ETA receipt outcome follows the provider status")


def receipt_send(rules, status, threw=False):
    if threw:
        return False                                          # outer catch, unchanged
    uuid_stored = status == "200"
    if rules == "legacy":
        return True                                           # try{ result=true; } unconditionally
    return bool(uuid_stored)


check("C1 legacy reported success for rejections/pending alike (bug reproduced)",
      receipt_send("legacy", "402") is True and receipt_send("legacy", "202") is True)
check("C2 repaired: true only when the provider accepted and the UUID was stored",
      receipt_send("fixed", "200") is True and
      receipt_send("fixed", "402") is False and receipt_send("fixed", "202") is False)
seg = RECPT.split("send_respons_model = await SendRecipt.send_recipt")[1][:1400]
check("C3 static: the acceptance arm owns the only true; the stuck-result scaffolding is gone",
      "return true;" in seg and "return false;" in seg and
      "bool result = default(bool);" not in seg and
      "send_respons_model != null && Operators.CompareString(send_respons_model.status" in RECPT)

print("Part D: R-064 / P6-032 - phone forms normalize without mangling")


def whatsapp_number(rules, raw):
    text = raw.strip()
    if rules == "legacy":
        if not text.startswith("966"):
            text = "966" + text.lstrip("0")
        return text
    if text.startswith("+"):
        return text[1:].lstrip("0")
    if text.startswith("00"):
        return text[2:].lstrip("0")
    if not text.startswith("966"):
        text = "966" + text.lstrip("0")
    return text


check("D1 legacy corrupted explicit international numbers (bug reproduced)",
      whatsapp_number("legacy", "+966501234567") == "966+966501234567" and
      whatsapp_number("legacy", "009677123456") == "9669677123456")   # zeros stripped too
check("D2 repaired unwraps + and 00 to E.164 digits",
      whatsapp_number("fixed", "+966501234567") == "966501234567" and
      whatsapp_number("fixed", "009677123456") == "9677123456")
nationals = ["0501234567", "501234567", "966501234567", "  0559876543 "]
check("D3 plain national inputs behave byte-identically to the legacy rule",
      all(whatsapp_number("fixed", n) == whatsapp_number("legacy", n) for n in nationals))
norm = WAPP.split("SendInvoiceAsync")[1][:1200]
check("D4 static: recognition precedes the preserved national normalization",
      norm.index('text.StartsWith("+")') < norm.index('text.StartsWith("00")') <
      norm.index('!text.StartsWith("966")') and '"966" + text.TrimStart(\'0\')' in norm)

print("Part E: R-065 / P6-035 - Android closing emails send once")


def closing_sends(rules, close_type, printer_set, auto_ok=True):
    if not printer_set:
        return 0                                              # settings warning instead
    sends = 0
    if close_type == 1:
        pass                                                  # N prints, not modeled
    elif close_type == 2:
        pass                                                  # preview dialog
    elif close_type == 3:
        if rules == "legacy":
            sends += 1                                        # the in-switch duplicate
    if auto_ok:
        sends += 1                                            # the shared trailing SendEmail
    return sends


check("E1 legacy delivered Type 3 twice while print/preview mailed once (bug reproduced)",
      closing_sends("legacy", 3, True) == 2 and
      closing_sends("legacy", 1, True) == 1 and closing_sends("legacy", 2, True) == 1)
check("E2 repaired: exactly one email per configured run, none without a printer",
      closing_sends("fixed", 3, True) == 1 and
      closing_sends("fixed", 1, True) == 1 and closing_sends("fixed", 3, False) == 0)
region = CLOSE[CLOSE.index("switch (Type)"): CLOSE.index("يجب  تحديد الطابعة من الإعدادات")]
case3 = region[region.index("case 3:"): region.index("}", region.index("case 3:"))]
check("E3 static: case 3 no longer CALLS SendEmail (comment aside) and the shared call survives once",
      "this.SendEmail(" not in case3 and region.count("this.SendEmail(xtraReport);") == 1)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - credentials insert, converters tell the truth, outcomes are honest,")
print("numbers keep their country, and closings mail once.")
sys.exit(0)
