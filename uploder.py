"""
Current module serves as music uploader
:)
"""
from tkinter import filedialog
from os import makedirs
import urllib
from musicInfoProcessing import get_urls_of_tracks_for_downloading
"""
Uploads song to the directory, which is made for album
input: artists name, album, dictionary with links ({song-name : link})
"""
def upload_songs(artist, album, song_links, file_path, status_handler):
    status_handler('Please, choose directory for saving album', 0)

    # generating name for folder Ex: Desktop/Green Day - American Idiot
    folder_directory = file_path + '/' + artist + ' - ' + album

    # creating folder
    # TODO: check if directory exists!!!
    makedirs(folder_directory)

    progress = 0
    tick = int((1 / song_links.keys().__len__()) * 100)
    # download every fucking song from dict
    for song in song_links.keys():
        status_handler('Downloading song: ' + song, progress)
        # making directory Ex: Desktop/Green Day - American Idiot/American Idiot.mp3
        if '/' in song:
            song = song.replace('/', '')
        song_name = folder_directory + '/' + song + '.mp3'

        # uploading
        urllib.request.urlretrieve(song_links[song], song_name)
        status_handler('Song uploaded', progress)
        progress += tick
    status_handler('Uploading completed', 100)

"""
Prepares dict with songs names and links
input: name of the artist, list of tracks for uploading, token, function for displaying status
output: dictionary for upload songs method
"""
def make_dict_for_downloading(artist_name, tracks, token, status_handler):
    status_handler('Beginning to collect links', 0)
    tracks_urls = get_urls_of_tracks_for_downloading(artist_name, tracks, token, status_handler)
    status_handler('Links collected. Beginning to prepare information for downloading', 0)
    links = []
    tick = int((1 / tracks_urls.__len__()) * 100)
    progress = 0
    for track in tracks_urls:
        try:
            progress += tick
            status_handler('parsing respond', progress)
            links.append(track['response'][1]['url'])
        except:
            continue
    songs_with_links = dict(zip(tracks, links))
    status_handler('Preparation finished. Ready for downloading', 100)
    return songs_with_links

