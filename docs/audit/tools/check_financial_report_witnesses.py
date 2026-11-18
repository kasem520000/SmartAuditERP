#!/usr/bin/env python3
"""Independent, manually transcribed7B2 illustrations and bounded literal checks.

Read-only Python stdlib. No application imports, C#/WPF/SQL/DevExpress compiler,
assemblies, spreadsheet evaluation, network, providers or devices. Arithmetic
fixtures illustrate specific local rules, not the executing ERP. Literal checks
only bind explicitly selected source text, not callgraphs, schema or semantics.
"""
from __future__ import annotations
import csv
from datetime import datetime, timedelta
import io
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[3]
EVIDENCE={'P7-052': 'SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:198-234;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:273-291;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:421-450;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:487-505', 'P7-053': 'SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:315-376;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:437-473;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:487-559', 'P7-054': 'SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:319-417;SmartAuditERP/Form_WPF/frmRptInventory.xaml:252-264', 'P7-055': 'SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:697-743;SmartAuditERP/Class/Report.cs:380-406;SmartAuditERP/Class/Report.cs:451-462;SmartAuditERP/Class/Report.cs:531-553;SmartAuditERP/Class/Report.cs:597-608', 'P7-056': 'SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:232-252;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:280-294;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml:649-700;SmartAuditERP/Properties/Resources.resx:3054-3064;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:798-809;SmartAuditERP/Form_WPF/frmSafeAdjust.xaml.cs:852-865;SmartAuditERP/Form_WPF/frmInventoryTransfer.xaml.cs:909-927', 'P7-057': 'SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:232-266;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1360-1366;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1479;SmartAuditERP/Properties/Resources.resx:3054-3056', 'P7-058': 'SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:187-205;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:312-347;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:889-943;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml:410-446', 'P7-059': 'SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:239-266;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:289-304;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:745-758;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml:355-366', 'P7-060': 'SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:289-356;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:434-449;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1360-1366;SmartAuditERP/Form_WPF/frmProductionOrder.xaml.cs:1425-1479;SmartAuditERP/Properties/Resources.resx:3054-3060', 'P7-061': 'SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:289-304;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:359-387;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1011-1172;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml:708-724;SmartAuditERP/Class_WPF/ItemActivityRow_ActivityDetailed.cs:13-39', 'P7-062': 'SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:184-223;SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:245-266;SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:279-302;SmartAuditERP/Form_WPF/frmRptKhzna.xaml:270-308', 'P7-063': 'SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:657-667;SmartAuditERP/Class/InvoiceOper.cs:3725-3746;SmartAuditERP/Form_WPF/frmRptInventory.xaml:370-409', 'P7-064': 'SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:161-169;SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:328-340;SmartAuditERP/Form_WPF/frmRptEntries.xaml:702-725', 'P7-065': 'SmartAuditERP/Form_WPF/frmRptIncomeStatement.xaml.cs:220-236;SmartAuditERP/Form_WPF/frmRptIncomeStatement.xaml.cs:332-406;SmartAuditERP/Form_WPF/frmMezanyaArba7.xaml.cs:194-230;SmartAuditERP/Form_WPF/frmMezanyaArba7.xaml.cs:304-322;SmartAuditERP/Class/Inventory.cs:462-472;SmartAuditERP/Properties/Resources.resx:48189-48209;SmartAuditERP/Form_WPF/frmRptIncomeStatement.xaml:208-220;SmartAuditERP/Form_WPF/frmMezanyaArba7.xaml:212-225', 'P1-011': 'SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:434-491;SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs:219-238', 'P1-033': 'SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:507-531;SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:576-581;SmartAuditERP/Form_WPF/frmRptEntries.xaml:730-738;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:824-828;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml:338-341;SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:428-435', 'P1-013': 'SmartAuditERP/Home.xaml.cs:2951-2965;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:201-213', 'P2-001': 'SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:1174-1193;SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:551-604', 'P2-010': 'SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:161-169;SmartAuditERP/Form_WPF/frmRptEntries.xaml.cs:365-400', 'P3-008': 'SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:159-180', 'P3-019': 'SmartAuditERP/Form_WPF/frmRptBalances.xaml.cs:248-297;SmartAuditERP/Form_WPF/frmRptBalances.xaml.cs:393-421;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:315-351;SmartAuditERP/Form_WPF/frmMezanyaArba7.xaml.cs:196-230', 'P3-023': 'SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:195-198;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:339-345;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:263-266;SmartAuditERP/Form_WPF/frmRptItemsActivityDetailed.xaml.cs:306-312;SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:188-200;SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:314-321;SmartAuditERP/Form_WPF/frmRptKhzna.xaml:291-299', 'P4-007': 'SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:264-266;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:363-427', 'P4-008': 'SmartAuditERP/Form_WPF/frmRptIncomeStatement.xaml.cs:366-406;SmartAuditERP/Form_WPF/frmMezanyaArba7.xaml.cs:304-322', 'P7-045': 'SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:705-749;SmartAuditERP/Form_WPF/frmRptBalances.xaml.cs:518-551;SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs:269-296', 'P7-046': 'SmartAuditERP/Form_WPF/frmAccountsStatement.xaml.cs:310-327;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:348-361;SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs:153-159', 'P7-048': 'SmartAuditERP/Form_WPF/frmRptBalances.xaml.cs:489-509;SmartAuditERP/Form_WPF/frmRptCostCenter.xaml.cs:668-692;SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:397-417;SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs:657-668;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:749-761;SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs:341-364', 'P7-049': 'SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:410-417;SmartAuditERP/Form_WPF/frmRptItemsActivity.xaml.cs:749-761;SmartAuditERP/Form_WPF/frmRptItemsExpiration.xaml.cs:341-364', 'P7-050': 'SmartAuditERP/Form_WPF/frmRptKhzna.xaml.cs:390-417', 'H7B2-02': 'SmartAuditERP/Properties/Resources.resx:3724-3736', 'P4-009': 'SmartAuditERP/Properties/Resources.resx:3724-3736'}

ALG=[]
ST=[]
READS=[]

def evidence(ids):
    result=[]
    for fid in ids.split(';'):
        for part in EVIDENCE[fid].split(';'):
            if part not in result: result.append(part)
    return ';'.join(result)

def illustration(ids,title,inputs,actual,reference,condition,limit):
    assert condition, title
    ALG.append(dict(id=f'ALG7B2-{len(ALG)+1:02d}',finding_ids=ids,title=title,
        synthetic_inputs=inputs,transcribed_rule_result=actual,independent_contract_reference=reference,
        evidence=evidence(ids),illustration_assertions_passed=True,source_application_executed=False,
        limit=limit+' Python fixture only; not C#/SQL/WPF or financial acceptance.'))

def bounded(path,start,end):
    lines=(ROOT/path).read_text(encoding='utf-8-sig').splitlines()
    assert 1<=start<=end<=len(lines), (path,start,end)
    row=dict(path=path,start=start,end=end)
    if row not in READS: READS.append(row)
    return '\n'.join(lines[start-1:end])

def textcheck(ids,title,observed):
    assert all(observed.values()), (title,observed)
    ST.append(dict(id=f'ST7B2-{len(ST)+1:02d}',finding_ids=ids,title=title,
        observations=observed,documented_text_observation_matches=True,evidence=evidence(ids),
        source_application_executed=False,
        limit='Bounded literal observation only; no overload resolution, semantic/callgraph completeness, UI rendering, deployed data or execution inferred.'))

F='SmartAuditERP/Form_WPF/'
C='SmartAuditERP/Class/'
R='SmartAuditERP/Properties/Resources.resx'
# 01: the local inverted ancestry predicate, not a production tree algorithm.
parents={10:0,11:10,111:11,90:0,99:90}
selected=10
accepted_parent=parents[99] if parents[99]!=selected else -1
immediate=[k for k,v in parents.items() if v==selected]
expected_subtree=[10,11,111]
illustration('P7-052','Unrelated ancestor accepted; detail is only one level',
    dict(parents=parents,selected=selected,foreign_node=99),
    dict(foreign_parent_result=accepted_parent,accepted=accepted_parent!=-1,detail_scope=immediate),
    dict(foreign_accepted=False,subtree=expected_subtree),accepted_parent==90 and immediate==[11],
    'Self postings depend on policy; this fixture demonstrates unrelated acceptance and missing transitive descendants, not cycles.')
# 02: CC-only first-match join, plus movement-led row enumeration.
opening=[('CC1','A',100),('CC1','B',200),('CC2','C',300)]
movements=[('CC1','A',10),('CC1','B',20)]
projected=[next(o[2] for o in opening if o[0]==cc)+q for cc,acc,q in movements]
reference=[next(o[2] for o in opening if o[:2]==(cc,acc))+q for cc,acc,q in movements]
illustration('P7-053','First opening reused across accounts; opening-only row absent',
    dict(opening=opening,movements=movements),dict(closings=projected,opening_only_rows=0),
    dict(closings=reference,opening_only_rows=1),projected==[110,120] and reference==[110,220],
    'Chosen first-row order is explicit; SQL order is not guaranteed. This is not summing running balance columns.')
# 03: a failed data bridge cannot carry the loaded row collection.
loaded=[{'InvoiceNo':1},{'InvoiceNo':2}]
argument=None
returned_tables=[] if argument is None else [loaded]
illustration('P7-055','Null bridge has no path carrying two loaded rows',
    dict(loaded_rows=loaded,argument=argument),dict(returned_tables=returned_tables),
    dict(required_loaded_count=2),len(loaded)==2 and returned_tables==[],
    'Transcribed catch return only. Does not choose between GridView/DataTable overloads or assert successful compilation/printing; ambiguity may block first.')
# 04: wrong classification need not imply wrong net for every fixture.
q7,q8=5,6
actual={'transfer_in':q7,'adjustment_in':q8,'net':q7+q8}
expected={'transfer_in':q8,'adjustment_in':q7,'net':q7+q8}
illustration('P7-056','Swapped adjustment/transfer columns with net counterevidence',
    {'type7_input':q7,'type8_input':q8},actual,expected,actual!=expected and actual['net']==expected['net'],
    'Net equality is retained as counterevidence to a blanket stock-total inversion claim.')
# 05: fixed enumerated type set omits persisted valid production movements.
selected_types={9,1,2,3,7,8,4,5}
fixture=[(1,10),(6,-3)]
actual=sum(q for typ,q in fixture if typ in selected_types)
expected=sum(q for typ,q in fixture)
illustration('P7-057','Production consumption omitted from aggregate quantity',
    {'movements':fixture,'enumerated_types':sorted(selected_types)},
    {'quantity':actual,'production_only_included':6 in selected_types},{'quantity':expected,'production_only_included':True},
    actual==10 and expected==7 and 6 not in selected_types,
    'A valid persisted row is assumed; does not execute or establish success of the production writer with prior P4-020 barriers.')
# 06: empty client-filter branch leaves the same rows regardless of selection.
client_rows=[('A',3),('B',7)]
actual=sum(q for _,q in client_rows)
expected=sum(q for client,q in client_rows if client=='A')
illustration('P7-058','Ignored selected customer does not narrow quantities',
    {'rows':client_rows,'selection':'A'},actual,expected,actual==10 and expected==3,
    'Query omission only. An earlier Items/ItemsSource barrier, analogous to the historical P7-027 invariant, can block real selection; it is not counted as another new defect here.')
# 07: TOP before eligibility / ascending chronology.
dates=['2026-01-01','2026-01-09']
actual=sorted(dates)[:1]
expected=sorted(dates,reverse=True)[:1]
illustration('P7-059','Latest option uses ascending first row',dates,actual,expected,
    actual==['2026-01-01'] and expected==['2026-01-09'],
    'Distinct dates; no assumed tie ordering or SQL execution.')
# 08: mixed production header contains outward component detail.
invtype,header_proc,sub_proc,qty=6,1,2,3
lookup_proc=sub_proc if invtype==7 else header_proc
is_input={(6,1):1,(6,2):2}[(invtype,lookup_proc)]
actual=qty if is_input==1 else -qty
expected=-qty
illustration('P7-060','Component uses header production input direction',
    dict(invtype=invtype,header_proc=header_proc,sub_proc=sub_proc,qty=qty),actual,expected,
    actual==3 and expected==-3,'Seed semantics must match deployment; a valid persisted production component is assumed.')
# 09: lost identity yields multiple candidates; no arbitrary winner asserted.
docs=[dict(id=42,branch=1,gid='G1'),dict(id=42,branch=2,gid='G2')]
local=[d['gid'] for d in docs if d['id']==42]
arabic_cases={'فاتورة مبيعات','مرتجع مبيعات','فاتورة مشتريات'}
illustration('P7-061','Local-number lookup is non-unique and localized case has no English route',
    {'docs':docs,'display_en':'Sale invoice'},
    {'candidate_gids':local,'english_case_found':'Sale invoice' in arabic_cases},
    {'required_gid':'G2','route_by_type_not_display':True},len(local)==2 and 'Sale invoice' not in arabic_cases,
    'No row order, actual opened branch or server authorization outcome is asserted.')
# 10: previous < midnight vs period >= 10:00 leaves an uncovered interval.
midnight=datetime(2026,1,2)
start=midnight+timedelta(hours=10)
events=[(midnight-timedelta(hours=1),100),(midnight+timedelta(hours=9),20),(midnight+timedelta(hours=11),-5)]
actual=sum(q for d,q in events if d<midnight)+sum(q for d,q in events if d>=start)
expected=sum(q for d,q in events)
illustration('P7-062','Intraday opening gap excludes same-day earlier cash movement',
    {'events':[(d.isoformat(),q) for d,q in events],'start':start.isoformat()},actual,expected,
    actual==95 and expected==115,'No SQL timezone, culture conversion or cash-account lookup execution is assumed; start00:00 is a counterexample without this gap.')
# 11: concrete producer/consumer field mapping.
row={'InvoiceNo':42,'InvNote':'استلام رف3'}
illustration('P7-063','Number-labelled export cell takes notes',row,row['InvNote'],row['InvoiceNo'],
    row['InvNote']!=row['InvoiceNo'],'Does not infer missing InvoiceTxt.InvNo property or external alias behavior.')
# 12: mixed id cursor/date ordering skips one chronological row.
entries=[(1,3),(2,1),(3,2)]
first=min(entries,key=lambda p:p[1])
forward=[first[0]]
current=first
while True:
    candidates=[p for p in entries if p[0]>current[0]]
    if not candidates: break
    current=min(candidates,key=lambda p:p[1])
    forward.append(current[0])
expected=[p[0] for p in sorted(entries,key=lambda p:p[1])]
illustration('P7-064','Date-ordered next with id cursor skips chronological last',entries,forward,expected,
    forward==[2,3] and expected==[2,3,1],'Dates do not follow IDs in this explicit fixture; monotonic dates can hide the problem.')
# 13: GL all-branch selection is not passed to stock source.
stocks={1:100,2:200}
actual=stocks[1]
expected=sum(stocks.values())
illustration('P7-065','All-branch GL with current-branch-only stock',stocks,
    {'gl_scope':[1,2],'stock_scope':[1],'stock_value':actual},
    {'gl_scope':[1,2],'stock_scope':[1,2],'stock_value':expected},actual==100 and expected==300,
    'Financial periodic/perpetual policy and manual _Stock override remain separate; this models branch-set mismatch only.')
# 14: carry-forward cannot be replaced by type0 inside the period.
opening,prior,period=100,20,-5
illustration('P3-019','Period-only closing omits pre-period ordinary movement',
    dict(opening_before=opening,ordinary_before=prior,in_period=period),period,opening+prior+period,
    period==-5 and opening+prior+period==115,'Required closing/as-of meaning must be agreed; a movement-only metric has a different contract.')
# 15: opposite boundary errors are not the same effect.
endday=datetime(2026,1,2)
eod=endday+timedelta(hours=23,minutes=59,seconds=59)
nextmid=endday+timedelta(days=1)
illustration('P3-023','Inclusive date-only vs inclusive next-midnight boundaries',
    {'date_to':endday.isoformat(),'late':eod.isoformat(),'nextmid':nextmid.isoformat()},
    {'aggregate_includes_late':eod<=endday,'detail_includes_nextmid':nextmid<=nextmid},
    {'aggregate_includes_late':True,'detail_includes_nextmid':False},not(eod<=endday) and nextmid<=nextmid,
    'No SQL DATETIME precision or timezone execution; hour/minute contracts need separate acceptance.')
# 16: base quantity times pack price divided by base quantity remains pack price.
baseqty,packprice,equality=12,120,12
actual=(baseqty*packprice)/baseqty
expected=packprice/equality
illustration('P4-007','Base-quantity weighted pack price is not base-unit average',
    dict(baseqty=baseqty,packprice=packprice,equality=equality),actual,expected,actual==120 and expected==10,
    'Unit convention is inherited from frozen inventory evidence; does not establish a complete chosen costing policy.')
# 17: benign neutral CSV parser, never Excel/formula evaluation.
raw='id,amount\n1,'+format(1000.5,',.2f')+'\n'
parsed=list(csv.reader(io.StringIO(raw)))
illustration('P7-048','Unquoted N2 thousands separator creates an extra CSV field',
    {'raw':raw},parsed,{'header_columns':2,'required_data_columns':2},len(parsed[0])==2 and len(parsed[1])==3,
    'Specific unquoted writer/en-style format example only; a correctly quoted comma/newline is not inherently broken.')
# 18: file type is not its extension.
raw_bytes=b'row,amount\n1,10.00\n'
illustration('P7-050','CSV bytes do not become an XLSX container by renaming',
    {'extension':'.xlsx','bytes_hex':raw_bytes.hex()}, {'starts_with_zip_signature':raw_bytes.startswith(b'PK')},
    {'requires_valid_office_open_xml_container':True},not raw_bytes.startswith(b'PK'),
    'A signature alone would not certify XLSX validity either; no Office application or file launch performed.')
# 19: old total is unchanged if empty return precedes calculation.
old_total=100
new_rows=[]
shown=old_total if not new_rows else sum(new_rows)
illustration('P7-046','Empty result early-return leaves previous cards',
    {'old_total':old_total,'new_rows':new_rows},shown,0,shown==100,
    'Control-flow illustration only; no DataBinding or rendered WPF observation.')
# 20: live criteria and cached rows must not identify different snapshots.
illustration('P7-045','Cached rowsA labelled from current criteriaB',
    {'loaded_query':'A','current_controls':'B'}, {'row_snapshot':'A','caption_snapshot':'B'},
    {'row_snapshot':'A','caption_snapshot':'A'},True,
    'Does not assume any absent event handler outside the explicitly selected report paths.')
# 21: unlike the older costing UNION, expiry rows preserve the store key.
rows=[('item',1,'2027-01-01',5),('item',2,'2027-01-01',5)]
retained=len(set(rows))
projected_without_store=len(set((r[0],r[2],r[3]) for r in rows))
illustration('P4-009','Counterevidence: expiry UNION retains distinct store identity',rows,
    {'retained_with_store':retained,'if_projected_away':projected_without_store},
    {'expiry_distinct_store_rows':2},retained==2 and projected_without_store==1,
    'Counterevidence only, not a new extension to P4-009 or proof every UNION path is safe.')
# 22: calendar-boundary counts vs a complete elapsed duration are policy-specific.
a,b=datetime(2026,12,31),datetime(2027,1,1)
calendar={'year_boundaries':b.year-a.year,'month_boundaries':12*(b.year-a.year)+b.month-a.month,'days':(b-a).days}
illustration('H7B2-02','DATEDIFF labels require a boundary-versus-duration display contract',
    {'from':a.isoformat(),'to':b.isoformat()},calendar,{'elapsed_days':1,'complete_elapsed_years':0},
    calendar=={'year_boundaries':1,'month_boundaries':1,'days':1},
    'Not a numbered defect: independent DATEDIFF measures may be intended. No SQL executed.')

# Explicitly bounded lexical checks. No absence/callgraph scan over the repository.
a=bounded(F+'frmRptCostCenter.xaml.cs',198,234)
b=bounded(F+'frmRptCostCenter.xaml.cs',421,450)
textcheck('P7-052','Inverted ancestor predicate and leaf-only source filter',{'not_equal': 'if (parentVal != selectedVal)' in a,'assign_parent':'_parentCode = (int)parentVal' in a,'leaf_filter':'if (ccType == 2)' in b})
a=bounded(F+'frmRptCostCenter.xaml.cs',487,505)
textcheck('P7-053','Movement-led rows and first CC-only opening match',{'movement_loop':'foreach (DataRow row in dt4.Rows)' in a,'cc_match':'initRow["CCcode"].ToString() == row["CCcode"].ToString()' in a,'first_only':'break;' in a})
a=bounded(F+'frmRptInventory.xaml.cs',319,376)
textcheck('P7-054','Worker executes method that reads WPF controls',{'task_run':'await Task.Run(() => ShowInvoice());' in a,'control_read':'if (chkAllBranches.IsChecked != true' in a,'some_dispatcher_exists':'Dispatcher.Invoke(() => GridControl2.ItemsSource = null)' in a})
a=bounded(F+'frmRptInventory.xaml.cs',731,743)
b=bounded(C+'Report.cs',380,406)
c=bounded(C+'Report.cs',531,553)
textcheck('P7-055','Null actual argument and both non-null collection contracts',{'null_argument':'null, // GridView2' in a,'grid_deref':'GridView1.RowCount' in b,'table_deref':'dt.Rows' in c})
a=bounded(F+'frmRptItemsActivity.xaml.cs',232,252)
b=bounded(R,3054,3064)
textcheck('P7-056','Type7 in transfer variables, type8 in adjustment variables',{'trans_7':'transToVal = GetSumVal(itemDbId, 7, 1' in a,'adjust_8':'safeAdjVal = GetSumVal(itemDbId, 8, 1' in a,'seed_adjust':"VALUES (16, 7, 1, N'تسوية جردية مدخلة'" in b,'seed_transfer':"VALUES (18, 8, 1, N'مناقلة إلى'" in b})
a=bounded(F+'frmRptItemsActivity.xaml.cs',232,244)
params=[int(x) for x in re.findall(r'GetSumVal\(itemDbId, (\d+),',a)]
textcheck('P7-057','Complete selected thirteen-call enumeration omits type6',{'thirteen_calls':len(params)==13,'exact_order':params==[9,1,1,2,2,3,3,7,7,8,8,4,5],'none6_in_this_enumeration':6 not in params})
a=bounded(F+'frmRptItemsActivity.xaml.cs',200,205)
b=bounded(F+'frmRptItemsActivity.xaml.cs',922,943)
c=bounded(F+'frmRptItemsActivity.xaml',432,445)
textcheck('P7-058','Empty client predicate and earlier Items/ItemsSource barrier, not a second finding',{'empty_branch_comment':'هنا نتجاهله' in a,'items_source_assignment':'cmbClients.ItemsSource' in b,'nine_static_items':c.count('<ComboBoxItem>')==9})
a=bounded(F+'frmRptItemsActivityDetailed.xaml.cs',263,304)
textcheck('P7-059','Last-process TOP1 combines with ascending order',{'top1':'condTop = " top (1) "' in a,'ascending':'ORDER BY inv.date ASC' in a})
a=bounded(F+'frmRptItemsActivityDetailed.xaml.cs',324,335)
b=bounded(F+'frmProductionOrder.xaml.cs',1460,1475)
textcheck('P7-060','Only type7 switches to detail direction; component sub2',{'only7_condition':'invType == 7' in a,'header_else':'ProcType={procType}' in a,'component_out':'Value = 2;' in b})
a=bounded(F+'frmRptItemsActivityDetailed.xaml.cs',289,304)
b=bounded(F+'frmRptItemsActivityDetailed.xaml.cs',1034,1058)
c=bounded(F+'frmRptItemsActivityDetailed.xaml.cs',359,369)
textcheck('P7-061','Selected row SQL/localized route and display-language choice',{'local_id_selected':'Inv.id' in a,'arabic_case':'case "فاتورة مبيعات"' in b,'id_route':'id={invNo}' in b,'english_display':'["NameEn"]' in c})
a=bounded(F+'frmRptKhzna.xaml.cs',189,223)
b=bounded(F+'frmRptKhzna.xaml.cs',254,257)
textcheck('P7-062','Previous receives date string but period receives dt1',{'intraday_start':'dateFrom.Date + startTime' in a,'previous_date_string':'dateFrom.ToShortDateString()' in a,'period_dt1':'Value = dt1' in b})
a=bounded(F+'frmRptInventory.xaml.cs',657,667)
b=bounded(C+'InvoiceOper.cs',3725,3746)
textcheck('P7-063','Number header maps InvNote whose producer reads notes',{'number_header':'رقم الفاتورة' in a,'note_in_first_column':'$"{inv.InvNote},{inv.InvDate:d}' in a,'number_producer':'invoiceTxt.InvoiceNo' in b and '["id"]' in b,'note_producer':'invoiceTxt.InvNote' in b and '["notes"]' in b})
a=bounded(F+'frmRptEntries.xaml.cs',328,340)
textcheck('P7-064','ID cursor and date ordering literal pair',{'previous':'id<{_code} ORDER BY date DESC' in a,'next':'id>{_code} ORDER BY date ASC' in a})
a=bounded(F+'frmRptIncomeStatement.xaml.cs',220,236)
b=bounded(F+'frmRptIncomeStatement.xaml.cs',366,384)
c=bounded(F+'frmMezanyaArba7.xaml.cs',304,322)
d=bounded(R,48189,48209)
textcheck('P7-065','All-branch GL differs from current-branch stock parameter',{'gl_checkbox':'chkAllBranches.IsChecked != true' in a,'stock_current_branch':'int branch = MainClass.BranchNo' in b,'balance_fallback':'selectedBranch.HasValue ? selectedBranch.Value : MainClass.BranchNo' in c,'sp_equality':'inv.branch=@branch' in d})

assert len(ALG)==22 and len(ST)==14
print(json.dumps(dict(phase='7B2-partial-static-audit',audit_reference_date_utc='2026-11-16',
    method='Independent manually transcribed fixtures plus explicitly bounded literal-source observations; no ERP acceptance.',
    illustration_count=len(ALG),static_lexical_contract_check_count=len(ST),illustrations=ALG,
    static_lexical_contract_checks=ST,bounded_source_reads_not_semantic_coverage=READS,
    application_code_imported_or_executed=False,erp_runtime_tests_executed=0,sql_or_external_service_tests_executed=0,
    spreadsheet_or_formula_interpreter_executed=False,application_remediation_performed=False,
    real_business_or_secret_data_used=False,
    limit='Even all assertions true do not establish source semantics, branch policy, deployed schema, a successful build, application behavior or financial/operational/compliance acceptance.'),ensure_ascii=False,indent=2))
