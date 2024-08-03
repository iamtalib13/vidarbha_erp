frappe.ui.form.on("Gst Invoice", {
  refresh: function (frm) {
    frm.trigger("set_from_details");
    frm.trigger("invoice_print");
  },

  set_from_details: function (frm) {
    if (frm.is_new()) {
      frappe.db
        .get_value("Company Details", "Company Details", [
          "company_name",
          "address",
          "gst_number",
        ])
        .then((r) => {
          let company_details = r.message;
          if (company_details) {
            frm.set_value("from", company_details.company_name);
            frm.set_value("from_address", company_details.address);
            frm.set_value("from_gst", company_details.gst_number);
            frm.refresh_field("from");
            frm.refresh_field("from_address");
            frm.refresh_field("from_gst");
          }
        });
    }
  },

  invoice_print: function (frm) {
    if (!frm.is_new()) {
      frm.add_custom_button(__("Invoice PDF"), function () {
        var printUrl = frappe.urllib.get_full_url(
          "/api/method/frappe.utils.weasyprint.download_pdf?" +
            "doctype=" +
            encodeURIComponent("Gst Invoice") +
            "&name=" +
            encodeURIComponent(frm.doc.name) +
            "&print_format=GST Invoice"
        );

        window.open(
          printUrl,
          "_blank",
          "toolbar=no,location=no,directories=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600"
        );

        console.log(printUrl);
      });
    }
  },

  before_save: function (frm) {
    calculate_total(frm);
  },
});

frappe.ui.form.on("Invoice Item", {
  rate: function (frm, cdt, cdn) {
    calculate_amount(frm, cdt, cdn);
  },
  qty: function (frm, cdt, cdn) {
    calculate_amount(frm, cdt, cdn);
  },
  invoice_items_add: function (frm, cdt, cdn) {
    calculate_amount(frm, cdt, cdn);
  },
});

function calculate_amount(frm, cdt, cdn) {
  let child = locals[cdt][cdn];

  if (child.rate) {
    // If qty is provided, multiply it by the rate. If not, use the rate as the amount.
    child.amount = child.qty ? child.rate * child.qty : child.rate;

    // Optional: Log the amount to the console for debugging
    console.log(
      `Item: ${child.item_name}, Rate: ${child.rate}, Qty: ${
        child.qty || 1
      }, Amount: ${child.amount}`
    );

    // Update the fields in the child table
    frappe.model.set_value(cdt, cdn, "amount", child.amount);

    // Refresh the child table field
    frm.refresh_field("invoice_items");
  }

  // Update the total fields in the parent doctype
  calculate_total(frm);
}

function calculate_total(frm) {
  let total_amount = 0;

  // Sum up the amounts for all items in the child table
  frm.doc.invoice_items.forEach(function (item) {
    total_amount += item.amount || 0;
  });

  // Round the total amount to 2 decimal places
  total_amount = parseFloat(total_amount.toFixed(2));

  // Calculate CGST, SGST, and IGST based on the total amount
  let cgst = (total_amount * 9) / 100;
  let sgst = (total_amount * 9) / 100;
  let igst = (total_amount * 18) / 100;

  // Round the tax values to 2 decimal places
  cgst = parseFloat(cgst.toFixed(2));
  sgst = parseFloat(sgst.toFixed(2));
  igst = parseFloat(igst.toFixed(2));

  // Calculate the invoice total including IGST
  let invoice_total = total_amount + igst;

  // Set the total values in the parent doctype
  frm.set_value("total_amount", total_amount);
  frm.set_value("cgst", cgst);
  frm.set_value("sgst", sgst);
  frm.set_value("igst", igst);
  frm.set_value("invoice_total", invoice_total);

  // Refresh the parent doctype fields
  frm.refresh_fields(["total_amount", "cgst", "sgst", "igst", "invoice_total"]);
}
