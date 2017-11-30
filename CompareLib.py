# -*- coding: utf-8 -*-
import os
import CSVLib
import shutil
import re
import CommonLib
import RGTCompareLib
import ExpectionList
from ConfigLib import ConfigInfo

#
#	1. 确保路径合法且正确。
#   2. 确保两个.csv文件格式正确。
#   3. 确保两个.csv文件类型一样。
#
def DoCompareCSV(FilePath1,FilePath2,ResultFilePath):
    if not os.path.isfile(FilePath1) or not os.path.isfile(FilePath2):
        print 'The path of .csv file is invalid!'
        assert(False)

    CSVType1 = CSVLib.GetCSVType(FilePath1)
    CSVType2 = CSVLib.GetCSVType(FilePath2)

    if CSVType1 != CSVType2:
        print FilePath1,'Type of .csv files are not same!'
        assert(False)

    ParseFuncMap = {
        'Platform Inventory'    :   CSVLib.ParsePlatformInventoryCSV,
        'GPIO Table'            :   CSVLib.ParseGPIOTableCSV,
        'Firmware Inventory'    :   CSVLib.ParseFirmwareInventoryCSV,
        'Configuration Settings':   CSVLib.ParseConfSettingCSV,
        'Flash Offset Layout'   :   CSVLib.ParseFlashLayoutCSV
    }

    #
    #   解析函数返回的是一个List类型，并且包含2个元素。
    #   每个元素都是dict类型的数据，并且是key-value的形式。
    #   比较时就是比较相同key对应的value是否相等。
    #
    Content1 = ParseFuncMap.get(CSVType1)(FilePath1)
    Content2 = ParseFuncMap.get(CSVType2)(FilePath2)

    Triple = CompareUniqueKeyDict(Content1[0],Content2[0])
    String = CompareMultipleKeyDict(Content1[1],Content2[1])

    SaveResultToFile(Triple,String,ResultFilePath)

'''
    Each dict type data has the unique key name.
    Return triple list, each field means as follow:
    1. The key name just in the Dict1, not exists in the Dict2.
    2. The key name just in the Dict2, not exists in the Dict1.
    3. The key name both in the Dict1 and Dict2, but the value of key is different.
'''
def CompareUniqueKeyDict(Dict1,Dict2):
    Keys1 = set(Dict1.keys())
    Keys2 = set(Dict2.keys())
    assert (len(Keys1) == len(Dict1))
    assert (len(Keys2) == len(Dict2))

    CompareResultString = str()
    for TheCommonKey in Keys1 & Keys2:
        Buffer1 = list(Dict1.get(TheCommonKey).split(','))
        Buffer2 = list(Dict2.get(TheCommonKey).split(','))

        if len(Buffer1) != len(Buffer2):
            CompareResultString = CompareResultString + '[' + TheCommonKey + ']' + \
                                  ' The count of field is different!\n'
        else:
            First = True
            HasDiff = False
            for index in range(0,len(Buffer1)):
                if Buffer1[index] == Buffer2[index]:
                    continue

                #
                #   The following code are the flexible code.
                #   You can according to the actual demand to change the comparing algorithm.
                #

                #
                #   Flexible code 1.
                #
                pattern = re.compile("0x.* (.*KB)")
                if pattern.match(Buffer1[index]) != None and pattern.match(Buffer2[index]) != None:
                    continue

                #
                #   Flexible code 2.
                #
                pattern = re.compile("0x[0-9a-fA-F]{8}")
                if pattern.match(Buffer1[index]) != None and pattern.match(Buffer2[index]) != None:
                    continue

                #
                #   Flexible code 3.
                #
                pattern = re.compile(".*FD_FIRMWAREIMAGE\.fd")
                if pattern.match(Buffer1[index]) != None and pattern.match(Buffer2[index]) != None:
                    continue
                #
                #	Flexbile code 4.
                #	Buffer1 is expected result, Buffer2 is test result.
                #	"0x80000047L" != "0x80000047"
                #
                pattern1 = re.compile('"0x[0-9a-fA-F]{8}L"')
                pattern2 = re.compile('"0x[0-9a-fA-F]{8}"')
                if pattern1.match(Buffer1[index]) != None and pattern2.match(Buffer2[index]) != None:
                    continue

                #
                #   Flexibility code ending.
                #
                if  Buffer1[index] == '"Specify the LPSS & SCC Devices Mode.<BR><BR>' and \
                    Buffer2[index] == '"Specify the LPSS & SCC Devices Mode.<BR><BR> 0: ACPI Mode<BR> 1: PCI Mode<BR>"':
                    continue

                HasDiff = True
                if First:
                    CompareResultString = CompareResultString + '[' + TheCommonKey + '] ' + \
                                          Buffer1[index] + ' != ' + Buffer2[index]
                    First = False
                else:
                    CompareResultString = CompareResultString + ' ' + \
                                          Buffer1[index] + ' != ' + Buffer2[index]
            if HasDiff:
                CompareResultString = CompareResultString + '\n'


    return [Keys1 - Keys2, Keys2 - Keys1, CompareResultString]

def CompareMultipleKeyDict(Dict1,Dict2):
    Keys1 = set(Dict1.keys())
    Keys2 = set(Dict2.keys())
    assert (len(Keys1) == len(Dict1))
    assert (len(Keys2) == len(Dict2))


    DiffCmpString = ''
    for item in Keys1 & Keys2:
        BufferList1 = Dict1.get(item)
        BufferList2 = Dict2.get(item)

        if len(BufferList1) != len(BufferList2):
            DiffCmpString = DiffCmpString + '[' + item + ']' + \
                            ' (Multi) The count of field is different!\n'
        else:
            DiffCmpString = DiffCmpString + CompareTwoList(item, BufferList1, BufferList2)

    return DiffCmpString

'''
    Compare the list, for example:
    List1: 123 124 132 446
    List2: 123 146 446 234
    
    After the first for loop, the result as follow:
    List1: 124 132
    List2: 146 234
    
    The result as follow:
    [KeyName]
        File1: 124 132
        File2: 146 234
'''
def CompareTwoList(KeyName, List1, List2):
    for item in List1 + List2:
        if item in List1 and item in List2:
            List1.remove(item)
            List2.remove(item)

    RetString = str()
    if len(List1) != 0 or len(List2) != 0:
        RetString = '[' + KeyName + ']\n'

    if len(List1) != 0:
        RetString = RetString + '\tFile1:'
        for item in List1:
            RetString = RetString + ' ' + item
        RetString = RetString + '\n'

    if len(List2) != 0:
        RetString = RetString + '\tFile2:'
        for item in List2:
            RetString = RetString + ' ' + item
        RetString = RetString + '\n'

    return RetString

def SaveResultToFile(Triple, String, FilePath):
    fd = open(FilePath, 'w')
    if len(Triple[0]) != 0:
        fd.write('#########################################Just in the Expected#########################################\n')
        for item in Triple[0]:
            fd.write(item+'\n')

    if len(Triple[1]) != 0:
        fd.write('#########################################Just in the TestResult#######################################\n')
        for item in Triple[1]:
            fd.write(item + '\n')

    if len(Triple[2]) != 0:
        fd.write('#########################################Different Value#########################################\n')
        fd.write(Triple[2])

    if len(String) != 0:
        fd.write('#########################################Multi Information#########################################\n')
        fd.write(String)
    fd.close()

def Compare():
    ExceptionContentList = []
    if os.path.isdir(ConfigInfo['ExceptionDir']):
        ExceptionContentList = ExpectionList.ReadExpectionContent(ConfigInfo['ExceptionDir'])

    Result = []
    for parent, dirs, files in os.walk(ConfigInfo['TestCaseDir']):
        if ConfigInfo['CmdFileName'] in files:
            CommonLib.CreateDir(os.path.join(parent, ConfigInfo['CompDirName']))

            L = RGTCompareLib.CompareOneCase(
                  os.path.join(parent, ConfigInfo['ExpectedDirName']),
                  os.path.join(parent, ConfigInfo['TestDirName']),
                  ConfigInfo['ExpectedLogName'],
                  ConfigInfo['TestLogName'],
                  os.path.join(parent,ConfigInfo['CompDirName'],ConfigInfo['CompCSVName']),
                  os.path.join(parent,ConfigInfo['CompDirName'],ConfigInfo['CompLogName']),
                  ExceptionContentList
                )
            Result.append(L)

    return Result