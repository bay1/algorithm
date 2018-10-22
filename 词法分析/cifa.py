# -*- coding: utf-8 -*-
"""
（1）按规则拼单词,并转换成二元式形式
（2）删除注释行
（3）删除空白符 (空格、回车符、制表符)
（4）显示源程序，在每行的前面加上行号，并且打印出每行包含的记号的二元形式
（5）发现并定位错误。
"""
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))

statue = 0

includedWord = ''
includeNote = ''

includeNoteList = []
includedErrorList = []
resultList = {}

KEY = ['if', 'then', 'else', 'end', 'repeat', 'until', 'read', 'write']
SYM = ['+', '-', '*', '/', '=', '<', '{', '}', ';']

"""
KEY  保留字
SYM  特殊符号
ID   标识符
NUM  数字常量
STR  字符串常量
BLANK 空白字符

1  if	   2 +
3  then	   4 -
5  else	   6 *
7  end	   8 /
9  repeat 10 =
11 until  12 <
13 read	  14 {
15 write  16 }
17 ;
"""


def readFile(fileName):
    '''
    读取文本内容返回生成器
    '''
    return (file.replace('\n', ' ')for file in open(basedir + '/' + fileName))


def outer(func):
    '''
    装饰主函数，打印文件内容
    '''
    def printFile(*args, **kwargs):
        num = 0
        contents = readFile('1.txt')
        for content in contents:
            print("第%s行:%s" % (num, content))
            num += 1
        return func(*args, **kwargs)
    return printFile


def appendWord(lineNum, appendWords):
    global resultList
    resultList[lineNum].append(appendWords)


def delLess(file, wordList):
    '''
    删除空白符 (空格、回车符、制表符)和注释行
    '''
    for word in wordList:
        file = file.replace(word, "").replace("\t", "").strip()
    return file


def printIndexWord(lineNum):
    '''
    输出识别的字符并重置includeWord
    '''
    global includedWord
    if includedWord.isdigit():
        appendWord(lineNum, "NUM:"+includedWord)
    elif includedWord.isalpha():
        if includedWord in KEY:
            appendWord(lineNum, "KEY:"+includedWord)
        else:
            appendWord(lineNum, "STR:"+includedWord)
    elif includedWord.isalnum():
        appendWord(lineNum, "ID:"+includedWord)
    includedWord = ''


def checkNote(word):
    global includeNote
    if statue == 1:
        includeNote += word


def checkType(word, lineNum):
    '''
    类别判断
    '''
    global includedWord, includedErrorList
    checkNote(word)
    if word.isdigit():
        # 如果是数字
        includedWord += word
    elif word.isalpha():
        # 如果是字母

        includedWord += word
    elif word.isspace():
        # 如果是空白符

        printIndexWord(lineNum)
        # print('空白符', word)
    elif word in SYM:
        # 如果是语言内的特殊符号

        printIndexWord(lineNum)
        appendWord(lineNum, 'SYM:'+word)
    else:
        includedErrorList.append(word)

        printIndexWord(lineNum)
        print('\033[1;31m 第%s行含有非法字符:%s \033[0m' % (lineNum, word))


def getToken(content, lineNum):
    '''
    按规则拼单词,并转换成二元式形式
    '''
    global statue, includeNote, includeNoteList

    for word in content:
        if word == '{' and statue == 0:
            statue = 1
        elif word == '}' and statue == 1:
            statue = 0
            includeNoteList.append(includeNote + word)
            includeNote = ''
        elif statue == 0:
            pass
        checkType(word, lineNum)


@outer
def main():
    global resultList
    lineNum = 0
    contents = readFile('1.txt')
    while 1:
        try:
            resultList[lineNum] = []
            getToken(contents.__next__(), lineNum)
            lineNum += 1
        except StopIteration as e:
            break
    print(json.dumps(resultList, indent=4))
    print('注释语句：\033[1;33;44m %s \033[0m' % includeNoteList)
    print('非法语句：\033[1;33;44m %s \033[0m' % includedErrorList)
    contents = ''
    for content in open(basedir + '/'+'1.txt'):
        contents += content.replace('\n', ' ')
    contents = delLess(contents, includeNoteList)
    contents = delLess(contents, includedErrorList)
    print('删除注释与非法语句之后：\033[1;33;44m%s\033[0m' % contents)
    newWord = open(basedir + '/' + '1_new.txt', 'w')
    newWord.write(contents)
    newWord.close()


if __name__ == '__main__':
    main()
