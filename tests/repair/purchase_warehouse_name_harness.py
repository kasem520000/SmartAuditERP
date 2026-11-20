#!/usr/bin/env python3
"""P7-087: local lookup contract witnessed in C# and modeled in SQLite.

This does not run SQL Server, WPF, the report, or its permission logic. The
P7B4T-21/22 acceptance scenarios are represented by synthetic model cases only.
"""
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[2]
source = (ROOT / 'SmartAuditERP/Form_WPF/frmRptInvPurchaseDetails.xaml.cs').read_text(encoding='utf-8-sig')
common = (ROOT / 'SmartAuditERP/Class/Common.cs').read_text(encoding='utf-8-sig')
load = (ROOT / 'SmartAuditERP/Class/LoadData.cs').read_text(encoding='utf-8-sig')
report = (ROOT / 'SmartAuditERP/Class/Report.cs').read_text(encoding='utf-8-sig')
schema = (ROOT / 'SmartAuditERP/Properties/Resources.resx').read_text(encoding='utf-8-sig')


def section(text, start, end):
    a = text.index(start)
    return text[a:text.index(end, a)]


def source_contract(text):
    method = section(text, 'private string BuildOptimizedSql(QueryParams p)',
                     'private InvoiceObj GetOrCreateInvoiceObj(')
    # The selected and joined fragments are extracted from actual C# literals,
    # not from comments or a second copy of the expected query.
    literals = re.findall(r'"([^"\n]*)"', method)
    sql = ''.join(literals)
    name = re.search(r'\bwarehouse\.name\s+as\s+StoreName\b', sql, re.I)
    join = re.search(r'\bleft\s+join\s+Safes\s+warehouse\s+on\s+inv\.safe\s*=\s*warehouse\.id\s+and\s+inv\.safe\s*>\s*0\b', sql, re.I)
    if not (name and join) or re.search(r'\bjoin\s+Stocks\b', sql, re.I):
        return None
    return name.group(), join.group()


count = 0

def check(name, value):
    global count
    count += 1
    if not value:
        raise AssertionError(name)
    print('PASS', name)


fragments = source_contract(source)
check('source selects the Safes warehouse name through a positive-id left join', fragments is not None)
lookup = section(common, 'public static string GetStoreName(int Id)', 'public static string GetSalesManName(')
check('legacy lookup uses positive ids and Safes', 'Id <= 0' in lookup and
      'Select Safes.name from Safes where id=@Id' in lookup)
check('inventory selector reads Safes', 'select id,name from Safes' in section(load,
      'public static DataTable Invertories(int EmpNo)', 'public static DataTable Customers(int Type)'))
check('schema identifies the two independent keyed tables', 'CONSTRAINT [PK_Safes]' in schema and
      'CONSTRAINT [PK_Stocks]' in schema and '[safe] [int] NULL' in schema)
check('override path still uses legacy lookup while optimized path reads StoreName',
      '? Common.GetStoreName(' in source and ': ("" + row["StoreName"])' in source)
check('the same Store identity and display field feed report and export',
      'Store = Convert.ToInt32("" + row["safe"])' in source and 'InvertoryName = storeName' in source and
      'dt.Columns.Add("InvertoryName", typeof(string));' in source and 'row.InvertoryName,' in source and
      'FieldName = "InvertoryName"' in report)
check('scope is limited to the documented repair', 'Repair R-101 (audit finding P7-087)' in source)

# The joined clause and selected expression are taken directly from the source
# witness and exercised against SQLite's equivalent LEFT JOIN semantics.
db = sqlite3.connect(':memory:')
db.executescript('''
CREATE TABLE Inv (id INTEGER PRIMARY KEY, safe INTEGER);
CREATE TABLE Safes (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE Stocks (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO Safes VALUES (0, 'zero should not resolve'), (3, 'مستودع أ'),
                         (4, 'مستودع ب'), (5, NULL);
INSERT INTO Stocks VALUES (3, 'خزينة مختلفة'), (9, 'خزينة بلا مستودع');
INSERT INTO Inv VALUES (1, 3), (2, 4), (3, 9), (4, 0), (5, -1), (6, NULL), (7, 5);
''')
select, join = fragments
query = 'SELECT inv.id, inv.safe, ' + select + ' FROM Inv inv ' + join + ' ORDER BY inv.id'
actual = db.execute(query).fetchall()
# C# string concatenation converts DBNull to the empty string.
def display(value):
    return '' if value is None else value


def legacy_lookup(value):
    if value is None or value <= 0:
        return ''
    row = db.execute('SELECT name FROM Safes WHERE id=?', (value,)).fetchone()
    return display(row[0]) if row else ''

check('same numeric id from different entities resolves to the warehouse', display(actual[0][2]) == 'مستودع أ')
check('missing treasury does not suppress a valid warehouse or invoice',
      actual[1] == (2, 4, 'مستودع ب'))
check('a treasury alone cannot invent a warehouse name', actual[2][:2] == (3, 9) and display(actual[2][2]) == '')
check('zero, negative, null and null name have no invented display name',
      all(display(row[2]) == '' for row in actual[3:]))
check('all input invoices survive the left join without changing their ids',
      [row[0] for row in actual] == list(range(1, 8)))
check('positive/missing/zero names match the legacy lookup on modeled rows',
      all(display(name) == legacy_lookup(safe) for _, safe, name in actual))
old = db.execute('SELECT Stocks.name FROM Inv inv LEFT JOIN Stocks ON inv.safe=Stocks.id WHERE inv.id=1').fetchone()[0]
check('legacy optimized join selects the wrong treasury on a colliding id', old == 'خزينة مختلفة')
for n, mutant in enumerate([
    source.replace('warehouse.name   as StoreName', 'Stocks.name as StoreName', 1),
    source.replace('left join Safes warehouse', 'left join Stocks warehouse', 1),
    source.replace('left join Safes warehouse', 'inner join Safes warehouse', 1),
    source.replace('inv.safe = warehouse.id and inv.safe > 0', 'inv.safe = warehouse.id', 1),
], 1):
    check('source witness rejects mutant %d' % n, source_contract(mutant) is None)
db.close()
print('RESULT: PASS - %d checks, SQLite model and source witnesses only.' % count)
