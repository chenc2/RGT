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
ExceptionDir    = ConfigLib.ConfigInfo.Exception
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
    Sheet.write(0, 3, 'Case Result')

    Row = 1
    for Case in ResultInfo:
        Sheet.write(Row, 0, Case[0])
        if 'Linux' in platform.system():
          Slash = '/'
        else:
          Slash = '\\'

        Sheet.write(Row, 1, Case[1])
        Sheet.write(Row, 2, Case[2])

        if Case[1] == Case[2] and Case[1] == u'[True]':
            Sheet.write(Row, 3, u'Pass')
        else:
            Sheet.write(Row, 3, u'Fail')

        Row = Row + 1

    if os.path.isfile(os.path.join(ResultFilePath, 'Report.xls')):
        os.remove(os.path.join(ResultFilePath, 'Report.xls'))
    xls.save(os.path.join(ResultFilePath, 'Report.xls'))

#
#   读取Exception列表，其中是用于过滤的内容。
#   开发那边code会进行修改，从而导致flashlayout或者size有变化。
#   但是这样的变化是符合的，需要把这些内容进行过滤掉。
#
def GetExceptionContent():
    Content = []
    for file in os.listdir(ExceptionDir):
        fd = open(os.path.join(ExceptionDir, file))
        Buffer = fd.read()
        fd.close()
        Content.append(Buffer)
    return Content

def Compare():
    ExceptionContentList = GetExceptionContent()
    
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
                  os.path.join(parent,CompDirName,CompLogName),
                  ExceptionContentList
                )
            Result.append(L)

    SaveResultInExcel(Result)

#
#   1. Check test cases are all valid.
#   2. Clean up unuseless in each test case.
#   3. Fix the path in the cmd.txt file.
#   4. Update .bimx file by current env settings.
#   5. Back up pdo files.
#   6. Create new pdo files for test.
#   7. RunCase(all cases) or RunOneCase(for debug).
#   8. Restore the original PDO files.
#   9. Compare the test result and generate report.
#
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