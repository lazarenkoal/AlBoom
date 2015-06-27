from io import BytesIO
import urllib
import urllib.request
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from musicInfoProcessing import *
from uploder import *
import threading
from tkinter import filedialog

token = 'ab0a03eb3b09b7a4e999930b33ae18be638e9cc7485e6d9a8e97122bbe96cbb980f99a3ba1dfd467d9445'

root = tk.Tk()
root.geometry('1100x700')
root.title('Music Scooper')
root.resizable(False, False)

# TODO: make function for dynamic adding of images
url = "http://userserve-ak.last.fm/serve/64s/88057565.png"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

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


def search_artist(event):
    global artists_cache
    search_string = searchEnter.get()
    if search_string == "":
        messagebox.showerror(title='No artist',message='Nothing, Everything, Anything, Something: '
                                     'If you have nothing, then you have everything, '
                                     'because you have the freedom to do anything, '
                                     'without the fear of losing something. So What??? Type artist!!!',
                             )
    else:
        artistsListBox.delete(0, 'end')
        artists = find_artists(search_string)
        artists_cache = artists[:]
        counter = 0
        for artist in artists:
            artistsListBox.insert(counter, artist)
            counter += 1


"""
The highest part of programs window
"""

# label for search field
searchLabel = tk.Label(master=upperMenuItemsFrame, text='Enter artist')
searchLabel.grid(row=0, column=0, sticky='w')

# search field
searchEnter = tk.Entry(upperMenuItemsFrame, width=25)
searchEnter.grid(row=0, column=1, sticky='W')

# search button
searchBtn = tk.Button(upperMenuItemsFrame, text='Search')
searchBtn.grid(row=0, column=2)
searchBtn.bind('<Button-1>', search_artist)

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

"""
Current function serves as double left mouse btn click handler
After double click listbox will show albums of chosen artist
"""
artist = ""


def select_artist(event):
    global artist
    chosen_artist = artistsListBox.get(artistsListBox.curselection())
    artist = chosen_artist
    albums = find_albums(chosen_artist)
    artistsListBox.delete(0, 'end')
    i = 0
    for album in albums:
        artistsListBox.insert(i, album)
        i += 1
    artistsListBox.bind('<Double-1>', select_album)


album = ""
songs_cache = []


def select_album(event):
    global album
    global songs_cache
    songs_cache = []
    try:
        chosen_album = artistsListBox.get(artistsListBox.curselection())
        album = chosen_album
        display_status('collecting songs')
        songs = get_tracks_from_album(artist, chosen_album)
        songsListBox.delete(0, 'end')
        i = 0
        for song in songs:
            songs_cache.append(song)
            songsListBox.insert(i, song)
            i += 1
        display_status('all songs collected')
    except KeyError:
        artistsListBox.bind('<Double-1>', select_artist)
        songsListBox.delete(0, 'end')
        select_artist(artist)

# listBox for displaying artists
artistsListBox = tk.Listbox(leftFrame, selectmode='SINGLE', height=42, width=66)
artistsListBox.grid(row=0, sticky='NE')
artistsListBox.yview()
artistsListBox.bind('<Double-1>', select_artist)

"""
Right sub menu part
"""


def download_album():
    # opening fucking dialog
    if artist != '' and album != '' and songs_cache.__len__() > 0:
        file_path = filedialog.askdirectory()
        songs_with_links = make_dict_for_downloading(artist, songs_cache, token, display_status)
        print(songs_cache)
        upload_songs(artist, album, songs_with_links, file_path, display_status)
    else:
        messagebox.showerror(title='Empty album',
                             message='You are trying to download nothing.'
                                     '\nSorry, option unavailable!'
                             '\nPlease, try to select something. Music is cool!'
                             )


def start_downloading_in_second_thread(event):
    second_thread = threading.Thread(target=download_album)
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

# listBox for displaying songs of artists
songsListBox = tk.Listbox(rightFrame, selectmode='SINGLE', height=42, width=69)
songsListBox.grid(row=0, sticky='E')
songsListBox.yview()


# label = tk.Label(artistsAlbumsFrame, image=image)
# label.grid(row=0, column=0)
# text = tk.Label(artistsAlbumsFrame, text='Artist: Depeche Mode')
# text.grid(row=0, column=1)

# rabel = tk.Label(songsFrame, image=image)
# rabel.grid(row=0, column=0)
# text3 = tk.Label(songsFrame, text='Song1')
# text3.grid(row=0, column=1)

def display_status(status_string, progress_value=0):
    progressStatusLabel['text'] = status_string
    progressBar['value'] = progress_value


root.mainloop()
