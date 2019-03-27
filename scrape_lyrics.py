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

    query = "Perfect One Direction lyrics"

    url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8'

    request = requests.get(url, headers=lyricheaders)

    soup = BeautifulSoup(request.text, "html.parser").find_all("span", {"jsname": "YS01Ge"})

    print (soup)

    lyrics = ""

    for link in soup:
        lyrics = f"{lyrics}\n{link.text}"

    # print (lyrics)
    return lyrics


if __name__ == "__main__":
    print(scrape())