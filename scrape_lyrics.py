from bs4 import BeautifulSoup
import requests

def scrape ():
    l = []

    lyricheaders = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    query = "perfect one direction lyrics"

    url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8'

    request = requests.get(url, headers=lyricheaders)

    lyrics = ""

    lyrics_paragraph = BeautifulSoup(request.text, "html.parser").find_all("div", {"jsname": "U8S5sf"})

    for para in lyrics_paragraph:
        if BeautifulSoup(str(para), "html.parser").find("div", {"class": "rGtH5c"}) is not None:
            continue

        lyrics_line = BeautifulSoup(str(para), "html.parser").find_all("span", {"jsname": "YS01Ge"})

        for line in lyrics_line:
            lyrics = f"{lyrics}\n{line.text}"

        lyrics = f"{lyrics}<br>"

    return lyrics


if __name__ == "__main__":
    print(scrape())