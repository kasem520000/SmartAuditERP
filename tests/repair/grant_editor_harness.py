#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-028 (audit finding P2-004) and
R-029 (P2-007). No .NET/WPF toolchain exists here, so both repairs are
validated with SQLite models of the exact data flows plus static witnesses.

Part A reproduces the grant-editor accumulation: loading employee A then B
in one window used to merge A's checks into B's model, and a failed load
left that merged state saveable. The repaired rules reset the tree per
switch, apply grants over a clean slate, certify successful loads only, and
refuse to persist uncertified state. Fully successful single-user editing is
shown identical pre/post fix.

Part B reproduces the identity mix-ups: opening the permissions editor from
a users-grid row passed Users.id where the combo expects the employee link,
and the edit-mode uniqueness check excluded by emp while holding a Users id,
so saving an unrenamed record always tripped a phantom duplicate.

Run: python3 tests/repair/grant_editor_harness.py
Exit 0 on PASS.
"""
import sqlite3
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


PERMS = open("SmartAuditERP/Form_WPF/frmUsersPermissions.xaml.cs", encoding="utf-8").read()
ADDU  = open("SmartAuditERP/Form_WPF/frmAddUsers.xaml.cs", encoding="utf-8").read()

# ------------------------- Part A: P2-004 -----------------------------------
print("Part A: R-028 / P2-004 - no cross-employee grant accumulation")

FORMS = ["F1", "F2", "F3"]
A_GRANTS = {"F1"}                     # employee A keeps exactly F1


def fresh_db():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE User_Permissions (user_id INT, Form_id TEXT)")
    db.executemany("INSERT INTO User_Permissions VALUES (?,?)",
                   [(1, f) for f in A_GRANTS])          # A persisted
    return db                                           # B has no rows


class EditorModel:
    """tree checkbox state + save pipeline under legacy vs repaired rules."""

    def __init__(self, rules):
        self.rules = rules
        self.tree = {f: False for f in FORMS}
        self.certified = rules == "legacy"              # legacy never gates on this

    def select_employee(self, db, emp_id, fail_load=False):
        if self.rules == "fixed":
            self.tree = {f: False for f in FORMS}       # ClearTreeCheckboxes on switch
            self.certified = False
        if fail_load:
            if self.rules == "fixed":
                self.certified = False                  # catch marks uncertified
            return                                       # legacy: empty catch, state untouched
        rows = [r[0] for r in db.execute(
            "SELECT Form_id FROM User_Permissions WHERE user_id=?", (emp_id,))]
        for f in rows:
            self.tree[f] = True                          # grants only ever add checks
        if self.rules == "fixed":
            self.certified = True

    def save(self, db, emp_id):
        if self.rules == "fixed" and not self.certified:
            return "refused"                             # uncertified => refuse
        db.execute("BEGIN")
        db.execute("DELETE FROM User_Permissions WHERE user_id=?", (emp_id,))
        db.executemany("INSERT INTO User_Permissions VALUES (?,?)",
                       [(emp_id, f) for f, c in self.tree.items() if c])
        db.commit()
        return "saved"


for rules in ("legacy", "fixed"):
    db = fresh_db()
    ed = EditorModel(rules)
    ed.select_employee(db, 1)        # load A (grants F1)
    ed.select_employee(db, 2)        # switch to B (no grants), no manual edits
    res = ed.save(db, 2)             # save as-is
    stored = sorted(r[0] for r in db.execute(
        "SELECT Form_id FROM User_Permissions WHERE user_id=2"))
    if rules == "legacy":
        check("A1 legacy re-saved employee A's grants onto B (bug reproduced)",
              res == "saved" and stored == ["F1"])
    else:
        check("A2 repaired A->B->save leaves B with exactly its own (zero) grants",
              res == "saved" and stored == [])

db = fresh_db()
ed = EditorModel("fixed")
ed.select_employee(db, 1)
ok = ed.save(db, 1)
check("A3 saving A after its own clean load still persists A's grants unchanged",
      ok == "saved" and sorted(r[0] for r in db.execute(
          "SELECT Form_id FROM User_Permissions WHERE user_id=1")) == ["F1"])

db = fresh_db()
ed = EditorModel("fixed")
ed.select_employee(db, 1)
ed.select_employee(db, 2, fail_load=True)
check("A4 certified flag drops when the load query fails", not ed.certified)
res = ed.save(db, 2)
stored = list(db.execute("SELECT * FROM User_Permissions WHERE user_id=2"))
check("A5 save refused while uncertified and nothing written (acceptance P2T-06)",
      res == "refused" and stored == [])

check("A6 source clears the tree on employee switch",
      "ClearTreeCheckboxes(treeView1.Items);\n                _treeLoadedForCurrentEmp = false;"
      in PERMS)
check("A7 load certifies success and fails loudly otherwise",
      "_treeLoadedForCurrentEmp = true;" in PERMS and
      "catch { }" not in PERMS.split("LoadUserPermissions")[1].split("FindTreeNode")[0])
check("A8 SaveFormsPermission gates on certification before writing",
      "if (!_treeLoadedForCurrentEmp)" in PERMS and
      PERMS.index("if (!_treeLoadedForCurrentEmp)") <
      PERMS.index('DELETE FROM User_Permissions WHERE user_id='))

# ------------------------- Part B: P2-007 -----------------------------------
print("Part B: R-029 / P2-007 - user record id vs employee link kept apart")

db = sqlite3.connect(":memory:", isolation_level=None)
db.execute("CREATE TABLE Users (id INT, emp INT, username TEXT, IS_Deleted INT)")
# deliberately diverging identities: user rec 5 -> employee 9; user rec 9 -> employee 2
db.executemany("INSERT INTO Users VALUES (?,?,?,0)",
               [(5, 9, "alice"), (9, 2, "bob"), (11, 7, "carol")])
EMPLOYEES = {2: "m2", 7: "m7", 9: "m9"}        # Employees.id -> name


def editor_selection(rules, userid, empid):
    value = userid if rules == "legacy" else empid
    # the editor combo resolves SelectedValue against Users.emp (SelectedValuePath="emp")
    hit = [e for e in EMPLOYEES if e == value]
    return hit[0] if hit else None


row_alice = dict(userid=5, empid=9)
check("B1 legacy opens the editor for the WRONG/absent employee (bug reproduced)",
      editor_selection("legacy", **row_alice) is None or
      editor_selection("legacy", **row_alice) != row_alice["empid"])
check("B2 repaired selection lands on alice's actual employee record",
      editor_selection("fixed", **row_alice) == 9)


def rename_blocked(db, code, username, rules):
    col = "emp" if rules == "legacy" else "id"           # exclusion column
    rows = db.execute(
        f"SELECT id FROM Users WHERE {col}<>? AND username=? AND IS_Deleted=0",
        (code, username)).fetchall()
    return len(rows) > 0


# editing alice (Code = Users.id = 5) WITHOUT renaming must be allowed
check("B3 legacy flags the edited record itself as duplicate (bug reproduced)",
      rename_blocked(db, 5, "alice", "legacy") is True)
check("B4 repaired check excludes self: unrenamed save proceeds",
      rename_blocked(db, 5, "alice", "fixed") is False)
# genuine duplicates must still be caught by both predicates
check("B5 real duplicate names remain blocked post-fix",
      rename_blocked(db, 11, "alice", "fixed") is True)
check("B6 exclusion column corrected from emp to the actual primary key",
      "where emp<>@code" not in ADDU and "where id<>@code and username=@username" in ADDU)

check("B7 editor opener passes the employee link, not the Users id",
      "frm.cmbEmp.SelectedValue = row.empid;" in ADDU and
      "frm.cmbEmp.SelectedValue = row.userid;" not in ADDU)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-028 (P2-004): switching employees starts from a clean,")
print("certified grant model and uncertified state can never be saved;")
print("R-029 (P2-007): the permissions editor targets the correct employee and")
print("the edit-time uniqueness check excludes by the record's own key.")
sys.exit(0)
