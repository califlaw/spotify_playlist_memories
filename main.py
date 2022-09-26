from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]


print("Which year do you want to travel to? YYYY-mm-dd format")
year = input("Year?: ")
month = input("Month?: ")
day = input("Day?: ")
date = f"{year}-{month}-{day}"

url = f'https://www.billboard.com/charts/hot-100/{date}/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
song_headings = [x.getText().strip() for x in soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")]
song_names = [x.getText().strip() for x in soup.find_all(name="span", class_="a-no-trucate")]
song_uris = []

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Sk2ipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)


