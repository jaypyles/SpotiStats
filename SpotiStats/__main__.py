import webbrowser
import click
from dotenv import load_dotenv
from SpotiStats.utils import generate_authorization_token, search_spotify, authenticate
import os

load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

result = generate_authorization_token(CLIENT_ID, CLIENT_SECRET)
token, response_code = result[0], result[1]

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
@click.argument('query')
@authenticate(response_code)
def search(option, query):
    if not query:
        print("Error: Query is required.")
        return
    print(f"Searching for: {query}")
    if (search := search_spotify(query, option, 0, token)):
        print("-- Search Results --")
        for key, item in search.items():
            if option == "artist":
                print(f"{key}: {item.name} - ID:{item.id}")
            elif option == "album":
                print(f"{key}: {item.artists} {item.name} - ID:{item.id}")
        open = input("Open Spotify link? (Y/N)")
        if open != "Y":
            return
        else:
            choice = input("Pick option: ")
            if(picked := search.get(int(choice))):
                if(url := picked.url):
                    webbrowser.open(url)
            else:
                print(f"No option with choice: {choice}")

if __name__ == "__main__":
    cli()
