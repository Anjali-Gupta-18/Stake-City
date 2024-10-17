from flask import Flask
from Register import register_bp
from Login import login_bp
from Profile import profile_bp
from question import question_bp
from answer import answer_bp
from payment import payment_bp
from reset import reset_password_bp 

from models import *
app = Flask(__name__)

# Register the blueprints

app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(question_bp)
app.register_blueprint(answer_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(reset_password_bp)


if __name__ == '__main__':
    app.run(debug=True)