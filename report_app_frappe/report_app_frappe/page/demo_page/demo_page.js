frappe.pages['demo-page'].on_page_load = function(wrapper) {
    const page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Airbnb Dashboard',
        single_column: true
    });

    page.set_indicator('Live Data', 'blue');

    // Create layout container
    const contentWrapper = $(`
        <div style="display: flex; flex-wrap: wrap; gap: 20px;">
            <div id="airbnb-chart" style="flex: 1 1 60%; height: 300px;">
                <p>Loading chart...</p>
            </div>
            <div style="flex: 1 1 35%;">
                <div style="max-height: 300px; overflow-y: auto; border: 1px solid #d1d8dd; padding: 15px; border-radius: 6px; background-color: #f9f9f9;">
                    <h4 style="margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">Available Listings</h4>
                    <ul id="airbnb-list" style="list-style: none; padding-left: 0; margin: 0;">
                        <li>Loading listings...</li>
                    </ul>
                </div>
            </div>
        </div>
    `).appendTo(page.body);

    // Refresh Button
    const refreshBtn = $('<button class="btn btn-sm btn-primary" style="margin-top: 20px;">Refresh Data</button>').appendTo(page.body);
    refreshBtn.on('click', function () {
        location.reload();
    });

    // Fetch chart data
    frappe.call({
        method: "report_app_frappe.report_app_frappe.api.mongo_chart.get_mongo_chart_data",
        callback: function(r) {
            if (r.message) {
                $("#airbnb-chart").empty();  // Clear loading text
                new frappe.Chart("#airbnb-chart", {
                    title: "Average Airbnb Prices by Suburb",
                    data: r.message,
                    type: 'bar',
                    height: 300,
                    colors: ['#5E64FF'],
                    barOptions: {
                        spaceRatio: 0.5
                    },
                    tooltipOptions: {
                        formatTooltipY: d => `$${d.toFixed(2)}`
                    }
                });
            }
        }
    });

    // Fetch listing data
    frappe.call({
        method: "report_app_frappe.report_app_frappe.api.mongo_chart.get_airbnb_listing_list",
        callback: function(r) {
            const list = r.message || [];
            const listContainer = $('#airbnb-list');
            listContainer.empty();

            if (list.length === 0) {
                listContainer.append("<li>No listings found.</li>");
            } else {
                list.forEach(item => {
                    listContainer.append(`
                        <li style="
                            margin-bottom: 12px;
                            padding: 10px;
                            border: 1px solid #e2e2e2;
                            border-radius: 5px;
                            background-color: #ffffff;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                            transition: box-shadow 0.2s ease;
                        " onmouseover="this.style.boxShadow='0 4px 10px rgba(0,0,0,0.1)'" onmouseout="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.05)'">
                            <strong style="font-size: 14px;">${item.name || "Unnamed"}</strong><br>
                            <span style="color: #6c757d;">${item.address || 'Unknown Location'}</span><br>
                            <span style="font-weight: 500;">Price: $${item.price || 'N/A'}</span>
                        </li>
                    `);
                });
            }
        }
    });
};
