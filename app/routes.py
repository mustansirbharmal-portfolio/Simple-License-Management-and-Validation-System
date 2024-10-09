# from flask import request, jsonify
# import json
# from .utils import check_license_status

# def initialize_routes(app, db):
#     @app.route('/validate_license', methods=['POST'])
#     def validate_license():
#         data = request.get_json()
#         license_key = data.get('key')

#         license = db.licenses.find_one({"key": license_key})

#         if not license:
#             return jsonify({"message": "License not found"}), 404

#         if check_license_status(license):
#             return jsonify({"message": "License is valid"})
#         else:
#             return jsonify({"message": "License is invalid or revoked"}), 400

#     @app.route('/admin/revoke_license', methods=['POST'])
#     def revoke_license():
#         data = request.get_json()
#         license_key = data.get('key')

#         result = db.licenses.update_one({"key": license_key}, {"$set": {"status": "revoked"}})

#         if result.modified_count:
#             return jsonify({"message": "License revoked successfully"})
#         else:
#             return jsonify({"message": "License not found or already revoked"}), 404
