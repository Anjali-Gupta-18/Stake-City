from pymongo import MongoClient

# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['stake_city']
collection = db['badge']

# Data to insert
badge_data = [
    {"Level": 1, "Name": "City Sleuth"},
    {"Level": 2, "Name": "Urban Whisperer"},
    {"Level": 3, "Name": "Concrete Conqueror"},
    {"Level": 4, "Name": "Metro Maverick"},
    {"Level": 5, "Name": "Skyline Sage"},
    {"Level": 6, "Name": "Street Smart"},
    {"Level": 7, "Name": "City Navigator"},
    {"Level": 8, "Name": "District Dazzler"},
    {"Level": 9, "Name": "Town Titan"},
    {"Level": 10, "Name": "Block Boss"},
    {"Level": 11, "Name": "Urban Detective"},
    {"Level": 12, "Name": "Metro Guru"},
    {"Level": 13, "Name": "Highway Hero"},
    {"Level": 14, "Name": "Pavement Philosopher"},
    {"Level": 15, "Name": "Cornerstone Champ"},
    {"Level": 16, "Name": "Urban Pathbreaker"},
    {"Level": 17, "Name": "Bridge Builder"},
    {"Level": 18, "Name": "Traffic Tactician"},
    {"Level": 19, "Name": "City Sentinel"},
    {"Level": 20, "Name": "Asphalt Analyst"},
    {"Level": 21, "Name": "Urban Oracle"},
    {"Level": 22, "Name": "Skyway Specialist"},
    {"Level": 23, "Name": "Boulevard Baron"},
    {"Level": 24, "Name": "Street Specialist"},
    {"Level": 25, "Name": "City Pulse Finder"},
    {"Level": 26, "Name": "Urban Virtuoso"},
    {"Level": 27, "Name": "Grit Guardian"},
    {"Level": 28, "Name": "Alley Ace"},
    {"Level": 29, "Name": "City Codecracker"},
    {"Level": 30, "Name": "Route Rocketeer"},
    {"Level": 31, "Name": "Crosswalk Captain"},
    {"Level": 32, "Name": "Urban Vanguard"},
    {"Level": 33, "Name": "Concrete Custodian"},
    {"Level": 34, "Name": "City Circuitry"},
    {"Level": 35, "Name": "Grid General"},
    {"Level": 36, "Name": "City Scoutmaster"},
    {"Level": 37, "Name": "Metropolis Maestro"},
    {"Level": 38, "Name": "Skyway Strategist"},
    {"Level": 39, "Name": "Avenue Ace"},
    {"Level": 40, "Name": "Urban Navigator Extraordinaire"}
]

# Insert the data into the badge collection
result = collection.insert_many(badge_data)

# Print inserted IDs to confirm successful insertion
print("Badge data inserted with IDs:", result.inserted_ids)
