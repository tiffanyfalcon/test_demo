# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
#

import time
from PyQt5.QtCore import QThread, QMutex, pyqtSignal


myQmutex = QMutex()


class MyThread(QThread):

    trigger = pyqtSignal(str)

    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        myQmutex.lock()               # 线程加锁
        for i in range(5):
            time.sleep(1)
            self.trigger.emit(str(i))

        print("end")
        self.trigger.emit("end")
        myQmutex.unlock()             # 线程解锁
