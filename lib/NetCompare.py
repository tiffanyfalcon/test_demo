#!/usr/bin/python3
# import os
from lib import MyFunction
# import tkinter.messagebox as messagebox


class NetCompare:

    strInputFile1 = ''
    strInputFile2 = ''
    strOutputFile = ''
    strOutNetFile1 = ''
    strOutNetFile2 = ''

    strNetTable1 = ''
    strNetTable2 = ''

    debugEn = 0
    saveMode = 0

    mf = MyFunction.MyFunction()

    # //// 设置网表文件名 ///////////////////////////////////////////////////////////
    def setFileName(self, str1, str2, str3, outNet1, outNet2):
        self.strInputFile1 = str1
        self.strInputFile2 = str2
        self.strOutputFile = str3

        self.strOutNetFile1 = outNet1
        self.strOutNetFile2 = outNet2

    # //// 转换网表 Orcad /////////////////////////////////////////////////////////
    def fStrNetChangeOrcad(self, strFileName, strDelCom):
        boolCurLineIsNet = False
        boolPreLineIsNet = False
        cntNet = 0
        strCurLine = ''
        strNetTable1 = ''

        # print(strFileName)

        with open(strFileName, 'r') as f:
            # print (f.read())
            for eachLine in f.readlines():
                line = eachLine.strip()

                if ("NET_NAME" in line):
                    boolCurLineIsNet = True
                    boolPreLineIsNet = False
                    cntNet += 1
                    if cntNet > 1:
                        strNetTable1 += strCurLine + '\n'

                else:  # net名称
                    if boolCurLineIsNet:
                        boolPreLineIsNet = boolCurLineIsNet
                        boolCurLineIsNet = False
                        strCurLine = line.strip('\n')

                        # print( strCurLine, end ='')

                    else:  # node 名称
                        if "NODE_NAME" in line:
                            strTemp = line.replace('NODE_NAME', '')
                            strTemp.replace('\t', '')
                            strCurLine += line.replace('NODE_NAME', '')
                            # print(strCurLine, end = '')

            f.close()

        strNetTable1 += strCurLine
        strNetTable1 = strNetTable1.replace(' ', '.')
        strNetTable1 = strNetTable1.replace('\'', '')

        # ---- 存文件 ---------------------------------------------------------
        if self.saveMode and self.debugEn:
            with open(r'netChgOrcad.csv', 'w') as f:
                f.write(strNetTable1)
                f.close()

        # ---- 删除要删除的器件 --------------------------------------------------------
        '''
        listDelcom = strDelCom.split(',')
        outPutDeledStr = ''
        for eachLine in strNetTable1.split('\n'):  # 器件行
            strDeledComLine = eachLine + '\t'       # 给末尾加一个 TAB，解决最后一个器件无法替换

            if len(eachLine) > 0:  # 有的器件行是空
                for eachDelCom in listDelcom:  # 删除表中的位号
                    for eachCom in eachLine.split('\t')[1:]:  # 器件行中的 0 列后
                        if self.mf.bool_str_equal_substr0(eachDelCom.strip(), eachCom, '.'):  # 有删除的器件
                            strDeledComLine = strDeledComLine.replace(eachCom + '\t', '') + '\t'

            # outPutDeledStr += strDeledComLine + '\t\t\t\t' + strComDeled + '\n'
            outPutDeledStr += strDeledComLine.strip('\t') + '\n'
        '''
        outPutDeledStr = self.mf.str_del_StrCom_in_str(strNetTable1, '\t', strDelCom, ',')
        strNetTable1 = outPutDeledStr

        return strNetTable1

    # //// 转换网表 allegro PCB ////////////////////////////////////////////////////////////////////////////
    def fStrNetChangeAllegroPcb(self, strFileName):
        # str1 = '+3.3V_AVDD               C8               1        CAPACITOR_0603-CT41G_0603_2X1_B'
        strNet = ''
        listNetName = ''

        # ---- 第一次转换网表，保留一个空格，去掉多余空格 -------------------------
        with open(strFileName, 'r') as f:
            # print (f.read())

            i = 0
            for eachLine in f.readlines():
                if i > 0:
                    # line += mf.cambine_space(eachLine.strip())
                    strNet += self.mf.cambine_space(eachLine)
                    # line += '\n'

                i += 1

        f.close()
        strNet = strNet.replace(' ,\n', ' ')
        strNet = strNet.replace('  ', ' ')

        # ---- 处理网表 --------------------------------------------------------

        strNetTable = ''
        listLine = strNet.split('\n')

        for eachLine in listLine:
            if '!' not in eachLine.split(' '):
                if ';' in eachLine.split(' '):
                    str_temp = eachLine.split(' ; ')
                    strNetTable += str_temp[0].replace('\'', '') + '\t' + str_temp[1].replace(' ', '\t')
                    strNetTable += '\n'

        # strNetTable = strNetTable.replace(' ', '\t')
        # strNetTable = strNetTable.replace('\'', '')
        # strNetTable = strNetTable.replace('.', ' ')

        # ---- 存文件 ---------------------------------------------------------
        if self.saveMode and self.debugEn:
            with open(r'30sou.csv', 'w') as f:
                f.write(strNet)
                f.close()

            # with open(r'30sou_netName_all.csv', 'w') as f:
            #     f.write(strNetName)
            #     f.close()

            with open(r'netChgAllPCB.csv', 'w') as f:
                f.write(strNetTable)
                f.close()

            # print(str2)

        return strNetTable

    # //// 转换网表 allegro ////////////////////////////////////////////////////////////////////////
    def fStrNetChangeAllegro(self, strFileName, strDelCom):

        # str1 = '+3.3V_AVDD               C8               1        CAPACITOR_0603-CT41G_0603_2X1_B'
        strNet = ''
        listNetName = ''

        # ---- 第一次转换网表，保留一个空格，去掉多余空格 -------------------------
        with open(strFileName, 'r') as f:
            # print (f.read())

            i = 0
            for eachLine in f.readlines():
                if i > 0:
                    # line += mf.cambine_space(eachLine.strip())
                    strNet += self.mf.cambine_space(eachLine)
                    # line += '\n'

                i += 1

        f.close()

        # ---- 得到网表列表 ----------------------------------------------------
        strNetName = ''

        listNetName = self.mf.list_get_net_name(strNet)
        for eachList in listNetName:
            strNetName += eachList
            strNetName += '\n'

        strNetName = strNetName[0: -1]

        # ---- 处理网表 --------------------------------------------------------

        strNetTable = ''

        for eachList1 in listNetName:
            strNetTable += eachList1
            strNetTable += '\t'

            listLine = strNet.split('\n')

            for eachLine in listLine:
                listText = eachLine.split(' ')
                strNetName = listText[0]

                if len(listText) > 2:
                    strCom = listText[1] + '.' + listText[2] + '\t'

                    if eachList1 == strNetName:
                        strNetTable += strCom

            strNetTable += '\n'
            strNetTable = strNetTable.replace('\'', '')

        # ---- 存文件 ---------------------------------------------------------

        if self.saveMode and self.debugEn:
            '''
            with open(r'30sou.csv', 'w') as f:
                f.write(strNet)
                f.close()

            with open(r'30sou_netName_all.csv', 'w') as f:
                f.write(strNetName)
                f.close()
            '''

            with open(r'netChgAll.csv', 'w') as f:
                f.write(strNetTable)
                f.close()

            # print(str2)

        # ---- 删除要删除的器件 --------------------------------------------------------
        '''
        listDelcom = strDelCom.split(',')
        outPutDeledStr = ''
        for eachLine in strNetTable.split('\n'):            # 器件行
            strDeledComLine = eachLine + '\t'  # 给末尾加一个 TAB，解决最后一个器件无法替换

            if len(eachLine) > 0:                               # 有的器件行是空
                for eachDelCom in listDelcom:                   # 删除表中的位号
                    for eachCom in eachLine.split('\t')[1:]:    # 器件行中的 0 列后
                        if self.mf.bool_str_equal_substr0(eachDelCom.strip(), eachCom, '.'):  # 有删除的器件
                            strDeledComLine = strDeledComLine.replace(eachCom.strip() + '\t', '') + '\t'

            # outPutDeledStr += strDeledComLine + '\t\t\t\t' + strComDeled + '\n'
            outPutDeledStr += strDeledComLine.strip('\t') + '\n'

            strNetTable = outPutDeledStr
        '''
        outPutDeledStr = self.mf.str_del_StrCom_in_str(strNetTable, '\t', strDelCom, ',')
        strNetTable = outPutDeledStr

        if self.saveMode and self.debugEn:
            with open(r'.\net3.csv', 'w') as f:
            # with open(self.strOutputFile + '_del.csv', 'w') as f:
            #     f.write(outPutDeledStr)
                f.write(strNetTable)
                f.close()

        return strNetTable

    # //// 比较网表 //////////////////////////////////////////////////////////////////////
    def voidNetCompare(self, strNet1, strNet2):

        strFileTalbe = 'Net Name' + '\t' + 'Both' + '\t' + 'Only A' + '\t' + 'Only B' + '\t' + \
                       '相同拓扑' + '\t' + '删除器件' + '\n'

        strNetAll = ''          # 网络拓扑完全相同
        str_net_both = ''       # 网络名相同，拓扑有差异
        str_net_only_a = ''     # 网络 只有A有
        str_net_only_b = ''     # 网络 只有B有
        str_net_com_equal = ''  # 网络名不同，网络相同

        strComBoth = ''
        strComSideA = ''
        strComSideB = ''
        strComNetEqual = ''     # 器件，网络名不同，网络相同

        strNetAllEqualNT = ''   # 网表完全相同，网名列表
        strNetTopEqualNT = ''   # 器件拓扑相同，网名列表
        strNetNameEqualNT = ''  # 网名相同，网名表

        listNet1 = strNet1.split('\n')
        listNet2 = strNet2.split('\n')

        # print( listNet1[53])

        # ==== 网表1 轮循 =============================================
        listComponent1 = []
        listComponent2 = []

        # ---- 网表 一行 -------------------------------------
        for eachNet1 in listNet1:

            bool_net_equal = False
            bool_net_name_equal = False
            bool_net_topology = False           # 网表拓扑结构相同

            for eachNet2 in listNet2:

                # 网表行完全相同 ==============
                if eachNet1 == eachNet2:
                    if eachNet1 != '':
                        bool_net_equal = True
                        bool_net_name_equal = True
                        # strNetAll += eachNet1 + '\n'
                        strNetAll += eachNet1.strip().replace('\t', ';').replace(';', '\t', 1) + ';\n'
                        listComponent1 = eachNet1.strip().split('\t')
                        strNetAllEqualNT += listComponent1[0] + '\n'
                        break

                # 网表行不相同 ==============
                else:
                    listComponent1 = eachNet1.strip().split('\t')
                    listComponent2 = eachNet2.strip().split('\t')

                    # 网表名相同 ================
                    if listComponent1[0] == listComponent2[0]:

                        cntCom = 0
                        bool_net_name_equal = True
                        strNetNameEqualNT += listComponent1[0] + '\n'

                        for eachCom1 in listComponent1[1:]:
                            inta = eachNet2.find(eachCom1)
                            # if eachNet2.find(eachCom1) > 0:
                            if inta > 0:
                                cntCom += 1
                                strComBoth += eachCom1 + ';'
                            # ---- 只存在 A 网络中 ----------------------------
                            else:
                                strComSideA += eachCom1 + ';'
                                # cntComA += 1
                                # if cntComA == 1:
                                #     strComSideA += eachCom1
                                # else:
                                #     strComSideA += ';' + eachCom1

                        # print('net = ', listComponent1[0], end = '\t')
                        # print('cnt = ', cntCom, end = '\t')
                        # print('len = ', len(listComponent2 ))

                        # ---- 两个网络的器件，顺序不同，节点相同，节点数也相同，则网表相同 -----------------
                        if cntCom == len(listComponent1) - 1 and cntCom == len(listComponent2) - 1:
                            bool_net_equal = True
                            strNetAll += eachNet1.replace('\t', ';').replace(';', '\t', 1) + ';\n'
                            strNetAllEqualNT += listComponent1[0] + '\n'
                            strComBoth = ''
                            strComSideA = ''
                            # strComSideB = ''
                        else:
                            for eachCom2 in listComponent2[1:]:
                                if eachNet1.find(eachCom2) < 0:
                                    strComSideB += eachCom2 + ';'
                        continue

                    # 查 网表名 不同，网络相同 ===========
                    else:
                        intLen = len(listComponent1)
                        if intLen == len(listComponent2):  # 个数完全相等（包括网表名称）

                            cntCom = 0
                            for eachCom1 in listComponent1[1:]:
                                if eachNet2.find(eachCom1) > 0:
                                    cntCom += 1
                                    strComNetEqual += eachCom1 + ';'

                            if intLen == cntCom + 1:  # 网表名称不同，网络结点相同
                                str_net_com_equal += listComponent1[0] + '\t' + strComNetEqual + '\t\t\t' + \
                                                     listComponent2[0] + '\n'  # A网络名 器件 A B B网络名

                                strComNetEqual = ''
                                bool_net_topology = True              # 实际网络相同，网名不同
                                strNetTopEqualNT += listComponent2[0] + '\n'

                                break
                            else:
                                strComNetEqual = ''


            # 网络名只存在 网表1 中 =============
            if not bool_net_name_equal:
                if not bool_net_topology:
                    strTemp = eachNet1.replace('\t', ';').replace(';', '\t', 1)
                    strTemp = strTemp[strTemp.find('\t') + 1:]

                    str_net_only_a += listComponent1[0] + '\t' + '\t' + strTemp + '\n'

            else:
                if not bool_net_equal:
                    str_net_both += listComponent1[0] + '\t' + strComBoth + '\t' + \
                                    strComSideA + '\t' + strComSideB + '\n'
                    strComBoth = ''
                    strComSideA = ''
                    strComSideB = ''

        # ==== 网表2 轮循 =============================================
        for eachNet2 in listNet2:

            bool_net_name_equal = False

            listComponent2 = eachNet2.split('\t')
            if self.mf.str_str_equal_substr(listComponent2[0], strNetAllEqualNT, '\n'):       # 网表相同，包括网名相同，但器件位置不同
                bool_net_name_equal = True

            elif self.mf.str_str_equal_substr(listComponent2[0], strNetTopEqualNT, '\n'):     # 网名不同，但拓扑相同，在 网名2 列表中
                bool_net_name_equal = True

            # elif listComponent2[0] in strNetNameEqualNT:    # 网名相同    2019年3月12日：这种比较方式不行，因为有的网名是：aaa_a，包含 aaa
            #     bool_net_name_equal = True

            elif self.mf.str_str_equal_substr(listComponent2[0], strNetNameEqualNT, '\n'):   # 网名完全相同
                bool_net_name_equal = True

            # 网络名只存在 网表2 中 =============
            if not bool_net_name_equal:
                strTemp = eachNet2.replace('\t', ';').replace(';', '\t', 1)
                strTemp = strTemp[strTemp.find('\t') + 1:]

                str_net_only_b += listComponent2[0] + '\t' + '\t' + '\t' + strTemp + ';\n'

        '''
        print()
        print('net all equal\t= ')
        print(strNetAll)
        print()
    
        print('net equal component Not Equal \t= ')
        print(str_net_both)
        print()
    
        print('net alone1 \t= ')
        print(str_net_only_a)
        print()
    
        print('net alone2 \t= ')
        print(str_net_only_b)
        '''

        # ==== 保存比较结果 =============================================
        outPutStr = strFileTalbe + strNetAll + '\n' + str_net_both + '\n' +\
                    str_net_only_a + '\n' + str_net_only_b + '\n' + str_net_com_equal + '\n'

        if self.saveMode == 1:
            # with open(r'.\net3.csv', 'w') as f:
            with open(self.strOutputFile, 'w') as f:
                f.write(outPutStr)
                f.close()
        '''
        # ---- 删除要删除的器件 --------------------------------------------------------
        listDelcom = strDelCom.split(',')
        strComDeled = ''    # 已删除的器件
        outPutDeledStr = ''
        strDeledComLine = ''
        for eachLine in outPutStr.split('\n'):              # 器件行
            strDeledComLine = eachLine
            for eachDelCom in listDelcom:                               # 删除表中的位号
                for eachComCambin in eachLine.split('\t')[1:4]:         # 器件行中的 1－3 列
                    listCom = eachComCambin.split(';')                  # x.1 器件列表
                    if len(listCom) > 0:                               # 有的器件行是空
                        for eachCom in listCom:                   # x.1 器件
                            if self.mf.str_str_equal_substr0(eachDelCom.strip(), eachCom, '.'):   # 有删除的器件
                                strDeledComLine = strDeledComLine.replace(eachCom.strip() + ';', '')
                                strComDeled += eachCom + ';'

            outPutDeledStr += strDeledComLine + '\t\t\t\t' + strComDeled + '\n'
            strComDeled = ''

        if self.saveMode == 1:
            # with open(r'.\net3.csv', 'w') as f:
            with open(self.strOutputFile.split('.')[0] + '_del.csv', 'w') as f:
                f.write(outPutDeledStr)
                f.close()
        '''

    # //// 比较网表 上层函数///////////////////////////////////////////////////////////////////////////
    def net_compare(self, file1, file2, file3, type1, type2, strDelCom, netFileOut1, netFileOut2):

        # ---- 设置文件名 ------------------------------------------------------
        self.setFileName(file1, file2, file3, netFileOut1, netFileOut2)

        # ---- 网表转换成统一格式，然后进行比较 ------------------------------------------------------------------
        if type1 == 'allegro':
            self.strNetTable1 = self.fStrNetChangeAllegro(self.strInputFile1, strDelCom)
        elif type1 == 'allegroPCB':
            self.strNetTable1 = self.fStrNetChangeAllegroPcb(self.strInputFile1)
        elif type1 == 'orcad':
            self.strNetTable1 = self.fStrNetChangeOrcad(self.strInputFile1, strDelCom)
        else:
            print("    file1 type wrong!")
            return

        if type2 == 'allegro':
            self.strNetTable2 = self.fStrNetChangeAllegro(self.strInputFile2, strDelCom)
        elif type2 == 'allegroPCB':
            self.strNetTable2 = self.fStrNetChangeAllegroPcb(self.strInputFile2)
        elif type2 == 'orcad':
            self.strNetTable2 = self.fStrNetChangeOrcad(self.strInputFile2, strDelCom)
        else:
            print("    file2 type wrong!")
            return

        # ---- 删除网表中 只有网名 无 位号的网络 ---------------------------------------------
        self.strNetTable1 = self.mf.str_del_netWithoutCom(self.strNetTable1, '\t')
        self.strNetTable2 = self.mf.str_del_netWithoutCom(self.strNetTable2, '\t')

        # ---- 保存转换的网表 ---------------------------------------------
        if self.saveMode and self.debugEn:
            with open(self.strOutNetFile1, 'w') as f:
                f.write(self.strNetTable1)
                f.close()

            with open(self.strOutNetFile2, 'w') as f:
                f.write(self.strNetTable2)
                f.close()

        # ---- 比较网表 --------------------------------------------------
        self.voidNetCompare(self.strNetTable1, self.strNetTable2)
