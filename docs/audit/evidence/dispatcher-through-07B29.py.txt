#!/usr/bin/env python3
"""Read-only consistency through PARTIAL7B29/R4m; NEVER ERP acceptance.

Actual CLI B29/current331; historical B28 OWN330/raw331CRLF/indexes/ALL48
in explicit presetB28 child with suite-local A.52B27/48B26/44B25/44B24 and all
older OWN cases retained. API main defaultB15 is distinct. Protect829/all330
exact dictionaries/ALLnext_phase/evidence/raw331CRLFprefix/G232/827 originals/
three freezes and complete RS14/SP3 ancestry/input-prefix/routes/disposition.
One Medium source-local159: accepted invoice search in sale/purchase bypasses
existing CheckBeforeClear and Navigate clears/replaces editor before reader.
Supplied dirty flags/UI-count and normal CLR completion ONLY;fresh not-done/
sentinel/guardNo/Yes/clean controls. No WPF schedule, dirty propagation, DTO
constructor, provider behavior, GC/all-references or saved loss inferred.
Seven old paths/22 slices/whole0;union426/complement401 not coverage percent,
all callers/reader/fields/477bodies/455FE or whole7B.330metadata/80pathmatches
plus selected nearest bodies/chains,not all330bodies.16FE/INV/32plans NOT
executed.014/132/145potential and020/021 financial/ACL/stock/save/production
barriers retained.015/046/061/091/148/151/155–158 not recounted;no new extension.
Actual34 historical subprocess summaries/identities with capture-time tools,
not full streams or final/postpush wholesale replay. Single later pin is
reversed in memory for identity proof,not used to overwrite captured hashes.
No protected edit/skip/globalPath/sharedsubprocess mutation/diskoverlay/
rebaseline/archive rewrite. Session date2026-11-16 and raw observed clock
separate;source10ba/officialB28capture436/deliveredB28entrydda not relabelled.
B10 additive10vs120/equality1=10/protectedG138 retained. No ERP/build/C#/VB/
WPF/.NET/SQL/DataView/provider/SDK/ToDataTable/REPX/scanner/printer/business-data/
secrets/remediation/measurement/acceptance execution. Independent repair start/
sync unknown,no repair→audit.7B/7partial,R4n/B30proposed,7Cunstarted,8unauthorized;
next_phase8 is planning only,not permission or a duration/session promise.
"""
from __future__ import annotations

import argparse
import ast
import collections
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs/audit"
HEAD = "10ba215152f722c8808aea0bb672c1d1d4d9d711"
BRANCH = "arena/94ae8414-smartauditerp"
ERRORS: list[str] = []
LINES: dict[str, list[str]] = {}
REFERENCE_COUNT = 0
LINK_COUNT = 0


def check(ok: bool, message: str) -> None:
    if not ok:
        ERRORS.append(message)


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> str:
    data = path.read_bytes()
    try:
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        # Read-only fallback; not the compiler's intended codepage certification.
        return data.decode("cp1256", errors="replace")


def rows(relative: str) -> list[dict[str, str]]:
    with (AUDIT / relative).open(encoding="utf-8", newline="") as stream:
        result = list(csv.DictReader(stream))
    for index, row in enumerate(result, 2):
        check(None not in row and all(v is not None for v in row.values()),
              f"Malformed CSV row {relative}:{index}")
    return result


def spans(value: str) -> list[tuple[int, int]]:
    result = []
    for part in re.split(r"[;,،]", value):
        match = re.fullmatch(r"\s*(\d+)(?:[-–](\d+))?\s*", part)
        if not match:
            raise ValueError(f"Malformed source range: {value}")
        result.append((int(match[1]), int(match[2] or match[1])))
    return result


def source_ref(path: str, value: str, location: str) -> None:
    global REFERENCE_COUNT
    file = ROOT / path
    check(file.is_file(), f"Missing source file in {location}: {path}")
    if not file.is_file():
        return
    if path not in LINES:
        LINES[path] = read(file).splitlines()
    for start, end in spans(value):
        REFERENCE_COUNT += 1
        check(1 <= start <= end <= len(LINES[path]),
              f"Out-of-bounds reference in {location}: {path}:{start}-{end}")


def evidence(value: str, location: str) -> None:
    """Explicit source paths and historical same-file abbreviated ranges."""
    last = None
    for part in value.split(";"):
        part = part.strip()
        if not part:
            continue
        if ":" in part:
            path, ranges = part.rsplit(":", 1)
            source_ref(path, ranges, location)
            last = path
        elif re.fullmatch(r"\d+(?:[-–]\d+)?", part):
            check(last is not None, f"Range without source path in {location}: {part}")
            if last:
                source_ref(last, part, location)
        else:
            # Historical P1-006 intentionally cites directories and inventory.
            check((ROOT / part).exists() or (AUDIT / part).exists(),
                  f"Missing path-only evidence in {location}: {part}")
            last = None


def scoped_evidence(value: str, scope: dict[str, list[tuple[int, int]]], location: str, phase: int = 4) -> None:
    """Explicit source citations must fit their phase's selected ranges.

    This is range inclusion only, not proof of reading depth or trace semantics.
    Bounds/existence have already been checked by evidence().
    """
    for part in value.split(";"):
        if not part.strip():
            continue
        path, value_range = part.strip().rsplit(":", 1)
        check(path in scope, f"P{phase} evidence path outside declared scope in {location}: {path}")
        for start, end in spans(value_range):
            check(any(a <= start <= end <= b for a, b in scope.get(path, [])),
                  f"P{phase} evidence range outside selected scope in {location}: {part}")


def sequential(data: list[dict], prefix: str, count: int, width: int = 2) -> None:
    expected = [f"{prefix}{n:0{width}d}" for n in range(1, count + 1)]
    check([r["id"] for r in data] == expected, f"Unexpected IDs/order: {prefix}")


def related(data: list[dict], known: set[str], field: str = "finding_ids") -> None:
    for row in data:
        values = row.get(field, "")
        if isinstance(values, str):
            values = values.split(";")
        for value in values:
            if value:
                check(value in known, f"Unknown {field} in {row['id']}: {value}")


def validate_evidence_rows(data: list[dict]) -> None:
    for row in data:
        for key in ("evidence", "source_evidence", "sink_evidence"):
            if key in row:
                evidence(row[key], row["id"])


def distributions(data: list[dict], severity: dict, certainty: dict, label: str) -> None:
    check(dict(collections.Counter(r["severity"] for r in data)) == severity,
          f"Severity distribution mismatch: {label}")
    check(dict(collections.Counter(r["certainty"] for r in data)) == certainty,
          f"Certainty distribution mismatch: {label}")


def provenance(name: str, count: int, registry_count: int) -> tuple[dict, list[dict]]:
    doc = json.loads(read(AUDIT / name))
    check(doc["source_head"] == HEAD and doc["branch"] == BRANCH,
          f"Phase-entry source context mismatch: {name}")
    historical = doc["historical_artifact_sha256"]
    check(len(historical) == count, f"Historical artifact count mismatch: {name}")
    for path, digest in historical.items():
        file = AUDIT / path
        check(file.is_file() and sha(file) == digest, f"Historical artifact changed: {path}")
    path = doc["registry_at_entry_snapshot"]
    check(sha(AUDIT / path) == doc["registry_at_entry_sha256"],
          f"Frozen registry hash changed: {path}")
    snapshot = rows(path)
    check(len(snapshot) == registry_count, f"Frozen registry row count changed: {path}")
    return doc, snapshot


def transition(previous: list[dict], current: list[dict], phase: int,
               allowed_extensions: set[str], replanned_next: dict[str, str] | None = None,
               *, preserve_followups: bool = False) -> list[str]:
    """Old classifications/core data immutable; only declared append-only evidence,
    removing the reviewed phase and explicitly named follow-up replans allowed.
    A partial-phase delivery explicitly preserves ALL historical follow-ups.
    A replan never changes open status or implies remediation/runtime acceptance.
    """
    check([r["id"] for r in current[:len(previous)]] == [r["id"] for r in previous],
          f"Historical row order changed entering phase {phase}")
    extensions = []
    for old, new in zip(previous, current):
        for field in old.keys() - {"evidence", "next_phase"}:
            check(old[field] == new[field], f"Historical core field changed: {old['id']}.{field}")
        expected_next = (replanned_next or {}).get(old["id"], old["next_phase"] if preserve_followups else
                        ";".join(n for n in old["next_phase"].split(";") if n != str(phase)))
        check(new["next_phase"] == expected_next,
              f"Undeclared historical next_phase change in phase {phase}: {old['id']}")
        check(new["evidence"].startswith(old["evidence"]),
              f"Historical source evidence removed/replaced: {old['id']}")
        if new["evidence"] != old["evidence"]:
            check(old["id"] in allowed_extensions,
                  f"Undeclared evidence extension in phase {phase}: {old['id']}")
            extensions.append(old["id"])
    check(set(extensions) == allowed_extensions, f"Expected evidence extensions missing in phase {phase}")
    return extensions


def proposed_tests(data: list[dict], prefix: str) -> None:
    for row in data:
        check(row["status"] == "not-executed", f"{prefix} acceptance execution claim: {row['id']}")
        for field in ("scenario", "prerequisites", "procedure", "acceptance_criterion",
                      "safety_controls", "invariant_ids", "evidence"):
            check(bool(row[field]), f"Incomplete proposed test {row['id']}.{field}")


def covered(phase_findings: list[dict], data: list[dict], label: str) -> None:
    associations = {f for r in data for f in r["finding_ids"].split(";")}
    check({r["id"] for r in phase_findings} <= associations,
          f"Finding without {label} association")


def recompute(relative_json: str, script: str) -> tuple[dict, bool]:
    saved = json.loads(read(AUDIT / relative_json))
    # Only an audit-only stdlib script; never application import or execution.
    actual = json.loads(subprocess.check_output([sys.executable, str(AUDIT / script)], cwd=ROOT))
    match = saved == actual
    check(match, f"Saved audit illustration differs from recomputation: {relative_json}")
    check(saved["application_code_imported_or_executed"] is False and
          saved["erp_runtime_tests_executed"] == 0 and
          saved["sql_or_external_service_tests_executed"] == 0,
          f"Illustration metadata implies ERP execution: {relative_json}")
    return saved, match


def main(through: int, phase7_part: str = "B15") -> int:
    head, branch = git("rev-parse", "HEAD"), git("branch", "--show-current")
    from audit_source_identity import inspect_identity
    source_identity, identity_errors = inspect_identity(HEAD, git)
    for error in identity_errors:
        check(False, error)
    # Audited application reference remains HEAD; documentation commits have a
    # separate checkout identity, with exact827 source path/hashes checked below.
    check(branch == BRANCH, "Current branch differs from this audit's branch")
    inventory = rows("evidence/inventory.csv")
    expected_hashes = {r["path"]: r["sha256"] for r in inventory}
    tracked = set(git("ls-files", "-z").split("\0"))
    project_paths = {p for p in tracked if p == "SmartAuditERP.sln" or
                     p.startswith(("SmartAuditERP/", "SmartAuditUpdater/"))}
    check(len(inventory) == 827, "Historical project inventory count changed")
    check(set(expected_hashes) == project_paths, "Original tracked project paths changed")
    changed = [p for p in sorted(project_paths | set(expected_hashes))
               if not (ROOT / p).is_file() or sha(ROOT / p) != expected_hashes.get(p)]
    check(not changed, "Original project hashes changed: " + ", ".join(changed))

    prov6, frozen137, ext6 = None, [], []
    prov7, frozen172, ext7 = None, [], []
    prov3, frozen49 = provenance("evidence/provenance-03.json", 14, 49)
    checks2 = json.loads(read(AUDIT / "evidence/checks-02.json"))
    check(checks2["findings"]["total_open_not_remediated"] == 49 and
          checks2["validation"]["errors"] == [], "Historical checks-02 record changed")
    for path, digest in checks2["phase_1_historical_artifact_sha256"].items():
        check(prov3["historical_artifact_sha256"].get(path) == digest,
              f"Phase-1 historical hash continuity failed: {path}")

    prov4, prov5, frozen74, frozen106, ext3, ext4, ext5 = None, None, [], [], [], [], []
    if through >= 3:
        prov4, frozen74 = provenance("evidence/provenance-04.json", 26, 74)
        for path, digest in prov3["historical_artifact_sha256"].items():
            check(prov4["historical_artifact_sha256"].get(path) == digest,
                  f"Phase-1/2 to phase-4 hash continuity failed: {path}")
        checks3 = json.loads(read(AUDIT / "evidence/checks-03.json"))
        check(checks3["findings"]["total_open_not_remediated"] == 74 and
              checks3["validation"]["errors"] == [] and
              checks3["original_project_hashes_matching"] == 827,
              "Historical checks-03 no longer describes its historical successful check")
        check(checks3["historical_artifact_sha256"] == prov3["historical_artifact_sha256"],
              "Phase-3 check/provenance historical hash map mismatch")
        ext3 = transition(frozen49, frozen74, 3, {"P1-033"})

    if through >= 4:
        prov5, frozen106 = provenance("evidence/provenance-05.json", 38, 106)
        for path, digest in prov4["historical_artifact_sha256"].items():
            check(prov5["historical_artifact_sha256"].get(path) == digest,
                  f"Phase-1/2/3 to phase-5 hash continuity failed: {path}")
        checks4 = json.loads(read(AUDIT / "evidence/checks-04.json"))
        check(checks4["findings"]["total_open_not_remediated"] == 106 and
              checks4["validation"]["errors"] == [] and
              checks4["original_project_hashes_matching"] == 827,
              "Historical checks-04 no longer describes its historical successful check")
        check(checks4["historical_artifact_sha256"] == prov4["historical_artifact_sha256"],
              "Phase-4 check/provenance historical hash map mismatch")
        ext4 = transition(frozen74, frozen106, 4, {"P1-033", "P3-003", "P3-005", "P3-006"})

    if through >= 5:
        prov6, frozen137 = provenance("evidence/provenance-06.json", 53, 137)
        for path, digest in prov5["historical_artifact_sha256"].items():
            check(prov6["historical_artifact_sha256"].get(path) == digest,
                  f"Phase-1..4 to phase-6 hash continuity failed: {path}")
        checks5 = json.loads(read(AUDIT / "evidence/checks-05.json"))
        check(checks5["findings"]["total_open_not_remediated"] == 137 and
              checks5["validation"]["errors"] == [] and
              checks5["original_project_hashes_matching"] == 827,
              "Historical checks-05 no longer describes its historical successful check")
        check(checks5["historical_artifact_sha256"] == prov5["historical_artifact_sha256"],
              "Phase-5 check/provenance historical hash map mismatch")
        check(sha(AUDIT / prov6["registry_at_entry_snapshot"]) ==
              "6dc63d157f05a25f1f7b580bbe8ee843b2c61267e18c13219905d4ce0073006c",
              "Phase-5 registry SHA256 differs from the delivered entry snapshot")

    if through >= 6:
        prov7, frozen172 = provenance("evidence/provenance-07.json", 67, 172)
        for path, digest in prov6["historical_artifact_sha256"].items():
            check(prov7["historical_artifact_sha256"].get(path) == digest,
                  f"Phase-1..5 to phase-7 hash continuity failed: {path}")
        checks6 = json.loads(read(AUDIT / "evidence/checks-06.json"))
        check(checks6["findings"]["total_open_not_remediated"] == 172 and
              checks6["validation"]["errors"] == [] and
              checks6["original_project_hashes_matching"] == 827,
              "Historical checks-06 no longer describes its successful historical check")
        check(checks6["historical_artifact_sha256"] == prov6["historical_artifact_sha256"],
              "Phase-6 check/provenance historical hash map mismatch")
        check(sha(AUDIT / prov7["registry_at_entry_snapshot"]) ==
              "1916bebebcb9d6af3e6bff94719c0269f44fb0e120c07c2bd3c316fd9ac07597",
              "Phase-6 registry SHA256 differs from the delivered entry-to7 snapshot")
        check(prov7["phase6_entry_consistency"] ==
              {"original_hashes_matching": 827, "findings": 172, "errors": [], "erp_runtime_tests_executed": 0},
              "Phase7 entry metadata no longer represents the checked partial-audit starting point")

    prov7b, frozen200 = None, []
    if through == 7:
        # The7A inputs are immutable even when the current registry grows.
        prov7b, frozen200 = provenance("evidence/provenance-07B.json", 86, 200)
        for path, digest in prov7["historical_artifact_sha256"].items():
            check(prov7b["historical_artifact_sha256"].get(path) == digest,
                  f"Historical hash continuity into7B1 failed: {path}")

    registry_path = ({2: prov3["registry_at_entry_snapshot"],
                      3: prov4["registry_at_entry_snapshot"] if prov4 else "",
                      4: prov5["registry_at_entry_snapshot"] if prov5 else "",
                      5: prov6["registry_at_entry_snapshot"] if prov6 else "",
                      6: prov7["registry_at_entry_snapshot"] if prov7 else "",
                      7: prov7b["registry_at_entry_snapshot"] if prov7b else ""})[through]
    findings = rows(registry_path)
    extensions5 = {"P1-010", "P1-011", "P1-014", "P1-017", "P2-003", "P3-003", "P3-006", "P4-029"}
    if through >= 5:
        # P1-014 had only5 scheduled; carry external broker TLS/auth/ACL
        # deployment acceptance to8 explicitly rather than an empty/closed item.
        check(next(r for r in frozen106 if r["id"] == "P1-014")["next_phase"] == "5",
              "Unexpected P1-014 original follow-up before explicit phase5-to8 replan")
        ext5 = transition(frozen106, frozen137, 5, extensions5, {"P1-014": "8"})
    extensions6 = {"P1-011", "P1-017", "P1-024", "P1-032", "P1-033",
                   "P2-015", "P3-003", "P3-005", "P3-006"}
    if through >= 6:
        check(next(r for r in frozen137 if r["id"] == "P1-032")["next_phase"] == "6",
              "Unexpected P1-032 follow-up before explicit phase6-to8 replan")
        ext6 = transition(frozen137, frozen172, 6, extensions6, {"P1-032": "8"})
    extensions7 = {"P1-011", "P1-013", "P1-017", "P1-030", "P1-033", "P2-010",
                   "P3-002", "P3-003", "P3-005", "P3-006", "P3-008", "P3-010", "P3-023",
                   "P4-020", "P4-025"}
    if through == 7:
        ext7 = transition(frozen172, findings, 7, extensions7, preserve_followups=True)
        check(sum("7" in r["next_phase"].split(";") for r in frozen172) == 43,
              "Historical phase7 follow-up count changed")

    scope_spec = [("review-scope.csv", 52), ("review-scope-02.csv", 60)]
    if through >= 3:
        scope_spec.append(("review-scope-03.csv", 50))
    if through >= 4:
        scope_spec.append(("review-scope-04.csv", 48))
    if through >= 5:
        scope_spec.append(("review-scope-05.csv", 54))
    if through >= 6:
        scope_spec.append(("review-scope-06.csv", 53))
    if through == 7:
        scope_spec.append(("review-scope-07.csv", 47))
    scopes, scope4_ranges, scope5_ranges, scope6_ranges, historical_scope_ranges = {}, {}, {}, {}, {}
    scope7_ranges = {}
    for name, count in scope_spec:
        data = rows(name)
        check(len(data) == count, f"Unexpected scope row count: {name}")
        check(len({r["path"] for r in data}) == len(data), f"Duplicate scope paths: {name}")
        for row in data:
            check(row["path"] in project_paths, f"Untracked project scope: {row['path']}")
            source_ref(row["path"], row["ranges"], name)
            if name == "review-scope-04.csv":
                scope4_ranges[row["path"]] = spans(row["ranges"])
            elif name == "review-scope-05.csv":
                scope5_ranges[row["path"]] = spans(row["ranges"])
            elif name == "review-scope-06.csv":
                scope6_ranges[row["path"]] = spans(row["ranges"])
            elif name == "review-scope-07.csv":
                scope7_ranges[row["path"]] = spans(row["ranges"])
            else:
                historical_scope_ranges.setdefault(row["path"], []).extend(spans(row["ranges"]))
        scopes[name] = {r["path"] for r in data}
    union12 = scopes["review-scope.csv"] | scopes["review-scope-02.csv"]
    check(len(union12) == 92, "Historical phase-1/2 scope union changed")
    union123 = set(union12)
    if through >= 3:
        check(len(scopes["review-scope-03.csv"] & union12) == 15, "Phase-3 scope overlap mismatch")
        union123 |= scopes["review-scope-03.csv"]
        check(len(union123) == 127, "Historical phase-1/2/3 union changed")
    union = set.union(*scopes.values())
    union1234 = set(union123)
    if through >= 4:
        check(len(scopes["review-scope-04.csv"] & union123) == 15, "Phase-4 overlap mismatch")
        check(len(scopes["review-scope-04.csv"] - union123) == 33, "Phase-4 new scope mismatch")
        union1234 |= scopes["review-scope-04.csv"]
        check(len(union1234) == 160, "Historical phase-1/2/3/4 unique scope mismatch")
    union12345 = set(union1234)
    if through >= 5:
        check(len(scopes["review-scope-05.csv"] & union1234) == 24, "Phase-5 overlap mismatch")
        check(len(scopes["review-scope-05.csv"] - union1234) == 30, "Phase-5 new scope mismatch")
        union12345 |= scopes["review-scope-05.csv"]
        check(len(union12345) == 190, "Cumulative phase-5 unique scope mismatch")
        for old, new in zip(frozen106, frozen137):
            if old["id"] in extensions5:
                added = new["evidence"][len(old["evidence"]):].lstrip(";")
                scoped_evidence(added, scope5_ranges, old["id"] + " phase5 extension", phase=5)

    union123456 = set(union12345)
    if through >= 6:
        check(len(scopes["review-scope-06.csv"] & union12345) == 17, "Phase-6 overlap mismatch")
        check(len(scopes["review-scope-06.csv"] - union12345) == 36, "Phase-6 new paths mismatch")
        union123456 |= scopes["review-scope-06.csv"]
        check(len(union123456) == 226, "Cumulative phase-6 unique scope mismatch")
        for old, new in zip(frozen137, frozen172):
            if old["id"] in extensions6:
                added = new["evidence"][len(old["evidence"]):].lstrip(";")
                scoped_evidence(added, scope6_ranges, old["id"] + " phase6 extension", phase=6)

    if through == 7:
        check(len(scopes["review-scope-07.csv"] & union123456) == 7, "Phase7A overlap mismatch")
        check(len(scopes["review-scope-07.csv"] - union123456) == 40, "Phase7A new paths mismatch")
        check(len(union) == 266, "Partial phase7A selected-path union mismatch")
        for old, new in zip(frozen172, findings):
            if old["id"] in extensions7:
                added = new["evidence"][len(old["evidence"]):].lstrip(";")
                scoped_evidence(added, scope7_ranges, old["id"] + " phase7A extension", phase=7)

    counts = {1: 33, 2: 16, 3: 25, 4: 32, 5: 31, 6: 35, 7: 28}
    phase_rows = {n: [r for r in findings if r["id"].startswith(f"P{n}-")]
                  for n in range(1, through + 1)}
    for n, data in phase_rows.items():
        sequential(data, f"P{n}-", counts[n], width=3)
    expected_count = {2: 49, 3: 74, 4: 106, 5: 137, 6: 172, 7: 200}[through]
    check(len(findings) == expected_count and len({r["id"] for r in findings}) == expected_count,
          "Cumulative findings count/uniqueness mismatch")
    distributions(phase_rows[1], {"Critical": 2, "High": 17, "Medium": 13, "Low": 1},
                  {"confirmed": 21, "potential": 7, "repository-gap": 5}, "phase 1")
    distributions(phase_rows[2], {"High": 10, "Medium": 6},
                  {"confirmed": 14, "potential": 2}, "phase 2")
    if through >= 3:
        distributions(phase_rows[3], {"High": 18, "Medium": 7},
                      {"confirmed": 23, "potential": 2}, "phase 3")
    if through >= 4:
        distributions(phase_rows[4], {"High": 24, "Medium": 8},
                      {"confirmed": 29, "potential": 3}, "phase 4")
        check([r["id"] for r in phase_rows[4] if r["certainty"] == "potential"] ==
              ["P4-007", "P4-014", "P4-021"], "Unexpected phase-4 conditional findings")
    if through >= 5:
        distributions(phase_rows[5], {"High": 22, "Medium": 9},
                      {"confirmed": 27, "potential": 4}, "phase 5")
        check([r["id"] for r in phase_rows[5] if r["certainty"] == "potential"] ==
              ["P5-004", "P5-005", "P5-026", "P5-028"], "Unexpected phase-5 conditional findings")
    if through >= 6:
        distributions(phase_rows[6], {"High": 26, "Medium": 9},
                      {"confirmed": 30, "potential": 3, "repository-gap": 2}, "phase 6")
        check([r["id"] for r in phase_rows[6] if r["certainty"] == "potential"] ==
              ["P6-005", "P6-019", "P6-021"], "Unexpected phase-6 conditional findings")
        check([r["id"] for r in phase_rows[6] if r["certainty"] == "repository-gap"] ==
              ["P6-029", "P6-030"], "Unexpected phase-6 repository gaps")
    if through == 7:
        distributions(phase_rows[7], {"High": 20, "Medium": 8},
                      {"confirmed": 23, "potential": 5}, "phase7A ONLY not complete7")
        check([r["id"] for r in phase_rows[7] if r["certainty"] == "potential"] ==
              ["P7-008", "P7-009", "P7-019", "P7-020", "P7-024"],
              "Unexpected phase7A conditional findings")
    for row in findings:
        check(row["status"] == "open-not-remediated", f"Unverified closure: {row['id']}")
        check(bool(row["title"]) and bool(row["evidence"]), f"Incomplete finding: {row['id']}")
        # Only7A has been delivered. Historical7 follow-ups remain valid and
        # MUST NOT be silently removed just because the through marker is7.
        minimum_followup = 7 if through == 7 and not row["id"].startswith("P7-") else through + 1
        check(all(n.isdigit() and minimum_followup <= int(n) <= 8
                  for n in row["next_phase"].split(";")), f"Unexpected next_phase: {row['id']}")
        evidence(row["evidence"], row["id"])
        if row["id"].startswith("P4-"):
            # A P5 append is separately scoped above; original P4 evidence stays frozen.
            original = next((r for r in frozen106 if r["id"] == row["id"]), row)
            scoped_evidence(original["evidence"], scope4_ranges, row["id"])
        elif row["id"].startswith("P5-"):
            scoped_evidence(row["evidence"], scope5_ranges, row["id"], phase=5)
        elif row["id"].startswith("P6-"):
            scoped_evidence(row["evidence"], scope6_ranges, row["id"], phase=6)
        elif row["id"].startswith("P7-"):
            scoped_evidence(row["evidence"], scope7_ranges, row["id"], phase=7)
    for n, data in phase_rows.items():
        name = f"PHASE-{n:02d}.md"
        headers = re.findall(r"^### (P[1234567]-\d{3}) —", read(AUDIT / name), re.M)
        check(headers == [r["id"] for r in data], f"Report headings/CSV mismatch: {name}")

    known = {r["id"] for r in findings} | {"H2-01", "H2-02", "H2-03"}
    if through >= 3:
        known |= {"H3-01", "H3-02", "H3-03", "H3-04"}
    if through >= 4:
        known |= {"H4-01", "H4-02", "H4-03", "H4-04"}
    if through >= 5:
        known |= {"H5-01", "H5-02", "H5-03", "H5-04"}
    if through >= 6:
        known |= {f"H6-{n:02d}" for n in range(1, 9)}
    if through == 7:
        known |= {f"H7-{n:02d}" for n in range(1, 9)}
    identity = rows("evidence/identity-flows-02.csv")
    acl = rows("evidence/authorization-matrix-02.csv")
    sql = rows("evidence/sql-source-sink-02.csv")
    tests2 = rows("evidence/acceptance-tests-02.csv")
    for data, prefix, count in ((identity, "ID2-", 12), (acl, "ACL2-", 21),
                                (sql, "SQL2-", 26), (tests2, "P2T-", 24)):
        sequential(data, prefix, count)
        related(data, known)
        validate_evidence_rows(data)
    for data, field in ((acl, "runtime_status"), (sql, "runtime_validation"), (tests2, "status")):
        for row in data:
            check(row[field] == "not-executed", f"P2 execution claim: {row['id']}")
    for row in tests2:
        check(bool(row["safety_controls"]) and bool(row["prerequisites"]),
              f"Unsafe/incomplete P2 proposed test: {row['id']}")
    covered(phase_rows[2], tests2, "P2 acceptance plan")
    sql_types = collections.Counter(r["classification"] for r in sql)
    check(dict(sql_types) == {"unparameterized-user-text": 13, "parameterized-slice": 9,
                              "controlled-or-typed-slice": 3, "derived-source-unresolved": 1},
          "Historical SQL trace classification mismatch")

    tests3, invariants3, lifecycles3, illustrations3 = [], [], [], []
    witness3_match = None
    if through >= 3:
        tests3 = rows("evidence/acceptance-tests-03.csv")
        invariants3 = rows("evidence/accounting-invariants-03.csv")
        lifecycles3 = rows("evidence/document-lifecycle-03.csv")
        for data, prefix, count in ((tests3, "P3T-", 35), (invariants3, "INV3-", 20),
                                    (lifecycles3, "LC3-", 16)):
            sequential(data, prefix, count)
            related(data, known)
            validate_evidence_rows(data)
        related(tests3, {r["id"] for r in invariants3}, "invariant_ids")
        related(invariants3, {r["id"] for r in tests3}, "acceptance_ids")
        proposed_tests(tests3, "P3")
        for row in invariants3 + lifecycles3:
            check(row["runtime_status"] == "not-executed", f"P3 execution claim: {row['id']}")
        covered(phase_rows[3], tests3, "P3 acceptance plan")
        covered(phase_rows[3], invariants3, "P3 invariant")
        witness3, witness3_match = recompute("evidence/arithmetic-witnesses-03.json",
                                           "tools/check_financial_witnesses.py")
        illustrations3 = witness3["illustrations"]
        sequential(illustrations3, "ALG3-", 8)
        related(illustrations3, known)
        check(witness3["illustration_count"] == 8, "P3 illustration count mismatch")
        for case in illustrations3:
            check(case["source_application_executed"] is False and bool(case["limit"]) and
                  case["illustration_assertions_passed"] is True,
                  f"P3 illustration missing limit or inappropriate execution claim: {case['id']}")
            evidence(case["evidence"], case["id"])

    tests4, invariants4, matrix4, illustrations4, parameter4 = [], [], [], [], []
    witness4_match = None
    if through >= 4:
        tests4 = rows("evidence/acceptance-tests-04.csv")
        invariants4 = rows("evidence/inventory-invariants-04.csv")
        matrix4 = rows("evidence/document-state-effects-04.csv")
        for data, prefix, count in ((tests4, "P4T-", 60), (invariants4, "INV4-", 25),
                                    (matrix4, "MX4-", 40)):
            sequential(data, prefix, count)
            related(data, known)
            validate_evidence_rows(data)
            for row in data:
                # P4T-57 is explicitly a future regression plan for still-open
                # P3 shift-close findings, not a new P4 reading/coverage claim.
                selected_ranges = historical_scope_ranges if row["id"] == "P4T-57" else scope4_ranges
                scoped_evidence(row["evidence"], selected_ranges, row["id"])
        test4_ids = {r["id"] for r in tests4}
        related(tests4, {r["id"] for r in invariants4}, "invariant_ids")
        related(invariants4 + matrix4, test4_ids, "acceptance_ids")
        proposed_tests(tests4, "P4")
        for row in invariants4 + matrix4:
            check(row["runtime_status"] == "not-executed", f"P4 execution claim: {row['id']}")
        for row in matrix4:
            for field in ("document", "state_or_transition", "entrypoint_and_calls", "financial_effect",
                          "inventory_effect", "commit_failure_and_guard", "scope_limit", "evidence"):
                check(bool(row[field]), f"Incomplete document/state/effect row: {row['id']}.{field}")
        covered(phase_rows[4], tests4, "P4 acceptance plan")
        covered(phase_rows[4], invariants4, "P4 invariant")
        covered(phase_rows[4], matrix4, "P4 document/state/effect matrix")
        witness4, witness4_match = recompute("evidence/inventory-witnesses-04.json",
                                           "tools/check_inventory_witnesses.py")
        illustrations4 = witness4["illustrations"]
        parameter4 = witness4["static_parameter_contract_checks"]
        sequential(illustrations4, "ALG4-", 12)
        sequential(parameter4, "ST4-", 4)
        related(illustrations4 + parameter4, known)
        check(witness4["illustration_count"] == 12 and
              witness4["static_parameter_contract_check_count"] == 4 and
              witness4["application_remediation_performed"] is False,
              "P4 witness metadata/count mismatch")
        for case in illustrations4 + parameter4:
            check(case["source_application_executed"] is False and bool(case["limit"]),
                  f"P4 illustration/text check inappropriate execution claim: {case['id']}")
            flag = "illustration_assertions_passed" if case["id"].startswith("ALG") else "documented_set_difference_matches"
            check(case[flag] is True, f"Inconsistent audit-only illustration/text check: {case['id']}")
            evidence(case["evidence"], case["id"])
            scoped_evidence(case["evidence"], scope4_ranges, case["id"])
        for filename, pattern, expected in (
            ("VALIDATION-04.md", r"^\| (P4T-\d{2}) \|", [r["id"] for r in tests4]),
            ("SALES-INVENTORY-04.md", r"^\| (INV4-\d{2}) \|", [r["id"] for r in invariants4]),
            ("SALES-INVENTORY-04.md", r"^\| (MX4-\d{2}) —", [r["id"] for r in matrix4]),
            ("SALES-INVENTORY-04.md", r"^\| (H4-\d{2}) —", [f"H4-{n:02d}" for n in range(1, 5)]),
            ("SALES-INVENTORY-04.md", r"^\| (Q4-\d{2}) \|", [f"Q4-{n:02d}" for n in range(1, 10)]),
        ):
            check(re.findall(pattern, read(AUDIT / filename), re.M) == expected,
                  f"Summary table IDs/order mismatch in {filename}: {pattern}")

    tests5, invariants5, flows5, owners5, topics5, matrix5, illustrations5, lexical5 = [], [], [], [], [], [], [], []
    witness5_match = None
    if through >= 5:
        tests5 = rows("evidence/acceptance-tests-05.csv")
        invariants5 = rows("evidence/sync-invariants-05.csv")
        flows5 = rows("evidence/sync-flows-05.csv")
        owners5 = rows("evidence/sync-data-ownership-05.csv")
        topics5 = rows("evidence/mqtt-topic-contracts-05.csv")
        matrix5 = rows("evidence/sync-failure-conflict-05.csv")
        for data, prefix, count in ((tests5, "P5T-", 64), (invariants5, "INV5-", 24),
                                    (flows5, "SF5-", 18), (owners5, "OWN5-", 12),
                                    (topics5, "MT5-", 25), (matrix5, "FM5-", 36)):
            sequential(data, prefix, count)
            related(data, known)
            validate_evidence_rows(data)
            for row in data:
                for field, value in row.items():
                    check(bool(value), f"Incomplete P5 evidence row: {row['id']}.{field}")
                scoped_evidence(row["evidence"], scope5_ranges, row["id"], phase=5)
        related(tests5 + matrix5, {r["id"] for r in invariants5}, "invariant_ids")
        related(invariants5 + flows5 + owners5 + topics5 + matrix5,
                {r["id"] for r in tests5}, "acceptance_ids")
        proposed_tests(tests5, "P5")
        for row in invariants5 + flows5 + owners5 + topics5 + matrix5:
            check(row["runtime_status"] == "not-executed", f"P5 execution claim: {row['id']}")
        for data, label in ((tests5, "P5 acceptance plan"), (invariants5, "P5 invariant"),
                            (matrix5, "P5 failure/conflict row")):
            covered(phase_rows[5], data, label)
        witness5, witness5_match = recompute("evidence/sync-witnesses-05.json",
                                           "tools/check_sync_witnesses.py")
        illustrations5 = witness5["illustrations"]
        lexical5 = witness5["static_lexical_contract_checks"]
        sequential(illustrations5, "ALG5-", 12)
        sequential(lexical5, "ST5-", 5)
        related(illustrations5 + lexical5, known)
        check(witness5["illustration_count"] == 12 and
              witness5["static_lexical_contract_check_count"] == 5 and
              witness5["application_remediation_performed"] is False,
              "P5 witness metadata/count mismatch")
        for case in illustrations5 + lexical5:
            flag = "illustration_assertions_passed" if case["id"].startswith("ALG") else "documented_text_observation_matches"
            check(case["source_application_executed"] is False and bool(case["limit"]) and case[flag] is True,
                  f"P5 inconsistent illustration/text check or execution claim: {case['id']}")
            evidence(case["evidence"], case["id"])
            scoped_evidence(case["evidence"], scope5_ranges, case["id"], phase=5)
        for filename, pattern, expected in (
            ("VALIDATION-05.md", r"^\| (P5T-\d{2}) \|", [r["id"] for r in tests5]),
            ("SYNC-OFFLINE-05.md", r"^\| (INV5-\d{2}) \|", [r["id"] for r in invariants5]),
            ("SYNC-OFFLINE-05.md", r"^\| (SF5-\d{2}) —", [r["id"] for r in flows5]),
            ("SYNC-OFFLINE-05.md", r"^\| (OWN5-\d{2}) —", [r["id"] for r in owners5]),
            ("SYNC-OFFLINE-05.md", r"^\| (MT5-\d{2}) —", [r["id"] for r in topics5]),
            ("SYNC-OFFLINE-05.md", r"^\| (FM5-\d{2}) —", [r["id"] for r in matrix5]),
            ("SYNC-OFFLINE-05.md", r"^\| (H5-\d{2}) —", [f"H5-{n:02d}" for n in range(1, 5)]),
            ("SYNC-OFFLINE-05.md", r"^\| (Q5-\d{2}) \|", [f"Q5-{n:02d}" for n in range(1, 11)]),
        ):
            check(re.findall(pattern, read(AUDIT / filename), re.M) == expected,
                  f"P5 summary table IDs/order mismatch in {filename}: {pattern}")

    tests6, invariants6, contracts6, matrix6, sources6, illustrations6, lexical6 = [], [], [], [], [], [], []
    witness6_match = None
    if through >= 6:
        tests6 = rows("evidence/acceptance-tests-06.csv")
        invariants6 = rows("evidence/integration-invariants-06.csv")
        contracts6 = rows("evidence/provider-contracts-06.csv")
        matrix6 = rows("evidence/integration-failure-matrix-06.csv")
        sources6 = rows("evidence/official-references-06.csv")
        for data, prefix, count in ((tests6, "P6T-", 80), (invariants6, "INV6-", 32),
                                    (contracts6, "INT6-", 14), (matrix6, "FM6-", 48),
                                    (sources6, "REF6-", 15)):
            sequential(data, prefix, count)
            for row in data:
                for field, value in row.items():
                    check(bool(value), f"Incomplete P6 evidence row: {row['id']}.{field}")
            if prefix != "REF6-":
                related(data, known)
                validate_evidence_rows(data)
                for row in data:
                    scoped_evidence(row["evidence"], scope6_ranges, row["id"], phase=6)
        test6_ids = {r["id"] for r in tests6}
        inv6_ids = {r["id"] for r in invariants6}
        contract6_ids = {r["id"] for r in contracts6}
        source6_ids = {r["id"] for r in sources6}
        related(tests6 + contracts6 + matrix6, inv6_ids, "invariant_ids")
        related(tests6 + matrix6, contract6_ids, "contract_ids")
        related(invariants6 + contracts6 + matrix6, test6_ids, "acceptance_ids")
        for row in contracts6 + matrix6:
            check(row["official_source_ids"] == "none" or
                  set(row["official_source_ids"].split(";")) <= source6_ids,
                  f"Unknown P6 official reference in {row['id']}")
        for row in sources6:
            parsed = urlsplit(row["url"])
            check(parsed.scheme == "https" and parsed.hostname in
                  {"zatca.gov.sa", "sdk.invoicing.eta.gov.eg", "docs.salla.dev"},
                  f"Unexpected public official reference URL: {row['id']}")
            check(row["retrieved_date_utc"] == "2026-11-17" and
                  row["body_retention"] == "not-retained" and
                  row["body_sha256"] == "not-available-body-not-retained" and
                  row["verification_status"] == "official-public-document-read-only-not-provider-tested",
                  f"P6 reference metadata overclaims retained proof/provider execution: {row['id']}")
        proposed_tests(tests6, "P6")
        for row in invariants6 + contracts6 + matrix6:
            check(row["runtime_status"] == "not-executed", f"P6 execution claim: {row['id']}")
        for pool, field in ((invariants6, "invariant_ids"), (contracts6, "contract_ids")):
            for row in pool:
                expected = [t["id"] for t in tests6 if row["id"] in t[field].split(";")]
                check(row["acceptance_ids"].split(";") == expected and bool(expected),
                      f"P6 reverse acceptance association mismatch: {row['id']}")
        for data, label in ((tests6, "P6 acceptance plan"), (invariants6, "P6 invariant"),
                            (contracts6, "P6 provider contract"), (matrix6, "P6 failure case")):
            covered(phase_rows[6], data, label)
        for contract in contracts6:
            linked = [m for m in matrix6 if contract["id"] in m["contract_ids"].split(";")]
            check(bool(linked), f"P6 provider without failure case: {contract['id']}")
            check(any(set(m["acceptance_ids"].split(";")) &
                      set(contract["acceptance_ids"].split(";")) for m in linked),
                  f"P6 provider failure case lacks linked acceptance: {contract['id']}")
        witness6, witness6_match = recompute("evidence/integration-witnesses-06.json",
                                           "tools/check_integration_witnesses.py")
        illustrations6 = witness6["illustrations"]
        lexical6 = witness6["static_lexical_contract_checks"]
        sequential(illustrations6, "ALG6-", 14)
        sequential(lexical6, "ST6-", 7)
        related(illustrations6 + lexical6, known)
        check(witness6["illustration_count"] == 14 and
              witness6["static_lexical_contract_check_count"] == 7 and
              witness6["application_remediation_performed"] is False and
              witness6["secrets_or_real_provider_payloads_used"] is False,
              "P6 witness metadata/count mismatch")
        for case in illustrations6 + lexical6:
            flag = "illustration_assertions_passed" if case["id"].startswith("ALG") else "documented_text_observation_matches"
            check(case["source_application_executed"] is False and bool(case["limit"]) and case[flag] is True,
                  f"P6 inconsistent illustration/text check or execution claim: {case['id']}")
            evidence(case["evidence"], case["id"])
            scoped_evidence(case["evidence"], scope6_ranges, case["id"], phase=6)
        for filename, pattern, expected in (
            ("VALIDATION-06.md", r"^\| (P6T-\d{2}) \|", [r["id"] for r in tests6]),
            ("INTEGRATIONS-06.md", r"^\| (INT6-\d{2}) —", [r["id"] for r in contracts6]),
            ("INTEGRATIONS-06.md", r"^\| (INV6-\d{2}) \|", [r["id"] for r in invariants6]),
            ("INTEGRATIONS-06.md", r"^\| (FM6-\d{2}) —", [r["id"] for r in matrix6]),
            ("INTEGRATIONS-06.md", r"^\| (REF6-\d{2}) —", [r["id"] for r in sources6]),
            ("INTEGRATIONS-06.md", r"^\| (H6-\d{2}) —", [f"H6-{n:02d}" for n in range(1, 9)]),
            ("INTEGRATIONS-06.md", r"^\| (Q6-\d{2}) \|", [f"Q6-{n:02d}" for n in range(1, 13)]),
        ):
            check(re.findall(pattern, read(AUDIT / filename), re.M) == expected,
                  f"P6 summary table IDs/order mismatch in {filename}: {pattern}")

    tests7, invariants7, features7, commands7, handoffs7, questions7, extensions7_rows, backlog7, ledger7 = [], [], [], [], [], [], [], [], []
    illustrations7, lexical7, witness7_match = [], [], None
    if through == 7:
        tests7 = rows("evidence/acceptance-tests-07.csv")
        invariants7 = rows("evidence/feature-invariants-07.csv")
        features7 = rows("evidence/feature-implementation-matrix-07.csv")
        commands7 = rows("evidence/command-completeness-07.csv")
        handoffs7 = rows("evidence/handoffs-07.csv")
        questions7 = rows("evidence/questions-07.csv")
        extensions7_rows = rows("evidence/historical-extensions-07.csv")
        backlog7 = rows("evidence/continuation-backlog-07.csv")
        ledger7 = rows("evidence/coverage-ledger-07.csv")
        for data, prefix, count in ((tests7, "P7T-", 64), (invariants7, "INV7-", 25),
                                    (features7, "FE7-", 36), (commands7, "CMD7-", 16),
                                    (handoffs7, "H7-", 8), (questions7, "Q7-", 12),
                                    (extensions7_rows, "EX7-", 15), (backlog7, "BK7-", 10)):
            sequential(data, prefix, count)
            related(data, known)
            validate_evidence_rows(data)
            for row in data:
                for field, value in row.items():
                    check(bool(value), f"Incomplete partial7A row: {row['id']}.{field}")
                if "evidence" in row:
                    scoped_evidence(row["evidence"], scope7_ranges, row["id"], phase=7)
        inv7_ids = {r["id"] for r in invariants7}
        feature7_ids = {r["id"] for r in features7}
        test7_ids = {r["id"] for r in tests7}
        handoff7_ids = {r["id"] for r in handoffs7}
        related(tests7, inv7_ids, "invariant_ids")
        related(tests7, feature7_ids, "feature_ids")
        related(invariants7 + features7 + commands7, test7_ids, "acceptance_ids")
        related(questions7, handoff7_ids, "handoff_ids")
        proposed_tests(tests7, "P7A")
        for row in invariants7 + features7 + commands7 + handoffs7 + extensions7_rows + backlog7:
            check(row["runtime_status"] == "not-executed", f"Partial7A execution claim: {row['id']}")
        for pool, field in ((invariants7, "invariant_ids"), (features7, "feature_ids")):
            for row in pool:
                expected = [t["id"] for t in tests7 if row["id"] in t[field].split(";")]
                check(row["acceptance_ids"].split(";") == expected and bool(expected),
                      f"Partial7A reverse acceptance association mismatch: {row['id']}")
        for data, label in ((tests7, "P7A acceptance plan"), (invariants7, "P7A invariant"),
                            (features7, "P7A feature/screen/implementation/test matrix")):
            covered(phase_rows[7], data, label)
        for finding in phase_rows[7]:
            direct_tests = [t for t in tests7 if finding["id"] in t["finding_ids"].split(";")]
            check(len(direct_tests) == 2, f"P7A finding lacks two explicit unexecuted plans: {finding['id']}")
        check([r["implementation_status"] for r in features7[-2:]] ==
              ["deferred-7B-unreviewed", "deferred-7C-unreviewed"],
              "7B/7C accidentally represented as completed/reviewed in feature matrix")
        check(all(r["implementation_status"] in {"implemented-with-observed-defects", "partial-or-stub",
                  "conditional-external-contract", "deferred-7B-unreviewed", "deferred-7C-unreviewed"}
                  for r in features7), "Unexpected feature implementation/completion claim")
        check(sum(r["assessment"].startswith("visible-") for r in commands7) == 13 and
              sum(r["assessment"] == "hidden-no-required-gap-established" for r in commands7) == 2 and
              sum(r["assessment"] == "optional-event-no-required-gap-established" for r in commands7) == 1,
              "P7A visible/hidden/optional command distinction changed")
        check(all(r["finding_ids"] == "P1-033" and r["acceptance_ids"] == "P7T-60" for r in commands7),
              "P7A command matrix duplicates findings or lacks shared acceptance")
        check({r["finding_ids"] for r in extensions7_rows} == extensions7,
              "Partial7A historical extension manifest mismatch")
        for row in extensions7_rows:
            old = next(r for r in frozen172 if r["id"] == row["finding_ids"])
            new = next(r for r in findings if r["id"] == row["finding_ids"])
            check(new["evidence"] == old["evidence"] + ";" + row["evidence"] and
                  new["next_phase"] == old["next_phase"] and
                  row["followup_policy"] == "unchanged-during-partial7",
                  f"Partial7A evidence/follow-up extension mismatch: {row['id']}")
        for row in backlog7:
            check(row["status"] == "not-started" and row["part"] in {"7B", "7C", "7B/7C"},
                  f"P7A continuation incorrectly represented as completed/authorized8: {row['id']}")
            check(row["selection_basis"] == "inventory-or-selected-caller-only-not-reviewed-implementation",
                  f"P7A candidate-path inventory overclaims review: {row['id']}")
            for path in row["candidate_paths"].split(";"):
                check(path in project_paths, f"Unknown continuation candidate path: {row['id']}:{path}")
        for row in questions7:
            check(row["status"] == "unanswered-no-secrets-requested", f"Undeclared Q7 resolution: {row['id']}")
        for row in handoffs7:
            check(row["status"] == "external-contract-or-policy-unresolved-not-absence-proof",
                  f"Undeclared H7 resolution/absence claim: {row['id']}")

        # Recompute declared-range bookkeeping from the frozen scope CSVs plus7A.
        # Metadata ranges are included but NEVER interpreted as semantic reading.
        def merged_ranges(ranges):
            out = []
            for a, b in sorted(ranges):
                if out and a <= out[-1][1] + 1:
                    out[-1] = (out[-1][0], max(out[-1][1], b))
                else:
                    out.append((a, b))
            return out

        def formatted_ranges(ranges):
            return ";".join(f"{a}-{b}" for a, b in ranges) or "none"

        declared, path_phases, path_states, phase7_spelling = {}, {}, {}, {}
        for n, (filename, _) in enumerate(scope_spec, 1):
            label = "7A" if n == 7 else str(n)
            for row in rows(filename):
                path = row["path"]
                declared.setdefault(path, []).extend(spans(row["ranges"]))
                path_phases.setdefault(path, []).append(label)
                path_states.setdefault(path, []).append(label + ":" + row["review_state"])
                if n == 7:
                    phase7_spelling[path] = row["ranges"]
        check([r["path"] for r in ledger7] == [r["path"] for r in inventory],
              "P7A coverage ledger must cover all827 original paths once in inventory order")
        for original, ledger in zip(inventory, ledger7):
            path = original["path"]
            merged = merged_ranges(declared.get(path, []))
            total = int(original["lines"]) if original["lines"] else None
            if total is None:
                remaining, line_state = "not-a-text-line-model", "binary-metadata-not-executed"
            elif not total:
                remaining, line_state = "none-zero-lines", "zero-line-artifact"
            else:
                cursor, gaps = 1, []
                for a, b in merged:
                    if cursor < a:
                        gaps.append((cursor, a - 1))
                    cursor = b + 1
                if cursor <= total:
                    gaps.append((cursor, total))
                remaining = formatted_ranges(gaps)
                line_state = "partial-or-no-declared-ranges" if gaps else "all-lines-in-declared-ranges-not-semantic-certification"
            expected = {"inventory_kind": original["kind"], "inventory_lines": original["lines"] or "not-text",
                        "path_scope_state": "selected-path-not-whole-file-certified" if merged else "inventory-only-no-selected-scope",
                        "selected_phase_ids": ";".join(path_phases.get(path, [])) or "none",
                        "declared_review_states": ";".join(path_states.get(path, [])) or "inventory-only",
                        "declared_range_union_not_reading_certification": formatted_ranges(merged),
                        "unselected_text_ranges": remaining, "line_range_state": line_state,
                        "phase7A_ranges": phase7_spelling.get(path, "none"), "runtime_status": "not-executed"}
            for field, value in expected.items():
                check(ledger[field] == value, f"P7A ledger mismatch: {path}.{field}")
            bucket = ("8-artifact-provenance-only-not-authorized" if original["kind"] == "generated-artifact" else
                      "7B-report-print-candidate-by-path-only" if re.search(r"(rpt|report|print|barcode|number2arabic)", Path(path).name, re.I) else
                      "7C-source-ui-resource-candidate-by-path-only")
            check(ledger["continuation_bucket"] == bucket and bool(ledger["next_scope_work"]),
                  f"P7A path-only continuation label mismatch/overclaim: {path}")
        check(sum(r["path_scope_state"] == "inventory-only-no-selected-scope" for r in ledger7) == 561,
              "P7A inventory-only count mismatch (not a completeness percentage)")
        witness7, witness7_match = recompute("evidence/feature-witnesses-07.json", "tools/check_feature_witnesses.py")
        illustrations7 = witness7["illustrations"]
        lexical7 = witness7["static_lexical_contract_checks"]
        sequential(illustrations7, "ALG7-", 12)
        sequential(lexical7, "ST7-", 8)
        related(illustrations7 + lexical7, known)
        check(witness7["phase"] == "7A-partial-static-audit" and
              witness7["illustration_count"] == 12 and witness7["static_lexical_contract_check_count"] == 8 and
              witness7["application_remediation_performed"] is False and
              witness7["secrets_or_real_employee_or_device_data_used"] is False,
              "P7A witness metadata/count/completion overclaim")
        for row in illustrations7 + lexical7:
            flag = "illustration_assertions_passed" if row["id"].startswith("ALG") else "documented_text_observation_matches"
            check(row["source_application_executed"] is False and bool(row["limit"]) and row[flag] is True,
                  f"P7A inconsistent audit-only illustration/text check: {row['id']}")
            evidence(row["evidence"], row["id"])
            scoped_evidence(row["evidence"], scope7_ranges, row["id"], phase=7)
        for filename, pattern, expected in (
            ("VALIDATION-07.md", r"^\| (P7T-\d{2}) \|", [r["id"] for r in tests7]),
            ("FEATURES-HR-PROJECTS-07.md", r"^\| (FE7-\d{2}) —", [r["id"] for r in features7]),
            ("FEATURES-HR-PROJECTS-07.md", r"^\| (CMD7-\d{2}) —", [r["id"] for r in commands7]),
            ("FEATURES-HR-PROJECTS-07.md", r"^\| (INV7-\d{2}) \|", [r["id"] for r in invariants7]),
            ("FEATURES-HR-PROJECTS-07.md", r"^\| (H7-\d{2}) —", [r["id"] for r in handoffs7]),
            ("FEATURES-HR-PROJECTS-07.md", r"^\| (Q7-\d{2}) \|", [r["id"] for r in questions7]),
            ("FEATURES-HR-PROJECTS-07.md", r"^\| (BK7-\d{2}) \|", [r["id"] for r in backlog7]),
        ):
            check(re.findall(pattern, read(AUDIT / filename), re.M) == expected,
                  f"P7A summary table IDs/order mismatch in {filename}: {pattern}")

    source_pattern = re.compile(
        r"((?:SmartAuditERP|SmartAuditUpdater)/[\w./-]+\.(?:cs|xaml|csproj|resx|config|settings))"
        r":(\d+(?:[-–]\d+)?(?:\s*[;،,]\s*\d+(?:[-–]\d+)?)*)")
    test_ids = {r["id"] for r in tests2 + tests3 + tests4 + tests5 + tests6 + tests7}
    # Historical views deliberately exclude mutable README/PLAN/IMPROVEMENTS
    # and newer-part Markdown. The current7B1 layer validates those separately.
    names = ["PHASE-01.md", "VALIDATION.md", "PHASE-02.md",
             "IDENTITY-AUTHORIZATION-02.md", "VALIDATION-02.md"]
    if through >= 3:
        names += ["PHASE-03.md", "ACCOUNTING-INTEGRITY-03.md", "VALIDATION-03.md"]
    if through >= 4:
        names += ["PHASE-04.md", "SALES-INVENTORY-04.md", "VALIDATION-04.md"]
    if through >= 5:
        names += ["PHASE-05.md", "SYNC-OFFLINE-05.md", "VALIDATION-05.md"]
    if through >= 6:
        names += ["PHASE-06.md", "INTEGRATIONS-06.md", "VALIDATION-06.md"]
    if through == 7:
        names += ["PHASE-07.md", "FEATURES-HR-PROJECTS-07.md", "VALIDATION-07.md"]
    documents = [AUDIT / n for n in names]
    for doc in documents:
        content = read(doc)
        for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", content):
            global LINK_COUNT
            target = match[1]
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            path = (doc.parent / unquote(parsed.path)).resolve()
            LINK_COUNT += 1
            check(path.exists(), f"Broken local link in {doc.name}: {target}")
        for match in source_pattern.finditer(content):
            source_ref(match[1], match[2], doc.name)
            if through >= 4 and doc.name in {"PHASE-04.md", "SALES-INVENTORY-04.md"}:
                # Normalize comma-separated Markdown same-file spans for scope inclusion.
                value = ";".join(f"{match[1]}:{a}-{b}" for a, b in spans(match[2]))
                scoped_evidence(value, scope4_ranges, doc.name)
            if through >= 5 and doc.name in {"PHASE-05.md", "SYNC-OFFLINE-05.md", "VALIDATION-05.md"}:
                value = ";".join(f"{match[1]}:{a}-{b}" for a, b in spans(match[2]))
                scoped_evidence(value, scope5_ranges, doc.name, phase=5)
            if through >= 6 and doc.name in {"PHASE-06.md", "INTEGRATIONS-06.md", "VALIDATION-06.md"}:
                value = ";".join(f"{match[1]}:{a}-{b}" for a, b in spans(match[2]))
                scoped_evidence(value, scope6_ranges, doc.name, phase=6)
            if through == 7 and doc.name in {"PHASE-07.md", "FEATURES-HR-PROJECTS-07.md", "VALIDATION-07.md"}:
                value = ";".join(f"{match[1]}:{a}-{b}" for a, b in spans(match[2]))
                scoped_evidence(value, scope7_ranges, doc.name, phase=7)
        for test in re.findall(r"\bP[234567]T-\d{2}\b", content):
            check(test in test_ids, f"Unknown acceptance plan in {doc.name}: {test}")

    syntax_tools = ["collect_baseline.py", "validate_audit.py", "check_financial_witnesses.py"]
    if through >= 4:
        syntax_tools.append("check_inventory_witnesses.py")
    if through >= 5:
        syntax_tools.append("check_sync_witnesses.py")
    if through >= 6:
        syntax_tools.append("check_integration_witnesses.py")
    if through == 7:
        syntax_tools += ["check_feature_witnesses.py", "test_audit_validator.py"]
    syntax_tools.append("audit_source_identity.py")
    for filename in syntax_tools:
        try:
            ast.parse(read(AUDIT / "tools" / filename), filename=filename)
        except SyntaxError as ex:
            check(False, f"Audit tool Python syntax error: {filename}: {ex}")

    report = {
        "audit_date_utc": "2026-11-16", "through_phase": through,
        "phase_7_delivery": "7A-partial" if through == 7 else "not-in-this-historical-check",
        "completed_static_phases_not_runtime_certification": list(range(1, min(through, 6) + 1)),
        "phase_7_remaining_parts": ["7B-not-started", "7C-not-started"] if through == 7 else [],
        "phase_8_authorized_or_started": False,
        "source_head": HEAD, "checkout_head": head, "source_reference_validation": source_identity, "branch": branch, "registry_used": registry_path,
        "method": "Offline source hashes and audit-document consistency; phase>=3 independent manually transcribed illustrations; phase>=4 separate bounded literal-source contract checks. NOT build, ERP/C#/SQL/MQTT/HTTP/SDK acceptance, exploit, provider/network or binary execution",
        "original_project_hashes_matching": len(project_paths) - len(changed),
        "scope_files": {**{name: len(paths) for name, paths in scopes.items()},
                        "historical_phase_1_2_union": len(union12),
                        "historical_phase_1_2_3_union": len(union123) if through >= 3 else None,
                        "phase_3_overlap_with_prior_union": 15 if through >= 3 else None,
                        "historical_phase_1_2_3_4_union": len(union1234) if through >= 4 else None,
                        "phase_4_overlap_with_prior_union": 15 if through >= 4 else None,
                        "phase_4_new_paths": 33 if through >= 4 else None,
                        "phase_5_overlap_with_prior_union": 24 if through >= 5 else None,
                        "phase_5_new_paths": 30 if through >= 5 else None,
                        "historical_phase_1_2_3_4_5_union": len(union12345) if through >= 5 else None,
                        "phase_6_overlap_with_prior_union": 17 if through >= 6 else None,
                        "phase_6_new_paths": 36 if through >= 6 else None,
                        "historical_phase_1_2_3_4_5_6_union": len(union123456) if through >= 6 else None,
                        "phase_7A_overlap_with_prior_union": 7 if through == 7 else None,
                        "phase_7A_new_paths": 40 if through == 7 else None,
                        "inventory_only_no_selected_scope": len(project_paths - union),
                        "unique_union_not_line_or_execution_coverage": len(union)},
        "findings": {**{f"phase_{n}": len(data) for n, data in phase_rows.items()},
                     "total_open_not_remediated": len(findings),
                     "severity": dict(collections.Counter(r["severity"] for r in findings)),
                     "certainty": dict(collections.Counter(r["certainty"] for r in findings))},
        "phase_2_historical_evidence": {
            "frozen_registry": prov3["registry_at_entry_snapshot"],
            "frozen_registry_sha256_matches": sha(AUDIT / prov3["registry_at_entry_snapshot"]) == prov3["registry_at_entry_sha256"],
            "earlier_report_evidence_artifacts_hash_checked": 14,
            "historical_check_record_overwritten": False,
            "evidence_extensions_during_phase_3_without_reclassification": ext3,
        },
        "phase_3_historical_evidence": None if prov4 is None else {
            "frozen_registry": prov4["registry_at_entry_snapshot"],
            "frozen_registry_sha256_matches": sha(AUDIT / prov4["registry_at_entry_snapshot"]) == prov4["registry_at_entry_sha256"],
            "earlier_report_evidence_artifacts_hash_checked": 26,
            "historical_check_record_overwritten": False,
            "current_registry_evidence_extensions_without_reclassification": ext4,
        },
        "phase_4_historical_evidence": None if prov5 is None else {
            "frozen_registry": prov5["registry_at_entry_snapshot"],
            "frozen_registry_sha256_matches": sha(AUDIT / prov5["registry_at_entry_snapshot"]) == prov5["registry_at_entry_sha256"],
            "earlier_report_evidence_artifacts_hash_checked": 38,
            "historical_check_record_overwritten": False,
            "current_registry_evidence_extensions_without_reclassification": ext5,
            "next_phase_replans_after_static_review_not_remediation":
                {"P1-014": {"from": "5", "to": "8", "reason": "External broker TLS/auth/ACL deployment acceptance still unexecuted"}} if through >= 5 else {},
        },
        "phase_5_historical_evidence": None if prov6 is None else {
            "frozen_registry": prov6["registry_at_entry_snapshot"],
            "frozen_registry_sha256_matches": sha(AUDIT / prov6["registry_at_entry_snapshot"]) == prov6["registry_at_entry_sha256"],
            "earlier_report_evidence_artifacts_hash_checked": 53,
            "historical_check_record_overwritten": False,
            "current_registry_evidence_extensions_without_reclassification": ext6,
            "next_phase_replans_after_static_review_not_remediation":
                {"P1-032": {"from": "6", "to": "8", "reason": "External entitlement policy/backend/device/offline acceptance remains unexecuted; no empty follow-up"}} if through >= 6 else {},
        },
        "phase_6_historical_evidence": None if prov7 is None else {
            "frozen_registry": prov7["registry_at_entry_snapshot"],
            "frozen_registry_sha256_matches": sha(AUDIT / prov7["registry_at_entry_snapshot"]) == prov7["registry_at_entry_sha256"],
            "earlier_report_evidence_artifacts_hash_checked": 67,
            "historical_check_record_overwritten": False,
            "current_registry_evidence_extensions_without_reclassification": ext7,
            "next_phase_followups_preserved_for_all172_during_partial7": through == 7,
            "historical_findings_still_scheduled_for7": 43 if through == 7 else None,
            "next_phase_replans_during_partial7": {},
        },
        "evidence_rows": {"phase_2_identity_flows": len(identity),
                          "phase_2_authorization_scenarios": len(acl),
                          "phase_2_sql_trace_groups_not_vulnerabilities": len(sql),
                          "phase_2_sql_classification": dict(sql_types),
                          "phase_2_unexecuted_acceptance_plans": len(tests2),
                          "phase_3_accounting_invariants_not_passed_tests": len(invariants3),
                          "phase_3_document_lifecycles": len(lifecycles3),
                          "phase_3_unexecuted_acceptance_plans": len(tests3),
                          "phase_3_independent_algebra_illustrations_not_erp_tests": len(illustrations3),
                          "phase_3_illustrations_recomputed_match_saved": witness3_match,
                          "phase_4_inventory_invariants_not_passed_tests": len(invariants4),
                          "phase_4_document_state_financial_inventory_effect_rows": len(matrix4),
                          "phase_4_unexecuted_acceptance_plans": len(tests4),
                          "phase_4_independent_illustrations_not_erp_tests": len(illustrations4),
                          "phase_4_static_parameter_name_set_checks_not_sql_tests": len(parameter4),
                          "phase_4_illustrations_and_text_checks_recomputed_match_saved": witness4_match,
                          "phase_5_sync_flows": len(flows5),
                          "phase_5_data_ownership_groups": len(owners5),
                          "phase_5_mqtt_topic_contract_rows_not_findings": len(topics5),
                          "phase_5_failure_conflict_rows": len(matrix5),
                          "phase_5_sync_invariants_not_passed_tests": len(invariants5),
                          "phase_5_unexecuted_acceptance_plans": len(tests5),
                          "phase_5_independent_illustrations_not_erp_tests": len(illustrations5),
                          "phase_5_static_lexical_contract_checks_not_application_tests": len(lexical5),
                          "phase_5_illustrations_and_text_checks_recomputed_match_saved": witness5_match,
                          "phase_6_provider_contracts_not_vendor_certification": len(contracts6),
                          "phase_6_integration_invariants_not_passed_tests": len(invariants6),
                          "phase_6_failure_case_rows_not_additional_findings": len(matrix6),
                          "phase_6_unexecuted_acceptance_plans": len(tests6),
                          "phase_6_public_official_references_read_only_not_body_hashed": len(sources6),
                          "phase_6_independent_illustrations_not_erp_tests": len(illustrations6),
                          "phase_6_static_lexical_contract_checks_not_application_tests": len(lexical6),
                          "phase_6_illustrations_and_text_checks_recomputed_match_saved": witness6_match,
                          "phase_7A_feature_screen_implementation_test_matrix_rows_not_completed_features": len(features7),
                          "phase_7A_command_groups_not_new_findings": len(commands7),
                          "phase_7A_invariants_not_passed_tests": len(invariants7),
                          "phase_7A_unexecuted_acceptance_plans": len(tests7),
                          "phase_7A_handoffs_not_absence_proof": len(handoffs7),
                          "phase_7A_unanswered_policy_contract_questions": len(questions7),
                          "phase_7A_historical_evidence_only_extensions": len(extensions7_rows),
                          "phase_7A_continuation_groups_not_started": len(backlog7),
                          "phase_7A_original_paths_in_coverage_ledger_not_reading_certification": len(ledger7),
                          "phase_7A_independent_illustrations_not_erp_tests": len(illustrations7),
                          "phase_7A_static_lexical_checks_not_application_tests": len(lexical7),
                          "phase_7A_illustrations_and_text_checks_recomputed_match_saved": witness7_match},
        "validation": {"source_range_references_checked_including_repeats": REFERENCE_COUNT,
                       "local_markdown_links_checked_including_repeats": LINK_COUNT,
                       "audit_only_python_tools_syntax_checked": syntax_tools,
                       "errors": ERRORS,
                       "limit": "Bounds, IDs, links, selected-range inclusion, hash continuity and audit-only illustration/text recomputation; NOT semantic/financial certification, deployed-schema checks, WPF rendering or acceptance execution. Output record not self-hashed."},
        "historical_artifact_sha256": ((prov7 if through == 7 else None) or prov6 or prov5 or prov4 or prov3)["historical_artifact_sha256"],
        "date_semantics": "Declared audit reference date2026-11-16; sandbox clock/public reference retrieval observed2026-11-17 recorded separately in provenance06/07. No application/provider tests on either date.",
        "erp_runtime_tests_executed": 0, "sql_or_external_service_tests_executed": 0,
        "application_remediation_performed": False,
    }
    if through == 7:
        report["phase_7A_historical_input_mode"] = "frozen200-and-protected7A-artifacts-not-current-shared-indexes"
        report["validation"]["limit"] += " Historical7A current-checker recomputation is not a claim of byte-identical reproduction of the original checks-07 metrics."
        if phase7_part in {"B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
            from validate_financial_report_part import validate_frozen_b1
            prov7b2, frozen223 = provenance("evidence/provenance-07B2.json", 110, 223)
            validate_frozen_b1(sys.modules[__name__], report, prov7b, frozen200, prov7b2, frozen223)
            if phase7_part in {"B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                from validate_commercial_report_part import validate_frozen_b2
                prov7b3, frozen237 = provenance("evidence/provenance-07B3.json", 132, 237)
                validate_frozen_b2(sys.modules[__name__], report, prov7b2, frozen223, prov7b, prov7b3, frozen237)
                if phase7_part in {"B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                    from validate_invoice_analysis_part import validate_frozen_b3
                    prov7b4, frozen248 = provenance("evidence/provenance-07B4.json", 155, 248)
                    validate_frozen_b3(sys.modules[__name__], report, prov7b3, frozen237, prov7b4, frozen248)
                    if phase7_part in {"B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                        from validate_sales_report_part import validate_frozen_b4
                        prov7b5, frozen261 = provenance("evidence/provenance-07B5.json", 178, 261)
                        validate_frozen_b4(sys.modules[__name__], report, prov7b4, frozen248, prov7b5, frozen261)
                        if phase7_part in {"B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                            from validate_pos_totals_part import validate_frozen_b5
                            prov7b6, frozen266 = provenance("evidence/provenance-07B6.json", 199, 266)
                            validate_frozen_b5(sys.modules[__name__], report, prov7b5, frozen261, prov7b6, frozen266)
                            if phase7_part in {"B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                from validate_financial_controls_part import validate_frozen_b6
                                prov7b7, frozen270 = provenance("evidence/provenance-07B7.json", 223, 270)
                                validate_frozen_b6(sys.modules[__name__], report, prov7b6, frozen266, prov7b7, frozen270)
                                if phase7_part in {"B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                    from validate_decision_summary_part import validate_frozen_b7
                                    prov7b8, frozen276 = provenance("evidence/provenance-07B8.json", 246, 276)
                                    validate_frozen_b7(sys.modules[__name__], report, prov7b7, frozen270, prov7b8, frozen276)
                                    if phase7_part in {"B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                        from validate_receipt_payroll_part import validate_frozen_b8
                                        prov7b9, frozen280 = provenance("evidence/provenance-07B9.json", 269, 280)
                                        validate_frozen_b8(sys.modules[__name__], report, prov7b8, frozen276, prov7b9, frozen280)
                                        if phase7_part in {"B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                            from validate_salesman_contract_part import validate_frozen_b9
                                            prov7b10, frozen282 = provenance("evidence/provenance-07B10.json", 292, 282)
                                            validate_frozen_b9(sys.modules[__name__], report, prov7b9, frozen280, prov7b10, frozen282)
                                            if phase7_part in {"B10", "B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                from validate_statement_contract_part import validate_frozen_b10
                                                prov7b11, frozen285 = provenance("evidence/provenance-07B11.json", 315, 285)
                                                validate_frozen_b10(sys.modules[__name__], report, prov7b10, frozen282, prov7b11, frozen285)
                                                if phase7_part in {"B11", "B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                    from validate_income_contract_part import validate_frozen_b11
                                                    prov7b12, frozen287 = provenance("evidence/provenance-07B12.json", 338, 287)
                                                    validate_frozen_b11(sys.modules[__name__], report, prov7b11, frozen285, prov7b12, frozen287)
                                                    if phase7_part in {"B12", "B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                        from validate_trial_balance_part import validate_frozen_b12
                                                        prov7b13, frozen289 = provenance("evidence/provenance-07B13.json", 361, 289)
                                                        validate_frozen_b12(sys.modules[__name__], report, prov7b12, frozen287, prov7b13, frozen289)
                                                        if phase7_part in {"B13", "B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                            from validate_inventory_activity_part import validate_frozen_b13
                                                            prov7b14, frozen291 = provenance("evidence/provenance-07B14.json", 387, 291)
                                                            validate_frozen_b13(sys.modules[__name__], report, prov7b13, frozen289, prov7b14, frozen291)
                                                            if phase7_part in {"B14", "B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                                from validate_accrual_tax_part import validate_frozen_b14, extend_accrual_tax
                                                                prov7b15, frozen294 = provenance("evidence/provenance-07B15.json", 413, 294)
                                                                validate_frozen_b14(sys.modules[__name__], report, prov7b14, frozen291, prov7b15, frozen294)
                                                                if phase7_part in {"B15", "B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                                    from validate_shared_contract_part import validate_frozen_b15, extend_shared_contracts
                                                                    prov7b16, frozen298 = provenance("evidence/provenance-07B16.json", 440, 298)
                                                                    validate_frozen_b15(sys.modules[__name__], report, prov7b15, frozen294, prov7b16, frozen298)
                                                                    if phase7_part in {"B16", "B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                                        from validate_consolidation_part import validate_frozen_b16, extend_consolidation
                                                                        prov7b17, frozen299 = provenance("evidence/provenance-07B17.json", 468, 299)
                                                                        validate_frozen_b16(sys.modules[__name__], report, prov7b16, frozen298, prov7b17, frozen299)
                                                                        if phase7_part in {"B17", "B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                                            from validate_caller_request_part import validate_frozen_b17, extend_caller_requests
                                                                            prov7b18, frozen300 = provenance("evidence/provenance-07B18.json", 495, 300)
                                                                            validate_frozen_b17(sys.modules[__name__], report, prov7b17, frozen299, prov7b18, frozen300)
                                                                            if phase7_part in {"B18", "B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                                                from validate_navigation_contract_part import validate_frozen_b18, extend_navigation_contracts
                                                                                prov7b19, frozen302 = provenance("evidence/provenance-07B19.json", 523, 302)
                                                                                validate_frozen_b18(sys.modules[__name__], report, prov7b18, frozen300, prov7b19, frozen302)
                                                                                if phase7_part in {"B19", "B20", "B21", "B22", "B23", "B24", "B25", "B26", "B27", "B28", "B29"}:
                                                                                    from validate_barcode_contract_part import historical_b19_validation, extend_barcode_contracts
                                                                                    prov7b20, frozen307 = provenance("evidence/provenance-07B20.json", 553, 307)
                                                                                    with historical_b19_validation(sys.modules[__name__], report, prov7b19, prov7b20, frozen307) as historical_b19:
                                                                                        extend_navigation_contracts(historical_b19, report, prov7b19, frozen302)
                                                                                    if phase7_part == "B19":
                                                                                        report["phase_7B19_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                    else:
                                                                                        from validate_amountword_contract_part import historical_b20_validation, extend_amountword_contracts
                                                                                        prov7b21, frozen310 = provenance("evidence/provenance-07B21.json", 583, 310)
                                                                                        with historical_b20_validation(sys.modules[__name__], report, prov7b20, prov7b21, frozen310) as historical_b20:
                                                                                            extend_barcode_contracts(historical_b20, report, prov7b20, frozen307)
                                                                                        if phase7_part == "B20":
                                                                                            report["phase_7B20_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                        else:
                                                                                            from validate_contract_item_part import historical_b21_validation, extend_contract_items
                                                                                            prov7b22, frozen313 = provenance("evidence/provenance-07B22.json", 613, 313)
                                                                                            with historical_b21_validation(sys.modules[__name__], report, prov7b21, prov7b22, frozen313) as historical_b21:
                                                                                                extend_amountword_contracts(historical_b21, report, prov7b21, frozen310)
                                                                                            if phase7_part == "B21":
                                                                                                report["phase_7B21_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                            else:
                                                                                                from validate_item_ingress_part import historical_b22_validation, extend_item_ingress
                                                                                                prov7b23, frozen316 = provenance("evidence/provenance-07B23.json", 643, 316)
                                                                                                with historical_b22_validation(sys.modules[__name__], report, prov7b22, prov7b23, frozen316) as historical_b22:
                                                                                                    extend_contract_items(historical_b22, report, prov7b22, frozen313)
                                                                                                if phase7_part == "B22":
                                                                                                    report["phase_7B22_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                else:
                                                                                                    from validate_row_ownership_part import historical_b23_validation, extend_row_ownership
                                                                                                    prov7b24, frozen319 = provenance("evidence/provenance-07B24.json", 673, 319)
                                                                                                    with historical_b23_validation(sys.modules[__name__], report, prov7b23, prov7b24, frozen319) as historical_b23:
                                                                                                        extend_item_ingress(historical_b23, report, prov7b23, frozen316)
                                                                                                    if phase7_part == "B23":
                                                                                                        report["phase_7B23_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                    else:
                                                                                                        from validate_property_dialog_part import historical_b24_validation, extend_property_dialogs
                                                                                                        prov7b25, frozen322 = provenance("evidence/provenance-07B25.json", 703, 322)
                                                                                                        with historical_b24_validation(sys.modules[__name__], report, prov7b24, prov7b25, frozen322) as historical_b24:
                                                                                                            extend_row_ownership(historical_b24, report, prov7b24, frozen319)
                                                                                                        if phase7_part == "B24":
                                                                                                            report["phase_7B24_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                        else:
                                                                                                            from validate_bulk_product_part import historical_b25_validation, extend_bulk_products
                                                                                                            prov7b26, frozen324 = provenance("evidence/provenance-07B26.json", 734, 324)
                                                                                                            with historical_b25_validation(sys.modules[__name__], report, prov7b25, prov7b26, frozen324) as historical_b25:
                                                                                                                extend_property_dialogs(historical_b25, report, prov7b25, frozen322)
                                                                                                            if phase7_part == "B25":
                                                                                                                report["phase_7B25_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                            else:
                                                                                                                from validate_invoice_search_part import historical_b26_validation, extend_invoice_search
                                                                                                                prov7b27, frozen326 = provenance("evidence/provenance-07B27.json", 765, 326)
                                                                                                                with historical_b26_validation(sys.modules[__name__], report, prov7b26, prov7b27, frozen326) as historical_b26:
                                                                                                                    extend_bulk_products(historical_b26, report, prov7b26, frozen324)
                                                                                                                if phase7_part == "B26":
                                                                                                                    report["phase_7B26_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                                else:
                                                                                                                    from validate_search_snapshot_part import historical_b27_validation, extend_search_snapshot
                                                                                                                    prov7b28, frozen329 = provenance("evidence/provenance-07B28.json", 797, 329)
                                                                                                                    with historical_b27_validation(sys.modules[__name__], report, prov7b27, prov7b28, frozen329) as historical_b27:
                                                                                                                        extend_invoice_search(historical_b27, report, prov7b27, frozen326)
                                                                                                                    if phase7_part == "B27":
                                                                                                                        report["phase_7B27_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                                    else:
                                                                                                                        from validate_dirty_navigation_part import historical_b28_validation, extend_dirty_navigation
                                                                                                                        prov7b29, frozen330 = provenance("evidence/provenance-07B29.json", 829, 330)
                                                                                                                        with historical_b28_validation(sys.modules[__name__], report, prov7b28, prov7b29, frozen330) as historical_b28:
                                                                                                                            extend_search_snapshot(historical_b28, report, prov7b28, frozen329)
                                                                                                                        if phase7_part == "B28":
                                                                                                                            report["phase_7B28_checked_as_explicit_historical_mode_not_current_default"] = True
                                                                                                                        else:
                                                                                                                            extend_dirty_navigation(sys.modules[__name__], report, prov7b29, frozen330)
    # New-part checks increment the same counters/errors without writing files.
    report["validation"]["source_range_references_checked_including_repeats"] = REFERENCE_COUNT
    report["validation"]["local_markdown_links_checked_including_repeats"] = LINK_COUNT
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if ERRORS else 0


# Public compatibility descriptors are functional choices bases, not today's
# parser. B16/B17 protected callers depend on these objects. Only LIVE is used
# by the actual entrypoint, and current tests inspect that parser and routing.
PHASE7_B16_CLI = dict(choices=("A", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "B11", "B12", "B13", "B14", "B15", "B16"), default="B16")
PHASE7_CURRENT_CLI = PHASE7_B16_CLI | dict(choices=PHASE7_B16_CLI["choices"] + ("B17",), default="B17")
PHASE7_B18_CLI = PHASE7_CURRENT_CLI | dict(choices=PHASE7_CURRENT_CLI["choices"] + ("B18",), default="B18")
PHASE7_B19_CLI = PHASE7_B18_CLI | dict(choices=PHASE7_B18_CLI["choices"] + ("B19",), default="B19")
PHASE7_B20_CLI = PHASE7_B19_CLI | dict(choices=PHASE7_B19_CLI["choices"] + ("B20",), default="B20")
PHASE7_B21_CLI = PHASE7_B20_CLI | dict(choices=PHASE7_B20_CLI["choices"] + ("B21",), default="B21")
PHASE7_B22_CLI = PHASE7_B21_CLI | dict(choices=PHASE7_B21_CLI["choices"] + ("B22",), default="B22")
PHASE7_B23_CLI = PHASE7_B22_CLI | dict(choices=PHASE7_B22_CLI["choices"] + ("B23",), default="B23")
PHASE7_B24_CLI = PHASE7_B23_CLI | dict(choices=PHASE7_B23_CLI["choices"] + ("B24",), default="B24")
PHASE7_B25_CLI = PHASE7_B24_CLI | dict(choices=PHASE7_B24_CLI["choices"] + ("B25",), default="B25")
PHASE7_B26_CLI = PHASE7_B25_CLI | dict(choices=PHASE7_B25_CLI["choices"] + ("B26",), default="B26")
PHASE7_B27_CLI = PHASE7_B26_CLI | dict(choices=PHASE7_B26_CLI["choices"] + ("B27",), default="B27")
PHASE7_B28_CLI = PHASE7_B27_CLI | dict(choices=PHASE7_B27_CLI["choices"] + ("B28",), default="B28")
PHASE7_LIVE_CLI = PHASE7_B28_CLI | dict(choices=PHASE7_B28_CLI["choices"] + ("B29",), default="B29")


def build_cli_parser():
    """Real current parser; immutable versioned descriptors are not defaults."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--through-phase", type=int, choices=(2, 3, 4, 5, 6, 7), default=7,
                        help="Default7 is7A+B1..B29/R4m partial;2..6 use OWN frozen historical inputs")
    parser.add_argument("--phase7-part", **PHASE7_LIVE_CLI,
                        help="A/B1..B28 historical OWN inputs; B28=OWN330/raw331CRLF/indexes and ALL48 original cases in explicit presetB28 child with suite-local A.52B27/48B26/44B25/44B24 and earlier retained. B29(default)=current331,one Medium local159 accepted-search dirty-guard omission in sale/purchase then Navigate/CLR before reader. Supplied dirty flags/counts and normal CLR completion,not DTO defaults or WPF/provider/save observation. Fresh not-done/sentinel/guardNo/Yes/clean controls;target acceptance is not abandon approval. Seven existing paths/22 bounded slices/whole0,zero new->union426/complement401 not all callers/reader/fields/477bodies/455FE or percent.330metadata/80pathmatches plus selected nearest bodies not all bodies.16FE/INV/32 integrated plans not-executed;RS14/SP3/HQ6 preserve full ancestry/input prefixes/routes/dispositions.829/all330 exact dictionaries/ALLnext_phase/evidence/raw331CRLFprefix/G232/827 originals/3freezes preserved;no protected edits/skips/globalPath/sharedsubprocess mutation/diskoverlay/rebaseline/archive rewrite.014/132/145 potential,020/021 and financial/ACL/stock/save/production barriers remain;015/046/061/091/148/151/155–158not recounted,no new extension. Actual34 historical capture-time tools/identities and single later inverse-pin proof,not final/postpush wholesale replay. Session reference2026-11-16/raw clock/source10ba/officialB28capture436/deliveredB28entrydda distinct. No ERP/build/WPF/.NET/SQL/SDK/provider/GC/saved loss/remediation/measurement/operational acceptance. No repair merge or assumed start/sync. R4n/7B30 proposed or reasoned split;7B/7partial,7Cunstarted,8unauthorized,next_phase8planningonly;counts not sessions/completion percent.")
    return parser


if __name__ == "__main__":
    args = build_cli_parser().parse_args()
    sys.exit(main(args.through_phase, args.phase7_part))
