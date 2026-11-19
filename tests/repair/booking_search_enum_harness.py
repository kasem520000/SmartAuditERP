#!/usr/bin/env python3
"""
Repair R-003 verification harness (audit finding P7-025).

Models the enumeration semantics of
SmartAuditERP/Form_WPF/frmBookingM.xaml.cs::btnSearch_Click.

Defect: the two foreach loops enumerate the LIVE ObservableCollection
_dgvSrchList, while their body calls Search(3) -> LoadDG which does
_dgvSrchList.Clear() and refills it -- mutating the collection mid-enumeration.
.NET's List/ObservableCollection enumerators are FAIL-FAST: they capture a
version at GetEnumerator and throw InvalidOperationException on the next
MoveNext once the collection's version changes.

Fix: enumerate a SNAPSHOT copy of the collection and stop at the first matching
customer, so the underlying list can be rebuilt by Search(3) without invalidating
the active enumerator.

Scope/limits (Rule 9): verifies the control-flow / enumeration-semantics logic
only (verified-in-scope). The real WPF/DataGrid/ADO.NET path cannot run here.

Usage: python3 tests/repair/booking_search_enum_harness.py
Exit 0 on success, 1 otherwise.
"""
import sys


class EnumModifiedError(RuntimeError):
    """Analog of .NET InvalidOperationException 'Collection was modified'."""


class BookingItem:
    __slots__ = ("name", "id", "mobile")

    def __init__(self, name, bid, mobile):
        self.name = name
        self.id = bid
        self.mobile = mobile

    def __repr__(self):
        return f"<{self.name},{self.id},{self.mobile}>"


class FailFastCollection:
    """Mimics a .NET ObservableCollection fail-fast enumerator via a version tag."""

    def __init__(self):
        self._items = []
        self._version = 0

    def clear(self):
        self._items.clear()
        self._version += 1

    def add(self, item):
        self._items.append(item)
        self._version += 1

    def snapshot(self):
        return list(self._items)          # independent shallow copy

    def items(self):
        return list(self._items)

    def __iter__(self):
        return _FailFastEnumerator(self)

    def __len__(self):
        return len(self._items)


class _FailFastEnumerator:
    def __init__(self, col):
        self._col = col
        self._version = col._version      # captured at enumeration start
        self._index = 0

    def __next__(self):
        # Fail fast: any structural mutation since enumeration began => throw.
        if self._col._version != self._version:
            raise EnumModifiedError(
                "Collection was modified; enumeration operation may not execute.")
        if self._index >= len(self._col._items):
            raise StopIteration
        item = self._col._items[self._index]
        self._index += 1
        return item


DATASET = [
    BookingItem("Khalid", 10, "0500000000"),
    BookingItem("Ali",    11, "0501111111"),
    BookingItem("Sara",   12, "0502222222"),
]


def make_world():
    world = {
        "srch": FailFastCollection(),
        "ClientN": None,
        "search3_calls": 0,
    }

    def search(kind):
        if kind == 2:
            world["srch"].clear()
            for row in DATASET:
                world["srch"].add(row)
        elif kind == 3:                       # refined by selected customer id
            cid = world["ClientN"]
            rows = [r for r in DATASET if r.id == cid]
            world["srch"].clear()
            for r in rows:
                world["srch"].add(r)
            world["search3_calls"] += 1

    world["search"] = search
    return world


def click_original(world, name=None, phone=None):
    search = world["search"]; srch = world["srch"]
    search(2)
    if name:
        for item in srch:                     # enumerates the LIVE collection
            if item.name == name:
                world["ClientN"] = item.id
                search(3)                     # mutates srch mid-foreach
    if phone:
        for item in srch:
            if item.mobile == phone:
                world["ClientN"] = item.id
                search(3)


def click_fixed(world, name=None, phone=None):
    search = world["search"]; srch = world["srch"]
    search(2)
    if name:
        name_snapshot = srch.snapshot()       # independent copy
        for item in name_snapshot:
            if item.name == name:
                world["ClientN"] = item.id
                search(3)
                break                          # stop once refined
    if phone:
        phone_snapshot = srch.snapshot()
        for item in phone_snapshot:
            if item.mobile == phone:
                world["ClientN"] = item.id
                search(3)
                break


def main():
    ok = True

    # --- Part A: original behaviour fails fast when a match triggers Search(3) ---
    w = make_world()
    crashed = False
    try:
        click_original(w, name="Ali")
    except EnumModifiedError as ex:
        crashed = True
        print("[A] PRE-FIX : foreach over live collection -> raised:", str(ex))
    if not crashed:
        print("[A] ! PRE-FIX did not surface the mid-enumeration fault"); ok = False

    # No-match case must not crash (it never mutated the collection).
    w0 = make_world()
    try:
        click_original(w0, name="NobodyMatches")
        print("[A] PRE-FIX no-match path completes (no mutation) -> OK")
    except EnumModifiedError:
        print("[A] ! unexpected crash on no-match path"); ok = False

    # --- Part B: fixed behaviour completes, refines once, picks correct customer ---
    wf = make_world()
    try:
        click_fixed(wf, name="Ali")
    except EnumModifiedError as ex:
        print("[B] ! POST-FIX still raised:", str(ex)); ok = False
    else:
        final_ids = [r.id for r in wf["srch"].items()]
        print("[B] POST-FIX name='Ali' -> ClientN =", wf["ClientN"],
              "| Search(3) calls =", wf["search3_calls"],
              "| refined list ids =", final_ids)
        if wf["ClientN"] != 11:
            print("    ! wrong customer selected"); ok = False
        if wf["search3_calls"] != 1:
            print("    ! expected exactly one refinement"); ok = False
        if final_ids != [11]:
            print("    ! refined list should hold only the matched customer"); ok = False

    # Phone path too.
    wp = make_world()
    try:
        click_fixed(wp, phone="0502222222")
    except EnumModifiedError as ex:
        print("[B] ! POST-FIX phone path raised:", str(ex)); ok = False
    else:
        print("[B] POST-FIX phone='0502222222' -> ClientN =", wp["ClientN"],
              "| Search(3) calls =", wp["search3_calls"])
        if wp["ClientN"] != 12 or wp["search3_calls"] != 1:
            print("    ! phone refinement incorrect"); ok = False

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
