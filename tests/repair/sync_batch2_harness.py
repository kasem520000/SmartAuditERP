#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-053 (audit finding P5-019), R-054 (P5-029),
R-055 (P5-022) and R-056 (P5-013). No .NET/SQL Server toolchain exists here,
so each repair is validated as a behavioural model of its exact contract
(including an SQLite-backed replay where natural) plus static witnesses over
the repaired code.

Run: python3 tests/repair/sync_batch2_harness.py
Exit 0 on PASS.
"""
import re
import sqlite3
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


ENT = open("SmartAuditERP/Class/EntityOperations.cs", encoding="utf-8").read()
INVOP = open("SmartAuditERP/Class/InvoiceOper.cs", encoding="utf-8").read()
CONTRACT = open("SmartAuditERP/Class/InvoiceOperContract.cs", encoding="utf-8").read()
SYNC = open("SmartAuditERP/Class/Sync.cs", encoding="utf-8").read()
RECVD = open("SmartAuditERP/Class/ReceivedData.cs", encoding="utf-8").read()

print("Part A: R-053 / P5-019 - downloaded employees actually update")


class Emp:
    def __init__(self, emp_id, name, salary):
        self.emp_id, self.name, self.salary = emp_id, name, salary


def save_employee(rules, db, employees, added_locally, branches_log):
    """mirrors the branch selection of EntityOperations.SaveEmployee."""
    for e in employees:
        count = len([r for r in db["employees"] if r["id"] == e.emp_id])
        if count == 0:
            action = "INSERT"
            db["employees"].append({"id": e.emp_id, "name": e.name, "salary": e.salary})
        elif added_locally or rules == "fixed":
            if added_locally:                              # branch refresh stays local-only
                db["empbranches"] = [b for b in db["empbranches"] if b[0] != e.emp_id]
                branches_log.append(e.emp_id)
            action = "UPDATE"
            for r in db["employees"]:
                if r["id"] == e.emp_id:
                    r.update(name=e.name, salary=e.salary)
        else:                                              # legacy download of existing row
            action = "EXECUTE_SELECT_COUNT_AS_NOOP"        # the SELECT text ran; nothing changed
    return True


seed = {"employees": [{"id": 5, "name": "old", "salary": 100.0}], "empbranches": [(5, 1)]}
log = []
save_employee("legacy", dict(seed, employees=[dict(r) for r in seed["employees"]]),
              [Emp(5, "fresh", 250.0)], added_locally=False, branches_log=log)
db_l = {"employees": [dict(r) for r in seed["employees"]], "empbranches": list(seed["empbranches"])}
save_employee("legacy", db_l, [Emp(5, "fresh", 250.0)], False, [])
check("A1 legacy download of an existing employee changed nothing (bug reproduced)",
      db_l["employees"][0]["name"] == "old" and db_l["employees"][0]["salary"] == 100.0)
db_f = {"employees": [dict(r) for r in seed["employees"]], "empbranches": list(seed["empbranches"])}
save_employee("fixed", db_f, [Emp(5, "fresh", 250.0)], False, [])
check("A2 repaired download lands the UPDATE",
      db_f["employees"][0]["name"] == "fresh" and db_f["employees"][0]["salary"] == 250.0 and
      db_f["empbranches"] == [(5, 1)])          # branch links untouched on download
db_a = {"employees": [], "empbranches": []}
for mode in ("legacy", "fixed"):
    d = {"employees": [], "empbranches": []}
    logx = []
    save_employee(mode, d, [Emp(9, "new", 300.0)], True, logx)
    db_a[mode] = (d, logx)
check("A3 brand-new local employee inserts identically under both rules (no branch churn on insert)",
      db_a["legacy"][0] == db_a["fixed"][0] and db_a["legacy"][1] == db_a["fixed"][1] == [])

m = ENT.split("public bool SaveEmployee")[1].split("public List<Employee> ReadEmployee()")[0]
updates = re.findall(r'sqlCommand = new SqlCommand\("update Employees set [^\n]+', m)
check("A4 existing-row else-branch now carries the UPDATE, byte-identical to the local-edit copy",
      len(updates) == 2 and updates[0] == updates[1] and "else\n                {" in m and
      "Repair R-053" in m)

print("Part B: R-054 / P5-029 - sync reports what happened")


def sync_invoice_model(rules, posted_ok, entry_throws=False):
    """returns the bool the caller receives; models the method tail exactly."""
    synced_list = ["inv1"] if posted_ok else []
    for _ in synced_list:
        pass                                                # update Inv set Sync=1
    if rules == "legacy":
        _ = entry_throws                                    # fire-and-forget: outcome unseen
        return False                                        # default(bool), never touched
    invoice_synced = len(synced_list) > 0
    try:
        if entry_throws:
            raise RuntimeError("journal transport down")
    except Exception:
        pass                                                # ProjectData journal, no rethrow
    return invoice_synced


check("B1 legacy reported failure even after marking the invoice synced (bug reproduced)",
      sync_invoice_model("legacy", posted_ok=True) is False)
check("B2 repaired success path reports true", sync_invoice_model("fixed", True) is True)
check("B3 repaired rejection stays honestly false", sync_invoice_model("fixed", False) is False)
check("B4 journal failure is absorbed without corrupting the invoice verdict",
      sync_invoice_model("fixed", True, entry_throws=True) is True)


def send_last_code(rules, http_status):
    threw = http_status is None
    if threw:
        return False                                        # catch arm, unchanged
    if rules == "legacy":
        return True                                         # any non-throwing response
    return 200 <= http_status < 300                         # IsSuccessStatusCode


check("B5 legacy counted a 500 as delivery success (bug); repaired rejects it",
      send_last_code("legacy", 500) is True and send_last_code("fixed", 500) is False)
check("B6 repaired 200 still succeeds and thrown transport still fails",
      send_last_code("fixed", 200) is True and send_last_code("fixed", None) is False)

for name, src in (("InvoiceOper", INVOP), ("InvoiceOperContract", CONTRACT)):
    tail = src.split("SyncInvoice(Invoice inv, Entry Eny, bool IsNew)")[1][:6000]
    check("B7 %s awaits the journal sync and returns the honest flag" % name,
          "await entryOper.SyncEntry(Eny, IsNew);" in tail and
          "return invoiceSynced;" in tail and
          "entryOper.SyncEntry(Eny, IsNew);\n\t\t\treturn result;" not in src)
send_block = SYNC.split("api/Customers/set-last-customers")
check("B8 SendLastCodeToApiAsync gates success on the HTTP status",
      len(send_block) == 2 and                                    # the endpoint literal appears exactly once
      "var httpResponse = await httpClient.PostAsync(" in send_block[0][-400:] + send_block[1] and
      "if (!httpResponse.IsSuccessStatusCode)" in send_block[1])

print("Part C: R-055 / P5-022 - the customer batch echoes exactly once")


def save_customers(rules, customers, abort_after=None):
    """returns (result, echo_count, echoed_sizes) mirroring SaveCustomer control flow."""
    echoes = []
    processed = 0
    for c in customers:
        if c is None:
            if rules == "legacy":
                echoes.append(len(customers))               # old label: echo, then next row
            continue
        if abort_after is not None and processed == abort_after:
            return False, echoes                            # goto end_IL_0009 path
        processed += 1
        if rules == "legacy":
            echoes.append(len(customers))                   # per-row echo inside the loop
    if rules == "fixed":
        echoes.append(len(customers))                       # single post-loop echo
    return True, echoes


ok_l, echoes_l = save_customers("legacy", ["a", "b", "c"])
check("C1 legacy echoed the full payload once per row (bug reproduced)",
      ok_l is True and echoes_l == [3, 3, 3])
ok_f, echoes_f = save_customers("fixed", ["a", "b", "c"])
check("C2 repaired run echoes exactly once, same payload",
      ok_f is True and echoes_f == [3])
_, echoes_nl = save_customers("legacy", ["a", None, "b"])
check("C3 legacy even echoed after null rows; repaired sends a single payload regardless",
      echoes_nl == [3, 3, 3] and save_customers("fixed", ["a", None, "b"])[1] == [3])
abort_l = save_customers("legacy", ["a", "b", "c"], abort_after=1)
abort_f = save_customers("fixed", ["a", "b", "c"], abort_after=1)
check("C4 aborted runs: legacy leaked partial echoes, repaired sends none, both report false",
      abort_l == (False, [3]) and abort_f == (False, []))

m2 = ENT.split("public bool SaveCustomer")[1]
m2 = m2[: m2.index("catch (Exception projectError)")]
check("C5 echo statement survives exactly once, after the loop, with the label retired",
      m2.count("new CustomerCRUD(Sync.APIUrl).AddCustomer(customers);") == 1 and
      "IL_0b02" not in m2 and "goto end_IL_0009;" in m2 and
      len(re.findall(r'\bcontinue;', m2)) >= 5 and "Repair R-055" in m2)

print("Part D: R-056 / P5-013 - grants reset once per distinct employee")


def apply_permissions(conn, rows, rules):
    cur = conn.cursor()
    if rules == "legacy":
        for r in rows:                                      # reset PER incoming row
            cur.execute("DELETE FROM OperationPermission WHERE OperNo>7 AND emp=?", (r["emp"],))
            cur.execute("UPDATE OperationPermission SET Activated=0 WHERE emp=?", (r["emp"],))
            cur.execute("INSERT INTO OperationPermission(emp,OperNo,OperVal,Activated) VALUES(?,?,?,?)",
                        (r["emp"], r["op"], r["val"], r["act"]))
    else:
        seen = []
        for r in rows:                                      # reset ONCE per distinct emp
            if r["emp"] not in seen:
                seen.append(r["emp"])
                cur.execute("DELETE FROM OperationPermission WHERE OperNo>7 AND emp=?", (r["emp"],))
                cur.execute("UPDATE OperationPermission SET Activated=0 WHERE emp=?", (r["emp"],))
        for r in rows:
            cur.execute("INSERT INTO OperationPermission(emp,OperNo,OperVal,Activated) VALUES(?,?,?,?)",
                        (r["emp"], r["op"], r["val"], r["act"]))
    conn.commit()


SCHEMA = "CREATE TABLE OperationPermission(id INTEGER PRIMARY KEY, emp INT, OperNo INT, OperVal TEXT, Activated INT)"
payload = [
    {"emp": 1, "op": 8, "val": "v8", "act": 1},
    {"emp": 1, "op": 9, "val": "v9", "act": 1},
    {"emp": 2, "op": 8, "val": "w8", "act": 0},
]
conn_l = sqlite3.connect(":memory:")
conn_l.execute(SCHEMA)
conn_l.execute("INSERT INTO OperationPermission(emp,OperNo,OperVal,Activated) VALUES(1,3,'keep-me',1)")
conn_l.commit()
apply_permissions(conn_l, payload, "legacy")
left_l = sorted(conn_l.execute("SELECT emp,OperNo,Activated FROM OperationPermission").fetchall())
check("D1 legacy kept only the FINAL payload row per employee (earlier siblings erased - bug)",
      left_l == [(1, 3, 0), (1, 9, 1), (2, 8, 0)], str(left_l))
conn_f = sqlite3.connect(":memory:")
conn_f.execute(SCHEMA)
conn_f.execute("INSERT INTO OperationPermission(emp,OperNo,OperVal,Activated) VALUES(1,3,'keep-me',1)")
conn_f.commit()
apply_permissions(conn_f, payload, "fixed")
left_f = sorted(conn_f.execute("SELECT emp,OperNo,Activated FROM OperationPermission").fetchall())
check("D2 repaired keeps every payload row, deactivating/stripping only what the reset defines",
      left_f == [(1, 3, 0), (1, 8, 1), (1, 9, 1), (2, 8, 0)], str(left_f))

pm = RECVD.split("private static void InsertOperPrimisson")[1]
pm = pm[: pm.index("catch (Exception projectError)")]
_parts = pm.split("foreach (ListOperationPermission permissions in permissionsList)")
assert len(_parts) == 2, "expected exactly one per-row insert loop"
reset_loop, insert_loop = _parts
check("D3 reset iterates distinct employees ahead of a separate pure-insert loop",
      "permissionsList.Select(p => p.emp).Distinct().ToList()" in pm and
      "delete from OperationPermission" not in insert_loop and
      "delete from OperationPermission" in reset_loop and
      reset_loop.count("ExecuteNonQuery();") == 2 and "Repair R-056" in pm)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - downloads update, sync reports honestly, batches echo once,")
print("and permission payloads stop erasing their own earlier rows.")
sys.exit(0)
