// Copyright (c) 2025, Talib Sheikh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Invoice", {
	refresh(frm) {},
});

frappe.ui.form.on("Invoice Item", {
	amount_without_gst(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		let gst_rate = 0.18;

		let amount = parseFloat(row.amount_without_gst) || 0;
		let gst = flt(amount * gst_rate, 2);
		let half = flt(gst / 2, 2);

		row.igst = gst;
		row.cgst = row.sgst = half;
		row.amount_with_gst = flt(amount + gst, 2);

		frm.refresh_field("invoice_item");
	},

	amount_with_gst(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		let gst_rate = 0.18;

		let total = parseFloat(row.amount_with_gst) || 0;
		let base = flt(total / (1 + gst_rate), 2);
		let gst = flt(total - base, 2);
		let half = flt(gst / 2, 2);

		row.amount_without_gst = base;
		row.igst = gst;
		row.cgst = row.sgst = half;

		frm.refresh_field("invoice_item");
	},
});
