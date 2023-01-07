# import what you need from tkinter module
from tkinter import Tk, Button, PhotoImage, Label, LabelFrame, W, E, N, S, Entry, END, StringVar, Scrollbar, Toplevel
from tkinter import ttk    # Provides access to the Tk themed widgets.

class Contacts:
    def __init__(self,root):
        self.root = root
        self.create_left_icon()

    def create_left_icon(self):
        photo = PhotoImage(file='E:\Tkinter Tutorial\Contacts\icons\logo.gif')
        label = Label(image=photo)
        label.image = photo
        label.grid(row=0,column=0)


if __name__ == '__main__':
    root  = Tk()
    root.title('My Contacts List')
    application = Contacts(root)
    root.mainloop()
