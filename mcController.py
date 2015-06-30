from mcView import *
import threading
from musicInfoProcessing import *
from uploder import *
from PIL import Image, ImageTk
from tkinter import filedialog

__author__ = 'aleksandrlazarenko'

artists = []
albums = []

class MainWindowViewController:
    def __init__(self, token):
        self.token = token
        self.connection = http.client.HTTPConnection(APIRoot)
        self.artists_cache = []
        self.artist = ""
        self.album = ""
        self.songs_cache = []
        self.main_window = MainWindow(
            artist_selector=self.select_artist_in_the_second_thread,
            album_getter=self.start_getting_album_in_another_thread,
            download_starter=self.start_downloading_in_second_thread,
            search_starter=self.start_searching_in_another_thread)

        self.main_window.root.mainloop()

    def start_searching_in_another_thread(self, event):
        second_thread = threading.Thread(target=self.search_artist,
                                         daemon=True)
        second_thread.run()

    def select_artist_in_the_second_thread(self, event):
        second_thread = threading.Thread(target=self.select_artist,
                                         daemon=True)
        second_thread.start()

    def start_getting_album_in_another_thread(self, event):
        second_thread = threading.Thread(target=self.select_album,
                                         daemon=True)
        second_thread.start()

    def start_downloading_in_second_thread(self, event):
        second_thread = threading.Thread(target=self.download_album,
                                         daemon=True)
        second_thread.start()

    def download_album(self):
        # opening fucking dialog
        if self.artist != '' and self.album != '' and self.songs_cache.__len__() > 0:
            file_path = filedialog.askdirectory()
            songs_with_links = get_urls_of_tracks_for_downloading(self.artist,
                                                                  self.songs_cache,
                                                                  self.token,
                                                                  self.main_window.display_status)
            upload_songs(self.artist, self.album, songs_with_links, file_path,
                         self.main_window.display_status)
        else:
            messagebox.showerror(title='Empty album',
                                 message='You are trying to download nothing.'
                                         '\nSorry, option unavailable!'
                                         '\nPlease, try to select something. Music is cool!'
                                 )

    def search_artist(self):
        search_string = self.main_window.searchEnter.get()
        if search_string == "":
            messagebox.showerror(title='No artist', message='Nothing, Everything, Anything, Something: '
                                                            'If you have nothing, then you have everything, '
                                                            'because you have the freedom to do anything, '
                                                            'without the fear of losing something. So What??? '
                                                            'Type artist!!!',
                                 )
        else:
            self.main_window.artistsListBox.delete(0, 'end')
            global artists
            artists = find_artists(search_string, self.connection)
            counter = 0
            for artist in artists:
                self.main_window.artistsListBox.insert(counter, artist['artistName'])
                counter += 1

    def select_artist(self):
        chosen_artist_index = self.main_window.artistsListBox.curselection()[0]
        self.artist = artists[chosen_artist_index]
        global albums
        albums = find_albums(artists[chosen_artist_index]['artistId'], self.connection)
        print(albums)
        self.main_window.albumsListBox.delete(0, 'end')
        i = 0
        for album in albums[1:]:
            self.main_window.albumsListBox.insert(i, album['collectionName'])
            i += 1

    def select_album(self):
        chosen_album_index = self.main_window.albumsListBox.curselection()[0]
        self.album = albums[chosen_album_index]
        self.main_window.display_status('Collecting songs')
        album_id = albums[chosen_album_index]['collectionId']
        print(album_id)
        songs = get_tracks_from_album(album_id, self.connection, self.main_window.display_status)

        #Show album cover
        cover = self.get_image(self.album['artworkUrl100'])

        self.main_window.albumPhoto.configure(image=cover)
        self.main_window.albumPhoto.image = cover
        self.main_window.photo = cover

        self.main_window.albumInfo.configure(state='normal')
        self.main_window.albumInfo.delete(1.0, 'end')
        self.main_window.albumInfo.insert(1.0, info)
        self.main_window.albumInfo.configure(state='disabled')

        self.main_window.songsList.configure(state='normal')
        self.main_window.songsList.delete(1.0, 'end')
        self.main_window.songsList.insert(1.0,
                                          'Contents: {} - {}\n\n'.format(self.artist['artistName'],
                                                                         self.album['collectionName']))
        i = 1
        for song in songs[1:]:
            print(song)
            self.songs_cache.append(song)
            self.main_window.songsList.insert('end', '{}) {}\n'.format(i, song['trackName']))
            i += 1
        self.main_window.songsList.configure(state='disabled')
        self.main_window.display_status('all songs collected', 100)

    def get_image(self, url):
        # Getting image from url
        image_bytes = urllib.request.urlopen(url).read()

        # Internal data file
        data_stream = io.BytesIO(image_bytes)

        # Open as a PIL image object
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)

        print(url)
        return tk_image
