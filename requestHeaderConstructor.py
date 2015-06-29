"""
Current module have functions for generating request strings
and other useful things.
:)

Last update: 29.06.2015
"""
from urllib.parse import urlencode

__author__ = 'aleksandrlazarenko'

# Api version and app credential
APIVersion = '/2.0/?'
APIKey = 'fd7e3140266c89c8912cd7f632abc289'

# constructing request string for artist search
def construct_find_artist_req_str(artist_name):
    query = urlencode({'method': 'artist.search', 'artist': artist_name, 'api_key': APIKey,
                       'format': 'json'})
    return APIVersion + query


# constructing request string for album search
def construct_find_albums_req_string(artist_name):
    query = urlencode({'method': 'artist.gettopalbums', 'artist': artist_name, 'api_key':
        APIKey, 'format': 'json'})
    return APIVersion + query


# constructing request string for list of tracks
def construct_get_album_tracks_req_string(artist_name, album_name):
    query = urlencode({'method': 'album.getinfo', 'api_key': APIKey, 'artist': artist_name,
                       'album': album_name, 'format': 'json'})
    return APIVersion + query


# constructing vk song search request
def construct_get_search_vk_audio_string(artist_name, track_name, token):
    q = '/method/audio.search?'
    query = urlencode({'q': artist_name + ' ' + track_name, 'count': 1, 'access_token': token})
    return q + query
