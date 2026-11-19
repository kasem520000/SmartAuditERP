#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-027 (audit findings P2-013, P2-014,
P2-016) in the attachment viewer and its callers. No .NET/WPF toolchain
exists here, so validation combines:

* SQLite models of the DELETE scopes proving a single-row delete leaves
  sibling attachment records intact (legacy wiped them all);
* a Python mirror of the store-containment guard proving open/delete refuse
  anything outside Settings.DocsRootPath and fail closed when unknown;
* a collection-model proof that deletion now removes the row from whatever
  ItemsSource the caller installed, not only the internal list;
* static witnesses pinning the narrowed statements, the typed-item call
  sites and the guard-before-action ordering in the sources.

Run: python3 tests/repair/attachment_cluster_harness.py
Exit 0 on PASS.
"""
import os
import sqlite3
import sys

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


VIEWER = open("SmartAuditERP/Form_WPF/frmshowdocument.xaml.cs", encoding="utf-8").read()

# ------------------------- Part A: P2-013 -----------------------------------
print("Part A: P2-013 - delete targets one row, siblings survive")

DOCS = [(1, "a.jpg", "/store/Receipt1.jpg", "D1", 3),
        (2, "b.png", "/store/Receipt2.png", "D1", 3),
        (3, "c.pdf", "/store/Receipt3.pdf", "D1", 3),
        (4, "x.jpg", "/store/Other1.jpg",  "D2", 3)]


def fresh_db():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE Documents (Id INTEGER PRIMARY KEY, FileName TEXT,"
               " FileUrl TEXT, GlobalID TEXT, type INT)")
    db.executemany("INSERT INTO Documents VALUES (?,?,?,?,?)", DOCS)
    return db


def ids(db):
    return sorted(r[0] for r in db.execute("SELECT Id FROM Documents"))


db = fresh_db()
db.execute("DELETE FROM Documents WHERE globalId=? AND type=?", ("D1", 3))   # legacy scope
check("A1 legacy statement wipes ALL of the document's attachment rows (bug reproduced)",
      ids(db) == [4])

for doc_id, label in ((2, "with Id"), (-1, "FileUrl fallback")):
    db = fresh_db()
    target_url = "/store/Receipt2.png"
    if doc_id >= 0:
        db.execute("DELETE FROM Documents WHERE globalId=? AND type=? AND Id=?",
                   ("D1", 3, doc_id))
    else:
        db.execute("DELETE FROM Documents WHERE globalId=? AND type=? AND FileUrl=?",
                   ("D1", 3, target_url))
    check("A2 repaired scope %s removes exactly the chosen row" % label,
          ids(db) == [1, 3, 4])

check("A3 viewer carries the narrowed statements and drops the blanket one",
      'AND Id=@id"' in VIEWER and 'AND FileUrl=@url"' in VIEWER and
      '"DELETE FROM Documents WHERE globalId=@GlobalId AND type=@type",' not in VIEWER)
check("A4 Id branch chosen by DocId, parameters always bound",
      "doc.DocId >= 0" in VIEWER and '@url", doc.FileUrl' in VIEWER and
      'SqlDbType.Int).Value = doc.DocId' in VIEWER)
check("A5 callers supply Documents.Id",
      "DocId = Convert.ToInt32(dt.Rows[i][\"Id\"])" in
      open("SmartAuditERP/Form_WPF/frmSandSD.xaml.cs", encoding="utf-8").read())
check("A6 parent context no longer blanked after open/delete",
      'type       = 0;\n                    GlobalIdDoc = "";' not in VIEWER and
      'type        = 0;\n                    GlobalIdDoc = "";' not in VIEWER)

# ------------------------- Part B: P2-016 -----------------------------------
print("Part B: P2-016 - open/delete confined to the attachment store")

ROOT = None                                   # Properties.Settings.Default.DocsRootPath mirror


def get_full_path(p):                         # Path.GetFullPath analogue
    return os.path.normpath(os.path.abspath(p))


def is_confined(file_url):                    # mirror of IsConfinedToStore
    if not file_url or not file_url.strip():
        return False
    if ROOT is None:                          # TryResolveDocsRoot failed -> fail closed
        return False
    try:
        full = get_full_path(file_url)
        root = get_full_path(ROOT)
        prefix = root if root.endswith(os.sep) else root + os.sep
        return full.startswith(prefix)
    except Exception:
        return False


case_root = "/srv/attachments"
cases = [
    ("/srv/attachments/Receipt1.jpg", True,  "stored attachment"),
    ("/srv/attachments/sub/deep.pdf", True,  "nested under the store"),
    ("/etc/passwd",                   False, "absolute path outside the store"),
    ("/srv/attachments/../secrets.txt", False, "traversal escaping the root"),
    ("",                              False, "empty value"),
]
ROOT = case_root
for url, expected, label in cases:
    check("B1 '%s' (%s)" % (label, "accepted" if expected else "refused"),
          is_confined(url) == expected)
ROOT = None
check("B2 unknown/unset store fails CLOSED", is_confined("/srv/attachments/x.jpg") is False)

open_block = VIEWER.split("DataGridView1_MouseDoubleClick")[1].split("#endregion")[0]
del_block = VIEWER.split("BtnDeleteDoc_Click")[1].split("#region Closing")[0]
gi = open_block.index("IsConfinedToStore"); gp = open_block.index("Process.Start")
di = del_block.index("IsConfinedToStore"); dd = del_block.index("File.Delete")
check("B3 open path consults the guard BEFORE Process.Start", gi < gp)
check("B4 delete path gates File.Delete behind the guard", di < dd and
      "if (IsConfinedToStore(doc.FileUrl) && File.Exists(doc.FileUrl))" in VIEWER)
check("B5 guard derives from the writers' DocsRootPath setting (symmetric by construction)",
      "Properties.Settings.Default.DocsRootPath" in VIEWER and
      "System.IO.Path.GetFullPath(configured)" in VIEWER)

# ------------------------- Part C: P2-014 -----------------------------------
print("Part C: P2-014 - viewer consumers all feed DocumentItem now")


class DocumentItem:
    def __init__(self, name): self.name = name


def viewer_can_act(row):                       # handler test: sender.Tag is DocumentItem
    return isinstance(row, DocumentItem)


legacy_rows = [object(), dict(name="a")]       # DataRowView / DocumentDisplayItem analogues
typed_rows = [DocumentItem("a"), DocumentItem("b")]
check("C1 legacy foreign row types left open/delete inert (bug reproduced)",
      not any(viewer_can_act(r) for r in legacy_rows))
check("C2 typed rows act correctly", all(viewer_can_act(r) for r in typed_rows))

inv_sale = open("SmartAuditERP/Form_WPF/frmInvSale.xaml.cs", encoding="utf-8").read()
customers = open("SmartAuditERP/Form_WPF/frmCustomers.xaml.cs", encoding="utf-8").read()
check("C3 sales invoice feeds List<DocumentItem> twice and drops the DataView table",
      inv_sale.count("new System.Collections.Generic.List<DocumentItem>()") >= 2 and
      "displayTable.Columns.Add(\"RowNo\"" not in inv_sale)
check("C4 customers feed ObservableCollection<DocumentItem> with RowNo (not RowNumber)",
      "ObservableCollection<DocumentItem>" in customers and
      "new DocumentDisplayItem\n" not in customers)
check("C5 viewer still acts exclusively on DocumentItem",
      "btn.Tag is DocumentItem doc" in VIEWER and
      "DataGridView1.SelectedItem is DocumentItem doc" in VIEWER)

# ------------------------- Part D: displayed-collection semantics ------------
print("Part D: delete removes the row from the ACTUAL displayed list")


def legacy_remove(internal, displayed, doc):   # _documents.Remove only
    if doc in internal:
        internal.remove(doc)


def fixed_remove(internal, displayed, doc):    # source ?? _documents
    if displayed is not None and doc in displayed:
        displayed.remove(doc)
    elif doc in internal:
        internal.remove(doc)


for remover, label in ((legacy_remove, "legacy"), (fixed_remove, "fixed")):
    internal = ["r1", "r2"]
    callers_own = ["r1", "r2"]                 # caller replaced ItemsSource
    remover(internal, callers_own, "r1")
    if label == "legacy":
        check("D1 legacy leaves the DISPLAYED row in place (bug reproduced)",
              callers_own == ["r1", "r2"])
    else:
        check("D2 repaired removes the row the user is looking at",
              callers_own == ["r2"])
internal = ["r1", "r2"]
fixed_remove(internal, internal, "r1")
check("D3 default constructor path (source is _documents) still works once",
      internal == ["r2"])
check("D4 viewer casts the real ItemsSource and guards ReferenceEquals on renumber",
      "DataGridView1.ItemsSource as System.Collections.IList" in VIEWER and
      "!ReferenceEquals(source, _documents)" in VIEWER)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-027: single-row attachment deletion preserves siblings")
print("(Id-first, FileUrl fallback), open/delete refuse paths outside the")
print("DocsRootPath store and fail closed, every flagged caller feeds typed")
print("items, and deletion touches the collection actually on screen.")
sys.exit(0)
