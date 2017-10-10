# -*- coding: UTF-8 -*-
import os
import CommonLib
import platform

#
#   在某个文件夹下读取过滤信息，是经过人工检查的。
#
def ReadExpectionContent(Directory):
    if not os.path.isdir(Directory):
        print Directory,"is an invalid directory path."
        assert(False)

    ExpectionContentList = []
    for file in os.listdir(Directory):
        String = CommonLib.ReadFile(os.path.join(Directory, file))
        if 'Linux' in platform.system():
            String = String.replace('\\' ,'/')
        ExpectionContentList.append(String)
    return ExpectionContentList