from cf import cifa

'''
KEY  保留字
SYM  特殊符号
ID   标识符
NUM  数字常量
STR  字符串常量
'''
flagError = 0
yfResult = ''

yfTypes = [
    ['KEY', 'SYM'],
    # 可赋值
    [
        'ID',
        # 常量
        ['STR', 'NUM']
    ]
]
KEY = [
    # 赋值
    ['int', 'float', 'double', 'char', 'void'],
    # 逻辑
    ['if', 'for', 'while', 'do', 'else']
]
SYM = [
    # 运算符
    ['=', '&', '<', '>', '++', '--', '+', '-', '*', '/', '>=', '<=', '!='],
    # 分隔符
    ['(', ')', '{', '}', '[', ']', '\"'],
    [',', ';']
]


def appendResult(wordLocate):
    global yfResult
    yfResult += result[wordLocate][1]
    print(wordLocate,yfResult)


def expression(wordLocate, zjList):
    # 表达式
    while result[wordLocate][1] not in zjList:
        # 常量
        if result[wordLocate][0] in yfTypes[1][1]:
            print('常量:%s' % result[wordLocate][1])
        # 变量或者数组的某元素
        elif result[wordLocate][0] == 'ID':
            # 变量
            if result[wordLocate + 1][1] in SYM[0] or result[wordLocate + 1][1] in SYM[2]:
                print('变量:%s' % result[wordLocate][1])
            # 数组的某一个元素ID[i]
            elif result[wordLocate + 1][0] == 'SYMLeftBracket':
                print('数组：%s' % result[wordLocate][0])
                wordLocate += 2
                if result[wordLocate][0] not in SYM[1][1] or result[wordLocate][0] != 'ID':
                    print('error: 数组下表必须为常量或标识符')
                    print(result[wordLocate][1])
                    break
                else:
                    pass
        # 运算符
        elif result[wordLocate][1] in SYM[0] and result[wordLocate+1][1] in SYM[0]:
            doubleOper = result[wordLocate][1]+result[wordLocate+1][1]
            if doubleOper in SYM[0]:
                appendResult(wordLocate)
                print('双目运算符:%s' % (doubleOper))
            else:
                print('非法双目运算符:%s' % (doubleOper))
            wordLocate += 1
        elif result[wordLocate][1] in SYM[0]:
            print('单目运算符:%s' % result[wordLocate][1])
        appendResult(wordLocate)
        wordLocate += 1
    return wordLocate


def assignment(wordLocate):
    # 赋值语句
    while result[wordLocate][1] not in SYM[2]:
        appendResult(wordLocate)
        if result[wordLocate][0] == 'ID' or result[wordLocate][0] in yfTypes[1][1]:
            print('被赋值的变量:%s' % result[wordLocate][1])
        elif result[wordLocate][1] == '=':
            wordLocate += 1
            return expression(wordLocate, SYM[2])
        wordLocate += 1


def isWhile(wordLocate):
    wordLocate += 1
    appendResult(wordLocate)
    if result[wordLocate][0] == 'SYMLeftCurves':
        tmpwordLocate = wordLocate
        while result[tmpwordLocate][0] != 'SYMRightCurves':
            tmpwordLocate += 1
            tmpwordLocate = expression(tmpwordLocate, [')'])
            appendResult(tmpwordLocate)
        return tmpwordLocate+1
    if result[wordLocate][0] == 'SYMLeftBrace':
        block(wordLocate)
        return


def isIfElse(wordLocate):
    # if标志
    if result[wordLocate][1] == 'if':
        wordLocate += 1
        appendResult(wordLocate)
        # 左小括号
        if result[wordLocate][0] == 'SYMLeftCurves':
            # 右小括号位置
            tmpwordLocate = wordLocate
            while result[tmpwordLocate][0] != 'SYMRightCurves':
                tmpwordLocate += 1
                tmpwordLocate = expression(tmpwordLocate, [')'])
                appendResult(tmpwordLocate)
            return tmpwordLocate+1
        else:
            print('error: lack of left bracket!')
            exit()

        # 左大括号
        if result[wordLocate][0] == 'SYMLeftBrace':
            block(wordLocate)
            return

    # 如果是else关键字
    if result[wordLocate][1] == 'else':
        wordLocate += 1
        # 左大括号
        appendResult(wordLocate)
        if result[wordLocate][0] == 'SYMLeftBrace':
            block(wordLocate)
            return


def control(tokenValue, wordLocate):
    appendResult(wordLocate)
    if tokenValue == 'while' or tokenValue == 'do':
        print("while语句")
        wordLocate = isWhile(wordLocate)
    elif tokenValue == 'if' or tokenValue == 'else':
        print("if else语句")
        wordLocate = isIfElse(wordLocate)
    else:
        print('控制关键字识别错误!')
        exit()
    return wordLocate


def tokenTypeFun(resultWord, wordLocate):
    tokenType = resultWord[0]
    tokenValue = resultWord[1]
    if tokenValue in KEY[1]:
        return control(tokenValue, wordLocate)
    elif tokenType in yfTypes[1][1] or tokenType == 'ID':
        wordLocate_1_token_type = result[wordLocate + 1][1]
        if wordLocate_1_token_type == '=':
            print("赋值语句")
            return assignment(wordLocate)
        else:
            return 'ERROR'
    # 右大括号，表明函数的结束
    elif tokenType == 'SYMRightBrace':
        appendResult(wordLocate)
        if wordLocate == len(result)-1:
            return wordLocate
        else:
            return 'SYMRightBrace'
    else:
        return 'ERROR'


def block(braceLocate):
    global result
    wordLocate = braceLocate+1
    while 1:
        tokenTypeR = tokenTypeFun(result[wordLocate], wordLocate)
        if isinstance(tokenTypeR, int):
            wordLocate = tokenTypeR
            if result[wordLocate][0] == 'SYMRightBrace':
                print('分析结束')
                exit()
            appendResult(tokenTypeR)
        wordLocate += 1


def yf():
    resultWord = [word[1] for word in result]
    braceLocate = resultWord.index('{')
    appendResult(braceLocate)
    block(braceLocate)

def main(fileName):
    global result
    cfResult = cifa(fileName)
    result = [cfWord.split(':') for cfWords in cfResult.values()
              for cfWord in cfWords]
    print("=========================")
    yf()


if __name__ == '__main__':
    main('1.txt')
