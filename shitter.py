from tkinter import *

root = Tk()

text = Text(root)
text.insert(INSERT, "Hello, world!\n")
text.insert(END, "This is a phrase.\n")
text.insert(END, "Bye bye...")
text.pack(expand=1, fill=BOTH)

# adding a tag to a part of text specifying the indices
text.tag_add("start", "1.8", "1.13")
text.tag_config("start", background="black", foreground="yellow")

root.mainloop()

