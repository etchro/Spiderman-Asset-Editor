from tkinter import *
class NewFile:

    def __init__(self, Obj, Type, Name, Path,):
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

