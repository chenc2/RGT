# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
import platform
import ConfigLib
import PDOLib
import shlex

#
#   获取某个目录下所有.bim文件。
#   其中文件名作为key（不包含后缀），
#   同时对应的文件路径作为value。
#
def GetAllBim(BimPath):
    FileMap = dict()
    for file in os.listdir(BimPath):
        if '.bimx' in file:
            FileMap[file[:-5]] = os.path.join(BimPath,file)
    return FileMap

def GetCmdList(FilePath):
    return shlex.split(GetCmdString(FilePath))

def GetCmdString(FilePath):
    fd = open(FilePath, 'r')
    String = fd.read().replace('RGT.exe', 'RGT')
    fd.close()

    return String

def WriteFile(FilePath,String):
    fd = open(FilePath, 'w')
    if 'Linux' in platform.system() and len(String) != 0:
        fd.write(String + '\n')
    else:
        fd.write(String)
    fd.close()

#
#   Copy bim file is depends on test command.
#
def CopyBimx(CmdFilePath, SrcBimPath, WorkSpace):
    Commands = GetCmdString(CmdFilePath)
    FileMaps = GetAllBim(SrcBimPath)
    for BimFileName in FileMaps.keys():
        if Commands.find(BimFileName) != -1:
            shutil.copy(FileMaps.get(BimFileName), WorkSpace)
            return os.path.join(WorkSpace, BimFileName + '.bimx')
    return ""

def RunCase(CmdFilePath, BimxFilePath, WorkSpace, TestResult, LogFileName):
    CmdString = GetCmdString(CmdFilePath)

    if (
        CmdString.find('-f') != -1 or CmdString.find('--Firmware') != -1 or \
        CmdString.find('-l') != -1 or CmdString.find('--FlashLayout') != -1
       ):
        if DoAssemble(BimxFilePath) != 0:
            print 'Error:',BimxFilePath
            assert(False)

    if CmdString.find('--debug') != -1 or CmdString.find('-d') != -1:
        RunDebugCase(GetCmdList(CmdFilePath), os.path.join(TestResult,LogFileName))
    else:
        RunNormalCase(CmdString, os.path.join(TestResult, LogFileName))

    OUTPUT = os.path.join(WorkSpace, 'OUTPUT')
    if os.path.isdir(OUTPUT):
        for file in os.listdir(OUTPUT):
            if '.csv' in file:
                shutil.copy(os.path.join(OUTPUT,file), TestResult)

def RunErrCase(CmdFilePath, SavePath):
    RGTRet = subprocess.Popen(GetCmdString(CmdFilePath), stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)
    WriteFile(SavePath, RGTRet.communicate()[1].strip('\n'))

def RunHelpCase(CmdFilePath, SavePath):
    RGTRet = subprocess.Popen(GetCmdList(CmdFilePath), stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    WriteFile(SavePath, RGTRet.stdout.read().strip('\n'))

def RunDebugCase(CmdList, SavePath):
    RGTRet = subprocess.Popen(CmdList, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    WriteFile(SavePath, RGTRet.communicate()[0].strip('\n'))

def RunNormalCase(CmdString, SavePath):
    RGTRet = subprocess.Popen(CmdString, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
    WriteFile(SavePath, RGTRet.stdout.read().strip('\n'))

def DoAssemble(BimFilePath):
    AsmRet = subprocess.Popen(['Assemble', BimFilePath], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    AsmRet.communicate()
    return AsmRet.returncode