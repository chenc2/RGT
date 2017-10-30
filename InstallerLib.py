# -*- coding: UTF-8 -*- 
import PDOLib
import CommonLib
import os
import time
import shutil
import subprocess
import platform
import xml.dom.minidom

InstallerConfigInfo = dict()

def InitializeInstallerLib():
    root = xml.dom.minidom.parse('IntelFirmwareEngine.xml').documentElement
    InstallerConfigInfo['InstallerDir'] = root.getElementsByTagName('InstallerDir')[0].firstChild.data
    if 'Linux' in platform.system():
        InstallerConfigInfo['PDOFileDir'] = root.getElementsByTagName('LinPDOFileDir')[0].firstChild.data
    else:
        InstallerConfigInfo['PDOFileDir'] = root.getElementsByTagName('WinPDOFileDir')[0].firstChild.data
    InstallerConfigInfo['InstallationInventory'] = root.getElementsByTagName('InstallationInventory')[0].firstChild.data
    InstallerConfigInfo['PlatformProjectInventory'] = root.getElementsByTagName('PlatformProjectInventory')[0].firstChild.data
    InstallerConfigInfo['RepositoryInventory'] = root.getElementsByTagName('RepositoryInventory')[0].firstChild.data
    InstallerConfigInfo['ToolsetInventory'] = root.getElementsByTagName('ToolsetInventory')[0].firstChild.data

def SetEnvVariable():
    if 'Linux' in platform.system():
        return

    import win32api
    import win32con

    Key = win32api.RegOpenKey(
            win32con.HKEY_LOCAL_MACHINE,
            "SYSTEM\\ControlSet001\\Control\\Session Manager\\Environment",
            0,
            win32con.KEY_ALL_ACCESS)

    Value = list(win32api.RegQueryValueEx(Key, 'Path'))[0]
    NewValue = []
    for path in Value.split(';'):
        if 'Intel(R) Firmware Engine' in path:
            pass
        else:
            NewValue.append(path)

    FilePath = os.path.join(InstallerConfigInfo['PDOFileDir'], InstallerConfigInfo['InstallationInventory'])
    SetValue = ';'.join(NewValue) + ';' + PDOLib.GetValueFromPDO(FilePath, 'ToolSet')
    win32api.RegSetValueEx(Key, 'Path', 0, win32con.REG_SZ, SetValue)
    win32api.RegCloseKey(Key)

#
#   检查PDO目录是否存在，并且检查4个.pdo文件是否存在。
#   该函数仅仅检查目录或文件是否存在，并不对.pdo文件内容进行检查。
#
def CheckWetherInstalled():
    if not os.path.isdir(InstallerConfigInfo.get('PDOFileDir')):
        return False
    else:
        for file in os.listdir(InstallerConfigInfo.get('PDOFileDir')):
            if InstallerConfigInfo.get(file[:-4]) == None:
                return False
    return True

#
#   读取当前系统安装的Installer版本号，需要确保已经安装。
#
def GetInstallerVersion():
    if CheckWetherInstalled:
        FilePath = os.path.join(InstallerConfigInfo.get('PDOFileDir'), InstallerConfigInfo.get('InstallationInventory'))
        return PDOLib.GetValueFromPDO(FilePath, 'ProductVersion')[-6:]
    else:
        return None

def WindowsInstaller():
    AuthCmd = 'AuthNetwork.exe %s' % InstallerConfigInfo.get('InstallerDir')
    try:
        os.system(AuthCmd)
    except Exception,e:
        print e

    #
    #   Try 30 times to access.
    #
    TryCount = 0
    while not os.path.isdir(InstallerConfigInfo.get('InstallerDir')):
        if TryCount == 30:
            return False

        print 'Access',InstallerConfigInfo.get('InstallerDir'),'fail, try again in 10 seconds.'
        time.sleep(10)
        TryCount = TryCount + 1
    
    #
    #   如果已经安装并且版本号相同，不重新安装Installer。
    #
    if CheckWetherInstalled():  
        if CommonLib.ReadFileList(os.path.join(InstallerConfigInfo.get('InstallerDir'), "Readme.txt"))[1] == GetInstallerVersion():
            print 'No updating today.'
            return False

    #
    #   Get installer name from share location.
    #
    InstallerName = ''
    for file in os.listdir(InstallerConfigInfo.get('InstallerDir')):
        if file.find('IntelFirmwareEngineSetup') != -1:
            InstallerName = file
            break
    if InstallerName == '':
        print 'Not found installer.'
        assert(False)

    #
    #   Download isntaller.
    #
    if os.path.isfile(InstallerName):
        os.remove(InstallerName)
    shutil.copy(os.path.join(InstallerConfigInfo.get('InstallerDir'), InstallerName), os.getcwd())

    #
    #   Delete older installer.
    #
    ListPath = [
        r'C:\Users\Public\Intel\Intel(R) Firmware Engine',
        r'C:\Users\Public\Repository',
        r'C:\Program Files (x86)\Intel\Intel(R) Firmware Engine'
    ]
    for Folder in ListPath:
        if os.path.exists(Folder):
            try:
                shutil.rmtree(Folder)
            except Exception, e:
                print e

    #
    #   Install isntaller.
    #
    Ret = subprocess.Popen('%s -i silent' % InstallerName, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    Ret.communicate()
    os.remove(InstallerName)