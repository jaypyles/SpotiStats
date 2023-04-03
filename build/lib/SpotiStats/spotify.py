from typing import Optional
from json import dumps, loads
import requests
from SpotiStats.exceptions import AuthenticationError

class SpotifyObject():
    """
    Basic class representing all types from Spotify
    """
    def __init__(self, id: str, name: str, url: str) -> None:
        self.id = id
        self.name = name
        self.url = url
    def __repr__(self) -> str:
        return f"Name: {self.name}, URL: {self.url}"


class Artist(SpotifyObject):
    def __init__(self, genres: Optional[str], followers: Optional[str], popularity: Optional[str], 
                 id: str, name: str, url: str) -> None:
        self.genres = genres
        self.followers = followers
        self.popularity = popularity
        super().__init__(id, name, url)

class Album(SpotifyObject):
    def __init__(self, artists: Optional[list], release: str, total_tracks: int,
                 id: str, name: str, url: str) -> None:
        self.artists = artists
        self.release = release
        self.total_tracks = total_tracks
        super().__init__(id, name, url)

class Track(SpotifyObject):
    def __init__(self, id: str, name: str, url: str, artists: list, duration: int, explicit: bool, popularity: int, album: Album, track_number: int) -> None:
        self.artists = artists
        self.duration = duration
        self.explicit = explicit
        self.popularity = popularity
        self.track_number = track_number
        self.album = album
        super().__init__(id, name, url)

class Authenticator():
    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str) -> None:
       self.CLIENT_ID = CLIENT_ID
       self.CLIENT_SECRET = CLIENT_SECRET
       self.access_token = None
       self.max_retries = 5

    def generate_authorization_token(self) -> str:
        """
        Generates Spotify user authorization token based on client_id and client_secret
        :param client_id: your client id from Spotify api
        :param client_secret: your client secret from Spotfiy api
        :return: your authorization token 
        :rtype: str
        """
        url = "https://accounts.spotify.com/api/token"
        payload = {"grant_type": "client_credentials", "client_id": self.CLIENT_ID, "client_secret": self.CLIENT_SECRET}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=payload, headers=headers)
        self.access_token = response.json().get("access_token")
        return response.json().get("access_token")
    
    def is_authenticated(self):
        """
        Checks if user is authenticated
        """
        return True if self.access_token is not None else False

class Spotify():
    def __init__(self, authenticator: Authenticator) -> None:
        self.authenticator = authenticator

    def search(self, query: str, type: str, offset: Optional[int]=0):
        retries = 0
        if not self.authenticator.is_authenticated() and retries <= self.authenticator.max_retries:
           self.authenticator.generate_authorization_token()
           retries += 1
            
        if self.authenticator.access_token is not None:
            headers = {
                "Authorization" : "Bearer " + self.authenticator.access_token
            }
            constructed_query = query.replace(" ", "%20") 
            base_url = f"https://api.spotify.com/v1/search?q={constructed_query}&type={type}&limit=1&offset={offset}"
            request = loads(dumps(requests.get(base_url, headers=headers).json()))
            if type == "artist":
                items = request["artists"]["items"][0]
                return self.__parse_artist(items)
            elif type == "album":
                items = request["albums"]["items"][0]
                return self.__parse_album(items)
            elif type == "track":
                items = request["tracks"]["items"][0]
                return self.__parse_track(items)
        else:
            raise AuthenticationError("Could not be authenticated.")

    def __parse_artist(self, items) -> Artist:
        return Artist(
            url = items["external_urls"]["spotify"],
            followers= items["followers"]["total"],
            genres = items["genres"],
            id = items["id"],
            name = items["name"],
            popularity=items["popularity"]
        )
    def __parse_album(self, items) -> Album:
        artists = items["artists"]
        artist_list = [] 
        for artist in artists:
            art = Artist(
                url = artist["external_urls"]["spotify"],
                id = artist["id"],
                name = artist["name"],
                followers = None,
                genres = None, 
                popularity= None
            )
            artist_list.append(art)
        return Album(
            artists = artist_list,
            id = items["id"],
            release= items["release_date"],
            total_tracks= items["total_tracks"],
            name = items["name"],
            url = items["external_urls"]["spotify"]
        )
    def __parse_track(self, items):
        album_data = items["album"]
        album = Album(
            artists = None, 
            id = album_data["id"],
            release= album_data["release_date"],
            total_tracks= album_data["total_tracks"],
            name = album_data["name"],
            url = album_data["external_urls"]["spotify"]
        ) 
        artists = items["artists"]
        artist_list = [] 
        for artist in artists:
            art = Artist(
                url = artist["external_urls"]["spotify"],
                id = artist["id"],
                name = artist["name"],
                followers = None,
                genres = None, 
                popularity= None
            )
            artist_list.append(art)
        return Track(
            name = items["name"], 
            url = items["external_urls"]["spotify"],
            id = items["id"],
            artists= artist_list,
            album = album,
            explicit = items["explicit"],
            duration= items["duration_ms"],
            popularity= items["popularity"],
            track_number = items["track_number"]
        )


