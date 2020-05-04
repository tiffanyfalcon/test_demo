# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
#

import logging

from PyQt5 import QtCore
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow

from lib.myExcel import MyExcel
from lib.myLog import MyLog, DbgMod
from lib.remoteGet import ZVA, RSRFSin, RSFSx
from view.M_thread import MyThread
from view.ui_main import Ui_MainWindow


# from PyQt5.QtCore import QTimer
# from PyQt5.Qt import QQEvent import QMouseEvent


# def ui_init(self, MainWindow, str_ver):
#     MainWindow.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", "自动测试系统客户端 " + str_ver))
#     MainWindow.label_foot.setText(QtCore.QCoreApplication.translate("MainWindow", str_ver))


class MyWindow(QMainWindow, Ui_MainWindow ):

    def __init__(self):
        super(MyWindow, self).__init__()
        self.str_version = "a"
        self.setupUi(self)

        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setMouseTracking(True)
        self.setMouseTracking(True)

        self.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow_cxd", "myPython"))
        self.statusbar.showMessage("")

        # ---- 初始化 -------------------------------------------------------------------
        self.file_path = './csv'
        self.file_name = 'calibration.xlsx'
        self.myExcel = MyExcel(self.file_path, self.file_name)

        # self.myZva = ZVA("ZVB8", "C:/Users/BRJX/Desktop/a")        # 初始化仪表
        self.myZva = ZVA('ZNB20', 'C:/Users/BRJX/Desktop/a', '192.168.1.20')        # 初始化仪表 － 空工矢网
        # self.myZva = ZVA('ZVA50', 'C:/Users/BRJX/Desktop/a', '192.168.1.15')        # 初始化仪表 － 公司矢网

        self.myRSRFSin = RSRFSin('SMF', '192.168.1.121')           # 初始化仪表 － 空工信号源
        self.myRSFSx = RSFSx('FSW', '192.168.1.81')           # 初始化仪表 － 空工频谱仪

        # 初始化 日志
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s : %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

        self.mylog = MyLog()
        self.mylog.DBG_MOD = DbgMod.DEBUG

        try:
            self.mylog.trigger.connect(self.getData)
        except Exception as e:
            print(e)
        else:
            print("try ok")

        # 初始化线程
        self.myThread = MyThread()

        # ---- 鼠标状态 -------------------------------------------------------------------
        self.bt_test.setMouseTracking(True)
        self.bt_test_2.setMouseTracking(True)
        self.bt_3_link.setMouseTracking(True)
        self.bt_4_begin.setMouseTracking(True)
        self.bt_4_begin.setMouseTracking(True)

        self.label_3_link.setMouseTracking(True)
        self.label_4_begin.setMouseTracking(True)
        self.label_foot.setMouseTracking(True)

        self.statusbar.setMouseTracking(True)
        # self.textEdit.setMouseTracking(True)

        # ---- 颜色设置 -------------------------------------------------------------------
        self.color_bt_disable = 'background-color:#cccccc'
        self.color_bt_on = 'background-color:#00aa00'
        self.color_bt_off = 'background-color:#aa0000'

        # ---- 控件状态 -------------------------------------------------------------------
        self.bt_3_linked = False
        self.bt_7_linked = False
        self.bt_8_linked = False
        self.bt_6_rfctrl_on = False

        self.bt_4_begin.setEnabled(False)
        self.bt_5_send.setEnabled(False)
        self.bt_6_rfctrl.setEnabled(False)
        self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

    def refresh(self, str_title):
        self.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow", str_title))
        self.statusbar.showMessage(str_title)

    # ---- 控件 -------------------------------------------------------------------
    def set_text(self, str_a):
        self.textEdit.append(str_a)

    def clear(self):
        self.textEdit.set_text("")

    # ---- test 按钮 -------------------------------------------------------------------
    def bt_test_click(self):
        self.set_text("begin")

        # 线程测试
        self.myThread = MyThread()
        self.myThread.trigger.connect(self.te_append_text)
        self.myThread.start()

        # Excel
        self.myExcel.open_file()
        self.myExcel.print_rows('Sheet1')

    def te_append_text(self, msg):
        self.textEdit.append(msg)

    def getData(self, msg):
        self.textEdit.append(msg)
        self.textEdit.moveCursor(QTextCursor.End)       # 移动到最后一行

    def bt_test_2_click(self):
        self.textEdit.setText("")

    # ---- 连接矢网 按钮 -------------------------------------------------------------------
    def bt_3_link_click(self):

        if not self.bt_3_linked:        # 未连接状态，开始连接

            self.myZva.open_inst()

            if self.myZva.linkState == 1:                           # 连接成功
                logging.debug("ZVA connect ok")
                self.bt_3_linked = True
                self.bt_3_link.setText("断开矢网")
                # print("link ZVA ok")
                self.label_3_link.setText("ZVA 已连接")

                self.bt_4_begin.setEnabled(True)
                self.bt_5_send.setEnabled(True)
                self.bt_6_rfctrl.setEnabled(True)

                if self.bt_6_rfctrl_on:
                    self.bt_6_rfctrl.setStyleSheet(self.color_bt_on)
                else:
                    self.bt_6_rfctrl.setStyleSheet(self.color_bt_off)

                self.bt_7_link_smf.setEnabled(False)
                self.bt_8_link_fsw.setEnabled(False)

            else:                                                   # 连接失败
                # print("link ZVA error!")
                self.bt_3_link.setText("连接矢网")
                self.label_3_link.setText("连接矢网")
                self.bt_4_begin.setEnabled(False)
                self.bt_5_send.setEnabled(False)
                self.bt_6_rfctrl.setEnabled(False)
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

                self.bt_7_link_smf.setEnabled(True)
                self.bt_8_link_fsw.setEnabled(True)

                logging.debug("connect ZVA error")

                try:
                    # self.mylog.logout(DbgMod.DEBUG, "mylog: connect ZVA error")
                    self.mylog.log_error("mylog: connect ZVA error")
                except Exception as e:
                    print(e)

        else:                               # 当前是已连接状态，断开连接
            self.bt_3_linked = False
            self.bt_3_link.setText("连接仪表")
            self.label_3_link.setText("连接仪表")
            self.bt_4_begin.setEnabled(False)
            self.bt_5_send.setEnabled(False)

            if self.bt_6_rfctrl_on:
                self.bt_6_rfctrl.click()            # 关闭射频

            self.bt_6_rfctrl.setEnabled(False)
            self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

            if self.myZva.linkState == 1:           # 已连接，断开连接
                self.myZva.close_inst()

            self.bt_7_link_smf.setEnabled(True)
            self.bt_8_link_fsw.setEnabled(True)

    def bt_4_begin_click(self):
        # self.myZva.mark_data()
        a = self.myZva.P1_data("10", "-0", "1000000000")

        self.mylog.logout(DbgMod.DEBUG, str(a))

    # ---- 发送指令 --------------------------------------------
    def bt_5_send_click(self):

        global str_rf_isOn

        str_utf = self.te_2_send.toPlainText().encode('utf-8')      # 转为 utf-8
        str_a = str_utf.decode('utf-8')                             # 变为 ANSI

        try:
            if self.bt_3_linked:                            # 矢网
                val = self.myZva.send_cmd(str_a)
                str_rf_isOn = self.myZva.send_cmd('OUTP?')

                self.mylog.logout(DbgMod.DEBUG, val)

            elif self.bt_7_linked:                          # 信号源
                val = self.myRSRFSin.send_cmd(str_a)
                str_rf_isOn = int(str(self.myRSRFSin.send_cmd('OUTP?').split(':')[-1]).strip())

                self.mylog.logout(DbgMod.DEBUG, val)
                # self.mylog.logout(DbgMod.DEBUG, str(str_rf_isOn))

            elif self.bt_8_linked:                          # 频谱仪
                val = self.myRSFSx.send_cmd(str_a)

                self.mylog.logout(DbgMod.DEBUG, val)
                # self.mylog.logout(DbgMod.DEBUG, str(str_rf_isOn))

            if not self.bt_8_linked:            # 设置 射频开关，频谱仪不处理
                if str_rf_isOn == 1:           # 射频已打开
                    self.bt_6_rfctrl_on = True
                else:
                    self.bt_6_rfctrl_on = False

            self.bt_6_set_state()

        except Exception as e:
            self.mylog.logout(DbgMod.DEBUG, str(e))

    # ---- 射频开关 -------------------------------------------
    def bt_6_rfctrl_click(self):

        try:
            if self.bt_6_rfctrl_on:                         # 射频 已打开
                self.bt_6_rfctrl_on = False

                if self.bt_3_linked:                        # 矢网 已连接
                    str_cmd = 'OUTP OFF'
                    self.myZva.send_cmd(str_cmd)

                elif self.bt_7_linked:                      # 信号源 已连接
                    str_cmd = 'OUTP OFF'
                    self.myRSRFSin.send_cmd(str_cmd)

                elif self.bt_8_linked:                      # 频谱仪
                    str_cmd = 'OUTP OFF'
                    self.myRSFSx.send_cmd(str_cmd)

            else:                                          # 射频 已关闭
                self.bt_6_rfctrl_on = True

                if self.bt_3_linked:                        # 矢网
                    str_cmd = 'OUTP ON'
                    self.myZva.send_cmd(str_cmd)

                elif self.bt_7_linked:                      # 信号源
                    str_cmd = 'OUTP ON'
                    self.myRSRFSin.send_cmd(str_cmd)

                elif self.bt_8_linked:                      # 频谱仪
                    str_cmd = 'OUTP ON'
                    self.myRSFSx.send_cmd(str_cmd)

            self.bt_6_set_state()

        except Exception as e:
            self.mylog.log_error(str(e))

    def bt_6_set_state(self):
        if self.bt_8_linked:                            # 频谱仪 打开，射频输入类
            self.bt_6_rfctrl.setText('RF ON')
            self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

        else:                                           # 射频 输出类
            if self.bt_6_rfctrl_on:                         # 射频 已打开
                self.bt_6_rfctrl.setText('RF ON')
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_on)

            else:                                          # 射频 已关闭
                self.bt_6_rfctrl.setText('RF OFF')
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_off)

    # ---- 信号源 连接 -------------------------------------
    def bt_7_link_smf_click(self):

        # 互斥操作 --------------------------
        if self.bt_3_linked:
            self.bt_3_link.click()

        if self.bt_8_linked:
            self.bt_8_lin_fsw_click()
        # 操作 --------------------------
        if not self.bt_7_linked:        # 未连接状态，开始连接

            self.myRSRFSin.open_inst()

            if self.myRSRFSin.linkState == 1:                           # 连接成功
                logging.debug("SMF connect ok")
                self.bt_7_linked = True
                # print("link ZVA ok")
                self.bt_7_link_smf.setText("断开信号源")

                self.bt_4_begin.setEnabled(True)
                self.bt_5_send.setEnabled(True)
                self.bt_6_rfctrl.setEnabled(True)

                # ---- 读取射频开关状态 --------------
                str_smr_rf_isOn = int(str(self.myRSRFSin.send_cmd('OUTP?').split(':')[-1]).strip())

                if str_smr_rf_isOn == 1:  # 射频已打开
                    self.bt_6_rfctrl_on = True
                else:
                    self.bt_6_rfctrl_on = False

                # ---- 设置开关颜色 --------------------
                self.bt_6_set_state()

                self.bt_3_link.setEnabled(False)
                self.bt_8_link_fsw.setEnabled(False)

                self.mylog.log_ok("mylog: connect SMF ok")

            else:                                                   # 连接失败
                # print("link ZVA error!")
                self.bt_7_link_smf.setText("连接信号源")
                self.bt_4_begin.setEnabled(False)
                self.bt_5_send.setEnabled(False)
                self.bt_6_rfctrl.setEnabled(False)
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

                self.bt_3_link.setEnabled(True)
                self.bt_8_link_fsw.setEnabled(True)

                logging.debug("connect SMF error")

                try:
                    # self.mylog.logout(DbgMod.DEBUG, "mylog: connect ZVA error")
                    self.mylog.log_error("mylog: connect SMF error")
                except Exception as e:
                    print(e)

        else:                               # 当前是已连接状态，断开连接
            if self.bt_6_rfctrl_on:
                self.bt_6_rfctrl.click()            # 关闭射频

            self.bt_7_linked = False
            self.bt_7_link_smf.setText("连接信号源")
            self.bt_4_begin.setEnabled(False)
            self.bt_5_send.setEnabled(False)

            self.bt_6_rfctrl.setEnabled(False)
            self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

            self.bt_3_link.setEnabled(True)
            self.bt_8_link_fsw.setEnabled(True)

            if self.myRSRFSin.linkState == 1:
                self.myRSRFSin.close_inst()

    # ---- 连接 频谱仪 ---------------------
    def bt_8_lin_fsw_click(self):
        # 互斥操作 --------------------------
        if self.bt_3_linked:
            self.bt_3_link.click()

        if self.bt_7_linked:
            self.bt_7_link_smf_click()
        # 操作 --------------------------
        if not self.bt_8_linked:        # 未连接状态，开始连接

            self.myRSFSx.open_inst()

            if self.myRSFSx.linkState == 1:                           # 连接成功
                logging.debug("FSW connect ok")
                self.bt_8_linked = True
                # print("link ZVA ok")
                self.bt_8_link_fsw.setText("断开频谱仪")

                self.bt_4_begin.setEnabled(True)
                self.bt_5_send.setEnabled(True)
                # self.bt_6_rfctrl.setEnabled(True)                     # 射频不输出，不控

                # ---- 读取射频开关状态 --------------
                # str_fsw_rf_isOn = int(str(self.myRSFSx.send_cmd('OUTP?').split(':')[-1]).strip())
                #
                # if str_fsw_rf_isOn == 1:  # 射频已打开
                #     self.bt_6_rfctrl_on = True
                # else:
                #     self.bt_6_rfctrl_on = False

                # ---- 设置开关颜色 --------------------
                # self.bt_6_set_state()

                self.bt_3_link.setEnabled(False)
                self.bt_7_link_smf.setEnabled(False)

                self.mylog.log_ok("mylog: FSW connect ok")

            else:                                                   # 连接失败
                # print("link ZVA error!")
                self.bt_8_link_fsw.setText("连接频谱仪")
                self.bt_4_begin.setEnabled(False)
                self.bt_5_send.setEnabled(False)
                self.bt_6_rfctrl.setEnabled(False)
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

                self.bt_3_link.setEnabled(True)
                self.bt_7_link_smf.setEnabled(True)

                logging.debug("FSW connect error")

                try:
                    # self.mylog.logout(DbgMod.DEBUG, "mylog: connect ZVA error")
                    self.mylog.log_error("mylog: FSW connect error")
                except Exception as e:
                    print(e)

        else:                               # 当前是已连接状态，断开连接
            if self.bt_6_rfctrl_on:
                self.bt_6_rfctrl.click()            # 关闭射频

            self.bt_8_linked = False
            self.bt_8_link_fsw.setText("连接频谱仪")
            self.bt_4_begin.setEnabled(False)
            self.bt_5_send.setEnabled(False)

            self.bt_6_rfctrl.setEnabled(False)
            self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

            self.bt_3_link.setEnabled(True)
            self.bt_7_link_smf.setEnabled(True)

            if self.myRSFSx.linkState == 1:
                self.myRSFSx.close_inst()

    # def delay_time(self):
    #     time.sleep(5)
    #     print("end")

    # ---- 鼠标事件 -------------------------------------------------------------------
    # class MyMouse(QMainWindow, Ui_MainWindow):
    #
    #     def __init__(self, parent=None):
    #         super(MyMouse, self).__init__(parent)

    '''重载一下鼠标按下事件(单击)'''
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:  # 左键按下
            # self.textEdit.append("单击鼠标左键的事件: 自己定义")
            print("单击鼠标左键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.RightButton:  # 右键按下
            # self.textEdit.append("单击鼠标右键的事件: 自己定义")
            print("单击鼠标右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton:  # 中键按下
            # self.textEdit.append("单击鼠标中键的事件: 自己定义")
            print("单击鼠标中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.RightButton:  # 左右键同时按下
            # self.textEdit.append("同时单击鼠标左右键的事件: 自己定义")
            print("单击鼠标左右键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton:  # 左中键同时按下
            # self.textEdit.append("同时单击鼠标左中键的事件: 自己定义")
            print("单击鼠标左中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 右中键同时按下
            # self.textEdit.append("同时单击鼠标右中键的事件: 自己定义")
            print("单击鼠标右中键")  # 响应测试语句
        elif event.buttons() == QtCore.Qt.LeftButton | QtCore.Qt.MidButton | QtCore.Qt.RightButton:  # 左中右键同时按下
            # self.textEdit.append("同时单击鼠标左中右键的事件: 自己定义")
            print("单击鼠标左中右键")  # 响应测试语句

    '''重载一下滚轮滚动事件'''
    def wheelEvent(self, event):
        #        if event.delta() > 0:                                                 # 滚轮上滚,PyQt4
        # This function has been deprecated, use pixelDelta() or angleDelta() instead.
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleX = angle.x()  # 水平滚过的距离(此处用不上)
        angleY = angle.y()  # 竖直滚过的距离

        # if angleX > 0:
        #     self.textEdit.append("wheel roll → 滚动的事件: 自己定义")
        #     print("鼠标滚轮右滚")  # 响应测试语句
        # else:  # 滚轮下滚
        #     self.textEdit.append("wheel roll ← 滚动的事件: 自己定义")
        #     print("鼠标滚轮左滚")  # 响应测试语句

        if angleY > 0:
            # self.textEdit.append("wheel roll ↑ 滚动的事件: 自己定义")
            print("鼠标滚轮上滚")  # 响应测试语句
        else:  # 滚轮下滚
            # self.textEdit.append("wheel roll ↓ 滚动的事件: 自己定义")
            print("鼠标滚轮下滚")  # 响应测试语句

    '''重载一下鼠标双击事件'''
    def mouseDoubleClickEvent(self, event):
        # if event.buttons () == QtCore.Qt.LeftButton:                           # 左键按下
        # self.setText ("双击鼠标左键的功能: 自己定义")
        self.textEdit.append("鼠标双击事件: 自己定义")

    '''重载一下鼠标键释放事件'''
    def mouseReleaseEvent(self, event):
        # self.textEdit.append("鼠标释放事件: 自己定义")
        print("鼠标释放")  # 响应测试语句

    '''重载一下鼠标移动事件'''
    def mouseMoveEvent(self, event):
        pos = event.pos()
        # print(pos)

        self.statusbar.showMessage("x=%d, y=%d" % (pos.x(), pos.y()))

        # self.textEdit.append("鼠标移动事件: 自己定义")
        # print("鼠标移动")  # 响应测试语句

    '''重载一下鼠标进入控件事件'''
    def enterEvent(self, event):
        pass

    '''重载一下鼠标离开控件事件'''
    def leaveEvent(self, event):
        pass
