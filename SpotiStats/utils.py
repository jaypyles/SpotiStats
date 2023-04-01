from typing import Union
import requests
from functools import wraps
from SpotiStats.spotify import Artist, Album, SpotifyObject

class AuthenticationError(Exception):
    "User is not authenticated."
    pass
def generate_authorization_token(client_id: str, client_secret:str) -> tuple[str, int]:
    """
    Generates Spotify user authorization token based on client_id and client_secret
    :param client_id: your client id from Spotify api
    :param client_secret: your client secret from Spotfiy api
    :return: your authorization token 
    :rtype: str
    """
    url = "https://accounts.spotify.com/api/token"
    payload = {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    return response.json().get("access_token", "No Token"), response.status_code

def authenticate(response_code):
    """
    Authenticator for the Spotify functions
    """
    def authenticate_command(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if response_code != 200:
                raise AuthenticationError("Is not authenticated.")
            else:
                result = func(*args, **kwargs)
                return result
        return wrapper
    return authenticate_command

def search_spotify(query: str, type: str, offset: int, token: str) -> Union[dict[int, Artist], dict[int, Album], None]:
    """
    Searches Spotify for the specified query
    :param query: the search  
    :param type: the type of search (artist, song, etc)
    :return: a Search object
    :rtype: SpotiStats.Search
    """
    try:
        headers = {
            "Authorization" : "Bearer " + token  
        }
        constructed_query = query.replace(" ", "%20") 
        base_url = f"https://api.spotify.com/v1/search?q={constructed_query}&type={type}&offset={offset}&limit=5"
        
        request = requests.get(base_url, headers=headers)
        json_request = request.json()
        if type == "artist":
            artist_list  = {}
            artists = json_request.get("artists")
            items = artists.get("items")
            for index, item in enumerate(items):
                artist = Artist()
                external_url = item.get("external_urls")
                artist.url = external_url.get("spotify")
                followers = item.get("followers")
                artist.followers = followers.get("total")
                genres = item.get("genres")
                genres = [genre for genre in genres]
                artist.id = item.get("id")
                artist.name = item.get("name")
                artist.popularity = item.get("popularity")
                artist_list[index] = artist

            return artist_list
        elif type == "album":
            album_list = {}
            albums = json_request.get("albums")
            items = albums.get("items")
            for index, item in enumerate(items):
                album = Album()
                playlist_artists = [] 
                artists = item.get("artists")
                for info in artists:
                    artist = Artist()
                    external_urls = info.get("external_urls") 
                    artist.url = external_urls.get("spotify")
                    artist.name = info.get("name")
                    artist.id = info.get("id")
                    playlist_artists.append(artist)
                external_urls = item.get("external_urls")
                album.url = external_urls.get("spotify")
                album.artists = playlist_artists
                album.id = item.get("id")
                album.name = item.get("name")
                album_list[index] = album
            return album_list
        else:
            return None 
    except Exception as e:
        print(e)
     
