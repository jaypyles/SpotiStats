import webbrowser
import click
from dotenv import load_dotenv
import os
from webbrowser import open

from SpotiStats.spotify import Authenticator, Spotify

load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
auth = Authenticator(CLIENT_ID, CLIENT_SECRET)
spotify = Spotify(auth)

@click.group()
def cli():
    pass

@cli.command()
def info():
    print("Info command")

@cli.command()
@click.option('-a', '--artist', 'option', flag_value='artist', help="Search for Spotify artist")
@click.option('-t', '--track', 'option', flag_value='track', default=True, help="Search for Spotify song")
@click.option('-al', '--album', 'option', flag_value='album', help="Search for Spotify album")
@click.option('-o', '--open', 'open', flag_value='open', help="Open Spotify link")
@click.argument('query')
def search(option, query, open):
    searched_term = spotify.search(query, option)
    print(searched_term)
    if open and searched_term is not None:
        url = searched_term.url
        webbrowser.open(url)

if __name__ == "__main__":
    cli()
