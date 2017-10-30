# -*- coding: UTF-8 -*-
import CommonLib

#
#   Modify the value by key in the PDO file.
#
def ModifyPDOFile(FilePath, Key, Value):
    ContentList = CommonLib.ReadFileList(FilePath)
    StringToWrite = ""
    for Line in ContentList:
        Buffer = Line.split('=')
        if len(Buffer) == 2 and Buffer[0][:-1] == Key:
            StringToWrite = StringToWrite + Buffer[0] + '= ' + Value + '\n'
        else:
            StringToWrite = StringToWrite + Line + '\n'
    CommonLib.WriteFile(FilePath, StringToWrite)

#
#   Get the value of PDO file by one key-name.
#
def GetValueFromPDO(FilePath, KeyName):
    for line in CommonLib.ReadFileList(FilePath):
        if line.find(KeyName) == 0:
                return line.split('=')[1][1:].strip('\n')

    assert(False)