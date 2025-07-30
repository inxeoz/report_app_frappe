frappe.pages['demo-page'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Hii How Are you',
        single_column: true
    });

    page.set_indicator('Pending', 'orange');

    // Create a container div for the chart
    const chartContainer = $('<div id="demo-chart" style="height: 300px;"></div>').appendTo(page.body);

    // Add a sample chart using frappe.Chart
    const chart = new frappe.Chart("#demo-chart", {
        title: "Demo Sales Chart",
        data: {
            labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            datasets: [
                {
                    name: "Sales",
                    values: [25, 40, 30, 35, 50, 49]
                }
            ]
        },
        type: 'bar', // or 'line', 'percentage', 'pie', etc.
        height: 250,
        colors: ['#7cd6fd']
    });
};
