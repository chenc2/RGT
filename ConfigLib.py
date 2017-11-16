# -*- coding: UTF-8 -*-
import xml.dom.minidom
import os
import InstallerLib
import platform

ConfigInfo = dict()

def InitializeConfigXml():
    SectionNameList = [
        'ExpectedDirName',
        'ExpectedLogName',

        'TestDirName',
        'TestLogName',

        'CompDirName',
        'CompLogName',
        'CompCSVName',

        'CmdFileName',

        'ProjectName',
        'PreBuild',
        'CaseRootTxt',

        'ExceptionDir',
        'RGTRepository',

        'TestCaseDir',
        'BimxFileDir',
        'ResultDir',
        'ShareFolder',

        'SendTo',
        'CCTo',
        'FailReport',
    ]

    root = xml.dom.minidom.parse('Config.xml').documentElement
    for Name in SectionNameList:
        ConfigInfo[Name] = root.getElementsByTagName(Name)[0].firstChild.data

    ConfigInfo['PDOFileDir'] = InstallerLib.InstallerConfigInfo['PDOFileDir']

    CheckDir = [
        'TestCaseDir',
        'BimxFileDir',
        'ResultDir',
        'RGTRepository',
    ]
    for Dir in CheckDir:
        if not os.path.isdir(ConfigInfo.get(Dir)):
            print ConfigInfo.get(Dir),'is an invalid path, please check.(ConfigLib)'
            assert(False)

    if 'Linux' not in platform.system():
        if not os.path.isdir(ConfigInfo.get('ShareFolder')):
            print ConfigInfo.get(Dir),'is an invalid path, please check.(ConfigLib)'
            assert(False)

def GetConfigInfo():
    if len(ConfigInfo) == 0:
        print 'Lib is not initialized.'
        assert(False)

    return ConfigInfo