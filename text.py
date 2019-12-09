
str_='fhdjksfkl//ds;\\\"\ndsha5kjds\"fhjdk\"dsgahj\"\nasd\"'
print(str_)

def findEffectiveLocOfSign(sign,str_,startLoc):

    loc=str_.find(sign,startLoc)
    if loc==-1:
        return -1
    unEffectiveCase1=(str_[loc-1]=='\\')
    locOfPreLinefeed=str_.rfind('\n',0,loc)#最近的换行符位置
    locOfPreAnnotation=str_.rfind('//',0,loc)#最近的注释位置
    if locOfPreLinefeed==-1:#此时是第一行，前面无换行符
        if locOfPreAnnotation!=-1:#前面有注释符
            unEffectiveCase2=True#属于无效位置
        else:
            unEffectiveCase2=False
    else:#前面有换行符
        if locOfPreAnnotation!=-1:#前面有注释符
            if locOfPreAnnotation>locOfPreLinefeed:#属于无效位置
                unEffectiveCase2=True
            else:
                unEffectiveCase2 = False
        else:
            unEffectiveCase2=False#属于有效位置
    if unEffectiveCase1==False and unEffectiveCase2==False:
        return loc
    else:#说明是无效位置，还要继续找
        loc=findEffectiveLocOfSign(sign,str_, loc+1)
    return(loc)


def getRidOfTextBetweenDoubleQuote(str_):
    # find first有效位置
    loc=findEffectiveLocOfSign(str_,0)
    if loc==-1:
        result=str_
        return(str_)
    else:
        loc2=findEffectiveLocOfSign(str_,loc+1)
        str_=str_.replace(str_[loc:loc2+1],'')
        str_=getRidOfTextBetweenDoubleQuote(str_)
        return (str_)
print(getRidOfTextBetweenDoubleQuote(str_))





    # sline=str_.split('\n')
    # lineCounter1=0
    # lineLen=0
    # for line in sline:
    #     startIndex=line.find('\"')
    #     if (line.find())or():
    #
    #
    #
    #         continue
    #
    #
    #     loc=lineLen+startIndex+lineCounter1#字符串中的准确位置
    #     lineCounter1+=1
    #
    #     lineLen+=len(line)
#
# getRidOfTextBetweenDoubleQuote(str_)