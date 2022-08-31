import tkinterdnd2
from tkinter import ttk
from functions import *
global my_notebook
global root
global event
from sys import exit


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
root.title('Spiderman Asset Editor')
#root.iconbitmap('./smpceditoricon.ico')

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


menubar = Menu(root)
root.config(menu=menubar)


file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open File", command=lambda: openFile(my_notebook, root))
file_menu.add_command(label="Save File", command=lambda: saveFile(my_notebook, root, True))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit)

edit_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=donothing)
edit_menu.add_command(label="Copy", command=donothing)
edit_menu.add_command(label="Paste", command=donothing)

about_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=about_menu)
about_menu.add_command(label="About", command=aboutinfo)


status = Label(root, text="Version 1.00" + "by bleedn", bg="#000000", fg="#bec2cb")
status.pack(fill=BOTH)

undo=True
autoseparators=True
maxundo=-1

def on_closing():
    if not len(my_notebook.tabs())>1:
        root.destroy()
        pass
        return
    savev = saveFile(my_notebook, root, False)
    if savev.bool == True :
        root.destroy()
        pass
    else:
        if messagebox.askokcancel("Quit", "Are you sure you want to quit? You have unsaved files!"):
            root.destroy()
        else:
            pass

root.protocol("WM_DELETE_WINDOW", on_closing)
root.configure(bg="#000000")
root.mainloop()

# try:
#     file = sys.argv[1]
#     f = open(file, 'rb')
#
#
# input("Press Enter to close...")
# f.close()
# sys.exit()
