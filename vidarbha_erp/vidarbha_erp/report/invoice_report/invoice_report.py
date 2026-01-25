import frappe
from collections import defaultdict
from frappe.utils import flt, getdate

def execute(filters=None):
    filters = filters or {}

    # Build WHERE conditions
    conditions = ""
    if filters.get("invoice_type"):
        conditions += " AND inv.invoice_type = %(invoice_type)s"
    if filters.get("status"):
        conditions += " AND inv.status = %(status)s"
    if filters.get("from_date"):
        conditions += " AND inv.invoice_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND inv.invoice_date <= %(to_date)s"

    # Report Columns
    columns = [
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Type", "fieldname": "invoice_type", "fieldtype": "Data", "width": 60},
        {"label": "Invoice No", "fieldname": "invoice_number", "fieldtype": "Data", "width": 60},
        {"label": "Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 110},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Data", "width": 100},
        {"label": "Amount Without GST", "fieldname": "amount_without_gst", "fieldtype": "Currency", "width": 120},
        {"label": "GST %", "fieldname": "gst", "fieldtype": "Data", "width": 80},
        {"label": "IGST", "fieldname": "igst", "fieldtype": "Currency", "width": 120},
        {"label": "CGST", "fieldname": "cgst", "fieldtype": "Currency", "width": 120},
        {"label": "SGST", "fieldname": "sgst", "fieldtype": "Currency", "width": 120},
        {"label": "Amount With GST", "fieldname": "amount_with_gst", "fieldtype": "Currency", "width": 120},
    ]

    # SQL Query
    query = f"""
        SELECT
            inv.name AS id,
            inv.invoice_number,
            inv.invoice_date,
            inv.invoice_type,
            inv.customer,
            inv.status,
            item.amount_without_gst,
            item.gst,
            item.igst,
            item.cgst,
            item.sgst,
            item.amount_with_gst
        FROM
            `tabInvoice` AS inv
        INNER JOIN
            `tabInvoice Item` AS item
        ON
            inv.name = item.parent
        WHERE
            inv.docstatus < 2 {conditions}
        ORDER BY
            inv.invoice_date DESC
    """

    data = frappe.db.sql(query, filters, as_dict=True)

    # Chart Data Preparation (Monthly + Type-wise)
    monthly_data = defaultdict(lambda: {"GST": 0, "DPDN": 0})

    for row in data:
        if not row.get("invoice_date"):
            continue

        month = row["invoice_date"].strftime("%b %Y")  # e.g. 'Jul 2025'
        invoice_type = row["invoice_type"] or "Unknown"
        monthly_data[month][invoice_type] += flt(row.get("amount_with_gst", 0), 2)

    # Chart Labels Sorted Chronologically
    labels = sorted(monthly_data.keys(), key=lambda m: getdate("01 " + m))

    # Datasets with 2-decimal precision
    dataset_gst = [flt(monthly_data[month].get("GST", 0), 2) for month in labels]
    dataset_dpdn = [flt(monthly_data[month].get("DPDN", 0), 2) for month in labels]

    # Final Chart Dict
    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "GST", "values": dataset_gst},    # Bottom bar
                {"name": "DPDN", "values": dataset_dpdn}   # Stacked on top
            ]
        },
        "type": "bar",
        "barOptions": {
            "stacked": True,
            "horizontal": True
        },
        "colors": ["#e74c3c", "#2980b9"]  # Red for GST, Blue for DPDN
    }

    return columns, data, None, chart
