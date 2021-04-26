#Date 1/11/2021
#Class CS 4541
#Assignment: Assignment 2
#Author: Marcus Durette

import sys, os, traceback

args = [False,False,False,False,False,False]
numofsets = 1
numoflines = 1
numofblockbits = 1
trace = ""
fileloc = ""
filesets = 0
filebbits = 0

datacache = {}
index = {}

hits = 0
misses = 0
evictions = 0

operationcount = 0

class line:
    def __init__(self, isvalid, tag, birth):
        self.isvalid = isvalid
        self.tag = tag
        self.birth = birth

#Cache Initializer

def cacheinits():
    global dcachefill,datacache
    columns = {}
    bits = {}
    dcachefill = (2**numofsets)*numoflines
    for i in range(2**numofsets):
        row = {}
        for j in range(numoflines):
            row[j] = -1
        columns[i] = row
    datacache = columns


def Add(op):
    global datacache,operationcount
    cset = datacache[op["Address"]]
    youngest = sys.maxsize
    for i in range(numoflines):
        if(cset[i] == -1):
            datacache[op["Address"]][i] = line(1,op["Tag"],operationcount)
            operationcount += 1
            return 0
        else:
            try:
                if(cset[i].birth < youngest):
                    youngest = i
            except:
                pass
    datacache[op["Address"]][youngest] = line(1,op["Tag"],operationcount)
    return -1

def Search(op):
    global datacache
    cset = datacache[op["Address"]]
    for i in range(numoflines):
        try:
            if(cset[i].tag == op["Tag"]):
                return True
        except:
            pass
    return False

def Remove(op):
    pass

#Control functions for finding or putting values into the cache

def dataload(op):
    if(Search(op) == True):
        hit()
    else:
        miss()
        if(Add(op) == -1):
            eviction()
    
def instructionload():
    pass
    
def datastore(op):
    if(Search(op) == True):
        hit()
    else:
        miss()
        if(Add(op) == -1):
            eviction()
    
def datamodify(op):
    dataload(op)
    datastore(op)

#Hit,Miss and Eviction value functions

def hit():
    if(args[1] == True):
        print(" Hit ", end="")
    global hits
    hits += 1
    
def miss():
    if(args[1] == True):
        print(" Miss ", end="")
    global misses
    misses += 1

def eviction():
    if(args[1] == True):
        print(" Eviction ", end="")
    global evictions
    evictions += 1

#Decode Address and Size
def AddressDecode(address,size):
    try:
        address = bin(int(address,16))
        address = address[2:]
        vallist = {}
        vallist["Offset"] = int('0b' + address[len(address)-numofblockbits:],2)
        address = address[:len(address)-numofblockbits]
        try:
            vallist["Address"] = int('0b' + address[len(address)-numofsets:],2)
        except:
            vallist["Address"] = 0
        address = address[:len(address)-numofsets]
        vallist["Tag"] = address
        print(vallist)
        return vallist
    except:
        pass

#Controller of base operations

def operations(string):
    sizeind = False
    operation = "N"
    address = ""
    index = 0
    data = string.split(",")
    try:
        op = AddressDecode(str(data[1]),str(data[2]))
        if(args[1] == True and data[0] != ""):
            print(string, end="")
        if(data[0] == "L"):
            dataload(op)
        elif(data[0] == ""):
            instructionload()
        elif(data[0] == "S"):
            datastore(op)
        elif(data[0] == "M"):
            datamodify(op)
        if(args[1] == True and data[0] != ""):
            print()
            #print(datacache[op["Address"]])
            #print()
    except:
        pass

#Main control over all functions

def cachesim(trace):
    cacheinits()
    trasize = 0
    try:
        file = open(trace,"r")
        lines = file.readlines()
        for line in lines:
            newstring = line.replace(" ",",")
            newstring = newstring.strip("\n\t")
            newstring = newstring[1:]
            operations(newstring)
            trasize = trasize + 1
        print()
        print("Hits:" + str(hits) + " Misses:" + str(misses) + " Evictions:" + str(evictions))
    except:
        traceback.print_exc()
        print("python <thisfile> <-v,-h> -s <Number of Sets> -E <Number of Lines> -b <Number of Bits per Block> -t <local trace path> ")

#Argument reading

def main(argv):
    
    global numofsets
    global numoflines
    global numofblockbits
    global fileloc,filesets,filebbits
    dir_path = os.path.dirname(__file__)
    inputfile = ''
    sflag = False
    Eflag = False
    bflag = False
    tflag = False
    for i in argv:
        if( i == "-h"):
            args[0] = True
            print()
            print("Commands:")
            print("-h: Optional help flag that prints usage info")
            print("-v: Optional verbose flag that displays trace info")
            print("-s <s>: Number of set index bits (S = 2 s is the number of sets)")
            print("-E <E>: Associativity (number of lines per set)")
            print("-b <b>: Number of block bits (B = 2 b is the block size)")
            print("-t <tracefile>: Name of the valgrind trace to replay")
            print()
        elif(i == "-v"):
            args[1] = True
        elif(i == "-s"):
            args[2] = True
            sflag = True
        elif(i == "-E"):
            args[3] = True
            Eflag = True
        elif(i == "-b"):
            args[4] = True
            bflag = True
        elif(i == "-t"):
            args[5] = True
            tflag = True
        else:
            if(sflag == True):
                sflag = False
                numofsets = int(i)
            elif(Eflag == True):
                Eflag = False
                numoflines = int(i)
                filesets = int(i)
            elif(bflag == True):
                bflag = False
                numofblockbits = int(i)
                filebbits = int(i)
            elif(tflag == True):
                tflag = False
                fileloc = str(i)
                trace = dir_path + "\\" +str(i) 
    if(trace != ""):
        if(len(argv) >= 8):
            cachesim(trace)
        if(args[2] == False):
            print("Error, -s not found")
        elif(args[3] == False):
            print("Error, -E not found")
        elif(args[4] == False):
            print("Error, -b not found")
        elif(args[5] == False):
            print("Error, -t not found")
    else:
        print("error empty trace path")

if __name__ == "__main__":
    print()
    main(sys.argv[1:])