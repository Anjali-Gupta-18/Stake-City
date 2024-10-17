from pymongo import MongoClient

# Connect to MongoDB
mongo_client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client['stake_city']  # Replace with your database name
collection = db['reputation']

# Data to insert

data = [
    {"Level": 1, "Name": "Crypto Seed Sower", "Investment Required for Level ($)": 1000, "Total Investment So Far ($)": 0, "Multiplier Applied": "1.0x"},
    {"Level": 2, "Name": "Token Tycoon", "Investment Required for Level ($)": 3000, "Total Investment So Far ($)": 1000, "Multiplier Applied": "1.1x"},
    {"Level": 3, "Name": "Stake Shark", "Investment Required for Level ($)": 9000, "Total Investment So Far ($)": 4000, "Multiplier Applied": "1.2x"},
    {"Level": 4, "Name": "Profit Pioneer", "Investment Required for Level ($)": 15000, "Total Investment So Far ($)": 13000, "Multiplier Applied": "1.3x"},
    {"Level": 5, "Name": "Blockchain Baron", "Investment Required for Level ($)": 50000, "Total Investment So Far ($)": 28000, "Multiplier Applied": "1.4x"},
    {"Level": 6, "Name": "Crypto Czar", "Investment Required for Level ($)": 80000, "Total Investment So Far ($)": 78000, "Multiplier Applied": "1.5x"},
    {"Level": 7, "Name": "Stake Sultan", "Investment Required for Level ($)": 120000, "Total Investment So Far ($)": 158000, "Multiplier Applied": "1.6x"},
    {"Level": 8, "Name": "Ethereum Emperor", "Investment Required for Level ($)": 170000, "Total Investment So Far ($)": 278000, "Multiplier Applied": "1.7x"},
    {"Level": 9, "Name": "Digital Dealmaker", "Investment Required for Level ($)": 250000, "Total Investment So Far ($)": 448000, "Multiplier Applied": "1.8x"},
    {"Level": 10, "Name": "Wealth Weaver", "Investment Required for Level ($)": 350000, "Total Investment So Far ($)": 698000, "Multiplier Applied": "1.9x"},
    {"Level": 11, "Name": "Liquidity Legend", "Investment Required for Level ($)": 500000, "Total Investment So Far ($)": 1048000, "Multiplier Applied": "2.0x"},
    {"Level": 12, "Name": "Blockchain Baller", "Investment Required for Level ($)": 650000, "Total Investment So Far ($)": 1548000, "Multiplier Applied": "2.1x"},
    {"Level": 13, "Name": "Crypto Chieftain", "Investment Required for Level ($)": 800000, "Total Investment So Far ($)": 2198000, "Multiplier Applied": "2.2x"},
    {"Level": 14, "Name": "DeFi Dynamo", "Investment Required for Level ($)": 1000000, "Total Investment So Far ($)": 2998000, "Multiplier Applied": "2.3x"},
    {"Level": 15, "Name": "Wealth Whisperer", "Investment Required for Level ($)": 1250000, "Total Investment So Far ($)": 3998000, "Multiplier Applied": "2.4x"},
    {"Level": 16, "Name": "Crypto Commander", "Investment Required for Level ($)": 1500000, "Total Investment So Far ($)": 5248000, "Multiplier Applied": "2.5x"},
    {"Level": 17, "Name": "Yield Yogi", "Investment Required for Level ($)": 2000000, "Total Investment So Far ($)": 6748000, "Multiplier Applied": "2.6x"},
    {"Level": 18, "Name": "Chain Champion", "Investment Required for Level ($)": 2500000, "Total Investment So Far ($)": 8748000, "Multiplier Applied": "2.7x"},
    {"Level": 19, "Name": "Staking Strategist", "Investment Required for Level ($)": 3000000, "Total Investment So Far ($)": 11248000, "Multiplier Applied": "2.8x"},
    {"Level": 20, "Name": "Satoshi Sage", "Investment Required for Level ($)": 4000000, "Total Investment So Far ($)": 14248000, "Multiplier Applied": "3.0x"}
]

# Insert the data into the collection
result = collection.insert_many(data)

# Print inserted IDs to confirm successful insertion
print("Data inserted with IDs:", result.inserted_ids)

