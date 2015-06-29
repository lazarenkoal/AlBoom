from mcView import *
import threading
from musicInfoProcessing import *
from uploder import *
from PIL import Image, ImageTk
from tkinter import filedialog

__author__ = 'aleksandrlazarenko'


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
            self.album = ""
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
            artists = find_artists(search_string, self.connection)
            self.artists_cache = artists[:]
            counter = 0
            for artist in artists:
                self.main_window.artistsListBox.insert(counter, artist)
                counter += 1

    def select_artist(self):
        chosen_artist = self.main_window.artistsListBox.get(
            self.main_window.artistsListBox.curselection())
        self.artist = chosen_artist
        albums = find_albums(chosen_artist, self.connection)
        self.main_window.albumsListBox.delete(0, 'end')
        i = 0
        for album in albums:
            self.main_window.albumsListBox.insert(i, album)
            i += 1

    def select_album(self):
        self.songs_cache = [] # clearing information about songs
        chosen_album = self.main_window.albumsListBox.get(
            self.main_window.albumsListBox.curselection())
        self.album = chosen_album
        self.main_window.display_status('collecting songs')
        songs, image_url, info = get_tracks_from_album(self.artist, chosen_album,
                                                       self.connection,
                                                       self.main_window.display_status)

        print('Пытаюсь открыть картинку')
        cover = self.get_image(image_url)

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
                                          'Contents: {} - {}\n\n'.format(self.artist,
                                                                         self.album))
        i = 1
        for song in songs:
            self.songs_cache.append(song)
            self.main_window.songsList.insert('end', '{}) {}\n'.format(i, song))
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
