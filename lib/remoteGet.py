import time

import visa


#日期：2019年08月24日
#版本：V1.0
#制作人：刘子恒


# ==== 矢网 =====================================================================================
#罗德矢量网络分析仪
class ZVA:
    #
    def __init__(self, dev_name, save_path, tcp_addr):
        self.dev_name = dev_name
        self.filePath = save_path
        self.tcp_addr = 'TCPIP0::' + tcp_addr + '::inst0::INSTR'

    # ---- 打开 ---------------------------------------------------------------------
    def open_inst(self):

        if self.dev_name == 'ZNB20':
            self.tcp_addr = self.tcp_addr        # 仪表上面的网口
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except Exception:
                self.linkState = 0
            else:
                self.linkState = 1

        if self.dev_name == 'ZVB8':
            # self.tcp_addr = 'TCPIP0::192.168.1.18::inst0::INSTR'        # 仪表上面的网口
            self.tcp_addr = self.tcp_addr        # 仪表上面的网口

            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except Exception:
                self.linkState = 0
            else:
                self.linkState = 1

        if self.dev_name == 'ZVA40':
            # self.tcp_addr = 'TCPIP0::192.168.1.20::inst0::INSTR'
            self.tcp_addr = self.tcp_addr        # 仪表上面的网口

            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except Exception:
                self.linkState = 0
            else:
                self.linkState = 1

        if self.dev_name == 'ZVA50':
            # self.tcp_addr = 'TCPIP0::192.168.1.15::inst0::INSTR'
            self.tcp_addr = self.tcp_addr        # 仪表上面的网口

            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except Exception:
                self.linkState = 0
            else:
                self.linkState = 1

    # ---- 关闭 ---------------------------------------------------------------------
    def close_inst(self):
        """
        lines =['SYST:DISP:UPD ON@',
                'SENS1:SWE:TYPE POW@',
                'SENS1:AVER:COUN AVERCOUNT@',
                'SENS1:AVER ON@',
                "DIAG:SERV:RFP ON@",
                "SENS1:FREQ:CW CWFREQ@",
                "延迟100ms@",
                "SOUR1:POW:STOP POWERSTOP@",
                "延迟100ms@",
                "CALC1:STAT:NLIN:COMP:LEV 1.000000E+0@",
                '延迟100ms@',
                'CALC1:STAT:NLIN:COMP:RES?@',
                'DIAG:SERV:RFP OFF@']
        """

        try:
            str_temp = ''
            cmd = 'OUTP OFF'
            str_temp = self.send_cmd(cmd)

            str_temp += str(self.instance.close())
            return str_temp
        except Exception as e:
            return str(e)

    # S参数测试方法，设置POWIN（输入功率）、STARTFREQ（起始频点）、STOPFREQ（终止频点）、FILENAME（s2p文件名称）参数，
    # 返回值0：s2p文件保存成功，其余返回值详见错误代码表
    def S_data_save(self, POWERIN, STARTFREQ, STOPFREQ, FILENAME):
        lines =['SYST:DISP:UPD ON@',
                'SENS1:SWE:TYPE LIN@',
                'SENS1:FREQ:STAR STARTFREQ@',
                'SENS1:FREQ:STOP STOPFREQ@',
                'SOUR1:POW POWERIN@',
                '延迟500ms@',
                "CALC1:PAR:SDEF 'Trc2','S11'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC2:FEED 'Trc2'@",
                "CALC1:PAR:SDEF 'Trc3','S12'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC3:FEED 'Trc3'@",
                "CALC1:PAR:SDEF 'Trc4','S22'@",
                "DISP:WIND1:STAT ON;:DISP:WIND1:TRAC4:FEED 'Trc4'@",
                '延迟500ms@',
                'MMEM:STOR:TRAC:CHAN ALL,FILEPATH@']
        FILEPATH = "'"+self.filePath+'\\'+FILENAME +'.s2p'+"'"
        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟500ms'):
                        time.sleep(0.5)
                    else:
                        instr = instr.replace('POWERIN', POWERIN)
                        instr = instr.replace('STARTFREQ', STARTFREQ)
                        instr = instr.replace('STOPFREQ', STOPFREQ)
                        instr = instr.replace('FILEPATH', FILEPATH)
                        print(instr)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
        return 0

    #P-1测试方法，设置AVERCOUNT（平均采样次数）、POWERSTOP（截至功率）、CWFREQ（待测频点）参数，
    # 返回值为'<port_In>,<port_Out>'：代表输入1dB压缩点和输出1dB压缩点，其余返回值详见错误代码表
    def P1_data(self, AVERCOUNT, POWERSTOP, CWFREQ):
        lines =['SYST:DISP:UPD ON@',
                'SENS1:SWE:TYPE POW@',
                'SENS1:AVER:COUN AVERCOUNT@',
                'SENS1:AVER ON@',
                "DIAG:SERV:RFP ON@",
                "SENS1:FREQ:CW CWFREQ@",
                "延迟100ms@",
                "SOUR1:POW:STOP POWERSTOP@",
                "延迟100ms@",
                "CALC1:STAT:NLIN:COMP:LEV 1.000000E+0@",
                '延迟100ms@',
                'CALC1:STAT:NLIN:COMP:RES?@',
                'DIAG:SERV:RFP OFF@']

        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟100ms'):
                        time.sleep(0.3)
                    else:
                        instr = instr.replace('AVERCOUNT', AVERCOUNT)
                        instr = instr.replace('CWFREQ', CWFREQ)
                        instr = instr.replace('POWERSTOP', POWERSTOP)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2

    #频段内最大增益点测试方法，设置AVERCOUNT（平均采样次数）、STARTFREQ（起始频点）、STOPFREQ（终止频点）参数，
    # 返回值为'<freq>,<mag>'：最大增益对应频率和最大增益值，其余返回值详见错误代码表
    def mark_max_data(self,AVERCOUNT,STARTFREQ,STOPFREQ):
        lines = ['SYST:DISP:UPD ON@',
                 'SENS1:SWE:TYPE LIN@',
                 'SENS1:AVER:COUN AVERCOUNT@',
                 'SENS1:AVER ON@',
                 "SENS1:FREQ:STAR STARTFREQ@",
                 "SENS1:FREQ:STOP STOPFREQ@",
                 "延迟100ms@",
                 "CALC1:MARK1 OFF@",
                 "延迟100ms@",
                 "CALC1:MARK1 ON@",
                 "延迟100ms@",
                 "CALC1:MARK1:FUNC:EXEC MAX@",
                 '延迟100ms@',
                 'CALC1:MARK1:FUNC:RES?@']

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('AVERCOUNT', AVERCOUNT)
                        instr = instr.replace('STARTFREQ', STARTFREQ)
                        instr = instr.replace('STOPFREQ', STOPFREQ)

                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return '-2:remote指令错误，请设置合适参数'
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return '-3:请求矢网返回数据超时'

    #通过MARK点获取频点对应Value
    def mark_data(self, **kwargs):
        strParams = ["ch", "markPoint", "freqData", "status"]
        for strParam in strParams:
            try:
                if type(kwargs[strParam]) != str:
                    kwargs[strParam] = str(kwargs[strParam])
            except BaseException:
                return "-3:缺少" + strParam + "参数"
        lines = [
            "CALC" + kwargs["ch"] + ":MARK" + kwargs["markPoint"]+" "+kwargs["status"]+"@",
            "CALC" + kwargs["ch"] + ":MARK" + kwargs["markPoint"]+":X "+kwargs["freqData"]+"@",
            '延迟100ms@',
            "CALC" + kwargs["ch"] + ":MARK" + kwargs["markPoint"]+":Y?@"
        ]

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.2)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                        return self.instance.query(instr)
                    except BaseException:
                        return -2

    #添加trace
    def add_ch(self,**kwargs):
        strParams = ["window","ch","testType","dataType","trac","traceName","traceType"]
        for strParam in strParams:
            try:
                if type(kwargs[strParam]) != str:
                    kwargs[strParam] = str(kwargs[strParam])
            except BaseException:
                return "-3:缺少"+strParam+"参数"
        lines = [
            "CALC" + kwargs["ch"] + ":PAR:SDEF " + "'" + kwargs["traceName"] + "'" + "," + "'" + kwargs[
                "traceType"] + "'" + "@",
            "DISP:WIND"+kwargs["window"]+":STAT ON;:DISP:WIND"+kwargs["window"]+":TRAC"+kwargs["trac"]+":FEED '"+kwargs["traceName"]+"'@",
            "SENS"+kwargs["ch"]+":SWE:TYPE "+kwargs["testType"]+"@",
            "CALC"+kwargs["ch"]+":FORM "+kwargs["dataType"]+"@"
            ]

        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟100ms'):
                        time.sleep(0.3)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
        return 0

    # 删除频道及trace
    def delete_ch(self,ch):
        if type(ch) != str:
            ch = str(ch)
        lines =[
            "CALC"+ch+":PAR:DEL:CALL@"
        ]

        for line in lines:
            if(line.find('@')>0):
                instr = line[:line.index('@')]
                if(instr.find('?')<0):
                    if(instr == '延迟100ms'):
                        time.sleep(0.3)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
        return 0

    # ---- 发送 -------------------------------------------------------------------------
    def send_cmd(self, str_cmds):
        a = self.cmd_tx(str_cmds)
        return a

    def cmd_tx(self, str_cmds):
        str_temp = ''

        i = 0
        for cmd in str(str_cmds).split('\n'):
            try:
                # // 为注释，# 为注释，只取一行中的前面的命令
                if cmd and cmd.strip() and cmd.strip()[0:2] != '//' and cmd.strip()[0] != '#':
                    for cmd_real in str(cmd).split('//'):

                        # // 为注释，# 为注释，只取一行中的前面的命令
                        if cmd_real and str(cmd_real).strip() and cmd_real[0] != '//':
                            i += 1
                            # print(cmd)
                            if cmd_real.strip()[-1] == '?':              # 查询命令
                                rt_v = self.instance.query(cmd_real)
                                print("query: %s" % str(cmd_real).strip())
                            else:                               # 配置命令
                                print("set: %s" % str(cmd_real).strip())
                                rt_v = self.instance.write(cmd_real)

                            print(str(rt_v))
                            str_temp += 'i = %s : %s\n' % (i, rt_v)
                            time.sleep(0.2)

                            break

            except Exception as e:
                return str(e)

        return str_temp


# ==== 频谱仪 =====================================================================================
# 罗德频谱仪系列
class RSFSx:
    #
    def __init__(self,devName):
        self.linkState = 0
        if(devName == 'FSWP'):
            self.tcp_addr = 'TCPIP0::FSWP26-101228::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

        if(devName == 'FSV'):
            self.tcp_addr = 'TCPIP0::192.168.1.81::inst0::INSTR'
            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

    # 频段内增益测试方法，设置CENTERFREQ（MARK点频率坐标）、SPANFREQ（扫描频率宽度）参数，
    # 返回值为'<mag>'：MARK点的功率值，其余返回值详见错误代码表
    def mark_data(self,CENTERFREQ, SPANFREQ):
        lines = ['SYST:DISP:UPD ON@',
                 'INST SAN@',
                 'FREQ:CENT CENTERFREQ@',
                 'FREQ:SPAN SPANFREQ@',
                 '延迟100ms@',
                 'CALC1:MARK1 ON@',
                 '延迟100ms@',
                 'CALC1:MARK1:TRAC 1@',
                 '延迟100ms@',
                 'CALC1:MARK1:X CENTERFREQ@',
                 '延迟100ms@',
                 'CALC1:MARK1:Y?@']
                 #Mark
        rm1 = visa.ResourceManager()
        try:
            instance = rm1.open_resource(self.tcp_addr)
        except BaseException:
            return '-1：连接矢网超时'
        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('CENTERFREQ', str(CENTERFREQ))
                        instr = instr.replace('SPANFREQ', str(SPANFREQ))
                        try:
                            instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    if(instr.find('MARK1') > 0):
                        try:
                            temp = str(instance.query(instr))
                            return temp
                        except BaseException:
                            return -2

    # ---- 发送 -------------------------------------------------------------------------
    def send_cmd(self, str_cmds):
        a = self.cmd_tx(str_cmds)
        return a

    def cmd_tx(self, str_cmds):
        str_temp = ''

        i = 0
        for cmd in str(str_cmds).split('\n'):
            try:
                # // 为注释，# 为注释，只取一行中的前面的命令
                if cmd and cmd.strip() and cmd.strip()[0:2] != '//' and cmd.strip()[0] != '#':
                    for cmd_real in str(cmd).split('//'):

                        # // 为注释，# 为注释，只取一行中的前面的命令
                        if cmd_real and str(cmd_real).strip() and cmd_real[0] != '//':
                            i += 1
                            # print(cmd)
                            if cmd_real.strip()[-1] == '?':              # 查询命令
                                rt_v = self.instance.query(cmd_real)
                                print("query: %s" % str(cmd_real).strip())
                            else:                               # 配置命令
                                print("set: %s" % str(cmd_real).strip())
                                rt_v = self.instance.write(cmd_real)

                            print(str(rt_v))
                            str_temp += 'i = %s : %s\n' % (i, rt_v)
                            time.sleep(0.2)

                            break

            except Exception as e:
                return str(e)

        return str_temp


# ==== 信号源 =====================================================================================
# 罗德信号源系列
class RSRFSin:
    def __init__(self, dev_name, tcp_addr):
        self.dev_name = dev_name
        self.tcp_addr = 'TCPIP0::' + tcp_addr + '::inst0::INSTR'
        self.linkState = 0

    def open_inst(self):

        if self.dev_name == 'SMW200A':
            # self.tcp_addr = 'TCPIP0::192.168.1.120::inst0::INSTR'

            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except Exception as e:
                self.linkState = 0
                print(str(e))
            else:
                self.linkState = 1

        if self.dev_name == 'SMF':
            # self.tcp_addr = 'TCPIP0::192.168.1.121::inst0::INSTR'

            rm1 = visa.ResourceManager()
            try:
                self.instance = rm1.open_resource(self.tcp_addr)
            except BaseException as e:
                self.linkState = 0
                print(str(e))
            else:
                self.linkState = 1

    # ---- 关闭 ---------------------------------------------------------------------
    def close_inst(self):
        try:
            str_temp = ''
            cmd = 'OUTP OFF'
            str_temp = self.send_cmd(cmd)

            str_temp += str(self.instance.close())
            return str_temp
        except Exception as e:
            return str(e)

    # 信号源输出控制功能，设置RFFREQ（期望输出频率值）、POWVALUE（期望输出功率值）、IQSTATE（IQ信号开关）、RFOUTSTATE（信号输出控制参数，ON为开，OFF为关），
    # 配置正常则返回0，其余返回值详见错误代码表
    def RFout(self,RFFREQ, POWVALUE, IQSTATE, RFOUTSTATE):
        lines = ['SOUR1:FREQ RFFREQ@',
                 'SOUR1:POW POWVALUE@',
                 ':SOUR1:IQ:STAT IQSTATE@',
                 'OUTP1 RFOUTSTATE@']

        for line in lines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟100ms'):
                        time.sleep(0.1)
                    else:
                        instr = instr.replace('RFFREQ', RFFREQ)
                        instr = instr.replace('POWVALUE', POWVALUE)
                        instr = instr.replace('IQSTATE', IQSTATE)
                        instr = instr.replace('RFOUTSTATE', RFOUTSTATE)
                        try:
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                       return self.instance.query(instr)
                    except BaseException:
                        return -2
        return 0

    def send_cmd(self, str_cmds):
        a = self.cmd_tx(str_cmds)
        return a

    def cmd_tx(self, str_cmds):
        str_temp = ''

        i = 0
        for cmd in str(str_cmds).split('\n'):
            try:
                # // 为注释，# 为注释，只取一行中的前面的命令
                if cmd and cmd.strip() and cmd.strip()[0:2] != '//' and cmd.strip()[0] != '#':
                    for cmd_real in str(cmd).split('//'):

                        # // 为注释，# 为注释，只取一行中的前面的命令
                        if cmd_real and str(cmd_real).strip() and cmd_real[0] != '//':
                            i += 1
                            # print(cmd)
                            if cmd_real.strip()[-1] == '?':              # 查询命令
                                rt_v = self.instance.query(cmd_real)
                                print("query: %s" % str(cmd_real).strip())
                            else:                               # 配置命令
                                print("set: %s" % str(cmd_real).strip())
                                rt_v = self.instance.write(cmd_real)

                            print(str(rt_v))
                            str_temp += 'i = %s : %s\n' % (i, rt_v)
                            time.sleep(0.2)

                            break

            except Exception as e:
                return str(e)

        return str_temp


# ==== 万用表 =====================================================================================
# 是德科技3446X系列（数字万用表）
class KeySightDigit:
    def __init__(self,devName):
        self.linkState = 0

        if(devName == '数字万用表1'):
            self.tcp_addr = '34461A_1'#地址为192.168.1.91
            rm1 = visa.ResourceManager()
            try:
                print(4)
                self.instance = rm1.open_resource(self.tcp_addr)
                print(5)

            except BaseException:
                self.linkState = 0
            else:
                self.linkState = 1

    def getValue(self,**kwargs):
        outData = 0
        getlines = [
            '延迟500ms@',
            ':FUNC "' + kwargs["testMode"]+'"@',
            ':' + kwargs["testMode"] + ':RANG:AUTO ON@',
            ':SAMP:COUN 1@',
            ':TRIG:SOUR IMM@',
            ':READ?@'
        ]
        for line in getlines:
            if (line.find('@') > 0):
                instr = line[:line.index('@')]
                if (instr.find('?') < 0):
                    if (instr == '延迟500ms'):
                        time.sleep(0.5)
                    else:
                        try:
                            print(instr)
                            self.instance.write(instr)
                        except BaseException:
                            return -1
                else:
                    try:
                        outData = self.instance.query(instr)
                    except BaseException:
                        return -2
        return outData


# ==== 通用功能 =====================================================================================
class comFun:
    def __init__(self,strType):
        self.flag = strType

    def flaotOrintAll(self,a):
        if(self.flag == 'float'):
            temp = 0
            if(a.find('-')>=0):
                try:
                    temp =0 - float(a.replace('-',''))
                except BaseException:
                   print( 'float转换错误')
            else:
                try:
                    temp = float(a)
                except BaseException:
                    print('float转换错误')
            return temp

        if(self.flag == 'int'):
            temp = 0
            if (a.find('-') >= 0):
                try:
                    temp = 0 - int(a.replace('-', ''))
                except BaseException:
                    print('int转换错误')
            else:
                try:
                    temp = int(a)
                except BaseException:
                    print('int转换错误')
            return temp


