import frappe

def execute(filters=None):
    filters = filters or {}

    conditions = ""
    if filters.get("status"):
        conditions += " AND inv.status = %(status)s"
    if filters.get("from_date"):
        conditions += " AND inv.invoice_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " AND inv.invoice_date <= %(to_date)s"

    columns = [
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 100},
        {"label": "Type", "fieldname": "invoice_type", "fieldtype": "Data", "width": 80},
        {"label": "Invoice No", "fieldname": "invoice_number", "fieldtype": "Data", "width": 100},
        {"label": "Date", "fieldname": "invoice_date", "fieldtype": "Date", "width": 110},
        {"label": "Customer", "fieldname": "customer", "fieldtype": "Link", "options": "Customer", "width": 150},
        {"label": "Amount Without GST", "fieldname": "amount_without_gst", "fieldtype": "Currency", "width": 120},
        {"label": "GST %", "fieldname": "gst", "fieldtype": "Data", "width": 100},
        {"label": "IGST", "fieldname": "igst", "fieldtype": "Currency", "width": 100},
        {"label": "CGST", "fieldname": "cgst", "fieldtype": "Currency", "width": 100},
        {"label": "SGST", "fieldname": "sgst", "fieldtype": "Currency", "width": 100},
        {"label": "Amount With GST", "fieldname": "amount_with_gst", "fieldtype": "Currency", "width": 120},
    ]

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


    return columns, data
