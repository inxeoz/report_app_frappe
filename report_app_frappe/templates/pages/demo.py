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


import frappe

def get_context(context):
    # If not logged in, redirect to login with redirect-to
    if frappe.session.user == "Guest":
        frappe.redirect(f"/login?redirect-to={frappe.request.path}")

    # Now they're logged in, execution resumes here
    context.user = frappe.session.user
    context.report = [
        {"date": "2025-08-01", "value": 130},
        {"date": "2025-08-02", "value": 170},
    ]
    return context
