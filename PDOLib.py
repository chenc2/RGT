# -*- coding: UTF-8 -*-
from ConfigLib import ConfigInfo
import platform
import os
import shutil
import CommonLib

#
#   Construct a new RepositoryInventory.pdo file by an exists PDO file.
#
def CreateNewRepositoryPDO(TheOldFile):
    Lines = CommonLib.ReadFileList(TheOldFile)
    
    String = ''
    for index in range(0,len(Lines)):
        if Lines[index] == '[Globals]':
            String = String + '[Globals]' + '\n'
            String = String + Lines[index+1] + '\n'
            String = String + Lines[index+2] + '\n'

    assert(len(String) != 0)

    String = String + '[Project_2]\n' + 'Path = ' + os.path.join(os.getcwd(),ConfigInfo.ProjectName)
    CommonLib.WriteFile(os.path.join(ConfigInfo.PDOFileDir, 'PlatformProjectInventory.pdo'), String)

#
#
#
def MovePDO(Src, Dst, DeleteSrc = False):
    if not os.path.isdir(Src):
        assert(False)

    if os.path.isdir(Dst):
        shutil.rmtree(Dst)
    elif os.path.isfile(Dst):
        assert(False)
    
    shutil.copytree(Src,Dst)

    if DeleteSrc:
        shutil.rmtree(Src)

#
#   Get the value of PDO file by one key-name.
#
def GetValueFromPDO(FileName, KeyName):
    List = CommonLib.ReadFileList(os.path.join(ConfigInfo.PDOFileDir, FileName))
    slash = '\\'
    if 'Linux' in platform.system():
        slash = '/'

    for line in List:
        if line.find(KeyName) == 0:
                return line.split('=')[1][1:].strip('\n') + slash

    assert(False)