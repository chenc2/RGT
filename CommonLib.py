# -*- coding: UTF-8 -*-
import os
import shutil

#
#   Read file as List type, and return.
#
def ReadFileList(FilePath):
    if not os.path.isfile(FilePath):
        print FilePath,'is an invalid path, please check.'
        assert(False)

    List = []
    fd = open(FilePath)
    Lines = fd.readlines()
    fd.close()

    for line in Lines:
        List.append(line.strip('\n'))
    return List

#
#   Read file as string type, and return.
#
def ReadFile(FilePath):
    if not os.path.isfile(FilePath):
        print FilePath,'is an invalid path, please check.'
        assert(False)

    fd = open(FilePath)
    string = fd.read()
    fd.close()

    return string

def ToUnixFormat(string):
    return string.replace('\r','')

#
#   If the last char is '\n', delete it.
#
def StripLastChar(string):
    if len(string) != 0 and string[-1] == '\n':
        return string[:-1]
    else:
        return string

#
#   Wrap the function ToUnixFormat and StripLastChar.
#
def ConvertAndStripString(string):
    return StripLastChar(ToUnixFormat(string))

#
#   Write string to file.
#
def WriteFile(FilePath, String):
    fd = open(FilePath, 'w')
    fd.write(String)
    fd.close()

#
#   Create a folder.
#
def CreateDir(ThePath):
    if os.path.isdir(ThePath):
        shutil.rmtree(ThePath)
    os.mkdir(ThePath)

#
#   Copy folder from Src to Dst.
#
def CopyFolder(Src, Dst, DeleteSrc = False):
    if not os.path.isdir(Src):
        assert(False)

    if os.path.isdir(Dst):
        shutil.rmtree(Dst)
    elif os.path.isfile(Dst):
        assert(False)
    
    shutil.copytree(Src,Dst)

    if DeleteSrc:
        shutil.rmtree(Src)