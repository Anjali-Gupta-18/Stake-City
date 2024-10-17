from flask import Flask, redirect, url_for, session, jsonify, request, render_template
from authlib.integrations.flask_client import OAuth
from mongoengine import connect
from models import User
import random
import re
from werkzeug.security import generate_password_hash

# Create Flask app
app = Flask(__name__)
# Hardcoded values for testing
app.secret_key = ''  # Replace with a strong secret key
GOOGLE_CLIENT_ID = ''  # Replace with your Google client ID
GOOGLE_CLIENT_SECRET = ''  # Replace with your Google client secret
MONGO_URI = 'mongodb://localhost/stake_city'  # Replace with your MongoDB URI

# Connect to MongoDB
connect(db='stake_city', host='localhost', port=27017)

# Initialize OAuth with app
oauth = OAuth(app)
# Register Google OAuth provider
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://openidconnect.googleapis.com/v1/',
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
    client_kwargs={
        'scope': 'openid profile email',
        'response_type': 'code'
    }
)

oauth.register(
    name='facebook',
    client_id='407676165470879',
    client_secret='',
    authorize_url='https://www.facebook.com/dialog/oauth',
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    userinfo_endpoint='https://graph.facebook.com/me?fields=id,name,email',
    client_kwargs={'scope': 'email'}
)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login/google', methods=['GET', 'POST'])
def google_login():
    # Generate a nonce and store it in the session
    nonce = str(random.randint(100000, 999999))
    session['nonce'] = nonce

    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/login/facebook', methods=['GET', 'POST'])
def facebook_login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri, prompt='select_account')
@app.route('/authorize')
def authorize():
    try:
        # Google OAuth process
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.parse_id_token(token, nonce=session['nonce'])

        # Extract email and full name
        email = user_info.get('email')
        full_name = user_info.get('name', '')
        session['email'] = email
        session['full_name'] = full_name

        # Check if user exists in the database
        user = User.objects(email=email).first()

        if not user:
            # Redirect user to the registration form if not found
            return redirect(url_for('complete_registration_form'))  # Redirect to registration form page
        else:
            # If user exists, log them in
            session['user_name'] = user.user_name
            return render_template('profile.html', user=user)  # Redirect to profile page after login

    except Exception as e:
        return jsonify({"error": "Authorization failed.", "details": str(e)}), 400

@app.route('/complete_registration', methods=['POST'])
def complete_registration():
    if 'email' not in session:
        return jsonify({"error": "User not logged in."}), 401


    # Get form data from the 
    email = request.form.get('email')
    user_name = request.form.get('user_name')
    mobile = request.form.get('mobile')
    age = request.form.get('age')
    gender = request.form.get('gender')
    terms_accepted = request.form.get('terms_accepted', False)
    full_name = request.form.get('full_name')
    # If user_name is not provided, set it to the full_name
    if not user_name:
        user_name = full_name

    # Create or update the user in the database
    user = User.objects(email=email).first()
    if not user:
        # Create a new user if one doesn't exist
        user = User(
            email=email,
            full_name=full_name,
            password="as",
            mobile=mobile,
            age=age,
            gender=gender,
            terms_accepted=terms_accepted
        )
        user.save()

        return redirect(url_for('profile'))
    # Redirect to profile page after successful registration

    return jsonify({"error": "User not found."}), 404
@app.route('/complete_registration_form')
def complete_registration_form():
    if 'email' not in session:
        return redirect(url_for('login'))  # Redirect to login if user is not authenticated

    return render_template('complete_registration.html', email=session['email'], full_name=session['full_name'])

if __name__ == "__main__":
    app.run(debug=True)
# from flask import Flask, redirect, url_for, session, jsonify, request, render_template
# from authlib.integrations.flask_client import OAuth
# from mongoengine import connect
# from models import User
# import random
# import re
# from werkzeug.security import generate_password_hash

# # Create Flask app
# app = Flask(__name__)
# # Hardcoded values for testing

# # Connect to MongoDB
# connect(db='stake_city', host='localhost', port=27017)

# # Initialize OAuth with app
# oauth = OAuth(app)
# # Register Google OAuth provider
# oauth.register(
#     name='google',
#     client_id=GOOGLE_CLIENT_ID,
#     client_secret=GOOGLE_CLIENT_SECRET,
#     access_token_url='https://oauth2.googleapis.com/token',
#     authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
#     api_base_url='https://openidconnect.googleapis.com/v1/',
#     jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
#     client_kwargs={
#         'scope': 'openid profile email',
#         'response_type': 'code'
#     }
# )

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login/google', methods=['GET', 'POST'])
# def google_login():
#     # Generate a nonce and store it in the session
#     nonce = str(random.randint(100000, 999999))
#     session['nonce'] = nonce

#     redirect_uri = url_for('authorize', _external=True)
#     return oauth.google.authorize_redirect(redirect_uri, nonce=nonce)
# @app.route('/authorize')
# def authorize():
#     try:
#         # Google OAuth process
#         token = oauth.google.authorize_access_token()
#         user_info = oauth.google.parse_id_token(token, nonce=session['nonce'])

#         # Extract email and full name
#         email = user_info.get('email')
#         full_name = user_info.get('name', '')
#         session['email'] = email
#         session['full_name'] = full_name

#         # Check if user exists in the database
#         user = User.objects(email=email).first()

#         if not user:
#             # Redirect user to the registration form if not found
#             return redirect(url_for('complete_registration_form'))  # Redirect to registration form page
#         else:
#             # If user exists, log them in
#             session['user_name'] = user.user_name
#             return render_template('profile.html', user=user)  # Redirect to profile page after login

#     except Exception as e:
#         return jsonify({"error": "Authorization failed.", "details": str(e)}), 400

# @app.route('/complete_registration', methods=['POST'])
# def complete_registration():
#     print(request.form)  # Debugging: print form data

#     if 'email' not in session:
#         return jsonify({"error": "User not logged in."}), 401

#     email = session['email']
#     full_name = session['full_name']
#     user_name = request.form.get('user_name')
#     mobile = request.form.get('mobile')
#     age = request.form.get('age')
#     gender = request.form.get('gender')
#     terms_accepted = request.form.get('terms_accepted') == 'on'

#     if not all([mobile, age, gender]):
#         return jsonify({"error": "All required fields must be provided (mobile, password, age, gender)."}), 400

#     # Check for existing user by email
#     existing_user = User.objects(email=email).first()
#     if existing_user:
#         return jsonify({"error": "Email is already registered. Please log in."}), 400

#     # Create new user if not found
#     new_user = User(
#         user_name=user_name, 
#         mobile=mobile,
#         email=email,
#         full_name = full_name,
#         age=age,
#         gender=gender,
#         terms_accepted=terms_accepted
#     )
#     new_user.save()

#     return jsonify({"message": "Registration completed successfully!", "user": new_user.to_json()})

# @app.route('/complete_registration_form')
# def complete_registration_form():
#     if 'email' not in session:
#         return redirect(url_for('login'))  # Redirect to login if user is not authenticated

#     return render_template('complete_registration.html', email=session['email'], full_name=session['full_name'])

# if __name__ == "__main__":
#     app.run(debug=True)