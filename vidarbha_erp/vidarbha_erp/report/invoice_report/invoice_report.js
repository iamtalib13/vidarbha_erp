frappe.query_reports["Invoice Report"] = {
	filters: [
		{
			fieldname: "status",
			label: "Status",
			fieldtype: "Select",
			options: [
				"", // empty option for 'All'
				"Uploaded",
				"Not-Uploaded",
			],
			default: "",
		},
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
	],

	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (column.fieldname === "status") {
			if (value === "Uploaded") {
				value = `<span style="color: green;">${value}</span>`;
			} else if (value === "Not-Uploaded") {
				value = `<span style="color: red;">${value}</span>`;
			}
		}

		return value;
	},
};
