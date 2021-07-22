from lyrics_extractor import SongLyrics
import lyrics_extractor
import requests
from bs4 import BeautifulSoup


GCS_API_KEY = 'AIzaSyBP8mqrzp4cpwKLzq-bYXs70GRuHBttGXg'
GCS_ENGINE_ID = '560b796bf72587c16'


def get_lyrics(song_name):
    extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)

    try:
        lyrics = extract_lyrics.get_lyrics(song_name)
    except lyrics_extractor.lyrics.LyricScraperException:
        return {'title': 'Unknown song',
                'lyrics': "Can't find lyrics for '" + song_name + "' :("}
    return lyrics


def get_lyrics2(song_name, artist, english=True):
    query = (song_name + " " + artist + (" lyrics" if english else " מילים")).lower()
    query = "https://www.google.com/search?q=" + '%20'.join(query.split(' '))
    page = requests.get(query)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('span', dir='ltr')
    start = 1 if artist + "</" not in str(results[1]) else 2 # which span to start from
    lyrics = ''.join(str(res) for res in results[start:start + 2])[16:]\
        .replace("</span>", "").replace('<span dir="ltr">', '\n')
    return lyrics


def valid(lyrics):
    invalids = ['genius', 'musixmatch', 'lyricstranslate.com', 'youtube', 'shironet', 'tab4u']
    lower_lyrics = lyrics.lower()
    for invalid in invalids:
        if invalid in lower_lyrics:
            return False
    return True
