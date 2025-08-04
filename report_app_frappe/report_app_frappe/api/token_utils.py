import frappe
import hmac
import base64
import time
from hashlib import sha256

def verify_token(token: str, max_age_seconds=300):
    secret = frappe.conf.get("iframe_secret")
    if not secret:
        return False, "Missing secret"

    try:
        decoded = base64.b64decode(token).decode()
        user, timestamp_str, received_hmac = decoded.split(":")

        timestamp = int(timestamp_str)
        now = int(time.time())

        if abs(now - timestamp) > max_age_seconds:
            return False, "Token expired"

        data = f"{user}:{timestamp}"
        expected_hmac = hmac.new(
            secret.encode(), data.encode(), sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_hmac, received_hmac):
            return False, "Invalid signature"

        return True, user

    except Exception as e:
        return False, f"Invalid token: {str(e)}"


import time
import hmac
import base64
from hashlib import sha256

def generate_token(user: str, secret: str) -> str:
    timestamp = int(time.time())
    data = f"{user}:{timestamp}"
    hmac_digest = hmac.new(secret.encode(), data.encode(), sha256).hexdigest()
    token_str = f"{user}:{timestamp}:{hmac_digest}"
    token_b64 = base64.b64encode(token_str.encode()).decode()
    return token_b64
