#!/usr/bin/python3
# from psutil import *        # 获取所有网卡
# from enum import Enum, unique
from enum import IntEnum, unique
from PyQt5 import QtCore
from PyQt5.QtCore import QObject
import time


@unique
class DbgMod(IntEnum):
    DEBUG = 0
    INFO = 1
    WORN = 2
    ERROR = 3
    FATAL = 4


class MyLog(QObject):

    trigger = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MyLog, self).__init__()
        self.DBG_MOD = 0

    def set_debug(self, dbg_mod):
        if dbg_mod <= DbgMod.FATAL:
            self.DBG_MOD = dbg_mod
        else:
            print("Mylog: DBG_MOD set error!")
            self.trigger.emit("DBG_MOD set error!")

    def logout(self, dbg_mod, log_str):
        if dbg_mod >= self.DBG_MOD:
            self.trigger.emit(log_str)
            print("Mylog: " + log_str)

    def log_ok(self, log_str):
        a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        str_print = "%s : \033[1;31;38m%s \033[0m" % (a, log_str)
        # str_log = a + " : <font color=#ff0000\">" + log_str + "</font><font color=\"#000000\">" + "<&nbsp;/font>"
        # str_log = a + ' : <font color=\"#ff0000\">' + log_str + '</font>'
        str_log = a + ' : <font color="green">' + log_str + '</font> <font color="black"/>'
        # str_log = a + log_str
        self.trigger.emit(str_log)
        print("Mylog: " + str_print)

    def log_error(self, log_str):
        a = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        str_print = "%s : \033[1;31;38m%s \033[0m" % (a, log_str)
        # str_log = a + " : <font color=#ff0000\">" + log_str + "</font><font color=\"#000000\">" + "<&nbsp;/font>"
        # str_log = a + ' : <font color=\"#ff0000\">' + log_str + '</font>'
        str_log = a + ' : <font color="red">' + log_str + '</font> <font color="black"/>'
        # str_log = a + log_str
        self.trigger.emit(str_log)
        print("Mylog: " + str_print)
