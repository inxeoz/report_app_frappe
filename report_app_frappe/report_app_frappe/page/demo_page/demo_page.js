// frappe.pages['demo-page'].on_page_load = function(wrapper) {
//     var page = frappe.ui.make_app_page({
//         parent: wrapper,
//         title: 'Hii How Are you',
//         single_column: true
//     });

//     page.set_indicator('Pending', 'orange');

//     // Create a container div for the chart
//     const chartContainer = $('<div id="demo-chart" style="height: 300px;"></div>').appendTo(page.body);

//     // Add a sample chart using frappe.Chart
//     const chart = new frappe.Chart("#demo-chart", {
//         title: "Demo Sales Chart",
//         data: {
//             labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
//             datasets: [
//                 {
//                     name: "Sales",
//                     values: [25, 40, 30, 35, 50, 49]
//                 }
//             ]
//         },
//         type: 'bar', // or 'line', 'percentage', 'pie', etc.
//         height: 250,
//         colors: ['#7cd6fd']
//     });
// };


// /home/inxeoz/report_bench/apps/report_app_frappe/report_app_frappe/report_app_frappe/api/mongo_api.py


frappe.pages['demo-page'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Airbnb Prices by Neighborhood',
        single_column: true
    });

    const chartContainer = $('<div id="airbnb-chart" style="height: 300px;"></div>').appendTo(page.body);

    frappe.call({
        method: "report_app_frappe.report_app_frappe.api.mongo_api.get_mongo_chart_data",
        callback: function(r) {
            if (r.message) {
                new frappe.Chart("#airbnb-chart", {
                    title: "Average Airbnb Prices",
                    data: r.message,
                    type: 'bar', // or 'line', 'pie'
                    height: 250,
                    colors: ['#ffa3ef']
                });
            } else {
                chartContainer.html("No data available.");
            }
        }
    });
};
