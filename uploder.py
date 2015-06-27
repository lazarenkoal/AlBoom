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
def upload_songs(artist, album, song_links):
    print('Выберете директорию для сохранения')

    # opening fucking dialog
    file_path = filedialog.askdirectory()

    # generating name for folder Ex: Desktop/Green Day - American Idiot
    folder_directory = file_path + '/' + artist + ' - ' + album

    # creating folder
    # TODO: check if directory exists!!!
    makedirs(folder_directory)

    # download every fucking song from dict
    for song in song_links.keys():
        print('Загружаю песню', song)

        # making directory Ex: Desktop/Green Day - American Idiot/American Idiot.mp3
        if '/' in song:
            song = song.replace('/', '')
        song_name = folder_directory + '/' + song + '.mp3'

        # uploading
        urllib.request.urlretrieve(song_links[song], song_name)
        print('Песня загружена')

"""
Prepares dict with songs names and links
input: name of the artist, list of tracks for uploading, token
output: dictionary for upload songs method
"""
def make_dict_for_downloading(artist_name, tracks, token):
    tracks_urls = get_urls_of_tracks_for_downloading(artist_name, tracks, token)
    links = []
    for track in tracks_urls:
        try:
            links.append(track['response'][1]['url'])
            print(track['response'][1]['url'])
        except:
            continue
    songs_with_links = dict(zip(tracks, links))
    return songs_with_links

