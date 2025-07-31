import frappe
from pymongo import MongoClient

@frappe.whitelist()
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

@frappe.whitelist()
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

def convert_bson_types(doc):
    """
    Recursively convert BSON Decimal128 and other unsupported
    types into JSON serializable types.
    """
    if isinstance(doc, dict):
        return {k: convert_bson_types(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_bson_types(i) for i in doc]
    elif isinstance(doc, Decimal128):
        # Convert Decimal128 to float (or str if precision matters)
        dec = doc.to_decimal()
        return float(dec)  # or str(dec) if you want string
    elif isinstance(doc, Decimal):
        return float(doc)
    else:
        return doc



import json
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://localhost:27017/")
db = client["sample_airbnb"]
collection = db["listingsAndReviews"]

@frappe.whitelist()
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
        # Perform find_one instead of find
        doc = collection.find_one(filters)

        if not doc:
            return {"error": "No matching entity found."}

        # Convert ObjectId to string for JSON serialization
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
            doc = convert_bson_types(doc)



        return doc

    except PyMongoError as e:
        return {"error": f"Database error: {str(e)}"}

