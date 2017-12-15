# -*- coding: UTF-8 -*-
import xlwt
import socket
import os
import xlwt
import CommonLib
import ConfigLib
import time
import platform
import InstallerLib
import PDOLib
import shutil
import sys 

sys.path.append(r'TemplateReport') 
import EmailReport
import GenerateHtmReport

FirstLineFormat = xlwt.easyxf( \
    'font: name Verdana, height 160, bold on, colour black;' \
    'align: wrap on, vert centre, horiz centre;'
     )
LinkFormat = xlwt.easyxf( \
    'font: name Verdana, colour blue;' \
    'align: vert centre, horiz left;'
)
TitleFormat = xlwt.easyxf( \
    'font: bold on, name Verdana, colour white, ;' \
    'borders: left Thin, right Thin, top Thin, bottom Thin;' \
    'align: wrap on, vert centre, horiz center;pattern: pattern solid, fore-colour blue;'
)
PassFormat = xlwt.easyxf( \
    'font: name Verdana, height 160, bold on, colour_index 3;' \
    'align: wrap on, vert centre, horiz centre;'
     )
FailFormat = xlwt.easyxf( \
    'font: name Verdana, height 160, bold on, colour red;' \
    'align: wrap on, vert centre, horiz centre;'
     )
CellFormat = xlwt.easyxf( \
    'font: name Verdana;' \
    'align: vert centre, horiz centre;'
     )

def SaveReport(ShareLocation, ResultInfo):
    xls = xlwt.Workbook()
    Sheet = xls.add_sheet('RGT Command Line')

    HostName = socket.gethostname()
    PassCount   = 0
    FailList    = []

    Sheet.col(0).width = 0x5000
    Sheet.col(1).width = 0x1000
    Sheet.col(2).width = 0x1000
    Sheet.col(3).width = 0x1000
    Sheet.write(0, 0, 'Test Case Path', FirstLineFormat)
    Sheet.write(0, 1, 'Compare CSV', FirstLineFormat)
    Sheet.write(0, 2, 'Compare Log', FirstLineFormat)
    Sheet.write(0, 3, 'Case Result', FirstLineFormat)

    Row = 1
    ConfigInfo = ConfigLib.GetConfigInfo()
    for Case in ResultInfo:
        NewPath = Case[0].replace(ConfigInfo['TestCaseDir'], ShareLocation)
        DriverDisk = NewPath[:NewPath.find('\\')]
        Link = NewPath.replace(DriverDisk, '\\\\' + HostName)

        Sheet.write(Row, 0, xlwt.Formula('HYPERLINK("%s";"%s")' %(Link, NewPath)), LinkFormat)
        Sheet.write(Row, 1, Case[1], CellFormat)
        Sheet.write(Row, 2, Case[2], CellFormat)

        if Case[1] == u'[True]' and (Case[2] == u'[True]' or Case[2] == u'[#True#]'):
            Sheet.write(Row, 3, u'Pass', PassFormat)
            PassCount = PassCount + 1
        else:
            Sheet.write(Row, 3, u'Fail', FailFormat)
            FailList.append(Case[0])

        Row = Row + 1

    xls.save(os.path.join(ShareLocation, 'RGT_Cmd_Report.xls'))
    return [PassCount, FailList]

#
#
#
def GenFailTestCaseReport(FailList):
    ConfigInfo = ConfigLib.GetConfigInfo()

    WorkBook = xlwt.Workbook()
    
    DetailsSheet = WorkBook.add_sheet('Details')
    DetailsSheet.col(0).width = 0x8000
    DetailsSheet.write(0, 0, 'Detail Case', TitleFormat)

    SummarySheet = WorkBook.add_sheet('Summary')
    SummarySheet.col(0).width = 0x3000
    SummarySheet.write(0, 0, 'Fail', TitleFormat)

    for index in range(0,len(FailList)):
        DetailsSheet.write(index + 1, 0, FailList[index])

    SummarySheet.write(1, 0, len(FailList), FailFormat)

    WorkBook.save(os.path.join(os.getcwd(), ConfigInfo['FailReport']))

#
#   Generate report.htm and send the report.
#
def GenHtmReportAndSendReport(PassNumber, FailNumber, ShareLocation):
    ConfigInfo = ConfigLib.GetConfigInfo()
    InstallerInfo = InstallerLib.GetConfigInfo()

    DriverDisk = ShareLocation[:ShareLocation.find('\\')]
    Link = ShareLocation.replace(DriverDisk, '\\\\' + socket.gethostname())

    SdbToolVer = InstallerInfo.get('SdbToolVersion')
    if SdbToolVer == None:
        SdbToolVer = '0'

    htm = GenerateHtmReport.GenerateHtmReport(
            os.path.join(os.getcwd(), 'report.htm'),
            'RGT Command Line',
            time.strftime('%Y-%m-%d', time.localtime()),
            SdbToolVer, 
            PDOLib.GetValueFromPDO(os.path.join(InstallerInfo['PDOFileDir'], InstallerInfo['InstallationInventory']), 'ProductVersion'),
            PassNumber,
            FailNumber,
            0,
            FailNumber,
            os.path.join(os.getcwd(), ConfigInfo['FailReport']),
            Link.encode('ascii'))
    htm.generateHtm()

    if platform.system() == 'Windows':
        em = EmailReport.Email(
                [ConfigInfo['SendTo']],
                [ConfigInfo['CCTo']],
                htm.generateMailTitle(),
                os.path.join(os.getcwd(), 'report.htm'),
                [os.path.join(os.getcwd(), ConfigInfo['FailReport'])])
        try:
            em.sendEmail()
        except Exception, e:
            print e

    shutil.move(os.path.join(os.getcwd(), 'report.htm'), ShareLocation)
    shutil.move(os.path.join(os.getcwd(), ConfigInfo['FailReport']), ShareLocation)

#
#   Copy the test result to the share location.
#
def CopyResultToShareLocation():
    ConfigInfo = ConfigLib.GetConfigInfo()
    CurrentTimeStamp = time.strftime("%Y_%m_%d_%H%M%S", time.localtime(time.time()))
    ShareLocation = os.path.join(ConfigInfo['ShareFolder'], CurrentTimeStamp)
    CommonLib.CopyFolder(ConfigInfo['TestCaseDir'], ShareLocation)
    return ShareLocation

def DoAutoReport(CompareResult):
    ShareLocation = CopyResultToShareLocation()
    ReportInfo = SaveReport(ShareLocation, CompareResult)
    GenFailTestCaseReport(ReportInfo[1])
    GenHtmReportAndSendReport(ReportInfo[0], len(ReportInfo[1]), ShareLocation)