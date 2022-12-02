from flask import Flask, render_template, request, flash, redirect, url_for
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from forms import RegisterForm, LoginForm, SearchForm

# Helper .py files
from settings import API_KEY
from helper import lookup

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Set up SQLite databse with SQLAlchemy
file_path = os.path.abspath(os.getcwd())+'/users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+file_path

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Set up secret key for login
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)


# Set up user class with details about registered users
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(150), index = True, unique = True)
    # Only store a password hash
    password_hash = db.Column(db.String(150))

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


# Set up class for user's interactions with movies
class MovieInteraction(db.Model):
    __tablename__ = 'interactions'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.String)
    watchlist = db.Column(db.Integer, default=0)
    watched = db.Column(db.Integer, default=0)
    liked = db.Column(db.Integer, default=0)



# Pass stuff to navbar
@app.context_processor
def layout():
    form = SearchForm()
    return dict(form_searched=form)


# Homepage
@app.route('/')
def index():
    movie = lookup("search", 'Batman')
    return render_template('index.html', movie=movie)


# List all movies matching the search
@app.route('/list', methods=['POST', 'GET'])
def list():
    form = SearchForm()
    if form.validate_on_submit():
        title = form.searched.data
        movies = lookup("list", title)
        return render_template("list.html", form_searched=form, movies=movies, title=title)

    # Else search is not successful
    movies = None
    return render_template("list.html", movies=movies)


# Unique page for each movie
@app.route('/movie/<title>')
def search(title):
    movie = lookup('search', title)
    watchlist = 0
    watched = 0
    liked = 0
    if current_user.is_authenticated:
        movie_id = movie['imdbID']

        interaction = MovieInteraction.query.filter_by(user_id=current_user.id, movie_id=movie_id).first() 
        if interaction is not None:
            # Get the interaction status
            watchlist = interaction.watchlist
            watched = interaction.watched
            liked = interaction.liked
        
    return render_template('movie.html', movie=movie, watchlist=watchlist, watched=watched, liked=liked)


# Process interaction request
@app.route('/process_interaction', methods=['POST'])
def process_interaction():
    if request.method == 'POST':
        client_data = request.get_json()
        
        # Get movie id
        movie_id = client_data['movie_id']
  
        # Get interaction type (watchlist, watched, liked) based on the key from client_data
        interaction_type = client_data.keys()
        # Get list of keys
        interaction_type = [*interaction_type]


        # Check if there is already an interaction by the current user with movie_id
        interaction = MovieInteraction.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()

        if interaction is not None:
            # Check the type of interaction from client (watchlist, watched, or liked)
            if interaction_type[0] == 'watchlist':
                interaction.watchlist = client_data['watchlist']
            elif interaction_type[0] == 'watched':
                interaction.watched = client_data['watched']
                # Delete the movie id from watchlist once watched is on
                # interaction.watchlist = 0
            elif interaction_type[0] == 'liked':
                interaction.liked = client_data['liked']
            db.session.commit()

            # If all interactions are zero delete the row
            if interaction.watchlist == 0 and interaction.watched == 0 and interaction.liked == 0:
                interaction.delete()
                db.session.commit()

        elif interaction is None:
            new_interaction = MovieInteraction(user_id=current_user.id, movie_id=movie_id) # The watchlist, watched, and liked columns default to 0

            if interaction_type[0] == 'watchlist':
                new_interaction.watchlist = client_data['watchlist']
            elif interaction_type[0] == 'watched':
                new_interaction.watched = client_data['watched']
            elif interaction_type[0] == 'liked':
                new_interaction.liked = client_data['liked']

            db.session.add(new_interaction)
            db.session.commit()

        return 'Success'
    
    return None


# Register page
@app.route('/register', methods=['POST','GET'])
def register():
    # Get data from register form
    form = RegisterForm()
    if form.validate_on_submit():
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        #  Add new user to db
        db.session.add(user)
        db.session.commit()

        # Redirect new user to login page
        return redirect('login.html')

    # Else only render the page
    return render_template('register.html', form=form)


# Login page
@app.route('/login', methods=['POST', 'GET'])
def login():
    # Get data from login form
    form = LoginForm()

    if form.validate_on_submit():
        # Check if input matches an email from db
        user_email = User.query.filter_by(email=form.name.data).first()
        
        # Check if input matches an email from db
        if user_email is not None:
            user = user_email
        # Else input does not match an email from db, look for the username
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
