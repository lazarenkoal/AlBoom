from main_view import *
import threading
from music_info_processing import *
from downloader import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import io
from program_data_manager import update_spent_money, get_spent_money
__author__ = 'aleksandrlazarenko'

artists = []
albums = []


class MainWindowViewController:
    def __init__(self, user_data):
        self.connection = http.client.HTTPConnection(APIRoot)
        self.artists_cache = []
        self.artist = ""
        self.album = ""
        self.user_data = user_data
        self.songs_cache = []
        self.album_price = 0
        self.main_window = MainWindow(
            artist_selector=self.select_artist_in_the_second_thread,
            album_getter=self.start_getting_album_in_another_thread,
            download_starter=self.start_downloading_in_second_thread,
            search_starter=self.start_searching_in_another_thread,
            spent_money=self.user_data['data']['spent_money'])

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
        try:
                # opening fucking dialog
            if self.artist != '' and self.album != '' and self.songs_cache.__len__() > 0:
                file_path = filedialog.askdirectory()
                songs_with_links = get_urls_of_tracks_for_downloading(self.artist,
                                                                      self.songs_cache,
                                                                      self.main_window.display_status)
                download_songs(self.artist, self.album, songs_with_links, file_path,
                               self.main_window.display_status)
                update_spent_money(self.album_price)
                self.main_window.moneySpentLbl['text'] ='Затарился на: {:.2f}$'.format(float(get_spent_money()))
            else:
                messagebox.showerror(title='Не выбрано ничего',
                                     message='Вы не можете загрузить ничего.'
                                             '\nИзвините, но такая опция пока что не поддерживается!'
                                             '\nНу хоть что-нибудь введите ;)!'
                                     )
        except:
            messagebox.showerror(title='Произошла какая-то ошибка',
                                 message='Извините, но что-то пошло не так... '
                                         'Пожалуйста, перезапустите программу и'
                                         'попробуйте еще раз')
#
    def search_artist(self):
        try:
            search_string = self.main_window.searchEnter.get()
            if search_string == "":
                messagebox.showerror(title='Не введен музыкант', message='Пожалуйста, выберете музыканта',
                                     )
            else:
                self.main_window.artistsListBox.delete(0, 'end')
                global artists
                artists = find_artists(search_string, self.connection)
                counter = 0
                for artist in artists:
                    self.main_window.artistsListBox.insert(counter, artist['artistName'])
                    counter += 1
        except:
            messagebox.showerror(title='Странная ошибка',
                                 message='Погода сегодня так себе. Духи не захотели найти этот альбом!')

    def select_artist(self):
        try:
            chosen_artist_index = self.main_window.artistsListBox.curselection()[0]
            self.artist = artists[int(chosen_artist_index)]
            global albums
            albums = find_albums(artists[int(chosen_artist_index)]['artistId'], self.connection)
            self.main_window.albumsListBox.delete(0, 'end')
            i = 0
            for album in albums[1:]:
                self.main_window.albumsListBox.insert(i, album['collectionName'])
                i += 1
        except:
            messagebox.showerror(title='Веселая ошибка',
                                 message='Попробуйте еще раз. '
                                         'Это артист против бесплатного '
                                         'скачивания своих песен!')

    def select_album(self):
        try:
            chosen_album_index = int(self.main_window.albumsListBox.curselection()[0]) + 1
            self.album = albums[chosen_album_index]
            self.main_window.display_status('Collecting songs')
            self.album_price = albums[chosen_album_index]['collectionPrice']

            album_id = albums[chosen_album_index]['collectionId']
            songs = get_tracks_from_album(album_id, self.connection, self.main_window.display_status)

            # Show album cover
            cover = self.get_image(self.album['artworkUrl100'])

            self.main_window.albumPhoto.configure(image=cover)
            self.main_window.albumPhoto.image = cover
            self.main_window.photo_logo = cover

            self.main_window.albumInfo.configure(state='normal')
            self.main_window.albumInfo.delete(1.0, 'end')
            self.main_window.albumInfo.insert(1.0, 'Цена вопроса: {}$'.format(self.album_price))
            self.main_window.albumInfo.configure(state='disabled')

            self.main_window.songsList.configure(state='normal')
            self.main_window.songsList.delete(1.0, 'end')
            self.main_window.songsList.insert(1.0,
                                              'Содержание: {} - {}\n\n'.format(self.artist['artistName'],
                                                                             self.album['collectionName']))
            i = 1
            self.songs_cache = []  # Clearing cache
            for song in songs[1:]:
                print(song)
                self.songs_cache.append(song)
                self.main_window.songsList.insert('end', '{}) {}\n'.format(i, song['trackName']))
                i += 1
            self.main_window.songsList.configure(state='disabled')
            self.main_window.display_status('Все песни собраны!', 100)

        except:
            messagebox.showerror(title='Хм-хм-хм',
                                 message='Попробуйте перезапустить программу и сделать все снова;)')

    @staticmethod
    def get_image(url):
        # Getting image from url
        image_bytes = urllib.request.urlopen(url).read()

        # Internal data file
        data_stream = io.BytesIO(image_bytes)

        # Open as a PIL image object
        pil_image = Image.open(data_stream)
        tk_image = ImageTk.PhotoImage(pil_image)

        print(url)
        return tk_image
