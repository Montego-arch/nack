# Copyright (c) 2025, Montego-arch and contributors
# For license information, please see license.txt

# import frappe


import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        _("Date") + ":Date:100",
        _("Customer") + ":Link/Customer:200",
        _("Invoice Number") + ":Link/Sales Invoice:150",
        _("Item Code") + "::120",
        _("Item Name") + "::200",
        _("Qty") + ":Float:80",
        _("Rate") + ":Currency:100",
        _("Total") + ":Currency:120",
        _("Mode of Payment") + "::150",
        _("Payment Amount") + ":Currency:120",
        _("Grand Total") + ":Currency:120",
    ]

def get_data(filters):
    # Fetch invoice + item details
    items = frappe.db.sql("""
        SELECT
            si.name AS invoice_number,
            si.posting_date,
            si.customer,
            sii.item_code,
            sii.item_name,
            sii.qty,
            sii.rate,
            sii.amount,
            si.grand_total
        FROM
            `tabSales Invoice` si
        JOIN
            `tabSales Invoice Item` sii ON si.name = sii.parent
        WHERE
            si.docstatus = 1
            AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND si.cost_center = %(cost_center)s
        ORDER BY
            si.name, sii.idx
    """, filters, as_dict=True)

    # Fetch payment details
    payments = frappe.db.sql("""
        SELECT
            parent AS invoice_number,
            mode_of_payment,
            amount
        FROM
            `tabSales Invoice Payment`
        ORDER BY
            parent
    """, as_dict=True)

    # Organize payments by invoice
    payments_map = {}
    for p in payments:
        payments_map.setdefault(p.invoice_number, []).append({
            "mode_of_payment": p.mode_of_payment,
            "amount": p.amount
        })

    data = []
    last_invoice = None

    for item in items:
        invoice = item.invoice_number

        if invoice != last_invoice:
            invoice_items = [i for i in items if i.invoice_number == invoice]
            invoice_payments = payments_map.get(invoice, [])

            max_rows = max(len(invoice_items), len(invoice_payments))
            
            for idx in range(max_rows):
                inv_item = invoice_items[idx] if idx < len(invoice_items) else None
                payment = invoice_payments[idx] if idx < len(invoice_payments) else None

                data.append([
                    inv_item.posting_date if idx == 0 else "" if inv_item else "",
                    inv_item.customer if idx == 0 else "" if inv_item else "",
                    invoice if idx == 0 else "" if inv_item else "",
                    inv_item.item_code if inv_item else "",
                    inv_item.item_name if inv_item else "",
                    inv_item.qty if inv_item else None,
                    inv_item.rate if inv_item else None,
                    inv_item.amount if inv_item else None,
                    payment["mode_of_payment"] if payment else "",
                    payment["amount"] if payment else None,
                    inv_item.grand_total if idx == 0 and inv_item else None
                ])
            last_invoice = invoice

    return data

