import frappe
from pymongo import MongoClient

# http://localhost:8000/api/method/report_app_frappe.report_app_frappe.api.mongo_chart.demofunc

@frappe.whitelist(allow_guest=True)
def demofunc():
    return "HII data from demo function"

@frappe.whitelist(allow_guest=True)
def get_mongo_chart_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sample_airbnb"]
    collection = db["listingsAndReviews"]

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
        "datasets": [
            {
                "name": "Avg Price (USD)",
                "values": values
            }
        ]
    }

@frappe.whitelist(allow_guest=True)
def get_airbnb_listing_list():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sample_airbnb"]
    collection = db["listingsAndReviews"]

    cursor = collection.find(
        {"address.market": {"$exists": True}, "price": {"$exists": True}},
        {"name": 1, "price": 1, "address": 1}
    ).limit(20)

    results = []
    for doc in cursor:
        results.append({
            "name": doc.get("name", "Unnamed"),
            "price": str(doc.get("price", "N/A")),
            "address": doc.get("address", {}).get("market", "Unknown")
        })

    return results


from bson import Decimal128
from decimal import Decimal
from datetime import datetime

def convert_bson_types(doc):
    """
    Recursively convert BSON Decimal128, datetime, ObjectId, and other unsupported
    types into JSON serializable types.
    """
    if isinstance(doc, dict):
        return {k: convert_bson_types(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_bson_types(i) for i in doc]
    elif isinstance(doc, Decimal128):
        return float(doc.to_decimal())
    elif isinstance(doc, Decimal):
        return float(doc)
    elif isinstance(doc, datetime):
        return doc.isoformat()  # e.g., "2025-08-04T14:00:00"
    elif hasattr(doc, '__str__'):
        return str(doc)
    else:
        return doc



import json
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/")
db = client["sample_airbnb"]
collection = db["listingsAndReviews"]

@frappe.whitelist(allow_guest=True)
def search_entity(filters=None):
    if not filters:
        return {"error": "Filters must be provided"}

    # Parse JSON string if required
    if isinstance(filters, str):
        try:
            filters = json.loads(filters)
        except Exception:
            return {"error": "Invalid JSON in filters"}

    if not isinstance(filters, dict):
        return {"error": "Filters must be a dictionary"}

    # Convert _id string to ObjectId if present
    # if "_id" in filters:
    #     try:
    #         if not isinstance(filters["_id"], ObjectId):
    #             filters["_id"] = ObjectId(str(filters["_id"]))
    #     except Exception:
    #         return {"error": "Invalid _id format"}

    try:

        doc = collection.find_one(filters)

        if not doc:
            return {"error": "No matching entity found."}

        # Convert all types for safe JSON rendering
        doc = convert_bson_types(doc)
        return doc

    except PyMongoError as e:
        return {"error": f"Database error: {str(e)}"}


#http://localhost:8000/api/method/report_app_frappe.report_app_frappe.api.mongo_chart.secure_html


# report_app_frappe/api/mongo_chart.py
import base64, hmac, time
from hashlib import sha256
import frappe

@frappe.whitelist()
def secure_html():
    secret = frappe.conf.get("iframe_secret")
    user = frappe.session.user
    timestamp = int(time.time())
    data = f"{user}:{timestamp}"
    hmac_hash = hmac.new(secret.encode(), data.encode(), sha256).hexdigest()
    token = base64.b64encode(f"{user}:{timestamp}:{hmac_hash}".encode()).decode()

    iframe_url = f"https://my-next-app.com/viewer?token={token}"

    html = f"""
    <div style="padding: 2rem; font-family: sans-serif;">
        <h2>Embedded Secure Viewer</h2>
        <iframe
            src="{iframe_url}"
            width="100%"
            height="700"
            style="border: 1px solid #ccc; border-radius: 8px;"
        ></iframe>
    </div>
    """
    return {"message": html}

