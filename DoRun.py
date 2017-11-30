# -*- coding: UTF-8 -*-
import RunRGT
import os
import CommonLib
import ConfigLib
import shutil

#
#   Copy bimx and (assemble data) to the workspace.
#
def CopyBimxToWorkSpace(CmdFilePath, BimxMapFolder, WorkSpace):
    Commands = CommonLib.ReadFile(CmdFilePath)
    for BimxFileName in BimxMapFolder.keys():
        if Commands.find(BimxFileName) != -1:
            CommonLib.DeleteFolder(WorkSpace)
            shutil.copytree(BimxMapFolder.get(BimxFileName), WorkSpace)
            break

#
#   Walk all test case and run.
#
def RunAllTestCase(BimMapFolder):
    ConfigInfo = ConfigLib.GetConfigInfo()

    for parent,dirs,files in os.walk(ConfigInfo['TestCaseDir']):
        if ConfigInfo['CmdFileName'] in files:
            print parent
            RunOneCase(parent, BimMapFolder)

#
#   Run the test case of CasePath.
#
def RunOneCase(CasePath, BimMapFolder):
    ConfigInfo = ConfigLib.GetConfigInfo()

    CmdFilePath = os.path.join(CasePath, ConfigInfo['CmdFileName'])
    TestDirPath = os.path.join(CasePath, ConfigInfo['TestDirName'])
    TestLogPath = os.path.join(CasePath, ConfigInfo['TestDirName'], ConfigInfo['TestLogName'])
    WorkSpace   = os.path.join(os.getcwd(), ConfigInfo['ProjectName'])

    CommonLib.CreateDir(TestDirPath)
    CopyBimxToWorkSpace(CmdFilePath, BimMapFolder, WorkSpace)
    ConfCase = os.path.basename(ConfigInfo['TestCaseDir'])
    
    #
    #   For "Conf/FirmwareReport/TCS185" test case, pre-build data will inflect test result.
    #   So delete the pre-buid data and just remain the .bimx file and do the test.
    #
    if CasePath[len(ConfigInfo['TestCaseDir']) + 1:] == 'Conf/FirmwareReport/TCS185' or \
       CasePath[len(ConfigInfo['TestCaseDir']) + 1:] == 'Conf\FirmwareReport\TCS185':
        for file in os.listdir(WorkSpace):
            if file[-5:] == '.bimx':
                continue
            else:
                CommonLib.DeleteFolder(os.path.join(WorkSpace, file))

    if CasePath.find(ConfCase+'/Conf') != -1 or CasePath.find(ConfCase+'\Conf') != -1:
        RunRGT.RunErrCase(CmdFilePath, TestLogPath)
    elif CasePath.find('HelpVersion') != -1:
        RunRGT.RunHelpCase(CmdFilePath, TestLogPath)
    else:
        RunRGT.RunCase(CmdFilePath, WorkSpace, TestDirPath, TestLogPath)
    
    CommonLib.DeleteFolder(WorkSpace)

#
#   Just run the test case in the List.txt file.
#
def RunListCase():
    PathList = CommonLib.ReadFileList('List.txt')
    ConfigInfo = ConfigLib.GetConfigInfo()

    for parent, dirs, files in os.walk(ConfigInfo['TestCaseDir']):
        if ConfigInfo['CmdFileName'] in files and parent in PathList:
            RunOneCase(parent)