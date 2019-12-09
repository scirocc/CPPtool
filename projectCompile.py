import sys
import os
import win32api
import win32con
import glob
import time
# print(123)
#
sSrcFile = []
sLIB = []
sDLL = []
sInclude = []
slibFolder = []
sIncludefolder = []


def findAllSrcFile(ab_dir):  # src目录下的所有文件及其子目录内的文件
    sSrc = glob.glob(ab_dir)
    if not sSrc:
        return 0
    for file in sSrc:
        if os.path.isfile(file) and (('.c' in file) or ('.cpp' in file)) and 'pyc' not in file:
            sSrcFile.append(file)
        elif os.path.isdir(file):  # 这时候需要继续迭代
            path = file + '/*'
            findAllSrcFile(path)


def findALLLibFile(ab_dir):
    sLib = glob.glob(ab_dir)
    if not sLib:
        return 0
    for file in sLib:
        if os.path.isfile(file) and '.lib' in file:
            sLIB.append(file)
            slibFolder.append(os.path.split(file)[0])
        elif os.path.isdir(file):  # 这时候需要继续迭代
            slibFolder.append(file)
            path = file + '/*'
            findALLLibFile(path)


def findALLDllFile(ab_dir):
    sDll = glob.glob(ab_dir)
    if not sDll:
        return 0
    for file in sDll:
        if os.path.isfile(file) and '.dll' in file:
            sDLL.append(file)
        elif os.path.isdir(file):  # 这时候需要继续迭代
            path = file + '/*'
            findALLDllFile(path)


def findALLIncludeFile(ab_dir):
    sinclude_ = glob.glob(ab_dir)
    if not sinclude_:
        return 0
    for file in sinclude_:
        if os.path.isfile(file) and (('.h' in file) or ('.c' in file) or ('.hpp' in file)):
            sInclude.append(file)
            sIncludefolder.append(os.path.split(file)[0])
        elif os.path.isdir(file):  # 这时候需要继续迭代
            sIncludefolder.append(file)
            path = file + '/*'
            findALLIncludeFile(path)


def WriteMake():
    s = sys.argv
    x, projectFiledir, filedir = s
    projectName = projectFiledir[projectFiledir.rfind('\\') + 1:]
    # 找出项目绝对路径
    ab_dir = s[1]
    print('项目绝对路径:', ab_dir)
    findAllSrcFile(ab_dir + '/src/*')
    findAllSrcFile(ab_dir + '/MyTool/src/*')
    findALLLibFile(ab_dir + '/bin/*')
    findALLDllFile(ab_dir + '/bin/*')
    findALLIncludeFile(ab_dir + '/include/*')
    findALLIncludeFile(ab_dir + '/MyTool/include/*')

    findALLLibFile('E:/frequentlyUsedCPPLibrary/bin/*')
    findALLDllFile('E:/frequentlyUsedCPPLibrary/bin/*')
    findALLIncludeFile('E:/frequentlyUsedCPPLibrary/include/*')
    print('项目源文件集合:', sSrcFile)
    print('项目动态库文件集合:', sDLL)
    print('项目静态库文件集合:', sLIB)
    print('项目头文件夹集合:', sInclude)
    print('项目库文件夹集合:', slibFolder)
    print('项目头文件夹集合:', sIncludefolder)
    str_ = 'add_executable({}\n'.format(projectName)
    for srcFile in set(sSrcFile):
        srcFile = srcFile.replace('\\', '/')
        str_ += srcFile + '\n'
    for header in set(sInclude):
        header = header.replace('\\', '/')
        str_ += header + '\n'
    str_ += 'D:/ProgramData/Anaconda3/include/Python.h' + '\n'
    str_ += ')\n'
    str_.replace('i', 'iiiiiiiiiiii')
    with open(ab_dir + '/CMakeLists.txt', 'w')as f:
        f.write('cmake_minimum_required(VERSION 3.14)\n')
        f.write('project({})\n'.format(projectName))
        f.write('set(CMAKE_CXX_STANDARD 17)\n')
        f.write('set(CMAKE_EXE_LINKER_FLAGS "-static-libgcc -static-libstdc++")\n')
        f.write('include_directories(include)\n')
        f.write(
            'include_directories(D:/ProgramData/Anaconda3/include)\n')  # 还要把python的inlcude文件夹添加进来，因为有可能和python交互，用到python.h
        for dir in set(sIncludefolder):
            dir = dir.replace('\\', '/')
            f.write('include_directories({})\n'.format(dir))
        f.write('link_directories(bin)\n')
        f.write(
            'link_directories(D:/ProgramData/Anaconda3/libs)\n')  # 还要把python的inlcude文件夹添加进来，因为有可能和python交互，用到python36.lib
        for dir in set(slibFolder):
            dir = dir.replace('\\', '/')
            f.write('include_directories({})\n'.format(dir))
        f.write(str_)  # add_executable信息
        str1_ = 'TARGET_LINK_LIBRARIES({}'.format(projectName) + ' \n'
        for lib in set(sLIB):
            lib = lib.replace('\\', '/')
            str1_ += lib + '\n'
        str1_ += 'python36.lib' + '\n'  # 添加这个东西
        str1_ += 'imagehlp.lib' + '\n'  # 添加这个东西
        str1_ += ')\n'
        f.write('{}'.format(str1_))
        str1_ = 'TARGET_LINK_LIBRARIES({}'.format(projectName) + ' \n'
        for dll in set(sDLL):
            dll = dll.replace('\\', '/')
            str1_ += dll + '\n'
        str1_ += ')\n'
        f.write('{}'.format(str1_))


# readMake()

def getRidOfTextBetweenDoubleQuote(str_):
    sign_counter = 0
    endloc = 0
    sign = '\"'
    needRecursiveMark=False
    for index, i in enumerate(str_):
        if i == sign and str_[index-1]!='\\':
            sign_counter += 1
            needRecursiveMark=True
            if sign_counter == 1:
                startloc = index
            elif sign_counter>1 and sign_counter%2==0:
                endloc=index
                break
    if needRecursiveMark:
        str_ = str_.replace(str_[startloc:endloc + 1], '')
        str_=getRidOfTextBetweenDoubleQuote(str_)
    return (str_)

def getRidOfTextBetweenSingleQuote(str_):
    sign_counter = 0
    endloc = 0
    sign = '\''
    needRecursiveMark=False
    for index, i in enumerate(str_):
        if i == sign and str_[index-1]!='\\':
            sign_counter += 1
            needRecursiveMark=True
            if sign_counter == 1:
                startloc = index
            elif sign_counter>1 and sign_counter%2==0:
                endloc=index
                break
    if needRecursiveMark:
        str_ = str_.replace(str_[startloc:endloc + 1], '')
        str_=getRidOfTextBetweenDoubleQuote(str_)
    return (str_)



def getIndexOfCorreBrace(str_,startloc):#查找对应右括号的位置
    left_sign_counter = 0
    right_sign_counter = 0
    endloc = 0
    left_sign = '{'
    right_sign = '}'
    for index, i in enumerate(str_):
        if index >=startloc:
            if i == left_sign :
                left_sign_counter += 1
                if left_sign_counter == 1:
                    startloc = index
            elif i == right_sign:
                right_sign_counter += 1
                if left_sign_counter == right_sign_counter:
                    endloc = index
                    break
    return(endloc)


def dealData(str_):#去掉{}当中的内容
    sData=str_.split('\n')
    indexInStr_ = -2
    recursiveMark=False
    lastline=''
    for line in sData:
        indexInStr_ += len(line) + 1
        #1 同一行包括'namespace'或'class'且包括'{' 这样括号间的内容不可删除
        #2 本行虽然没有'namespace'或'class'，且本行包括'{'，但上一行包括'namespace'或'class',且上一行不含'{' 这样括号间的内容不可删除
        condition1=(('namespace' in line) or('class' in line))and ('{' in line)
        condition2=((('namespace' not in line) and('class' not in line))and('{' in line)and(('namespace' in lastline)or('class' in lastline))and('{' not in lastline))
        if condition1 or condition2:#不可删除，看下一行
            pass
        else:
            recursiveMark=True
            indexOfleftBrace = line.find('{')
            if indexOfleftBrace!=-1:#找到了，那么就可以删除
                index_=indexInStr_-(len(line)-indexOfleftBrace)+1
                endloc=getIndexOfCorreBrace(str_,index_)
                str_=str_.replace(str_[index_:endloc+1],'')
                if recursiveMark == True: str_=dealData(str_)
                break
        lastline=line
    return(str_)



def gen_str_to_write_in_headerfile(sourceFilePath):
    with open(sourceFilePath, 'r', encoding='utf-8')as f:
        datas = f.readlines()
    sData = [line for line in datas if '#include' not in line]
    sInclude_str=[line for line in datas if '#include' in line]
    str_ = "".join(sData)
    str_=getRidOfTextBetweenDoubleQuote(str_)
    str_=getRidOfTextBetweenSingleQuote(str_).strip()
    str_=dealData(str_)
    str_include="".join(sInclude_str)+'\n'
    str_=str_include+str_
    return (str_)

def finalAdjustContent(content):
    sline=content.split('\n')
    sTemp=[]
    templateMark=False
    for line in sline:
        if line.strip():
            if (line[0]!='#')and('class' not in line)and('template' not in line)and('namespace' not in line)and(line.strip()[-1]==')'):
                line=line+';'
            if('template' in line)and(line.index('template')<line.index('//')):#模板关键字并不在注释中
                templateMark=True
        sTemp.append(line)
    return('\n'.join(sTemp),templateMark)

def reWriteThisCPPFile(sourceFilePath):
    with open(sourceFilePath, 'r', encoding='utf-8')as f:
        datas = f.readlines()
    sData = [line for line in datas if '#include' not in line]
    sInclude_str = [line for line in datas if '#include' in line]
    print(sourceFilePath.split('\\'))
    headerName=sourceFilePath.split('\\')[-1].replace('.cpp','.h')
    str_='#include"{}"\n'.format(headerName)
    str_=str_+"".join(sData)
    with open(sourceFilePath, 'w', encoding='utf-8')as f:
        f.write(str_)


def autoReplenishFile():
    s = sys.argv
    projectDir = s[1]
    projectName = projectDir.split('\\')[-1]
    # 检查所有源文件是否有对应的头文件
    for file in sSrcFile:
        if 'main.cpp' not in file:
            corresponding_header = file.replace('src', 'include').replace('.cpp', '.h')
            sfolder = corresponding_header.split('\\')
            s = []
            for folder in sfolder:
                s.extend(folder.split('/'))
            if not os.path.isfile(corresponding_header):  # 没有这些文件，应该新建
                try:os.makedirs(corresponding_header[:corresponding_header.rfind('\\')])
                except:pass
                fileName = corresponding_header.split('\\')[-1].replace('.h', '')
                sFolder = s
                sFolder = sFolder[sFolder.index(projectName):-1]
                print('sFolder:', sFolder)
                content=gen_str_to_write_in_headerfile(file)
                content,templateMark=finalAdjustContent(content)
                with open(corresponding_header, 'w')as f:
                    str_ = '#ifndef '
                    for folder in sFolder:
                        str_ += folder.upper() + '_'
                    str_ += fileName.upper()
                    str_ += '_H\n'
                    f.write(str_)

                    str_ = '#define '
                    for folder in sFolder:
                        str_ += folder.upper() + '_'
                    str_ += fileName.upper()
                    str_ += '_H\n'
                    f.write(str_)

                    f.write(content)
                    if templateMark:
                        str_='\n#include'+"\"{}.cpp\"\n".format(fileName)
                        f.write(str_)

                    str_ = '\n#endif'
                    f.write(str_)
                reWriteThisCPPFile(file)#改头


def pushShutcut():
    time.sleep(1)
    win32api.keybd_event(16, 0, 0, 0)  # shift
    win32api.keybd_event(121, 0, 0, 0)  # f10
    time.sleep(0.1)
    win32api.keybd_event(16, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(121, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键

def main():
    s = sys.argv
    projectDir = s[1]
    try:os.makedirs(projectDir+'/bin/')
    except:pass
    try:os.makedirs(projectDir+'/src/')
    except:pass
    try:os.makedirs(projectDir+'/include/')
    except:pass
    try:os.makedirs(projectDir+'/MyTool/include/')
    except:pass
    try:os.makedirs(projectDir+'/MyTool/src/')
    except:pass
    WriteMake()
    autoReplenishFile()
    WriteMake()
    # pushShutcut()
    return 0

main()
# gen_str_to_write_in_headerfile('E:\CLionProjects\MultiFactor\src\getData/getTradebleShare.cpp')

