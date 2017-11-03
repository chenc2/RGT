# -*- coding: UTF-8 -*-
import os
import PDOLib
import InstallerLib
import subprocess
import os

def DoUpdateRepo(SpecialRepoPath):
    if not os.path.isdir(SpecialRepoPath):
        print 'Not invalid repo path:',SpecialRepoPath
        assert(False)

    RepoInfoPDO = os.path.join(SpecialRepoPath, 'RepositoryInformation.pdo')
    RepoName = PDOLib.GetValueFromPDO(RepoInfoPDO, 'RepositoryName')

    Info = InstallerLib.GetConfigInfo()
    Path = PDOLib.GetValueFromPDO(os.path.join(Info['PDOFileDir'], Info['InstallationInventory']), 'ToolSet')
    Path = os.path.join(Path, 'RMT')
    Path = '"' + Path + '"'
    Cmd = Path + ' -p ' + RepoName
    os.system(Cmd)