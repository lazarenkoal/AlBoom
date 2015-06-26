"""
Current module have functions for generating request strings
and other useful things.
:)

Last update: 26.06.2015
"""
__author__ = 'aleksandrlazarenko'

# Api version and app credential
APIVersion = '/2.0/?'
APIKey = 'fd7e3140266c89c8912cd7f632abc289'

# constructing request string for artist search
def construct_find_artist_req_str(artist_name):
    if ' ' in artist_name:
        artist_name = artist_name.replace(' ', '+')
    return (APIVersion + 'method=artist.search&artist=' + artist_name
            + '&api_key=' + APIKey + '&format=json')

# constructing request string for album search
def construct_find_albums_req_string(artist_name):
    if ' ' in artist_name:
        artist_name = artist_name.replace(' ', '+')
    return  (APIVersion + 'method=artist.gettopalbums&artist=' + artist_name +
              '&api_key=' + APIKey + '&format=json')

# constructing request string for list of tracks
def construct_get_album_tracks_req_string(artist_name, album_name):
    if ' ' in artist_name:
        artist_name = artist_name.replace(' ', '+')
    if ' ' in album_name:
        album_name = album_name.replace(' ', '+')
    return  (APIVersion + 'method=album.getinfo&api_key=' + APIKey + '&artist=' +
    artist_name + '&album=' + album_name + '&format=json')

def constrict_get_search_vk_audio_string(artist_name, track_name, token):
    if ' ' in artist_name:
        artist_name = artist_name.replace(' ', '+')
    if ' ' in track_name:
        track_name = track_name.replace(' ', '+')
    return ('/method/audio.search?q='+artist_name+'+'+track_name+'&count=1&access_token='+ token)