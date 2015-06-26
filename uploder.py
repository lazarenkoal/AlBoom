"""
Current module serves as music uploader
:)
"""
from tkinter import filedialog
from os import makedirs
import urllib

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
        song_name = folder_directory + '/' + song + '.mp3'

        # uploading
        urllib.request.urlretrieve(song_links[song], song_name)
        print('Песня загружена')
