import sys
import struct


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


if sys.argv[1] is None:
    print(
        "You didn't open this program with a file, either drag a .model onto the program to drag it as your arg in cmd")
    input("Press Enter to close...")
    sys.exit()

else:
    try:
        file = sys.argv[1]
        f = open(file, 'rb')
        f.seek(44)
        fileSize = Int32(f)
        sectionsamount = UInt32(f)
        endstringseco = 0
        endstringstatico = 0
        for i in range(sectionsamount):
            inlist = False
            sectiontype = UInt32(f)
            sectionoffset = UInt32(f)
            sectionsize = UInt32(f)
            if sectiontype == 4023987816:
                endstringseco = sectionoffset
            elif sectiontype == 675087235:
                endstringstatico = sectionoffset
        f.seek(52 + (sectionsamount * 12) + 17)
        if not endstringseco == 0:
            stringread = (endstringseco + 40) - (52 + (sectionsamount * 12) + 17)
        else:
            stringread = (endstringstatico + 40) - (52 + (sectionsamount * 12) + 17)
        strings = f.read(stringread - 4)
        strings = strings.decode('utf-8')
        DataEntrys = strings.split("\x00")
        MaterialPaths = []
        for i in DataEntrys:
            if ".material" in i:
                MaterialPaths.append(DataEntrys.index(i))

        if not MaterialPaths:
            print("Model has no material slots")
        else:
            for loop, i in enumerate(MaterialPaths):
                print("Material Slot " + str(loop) + ": " + str(DataEntrys[i]))

    except:
        print('error')
        pass

    input("Press Enter to close...")
    f.close()
    sys.exit()
