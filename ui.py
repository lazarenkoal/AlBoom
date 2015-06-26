from tkinter import *

root = Tk()
root.title('Music scooper')
root.geometry('680x420')

singer_name = StringVar()
singer = Entry(root, textvariable=singer_name)
singer.pack()
singer.place(x=20, y=20, width = 100)

chosen = StringVar()

singer_listbox = Listbox(root, width = 25, height=20, selectmode = SINGLE)

def select():
    chosen=singer_listbox.get(singer_listbox.curselection())
    #searching songs
    songs_listbox = Listbox(root, width = 25, height=20, selectmode = MULTIPLE)
    songs_listbox.pack()
    songs_listbox.place(x=370, y=60, width = 200)

def show_listbox():
    singer_listbox.pack()
    singer_listbox.place(x=20, y=60,width = 200)
    s=singer_name.get()
    singer_listbox.insert(1,'a')
    singer_listbox.insert(2,'b')
    singer_listbox.insert(3,'c')
    select_from_found=Button(text = "Select", command =select)
    select_from_found.pack()
    select_from_found.place(x=250, y=60)
    #searching singers, getting an array of strings
    #inserting elements from the array

search_singer = Button(text = "Search", command = show_listbox)
search_singer.pack()
search_singer.place(x=130, y = 20)

root.update()
root.mainloop()