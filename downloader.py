"""
This module downloads tracks
"""
import os
from os import makedirs
import urllib
from mutagen.mp3 import EasyMP3 as MP3



"""
Uploads song to the directory, which is made for album
input: artists name, album, dictionary with links ({song-name : link})
"""
def download_songs(artist, album, tracks, file_path, status_handler):

    # Create folder
    folder_directory = file_path + '/' + artist['artistName'] + ' - ' + album['collectionName']
    if not os.path.exists(folder_directory):
        makedirs(folder_directory)

    progress = 0
    tick = int((1 / len(tracks)) * 100)

    print(tracks)
    # Download every fucking track from dict
    for track in tracks:
        status_handler('Downloading track: ' + track['trackName'], progress)

        track_name = track['trackName']
        if '/' in track_name:
            track_name = track_name.replace('/', '')

        song_name = folder_directory + '/' + track_name + '.mp3'

        # Download track
        urllib.request.urlretrieve(track['trackUrl'], song_name)

        # Metadata correction
        metadata = MP3(song_name)
        print(metadata.tags)
        metadata.delete()
        # Artist
        metadata['composer'] = artist['artistName']
        metadata['performer'] = artist['artistName']
        metadata['artist'] = artist['artistName']

        metadata['album'] = track['collectionName']
        metadata['title'] = track['trackName']
        metadata['date'] = track['releaseDate']
        metadata['genre'] = track['primaryGenreName']
        metadata['tracknumber'] = str(track['trackNumber'])
        metadata['discnumber'] = str(track['discNumber'])

        metadata.update()
        metadata.save()

        status_handler('Song uploaded', progress)
        progress += tick

    status_handler('Uploading completed', 100)


