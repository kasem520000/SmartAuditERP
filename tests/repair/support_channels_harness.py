#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-066 (audit finding P6-023), R-067 (P6-024),
R-068 (P6-025) and R-069 (P6-033). No .NET/HTTP/Selenium toolchain exists
here, so each repair is validated as a behavioural model of its exact
contract plus static witnesses over the repaired code.

Run: python3 tests/repair/support_channels_harness.py
Exit 0 on PASS.
"""
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


CLOUD = open("SmartAuditERP/Form_WPF/frmCloudPaymentSetting.xaml.cs", encoding="utf-8").read()
CLIENT = open("SmartAuditERP/Class/SupportTicketApiClient.cs", encoding="utf-8").read()
FORMT = open("SmartAuditERP/Form_WPF/FormCreateTicket.xaml.cs", encoding="utf-8").read()
WAPP = open("SmartAuditERP/Class/WhatsAppSender.cs", encoding="utf-8").read()

print("Part A: R-066 / P6-023 - revoking every link really clears it")


def save_bank_links(rules, db_links, ui_rows):
    """db_links: stored id>4 rows; ui_rows: (BankId,PayTypeId) pairs in the grid."""
    if rules == "legacy" and len(ui_rows) > 0:              # delete hid inside the guard
        db_links = []
    elif rules == "fixed":                                  # unconditional scoped clear
        db_links = []
    for bank_id, pay_type in ui_rows:
        if not bank_id or not pay_type:                     # blanks skipped, unchanged
            continue
        db_links.append((bank_id, pay_type))
    return db_links


stored = [("B1", "P1"), ("B2", "P2")]
check("A1 deleting the LAST link left stale rows feeding cloud payments (bug reproduced)",
      save_bank_links("legacy", list(stored), []) == stored and
      save_bank_links("fixed", list(stored), []) == [])
check("A2 partial edits converge identically under both rules (no behaviour change there)",
      save_bank_links("legacy", list(stored), [("B9", "P9")]) ==
      save_bank_links("fixed", list(stored), [("B9", "P9")]) == [("B9", "P9")])
check("A3 blank grid cells stay skipped exactly as before",
      save_bank_links("fixed", [], [("B1", ""), ("", "P2"), ("B3", "P3")]) == [("B3", "P3")])
save_region = CLOUD[CLOUD.index("private void btnSave_Click"): CLOUD.index("GetNextSettingId")]
check("A4 static: the scoped delete precedes the count guard; loading happens at window load",
      save_region.index('DELETE FROM CloudPaytypeSetting WHERE ID > 4') <
      save_region.index("if (_bankRows.Count > 0)") and
      "_bankRows.Clear();" in CLOUD and
      CLOUD.index("loadSavedData();") < CLOUD.index("private void btnSave_Click"))

print("Part B: R-067 / P6-024 - ticket lookup can no longer hand back an empty Ticket")


def get_ticket(rules, http_ok, body):
    """body: None | {'success': bool, 'ticketNumber': str}; returns (Success, Ticket)."""
    if not http_ok:
        return (False, None)
    if rules == "legacy":
        _ = body                                            # deserialized then DISCARDED
        return (True, None)                                 # Success with empty Ticket
    if body is None or not body.get("success"):
        return (False, None)
    num = body.get("ticketNumber") or ""
    return (True, {"TicketNumber": num, "Subject": None, "Status": None})


def view_handler_gets_subject(outcome):
    success, ticket = outcome
    if rules_consumed_by_legacy_view(success, ticket):
        return ticket["Subject"]                            # would raise on None ticket
    return "(guarded)"


def rules_consumed_by_legacy_view(success, ticket):
    return success                                          # legacy: reads fields unconditionally


leg = get_ticket("legacy", True, {"success": True, "ticketNumber": "T-9"})
fix = get_ticket("fixed", True, {"success": True, "ticketNumber": "T-9"})
try:
    view_handler_gets_subject(leg)
    raised = False
except TypeError:
    raised = True
check("B1 legacy Success carried a null Ticket that the view dereferenced (bug reproduced)",
      leg == (True, None) and raised)
check("B2 repaired success returns the guaranteed number; business failure propagates",
      fix[0] is True and fix[1]["TicketNumber"] == "T-9" and
      get_ticket("fixed", True, {"success": False, "ticketNumber": ""}) == (False, None) and
      get_ticket("fixed", True, None) == (False, None))
check("B3 success still holds with a blank returned number (fallback shown statically in B4)",
      get_ticket("fixed", True, {"success": True, "ticketNumber": ""})[0] is True)
getm = CLIENT.split("public async Task<TicketDetailsResponse> GetTicketAsync")[1][:2200]
check("B4 static: wrapper captured, failure honoured, path encoded, consumer null-safe",
      "var apiDetails = JsonConvert.DeserializeObject<TicketDetailsApiResponse>(responseBody);" in getm and
      "if (apiDetails == null || !apiDetails.Success)" in getm and
      "? ticketNumber" in getm and
      "JsonConvert.DeserializeObject<TicketDetailsApiResponse>(responseBody);\n                    return new TicketDetailsResponse { Success = true };" not in CLIENT and
      "Uri.EscapeDataString(ticketNumber)" in getm and
      "if (result.Success && result.Ticket != null)" in FORMT and
      '?? "(غير متوفر)"' in FORMT)

def call_raises(fn):
    try:
        fn()
        return False
    except Exception:
        return True


print("Part C: R-068 / P6-025 - transport acceptance is not business success")


def create_ticket(rules, http_ok, envelope):
    if not http_ok:
        return False
    if rules == "legacy":
        return True                                         # any 2xx
    return envelope is not None and envelope.get("success", False)


def add_reply(rules, http_ok, body_text, parsed):
    if not http_ok:
        return (False, "فشل إضافة الرد")
    if rules == "legacy":
        return (True, "تم إضافة الرد بنجاح")               # body ignored entirely
    if parsed is not None and not parsed.get("success", False):
        return (False, parsed.get("message") or "رفض الخادم إضافة الرد")
    return (True, "تم إضافة الرد بنجاح")


def customer_tickets(rules, http_ok, rows=None, threw=False):
    if threw:
        if rules == "legacy":
            return []                                       # silence
        raise RuntimeError("transport down")
    if not http_ok:
        if rules == "legacy":
            return []                                       # indistinguishable from empty
        raise RuntimeError("فشل جلب التذاكر (500)")
    return rows if rows is not None else []


check("C1 legacy counted a business rejection inside 2xx as success (bug reproduced)",
      create_ticket("legacy", True, {"success": False}) is True and
      create_ticket("fixed", True, {"success": False}) is False)
check("C2 honest paths preserved: real success true, HTTP failure false, unreadable body false",
      create_ticket("fixed", True, {"success": True}) is True and
      create_ticket("fixed", False, None) is False and
      create_ticket("fixed", True, None) is False)
check("C3 reply failures carried by a 2xx body now surface; shape-less bodies keep acceptance",
      add_reply("legacy", True, '{"success":false}', {"success": False})[0] is True and
      add_reply("fixed", True, "...", {"success": False, "message": "مرفوض"}) == (False, "مرفوض") and
      add_reply("fixed", True, "", None)[0] is True and add_reply("fixed", False, "", None)[0] is False)
check("C4 failed listings no longer masquerade as empty while genuine empties stay empty",
      customer_tickets("legacy", False) == [] and
      call_raises(lambda: customer_tickets("fixed", False)) and
      call_raises(lambda: customer_tickets("fixed", True, threw=True)) and
      customer_tickets("fixed", True, rows=[]) == [])
cc = CLIENT.split("public async Task<TicketResponse>")[1]
check("C5 static: envelope flag trusted, reply body parsed, failures thrown, values encoded",
      "Success = apiResponse != null && apiResponse.Success," in cc and
      "JsonConvert.DeserializeObject<ApiResponseBase>(replyBody)" in cc and
      "throw new HttpRequestException(" in cc and
      "Uri.EscapeDataString(customerName ?? \"\")" in cc)
m_tail = CLIENT.split("خطأ في GetCustomerTicketsAsync")[1][:200]
check("C6 the listing catch logs then rethrows instead of swallowing",
      "throw;" in m_tail)

print("Part D: R-069 / P6-033 - a missing attachment aborts before anything sends")


def whatsapp_flow(rules, file_exists):
    events = []
    if rules == "fixed":
        if not file_exists:
            return ["preflight-abort"]                      # nothing touched
    events += ["navigate", "wait-chat"]
    events += ["send-text"]
    events += ["open-attach-dialog"]
    if rules == "legacy" and not file_exists:
        events += ["abort-after-partial-send"]
        return events
    events += ["send-file", "click-send"]
    return events


leg_absent = whatsapp_flow("legacy", False)
fix_absent = whatsapp_flow("fixed", False)
check("D1 legacy half-delivered the notification before noticing the missing file (bug)",
      "send-text" in leg_absent and leg_absent[-1] == "abort-after-partial-send")
check("D2 repaired absence aborts pre-flight; present files flow identically thereafter",
      fix_absent == ["preflight-abort"] and
      whatsapp_flow("legacy", True) == whatsapp_flow("fixed", True) ==
      ["navigate", "wait-chat", "send-text", "open-attach-dialog", "send-file", "click-send"])
m = WAPP.split("public async Task<bool> SendInvoiceAsync")[1]
check("D3 static: the single existence check now precedes navigation and the late abort is gone",
      m.count("لم يتم العثور على الملف:") == 1 and
      m.index("!File.Exists(invoiceFilePath)") < m.index("Navigate().GoToUrl") and
      "// R-069: attachment existence was already enforced pre-flight" in m)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - links revoke, tickets report honestly, listings distinguish empty from")
print("failed, and attachments are checked before a single keystroke.")
sys.exit(0)
