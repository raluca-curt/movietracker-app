import requests
from settings import API_KEY
from flask_sqlalchemy import SQLAlchemy 


# Display a list of all movies with the same title
def lookup_title(title):
    # Handle errors
    try:
        response_raw = requests.get(f"http://www.omdbapi.com/?apikey=5aa61ad0&s={title}&type=movie")
        
        response_raw.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    try:
        response = response_raw.json()
        return response

    except requests.exceptions.JSONDecodeError:
        return None


# Lookup movie by id
def lookup_id(movie_id):
    # Handle errors
    try:
        response_raw = requests.get(f"http://www.omdbapi.com/?apikey=5aa61ad0&i={movie_id}")
        
        response_raw.raise_for_status()
    except requests.exceptions.RequestException:
        return None
    try:
        response = response_raw.json()
        return response

    except requests.exceptions.JSONDecodeError:
        return None