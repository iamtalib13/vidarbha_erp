// Copyright (c) 2025, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Transaction", {

	 transaction_type(frm) {
        frm.set_query('category', function() {
            return {
                filters: {
                    'transaction_type': frm.doc.transaction_type
                }
            };
        });
    }
});