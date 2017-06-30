# -*- coding: UTF-8 -*-
import xml.dom.minidom
import platform

class Config:
    def __init__(self):
        root = xml.dom.minidom.parse('Config.xml').documentElement
        self.Expected = root.getElementsByTagName('Expected')[0].firstChild.data
        self.Command = root.getElementsByTagName('Command')[0].firstChild.data
        self.ExpectedLogName = root.getElementsByTagName('ExpectedLogName')[0].firstChild.data
        self.TestDirName = root.getElementsByTagName('TestDirName')[0].firstChild.data
        self.CompDirName = root.getElementsByTagName('CompDirName')[0].firstChild.data
        self.TestLogName = root.getElementsByTagName('TestLogName')[0].firstChild.data
        self.CompLogName = root.getElementsByTagName('CompLogName')[0].firstChild.data
        self.CompCSVName = root.getElementsByTagName('CompCSVName')[0].firstChild.data
        self.ProjectName = root.getElementsByTagName('ProjectName')[0].firstChild.data
        self.CaseRootTxt = root.getElementsByTagName('CaseRootTxt')[0].firstChild.data

        if 'Linux' in platform.system():
            self.TestCaseRoot = root.getElementsByTagName('Linux-TestCaseRoot')[0].firstChild.data
            self.BimFilePath = root.getElementsByTagName('Linux-BimFilePath')[0].firstChild.data
            self.PDOFilePath = root.getElementsByTagName('Linux-PDOFilePath')[0].firstChild.data
        else:
            self.TestCaseRoot = root.getElementsByTagName('Win-TestCaseRoot')[0].firstChild.data
            self.BimFilePath = root.getElementsByTagName('Win-BimFilePath')[0].firstChild.data
            self.PDOFilePath = root.getElementsByTagName('Win-PDOFilePath')[0].firstChild.data


ConfigInfo = Config()