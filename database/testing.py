from pymongo import MongoClient
from bson.objectid import ObjectId

# Initialize MongoDB Client
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['stake_city']
reputation_collection = db['reputation']
user_reputation_collection = db['users_reputation']  # Collection for user reputations
user_data_collection = db['user_data']  # Collection to insert user data

# Function to fetch the user's level and total stake amount
# def get_user_level_and_total_stake(user_id):
#     try:
#         user_id_object = ObjectId(user_id)
#         user_reputation_data = user_reputation_collection.find_one({"_id": user_id_object})
        
#         if user_reputation_data:
#             return {
#                 "level": user_reputation_data.get("level"),
#                 "total_stake_amount": user_reputation_data.get("total_stake_amount"),
#                 "user_name": user_reputation_data.get("user_name_str")  # Fetch the username if needed
#             }
#     except Exception as e:
#         print("Error:", str(e))
#     return None

def get_user_level_and_total_stake(user_id):
    try:
        user_id_object = ObjectId(user_id)
        user_reputation_data = user_reputation_collection.find_one({"_id": user_id_object})
        
        if user_reputation_data:
            # Fetch the username, if not found, assume the user is at level 1
            user_name = user_reputation_data.get("user_name_str")
            
            return {
                "level": user_reputation_data.get("level", 1),  # Default to level 1 if no level data is found
                "total_stake_amount": user_reputation_data.get("total_stake_amount", 0),  # Default to 0 if no stake amount
                "user_name": user_name if user_name else "Unknown"  # Assign "Unknown" if no username is found
            }
        else:
            # Default behavior for users not found in the reputation table
            return {
                "level": 1,
                "total_stake_amount": 0,
                "user_name": "Unknown"  # If user is not found, assign "Unknown" username
            }
    except Exception as e:
        print("Error:", str(e))
    return None


# Function to calculate 'earn' based on user levels and total stake amounts
def calculate_earn(user_ids):
    multipliers = []
    user_names = []

    # For a temporary stake amount
    stake_amount = 1000  # Temporary stake amount for calculation

    # Fetch each user's level, total stake amount, and username
    for user_id in user_ids:
        user_data = get_user_level_and_total_stake(user_id)
        if user_data:
            level = user_data['level']
            user_name = user_data['user_name']

            # Check if level is valid before querying reputation data
            if level is not None:
                # Query the reputation collection for the corresponding level
                reputation_data = reputation_collection.find_one({"Level": level})

                if reputation_data:
                    # Extract and convert the multiplier to float (assuming it's a string like "1.2x")
                    multiplier_str = reputation_data.get("Multiplier Applied", "1x")  # Default to "1x" if not found
                    multiplier = float(multiplier_str.replace("x", ""))  # Convert to float
                    multipliers.append(multiplier)
                else:
                    print(f"No reputation data found for level: {level}")
                    multipliers.append(1)  # Default multiplier if no reputation data found
            else:
                print(f"User {user_id} has no level data.")
                multipliers.append(1)  # Default multiplier if no level found

            user_names.append(user_name)
        else:
            print(f"No data found for user ID: {user_id}")
            multipliers.append(1)  # Default multiplier if user data not found
            user_names.append(None)  # Placeholder for username

    # Calculate total weight (sum of multipliers)
    total_weight = sum(multipliers)

    # For each user, calculate their share and earn
    earnings = []
    for i in range(len(user_ids)):
        user_multiplier = multipliers[i]

        # Calculate share: total_stake_amount / total_weight
        if total_weight > 0:
            share = stake_amount / total_weight
            # Calculate earn: share * user_multiplier 
            earn = share * user_multiplier
            earnings.append(earn)
            # Insert into user_data collection if user_names[i] is not None
            if user_names[i]:
                user_data_entry = {
                    "user_id": user_ids[i],
                    "user_name": user_names[i],
                    "stake_amount": stake_amount,
                    "earn": earn
                }
                try:
                    print(f"Inserting into database: {user_data_entry}")
                    user_data_collection.insert_one(user_data_entry)
                    print(f"Successfully inserted data for user {user_ids[i]}")
                except Exception as e:
                    print(f"Error inserting data for user {user_ids[i]}: {e}")
        else:
            earnings.append(0)  # If no total weight, earn is 0

    return earnings



# Example usage
user_ids = ["670549c1c534b44fc783b381", "670549c1c534b44fc783b382", "67069db8e0803dc2c2dffd51"]  # Replace with actual user IDs
earn_values = calculate_earn(user_ids)

for idx, earn in enumerate(earn_values):
    print(f"User {user_ids[idx]} Earn: {earn}")
