from flask import Flask, Blueprint, request, jsonify
from mongoengine import *
import requests
import uuid
from datetime import datetime
from models import User, Question

# Blueprint for questions
question_bp = Blueprint('questions', __name__)

# Function to get location name using OpenStreetMap (Nominatim) API
def get_location_name(latitude, longitude):
    url = f'https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json'
    headers = {
        'User-Agent': 'StakeCityApp/1.0 (your_email@example.com)'  # Replace with your app info
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        location_data = response.json()
        return location_data.get('display_name')  # Fetch the full location name
    else:
        return None

@question_bp.route('/api/pin_location_and_ask_question', methods=['POST'])
def pin_location_and_ask_question():
    question_data = request.json

    # Required fields
    user_name = question_data.get('user_name')  # Use user_name for user identification
    question = question_data.get('question')
    latitude = question_data.get('latitude')
    longitude = question_data.get('longitude')

    if not user_name or not question or not latitude or not longitude:
        return jsonify({"message": "user_name, question, latitude, and longitude are required."}), 400

    # Check if user exists in MongoDB using the custom user_name field
    user = User.objects(user_name=user_name).first()
    if not user:
        return jsonify({"message": "User ID not found."}), 404

    # Get location name from OpenStreetMap (Nominatim)
    location_name = get_location_name(latitude, longitude)
    if not location_name:
        return jsonify({"message": "Failed to retrieve location name from coordinates."}), 500

    # Create and save the new question
    new_question = Question(
        user_name=user,  # Assign the User object
        question=question,
        latitude=latitude,
        longitude=longitude,
        location_name=location_name,  # Include the location name
    )
    new_question.save()

    # Create navigation URL for the map
    navigation_url = f"https://www.google.com/maps?q={latitude},{longitude}"

    # Create shareable URL for viewing the question
    share_url = f"http://127.0.0.1:5000/api/view_question/{str(new_question.id)}"

    return jsonify({
        "message": "Question posted and location pinned successfully!",
        "user_name": user_name,  # Return the user_id as a string
        "question_id": str(new_question.id),
        "full_name": user.full_name,
        "location_name": location_name,
        "question": question,
        "navigation_url": navigation_url,  # Include the navigation URL in the response
        "share_url": share_url,  # Shareable URL for viewing the question
    }), 201

@question_bp.route('/api/view_question/<question_id>', methods=['GET'])
def view_question(question_id):
    # Attempt to find the question by ID
    question = Question.objects(id=question_id).first()

    if not question:
        return jsonify({"message": "Question not found."}), 404

    # Check if the user is registered
    is_registered = request.args.get('registered', 'false').lower() == 'true'

    if not is_registered:
        return jsonify({
            "message": "To view the full question, please register at http://localhost:8000/try.html."
        }), 403  # Forbidden

    # Return the question details if the user is registered
    return jsonify({
        "question_id": str(question.id),
        "user_name": str(question.user_name.user_id),  # Assuming user_name is a reference to User
        "question": question.question,
        "latitude": question.latitude,
        "longitude": question.longitude,
        "location_name": question.location_name,
        "created_at": question.created_at,
        # If you have an updated_at field, uncomment the line below
        # "updated_at": question.updated_at,
    }), 200

# Route to delete a question
@question_bp.route('/api/delete_question', methods=['DELETE'])
def delete_question():
    question_data = request.json
    question_id = question_data.get('question_id')

    if not question_id:
        return jsonify({"message": "Question ID is required."}), 400

    # Attempt to delete the question
    question = Question.objects(id=question_id).first()

    if not question:
        return jsonify({"message": "Question not found."}), 404

    question.delete()
    
    return jsonify({"message": "Question deleted successfully."}), 200
