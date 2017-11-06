import os
import xlrd

class GenerateHtmReport(object):
    def __init__(self, reportHtm, projectName, date, sdbVer, installerVer, passNum, failNum, blockedNum, importantFailNum, importantFailExcel, sharelocation):
        self.tempHtm       = reportHtm.replace('report.htm', 'TemplateReport\\TemplateReport.htm')
        self.reportHtm     = reportHtm
        self.projectName   = projectName
        self.date          = date
        self.sdbVer        = sdbVer
        self.installerVer  = installerVer
        self.passNum       = str(passNum)
        self.failNum       = str(failNum)
        self.blockedNum    = str(blockedNum)
        self.total         = str(passNum + failNum + blockedNum)
        self.importantFailNum = str(importantFailNum)
        self.importantFailExcel = importantFailExcel
        self.passRate      = '%.2f%%' % (float(passNum)/float(passNum + failNum + blockedNum)*100)
        self.sharelocation = sharelocation
    
    def generateHtm(self):
        tempfile = open(self.tempHtm, 'r')    
        tempcont = tempfile.read()
        tempfile.close()
        
        tempcont = tempcont.replace('$Project', self.projectName)
        tempcont = tempcont.replace('$Date', self.date)
        tempcont = tempcont.replace('$SdbVer', self.sdbVer)
        tempcont = tempcont.replace('$InstallerVer', self.installerVer)
        tempcont = tempcont.replace('$passnum', self.passNum)
        tempcont = tempcont.replace('$failnum', self.failNum)
        tempcont = tempcont.replace('$blockednum', self.blockedNum)
        tempcont = tempcont.replace('$total', self.total)
        tempcont = tempcont.replace('$passrate', self.passRate)
        tempcont = tempcont.replace('$sharelocation', self.sharelocation)
        tempcont = tempcont.replace('$TotalImportantFailure', self.importantFailNum)
        tempcont = tempcont.replace('$ImportantFailureList', self.genImportantFailureHtm())
        
        reportfile = open(self.reportHtm, 'w')
        reportfile.write(tempcont)
        reportfile.close()
    
    def generateMailTitle(self):
        titleTemp = "[Auto][OC][Win10][SDB]$Project Test Report $Date[Pass rate $passrate]"
        titleTemp = titleTemp.replace('$Project', self.projectName)
        titleTemp = titleTemp.replace('$Date', self.date)
        titleTemp = titleTemp.replace('$passrate', self.passRate)
        title = titleTemp
        return title

    # Gnerate Important Failure htm content
    def genImportantFailureHtm(self):
        pathRoot = self.sharelocation
        htmAll = []
        redTd = """<td width=auto nowrap style='width:auto;border:solid windowtext 1.0pt;\
                    padding:0in 5.4pt 0in 5.4pt;height:15.0pt'>\
                    <p class=MsoNormal align=center style='text-align:center'><span\
                    style='mso-bookmark:_MailOriginal'><span style='font-size:11.0pt;font-family:\
                    "Calibri",sans-serif;color:red'>content</span></span><span\
                    style='mso-bookmark:_MailOriginal'><span style='font-size:11.0pt;font-family:\
                    "Calibri",sans-serif;color:black'><o:p></o:p></span></span></p>\
                    </td>"""
        # redTd=  '<td style="width:auto;border: 1px solid #888888;background:#ffffff;padding:2px 3px 2px 3px;font-weight:bold;color:Red;font-size:12px;font-family:Arial">content</td>'
        aHref = """<a href="file://rootPath">content</a>"""

        table = """<table class=MsoNormalTable border=0 cellspacing=0 cellpadding=0 width=0\
                   style='width:143.75pt;margin-left:-.15pt;border-collapse:collapse;mso-yfti-tbllook:\
                   1184;mso-padding-alt:0in 0in 0in 0in'>"""
        tableEnd = '</table>'
        tr = "<tr style='mso-yfti-irow:1;mso-yfti-lastrow:yes;height:15.0pt'>"
        trEnd = '</tr>'
        wb = xlrd.open_workbook(self.importantFailExcel, formatting_info=True)
        sheet = wb.sheet_by_name('Details')

        nColumns = sheet.ncols
        nRows = sheet.nrows

        for i in range(1, nRows):
            for j in range(0, nColumns):
                tmp = sheet.cell_value(i, j)
                if isinstance(tmp, float) and str(tmp).endswith('.0'):
                    tbContent = str(int(tmp))
                else:
                    tbContent = str(tmp)

                if tbContent == "":
                    tbContent = '&nbsp;'
                else:
                    if pathRoot and os.path.exists(os.path.join(pathRoot, 'TCS\\'+ tbContent)):
                        tbContent = aHref.replace('rootPath', os.path.join(pathRoot, 'TCS\\'+ tbContent)).replace('content', tbContent)

                htmContent = tr + redTd.replace('content', tbContent) + trEnd
                htmAll.append(htmContent)

        return   table + '\n'.join(htmAll) + tableEnd


        