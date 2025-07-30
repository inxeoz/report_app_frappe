frappe.query_reports["Mongodb Room Prices"] = {
	after_datatable_render: function (report) {
		// Remove previous title if exists
		if (report.$custom_title) {
			report.$custom_title.remove();
		}

		// Only show the custom title
		report.$custom_title = $(
			`<div style="margin-top: 30px; font-size: 18px; font-weight: bold; text-align: center;">
				THIS IS DEMO TITLE
			</div>`
		).appendTo(report.page.wrapper);
	}
};
