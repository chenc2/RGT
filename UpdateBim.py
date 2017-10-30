# -*- coding: UTF-8 -*-
import os
import PDOLib
import CommonLib

#
#   更新.bimx文件中ToolPath和Repository的值，需要符合当前测试环境。
#
def UpdateBim(InstallerPDO, BimxFileDir):
    ToolPath = '"' + PDOLib.GetValueFromPDO(InstallerPDO, 'ToolSet') + '"'
    RepoPath = '"' + PDOLib.GetValueFromPDO(InstallerPDO, 'Repository') + '"'

    for file in os.listdir(BimxFileDir):
        String = CommonLib.ReadFile(os.path.join(BimxFileDir, file))

        Index1 = String.find('ToolPath=') + len('ToolPath') + 1
        Index2 = String.find('ToolVer=') - 1

        String = String.replace(String[Index1:Index2], ToolPath)

        Index1 = String.find('RepositoryPath=') + len('RepositoryPath') + 1
        Index2 = String.find('"', Index1 + 1) + 1

        String = String.replace(String[Index1:Index2], RepoPath)

        CommonLib.WriteFile(os.path.join(BimxFileDir, file), String)