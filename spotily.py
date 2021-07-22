import requests
from get_lyrics import *
from graphics import *
import time
from artist_translation import translate_name
import artist_translation


SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = 'BQCdYK9TMLuASz-A2S5ziCw7BaAY-ogOCa_cFBzCmvPr2nrQk_zGx6993osxUf0wYFuYGP4YhoEfVrfwur2p3zH0IOWQNU_3AsiVeuEiZHo4DfjvwdXbhCadgonfehUcD6Lf7hudI8TMxesAx3LeKg_DMkJTneK4NhoLUoUL'


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    if response.status_code != 200:
        return {'id': -1 if response.status_code == 401 else -2 }

    json_resp = response.json()

    track_id = json_resp['item']['id']
    track_name = json_resp['item']['name']
    artists = [artist for artist in json_resp['item']['artists']]

    link = json_resp['item']['external_urls']['spotify']

    artist_names = ', '.join([artist['name'] for artist in artists])

    current_track_info = {
        "id": track_id,
        "track_name": track_name,
        "artists": artist_names,
        "link": link
    }

    return current_track_info


def remove_not_relevant(name, char):
    if char in name:
        return name[:name.find(char)]
    return name


def change_lyrics(scrollwindow):
    song_id = None
    while True:
        current_track_info = get_current_track(ACCESS_TOKEN)
        if current_track_info['id'] == -1:
            scrollwindow.set_lines('Token Refresh Needed', ["Looks like you need a Spotify Token Refresh"])
            song_id = -1
        elif current_track_info['id'] == -2:
            scrollwindow.set_lines('No Song Playing', ["There is no song currently Playing :)"])
            song_id = -1
        elif current_track_info['id'] != song_id:

            song_name = str(current_track_info['track_name'])
            song_name = remove_not_relevant(song_name, '-')
            song_name = remove_not_relevant(song_name, ' (')

            artist = current_track_info['artists']
            artist_org = artist
            is_english = song_name[0] not in artist_translation.abc
            if not is_english:
                artist = translate_name(artist)

            lyrics = get_lyrics2(song_name, artist, is_english)
            if not valid(lyrics):
                query = str(artist_org) + " " + song_name
                lyrics = get_lyrics(query)['lyrics']

            title = song_name + ' \ ' + str(artist)
            lines = lyrics.split('\n')
            lines.insert(0, "-- " + title + " --\n")
            scrollwindow.set_lines(title, lines)
            song_id = current_track_info['id']

        time.sleep(5)


s = ScrollWindow2()
s.start(lambda: change_lyrics(s))





