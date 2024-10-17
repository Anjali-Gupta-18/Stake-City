from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from pymongo import MongoClient
import secrets

app = Flask(__name__)
jwt_secret_key = secrets.token_hex(32)
app.config['JWT_SECRET_KEY'] = jwt_secret_key 
jwt = JWTManager(app)

# MongoDB setup
client = MongoClient("mongodb+srv://p2etokens:Play2earn%40@cluster0.hfnr9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['stake_city']
sessions_collection = db['sessions']
users_collection = db["users"] 
# Mock User Data (Replace with your real database lookup)
# users = {'user1': 'password1', 'user2': 'password2'}
# Login Endpoinst
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
  
    if users_collection.find_one({"user_name": username}):
        login_time = datetime.now()
        access_token = create_access_token(identity={'username': username, 'login_time': login_time.isoformat()})
        
        # Save login time in MongoDB (for session tracking)
        sessions_collection.insert_one({
            'username': username,
            'login_time': login_time,
            'logout_time': None
        })
        
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Protected Route (to ensure user is logged in)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Logout Endpoint
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    username = current_user['username']
    
    # Calculate logout time
    logout_time = datetime.now()
    
    # Fetch the user's session (login time) from MongoDB
    session = sessions_collection.find_one({'username': username, 'logout_time': None})
    
    if session:
        login_time = session['login_time']
        time_spent = logout_time - login_time
        time_spent_minutes = time_spent.total_seconds() / 60
        
        # Update the session with logout time and time spent
        sessions_collection.update_one(
            {'_id': session['_id']},
            {'$set': {'logout_time': logout_time, 'time_spent': time_spent_minutes}}
        )
        
        return jsonify(message=f'You spent {time_spent_minutes:.2f} minutes in this session.'), 200
    else:
        return jsonify({'message': 'No active session found'}), 400

if __name__ == '__main__':
    app.run(debug=True)
