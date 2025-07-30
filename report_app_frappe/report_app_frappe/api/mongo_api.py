# my_app/api/mongo_chart.py
import frappe
from pymongo import MongoClient

@frappe.whitelist()
def get_mongo_chart_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sample_airbnb"]
    collection = db["listingsAndReviews"]

    # Example: average price per neighborhood
    pipeline = [
        {
            "$group": {
                "_id": "$address.suburb",  # or use address.neighbourhood or address.country
                "average_price": {"$avg": {"$toDouble": "$price"}}
            }
        },
        {"$sort": {"average_price": -1}},
        {"$limit": 6}  # Show top 6 for clarity
    ]

    result = list(collection.aggregate(pipeline))

    # Format data for frappe.Chart
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
