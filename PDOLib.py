# -*- coding: UTF-8 -*-

import ConfigLib
import platform
import os
import shutil

#
#   Construct a new RepositoryInventory.pdo file by an exists PDO file.
#
def CreateNewRepositoryPDO(TheOldFile):
    fd = open(TheOldFile)

    Lines = []
    for line in fd.readlines():
        Lines.append(line.strip('\n'))
    fd.close()
    
    String = ''
    for index in range(0,len(Lines)):
        if Lines[index] == '[Globals]':
            String = String + '[Globals]' + '\n'
            String = String + Lines[index+1] + '\n'
            String = String + Lines[index+2] + '\n'

    assert(len(String) != 0)
            
    fd = open(os.path.join(ConfigLib.ConfigInfo.PDOFilePath, 'PlatformProjectInventory.pdo'), 'w')
    fd.write(String)
    fd.write('[Project_2]\n')
    fd.write('Path = ' + os.path.join(os.getcwd(),ConfigLib.ConfigInfo.ProjectName))
    fd.close()

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
    fd = open(os.path.join(ConfigLib.ConfigInfo.PDOFilePath, FileName))
    for line in fd.readlines():
        if line.find(KeyName) == 0:
            if 'Linux' in platform.system():
                return line.split('=')[1][1:].strip('\n') + '/'
            else:
                return line.split('=')[1][1:].strip('\n') + '\\'
    assert(False)