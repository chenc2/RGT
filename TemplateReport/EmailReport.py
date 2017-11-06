#! /usr/bin/python
# Author       : Zhengyuxin   yuxin.zheng@intel.com
# Create Time  : 2011-7-18 02:55:31
# Description  : 
from platform import system
import os
import sys
import re
import subprocess

class Email(object):
    "Send report as email"
    
    def __init__(self,toList,ccList,subject,reportHtm,attachmentList):
        self.toList=toList
        self.ccList=ccList
        self.subject=subject
        self.reportHtm=reportHtm
        self.attachmentList=attachmentList
        
        print "this Email will be sent to %s" % ';'.join(self.toList)
    
    def createTxt(self,name,content):
        f=open(name,'w')
        f.write(content)
        f.close() 
        
    def genTxt(self):
        
        self.createTxt('__EMail_To_File.txt',';'.join(self.toList))
        self.createTxt('__EMail_Cc_File.txt',';'.join(self.ccList))
        self.createTxt('__EMail_Subject_File.txt',self.subject)
        self.createTxt('__Email_Attachment_File.txt',';'.join(self.attachmentList))
        
        f=open(self.reportHtm,'r')
        htmTmp=f.read()
        f.close()
        
        fTxt=open('__Email_Body_File.txt','w')
        fTxt.write(htmTmp)
        fTxt.close()
        
    def sendEmail(self):
        
        self.genTxt()

        if system()=='Windows':
        
            f=open('SendReport.bat','w')
            f.write(\
    '''
    set __EMail_To=.\__EMail_To_File.txt
    set __EMail_Cc=.\__EMail_Cc_File.txt
    set __Email_Subject=.\__EMail_Subject_File.txt
    set __EMail_Body=.\__Email_Body_File.txt
    set __EMail_Attachment=.\__Email_Attachment_File.txt
    SendEmail.exe
    '''
                    )
            f.close()
            bat_name='SendReport.bat'
            sendEmailSP=subprocess.Popen('SendReport.bat',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        else:
            f=open('SendReport.sh','w')
            f.write(\
    '''
    export __EMail_To=./__EMail_To_File.txt
    export __EMail_Cc=./__EMail_Cc_File.txt
    export __EMail_Subject=./__EMail_Subject_File.txt
    export __EMail_Body=./__Email_Body_File.txt
    export __EMail_Attachment=.\__Email_Attachment_File.txt
    mono .SendEmail.exe
    '''
                    )
            f.close()
            bat_name='SendReport.sh'
            os.system('chmod +x '+'SendReport.sh')
            sendEmailSP=subprocess.Popen('./SendReport.sh',
                                                 stdin=subprocess.PIPE,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE,
                                                 shell=True)
        msg=sendEmailSP.communicate()
        # print 'stdout:'
        # print msg[0]
        # print 'stderr:'
        print msg[1]
        # print 'finished' 
        mailList=[bat_name,'__Email_Body_File.txt','__EMail_Cc_File.txt','__EMail_Subject_File.txt','__EMail_To_File.txt', '__Email_Attachment_File.txt']
        try:
            for siFile in mailList:
                os.remove(siFile)
        except Exception,e:
            print e
        
if __name__ == '__main__':
    pass
        
        
