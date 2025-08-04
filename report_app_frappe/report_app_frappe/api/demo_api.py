# file: report_app_frappe/api/demo_api.py

import frappe
from report_app_frappe.report_app_frappe.api.demo_data import get_demo_context_data

@frappe.whitelist()
def fetch_demo_page_data(filters=None):
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    data = get_demo_context_data(filters)
    data["user"] = frappe.session.user
    return data


# file: report_app_frappe/report_app_frappe/api/demo_api.py

import frappe
from frappe import _
from frappe.utils.response import json_handler
import json

from report_app_frappe.report_app_frappe.api.mongo_chart import (
    get_mongo_chart_data,
    get_airbnb_listing_list,
    search_entity
)

@frappe.whitelist()
def render_demo_html():
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to view this"))

    context = {
        "chart_data": {},
        "listings": [],
        "search_filter": "",
        "search_results": None,
        "search_error": None
    }

    # Load data
    try:
        context["chart_data"] = get_mongo_chart_data() or {}
    except Exception as e:
        frappe.log_error(title="Chart Data Load Error", message=frappe.get_traceback())

    try:
        context["listings"] = get_airbnb_listing_list() or []
    except Exception as e:
        frappe.log_error(title="Listing Load Error", message=frappe.get_traceback())

    filters_json = frappe.form_dict.get("filters")
    context["search_filter"] = filters_json

    if filters_json:
        try:
            filters = json.loads(filters_json)
            result = search_entity(filters=filters)
            if isinstance(result, dict) and result.get("error"):
                context["search_error"] = result["error"]
            else:
                context["search_results"] = result
        except Exception as e:
            context["search_error"] = str(e)

    # Render the template into HTML
    html = frappe.render_template("report_app_frappe/templates/pages/demo.html", context)
    return {"html": html}
