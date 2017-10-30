# -*- coding: UTF-8 -*-
import xml.dom.minidom
import os
import InstallerLib

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
        'CaseRootTxt',

        'ExceptionDir',
        'RGTRepository',

        'TestCaseDir',
        'BimxFileDir',
        'ResultDir',
    ]

    root = xml.dom.minidom.parse('Config.xml').documentElement
    for Name in SectionNameList:
        ConfigInfo[Name] = root.getElementsByTagName(Name)[0].firstChild.data

    ConfigInfo['PDOFileDir'] = InstallerLib.InstallerConfigInfo['PDOFileDir']

    CheckDir = [
        'TestCaseDir',
        'BimxFileDir',
        'ResultDir',
        'RGTRepository'
    ]
    for Dir in CheckDir:
        if not os.path.isdir(ConfigInfo.get(Dir)):
            print ConfigInfo.get(Dir),'is an invalid path, please check.(ConfigLib)'
            assert(False)

def GetConfigInfo():
    return ConfigInfo