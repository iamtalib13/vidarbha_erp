frappe.query_reports["Invoice Report"] = {
	filters: [
		{
			fieldname: "from_date",
			label: "From Date",
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: "To Date",
			fieldtype: "Date",
		},
		{
			fieldname: "invoice_type",
			label: "Type",
			fieldtype: "Select",
			options: ["", "GST", "DPDN"],
			default: "",
		},
		{
			fieldname: "status",
			label: "Status",
			fieldtype: "Select",
			options: ["", "Uploaded", "Not-Uploaded"],
			default: "",
		},
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		const status_colors = {
			Uploaded: "green",
			"Not-Uploaded": "red",
		};

		const invoice_type_colors = {
			GST: "#e74c3c",
			DPDN: "#2980b9",
		};

		const color_fields = [
			"invoice_type",
			"invoice_number",
			"invoice_date",
			"amount_with_gst",
			"amount_without_gst",
			"igst",
			"cgst",
			"sgst",
			"gst",
			"customer",
		];

		// Status color formatting
		if (column.fieldname === "status" && status_colors[value]) {
			return `<span style="color: ${status_colors[value]} !important; font-size: 10px;">${value}</span>`;
		}

		// Invoice Type color formatting
		if (column.fieldname === "invoice_type" && invoice_type_colors[value]) {
			return `<span style="color: ${invoice_type_colors[value]} !important; font-size: 10px;">${value}</span>`;
		}

		// Default color for other fields if needed
		const default_color = "#333";
		if (color_fields.includes(column.fieldname)) {
			return `<span style="color: ${default_color} !important; font-size: 10px;">${value}</span>`;
		}

		return value;
	},
};
