import pathlib
import sys
import os
from tkinter import *


def newline(n=1):
    for x in range(n):
        print()


class NewFile:

    def __init__(self, Obj, Type, Name, Path, ):
        self.Obj = Obj
        self.Type = Type
        self.Name = Name
        self.Path = Path


class NewFrame:
    def __init__(self, notebook, width, height, bg):
        self.notebook = notebook
        self.width = width
        self.height = height
        self.bg = bg
        self.self = Frame(notebook, width, height, bg)


class SaveClass:
    def __init__(self, bool, newpath, newmat):
        self.bool = bool
        self.newpath = newpath
        self.newmat = newmat


def save():
    print('save')
    return None


def add():
    print('add')
    return None


class NewMenuBar(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bd=1, relief='raised')
        self.master = master
        self.configure(background='black',
                       cursor='hand2')

        # close = Button(self, text='X', command=lambda: root.exit(),
        # background='black',
        # foreground='white')
        # close.pack(side='right')


def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform == "linux":
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"


# create your program's directory

my_datadir = get_datadir() / "SMPCEditor"


class Startup():

    def __init__(self, frame):
        self.frame = frame

        def blank(num):
            for i in range(num):
                Label(frame, text='').pack()

        programversion = 'Beta'
        Label(frame, text='Spiderman Asset Editor', font='lucida 20 bold').pack(fill=BOTH)
        programdesc = 'Spiderman Asset Editor is a program that allows you to modify .model files. For now, ' \
                      'you can change strings (path and name) in order to nullify specific slots, or change materials ' \
                      'of specific slots. ' \
                      'Please note that files are only supposed to be opened and edited ' \
                      'in one session, opening a previously edited file will not work properly. If you have a bug, ' \
                      'or want to request a feature, ' \
                      'click on Help -> Report a bug/Request a feature.'
        Label(frame, text=programdesc, font='lucida 14', wraplength=1080).pack(fill=BOTH)
        blank(1)

        Label(frame, text="What's new in version " + str(programversion), font='lucida 20 bold').pack(fill=BOTH)
        changes = []
        changes.append('Added the ability to edit strings')
        changes.append('Added proper GUI')
        changes.append('Added the ability to save files')
        for i in changes:
            Label(frame, font='lucida 12', text='- ' + i).pack(fill=BOTH)

        blank(1)

        Label(frame, text="Notes about version " + str(programversion), font='lucida 20 bold').pack(fill=BOTH)
        notes = []
        notes.append('Allows editing strings with strings of the same length (or less)')
        notes.append("Allows saving of files (I recommend 'ogfilename.new')")
        notes.append("Only allows for 1 file to be open at a time")
        notes.append("Includes light and dark theme (View menu to change theme)")
        for i in notes:
            Label(frame, font='lucida 12', text='- ' + i).pack(fill=BOTH)

        blank(1)

        Label(frame, text="What's next?", font='lucida 20 bold').pack(fill=BOTH)
        next = []
        next.append('Support for multiple files to be open at one time')
        next.append('The option to fully customize materials (amount, string size, etc)')
        for i in next:
            Label(frame, font='lucida 12', text='- ' + i).pack(fill=BOTH)
