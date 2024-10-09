from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import base64
import re

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.license_db

# Function to encode the license key
def encode_license_key(license_key):
    return base64.b64encode(license_key.encode()).decode()

# Function to decode the license key
def decode_license_key(encoded_key):
    return base64.b64decode(encoded_key.encode()).decode()

# Ensure license collection and add a default license for testing if not exists
def initialize_db():
    test_license_key = "XYZ123ABC"
    encoded_key = encode_license_key(test_license_key)
    license = db.licenses.find_one({"key": encoded_key})
    if not license:
        db.licenses.insert_one({
            "key": encoded_key,
            "status": "Active",
            "user": "client_name",
            "start_date": datetime.now(),
            "end_date": datetime(2030, 1, 1),
            "checksum": "some_generated_checksum"
        })

# Initialize database on app startup
initialize_db()

# Route to render the client page (HTML)
@app.route('/')
def client_page():
    return render_template('client.html')

# Route to render the admin page (HTML)
@app.route('/admin/revoke_license')
def admin_page():
    return render_template('admin.html')

# Route to get all licenses for admin view
@app.route('/admin/get_licenses', methods=['GET'])
def get_licenses():
    licenses = db.licenses.find()
    licenses_list = []
    for license in licenses:
        licenses_list.append({
            "key": decode_license_key(license["key"]),
            "status": license["status"],
            "start_date": license["start_date"],
            "end_date": license["end_date"]
        })
    return jsonify({"licenses": licenses_list})

# Helper function to check license status
def check_license_status(license):
    current_time = datetime.now()
    return license['status'] == 'Active' and license['end_date'] > current_time

# Route to validate or activate the license
@app.route('/validate_license', methods=['POST'])
def validate_license():
    data = request.get_json()
    license_key = data.get('key')

    # Validate that the license key is at least 8 alphanumeric characters
    if not re.match(r'^[a-zA-Z0-9]{8,}$', license_key):
        return jsonify({"message": "License key must be at least 8 alphanumeric characters."}), 400

    encoded_license_key = encode_license_key(license_key)

    # Find the license by encoded key in the database
    license = db.licenses.find_one({"key": encoded_license_key})

    if not license:
        # If license doesn't exist, create and activate it
        db.licenses.insert_one({
            "key": encoded_license_key,
            "status": "Active",
            "user": "client_name",
            "start_date": datetime.now(),
            "end_date": datetime(2030, 1, 1),
            "checksum": "some_generated_checksum"
        })
        return jsonify({"message": "License key activated successfully."})

    # Check if the license is valid
    if check_license_status(license):
        return jsonify({"message": "License is valid"})
    else:
        return jsonify({"message": "License is invalid or revoked"}), 400

# Admin route to revoke a license
@app.route('/admin/revoke_license', methods=['POST'])
def revoke_license():
    data = request.get_json()
    license_key = data.get('key')

    # Encode the incoming license key for secure comparison
    encoded_license_key = encode_license_key(license_key)

    # Find and revoke the license by setting its status to "revoked"
    result = db.licenses.update_one({"key": encoded_license_key}, {"$set": {"status": "Revoked"}})

    if result.modified_count > 0:
        return jsonify({"message": "License revoked successfully"}), 200
    else:
        return jsonify({"message": "License not found or already revoked"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5003)
