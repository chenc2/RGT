# -*- coding: UTF-8 -*-
import os
import platform
import ConfigLib
import CommonLib

#
#   用NewString替换OldString，并且重新写入到FilePath文件中。
#
def ReplaceEx(FilePath, OldString, NewString):
    CommonLib.WriteFile(FilePath, CommonLib.ReadFile(FilePath).replace(OldString, NewString))

#
#   Replace the path recursively.
#   For example:RGT.exe -v --s -o "C:\Users\chenche4\Desktop\RGT Test Case\Conf\..." MaximumConfig_IA32
#   Maybe the path 'C:\Users\chenche4\Desktop\RGT Test Case' is an invalid path in another OS.
#   So we replace it by actually path.
#
def RecursiveReplaceCmd(RootPath):
    OldStr = CommonLib.ReadFile(os.path.join(RootPath,ConfigLib.ConfigInfo.CaseRootTxt))
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
    CommonLib.WriteFile(os.path.join(RootPath,ConfigLib.ConfigInfo.CaseRootTxt), NewStr)