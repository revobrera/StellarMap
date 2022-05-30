
import numpy as np
import pandas as pd
import scipy.stats
from PyQt5 import QtCore, uic
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QWidget, QVBoxLayout
from openpyxl import load_workbook
import qtvscodestyle as qtvsc
import sys

class embeddedTerminal(QWidget):

    def __init__(self):

        QWidget.__init__(self)
        self.resize(800, 600)
        self.process  = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        self.process.start(
            'xterm',
            ['-into', str(self.terminal.winId())]
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = embeddedTerminal()
    main.show()
    sys.exit(app.exec_())
