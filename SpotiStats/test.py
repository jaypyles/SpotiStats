from dotenv import load_dotenv
import os
from SpotiStats.spotify import *
load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"] 
CLIENT_SECRET = os.environ["CLIENT_SECRET"] 

auth = Authenticator(CLIENT_ID, CLIENT_SECRET)
spot = Spotify(auth)
album = spot.search("radiohead", "track")
print(album)
