#!/usr/bin/env python3
"""Inert B34/R4r request/await illustrations and lexical observations only.

No C#/WPF,Tasks,Selenium,Chrome,SQL,REPX,PDF,files of a business request,
network,provider,phones or messages execute. Targets,DOM/element readiness,
return flags,file-version tokens and an explicit interleaving are SUPPLIED.
A path handed to a file input is not proof of bytes uploaded or delivery.
P6-031/033 ALREADY describe shared chat/file interleaving:zero new roots,
zero registry evidence extensions,all335 dictionaries/raw336 bytes exact.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ENTRY = 'dea2244267d74dd540af59c6e63b0f4362ab8c1c'
SC = 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
SX = 'SmartAuditERP/Form_WPF/frmInvSale.xaml'
WA = 'SmartAuditERP/Class/WhatsAppSender.cs'
SE = 'SmartAuditERP/Class/Session.cs'
PT = 'SmartAuditERP/Class/Print.cs'
SOURCE_SLICES = (
    (SC, 3124, 3126), (SC, 3128, 3141), (SC, 3142, 3155), (SC, 3156, 3165),
    (SC, 3166, 3177), (SC, 3179, 3187), (SC, 3188, 3199), (SX, 1187, 1191),
    (SE, 9, 21), (SE, 22, 30), (WA, 16, 21), (WA, 107, 118),
    (WA, 119, 144), (WA, 145, 155), (WA, 156, 180), (WA, 181, 189),
    (WA, 190, 217), (WA, 218, 228), (WA, 230, 245), (WA, 66, 105),
)
EXPLORATORY_SLICES = (
    (WA, 22, 63), (WA, 247, 261), (WA, 263, 266), (SC, 2986, 3006),
    (SC, 3007, 3033), (SC, 2581, 2595), (SC, 3201, 3208), (PT, 1193, 1229),
)
LIMIT = ('Supplied symbolic schedule/targets/DOM readiness/element validity and return flags only;'
         'not C# Tasks/WPF/Selenium/browser or PDF/network execution. Path/version tokens do not '
         'prove bytes uploaded,provider acceptance,delivery,save,financial loss or a repaired system.')


def token(value, *, empty=False):
    if (type(value) is not str or not (0 if empty else 1) <= len(value) <= 80
            or any(not (c.isascii() and (c.isalnum() or c in '_-:')) for c in value)):
        raise ValueError('Bounded opaque ASCII token required,not a path,phone or secret')
    return value


def flag(value):
    if type(value) is not bool:
        raise ValueError('Explicit bool only,not int or inferred SDK behaviour')
    return value


def caller_gate(items, *, customer_found=True, mobile_present=True,
                mapping_returned=True, export_returned=True):
    if type(items) is not int or not 0 <= items <= 100:
        raise ValueError('Supplied bounded item count,not bool')
    supplied = [flag(v) for v in (customer_found, mobile_present, mapping_returned, export_returned)]
    return items > 0 and all(supplied)


def session_route(*, present, handles_readable):
    present, handles_readable = flag(present), flag(handles_readable)
    return 'reuse-same-sender' if present and handles_readable else 'new-sender-initialization-awaited-not-authenticated'


class Trace:
    """Finite symbolic machine. No real scheduling,blocking,locks,DOM or files."""
    def __init__(self):
        self.requests = {}
        self.dom = {}
        self.files = {}
        self.events = []

    def add(self, name, target, file_key, version, *, sender='sender-S', caption='caption',
            items=1, customer_found=True, mobile_present=True,
            mapping_returned=True, export_returned=True):
        for t in (name, target, file_key, version, sender):
            token(t)
        token(caption, empty=True)
        allowed = caller_gate(items, customer_found=customer_found, mobile_present=mobile_present,
                              mapping_returned=mapping_returned, export_returned=export_returned)
        if name in self.requests or len(self.requests) >= 8:
            raise ValueError('At most8 distinct symbolic requests')
        self.requests[name] = dict(target=target, file_key=file_key, version=version, sender=sender,
            caption=caption, allowed=allowed, stage='created', result=None,
            caption_element_target=None, attachment_context=None, last_upload_context=None)
        return self

    def event(self, name, kind, *, context=None, **data):
        r = self.requests[name]
        item = dict(request=name, kind=kind, requested_target=r['target'],
                    selector_or_element_context=context, **data)
        self.events.append(item)
        return item

    def step(self, name, action, *, ready=True):
        token(name)
        ready = flag(ready)
        if name not in self.requests or len(self.events) >= 96:
            raise ValueError('Known request and bounded trace required')
        r = self.requests[name]
        expected = {'prepare': 'created', 'navigate': 'prepared', 'chat': 'await-chat',
                    'caption-enter': 'await-caption-enter', 'attach': 'await-attach',
                    'file': 'await-file', 'send': 'await-send', 'finish': 'await-return'}
        if action not in expected or r['stage'] != expected[action]:
            raise ValueError('Explicit legal source-order step required')
        context = self.dom.get(r['sender'])
        if action == 'prepare':
            if not r['allowed'] or not ready:
                r['stage'] = 'blocked-before-sender'
                self.event(name, 'caller-blocked')
            else:
                # Only dictionary tokens change:never File.Delete/ExportToPdf.
                self.files[r['file_key']] = r['version']
                r['stage'] = 'prepared'
                self.event(name, 'symbolic-export-returned', file_key=r['file_key'], version=r['version'])
        elif action == 'navigate':
            if ready:
                self.dom[r['sender']] = r['target']
                r['stage'] = 'await-chat'
                self.event(name, 'navigate-request-before-await', context=r['target'])
            else:
                self.fail(name, 'supplied-navigate-nonreturn')
        elif not ready:
            self.fail(name, 'supplied-' + action + '-not-ready-or-element-invalid')
        elif action == 'chat':
            self.event(name, 'generic-chat-selector-observed', context=context)
            if r['caption']:
                r['caption_element_target'] = context
                self.event(name, 'caption-typed-before-await', context=context, caption=r['caption'])
                r['stage'] = 'await-caption-enter'
            else:
                r['stage'] = 'await-attach'
        elif action == 'caption-enter':
            # Stored IWebElement is NOT silently retargeted after another navigation.
            # ready explicitly supplies its validity;stale-element failure is possible.
            self.event(name, 'caption-enter-request', context=r['caption_element_target'])
            r['stage'] = 'await-attach'
        elif action == 'attach':
            r['attachment_context'] = context
            self.event(name, 'generic-attach-button-request', context=context)
            r['stage'] = 'await-file'
        elif action == 'file':
            version = self.files.get(r['file_key'])
            if version is None:
                self.fail(name, 'supplied-file-absent')
            else:
                r['last_upload_context'] = context
                self.event(name, 'file-path-handed-to-input-not-upload-proof', context=context,
                           file_key=r['file_key'], latest_symbolic_version=version,
                           requested_version=r['version'], browser_read_bytes_proved=False)
                r['stage'] = 'await-send'
        elif action == 'send':
            self.event(name, 'generic-send-control-click-request', context=context,
                       previous_file_input_context=r['last_upload_context'], delivery_proved=False)
            r['stage'] = 'await-return'
        elif action == 'finish':
            r['result'], r['stage'] = True, 'returned'
            self.event(name, 'local-true-after-click-and-delay-not-delivered', context=context)
        return self

    def fail(self, name, reason):
        r = self.requests[name]
        r['result'], r['stage'] = False, 'returned'
        self.event(name, 'local-false-or-nonreturn-boundary', context=self.dom.get(r['sender']), reason=reason)

    def run_tail(self, name):
        r = self.requests[name]
        actions = {'created': 'prepare', 'prepared': 'navigate', 'await-chat': 'chat',
                   'await-caption-enter': 'caption-enter', 'await-attach': 'attach',
                   'await-file': 'file', 'await-send': 'send', 'await-return': 'finish'}
        for _ in range(9):
            if r['stage'] not in actions:
                break
            self.step(name, actions[r['stage']])
        return self

    def summary(self):
        return dict(requests={k: dict(v) for k, v in self.requests.items()},
                    symbolic_current_targets=dict(self.dom), symbolic_file_versions=dict(self.files),
                    operations=[dict(e) for e in self.events], delivery_proved=False,
                    file_bytes_read_or_uploaded_proved=False, limit=LIMIT)


def pair(*, same_file=False, same_target=False, separate_senders=False, caption=True):
    return (Trace().add('A', 'target-A', 'file-X' if same_file else 'file-A', 'version-A',
                       caption='caption-A' if caption else '')
            .add('B', 'target-A' if same_target else 'target-B',
                 'file-X' if same_file else 'file-B', 'version-B',
                 sender='sender-T' if separate_senders else 'sender-S',
                 caption='caption-B' if caption else ''))


def race(**kwargs):
    t = pair(**kwargs)
    t.step('A', 'prepare').step('A', 'navigate').step('B', 'prepare').step('B', 'navigate')
    t.run_tail('A').run_tail('B')
    return t


def build():
    illustrations = []
    def alg(n, title, result, passed, evidence, roots='P6-033'):
        illustrations.append(dict(id=f'ALG7B34-{n:02d}', title=title, supplied_trace=result,
            illustration_assertions_passed=bool(passed), finding_ids=roots, evidence=evidence,
            source_application_executed=False, limit=LIMIT))
    ev=lambda p,a,z:f'{p}:{a}-{z}'
    local=race();ops=local.events
    a_caption=next(e for e in ops if e['request']=='A' and e['kind']=='caption-enter-request')
    alg(1,'A resumes after B navigation on the SAME supplied valid sender',local.summary(),
        a_caption['selector_or_element_context']=='target-B',ev(WA,107,155)+';'+ev(SE,9,21),'P6-031;P6-033')
    seq=pair();seq.run_tail('A').run_tail('B')
    alg(2,'Sequential complete requests:negative control',seq.summary(),
        all(e['selector_or_element_context']==e['requested_target'] for e in seq.events if e['kind']=='generic-send-control-click-request'),ev(WA,107,217))
    separate=race(separate_senders=True)
    alg(3,'Distinct sender/driver tokens:conditional isolation control,not deployed repair',separate.summary(),
        all(e['selector_or_element_context']==e['requested_target'] for e in separate.events if e['kind']=='caption-enter-request'),ev(WA,16,21)+';'+ev(SE,9,21),'P6-031;P6-033')
    same=race(same_target=True)
    alg(4,'Same recipient removes this cross-target difference,not duplicate-attempt risk',same.summary(),
        all(e['selector_or_element_context']==e['requested_target'] for e in same.events if e['kind']=='caption-enter-request'),ev(WA,117,155))
    blank=race(caption=False)
    alg(5,'Blank caption skips text only;file-input context is still shared',blank.summary(),
        not any(e['kind']=='caption-enter-request' for e in blank.events) and any(e['request']=='A' and e['selector_or_element_context']=='target-B' for e in blank.events if e['kind']=='file-path-handed-to-input-not-upload-proof'),ev(WA,145,189))
    overwrite=race(same_file=True)
    alg(6,'Same invoice-number path:latest token B at A path handoff,not byte upload proof',overwrite.summary(),
        next(e for e in overwrite.events if e['request']=='A' and e['kind']=='file-path-handed-to-input-not-upload-proof')['latest_symbolic_version']=='version-B',ev(SC,3166,3177)+';'+ev(WA,181,189))
    distinct=race()
    alg(7,'Distinct file tokens do not fix shared chat context',distinct.summary(),
        next(e for e in distinct.events if e['request']=='A' and e['kind']=='file-path-handed-to-input-not-upload-proof')['latest_symbolic_version']=='version-A',ev(SC,3166,3187)+';'+ev(WA,181,189))
    zero=Trace().add('A','target-A','file-A','v-A',items=0).run_tail('A')
    alg(8,'Zero rows blocks before mapping/export/session',zero.summary(),not zero.files and not zero.dom,ev(SC,3128,3141))
    no_customer=Trace().add('A','target-A','file-A','v-A',customer_found=False).run_tail('A')
    alg(9,'Customer lookup false:source returns no sender request',no_customer.summary(),not no_customer.dom,ev(SC,3150,3192))
    no_mobile=Trace().add('A','target-A','file-A','v-A',mobile_present=False).run_tail('A')
    alg(10,'Empty mobile returns before PDF path/export',no_mobile.summary(),not no_mobile.files,ev(SC,3155,3175),'P6-032;P6-033')
    no_mapping=Trace().add('A','target-A','file-A','v-A',mapping_returned=False).run_tail('A')
    alg(11,'Mapping nonreturn supplied,not an SDK exception induced',no_mapping.summary(),not no_mapping.dom,ev(SC,3141,3146))
    no_export=Trace().add('A','target-A','file-A','v-A',export_returned=False).run_tail('A')
    alg(12,'Export nonreturn supplied:sender not reached',no_export.summary(),not no_export.dom,ev(SC,3172,3187))
    no_chat=Trace().add('A','target-A','file-A','v-A').step('A','prepare').step('A','navigate').step('A','chat',ready=False)
    alg(13,'Chat timeout/absence false before caption',no_chat.summary(),no_chat.requests['A']['result'] is False and not any(e['kind']=='caption-enter-request' for e in no_chat.events),ev(WA,119,144))
    no_attach=Trace().add('A','target-A','file-A','v-A')
    for a in ('prepare','navigate','chat','caption-enter'):no_attach.step('A',a)
    no_attach.step('A','attach',ready=False)
    alg(14,'Missing attachment button after caption request:existing partial outcome',no_attach.summary(),no_attach.requests['A']['result'] is False and any(e['kind']=='caption-enter-request' for e in no_attach.events),ev(WA,145,180))
    no_file=Trace().add('A','target-A','file-A','v-A')
    for a in ('prepare','navigate','chat','caption-enter','attach'):no_file.step('A',a)
    no_file.files.clear();no_file.step('A','file')
    alg(15,'Missing file can follow caption submission request',no_file.summary(),no_file.requests['A']['result'] is False and not any(e['kind']=='file-path-handed-to-input-not-upload-proof' for e in no_file.events),ev(WA,145,189))
    no_send=Trace().add('A','target-A','file-A','v-A')
    for a in ('prepare','navigate','chat','caption-enter','attach','file'):no_send.step('A',a)
    no_send.step('A','send',ready=False)
    alg(16,'File-input handoff with no send button is not Delivered',no_send.summary(),no_send.requests['A']['result'] is False,ev(WA,181,217))
    stale=Trace().add('A','target-A','file-A','v-A')
    for a in ('prepare','navigate','chat'):stale.step('A',a)
    stale.step('A','caption-enter',ready=False)
    alg(17,'Stored caption element can fail;no guaranteed retarget after capture',stale.summary(),stale.requests['A']['result'] is False,ev(WA,145,155)+';'+ev(WA,219,228))
    alg(18,'Handles readable chooses reuse,not account or recipient proof',dict(route=session_route(present=True,handles_readable=True)),session_route(present=True,handles_readable=True)=='reuse-same-sender',ev(SE,9,21)+';'+ev(WA,230,245),'P6-031')
    alg(19,'Missing/invalid sender requests initialization,not authenticated success',dict(missing=session_route(present=False,handles_readable=False),invalid=session_route(present=True,handles_readable=False)),session_route(present=False,handles_readable=False)==session_route(present=True,handles_readable=False),ev(SE,9,30)+';'+ev(WA,66,105),'P6-031;P6-033')
    alg(20,'Local true is click+delay only;caller does not assign bool',local.summary(),all(r['result'] is True for r in local.requests.values()) and local.summary()['delivery_proved'] is False,ev(WA,210,228)+';'+ev(SC,3185,3187))
    def text(p,a,z):return '\n'.join((ROOT/p).read_text().splitlines()[a-1:z])
    static=[]
    def st(n,title,p,a,z,ok,roots='P6-033'):
        static.append(dict(id=f'ST7B34-{n:02d}',title=title,evidence=ev(p,a,z),finding_ids=roots,
            documented_text_observation_matches=bool(ok),source_application_executed=False,
            limit='Lexical observation of exactly this selected slice;not compilation,SDK behaviour,DOM readiness,whole-callgraph protection or runtime acceptance.'))
    st(1,'XAML names the WhatsApp click entry',SX,1187,1191,'Click="SendWhatsapp_Click"' in text(SX,1187,1191))
    st(2,'Outer async-void delegates to inner async-void',SC,3124,3128,'=> printwhatsapp();' in text(SC,3124,3128) and text(SC,3124,3128).count('async void')==2)
    st(3,'Item-count guard precedes mapping;not a saved-state predicate proof',SC,3128,3141,'InvoiceItems.Count == 0' in text(SC,3128,3141))
    st(4,'Customer/mobile lookup and explicit Read guard present',SC,3150,3165,'if (reader.Read())' in text(SC,3150,3165) and 'IsNullOrEmpty(mobile)' in text(SC,3150,3165),'P6-032;P6-033')
    st(5,'Invoice-number-only path and regenerate before awaits',SC,3166,3177,'"INV" + txtNo.Text' in text(SC,3166,3177) and text(SC,3166,3177).index('File.Delete') < text(SC,3166,3177).index('ExportToPdf'))
    st(6,'Locals captured before two awaits;bool not assigned in selected caller',SC,3179,3187,'await Session.EnsureWhatsAppSessionAsync();' in text(SC,3179,3187) and 'await Session.waSender.SendInvoiceAsync(' in text(SC,3179,3187))
    st(7,'Static sender reused by handles-only check',SE,9,21,'static WhatsAppSender waSender;' in text(SE,9,21) and '!Session.waSender.IsSessionValid()' in text(SE,9,21),'P6-031;P6-033')
    st(8,'Initialization catch reports then returns without typed authentication outcome',SE,14,30,'Task EnsureWhatsAppSessionAsync()' in text(SE,14,30) and 'catch (Exception ex)' in text(SE,14,30),'P6-031;P6-033')
    st(9,'Sender stores driver and wait fields,not request-local arguments',WA,16,21,'private IWebDriver driver;' in text(WA,16,21) and 'private WebDriverWait wait;' in text(WA,16,21),'P6-031;P6-033')
    st(10,'Navigate precedes first asynchronous delay',WA,107,118,text(WA,107,118).index('this.driver.Navigate()')<text(WA,107,118).index('await Task.Delay(10000)'))
    st(11,'Chat readiness selector does not include recipient text',WA,119,144,"div[contenteditable='true'][data-tab='10']" in text(WA,119,144) and 'customerPhone' not in text(WA,119,144))
    st(12,'Caption element is captured before delayed Enter',WA,145,155,text(WA,145,155).index('webElement =')<text(WA,145,155).index('await Task.Delay(500)')<text(WA,145,155).index('Keys.Enter'))
    st(13,'Attachment lookup uses current driver generic button',WA,156,180,'this.driver.FindElement' in text(WA,156,180) and "//button[@data-tab='10']" in text(WA,156,180))
    st(14,'File existence check follows button delay,not immutable content proof',WA,181,189,text(WA,181,189).index('await Task.Delay(2000)')<text(WA,181,189).index('File.Exists(invoiceFilePath)')<text(WA,181,189).index('SendKeys(invoiceFilePath)'))
    st(15,'File-input selector is generic after delay',WA,181,189,"input[type='file']" in text(WA,181,189))
    st(16,'Send selector is generic with later true after click+delay',WA,190,217,"contains(@data-icon, 'send')" in text(WA,190,217) and text(WA,190,217).index('webElement3.Click()')<text(WA,190,217).index('return true;'))
    st(17,'Outer catch returns false;no blanket silence claim',WA,219,228,'MessageBox.Show' in text(WA,219,228) and 'return result;' in text(WA,219,228))
    st(18,'IsSessionValid reads handles,not logged-in account',WA,230,245,'this.driver.WindowHandles' in text(WA,230,245),'P6-031')
    st(19,'Selected sender body contains no local single-flight primitive',WA,107,228,all(x not in text(WA,107,228) for x in ('SemaphoreSlim','lock (','WaitAsync(','Monitor.Enter')))
    st(20,'Email comparison regenerates PDF before attaching and synchronous Send',PT,1193,1229,text(PT,1193,1229).index('ExportToPdf')<text(PT,1193,1229).index('new Attachment')<text(PT,1193,1229).index('smtpClient.Send'),'P6-034')
    def reads(slices):
        result=[]
        for p,a,z in slices:
            raw=(ROOT/p).read_bytes();assert 1<=a<=z<=len(raw.decode().splitlines())
            result.append(dict(path=p,start=a,end=z,sha256=hashlib.sha256(raw).hexdigest(),
                whole_local_file_selected=False,whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True))
        return result
    errors=[r['id'] for r in illustrations if r['illustration_assertions_passed'] is not True]+[r['id'] for r in static if r['documented_text_observation_matches'] is not True]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,
        new_root_ids=[],extended_existing_root_ids=[],existing_roots_deepened_without_registry_change=['P6-031','P6-033'],
        selected_source_paths=5,selected_contract_slices=20,context_slices_not_certified=8,whole_local_files_selected=0,
        illustration_count=len(illustrations),lexical_check_count=len(static),
        application_code_imported_or_executed=False,dotnet_wpf_sql_or_SDK_executed=False,
        browser_driver_provider_PDF_or_messages_executed=False,provider_acceptance_or_delivery_or_file_bytes_upload_proved=False,
        saved_invoice_dirty_DTO_contract_proved=False,application_remediation_performed=False,
        phase7C_started=False,phase8_authorized_or_started=False,all_callers_or_historical_bodies_certified=False,
        schedule_targets_readiness_and_version_tokens_are_supplied=True,stored_elements_not_silently_retargeted=True,
        path_handoff_not_content_upload_or_delivery_proof=True,prior_roots_already_describe_this_mechanism=True,
        retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
        erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
        bounded_source_reads_not_semantic_coverage=reads(SOURCE_SLICES),
        exploratory_source_reads_not_capability_certification=reads(EXPLORATORY_SLICES),
        illustrations=illustrations,static_lexical_contract_checks=static,errors=errors,limit=LIMIT)


if __name__ == '__main__':
    result=build()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(1 if result['errors'] else 0)
