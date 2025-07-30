import frappe
from pymongo import MongoClient

@frappe.whitelist()
def get_room_type_distribution():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sample_airbnb"]
    collection = db["listingsAndReviews"]

    pipeline = [
        {"$group": {"_id": "$room_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]

    data = list(collection.aggregate(pipeline))
    
    # Format to: [{"room_type": "Entire home/apt", "count": 456}, ...]
    return [{"room_type": item["_id"], "count": item["count"]} for item in data]
