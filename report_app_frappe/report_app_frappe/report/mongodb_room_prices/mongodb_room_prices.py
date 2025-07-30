# Copyright (c) 2025, inxeoz and contributors
# For license information, please see license.txt

from frappe import _
from report_app_frappe.report_app_frappe.doctype.custom_report.custom_report import get_mongo_client


def execute(filters: dict | None = None):
	columns = get_columns()
	data = get_data()
	return columns, data


# def get_columns() -> list[dict]:
# 	return [
# 		{
# 			"label": _("Room Type"),
# 			"fieldname": "room_type",
# 			"fieldtype": "Data",
# 			"width": 200,
# 		},
# 		{
# 			"label": _("Price"),
# 			"fieldname": "price",
# 			"fieldtype": "Currency",
# 			"width": 120,
# 		},
# 	]


def get_columns() -> list[dict]:
	return [
		{
			"label": _("Room Type"),
			"fieldname": "room_type",
			"fieldtype": "Data",
			"width": 200,
		},
		{
			"label": _("Price"),
			"fieldname": "price",
			"fieldtype": "HTML",  # Use HTML if you include styled text
			"width": 120,
		},
	]

# def get_data() -> list[dict]:
# 	client = get_mongo_client()
# 	db = client["sample_airbnb"]
# 	col = db["listingsAndReviews"]

# 	results = col.find({}, {"room_type": 1, "price": 1}).limit(100)

# 	data = []
# 	for r in results:
# 		price = r.get("price")
# 		data.append({
# 			"room_type": r.get("room_type"),
# 			"price": float(price.to_decimal()) if price else 0
# 		})

# 	return data

def get_data() -> list[dict]:
	client = get_mongo_client()
	db = client["sample_airbnb"]
	col = db["listingsAndReviews"]

	results = list(col.find({}, {"room_type": 1, "price": 1}).limit(100))

	data = []
	total_price = 0
	count = 0

	for r in results:
		price = r.get("price")
		price_val = float(price.to_decimal()) if price else 0
		data.append({
			"room_type": r.get("room_type"),
			"price": price_val
		})
		total_price += price_val
		count += 1

	# Add a summary row as the first item (optional)
	average_price = round(total_price / count, 2) if count else 0
	data.insert(0, {
		"room_type": "<b style='color: green;'>Average</b>",
		"price": f"<b style='color: green;'>{average_price}</b>"
	})

	return data

