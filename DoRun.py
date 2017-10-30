# -*- coding: UTF-8 -*-
import RunRGT
import os
import shutil
import CommonLib
import time
from ConfigLib import ConfigInfo

#
#   Walk all test case and run.
#
def RunAllTestCase():
    for parent,dirs,files in os.walk(ConfigInfo['TestCaseDir']):
        if ConfigInfo['CmdFileName'] in files:
            print parent
            RunOneCase(parent)

def DeleteDir(ThePath):
    time.sleep(3)
    if os.path.isdir(ThePath):
        while 1:
            try:
                shutil.rmtree(ThePath)
                break
            except:
                pass

#
#   Run the test case of CasePath.
#
def RunOneCase(CasePath):
    CmdFilePath = os.path.join(CasePath, ConfigInfo['CmdFileName'])
    TestDirPath = os.path.join(CasePath, ConfigInfo['TestDirName'])
    TestLogPath = os.path.join(CasePath, ConfigInfo['TestDirName'], ConfigInfo['TestLogName'])
    ProjectPath = os.path.join(os.getcwd(), ConfigInfo['ProjectName'])

    CommonLib.CreateDir(ProjectPath)
    CommonLib.CreateDir(TestDirPath)
    DstBimFilePath = RunRGT.CopyBimx(CmdFilePath, ConfigInfo['BimxFileDir'], ProjectPath)
    ConfCase = os.path.basename(ConfigInfo['TestCaseDir'])
    
    if CasePath.find(ConfCase+'/Conf') != -1 or CasePath.find(ConfCase+'\Conf') != -1:
        RunRGT.RunErrCase(CmdFilePath, TestLogPath)
    elif CasePath.find('HelpVersion') != -1:
        RunRGT.RunHelpCase(CmdFilePath, TestLogPath)
    else:
        RunRGT.RunCase(CmdFilePath, DstBimFilePath, ProjectPath, TestDirPath, TestLogPath)
    DeleteDir(ProjectPath)

#
#   Function to run test case in debug mode.
#   If Skip = True,  The path of List.txt file will be skipped.
#   If Skip = False, The path of List.txt file will be executed.
#   List.txt for debug, When debugging, you can skip some paths
#   or execute special paths.
#
def RunCaseDebug(Skip = True):
    SList = CommonLib.ReadFileList('List.txt')

    for parent,dirs,files in os.walk(ConfigInfo['TestCaseDir']):
        if ConfigInfo['CmdFileName'] in files:
            if Skip and parent not in SList:
                print parent
                RunOneCase(parent)
            elif not Skip and parent in SList:
                print parent
                RunOneCase(parent)