# report_app_frappe/api/demo_data.py

import json
import frappe

from report_app_frappe.report_app_frappe.api.mongo_chart import (
    get_mongo_chart_data,
    get_airbnb_listing_list,
    search_entity
)

def get_demo_context_data(filters_json=None):
    data = {}

    # Chart
    try:
        chart_result = get_mongo_chart_data()
        data["chart_data"] = chart_result if isinstance(chart_result, dict) else {}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Chart Load Failed")
        data["chart_data"] = {}

    # Listings
    try:
        listings = get_airbnb_listing_list()
        data["listings"] = listings if isinstance(listings, list) else []
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Listings Load Failed")
        data["listings"] = []

    # Filters
    data["search_filter"] = filters_json
    data["search_results"] = None
    data["search_error"] = None

    if filters_json:
        try:
            filters = json.loads(filters_json)
            result = search_entity(filters=filters)
            if isinstance(result, dict) and "error" in result:
                data["search_error"] = result["error"]
            else:
                data["search_results"] = result
        except Exception as e:
            data["search_error"] = str(e)

    return data
