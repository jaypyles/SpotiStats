class SpotifyObject():
    """
    Basic class representing all types from Spotify
    """
    def __init__(self) -> None:
        self.id = None
        self.name = None
        self.url = None

class Song(SpotifyObject):
    pass
class Artist(SpotifyObject):
    def __init__(self) -> None:
        self.genres = None
        self.followers = None
        self.popularity = None
        super().__init__()

    def __repr__(self):
        return self.name
class Track(SpotifyObject):
    pass

class Album(SpotifyObject):
    def __init__(self) -> None:
        self.artists = []
        self.release = None
        self.total_tracks = None
        super().__init__()
class Search():
    pass
