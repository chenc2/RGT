# -*- coding: utf-8 -*-
import os
import CSVLib
import shutil
import platform
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

def ConvertExpectedLogFile(LogFilePath):
    CommonLib.WriteFile(LogFilePath, CommonLib.ToUnixFormat(CommonLib.ReadFile(LogFilePath)))

#
#   Check and make sure each test case is correct.
#
def RecursiveCheckTCS(TestCaseDir, ExpectedDirName, ExpectedLogName, CmdFileName):
    for parent,dirs,files in os.walk(TestCaseDir):
        if CmdFileName in files:
            CheckTCS(parent, ExpectedDirName, CmdFileName, False)
            if 'Linux' in platform.system():
                ConvertExpectedLogFile(os.path.join(parent, ExpectedDirName, ExpectedLogName))

#
#   Clean up all files except 'Expected' and 'Command'.
#
def RecursiveCleanUpTCS(TestCaseDir, ExpectedDirName, CmdFileName):
    for parent,dirs,files in os.walk(TestCaseDir):
        if CmdFileName in files:
            CheckTCS(parent, ExpectedDirName, CmdFileName, True)