import requests
from settings import API_KEY
from flask_sqlalchemy import SQLAlchemy 




# Two types can be used to search by movie title
def lookup_title(type, title):
    # Display a list of all movies with the same title
    if type == 'list':
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

    # Display the first 
    elif type == 'search':
        try:
            response_raw = requests.get(f"http://www.omdbapi.com/?apikey=5aa61ad0&t={title}")
            
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
    # movie_id = int(movie_id)
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