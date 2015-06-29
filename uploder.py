"""
Current module serves as music uploader
:)
"""
from os import makedirs
import urllib
"""
Uploads song to the directory, which is made for album
input: artists name, album, dictionary with links ({song-name : link})
"""
def upload_songs(artist, album, song_links, file_path, status_handler):

    # generating name for folder Ex: Desktop/Green Day - American Idiot
    folder_directory = file_path + '/' + artist + ' - ' + album

    # creating folder
    # TODO: check if directory exists!!!
    makedirs(folder_directory)

    progress = 0
    tick = int((1 / len(song_links)) * 100)

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


