from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize MongoDB Client
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['stake_city']
question_collection = db['questions']
user_repu_collection = db['users_reputation']


# Function to get level based on investment
def get_level_from_investment(investment):
    if investment < 1000:
        return 1
    elif investment < 4000:
        return 2
    elif investment < 13000:
        return 3
    elif investment < 28000:
        return 4
    elif investment < 78000:
        return 5
    elif investment < 158000:
        return 6
    elif investment < 278000:
        return 7
    elif investment < 448000:
        return 8
    elif investment < 698000:
        return 9
    elif investment < 1048000:
        return 10
    elif investment < 1548000:
        return 11
    elif investment < 2198000:
        return 12
    elif investment < 2998000:
        return 13
    elif investment < 3998000:
        return 14
    elif investment < 5248000:
        return 15
    elif investment < 6748000:
        return 16
    elif investment < 8748000:
        return 17
    elif investment < 11248000:
        return 18
    elif investment < 14248000:
        return 19
    else:
        return 20

# Function to fetch the total stake amount, level, and username for a user
def get_user_total_stake_and_level(user_id):
    user_id_object = ObjectId(user_id)
    print(user_id_object)

    # Calculate total stake amount by summing all the stake_amount values for the user
    total_stake = question_collection.aggregate([
        {"$match": {"user_name": user_id_object}},  # Match documents for this specific user
        {"$group": {
            "_id": "$user_name",  # This keeps the grouping consistent
            "total_stake": {"$sum": "$stake_amount"}  # Sum the stake_amount
        }}
    ])
    total_stake = list(total_stake)  # Convert to list to access the result

    if total_stake:
        total_stake_amount = total_stake[0]["total_stake"]
        level = get_level_from_investment(total_stake_amount)

        # Retrieve the username and user_name_str from question collection
        question_data = question_collection.find_one({"user_name": user_id_object})
        
        # Verify if data is found, if not, print a message
        if question_data:
            user_name = question_data.get("user_name")
            user_name_str = question_data.get("user_name_str")
        else:
            print("No matching user found in questions collection.")
            user_name = None
            user_name_str = None

        # Insert or update the user's total stake and level in the user_data collection
        user_repu_collection.update_one(
            {"_id": user_id_object},  # Match by user ID
            {"$set": {
                "total_stake_amount": total_stake_amount,
                "level": level,
                "user_name": user_name,
                "user_name_str": user_name_str  # Optional: You might want to store the user_name_str as well
            }},
            upsert=True  # Insert if the document doesn't exist
        )

        return {
            "total_stake_amount": total_stake_amount,
            "level": level,
            "user_name": user_name,
            "user_name_str": user_name_str
        }

    return None

# Example usage
user_id = "670549c1c534b44fc783b381"  # Replace with the actual user ID
user_data = get_user_total_stake_and_level(user_id)

if user_data:
    print(f"User: {user_data['user_name']} ({user_data['user_name_str']}) | Total Stake: {user_data['total_stake_amount']} | Level: {user_data['level']}")
else:
    print("User not found or no stake amount data.")
