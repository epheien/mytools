#!/usr/bin/env python
# -*- coding:utf-8 -*-

# ver.1.0 2012-04-03

import os
import re
import shutil
import sys

reFile = re.compile(r"""call delete\('([^']+?)'\)""")

def GetVBARecordLine(sFile, sName):
    """从 Record 文件中查找包名为 sName 的 Record 行"""
    s = "(%s)" % sName
    reFind = re.compile(s + r"""(?:-[a-zA-Z0-9.-]*)?\.vba:""")
    with open(sFile, "rb") as f:
        for sLine in f:
            #if sLine.startswith(sName):
                #return sLine
            m = reFind.match(sLine)
            if m:
                #print m.group(1)
                return sLine

    return ""

def GetFilesFromLine(sLine):
    """从 .VimballRecord 行获取所有的文件
    返回：文件列表"""
    global reFile
    return reFile.findall(sLine)

def DumpVBA(sFile, sName, nIgnLevel, sOutDir):
    if nIgnLevel < 0:
        nIgnLevel = 0

    if not sOutDir:
        sOutDir = os.getcwd()

    if not os.path.exists(sOutDir):
        os.makedirs(sOutDir)

    oldwd = os.getcwd()
    os.chdir(sOutDir)

    sLine = GetVBARecordLine(sFile, sName)
    if sLine:
        lFiles = GetFilesFromLine(sLine)
        for sOrigFile in lFiles:
            sFile = os.path.normpath(os.path.abspath(sOrigFile))
            sFile = os.sep.join((sFile.split(os.sep)[nIgnLevel:]))
            sDir = os.path.dirname(sFile)
            if sDir and not os.path.exists(sDir):
                os.makedirs(sDir)
            shutil.copy(sOrigFile, sFile)
            print '"%s" -> "%s"' % (sOrigFile, os.path.abspath(sFile))
    else:
        print >> sys.stderr, "package \"%s\" not found" % (sName, )

    os.chdir(oldwd)


def main():
    if len(sys.argv[1:]) < 2:
        print "usage: %s {package name} {out directory}" % (sys.argv[0], )
        return 1

    sFile = os.path.expanduser("~/.vim/.VimballRecord")
    sPack = sys.argv[1]
    sOutDir = sys.argv[2]
    DumpVBA(sFile, sPack, 4, sOutDir)

    return 0


if __name__ == "__main__":
    #print '\n'.join(GetFilesFromLine("""mark.vba: call delete('/home/eph/.vim/autoload/mark.vim')|call delete('/home/eph/.vim/plugin/mark.vim')|call delete('/home/eph/.vim/doc/mark.txt')"""))
    #print test(, "mark", 4, "testtt")
    main()

