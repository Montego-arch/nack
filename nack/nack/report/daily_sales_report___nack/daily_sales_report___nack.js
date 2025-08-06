// Copyright (c) 2025, Montego-arch and contributors
// For license information, please see license.txt

// frappe.query_reports["Daily Sales Report - NACK"] = {
// 	"filters": [

// 	]
// };


frappe.query_reports["Daily Sales Report - NACK"] = {
    "filters": [
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.month_start(),  // Start of current month
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),  // Today
            "reqd": 1
        },
        {
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center",
            "reqd": 1
        }
    ]
};
