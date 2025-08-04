import frappe

def get_context(context):
    print("🎯 demo.py loaded!")  # Will show in server logs

    frappe.logger().info("🔧 demo.py running")
    context.my_var = "Hello from backend!"
