#!/usr/bin/env python3
"""Exclusively author the R9 bounded source assessment, never run the ERP.

Narrative dispositions below were authored after source display. Derivation
only pins the supplied syntax/ranges; it cannot perform a semantic review or
certify chronology, all routes, a deployed allowed-set or capability exits.
Do not rerun over consumed evidence: use a new version after any correction.
"""
from __future__ import annotations

import json
from pathlib import Path

import verify_save_edit as v

E = 'docs/audit/evidence/'
OUTPUTS = (v.FACTS, v.READS, v.MATRIX, v.ROOTS, v.WORK, v.REVIEW)


def exclusive(name, obj):
    with (v.EV / name).open('x', encoding='utf8', newline='\n') as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def envelope(kind):
    return {'schema_version': 1, 'kind': kind,
        'assessment_reference_date_utc': v.DATE, 'session_reference_date_utc': v.SESSION_DATE,
        'raw_clocks_are_calendar_authority': False, 'application_execution_count': 0,
        'whole_7B_static_assessment_complete': False, 'capability_exit_certificates_issued': 0,
        'four_family_exit_certificates_issued': 0, 'new_accepted_external_handoffs': 0,
        'phase7C_started': False, 'phase8_authorized': False,
        'prior196_tests_recertified': False, 'R2_R3_files_recovered': False}


def author():
    collisions = [n for n in OUTPUTS if (v.EV / n).exists()]
    if collisions: raise FileExistsError('Preserve authored versions; do not overwrite: ' + ', '.join(collisions))
    facts = v.derive()
    def basis(rel, *selectors):
        return [dict(path=rel, selector=s, **{k: v.method(facts, rel, s)[k]
            for k in ('start', 'end', 'syntax_utf8_sha256')}) for s in selectors]
    def text_basis(key):
        r = facts['text_ranges'][key]
        return dict(path=r['path'], text_range_key=key, **{k: r[k]
            for k in ('start', 'end', 'decoded_range_utf8_sha256')})
    def pins(*names): return [v.identity(n if '/' in n else E + n) for n in names]
    common = (v.ENTRY, v.DATE_NOTE, v.FACTS)
    exclusive(v.FACTS, facts)

    reads = envelope('R9-selected-source-display-coverage-not-raw-telemetry-or-human-certification')
    reads.update(extraction_equals_reading=False, independent_human_review_claimed=False,
        individual_read_timestamps_invented=False, raw_stdout_preserved=False,
        assistant_source_read_and_assessment_reported=True,
        all_file_methods_or_all_document_ingress_reviewed=False,
        original_R6_read_flags_rewritten=False,
        range_manifest_limit=v.load(v.DISPLAYS)['limit'], reads=[])
    for i, original in enumerate(v.load(v.DISPLAYS)['ranges'], 1):
        row = dict(original)
        code = v.previous.prior.prior.text_range(v.base.decode((v.ROOT / row['path']).read_bytes()), row['start'], row['end'])
        row.update(id=f'R9READ-{i:03}', decoded_range_utf8_sha256=v.base.sha(code.encode('utf8')),
                   statement='Assistant-reported source display, not a parser-issued read/calendar certificate.')
        reads['reads'].append(row)
    reads['pinned_inputs'] = pins(*common, v.DISPLAYS)
    exclusive(v.READS, reads)

    # Separate route dispositions. These strings describe written branches, not
    # simulated WPF dispatch, SQL effects or a generalized healthy-save result.
    PIPE = {
        v.IO: dict(
            input_mapping='MappingInvoice(ref Invoic) allocates/mutates new numbers/global keys before the writer; BindControls and public import feed the same parent. Entry is explicitly null.',
            validation='Save checks period helper and parsed txtNet > 0 except InvType9. SavePrint instead checks previous return with the same key twice; public PayBill consumes PayInvoice bool. They do not share one validator.',
            permission='Loaded/Common ApplyEditAddPermission and MainClass act on UI controls. F6 invokes the handler directly; SaveAndPrint/SaveInvoice do not consult the button state or a document allowed-set.',
            writer='InvoiceOper.SaveInvoice(invoice, null, Invoic.ISNew) returns a local bool after central employee/store/payment checks, not an authorization token.',
            entry='Explicit null skips EntryOper and the central null branch commits the invoice. Do not call that a failed BindToEntry here: no entry was requested in this parent.',
            stock='Inventory.UpdateItemStock runs before SaveInvoice and has no reversal on saved=false in this body. This is loaded ItemsStock DataTable cache mutation, not a SQL stock commit.',
            transaction='Central header/children share a local SQL transaction; cache, mapping, files and optional remote work do not become atomic with it.',
            publication='Log, print and sync are saved-guarded, then false returns before cost/message/CLR. Sync bool is awaited but not tested; async void returns no save outcome to the entry command.',
            allowed_set_and_origin='Navigate accepts a raw SQL string and BindControls reflect the loaded invoice; no immutable user/document/branch/year allowed-set is passed through MappingInvoice to the writer. Store existence and Branch copied into payload are not ACL evidence.',
            remaining_readable_local='Finish other direct openers/search/navigation predicates, all item writers and year/connection ownership before any external-policy handoff.'),
        v.POS: dict(
            input_mapping='Pay binds cash-customer controls. MappingInvoice mutates parent IDs; new and non-electronic edited invoice dates are overwritten with DateTime.Now in SaveAndPrint.',
            validation='F6 uses btnPay period/employee/customer/items/quantity and status-specific electronic/edit guards. Public PayBill checks a different edit/payment exception; F7 Hold checks items/slot but skips btnPay validation and sets ProcType3.',
            permission='allowEditInvoice is queried once in Window_Loaded. btnPay rejection is limited to nonnew, nonhold, Paid documents; public PayBill has another condition. UI FormPermission/ApplyWpfPermissions classify different button sets.',
            writer='When cloud-first is enabled and not hold, awaited SyncInvoice must return true before local SaveInvoice. Otherwise local bool controls later paths. Cloud wrapper return is not proof of remote and local joint durability.',
            entry='BindToEntry result may be null and is not explicitly rejected here; central writer can commit null-entry invoice. No runtime model-failure claim.',
            stock='Unlike the other editors, a false local save returns before UpdateItemStock; successful cache changes are limited to ProcType1/2.',
            transaction='Independent entry transaction and optional cloud-first precede invoice completion; table/order helpers use separate local calls, catch and do not join the header transaction.',
            publication='updat_table/Insert_Table_Order/Update_Table_Order and RptPrint_Tables call occur before if(!saved)return; Hold publishes HoldList and button state after a void SaveAndPrint call. Empty BackgroundWorker1_DoWork is not a sync execution.',
            allowed_set_and_origin='Public ImportInventoryItems can target the first open POS via frmSelectInv. No per-document branch/year allowed-set accompanies that mutation or command. Loaded role flag/UI enablement is not document authorization.',
            remaining_readable_local='Trace remaining POS open/return/search and table-print dependencies and all line mutations; distinguish hold, unpaid, partially paid and payment-only edits without assuming enum setter contracts.'),
        v.PURCH: dict(
            input_mapping='SetPayAmounts writes cash/ATM/paid from PayType; MappingInvoice mutates new IDs. Return quantity checkbox may zero impacts after a confirmation, not an authorization decision.',
            validation='Ordinary Save uses CheckProiedAcc, reference warning, parsed positive net except type9, confirmation and supplier. SavePrint uses nonempty/nonzero parent net, positive quantities and supplier, but no same period/reference/confirmation branch (P4-031).',
            permission='UI Common/MainClass/FormPermission setters are not reevaluated by command handlers or central SaveInvoice. Keyboard F6 calls btnSave regardless of its enabled state in this body.',
            writer='Calls ordinary InvoiceOper.SaveInvoice with mapped invoice and the original ISNew flag. Uses local bool for log/print/sync/broker/message branches.',
            entry='Counterexample to blanket null acceptance: for ProcType1/2 and InvType1/22, BindToEntry null immediately returns before cache/save. Other types may intentionally pass null.',
            stock='Cache mutation is before local save even in this parent that checks null entry; saved=false does not undo that cache delta.',
            transaction='Header/children parent transaction and EntryOper own transaction remain distinct. A null guard does not make two commits atomic.',
            publication='Print sets Invoic.ISNew=false before awaited SyncInvoice, so the later sync receives that flag; wasNew is separately kept for message/log. Broker is saved-guarded, unlike transfer. No remote wrapper bool is consumed.',
            allowed_set_and_origin='Home configures purchase/return/note/beginning-stock variants with different Name/Tag/type/entry values. The UI lookup names and raw Navigate predicates are not a supplied allowed-document set.',
            remaining_readable_local='Complete remaining purchase note/return/open-search routes, imported-row producers, reference helpers and connection-year owners. Do not externalize these local bodies as unavailable DTO behavior.'),
        v.SALE: dict(
            input_mapping='ValidateInvoice maps payment fields or dispatches PayBill; quotation temporarily changes parent and form ProcType4 and impacts before calling that void validator.',
            validation='Save and SavePrint call the period helper; F6 calls ValidateInvoice directly. Validator checks return linkage, items, quantities, required salesman, confirmation, trial, net and credit client; its body contains no period call.',
            permission='SaveAndPrint edit guard applies to nonnew ProcType1/2 only outside the payment-status/not-updated exception, then electronic/allowEdit flags. This is not a universal save or document ACL.',
            writer='MappingInvoice -> optional BindToEntry -> SaveInvoice. Public PayBill and repayment can reach SaveAndPrint without the ordinary button wrapper. Duplicate written KeyDown registration is P7-162, not a measured double SQL write.',
            entry='For ProcType1/2 BindToEntry is called but null is not rejected here; central null branch remains possible. Purchase is the explicit counterexample.',
            stock='UpdateItemStock executes outside the saved block, after optional saved sync, including saved=false absent an earlier exception/return. Do not claim persistent inventory loss.',
            transaction='EntryOper commits independently. async void callers cannot await or inspect a typed validation/save result; mapping and cache publication are not rolled back by parent SQL.',
            publication='Log/print/sync/message are saved-guarded; successful print path sets ISNew=false before SyncInvoice. Quotation restores ProcType1 and CLR after calling void ValidateInvoice, including a synchronous validation rejection.',
            allowed_set_and_origin='Loaded selects different Common.AllowEdit form keys for return/note/sale; Home Name/Tag and pre/post-lookup order differ. Neither this cached flag nor a query filter is a per-document/year allowed-set.',
            remaining_readable_local='Finish all remaining row/edit/quotation/import/openers, reference health and year/closing owners. Preserve precise early return versus async continuation; no universal ordering claim.'),
        v.CONTRACT: dict(
            input_mapping='SaveAndPrint copies ten contract text values into parent, then MappingInvoicecontract maps those fields and shared collection properties. This local mapping is readable despite missing setter contracts.',
            validation='Save calls period helper; SavePrint skips it and calls ValidateInvoice with item/quantity/salesman/confirmation/trial/net/client checks. The latter still performs meaningful checks; not a no-validation route.',
            permission='Constructor initializes allowEditInvoice=true; selected full-file flag-write census finds no later local write, and ConfigurePermissions only adjusts date/delete UI. Electronic invoice policy is independently loaded and can still block edits.',
            writer='InvoiceOperContract.SaveInvoice writes InvContratct and contract lines. Header SQL bridge shows all four allegedly missing tax parameters ARE added before ExecuteNonQuery; reject that proposed defect.',
            entry='ProcType1/2 requests BindToEntry; null is not rejected here and central writer accepts null. EntryOper transaction remains separate from contract transaction.',
            stock='Cache update is outside saved block after optional sync and can occur on false. It updates ordinary in-memory ItemsStock, not deployed stock tables.',
            transaction='Contract sends/integrates and can update tax status on its own connection before local parent transaction. Encoded invoice SQL uses the parent transaction here, a counterexample to ordinary fresh-connection encoded helper.',
            publication='The saved/IsPrinted/PrintNo branch only sets ISNew=false: no RptPrint call exists in SaveAndPrint. Sync bool is ignored. Message and CLR remain saved-guarded; cache does not.',
            allowed_set_and_origin='Home contract-return uses Name frmcontractReturn and Tag frmcontract; detail-report opener selects inv_type23 but sets editor InvType2 and omits MainClass.ApplyPermissionToForm. Receiver Loaded/guards still exist: no observed unauthorized save asserted.',
            remaining_readable_local='Trace remaining contract import/copy/line helpers, fallback Inv_Sub path, all openers/type coupling, authoritative role keys and year/close owners.'),
        v.TRANS: dict(
            input_mapping='MappingInvoice(ref _invoic) mutates IDs, then branch/destination are rewritten from selected source/destination store. GetInventoryBranch returns1 on no row/error.',
            validation='Save applies period helper then ProcType1 Receive / ProcType2 Send. SavePrint dispatches new ProcType2 to Receive, otherwise tab0 directly calls SaveAndPrint without the ordinary period branch.',
            permission='No command-level role or button IsEnabled result check occurs here. Store selection and calculated branch IDs do not prove membership in a user allowed-document/branch set.',
            writer='SaveSend and SaveReceive each invoke async-void SaveAndPrint twice. Send mutates to incoming/new, recalculates cost and shows success without a returned bool from either call (P4-019).',
            entry='Explicit null is passed to central invoice writer for transfer; no shared EntryOper transaction or paired-transfer transaction/result is introduced.',
            stock='Cache changes before branch rewrite and local SaveInvoice; two parent invocations can each mutate the loaded cache. No SQL stock result is executed or certified.',
            transaction='Each central SaveInvoice has its own local transaction; two void parent invocations and broker publication do not become one atomic send/receive operation.',
            publication='Log/print/sync are saved-guarded but broker/offline section only checks Home._is_active, not saved. Success dialog in Send cannot establish two durable saves.',
            allowed_set_and_origin='RptInventory supplies a global key (counterexample to blanket local-id reopen), yet receiver accepts raw SQL and Branch fallback1 is not ACL evidence. No explicit origin-year token reaches writer.',
            remaining_readable_local='Complete transfer receipt-status variants, remaining direct openers/store ownership, all cost/line effects and publication helper bodies before contract handoffs.'),
    }
    basis_for = {
        v.IO: basis(v.IO, 'SaveAndPrint', 'BindingControls', 'Navigate') + basis(v.IP, 'MappingInvoice', 'SaveInvoice') + basis(v.STOCK, 'UpdateItemStock'),
        v.POS: basis(v.POS, 'SaveAndPrint', 'btnPay_Click', 'PayBill', 'btnHoldOrd_Click', 'CheckEditable', 'BindingDGV') + basis(v.IP, 'SaveInvoice', 'SyncInvoice') + basis(v.STOCK, 'UpdateItemStock'),
        v.PURCH: basis(v.PURCH, 'SaveAndPrint', 'SetPayAmounts', 'Navigate') + basis(v.IP, 'SaveInvoice', 'BindToEntry') + basis(v.STOCK, 'UpdateItemStock'),
        v.SALE: basis(v.SALE, 'SaveAndPrint', 'ValidateInvoice', 'PayBill', 'btnSaveQuotation_Click', 'btnRepaid_Click') + basis(v.IP, 'SaveInvoice', 'MappingInvoice') + basis(v.STOCK, 'UpdateItemStock'),
        v.CONTRACT: basis(v.CONTRACT, 'SaveAndPrint', 'ConfigurePermissions', 'LoadFoundation', 'ValidateInvoice') + basis(v.IPC, 'SaveInvoice', 'MappingInvoicecontract') + basis(v.STOCK, 'UpdateItemStock'),
        v.TRANS: basis(v.TRANS, 'SaveAndPrint', 'SaveSend', 'SaveReceive', 'RecalculateCost') + basis(v.COMMON, 'GetInventoryBranch') + basis(v.IP, 'SaveInvoice') + basis(v.STOCK, 'UpdateItemStock'),
    }
    ROUTE = {
        (v.IO, 'btnSave_Click'): ('Date EditValue DateTime-or-Now -> CheckProiedAcc; set IsPrinted=false; txtNet parse/positive except type9 -> SaveAndPrint.', 'False period/net branches return before mapping; helper always-true is not a valid period enforcement.'),
        (v.IO, 'btnSavePrint_Click'): ('New return calls IsPreviousReturned(InvGlobalID, InvGlobalID); otherwise IsPrinted=true -> SaveAndPrint. No same period/net wrapper.', 'The previous-return guard is present; do not describe this as having no checks at all.'),
        (v.IO, 'PayBill'): ('Public PayInvoice(ref parent, InvObj) true -> SaveAndPrint, bypassing ordinary button period/net wrapper.', 'PayInvoice has its own payment validation/dialog contract; true is not proof of final save.'),
        (v.IO, 'OnKeyDown'): ('F6 directly calls btnSave_Click; F7 is Print, not SavePrint. No local IsEnabled check before direct method call.', 'Other keyboard commands are discovered/read but not all print/delete/add-helper routes certified.'),
        (v.POS, 'btnPay_Click'): ('Bind cash customer controls -> period, EmpNo, credit client, nonempty, conditional Paid-edit and quantity guards -> payment fields/dialog -> SaveAndPrint.', 'Status-specific Paid/nonhold guards are not a blanket denial of all existing documents; central invariants still apply.'),
        (v.POS, 'PayBill'): ('Public payment route applies electronic/status/not-updated edit exception and PayInvoice bool -> SaveAndPrint, not btnPay_Click.', 'Do not infer that every public caller exists or every edit is permitted; this is the supplied public body.'),
        (v.POS, 'btnHoldOrd_Click'): ('Require items and an empty HoldList slot; set holdbool/ProcType3/zero payment -> void SaveAndPrint -> HoldList and UpdateHoldButtons.', 'No available slot means no Save call. A synchronous mapping/writer effect may already occur before the void call returns; async scheduling is not certified.'),
        (v.POS, 'Window_KeyDown'): ('F6 directly invokes btnPay; F7 directly invokes Hold. Neither dispatch checks the control IsEnabled.', 'No WPF routed-event reachability or number of actual invocations measured.'),
        (v.PURCH, 'btnSave_Click'): ('Period -> duplicate reference warning with edit number or0 -> disable button -> net/confirmation/supplier -> SetPayAmounts/IsPrinted=false -> SaveAndPrint -> reenable.', 'Disabling/re-enabling is UI state, not an authorization result or awaiting async-void completion.'),
        (v.PURCH, 'btnSavePrint_Click'): ('Nonempty/nonzero net, positive item quantities and supplier -> IsPrinted=true/SetPayAmounts -> SaveAndPrint; no ordinary reference/period/confirmation branch.', 'Contrasting quantity/nonempty guards are real counterevidence to an oversimplified print-is-unvalidated assertion.'),
        (v.PURCH, 'frmInvInOut_KeyDown'): ('F6 calls btnSave_Click directly without IsEnabled check; F7 calls print-only handler.', 'Keyboard body does not prove GUI dispatch or all indirect input paths.'),
        (v.SALE, 'btnSave_Click'): ('Period helper -> IsPrinted=false -> void ValidateInvoice -> payment/SaveAndPrint as selected by validator.', 'Validator may return on reject/No; button does not receive a save result.'),
        (v.SALE, 'btnSavePrint_Click'): ('Period helper -> IsPrinted=true -> same void ValidateInvoice.', 'Unlike purchase/IO/contract/transfer Print, Sale has a written period call, although the shared helper permits all outcomes.'),
        (v.SALE, 'PayBill'): ('Existing ProcType1/2 not payment-only exception shows alarm; else PayInvoice true -> SaveAndPrint; this body does not use EnableE_Invoice in that first branch.', 'Do not substitute the different SaveAndPrint electronic/allowEdit predicate for this separate public parent.'),
        (v.SALE, 'btnRepaid_Click'): ('Require loaded invoice then void PayBill directly, not the ordinary period/ValidateInvoice route.', 'Repayment is intentionally distinct; no claim that payment arithmetic or posted entry correctness was executed.'),
        (v.SALE, 'btnSaveQuotation_Click'): ('Set quotation ProcType4 and zero impacts -> ValidateInvoice -> restore ProcType1 and CLR without a returned validation/save bool.', 'A synchronous validation rejection still returns to reset/CLR. With awaited child work, precise model aliasing/schedule remains unproved.'),
        (v.SALE, 'Window_KeyDown'): ('F6 directly calls ValidateInvoice, skipping btnSave period/IsPrinted wrapper; constructor plus XAML both write KeyDown subscription.', 'P7-162 is written duplicate wiring, not observed double database commits or a certified routed-event schedule.'),
        (v.CONTRACT, 'btnSave_Click'): ('CheckProiedAcc(date) -> IsPrinted=false -> ValidateInvoice -> SaveAndPrint.', 'Electronic blocking in SaveAndPrint remains possible even though allowEditInvoice locally stays true.'),
        (v.CONTRACT, 'btnSavePrint_Click'): ('Set IsPrinted=true -> ValidateInvoice without the Save button period call.', 'Saved print-flag branch in SaveAndPrint only changes ISNew; an actual RptPrint is absent there, not proof the report engine failed.'),
        (v.CONTRACT, 'frmcontract_KeyDown'): ('F6 invokes btnSave_Click; F7 print-only, F8 preview, Escape Close. No local IsEnabled guard.', 'SetupButtonEvents attaches save clicks in code, unlike assuming XAML+code duplicate click wiring.'),
        (v.TRANS, 'btnSave_Click'): ('Period helper -> ProcType1 SaveReceive, ProcType2 SaveSend.', 'Both deeper routines call void SaveAndPrint twice; the entry handler gets no combined save outcome.'),
        (v.TRANS, 'btnSavePrint_Click'): ('New ProcType2 -> SaveReceive, else tab0 direct SaveAndPrint; no SaveSend or period call in this body.', 'The method name is not evidence of send intent; exact written branch is retained pending workflow contract.'),
        (v.TRANS, 'Window_KeyDown'): ('F6 directly invokes ordinary save; F7 print-only. Other key branches are read, not all target helpers certified.', 'Keyboard contains catch/reporting, not a role decision or a composite transfer success result.'),
    }
    decision_for = {v.IO: 'R9D-IO', v.POS: 'R9D-POS', v.PURCH: 'R9D-PURCHASE', v.SALE: 'R9D-SALE', v.CONTRACT: 'R9D-CONTRACT', v.TRANS: 'R9D-TRANSFER'}
    matrix = envelope('R9-per-command-six-editor-pipelines-and-selected-alternate-openers-not-all-routes')
    matrix.update(literal_command_sites=facts['literal_command_sites'], selected_alternate_editor_creations=facts['selected_alternate_editor_creations'],
                  literal_sites_are_discovery_not_compiler_bindings=True, all_alias_reflection_or_document_ingress_complete=False,
                  command_reviews=[], editor_pipelines={}, alternate_opener_reviews=[])
    for rel, names in v.COMMAND_OWNERS.items():
        pipe = PIPE[rel]
        for sel in names:
            f = v.method(facts, rel, sel); trace, limit = ROUTE[rel, sel]
            matrix['command_reviews'].append(dict(path=rel, entry_selector=sel,
                whole_entry_context={k: f[k] for k in ('start', 'end', 'syntax_utf8_sha256')},
                whole_body_displayed_and_assessed_in_R9=True, compiler_or_runtime_reachability_certified=False,
                whole_route_or_capability_certified=False, accepted_external_handoff=False,
                input_to_validation=trace, permission_and_allowed_set=pipe['permission'] + ' ' + pipe['allowed_set_and_origin'],
                writer_entry_stock_transaction=' '.join(pipe[k] for k in ('writer', 'entry', 'stock', 'transaction')),
                publication_and_outcomes=pipe['publication'], counterevidence_and_limit=limit,
                remaining_local=pipe['remaining_readable_local'], decision_ids=[decision_for[rel], 'R9D-PERMISSION', 'R9D-WRITER-SCOPE'],
                source_basis=basis(rel, sel) + basis_for[rel]))
        matrix['editor_pipelines'][rel] = dict(pipe, all_readable_local_obligations_complete=False, is_capability_exit=False,
            source_basis=basis_for[rel] + basis(v.EO, 'SaveEnty') + basis(v.COMMON, 'CheckProiedAcc', 'AllowEdit'))
    for rel, sels in v.OPENER_OWNERS.items():
        for sel in sels:
            f = v.method(facts, rel, sel)
            creates = [r for r in f['creations'] if r['type'] in v.EDITOR_TYPES]
            config = [a for a in f['assignments'] if a['left'].split('.')[-1] in ('InvType', 'ProcType', 'EntryType', 'Tag', 'Name', 'Title')]
            request = 'Selected creation syntax and explicit configuration below are retained individually; not inferred from menu names.'
            policy = 'MainClass.ApplyPermissionToForm targets a UI object; order/Name/Tag choices differ. Neither it nor DoApplyUserSett returns an allowed-document set.'
            origin = 'New-editor opener has no selected persisted document origin/branch/year token. Current session and receiver defaults/loaders still apply; no all-routes access decision claimed.'
            remaining = 'Read upstream menu enabled/permission ownership and downstream variant-specific reset/search/item/connection consumers; do not claim this selected opener closes all ingress.'
            if rel == v.HOME and sel == 'btnPOS2_Click':
                policy = 'Counterexample: POS branch is guarded by stripPOS.IsEnabled; marine branch has its own visibility/trial/enabled conjunction. Other selected Home handlers do not all repeat such checks.'
            elif rel == v.SELECT:
                request = 'invType1/2/9/4/5/3 create configured editors and ImportInventoryItems before Show. Existing POS path selects FirstOrDefault<T>, imports into that instance and closes the selector without constructing/reapplying policy to a new POS.'
                origin = 'Input is List<InvoiceItem>; four local imports SearchByID then overwrite first ItemId match, not a returned inserted-row identity. Existing POS state/branch/year is not carried by itemList as an explicit allowed-set.'
                remaining = 'Finish SearchByID and ItemOper insertion/duplicate outcomes and source itemList producers before asserting merge/replacement safety; no setter deep-copy assumption.'
            elif rel == v.RPTINV:
                request = 'Selected report opener configures editor, calls Show then raw Navigate with inv_type/proc_type and InvGlobalID. Global key is present: do not generalize local-id loss from P7-061 to this route.'
                origin = 'No explicit original connection/year/allowed-document token accompanies globalId. No branch predicate in these bounded query strings, but global-key use is real counterevidence; no collision or unauthorized read observed.'
                remaining = 'Finish report-row key/procType producers and all receiver reset/binder/connection consumers. Show-before-Navigate is written order, not Loaded scheduling proof.'
            elif rel == v.CONTACT:
                request = 'Tagged InvoiceTxt row -> globalId/procType/type. Branch invType23 constructs frmcontract but sets editor InvType2, then Show and Navigate selects InvContratct inv_type23 by globalId.'
                policy = 'No MainClass.ApplyPermissionToForm call in this opener. Receiver constructor/Loaded/FormPermission/central guards are present; do not conclude all authorization absent.'
                origin = 'Global key is retained but UI InvType2 differs from selected row type23. Trace receiver uses of form InvType versus hydrated invoice type before alleging an actual wrong save; branch/year/allowed-set remains unproven.'
                remaining = 'Complete InvoiceTxt row producer and all form-type consumers, permission key and connection/year paths. Keep unnumbered type coupling separate from P7-061 local-id-loss and potential P7-132 lifecycle.'
            matrix['alternate_opener_reviews'].append(dict(path=rel, entry_selector=sel, configured_request=request,
                explicit_source_configurations=config, selected_creations=creates, policy_lookup_and_order=policy,
                document_branch_year_and_allowed_set=origin, remaining_local=remaining,
                source_basis=basis(rel, sel) + (basis(v.SELECT, 'FindOpenedWindow', 'ShowWindowAndCloseCurrent') if rel == v.SELECT else []),
                all_ingress_or_runtime_schedule_certified=False, accepted_external_handoff=False))
    matrix['pinned_inputs'] = pins(*common, v.READS, v.previous.WORK)
    exclusive(v.MATRIX, matrix)

    original_rows = v.base.rows('findings.csv', v.AUDIT) + v.base.rows('findings-additions-07B39R1.csv')
    by_id = {r['id']: r for r in original_rows}
    ROOT_REASON = {
        'P1-012': 'Same fail-open permission root: Common.AllowEdit returns true on absent row/catch; constructor FormPermission starts allowed. Role/UI/source scope only; deployed grants not attested.',
        'P1-013': 'UI permission-context comparison, not proof these Save commands implement the same original root. Need exact Name/Tag/form row semantics; do not merge a document ACL question by title.',
        'P2-006': 'Grant/SQL trust context is adjacent. Local absence of a document-set check is not an independently proven deployed SQL authorization defect or remediation closure.',
        'P3-001': 'Same period root: CheckProiedAcc includes || true and permits empty/error paths. The selected entry commands show both calls and bypasses; no executed out-of-period posting.',
        'P3-002': 'SaveEnty contains local account iteration/commit without empty/balance/period guard. Arithmetic/DTO/provider invariants remain qualified; no simulated posting acceptance.',
        'P3-003': 'Direct same-root support: both central invoice writers invoke EntryOper.SaveEnty on its own connection/transaction before their own commit; no shared transaction parameter.',
        'P3-025': 'Invoice-entry mapping/rounding context is adjacent, not automatic equivalence for null BindToEntry or header/cache publication. No claim all formulas or accounts reviewed.',
        'P4-014': 'Retain original potential certainty. Local SaveEnty independent commit and no balance guard do not authenticate historical potential mechanisms as observed failures.',
        'P4-019': 'Same transfer outcome root: two async-void SaveAndPrint calls with parent mutation/cost/success publication and no aggregate returned save result. No observed inventory imbalance claimed.',
        'P4-020': 'Production-specific missing-parameter root is not a contract-header finding. Contract header visibly supplies QRCode/InvoiceHash/UUID/ZatcaSent; reject the suggested missing-four claim.',
        'P4-031': 'Same purchase Save/SavePrint validation parity root with exact counterchecks recorded; SavePrint has quantity/items checks that ordinary Save lacks locally.',
        'P5-030': 'General sync-health UI root is adjacent. New local wrapper result/target and transfer broker questions need exact caller-to-provider comparison before root merge or novelty.',
        'P6-001': 'General tax integration context is not sufficient for a novel contract transaction/status root. Static source order and independent connection are recorded, not remote acceptance.',
        'P6-007': 'Direct ordinary SaveInvoice support: tax send precedes parent transaction and non-tax path follows commit/reuses transaction. Contract encoded writes differ and cannot be generalized.',
        'P7-031': 'Print outcome root is adjacent, but contract SaveAndPrint has no RptPrint call, a different immediate mechanic. No SDK/printer failure observed and no forced merge.',
        'P7-061': 'Selected RptInventory/contract detail use global keys, counterexamples to blanket local-id reopening. Separate missing origin-year/allowed-set and UI type2/row23 questions remain open.',
        'P7-132': 'Retain potential certainty; Show/Loaded/reset written order is not an executed WPF schedule. Selected Home/report opener readings do not upgrade chronology or runtime loss.',
        'P7-144': 'Original contract import chooses last matching row; these four modern imports overwrite FirstOrDefault ItemId after void SearchByID. Same concern is plausible, not the same proven root by assumption.',
        'P7-135': 'Direct same-root support: POS SaveAndPrint overwrites new invoice date and non-electronic edit date with Now before writer. No date-dependent financial run.',
        'P7-159': 'Void new/clear cancellation context is adjacent, not automatic same root for quotation CLR after void ValidateInvoice or HoldList publication.',
        'P7-160': 'Prior linked-child cancellation root remains unchanged; this slice reads parent save aftermath and four direct imports, not reclassification of accepted child outcome.',
        'P7-161': 'Partial/null parent hydration is prior context. BindToEntry null path and central null-entry commit require independent mapping policy comparison; purchase explicit null return prevents blanket claim.',
        'P7-162': 'Direct same-root support: Sale constructor and root XAML both register Window_KeyDown; direct F6 ValidateInvoice also bypasses period wrapper. No runtime invocation multiplicity certified.',
    }
    roots = envelope('R9-focused-source-root-comparisons-with-all-available-prior-dictionaries-preserved')
    roots.update(available_prior_rows=original_rows, focused_root_reviews={rid: dict(canonical_prior_row=by_id[rid], reason=ROOT_REASON[rid],
        prior_severity_certainty_status_not_rewritten=True, fresh_whole_root_source_audit_claimed=False) for rid in v.FOCUSED},
        all339_semantically_reread_in_R9=False, all345_roots_screened=False, missing_six_dictionaries_reconstructed=False,
        historical_root_fields_rewritten=False, new_finding_ids=[], candidate_dispositions=[])
    candidate_data = {
        'R9C-PERIOD': ('same-root-additional-bounded-evidence', 'Selected command paths call an always-permitting period helper or bypass it; P3-001 not a new numbered defect.', basis(v.COMMON, 'CheckProiedAcc')),
        'R9C-FAILOPEN': ('same-root-additional-bounded-evidence', 'Missing/error Common.AllowEdit allows true and FormPermission defaults allowed; P1-012. Do not treat UI disabled state as a document ACL.', basis(v.COMMON, 'AllowEdit') + basis(v.FP, 'ctor:FormPermission', 'ApplyFrmPermissionInternal')),
        'R9C-COMMAND-AUTH': ('unnumbered-source-question-not-novelty-certified', 'Direct keyboard/public command bodies do not recheck disabled UI buttons or a resource allowed-set; compare role/Name/Tag/document policy and downstream guards individually.', basis(v.SALE, 'Window_KeyDown', 'SaveAndPrint') + basis(v.MC, 'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions')),
        'R9C-PURCHASE-PARITY': ('same-root-additional-bounded-evidence', PIPE[v.PURCH]['validation'], basis(v.PURCH, 'btnSave_Click', 'btnSavePrint_Click')),
        'R9C-POS-DATE': ('same-root-additional-bounded-evidence', PIPE[v.POS]['input_mapping'], basis(v.POS, 'SaveAndPrint')),
        'R9C-SALE-DOUBLE-WIRING': ('same-root-additional-bounded-evidence', 'P7-162 written duplicate subscription remains distinct from runtime double commit; root XAML is pinned in facts/read log.', basis(v.SALE, 'ctor:frmInvSale', 'Window_KeyDown')),
        'R9C-TRANSFER-OUTCOME': ('same-root-additional-bounded-evidence', PIPE[v.TRANS]['writer'] + ' ' + PIPE[v.TRANS]['publication'], basis(v.TRANS, 'SaveSend', 'SaveReceive', 'SaveAndPrint')),
        'R9C-ENTRY-TRANSACTIONS': ('same-root-additional-bounded-evidence', 'EntryOper uses MainClass.ConnObj and its own BeginTransaction/Commit; invoice/contract each commit afterward. P3-003.', basis(v.EO, 'SaveEnty') + basis(v.IP, 'SaveInvoice') + basis(v.IPC, 'SaveInvoice')),
        'R9C-ENTRY-INVARIANTS': ('same-root-qualified-additional-evidence', 'No local SaveEnty empty/balance/period guard in the complete body; no balance/arithmetic/provider contract executed. P3-002 qualified.', basis(v.EO, 'SaveEnty')),
        'R9C-TAX-COMMIT': ('same-root-additional-bounded-evidence', 'Ordinary writer send/commit ordering supports P6-007. Contract integrates/status-writes before parent, but encoded SQL is inside parent: retain the counterexample.', basis(v.IP, 'SaveInvoice', 'InsertZatcaEncodedInvoice') + basis(v.IPC, 'SaveInvoice')),
        'R9C-STOCK-CACHE': ('unnumbered-source-question-not-novelty-certified', 'IO/Purchase/Transfer mutate cache before save; Sale/Contract outside saved block; POS only after false return and ProcType1/2. Helper is DataTable cache, not SQL persistent stock.', basis(v.STOCK, 'UpdateItemStock') + [b for rel in v.EDITORS for b in basis(rel, 'SaveAndPrint')]),
        'R9C-MAPPING-RETRY': ('unnumbered-source-question-with-counterexample', 'Mapping changes parent IDs/rows before durable save and can survive false. VerifyIsNewInvoice assigns result=false only; do not assert proven clone trigger/deep alias behavior.', basis(v.IP, 'MappingInvoice', 'VerifyIsNewInvoice') + basis(v.IPC, 'MappingInvoicecontract')),
        'R9C-POS-TABLES': ('unnumbered-source-question-not-novelty-certified', 'Separate table/order writes and RptPrint_Tables call precede local false return; HoldList publishes after void save. Exact helper catches are read, remote/print outcomes not executed.', basis(v.POS, 'SaveAndPrint', 'btnHoldOrd_Click', 'updat_table', 'Insert_Table_Order', 'Update_Table_Order', 'RptPrint_Tables')),
        'R9C-QUOTATION-CLEAR': ('unnumbered-source-question-not-merged-with-linked-cancel', PIPE[v.SALE]['publication'], basis(v.SALE, 'btnSaveQuotation_Click', 'ValidateInvoice', 'SaveAndPrint')),
        'R9C-CONTRACT-PRINT': ('unnumbered-source-question-not-merged-with-print-engine', 'Saved print branch only sets ISNew=false; absence of RptPrint here is not swallowed Print.Printing outcome P7-031 or a provider failure.', basis(v.CONTRACT, 'btnSavePrint_Click', 'SaveAndPrint')),
        'R9C-NULL-ENTRY': ('unnumbered-source-question-with-purchase-counterexample', 'BindToEntry catches can return null; Sale/POS/Contract do not reject while Purchase does for ProcType1/2,type1/22. Central Entr==null commits; intentional no-entry types must stay distinct.', basis(v.IP, 'BindToEntry', 'SaveInvoice') + basis(v.IPC, 'BindToEntry', 'SaveInvoice') + basis(v.PURCH, 'SaveAndPrint')),
        'R9C-CONTRACT-FALLBACK': ('unnumbered-source-question-not-novelty-certified', 'Contract writer normal InvoiceItems go to InsertInvSubcontract, but when InvoiceItems.Count==0 it writes inv.Items via ordinary InsertInvSub. Need actual type/Items producer and policy, not a forced P4-020 merge.', basis(v.IPC, 'SaveInvoice', 'MappingInvoicecontract') + [text_basis('ordinary-header-and-line-SQL'), text_basis('contract-header-and-line-SQL')]),
        'R9C-CLOUD-LOCAL-RESULT': ('unnumbered-source-question-not-end-to-end-health', 'Both SyncInvoice wrappers return true in successful BranchType4 path, but noncloud branch posts/marks/syncs entry then returns default false; contract noncloud marks Inv vs cloud InvContratct. POS cloud-first consumes result; other parents ignore it. No remote contract certified.', basis(v.IP, 'SyncInvoice') + basis(v.IPC, 'SyncInvoice') + basis(v.POS, 'SaveAndPrint') + basis(v.TRANS, 'SaveAndPrint')),
        'R9C-CONTRACT-PARAMETERS': ('rejected-alleged-missing-four-tax-parameters', 'Counterevidence: contract SaveInvoice header adds @QRCode/@InvoiceHash/@UUID/@ZatcaSent before ExecuteNonQuery. All62 raw header names are retained; trimmed placeholder comparison has no missing names. This refutes the suggested omission, not all provider/name-whitespace/type correctness.', basis(v.IPC, 'SaveInvoice') + [text_basis('contract-header-and-line-SQL')]),
        'R9C-ALTERNATE-CONTRACT': ('unnumbered-source-question-not-novelty-certified', 'Contract detail row type23/global key -> editor InvType2 -> query InvContratct inv_type23. UI form-type coupling and missing explicit opener permission call need all downstream type consumers; not local-id-loss or observed bypass.', basis(v.CONTACT, 'BtnShowInv_Click') + basis(v.CONTRACT, 'Navigate', 'frmcontract_Load', 'SaveAndPrint')),
        'R9C-IMPORT-FIRST-MATCH': ('unnumbered-source-question-not-automatic-P7-144-root', 'Four public ImportInventoryItems call void SearchByID then overwrite FirstOrDefault ItemId price/quantity. A preexisting row can be selected structurally, but insertion/merge/cancel/serial/unit policy needs readable SearchByID/ItemOper followthrough. Existing POS opener increases scope, not proof of bad financial output.', [b for rel in (v.IO, v.POS, v.PURCH, v.SALE) for b in basis(rel, 'ImportInventoryItems')] + basis(v.SELECT, 'GenerateInvoice')),
        'R9C-UI-POLICY-IDENTITY': ('unnumbered-source-question-with-opener-counterexamples', 'Home sets varying Name/Tag/InvType/ProcType and sometimes invokes UI permission before configuration; return-contract Name differs from Tag. btnPOS2 explicitly checks IsEnabled, unlike a blanket all-opener-bypass assertion. Need authoritative row and receiver lookup comparison.', basis(v.HOME, 'stripSaleRetu_Click', 'stripPurchInv_Click', 'stripinvcontractreturn_Click', 'btnPOS2_Click') + basis(v.MC, 'ApplyPermissionToForm@System.Windows.Window')),
    }
    for cid, root_id in v.CANDIDATES.items():
        status, disposition, src = candidate_data[cid]
        roots['candidate_dispositions'].append(dict(id=cid, root_id=root_id, disposition=status,
            source_disposition=disposition, source_basis=src, novelty_certified=False, accepted_external_handoff=False,
            observed_financial_or_provider_failure=False,
            prior_certainty_preserved=by_id[root_id]['certainty'] if root_id else None,
            remaining_local='Continue the named local worklist and exact caller/variant/root comparison; rejected missing-four allegation stays rejected. Missing six historical dictionaries and runtime contracts are not reconstructed.'))
    roots['pinned_inputs'] = pins(*common, v.MATRIX, 'docs/audit/findings.csv', 'findings-additions-07B39R1.csv', v.previous.ROOTS)
    exclusive(v.ROOTS, roots)

    work = envelope('R9-readable-local-successor-worklist-do-not-delegate-local-source-to-missing-contracts')
    work.update(original37_R6_rows_verbatim=v.load(v.previous.OLD_WORK)['calls'], original_R6_read_flags_rewritten=False,
        preserved_R8_local_task_rows_verbatim=v.load(v.previous.WORK)['remaining_readable_local_tasks'],
        entire_R8LOCAL_SAVE_EDIT_marked_complete=False, all_alias_reflection_or_document_ingress_complete=False,
        completed_bounded_R9_work='Whole selected Save/Pay/Print/keyboard/mapping/central writers, permission helpers, 26 selected opener owners and four ImportInventoryItems bodies assessed individually. This is not closure of six editors or26 capabilities.',
        remaining_readable_local_tasks=[])
    tasks = [
        ('R9LOCAL-REMAINING-OPENERS', [v.P+'frmInvDetails.xaml.cs', v.P+'frmTaxInvDetails.xaml.cs', v.P+'frmRptInvSalesDetails.xaml.cs', v.P+'frmRptInvSalesDetailsPos.xaml.cs', v.P+'frmRptInvSalesDetailsPosAndroid.xaml.cs', v.P+'frmRptInvPurchaseDetails.xaml.cs', v.P+'frmRptInvNotfic.xaml.cs', v.P+'frmInvSumByClient.xaml.cs', v.P+'frmCashCustomer.xaml.cs', v.EO], 'Read remaining literal alternate editor opener containing bodies and row/global/local-key producers; keep aliases/reflection/target-typed creation census separate from these selected factories. Compare each request to receiver command/allowed document, branch and year scope.'),
        ('R9LOCAL-IMPORT-INSERT-OUTCOMES', [v.IO, v.POS, v.PURCH, v.SALE, v.C+'ItemOper.cs', v.C+'ItemOpercontract.cs', v.SELECT], 'Continue four ImportInventoryItems through whole SearchByID/ItemOper duplicate/add/cancel/unit/serial outcomes and itemList producers. Do not reread first-match bodies as still unreviewed, or assert deep alias/default semantics from property assignment.'),
        ('R9LOCAL-ALLOWED-SETS', [v.FP, v.MC, v.COMMON, v.P+'frmInvoiceSrch.xaml.cs', v.CONTRACT, v.CONTACT], 'Complete concrete Name/Tag lookup rows and each reader/search/navigation SQL source and consumers. Trace immutable document/branch/year allowed-set, command guards and original connection owner. UI disablement, employee/store presence, payload Branch and query parameter are not ACL evidence.'),
        ('R9LOCAL-TRANSFER-PUBLICATION', [v.TRANS, v.POS, v.C+'SendData.cs', v.C+'ConnectBroker.cs', v.IP, v.IPC], 'Finish branch/status-dependent transfer call variants, offline queue/broker readers, POS table print/reset and selected sync helper dependencies. Preserve false/success/order asymmetry; do not replace local bodies with a remote handoff or simulate an ERP transaction.'),
        ('R9LOCAL-CONTRACT-TYPE-FALLBACK', [v.CONTACT, v.CONTRACT, v.IPC], 'Read remaining form InvType versus hydrated InvoiceType consumers and fallback Items lineage/ordinary Inv_Sub target, compare against contract import and lookup roots. The alleged four missing header tax parameters are refuted, not an unresolved defect.'),
        ('R9LOCAL-YEAR-CLOSE', [v.SALE, v.CONTRACT, v.P+'frmInvoiceSrch.xaml.cs', v.P+'frmInvoiceItems.xaml.cs', 'docs/audit/evidence/session-year-local-worklist-07B39R6.json'], 'Finish nested shared-backup/previous-year and cached connection consumers, normal/chrome/Escape/failed closure and quotation/hold publication. Neither async void written order nor Show/Loaded source proves a runtime schedule.'),
        ('R9LOCAL-REMAINING26-AND-ROOTS', ['docs/audit/evidence/capability-register-07B38.csv', 'docs/audit/evidence/capability-reconciliation-07B39R8.json', E+v.ROOTS, E+v.previous.WORK], 'Continue every original capability/family local obligation, including R7 D05/D06 Recipient/reader and independent transaction questions; compare unnumbered R9 cache/print/type/publication candidates to available roots without certifying all339 or reconstructing missing345/196/49 history.'),
    ]
    for tid, src, action in tasks:
        work['remaining_readable_local_tasks'].append(dict(id=tid, source_paths_or_prior_evidence=src, next_action=action,
            owner_role='Static source audit agent within approved26 capability scope', externalized=False, accepted_external_handoff=False))
    work['pinned_inputs'] = pins(*common, v.MATRIX, v.ROOTS, v.previous.WORK, v.previous.OLD_WORK)
    exclusive(v.WORK, work)

    decisions_data = [
        ('R9D-PERIOD', 'The period validator always writes allowing returns, including empty/error; selected callers also differ in whether they invoke it. P3-001 remains open, not a new result.', 'Do not infer actual accounting-period acceptance from dead rejection UI, or call a Print route fully unvalidated when its own checks exist.', basis(v.COMMON, 'CheckProiedAcc') + [b for rel in (v.IO, v.PURCH, v.SALE, v.CONTRACT, v.TRANS) for b in basis(rel, 'btnSave_Click', 'btnSavePrint_Click')]),
        ('R9D-PERMISSION', 'Common.AllowEdit fail-open, default-allowed FormPermission and different button classifiers are distinct from a resource-aware command decision. Read all16 local allowEdit/electronic flag writes and their whole containing bodies; contract allowEdit only initializes true.', 'Electronic policy can independently block Contract; POS/Sale have status/ProcType exceptions; one Home POS opener tests IsEnabled. No blanket all-permissions-absent or deployed unauthorized-save assertion.', basis(v.COMMON, 'AllowEdit', 'ApplyEditAddPermissionInternal') + basis(v.FP, 'ctor:FormPermission', 'ApplyFrmPermissionInternal', 'IsSavePermissionButton') + basis(v.MC, 'ApplyPermissionToForm@System.Windows.Window', 'ApplyWpfPermissions') + basis(v.CONTRACT, 'ConfigurePermissions', 'LoadFoundation') + basis(v.HOME, 'btnPOS2_Click')),
        ('R9D-IO', ' '.join(PIPE[v.IO][k] for k in ('validation', 'entry', 'stock', 'publication')), 'Public PayInvoice true is a payment-dialog result, not SaveInvoice success; no all-route safety or SQL stock-loss claim.', basis_for[v.IO] + basis(v.IO, 'btnSave_Click', 'btnSavePrint_Click', 'PayBill', 'OnKeyDown')),
        ('R9D-PURCHASE', ' '.join(PIPE[v.PURCH][k] for k in ('validation', 'entry', 'stock', 'publication')), 'Purchase rejects null entry for selected financial variants, contrasting other editors. Print quantity guards are real. Neither makes separate transactions atomic.', basis_for[v.PURCH] + basis(v.PURCH, 'btnSave_Click', 'btnSavePrint_Click')),
        ('R9D-POS', ' '.join(PIPE[v.POS][k] for k in ('validation', 'stock', 'transaction', 'publication')), 'Status/ProcType guards and stock-after-false-return are counterexamples. Hold slot full produces no save. No exact async schedule or remote durability claim.', basis_for[v.POS] + basis(v.POS, 'btnHoldOrd_Click', 'Window_KeyDown', 'BackgroundWorker1_DoWork', 'updat_table', 'Insert_Table_Order', 'Update_Table_Order', 'RptPrint_Tables')),
        ('R9D-SALE', ' '.join(PIPE[v.SALE][k] for k in ('validation', 'permission', 'publication')), 'P7-162 remains written event duplication; quotation void rejection/reset is a separate unnumbered question. No executed duplicate posting or CLR alias claim.', basis_for[v.SALE] + basis(v.SALE, 'Window_KeyDown', 'ctor:frmInvSale', 'btnSave_Click', 'btnSavePrint_Click')),
        ('R9D-CONTRACT', ' '.join(PIPE[v.CONTRACT][k] for k in ('validation', 'permission', 'writer', 'publication')), 'Four tax header parameters are present, refuting suggested omission. Guarded electronic edits still reject; print-call absence is not swallowed printer outcome.', basis_for[v.CONTRACT] + basis(v.CONTRACT, 'btnSave_Click', 'btnSavePrint_Click')),
        ('R9D-TRANSFER', ' '.join(PIPE[v.TRANS][k] for k in ('validation', 'writer', 'stock', 'publication')), 'Source-store branch calculation/fallback1 is not document authorization; two void calls may perform synchronous work before returning. No invented timing or persistent stock result.', basis_for[v.TRANS] + basis(v.TRANS, 'btnSave_Click', 'btnSavePrint_Click')),
        ('R9D-MAPPING', 'Both mapping bodies mutate parent IDs/numbers, copy header/collection properties, build Items projection and invoke local composite writer; VerifyIsNewInvoice has no true assignment in the read body. These are local facts, not a missing-model substitute.', 'Property setter copy/reference behavior and model enum semantics are not established by assignment syntax. No universal cloning, financial-formula or deep-alias certification.', basis(v.IP, 'MappingInvoice', 'BindingCompositeItems', 'VerifyIsNewInvoice', 'GetInvoiceGlobalID') + basis(v.IPC, 'MappingInvoicecontract', 'BindingCompositeItems', 'GetInvoiceGlobalIDcontract')),
        ('R9D-ENTRY', 'Both BindToEntry bodies catch to null; central writers permit Entr==null and otherwise call EntryOper.SaveEnty with a new connection/transaction before parent commit. Full SaveEnty has no local empty/balance/period check. P3-003/P3-002 qualified.', 'Purchase explicitly returns on null for its financial variants; IO/Transfer intentionally pass null. Do not conflate all nulls or certify model/accounting invariants from syntax.', basis(v.IP, 'BindToEntry', 'SaveInvoice') + basis(v.IPC, 'BindToEntry', 'SaveInvoice') + basis(v.EO, 'SaveEnty') + basis(v.PURCH, 'SaveAndPrint')),
        ('R9D-STOCK', 'Read helper mutates loaded ItemsStock rows by ItemId first match, then store check and PrimaryQnty delta; catches write debug. IO/Purchase/Transfer pre-save, Sale/Contract outside saved, POS saved success ProcType1/2 only.', 'This is in-memory DataTable cache consistency, not a SQL persistent-stock update or observed business loss. No prior-edit reverse delta is in this body, but not all event/reload owners are closed.', basis(v.STOCK, 'UpdateItemStock') + [b for rel in v.EDITORS for b in basis(rel, 'SaveAndPrint')]),
        ('R9D-PUBLICATION', 'Print/sync/broker/table/cache/messages have different saved guards. Attachment helpers use File.Copy and separate connections; ordinary encoded helper owns a connection while contract encoded SQL is inside parent. Sync noncloud posts/marks then returns default false; contract noncloud marks ordinary Inv.', 'P6-007 same-root ordinary ordering; remaining broker/remote/provider/helper contracts are not run or all reviewed. No end-to-end health from bool, log, green UI or thread scheduling.', basis(v.IP, 'SaveInvoice', 'SyncInvoice', 'insertDocument', 'InsertZatcaEncodedInvoice') + basis(v.IPC, 'SaveInvoice', 'SyncInvoice', 'insertDocument') + basis(v.TRANS, 'SaveAndPrint') + basis(v.POS, 'SaveAndPrint')),
        ('R9D-WRITER-SCOPE', 'Whole central writers check employee/store/treasury/payment/customer/trial and key header updates by InvGlobalID; they receive no period/form permission/original connection/allowed-set parameter. Payload Branch set/update is not branch ownership authorization. Contract normal and empty-line fallback targets differ.', 'No claim deployed constraints or grants are absent, global keys collide, or any user accessed a forbidden invoice. RptInventory global-key reopen is a counterexample to blanket local-id claim. Header parameters are present, not missing-four.', basis(v.IP, 'SaveInvoice') + basis(v.IPC, 'SaveInvoice') + [text_basis('ordinary-header-and-line-SQL'), text_basis('contract-header-and-line-SQL')] + basis(v.RPTINV, 'OpenInventoryTransfer')),
        ('R9D-ALTERNATE-OPENERS', 'Individually assessed21 Home factories, GenerateInvoice, three RptInventory helpers and contract detail opener. Name/Tag/lookup timing and type/proc/entry configurations differ; global-key reopens differ from old local-id routes. Contract detail sets UI InvType2 while query row type23.', '26 selected opener OWNERS and31 creation expressions are not26 capability assessments, not all repository factories, and not WPF Loaded schedule proof. Receiver guards remain; type/policy questions stay unnumbered.', [b for rel, sels in v.OPENER_OWNERS.items() for b in basis(rel, *sels)]),
        ('R9D-IMPORTS', 'Four whole public imports call void SearchByID, then overwrite first matching ItemId price/quantity and recalculate/bind. GenerateInvoice can import into first open POS without a new window. No explicit inserted/merged/cancelled result is consumed.', 'P7-144 is contract/last-match and not automatically the same root. SearchByID/ItemOper and itemList producers remain readable-local obligations; no null/deep-copy/unit/financial-outcome assumptions.', [b for rel in (v.IO, v.POS, v.PURCH, v.SALE) for b in basis(rel, 'ImportInventoryItems')] + basis(v.SELECT, 'GenerateInvoice', 'FindOpenedWindow', 'ShowWindowAndCloseCurrent')),
    ]
    review = envelope('R9-authored-substantive-Save-edit-source-dispositions-not-capability-completion')
    review['source_decisions'] = [dict(id=did, source_disposition=disposition, counterevidence_and_limit=limit, source_basis=src,
        observed_in_ERP=False, is_capability_exit=False, root_remediated=False) for did, disposition, limit, src in decisions_data]
    canonical = {r['id']: r for r in v.base.rows('capability-register-07B38.csv')}
    cap_remainders = {
        'CAP7B38-D08': 'Cache-vs-persistent stock and transfer Save outcome traced, but remaining ItemOper stock/cost/reload owners, branch-status variants and every inventory/report/expiry obligation remain local and open.',
        'CAP7B38-D17': 'Selected command boundaries/26 opener owners traced; remaining direct factories/row producers/reader and search/navigation SQL, alias/reflection ingress, branch/year/allowed-document origins and healthy outcomes not complete.',
        'CAP7B38-D19': 'Four ImportInventoryItems first-match writers and central/composite mapping are now read; whole SearchByID/ItemOper duplicate/insert/cancel/unit/serial and other copy/merge/VAT/discount/row producers remain local.',
        'CAP7B38-D22': 'Quotation CLR/HoldList/two transfer saves and six async-void publication boundaries assessed; remaining CheckBeforeClear, draft/new/open/normal/chrome/Escape/failure and shared-year owners remain local.',
        'CAP7B38-D25': 'Central update key/branch fallback/UI role defaults are traced; no deployed schema/grant attestation. Remaining all local authorization lookup/query/ownership/uniqueness consumers must be exhausted before individually evidenced policy handoffs.',
    }
    review['capabilities'] = {cid: dict(canonical_capability_row=canonical[cid], whole_capability_certified=False,
        local_semantic_obligations_complete=False, readable_local_externalized=False,
        remaining_readable_local=cap_remainders[cid], source_decision_ids=sorted(v.DECISIONS),
        fresh_whole_capability_assessment=False) for cid in v.TARGETS}
    review['unavailable_contracts_not_accepted_as_handoffs'] = [
        dict(id='R9BOUND-MODEL-OWNERSHIP', source_basis=[text_basis('external-AuditorAPI-reference')] + basis(v.IP, 'MappingInvoice') + basis(v.IPC, 'MappingInvoicecontract'),
            owner_role='Owner of externally referenced AuditorAPI model package', required_redacted_input='Versioned Invoice/InvoiceDGV/Invoicecontract/InvoiceItem/Entry setter, constructor, enum and collection ownership contract or redacted source; no credentials or business data.',
            absence_impact='Property sharing/deep copy/default enum and invariant behavior cannot be certified by local assignment syntax.', next_action='After readable local writers/consumers are exhausted, request the precise ownership/invariant contract by package version.',
            static_disposition='Blocked contract clarification, NOT an accepted completion handoff and not evidence all missing model behavior is defective.', readable_local_not_delegated='Mapping, composite, cache and four import bodies have been read; remaining SearchByID/ItemOper and all other consumers stay in local worklist.', accepted_external_handoff=False),
        dict(id='R9BOUND-POLICY-GRANTS', source_basis=basis(v.COMMON, 'AllowEdit') + basis(v.FP, 'LoadPermissionData') + basis(v.MC, 'ApplyPermissionToForm@System.Windows.Window') + basis(v.IP, 'SaveInvoice'),
            owner_role='Product/security policy and SQL grant owner', required_redacted_input='Authoritative form Name/Tag/role-to-command and document/branch/year allowed-set contract, plus redacted grant/schema manifest, not live identities or databases.',
            absence_impact='UI flags and writer SQL cannot certify a deployed allowed-set or deny rules. This bounded read does not establish absence of all policy documents elsewhere.', next_action='Finish remaining local lookup/query/reader/variant consumers, then request only the independently identified unresolved policy boundary.',
            static_disposition='No deployed authorization certification and no accepted handoff while local command/ingress ownership remains.', readable_local_not_delegated='All remaining local factories, query producers, reader and policy-key consumers remain locally owned.', accepted_external_handoff=False),
        dict(id='R9BOUND-REMOTE-RESULT', source_basis=basis(v.IP, 'SyncInvoice', 'SaveInvoice') + basis(v.IPC, 'SyncInvoice', 'SaveInvoice'),
            owner_role='Versioned cloud/tax integration contract owner', required_redacted_input='Redacted request/response, idempotency, remote commit/reject/partial/timeout and retry contract for called service version; no endpoint secrets, payload business data or live invocation.',
            absence_impact='Local Task<bool>/flags cannot attest remote durability or cross-transaction atomicity; locally supplied service/helper bodies are not declared absent.', next_action='Read remaining local service/queue/broker/response consumers before accepting any individual unavailable-contract disposition.',
            static_disposition='Static publication mismatch/source order only; no remote run, financial acceptance or completion handoff.', readable_local_not_delegated='SendData, offline queue, selected service dependencies and all remaining consumer logic stay in local worklist.', accepted_external_handoff=False),
    ]
    review.update(new_numbered_findings=[], all26_capabilities_freshly_semantically_reviewed=False,
        historical339_dictionaries_preserved_not_recertified=True,
        R8_historical_21Nov_label_or_user_date_attribution_authenticated=False,
        reference_date_disposition='New R9 uses current16-Nov session reference prospectively; frozen21-Nov labels, contradictory condensed-summary22-Nov assertions and raw clocks are not adopted as authority or retroactive chronology proof.')
    review['pinned_inputs'] = pins(*common, v.DISPLAYS, v.READS, v.MATRIX, v.ROOTS, v.WORK, 'capability-register-07B38.csv', 'capability-reconciliation-07B39R8.json')
    exclusive(v.REVIEW, review)
    print(json.dumps({'authored_exclusively': list(OUTPUTS), 'source_decisions': len(decisions_data),
        'selected_whole_contexts': sum(map(len, facts['methods'].values())),
        'command_reviews': len(matrix['command_reviews']), 'alternate_opener_owners': len(matrix['alternate_opener_reviews']),
        'application_execution_count': 0, 'whole_7B_static_assessment_complete': False}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    author()
