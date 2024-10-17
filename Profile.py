from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from mongoengine import Document, StringField, DateTimeField, ReferenceField, connect
from datetime import datetime
from models import User, PasswordReset
# Create a Blueprint for profile
profile_bp = Blueprint('profile', __name__)


# Profile setup route: Update name, profile picture, and password
@profile_bp.route('/api/profile_setup', methods=['POST'])
def profile_setup():
    user_data = request.json
    user_id = user_data.get('user_name')
    profile_picture = user_data.get('profile_picture')
    new_password = user_data.get('new_password')
    old_password = user_data.get('old_password')

    if not user_id:
        return jsonify({"message": "User ID is required."}), 400

    # Fetch the user based on user_id
    user = User.objects(user_id=user_id).first()

    if not user:
        return jsonify({"message": "User not found."}), 404

    # Update profile picture if provided
    if profile_picture:
        user.profile_picture = profile_picture

    # Update password if old and new passwords are provided
    if new_password and old_password:
        # Check if the old password is correct
        if not check_password_hash(user.password, old_password):
            return jsonify({"message": "Old password is incorrect."}), 400

        if new_password == old_password:
            return jsonify({"message": "New password cannot be the same as the old password."}), 400

        # Hash the new password and update the user's password
        hashed_new_password = generate_password_hash(new_password)
        old_password_hashed = user.password  # store the old password

        # Update the user's password
        user.password = hashed_new_password
        user.save()

        # Record the password reset in the PasswordReset model
        PasswordReset(user=user, old_password=old_password_hashed, new_password=hashed_new_password).save()

        # Keep only the last 3 password resets
        password_resets = PasswordReset.objects(user=user).order_by('-reset_timestamp')
        if password_resets.count() > 3:
            # Remove older resets, keeping only the most recent 3
            password_resets.skip(3).delete()

    return jsonify({"message": "Profile updated successfully."}), 200
