import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main_controller
import http.client
from request_constructor import construct_vk_check_token
import json
from music_info_processing import VKApiRoot
import time
import webbrowser

__author__ = 'aleksandrlazarenko'

"""Main MusicScooper Window
"""


class MainWindow:
    def __init__(self, search_starter, artist_selector, album_getter, download_starter, spent_money):

        self.background_color = 'white'

        self.WELCOME_TEXT = ('Добро пожаловать в AlBoom! Это программа для загрузки'
                             'альбомов твоих любимых исполнителей через Вконтакте.'
                             'Просто введи имя исполнителя и выбери альбом.'
                             '\n\nBeautiful music is the art of the prophets that '
                             'can calm the agitations of the soul '
                             'it is one of the most magnificent and delightful '
                             'presents God has given us.'
                             '\n\nMartin Luther')

        self.BASIC_INSTRUCTION = ('Что делать?\n'
                                  '1) Введи имя артиста и нажми "Найти"\n'
                                  '2) Кликни 2 раза по нужному имени\n'
                                  '3) Кликни 2 раза по нужному альбому\n'
                                  '4) Нажми "Скачать альбом"')

        # Configuring root
        self.root = tk.Tk()
        self.root.geometry('1081x700')
        self.root.title('AlBoom')
        self.root.resizable(False, False)
        self.root.configure(background=self.background_color)

        # Creating pop-up
        self.captcha_window = None

        # The highest, first frame for search and progress bar
        self.upperMenuFrame = tk.Frame(self.root)
        self.upperMenuFrame.grid(row=0, columnspan=2)
        self.upperMenuFrame.configure(background=self.background_color)

        # Frame in the highest for storing content
        self.upperMenuItemsFrame = tk.Frame(master=self.upperMenuFrame)
        self.upperMenuItemsFrame.grid(row=0, column=0, sticky='W')
        self.upperMenuFrame.configure(background=self.background_color)

        # Label for search field
        self.searchLabel = tk.Label(master=self.upperMenuItemsFrame, text='Имя артиста:')
        self.searchLabel.grid(row=0, column=0, sticky='w')
        self.searchLabel.configure(background=self.background_color)

        # Search field
        self.searchEnter = tk.Entry(self.upperMenuItemsFrame, width=25)
        self.searchEnter.grid(row=0, column=1, sticky='W')

        # Search button
        self.searchBtn = tk.Button(self.upperMenuItemsFrame, text='Найти')
        self.searchBtn.grid(row=0, column=2)
        self.searchBtn.configure(background=self.background_color)

        # Amount of money display
        self.moneySpentLbl = tk.Label(self.upperMenuItemsFrame, text='Затарился на: {:.2f}$'.format(float(spent_money)))
        self.moneySpentLbl.grid(row=0, column=3)
        self.moneySpentLbl.configure(background=self.background_color)

        # Left little menu frame
        self.leftSubMenuFrame = tk.Frame(self.root)
        self.leftSubMenuFrame.grid(row=1, column=0)
        self.leftSubMenuFrame.configure(background=self.background_color)

        # Label for progress status
        self.progressStatusLabel = tk.Label(self.leftSubMenuFrame, text='Готов искать')
        self.progressStatusLabel.grid(row=0, column=0, sticky='E')
        self.progressStatusLabel.configure(background=self.background_color)

        # Progress bar
        self.progressBar = tk.ttk.Progressbar(self.leftSubMenuFrame, orient="horizontal", length=300,
                                              mode="determinate")
        self.progressBar.grid(row=0, column=1)
        self.progressBar['maximum'] = 100

        # Main left frame
        self.leftFrame = tk.LabelFrame(self.root, bd=2, relief='ridge', pady=5, padx=5)
        self.leftFrame.grid(row=2, column=0)
        self.leftFrame.grid_rowconfigure(0, weight=1)
        self.leftFrame.grid_rowconfigure(1, weight=1)
        self.leftFrame.grid_columnconfigure(0, weight=1)

        # Label for "Search results2
        self.artistLbl = tk.Label(self.leftFrame, text='Результаты поиска')
        self.artistLbl.grid(row=0)

        # ListBox for displaying found musicians
        self.artistsListBox = tk.Listbox(self.leftFrame, selectmode='SINGLE', height=17, width=66)
        self.artistsListBox.grid(row=1, column=0, sticky='n')
        self.artistsListBox.yview()

        # Label for displaying "Albums" text
        self.albumLbl = tk.Label(self.leftFrame, text='Альбомы')
        self.albumLbl.grid(row=2, sticky='N')

        # ListBox for displaying found albums
        self.albumsListBox = tk.Listbox(self.leftFrame, selectmode='SINGLE', height=17, width=66)
        self.albumsListBox.grid(row=3, column=0, sticky='N')
        self.albumsListBox.yview()

        # Right little menu frame
        self.rightSubMenuFrame = tk.Frame(self.root)
        self.rightSubMenuFrame.grid(row=1, column=1)
        self.rightSubMenuFrame.configure(background=self.background_color)

        # Button for uploading album
        self.downloadAlbumBtn = tk.Button(self.rightSubMenuFrame, text='Скачать альбом')
        self.downloadAlbumBtn.grid(row=0, column=0)
        self.downloadAlbumBtn.configure(background=self.background_color)

        # Main right frame
        self.rightFrame = tk.LabelFrame(self.root, padx=5, pady=9, bd=2, relief='ridge')
        self.rightFrame.grid(row=2, column=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)

        # Preparing start image
        self.logo_image_bytes = Image.open("AlBoomLogo.jpg")
        self.photo_logo = ImageTk.PhotoImage(self.logo_image_bytes)

        # Setting starting image
        self.albumPhoto = tk.Label(self.rightFrame)
        self.albumPhoto['image'] = self.photo_logo
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

    @staticmethod
    def get_captcha_key(url):
        captcha_window = CaptchaWindow(url)
        while True:
            if captcha_window.key != "":
                key = captcha_window.key
                break
        captcha_window.captcha_window.destroy()
        return key

class TokenWindow:
    def __init__(self):
        self.AUTH_URL = ('https://oauth.vk.com/authorize?' +
                         'client_id=4973489&' +
                         'scope=audio&' +
                         'redirect_uri=https://oauth.vk.com/blank.html&' +
                         'display=page&' +
                         'v=5.34&' +
                         'response_type=token')

        self.token_window = tk.Toplevel()
        self.token_window.title('Нужен токен')
        self.token_window.resizable(False, False)

        self.token_instruction = tk.Text(self.token_window)
        self.token_instruction.insert(1.0, 'Дорогой пользователь,\n')
        self.token_instruction.insert(2.0, 'Нам нужно получить токен для скачивания кнопки:\n{}\n'.format(self.AUTH_URL))
        self.token_instruction.insert(3.0, 'After giving your permission you will be redirected\n')
        self.token_instruction.insert(4.0, 'Just paste final url and click on submit btn!\n')
        self.token_instruction.pack()

        self.enter_url_field = tk.Entry(self.token_window)
        self.enter_url_field.pack()
        self.enter_url_field.bind('<Return>', self.get_new_token)

        self.submit_btn = tk.Button(self.token_window, text='Отправить')
        self.submit_btn.pack()
        self.submit_btn.bind('<1>', self.get_new_token)

        self.token = ""
        self.token_url = ""

        webbrowser.open(self.AUTH_URL)

    def get_new_token(self, event):
        self.token_url = self.enter_url_field.get()
        self.token = self.token_url.split('#')[1].split('&')[0].split('=')[1]



def check_token(token):
    api_sub_root = construct_vk_check_token(token)
    conn = http.client.HTTPConnection(VKApiRoot)
    conn.request('GET', api_sub_root)
    response = conn.getresponse()
    byte_data_about_token = response.read()
    json_data_about_token = byte_data_about_token.decode('utf-8')     # getting string from bytes
    parsed_data = json.loads(json_data_about_token)                    # parsing json
    print(parsed_data)
    if 'error' in parsed_data:
        return False
    else:
        return True


def get_token():
    token_window = TokenWindow()
    while True:
        if token_window.token != "":
            token = token_window.token
            break
        time.sleep(2)
    token_window.token_window.destroy()
    return token


class CaptchaWindow:
    def __init__(self, captcha_url):
        self.captcha_window = tk.Toplevel()
        self.captcha_window.title('Captcha')
        self.captcha_window.resizable(False, False)

        self.need_captcha_label = tk.Label(self.captcha_window, text='Что там написано?')
        self.need_captcha_label.pack()

        self.captcha_enter = tk.Entry(self.captcha_window)
        self.captcha_enter.pack()
        self.captcha_enter.bind('<Return>', self.get_key)

        self.submit_btn = tk.Button(self.captcha_window, text='Это')
        self.submit_btn.bind('<1>', self.get_key)
        self.submit_btn.pack()

        self.captcha_display = tk.Label(self.captcha_window)
        captcha_img = main_controller.MainWindowViewController.get_image(captcha_url)
        self.captcha_display.configure(image=captcha_img)
        self.captcha_display.image = captcha_img
        self.captcha_display.pack()

        self.key = ""

    def get_key(self, event):
        self.key = self.captcha_enter.get()
