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

__author__ = 'aleksandrlazarenko'

# General root for requests
APIRoot = 'ws.audioscrobbler.com'   # last fm API root path
VKApiRoot = 'api.vk.com'            # VK API root path

"""
Function finds information about artists
API method: artist.search
API method URL: http://www.lastfm.ru/api/show/artist.search
input: name of the artist
output: all found artists
"""
def find_artists(artist_name):
    # TODO: refactor it
    connection = http.client.HTTPConnection(APIRoot)                    # opening connection
    api_sub_root = construct_find_artist_req_str(artist_name)           # getting sub root
    connection.request('GET', api_sub_root)                             # making request
    response = connection.getresponse()                                 # getting response
    byte_data_about_artist = response.read()                            # reading response
    json_data_about_artist = byte_data_about_artist.decode('utf-8')     # getting string from bytes
    connection.close()                                                  # closing connection
    parsed_data = json.loads(json_data_about_artist)                    # parsing json
    artists = parsed_data['results']['artistmatches']['artist']         # getting list of artists
    return artists                                                      # sending to caller


"""
Function finds all albums of artist
API method: artist.getTopAlbums
API method URL: http://www.lastfm.ru/api/show/artist.getTopAlbums
input: name of artist
output: related albums
"""
def find_albums(artist_name):
    # TODO: refactor it
    connection = http.client.HTTPConnection(APIRoot)                    # opening connection
    api_sub_root = construct_find_albums_req_string(artist_name)        # getting sub root
    connection.request('GET', api_sub_root)                             # making request
    response = connection.getresponse()                                 # getting response
    byte_data_about_albums = response.read()                            # reading response
    json_data_about_albums = byte_data_about_albums.decode('utf-8')     # getting string from bytes
    connection.close()                                                  # closing connection
    parsed_data = json.loads(json_data_about_albums)                    # parsing json
    albums = parsed_data['topalbums']['album']                          # getting list of albums
    return albums                                                       # sending to caller

"""
Function finds all tracks in album
API method: album.getInfo
API method URL: http://www.lastfm.ru/api/show/album.getInfo
input: name of album
output: list of tracks
"""
def get_tracks_from_album(artist_name, album_name):
    # TODO: refactor it
    connection = http.client.HTTPConnection(APIRoot)                                    # opening connection
    api_sub_root = construct_get_album_tracks_req_string(artist_name, album_name)       # getting sub root
    connection.request('GET', api_sub_root)                                             # making request
    response = connection.getresponse()                                                 # getting response
    byte_data_about_tracks = response.read()                                            # reading response
    json_data_about_tracks = byte_data_about_tracks.decode('utf-8')                     # getting string from bytes
    connection.close()                                                                  # closing connection
    parsed_data = json.loads(json_data_about_tracks)                                    # parsing json
    tracks = parsed_data['album']['tracks']['track']                                    # getting list of tracks
    return tracks

"""
Gets urls of tracks from VK
API method: audio.search
API method URL: https://vk.com/dev/audio.search
input author, listOfNames, token
output: list of urls for uploading
"""
def get_urls_of_tracks_for_downloading(author, list_of_names, token):
    # TODO: refactor it
    list_of_urls = []                                                                     # list for urs
    connection = http.client.HTTPSConnection(VKApiRoot)                                   # opening connection
    for track in list_of_names:                                                           # go foreach song in album
        request_string = construct_get_search_vk_audio_string(author, track, token)       # constructing request
        connection.request('GET', request_string)                                         # making request
        response = connection.getresponse()                                               # getting response
        byte_tracks = response.read()                                                     # reading bytes from response
        json_tracks = byte_tracks.decode('utf-8')                                         # decoding
        parsed_tracks = json.loads(json_tracks)                                           # parsing json
        list_of_urls.append(parsed_tracks)                                                # taking link
        time.sleep(1)                                                                     # waiting for a second
    connection.close()                                                                    # closing connection
    return list_of_urls                                                                   # returning links
