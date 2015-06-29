import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

__author__ = 'aleksandrlazarenko'

"""Main MusicScooper Window
"""


class MainWindow:
    WELCOME_TEXT = ('Welcome to Music Scooper! Absolutely free tool'
                    ' for downloading music by albums from VK social network.'
                    ' Type in your favourite musician and begin uploading!'
                    '\n\nBeautiful music is the art of the prophets that can calm the agitations of the soul; '
                    'it is one of the most magnificent and delightful presents God has given us.'
                    '\n\nMartin Luther')

    BASIC_INSTRUCTION = ('Instruction\n'
                         '1) Find desired musician\n'
                         '2) Pick album\n'
                         '3) Download it!!!')

    def __init__(self, search_starter, artist_selector, album_getter, download_starter):
        # Binding search button
        self.searchBtn.bind('<Button-1>', search_starter)

        # Binding artistsListBox
        self.artistsListBox.bind('<Double-1>', artist_selector)

        # Binding albums ListBox
        self.albumsListBox.bind('<Double-1>', album_getter)

        # Binding download btn listbox
        self.downloadAlbumBtn.bind('<1>', download_starter)

        # Start everything
        self.root.mainloop()

    # Configuring root
    root = tk.Tk()
    root.geometry('1100x700')
    root.title('Music Scooper')
    root.resizable(False, False)

    # The highest, first frame for search and progress bar
    upperMenuFrame = tk.Frame(root)
    upperMenuFrame.grid(row=0, columnspan=2)

    # Frame in the highest for storing content
    upperMenuItemsFrame = tk.Frame(master=upperMenuFrame)
    upperMenuItemsFrame.grid(row=0, column=0, sticky='W')

    # Label for search field
    searchLabel = tk.Label(master=upperMenuItemsFrame, text='Enter artist')
    searchLabel.grid(row=0, column=0, sticky='w')

    # Search field
    searchEnter = tk.Entry(upperMenuItemsFrame, width=25)
    searchEnter.grid(row=0, column=1, sticky='W')

    # Search button
    searchBtn = tk.Button(upperMenuItemsFrame, text='Search')
    searchBtn.grid(row=0, column=2)

    # Left little menu frame
    leftSubMenuFrame = tk.Frame(root)
    leftSubMenuFrame.grid(row=1, column=0)

    # Label for progress status
    progressStatusLabel = tk.Label(leftSubMenuFrame, text='Waiting for your commands')
    progressStatusLabel.grid(row=0, column=0, sticky='E')

    # Progress bar
    progressBar = tk.ttk.Progressbar(leftSubMenuFrame, orient="horizontal", length=300, mode="determinate")
    progressBar.grid(row=0, column=1)
    progressBar['maximum'] = 100

    # Main left frame
    leftFrame = tk.Frame(root, bd=5)
    leftFrame.grid(row=2, column=0)
    leftFrame.grid_rowconfigure(0, weight=1)
    leftFrame.grid_rowconfigure(1, weight=1)
    leftFrame.grid_columnconfigure(0, weight=1)

    # Label for "Search results2
    artistLbl = tk.Label(leftFrame, text='Search results')
    artistLbl.grid(row=0)

    # ListBox for displaying found musicians
    artistsListBox = tk.Listbox(leftFrame, selectmode='SINGLE', height=17, width=66)
    artistsListBox.grid(row=1, sticky='n')
    artistsListBox.yview()

    # Label for displaying "Albums" text
    albumLbl = tk.Label(leftFrame, text='Albums')
    albumLbl.grid(row=2, sticky='N')

    # ListBox for displaying found albums
    albumsListBox = tk.Listbox(leftFrame, selectmode='SINGLE', height=17, width=66)
    albumsListBox.grid(row=3, sticky='N')
    albumsListBox.yview()

    # Right little menu frame
    rightSubMenuFrame = tk.Frame(root)
    rightSubMenuFrame.grid(row=1, column=1)

    # Button for uploading album
    downloadAlbumBtn = tk.Button(rightSubMenuFrame, text='upload album')
    downloadAlbumBtn.grid(row=0, column=0)

    # Main right frame
    rightFrame = tk.Frame(root)
    rightFrame.grid(row=2, column=1)
    rightFrame.grid_rowconfigure(0, weight=1)

    # Preparing start image
    image = Image.open("logo.jpg")
    photo = ImageTk.PhotoImage(image)

    # Setting starting image
    albumPhoto = tk.Label(rightFrame)
    albumPhoto['image'] = photo
    albumPhoto.grid(row=0, column=0, sticky='W')

    # Preparing Welcome text
    albumInfo = tk.Text(rightFrame, font=('times', 14), width=42, height=10, wrap='word')
    albumInfo.grid(row=0, column=1, sticky='N')
    albumInfo.insert(1.0, WELCOME_TEXT)
    albumInfo.configure(state='disabled')

    # ListBox for displaying songs of artists
    songsList = tk.Text(rightFrame, font=('times', 16), width=42, height=24, wrap='word')
    songsList.grid(row=1, sticky='W', columnspan=2)
    songsList.insert(1.0, BASIC_INSTRUCTION)
    songsList.configure(state='disabled')
