from mongoengine import Document, StringField, DateTimeField, ReferenceField, IntField, FloatField, BooleanField, connect
from datetime import datetime

# Connect to MongoDB on localhost
connect('stake_city', host='localhost', port=27017)

# User Model
class User(Document):
    user_name = StringField(required=True, unique=True)  # This is the unique user identifier
    mobile = StringField(required=True)
    email = StringField(required=True,unique=True)
    password = StringField()
    full_name = StringField(required=True)
    age = IntField(required=True)
    gender = StringField(required=True)
    terms_accepted = BooleanField(default=False)
    verified_email = BooleanField(default=False)
    verified_mobile = BooleanField(default=False)
    otp = StringField()

# Question Model
class Question(Document):
    user_name = ReferenceField(User, required=True)  # Foreign key to User (reference)
    question = StringField(required=True)
    latitude = FloatField()
    longitude = FloatField()
    location_name = StringField()  # Column for location name
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp

# Answer Model
class Answer(Document):
    question_id = ReferenceField(Question, required=True)  # Foreign key to Question
    asker_user_name = ReferenceField(User, required=True)  # User who asked the question
    answer_giver_user_name = ReferenceField(User, required=True)  # User who provided the answer
    answer = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp
    likes = IntField(default=0)
    dislikes = IntField(default=0)
    reports = IntField(default=0)

# Payment Model
class Payment(Document):
    user_name = ReferenceField(User, required=True)  # Foreign key to User
    question_id = ReferenceField(Question, required=True)  # Foreign key to Question
    answer_id = ReferenceField(Answer, required=True)  # Foreign key to Answer
    likes = IntField(default=0)
    transaction_id = StringField()
    amount_paid = FloatField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)  # Timestamp

# Login Activity Model
class LoginActivity(Document):
    user_name = ReferenceField('User', required=True)  # Reference to the User model (Foreign key)
    ip_address = StringField(required=True)  # IP address of the user
    browser_name = StringField(required=True)  # Browser name
    device_type = StringField(required=True)  # Device type (e.g., mobile, desktop)
    device_name = StringField(required=True)  # Device name (e.g., iPhone, Pixel)
    brand = StringField(required=True)  # Brand of the device (e.g., Apple, Google)
    model = StringField(required=True)  # Model of the device (e.g., iPhone 12)
    city = StringField(required=True)  # City based on IP address
    region = StringField(required=True)  # Region (state/province) based on IP
    country = StringField(required=True)  # Country based on IP
    login_timestamp = DateTimeField(default=datetime.utcnow)
    last_passwords = StringField()  # Timestamp of login

# Password Reset Model
class PasswordReset(Document):
    user_name = ReferenceField(User, required=True)
    old_password = StringField(required=True)
    new_password = StringField(required=True)
    reset_timestamp = DateTimeField(default=datetime.utcnow)


# Model to store previous passwords
class PreviousPasswords(Document):
    email = StringField(required=True)  # Store email directly
    old_password = StringField(required=True)
    reset_timestamp = DateTimeField(default=datetime.utcnow)