# -*- coding: UTF-8 -*-
import os
import RunRGT
import shutil
import RGTCompareLib
import ConfigLib
import TCSLib
import CmdLib
import UpdateBim
import PDOLib
import platform
import xlwt

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
ResultFilePath  = ConfigLib.ConfigInfo.ResultPath
ProjectPath     = os.path.join(os.getcwd(), ConfigLib.ConfigInfo.ProjectName)

def GetPathList():
    TheList = []
    if os.path.isfile('List.txt'):
        fd = open('List.txt')
        Lines = fd.readlines()
        fd.close()
        
        for line in Lines:
            TheList.append(line.strip('\n'))
    return TheList

def DeleteDir(ThePath):
    if os.path.isdir(ThePath):
        shutil.rmtree(ThePath)

def CreateDir(ThePath):
    if os.path.isdir(ThePath):
        shutil.rmtree(ThePath)
    os.mkdir(ThePath)

#
#   Run the test case of CasePath.
#
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

#
#   Walk all test case and run.
#
def RunCase():
    for parent,dirs,files in os.walk(CaseRoot):
        if CmdFileName in files:
            print parent
            RunOneCase(parent)

#
#   Function to run test case in debug mode.
#   If Skip = True,  The path of List.txt file will be skipped.
#   If Skip = False, The path of List.txt file will be executed.
#   List.txt for debug, When debugging, you can skip some paths
#   or execute special paths.
#
def RunCaseDebug(Skip = True):
    SList = GetPathList()
    for parent,dirs,files in os.walk(CaseRoot):
        if CmdFileName in files:
            if Skip and parent not in SList:
                print parent
                RunOneCase(parent)
            elif not Skip and parent in SList:
                print parent
                RunOneCase(parent)

#
#   Each ResultInfo is the list type.
#   ResultInfo[x][0] is the path of test case
#   ResultInfo[x][1] is the result of compare csv
#   ResultInfo[x][2] is the result of compare log
#
def SaveResultInExcel(ResultInfo):
    xls = xlwt.Workbook()
    Sheet = xls.add_sheet('RGT Command Line')

    Sheet.write(0, 0, 'Test Case Path')
    Sheet.write(0, 1, 'Compare CSV')
    Sheet.write(0, 2, 'Compare Log')

    Row = 1
    for Case in ResultInfo:
        Sheet.write(Row, 0, Case[0])
        if Case[0][len(CaseRoot):].split('\\')[1] == 'Conf' and Case[1] == '[Skip]':
            Sheet.write(Row, 1, '[True]')
        else:
            Sheet.write(Row, 1, Case[1])
        Sheet.write(Row, 2, Case[2])
        Row = Row + 1
    if os.path.isfile(os.path.join(ResultFilePath, 'Report.xls')):
        os.remove(os.path.join(ResultFilePath, 'Report.xls'))
    xls.save(os.path.join(ResultFilePath, 'Report.xls'))

def Compare():
    Result = []
    for parent, dirs, files in os.walk(CaseRoot):
        if CmdFileName in files:
            CreateDir(os.path.join(parent, CompDirName))

            L = RGTCompareLib.CompareOneCase(
                  os.path.join(parent, Expected),
                  os.path.join(parent, TestResult),
                  ExpectedLogName,
                  TestLogName,
                  os.path.join(parent,CompDirName,CompCSVName),
                  os.path.join(parent,CompDirName,CompLogName)
                )
            Result.append(L)

    SaveResultInExcel(Result)

#
#   1. Fix error test case, like .bimx format error.
#   2. Clean up redundancy folder.
#   3. Replace the path in the test command.
#   4. Update the path of ToolSet in the bimx file.
#   5. Backup all pdo files.
#   6. Create a new pdo file for run RGT.
#   7. Run all test case.
#   8. Recover all pdo files.
#   9. Compare the result.
def Start():
    #TCSLib.RecursiveCheckTCS(CaseRoot, Expected, CmdFileName)
    #TCSLib.RecursiveCleanUpTCS(CaseRoot, Expected, CmdFileName)
    #CmdLib.RecursiveReplaceCmd(CaseRoot)
    #UpdateBim.UpdateBim()
    #PDOLib.MovePDO(ConfigLib.ConfigInfo.PDOFilePath, os.path.join(os.getcwd(),'etc'))
    #PDOLib.CreateNewRepositoryPDO(os.path.join(os.getcwd(),'etc','PlatformProjectInventory.pdo'))
    #RunCase()
    #RunOneCase('C:\Users\chenche4\Desktop\RGT Test Case\Func\Basic\MaximumConfig_IA32\TCS10')
    #PDOLib.MovePDO(os.path.join(os.getcwd(),'etc'), ConfigLib.ConfigInfo.PDOFilePath, True)
    Compare()

if __name__ == '__main__':
    Start()