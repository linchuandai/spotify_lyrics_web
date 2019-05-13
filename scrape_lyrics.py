from bs4 import BeautifulSoup
import requests
import spotify_token as st
from datetime import datetime
import time
import json


def scrape (song_name, song_artist):

    lyricheaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    # used only for testing so we don't continually have to call spotify api
    if not song_name and not song_artist:
        query = f"say you wont let go James Arthur lyrics"
        lyrics = "Say you wont let go James Arthur"

    else:
        query = f"{song_name} {song_artist} lyrics"
        lyrics = f"{song_name} {song_artist}"

    url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8'

    request = requests.get(url, headers=lyricheaders)

    lyricsArr = [lyrics]

    lyrics_paragraph = BeautifulSoup(request.text, "html.parser").find_all("div", {"jsname": "U8S5sf"})

    for para in lyrics_paragraph:
        # TO DO: find better way of removing the partially cut off paragraph
        if BeautifulSoup(str(para), "html.parser").find("div", {"class": "OULBYb"}) is not None:
            continue

        lyrics_line = BeautifulSoup(str(para), "html.parser").find_all("span", {"jsname": "YS01Ge"})

        for line in lyrics_line:
            lyrics = f"{lyrics}<br>{line.text}"
            lyricsArr.append(line.text)

        lyrics = f"{lyrics} <br>"
        lyricsArr.append('')

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
        print(response.status_code)
        print("Bad Response from Spotify API")

    else:
        json_data = json.loads(response.text)
        artist = json_data["item"]["artists"][0]["name"]
        if song != json_data["item"]["name"]:
            song = json_data["item"]["name"]

    return scrape(song, artist)

# here for testing this function with terminal, probably remove later
# def getSongWithUser(user, passw):
#     token = None
#     if token is None or token_exp < datetime.now():
#         data = st.start_session(user, passw)
#         token = data[0]
#         token_exp = data[1]

#     spotheaders = {'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {token}',
#     }

#     artist = ""
#     song = ""

#     response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=spotheaders)
#     if response.status_code != 200:
#         print(response.status_code)
#         print("Bad Response from Spotify API")

#     else:
#         json_data = json.loads(response.text)
#         artist = json_data["item"]["artists"][0]["name"]
#         if song != json_data["item"]["name"]:
#             song = json_data["item"]["name"]

#     return scrape(song, artist)

# if __name__ == "__main__":

#     while True:
#         print(getSongWithUser('', ''))
#         time.sleep(3)
