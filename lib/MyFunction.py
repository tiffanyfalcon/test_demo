#!/usr/bin/python3
# from psutil import *        # 获取所有网卡
import binascii
import uuid


# ---- 获取 MAC 地址 -----------------------------------------------------
def get_mac_address(self):
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    strMac = ":".join([mac[e:e + 2] for e in range(0, 11, 2)])
    str1 = ''
    str1 += strMac
    return strMac

# ---- 获取所有 MAC 地址 -----------------------------------------------------
'''
def get_mac_all(self):
    add = ''
    for k, v in net_if_addrs().items():
        for item in v:
            address = item[1]
            if '-' in address and len(address) == 17:
                # print(address)
                add += address + '\n'
    return add
'''

# ---- 合并 空格 -----------------------------------------------------
def cambine_space(self, str1):
    cntSpace = 0
    str2 = ''

    for i in range(len(str1)):
        if i > 0:
            if str1[i] == str1[i-1] and str1[i] == ' ':
                str2 += ''
            else:
                str2 += str1[i]
        else:
            str2 += str1[i]

    return str2

# ---- 提取网表名称 -----------------------------------------------------
def str_get_first_name(self, str1):

    strTemp = ''

    listLine = str1.split('\n')

    for eachLine in listLine:
        strTemp += eachLine[0:eachLine.find(' ', 1)]
        strTemp += '\n'

    strTemp = strTemp[0: -1]

    return strTemp

# ---- 去掉重复网表名称 -----------------------------------------------------
def list_get_net_name(self, str1):

    listReture = []
    str2 = self.str_get_first_name(str1)

    listLine = str2.split('\n')

    for eachLine in listLine:
        if eachLine not in listReture:
            listReture.append(eachLine)

    return listReture

# ---- CRC32 -----------------------------------------------------
def str_my_crc32(self, v):
    """
    Generates the crc32 hash of the v.
    @return: str, the str value for the crc32 of the v
    """
    # return '0x%x' % (binascii.crc32(v.encode) & 0xffffffff)  # 取crc32的八位数据 %x返回16进制
    intCrc = (binascii.crc32(v.encode()) & 0xffffffff)    # 取crc32的八位数据 %x返回16进制
    strCrc = str(intCrc)
    return strCrc

    # print(_crc32(mac.encode()))       # 使用方法

# ---- 查找 字符串A 存在于 B 表中，B 以 C 分割 --------------------------------
def str_str_equal_substr(self, strA, strB, charC):

    boolRet = False

    for listStr in strB.split(charC):
        if strA == listStr:
            boolRet = True
            break

    return boolRet

# ---- 查找 字符串A 存在于 B 表中的第 0 个，B 以 C 分割 --------------------------------
def bool_str_equal_substr0(self, strA, strB, charC) -> bool:

    boolRet = False

    listStr = strB.split(charC)
    if len(listStr) > 0:
        if strA == listStr[0]:
            boolRet = True

    return boolRet

# ---- 删除 str --------------------------------
def str_del_StrCom_in_str(self, strNetSrc, charSplitSrc, strDel, charSplitDel) -> str:
    '''
    :param strNetSrc: 源字符串，网名\t 位号.pin...
    :param splitSrcChar: 源字符串分割符
    :param strDel: 删除位号的字符串
    :param splitDelChar: 删除字符串的翻分割符
    :return: 删除位号后的字符串
    '''

    listDelcom = strDel.split(charSplitDel)
    retStr = ''
    outPutDeledStr = ''
    for eachLine in strNetSrc.split('\n'):            # 器件行
        strDeledComLine = eachLine + charSplitSrc  # 给末尾加一个 TAB，解决最后一个器件无法替换

        if len(eachLine) > 0:                               # 有的器件行是空
            for eachDelCom in listDelcom:                   # 删除表中的位号
                for eachCom in eachLine.split(charSplitSrc)[1:]:    # 器件行中的 0 列后
                    if self.bool_str_equal_substr0(eachDelCom.strip(), eachCom, '.'):  # 有删除的器件
                        strDeledComLine = strDeledComLine.replace(eachCom.strip() + charSplitSrc, '') + charSplitSrc

        outPutDeledStr += strDeledComLine.strip(charSplitSrc) + '\n'

        retStr = outPutDeledStr

    return retStr

# //// 删除网表中 只有网名 无 位号的网络 ////////////////////////////////////////////////////
def str_del_netWithoutCom(self, strNetSrc, charSplitSrc) -> str:
    '''

    :param strNetSrc: string
    :param charSplitSrc: char
    :return:
    '''

    retStr = ''
    for eachLine in strNetSrc.split('\n'):          # 器件行
        strLineTemp = eachLine
        listLen = len(strLineTemp.split(charSplitSrc))
        if listLen > 1:
            retStr += eachLine + '\n'

    retStr = retStr.strip('\n') + '\n'

    return retStr


