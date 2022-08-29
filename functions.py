import struct
import pathlib
from tkinter import filedialog, Text
import os
from classes import *
from tkinterdnd2 import *
import json
import binascii
from tkinter.messagebox import showerror, showwarning, showinfo
import torch

global MaterialAmount
global Materials
global MaterialPaths
global LabelColl
global EntryColl
global NewMaterialPaths
global ButtonColl

TabID = []
TabOBJ = []
File = ''
NCan = ''
NFrame = ''
secTypeArr = [140084797, 2027539422, 2844518043, 1488475530, 1242726946, 3842054255, 844151680, 4023987816, 675087235]
# The corresponding names, probably not the best way to do it, but
secNameArr = ["Vertices", "Model Information", "Faces", "Config End", "Config Beginning", "Config Data", "Materials"]
configtypeArr = [10, 12]
OffsetData = ["Data Table", "Awards"]
configdatao = 0
DataEntrys = 0


def callback(input):
    if input.isdigit():
        return True

    elif input == "":
        return True

    else:
        return False
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
    intvar = (struct.unpack("<Q", f.read(8))[0])
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
def aboutinfo():
    showinfo(title='About', message="This program was made to edit assets from Spiderman PC, by bleedn#3333 on discord, and is currently in version (Alpha)!")
def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)
def openFile(notebook, root):
    global File
    global NCan
    global NFrame
    global TabOBJ
    global TabID
    fo = filedialog.askopenfilename(title="Select File", filetypes=(("model files", "*.model"), ("all files", "*")))
    exists = False
    CheckFile = NewFile(open(fo, 'rb'), pathlib.Path(fo).suffix, os.path.basename(str(fo)), fo)
    if CheckFile.Name in TabOBJ:
        exists = True
        index = TabOBJ.index(CheckFile.Name)
    if not exists:
        try:
            File = NewFile(open(fo, 'rb'), pathlib.Path(fo).suffix, os.path.basename(str(fo)), fo)
            NFrame = Frame(width=1200, height=800, bg="#232023")
            notebook.add(NFrame, text=File.Name)
            TabOBJ.append(File.Name)
            intvar = len(notebook.tabs())
            intvar -= 1
            TabID.append(intvar)
            print(TabID)
            selectvar = TabID.index(intvar)
            notebook.select(TabID[selectvar])
        except:
            pass
            print("error")
    else:
        try:
            del CheckFile
            notebook.select(TabID[index])
        except:
            print("error")
def setText(e, t):
    e.delete(0,END)
    e.insert(0,t)


def donothing():
    pass


def Get_Info(file, ftype):
    global ConfigData
    global configdatao
    global DataEntrys
    try:
        # Get Header Information
        OffsetData.clear()
        f = file
        f.seek(44)
        fileSize = Int32(f)
        print("File Size: " + str(fileSize))
        sectionsamount = UInt32(f)
        endstringseco = 0
        endstringstatico = 0
        print("Amount of sections: " + str(sectionsamount))
        newline()

        for i in range(sectionsamount):
            inlist = False
            sectiontype = UInt32(f)
            if sectiontype in list(secTypeArr):
                inlist = True
            sectionoffset = UInt32(f)
            sectionsize = UInt32(f)
            if inlist:
                if secTypeArr.index(sectiontype) == 6:
                    matoffset = sectionoffset
                    matsize = sectionsize
                if secTypeArr.index(sectiontype) == 7:
                    endstringseco = sectionoffset
                if secTypeArr.index(sectiontype) == 8:
                    endstringstatico = sectionoffset


        if ftype == '.model':
            if matsize >= 32:

                f.seek(52 + (sectionsamount * 12) + 17)
                if not endstringseco == 0:
                    stringread = (endstringseco + 40) - (52 + (sectionsamount * 12) + 17)
                else:
                    stringread = (endstringstatico + 40) - (52 + (sectionsamount * 12) + 17)
                strings = f.read(stringread - 4)
                strings = strings.decode('utf-8')
                DataEntrys = strings.split("\x00")
                print(DataEntrys)

                f.seek(matoffset + 36)
                MaterialPathOffsets = []
                MaterialOffsets = []
                global MaterialAmount
                MaterialAmount = round(matsize/32)
                global Materials
                Materials = []
                global MaterialPaths
                MaterialPaths = []
                print("# of Materials: " + str(MaterialAmount))
                for i in range(MaterialAmount):
                    MaterialPathOffsets.append(UInt32(f)+36)
                    advance(f, 4)
                    MaterialOffsets.append(UInt32(f)+36)
                    advance(f, 4)
                for loop, i in enumerate(MaterialOffsets):
                    f.seek(i)
                    strlength=0
                    while True:
                        byte = f.read(1)
                        if not byte == b'\x00':
                            pass
                            strlength+=1
                        else:
                            back(f, 1)
                            break
                    f.seek(i)
                    stringv = str(f.read(strlength))
                    stringv = stringv[2:-1]
                    Materials.append(stringv)
                print("Materials: " + str(Materials))
                for loop, i in enumerate(MaterialPathOffsets):
                    f.seek(i)
                    strlength = 0
                    while True:
                        byte = f.read(1)
                        if not byte == b'\x00':
                            pass
                            strlength+=1
                        else:
                            back(f, 1)
                            break
                    f.seek(i)
                    strings = f.read(strlength)
                    strings = strings.decode('UTF-8')
                    MaterialPaths.append(strings)
                # print(*MaterialPaths)

                global LabelColl
                global EntryColl
                global ButtonColl
                LabelColl = []
                EntryColl = []
                ButtonColl = []
                reg=NFrame.register(callback)
                for loop, i in enumerate(MaterialPaths):
                    print("Material Slot " + str(loop) + ": " + i)
                    lv = Label(NFrame, text="Material " + str(loop) + " Path:").grid(row=loop,column=1, sticky=W)
                    LabelColl.append(lv)
                    var = StringVar()
                    var.set(i)
                    width = len(i)
                    width = round(width)
                    width = clamp(width, 1, 1080)
                    entryvar = Entry(NFrame, textvariable=var, width=width, validate="key", validatecommand=(reg, '% P'))
                    entryvar.grid(row=loop, column=2, sticky=W)
                    def Reset(id):
                        stringv2 = MaterialPaths[id]
                        setText( EntryColl[id], stringv2)

                    EntryColl.append(entryvar)
                    b = Button(NFrame, text="Reset Material Path", command=lambda x=loop: Reset(x)).grid(row=loop, column=3, sticky=W)
                #vsb = Scrollbar(NFrame)
                #vsb.grid(row=i, column=3, sticky=NE)


    except:
        print("errorfunc")
        pass




def drop_Func2(event, notebook, root):
    dragFile(notebook, root, event.data)


def dragFile(notebook, root, f):
    global File
    global NCan
    global NFrame
    global TabOBJ
    global TabID
    global configbegino
    global configbegins
    print(f)
    fo = f
    exists = False
    CheckFile = NewFile(open(fo, 'rb'), pathlib.Path(fo).suffix, os.path.basename(str(fo)), fo)
    if CheckFile.Name in TabOBJ:
        exists = True
        index = TabOBJ.index(CheckFile.Name)
    if not exists:
        try:
            if pathlib.Path(fo).suffix == '.model':
                File = NewFile(open(fo, 'rb'), pathlib.Path(fo).suffix, os.path.basename(str(fo)), fo)
                NFrame = Frame(width=1200, height=800, bg="#232023")
                NFrame.drop_target_register(DND_FILES)
                NFrame.dnd_bind('<<Drop>>', lambda x: drop_Func2(event=x, notebook=notebook, root=root))
                notebook.add(NFrame, text=File.Name)
                TabOBJ.append(File.Name)
                intvar = len(notebook.tabs())
                intvar -= 1
                TabID.append(intvar)
                print(TabID)
                selectvar = TabID.index(intvar)
                notebook.select(TabID[selectvar])
                print("GetInfo")
                Get_Info(File.Obj, File.Type)
                del CheckFile
            else:
                showinfo(title='Info', message="For now, only .model files are supported, more will be added in later versions!")

        except:
            pass
            print("error")
    else:
        try:
            del CheckFile
            notebook.select(TabID[index])
        except:
            print("error")

def saveFile(notebook, root):
    try:
        global MaterialPaths
        global NewMaterialPaths
        NewMaterialPaths = []
        x = True
        while x:
            for i in range(MaterialAmount):
                givelen = len(EntryColl[i].get())
                expeclen = len(MaterialPaths[i])
                entrytoadd = EntryColl[i].get()
                if givelen > expeclen:
                    #message = 'Mismatch string at material '
                    messagevar ='Mismatched string sizes in Material ' + str(i)+ ', expected ' + str(expeclen) + ", got " + str(givelen)
                    showerror(title='Mismatched string sizes', message=messagevar)
                    x = False
                elif givelen < expeclen:
                    amounttopad=expeclen-givelen
                    entrytoadd+=" "*amounttopad
                    NewMaterialPaths.append(entrytoadd)
                elif givelen == expeclen:
                    NewMaterialPaths.append(entrytoadd)
                if i == MaterialAmount-1:
                    x = False
        for i in NewMaterialPaths:
            print(i)
    except:
        print("error saving file")
        pass