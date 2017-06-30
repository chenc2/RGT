# -*- coding: UTF-8 -*-
import os
import RunRGT
import shutil
import SkipList
import RGTCompareLib
import ConfigLib
import TCSLib
import CmdLib
import UpdateBim
import PDOLib
import platform

CaseRoot        = ConfigLib.ConfigInfo.TestCaseRoot
BimFilePath     = ConfigLib.ConfigInfo.BimFilePath
CmdFileName     = ConfigLib.ConfigInfo.Command
TestResultName  = ConfigLib.ConfigInfo.TestDirName
TestLogName     = ConfigLib.ConfigInfo.TestLogName
CompDirName     = ConfigLib.ConfigInfo.CompDirName
Expected        = ConfigLib.ConfigInfo.Expected
TestResult      = ConfigLib.ConfigInfo.TestDirName
ExpectedLogName = ConfigLib.ConfigInfo.ExpectedLogName
CompLogName     = ConfigLib.ConfigInfo.CompLogName
CompCSVName     = ConfigLib.ConfigInfo.CompCSVName
ProjectPath     = os.path.join(os.getcwd(), ConfigLib.ConfigInfo.ProjectName)

def DeleteDir(ThePath):
    if os.path.isdir(ThePath):
        shutil.rmtree(ThePath)

def CreateDir(ThePath):
    if os.path.isdir(ThePath):
        shutil.rmtree(ThePath)
    os.mkdir(ThePath)

def RunOneCase(CasePath):
    TestResult = os.path.join(CasePath, TestResultName)
    CmdFilePath = os.path.join(CasePath, CmdFileName)
    TestLogPath = os.path.join(TestResult, TestLogName)

    CreateDir(ProjectPath)
    CreateDir(TestResult)
    DstBimFilePath = RunRGT.CopyBimx(CmdFilePath, BimFilePath, ProjectPath)
    ConfCase = os.path.basename(CaseRoot)
    
    if CasePath.find(ConfCase+'/Conf') != -1 or CasePath.find(ConfCase+'\Conf') != -1:
        RunRGT.RunErrCase(CmdFilePath, TestLogPath)
    elif CasePath.find('HelpVersion') != -1:
        RunRGT.RunHelpCase(CmdFilePath, TestLogPath)
    else:
        RunRGT.RunCase(CmdFilePath, DstBimFilePath, ProjectPath, TestResult, TestLogName)
    DeleteDir(ProjectPath)

def RunCase():
    SList = SkipList.SkipList().GetSkipList()
    for parent,dirs,files in os.walk(CaseRoot):
        if CmdFileName in files:
            if parent not in SList:
                print parent
                RunOneCase(parent)

def Compare():
    for parent, dirs, files in os.walk(CaseRoot):
        if CmdFileName in files:
            CreateDir(os.path.join(parent, CompDirName))

            RGTCompareLib.CompareOneCase(
                os.path.join(parent, Expected),
                os.path.join(parent, TestResult),
                ExpectedLogName,
                TestLogName,
                os.path.join(parent,CompDirName,CompCSVName),
                os.path.join(parent,CompDirName,CompLogName)
            )

#
#   1. Fix error test case, like .bimx format error.
#   2. Clean up redundancy folder.
#   3. Replace the path in the test command.
#   4. Update the path of ToolSet in the bimx file.
#   5. Backup all pdo files.
#   6. Create a new pdo file for run RGT.
#   7. Recover all pdo files.
#   8. Call RunCase function to generate report.
#   9. Call Compare function to compare the result.
#
def Start():
    #TCSLib.RecursiveCheckTCS(CaseRoot, Expected, CmdFileName)
    #TCSLib.RecursiveCleanUpTCS(CaseRoot, Expected, CmdFileName)
    #CmdLib.RecursiveReplaceCmd(CaseRoot)
    #UpdateBim.UpdateBim()
    PDOLib.MovePDO(ConfigLib.ConfigInfo.PDOFilePath, os.path.join(os.getcwd(),'etc'))
    PDOLib.CreateNewRepositoryPDO(os.path.join(os.getcwd(),'etc','PlatformProjectInventory.pdo'))
    #RunCase()
    RunOneCase('C:\Users\chenche4\Desktop\RGT Test Case\Manual\Func\ConfigSettingReport\TCS1')
    PDOLib.MovePDO(os.path.join(os.getcwd(),'etc'), ConfigLib.ConfigInfo.PDOFilePath, True)
    #Compare()

if __name__ == '__main__':
    Start()