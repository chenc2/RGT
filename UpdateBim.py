# -*- coding: UTF-8 -*-

import ConfigLib
import os
import PDOLib

#
#   Update the path of ToolSet.
#   If the path of ToolSet in the .bimx file is not same as the path in the pdo file,
#   It will cause error when run RGT tool, so We need to replace the path before run.
#   
#   Update the path of Repository.
#
def UpdateBim():
    ToolPath = '"' + PDOLib.GetValueFromPDO('ToolsetInventory.pdo', 'Path')[:-1] + '"'
    RepoPath = '"' + PDOLib.GetValueFromPDO('RepositoryInventory.pdo', 'Path')[:-1] + '"'

    assert(ToolPath != "")
    assert(RepoPath != "")

    for file in os.listdir(ConfigLib.ConfigInfo.BimFilePath):
        fd = open(os.path.join(ConfigLib.ConfigInfo.BimFilePath, file))
        String = fd.read()
        fd.close()

        Index1 = String.find('ToolPath=') + len('ToolPath') + 1
        Index2 = String.find('ToolVer=') - 1

        String = String.replace(String[Index1:Index2], ToolPath)

        Index1 = String.find('RepositoryPath=') + len('RepositoryPath') + 1
        Index2 = String.find('"', Index1 + 1) + 1

        String = String.replace(String[Index1:Index2], RepoPath)

        fd = open(os.path.join(ConfigLib.ConfigInfo.BimFilePath, file), 'w')
        fd.write(String)
        fd.close()