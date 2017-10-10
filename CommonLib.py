# -*- coding: UTF-8 -*-
import os
import shutil

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
#
#
def StripLastChar(string):
    if len(string) != 0 and string[-1] == '\n':
        return string[:-1]
    else:
        return string

#
#
#
def WriteFile(FilePath, String):
    fd = open(FilePath, 'w')
    fd.write(String)
    fd.close()

#
#
#
def CreateDir(ThePath):
    if os.path.isdir(ThePath):
        shutil.rmtree(ThePath)
    os.mkdir(ThePath)