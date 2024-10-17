from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required, create_access_token
from pymongo import MongoClient
import secrets
from datetime import timedelta
# Flask app initialization
app = Flask(__name__)

# MongoDB Client Setup
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client["test"]
users_collection = db["users"]

@app.route('/reset-password', methods=['POST'])
# @jwt_required()  # Ensure that the user is logged in
def reset_password():
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({"message": "new passwords are required"}), 400

    # Get the logged-in user's email from the JWT token
    # email = get_jwt_identity()
    email = "johndoe@example.com"

    # Fetch the user from MongoDB
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Update the password in MongoDB
    users_collection.update_one({"email": email}, {"$set": {"password": new_password}})

    return jsonify({"message": "Password successfully updated"}), 200

# Main driver code
if __name__ == '__main__':
    app.run(debug=True)
