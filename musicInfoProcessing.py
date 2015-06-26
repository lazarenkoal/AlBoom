"""
Current module contains functions for working with information
related to artist. Searching, getting albums.
Functions are using audioscrobblet API.
Last update: 26.06.2015
"""
from urllib.request import *
import http.client
from requestHeaderConstructor import *
import json
import time

__author__ = 'aleksandrlazarenko'

# General root for requests
APIRoot = 'ws.audioscrobbler.com'
VKApiRoot = 'api.vk.com'

"""
Function finds information about artists
API method: artist.search
API method URL: http://www.lastfm.ru/api/show/artist.search
input: name of the artist
output: all found artists
"""
def find_artists(artist_name):
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
outut: list of urls for uploading
"""
def get_urls_of_tracks_for_downloading(author, listOfNames, token):
    listOfUrls = []                                                             # list for urs
    connection = http.client.HTTPSConnection(VKApiRoot)                         # opening connection
    for track in listOfNames:                                                   # go foreach song in album
        str = constrict_get_search_vk_audio_string(author, track, token)        # constructing request for each song
        connection.request('GET', str)                                          # making request
        response = connection.getresponse()                                     # getting response
        bytetracks = response.read()                                            # reading bytes from response
        jsontracks = bytetracks.decode('utf-8')                                 # decoding
        parsed = json.loads(jsontracks)                                         # parsing json
        listOfUrls.append(parsed)                                               # taking link
        time.sleep(1)                                                           # waiting for a second
    connection.close()                                                          # closing connection
    return listOfUrls                                                           # returning links
