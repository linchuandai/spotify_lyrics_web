from bs4 import BeautifulSoup
import requests
import spotify_token as st
from datetime import datetime
import time
import json

def scrape (song_name, song_artist):

    # used only for testing so we don't continually have to call spotify api
    if not song_name and not song_artist:
        query = f"say you wont let go James Arthur lyrics"
        lyrics = "Say you wont let go James Arthur"

    else:
        query = f"{song_name} {song_artist} lyrics"
        lyrics = f"{song_name} {song_artist}"

    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + 'O-a11WJg5nnCfmtkbvPxWO1Z7d7Q8a2YbEZg0RG7nVfW859_JuHAs9wWFk3uQNDt'}
    search_url = base_url + '/search'
    data = {'q': song_name + ' ' + song_artist}
    response = requests.get(search_url, data=data, headers=headers)

    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if song_artist.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    if remote_song_info:
        song_url = remote_song_info['result']['url']
    else: 
        return ['Song not found']

    page = requests.get(song_url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics_paragraph = html.find('div', class_='lyrics').get_text()

    lyricsArr = lyrics_paragraph.split('\n')
    lyricsArr[0] = lyrics

    return lyricsArr

def getSong(token):
    spotheaders = {'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    artist = ""
    song = ""

    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=spotheaders)
    if response.status_code != 200:
        return response.status_code

    else:
        json_data = json.loads(response.text)
        artist = json_data["item"]["artists"][0]["name"]
        if song != json_data["item"]["name"]:
            song = json_data["item"]["name"]

    return scrape(song, artist)

# here for testing this function with terminal, probably remove later
def getSongWithUser(user, passw):
    token = None
    if token is None or token_exp < datetime.now():
        data = st.start_session(user, passw)
        token = data[0]
        token_exp = data[1]

    spotheaders = {'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    artist = ""
    song = ""

    # TODO: Handle more errors (such as 204)
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=spotheaders)
    if response.status_code != 200:
        print(response.status_code)
        print("Bad Response from Spotify API")

    else:
        json_data = json.loads(response.text)
        artist = json_data["item"]["artists"][0]["name"]
        if song != json_data["item"]["name"]:
            song = json_data["item"]["name"]

    return scrape(song, artist)

if __name__ == "__main__":

    # while True:
    for line in scrape('Payphone', 'Maroon 5'):
        print(line)
        # time.sleep(3)
