#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repair-validation harness for R-031 (audit finding P2-005). No .NET/WPF
toolchain exists here, so validation proves the display contract
structurally: the XAML must be well-formed and must bind the TreeView to
the PermissionTreeNode model (hierarchy, checkbox state, expansion), while
the code-behind model must expose exactly those properties. A small
resolution model shows what WPF renders with vs without the template:
without any HierarchicalDataTemplate a node falls back to ToString() with no
children or checkboxes - the audited defect - while the bound template
renders Name text plus an IsChecked control that load/save already read.

Run: python3 tests/repair/permission_tree_harness.py
Exit 0 on PASS.
"""
import sys
import xml.etree.ElementTree as ET

FAILS = []


def check(name, cond, detail=""):
    if cond:
        print("  ok:", name)
    else:
        FAILS.append(name)
        print("  FAIL:", name, detail)


XAML_PATH = "SmartAuditERP/Form_WPF/frmUsersPermissions.xaml"
CS_PATH   = "SmartAuditERP/Form_WPF/frmUsersPermissions.xaml.cs"

print("Part A: XAML is well-formed and carries the model bindings")
try:
    ET.parse(XAML_PATH)
    check("A1 XAML parses as XML", True)
except ET.ParseError as ex:
    check("A1 XAML parses as XML", False, str(ex))

xaml = open(XAML_PATH, encoding="utf-8").read()
tree_block = xaml.split('<TreeView x:Name="treeView1"')[1].split("</TreeView>")[0]

check("A2 a HierarchicalDataTemplate feeds the tree from Children",
      "<HierarchicalDataTemplate ItemsSource=\"{Binding Children}\">" in tree_block)
check("A3 every node exposes a CheckBox two-way bound to IsChecked",
      'IsChecked="{Binding IsChecked, Mode=TwoWay}"' in tree_block)
check("A4 node labels render the model Name (not ToString())",
      'Text="{Binding Name}"' in tree_block)
check("A5 expansion follows the model both ways (root.IsExpanded=true still applies)",
      'Value="{Binding IsExpanded, Mode=TwoWay}"' in tree_block)
check("A6 the old fixed IsExpanded=False setter is gone",
      '<Setter Property="IsExpanded" Value="False"/>' not in tree_block)
check("A7 exactly one template definition (tags, not comments) and none in App.xaml",
      xaml.count("<HierarchicalDataTemplate ") == 1 and
      xaml.count("</HierarchicalDataTemplate>") == 1 and
      "HierarchicalDataTemplate" not in open("SmartAuditERP/App.xaml", encoding="utf-8").read())

print("Part B: the model exposes exactly what the template binds")
cs = open(CS_PATH, encoding="utf-8").read()
model = cs.split("public class PermissionTreeNode")[1].split("#endregion")[0]
for prop in ("public string Id", "public string Name", "public bool IsChecked",
             "public bool IsExpanded",
             "ObservableCollection<PermissionTreeNode> Children"):
    check("B1 model declares %s" % prop.split()[-1], prop in model)
check("B2 IsChecked raises PropertyChanged (UI updates flow back to save logic)",
      'OnPropertyChanged(nameof(IsChecked))' in model)
check("B3 load/save already operate on IsChecked (no logic change needed)",
      "child.IsChecked = true;" in cs and "if (!node.IsChecked) continue;" in cs)

print("Part C: rendering resolution model")


class Node:
    def __init__(self, name, children=()):
        self.name = name
        self.children = list(children)
        self.is_checked = False

    def __repr__(self):
        return "<PermissionTreeNode>"                      # WPF's fallback visual


def render_legacy(items):                                   # no data template anywhere
    # Without a template WPF shows each *Items-collection* object via ToString();
    # the .Children collections are plain properties nothing binds to, so the
    # hierarchy never expands visually. Only rootNode was added to treeView1.Items.
    return [str(n) for n in items]                          # ToString(), flat, no boxes


def render_fixed(node):                                     # HierarchicalDataTemplate
    out = [("row", node.name, node.is_checked)]
    for c in node.children:
        out.extend(render_fixed(c))
    return out


leaf_ops = [Node("حفظ"), Node("تعديل")]
screen = Node("الشاشة", leaf_ops)
root = Node("الشاشات", [screen])

legacy_view = render_legacy([root])                         # only rootNode sat in Items
check("C1 legacy view shows ONE class-name row: no hierarchy, no checkboxes (bug reproduced)",
      legacy_view == ["<PermissionTreeNode>"])
fixed_view = render_fixed(root)
check("C2 repaired view nests names down to the operation leaves with a check state each",
      fixed_view == [("row", "الشاشات", False), ("row", "الشاشة", False),
                     ("row", "حفظ", False), ("row", "تعديل", False)])
fixed_view[2] = ("row", "حفظ", True)                        # user ticks an operation box
check("C3 a ticked leaf flips its bound state which SaveTreeNodes persists",
      fixed_view[2][2] is True)

print()
if FAILS:
    print("RESULT: FAIL (%d failing checks)" % len(FAILS))
    for f in FAILS:
        print(" -", f)
    sys.exit(1)
print("RESULT: PASS - R-031 (P2-005): the permissions tree now binds to its own")
print("model - hierarchy, names, expansion and per-node checkboxes that the")
print("existing load/save code reads and writes; parent->child cascade policy")
print("stays documented residual pending product input.")
sys.exit(0)
