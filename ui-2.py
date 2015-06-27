from io import BytesIO
import urllib
import urllib.request
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from musicInfoProcessing import *
from uploder import *

token = '850f1fc36b0f0778223079c2554315fd30e35654194102b2169064485c8d2495013d3422652fa503c1afd'

root = tk.Tk()
root.geometry('1000x800')
root.title('Music Scooper')

# TODO: make function for dynamic adding of images
url = "http://userserve-ak.last.fm/serve/64s/88057565.png"
with urllib.request.urlopen(url) as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
image = ImageTk.PhotoImage(im)

# the highest, first frame for search and progress bar
upperMenuFrame = tk.Frame(root, width=1000, height=40, bg='grey')
upperMenuFrame.grid(row=0, columnspan=2)

# frame in the highest for storing content
upperMenuItemsFrame = tk.Frame(upperMenuFrame, width=1000, height=40)
upperMenuItemsFrame.grid(row=0)

"""
Function for displaying list of artists in listBox
returns names of artists, cause we need them for coming back
"""
artists_cache = []
def search_artist(event):
    global artists_cache
    search_string = searchEnter.get()
    if search_string == "":
        messagebox.showerror('Empty search artist field',
                             'Please, paste smth there, because we can\'t find empty artist')
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
searchLabel = tk.Label(upperMenuItemsFrame, text='Enter artist')
searchLabel.grid(row=0, column=0, sticky='W')

# search field
searchEnter = tk.Entry(upperMenuItemsFrame, width=25)
searchEnter.grid(row=0, column=1, sticky='W')

# search button
searchBtn = tk.Button(upperMenuItemsFrame, text='Search')
searchBtn.grid(row=0, column=2)
searchBtn.bind('<Button-1>', search_artist)

# input code field
codeField = tk.Label(upperMenuItemsFrame, text='Input safe code')
codeField.grid(row=0, column=3)

# enter code field
enterCodeField = tk.Entry(upperMenuItemsFrame, width=25)
enterCodeField.grid(row=0, column=4)

# enter code button
enterCodeBtn = tk.Button(upperMenuItemsFrame, text='Enter')
enterCodeBtn.grid(row=0, column=5)

# place for progress bar
progressLabel = tk.Label(upperMenuItemsFrame, text='Here will be current progress')
progressLabel.grid(row=0, column=6)


"""
Left sub menu part
"""

# left little menu frame
leftSubMenuFrame = tk.Frame(root, width=500, height=40, bg='yellow')
leftSubMenuFrame.grid(row=1, column=0)


"""
Left frame part
"""
# main left frame
leftFrame = tk.Frame(root, width=500, height=720, bg='blue')
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
        songs = get_tracks_from_album(artist, chosen_album)
        songsListBox.delete(0, 'end')
        i = 0
        for song in songs:
            songs_cache.append(song)
            songsListBox.insert(i, song)
            i += 1
    except KeyError:
        artistsListBox.bind('<Double-1>', select_artist)
        songsListBox.delete(0, 'end')
        select_artist(artist)


# listBox for displaying artists
artistsListBox = tk.Listbox(leftFrame, selectmode='SINGLE', height=42, width=70)
artistsListBox.grid(row=0, sticky='N')
artistsListBox.yview()
artistsListBox.bind('<Double-1>', select_artist)

"""
Right submenu part
"""
def download_album(event):
    if artist != '' and album != '' and songs_cache.__len__() > 0:
        songs_with_links = make_dict_for_downloading(artist, songs_cache, token)
        upload_songs(artist, album, songs_with_links)

# right little menu frame
rightSubMenuFrame = tk.Frame(root, width=500, height=40, bg='green')
rightSubMenuFrame.grid(row=1, column=1)

downloadAlbumBtn = tk.Button(rightSubMenuFrame, text='upload album')
downloadAlbumBtn.grid(row=0, column=0)
downloadAlbumBtn.bind('<1>', download_album)

"""
Right menu part
"""
# main right frame
rightFrame = tk.Frame(root, width=500, height=720, bg='red')
rightFrame.grid(row=2, column=1)

# listBox for displaying songs of artists
songsListBox = tk.Listbox(rightFrame, selectmode='SINGLE', height=42, width=70)
songsListBox.grid(row=0, sticky='N')
songsListBox.yview()


# label = tk.Label(artistsAlbumsFrame, image=image)
# label.grid(row=0, column=0)
# text = tk.Label(artistsAlbumsFrame, text='Artist: Depeche Mode')
# text.grid(row=0, column=1)

# rabel = tk.Label(songsFrame, image=image)
# rabel.grid(row=0, column=0)
# text3 = tk.Label(songsFrame, text='Song1')
# text3.grid(row=0, column=1)


root.mainloop()
