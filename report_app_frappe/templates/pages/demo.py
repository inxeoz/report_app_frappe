# import frappe

# def get_context(context):
#     print("🎯 demo.py loaded!")  # Will show in server logs

#     frappe.logger().info("🔧 demo.py running")
#     context.my_var = "Hello from backend!"
# http://localhost:8000/app/demo-page


# import frappe

# def get_context(context):
#     if frappe.session.user == "Guest":
#         frappe.redirect("/login")

#     context.user = frappe.session.user
#     context.report = [
#         {"date": "2025-08-01", "value": 130},
#         {"date": "2025-08-02", "value": 170},
#     ]
#     return context


# import frappe

# def get_context(context):
#     # If not logged in, redirect to login with redirect-to
#     if frappe.session.user == "Guest":
#         frappe.redirect(f"/login?redirect-to={frappe.request.path}")

#     # Now they're logged in, execution resumes here
#     context.user = frappe.session.user
#     context.report = [
#         {"date": "2025-08-01", "value": 130},
#         {"date": "2025-08-02", "value": 170},
#     ]
#     return context

# import frappe
# import json

# from report_app_frappe.report_app_frappe.api.mongo_chart import (
#     get_mongo_chart_data,
#     get_airbnb_listing_list,
#     search_entity
# )

# from report_app_frappe.report_app_frappe.api.token_utils import verify_token

# def get_context(context):

#     # token = frappe.form_dict.get("token")
#     # valid, result = verify_token(token)

#     # if not valid:
#     #     frappe.throw("Unauthorized: " + result)
#     #     return

#     if frappe.session.user == "Guest":
#         frappe.redirect(f"/login?redirect-to={frappe.request.path}")

#     context.user = frappe.session.user

#     # Chart Data
#     try:
#         chart_result = get_mongo_chart_data()
#         context.chart_data = chart_result if isinstance(chart_result, dict) else {}
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Chart Data Load Failed")
#         context.chart_data = {}

#     # Listings
#     try:
#         listing_result = get_airbnb_listing_list()
#         context.listings = listing_result if isinstance(listing_result, list) else []
#     except Exception as e:
#         frappe.log_error(frappe.get_traceback(), "Listing Load Failed")
#         context.listings = []

#     # Filter/Search
#     filters_json = frappe.form_dict.get("filters")
#     context.search_filter = filters_json
#     context.search_results = None
#     context.search_error = None

#     if filters_json:
#         try:
#             filters = json.loads(filters_json)
#             result = search_entity(filters=filters)
#             if isinstance(result, dict) and "error" in result:
#                 context.search_error = result["error"]
#             else:
#                 context.search_results = result  # result is a single dict
#         except Exception as e:
#             context.search_error = str(e)

#     return context


# report_app_frappe/templates/pages/demo.py

import frappe
import json
from report_app_frappe.report_app_frappe.api.mongo_demo import get_demo_context_data
from report_app_frappe.report_app_frappe.api.token_utils import verify_token

def get_context(context):
    token = frappe.form_dict.get("token")

    valid, result = verify_token(token)
    if not valid:
        frappe.throw("Unauthorized: " + result)

    if frappe.session.user == "Guest":
        frappe.redirect(f"/login?redirect-to={frappe.request.path}")

    filters_json = frappe.form_dict.get("filters")
    context.user = frappe.session.user
    context.update(get_demo_context_data(filters_json))
