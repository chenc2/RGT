# -*- coding: UTF-8 -*-
import os

#
#   Get all .csv file in the path.
#   Return data by key-value format.
#   The type of .csv file as KEY.
#   The path of .csv file as VALUE.
#
def GetCSVFiles(path):
    Map = dict()
    for file in os.listdir(path):
        if '.csv' in file:
            Map[GetCSVType(os.path.join(path,file))] = os.path.join(path,file)
    return Map

#
#   Check the header of .csv file.
#   The .csv file header format as follow:
#
#   Intel(R) Firmware Engine Version, 3.0.0.120084
#   Project Name,test
#   Firmware Version, 3.0.0
#   Report Type,Configuration Settings
#   Report Date,05/11/2017
#   Report Time,04:52:02 PM
#
def CheckCSVHeader(FilePath):
    Data = []
    fd = open(FilePath, 'rb')
    fd.read(2)
    for index in range(0,6):
        Data.append(fd.readline().replace('\0','').replace('\n',''))
    fd.close()

    if  Data[0].find('Intel(R) Firmware Engine Version') == -1 or \
        Data[1].find('Project Name') == -1 or \
        Data[2].find('Firmware Version') == -1 or \
        Data[3].find('Report Type') == -1 or \
        Data[4].find('Report Date') == -1 or \
        Data[5].find('Report Time') == -1:
        return False

    return True

#
#   Check .csv file contains two parts.
#   The first part is to check the header of .csv file.
#   The second part is to check whether this file can
#   be parse by ParseXXX function.
#
def CheckCSV(FilePath):
    if not CheckCSVHeader(FilePath):
        return False

    ParseFuncMap = {
        'GPIO Table'                : ParseGPIOTableCSV,
        'Flash Offset Layout'       : ParseFlashLayoutCSV,
        'Firmware Inventory'        : ParseFirmwareInventoryCSV,
        'Platform Inventory'        : ParsePlatformInventoryCSV,
        'Configuration Settings'    : ParseConfSettingCSV,
    }

    #
    #   If the file could be parse, then it's a valid .csv file.
    #
    ParseFuncMap.get(GetCSVType(FilePath))(FilePath)
    return True

#
#   Check header and get the type.
#
def GetCSVType(FilePath):
    if not CheckCSVHeader(FilePath):
        return None

    Ret = None
    fd = open(FilePath, 'rb')
    fd.read(2)

    for index in range(0,3):
        fd.readline()

    Buffer = fd.readline().replace('\0','').replace('\n','')
    if Buffer.find('Report Type') == 0:
        Ret = Buffer[Buffer.find(',')+1:].strip()
    fd.close()

    return Ret

def GetVersion(FilePath):
    Ret = None
    fd = open(FilePath, 'rb')
    fd.read(2)

    Buffer = fd.readline().replace('\0','').replace('\n','')
    if Buffer.find('Intel(R) Firmware Engine Version') == 0:
        Ret = Buffer[Buffer.find(',')+1:].strip()
    fd.close()
    return Ret

def GetFirmwareVersion(FilePath):
    Ret = None
    fd = open(FilePath, 'rb')
    fd.read(2)

    for index in range(0,2):
        fd.readline()

    Buffer = fd.readline().replace('\0','').replace('\n','')
    if Buffer.find('Firmware Version') == 0:
        Ret = Buffer[Buffer.find(',')+1:].strip()
    fd.close()
    return Ret

def ReadCSVFile(file):
    Data = []
    fd = open(file, 'rb')

    fd.read(2)
    line = fd.readline().replace('\0', '').replace('\r', '')
    while 1:
        if not line:
            break

        #
        #   "" -> "
        #
        while line.replace('\"\"', '\"') != line:
            line = line.replace('\"\"', '\"')

        #
        #   [, ] -> [,]
        #
        while line != line.replace(', ', ','):
            line = line.replace(', ', ',')

        while line != line.strip('\"'):
            line = line.strip('\"')

        #
        #   delete both '\n' char.
        #
        if len(line.strip('\n')) != 0:
            Data.append(line.strip('\n'))
        line = fd.readline().replace('\0', '').replace('\r', '')

    fd.close()
    return Data

def ParseCSV(Data, KeyCol):
    assert (len(KeyCol) != 0)
    KeyName = dict()

    for line in Data:
        if len(line) == 0:
            continue

        Name = line.split(',')[KeyCol[0]]
        for elem in KeyCol[1:]:
            Name = Name + '|' + line.split(',')[elem].strip()

        if Name in KeyName.keys():
            KeyName[Name] = KeyName.get(Name) + 1
        else:
            KeyName[Name] = 1

    UniqueKeyData = dict()
    MultipleKeyData = dict()

    for line in Data:
        if len(line) == 0:
            continue

        Name = line.split(',')[KeyCol[0]]
        for elem in KeyCol[1:]:
            Name = Name + '|' + line.split(',')[elem].strip()

        if KeyName.get(Name) == 1:
            UniqueKeyData[Name] = line
        else:
            if Name in MultipleKeyData.keys():
                MultipleKeyData[Name].append(line)
            else:
                MultipleKeyData[Name] = [line]

    #
    #   UniqueKeyData format as follow:
    #   Key1, Value1
    #   Key2, Value2
    #   ...
    #   KayN, ValueN
    #
    #   MultipleKeyData format as follow:
    #   Key1, Value11, Value12, Value13 ...
    #   Key2, Value21, Value22, Value23 ...
    #   ...
    #   KeyN, ValueN1, ValueN2, ValueN3 ...
    #
    return [UniqueKeyData, MultipleKeyData]

#
#   Format: B1, BOM, 'Item Name', 'Item Type', 'Item Description'
#
#   Use the 'Item Name' as the key name, save as Data['Item Name'] = ...
#
def ParsePlatformInventoryCSV(file):
    ListData = ReadCSVFile(file)[6:]
    #
    #   Check B1 and BOM tag.
    #
    for item in ListData:
        if 'B1' != list(item.split(','))[0] or 'BOM' != list(item.split(','))[1]:
            print file, 'is an invalid PlatformInventory file!'
            assert (False)

    return ParseCSV(ListData, [2])

'''
    Line Code Notation about Flash Offset Report:
    M1	Firmware Inventory: Module Line Item
    S1	Firmware Inventory: Summary Line Item

    Format: M1, Firmware, Module Name, Module Size, Module Description.
            S1, Summary, ...

    M1: Use third field as key name.
    S1: Use third field as key name.
'''
def ParseFirmwareInventoryCSV(file):
    ListData = ReadCSVFile(file)[6:]
    #
    #   Check M1,Firmware tag.
    #
    for item in ListData[:-1]:
        TheLineList = list(item.split(','))
        if 'M1' != TheLineList[0] or 'Firmware' != TheLineList[1]:
            print file, 'is an invalid FirmwareInventory file!'
            assert (False)
    #
    #   Check S1,Summary tag.
    #
    TheLineList = ListData[-1:][0].split(',')
    if 'S1' != TheLineList[0] or 'Summary' != TheLineList[1]:
        print file, 'is an invalid FirmwareInventory file!'
        assert (False)

    return ParseCSV(ListData, [2])

#
#   Line Code Notation about Flash Offset Report:
#   P1	Configuration : PCD Line item
#   Q1	Configuration : Question Line item
#
#   Parse Q1 and P1.
#
#   P1, PCD,<PCD name>,<Module name>,...
#   Use Module and PCD as key-name.
#
def ParseConfSettingCSV(file):
    BufList = ReadCSVFile(file)[6:]
    TheList = []

    for line in BufList:
        TheLineList = list(line.split(','))
        #
        #   Bug: 如果P1,PCD写成PCD，那么解析时就会发生错误。
        #
        if TheLineList[0] == 'P1' or TheLineList[0] == 'Q1':
            TheList.append(line)

    return ParseCSV(TheList, [3, 2])

#
#   Line Code Notation about Flash Offset Report:
#   R1	Flash Offset Report: Flash Region Line
#   H1	Flash Offset Report: Flash Header Line (Base/Size)
#   H2	Flash Offset Report: VPD Header
#   V1	Flash Offset Report: VPD Area Line
#   U0	Flash Offset Report: Microcode Header
#   U1	Flash Offset Report: Microcode items
#
#   R1: Use the second field as the key name.
#   H1: Use the second field as the key name.
#   H2: Skip
#   V1: Use the second field as the key name.
#   U0: Skip
#   U1: Use the third field as the key name.
#
#   Just parse R1, H1, V1, U1
#
#   Valid repeat item:
#   R1, Vital Product Data (VPD) Area, 0x0078f900, 0x0078ffff, 0x00000700
#
def ParseFlashLayoutCSV(file):
    BufList = ReadCSVFile(file)[6:]
    ValidTag = ['R1', 'H1', 'H2', 'V1', 'U0', 'U1']
    TheList = []

    for item in BufList:
        TheLineList = list(item.split(','))
        if TheLineList[0] in ValidTag:
            if TheLineList[0] != 'H2' and TheLineList[0] != 'U0':
                TheList.append(item)
        else:
            print file, 'is an invalid FlashLayout file!'
            assert (False)

    return ParseCSV(TheList, [1])

#
#  G1, Source Pin, ...
#  G1, GPIONCx, ...
#  G1, GPIOSCx, ...
#
#  Use GPIONCx or GPIOCx as key-name.
#
def ParseGPIOTableCSV(file):
    TheList = ReadCSVFile(file)[6:]
    #
    #   Check G1 tag.
    #
    for item in TheList:
        TheLineList = list(item.split(','))
        if TheLineList[0] != 'G1':
            print file, 'is an invalid GPIO file!'
            assert (False)

    return ParseCSV(TheList, [1])