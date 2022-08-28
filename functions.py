import struct
import pathlib
from tkinter import filedialog, Text
import os
from classes import *
from tkinterdnd2 import *
import json
import binascii

TabID = []
TabOBJ = []
File = ''
NCan = ''
NFrame = ''
secTypeArr = [140084797, 2027539422, 2844518043, 1488475530, 1242726946, 3842054255]
# The corresponding names, probably not the best way to do it, but
secNameArr = ["Vertices", "Model Information", "Faces", "Config End", "Config Beginning", "Config Data"]
configtypeArr = [10, 12]
OffsetData = ["Data Table", "Awards"]
configdatao = 0
DataEntrys = 0


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


def openFile(notebook, root):
    global File
    global NCan
    global NFrame
    global TabOBJ
    global TabID
    fo = filedialog.askopenfilename(title="Select File", filetypes=(("config files", "*.config"), ("all files", "*")))
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


def donothing():
    pass


def Get_Info(file):
    global ConfigData
    global configdatao
    global DataEntrys
    try:
        OffsetData.clear()
        f = file
        f.seek(44)
        fileSize = Int32(f)
        print("File Size: " + str(fileSize))
        sectionsamount = UInt32(f)
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
                if secTypeArr.index(sectiontype) == 4:
                    configbegino = sectionoffset
                    configbegins = sectionsize
                    # print("Section offset of config begin = " + str(configbegino))
                elif secTypeArr.index(sectiontype) == 5:
                    configdatao = sectionoffset
                    configdatas = sectionsize
                    # print("Section offset of config data = " + str(configdatao))
                    # print("Section size of config data = " + str(configdatas))

        f.seek(configbegino + 40)

        blankl = 0
        while True:
            blankl += 1
            back(f)
            byte = f.read(1)
            if byte == b'\x00':
                pass
            else:
                blankl -= 1
                break
            back(f)
        # print(blankl)
        stringendpos = configbegino - blankl + 40
        # print(stringendpos)
        stringsize = stringendpos - (52 + (sectionsamount * 12) + 18)
        # print(stringsize)

        f.seek(52 + (sectionsamount * 12) + 18)
        strings = f.read(stringsize)
        strings = strings.decode('utf-8')
        DataEntrys = strings.split("\x00")
        # print(stringsize)
        f.seek(52 + (sectionsamount * 12) + 18)
        for i in DataEntrys:
            StringLen = len(i)
            OffsetData.append(f.tell() - 36)
            advance(f, StringLen + 1)
        print(DataEntrys)
        previous = f.tell()
        f.seek(configdatao + 40)
        ConfigData = File.Obj.read(configdatas)
        f.seek(previous)
        Get_Data()


    except:
        print("errorfunc")
        pass


def Get_Data():
    # global ConfigData
    try:
        # UOffsetData = []
        # print(OffsetData)
        # print(ConfigData)
        hexvar = 70
        hexvar = hex(hexvar)
        print(hexvar)
        # for i in OffsetData:
        #     hex_val = str(i)
        #     #print(hex_val)
        #     print(unhexlify(hex_val))

    except:
        pass
        print("error data")


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
            Get_Info(File.Obj)

        except:
            pass
            print("error")
    else:
        try:
            del CheckFile
            notebook.select(TabID[index])
        except:
            print("error")
