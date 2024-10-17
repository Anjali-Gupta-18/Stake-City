from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import User  # Import the User model from models.py

# Create a Blueprint
register_bp = Blueprint('register', __name__)

# Password validation function
def validate_password(password):
    min_length = 8
    has_uppercase = re.search(r'[A-Z]', password)
    has_lowercase = re.search(r'[a-z]', password)
    has_number = re.search(r'[0-9]', password)
    has_special = re.search(r'[!@#$%^&*]', password)

    return (len(password) >= min_length and
            has_uppercase and
            has_lowercase and
            has_number and
            has_special)

def login_app_email():
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "testingben12@gmail.com"
    sender_pwd = "qxxa yqbu boeq dojd"
    user_data = request.json
    user_name = user_data.get('user_name')
    subject = 'Email Verification'
    verification_link = f"http://localhost:5000/api/verify_email/{user_name}"
    # body = f'Please click on this link to verify {verification_link}'
    body = f'''
        <html>
            <body>
                <p>Please click on the verification link: 
                <a href="{verification_link}">Click Here</a></p>
            </body>
        </html>
        '''
    return smtp_server,port, sender_email,sender_pwd,subject,body

# Register route
@register_bp.route('/api/register', methods=['POST'])
def register():
    user_data = request.json
    user_name = user_data.get('user_name')
    mobile = user_data.get('mobile')
    email = user_data.get('email')
    password = user_data.get('password')
    full_name = user_data.get('full_name')
    age = user_data.get('age')
    gender = user_data.get('gender')
    terms_accepted = user_data.get('terms_accepted', False)

    if not all([user_name, mobile, email, password, full_name, age, gender]):
        return jsonify({"message": "All fields are required."}), 400
    if not terms_accepted:
        return jsonify({"message": "You must accept the terms and conditions."}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"message": "Invalid email format."}), 400
    if not isinstance(age, int) or age < 0:
        return jsonify({"message": "Invalid age. Must be a non-negative integer."}), 400
    if gender not in ["male", "female", "other"]:
        return jsonify({"message": "Invalid gender."}), 400
    if not validate_password(password):
        return jsonify({"message": "Password must be at least 8 characters long, include uppercase, lowercase, number, and special character."}), 400

    # Check if the user already exists in MongoDB
    if User.objects(mobile=mobile).first() or User.objects(email=email).first():
        return jsonify({"message": "Mobile number or email already registered."}), 400

    hashed_password = generate_password_hash(password)
    otp = str(random.randint(100000, 999999))

    # Create a new user
    new_user = User(
        user_name=user_name,
        mobile=mobile,
        email=email,
        password=hashed_password,
        full_name=full_name,
        age=age,
        gender=gender,
        terms_accepted=terms_accepted,
        otp=otp
    )
    new_user.save()
    sender_details = login_app_email()
    msg = MIMEMultipart()
    msg['From'] = sender_details[2]
    msg['To'] = email
    msg['Subject'] = sender_details[4]
    msg.attach(MIMEText(sender_details[5],'html'))

    server = smtplib.SMTP(sender_details[0],sender_details[1])
    server.starttls()
    server.login(sender_details[2],sender_details[3])
    # server.sendmail(sender_details[2],email,sender_details[5])
    server.send_message(msg)
    server.close()
    
    # Simulate sending email and OTP
    print(f"Verification email sent to {email}")
    print(f"OTP sent to mobile {mobile}: {otp}")

    # Update the response to include user_name
    return jsonify({"user_name": user_name, "message": "User registered successfully."}), 200
# Mobile verification route
@register_bp.route('/api/verify_mobile', methods=['POST'])
def verify_mobile():
    user_data = request.json
    mobile = user_data.get('mobile')
    otp = user_data.get('otp')

    if not mobile or not otp:
        return jsonify({"message": "Mobile and OTP are required."}), 400

    user = User.objects(mobile=mobile, otp=otp).first()

    if user:
        user.verified_mobile = True
        user.save()
        return jsonify({"message": "Mobile verified successfully!"}), 200

    return jsonify({"message": "Invalid mobile number or OTP."}), 400

# Email verification route
@register_bp.route('/api/verify_email/<string:user_name>', methods=['GET'])
def verify_email(user_name):
    user = User.objects(user_name=user_name).first()  # Query by user_name (user_id in your model)

    if user:
        user.verified_email = True
        user.save()
        return jsonify({"message": "Email verified successfully!"}), 200

    return jsonify({"message": "Invalid user name."}), 400

# View users route
@register_bp.route('/api/view_users', methods=['GET'])
def view_users():
    users = User.objects()
    return jsonify(users), 200

# Delete user route
@register_bp.route('/api/delete_user', methods=['DELETE'])
def delete_user():
    user_data = request.json
    user_name = user_data.get('user_name')

    if not user_name:
        return jsonify({"message": "User ID is required."}), 400

    user = User.objects(id=user_name).first()
    if not user:
        return jsonify({"message": "User not found."}), 404

    user.delete()
    return jsonify({"message": "User deleted successfully."}), 200