# MovieTracker
### Deployment: https://movietracker-app.herokuapp.com/

### Video Demo: https://youtu.be/zMxCedVnx2Y

## About
MovieTracker allows you to look up movies and:
- Track the ones you've watched;
- Add movies to your favorites;
- Save the ones you want to see.

## Technologies
- Flask
- Python
- SQLite
- HTML
- CSS
- Bootstrap
- JavaScript
- jQuery

## Installation
- Fork this repository;
- Create a virtual environment in your local directory (https://flask.palletsprojects.com/en/2.2.x/installation/#virtual-environments);
- Get your own API KEY from [OMDB API](http://www.omdbapi.com/) and save it in an .env file. Then, follow the template in settings.py in order to set up the app to use the key;
- Install the libraries listed in requirements.txt
- Run the app in the virtual environment
```
$ flask run
```

# Features
## Index page
Users can access the index/home page without being logged in. They can search for a movie using the search form in the navbar. The input will be send to backend using a POST request and the user will be redirected to the List page.

## List page
Users will be presented with a maximum of ten movies that best match their search input. In the case of no results or an error, users will be asked to try again.

An empty search value is handled by the backend which will request users to type at least one character before submitting.

## Movie page
Once users click on a movie presented on the list page, they will be redirected to that individual movie's page: /movie/<movie_id>, where movie_id stands for the movie's IMDB ID.

Using the OMDB API the backend fetches the data available for the specific movie, such as title, year, director, description, ratings, genre, actors, and other details.

If the user is logged in, they will be presented with the option of interacting with the movie by adding it to their watchlist, watched, or liked lists. The data will be stored in the database using SQLite and SQLAlchemy.

## Register & Log in pages
Form validation is implemented on both frontend and backend, and users won't be able to submit an empty form, passwords that don't match, an invalid email, or a password that is less than 12 characters. Passwords are stored safely using a password hash.

## Profile page
Users can view their watchlist, watched, or liked lists. The app will display the data stored in db for each user. They can click on each movie and navigate to its page.


## SQLite database using SQLAlchemy
The database contains two tables:
- users stores the users information once they register an account: id, username, email, password_hash;
- interactions stores the users' interactions with each movie: user_id, movie_id, watchlist (1 or 0), watched (1 or 0), liked (1 or 0).
