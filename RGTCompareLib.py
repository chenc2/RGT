# -*- coding: utf-8 -*-

#
#   为RGT测试提供封装，内部调用CompareLib.py实现。
#

import os
import CSVLib
import CompareLib
import filecmp

def ReadFileString(FilePath):
    fd = open(FilePath, 'r')
    string = fd.read()
    fd.close()
    return string

def IsContainSubStr(String, SubStr):
    return String.find(SubStr) != -1

def BothContainSubStr(String1, String2, SubStr):
    if String1.find(SubStr) != -1 and String2.find(SubStr) != -1:
        return True
    else:
        return False

#
#   Expected:       保存期待.csv的目录
#   Test:           保存测试.csv的目录
#   SaveFilePath:   保存比较结果的目录
#
def CompareOneCaseCSV(Expected,Test,SaveFilePath):
    CSVFile1 = CSVLib.GetCSVFiles(Expected)
    CSVFile2 = CSVLib.GetCSVFiles(Test)
    fd = open(SaveFilePath, 'w')

    if len(CSVFile1) == 0 and len(CSVFile2) == 0:
        fd.write("Both no csv")
    elif len(CSVFile1) == 0 and len(CSVFile2) != 0:
        fd.write("Expected no csv")
    elif len(CSVFile1) != 0 and len(CSVFile2) == 0:
        fd.write("Test no csv")
    else:
        fd.close()
        #
        #   默认RGT的每个Test Case中只生成1个.csv文件。
        #
        assert(len(CSVFile1) == 1 and len(CSVFile2) == 1)
        CompareLib.DoCompareCSV(CSVFile1.get(CSVFile1.keys()[0]),
                                CSVFile2.get(CSVFile2.keys()[0]),
                                SaveFilePath)
    fd.close()

#
#   ExpectedLogPath:    期待log文件
#   TestLogPath:        测试log文件
#   LogSavePath:        保存结果文件
#   
#   ExpectedLog always save as windows type.
#
def CompareOneCaseLog(ExpectedLogPath,TestLogPath,LogSavePath):
    fd = open(LogSavePath, 'w')

    #
    #   期待不存在或者内容为空，直接略过。
    #
    if not os.path.isfile(ExpectedLogPath) or (
        os.path.getsize(ExpectedLogPath) == 0 and
        os.path.getsize(TestLogPath) != 0
    ):
        fd.write('[Skip]')
        fd.close()
        return

    #
    #   测试的log如果不存在则表示RGT运行错误，需要查看。
    #
    if not os.path.isfile(TestLogPath) or not os.path.isfile(TestLogPath):
        fd.write('[Error]')
        fd.close()
        return

    ExpectedString = ReadFileString(ExpectedLogPath)
    TestLogString = ReadFileString(TestLogPath)

    #
    #   试图比较正确的log信息。
    #
    if ExpectedString == TestLogString:
        fd.write('[True]')
        fd.close()
        return

    #
    #   优先处理
    #
    if (
        BothContainSubStr(ExpectedString, TestLogString, 'Configuration Settings Report generated at') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Platform Inventory Report generated at') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Firmware Inventory Report generated at') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Flash Layout Report generated at')
       ):
        fd.write('[True#]')
        fd.close()
        return

    if (
        BothContainSubStr(ExpectedString, TestLogString, 'Configuration Settings Report') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Firmware Inventory Report') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Flash Layout Report') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Platform Inventory Report') or \
        BothContainSubStr(ExpectedString, TestLogString, 'Error: 1: The Report specified was not found.')
    ):
        fd.write('[True]')
        fd.close()
        return

    fd.write('[False]')
    fd.close()

#
#   查看CSV和log的比较结果。
#
def CheckCompareResult(CSVResultPath,LogResultPath):
    String1 = ReadFileString(CSVResultPath)

    if String1 == '':
        StringToReturn = '[True]'
    else:
        if String1 == 'Both no csv' or String1 == 'Expected no csv':
            StringToReturn = '[Skip]'
        elif String1 == 'Test no csv':
            StringToReturn = '[Error]'
        else:
            StringToReturn = '[Check]'

    return StringToReturn + '\t' + ReadFileString(LogResultPath)

#
#   1. 比较CSV文件
#   2. 比较Log文件
#   3. 检查比较结果
#
#   Param1 : 测试用例路径
#   Param2 : 期待目录路径
#   Param3 : 测试目录路径
#   Param4 : 期待log文件名
#   Param5 : 测试log文件名
#   Param6 : 保存对比csv结果路径
#   Param7 : 保存对比log结果路径
def CompareOneCase(ExpectedPath, TestPath, ExpLogFileName, TestLogFileName, CSVSavePath, LogSavePath):
    CompareOneCaseCSV(ExpectedPath, TestPath, CSVSavePath)
    CompareOneCaseLog(os.path.join(ExpectedPath,ExpLogFileName),
                      os.path.join(TestPath,TestLogFileName),
                      LogSavePath)
    print os.path.dirname(ExpectedPath) + '\t' + CheckCompareResult(CSVSavePath,LogSavePath)