from flask import Blueprint, request, jsonify
from mongoengine import *
import uuid
from datetime import datetime

# Create a Blueprint for payment
payment_bp = Blueprint('payment', __name__)


# Pay for answers endpoint
@payment_bp.route('/pay_for_answers', methods=['POST'])
def pay_for_answers():
    data = request.json
    question_id = data.get('question_id')
    amount_to_distribute = data.get('amount')  # Total amount to distribute among answerers

    if not question_id or amount_to_distribute <= 0:
        return jsonify({'error': 'Invalid input!'}), 400

    # Fetch the question and answers
    question = Question.objects(id=question_id).first()
    if not question:
        return jsonify({'error': 'Question not found!'}), 404

    # Fetch answers and likes for the given question
    answers = Answer.objects(question_id=question).all()

    # Check if any answers were found
    if not answers:
        return jsonify({'error': 'No answers found for this question.'}), 404

    # Calculate total likes and payment distribution
    total_likes = sum(answer.likes for answer in answers)
    payments = []

    if total_likes > 0:
        for answer in answers:
            share = (answer.likes / total_likes) * amount_to_distribute
            payment_id = str(uuid.uuid4())
            transaction_id = str(uuid.uuid4())  # Replace with actual transaction ID from blockchain integration later

            # Create and save the payment
            payment = Payment(
                user_id=answer.answer_giver_user_id,
                question_id=question,
                answer_id=answer,
                likes=answer.likes,
                transaction_id=transaction_id,
                amount_paid=share
            )
            payment.save()

            # Add payment info to the response
            payments.append({
                'payment_id': str(payment.id),
                'user_id': str(answer.answer_giver_user_id.id),
                'question_id': str(question.id),
                'answer_id': str(answer.id),
                'likes': answer.likes,
                'transaction_id': transaction_id,
                'amount_paid': share
            })

    else:
        return jsonify({'error': 'No likes found for the answers.'}), 400

    return jsonify(payments), 201

# Delete a payment
@payment_bp.route('/api/delete_payment', methods=['DELETE'])
def delete_payment():
    payment_data = request.json
    payment_id = payment_data.get('payment_id')

    if not payment_id:
        return jsonify({"message": "Payment ID is required."}), 400

    try:
        # Find and delete the payment by ID
        payment = Payment.objects(id=payment_id).first()
        if not payment:
            return jsonify({"message": "Payment not found."}), 404

        payment.delete()
        return jsonify({"message": "Payment deleted successfully."}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
