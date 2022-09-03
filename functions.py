import struct
import pathlib
from tkinter import filedialog, messagebox
import os
from tkinter.filedialog import asksaveasfile
import math
from tkinter import ttk

from classes import *
from tkinterdnd2 import *
from tkinter.messagebox import showerror, showwarning, showinfo

global OffsetData
global DataEntrys

global MaterialAmount
global Materials
global MaterialPaths
global LabelColl
global LabelColl2
global EntryColl
global NewMaterialPaths
global ButtonColl
global LabelColl

global MatLabelColl
global MatLabelColl2
global MatEntryColl
global MatButtonColl

global NewMaterials
global Open  # Globals

Open = False

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
DataEntrys = 0  # Variables


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


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def setText(e, t):
    e.delete(0, END)
    e.insert(0, t)


def donothing():
    pass  # Functions


def Get_Info(file, ftype):
    global ConfigData
    global configdatao
    global DataEntrys
    global OffsetData
    OffsetData = []
    # try:
    # Get Header Information
    OffsetData.clear()
    f = file
    f.seek(44)
    fileSize = Int32(f)
    # print("File Size: " + str(fileSize))
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
            f.seek(52 + (sectionsamount * 12) + 17)
            for i in DataEntrys:
                StringLen = len(i)
                OffsetData.append(f.tell())
                advance(f, StringLen + 1)

            f.seek(matoffset + 36)
            MaterialPathOffsets = []
            MaterialOffsets = []
            global MaterialAmount
            MaterialAmount = round(matsize / 32)
            global Materials
            Materials = []
            global MaterialPaths
            MaterialPaths = []
            for i in range(MaterialAmount):
                MaterialPathOffsets.append(UInt32(f) + 36)
                advance(f, 4)
                MaterialOffsets.append(UInt32(f) + 36)
                advance(f, 4)
            for loop, i in enumerate(MaterialOffsets):
                f.seek(i)
                strlength = 0
                while True:
                    byte = f.read(1)
                    if not byte == b'\x00':
                        pass
                        strlength += 1
                    else:
                        back(f, 1)
                        break
                f.seek(i)
                stringv = str(f.read(strlength))
                stringv = stringv[2:-1]
                Materials.append(stringv)
            for loop, i in enumerate(MaterialPathOffsets):
                f.seek(i)
                strlength = 0
                while True:
                    byte = f.read(1)
                    if not byte == b'\x00':
                        pass
                        strlength += 1
                    else:
                        back(f, 1)
                        break
                f.seek(i)
                strings = f.read(strlength)
                strings = strings.decode('UTF-8')
                MaterialPaths.append(strings)
            # print(*MaterialPaths)

            global LabelColl
            global LabelColl2
            global EntryColl
            global ButtonColl

            global MatLabelColl
            global MatLabelColl2
            global MatEntryColl
            global MatButtonColl

            LabelColl = []
            LabelColl2 = []
            EntryColl = []
            ButtonColl = []

            MatLabelColl = []
            MatLabelColl2 = []
            MatEntryColl = []
            MatButtonColl = []
            reg = NFrame.register(callback)
            rowvar = 0
            for loop, i in enumerate(MaterialPaths):
                rowvar += 1
                lv = ttk.Label(NFrame, text="Material " + str(loop) + " Path:").grid(row=rowvar, column=1, sticky=W)
                LabelColl.append(lv)
                var = StringVar()
                var.set(i)
                width = len(i)
                width = round(width)
                width = clamp(width, 1, 1080)

                def KeyPressed(id):
                    length = (len(MaterialPaths[id])) - (len(EntryColl[id].get()))
                    LabelColl2[id].config(text=str(length))
                    if length < 0:
                        LabelColl2[id].config(fg='red')
                    else:
                        LabelColl2[id].config(fg='white')

                entryvar = Entry(NFrame, textvariable=var, width=width, validate="key",
                                 validatecommand=(reg, '% P'))

                entryvar.grid(row=rowvar, column=2, sticky=W)

                llb = Label(NFrame, text="Placeholder", bg="#232023", fg='white')
                llb.grid(row=rowvar, column=3, sticky=W)
                LabelColl2.append(llb)

                def Reset(id):
                    stringv2 = MaterialPaths[id]
                    setText(EntryColl[id], stringv2)

                def Clear(id):
                    stringv2 = MaterialPaths[id]
                    setText(EntryColl[id], "")

                def FocusFrame(event):
                    NFrame.focus_set()

                EntryColl.append(entryvar)
                entryvar.bind("<KeyRelease>", lambda event, x=EntryColl.index(entryvar): KeyPressed(x))
                entryvar.bind("<Return>", FocusFrame)
                b = Button(NFrame, text="Reset Material Path", command=lambda x=loop: [Reset(x), KeyPressed(x)])
                b.grid(row=rowvar, column=4, sticky=W)
                ButtonColl.append(b)
                b = Button(NFrame, text="Clear Material Path", command=lambda x=loop: [Clear(x), KeyPressed(x)])
                b.grid(row=rowvar, column=5, sticky=W)
                KeyPressed(loop)

                rowvar += 1
                lv = Label(NFrame, text="Material " + str(loop) + " Name:").grid(row=rowvar, column=1, sticky=W)
                MatLabelColl.append(lv)
                var = StringVar()
                var.set(Materials[loop])
                width = len(Materials[loop])
                width = round(width)
                width = clamp(width, 1, 1080)

                def KeyPressed2(id):
                    length = (len(Materials[id])) - (len(MatEntryColl[id].get()))
                    MatLabelColl2[id].config(text=str(length))
                    if length < 0:
                        MatLabelColl2[id].config(fg='red')
                    else:
                        MatLabelColl2[id].config(fg='white')

                entryvar = Entry(NFrame, textvariable=var, width=width, validate="key",
                                 validatecommand=(reg, '% P'))

                entryvar.grid(row=rowvar, column=2, sticky=W)

                llb = Label(NFrame, text="Placeholder", bg="#232023", fg='white')
                llb.grid(row=rowvar, column=3, sticky=W)
                MatLabelColl2.append(llb)

                def Reset2(id):
                    stringv2 = Materials[id]
                    setText(MatEntryColl[id], stringv2)

                def Clear2(id):
                    stringv2 = Materials[id]
                    setText(MatEntryColl[id], "")

                def FocusFrame2(event):
                    NFrame.focus_set()

                MatEntryColl.append(entryvar)
                entryvar.bind("<KeyRelease>", lambda event, x=MatEntryColl.index(entryvar): KeyPressed2(x))
                entryvar.bind("<Return>", FocusFrame2)
                b = Button(NFrame, text="Reset Material Name", command=lambda x=loop: [Reset2(x), KeyPressed2(x)])
                b.grid(row=rowvar, column=4, sticky=W)
                MatButtonColl.append(b)
                b = Button(NFrame, text="Clear Material Slot Name", command=lambda x=loop: [Clear2(x), KeyPressed2(x)])
                b.grid(row=rowvar, column=5, sticky=W)
                KeyPressed2(loop)

            # Add a canvas in that frame
            # canvas = Canvas(NFrame, bg="yellow")
            # canvas.grid(row=0, column=0, sticky="news")

            # Link a scrollbar to the canvas
            # vsb = Scrollbar(orient=VERTICAL, command=NFrame.yview)
            # vsb.grid(row=1, column=6, sticky='ns', in_=NFrame)
            # NFrame.configure(yscrollcommand=vsb.set)
            # grid.configure
            # NFrame.configure(yscrollcommand=vsb.set)
            # NFrame.config(scrollregion=NFrame.bbox("all"))

            # vsb = Scrollbar(NFrame)
            # vsb.grid(column=6, row=1, rowspan=50, sticky=N + S + W)

    #
    # except:
    #     print("errorfunc")
    #     pass


def drop_Func2(event, notebook, root):
    dragFile(notebook, root, event.data, True)


def dragFile(notebook, root, f, dragged):
    global Open
    global File
    global NCan
    global NFrame
    global TabOBJ
    global TabID
    global configbegino
    global configbegins

    if dragged:
        fo = f
    else:
        fo = filedialog.askopenfilename(title="Select File", filetypes=(("model files", "*.model"), ("all files", "*")))
    exists = False
    CheckFile = NewFile(open(fo, 'rb'), pathlib.Path(fo).suffix, os.path.basename(str(fo)), fo)
    if CheckFile.Name in TabOBJ:
        exists = True
        index = TabOBJ.index(CheckFile.Name)
        del CheckFile
        notebook.select(TabID[index])
        return
    if not len(notebook.tabs()) == 2:
        pass
    else:
        saved = saveFile(notebook, root, False)
        messageboxv = messagebox.askquestion('Open File', 'Are you sure you want to open a new file?')
        if messageboxv == 'yes':
            print(TabOBJ)
            print(os.path.basename(str(fo)))
            TabOBJ.remove(notebook.tab(1, "text"))
            notebook.forget(1)
            #TabOBJ
            pass
        else:
            return
    Open = True
    print(f)

    # try:
    if pathlib.Path(fo).suffix == '.model':
        File = NewFile(open(fo, 'rb'), pathlib.Path(fo).suffix, os.path.basename(str(fo)), fo)

        # Create Main Frame
        main_frame = Frame(notebook, width=1200, height=800)
        main_frame.drop_target_register(DND_FILES)
        main_frame.dnd_bind('<<Drop>>', lambda x: drop_Func2(event=x, notebook=notebook, root=root))

        def get_datadir() -> pathlib.Path:
            home = pathlib.Path.home()
            if sys.platform == "win32":
                return home / "AppData/Roaming"
            elif sys.platform == "linux":
                return home / ".local/share"
            elif sys.platform == "darwin":
                return home / "Library/Application Support"
        my_datadir = get_datadir() / "SMPCEditor"
        completename = os.path.join(my_datadir, 'VersionInfo' + '.txt')
        versioninfo = open(completename, 'r')
        currentversion = versioninfo.read()
        versioninfo.close()
        status = Label(main_frame, text="Version " + str(currentversion), bg="#000000", fg="#bec2cb").pack(fill=BOTH, side=BOTTOM)
        # put the main frame into notebook
        notebook.add(main_frame, text=File.Name)

        # Create canvas inside main frame
        my_canvas = Canvas(main_frame, highlightthickness=0)
        my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        # Create ScrollBar inside main frame
        my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        # my_scrollbar2 = Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
        # my_scrollbar2.pack(side=BOTTOM, fill=X)

        # def _on_mousewheel(event):
        #     shift = (event.state & 0x1) != 0
        #     scroll = -1 if event.delta > 0 else 1
        #     if shift:
        #         my_canvas.xview_scroll(scroll, "units")
        #     else:
        #         my_canvas.yview_scroll(scroll, "units")

        my_canvas.configure(yscrollcommand=my_scrollbar.set)
        # my_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Creating Frame to show the Canvas
        NFrame = Frame(my_canvas, width=1200, height=800)
        NFrame.drop_target_register(DND_FILES)
        NFrame.dnd_bind('<<Drop>>', lambda x: drop_Func2(event=x, notebook=notebook, root=root))
        # Showing Canvas into/as a Frame
        NFrame.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
        #my_canvas.configure(width=NFrame.winfo_width(), height=NFrame.winfo_height())
        my_canvas.create_window((0, 0), window=NFrame, anchor="nw")


        # canvas = Canvas(container, width=200, height=400)
        # scroll = Scrollbar(container, command=canvas.yview)
        # canvas.config(yscrollcommand=scroll.set, scrollregion=(0, 0, 100, 1000))
        # canvas.pack(side=LEFT, fill=BOTH, expand=True)
        # scroll.pack(side=RIGHT, fill=Y)
        # canvas.create_window(100, 500, window=NFrame)

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
        showinfo(title='Info',
                 message="For now, only .model files are supported, more will be added in later versions!")

    # except:
    #     pass
    #     print("error")


def saveFile(notebook, root, bool):
    # try:
    f = File.Obj
    global MaterialPaths
    global NewMaterialPaths
    global NewMaterials
    NewMaterialPaths = []
    NewMaterials = []
    x = True
    while x:
        for i in range(MaterialAmount):
            givelen = len(EntryColl[i].get())
            expeclen = len(MaterialPaths[i])
            entrytoadd = EntryColl[i].get()
            if givelen > expeclen:
                # message = 'Mismatch string at material '
                messagevar = 'Mismatched string sizes in Material Path ' + str(i) + ', expected ' + str(
                    expeclen) + ", got " + str(givelen)
                showerror(title='Mismatched string sizes', message=messagevar)
                x = False
                return
            elif givelen < expeclen:
                amounttopad = expeclen - givelen
                entrytoadd += "\0" * amounttopad
                NewMaterialPaths.append(entrytoadd)
            elif givelen == expeclen:
                NewMaterialPaths.append(entrytoadd)
            if i == MaterialAmount - 1:
                x = False
    y = True
    while y:
        for i in range(MaterialAmount):
            givelen = len(MatEntryColl[i].get())
            expeclen = len(Materials[i])
            entrytoadd = MatEntryColl[i].get()
            if givelen > expeclen:
                # message = 'Mismatch string at material '
                messagevar = 'Mismatched string sizes in Material ' + str(i) + ', expected ' + str(
                    expeclen) + ", got " + str(givelen)
                showerror(title='Mismatched string sizes', message=messagevar)
                y = False
                return
            elif givelen < expeclen:
                amounttopad = expeclen - givelen
                entrytoadd += "\0" * amounttopad
                NewMaterials.append(entrytoadd)
            elif givelen == expeclen:
                NewMaterials.append(entrytoadd)
            if i == MaterialAmount - 1:
                y = False
    if bool == True:
        f.seek(0, os.SEEK_END)
        end = f.tell()
        f.seek(0)
        global DataEntrys
        offsetlist = []
        strtype = []
        indexarr = []
        for loop, i in enumerate(DataEntrys):
            if i in MaterialPaths:
                offsetlist.append(OffsetData[DataEntrys.index(i)])
                strtype.append('l')
            elif i in Materials:
                offsetlist.append(OffsetData[DataEntrys.index(i)])
                strtype.append('m')

        ogfile = b''
        print(offsetlist)
        print(strtype)
        for loop, i in enumerate(offsetlist):
            print(i)
            if strtype[loop] == "m":
                total = i - (f.tell())
                ogfile += f.read(total)
                index = math.floor(offsetlist.index(i) / 2)
                ata = len(Materials[index])
                if i == offsetlist[-1]:
                    ogfile += NewMaterials[index].encode()
                    advance(f, ata)
                    left = end - f.tell()
                    ogfile += f.read(left)
                    pass
                else:
                    index = math.floor(offsetlist.index(i) / 2)
                    ogfile += NewMaterials[index].encode()
                    advance(f, ata)
            else:
                total = i - (f.tell())
                ogfile += f.read(total)
                index = math.floor(offsetlist.index(i) / 2)
                ata = len(MaterialPaths[index])
                if i == offsetlist[-1]:
                    ogfile += NewMaterialPaths[index].encode()
                    advance(f, ata)
                    left = end - f.tell()
                    ogfile += f.read(left)
                    pass
                else:
                    index = math.floor(offsetlist.index(i) / 2)
                    ogfile += NewMaterialPaths[index].encode()
                    advance(f, ata)

        initial = str(File.Name + "_new" + File.Type)
        # fn = asksaveasfile(initalfile = initial, defaultextension=".model",filetypes=[("All Files","*.*"),("Model Files","*.model")])
        nf = asksaveasfile(mode='wb', defaultextension=".model",
                           filetypes=(("Model Files", "*.model"), ("All Files", "*.*")), title='Select file to save as')
        if nf is None:
            return
        try:
            nf.write(ogfile)
            newname = os.path.basename(nf.name)
            notebook.tab(1, text=newname)
            nf.close()
            showinfo(title='Success saving file', message="Succesfully saved file to: " + str(nf.name))
        except Exception as e:
            showerror(title='Error saving file', message='There was an error saving the file: ' + repr(e))
        # print(f.read())
        # for loop, i in enumerate(NewMaterials):
        #     encoded = i.encode()
        #     btf = Materials[loop].encode()
        #     print(btf)
        #     ogfile = ogfile.replace(btf, encoded)
        #     print(ogfile)
    else:
        if NewMaterials == Materials and NewMaterialPaths == MaterialPaths:
            saveobj = SaveClass(True, NewMaterialPaths, NewMaterials)
            return (saveobj)
        else:
            saveobj = SaveClass(False, NewMaterialPaths, NewMaterials)
            return (saveobj)
    # except:
    #     print("error saving file")
    #     pass
