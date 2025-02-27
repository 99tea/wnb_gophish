import logging
import csv
import os
import time
import hmac
import hashlib
from flask import Flask, request, jsonify

# Mailgun Signing Key (Used for verifying webhook authenticity)
MAILGUN_SIGNING_KEY = "57e1b9bb6bbb81dff74577cb550d35f2"

# Base directory for storing CSV files
CSV_DIR = "csv"
DEBUG_LOG_FILENAME = "debug_log.txt"

# Ensure the CSV directory exists
os.makedirs(CSV_DIR, exist_ok=True)

# Configure logging for errors only
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.ERROR,
    handlers=[
        logging.FileHandler(DEBUG_LOG_FILENAME),
        logging.StreamHandler()
    ]
)

# Flask App
app = Flask(__name__)

# Disable Flask's built-in logging
logging.getLogger('werkzeug').setLevel(logging.ERROR)

def verify_webhook_signature(timestamp, token, signature):
    """
    Verifies the Mailgun webhook signature for authenticity.
    """
    try:
        data = f"{timestamp}{token}".encode('utf-8')
        computed_signature = hmac.new(
            MAILGUN_SIGNING_KEY.encode('utf-8'),
            data,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(computed_signature, signature)
    except Exception as e:
        logging.error(f"Signature verification failed: {e}")
        return False

def get_csv_file(campaign_name):
    """
    Ensures a CSV file exists for the campaign name.
    Uses 'unknown_campaign' if no valid tag is found.
    """
    # Handle empty campaign names
    sanitized_name = "unknown_campaign" if not campaign_name else campaign_name
    
    # Sanitize remaining characters
    valid_chars = "-_.() %s%s" % (os.path.sep, '')
    sanitized_name = ''.join(
        c if c.isalnum() or c in valid_chars else '_' 
        for c in sanitized_name
    )
    
    csv_filename = os.path.join(CSV_DIR, f"log_{sanitized_name}.csv")

    if not os.path.exists(csv_filename):
        with open(csv_filename, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                "Timestamp", "Event", "Recipient", "Campaign", "Message ID",
                "Sender", "Sender IP", "Recipient IP", "Clicked URL", "Failure Reason", "User Agent"
            ])

    return csv_filename

@app.route("/mailgun/webhook", methods=["POST"])
def mailgun_webhook():
    """Handles Mailgun webhook events with campaign-based CSV file grouping."""
    try:
        data = request.json
        signature_data = data.get("signature", {})
        event_data = data.get("event-data", {})

        # Verify signature
        timestamp = signature_data.get("timestamp")
        token = signature_data.get("token")
        signature = signature_data.get("signature")
        if not (timestamp and token and signature and verify_webhook_signature(timestamp, token, signature)):
            logging.error("Invalid webhook signature")
            return jsonify({"error": "Invalid signature"}), 403

        # Check timestamp freshness
        if abs(time.time() - int(timestamp)) > 300:
            logging.error("Webhook timestamp out of range")
            return jsonify({"error": "Timestamp out of range"}), 403

        # Extract event data
        message_id = event_data.get("message", {}).get("headers", {}).get("message-id", "unknown")
        tags = event_data.get("tags", [])
        campaign_name = tags[0] if tags else "unknown_campaign"

        # Prepare CSV data
        csv_file_path = get_csv_file(campaign_name)
        event_row = [
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(timestamp))),
            event_data.get("event", "unknown"),
            event_data.get("recipient", "unknown"),
            campaign_name,
            message_id,
            event_data.get("envelope", {}).get("sender", "unknown"),
            event_data.get("envelope", {}).get("sending-ip", "unknown"),
            event_data.get("ip", "unknown"),
            event_data.get("url", "") if event_data.get("event") == "clicked" else "",
            event_data.get("delivery-status", {}).get("description", "") if event_data.get("event") in ["failed", "permanent failure"] else "",
            event_data.get("client-info", {}).get("user-agent", "unknown")
        ]

        # Write to CSV
        with open(csv_file_path, "a", newline="") as csv_file:
            csv.writer(csv_file).writerow(event_row)

        return jsonify({"status": "received"}), 200

    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
