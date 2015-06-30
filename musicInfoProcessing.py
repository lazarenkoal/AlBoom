"""
Current module contains functions for working with information
related to artist. Searching, getting albums.
Functions are using audioscrobbler API.
Last update: 29.06.2015
"""
from urllib.request import *
import http.client
from requestHeaderConstructor import *
import json
import time
import re
from tkinter import messagebox


__author__ = 'aleksandrlazarenko'

# General root for requests
APIRoot = 'itunes.apple.com'        # ITunes API root path
VKApiRoot = 'api.vk.com'            # VK API root path

# To establish connection connection = http.client.HTTPConnection(APIRoot)


"""
Function finds information about artists
API method: artist.search
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
    artists = parsed_data['results']                                    # getting list of artists
    return artists                                                      # sending to caller


"""
Function finds all albums of artist
API method: artist.getTopAlbums
API method URL: http://www.lastfm.ru/api/show/artist.getTopAlbums
input: name of artist
output: related albums
"""
def find_albums(artist_id, connection):

    api_sub_root = construct_find_albums_req_string(artist_id)          # getting sub root
    connection.request('GET', api_sub_root)                             # making request
    response = connection.getresponse()                                 # getting response
    byte_data_about_albums = response.read()                            # reading response
    json_data_about_albums = byte_data_about_albums.decode('utf-8')     # getting string from bytes
    parsed_data = json.loads(json_data_about_albums)                    # parsing json
    print(parsed_data)
    albums = parsed_data['results']                                     # getting list of albums
    return albums                                               # sending to caller

"""
Function finds all tracks in album
API method: album.getInfo
API method URL: http://www.lastfm.ru/api/show/album.getInfo
input: name of album
output: list of tracks
"""
def get_tracks_from_album(album_id, connection, status_handler):

    api_sub_root = construct_get_album_tracks_req_string(album_id)                      # getting sub root
    connection.request('GET', api_sub_root)                                             # making request
    response = connection.getresponse()                                                 # getting response
    byte_data_about_tracks = response.read()                                            # reading response
    json_data_about_tracks = byte_data_about_tracks.decode('utf-8')                     # getting string from bytes
    parsed_data = json.loads(json_data_about_tracks)                                    # parsing json
    songs = parsed_data['results'] 
    return songs

"""
Gets urls of tracks from VK
API method: audio.search
API method URL: https://vk.com/dev/audio.search
input author, listOfNames, token
output: list of urls for uploading
"""
def get_urls_of_tracks_for_downloading(author, tracks, token, handler):
    # TODO: refactor it
    # TODO: should return dictionary here {song_name : link_for_uploading)
    upload_dict = {}                                                                          # list for urs
    connection = http.client.HTTPSConnection(VKApiRoot)                                       # opening connection
    progress = 0
    max_progress = len(tracks)
    tick = int((1 / max_progress) * 100)
    try:
        for track, i in zip(tracks, range(0, len(tracks), 1)):                           # go foreach song in album
            handler('getting links', progress)
            progress += tick
            track_name = track['trackName']
            request_string = construct_get_search_vk_audio_string(author['artistName'], track_name, token)       # constructing request
            connection.request('GET', request_string)                                         # making request
            response = connection.getresponse()                                               # getting response
            byte_tracks = response.read()                                                     # reading bytes from response
            json_tracks = byte_tracks.decode('utf-8')                                         # decoding
            parsed_tracks = json.loads(json_tracks)                                           # parsing json

            print(parsed_tracks)
            # handling empty search result (reason = son_name (fucking best version mafckc)
            if parsed_tracks['response'] == [0]:
                track_name = re.sub(r'\([^)]*\)', '', track['trackName']).strip() # deleting fucking (()) in title
                request_string = construct_get_search_vk_audio_string(author['artistName'], track_name, token)       # constructing request
                connection.request('GET', request_string)                                         # making request
                response = connection.getresponse()                                               # getting response
                byte_tracks = response.read()                                                     # reading bytes from response
                json_tracks = byte_tracks.decode('utf-8')                                         # decoding
                parsed_tracks = json.loads(json_tracks)

            if parsed_tracks['response'] != [0]:
                tracks[i]['trackUrl'] = parsed_tracks['response'][1]['url']
            time.sleep(1)
    except KeyError:
        messagebox.showerror('Token expired', 'I will fill in new token!')
        # TODO: use special function for gettin new token
    connection.close()                                                                    # closing connection
    return tracks                                                                # returning links

