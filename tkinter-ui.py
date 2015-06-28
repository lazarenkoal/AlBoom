import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from musicInfoProcessing import *
from uploder import *
import threading
from tkinter import filedialog
import io
token = '58fca0ab24a05f6ec8579518e9585ea09679a02849fd66300e10bc581b8bea3fb08e645e97c860bab137e'

root = tk.Tk()
root.geometry('1100x700')
root.title('Music Scooper')
root.resizable(False, False)
connection = None

# TODO: placeholder!!!!
def get_image(url="http://userserve-ak.last.fm/serve/174s/97263801.jpg"):
    image_bytes = urlopen(url).read()
    # internal data file
    data_stream = io.BytesIO(image_bytes)
    # open as a PIL image object
    pil_image = Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)

    return tk_image


# the highest, first frame for search and progress bar
upperMenuFrame = tk.Frame(root)
upperMenuFrame.grid(row=0, columnspan=2)

# frame in the highest for storing content
upperMenuItemsFrame = tk.Frame(master=upperMenuFrame)
upperMenuItemsFrame.grid(row=0, column=0, sticky='W')

"""
Function for displaying list of artists in listBox
returns names of artists, cause we need them for coming back
"""
artists_cache = []


def search_artist():
    global connection
    if connection is None:
        connection = http.client.HTTPConnection(APIRoot)        # opening connection with
    global artists_cache
    search_string = searchEnter.get()
    if search_string == "":
        messagebox.showerror(title='No artist', message='Nothing, Everything, Anything, Something: '
                                     'If you have nothing, then you have everything, '
                                     'because you have the freedom to do anything, '
                                     'without the fear of losing something. So What??? Type artist!!!',
                             )
    else:
        artistsListBox.delete(0, 'end')
        artists = find_artists(search_string, connection)
        artists_cache = artists[:]
        counter = 0
        for artist in artists:
            artistsListBox.insert(counter, artist)
            counter += 1

def start_searching_in_another_thread(event):
    second_thread = threading.Thread(target=search_artist, daemon=True)
    second_thread.run()

"""
The highest part of programs window
"""

# label for search field
searchLabel = tk.Label(master=upperMenuItemsFrame, text='Enter artist')
searchLabel.grid(row=0, column=0, sticky='w')

# search field
searchEnter = tk.Entry(upperMenuItemsFrame, width=25)
searchEnter.grid(row=0, column=1, sticky='W')
searchEnter.bind('<Return>', start_searching_in_another_thread)

# search button
searchBtn = tk.Button(upperMenuItemsFrame, text='Search')
searchBtn.grid(row=0, column=2)
searchBtn.bind('<Button-1>', start_searching_in_another_thread)


"""
Left sub menu part
"""

# left little menu frame
leftSubMenuFrame = tk.Frame(root)
leftSubMenuFrame.grid(row=1, column=0)

# place for progress status
progressStatusLabel = tk.Label(leftSubMenuFrame, text='Waiting for your commands')
progressStatusLabel.grid(row=0, column=0, sticky='E')

progressBar = ttk.Progressbar(leftSubMenuFrame, orient="horizontal", length=300, mode="determinate")
progressBar.grid(row=0, column=1)
progressBar['maximum'] = 100
"""
Left frame part
"""
# main left frame
leftFrame = tk.Frame(root, bd=5)
leftFrame.grid(row=2, column=0)
leftFrame.grid_rowconfigure(0, weight=1)
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_rowconfigure(1, weight=1)

"""
Current function serves as double left mouse btn click handler
After double click listbox will show albums of chosen artist
"""
artist = ""


def select_artist():
    global artist
    chosen_artist = artistsListBox.get(artistsListBox.curselection())
    artist = chosen_artist
    albums = find_albums(chosen_artist, connection)
    albumsListBox.delete(0, 'end')
    i = 0
    for album in albums:
        albumsListBox.insert(i, album)
        i += 1

def select_artist_in_the_second_thread(event):
    second_thread = threading.Thread(target=select_artist, daemon=True)
    second_thread.start()

album = ""
songs_cache = []


def select_album():
    global album
    global songs_cache
    songs_cache = []
    chosen_album = albumsListBox.get(albumsListBox.curselection())
    album = chosen_album
    display_status('collecting songs')
    songs, image_url, info = get_tracks_from_album(artist, chosen_album, connection, display_status)
    print(image_url)
    print(info)
    try:
        cover = get_image(image_url)
    except:
        cover = None # TODO: find image for album placeholder
    albumPhoto.configure(image=cover)
    albumPhoto.image = cover
    albumInfo.configure(state='normal')
    albumInfo.delete(1.0, 'end')
    albumInfo.insert(1.0, info)
    albumInfo.configure(state='disabled')
    songsList.configure(state='normal')
    songsList.delete(1.0, 'end')
    songsList.insert(1.0, 'Contents: {} - {}\n\n'.format(artist, album))
    i = 1
    for song in songs:
        songs_cache.append(song)
        songsList.insert('end', '{}) {}\n'.format(i, song))
        i += 1
    songsList.configure(state='disabled')
    display_status('all songs collected', 100)


def start_getting_album_in_another_thread(event):
    second_thread = threading.Thread(target=select_album, daemon=True)
    second_thread.start()

# listBox for displaying artists
artistLbl = tk.Label(leftFrame, text='Search results')
artistLbl.grid(row=0)

artistsListBox = tk.Listbox(leftFrame, selectmode='SINGLE', height=17, width=66)
artistsListBox.grid(row=1, sticky='n')
artistsListBox.yview()
artistsListBox.bind('<Double-1>', select_artist_in_the_second_thread)

albumLbl = tk.Label(leftFrame, text='Albums')
albumLbl.grid(row=2, sticky='N')

albumsListBox = tk.Listbox(leftFrame, selectmode='SINGLE', height=17, width=66)
albumsListBox.grid(row=3, sticky='N')
albumsListBox.yview()
albumsListBox.bind('<Double-1>', start_getting_album_in_another_thread)

"""
Right sub menu part
"""


def download_album():
    # opening fucking dialog
    if artist != '' and album != '' and songs_cache.__len__() > 0:
        file_path = filedialog.askdirectory()
        songs_with_links = get_urls_of_tracks_for_downloading(artist, songs_cache, token, display_status)
        print(songs_cache)
        upload_songs(artist, album, songs_with_links, file_path, display_status)
    else:
        messagebox.showerror(title='Empty album',
                             message='You are trying to download nothing.'
                                     '\nSorry, option unavailable!'
                             '\nPlease, try to select something. Music is cool!'
                             )


def start_downloading_in_second_thread(event):
    second_thread = threading.Thread(target=download_album, daemon=True)
    second_thread.start()

# right little menu frame
rightSubMenuFrame = tk.Frame(root)
rightSubMenuFrame.grid(row=1, column=1)

downloadAlbumBtn = tk.Button(rightSubMenuFrame, text='upload album')
downloadAlbumBtn.grid(row=0, column=0)
downloadAlbumBtn.bind('<1>', start_downloading_in_second_thread)

"""
Right menu part
"""
# main right frame
rightFrame = tk.Frame(root)
rightFrame.grid(row=2, column=1)
rightFrame.grid_rowconfigure(0, weight=1)

# information about album
image = Image.open("logo.jpg")
photo = ImageTk.PhotoImage(image)
albumPhoto = tk.Label(rightFrame)
albumPhoto['image'] = photo
albumPhoto.grid(row=0, column=0, sticky='W')
albumInfo = tk.Text(rightFrame, font=('times', 14), width=42, height=10, wrap='word')
albumInfo.grid(row=0, column=1, sticky='N')
albumInfo.insert(1.0, 'Welcome to Music Scooper! Absolutely free tool'
                 ' for downloading music by albums from VK social network.'
                 ' Type in your favourite musician and begin uploading!'
                 '\n\nBeautiful music is the art of the prophets that can calm the agitations of the soul; '
                      'it is one of the most magnificent and delightful presents God has given us.'
                 '\n\nMartin Luther')
albumInfo.configure(state='disabled')

# listBox for displaying songs of artists
songsList = tk.Text(rightFrame, font=('times', 16), width=42, height=24, wrap='word')
songsList.grid(row=1, sticky='W', columnspan=2)
songsList.insert(1.0, 'Instruction\n'
                 '1) Find desired musician\n'
                      '2) Pick album\n'
                      '3) Download it!!!')
songsList.configure(state='disabled')

def display_status(status_string, progress_value=0):
    progressStatusLabel['text'] = status_string
    progressBar['value'] = progress_value

# TODO: make normal event handling for chosen artist and album
# TODO: debug everything
# TODO: add an easy way for pasting vk access token inside in app

root.mainloop()
