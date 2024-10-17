
from authlib.integrations.flask_client import OAuth
from flask import Flask

GOOGLE_CLIENT_ID = ''  # Replace with your Google client ID
GOOGLE_CLIENT_SECRET = ''  # Replace with your Google client secret

# Create Flask app
app = Flask(__name__)

# Initialize OAuth with app
oauth = OAuth(app)

# Register Google OAuth provider
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'},
)

token = oauth.google.authorize_access_token()
print(token['id_token'])