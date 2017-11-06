# -*- coding: utf-8 -*-
import subprocess
import shutil
import os
import platform
import shlex
import CommonLib

#
#   Split by shlex.
#
def GetCmdList(FilePath):
    return shlex.split(GetCmdString(FilePath))

#
#   For compatibility.
#
def GetCmdString(FilePath):
    return CommonLib.ReadFile(FilePath).replace('RGT.exe', 'RGT')

def WriteFile(FilePath,String):
    if 'Linux' in platform.system() and len(String) != 0:
        String = String + '\n'
    CommonLib.WriteFile(FilePath, String)

def RunCase(CmdFilePath, WorkSpace, TestResult, LogFileName):
    CmdString = GetCmdString(CmdFilePath)

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
    Cmd = GetCmdList(CmdFilePath)
    RGTRet = subprocess.Popen(Cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    WriteFile(SavePath, RGTRet.stdout.read().strip('\n'))

def RunDebugCase(CmdList, SavePath):
    RGTRet = subprocess.Popen(CmdList, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
    WriteFile(SavePath, RGTRet.communicate()[0].strip('\n'))

def RunNormalCase(CmdString, SavePath):
    RGTRet = subprocess.Popen(CmdString, stdout = subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
    WriteFile(SavePath, RGTRet.stdout.read().strip('\n'))