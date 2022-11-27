from flask import Flask, render_template, request, flash, redirect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from forms import Register, Login


app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set up SQLite databse with SQLAlchemy
file_path = os.path.abspath(os.getcwd())+'/users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
    # Only store a password hash
    password_hash = db_users.Column(db_users.String(150))

    # Get hash for password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    # Check password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Get current user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Homepage
@app.route('/')
def index():
    return render_template('index.html')


# Register page
@app.route('/register', methods = ['POST','GET'])
def register():
    # Get data from register form
    form = Register()
    if form.validate_on_submit():
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        #  Add new user to db_users
        db_users.session.add(user)
        db_users.session.commit()

        # Redirect new user to login page
        return redirect('login.html')

    # Else only render the page
    return render_template('register.html', form=form)


# Login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    # Get data from login form
    form = Login()

    if form.validate_on_submit():
        # Check if input matches an email from db_users
        user_email = User.query.filter_by(email=form.name.data).first()
        
        # Check if input matches an email from db_users
        if user_email is not None:
            user = user_email
        # Else input does not match an email from db_users, look for the username
        else:
            user = User.query.filter_by(username=form.name.data).first()
            
        # If user exists and it matches the password, login user
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get("next")
            return redirect(next or '/')

        # If invalid email or password, flash error
        flash('Invalid email or password.')

    # Else only render the page
    return render_template('login.html', form=form)


# Logout user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')