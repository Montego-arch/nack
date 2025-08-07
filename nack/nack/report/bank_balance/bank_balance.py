# Copyright (c) 2025, Montego-arch and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import flt

def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = get_columns()
    data = get_data(from_date, to_date)

    return columns, data

def get_columns():
    return [
        {"label": "Account", "fieldname": "account", "fieldtype": "Link", "options": "Account", "width": 200},
        {"label": "Account Name", "fieldname": "account_name", "fieldtype": "Data", "width": 200},
        {"label": "Company", "fieldname": "company", "fieldtype": "Link", "options": "Company", "width": 150},
        {"label": "Currency", "fieldname": "account_currency", "fieldtype": "Link", "options": "Currency", "width": 100},
        {"label": "Balance", "fieldname": "balance", "fieldtype": "Currency", "width": 150}
    ]

def get_data(from_date, to_date):
    return frappe.db.sql("""
        SELECT
            acc.name AS account,
            acc.account_name,
            acc.company,
            acc.account_currency,
            SUM(gl.debit - gl.credit) AS balance
        FROM
            `tabAccount` acc
        LEFT JOIN
            `tabGL Entry` gl ON gl.account = acc.name
            AND gl.posting_date BETWEEN %(from_date)s AND %(to_date)s
        WHERE
            acc.account_type = 'Bank'
            AND acc.is_group = 0
            AND acc.disabled = 0
        GROUP BY
            acc.name, acc.account_name, acc.company, acc.account_currency
        ORDER BY
            acc.company, acc.name
    """, {
        "from_date": from_date,
        "to_date": to_date
    }, as_dict=True)

