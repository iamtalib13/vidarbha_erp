# Copyright (c) 2025, Talib Sheikh and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from decimal import Decimal, ROUND_HALF_UP

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


    def before_save(self):
        gst_rate = Decimal("0.18")

        for row in self.invoice_item:
            # Convert to Decimal for accuracy
            amt_with_gst = Decimal(str(row.amount_with_gst or 0))

            # Calculate amount without GST
            amt_without_gst = (amt_with_gst / (Decimal("1.00") + gst_rate)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # Calculate total GST
            gst = (amt_with_gst - amt_without_gst).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # Calculate CGST and SGST as half of GST
            half_gst = (gst / 2).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            # Assign values
            row.amount_without_gst = float(amt_without_gst)
            row.igst = float(gst)               # Full GST
            row.cgst = float(half_gst)
            row.sgst = float(half_gst)