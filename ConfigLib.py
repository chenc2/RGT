# -*- coding: UTF-8 -*-
import xml.dom.minidom
import platform
import os

#
#   读取Config.xml配置文件。
#
class Config:
    def __init__(self):
        root = xml.dom.minidom.parse('Config.xml').documentElement
        self.ExpectedDirName = root.getElementsByTagName('ExpectedDirName')[0].firstChild.data
        self.ExpectedLogName = root.getElementsByTagName('ExpectedLogName')[0].firstChild.data

        self.TestDirName    = root.getElementsByTagName('TestDirName')[0].firstChild.data
        self.TestLogName    = root.getElementsByTagName('TestLogName')[0].firstChild.data
    
        self.CompDirName    = root.getElementsByTagName('CompDirName')[0].firstChild.data
        self.CompLogName    = root.getElementsByTagName('CompLogName')[0].firstChild.data
        self.CompCSVName    = root.getElementsByTagName('CompCSVName')[0].firstChild.data

        self.CmdFileName    = root.getElementsByTagName('CmdFileName')[0].firstChild.data

        self.ProjectName    = root.getElementsByTagName('ProjectName')[0].firstChild.data
        self.CaseRootTxt    = root.getElementsByTagName('CaseRootTxt')[0].firstChild.data

        if (    self.ExpectedDirName == "" or \
                self.ExpectedLogName == "" or \
                self.TestDirName == "" or \
                self.TestLogName == "" or \
                self.CompDirName == "" or \
                self.CompLogName == "" or \
                self.CmdFileName == "" or \
                self.ProjectName == "" or \
                self.CaseRootTxt == ""
           ):
            print "Please check config.xml file, it has error configuration."
            assert(False)

        if 'Linux' in platform.system():
            self.PDOFileDir  = root.getElementsByTagName('LinPDOFileDir')[0].firstChild.data
            if not os.path.isdir(self.PDOFileDir):
                print "Please check the path of PDO files."
                assert(False)
        else:
            self.PDOFileDir  = root.getElementsByTagName('WinPDOFileDir')[0].firstChild.data
            if not os.path.isdir(self.PDOFileDir):
                print "Please check the path of PDO files."
                assert(False)

        self.TestCaseDir    = root.getElementsByTagName('TestCaseDir')[0].firstChild.data
        self.BimxFileDir    = root.getElementsByTagName('BimxFileDir')[0].firstChild.data
        self.ResultDir      = root.getElementsByTagName('ResultDir')[0].firstChild.data
        self.ExceptionDir   = root.getElementsByTagName('ExceptionDir')[0].firstChild.data

        if (    not os.path.isdir(self.TestCaseDir) or \
                not os.path.isdir(self.BimxFileDir) or \
                not os.path.isdir(self.ResultDir) or 
                not os.path.isdir(self.ExceptionDir)
           ):
            print "Please check config.xml file, it has error configuration."
            assert(False)

ConfigInfo = Config()