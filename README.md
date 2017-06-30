# OC-RGT
Automation test tool for RGT.

RGT User Guide:
1. Install Intel Firmware Engine by default settings.
2. To configure 'Config.xml' file.
3. Add the path of RGT tool into environment variable.
4. Check the path of test command in cmd.txt file.
5. Run.

Notes:
1. Intel Firmware Engine default settings:
  Windows, PDO file path is "C:\Program Files (x86)\Intel\Intel(R) Firmware Engine\etc"
  Linux,   PDO file path is "/opt/Intel/Intel(R) Firmware Engine/etc"
  Please check whether the path is correct before run RGT tool.
  
2. How to configure .xml by manual:
  If suppose your OS is Windows*, you should modify the follow section.
  <Win-TestCaseRoot>: The root path of all test case.
  <Win-BimFilePath> : A directory named "BIMFiles" of <Win-TestCaseRoot>.
  <Win-PDOFilePath> : This section should always be "C:\Program Files (x86)\Intel\Intel(R) Firmware Engine\etc"
  
3. Set environment variable:
  Windows ToolSet Path: C:\Program Files (x86)\Intel\Intel(R) Firmware Engine\<version number>\Bin\Win32
  Linux   ToolSet Path: "/opt/Intel/Intel(R) Firmware Engine/<version number>/Bin"
  If your OS is Linux, add [alias sudo='sudo env PATH="$PATH"'] in .bash_profile and type "source ~/.bash_profile" to update.

4. Check the path of test command.
  There are some test command involved output path, Maybe the output path is an invalid path in your environment.
  So we need to replace the invalid path. First, you need to check what is the output path. For example "Conf\FirmwareReport\TCS180", 
  the output path is "C:\Users\chenche4\Desktop\RGT Test Case\Conf\FirmwareReport\TCS180\TestResult\FirmwareReport.csv".
  So the path is "C:\Users\chenche4\Desktop\RGT Test Case", you should save this path in the CaseRoot.txt file, this file is
  under the root path of test case.
  
5. Run
  Windows: Use command line and change directory to OC-RGT, type "Run.bat"
  Linux  : change directory to OC-RGT, type "sudo python Main.py"
  
