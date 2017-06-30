# -*- coding: UTF-8 -*-
import os
import platform
import ConfigLib

def ReplaceEx(FilePath, OldString, NewString):
    fd = open(FilePath, 'r')
    Strings = fd.read().replace(OldString, NewString)
    fd.close()

    fd = open(FilePath, 'w')
    fd.write(Strings)
    fd.close()

#
#   Replace the path recursively.
#   For example:RGT.exe -v --s -o "C:\Users\chenche4\Desktop\RGT Test Case\Conf\..." MaximumConfig_IA32
#   Maybe the path 'C:\Users\chenche4\Desktop\RGT Test Case' is an invalid path in another OS.
#   So we replace it by actually path.
#
def RecursiveReplaceCmd(RootPath):
    fd = open(os.path.join(RootPath,ConfigLib.ConfigInfo.CaseRootTxt))
    OldStr = fd.read()
    fd.close()

    NewStr = RootPath

    if OldStr == NewStr:
        return

    for parent,dirs,files in os.walk(RootPath):
        for file in files:
            if file == ConfigLib.ConfigInfo.Command:
                ReplaceEx(os.path.join(parent, file), OldStr, NewStr)
                if 'Linux' in platform.system():
                    ReplaceEx(os.path.join(parent, file), '\\', '/')

    #
    #   Update the path.
    #
    fd = open(os.path.join(RootPath,ConfigLib.ConfigInfo.CaseRootTxt), 'w')
    fd.write(NewStr)
    fd.close()