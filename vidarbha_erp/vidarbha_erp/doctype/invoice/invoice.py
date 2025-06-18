# Copyright (c) 2025, Talib Sheikh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


import frappe
from frappe.model.naming import make_autoname  # If you use frappe's naming series

class Invoice(Document):
	
	# add custom naming  as per requirment
    def autoname(self):
        # Correct field names
        if not self.invoice_type:  # <-- corrected from 'type' to 'invoice_type'
            frappe.throw("Invoice Type field is mandatory for naming.")
        
        if not self.invoice_date:
            frappe.throw("Invoice Date is required for naming.")

        # Extract DD, MM, YY from invoice_date
        from datetime import datetime
        invoice_date_obj = self.invoice_date
        if isinstance(invoice_date_obj, str):
            invoice_date_obj = datetime.strptime(invoice_date_obj, "%Y-%m-%d")
        dd = invoice_date_obj.strftime('%d')
        mm = invoice_date_obj.strftime('%m')
        yy = invoice_date_obj.strftime('%y')

        # Generate a unique invoice number using frappe's naming series
        series = f"{self.invoice_type}--{dd}-{mm}-{yy}-.####"
        # self.invoice_number = make_autoname(series)

        # Create the naming prefix
        prefix = f"{self.invoice_type}-{dd}-{mm}-{yy}-{self.invoice_number}"

        # Set the document name
        self.name = prefix


#  calculate gst and displaing in invoice
    def before_save(self):
        items = getattr(self, "invoice_item", [])
        gst_rate = 0.18

        total_amount = sum(float(row.amount_without_gst or 0) for row in items)
        total_gst = round(total_amount * gst_rate, 2)
        half_gst = round(total_gst / 2, 2)

        for row in items:
            amount = float(row.amount_without_gst or 0)
            gst = round(amount * gst_rate, 2)
            half = round(gst / 2, 2)
            row.igst = gst
            row.cgst = row.sgst = half
            row.amount_with_gst = round(amount + gst, 2)

        self.amount_without_gst = round(total_amount, 2)
        self.gst_amount = total_gst
        self.cgst = self.sgst = half_gst
        self.amount_with_gst = round(total_amount + total_gst, 2)



