from flask import Flask, render_template, request
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin


app = Flask(__name__)

# # # From CSS50 PSET9
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Set up session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set API key
api_key = "5aa61ad0"

@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
# # # End

# Set up SQLite databse with SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_users = SQLAlchemy(app)

# Set up secrete key for login
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Set up user class with details about registered users
class User(UserMixin, db_users.Model):
    id = db_users.Column(db_users.Integer, primary_key=True, unique=True)
    username = db_users.Column(db_users.String(50), index=True, unique=True)
    email = db_users.Column(db_users.String(150), index = True, unique = True)
    password_hash = db_users.Column(db_users.String(150))

    # Set password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    # Check password
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

# Get current user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    return render_template("index.html")