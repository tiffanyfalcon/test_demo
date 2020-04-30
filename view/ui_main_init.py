# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
#

from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore
import time
# from PyQt5.QtCore import QTimer
# from PyQt5.Qt import QQEvent import QMouseEvent

from view.ui_main import Ui_MainWindow
from view.M_thread import MyThread
from lib.remoteGet import ZVA
import logging
from lib.myLog import MyLog, DbgMod


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

        # self.myZva = ZVA("ZVB8", "C:/Users/BRJX/Desktop/a")        # 初始化仪表
        # self.myZva = ZVA('ZNB20', 'C:/Users/BRJX/Desktop/a', '192.168.1.20')        # 初始化仪表
        self.myZva = ZVA('ZVA50', 'C:/Users/BRJX/Desktop/a', '192.168.1.15')        # 初始化仪表

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

    # ---- 按钮事件 -------------------------------------------------------------------
    def bt_test_click(self):
        self.set_text("begin")

        # 线程测试
        self.myThread = MyThread()
        self.myThread.trigger.connect(self.te_append_text)
        self.myThread.start()

    def te_append_text(self, msg):
        self.textEdit.append(msg)

    def getData(self, msg):
        self.textEdit.append(msg)
        self.textEdit.moveCursor(QTextCursor.End)       # 移动到最后一行

    def bt_test_2_click(self):
        self.textEdit.setText("")

    def bt_3_link_click(self):

        if not self.bt_3_linked:        # 未连接状态，开始连接

            self.myZva.open_inst()

            if self.myZva.linkState == 1:                           # 连接成功
                logging.debug("ZVA connect ok")
                self.bt_3_linked = True
                self.bt_3_link.setText("断开仪表")
                # print("link ZVA ok")
                self.bt_3_link.setText("断开连接")
                self.label_3_link.setText("ZVA 已连接")

                self.bt_4_begin.setEnabled(True)
                self.bt_5_send.setEnabled(True)
                self.bt_6_rfctrl.setEnabled(True)
                if self.bt_6_rfctrl_on:
                    self.bt_6_rfctrl.setStyleSheet(self.color_bt_on)
                else:
                    self.bt_6_rfctrl.setStyleSheet(self.color_bt_off)

            else:                                                   # 连接失败
                # print("link ZVA error!")
                self.bt_3_link.setText("断开连接")
                self.label_3_link.setText("连接仪表")
                self.bt_4_begin.setEnabled(False)
                self.bt_5_send.setEnabled(False)
                self.bt_6_rfctrl.setEnabled(False)
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_disable)

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

            if self.myZva.linkState == 1:
                self.myZva.close_inst()

    def bt_4_begin_click(self):
        # self.myZva.mark_data()
        a = self.myZva.P1_data("10", "-0", "1000000000")

        self.mylog.logout(DbgMod.DEBUG, str(a))

    def bt_5_send_click(self):
        str_utf = self.te_2_send.toPlainText().encode('utf-8')
        str_a = str_utf.decode('utf-8')
        try:
            val = self.myZva.send_cmd(str_a)
            self.mylog.logout(DbgMod.DEBUG, val)
        except Exception as e:
            self.mylog.logout(DbgMod.DEBUG, e)

    def bt_6_rfctrl_click(self):

        try:
            if self.bt_6_rfctrl_on:
                self.bt_6_rfctrl_on = False
                self.bt_6_rfctrl.setText('RF OFF')
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_off)
                str_cmd = 'OUTP OFF'
                self.myZva.send_cmd(str_cmd)

            else:
                self.bt_6_rfctrl_on = True
                self.bt_6_rfctrl.setText('RF ON')
                self.bt_6_rfctrl.setStyleSheet(self.color_bt_on)
                str_cmd = 'OUTP ON'
                self.myZva.send_cmd(str_cmd)

        except Exception as e:
            self.mylog.log_error(str(e))

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

        self.statusbar.showMessage("x=%d, y=%d" %(pos.x(), pos.y()))

        # self.textEdit.append("鼠标移动事件: 自己定义")
        # print("鼠标移动")  # 响应测试语句

    '''重载一下鼠标进入控件事件'''
    def enterEvent(self, event):
        pass

    '''重载一下鼠标离开控件事件'''
    def leaveEvent(self, event):
        pass
