import json
import frappe
from frappe import _
from frappe.utils.response import json_handler

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import Decimal128
from decimal import Decimal
from datetime import datetime

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["sample_airbnb"]
collection = db["listingsAndReviews"]

# ------------------------- Utilities -------------------------

def convert_bson_types(doc):
    """Recursively convert MongoDB BSON types to JSON-serializable types."""
    if isinstance(doc, dict):
        return {k: convert_bson_types(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_bson_types(i) for i in doc]
    elif isinstance(doc, Decimal128):
        return float(doc.to_decimal())
    elif isinstance(doc, Decimal):
        return float(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()
    elif hasattr(doc, '__str__'):
        return str(doc)
    else:
        return doc

# ------------------------- API Functions -------------------------

@frappe.whitelist(allow_guest=True)
def demofunc():
    return "HII data from demo function"

@frappe.whitelist(allow_guest=True)
def get_mongo_chart_data():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$address.suburb",
                    "average_price": {"$avg": {"$toDouble": "$price"}}
                }
            },
            {"$sort": {"average_price": -1}},
            {"$limit": 6}
        ]
        result = list(collection.aggregate(pipeline))
        labels = [item['_id'] or 'Unknown' for item in result]
        values = [round(item['average_price'], 2) for item in result]

        return {
            "labels": labels,
            "datasets": [{
                "name": "Avg Price (USD)",
                "values": values
            }]
        }
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Chart Data Error")
        return {"error": "Failed to load chart data."}

@frappe.whitelist(allow_guest=True)
def get_airbnb_listing_list():
    try:
        cursor = collection.find(
            {"address.market": {"$exists": True}, "price": {"$exists": True}},
            {"name": 1, "price": 1, "address": 1}
        ).limit(20)

        return [
            {
                "name": doc.get("name", "Unnamed"),
                "price": str(doc.get("price", "N/A")),
                "address": doc.get("address", {}).get("market", "Unknown")
            }
            for doc in cursor
        ]
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Listing Load Error")
        return []

@frappe.whitelist(allow_guest=True)
def search_entity(filters=None):
    if not filters:
        return {"error": "Filters must be provided"}

    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            return {"error": "Invalid JSON in filters"}

    if not isinstance(filters, dict):
        return {"error": "Filters must be a dictionary"}

    try:
        doc = collection.find_one(filters)
        if not doc:
            return {"error": "No matching entity found."}
        return convert_bson_types(doc)
    except PyMongoError as e:
        return {"error": f"Database error: {str(e)}"}

# ------------------------- Demo Context Builder -------------------------

def get_demo_context_data(filters_json=None):
    data = {
        "chart_data": {},
        "listings": [],
        "search_filter": filters_json,
        "search_results": None,
        "search_error": None
    }

    try:
        data["chart_data"] = get_mongo_chart_data() or {}
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Chart Load Failed")

    try:
        data["listings"] = get_airbnb_listing_list() or []
    except Exception:
        frappe.log_error(frappe.get_traceback(), "Listings Load Failed")

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

# ------------------------- Demo APIs -------------------------

@frappe.whitelist()
def fetch_demo_page_data(filters=None):
    if frappe.session.user == "Guest":
        frappe.throw("Login required")

    data = get_demo_context_data(filters)
    data["user"] = frappe.session.user
    return data



@frappe.whitelist()
def render_demo_html(filters=None):
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to view this"))

    context = {
        "chart_data": {},
        "listings": [],
        "search_filter": "",
        "search_results": None,
        "search_error": None
    }

    try:
        context["chart_data"] = get_mongo_chart_data() or {}
    except Exception:
        frappe.log_error(title="Chart Data Load Error", message=frappe.get_traceback())

    try:
        context["listings"] = get_airbnb_listing_list() or []
    except Exception:
        frappe.log_error(title="Listing Load Error", message=frappe.get_traceback())

    if filters:
        context["search_filter"] = filters
        try:
            parsed = json.loads(filters)
            result = search_entity(filters=parsed)
            if isinstance(result, dict) and result.get("error"):
                context["search_error"] = result["error"]
            else:
                context["search_results"] = result
        except Exception as e:
            context["search_error"] = str(e)

    html = frappe.render_template("report_app_frappe/templates/pages/demo.html", context)
    return {"html": html}
