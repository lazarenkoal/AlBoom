"""
Current module have functions for generating request strings
and other useful things.
:)

Last update: 27.06.2015
"""
# TODO: rewrite everything with native urlencode

__author__ = 'aleksandrlazarenko'

# Api version and app credential
APIVersion = '/2.0/?'
APIKey = 'fd7e3140266c89c8912cd7f632abc289'

# constructing request string for artist search
def construct_find_artist_req_str(artist_name):
    if ' ' in artist_name:
        artist_name = artist_name.replace(' ', u'+')
    return (APIVersion + u'method=artist.search&artist=' + artist_name
            + u'&api_key=' + APIKey + u'&format=json')


# constructing request string for album search
def construct_find_albums_req_string(artist_name):
    if ' ' in artist_name:
        artist_name = artist_name.replace(u' ', u'+')
    return (APIVersion + u'method=artist.gettopalbums&artist=' + artist_name +
            u'&api_key=' + APIKey + u'&format=json')


# constructing request string for list of tracks
def construct_get_album_tracks_req_string(artist_name, album_name):
    if ' ' in artist_name:
        artist_name = artist_name.replace(u' ', u'+')
    if ' ' in album_name:
        album_name = album_name.replace(u' ', u'+')
    return (APIVersion + u'method=album.getinfo&api_key=' + APIKey + u'&artist=' +
            artist_name + u'&album=' + album_name + u'&format=json')


# constructing vk song search request
def construct_get_search_vk_audio_string(artist_name, track_name, token):
    if ' ' in artist_name:                                                  # checking if artist contains whitespace
        artist_name = artist_name.replace(' ', u'+')                        # replacing by +
    if ' ' in track_name:                                                   # checking if trackName contains whitespace
        track_name = track_name.replace(' ', u'+')                          # replacing by +
    track_name = str(track_name.encode('ascii', 'ignore'))[2:-1]            # fucking magic, :D
    return (u'/method/audio.search?q=' + artist_name + u'+'                 # sending to caller
            + track_name + u'&count=1&access_token=' + token)
