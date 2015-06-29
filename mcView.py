import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import urllib
__author__ = 'aleksandrlazarenko'

"""Main MusicScooper Window
"""


class MainWindow:
    def __init__(self, search_starter, artist_selector, album_getter, download_starter):
        self.WELCOME_TEXT = ('Welcome to Music Scooper! Absolutely free tool'
                             ' for downloading music by albums from VK social network.'
                             ' Type in your favourite musician and begin uploading!'
                             '\n\nBeautiful music is the art of the prophets that can calm the agitations of the soul; '
                             'it is one of the most magnificent and delightful presents God has given us.'
                             '\n\nMartin Luther')

        self.BASIC_INSTRUCTION = ('Instruction\n'
                                  '1) Find desired musician\n'
                                  '2) Pick album\n'
                                  '3) Download it!!!')

        # Configuring root
        self.root = tk.Tk()
        self.root.geometry('1100x700')
        self.root.title('Music Scooper')
        self.root.resizable(False, False)

        # The highest, first frame for search and progress bar
        self.upperMenuFrame = tk.Frame(self.root)
        self.upperMenuFrame.grid(row=0, columnspan=2)

        # Frame in the highest for storing content
        self.upperMenuItemsFrame = tk.Frame(master=self.upperMenuFrame)
        self.upperMenuItemsFrame.grid(row=0, column=0, sticky='W')

        # Label for search field
        self.searchLabel = tk.Label(master=self.upperMenuItemsFrame, text='Enter artist')
        self.searchLabel.grid(row=0, column=0, sticky='w')

        # Search field
        self.searchEnter = tk.Entry(self.upperMenuItemsFrame, width=25)
        self.searchEnter.grid(row=0, column=1, sticky='W')

        # Search button
        self.searchBtn = tk.Button(self.upperMenuItemsFrame, text='Search')
        self.searchBtn.grid(row=0, column=2)

        # Left little menu frame
        self.leftSubMenuFrame = tk.Frame(self.root)
        self.leftSubMenuFrame.grid(row=1, column=0)

        # Label for progress status
        self.progressStatusLabel = tk.Label(self.leftSubMenuFrame, text='Waiting for your commands')
        self.progressStatusLabel.grid(row=0, column=0, sticky='E')

        # Progress bar
        self.progressBar = tk.ttk.Progressbar(self.leftSubMenuFrame, orient="horizontal", length=300,
                                              mode="determinate")
        self.progressBar.grid(row=0, column=1)
        self.progressBar['maximum'] = 100

        # Main left frame
        self.leftFrame = tk.Frame(self.root, bd=5)
        self.leftFrame.grid(row=2, column=0)
        self.leftFrame.grid_rowconfigure(0, weight=1)
        self.leftFrame.grid_rowconfigure(1, weight=1)
        self.leftFrame.grid_columnconfigure(0, weight=1)

        # Label for "Search results2
        self.artistLbl = tk.Label(self.leftFrame, text='Search results')
        self.artistLbl.grid(row=0)

        # ListBox for displaying found musicians
        self.artistsListBox = tk.Listbox(self.leftFrame, selectmode='SINGLE', height=17, width=66)
        self.artistsListBox.grid(row=1, sticky='n')
        self.artistsListBox.yview()

        # Label for displaying "Albums" text
        self.albumLbl = tk.Label(self.leftFrame, text='Albums')
        self.albumLbl.grid(row=2, sticky='N')

        # ListBox for displaying found albums
        self.albumsListBox = tk.Listbox(self.leftFrame, selectmode='SINGLE', height=17, width=66)
        self.albumsListBox.grid(row=3, sticky='N')
        self.albumsListBox.yview()

        # Right little menu frame
        self.rightSubMenuFrame = tk.Frame(self.root)
        self.rightSubMenuFrame.grid(row=1, column=1)

        # Button for uploading album
        self.downloadAlbumBtn = tk.Button(self.rightSubMenuFrame, text='upload album')
        self.downloadAlbumBtn.grid(row=0, column=0)

        # Main right frame
        self.rightFrame = tk.Frame(self.root)
        self.rightFrame.grid(row=2, column=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)

        # Preparing start image
        self.image_bytes = Image.open("logo.jpg")
        self.photo = ImageTk.PhotoImage(self.image_bytes)

        # Setting starting image
        self.albumPhoto = tk.Label(self.rightFrame)
        self.albumPhoto['image'] = self.photo
        self.albumPhoto.grid(row=0, column=0, sticky='W')

        # Preparing Welcome text
        self.albumInfo = tk.Text(self.rightFrame, font=('times', 14), width=42, height=10, wrap='word')
        self.albumInfo.grid(row=0, column=1, sticky='N')
        self.albumInfo.insert(1.0, self.WELCOME_TEXT)
        self.albumInfo.configure(state='disabled')

        # ListBox for displaying songs of artists
        self.songsList = tk.Text(self.rightFrame, font=('times', 16), width=42, height=24, wrap='word')
        self.songsList.grid(row=1, sticky='W', columnspan=2)
        self.songsList.insert(1.0, self.BASIC_INSTRUCTION)
        self.songsList.configure(state='disabled')

        # Binding search button
        self.searchBtn.bind('<Button-1>', search_starter)

        # Binding search enter
        self.searchEnter.bind('<Return>', search_starter)

        # Binding artistsListBox
        self.artistsListBox.bind('<Double-1>', artist_selector)

        # Binding albums ListBox
        self.albumsListBox.bind('<Double-1>', album_getter)

        # Binding download btn listbox
        self.downloadAlbumBtn.bind('<1>', download_starter)

    def display_status(self, status_string, progress_value=0):
        self.progressStatusLabel['text'] = status_string
        self.progressBar['value'] = progress_value


