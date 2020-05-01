#!/usr/bin/python3

# import visa

import sys

from PyQt5 import QtWidgets

from view.ui_main_init import MyWindow

# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import QApplication, QMainWindow
# from view import ui_main
# import view.ui_main


str_version         = " V1.06"
str_date            = " 2020-05-01"
str_auther          = " ChenXudong"
str_company         = " Xian BRJX"
str_software_name   = " Near Feild Test"

str_foot = "\n" + str_company + str_software_name + ", Ver:" + str_version + "  date:" + str_date + \
            "\n designed by" + str_auther

str_title = str_software_name + str_version

print(str_foot)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QMainWindow()
    # ui = view.ui_main.Ui_MainWindow()
    # ui.setupUi(MainWindow)
    ui = MyWindow()
    # ui.str_version = str_software_name;
    # ui.setWindowTitle(QtCore.QCoreApplication.translate("MainWindow111", "自动测试系统客户端"))
    # ui.str_version = str_version

    ui.show()
    ui.refresh(str_title)

    # mywindow.show()
    sys.exit(app.exec_())


# **** 主程序 ********************************************************


# ---- 读取配置 ------------------------------------------------------


# ---- 判断序列号 ------------------------------------------------------

# ---- 比较网表 ------------------------------------------------------
# str30Netfile1 += r'.\pstxnet1.dat'
# str30Netfile1 += r'.\【内部】dialcnet.txt'
# strNetfile2 += r'.\pstxnet2.dat'
# strNetfile2 += r'.\【内部】dialcnet2.txt'
# strOutfile += r'.\net3.csv'

# nc.setFileName(strNetfile1, strNetfile2, strOutfile)


# ---- 打印 ------------------------------------------------------

