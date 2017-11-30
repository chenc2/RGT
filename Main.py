# -*- coding: UTF-8 -*-
import os
import TCSLib
import CmdLib
import UpdateBim
import PDOLib
import DoRun
import ConfigLib
import InstallerLib
import platform
import CommonLib
import CompareLib
import ExlLib
import UpdateRepository
import sys
import PreBuildLib
import AutoReportLib

if __name__ == '__main__':
    InstallerLib.InitializeInstallerLib()
    ConfigLib.InitializeConfigXml()

    TestCaseDir = ConfigLib.ConfigInfo['TestCaseDir']
    ExpectedDirName = ConfigLib.ConfigInfo['ExpectedDirName']
    CmdFileName = ConfigLib.ConfigInfo['CmdFileName']
    CaseRootTxt = ConfigLib.ConfigInfo['CaseRootTxt']
    CmdFileName = ConfigLib.ConfigInfo['CmdFileName']
    BimxFileDir = ConfigLib.ConfigInfo['BimxFileDir']
    PDOFileDir = ConfigLib.ConfigInfo['PDOFileDir']
    ProjectName = ConfigLib.ConfigInfo['ProjectName']
    ExpectedLogName = ConfigLib.ConfigInfo['ExpectedLogName']
    RGTRepository = ConfigLib.ConfigInfo['RGTRepository']
    ResultDir = ConfigLib.ConfigInfo['ResultDir']
    PreBuildFolder = os.path.join(os.getcwd(), ConfigLib.ConfigInfo['PreBuild'])
    TempEtcPath = os.path.join(os.getcwd(), 'etc')

    InstallationPDOFilePath = os.path.join(InstallerLib.InstallerConfigInfo['PDOFileDir'], InstallerLib.InstallerConfigInfo['InstallationInventory'])
    PlatformProjPDOFilePath = os.path.join(InstallerLib.InstallerConfigInfo['PDOFileDir'], InstallerLib.InstallerConfigInfo['PlatformProjectInventory'])
    RepositoryPDOFilePath = os.path.join(InstallerLib.InstallerConfigInfo['PDOFileDir'], InstallerLib.InstallerConfigInfo['RepositoryInventory'])

    Parameters = []
    if 'Linux' in platform.system():
        if len(sys.argv) != 1:
            print 'Usage:', sys.argv[0]
            quit()
    else:
        for param in sys.argv[1:]:
            Parameters.append(param[:2] + param[2:].lower())

        ValidParam = [
            '--installer',
            '--autoreport'
        ]
        for param in Parameters:
            if not param in ValidParam:
                print 'Invalid parameter:', param
                print 'Usage:',sys.argv[0],'[--AutoRerpot] [--Installer]'
                quit()

    #
    #   Just for windows.
    #
    if "--installer" in Parameters:
        InstallerLib.WindowsInstaller()

    #
    #   1. Set environment variable.
    #   2. Check each test case, make sure all test case are not corruption.
    #   3. Clean up each test case, just remain cmd.txt and ExpectedResult.
    #   4. Replace the commnad path in cmd.txt file.
    #   5. Back up etc folder.
    #   6-8. Change PDO file for test.
    #   9. Update the .bimx files.
    #   10. Update the special repository.
    #   11. Do pre-build on .bimx files.
    #   12. Run all test case.
    #   13. Clean up the pre-build result.
    #   14. Recover the etc folder.
    #   15. Compare the test result.
    #   16. Save the compare result to .xls file.
    #
    InstallerLib.SetEnvVar()
    TCSLib.RecursiveCheckTCS(TestCaseDir, ExpectedDirName, ExpectedLogName, CmdFileName)
    TCSLib.RecursiveCleanUpTCS(TestCaseDir, ExpectedDirName, CmdFileName)
    CmdLib.RecursiveReplaceCmd(TestCaseDir, CaseRootTxt, CmdFileName)

    CommonLib.CopyFolder(InstallerLib.InstallerConfigInfo['PDOFileDir'], TempEtcPath)
    PDOLib.ModifyPDOFile(RepositoryPDOFilePath, "Path", RGTRepository)
    PDOLib.ModifyPDOFile(PlatformProjPDOFilePath, "Path", os.path.join(os.getcwd(), ProjectName))
    PDOLib.ModifyPDOFile(InstallationPDOFilePath, "Repository", RGTRepository)
    UpdateBim.UpdateBim(InstallationPDOFilePath,BimxFileDir)

    UpdateRepository.DoUpdateRepo(RGTRepository)
    BimMapFolder = PreBuildLib.DoPreBuild(BimxFileDir, PreBuildFolder)

    DoRun.RunAllTestCase(BimMapFolder)
    PreBuildLib.CleanUpPreBuild(PreBuildFolder)
    CommonLib.CopyFolder(TempEtcPath, InstallerLib.InstallerConfigInfo['PDOFileDir'], True)

    CompareResult = CompareLib.Compare()
    ExlLib.SaveReport(CompareResult, ResultDir)

    #
    #   Just for windows.
    #
    if "--autoreport" in Parameters:
        AutoReportLib.DoAutoReport(CompareResult)