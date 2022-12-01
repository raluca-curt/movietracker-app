import requests
from settings import API_KEY
from flask_sqlalchemy import SQLAlchemy 




# Two types can be used
def lookup(type, title):
    # Display a list of all movies with the same title
    if type == 'list':
        try:
            response_raw = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&s={title}")
            
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
            response_raw = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}")
            
            response_raw.raise_for_status()
        except requests.exceptions.RequestException:
            return None
        try:
            response = response_raw.json()
            return response

        except requests.exceptions.JSONDecodeError:
            return None


