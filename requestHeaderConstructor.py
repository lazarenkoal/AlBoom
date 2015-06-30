"""
Current module have functions for generating request strings
and other useful things.
:)

Last update: 29.06.2015
"""
from urllib.parse import urlencode

__author__ = 'aleksandrlazarenko'

# constructing request string for artist search
def construct_find_artist_req_str(artist_name):
    query = urlencode({'term': artist_name, 'entity': 'musicArtist', 'format': 'json'})
    return '/search?' + query


# constructing request string for album search
def construct_find_albums_req_string(artist_id):
    query = urlencode({'id': artist_id, 'entity': 'album', 'format': 'json'})
    return '/lookup?' + query


# constructing request string for list of tracks
def construct_get_album_tracks_req_string(album_id):
    query = urlencode({'id': album_id, 'entity': 'song', 'format': 'json'})
    return '/lookup?' + query


# constructing vk song search request
def construct_vk_search_string(artist_name, track_name, token):
    q = '/method/audio.search?'
    query = urlencode({'q': artist_name + ' ' + track_name, 'count': str(1), 'access_token': token})
    print(q + query)
    return q + query + '&'

def construct_vk_search_string_with_captcha(artist_name, track_name, token, captcha_sid, captcha_key):
    q = construct_vk_search_string(artist_name, track_name,token)
    query = urlencode({'captcha_sid': str(captcha_sid), 'captcha_key': captcha_key})
    print(q+'&' + query)
    return  q + query
