"""
Current module contains functions for working with information
related to artist. Searching, getting albums.
Functions are using audioscrobbler API.
Last update: 27.06.2015
"""
from urllib.request import *
import http.client
from requestHeaderConstructor import *
import json
import time
import re

__author__ = 'aleksandrlazarenko'

# General root for requests
APIRoot = 'ws.audioscrobbler.com'   # last fm API root path
VKApiRoot = 'api.vk.com'            # VK API root path

# To establish connection connection = http.client.HTTPConnection(APIRoot)


"""
Function finds information about artists
API method: artist.search
API method URL: http://www.lastfm.ru/api/show/artist.search
input: name of the artist
output: all found artists
"""
def find_artists(artist_name, connection):
    # TODO: refactor it
    api_sub_root = construct_find_artist_req_str(artist_name)           # getting sub root
    connection.request('GET', api_sub_root)                             # making request
    response = connection.getresponse()                                 # getting response
    byte_data_about_artist = response.read()                            # reading response
    json_data_about_artist = byte_data_about_artist.decode('utf-8')     # getting string from bytes
    parsed_data = json.loads(json_data_about_artist)                    # parsing json
    artists = parsed_data['results']['artistmatches']['artist']         # getting list of artists
    artists_names = []
    for artist in artists:
        artists_names.append(artist['name'])
    return artists_names                                                     # sending to caller


"""
Function finds all albums of artist
API method: artist.getTopAlbums
API method URL: http://www.lastfm.ru/api/show/artist.getTopAlbums
input: name of artist
output: related albums
"""
def find_albums(artist_name, connection):
    # TODO: refactor it
    api_sub_root = construct_find_albums_req_string(artist_name)        # getting sub root
    connection.request('GET', api_sub_root)                             # making request
    response = connection.getresponse()                                 # getting response
    byte_data_about_albums = response.read()                            # reading response
    json_data_about_albums = byte_data_about_albums.decode('utf-8')     # getting string from bytes
    parsed_data = json.loads(json_data_about_albums)                    # parsing json
    albums = parsed_data['topalbums']['album']                          # getting list of albums
    album_names = []
    for album in albums:
        album_names.append(album['name'])
    return album_names                                                      # sending to caller

"""
Function finds all tracks in album
API method: album.getInfo
API method URL: http://www.lastfm.ru/api/show/album.getInfo
input: name of album
output: list of tracks
"""
def get_tracks_from_album(artist_name, album_name, connection, status_handler):
    # TODO: refactor it
    api_sub_root = construct_get_album_tracks_req_string(artist_name, album_name)       # getting sub root
    connection.request('GET', api_sub_root)                                             # making request
    response = connection.getresponse()                                                 # getting response
    byte_data_about_tracks = response.read()                                            # reading response
    json_data_about_tracks = byte_data_about_tracks.decode('utf-8')                     # getting string from bytes
    parsed_data = json.loads(json_data_about_tracks)                                    # parsing json
    tracks = parsed_data['album']['tracks']['track']                                    # getting list of tracks
    img_url = parsed_data['album']['image'][2]['#text']
    try:
        info = parsed_data['album']['wiki']['summary']
    except:
        info = 'No any information...'
    tracks_names = []
    progress = 0
    tick = int((1 / tracks.__len__()) * 100)
    for track in tracks:
        try:
            track_to_append = track['name']
        except TypeError: # in case of bullshit (1 song in alb)
            track_to_append = 'Unable to find info about this song'
            break
        if '/' in track_to_append:
            track_to_append = track_to_append.replace('/', '')
        tracks_names.append(track_to_append)
        status_handler('Song {} collected'.format(track_to_append), progress)
        progress += tick
    return tracks_names, img_url, info

"""
Gets urls of tracks from VK
API method: audio.search
API method URL: https://vk.com/dev/audio.search
input author, listOfNames, token
output: list of urls for uploading
"""
def get_urls_of_tracks_for_downloading(author, list_of_names, token, handler):
    # TODO: refactor it
    # TODO: should return dictionary here {song_name : link_for_uploading)
    upload_dict = {}                                                         # list for urs
    connection = http.client.HTTPSConnection(VKApiRoot)                                   # opening connection
    progress = 0
    max_progress = list_of_names.__len__()
    tick = int((1 / max_progress) * 100)

    for track in list_of_names:                                                           # go foreach song in album
        handler('getting links', progress)
        progress += tick
        request_string = construct_get_search_vk_audio_string(author, track, token)       # constructing request
        connection.request('GET', request_string)                                         # making request
        response = connection.getresponse()                                               # getting response
        byte_tracks = response.read()                                                     # reading bytes from response
        json_tracks = byte_tracks.decode('utf-8')                                         # decoding
        parsed_tracks = json.loads(json_tracks)                                           # parsing json

        # handling empty search result (reason = son_name (fucking best version mafckc)
        if parsed_tracks['response'] == [0]:
            track = re.sub(r'\([^)]*\)', '', track).strip()
            request_string = construct_get_search_vk_audio_string(author, track, token)       # constructing request
            connection.request('GET', request_string)                                         # making request
            response = connection.getresponse()                                               # getting response
            byte_tracks = response.read()                                                     # reading bytes from response
            json_tracks = byte_tracks.decode('utf-8')                                         # decoding
            parsed_tracks = json.loads(json_tracks)

        if parsed_tracks['response'] != [0]:
            upload_dict[track] = parsed_tracks['response'][1]['url']
        time.sleep(1)                                                                     # waiting for a second
    connection.close()                                                                    # closing connection
    return upload_dict                                                                  # returning links

