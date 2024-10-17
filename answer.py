from flask import Blueprint, request, jsonify
from mongoengine import *
from datetime import datetime
from models import User, Question, Answer
# Create a Blueprint for profile
answer_bp = Blueprint('answer', __name__)


# Post an answer to a question
@answer_bp.route('/api/post_answer', methods=['POST'])
def post_answer():
    answer_data = request.json
    asker_user_id = answer_data.get('asker_user_id')
    answer_giver_user_id = answer_data.get('answer_giver_user_id')
    question_id = answer_data.get('question_id')
    answer_text = answer_data.get('answer')

    if not asker_user_id or not answer_giver_user_id or not question_id or not answer_text:
        return jsonify({"message": "asker_user_id, answer_giver_user_id, question_id, and answer are required."}), 400

    try:
        # Check if question exists
        question = Question.objects(id=question_id).first()
        if not question:
            return jsonify({"message": "Question not found."}), 404

        # Check if users exist
        asker_user = User.objects(id=asker_user_id).first()
        answer_giver_user = User.objects(id=answer_giver_user_id).first()

        if not asker_user or not answer_giver_user:
            return jsonify({"message": "User not found."}), 404

        # Create and save the answer
        answer = Answer(
            question_id=question,
            asker_user_id=asker_user,
            answer_giver_user_id=answer_giver_user,
            answer=answer_text
        )
        answer.save()

        return jsonify({
            "message": "Answer posted successfully!",
            "answer_id": str(answer.id),
            "question_id": str(question.id),
            "asker_user_id": str(asker_user.id),
            "answer_giver_user_id": str(answer_giver_user.id),
            "answer": answer_text
        }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Like an answer
@answer_bp.route('/api/like_answer/<answer_id>', methods=['POST'])
def like_answer(answer_id):
    try:
        # Find the answer by ID
        answer = Answer.objects(id=answer_id).first()
        if not answer:
            return jsonify({"message": "Answer not found."}), 404

        # Increment likes
        answer.likes += 1
        answer.save()

        return jsonify({"message": "Answer liked successfully!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Dislike an answer
@answer_bp.route('/api/dislike_answer/<answer_id>', methods=['POST'])
def dislike_answer(answer_id):
    try:
        # Find the answer by ID
        answer = Answer.objects(id=answer_id).first()
        if not answer:
            return jsonify({"message": "Answer not found."}), 404

        # Increment dislikes
        answer.dislikes += 1
        answer.save()

        return jsonify({"message": "Answer disliked successfully!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Report an answer
@answer_bp.route('/api/report_answer/<answer_id>', methods=['POST'])
def report_answer(answer_id):
    try:
        # Find the answer by ID
        answer = Answer.objects(id=answer_id).first()
        if not answer:
            return jsonify({"message": "Answer not found."}), 404

        # Increment reports
        answer.reports += 1
        answer.save()

        return jsonify({"message": "Answer reported successfully!"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# Delete an answer
@answer_bp.route('/api/delete_answer', methods=['DELETE'])
def delete_answer():
    answer_data = request.json
    answer_id = answer_data.get('answer_id')

    if not answer_id:
        return jsonify({"message": "Answer ID is required."}), 400

    try:
        # Find and delete the answer by ID
        answer = Answer.objects(id=answer_id).first()
        if not answer:
            return jsonify({"message": "Answer not found."}), 404

        answer.delete()
        return jsonify({"message": "Answer deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
