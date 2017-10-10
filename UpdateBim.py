# -*- coding: UTF-8 -*-
from ConfigLib import ConfigInfo
import os
import PDOLib
import CommonLib

#
#   更新.bimx文件中ToolPath和Repository的值，需要符合当前测试环境。
#
def UpdateBim():
    ToolPath = '"' + PDOLib.GetValueFromPDO('ToolsetInventory.pdo', 'Path')[:-1] + '"'
    RepoPath = '"' + PDOLib.GetValueFromPDO('RepositoryInventory.pdo', 'Path')[:-1] + '"'

    assert(ToolPath != "")
    assert(RepoPath != "")

    for file in os.listdir(ConfigInfo.BimxFileDir):
        String = CommonLib.ReadFile(os.path.join(ConfigInfo.BimxFileDir, file))

        Index1 = String.find('ToolPath=') + len('ToolPath') + 1
        Index2 = String.find('ToolVer=') - 1

        String = String.replace(String[Index1:Index2], ToolPath)

        Index1 = String.find('RepositoryPath=') + len('RepositoryPath') + 1
        Index2 = String.find('"', Index1 + 1) + 1

        String = String.replace(String[Index1:Index2], RepoPath)

        CommonLib.WriteFile(os.path.join(ConfigInfo.BimxFileDir, file), String)