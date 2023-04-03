import click
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]


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
def search(option, query):
    pass
if __name__ == "__main__":
    cli()
