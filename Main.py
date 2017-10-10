# -*- coding: UTF-8 -*-
import os
import RGTCompareLib
import TCSLib
import CmdLib
import UpdateBim
import PDOLib
import platform
import xlwt
import DoRun
import ExpectionList
import CommonLib
from ConfigLib import ConfigInfo

ExpectedDirName = ConfigInfo.ExpectedDirName
ExpectedLogName = ConfigInfo.ExpectedLogName

TestDirName = ConfigInfo.TestDirName
TestLogName = ConfigInfo.TestLogName

CompDirName = ConfigInfo.CompDirName
CompLogName = ConfigInfo.CompLogName
CompCSVName = ConfigInfo.CompCSVName

CmdFileName = ConfigInfo.CmdFileName

ProjectName = ConfigInfo.ProjectName
ProjectPath = os.path.join(os.getcwd(), ProjectName)
CaseRootTxt = ConfigInfo.CaseRootTxt

PDOFileDir = ConfigInfo.PDOFileDir

TestCaseDir = ConfigInfo.TestCaseDir

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

    if os.path.isfile(os.path.join(ConfigInfo.ResultDir, 'Report.xls')):
        os.remove(os.path.join(ConfigInfo.ResultDir, 'Report.xls'))
    xls.save(os.path.join(ConfigInfo.ResultDir, 'Report.xls'))

def Compare():
    ExceptionContentList = ExpectionList.ReadExpectionContent(ConfigInfo.ExceptionDir)
    
    Result = []
    for parent, dirs, files in os.walk(ConfigInfo.TestCaseDir):
        if CmdFileName in files:
            CommonLib.CreateDir(os.path.join(parent, CompDirName))

            L = RGTCompareLib.CompareOneCase(
                  os.path.join(parent, ExpectedDirName),
                  os.path.join(parent, TestDirName),
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
if __name__ == '__main__':
    #TCSLib.RecursiveCheckTCS(TestCaseDir, ExpectedDirName, CmdFileName)
    #TCSLib.RecursiveCleanUpTCS(TestCaseDir, ExpectedDirName, CmdFileName)
    #CmdLib.RecursiveReplaceCmd(TestCaseDir)
    #UpdateBim.UpdateBim()
    #PDOLib.MovePDO(ConfigInfo.PDOFileDir, os.path.join(os.getcwd(),'etc'))
    #PDOLib.CreateNewRepositoryPDO(os.path.join(os.getcwd(),'etc','PlatformProjectInventory.pdo'))
    #DoRun.RunAllTestCase()
    #DoRun.RunCaseDebug(False)
    #PDOLib.MovePDO(os.path.join(os.getcwd(),'etc'), ConfigInfo.PDOFileDir, True)
    Compare()