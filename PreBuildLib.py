# -*- coding: UTF-8 -*-
import CommonLib
import os
import shutil
import subprocess

#
#   Pre build .bimx files, it will prompt test performance.
#
def DoPreBuild(BimxFileDir, PreBuildFolder):
    PreBuildFolder = os.path.join(os.getcwd(), PreBuildFolder)
    CommonLib.CreateDir(PreBuildFolder)

    BimMapPath = dict()

    for file in os.listdir(BimxFileDir):
        if file[-5:] != '.bimx':
            print file,'is an invalid .bimx file, please check.'
            assert(False)

        CommonLib.CreateDir(os.path.join(PreBuildFolder, file[:-5]))

        SrcFile = os.path.join(BimxFileDir, file)
        DstFile = os.path.join(PreBuildFolder, file[:-5], file)
        shutil.copyfile(SrcFile, DstFile)
        
        '''
        AsmRet = subprocess.Popen(['Assemble', DstFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        AsmRet.communicate()
        if AsmRet.returncode != 0:
            print DstFile,'Pre build fail, please check.'
            assert(False)
        '''

        BimMapPath[file[:-5]] = os.path.join(PreBuildFolder, file[:-5])

    return BimMapPath

#
#   Clean up pre-build data.
#
def CleanUpPreBuild(PreBuildFolder):
    while 1:
        try:
            shutil.rmtree(PreBuildFolder)
            break
        except:
            pass