import frappe

def execute(filters=None):
    filters = filters or {}

    columns = [
		{"label": "Invoice ID", "fieldname": "id", "fieldtype": "Link", "options": "Invoice","width": 120},
        {"label": "Invoice Number", "fieldname": "invoice_number", "fieldtype": "Data", "width": 120},
        {"label": "Invoice Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 100},
        {"label": "Invoice Type", "fieldname": "invoice_type", "fieldtype": "Data", "width": 100},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Amount Without GST", "fieldname": "amount_without_gst", "fieldtype": "Currency", "width": 120},
        {"label": "GST %", "fieldname": "gst", "fieldtype": "Data", "width": 80},
        {"label": "IGST", "fieldname": "igst", "fieldtype": "Currency", "width": 80},
        {"label": "CGST", "fieldname": "cgst", "fieldtype": "Currency", "width": 80},
        {"label": "SGST", "fieldname": "sgst", "fieldtype": "Currency", "width": 80},
        {"label": "Amount With GST", "fieldname": "amount_with_gst", "fieldtype": "Currency", "width": 120},
    ]

    # SQL Query to fetch data from Invoice and its child table Invoice Item
    data = frappe.db.sql("""
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
            inv.docstatus < 2
        ORDER BY
            inv.invoice_date DESC
    """, as_dict=True)

    return columns, data
