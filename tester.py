from musicInfoProcessing import *
from uploder import *
import webbrowser
url = ('https://oauth.vk.com/authorize?' +
       'client_id=4973489&' +
       'scope=audio&' +
       'redirect_uri=https://oauth.vk.com/blank.html&' +
       'display=page&' +
       'v=5.34&' +
       'response_type=token')

webbrowser.open_new(url)


token = '850f1fc36b0f0778223079c2554315fd30e35654194102b2169064485c8d2495013d3422652fa503c1afd'
print('Введите информацию об имени артиста')
artistName = input()
artists = find_artists(artistName)
for singer in artists:
    print(singer)

print('Получаю альбомы')
albums = find_albums(artistName)
print(albums)

tracksForUploading = []
print('Введите название альбома, треки из которого вы хотите получить')
albumName = input()
tracks = get_tracks_from_album(artistName, albumName)
print(tracks)

tracksUrl = get_urls_of_tracks_for_downloading(artistName, tracksForUploading, token)
links = []
for track in tracksUrl:
    try:
        links.append(track['response'][1]['url'])
        print(track['response'][1]['url'])
    except:
        continue
print('Загрузка ссылок завершена')
songWithLinks = dict(zip(tracksForUploading, links))
print(songWithLinks)
upload_songs(artistName, albumName, songWithLinks)

