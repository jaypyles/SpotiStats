from dotenv import load_dotenv
import json
from SpotiStats.utils import generate_authorization_token, search_spotify
import os
import requests
load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"] 
CLIENT_SECRET = os.environ["CLIENT_SECRET"] 

token = generate_authorization_token(CLIENT_ID, CLIENT_SECRET)

response = search_spotify("Tame Impala", "artist", token)
print(response)
