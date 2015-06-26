from musicInfoProcessing import *

print('Введите информацию об имени артиста')
artistName = input()
artists = find_artists(artistName)
for singer in artists:
    print(singer['name'])

print('Получаю альбомы')
albums = find_albums(artistName)
print(albums)
for album in albums:
    print(album['name'])

print('Введите название альбома, треки из которого вы хотите получить')
albumName = input()
tracks = get_tracks_from_album(artistName, albumName)
for track in tracks:
    print(track['name'])