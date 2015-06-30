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
def upload_songs(artist, album, tracks, file_path, status_handler):

    # Generating name for folder Ex: Desktop/Green Day - American Idiot
    folder_directory = file_path + '/' + artist['artistName'] + ' - ' + album['collectionName']

    # Creating folder
    # TODO: check if directory exists!!!
    makedirs(folder_directory)

    progress = 0
    print(tracks)
    tick = int((1 / len(tracks)) * 100)

    # Download every fucking track from dict
    for track in tracks:
        status_handler('Downloading track: ' + track['trackName'], progress)
        # Making directory Ex: Desktop/Green Day - American Idiot/American Idiot.mp3
        song_name = folder_directory + '/' + track['trackName'] + '.mp3'

        # Uploading
        print(track)
        urllib.request.urlretrieve(track['trackUrl'], song_name)

        # Metadata correction
        metadata = MP3(song_name)
        metadata.delete()
        metadata['Album'] = track['collectionName']
        metadata['Composer'] = track['artistName']
        metadata['Title'] = track['trackName']
        metadata['Artist'] = track['artistName']
        metadata['tracknumber'] = str(track['trackNumber'])
        metadata['date'] = track['releaseDate']
        metadata['genre'] = track['primaryGenreName']
        metadata['performer'] = track['artistName']

        metadata.update()
        metadata.save()
        status_handler('Song uploaded', progress)
        progress += tick

    status_handler('Uploading completed', 100)


