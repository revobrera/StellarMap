import os
import sys


import numpy as np
import pandas as pd
import scipy.stats
from PyQt5 import QtCore, uic
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from openpyxl import load_workbook
import qtvscodestyle as qtvsc


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('D:\python_projects\\revobrera\GUI.ui', self)
        # stylesheet = qtvsc.load_stylesheet('D:\python_projects\\revobrera\windows-terminal-aurelia-master\posh-theme\purple-man.json')

        File = QtCore.QFile('D:\python_projects\\revobrera\windows-terminal-aurelia-master\posh-theme\purple-man.json')
        if not File.open( QtCore.QFile.ReadOnly | QtCore.QFile.Text):
            return
        print('here')
        qss = QtCore.QTextStream(File)
        # setup stylesheet
        app.setStyleSheet(qss.readAll())
        # app.setStyleSheet(stylesheet)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())