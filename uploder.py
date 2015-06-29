"""
Current module serves as music uploader
:)
"""
from os import makedirs
import urllib
from mutagen.mp3 import EasyMP3 as MP3
"""
Uploads song to the directory, which is made for album
input: artists name, album, dictionary with links ({song-name : link})
"""
def upload_songs(artist, album, song_links, file_path, status_handler):

    # Generating name for folder Ex: Desktop/Green Day - American Idiot
    folder_directory = file_path + '/' + artist + ' - ' + album

    # Creating folder
    # TODO: check if directory exists!!!
    makedirs(folder_directory)

    progress = 0
    tick = int((1 / len(song_links)) * 100)

    # Download every fucking song from dict
    for song in song_links.keys():
        status_handler('Downloading song: ' + song, progress)
        # Making directory Ex: Desktop/Green Day - American Idiot/American Idiot.mp3
        if '/' in song:
            song = song.replace('/', '')
        song_name = folder_directory + '/' + song + '.mp3'

        # Uploading
        urllib.request.urlretrieve(song_links[song][1], song_name)

        # Metadata correction
        metadata = MP3(song_name)
        metadata['album'] = album
        metadata['tracknumber'] = str(song_links[song][0])
        metadata['artist'] = artist
        metadata.save()
        status_handler('Song uploaded', progress)
        progress += tick

    status_handler('Uploading completed', 100)


