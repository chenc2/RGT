# -*- coding: UTF-8 -*-
import xlwt
import os

#
#   Each ResultInfo is the list type.
#   ResultInfo[x][0] is the path of test case
#   ResultInfo[x][1] is the result of compare csv
#   ResultInfo[x][2] is the result of compare log
#
def SaveReport(ResultInfo, ResultDir):
    xls = xlwt.Workbook()
    Sheet = xls.add_sheet('RGT_Cmd_Result')

    Sheet.write(0, 0, 'Test Case Path')
    Sheet.write(0, 1, 'Compare CSV')
    Sheet.write(0, 2, 'Compare Log')
    Sheet.write(0, 3, 'Case Result')

    Row = 1
    for Case in ResultInfo:
        Sheet.write(Row, 0, Case[0])
        Sheet.write(Row, 1, Case[1])
        Sheet.write(Row, 2, Case[2])

        if Case[1] == u'[True]' and (Case[2] == u'[True]' or Case[2] == u'[#True#]'):
            Sheet.write(Row, 3, u'Pass')
        else:
            Sheet.write(Row, 3, u'Fail')

        Row = Row + 1

    SavePath = os.path.join(ResultDir, 'RGT_Cmd_Report.xls')
    if os.path.isfile(SavePath):
        os.remove(SavePath)
    xls.save(SavePath)

PassFormat = xlwt.easyxf( \
    'font: name Verdana, height 160, bold on, colour_index 3;' \
    'align: wrap on, vert centre, horiz centre;'
     )

FailFormat = xlwt.easyxf( \
    'font: name Verdana, height 160, bold on, colour red;' \
    'align: wrap on, vert centre, horiz centre;'
     )

LinkFormat = xlwt.easyxf( \
    'font: name Verdana, colour blue;' \
    'align: vert centre, horiz left;'
     )

CellFormat = xlwt.easyxf( \
    'font: name Verdana, height 160, bold on;' \
    'align: wrap on, vert centre, horiz centre;'
     )

#
#   Save excel.
#
def SaveReportEx(ResultInfo,ResultDir,TestCaseDir,ShareLocation):
    xls = xlwt.Workbook()
    Sheet = xls.add_sheet('RGT_Cmd_Result')

    Sheet.write(0, 0, 'Test Case Path')
    Sheet.write(0, 1, 'Compare CSV')
    Sheet.write(0, 2, 'Compare Log')
    Sheet.write(0, 3, 'Case Result')

    Row = 1
    for Case in ResultInfo:
        Name = os.path.join(os.path.basename(TestCaseDir),Case[0][len(TestCaseDir)+1:])
        Link = os.path.join(ShareLocation, Name)

        Sheet.write(Row, 0, xlwt.Formula('HYPERLINK("%s";"%s")' %(Link,Name)), LinkFormat)
        Sheet.write(Row, 1, Case[1], CellFormat)
        Sheet.write(Row, 2, Case[2], CellFormat)

        if Case[1] == u'[True]' and Case[2] == u'[True]':
            Sheet.write(Row, 3, u'Pass', PassFormat)
        else:
            Sheet.write(Row, 3, u'Fail', FailFormat)

        Row = Row + 1

    SavePath = os.path.join(ResultDir, 'RGT_Cmd_Report.xls')
    if os.path.isfile(SavePath):
        os.remove(SavePath)
    xls.save(SavePath)