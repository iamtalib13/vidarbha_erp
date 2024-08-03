# Copyright (c) 2024, Talib and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class GstInvoice(Document):
    def before_save(self):
        # Concatenate '0' to the beginning of self.name
        self.invoice_number = f"0{self.name}"
