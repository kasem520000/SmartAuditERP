#!/usr/bin/env python3
"""
Repair R-007 verification harness (audit finding P7-063).

Models the CSV row projection in
SmartAuditERP/Form_WPF/frmRptInventory.xaml.cs::btnExportExcel_Click.

Defect: the header's FIRST column is "رقم الفاتورة" (invoice number) but each data
row wrote inv.InvNote (the notes) in that position -- so notes appeared where the
invoice number belongs.

Fix: write inv.InvoiceNo (the populated source-of-truth number, == Inv.id) in the
first column. The other columns are unchanged.

Scope/limits (Rule 9): verifies the column-mapping logic only (verified-in-scope);
WPF/.NET cannot run here. Field values mimic the C# format (date 'd', numbers N2).

Usage: python3 tests/repair/inventory_export_harness.py
Exit 0 on success, 1 otherwise.
"""
import sys


class Inv:
    def __init__(self, no, date, customer, user, branch, sump, disc, total, vat, net, note):
        self.InvoiceNo = no
        self.InvDate = date
        self.Customer = customer
        self.User = user
        self.Branch = branch
        self.SumPrice = sump
        self.TotDiscount = disc
        self.Total = total
        self.VAT = vat
        self.Net = net
        self.InvNote = note


HEADER = ("رقم الفاتورة,التاريخ,العميل/المورد,المستخدم,الفرع,"
          "المجموع,الخصم,الإجمالي,الضريبة,الصافي")


def n2(x):
    # Plain two-decimal formatting WITHOUT thousands separators. (Real C# {x:N2}
    # may emit group separators that themselves break naive CSV -- that distinct
    # concern is audit finding P7-048, deliberately out of scope for this harness,
    # whose only subject is which field lands in the first 'invoice number' column.)
    return f"{x:.2f}"


def row_original(inv):
    # First field uses InvNote (the bug).
    return (f"{inv.InvNote},{inv.InvDate},{inv.Customer},"
            f"{inv.User},{inv.Branch},"
            f"{n2(inv.SumPrice)},{n2(inv.TotDiscount)},"
            f"{n2(inv.Total)},{n2(inv.VAT)},{n2(inv.Net)}")


def row_fixed(inv):
    # First field uses InvoiceNo (the repair).
    return (f"{inv.InvoiceNo},{inv.InvDate},{inv.Customer},"
            f"{inv.User},{inv.Branch},"
            f"{n2(inv.SumPrice)},{n2(inv.TotDiscount)},"
            f"{n2(inv.Total)},{n2(inv.VAT)},{n2(inv.Net)}")


def csv_parse(line):
    """Simple split adequate for these single-token-per-column sample values."""
    return line.split(",")


def main():
    ok = True
    headers = csv_parse(HEADER)
    first_header = headers[0]                 # "رقم الفاتورة"

    samples = [
        Inv(1042, "01/05/2026", "شركة النور", "ahmed", "1",
            1000.0, 50.0, 950.0, 142.5, 1092.5, "دفعة أولى"),
        Inv(1043, "02/05/2026", "مؤسسة البحر", "sara", "2",
            250.0, 0.0, 250.0, 37.5, 287.5, ""),
    ]

    print("header columns:", headers)
    print()
    for inv in samples:
        orig_cols = csv_parse(row_original(inv))
        fixed_cols = csv_parse(row_fixed(inv))
        print(f"invoice {inv.InvoiceNo} (note={inv.InvNote!r})")
        print("   original first cell:", repr(orig_cols[0]))
        print("   fixed    first cell:", repr(fixed_cols[0]))

        # Column count must equal header count in both.
        if len(orig_cols) != len(headers) or len(fixed_cols) != len(headers):
            print("   ! column/header arity mismatch"); ok = False

        # Original demonstrably wrong: first cell carries the NOTE, not the number.
        if orig_cols[0] != str(inv.InvNote):
            print("   ! expected original to expose the NOTE in the number column"); ok = False
        if orig_cols[0] == str(inv.InvoiceNo):
            print("   ! original unexpectedly already correct"); ok = False

        # Fixed correct: first cell equals the invoice number under the number header.
        if fixed_cols[0] != str(inv.InvoiceNo):
            print("   ! fixed first cell must be the invoice number"); ok = False

        # Remaining columns identical between original and fixed (no collateral change).
        if orig_cols[1:] != fixed_cols[1:]:
            print("   ! non-first columns changed unexpectedly"); ok = False
        print()

    # Spot-check the second column really is the date and third the customer.
    cols = csv_parse(row_fixed(samples[0]))
    if cols[1] != samples[0].InvDate or cols[2] != samples[0].Customer:
        print("! downstream column alignment broken"); ok = False
    else:
        print("downstream alignment (date, customer, ...) preserved -> OK")

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
