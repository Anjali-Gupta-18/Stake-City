from pymongo import MongoClient
from bson.objectid import ObjectId  # To generate ObjectId for user IDs

# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['stake_city']

# Collections
user_collection = db['user_data'] 
user_col = db['users'] 
reputation_collection = db['reputation']
question_collection = db['questions']  # Assuming there's a questions collection
answers_collection = db['answers']  # Assuming there's an answers collection

# Detailed stake-to-level mapping
stake_level_mapping = {
    (0, 1000): 1,
    (1000, 4000): 2,
    (4000, 13000): 3,
    (13000, 28000): 4,
    (28000, 78000): 5,
    (78000, 158000): 6,
    (158000, 278000): 7,
    (278000, 448000): 8,
    (448000, 698000): 9,
    (698000, 1048000): 10,
    (1048000, 1548000): 11,
    (1548000, 2198000): 12,
    (2198000, 2998000): 13,
    (2998000, 3998000): 14,
    (3998000, 5248000): 15,
    (5248000, 6748000): 16,
    (6748000, 8748000): 17,
    (8748000, 11248000): 18,
    (11248000, 14248000): 19,
    (14248000, float('inf')): 20,
}

# Function to get level based on stake amount
def get_level_by_stake(stake_amount):
    for stake_range, level in stake_level_mapping.items():
        if stake_range[0] <= stake_amount < stake_range[1]:
            return level
    return None  # Return None if no level is found

# Function to calculate current earnings and insert into MongoDB
def calculate_and_store_earnings(question_id, stake_amount):
    # Fetch the question
    question = question_collection.find_one({"_id": ObjectId(question_id)})
    
    if not question:
        print(f"Question with ID {question_id} not found.")
        return

    # Fetch answers related to the question
    answers = list(answers_collection.find({"question_id": ObjectId(question_id)}))
    
    # Extract the IDs of users who answered the question
    answered_users_ids = [answer["answer_giver_user_name"] for answer in answers]

    # Fetch users who answered the question from the user collection by their IDs
    answered_users = list(user_col.find({"_id": {"$in": answered_users_ids}}))

    total_weight = 0
    user_shares = {}
    
    for user in answered_users:
        user_id = user["_id"]  # Fetch the user ID (ObjectId)
        username = user["user_name"]  # Fetch the username for the user
        
        # Count correct answers by comparing user_id with answer_giver_user_name (both ObjectId)
        correct_answers = sum(1 for answer in answers if answer["answer_giver_user_name"] == user_id)

        # Count total answers given by the user for this question
        total_answers = sum(1 for answer in answers if answer["answer_giver_user_name"] == user_id)

        # Determine level based on stake amount
        level = get_level_by_stake(stake_amount)
        if level is None:
            print(f"No level found for {username} with stake amount £{stake_amount}.")
            continue
        
        # Fetch user reputation details from MongoDB
        reputation = reputation_collection.find_one({"Level": level})

        if reputation:
            multiplier = float(reputation["Multiplier Applied"].replace('x', ''))  # Remove 'x' and convert to float
            weight = correct_answers  # Weight is based on the number of correct answers

            total_weight += weight  # Add to total weight
            
            user_shares[user_id] = {
                "weight": weight,
                "multiplier": multiplier,
                "total_answers": total_answers,
                "username": username  # Store the username here
            }
    
    # Calculate shares and earnings
    for user_id, details in user_shares.items():
        weight = details["weight"]
        multiplier = details["multiplier"]
        total_answers = details["total_answers"]
        username = details["username"]  # Get the username for this user

        # Calculate proportional share for this user
        share = (weight / total_weight) * stake_amount if total_weight > 0 else 0
        
        # Calculate earnings based on share and multiplier
        earnings = share * multiplier
        
        # Insert a new earnings record for the user
        user_collection.insert_one({
            "user_id": user_id,
            "username": username,
            "stake_amount": stake_amount,
            "earnings": earnings
           
        })

        # Print the results for the user
        print(f"User ID: {user_id} - Username: {username}, Weight: {weight}, Total Answers: {total_answers}, Share: £{share:.2f}, Earnings: £{earnings:.2f}")


question_id = "670549c1c534b44fc783b394"  
stake_amount = 1000  # Example stake amount
calculate_and_store_earnings(question_id, stake_amount)
