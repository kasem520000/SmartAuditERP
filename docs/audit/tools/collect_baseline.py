#!/usr/bin/env python3
"""Offline, read-only source inventory for the SmartAuditERP audit.

Default: print aggregate observations. --write writes ONLY audit evidence files.
--verify compares current project-file hashes with the recorded inventory.
This is not a C# compiler, test runner, vulnerability scanner or proof of safety.
No assemblies are loaded, serialized resources decoded, SQL executed, or network used.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs" / "audit"
EVIDENCE = AUDIT / "evidence"
XCLASS = "{http://schemas.microsoft.com/winfx/2006/xaml}Class"
TEXT_SUFFIXES = {".cs", ".xaml", ".csproj", ".sln", ".resx", ".config", ".settings", ".user", ".json", ".txt", ".props", ".targets", ".editorconfig", ".cache", ".BuildWithSkipAnalyzers"}
XML_SUFFIXES = {".xaml", ".csproj", ".resx", ".config", ".settings"}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def project_paths() -> list[str]:
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    return sorted(p for p in paths if p and (p == "SmartAuditERP.sln" or p.startswith(("SmartAuditERP/", "SmartAuditUpdater/"))))


def generated(path: str) -> bool:
    return bool({"bin", "obj"} & set(Path(path).parts))


def source(path: str) -> bool:
    return Path(path).suffix in {".cs", ".xaml"} and not generated(path)


def decode(data: bytes) -> tuple[str, str]:
    try:
        return data.decode("utf-8-sig"), "utf-8"
    except UnicodeDecodeError:
        # A reading fallback only. This does NOT prove the intended source code page.
        return data.decode("cp1256", errors="replace"), "non-utf8; cp1256-reading-fallback"


def text(path: str) -> str:
    return decode((ROOT / path).read_bytes())[0]


def manual_scope() -> dict[str, dict[str, str]]:
    with (AUDIT / "review-scope.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    result = {}
    for row in rows:
        if row["path"] in result:
            raise ValueError(f"Duplicate scope path: {row['path']}")
        if not (ROOT / row["path"]).is_file():
            raise ValueError(f"Missing scope path: {row['path']}")
        result[row["path"]] = row
    return result


def inventory(paths: list[str], scope: dict) -> list[dict]:
    result = []
    for path in paths:
        p = ROOT / path
        data = p.read_bytes()
        is_text = p.suffix in TEXT_SUFFIXES
        content, encoding = decode(data) if is_text else ("", "binary-not-loaded")
        kind = "generated-artifact" if generated(path) else "source" if source(path) else "project-or-resource"
        row = scope.get(path, {})
        result.append({
            "path": path,
            "kind": kind,
            "bytes": len(data),
            "lines": len(content.splitlines()) if is_text else "",
            "encoding_observation": encoding,
            "sha256": hashlib.sha256(data).hexdigest(),
            "review_state": row.get("review_state", "generated-metadata-only" if generated(path) else "inventory-only"),
            "reviewed_ranges": row.get("ranges", ""),
        })
    return result


def collect(paths: list[str], rows: list[dict]) -> dict:
    src = [r for r in rows if source(r["path"])]
    gen = [r for r in rows if generated(r["path"])]
    xml_errors = []
    roots = {}
    for path in paths:
        if not generated(path) and Path(path).suffix in XML_SUFFIXES:
            try:
                roots[path] = ET.parse(ROOT / path).getroot()
            except ET.ParseError as ex:
                xml_errors.append({"path": path, "error": str(ex)})
    classes = collections.defaultdict(list)
    mismatches = []
    for path, root in roots.items():
        if not path.endswith(".xaml"):
            continue
        xc = root.get(XCLASS)
        if not xc:
            continue
        classes[xc].append(path)
        cb = path + ".cs"
        if cb not in paths:
            mismatches.append({"path": path, "reason": "missing-codebehind"})
            continue
        code = text(cb)
        ns = re.search(r"\bnamespace\s+([\w.]+)", code)
        if not ns or ns[1] != xc.rsplit(".", 1)[0] or not re.search(r"\bclass\s+" + re.escape(xc.rsplit(".", 1)[-1]) + r"\b", code):
            mismatches.append({"path": path, "reason": "class-or-namespace-name-mismatch"})

    packages, references, projects = [], [], []
    for path in paths:
        if not path.endswith(".csproj"):
            continue
        root = roots[path]
        props = {x.tag: (x.text or "") for pg in root.findall("PropertyGroup") for x in pg}
        projects.append({"path": path, "properties": props})
        for p in root.findall(".//PackageReference"):
            packages.append({"project": path, "name": p.get("Include"), "version": p.get("Version")})
        for ref in root.findall(".//Reference"):
            hint = ref.findtext("HintPath", "")
            references.append({
                "project": path,
                "assembly": ref.get("Include"),
                "hint_kind": "absolute-developer-profile" if re.match(r"[A-Za-z]:", hint) else "relative-external" if hint.startswith("..\\..\\") else "other",
                # Do not reproduce developer profile names from local HintPaths.
                "hint_filename": hint.replace("\\", "/").split("/")[-1],
            })

    resources = []
    resx_path = "SmartAuditERP/Properties/Resources.resx"
    resx_lines = text(resx_path).splitlines()
    for key in ("CrystalLiteDB", "AlterDb"):
        item = next(x for x in roots[resx_path].findall("data") if x.get("name") == key)
        value = item.findtext("value", "")
        lines = value.splitlines()
        nonstandalone = [n for n, line in enumerate(lines, 1) if "GO" in line and not re.fullmatch(r"\s*GO\s*", line)]
        start = next(n for n, line in enumerate(resx_lines, 1) if f'<data name="{key}"' in line)
        resources.append({"name": key, "resx_entry_line": start, "lines": len(lines), "characters": len(value), "uppercase_GO_occurrences": value.count("GO"), "nonstandalone_GO_resource_lines": nonstandalone})

    empty_handlers = []
    not_implemented = []
    lexical = collections.Counter()
    lexical_files = collections.Counter()
    patterns = {
        "sql_adapter": r"new\s+SqlDataAdapter\s*\(",
        "sql_command": r"new\s+SqlCommand\s*\(",
        "begin_transaction": r"BeginTransaction\s*\(",
        "empty_click_handler": r"\bvoid\s+(\w+_Click)\([^\n]*\)\s*\{\s*\}",
    }
    for path in paths:
        if not source(path) or not path.endswith(".cs"):
            continue
        code = text(path)
        for label, pat in patterns.items():
            hits = list(re.finditer(pat, code))
            lexical[label] += len(hits)
            if hits:
                lexical_files[label] += 1
            if label == "empty_click_handler":
                for m in hits:
                    empty_handlers.append({"path": path, "line": code[:m.start()].count("\n") + 1, "method": m[1]})
        for m in re.finditer(r"throw\s+new\s+NotImplementedException", code):
            not_implemented.append({"path": path, "line": code[:m.start()].count("\n") + 1})

    # These booleans corroborate narrowly defined source observations, not exploitability.
    login = text("SmartAuditERP/Form_WPF/frmUserLogin.xaml.cs")
    setup = text("SmartAuditERP/Form_WPF/frmServerSetting.xaml.cs")
    upd = text("SmartAuditUpdater/MainWindow.xaml.cs")
    acl = text("SmartAuditERP/Class/MainClass.cs")
    backup = text("SmartAuditERP/Form_WPF/frmBackupRstore.xaml.cs")
    facts = {
        "P1-007_privileged_server_role_command_present": "ALTER SERVER ROLE [sysadmin] ADD MEMBER" in setup,
        "P1-007_sa_enable_command_present": "ALTER LOGIN sa ENABLE" in setup,
        "P1-008_fixed_password_validator_present": "ValidateFixedPassword" in text("SmartAuditERP/Form_WPF/frmCheckPwd.xaml.cs"),
        "P1-009_password_assigned_to_serialized_startup_data": "Password = txtPwd.Password" in login and "SerializeObject(startupData" in login,
        "P1-012_no_permission_row_returns_without_deny": "if (dt.Rows.Count == 0) return;" in acl,
        "legacy_items_permission_alias_present_not_itself_a_defect": 'formName = "frmcurrency";' in acl,
        "P1-013_visual_tree_traversal_used_for_permissions": "VisualTreeHelper.GetChildrenCount(parent)" in acl,
        "P1-014_mqtt_explicitly_insecure": "secure: false" in text("SmartAuditERP/Class/ConnectBroker.cs"),
        "P1-015_ftp_upload_and_literal_credential_constructor_present": "Ftp.UploadFile" in backup and bool(re.search(r'new NetworkCredential\("[^"\n]+", "[^"\n]+"\)', backup)),
        "P1-021_download_failure_early_return_present": "if (!downloaded) return;" in upd,
        "P1-022_copy_failure_only_logged": bool(re.search(r'if \(!copied\)\s+AddLog', upd)),
        "P1-027_migration_error_counter_present": "errorCount++" in text("SmartAuditERP/Home.xaml.cs"),
    }
    fileset = set(paths)
    return {
        "audit_date_utc": "2026-11-16",
        "source_head_at_collection": git("rev-parse", "HEAD"),
        "branch": git("branch", "--show-current"),
        "scope": "Git-tracked SmartAuditERP.sln and the two project trees; excludes audit documentation",
        "method": "Offline metadata and lexical inspection only; no C# compilation, runtime, SQL, binary loading or network access",
        "environment": {"os": platform.system(), "machine": platform.machine(), "python": platform.python_version(), "dotnet_available": bool(shutil.which("dotnet")), "msbuild_available": bool(shutil.which("msbuild"))},
        "statistics": {
            "tracked_project_files": len(paths), "tracked_project_bytes": sum(r["bytes"] for r in rows),
            "source_files_excluding_bin_obj": len(src), "source_lines_including_comments_and_designer": sum(int(r["lines"]) for r in src),
            "cs_files": sum(r["path"].endswith(".cs") for r in src), "cs_lines": sum(int(r["lines"]) for r in src if r["path"].endswith(".cs")),
            "xaml_files": sum(r["path"].endswith(".xaml") for r in src), "xaml_lines": sum(int(r["lines"]) for r in src if r["path"].endswith(".xaml")),
            "wpf_form_xaml_files": sum(Path(r["path"]).parent.name == "Form_WPF" and r["path"].endswith(".xaml") for r in src),
            "tracked_generated_files": len(gen), "tracked_generated_bytes": sum(r["bytes"] for r in gen),
            "bin_files": sum("bin" in Path(r["path"]).parts for r in gen), "obj_files": sum("obj" in Path(r["path"]).parts for r in gen),
            "manually_scoped_files": sum(r["review_state"] not in {"inventory-only", "generated-metadata-only"} for r in rows),
        },
        "source_non_utf8_paths": [r["path"] for r in src if r["encoding_observation"] != "utf-8"],
        "xml": {"examined": len(roots) + len(xml_errors), "parse_errors": xml_errors, "limit": "Well-formed XML only; not WPF binding, resource-type or event-handler validation"},
        "xaml_codebehind_name_check": {"classes": len(classes), "mismatches": mismatches, "duplicate_classes": {k: v for k, v in classes.items() if len(v) > 1}, "limit": "Class/namespace name presence only, not compilation or inheritance correctness"},
        "projects": projects, "package_references": packages, "assembly_references": references,
        "repository_asset_observations": {
            "root_gitignore_present": ".gitignore" in fileset,
            "version_txt_present": any(Path(p).name == "Version.txt" for p in paths),
            "log4net_config_present": any(Path(p).name.lower() == "log4net.config" for p in paths),
            "repx_templates": sum(p.lower().endswith(".repx") for p in paths),
            "versioned_github_workflows": git("ls-files", ".github/workflows"),
            "test_projects_by_project_manifest": [p for p in paths if p.endswith(".csproj") and re.search(r"Microsoft\.NET\.Test\.Sdk|xunit|NUnit|MSTest", text(p), re.I)],
        },
        "sql_resources_metadata_only": resources,
        "lexical_indicators_not_findings": {k: {"occurrences": v, "files": lexical_files[k]} for k, v in lexical.items()},
        "empty_click_handler_candidates_not_all_confirmed_missing_features": empty_handlers,
        "not_implemented_exception_locations_not_automatically_defects": not_implemented,
        "narrow_static_corroboration_not_exploit_tests": facts,
    }


def csv_text(rows: list[dict]) -> str:
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write audit evidence only")
    mode.add_argument("--verify", action="store_true", help="Compare current tracked project hashes with the recorded inventory")
    args = parser.parse_args()
    paths = project_paths()
    rows = inventory(paths, manual_scope())
    report = collect(paths, rows)
    if args.write:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        (EVIDENCE / "baseline.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (EVIDENCE / "inventory.csv").write_text(csv_text(rows), encoding="utf-8")
        print("Wrote docs/audit/evidence/baseline.json and inventory.csv. No application files changed.")
    if args.verify:
        with (EVIDENCE / "inventory.csv").open(encoding="utf-8", newline="") as f:
            expected = {r["path"]: r["sha256"] for r in csv.DictReader(f)}
        actual = {r["path"]: r["sha256"] for r in rows}
        changed = sorted(p for p in expected.keys() | actual.keys() if expected.get(p) != actual.get(p))
        if changed:
            print("Source snapshot differs:")
            print("\n".join(changed))
            return 1
        print(f"Snapshot verification: {len(actual)} project file hashes match. This does not mean the application passed tests.")
    print(json.dumps({"statistics": report["statistics"], "xml_parse_errors": len(report["xml"]["parse_errors"]), "xaml_name_mismatches": len(report["xaml_codebehind_name_check"]["mismatches"]), "dotnet_available": report["environment"]["dotnet_available"]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
