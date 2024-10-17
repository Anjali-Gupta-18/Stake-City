from pymongo import MongoClient
from bson.objectid import ObjectId  # To generate ObjectId for user IDs
import random
from datetime import datetime, timedelta

# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['stake_city']

# Drop collections if they exist
db.users.drop()
db.questions.drop()
db.answers.drop()

# Create collections
users_collection = db.users
questions_collection = db.questions
answers_collection = db.answers

# Function to insert dummy users
def insert_dummy_users(num_users=10):
    users = []
    for i in range(num_users):
        user = {
            "user_name": f"user_{i+1}",
            "mobile": f"12345678{i+1}",
            "email": f"user{i+1}@example.com",
            "password": "password123",
            "full_name": f"User {i+1}",
            "age": random.randint(18, 50),
            "gender": random.choice(["Male", "Female"]),
            "terms_accepted": True,
            "verified_email": True,
            "verified_mobile": True,
            "otp": None  # No OTP for dummy data
        }
        users.append(user)
    users_collection.insert_many(users)  # Insert all users at once

# Function to insert dummy questions
def insert_dummy_questions(num_questions=5):
    users = list(users_collection.find())  # Fetch all users to assign questions
    for i in range(num_questions):
        if users:
            question = {
                "user_name": random.choice(users)["_id"],  # Reference to User ID
                "user_name_str": random.choice(users)["user_name"],  # Store the username as a string
                "question": f"This is a sample question {i+1}",
                "question_id": str(ObjectId()),  # Generate a new question ID
                "latitude": random.uniform(-90.0, 90.0),  # Random latitude
                "longitude": random.uniform(-180.0, 180.0),  # Random longitude
                "location_name": f"Location {i+1}",
                "created_at": datetime.utcnow(),
                "visible_until": datetime.utcnow() + timedelta(days=7),  # Visible for 7 days
                "has_been_extended": False,
                "stake_amount": random.uniform(100.0, 1000.0)  # Random stake amount
            }
            questions_collection.insert_one(question)  # Save each question

# Function to insert dummy answers
def insert_dummy_answers(num_answers=15):
    questions = list(questions_collection.find())  # Fetch all questions to assign answers
    users = list(users_collection.find())  # Fetch all users to assign answer givers
    for i in range(num_answers):
        if questions and users:
            answer = {
                "question_id": random.choice(questions)["_id"],  # Reference to Question ID
                "asker_user_name": random.choice(users)["_id"],  # User who asked the question
                "answer_giver_user_name": random.choice(users)["_id"],  # User who provided the answer
                "answer": f"This is a sample answer {i+1}",
                "created_at": datetime.utcnow(),  # Timestamp
                "likes": random.randint(0, 100),  # Random likes
                "dislikes": random.randint(0, 10),  # Random dislikes
                "reports": random.randint(0, 5)  # Random reports
            }
            answers_collection.insert_one(answer)  # Save each answer

# Insert dummy data
insert_dummy_users(10)  # Insert 10 dummy users
insert_dummy_questions(10)  # Insert 5 dummy questions
insert_dummy_answers(15)  # Insert 15 dummy answers

print("Dummy data inserted successfully.")
