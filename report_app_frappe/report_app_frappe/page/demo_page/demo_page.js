


// frappe.pages['demo-page'].on_page_load = function(wrapper) {
//     const user = frappe.session.user;
//     const secret = 'hardcoded-or-pulled-from-conf'; // ⚠️ Avoid hardcoding
//     const token = generateToken(user, secret);

//     const page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Secure Report',
//         single_column: true
//     });

//     const iframeHTML = `
//         <iframe
//             src="https://my-next-app.com/viewer?token=${token}"
//             width="100%"
//             height="700"
//             style="border: 1px solid #ccc; border-radius: 8px;"
//         ></iframe>
//     `;

//     $(page.body).html(iframeHTML);
// };





frappe.pages['demo-page'].on_page_load = async function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Secure Report',
		single_column: true,
	});

	const $container = $('<div id="demo-report-wrapper" style="padding: 2rem;"></div>');
	$container.appendTo(page.body);

	try {
		const res = await frappe.call({
			method: "report_app_frappe.report_app_frappe.api.demo_api.render_demo_html",
		});

		if (res.message.html) {
			$container.html(res.message.html);
		} else {
			$container.html(`<div class="text-muted">⚠ No content received from server.</div>`);
		}
	} catch (err) {
		console.error("Failed to load report:", err);
		frappe.msgprint("❌ Could not load report HTML.");
		$container.html(`<div class="text-danger">Error: ${err.message}</div>`);
	}
};