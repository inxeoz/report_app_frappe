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
