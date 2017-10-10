# -*- coding: utf-8 -*-
import os
import CSVLib
import shutil
import platform
import ConfigLib
import CommonLib

def CheckExpectedCSV(ExpectedPath):
    FileMap = CSVLib.GetCSVFiles(ExpectedPath)
    if FileMap != None:
        for key in FileMap.keys():
            if not CSVLib.CheckCSV(FileMap.get(key)):
                print "CSV Error:",FileMap.get(key)
                assert(False)

def CheckTCS(ThePath, Expected, Command, CleanUp):
    Flag1 = False
    Flag2 = False

    for file in os.listdir(ThePath):
        FilePath = os.path.join(ThePath,file)
        if file == Expected:
            CheckExpectedCSV(FilePath)
            Flag1 = True

        elif file == Command:
            fd = open(FilePath)
            fd.close()
            Flag2 = True

        elif CleanUp:
            if os.path.isfile(FilePath):
                os.remove(FilePath)
            else:
                shutil.rmtree(FilePath)

    if not Flag1:
        print 'TCS:', ThePath, 'Not include', Expected
        assert(False)

    if not Flag2:
        print 'TCS:',ThePath, 'Not include', Command
        assert(False)

def RecursiveCheckTCS(RootPath, Expected, Command, CleanUp = False):
    for parent,dirs,files in os.walk(RootPath):
        for file in files:
            if Command in file:
                CheckTCS(parent, Expected, Command, CleanUp)
                if 'Linux' in platform.system():
                    String = CommonLib.ReadFile(os.path.join(parent, Expected, ConfigLib.ConfigInfo.ExpectedLogName))
                    String = CommonLib.ToUnixFormat(String)
                    CommonLib.WriteFile(os.path.join(parent, Expected, ConfigLib.ConfigInfo.ExpectedLogName), String)

#
#   Clean up all files except 'Expected' and 'Command'.
#
def RecursiveCleanUpTCS(RootPath, Expected, Command):
    RecursiveCheckTCS(RootPath, Expected, Command, True)