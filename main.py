import sys
import struct
import atexit
import tkinterdnd2
from tkinter import *
from tkinter import ttk
from tkinterdnd2 import *
from functions import *
global my_notebook
global root
global event

# Open to see functions I used
def UInt32(f):
    intvar = (struct.unpack("<I", f.read(4))[0])
    return intvar


def Int32(f):
    intvar = (struct.unpack("<i", f.read(4))[0])
    return intvar


def UInt16(f):
    intvar = (struct.unpack("<H", f.read(2))[0])
    return intvar


def Int16(f):
    intvar = (struct.unpack("<h", f.read(2))[0])
    return intvar


def Float(f):
    intvar = (struct.unpack("<f", f.read(4))[0])
    return intvar


def UInt64(f):
    intvar = (struct.unpack("<L", f.read(8))[0])
    return intvar


def Int64(f):
    intvar = (struct.unpack("<l", f.read(8))[0])
    return intvar


def Byte(f):
    intvar = (struct.unpack("<B", f.read(2))[0])
    return intvar


def advance(f, a=1):
    f.seek(f.tell() + a)


def back(f, a=1):
    f.seek(f.tell() - a)


def newline(n=1):
    for x in range(n):
        print()


# if sys.argv[1] is None:
#     print(
#         "You didn't open this program with a file, either drag a .model onto the program to drag it as your arg in cmd")
#     input("Press Enter to close...")
#     sys.exit()

def drop_Func(event):
    dragFile(my_notebook, root, event.data)



root = tkinterdnd2.Tk()
root.title('Spiderman Editor')
root.call('wm', 'iconphoto', root._w, PhotoImage(file='smpceditoricon.png'))

style=ttk.Style()
style.layout("TNotebook", [])
style.configure("TNotebook", highlightbackground="#848a98",tabmargins=0)

my_notebook = ttk.Notebook(root, padding=0, style="TNotebook")
my_notebook.pack(fill=BOTH, expand=TRUE)
my_notebook.enable_traversal()

IFrame = Frame(width=1200, height=800, bg="#232023", bd=0, highlightthickness=0, relief='ridge')
IFrame.drop_target_register(DND_FILES)
IFrame.dnd_bind('<<Drop>>', drop_Func)
#IFrame.
my_notebook.add(IFrame, text="Startup")

# closebutton=tkinter.Button(IFrame, text="Close File", anchor=NE)
# closebutton.pack(fill=BOTH)



#canvas = Canvas(root, height=800, width=1200, bg="#232023", bd=0, highlightthickness=0, relief='ridge')
#canvas = Canvas(my_notebook.page1)
#canvas.pack(fill="both", expand=True)


menubar = Menu(root)
root.config(menu=menubar)


file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open File", command=lambda: openFile(my_notebook, root))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=donothing)
edit_menu.add_command(label="Copy", command=donothing)
edit_menu.add_command(label="Paste", command=donothing)

status = Label(root, text="Version 1.00" + "by bleedn", bg="#000000", fg="#bec2cb")
status.pack(fill=BOTH)


root.configure(bg="#000000")
root.mainloop()

def exit_handler():
    try:
        File.Obj.close
        print(my_notebook.tabs())
    except:
        pass

atexit.register(exit_handler)
# try:
#     file = sys.argv[1]
#     f = open(file, 'rb')
#     f.seek(44)
#     fileSize = Int32(f)
#     sectionsamount = UInt32(f)
#     endstringseco = 0
#     endstringstatico = 0
#     for i in range(sectionsamount):
#         inlist = False
#         sectiontype = UInt32(f)
#         sectionoffset = UInt32(f)
#         sectionsize = UInt32(f)
#         if sectiontype == 4023987816:
#             endstringseco = sectionoffset
#         elif sectiontype == 675087235:
#             endstringstatico = sectionoffset
#     f.seek(52 + (sectionsamount * 12) + 17)
#     if not endstringseco == 0:
#         stringread = (endstringseco + 40) - (52 + (sectionsamount * 12) + 17)
#     else:
#         stringread = (endstringstatico + 40) - (52 + (sectionsamount * 12) + 17)
#     strings = f.read(stringread - 4)
#     strings = strings.decode('utf-8')
#     DataEntrys = strings.split("\x00")
#     MaterialPaths = []
#     for i in DataEntrys:
#         if ".material" in i:
#             MaterialPaths.append(DataEntrys.index(i))
#
#     if not MaterialPaths:
#         print("Model has no material slots")
#     else:
#         for loop, i in enumerate(MaterialPaths):
#             print("Material Slot " + str(loop) + ": " + str(DataEntrys[i]))
#
# except:
#     print('error')
#     pass
#
# input("Press Enter to close...")
# f.close()
# sys.exit()
