#!/usr/bin/env python3
"""Read-only source reference vs documentation-checkout identity.

A docs-only descendant commit does not change the audited ERP reference.
The main validator independently checks exact original827 paths AND hashes in
its working tree. This helper is not a Git signature, authorization check,
whole-history provenance verifier or replacement for that inventory comparison.
No writes, network, application import, build, SQL or binary execution.
"""
from __future__ import annotations
import re,subprocess


def identity_errors(reference,checkout,is_ancestor,changed_paths):
    errors=[]
    if not all(isinstance(x,str) and re.fullmatch(r'[0-9a-f]{40}',x) for x in (reference,checkout)):
        errors.append('Invalid full source/checkout commit identity')
    if is_ancestor is not True:errors.append('Audited source reference is not an ancestor of checkout')
    if not isinstance(changed_paths,list) or not all(isinstance(p,str) for p in changed_paths):
        return errors+['Invalid checkout delta path list']
    if len(set(changed_paths))!=len(changed_paths):errors.append('Duplicate checkout delta path')
    for p in changed_paths:
        parts=p.split('/')
        if parts[:2]!=['docs','audit'] or len(parts)<3 or any(x in {'','.', '..'} for x in parts) or '\\' in p or any(ord(c)<32 or ord(c)==127 for c in p):
            errors.append('Non-audit or noncanonical committed delta: '+p)
    if reference==checkout and changed_paths:errors.append('Same commit cannot have a committed tree delta')
    if reference!=checkout and not changed_paths:errors.append('Different checkout requires an explicit docs-only delta, not an unbound source alias')
    return errors


def inspect_identity(reference,git):
    checkout=git('rev-parse','HEAD')
    try:
        git('merge-base','--is-ancestor',reference,checkout);ancestor=True
    except subprocess.CalledProcessError:
        ancestor=False
    paths=[p for p in git('diff','--name-only','-z',reference,checkout).split('\0') if p]
    errors=identity_errors(reference,checkout,ancestor,paths)
    return dict(audited_application_reference=reference,checkout_head=checkout,reference_ancestor_of_checkout=ancestor,committed_net_delta_paths=paths,committed_net_delta_path_count=len(paths),all_committed_net_delta_paths_under_docs_audit=not errors,original827_paths_and_hashes_checked_separately=True,limit='Current committed tree delta only, not all intermediate history or a signature/security/ERP certificate. Working-tree original827 path/hash checks remain mandatory.'),errors
