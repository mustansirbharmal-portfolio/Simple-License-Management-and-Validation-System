from datetime import datetime

# License document structure for MongoDB
license_doc = {
    "key": "XYZ123ABC",
    "status": "active",  # Other values: revoked, expired
    "user": "client_name",
    "start_date": datetime.now(),
    "end_date": datetime.now(),  # License validity period
    "checksum": "some_generated_checksum"
}
