#!/usr/bin/env python3
"""B28 source-bound, inert illustrations. NOT SQL/DataView/.NET/WPF execution.

One new root158: empty maximum-price branch skips view invalidation. The
reload-failure chain extends existing046 instead of counting another root.
Supplied integer rows, explicit actions and stipulated failure outcomes ONLY;
no provider failure, event scheduler, parsing/culture, DTO, save or loss tested.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
ENTRY = '436446091caf82c05ec01817bed5d18b4ea9fb34'
C = 'SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml.cs'
X = 'SmartAuditERP/Form_WPF/frmInvoiceSrch.xaml'
P = 'SmartAuditERP/Form_WPF/frmInvPurch.xaml.cs'
I = 'SmartAuditERP/Class/InvoiceOper.cs'
S = 'SmartAuditERP/Form_WPF/frmInvSale.xaml.cs'
SOURCE_SLICES = ((C,1,698,True),(X,1,561,True),(P,481,548,False),
                 (P,2641,2662,False),(I,3219,3290,False),(S,2610,2699,False))
EV_MAX = f'{C}:173-186;{C}:492-508;{C}:549-565;{X}:316-331'
EV_LOAD = f'{C}:49-66;{C}:189-211;{C}:267-284;{C}:310-334;{C}:567-596;{X}:391-414'
EV_CONSUMER = f'{P}:2641-2662;{P}:481-502;{I}:3219-3290'


def integer(value, label='integer'):
    if type(value) is not int or not 0 <= value <= 100000:
        raise ValueError(label + ': bounded non-Boolean integer required')
    return value


def records(rows):
    if type(rows) not in (list, tuple) or len(rows) > 12:
        raise ValueError('At most12 explicit supplied rows required')
    out=[];seen=set()
    for row in rows:
        if type(row) is not dict or set(row) != {'gid','net','day','branch'}:
            raise ValueError('Explicit gid/net/day/branch shape required, not an external DTO')
        gid=row['gid']
        if type(gid) is not str or re.fullmatch(r'fixture-[A-Z][0-9]?',gid) is None or gid in seen:
            raise ValueError('Unique artificial fixture identifiers required')
        seen.add(gid)
        out.append(dict(gid=gid,net=integer(row['net'],'net'),day=integer(row['day'],'ordinal-day'),branch=integer(row['branch'],'branch')))
    return out


def literal(text):
    """Restricted ASCII fixture domain, NOT double.TryParse or Unicode .NET."""
    if type(text) is not str or len(text)>8:
        raise ValueError('Short ASCII fixture text required')
    if text.strip(' \t\r\n') == '':
        return None
    if re.fullmatch(r'(?:0|[1-9][0-9]{0,4})',text) is None:
        raise ValueError('Only explicit small nonnegative integer literals; culture parsing not modeled')
    return integer(int(text),'literal')


def filtered(rows, minimum_text='', maximum_text=''):
    rows=records(rows);lo,hi=literal(minimum_text),literal(maximum_text)
    return [r for r in rows if (lo is None or r['net']>=lo) and (hi is None or r['net']<=hi)]


def maximum_changed(master, display_before, minimum_text, new_text):
    """Only the explicit selected branch of173..186, no WPF event count."""
    master,display_before=records(master),records(display_before)
    lo,hi=literal(minimum_text),literal(new_text)
    if hi is None:
        return dict(minimum_text=minimum_text,maximum_text=new_text,display=display_before,apply_filter_called=False)
    minimum='0' if lo is None else minimum_text
    return dict(minimum_text=minimum,maximum_text=new_text,display=filtered(master,minimum,new_text),apply_filter_called=True)


def minimum_changed(master, maximum_text, new_text):
    return dict(minimum_text=new_text,maximum_text=maximum_text,display=filtered(master,new_text,maximum_text),apply_filter_called=True)


def reload_result(display_before, supplied_replacement, outcome, minimum_text='', maximum_text=''):
    """Caller explicitly cleared master; failure is stipulated, never induced.

    The optional partial-master case stipulates supplied contents at the throw;
    it does not claim SqlDataAdapter has exhibited any particular partial fill.
    """
    before,replacement=records(display_before),records(supplied_replacement)
    if outcome not in ('success','failed-before-fill','failed-with-supplied-partial-master'):
        raise ValueError('Explicit bounded outcome required')
    literal(minimum_text);literal(maximum_text)
    if outcome=='failed-before-fill' and replacement:
        raise ValueError('Before-fill failure cannot have supplied replacement rows')
    success=outcome=='success'
    return dict(master=replacement,display=filtered(replacement,minimum_text,maximum_text) if success else before,
                apply_filter_reached=success,console_catch_taken=not success,
                source_health_flag_or_invalidation_written=False)


def selected_result(display, index, gesture='double-click'):
    display=records(display)
    if gesture not in ('double-click','enter-with-explicit-valid-row-index'):
        raise ValueError('Only documented ordinary selection branches')
    if index is None:
        return dict(done=False,gid='-1')
    if type(index) is not int or not 0<=index<len(display):
        raise ValueError('Explicit existing selected index required')
    return dict(done=True,gid=display[index]['gid'])


def consumer_lookup(result, supplied_rows, branch):
    rows=records(supplied_rows);integer(branch,'branch')
    if (type(result) is not dict or set(result)!={'done','gid'} or type(result['done']) is not bool
            or type(result['gid']) is not str or (result['gid']!='-1' and re.fullmatch(r'fixture-[A-Z][0-9]?',result['gid']) is None)):
        raise ValueError('Only the explicit selected result fields, not a DTO/default oracle')
    if not result['done'] or result['gid']=='-1':return []
    return [r for r in rows if r['gid']==result['gid'] and r['branch']==branch]


def gids(rows):return [r['gid'] for r in rows]


def collect():
    texts={};reads=[]
    for path,start,end,whole in SOURCE_SLICES:
        raw=(ROOT/path).read_bytes();lines=raw.decode('utf-8',errors='strict').splitlines()
        if not 1<=start<=end<=len(lines):raise ValueError('Source range changed:'+path)
        if whole and (start,end)!=(1,len(lines)):raise ValueError('Declared whole local file changed:'+path)
        texts.setdefault(path,lines)
        reads.append(dict(path=path,start=start,end=end,whole_local_file_selected=whole,
          sha256=hashlib.sha256(raw).hexdigest(),encoding='strict-utf-8',whole_bytes_read_for_hash_and_line_index_not_whole_body_review=True))
    get=lambda p,a,b:'\n'.join(texts[p][a-1:b])
    rows=[dict(gid='fixture-A',net=5,day=10,branch=1),dict(gid='fixture-B',net=20,day=20,branch=1)]
    old=filtered(rows,'0','10');limited=maximum_changed(rows,rows,'0','10')
    empty=maximum_changed(rows,old,'0','');space=maximum_changed(rows,old,'0',' \t')
    failure=reload_result([rows[0]],[],'failed-before-fill')
    partial=reload_result([rows[0]],[rows[1]],'failed-with-supplied-partial-master')
    chosen=selected_result(failure['display'],0)
    cases=[]
    def case(title,root,evidence,actual,expected,limit):
        cases.append(dict(id=f'ALG7B28-{len(cases)+1:02d}',title=title,finding_ids=root,evidence=evidence,
          actual=copy.deepcopy(actual),expected=copy.deepcopy(expected),illustration_assertions_passed=actual==expected,
          source_application_executed=False,limit=limit))
    narrow='Restricted integer net values5/20 and explicit handlers; not .NET numeric/culture/DataView parsing or WPF events.'
    health='A successful old display is supplied, then a source failure is stipulated after explicit master.Clear. No provider or business execution.'
    case('Nonblank maximum10 applies the cap','P7-158',EV_MAX,(gids(limited['display']),limited['apply_filter_called']),(['fixture-A'],True),narrow)
    case('Empty maximum skips ApplyFilter despite full master','P7-158',EV_MAX,(gids(empty['display']),empty['apply_filter_called'],gids(filtered(rows,'0',''))),(['fixture-A'],False,['fixture-A','fixture-B']),narrow)
    case('ASCII whitespace also skips the same maximum branch','P7-158',EV_MAX,(gids(space['display']),space['apply_filter_called']),(['fixture-A'],False),'Same158 root, not a second whitespace or Unicode parsing finding. '+narrow)
    wide=maximum_changed(rows,old,'0','30')
    case('Nonempty wider maximum re-applies from the complete master','P7-158',EV_MAX,(gids(wide['display']),wide['apply_filter_called']),(['fixture-A','fixture-B'],True),'Positive control: neither fixed-process source155 nor a missing source row is needed. '+narrow)
    minclear=minimum_changed(rows,'','')
    case('Empty minimum unconditionally re-applies the filter','P7-158',EV_MAX,(gids(minclear['display']),minclear['apply_filter_called']),(['fixture-A','fixture-B'],True),narrow)
    minrefresh=minimum_changed(rows,empty['maximum_text'],'0')
    case('Another explicit filter action can recover the stale max view','P7-158',EV_MAX,gids(minrefresh['display']),['fixture-A','fixture-B'],'Counter-control, not an application fix or an event-order assertion.')
    clear=reload_result(old,rows,'success','','')
    case('Explicit successful Clear reload can recover both rows','P7-158',f'{C}:236-254;{C}:327-334;{C}:549-596',gids(clear['display']),['fixture-A','fixture-B'],'Only final supplied successful reload. Does not accept caller eligibility reset156 or hidden event counts.')
    fresh=maximum_changed(rows,rows,'','')
    case('Initially empty maximum with an already current view has no drift','P7-158',EV_MAX,gids(fresh['display']),['fixture-A','fixture-B'],'A prior cap is required for this counterexample; no claim every empty field is wrong.')
    case('Failed reload leaves empty master but old independent display','P7-046',EV_LOAD,(gids(failure['master']),gids(failure['display']),failure['apply_filter_reached'],failure['console_catch_taken']),([],['fixture-A'],False,True),health)
    case('Supplied partial master failure also does not publish replacement','P7-046',EV_LOAD,(gids(partial['master']),gids(partial['display'])),(['fixture-B'],['fixture-A']),'Partial contents are stipulated only; no actual partial-fill behavior measured. '+health)
    case('Ordinary double-click exports the old displayed identity','P7-046',f'{C}:267-284;{C}:310-334',chosen,dict(done=True,gid='fixture-A'),'Existing displayed selected row supplied; not a WPF gesture, Return guard or SQL execution.')
    consumed=consumer_lookup(chosen,rows,1)
    case('Consumer still matches old GID and branch, not requested day20','P7-046',EV_LOAD+';'+EV_CONSUMER,(gids(consumed),[r['day'] for r in consumed]),(['fixture-A'],[10]),'Only selected predicate boundary; no completed Navigate render, financial save or lost GlobalID061 claim.')
    success=reload_result([rows[0]],[rows[1]],'success')
    case('A successful replacement publishes only the new display','P7-046',f'{C}:310-334;{C}:492-508;{C}:567-596',gids(success['display']),['fixture-B'],health)
    okempty=reload_result([rows[0]],[],'success')
    case('A successful empty replacement removes old display rows','P7-046',f'{C}:327-334;{C}:567-596',gids(okempty['display']),[],'Distinguishes successful empty from failed/unknown, not a database result measured here.')
    case('Default not-done result is not consumed','P7-046',f'{C}:49-66;{P}:2641-2662',consumer_lookup(selected_result([],None),rows,1),[],'Positive guard on explicitly supplied result fields; no external DTO/default assumption.')
    case('Different branch remains a positive nonmatch control','P7-046',f'{P}:2641-2662',consumer_lookup(chosen,rows,2),[],'No deployed authorization or uniqueness proof; only the branch predicate on supplied rows.')
    lexical=[]
    def textcase(label,root,evidence,condition,limit):
        lexical.append(dict(id=f'ST7B28-{len(lexical)+1:02d}',title=label,finding_ids=root,evidence=evidence,
         documented_text_observation_matches=bool(condition),source_application_executed=False,limit=limit))
    lim='Lexical source observation only; not executing the application, provider, parser, event loop, SDK or business policy.'
    t=get(C,49,66)
    textcase('master and display are independent; ItemsSource is display','P7-046',f'{C}:49-66',all(x in t for x in ('new DataTable()','new ObservableCollection<InvoiceSrchRow>()','dgvItems.ItemsSource = _displayRows')),lim)
    t=get(C,178,186)
    textcase('ApplyFilter is inside nonblank maximum guard','P7-158',f'{C}:178-186',t.count('ApplyFilter();')==1 and 'if (!string.IsNullOrWhiteSpace(txtMaxPrice.Text))' in t and 'else' not in t,lim)
    textcase('minimum handler unconditionally calls ApplyFilter','P7-158',f'{C}:173-176','ApplyFilter();' in get(C,173,176) and 'if (' not in get(C,173,176),lim)
    textcase('maximum predicate is optional only when parse succeeds','P7-158',f'{C}:549-565','double.TryParse(txtMaxPrice.Text, out double maxPrice)' in get(C,549,565) and 'Net <= {maxPrice}' in get(C,549,565),lim)
    t=get(X,316,331)
    textcase('both price fields are wired TextChanged','P7-158',f'{X}:316-331',all(x in t for x in ('txtMinPrice','txtMaxPrice','txtMaxPrice_TextChanged','txtMinPrice_TextChanged')),lim)
    t=get(C,189,211)
    textcase('each date handler clears master then calls reload','P7-046',f'{C}:189-211',t.count('_masterTable.Clear();')==2 and t.count('LoadInvoices();')==2,lim)
    t=get(C,310,334)
    textcase('Fill must finish before ApplyFilter and catch only writes console','P7-046',f'{C}:310-334',t.index('adapter.Fill(_masterTable);')<t.index('ApplyFilter();')<t.index('catch (Exception ex)') and 'Console.WriteLine(ex.Message);' in t and '_displayRows' not in t,lim)
    t=get(C,492,508)+get(C,567,596)
    textcase('display refresh is separate and clears display only when reached','P7-046',f'{C}:492-508;{C}:567-596','RefreshDisplayRows(view);' in t and '_displayRows.Clear();' in t,lim)
    t=get(C,267,284)
    textcase('ordinary double click exports row GID and done','P7-046',f'{C}:267-284',all(x in t for x in ('dgvItems.SelectedItem as InvoiceSrchRow','ISDone      = true;','InvGlobalID = row.InvGlobalID;','Hide();')),lim)
    t=get(C,89,116)
    textcase('Enter also exports an explicitly valid displayed row','P7-046',f'{C}:89-116','_displayRows[_rowIndex]' in t and 'InvGlobalID = row.InvGlobalID;' in t and 'ISDone      = true;' in t,lim)
    t=get(P,2641,2662)
    textcase('purchase caller consumes done and GID with branch only','P7-046',f'{P}:2641-2662',all(x in t for x in ('frm.ISDone','frm.InvGlobalID','branch={MainClass.BranchNo}','this.Navigate(')) and 'SelectedDate' not in t and 'health' not in t.lower(),lim)
    textcase('Navigate forwards the query to BindingInvoice','P7-046',f'{P}:481-502','InvoiceOper.BindingInvoice(ref this.Invoic, sqlStr);' in get(P,481,502),lim)
    textcase('selected reader maps supplied row identity','P7-046',f'{I}:3219-3290','Invo.InvGlobalID = Conversions.ToString(sqlDataReader["InvGlobalID"]);' in get(I,3219,3290),lim)
    t=get(S,2641,2662)
    textcase('selected sales caller is a bounded supporting comparison','P7-046',f'{S}:2610-2699','new frmInvoiceSrch()' in t and 'frm.ISDone' in t and 'Navigate(' in t,lim+' This is not all sales caller paths or a second finding.')
    t=get(C,236,254)
    textcase('Clear has an explicit reload at the end','P7-158',f'{C}:236-254','txtMaxPrice.Text         = "";' in t and '_masterTable.Clear();' in t and 'LoadInvoices();' in t,lim+' Does not approve the mandatory-condition loss156.')
    t=get(C,219,229)
    textcase('period and postponed remain separately named leads','H7B28-05',f'{C}:219-229','ckTotalPeriod_CheckedChanged' in t and 'txtFromDate.IsEnabled' in t and 'LoadInvoices();' not in t,lim+' Period/postponed/quoting/return are not adjudicated extra findings here.')
    errors=[r['id'] for r in cases if r['illustration_assertions_passed'] is not True]+[r['id'] for r in lexical if r['documented_text_observation_matches'] is not True]
    return dict(audit_reference_date_utc='2026-11-16',entry_checkout=ENTRY,source_head='10ba215152f722c8808aea0bb672c1d1d4d9d711',
      method='Source hashes/lexical checks plus finite supplied-record predicate illustrations; NEVER C#/VB/WPF/SQL/DataView execution',
      application_code_imported_or_executed=False,dotnet_wpf_sql_or_DataView_executed=False,application_remediation_performed=False,
      phase7C_started=False,phase8_authorized_or_started=False,all_callers_or_external_DTOs_body_reviewed=False,
      actual_WPF_event_order_or_count_claimed=False,financial_or_status_policy_invented=False,external_DTO_constructor_defaults_assumed=False,
      database_commit_or_saved_loss_claimed=False,provider_failure_or_partial_fill_observed=False,
      erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,scanner_or_printer_tests_executed=0,
      B_R4l_bounded_not_whole7B_closure=True,unresolved_external_contracts_and_explicit_splits_retained=True,
      selected_paths_strict_utf8_decode=True,prior045_046_085_155_156_157_not_recounted=True,
      new_root_ids=['P7-158'],extended_existing_root_ids=['P7-046'],illustration_count=len(cases),lexical_check_count=len(lexical),
      selected_source_paths=len({r[0] for r in SOURCE_SLICES}),whole_local_search_files_selected=2,source_read_slice_count=len(reads),
      retained_additive_B10_arithmetic_erratum=dict(local_cost=10,reference_cost=120,equality1_control=10,protected_G138_not_rewritten=True),
      unadjudicated_source_leads_not_additional_findings=['period/postponed source-view reconciliation','DataView quoting/culture/invalid numeric input','return eligibility/failure policy','external DTO/reader/Loaded/complete save outcome'],
      bounded_source_reads_not_semantic_coverage=reads,illustrations=cases,static_lexical_contract_checks=lexical,errors=errors)


if __name__=='__main__':
    result=collect();print(json.dumps(result,ensure_ascii=False,indent=2));raise SystemExit(bool(result['errors']))
